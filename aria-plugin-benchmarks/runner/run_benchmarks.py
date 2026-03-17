#!/usr/bin/env python3
"""
Aria Plugin Skill Benchmark Runner

Executes real skill evaluations against a test project using `claude -p`.
Validates outputs against regex assertions and generates grading/timing data.

Usage:
    python run_benchmarks.py                    # Run all enabled skills
    python run_benchmarks.py --skill state-scanner  # Run single skill
    python run_benchmarks.py --dry-run          # Show what would run
"""

import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone

# Fix Windows console encoding for Chinese output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / "config.json"


def load_config():
    with open(CONFIG_FILE, encoding="utf-8") as f:
        return json.load(f)


def run_claude(prompt, cwd, skill_name=None, timeout=120, model="sonnet"):
    """Execute a prompt via claude -p and return result + timing."""
    cmd = ["claude", "-p", "--output-format", "json"]
    if model:
        cmd.extend(["--model", model])

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    # Ensure npm-global bin is in PATH for claude CLI
    npm_global_bin = os.path.expanduser("~/.npm-global/bin")
    if npm_global_bin not in env.get("PATH", ""):
        env["PATH"] = npm_global_bin + os.pathsep + env.get("PATH", "")

    start = time.time()
    try:
        proc = subprocess.run(
            cmd,
            input=prompt.encode("utf-8"),
            capture_output=True,
            cwd=cwd,
            timeout=timeout,
            env=env,
        )
        # Decode as UTF-8 explicitly to handle Chinese output on Windows
        proc_stdout = proc.stdout.decode("utf-8", errors="replace")
        proc_stderr = proc.stderr.decode("utf-8", errors="replace")
        duration = time.time() - start
        stdout = proc_stdout.strip()

        if not stdout:
            return {
                "result": proc_stderr or "No output",
                "total_tokens": 0,
                "duration_ms": int(duration * 1000),
                "cost_usd": 0,
                "error": True,
            }

        try:
            data = json.loads(stdout)
            return {
                "result": data.get("result", ""),
                "total_tokens": data.get("usage", {}).get("input_tokens", 0)
                + data.get("usage", {}).get("output_tokens", 0),
                "duration_ms": data.get("duration_ms", int(duration * 1000)),
                "cost_usd": data.get("total_cost_usd", 0),
                "error": data.get("is_error", False),
                "raw": data,
            }
        except json.JSONDecodeError:
            return {
                "result": stdout,
                "total_tokens": 0,
                "duration_ms": int(duration * 1000),
                "cost_usd": 0,
                "error": False,
            }

    except subprocess.TimeoutExpired:
        return {
            "result": "TIMEOUT after %ds" % timeout,
            "total_tokens": 0,
            "duration_ms": int(timeout * 1000),
            "cost_usd": 0,
            "error": True,
        }
    except Exception as e:
        return {
            "result": "ERROR: " + str(e),
            "total_tokens": 0,
            "duration_ms": 0,
            "cost_usd": 0,
            "error": True,
        }


def check_assertion(output, assertion):
    """Check a single assertion against output using regex."""
    pattern = assertion["check"]
    try:
        match = re.search(pattern, output, re.IGNORECASE | re.MULTILINE)
        return {
            "text": assertion["text"],
            "passed": match is not None,
            "evidence": (
                "Matched: '%s'" % match.group()[:100]
                if match
                else "Pattern '%s' not found in output" % pattern
            ),
        }
    except re.error as e:
        return {
            "text": assertion["text"],
            "passed": False,
            "evidence": "Regex error: " + str(e),
        }


def run_eval(skill_name, eval_def, config):
    """Run a single evaluation."""
    project_dir = config["test_project"]
    timeout = config.get("timeout_seconds", 120)
    model = config.get("model", "sonnet")

    eval_id = eval_def["id"]
    eval_name = eval_def["name"]
    prompt = eval_def["prompt"]

    print("  [%s] %s ..." % (eval_id, eval_name), end=" ", flush=True)

    # Run setup command if defined
    if "setup" in eval_def:
        subprocess.run(
            eval_def["setup"],
            shell=True,
            cwd=project_dir,
            capture_output=True,
        )

    # Execute skill via claude -p
    result = run_claude(prompt, cwd=project_dir, skill_name=skill_name,
                        timeout=timeout, model=model)

    # Run cleanup if defined
    if "cleanup" in eval_def:
        subprocess.run(
            eval_def["cleanup"],
            shell=True,
            cwd=project_dir,
            capture_output=True,
        )

    # Check assertions
    output = result["result"]
    assertion_results = []
    for assertion in eval_def.get("assertions", []):
        assertion_results.append(check_assertion(output, assertion))

    total_a = len(assertion_results)
    passed_a = sum(1 for a in assertion_results if a["passed"])
    all_passed = passed_a == total_a

    if all_passed:
        print("PASS (%d/%d) [%.1fs]" % (passed_a, total_a, result["duration_ms"] / 1000))
    else:
        print("FAIL (%d/%d) [%.1fs]" % (passed_a, total_a, result["duration_ms"] / 1000))
        for a in assertion_results:
            if not a["passed"]:
                print("    FAIL: %s - %s" % (a["text"], a["evidence"]))

    return {
        "eval_id": eval_id,
        "eval_name": eval_name,
        "skill": skill_name,
        "output": output,
        "grading": {
            "eval_id": eval_id,
            "eval_name": eval_name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "assertions": assertion_results,
            "verdict": "PASS" if all_passed else "FAIL",
            "pass_rate": passed_a / total_a if total_a > 0 else 0,
        },
        "timing": {
            "total_tokens": result["total_tokens"],
            "duration_ms": result["duration_ms"],
            "total_duration_seconds": round(result["duration_ms"] / 1000, 1),
            "cost_usd": result.get("cost_usd", 0),
        },
        "error": result.get("error", False),
    }


def save_results(skill_name, eval_result, output_dir):
    """Save eval results to disk."""
    eval_id = eval_result["eval_id"]
    eval_dir = Path(output_dir) / skill_name / ("eval-%s" % eval_id)
    output_subdir = eval_dir / "with_skill" / "outputs"
    output_subdir.mkdir(parents=True, exist_ok=True)

    # Save output
    with open(output_subdir / "result.txt", "w", encoding="utf-8") as f:
        f.write(eval_result["output"])

    # Save grading
    with open(eval_dir / "grading.json", "w", encoding="utf-8") as f:
        json.dump(eval_result["grading"], f, ensure_ascii=False, indent=2)
        f.write("\n")

    # Save timing
    with open(eval_dir / "timing.json", "w", encoding="utf-8") as f:
        json.dump(eval_result["timing"], f, ensure_ascii=False, indent=2)
        f.write("\n")


def generate_summary(skill_name, results):
    """Generate a skill-level benchmark summary."""
    total = len(results)
    passed = sum(1 for r in results if r["grading"]["verdict"] == "PASS")
    total_tokens = sum(r["timing"]["total_tokens"] for r in results)
    total_time = sum(r["timing"]["duration_ms"] for r in results)
    total_cost = sum(r["timing"].get("cost_usd", 0) for r in results)

    return {
        "benchmark_name": skill_name,
        "test_type": "real_execution",
        "test_project": "todo-web",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_evals": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": passed / total if total > 0 else 0,
        "total_tokens": total_tokens,
        "total_duration_ms": total_time,
        "total_cost_usd": round(total_cost, 4),
        "eval_results": [
            {
                "eval_id": r["eval_id"],
                "eval_name": r["eval_name"],
                "verdict": r["grading"]["verdict"],
                "pass_rate": r["grading"]["pass_rate"],
                "tokens": r["timing"]["total_tokens"],
                "duration_ms": r["timing"]["duration_ms"],
                "failed_assertions": [
                    a["text"]
                    for a in r["grading"]["assertions"]
                    if not a["passed"]
                ],
            }
            for r in results
        ],
    }


def main():
    config = load_config()
    output_dir = Path(config["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    # Parse CLI args
    target_skill = None
    dry_run = False
    for arg in sys.argv[1:]:
        if arg == "--dry-run":
            dry_run = True
        elif arg == "--skill":
            pass
        elif sys.argv[sys.argv.index(arg) - 1] == "--skill":
            target_skill = arg

    skills = config["skills"]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = output_dir / ("run_%s" % timestamp)

    print("=" * 60)
    print("Aria Plugin Benchmark Runner")
    print("=" * 60)
    print("Test project: %s" % config["test_project"])
    print("Model: %s" % config.get("model", "default"))
    print("Output: %s" % run_dir)
    print()

    all_summaries = {}
    total_evals = 0
    total_passed = 0
    total_cost = 0

    for skill_name, skill_config in skills.items():
        if target_skill and skill_name != target_skill:
            continue
        if not skill_config.get("enabled", True):
            continue

        evals = skill_config.get("evals", [])
        if not evals:
            continue

        print("[%s] Running %d eval(s)..." % (skill_name, len(evals)))

        if dry_run:
            for ev in evals:
                print("  [%s] %s: %s" % (ev["id"], ev["name"], ev["prompt"][:60]))
            print()
            continue

        skill_results = []
        for ev in evals:
            result = run_eval(skill_name, ev, config)
            save_results(skill_name, result, run_dir)
            skill_results.append(result)

        summary = generate_summary(skill_name, skill_results)
        all_summaries[skill_name] = summary

        # Save skill summary
        skill_dir = run_dir / skill_name
        skill_dir.mkdir(parents=True, exist_ok=True)
        with open(skill_dir / "benchmark.json", "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
            f.write("\n")

        total_evals += summary["total_evals"]
        total_passed += summary["passed"]
        total_cost += summary.get("total_cost_usd", 0)
        print()

    if dry_run:
        print("Dry run complete.")
        return

    # Save overall summary
    overall = {
        "runner_version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "test_project": config["test_project"],
        "model": config.get("model", "default"),
        "total_skills": len(all_summaries),
        "total_evals": total_evals,
        "total_passed": total_passed,
        "total_failed": total_evals - total_passed,
        "overall_pass_rate": (
            round(total_passed / total_evals, 4) if total_evals > 0 else 0
        ),
        "total_cost_usd": round(total_cost, 4),
        "skills": all_summaries,
    }

    with open(run_dir / "summary.json", "w", encoding="utf-8") as f:
        json.dump(overall, f, ensure_ascii=False, indent=2)
        f.write("\n")

    # Print final report
    print("=" * 60)
    print("FINAL REPORT")
    print("=" * 60)
    print("Skills tested: %d" % len(all_summaries))
    print("Total evals:   %d" % total_evals)
    print("Passed:        %d" % total_passed)
    print("Failed:        %d" % (total_evals - total_passed))
    print(
        "Pass rate:     %.1f%%"
        % (total_passed / total_evals * 100 if total_evals > 0 else 0)
    )
    print("Total cost:    $%.4f" % total_cost)
    print()
    print("Results saved to: %s" % run_dir)

    # Per-skill summary
    for name, s in all_summaries.items():
        status = "PASS" if s["pass_rate"] == 1.0 else "FAIL"
        print(
            "  %-30s %s (%d/%d) $%.4f"
            % (name, status, s["passed"], s["total_evals"], s.get("total_cost_usd", 0))
        )


if __name__ == "__main__":
    main()

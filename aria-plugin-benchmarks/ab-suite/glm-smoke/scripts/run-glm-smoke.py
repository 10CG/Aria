#!/usr/bin/env -S uv run --quiet --with jinja2 --with pyyaml --with requests
"""T3.4 GLM smoke test — M0 aria-2.0-m0-prerequisite.

Renders 5 Jinja2 templates, asks GLM (via Luxeno OpenAI-compat) to humanize
each into a user prompt, pipes each prompt through `claude -p` (routed to
Luxeno Anthropic-compat), and checks for state-scanner output markers.

Pass criterion (per Spec §T3.4): ≥4/5 samples match regex
`Phase/Cycle:|phase_cycle:` in claude -p stdout.

Secret: reads LUXENO_API_KEY from /tmp/.luxeno-key (KEY=VALUE format).
Never logs the key value.

Usage:
    uv run run-glm-smoke.py [--limit N] [--timestamp YYYYMMDD-HHMMSS]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import jinja2
import requests
import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
SUITE_DIR = SCRIPT_DIR.parent
TEMPLATES_DIR = SUITE_DIR / "templates"
ARCHIVE_DIR = SUITE_DIR / "failed-samples"

LUXENO_CHAT_URL = "https://api.luxeno.ai/v1/chat/completions"
LUXENO_ANTHROPIC_BASE = "https://api.luxeno.ai"  # claude CLI appends /v1/messages
GLM_MODEL_OPENAI = "glm-4.5"           # prompt generation (OpenAI-compat); spec says glm-4.7-flashx
                                        # but flashx returns 408 upstream timeouts on ≥800-char inputs
                                        # (Luxeno reliability finding 2026-04-17).
GLM_MODEL_ANTHROPIC = "glm-4.7"        # for claude -p (Anthropic-compat endpoint, flashx not supported)
EXPECTED_GREP = r"Phase/Cycle:|phase_cycle:"

TEMPLATES = [
    "01-initial-scan",
    "02-resume-after-break",
    "03-pre-action-guidance",
    "04-ambiguous-request",
    "05-anomaly-triage",
]


def load_secret(path: str = "/tmp/.luxeno-key") -> str:
    p = Path(path)
    if not p.exists():
        sys.exit(f"ERROR: secret file not found: {path}")
    raw = p.read_text().strip()
    for line in raw.splitlines():
        line = line.strip()
        if line.startswith("LUXENO_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    # Fallback: bare key format (entire file is the key itself)
    if raw and "\n" not in raw and "=" not in raw:
        return raw
    sys.exit(f"ERROR: could not parse key from {path} (expected bare key or LUXENO_API_KEY=<value>)")


def render_template(name: str, seed: str) -> str:
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=False,
        undefined=jinja2.StrictUndefined,
    )
    tpl = env.get_template(f"{name}.j2.md")
    return tpl.render(seed=seed, language="中文", register="casual")


def call_glm(system_prompt: str, api_key: str, max_retries: int = 2) -> str:
    payload = {
        "model": GLM_MODEL_OPENAI,
        "messages": [{"role": "user", "content": system_prompt}],
        "temperature": 0.8,
        # GLM models burn tokens on internal reasoning_content before content;
        # budget high enough for 40-100 字 output + reasoning overhead.
        "max_tokens": 800,
    }
    last_err = None
    for attempt in range(max_retries + 1):
        try:
            r = requests.post(
                LUXENO_CHAT_URL,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=60,
            )
            r.raise_for_status()
            data = r.json()
            if "error" in data:
                last_err = f"API error: {data['error']}"
                if attempt < max_retries:
                    print(f"  GLM retry {attempt+1}/{max_retries}: {last_err}", flush=True)
                    continue
                raise requests.HTTPError(last_err)
            content = data["choices"][0]["message"].get("content", "").strip()
            if not content:
                last_err = "empty content (likely max_tokens exhausted on reasoning)"
                if attempt < max_retries:
                    print(f"  GLM retry {attempt+1}/{max_retries}: {last_err}", flush=True)
                    continue
                raise RuntimeError(last_err)
            return content
        except requests.HTTPError as e:
            last_err = str(e)
            if attempt < max_retries:
                print(f"  GLM retry {attempt+1}/{max_retries}: HTTP {last_err[:80]}", flush=True)
                continue
            raise
    raise RuntimeError(f"GLM failed after {max_retries+1} attempts: {last_err}")


def run_claude_p(prompt: str, api_key: str, timeout_s: int = 120) -> tuple[str, str, int]:
    env = os.environ.copy()
    env["ANTHROPIC_BASE_URL"] = LUXENO_ANTHROPIC_BASE
    env["ANTHROPIC_API_KEY"] = api_key
    env["ANTHROPIC_MODEL"] = GLM_MODEL_ANTHROPIC
    try:
        proc = subprocess.run(
            # --permission-mode bypassPermissions: autonomous smoke test; GLM-4.7
            # otherwise asks for human approval before invoking Skills in -p mode.
            ["claude", "-p", "--permission-mode", "bypassPermissions", prompt],
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout_s,
        )
        return proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired as e:
        return (e.stdout or "", (e.stderr or "") + "\n[TIMEOUT]", -1)


def classify(stdout: str, stderr: str, rc: int) -> tuple[str, str]:
    if rc == -1:
        return "fail", "timeout"
    if re.search(EXPECTED_GREP, stdout):
        return "pass", ""
    if not stdout.strip():
        return "fail", "not_triggered"
    if "Phase" not in stdout and "phase" not in stdout:
        return "fail", "partial_response"
    return "fail", "triggered_invalid_yaml"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=5, help="number of templates to run (for dry-run)")
    ap.add_argument(
        "--timestamp",
        default=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        help="archive timestamp prefix",
    )
    ap.add_argument(
        "--only",
        help="comma-separated template base names to run (subset of default 5)",
    )
    ap.add_argument(
        "--mode",
        choices=["auto", "slash"],
        default="auto",
        help=(
            "auto = T3.4.a natural-language → Skill auto-invoke; "
            "slash = T3.4.b explicit /state-scanner invocation (tests Luxeno reliability + Skill routing, skips GLM pre-generation)"
        ),
    )
    args = ap.parse_args()

    api_key = load_secret()
    print(f"[load] secret loaded ({len(api_key)} chars, not logged)", flush=True)

    ARCHIVE_DIR.mkdir(exist_ok=True)
    run_dir = ARCHIVE_DIR / args.timestamp
    run_dir.mkdir(exist_ok=True)

    seeds = ["a1", "b2", "c3", "d4", "e5"]
    targets = TEMPLATES
    if args.only:
        selected = set(args.only.split(","))
        targets = [t for t in TEMPLATES if t in selected]
    targets = targets[: args.limit]

    results = []
    for idx, name in enumerate(targets, start=1):
        seed = seeds[TEMPLATES.index(name)]
        print(f"\n[{idx}/{len(targets)}] template={name} seed={seed} mode={args.mode}", flush=True)

        if args.mode == "auto":
            system_prompt = render_template(name, seed)
            print(f"  render OK ({len(system_prompt)} chars)", flush=True)
            try:
                generated_prompt = call_glm(system_prompt, api_key)
            except requests.HTTPError as e:
                print(f"  GLM HTTP error: {e} — recording as skip, continuing", flush=True)
                generated_prompt = ""
            except (requests.RequestException, RuntimeError) as e:
                print(f"  GLM error: {e} — recording as skip, continuing", flush=True)
                generated_prompt = ""
            if generated_prompt:
                print(f"  GLM OK ({len(generated_prompt)} chars)", flush=True)
                print(f"  → prompt: {generated_prompt[:100]}{'...' if len(generated_prompt)>100 else ''}", flush=True)
            else:
                print(f"  GLM FAIL — marking sample as fail/glm_error", flush=True)
        else:  # slash
            generated_prompt = "/state-scanner"
            print(f"  slash mode — prompt: '/state-scanner' (fixed)", flush=True)

        if not generated_prompt:
            # GLM generation failed — record and skip claude call
            sample = {
                "prompt": "",
                "failure_mode": "glm_generation_failed",
                "raw_output": "",
                "raw_stderr": "",
                "return_code": None,
                "expected_grep": EXPECTED_GREP,
                "glm_model_openai": GLM_MODEL_OPENAI,
                "glm_model_anthropic": GLM_MODEL_ANTHROPIC,
                "status": "fail",
                "template": name,
                "seed": seed,
                "mode": args.mode,
                "ran_at": datetime.now(timezone.utc).isoformat(),
            }
            sample_path = run_dir / f"{idx:02d}-{name}.yaml"
            sample_path.write_text(yaml.safe_dump(sample, allow_unicode=True, sort_keys=False), encoding="utf-8")
            print(f"  archived: {sample_path.relative_to(SUITE_DIR)}", flush=True)
            results.append(sample)
            continue

        print(f"  running claude -p (timeout 120s)...", flush=True)
        stdout, stderr, rc = run_claude_p(generated_prompt, api_key)
        status, failure_mode = classify(stdout, stderr, rc)
        print(f"  → status={status} rc={rc} stdout_len={len(stdout)} stderr_len={len(stderr)}", flush=True)
        if failure_mode:
            print(f"  → failure_mode={failure_mode}", flush=True)

        sample = {
            "prompt": generated_prompt,
            "failure_mode": failure_mode or None,
            "raw_output": stdout,
            "raw_stderr": stderr,
            "return_code": rc,
            "expected_grep": EXPECTED_GREP,
            "glm_model_openai": GLM_MODEL_OPENAI,
            "glm_model_anthropic": GLM_MODEL_ANTHROPIC,
            "status": status,
            "template": name,
            "seed": seed,
            "mode": args.mode,
            "ran_at": datetime.now(timezone.utc).isoformat(),
        }
        sample_path = run_dir / f"{idx:02d}-{name}.yaml"
        sample_path.write_text(
            yaml.safe_dump(sample, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
        print(f"  archived: {sample_path.relative_to(SUITE_DIR)}", flush=True)
        results.append(sample)

    # summary.yaml
    passed = sum(1 for r in results if r["status"] == "pass")
    total = len(results)
    summary = {
        "timestamp": args.timestamp,
        "mode": args.mode,
        "sub_test": "T3.4.a" if args.mode == "auto" else "T3.4.b",
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "threshold": 4 if total == 5 else None,
        "overall_pass": (passed >= 4) if total == 5 else None,
        "glm_model_openai": GLM_MODEL_OPENAI,
        "glm_model_anthropic": GLM_MODEL_ANTHROPIC,
        "samples": [
            {
                "index": i + 1,
                "template": r["template"],
                "status": r["status"],
                "failure_mode": r["failure_mode"],
                "path": f"{args.timestamp}/{i+1:02d}-{r['template']}.yaml",
            }
            for i, r in enumerate(results)
        ],
    }
    (run_dir / "summary.yaml").write_text(
        yaml.safe_dump(summary, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    print("\n====== SUMMARY ======", flush=True)
    print(f"  passed: {passed}/{total}", flush=True)
    if total == 5:
        verdict = "PASS" if passed >= 4 else "FAIL"
        print(f"  T3.4 verdict: {verdict} (threshold ≥4/5)", flush=True)
    print(f"  archive: failed-samples/{args.timestamp}/", flush=True)
    return 0 if (total < 5 or passed >= 4) else 1


if __name__ == "__main__":
    sys.exit(main())

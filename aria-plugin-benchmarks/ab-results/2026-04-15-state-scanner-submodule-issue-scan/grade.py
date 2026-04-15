#!/usr/bin/env python3
"""Grade benchmark outputs into the layout expected by aggregate_benchmark.py.

Target layout:
  iteration-1/
    eval-<name>/
      eval_metadata.json
      with_skill/
        run-1/
          outputs/  (symlink or move from with_skill/outputs)
          grading.json   <- with summary{pass_rate,passed,failed,total} + expectations
          timing.json    (optional, from existing with_skill/timing.json)
      old_skill/
        run-1/
          outputs/
          grading.json
          timing.json

This script:
1. Walks iteration dir
2. For each eval/config, moves outputs/ and timing.json into run-1/ if not already there
3. Runs assertions from eval_metadata.json, writes grading.json
"""
import json
import shutil
import sys
from pathlib import Path


def check_contains(text: str, value: str) -> bool:
    return value.lower() in text.lower()


def check_contains_any(text: str, values: list) -> tuple:
    hits = [v for v in values if v.lower() in text.lower()]
    return len(hits) > 0, hits


def check_contains_count(text: str, values: list, minimum: int) -> tuple:
    hits = [v for v in values if v.lower() in text.lower()]
    return len(hits) >= minimum, hits


def grade_blob(blob: str, assertions: list) -> list:
    expectations = []
    for a in assertions:
        ct = a.get("check_type", "contains")
        text = a["text"]
        if ct == "contains":
            v = a["value"]
            passed = check_contains(blob, v)
            evidence = f"Looking for: {v!r}; {'found' if passed else 'not found'}"
        elif ct == "contains_any":
            vs = a["values"]
            passed, hits = check_contains_any(blob, vs)
            evidence = f"Any of {vs}; found: {hits or 'none'}"
        elif ct == "contains_count":
            vs = a["values"]
            m = a.get("min", 1)
            passed, hits = check_contains_count(blob, vs, m)
            evidence = f"Need {m}+ of {vs}; found {len(hits)}: {hits}"
        else:
            passed = False
            evidence = f"Unknown check_type: {ct}"
        expectations.append({"text": text, "passed": passed, "evidence": evidence})
    return expectations


def ensure_run_layout(config_dir: Path):
    """Move outputs/ and timing.json into run-1/ if they're at config level."""
    run1 = config_dir / "run-1"
    run1.mkdir(exist_ok=True)

    old_outputs = config_dir / "outputs"
    new_outputs = run1 / "outputs"
    if old_outputs.exists() and not new_outputs.exists():
        shutil.move(str(old_outputs), str(new_outputs))

    old_timing = config_dir / "timing.json"
    new_timing = run1 / "timing.json"
    if old_timing.exists() and not new_timing.exists():
        shutil.move(str(old_timing), str(new_timing))


def grade_run(run_dir: Path, assertions: list) -> dict:
    outputs_dir = run_dir / "outputs"
    if not outputs_dir.exists():
        expectations = [{"text": a["text"], "passed": False, "evidence": "outputs/ missing"} for a in assertions]
    else:
        blob = ""
        for fp in outputs_dir.rglob("*"):
            if fp.is_file():
                try:
                    blob += fp.read_text(errors="ignore") + "\n"
                except Exception:
                    pass
        if not blob.strip():
            expectations = [{"text": a["text"], "passed": False, "evidence": "empty output"} for a in assertions]
        else:
            expectations = grade_blob(blob, assertions)

    passed = sum(1 for e in expectations if e["passed"])
    total = len(expectations)
    failed = total - passed
    # aggregate_benchmark.py expects pass_rate as 0.0-1.0 fraction
    pass_rate = (passed / total) if total else 0.0

    return {
        "summary": {
            "pass_rate": round(pass_rate, 4),
            "passed": passed,
            "failed": failed,
            "total": total,
        },
        "expectations": expectations,
    }


def main():
    iteration_dir = Path(sys.argv[1])
    for eval_dir in sorted(iteration_dir.iterdir()):
        if not eval_dir.is_dir() or not eval_dir.name.startswith("eval-"):
            continue
        meta_path = eval_dir / "eval_metadata.json"
        if not meta_path.exists():
            continue
        metadata = json.loads(meta_path.read_text())
        assertions = metadata.get("assertions", [])

        for config in ["with_skill", "old_skill"]:
            config_dir = eval_dir / config
            if not config_dir.exists():
                continue
            ensure_run_layout(config_dir)
            run_dir = config_dir / "run-1"
            grading = grade_run(run_dir, assertions)
            (run_dir / "grading.json").write_text(json.dumps(grading, indent=2, ensure_ascii=False))
            s = grading["summary"]
            print(f"{eval_dir.name}/{config}/run-1: {s['passed']}/{s['total']} ({s['pass_rate']}%)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""aggregate.py — 从 grading.json + timing.json 聚合 benchmark.json (skill-creator schema 兼容子集)。"""
from __future__ import annotations

import json
import statistics
from pathlib import Path

IT = Path(__file__).resolve().parent


def arm_stats(arm: str) -> dict:
    runs = [d for d in sorted(IT.glob("eval-*")) if (d / arm / "grading.json").exists()]
    passed, tokens, secs = 0, [], []
    for d in runs:
        g = json.load((d / arm / "grading.json").open())
        if all(e["passed"] for e in g["expectations"]):
            passed += 1
        t = d / arm / "timing.json"
        if t.exists():
            tm = json.load(t.open())
            tokens.append(tm["total_tokens"])
            secs.append(tm["total_duration_seconds"])
    n = len(runs)
    out = {
        "configuration": arm,
        "num_evals": n,
        "num_passed": passed,
        "pass_rate": round(passed / n, 3) if n else None,
    }
    if tokens:
        out["tokens_mean"] = round(statistics.mean(tokens), 1)
        out["duration_seconds_mean"] = round(statistics.mean(secs), 1)
    return out


def main() -> None:
    with_arm, old_arm = arm_stats("with_skill"), arm_stats("old_skill")
    bench = {
        "skill_name": "branch-manager + branch-finisher (branch-risk-build-gate-alignment, Aria#231)",
        "iteration": 1,
        "configurations": [with_arm, old_arm],
        "delta_pass_rate": round(
            (with_arm["pass_rate"] or 0) - (old_arm["pass_rate"] or 0), 3),
    }
    (IT / "benchmark.json").write_text(json.dumps(bench, ensure_ascii=False, indent=2))
    print(json.dumps(bench, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

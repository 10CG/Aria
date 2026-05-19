#!/usr/bin/env python3
"""H4 — Rule #6 structural benchmark for the H0 handoff collector.

Deterministic-type Rule #6 (per memory feedback_rule6_framing_differs_by_skill_type):
collectors/handoff.py is a pure stdlib function — the meaningful benchmark is
mechanical correctness across fixture scenarios, NOT an LLM with/without AB.

Closes the owner-directed T8.2 skip (.aria/decisions/2026-05-15-h0-rule6-benchmark-skip.md
§Follow-up). Covers the post-H5 collector (pointer-priority + mtime fallback).

Metrics:
  M1 mtime-sort accuracy   — fixture sets, correct newest picked when no pointer
  M2 pointer-priority      — latest.md target wins over newer-mtime predecessor
  M3 misplaced precision   — .aria/handoff/*.md correctly flagged, no FP
  M4 misplaced recall      — every misplaced .md detected, none missed
  M5 latest.md exclusion   — pointer file never a candidate / never misplaced
  M6 stale-pointer fallback — bad pointer → soft_error + mtime fallback
"""
import json
import os
import sys
import tempfile
import time
from pathlib import Path

_SCRIPTS = Path("/home/dev/Aria/aria/skills/state-scanner/scripts")
sys.path.insert(0, str(_SCRIPTS))
from collectors.handoff import collect_handoff  # noqa: E402


def _touch(p: Path, off: float) -> None:
    t = time.time() + off
    os.utime(p, (t, t))


def _mk(root: Path, rel: str, content="x", mtime_off=None):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    if mtime_off is not None:
        _touch(p, mtime_off)
    return p


CASES = []


def case(name):
    def deco(fn):
        CASES.append((name, fn))
        return fn
    return deco


@case("M1.a mtime-sort newest picked (no pointer, 5 files)")
def _(root):
    for i, off in enumerate([-7200, -3600, -100, -50000, -200]):
        _mk(root, f"docs/handoff/2026-05-{10+i:02d}-h.md", mtime_off=off)
    r = collect_handoff(root).data
    return r["latest_filename"] == "2026-05-12-h.md" and r["latest_source"] == "mtime"


@case("M1.b mtime-sort single file")
def _(root):
    _mk(root, "docs/handoff/only.md", mtime_off=-10)
    r = collect_handoff(root).data
    return r["latest_filename"] == "only.md" and r["exists"] is True


@case("M2.a pointer wins over newer-mtime predecessor")
def _(root):
    _mk(root, "docs/handoff/2026-05-15-real.md", mtime_off=-7200)
    _mk(root, "docs/handoff/2026-05-10-old.md", mtime_off=0)  # newest mtime
    _mk(root, "docs/handoff/latest.md",
        "**Latest**: [2026-05-15-real.md](./2026-05-15-real.md) — d\n", mtime_off=-1)
    r = collect_handoff(root).data
    return r["latest_filename"] == "2026-05-15-real.md" and r["latest_source"] == "pointer"


@case("M2.b pointer with bare filename (no ./)")
def _(root):
    _mk(root, "docs/handoff/a.md", mtime_off=-3600)
    _mk(root, "docs/handoff/b.md", mtime_off=0)
    _mk(root, "docs/handoff/latest.md", "**Latest**: [a.md](a.md) — d\n")
    r = collect_handoff(root).data
    return r["latest_filename"] == "a.md" and r["latest_source"] == "pointer"


@case("M3.a misplaced precision — clean docs/handoff only, no FP")
def _(root):
    _mk(root, "docs/handoff/ok.md")
    r = collect_handoff(root).data
    return r["misplaced_files"] == []


@case("M3.b misplaced precision — non-.md in .aria/handoff not flagged")
def _(root):
    _mk(root, "docs/handoff/ok.md")
    _mk(root, ".aria/handoff/README.json", "{}")
    _mk(root, ".aria/handoff/notes.txt", "n")
    r = collect_handoff(root).data
    return r["misplaced_files"] == []


@case("M4.a misplaced recall — all 3 .aria/handoff/*.md detected, sorted")
def _(root):
    _mk(root, "docs/handoff/ok.md")
    for n in ("z.md", "a.md", "m.md"):
        _mk(root, f".aria/handoff/{n}")
    r = collect_handoff(root).data
    return r["misplaced_files"] == [
        ".aria/handoff/a.md", ".aria/handoff/m.md", ".aria/handoff/z.md"]


@case("M4.b misplaced recall — drift state (both dirs populated)")
def _(root):
    _mk(root, "docs/handoff/good.md", mtime_off=-10)
    _mk(root, ".aria/handoff/bad.md")
    r = collect_handoff(root).data
    return (r["exists"] is True and r["latest_filename"] == "good.md"
            and r["misplaced_files"] == [".aria/handoff/bad.md"])


@case("M5.a latest.md never a candidate (only latest.md → exists false)")
def _(root):
    _mk(root, "docs/handoff/latest.md", "**Latest**: [x.md](x.md) — d\n")
    r = collect_handoff(root).data
    return r["exists"] is False and r["latest_path"] is None


@case("M5.b latest.md in .aria/handoff NOT flagged misplaced")
def _(root):
    _mk(root, "docs/handoff/ok.md")
    _mk(root, ".aria/handoff/latest.md", "ptr\n")
    r = collect_handoff(root).data
    return r["misplaced_files"] == []  # latest.md excluded everywhere


@case("M6.a stale pointer (target absent) → mtime fallback + soft_error")
def _(root):
    _mk(root, "docs/handoff/exists.md", mtime_off=-10)
    _mk(root, "docs/handoff/latest.md",
        "**Latest**: [2099-deleted.md](./2099-deleted.md) — d\n")
    res = collect_handoff(root)
    r = res.data
    kinds = {e["error"] for e in res.errors}
    return (r["latest_filename"] == "exists.md" and r["latest_source"] == "mtime"
            and "handoff_pointer_target_missing" in kinds)


@case("M6.b no pointer file at all → mtime fallback, no error")
def _(root):
    _mk(root, "docs/handoff/p.md", mtime_off=-3600)
    _mk(root, "docs/handoff/q.md", mtime_off=0)
    res = collect_handoff(root)
    return (res.data["latest_filename"] == "q.md"
            and res.data["latest_source"] == "mtime" and res.errors == [])


@case("M6.c empty docs/handoff → exists false, all null, no crash")
def _(root):
    (root / "docs" / "handoff").mkdir(parents=True)
    r = collect_handoff(root).data
    return (r["exists"] is False and r["latest_path"] is None
            and r["age_hours"] is None and r["latest_source"] is None
            and r["misplaced_files"] == [])


@case("M6.d docs/handoff absent entirely → graceful")
def _(root):
    r = collect_handoff(root).data
    return r["exists"] is False and r["misplaced_files"] == []


def main():
    results = []
    for name, fn in CASES:
        with tempfile.TemporaryDirectory(prefix="h4-") as tmp:
            try:
                ok = bool(fn(Path(tmp)))
                err = None
            except Exception as e:  # noqa: BLE001
                ok = False
                err = f"{type(e).__name__}: {e}"
        results.append({"case": name, "passed": ok, "error": err})

    passed = sum(1 for r in results if r["passed"])
    total = len(results)

    # Metric-group rollup
    groups = {}
    for r in results:
        g = r["case"].split(".")[0].split(" ")[0]  # M1..M6
        groups.setdefault(g, [0, 0])
        groups[g][1] += 1
        if r["passed"]:
            groups[g][0] += 1

    out = {
        "benchmark": "H0 handoff collector — structural (Rule #6 deterministic)",
        "date": "2026-05-17",
        "collector_under_test": "aria/skills/state-scanner/scripts/collectors/handoff.py (post-H5, pointer-priority)",
        "aria_plugin_version": "v1.21.3",
        "total": total,
        "passed": passed,
        "pass_rate": round(passed / total, 4),
        "metric_groups": {
            g: {"passed": v[0], "total": v[1],
                "label": {"M1": "mtime-sort accuracy",
                          "M2": "pointer-priority",
                          "M3": "misplaced precision (no FP)",
                          "M4": "misplaced recall (no miss)",
                          "M5": "latest.md exclusion",
                          "M6": "fallback/edge robustness"}[g]}
            for g, v in sorted(groups.items())
        },
        "cases": results,
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))
    Path(__file__).parent.joinpath("benchmark.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False))
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""D1-D5 grader for issue-triage iteration-2 benchmark.

D1 JSON output         — triage-report.json exists + parses
D2 triage-comment.md   — exists + non-trivial (>200 chars, has Verdict)
D3 schema conformance  — jsonschema validation pass (PRIMARY; was 0/3)
D4 canonical enums     — verdict + severity + recommended_action all in enum
D5 multi-artifact      — >=2 distinct output files
Plus: script_produced  — triage_tool_version + generated_at present (not hand-authored)
"""
import json
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parent
SCHEMA = json.loads(
    (ROOT.parent.parent.parent
     / "aria/skills/issue-triage/references/triage-report.schema.json").read_text()
)
# The schema's "$id" is a relative repo path, not a resolvable URI. jsonschema
# would combine it as a base when resolving internal "#/$defs/..." refs,
# producing a doubled broken path. Drop $id so internal refs resolve against
# the document root (correct behavior for a self-contained schema).
SCHEMA.pop("$id", None)

VERDICTS = {"already-fixed", "fixed", "fixed-in-X", "fixed-in-1.20.0",
            "confirmed", "partial-repro", "not-reproducible", "needs-info",
            "duplicate", "wont-fix", "enhancement"}
SEVERITIES = {"critical", "major", "medium", "minor", "trivial"}
ACTIONS = {"hotfix", "next-cycle", "backlog", "close", "schedule",
           "open-spec", "open-cycle", "no-new-cycle", "needs-info"}


def grade_run(d: Path) -> dict:
    out = d / "outputs"
    rj = out / "triage-report.json"
    cm = out / "triage-comment.md"
    res = {}

    # D1
    d1 = False
    report = None
    if rj.is_file():
        try:
            report = json.loads(rj.read_text())
            d1 = True
        except Exception:
            pass
    res["D1_json_output"] = d1

    # D2
    d2 = False
    if cm.is_file():
        t = cm.read_text()
        d2 = len(t) > 200 and ("Verdict" in t or "verdict" in t)
    res["D2_comment_md"] = d2

    # D3 — schema conformance (PRIMARY)
    d3 = False
    d3_err = None
    if report is not None:
        try:
            jsonschema.validate(report, SCHEMA)
            d3 = True
        except jsonschema.ValidationError as e:
            d3_err = f"{'.'.join(str(p) for p in e.absolute_path)}: {e.message[:120]}"
        except Exception as e:
            d3_err = str(e)[:120]
    res["D3_schema_conformance"] = d3
    res["D3_error"] = d3_err

    # D4 — canonical enums
    d4 = False
    if report is not None:
        v = report.get("verdict")
        s = report.get("severity")
        a = report.get("recommended_action")
        d4 = v in VERDICTS and s in SEVERITIES and a in ACTIONS
        res["D4_values"] = {"verdict": v, "severity": s, "recommended_action": a}
    res["D4_canonical_enums"] = d4

    # D5 — multi-artifact
    files = [p for p in out.glob("*") if p.is_file()] if out.is_dir() else []
    res["D5_multi_artifact"] = len(files) >= 2
    res["_files"] = sorted(p.name for p in files)

    # script-produced (anti-hand-author signal)
    sp = False
    if report is not None:
        sp = bool(report.get("triage_tool_version")) and bool(report.get("generated_at"))
    res["script_produced"] = sp

    return res


def main():
    B = ROOT / "iteration-1"
    summary = {}
    for cfg in ("with_skill", "old_skill"):
        agg = {k: 0 for k in
               ["D1_json_output", "D2_comment_md", "D3_schema_conformance",
                "D4_canonical_enums", "D5_multi_artifact", "script_produced"]}
        n = 0
        details = {}
        for e in (1, 2, 3, 4):
            d = B / f"eval-{e}" / cfg
            if not d.is_dir():
                continue
            n += 1
            r = grade_run(d)
            details[f"eval-{e}"] = r
            for k in agg:
                agg[k] += 1 if r.get(k) else 0
            (d / "grading.json").write_text(json.dumps({
                "expectations": [
                    {"text": k.replace("_", " "), "passed": bool(r.get(k)),
                     "evidence": str(r.get("D3_error") or r.get("D4_values") or r.get("_files") or "")}
                    for k in ["D1_json_output", "D2_comment_md",
                              "D3_schema_conformance", "D4_canonical_enums",
                              "D5_multi_artifact", "script_produced"]
                ]
            }, indent=2, ensure_ascii=False))
        summary[cfg] = {"n": n, "agg": agg, "details": details}

    print(json.dumps(summary, indent=2, ensure_ascii=False, default=str))
    (ROOT / "iteration-1" / "grade-summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
calc_dual_delta.py — Spike prototype

Computes internal_delta + cross_project_delta for a Skill benchmark run by
joining grading.json output with eval_metadata.json assertions, then applying
an external category classification (aria_convention / generic_capability /
behavior_contract).

This is a PROTOTYPE for spike validation of Aria#8 Phase 3 assumptions.
Not production quality — no CLI parser, no error handling for edge cases.

Handles 3 known eval_metadata formats and 2 known grading field names:
  - state-scanner v2.9.0: assertions=[{text, weight}]
  - state-scanner v2.4.0: assertions=[{id, text, severity}]
  - commit-msg-generator: assertions=[{id, name, description, check, severity}]
  - grading.json uses 'expectations' OR 'assertions' field

Usage:
    python3 calc_dual_delta.py <skill_iteration_dir> <category_map_json>

Where:
  skill_iteration_dir: contains eval-N/ subdirs with eval_metadata.json + with_skill/ + without_skill/
  category_map_json:   JSON dict {assertion_join_key: category} for classification
"""
import json
import sys
from pathlib import Path


def extract_assertions(meta: dict) -> list[dict]:
    """Return list of {'key': str, 'severity': str} from eval_metadata.
    'key' is the field that grading.json 'text' will match on.
    """
    result = []
    for a in meta.get("assertions", []):
        # Prefer 'name' (commit-msg style) then 'text' (state-scanner style)
        if "name" in a:
            key = a["name"]
        elif "text" in a:
            key = a["text"]
        else:
            continue
        severity = a.get("severity", "unknown")
        result.append({"key": key, "severity": severity})
    return result


def extract_grading_items(grading: dict) -> list[dict]:
    """Return list of {'text': str, 'passed': bool} from grading.
    Tries 'expectations' first, then 'assertions'.
    """
    items = grading.get("expectations") or grading.get("assertions") or []
    return [{"text": i.get("text", ""), "passed": bool(i.get("passed", False))} for i in items]


_unmapped_warned = set()


def classify(key: str, category_map: dict) -> str:
    """Look up category for an assertion key. Default to 'aria_convention' (conservative).

    Emits a stderr warning the first time each unmapped key is encountered.
    """
    if key in category_map:
        return category_map[key]
    if key not in _unmapped_warned:
        print(
            f'WARNING: unmapped assertion "{key[:80]}", defaulting to aria_convention',
            file=sys.stderr,
        )
        _unmapped_warned.add(key)
    return "aria_convention"


def compute_eval_delta(eval_dir: Path, category_map: dict) -> dict:
    """Compute dual delta for a single eval directory."""
    meta_path = eval_dir / "eval_metadata.json"
    if not meta_path.exists():
        return None

    with open(meta_path) as f:
        meta = json.load(f)

    assertions = extract_assertions(meta)
    eval_name = meta.get("eval_name", eval_dir.name)

    # Read grading
    with_path = eval_dir / "with_skill" / "grading.json"
    without_path = eval_dir / "without_skill" / "grading.json"

    # Fallback: outputs/grading.json (some older evals)
    if not with_path.exists():
        alt = eval_dir / "with_skill" / "outputs" / "grading.json"
        if alt.exists():
            with_path = alt
    if not without_path.exists():
        alt = eval_dir / "without_skill" / "outputs" / "grading.json"
        if alt.exists():
            without_path = alt

    if not with_path.exists() or not without_path.exists():
        return {"eval_name": eval_name, "error": "missing grading files", "skipped": True}

    with open(with_path) as f:
        with_grade = json.load(f)
    with open(without_path) as f:
        without_grade = json.load(f)

    with_items = extract_grading_items(with_grade)
    without_items = extract_grading_items(without_grade)

    # Use grading.json items as source of truth (not eval_metadata, which is
    # often incomplete). Classify each grading text via category_map, default
    # aria_convention if unmapped. Union of with/without texts.
    all_keys = set()
    with_map = {}
    without_map = {}
    for item in with_items:
        all_keys.add(item["text"])
        with_map[item["text"]] = item["passed"]
    for item in without_items:
        all_keys.add(item["text"])
        without_map[item["text"]] = item["passed"]

    def build_joined(pass_map):
        return [
            {
                "key": k,
                "category": classify(k, category_map),
                "passed": pass_map.get(k),
                "matched": k in pass_map,
            }
            for k in sorted(all_keys)
        ]

    with_joined = build_joined(with_map)
    without_joined = build_joined(without_map)
    # Redefine classified for category breakdown based on grading source
    classified = [
        {"key": k, "category": classify(k, category_map)} for k in all_keys
    ]

    # Compute internal delta (all matched assertions)
    def compute_delta(items, filter_fn=None):
        filtered = [i for i in items if i["matched"] and (filter_fn is None or filter_fn(i))]
        if not filtered:
            return None, 0
        passed = sum(1 for i in filtered if i["passed"])
        total = len(filtered)
        return passed / total, total

    with_internal_rate, with_internal_count = compute_delta(with_joined)
    without_internal_rate, without_internal_count = compute_delta(without_joined)

    # Cross-project delta: exclude aria_convention
    def not_aria_convention(i):
        return i["category"] != "aria_convention"

    with_cross_rate, with_cross_count = compute_delta(with_joined, not_aria_convention)
    without_cross_rate, without_cross_count = compute_delta(without_joined, not_aria_convention)

    internal_delta = None
    if with_internal_rate is not None and without_internal_rate is not None:
        internal_delta = round(with_internal_rate - without_internal_rate, 3)

    cross_delta = None
    if with_cross_rate is not None and without_cross_rate is not None:
        cross_delta = round(with_cross_rate - without_cross_rate, 3)

    # Category breakdown
    category_counts = {"aria_convention": 0, "generic_capability": 0, "behavior_contract": 0}
    for a in classified:
        category_counts[a["category"]] = category_counts.get(a["category"], 0) + 1

    total_assertions = len(classified)
    aria_ratio = (
        category_counts["aria_convention"] / total_assertions
        if total_assertions > 0
        else 0
    )

    return {
        "eval_name": eval_name,
        "total_assertions": total_assertions,
        "category_breakdown": category_counts,
        "aria_convention_ratio": round(aria_ratio, 3),
        "internal": {
            "with_pass_rate": with_internal_rate,
            "without_pass_rate": without_internal_rate,
            "delta": internal_delta,
            "assertion_count": with_internal_count,
        },
        "cross_project": {
            "with_pass_rate": with_cross_rate,
            "without_pass_rate": without_cross_rate,
            "delta": cross_delta,
            "assertion_count": with_cross_count,
            "aria_convention_excluded": category_counts["aria_convention"],
            "verdict": (
                "INSUFFICIENT_SAMPLE"
                if with_cross_count < 3
                else "POSITIVE_DELTA"
                if cross_delta and cross_delta >= 0.2
                else "NEGATIVE_OR_FLAT"
            ),
        },
        "skipped": False,
    }


def aggregate(eval_results: list[dict]) -> dict:
    """Average delta across evals, weighted by assertion count."""
    valid = [r for r in eval_results if not r.get("skipped") and not r.get("error")]
    if not valid:
        return {"error": "no valid evals"}

    def weighted_avg(delta_field: str, count_field: str):
        total_num = 0.0
        total_den = 0
        for r in valid:
            d = r[delta_field]["delta"]
            c = r[delta_field][count_field]
            if d is not None and c:
                total_num += d * c
                total_den += c
        return round(total_num / total_den, 3) if total_den else None, total_den

    internal_delta, internal_total = weighted_avg("internal", "assertion_count")
    cross_delta, cross_total = weighted_avg("cross_project", "assertion_count")

    # Overall aria_convention_ratio (all assertions, not just cross-project eligible)
    total_assertions = sum(r["total_assertions"] for r in valid)
    aria_count = sum(r["category_breakdown"]["aria_convention"] for r in valid)
    overall_aria_ratio = round(aria_count / total_assertions, 3) if total_assertions else 0

    # Inflation = 1 - (cross / internal) when internal > 0
    inflation = None
    if internal_delta and internal_delta > 0 and cross_delta is not None:
        inflation = round(1 - (cross_delta / internal_delta), 3)

    return {
        "evals_analyzed": len(valid),
        "total_assertions": total_assertions,
        "overall_aria_convention_ratio": overall_aria_ratio,
        "internal_delta": internal_delta,
        "internal_assertion_count": internal_total,
        "cross_project_delta": cross_delta,
        "cross_project_assertion_count": cross_total,
        "inflation_ratio": inflation,  # 0 = internal matches cross, 1 = 100% inflation
    }


def main():
    if len(sys.argv) >= 2 and sys.argv[1] in ("--help", "-h"):
        print(__doc__)
        sys.exit(0)
    if len(sys.argv) < 3:
        print("Usage: calc_dual_delta.py <iteration_dir> <category_map.json>", file=sys.stderr)
        print("       calc_dual_delta.py --help    show full documentation", file=sys.stderr)
        sys.exit(1)

    iteration_dir = Path(sys.argv[1])
    category_map_path = Path(sys.argv[2])

    with open(category_map_path) as f:
        category_map = json.load(f)

    # Find all eval-* subdirectories
    eval_dirs = sorted(
        p for p in iteration_dir.iterdir() if p.is_dir() and p.name.startswith("eval-")
    )

    eval_results = []
    for ed in eval_dirs:
        result = compute_eval_delta(ed, category_map)
        if result is None:
            continue
        eval_results.append(result)

    summary = {
        "iteration_dir": str(iteration_dir),
        "eval_results": eval_results,
        "aggregate": aggregate(eval_results),
    }

    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

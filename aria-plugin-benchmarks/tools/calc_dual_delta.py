#!/usr/bin/env python3
"""
calc_dual_delta.py — Dual Delta Reporting Tool (non-gate)

Computes internal_delta + cross_project_delta for a Skill benchmark run by
joining grading.json output with eval_metadata.json assertions, then applying
an external category classification (aria_convention / generic_capability /
behavior_contract).

**Status**: Official reporting tool (graduated from spike 2026-04-10).
**Not a gate**: output is informational only; Rule #6 still relies on
/skill-creator benchmark for merge decisions. See AB_TEST_OPERATIONS.md
"Dual Delta Reporting" section for usage guidance.

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

Exit codes:
  0  success (stdout: JSON summary)
  1  argument error / file not found / JSON parse error (stderr: error message)
"""
import json
import sys
from pathlib import Path

# Named constants (Round 1 cr/qa minors: no magic numbers)
MIN_CROSS_PROJECT_ASSERTIONS = 3  # statistical minimum for cross-project verdict
POSITIVE_DELTA_THRESHOLD = 0.2    # derived from Aria#8 spike baseline (+0.2 = meaningful gain)
INFLATION_CAP_UPPER = 1.0          # ratio capped at 1.0 (100%); negative cross is clamped
INFLATION_CAP_LOWER = -1.0         # lower bound for display sanity


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


def classify(key: str, category_map: dict, warned: set = None) -> str:
    """Look up category for an assertion key. Default to 'aria_convention' (conservative).

    Emits a stderr warning the first time each unmapped key is encountered.

    Round 1 cr_m3 fix: `warned` is an explicit per-call state set (not module-level global),
    so tests can pass an empty set for isolation. If None, uses module-level fallback.
    """
    if key in category_map:
        return category_map[key]
    state = warned if warned is not None else _default_warned
    if key not in state:
        print(
            f'WARNING: unmapped assertion "{key[:80]}", defaulting to aria_convention',
            file=sys.stderr,
        )
        state.add(key)
    return "aria_convention"


# Fallback module-level state for callers that don't pass explicit `warned` set.
# Tests should always pass their own set to avoid cross-test coupling.
_default_warned: set = set()


def compute_eval_delta(eval_dir: Path, category_map: dict, warned: set = None) -> dict:
    """Compute dual delta for a single eval directory.

    `warned` is passed through to classify() for per-call state isolation.
    """
    meta_path = eval_dir / "eval_metadata.json"
    if not meta_path.exists():
        return None

    try:
        with open(meta_path, encoding="utf-8") as f:
            meta = json.load(f)
    except json.JSONDecodeError as e:
        return {"eval_name": eval_dir.name, "error": f"eval_metadata.json parse error: {e}", "skipped": True}

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

    try:
        with open(with_path, encoding="utf-8") as f:
            with_grade = json.load(f)
        with open(without_path, encoding="utf-8") as f:
            without_grade = json.load(f)
    except json.JSONDecodeError as e:
        return {"eval_name": eval_name, "error": f"grading.json parse error: {e}", "skipped": True}

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

    # Pre-classify once (Round 1 cr_m6 fix: was doing classify() twice).
    # This is also needed for deterministic warning ordering.
    key_category = {k: classify(k, category_map, warned) for k in sorted(all_keys)}

    def build_joined(pass_map):
        return [
            {
                "key": k,
                "category": key_category[k],
                "passed": pass_map.get(k),
                "matched": k in pass_map,
            }
            for k in sorted(all_keys)
        ]

    with_joined = build_joined(with_map)
    without_joined = build_joined(without_map)
    classified = [{"key": k, "category": key_category[k]} for k in sorted(all_keys)]

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
                if with_cross_count < MIN_CROSS_PROJECT_ASSERTIONS
                else "POSITIVE_DELTA"
                if cross_delta and cross_delta >= POSITIVE_DELTA_THRESHOLD
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
    #
    # Semantic:
    #   0.0  = internal matches cross exactly (ideal)
    #   0.2  = 20% inflation (internal higher than cross, reasonable)
    #   1.0  = 100% inflation (cross is 0 while internal > 0)
    #   >1.0 = cross is NEGATIVE while internal is positive (Skill degrades on
    #          generic scenarios) — this is pathological and deserves a warning.
    #   None = internal is 0 or None (ratio undefined)
    #
    # Round 1 qa_M2 fix: clamp to [INFLATION_CAP_LOWER, INFLATION_CAP_UPPER] for
    # display sanity. A separate inflation_uncapped field preserves the raw value
    # so pathological cases are still visible for diagnostics.
    inflation = None
    inflation_uncapped = None
    inflation_warning = None
    if internal_delta and internal_delta > 0 and cross_delta is not None:
        raw = 1 - (cross_delta / internal_delta)
        inflation_uncapped = round(raw, 3)
        if raw > INFLATION_CAP_UPPER:
            inflation = INFLATION_CAP_UPPER
            inflation_warning = (
                f"cross_project_delta ({cross_delta}) is negative while internal_delta "
                f"({internal_delta}) is positive — Skill may degrade on generic scenarios; "
                f"inflation capped at {INFLATION_CAP_UPPER}"
            )
        elif raw < INFLATION_CAP_LOWER:
            inflation = INFLATION_CAP_LOWER
            inflation_warning = f"inflation out of bounds ({raw}); clamped to {INFLATION_CAP_LOWER}"
        else:
            inflation = round(raw, 3)

    result = {
        "evals_analyzed": len(valid),
        "total_assertions": total_assertions,
        "overall_aria_convention_ratio": overall_aria_ratio,
        "internal_delta": internal_delta,
        "internal_assertion_count": internal_total,
        "cross_project_delta": cross_delta,
        "cross_project_assertion_count": cross_total,
        "inflation_ratio": inflation,  # 0 = internal matches cross, 1 = 100% inflation, capped at [-1.0, 1.0]
        "inflation_ratio_uncapped": inflation_uncapped,  # raw value for diagnostics
    }
    if inflation_warning:
        result["inflation_warning"] = inflation_warning
        print(f"WARNING: {inflation_warning}", file=sys.stderr)
    return result


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

    # Round 1 cr_M1 fix: catch FileNotFoundError / JSONDecodeError with
    # user-friendly messages instead of raw Python tracebacks.
    if not iteration_dir.exists():
        print(f"ERROR: iteration_dir not found: {iteration_dir}", file=sys.stderr)
        sys.exit(1)
    if not iteration_dir.is_dir():
        print(f"ERROR: iteration_dir is not a directory: {iteration_dir}", file=sys.stderr)
        sys.exit(1)
    if not category_map_path.exists():
        print(f"ERROR: category_map file not found: {category_map_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(category_map_path, encoding="utf-8") as f:
            category_map = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: category_map JSON parse error: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(category_map, dict):
        print(f"ERROR: category_map must be a JSON object (dict), got {type(category_map).__name__}", file=sys.stderr)
        sys.exit(1)

    # Find all eval-* subdirectories
    eval_dirs = sorted(
        p for p in iteration_dir.iterdir() if p.is_dir() and p.name.startswith("eval-")
    )

    # Per-run warning state (no global pollution).
    run_warned: set = set()

    eval_results = []
    for ed in eval_dirs:
        result = compute_eval_delta(ed, category_map, warned=run_warned)
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

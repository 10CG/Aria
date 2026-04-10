"""Unit tests for calc_dual_delta.py prototype.

Run: python3 -m pytest aria-plugin-benchmarks/tools/test_calc_dual_delta.py -v
"""
import json
import os
import sys
import tempfile
from pathlib import Path

# Make calc_dual_delta importable
sys.path.insert(0, str(Path(__file__).parent))
import calc_dual_delta as cdd


def make_eval_dir(tmp: Path, eval_name: str, assertions: list, with_grading: list, without_grading: list):
    """Create a minimal eval-N/ directory with eval_metadata + with_skill + without_skill grading."""
    d = tmp / eval_name
    (d / "with_skill").mkdir(parents=True)
    (d / "without_skill").mkdir(parents=True)
    (d / "eval_metadata.json").write_text(json.dumps({
        "eval_id": 1,
        "eval_name": eval_name.replace("eval-", ""),
        "assertions": assertions,
    }))
    (d / "with_skill" / "grading.json").write_text(json.dumps({
        "eval_id": 1,
        "expectations": [{"text": t, "passed": p} for t, p in with_grading],
    }))
    (d / "without_skill" / "grading.json").write_text(json.dumps({
        "eval_id": 1,
        "expectations": [{"text": t, "passed": p} for t, p in without_grading],
    }))
    return d


def test_normal_dual_delta_computation():
    """Mixed assertions: 2 generic, 1 aria_convention. with_skill all pass, without_skill 1/3."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        make_eval_dir(
            tmp_path,
            "eval-1",
            [{"text": "generic_a", "weight": 1.0}, {"text": "generic_b", "weight": 1.0}, {"text": "aria_x", "weight": 1.0}],
            [("generic_a", True), ("generic_b", True), ("aria_x", True)],
            [("generic_a", True), ("generic_b", False), ("aria_x", False)],
        )
        cat_map = {"generic_a": "generic_capability", "generic_b": "generic_capability", "aria_x": "aria_convention"}
        result = cdd.compute_eval_delta(tmp_path / "eval-1", cat_map)
        # with=3/3=1.0, without=1/3=0.333, delta=0.667
        assert result["internal"]["delta"] == 0.667
        # Cross-project (excluding aria): with=2/2=1.0, without=1/2=0.5, delta=0.5
        assert result["cross_project"]["delta"] == 0.5
        assert result["cross_project"]["assertion_count"] == 2
        assert result["aria_convention_ratio"] == 0.333


def test_insufficient_sample_when_all_aria_convention():
    """All assertions aria_convention → cross-project INSUFFICIENT_SAMPLE."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        make_eval_dir(
            tmp_path,
            "eval-1",
            [{"text": "marker_1", "weight": 1.0}, {"text": "marker_2", "weight": 1.0}],
            [("marker_1", True), ("marker_2", True)],
            [("marker_1", False), ("marker_2", False)],
        )
        cat_map = {"marker_1": "aria_convention", "marker_2": "aria_convention"}
        result = cdd.compute_eval_delta(tmp_path / "eval-1", cat_map)
        assert result["cross_project"]["verdict"] == "INSUFFICIENT_SAMPLE"
        assert result["cross_project"]["delta"] is None
        assert result["aria_convention_ratio"] == 1.0
        assert result["internal"]["delta"] == 1.0


def test_missing_category_defaults_to_aria_convention_with_warning(capsys):
    """Unmapped key → default aria_convention + stderr warning."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        make_eval_dir(
            tmp_path,
            "eval-1",
            [{"text": "unknown_key", "weight": 1.0}],
            [("unknown_key", True)],
            [("unknown_key", False)],
        )
        # Round 1 cr_m3 fix: pass an explicit per-call warned set to avoid
        # module-level state pollution between tests.
        local_warned: set = set()
        result = cdd.compute_eval_delta(tmp_path / "eval-1", {}, warned=local_warned)
        captured = capsys.readouterr()
        assert "WARNING" in captured.err
        assert "unknown_key" in captured.err
        # Default to aria_convention → cross-project gets nothing
        assert result["cross_project"]["assertion_count"] == 0
        # The local set should have captured the warning state, not module-level
        assert "unknown_key" in local_warned


def test_grading_with_extra_items_uses_grading_as_source_of_truth():
    """If grading has more items than eval_metadata, use grading (the actual measurement)."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        make_eval_dir(
            tmp_path,
            "eval-1",
            # eval_metadata only declares 1 assertion
            [{"text": "declared", "weight": 1.0}],
            # but grading evaluated 2
            [("declared", True), ("extra_orphan", True)],
            [("declared", False), ("extra_orphan", False)],
        )
        cat_map = {"declared": "generic_capability", "extra_orphan": "behavior_contract"}
        result = cdd.compute_eval_delta(tmp_path / "eval-1", cat_map)
        # Should include both assertions (grading is source of truth)
        assert result["total_assertions"] == 2
        # Both are non-aria, both contribute to cross-project
        assert result["cross_project"]["assertion_count"] == 2
        assert result["cross_project"]["delta"] == 1.0  # (2/2 - 0/2)


def test_aggregate_across_multiple_evals():
    """Aggregate computes weighted averages and inflation ratio."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        make_eval_dir(
            tmp_path,
            "eval-1",
            [{"text": "gen_a", "weight": 1.0}, {"text": "gen_b", "weight": 1.0}],
            [("gen_a", True), ("gen_b", True)],
            [("gen_a", False), ("gen_b", True)],  # 1/2 = 0.5
        )
        make_eval_dir(
            tmp_path,
            "eval-2",
            [{"text": "aria_only", "weight": 1.0}],
            [("aria_only", True)],
            [("aria_only", False)],
        )
        cat_map = {"gen_a": "generic_capability", "gen_b": "generic_capability", "aria_only": "aria_convention"}
        results = [
            cdd.compute_eval_delta(tmp_path / "eval-1", cat_map),
            cdd.compute_eval_delta(tmp_path / "eval-2", cat_map),
        ]
        agg = cdd.aggregate(results)
        assert agg["evals_analyzed"] == 2
        assert agg["total_assertions"] == 3
        # Internal: eval-1 delta=0.5 (n=2), eval-2 delta=1.0 (n=1) → weighted = (0.5*2 + 1.0*1) / 3 = 0.667
        assert agg["internal_delta"] == 0.667
        # Cross-project: only eval-1 has generic. delta=0.5, n=2
        assert agg["cross_project_delta"] == 0.5
        assert agg["cross_project_assertion_count"] == 2
        # Inflation = 1 - (0.5 / 0.667) = 0.25
        assert agg["inflation_ratio"] == 0.25


def test_help_flag_exits_zero(capsys, monkeypatch):
    """--help prints docstring and exits 0."""
    monkeypatch.setattr(sys, "argv", ["calc_dual_delta.py", "--help"])
    try:
        cdd.main()
    except SystemExit as e:
        assert e.code == 0
    captured = capsys.readouterr()
    assert "calc_dual_delta.py" in captured.out
    # Round 1 qa_m9 fix: docstring no longer says "Spike prototype"
    # (graduated to official reporting tool per Spec AC1)
    assert "Dual Delta Reporting" in captured.out


def test_no_args_exits_one(capsys, monkeypatch):
    """Missing positional args prints usage and exits 1."""
    monkeypatch.setattr(sys, "argv", ["calc_dual_delta.py"])
    try:
        cdd.main()
    except SystemExit as e:
        assert e.code == 1
    captured = capsys.readouterr()
    assert "Usage" in captured.err


def test_inflation_ratio_capped_when_cross_delta_negative(capsys):
    """Round 1 qa_M1 + Round 2 nf_01 fix: cross_delta<0 with internal_delta>0 →
    inflation raw > 1.0 → capped at INFLATION_CAP_UPPER=1.0 + warning + uncapped preserved.

    Fixture design (Round 2 nf_01 fix): need internal_delta > 0 AND cross_delta < 0
    simultaneously across the aggregate. Use UNEQUAL assertion counts to prevent
    internal cancellation:
      - eval-1: 3 aria assertions (all pass with_skill, all fail without) → internal=+1.0, count=3
      - eval-2: 1 generic assertion (fails with_skill, passes without)     → internal=-1.0, count=1, cross=-1.0, count=1
    Weighted internal = (1.0*3 + (-1.0)*1) / 4 = 0.5
    Weighted cross    = (-1.0*1) / 1 = -1.0
    Raw inflation = 1 - (-1.0 / 0.5) = 3.0 → CAPPED to 1.0, uncapped = 3.0
    """
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        # eval-1: 3 aria assertions, positive internal, no cross
        make_eval_dir(
            tmp_path,
            "eval-1",
            [{"text": f"aria_{i}", "weight": 1.0} for i in range(3)],
            [(f"aria_{i}", True) for i in range(3)],
            [(f"aria_{i}", False) for i in range(3)],
        )
        # eval-2: 1 generic assertion, NEGATIVE cross
        make_eval_dir(
            tmp_path,
            "eval-2",
            [{"text": "gen_x", "weight": 1.0}],
            [("gen_x", False)],  # with_skill fails
            [("gen_x", True)],   # without_skill passes
        )
        cat_map = {
            "aria_0": "aria_convention", "aria_1": "aria_convention", "aria_2": "aria_convention",
            "gen_x": "generic_capability",
        }
        results = [
            cdd.compute_eval_delta(tmp_path / "eval-1", cat_map),
            cdd.compute_eval_delta(tmp_path / "eval-2", cat_map),
        ]
        agg = cdd.aggregate(results)

        # Verify the fixture really produces the conditions we need
        assert agg["internal_delta"] == 0.5, f"expected 0.5, got {agg['internal_delta']}"
        assert agg["cross_project_delta"] == -1.0

        # ---- The core assertions for qa_M1 cap logic ----
        # Raw inflation = 1 - (-1.0 / 0.5) = 3.0 → capped at 1.0
        assert agg["inflation_ratio"] == 1.0, f"expected cap at 1.0, got {agg['inflation_ratio']}"
        # Uncapped raw value preserved for diagnostics
        assert agg["inflation_ratio_uncapped"] == 3.0, f"expected 3.0, got {agg['inflation_ratio_uncapped']}"
        # stderr warning was emitted
        captured = capsys.readouterr()
        assert "WARNING" in captured.err
        assert "inflation capped" in captured.err or "negative" in captured.err
        # The warning field is present in the output
        assert "inflation_warning" in agg


def test_inflation_ratio_none_when_internal_delta_zero():
    """Round 2 nf_02 fix: when internal_delta is 0 or None, inflation_ratio is None
    (division-by-zero guard), and inflation_ratio_uncapped is also None."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        # Two assertions that cancel internally: 1 pass both, 1 fail both → delta=0
        make_eval_dir(
            tmp_path,
            "eval-1",
            [{"text": "gen_x", "weight": 1.0}, {"text": "aria_y", "weight": 1.0}],
            [("gen_x", False), ("aria_y", True)],  # with: 1/2
            [("gen_x", True), ("aria_y", False)],  # without: 1/2
        )
        cat_map = {"gen_x": "generic_capability", "aria_y": "aria_convention"}
        results = [cdd.compute_eval_delta(tmp_path / "eval-1", cat_map)]
        agg = cdd.aggregate(results)
        # internal: 1/2 - 1/2 = 0 → inflation is None (undefined, division guard)
        assert agg["internal_delta"] == 0.0
        assert agg["inflation_ratio"] is None
        assert agg["inflation_ratio_uncapped"] is None
        # No warning should be emitted (this is a normal undefined case, not pathological)
        assert "inflation_warning" not in agg

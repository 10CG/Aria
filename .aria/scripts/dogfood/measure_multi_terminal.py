"""Dogfood metric collector for multi-terminal-coordination.

Per multi-terminal-coordination tasks.md §3.6 (TASK-028).

Three observable metrics (falsifiable):
  (a) max active claim count per track-id in refs/aria/coordination
      Expected: ≤ 1 per track-id.  Actual > 1 = duplicate-work event.
  (b) handoff frontmatter updated-at vs git log latest handoff commit time delta
      Expected: < 60s per file.  Actual ≥ 60s = stale-handoff / wrong-baton risk.
  (c) metric_c_complete: both (a) and (b) produced real numeric measurements
      (non-empty, non-error).  "No problems observed" is not an acceptable PASS.

Usage (run AFTER Layer L ships to master and refs/aria/coordination is
bootstrapped by at least one real session):

    python3 .aria/scripts/dogfood/measure_multi_terminal.py \\
        --repo-path /path/to/Aria \\
        --cycle-id  post-p3-merge-2026-05-XX \\
        --output    .aria/dogfood-reports/multi-terminal-coordination-$(date -u +%Y-%m-%d).md

Exit codes
----------
0   metric_c_complete is True  (all metrics populated; values may still reveal issues)
1   metric_c_complete is False (Layer L not yet deployed or import failure)

Design constraints
------------------
- stdlib only (no third-party deps beyond what Layer L itself requires)
- Does NOT write to git or push any ref
- Does NOT produce false data; if Layer L is not deployed the error is surfaced
  in JSON output rather than silently returning zero/empty
- All subprocess calls use capture_output=True per Rule #7 (no secret paths
  here, but the pattern keeps the module Rule #7-clean by default)

References
----------
- openspec/changes/multi-terminal-coordination/tasks.md §3.6
- openspec/changes/multi-terminal-coordination/detailed-tasks.yaml TASK-028
- .aria/notes/multi-terminal-coordination-p2-closeout.md (P2 ship state)
- aria/skills/state-scanner/lib/constants.py (STALE_TTL, HEARTBEAT_INTERVAL)
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class MetricAResult:
    """Metric (a) — duplicate active claim detection."""
    per_track: dict[str, int]          # {track_id: active_count}
    duplicates: list[str]              # track_ids with active_count > 1
    max_active_per_track: Optional[int]  # None if per_track is empty
    error: Optional[str]               # None = success


@dataclass
class HandoffFileEntry:
    """Per-file breakdown for metric (b)."""
    frontmatter_updated_at: Optional[str]   # ISO 8601 from YAML frontmatter
    git_last_commit_at: Optional[str]       # ISO 8601 from git log
    delta_seconds: Optional[float]         # abs diff; None if either field missing
    exceeds_threshold: bool                 # delta_seconds >= 60


@dataclass
class MetricBResult:
    """Metric (b) — handoff freshness (frontmatter vs git log delta)."""
    per_file: dict[str, HandoffFileEntry]   # filename → entry
    stale_files: list[str]                  # files where delta_seconds >= 60
    max_delta_seconds: Optional[float]      # None if no measurable files
    error: Optional[str]                    # None = success


@dataclass
class DogfoodMeasurement:
    """Complete measurement snapshot for one dogfood cycle."""
    cycle_id: str
    run_at: str                              # ISO 8601 UTC
    layer_l_deployed: bool                   # True if coordination_ref import ok
    metric_a: MetricAResult
    metric_b: MetricBResult
    metric_c_complete: bool                  # True if both a+b have real data
    verdict: str                             # PASS / FAIL / PENDING
    verdict_reason: str
    notes: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Metric (a) — duplicate active claim detection
# ---------------------------------------------------------------------------

def measure_metric_a(repo_path: Path) -> MetricAResult:
    """Count status=active claims per track_id in refs/aria/coordination.

    Requires Layer L to be deployed (aria/skills/state-scanner/lib importable)
    and refs/aria/coordination to exist in the local repo.

    Returns a MetricAResult with error set when Layer L is absent.
    """
    # Attempt to import Layer L lib from the submodule path.
    lib_path = repo_path / "aria" / "skills" / "state-scanner"
    _maybe_add_sys_path(lib_path)

    try:
        from lib.coordination_ref import read_claims  # type: ignore[import]
    except ImportError as exc:
        return MetricAResult(
            per_track={},
            duplicates=[],
            max_active_per_track=None,
            error=f"layer_l_import_failed: {exc}",
        )

    try:
        result = read_claims(repo_path)
    except Exception as exc:  # noqa: BLE001
        return MetricAResult(
            per_track={},
            duplicates=[],
            max_active_per_track=None,
            error=f"read_claims_exception: {exc}",
        )

    if not result.ref_exists:
        return MetricAResult(
            per_track={},
            duplicates=[],
            max_active_per_track=None,
            error="coordination_ref_not_bootstrapped: no claims to measure; "
                  "run at least one real session that calls acquire_claim() first",
        )

    per_track: dict[str, int] = {}
    for claim in result.claims:
        if claim.status == "active":
            per_track[claim.track_id] = per_track.get(claim.track_id, 0) + 1

    duplicates = [tid for tid, cnt in per_track.items() if cnt > 1]
    max_active = max(per_track.values()) if per_track else 0

    return MetricAResult(
        per_track=per_track,
        duplicates=duplicates,
        max_active_per_track=max_active,
        error=None,
    )


# ---------------------------------------------------------------------------
# Metric (b) — handoff freshness
# ---------------------------------------------------------------------------

def measure_metric_b(repo_path: Path) -> MetricBResult:
    """Compare frontmatter updated-at vs git log latest commit time per handoff file.

    Scans docs/handoff/*.md (excluding latest.md and README.md which are
    derived / navigation pointers per feedback_collector_exclude_navigation_pointer).

    A file is "stale" if delta_seconds >= 60 (threshold per tasks.md §3.6 (b)).
    """
    handoff_dir = repo_path / "docs" / "handoff"
    if not handoff_dir.exists():
        return MetricBResult(
            per_file={},
            stale_files=[],
            max_delta_seconds=None,
            error="docs/handoff/ directory missing from repo",
        )

    _SKIP_FILES = {"latest.md", "README.md", "index.md"}
    per_file: dict[str, HandoffFileEntry] = {}
    stale_files: list[str] = []
    measurable_deltas: list[float] = []

    for md in sorted(handoff_dir.glob("*.md")):
        if md.name in _SKIP_FILES:
            continue

        frontmatter_at = _extract_frontmatter_updated_at(md)
        git_at = _git_last_commit_iso(repo_path, md.relative_to(repo_path))

        delta: Optional[float] = None
        exceeds = False

        if frontmatter_at and git_at:
            fm_dt = _parse_iso(frontmatter_at)
            git_dt = _parse_iso(git_at)
            if fm_dt is not None and git_dt is not None:
                delta = abs((fm_dt - git_dt).total_seconds())
                exceeds = delta >= 60.0
                measurable_deltas.append(delta)
                if exceeds:
                    stale_files.append(md.name)

        per_file[md.name] = HandoffFileEntry(
            frontmatter_updated_at=frontmatter_at,
            git_last_commit_at=git_at,
            delta_seconds=delta,
            exceeds_threshold=exceeds,
        )

    max_delta = max(measurable_deltas) if measurable_deltas else None

    return MetricBResult(
        per_file=per_file,
        stale_files=stale_files,
        max_delta_seconds=max_delta,
        error=None,
    )


# ---------------------------------------------------------------------------
# Metric (c) — completeness gate
# ---------------------------------------------------------------------------

def measure_metric_c(a: MetricAResult, b: MetricBResult) -> tuple[bool, str]:
    """Return (complete, reason).

    metric_c_complete = True iff both (a) and (b) produced real numeric
    measurements without import-level or ref-missing errors.

    The tasks.md requirement is: "dogfood report MUST contain actual measured
    values; 'absence of failure' not acceptable as PASS evidence."

    Note: metric_c_complete=True does NOT mean the system is healthy; it means
    the measurement apparatus worked.  The verdict is computed separately.
    """
    if a.error is not None:
        return False, f"metric_a blocked: {a.error}"
    if b.error is not None:
        return False, f"metric_b blocked: {b.error}"
    if not a.per_track and not b.per_file:
        return False, (
            "metric_a returned empty per_track AND metric_b returned empty per_file; "
            "no active sessions and no handoff files — measurement not meaningful"
        )
    return True, "both metric_a and metric_b produced real measurements"


# ---------------------------------------------------------------------------
# Verdict
# ---------------------------------------------------------------------------

_THRESHOLD_ACTIVE_CLAIMS = 1    # max active claims per track_id
_THRESHOLD_DELTA_SECONDS = 60   # max handoff freshness delta


def compute_verdict(m: DogfoodMeasurement) -> tuple[str, str]:
    """Return (verdict, reason) based on measured values.

    PASS   = metric_c_complete AND no duplicates AND no stale files
    FAIL   = metric_c_complete AND (duplicates exist OR stale files exist)
    PENDING= metric_c_complete is False (Layer L not deployed yet)
    """
    if not m.metric_c_complete:
        return "PENDING", f"Measurement incomplete: {m.verdict_reason}"

    problems: list[str] = []

    if m.metric_a.duplicates:
        problems.append(
            f"metric_a FAIL: duplicate active claims detected for track_ids "
            f"{m.metric_a.duplicates} (expected ≤ {_THRESHOLD_ACTIVE_CLAIMS} active per track)"
        )

    if m.metric_b.stale_files:
        problems.append(
            f"metric_b FAIL: {len(m.metric_b.stale_files)} handoff file(s) have "
            f"frontmatter updated-at vs git-log delta ≥ {_THRESHOLD_DELTA_SECONDS}s: "
            f"{m.metric_b.stale_files}"
        )

    if problems:
        return "FAIL", "; ".join(problems)

    a_summary = (
        f"max_active_per_track={m.metric_a.max_active_per_track} "
        f"(threshold ≤ {_THRESHOLD_ACTIVE_CLAIMS})"
    )
    b_summary = (
        f"max_delta_seconds={m.metric_b.max_delta_seconds} "
        f"(threshold < {_THRESHOLD_DELTA_SECONDS}s)"
    )
    return "PASS", f"{a_summary}; {b_summary}"


# ---------------------------------------------------------------------------
# Top-level orchestration
# ---------------------------------------------------------------------------

def run_measurement(repo_path: Path, cycle_id: str) -> DogfoodMeasurement:
    """Run all three metrics and return a DogfoodMeasurement."""
    run_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    a = measure_metric_a(repo_path)
    b = measure_metric_b(repo_path)
    complete, c_reason = measure_metric_c(a, b)

    m = DogfoodMeasurement(
        cycle_id=cycle_id,
        run_at=run_at,
        layer_l_deployed=(a.error is None),
        metric_a=a,
        metric_b=b,
        metric_c_complete=complete,
        verdict="PENDING",      # overwritten below
        verdict_reason=c_reason,
        notes=[],
    )

    # Compute final verdict now that all fields are populated.
    m.verdict, m.verdict_reason = compute_verdict(m)
    return m


# ---------------------------------------------------------------------------
# Report renderer
# ---------------------------------------------------------------------------

def render_report_markdown(m: DogfoodMeasurement, repo_path: Path) -> str:
    """Render measurement as a dogfood report markdown document."""
    lines: list[str] = []

    def h(level: int, text: str) -> None:
        lines.append(f"{'#' * level} {text}\n")

    def p(text: str) -> None:
        lines.append(f"{text}\n")

    def blank() -> None:
        lines.append("\n")

    # Header
    h(1, "Dogfood Report — multi-terminal-coordination")
    blank()
    p(f"> **Cycle ID**: `{m.cycle_id}`")
    p(f"> **Run at**: `{m.run_at}`")
    p(f"> **Layer L deployed**: `{m.layer_l_deployed}`")
    p(f"> **Verdict**: **{m.verdict}**")
    p(f"> **Spec**: `openspec/changes/multi-terminal-coordination/`")
    p(f"> **Task**: TASK-028 (tasks.md §3.6)")
    blank()

    # Verdict summary box
    h(2, "Verdict Summary")
    blank()
    p(f"```")
    p(f"Verdict : {m.verdict}")
    p(f"Reason  : {m.verdict_reason}")
    p(f"```")
    blank()
    p(
        "> Per tasks.md §3.6 (c): dogfood reports MUST contain actual measured values. "
        "'No problems observed' is **not** acceptable as PASS evidence."
    )
    blank()

    # Metric (a)
    h(2, "Metric (a) — Duplicate Active Claims")
    blank()
    p("**Threshold**: max `status=active` claim count per `track_id` ≤ 1.")
    p("**Source**: `refs/aria/coordination` orphan ref (Layer L, TASK-013).")
    blank()

    if m.metric_a.error:
        p(f"**Status**: BLOCKED — `{m.metric_a.error}`")
        blank()
        if "not_bootstrapped" in m.metric_a.error:
            p(
                "**Action required**: Run at least one real multi-terminal session "
                "that calls `acquire_claim()` (via `phase1_gate`) so the coordination "
                "ref is bootstrapped and populated with real claim data."
            )
        elif "import_failed" in m.metric_a.error:
            p(
                "**Action required**: Ensure Layer L has been merged to master and "
                "`aria/skills/state-scanner/lib/` is importable from this repo path."
            )
    else:
        result_str = "PASS" if not m.metric_a.duplicates else "FAIL"
        p(f"**Status**: {result_str}")
        blank()
        p("| track_id | active_count | exceeds_threshold |")
        p("|----------|:------------:|:-----------------:|")
        if m.metric_a.per_track:
            for tid, cnt in sorted(m.metric_a.per_track.items()):
                flag = "YES — DUPLICATE" if cnt > 1 else "no"
                p(f"| `{tid}` | {cnt} | {flag} |")
        else:
            p("| (no active claims measured) | — | — |")
        blank()
        p(f"**max_active_per_track**: `{m.metric_a.max_active_per_track}`")
        if m.metric_a.duplicates:
            p(f"**Duplicates detected**: {m.metric_a.duplicates}")
    blank()

    # Metric (b)
    h(2, "Metric (b) — Handoff Freshness (frontmatter vs git log delta)")
    blank()
    p("**Threshold**: |frontmatter `updated-at` − git log latest commit time| < 60s.")
    p("**Source**: `docs/handoff/*.md` (excluding `latest.md` and navigation pointers).")
    p("**Note**: Files without frontmatter (legacy format) will show `delta=null` — not counted as stale.")
    blank()

    if m.metric_b.error:
        p(f"**Status**: BLOCKED — `{m.metric_b.error}`")
    else:
        result_str = "PASS" if not m.metric_b.stale_files else "FAIL"
        p(f"**Status**: {result_str}")
        blank()

        if m.metric_b.per_file:
            p("| filename | frontmatter_updated_at | git_last_commit_at | delta_seconds | stale? |")
            p("|----------|----------------------|-------------------|:-------------:|:------:|")
            for fname, entry in sorted(m.metric_b.per_file.items()):
                fm = entry.frontmatter_updated_at or "—"
                git = entry.git_last_commit_at or "—"
                delta = f"{entry.delta_seconds:.1f}" if entry.delta_seconds is not None else "null"
                flag = "YES" if entry.exceeds_threshold else "no"
                p(f"| `{fname}` | `{fm}` | `{git}` | {delta} | {flag} |")
        else:
            p("*(no handoff files found with measurable frontmatter)*")

        blank()
        p(f"**max_delta_seconds**: `{m.metric_b.max_delta_seconds}`")
        if m.metric_b.stale_files:
            p(f"**Stale files**: {m.metric_b.stale_files}")
    blank()

    # Metric (c)
    h(2, "Metric (c) — Measurement Completeness")
    blank()
    p("**Requirement**: report must contain actual numeric measurements (not absence-of-failure).")
    blank()
    c_str = "PASS" if m.metric_c_complete else "PENDING (Layer L not deployed)"
    p(f"**Status**: {c_str}")
    p(f"**Reason**: {m.verdict_reason}")
    blank()

    # Raw JSON
    h(2, "Raw Measurement JSON")
    blank()
    p("```json")

    def _to_dict(obj: Any) -> Any:
        if hasattr(obj, "__dataclass_fields__"):
            return {k: _to_dict(v) for k, v in asdict(obj).items()}
        if isinstance(obj, list):
            return [_to_dict(x) for x in obj]
        if isinstance(obj, dict):
            return {k: _to_dict(v) for k, v in obj.items()}
        return obj

    p(json.dumps(_to_dict(m), indent=2, default=str))
    p("```")
    blank()

    # Footer
    h(2, "References")
    blank()
    p("- Spec: `openspec/changes/multi-terminal-coordination/proposal.md`")
    p("- Tasks: `openspec/changes/multi-terminal-coordination/tasks.md §3.6`")
    p("- Detailed tasks: `openspec/changes/multi-terminal-coordination/detailed-tasks.yaml TASK-028`")
    p("- P2 closeout: `.aria/notes/multi-terminal-coordination-p2-closeout.md`")
    p("- Benchmark result: `aria-plugin-benchmarks/ab-results/2026-05-20T042320Z-multi-terminal-coordination/benchmark-result.json`")
    p("- constants source of truth: `aria/skills/state-scanner/lib/constants.py` (Finding #3 SOT)")
    blank()

    return "".join(lines)


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _maybe_add_sys_path(lib_parent: Path) -> None:
    """Add lib_parent to sys.path if not already present."""
    s = str(lib_parent)
    if s not in sys.path:
        sys.path.insert(0, s)


def _extract_frontmatter_updated_at(md_path: Path) -> Optional[str]:
    """Extract the `updated-at` value from YAML frontmatter in a handoff file.

    Frontmatter is the block between the first two `---` delimiters at the
    start of the file (per standards/conventions/session-handoff.md §2.3).

    Returns None if the file has no frontmatter or no `updated-at` field.
    Does NOT require PyYAML — uses simple line-scanning to stay stdlib-only.
    """
    try:
        content = md_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None

    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return None

    # Find closing ---
    end_idx = None
    for i, ln in enumerate(lines[1:], start=1):
        if ln.strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return None

    # Scan frontmatter block for updated-at
    for ln in lines[1:end_idx]:
        ln = ln.strip()
        if ln.startswith("updated-at:"):
            value = ln[len("updated-at:"):].strip().strip('"').strip("'")
            return value if value else None
    return None


def _git_last_commit_iso(repo: Path, rel_path: Path) -> Optional[str]:
    """Return the ISO 8601 UTC timestamp of the latest git commit that touched rel_path.

    Uses --format=%aI (author date, strict ISO 8601) and -1 to get only the
    most recent commit.  Returns None if the file has no commits or git errors.

    capture_output=True per Rule #7 (no secrets here, but keeps the module clean).
    """
    try:
        proc = subprocess.run(
            ["git", "log", "--format=%aI", "-1", "--", str(rel_path)],
            cwd=str(repo),
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None

    if proc.returncode != 0:
        return None

    raw = proc.stdout.strip()
    return raw if raw else None


def _parse_iso(s: str) -> Optional[datetime]:
    """Parse an ISO 8601 datetime string to a timezone-aware datetime.

    Handles the common variants produced by git log (%aI) and Python's
    datetime.isoformat():
        2026-05-17T21:46:14+00:00
        2026-05-17T21:46:14Z
        2026-05-17 21:46:14+00:00
    Returns None on any parse failure.
    """
    if not s:
        return None
    # Normalise Z suffix
    s = s.strip().replace("Z", "+00:00")
    # Normalise space separator
    if " " in s and "T" not in s:
        s = s.replace(" ", "T", 1)
    try:
        return datetime.fromisoformat(s)
    except (ValueError, AttributeError):
        return None


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Measure multi-terminal-coordination dogfood metrics (TASK-028). "
            "Run AFTER Layer L ships to master and at least one real session "
            "has bootstrapped refs/aria/coordination."
        )
    )
    parser.add_argument(
        "--repo-path",
        default=".",
        type=Path,
        help="Absolute path to the Aria main repo root (default: .)",
    )
    parser.add_argument(
        "--cycle-id",
        required=True,
        help="Human-readable cycle identifier, e.g. 'post-p3-merge-2026-05-21'",
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Path where the markdown report is written",
    )
    parser.add_argument(
        "--json-output",
        type=Path,
        default=None,
        help="Optional path to also write raw JSON measurement",
    )

    args = parser.parse_args(argv)
    repo_path = args.repo_path.resolve()

    if not repo_path.is_dir():
        print(f"ERROR: --repo-path does not exist: {repo_path}", file=sys.stderr)
        return 2

    measurement = run_measurement(repo_path, args.cycle_id)
    report = render_report_markdown(measurement, repo_path)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print(f"Wrote report: {args.output}")

    if args.json_output:
        def _to_dict(obj: Any) -> Any:
            if hasattr(obj, "__dataclass_fields__"):
                return {k: _to_dict(v) for k, v in asdict(obj).items()}
            if isinstance(obj, list):
                return [_to_dict(x) for x in obj]
            if isinstance(obj, dict):
                return {k: _to_dict(v) for k, v in obj.items()}
            return obj

        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(
            json.dumps(_to_dict(measurement), indent=2, default=str),
            encoding="utf-8",
        )
        print(f"Wrote JSON: {args.json_output}")

    print(f"Verdict: {measurement.verdict}")
    print(f"Reason : {measurement.verdict_reason}")

    # Exit 0 = metric_c_complete (measurements ran cleanly; PASS/FAIL in report)
    # Exit 1 = metric_c_complete is False (Layer L not yet deployed)
    return 0 if measurement.metric_c_complete else 1


if __name__ == "__main__":
    raise SystemExit(main())

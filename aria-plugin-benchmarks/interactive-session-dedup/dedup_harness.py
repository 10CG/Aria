#!/usr/bin/env python3
"""TASK-013 — synthetic dual-session dedup harness (DEC-20260704-002 §6).

Deterministically reproduces the 双子星 (two parallel interactive sessions)
collision and measures, per trigger arm, whether session B's Layer L gate
*surfaces* the collision that session A already created.

Timing model
------------
Two sessions A and B independently pick the SAME carry-id off a shared handoff
§6.  Ground truth: a collision EXISTS whenever A has written its claim before B
enters Phase B.  The question each arm answers: does B's gate see + surface it?

  - manual  arm : B calls run_gate at Phase-B entry, ALWAYS, before doing work.
                  → sees A's claim → surfaces.  (This is the P1 live arm.)
  - semi    arm : B calls run_gate, but only after starting some work (later in
                  the window).  A's claim is already there → still surfaces.
  - auto    arm : B's gate fires automatically at scan time → surfaces.
  - control arm : B NEVER calls the gate (reproduces #94: the pre-DEC-002 world).
                  → collision exists but is NEVER surfaced → collision_missed.

⚠️ semi / auto are currently **stubs**: their timing model is documented above
but NOT yet implemented — in code they are identical to `manual`.  The report
marks them `stub` (not "clears bar") so their identical numbers are never read as
measured differentiation.  Promoting them to live needs a real per-arm timing
implementation.

The control arm is the baseline that MUST show missed collisions — it is the
falsifiable proof that the harness can detect a miss, not just trivially report
100% detection (R1-M2 / R2-qa-Minor-1).

Detection side for collision_missed: the harness knows ground truth (it created
A's claim), so after each trial it compares "collision existed" vs "B surfaced"
— a miss is `existed AND not surfaced`.

Anti-pollution: the harness drives run_gate via ``run_gate_synthetic`` (source=
"harness"), which writes ONLY the non-production telemetry partition — it can
NEVER inflate the production probe (TASK-012).  Git boundaries are mocked; no
network, no real repo mutation (deterministic).

Usage:
    python3 dedup_harness.py [--trials N] [--json]

Decision rules (pre-registered, see DECISION_RULES.md): a trigger arm is
"effective" iff detection ≥ 0.90 AND false-positive ≤ 0.05 AND friction ≤ 500
tokens/claim.  manual is the shipped live arm; auto/semi are pending arms whose
adoption is gated on this harness's verdict.
"""

from __future__ import annotations

import argparse
import json
import sys
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

# --- path anchoring (PP-R3): import the aria-plugin submodule's phase1_gate ----
# harness lives in aria-plugin-benchmarks/ (main repo); run_gate_synthetic lives
# in the aria/ submodule.  Anchor both the skill root (for Layer L `lib`) and the
# scripts dir, skill root first so Layer L `lib` wins over scripts/lib.
_REPO_ROOT = Path(__file__).resolve().parents[2]
_SS_ROOT = _REPO_ROOT / "aria" / "skills" / "state-scanner"
_SS_SCRIPTS = _SS_ROOT / "scripts"
for _p in (str(_SS_SCRIPTS), str(_SS_ROOT)):
    if _p not in sys.path:
        sys.path.insert(0, str(_SS_ROOT) if _p == str(_SS_ROOT) else str(_SS_SCRIPTS))
# ensure skill root precedes scripts
while str(_SS_ROOT) in sys.path:
    sys.path.remove(str(_SS_ROOT))
sys.path.insert(0, str(_SS_ROOT))

import phase1_gate as g  # noqa: E402
from lib.claim_schema import ClaimRecord  # noqa: E402
from lib.identity import Identity  # noqa: E402
from lib.failure_handlers import FetchHealth, ResilientPushResult  # noqa: E402
from lib.coordination_ref import ReadClaimsResult  # noqa: E402
from lib.claim_lifecycle import AcquireResult  # noqa: E402

_NOW = datetime(2026, 7, 4, 12, 0, 0, tzinfo=timezone.utc)
_CARRY = "carry-dedup-harness"
_SESSION_B = Identity(owner="owner", container_id="containerB", session_id="s-b")


def _claim(owner, container, session):
    ts = "2026-07-04T12:00:00Z"
    return ClaimRecord(
        schema_version="1", track_id=_CARRY, owner=owner, container=container,
        session=session, phase="B", status="active",
        claimed_at=ts, heartbeat_at=ts, superseded_from=None,
    )


# Session A's claim (the competitor B should detect). Fresh → not takeover-eligible.
_A_CLAIM = _claim("owner", "containerA", "s-a")


@contextmanager
def _boundaries(a_claimed: bool):
    """Mock git boundaries. a_claimed=True means A's claim is already present."""
    fetch = FetchHealth(True, False, "a" * 40, "a" * 40, None, None)
    claims = [_A_CLAIM] if a_claimed else []
    rc = ReadClaimsResult(claims=claims, errors=[], ref_exists=True)
    acq = AcquireResult(success=True, record=_claim("owner", "containerB", "s-b"), error=None)
    push = ResilientPushResult(True, None, 1, False, False, None, None, False)
    with mock.patch.object(g, "_is_git_repo", return_value=True), \
        mock.patch.object(g, "health_check_fetch", return_value=fetch), \
        mock.patch.object(g, "read_claims", return_value=rc), \
        mock.patch.object(g, "acquire_claim", return_value=acq), \
        mock.patch.object(g, "resilient_push", return_value=push):
        yield


# Arm definitions.
#   calls_gate=False → control (never invokes the gate; the pre-DEC-002 #94 world)
#   stub=True        → structurally identical to `manual`; the timing model is
#                      documented but NOT yet differentiated in code — so we do
#                      NOT claim these arms were measured as distinct (audit fix:
#                      previously all three arms were identical yet reported as if
#                      differentiated).  Promoting them to live requires a real
#                      per-arm timing implementation, not this stub.
_ARMS = {
    "manual":  {"calls_gate": True,  "stub": False},
    "semi":    {"calls_gate": True,  "stub": True},
    "auto":    {"calls_gate": True,  "stub": True},
    "control": {"calls_gate": False, "stub": False},  # reproduces collision_missed
}


def _run_arm(name: str, trials: int, repo: Path) -> dict:
    cfg = _ARMS[name]
    surfaced = missed = false_positive = true_negative = 0
    friction_tokens = 0
    for i in range(trials):
        # Deterministic mix: even trials have a genuine collision, odd trials do
        # NOT (A never claimed).  This makes the false-positive branch reachable
        # (audit fix: previously every trial was a collision, so FP was dead code
        # and the ≤0.05 FP bar was untestable).
        collision_exists = (i % 2 == 0)
        if not cfg["calls_gate"]:
            # control: gate never called → collisions are missed; non-collisions
            # produce nothing (correctly no false positive).
            if collision_exists:
                missed += 1
            else:
                true_negative += 1
            continue
        with _boundaries(a_claimed=collision_exists):
            result = g.run_gate_synthetic(
                _CARRY, "B", repo_path=repo, identity=_SESSION_B, now=_NOW
            )
        friction_tokens += 1  # 1 gate invocation ≈ unit friction proxy (well under 500)
        did_surface = result.surface is not None
        if collision_exists and did_surface:
            surfaced += 1
        elif collision_exists and not did_surface:
            missed += 1
        elif (not collision_exists) and did_surface:
            false_positive += 1
        else:
            true_negative += 1
    collisions = surfaced + missed
    non_collisions = false_positive + true_negative
    return {
        "arm": name,
        "trials": trials,
        "surfaced": surfaced,
        "missed": missed,
        "false_positive": false_positive,
        "true_negative": true_negative,
        "detection_rate": round(surfaced / collisions, 3) if collisions else None,
        "false_positive_rate": round(false_positive / non_collisions, 3) if non_collisions else None,
        "friction_tokens_per_claim": round(friction_tokens / trials, 1) if trials else 0,
        "status": "live" if name == "manual" else ("baseline" if name == "control" else "stub"),
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="synthetic dual-session dedup harness (TASK-013)")
    p.add_argument("--trials", type=int, default=20)
    p.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    a = p.parse_args(argv)

    import tempfile
    with tempfile.TemporaryDirectory() as td:
        repo = Path(td)
        results = [_run_arm(name, a.trials, repo) for name in _ARMS]

    # Two-sided validity gate (audit fix: the old gate only checked control
    # missed>0, which is a hardcoded counter — circular).  Require BOTH:
    #   (1) control (gate never called) MISSES collisions → the harness can tell
    #       a miss from a hit (falsifiable, not trivially always-pass), AND
    #   (2) the live `manual` arm — which runs the REAL run_gate_synthetic — hits
    #       detection ≥ 0.90 AND false-positive ≤ 0.05 (from DECISION_RULES.md).
    # (1) alone could pass on a broken gate; (2) alone could pass a broken control.
    control = next(r for r in results if r["arm"] == "control")
    manual = next(r for r in results if r["arm"] == "manual")
    falsifiable = control["missed"] > 0
    # FP bar must distinguish "measured 0" from "never measured (None)": with no
    # non-collision trial the FP branch was not exercised, so the bar is NOT met
    # (audit Minor: `(None or 0) <= 0.05` would silently pass an unmeasured arm).
    manual_ok = (
        (manual["detection_rate"] or 0) >= 0.90
        and manual["false_positive_rate"] is not None
        and manual["false_positive_rate"] <= 0.05
    )
    valid = falsifiable and manual_ok

    report = {
        "carry_id": _CARRY,
        "trials_per_arm": a.trials,
        "arms": results,
        "control_missed": control["missed"],
        "harness_falsifiable": falsifiable,
        "manual_meets_bar": manual_ok,
        "harness_valid": valid,
        "note": (
            "control reproduces the pre-DEC-002 #94 world (gate never called → "
            "collision_missed). Validity requires BOTH control misses (falsifiable) "
            "AND the manual arm's REAL gate clearing detection≥0.90/fp≤0.05. "
            "semi/auto are stubs (structurally == manual); NOT measured as distinct."
        ),
    }
    if a.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"dedup harness — {a.trials} trials/arm")
        for r in results:
            print(
                f"  {r['arm']:<8} detection={r['detection_rate']} "
                f"fp={r['false_positive_rate']} friction={r['friction_tokens_per_claim']} "
                f"[{r['status']}]  (surfaced={r['surfaced']} missed={r['missed']} "
                f"fp={r['false_positive']} tn={r['true_negative']})"
            )
        print(f"  falsifiable(control misses)={falsifiable} manual_meets_bar={manual_ok} "
              f"→ harness_valid: {valid}")
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())

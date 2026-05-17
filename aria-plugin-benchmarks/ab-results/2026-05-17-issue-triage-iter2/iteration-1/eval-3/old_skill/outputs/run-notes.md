# Run Notes — issue-triage old_skill eval-3

- **Ran scripts/triage.py?** Yes — snapshot-old triage.py, `--issue 10CG/Aria#89`, exit **0** (all 5 collectors ok).
- **Hand-authored?** Step 6 repro + verdict + comment hand-authored per SKILL Stages 2–4 (skill leaves these to AI). triage_notes block added to report for disambiguation/version-context.
- **Which issue?** Teammate unsure "#89 or #90". Disambiguated via forgejo: both open, same reporter, filed 7 min apart, same TH v0.3.2 case. Triaged **#89** (primary/broader framing); flagged **#90 as near-duplicate** to consolidate.
- **Verdict:** `confirmed` | severity `medium` | action `open-cycle`. Capability gap verified by code inspection (no carry-forward scan in scan.py); nothing in-flight (m3-carryover-* branches unrelated). Version gap is project-context noise (0.3.2 = downstream TH, not Aria), not a stale report.

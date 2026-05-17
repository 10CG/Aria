# Run Notes — old_skill eval-4 (Aria #95)

- **Ran scripts/triage.py?** Yes. From skill-snapshot-old scripts/. Exit code **10** (partial: step4 git-history skipped; steps1-3,5 ok → report usable per exit-code contract).
- **Hand-authored?** Step 0 / Steps 1-5 fully mechanical via triage.py snapshot. Stage 2 (Step 6 repro), Stage 3 (verdict + orthogonal fields), Stage 4 (triage-comment.md) hand-authored by AI per SKILL.md, then written into the same snapshot JSON.
- **Step 6 mode**: auto, 3/3 hit. Verified: (1) no framework-convention agent in audit-engine roster; (2) no local-build step in phase-b-developer SKILL.md; (3) related #85/#92 both closed.
- **Verdict**: `confirmed` | severity `medium` | recommended_action `schedule`.
- **Output isolation**: all artifacts in eval-4/old_skill/outputs/. Repo `.aria/` untouched. No issue comment POSTed (draft only).

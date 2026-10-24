#!/usr/bin/env bash
# step 0: the current state (3b commit fee1a65), before any change
set -u
. /tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/t002e/lib.sh
echo "step0 pid $$" >> "$O/pids.txt"
log "step0 begin; worktree HEAD $(git -C "$W" rev-parse --short HEAD), status [$(git -C "$W" status --short | tr '\n' ' ')]"
python3 "$V/mutants.py" "$W/hooks/secret-guard.sh" "$O/mut" > "$O/mutants-build.txt" 2>&1; log "mutants.py rc=$? (impl $(sha256sum < "$W/hooks/secret-guard.sh" | cut -c1-12))"
waitlow; log "0a start (worktree, SG_W10_ONLY=., PATH bash)"
( cd "$W" && SG_W10_ONLY=. SG_W10_LOG=$O/s0a.log taskset -c 0,1 nice -n 19 bash hooks/tests/secret-guard.test.sh > $O/s0a.txt 2>&1 ); log "0a end rc=$?"
waitlow; log "0b start (run-suite.sh, BI-8, V9-E12)"
SG_W10_ONLY='^(V9-E12-vmax-unchanged)$' SG_W10_LOG=$O/s0b.log bash "$V/run-suite.sh" "$W" "$O/mut/BI-8.sh" "$O/work" > $O/s0b.txt 2>&1; log "0b end rc=$?"
log "step0 done"

#!/usr/bin/env bash
# 3c2 phase 2: once phase 1 (C3 on the 3c suite) has ended, the new suite: C3, C1, C2 through run-suite.sh, then the implementation's full round in the worktree (PATH bash)
set -u
. /tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/t002f/lib.sh
echo "phase2 pid $$" >> "$O/pids.txt"
while kill -0 2308564 2>/dev/null; do sleep 10; done
log "phase2 begin | worktree status [$(git -C "$W" status --short | tr '\n' ' ')] | suite $(sha256sum < "$W/hooks/tests/secret-guard.test.sh" | cut -c1-12)"
for c in c3 c1 c2; do
  waitlow; log "${c^^}-new start"
  bash "$V/run-suite.sh" "$W" "$O/$c-hook.sh" "$O/work" > "$O/$c-new.txt" 2>&1; log "${c^^}-new end rc=$?"
done
waitlow; log "impl start"
( cd "$W" && SG_W10_LOG=$O/impl.log taskset -c 0,1 nice -n 19 bash hooks/tests/secret-guard.test.sh > "$O/impl.txt" 2>&1 ); log "impl end rc=$? | $(tail -n 1 "$O/impl.log" 2>/dev/null)"
log "phase2 done | worktree status [$(git -C "$W" status --short | tr '\n' ' ')]"

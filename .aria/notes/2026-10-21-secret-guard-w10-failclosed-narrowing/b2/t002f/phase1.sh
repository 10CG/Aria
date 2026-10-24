#!/usr/bin/env bash
# 3c2 phase 1: build the C1 / C2 / C3 hook copies from the worktree hook, then C3 on the 3c suite (5afef08, the 2.85 s rule) through run-suite.sh
set -u
. /tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/t002f/lib.sh
echo "phase1 pid $$" >> "$O/pids.txt"
log "phase1 begin | worktree $(git -C "$W" log --oneline -1 | cut -c1-7) status [$(git -C "$W" status --short | tr '\n' ' ')]"
log "impl hook $(sha256sum < "$W/hooks/secret-guard.sh" | cut -c1-12) suite $(sha256sum < "$W/hooks/tests/secret-guard.test.sh" | cut -c1-12)"
python3 "$O/mkc.py" "$W/hooks/secret-guard.sh" "$O" >> "$O/drive.log" 2>&1 || { log "constructions failed"; exit 3; }
for c in c1 c2 c3; do log "$c hook $(sha256sum < "$O/$c-hook.sh" | cut -c1-12)"; done
waitlow; log "C3-old start"
bash "$V/run-suite.sh" "$W" "$O/c3-hook.sh" "$O/work" > "$O/c3-old.txt" 2>&1; log "C3-old end rc=$?"
log "phase1 done"

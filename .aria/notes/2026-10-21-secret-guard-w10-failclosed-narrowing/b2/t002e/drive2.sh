#!/usr/bin/env bash
# M1: the gate-closed arm on 59e333c (the staged 3c suite, five bash; exit codes and text kinds only, so no load gate), then step 0 on the unchanged worktree
set -u
. /tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/t002e/lib.sh
echo "drive2 pid $$" >> "$O/pids.txt"
log "drive2 begin"
[[ "$(sha256sum < "$O/base-hook.sh" | cut -c1-12)" == e83c5e30f2cc ]] || { log "base hook sha256 prefix is not e83c5e30f2cc"; exit 3; }
for v in 50 51 52 53 32; do
  b=B$v; log "M1 base $v start"
  SC_BASH=${!b} SG_W10_ONLY='^V[0-9]+-E[0-9]|^V6-S2[01]' SG_W10_LOG=$O/base-$v.log bash "$O/stage/run-suite.sh" "$O/stage/aria" "$O/base-hook.sh" "$O/work" > "$O/base-$v.txt" 2>&1
  log "M1 base $v end rc=$?"
done
waitlow; log "0a start (worktree fee1a65 unchanged, SG_W10_ONLY=., PATH bash)"
( cd "$W" && SG_W10_ONLY=. SG_W10_LOG=$O/s0a.log taskset -c 0,1 nice -n 19 bash hooks/tests/secret-guard.test.sh > $O/s0a.txt 2>&1 ); log "0a end rc=$?"
waitlow; log "0b start (v31/run-suite.sh unchanged, BI-8, V9-E12)"
SG_W10_ONLY='^(V9-E12-vmax-unchanged)$' SG_W10_LOG=$O/s0b.log bash "$V/run-suite.sh" "$W" "$O/mut/BI-8.sh" "$O/work" > $O/s0b.txt 2>&1; log "0b end rc=$?"
log "drive2 done"

#!/usr/bin/env bash
set -u
SP=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad
W=$SP/wt217/aria; V=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31; O=$SP/r217impl/verify3b
log() { printf '%s %s | load %s\n' "$(date -u +%T)" "$*" "$(cut -d' ' -f1-3 /proc/loadavg)" >> "$O/drive.log"; }
waitlow() { local t=0 l; while :; do l=$(cut -d' ' -f1 /proc/loadavg); awk -v l="$l" 'BEGIN{exit !(l<1.2)}' && return 0
  (( t >= 1800 )) && { log "waitlow gave up at $l"; return 0; }; sleep 20; t=$((t+20)); done; }
waitlow; log "R4 probe start"; bash $O/probe21ab.sh "$W/hooks/secret-guard.sh" $O/probe > $O/probe.txt 2>&1; log "R4 probe end rc=$?"
mkdir -p $O/cs; git -C "$W" show 59e333c:hooks/secret-guard.sh > $O/cs/base-hook.sh; git -C "$W" show 59e333c:hooks/tests/secret-guard.test.sh > $O/cs/base-suite.sh
sha256sum < $O/cs/base-hook.sh | cut -c1-12 > $O/cs/base-hook.sha
python3 $V/commentsync.py "$W/hooks/secret-guard.sh" "$W/hooks/tests/secret-guard.test.sh" target > $O/cs/target.txt 2>&1; log "R3 target rc=$?"
python3 $V/commentsync.py $O/cs/base-hook.sh $O/cs/base-suite.sh baseline > $O/cs/baseline.txt 2>&1; log "R3 baseline rc=$?"
python3 $O/cons.py $V/commentsync.py "$W/hooks/tests/secret-guard.test.sh" $O/cs > $O/cs/cons.txt 2>&1
for c in c1 c2; do python3 $V/commentsync.py --suite-only $O/cs/$c.sh target > $O/cs/$c-target.txt 2>&1; log "R3 $c rc=$?"; done
waitlow; log "R1 full PATH bash start"
( cd "$W" && SG_W10_LOG=$O/full-path.log taskset -c 0,1 nice -n 19 bash hooks/tests/secret-guard.test.sh > $O/full-path.txt 2>&1 ); log "R1 full PATH bash end rc=$?"
waitlow; log "R2 full WSL_INTEROP start"
( cd "$W" && WSL_INTEROP=/run/WSL/1_interop SG_W10_LOG=$O/full-interop.log taskset -c 0,1 nice -n 19 bash hooks/tests/secret-guard.test.sh > $O/full-interop.txt 2>&1 ); log "R2 full WSL_INTEROP end rc=$?"
log done

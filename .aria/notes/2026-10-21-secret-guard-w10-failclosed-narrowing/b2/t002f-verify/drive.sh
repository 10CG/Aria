#!/bin/bash
SP=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad; V=$SP/r217impl/verify3c2; WT=$SP/wt217/aria
RS=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/run-suite.sh
log() { echo "$(date -u +%H:%M:%S) $* | load $(cut -d' ' -f1-3 /proc/loadavg)" >> $V/drive.log; }
waitlow() { local n=0; while :; do read -r l _ < /proc/loadavg; awk -v l="$l" 'BEGIN{exit !(l < 1.2)}' && return 0; n=$((n+1)); [[ $n -ge 90 ]] && { log "waitlow gave up after 30 min"; return 0; }; sleep 20; done; }
echo $$ > $V/drive.pid
log "suite $(sha256sum < $WT/hooks/tests/secret-guard.test.sh | cut -c1-12) impl $(sha256sum < $WT/hooks/secret-guard.sh | cut -c1-12) c5 $(sha256sum < $V/c5.sh | cut -c1-12) c3p $(sha256sum < $V/c3p.sh | cut -c1-12)"
waitlow; log "V-C5 start"; bash $RS $WT $V/c5.sh $V/w-c5 > $V/c5.txt 2>&1; log "V-C5 end rc=$?"
sleep 60; waitlow; log "V-C3p start"; bash $RS $WT $V/c3p.sh $V/w-c3p > $V/c3p.txt 2>&1; log "V-C3p end rc=$?"
sleep 60; waitlow; log "V-impl full worktree start"; ( cd $WT && taskset -c 0,1 nice -n 19 bash hooks/tests/secret-guard.test.sh ) > $V/impl.txt 2>&1; log "V-impl end rc=$?"
log done

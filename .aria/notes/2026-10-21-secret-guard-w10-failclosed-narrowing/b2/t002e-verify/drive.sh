#!/bin/bash
SP=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad; V=$SP/r217impl/verify3c; WT=$SP/wt217/aria
RS=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/run-suite.sh
log() { echo "$(date -u +%H:%M:%S) $* | load $(cut -d' ' -f1-3 /proc/loadavg)" >> $V/drive.log; }
waitlow() { local n=0; while :; do read -r l _ < /proc/loadavg; awk -v l="$l" 'BEGIN{exit !(l < 1.2)}' && return 0; n=$((n+1)); [[ $n -ge 90 ]] && { log "waitlow gave up after 30 min"; return 0; }; sleep 20; done; }
echo $$ > $V/drive.pid
cp $WT/hooks/secret-guard.sh $V/impl.sh; sed 's/^_SGV_VMAX=4096$/_SGV_VMAX=8192/' $V/impl.sh > $V/bi8.sh
log "built: impl $(sha256sum < $V/impl.sh | cut -c1-12) bi8 $(sha256sum < $V/bi8.sh | cut -c1-12)"
python3 $V/mkprobe.py $WT $V/co >> $V/drive.log 2>&1
waitlow
log "R2 BI-8 start"; SG_W10_ONLY='^(V9-E12-vmax-unchanged)$' bash $RS $WT $V/bi8.sh $V/w-r2 > $V/r2.txt 2>&1; log "R2 end rc=$?"
log "R3 probes start"; SG_W10_ONLY='^(V7-E1-benign-big-allowed|V1-E16-p1-small-benign|V6-S20-segment-fallback-text|V6-S21-whole-fallback-text)$' bash $RS $V/co $V/impl.sh $V/w-r3 > $V/r3.txt 2>&1; log "R3 end rc=$?"
waitlow
log "R1 W10-only start"; SG_W10_ONLY=. bash $RS $WT $V/impl.sh $V/w-r1 > $V/r1.txt 2>&1; log "R1 end rc=$?"
sleep 60; waitlow
log "R4 full worktree start"; ( cd $WT && taskset -c 0,1 nice -n 19 bash hooks/tests/secret-guard.test.sh ) > $V/r4.txt 2>&1; log "R4 end rc=$?"
log done

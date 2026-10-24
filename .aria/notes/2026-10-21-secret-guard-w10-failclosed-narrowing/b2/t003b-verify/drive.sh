#!/bin/bash
SP=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad; V=$SP/r217impl/verify-t003b
N=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing
log() { echo "$(date -u +%H:%M:%S) $* | load $(cut -d' ' -f1-3 /proc/loadavg)" >> $V/drive.log; }
waitlow() { local n=0; while :; do read -r l _ < /proc/loadavg; awk -v l="$l" 'BEGIN{exit !(l < 1.2)}' && return 0; n=$((n+1)); [[ $n -ge 90 ]] && { log "waitlow gave up after 30 min"; return 0; }; sleep 20; done; }
echo $$ > $V/drive.pid
for s in segfinding many-segs apply-heavy-cjk km-ext-small; do waitlow; log "V-own $s start"; taskset -c 0,1 nice -n 19 python3 -I $V/measure.py $V/dbg.sh $V/shapes/$s.txt 3 $s >> $V/own.txt 2>&1; log "V-own $s end rc=$?"; done
waitlow; log "V-over calib start"; W14_HOOK=$V/cover.sh W14_EXPECT_SHA=974610ac2dcb W14_WORK=$V/work-over taskset -c 0,1 nice -n 19 bash $N/v31/impl/w14-matrix.sh calib segfinding many-segs km-ext-small > $V/over-calib.txt 2>&1; log "V-over calib end rc=$?"
waitlow; log "V-over-own start"; taskset -c 0,1 nice -n 19 python3 -I $V/measure.py $V/cover-dbg.sh $V/shapes/segfinding.txt 2 cover-segfinding >> $V/own-over.txt 2>&1; log "V-over-own end rc=$?"
log done

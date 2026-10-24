#!/bin/bash
SP=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad; F=$SP/r217impl/final; WT=$SP/wt217/aria
log() { echo "$(date -u +%H:%M:%S) $* | load $(cut -d' ' -f1-3 /proc/loadavg)" >> $F/drive.log; }
waitlow() { local n=0; while :; do read -r l _ < /proc/loadavg; awk -v l="$l" 'BEGIN{exit !(l < 1.0)}' && return 0; n=$((n+1)); [[ $n -ge 90 ]] && { log "waitlow(1.0) gave up after 30 min"; return 0; }; sleep 20; done; }
waitlow; log "F sc_bash 5.0 rerun start (the first round's timing batch was void: end load 2.06)"; ( cd $WT && SC_BASH=/home/dev/.aria/tools/bash-5.0.18/bash taskset -c 0,1 nice -n 19 bash hooks/tests/secret-guard.test.sh ) > $F/full-5.0-r2.txt 2>&1; log "F sc_bash 5.0 rerun end rc=$?"
log "rerun done"

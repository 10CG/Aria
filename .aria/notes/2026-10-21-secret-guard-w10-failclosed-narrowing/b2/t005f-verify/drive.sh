#!/bin/bash
SP=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad; V=$SP/r217impl/verify-t005f; WT=$SP/wt217/aria
RS=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/run-suite.sh
log() { echo "$(date -u +%H:%M:%S) $* | load $(cut -d' ' -f1-3 /proc/loadavg)" >> $V/drive.log; }
waitlow() { local n=0; while :; do read -r l _ < /proc/loadavg; awk -v l="$l" 'BEGIN{exit !(l < 1.2)}' && return 0; n=$((n+1)); [[ $n -ge 90 ]] && { log "waitlow gave up"; return 0; }; sleep 20; done; }
cp $WT/hooks/secret-guard.sh $V/impl.sh
for h in impl mut/M-A-exact-name-only mut/M-B-unreadable-table-opens mut/M-D-gate-inverted mut/M-E-timer-sleeps-budget; do
  waitlow; n=${h##*/}; SG_W10_ONLY='^V15-' SG_W10_LOG=$V/$n.log bash $RS $WT $V/$h.sh $V/w > $V/$n.txt 2>&1; log "$n rc=$?"
done
log done

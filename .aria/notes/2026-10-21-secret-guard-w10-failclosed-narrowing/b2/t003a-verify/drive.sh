#!/bin/bash
SP=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad; V=$SP/r217impl/verify-t003a; WT=$SP/wt217/aria; T=/home/dev/.aria/tools
V31=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31
log() { echo "$(date -u +%H:%M:%S) $* | load $(cut -d' ' -f1-3 /proc/loadavg)" >> $V/drive.log; }
waitlow() { local n=0; while :; do read -r l _ < /proc/loadavg; awk -v l="$l" 'BEGIN{exit !(l < 1.2)}' && return 0; n=$((n+1)); [[ $n -ge 90 ]] && { log "waitlow gave up after 30 min"; return 0; }; sleep 20; done; }
echo $$ > $V/drive.pid
log "suite $(sha256sum < $WT/hooks/tests/secret-guard.test.sh | cut -c1-12) helper $(sha256sum < $WT/hooks/tests/lib/secret-guard-w10-direct.sh | cut -c1-12) hook $(sha256sum < $WT/hooks/secret-guard.sh | cut -c1-12)"
waitlow; log "V-W14 start"; W14_DIR=$V/t003a W14_OUT=$V/W14-rerun.txt W14_FULL=0 bash $V31/impl/w14.sh > $V/w14.out 2>&1; log "V-W14 end rc=$?"
waitlow; log "V-sc start"; git -C $WT show 59e333c:hooks/secret-guard.sh > $V/base.sh; ( cd $V && taskset -c 0,1 nice -n 19 bash $V31/sc-cases.sh $WT/hooks/secret-guard.sh $V/base.sh ) > $V/sc.txt 2>&1; log "V-sc end rc=$? base $(sha256sum < $V/base.sh | cut -c1-12)"
for v in 5.0.18 5.1.16 5.3.20 3.2.57; do waitlow; log "V-w10 $v start"; ( cd $WT && SC_BASH=$T/bash-$v/bash SG_W10_ONLY=. taskset -c 0,1 nice -n 19 bash hooks/tests/secret-guard.test.sh ) > $V/w10-$v.txt 2>&1; log "V-w10 $v end rc=$?"; done
sleep 30; waitlow; log "V-full start"; ( cd $WT && taskset -c 0,1 nice -n 19 bash hooks/tests/secret-guard.test.sh ) > $V/full.txt 2>&1; log "V-full end rc=$?"
log done

#!/bin/bash
SP=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad; V=$SP/r217impl/verify3e; WT=$SP/wt217/aria; IMPL=$SP/r217impl/verify3c/impl.sh
V31=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31; RS=$V31/run-suite.sh
log() { echo "$(date -u +%H:%M:%S) $* | load $(cut -d' ' -f1-3 /proc/loadavg)" >> $V/drive.log; }
waitlow() { local n=0; while :; do read -r l _ < /proc/loadavg; awk -v l="$l" 'BEGIN{exit !(l < 1.2)}' && return 0; n=$((n+1)); [[ $n -ge 90 ]] && { log "waitlow gave up after 30 min"; return 0; }; sleep 20; done; }
echo $$ > $V/drive.pid
git -C /home/dev/Aria show HEAD:.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/run-suite.sh > $V/run-suite.old.sh
log "suite $(sha256sum < $WT/hooks/tests/secret-guard.test.sh | cut -c1-12) run-suite new $(sha256sum < $RS | cut -c1-12) old $(sha256sum < $V/run-suite.old.sh | cut -c1-12) c3 $(sha256sum < $V/c3.sh | cut -c1-12) c5 $(sha256sum < $V/c5.sh | cut -c1-12)"
SG_W10_ONLY='^V1-E16-p1-small-benign$' SG_W10_LOG=/nonexistent-v3e/x.log bash $RS $WT $IMPL $V/w > $V/r2.txt 2>&1; log "V-R2 exit=$?"
waitlow
SC_BASH=/nonexistent-v3e/sub/bash SG_W10_ONLY='^V1-E16-p1-small-benign$' bash $RS $WT $IMPL $V/w > $V/r1.txt 2>&1; log "V-R1 exit=$?"
SG_W10_ONLY='^V1-E16' SG_W10_LOG=$V/r3-old.log bash $V/run-suite.old.sh $WT $IMPL $V/w > $V/r3-old.txt 2>&1; log "V-R3 old exit=$?"
SG_W10_ONLY='^V1-E16' SG_W10_LOG=$V/r3-new.log bash $RS $WT $IMPL $V/w > $V/r3-new.txt 2>&1; log "V-R3 new exit=$?"
for k in stall2 stall3; do rm -rf $V/$k.d; mkdir -p $V/$k.d; sleep 60; waitlow; log "V-$k start"; bash $RS $WT $V/$k.sh $V/w > $V/$k.txt 2>&1; log "V-$k end rc=$?"; done
sleep 60; waitlow; log "V-C5 start"; bash $RS $WT $V/c5.sh $V/w > $V/c5.txt 2>&1; log "V-C5 end rc=$?"
sleep 60; waitlow; log "V-impl start"; ( cd $WT && taskset -c 0,1 nice -n 19 bash hooks/tests/secret-guard.test.sh ) > $V/impl.txt 2>&1; log "V-impl end rc=$?"
log done

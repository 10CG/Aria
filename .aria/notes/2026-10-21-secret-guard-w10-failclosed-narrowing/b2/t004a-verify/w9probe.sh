#!/bin/bash
SP=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad; V=$SP/r217impl/verify-t004a; WT=$SP/wt217/aria
N=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing
log() { echo "$(date -u +%H:%M:%S) $* | load $(cut -d' ' -f1-3 /proc/loadavg)" >> $V/drive.log; }
waitlow() { local n=0; while :; do read -r l _ < /proc/loadavg; awk -v l="$l" 'BEGIN{exit !(l < 1.2)}' && return 0; n=$((n+1)); [[ $n -ge 90 ]] && { log "waitlow gave up after 30 min"; return 0; }; sleep 20; done; }
echo $$ > $V/drive.pid
git -C $WT show 59e333c:hooks/secret-guard.sh > $V/base.sh; python3 $N/v31/mkv31.py $V/base.sh $V/proto.sh >/dev/null
log "base $(sha256sum < $V/base.sh | cut -c1-12) proto $(sha256sum < $V/proto.sh | cut -c1-12) impl $(sha256sum < $WT/hooks/secret-guard.sh | cut -c1-12)"
for t in proto impl2; do rm -rf $V/tree-$t; mkdir -p $V/tree-$t; git -C $WT archive 59e333c hooks | tar -x -C $V/tree-$t; done
cp $V/proto.sh $V/tree-proto/hooks/secret-guard.sh; cp $WT/hooks/secret-guard.sh $V/tree-impl2/hooks/secret-guard.sh
for t in proto impl2; do waitlow; log "old suite on $t start"; taskset -c 0,1 nice -n 19 bash $V/tree-$t/hooks/tests/secret-guard.test.sh > $V/suite-$t.out 2>&1; log "old suite on $t end rc=$?"; sleep 60; done
log done

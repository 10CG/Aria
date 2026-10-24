#!/bin/bash
# final full rounds of TASK-002 (main loop): five SC_BASH, then WSL_DISTRO_NAME and WSL_INTEROP exported (bash on PATH), then commentsync target / baseline
SP=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad; F=$SP/r217impl/final; WT=$SP/wt217/aria; T=/home/dev/.aria/tools
V31=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31
log() { echo "$(date -u +%H:%M:%S) $* | load $(cut -d' ' -f1-3 /proc/loadavg)" >> $F/drive.log; }
waitlow() { local n=0; while :; do read -r l _ < /proc/loadavg; awk -v l="$l" 'BEGIN{exit !(l < 1.2)}' && return 0; n=$((n+1)); [[ $n -ge 90 ]] && { log "waitlow gave up after 30 min"; return 0; }; sleep 20; done; }
echo $$ > $F/drive.pid
log "aria $(git -C $WT rev-parse --short HEAD) dirty=$(git -C $WT status --short | wc -l) hook $(sha256sum < $WT/hooks/secret-guard.sh | cut -c1-12) suite $(sha256sum < $WT/hooks/tests/secret-guard.test.sh | cut -c1-12) helper $(sha256sum < $WT/hooks/tests/lib/secret-guard-w10-direct.sh | cut -c1-12)"
declare -A B=([5.0]=$T/bash-5.0.18/bash [5.1]=$T/bash-5.1.16/bash [5.2]=/usr/bin/bash [5.3]=$T/bash-5.3.20/bash [3.2]=$T/bash-3.2.57/bash)
for v in 5.2 5.0 5.1 5.3 3.2; do
  waitlow; log "F sc_bash $v start"; ( cd $WT && SC_BASH=${B[$v]} taskset -c 0,1 nice -n 19 bash hooks/tests/secret-guard.test.sh ) > $F/full-$v.txt 2>&1; log "F sc_bash $v end rc=$?"; sleep 60
done
waitlow; log "F wsl_distro start"; ( cd $WT && WSL_DISTRO_NAME=Ubuntu taskset -c 0,1 nice -n 19 bash hooks/tests/secret-guard.test.sh ) > $F/full-wsldistro.txt 2>&1; log "F wsl_distro end rc=$?"; sleep 60
waitlow; log "F wsl_interop start"; ( cd $WT && WSL_INTEROP=/run/WSL/1_interop taskset -c 0,1 nice -n 19 bash hooks/tests/secret-guard.test.sh ) > $F/full-wslinterop.txt 2>&1; log "F wsl_interop end rc=$?"
git -C $WT show 59e333c:hooks/secret-guard.sh > $F/base-hook.sh; git -C $WT show 59e333c:hooks/tests/secret-guard.test.sh > $F/base-suite.sh
python3 $V31/commentsync.py $WT/hooks/secret-guard.sh $WT/hooks/tests/secret-guard.test.sh target > $F/cs-target.txt 2>&1; log "commentsync target rc=$?"
python3 $V31/commentsync.py $F/base-hook.sh $F/base-suite.sh baseline > $F/cs-baseline.txt 2>&1; log "commentsync baseline rc=$? (base hook $(sha256sum < $F/base-hook.sh | cut -c1-12))"
log done

#!/bin/bash
SP=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad; V=$SP/r217impl/verify3d; WT=$SP/wt217/aria; IMPL=$SP/r217impl/verify3c/impl.sh
V31=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31; B=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/b2
log() { echo "$(date -u +%H:%M:%S) $* | load $(cut -d' ' -f1-3 /proc/loadavg)" >> $V/drive.log; }
waitlow() { local n=0; while :; do read -r l _ < /proc/loadavg; awk -v l="$l" 'BEGIN{exit !(l < 1.2)}' && return 0; n=$((n+1)); [[ $n -ge 90 ]] && { log "waitlow gave up after 30 min"; return 0; }; sleep 20; done; }
echo $$ > $V/drive.pid
log "run-mutants $(sha256sum < $V31/run-mutants.sh | cut -c1-12) run-suite $(sha256sum < $V31/run-suite.sh | cut -c1-12) suite $(sha256sum < $WT/hooks/tests/secret-guard.test.sh | cut -c1-12) impl $(sha256sum < $IMPL | cut -c1-12)"
# V2 copies: two reasons changed in mutants.py; negB also drops V9-E12 from REFIDS
python3 - "$V31" "$V" <<'PY'
import sys, shutil, os
src, v = sys.argv[1], sys.argv[2]
for k in ('negA', 'negB'):
    d = os.path.join(v, k, 'v31')
    if os.path.exists(os.path.join(v, k)): shutil.rmtree(os.path.join(v, k))
    shutil.copytree(src, d)
    p = os.path.join(d, 'mutants.py'); s = open(p, encoding='utf-8').read()
    a = "mut('BI-1', [('V4-S6-spoofed-tail-0', r'\\[rc\\]')]"; b = "mut('BI-8', [('V9-E12-vmax-unchanged', r'\\[bytes\\]')]"
    assert s.count(a) == 1 and s.count(b) == 1
    s = s.replace(a, a.replace('rc', 'bytes')).replace(b, b.replace('bytes', 'status')); open(p, 'w', encoding='utf-8').write(s)
    if k == 'negB':
        p = os.path.join(d, 'run-mutants.sh'); s = open(p, encoding='utf-8').read()
        assert s.count(" V9-E12-vmax-unchanged") == 1
        open(p, 'w', encoding='utf-8').write(s.replace(" V9-E12-vmax-unchanged", ""))
print('copies built')
PY
waitlow
log "V3 env start"; SC_BASH=/nonexistent-v3d/sub/bash SG_W10_ONLY='^V1-E16-p1-small-benign$' bash $V31/run-suite.sh $WT $IMPL $V/w > $V/v3-runsuite.txt 2>&1; log "V3a run-suite exit=$?"
( cd $WT && SC_BASH=/nonexistent-v3d/sub/bash SG_W10_ONLY='^V1-E16-p1-small-benign$' taskset -c 0,1 nice -n 19 bash hooks/tests/secret-guard.test.sh ) > $V/v3-direct.txt 2>&1; log "V3b direct exit=$?"
log "V2 negA start"; MUT_SUITE=$WT MUT_ONLY='BI-1|BI-8' bash $V/negA/v31/run-mutants.sh $IMPL $V/negA/work > $V/v2-negA.txt 2>&1; log "V2 negA exit=$?"
log "V2 negB start"; MUT_SUITE=$WT MUT_ONLY='BI-1|BI-8' bash $V/negB/v31/run-mutants.sh $IMPL $V/negB/work > $V/v2-negB.txt 2>&1; log "V2 negB exit=$?"
waitlow
log "V1 start"; MUT_SUITE=$WT MUT_ONLY='BI-8|BI-13|BI-45|BI-1|BI-24|P-0|P-M29' bash $V31/run-mutants.sh $IMPL $V/pos > $V/v1.txt 2>&1; log "V1 exit=$?"
git -C $WT show 59e333c:hooks/secret-guard.sh > $V/base.sh; s=$(sha256sum < $V/base.sh | cut -c1-12); log "base sha $s"
if [[ $s == e83c5e30f2cc ]]; then waitlow; log "V4 start"; rm -f $V/base.log; SG_W10_ONLY=. SG_W10_LOG=$V/base.log bash $V31/run-suite.sh $WT $V/base.sh $V/w > $V/v4.txt 2>&1; log "V4 exit=$?"
  python3 $V/cmp-base.py $B/t002b-verify/base-5.2.15.txt $V/base.log > $V/v4-cmp.txt 2>&1; else log "V4 skipped: base sha mismatch"; fi
log done

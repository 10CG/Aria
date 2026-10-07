#!/usr/bin/env bash
# run_quiet_measure.sh -- the measurements that want an otherwise idle host (run them one after the other, nothing else in parallel):
#   1. ere_claims.py   grep -oE CPU of the target and bad patterns on one long line        -> out/ere_claims.txt   (W2 linear paragraph)
#   2. occ_cost.py     the per-occurrence stage cut against the baseline, 2 KB and 8 KB     -> out/occ.txt          (W9 matching cost)
#   3. run_gitcopy_suite.sh proto work/t6   the two existing suites on the git copy, final prototype                  -> out/gitcopy_proto*
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v6
cd "$EXP" || exit 1
export HOME=$EXP/home TMPDIR=$EXP/tmp
echo "quiet measure start $(date +%T) load=$(cut -d' ' -f1-3 /proc/loadavg)" >> logs/quiet.log
mkdir -p work/vr
for v in kv_unbounded cli_unbounded cli_noleft; do mkdir -p "work/vr/$v" && python3 proto/patch_l3.py base/aria/hooks/secret-scan.sh "work/vr/$v/secret-scan.sh" --variant "$v" > /dev/null; done
python3 proto/ere_claims.py work/t6/aria/hooks/secret-scan.sh work/vr > out/ere_claims.txt 2>&1
echo "ere_claims done $(date +%T) load=$(cut -d' ' -f1-3 /proc/loadavg)" >> logs/quiet.log
mkdir -p work/tv/ext_v4stage
python3 proto/patch_l1.py base/aria/hooks/secret-guard.sh work/tv/ext_v4stage/secret-guard.sh --variant ext_v4stage > /dev/null
python3 proto/occ_cost.py base/aria/hooks/secret-guard.sh work/t6/aria/hooks/secret-guard.sh work/tv/ext_v4stage/secret-guard.sh --sizes 2000,8000 --pairs 3 --cpu-cap 300 > out/occ.txt 2>&1
echo "occ_cost done $(date +%T) load=$(cut -d' ' -f1-3 /proc/loadavg)" >> logs/quiet.log
bash proto/run_gitcopy_suite.sh proto work/t6 proto
echo "gitcopy proto done $(date +%T) load=$(cut -d' ' -f1-3 /proc/loadavg)" >> logs/quiet.log
echo "QUIET_DONE $(date +%T)" >> logs/quiet.log

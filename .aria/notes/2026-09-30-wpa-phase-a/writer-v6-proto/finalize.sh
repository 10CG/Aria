#!/usr/bin/env bash
# finalize.sh -- after evidence stage 2: refresh the derived outputs, assemble deliver/, self-scan it, compose the report.
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v6
cd "$EXP" || exit 1
export HOME=$EXP/home TMPDIR=$EXP/tmp
set -u
# 1. the target stdout feeds the numbers / family scan; the baseline stdout the baseline counts
cp logs/final_A.out out/probe_baseline.out
cp logs/final_T.out out/probe_target.out
python3 proto/mk_numbers6.py > /dev/null
python3 proto/apply_edits_v6.py spec/proposal.v5.md out/numbers.json work/proposal_final_check.md > /dev/null
cmp work/proposal_final_check.md spec/proposal.md || { echo "PROPOSAL WOULD CHANGE -- stop"; exit 2; }
# 2. checks on the final files
python3 proto/check_counts.py spec/proposal.md logs/final_T.out > out/check_counts.txt 2>&1
python3 proto/xref_check.py spec/proposal.md logs/final_T.out > out/xref_check.txt 2>&1
python3 proto/format_lint.py spec/proposal.md spec/baseline_probe.py spec/baseline-evidence.md > out/format_lint.txt 2>&1
python3 proto/family_scan.py > /dev/null
python3 proto/coverage_check6.py logs/v5base_A.out logs/final_A.out > out/coverage_check.txt 2>&1; echo "coverage_check rc=$?" >> out/coverage_check.txt
python3 proto/build_mut_summary6.py > out/build_mut_summary.txt 2>&1; echo "build_mut_summary rc=$?" >> out/build_mut_summary.txt
python3 proto/mk_timing_summary6.py > /dev/null
python3 proto/refs_check.py > out/refs_check.txt 2>&1; echo "refs_check rc=$?" >> out/refs_check.txt
python3 proto/readface_check.py base/aria/hooks/secret-guard.sh spec/baseline_probe.py > out/readface_check.txt 2>&1; echo "readface_check rc=$?" >> out/readface_check.txt
# 3. deliver/
python3 proto/build_deliver6.py > out/build_deliver.txt 2>&1 || { cat out/build_deliver.txt; exit 3; }
cat out/build_deliver.txt
# 4. Rule #7 self-scan of the delivery (baseline and target secret-scan, Bash and Read faces)
python3 proto/scan_all.py deliver > out/scan_all_deliver.txt 2>&1; tail -2 out/scan_all_deliver.txt
cp out/scan_all_deliver.txt deliver/logs/scan_all_deliver.txt
python3 proto/manifest6.py
echo FINALIZE_DONE

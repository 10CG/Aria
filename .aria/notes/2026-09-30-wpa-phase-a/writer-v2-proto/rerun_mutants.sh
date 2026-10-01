#!/usr/bin/env bash
# rerun the three mutation campaigns with the FINAL probe, keep the first-pass summaries for comparison
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v2
cd "$EXP" || exit 1
mkdir -p final/mut_prev && cp final/mut_summary.txt final/mut_summary2.txt final/mut_summary3.txt final/mut_prev/ 2>/dev/null
rm -f final/rerun_done
final/run_mutants.sh  > final/run_mutants.log 2>&1
final/run_mutants2.sh > final/run_mutants2.log 2>&1
final/run_mutants3.sh > final/run_mutants3.log 2>&1
echo done > final/rerun_done

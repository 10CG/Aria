#!/usr/bin/env bash
# Regression run of the previous round's bad implementations on the v4 prototype: only the rows that were red in v3 are run (plans_v3r/, see work/mk_refined_v3_plans.py).
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v4
cd "$EXP" || exit 1
export HOME=$EXP/home TMPDIR=$EXP/tmp
T=$EXP/work/t4f
log=mut/final/campaign.log
echo "v3 regression start $(date +%T)" >> "$log"
for p in plan_extra plan_extra4 plan_repeat plan_vsym plan_l3_wl plan_l3_w4w5 plan_l3_enum plan_l1_w8w9w10 plan_l1_w11; do
  [ -s "work/plans_v3r/$p.tsv" ] || continue
  mkdir -p "mut/final/v3r_$p"
  python3 proto/mutbatch.py "work/plans_v3r/$p.tsv" --jobs 3 --out "mut/final/v3r_$p" --tree "$T" --spec "$EXP/spec" > "mut/final/v3r_$p.log" 2>&1
  echo "v3r_$p done $(date +%T)" >> "$log"
done
mkdir -p mut/final/v3r_plan_extra2_b32
python3 proto/mutbatch.py work/plans_v3r/plan_extra2_b32.tsv --jobs 2 --b32 --out mut/final/v3r_plan_extra2_b32 --tree "$T" --spec "$EXP/spec" > mut/final/v3r_plan_extra2_b32.log 2>&1
echo "v3r_plan_extra2_b32 done $(date +%T)" >> "$log"
echo "ALL_DONE v3r $(date +%T)" >> "$log"

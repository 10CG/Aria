#!/usr/bin/env bash
# Final mutation campaign: every bad implementation of this round's plans (plans/) and of the earlier round's plans (plans_v3/) is generated from the
# FINAL target prototype tree, run against the FINAL probe, and the rows that turn red are recorded (mut/final/<plan>/SUMMARY.txt).
# usage: run_final_campaign.sh [stage]      stage = v4 | v3 | all (default all)
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v4
cd "$EXP" || exit 1
export HOME=$EXP/home TMPDIR=$EXP/tmp
stage=${1:-all}
T=$EXP/work/t4f
mkdir -p mut/final logs
log=mut/final/campaign.log
run() {   # run <plan file> <jobs> [--b32]
  local f=$1 jobs=$2 b32=${3:-}
  local name
  name=$(basename "$f" .tsv)
  mkdir -p "mut/final/$name"
  python3 proto/mutbatch.py "$f" --jobs "$jobs" $b32 --out "mut/final/$name" --tree "$T" --spec "$EXP/spec" > "mut/final/$name.log" 2>&1
  echo "$name done $(date +%T)" >> "$log"
}
echo "campaign $stage start $(date +%T)" >> "$log"
if [ "$stage" = v4 ] || [ "$stage" = all ]; then
  run work/plans/plan_v4_l3.tsv 3
  run work/plans/plan_v4_l1_w9w10w12.tsv 3
  run work/plans/plan_v4_l1_w11w8.tsv 3
  run work/plans/plan_v4_l1_charsem.tsv 2
  run work/plans/plan_v4_b32.tsv 1 --b32
fi
if [ "$stage" = v3 ] || [ "$stage" = all ]; then
  for p in plan_l3_wl plan_l3_w4w5 plan_l3_enum plan_l1_w8w9w10 plan_l1_w11 plan_extra plan_repeat plan_extra4 plan_vsym; do
    [ -f "work/plans_v3/$p.tsv" ] && run "work/plans_v3/$p.tsv" 3
  done
  for p in plan_extra_b32 plan_extra2_b32; do
    [ -f "work/plans_v3/$p.tsv" ] && run "work/plans_v3/$p.tsv" 2 --b32
  done
fi
echo "ALL_DONE $stage $(date +%T)" >> "$log"

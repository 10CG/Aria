#!/usr/bin/env bash
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v3b
cd "$EXP" || exit 1
for plan in plan_l3_wl plan_l3_w4w5 plan_l3_enum plan_l1_w8w9w10 plan_l1_w11; do
  mkdir -p mut/$plan
  python3 proto/mutbatch.py work/plans/$plan.tsv --jobs 3 --out mut/$plan > mut/$plan.log 2>&1
  echo "$plan done $(date +%T)" >> mut/campaign.log
done
echo ALL_DONE >> mut/campaign.log

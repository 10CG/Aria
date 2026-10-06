#!/usr/bin/env bash
# waits for plan_extra2_b32, then runs plan_vsym (the 13 value-class symbol variants; the first pass and the repeat pass had colliding work-directory names for 9 of them)
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v3b
cd "$EXP" || exit 1
until /usr/bin/grep -q "plan_extra2_b32 done" mut/campaign.log 2>/dev/null; do sleep 15; done
mkdir -p mut/plan_vsym
python3 proto/mutbatch.py work/plans/plan_vsym.tsv --jobs 3 --out mut/plan_vsym > mut/plan_vsym.log 2>&1
echo "plan_vsym done $(date +%T)" >> mut/campaign.log

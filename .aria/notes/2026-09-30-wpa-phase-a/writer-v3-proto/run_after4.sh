#!/usr/bin/env bash
# waits for plan_repeat, then runs plan_extra2 (PEM variants against 12m) and plan_extra2_b32 (real bash 3.2 differential: 32c needs SC rows with hook-direct runs in the same process)
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v3b
cd "$EXP" || exit 1
until /usr/bin/grep -q "plan_repeat done" mut/campaign.log 2>/dev/null; do sleep 15; done
mkdir -p mut/plan_extra2 mut/plan_extra2_b32
python3 proto/mutbatch.py work/plans/plan_extra2.tsv --jobs 3 --out mut/plan_extra2 > mut/plan_extra2.log 2>&1
echo "plan_extra2 done $(date +%T)" >> mut/campaign.log
python3 proto/mutbatch.py work/plans/plan_extra2_b32.tsv --jobs 2 --b32 --out mut/plan_extra2_b32 > mut/plan_extra2_b32.log 2>&1
echo "plan_extra2_b32 done $(date +%T)" >> mut/campaign.log

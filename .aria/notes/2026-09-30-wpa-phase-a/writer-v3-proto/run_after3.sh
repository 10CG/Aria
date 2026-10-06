#!/usr/bin/env bash
# waits for plan_extra_b32, then repeats the classifier-type L3 bad implementations once more (determinism check: same red rows as the first pass)
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v3b
cd "$EXP" || exit 1
until /usr/bin/grep -q "plan_extra_b32 done" mut/campaign.log 2>/dev/null; do sleep 20; done
mkdir -p mut/plan_repeat
python3 proto/mutbatch.py work/plans/plan_repeat.tsv --jobs 3 --out mut/plan_repeat > mut/plan_repeat.log 2>&1
echo "plan_repeat done $(date +%T)" >> mut/campaign.log

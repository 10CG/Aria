#!/usr/bin/env bash
# waits for the campaign, then runs the extra plan
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v3b
cd "$EXP" || exit 1
until /usr/bin/grep -q ALL_DONE mut/campaign.log 2>/dev/null; do sleep 20; done
mkdir -p mut/plan_extra
python3 proto/mutbatch.py work/plans/plan_extra.tsv --jobs 3 --out mut/plan_extra > mut/plan_extra.log 2>&1
echo "plan_extra done $(date +%T)" >> mut/campaign.log

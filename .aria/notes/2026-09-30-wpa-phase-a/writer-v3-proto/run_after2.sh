#!/usr/bin/env bash
# waits for plan_extra, then runs the two bash-3.2 mutants (32a static + 32c real-3.2 differential)
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v3b
cd "$EXP" || exit 1
until /usr/bin/grep -q "plan_extra done" mut/campaign.log 2>/dev/null; do sleep 20; done
mkdir -p mut/plan_extra_b32
python3 proto/mutbatch.py work/plans/plan_extra_b32.tsv --jobs 2 --b32 --out mut/plan_extra_b32 > mut/plan_extra_b32.log 2>&1
echo "plan_extra_b32 done $(date +%T)" >> mut/campaign.log

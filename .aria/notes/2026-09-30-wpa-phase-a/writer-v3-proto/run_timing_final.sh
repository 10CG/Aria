#!/usr/bin/env bash
# waits for a quiet host (1-minute load < 1.5, up to 15 minutes), then runs the timing tiers on the good hooks and the bad-implementation tiers
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v3b
cd "$EXP" || exit 1
for i in $(seq 1 90); do
  l=$(cut -d' ' -f1 /proc/loadavg)
  if awk "BEGIN{exit !($l < 1.5)}"; then break; fi
  sleep 10
done
echo "quiet-wait ended: load $(cut -d' ' -f1-3 /proc/loadavg) at $(date +%T)" > logs/timing_final.status
work/run_timing.sh final_good good 5
work/run_timing_variants.sh final_var 3
echo "timing done $(date +%T) load $(cut -d' ' -f1-3 /proc/loadavg)" >> logs/timing_final.status

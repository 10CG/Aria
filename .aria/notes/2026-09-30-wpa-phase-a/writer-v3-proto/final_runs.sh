#!/usr/bin/env bash
# Final evidence runs.  usage: final_runs.sh stage1|stage2
#   stage1: baseline WITH b32 (final_A) and WITHOUT b32 (final_N) concurrently, on the final proposal + probe (evidence file = whatever is in spec/ now)
#   stage2: (after mk_evidence has put the final baseline-evidence.md into spec/) baseline WITH b32 again (final_B), target WITH b32 (final_T), target WITHOUT b32 (final_TN)
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v3b
cd "$EXP" || exit 1
stage=$1
if [ "$stage" = stage1 ]; then
  proto/runprobe.sh final_A "$EXP/base" "$EXP/spec" 1 &
  proto/runprobe.sh final_N "$EXP/base" "$EXP/spec" 0 &
  wait
  echo "stage1 done $(date +%T)" >> logs/final.log
elif [ "$stage" = stage2 ]; then
  proto/runprobe.sh final_B "$EXP/base" "$EXP/spec" 1 &
  WPA_REQUIRE_ALL_PASS=1 proto/runprobe.sh final_T "$EXP/work/t3" "$EXP/spec" 1 &
  proto/runprobe.sh final_TN "$EXP/work/t3" "$EXP/spec" 0 &
  wait
  echo "stage2 done $(date +%T)" >> logs/final.log
fi

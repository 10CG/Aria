#!/usr/bin/env bash
# Final evidence runs.  usage: final_runs.sh stage1|stage2
#   stage1: three BASELINE runs concurrently on the final proposal + probe:  final_A (WPA_BASH32), final_B (WPA_BASH32, the reproducibility twin), final_N (no WPA_BASH32)
#           (the evidence file in spec/ at that moment is only scanned by row 15g; none of the three outputs embeds anything of it)
#   stage2: (after proto/mk_evidence.py has put the final baseline-evidence.md into spec/)  final_T (target tree, WPA_BASH32 + WPA_REQUIRE_ALL=1),
#           final_TN (target tree, no WPA_BASH32), final_C (baseline, WPA_BASH32, with the FINAL evidence in place: must be byte-equal to final_A)
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v5
cd "$EXP" || exit 1
stage=$1
mkdir -p logs
echo "$stage start $(date +%T)" >> logs/final.log
if [ "$stage" = stage1 ]; then
  proto/runprobe.sh final_A "$EXP/base" "$EXP/spec" 1 &
  proto/runprobe.sh final_B "$EXP/base" "$EXP/spec" 1 &
  proto/runprobe.sh final_N "$EXP/base" "$EXP/spec" 0 &
  wait
  echo "stage1 done $(date +%T)" >> logs/final.log
elif [ "$stage" = stage2 ]; then
  WPA_REQUIRE_ALL_PASS=1 proto/runprobe.sh final_T "$EXP/work/t5f" "$EXP/spec" 1 &
  proto/runprobe.sh final_TN "$EXP/work/t5f" "$EXP/spec" 0 &
  proto/runprobe.sh final_C "$EXP/base" "$EXP/spec" 1 &
  wait
  echo "stage2 done $(date +%T)" >> logs/final.log
fi

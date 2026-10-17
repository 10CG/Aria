#!/usr/bin/env bash
# run_timing_good6.sh -- the W14 time tiers on the FINAL target prototype (work/t6), judged (pure ratios), on a quiet host.
#   out/timing_t6_main.txt   all tiers, 5 interleaved pairs (f / f0 are repeated with 15 pairs below because their millisecond minima move with the host)
#   out/timing_t6_f15.txt    tiers f / f0, 15 pairs
# usage: run_timing_good6.sh [tree]      (tree default: work/t6)
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v6
cd "$EXP" || exit 1
export HOME=$EXP/home TMPDIR=$EXP/tmp
TREE=${1:-$EXP/work/t6}
mkdir -p out
{
  echo "== good-prototype timing main: tree=$TREE load(start)=$(cut -d' ' -f1-3 /proc/loadavg) $(date +%T)"
  python3 proto/timing.py "$EXP/base/aria/hooks" "$TREE/aria/hooks" f,f0,g,gmax,h,i,w1,fhit,i3 --pairs 5 --judge
  echo "rc=$?"
  echo "== done load(end)=$(cut -d' ' -f1-3 /proc/loadavg) $(date +%T)"
} > out/timing_t6_main.txt 2>&1
{
  echo "== good-prototype timing f/f0 15 pairs: tree=$TREE load(start)=$(cut -d' ' -f1-3 /proc/loadavg) $(date +%T)"
  python3 proto/timing.py "$EXP/base/aria/hooks" "$TREE/aria/hooks" f,f0 --pairs 15 --judge
  echo "rc=$?"
  echo "== done load(end)=$(cut -d' ' -f1-3 /proc/loadavg) $(date +%T)"
} > out/timing_t6_f15.txt 2>&1
echo "TIMING_GOOD_DONE $(date +%T)" >> logs/timing.log

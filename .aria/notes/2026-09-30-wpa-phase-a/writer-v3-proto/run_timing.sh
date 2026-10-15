#!/usr/bin/env bash
# run_timing.sh LABEL VARIANT [pairs]  -- interleaved A/B timing of the baseline hooks vs work/tv/VARIANT on every W14 tier
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v3b
label=$1; variant=$2; pairs=${3:-5}
out="$EXP/logs/timing_$label.log"
cd "$EXP" || exit 1
{
  echo "== $label ($variant) pairs=$pairs load=$(cut -d' ' -f1-3 /proc/loadavg) $(date +%T)"
  python3 proto/timing.py "$EXP/base/aria/hooks" "$EXP/work/tv/$variant" f,f0,i --pairs "$pairs"
  python3 proto/timing.py "$EXP/base/aria/hooks" "$EXP/work/tv/$variant" g --pairs "$pairs" --gsize 4000 --nvars 8 --vlen 300 --nrefs 40
  python3 proto/timing.py "$EXP/base/aria/hooks" "$EXP/work/tv/$variant" g --pairs "$pairs" --gsize 4000 --nvars 16 --vlen 100 --nrefs 128
  python3 proto/timing.py "$EXP/base/aria/hooks" "$EXP/work/tv/$variant" h --pairs "$pairs"
  python3 proto/timing.py "$EXP/base/aria/hooks" "$EXP/work/tv/$variant" w1 --pairs "$pairs"
  echo "== done $(date +%T) load=$(cut -d' ' -f1-3 /proc/loadavg)"
} > "$out" 2>&1

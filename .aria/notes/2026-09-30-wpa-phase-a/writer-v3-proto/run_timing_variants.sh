#!/usr/bin/env bash
# run_timing_variants.sh LABEL [pairs] -- the bad implementations of the W14 time tiers, each on the tier that is meant to catch it
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v3b
label=$1; pairs=${2:-3}
cd "$EXP" || exit 1
T="python3 proto/timing.py $EXP/base/aria/hooks"
{
  echo "== variants $label pairs=$pairs load=$(cut -d' ' -f1-3 /proc/loadavg) $(date +%T)"
  echo "-- vx_quadratic (remainder after a hit taken with \${s#*\"\$pat\"}) on g"
  $T "$EXP/work/tv/vx_quadratic" g --pairs "$pairs" --gsize 4000 --nvars 8 --vlen 300 --nrefs 40
  $T "$EXP/work/tv/vx_quadratic" g --pairs "$pairs" --gsize 4000 --nvars 16 --vlen 100 --nrefs 128
  echo "-- ext_perentry (one grep process per extension entry) on f"
  $T "$EXP/work/tv/ext_perentry" f --pairs "$pairs"
  echo "-- no_cap (every span iterated) on i"
  $T "$EXP/work/tv/no_cap" i --pairs "$pairs"
  echo "-- vx_interleave (substituted copy judged right after each segment) on h"
  $T "$EXP/work/tv/vx_interleave" h --pairs "$pairs"
  echo "-- ext_first (extension before the built-ins) on f / h"
  $T "$EXP/work/tv/ext_first" f,h --pairs "$pairs"
  echo "== done $(date +%T) load=$(cut -d' ' -f1-3 /proc/loadavg)"
} > "$EXP/logs/timing_$label.log" 2>&1

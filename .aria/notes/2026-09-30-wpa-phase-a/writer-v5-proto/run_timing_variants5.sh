#!/usr/bin/env bash
# run_timing_variants5.sh [pairs] [slow_pairs] -- the bad implementations of the W14 time tiers, each on the tier that is meant to catch it (output on stdout).
# Every bad implementation is the FINAL target prototype hooks with ONE hook replaced by patch_l1.py / patch_l3.py --variant NAME; the other hook stays the target's.
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v5
pairs=${1:-3}
slow=${2:-1}
cd "$EXP" || exit 1
export HOME=$EXP/home TMPDIR=$EXP/tmp
TREE=${TREE:-$EXP/work/t5}
mk() {   # mk <dir name> <l1|l3> <variant>
  local d="$EXP/work/tv/$1"
  rm -rf "$d" && mkdir -p "$d" && cp -a "$TREE/aria/hooks/." "$d/"
  if [ "$2" = l1 ]; then python3 "$EXP/proto/patch_l1.py" "$EXP/base/aria/hooks/secret-guard.sh" "$d/secret-guard.sh" --variant "$3" >/dev/null || return 1
  else python3 "$EXP/proto/patch_l3.py" "$EXP/base/aria/hooks/secret-scan.sh" "$d/secret-scan.sh" --variant "$3" >/dev/null || return 1; fi
}
run() {   # run <dir name> <tiers> <pairs>
  python3 "$EXP/proto/timing.py" "$EXP/base/aria/hooks" "$EXP/work/tv/$1" "$2" --pairs "$3"
}
echo "== variants pairs=$pairs slow=$slow load=$(cut -d' ' -f1-3 /proc/loadavg) $(date +%T)"
echo "-- vx_quadratic (remainder after a hit taken with \${s#*\"\$pat\"}) on g / gmax"; mk vx_quadratic l1 vx_quadratic && run vx_quadratic g,gmax "$pairs"
echo "-- ext_perentry (one grep process per extension entry) on f"; mk ext_perentry l1 ext_perentry && run ext_perentry f "$pairs"
echo "-- no_cap (every span iterated) on i"; mk no_cap l3 no_cap && run no_cap i "$pairs"
echo "-- vx_interleave (substituted copy judged right after each segment) on h"; mk vx_interleave l1 vx_interleave && run vx_interleave h "$pairs"
echo "-- ext_first (extension before the built-ins) on f / h"; mk ext_first l1 ext_first && run ext_first f,h "$pairs"
echo "-- ext_v4stage (hand-written quote mask + stage cut per occurrence) on fhit"; mk ext_v4stage l1 ext_v4stage && run ext_v4stage fhit "$slow"
echo "-- ext_perocc_judge (one built-in judgement per occurrence) on fhit"; mk ext_perocc_judge l1 ext_perocc_judge && run ext_perocc_judge fhit "$slow"
echo "-- val_quadratic (value extraction with the prefix-removal idiom) on i3 / i"; mk val_quadratic l3 val_quadratic && run val_quadratic i3,i "$slow"
echo "-- cli_unbounded / kv_unbounded / cli_v4 / cli_noleft (patterns with unbounded name affixes or no left boundary) on i3"
for v in cli_unbounded kv_unbounded cli_v4 cli_noleft; do echo "   [$v]"; mk "$v" l3 "$v" && run "$v" i3 "$slow"; done
echo "== done $(date +%T) load=$(cut -d' ' -f1-3 /proc/loadavg)"

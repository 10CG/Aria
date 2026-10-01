#!/usr/bin/env bash
# Mutation campaign with the FINAL probe: every mutant = the full target prototype (final/full) with ONE hook replaced by a
# 'bad implementation' variant; the probe rows that are not 'yes' are the rows that catch it.
# usage: run_mutants.sh            (writes final/mut/<name>.out and final/mut_summary.txt)
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v2
cd "$EXP" || exit 1
mkdir -p final/mut
L3_SCS=SC-1,SC-2,SC-3,SC-4,SC-5,SC-6,SC-7,SC-8,SC-9,SC-10,SC-11,SC-12,SC-13,SC-15
L1_SCS=SC-16,SC-17,SC-18,SC-19,SC-20,SC-21,SC-22,SC-23,SC-24,SC-25
: > final/mut_summary.txt
run_one() {   # name kind variant sclist
  local name=$1 kind=$2 variant=$3 scs=$4
  rm -rf "final/mut/$name" && mkdir -p "final/mut/$name"
  cp -a final/full/aria "final/mut/$name/aria" && cp -a final/full/standards "final/mut/$name/standards"
  if [ "$kind" = l3 ]; then
    python3 proto/patch_l3.py aria/hooks/secret-scan.sh "final/mut/$name/aria/hooks/secret-scan.sh" --variant "$variant" > /dev/null
  else
    python3 proto/patch_l1.py aria/hooks/secret-guard.sh "final/mut/$name/aria/hooks/secret-guard.sh" --variant "$variant" > /dev/null
  fi
  final/runprobe.sh "mut_$name" "$EXP/final/mut/$name" "$EXP/final/spec" 0 "$scs"
  mv "final/mut_$name.out" "final/mut/$name.out"; mv "final/mut_$name.rc" "final/mut/$name.rc"; rm -f "final/mut_$name.err"
  {
    echo "== $name ($kind variant $variant; WPA_ONLY=$scs)"
    grep -E '│ no$' "final/mut/$name.out" | awk -F' │ ' '{print "   " $1 " " $2 " | " $3 " | actual: " substr($6,1,110)}'
    echo "   (rows not yes: $(grep -cE '│ no$' "final/mut/$name.out"))"
  } >> final/mut_summary.txt
}
for v in noident nopath loosepath wl_prefix wl_contains wl_nocase ent_digit ent_on_old wl_envline w5_append; do
  run_one "$v" l3 "$v" "$L3_SCS"
done
for v in noentropy noident nopath; do
  run_one "census_$v" l3 "$v" SC-33
done
for v in ext_bare ext_first vx_interleave env_boundary proc_status ext_regex ext_trunc notight jq_loose; do
  run_one "$v" l1 "$v" "$L1_SCS"
done
echo DONE >> final/mut_summary.txt

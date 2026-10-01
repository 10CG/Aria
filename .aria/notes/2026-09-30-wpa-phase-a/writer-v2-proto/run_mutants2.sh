#!/usr/bin/env bash
# second mutation campaign (variants added or repaired after the first one); same harness as run_mutants.sh
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v2
cd "$EXP" || exit 1
mkdir -p final/mut
L3_SCS=SC-1,SC-2,SC-3,SC-4,SC-5,SC-6,SC-7,SC-8,SC-9,SC-10,SC-11,SC-12,SC-13,SC-15
L1_SCS=SC-16,SC-17,SC-18,SC-19,SC-20,SC-21,SC-22,SC-23,SC-24,SC-25
: > final/mut_summary2.txt
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
    echo "   (rows not yet 'yes': $(grep -cE '│ no$' "final/mut/$name.out"))"
  } >> final/mut_summary2.txt
}
run_one path_firstlower l3 path_firstlower "$L3_SCS"
run_one fp_span l3 fp_span "$L3_SCS"
run_one ext_regex l1 ext_regex "$L1_SCS"
run_one vx_interleave l1 vx_interleave "$L1_SCS"
echo DONE >> final/mut_summary2.txt

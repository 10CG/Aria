#!/usr/bin/env bash
# third campaign: the bash-3.2 differential (needs WPA_BASH32), and the doc-sync token-stuffing mutant
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v2
cd "$EXP" || exit 1
: > final/mut_summary3.txt
run_one() {   # name variant sclist b32
  local name=$1 variant=$2 scs=$3 b32=$4
  rm -rf "final/mut/$name" && mkdir -p "final/mut/$name"
  cp -a final/full/aria "final/mut/$name/aria" && cp -a final/full/standards "final/mut/$name/standards"
  python3 proto/patch_l1.py aria/hooks/secret-guard.sh "final/mut/$name/aria/hooks/secret-guard.sh" --variant "$variant" > /dev/null
  final/runprobe.sh "mut_$name" "$EXP/final/mut/$name" "$EXP/final/spec" "$b32" "$scs"
  mv "final/mut_$name.out" "final/mut/$name.out"; mv "final/mut_$name.rc" "final/mut/$name.rc"; rm -f "final/mut_$name.err"
  {
    echo "== $name (l1 variant $variant; WPA_ONLY=$scs; bash3.2 leg=$b32)"
    grep -E '│ no$' "final/mut/$name.out" | awk -F' │ ' '{print "   " $1 " " $2 " | " $3 " | actual: " substr($6,1,150)}'
    echo "   (rows not yet 'yes': $(grep -cE '│ no$' "final/mut/$name.out"))"
  } >> final/mut_summary3.txt
}
run_one b4 b4 SC-21,SC-32 1
run_one vx_patsub vx_patsub SC-21,SC-32 1
# doc-sync token stuffing: full target docs, but the SOT facts only appended as one line to the version history
name=docs_bad2
rm -rf "final/mut/$name" && mkdir -p "final/mut/$name"
cp -a final/full/aria "final/mut/$name/aria" && cp -a final/full/standards "final/mut/$name/standards"
cp standards/conventions/secret-hygiene.md "final/mut/$name/standards/conventions/secret-hygiene.md"
python3 proto/patch_docs.py "final/mut/$name" --bad > /dev/null
final/runprobe.sh "mut_$name" "$EXP/final/mut/$name" "$EXP/final/spec" 0 SC-26,SC-28
mv "final/mut_$name.out" "final/mut/$name.out"; mv "final/mut_$name.rc" "final/mut/$name.rc"; rm -f "final/mut_$name.err"
{
  echo "== $name (docs: SOT = baseline + one stuffed line in the version history; WPA_ONLY=SC-26,SC-28)"
  grep -E '│ no$' "final/mut/$name.out" | awk -F' │ ' '{print "   " $1 " " $2 " | " $3 " | actual: " substr($6,1,100)}'
  echo "   (rows not yet 'yes': $(grep -cE '│ no$' "final/mut/$name.out"))"
} >> final/mut_summary3.txt
echo DONE >> final/mut_summary3.txt

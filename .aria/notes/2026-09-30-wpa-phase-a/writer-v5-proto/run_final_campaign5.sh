#!/usr/bin/env bash
# Final mutation campaign of this round, run on the FINAL prototype tree (work/t5f) with the FINAL probe (spec/):
#   stage v5   this round's bad implementations (work/plans5/*.tsv)
#   stage v4   the previous round's bad implementations (work/plans/plan_v4_*.tsv; the 7 whose design no longer exists are removed and listed as superseded in the summary)
#   stage v3   the rounds before (work/plans_v3/*.tsv, refined to the rows that were red then)
#   stage doc  document variants (patch_docs.py flags) on SC-26 / SC-27 / SC-28
# usage: run_final_campaign5.sh [stage ...]      (default: all)       results: mut/final5/<plan>/SUMMARY.txt, mut/final5/campaign.log
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v5
cd "$EXP" || exit 1
export HOME=$EXP/home TMPDIR=$EXP/tmp
T=$EXP/work/t5f
mkdir -p mut/final5 logs
log=mut/final5/campaign.log
stages=${*:-v5 v4 v3 doc}
run() {   # run <plan file> <jobs> [--b32]
  local f=$1 jobs=$2 b32=${3:-} name
  name=$(basename "$f" .tsv)
  [ -n "$PREFIX" ] && name="${PREFIX}_$name"
  mkdir -p "mut/final5/$name"
  python3 proto/mutbatch.py "$f" --jobs "$jobs" $b32 --out "mut/final5/$name" --tree "$T" --spec "$EXP/spec" > "mut/final5/$name.log" 2>&1
  echo "$name done $(date +%T)" >> "$log"
}
echo "campaign [$stages] start $(date +%T) load=$(cut -d' ' -f1-3 /proc/loadavg)" >> "$log"
for s in $stages; do
  case $s in
    v5)
      PREFIX=""; run work/plans5/plan_v5_l3.tsv 3; run work/plans5/plan_v5_l1.tsv 3; run work/plans5/plan_v5_l1b.tsv 2; run work/plans5/plan_v5_l1c.tsv 3; run work/plans5/plan_v5_b32.tsv 1 --b32 ;;
    v4)
      PREFIX=""
      for p in plan_v4_l3 plan_v4_l1_w9w10w12 plan_v4_l1_w11w8 plan_v4_l1_charsem plan_v4_l1_w12 plan_v4_l1_evals plan_v4_l1_redo; do [ -f "work/plans/$p.tsv" ] && run "work/plans/$p.tsv" 3; done
      [ -f work/plans/plan_v4_b32.tsv ] && run work/plans/plan_v4_b32.tsv 1 --b32 ;;
    v3)
      PREFIX=v3r
      for p in plan_l3_wl plan_l3_w4w5 plan_l3_enum plan_l1_w8w9w10 plan_l1_w11 plan_extra plan_repeat plan_extra4 plan_vsym; do [ -f "work/plans_v3/$p.tsv" ] && run "work/plans_v3/$p.tsv" 3; done
      for p in plan_extra_b32 plan_extra2_b32; do [ -s "work/plans_v3/$p.tsv" ] && run "work/plans_v3/$p.tsv" 2 --b32; done ;;
    doc)
      bash proto/run_docvariants5.sh ;;
  esac
done
echo "ALL_DONE [$stages] $(date +%T)" >> "$log"

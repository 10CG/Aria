#!/usr/bin/env bash
# Final mutation campaign of this round, run on the FINAL prototype tree (work/t6) with the FINAL probe (spec/):
#   stage v6   this round's bad implementations (work/plans6/*.tsv: L3, L1, hooks.json)
#   stage doc  document variants (patch_docs.py flags) on SC-26 / SC-27 / SC-28 (docvariants6.py)
#   stage v5   the previous round's bad implementations (work/plans_v5/*.tsv), re-run as a regression
#   stage v4   the round before (work/plans_v4/*.tsv)
#   stage v3   the rounds before that (work/plans_v3/*.tsv, refined to the rows that were red then)
# usage: run_final_campaign6.sh [jobs] [stage ...]      (default: 3 jobs, all stages)       results: mut/final6/<plan>/SUMMARY.txt, mut/final6/campaign.log
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v6
cd "$EXP" || exit 1
export HOME=$EXP/home TMPDIR=$EXP/tmp
T=$EXP/work/t6
mkdir -p mut/final6 logs
log=mut/final6/campaign.log
J=${1:-3}; shift
stages=${*:-v6 doc v5 v4 v3}
run() {   # run <plan file> <jobs> [--b32]
  local f=$1 jobs=$2 b32=${3:-} name
  name=$(basename "$f" .tsv)
  [ -n "$PREFIX" ] && name="${PREFIX}_$name"
  mkdir -p "mut/final6/$name"
  python3 proto/mutbatch.py "$f" --jobs "$jobs" $b32 --out "mut/final6/$name" --tree "$T" --spec "$EXP/spec" > "mut/final6/$name.log" 2>&1
  echo "$name done $(date +%T)" >> "$log"
}
echo "campaign [$stages] jobs=$J start $(date +%T) load=$(cut -d' ' -f1-3 /proc/loadavg)" >> "$log"
for s in $stages; do
  case $s in
    v6)
      PREFIX=""; run work/plans6/plan_v6_l3.tsv "$J"; run work/plans6/plan_v6_hj.tsv "$J"; run work/plans6/plan_v6_l1.tsv "$J" ;;
    doc)
      python3 proto/docvariants6.py --jobs "$J" > mut/final6/doc.log 2>&1
      echo "doc done $(date +%T)" >> "$log" ;;
    v5)
      PREFIX=""
      for p in plan_v5_l3 plan_v5_l1 plan_v5_l1b plan_v5_l1c; do [ -f "work/plans_v5/$p.tsv" ] && run "work/plans_v5/$p.tsv" "$J"; done
      [ -f work/plans_v5/plan_v5_b32.tsv ] && run work/plans_v5/plan_v5_b32.tsv 1 --b32 ;;
    v4)
      PREFIX=""
      for p in plan_v4_l3 plan_v4_l1_w9w10w12 plan_v4_l1_w11w8 plan_v4_l1_charsem plan_v4_l1_w12 plan_v4_l1_evals plan_v4_l1_redo; do [ -f "work/plans_v4/$p.tsv" ] && run "work/plans_v4/$p.tsv" "$J"; done
      [ -f work/plans_v4/plan_v4_b32.tsv ] && run work/plans_v4/plan_v4_b32.tsv 1 --b32 ;;
    v3)
      PREFIX=v3r
      for p in plan_l3_wl plan_l3_w4w5 plan_l3_enum plan_l1_w8w9w10 plan_l1_w11 plan_extra plan_repeat plan_extra4 plan_vsym; do [ -f "work/plans_v3/$p.tsv" ] && run "work/plans_v3/$p.tsv" "$J"; done
      for p in plan_extra_b32 plan_extra2_b32; do [ -s "work/plans_v3/$p.tsv" ] && run "work/plans_v3/$p.tsv" 2 --b32; done ;;
  esac
done
echo "ALL_DONE [$stages] $(date +%T)" >> "$log"

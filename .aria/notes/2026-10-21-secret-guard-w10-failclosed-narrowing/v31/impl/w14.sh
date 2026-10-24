#!/usr/bin/env bash
# w14.sh : TASK-003 first stage of 10CG/aria-plugin#217 -- the independent mutants (QA seat, not the author of the implementation or of its tests).
# Defensive context: mutation testing of a leak-prevention hook. Every mutant is the implementation plus ONE authoring mistake (w14-mutants.py: verbatim
# replacements, each asserted to match exactly once); the mutants live only in the scratch directory DIR, are only run through the regression suite
# (v31/run-suite.sh, which puts the mutant into a copy of aria's hooks/ and runs hooks/tests/secret-guard.test.sh there), and are never installed.
#
# What it does: generates the mutants from the implementation, and for each Q-n runs the suite on the cases written down BEFORE the run (predict.md: cases and
# reason tags per mutant; SG_W10_ONLY='^(id|id)$'), then classifies:
#   caught as predicted  a predicted case is FAIL and its detail carries one of the predicted reason tags
#   caught elsewhere     only other cases (or the predicted case with another tag) are FAIL -- counts as a gap (an unrelated assertion hitting red is no catch)
#   not caught           nothing is FAIL (after a SG_W10_ONLY=. round when FULL=1)
#   not judged           a predicted timing case was SKIP [load]/[void]/[inconclusive]: run again under a low load
#   caught by the added case   (GAPMAP) the case added for the gap (V14-...) is FAIL on the mutant
# Environment: W14_IDS="Q-1 Q-2" (default all) | W14_FULL=0 skips the SG_W10_ONLY=. round | W14_TAG=<prefix of the log files> | W14_SC_BASH=<bash that runs the
# cases> | W14_ARIA (aria checkout) | W14_DIR (scratch: mut/ logs/ tmp/, predict.md) | W14_PREDICT | W14_GAPMAP (Q-n <TAB> case id <TAB> [tag]) | W14_OUT.
# Load rule (INV-7): before every run it waits (at most 10 min) for a one-minute load <= 1.2; the suite itself judges the timing cases only when the load at
# the start is below 2 and turns them into SKIP [void] when it is 2 or more at the end. Everything runs under taskset -c 0,1 nice -n 19, one run at a time.
# Output: OUT (default W14-independent-mutants.txt next to this script): line 1 = date, load, sha256 prefixes (INV-8); then one line per mutant.
set -u
HERE=$(cd "$(dirname "$0")" && pwd); V31=$(dirname "$HERE")
SCR=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad
ARIA=${W14_ARIA:-$SCR/wt217/aria}
DIR=${W14_DIR:-$SCR/r217impl/t003a}
PRED=${W14_PREDICT:-$DIR/predict.md}
GAPMAP=${W14_GAPMAP:-$DIR/gapmap.tsv}
OUT=${W14_OUT:-$HERE/W14-independent-mutants.txt}
IDS=${W14_IDS:-}; FULL=${W14_FULL:-1}; TAG=${W14_TAG:-run}
[[ -n "${W14_SC_BASH:-}" ]] && export SC_BASH="$W14_SC_BASH"
IMPL=$ARIA/hooks/secret-guard.sh; M=$DIR/mut; L=$DIR/logs
mkdir -p "$M" "$L" "$DIR/tmp" || exit 3

sha12() { sha256sum < "$1" | cut -c1-12; }
load3() { cut -d' ' -f1-3 /proc/loadavg; }
wait_load() { local i; for ((i = 0; i < 120; i++)); do awk '{exit !($1 <= 1.2)}' /proc/loadavg && return 0; sleep 5; done; return 0; }
run_round() {   # HOOK ONLY LOG OUT : one suite run on the hook, filtered by the regex ONLY
  wait_load
  SG_W10_ONLY="$2" SG_W10_LOG="$3" taskset -c 0,1 nice -n 19 timeout -k 10 1500 bash "$V31/run-suite.sh" "$ARIA" "$1" "$DIR/tmp" > "$4" 2>&1
  return $?
}
pred_row() { awk -F'|' -v q="$1" '{a=$2; gsub(/^ +| +$/, "", a); if (a == q) { c=$3; t=$4; gsub(/^ +| +$/, "", c); gsub(/^ +| +$/, "", t); print c "\t" t; exit } }' "$PRED"; }
status_of() { awk -v id="$2" '$2 == id { print $1; exit }' "$1"; }                      # LOG ID -> PASS|FAIL|SKIP (empty: not reported)
detail_of() { awk -v id="$2" '$2 == id { print; exit }' "$1"; }
tags_in() { grep -o '\[[a-z<>]*\]' <<< "$1" | sort -u | tr '\n' ' '; }
mkre() { tr ' ' '\n' <<< "$1" | grep -v '^$' | paste -sd'|' -; }

[[ "$(git -C "$ARIA" show 59e333c:hooks/secret-guard.sh | sha256sum | cut -c1-12)" == e83c5e30f2cc ]] || { echo "w14.sh: the baseline is not e83c5e30f2cc (INV-9)" >&2; exit 3; }
python3 -I "$HERE/w14-mutants.py" "$IMPL" "$M" > "$DIR/gen.out" || { echo "w14.sh: w14-mutants.py failed" >&2; exit 3; }
{
  printf '# W14 independent mutants (TASK-003 first stage, 10CG/aria-plugin#217) | %s | load %s | base e83c5e30f2cc | impl %s | suite %s | helper %s | sc-cases.sh %s | sc-direct.sh %s | mutants.py %s | w14-mutants.py %s | SC_BASH %s | predict.md %s\n' \
    "$(date -u +%FT%TZ)" "$(load3)" "$(sha12 "$IMPL")" "$(sha12 "$ARIA/hooks/tests/secret-guard.test.sh")" "$(sha12 "$ARIA/hooks/tests/lib/secret-guard-w10-direct.sh")" \
    "$(sha12 "$V31/sc-cases.sh")" "$(sha12 "$V31/sc-direct.sh")" "$(sha12 "$V31/mutants.py")" "$(sha12 "$HERE/w14-mutants.py")" "${SC_BASH:-bash on PATH}" "$(sha12 "$PRED")"
  printf '# columns: id | change | predicted (cases ; tags) | actual (case=STATUS tags-in-detail) | load of the run | verdict. Logs: %s/%s-*.log\n' "$L" "$TAG"
} > "$OUT"

n_pred=0; n_else=0; n_none=0; n_unj=0; n_added=0
for q in ${IDS:-$(cut -f1 "$DIR/gen.out")}; do
  title=$(awk -F'\t' -v q="$q" '$1 == q { print $3 }' "$DIR/gen.out")
  IFS=$'\t' read -r cases tags < <(pred_row "$q"); cases=${cases:-}; tags=${tags:-}
  sel=$cases; [[ $sel == "-" ]] && sel=''
  added=$(awk -F'\t' -v q="$q" '$1 == q { printf "%s ", $2 }' "$GAPMAP" 2>/dev/null); addtag=$(awk -F'\t' -v q="$q" '$1 == q { printf "%s ", $3 }' "$GAPMAP" 2>/dev/null)
  re=$(mkre "$sel $added"); sub=$L/$TAG-$q.sub.log; sout=$L/$TAG-$q.sub.out; full=$L/$TAG-$q.full.log; fout=$L/$TAG-$q.full.out
  actual=''; verdict=''; ldesc=''
  if [[ -n $re ]]; then
    run_round "$M/$q.sh" "^($re)\$" "$sub" "$sout"
    ldesc=$(grep -o 'load start.*' "$sout" | head -1 | cut -c1-120)
    hit=''; wrong=''; unj=''; addhit=''
    for id in $sel $added; do
      st=$(status_of "$sub" "$id"); det=$(detail_of "$sub" "$id"); tg=$(tags_in "$det")
      actual+="$id=${st:-NOTREPORTED}${tg:+ $tg}; "
      [[ $st == FAIL ]] || { [[ $st == SKIP && "$det" =~ \[(load|void|inconclusive)\] ]] && unj+="$id "; continue; }
      if [[ " $added " == *" $id "* ]]; then addhit+="$id "; continue; fi
      ok=''; IFS=/ read -ra tl <<< "$tags"; for t in "${tl[@]}"; do [[ -n $t && "$det" == *"$t"* ]] && ok=1; done
      if [[ -n $ok ]]; then hit+="$id "; else wrong+="$id "; fi
    done
    if [[ -n $addhit ]]; then verdict="caught by the added case ($addhit)"; n_added=$((n_added + 1))
    elif [[ -n $hit ]]; then verdict="caught as predicted ($hit)"; n_pred=$((n_pred + 1))
    elif [[ -n $wrong ]]; then verdict="caught elsewhere: predicted case red with another tag ($wrong)"; n_else=$((n_else + 1))
    elif [[ -n $unj ]]; then verdict="not judged (timing case skipped: $unj)"; n_unj=$((n_unj + 1))
    fi
  else
    actual='no case predicted; '
  fi
  if [[ -z $verdict ]]; then
    if [[ $FULL == 1 ]]; then
      run_round "$M/$q.sh" '.' "$full" "$fout"
      other=$(awk '$1 == "FAIL" && $2 !~ /^V0-/ { printf "%s ", $2 }' "$full")
      actual+="full round: FAIL ${other:-none}"
      if [[ -n $other ]]; then verdict="caught elsewhere (not by the predicted cases): $other"; n_else=$((n_else + 1)); else verdict="NOT CAUGHT"; n_none=$((n_none + 1)); fi
    else
      verdict="not caught by the predicted cases (no full round)"; n_none=$((n_none + 1))
    fi
  fi
  printf '%s | %s | %s ; %s | %s | %s | %s\n' "$q" "$title" "${cases:-?}" "${tags:-?}" "${actual% }" "${ldesc:-no load line}" "$verdict" >> "$OUT"
  echo "$q: $verdict" | cut -c1-200
done
printf '# end | %s | load %s | caught as predicted %d, caught by the added case %d, caught elsewhere %d, not judged %d, NOT CAUGHT %d\n' "$(date -u +%FT%TZ)" "$(load3)" "$n_pred" "$n_added" "$n_else" "$n_unj" "$n_none" >> "$OUT"
tail -n 1 "$OUT"

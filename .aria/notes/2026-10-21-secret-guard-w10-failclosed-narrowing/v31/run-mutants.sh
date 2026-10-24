#!/usr/bin/env bash
# run-mutants.sh <hook> <work dir> : builds the bad implementations from the hook under test (mutants.py) and runs sc-cases.sh on each, one at a time
# (SC_BASH as for sc-cases.sh). By default only the designated cases run (SC_ONLY = their ids; sc-direct.sh skips its slow unselected cases);
# MUT_SCOPE=full runs every case and also lists the other cases that turned red. MUT_ONLY=<regex of ids> runs only those (BI and P ids).
# A BI is CAUGHT when every designated case is FAIL and its detail matches the reason listed in reasons.tsv (the tag of the failed check: "red for the
# designated reason", post_planning R2). Otherwise, in this order:
#   SETUP         a designated case was SETUP, MISSING or absent -- never counted as caught (R2 PP2-m2)
#   WRONG-REASON  a designated case is FAIL, but not for the listed reason (an unrelated assertion turned red)
#   MISSED        a designated case passed in a run whose timing batch was judged (or a direct / static case passed under any load)
#   NOT-JUDGED    a designated case was SKIP (load, void, inconclusive, root), or an end-to-end case stayed green in a run whose timing batch was not
#                 judged: on a loaded host the rerun can fall back to the baseline bytes before a bad implementation shows (INV-7) -- run it again
# Then the perturbation round (perturb.tsv): P-0 must have no FAIL, MISSING or SETUP over all cases; every other P-* must turn its designated cases red
# for the listed reason. The summary goes to stdout; every sc-cases.sh output stays in the work dir. Exit 0 when every BI is CAUGHT, P-0 is GREEN and every
# other P-* is CAUGHT; 1 otherwise; 3 when mutants.py fails.
# Suite mode, MUT_SUITE=<aria checkout> (TASK-002 3d, 10CG/aria-plugin#217): each bad implementation and perturbation runs instead as a filtered round of
# the ported suite, run-suite.sh <aria checkout> <bad implementation> <work dir> -> $W/<ID>.txt, with SG_W10_ONLY = the designated cases ("." for P-0 and
# under MUT_SCOPE=full) and SG_W10_LOG = $W/<ID>.log, the per-case lines (v31 format) that the verdicts read. The verdicts are the same, except:
#   [reference]  a designated case that goes through the gate-closed arm (REFIDS below: the 23 ids of the suite's sg_w10_ref table and the helper's fbref
#                ids V6-S20, V6-S21, as at aria df2d629) is red for the listed reason also when its detail carries [reference], whatever reasons.tsv
#                lists (its state then reads red[reference]). Why: (1) the suite does not read 59e333c (no git history), so "not the baseline's bytes"
#                is said there by two checks together: "not the gate-closed arm's bytes" and "the gate-closed arm gives the baseline's known outcome"
#                (sg_w10_ref / fbref, measured on 59e333c); (2) the suite checks that reference first and returns early when it does not hold, without
#                the original check, so a bad implementation that moves the gate-closed arm off the baseline's known outcome is reported as [reference]
#                -- itself a real fault: with the gate closed, the hook no longer gives what 59e333c gives. (The plan first allowed this only where
#                reasons.tsv lists [bytes]; the lead widened it to every designated case of the gate-closed arm on 2026-10-24, for reason (2).)
#   [missing]    the suite records MISSING (the helper's, and its own check that a function is defined) as FAIL [missing], and the helper's SETUP as
#                FAIL [setup]: judged as a FAIL like any other, it lands in WRONG-REASON where it does not match reasons.tsv -- like SETUP in the
#                sc-cases.sh mode, never counted as caught.
#   P-0          must have no FAIL over all the ported cases and no SKIP other than [platform]: a FAIL makes it RED, another SKIP NOT-JUDGED (run it again).
# Without MUT_SUITE the script behaves exactly as before. A MUT_SUITE that has no hooks/tests/secret-guard.test.sh exits 3.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; H=$(readlink -f "$1"); W=$2; mkdir -p "$W"
python3 "$HERE/mutants.py" "$H" "$W/mut" > "$W/mutants.log" || { cat "$W/mutants.log"; exit 3; }
SCOPE=${MUT_SCOPE:-designated}
SUITE=''; RES=.txt   # suite mode: the aria checkout, and the verdicts read $W/<ID>.log instead of $W/<ID>.txt
REFIDS='V1-E16-p1-small-benign V1-E16-p1-small-read-filter V1-E16-p1-var-mid V1-E16-p1-small-read V1-E16-p1-var-read V1-E16-p1-var-mid-read'
REFIDS+=' V9-E12-vmax-unchanged V7-E1-benign-big-allowed V6-E2-deadline-fallback-bytes V3-E3-anchor-at-hook-start V3-E4-cap-3-at-budget-4 V3-E5-budget-2'
REFIDS+=' V2-E6-flag-from-environment-ignored V2-E7-no-time-left V2-E8-ostype-from-environment-ignored V2-E9-extension-project V9-E10-count-axis-read-blocked'
REFIDS+=' V9-E11-tmax-in-rerun V7-E13-multiline-copy-normal-text V7-E14-long-line-from-expansion V7-E15-credit-as-normal V2-E18-extension-via-stdin-cwd'
REFIDS+=' V5-E19-deadline-with-term-ignored V6-S20-segment-fallback-text V6-S21-whole-fallback-text'
if [[ -n "${MUT_SUITE:-}" ]]; then
  SUITE=$(readlink -f "$MUT_SUITE"); RES=.log
  [[ -n "$SUITE" && -f "$SUITE/hooks/tests/secret-guard.test.sh" ]] || { echo "run-mutants.sh: MUT_SUITE=$MUT_SUITE has no hooks/tests/secret-guard.test.sh" >&2; exit 3; }
  printf '# run-mutants.sh | %s | hook %s | mutants.py %s | suite mode: %s (secret-guard.test.sh %s, helper %s, run-suite.sh %s) | SC_BASH %s | scope %s | load %s\n' \
    "$(date -u +%FT%TZ)" "$(sha256sum < "$H" | cut -c1-12)" "$(sha256sum < "$HERE/mutants.py" | cut -c1-12)" "$SUITE" \
    "$(sha256sum < "$SUITE/hooks/tests/secret-guard.test.sh" | cut -c1-12)" "$( { sha256sum < "$SUITE/hooks/tests/lib/secret-guard-w10-direct.sh" || echo missing; } 2>/dev/null | cut -c1-12)" \
    "$(sha256sum < "$HERE/run-suite.sh" | cut -c1-12)" "${SC_BASH:-bash on PATH}" "$SCOPE" "$(cut -d' ' -f1-3 /proc/loadavg)"
else
printf '# run-mutants.sh | %s | hook %s | mutants.py %s | sc-cases %s | SC_BASH %s | scope %s | load %s\n' "$(date -u +%FT%TZ)" "$(sha256sum < "$H" | cut -c1-12)" \
  "$(sha256sum < "$HERE/mutants.py" | cut -c1-12)" "$(sha256sum < "$HERE/sc-cases.sh" | cut -c1-12)" "${SC_BASH:-bash on PATH}" "$SCOPE" "$(cut -d' ' -f1-3 /proc/loadavg)"
fi
runsc() {   # ID HOOK CASES|all : runs sc-cases.sh -> $W/<ID>.txt (suite mode: run-suite.sh -> $W/<ID>.txt, the per-case lines -> $W/<ID>.log)
  local only='.'
  [[ $SCOPE != full && $3 != all ]] && only="^($(tr ' ' '|' <<< "$3"))\$"
  if [[ -n $SUITE ]]; then
    rm -f "$W/$1.log"
    SG_W10_ONLY="$only" SG_W10_LOG="$W/$1.log" bash "$HERE/run-suite.sh" "$SUITE" "$2" "$W" > "$W/$1.txt" 2>&1
    [[ -f "$W/$1.log" ]] || : > "$W/$1.log"   # no log written: every designated case is absent (SETUP)
  else
  SC_ONLY="$only" bash "$HERE/sc-cases.sh" "$2" > "$W/$1.txt" 2>&1
  fi
}
verdict() {   # ID CASES OUTFILE : sets V (the verdict word) and VD (per designated case: id=state)
  local id=$1 o=$3 c st det rx ref batch s_set=0 s_wr=0 s_miss=0 s_nj=0 s_red=0
  batch=$(grep -o 'timing batch: .*' "$o" | head -1)
  VD=''
  for c in $2; do
    st=$(awk -v c="$c" '$2==c {print $1; exit}' "$o"); det=$(awk -v c="$c" '$2==c {$1=""; $2=""; print; exit}' "$o")
    rx=$(awk -F'\t' -v i="$id" -v c="$c" '$1==i && $2==c {print $3; exit}' "$W/mut/reasons.tsv")
    ref=''; [[ -n $SUITE && " $REFIDS " == *" $c "* && $det == *'[reference]'* ]] && ref='[reference]'   # suite mode only (header)
    case $st in
      FAIL) if grep -qE -- "$rx" <<< "$det" || [[ -n $ref ]]; then s_red=$((s_red+1)); VD+=" $c=red$ref"; else s_wr=$((s_wr+1)); VD+=" $c=red-for-another-reason(want $rx)"; fi ;;
      PASS) if [[ $batch != 'timing batch: judged' && $c =~ ^V[0-9]+-E[0-9]+ ]]; then s_nj=$((s_nj+1)); VD+=" $c=green-under-load"; else s_miss=$((s_miss+1)); VD+=" $c=green"; fi ;;
      SKIP) s_nj=$((s_nj+1)); VD+=" $c=skip$(grep -o '^ *\[[a-z]*\]' <<< "$det" | tr -d ' ')" ;;
      *) s_set=$((s_set+1)); VD+=" $c=${st:-absent}" ;;
    esac
  done
  if (( s_set )); then V=SETUP; elif (( s_wr )); then V=WRONG-REASON; elif (( s_miss )); then V=MISSED; elif (( s_nj )); then V=NOT-JUDGED; else V=CAUGHT; fi
}
declare -A N=([CAUGHT]=0 [MISSED]=0 [WRONG-REASON]=0 [NOT-JUDGED]=0 [SETUP]=0)
while IFS=$'\t' read -r id cases desc seats; do
  [[ "$id" =~ ^(${MUT_ONLY:-.*})$ ]] || continue
  runsc "$id" "$W/mut/$id.sh" "$cases"; verdict "$id" "$cases" "$W/$id$RES"; N[$V]=$((N[$V]+1))
  other=''; [[ $SCOPE == full ]] && other=$(awk '$1=="FAIL"||$1=="MISSING"||$1=="SETUP" {print $2}' "$W/$id$RES" | grep -vxF -f <(tr ' ' '\n' <<< "$cases") | tr '\n' ' ')
  printf '%-7s %-12s %s | seats: %s |%s | %s%s\n' "$id" "$V" "$desc" "$seats" "$VD" "$(grep -o 'load start .*' "$W/$id$RES" | head -1)" "${other:+ | other red: $other}"
done < "$W/mut/designated.tsv"
total=$(( N[CAUGHT] + N[MISSED] + N[WRONG-REASON] + N[NOT-JUDGED] + N[SETUP] ))
printf '# %d caught, %d missed, %d wrong reason, %d not judged, %d setup (of %d)\n' "${N[CAUGHT]}" "${N[MISSED]}" "${N[WRONG-REASON]}" "${N[NOT-JUDGED]}" "${N[SETUP]}" "$total"
pbad=0
while IFS=$'\t' read -r id cases desc; do
  [[ "$id" =~ ^(${MUT_ONLY:-.*})$ ]] || continue
  if [[ $cases == all ]]; then
    runsc "$id" "$W/mut/$id.sh" all
    red=$(awk '$1=="FAIL"||$1=="MISSING"||$1=="SETUP" {print $2}' "$W/$id$RES" | tr '\n' ' ')
    skipx=''; [[ -n $SUITE ]] && skipx=$(awk '$1=="SKIP" && $3!="[platform]" {print $2}' "$W/$id$RES" | tr '\n' ' ')   # suite mode: SKIP only as [platform]
    if [[ -z "$red$skipx" ]]; then V=GREEN; elif [[ -z "$red" ]]; then V=NOT-JUDGED; pbad=$((pbad+1)); else V=RED; pbad=$((pbad+1)); fi
    printf '%-17s %-12s %s | %s | %s%s\n' "$id" "$V" "$desc" "$(tail -1 "$W/$id.txt")" "$(grep -o 'load start .*' "$W/$id$RES" | head -1)" "${red:+ | red: $red}${skipx:+ | SKIP other than [platform]: $skipx}"
  else
    runsc "$id" "$W/mut/$id.sh" "$cases"; verdict "$id" "$cases" "$W/$id$RES"; [[ $V == CAUGHT ]] || pbad=$((pbad+1))
    printf '%-17s %-12s %s |%s | %s\n' "$id" "$V" "$desc" "$VD" "$(grep -o 'load start .*' "$W/$id$RES" | head -1)"
  fi
done < "$W/mut/perturb.tsv"
printf '# perturbation round: %d not as expected | load at the end %s\n' "$pbad" "$(cut -d' ' -f1-3 /proc/loadavg)"
(( N[CAUGHT] == total && pbad == 0 ))

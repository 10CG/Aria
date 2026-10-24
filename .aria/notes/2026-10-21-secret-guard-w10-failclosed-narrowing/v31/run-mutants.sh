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
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; H=$(readlink -f "$1"); W=$2; mkdir -p "$W"
python3 "$HERE/mutants.py" "$H" "$W/mut" > "$W/mutants.log" || { cat "$W/mutants.log"; exit 3; }
SCOPE=${MUT_SCOPE:-designated}
printf '# run-mutants.sh | %s | hook %s | mutants.py %s | sc-cases %s | SC_BASH %s | scope %s | load %s\n' "$(date -u +%FT%TZ)" "$(sha256sum < "$H" | cut -c1-12)" \
  "$(sha256sum < "$HERE/mutants.py" | cut -c1-12)" "$(sha256sum < "$HERE/sc-cases.sh" | cut -c1-12)" "${SC_BASH:-bash on PATH}" "$SCOPE" "$(cut -d' ' -f1-3 /proc/loadavg)"
runsc() {   # ID HOOK CASES|all : runs sc-cases.sh -> $W/<ID>.txt
  local only='.'
  [[ $SCOPE != full && $3 != all ]] && only="^($(tr ' ' '|' <<< "$3"))\$"
  SC_ONLY="$only" bash "$HERE/sc-cases.sh" "$2" > "$W/$1.txt" 2>&1
}
verdict() {   # ID CASES OUTFILE : sets V (the verdict word) and VD (per designated case: id=state)
  local id=$1 o=$3 c st det rx batch s_set=0 s_wr=0 s_miss=0 s_nj=0 s_red=0
  batch=$(grep -o 'timing batch: .*' "$o" | head -1)
  VD=''
  for c in $2; do
    st=$(awk -v c="$c" '$2==c {print $1; exit}' "$o"); det=$(awk -v c="$c" '$2==c {$1=""; $2=""; print; exit}' "$o")
    rx=$(awk -F'\t' -v i="$id" -v c="$c" '$1==i && $2==c {print $3; exit}' "$W/mut/reasons.tsv")
    case $st in
      FAIL) if grep -qE -- "$rx" <<< "$det"; then s_red=$((s_red+1)); VD+=" $c=red"; else s_wr=$((s_wr+1)); VD+=" $c=red-for-another-reason(want $rx)"; fi ;;
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
  runsc "$id" "$W/mut/$id.sh" "$cases"; verdict "$id" "$cases" "$W/$id.txt"; N[$V]=$((N[$V]+1))
  other=''; [[ $SCOPE == full ]] && other=$(awk '$1=="FAIL"||$1=="MISSING"||$1=="SETUP" {print $2}' "$W/$id.txt" | grep -vxF -f <(tr ' ' '\n' <<< "$cases") | tr '\n' ' ')
  printf '%-7s %-12s %s | seats: %s |%s | %s%s\n' "$id" "$V" "$desc" "$seats" "$VD" "$(grep -o 'load start .*' "$W/$id.txt" | head -1)" "${other:+ | other red: $other}"
done < "$W/mut/designated.tsv"
total=$(( N[CAUGHT] + N[MISSED] + N[WRONG-REASON] + N[NOT-JUDGED] + N[SETUP] ))
printf '# %d caught, %d missed, %d wrong reason, %d not judged, %d setup (of %d)\n' "${N[CAUGHT]}" "${N[MISSED]}" "${N[WRONG-REASON]}" "${N[NOT-JUDGED]}" "${N[SETUP]}" "$total"
pbad=0
while IFS=$'\t' read -r id cases desc; do
  [[ "$id" =~ ^(${MUT_ONLY:-.*})$ ]] || continue
  if [[ $cases == all ]]; then
    runsc "$id" "$W/mut/$id.sh" all
    red=$(awk '$1=="FAIL"||$1=="MISSING"||$1=="SETUP" {print $2}' "$W/$id.txt" | tr '\n' ' ')
    if [[ -z "$red" ]]; then V=GREEN; else V=RED; pbad=$((pbad+1)); fi
    printf '%-17s %-12s %s | %s | %s%s\n' "$id" "$V" "$desc" "$(tail -1 "$W/$id.txt")" "$(grep -o 'load start .*' "$W/$id.txt" | head -1)" "${red:+ | red: $red}"
  else
    runsc "$id" "$W/mut/$id.sh" "$cases"; verdict "$id" "$cases" "$W/$id.txt"; [[ $V == CAUGHT ]] || pbad=$((pbad+1))
    printf '%-17s %-12s %s |%s | %s\n' "$id" "$V" "$desc" "$VD" "$(grep -o 'load start .*' "$W/$id.txt" | head -1)"
  fi
done < "$W/mut/perturb.tsv"
printf '# perturbation round: %d not as expected | load at the end %s\n' "$pbad" "$(cut -d' ' -f1-3 /proc/loadavg)"
(( N[CAUGHT] == total && pbad == 0 ))

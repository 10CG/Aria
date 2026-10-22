#!/usr/bin/env bash
# run-mutants.sh <v3.1 hook> <work dir> : runs sc-cases.sh on every bad implementation of mutants.py (bash on PATH) and reports, per BI, whether each of its
# designated cases turned red (CAUGHT) and which other cases turned red as well (collateral). The summary goes to stdout; full outputs stay in the work dir.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; H=$(readlink -f "$1"); W=$2; mkdir -p "$W"
python3 "$HERE/mutants.py" "$H" "$W/mut" >/dev/null || exit 3
caught=0 missed=0
while IFS=$'\t' read -r id cases desc; do
  [[ "$id" =~ ^(${MUT_ONLY:-.*})$ ]] || continue   # MUT_ONLY=<regex of BI ids>: run only those
  o="$W/$id.txt"; bash "$HERE/sc-cases.sh" "$W/mut/$id.sh" > "$o" 2>&1
  red=$(awk '$1=="FAIL"{print $2}' "$o" | sort -u)
  miss=""; for c in $cases; do grep -qxF "$c" <<< "$red" || miss="$miss $c"; done
  other=$(comm -23 <(printf '%s\n' "$red") <(tr ' ' '\n' <<< "$cases" | sort -u) | grep -v '^$' | tr '\n' ' ')
  if [[ -z "$miss" ]]; then caught=$((caught+1)); v=CAUGHT; else missed=$((missed+1)); v="MISSED (designated still green:$miss)"; fi
  printf '%-6s %-8s %s | designated: %s | other red: %s\n' "$id" "${v%% *}" "$desc" "$cases" "${other:-none}"
  [[ $v == CAUGHT ]] || printf '       %s\n' "$v"
done < "$W/mut/designated.tsv"
printf '# %d caught, %d missed (of %d)\n' "$caught" "$missed" $((caught+missed))
(( missed == 0 ))

#!/usr/bin/env bash
# reftab.sh <label>=<SG_W10_LOG file> ... : the gate-closed arm's outcome per case id and per log ("rc kind"; fbt: "status kind"), one row per id, and
# the ids whose outcome differs between the logs; also counts the [reference] tags per log
for a in "$@"; do
  l=${a%%=*}; f=${a#*=}
  awk -v L="$l" '
    /^(PASS|FAIL|SKIP) V[0-9]+-/ {
      id=$2; v=""
      if (match($0, /gate-closed rc=[0-9]+ [a-z]+/)) { s=substr($0, RSTART, RLENGTH); sub(/gate-closed rc=/, "", s); v=s }
      else if (match($0, /gate closed by WSL_DISTRO_NAME: status [0-9]+ [a-z]+/)) { s=substr($0, RSTART, RLENGTH); sub(/.*status /, "", s); v=s }
      else if (match($0, /\(status [0-9]+ [a-z]+\)/)) { s=substr($0, RSTART+8, RLENGTH-9); v=s }
      if (v != "") print id "\t" L "\t" v "\t" ($0 ~ /\[reference\]/ ? "REF" : "-")
    }' "$f"
done | sort -k1,1 -k2,2 | awk -F'\t' '
  { k=$1; if (!(k in row)) { ids[++n]=k; row[k]="" } row[k]=row[k] sprintf("  %s:%s%s", $2, $3, ($4=="REF" ? "[REF]" : "")); vals[k, $3]=1; if (!((k SUBSEP "c") in cnt)) cnt[k SUBSEP "c"]=0 }
  { if (!((k, $3) in seen)) { seen[k, $3]=1; nv[k]++ } }
  END { for (i=1; i<=n; i++) { k=ids[i]; printf "%-42s %s%s\n", k, (nv[k]>1 ? "DIFFERS " : ""), row[k] } }'
for a in "$@"; do f=${a#*=}; printf '%s: [reference] %s, FAIL %s, PASS %s, SKIP %s\n' "${a%%=*}" "$(grep -c '\[reference\]' "$f")" "$(grep -c '^FAIL ' "$f")" "$(grep -c '^PASS ' "$f")" "$(grep -c '^SKIP ' "$f")"; done

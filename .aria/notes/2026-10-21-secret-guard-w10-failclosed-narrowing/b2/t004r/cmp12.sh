#!/usr/bin/env bash
# cmp12.sh OLD_TSV NEW_TSV : per-n outcome (rc, kind, rerun entered or not) of the W12 replay, old vs new; prints counts and n only
awk -F'\t' 'FNR == 1 { f++ } /^#/ { next }
  f == 1 { o[$1] = $2 " " $3; ors[$1] = ($6 == "-") ? "no-rerun" : "rerun"; next }
  f == 2 { m++; nr = ($6 == "-") ? "no-rerun" : "rerun"; c[$2 " " $3 " " nr]++
           if (!($1 in o)) { add = add " " $1; next }
           if (o[$1] != $2 " " $3 || ors[$1] != nr) { d++; dl = dl sprintf(" n=%s %s/%s->%s/%s", $1, o[$1], ors[$1], $2 " " $3, nr) } ; seen[$1] = 1 }
  END { for (k in o) if (!(k in seen)) gone = gone " " k
        for (k in c) printf "  new outcome %-28s %d\n", k, c[k]
        printf "  rows new %d | differ from old %d%s | only in new:%s | only in old:%s\n", m, d + 0, dl, (add == "" ? " none" : add), (gone == "" ? " none" : gone) }' "$1" "$2" | sort

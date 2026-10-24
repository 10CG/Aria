#!/bin/bash
# cross-check: the suite's sg_w10_ref table and the helper's fbref against the gate-closed outcomes logged on 59e333c and on the implementation (3c's logs)
D=$1; S=$2/hooks/tests/secret-guard.test.sh; H=$2/hooks/tests/lib/secret-guard-w10-direct.sh
eval "$(sed -n '/^sg_w10_ref() {/,/^}/p' "$S")"
for side in base impl; do
  for v in 32 50 51 52 53; do
    f=$D/$side-$v.log; [[ -f $f ]] || { echo "$side-$v: no log"; continue; }
    n=0; bad=0
    while IFS= read -r l; do
      id=$(awk '{print $2}' <<<"$l")
      if [[ $l =~ gate-closed\ rc=([0-9]+)\ ([a-z]+) ]]; then got="${BASH_REMATCH[1]} ${BASH_REMATCH[2]}"
      elif [[ $l =~ \(status\ ([0-9]+)\ ([a-z]+)\) ]]; then got="${BASH_REMATCH[1]} ${BASH_REMATCH[2]}"
      else continue; fi
      n=$((n+1))
      case $id in V6-S2[01]*) want=fbref ;; *) want=$(sg_w10_ref "$id") ;; esac
      [[ $want == fbref ]] && want='2 oversize'
      [[ $got == "$want" ]] || { bad=$((bad+1)); echo "  $side-$v $id got [$got] table [$want]"; }
    done < <(grep -E '^(PASS|FAIL|TIMED|SKIP) ' "$f")
    echo "$side-$v: $n gate-closed outcomes read, $bad differ from the table"
  done
done
echo "fbref in helper:"; grep -n '^fbref\|fbref()' "$H" | head -3
n=$(grep -n 'fbref() {' "$H" | cut -d: -f1); [[ -n $n ]] && sed -n "${n},$((n+4))p" "$H" | cut -c1-200

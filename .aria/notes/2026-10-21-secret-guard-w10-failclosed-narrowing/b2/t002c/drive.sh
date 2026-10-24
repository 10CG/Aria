#!/usr/bin/env bash
# drive.sh : the 3a runs, one at a time. Each waits (at most 20 min) for a one-minute load below 1.8, records its loads, and timing-dependent runs retry
# (at most 3 tries) until their timing batch is judged. Everything goes to files under t002c/; progress to drive.log; "DRIVE DONE" at the end.
set -u
S=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad
WT=$S/wt217/aria; O=$S/r217impl/t002c; V=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31
LOG=$O/drive.log; HK=$WT/hooks/secret-guard.sh
note() { echo "$(date -u +%T) $*" >> "$LOG"; return 0; }
waitlow() {   # waits for a one-minute load below 1.8 (at most 120 x 10 s); returns 0 either way -- each run records its own loads
  local i=0
  while (( i < 120 )); do awk '{exit !($1 < 1.8)}' /proc/loadavg && return 0; sleep 10; i=$((i+1)); done
  note "waitlow: gave up after 20 min at load $(cut -d' ' -f1-3 /proc/loadavg)"
  return 0
}
judged() { grep -q 'timing batch: judged$' "$1" 2>/dev/null; }
round() {   # TAG BASH : the whole suite in the worktree (git checkout), SC_BASH=BASH, SG_W10_LOG; retried until the W10 timing batch is judged
  local tag=$1 b=$2 n rc
  for n in 1 2 3; do
    waitlow; note "round $tag try $n start load $(cut -d' ' -f1-3 /proc/loadavg)"
    ( cd "$WT" && SC_BASH=$b SG_W10_LOG=$O/round-$tag.log taskset -c 0,1 nice -n 19 bash hooks/tests/secret-guard.test.sh ) > "$O/round-$tag.txt" 2>&1; rc=$?
    note "round $tag try $n rc=$rc end load $(cut -d' ' -f1-3 /proc/loadavg) | $(grep -o 'timing batch: .*' "$O/round-$tag.log" | head -1) | $(grep -E '^(PASS|FAIL|SKIP):' "$O/round-$tag.txt" | tr '\n' ' ')"
    judged "$O/round-$tag.log" && break
  done
  return 0
}
viasuite() {   # TAG HOOK REGEX : run-suite.sh on a copy, only the ported cases matching REGEX; retried until judged
  local tag=$1 h=$2 rx=$3 n rc
  for n in 1 2 3; do
    waitlow; note "suite-copy $tag try $n start load $(cut -d' ' -f1-3 /proc/loadavg)"
    SC_BASH=/usr/bin/bash SG_W10_ONLY="$rx" SG_W10_LOG=$O/$tag.log bash "$V/run-suite.sh" "$WT" "$h" "$O/copies" > "$O/$tag.txt" 2>&1; rc=$?
    note "suite-copy $tag try $n rc=$rc | $(grep -o 'timing batch: .*' "$O/$tag.log" | head -1) | $(grep -E '^(PASS|FAIL|SKIP):' "$O/$tag.txt" | tr '\n' ' ')"
    judged "$O/$tag.log" && break
  done
  return 0
}
verdict() {   # BI LOG CASES : every designated case FAIL with the reason of reasons.tsv -> CAUGHT
  local id=$1 lg=$2 c st det rx out=''
  for c in $3; do
    st=$(awk -v c="$c" '$2==c {print $1; exit}' "$lg"); det=$(awk -v c="$c" '$2==c {$1=""; $2=""; print; exit}' "$lg")
    rx=$(awk -F'\t' -v i="$id" -v c="$c" '$1==i && $2==c {print $3; exit}' "$O/mut/reasons.tsv")
    if [[ $st == FAIL ]] && grep -qE -- "$rx" <<< "$det"; then out+=" $c=red(reason $rx)"; else out+=" $c=NOT-CAUGHT(st=${st:-absent}, want reason $rx)"; fi
  done
  note "verdict $id:$out"
  return 0
}
note "DRIVE START load $(cut -d' ' -f1-3 /proc/loadavg) hook $(sha256sum < "$HK" | cut -c1-12)"
# ---- 1. bad implementations (built from the implementation), through run-suite.sh on a copy ----
python3 "$V/mutants.py" "$HK" "$O/mut" > "$O/mutants.log" 2>&1 || note "mutants.py failed: $(tail -2 "$O/mutants.log")"
viasuite ctl-impl "$HK" '^(V2-G12-segment-trigger-asks-gate|V6-E2-deadline-fallback-bytes|V10-N3-environ-big-judge|V11-S4-one-rule-loop)$'
viasuite mut-BI-24 "$O/mut/BI-24.sh" '^(V2-G12-segment-trigger-asks-gate)$'; verdict BI-24 "$O/mut-BI-24.log" 'V2-G12-segment-trigger-asks-gate'
viasuite mut-BI-7 "$O/mut/BI-7.sh" '^(V6-E2-deadline-fallback-bytes)$'; verdict BI-7 "$O/mut-BI-7.log" 'V6-E2-deadline-fallback-bytes'
viasuite mut-BI-11 "$O/mut/BI-11.sh" '^(V10-N3-environ-big-judge|V11-S4-one-rule-loop)$'; verdict BI-11 "$O/mut-BI-11.log" 'V10-N3-environ-big-judge V11-S4-one-rule-loop'
# ---- 2. the five rounds in the worktree ----
round bash-5.2 /usr/bin/bash
for v in 5.0.18 5.1.16 5.3.20 3.2.57; do round bash-$v /home/dev/.aria/tools/bash-$v/bash; done
# ---- 3. equivalence: v31/sc-cases.sh on the implementation, same bash (5.2), then the per-id statuses against the suite's round ----
for n in 1 2 3; do
  waitlow; note "sc-cases try $n start load $(cut -d' ' -f1-3 /proc/loadavg)"
  SC_BASH=/usr/bin/bash bash "$V/sc-cases.sh" "$HK" > "$O/equiv-sc-cases.txt" 2>&1
  note "sc-cases try $n rc=$? | $(grep -o 'timing batch: .*' "$O/equiv-sc-cases.txt" | head -1) | $(tail -1 "$O/equiv-sc-cases.txt")"
  judged "$O/equiv-sc-cases.txt" && break
done
awk 'FNR==1{f++} /^#/{next} f==1{a[$2]=$1} f==2 && $1 ~ /^(PASS|FAIL|SKIP|MISSING|SETUP)$/ {b[$2]=$1}
  END{for(k in a) if(!(k in b)) print "only-suite", k, a[k]; for(k in b) if(!(k in a)) print "only-v31", k, b[k]
      for(k in a) if((k in b) && a[k]!=b[k]) print "status-differs", k, "suite=" a[k], "v31=" b[k]
      n=0; for(k in a) if(k in b) n++; print "# ids in both:", n}' "$O/round-bash-5.2.log" "$O/equiv-sc-cases.txt" | sort > "$O/equiv-diff.txt"
note "equivalence: $(grep -vc '^#' "$O/equiv-diff.txt") difference line(s); $(grep '^#' "$O/equiv-diff.txt")"
note "DRIVE DONE load $(cut -d' ' -f1-3 /proc/loadavg)"

#!/usr/bin/env bash
# drive2.sh OLD_PID... : replaces drive.sh after its mutant part. Waits until the given processes (the old driver's running suite, recorded by PID) are
# gone, then, one at a time: W10-only rounds (SG_W10_ONLY=.) per bash, retried (at most 3) until the timing batch is judged; v31/sc-cases.sh on the
# implementation (5.2, at most 3 tries); the equivalence diff; one full round per bash in the worktree. Progress to drive.log; "DRIVE DONE" at the end.
set -u
S=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad
WT=$S/wt217/aria; O=$S/r217impl/t002c; V=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31
LOG=$O/drive.log; HK=$WT/hooks/secret-guard.sh
BASHES="bash-5.2:/usr/bin/bash bash-5.0.18:/home/dev/.aria/tools/bash-5.0.18/bash bash-5.1.16:/home/dev/.aria/tools/bash-5.1.16/bash bash-5.3.20:/home/dev/.aria/tools/bash-5.3.20/bash bash-3.2.57:/home/dev/.aria/tools/bash-3.2.57/bash"
note() { echo "$(date -u +%T) $*" >> "$LOG"; return 0; }
ld() { cut -d' ' -f1-3 /proc/loadavg; }
waitfor() {   # LIMIT MAX : waits for a one-minute load below LIMIT, at most MAX x 10 s; returns 0 either way (each run records its own loads)
  local lim=$1 max=$2 i=0
  while (( i < max )); do awk -v l="$lim" '{exit !($1 < l)}' /proc/loadavg && return 0; sleep 10; i=$((i+1)); done
  note "wait: load $(ld) after $((max * 10)) s (limit $lim)"
  return 0
}
judged() { grep -q 'timing batch: judged$' "$1" 2>/dev/null; }
for p in "$@"; do while kill -0 "$p" 2>/dev/null; do sleep 5; done; done
note "drive2 start: the old driver is stopped and its last suite run has ended; load $(ld)"
# ---- 1. W10-only rounds in the worktree (all 136 ported ids), until the timing batch is judged ----
for e in $BASHES; do
  tag=${e%%:*}; b=${e#*:}
  for n in 1 2 3; do
    waitfor 1.5 120; note "w10-only $tag try $n start load $(ld)"
    ( cd "$WT" && SC_BASH=$b SG_W10_ONLY=. SG_W10_LOG=$O/w10-$tag.log taskset -c 0,1 nice -n 19 bash hooks/tests/secret-guard.test.sh ) > "$O/w10-$tag.txt" 2>&1; rc=$?
    note "w10-only $tag try $n rc=$rc end load $(ld) | $(grep -o 'timing batch: .*' "$O/w10-$tag.log" | head -1) | $(grep -E '^(PASS|FAIL|SKIP):' "$O/w10-$tag.txt" | tr '\n' ' ')"
    judged "$O/w10-$tag.log" && break
  done
done
# ---- 2. equivalence: v31/sc-cases.sh on the implementation under 5.2, then the per-id statuses against the judged W10-only round on 5.2 ----
for n in 1 2 3; do
  waitfor 1.5 120; note "sc-cases try $n start load $(ld)"
  SC_BASH=/usr/bin/bash bash "$V/sc-cases.sh" "$HK" > "$O/equiv-sc-cases.txt" 2>&1; rc=$?
  note "sc-cases try $n rc=$rc | $(grep -o 'timing batch: .*' "$O/equiv-sc-cases.txt" | head -1) | $(tail -1 "$O/equiv-sc-cases.txt")"
  judged "$O/equiv-sc-cases.txt" && break
done
awk 'FNR==1{f++} /^#/{next} f==1{a[$2]=$1} f==2 && $1 ~ /^(PASS|FAIL|SKIP|MISSING|SETUP)$/ {b[$2]=$1}
  END{for(k in a) if(!(k in b)) print "only-suite", k, a[k]; for(k in b) if(!(k in a)) print "only-v31", k, b[k]
      for(k in a) if((k in b) && a[k]!=b[k]) print "status-differs", k, "suite=" a[k], "v31=" b[k]
      n=0; for(k in a) if(k in b) n++; print "# ids in both:", n}' "$O/w10-bash-5.2.log" "$O/equiv-sc-cases.txt" | sort > "$O/equiv-diff.txt"
note "equivalence: $(grep -vc '^#' "$O/equiv-diff.txt") difference line(s); $(grep '^#' "$O/equiv-diff.txt")"
# ---- 3. one full round per bash in the worktree (git checkout: SC-8, SC-9a and SC-13 run) ----
for e in $BASHES; do
  tag=${e%%:*}; b=${e#*:}
  waitfor 1.0 60; note "full $tag start load $(ld)"
  ( cd "$WT" && SC_BASH=$b SG_W10_LOG=$O/full-$tag.log taskset -c 0,1 nice -n 19 bash hooks/tests/secret-guard.test.sh ) > "$O/full-$tag.txt" 2>&1; rc=$?
  note "full $tag rc=$rc end load $(ld) | $(grep -o 'timing batch: .*' "$O/full-$tag.log" | head -1) | $(grep -E '^(PASS|FAIL|SKIP):' "$O/full-$tag.txt" | tr '\n' ' ')"
done
note "DRIVE DONE load $(ld)"

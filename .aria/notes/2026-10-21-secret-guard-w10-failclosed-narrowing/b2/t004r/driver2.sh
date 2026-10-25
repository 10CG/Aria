#!/usr/bin/env bash
# t004r driver (10CG/aria-plugin#217, TASK-004 rerun): one heavy phase at a time; each attempt waits (<= 40 min) for a 1-minute load < 1.2,
# records /proc/loadavg at its start and end, and is VOID (INV-7) when either 1-minute reading is >= 2 (at most 3 attempts). Every attempt writes into
# its own dir so/<phase>.<n>; only a valid attempt's files are copied into v31/impl. No command text is read or written here.
set -u
S=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad
T=$S/r217impl/t004r
V=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31
O=$V/impl
ARIA=$S/wt217/aria
HOOK=$T/impl-hook.sh
B32=/home/dev/.aria/tools/bash-3.2.57/bash
WD=$T/work
LOG=$T/driver.log
PH=$T/phases.tsv
N=(taskset -c 0,1 nice -n 19)
ld3() { cut -d' ' -f1-3 /proc/loadavg; }
note() { printf '%s %s\n' "$(date -u +%FT%TZ)" "$*" >> "$LOG"; }
gate() { local i; for ((i = 0; i < 480; i++)); do awk '{exit !($1 < 1.2)}' /proc/loadavg && return 0; sleep 5; done; return 1; }
phase() {
  local name=$1 files=$2; shift 2; local a s e rc t0
  for a in 1 2 3; do
    A=$T/so/$name.$a; mkdir -p "$A"; t0=$(date -u +%FT%TZ)
    if ! gate; then note "$name #$a: no 1-minute load < 1.2 within 40 min (load $(ld3))"; printf '%s\t%s\t%s\t-\t-\t-\tno-window\n' "$name" "$a" "$t0" >> "$PH"; continue; fi
    s=$(ld3); note "$name #$a start, load $s"
    "$@"; rc=$?
    e=$(ld3); note "$name #$a end rc $rc, load $e"
    if awk -v s="${s%% *}" -v e="${e%% *}" 'BEGIN{exit !(s >= 2 || e >= 2)}'; then
      printf '%s\t%s\t%s\t%s\t%s\t%s\tVOID\n' "$name" "$a" "$t0" "$s" "$e" "$rc" >> "$PH"; note "$name #$a VOID (INV-7)"; continue; fi
    printf '%s\t%s\t%s\t%s\t%s\t%s\tvalid\n' "$name" "$a" "$t0" "$s" "$e" "$rc" >> "$PH"
    for f in $files; do cp "$A/$f" "$O/$f" || note "$name: copy of $f failed"; done
    note "$name #$a valid, copied: $files"; return 0
  done
  note "$name: no valid attempt"; return 1
}
# driver2: after driver.sh (pid in driver.pid) has exited: the NOT-JUDGED bad implementations of W13 run again (run-mutants.sh: "run it again"),
# a fourth W9 attempt, and the suite-mode bad implementations once more under a low load (kept in so/ only, not copied).
LOG=$T/driver.log
note() { printf '%s d2 %s\n' "$(date -u +%FT%TZ)" "$*" >> "$LOG"; }
P1=$(cat "$T/driver.pid"); while kill -0 "$P1" 2>/dev/null; do sleep 15; done
note "driver2 start, pid $$"
ev() { OUT=$A IMPL=$HOOK BASH32=$B32 "${N[@]}" bash "$V/run-evidence.sh" "$WD" "$@" > "$A/stdout.txt" 2>&1; }
bi1415() { SC_BASH=/usr/bin/bash MUT_SCOPE=full MUT_ONLY='BI-1[45]' "${N[@]}" bash "$V/run-mutants.sh" "$HOOK" "$A/work" > "$A/W13-rerun-BI-14-15.txt" 2> "$A/stderr.txt"; }
msuite() { MUT_SUITE=$ARIA SC_BASH=/usr/bin/bash "${N[@]}" bash "$V/run-mutants.sh" "$HOOK" "$A/work" > "$A/W13-suite-mutants.txt" 2> "$A/stderr.txt"; }
phase BI1415 "W13-rerun-BI-14-15.txt" bi1415
phase1() { local name=$1 files=$2; shift 2; A=$T/so/$name; mkdir -p "$A"; local s e rc
  gate || { note "$name: no 1-minute load < 1.2 within 40 min"; return 1; }
  s=$(ld3); note "$name start, load $s"; "$@"; rc=$?; e=$(ld3); note "$name end rc $rc, load $e"
  if awk -v s="${s%% *}" -v e="${e%% *}" 'BEGIN{exit !(s >= 2 || e >= 2)}'; then note "$name VOID (INV-7)"; printf '%s\t1\t-\t%s\t%s\t%s\tVOID\n' "$name" "$s" "$e" "$rc" >> "$PH"; return 1; fi
  printf '%s\t1\t-\t%s\t%s\t%s\tvalid\n' "$name" "$s" "$e" "$rc" >> "$PH"
  for f in $files; do cp "$A/$f" "$O/$f"; done; note "$name valid, copied: ${files:-nothing}"; }
phase1 W9.4 "W9-suite.txt" ev W9
phase1 Msuite-r "" msuite
note "driver2 end"; touch "$T/driver2.done"

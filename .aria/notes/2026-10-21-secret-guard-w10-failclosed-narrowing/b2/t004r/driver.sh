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
ev() { OUT=$A IMPL=$HOOK BASH32=$B32 "${N[@]}" bash "$V/run-evidence.sh" "$WD" "$@" > "$A/stdout.txt" 2>&1; }
w13() { MUT_SCOPE=full ev W13; local rc=$?; cp "$WD/sc-base.txt" "$A/W13-sc-base.txt"; return $rc; }
p0v31() { SC_BASH=/usr/bin/bash MUT_ONLY=P-0 "${N[@]}" bash "$V/run-mutants.sh" "$HOOK" "$A/work" > "$A/W13-P0-v31.txt" 2> "$A/stderr.txt"; }
p0suite() { MUT_SUITE=$ARIA SC_BASH=/usr/bin/bash MUT_ONLY=P-0 "${N[@]}" bash "$V/run-mutants.sh" "$HOOK" "$A/work" > "$A/W13-P0-suite.txt" 2> "$A/stderr.txt"; }
msuite() { MUT_SUITE=$ARIA SC_BASH=/usr/bin/bash "${N[@]}" bash "$V/run-mutants.sh" "$HOOK" "$A/work" > "$A/W13-suite-mutants.txt" 2> "$A/stderr.txt"; }
w12() { mkdir -p "$S/tmp-t004r-w12"; TMPDIR=$S/tmp-t004r-w12 TRAFFIC_DIR=$S/traffic-frozen ev W12; }
w14i() { W14_DIR=$A/w14dir W14_PREDICT=$S/r217impl/t003a/predict.md W14_GAPMAP=$S/r217impl/t003a/gapmap.tsv W14_OUT=$A/W14-independent-mutants.txt "${N[@]}" bash "$O/w14.sh" > "$A/stdout.txt" 2>&1; }
w14m() { mkdir -p "$A/w14m"; W14_HOOK=$ARIA/hooks/secret-guard.sh W14_EXPECT_SHA=628652570ce3 W14_WORK=$A/w14m W14_OUT=$A/W14-timing-matrix.txt "${N[@]}" bash "$O/w14-matrix.sh" full > "$A/stdout.txt" 2>&1; }
note "driver start, pid $$, hook $(sha256sum < "$HOOK" | cut -c1-12)"
phase W8 "W8-v31.diff" ev W8
phase W11 "W11-adversarial.txt" ev W11
phase W9 "W9-suite.txt" ev W9
phase W13 "W13-sc-cases.txt W13-sc-base.txt" w13
phase P0v31 "W13-P0-v31.txt" p0v31
phase P0suite "W13-P0-suite.txt" p0suite
phase Msuite "W13-suite-mutants.txt" msuite
phase W12 "W12-real-traffic.txt W12-replay-138.tsv W12-replay-138-base.tsv W12-ident-138.txt" w12
phase W14i "W14-independent-mutants.txt" w14i
phase W14m "W14-timing-matrix.txt" w14m
note "driver end"; touch "$T/driver.done"

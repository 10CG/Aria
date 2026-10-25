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
# driver3 (executor, after the coordinator's added check): an attempt is valid only when its start and end 1-minute readings are < 2 AND, for
# run-mutants.sh outputs, the summary says 0 not judged and every BI / P line says "timing batch: judged" (suite mode: every suite output's
# "W10 ported cases" summary line says "timing batch: judged"). Order by priority: W12, the W13 reruns, then W9 (W9 kept in so/ only: see report).
echo $$ > "$T/driver3.pid"
note() { printf '%s d3 %s\n' "$(date -u +%FT%TZ)" "$*" >> "$LOG"; }
ev() { OUT=$A IMPL=$HOOK BASH32=$B32 "${N[@]}" bash "$V/run-evidence.sh" "$WD" "$@" > "$A/stdout.txt" 2>&1; }
w12() { mkdir -p "$S/tmp-t004r-w12"; TMPDIR=$S/tmp-t004r-w12 TRAFFIC_DIR=$S/traffic-frozen ev W12; }
bi1415() { SC_BASH=/usr/bin/bash MUT_SCOPE=full MUT_ONLY='BI-1[45]' "${N[@]}" bash "$V/run-mutants.sh" "$HOOK" "$A/work" > "$A/W13-rerun-BI-14-15.txt" 2> "$A/stderr.txt"; }
msuite() { MUT_SUITE=$ARIA SC_BASH=/usr/bin/bash "${N[@]}" bash "$V/run-mutants.sh" "$HOOK" "$A/work" > "$A/W13-suite-mutants.txt" 2> "$A/stderr.txt"; }
judged_mut() { [[ -s $1 ]] && grep -qE '^# [0-9]+ caught, 0 missed, 0 wrong reason, 0 not judged, 0 setup' "$1" && ! grep -E '^(BI|P)-' "$1" | grep -vq 'timing batch: judged'; }
judged_suite() { local n b; n=$(grep -rh --include='*.txt' 'W10 ported cases' "$1" | grep -c 'timing batch:'); b=$(grep -rh --include='*.txt' 'W10 ported cases' "$1" | grep 'timing batch:' | grep -vc 'timing batch: judged'); note "suite summary lines in $1: $n, not judged: $b"; (( n > 0 && b == 0 )); }
chk_bi() { judged_mut "$A/W13-rerun-BI-14-15.txt"; }
chk_ms() { judged_mut "$A/W13-suite-mutants.txt" && grep -q '^# perturbation round: 0 not as expected' "$A/W13-suite-mutants.txt" && judged_suite "$A/work"; }
rphase() { local name=$1 max=$2 files=$3 check=$4; shift 4; local a s e rc ok
  for ((a = 1; a <= max; a++)); do A=$T/so/$name.$a; mkdir -p "$A"
    gate || { note "$name #$a: no 1-minute load < 1.2 within 40 min"; continue; }
    s=$(ld3); note "$name #$a start, load $s"; "$@"; rc=$?; e=$(ld3); note "$name #$a end rc $rc, load $e"
    ok=valid; awk -v s="${s%% *}" -v e="${e%% *}" 'BEGIN{exit !(s >= 2 || e >= 2)}' && ok=VOID-load
    if [[ $ok == valid && $check != - ]] && ! $check; then ok=VOID-not-judged; fi
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$name" "$a" "$(date -u +%FT%TZ)" "$s" "$e" "$rc" "$ok" >> "$PH"; note "$name #$a $ok"
    [[ $ok == valid ]] || continue
    for f in $files; do cp "$A/$f" "$O/$f"; done; note "$name #$a copied: ${files:-nothing}"; return 0
  done; note "$name: no valid attempt"; return 1; }
note "driver3 start, pid $$"
rphase W12r 2 "W12-real-traffic.txt W12-replay-138.tsv W12-replay-138-base.tsv W12-ident-138.txt" - w12
rphase BI1415 3 "W13-rerun-BI-14-15.txt" chk_bi bi1415
rphase Msuiter 2 "W13-suite-mutants.txt" chk_ms msuite
rphase W9r 1 "" - ev W9
note "driver3 end"; touch "$T/driver3.done"

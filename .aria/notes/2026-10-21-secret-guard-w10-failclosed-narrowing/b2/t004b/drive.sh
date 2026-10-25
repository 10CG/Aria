#!/usr/bin/env bash
# drive.sh (T004b, 10CG/aria-plugin#217): the five phases one after another (one heavy experiment at a time). A phase starts only when the 1-min load is
# < 1.2; INV-7 judges it on the readings its output records at its start and at its end (first and last line): either >= 2 -> void, rerun, at most 3
# attempts; 6 h without a low-load window -> give up on that phase. NOT-JUDGED bad implementations (P-0 aside: it has its own phase) are rerun once.
set -u
S=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad
T=$S/r217impl/t004b; V31=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31; OUTD=$V31/impl
WT=$S/wt217/aria; HK=$T/impl-hook.sh; B52=/usr/bin/bash
export IMPL=$HK OUT=$OUTD BASH32=/home/dev/.aria/tools/bash-3.2.57/bash
TN=(taskset -c 0,1 nice -n 19); LOG=$T/drive.log; mkdir -p "$T/runs"
cd "$T" || exit 3; echo $$ > "$T/drive.pid"
note() { printf '%s %s | load %s\n' "$(date -u +%FT%TZ)" "$*" "$(cut -d' ' -f1-3 /proc/loadavg)" >> "$LOG"; }
ge() { awk -v a="$1" -v b="$2" 'BEGIN{exit !(a + 0 >= b + 0)}'; }
waitlow() { local t0=$SECONDS; while ge "$(cut -d' ' -f1 /proc/loadavg)" 1.2; do (( SECONDS - t0 >= 21600 )) && return 1; sleep 15; done; }
[[ "$(sha256sum < "$HK" | cut -c1-12)" == af4658b6f935 ]] || { note "STOP: the hook copy is not af4658b6f935"; exit 3; }
note "DRIVER-START pid $$ | wt $(git -C "$WT" rev-parse --short HEAD) dirty $(git -C "$WT" status --porcelain | wc -l) | run-evidence.sh $(sha256sum < "$V31/run-evidence.sh" | cut -c1-12)"
runW9()   { "${TN[@]}" bash "$V31/run-evidence.sh" "$T/wd-W9-a$1" W9; };   outW9()   { echo "$T/wd-W9-a$1/W9-suite.txt"; }
runW13()  { MUT_SCOPE=full "${TN[@]}" bash "$V31/run-evidence.sh" "$T/wd-W13-a$1" W13; };   outW13()  { echo "$T/wd-W13-a$1/W13-sc-cases.txt"; }
runP0v()  { SC_BASH=$B52 MUT_ONLY='P-0' "${TN[@]}" bash "$V31/run-mutants.sh" "$HK" "$T/wd-P0v-a$1" > "$T/P0-v31-a$1.txt" 2>&1; };   outP0v()  { echo "$T/P0-v31-a$1.txt"; }
runP0s()  { SC_BASH=$B52 MUT_ONLY='P-0' MUT_SUITE="$WT" "${TN[@]}" bash "$V31/run-mutants.sh" "$HK" "$T/wd-P0s-a$1" > "$T/P0-suite-a$1.txt" 2>&1; };   outP0s()  { echo "$T/P0-suite-a$1.txt"; }
runSM()   { SC_BASH=$B52 MUT_SUITE="$WT" "${TN[@]}" bash "$V31/run-mutants.sh" "$HK" "$T/wd-SM-a$1" > "$T/suite-mutants-a$1.txt" 2>&1; };   outSM()   { echo "$T/suite-mutants-a$1.txt"; }
runNJ13() { SC_BASH=$B52 MUT_SCOPE=full MUT_ONLY="$NJIDS" "${TN[@]}" bash "$V31/run-mutants.sh" "$HK" "$T/wd-NJ13-a$1" > "$T/W13-rerun-a$1.txt" 2>&1; };   outNJ13() { echo "$T/W13-rerun-a$1.txt"; }
runNJSM() { SC_BASH=$B52 MUT_SUITE="$WT" MUT_ONLY="$NJIDS" "${TN[@]}" bash "$V31/run-mutants.sh" "$HK" "$T/wd-NJSM-a$1" > "$T/suite-rerun-a$1.txt" 2>&1; };   outNJSM() { echo "$T/suite-rerun-a$1.txt"; }
runW12()  { TRAFFIC_DIR="$S/traffic-frozen" "${TN[@]}" bash "$V31/run-evidence.sh" "$T/wd-W12-a$1" W12; };   outW12()  { echo "$T/wd-W12-a$1/W12-real-traffic.txt"; }
LAST=''; NJIDS=''
phase() { local p=$1 a f s e rc
  for a in 1 2 3; do
    waitlow || { note "$p NO-LOW-WINDOW-6H"; return 1; }
    f=$(out$p "$a"); note "$p a$a START"
    run$p "$a" > "$T/runs/$p.a$a.log" 2>&1; rc=$?
    s=$(head -1 "$f" 2>/dev/null | grep -oE 'load [0-9.]+' | head -1 | cut -d' ' -f2)
    e=$(tail -1 "$f" 2>/dev/null | grep -oE 'load (at the end )?[0-9.]+' | tail -1 | grep -oE '[0-9.]+$')
    LAST=$f
    if [[ -n "$s" && -n "$e" ]] && ! ge "$s" 2 && ! ge "$e" 2; then note "$p a$a END rc=$rc VALID start=$s end=$e"; return 0; fi
    note "$p a$a END rc=$rc VOID start=${s:-none} end=${e:-none}"
  done
  note "$p VOID-3X"; return 1; }
nj() { awk '$2=="NOT-JUDGED" && $1!="P-0"{print $1}' "$1" 2>/dev/null | paste -sd'|' -; }
phase W9
phase W13; NJIDS=$(nj "$LAST"); [[ -n $NJIDS ]] && { note "W13 NOT-JUDGED other than P-0: $NJIDS"; phase NJ13; cp "$LAST" "$OUTD/W13-mutants-rerun.txt"; }
phase P0v; [[ -f $LAST ]] && cp "$LAST" "$OUTD/W13-P0-v31.txt"
phase P0s; [[ -f $LAST ]] && cp "$LAST" "$OUTD/W13-P0-suite.txt"
phase SM; [[ -f $LAST ]] && cp "$LAST" "$OUTD/W13-suite-mutants.txt"; NJIDS=$(nj "$LAST")
[[ -n $NJIDS ]] && { note "SM NOT-JUDGED other than P-0: $NJIDS"; phase NJSM; cp "$LAST" "$OUTD/W13-suite-mutants-rerun.txt"; }
phase W12
note "DRIVER-END | wt $(git -C "$WT" rev-parse --short HEAD) dirty $(git -C "$WT" status --porcelain | wc -l)"

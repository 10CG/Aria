#!/bin/bash
# watchdog-probe.sh <hook> -- feasibility of a hard deadline (background judge + timer subshell + wait) for #217 v2, bash 3.2 compatible.
# Run it under each bash to test: `<bash> watchdog-probe.sh <hook>`. Prints one line per case; no command text, no secret values.
# slow_regex reproduces a single slow regexec with the hook's own _SG_SRVCFG pattern (extracted at runtime from <hook>) on one long token.
HOOK=${1:?usage: watchdog-probe.sh <hook>}
eval "$(grep -m1 '^_SG_SRVCFG=' "$HOOK")"
slow_loop() { local i=0; while :; do i=$((i+1)); [[ "abc$i" =~ ^abc[0-9]+$ ]]; done; }
slow_regex() { local tok; tok=$(printf '%*s' "$1" '' | tr ' ' a); [[ "$tok" =~ ($_SG_SRVCFG) ]]; return 0; }
fast() { return 0; }
block_inner() { echo "inner-block-reason" >&2; return 2; }
wd_run() {  # wd_run <deadline_s> <fn> [args...]; rc >= 128 => killed at the deadline
  local dl=$1 jp tp rc; shift
  ( "$@" ) &
  jp=$!
  ( sleep "$dl"; kill -KILL "$jp" ) >/dev/null 2>&1 </dev/null &
  tp=$!
  wait "$jp" 2>/dev/null; rc=$?   # 2>/dev/null: silences the shell's "Killed" job notice, which would otherwise land in the block text
  kill -KILL "$tp" >/dev/null 2>&1; wait "$tp" 2>/dev/null
  return $rc
}
now() { date +%s.%N; }
el() { awk -v a="$1" -v b="$2" 'BEGIN{printf "%.3f", b-a}'; }
echo "bash $BASH_VERSION"
t0=$(now); slow_regex 16000; t1=$(now); echo "  baseline: one regexec on a 16000-char token, no watchdog: $(el $t0 $t1)s"
t0=$(now); wd_run 2 slow_loop; rc=$?; t1=$(now); echo "  deadline 2s, endless loop of small builtins: rc=$rc wall=$(el $t0 $t1)s"
t0=$(now); wd_run 2 slow_regex 16000; rc=$?; t1=$(now); echo "  deadline 2s, the single slow regexec: rc=$rc wall=$(el $t0 $t1)s"
t0=$(now); wd_run 3 fast; rc=$?; t1=$(now); echo "  deadline 3s, fast judge: rc=$rc wall=$(el $t0 $t1)s"
t0=$(now); err=$(wd_run 3 block_inner 2>&1); rc=$?; t1=$(now); echo "  deadline 3s, judge blocks itself, read through a pipe: rc=$rc stderr=[$err] pipe EOF after $(el $t0 $t1)s (a timer holding the pipe would make this ~3s)"
err=$(wd_run 1 slow_loop 2>&1); echo "  stderr of a killed judge (must be empty, no job notice): [$err]"
t0=$(now); for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do wd_run 3 fast; done; t1=$(now)
echo "  overhead per wd_run (fork judge + timer): $(awk -v a=$t0 -v b=$t1 'BEGIN{printf "%.4f", (b-a)/20}')s"

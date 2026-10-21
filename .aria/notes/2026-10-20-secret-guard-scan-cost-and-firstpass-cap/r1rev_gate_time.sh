#!/usr/bin/env bash
# The gate alone, in process: source the hook (functions above the sourcing gate) + its risky_patterns, then time _sg_pregate on each input
# (includes _sg_bytelen, both match passes and the sed fork; no first pass). Inputs as in hook-time.sh.
#   bash gate-time.sh <hook> <label> <input name>...
set -u
H="$1"; L="$2"; shift 2
D="$(mktemp -d)"; trap 'rm -rf "$D"' EXIT; export HOME="$D"
source "$H"
awk '/^declare -a risky_patterns=\(/,/^\)$/' "$H" > "$D/rp.sh"; source "$D/rp.sh"
unset SECRET_GUARD_RAW_GATE CLAUDE_PROJECT_DIR
input=""
TIMEFORMAT='%3R'
rd="cat /opt/.e""nv"
rep() { local u="$1" n="$2" s=""; while (( ${#s} < n )); do s="$s$u$u$u$u$u$u$u$u"; done; printf '%s' "$s"; }
cjk=$'\xe4\xb8\xad'
mk() {
  case "$1" in
    c14) local s="$rd"; while (( ${#s} < 14000 )); do s="$s | cat | cat | cat | cat"; done; printf '%s' "$s" ;;
    cjk4000) local p="" i=0; while (( i < 4000 )); do p="$p$cjk"; i=$((i+1)); done; printf '%s' "$rd; echo $p" ;;
    benign60c) local s="echo hi"; while (( ${#s} < 60000 )); do s="$s | cat | cat | cat | cat"; done; printf '%s' "$s" ;;
    benign60s) rep 'echo xxxxxxx; ' 60000 ;;
    adv60curl) printf '%s' "$(rep 'curl ' 60000); $rd" ;;
    adv32env) printf '%s' "python3 -c \"import os; $(rep "x.environ.get('A');" 32000)\"; $rd" ;;
  esac
}
for x in "$@"; do
  command="$(mk "$x")"
  t=$( { time { _sg_pregate "$command" 2>/dev/null; echo "$?" > "$D/rc"; }; } 2>&1 )
  printf '%-10s gate-only %-10s chars=%-6s rc=%s  %ss   (bash %s, LANG=%s, LC_ALL=%s)\n' "$L" "$x" "${#command}" "$(cat "$D/rc")" "$t" "${BASH_VERSION%%(*}" "${LANG:-}" "${LC_ALL:-unset}"
done

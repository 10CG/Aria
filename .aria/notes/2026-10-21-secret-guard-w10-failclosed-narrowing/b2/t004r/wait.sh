#!/usr/bin/env bash
# wait.sh [max s] [lines] : blocks until driver.log says DONE, the driver is gone, or the time is up; then prints the last status lines
T=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/t004r
LOG=$T/driver.log; P=$(cat "$T/driver.pid" 2>/dev/null); end=$((SECONDS + ${1:-575}))
while (( SECONDS < end )); do grep -q 'driver DONE' "$LOG" 2>/dev/null && break; kill -0 "$P" 2>/dev/null || break; sleep 15; done
tail -n "${2:-6}" "$LOG"; printf 'now %s load %s driver %s %s\n' "$(date -u +%T)" "$(cut -d' ' -f1-3 /proc/loadavg)" "$P" "$(kill -0 "$P" 2>/dev/null && echo alive || echo gone)"

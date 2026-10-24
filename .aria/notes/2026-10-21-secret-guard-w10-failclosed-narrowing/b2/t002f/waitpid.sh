#!/usr/bin/env bash
# waitpid.sh <pid> <max seconds> [<log lines>]: waits while <pid> runs (at most <max seconds>), then says whether it still runs and prints the driver log's tail
p=$1; m=$2; t=0
while kill -0 "$p" 2>/dev/null && (( t < m )); do sleep 15; t=$((t+15)); done
if kill -0 "$p" 2>/dev/null; then echo "pid $p still running after ${t}s"; else echo "pid $p gone after ${t}s"; fi
tail -n "${3:-6}" /tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/t002f/drive.log
exit 0

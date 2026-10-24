#!/usr/bin/env bash
D=$(cd "$(dirname "$0")" && pwd); cd "$D"
w=0; while (( w < 60 )); do l=$(cut -d' ' -f1 /proc/loadavg); awk -v l="$l" 'BEGIN{exit !(l<7)}' && break; sleep 5; w=$((w+5)); done
echo "# start $(date -u +%FT%TZ) after waiting ${w}s, load $(cut -d' ' -f1-3 /proc/loadavg)"
echo "######## xp-fo M28 (padding evasion, hook level)"; bash xp-fo.sh M28 M28c 2>&1
echo "######## xp-term (SIGTERM ignored behind timeout)"; bash xp-term.sh M20 M30 2>&1
echo "# end $(date -u +%FT%TZ) load $(cut -d' ' -f1-3 /proc/loadavg)"; echo XP2DONE

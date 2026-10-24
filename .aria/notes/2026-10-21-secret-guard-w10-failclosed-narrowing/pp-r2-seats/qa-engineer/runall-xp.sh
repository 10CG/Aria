#!/usr/bin/env bash
# runall-xp.sh : wait (at most 240 s) for the 1-minute load to drop below 7, then run the consequence demos one after another. Every block prints its own load.
D=$(cd "$(dirname "$0")" && pwd); cd "$D"
w=0; while (( w < 240 )); do l=$(cut -d' ' -f1 /proc/loadavg); awk -v l="$l" 'BEGIN{exit !(l<7)}' && break; sleep 5; w=$((w+5)); done
echo "# start $(date -u +%FT%TZ) after waiting ${w}s, load $(cut -d' ' -f1-3 /proc/loadavg)"
echo "######## xp-fo (hook-level consequences of the fail-open survivors)"; bash xp-fo.sh M24 M17 M18 M28 M28c 2>&1
echo "######## xp-ext (extension projects)"; taskset -c 0,1 nice -n 19 bash xp-ext.sh 2>&1
echo "######## xp-term (SIGTERM ignored)"; bash xp-term.sh M20 M30 2>&1
echo "######## xp-tick (SECONDS tick phase sweep over the V3-E5 invocation)"; bash xp-tick.sh 2>&1
echo "# end $(date -u +%FT%TZ) load $(cut -d' ' -f1-3 /proc/loadavg)"; echo XPDONE

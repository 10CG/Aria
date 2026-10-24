#!/usr/bin/env bash
# lowload.sh OUT : the timing batch (INV-7) -- each round starts only when the one-minute load is below START_MAX (default 1.5, headroom under 2, since the
# round itself adds load), and is repeated (up to 3 tries) until sc-cases.sh reports "timing batch: judged" (start < 2 and end < 2). One round at a time.
V=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31; S=$(cd "$(dirname "$0")" && pwd)
O=$1; mkdir -p "$O"; SM=${START_MAX:-1.5}; WAITMAX=${WAITMAX:-5400}
lt() { awk -v a="$1" -v b="$2" 'BEGIN{exit !(a+0 < b+0)}'; }
waitlow() { local t=0; until lt "$(cut -d' ' -f1 /proc/loadavg)" "$SM"; do sleep 10; t=$((t+10)); (( t >= WAITMAX )) && { echo "$(date -u +%T) gave up waiting: load $(cat /proc/loadavg)" >> "$O/log"; return 1; }; done; }
round() {   # TAG CMD... : runs the round until its timing batch was judged (3 tries)
  local tag=$1 k; shift
  for k in 1 2 3; do
    waitlow || return 1
    echo "$(date -u +%T) start $tag try $k load $(cat /proc/loadavg)" >> "$O/log"
    "$@" > "$O/$tag.try$k.txt" 2>&1
    echo "$(date -u +%T) end   $tag try $k load $(cat /proc/loadavg) | $(grep -o 'timing batch: [^|]*' "$O/$tag.try$k.txt" | sort | uniq -c | tr '\n' ' ') | $(grep -E '^# totals|caught' "$O/$tag.try$k.txt" | tail -2 | tr '\n' ' ')" >> "$O/log"
    if ! grep -q 'timing batch: SKIP\|timing batch: void' "$O/$tag.try$k.txt"; then cp "$O/$tag.try$k.txt" "$O/$tag.txt"; return 0; fi
  done
}
for b in /usr/bin/bash /home/dev/.aria/tools/bash-5.0.18/bash /home/dev/.aria/tools/bash-5.1.16/bash /home/dev/.aria/tools/bash-5.3.20/bash /home/dev/.aria/tools/bash-3.2.57/bash; do
  tag=impl-$(basename "$(dirname "$b")"); [[ $b == /usr/bin/bash ]] && tag=impl-bash-5.2.15
  round "$tag" env SC_BASH="$b" taskset -c 0,1 nice -n 19 bash "$V/sc-cases.sh" "$S/work/impl.sh" || break
done
round base-bash-5.2.15 env SC_BASH=/usr/bin/bash taskset -c 0,1 nice -n 19 bash "$V/sc-cases.sh" "$S/work/base.sh"
round mut-timing env MUT_ONLY='BI-(2|6|7|13|14|15)' SC_BASH=/usr/bin/bash bash "$V/run-mutants.sh" "$S/work/impl.sh" "$O/mut"
round p0-full env SC_BASH=/usr/bin/bash taskset -c 0,1 nice -n 19 bash "$V/sc-cases.sh" "$S/runs/pert-det/mut/P-0.sh"
echo "$(date -u +%T) done" >> "$O/log"

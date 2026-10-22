#!/usr/bin/env bash
# run-w12b.sh <work dir with v3.sh> : a second, independent replay of the 138 W1 commands on the same prototype (load-dependence of the outcome near the deadline)
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; W=$1; : "${TRAFFIC_DIR:?}"
W1="$(cd "$HERE/.." && pwd)/evidence/W1-classification.tsv"
{ printf '# %s | %s | bash %s | load %s\n' "$(date -u +%FT%TZ)" "$(uname -sr)" "$BASH_VERSION" "$(cut -d' ' -f1-3 /proc/loadavg)"
  echo "## second replay of the 138 W1 commands, v3 prototype, bash 5"
  taskset -c 0,1 nice -n 19 bash "$HERE/replay138.sh" "$W/v3.sh" "$W1" "$HERE/W12b-replay-138.tsv" 2>&1 | grep -v setlocale
  awk -F'\t' '{c[$3]++} END{for (k in c) printf "  outcome %-10s %d\n", k, c[k]}' "$HERE/W12b-replay-138.tsv" | sort
  awk -F'\t' '$3=="allow"{print $4}' "$HERE/W12b-replay-138.tsv" | sort -n | awk '{a[NR]=$1} END{printf "  allow wall (s): n=%d p50=%.2f p90=%.2f p99=%.2f max=%.2f\n", NR, a[int(NR*.5)], a[int(NR*.9)], a[int(NR*.99)], a[NR]}'
  echo "## commands whose outcome differs between the two replays (W12-replay-138.tsv vs W12b-replay-138.tsv)"
  awk -F'\t' 'NR==FNR{o[$1]=$3; w[$1]=$4; next} o[$1]!=$3 {printf "  n=%s run1=%s (%ss) run2=%s (%ss)\n", $1, o[$1], w[$1], $3, $4; d++} END{printf "  differing: %d\n", d+0}' "$HERE/W12-replay-138.tsv" "$HERE/W12b-replay-138.tsv"
  printf '# end %s | load %s\n' "$(date -u +%FT%TZ)" "$(cut -d' ' -f1-3 /proc/loadavg)"; } > "$HERE/W12b-rerun.txt"
echo done

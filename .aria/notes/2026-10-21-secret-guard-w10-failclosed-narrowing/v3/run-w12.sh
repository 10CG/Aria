#!/usr/bin/env bash
# run-w12.sh <work dir with base.sh + v3.sh from run-w10-w11.sh> <bash 3.2 binary> : real-traffic evidence, aggregates only (TRAFFIC_DIR = the frozen corpus, outside the repo)
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; W=$1; B32=$2; : "${TRAFFIC_DIR:?}"
NOTES="$(cd "$HERE/.." && pwd)"; W1="$NOTES/evidence/W1-classification.tsv"
hdr() { printf '# %s | %s | bash %s | load %s\n' "$(date -u +%FT%TZ)" "$(uname -sr)" "$BASH_VERSION" "$(cut -d' ' -f1-3 /proc/loadavg)"; }
{ hdr
  echo "## 1. the W10 size-blocked class (W1: 138 commands; the baseline blocks all of them for size), v3 prototype, bash 5"
  taskset -c 0,1 nice -n 19 bash "$HERE/replay138.sh" "$W/v3.sh" "$W1" "$HERE/W12-replay-138.tsv" 2>&1 | grep -v setlocale
  awk -F'\t' '{c[$3]++} END{for (k in c) printf "  outcome %-10s %d\n", k, c[k]}' "$HERE/W12-replay-138.tsv" | sort
  awk -F'\t' 'NR==FNR{cls[$1]=$5; next} {printf "  W1 class %-6s -> %s\n", cls[$1], $3}' "$W1" "$HERE/W12-replay-138.tsv" | sort | uniq -c
  awk -F'\t' '$3=="allow"{print $4}' "$HERE/W12-replay-138.tsv" | sort -n | awk '{a[NR]=$1} END{printf "  allow wall (s): n=%d p50=%.2f p90=%.2f p99=%.2f max=%.2f\n", NR, a[int(NR*.5)], a[int(NR*.9)], a[int(NR*.99)], a[NR]}'
  echo "## 2. outside the class: rc + sha256(stderr) of base vs v3 on 300 sampled commands (baseline allow/finding under 1 s; list: ident-300.lst), bash 5"
  taskset -c 0,1 nice -n 19 bash "$HERE/ident.sh" "$W/base.sh" "$W/v3.sh" "$HERE/ident-300.lst" 2>&1 | grep -v setlocale | tail -3
  echo "## 3. bash 3.2 (no EPOCHREALTIME -> no relaxation): base vs v3 on 40 sampled W1 commands (list: w1-sample40.lst)"
  taskset -c 0,1 nice -n 19 bash "$HERE/ident32.sh" "$B32" "$W/base.sh" "$W/v3.sh" "$HERE/w1-sample40.lst" 2>&1 | grep -v setlocale | tail -3
  hdr; } > "$HERE/W12-real-traffic.txt"
echo done

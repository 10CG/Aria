#!/bin/bash
# prove.sh HOOKDIR-OF-BAD HELPER REALHOOK : the V15 cases on the real hook (5.2 relax, 3.2 norelax) and on each bad hook (5.2 relax)
D=$1; HL=$2; RH=$3; B32=/home/dev/.aria/tools/bash-3.2.57/bash
row() { printf '%-22s ' "$1"; SC_ONLY='^V15-' taskset -c 0,1 nice -n 19 "$2" "$HL" "$3" "$4" 2>/dev/null | awk '$2 ~ /^V15-/ {n[$1]++; if ($1 != "PASS") { m=$0; t=""; while (match(m, /\[[a-z-]+\]/)) { t=t substr(m, RSTART, RLENGTH); m=substr(m, RSTART+RLENGTH) }; f=f " " $1 ":" substr($2,1,8) t } } END { for (k in n) printf "%s=%d ", k, n[k]; print "|" f }'; }
row real-5.2-relax bash "$RH" relax
row real-3.2-norelax $B32 "$RH" norelax
for b in "$D"/B*.sh; do row "$(basename "$b" .sh)" bash "$b" relax; done

#!/usr/bin/env bash
# chain.sh -- the six rounds of step 6, one after another (one heavy experiment at a time)
OUT=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/t002d
echo "chain pid $$ $(date -u +%FT%TZ)" > "$OUT/chain.meta"
bash "$OUT/run1.sh" b-usr SC_BASH=/usr/bin/bash SG_W10_LOG="$OUT/b-usr.w10log"
for v in 5.0.18 5.1.16 5.3.20 3.2.57; do
  bash "$OUT/run1.sh" "b-$v" SC_BASH="/home/dev/.aria/tools/bash-$v/bash" SG_W10_LOG="$OUT/b-$v.w10log"
done
bash "$OUT/run1.sh" wsl WSL_DISTRO_NAME=Ubuntu SG_W10_LOG="$OUT/wsl.w10log"
echo "ALLDONE $(date -u +%FT%TZ)" >> "$OUT/chain.meta"
exit 0

#!/usr/bin/env bash
# t004w3 driver (main loop, 2026-10-28): W9 on the final hook 628652570ce3, INV-7 unchanged (start < 1.2, end < 2).
# The host has had a standing external load of ~0.9-1.2 for three days, so a two-core W9 (its own contribution ~1.6)
# cannot end below 2 unless the host is nearly idle. Two attempt kinds, criteria identical:
#   A (two cores, SC_TASKSET unset)   when 1-min < 0.50 and 5-min < 0.90
#   B (one core,  SC_TASKSET="-c 0")  when 1-min < 0.90 and 5-min < 1.10  (a gentler run of the same stage; outcomes must match the stable content, else void)
# Checks every 10 min, at most 100 attempts, self-stops by 2026-11-01T00:00Z. A valid output is copied into v31/impl; a void one never is.
set -u
SP=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad; D=$SP/r217impl/t004w3
V=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31; IMPLDIR=$V/impl
HOOK=$SP/r217impl/t004w/hook-final.sh; B32=/home/dev/.aria/tools/bash-3.2.57/bash; LOG=$D/driver.log
DEADLINE=1793491200
echo $$ > $D/driver.pid
ld() { cut -d' ' -f1-3 /proc/loadavg; }
note() { echo "$(date -u +%FT%TZ) $* | load $(ld)" >> "$LOG"; }
[[ "$(sha256sum < "$HOOK" | cut -c1-12)" == 628652570ce3 ]] || { note "hook copy is not 628652570ce3: stop"; exit 3; }
note "driver start (pid $$)"
ok=0
for a in $(seq 1 100); do
  (( $(date -u +%s) >= DEADLINE )) && { note "deadline reached, stopping"; break; }
  kind=; read -r m1 m5 m15 _ < /proc/loadavg
  if awk -v a="$m1" -v b="$m5" 'BEGIN{exit !(a < 0.50 && b < 0.90)}'; then kind=A; TS=();
  elif awk -v a="$m1" -v b="$m5" 'BEGIN{exit !(a < 1.00 && b < 1.15)}'; then kind=B; TS=("SC_TASKSET=-c 0");
  else sleep 600; continue; fi
  A=$D/W9.$a.$kind; mkdir -p "$A/wd"; note "W9 attempt $a kind $kind start"
  env "${TS[@]}" OUT=$A IMPL=$HOOK BASH32=$B32 taskset -c 0,1 nice -n 19 bash "$V/run-evidence.sh" "$A/wd" W9 > "$A/stdout.txt" 2>&1; rc=$?
  s=$(head -1 "$A/W9-suite.txt" 2>/dev/null | grep -oE 'load [0-9.]+' | head -1 | cut -d' ' -f2); e=$(tail -1 "$A/W9-suite.txt" 2>/dev/null | grep -oE 'load [0-9.]+' | tail -1 | cut -d' ' -f2)
  base=$(grep -cE '^PASS: 813 / 814' "$A/W9-suite.txt" 2>/dev/null); impl=$(grep -cE '^PASS: 807 / 814' "$A/W9-suite.txt" 2>/dev/null)
  if [[ $rc == 0 && -n "$s" && -n "$e" ]] && awk -v s="$s" -v e="$e" 'BEGIN { exit !(s < 1.2 && e < 2) }' && [[ $base == 1 && $impl == 1 ]]; then
    cp "$A/W9-suite.txt" "$IMPLDIR/W9-suite.txt"; note "W9 attempt $a kind $kind VALID: start $s end $e, content matches (base 813/814, impl 807/814): copied"; ok=1; break
  else
    note "W9 attempt $a kind $kind VOID: rc=$rc start ${s:-?} end ${e:-?} base ${base:-?}/1 impl ${impl:-?}/1"
  fi
  sleep 300   # a cooldown after a void attempt: never burn the attempt budget inside one second
done
note "driver end: W9 valid=$ok"

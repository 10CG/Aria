#!/usr/bin/env bash
V=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31
cd "$(dirname "$0")"
for m in TL-M1 TL-M2 TL-M3 TL-M4 TL-M5 TL-M6 TL-M7 TL-M8 TL-M9 TL-M10; do
  echo "=== $m start $(date -u +%T) load $(cut -d' ' -f1-3 /proc/loadavg)"
  bash $V/sc-cases.sh mut/$m.sh ./base.sh > mutres-$m.txt 2>&1; echo "rc=$?" >> mutres-$m.txt
  echo "=== $m end $(date -u +%T) load $(cut -d' ' -f1-3 /proc/loadavg) $(grep -c '^FAIL' mutres-$m.txt) FAIL: $(grep '^FAIL' mutres-$m.txt | awk '{print $2}' | tr '\n' ' ')"
done

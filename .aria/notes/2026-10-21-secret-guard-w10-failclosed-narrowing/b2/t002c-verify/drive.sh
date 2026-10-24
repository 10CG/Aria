#!/usr/bin/env bash
set -u
SP=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad
W=$SP/wt217/aria; V=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31
O=$SP/r217impl/verify3a; T=/home/dev/.aria/tools
waitlow() { local t=0 l; while :; do l=$(cut -d' ' -f1 /proc/loadavg); awk -v l="$l" 'BEGIN{exit !(l<1.2)}' && return 0
  (( t >= 1800 )) && { log "waitlow gave up at $l"; return 0; }; sleep 20; t=$((t+20)); done; }
log() { printf '%s %s | load %s\n' "$(date -u +%T)" "$*" "$(cut -d' ' -f1-3 /proc/loadavg)" >> "$O/drive.log"; }
declare -A B=([5.2]=/usr/bin/bash [5.0]=$T/bash-5.0.18/bash [5.1]=$T/bash-5.1.16/bash [5.3]=$T/bash-5.3.20/bash [3.2]=$T/bash-3.2.57/bash)
for v in 5.2 5.0 5.1 5.3 3.2; do
  waitlow; log "R1 w10 $v start"
  ( cd "$W" && SC_BASH=${B[$v]} SG_W10_ONLY=. SG_W10_LOG=$O/w10-$v.log taskset -c 0,1 nice -n 19 bash hooks/tests/secret-guard.test.sh > $O/w10-$v.txt 2>&1 ); log "R1 w10 $v end rc=$?"
done
waitlow; log "R2 sc-cases start"
bash $V/sc-cases.sh "$W/hooks/secret-guard.sh" > $O/sc-cases-5.2.txt 2>&1; log "R2 sc-cases end rc=$?"
python3 $V/mutants.py "$W/hooks/secret-guard.sh" $O/mut > $O/mutants.log 2>&1 || log "mutants.py failed"
for b in BI-8 BI-5 BI-45 BI-24 BI-7 BI-11; do
  cases=$(awk -F'\t' -v i=$b '$1==i {print $2}' $O/mut/designated.tsv); re="^($(tr ' ' '|' <<< "$cases"))\$"
  waitlow; log "R4 $b start ($cases)"
  SG_W10_ONLY="$re" SG_W10_LOG=$O/mut-$b.log bash $V/run-suite.sh "$W" $O/mut/$b.sh $O/copies > $O/mut-$b.txt 2>&1; log "R4 $b end rc=$?"
done
waitlow; log "R4 ctl start"
SG_W10_ONLY='^(V9-E12-vmax-unchanged|V2-G4-extension-file-with-entry|V2-E9-extension-project|V6-S20-segment-fallback-text|V2-G12-segment-trigger-asks-gate|V6-E2-deadline-fallback-bytes|V10-N3-environ-big-judge|V11-S4-one-rule-loop)$' \
  SG_W10_LOG=$O/ctl-impl.log bash $V/run-suite.sh "$W" "$W/hooks/secret-guard.sh" $O/copies > $O/ctl-impl.txt 2>&1; log "R4 ctl end rc=$?"
waitlow; log "R3 full 5.2 start"
( cd "$W" && SG_W10_LOG=$O/full-5.2.log taskset -c 0,1 nice -n 19 bash hooks/tests/secret-guard.test.sh > $O/full-5.2.txt 2>&1 ); log "R3 full 5.2 end rc=$?"
log done

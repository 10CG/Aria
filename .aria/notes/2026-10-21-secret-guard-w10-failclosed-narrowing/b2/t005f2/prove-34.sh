#!/bin/bash
S=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad; O=$S/r217impl/t005f2; W=$S/wt217/aria; V=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31
T=(taskset -c 0,1 nice -n 19); HL=$W/hooks/tests/lib/secret-guard-w10-direct.sh; BASE=$O/cs/hook-59e333c.sh
echo "load0 $(cut -d' ' -f1-3 /proc/loadavg)"
for h in $W/hooks/secret-guard.sh $O/bad/B5-anchor-in-job.sh $O/bad/B7-anchor-in-run.sh $O/bad/B8-anchor-in-gate.sh; do
  for x in "$HL" "$V/sc-direct.sh"; do
    r=$(SC_ONLY='^V15-T2' "${T[@]}" bash "$x" "$h" relax "$BASE" 2>/dev/null | grep ' V15-T2-' | head -1)
    printf 'T2 %-22s %-26s %s\n' "$(basename "$h" .sh)" "$(basename "$x")" "$(cut -c1-12 <<< "$r" | awk '{print $1}') $(grep -o 'saw _SG_LEFT \[[^]]*\]' <<< "$r") $(grep -o '\[[a-z]*\]$\|\[static\] \[value\]$' <<< "$r")"
  done
done
rm -rf "$O/inv4"; mkdir -p "$O/inv4"; cp -a "$W/hooks" "$O/inv4/"; cp "$O/bad/B10-nowslfs-below-gate.sh" "$O/inv4/hooks/secret-guard.sh"; cp "$O/pre/suite-5f.sh" "$O/inv4/hooks/tests/suite-5f.sh"
s1() { grep -E "V11-S1-above-gate" | awk '{printf "%s:%s ", $1, $2}' | sed 's/V11-S1-above-gate://g'; echo; }
echo "sc-cases new  real: $(SC_ONLY='^V11-S1' SC_DIRECT=0 "${T[@]}" bash "$V/sc-cases.sh" "$W/hooks/secret-guard.sh" "$BASE" 2>&1 | s1)"
echo "sc-cases new  B10 : $(SC_ONLY='^V11-S1' SC_DIRECT=0 "${T[@]}" bash "$V/sc-cases.sh" "$O/bad/B10-nowslfs-below-gate.sh" "$BASE" 2>&1 | s1)"
echo "sc-cases 5f   B10 : $(SC_ONLY='^V11-S1' SC_DIRECT=0 "${T[@]}" bash "$O/pre/sc-cases-5f.sh" "$O/bad/B10-nowslfs-below-gate.sh" "$BASE" 2>&1 | s1)"
echo "suite    new  real: $(SG_W10_ONLY='^V11-S1' "${T[@]}" bash "$W/hooks/tests/secret-guard.test.sh" 2>&1 | s1)"
echo "suite    new  B10 : $(SG_W10_ONLY='^V11-S1' "${T[@]}" bash "$O/inv4/hooks/tests/secret-guard.test.sh" 2>&1 | s1)"
echo "suite    5f   B10 : $(SG_W10_ONLY='^V11-S1' "${T[@]}" bash "$O/inv4/hooks/tests/suite-5f.sh" 2>&1 | s1)"
echo "load1 $(cut -d' ' -f1-3 /proc/loadavg)"

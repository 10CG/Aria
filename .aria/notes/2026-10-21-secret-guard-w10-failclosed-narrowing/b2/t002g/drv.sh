#!/usr/bin/env bash
# drv.sh <step> [args] : scratch driver of TASK-002 3d (10CG/aria-plugin#217); in no repo. One heavy experiment at a time, taskset -c 0,1 nice -n 19.
set -u
V=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing
V31=$V/v31
WT=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/wt217/aria
OUT=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/t002g
IMPL=$WT/hooks/secret-guard.sh
TS=(taskset -c 0,1 nice -n 19)
mkdir -p "$OUT/tmp"
la() { cut -d' ' -f1-3 /proc/loadavg; }
waitload() {   # [max seconds] : wait while the one-minute load is above 1.2; 0 once it is not, 1 when the wait ran out
  local max=${1:-${WAITMAX:-480}} n=0
  while awk '{exit !($1 > 1.2)}' /proc/loadavg; do
    if (( n >= max )); then echo "WAIT: load still above 1.2 after ${n} s: $(la)"; return 1; fi
    sleep 10; n=$((n + 10))
  done
  echo "WAIT: ${n} s, load $(la)"
  return 0
}
norm() { sed -E 's/[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z/<time>/g; s/[0-9]+\.[0-9]{2} [0-9]+\.[0-9]{2} [0-9]+\.[0-9]{2}/<load>/g' "$1"; }
case $1 in
  s0)
    cp "$V31/run-mutants.sh" "$OUT/run-mutants.orig.sh"
    waitload || exit 4
    echo "s0a start $(la)"; MUT_ONLY='BI-8' "${TS[@]}" bash "$V31/run-mutants.sh" "$IMPL" "$OUT/s0-v31" > "$OUT/s0-v31.txt" 2>&1; echo "s0a exit $? end $(la)"
    echo "BI-8.sh sha256 $(sha256sum < "$OUT/s0-v31/mut/BI-8.sh" | cut -c1-12)"
    waitload || exit 4
    echo "s0b start $(la)"; SG_W10_ONLY='^(V9-E12-vmax-unchanged)$' SG_W10_LOG="$OUT/s0-suite.log" "${TS[@]}" bash "$V31/run-suite.sh" "$WT" "$OUT/s0-v31/mut/BI-8.sh" "$OUT/tmp" > "$OUT/s0-suite.txt" 2>&1; echo "s0b exit $? end $(la)"
    cut -c1-260 "$OUT/s0-v31.txt"; echo '-- suite log'; cut -c1-300 "$OUT/s0-suite.log"; tail -1 "$OUT/s0-suite.txt" ;;
  ba)   # before|after : the script as it is now, without MUT_SUITE, MUT_ONLY='BI-8|BI-24'
    waitload || exit 4
    echo "$2 start $(la)"; MUT_ONLY='BI-8|BI-24' "${TS[@]}" bash "$V31/run-mutants.sh" "$IMPL" "$OUT/$2" > "$OUT/$2.txt" 2>&1; echo "$2 exit $? end $(la)"
    cut -c1-200 "$OUT/$2.txt"
    if [[ -f "$OUT/before.txt" && -f "$OUT/after.txt" ]]; then
      if diff <(norm "$OUT/before.txt") <(norm "$OUT/after.txt") > "$OUT/before-after.diff"; then echo 'before/after: identical apart from times and loads'
      else echo 'before/after: DIFFERENT'; head -20 "$OUT/before-after.diff" | cut -c1-200; fi
    fi ;;
  install)
    bash -n "$OUT/run-mutants.new.sh" || exit 6
    cp "$OUT/run-mutants.new.sh" "$V31/run-mutants.sh"
    diff "$OUT/run-mutants.orig.sh" "$V31/run-mutants.sh" > "$OUT/run-mutants.diff"; echo "diff lines: $(wc -l < "$OUT/run-mutants.diff")"; wc -l < "$V31/run-mutants.sh"; ls -l "$V31/run-mutants.sh" ;;
  refcheck)   # REFIDS in run-mutants.sh against the suite's sg_w10_ref table and the helper's fbref
    S=$WT/hooks/tests/secret-guard.test.sh; HL=$WT/hooks/tests/lib/secret-guard-w10-direct.sh
    tab=$( { sed -n '/^sg_w10_ref() {/,/^}/p' "$S"; sed -n '/fbref() {/,/^ *}/p' "$HL"; } | grep -oE '^ +[A-Za-z0-9|:.-]+\) echo' | sed -E 's/^ +//; s/\) echo$//' | tr '|' '\n' | sort)
    mine=$(grep -oE "^REFIDS\+?='[^']*'" "$V31/run-mutants.sh" | sed -E "s/^REFIDS\+?='//; s/'$//" | tr ' ' '\n' | grep -v '^$' | sort)
    echo "table: $(wc -l <<< "$tab") ids; REFIDS: $(wc -l <<< "$mine") ids"
    diff <(echo "$tab") <(echo "$mine") && echo 'REFIDS == sg_w10_ref ids + fbref ids' ;;
  smoke)
    waitload || exit 4
    echo "smoke start $(la)"; MUT_SUITE="$WT" MUT_ONLY="${2:-BI-8}" "${TS[@]}" bash "$V31/run-mutants.sh" "$IMPL" "$OUT/smoke" > "$OUT/smoke.txt" 2>&1; echo "smoke exit $? end $(la)"
    cut -c1-300 "$OUT/smoke.txt" ;;
  all)
    rm -f "$OUT/all.exit"
    waitload 1800 || { echo "all: no low-load window in 30 min" > "$OUT/all.exit"; exit 4; }
    echo "all start $(la) $(date -u +%FT%TZ)" > "$OUT/all.loads"
    MUT_SUITE="$WT" "${TS[@]}" bash "$V31/run-mutants.sh" "$IMPL" "$OUT/all" > "$OUT/all.txt" 2>&1; rc=$?
    echo "all end $(la) $(date -u +%FT%TZ)" >> "$OUT/all.loads"; echo "all exit $rc" > "$OUT/all.exit" ;;
  rerun)   # REGEX NAME : suite mode on those ids only
    waitload || exit 4
    echo "$3 start $(la)"; MUT_SUITE="$WT" MUT_ONLY="$2" "${TS[@]}" bash "$V31/run-mutants.sh" "$IMPL" "$OUT/$3" > "$OUT/$3.txt" 2>&1; echo "$3 exit $? end $(la)"
    cut -c1-300 "$OUT/$3.txt" | head -20 ;;
  env)   # e1 | e1b | e2 ... : the two environment errors on the suite (SG_W10_ONLY=.), hook = the implementation
    mkdir -p "$OUT/env"
    for e in "${@:2}"; do
      sb=''; A=$WT
      case $e in
        e1)  sb="$OUT/env/nope/bash"; rm -rf "$OUT/env/nope" ;;
        e1b) sb="$OUT/env/bash-not-here"; rm -f "$sb" ;;
        e2)  A="$OUT/env/e2-aria"; rm -rf "$A"; mkdir -p "$A"; cp -a "$WT/hooks" "$A/hooks"
             HC="$A/hooks/tests/lib/secret-guard-w10-direct.sh"
             n=$(awk 'NR > 1 && $0 !~ /^[[:space:]]*(#|$)/ {print NR; exit}' "$HC"); sed -i "${n}i exit 7" "$HC"
             echo "e2: helper line 1 [$(sed -n 1p "$HC" | cut -c1-40)]; 'exit 7' inserted as line $n, before [$(sed -n "$((n + 1))p" "$HC" | cut -c1-80)]" ;;
      esac
      waitload || exit 4
      echo "$e start $(la)"
      if [[ -n $sb ]]; then SC_BASH="$sb" SG_W10_ONLY=. SG_W10_LOG="$OUT/env/$e.log" "${TS[@]}" bash "$V31/run-suite.sh" "$A" "$A/hooks/secret-guard.sh" "$OUT/tmp" > "$OUT/env/$e.txt" 2>&1; rc=$?
      else SG_W10_ONLY=. SG_W10_LOG="$OUT/env/$e.log" "${TS[@]}" bash "$V31/run-suite.sh" "$A" "$A/hooks/secret-guard.sh" "$OUT/tmp" > "$OUT/env/$e.txt" 2>&1; rc=$?; fi
      echo "== $e: exit $rc | $(head -1 "$OUT/env/$e.txt" | grep -o 'SC_BASH [^|]*') | log states: $(awk '$1 != "#" {print $1}' "$OUT/env/$e.log" 2>/dev/null | sort | uniq -c | tr -s ' \n' ' ') | end $(la)"
      grep -E '^(FAIL|PASS|SKIP) V0-H[12]' "$OUT/env/$e.log" 2>/dev/null | cut -c1-330
      grep -E 'FAIL|PASS' "$OUT/env/$e.txt" | grep -iE 'summary|total|passed|failed' | tail -2 | cut -c1-200; tail -1 "$OUT/env/$e.txt" | cut -c1-160
    done ;;
  base)
    mkdir -p "$OUT/base"; BH="$OUT/base/secret-guard.59e333c.sh"
    git -C "$WT" show 59e333c:hooks/secret-guard.sh > "$BH" || exit 5
    p=$(sha256sum < "$BH" | cut -c1-12); [[ $p == e83c5e30f2cc ]] || { echo "INV-9: base prefix $p, want e83c5e30f2cc"; exit 5; }
    echo "INV-9: base prefix $p ok"
    waitload || exit 4
    echo "base start $(la)"; SG_W10_ONLY=. SG_W10_LOG="$OUT/base/base.log" "${TS[@]}" bash "$V31/run-suite.sh" "$WT" "$BH" "$OUT/tmp" > "$OUT/base/base.txt" 2>&1; echo "base exit $? end $(la)"
    bash "$0" basecmp ;;
  basecmp)
    B=$V/b2/t002b-verify/base-5.2.15.txt; L=$OUT/base/base.log
    tag() { awk '$1 != "#" { t = "-"; s = $0; while (match(s, /\[[a-z][a-z0-9-]*\]/)) { t = substr(s, RSTART, RLENGTH); s = substr(s, RSTART + RLENGTH) } print $2, $1, t }' "$1" | sort; }
    join -a1 -a2 -e NONE -o 0,1.2,1.3,2.2,2.3 <(tag "$B") <(tag "$L") > "$OUT/base/align.txt"
    echo "aligned ids: $(wc -l < "$OUT/base/align.txt")"
    awk '{ v = ($2 == "MISSING") ? "FAIL" : $2; if (v != $4) print "STATE", $0 }' "$OUT/base/align.txt" > "$OUT/base/diff-state.txt"
    awk '$2 == "MISSING" && $5 != "[missing]" {print "MISSING-not-[missing]", $0} $2 == "FAIL" && $4 == "FAIL" && $3 != $5 {print "TAG", $0}' "$OUT/base/align.txt" > "$OUT/base/diff-tag.txt"
    echo "state differences: $(wc -l < "$OUT/base/diff-state.txt"); tag differences: $(wc -l < "$OUT/base/diff-tag.txt")"
    head -20 "$OUT/base/diff-state.txt" | cut -c1-200; head -20 "$OUT/base/diff-tag.txt" | cut -c1-200
    echo "suite log states: $(awk '$1 != "#" {print $1}' "$L" | sort | uniq -c | tr -s ' \n' ' '); [missing] $(grep -c '\[missing\]' "$L"); [reference] $(grep -c '\[reference\]' "$L")"; tail -1 "$L"
    R="$OUT/all/mut/reasons.tsv"; [[ -f $R ]] || R="$OUT/smoke/mut/reasons.tsv"
    while IFS=$'\t' read -r i c rx; do   # a FAIL [missing] must never count as caught: no listed regex may match the [missing] detail of its case
      d=$(awk -v c="$c" '$2 == c && $1 == "FAIL" {$1 = ""; $2 = ""; print; exit}' "$L")
      [[ $d == *'[missing]'* ]] && grep -qE -- "$rx" <<< "$d" && echo "reasons.tsv $i $c: regex [$rx] matches the [missing] detail"
    done < "$R"
    awk -F'\t' '$3 == "" {print "empty regex:", $1, $2}' "$R"; echo "reasons.tsv rows checked: $(wc -l < "$R") ($R)" ;;
  batch)   # all, then env e1 e1b e2, then base; one after the other
    echo $$ > "$OUT/batch.pid"; rm -f "$OUT/batch.done"; export WAITMAX=1800
    bash "$0" all; bash "$0" env e1 e1b e2 > "$OUT/env.out" 2>&1; bash "$0" base > "$OUT/base.out" 2>&1
    echo "batch done $(date -u +%FT%TZ) load $(la)" > "$OUT/batch.done" ;;
  wait)   # [max seconds] : poll for the batch's end
    n=0; while [[ ! -f "$OUT/batch.done" ]] && (( n < ${2:-540} )); do sleep 20; n=$((n + 20)); done
    if [[ -f "$OUT/batch.done" ]]; then cat "$OUT/batch.done"; else echo "batch not done after $n s"; fi
    echo "all.txt: $(grep -cE '^(BI|P)-' "$OUT/all.txt" 2>/dev/null) result lines; not CAUGHT/GREEN: $(grep -E '^(BI|P)-' "$OUT/all.txt" 2>/dev/null | awk '$2 != "CAUGHT" && $2 != "GREEN" {printf "%s=%s ", $1, $2}'); load $(la)"
    [[ -f "$OUT/all.exit" ]] && cat "$OUT/all.exit"; true ;;
  cmp)   # FILE : per id, the verdict and the designated-case states of FILE against mut-summary.txt
    python3 -I - "$V/b2/t002b-verify/mut-summary.txt" "$2" <<'PY'
import re, sys
def parse(p):
    d = {}
    for line in open(p, encoding='utf-8', errors='replace'):
        m = re.match(r'^((?:BI|P)-\S+)\s+(\S+)', line)
        if not m: continue
        d[m.group(1)] = (m.group(2), re.findall(r'\s(V\d+-[A-Z]\d+\S*?)=(\S+)', line))
    return d
a, b = parse(sys.argv[1]), parse(sys.argv[2])
ref = []
for i in a:
    if i not in b: print(f'{i}: v31 {a[i][0]}, suite: absent'); continue
    va, ta = a[i]; vb, tb = b[i]
    r = [f'{c}={s}' for c, s in tb if s.endswith('[reference]')]
    if r: ref.append(f'{i} {" ".join(r)}')
    if va != vb or ta != tb: print(f'{i}: v31 {va} {" ".join(c + "=" + s for c, s in ta)} | suite {vb} {" ".join(c + "=" + s for c, s in tb)}')
for i in b:
    if i not in a: print(f'{i}: only in the suite run')
print(f'ids: v31 {len(a)}, suite {len(b)}; caught with [reference]: {len(ref)}')
for x in ref: print('  ref:', x)
PY
    ;;
  *) echo "unknown step $1" >&2; exit 2 ;;
esac

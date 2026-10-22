#!/usr/bin/env bash
# sc-cases.sh HOOK [BASE] : the Success Criteria of 10CG/aria-plugin#217 (v3.1 design pin) as executable cases -- the direct-call cases (sc-direct.sh, run by
# SC_BASH), the end-to-end cases (the hook executed by SC_BASH on a JSON input, as Claude Code runs it) and the static checks of the hook text.
# Every e2e case that compares bytes runs the baseline on the same input. Every timing bound comes from a fixed delay injected through shim/ (jq: before the
# trigger point; sed: inside the job's block text), never from the natural speed of the machine.
#   HOOK  the hook under test (the prototype, the implementation, or a bad implementation)
#   BASE  the baseline hook; default: aria 59e333c:hooks/secret-guard.sh. Its sha256 prefix must be e83c5e30f2cc.
#   SC_BASH  the bash that runs the hook (default: bash on PATH). On a GNU/Linux bash 5.0-5.3 the relaxation is expected to be in effect; on any other
#            bash every e2e outcome must equal the baseline's and the gate must stay closed.
#   SC_ONLY  a regex: report only the cases whose id matches.   SC_DIRECT=0  skip the direct cases.   SC_NICE=0  no taskset / nice (default: -c 0,1 / 19).
# Output: one line per case "PASS|FAIL|SKIP <id> <detail>", then the totals. Exit 0 when nothing FAILed, 1 otherwise, 3 on a setup error.
set -u
(( ${BASH_VERSINFO[0]} >= 5 )) || { echo "SETUP: run sc-cases.sh with bash 5 (EPOCHREALTIME); the hook's bash is SC_BASH"; exit 3; }
HERE="$(cd "$(dirname "$0")" && pwd)"
HOOK=$(readlink -f "$1"); BASE=${2:-}
SC_BASH=$(readlink -f "${SC_BASH:-$(command -v bash)}"); SC_ONLY=${SC_ONLY:-.}
REAL_JQ=$(command -v jq); REAL_SED=$(command -v sed)
NICE=(taskset -c 0,1 nice -n 19); [[ "${SC_NICE:-1}" == 0 ]] && NICE=()
W=$(mktemp -d); trap 'rm -rf "$W"' EXIT
if [[ -z "$BASE" ]]; then
  root=$(git -C "$HERE" rev-parse --show-toplevel 2>/dev/null) && git -C "$root/aria" show 59e333c:hooks/secret-guard.sh > "$W/base.sh" 2>/dev/null || { echo "SETUP: cannot extract aria 59e333c:hooks/secret-guard.sh"; exit 3; }
  BASE=$W/base.sh
fi
[[ "$(sha256sum < "$BASE" | cut -c1-12)" == e83c5e30f2cc ]] || { echo "SETUP: BASE is not the baseline hook (sha256 prefix e83c5e30f2cc)"; exit 3; }
read -r MACH MAJ MIN < <("$SC_BASH" -c 'echo "${BASH_VERSINFO[5]} ${BASH_VERSINFO[0]} ${BASH_VERSINFO[1]}"')
RELAX=no; [[ "$MACH" == *-linux-gnu* ]] && (( MAJ == 5 && MIN <= 3 )) && RELAX=yes
printf '# sc-cases.sh | %s | hook sha256 %s | base sha256 %s | SC_BASH %s (%s %s.%s) -> relaxation expected: %s | load %s\n' "$(date -u +%FT%TZ)" \
  "$(sha256sum < "$HOOK" | cut -c1-12)" "$(sha256sum < "$BASE" | cut -c1-12)" "$SC_BASH" "$MACH" "$MAJ" "$MIN" "$RELAX" "$(cut -d' ' -f1-3 /proc/loadavg)"
pass=0 fail=0 skip=0
res() { case $1 in PASS) pass=$((pass+1));; FAIL) fail=$((fail+1));; SKIP) skip=$((skip+1));; esac; printf '%s %s %s\n' "$1" "$2" "$3"; }
sel() { [[ "$1" =~ $SC_ONLY ]]; }
mkdir -p "$W/in"
for s in $(python3 "$HERE/shapes.py" list x); do python3 "$HERE/shapes.py" "$s" "$W/in/$s.txt" && "$REAL_JQ" -Rs '{tool_name:"Bash", tool_input:{command:.}}' < "$W/in/$s.txt" > "$W/in/$s.json"; done
mkdir -p "$W/ext/.aria"; printf '%s\n' "billing/conf/prod.toml" > "$W/ext/.aria/secret-guard.paths"

# ---------------- direct-call cases (sc-direct.sh under SC_BASH) ----------------
if [[ "${SC_DIRECT:-1}" != 0 ]]; then   # the direct cases always run (SC_ONLY filters their lines); SC_DIRECT=0 skips them
  mode=norelax; [[ $RELAX == yes ]] && mode=relax
  while IFS= read -r line; do
    case $line in PASS\ *|FAIL\ *) st=${line%% *}; rest=${line#* }; sel "${rest%% *}" && res "$st" "${rest%% *}" "${rest#* }";; esac
  done < <("${NICE[@]}" "$SC_BASH" "$HERE/sc-direct.sh" "$HOOK" "$mode" 2>/dev/null)
fi

# ---------------- end-to-end cases ----------------
kind() { if grep -q 'has a line longer than' "$1"; then echo longline; elif grep -q 'grows by more than' "$1"; then echo growth
  elif grep -q 'segments together are longer than' "$1"; then echo tmax; elif grep -q 'too large to scan' "$1"; then echo oversize
  elif grep -q 'within the time budget' "$1"; then echo time; elif grep -q 'value-REDACTING filter' "$1"; then echo finding
  elif [[ -s "$1" ]]; then echo other; else echo none; fi; }
run() {   # OUTVAR-PREFIX HOOK SHAPE [VAR=VALUE ...] : runs the hook on the shape -> <prefix>_RC, <prefix>_WALL, <prefix>_ERR (file)
  local p=$1 h=$2 s=$3 st e t0 t1 rc; shift 3
  st=$(mktemp -d -p "$W"); e=$(mktemp -p "$W")
  t0=$EPOCHREALTIME
  env -u CLAUDE_PROJECT_DIR -u _SG_RELAXED -u SECRET_GUARD_TIME_BUDGET_S SC_SHIM_STATE="$st" SC_REAL_jq="$REAL_JQ" SC_REAL_sed="$REAL_SED" "$@" \
    "${NICE[@]}" timeout 12 "$SC_BASH" "$h" < "$W/in/$s.json" >/dev/null 2>"$e"; rc=$?
  t1=$EPOCHREALTIME
  printf -v "${p}_RC" '%s' "$rc"; printf -v "${p}_ERR" '%s' "$e"
  printf -v "${p}_WALL" '%s' "$(awk -v a="${t0/,/.}" -v b="${t1/,/.}" 'BEGIN{printf "%.2f", b-a}')"
}
inr() { awk -v w="$1" -v a="$2" -v b="$3" 'BEGIN{exit !(w>=a && w<=b)}'; }
same() { [[ $H_RC == "$B_RC" ]] && cmp -s "$H_ERR" "$B_ERR"; }
SHIM="PATH=$HERE/shim:$PATH"
desc() { printf 'hook rc=%s %s %ss | base rc=%s %s %ss | stderr %s' "$H_RC" "$(kind "$H_ERR")" "$H_WALL" "$B_RC" "$(kind "$B_ERR")" "$B_WALL" "$(same && echo IDENTICAL || echo DIFFERENT)"; }
identity() {   # ID SHAPE [VAR=VALUE ...] : the hook must equal the baseline, byte for byte
  local id=$1 s=$2; shift 2; sel "$id" || return 0
  run B "$BASE" "$s" "$@"; run H "$HOOK" "$s" "$@"
  if same; then res PASS "$id" "$(desc)"; else res FAIL "$id" "$(desc)"; fi
}
deadline() {   # ID SHAPE MIN MAX [VAR=VALUE ...] : (relaxation expected) the job is cut by the deadline: baseline bytes, wall in [MIN, MAX]
  local id=$1 s=$2 lo=$3 hi=$4; shift 4; sel "$id" || return 0
  if [[ $RELAX != yes ]]; then identity "$id" "$s"; return 0; fi
  run B "$BASE" "$s"; run H "$HOOK" "$s" "$SHIM" "$@"
  if same && inr "$H_WALL" "$lo" "$hi"; then res PASS "$id" "$(desc) (wall window $lo..$hi)"; else res FAIL "$id" "$(desc) (want IDENTICAL, wall window $lo..$hi)"; fi
}
outcome() {   # ID SHAPE WANT_RC WANT_KINDS(|-separated) [VAR=VALUE ...] : (relaxation expected) rc and text kind; otherwise identity
  local id=$1 s=$2 wr=$3 wk=$4 k; shift 4; sel "$id" || return 0
  if [[ $RELAX != yes ]]; then identity "$id" "$s" "$@"; return 0; fi
  run B "$BASE" "$s" "$@"; run H "$HOOK" "$s" "$@"; k=$(kind "$H_ERR")
  if [[ $H_RC == "$wr" && "|$wk|" == *"|$k|"* ]] && inr "$H_WALL" 0 4.5; then res PASS "$id" "$(desc)"; else res FAIL "$id" "$(desc) (want rc=$wr text=$wk within 4.5 s)"; fi
}
# P7 allow path; P3/P6 deadline and fallback bytes (sed stalls the job's block text for 10 s, so only the deadline can end the job)
outcome   V7-E1-benign-big-allowed            benign-big 0 none
deadline  V6-E2-deadline-fallback-bytes       stall-read 2.85 3.6 SC_DELAY_sed=10
deadline  V3-E3-anchor-at-hook-start          stall-read 2.85 3.6 SC_DELAY_jq=1.5 SC_DELAY_sed=10
deadline  V3-E4-cap-3-at-budget-4             stall-read 2.85 3.6 SC_DELAY_sed=10 SECRET_GUARD_TIME_BUDGET_S=4
deadline  V3-E5-budget-1                      stall-read 0.85 1.6 SC_DELAY_sed=10 SECRET_GUARD_TIME_BUDGET_S=1
deadline  V2-E6-flag-from-environment-ignored stall-read 2.85 3.6 SC_DELAY_sed=10 _SG_RELAXED=1
deadline  V2-E7-no-time-left                  stall-read 3.2 4.3 SC_DELAY_jq=3.2
# P2: OSTYPE does not decide; an extension project keeps the baseline
outcome   V2-E8-ostype-from-environment-ignored benign-big 0 none OSTYPE=darwin21
identity  V2-E9-extension-project             ext-read CLAUDE_PROJECT_DIR="$W/ext"
# P9: no count bound in the rerun; TMAX holds in the rerun; VMAX unchanged
outcome   V9-E10-count-axis-read-blocked      count-axis 2 "finding|longline"
outcome   V9-E11-tmax-in-rerun                tmax-rerun 2 tmax
identity  V9-E12-vmax-unchanged               vmax
# P7 routing: by the copy's longest line; multi-line copies get the normal judgement (credit included)
outcome   V7-E13-multiline-copy-normal-text   count-axis-ctl 2 finding
outcome   V7-E14-long-line-from-expansion     longline-expansion 2 longline
if sel V7-E15-credit-as-normal; then
  if [[ $RELAX == yes ]]; then
    run B "$BASE" multiline-credit; run H "$HOOK" multiline-credit
    if [[ $H_RC == 0 ]] || same; then res PASS V7-E15-credit-as-normal "$(desc) (want allowed, or the baseline bytes if the deadline cut it)"
    else res FAIL V7-E15-credit-as-normal "$(desc) (want allowed, or the baseline bytes)"; fi
  else identity V7-E15-credit-as-normal multiline-credit; fi
fi
# P1 sampler: commands that never reach a trigger point
for s in p1-small-benign p1-small-read p1-small-read-filter p1-var-read p1-var-mid p1-var-mid-read; do identity "V1-E16-$s" "$s"; done

# ---------------- static checks of the hook text ----------------
if sel V11; then
  g=$(grep -n '^if \[\[ "${BASH_SOURCE\[0\]}" != "$0" \]\]; then' "$HOOK" | head -1 | cut -d: -f1)
  for f in _sg_vx_big_judge _sg_relax_left _sg_relax_ok _sg_relax_platform _sg_relax_noext _sg_relax_job _sg_relax_run; do
    l=$(grep -n "^$f() {" "$HOOK" | head -1 | cut -d: -f1)
    if [[ -n "$l" && -n "$g" ]] && (( l < g )); then res PASS "V11-S1-above-gate:$f" "line $l < sourcing gate $g"; else res FAIL "V11-S1-above-gate:$f" "line ${l:-missing}, gate ${g:-missing}"; fi
  done
  blk() { awk -v k="$2" '$0 ~ "kind\" == " k " \\]\\]; then" {f=1} f && /^Split it into smaller commands/ {p=1} p {print} p && /请拆成更小的命令/ {exit}' "$1"; }
  o=$(blk "$HOOK" oversize | sed '$d'); l=$(blk "$HOOK" longline | sed '$d'); lz=$(blk "$HOOK" longline | tail -1)
  if [[ -n "$o" && "$o" == "$l" && "$lz" == *请拆成更小的命令 ]]; then res PASS V11-S3-longline-instructions-verbatim "the longline instruction lines equal the oversize ones ($(printf '%s\n' "$l" | wc -l) lines)"
  else res FAIL V11-S3-longline-instructions-verbatim "oversize [$(printf '%s' "$o" | head -c 60)] longline [$(printf '%s' "$l" | head -c 60)]"; fi
  a=$(grep -c 'risky_patterns\[@\]' "$BASE"); b=$(grep -c 'risky_patterns\[@\]' "$HOOK")
  if [[ $a == "$b" ]]; then res PASS V11-S4-one-rule-loop "loops over risky_patterns: $b (baseline $a)"; else res FAIL V11-S4-one-rule-loop "loops over risky_patterns: $b (baseline $a)"; fi
fi
if sel V12; then
  if python3 "$HERE/commentsync.py" --hook-only "$HOOK" target >/dev/null 2>&1; then res PASS V12-C1-hook-comments "commentsync --hook-only target: GREEN"
  else res FAIL V12-C1-hook-comments "commentsync --hook-only target: $(python3 "$HERE/commentsync.py" --hook-only "$HOOK" target 2>&1 | tail -1)"; fi
fi
printf '# totals: PASS %d  FAIL %d  SKIP %d\n' "$pass" "$fail" "$skip"
(( fail == 0 ))

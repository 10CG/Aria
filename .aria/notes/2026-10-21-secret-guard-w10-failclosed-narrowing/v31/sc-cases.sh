#!/usr/bin/env bash
# sc-cases.sh HOOK [BASE] : the Success Criteria of 10CG/aria-plugin#217 as executable cases -- the direct-call cases (sc-direct.sh, run by SC_BASH), the
# end-to-end cases (the hook executed by SC_BASH on a JSON input, as Claude Code runs it) and the static checks of the hook text. v3.2: with the
# post_planning R2 reinforcement (TASK-002 (a)-(f)).
#   HOOK  the hook under test (the implementation, the prototype, a bad implementation, or the baseline itself for its red set)
#   BASE  the baseline hook; default: aria 59e333c:hooks/secret-guard.sh. Its sha256 prefix must be e83c5e30f2cc.
#   SC_BASH  the bash that runs the hook (default: bash on PATH). The relaxation is expected exactly where the gate of What 1 and its supplement opens: an
#            x86_64 GNU/Linux build (BASH_VERSINFO[5] x86_64-*-linux-gnu*) of bash 5.0-5.3, a readable kernel string with no Microsoft, microsoft or WSL in
#            it, and no WSL mark in the file system (wslmark below, the rule of What 1 supplement 2 (v3.4) written apart from the hook's _sg_relax_nowslfs:
#            a mount table that cannot be read or reads empty, or a binfmt_misc topmost at /proc/sys/fs/binfmt_misc whose directory cannot be searched or
#            holds WSLInterop or WSLInterop-late). Every run of the hook clears
#            WSL_DISTRO_NAME and WSL_INTEROP (only the WSL case sets one), and so does sc-direct.sh. On any other bash every e2e outcome must equal the
#            baseline's and the gate must stay closed.
#   SC_ONLY  a regex: run and report only the cases whose id matches.   SC_DIRECT=0  skip the direct cases.   SC_NICE=0  no taskset / nice.
#   SC_LOAD_MAX  the one-minute load below which the timing batch is judged (default 2, INV-7); the header records the value used.
# Timing (INV-7; post_planning R2 PP2-A, B, C). Lower bounds and byte comparisons are always judged. Upper bounds and "the rerun / the job must finish
# before its deadline" are judged only when the one-minute load at the start is below SC_LOAD_MAX; otherwise those cases are SKIP [load], counted on their
# own. When the load at the end is at or over SC_LOAD_MAX, the timing results of a judged batch become SKIP [void]: void, run again (INV-7). A check that
# no load explains (a wrong status, text or byte, a lower bound, a stall that ran to its end) is FAIL under any load -- except that a byte comparison in
# which an arm hit the harness's 12 s timeout, or the guard's own whole-second time budget fired in one arm only (its time text), counts as timing: on a
# loaded host the hook's own time checkpoints decide the text (slow()). The sed shim stalls only inside the rerun's job (shim/delay-first); a deadline
# case whose wall reaches the stall without a stall that ran to its end is SKIP [inconclusive].
# Output: one line per case "PASS|FAIL|MISSING|SETUP|SKIP <id> <detail>" (MISSING: a function the case calls is not defined in the hook under test, the
# baseline's status 127; SETUP: the case could not be built), then the totals. Two harness checks always run (post_planning R2 PP2-L): V0-H1, sc-direct.sh
# ran to its sentinel and exited 0; V0-H2, every expected case id of the mode was reported once and no other. Exit 0 when nothing is FAIL, MISSING or
# SETUP; 1 otherwise; 3 when the run cannot start (SETUP: a missing tool, an SC_BASH that does not run, the canary on the baseline).
set -u
setup() { echo "SETUP: $*"; exit 3; }
(( ${BASH_VERSINFO[0]} >= 5 )) || setup "run sc-cases.sh with bash 5 (EPOCHREALTIME); the hook's bash is SC_BASH"
HERE="$(cd "$(dirname "$0")" && pwd)"
[[ $# -ge 1 && -f "$1" && -r "$1" ]] || setup "the hook under test is not a readable file: ${1:-<none>}"
HOOK=$(readlink -f "$1"); BASE=${2:-}
SC_BASH_IN=${SC_BASH:-$(command -v bash)}; SC_BASH=$(readlink -f "$SC_BASH_IN" 2>/dev/null); SC_ONLY=${SC_ONLY:-.}
LOADMAX=${SC_LOAD_MAX:-2}
NICE=(taskset -c 0,1 nice -n 19); [[ "${SC_NICE:-1}" == 0 ]] && NICE=()
# ---- canary, part 1: the tools and the bash that runs the hook ----
for t in jq sed python3 timeout awk cmp sha256sum mktemp ps grep tr od git env; do command -v "$t" >/dev/null 2>&1 || setup "a tool is missing: $t"; done
(( ${#NICE[@]} == 0 )) || { command -v taskset >/dev/null 2>&1 && command -v nice >/dev/null 2>&1; } || setup "taskset or nice is missing (SC_NICE=0 runs without them)"
sleep 0.01 2>/dev/null || setup "sleep does not take fractional seconds"
[[ -n "$SC_BASH" && -f "$SC_BASH" && -x "$SC_BASH" ]] && "$SC_BASH" -c : </dev/null >/dev/null 2>&1 || setup "SC_BASH does not run: $SC_BASH_IN"
W=$(mktemp -d); trap 'rm -rf "$W"' EXIT
if [[ -z "$BASE" ]]; then
  root=$(git -C "$HERE" rev-parse --show-toplevel 2>/dev/null) && git -C "$root/aria" show 59e333c:hooks/secret-guard.sh > "$W/base.sh" 2>/dev/null || setup "cannot extract aria 59e333c:hooks/secret-guard.sh"
  BASE=$W/base.sh
fi
[[ -f "$BASE" && -r "$BASE" ]] || setup "BASE is not a readable file: $BASE"
BASE=$(readlink -f "$BASE")
[[ "$(sha256sum < "$BASE" | cut -c1-12)" == e83c5e30f2cc ]] || setup "BASE is not the baseline hook (sha256 prefix e83c5e30f2cc)"
read -r MACH MAJ MIN < <("$SC_BASH" -c 'echo "${BASH_VERSINFO[5]} ${BASH_VERSINFO[0]} ${BASH_VERSINFO[1]}"')
wslmark() {   # [MOUNTS [DIR]] : status 0 where the gate must see a WSL mark in the file system -- the rule of the hook's _sg_relax_nowslfs (What 1 supplement 2,
  # v3.4), written apart from it, never sourced or called (status 0 here is status 1 there): the mount table (default /proc/self/mounts) cannot be read or
  # reads empty; or the topmost mount at DIR (default /proc/sys/fs/binfmt_misc; the table's last line for it) is a binfmt_misc file system and DIR cannot
  # be searched (cd fails) or holds WSLInterop or WSLInterop-late (each name tested on its own: no glob, no listing). DIR is looked at only under a topmost
  # binfmt_misc, so the check never triggers an automount. The two arguments exist to check it against the hook's function; WSLF below calls it with none
  local t y d="${2:-/proc/sys/fs/binfmt_misc}"
  t=$(cat -- "${1:-/proc/self/mounts}" 2>/dev/null && echo .) || return 0
  [[ "$t" != . ]] || return 0
  y=$(printf '%s\n' "${t%.}" | awk -v d="$d" '$2 == d { print $3 }' | tail -n 1)
  [[ "$y" == binfmt_misc ]] || return 1
  ( cd -- "$d" ) >/dev/null 2>&1 || return 0
  [ -e "$d/WSLInterop" ] || [ -e "$d/WSLInterop-late" ]
}
OSR=$(cat /proc/sys/kernel/osrelease 2>/dev/null); WSLF=no; wslmark && WSLF=yes
RELAX=no   # the same rule as the gate (What 1 supplement); the WSL variables are cleared for every run of the hook, so only the kernel facts count here
[[ "$MACH" == x86_64-*-linux-gnu* && -n "$OSR" && "$OSR" != *[Mm]icrosoft* && "$OSR" != *WSL* && $WSLF == no ]] && (( MAJ == 5 && MIN <= 3 )) && RELAX=yes
sh12() { if [[ -r "$1" ]]; then sha256sum < "$1" | cut -c1-12; else echo -; fi; }
lt() { awk -v a="$1" -v b="$2" 'BEGIN{exit !(a+0 < b+0)}'; }
LOAD0=$(cut -d' ' -f1-3 /proc/loadavg); L0=${LOAD0%% *}
TGATE=no; lt "$L0" "$LOADMAX" && TGATE=yes
printf '# sc-cases.sh | %s | hook %s | base %s | sc-cases %s sc-direct %s mutants %s shim %s shapes %s commentsync %s | SC_BASH %s (%s %s.%s, kernel %s) -> relaxation expected: %s | load %s -> timing batch %s (SC_LOAD_MAX %s)\n' \
  "$(date -u +%FT%TZ)" "$(sh12 "$HOOK")" "$(sh12 "$BASE")" "$(sh12 "$HERE/sc-cases.sh")" "$(sh12 "$HERE/sc-direct.sh")" "$(sh12 "$HERE/mutants.py")" \
  "$(sh12 "$HERE/shim/delay-first")" "$(sh12 "$HERE/shapes.py")" "$(sh12 "$HERE/commentsync.py")" "$SC_BASH" "$MACH" "$MAJ" "$MIN" "${OSR:-<none>}" "$RELAX" \
  "$LOAD0" "$([[ $TGATE == yes ]] && echo judged || echo 'SKIP [load]')" "$LOADMAX"
# results are kept until the end: the load at the end decides whether the timing batch stands (INV-7)
R_ST=(); R_ID=(); R_DET=(); R_TM=()
res() { R_ST+=("$1"); R_ID+=("$2"); R_DET+=("$3"); R_TM+=("${4:-0}"); }
timed() {   # ID HARD SOFT DETAIL : hard bad -> FAIL under any load; otherwise PASS / FAIL by the soft part, or SKIP [load] when the batch is not judged
  if [[ $2 != ok ]]; then res FAIL "$1" "$4"
  elif [[ $TGATE != yes ]]; then res SKIP "$1" "[load] $4"
  elif [[ $3 == ok ]]; then res PASS "$1" "$4" 1
  else res FAIL "$1" "$4" 1; fi
}
sel() { [[ "$1" =~ $SC_ONLY ]]; }
REAL_JQ=$(command -v jq); REAL_SED=$(command -v sed)
mkdir -p "$W/in" "$W/home" "$W/ext/.aria"
for s in $(python3 "$HERE/shapes.py" list x); do
  python3 "$HERE/shapes.py" "$s" "$W/in/$s.txt" && "$REAL_JQ" -Rs '{tool_name:"Bash", tool_input:{command:.}}' < "$W/in/$s.txt" > "$W/in/$s.json" || setup "cannot build the input $s"
done
printf '%s\n' "billing/conf/prod.toml" > "$W/ext/.aria/secret-guard.paths"
"$REAL_JQ" -Rs --arg cwd "$W/ext" '{tool_name:"Bash", cwd:$cwd, tool_input:{command:.}}' < "$W/in/ext-read.txt" > "$W/in/ext-read-cwd.json" || setup "cannot build the input ext-read-cwd"

# ---------------- end-to-end helpers ----------------
kind() { if grep -q 'has a line longer than' "$1"; then echo longline; elif grep -q 'grows by more than' "$1"; then echo growth
  elif grep -q 'segments together are longer than' "$1"; then echo tmax; elif grep -q 'variable value is longer than' "$1"; then echo vmax
  elif grep -q 'too large to scan' "$1"; then echo oversize; elif grep -q 'within the time budget' "$1"; then echo time
  elif grep -q 'value-REDACTING filter' "$1"; then echo finding; elif [[ -s "$1" ]]; then echo other; else echo none; fi; }
HWRAP=()   # a wrapper for the hook under test only (the H arm), e.g. one that starts it with SIGTERM ignored
run() {   # PREFIX HOOK SHAPE [VAR=VALUE ...] : runs the hook on the shape -> <prefix>_RC, <prefix>_WALL, <prefix>_ERR (file), <prefix>_ST (the shim's state dir)
  local p=$1 h=$2 s=$3 st e t0 t1 rc; shift 3
  local -a wrap=(); [[ $p == H ]] && wrap=("${HWRAP[@]}")
  st=$(mktemp -d -p "$W"); e=$(mktemp -p "$W")
  t0=$EPOCHREALTIME
  env -u CLAUDE_PROJECT_DIR -u _SG_RELAXED -u SECRET_GUARD_TIME_BUDGET_S -u WSL_DISTRO_NAME -u WSL_INTEROP HOME="$W/home" SC_SHIM_STATE="$st" \
    SC_REAL_jq="$REAL_JQ" SC_REAL_sed="$REAL_SED" "$@" "${NICE[@]}" timeout 12 "${wrap[@]}" "$SC_BASH" "$h" < "$W/in/$s.json" >/dev/null 2>"$e"; rc=$?
  t1=$EPOCHREALTIME
  printf -v "${p}_RC" '%s' "$rc"; printf -v "${p}_ERR" '%s' "$e"; printf -v "${p}_ST" '%s' "$st"
  printf -v "${p}_WALL" '%s' "$(awk -v a="${t0/,/.}" -v b="${t1/,/.}" 'BEGIN{printf "%.2f", b-a}')"
}
ge() { awk -v a="$1" -v b="$2" 'BEGIN{exit !(a+0 >= b+0)}'; }
le() { awk -v a="$1" -v b="$2" 'BEGIN{exit !(a+0 <= b+0)}'; }
same() { [[ $H_RC == "$B_RC" ]] && cmp -s "$H_ERR" "$B_ERR"; }
SHIM="PATH=$HERE/shim:$PATH"
desc() { printf 'hook rc=%s %s %ss | base rc=%s %s %ss | stderr %s' "$H_RC" "$(kind "$H_ERR")" "$H_WALL" "$B_RC" "$(kind "$B_ERR")" "$B_WALL" "$(same && echo IDENTICAL || echo DIFFERENT)"; }
slow() {   # prints a tag when an arm shows that the host was too slow for a byte comparison: the harness's 12 s timeout (rc 124), or the guard's own
           # whole-second time budget firing in one arm only (its time text). Such a result is judged only in a judged timing batch (INV-7).
  local ht=no bt=no
  if [[ $H_RC == 124 || $B_RC == 124 ]]; then printf '[timeout12]'; return; fi
  [[ "$(kind "$H_ERR")" == time ]] && ht=yes; [[ "$(kind "$B_ERR")" == time ]] && bt=yes
  [[ $ht == "$bt" ]] || printf '[time-text]'
}
identity() {   # ID SHAPE [VAR=VALUE ...] : the hook must equal the baseline, byte for byte (load-independent unless the host was too slow: slow())
  local id=$1 s=$2 w; shift 2; sel "$id" || return 0
  run B "$BASE" "$s" "$@"; run H "$HOOK" "$s" "$@"; w=$(slow)
  if [[ -n "$w" ]]; then timed "$id" ok bad "$(desc) $w"
  elif same; then res PASS "$id" "$(desc)"; else res FAIL "$id" "$(desc) [bytes]"; fi
}
deadline() {   # ID SHAPE MIN MAX [VAR=VALUE ...] : (relaxation expected) the job is cut by the deadline: the baseline's bytes, wall in [MIN, MAX]
  local id=$1 s=$2 lo=$3 hi=$4 a sd='' st w hard=ok soft=ok t=''; shift 4; sel "$id" || return 0
  if [[ $RELAX != yes ]]; then identity "$id" "$s" "$@"; return 0; fi   # R2 PP2-m1: the variables reach the hook on every bash
  for a in "$@"; do [[ $a == SC_DELAY_sed=* ]] && sd=${a#*=}; done
  run B "$BASE" "$s"; run H "$HOOK" "$s" "$SHIM" "$@"
  st=none; [[ -f "$H_ST/sed.stall" ]] && st=job; [[ -f "$H_ST/sed.uncut" ]] && st=uncut
  if [[ $st == uncut ]]; then res FAIL "$id" "$(desc) sed-stall=$st (want IDENTICAL, wall window $lo..$hi) [uncut]"; return 0; fi   # nothing killed the job's group
  w=$(slow); if [[ -n "$w" ]]; then timed "$id" ok bad "$(desc) sed-stall=$st (want IDENTICAL, wall window $lo..$hi) $w"; return 0; fi
  if [[ -n "$sd" ]] && ge "$H_WALL" "$sd"; then res SKIP "$id" "[inconclusive] $(desc) sed-stall=$st: the wall reached the ${sd} s stall, which did not run to its end inside the job"; return 0; fi
  same || { hard=bad; t+=' [bytes]'; }
  ge "$H_WALL" "$lo" || { hard=bad; t+=' [wall<lo]'; }
  le "$H_WALL" "$hi" || { soft=bad; t+=' [wall>hi]'; }
  timed "$id" $hard $soft "$(desc) sed-stall=$st (want IDENTICAL, wall window $lo..$hi)$t"
}
outcome() {   # ID SHAPE WANT_RC WANT_KINDS(|-separated) [VAR=VALUE ...] : (relaxation expected) the rerun finishes before the deadline with this rc and text kind
  local id=$1 s=$2 wr=$3 wk=$4 k hard=ok soft=ok t=''; shift 4; sel "$id" || return 0
  if [[ $RELAX != yes ]]; then identity "$id" "$s" "$@"; return 0; fi
  run B "$BASE" "$s" "$@"; run H "$HOOK" "$s" "$@"; k=$(kind "$H_ERR")
  if [[ $H_RC == "$wr" && "|$wk|" == *"|$k|"* ]]; then le "$H_WALL" 4.5 || { soft=bad; t=' [wall>hi]'; }
  elif [[ -n "$(slow)" ]]; then soft=bad; t=" $(slow)"
  elif same; then soft=bad; t=' [fallback]'   # the baseline's bytes: the rerun did not finish before the deadline (a slow host) or never ran
  else hard=bad; [[ $H_RC == "$wr" ]] || t+=' [rc]'; [[ "|$wk|" == *"|$k|"* ]] || t+=' [kind]'; fi
  timed "$id" $hard $soft "$(desc) (want rc=$wr text=$wk within 4.5 s)$t"
}

# ---------------- direct-call cases (sc-direct.sh under SC_BASH) ----------------
if [[ "${SC_DIRECT:-1}" != 0 ]]; then
  mode=norelax; [[ $RELAX == yes ]] && mode=relax
  SC_ONLY="$SC_ONLY" "${NICE[@]}" "$SC_BASH" "$HERE/sc-direct.sh" "$HOOK" "$mode" "$BASE" </dev/null >"$W/direct.out" 2>"$W/direct.err"; drc=$?
  while IFS= read -r line; do
    st=${line%% *}; rest=${line#* }; id=${rest%% *}; det=${rest#"$id"}; det=${det# }
    case $st in
      PASS|FAIL|MISSING|SETUP|SKIP) sel "$id" && res "$st" "$id" "$det" ;;
      TIMED) h=${det%% *}; det=${det#* }; s=${det%% *}; det=${det#* }; sel "$id" && timed "$id" "$h" "$s" "$det" ;;
    esac
  done < "$W/direct.out"
  last=$(tail -n 1 "$W/direct.out")
  if [[ "$last" == "END sc-direct" && $drc == 0 ]]; then res PASS V0-H1-direct-complete "sc-direct.sh ($mode) ran to its sentinel and exited 0"
  else res FAIL V0-H1-direct-complete "sc-direct.sh ($mode): last line [$(printf '%s' "$last" | cut -c1-80)] (want END sc-direct), exit $drc (want 0); stderr: $(tail -n 3 "$W/direct.err" | tr '\n' ' ' | cut -c1-200) [harness]"; fi
fi

# ---------------- end-to-end cases ----------------
# P7 allow path; P3/P6 deadline and fallback bytes (the sed shim stalls the job's block text for 10 s, so only the deadline can end the job)
outcome   V7-E1-benign-big-allowed            benign-big 0 none
deadline  V6-E2-deadline-fallback-bytes       stall-read 2.85 3.6 SC_DELAY_sed=10
deadline  V3-E3-anchor-at-hook-start          stall-read 2.85 3.6 SC_DELAY_jq=1.5 SC_DELAY_sed=10
deadline  V3-E4-cap-3-at-budget-4             stall-read 2.85 3.6 SC_DELAY_sed=10 SECRET_GUARD_TIME_BUDGET_S=4
deadline  V3-E5-budget-2                      stall-read 1.85 2.6 SC_DELAY_sed=10 SECRET_GUARD_TIME_BUDGET_S=2   # budget 2, not 1: a whole-second tick of the first pass cannot reach it (R2 PP2-C)
deadline  V2-E6-flag-from-environment-ignored stall-read 2.85 3.6 SC_DELAY_sed=10 _SG_RELAXED=1
deadline  V2-E7-no-time-left                  stall-read 3.2 4.3 SC_DELAY_jq=3.2
# P2: OSTYPE, MACHTYPE and HOSTTYPE come from the environment and decide nothing (R2 PP2-m8); an extension project keeps the baseline
outcome   V2-E8-ostype-from-environment-ignored benign-big 0 none OSTYPE=darwin21 MACHTYPE=x86_64-apple-darwin23.0.0 HOSTTYPE=aarch64
identity  V2-E9-extension-project             ext-read CLAUDE_PROJECT_DIR="$W/ext"
# P9: no count bound in the rerun; TMAX holds in the rerun; VMAX unchanged
outcome   V9-E10-count-axis-read-blocked      count-axis 2 "finding|longline"
outcome   V9-E11-tmax-in-rerun                tmax-rerun 2 tmax
identity  V9-E12-vmax-unchanged               vmax
# P7 routing: by the copy's longest line; multi-line copies get the normal judgement, credit included (V7-E15 must be allowed: R2 PP2-m9)
outcome   V7-E13-multiline-copy-normal-text   count-axis-ctl 2 finding
outcome   V7-E14-long-line-from-expansion     longline-expansion 2 longline
outcome   V7-E15-credit-as-normal             multiline-credit 0 none
# P1 sampler: commands that never reach a trigger point
for s in p1-small-benign p1-small-read p1-small-read-filter p1-var-read p1-var-mid p1-var-mid-read; do identity "V1-E16-$s" "$s"; done
# P2: a WSL mark in the environment closes the gate (What 1 supplement); an extension project known only through the stdin cwd (R2 PP2-D)
identity  V2-E17-wsl-mark-keeps-baseline      benign-big WSL_DISTRO_NAME=Ubuntu
identity  V2-E18-extension-via-stdin-cwd      ext-read-cwd
# P3/P5: the deadline holds when the hook starts with SIGTERM ignored -- the timer and the group kill use KILL (R2 PP2-m12)
HWRAP=("$SC_BASH" -c 'trap "" TERM; exec "$0" "$@"')
deadline  V5-E19-deadline-with-term-ignored   stall-read 2.85 3.6 SC_DELAY_sed=10
HWRAP=()

# ---------------- static checks of the hook text ----------------
g=$(grep -n '^if \[\[ "${BASH_SOURCE\[0\]}" != "$0" \]\]; then' "$HOOK" | head -1 | cut -d: -f1)
for f in _sg_vx_big_judge _sg_relax_left _sg_relax_ok _sg_relax_platform _sg_relax_nowslfs _sg_relax_noext _sg_relax_job _sg_relax_run; do
  id="V11-S1-above-gate:$f"; sel "$id" || continue
  l=$(grep -n "^$f() {" "$HOOK" | head -1 | cut -d: -f1)
  if [[ -z "$l" ]]; then res MISSING "$id" "[missing] $f is not defined in the hook (sourcing gate at line ${g:-missing})"
  elif [[ -n "$g" ]] && (( l < g )); then res PASS "$id" "line $l < sourcing gate $g"
  else res FAIL "$id" "line $l, gate ${g:-missing} [value]"; fi
done
if sel V11-S3-longline-instructions-verbatim; then
  blk() { awk -v k="$2" '$0 ~ "kind\" == " k " \\]\\]; then" {f=1} f && /^Split it into smaller commands/ {p=1} p {print} p && /请拆成更小的命令/ {exit}' "$1"; }
  o=$(blk "$HOOK" oversize | sed '$d'); l=$(blk "$HOOK" longline | sed '$d'); lz=$(blk "$HOOK" longline | tail -1)
  if [[ -n "$o" && "$o" == "$l" && "$lz" == *请拆成更小的命令 ]]; then res PASS V11-S3-longline-instructions-verbatim "the longline instruction lines equal the oversize ones ($(printf '%s\n' "$l" | wc -l) lines)"
  else res FAIL V11-S3-longline-instructions-verbatim "oversize [$(printf '%s' "$o" | head -c 60 | tr '\n' '/')] longline [$(printf '%s' "$l" | head -c 60 | tr '\n' '/')] [text]"; fi
fi
if sel V11-S4-one-rule-loop; then
  a=$(grep -c 'risky_patterns\[@\]' "$BASE"); b=$(grep -c 'risky_patterns\[@\]' "$HOOK")
  if [[ $a == "$b" ]]; then res PASS V11-S4-one-rule-loop "loops over risky_patterns: $b (baseline $a)"; else res FAIL V11-S4-one-rule-loop "loops over risky_patterns: $b (baseline $a) [count]"; fi
fi
if sel V12-C1-hook-comments; then
  if python3 "$HERE/commentsync.py" --hook-only "$HOOK" target >/dev/null 2>&1; then res PASS V12-C1-hook-comments "commentsync --hook-only target: GREEN"
  else res FAIL V12-C1-hook-comments "commentsync --hook-only target: $(python3 "$HERE/commentsync.py" --hook-only "$HOOK" target 2>&1 | grep -E '^(RED|ok )' | grep -m 3 '^RED' | cut -c1-90 | tr '\n' ';') $(python3 "$HERE/commentsync.py" --hook-only "$HOOK" target 2>&1 | tail -1) [text]"; fi
fi

# ---------------- V0-H2: every expected case id of this mode, once (post_planning R2 PP2-L) ----------------
EXP_DIRECT_BOTH="V2-G1-gate
V2-G2-platform:x86_64-pc-linux-gnu:5.0 V2-G2-platform:x86_64-pc-linux-gnu:5.1 V2-G2-platform:x86_64-pc-linux-gnu:5.2 V2-G2-platform:x86_64-pc-linux-gnu:5.3
V2-G2-platform:aarch64-unknown-linux-gnu:5.2 V2-G2-platform:x86_64-pc-linux-gnu:5.4 V2-G2-platform:x86_64-pc-linux-gnu:6.0 V2-G2-platform:x86_64-pc-linux-gnu:4.4
V2-G2-platform:x86_64-unknown-linux-gnu:3.2 V2-G2-platform:x86_64-apple-darwin23.0.0:5.2 V2-G2-platform:x86_64-pc-msys:5.2 V2-G2-platform:x86_64-pc-cygwin:5.2
V2-G2-platform:x86_64-alpine-linux-musl:5.2 V2-G2-platform:aarch64-unknown-linux-android:5.2 V2-G2-platform:x86_64-pc-linux-gnu:5.2:osrelease-wsl1
V2-G2-platform:x86_64-pc-linux-gnu:5.2:osrelease-wsl2 V2-G2-platform:x86_64-pc-linux-gnu:5.2:osrelease-wsl2-2020 V2-G2-platform:x86_64-pc-linux-gnu:5.2:osrelease-WSL-tag
V2-G2-platform:x86_64-pc-linux-gnu:5.2:wsl-mark V2-G2-platform:x86_64-pc-linux-gnu:5.2:osrelease-empty V2-G2-platform:x86_64-pc-linux-gnu:5.2:three-args
V2-G3-gate-calls-platform V2-G3b-gate-uses-build-facts V2-G4-project-without-extension-file V2-G4-extension-file-with-entry V2-G4-empty-extension-file
V2-G4-extension-path-is-a-directory V2-G5-nested V2-G6-no-time-left V2-G7-no-anchor V2-G8-budget-0 V2-G11-flag-not-from-environment
V2-G12-segment-trigger-asks-gate V2-G13-whole-trigger-asks-gate V2-G14-cwd-extension-file-with-entry V2-G15-cwd-project-without-extension-file
V2-G16-environment-root-before-cwd V2-G17-wsl-distro-name-closes-gate V2-G18-wsl-interop-closes-gate
V11-S5-longline-head-verbatim V11-S6-longline-chinese-line-verbatim V11-S7-longline-text-verbatim
V15-W1a-autofs-mount-point-not-looked-at V15-W1b-binfmt-misc-with-wslinterop-late V15-W1c-binfmt-misc-without-entry V15-W1d-unreadable-mount-table V15-W1f-empty-mount-table V15-W1g-autofs-on-top-of-binfmt-misc-not-looked-at V15-W1h-directory-as-mount-table V15-W1i-noglob-binfmt-misc-with-wslinterop-late V15-W1j-failglob-binfmt-misc-without-entry V15-W1k-unsearchable-directory V15-W1l-unlistable-directory-with-wslinterop-late V15-W1m-mount-table-read-only-after-platform-and-time"
EXP_DIRECT_RELAX="V3-G9-clock-backwards V3-G10-cap-3 V3-G12-time-left-zero-padded
V4-S1-allow V4-S2-block-with-text V4-S3-block-without-text V3-S4-slow-judgement V5-S5-pipe-holder V4-S6-spoofed-tail-0 V4-S7-time-checkpoint V4-S8-internal-error
V5-S9-child-left-behind V5-S13-detached-child V5-S13b-nothing-outlives-the-run V4-S11-bare-zero V5-S10-timer-fork-fails V5-S10b-no-judgement-without-timer
V5-S10c-dead-timer-no-judgement V5-S10d-no-judgement-with-dead-timer V5-S14-failing-sleep-kills-at-once V5-S15-job-refuses-outside-group-leader
V4-S19-block-text-bytes V5-S12-no-leftovers V4-S16-rerun-collect-checkpoint V4-S17-rerun-whole-checkpoint V4-S18-rerun-segment-checkpoint
V6-S20-segment-fallback-text V6-S21-whole-fallback-text
V8-D1-late-references-plain V8-D1-late-references-braced V8-D2-growth-8192-plain V8-D3-growth-8193-plain V8-D2-growth-8192-braced V8-D3-growth-8193-braced
V8-D4-growth-text-whole V8-D5-growth-text-segment
V9-C1-assignments-rerun V9-C1b-assignments-baseline V9-C2-references-rerun-c12 V9-C2b-references-baseline-c12 V9-C2-references-rerun-cb12
V9-C2b-references-baseline-cb12 V9-C3-for-statements-rerun V9-C3b-for-statements-baseline V9-C4-value-limit-in-rerun
V10-N1-environ-rows-only V10-N2-read-rows-only V10-N3-environ-big-judge V10-N4-read-big-judge V7-N5-read-big-judge-short-lines
V10-N6-filtered-long-line-rows-only V7-N7-big-judge-filtered-long-line V7-N10-blank-padded-long-line V7-N11-lmax-edge-normal V7-N12-lmax-edge-rows-only
V7-N8-whole-branch-returns-big-judge V7-N9-segment-routes-to-big-judge V7-N13-unmeasured-length-rows-only V14-N1-nocredit-never-runs-credit V14-N2-longline-pattern-is-a-rule V14-G1-triggers-return-4-with-the-baseline-reason V14-G2-growth-limit-follows-gmax V14-F1-status-4-falls-back-to-the-baseline-block
V15-T1-timer-sleeps-time-left V15-T2-anchor-taken-once-at-hook-start V15-T3-job-errors-silenced V15-W1e-gate-closed-by-wsl-file-system V15-W1n-mount-table-read-in-one-pass"
EXP_E2E="V7-E1-benign-big-allowed V6-E2-deadline-fallback-bytes V3-E3-anchor-at-hook-start V3-E4-cap-3-at-budget-4 V3-E5-budget-2 V2-E6-flag-from-environment-ignored
V2-E7-no-time-left V2-E8-ostype-from-environment-ignored V2-E9-extension-project V9-E10-count-axis-read-blocked V9-E11-tmax-in-rerun V9-E12-vmax-unchanged
V7-E13-multiline-copy-normal-text V7-E14-long-line-from-expansion V7-E15-credit-as-normal V1-E16-p1-small-benign V1-E16-p1-small-read V1-E16-p1-small-read-filter
V1-E16-p1-var-read V1-E16-p1-var-mid V1-E16-p1-var-mid-read V2-E17-wsl-mark-keeps-baseline V2-E18-extension-via-stdin-cwd V5-E19-deadline-with-term-ignored"
EXP_STATIC="V11-S1-above-gate:_sg_vx_big_judge V11-S1-above-gate:_sg_relax_left V11-S1-above-gate:_sg_relax_ok V11-S1-above-gate:_sg_relax_platform
V11-S1-above-gate:_sg_relax_nowslfs V11-S1-above-gate:_sg_relax_noext V11-S1-above-gate:_sg_relax_job V11-S1-above-gate:_sg_relax_run V11-S3-longline-instructions-verbatim V11-S4-one-rule-loop
V12-C1-hook-comments"
want=" "; got=" "; dup=''
add_want() { local i; for i in $1; do sel "$i" && want+="$i "; done; }
if [[ "${SC_DIRECT:-1}" != 0 ]]; then add_want "$EXP_DIRECT_BOTH"; [[ $RELAX == yes ]] && add_want "$EXP_DIRECT_RELAX"; fi
add_want "$EXP_E2E"; add_want "$EXP_STATIC"
for i in "${!R_ID[@]}"; do id=${R_ID[i]}; [[ $id == V0-H* ]] && continue; [[ "$got" == *" $id "* ]] && dup+="$id "; got+="$id "; done
missing=''; for id in $want; do [[ "$got" == *" $id "* ]] || missing+="$id "; done
extra=''; for id in $got; do [[ "$want" == *" $id "* ]] || extra+="$id "; done
nw=$(wc -w <<< "$want"); ng=$(wc -w <<< "$got")
if [[ -z "$missing$extra$dup" ]]; then res PASS V0-H2-case-list "all $nw expected case ids of mode $([[ $RELAX == yes ]] && echo relax || echo norelax) reported once"
else res FAIL V0-H2-case-list "expected $nw ids, reported $ng; missing: [${missing% }] unexpected: [${extra% }] reported twice: [${dup% }] [harness]"; fi

# ---------------- the load at the end; the report ----------------
LOAD1=$(cut -d' ' -f1-3 /proc/loadavg); L1=${LOAD1%% *}
VOID=no; [[ $TGATE == yes ]] && ! lt "$L1" "$LOADMAX" && VOID=yes
if [[ $VOID == yes ]]; then
  for i in "${!R_ST[@]}"; do [[ ${R_TM[i]} == 1 ]] && { R_DET[i]="[void] ${R_ST[i]} at load $L0 -> $L1: ${R_DET[i]}"; R_ST[i]=SKIP; }; done
fi
pass=0 fail=0 missing=0 setupn=0 skip=0 sk_load=0 sk_void=0 sk_inc=0 sk_root=0
for i in "${!R_ST[@]}"; do
  printf '%s %s %s\n' "${R_ST[i]}" "${R_ID[i]}" "${R_DET[i]}"
  case ${R_ST[i]} in
    PASS) pass=$((pass+1));; FAIL) fail=$((fail+1));; MISSING) missing=$((missing+1));; SETUP) setupn=$((setupn+1));;
    SKIP) skip=$((skip+1)); case ${R_DET[i]} in '[load]'*) sk_load=$((sk_load+1));; '[void]'*) sk_void=$((sk_void+1));; '[inconclusive]'*) sk_inc=$((sk_inc+1));; '[root]'*) sk_root=$((sk_root+1));; esac;;
  esac
done
printf '# load start %s end %s | timing batch: %s\n' "$LOAD0" "$LOAD1" "$([[ $TGATE != yes ]] && echo 'SKIP [load]' || { [[ $VOID == yes ]] && echo 'void (SKIP [void]): run again' || echo judged; })"
printf '# totals: PASS %d  FAIL %d  MISSING %d  SETUP %d  SKIP %d (load %d, void %d, inconclusive %d, root %d)\n' "$pass" "$fail" "$missing" "$setupn" "$skip" "$sk_load" "$sk_void" "$sk_inc" "$sk_root"
(( fail == 0 && missing == 0 && setupn == 0 ))

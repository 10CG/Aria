#!/usr/bin/env bash
# sc-direct.sh HOOK MODE : the direct-call cases of sc-cases.sh, run under the bash being tested. MODE relax = a measured bash (the gate must open; mechanism cases
# with a stubbed judgement at a 1 s deadline; growth, count and rows-only cases) | norelax = any other bash (the gate must stay closed). One line per case:
# "PASS|FAIL <id> <detail>". The hook is sourced: it stops at its unit-test sourcing gate, so only the functions above that gate exist; risky_patterns,
# _sg_judge_one and _sg_redact_echo (below it) are pulled out by anchor where a case needs them, as the suite's SC-8 harness does.
H=$1; MODE=$2
source "$H" </dev/null >/dev/null 2>&1
set +e
unset CLAUDE_PROJECT_DIR; input=''
X=$(mktemp -d)
ok() { if [[ $1 == 0 ]]; then printf 'PASS %s %s\n' "$2" "$3"; else printf 'FAIL %s %s\n' "$2" "$3"; fi; }
want_gate() { [[ $MODE == relax ]] && echo 0 || echo 1; }
gate() { _sg_relax_ok; echo $?; }

# ---- P2: the gate ----
_SG_P0=${EPOCHREALTIME:-}; r=$(gate); ok $([[ $r == $(want_gate) ]]; echo $?) V2-G1-gate "this bash: status $r (want $(want_gate))"
while read -r m ma mi w; do
  _sg_relax_platform "$m" "$ma" "$mi"; r=$?; ok $([[ $r == "$w" ]]; echo $?) "V2-G2-platform:$m:$ma.$mi" "status $r (want $w)"
done <<'T'
x86_64-pc-linux-gnu 5 0 0
x86_64-pc-linux-gnu 5 1 0
x86_64-pc-linux-gnu 5 2 0
x86_64-pc-linux-gnu 5 3 0
aarch64-unknown-linux-gnu 5 2 0
x86_64-pc-linux-gnu 5 4 1
x86_64-pc-linux-gnu 6 0 1
x86_64-pc-linux-gnu 4 4 1
x86_64-unknown-linux-gnu 3 2 1
x86_64-apple-darwin23.0.0 5 2 1
x86_64-pc-msys 5 2 1
x86_64-pc-cygwin 5 2 1
x86_64-alpine-linux-musl 5 2 1
aarch64-unknown-linux-android 5 2 1
T
saved_pl=$(declare -f _sg_relax_platform)
_sg_relax_platform() { return 1; }
_SG_P0=${EPOCHREALTIME:-}; r=$(gate); ok $([[ $r == 1 ]]; echo $?) V2-G3-gate-calls-platform "status $r with the platform check failing (want 1)"
M=$X/pl; _sg_relax_platform() { printf '%s|%s|%s' "$1" "$2" "$3" > "$M"; return 0; }
OSTYPE=darwin21; _SG_P0=${EPOCHREALTIME:-}; gate >/dev/null; got=$(cat "$M" 2>/dev/null); exp="${BASH_VERSINFO[5]}|${BASH_VERSINFO[0]}|${BASH_VERSINFO[1]}"
ok $([[ "$got" == "$exp" ]]; echo $?) V2-G3b-gate-uses-build-facts "platform check got [$got], want [$exp] (OSTYPE set to darwin21)"
eval "$saved_pl"
mkdir -p "$X/p1/.aria" "$X/p2/.aria" "$X/p3/.aria" "$X/p4/.aria/secret-guard.paths"
printf '%s\n' "some/entry/path" > "$X/p2/.aria/secret-guard.paths"; : > "$X/p3/.aria/secret-guard.paths"
for c in "p1 $(want_gate) project-without-extension-file" "p2 1 extension-file-with-entry" "p3 1 empty-extension-file" "p4 1 extension-path-is-a-directory"; do
  set -- $c; r=$( export CLAUDE_PROJECT_DIR="$X/$1"; _SG_P0=${EPOCHREALTIME:-}; gate ); ok $([[ $r == "$2" ]]; echo $?) "V2-G4-$3" "status $r (want $2)"
done
r=$( _SG_RELAXED=1; _SG_P0=${EPOCHREALTIME:-}; gate ); ok $([[ $r == 1 ]]; echo $?) V2-G5-nested "status $r (want 1)"
r=$( SECRET_GUARD_TIME_BUDGET_S=1; _SG_P0=$(awk -v e="${EPOCHREALTIME:-0}" 'BEGIN{sub(",",".",e); printf "%.6f", e-1.5}'); gate ); ok $([[ $r == 1 ]]; echo $?) V2-G6-no-time-left "status $r (want 1)"
r=$( _SG_P0=; gate ); ok $([[ $r == 1 ]]; echo $?) V2-G7-no-anchor "status $r (want 1)"
r=$( SECRET_GUARD_TIME_BUDGET_S=0; _SG_P0=${EPOCHREALTIME:-}; gate ); ok $([[ $r == 1 ]]; echo $?) V2-G8-budget-0 "status $r (want 1)"
r=$(env _SG_RELAXED=1 "$BASH" -c 'source "$1" </dev/null >/dev/null 2>&1; printf "[%s]" "${_SG_RELAXED-unset}"' _ "$H")
ok $([[ $r == "[]" ]]; echo $?) V2-G11-flag-not-from-environment "a hook sourced with _SG_RELAXED=1 in its environment holds $r (want [])"

if [[ $MODE == relax ]]; then
  el() { awk -v a="${1/,/.}" -v b="${2/,/.}" 'BEGIN{printf "%.2f", b-a}'; }
  # ---- P3: the deadline value ----
  r=$( SECRET_GUARD_TIME_BUDGET_S=1; _SG_P0=$(awk -v e="$EPOCHREALTIME" 'BEGIN{sub(",",".",e); printf "%.6f", e+5}'); _sg_relax_left; echo "$_SG_LEFT" )
  ok $(awk -v l="$r" 'BEGIN{exit !(l>0 && l<=1.0)}'; echo $?) V3-G9-clock-backwards "time left $r with the anchor 5 s in the future, budget 1 (want 0 < left <= 1.000000)"
  r=$( SECRET_GUARD_TIME_BUDGET_S=4; _SG_P0=$EPOCHREALTIME; _sg_relax_left; echo "$_SG_LEFT" )
  ok $(awk -v l="$r" 'BEGIN{exit !(l>2.9 && l<=3.0)}'; echo $?) V3-G10-cap-3 "time left $r at budget 4 (want 2.9 < left <= 3.000000: min(budget, 3))"
  # ---- P3 / P4 / P5: the job, with a stubbed judgement; deadline 1 s ----
  export SECRET_GUARD_TIME_BUDGET_S=1; _SG_MODE=whole
  run() {   # id want_rc min_wall max_wall want_stderr
    local id=$1 want=$2 minw=$3 maxw=$4 wsd=$5 err t0 t1 rc w sd
    _SG_P0=$EPOCHREALTIME; err=$(mktemp -p "$X"); t0=$EPOCHREALTIME
    _sg_relax_run "cmd" 2>"$err"; rc=$?
    t1=$EPOCHREALTIME; w=$(el "$t0" "$t1"); sd=$(cat "$err")
    ok $([[ $rc == "$want" && "$sd" == "$wsd" ]] && awk -v w="$w" -v a="$minw" -v b="$maxw" 'BEGIN{exit !(w>=a && w<=b)}'; echo $?) "$id" "rc=$rc (want $want) wall=${w}s (want $minw..$maxw) stderr=$(printf '%q' "${sd:0:40}") (want $(printf '%q' "$wsd"))"
  }
  _sg_vx_pass() { return 0; };                                                     run V4-S1-allow 0 0 0.3 ''
  _sg_vx_pass() { echo "BLOCK TEXT" >&2; return 2; };                              run V4-S2-block-with-text 2 0 0.3 'BLOCK TEXT'
  _sg_vx_pass() { return 2; };                                                     run V4-S3-block-without-text 4 0 0.3 ''
  _sg_vx_pass() { sleep 10.111; return 0; };                                       run V3-S4-slow-judgement 4 0.85 1.3 ''
  _sg_vx_pass() { sleep 6.222 & wait; return 0; };                                 run V5-S5-pipe-holder 4 0.85 1.3 ''
  _sg_vx_pass() { { sleep 0.5; printf 'x\n0\n' >&2; } & sleep 10.333; return 0; };  run V4-S6-spoofed-tail-0 4 0.85 1.3 ''
  _sg_vx_pass() { return 3; };                                                     run V4-S7-time-checkpoint 4 0 0.3 ''
  _sg_vx_pass() { echo "$undefined_var_xyz"; return 0; };                          run V4-S8-internal-error 4 0 0.3 ''
  _sg_vx_pass() { sleep 2.718 & return 0; };                                      run V5-S9-child-left-behind 0 0 0.3 ''
  _sg_vx_pass() { sleep 7.777 >/dev/null 2>&1 & return 0; };                     run V5-S13-detached-child 0 0 0.3 ''
  n=$(ps -eo args | awk '$1=="sleep" && $2=="7.777"' | wc -l)
  ok $([[ $n == 0 ]]; echo $?) V5-S13b-nothing-outlives-the-run "a child that does not hold the pipe, still alive right after _sg_relax_run returned: $n (want 0)"
  saved_job=$(declare -f _sg_relax_job)
  _sg_relax_job() { return 0; };                                                   run V4-S11-bare-zero 4 0 0.3 ''
  eval "$saved_job"
  MK=$X/ran; _sg_vx_pass() { echo ran > "$MK"; return 0; }
  inj=$(declare -f _sg_relax_job | sed '0,/local me=\$BASHPID tp/s//local me=$BASHPID tp; ulimit -u 1/')
  if [[ "$inj" == *"ulimit -u 1"* ]]; then
    eval "$inj"; run V5-S10-timer-fork-fails 4 0 16.5 ''
    ok $([[ ! -e "$MK" ]]; echo $?) V5-S10b-no-judgement-without-timer "judgement started: $([[ -e $MK ]] && echo yes || echo no) (want no)"
    eval "$saved_job"
  else
    ok 1 V5-S10-timer-fork-fails "SETUP: the timer line (local me=\$BASHPID tp) was not found in _sg_relax_job"
  fi
  # the defensive branch itself: a timer that is not running (here: replaced by a process that has already ended) -> no judgement at all
  rm -f "$MK"; fj=$(declare -f _sg_relax_job); tpat='( sleep "$_SG_LEFT";'
  if [[ "$fj" == *"$tpat"* && "$fj" == *'& tp=${!:-};'* ]]; then
    pre=${fj%%"$tpat"*}; rest=${fj#*"$tpat"}; rest=${rest#*'& tp=${!:-};'}
    eval "${pre}true & wait \"\$!\"; tp=\${!:-};${rest}"; run V5-S10c-dead-timer-no-judgement 4 0 0.3 ''
    ok $([[ ! -e "$MK" ]]; echo $?) V5-S10d-no-judgement-with-dead-timer "judgement started: $([[ -e $MK ]] && echo yes || echo no) (want no)"
    eval "$saved_job"
  else
    ok 1 V5-S10c-dead-timer-no-judgement "SETUP: the timer start (( sleep \"\$_SG_LEFT\"; ... & tp=\${!:-};) was not found in _sg_relax_job"
  fi
  # the timer fails closed: a sleep that fails at once (missing, or one that rejects fractional seconds) makes the timer kill the group at once -> fallback
  FS=$X/failsleep; mkdir -p "$FS"; printf '#!/bin/sh\nexit 1\n' > "$FS/sleep"; chmod +x "$FS/sleep"
  _sg_vx_pass() { local i; for (( i = 0; i < 10000000; i++ )); do :; done; return 0; }
  PATH="$FS:$PATH" run V5-S14-failing-sleep-kills-at-once 4 0 0.3 ''
  sleep 1.2
  n=$(ps -eo args | awk '$1=="sleep" && ($2=="10.111"||$2=="6.222"||$2=="10.333"||$2=="2.718"||$2=="7.777")' | wc -l)
  ok $([[ $n == 0 ]]; echo $?) V5-S12-no-leftovers "stub processes still alive after the cases: $n (want 0)"
  source "$H" </dev/null >/dev/null 2>&1; set +e; unset CLAUDE_PROJECT_DIR; input=''   # the real functions back (the stubs above replaced _sg_vx_pass)
  # ---- P8: growth, measured against the input ----
  grow() {   # id cmd want_rc
    local id=$1 c=$2 want=$3 r
    r=$( _SG_RELAXED=1; _sg_vx_collect "$c" >/dev/null 2>&1; _sg_vx_apply "$c" >/dev/null 2>&1; echo "$? $(( ${#_SG_SUB} - ${#c} ))" )
    ok $([[ ${r%% *} == "$want" ]]; echo $?) "$id" "apply status ${r%% *} growth ${r##* } (want status $want)"
  }
  # growth = 2 x (4000 - len(reference)) + (len(b) - len(reference)): plain $a is 2 characters, braced ${a} is 4
  a=$(printf '%*s' 4000 '' | tr ' ' a); b198=$(printf '%*s' 198 '' | tr ' ' b); b199=${b198}b; b204=$(printf '%*s' 204 '' | tr ' ' b); b205=${b204}b
  v2k=$(printf '%*s' 2000 '' | tr ' ' v)
  pad=$(printf '%*s' 6500 '' | tr ' ' y)
  grow V8-D1-late-references-plain "v=$v2k; : $pad \$v \$v" 0
  grow V8-D1-late-references-braced "v=$v2k; : $pad \${v} \${v}" 0
  grow V8-D2-growth-8192-plain "a=$a; b=$b198; : \$a \$a \$b" 0
  grow V8-D3-growth-8193-plain "a=$a; b=$b199; : \$a \$a \$b" 2
  grow V8-D2-growth-8192-braced "a=$a; b=$b204; : \${a} \${a} \${b}" 0
  grow V8-D3-growth-8193-braced "a=$a; b=$b205; : \${a} \${a} \${b}" 2
  # ---- P9: no count bound inside the rerun (baseline bounds unchanged outside it) ----
  c20=$(for i in $(seq -w 1 20); do printf 'a%s=1; ' "$i"; done)": \$a20"
  r=$( _SG_RELAXED=1; _sg_vx_collect "$c20"; echo ${#_SGV_N[@]} ); ok $([[ $r == 20 ]]; echo $?) V9-C1-assignments-rerun "collected $r of 20 inside the rerun (want 20)"
  r=$( _SG_RELAXED=; _sg_vx_collect "$c20"; echo ${#_SGV_N[@]} );  ok $([[ $r == 16 ]]; echo $?) V9-C1b-assignments-baseline "collected $r of 20 in the baseline pass (want 16, unchanged)"
  c12="v=Q; : $(for i in $(seq 1 12); do printf '$v '; done)"; cb12="v=Q; : $(for i in $(seq 1 12); do printf '${v} '; done)"
  for k in c12 cb12; do
    r=$( _SG_RELAXED=1; _sg_vx_collect "${!k}"; _sg_vx_apply "${!k}" >/dev/null; [[ "$_SG_SUB" == *'$v'* || "$_SG_SUB" == *'${v}'* ]] && echo left || echo none )
    ok $([[ $r == none ]]; echo $?) "V9-C2-references-rerun-$k" "references left unexpanded inside the rerun: $r (want none)"
    r=$( _SG_RELAXED=; _sg_vx_collect "${!k}"; _sg_vx_apply "${!k}" >/dev/null; [[ "$_SG_SUB" == *'$v'* || "$_SG_SUB" == *'${v}'* ]] && echo left || echo none )
    ok $([[ $r == left ]]; echo $?) "V9-C2b-references-baseline-$k" "references left unexpanded in the baseline pass: $r (want left, unchanged)"
  done
  # ---- P10 / P7: rows only keeps the W12 neutralisation; _sg_vx_big_judge routes by the copy's longest line ----
  awk '/^declare -a risky_patterns=\(/,/^\)$/' "$H" > "$X/rp.sh"; awk '/^_sg_judge_one\(\) \{/,/^\}$/' "$H" > "$X/jo.sh"; awk '/^_sg_redact_echo\(\) \{/,/^\}$/' "$H" > "$X/re.sh"
  if [[ -s "$X/rp.sh" && -s "$X/jo.sh" && -s "$X/re.sh" ]]; then
    source "$X/rp.sh"; source "$X/jo.sh"; source "$X/re.sh"
    z=$(printf '%*s' 9000 '' | tr ' ' z); cfg="/etc/forg""ejo/app"".ini"
    env1="python3 -c 'import os; print(os.environ.get(\"HOME\"))' $z"; rd="cat $cfg $z"; rdl="cat $cfg"$'\n'"$(for i in $(seq 1 40); do printf 'echo %0250d\n' 0; done)"
    one() {   # id fn args... -- want_rc want_kind
      local id=$1; shift; local want=${@: -2:1} wk=${@: -1} e rc k; set -- "${@:1:$#-3}"
      e=$(mktemp -p "$X"); command="$2"; "$@" 2>"$e" >/dev/null; rc=$?
      if grep -q 'has a line longer than' "$e"; then k=longline; elif grep -q 'value-REDACTING filter' "$e"; then k=finding; elif [[ -s $e ]]; then k=other; else k=none; fi
      ok $([[ $rc == "$want" && $k == "$wk" ]]; echo $?) "$id" "rc=$rc text=$k (want rc=$want text=$wk)"
    }
    one V10-N1-environ-rows-only _sg_judge_one "$env1" whole nocredit -- 0 none
    one V10-N2-read-rows-only _sg_judge_one "$rd" whole nocredit -- 2 longline
    one V10-N3-environ-big-judge _sg_vx_big_judge "$env1" whole -- 0 none
    one V10-N4-read-big-judge _sg_vx_big_judge "$rd" whole -- 2 longline
    one V7-N5-read-big-judge-short-lines _sg_vx_big_judge "$rdl" whole -- 2 finding
  else
    ok 1 V10-SETUP "risky_patterns / _sg_judge_one / _sg_redact_echo not found by anchor"
  fi
fi
rm -rf "$X"

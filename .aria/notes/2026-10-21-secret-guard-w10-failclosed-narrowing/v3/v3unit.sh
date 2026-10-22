#!/usr/bin/env bash
# v3unit.sh <hook>: mechanism checks of the relaxed rerun with a stubbed judgement (deadline 1 s). Prints one line per scenario.
H=$1
source "$H" </dev/null >/dev/null 2>&1
set +e
export SECRET_GUARD_TIME_BUDGET_S=1
_SG_MODE=whole
el() { awk -v a=${1/,/.} -v b=${2/,/.} 'BEGIN{printf "%.2f", b-a}'; }
run() {   # name expect_rc max_wall
  local name=$1 want=$2 maxw=$3 err t0 t1 rc w
  _SG_P0=$EPOCHREALTIME
  err=$(mktemp); t0=$EPOCHREALTIME
  _sg_relax_run "cmd" 2>"$err"; rc=$?
  t1=$EPOCHREALTIME; w=$(el $t0 $t1)
  local ok=PASS; [[ $rc == "$want" ]] || ok=FAIL; awk -v w=$w -v m=$maxw 'BEGIN{exit !(w<=m)}' || ok=FAIL
  printf '%-4s %-26s rc=%s (want %s) wall=%ss (max %s) stderr=%q\n' "$ok" "$name" "$rc" "$want" "$w" "$maxw" "$(head -c 60 "$err")"
  rm -f "$err"
}
_sg_vx_pass() { return 0; };                                                    run S1-allow 0 0.3
_sg_vx_pass() { echo "BLOCK TEXT" >&2; return 2; };                             run S2-block 2 0.3
_sg_vx_pass() { return 2; };                                                    run S3-block-no-text 4 0.3
_sg_vx_pass() { sleep 10.111; return 0; };                                      run S4-slow-judge 4 1.3
_sg_vx_pass() { sleep 6.222 & wait; return 0; };                                run S5-pipe-holder 4 1.3
_sg_vx_pass() { { sleep 0.5; printf 'x\n0\n' >&2; } & sleep 10.333; return 0; }; run S6-spoof-tail-0 4 1.3
_sg_vx_pass() { return 3; };                                                    run S7-time-checkpoint 4 0.3
_sg_vx_pass() { local z; echo "$undefined_var_xyz"; return 0; };                run S8-internal-error 4 0.3
sleep 1.6; echo "orphans: $(pgrep -f 'sleep (10\.111|6\.222|10\.333)' | wc -l)"
# gate
_sg_vx_pass() { return 0; }
_SG_P0=$EPOCHREALTIME; _sg_relax_ok && echo "PASS G1-gate-open (linux, time left, no extension)" || echo "FAIL G1-gate-open"
( OSTYPE=darwin21; _SG_P0=$EPOCHREALTIME; _sg_relax_ok && echo "FAIL G2-darwin" || echo "PASS G2-darwin: no relaxation" )
( OSTYPE=msys; _SG_P0=$EPOCHREALTIME; _sg_relax_ok && echo "FAIL G3-msys" || echo "PASS G3-msys: no relaxation" )
( _sg_ext_entries() { echo "some/entry"; }; _SG_P0=$EPOCHREALTIME; _sg_relax_ok && echo "FAIL G4-extension" || echo "PASS G4-extension: no relaxation" )
( _SG_RELAXED=1; _SG_P0=$EPOCHREALTIME; _sg_relax_ok && echo "FAIL G5-nested" || echo "PASS G5-nested: no relaxation" )
( _SG_P0=$(awk -v e=${EPOCHREALTIME/,/.} 'BEGIN{printf "%.6f", e-1.5}'); _sg_relax_ok && echo "FAIL G6-no-time" || echo "PASS G6-no-time-left: no relaxation" )
( _SG_P0=; _sg_relax_ok && echo "FAIL G7-no-anchor" || echo "PASS G7-no-anchor: no relaxation" )
( SECRET_GUARD_TIME_BUDGET_S=0; _SG_P0=$EPOCHREALTIME; _sg_relax_ok && echo "FAIL G8-budget0" || echo "PASS G8-budget-0: no relaxation" )

"""patch3c2.py <suite>: the 3c2 change of the six groups' deadline fallback (wpa_x6), its comment block, the shared comment's one sentence and the
summary line. Line-anchored; every anchor must hit exactly once; nothing else in the suite is touched."""
import sys

NEW_A = r'''# In the relaxed branch a trigger-point command (a copy over 8192) goes through wpa_x6, which also accepts the deadline fallback (the baseline branch's
# assertion on the same output, with a wall only a fallback for time gives: >= 3.0 s, or over 2.0 s with a gate-closed run of the same input at least
# 1.0 s quicker; see wpa_x6), and the summary counts those fallbacks.
'''

NEW_B = r'''# Deadline fallback of the relaxed branch (plan notes: the 3b ruling, its 2.85 s bound replaced by (1) of the 3c ruling; technical, the posture unchanged).
# A trigger-point command there -- its copy over 8192: 21ab's three, 21ac's 4096-character for list, 21ag, 21aj's three, the 8193 of 21al and 21ao --
# runs the hook ONCE (wpa_x6_hook; SECRET_GUARD_TIME_BUDGET_S cleared, so the deadline is _SG_P0 + 3 s). Its wall W is taken by EPOCHREALTIME and
# compared in whole microseconds, never rounded first (shown cut to two decimals). Why the hook falls back: the baseline pass runs first and on a busy
# host takes much of the 3 s (21ab: 2.37-2.58 s for the whole hook at load 1.2-1.6, 2.39-3.08 s gate-closed, b2/t002d-verify/probe.txt), and then the
# hook gives the baseline's block (What 4; P3, P6). Worked out from the hook (sha256 af4658b6f935), a fallback for time has three ways and no other:
#   F1 the gate closes for lack of time: _sg_relax_left gives status 1 only once now >= _SG_P0 + 3 s;
#   F2 the deadline kills the job: its timer (sleep "$_SG_LEFT") starts after _SG_LEFT is worked out, so the kill comes after _SG_P0 + 3 s;
#   F3 the rerun's own time checkpoint: _sg_vx_collect resets _SG_T0=$SECONDS and _sg_over_budget sends the rerun back (status 3, then the baseline
#      block) once SECONDS - _SG_T0 >= 3; SECONDS counts whole seconds, so that is more than 2 s and at most 3 s after the reset, which comes after the
#      job starts, which comes after the baseline pass (its time Tb) ends.
# W starts before the hook process does, so before _SG_P0: F1 and F2 give W > 3.0 s; F3 gives W > Tb + 2 s, which is 2-3 s for a command whose
# baseline pass takes under 1 s; any fallback for time gives W > 2.0 s. A gate that closes early (a bad implementation) gives W about Tb. The rule:
# (1) the relaxed branch's assertion holds on that output: passes. (2) Otherwise, when the baseline branch's assertion for that command (the else
# branch's wpa_x_toolarge and its limit line) does not hold on the SAME output either: the check is off, its detail naming both assertions' misses and
# W. (3) Otherwise (the output is the baseline's block): (a) W >= 3.0 s: a deadline fallback (F1, F2 or a late F3). (b) 2.0 s < W < 3.0 s: the same
# input runs once more -- the same variables and directory, the budget variable cleared, plus WSL_DISTRO_NAME=Ubuntu, which closes the gate -- and its
# wall is Tb'; Tb' <= W - 1.0 s is a deadline fallback (F3: the checkpoint sent the rerun back, W more than 2 s over the baseline pass); otherwise the
# check is off with W and Tb' (the gate-closed run is as slow: the gate closed early, not the rerun's checkpoint). 1 s sits in the middle of F3's 2 s
# gap and leaves 1 s on each side for load jitter. (c) W <= 2.0 s: the check is off with W (a fallback for time does not end this early).
# This replaces the 3b rule's lower bound of 2.85 s, which was copied from the deadline cases instead of worked out from the hook and had a hole on
# each side: from 2.0 to 2.85 s it turned a lawful F3 red, and from 2.85 to 3.0 s it could not tell F3 from a gate that closed early. Left as it is
# (the 3c ruling): a command whose baseline pass alone runs past 3 s gives the same output as a lawful "no time to close the gate" and cannot be told
# apart; each group has a command with a quick baseline pass, and the ported cases cover the rest. No load gate: the six groups run late in the suite,
# where 3b's seven full rounds ended at load 2.21-4.13, so a gate would SKIP them nearly every round. A group still counts once; the summary line of the
# six groups gives the fallbacks over the trigger-point commands judged, each with its group and W (and Tb' for (b)).
'''

NEW_C = r'''wpa_x6_hook() {   # <input> [NAME=VALUE ...]: one run of the hook on <input> the way wpa_err runs it (in wpa_cwd, with WPA_ENV), SECRET_GUARD_TIME_BUDGET_S
                  # cleared and the extra variables last; sets wpa_x6_out (stderr, then WPA_RC=), wpa_x6_us (the wall in whole microseconds by EPOCHREALTIME,
                  # 0 without a usable clock) and wpa_x6_s (that wall in seconds cut to two decimals, for display only) -- wpa_x6's locals
  local in=$1 t0 t1; shift
  t0=${EPOCHREALTIME:-}
  wpa_x6_out="$( cd "$wpa_cwd" && printf '%s' "$in" | env -u SECRET_GUARD_TIME_BUDGET_S "${WPA_ENV[@]}" "$@" "$WPA_HOOK" 2>&1 >/dev/null; echo "WPA_RC=$?" )"
  t1=${EPOCHREALTIME:-}; t0=${t0/[.,]/}; t1=${t1/[.,]/}; wpa_x6_us=0
  [[ $t0 =~ ^[0-9]+$ && $t1 =~ ^[0-9]+$ ]] && (( 10#$t1 > 10#$t0 )) && wpa_x6_us=$(( 10#$t1 - 10#$t0 ))
  printf -v wpa_x6_s '%d.%02d' $(( wpa_x6_us / 1000000 )) $(( wpa_x6_us % 1000000 / 10000 ))
}
wpa_x6() {   # <the relaxed assertion: longline | pass (exit 0) | growth (wpa_L_gseg)> <the baseline branch's limit line for this command> <command>
  local how=$1 lim=$2 c=$3 input e wus ws r b fb='' bad='' g='?' p="${3//$wpa_nl/ }" wpa_x6_out wpa_x6_us wpa_x6_s
  input="$(wpa_in Bash "$c")"   # built before the clock starts: W is the hook's run alone
  wpa_x6_hook "$input"; e=$wpa_x6_out; wus=$wpa_x6_us; ws=$wpa_x6_s
  wpa_x6_n=$((wpa_x6_n + 1))
  r=$(wpa_x6_eval "$e" "$how" "$lim" "$c"); [[ ${r%%$'\t'*} == 0 ]] && return 0   # (1) the relaxed branch's assertion holds
  b=$(wpa_x6_eval "$e" toolarge "$lim" "$c")
  if [[ ${b%%$'\t'*} != 0 ]]; then   # (2) nor does the baseline branch's
    bad="relaxed ($how):${r#*$'\t'} | baseline branch:${b#*$'\t'} | wall ${ws}s"
  elif (( wus >= 3000000 )); then   # (3a) F1, F2 or a late F3
    fb="${ws}s"
  elif (( wus > 2000000 )); then   # (3b) F3 or a gate closed early: the same input once more with the gate closed (a reading of 0 is no reading)
    wpa_x6_hook "$input" WSL_DISTRO_NAME=Ubuntu
    if (( wpa_x6_us > 0 && wpa_x6_us <= wus - 1000000 )); then fb="${ws}s/Tb ${wpa_x6_s}s"
    else bad="baseline block at wall ${ws}s, gate-closed Tb' ${wpa_x6_s}s (want <= wall - 1.0 s): 关门那一遍同样慢：是准入门提前关，不是重跑的检查点"; fi
  else   # (3c) W <= 2.0 s
    bad="baseline block at wall ${ws}s (want > 2.0 s): 因时间的回落不会这么早结束"
  fi
  if [[ -n $fb ]]; then
    [[ $_wpa_name =~ SC-(21a[a-z]) ]] && g=${BASH_REMATCH[1]}
    wpa_x6_fb=$((wpa_x6_fb + 1)); wpa_x6_where+="$g $fb; "; return 0
  fi
  _wpa_nbad=$((_wpa_nbad + 1))
  [[ $_wpa_nbad -le 6 ]] && _wpa_bad="$_wpa_bad {Bash ${p:0:72}: $bad}"
  return 0
}
'''


def die(m):
    sys.exit('patch3c2: ' + m)


path = sys.argv[1]
t = open(path, encoding='utf-8', newline='').read()
if '\r' in t:
    die('CR in the suite')
L = t.split('\n')


def idx(pred, what):
    hits = [i for i, s in enumerate(L) if pred(s)]
    if len(hits) != 1:
        die(f'{what}: {len(hits)} hits')
    return hits[0]


A = idx(lambda s: s.startswith('# In the relaxed branch a trigger-point command (a copy over 8192) goes through wpa_x6,'), 'A')
if not L[A + 1].startswith('# assertion on the same output, wall >= 2.85 s; see wpa_x6)'):
    die('A+1')
B0 = idx(lambda s: s.startswith('# Deadline fallback of the relaxed branch (3b ruling'), 'B0')
B1 = idx(lambda s: s == "wpa_x6_n=0; wpa_x6_fb=0; wpa_x6_where=''", 'B1')
if B1 - B0 != 11 or not all(L[i].startswith('#') for i in range(B0, B1)):
    die('B block shape')
C0 = idx(lambda s: s.startswith('wpa_x6() {   # <the relaxed assertion'), 'C0')
C1 = next(i for i in range(C0, len(L)) if L[i] == '}')
if not L[C1 + 1].startswith('# 21aa / 21ab:'):
    die('C end')
if 'sg_w10_ge "$wall" 2.85' not in '\n'.join(L[C0:C1 + 1]):
    die('C content')
if not L[C0 - 1] == '}' or not L[C0 - 4].startswith('  ( wpa_x6_e=$1;'):
    die('C is not right after wpa_x6_eval')
S = idx(lambda s: s.startswith('echo "W10 older groups 21ab 21ac 21ag 21aj 21al 21ao:'), 'S')
if L[S].count('${wpa_x6_where% }') != 1:
    die('S content')
if not (A < B0 < B1 < C0 < C1 < S):
    die('order')
# bottom up, so the earlier indices stay valid
L[S] = L[S].replace('${wpa_x6_where% }', '${wpa_x6_where%; }')
L[C0:C1 + 1] = NEW_C.rstrip('\n').split('\n')
L[B0:B1] = NEW_B.rstrip('\n').split('\n')
L[A:A + 2] = NEW_A.rstrip('\n').split('\n')
open(path, 'w', encoding='utf-8', newline='').write('\n'.join(L))
print(f'patched: A at {A + 1}, B {B0 + 1}-{B1}, C {C0 + 1}-{C1 + 1}, S at {S + 1} (old numbering)')

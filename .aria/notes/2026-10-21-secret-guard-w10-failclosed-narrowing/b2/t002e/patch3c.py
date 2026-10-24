#!/usr/bin/env python3
"""patch3c.py <aria root> <run-suite.sh> : the 3c edits (each old text must occur exactly once). Line endings kept (newline='')."""
import sys
root, rs = sys.argv[1], sys.argv[2]
SUITE = root + '/hooks/tests/secret-guard.test.sh'
HELP = root + '/hooks/tests/lib/secret-guard-w10-direct.sh'
SHIM = root + '/hooks/tests/lib/sg-shim/delay-first'

def edit(path, pairs):
    with open(path, encoding='utf-8', newline='') as f:
        t = f.read()
    for old, new in pairs:
        n = t.count(old)
        if n != 1:
            sys.exit(f'{path}: {n} hits for {old[:100]!r}')
        t = t.replace(old, new)
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(t)

# ---------------- suite: [reference] ----------------
REF_COMMENT = '''with SG_W10_ONLY set the round ends after it.
# [reference] (3c; the plan's notes, "the gap of reading (ii)"): the gate-closed arm runs the hook under test, so a slip in code or a constant that both arms
# share moves both arms alike and the byte comparison stays green (BI-8, _SGV_VMAX 4096 -> 8192: both arms rc 0 on V9-E12, which v31 catches against the real
# baseline). So every call that runs the gate-closed arm -- sg_w10_identity, sg_w10_deadline, sg_w10_outcome, and their fall back to identity where the
# relaxation is not expected -- first checks that arm against the outcome 59e333c (INV-9) gives for the same input, variables and WSL mark: exit code and
# text kind (sg_w10_ref, a table by case id, measured through v31/run-suite.sh on the five bash). A mismatch is FAIL [reference], its detail naming both,
# unless the arm hit the 12 s timeout or shows the time text: that counts as timing, as in sg_w10_slow. Only a check is added; v31's wanted values and
# reason tags are unchanged. V2-E17 (one arm, an outcome of its own) has none; the direct calls V6-S20 / V6-S21 check theirs in the helper (fbref).
SG_W10_DIR='''

REF_FUNCS = '''sg_w10_ref() {   # ID -> "<rc> <kind>": what 59e333c gives at this case's gate-closed call (the same input and variables; it ignores the WSL mark),
                 # measured through v31/run-suite.sh on the five bash in 3c: the same on each bash and in both modes. An id without an entry fails.
  case $1 in
    V1-E16-p1-small-benign|V1-E16-p1-small-read-filter|V1-E16-p1-var-mid) echo '0 none' ;;
    V1-E16-p1-small-read|V1-E16-p1-var-read|V1-E16-p1-var-mid-read) echo '2 finding' ;;
    V9-E12-vmax-unchanged) echo '2 vmax' ;;
    V7-E1-benign-big-allowed|V6-E2-deadline-fallback-bytes|V3-E3-anchor-at-hook-start|V3-E4-cap-3-at-budget-4|V3-E5-budget-2) echo '2 oversize' ;;
    V2-E6-flag-from-environment-ignored|V2-E7-no-time-left|V2-E8-ostype-from-environment-ignored|V2-E9-extension-project) echo '2 oversize' ;;
    V9-E10-count-axis-read-blocked|V9-E11-tmax-in-rerun|V7-E13-multiline-copy-normal-text|V7-E14-long-line-from-expansion) echo '2 oversize' ;;
    V7-E15-credit-as-normal|V2-E18-extension-via-stdin-cwd|V5-E19-deadline-with-term-ignored) echo '2 oversize' ;;
    *) echo 'unrecorded -' ;;
  esac
}
sg_w10_refok() {   # ID TAIL : [reference] the gate-closed arm (SGW_B_*) must give sg_w10_ref's outcome -> status 0. Otherwise the case is recorded here and the
                   # status is 1: timing when that arm hit the 12 s timeout or shows the time text (as sg_w10_slow), else FAIL [reference]. TAIL ends the detail.
  local want got w=''; want=$(sg_w10_ref "$1"); got="$SGW_B_RC $(sg_w10_kind "$SGW_B_ERR")"
  [[ $got == "$want" ]] && return 0
  if [[ $SGW_B_RC == 124 ]]; then w=' [timeout12]'; elif [[ ${got#* } == time ]]; then w=' [time-text]'; fi
  if [[ -n "$w" ]]; then sg_w10_timed "$1" ok bad "$(sg_w10_desc)$2 | gate-closed arm rc=${got% *} ${got#* }, reference (59e333c) rc=${want% *} ${want#* }$w"
  else sg_w10_res FAIL "$1" "$(sg_w10_desc)$2 | gate-closed arm rc=${got% *} ${got#* }, reference (59e333c) rc=${want% *} ${want#* } [reference]"; fi
  return 1
}
sg_w10_identity() {   # ID SHAPE [VAR=VALUE ...]'''

edit(SUITE, [
    ('with SG_W10_ONLY set the round ends after it.\nSG_W10_DIR=', REF_COMMENT),
    ('sg_w10_identity() {   # ID SHAPE [VAR=VALUE ...]', REF_FUNCS),
    ('''  sg_w10_run B "$s" WSL_DISTRO_NAME=Ubuntu "$@"; sg_w10_run H "$s" "$@"; w=$(sg_w10_slow)''',
     '''  sg_w10_run B "$s" WSL_DISTRO_NAME=Ubuntu "$@"; sg_w10_run H "$s" "$@"; sg_w10_refok "$id" '' || return 0; w=$(sg_w10_slow)'''),
    ('''  st=none; [[ -f "$SGW_H_ST/sed.stall" ]] && st=job; [[ -f "$SGW_H_ST/sed.uncut" ]] && st=uncut\n''',
     '''  st=none; [[ -f "$SGW_H_ST/sed.stall" ]] && st=job; [[ -f "$SGW_H_ST/sed.uncut" ]] && st=uncut\n'''
     '''  sg_w10_refok "$id" " sed-stall=$st (want IDENTICAL, wall window $lo..$hi)" || return 0\n'''),
    ('''  sg_w10_run B "$s" WSL_DISTRO_NAME=Ubuntu "$@"; sg_w10_run H "$s" "$@"; k=$(sg_w10_kind "$SGW_H_ERR")''',
     '''  sg_w10_run B "$s" WSL_DISTRO_NAME=Ubuntu "$@"; sg_w10_run H "$s" "$@"; sg_w10_refok "$id" " (want rc=$wr text=$wk within 4.5 s)" || return 0
  k=$(sg_w10_kind "$SGW_H_ERR")'''),
])

# ---------------- suite: the six groups' deadline fallback ----------------
X6 = '''  wpa_chk "finding [${p:0:48}]: not the longline text" no "$([[ "$e" == *"has a line longer than"* ]] && echo yes || echo no)"
}
# Deadline fallback of the relaxed branch (3b ruling in the plan's notes; technical, the posture unchanged). A trigger-point command there -- its copy over
# 8192: 21ab's three, 21ac's 4096-character for list, 21ag, 21aj's three, the 8193 of 21al and 21ao -- runs the hook ONCE (wpa_x6, wall by EPOCHREALTIME).
# The relaxed branch's assertion holding on that output passes. Otherwise the SAME output passes as a deadline fallback when it satisfies the baseline
# branch's assertion for that command (the else branch's wpa_x_toolarge and its limit line) and the wall is >= 2.85 s; neither: the check is off, its
# detail naming both assertions' misses and the wall. Why: the relaxed rerun must finish by _SG_P0 + min(budget, 3) s, and the baseline pass that runs
# first takes most of that on a busy host (21ab: 2.37-2.58 s for the whole hook at load 1.2-1.6, and 2.39-3.08 s gate-closed, b2/t002d-verify/probe.txt),
# so the hook falls back to the baseline's block (What 4; P3, P6); _sg_relax_left closes only once the deadline has passed, so such a fallback ends at about
# 3 s or later, and 2.85 s is the lower bound the deadline cases use. A quick baseline block (the gate shut, the rerun skipped) stays red. No load gate:
# the six groups run late in the suite, where 3b's seven full rounds ended at load 2.21-4.13, so a gate would SKIP them nearly every round. These runs
# clear SECRET_GUARD_TIME_BUDGET_S, so the deadline is 3 s and the bound holds. A group still counts once; the summary line of the six groups gives the
# fallbacks over the trigger-point commands judged (and their groups).
wpa_x6_n=0; wpa_x6_fb=0; wpa_x6_where=''
wpa_x6_eval() {   # <output as wpa_err gives it> <longline | pass | growth | toolarge> <limit line> <command> -> "<checks off>" TAB "<their list>": the assertion
                  # helper itself, in a subshell where wpa_err / wpa_rc hand back that output, so both branches judge ONE run of the hook
  ( wpa_x6_e=$1; wpa_err() { printf '%s' "$wpa_x6_e"; }; wpa_rc() { printf '%s' "${wpa_x6_e##*WPA_RC=}"; }; _wpa_bad=''; _wpa_nbad=0
    case $2 in longline) wpa_x_longline "$4" ;; pass) wpa_x Bash 0 "$4" ;; growth) wpa_x_toolarge "$4" "$wpa_L_gseg" ;; *) wpa_x_toolarge "$4" "$3" ;; esac
    printf '%s\\t%s' "$_wpa_nbad" "$_wpa_bad" )
}
wpa_x6() {   # <the relaxed assertion: longline | pass (exit 0) | growth (wpa_L_gseg)> <the baseline branch's limit line for this command> <command>
  local how=$1 lim=$2 c=$3 input e t0 t1 wall r b p="${3//$wpa_nl/ }"
  local -a env6=(-u SECRET_GUARD_TIME_BUDGET_S "${WPA_ENV[@]}")
  input="$(wpa_in Bash "$c")"
  t0=$EPOCHREALTIME   # the hook alone: wpa_err's call, with the budget variable cleared (the input is built before)
  e="$( cd "$wpa_cwd" && printf '%s' "$input" | env "${env6[@]}" "$WPA_HOOK" 2>&1 >/dev/null; echo "WPA_RC=$?" )"
  t1=$EPOCHREALTIME; wall=$(awk -v a="${t0/,/.}" -v b="${t1/,/.}" 'BEGIN{printf "%.2f", b-a}')
  wpa_x6_n=$((wpa_x6_n + 1))
  r=$(wpa_x6_eval "$e" "$how" "$lim" "$c"); [[ ${r%%$'\\t'*} == 0 ]] && return 0
  b=$(wpa_x6_eval "$e" toolarge "$lim" "$c")
  if [[ ${b%%$'\\t'*} == 0 ]] && sg_w10_ge "$wall" 2.85; then
    wpa_x6_fb=$((wpa_x6_fb + 1)); [[ $_wpa_name =~ SC-(21a[a-z]) ]] && wpa_x6_where+="${BASH_REMATCH[1]} "; return 0
  fi
  _wpa_nbad=$((_wpa_nbad + 1))
  [[ $_wpa_nbad -le 6 ]] && _wpa_bad="$_wpa_bad {Bash ${p:0:72}: relaxed ($how):${r#*$'\\t'} | deadline fallback (baseline branch; wall ${wall}s, want >= 2.85):${b#*$'\\t'}$(sg_w10_ge "$wall" 2.85 || printf ' {wall under 2.85}')}"
  return 0
}'''

edit(SUITE, [
    ('''  wpa_chk "finding [${p:0:48}]: not the longline text" no "$([[ "$e" == *"has a line longer than"* ]] && echo yes || echo no)"
}''', X6),
    ('''Either way a group is one case, so the count does not depend on the platform (SC-13). The summary prints the branch and its inputs.\n''',
     '''Either way a group is one case, so the count does not depend on the platform (SC-13). The summary prints the branch and its inputs.
# In the relaxed branch a trigger-point command (a copy over 8192) goes through wpa_x6, which also accepts the deadline fallback (the baseline branch's
# assertion on the same output, wall >= 2.85 s; see wpa_x6), and the summary counts those fallbacks.\n'''),
    ('''wpa_x_longline "$(wpa_vx_cmd 159)"; wpa_x Bash 0 "f=x; echo \\$f$(wpa_vx_fill 9000)"
wpa_x Bash 0 "f=x; echo \\$f$(wpa_rep a 4500 | sed 's/a/ a/g')"''',
     '''wpa_x6 longline "$wpa_L_seg" "$(wpa_vx_cmd 159)"; wpa_x6 pass "$wpa_L_seg" "f=x; echo \\$f$(wpa_vx_fill 9000)"
wpa_x6 pass "$wpa_L_seg" "f=x; echo \\$f$(wpa_rep a 4500 | sed 's/a/ a/g')"'''),
    ('''wpa_x_longline "for f in $(wpa_vx_val 4096); do cat \\"\\$f\\"; done"''',
     '''wpa_x6 longline "$wpa_L_whole" "for f in $(wpa_vx_val 4096); do cat \\"\\$f\\"; done"'''),
    ('''wpa_x_toolarge "$(wpa_vx_dense 300)" "$wpa_L_gseg"''', '''wpa_x6 growth "$wpa_L_seg" "$(wpa_vx_dense 300)"'''),
    ('''wpa_x_toolarge "$(wpa_vx_over 1)" "$wpa_L_gseg"; wpa_x_toolarge "$(wpa_vx_over 7)" "$wpa_L_gseg"; wpa_x_toolarge "$(wpa_vx_over 8)" "$wpa_L_gseg"''',
     '''wpa_x6 growth "$wpa_L_seg" "$(wpa_vx_over 1)"; wpa_x6 growth "$wpa_L_seg" "$(wpa_vx_over 7)"; wpa_x6 growth "$wpa_L_seg" "$(wpa_vx_over 8)"'''),
    ('''wpa_x_hit "$(wpa_vx_braced 31)"; wpa_x_longline "$(wpa_vx_braced 32)"''',
     '''wpa_x_hit "$(wpa_vx_braced 31)"; wpa_x6 longline "$wpa_L_whole" "$(wpa_vx_braced 32)"'''),
    ('''wpa_x_hit "$(wpa_vx_whole 2123)"; wpa_x_longline "$(wpa_vx_whole 2124)"''',
     '''wpa_x_hit "$(wpa_vx_whole 2123)"; wpa_x6 longline "$wpa_L_whole" "$(wpa_vx_whole 2124)"'''),
    ('''echo "W10 older groups 21ab 21ac 21ag 21aj 21al 21ao: ${wpa_rx6_note:-branch not chosen}"''',
     '''echo "W10 older groups 21ab 21ac 21ag 21aj 21al 21ao: ${wpa_rx6_note:-branch not chosen} | deadline fallback (截止回落) ${wpa_x6_fb:-0} / ${wpa_x6_n:-0}${wpa_x6_where:+ (${wpa_x6_where% })}"'''),
])

# ---------------- helper: fbt [reference] ----------------
edit(HELP, [
    ('''# a case whose tool is missing on the platform (ps) is SKIP [platform], not FAIL.''',
     '''# that gate-closed call must itself give the status and text kind 59e333c gives for the same copy and mode (fbref, measured on the five bash in 3c), else
# FAIL [reference]: it runs the hook under test, so a slip in code or a constant both calls share would move both alike and the byte comparison would stay
# green (the suite's [reference]; the time text there is TIMED). A case whose tool is missing on the platform (ps) is SKIP [platform], not FAIL.'''),
    ('''# [wall>hi] [fallback]. The last line''', '''# [wall>hi] [fallback] [reference]. The last line'''),
    ('''  fbt() {   # id mode cmd [segment...]''',
     '''  fbref() {   # id -> "<status> <kind>": what 59e333c's _sg_vx_pass gives at fbt's gate-closed call (the same copy and mode; it ignores the WSL mark), measured
              # in 3c on the five bash: the same on each. An id without an entry fails.
    case $1 in
      V6-S20-segment-fallback-text|V6-S21-whole-fallback-text) echo '2 oversize' ;;
      *) echo 'unrecorded -' ;;
    esac
  }
  fbt() {   # id mode cmd [segment...]'''),
    ('''    local id=$1 m=$2 c=$3 r rb t=''; shift 3''', '''    local id=$1 m=$2 c=$3 r rb kb ref t=''; shift 3'''),
    ('''    rb=$("$BASH" "$X/basefb.sh" "$H" "$X/fb-base" "$m" "$c" "$@")
''', '''    rb=$("$BASH" "$X/basefb.sh" "$H" "$X/fb-base" "$m" "$c" "$@"); kb=$(kindf "$X/fb-base"); ref=$(fbref "$id")
    if [[ "$rb $kb" != "$ref" ]]; then   # [reference]: first the gate-closed call against 59e333c's known outcome for this copy (the time text: timing)
      if [[ $kb == time ]]; then timed "$id" ok bad "gate closed by WSL_DISTRO_NAME: status $rb $kb, reference (59e333c) $ref [time-text]"
      else out FAIL "$id" "gate closed by WSL_DISTRO_NAME: status $rb $kb, reference (59e333c, the same copy and mode) $ref [reference]"; fi
      return 0
    fi
'''),
    ('''(status $rb) $(wc -c < "$X/fb-base") bytes''', '''(status $rb $kb) $(wc -c < "$X/fb-base") bytes'''),
])

# ---------------- shim: the header only ----------------
edit(SHIM, [
    ('''# Test shim for sc-cases.sh (installed as shim/jq and shim/sed): puts a fixed, machine-independent delay at a known point of the hook, then execs the real
# tool (SC_REAL_<name>) on every call.''',
     '''# Test shim of the secret-guard suite (hooks/tests/lib/sg-shim/, linked as jq and sed by relative symlinks). secret-guard.test.sh sets SC_SHIM_STATE (a
# fresh directory per run), SC_REAL_jq and SC_REAL_sed for every end-to-end run of the W10 ported cases (sg_w10_run); the deadline cases (sg_w10_deadline)
# also put this directory first on the hook's PATH and pass SC_DELAY_jq / SC_DELAY_sed. It puts a fixed, machine-independent delay at a known point of the
# hook, then execs the real tool (SC_REAL_<name>) on every call.'''),
])

# ---------------- v31/run-suite.sh: the helper's sha256 prefix on the first line ----------------
edit(rs, [
    ('''The first line records the date, the sha256 prefixes of <hook> and of the suite, and the one-minute loads; the''',
     '''The first line records the date, the sha256 prefixes of <hook>, of the suite and of its direct-call helper
# (hooks/tests/lib/secret-guard-w10-direct.sh; "missing" when the copy has none), and the one-minute loads; the'''),
    ('''printf '# run-suite.sh | %s | hook %s | suite %s | SC_BASH %s | SG_W10_ONLY %s | load %s\\n' "$(date -u +%FT%TZ)" "$(sha256sum < "$HK" | cut -c1-12)" \\
  "$(sha256sum < "$T/hooks/tests/secret-guard.test.sh" | cut -c1-12)" "${SC_BASH:-bash on PATH}"''',
     '''HL="$T/hooks/tests/lib/secret-guard-w10-direct.sh"
printf '# run-suite.sh | %s | hook %s | suite %s | helper %s | SC_BASH %s | SG_W10_ONLY %s | load %s\\n' "$(date -u +%FT%TZ)" "$(sha256sum < "$HK" | cut -c1-12)" \\
  "$(sha256sum < "$T/hooks/tests/secret-guard.test.sh" | cut -c1-12)" "$([[ -f "$HL" ]] && sha256sum < "$HL" | cut -c1-12 || echo missing)" "${SC_BASH:-bash on PATH}"'''),
])
print('patched')

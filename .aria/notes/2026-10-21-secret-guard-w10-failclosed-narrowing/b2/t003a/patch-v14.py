#!/usr/bin/env python3
# patch-v14.py <aria checkout> <v31 dir> : adds the TASK-003 gap cases (V14-...) to the suite's id list (V0-H2) and counts, to lib/secret-guard-w10-direct.sh and
# to v31/sc-direct.sh (INV-2). All anchors are asserted to match exactly once before anything is written.
import sys

WT, V31 = sys.argv[1], sys.argv[2]
IDS = ["V14-N1-nocredit-never-runs-credit", "V14-N2-longline-pattern-is-a-rule", "V14-G1-triggers-return-4-with-the-baseline-reason",
       "V14-G2-growth-limit-follows-gmax", "V14-F1-status-4-falls-back-to-the-baseline-block"]
IDLINE = " ".join(IDS)

BLOCK = r'''    # ---- V14: cases added by TASK-003 for the independent mutants no case caught for its own reason (Q-7 Q-15 Q-22 Q-29 Q-31); no load dependence ----
    if sel V14-N1-nocredit-never-runs-credit; then   # Q-15: a matching row on a line over _SGV_LMAX blocks before the O(n^2) credit is ever computed
      if need _sg_compute_credit; then
        r=$( _sg_compute_credit() { : > "$X/n14a.mark"; return 0; }; command="$rd"; _sg_judge_one "$rd" whole nocredit >/dev/null 2>"$X/n14a"; echo "$? $(kindf "$X/n14a") $([[ -e "$X/n14a.mark" ]] && echo credit-run || echo credit-skipped)" )
        [[ $r == "2 longline credit-skipped" ]]; chk $? V14-N1-nocredit-never-runs-credit "nocredit on a matching line over ${_SGV_LMAX:-8192}: status/text/credit [$r] (want [2 longline credit-skipped]); the credit must not be computed before the longline block" "[judged]"
      else miss V14-N1-nocredit-never-runs-credit; fi
    fi
    if sel V14-N2-longline-pattern-is-a-rule; then   # Q-22: the longline text names the matched RULE, not the (long) copy
      command="$rd"; _sg_judge_one "$rd" whole nocredit >/dev/null 2>"$X/n14b"; n14p=$(sed -n 's/^.*Matched pattern: //p' "$X/n14b" | head -n 1); n14n=$(wc -c < "$X/n14b"); n14m=no
      for n14r in "${risky_patterns[@]}"; do [[ "$n14p" == "$n14r" ]] && { n14m=yes; break; }; done
      [[ $n14m == yes && $n14n -lt 3000 ]]; chk $? V14-N2-longline-pattern-is-a-rule "the longline text: the matched pattern is one of the rules: $n14m; text $n14n bytes (want yes, under 3000: the copy must not stand in for the pattern)" "[text]"
    fi
    if sel V14-G1-triggers-return-4-with-the-baseline-reason; then   # Q-7 (and the copy-paste of the two reason strings): both trigger points hand over with status 4 and keep their own baseline reason
      if need _sg_vx_pass; then
        g1c="v=$x4; : \$v \$v \$v"; g1S=${_SGV_SMAX:-8192}
        g1w=$( _sg_relax_ok() { return 0; }; command=$g1c; _sg_vx_pass "$g1c" whole >/dev/null 2>&1; echo "$?|$_SG_OV_PAT|$_SG_OV_MODE" )
        g1s=$( _sg_relax_ok() { return 0; }; command=$g1c; _SG_SEGS=("v=$x4" ": \$v \$v \$v"); _sg_vx_pass "$g1c" segment >/dev/null 2>&1; echo "$?|$_SG_OV_PAT|$_SG_OV_MODE" )
        g1wa="4|the command is longer than $g1S characters after variable expansion|whole"; g1sa="4|a command segment is longer than $g1S characters after variable expansion|segment"
        t=''; [[ ${g1w%%|*} == 4 && ${g1s%%|*} == 4 ]] || t+='[status] '; [[ "$g1w" == "$g1wa" && "$g1s" == "$g1sa" ]] || t+='[text]'
        [[ -z "$t" ]]; chk $? V14-G1-triggers-return-4-with-the-baseline-reason "gate stubbed open, baseline pass, a copy over $g1S: whole [${g1w:0:140}] (want [$g1wa]); segment [${g1s:0:140}] (want [$g1sa])" "$t"
      else miss V14-G1-triggers-return-4-with-the-baseline-reason; fi
    fi
    if sel V14-G2-growth-limit-follows-gmax; then   # Q-31: the growth limit of the rerun is _SGV_GMAX over the input, not _SGV_SMAX (both are 8192 today: perturb them apart)
      if need _sg_vx_collect _sg_vx_apply; then
        g2c="v=$(printf '%*s' 300 '' | tr ' ' w); : \$v"
        g2a=$( _SG_RELAXED=1; _SGV_GMAX=100; _sg_vx_collect "$g2c" >/dev/null 2>&1; _sg_vx_apply "$g2c" >/dev/null 2>&1; echo $? )
        g2b=$( _SG_RELAXED=1; _SGV_GMAX=400; _SGV_SMAX=100; _sg_vx_collect "$g2c" >/dev/null 2>&1; _sg_vx_apply "$g2c" >/dev/null 2>&1; echo $? )
        [[ "$g2a $g2b" == "2 0" ]]; chk $? V14-G2-growth-limit-follows-gmax "relaxed _sg_vx_apply, growth 298: _SGV_GMAX 100 -> status $g2a (want 2); _SGV_GMAX 400 with _SGV_SMAX 100 -> status $g2b (want 0); the limit is the growth over the input" "[status]"
      else miss V14-G2-growth-limit-follows-gmax; fi
    fi
    if sel V14-F1-status-4-falls-back-to-the-baseline-block; then   # Q-29: _sg_per_segment_eval turns status 4 of a failed rerun into the baseline block (status 2 and its reason), whatever the host load
      awk '/^_sg_per_segment_eval\(\) \{/,/^\}$/' "$H" > "$X/pse.sh"
      if [[ ! -s "$X/pse.sh" ]]; then out SETUP V14-F1-status-4-falls-back-to-the-baseline-block "_sg_per_segment_eval not found by anchor"
      elif ! need _sg_emit_blocked _sg_time_budget; then miss V14-F1-status-4-falls-back-to-the-baseline-block
      else
        f1p="the command is longer than ${_SGV_SMAX:-8192} characters after variable expansion"
        f1r=$( source "$X/pse.sh"; _sg_core_eval() { _SG_MODE=whole; return 0; }; _sg_vx_pass() { _SG_OV_PAT="$f1p"; _SG_OV_MODE=whole; return 4; }; _sg_relax_run() { return 4; }; command="$rd"; _sg_per_segment_eval "$rd" >/dev/null 2>"$X/f1"; echo $? )
        f1l=$(head -n 1 "$X/f1"); f1w="[secret-guard] BLOCKED: command too large to scan for secrets. Limit hit: $f1p"
        t=''; [[ $f1r == 2 ]] || t+='[status] '; [[ "$f1l" == "$f1w" ]] || t+='[text]'
        [[ -z "$t" ]]; chk $? V14-F1-status-4-falls-back-to-the-baseline-block "_sg_per_segment_eval with a rerun that falls back (status 4): status $f1r (want 2), first line [${f1l:0:140}] (want [$f1w])" "$t"
      fi
    fi
'''

def apply(path, edits):
    t = open(path, encoding="utf-8", newline="").read()
    for old, new in edits:
        n = t.count(old)
        assert n == 1, "%s: anchor occurs %d times: %r" % (path, n, old[:70])
        t = t.replace(old, new)
    return t

H = WT + "/hooks/tests/lib/secret-guard-w10-direct.sh"
S = WT + "/hooks/tests/secret-guard.test.sh"
D = V31 + "/sc-direct.sh"
NID_OLD = 'V7-N12-lmax-edge-rows-only V7-N13-unmeasured-length-rows-only"'
NID_NEW = 'V7-N12-lmax-edge-rows-only V7-N13-unmeasured-length-rows-only\n    ' + IDLINE + '"'
INS_OLD = "  else nobelow $N_IDS; fi"
out = {
    H: apply(H, [
        ('V7-N9-segment-routes-to-big-judge V7-N13-unmeasured-length-rows-only"   # the cases of MODE relax',
         'V7-N9-segment-routes-to-big-judge V7-N13-unmeasured-length-rows-only\n' + IDLINE + '"   # the cases of MODE relax'),
        (NID_OLD, NID_NEW),
        (INS_OLD, BLOCK + INS_OLD)]),
    D: apply(D, [(NID_OLD, NID_NEW), (INS_OLD, BLOCK + INS_OLD)]),
    S: apply(S, [
        ('V7-N8-whole-branch-returns-big-judge V7-N9-segment-routes-to-big-judge V7-N13-unmeasured-length-rows-only"',
         'V7-N8-whole-branch-returns-big-judge V7-N9-segment-routes-to-big-judge V7-N13-unmeasured-length-rows-only\n' + IDLINE + '"'),
        ("Coverage: 967 cases (961 without zsh)", "Coverage: 972 cases (966 without zsh)"),
        ("# 136 of those cases are the W10", "# 141 of those cases are the W10")]),
}
for path, text in out.items():
    open(path, "w", encoding="utf-8", newline="").write(text)
print("patched:", ", ".join(sorted(out)))

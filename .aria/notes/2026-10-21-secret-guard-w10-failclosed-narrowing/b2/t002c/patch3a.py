#!/usr/bin/env python3
"""patch3a.py : T002c-3a. (1) lib/secret-guard-w10-direct.sh = v31/sc-direct.sh + the listed changes; (2) secret-guard.test.sh: header, the W10 block
after the helpers, the call before SC-13, SC-13 counts SKIP, the summary lists SKIP. Every replacement must hit exactly once. Run once, on the
unmodified suite (it refuses a suite that already has the block)."""
import sys, os
V = '/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31'
WT = '/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/wt217/aria'
SP = '/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/t002c'

def rep(t, old, new, label):
    n = t.count(old)
    if n != 1:
        sys.exit(f'{label}: hit {n} times: {old[:100]!r}')
    return t.replace(old, new)

RELAX_IDS = """V3-G9-clock-backwards V3-G10-cap-3 V3-G12-time-left-zero-padded
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
V7-N8-whole-branch-returns-big-judge V7-N9-segment-routes-to-big-judge V7-N13-unmeasured-length-rows-only"""

HEAD = """#!/usr/bin/env bash
# lib/secret-guard-w10-direct.sh HOOK MODE : the direct-call cases of the W10 fail-closed narrowing (10CG/aria-plugin#217), ported from v31/sc-direct.sh:
# ids, assertions, wanted values, reason tags and the sentinel unchanged. secret-guard.test.sh (sg_w10_cases) runs it with SC_BASH, the bash being tested,
# and turns its lines into PASS, FAIL or SKIP. MODE relax = a bash the relaxation is expected on (the gate must open; mechanism cases with a stubbed
# judgement at a 1 s deadline; growth, count, checkpoint and rows-only cases) | norelax = any other bash (the gate must stay closed; every case of the
# relaxation is reported once, as SKIP [platform], so both modes report the same ids). Changed from v31: the fallback-text cases (V6-S20, V6-S21) compare
# with the block the same hook writes when the gate is closed by WSL_DISTRO_NAME, set in the shell that sources it (no baseline file, no git history);
# a case whose tool is missing on the platform (ps) is SKIP [platform], not FAIL.
# The hook is sourced: it stops at its unit-test sourcing gate, so only the functions above that gate exist; risky_patterns, _sg_judge_one and
# _sg_redact_echo (below it) are pulled out by anchor, as the suite's SC-8 harness does. One line per case:
#   PASS|FAIL|MISSING|SETUP <id> <detail>   MISSING: a function the case calls is not defined in the hook under test (status 127 if it were called);
#                                            SETUP: the case could not be built (an injection anchor not found). The suite reports both as FAIL.
#   SKIP <id> [reason] <detail>             [platform]: see above; [root]: RLIMIT_NPROC does not bind this process, so no fork failure can be made
#                                            (post_planning R2 PP2-m2)
#   TIMED <id> <hard> <soft> <detail>       a case with a part that depends on the speed of the host: hard (ok|bad) = the checks no load explains
#                                            (status, text, bytes, lower bounds); soft (ok|bad) = the upper bound, or "the job finished before its
#                                            deadline". The suite turns it into PASS, FAIL or SKIP by the load rule of INV-7 (post_planning R2 PP2-A).
# A failed check names itself in the detail with a tag: [status] [rc] [stderr] [bytes] [value] [kind] [text] [count] [judged] [leftover] [wall<lo]
# [wall>hi] [fallback]. The last line is the sentinel "END sc-direct": a run that stops early (set -u, a crash) has none, and the suite reports that
# (V0-H1). SC_ONLY (set by the suite from SG_W10_ONLY) skips the slow cases that are not selected; the suite filters the lines again.
"""

# ---------------- (1) the helper ----------------
d = open(os.path.join(V, 'sc-direct.sh'), encoding='utf-8').read()
i = d.index('H=$1; MODE=$2; BASE=${3:-}\n')
d = HEAD + d[i:]
d = rep(d, 'H=$1; MODE=$2; BASE=${3:-}\n', 'H=$1; MODE=$2\n', 'args')
d = rep(d, 'WG=$(want_gate)\n', 'WG=$(want_gate)\nRELAX_IDS="' + RELAX_IDS + '"   # the cases of MODE relax; SKIP [platform] in MODE norelax\n', 'relax ids')
d = rep(d, "            # text written from it equals the baseline hook's own block for the same copy, byte for byte (R2 PP2-I)\n",
           "            # text written from it equals the block the same hook writes for the same copy with the gate closed by WSL_DISTRO_NAME, byte for\n"
           "            # byte (R2 PP2-I; v31 compares with the baseline hook's file)\n", 'fbt comment')
d = rep(d, '    [[ -n "$BASE" && -r "$BASE" ]] || { out SETUP "$id" "no baseline hook given (sc-direct.sh HOOK MODE BASE)"; return 0; }\n', '', 'fbt base check')
d = rep(d, "B=$1; OUT=$2; m=$3; c=$4; shift 4\nsource \"$B\" </dev/null >/dev/null 2>&1; set +e; input=''\n",
           "B=$1; OUT=$2; m=$3; c=$4; shift 4\n"
           "export WSL_DISTRO_NAME=Ubuntu   # the gate's closing switch, set in the shell that sources the hook: it writes its gate-closed block\n"
           "source \"$B\" </dev/null >/dev/null 2>&1; set +e; input=''; _SG_P0=${EPOCHREALTIME:-}   # an anchor: only the WSL mark closes the gate\n", 'basefb')
d = rep(d, 'rb=$("$BASH" "$X/basefb.sh" "$BASE" "$X/fb-base" "$m" "$c" "$@")', 'rb=$("$BASH" "$X/basefb.sh" "$H" "$X/fb-base" "$m" "$c" "$@")', 'basefb call')
d = rep(d, "vs the baseline's block (status $rb)", "vs the same hook's block with the gate closed by WSL_DISTRO_NAME (status $rb)", 'fbt detail')
d = rep(d, '    if need _sg_relax_run _sg_relax_job; then\n      n=$(lv "7.777$U")',
           '    if ! command -v ps >/dev/null 2>&1; then out SKIP V5-S13b-nothing-outlives-the-run "[platform] ps not found: the processes left behind cannot be counted"\n'
           '    elif need _sg_relax_run _sg_relax_job; then\n      n=$(lv "7.777$U")', 'ps S13b')
d = rep(d, '  if sel V5-S12-no-leftovers; then\n',
           '  if sel V5-S12-no-leftovers && ! command -v ps >/dev/null 2>&1; then out SKIP V5-S12-no-leftovers "[platform] ps not found: the stub processes left behind cannot be counted"\n'
           '  elif sel V5-S12-no-leftovers; then\n', 'ps S12')
d = rep(d, '  else nobelow $N_IDS; fi\nfi\necho "END sc-direct"\n',
           '  else nobelow $N_IDS; fi\n'
           'else\n'
           '  # MODE norelax: the relaxation is not expected on this bash. Each of its cases is reported once, as SKIP [platform], so the list of ids is the same\n'
           '  # on every platform (the suite\'s V0-H2)\n'
           '  for id in $RELAX_IDS; do\n'
           '    sel "$id" && out SKIP "$id" "[platform] the relaxation is not expected on this bash (${BASH_VERSINFO[5]} ${BASH_VERSINFO[0]}.${BASH_VERSINFO[1]}, kernel ${OSR:-<none>}${WSLM:+, WSLInterop}): MODE norelax"\n'
           '  done\n'
           'fi\necho "END sc-direct"\n', 'norelax skip')
assert 'BASE' not in d.replace('_SG_', ''), 'a BASE reference is left'
os.makedirs(os.path.join(WT, 'hooks/tests/lib'), exist_ok=True)
hp = os.path.join(WT, 'hooks/tests/lib/secret-guard-w10-direct.sh')
open(hp, 'w', encoding='utf-8', newline='').write(d)
os.chmod(hp, 0o755)

# ---------------- (2) the suite ----------------
tp = os.path.join(WT, 'hooks/tests/secret-guard.test.sh')
t = open(tp, encoding='utf-8', newline='').read()
assert '\r' not in t, 'CRLF in the suite'
assert 'sg_w10_cases' not in t, 'the suite is already patched'
blk = open(os.path.join(SP, 'w10-block.sh'), encoding='utf-8').read()
t = rep(t, '# Coverage: 831 cases (825 without zsh) across', '# Coverage: 967 cases (961 without zsh) across', 'coverage')
t = rep(t, '# count here has already misled one spec into planning against "~50".\n',
        '# count here has already misled one spec into planning against "~50".\n'
        '#\n'
        '# 136 of those cases are the W10 fail-closed narrowing (10CG/aria-plugin#217) acceptance cases ported from\n'
        '# v31 (sg_w10_cases, after the helpers; ids V<k>-... and the harness checks V0-H1 / V0-H2): the direct calls in\n'
        '# lib/secret-guard-w10-direct.sh, the end-to-end and static ones in this file. They run the hook with SC_BASH\n'
        '# (default: bash on PATH); every older case runs it as before. lib/sg-shim/delay-first, linked as jq and sed\n'
        '# (relative symlinks), puts fixed delays at known points of the hook for the deadline cases; the end-to-end\n'
        '# cases also need timeout (coreutils). Two switches: SG_W10_ONLY=<regex> runs only the ported cases whose id\n'
        '# matches (no other case and no SC-13; the summary says it is a filtered round); SG_W10_LOG=<file> writes one\n'
        '# line per ported case, "PASS|FAIL|SKIP <id> <detail>" with v31\'s reason tags. A ported case that cannot be\n'
        '# judged here is SKIP with its reason: [platform] (the relaxation is not expected on SC_BASH, or a tool is\n'
        '# missing), [load] / [void] (the timing batch, INV-7: one-minute load under 2 at the start and at the end),\n'
        '# [inconclusive], [root]. Every ported id is reported exactly once on every platform, so SKIP counts in the\n'
        '# Coverage total and in SC-13, is listed on its own in the summary, and never fails the run.\n', 'header text')
t = rep(t, '# ── BLOCK cases (exit 2) — Nomad / Vault / cloud / managers ───────────────\n',
        blk + '# ── BLOCK cases (exit 2) — Nomad / Vault / cloud / managers ───────────────\n', 'block')
t = rep(t, '# ── TASK-020 (SC-13): SOT 计数回填断言',
        '# the W10 cases ported from v31 (sg_w10_cases, after the helpers): last before SC-13, which counts their SKIP\nsg_w10_cases\n\n'
        '# ── TASK-020 (SC-13): SOT 计数回填断言', 'call')
t = rep(t, '使 pass+fail+1 (含本条自己) = 最终 total', '使 pass+fail+skip+1 (含本条自己) = 最终 total', 'sc13 comment')
t = rep(t, 'sc13_total_expected=$((pass + fail + 1))', 'sc13_total_expected=$((pass + fail + skip + 1))', 'sc13 total')
t = rep(t, 'total=$((pass + fail))\n', 'total=$((pass + fail + skip))\n', 'summary total')
t = rep(t, 'echo "secret-guard.sh regression test"\necho "PASS: $pass / $total"\necho "FAIL: $fail / $total"\n',
        'echo "secret-guard.sh regression test"\necho "PASS: $pass / $total"\necho "FAIL: $fail / $total"\n'
        'echo "SKIP: $skip / $total ($(sg_w10_skips))"\necho "W10 ported cases: $sg_w10_batch"\n', 'summary skip')
open(tp, 'w', encoding='utf-8', newline='').write(t)
print('patched: helper', len(d.splitlines()), 'lines; suite', len(t.splitlines()), 'lines')

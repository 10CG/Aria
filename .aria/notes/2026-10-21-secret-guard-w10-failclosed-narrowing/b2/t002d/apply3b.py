#!/usr/bin/env python3
"""apply3b.py suite <suite> | cs <commentsync.py> <base suite> <target suite> | verify <suite>
TASK-002 step 3b (10CG/aria-plugin#217). `suite` edits hooks/tests/secret-guard.test.sh in place (every anchor must match exactly once);
`cs` adds the suite's sentence level to v31/commentsync.py (only additions); `verify` counts anchors, old titles and ADD words in a suite."""
import re, sys

def runs(path):   # commentsync.py's reading of comment runs, verbatim
    out, cur = [], []
    for ln in open(path, encoding='utf-8').read().split('\n'):
        m = re.match(r'\s*#(.*)$', ln)
        if m and not ln.lstrip().startswith('#!'):
            cur.append(m.group(1))
        else:
            if cur: out.append((re.sub(r'\s+', ' ', ' '.join(cur)).strip(), ln)); cur = []
    if cur: out.append((re.sub(r'\s+', ' ', ' '.join(cur)).strip(), ''))
    return out

def site_run(R, loc):
    kind, key = loc
    for txt, nxt in R:
        if (kind == 'next' and nxt.startswith(key)) or (kind == 'has' and key in txt): return txt
    return None

def block(text):
    return text.strip('\n').split('\n')

EXPECTS = r'''
# Expects: bash 5.0 or later to run the suite itself: it runs under `set -u`, and SC-8's timing helpers and sg_w10_run
# read $EPOCHREALTIME directly, which bash 4.x and 3.2 do not set, so the suite aborts there (SC_BASH, the bash that
# runs the hook in the ported W10 cases, is not bound by this). External tools: jq; python3 (the #128 SC-20
# internal-error-injection cases, which make two modified hook copies by precise text replacement, and the SC-19
# census, corpus_census.py); timeout from coreutils (the ported W10 end-to-end cases); ps (two ported W10 cases in
# lib/secret-guard-w10-direct.sh, SKIP [platform] without it); git (SC-8 and the pre-change part of SC-9a read the
# hook of af87cae through git show: outside a git checkout that reaches it they print a [SKIP] line and are not
# counted). zsh is optional: 6 cases run only with it.
'''

RELAX_RULE = r'''
sg_w10_relax_rule() {   # MACH MAJ MIN OSRELEASE WSLINTEROP(yes|no) -> status 0 where the gate's platform rule (What 1 and its supplement) lets the relaxation in
  [[ "${1:-}" == x86_64-*-linux-gnu* && -n "${4:-}" && "${4:-}" != *[Mm]icrosoft* && "${4:-}" != *WSL* && "${5:-yes}" == no ]] && (( ${2:-0} == 5 && ${3:-0} <= 3 ))
}
'''

FIRST_CALL = r'''
# The ported W10 cases run here, once, first: before every older case (3a ruling (1), 2026-10-24). Run at the end of the suite, their timing batch read a
# one-minute load that held the suite's own load from the older cases (2.10 or more at the start of the batch in every whole round of 3a), so the batch was never
# judged; the threshold (2) and the batch's two readings, at its start and at its end, are unchanged. SC-13 at the end counts their SKIP. SG_W10_ONLY: a
# filtered round -- only the ported cases whose id matches; no other case and no SC-13.
sg_w10_cases
if [[ -n "${SG_W10_ONLY:-}" ]]; then
'''

SITE9 = r'''
# ── review M6 (TASK-014): the second pass has a LENGTH BUDGET -- three limits, each pinned to the character on both sides (21aa-21ap) ──
# Without them the judged copy is the segment plus references x value length, one level of chaining multiplies a value by 8 per level, and the pass overran the 5 s hook
# timeout on a 5 KB command (a timeout lets the command through). Owner ruling 2026-10-14, narrowed by 10CG/aria-plugin#217 (owner rulings A and E, 2026-10-23): a value
# over the value limit, or copies over the pass-wide limit, block the command on every platform -- exit 2 with the "command too large to scan for secrets ... split it"
# text, not the finding text -- and are never passed (P9); a copy over the copy limit is blocked that way only where the relaxation is not in effect (What 1 and its
# supplement: another platform or bash version, WSL, a project extension, or no time left; P2). Where it is in effect the pass is re-run under a hard deadline with the
# relaxed rules (What 1): a copy that grows by more than _SGV_GMAX over its input is blocked with the growth text (P8, What 5), a copy over _SGV_SMAX whose longest line is
# longer than _SGV_LMAX is matched against the rows only and a match blocks with the longline text (P7, What 5), and any other copy is judged as usual, so it may pass
# (R-a). The COUNT bounds of the baseline pass, 21y, still pass (P9). After the flip both sides of a limit exit 2 wherever a row matches (in the relaxed branch the outside
# of the copy limit passes when none does, 21ab), so the exit code alone does not tell "judged" from "refused": the text does. wpa_x_finding = the call was judged and
# blocked as a finding (the shared BLOCKED text, not the size text); wpa_x_toolarge = it was refused as too large (the size text, not the finding text). Every limit is
# pinned from both sides. In the cases that the relaxation does not change, and in the baseline branch of the six groups that it changes (21ab, 21ac, 21ag, 21aj, 21al,
# 21ao; the branch is chosen once, below: wpa_rx6), the inside asserts the first helper and the outside the second, so a limit one too low or too high swaps the text of
# a side and turns a case red, and an overrun there that passes (exit 0, the fail-open M6) or draws the finding text turns the outside red. In the relaxed branch of the
# six groups wpa_x_hit asserts the ordinary finding text (value-REDACTING filter, and not the longline text), wpa_x_longline the longline text (has a line longer than ...
# Matched pattern:), and wpa_x_toolarge the growth line where a copy grows too much: wpa_x_finding cannot tell the ordinary finding text from the longline text, both say
# that the command reads a secret-bearing source (PP1-A12). The numbers are part of the contract (_SGV_SMAX 8192 = the longest copy the baseline pass builds, _SGV_VMAX
# 4096 = one collected value, _SGV_TMAX 65536 = all copies of one command; in the relaxed rerun _SGV_GMAX 8192 = the most a copy may grow over its input, _SGV_LMAX 8192 =
# the longest line of a copy over _SGV_SMAX that is still judged with credit); changing one means changing these cases. The pad value p has 4000 characters: every `$p`
# adds 3998 to a copy, the reader `$f` (the 20-character app.ini name) adds 18.
'''

HELPERS = r'''
# The six groups whose outcome the relaxation of 10CG/aria-plugin#217 changes (21ab, 21ac, 21ag, 21aj, 21al, 21ao) assert in two branches (the plan's design, suite (1)
# supplement (iv); owner ruling E). The branch is chosen once, here, by the gate's platform rule of What 1 and its supplement (sg_w10_relax_rule, the rule that sets
# SGW_RELAX for the ported cases), asked of the bash that runs these cases: wpa_err runs the hook file itself, so its shebang (/usr/bin/env bash) picks the bash on PATH,
# not SC_BASH. These cases pass the suite's environment to the hook, so WSL_DISTRO_NAME or WSL_INTEROP set in it closes the gate as well (the ported cases clear both).
# None of the six runs in a project (wpa_use_none), so the gate's extension condition holds; its time condition holds unless the host is too slow for the deadline.
# wpa_rx6=yes: the relaxation is expected and a group asserts the outcome the proposal gives (its comment names the What / P item); wpa_rx6=no: the group keeps its
# baseline assertions word for word. Either way a group is one case, so the count does not depend on the platform (SC-13). The summary prints the branch and its inputs.
wpa_rx6=no; wpa_rx6_mach=''; wpa_rx6_maj=''; wpa_rx6_min=''; wpa_rx6_ver=''; wpa_rx6_osr=$(cat /proc/sys/kernel/osrelease 2>/dev/null); wpa_rx6_wslf=no
[[ -e /proc/sys/fs/binfmt_misc/WSLInterop ]] && wpa_rx6_wslf=yes
read -r wpa_rx6_mach wpa_rx6_maj wpa_rx6_min wpa_rx6_ver < <(env bash -c 'echo "${BASH_VERSINFO[5]} ${BASH_VERSINFO[0]} ${BASH_VERSINFO[1]} $BASH_VERSION"' 2>/dev/null)
sg_w10_relax_rule "$wpa_rx6_mach" "$wpa_rx6_maj" "$wpa_rx6_min" "$wpa_rx6_osr" "$wpa_rx6_wslf" && [[ -z "${WSL_DISTRO_NAME:-}${WSL_INTEROP:-}" ]] && wpa_rx6=yes
wpa_rx6_note="$([[ $wpa_rx6 == yes ]] && echo 'relaxed branch (new outcomes)' || echo 'baseline branch (assertions as before)') | bash on PATH $(command -v bash) ${wpa_rx6_ver:-?} (machtype ${wpa_rx6_mach:-?}) | osrelease ${wpa_rx6_osr:-unreadable} | WSLInterop $wpa_rx6_wslf | WSL_DISTRO_NAME '${WSL_DISTRO_NAME:-}' WSL_INTEROP '${WSL_INTEROP:-}'"
wpa_L_gseg='a command segment grows by more than 8192 characters after variable expansion'   # the growth line of the relaxed rerun, segment mode (What 5; _SGV_GMAX 8192)
wpa_x_longline() {   # <command>: (relaxed branch) judged in full and blocked with the longline text of What 5: a row matched on a line longer than _SGV_LMAX
  local e p="${1//$wpa_nl/ }"; e="$(wpa_err Bash "$1")"
  wpa_chk "longline [${p:0:48}]: exit code" 2 "${e##*WPA_RC=}"
  wpa_chk "longline [${p:0:48}]: has a line longer than" yes "$([[ "$e" == *"has a line longer than"* ]] && echo yes || echo no)"
  wpa_chk "longline [${p:0:48}]: Matched pattern:" yes "$([[ "$e" == *"Matched pattern:"* ]] && echo yes || echo no)"
  wpa_chk "longline [${p:0:48}]: not the size text" no "$([[ "$e" == *"too large to scan"* ]] && echo yes || echo no)"
  wpa_chk "longline [${p:0:48}]: short (the first 200 characters of the command, no triggering segment)" yes "$([[ ${#e} -lt 3000 ]] && echo yes || echo no)"
}
wpa_x_hit() {   # <command>: (relaxed branch) judged and blocked with the ordinary finding text -- value-REDACTING filter, and not the longline text (PP1-A12)
  local e p="${1//$wpa_nl/ }"; e="$(wpa_err Bash "$1")"
  wpa_chk "finding [${p:0:48}]: exit code" 2 "${e##*WPA_RC=}"
  wpa_chk "finding [${p:0:48}]: value-REDACTING filter" yes "$([[ "$e" == *"value-REDACTING filter"* ]] && echo yes || echo no)"
  wpa_chk "finding [${p:0:48}]: not the longline text" no "$([[ "$e" == *"has a line longer than"* ]] && echo yes || echo no)"
}
'''

SITE10 = r'''
# 21aa / 21ab: the segment ` echo $p $p<filler> | cat $f` has 20 characters + the filler and becomes 2 x 4000 + 34 + filler: a 158-character filler makes exactly 8192, 159 makes 8193.
# 21aa's copy (8192) is not over the copy limit, so it is not a trigger point of the relaxation: it is judged and its reader found on every platform (What 1, P1). 21ab's
# three commands are over it: the 8193-character copy, a 9000-character segment with a one-character value and one reference, and a segment of short words (nothing the
# echo's redaction would cut away). Where the relaxation is not in effect all three are refused as too large, the baseline bytes (P2): the limit counts the whole copy, not
# its growth, so a tiny value behind one reference is refused too (so is a big heredoc that happens to hold `x=1` and `$x`), and the size text echoes only the START of
# the command. 10CG/aria-plugin#217 narrowed that posture on purpose (owner ruling A): where the relaxation is in effect the copy limit of the rerun is the growth over the
# input (_SGV_GMAX, P8) and none of the three grows by that much, so each copy is judged in full (What 1, R-a); each is one line longer than _SGV_LMAX, so it is matched
# against the rows only (P7): the first, whose reader matches a row, is blocked with the longline text (What 5), and the other two hold no reader, match no row and pass
# (R-a). Red when (21ab), where the relaxation is not in effect: a command passes (exit 0 -- the fail-open M6), is refused with the finding text or by another limit line,
# the limit is 8191 / 8193 (21aa and 21ab swap sides), or the size text echoes the whole command; where it is in effect: the first command passes, is refused as too large
# or draws the ordinary finding text, or one of the other two is blocked.
'''

SITE11 = r'''
# 21ac / 21ad: a collected value of exactly 4096 characters (a path that ends in the app.ini name) is expanded and its read found, one character more refuses the command.
# The list of a for statement is the third place a value is collected: 3000 characters are expanded and the read is found on every platform (the list stays in the
# command, so the copy holds it twice, about 6 KB: inside the copy limit, not a trigger point of the relaxation, P1), and 4097 refuses the command by the value limit on
# every platform (P9). A 4096-character list makes a copy over the copy limit (2 x 4096 and the rest). Where the relaxation is not in effect that copy is refused by the
# COPY limit with the size text, not by the value limit (P2); where it is in effect the copy grows by about 4 KB over the input, under _SGV_GMAX, so it is judged in full,
# and as its one line is longer than _SGV_LMAX the read is blocked with the longline text (P7, What 5). The two reads inside the limits draw the ordinary finding text on
# every platform (P1), which the relaxed branch checks with wpa_x_hit: not the longline text. 21ad's second command pins the posture of the value limit: the variable does
# not have to be MENTIONED -- an oversize assignment blocks the command on its own ("absolutely not passed"), as soon as the command holds a `$` at all (the collector's
# entry gate: with no `$` nothing could be expanded and nothing is refused). A reference check would narrow that, and narrowing is the owner's call, not the code's. Red
# when (21ad): an oversize value is dropped and the command passes (exit 0 -- the fail-open M6), in the assignment, in the for list or in the command that never mentions
# it, or the value is refused by another limit line; (21ac), where the relaxation is not in effect: the 4096-character for list is refused by the value limit instead of the
# copy limit; where it is in effect: that list passes, is refused as too large or draws the ordinary finding text instead of the longline text, or a read inside the limits
# draws the longline text.
'''

SITE12 = r'''
# 21ag: the dense copy (about 36 KB in one segment) is over the copy limit, and it grows by far more than _SGV_GMAX over its input: it is refused as too large on every
# platform, only the limit line differs -- the copy limit where the relaxation is not in effect (P2), the growth line of the rerun where it is (P8, What 5: "a command
# segment grows by more than 8192 characters after variable expansion"). Red when (21ag): the command passes (exit 0 -- the fail-open M6), or the refusal names a limit
# line other than its branch's.
'''

SITE13 = r'''
# 21aj: each heavy segment ` echo $p $p $p` makes a copy of about 12 KB, over the copy limit, that grows by about 12 KB over its own text, over _SGV_GMAX as well: the
# first of them ends the pass, the command is refused at once and the reader behind it is never judged -- by the copy limit where the relaxation is not in effect (P2),
# by the growth line of the rerun where it is (P8, What 5). (The fail-open M6 refused such a segment cheaply but counted it as a whole copy, 8192, against the pass-wide
# limit: after seven of them the reader was still judged and blocked, after eight it passed.) Red when (21aj): a heavy segment does not refuse the command -- the finding
# text after seven of them, exit 0 after eight (the fail-open M6) -- or the refusal names a limit line other than its branch's.
'''

SITE21 = r'''
# 21al: the braced form ${NAME} goes through the same copy limit as $NAME (through _sg_vx_replace, not through the $NAME loop). A brace makes the command unsafe to split,
# so the unit is the WHOLE command: with a 2700-character pad value, `f=<app.ini>; p=<pad>; echo ${p} ${p}<filler> | cat ${f}` has 53 + 2700 + filler characters and its
# copy 2 x 2696 + 16 more -- 8161 + filler, so a 31-character filler makes exactly 8192. Exactly 8192 is not over the limit: it is judged, with the ordinary finding text,
# on every platform (P1). 8193 is refused as too large where the relaxation is not in effect (P2); where it is in effect the whole copy grows by about 5.4 KB over the
# input, under _SGV_GMAX, so it is judged in full, and as its one line is longer than _SGV_LMAX its read is blocked with the longline text (P7, What 5).
'''

SITE14 = r'''
# Red when (21al): either command passes (exit 0 -- the fail-open M6), the edge moves by one (the two commands swap sides), or the 8193-character copy draws a text other
# than its branch's: the size text that names the whole-command limit where the relaxation is not in effect, the longline text where it is.
'''

SITE22 = r'''
# 21ao: whole-command mode (the command degrades because of a `(`) meets the same copy limit -- the unit is the whole command: 6069 + filler, so a 2123-character filler
# makes 8192. Exactly 8192 is not over the limit: it is judged, with the ordinary finding text, on every platform (P1). 8193 is refused as too large where the relaxation
# is not in effect (P2); where it is in effect the whole copy grows by about 4 KB over the input, under _SGV_GMAX, so it is judged in full, and as its one line is longer
# than _SGV_LMAX its read is blocked with the longline text (P7, What 5).
'''

SITE15 = r'''
# Red when (21ao): either command passes (exit 0 -- the fail-open M6), the edge moves by one (the two commands swap sides), or the 8193-character copy draws a text other
# than its branch's: the size text that names the whole-command limit where the relaxation is not in effect, the longline text where it is.
'''

T16 = 'W10 SC-21ab bf: copy limit exceeded — 8193 characters, or a 9000-character segment with a one-character value: refused as too large where the relaxation is not in effect; where it is, each copy is judged in full: the reader is blocked with the longline text, the two commands with no reader pass'
T17 = 'W10 SC-21ag bf: the dense shape of the review (15 assignments of 300 B, 8 references each: a 36 KB copy; 16 x 300 B x 8 took 5.4 s) is refused as too large on every platform — by the copy limit where the relaxation is not in effect, by the growth limit where it is'
T18 = 'W10 SC-21aj bf: a segment over the copy limit that also grows over the growth limit ends the pass — with one, seven or eight of them in front of the reader the command is refused as too large (the copy limit, or the growth limit where the relaxation is in effect) and the reader is never judged'
T19 = 'W10 SC-21al bf: the braced form meets the same copy limit — a substituted whole command of exactly 8192 characters is judged and blocked; 8193 is refused as too large where the relaxation is not in effect and blocked with the longline text where it is'
T20 = 'W10 SC-21ao bf: whole-command mode meets the same copy limit — a whole copy of exactly 8192 characters is judged and blocked; 8193 is refused as too large where the relaxation is not in effect and blocked with the longline text where it is'

R21AB = r'''
wpa_x_longline "$(wpa_vx_cmd 159)"; wpa_x Bash 0 "f=x; echo \$f$(wpa_vx_fill 9000)"
wpa_x Bash 0 "f=x; echo \$f$(wpa_rep a 4500 | sed 's/a/ a/g')"
'''
R21AC = r'''
wpa_x_hit "f=$(wpa_vx_val 4096); cat \$f"; wpa_x_hit "for f in $(wpa_vx_val 3000); do cat \"\$f\"; done"
wpa_x_longline "for f in $(wpa_vx_val 4096); do cat \"\$f\"; done"
'''
R21AJ = r'''
wpa_x_toolarge "$(wpa_vx_over 1)" "$wpa_L_gseg"; wpa_x_toolarge "$(wpa_vx_over 7)" "$wpa_L_gseg"; wpa_x_toolarge "$(wpa_vx_over 8)" "$wpa_L_gseg"
'''
R21AL = r'''wpa_x_hit "$(wpa_vx_braced 31)"; wpa_x_longline "$(wpa_vx_braced 32)"'''
R21AO = r'''wpa_x_hit "$(wpa_vx_whole 2123)"; wpa_x_longline "$(wpa_vx_whole 2124)"'''

def patch_suite(path):
    src = open(path, encoding='utf-8').read()
    assert '\r' not in src
    L = src.split('\n')
    def find(pred, what):
        h = [i for i, s in enumerate(L) if pred(s)]
        assert len(h) == 1, f'{what}: {len(h)} hits'
        return h[0]
    def upto(i, pred, what):
        for j in range(i + 1, len(L)):
            if pred(L[j]): return j
        raise AssertionError(f'{what}: no end')
    def group(prefix, title, relaxed, n_old, keep_title=False):
        i = find(lambda s: s.startswith(prefix), prefix)
        j = upto(i, lambda s: s == 'wpa_end_case', prefix + ' end')
        old = L[i + 1:j]; assert len(old) == n_old, (prefix, old)
        head = [L[i]] if keep_title else ['wpa_begin_bash_case "' + title + '"']
        L[i:j + 1] = head + ['if [[ $wpa_rx6 == yes ]]; then'] + relaxed + ['else'] + old + ['fi', 'wpa_end_case']
    def comment(prefix, nxt, n, new):
        i = find(lambda s: s.startswith(prefix), prefix)
        j = find(lambda s: s.startswith(nxt), nxt) if nxt else i + n
        assert j == i + n and all(L[k].startswith('#') for k in range(i, j)), (prefix, i, j)
        L[i:j] = new
    # head comment
    i = find(lambda s: s.startswith('# Expects: jq installed. python3 installed'), 'Expects')
    assert L[i + 1].startswith('# internal-error-injection cases') and L[i + 2].startswith('# copies via precise text replacement')
    L[i:i + 3] = block(EXPECTS)
    i = find(lambda s: s.startswith('# Coverage: 967 cases (961 without zsh) across Bash'), 'Coverage')
    L[i] = L[i].replace('(961 without zsh) across', '(961 without zsh), counted in a git checkout of aria, across', 1)
    i = find(lambda s: s.startswith('# v31 (sg_w10_cases, after the helpers; ids'), 'head v31')
    L[i] = L[i].replace('(sg_w10_cases, after the helpers; ids', '(sg_w10_cases, defined after the helpers and run once, before every older case; ids', 1)
    old = 'sg_w10_cases runs just before SC-13 (which counts its SKIP), or alone when SG_W10_ONLY is set (below).'
    i = find(lambda s: old in s, 'ported block head')
    L[i] = L[i].replace(old, 'sg_w10_cases runs once, right after its definition, before every older case (3a ruling (1)); SC-13 at the end counts its SKIP; with SG_W10_ONLY set the round ends after it.')
    # one rule for the gate, used by SGW_RELAX and by the six older groups
    i = find(lambda s: s.startswith('sg_w10_sel() {'), 'sg_w10_sel')
    L[i + 1:i + 1] = block(RELAX_RULE)
    i = find(lambda s: s == '  [[ "$MACH" == x86_64-*-linux-gnu* && -n "$OSR" && "$OSR" != *[Mm]icrosoft* && "$OSR" != *WSL* && $WSLF == no ]] && (( MAJ == 5 && MIN <= 3 )) && SGW_RELAX=yes', 'SGW_RELAX rule')
    L[i] = '  sg_w10_relax_rule "$MACH" "$MAJ" "$MIN" "$OSR" "$WSLF" && SGW_RELAX=yes'
    # the ported batch runs first; the call before SC-13 goes
    i = find(lambda s: s == '# SG_W10_ONLY: a filtered round -- only the ported cases whose id matches; no other case and no SC-13', 'filter comment')
    assert L[i + 1] == 'if [[ -n "${SG_W10_ONLY:-}" ]]; then' and L[i + 2] == '  sg_w10_cases'
    L[i:i + 3] = block(FIRST_CALL)
    i = find(lambda s: s == '# the W10 cases ported from v31 (sg_w10_cases, after the helpers): last before SC-13, which counts their SKIP', 'old call')
    assert L[i + 1] == 'sg_w10_cases'
    L[i:i + 2] = ['# (the W10 cases ported from v31 ran first, before every older case: see the call right after the definition of sg_w10_cases; SC-13 below counts their SKIP)']
    i = find(lambda s: s == 'echo "W10 ported cases: $sg_w10_batch"', 'summary')
    L[i + 1:i + 1] = ['echo "W10 older groups 21ab 21ac 21ag 21aj 21al 21ao: ${wpa_rx6_note:-branch not chosen}"']
    # the W10 block of the older cases: 7 comment blocks, 2 adjacent heads, 5 titles, the branch and its helpers
    comment('# ── review M6 (TASK-014): the second pass has a LENGTH BUDGET', 'wpa_rep() {', 9, block(SITE9))
    comment('# 21aa / 21ab: the segment', 'wpa_vx_cmd() {', 6, block(HELPERS) + block(SITE10))
    group('wpa_begin_bash_case "W10 SC-21ab bf: copy limit exceeded is refused', T16, block(R21AB), 2)
    comment('# 21ac / 21ad: a collected value of exactly 4096', 'wpa_vx_val() {', 7, block(SITE11))
    group('wpa_begin_bash_case "W10 SC-21ac bf: value limit, last accepted', None, block(R21AC), 2, keep_title=True)
    comment('# Red when (21ag): the 36 KB dense copy passes', None, 1, block(SITE12))
    i = find(lambda s: s.startswith('wpa_begin_bash_case "W10 SC-21ag bf: the dense shape of the review'), '21ag')
    tail = '; wpa_x_toolarge "$(wpa_vx_dense 300)" "$wpa_L_seg"; wpa_end_case'
    assert L[i].endswith(tail) and L[i - 1].startswith('#')
    L[i:i + 1] = ['wpa_begin_bash_case "' + T17 + '"', 'if [[ $wpa_rx6 == yes ]]; then', 'wpa_x_toolarge "$(wpa_vx_dense 300)" "$wpa_L_gseg"', 'else',
                  'wpa_x_toolarge "$(wpa_vx_dense 300)" "$wpa_L_seg"', 'fi', 'wpa_end_case']
    comment('# 21aj: a segment whose copy is over the copy limit ends the pass', 'wpa_vx_over() {', 3, block(SITE13))
    group('wpa_begin_bash_case "W10 SC-21aj bf: a segment over the copy limit ends the pass', T18, block(R21AJ), 1)
    comment('# 21al: the copy limit holds for the braced form', 'wpa_vx_braced() {', 3, block(SITE21))
    comment('# Red when (21al): the braced 8193-character whole copy passes', None, 1, block(SITE14))
    group('wpa_begin_bash_case "W10 SC-21al bf: the copy limit holds for the braced form too', T19, [R21AL], 1)
    comment('# 21ao: whole-command mode (the command degrades because of a `(`) obeys', 'wpa_vx_whole() {', 1, block(SITE22))
    comment('# Red when (21ao): the 8193-character whole copy passes', None, 1, block(SITE15))
    group('wpa_begin_bash_case "W10 SC-21ao bf: whole-command mode obeys the copy limit', T20, [R21AO], 1)
    open(path, 'w', encoding='utf-8').write('\n'.join(L))
    print('suite patched')

LOCS = [('9 test W10 block head (3b)', ('next', 'wpa_rep() {')), ('10 test 21aa/21ab (3b)', ('next', 'wpa_vx_cmd() {')),
        ('11 test 21ac/21ad (3b)', ('next', 'wpa_vx_val() {')), ('12 test 21ag (3b)', ('next', 'wpa_begin_bash_case "W10 SC-21ag')),
        ('13 test 21aj (3b)', ('next', 'wpa_vx_over() {')), ('14 test 21al (3b)', ('next', 'wpa_begin_bash_case "W10 SC-21al')),
        ('15 test 21ao (3b)', ('next', 'wpa_begin_bash_case "W10 SC-21ao')), ('21 test 21al head (3b)', ('next', 'wpa_vx_braced() {')),
        ('22 test 21ao head (3b)', ('next', 'wpa_vx_whole() {'))]

CS_COMMENT = r'''
# Suite sentences (TASK-002 step 3b, 2026-10-24): sites 9-15, 21 and 22 at the sentence level, as HOOK_TEXT does for the hook. Per site: the sentences of the
# baseline run that the rewrite removed (cut mechanically after '.' and ';' from the run of aria 59e333c; a sentence the rewrite kept word for word is not listed)
# -- in the baseline each is in its run, in the target none is anywhere in the comments; and the sentences of the 3b rewrite (true on both branches of the six
# groups: where the relaxation is in effect and elsewhere) -- in the target each is in the site's own run, found by its locator (the code line right after the
# run), in the baseline none is anywhere in the comments. The lists were generated by cutting the baseline run and the rewritten run the same way and keeping
# what only one of them holds; they were not typed. The titles (sites 16-20), the anchors, the run hashes and ADD_SUITE stay as above.
'''

CS_FUNC = r'''
def check_suite_text(R, joined):   # TASK-002 step 3b: the suite sites at the sentence level (SUITE_TEXT), like check_text for the hook
    for site, loc, untrue, new in SUITE_TEXT:
        run = site_run(R, loc)
        if run is None: say(False, 'site', site, 0, f'no comment run found by {loc}')
        for u in untrue:
            n = (run or '').count(u) if mode == 'baseline' else joined.count(u)
            say((n >= 1) if mode == 'baseline' else (n == 0), 'old', site, n, u)
        for u in new:
            n = joined.count(u) if mode == 'baseline' else (run or '').count(u)
            say((n == 0) if mode == 'baseline' else (n >= 1), 'new', site, n, u)
'''

def patch_cs(cs, base, target):
    src = open(cs, encoding='utf-8').read()
    assert 'SUITE_TEXT' not in src and '\r' not in src
    RB, RT = runs(base), runs(target)
    cut = lambda t: re.split(r'(?<=[.;])\s+', t)
    lit = ['SUITE_TEXT = [  # site, locator, untrue sentences of the baseline run, new sentences of the 3b rewrite']
    for site, loc in LOCS:
        b, t = site_run(RB, loc), site_run(RT, loc)
        assert b and t, site
        old = [s for s in cut(b) if s not in t]
        new = [s for s in cut(t) if s not in b]
        assert old and new, site
        print(f'{site}: {len(old)} old, {len(new)} new, {len(cut(b)) - len(old)} kept')
        lit.append(f' ({site!r}, {loc!r},')
        lit.append('  [' + ',\n   '.join(repr(s) for s in old) + '],')
        lit.append('  [' + ',\n   '.join(repr(s) for s in new) + ']),')
    lit.append(']')
    a1 = "ADD_SUITE = ['_SGV_GMAX', 'longline']\n"
    a2 = "if hook:\n    R, joined = check('hook', hook, HOOK_SITES, [], ADD_HOOK)\n"
    a3 = "if suite: check('test', suite, SUITE_SITES, SUITE_TITLES, ADD_SUITE)\n"
    assert src.count(a1) == 1 and src.count(a2) == 1 and src.count(a3) == 1
    src = src.replace(a1, a1 + '\n'.join(block(CS_COMMENT) + lit) + '\n', 1)
    src = src.replace(a2, '\n'.join(block(CS_FUNC)) + '\n' + a2, 1)
    src = src.replace(a3, a3 + "if suite:\n    RS = runs(suite); check_suite_text(RS, '\\n'.join(t for t, _ in RS))\n", 1)
    open(cs, 'w', encoding='utf-8').write(src)
    print('commentsync patched')

ANCHORS = ['beyond a limit the command is BLOCKED', '_SGV_SMAX 8192 = one substituted copy', 'the WHOLE judged string, not its growth',
           'which is how a 4096-character list is refused', 'Red when (21ag): the 36 KB dense copy passes',
           'Red when (21aj): such a segment is skipped or counted instead of refused', 'Red when (21al): the braced 8193-character whole copy passes',
           'Red when (21ao): the 8193-character whole copy passes', 'the copy limit holds for the braced form ${NAME} too',
           'whole-command mode (the command degrades because of a `(`) obeys the same copy limit', 'just before SC-13']
OLD_TITLES = ['copy limit exceeded is refused — 8193 characters: the copy is not judged, the command is blocked as too large (no padding passes)',
              'is over the copy limit and refused as too large', 'a segment over the copy limit ends the pass — with one, seven or eight of them in front of the reader the command is refused as too large and the reader is never judged',
              'the copy limit holds for the braced form too — a substituted whole command of exactly 8192 characters is judged and blocked, 8193 is refused as too large',
              'whole-command mode obeys the copy limit — a whole copy of exactly 8192 characters is judged and blocked, 8193 is refused as too large']

def verify(path):
    raw = open(path, encoding='utf-8').read(); joined = '\n'.join(t for t, _ in runs(path))
    for a in ANCHORS: print(f'anchor raw {raw.count(a)} comments {joined.count(a)}  {a[:70]}')
    for t in OLD_TITLES: print(f'old title raw {raw.count(t)}  {t[:70]}')
    for w in ['_SGV_GMAX', 'longline']: print(f'ADD {w}: comments {joined.count(w)}')
    print('sg_w10_cases calls:', len(re.findall(r'^\s*sg_w10_cases\s*$', raw, re.M)), '| wpa_rx6 branches:', raw.count('if [[ $wpa_rx6 == yes ]]; then'))

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'suite': patch_suite(sys.argv[2])
    elif cmd == 'cs': patch_cs(*sys.argv[2:5])
    elif cmd == 'verify': verify(sys.argv[2])

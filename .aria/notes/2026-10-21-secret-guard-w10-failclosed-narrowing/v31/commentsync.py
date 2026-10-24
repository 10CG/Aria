#!/usr/bin/env python3
"""commentsync.py [--hook-only | --suite-only] <hook> [<suite>] <baseline|proto|target> : the What 7 closed list of comment sites, sentence level (v3.2:
post_planning R2 PP2-M, TASK-002 (e)). Comment text is read the way a reader sees it: every run of consecutive comment lines is stripped of its '#' prefix,
whitespace is collapsed, and the run is joined into one string, so a phrase the source wraps across two lines is still found once.
Hook -- sites 1-8 of What 7 and the four places of the What 7 supplement (in sites 1 and 2, and two sites of their own: _sg_vx_replace, the relaxed-rerun
block). Per site: every sentence of the old text that the rewrite removed (the baseline's, and the v3.1 prototype's where the supplement rewrote it) must
occur 0 times anywhere in the comments; every sentence of the new text must occur inside the site's own run, found by its locator (the run right before a
code line, or the run holding a phrase). The lists were derived mechanically -- sentence units split after '.' and ';' -- from the baseline (aria
59e333c), the prototype (mkv31.py, sha256 9f61db0e7b8b) and the spec target (that prototype with the four comment rewrites of the What 7 supplement, taken
from proposal.md): the new text is the proposal's, not the implementation's. So a phrase changed inside an anchor, or a block deleted whole, is RED -- the
new sentences are missing (R2 PP2-M: both were GREEN under the block-hash check). The anchors, run hashes and ADD words of v3.1 are kept as further checks.
  baseline: the old sentences of the baseline are in their runs and the new ones are not, so the check can fail; every anchor occurs as listed; every run
            has its listed hash; no ADD word.
  proto:    the prototype holds the What 7 rewrite but not the supplement: its own old sentences are in their runs, the supplement's new ones are not;
            no anchor, no listed run hash, every ADD word (the target rules of v3.1).
  target:   no old sentence anywhere, every new sentence in its site's run, no anchor, no listed run hash, every ADD word.
Suite -- sites 9-22: the anchors, run hashes and case titles of the baseline that become untrue (0 in the target), with two adjacent comments that become
untrue too (R2 KM2-14: 21al's head, 21ao's head), and the ADD words. The new suite text is written when the suite is ported (TASK-002, suite part); the
sentences each suite site must then hold are bound there. Whether the rewritten text is accurate is reviewed (TASK-005)."""
import re, sys, hashlib
a = sys.argv[1:]
only = a.pop(0) if a and a[0] in ('--hook-only', '--suite-only') else None
if only == '--hook-only':
    hook, mode = a; suite = None
elif only == '--suite-only':
    suite, mode = a; hook = None
else:
    hook, suite, mode = a
assert mode in ('baseline', 'proto', 'target'), mode
if mode == 'proto' and suite: sys.exit('proto mode checks the hook only (the suite has no prototype)')
def runs(path):   # [(run text, the line right after the run)]
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
sha = lambda s: hashlib.sha256(s.encode('utf-8')).hexdigest()[:16]
# (site, baseline sha256 of the whole run, [(anchor phrase, baseline count)])
HOOK_SITES = [
 ('1 hook :87-95 header W10 gap', 'deb0ac78daffb395', [('beyond a SIZE limit the whole command is BLOCKED as too large to scan', 1), ('never passed', 2)]),
 ('2 hook :577-590 LENGTH BUDGET', 'ccc5d4d623e6707e', [('Beyond ANY of them the whole command is BLOCKED', 1), ('blocking is as cheap as passing was', 1),
                                           ('The limit counts the whole judged string, not its growth', 1)]),
 ('3 hook :597-606 time budget', '4f80e337cf4f7bb9', [('the _SGV_* size budget are unchanged', 1)]),
 ('4 hook :674-676 _sg_vx_apply', '3f15b92e57d303ec', [('2 = the copy would be longer than _SGV_SMAX', 1)]),
 ('5 hook :701-703 _sg_vx_pass', '12bfb333904a113c', [('ends the pass at once with an oversize BLOCK', 1)]),
 ('6 hook :826-828 _sg_emit_blocked', 'e3149a7b70a73438', [('_sg_emit_blocked PAT SEG MODE [oversize]', 1)]),
 ('7 hook :1492-1496 _sg_judge_one', 'abf172890d25f686', [('string to judge, $2 = mode (whole|segment). Returns', 1)]),
 ('8 hook :1531-1536 _sg_per_segment_eval', '02cc1e169164ae2c', [('2. only if it allowed, the W10 variable pass (_sg_vx_pass);', 1),
                                                    ('Length budget: an overrun inside _sg_vx_pass blocks there', 1)]),
]
HOOK_TEXT = [  # site, locator, untrue sentences (b = in the baseline run, p = in the prototype run), new sentences (p = the prototype has it, s = What 7 supplement)
 ('1 header: shell variable indirection', ('has', 'Shell variable indirection'),
  [('b', 'cat "$f"`) is covered only in part: literal assignments are expanded in a second pass (at most 16 assignments and 8 replacements per variable;'),
   ('b', 'The SIZE of the expansion is bounded as well -- a value up to 4096 characters, a substituted segment up to 8192 characters and 65536 characters of substituted text per command -- and beyond a SIZE limit the whole command is BLOCKED as too large to scan ("split it", fail-closed, owner ruling 2026-10-14), never passed.'),
   ('p', 'cat "$f"`) is covered only in part: literal assignments are expanded in a second pass (at most 16 assignments and 8 replacements per variable in the baseline pass;'),
   ('p', 'where it is (a Linux build of bash 5.0-5.3, no project extension, time left), the pass is re-run under a hard deadline with no count bound, the growth over the input as the limit and the copy judged in full, and growth over 8192 characters, the deadline or any failure of the rerun still blocks.')],
  [('s', 'cat "$f"`) is covered only in part: literal assignments are expanded in a second pass (at most 16 assignments, 8 for lists and 8 replacements per variable in the baseline pass;'),
   ('p', 'The SIZE of the expansion is bounded too: a value over 4096 characters, or more than 65536 characters of substituted text per command, blocks the command (fail-closed, owner ruling 2026-10-14).'),
   ('p', 'A substituted copy over 8192 characters is blocked for its size only where the relaxed rerun of 10CG/aria-plugin#217 is not in effect;'),
   ('s', 'where it is (an x86_64 GNU/Linux build of bash 5.0-5.3 outside WSL, no project extension, time left), the pass is re-run under a hard deadline with no count bound, the growth over the input as the limit and the copy judged in full, and growth over 8192 characters, the deadline or any failure of the rerun still blocks.'),
   ('s', 'The pass substitutes text;'),
   ('s', "it does not run the shell: a variable assigned twice is replaced by its FIRST value (bash reads the last), and in segment mode a value holding shell syntax (`G='| jq keys'`) becomes syntax in the copy, so a read can earn a filter credit that bash never applies."),
   ('s', 'Both pass, in small commands since the baseline and, with the rerun, in big ones (declared under owner ruling A, 2026-10-23).')]),
 ('2 W10 head + LENGTH BUDGET', ('next', '_SGV_N=(); _SGV_V=()'),
  [('bp', 'at most 16 assignments and 8 replacements per variable);'),
   ('b', 'fail-CLOSED, owner ruling 2026-10-14): without it the judged string is the segment plus references x value length, and one level of chaining multiplies a value by 8, so a 5 KB command overran the 5 s hook timeout (and a timeout lets the command through).'),
   ('b', 'Beyond ANY of them the whole command is BLOCKED with a text of its own ("command too large to scan for secrets ...'),
   ('b', 'split it": _sg_emit_blocked with the 4th word oversize, status 2) and never passed: a copy that is not judged is a way past the guard, and padding a value or a chain would be the recipe.'),
   ('b', 'The oversize string is never built, expanded further, judged or scanned: the pass stops at the first overrun and nothing behind it is touched, so an overrun costs no more than the budgeted work in front of it (blocking is as cheap as passing was;'),
   ('b', 'the 5 s timeout and its fail-open, 10CG/aria-plugin#216, are not touched).'),
   ('b', '(The COUNTS above -- 16 assignments, 8 replacements, 8 for statements -- are another bound and still pass beyond the limit, SC-21 21y.) (1) _SGV_VMAX: a value longer than that (as collected, or after chaining) blocks the command whether or not the variable is mentioned: _sg_vx_collect stops at it and returns 2;'),
   ('b', '(2) _SGV_SMAX: a substituted copy (a segment, or the whole command) that would become longer blocks the command (status 2 of _sg_vx_apply;'),
   ('b', "the W9 extension's look at the substituted whole command, after the pass, blocks on it only when an extension is in effect -- without one nothing is left unjudged)."),
   ('b', '8192 because a BLOCK verdict costs the square of the copy length (_sg_compute_credit on one long line: about 0.9 s at 8 KB, 3 s at 16 KB, 13 s at 32 KB) and a verdict that arrives after the timeout is lost.'),
   ('b', 'The limit counts the whole judged string, not its growth: a segment (in whole-command mode: the command) over 8192 characters that mentions a collected variable is blocked however small the value is.'),
   ('b', '_sg_vx_collect, _sg_vx_apply and _SG_SUB are names of the contract, like _sg_vx_pass: the budget probes of the suite use them.')],
  [('s', 'at most 16 assignments, 8 for lists and 8 replacements per variable in the baseline pass, none in the relaxed rerun of 10CG/aria-plugin#217);'),
   ('p', 'fail-CLOSED, owner ruling 2026-10-14;'),
   ('p', 'narrowed by 10CG/aria-plugin#217): without it the judged string is the segment plus references x value length, and one level of chaining multiplies a value by 8, so a 5 KB command overran the 5 s hook timeout (and a timeout lets the command through).'),
   ('p', 'Both block with a text of their own ("command too large to scan for secrets ...'),
   ('p', 'split it": _sg_emit_blocked with the 4th word oversize, status 2), and the oversize string is never built, expanded further, judged or scanned.'),
   ('p', '(2) _SGV_SMAX: a substituted copy (a segment, or the whole command) that would become longer than 8192 characters ends the baseline pass at that copy (status 2 of _sg_vx_apply), because a BLOCK verdict costs the square of the copy length (_sg_compute_credit on one long line: about 0.9 s at 8 KB, 3 s at 16 KB, 13 s at 32 KB) and a verdict that arrives after the 5 s timeout is lost.'),
   ('p', 'What follows depends on _sg_relax_ok: where the relaxation is in effect, _sg_vx_pass returns status 4 and _sg_per_segment_eval re-runs the pass in a background job under a hard deadline (_sg_relax_run);'),
   ('p', 'there the copy limit is the growth over the input (_SGV_GMAX), and a copy over 8192 characters is judged in full by _sg_vx_big_judge (a line longer than _SGV_LMAX is matched against the rows only: nocredit, the longline text).'),
   ('p', "Elsewhere, and whenever the rerun does not finish in time, the command is blocked with the size text, byte for byte as before (the W9 extension's look at the substituted whole command, after the pass, blocks on such a copy only when an extension is in effect)."),
   ('p', '(The COUNTS above -- 16 assignments, 8 replacements, 8 for statements -- bound the baseline pass and still pass beyond the limit, SC-21 21y;'),
   ('p', 'the relaxed rerun has no count bound, the deadline caps its cost.)')]),
 ('3 time budget', ('next', '_SG_T0=$SECONDS'),
  [('b', 'the `# guard:ack` escape and the _SGV_* size budget are unchanged;')],
  [('p', 'the `# guard:ack` escape is unchanged;'),
   ('p', 'the relaxed rerun of 10CG/aria-plugin#217 has a hard deadline of its own (_SG_P0 + min(budget, 3) s, see _sg_relax_run) and its checkpoints fall back to the size block, never to the time text;')]),
 ('4 _sg_vx_apply', ('next', '_sg_vx_apply() {'),
  [('b', 'Status 0 = a copy was built, 1 = nothing to substitute, 2 = the copy would be longer than _SGV_SMAX (not built, _SG_SUB stays S;'),
   ('b', 'the caller blocks the command).'),
   ('b', 'the remainder keeps the character that ended the match, so $f$f works), at most 8 times.')],
  [('p', 'Status 0 = a copy was built, 1 = nothing to substitute, 2 = the copy would be over the limit (not built, _SG_SUB stays S;'),
   ('p', 'the caller decides): the limit is _SGV_SMAX in the baseline pass and the input length + _SGV_GMAX in the relaxed rerun (_SG_RELAXED).'),
   ('p', 'the remainder keeps the character that ended the match, so $f$f works), at most 8 times in the baseline pass and with no count bound in the relaxed rerun.')]),
 ('5 _sg_vx_pass', ('next', '_sg_vx_pass() {'),
  [('b', 'An overrun of the length budget (a value, a copy, the total) ends the pass at once with an oversize BLOCK (the size text of _sg_emit_blocked, status 2): nothing behind the overrun is built or judged.')],
  [('p', 'A value or total overrun stops the pass with an oversize BLOCK (status 2).'),
   ('p', 'A copy over _SGV_SMAX ends the baseline pass too: with status 4 when the relaxation is in effect (_sg_relax_ok;'),
   ('p', 'the baseline block text is kept in _SG_OV_PAT / _SG_OV_MODE for the fallback), else with the oversize BLOCK.'),
   ('p', 'Inside the relaxed rerun (_SG_RELAXED) a growth overrun blocks with the growth text, a copy over _SGV_SMAX goes to _sg_vx_big_judge, and a time checkpoint returns 3 (no time text: the caller falls back to the baseline block).'),
   ('p', 'Nothing behind an overrun is built or judged.')]),
 ('6 _sg_emit_blocked', ('next', '_sg_emit_blocked() {'),
  [('b', '_sg_emit_blocked PAT SEG MODE [oversize] : the (unchanged) BLOCKED text, shared by every block path.'),
   ('b', 'The size text echoes only the first 200 characters of the command (the command is by definition a large one).')],
  [('p', '_sg_emit_blocked PAT SEG MODE [oversize|timeout|longline] : the BLOCKED text, shared by every block path.'),
   ('p', 'With `longline` (10CG/aria-plugin#217) it prints the text for a big copy that matched a row on a line longer than _SGV_LMAX, where credit is not evaluated;'),
   ('p', 'PAT is the row.'),
   ('p', 'The size, time and longline texts echo only the first 200 characters of the command (the command is by definition a large one).')]),
 ('7 _sg_judge_one', ('next', '_sg_judge_one() {'),
  [('b', '$1 = string to judge, $2 = mode (whole|segment).'),
   ('b', 'Returns 0 = allow, 2 = blocked (BLOCKED message already written to stderr;')],
  [('p', '$1 = string to judge, $2 = mode (whole|segment), $3 = nocredit or empty: with nocredit (10CG/aria-plugin#217: a big copy with a line longer than _SGV_LMAX) a matched row blocks at once with the longline text and credit is not evaluated;'),
   ('p', 'the W12 neutralisation still runs first.'),
   ('p', 'Return 0 = allow, 2 = blocked (BLOCKED message already written to stderr;')]),
 ('8 _sg_per_segment_eval', ('next', '_sg_per_segment_eval() {'),
  [('b', 'only if it allowed, the W10 variable pass (_sg_vx_pass);'),
   ('b', 'Length budget: an overrun inside _sg_vx_pass blocks there;')],
  [('p', 'only if it allowed, the W10 variable pass (_sg_vx_pass), and when that pass returns status 4 (a copy over _SGV_SMAX with the relaxation in effect), the relaxed rerun under the hard deadline (_sg_relax_run, 10CG/aria-plugin#217): its allow or block is final -- the relaxation is in effect only when no extension is, so stage 3 would add nothing -- and any failure of the rerun falls back to the baseline size block;'),
   ('p', 'Length budget: a value or total overrun inside _sg_vx_pass blocks there;')]),
 ('9 _sg_vx_replace (supplement 2)', ('next', '_sg_vx_replace() {'),
  [('bp', '_sg_vx_replace S PAT REP [MAX] : literal replace-all of PAT in S, at most 8 replacements -> _SG_RP;')],
  [('s', '_sg_vx_replace S PAT REP [MAX] : literal replace-all of PAT in S, at most 8 replacements in the baseline pass (no bound in the relaxed rerun) -> _SG_RP;')]),
 ('10 relaxed rerun block (supplement 4)', ('next', '_sg_vx_big_judge() {'),
  [('p', 'In effect only on a Linux build of bash 5.0-5.3 on GNU/Linux (the versions and the platform measured), with no project extension in effect (with one, the extension blocks a copy over _SGV_SMAX by its own absolute limit anyway), and with time left before the deadline.')],
  [('p', '10CG/aria-plugin#217 relaxed rerun.'),
   ('p', 'When the relaxation is in effect (_sg_relax_ok), a copy over _SGV_SMAX is not blocked for its size alone: _sg_vx_pass returns 4 instead and keeps the baseline block text in _SG_OV_PAT / _SG_OV_MODE, and _sg_per_segment_eval re-runs the W10 pass with the relaxed rules (_SG_RELAXED: the copy limit is the growth over the input, _SGV_GMAX;'),
   ('p', 'a copy over _SGV_SMAX is judged in full, _sg_vx_big_judge;'),
   ('p', 'the counts -- 16 assignments, 8 for statements, 8 replacements per variable -- are not bounded, so every reference is expanded) in a background job under a HARD deadline: _SG_P0 (hook start) + min(_SG_TIME_BUDGET, 3) s.'),
   ('p', 'The job leads its own process group (set -m);'),
   ('p', 'its timer runs inside the group and is started before the first expensive step;'),
   ('p', 'the deadline kills the whole group, and so does _sg_relax_run once the job has ended, so nothing of the job outlives it or holds the pipe.'),
   ('p', "The verdict is the job's exit status, never parsed from text: 77 allows, 2 blocks with the job's own text;"),
   ('p', 'any other outcome -- the deadline, a time checkpoint, the self-check, an internal error, a bare 0 -- falls back to the baseline block, byte for byte.'),
   ('s', 'In effect only on an x86_64 GNU/Linux build of bash 5.0-5.3 outside WSL (the versions, architecture and platform measured), with no project extension in effect (with one, the extension blocks a copy over _SGV_SMAX by its own absolute limit anyway), and with time left before the deadline.')]),
]
SUITE_SITES = [
 ('9 test :2510-2518 W10 block head', '4a7c44caa0c7b992', [('beyond a limit the command is BLOCKED', 1), ('_SGV_SMAX 8192 = one substituted copy', 1)]),
 ('10 test :2544-2549 21aa/21ab', 'f3fa3abab18f053b', [('the WHOLE judged string, not its growth', 1)]),
 ('11 test :2556-2562 21ac/21ad', '3ecdb01f064087db', [('which is how a 4096-character list is refused', 1)]),
 ('12 test :2578-2585 21af/21ag', '1bd18760d748990e', [('Red when (21ag): the 36 KB dense copy passes', 1)]),
 ('13 test :2597-2599 21aj', 'dbca04b5e10c90bc', [('Red when (21aj): such a segment is skipped or counted instead of refused', 1)]),
 ('14 test :2628-2632 21al', '32ec743f4667c650', [('Red when (21al): the braced 8193-character whole copy passes', 1)]),
 ('15 test :2679-2681 21ao', '1c6bab0505df9784', [('Red when (21ao): the 8193-character whole copy passes', 1)]),
 ('21 test :2628-2630 21al head', '7e3c405bfc08e835', [('the copy limit holds for the braced form ${NAME} too', 1)]),
 ('22 test :2679 21ao head', '65da1f91daeab547', [('whole-command mode (the command degrades because of a `(`) obeys the same copy limit', 1)]),
]
SUITE_TITLES = [  # the full baseline titles of the cases whose title becomes untrue (21ac keeps its title: its read is still blocked)
 ('16 test :2552 21ab title', 'W10 SC-21ab bf: copy limit exceeded is refused — 8193 characters: the copy is not judged, the command is blocked as too large (no padding passes)', 1),
 ('17 test :2586 21ag title', 'W10 SC-21ag bf: the dense shape of the review (15 assignments of 300 B, 8 references each: a 36 KB copy; 16 x 300 B x 8 took 5.4 s) is over the copy limit and refused as too large', 1),
 ('18 test :2605 21aj title', 'W10 SC-21aj bf: a segment over the copy limit ends the pass — with one, seven or eight of them in front of the reader the command is refused as too large and the reader is never judged', 1),
 ('19 test :2633 21al title', 'W10 SC-21al bf: the copy limit holds for the braced form too — a substituted whole command of exactly 8192 characters is judged and blocked, 8193 is refused as too large', 1),
 ('20 test :2682 21ao title', 'W10 SC-21ao bf: whole-command mode obeys the copy limit — a whole copy of exactly 8192 characters is judged and blocked, 8193 is refused as too large', 1),
]
ADD_HOOK = ['_SGV_GMAX', '_SGV_LMAX', '_SG_P0', 'hard deadline', 'nocredit', 'longline', '_sg_relax_run', 'status 4']
ADD_SUITE = ['_SGV_GMAX', 'longline']
bad = 0
def say(ok, kind, site, n, text):
    global bad
    bad += not ok
    print(f"{'ok ' if ok else 'RED'} {kind:7s} {site:40s} n={n}  {text[:110]}")
def check(label, path, sites, titles, add):
    R = runs(path); texts = [t for t, _ in R]; joined = '\n'.join(texts); raw = open(path, encoding='utf-8').read(); hashes = {sha(t) for t in texts}
    old_rules = 'baseline' if mode == 'baseline' else 'target'   # proto mode keeps the target rules of v3.1 for the anchors, hashes and ADD words
    for site, h, anchors in sites:
        for ph, n0 in anchors:
            n = joined.count(ph); say((n == n0) if old_rules == 'baseline' else (n == 0), 'anchor', site, n, ph)
        if old_rules == 'baseline':
            got = [sha(t) for t in texts if anchors[0][0] in t]; say(got == [h], 'block', site, len(got), f'sha256 {got} (listed {h})')
        else:
            say(h not in hashes, 'block', site, int(h in hashes), 'rewritten' if h not in hashes else 'the baseline block is still there')
    for site, ph, n0 in titles:
        n = raw.count(ph); say((n == n0) if old_rules == 'baseline' else (n == 0), 'title', site, n, ph)
    for w in add:
        n = joined.count(w); say((n == 0) if old_rules == 'baseline' else (n >= 1), 'add', label, n, w)
    return R, joined
def check_text(R, joined):
    for site, loc, untrue, new in HOOK_TEXT:
        run = site_run(R, loc)
        if mode == 'baseline' and run is None and all('b' not in f for f, _ in untrue):
            print(f"ok  site    {site:40s} n/a: the site is new in the prototype"); continue
        if run is None:
            say(False, 'site', site, 0, f'no comment run found by {loc}')
        for f, u in untrue:
            if mode == 'baseline' and 'b' in f: n = (run or '').count(u); say(n >= 1, 'old', site, n, u)
            elif mode == 'proto' and 'p' in f: n = (run or '').count(u); say(n >= 1, 'old', site, n, u)
            else: n = joined.count(u); say(n == 0, 'old', site, n, u)
        for f, u in new:
            n = (run or '').count(u)
            if mode == 'target' or (mode == 'proto' and f == 'p'): say(n >= 1, 'new', site, n, u)
            else: say(n == 0, 'new', site, n, u)
if hook:
    R, joined = check('hook', hook, HOOK_SITES, [], ADD_HOOK)
    check_text(R, joined)
if suite: check('test', suite, SUITE_SITES, SUITE_TITLES, ADD_SUITE)
print(f"{mode}{' ' + only if only else ''}: {'GREEN' if bad == 0 else 'RED (%d)' % bad}")
sys.exit(1 if bad else 0)

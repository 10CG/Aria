import sys, re, hashlib, difflib
W, V = sys.argv[1], sys.argv[2]
HK = W + '/hooks/secret-guard.sh'; SU = W + '/hooks/tests/secret-guard.test.sh'; HL = W + '/hooks/tests/lib/secret-guard-w10-direct.sh'
SD = V + '/sc-direct.sh'; SC = V + '/sc-cases.sh'; WM = V + '/impl/w14-mutants.py'
rd = lambda p: open(p, encoding='utf-8', newline='').read()
def wr(p, t): open(p, 'w', encoding='utf-8', newline='').write(t)
def rep(t, a, b, what):
    c = t.count(a); assert c == 1, (what, c); return t.replace(a, b)
out = []
# 1. hook: the one comment line of the rerun block head
h = rd(HK)
O796 = "# returns 4 instead and keeps the baseline block text in _SG_OV_PAT / _SG_OV_MODE, and _sg_per_segment_eval re-runs the W10 pass with the relaxed rules\n"
N796 = "# returns 4 instead and keeps the baseline reason and mode in _SG_OV_PAT / _SG_OV_MODE; _sg_per_segment_eval re-runs the W10 pass with the relaxed rules\n"
assert h.split('\n')[795] + '\n' == O796
h2 = rep(h, O796, N796, 'hook796'); a, b = h.split('\n'), h2.split('\n')
assert len(a) == len(b) and sum(x != y for x, y in zip(a, b)) == 1
wr(HK, h2); sha = hashlib.sha256(h2.encode('utf-8')).hexdigest()[:12]
out.append('hook: 1 line changed (796), width %d -> %d, block max 155; sha12 %s' % (len(O796) - 1, len(N796) - 1, sha))
FN_BODY = r'''  local t l d="${2:-/proc/sys/fs/binfmt_misc}"
  t=$(cat -- "${1:-/proc/self/mounts}" 2>/dev/null) || return 0
  awk -v d="$d" '$2 == d && $3 == "binfmt_misc" { m = 1 } END { exit !m }' <<< "$t" || return 1
  l=$'\n'$(ls -A -- "$d" 2>/dev/null); [[ $l == *$'\n'WSLInterop* ]]
}
'''
# 2a. helper and sc-direct.sh: the same new lines (INV-2)
WSL_OLD = "OSR=$(cat /proc/sys/kernel/osrelease 2>/dev/null); WSLM=''; [[ -e /proc/sys/fs/binfmt_misc/WSLInterop ]] && WSLM=wsl\n"
WSL_NEW = ('''wslmark() {   # [MOUNTS [DIR]] : status 0 where the gate must see a WSL mark in the file system -- the rule of the hook's _sg_relax_nowslfs (What 1 supplement 2),
  # written apart from it, never sourced or called (status 0 here is status 1 there): the mount table (default /proc/self/mounts) cannot be read, or a
  # binfmt_misc file system is mounted at DIR (default /proc/sys/fs/binfmt_misc) and holds an entry named WSLInterop*. DIR is listed only when that mount is
  # in the table, so the check never triggers an automount. The two arguments exist to check it against the hook's function; WSLM below calls it with none
''' + FN_BODY + "OSR=$(cat /proc/sys/kernel/osrelease 2>/dev/null); WSLM=''; wslmark && WSLM=wsl\n")
T2C = re.compile(r'^( *)# \(b\) with the anchor 2\.5 s back and budget 3 the judgement inside the job sees at most 0\.5 s left \(a fresh anchor in the gate, the run or the job gives about 3 s\)\n', re.M)
def t2c(m):
    i = m.group(1)
    return (i + "# (b) with the anchor 2.0 s back and budget 3 the judgement inside the job sees 0 < left <= 1.0 s: a fresh anchor in the gate, the run or the job\n"
            + i + "# (a bad implementation) gives about 3 s there, and a slow host only makes the value smaller (it reaches 0 only after 1.0 s from here to the judgement)\n")
pair = {}
for p in (HL, SD):
    t = rd(p); t0 = t
    t = rep(t, WSL_OLD, WSL_NEW, p + ' wsl')
    t, n = T2C.subn(t2c, t); assert n == 1, (p, 't2 comment', n)
    t = rep(t, '''printf "%.6f", e-2.5}\'''', '''printf "%.6f", e-2.0}\'''', p + ' anchor')
    t = rep(t, 'l+0 > 0 && l+0 <= 0.5)}', 'l+0 > 0 && l+0 <= 1.0)}', p + ' bound')
    t = rep(t, 'anchor 2.5 s back, budget 3: the judgement in the job saw _SG_LEFT [$t2a] (want 0 < left <= 0.5;', 'anchor 2.0 s back, budget 3: the judgement in the job saw _SG_LEFT [$t2a] (want 0 < left <= 1.0;', p + ' msg')
    wr(p, t)
    d = [x for x in difflib.unified_diff(t0.split('\n'), t.split('\n'), lineterm='', n=0) if x[:1] in '+-' and x[:3] not in ('+++', '---')]
    pair[p] = d; out.append('%s: -%d +%d lines' % (p.rsplit('/', 1)[1], sum(x[0] == '-' for x in d), sum(x[0] == '+' for x in d)))
out.append('INV-2 helper vs sc-direct.sh changed lines identical: %s' % (pair[HL] == pair[SD]))
# 2b + 4. suite
s = rd(SU); s0 = s
SFN = ('''sg_w10_wslfs() {   # [MOUNTS [DIR]] -> status 0 where the gate must see a WSL mark in the file system (WSLF in sg_w10_cases, wpa_rx6_wslf): the rule of the hook's
  # _sg_relax_nowslfs (What 1 supplement 2), written apart from it, never sourced or called (status 0 here is status 1 there) -- the mount table (default
  # /proc/self/mounts) cannot be read, or a binfmt_misc file system is mounted at DIR (default /proc/sys/fs/binfmt_misc) and holds an entry named WSLInterop*.
  # DIR is listed only when that mount is in the table, so the check never triggers an automount. The two arguments exist to check it against the hook's function
''' + FN_BODY)
s = rep(s, '\nsg_w10_relax_rule() {', '\n' + SFN + 'sg_w10_relax_rule() {', 'suite fn')
s = rep(s, 'WSLF=no; [[ -e /proc/sys/fs/binfmt_misc/WSLInterop ]] && WSLF=yes', 'WSLF=no; sg_w10_wslfs && WSLF=yes', 'suite WSLF')
s = rep(s, '\n[[ -e /proc/sys/fs/binfmt_misc/WSLInterop ]] && wpa_rx6_wslf=yes\n', '\nsg_w10_wslfs && wpa_rx6_wslf=yes\n', 'suite wpa')
LST_O = 'for f in _sg_vx_big_judge _sg_relax_left _sg_relax_ok _sg_relax_platform _sg_relax_noext _sg_relax_job _sg_relax_run; do'
LST_N = 'for f in _sg_vx_big_judge _sg_relax_left _sg_relax_ok _sg_relax_platform _sg_relax_nowslfs _sg_relax_noext _sg_relax_job _sg_relax_run; do'
EXP_O = 'V11-S1-above-gate:_sg_relax_platform\nV11-S1-above-gate:_sg_relax_noext '
EXP_N = 'V11-S1-above-gate:_sg_relax_platform\nV11-S1-above-gate:_sg_relax_nowslfs V11-S1-above-gate:_sg_relax_noext '
s = rep(s, LST_O, LST_N, 'suite list'); s = rep(s, EXP_O, EXP_N, 'suite exp')
s = rep(s, '# Coverage: 980 cases (974 without zsh)', '# Coverage: 981 cases (975 without zsh)', 'suite cov')
s = rep(s, '\n# 149 of those cases are the W10 ', '\n# 150 of those cases are the W10 ', 'suite 149')
wr(SU, s)
# 2c + 4. sc-cases.sh
c = rd(SC)
C_O = '''#            it, no /proc/sys/fs/binfmt_misc/WSLInterop. Every run of the hook clears WSL_DISTRO_NAME and WSL_INTEROP (only the WSL case sets one), and so
#            does sc-direct.sh. On any other bash every e2e outcome must equal the baseline's and the gate must stay closed.
'''
C_N = '''#            it, and no WSL mark in the file system (wslmark below, the rule of What 1 supplement 2 written apart from the hook's _sg_relax_nowslfs: a mount
#            table that cannot be read, or a WSLInterop* entry under a binfmt_misc mounted at /proc/sys/fs/binfmt_misc). Every run of the hook clears
#            WSL_DISTRO_NAME and WSL_INTEROP (only the WSL case sets one), and so does sc-direct.sh. On any other bash every e2e outcome must equal the
#            baseline's and the gate must stay closed.
'''
c = rep(c, C_O, C_N, 'sc-cases head')
CW_O = 'OSR=$(cat /proc/sys/kernel/osrelease 2>/dev/null); WSLF=no; [[ -e /proc/sys/fs/binfmt_misc/WSLInterop ]] && WSLF=yes\n'
CW_N = ('''wslmark() {   # [MOUNTS [DIR]] : status 0 where the gate must see a WSL mark in the file system -- the rule of the hook's _sg_relax_nowslfs (What 1 supplement 2),
  # written apart from it, never sourced or called (status 0 here is status 1 there): the mount table (default /proc/self/mounts) cannot be read, or a
  # binfmt_misc file system is mounted at DIR (default /proc/sys/fs/binfmt_misc) and holds an entry named WSLInterop*. DIR is listed only when that mount is
  # in the table, so the check never triggers an automount. The two arguments exist to check it against the hook's function; WSLF below calls it with none
''' + FN_BODY + 'OSR=$(cat /proc/sys/kernel/osrelease 2>/dev/null); WSLF=no; wslmark && WSLF=yes\n')
c = rep(c, CW_O, CW_N, 'sc-cases wsl')
c = rep(c, LST_O, LST_N, 'sc-cases list'); c = rep(c, EXP_O, EXP_N, 'sc-cases exp')
wr(SC, c)
for p, t0 in ((SU, s0), (SC, None)):
    pass
w = rd(WM); w = rep(w, "'50ce186a28c9'", "'%s'" % sha, 'w14 sha') if "'50ce186a28c9'" in w else rep(w, '"50ce186a28c9"', '"%s"' % sha, 'w14 sha'); wr(WM, w)
mx = {p: max(len(x) for x in rd(p).split('\n') if x.lstrip().startswith('#') and ('wslmark' in x or 'WSL mark' in x or 'binfmt_misc' in x or '2.0 s' in x or 'bad implementation' in x)) for p in (HL, SD, SU, SC)}
out.append('widest new comment line per file: ' + str({k.rsplit('/', 1)[1]: v for k, v in mx.items()}))
print('\n'.join(out))

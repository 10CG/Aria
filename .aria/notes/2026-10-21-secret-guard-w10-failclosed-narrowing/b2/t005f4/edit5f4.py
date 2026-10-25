# edit5f4.py (10CG/aria-plugin#217, TASK-005 fix round part 4): every change of 5f4, from the pre/ copies (replayable)
import os, re, shutil, hashlib, difflib
S = '/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad'
WT = S + '/wt217/aria'; MR = '/home/dev/Aria'
V = MR + '/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31'
O = S + '/r217impl/t005f4'; P2 = S + '/r217impl/spec-probe2'
PROP = MR + '/openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md'
F = dict(hook=WT + '/hooks/secret-guard.sh', helper=WT + '/hooks/tests/lib/secret-guard-w10-direct.sh', suite=WT + '/hooks/tests/secret-guard.test.sh',
         scdirect=V + '/sc-direct.sh', sccases=V + '/sc-cases.sh', w14mut=V + '/impl/w14-mutants.py', mutants=V + '/mutants.py')
os.makedirs(O + '/pre', exist_ok=True); T = {}
for k, pth in F.items():
    pre = O + '/pre/' + k + '-' + os.path.basename(pth)
    if not os.path.exists(pre): shutil.copyfile(pth, pre)
    T[k] = open(pre, encoding='utf-8', newline='').read()
    assert '\r' not in T[k], k + ' has CR'
def once(t, a, b, what):
    n = t.count(a); assert n == 1, (what, n); return t.replace(a, b, 1)
def line(t, prefix, what):
    x = [l for l in t.split('\n') if l.startswith(prefix)]; assert len(x) == 1, (what, len(x)); return x[0]
W1O = 'V15-W1o-regular-file-as-directory'

# ---------------- A. hook: the two code blocks of What 1 supplement 2 (v3.5), taken from the proposal ----------------
p = open(PROP, encoding='utf-8').read(); mk = '做法（v3.4；v3.5 只补了目录判据并改准注释）：'
assert p.count(mk) == 1, 'marker'
blocks = re.findall(r'```bash\n(.*?)```', p[p.index(mk):], re.S)[:2]
L = blocks[0].rstrip('\n').split('\n'); FN = blocks[1]
assert len(L) == 2 and FN.startswith('_sg_relax_nowslfs() {') and FN.endswith('\n}\n'), 'proposal blocks'
print('A0 proposal function == spec-probe2/spec5.sh:', FN == open(P2 + '/spec5.sh', encoding='utf-8').read())
h = T['hook']
assert line(h, '  [[ -n "${WSL_DISTRO_NAME:-}${WSL_INTEROP:-}" ]] && wsl=wsl', 'env') == L[0], 'env line differs from block line 1'
g = line(h, '  _sg_relax_nowslfs || return 1', 'gate line')
assert g.split('   #')[0] == L[1].split('   #')[0] == '  _sg_relax_nowslfs || return 1', 'gate line code part'
h = once(h, g + '\n', L[1] + '\n', 'gate line')
i = h.index('\n_sg_relax_nowslfs() {') + 1; j = h.index('\n}\n', i) + 3; old = h[i:j]
s3 = open(P2 + '/spec3.sh', encoding='utf-8').read()
print('A1 hook v3.4 function == spec3.sh:', old == s3, '| lines', old.count('\n'), '->', FN.count('\n'))
if old != s3:
    k = next(n for n in range(min(len(old), len(s3))) if old[n] != s3[n]); print('   first difference at char', k, ': hook', repr(old[k-30:k+50]), '| spec3', repr(s3[k-30:k+50]))
ch = [n for n, (a, b) in enumerate(zip(old.split('\n'), FN.split('\n'))) if a != b]
print('A2 function lines changed (0-based):', ch)
h = h[:i] + FN + h[j:]
d = [x for x in difflib.unified_diff(T['hook'].split('\n'), h.split('\n'), lineterm='', n=0) if x[:1] in '+-' and x[:3] not in ('+++', '---')]
print('A3 hook: lines', T['hook'].count('\n'), '->', h.count('\n'), '| -%d +%d' % (sum(x[0] == '-' for x in d), sum(x[0] == '+' for x in d)))
T['hook'] = h; NEW12 = hashlib.sha256(h.encode('utf-8')).hexdigest()[:12]; print('A4 new hook sha256 prefix', NEW12)

# ---------------- B. helper and v31/sc-direct.sh: the same code (INV-2) ----------------
W1L_TAIL = ('. uid 0 lists any directory, so there a look name by name cannot be told from a glob: not applicable there (review R3 m-4)')
W1L_SKIP = ('    if [[ "$(id -ru)" == 0 ]]; then out SKIP V15-W1l-unlistable-directory-with-wslinterop-late "[platform] uid 0 lists any directory, one of '
            'mode 0311 too, so here the case cannot tell a look name by name from a glob"')
W1O_BLOCK = (
    '  if sel ' + W1O + '; then   # a DIR that is not a directory -- an empty regular file of mode 0755 that the table lists as a binfmt_misc mount point: the\n'
    '    # entries cannot be seen, so they may exist (What 1 supplement 2 v3.5; review R3 m-3: -x alone is true for such a file, and the look then finds nothing). Any uid\n'
    r'''    w1o="$X/w1-xfile"; : > "$w1o"; chmod 0755 "$w1o"; printf 'binfmt_misc %s binfmt_misc rw,nosuid,nodev,noexec,relatime 0 0\nproc /proc proc rw,nosuid,nodev,noexec,relatime 0 0\n' "$w1o" > "$X/w1-xfile-mounts"''' '\n'
    '    w1x ' + W1O + ' "$X/w1-xfile-mounts" "$w1o" 1 "binfmt_misc listed at DIR, DIR an empty regular file of mode 0755 (not a directory)"\n'
    '  fi\n')
W1N_CMT = ('    # time, at most 0.5 s. SKIP [platform] where unshare -rm is not available, where no tmpfs can be mounted, and where the stacking stops after 1 to 999\n'
           '    # mounts (a low fs.mount-max, say; review R3): the table the case needs cannot be made there\n')
W1N_ELIF = ('      elif [[ $w1nn =~ ^[0-9]+$ ]] && (( w1nn < 1000 )); then out SKIP V15-W1n-mount-table-read-in-one-pass "[platform] the stacking stopped after $w1nn '
            'of 1000 tmpfs mounts (a low fs.mount-max, say), so the table the case needs cannot be made here"\n')
def direct(t, nm):
    a = t.index('  if sel V15-W1l-unlistable-directory-with-wslinterop-late; then   #'); b = t.index('\n  fi\n', a) + 6
    ls = t[a:b].split('\n'); assert len(ls) == 5 and ls[3] == '  fi' and ls[4] == '', (nm, 'W1l block', len(ls))
    assert ls[0].endswith('each name is still seen, where a glob sees none (review R2 m-1)'), (nm, 'W1l comment')
    new = '\n'.join([ls[0] + W1L_TAIL, W1L_SKIP, '    else', '  ' + ls[1], '  ' + ls[2], '    fi', '  fi', ''])
    t = t[:a] + new + W1O_BLOCK + t[b:]
    t = once(t, 'V15-W1l-unlistable-directory-with-wslinterop-late; fi\n', 'V15-W1l-unlistable-directory-with-wslinterop-late ' + W1O + '; fi\n', nm + ' miss list')
    c = line(t, '    # regenerates the table at every seek back: 2.2 s there). Hard: the 1000 mounts made', nm + ' W1n comment')
    assert c.endswith('soft (INV-7): the wall'), (nm, 'W1n comment end')
    t = once(t, c + '\n', c + '\n' + W1N_CMT, nm + ' W1n comment')
    s = line(t, '      if [[ "${w1nn:-0}" == 0 ]]; then out SKIP V15-W1n-mount-table-read-in-one-pass ', nm + ' W1n skip')
    t = once(t, s + '\n      else\n', s + '\n' + W1N_ELIF + '      else\n', nm + ' W1n elif')
    return t
for k in ('helper', 'scdirect'):
    n0 = T[k].count('\n'); T[k] = direct(T[k], k); print('B1', k, 'lines', n0, '->', T[k].count('\n'))
def dd(x, y): return [l for l in difflib.unified_diff(x.split('\n'), y.split('\n'), lineterm='', n=0) if l[:1] in '+-' and l[:3] not in ('+++', '---')]
P0 = {k: open(O + '/pre/' + k + '-' + os.path.basename(F[k]), encoding='utf-8', newline='').read() for k in ('helper', 'scdirect')}
print('B2 helper vs sc-direct: the differing lines are the same before and after the edit (INV-2):', dd(P0['helper'], P0['scdirect']) == dd(T['helper'], T['scdirect']), '| differing lines', len(dd(T['helper'], T['scdirect'])))

# ---------------- B5. lists and the suite's count ----------------
T['suite'] = once(T['suite'], 'V15-W1l-unlistable-directory-with-wslinterop-late V15-W1m-mount-table-read-only-after-platform-and-time',
                  'V15-W1l-unlistable-directory-with-wslinterop-late V15-W1m-mount-table-read-only-after-platform-and-time ' + W1O, 'SGW_EXP_DIRECT')
T['suite'] = once(T['suite'], '# Coverage: 990 cases (984 without zsh)', '# Coverage: 991 cases (985 without zsh)', 'suite count')
T['sccases'] = once(T['sccases'], 'V15-W1m-mount-table-read-only-after-platform-and-time"', 'V15-W1m-mount-table-read-only-after-platform-and-time ' + W1O + '"', 'sc-cases list')

# ---------------- C. v31 tools ----------------
for a in ('  _sg_relax_left || return 1\n  _sg_relax_nowslfs',):
    print('C1 mutants.py / w14 Q-30 anchor present in the new hook:', h.count(a) == 1)
T['w14mut'] = once(T['w14mut'], 'IMPL_SHA12 = "16996eb7db21"', 'IMPL_SHA12 = "%s"' % NEW12, 'IMPL_SHA12')
for k, pth in F.items():
    if k == 'mutants': continue
    open(pth, 'w', encoding='utf-8', newline='').write(T[k])
print('written', ' '.join(k for k in F if k != 'mutants'))

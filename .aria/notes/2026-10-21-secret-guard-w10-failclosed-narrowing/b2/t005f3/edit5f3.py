#!/usr/bin/env python3
# edit5f3.py: TASK-005 fix round part 3 (5f3), 10CG/aria-plugin#217. Always edits from the pre-edit copies in t005f3/pre/ (idempotent).
import re, sys, os, shutil, hashlib
S = '/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad'
WT = S + '/wt217/aria'; MR = '/home/dev/Aria'
V = MR + '/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31'
O = S + '/r217impl/t005f3'
PROP = MR + '/openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md'
F = dict(hook=WT + '/hooks/secret-guard.sh', helper=WT + '/hooks/tests/lib/secret-guard-w10-direct.sh',
         suite=WT + '/hooks/tests/secret-guard.test.sh', scdirect=V + '/sc-direct.sh', sccases=V + '/sc-cases.sh',
         mutants=V + '/mutants.py', w14m=V + '/impl/w14-mutants.py')
os.makedirs(O + '/pre', exist_ok=True)
T = {}
for k, p in F.items():
    pre = O + '/pre/' + k + '-' + os.path.basename(p)
    if not os.path.exists(pre): shutil.copyfile(p, pre)
    T[k] = open(pre, encoding='utf-8', newline='').read()
    assert '\r' not in T[k], k

def once(t, a, b, what):
    n = t.count(a)
    if n != 1: sys.exit('%s: anchor occurs %d times' % (what, n))
    return t.replace(a, b, 1)
def repl_fn(t, start, new, what):   # replace the function that starts with START (at a line start) up to its first '\n}\n'
    assert t.count('\n' + start) == 1, what
    i = t.index('\n' + start) + 1; j = t.index('\n}\n', i) + 3
    return t[:i] + new + t[j:]
def wrap(prefix, text, width):
    out, cur = [], prefix
    for w in text.split(' '):
        if cur == prefix: cur += w
        elif len(cur) + 1 + len(w) <= width: cur += ' ' + w
        else: out.append(cur); cur = prefix + w
    out.append(cur); return '\n'.join(out) + '\n'
def sub(tpl, d):
    for k, v in d.items(): tpl = tpl.replace('@' + k + '@', v)
    assert not re.search(r'@[A-Za-z0-9]+@', tpl), re.findall(r'@[A-Za-z0-9]+@', tpl)
    return tpl

ID = dict(a='V15-W1a-autofs-mount-point-not-looked-at', b='V15-W1b-binfmt-misc-with-wslinterop-late', c='V15-W1c-binfmt-misc-without-entry',
          d='V15-W1d-unreadable-mount-table', e='V15-W1e-gate-closed-by-wsl-file-system',
          f='V15-W1f-empty-mount-table', g='V15-W1g-autofs-on-top-of-binfmt-misc-not-looked-at', h='V15-W1h-directory-as-mount-table',
          i='V15-W1i-noglob-binfmt-misc-with-wslinterop-late', j='V15-W1j-failglob-binfmt-misc-without-entry', k='V15-W1k-unsearchable-directory',
          l='V15-W1l-unlistable-directory-with-wslinterop-late', m='V15-W1m-mount-table-read-only-after-platform-and-time',
          n='V15-W1n-mount-table-read-in-one-pass')
BOTH_NEW = ' '.join(ID[x] for x in 'fghijklm')
BUD = 'SECRET' + '_GUARD_TIME_BUDGET_S'

# ---------------- A. hook ----------------
p = open(PROP, encoding='utf-8').read()
blocks = re.findall(r'```bash\n(.*?)```', p[p.index('v3.4 的做法：'):], re.S)
L = blocks[0].rstrip('\n').split('\n'); FN = blocks[1]
assert len(L) == 2 and FN.startswith('_sg_relax_nowslfs() {') and FN.endswith('\n}\n'), 'proposal blocks'
h = T['hook']
env_old = [x for x in h.split('\n') if x.startswith('  [[ -n "${WSL_DISTRO_NAME:-}${WSL_INTEROP:-}" ]] && wsl=wsl')]
assert len(env_old) == 1
print('A1 WSL line already identical to the v3.4 first line:', env_old[0] == L[0])
h = once(h, env_old[0] + '\n', L[0] + '\n', 'env line')
h = once(h, '  [[ -n "$wsl" ]] || _sg_relax_nowslfs || wsl=wsl   # a WSLInterop* entry under a mounted binfmt_misc, or a mount table that cannot be read\n', '', 'v3.3 line')
h = once(h, '  _sg_relax_left || return 1\n  [[ "$( _sg_relax_noext 2>/dev/null )" == none ]]\n',
         '  _sg_relax_left || return 1\n' + L[1] + '\n  [[ "$( _sg_relax_noext 2>/dev/null )" == none ]]\n', 'second line')
i = h.index('\n_sg_relax_nowslfs() {') + 1; j = h.index('\n_sg_relax_noext() {', i) + 1
h = h[:i] + FN + h[j:]
lines = h.split('\n')
s = next(k for k, x in enumerate(lines) if x.startswith('#   - Shell variable indirection'))
e = next(k for k in range(s + 1, len(lines)) if not lines[k].startswith('#     '))
width = max(len(x) for x in lines[s:e])
D3 = ("The one exception (What 4): a fatal error of bash itself inside the rerun that makes it exit with status 2 and write its error message is "
      "passed on as the block text -- the command is still blocked, but with bash's message instead of the size block's text.")
h = once(h, '#     block. The pass substitutes text; it does not run the shell: a\n',
         wrap('#     ', 'block. ' + D3 + ' The pass substitutes text; it does not run the shell: a', width), 'header D-3')
print('A3 header bullet lines %d-%d, width %d' % (s + 1, e, width))
T['hook'] = h
SHA12 = hashlib.sha256(h.encode('utf-8')).hexdigest()[:12]
print('new hook sha256 prefix', SHA12)

# ---------------- B. test side ----------------
WM_BODY = r'''  local t y d="${2:-/proc/sys/fs/binfmt_misc}"
  t=$(cat -- "${1:-/proc/self/mounts}" 2>/dev/null && echo .) || return 0
  [[ "$t" != . ]] || return 0
  y=$(printf '%s\n' "${t%.}" | awk -v d="$d" '$2 == d { print $3 }' | tail -n 1)
  [[ "$y" == binfmt_misc ]] || return 1
  ( cd -- "$d" ) >/dev/null 2>&1 || return 0
  [ -e "$d/WSLInterop" ] || [ -e "$d/WSLInterop-late" ]
}
'''
def wm_head(v): return (
    "wslmark() {   # [MOUNTS [DIR]] : status 0 where the gate must see a WSL mark in the file system -- the rule of the hook's _sg_relax_nowslfs (What 1 supplement 2,\n"
    "  # v3.4), written apart from it, never sourced or called (status 0 here is status 1 there): the mount table (default /proc/self/mounts) cannot be read or\n"
    "  # reads empty; or the topmost mount at DIR (default /proc/sys/fs/binfmt_misc; the table's last line for it) is a binfmt_misc file system and DIR cannot\n"
    "  # be searched (cd fails) or holds WSLInterop or WSLInterop-late (each name tested on its own: no glob, no listing). DIR is looked at only under a topmost\n"
    "  # binfmt_misc, so the check never triggers an automount. The two arguments exist to check it against the hook's function; %s below calls it with none\n" % v)
SUITE_HEAD = (
    "sg_w10_wslfs() {   # [MOUNTS [DIR]] -> status 0 where the gate must see a WSL mark in the file system (WSLF in sg_w10_cases, wpa_rx6_wslf): the rule of the hook's\n"
    "  # _sg_relax_nowslfs (What 1 supplement 2, v3.4), written apart from it, never sourced or called (status 0 here is status 1 there) -- the mount table (default\n"
    "  # /proc/self/mounts) cannot be read or reads empty; or the topmost mount at DIR (default /proc/sys/fs/binfmt_misc; the table's last line for it) is a\n"
    "  # binfmt_misc file system and DIR cannot be searched (cd fails) or holds WSLInterop or WSLInterop-late (each name tested on its own: no glob, no listing).\n"
    "  # DIR is looked at only under a topmost binfmt_misc, so the check never triggers an automount. The two arguments exist to check it against the hook's function\n")
BF = 'binfmt_misc %s binfmt_misc rw,nosuid,nodev,noexec,relatime 0 0'
AF = 'systemd-1 %s autofs rw,relatime,fd=29,pgrp=1,timeout=0,minproto=5,maxproto=5,direct 0 0'
PR = 'proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0'

W1_TPL = r'''# What 1 supplement 2 (v3.4; TASK-005 D-1, D-2; review R2 M-1, m-1 and doubt 1): _sg_relax_nowslfs reads the mount table in one pass and takes the topmost
# mount at DIR (the table's last line for it); the entries are looked at only when that is binfmt_misc, so the look never triggers an automount, and the
# two names are tested one by one (no glob: noglob or failglob cannot change the look). A table that cannot be read or reads empty, or a DIR that cannot be
# searched, keeps the relaxation off. Fake mount tables and directories under $X; both modes
if need _sg_relax_nowslfs; then
  w1d="$X/w1-binfmt"; mkdir -p "$w1d" "$X/w1-tabledir"
@PA0@
@PA1@
  printf '@BF@\n@AF@\n@PR@\n' "$w1d" "$w1d" > "$X/w1-stacked"; : > "$X/w1-empty"
  w1x() {   # id mounts dir want what [setup] : _sg_relax_nowslfs MOUNTS DIR after SETUP (a shell option, set in the same subshell); status and stderr
    local r t=''
    r=$( [[ -z "${6:-}" ]] || eval "$6"; _sg_relax_nowslfs "$2" "$3" 2>"$X/w1e"; echo $? )
    [[ $r == "$4" ]] || t+='[status] '; [[ -s "$X/w1e" ]] && t+='[stderr]'
    [[ -z "$t" ]]; chk $? "$1" "$5: status $r (want $4), stderr $(wc -c < "$X/w1e") bytes (want 0)" "${t% }"
  }
  w1() { rm -f "$w1d"/*; : > "$w1d/$3"; w1x "$1" "$2" "$w1d" "$4" "$5" "${6:-}"; }   # id mounts entry want what [setup] : DIR = $w1d holding only ENTRY (the last line of each table does not match)
  sel @a@ && w1 @a@ "$X/w1-autofs" WSLInterop 0 "an autofs mount point at DIR (nothing mounted) that holds WSLInterop"
  sel @b@ && w1 @b@ "$X/w1-mounted" WSLInterop-late 1 "binfmt_misc mounted at DIR, holding WSLInterop-late"
  sel @c@ && w1 @c@ "$X/w1-mounted" status 0 "binfmt_misc mounted at DIR, neither WSLInterop nor WSLInterop-late in it"
  sel @d@ && w1 @d@ "$X/w1-none/mounts" WSLInterop 1 "a mount table that cannot be read"
  sel @f@ && w1 @f@ "$X/w1-empty" status 1 "a mount table that reads empty (0 lines; no WSL entry in DIR)"
  sel @g@ && w1 @g@ "$X/w1-stacked" WSLInterop 0 "binfmt_misc at DIR with autofs mounted on top of it (the topmost mount decides: not looked at), DIR holding WSLInterop"
  sel @h@ && w1 @h@ "$X/w1-tabledir" status 1 "a directory given as the mount table (no WSL entry in DIR)"
  sel @i@ && w1 @i@ "$X/w1-mounted" WSLInterop-late 1 "under set -f (noglob, which the environment can import): binfmt_misc mounted at DIR, holding WSLInterop-late" 'set -f'
  sel @j@ && w1 @j@ "$X/w1-mounted" status 0 "under shopt -s failglob: binfmt_misc mounted at DIR, neither name in it" 'shopt -s failglob'
  if sel @k@; then   # a DIR that cannot be searched: the entries cannot be seen, so they may exist (review R2 m-1). uid 0 searches any directory: not applicable there
    if [[ "$(id -ru)" == 0 ]]; then out SKIP @k@ "[platform] uid 0 searches a directory of mode 000, so a DIR that cannot be searched cannot be made here"
    else
      w1k="$X/w1-nosearch"; mkdir -p "$w1k"; printf '@BF@\n@PR@\n' "$w1k" > "$X/w1-nosearch-mounts"; chmod 000 "$w1k"
      w1x @k@ "$X/w1-nosearch-mounts" "$w1k" 1 "binfmt_misc mounted at DIR, DIR of mode 000 (cannot be searched; nothing in it)"; chmod 755 "$w1k"
    fi
  fi
  if sel @l@; then   # a DIR that can be searched but not listed (mode 0311): each name is still seen, where a glob sees none (review R2 m-1)
    w1l="$X/w1-listless"; mkdir -p "$w1l"; : > "$w1l/WSLInterop-late"; printf '@BF@\n@PR@\n' "$w1l" > "$X/w1-listless-mounts"; chmod 0311 "$w1l"
    w1x @l@ "$X/w1-listless-mounts" "$w1l" 1 "binfmt_misc mounted at DIR, DIR of mode 0311 (searched, not listed) holding WSLInterop-late"; chmod 755 "$w1l"
  fi
else miss @a@ @b@ @c@ @d@ @f@ @g@ @h@ @i@ @j@ @k@ @l@; fi
# What 1 supplement 2 (v3.4): the gate asks for the WSL mark of the file system after the platform and the time, so where either closes the gate the mount
# table is never read. _sg_relax_nowslfs stubbed to count its calls, on a freshly sourced hook with no WSL mark in the environment; both modes
if sel @m@; then
  if need _sg_relax_ok _sg_relax_platform _sg_relax_left _sg_relax_nowslfs _sg_relax_noext; then
    w1m() {   # PLATFORM LEFT : the _sg_relax_nowslfs calls of one _sg_relax_ok, with _sg_relax_platform returning PLATFORM and _sg_relax_left returning LEFT
      : > "$X/w1m"
      ( source "$H" </dev/null >/dev/null 2>&1; set +e; unset _SG_RELAXED WSL_DISTRO_NAME WSL_INTEROP; w1mp=$1 w1ml=$2
        _sg_relax_platform() { return "$w1mp"; }; _sg_relax_left() { return "$w1ml"; }
        _sg_relax_nowslfs() { printf x >> "$X/w1m"; return 0; }; _sg_relax_noext() { echo none; }
        _sg_relax_ok ) >/dev/null 2>&1
      wc -c < "$X/w1m" | tr -d ' '
    }
    w1m1=$(w1m 1 0); w1m2=$(w1m 0 1); w1m3=$(w1m 0 0); t=''
    [[ $w1m1 == 0 ]] || t+='[platform] '; [[ $w1m2 == 0 ]] || t+='[time] '; [[ $w1m3 == 1 ]] || t+='[control]'
    [[ -z "$t" ]]; chk $? @m@ "_sg_relax_nowslfs calls in one _sg_relax_ok: the platform fails $w1m1 (want 0), no time left $w1m2 (want 0), both pass $w1m3 (want 1: the stub is reached)" "${t% }"
  else miss @m@; fi
fi
'''
W1E_TPL = r'''  if sel @e@; then   # What 1 supplement 2 (v3.4): the gate's last check before the extension -- _sg_relax_nowslfs failing closes the gate on this relaxing bash.
    # Two sides, so that a gate closed by an earlier check cannot pass the case: every check before it passes here (a fresh anchor, budget 3, no WSL mark in
    # the environment, this bash's platform; _sg_relax_noext stubbed to print none), so the stub returning 0 must open the gate and returning 1 must close it
    if need _sg_relax_ok _sg_relax_nowslfs _sg_relax_noext; then
      w1e() { ( v15src; unset _SG_RELAXED WSL_DISTRO_NAME WSL_INTEROP; export @BUD@=3; w1es=$1
                _sg_relax_nowslfs() { return "$w1es"; }; _sg_relax_noext() { echo none; }; _SG_P0=${EPOCHREALTIME:-}; gate ); }
      w1e0=$(w1e 0); w1e1=$(w1e 1); t=''
      [[ $w1e0 == 0 ]] || t+='[open] '; [[ $w1e1 == 1 ]] || t+='[closed]'
      [[ -z "$t" ]]; chk $? @e@ "every check before it passing: _sg_relax_nowslfs stubbed to return 0 -> _sg_relax_ok status $w1e0 (want 0), stubbed to return 1 (a WSLInterop entry, a DIR that cannot be searched, a mount table that cannot be read or reads empty) -> $w1e1 (want 1)" "${t% }"
    else miss @e@; fi
  fi
  if sel @n@; then   # What 1 supplement 2 (v3.4; review R2 M-1): awk reads the mount table in one pass. In a private mount namespace (unshare -rm) with 1000 tmpfs
    # mounts stacked on one directory, _sg_relax_nowslfs reads the real table and returns within 0.5 s (v3.3 read it line by line in bash, and procfs
    # regenerates the table at every seek back: 2.2 s there). Hard: the 1000 mounts made, status 0 (no WSL mark: MODE relax), stderr empty; soft (INV-7): the wall
    if ! need _sg_relax_nowslfs; then miss @n@
    elif ! unshare -rm true >/dev/null 2>&1; then out SKIP @n@ "[platform] unshare -rm (a private user and mount namespace) is not available here"
    else
      printf '%s\n' 'source "$1" </dev/null >/dev/null 2>&1; set +e; m=$2/w1n-m; mkdir -p "$m"; n=0' \
        'while (( n < 1000 )); do mount -t tmpfs w1n "$m" 2>/dev/null || break; n=$(( n + 1 )); done' \
        't0=$EPOCHREALTIME; _sg_relax_nowslfs 2>"$2/w1n-e"; r=$?; t1=$EPOCHREALTIME' \
        'echo "$n $r $(grep -c "" /proc/self/mounts) ${t0/,/.} ${t1/,/.}"' > "$X/w1n.sh"
      read -r w1nn w1nr w1nl w1n0 w1n1 <<< "$(unshare -rm "$BASH" "$X/w1n.sh" "$H" "$X" 2>/dev/null)"
      if [[ "${w1nn:-0}" == 0 ]]; then out SKIP @n@ "[platform] tmpfs cannot be mounted in a private mount namespace here"
      else
        w1nw=$(awk -v a="${w1n0:-0}" -v b="${w1n1:-0}" 'BEGIN{printf "%.3f", b-a}'); w1nh=ok; w1ns=ok
        [[ $w1nn == 1000 && $w1nr == 0 && ! -s "$X/w1n-e" ]] || w1nh=bad; le "$w1nw" 0.5 || w1ns=bad
        timed @n@ $w1nh $w1ns "1000 tmpfs mounts stacked in a private mount namespace ($w1nn made, the table $w1nl lines): _sg_relax_nowslfs on the real table returned $w1nr (want 0) in ${w1nw} s (want <= 0.5), stderr $(wc -c 2>/dev/null < "$X/w1n-e" || echo '?') bytes (want 0)"
      fi
    fi
  fi
'''
T2_OLD = "    # (a bad implementation) gives about 3 s there, and a slow host only makes the value smaller (it reaches 0 only after 1.0 s from here to the judgement)\n"
T2_NEW = ("    # (a bad implementation) gives about 3 s there, and a slow host only makes the value smaller. The value is fixed by the two _sg_relax_left calls, in the\n"
          "    # gate and in the run (the job gets the run's): more than 1.0 s from setting the anchor here to those calls closes the gate or makes the run fall back,\n"
          "    # and the judgement never runs (_SG_LEFT [], a false red)\n")
W1_START = '# What 1 supplement 2 (TASK-005 D-1, D-2): _sg_relax_nowslfs looks at the WSLInterop* entries only under a mounted binfmt_misc, so the look never\n'
W1_END = 'else miss %s %s %s %s; fi\n' % (ID['a'], ID['b'], ID['c'], ID['d'])
W1E_START = '  if sel %s; then' % ID['e']
W1E_END = '    else miss %s; fi\n  fi\n' % ID['e']

def direct(t, wmv):
    t = repl_fn(t, 'wslmark() {', wm_head(wmv) + WM_BODY, 'wslmark')
    assert t.count(W1_START) == 1 and t.count(W1_END) == 1
    i = t.index(W1_START); j = t.index(W1_END, i) + len(W1_END)
    pa = [x for x in t[i:j].split('\n') if x.startswith('  printf ')]
    assert len(pa) == 2 and 'w1-autofs' in pa[0] and 'w1-mounted' in pa[1], pa
    d = dict(ID); d.update(PA0=pa[0], PA1=pa[1], BF=BF, AF=AF, PR=PR)
    t = t[:i] + sub(W1_TPL, d) + t[j:]
    t = once(t, T2_OLD, T2_NEW, 'T2 comment')
    assert t.count(W1E_START) == 1
    i = t.index(W1E_START); j = t.index(W1E_END, i) + len(W1E_END)
    d = dict(ID); d.update(BUD=BUD)
    return t[:i] + sub(W1E_TPL, d) + t[j:]

T['helper'] = direct(T['helper'], 'WSLM')
T['helper'] = once(T['helper'], ' %s"   # the cases of MODE relax' % ID['e'], ' %s %s"   # the cases of MODE relax' % (ID['e'], ID['n']), 'RELAX_IDS')
T['scdirect'] = direct(T['scdirect'], 'WSLM')

t = T['suite']
t = repl_fn(t, 'sg_w10_wslfs() {', SUITE_HEAD + WM_BODY, 'sg_w10_wslfs')
i = t.index('SGW_EXP_DIRECT="'); j = t.index('"', i + len('SGW_EXP_DIRECT="'))
lst = t[i:j]
assert lst.count(ID['d']) == 1 and lst.count(ID['e']) == 1
lst = lst.replace(ID['d'], ID['d'] + ' ' + BOTH_NEW).replace(ID['e'], ID['e'] + ' ' + ID['n'])
t = t[:i] + lst + t[j:]
t = once(t, '# Coverage: 981 cases (975 without zsh)', '# Coverage: 990 cases (984 without zsh)', 'suite count')
T['suite'] = t

t = T['sccases']
t = repl_fn(t, 'wslmark() {', wm_head('WSLF') + WM_BODY, 'sc-cases wslmark')
t = once(t, ' %s"\n' % ID['d'], ' %s %s"\n' % (ID['d'], BOTH_NEW), 'EXP_DIRECT_BOTH')
t = once(t, ' %s"\n' % ID['e'], ' %s %s"\n' % (ID['e'], ID['n']), 'EXP_DIRECT_RELAX')
t = once(t, "#            it, and no WSL mark in the file system (wslmark below, the rule of What 1 supplement 2 written apart from the hook's _sg_relax_nowslfs: a\n"
            "#            mount table that cannot be read, or a WSLInterop* entry under a binfmt_misc mounted at /proc/sys/fs/binfmt_misc). Every run of the hook clears\n",
            "#            it, and no WSL mark in the file system (wslmark below, the rule of What 1 supplement 2 (v3.4) written apart from the hook's _sg_relax_nowslfs:\n"
            "#            a mount table that cannot be read or reads empty, or a binfmt_misc topmost at /proc/sys/fs/binfmt_misc whose directory cannot be searched or\n"
            "#            holds WSLInterop or WSLInterop-late). Every run of the hook clears\n", 'sc-cases header')
T['sccases'] = t

# ---------------- C. v31 tools ----------------
T['mutants'] = once(T['mutants'], r"""[('  _sg_relax_left || return 1\n  [[ "$( _sg_relax_noext', '  [[ "$( _sg_relax_noext')]""",
                    r"""[('  _sg_relax_left || return 1\n  _sg_relax_nowslfs', '  _sg_relax_nowslfs')]""", 'mutants.py anchor')
T['w14m'] = once(T['w14m'], "[('''  _sg_relax_left || return 1\n  [[ \"$( _sg_relax_noext''',\n       '''  [[ \"$( _sg_relax_noext''')])",
                 "[('''  _sg_relax_left || return 1\n  _sg_relax_nowslfs''',\n       '''  _sg_relax_nowslfs''')])", 'w14 Q-30 anchor')
T['w14m'] = once(T['w14m'], 'IMPL_SHA12 = "834dee6db0d0"', 'IMPL_SHA12 = "%s"' % SHA12, 'IMPL_SHA12')

for k, pth in F.items():
    open(pth, 'w', encoding='utf-8', newline='').write(T[k])
print('written:', ', '.join(F))
print('new both-mode ids:', BOTH_NEW); print('new relax id:', ID['n'])

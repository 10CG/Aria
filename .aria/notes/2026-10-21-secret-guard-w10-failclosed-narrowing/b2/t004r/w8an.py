import sys, re, subprocess, hashlib
P = '/home/dev/Aria/openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md'
proto, impl, prev, out = sys.argv[1:5]
sha = lambda f: hashlib.sha256(open(f, 'rb').read()).hexdigest()[:12]
prop = open(P, encoding='utf-8').read().split('\n')
def find(pat):
    for i, l in enumerate(prop):
        if re.search(pat, l): return i
    raise SystemExit('marker not found: ' + pat)
s1, s12, e1 = find(r'^\*\*What 1 补充：'), find(r'^\*\*What 1 补充 2：'), find(r'^### 2\. ')
s6, e6 = find(r'^### 6\. '), find(r'^### 7\. ')
s7, s72, e7 = find(r'^\*\*What 7 补充：'), find(r'^\*\*What 7 补充 2：'), find(r'^### 参考实现')
SEC = {'What1补充': (s1, s12), 'What1补充2': (s12, e1), 'What6': (s6, e6), 'What7补充': (s7, s72), 'What7补充2': (s72, e7)}
fen, inl, txt = {}, {}, {}
for k, (a, b) in SEC.items():
    f, inside, spans = [], False, []
    for l in prop[a:b]:
        if l.lstrip().startswith('```'): inside = not inside; continue
        if inside: f.append(l.rstrip())
        else: spans += re.findall(r'`([^`]+)`', l)
    fen[k], inl[k], txt[k] = f, spans, '\n'.join(prop[a:b])
I = [l.rstrip('\n') for l in open(impl, encoding='utf-8', errors='replace')]
Pv = set(l.rstrip('\n') for l in open(prev, encoding='utf-8', errors='replace'))
Pr = set(l.rstrip('\n') for l in open(proto, encoding='utf-8', errors='replace'))
Is = set(I)
o = open(out, 'w')
def say(s): o.write(s + '\n')
say('proto %s impl %s prev(2893bcc) %s | proposal sections (0-based start line): %s' % (sha(proto), sha(impl), sha(prev), {k: v[0] + 1 for k, v in SEC.items()}))
d = subprocess.run(['diff', '-u', '-F', r'^[_A-Za-z0-9]* *()', proto, impl], capture_output=True, text=True).stdout.split('\n')
h0 = subprocess.run(['diff', '-U0', proto, impl], capture_output=True, text=True).stdout.count('\n@@')
hp = subprocess.run(['diff', '-u', prev, impl], capture_output=True, text=True).stdout.count('\n@@')
hunks, cur = [], None
for l in d[2:]:
    if l.startswith('@@'): cur = {'h': l, 'p': [], 'm': []}; hunks.append(cur)
    elif cur is not None and l.startswith('+'): cur['p'].append(l[1:])
    elif cur is not None and l.startswith('-'): cur['m'].append(l[1:])
say('hunks proto->impl (diff -u): %d | diff -U0 hunks: %d | prev->impl (diff -u) hunks: %d' % (len(hunks), h0, hp))
def where(line):
    ex = [k for k in SEC if line.rstrip() in fen[k]]
    il = [k for k in SEC if line.strip() and any(line.strip() == s.strip() for s in inl[k])]
    lo = [k for k in SEC if line.strip() and line.strip() in txt[k]]
    return ex, il, lo
for n, h in enumerate(hunks, 1):
    cls, un, unl = set(), [], []
    for l in h['p']:
        ex, il, lo = where(l)
        if not l.strip(): continue
        if ex or il: cls |= set(ex + il)
        else: un.append(l); unl.append(lo)
    mcls = set()
    for l in h['m']:
        ex, il, lo = where(l); mcls |= set(ex + il + lo)
    say('H%d %s | -%d +%d | + lines verbatim in: %s | + lines not verbatim in any of the five: %d | - lines found in: %s' % (n, h['h'][:90], len(h['m']), len(h['p']), ','.join(sorted(cls)) or '-', len(un), ','.join(sorted(mcls)) or '-'))
    for l, lo in zip(un, unl): say('    unmatched+ (substring in: %s): %s' % (','.join(lo) or 'none', l[:150]))
for k in SEC:
    a = [l for l in fen[k] if l.strip()]
    ini = sum(l in Is for l in a); pvo = sum((l not in Is) and (l in Pv) for l in a); pro = sum((l not in Is) and (l not in Pv) and (l in Pr) for l in a)
    none = [l for l in a if l not in Is and l not in Pv and l not in Pr]
    say('reverse %-11s fenced non-blank lines %3d: in impl %3d | not in impl but in prev %d | only in proto %d | in none %d' % (k, len(a), ini, pvo, pro, len(none)))
    for l in none[:6]: say('    in none: %s' % l[:150])

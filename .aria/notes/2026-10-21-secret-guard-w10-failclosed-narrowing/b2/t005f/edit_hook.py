import sys, re, textwrap
hook, prop = sys.argv[1], sys.argv[2]
L = open(hook, encoding='utf-8').read().split('\n')
P = open(prop, encoding='utf-8').read().split('\n')
# verbatim code from proposal What 1 supplement 2: the first two ```bash blocks after its heading
h = next(i for i, s in enumerate(P) if s.startswith('**What 1 补充 2'))
blocks, cur, inb = [], [], False
for s in P[h+1:]:
    if s.startswith('```bash'): inb, cur = True, []; continue
    if inb and s.startswith('```'): blocks.append(cur); inb = False
    elif inb: cur.append(s)
    if len(blocks) == 2: break
wsl2, fn = blocks
assert len(wsl2) == 2 and fn[0].startswith('_sg_relax_nowslfs() {') and fn[-1] == '}', (wsl2, fn[0], fn[-1])
def idx(pred, what):
    r = [i for i, s in enumerate(L) if pred(s)]
    assert len(r) == 1, (what, r); return r[0]
def rewrap(i0, i1, prefix, width, old, new, what):
    seg = L[i0:i1+1]
    assert all(s.startswith(prefix) for s in seg), what
    txt = ' '.join(s[len(prefix):].strip() for s in seg)
    assert txt.count(old) == 1, (what, txt.count(old))
    out = textwrap.wrap(txt.replace(old, new), width=width - len(prefix), break_long_words=False, break_on_hyphens=False)
    L[i0:i1+1] = [prefix + s for s in out]
    print(f'{what}: {i1-i0+1} lines -> {len(out)} (width {width})')
# 1. WSL line -> two lines (verbatim)
i = idx(lambda s: '|| -e /proc/sys/fs/binfmt_misc/WSLInterop ]] && wsl=wsl' in s, 'wsl line'); L[i:i+1] = wsl2
# 2. _sg_relax_nowslfs right after _sg_relax_platform (above the sourcing gate)
i = idx(lambda s: s.startswith('_sg_relax_platform() {'), 'platform'); j = next(k for k in range(i, len(L)) if L[k] == '}'); L[j+1:j+1] = fn
# What 7 supplement 2, 1: header bullet
i0 = idx(lambda s: s.endswith('(fail-closed, owner ruling 2026-10-14). A substituted copy over 8192 characters is'), 'hdr0')
i1 = idx(lambda s: s.startswith('#     the rerun still blocks. The pass substitutes text; it does not run the shell: a'), 'hdr1')
w = max(len(L[k]) for k in range(i0 - 6, i1 + 4))
rewrap(i0, i1, '#     ', w,
 'A substituted copy over 8192 characters is blocked for its size only where the relaxed rerun of 10CG/aria-plugin#217 is not in effect; where it is (an x86_64 GNU/Linux build of bash 5.0-5.3 outside WSL, no project extension, time left), the pass is re-run under a hard deadline with no count bound, the growth over the input as the limit and the copy judged in full, and growth over 8192 characters, the deadline or any failure of the rerun still blocks.',
 'A substituted copy over 8192 characters is blocked for its size wherever the relaxed rerun of 10CG/aria-plugin#217 is not in effect, and also where it is (an x86_64 GNU/Linux build of bash 5.0-5.3 outside WSL, no project extension, time left) whenever that rerun falls back. The rerun runs the pass again under a hard deadline with no count bound, the growth over the input as the limit and the copy judged in full: growth over 8192 characters blocks with the growth text, a value over 4096 characters with the value text (the rerun reaches values that the counts cut off in the baseline pass), and the deadline, a time checkpoint, the self-check or any other failure of the rerun falls back to that size block.', 'hdr')
# 2: LENGTH BUDGET
i0 = idx(lambda s: 'Elsewhere, and whenever the rerun does not finish in time, the command is blocked with the size text' in s, 'lb0')
i1 = idx(lambda s: s.endswith('the relaxed rerun has no count bound, the deadline caps its cost.)'), 'lb1'); assert i1 == i0 + 2
w = max(len(L[k]) for k in range(i0 - 3, i1 + 1))
rewrap(i0, i1, '# ', w, 'whenever the rerun does not finish in time,', 'whenever the rerun neither allows nor blocks on its own (the deadline, a time checkpoint, the self-check, any other failure),', 'lb')
# 3: _sg_relax_noext trailing comment
i = idx(lambda s: s.startswith('_sg_relax_noext() {   # '), 'noext')
old = '# prints "none" only when no extension can be in effect: no project root, or no .aria/secret-guard.paths under it. A file in any state, or an error, keeps the relaxation off'
assert L[i].endswith(old); L[i] = L[i][:-len(old)] + '# prints "none" only when no extension can be in effect: no project root is found (_sg_ext_root prints nothing, which includes a cwd that jq cannot read: without a root no extension can be in effect), or there is no .aria/secret-guard.paths under it. A file there, in any state, keeps the relaxation off'
# 4: _sg_vx_pass description
i0 = idx(lambda s: s.endswith('(_sg_relax_ok; the baseline block text is kept'), 'vx0'); i1 = i0 + 3; assert L[i1] == '# or judged.', L[i1]
w = max(len(L[k]) for k in range(i0 - 2, i1))
rewrap(i0, i1, '# ', w, 'the baseline block text is kept in _SG_OV_PAT / _SG_OV_MODE for the fallback)', 'the baseline reason string and mode are kept in _SG_OV_PAT / _SG_OV_MODE -- not a text: on a fallback _sg_emit_blocked writes the baseline block text from them again)', 'vx')
# 5: relaxed-rerun block head
i0 = idx(lambda s: s.startswith('# deadline, a time checkpoint, the self-check, an internal error, a bare 0 -- falls back to the baseline block, byte for byte.'), 'rr0')
i1 = idx(lambda s: s == '# absolute limit anyway), and with time left before the deadline.', 'rr1'); assert i1 == i0 + 2
w = max(len(L[k]) for k in range(i0 - 7, i0))
rewrap(i0, i1, '# ', w, 'falls back to the baseline block, byte for byte.', 'falls back to the baseline block, byte for byte. The one exception (What 4): a fatal error of bash itself inside the job that makes it exit with status 2 and write its error message is passed on as the block text -- the command is still blocked, but with bash\'s message instead of the baseline text.', 'rr')
open(hook, 'w', encoding='utf-8').write('\n'.join(L))

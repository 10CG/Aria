# build the expected v3.4 hook from the 710a36d hook and the proposal's code blocks (header comment D-3 sentence excluded: free text)
import sys, re
hook, prop, out = sys.argv[1:4]
h = open(hook, encoding='utf-8').read()
p = open(prop, encoding='utf-8').read()
sec = p[p.index('**What 1 补充 2'):p.index('### 2. 放宽重跑的规则')]
blocks = re.findall(r'```bash\n(.*?)```', sec, re.S)
assert len(blocks) == 2, len(blocks)
gate1, gate2 = blocks[0].rstrip('\n').split('\n')
func = blocks[1]
old_wsl = [l for l in h.split('\n') if l.startswith('  [[ -n "$wsl" ]] || _sg_relax_nowslfs || wsl=wsl')]
assert len(old_wsl) == 1
h = h.replace(old_wsl[0] + '\n', '', 1)
assert h.count(gate1 + '\n') == 1   # the first line is unchanged from 710a36d
i = h.index('_sg_relax_ok() {'); j = h.index('\n}\n', i)
body = h[i:j]
anchor = '  _sg_relax_left || return 1\n'
assert body.count(anchor) == 1
body = body.replace(anchor, anchor + gate2 + '\n')
h = h[:i] + body + h[j:]
k = h.index('_sg_relax_nowslfs() {'); m = h.index('\n}\n', k) + 3
h = h[:k] + func + h[m:]
open(out, 'w', encoding='utf-8').write(h)
print('ok', len(h))

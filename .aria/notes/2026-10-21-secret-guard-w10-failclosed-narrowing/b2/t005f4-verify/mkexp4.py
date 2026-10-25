# expected 5f4 hook = the 3ed6c24 hook with the gate's second line and the whole _sg_relax_nowslfs taken from proposal v3.5 (nothing else changes)
import sys, re
hook, prop, out = sys.argv[1:4]
h = open(hook, encoding='utf-8').read(); p = open(prop, encoding='utf-8').read()
sec = p[p.index('**What 1 补充 2'):p.index('### 2. 放宽重跑的规则')]
blocks = re.findall(r'```bash\n(.*?)```', sec, re.S); assert len(blocks) == 2
g2 = blocks[0].rstrip('\n').split('\n')[1]; func = blocks[1]
old = [l for l in h.split('\n') if l.startswith('  _sg_relax_nowslfs || return 1   #')]; assert len(old) == 1
h = h.replace(old[0], g2, 1)
k = h.index('_sg_relax_nowslfs() {'); m = h.index('\n}\n', k) + 3
h = h[:k] + func + h[m:]
open(out, 'w', encoding='utf-8').write(h); print('ok', len(h))

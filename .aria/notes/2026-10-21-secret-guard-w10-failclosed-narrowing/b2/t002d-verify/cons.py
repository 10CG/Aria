# cons.py <commentsync.py> <suite> <out dir> : two constructions on copies of the suite for commentsync (c1: one character changed in a new sentence of site 9;
# c2: the rewritten comment run right before the 21ag case deleted). Prints what it changed (no file content beyond one word).
import ast, sys, re, collections
cs, suite, out = sys.argv[1:4]
tree = ast.parse(open(cs, encoding='utf-8').read())
ST = [ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', '') == 'SUITE_TEXT'][0]
s9 = [x for x in ST if x[0].startswith('9 ')][0]; raw = open(suite, encoding='utf-8').read()
words = collections.Counter(re.findall(r'[A-Za-z_]{6,}', raw))
w = next(x for sent in s9[3] for x in re.findall(r'[A-Za-z_]{6,}', sent) if words[x] == 1)
c1 = raw.replace(w, w[:-1] + ('X' if w[-1] != 'X' else 'Y'), 1); open(f'{out}/c1.sh', 'w', encoding='utf-8').write(c1)
print('c1: changed the unique word', w, 'of a new sentence of site 9')
L = raw.split('\n'); i = next(k for k, l in enumerate(L) if l.startswith('wpa_begin_bash_case "W10 SC-21ag'))
j = i
while j > 0 and L[j - 1].startswith('#'): j -= 1
open(f'{out}/c2.sh', 'w', encoding='utf-8').write('\n'.join(L[:j] + L[i:])); print('c2: deleted', i - j, 'comment lines before the 21ag case')

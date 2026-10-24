# excerpt of a full-round output: header and summary lines, the six groups' FAIL lines in full, every other FAIL by its id only (its detail dropped:
# fixture command text there can be credential-path shaped). Usage: excerpt.py <in> <out>
import re, sys
src, dst = sys.argv[1], sys.argv[2]
keep = re.compile(r'^(# |PASS:|FAIL:|SKIP:|W10 ported|W10 older|Coverage)')
six = re.compile(r'^  FAIL \[W10 SC-21a(b|c|g|j|l|o)\b')
out = [f'# excerpt of {src.rsplit("/", 1)[-1]} by excerpt.py: summary lines, the six groups in full, other FAILs by id only']
for ln in open(src, encoding='utf-8', errors='replace'):
    ln = ln.rstrip('\n')
    if keep.match(ln) or six.match(ln): out.append(ln)
    elif ln.startswith('  FAIL ['):
        m = re.match(r'^  FAIL \[([^\]]*)\]', ln); out.append(f'  FAIL [{m.group(1) if m else "?"}] (detail dropped)')
open(dst, 'w', encoding='utf-8').write('\n'.join(out) + '\n'); print(dst.rsplit('/', 1)[-1], len(out))

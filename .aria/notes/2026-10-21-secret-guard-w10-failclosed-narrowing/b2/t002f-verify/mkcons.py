# my own constructions for the 3c2 check (not the author's): the relaxed job ends with status 1 (fallback) a fixed time after its timer is up
import sys
src, out = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
a = '  [[ -n "$tp" ]] && kill -0 "$tp" 2>/dev/null || return 9'
assert s.count(a) == 1
cons = {
  'c5': "  sleep 0.5; return 1   # verify-3c2 C5: the job fails 0.5 s after its timer is up (a quick failure, not time)",
  'c3p': "  sleep 2.05; return 1   # verify-3c2 C3': the job ends 2.05 s after its timer is up (the lower edge of the rerun's checkpoint window)",
}
for k, line in cons.items():
    i = s.index("\n", s.index(a))
    open(f'{out}/{k}.sh', 'w', encoding='utf-8').write(s[:i] + '\n' + line + s[i:])
print('ok')

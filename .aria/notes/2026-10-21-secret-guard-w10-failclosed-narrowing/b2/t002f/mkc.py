import sys
src, o = sys.argv[1], sys.argv[2]
t = open(src, encoding='utf-8', newline='').read()
def one(t, old, new, tag):
    n = t.count(old)
    if n != 1:
        sys.exit(f'{tag}: {n} hits')
    return t.replace(old, new)
c1 = one(t, '  [[ -z "${_SG_RELAXED:-}" ]] || return 1\n  local osr= wsl=\n',
         '  return 1   # construction C1 (3c): the admission gate is always closed\n  [[ -z "${_SG_RELAXED:-}" ]] || return 1\n  local osr= wsl=\n', 'c1')
c2 = one(t, '  _SG_RELAXED=1\n  _sg_vx_pass "$1" "$_SG_MODE"\n',
         '  sleep 4   # construction C2 (3c): the rerun is held past the deadline (its timer already runs)\n  _SG_RELAXED=1\n  _sg_vx_pass "$1" "$_SG_MODE"\n', 'c2')
a = '2>/dev/null || return 9   # no running timer, no judgement: the deadline must exist before the first expensive step\n  _SG_RELAXED=1\n'
c3 = one(t, a, a.replace('  _SG_RELAXED=1\n', "  sleep 2.2; return 1   # construction C3 (3c2): the rerun's checkpoint sends it back 2.2 s after the job starts\n  _SG_RELAXED=1\n"), 'c3')
for n, b in (('c1', c1), ('c2', c2), ('c3', c3)):
    open(f'{o}/{n}-hook.sh', 'w', encoding='utf-8', newline='').write(b)
print('constructions built')

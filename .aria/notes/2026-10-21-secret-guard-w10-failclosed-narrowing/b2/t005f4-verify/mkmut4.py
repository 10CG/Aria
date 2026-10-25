# 主控自己的坏实现 (5f4 复核; 由 5f3 复核的 mkmut3.py 改锚点为 v3.5 原文, 另加 MD): 从被测 hook 机械构造, 锚点取 proposal v3.4 的字面; 每处锚点须恰好出现一次
import sys, os
hook, outdir = sys.argv[1:3]
h = open(hook, encoding='utf-8').read()
AWK = """  r=$(awk -v d="$d" '$2 == d { t = $3 } END { print NR, t }' "${1:-/proc/self/mounts}" 2>/dev/null) || return 1\n"""
LOOK = """  [[ -e "$d/WSLInterop" || -e "$d/WSLInterop-late" ]] && return 1\n"""
XLINE = """  [[ -d "$d" && -x "$d" ]] || return 1   # DIR is not a directory that can be searched: the entries cannot be seen, so they may exist\n"""
NRLINE = """  [[ "${r%% *}" =~ ^[1-9][0-9]*$ ]] || return 1   # no line read: a table that cannot be read, or reads empty\n"""
G2 = [l + '\n' for l in h.split('\n') if l.startswith('  _sg_relax_nowslfs || return 1   #')]
assert len(G2) == 1, len(G2)
G2 = G2[0]
LOCAL = '  local osr= wsl=\n'
M = {
 'MW-while-read': [(AWK, """  local m f n=0 t=; { while read -r _ m f _; do n=$((n+1)); if [[ "$m" == "$d" ]]; then t=$f; fi; done; } 2>/dev/null < "${1:-/proc/self/mounts}" || return 1; r="$n $t"\n""")],
 'MG-glob': [(LOOK, """  local e; for e in "$d"/WSLInterop*; do if [[ -e "$e" ]]; then return 1; fi; done\n""")],
 'MF-first-line': [("""'$2 == d { t = $3 } END { print NR, t }'""", """'$2 == d && t == "" { t = $3 } END { print NR, t }'""")],
 'MX-no-dir-search-check': [(XLINE, '')],
 'MD-no-dir-check': [(XLINE, XLINE.replace('[[ -d "$d" && -x "$d" ]]', '[[ -x "$d" ]]', 1))],
 'MO-before-platform': [(G2, ''), (LOCAL, LOCAL + G2)],
 'ME-empty-as-none': [(NRLINE, '')],
 'MS-result-ignored': [(G2, G2.replace('_sg_relax_nowslfs || return 1', '_sg_relax_nowslfs || :', 1))],
 'MI-inverted': [(G2, G2.replace('_sg_relax_nowslfs || return 1', '_sg_relax_nowslfs && return 1', 1))],
 'MN-one-name': [(LOOK, LOOK.replace(' || -e "$d/WSLInterop-late"', '', 1))],
}
os.makedirs(outdir, exist_ok=True)
for name, reps in M.items():
    s = h
    for old, new in reps:
        n = s.count(old)
        assert n == 1, (name, n, old[:50])
        s = s.replace(old, new, 1)
    assert s != h
    open(os.path.join(outdir, name + '.sh'), 'w', encoding='utf-8').write(s)
print('wrote', len(M))

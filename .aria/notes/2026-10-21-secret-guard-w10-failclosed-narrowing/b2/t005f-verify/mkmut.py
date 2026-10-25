# the main loop's own bad implementations for the TASK-005 fix round (not the author's B1-B9): one verbatim replacement each, asserted to match once
import sys, os
src, out = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
M = {
 'M-A-exact-name-only': ('  for e in "$d"/WSLInterop*; do [[ -e "$e" ]] && return 1; done', '  [[ -e "$d/WSLInterop" ]] && return 1'),
 'M-B-unreadable-table-opens': ('2>/dev/null < "${1:-/proc/self/mounts}" || return 1', '2>/dev/null < "${1:-/proc/self/mounts}" || return 0'),
 'M-D-gate-inverted': ('  [[ -n "$wsl" ]] || _sg_relax_nowslfs || wsl=wsl', '  [[ -n "$wsl" ]] || ! _sg_relax_nowslfs || wsl=wsl'),
 'M-E-timer-sleeps-budget': ('( sleep "$_SG_LEFT"; kill', '( sleep "$_SG_TIME_BUDGET"; kill'),
}
os.makedirs(out, exist_ok=True)
for k, (a, b) in M.items():
    assert s.count(a) == 1, (k, s.count(a))
    open(os.path.join(out, k + '.sh'), 'w', encoding='utf-8').write(s.replace(a, b))
print('built', len(M))

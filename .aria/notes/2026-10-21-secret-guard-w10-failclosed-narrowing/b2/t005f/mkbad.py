import sys
src, out = sys.argv[1], sys.argv[2]
t0 = open(src, encoding='utf-8').read()
WSL2 = '''  [[ -n "${WSL_DISTRO_NAME:-}${WSL_INTEROP:-}" ]] && wsl=wsl   # WSL marks in the environment; the environment can only switch the relaxation off with them
  [[ -n "$wsl" ]] || _sg_relax_nowslfs || wsl=wsl   # a WSLInterop* entry under a mounted binfmt_misc, or a mount table that cannot be read'''
B = {
 'B1-wsl-old-line': (WSL2, '  [[ -n "${WSL_DISTRO_NAME:-}${WSL_INTEROP:-}" || -e /proc/sys/fs/binfmt_misc/WSLInterop ]] && wsl=wsl   # WSL marks; the environment can only switch the relaxation off with them'),
 'B2-and-m1': ('do if [[ "$l" == *" $d binfmt_misc "* ]]; then m=1; fi; done;', 'do [[ "$l" == *" $d binfmt_misc "* ]] && m=1; done;'),
 'B3-redirect-order': ('} 2>/dev/null < "${1:-/proc/self/mounts}"', '} < "${1:-/proc/self/mounts}" 2>/dev/null'),
 'B4-timer-sleeps-3': ('( sleep "$_SG_LEFT"; kill -KILL -- "-$me" )', '( sleep 3; kill -KILL -- "-$me" )'),
 'B5-anchor-in-job': ('  local me=$BASHPID tp\n', '  local me=$BASHPID tp\n  _SG_P0=${EPOCHREALTIME:-}; _sg_relax_left || return 9\n'),
 'B6-no-exec-2': ('out="$( exec 2>/dev/null; set -m', 'out="$( set -m'),
 'B7-anchor-in-run': ('  local out rc\n  _sg_relax_left || return 4', '  local out rc\n  _SG_P0=${EPOCHREALTIME:-}; _sg_relax_left || return 4'),
 'B8-anchor-in-gate': ('  [[ -z "${_SG_RELAXED:-}" ]] || return 1\n  local osr= wsl=\n', '  [[ -z "${_SG_RELAXED:-}" ]] || return 1\n  _SG_P0=${EPOCHREALTIME:-}\n  local osr= wsl=\n'),
 'B9-looks-unmounted': ('  (( m )) || return 0\n  for e in "$d"/WSLInterop*', '  for e in "$d"/WSLInterop*'),
}
for k, (a, b) in B.items():
    assert t0.count(a) == 1, (k, t0.count(a)); open(f'{out}/{k}.sh', 'w', encoding='utf-8').write(t0.replace(a, b))
print(len(B), 'bad hooks')

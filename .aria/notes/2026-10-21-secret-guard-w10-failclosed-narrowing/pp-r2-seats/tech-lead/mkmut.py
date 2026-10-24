#!/usr/bin/env python3
# tech-lead seat mutants: v3.1 prototype + ONE change each; every replacement must hit exactly once
import sys, os
src, out = sys.argv[1], sys.argv[2]
base = open(src, encoding='utf-8').read()
M = {
 'TL-M1': [('&& ca=1000000 cf=1000000   #', '&& ca=1000000   #')],
 'TL-M2': [('then _sg_vx_big_judge "$_SG_SUB" whole; return $?; fi', 'then _sg_vx_big_judge "$_SG_SUB" whole; fi')],
 'TL-M3': [('if [[ -n "${_SG_RELAXED:-}" ]] && (( ${#_SG_SUB} > _SGV_SMAX )); then _sg_vx_big_judge "$_SG_SUB" segment; else _sg_judge_one "$_SG_SUB" segment; fi',
            '_sg_judge_one "$_SG_SUB" segment')],
 'TL-M4': [('  while IFS= read -r line; do seen=1;', '  while read -r line; do seen=1;')],
 'TL-M5': [('''    if _sg_over_budget; then   # time-budget fail-closed before each per-segment _sg_vx_apply / _sg_judge_one (the O(copy^2) hot leg)
      [[ -n "${_SG_RELAXED:-}" ]] && return 3   # 10CG/aria-plugin#217 relaxed rerun: no time text of its own, the caller falls back to the baseline block
''', '''    if _sg_over_budget; then   # time-budget fail-closed before each per-segment _sg_vx_apply / _sg_judge_one (the O(copy^2) hot leg)
''')],
 'TL-M6': [('[[ $rc -eq 2 && -n "$out" ]] && {', '[[ $rc -eq 2 ]] && {')],
 'TL-M7': [('out="$( exec 2>/dev/null; set -m', 'out="$( set -m')],
 'TL-M8': [('  root="$(_sg_ext_root)"\n  if [[ -z "$root" || ! -e "$root/.aria/secret-guard.paths" ]]; then printf none; fi',
            '  root="${CLAUDE_PROJECT_DIR:-}"\n  if [[ -z "$root" || ! -e "$root/.aria/secret-guard.paths" ]]; then printf none; fi')],
 'TL-M9': [('  if (( max > _SGV_LMAX )); then _sg_judge_one "$1" "$2" nocredit;', '  if (( max >= _SGV_LMAX )); then _sg_judge_one "$1" "$2" nocredit;')],
 'TL-M10': [('! -e "$root/.aria/secret-guard.paths" ]]; then printf none; fi', '! -f "$root/.aria/secret-guard.paths" ]]; then printf none; fi')],
}
os.makedirs(out, exist_ok=True)
for k, pairs in M.items():
    t = base
    for old, new in pairs:
        n = t.count(old)
        if n != 1: sys.exit(f'{k}: hit {n} times: {old[:80]!r}')
        t = t.replace(old, new)
    open(os.path.join(out, k + '.sh'), 'w', encoding='utf-8').write(t)
print(len(M), 'mutants')

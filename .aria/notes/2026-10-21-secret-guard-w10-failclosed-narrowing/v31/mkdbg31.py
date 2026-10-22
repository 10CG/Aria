#!/usr/bin/env python3
"""mkdbg31.py <v3.1 hook> <out>: stage-timing instrumentation of a v3.1 hook (prototype or implementation) for the real-traffic replay. SG_DBG=<file>
receives "<EPOCHREALTIME> <stage>" lines: firstpass-done (after the built-in judgement), relax-start (the relaxed rerun begins: the trigger time),
relax-joined (the job is over). The probes are anchored on code lines, not on comments, and each comes after a statement whose status is already saved."""
import sys
t = open(sys.argv[1], encoding='utf-8').read()
D = '[[ -n "${SG_DBG:-}" ]] && printf "%s %s\\n" "$EPOCHREALTIME" '
def ins(old, new):
    global t
    assert t.count(old) == 1, (old[:60], t.count(old))
    t = t.replace(old, new)
ins('  _sg_core_eval "$cmd"\n  rc=$?\n', '  _sg_core_eval "$cmd"\n  rc=$?\n  ' + D + '"firstpass-done" >> "$SG_DBG"\n')
ins('  local out rc\n  _sg_relax_left || return 4\n', '  local out rc\n  _sg_relax_left || return 4\n  ' + D + '"relax-start" >> "$SG_DBG"\n')
ins('  rc=$?\n  [[ $rc -eq 77 ]] && return 0\n', '  rc=$?\n  ' + D + '"relax-joined" >> "$SG_DBG"\n  [[ $rc -eq 77 ]] && return 0\n')
with open(sys.argv[2], 'w', encoding='utf-8') as f: f.write(t)
print('ok')

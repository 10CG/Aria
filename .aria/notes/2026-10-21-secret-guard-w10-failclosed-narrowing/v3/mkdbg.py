#!/usr/bin/env python3
"""mkdbg.py <v3 hook> <out>: stage-timing instrumentation of the v3 prototype (SG_DBG=<file> receives "<EPOCHREALTIME> <stage>" lines).
Timing only: every probe keeps the status of the statement it follows."""
import sys
t = open(sys.argv[1], encoding='utf-8').read()
D = '[[ -n "${SG_DBG:-}" ]] && printf "%s %s\\n" "$EPOCHREALTIME" '
def ins(old, label, after=True):
    global t
    assert t.count(old) == 1, (old[:60], t.count(old))
    t = t.replace(old, (old + D + f'"{label}" >> "$SG_DBG"\n') if after else (D + f'"{label}" >> "$SG_DBG"\n' + old))
ins('_SG_P0=${EPOCHREALTIME:-}   # #217: hook-start anchor of the relaxed rerun\'s hard deadline (empty under a bash without EPOCHREALTIME: no relaxation)\n', 'P0')
ins('  _sg_core_eval "$cmd"\n  rc=$?\n', 'firstpass-done')
ins('    _sg_vx_pass "$cmd" "$_SG_MODE"\n    rc=$?\n', 'vxpass-done')
ins('_sg_relax_run() {   # CMD: status 0 = allowed, 2 = blocked (the job\'s text is on stderr), 4 = fall back to the baseline block\n  local out rc\n  _sg_relax_left || return 4\n', 'relax-start')
old = '  _SG_RELAXED=1\n  _sg_vx_pass "$1" "$_SG_MODE"\n'
assert t.count(old) == 1
t = t.replace(old, '  _SG_RELAXED=1\n  _sg_vx_pass "$1" "$_SG_MODE"\n  local _dr=$?; ' + D + '"job-done" >> "$SG_DBG"; return $_dr\n')
open(sys.argv[2], 'w', encoding='utf-8').write(t)
print('ok')

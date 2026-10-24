#!/usr/bin/env bash
# demo78.sh HOOK : (M7) _sg_relax_job called where the shell is NOT a process-group leader (what a bash without working set -m would give);
#                  (M8) _sg_vx_pass under _SG_RELAXED with an exhausted time budget: status and stderr.
H=$1
source "$H" </dev/null >/dev/null 2>&1
set +e
# --- M7: foreground subshell is not a group leader
_sg_vx_pass() { return 0; }
_SG_MODE=whole; _SG_LEFT=1.0
( _sg_relax_job "cmd" ) >/dev/null 2>&1; echo "M7: _sg_relax_job outside a group-leader shell -> status $? (good: 9 = refuses to judge; mutant: 77 = allows with a timer aimed at a group that does not exist)"
# --- M8: relaxed vx_pass with budget 0 (first checkpoint)
source "$H" </dev/null >/dev/null 2>&1; set +e
unset CLAUDE_PROJECT_DIR; input=''
for m in whole segment; do
  r=$( export SECRET_GUARD_TIME_BUDGET_S=0; _SG_RELAXED=1
       cmd='v=Q; w=R; : $v $w'
       _sg_core_eval "$cmd" >/dev/null 2>&1; mode=$_SG_MODE
       [[ $m == segment ]] && { _SG_MODE=segment; _SG_SEGS=('v=Q' 'w=R' ': $v $w'); mode=segment; } || { _SG_MODE=whole; mode=whole; }
       err=$(_sg_vx_pass "$cmd" "$mode" 2>&1 >/dev/null); st=$?
       printf 'status=%s stderr_bytes=%s first=%s' "$st" "${#err}" "$(printf '%s' "$err" | head -1 | cut -c1-60)" )
  echo "M8 ($m mode, rerun flag set, budget 0): $r   (good: status 3 and no text; mutant: status 2 with the time text)"
done

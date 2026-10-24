#!/usr/bin/env bash
# demo3.sh HOOK SHAPE-FILE [stub]: deterministic check of the fallback bytes in SEGMENT mode: with _sg_relax_run stubbed to "fall back" (status 4), the stderr of
# _sg_per_segment_eval must equal the baseline's stderr for the same command (P6). No timing involved.
H=$1; CMDF=$2
source "$H" </dev/null >/dev/null 2>&1
set +e
unset CLAUDE_PROJECT_DIR; input=''; command=$(cat "$CMDF")
[[ "${3:-}" == stub ]] && _sg_relax_run() { return 4; }
_SG_P0=$EPOCHREALTIME
( _sg_per_segment_eval "$command" ) 2> "$4"; echo "rc=$? mode=$(grep -c 'a command segment is longer' "$4") seg-wording / $(grep -c 'the command is longer' "$4") whole-wording"

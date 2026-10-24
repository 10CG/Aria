#!/usr/bin/env bash
# mimic.sh STATE_DIR MODE(m|nom) : the shape of _sg_relax_run -- a command substitution with set -m starts a background job; the job writes a text whose
# command echo goes through `printf | sed` in a command substitution (as _sg_redact_echo does). MODE nom: the same without set -m (no job group).
V=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31
export SC_SHIM_STATE=$1 SC_DELAY_sed=0.3 SC_REAL_sed=$(command -v sed) PATH=$V/shim:$PATH
f() { printf '%s' "$1" | LC_ALL=C sed -e 's/a/b/'; }
job() { local x; x=$(f "aaa"); echo "text $x" >&2; return 2; }
t0=$EPOCHREALTIME
if [[ $2 == m ]]; then out="$( exec 2>/dev/null; set -m; job 2>&1 </dev/null & jp=$!; wait "$jp"; exit $? )"
else out="$( exec 2>/dev/null; job 2>&1 </dev/null & jp=$!; wait "$jp"; exit $? )"; fi
echo "status=$? out=[$out] wall=$(awk -v a=$t0 -v b=$EPOCHREALTIME 'BEGIN{printf "%.2f", b-a}')"
f "main-a" >/dev/null; echo "state after a call in the main process: [$(ls "$1" | tr '\n' ' ')]"

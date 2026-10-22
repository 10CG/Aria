#!/usr/bin/env bash
# matrix.sh <hook> <cmdfile>... : one e2e call per file (bash 5.2), prints rc, wall, template kind. Extension project via EXTDIR=<dir> (sets CLAUDE_PROJECT_DIR).
H=$1; shift
for F in "$@"; do
  J=$(jq -Rs '{tool_name:"Bash", tool_input:{command:.}}' < "$F")
  E=$(mktemp)
  t0=$EPOCHREALTIME
  if [[ -n "${EXTDIR:-}" ]]; then
    printf '%s' "$J" | CLAUDE_PROJECT_DIR="$EXTDIR" timeout 60 bash "$H" >/dev/null 2>"$E"; rc=$?
  else
    printf '%s' "$J" | env -u CLAUDE_PROJECT_DIR timeout 60 bash "$H" >/dev/null 2>"$E"; rc=$?
  fi
  t1=$EPOCHREALTIME
  kind=-
  if (( rc == 2 )); then
    if grep -q 'has a line longer than' "$E"; then kind=longline
    elif grep -q 'grows by more than' "$E"; then kind=growth
    elif grep -q 'project extension' "$E"; then kind=ext-oversize
    elif grep -q 'too large to scan' "$E"; then kind="oversize($(grep -o 'Limit hit: [a-z ]*' "$E" | cut -c12-40))"
    elif grep -q 'within the time budget' "$E"; then kind=time
    elif grep -q '(extension)' "$E"; then kind=ext-finding
    elif grep -q 'reads a secret-bearing source' "$E"; then kind=finding
    else kind=other; fi
  fi
  (( rc == 124 )) && kind=KILLED60
  printf '%-22s rc=%-3s wall=%6.2fs %s\n' "$(basename "$F" .txt)" "$rc" "$(awk -v a=${t0/,/.} -v b=${t1/,/.} 'BEGIN{print b-a}')" "$kind"
  rm -f "$E"
done

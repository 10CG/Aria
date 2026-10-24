#!/usr/bin/env bash
# which mode (whole / segment / none) does _sg_core_eval leave for a command? (source the hook up to its gate, call the function)
D=$(cd "$(dirname "$0")" && pwd)
X4000=$(printf '%*s' 4000 '' | tr ' ' x); FILL=$(printf ' y%.0s' $(seq 1 2100))
seg="x=${X4000}; : \$x \$x${FILL}; cat /srv/billing/conf/prod.toml"
tm="x=${X4000}; y=$(printf '%*s' 196 '' | tr ' ' y)$(for i in 1 2 3 4 5 6 7 8; do printf '; : $x $x $y'; done)"
for name in seg tm; do
  cmd=${!name}
  m=$(bash -c 'source "$1" </dev/null >/dev/null 2>&1; set +e; unset CLAUDE_PROJECT_DIR; input=""; _sg_core_eval "$2" >/dev/null 2>&1; echo "$_SG_MODE segs=${#_SG_SEGS[@]}"' _ "$D/v31.sh" "$cmd")
  echo "$name: ${#cmd} chars -> mode/segments: $m"
done

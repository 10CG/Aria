#!/usr/bin/env bash
# Main-loop review: does the BUILT-IN judgement (below the gate, i.e. short commands) let a token through when its right boundary
# is a separator/quote with no blank? Pre-existing behaviour check on any hook. Strings assembled at runtime.
#   bash rbound.sh <hook>
H="$1"
F="forg""ejo"; T="/users/bot/tok""ens"; K="~/.s""sh/id_new"; N="nomad var p""ut"
run() { local rc; jq -nc --arg c "$1" '{tool_name:"Bash",tool_input:{command:$c}}' | env -u SECRET_GUARD_RAW_GATE "$H" >/dev/null 2>&1; rc=$?; printf 'rc=%s  %s\n' "$rc" "$2"; }
run "$F POST $T" "PAT: bare"
run "$F POST $T | cat" "PAT: | cat (blank)"
run "$F POST $T|cat" "PAT: |cat (no blank)"
run "$F POST \"$T\"" "PAT: double-quoted path"
run "$F POST '$T'" "PAT: single-quoted path"
run "$F POST \"/users/\$U/tok\"\"ens\"" "PAT: \$U in quotes (split quote)"
run "($F POST $T)" "PAT: in ( )"
run "echo \`$F POST $T\`" "PAT: in back quotes"
run "x=\$($F POST $T)" "PAT: in \$( )"
run "$F POST $T>/tmp/o" "PAT: >file (no blank)"
run "$F POST $T&" "PAT: & (no blank)"
run "cp /tmp/x $K" "cp key: bare"
run "cp /tmp/x \"$K\"" "cp key: quoted"
run "cp /tmp/x $K|cat" "cp key: |cat"
run "$N" "nomad var put: bare"
run "$N|cat" "nomad var put: |cat"

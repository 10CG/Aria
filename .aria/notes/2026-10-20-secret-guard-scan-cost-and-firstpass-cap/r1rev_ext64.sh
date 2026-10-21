#!/usr/bin/env bash
# Main-loop review: W9 extension, first-64-hits cap. A project lists a path; a read of it is blocked; is it still blocked when the
# command mentions the path 64 times first (harmless echo), then reads it? Pre-existing behaviour check on any hook.
#   bash ext64.sh <hook>
H="$1"; R="$(mktemp -d)"; trap 'rm -rf "$R"' EXIT
mkdir -p "$R/.aria"; P="/srv/app/conf/priv""ate-settings.ini"; printf '%s\n' "$P" > "$R/.aria/secret-guard.paths"
run() { local rc; jq -nc --arg c "$1" '{tool_name:"Bash",tool_input:{command:$c}}' | env -u SECRET_GUARD_RAW_GATE CLAUDE_PROJECT_DIR="$R" "$H" >/dev/null 2>&1; rc=$?; printf 'rc=%s bytes=%-5s %s\n' "$rc" "${#1}" "$2"; }
run "cat $P" "read alone"
d=""; for i in $(seq 1 63); do d="$d $P"; done
run "echo$d; cat $P" "63 mentions, then the read"
d="$d $P"
run "echo$d; cat $P" "64 mentions, then the read"

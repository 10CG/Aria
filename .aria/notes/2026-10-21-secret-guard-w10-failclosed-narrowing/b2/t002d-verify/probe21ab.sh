#!/usr/bin/env bash
# probe21ab.sh <hook> <out dir> : wall time of 21ab's two relaxed-branch commands that must pass, fed to the hook as wpa_err does (private HOME, no project)
set -u
H=$1; O=$2; mkdir -p "$O/home"
rep() { printf '%*s' "$2" '' | tr ' ' "$1"; }
fill() { [[ "$1" -ge 2 ]] && printf ' %s' "$(rep y $(( $1 - 1 )))"; return 0; }
b="f=x; echo \$f$(fill 9000)"; c="f=x; echo \$f$(rep a 4500 | sed 's/a/ a/g')"
jq -nc --arg c "$b" '{tool_name:"Bash",tool_input:{command:$c}}' > "$O/b.json"; jq -nc --arg c "$c" '{tool_name:"Bash",tool_input:{command:$c}}' > "$O/c.json"
run() {   # label input [VAR=VALUE]
  local t0 t1 rc; t0=$EPOCHREALTIME
  env -u CLAUDE_PROJECT_DIR -u SECRET_GUARD_ACK_PATH -u SECRET_GUARD_ACK_NONCE -u WSL_DISTRO_NAME -u WSL_INTEROP HOME="$O/home" ${3:+"$3"} \
    taskset -c 0,1 nice -n 19 bash "$H" < "$O/$2.json" > /dev/null 2> "$O/err"; rc=$?; t1=$EPOCHREALTIME
  printf '%s rc=%s wall=%s size-text=%s load=%s\n' "$1" "$rc" "$(awk -v a="$t0" -v b="$t1" 'BEGIN{printf "%.2f", b-a}')" \
    "$(grep -q 'too large to scan' "$O/err" && echo yes || echo no)" "$(cut -d' ' -f1 /proc/loadavg)"
}
for i in 1 2 3; do run "b#$i" b; run "c#$i" c; done
run "b gate-closed" b WSL_DISTRO_NAME=Ubuntu; run "c gate-closed" c WSL_DISTRO_NAME=Ubuntu

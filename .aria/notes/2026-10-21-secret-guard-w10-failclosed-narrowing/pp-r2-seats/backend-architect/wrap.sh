#!/usr/bin/env bash
# wrap.sh HOOK JSON ERRFILE RCFILE : runs the hook with stdin from a file, stdout /dev/null, stderr to a file -- inside `script` there is a CONTROLLING TTY
t0=$EPOCHREALTIME
bash "$1" < "$2" > /dev/null 2> "$3"; rc=$?
t1=$EPOCHREALTIME
printf 'rc=%s wall=%s tty_ctl=%s\n' "$rc" "$(awk -v a="${t0/,/.}" -v b="${t1/,/.}" 'BEGIN{printf "%.2f", b-a}')" "$( (: < /dev/tty) 2>/dev/null && echo yes || echo no)" > "$4"

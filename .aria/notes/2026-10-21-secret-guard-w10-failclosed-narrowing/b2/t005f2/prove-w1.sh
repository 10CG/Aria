#!/bin/bash
# prove-w1.sh : every test-side WSL-mark function (extracted from its file) against the hook's _sg_relax_nowslfs (in its own subshell), on 5f's W1a-d
# fake tables and directory, three extra cases, one informational case (a directory as the table), and the real paths. "has" = test status 0 = hook status 1
S=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad; W=$S/wt217/aria; V=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31
H=$W/hooks/secret-guard.sh; X=$(mktemp -d "$S/r217impl/t005f2/w1x.XXXXXX")
w1d="$X/w1-binfmt"; mkdir -p "$w1d" "$X/elsewhere" "$X/w1-dir"
printf 'systemd-1 %s autofs rw,relatime,fd=29,pgrp=1,timeout=0,minproto=5,maxproto=5,direct 0 0\nproc /proc proc rw,nosuid,nodev,noexec,relatime 0 0\n' "$w1d" > "$X/w1-autofs"
printf 'binfmt_misc %s binfmt_misc rw,nosuid,nodev,noexec,relatime 0 0\nproc /proc proc rw,nosuid,nodev,noexec,relatime 0 0\n' "$w1d" > "$X/w1-mounted"
: > "$X/w1-empty"; printf 'binfmt_misc %s binfmt_misc rw 0 0\n' "$X/elsewhere" > "$X/w1-elsewhere"
ext() { sed -n "/^$2() {/,/^}/p" "$1" | sed "1s/^$2()/$3()/"; }
eval "$(ext $W/hooks/tests/lib/secret-guard-w10-direct.sh wslmark f_helper)"; eval "$(ext $V/sc-direct.sh wslmark f_scdirect)"
eval "$(ext $W/hooks/tests/secret-guard.test.sh sg_w10_wslfs f_suite)"; eval "$(ext $V/sc-cases.sh wslmark f_sccases)"
for f in f_helper f_scdirect f_suite f_sccases; do declare -F $f > /dev/null || { echo "EXTRACT FAIL $f"; exit 3; }; done
hk() { ( source "$H" < /dev/null > /dev/null 2>&1; _sg_relax_nowslfs "$@" 2>"$X/hk.err"; echo $? ) ; }
yn() { [[ $1 == "$2" ]] && echo has || echo none; }
n=0; ok=0
row() {   # label mounts entry
  local h r f s e line
  rm -f "$w1d"/*; : > "$w1d/$3"
  h=$(hk "$2" "$w1d"); line="$1 hook=$h($(yn "$h" 1))"; r=ok
  for f in f_helper f_scdirect f_suite f_sccases; do s=$($f "$2" "$w1d" 2>"$X/tf.err"; echo $?); e=$(wc -c < "$X/tf.err")
    line+=" $f=$s($(yn "$s" 0))"; [[ $(yn "$s" 0) == "$(yn "$h" 1)" && $e == 0 && ( $s == 0 || $s == 1 ) ]] || r=MISMATCH; done
  [[ $1 == info* ]] || { n=$((n+1)); [[ $r == ok ]] && ok=$((ok+1)); }
  echo "$r $line"
}
row W1a-autofs "$X/w1-autofs" WSLInterop; row W1b-late "$X/w1-mounted" WSLInterop-late; row W1c-noentry "$X/w1-mounted" status; row W1d-unreadable "$X/w1-none/mounts" WSLInterop
row x1-mounted-exact "$X/w1-mounted" WSLInterop; row x2-empty-table "$X/w1-empty" WSLInterop; row x3-mounted-elsewhere "$X/w1-elsewhere" WSLInterop
row info-dir-as-table "$X/w1-dir" WSLInterop
echo "SUMMARY bash ${BASH_VERSION}: $ok/$n agree (W1a-d + 3 extra)"
h=$(hk); old=none; timeout 5 bash -c '[[ -e /proc/sys/fs/binfmt_misc/WSLInterop ]]' && old=has
echo "REAL PATHS: hook=$h($(yn "$h" 1)) old -e check=$old helper=$(f_helper; echo $?) scdirect=$(f_scdirect; echo $?) suite=$(f_suite; echo $?) sccases=$(f_sccases; echo $?) (test status 1 = none)"
rm -rf "$X"

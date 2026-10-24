#!/usr/bin/env bash
# xp-fo.sh <mutant ids...> : consequence demos of the survivors that are fail-open candidates. Each shape is built at run time (the credential-shaped path is assembled from pieces);
# the hook only judges text. Output: per hook rc, wall, text kind. baseline = aria 59e333c, good = the v3.1 prototype.
D=$(cd "$(dirname "$0")" && pwd); W=$(mktemp -d); trap 'rm -rf "$W"' EXIT
git -C /home/dev/Aria/aria show 59e333c:hooks/secret-guard.sh > "$W/base.sh"
APPINI="/etc/forg""ejo/app"".ini"
X4000=$(printf '%*s' 4000 '' | tr ' ' x); FILL=$(printf ' y%.0s' $(seq 1 2100)); V5000=$(printf '%*s' 5000 '' | tr ' ' v); PAD=$(printf '%*s' 9000 '')
# M24: the 17th assignment is over VMAX, the 18th names the credential file; the baseline pass collects 16, the rerun collects all
c24="x=${X4000}"; for i in $(seq -w 2 16); do c24="$c24; b$i=1"; done; c24="$c24; big=${V5000}; F=${APPINI}; : \$x \$x${FILL}; cat \$F"
# M17: segment mode, one segment grows by more than 8192 and holds the read
c17="x=${X4000}; F=${APPINI}; cat \$F \$x \$x \$x \$x"
# M18: whole mode (parenthesis), the whole command grows by more than 8192 and holds the read
c18="(true); x=${X4000}; F=${APPINI}; cat \$F \$x \$x \$x \$x"
# M28: whole mode, a read with a value-redacting filter, one line padded with blanks to over 8192 characters
c28="(true); F=${APPINI}; cat \$F | wc -c${PAD}"
c28c="(true); F=${APPINI}; cat \$F | wc -c$(printf '%*s' 9000 '' | tr ' ' z)"
kind() { if grep -q 'has a line longer than' "$1"; then echo longline; elif grep -q 'grows by more than' "$1"; then echo growth; elif grep -q 'variable value is longer' "$1"; then echo vmax;
  elif grep -q 'too large to scan' "$1"; then echo oversize; elif grep -q 'value-REDACTING filter' "$1"; then echo finding; elif [[ -s "$1" ]]; then echo other; else echo none; fi; }
one() { local name=$1 h=$2 cmd=$3 t0 t1 rc; printf '%s' "$cmd" | jq -Rs '{tool_name:"Bash", tool_input:{command:.}}' > "$W/in.json"
  t0=$EPOCHREALTIME; env -u CLAUDE_PROJECT_DIR taskset -c 0,1 nice -n 19 timeout 12 bash "$h" < "$W/in.json" >/dev/null 2>"$W/err"; rc=$?; t1=$EPOCHREALTIME
  printf '  %-9s rc=%s %s wall=%ss\n' "$name" "$rc" "$(kind "$W/err")" "$(awk -v a="${t0/,/.}" -v b="${t1/,/.}" 'BEGIN{printf "%.2f", b-a}')"; }
for m in "$@"; do case $m in
  M24) cmd=$c24 ;; M17) cmd=$c17 ;; M18) cmd=$c18 ;; M28) cmd=$c28 ;; M28c) cmd=$c28c; m=M28 ;; *) continue ;; esac
  echo "== $m  (load $(cut -d' ' -f1 /proc/loadavg))"; one baseline "$W/base.sh" "$cmd"; one good "$D/v31.sh" "$cmd"; one "$m" "$D/mut/$m.sh" "$cmd"
done

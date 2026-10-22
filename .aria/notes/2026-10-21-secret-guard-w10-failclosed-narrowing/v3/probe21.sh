#!/usr/bin/env bash
# Runs the 21ab/21ac/21al/21ao command shapes of the suite against a hook; prints exit, template head, wall time. Paths are assembled at runtime.
HOOK=$1
wpa_AI="/etc/$(printf 'forg%s' ejo)/app.$(printf 'in%s' i)"
wpa_rep() { printf '%*s' "$2" '' | tr ' ' "$1"; }
wpa_vx_pad="$(wpa_rep x 4000)"
wpa_vx_fill() { [[ "$1" -ge 2 ]] && printf ' %s' "$(wpa_rep y $(( $1 - 1 )))"; return 0; }
wpa_vx_cmd() { printf 'f=%s; p=%s; echo $p $p%s | cat $f' "$wpa_AI" "$wpa_vx_pad" "$(wpa_vx_fill "$1")"; }
wpa_vx_val() { printf '/%s%s' "$(wpa_rep d $(( $1 - 21 )))" "$wpa_AI"; }
run() {
  local name=$1 cmd=$2 in t0 t1 err rc kind
  in="$(jq -n --arg c "$cmd" '{tool_name: "Bash", tool_input: {command: $c}}')"
  t0=$EPOCHREALTIME
  err="$(printf '%s' "$in" | bash "$HOOK" 2>&1 >/dev/null)"; rc=$?
  t1=$EPOCHREALTIME
  case "$err" in
    *"has a line longer than"*) kind=longline ;;
    *"grows by more than"*) kind=growth ;;
    *"too large to scan"*) kind="oversize:$(grep -o 'Limit hit: .*' <<<"$err" | cut -c12-60)" ;;
    *"within the time budget"*) kind=time ;;
    *"reads a secret-bearing source"*) kind=finding ;;
    "") kind=- ;;
    *) kind=other ;;
  esac
  printf '%-8s rc=%s %-62s %5.2fs len=%s\n' "$name" "$rc" "$kind" "$(awk -v a=${t0/,/.} -v b=${t1/,/.} 'BEGIN{print b-a}')" "${#cmd}"
}
run 21ab#1 "$(wpa_vx_cmd 159)"
run 21ab#2 "f=x; echo \$f$(wpa_vx_fill 9000)"
run 21ab#3 "f=x; echo \$f$(wpa_rep a 4500 | sed 's/a/ a/g')"
run 21ac#3 "for f in $(wpa_vx_val 4096); do cat \"\$f\"; done"
run 21al#2 "( f=$wpa_AI; p=$wpa_vx_pad; echo \${p} \${p}$(wpa_vx_fill 159) | cat \${f} )"

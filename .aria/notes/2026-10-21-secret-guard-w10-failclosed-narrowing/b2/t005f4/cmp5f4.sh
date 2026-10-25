H=$1; P=$2; TW=$3; D=$P/fx; cd "$P" || exit 3
source "$H" </dev/null >/dev/null 2>&1; set +e +u
for f in "$TW"/tw-*.sh; do source "$f"; done
n=0; bad=0
c() {   # NAME WANT OPT [MOUNTS DIR] : the hook's function and the four test-side criteria under OPT ('-' = none); a test side must say the opposite
  local nm=$1 w=$2 o=$3 hs e k ts r='' st=ok; shift 3
  hs=$( [[ $o == - ]] || eval "$o"; _sg_relax_nowslfs "$@" 2>"$TW/err"; echo $? ); e=$(wc -c < "$TW/err")
  [[ $hs == "$w" && $e == 0 ]] || st=WANT-MISMATCH
  for k in helper scdirect suite sccases; do
    ts=$( [[ $o == - ]] || eval "$o"; tw_$k "$@" 2>/dev/null; echo $? ); r+=" $k=$ts"
    [[ $ts == $(( 1 - hs )) ]] || st=MISMATCH
  done
  n=$((n + 1)); [[ $st == ok ]] || bad=$((bad + 1))
  printf '%-20s hook=%s (want %s) stderr=%s |%s  %s\n' "$nm" "$hs" "$w" "$e" "$r" "$st"
}
c host 0 -
c autofs+WSLInterop 0 - t-autofs "$D/wsl"
c binfmt+late 1 - t-late "$D/late"
c binfmt+none 0 - t-none "$D/none"
c stacked+WSLInterop 0 - t-stacked "$D/wsl"
c empty 1 - t-empty "$D/wsl"
c unreadable 1 - /nonexistent/x "$D/wsl"
c dir-as-table 1 - "$D" "$D/wsl"
c noglob+late 1 'set -f' t-late "$D/late"
c failglob+none 0 'shopt -s failglob' t-none "$D/none"
c nosearch-000 1 - t-nosearch "$D/nosearch"
c listless-0311+late 1 - t-listless "$D/listless"
c xfile-0755 1 - t-xfile "$D/xfile"
echo "# ${BASH_VERSION%%(*}: $n cases, $bad not ok"

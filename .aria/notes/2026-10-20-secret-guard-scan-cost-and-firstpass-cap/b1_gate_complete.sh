#!/usr/bin/env bash
# b1_gate_complete.sh HOOK : whole-string vs per-segment detection on separator variants of a credential read
# (does matching risky_patterns on the RAW command -- what a pre-scan gate does -- miss a read in a later segment?)
# The credential path is assembled at run time; prints only form numbers and pattern indexes.
source "$1"; eval "$(sed -n '/^declare -a risky_patterns=(/,/^)/p' "$1")"
P="~/"".aw""s/cre""dentials"; C="cat $P"
hit() { local s="$1" i=0 pat; for pat in "${risky_patterns[@]}"; do [[ "$s" =~ $pat ]] && { echo "$i"; return; }; i=$((i+1)); done; echo "-"; }
forms=( "$C;echo x" "echo x;$C" "echo x&&$C" "echo x||$C|cat" "($C)" "echo \$($C)" "$C&" "echo x;$C;echo y" "echo x | $C" "echo x;  $C  ;echo y" "x=1;$C>/tmp/o" )
n=0; for f in "${forms[@]}"; do
  n=$((n+1)); w=$(hit "$f")
  _sg_split_top "$f"; segs=""; for s in "${_SG_SEGS[@]}"; do segs+="$(hit "$s"),"; done
  printf 'form%-2d whole_hit=%-3s per_segment_hits=[%s]\n' "$n" "$w" "${segs%,}"
done

#!/usr/bin/env bash
# xp-newcases.sh : the direct-call cases I propose, run on the good prototype and on the mutants they are meant to catch. Deterministic (no wall-clock windows).
# Each probe prints "rc/kind" per hook. A probe is useful when the mutant column differs from the good column. Hook source gate: only the functions above it exist, so
# risky_patterns / _sg_judge_one / _sg_redact_echo are extracted by anchor, as sc-direct.sh does. No credential values anywhere (the config path is assembled from pieces).
D=$(cd "$(dirname "$0")" && pwd)
APPINI="/etc/forg""ejo/app"".ini"
export APPINI
probe() {   # $1 hook  $2 snippet : runs the snippet in a fresh bash that has sourced the hook; prints rc/kind
  bash -c '
    H=$1; snippet=$2; source "$H" </dev/null >/dev/null 2>&1; set +e; unset CLAUDE_PROJECT_DIR; input=""; command="probe"
    X=$(mktemp -d); trap "rm -rf $X" EXIT
    awk "/^declare -a risky_patterns=\\(/,/^\\)\$/" "$H" > $X/rp.sh; awk "/^_sg_judge_one\\(\\) \\{/,/^\\}\$/" "$H" > $X/jo.sh; awk "/^_sg_redact_echo\\(\\) \\{/,/^\\}\$/" "$H" > $X/re.sh
    source $X/rp.sh; source $X/jo.sh; source $X/re.sh
    kind() { if grep -q "has a line longer than" "$1"; then echo longline; elif grep -q "grows by more than" "$1"; then echo growth; elif grep -q "variable value is longer" "$1"; then echo vmax;
      elif grep -q "within the time budget" "$1"; then echo time; elif grep -q "too large to scan" "$1"; then echo oversize; elif grep -q "value-REDACTING filter" "$1"; then echo finding; elif [[ -s "$1" ]]; then echo other; else echo none; fi; }
    E=$X/err
    eval "$snippet"
  ' _ "$1" "$2" 2>&1 | tail -1
}
x4=$(printf '%*s' 4000 '' | tr ' ' x); fill=$(printf ' y%.0s' $(seq 1 2100)); v5=$(printf '%*s' 5000 '' | tr ' ' v)
ext=$(mktemp -d); mkdir -p "$ext/.aria"; printf '%s\n' "billing/conf/prod.toml" > "$ext/.aria/secret-guard.paths"
R='_SG_RELAXED=1; export SECRET_GUARD_TIME_BUDGET_S=0'
declare -A P   # name -> snippet (stdout of the snippet is discarded; the last line printed is rc/kind)
P[T1-collect-checkpoint-in-rerun]="$R; _sg_vx_pass 'a=1; b=2; : \$a \$b' whole 2>\$E; r=\$?; echo \"\$r/\$(kind \$E)\""
P[T2-whole-checkpoint-in-rerun]="$R; _sg_vx_pass 'a=1; : \$a' whole 2>\$E; r=\$?; echo \"\$r/\$(kind \$E)\""
P[T3-segment-checkpoint-in-rerun]="$R; _SG_SEGS=('a=1' ': \$a'); _sg_vx_pass 'a=1; : \$a' segment 2>\$E; r=\$?; echo \"\$r/\$(kind \$E)\""
P[T0-checkpoint-baseline-pass-control]="_SG_RELAXED=; export SECRET_GUARD_TIME_BUDGET_S=0; _sg_vx_pass 'a=1; : \$a' whole 2>\$E; r=\$?; echo \"\$r/\$(kind \$E)\""
P[G1-extension-via-stdin-cwd]="input='{\"tool_name\":\"Bash\",\"cwd\":\"$ext\"}'; _SG_P0=\$EPOCHREALTIME; _sg_relax_ok; echo \"\$?/gate\""
P[G2-segment-site-asks-gate]="_sg_relax_platform() { return 1; }; _SG_P0=\$EPOCHREALTIME; _SG_SEGS=('x=$x4' ': \$x \$x$fill'); _sg_vx_pass 'x=$x4; : \$x \$x$fill' segment 2>\$E; r=\$?; echo \"\$r/\$(kind \$E)\""
P[G3-whole-site-asks-gate]="_sg_relax_platform() { return 1; }; _SG_P0=\$EPOCHREALTIME; _sg_vx_pass '(true); x=$x4; : \$x \$x$fill' whole 2>\$E; r=\$?; echo \"\$r/\$(kind \$E)\""
P[G4-platform-from-build-facts-MACHTYPE]="MACHTYPE=x86_64-apple-darwin23.0.0; HOSTTYPE=aarch64; _SG_P0=\$EPOCHREALTIME; _sg_relax_ok; echo \"\$?/gate\""
P[V1-vmax-in-rerun-17th-assignment]="$(printf 'c="x=%s"; for i in $(seq -w 2 16); do c="$c; b$i=1"; done; c="$c; big=%s; F=%s; : \\$x \\$x%s; cat \\$F"' "$x4" "$v5" "$APPINI" "$fill")"
P[V1-vmax-in-rerun-17th-assignment]+="; _SG_RELAXED=1; _SG_SEGS=(); IFS=';' read -ra _p <<< \"\$c\"; for s in \"\${_p[@]}\"; do _SG_SEGS+=(\"\${s# }\"); done; _sg_vx_pass \"\$c\" segment 2>\$E; r=\$?; echo \"\$r/\$(kind \$E)\""
P[V2-growth-overrun-segment]="_SG_RELAXED=1; _SG_SEGS=('x=$x4' 'F=$APPINI' 'cat \$F \$x \$x \$x \$x'); _sg_vx_pass 'x=$x4; F=$APPINI; cat \$F \$x \$x \$x \$x' segment 2>\$E; r=\$?; echo \"\$r/\$(kind \$E)\""
P[V3-growth-overrun-whole]="_SG_RELAXED=1; _sg_vx_pass '(true); x=$x4; F=$APPINI; cat \$F \$x \$x \$x \$x' whole 2>\$E; r=\$?; echo \"\$r/\$(kind \$E)\""
pad=$(printf '%*s' 9000 '' )
P[L1-blank-padded-long-line-with-filter]="_sg_vx_big_judge \"cat $APPINI | wc -c$pad\" whole 2>\$E; r=\$?; echo \"\$r/\$(kind \$E)\""
l8192=$(printf 'cat %s ' "$APPINI"); l8192="$l8192$(printf '%*s' $((8192 - ${#l8192})) '' | tr ' ' z)"; l8193="${l8192}z"
P[L2-edge-8192-is-normal]="_sg_vx_big_judge \"$l8192\" whole 2>\$E; r=\$?; echo \"\$r/\$(kind \$E)\""
P[L3-edge-8193-is-rows-only]="_sg_vx_big_judge \"$l8193\" whole 2>\$E; r=\$?; echo \"\$r/\$(kind \$E)\""
seg3="cat \$F | wc -c \$x \$x$(printf ' y%.0s' $(seq 1 100))"
P[S1-segment-fallback-pattern]="_SG_RELAXED=; _SG_P0=\$EPOCHREALTIME; _SG_SEGS=('x=$x4' ': \$x \$x$fill'); _sg_vx_pass 'x=$x4; : \$x \$x$fill' segment 2>\$E; r=\$?; echo \"\$r/\${_SG_OV_PAT:0:33}\""
P[S2-segment-big-copy-rows-only]="_SG_RELAXED=1; _SG_SEGS=('x=$x4' 'F=$APPINI' '$seg3'); _sg_vx_pass 'x=$x4; F=$APPINI; $seg3' segment 2>\$E; r=\$?; echo \"\$r/\$(kind \$E)\""
P[C1-ninth-for-statement-in-rerun]="_SG_RELAXED=1; c='echo \$x'; for i in 1 2 3 4 5 6 7 8 9; do c=\"\$c; for v\$i in w\$i; do :; done\"; done; _sg_vx_collect \"\$c\"; echo \"\${#_SGV_N[@]}/collected\""
declare -A WHO=( [T1-collect-checkpoint-in-rerun]="M08" [T2-whole-checkpoint-in-rerun]="M06" [T3-segment-checkpoint-in-rerun]="M07" [T0-checkpoint-baseline-pass-control]=""
  [G1-extension-via-stdin-cwd]="M01" [G2-segment-site-asks-gate]="M02" [G3-whole-site-asks-gate]="M03" [G4-platform-from-build-facts-MACHTYPE]="M04"
  [V1-vmax-in-rerun-17th-assignment]="M24" [V2-growth-overrun-segment]="M17" [V3-growth-overrun-whole]="M18" [L1-blank-padded-long-line-with-filter]="M28"
  [L2-edge-8192-is-normal]="M13 M29" [S1-segment-fallback-pattern]="M09" [S2-segment-big-copy-rows-only]="M10" [C1-ninth-for-statement-in-rerun]="M12" [L3-edge-8193-is-rows-only]="M13 M29" )
printf '%-42s %s\n' probe 'good(v3.1) | mutant(s) -> value'
for k in $(printf '%s\n' "${!P[@]}" | sort); do
  line=$(printf '%-42s good=%-16s' "$k" "$(probe "$D/v31.sh" "${P[$k]}")")
  for m in ${WHO[$k]}; do line="$line $m=$(probe "$D/mut/$m.sh" "${P[$k]}")"; done
  echo "$line"
done
rm -rf "$ext"

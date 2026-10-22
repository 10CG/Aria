#!/usr/bin/env bash
# ident32.sh <bash> <base hook> <v3 hook> <list of n>: rc + sha256(stderr) equality, hooks run by the given bash binary (aggregates only)
BASHBIN=$1; B=$2; V=$3; L=$4; T="${TRAFFIC_DIR:?}"; D="$(mktemp -d)"; trap 'rm -rf "$D"' EXIT
same=0; diff=0
while read -r n; do
  jq -Rs '{tool_name:"Bash",tool_input:{command:.}}' < "$T/cmds/$n.txt" > "$D/in.json"
  HOME="$D" timeout 120 env -u SECRET_GUARD_RAW_GATE -u CLAUDE_PROJECT_DIR "$BASHBIN" "$B" < "$D/in.json" >/dev/null 2>"$D/eb"; rb=$?
  HOME="$D" timeout 120 env -u SECRET_GUARD_RAW_GATE -u CLAUDE_PROJECT_DIR "$BASHBIN" "$V" < "$D/in.json" >/dev/null 2>"$D/ev"; rv=$?
  if [[ $rb == "$rv" && "$(sha256sum < "$D/eb")" == "$(sha256sum < "$D/ev")" ]]; then same=$((same+1)); else diff=$((diff+1)); echo "DIFF n=$n base_rc=$rb v3_rc=$rv"; fi
done < "$L"
echo "identical=$same different=$diff"

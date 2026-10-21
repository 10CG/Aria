#!/usr/bin/env bash
# Main-loop review: gate-only and whole-hook time on REALISTIC multi-line scripts (mixed commands, few pipes) with a credential-shaped
# read at the end, at several sizes. Gate-only = _sg_pregate in process (sourced hook + risky_patterns); hook = one real hook process.
#   bash realistic.sh <hook> <sizes...>
set -u
H="$1"; shift
D="$(mktemp -d)"; trap 'rm -rf "$D"' EXIT; export HOME="$D"
source "$H"
awk '/^declare -a risky_patterns=\(/,/^\)$/' "$H" > "$D/rp.sh"; source "$D/rp.sh"
unset SECRET_GUARD_RAW_GATE CLAUDE_PROJECT_DIR
TIMEFORMAT='%3R'
rd="cat /opt/.e""nv"
block='cd /home/dev/proj/app && git status --short
for f in $(ls src); do echo "== $f"; wc -l "src/$f"; done
grep -n "def handler" src/server.py | head -20
curl -s -H "Accept: application/json" https://example.com/api/v1/items | jq ".items[] | .name"
python3 -c "import json; d=json.load(open(\"build/out.json\")); print(len(d))"
sed -n "1,40p" README.md
if [[ -f build/stamp ]]; then echo built; else make -j4 build; fi
mkdir -p /tmp/work/out; cp -r assets /tmp/work/out/
find . -name "*.log" -mtime +7 -print
npm run lint --silent; npm test -- --runInBand
docker ps --format "{{.Names}}"; kubectl get pods -n default
awk -F, "{s+=\$3} END {print s}" data/report.csv
'
mk() { local n="$1" s="" i=0; while (( ${#s} < n )); do i=$((i+1)); s="$s# step $i
$block"; done; if [[ "${BENIGN:-}" == 1 ]]; then printf '%s' "$s"; else printf '%s' "$s
$rd"; fi; }
for n in "$@"; do
  command="$(mk "$n")"
  printf '%s' "$command" > "$D/cmd"
  tg=$( { time { _sg_pregate "$command" >/dev/null 2>&1; echo "$?" > "$D/rc"; }; } 2>&1 )
  th=-; echo - > "$D/hrc"; : > "$D/err"
  [[ "${BENIGN:-}" == 1 ]] || th=$( { time { jq -Rs '{tool_name:"Bash",tool_input:{command:.}}' < "$D/cmd" | timeout 60 env -u SECRET_GUARD_RAW_GATE "$H" >/dev/null 2>"$D/err"; echo "$?" > "$D/hrc"; }; } 2>&1 )
  printf 'realistic%s bytes=%-6s gate-only rc=%s %ss | hook rc=%s %ss %s\n' "${BENIGN:+-benign}" "$(LC_ALL=C; printf %s "${#command}")" "$(cat "$D/rc")" "$tg" "$(cat "$D/hrc")" "$th" "$(head -c 70 "$D/err" | tr '\n' ' ')"
done

#!/usr/bin/env bash
# xp-harness.sh : harness-level demos (no timing dependence). Inputs are built at run time; nothing credential-shaped is printed.
D=$(cd "$(dirname "$0")" && pwd); V=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31
W=$(mktemp -d); trap 'rm -rf "$W"' EXIT
git -C /home/dev/Aria/aria show 59e333c:hooks/secret-guard.sh > "$W/base.sh"
echo "== H1. SC_BASH points to a file that does not exist: does sc-cases.sh notice? =="
SC_BASH="$D/no-such-bash" SC_ONLY='V1-E16|V2-E9|V9-E12|V2-E8' bash "$V/sc-cases.sh" "$D/v31.sh" "$W/base.sh" 2>&1 | cut -c1-210 | tail -12; echo "exit=${PIPESTATUS[0]}"
echo "== H2. sc-direct.sh dies at once (stderr is discarded by sc-cases.sh): do the direct cases go missing silently? =="
cp -r "$V" "$W/v31copy"; printf '#!/usr/bin/env bash\necho boom >&2\nexit 1\n' > "$W/v31copy/sc-direct.sh"
SC_ONLY='V1-E16' bash "$W/v31copy/sc-cases.sh" "$D/v31.sh" "$W/base.sh" 2>&1 | cut -c1-160 | tail -4; echo "exit=${PIPESTATUS[0]}"
echo "== H3. V5-S12 / V5-S13b scan the whole process table by argument (ps -eo args): a foreign process with the same arguments counts =="
sleep 2.718 & dp=$!
n=$(ps -eo args | awk '$1=="sleep" && ($2=="10.111"||$2=="6.222"||$2=="10.333"||$2=="2.718"||$2=="7.777")' | wc -l)
kill "$dp" 2>/dev/null; wait "$dp" 2>/dev/null
echo "decoy sleep started by this script (pid $dp), V5-S12 pattern counted: $n (the case wants 0)"

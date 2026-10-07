#!/usr/bin/env bash
# iso_test.sh -- the per-row exception isolation of the probe (a hook call past its timeout is that ROW's failure, not the probe's crash), shown on a scratch copy:
#   * a tree whose secret-scan.sh sleeps 30 s when the envelope carries a marker text (row 35e feeds such texts), and a scratch copy of the probe whose hook-call timeout is 20 s instead of 300 s
#   * expected: row 35e is `no` with actual `error: TimeoutExpired`, the other rows of the run are untouched (`yes`), the probe exits 0; in acceptance mode (WPA_REQUIRE_ALL=1) it exits 4
# output: out/iso_test.txt
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v6
cd "$EXP" || exit 1
export HOME=$EXP/home TMPDIR=$EXP/tmp
W=$EXP/work/iso
rm -rf "$W" && mkdir -p "$W/aria" "$W/spec"
cp -a "$EXP/work/t6/aria/hooks" "$W/aria/hooks"
ln -s "$EXP/work/t6/standards" "$W/standards"
mv "$W/aria/hooks/secret-scan.sh" "$W/aria/hooks/secret-scan.real.sh"
cat > "$W/aria/hooks/secret-scan.sh" <<'EOF'
#!/usr/bin/env bash
in="$(cat)"
case "$in" in *"Exit code 1"*) sleep 30 ;; esac
printf '%s' "$in" | bash "$(dirname "$0")/secret-scan.real.sh"
EOF
sed -e 's/timeout=300)/timeout=20)/' "$EXP/spec/baseline_probe.py" > "$W/spec/baseline_probe.py"
cp "$EXP/spec/proposal.md" "$EXP/spec/baseline-evidence.md" "$W/spec/"
{
  echo "== normal mode (exit code must be 0): WPA_ONLY=SC-35 WPA_ROWS=35a,35b,35c,35d,35e"
  (cd "$W/spec" && WPA_ONLY=SC-35 WPA_ROWS=35a,35b,35c,35d,35e python3 baseline_probe.py "$W/aria" 2>&1 | grep -E '^SC-35 │ 35|^SC-35:|^target shape' | awk -F' │ ' '/^SC-35 │/ {print $1" "$2" | actual: "$(NF-1)" | match: "$NF; next} {print}'; echo "probe exit code: ${PIPESTATUS[0]}")
  echo "== acceptance mode (WPA_REQUIRE_ALL=1): exit code must be 4"
  (cd "$W/spec" && WPA_REQUIRE_ALL=1 WPA_ONLY=SC-35 WPA_ROWS=35a,35b,35c,35d,35e python3 baseline_probe.py "$W/aria" > /dev/null 2>&1; echo "probe exit code: $?")
} > out/iso_test.txt 2>&1
cat out/iso_test.txt

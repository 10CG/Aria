#!/usr/bin/env bash
# run-w10-w11.sh <aria hooks/secret-guard.sh at the baseline> <work dir> : builds base + v3 hooks, writes W10-mechanism.txt and W11-adversarial.txt next to this script
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; SRC=$1; W=$2; mkdir -p "$W/adv" "$W/ext/proj/.aria"
cp "$SRC" "$W/base.sh"; python3 "$HERE/mkv3.py" "$SRC" "$W/v3.sh" >/dev/null || exit 1
hdr() { printf '# %s | %s | bash %s | baseline sha256 %s | load %s\n' "$(date -u +%FT%TZ)" "$(uname -sr)" "$BASH_VERSION" "$(sha256sum < "$SRC" | cut -c1-12)" "$(cut -d' ' -f1-3 /proc/loadavg)"; }
{ hdr; echo "# v3unit.sh: relaxed rerun with a stubbed judgement, deadline 1 s"; taskset -c 0,1 nice -n 19 bash "$HERE/v3unit.sh" "$W/v3.sh" 2>&1 | grep -v setlocale | sed '/^orphans:/d'
  echo "# leftover stub processes (exact name match): $(ps -eo args | awk '$1=="sleep" && ($2=="10.111"||$2=="6.222"||$2=="10.333")' | wc -l)"; } > "$HERE/W10-mechanism.txt"
for s in apply-heavy apply-heavy-seg apply-heavy-cjk shrink segfinding f5like km-ext km-ext-small; do python3 "$HERE/gen-v3.py" $s "$W/adv/$s.txt" >/dev/null; done
printf '%s\n' "billing/conf/prod.toml" > "$W/ext/proj/.aria/secret-guard.paths"
L="apply-heavy apply-heavy-seg apply-heavy-cjk shrink segfinding f5like km-ext"
{ hdr; echo "# matrix.sh: one e2e call per input, bash 5, no project extension (CLAUDE_PROJECT_DIR unset)"
  for h in base v3; do echo "## $h"; ( cd "$W/adv" && taskset -c 0,1 nice -n 19 bash "$HERE/matrix.sh" "$W/$h.sh" $(for s in $L; do echo $s.txt; done) 2>&1 | grep -v setlocale ); done
  echo "# extension project (CLAUDE_PROJECT_DIR=<dir with .aria/secret-guard.paths listing the read path>)"
  for h in base v3; do echo "## $h"; ( cd "$W/adv" && EXTDIR="$W/ext/proj" taskset -c 0,1 nice -n 19 bash "$HERE/matrix.sh" "$W/$h.sh" km-ext.txt km-ext-small.txt 2>&1 | grep -v setlocale ); done
  echo "# suite shapes (probe21.sh)"
  for h in base v3; do echo "## $h"; taskset -c 0,1 nice -n 19 bash "$HERE/probe21.sh" "$W/$h.sh" 2>&1 | grep -v setlocale; done; } > "$HERE/W11-adversarial.txt"
echo done

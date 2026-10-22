#!/usr/bin/env bash
# w10b.sh <work dir with base.sh + v3.sh and adv/*.txt from run-w10-w11.sh>: two more properties of the prototype
#  P6  fallback text = baseline text, byte for byte (inputs on which v3 falls back; the same input is run on both hooks, stderr compared by sha256)
#  P10 the rows-only (nocredit) path keeps the W12 neutralisation: an os.environ single-key read on a long line is not blocked; a real read on a long line is
set -u
W=$1; HERE="$(cd "$(dirname "$0")" && pwd)"
printf '# %s | bash %s | load %s\n' "$(date -u +%FT%TZ)" "$BASH_VERSION" "$(cut -d' ' -f1-3 /proc/loadavg)"
echo "## P6 fallback = baseline (stderr sha256), inputs that fall back on v3 under the deadline"
for f in apply-heavy-cjk f5like; do
  J=$(jq -Rs '{tool_name:"Bash", tool_input:{command:.}}' < "$W/adv/$f.txt")
  for i in 1 2; do
    eb=$(printf '%s' "$J" | env -u CLAUDE_PROJECT_DIR taskset -c 0,1 nice -n 19 bash "$W/base.sh" 2>&1 >/dev/null | sha256sum | cut -c1-16)
    ev=$(printf '%s' "$J" | env -u CLAUDE_PROJECT_DIR taskset -c 0,1 nice -n 19 bash "$W/v3.sh" 2>&1 >/dev/null | sha256sum | cut -c1-16)
    printf '%-16s run %s base=%s v3=%s %s\n' "$f" "$i" "$eb" "$ev" "$([[ $eb == "$ev" ]] && echo IDENTICAL || echo DIFFERENT)"
  done
done
echo "## P10 rows-only path (direct call of _sg_judge_one ... nocredit on a single line of about 9000 characters)"
( source "$W/v3.sh" </dev/null >/dev/null 2>&1; set +e
  # risky_patterns, _sg_judge_one and _sg_redact_echo sit below the hook's source gate: extract them by anchor, as the suite's SC-8 harness does
  X=$(mktemp -d)
  awk '/^declare -a risky_patterns=\(/,/^\)$/' "$W/v3.sh" > "$X/rp.sh"
  awk '/^_sg_judge_one\(\) \{/,/^\}$/' "$W/v3.sh" > "$X/jo.sh"
  awk '/^_sg_redact_echo\(\) \{/,/^\}$/' "$W/v3.sh" > "$X/re.sh"
  [[ -s "$X/rp.sh" && -s "$X/jo.sh" && -s "$X/re.sh" ]] || { echo "SETUP FAILED: extraction came back empty"; exit 1; }
  source "$X/rp.sh"; source "$X/jo.sh"; source "$X/re.sh"; rm -rf "$X"
  echo "extracted: risky_patterns=${#risky_patterns[@]} rows, $(type -t _sg_judge_one) _sg_judge_one, $(type -t _sg_redact_echo) _sg_redact_echo"
  pad=$(printf '%*s' 9000 '' | tr ' ' 'z')
  env1="python3 -c 'import os; print(os.environ.get(\"HOME\"))' $pad"
  cfg="/etc/forg""ejo/app"".ini"
  rd="cat $cfg $pad"
  command="$env1"; _sg_judge_one "$env1" whole nocredit 2>/dev/null; echo "environ single-key read, long line, nocredit: rc=$? (want 0)"
  command="$rd"
  _sg_judge_one "$rd" whole nocredit 2>&1 >/dev/null | head -1 | cut -c1-80 | sed 's/^/  first line: /'
  _sg_judge_one "$rd" whole nocredit 2>/dev/null; echo "credential-path read, long line, nocredit: rc=$? (want 2)"
  _sg_judge_one "$rd" whole 2>/dev/null; echo "same read, normal path: rc=$? (want 2)" )

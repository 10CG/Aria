#!/usr/bin/env bash
# run_gitcopy_suite.sh <baseline|proto> [tree] [label]
# The two existing hook suites on a GIT COPY of the aria repository (history present, so the suite's SC-8 benchmark and SC-9a pre-change comparison reach their old reference commit):
#   baseline : the working tree at the baseline commit, untouched
#   proto    : the same working tree with the prototype's hooks / hooks.json / suites copied over (uncommitted, like an implementer's tree before the commit)
# Output: out/gitcopy_<label>_{guard,scan}.txt (suite stdout + stderr) and out/gitcopy_<label>.meta (load average before / after, bash version, sha256[:16] of the files that ran).
# The measurement is wall-clock inside the suite (EPOCHREALTIME): run it on an otherwise quiet host.
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v6
which=${1:?baseline|proto}
TREE=$(cd "${2:-$EXP/work/t6}" && pwd) || exit 1      # absolute: the script changes directory before it copies
label=${3:-$which}
G=$EXP/gitcopy
export HOME=$EXP/home TMPDIR=$EXP/tmp
mkdir -p "$HOME" "$TMPDIR" "$EXP/out"
if [ ! -d "$G/.git" ]; then
  git clone -q --no-hardlinks /home/dev/Aria/.git/modules/aria "$G" || exit 1
fi
cd "$G" || exit 1
git checkout -q -f 268da8f || exit 1
git clean -fdq
if [ "$which" = proto ]; then
  cp "$TREE/aria/hooks/secret-guard.sh" "$TREE/aria/hooks/secret-scan.sh" "$TREE/aria/hooks/hooks.json" hooks/
  cp "$TREE/aria/hooks/tests/secret-guard.test.sh" "$TREE/aria/hooks/tests/secret-scan.test.sh" hooks/tests/
fi
meta=$EXP/out/gitcopy_$label.meta
{
  echo "label=$label which=$which tree=${TREE#$EXP/} head=$(git rev-parse --short HEAD) bash=$BASH_VERSION kernel=$(uname -r) cores=$(nproc)"
  echo "files: guard=$(sha256sum hooks/secret-guard.sh | cut -c1-16) scan=$(sha256sum hooks/secret-scan.sh | cut -c1-16) hooks.json=$(sha256sum hooks/hooks.json | cut -c1-16)"
  echo "tests: guard=$(sha256sum hooks/tests/secret-guard.test.sh | cut -c1-16) scan=$(sha256sum hooks/tests/secret-scan.test.sh | cut -c1-16)"
  echo "git status: $(git status --short | tr '\n' ' ')"
  echo "load(start)=$(cut -d' ' -f1-3 /proc/loadavg) $(date +%T)"
} > "$meta"
bash hooks/tests/secret-guard.test.sh > "$EXP/out/gitcopy_${label}_guard.txt" 2>&1
echo "guard rc=$? load=$(cut -d' ' -f1-3 /proc/loadavg) $(date +%T)" >> "$meta"
bash hooks/tests/secret-scan.test.sh > "$EXP/out/gitcopy_${label}_scan.txt" 2>&1
echo "scan rc=$? load=$(cut -d' ' -f1-3 /proc/loadavg) $(date +%T)" >> "$meta"
echo "GITCOPY_DONE $label $(date +%T)" >> "$EXP/logs/gitcopy.log"

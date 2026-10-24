#!/usr/bin/env bash
# drive.sh (3e, 10CG/aria-plugin#217). Phase 0 on the 3c2 code (git HEAD df2d629 of the worktree, snapshot in old-aria/; the old run-suite.sh copied
# to run-suite-before.sh): C6 through a full round, then the old run-suite.sh's filtered checks. Then waits for <t002h>/ready (new suite and
# run-suite.sh in place, phase-2 predictions written) and runs phase 2 on the new code. One heavy run at a time; every suite run first waits for a
# one-minute load <= 1.2 (at most 30 minutes, then runs anyway, the reading logged). PIDs it starts: <t002h>/pids. Constructions: patched copies of
# the worktree hook in <t002h> (c1, c3, c5 from the 3c2 / verify-3c2 diffs) and the C6 wrapper around c3.
# bash drive.sh --wait <pattern> <seconds> [<lines>]: waits until drive.log has <pattern> (at most <seconds>), then prints its last lines.
set -u
S=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad
OUT=$S/r217impl/t002h; WT=$S/wt217/aria
N=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing; V=$N/v31
LOG=$OUT/drive.log; NO=$OUT/no-such-dir; H=$WT/hooks/secret-guard.sh
if [[ ${1:-} == --wait ]]; then
  t=0; until grep -q -- "$2" "$LOG" 2>/dev/null || (( t >= $3 )); do sleep 10; t=$((t + 10)); done
  echo "(waited ${t}s)"; tail -n "${4:-8}" "$LOG"; exit 0
fi
echo $$ >> "$OUT/pids"
ld() { cut -d' ' -f1-3 /proc/loadavg; }
log() { printf '%s %s | load %s\n' "$(date +%T)" "$*" "$(ld)" >> "$LOG"; }
waitlow() {
  local t=0 l
  while :; do
    l=$(cut -d' ' -f1 /proc/loadavg)
    if awk -v l="$l" 'BEGIN { exit !(l <= 1.2) }'; then log "waitlow ok at $l after ${t}s"; return 0; fi
    if (( t >= 1800 )); then log "waitlow GAVE UP at $l after ${t}s, runs anyway"; return 0; fi
    sleep 10; t=$((t + 10))
  done
  return 0
}
run1() {   # <out file> <command ...>: under taskset -c 0,1 nice -n 19, stdin /dev/null, PID recorded and waited for
  local o=$1 rc; shift
  taskset -c 0,1 nice -n 19 "$@" > "$o" 2>&1 < /dev/null &
  echo $! >> "$OUT/pids"; wait $!; rc=$?
  log "  -> ${o##*/} rc=$rc"
  return 0
}
x6() {   # <suite output> -> <same>.x6: header, totals, the six groups' line (verbatim), per-group verdict, their FAIL lines (commands cut, long tokens masked), last line
  local f=$1 g
  {
    head -n 1 "$f" | cut -c1-260
    grep -a -m1 '^PASS: ' "$f"; grep -a -m1 '^FAIL: ' "$f"
    grep -a 'W10 older groups' "$f"
    for g in 21ab 21ac 21ag 21aj 21al 21ao; do if grep -aq "FAIL \[W10 SC-$g" "$f"; then printf '%s FAIL  ' $g; else printf '%s pass  ' $g; fi; done; echo
    grep -a 'FAIL \[W10 SC-21a' "$f" | sed -E 's/\{Bash ([^:]{0,10})[^:]*:/{Bash \1…:/g; s/[A-Za-z0-9_+\/=-]{20,}/«masked»/g'
    tail -n 1 "$f"
  } > "$f.x6" 2>&1
  return 0
}
round() {   # <name> <hook> <aria> <run-suite>: one full round through run-suite.sh
  local n=$1 h=$2 a=$3 rs=$4
  waitlow; log "$n start"
  run1 "$OUT/$n.txt" bash "$rs" "$a" "$h" "$OUT/work"
  x6 "$OUT/$n.txt"; log "$n end | $(tail -n 1 "$OUT/$n.txt" | cut -c1-100)"
  return 0
}
c6round() {   # <name> <aria> <run-suite>: a C6 round with a fresh marker directory, kept afterwards as c6-marks-<name>
  rm -rf "$OUT/c6-marks"; mkdir "$OUT/c6-marks"
  round "$1" "$OUT/c6-wrap.sh" "$2" "$3"
  mv "$OUT/c6-marks" "$OUT/c6-marks-$1"
  log "  $1 marks: $(find "$OUT/c6-marks-$1" -mindepth 1 -maxdepth 1 -type d | wc -l) inputs stalled, $(find "$OUT/c6-marks-$1" -name 'in.*' | wc -l) gate-closed calls"
  return 0
}
norm() { sed -E 's/[0-9]+\.[0-9]+s/#s/g; s/load( [0-9]+\.[0-9]+)+/load #/g; s/[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:]+Z/#date/g' "$1"; }

log "begin | worktree $(git -C "$WT" rev-parse --short HEAD) status [$(git -C "$WT" status --short | tr '\n' ' ')]"
[[ -e $NO ]] && { log "$NO exists, stop"; exit 4; }
cp -p "$V/run-suite.sh" "$OUT/run-suite-before.sh"
mkdir -p "$OUT/old-aria" "$OUT/work" && git -C "$WT" archive HEAD hooks | tar -x -C "$OUT/old-aria" || { log "snapshot failed"; exit 4; }
log "snapshot: old suite $(sha256sum < "$OUT/old-aria/hooks/tests/secret-guard.test.sh" | cut -c1-12) | run-suite-before $(sha256sum < "$OUT/run-suite-before.sh" | cut -c1-12) | impl hook $(sha256sum < "$H" | cut -c1-12)"
for c in c1 c3 c5; do
  case $c in c1) d=$N/b2/t002f/c1-hook.diff ;; c3) d=$N/b2/t002f/c3-hook.diff ;; c5) d=$N/b2/t002f-verify/c5-hook.diff ;; esac
  patch -s -o "$OUT/$c-hook.sh" "$H" < "$d" || { log "patch $c failed"; exit 4; }
  chmod 755 "$OUT/$c-hook.sh"; log "$c hook $(sha256sum < "$OUT/$c-hook.sh" | cut -c1-12)"
done
log "c5 reference (t002f-verify/c5.txt): $(head -n 1 "$N/b2/t002f-verify/c5.txt" | grep -o 'hook [0-9a-f]*')"
sed "s|@OUT@|$OUT|g" > "$OUT/c6-wrap.sh" <<'EOF'
#!/usr/bin/env bash
# construction C6 (3e): C3 (the job returns 1 2.2 s after it starts) behind a stall of 1.5 s on the FIRST gate-closed run (WSL_DISTRO_NAME set) of
# each input, keyed by the sha256 of stdin in @OUT@/c6-marks (made anew for each round); later runs of the same input go straight to C3, under
# the same bash. Sourced (the direct-call helper), it sources C3 instead.
H=@OUT@/c3-hook.sh; M=@OUT@/c6-marks
if [[ "${BASH_SOURCE[0]}" != "$0" ]]; then . "$H"; return; fi
if [[ -n "${WSL_DISTRO_NAME+x}" ]]; then
  f=$(mktemp "$M/in.XXXXXX") || exit 98
  cat > "$f"
  k=$(sha256sum < "$f"); k=${k%% *}
  mkdir "$M/$k" 2>/dev/null && sleep 1.5
  exec "$BASH" "$H" "$@" < "$f"
fi
exec "$BASH" "$H" "$@"
EOF
chmod 755 "$OUT/c6-wrap.sh"; log "c6 wrapper $(sha256sum < "$OUT/c6-wrap.sh" | cut -c1-12)"

log "PHASE0 begin"
c6round c6-old "$OUT/old-aria" "$OUT/run-suite-before.sh"
waitlow; log "filt-before start"
run1 "$OUT/filt-before.txt" env SG_W10_ONLY='^V1-E16' SG_W10_LOG="$OUT/filt-before.log" bash "$OUT/run-suite-before.sh" "$OUT/old-aria" "$H" "$OUT/work"
waitlow; log "scbash-before start"
run1 "$OUT/scbash-before.txt" env SC_BASH="$NO/sub/bash" SG_W10_ONLY='^V1-E16' bash "$OUT/run-suite-before.sh" "$OUT/old-aria" "$H" "$OUT/work"
waitlow; log "log-before start"
run1 "$OUT/log-before.txt" env SG_W10_LOG="$NO/w10.log" SG_W10_ONLY='^V1-E16' bash "$OUT/run-suite-before.sh" "$OUT/old-aria" "$H" "$OUT/work"
log "  log-before: $NO exists? $([[ -e $NO ]] && echo yes || echo no)"
log "PHASE0 DONE"

t=0; until [[ -e "$OUT/ready" ]]; do sleep 10; t=$((t + 10)); (( t >= 5400 )) && { log "no ready after ${t}s, phase 2 not run"; exit 5; }; done
log "PHASE2 begin | worktree status [$(git -C "$WT" status --short | tr '\n' ' ')] | suite $(sha256sum < "$WT/hooks/tests/secret-guard.test.sh" | cut -c1-12) | run-suite $(sha256sum < "$V/run-suite.sh" | cut -c1-12)"
log "log-after start"
run1 "$OUT/log-after.txt" env SG_W10_LOG="$NO/w10.log" SG_W10_ONLY='^V1-E16' bash "$V/run-suite.sh" "$WT" "$H" "$OUT/work"
log "  log-after: $NO exists? $([[ -e $NO ]] && echo yes || echo no)"
waitlow; log "filt-after-old start"
run1 "$OUT/filt-after-old.txt" env SG_W10_ONLY='^V1-E16' SG_W10_LOG="$OUT/filt-after-old.log" bash "$V/run-suite.sh" "$OUT/old-aria" "$H" "$OUT/work"
waitlow; log "filt-after-new start"
run1 "$OUT/filt-after-new.txt" env SG_W10_ONLY='^V1-E16' SG_W10_LOG="$OUT/filt-after-new.log" bash "$V/run-suite.sh" "$WT" "$H" "$OUT/work"
for x in old new; do
  diff "$OUT/filt-before.log" "$OUT/filt-after-$x.log" > "$OUT/cmp-log-raw-$x.diff"; r1=$?
  diff <(norm "$OUT/filt-before.log") <(norm "$OUT/filt-after-$x.log") > "$OUT/cmp-log-norm-$x.diff"; r2=$?
  diff <(sed '1d;$d' "$OUT/filt-before.txt" | norm /dev/stdin) <(sed '1d;$d' "$OUT/filt-after-$x.txt" | norm /dev/stdin) > "$OUT/cmp-out-norm-$x.diff"; r3=$?
  log "  cmp filt-before vs filt-after-$x: log raw rc=$r1 ($(wc -l < "$OUT/cmp-log-raw-$x.diff") lines), log norm rc=$r2, output norm rc=$r3 | lines $(wc -l < "$OUT/filt-before.log")/$(wc -l < "$OUT/filt-after-$x.log")"
done
waitlow; log "scbash-after start"
run1 "$OUT/scbash-after.txt" env SC_BASH="$NO/sub/bash" SG_W10_ONLY=. bash "$V/run-suite.sh" "$WT" "$H" "$OUT/work"
log "  scbash-after: $(grep -a -m1 '^FAIL: ' "$OUT/scbash-after.txt") | $(tail -n 1 "$OUT/scbash-after.txt")"
c6round c6-new "$WT" "$V/run-suite.sh"
round c1-new "$OUT/c1-hook.sh" "$WT" "$V/run-suite.sh"
round c5-new "$OUT/c5-hook.sh" "$WT" "$V/run-suite.sh"
waitlow; log "impl start"
run1 "$OUT/impl.txt" bash -c 'cd "$1" && exec bash hooks/tests/secret-guard.test.sh' _ "$WT"
x6 "$OUT/impl.txt"; log "impl end | $(grep -a -m1 '^FAIL: ' "$OUT/impl.txt")"
log "PHASE2 DONE"

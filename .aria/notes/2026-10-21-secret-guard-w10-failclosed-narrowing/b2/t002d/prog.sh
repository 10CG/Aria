#!/usr/bin/env bash
# prog.sh <max seconds> <rounds ended> : wait (python sleep loop) until that many rounds have ended or ALLDONE; then print each round's summary lines
T=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/t002d
python3 - "$1" "$2" "$T" <<'PY'
import sys, time, glob
lim, want, T = float(sys.argv[1]), int(sys.argv[2]), sys.argv[3]; t0 = time.time()
def ended(): return sum(1 for m in glob.glob(T + '/*.meta') if not m.endswith(('pre.meta', 'chain.meta')) and '\nend ' in open(m).read())
while time.time() - t0 < lim and ended() < want and 'ALLDONE' not in open(T + '/chain.meta').read(): time.sleep(10)
PY
for l in b-usr b-5.0.18 b-5.1.16 b-5.3.20 b-3.2.57 wsl; do
  [[ -f $T/$l.meta ]] || continue
  printf '== %s | %s\n' "$l" "$(grep -E '^(wait|WAIT|start|end)' $T/$l.meta | cut -c1-80 | tr '\n' '|')"
  grep -E '^(PASS|FAIL|SKIP)' $T/$l.out 2>/dev/null | tr '\n' ' '; echo
  grep -E '^W10 (ported|older)' $T/$l.out 2>/dev/null | cut -c1-330
  grep -E '^  FAIL' $T/$l.out 2>/dev/null | cut -c1-300 | head -5
done
grep ALLDONE $T/chain.meta; echo "now $(date -u +%T) load $(cat /proc/loadavg)"
exit 0

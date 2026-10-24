# sourced by the 3c drivers
SP=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad
W=$SP/wt217/aria; V=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31; O=$SP/r217impl/t002e
B50=/home/dev/.aria/tools/bash-5.0.18/bash; B51=/home/dev/.aria/tools/bash-5.1.16/bash; B52=/usr/bin/bash
B53=/home/dev/.aria/tools/bash-5.3.20/bash; B32=/home/dev/.aria/tools/bash-3.2.57/bash
log() { printf '%s %s | load %s\n' "$(date -u +%T)" "$*" "$(cut -d' ' -f1-3 /proc/loadavg)" >> "$O/drive.log"; }
waitlow() {   # waits until the one-minute load is below 1.2 (at most 30 min, then goes on and logs it); always returns 0
  local t=0 l
  while :; do
    l=$(cut -d' ' -f1 /proc/loadavg)
    awk -v l="$l" 'BEGIN{exit !(l<1.2)}' && { log "waitlow ok at $l after ${t}s"; return 0; }
    if (( t >= 1800 )); then log "waitlow gave up at $l after ${t}s"; return 0; fi
    sleep 20; t=$((t+20))
  done
  return 0
}

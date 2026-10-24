#!/bin/bash
# verify-3e wrapper: for each distinct input, the first 2 calls with WSL_DISTRO_NAME set (the gate-closed runs) stall 1.5 s; then the C3 hook judges
if [[ "${BASH_SOURCE[0]}" != "$0" ]]; then source /tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/verify3e/c3.sh; return; fi   # sourced (the direct-call helper): just the C3 hook
in=$(cat)
if [[ -n ${WSL_DISTRO_NAME:-} ]]; then
  k=$(printf '%s' "$in" | sha256sum | cut -c1-16); c=0
  [[ -f /tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/verify3e/stall2.d/$k ]] && c=$(cat /tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/verify3e/stall2.d/$k)
  if (( c < 2 )); then echo $((c + 1)) > /tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/verify3e/stall2.d/$k; sleep 1.5; fi
fi
printf '%s' "$in" | exec bash /tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/verify3e/c3.sh

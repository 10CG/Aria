#!/usr/bin/env bash
# construction C6 (3e): C3 (the job returns 1 2.2 s after it starts) behind a stall of 1.5 s on the FIRST gate-closed run (WSL_DISTRO_NAME set) of
# each input, keyed by the sha256 of stdin in /tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/t002h/c6-marks (made anew for each round); later runs of the same input go straight to C3, under
# the same bash. Sourced (the direct-call helper), it sources C3 instead.
H=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/t002h/c3-hook.sh; M=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/t002h/c6-marks
if [[ "${BASH_SOURCE[0]}" != "$0" ]]; then . "$H"; return; fi
if [[ -n "${WSL_DISTRO_NAME+x}" ]]; then
  f=$(mktemp "$M/in.XXXXXX") || exit 98
  cat > "$f"
  k=$(sha256sum < "$f"); k=${k%% *}
  mkdir "$M/$k" 2>/dev/null && sleep 1.5
  exec "$BASH" "$H" "$@" < "$f"
fi
exec "$BASH" "$H" "$@"

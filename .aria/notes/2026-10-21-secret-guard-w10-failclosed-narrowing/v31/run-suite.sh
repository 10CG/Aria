#!/usr/bin/env bash
# run-suite.sh <aria checkout> <hook> [<work dir>] : runs aria's secret-guard regression suite (hooks/tests/secret-guard.test.sh, which carries the v31 cases
# ported by TASK-002 of 10CG/aria-plugin#217) on <hook>. <aria>/hooks is copied to a temporary directory (under <work dir> when given, removed at the end),
# its secret-guard.sh is replaced by <hook>, and the copy's suite runs there under taskset -c 0,1 nice -n 19. SC_BASH (the bash that runs the hook in the
# ported cases), SG_W10_ONLY (run only the ported cases whose id matches) and SG_W10_LOG (one result line per ported case, v31 format) are passed through;
# relative paths in SC_BASH and SG_W10_LOG are made absolute first, by readlink -m, which does not need the path to exist (3e; plan notes, the 3d
# ruling (1)): the value given always reaches the suite, so a SC_BASH that does not exist is the suite's FAIL to report, and when readlink -m gives
# nothing the value goes on unchanged. readlink -f, used before, printed nothing once the parent directory was missing too: SC_BASH went empty, the suite
# fell back to the bash on PATH and passed with status 0 (an environment error swallowed, fail-open), and SG_W10_LOG went empty, the log lost without
# a word. So when SG_W10_LOG's directory does not exist (or the path cannot be made absolute) this script stops with status 3 and says so on stderr:
# a log asked for must not be lost silently.
# The copy is not a git checkout: the cases that read an old hook through git show (SC-8, SC-9a) do not run in it, so the total that SC-13 counts differs
# from the header's Coverage numbers and SC-13 is red in the copy. Read SC-13 only from a run in a git checkout; a filtered round (SG_W10_ONLY) has no SC-13.
# Output: the suite's stdout and stderr. The first line records the date, the sha256 prefixes of <hook>, of the suite and of its direct-call helper
# (hooks/tests/lib/secret-guard-w10-direct.sh; "missing" when the copy has none), and the one-minute loads; the
# last line the loads at the end and the suite's exit status, which is also this script's (3, with neither line, when the copy cannot be built or
# SG_W10_LOG's directory does not exist).
set -u
[[ $# -ge 2 && -f "$1/hooks/tests/secret-guard.test.sh" && -f "$2" && -r "$2" ]] || { echo "usage: run-suite.sh <aria checkout> <hook> [<work dir>]" >&2; exit 3; }
A=$(readlink -f "$1"); HK=$(readlink -f "$2")
if [[ -n "${3:-}" ]]; then mkdir -p "$3" && T=$(mktemp -d "$(readlink -f "$3")/suite.XXXXXX"); else T=$(mktemp -d); fi || exit 3
trap 'rm -rf "$T"' EXIT
cp -a "$A/hooks" "$T/hooks" && cp "$HK" "$T/hooks/secret-guard.sh" && chmod 755 "$T/hooks/secret-guard.sh" || { echo "run-suite.sh: cannot build the copy in $T" >&2; exit 3; }
[[ -n "${SC_BASH:-}" ]] && export SC_BASH="$(readlink -m -- "$SC_BASH" || printf '%s' "$SC_BASH")"
if [[ -n "${SG_W10_LOG:-}" ]]; then
  export SG_W10_LOG="$(readlink -m -- "$SG_W10_LOG" || printf '%s' "$SG_W10_LOG")"
  [[ $SG_W10_LOG == /* && -d "$(dirname -- "$SG_W10_LOG")" ]] || { echo "run-suite.sh: SG_W10_LOG $SG_W10_LOG: its directory does not exist (or the path cannot be made absolute); the log asked for cannot be written" >&2; exit 3; }
fi
[[ -n "${SG_W10_ONLY:-}" ]] && export SG_W10_ONLY
HL="$T/hooks/tests/lib/secret-guard-w10-direct.sh"
printf '# run-suite.sh | %s | hook %s | suite %s | helper %s | SC_BASH %s | SG_W10_ONLY %s | load %s\n' "$(date -u +%FT%TZ)" "$(sha256sum < "$HK" | cut -c1-12)" \
  "$(sha256sum < "$T/hooks/tests/secret-guard.test.sh" | cut -c1-12)" "$([[ -f "$HL" ]] && sha256sum < "$HL" | cut -c1-12 || echo missing)" "${SC_BASH:-bash on PATH}" "${SG_W10_ONLY:-<none>}" "$(cut -d' ' -f1-3 /proc/loadavg)"
( cd "$T" && exec taskset -c 0,1 nice -n 19 bash hooks/tests/secret-guard.test.sh ) 2>&1; rc=$?
printf '# run-suite.sh end | load %s | suite exit %s\n' "$(cut -d' ' -f1-3 /proc/loadavg)" "$rc"
exit "$rc"

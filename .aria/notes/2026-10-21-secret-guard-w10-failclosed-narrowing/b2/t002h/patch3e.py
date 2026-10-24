#!/usr/bin/env python3
"""3e patch (10CG/aria-plugin#217): exact replacements, each old text must occur exactly once; line endings kept (newline=''); written atomically
with the file mode kept. Usage: patch3e.py <suite> <run-suite.sh>"""
import os, shutil, sys, tempfile

SUITE = [
# A: the six groups' shared comment
("""# assertion on the same output, with a wall only a fallback for time gives: >= 3.0 s, or over 2.0 s with a gate-closed run of the same input at least
# 1.0 s quicker; see wpa_x6), and the summary counts those fallbacks.
""",
"""# assertion on the same output, with a wall only a fallback for time gives: >= 3.0 s, or over 2.0 s with one of up to three gate-closed runs of the
# same input at least 1.0 s quicker; see wpa_x6), and the summary counts those fallbacks.
"""),
# B: no hook sha in the comment, the function names stay
("""# hook gives the baseline's block (What 4; P3, P6). Worked out from the hook (sha256 af4658b6f935), a fallback for time has three ways and no other:
""",
"""# hook gives the baseline's block (What 4; P3, P6). Worked out from the hook, a fallback for time has three ways and no other:
"""),
# C: (b) with up to three gate-closed runs, and why
("""# W. (3) Otherwise (the output is the baseline's block): (a) W >= 3.0 s: a deadline fallback (F1, F2 or a late F3). (b) 2.0 s < W < 3.0 s: the same
# input runs once more -- the same variables and directory, the budget variable cleared, plus WSL_DISTRO_NAME=Ubuntu, which closes the gate -- and its
# wall is Tb'; Tb' <= W - 1.0 s is a deadline fallback (F3: the checkpoint sent the rerun back, W more than 2 s over the baseline pass); otherwise the
# check is off with W and Tb' (the gate-closed run is as slow: the gate closed early, not the rerun's checkpoint). 1 s sits in the middle of F3's 2 s
# gap and leaves 1 s on each side for load jitter. (c) W <= 2.0 s: the check is off with W (a fallback for time does not end this early).
""",
"""# W. (3) Otherwise (the output is the baseline's block): (a) W >= 3.0 s: a deadline fallback (F1, F2 or a late F3). (b) 2.0 s < W < 3.0 s: the same
# input runs again up to three times, 1 s apart -- each run the same variables and directory, the budget variable cleared, plus WSL_DISTRO_NAME=Ubuntu,
# which closes the gate -- and each run's wall is a reading Tb'. The first reading with 0 < Tb' <= W - 1.0 s is a deadline fallback (F3: the
# checkpoint sent the rerun back, W more than 2 s over the baseline pass) and ends the runs; when none of the three is, the check is off with W and all
# three readings (the gate-closed runs are as slow: the gate closed early, not the rerun's checkpoint). 1 s sits in the middle of F3's 2 s gap and
# leaves 1 s on each side for load jitter. Why up to three runs (the 3c2 ruling): with one reading, a host that stalls that one run turns a lawful
# fallback red, and a lawful (b) shows up only when the host held the rerun past 2 s -- the host is busy just then, so the gate-closed run that follows
# is likely held up too (3c2: W 2.86 s with Tb' 1.74 s, for a command that takes about 0.66 s). A gate that closes early reads about W every time and
# stays red; a false green still needs W itself drawn out by more than 1 s (the retries only make Tb' less exposed to stalls).
# (c) W <= 2.0 s: the check is off with W (a fallback for time does not end this early).
"""),
# D: the summary's (b) item
("""# six groups gives the fallbacks over the trigger-point commands judged, each with its group and W (and Tb' for (b)).
""",
"""# six groups gives the fallbacks over the trigger-point commands judged, each with its group and W (and for (b) the Tb' that met the bound, followed by
# "(try k)" when that was the k-th run, k > 1).
"""),
# E: the (b) branch itself
("""  elif (( wus > 2000000 )); then   # (3b) F3 or a gate closed early: the same input once more with the gate closed (a reading of 0 is no reading)
    wpa_x6_hook "$input" WSL_DISTRO_NAME=Ubuntu
    if (( wpa_x6_us > 0 && wpa_x6_us <= wus - 1000000 )); then fb="${ws}s/Tb ${wpa_x6_s}s"
    else bad="baseline block at wall ${ws}s, gate-closed Tb' ${wpa_x6_s}s (want <= wall - 1.0 s): 关门那一遍同样慢：是准入门提前关，不是重跑的检查点"; fi
""",
"""  elif (( wus > 2000000 )); then   # (3b) F3 or a gate closed early: the same input with the gate closed, up to three runs 1 s apart (a reading of 0 is no reading)
    local try tbs=''
    for try in 1 2 3; do
      (( try > 1 )) && sleep 1
      wpa_x6_hook "$input" WSL_DISTRO_NAME=Ubuntu
      tbs+="${tbs:+, }${wpa_x6_s}s"
      if (( wpa_x6_us > 0 && wpa_x6_us <= wus - 1000000 )); then fb="${ws}s/Tb ${wpa_x6_s}s"; (( try > 1 )) && fb+=" (try $try)"; break; fi
    done
    [[ -n $fb ]] || bad="baseline block at wall ${ws}s, gate-closed Tb' ${tbs} (want <= wall - 1.0 s): 关门那一遍同样慢：是准入门提前关，不是重跑的检查点"
"""),
]

RUNSUITE = [
("""# relative paths in them are made absolute first.
""",
"""# relative paths in SC_BASH and SG_W10_LOG are made absolute first, by readlink -m, which does not need the path to exist (3e; plan notes, the 3d
# ruling (1)): the value given always reaches the suite, so a SC_BASH that does not exist is the suite's FAIL to report, and when readlink -m gives
# nothing the value goes on unchanged. readlink -f, used before, printed nothing once the parent directory was missing too: SC_BASH went empty, the suite
# fell back to the bash on PATH and passed with status 0 (an environment error swallowed, fail-open), and SG_W10_LOG went empty, the log lost without
# a word. So when SG_W10_LOG's directory does not exist (or the path cannot be made absolute) this script stops with status 3 and says so on stderr:
# a log asked for must not be lost silently.
"""),
("""# last line the loads at the end and the suite's exit status, which is also this script's (3 when the copy cannot be built).
""",
"""# last line the loads at the end and the suite's exit status, which is also this script's (3, with neither line, when the copy cannot be built or
# SG_W10_LOG's directory does not exist).
"""),
("""[[ -n "${SC_BASH:-}" ]] && export SC_BASH="$(readlink -f "$SC_BASH")"
[[ -n "${SG_W10_LOG:-}" ]] && export SG_W10_LOG="$(readlink -f "$SG_W10_LOG")"
""",
"""[[ -n "${SC_BASH:-}" ]] && export SC_BASH="$(readlink -m -- "$SC_BASH" || printf '%s' "$SC_BASH")"
if [[ -n "${SG_W10_LOG:-}" ]]; then
  export SG_W10_LOG="$(readlink -m -- "$SG_W10_LOG" || printf '%s' "$SG_W10_LOG")"
  [[ $SG_W10_LOG == /* && -d "$(dirname -- "$SG_W10_LOG")" ]] || { echo "run-suite.sh: SG_W10_LOG $SG_W10_LOG: its directory does not exist (or the path cannot be made absolute); the log asked for cannot be written" >&2; exit 3; }
fi
"""),
]

def apply(path, edits):
    with open(path, encoding='utf-8', newline='') as f:
        text = f.read()
    for i, (old, new) in enumerate(edits):
        n = text.count(old)
        if n != 1:
            sys.exit(f'{path}: edit {i} matches {n} times, nothing written')
        text = text.replace(old, new)
    d = os.path.dirname(path)
    fd, tmp = tempfile.mkstemp(dir=d, prefix='.patch3e.')
    with os.fdopen(fd, 'w', encoding='utf-8', newline='') as f:
        f.write(text)
    shutil.copymode(path, tmp)
    os.replace(tmp, path)
    print(f'{path}: {len(edits)} edits applied')

if __name__ == '__main__':
    apply(sys.argv[1], SUITE)
    apply(sys.argv[2], RUNSUITE)

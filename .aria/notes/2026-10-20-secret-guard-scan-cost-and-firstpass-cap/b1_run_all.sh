#!/usr/bin/env bash
# b1_run_all.sh : regenerate every B.1 measurement into evidence/ (run from the main repo root; hook under test = aria/hooks).
# Shared-host discipline: everything under taskset -c 0,1 nice -n 19, one experiment at a time.  Each file records UTC time,
# host load and the bash version.  The pilot (pilot-8-32.tsv, b1_curve.py --lens 8,32 --reps 1) is NOT re-run here (6.5 min).
set -u
N=$(cd "$(dirname "$0")" && pwd); E=$N/evidence; mkdir -p "$E"
HOOK=aria/hooks/secret-guard.sh; B32=/home/dev/.aria/tools/bash-3.2.57/bash; T="taskset -c 0,1 nice -n 19"
hdr() { echo "# $1 | $(date -u +%FT%TZ) | load $(uptime | sed 's/.*load average: //') | hook $(git -C aria rev-parse --short HEAD)"; }
IN=$(mktemp -d)
python3 -c "
import sys; sys.path.insert(0,'$N'); from b1_shapes import build
for kind in ('benign','secret'):
    for kb in (4,8,16,32): open('$IN/%s_C_%02d.txt'%(kind,kb),'w').write(build(kind,'C',kb))
"
# E2 -- in-process stage timing, C.UTF-8 vs C (bash 5)
{ hdr "E2 stage timing (b1_stage.sh), benign shape C"; for L in C.UTF-8 C; do env -i PATH=/usr/bin:/bin HOME=$IN LANG=$L LC_ALL=$L $T bash $N/b1_stage.sh $HOOK $IN/benign_C_04.txt $IN/benign_C_08.txt $IN/benign_C_16.txt 2>&1 | grep -v setlocale; done; } > $E/E2-stage.tsv
# E3 -- the bypass at the production default budget: credential read + padding (one pipeline C; own first segment S)
{ hdr "E3 bypass (b1_curve.py), production default budget"; $T python3 $N/b1_curve.py $HOOK --lens 12,14 --shapes C,S --kinds secret --reps 1 --timeout 60 2>&1 | grep -v setlocale; } > $E/E3-bypass.tsv
# E4 -- bash 3.2.57 whole process, benign C
{ hdr "E4 bash-3.2.57 whole process (b1_curve.py --bash)"; $T python3 $N/b1_curve.py $HOOK --bash $B32 --lens 2,4,8 --shapes C --kinds benign --reps 1 --timeout 90 2>&1 | grep -v setlocale; } > $E/E4-bash32.tsv
# E5 -- the risky_patterns detection loop alone, bash 3.2 and bash 5 (linear?)
{ hdr "E5 detection loop (b1_detect.sh)"; for B in $B32 /bin/bash; do env -i PATH=/usr/bin:/bin HOME=$IN LANG=C.UTF-8 LC_ALL=C.UTF-8 $T $B $N/b1_detect.sh $HOOK $IN/benign_C_08.txt $IN/benign_C_16.txt $IN/benign_C_32.txt $IN/secret_C_32.txt 2>&1 | grep -v setlocale; done; } > $E/E5-detect.tsv
# E6 -- g-c tier absolute (timing.py, A = B = the baseline hook)
{ hdr "E6 g-c tier (timing.py gc --pairs 3)"; $T python3 /home/dev/Aria/.aria/notes/2026-09-30-wpa-phase-a/writer-v6-proto/timing.py aria/hooks aria/hooks gc --pairs 3 2>&1 | grep -v setlocale; } > $E/E6-gc.txt
# E7 -- gate completeness: whole-string vs per-segment detection on 11 separator variants
{ hdr "E7 gate completeness (b1_gate_complete.sh)"; env -i PATH=/usr/bin:/bin HOME=$IN LANG=C.UTF-8 LC_ALL=C.UTF-8 bash $N/b1_gate_complete.sh $HOOK 2>&1 | grep -v setlocale; } > $E/E7-gate-complete.txt
rm -rf "$IN"
echo "evidence regenerated: $(ls $E | tr '\n' ' ')"

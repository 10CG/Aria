#!/bin/bash
# runall2.sh: the t005f2 runs (5f's runall.sh with the outputs under t005f2/runs). Each step starts only when the one-minute load is below 1.2, waiting
# up to 2 h; a step that never gets there is recorded NOT-RUN instead of being run anyway (INV-7). One step at a time.
set -u
S=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad
W=$S/wt217/aria; V=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31
O=$S/r217impl/t005f2/runs; mkdir -p "$O"; echo $$ > "$O/runall.pid"
BASE=$S/r217impl/t005f2/cs/hook-59e333c.sh; HK=$W/hooks/secret-guard.sh
T=(taskset -c 0,1 nice -n 19)
la() { cut -d' ' -f1-3 /proc/loadavg; }
waitload() { local i; for i in $(seq 1 720); do awk '{exit !($1 < 1.2)}' /proc/loadavg && return 0; sleep 10; done; return 1; }
step() { local n=$1 l0 t0=$SECONDS rc; shift; waitload || { echo "$n NOT-RUN load stayed >= 1.2 for 2 h" >> "$O/steps.log"; return 0; }; l0=$(la); "$@" > "$O/$n.txt" 2>&1; rc=$?; echo "$n rc=$rc load0=[$l0] load1=[$(la)] secs=$((SECONDS - t0))" >> "$O/steps.log"; }
unjudged() { grep -E '^SKIP: |^# totals' "$O/$1.txt" 2>/dev/null | grep -Eq '(load|void|inconclusive) [1-9]'; }
for b in /home/dev/.aria/tools/bash-5.0.18/bash /home/dev/.aria/tools/bash-5.1.16/bash /usr/bin/bash /home/dev/.aria/tools/bash-5.3.20/bash /home/dev/.aria/tools/bash-3.2.57/bash; do
  v=$("$b" -c 'echo ${BASH_VERSINFO[0]}.${BASH_VERSINFO[1]}.${BASH_VERSINFO[2]}')
  step "w10-$v" env -C "$W" SC_BASH="$b" SG_W10_ONLY=. "${T[@]}" bash hooks/tests/secret-guard.test.sh
  unjudged "w10-$v" && step "w10-$v-r2" env -C "$W" SC_BASH="$b" SG_W10_ONLY=. "${T[@]}" bash hooks/tests/secret-guard.test.sh
done
step full-path env -C "$W" "${T[@]}" bash hooks/tests/secret-guard.test.sh
unjudged full-path && step full-path-r2 env -C "$W" "${T[@]}" bash hooks/tests/secret-guard.test.sh
step full-wsl env -C "$W" WSL_DISTRO_NAME=Ubuntu "${T[@]}" bash hooks/tests/secret-guard.test.sh
step sc-cases env -C "$V" "${T[@]}" bash sc-cases.sh "$HK" "$BASE"
unjudged sc-cases && step sc-cases-r2 env -C "$V" "${T[@]}" bash sc-cases.sh "$HK" "$BASE"
for m in v31 suite; do
  e=(X_T005F2=1); [[ $m == suite ]] && e=(MUT_SUITE="$W")
  step "mut-$m" env "${e[@]}" "${T[@]}" bash "$V/run-mutants.sh" "$HK" "$O/mut-$m"
  nj=$(awk '$2=="NOT-JUDGED"{printf "%s|", $1}' "$O/mut-$m.txt" 2>/dev/null); nj=${nj%|}
  [[ -n "$nj" ]] && step "mut-$m-nj" env "${e[@]}" MUT_ONLY="^($nj)\$" "${T[@]}" bash "$V/run-mutants.sh" "$HK" "$O/mut-$m-nj"
  [[ "$(awk '$1=="P-0"{print $2}' "$O/mut-$m.txt" 2>/dev/null)" == GREEN ]] || step "mut-$m-p0" env "${e[@]}" MUT_ONLY='^P-0$' "${T[@]}" bash "$V/run-mutants.sh" "$HK" "$O/mut-$m-p0"
done
step w14 env W14_DIR="$O/w14" W14_OUT="$O/W14-independent-mutants.txt" W14_PREDICT="$S/r217impl/t003a/predict.md" W14_GAPMAP="$S/r217impl/t003a/gapmap.tsv" "${T[@]}" bash "$V/impl/w14.sh"
grep -q 'not judged 0,' "$O/W14-independent-mutants.txt" 2>/dev/null || step w14-r2 env W14_DIR="$O/w14b" W14_OUT="$O/W14-independent-mutants-r2.txt" W14_PREDICT="$S/r217impl/t003a/predict.md" W14_GAPMAP="$S/r217impl/t003a/gapmap.tsv" "${T[@]}" bash "$V/impl/w14.sh"
echo "ALL DONE $(date -u +%FT%TZ) load [$(la)]" >> "$O/steps.log"

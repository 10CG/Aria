#!/usr/bin/env bash
# w14-matrix.sh full | calib [case ...]        (TASK-003 second segment, 10CG/aria-plugin#217)
# Adversarial timing matrix of the relaxed rerun of the secret-guard hook. Run it as:   taskset -c 0,1 nice -n 19 bash w14-matrix.sh full
#   full  : writes W14-timing-matrix.txt next to this script: every shape x 5 runs under the bash on PATH, then the heaviest shapes x 3 runs under bash 5.0.18 and 5.3.20
#   calib : one run per named case (default: every w14 shape), one line each on stdout, nothing else written (sizing the shapes)
# Method (the one-call measure of v3/matrix.sh): the hook under test is the stage-timing copy of v31/mkdbg31.py (3 probe lines more than the hook, checked); one e2e call per run
# (JSON on stdin through a pipe, stderr to a file, HOME and cwd a scratch dir, LC_ALL=C.UTF-8, timeout), W = wall clock of that call from just before the launch to its exit.
# T_trigger = the relax-start probe (the relaxed rerun begins) relative to the same launch (first probe if several); a run with no rerun uses W itself (v31/run-evidence.sh, W12).
# bound = max(T_trigger, 3 s) + 0.3 s.  INV-7: one heavy experiment at a time; /proc/loadavg read at the start and the end of every batch (a batch = the runs of one case under one bash),
# a 1-minute reading >= 2.00 voids the batch (run again, at most 3 attempts); a batch starts only after the 1-minute load is < 1.2 (bounded wait; the reading is printed).
# After every run the scratch dir is searched for processes whose cwd is in it (a survivor of the rerun job); they are counted and killed (self-recorded: only this script's dirs).
set -u
export LC_ALL=C
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
NOTES=${W14_NOTES:-/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing}
SCR=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad
WORK=${W14_WORK:-$SCR/r217impl/t003b}
HOOK=${W14_HOOK:-$SCR/wt217/aria/hooks/secret-guard.sh}
EXPECT=${W14_EXPECT_SHA:-af4658b6f935}
GEN3=$NOTES/v3/gen-v3.py
MKDBG=$NOTES/v31/mkdbg31.py
SHAPES=$HERE/w14-shapes.py
OUT=${W14_OUT:-$HERE/W14-timing-matrix.txt}
B52=${W14_B52:-bash}
B50=/home/dev/.aria/tools/bash-5.0.18/bash
B53=/home/dev/.aria/tools/bash-5.3.20/bash
NRUN=${W14_NRUN:-5}
NRUN2=${W14_NRUN2:-3}
RUNTO=${W14_TO:-60}
WAITCUR=${W14_WAITMAX:-120}
HIGHN=0
EXTRA_C="cjk-bytes-lmax"
EXTRA_X="km-ext km-ext-small"
EXTRA_L="multiline-cred assign-storm late-core3"
FLOOR_US=${W14_FLOOR_US:-3000000}
SLACK_US=${W14_SLACK_US:-300000}
VOID_CENT=${W14_VOID_CENT:-200}
ONLY=${W14_ONLY:-}
WAITMAX_ORIG=$WAITCUR
LCDEF=C.UTF-8
TAGP="w14.$$"
ROWS=$WORK/rows.tsv
DBGH=$WORK/impl-dbg.sh
CASES=$WORK/cases.tsv
XDIR=$WORK/ext/proj
MODE=${1:-}
[[ $# -gt 0 ]] && shift

die() { echo "w14-matrix: $*" >&2; exit 3; }
sha12() { sha256sum < "$1" | cut -c1-12; }
sec() { if [[ "$1" == - ]]; then printf '%s' -; else printf '%d.%03d' $(( $1 / 1000000 )) $(( ($1 % 1000000) / 1000 )); fi; }
ld1() { local a; read -r a _ < /proc/loadavg; printf '%s' "$a"; }
cent() { local v=${1/./}; printf '%d' $((10#$v)); }
bver_of() { "$1" --version | head -1 | sed -E 's/.*version ([0-9.]+).*/\1/'; }
cleanup() {
  local p
  for p in $(find /proc -maxdepth 2 -name cwd -lname "$WORK/runs/$TAGP.*" 2>/dev/null | sed -E 's#/proc/([0-9]+)/cwd#\1#'); do
    [[ "$p" == "$$" ]] || kill -KILL "$p" 2>/dev/null
  done
  return 0
}
trap cleanup EXIT

wait_load() {   # waits for a 1-minute load < 1.2 (at most WAITCUR s; after 3 timeouts in a row the cap drops to 30 s); sets WAITED, PRELOAD; always returns 0
  local t=0 l
  PRELOAD=ok
  while :; do
    l=$(ld1)
    if (( $(cent "$l") < 120 )); then HIGHN=0; break; fi
    if (( t >= WAITCUR )); then PRELOAD=high; HIGHN=$((HIGHN + 1)); if (( HIGHN >= 3 )); then WAITCUR=30; fi; break; fi
    sleep 5; t=$((t + 5))
  done
  WAITED=$t
  return 0
}

prepare() {
  mkdir -p "$WORK/shapes" "$WORK/runs" "$XDIR/.aria"
  printf '%s\n' "/srv/billing/conf/prod.toml" > "$XDIR/.aria/secret-guard.paths"
  local got; got=$(sha12 "$HOOK"); [[ "$got" == "$EXPECT" ]] || die "the hook is $got, expected $EXPECT"
  python3 -I "$MKDBG" "$HOOK" "$DBGH" >/dev/null || die "mkdbg31.py failed"
  PD_PLUS=$(diff "$HOOK" "$DBGH" | grep -c '^>'); PD_MINUS=$(diff "$HOOK" "$DBGH" | grep -c '^<')
  [[ "$PD_PLUS" == 3 && "$PD_MINUS" == 0 ]] || die "probe diff is +$PD_PLUS -$PD_MINUS, not +3 -0"
  : > "$CASES"
  local name src desc c
  while IFS=$'\t' read -r name src desc; do
    if [[ "$src" == gen-v3 ]]; then python3 -I "$GEN3" "$name" "$WORK/shapes/$name.txt" >/dev/null || die "gen-v3 $name"
    else python3 -I "$SHAPES" "$name" "$WORK/shapes/$name.txt" >/dev/null || die "w14 $name"; fi
    jq -Rs '{tool_name:"Bash", tool_input:{command:.}}' < "$WORK/shapes/$name.txt" > "$WORK/shapes/$name.json" || die "jq $name"
    printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$name" "$name" "$src" "$LCDEF" "$desc" 0 >> "$CASES"
  done < <(python3 -I "$SHAPES" --list)
  for c in $EXTRA_C; do
    desc=$(awk -F'\t' -v c="$c" '$1==c{print $5}' "$CASES")
    printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$c@C" "$c" w14 C "$desc  [run under LC_ALL=C: a character is a byte]" 0 >> "$CASES"
  done
  for c in $EXTRA_X; do
    desc=$(awk -F'\t' -v c="$c" '$1==c{print $5}' "$CASES")
    printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$c@ext" "$c" gen-v3 "$LCDEF" "$desc  [run WITH a project extension (.aria/secret-guard.paths listing the read path): the relaxation is off, no rerun by design]" 1 >> "$CASES"
  done
  for c in $EXTRA_L; do
    desc=$(awk -F'\t' -v c="$c" '$1==c{print $5}' "$CASES")
    printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$c@en_US" "$c" w14 en_US.UTF-8 "$desc  [run under LC_ALL=en_US.UTF-8: collation-aware bracket expressions]" 0 >> "$CASES"
  done
  if [[ -n "$ONLY" ]]; then awk -F'\t' -v only=" $ONLY " 'index(only, " " $1 " ")' "$CASES" > "$CASES.f" && mv "$CASES.f" "$CASES"; fi
  return 0
}

classify() {   # RC ERRFILE -> the text kind
  local rc=$1 E=$2
  if (( rc == 0 )); then echo allow
  elif (( rc == 124 )); then echo KILLED
  elif (( rc != 2 )); then echo "rc$rc"
  elif grep -q 'exceeds 64 KB' "$E"; then echo bytes64k
  elif grep -q 'has a line longer than' "$E"; then echo longline
  elif grep -q 'grows by more than' "$E"; then echo growth
  elif grep -q 'segments together are longer than' "$E"; then echo tmax
  elif grep -q 'a variable value is longer than' "$E"; then echo size-value
  elif grep -q 'a command segment is longer than' "$E"; then echo size-seg
  elif grep -q 'too large for the project extension' "$E"; then echo ext-size
  elif grep -q 'the command is longer than' "$E"; then echo size-whole
  elif grep -q 'within the time budget' "$E"; then echo time
  elif grep -q '(extension)' "$E"; then echo ext-finding
  elif grep -q 'reads a secret-bearing source' "$E"; then echo finding
  else echo other; fi
  return 0
}

run_once() {   # BASHBIN HOOKFILE JSONFILE LOCALE [EXTDIR] -> ROW = rc kind W trig nrs job firstpass bound over survivors (tab separated; microseconds)
  local B=$1 H=$2 JF=$3 LCX=$4 XD=${5:-} D J t0 t1 rc kind fp rs nrs rj w trig t b over surv job fpv p
  local -a EV=(-u SECRET_GUARD_RAW_GATE -u SECRET_GUARD_TIME_BUDGET_S)
  if [[ -n "$XD" ]]; then EV+=("CLAUDE_PROJECT_DIR=$XD"); else EV+=(-u CLAUDE_PROJECT_DIR); fi
  D=$(mktemp -d "$WORK/runs/$TAGP.XXXXXX") || die "mktemp"
  : > "$D/dbg"
  J=$(<"$JF")
  t0=${EPOCHREALTIME/[.,]/}
  ( cd "$D" && printf '%s' "$J" | env "${EV[@]}" HOME="$D" SG_DBG="$D/dbg" LC_ALL="$LCX" timeout "$RUNTO" "$B" "$H" >/dev/null 2>"$D/err" )
  rc=$?
  t1=${EPOCHREALTIME/[.,]/}
  surv=0
  for p in $(find /proc -maxdepth 2 -name cwd -lname "$D" 2>/dev/null | sed -E 's#/proc/([0-9]+)/cwd#\1#'); do
    [[ "$p" == "$$" ]] && continue
    surv=$((surv + 1)); kill -KILL "$p" 2>/dev/null
  done
  read -r fp rs nrs rj < <(awk '$2=="firstpass-done" && fp=="" {fp=$1} $2=="relax-start" {n++; if (rs=="") rs=$1} $2=="relax-joined" && rj=="" {rj=$1} END {print (fp==""?"-":fp), (rs==""?"-":rs), n+0, (rj==""?"-":rj)}' "$D/dbg")
  w=$((t1 - t0)); trig=-; t=$w; job=-; fpv=-
  if [[ "$rs" != "-" ]]; then
    rs=${rs/[.,]/}; trig=$((rs - t0)); t=$trig
    if [[ "$rj" != "-" ]]; then job=$(( ${rj/[.,]/} - rs )); fi
  fi
  if [[ "$fp" != "-" ]]; then fpv=$(( ${fp/[.,]/} - t0 )); fi
  b=$(( (t > FLOOR_US ? t : FLOOR_US) + SLACK_US ))
  over=0; if (( w > b )); then over=1; fi
  kind=$(classify "$rc" "$D/err")
  if (( over == 0 )); then rm -rf "$D"; fi
  ROW=$(printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' "$rc" "$kind" "$w" "$trig" "$nrs" "$job" "$fpv" "$b" "$over" "$surv")
  return 0
}

batch() {   # CASE BASHBIN BASHVER NRUNS [STATUS] [LABEL] : runs the batch, appends the section to $OUT and the rows to $ROWS
  local cs=$1 B=$2 bver=$3 n=$4 st=${5:-ok} label=${6:-} shape src lcx desc xf xd="" attempt=0 ok=0 i l0="" l1="" a0 a1 chars bytes pre
  shape=$(awk -F'\t' -v c="$cs" '$1==c{print $2}' "$CASES"); src=$(awk -F'\t' -v c="$cs" '$1==c{print $3}' "$CASES")
  lcx=$(awk -F'\t' -v c="$cs" '$1==c{print $4}' "$CASES"); desc=$(awk -F'\t' -v c="$cs" '$1==c{print $5}' "$CASES"); xf=$(awk -F'\t' -v c="$cs" '$1==c{print $6}' "$CASES")
  if [[ "$xf" == 1 ]]; then xd=$XDIR; fi
  chars=$(LC_ALL=C.UTF-8 wc -m < "$WORK/shapes/$shape.txt"); bytes=$(wc -c < "$WORK/shapes/$shape.txt")
  : > "$WORK/batch.void"
  while (( attempt < 3 && ok == 0 )); do
    attempt=$((attempt + 1))
    wait_load
    l0=$(</proc/loadavg)
    : > "$WORK/batch.rows"
    for ((i = 1; i <= n; i++)); do
      run_once "$B" "$DBGH" "$WORK/shapes/$shape.json" "$lcx" "$xd"
      printf '%s\n' "$ROW" >> "$WORK/batch.rows"
    done
    l1=$(</proc/loadavg)
    a0=$(cent "${l0%% *}"); a1=$(cent "${l1%% *}")
    if (( a0 >= VOID_CENT || a1 >= VOID_CENT )); then
      echo "  VOID attempt $attempt: 1-minute load ${l0%% *} before / ${l1%% *} after (a reading >= $((VOID_CENT / 100)).$(printf %02d $((VOID_CENT % 100)))); batch discarded, run again" >> "$WORK/batch.void"
      awk -F'\t' -v b="$bver" -v c="$cs" -v a="$attempt" '{printf "%s\t%s\t%s\t%d\t%s\tvoid\n", b, c, a, NR, $0}' "$WORK/batch.rows" >> "$ROWS"
      continue
    fi
    ok=1
  done
  if [[ "$PRELOAD" == ok ]]; then pre='< 1.2'; else pre='HIGH (>= 1.2 after the bounded wait)'; fi
  {
    printf '## %s  [%s]  bash %s  LC_ALL=%s  command %s characters / %s bytes%s\n' "$cs" "$src" "$bver" "$lcx" "$chars" "$bytes" "${label:+  ($label)}"
    printf 'what: %s\n' "$desc"
    cat "$WORK/batch.void"
    printf 'load before: %s | after: %s | waited %ss | pre-run 1-minute load %s | attempt %s%s\n' "$l0" "$l1" "$WAITED" "$pre" "$attempt" "$( ((ok)) || echo '  UNRESOLVED: every attempt voided by load, rows not counted')"
    awk -F'\t' '{ t=($4=="-")?"-":sprintf("%.3f",$4/1e6); j=($6=="-")?"-":sprintf("%.3f",$6/1e6);
      printf "  run %d  rc=%-3s %-10s W=%7.3f s  T_trigger=%7s s  bound=%6.3f s  over=%-3s reruns=%s  job=%7s s  survivors=%s\n", NR, $1, $2, $3/1e6, t, $8/1e6, ($9==1?"YES":"no"), $5, j, $10 }' "$WORK/batch.rows"
    awk -F'\t' '{n++; if ($5>0) r++; if ($9==1) o++} END {printf "  summary: a rerun began in %d of %d runs; over the bound in %d\n\n", r, n, o}' "$WORK/batch.rows"
  } >> "$OUT"
  if (( ok )); then awk -F'\t' -v b="$bver" -v c="$cs" -v a="$attempt" -v s="$st" '{printf "%s\t%s\t%s\t%d\t%s\t%s\n", b, c, a, NR, $0, s}' "$WORK/batch.rows" >> "$ROWS"; fi
  echo "$(date +%T) $cs bash $bver ok=$ok attempt=$attempt load=${l1%% *}" >> "$WORK/progress.log"
  return 0
}

heaviest() {   # ranks the cases by the median W of the PATH-bash runs; both readings of "heaviest" are covered (union)
  local c med n anyr tmp="$WORK/rank.tsv" la lb
  : > "$tmp"
  while IFS=$'\t' read -r -u 3 c _; do
    n=$(awk -F'\t' -v c="$c" -v v="$B52VER" '$1==v && $2==c && $15=="ok"' "$ROWS" | wc -l)
    if (( n == 0 )); then continue; fi
    med=$(awk -F'\t' -v c="$c" -v v="$B52VER" '$1==v && $2==c && $15=="ok"{print $7}' "$ROWS" | sort -n | sed -n "$(( (n + 1) / 2 ))p")
    anyr=$(awk -F'\t' -v c="$c" -v v="$B52VER" '$1==v && $2==c && $15=="ok" && $9>0{k=1} END{print k+0}' "$ROWS")
    printf '%s\t%s\t%s\n' "$c" "$med" "$anyr" >> "$tmp"
  done 3< "$CASES"
  la=$(awk -F'\t' '$3==1' "$tmp" | sort -t$'\t' -k2,2nr -k1,1 | head -4 | cut -f1 | tr '\n' ' ')
  lb=$(sort -t$'\t' -k2,2nr -k1,1 "$tmp" | head -4 | cut -f1 | tr '\n' ' ')
  HEAVY=$(printf '%s %s' "$la" "$lb" | tr ' ' '\n' | awk 'NF && !seen[$0]++' | tr '\n' ' ')
  {
    echo "## the heaviest shapes (by the median W of the 5 runs under bash $B52VER); the brief does not say which of two readings is meant, so both are run:"
    echo "   A: among the shapes where a relaxed rerun began, the 4 with the highest median W (many end at the deadline, ~3.0 s, so ties are broken by name):  $la"
    echo "   B: among all shapes, the 4 with the highest median W:                                                                                         $lb"
    echo "   run under bash 5.0.18 and 5.3.20 (3 runs each), the union:                                                                                    $HEAVY"
    echo "   median W (s) of every case under bash $B52VER: $(sort -t$'\t' -k2,2nr -k1,1 "$tmp" | awk -F'\t' '{printf "%s=%.2f%s ", $1, $2/1e6, ($3==1?"*":"")}')   (* = a rerun began)"
    echo
  } >> "$OUT"
  return 0
}

full() {
  echo $$ > "$WORK/full.pid"
  prepare
  : > "$OUT"; : > "$ROWS"; : > "$WORK/progress.log"
  B52VER=$(bver_of "$B52"); local V50 V53 c ver B pairs
  V50=$(bver_of "$B50"); V53=$(bver_of "$B53")
  {
    echo "# W14 timing matrix | date $(date '+%F %T %z') | load $(</proc/loadavg) | implementation secret-guard.sh sha256 $(sha12 "$HOOK") | instrumented copy (mkdbg31.py, diff +$PD_PLUS -$PD_MINUS) $(sha12 "$DBGH") | gen-v3.py $(sha12 "$GEN3") | w14-shapes.py $(sha12 "$SHAPES")"
    echo "# TASK-003 second segment, 10CG/aria-plugin#217 | w14-matrix.sh $(sha12 "${BASH_SOURCE[0]}") | mkdbg31.py $(sha12 "$MKDBG") | bash $B52VER (PATH), $V50, $V53 | taskset $(taskset -cp $$ | sed 's/.*: //') nice $(ps -o ni= -p $$ | tr -d ' ') | hook timeout ${RUNTO}s"
    echo "# one e2e call per run (JSON on stdin through a pipe, stderr to a file, HOME and cwd a scratch dir); W = wall clock of the call; T_trigger = the relax-start probe of the instrumented copy, relative to the same launch (W itself when no rerun began);"
    echo "# parameters: floor ${FLOOR_US} us, slack ${SLACK_US} us, void at ${VOID_CENT} (hundredths of the 1-minute load), runs ${NRUN}/${NRUN2}, wait cap ${WAITMAX_ORIG} s, cases: ${ONLY:-all}"
    echo "# bound = max(T_trigger, 3 s) + 0.3 s; over = W > bound. Loads are /proc/loadavg (1 5 15 minutes, running/total, last pid); a 1-minute reading >= 2.00 at the start or the end of a batch voids the batch."
    echo
  } >> "$OUT"
  while IFS=$'\t' read -r -u 3 c _; do batch "$c" "$B52" "$B52VER" "$NRUN" ok; done 3< "$CASES"
  heaviest
  for ver in "$V50" "$V53"; do
    if [[ "$ver" == "$V50" ]]; then B=$B50; else B=$B53; fi
    for c in $HEAVY; do batch "$c" "$B" "$ver" "$NRUN2" ok; done
  done
  pairs=$(awk -F'\t' '$15=="ok" && $13==1{print $1 "\t" $2}' "$ROWS" | sort -u)
  if [[ -n "$pairs" ]]; then
    WAITCUR=300; HIGHN=0
    echo "## re-runs of every (bash, shape) that went over its bound, at low load (not counted in the totals):" >> "$OUT"
    while IFS=$'\t' read -r -u 4 ver c; do
      if [[ "$ver" == "$V50" ]]; then B=$B50; elif [[ "$ver" == "$V53" ]]; then B=$B53; else B=$B52; fi
      batch "$c" "$B" "$ver" 5 confirm "confirmation re-run"
    done 4<<< "$pairs"
  fi
  local M O
  M=$(awk -F'\t' '$15=="ok"' "$ROWS" | wc -l); O=$(awk -F'\t' '$15=="ok" && $13==1' "$ROWS" | wc -l)
  {
    echo "## outcomes over 3 s with no relaxed rerun (outside the bound by definition: the baseline first pass, 10CG/aria-plugin#228):"
    awk -F'\t' '$15=="ok" && $9==0 && $7>3000000 {printf "  bash %s  %s  run %d  rc=%s %s  W=%.3f s\n", $1, $2, $4, $5, $6, $7/1e6; k++} END {if (!k) print "  none"}' "$ROWS"
    echo "## runs that left a process behind (found by cwd and killed): $(awk -F'\t' '$15=="ok" && $14>0' "$ROWS" | wc -l); batches voided by load: $(awk -F'\t' '$15=="void" && $4==1' "$ROWS" | wc -l); confirmation runs over the bound: $(awk -F'\t' '$15=="confirm" && $13==1' "$ROWS" | wc -l) of $(awk -F'\t' '$15=="confirm"' "$ROWS" | wc -l)"
    echo "every outcome within max(trigger, 3 s) + 0.3 s: $((M - O)) of $M (over the bound: $O)"
  } >> "$OUT"
  return 0
}

calib() {
  prepare
  B52VER=$(bver_of "$B52")
  local list=("$@") c shape lcx xf xd rc kind w trig nrs job fpv bound over surv
  if (( ${#list[@]} == 0 )); then mapfile -t list < <(awk -F'\t' '$3=="w14"{print $1}' "$CASES"); fi
  echo "calib bash $B52VER, timeout ${RUNTO}s, load at start: $(</proc/loadavg)"
  for c in "${list[@]}"; do
    shape=$(awk -F'\t' -v c="$c" '$1==c{print $2}' "$CASES"); lcx=$(awk -F'\t' -v c="$c" '$1==c{print $4}' "$CASES"); xf=$(awk -F'\t' -v c="$c" '$1==c{print $6}' "$CASES")
    if [[ -z "$shape" ]]; then   # not a listed case: a free-form shape name of w14-shapes.py (late:<k>:<pad>), sized on the fly
      shape=$c; lcx=$LCDEF; xf=0
      python3 -I "$SHAPES" "$shape" "$WORK/shapes/$shape.txt" >/dev/null 2>&1 || { echo "$c: no such case"; continue; }
      jq -Rs '{tool_name:"Bash", tool_input:{command:.}}' < "$WORK/shapes/$shape.txt" > "$WORK/shapes/$shape.json"
    fi
    xd=""; if [[ "$xf" == 1 ]]; then xd=$XDIR; fi
    run_once "$B52" "$DBGH" "$WORK/shapes/$shape.json" "$lcx" "$xd"
    IFS=$'\t' read -r rc kind w trig nrs job fpv bound over surv <<< "$ROW"
    printf '%-18s rc=%-3s %-10s W=%7s trig=%7s reruns=%s job=%7s firstpass=%7s over=%s surv=%s\n' "$c" "$rc" "$kind" "$(sec "$w")" "$(sec "$trig")" "$nrs" "$(sec "$job")" "$(sec "$fpv")" "$over" "$surv"
  done
  echo "load at end: $(</proc/loadavg)"
  return 0
}

case "$MODE" in
  full) full ;;
  calib) calib "$@" ;;
  *) echo "usage: w14-matrix.sh full | calib [case ...]" >&2; exit 2 ;;
esac

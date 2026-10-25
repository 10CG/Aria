#!/usr/bin/env bash
# patch-and-check.sh (T004b, 10CG/aria-plugin#217): applies the four changes of the brief to v31/run-evidence.sh, runs the light checks (no heavy
# experiment), and writes drive.sh (the background driver of the five phases). No command text of the corpus is read or printed.
set -u
S=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad; T=$S/r217impl/t004b; C=$T/chk
REPO=/home/dev/Aria; NR=.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing; V31=$REPO/$NR/v31; F=$V31/run-evidence.sh
B32=/home/dev/.aria/tools/bash-3.2.57/bash
mkdir -p "$C"
echo "== CR bytes in run-evidence.sh before: $(grep -c $'\r' "$F")"
python3 - "$F" <<'PY' || exit 1
import sys
p = sys.argv[1]
t = open(p, encoding='utf-8', newline='').read()
n0 = t.count('\n')
def rep(old, new):
    global t
    c = t.count(old)
    assert c == 1, (old[:80], c)
    t = t.replace(old, new)
B1B = r'''      echo "## 1b. latency cost: the same 138 replayed on the baseline hook (replay138.sh fed base.sh: no probes, so no trigger time), aligned by n; extra = wall of the hook under test - wall of the baseline (s; p50 / p90 by nearest rank)"
      "${N[@]}" bash "$HERE/replay138.sh" "$W/base.sh" "$W1" "$W/W12-replay-138-base.rows" 2>&1 | grep -v setlocale
      { printf '%s\n' "$H12"; cat "$W/W12-replay-138-base.rows"; } > "$W/W12-replay-138-base.tsv"
      echo "  bytes: ident.sh (rc + sha256(stderr), the baseline vs the uninstrumented hook under test) on the same 138 in a separate pass (W12-ident-138.txt)"
      cut -f1 "$W1" > "$W/W12-138.lst"
      { printf '%s\n' "$H12"; "${N[@]}" bash "$HERE/ident.sh" "$W/base.sh" "$W/impl.sh" "$W/W12-138.lst" 2>&1 | grep -v setlocale; } > "$W/W12-ident-138.txt"
      awk -F'\t' '
        function srt(a, n,   i, j, x) { for (i = 2; i <= n; i++) { x = a[i]; for (j = i - 1; j > 0 && a[j] > x; j--) a[j + 1] = a[j]; a[j + 1] = x } }
        function q(a, n, pc,   i) { i = int(pc * n); if (i < pc * n) i++; if (i < 1) i = 1; return a[i] }
        function dist(a, n) { if (n == 0) return "n=0"; srt(a, n); return sprintf("n=%d p50=%.3f p90=%.3f max=%.3f", n, q(a, n, .5), q(a, n, .9), a[n]) }
        FNR == 1 { f++ }
        /^#/ { next }
        f == 1 { o[++m] = $1; rc[$1] = $2 + 0; k[$1] = $3; w[$1] = $4; rs[$1] = $6; next }
        f == 2 { bk[$1] = $3; bw[$1] = $4; bc[$3]++; next }
        f == 3 && /^DIFF n=/ { split($0, dv, /[ =]/); d[dv[3]] = 1; next }
        f == 3 && /^identical=/ { idl = $0; next }
        END {
          for (x in bc) bl = bl sprintf(" %s %d", x, bc[x]); printf "  baseline replay outcomes:%s\n", bl
          for (i = 1; i <= m; i++) { x = o[i]
            if (!(x in bw)) { nb = nb " " x; continue }
            e = w[x] - bw[x]
            if (rs[x] == "-") { nr++; if (x in d) nd = nd " " x; else ni++; continue }
            if (rc[x] == 0) { ea[++na] = e; continue }
            if (rc[x] == 2 && k[x] == bk[x] && k[x] ~ /^(oversize|longline|growth|tmax)$/) { ef[++nf] = e
              fl[nf] = sprintf("    n=%-6s W %.3f  base W %.3f  extra %.3f  (%s; ident pass: %s)", x, w[x], bw[x], e, k[x], ((x in d) ? "differs" : "identical")); continue }
            no++; ol = ol sprintf("\n    n=%-6s rc %d %s (baseline %s)  W %.3f  base W %.3f", x, rc[x], k[x], bk[x], w[x], bw[x])
          }
          printf "  entered the rerun, fell back to the size text of the baseline (relax-start, rc 2, the kind of the baseline): %d\n", nf
          for (i = 1; i <= nf; i++) print fl[i]
          printf "    extra (s): %s\n", dist(ef, nf)
          printf "  entered the rerun and allowed: extra (s): %s\n", dist(ea, na)
          printf "  entered the rerun, any other outcome: %d%s\n", no, ol
          printf "  did not enter the rerun: %d; rc + sha256(stderr) identical to the baseline (ident pass): %d of %d%s\n", nr, ni, nr, (nd == "" ? "" : "; differ:" nd)
          printf "  ident pass over the 138: %s%s\n", idl, (nb == "" ? "" : "; not in the baseline replay:" nb)
        }' "$W/W12-replay-138.tsv" "$W/W12-replay-138-base.tsv" "$W/W12-ident-138.txt"
'''
# 1. W9: the first line is taken before the two suite runs
rep(r'''    for t in base impl; do "${N[@]}" bash "$W/tree-$t/hooks/tests/secret-guard.test.sh"''',
    r'''    H9=$(hdr)   # before the two suite runs: the first line carries the load at the start, the last line (hdr below) the load at the end (INV-7)
    for t in base impl; do "${N[@]}" bash "$W/tree-$t/hooks/tests/secret-guard.test.sh"''')
rep(r'''    { hdr; echo "# the suite of aria 59e333c''', r'''    { printf '%s\n' "$H9"; echo "# the suite of aria 59e333c''')
# 2. W12 without TRAFFIC_DIR/cmds exits 3 with the other checks, before any file is written
rep(r'''(W13 and W12 need BASH32)"; exit 3; }; done
''', r'''(W13 and W12 need BASH32)"; exit 3; }; done
for st in $STAGES; do [[ $st != W12 || ( -n "${TRAFFIC_DIR:-}" && -d "${TRAFFIC_DIR:-}/cmds" ) ]] || { echo "W12 needs TRAFFIC_DIR, the frozen corpus with its cmds directory: '${TRAFFIC_DIR:-}'"; exit 3; }; done
''')
rep(r'''W12 also TRAFFIC_DIR (the frozen corpus, outside the
# repo). A bash under test that is missing or not executable, an OUT that is not a writable directory, or a work dir that cannot be created exits 3 before
# any file is written.
''', r'''W12 also TRAFFIC_DIR (the frozen corpus, outside the
# repo, with its cmds directory). A bash under test that is missing or not executable, W12 without TRAFFIC_DIR/cmds, an OUT that is not a writable
# directory, or a work dir that cannot be created exits 3 before any file is written.
''')
rep(r'''# the load; the W8 diff starts with that line too (patch and git apply skip the text before a diff).
''', r'''# the load, taken before the stage's runs start; W9, W11, W12 and W13 write it again as their last line (the load at the end, INV-7). The W8 diff starts
# with that line too (patch and git apply skip the text before a diff), and so do the W12 TSVs (their readers skip the lines that start with #).
''')
# 3. the header line of W12-replay-138.tsv (INV-8); every reader skips the lines that start with #
rep(r'''>/dev/null || exit 3
    { hdr; echo "## 1. the W10''', r'''>/dev/null || exit 3
    H12=$(hdr)   # the first line of W12-real-traffic.txt and of the TSVs written beside it (INV-8)
    { printf '%s\n' "$H12"; echo "## 1. the W10''')
rep(r'''"$W/impl-dbg.sh" "$W1" "$W/W12-replay-138.tsv" 2>&1 | grep -v setlocale
''', r'''"$W/impl-dbg.sh" "$W1" "$W/W12-replay-138.rows" 2>&1 | grep -v setlocale
      { printf '%s\n' "$H12"; cat "$W/W12-replay-138.rows"; } > "$W/W12-replay-138.tsv"
''')
rep(r'''awk -F'\t' '{c[$3]++}''', r'''awk -F'\t' '/^#/{next} {c[$3]++}''')
rep(r'''NR==FNR{cls[$1]=$5; next} {printf''', r'''NR==FNR{cls[$1]=$5; next} /^#/{next} {printf''')
rep(r'''awk -F'\t' '$3=="allow"{print''', r'''awk -F'\t' '/^#/{next} $3=="allow"{print''')
rep(r'''awk -F'\t' '{t=($6=="-"?$4:$6);''', r'''awk -F'\t' '/^#/{next} {m++; t=($6=="-"?$4:$6);''')
# 4. 1b, after the last line of section 1
rep(r'''over the bound\n", v+0, NR}' "$W/W12-replay-138.tsv"
''', r'''over the bound\n", v+0, m}' "$W/W12-replay-138.tsv"
''' + B1B)
rep(r'''cp "$W/W12-real-traffic.txt" "$W/W12-replay-138.tsv" "$OUT/"''',
    r'''cp "$W/W12-real-traffic.txt" "$W/W12-replay-138.tsv" "$W/W12-replay-138-base.tsv" "$W/W12-ident-138.txt" "$OUT/"''')
open(p, 'w', encoding='utf-8', newline='').write(t)
print('patched: newlines', n0, '->', t.count('\n'))
PY
echo "== CR bytes after: $(grep -c $'\r' "$F") | bash -n: $(bash -n "$F" 2>&1 && echo ok) | mode $(stat -c %a "$F")"
git -C "$REPO" diff -- "$NR/v31/run-evidence.sh" > "$T/run-evidence.diff"
echo "== diff: +$(grep -c '^+[^+]' "$T/run-evidence.diff") -$(grep -c '^-[^-]' "$T/run-evidence.diff") | other v31 changes: $(git -C "$REPO" status --porcelain -- "$NR/v31" | grep -v -e 'run-evidence.sh$' -e 'v31/impl/W9-suite.txt$' | wc -l)"

echo "== 2. TRAFFIC_DIR: exit 3 before any file (new script); the old script (HEAD) for contrast"
rm -rf "$C/out" "$C/out-old" "$C/nocmds" "$C"/tA "$C"/tB "$C"/tC "$C"/tD "$C"/tE "$C"/tOLD; mkdir -p "$C/out" "$C/out-old" "$C/nocmds"
trun() { local tag=$1 td=$2 rc; shift 2
  if [[ $td == UNSET ]]; then env -u TRAFFIC_DIR IMPL="$T/impl-hook.sh" OUT="$C/out" BASH32="$B32" bash "$F" "$C/$tag/wd" "$@" > "$C/$tag.log" 2>&1
  else TRAFFIC_DIR="$td" IMPL="$T/impl-hook.sh" OUT="$C/out" BASH32="$B32" bash "$F" "$C/$tag/wd" "$@" > "$C/$tag.log" 2>&1; fi; rc=$?
  printf '  %-4s %-9s rc=%s wd=%s out-files=%s | %s\n' "$tag" "$*" "$rc" "$([[ -e $C/$tag ]] && echo created || echo absent)" "$(ls "$C/out" | wc -l)" "$(tail -1 "$C/$tag.log" | cut -c1-80)"; }
trun tA '' W12; trun tB "$C/nocmds" W12; trun tC UNSET W12; trun tE '' W8 W12; trun tD UNSET W8
( cd "$V31" && TRAFFIC_DIR='' IMPL="$T/impl-hook.sh" OUT="$C/out-old" BASH32="$B32" bash -c "$(git -C "$REPO" show HEAD:"$NR"/v31/run-evidence.sh)" ./run-evidence.sh "$C/tOLD/wd" W12 > "$C/tOLD.log" 2>&1 ); rc=$?
printf '  OLD  W12       rc=%s wd=%s files-in-wd=%s | %s\n' "$rc" "$([[ -e $C/tOLD ]] && echo created || echo absent)" "$(ls "$C/tOLD/wd" 2>/dev/null | wc -l)" "$(tail -1 "$C/tOLD.log" | cut -c1-80)"

echo "== 3. section 1 of W12: old readers on the TSV without a header vs new readers on it with a header (95cf1de7's TSV)"
git -C "$REPO" show HEAD:"$NR"/v31/run-evidence.sh | grep -F -e 'outcome %-10s' -e 'W1 class %-6s' -e 'allow wall (s)' -e 'every outcome within' | sed 's|"$W/W12-replay-138.tsv"|"$TSV"|g' > "$C/s1-old.sh"
grep -F -e 'outcome %-10s' -e 'W1 class %-6s' -e 'allow wall (s)' -e 'every outcome within' "$F" | sed 's|"$W/W12-replay-138.tsv"|"$TSV"|g' > "$C/s1-new.sh"
git -C "$REPO" show 95cf1de7:"$NR"/v31/W12-replay-138.tsv > "$C/95.rows"; { echo '# header (check)'; cat "$C/95.rows"; } > "$C/95.tsv"
git -C "$REPO" show 95cf1de7:"$NR"/v31/W12-real-traffic.txt | sed -n '3,10p' > "$C/s1-95.txt"
export W1="$REPO/$NR/evidence/W1-classification.tsv"
TSV="$C/95.rows" bash "$C/s1-old.sh" > "$C/s1-old.txt"; TSV="$C/95.tsv" bash "$C/s1-new.sh" > "$C/s1-new.txt"; TSV="$C/95.tsv" bash "$C/s1-old.sh" > "$C/s1-oldhdr.txt"
echo "  readers: old $(wc -l < "$C/s1-old.sh") lines, new $(wc -l < "$C/s1-new.sh") lines, new lines reading the TSV $(grep -c '"$TSV"' "$C/s1-new.sh")"
cmp -s "$C/s1-old.txt" "$C/s1-new.txt" && echo "  SAME: old on rows vs new on header+rows ($(wc -l < "$C/s1-new.txt") lines)" || echo "  DIFFER: old vs new"
cmp -s "$C/s1-old.txt" "$C/s1-95.txt" && echo "  SAME as 95cf1de7 W12-real-traffic.txt lines 3-10" || echo "  DIFFER from 95cf1de7 lines 3-10"
cmp -s "$C/s1-old.txt" "$C/s1-oldhdr.txt" && echo "  NEGATIVE CONTROL SAME (the check cannot go red)" || echo "  negative control: old readers on header+rows differ in $(diff "$C/s1-old.txt" "$C/s1-oldhdr.txt" | grep -c '^[<>]') lines"

echo "== 4. 1b on synthetic inputs (95cf1de7 rows as the hook under test; a made-up baseline at 0.200 s; ident DIFF for the allowed ones)"
python3 - "$F" "$C" <<'PY'
import sys
f, c = sys.argv[1], sys.argv[2]
L = open(f, encoding='utf-8').read().split('\n')
i = L.index("      awk -F'\\t' '")
j = next(k for k in range(i, len(L)) if L[k].startswith("        }' \"$W/W12-replay-138.tsv\""))
prog = '\n'.join(L[i:j + 1]).replace('"$W/W12-replay-138.tsv"', '"$C/95.tsv"').replace('"$W/W12-replay-138-base.tsv"', '"$C/fakebase.tsv"').replace('"$W/W12-ident-138.txt"', '"$C/fakeident.txt"')
open(c + '/b1b.sh', 'w').write(prog + '\n')
rows = [l.split('\t') for l in open(c + '/95.rows').read().split('\n') if l]
with open(c + '/fakebase.tsv', 'w') as o:
    o.write('# header (check)\n')
    for r in rows: o.write('\t'.join([r[0], '2', 'growth' if r[2] == 'growth' else 'oversize', '0.200', '-', '-', '-']) + '\n')
d = [r[0] for r in rows if r[2] == 'allow']
with open(c + '/fakeident.txt', 'w') as o:
    o.write('# header (check)\n')
    for n in d: o.write('DIFF n=%s base_rc=2 impl_rc=0\n' % n)
    o.write('identical=%d different=%d\n' % (len(rows) - len(d), len(d)))
print('  extracted', j - i + 1, 'lines; rows', len(rows), 'allow', len(d), '| relax-start present:', sum(r[5] != '-' for r in rows), '| kinds with relax-start:', sorted(set(r[2] for r in rows if r[5] != '-')))
PY
C="$C" bash "$C/b1b.sh" 2>&1 | head -14

cat > "$T/drive.sh" <<'DRV'
#!/usr/bin/env bash
# drive.sh (T004b, 10CG/aria-plugin#217): the five phases one after another (one heavy experiment at a time). A phase starts only when the 1-min load is
# < 1.2; INV-7 judges it on the readings its output records at its start and at its end (first and last line): either >= 2 -> void, rerun, at most 3
# attempts; 6 h without a low-load window -> give up on that phase. NOT-JUDGED bad implementations (P-0 aside: it has its own phase) are rerun once.
set -u
S=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad
T=$S/r217impl/t004b; V31=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31; OUTD=$V31/impl
WT=$S/wt217/aria; HK=$T/impl-hook.sh; B52=/usr/bin/bash
export IMPL=$HK OUT=$OUTD BASH32=/home/dev/.aria/tools/bash-3.2.57/bash
TN=(taskset -c 0,1 nice -n 19); LOG=$T/drive.log; mkdir -p "$T/runs"
cd "$T" || exit 3; echo $$ > "$T/drive.pid"
note() { printf '%s %s | load %s\n' "$(date -u +%FT%TZ)" "$*" "$(cut -d' ' -f1-3 /proc/loadavg)" >> "$LOG"; }
ge() { awk -v a="$1" -v b="$2" 'BEGIN{exit !(a + 0 >= b + 0)}'; }
waitlow() { local t0=$SECONDS; while ge "$(cut -d' ' -f1 /proc/loadavg)" 1.2; do (( SECONDS - t0 >= 21600 )) && return 1; sleep 15; done; }
[[ "$(sha256sum < "$HK" | cut -c1-12)" == af4658b6f935 ]] || { note "STOP: the hook copy is not af4658b6f935"; exit 3; }
note "DRIVER-START pid $$ | wt $(git -C "$WT" rev-parse --short HEAD) dirty $(git -C "$WT" status --porcelain | wc -l) | run-evidence.sh $(sha256sum < "$V31/run-evidence.sh" | cut -c1-12)"
runW9()   { "${TN[@]}" bash "$V31/run-evidence.sh" "$T/wd-W9-a$1" W9; };   outW9()   { echo "$T/wd-W9-a$1/W9-suite.txt"; }
runW13()  { MUT_SCOPE=full "${TN[@]}" bash "$V31/run-evidence.sh" "$T/wd-W13-a$1" W13; };   outW13()  { echo "$T/wd-W13-a$1/W13-sc-cases.txt"; }
runP0v()  { SC_BASH=$B52 MUT_ONLY='P-0' "${TN[@]}" bash "$V31/run-mutants.sh" "$HK" "$T/wd-P0v-a$1" > "$T/P0-v31-a$1.txt" 2>&1; };   outP0v()  { echo "$T/P0-v31-a$1.txt"; }
runP0s()  { SC_BASH=$B52 MUT_ONLY='P-0' MUT_SUITE="$WT" "${TN[@]}" bash "$V31/run-mutants.sh" "$HK" "$T/wd-P0s-a$1" > "$T/P0-suite-a$1.txt" 2>&1; };   outP0s()  { echo "$T/P0-suite-a$1.txt"; }
runSM()   { SC_BASH=$B52 MUT_SUITE="$WT" "${TN[@]}" bash "$V31/run-mutants.sh" "$HK" "$T/wd-SM-a$1" > "$T/suite-mutants-a$1.txt" 2>&1; };   outSM()   { echo "$T/suite-mutants-a$1.txt"; }
runNJ13() { SC_BASH=$B52 MUT_SCOPE=full MUT_ONLY="$NJIDS" "${TN[@]}" bash "$V31/run-mutants.sh" "$HK" "$T/wd-NJ13-a$1" > "$T/W13-rerun-a$1.txt" 2>&1; };   outNJ13() { echo "$T/W13-rerun-a$1.txt"; }
runNJSM() { SC_BASH=$B52 MUT_SUITE="$WT" MUT_ONLY="$NJIDS" "${TN[@]}" bash "$V31/run-mutants.sh" "$HK" "$T/wd-NJSM-a$1" > "$T/suite-rerun-a$1.txt" 2>&1; };   outNJSM() { echo "$T/suite-rerun-a$1.txt"; }
runW12()  { TRAFFIC_DIR="$S/traffic-frozen" "${TN[@]}" bash "$V31/run-evidence.sh" "$T/wd-W12-a$1" W12; };   outW12()  { echo "$T/wd-W12-a$1/W12-real-traffic.txt"; }
LAST=''; NJIDS=''
phase() { local p=$1 a f s e rc
  for a in 1 2 3; do
    waitlow || { note "$p NO-LOW-WINDOW-6H"; return 1; }
    f=$(out$p "$a"); note "$p a$a START"
    run$p "$a" > "$T/runs/$p.a$a.log" 2>&1; rc=$?
    s=$(head -1 "$f" 2>/dev/null | grep -oE 'load [0-9.]+' | head -1 | cut -d' ' -f2)
    e=$(tail -1 "$f" 2>/dev/null | grep -oE 'load (at the end )?[0-9.]+' | tail -1 | grep -oE '[0-9.]+$')
    LAST=$f
    if [[ -n "$s" && -n "$e" ]] && ! ge "$s" 2 && ! ge "$e" 2; then note "$p a$a END rc=$rc VALID start=$s end=$e"; return 0; fi
    note "$p a$a END rc=$rc VOID start=${s:-none} end=${e:-none}"
  done
  note "$p VOID-3X"; return 1; }
nj() { awk '$2=="NOT-JUDGED" && $1!="P-0"{print $1}' "$1" 2>/dev/null | paste -sd'|' -; }
phase W9
phase W13; NJIDS=$(nj "$LAST"); [[ -n $NJIDS ]] && { note "W13 NOT-JUDGED other than P-0: $NJIDS"; phase NJ13; cp "$LAST" "$OUTD/W13-mutants-rerun.txt"; }
phase P0v; [[ -f $LAST ]] && cp "$LAST" "$OUTD/W13-P0-v31.txt"
phase P0s; [[ -f $LAST ]] && cp "$LAST" "$OUTD/W13-P0-suite.txt"
phase SM; [[ -f $LAST ]] && cp "$LAST" "$OUTD/W13-suite-mutants.txt"; NJIDS=$(nj "$LAST")
[[ -n $NJIDS ]] && { note "SM NOT-JUDGED other than P-0: $NJIDS"; phase NJSM; cp "$LAST" "$OUTD/W13-suite-mutants-rerun.txt"; }
phase W12
note "DRIVER-END | wt $(git -C "$WT" rev-parse --short HEAD) dirty $(git -C "$WT" status --porcelain | wc -l)"
DRV
echo "== drive.sh: bash -n $(bash -n "$T/drive.sh" 2>&1 && echo ok) | load $(cut -d' ' -f1-3 /proc/loadavg)"

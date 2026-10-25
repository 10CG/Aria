#!/usr/bin/env bash
# run-evidence.sh <work dir> [W8 W13 W11 W12 W9] : regenerates the v3.1 evidence. The baseline always comes from aria 59e333c (sha256 prefix e83c5e30f2cc,
# asserted); the hook under test is the prototype built by mkv31.py, or IMPL=<hook> (TASK-004: the real implementation; its sha256 must differ from the
# baseline's). Every output is written into the work dir first and copied to OUT only when its stage has finished, so a failed or partial run never
# overwrites committed evidence; OUT=<an existing directory> (TASK-004: v31/impl), default this script's directory, which reproduces the evidence of 95cf1de7.
# Every output's first line records the date, the platform, the sha256 prefixes of both hooks and of sc-cases.sh, sc-direct.sh and mutants.py (INV-8) and
# the load, taken before the stage's runs start; W9, W11, W12 and W13 write it again as their last line (the load at the end, INV-7). The W8 diff starts
# with that line too (patch and git apply skip the text before a diff), and so do the W12 TSVs (their readers skip the lines that start with #).
# Needs: Linux, bash 5 on PATH, jq, python3, taskset, nice; W13 and W12 also BASH32 (a bash 3.2 binary), W12 also TRAFFIC_DIR (the frozen corpus, outside the
# repo, with its cmds directory). A bash under test that is missing or not executable, W12 without TRAFFIC_DIR/cmds, an OUT that is not a writable
# directory, or a work dir that cannot be created exits 3 before any file is written.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; W=$(readlink -m "$1"); shift; STAGES=${*:-W8 W13 W11 W12 W9}; OUT=${OUT:-$HERE}
B13=(/home/dev/.aria/tools/bash-5.0.18/bash /home/dev/.aria/tools/bash-5.1.16/bash /usr/bin/bash /home/dev/.aria/tools/bash-5.3.20/bash)   # W13: one run each, then BASH32
NB=(); for st in $STAGES; do case $st in W13) NB+=("${B13[@]}" "${BASH32:-}");; W12) NB+=("${BASH32:-}" "$(command -v bash)");; W11|W9) NB+=("$(command -v bash)");; esac; done
for b in "${NB[@]}"; do [[ -n "$b" && -f "$b" && -x "$b" ]] || { echo "a bash under test is missing or not executable: '$b' (W13 and W12 need BASH32)"; exit 3; }; done
for st in $STAGES; do [[ $st != W12 || ( -n "${TRAFFIC_DIR:-}" && -d "${TRAFFIC_DIR:-}/cmds" ) ]] || { echo "W12 needs TRAFFIC_DIR, the frozen corpus with its cmds directory: '${TRAFFIC_DIR:-}'"; exit 3; }; done
for f in sc-cases.sh sc-direct.sh mutants.py; do [[ -f "$HERE/$f" ]] || { echo "missing $HERE/$f (its sha256 goes into every header, INV-8)"; exit 3; }; done
[[ -d "$OUT" && -w "$OUT" ]] || { echo "OUT is not a writable directory: $OUT"; exit 3; }
ROOT=$(git -C "$HERE" rev-parse --show-toplevel); [[ -n "$W" ]] && mkdir -p "$W" || { echo "cannot create the work dir: ${W:-<empty>}"; exit 3; }
git -C "$ROOT/aria" show 59e333c:hooks/secret-guard.sh > "$W/base.sh" && [[ "$(sha256sum < "$W/base.sh" | cut -c1-12)" == e83c5e30f2cc ]] || { echo "baseline: not e83c5e30f2cc"; exit 3; }
if [[ -n "${IMPL:-}" ]]; then cp "$IMPL" "$W/impl.sh"; else python3 "$HERE/mkv31.py" "$W/base.sh" "$W/impl.sh" >/dev/null || exit 3; fi
[[ "$(sha256sum < "$W/impl.sh")" != "$(sha256sum < "$W/base.sh")" ]] || { echo "the hook under test is the baseline itself"; exit 3; }
BS=$(sha256sum < "$W/base.sh" | cut -c1-12); IS=$(sha256sum < "$W/impl.sh" | cut -c1-12)
hdr() { printf '# %s | %s | bash %s | base sha256 %s | hook sha256 %s' "$(date -u +%FT%TZ)" "$(uname -sr)" "$BASH_VERSION" "$BS" "$IS"
  for f in sc-cases.sh sc-direct.sh mutants.py; do printf ' | %s sha256 %s' "$f" "$(sha256sum < "$HERE/$f" | cut -c1-12)"; done; printf ' | load %s\n' "$(cut -d' ' -f1-3 /proc/loadavg)"; }
N=(taskset -c 0,1 nice -n 19)
for st in $STAGES; do case $st in
W8) { hdr; diff -u "$W/base.sh" "$W/impl.sh" | sed '1,2s/\t.*//'; } > "$W/W8-v31.diff"
    printf 'added %s (blank %s) removed %s\n' "$(grep -c '^+[^+]' "$W/W8-v31.diff")" "$(grep -c '^+$' "$W/W8-v31.diff")" "$(grep -c '^-[^-]' "$W/W8-v31.diff")" > "$W/W8-count.txt"
    cp "$W/W8-v31.diff" "$OUT/"; echo "W8 done: $(cat "$W/W8-count.txt")" ;;
W13) { hdr; echo "## 1. the hook under test, one run per bash (SC_BASH); relaxation expected on GNU/Linux bash 5.0-5.3 only"
      for b in "${B13[@]}" "$BASH32"; do
        SC_BASH=$b bash "$HERE/sc-cases.sh" "$W/impl.sh" "$W/base.sh" > "$W/sc-$(basename "$(dirname "$b")").txt" 2>&1
        printf '%-28s %s | %s\n' "$("$b" -c 'echo bash $BASH_VERSION')" "$(tail -1 "$W/sc-$(basename "$(dirname "$b")").txt")" "$(head -1 "$W/sc-$(basename "$(dirname "$b")").txt" | grep -o 'relaxation expected: [a-z]*')"
        grep '^FAIL' "$W/sc-$(basename "$(dirname "$b")").txt"; done
      echo "## 2. the baseline as the hook under test (bash 5.2): the cases it fails are the baseline red set"
      SC_BASH=/usr/bin/bash bash "$HERE/sc-cases.sh" "$W/base.sh" "$W/base.sh" > "$W/sc-base.txt" 2>&1; tail -1 "$W/sc-base.txt"
      echo "  red:   $(awk '$1=="FAIL"{print $2}' "$W/sc-base.txt" | tr '\n' ' ')"
      echo "  green: $(awk '$1=="PASS"{print $2}' "$W/sc-base.txt" | tr '\n' ' ')"
      echo "## 3. the bad implementations of mutants.py (author-built: a self-check of the cases, not TASK-003), bash 5.2"
      SC_BASH=/usr/bin/bash bash "$HERE/run-mutants.sh" "$W/impl.sh" "$W/mut"; hdr; } > "$W/W13-sc-cases.txt" 2>&1
    cp "$W/W13-sc-cases.txt" "$OUT/"; echo "W13 done" ;;
W11) mkdir -p "$W/adv" "$W/ext/proj/.aria"; printf '%s\n' "billing/conf/prod.toml" > "$W/ext/proj/.aria/secret-guard.paths"
    for s in apply-heavy apply-heavy-seg apply-heavy-cjk shrink segfinding f5like km-ext km-ext-small; do python3 "$HERE/../v3/gen-v3.py" $s "$W/adv/$s.txt" >/dev/null; done
    L="apply-heavy apply-heavy-seg apply-heavy-cjk shrink segfinding f5like km-ext"
    { hdr; echo "# the adversarial shapes of v3 (../v3/gen-v3.py), one e2e call each, bash 5.2, LC_ALL=C.UTF-8 (the CJK shape depends on a multibyte locale)"
      for h in base impl; do echo "## $h"; ( cd "$W/adv" && LC_ALL=C.UTF-8 "${N[@]}" bash "$HERE/../v3/matrix.sh" "$W/$h.sh" $(for s in $L; do echo $s.txt; done) 2>&1 | grep -v setlocale ); done
      echo "# extension project (CLAUDE_PROJECT_DIR=<dir with .aria/secret-guard.paths listing the read path>)"
      for h in base impl; do echo "## $h"; ( cd "$W/adv" && EXTDIR="$W/ext/proj" LC_ALL=C.UTF-8 "${N[@]}" bash "$HERE/../v3/matrix.sh" "$W/$h.sh" km-ext.txt km-ext-small.txt 2>&1 | grep -v setlocale ); done
      hdr; } > "$W/W11-adversarial.txt"; cp "$W/W11-adversarial.txt" "$OUT/"; echo "W11 done" ;;
W12) : "${TRAFFIC_DIR:?W12 needs TRAFFIC_DIR}" "${BASH32:?W12 needs BASH32}"; W1="$HERE/../evidence/W1-classification.tsv"
    python3 "$HERE/mkdbg31.py" "$W/impl.sh" "$W/impl-dbg.sh" >/dev/null || exit 3
    H12=$(hdr)   # the first line of W12-real-traffic.txt and of the TSVs written beside it (INV-8)
    { printf '%s\n' "$H12"; echo "## 1. the W10 size-blocked class (W1: 138 commands; the baseline blocks all of them for size), the hook under test (instrumented copy), bash 5.2"
      "${N[@]}" bash "$HERE/replay138.sh" "$W/impl-dbg.sh" "$W1" "$W/W12-replay-138.rows" 2>&1 | grep -v setlocale
      { printf '%s\n' "$H12"; cat "$W/W12-replay-138.rows"; } > "$W/W12-replay-138.tsv"
      awk -F'\t' '/^#/{next} {c[$3]++} END{for (k in c) printf "  outcome %-10s %d\n", k, c[k]}' "$W/W12-replay-138.tsv" | sort
      awk -F'\t' 'NR==FNR{cls[$1]=$5; next} /^#/{next} {printf "  W1 class %-6s -> %s\n", cls[$1], $3}' "$W1" "$W/W12-replay-138.tsv" | sort | uniq -c
      awk -F'\t' '/^#/{next} $3=="allow"{print $4}' "$W/W12-replay-138.tsv" | sort -n | awk '{a[NR]=$1} END{printf "  allow wall (s): n=%d p50=%.2f p90=%.2f p99=%.2f max=%.2f\n", NR, a[int(NR*.5)], a[int(NR*.9)], a[int(NR*.99)], a[NR]}'
      awk -F'\t' '/^#/{next} {m++; t=($6=="-"?$4:$6); b=(t>3?t:3)+0.3; if ($4>b) {v++; printf "  OVER n=%s wall %.3f > bound %.3f\n", $1, $4, b}} END{printf "  every outcome within max(trigger, 3 s) + 0.3 s: %d of %d over the bound\n", v+0, m}' "$W/W12-replay-138.tsv"
      echo "## 1b. latency cost: the same 138 replayed on the baseline hook (replay138.sh fed base.sh: no probes, so no trigger time), aligned by n; extra = wall of the hook under test - wall of the baseline (s; p50 / p90 by nearest rank)"
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
      echo "## 2. outside the class: rc + sha256(stderr) of base vs the hook under test on 300 sampled commands (ident-300.lst), bash 5.2"
      "${N[@]}" bash "$HERE/ident.sh" "$W/base.sh" "$W/impl.sh" "$HERE/ident-300.lst" 2>&1 | grep -v setlocale | tail -3
      echo "## 3. bash 3.2 (no relaxation): base vs the hook under test on 40 sampled W1 commands (w1-sample40.lst)"
      "${N[@]}" bash "$HERE/ident32.sh" "$BASH32" "$W/base.sh" "$W/impl.sh" "$HERE/w1-sample40.lst" 2>&1 | grep -v setlocale | tail -3
      hdr; } > "$W/W12-real-traffic.txt"; cp "$W/W12-real-traffic.txt" "$W/W12-replay-138.tsv" "$W/W12-replay-138-base.tsv" "$W/W12-ident-138.txt" "$OUT/"; echo "W12 done" ;;
W9) HK="$W/hooks-base"; rm -rf "$HK"; git -C "$ROOT/aria" archive 59e333c hooks | tar -x -C "$W" --transform 's,^hooks,hooks-base,'
    [[ "$(sha256sum < "$HK/secret-guard.sh" | cut -c1-12)" == e83c5e30f2cc ]] || { echo "W9: archived hook is not the baseline"; exit 3; }
    for t in base impl; do rm -rf "$W/tree-$t"; mkdir -p "$W/tree-$t"; cp -r "$HK" "$W/tree-$t/hooks"; done; cp "$W/impl.sh" "$W/tree-impl/hooks/secret-guard.sh"
    H9=$(hdr)   # before the two suite runs: the first line carries the load at the start, the last line (hdr below) the load at the end (INV-7)
    for t in base impl; do "${N[@]}" bash "$W/tree-$t/hooks/tests/secret-guard.test.sh" > "$W/suite-$t.out" 2>&1; done
    { printf '%s\n' "$H9"; echo "# the suite of aria 59e333c run on a copy with the baseline hook and on a copy with the hook under test (not git checkouts: the cases that read an old hook through git show do not run in either)"
      for t in base impl; do echo "## $t"; grep -E '^(PASS|FAIL):' "$W/suite-$t.out"
        grep -E '^  FAIL \[' "$W/suite-$t.out" | python3 -c '
import sys, re
for ln in sys.stdin:
    m = re.match(r"  FAIL \[(.*?)\]: (.*)", ln.rstrip("\n"))
    name, body = m.group(1), m.group(2)
    print("  FAIL", name[:110])
    for chk in re.findall(r"\{(.*?)\}(?= \{|$)", body):
        chk = re.sub(r"\[[^\]]*\]", "[...]", chk, count=1)
        print("     ", chk[:220])
    if not body.startswith(tuple("0123456789")): print("     ", re.sub(r"\[[^\]]*\]", "[...]", body)[:220])
'; done; hdr; } > "$W/W9-suite.txt"; cp "$W/W9-suite.txt" "$OUT/"; echo "W9 done" ;;
*) echo "unknown stage $st"; exit 2 ;;
esac; done

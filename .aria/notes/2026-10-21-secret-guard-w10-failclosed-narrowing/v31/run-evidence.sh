#!/usr/bin/env bash
# run-evidence.sh <work dir> [W8 W13 W11 W12 W9] : regenerates the v3.1 evidence. The baseline always comes from aria 59e333c (sha256 prefix e83c5e30f2cc,
# asserted); the hook under test is the prototype built by mkv31.py, or IMPL=<hook> (TASK-004: the real implementation; its sha256 must differ from the
# baseline's). Every output is written into the work dir first and copied next to this script only when its stage has finished, so a failed or partial run
# never overwrites committed evidence. Every output's first line records the date, the platform, both sha256 prefixes and the load.
# Needs: Linux, bash 5 on PATH, jq, python3, taskset, nice; W12 also TRAFFIC_DIR (the frozen corpus, outside the repo) and BASH32 (a bash 3.2 binary).
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; W=$(readlink -f "$1"); shift; STAGES=${*:-W8 W13 W11 W12 W9}
ROOT=$(git -C "$HERE" rev-parse --show-toplevel); mkdir -p "$W"
git -C "$ROOT/aria" show 59e333c:hooks/secret-guard.sh > "$W/base.sh" && [[ "$(sha256sum < "$W/base.sh" | cut -c1-12)" == e83c5e30f2cc ]] || { echo "baseline: not e83c5e30f2cc"; exit 3; }
if [[ -n "${IMPL:-}" ]]; then cp "$IMPL" "$W/impl.sh"; else python3 "$HERE/mkv31.py" "$W/base.sh" "$W/impl.sh" >/dev/null || exit 3; fi
[[ "$(sha256sum < "$W/impl.sh")" != "$(sha256sum < "$W/base.sh")" ]] || { echo "the hook under test is the baseline itself"; exit 3; }
BS=$(sha256sum < "$W/base.sh" | cut -c1-12); IS=$(sha256sum < "$W/impl.sh" | cut -c1-12)
hdr() { printf '# %s | %s | bash %s | base sha256 %s | hook sha256 %s | load %s\n' "$(date -u +%FT%TZ)" "$(uname -sr)" "$BASH_VERSION" "$BS" "$IS" "$(cut -d' ' -f1-3 /proc/loadavg)"; }
N=(taskset -c 0,1 nice -n 19)
for st in $STAGES; do case $st in
W8) diff -u "$W/base.sh" "$W/impl.sh" | sed '1,2s/\t.*//' > "$W/W8-v31.diff"
    printf 'added %s (blank %s) removed %s\n' "$(grep -c '^+[^+]' "$W/W8-v31.diff")" "$(grep -c '^+$' "$W/W8-v31.diff")" "$(grep -c '^-[^-]' "$W/W8-v31.diff")" > "$W/W8-count.txt"
    cp "$W/W8-v31.diff" "$HERE/"; echo "W8 done: $(cat "$W/W8-count.txt")" ;;
W13) { hdr; echo "## 1. the hook under test, one run per bash (SC_BASH); relaxation expected on GNU/Linux bash 5.0-5.3 only"
      for b in /home/dev/.aria/tools/bash-5.0.18/bash /home/dev/.aria/tools/bash-5.1.16/bash /usr/bin/bash /home/dev/.aria/tools/bash-5.3.20/bash ${BASH32:-}; do
        SC_BASH=$b bash "$HERE/sc-cases.sh" "$W/impl.sh" "$W/base.sh" > "$W/sc-$(basename "$(dirname "$b")").txt" 2>&1
        printf '%-28s %s | %s\n' "$("$b" -c 'echo bash $BASH_VERSION')" "$(tail -1 "$W/sc-$(basename "$(dirname "$b")").txt")" "$(head -1 "$W/sc-$(basename "$(dirname "$b")").txt" | grep -o 'relaxation expected: [a-z]*')"
        grep '^FAIL' "$W/sc-$(basename "$(dirname "$b")").txt"; done
      echo "## 2. the baseline as the hook under test (bash 5.2): the cases it fails are the baseline red set"
      SC_BASH=/usr/bin/bash bash "$HERE/sc-cases.sh" "$W/base.sh" "$W/base.sh" > "$W/sc-base.txt" 2>&1; tail -1 "$W/sc-base.txt"
      echo "  red:   $(awk '$1=="FAIL"{print $2}' "$W/sc-base.txt" | tr '\n' ' ')"
      echo "  green: $(awk '$1=="PASS"{print $2}' "$W/sc-base.txt" | tr '\n' ' ')"
      echo "## 3. the bad implementations of mutants.py (author-built: a self-check of the cases, not TASK-003), bash 5.2"
      SC_BASH=/usr/bin/bash bash "$HERE/run-mutants.sh" "$W/impl.sh" "$W/mut"; hdr; } > "$W/W13-sc-cases.txt" 2>&1
    cp "$W/W13-sc-cases.txt" "$HERE/"; echo "W13 done" ;;
W11) mkdir -p "$W/adv" "$W/ext/proj/.aria"; printf '%s\n' "billing/conf/prod.toml" > "$W/ext/proj/.aria/secret-guard.paths"
    for s in apply-heavy apply-heavy-seg apply-heavy-cjk shrink segfinding f5like km-ext km-ext-small; do python3 "$HERE/../v3/gen-v3.py" $s "$W/adv/$s.txt" >/dev/null; done
    L="apply-heavy apply-heavy-seg apply-heavy-cjk shrink segfinding f5like km-ext"
    { hdr; echo "# the adversarial shapes of v3 (../v3/gen-v3.py), one e2e call each, bash 5.2, LC_ALL=C.UTF-8 (the CJK shape depends on a multibyte locale)"
      for h in base impl; do echo "## $h"; ( cd "$W/adv" && LC_ALL=C.UTF-8 "${N[@]}" bash "$HERE/../v3/matrix.sh" "$W/$h.sh" $(for s in $L; do echo $s.txt; done) 2>&1 | grep -v setlocale ); done
      echo "# extension project (CLAUDE_PROJECT_DIR=<dir with .aria/secret-guard.paths listing the read path>)"
      for h in base impl; do echo "## $h"; ( cd "$W/adv" && EXTDIR="$W/ext/proj" LC_ALL=C.UTF-8 "${N[@]}" bash "$HERE/../v3/matrix.sh" "$W/$h.sh" km-ext.txt km-ext-small.txt 2>&1 | grep -v setlocale ); done
      hdr; } > "$W/W11-adversarial.txt"; cp "$W/W11-adversarial.txt" "$HERE/"; echo "W11 done" ;;
W12) : "${TRAFFIC_DIR:?W12 needs TRAFFIC_DIR}" "${BASH32:?W12 needs BASH32}"; W1="$HERE/../evidence/W1-classification.tsv"
    python3 "$HERE/mkdbg31.py" "$W/impl.sh" "$W/impl-dbg.sh" >/dev/null || exit 3
    { hdr; echo "## 1. the W10 size-blocked class (W1: 138 commands; the baseline blocks all of them for size), the hook under test (instrumented copy), bash 5.2"
      "${N[@]}" bash "$HERE/replay138.sh" "$W/impl-dbg.sh" "$W1" "$W/W12-replay-138.tsv" 2>&1 | grep -v setlocale
      awk -F'\t' '{c[$3]++} END{for (k in c) printf "  outcome %-10s %d\n", k, c[k]}' "$W/W12-replay-138.tsv" | sort
      awk -F'\t' 'NR==FNR{cls[$1]=$5; next} {printf "  W1 class %-6s -> %s\n", cls[$1], $3}' "$W1" "$W/W12-replay-138.tsv" | sort | uniq -c
      awk -F'\t' '$3=="allow"{print $4}' "$W/W12-replay-138.tsv" | sort -n | awk '{a[NR]=$1} END{printf "  allow wall (s): n=%d p50=%.2f p90=%.2f p99=%.2f max=%.2f\n", NR, a[int(NR*.5)], a[int(NR*.9)], a[int(NR*.99)], a[NR]}'
      awk -F'\t' '{t=($6=="-"?$4:$6); b=(t>3?t:3)+0.3; if ($4>b) {v++; printf "  OVER n=%s wall %.3f > bound %.3f\n", $1, $4, b}} END{printf "  every outcome within max(trigger, 3 s) + 0.3 s: %d of %d over the bound\n", v+0, NR}' "$W/W12-replay-138.tsv"
      echo "## 2. outside the class: rc + sha256(stderr) of base vs the hook under test on 300 sampled commands (ident-300.lst), bash 5.2"
      "${N[@]}" bash "$HERE/ident.sh" "$W/base.sh" "$W/impl.sh" "$HERE/ident-300.lst" 2>&1 | grep -v setlocale | tail -3
      echo "## 3. bash 3.2 (no relaxation): base vs the hook under test on 40 sampled W1 commands (w1-sample40.lst)"
      "${N[@]}" bash "$HERE/ident32.sh" "$BASH32" "$W/base.sh" "$W/impl.sh" "$HERE/w1-sample40.lst" 2>&1 | grep -v setlocale | tail -3
      hdr; } > "$W/W12-real-traffic.txt"; cp "$W/W12-real-traffic.txt" "$W/W12-replay-138.tsv" "$HERE/"; echo "W12 done" ;;
W9) HK="$W/hooks-base"; rm -rf "$HK"; git -C "$ROOT/aria" archive 59e333c hooks | tar -x -C "$W" --transform 's,^hooks,hooks-base,'
    [[ "$(sha256sum < "$HK/secret-guard.sh" | cut -c1-12)" == e83c5e30f2cc ]] || { echo "W9: archived hook is not the baseline"; exit 3; }
    for t in base impl; do rm -rf "$W/tree-$t"; mkdir -p "$W/tree-$t"; cp -r "$HK" "$W/tree-$t/hooks"; done; cp "$W/impl.sh" "$W/tree-impl/hooks/secret-guard.sh"
    for t in base impl; do "${N[@]}" bash "$W/tree-$t/hooks/tests/secret-guard.test.sh" > "$W/suite-$t.out" 2>&1; done
    { hdr; echo "# the suite of aria 59e333c run on a copy with the baseline hook and on a copy with the hook under test (not git checkouts: the cases that read an old hook through git show do not run in either)"
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
'; done; hdr; } > "$W/W9-suite.txt"; cp "$W/W9-suite.txt" "$HERE/"; echo "W9 done" ;;
*) echo "unknown stage $st"; exit 2 ;;
esac; done

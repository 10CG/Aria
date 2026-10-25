#!/bin/bash
# prove5f3.sh (10CG/aria-plugin#217, TASK-005 fix round part 3): bad implementations and the "can go red" runs of the new and changed cases (perf case
# excluded: runall3.sh runs it alone); the four test-side WSL criteria against the hook's function on the controller's 12 cases (5 bashes); mutant
# generation; commentsync re-export and its 7 runs. When every result is as predicted (expect.md), runall3.sh is started detached and its PID recorded.
set -u
S=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad; O=$S/r217impl/t005f3; WT=$S/wt217/aria; P=$S/r217impl/spec-probe2
V=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31; H=$WT/hooks/secret-guard.sh
HL=$WT/hooks/tests/lib/secret-guard-w10-direct.sh; ST=$WT/hooks/tests/secret-guard.test.sh
T=(taskset -c 0,1 nice -n 19)
B="/home/dev/.aria/tools/bash-3.2.57/bash /home/dev/.aria/tools/bash-5.0.18/bash /home/dev/.aria/tools/bash-5.1.16/bash /usr/bin/bash /home/dev/.aria/tools/bash-5.3.20/bash"
mkdir -p $O/proofs $O/home $O/tw $O/bad $O/cs $O/gen-v31 $O/gen-w14
ok=yes; nope() { ok=no; echo "UNEXPECTED: $*"; }
echo "load0 $(cut -d' ' -f1-3 /proc/loadavg)"

# 1. bad implementations (scratchpad only)
python3 - "$H" "$O" "$P" > $O/mkbad.out 2>&1 <<'EOF'
import sys
H, O, P = sys.argv[1:4]
t = open(H, encoding='utf-8', newline='').read(); pre = open(O + '/pre/hook-secret-guard.sh', encoding='utf-8', newline='').read()
def fn(x):
    i = x.index('\n_sg_relax_nowslfs() {') + 1; return i, x.index('\n_sg_relax_noext() {', i) + 1
i, j = fn(t); pi, pj = fn(pre); old = pre[pi:pj]
print('v3.3 function of the pre hook == spec-probe2/old.sh:', old == open(P + '/old.sh', encoding='utf-8').read())
one = lambda s: [x + '\n' for x in t.split('\n') if x.startswith(s)]
L2 = one('  _sg_relax_nowslfs || return 1'); XL = one('  [[ -x "$d" ]] || return 1'); ENV = one('  [[ -n "${WSL_DISTRO_NAME:-}${WSL_INTEROP:-}" ]] && wsl=wsl')
assert len(L2) == len(XL) == len(ENV) == 1; L2, XL, ENV = L2[0], XL[0], ENV[0]
V33 = '  [[ -n "$wsl" ]] || _sg_relax_nowslfs || wsl=wsl   # a WSLInterop* entry under a mounted binfmt_misc, or a mount table that cannot be read\n'
B = {'v33fn': t[:i] + old + t[j:], 'nox': t.replace(XL, '', 1), 'order': t.replace(L2, '', 1).replace(ENV, ENV + V33, 1),
     'w1e-a': t.replace(L2, '', 1), 'w1e-b': t.replace(L2, '  ! ' + L2[2:], 1)}
for k, v in B.items():
    assert v != t; open(O + '/bad/hook-' + k + '.sh', 'w', encoding='utf-8', newline='').write(v)
print('built', ' '.join(sorted(B)))
EOF
echo "mkbad rc=$? $(tr '\n' ' ' < $O/mkbad.out)"

# 2. "can go red": the W1 cases on PATH bash (5.2, MODE relax) against the target and each bad implementation; FAIL letters must equal the prediction
fails() { grep '^FAIL V15-W1' "$1" | awk '{print substr($2,7,1)}' | sort | tr -d '\n'; }
for kv in good: v33fn:fghijkl nox:k order:m w1e-a:em w1e-b:e; do
  k=${kv%%:*}; want=${kv#*:}; hk=$H; [[ $k == good ]] || hk=$O/bad/hook-$k.sh
  HOME=$O/home SC_ONLY='^V15-W1[a-m]' "${T[@]}" /usr/bin/bash $HL $hk relax > $O/proofs/$k.txt 2>&1
  got=$(fails $O/proofs/$k.txt); np=$(grep -c '^PASS V15-W1' $O/proofs/$k.txt); nm=$(grep -c -E '^(MISSING|SETUP|SKIP) V15-W1' $O/proofs/$k.txt)
  printf '%-6s FAIL [%s] (want [%s]) PASS %s other %s | %s\n' "$k" "$got" "$want" "$np" "$nm" \
    "$(grep '^FAIL V15-W1' $O/proofs/$k.txt | awk '{t=""; for (i = NF; i > 0 && $i ~ /^\[/; i--) t = $i " " t; printf "%s:%s ", substr($2,7,1), t}')"
  [[ $got == "$want" && $nm == 0 && $((np + ${#got})) == 13 ]] || nope "proof $k"
done

# 3. the test-side criteria (helper, sc-direct.sh, suite, sc-cases.sh) against the hook's _sg_relax_nowslfs, the controller's 12 cases, 5 bashes
awk '/^wslmark\(\) \{/,/^\}$/' $HL | sed 's/^wslmark()/tw_helper()/' > $O/tw/tw-helper.sh
awk '/^wslmark\(\) \{/,/^\}$/' $V/sc-direct.sh | sed 's/^wslmark()/tw_scdirect()/' > $O/tw/tw-scdirect.sh
awk '/^sg_w10_wslfs\(\) \{/,/^\}$/' $ST | sed 's/^sg_w10_wslfs()/tw_suite()/' > $O/tw/tw-suite.sh
awk '/^wslmark\(\) \{/,/^\}$/' $V/sc-cases.sh | sed 's/^wslmark()/tw_sccases()/' > $O/tw/tw-sccases.sh
cat > $O/cmp5f3.sh <<'EOF'
H=$1; P=$2; TW=$3; D=$P/fx; cd "$P" || exit 3
source "$H" </dev/null >/dev/null 2>&1; set +e +u
for f in "$TW"/tw-*.sh; do source "$f"; done
n=0; bad=0
c() {   # NAME WANT OPT [MOUNTS DIR] : the hook's function and the four test-side criteria under OPT ('-' = none); a test side must say the opposite
  local nm=$1 w=$2 o=$3 hs e k ts r='' st=ok; shift 3
  hs=$( [[ $o == - ]] || eval "$o"; _sg_relax_nowslfs "$@" 2>"$TW/err"; echo $? ); e=$(wc -c < "$TW/err")
  [[ $hs == "$w" && $e == 0 ]] || st=WANT-MISMATCH
  for k in helper scdirect suite sccases; do
    ts=$( [[ $o == - ]] || eval "$o"; tw_$k "$@" 2>/dev/null; echo $? ); r+=" $k=$ts"
    [[ $ts == $(( 1 - hs )) ]] || st=MISMATCH
  done
  n=$((n + 1)); [[ $st == ok ]] || bad=$((bad + 1))
  printf '%-20s hook=%s (want %s) stderr=%s |%s  %s\n' "$nm" "$hs" "$w" "$e" "$r" "$st"
}
c host 0 -
c autofs+WSLInterop 0 - t-autofs "$D/wsl"
c binfmt+late 1 - t-late "$D/late"
c binfmt+none 0 - t-none "$D/none"
c stacked+WSLInterop 0 - t-stacked "$D/wsl"
c empty 1 - t-empty "$D/wsl"
c unreadable 1 - /nonexistent/x "$D/wsl"
c dir-as-table 1 - "$D" "$D/wsl"
c noglob+late 1 'set -f' t-late "$D/late"
c failglob+none 0 'shopt -s failglob' t-none "$D/none"
c nosearch-000 1 - t-nosearch "$D/nosearch"
c listless-0311+late 1 - t-listless "$D/listless"
echo "# ${BASH_VERSION%%(*}: $n cases, $bad not ok"
EOF
for b in $B; do
  v=$($b -c 'echo ${BASH_VERSINFO[0]}.${BASH_VERSINFO[1]}.${BASH_VERSINFO[2]}')
  "${T[@]}" $b $O/cmp5f3.sh $H $P $O/tw > $O/proofs/cmp-$v.txt 2>&1; echo "cmp $v: $(tail -1 $O/proofs/cmp-$v.txt)"
  grep -q ': 12 cases, 0 not ok$' $O/proofs/cmp-$v.txt || nope "cmp $v"
done

# 4. mutant generation on the new hook (every anchor must still apply)
python3 -I $V/mutants.py $H $O/gen-v31 > $O/gen-v31.out 2>&1; r=$?; echo "gen v31 rc=$r $(tail -1 $O/gen-v31.out | cut -c1-140)"; [[ $r == 0 ]] || nope "gen v31"
python3 -I $V/impl/w14-mutants.py $H $O/gen-w14 > $O/gen-w14.out 2>&1; r=$?; echo "gen w14 rc=$r lines $(grep -c '' $O/gen-w14.out) $(tail -1 $O/gen-w14.out | cut -c1-100)"; [[ $r == 0 ]] || nope "gen w14"

# 5. commentsync: re-export from the pre-derive version (eeb67786) with t005f/cs/derive-5f.py, then target / baseline / proto and the four constructions
VR=.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31; D2=$S/r217impl/t005f2/cs; CS=$O/cs
[[ -f $O/pre/commentsync-commentsync.py ]] || cp $V/commentsync.py $O/pre/commentsync-commentsync.py
git -C /home/dev/Aria show eeb67786:$VR/commentsync.py > $CS/commentsync-base.py; cp $CS/commentsync-base.py $CS/commentsync-5f3.py
python3 $S/r217impl/t005f/cs/derive-5f.py $CS/commentsync-5f3.py $D2 $H $ST > $CS/derive.out 2>&1; r=$?; echo "derive rc=$r $(head -1 $CS/derive.out | cut -c1-160)"; [[ $r == 0 ]] || nope derive
diff $O/pre/commentsync-commentsync.py $CS/commentsync-5f3.py > $CS/commentsync-5f2-vs-5f3.diff; echo "commentsync 5f2 -> 5f3: $(grep -c '^[<>]' $CS/commentsync-5f2-vs-5f3.diff) diff lines"
cp $CS/commentsync-5f3.py $V/commentsync.py
cp $D2/hook-59e333c.sh $D2/suite-59e333c.sh $CS/; python3 $S/r217impl/t005f/cs/constr.py $V/commentsync.py $CS > $CS/constr.out 2>&1; echo "constr: $(tr '\n' ' ' < $CS/constr.out)"
cs() { local n=$1 w=$2; shift 2; python3 $V/commentsync.py "$@" > $CS/o-$n.txt 2>&1; echo "cs $n rc=$? $(tail -1 $CS/o-$n.txt)"; tail -1 $CS/o-$n.txt | grep -q "$w" || nope "cs $n"; }
cs target GREEN $H $ST target; cs baseline GREEN $D2/hook-59e333c.sh $D2/suite-59e333c.sh baseline; cs proto GREEN --hook-only $D2/hook-proto.sh proto
cs hook-c1-insert RED --hook-only $CS/hook-c1-insert.sh target; cs hook-c2-delete RED --hook-only $CS/hook-c2-delete.sh target
cs suite-c1-insert RED --suite-only $CS/suite-c1-insert.sh target; cs suite-c2-delete RED --suite-only $CS/suite-c2-delete.sh target

echo "load1 $(cut -d' ' -f1-3 /proc/loadavg)"
if [[ $ok == yes ]]; then
  mkdir -p $O/runs; setsid nohup bash $O/runall3.sh > $O/runs/runall3.log 2>&1 < /dev/null & echo "runall3 started, pid $!"; echo $! > $O/runs/runall3.launch.pid
else echo "runall3 NOT started"; fi

#!/bin/bash
# prove5f4.sh (10CG/aria-plugin#217, TASK-005 fix round part 4): bash -n; bad implementations and the "can go red" / "can SKIP" runs of the new and
# changed cases (W1o, W1l, W1n); the four test-side WSL criteria against the hook's function on the controller's 13 cases (5 bashes); mutant generation;
# commentsync re-export and its 7 runs. Starts when the one-minute load is below 1.2. When every result is as predicted (expect.md), runall4.sh is started.
set -u
S=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad; O=$S/r217impl/t005f4; WT=$S/wt217/aria; P=$S/r217impl/spec-probe2
V=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31; H=$WT/hooks/secret-guard.sh
HL=$WT/hooks/tests/lib/secret-guard-w10-direct.sh; ST=$WT/hooks/tests/secret-guard.test.sh
T=(taskset -c 0,1 nice -n 19)
B="/home/dev/.aria/tools/bash-3.2.57/bash /home/dev/.aria/tools/bash-5.0.18/bash /home/dev/.aria/tools/bash-5.1.16/bash /usr/bin/bash /home/dev/.aria/tools/bash-5.3.20/bash"
mkdir -p $O/proofs $O/home $O/tw $O/bad $O/cs $O/gen-v31 $O/gen-w14 $O/mnt
ok=yes; nope() { ok=no; echo "UNEXPECTED: $*"; }
for i in $(seq 1 180); do awk '{exit !($1 < 1.2)}' /proc/loadavg && break; sleep 10; done
echo "load0 $(cut -d' ' -f1-3 /proc/loadavg) (waited $i x 10 s at most)"

# 0. bash -n: 5 bashes x 5 files
: > $O/bash-n.err; for b in $B; do for f in $H $HL $ST $V/sc-direct.sh $V/sc-cases.sh; do $b -n $f 2>>$O/bash-n.err || nope "bash -n $b $f"; done; done
echo "bash -n: 25 checks, stderr $(wc -c < $O/bash-n.err) bytes"

# 1. bad implementations (scratchpad only): v34fn = the v3.4 function (spec-probe2/spec3.sh); v33fn = the v3.3 function (old.sh, for the perf case);
#    nodx = the -d/-x line dropped; donly = -d kept, -x dropped
python3 - "$H" "$O" "$P" > $O/mkbad.out 2>&1 <<'EOF'
import sys
H, O, P = sys.argv[1:4]
t = open(H, encoding='utf-8', newline='').read()
i = t.index('\n_sg_relax_nowslfs() {') + 1; j = t.index('\n}\n', i) + 3
v34 = open(P + '/spec3.sh', encoding='utf-8').read(); v33 = open(P + '/old.sh', encoding='utf-8').read()
assert v34.endswith('\n}\n') and v33.endswith('\n}\n')
DX = [x + '\n' for x in t.split('\n') if x.startswith('  [[ -d "$d" && -x "$d" ]] || return 1')]
assert len(DX) == 1; DX = DX[0]
B = {'v34fn': t[:i] + v34 + t[j:], 'v33fn': t[:i] + v33 + t[j:], 'nodx': t.replace(DX, '', 1), 'donly': t.replace(DX, '  [[ -d "$d" ]] || return 1\n', 1)}
for k, v in B.items():
    assert v != t; open(O + '/bad/hook-' + k + '.sh', 'w', encoding='utf-8', newline='').write(v)
print('built', ' '.join(sorted(B)))
EOF
echo "mkbad rc=$? $(tr '\n' ' ' < $O/mkbad.out)"

# 2. "can go red": the W1 cases (W1a-m, W1o) on PATH bash (5.2, MODE relax) against the target and each bad implementation; FAIL letters must equal the
#    prediction. Then W1o in MODE norelax on 3.2.57 (both modes run it)
fails() { grep '^FAIL V15-W1' "$1" | awk '{print substr($2,7,1)}' | sort | tr -d '\n'; }
for kv in good: v34fn:o nodx:ko donly:k; do
  k=${kv%%:*}; want=${kv#*:}; hk=$H; [[ $k == good ]] || hk=$O/bad/hook-$k.sh
  HOME=$O/home SC_ONLY='^V15-W1[a-mo]-' "${T[@]}" /usr/bin/bash $HL $hk relax > $O/proofs/$k.txt 2>&1
  got=$(fails $O/proofs/$k.txt); np=$(grep -c '^PASS V15-W1' $O/proofs/$k.txt); nm=$(grep -c -E '^(MISSING|SETUP|SKIP) V15-W1' $O/proofs/$k.txt)
  printf '%-6s FAIL [%s] (want [%s]) PASS %s other %s | %s\n' "$k" "$got" "$want" "$np" "$nm" "$(grep '^FAIL V15-W1' $O/proofs/$k.txt | cut -c1-150 | tr '\n' ' ')"
  [[ $got == "$want" && $nm == 0 && $((np + ${#got})) == 14 ]] || nope "proof $k"
done
for kv in good:PASS v34fn:FAIL; do
  k=${kv%%:*}; want=${kv#*:}; hk=$H; [[ $k == good ]] || hk=$O/bad/hook-$k.sh
  HOME=$O/home SC_ONLY='^V15-W1o-' "${T[@]}" /home/dev/.aria/tools/bash-3.2.57/bash $HL $hk norelax > $O/proofs/norelax-$k.txt 2>&1
  echo "norelax 3.2.57 $k (want $want): $(grep 'V15-W1o' $O/proofs/norelax-$k.txt | cut -c1-200)"
  grep -q "^$want V15-W1o-regular-file-as-directory " $O/proofs/norelax-$k.txt || nope "norelax $k"
done

# 3. W1n: a mount wrapper ahead on PATH that fails from call FROM on (as a low fs.mount-max would). Target helper: SKIP [platform] for 500 and for 0
#    mounts; the pre-5f4 helper with 500 mounts: TIMED with the hard part bad (FAIL in the suite) -- the judgement this round changes
cat > $O/mnt/mount <<'EOF'
#!/bin/bash
# test double (scratchpad only): the real mount until call MOUNT_FAIL_FROM - 1, then status 32
c=$(( $(cat "${MOUNT_COUNT_FILE:?}" 2>/dev/null || echo 0) + 1 )); echo "$c" > "$MOUNT_COUNT_FILE"
(( c < ${MOUNT_FAIL_FROM:?} )) || { echo "mount: test double refuses call $c" >&2; exit 32; }
exec /usr/bin/mount "$@"
EOF
chmod 755 $O/mnt/mount
w1n() { local n=$1 from=$2 hl=$3; rm -f $O/mnt/count
  HOME=$O/home PATH="$O/mnt:$PATH" MOUNT_COUNT_FILE=$O/mnt/count MOUNT_FAIL_FROM=$from SC_ONLY='^V15-W1n-' "${T[@]}" /usr/bin/bash $hl $H relax > $O/proofs/w1n-$n.txt 2>&1
  echo "w1n $n (fails from call $from; calls made $(cat $O/mnt/count 2>/dev/null)): $(grep 'V15-W1n' $O/proofs/w1n-$n.txt | cut -c1-260)"; }
w1n stop501 501 $HL; grep -q '^SKIP V15-W1n-mount-table-read-in-one-pass \[platform\] the stacking stopped after 500 ' $O/proofs/w1n-stop501.txt || nope "w1n stop501"
w1n stop1 1 $HL; grep -q '^SKIP V15-W1n-mount-table-read-in-one-pass \[platform\] tmpfs cannot be mounted' $O/proofs/w1n-stop1.txt || nope "w1n stop1"
w1n pre-stop501 501 $O/pre/helper-secret-guard-w10-direct.sh; grep -q '^TIMED V15-W1n-mount-table-read-in-one-pass bad ' $O/proofs/w1n-pre-stop501.txt || nope "w1n pre-stop501"

# 4. the four test-side criteria (helper, sc-direct.sh, suite, sc-cases.sh) against the hook's _sg_relax_nowslfs, the controller's 13 cases, 5 bashes
awk '/^wslmark\(\) \{/,/^\}$/' $HL | sed 's/^wslmark()/tw_helper()/' > $O/tw/tw-helper.sh
awk '/^wslmark\(\) \{/,/^\}$/' $V/sc-direct.sh | sed 's/^wslmark()/tw_scdirect()/' > $O/tw/tw-scdirect.sh
awk '/^sg_w10_wslfs\(\) \{/,/^\}$/' $ST | sed 's/^sg_w10_wslfs()/tw_suite()/' > $O/tw/tw-suite.sh
awk '/^wslmark\(\) \{/,/^\}$/' $V/sc-cases.sh | sed 's/^wslmark()/tw_sccases()/' > $O/tw/tw-sccases.sh
for f in helper scdirect suite sccases; do cmp -s $O/tw/tw-$f.sh $S/r217impl/t005f3/tw/tw-$f.sh && echo "tw-$f: same as in 5f3 ($(grep -c '' $O/tw/tw-$f.sh) lines)" || nope "tw-$f differs from 5f3"; done
for b in $B; do
  v=$($b $O/ver.sh)
  "${T[@]}" $b $O/cmp5f4.sh $H $P $O/tw > $O/proofs/cmp-$v.txt 2>&1; echo "cmp $v: $(tail -1 $O/proofs/cmp-$v.txt)"
  grep -q ': 13 cases, 0 not ok$' $O/proofs/cmp-$v.txt || nope "cmp $v"
done

# 5. mutant generation on the new hook (every anchor must still apply)
python3 -I $V/mutants.py $H $O/gen-v31 > $O/gen-v31.out 2>&1; r=$?; echo "gen v31 rc=$r $(tail -1 $O/gen-v31.out | cut -c1-140)"; [[ $r == 0 ]] || nope "gen v31"
python3 -I $V/impl/w14-mutants.py $H $O/gen-w14 > $O/gen-w14.out 2>&1; r=$?; echo "gen w14 rc=$r lines $(grep -c '' $O/gen-w14.out) $(tail -1 $O/gen-w14.out | cut -c1-100)"; [[ $r == 0 ]] || nope "gen w14"

# 6. commentsync: re-export from eeb67786 with t005f/cs/derive-5f.py (as in 5f, 5f2, 5f3), then target / baseline / proto and the four constructions
VR=.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31; D2=$S/r217impl/t005f2/cs; CS=$O/cs
[[ -f $O/pre/commentsync-commentsync.py ]] || cp $V/commentsync.py $O/pre/commentsync-commentsync.py
git -C /home/dev/Aria show eeb67786:$VR/commentsync.py > $CS/commentsync-base.py; cp $CS/commentsync-base.py $CS/commentsync-5f4.py
python3 $S/r217impl/t005f/cs/derive-5f.py $CS/commentsync-5f4.py $D2 $H $ST > $CS/derive.out 2>&1; r=$?; echo "derive rc=$r $(head -1 $CS/derive.out | cut -c1-160)"; [[ $r == 0 ]] || nope derive
diff $O/pre/commentsync-commentsync.py $CS/commentsync-5f4.py > $CS/commentsync-5f3-vs-5f4.diff; echo "commentsync 5f3 -> 5f4: $(grep -c '^[<>]' $CS/commentsync-5f3-vs-5f4.diff) diff lines"
cp $CS/commentsync-5f4.py $V/commentsync.py
cp $D2/hook-59e333c.sh $D2/suite-59e333c.sh $CS/; python3 $S/r217impl/t005f/cs/constr.py $V/commentsync.py $CS > $CS/constr.out 2>&1; echo "constr: $(tr '\n' ' ' < $CS/constr.out)"
cs() { local n=$1 w=$2; shift 2; python3 $V/commentsync.py "$@" > $CS/o-$n.txt 2>&1; echo "cs $n rc=$? $(tail -1 $CS/o-$n.txt)"; tail -1 $CS/o-$n.txt | grep -q "$w" || nope "cs $n"; }
cs target GREEN $H $ST target; cs baseline GREEN $D2/hook-59e333c.sh $D2/suite-59e333c.sh baseline; cs proto GREEN --hook-only $D2/hook-proto.sh proto
cs hook-c1-insert RED --hook-only $CS/hook-c1-insert.sh target; cs hook-c2-delete RED --hook-only $CS/hook-c2-delete.sh target
cs suite-c1-insert RED --suite-only $CS/suite-c1-insert.sh target; cs suite-c2-delete RED --suite-only $CS/suite-c2-delete.sh target

echo "load1 $(cut -d' ' -f1-3 /proc/loadavg)"
if [[ $ok == yes ]]; then
  mkdir -p $O/runs; setsid nohup bash $O/runall4.sh > $O/runs/runall4.log 2>&1 < /dev/null & echo "runall4 started, pid $!"; echo $! > $O/runs/runall4.launch.pid
else echo "runall4 NOT started"; fi

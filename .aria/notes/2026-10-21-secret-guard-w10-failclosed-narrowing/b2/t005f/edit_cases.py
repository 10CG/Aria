import sys, textwrap
helper, scd, suite, scc = sys.argv[1:5]
W1 = ['V15-W1a-autofs-mount-point-not-looked-at', 'V15-W1b-binfmt-misc-with-wslinterop-late', 'V15-W1c-binfmt-misc-without-entry', 'V15-W1d-unreadable-mount-table']
RX = ['V15-T1-timer-sleeps-time-left', 'V15-T2-anchor-taken-once-at-hook-start', 'V15-T3-job-errors-silenced', 'V15-W1e-gate-closed-by-wsl-file-system']
def rep(t, old, new, what):
    assert t.count(old) == 1, (what, t.count(old)); return t.replace(old, new)
M3C_OLD = '# both trigger points ask the gate (R2 PP2-D): with the platform check failing, a copy over 8192 is the baseline size block (2), never 4\n'
M3C_NEW = ('# the closed pole of the gate at both trigger points (R2 PP2-D): with the platform check failing, a copy over 8192 is the baseline size block (2), never 4.\n'
           '# A trigger point that never asks the gate passes this too; the open pole -- status 4 with the gate open -- is V14-G1 (the ids keep their names: the evidence cites them)\n')
M3K_OLD = '"the platform check failing, a $2 copy over 8192: status/text [$r] (want [2 oversize], never 4)"'
M3K_NEW = '"gate closed (the platform check failing), a $2 copy over 8192: status/text [$r] (want [2 oversize], never 4; this pins the closed pole only, the open pole is V14-G1)"'
M4_OLD = '''  nproc_binds() {   # status 0 when RLIMIT_NPROC binds this process. It does not for uid 0, nor with CAP_SYS_RESOURCE or CAP_SYS_ADMIN (getrlimit(2)); then probe
    local c; c=$(awk '/^CapEff:/{print $2}' /proc/self/status 2>/dev/null)
    if [[ "$(id -u)" != 0 && "$c" =~ ^[0-9a-fA-F]+$ ]]'''
M4_NEW = '''  nproc_binds() {   # status 0 when RLIMIT_NPROC binds this process. It does not for real user ID 0, nor with CAP_SYS_RESOURCE or CAP_SYS_ADMIN (getrlimit(2)); then probe
    local c='' l   # CapEff of this bash itself, read by bash: an awk would read its own /proc/self/status, with only the capabilities that survived its execve
    { while IFS= read -r l; do [[ $l == CapEff:* ]] && c=${l#CapEff:}; done < "/proc/$BASHPID/status"; } 2>/dev/null; c=${c//[[:space:]]/}
    if [[ "$(id -ru)" != 0 && "$c" =~ ^[0-9a-fA-F]+$ ]]'''
W1_BLOCK = r'''# What 1 supplement 2 (TASK-005 D-1, D-2): _sg_relax_nowslfs looks at the WSLInterop* entries only under a mounted binfmt_misc, so the look never
# triggers an automount, and a mount table that cannot be read keeps the relaxation off. Fake mount tables and a directory under $X; both modes
if need _sg_relax_nowslfs; then
  w1d="$X/w1-binfmt"; mkdir -p "$w1d"
  printf 'systemd-1 %s autofs rw,relatime,fd=29,pgrp=1,timeout=0,minproto=5,maxproto=5,direct 0 0\nproc /proc proc rw,nosuid,nodev,noexec,relatime 0 0\n' "$w1d" > "$X/w1-autofs"
  printf 'binfmt_misc %s binfmt_misc rw,nosuid,nodev,noexec,relatime 0 0\nproc /proc proc rw,nosuid,nodev,noexec,relatime 0 0\n' "$w1d" > "$X/w1-mounted"
  w1() {   # id mounts entry want what : _sg_relax_nowslfs MOUNTS DIR, DIR holding only ENTRY; status and stderr (the last line of each table does not match)
    local r t=''; rm -f "$w1d"/*; : > "$w1d/$3"
    r=$( _sg_relax_nowslfs "$2" "$w1d" 2>"$X/w1e"; echo $? )
    [[ $r == "$4" ]] || t+='[status] '; [[ -s "$X/w1e" ]] && t+='[stderr]'
    [[ -z "$t" ]]; chk $? "$1" "$5: status $r (want $4), stderr $(wc -c < "$X/w1e") bytes (want 0)" "${t% }"
  }
  sel V15-W1a-autofs-mount-point-not-looked-at && w1 V15-W1a-autofs-mount-point-not-looked-at "$X/w1-autofs" WSLInterop 0 "an autofs mount point at DIR (nothing mounted) that holds WSLInterop"
  sel V15-W1b-binfmt-misc-with-wslinterop-late && w1 V15-W1b-binfmt-misc-with-wslinterop-late "$X/w1-mounted" WSLInterop-late 1 "binfmt_misc mounted at DIR, holding WSLInterop-late"
  sel V15-W1c-binfmt-misc-without-entry && w1 V15-W1c-binfmt-misc-without-entry "$X/w1-mounted" status 0 "binfmt_misc mounted at DIR, no WSLInterop* entry"
  sel V15-W1d-unreadable-mount-table && w1 V15-W1d-unreadable-mount-table "$X/w1-none/mounts" WSLInterop 1 "a mount table that cannot be read"
else miss V15-W1a-autofs-mount-point-not-looked-at V15-W1b-binfmt-misc-with-wslinterop-late V15-W1c-binfmt-misc-without-entry V15-W1d-unreadable-mount-table; fi
'''
RX_BLOCK = r'''  # ---------------- TASK-005 (review m-6; What 1 supplement 2): load-independent direct cases, each in a subshell on a freshly sourced hook ----------------
  # (the cases above leave stubs behind). The timing cases still prove the whole chain in real time; these pin three of its parts whatever the host load.
  v15src() { source "$H" </dev/null >/dev/null 2>&1; set +e; input=''; command=''; }
  if sel V15-T1-timer-sleeps-time-left; then   # the timer sleeps exactly _SG_LEFT: a sleep function records its argument, the judgement waits until it has
    if need _sg_relax_run _sg_relax_job _sg_relax_left; then
      t1f="$X/t1-sleep"; : > "$t1f"
      r=$( v15src; sleep() { printf '%s\n' "${1-}" >> "$t1f"; command sleep "$@"; }
           _sg_relax_left() { _SG_LEFT=1.234567; return 0; }
           _sg_vx_pass() { local k; for k in $(seq 1 300); do [[ -s "$t1f" ]] && return 0; command sleep 0.01; done; return 0; }
           _SG_P0=${EPOCHREALTIME:-}; _sg_relax_run "cmd" 2>/dev/null; echo $? )
      t1a=$(head -n 1 "$t1f"); t1n=$(grep -c '' "$t1f")
      [[ "$t1a" == 1.234567 ]]; chk $? V15-T1-timer-sleeps-time-left "the timer's sleep argument [$t1a] (want [1.234567], the _SG_LEFT that _sg_relax_left set; $t1n sleep call(s) recorded, _sg_relax_run status $r)" "[value]"
    else miss V15-T1-timer-sleeps-time-left; fi
  fi
  if sel V15-T2-anchor-taken-once-at-hook-start; then   # the anchor _SG_P0 is taken once, at the hook start: (a) one assignment, on the line after set -uo pipefail;
    # (b) with the anchor 2.5 s back and budget 3 the judgement inside the job sees at most 0.5 s left (a fresh anchor in the gate, the run or the job gives about 3 s)
    if need _sg_relax_ok _sg_relax_run _sg_relax_job _sg_vx_pass; then
      t2s=$(awk '/^[[:space:]]*#/{p=$0; next} /(^|[^A-Za-z0-9_])_SG_P0=/{n++; if (p ~ /^set -uo pipefail/) a++} {p=$0} END{printf "%d %d", n, a}' "$H")
      awk '/^_sg_per_segment_eval\(\) \{/,/^\}$/' "$H" > "$X/t2-pse.sh"
      t2f="$X/t2-left"; : > "$t2f"; t2c="v=$x4; : \$v \$v \$v"
      if [[ ! -s "$X/t2-pse.sh" ]]; then out SETUP V15-T2-anchor-taken-once-at-hook-start "_sg_per_segment_eval not found by anchor"
      else
        r=$( v15src; source "$X/t2-pse.sh"; export SECRET_GUARD_TIME_BUDGET_S=3
             _sg_core_eval() { _SG_MODE=whole; return 0; }
             t2d=$(declare -f _sg_vx_pass); eval "_sg_t2_vx_pass () ${t2d#*\(\)}"
             _sg_vx_pass() { if [[ -n "${_SG_RELAXED:-}" ]]; then printf '%s\n' "${_SG_LEFT-}" >> "$t2f"; return 0; fi; _sg_t2_vx_pass "$@"; }
             _SG_P0=$(awk -v e="${EPOCHREALTIME:-0}" 'BEGIN{sub(",",".",e); printf "%.6f", e-2.5}'); command=$t2c
             _sg_per_segment_eval "$t2c" >/dev/null 2>&1; echo $? )
        t2a=$(head -n 1 "$t2f"); t=''
        [[ $t2s == "1 1" ]] || t+='[static] '
        awk -v l="$t2a" 'BEGIN{exit !(l != "" && l+0 > 0 && l+0 <= 0.5)}' || t+='[value]'
        [[ -z "$t" ]]; chk $? V15-T2-anchor-taken-once-at-hook-start "assignments to _SG_P0 / of them on the line after set -uo pipefail [$t2s] (want [1 1]); anchor 2.5 s back, budget 3: the judgement in the job saw _SG_LEFT [$t2a] (want 0 < left <= 0.5; _sg_per_segment_eval status $r)" "${t% }"
      fi
    else miss V15-T2-anchor-taken-once-at-hook-start; fi
  fi
  if sel V15-T3-job-errors-silenced; then   # exec 2>/dev/null in the run's command substitution: a job that dies the way the deadline kills it leaves stderr empty
    if need _sg_relax_run; then
      r=$( v15src; _sg_relax_left() { _SG_LEFT=2.000000; return 0; }; _sg_relax_job() { kill -KILL "$BASHPID"; }
           _sg_relax_run "cmd" 2>"$X/t3e"; echo $? )
      t=''; [[ $r == 4 ]] || t+='[rc] '; [[ -s "$X/t3e" ]] && t+='[stderr]'
      [[ -z "$t" ]]; chk $? V15-T3-job-errors-silenced "a job killed the way the deadline kills it (kill -KILL on itself): _sg_relax_run status $r (want 4), stderr [$(head -c 80 "$X/t3e" | tr '\n' ' ')] (want empty)" "${t% }"
    else miss V15-T3-job-errors-silenced; fi
  fi
  if sel V15-W1e-gate-closed-by-wsl-file-system; then   # What 1 supplement 2: the gate's second WSL line -- _sg_relax_nowslfs failing closes the gate on this relaxing bash
    if need _sg_relax_ok _sg_relax_nowslfs; then
      r=$( v15src; _sg_relax_nowslfs() { return 1; }; _SG_P0=${EPOCHREALTIME:-}; gate )
      [[ $r == 1 ]]; chk $? V15-W1e-gate-closed-by-wsl-file-system "_sg_relax_nowslfs stubbed to fail (a WSLInterop* entry, or a mount table that cannot be read) on a bash whose gate opens: _sg_relax_ok status $r (want 1)" "[status]"
    else miss V15-W1e-gate-closed-by-wsl-file-system; fi
  fi
'''
for f in (helper, scd):
    t = open(f, encoding='utf-8').read()
    t = rep(t, M3C_OLD, M3C_NEW, f + ' m3c'); t = rep(t, M3K_OLD, M3K_NEW, f + ' m3k'); t = rep(t, M4_OLD, M4_NEW, f + ' m4')
    L = t.split('\n')
    i = [k for k, s in enumerate(L) if s.startswith('else miss V2-G14-cwd-extension-file-with-entry')]; assert len(i) == 1, (f, i)
    L[i[0]+1:i[0]+1] = W1_BLOCK.rstrip('\n').split('\n')
    e = L.index('echo "END sc-direct"'); assert L[e-1] == 'fi', (f, L[e-1])
    if f == helper:
        k = max(j for j in range(e) if L[j] == 'else')
    else:
        k = e - 1
    L[k:k] = RX_BLOCK.rstrip('\n').split('\n')
    t = '\n'.join(L)
    if f == helper:
        t = rep(t, 'V14-F1-status-4-falls-back-to-the-baseline-block"   # the cases of MODE relax', 'V14-F1-status-4-falls-back-to-the-baseline-block\n' + ' '.join(RX) + '"   # the cases of MODE relax', 'relax_ids')
    open(f, 'w', encoding='utf-8').write(t)
def close_list(t, start, add, what):
    L = t.split('\n'); i = [k for k, s in enumerate(L) if s.startswith(start)]; assert len(i) == 1, (what, i)
    j = next(k for k in range(i[0], len(L)) if L[k].rstrip().endswith('"') and (k > i[0] or L[k].count('"') > 1)); assert L[j].endswith('"'), (what, L[j])
    L[j] = L[j][:-1] + '\n' + ' '.join(add) + '"'; print(what, 'closed at line', j + 1)
    return '\n'.join(L)
t = open(scc, encoding='utf-8').read()
t = close_list(t, 'EXP_DIRECT_BOTH="', W1, 'scc both'); t = close_list(t, 'EXP_DIRECT_RELAX="', RX, 'scc relax')
open(scc, 'w', encoding='utf-8').write(t)
t = open(suite, encoding='utf-8').read()
t = close_list(t, 'SGW_EXP_DIRECT="', W1 + RX, 'suite direct')
t = rep(t, '# Coverage: 972 cases (966 without zsh)', '# Coverage: 980 cases (974 without zsh)', 'count'); t = rep(t, '# 141 of those cases are the W10', '# 149 of those cases are the W10', 'count141')
L = t.split('\n')
i0 = [k for k, s in enumerate(L) if 'and are never passed (P9); a copy over the copy limit is blocked that way only where the relaxation is not in effect (What 1 and its' in s]; assert len(i0) == 1
i0 = i0[0]; i1 = i0 + 3; assert L[i1].endswith('and any other copy is judged as usual, so it may pass'), L[i1]
w = max(len(L[k]) for k in range(i0 - 2, i1 + 1)); txt = ' '.join(s[2:].strip() for s in L[i0:i1+1])
old = 'a copy over the copy limit is blocked that way only where the relaxation is not in effect (What 1 and its supplement: another platform or bash version, WSL, a project extension, or no time left; P2).'
new = 'a copy over the copy limit is blocked that way wherever the relaxation is not in effect (What 1 and its supplement: another platform or bash version, WSL, a project extension, or no time left; P2), and also where it is whenever the rerun falls back (the deadline, a time checkpoint, the self-check, any other failure: What 4).'
assert txt.count(old) == 1; out = textwrap.wrap(txt.replace(old, new), width=w - 2, break_long_words=False, break_on_hyphens=False)
L[i0:i1+1] = ['# ' + s for s in out]; print('suite head', i1 - i0 + 1, '->', len(out), 'width', w)
open(suite, 'w', encoding='utf-8').write('\n'.join(L))

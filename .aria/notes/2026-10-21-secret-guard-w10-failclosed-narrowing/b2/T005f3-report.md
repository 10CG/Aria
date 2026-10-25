# TASK-005 修复轮第三段（5f3）执笔席报告（10CG/aria-plugin#217）

执笔席：5f3（全新实例），2026-10-25。aria worktree 基线 `710a36d`（hook `834dee6db0d0`），改后 hook sha256 前缀 **`16996eb7db21`**，未 commit。工具调用 36 次（上限 60；含写本报告与此次改计数）。
脚本与证据都在 `r217impl/t005f3/`：`edit5f3.py`（全部改动，从 `pre/` 的改前副本出发，可重放）、`prove5f3.sh`（坏实现、能红、判据对照、变异生成、commentsync）、`runall3.sh`（各轮）、`expect.md`（先写的预期）、`proofs/`、`runs/`、`diffs/`、`cs/`。

## 一、各项结论

- **A1** `_sg_relax_ok`：环境变量那一行原本已与 v3.4 第一行逐字相同（脚本断言后照换，零字节变化）；删掉 v3.3 那行 `[[ -n "$wsl" ]] || _sg_relax_nowslfs || wsl=wsl`；在 `_sg_relax_left || return 1` 之后加 v3.4 第二行。两行都由脚本从 proposal「v3.4 的做法」之后的第一个代码块机械取出。
- **A2** `_sg_relax_nowslfs` 整个换成 proposal 第二个代码块（机械取出，逐字）。
- **A3** 头注释「Shell variable indirection」补 D-3 例外一句（与重跑块头那句同义：「inside the rerun」对应块头的「inside the job」，「instead of the size block's text」对应「instead of the baseline text」——头注释里回落就叫 that size block），只重排了原来那一短行，宽度取该条目最宽的 91 列。
- **A4** hook 其余一字未改：完整 diff 见第二节（3 个 hunk）。
- **B1** V15-W1a-d 结论仍为 a 0、b 1、c 0、d 1；只改了 W1c 的说明文字（两个名字）和 `w1` 的实现（拆出通用的 `w1x`，见下）。
- **B2** V15-W1e 改成两面（id 不变）：子壳里新 source hook、`unset _SG_RELAXED WSL_DISTRO_NAME WSL_INTEROP`、预算显式 3、新锚点、`_sg_relax_noext` 桩成 none，平台用本 bash（MODE relax）；桩返回 0 须开门（标签 `[open]`），返回 1 须关门（`[closed]`）。
- **B3** 新增 9 条：W1f 空表、W1g 叠 autofs、W1h 目录当表、W1i noglob、W1j failglob、W1k 不可查（uid 0 下 SKIP [platform]）、W1l 可查不可列（结束前改回权限）、W1m 顺序（两种模式），W1n 开销（MODE relax）。全部在目标 hook 上 PASS（5 个 bash 的过滤轮、整轮、sc-cases）。
- **B4** 能红：全部按预期——v3.3 函数使 f g h i j k l 变红；去 `-x` 行只红 k；挪回平台判据之前只红 m（`[platform] [time]`）；W1e 两面各一个坏实现分别红 `[closed]` 与 `[open]`；v3.3 函数下 W1n 墙钟 2.219 s（soft bad）。见第三节。
- **B5** 四份测试侧判据（helper / sc-direct.sh 的 `wslmark`、套件 `sg_w10_wslfs`、sc-cases.sh 的 `wslmark`）改为同一函数体（另写，不 source hook）；在主控的 12 种情形上与 hook 函数逐种对照，5 个 bash 都是 12 条 0 不一致，hook 结论与 proposal 列的 12 个值一致、stderr 全 0。
- **B6** V15-T2 注释改为：值由准入门与 run 里那两次 `_sg_relax_left` 定，从设锚点到这两次调用超过 1.0 s 时门关上或 run 回落、判定根本不运行（`_SG_LEFT []` 的假红）。
- **B7** 编号进了 helper `RELAX_IDS`（W1n）、套件 `SGW_EXP_DIRECT`、sc-cases.sh 的 `EXP_DIRECT_BOTH` / `EXP_DIRECT_RELAX`；套件头注释 981 (975) -> 990 (984)。本机无 zsh，整轮实数 984，与「无 zsh」计数相符。
- **C** `mutants.py` 一个锚点（删 `_sg_relax_left || return 1` 那个变异）改成新原文；`impl/w14-mutants.py` 的 Q-30 锚点同样改、`IMPL_SHA12` 834dee6db0d0 -> 16996eb7db21；两者在新 hook 上都能全部生成（57 + 7；31）。commentsync 照前两段的做法从 eeb67786 版用 `t005f/cs/derive-5f.py` 重新导出，与 5f2 版只差 FIX5_HOOK 一行（站点 1 由删 2 增 2 变为删 2 增 3：D-3 那句是新单元）；target / baseline / proto GREEN，四个构造 RED（78、60、58、57；5f2 为 77、59、58、57）。
- **各轮**：全部绿。5 个 bash 过滤轮 0 FAIL；整轮两轮 0 FAIL；sc-cases 160 PASS 0 FAIL；run-mutants v31 模式 63 CAUGHT + P-0 GREEN，套件模式 63 CAUGHT、P-0 首轮 NOT-JUDGED（负载），低负载单跑两次都 GREEN；w14 预测内 26、新增用例抓到 5、未判 0、未抓到 0（与 5f2 同）。

## 二、hook 完整 diff（相对 710a36d）

```diff
diff --git a/hooks/secret-guard.sh b/hooks/secret-guard.sh
index c687e9e..c7d445d 100755
--- a/hooks/secret-guard.sh
+++ b/hooks/secret-guard.sh
@@ -98,7 +98,10 @@
 #     growth text, a value over 4096 characters with the value text (the rerun reaches
 #     values that the counts cut off in the baseline pass), and the deadline, a time
 #     checkpoint, the self-check or any other failure of the rerun falls back to that size
-#     block. The pass substitutes text; it does not run the shell: a
+#     block. The one exception (What 4): a fatal error of bash itself inside the rerun that
+#     makes it exit with status 2 and write its error message is passed on as the block
+#     text -- the command is still blocked, but with bash's message instead of the size
+#     block's text. The pass substitutes text; it does not run the shell: a
 #     variable assigned twice is replaced by its FIRST value (bash reads the last), and in
 #     segment mode a value holding shell syntax (`G='| jq keys'`) becomes syntax in the
 #     copy, so a read can earn a filter credit that bash never applies. Both pass, in small
@@ -827,19 +830,21 @@ _sg_relax_ok() {   # status 0 when the relaxation is in effect for this command;
   local osr= wsl=
   { IFS= read -r osr < /proc/sys/kernel/osrelease; } 2>/dev/null
   [[ -n "${WSL_DISTRO_NAME:-}${WSL_INTEROP:-}" ]] && wsl=wsl   # WSL marks in the environment; the environment can only switch the relaxation off with them
-  [[ -n "$wsl" ]] || _sg_relax_nowslfs || wsl=wsl   # a WSLInterop* entry under a mounted binfmt_misc, or a mount table that cannot be read
   _sg_relax_platform "${BASH_VERSINFO[5]:-}" "${BASH_VERSINFO[0]:-0}" "${BASH_VERSINFO[1]:-0}" "$osr" "$wsl" || return 1   # read-only build and kernel facts, which the environment cannot rewrite (OSTYPE, MACHTYPE and HOSTTYPE can be)
   _sg_relax_left || return 1
+  _sg_relax_nowslfs || return 1   # the WSL mark of the file system (a WSLInterop entry under binfmt_misc, or a mount table that cannot be read), asked only where the platform and the time would relax: elsewhere the mount table is never read
   [[ "$( _sg_relax_noext 2>/dev/null )" == none ]]
 }
 _sg_relax_platform() {   # MACHINE MAJOR MINOR OSRELEASE [WSL]: status 0 on an x86_64 GNU/Linux build of a bash version the mechanism was measured on, 5.0 to 5.3, outside WSL (owner ruling E, 2026-10-22 and 2026-10-23: an untested platform -- macOS, Windows, WSL1 and WSL2, musl, Android, aarch64 and other architectures, another bash -- keeps the baseline)
   [[ "${1:-}" == x86_64-*-linux-gnu* && -n "${4:-}" && "${4:-}" != *[Mm]icrosoft* && "${4:-}" != *WSL* && -z "${5:-}" ]] && (( ${2:-0} == 5 && ${3:-0} <= 3 ))
 }
-_sg_relax_nowslfs() {   # [MOUNTS [DIR]]: status 0 only when no WSL interop entry can exist -- the mount table (default /proc/self/mounts) reads, and no binfmt_misc file system is mounted at DIR (default /proc/sys/fs/binfmt_misc), or one is and holds no entry named WSLInterop*. The entries are looked at only under a mounted binfmt_misc, so the look never triggers an automount (an autofs mount point there that nobody serves can hold a stat until the hook is killed, and a killed hook lets the command through); a mount table that cannot be read keeps the relaxation off. The two arguments exist for the direct-call cases only; the gate calls it with none
-  local d="${2:-/proc/sys/fs/binfmt_misc}" l e m=0
-  { while IFS= read -r l; do if [[ "$l" == *" $d binfmt_misc "* ]]; then m=1; fi; done; } 2>/dev/null < "${1:-/proc/self/mounts}" || return 1   # if, not &&: a last line that does not match must not make the loop's status 1 (that would read as an unreadable table); 2>/dev/null before <, so a table that cannot be opened writes nothing to stderr
-  (( m )) || return 0
-  for e in "$d"/WSLInterop*; do [[ -e "$e" ]] && return 1; done
+_sg_relax_nowslfs() {   # [MOUNTS [DIR]]: status 0 only when no WSL interop entry can exist -- the mount table (default /proc/self/mounts) reads and is not empty, and the topmost mount at DIR (default /proc/sys/fs/binfmt_misc; the table's last line for it) is not a binfmt_misc file system, or it is, DIR can be searched, and it holds neither WSLInterop nor WSLInterop-late. awk reads the table in one pass: a line-by-line read of /proc/self/mounts in bash costs O(n^2) (bash seeks back after every line and procfs regenerates the table from the start), seconds on a host with a few thousand mounts, outside the hard deadline. The entries are looked at only when binfmt_misc is the topmost mount there, so the look never triggers an automount; the two names are tested one by one, not by a glob, so noglob or failglob imported from the environment cannot change the look. A table that cannot be read, or reads empty, keeps the relaxation off. The two arguments exist for the direct-call cases only; the gate calls it with none
+  local d="${2:-/proc/sys/fs/binfmt_misc}" r
+  r=$(awk -v d="$d" '$2 == d { t = $3 } END { print NR, t }' "${1:-/proc/self/mounts}" 2>/dev/null) || return 1
+  [[ "${r%% *}" =~ ^[1-9][0-9]*$ ]] || return 1   # no line read: a table that cannot be read
+  [[ "${r#* }" == binfmt_misc ]] || return 0   # binfmt_misc is not the topmost mount at DIR: no interop entry can be registered there, and nothing under DIR is looked at
+  [[ -x "$d" ]] || return 1   # DIR cannot be searched: the entries cannot be seen, so they may exist
+  [[ -e "$d/WSLInterop" || -e "$d/WSLInterop-late" ]] && return 1
   return 0
 }
 _sg_relax_noext() {   # prints "none" only when no extension can be in effect: no project root is found (_sg_ext_root prints nothing, which includes a cwd that jq cannot read: without a root no extension can be in effect), or there is no .aria/secret-guard.paths under it. A file there, in any state, keeps the relaxation off
```

## 三、新用例与改过的用例（helper 与 v31/sc-direct.sh 同一份代码，INV-2）

两种模式的部分（W1a-d 改说明、W1f-l 新增、W1m 新增；`w1` 拆成通用的 `w1x` 加只管 `$w1d` 的 `w1`）：

```bash
# What 1 supplement 2 (v3.4; TASK-005 D-1, D-2; review R2 M-1, m-1 and doubt 1): _sg_relax_nowslfs reads the mount table in one pass and takes the topmost
# mount at DIR (the table's last line for it); the entries are looked at only when that is binfmt_misc, so the look never triggers an automount, and the
# two names are tested one by one (no glob: noglob or failglob cannot change the look). A table that cannot be read or reads empty, or a DIR that cannot be
# searched, keeps the relaxation off. Fake mount tables and directories under $X; both modes
if need _sg_relax_nowslfs; then
  w1d="$X/w1-binfmt"; mkdir -p "$w1d" "$X/w1-tabledir"
  printf 'systemd-1 %s autofs rw,relatime,fd=29,pgrp=1,timeout=0,minproto=5,maxproto=5,direct 0 0\nproc /proc proc rw,nosuid,nodev,noexec,relatime 0 0\n' "$w1d" > "$X/w1-autofs"
  printf 'binfmt_misc %s binfmt_misc rw,nosuid,nodev,noexec,relatime 0 0\nproc /proc proc rw,nosuid,nodev,noexec,relatime 0 0\n' "$w1d" > "$X/w1-mounted"
  printf 'binfmt_misc %s binfmt_misc rw,nosuid,nodev,noexec,relatime 0 0\nsystemd-1 %s autofs rw,relatime,fd=29,pgrp=1,timeout=0,minproto=5,maxproto=5,direct 0 0\nproc /proc proc rw,nosuid,nodev,noexec,relatime 0 0\n' "$w1d" "$w1d" > "$X/w1-stacked"; : > "$X/w1-empty"
  w1x() {   # id mounts dir want what [setup] : _sg_relax_nowslfs MOUNTS DIR after SETUP (a shell option, set in the same subshell); status and stderr
    local r t=''
    r=$( [[ -z "${6:-}" ]] || eval "$6"; _sg_relax_nowslfs "$2" "$3" 2>"$X/w1e"; echo $? )
    [[ $r == "$4" ]] || t+='[status] '; [[ -s "$X/w1e" ]] && t+='[stderr]'
    [[ -z "$t" ]]; chk $? "$1" "$5: status $r (want $4), stderr $(wc -c < "$X/w1e") bytes (want 0)" "${t% }"
  }
  w1() { rm -f "$w1d"/*; : > "$w1d/$3"; w1x "$1" "$2" "$w1d" "$4" "$5" "${6:-}"; }   # id mounts entry want what [setup] : DIR = $w1d holding only ENTRY (the last line of each table does not match)
  sel V15-W1a-autofs-mount-point-not-looked-at && w1 V15-W1a-autofs-mount-point-not-looked-at "$X/w1-autofs" WSLInterop 0 "an autofs mount point at DIR (nothing mounted) that holds WSLInterop"
  sel V15-W1b-binfmt-misc-with-wslinterop-late && w1 V15-W1b-binfmt-misc-with-wslinterop-late "$X/w1-mounted" WSLInterop-late 1 "binfmt_misc mounted at DIR, holding WSLInterop-late"
  sel V15-W1c-binfmt-misc-without-entry && w1 V15-W1c-binfmt-misc-without-entry "$X/w1-mounted" status 0 "binfmt_misc mounted at DIR, neither WSLInterop nor WSLInterop-late in it"
  sel V15-W1d-unreadable-mount-table && w1 V15-W1d-unreadable-mount-table "$X/w1-none/mounts" WSLInterop 1 "a mount table that cannot be read"
  sel V15-W1f-empty-mount-table && w1 V15-W1f-empty-mount-table "$X/w1-empty" status 1 "a mount table that reads empty (0 lines; no WSL entry in DIR)"
  sel V15-W1g-autofs-on-top-of-binfmt-misc-not-looked-at && w1 V15-W1g-autofs-on-top-of-binfmt-misc-not-looked-at "$X/w1-stacked" WSLInterop 0 "binfmt_misc at DIR with autofs mounted on top of it (the topmost mount decides: not looked at), DIR holding WSLInterop"
  sel V15-W1h-directory-as-mount-table && w1 V15-W1h-directory-as-mount-table "$X/w1-tabledir" status 1 "a directory given as the mount table (no WSL entry in DIR)"
  sel V15-W1i-noglob-binfmt-misc-with-wslinterop-late && w1 V15-W1i-noglob-binfmt-misc-with-wslinterop-late "$X/w1-mounted" WSLInterop-late 1 "under set -f (noglob, which the environment can import): binfmt_misc mounted at DIR, holding WSLInterop-late" 'set -f'
  sel V15-W1j-failglob-binfmt-misc-without-entry && w1 V15-W1j-failglob-binfmt-misc-without-entry "$X/w1-mounted" status 0 "under shopt -s failglob: binfmt_misc mounted at DIR, neither name in it" 'shopt -s failglob'
  if sel V15-W1k-unsearchable-directory; then   # a DIR that cannot be searched: the entries cannot be seen, so they may exist (review R2 m-1). uid 0 searches any directory: not applicable there
    if [[ "$(id -ru)" == 0 ]]; then out SKIP V15-W1k-unsearchable-directory "[platform] uid 0 searches a directory of mode 000, so a DIR that cannot be searched cannot be made here"
    else
      w1k="$X/w1-nosearch"; mkdir -p "$w1k"; printf 'binfmt_misc %s binfmt_misc rw,nosuid,nodev,noexec,relatime 0 0\nproc /proc proc rw,nosuid,nodev,noexec,relatime 0 0\n' "$w1k" > "$X/w1-nosearch-mounts"; chmod 000 "$w1k"
      w1x V15-W1k-unsearchable-directory "$X/w1-nosearch-mounts" "$w1k" 1 "binfmt_misc mounted at DIR, DIR of mode 000 (cannot be searched; nothing in it)"; chmod 755 "$w1k"
    fi
  fi
  if sel V15-W1l-unlistable-directory-with-wslinterop-late; then   # a DIR that can be searched but not listed (mode 0311): each name is still seen, where a glob sees none (review R2 m-1)
    w1l="$X/w1-listless"; mkdir -p "$w1l"; : > "$w1l/WSLInterop-late"; printf 'binfmt_misc %s binfmt_misc rw,nosuid,nodev,noexec,relatime 0 0\nproc /proc proc rw,nosuid,nodev,noexec,relatime 0 0\n' "$w1l" > "$X/w1-listless-mounts"; chmod 0311 "$w1l"
    w1x V15-W1l-unlistable-directory-with-wslinterop-late "$X/w1-listless-mounts" "$w1l" 1 "binfmt_misc mounted at DIR, DIR of mode 0311 (searched, not listed) holding WSLInterop-late"; chmod 755 "$w1l"
  fi
else miss V15-W1a-autofs-mount-point-not-looked-at V15-W1b-binfmt-misc-with-wslinterop-late V15-W1c-binfmt-misc-without-entry V15-W1d-unreadable-mount-table V15-W1f-empty-mount-table V15-W1g-autofs-on-top-of-binfmt-misc-not-looked-at V15-W1h-directory-as-mount-table V15-W1i-noglob-binfmt-misc-with-wslinterop-late V15-W1j-failglob-binfmt-misc-without-entry V15-W1k-unsearchable-directory V15-W1l-unlistable-directory-with-wslinterop-late; fi
# What 1 supplement 2 (v3.4): the gate asks for the WSL mark of the file system after the platform and the time, so where either closes the gate the mount
# table is never read. _sg_relax_nowslfs stubbed to count its calls, on a freshly sourced hook with no WSL mark in the environment; both modes
if sel V15-W1m-mount-table-read-only-after-platform-and-time; then
  if need _sg_relax_ok _sg_relax_platform _sg_relax_left _sg_relax_nowslfs _sg_relax_noext; then
    w1m() {   # PLATFORM LEFT : the _sg_relax_nowslfs calls of one _sg_relax_ok, with _sg_relax_platform returning PLATFORM and _sg_relax_left returning LEFT
      : > "$X/w1m"
      ( source "$H" </dev/null >/dev/null 2>&1; set +e; unset _SG_RELAXED WSL_DISTRO_NAME WSL_INTEROP; w1mp=$1 w1ml=$2
        _sg_relax_platform() { return "$w1mp"; }; _sg_relax_left() { return "$w1ml"; }
        _sg_relax_nowslfs() { printf x >> "$X/w1m"; return 0; }; _sg_relax_noext() { echo none; }
        _sg_relax_ok ) >/dev/null 2>&1
      wc -c < "$X/w1m" | tr -d ' '
    }
    w1m1=$(w1m 1 0); w1m2=$(w1m 0 1); w1m3=$(w1m 0 0); t=''
    [[ $w1m1 == 0 ]] || t+='[platform] '; [[ $w1m2 == 0 ]] || t+='[time] '; [[ $w1m3 == 1 ]] || t+='[control]'
    [[ -z "$t" ]]; chk $? V15-W1m-mount-table-read-only-after-platform-and-time "_sg_relax_nowslfs calls in one _sg_relax_ok: the platform fails $w1m1 (want 0), no time left $w1m2 (want 0), both pass $w1m3 (want 1: the stub is reached)" "${t% }"
  else miss V15-W1m-mount-table-read-only-after-platform-and-time; fi
fi
```

MODE relax 的部分（W1e 两面、W1n 开销）：

```bash
  if sel V15-W1e-gate-closed-by-wsl-file-system; then   # What 1 supplement 2 (v3.4): the gate's last check before the extension -- _sg_relax_nowslfs failing closes the gate on this relaxing bash.
    # Two sides, so that a gate closed by an earlier check cannot pass the case: every check before it passes here (a fresh anchor, budget 3, no WSL mark in
    # the environment, this bash's platform; _sg_relax_noext stubbed to print none), so the stub returning 0 must open the gate and returning 1 must close it
    if need _sg_relax_ok _sg_relax_nowslfs _sg_relax_noext; then
      w1e() { ( v15src; unset _SG_RELAXED WSL_DISTRO_NAME WSL_INTEROP; export SECRET_GUARD_TIME_BUDGET_S=3; w1es=$1
                _sg_relax_nowslfs() { return "$w1es"; }; _sg_relax_noext() { echo none; }; _SG_P0=${EPOCHREALTIME:-}; gate ); }
      w1e0=$(w1e 0); w1e1=$(w1e 1); t=''
      [[ $w1e0 == 0 ]] || t+='[open] '; [[ $w1e1 == 1 ]] || t+='[closed]'
      [[ -z "$t" ]]; chk $? V15-W1e-gate-closed-by-wsl-file-system "every check before it passing: _sg_relax_nowslfs stubbed to return 0 -> _sg_relax_ok status $w1e0 (want 0), stubbed to return 1 (a WSLInterop entry, a DIR that cannot be searched, a mount table that cannot be read or reads empty) -> $w1e1 (want 1)" "${t% }"
    else miss V15-W1e-gate-closed-by-wsl-file-system; fi
  fi
  if sel V15-W1n-mount-table-read-in-one-pass; then   # What 1 supplement 2 (v3.4; review R2 M-1): awk reads the mount table in one pass. In a private mount namespace (unshare -rm) with 1000 tmpfs
    # mounts stacked on one directory, _sg_relax_nowslfs reads the real table and returns within 0.5 s (v3.3 read it line by line in bash, and procfs
    # regenerates the table at every seek back: 2.2 s there). Hard: the 1000 mounts made, status 0 (no WSL mark: MODE relax), stderr empty; soft (INV-7): the wall
    if ! need _sg_relax_nowslfs; then miss V15-W1n-mount-table-read-in-one-pass
    elif ! unshare -rm true >/dev/null 2>&1; then out SKIP V15-W1n-mount-table-read-in-one-pass "[platform] unshare -rm (a private user and mount namespace) is not available here"
    else
      printf '%s\n' 'source "$1" </dev/null >/dev/null 2>&1; set +e; m=$2/w1n-m; mkdir -p "$m"; n=0' \
        'while (( n < 1000 )); do mount -t tmpfs w1n "$m" 2>/dev/null || break; n=$(( n + 1 )); done' \
        't0=$EPOCHREALTIME; _sg_relax_nowslfs 2>"$2/w1n-e"; r=$?; t1=$EPOCHREALTIME' \
        'echo "$n $r $(grep -c "" /proc/self/mounts) ${t0/,/.} ${t1/,/.}"' > "$X/w1n.sh"
      read -r w1nn w1nr w1nl w1n0 w1n1 <<< "$(unshare -rm "$BASH" "$X/w1n.sh" "$H" "$X" 2>/dev/null)"
      if [[ "${w1nn:-0}" == 0 ]]; then out SKIP V15-W1n-mount-table-read-in-one-pass "[platform] tmpfs cannot be mounted in a private mount namespace here"
      else
        w1nw=$(awk -v a="${w1n0:-0}" -v b="${w1n1:-0}" 'BEGIN{printf "%.3f", b-a}'); w1nh=ok; w1ns=ok
        [[ $w1nn == 1000 && $w1nr == 0 && ! -s "$X/w1n-e" ]] || w1nh=bad; le "$w1nw" 0.5 || w1ns=bad
        timed V15-W1n-mount-table-read-in-one-pass $w1nh $w1ns "1000 tmpfs mounts stacked in a private mount namespace ($w1nn made, the table $w1nl lines): _sg_relax_nowslfs on the real table returned $w1nr (want 0) in ${w1nw} s (want <= 0.5), stderr $(wc -c 2>/dev/null < "$X/w1n-e" || echo '?') bytes (want 0)"
      fi
    fi
  fi
```

V15-T2 注释（m-3）：

```bash
  if sel V15-T2-anchor-taken-once-at-hook-start; then   # the anchor _SG_P0 is taken once, at the hook start: (a) one assignment, on the line after set -uo pipefail;
    # (b) with the anchor 2.0 s back and budget 3 the judgement inside the job sees 0 < left <= 1.0 s: a fresh anchor in the gate, the run or the job
    # (a bad implementation) gives about 3 s there, and a slow host only makes the value smaller. The value is fixed by the two _sg_relax_left calls, in the
    # gate and in the run (the job gets the run's): more than 1.0 s from setting the anchor here to those calls closes the gate or makes the run fall back,
    # and the judgement never runs (_SG_LEFT [], a false red)
```

### 能红证明（`prove5f3.sh`，PATH 上的 bash 5.2.15，MODE relax，`SC_ONLY='^V15-W1[a-m]'`；W1n 另跑，见第五节）

坏实现（只在 `t005f3/bad/`，由 `prove5f3.sh` 里的 Python 段从改后 hook 生成）：`v33fn` = 函数换回 v3.3（与 `spec-probe2/old.sh` 逐字相同，已断言）；`nox` = 去掉 `[[ -x "$d" ]] || return 1` 一行；`order` = 删第二行、在环境变量行后放回 v3.3 那行（挪回平台判据之前）；`w1e-a` = 删 `_sg_relax_nowslfs || return 1`（W1e 关门面的坏实现）；`w1e-b` = 改成 `! _sg_relax_nowslfs || return 1`（开门面的坏实现）。

```
load0 0.91 0.86 0.95
mkbad rc=0 v3.3 function of the pre hook == spec-probe2/old.sh: True built nox order v33fn w1e-a w1e-b 
good   FAIL [] (want []) PASS 13 other 0 | 
v33fn  FAIL [fghijkl] (want [fghijkl]) PASS 6 other 0 | f:[status]  g:[status]  h:[status]  i:[status]  j:[status] [stderr]  k:[status]  l:[status]  
nox    FAIL [k] (want [k]) PASS 12 other 0 | k:[status]  
order  FAIL [m] (want [m]) PASS 12 other 0 | m:[platform] [time]  
w1e-a  FAIL [em] (want [em]) PASS 11 other 0 | m:[control]  e:[closed]  
w1e-b  FAIL [e] (want [e]) PASS 12 other 0 | e:[open] [closed]  
load1 1.08 0.89 0.96
```

## 四、测试侧 WSL 判据与 hook 函数的对照（主控 12 种情形，`spec-probe2/` 的假挂载表与 fx 目录）

四份判据的函数体相同（`edit5f3.py` 的 WM_BODY）：`cat` 读表（读不出或 0 字节算有标记）、`awk` 取该挂载点各行的类型再 `tail -n 1`（最上层）、不是 binfmt_misc 就没有标记、`( cd -- DIR )` 失败算有（不可查）、再逐个 `[ -e ]` 两个名字。与 hook 的写法不同（hook 用 awk 的 NR、`-x`），结论相反为一致。

```bash
wslmark() {   # [MOUNTS [DIR]] : status 0 where the gate must see a WSL mark in the file system -- the rule of the hook's _sg_relax_nowslfs (What 1 supplement 2,
  # v3.4), written apart from it, never sourced or called (status 0 here is status 1 there): the mount table (default /proc/self/mounts) cannot be read or
  # reads empty; or the topmost mount at DIR (default /proc/sys/fs/binfmt_misc; the table's last line for it) is a binfmt_misc file system and DIR cannot
  # be searched (cd fails) or holds WSLInterop or WSLInterop-late (each name tested on its own: no glob, no listing). DIR is looked at only under a topmost
  # binfmt_misc, so the check never triggers an automount. The two arguments exist to check it against the hook's function; WSLM below calls it with none
  local t y d="${2:-/proc/sys/fs/binfmt_misc}"
  t=$(cat -- "${1:-/proc/self/mounts}" 2>/dev/null && echo .) || return 0
  [[ "$t" != . ]] || return 0
  y=$(printf '%s\n' "${t%.}" | awk -v d="$d" '$2 == d { print $3 }' | tail -n 1)
  [[ "$y" == binfmt_misc ]] || return 1
  ( cd -- "$d" ) >/dev/null 2>&1 || return 0
  [ -e "$d/WSLInterop" ] || [ -e "$d/WSLInterop-late" ]
}
```

5.2.15 的逐条结果：

```
host                 hook=0 (want 0) stderr=0 | helper=1 scdirect=1 suite=1 sccases=1  ok
autofs+WSLInterop    hook=0 (want 0) stderr=0 | helper=1 scdirect=1 suite=1 sccases=1  ok
binfmt+late          hook=1 (want 1) stderr=0 | helper=0 scdirect=0 suite=0 sccases=0  ok
binfmt+none          hook=0 (want 0) stderr=0 | helper=1 scdirect=1 suite=1 sccases=1  ok
stacked+WSLInterop   hook=0 (want 0) stderr=0 | helper=1 scdirect=1 suite=1 sccases=1  ok
empty                hook=1 (want 1) stderr=0 | helper=0 scdirect=0 suite=0 sccases=0  ok
unreadable           hook=1 (want 1) stderr=0 | helper=0 scdirect=0 suite=0 sccases=0  ok
dir-as-table         hook=1 (want 1) stderr=0 | helper=0 scdirect=0 suite=0 sccases=0  ok
noglob+late          hook=1 (want 1) stderr=0 | helper=0 scdirect=0 suite=0 sccases=0  ok
failglob+none        hook=0 (want 0) stderr=0 | helper=1 scdirect=1 suite=1 sccases=1  ok
nosearch-000         hook=1 (want 1) stderr=0 | helper=0 scdirect=0 suite=0 sccases=0  ok
listless-0311+late   hook=1 (want 1) stderr=0 | helper=0 scdirect=0 suite=0 sccases=0  ok
# 5.2.15: 12 cases, 0 not ok
```

五个 bash 的汇总：

```
# 3.2.57: 12 cases, 0 not ok
# 5.0.18: 12 cases, 0 not ok
# 5.1.16: 12 cases, 0 not ok
# 5.2.15: 12 cases, 0 not ok
# 5.3.20: 12 cases, 0 not ok
```

## 五、各轮预期、结果与首尾负载

预期（开跑前写，`expect.md`）：

```markdown
# 5f3 预期 (先写后跑)
## prove5f3.sh
- 能红 (PATH bash 5.2.15, MODE relax, W1n 除外): good FAIL [] PASS 13; v33fn FAIL [fghijkl] (空表/叠 autofs/目录当表/noglob/failglob 应红, 另 000 与 0311 两条也红); nox FAIL [k]; order FAIL [m] ([platform] [time]); w1e-a FAIL [em] (W1e [closed], W1m [control]); w1e-b FAIL [e] ([open] [closed])
- 测试侧判据对照 (3.2.57/5.0.18/5.1.16/5.2.15/5.3.20): 12 种情形 0 不一致; hook 结论 host 0, autofs 0, late 1, none 0, stacked 0, empty 1, unreadable 1, dir 1, noglob 1, failglob 0, nosearch 1, listless 1; stderr 全 0
- 变异生成: mutants.py rc 0 (57 个坏实现, 7 个扰动); w14-mutants.py rc 0
- commentsync: target / baseline / proto GREEN; 四个构造 RED (计数与 5f2 的 77/59/58/57 接近, hook 两个可能因站点 1 多一个新单元而变)
## runall3.sh
- perf-good (4 个放宽 bash): TIMED ok ok, 墙钟 < 0.1 s; perf-v33fn: TIMED ok bad, 墙钟约 2 s (负载首尾 < 2 时才算数)
- w10 过滤轮: 5.x 四轮无 FAIL/MISSING; 3.2.57 放宽用例 SKIP [platform], W1a-m PASS
- full-path: 无 FAIL, 计数 990 (无 zsh 984) 与头注释一致; full-wsl: 放宽用例 SKIP [platform], 其余 PASS
- sc-cases: 无 FAIL/MISSING; run-mutants 两种模式: 全部 CAUGHT, P-0 GREEN; w14: 与上一段同 (not judged 0)
```

`runall3.sh` 的步骤记录（每步开跑前等一分钟负载 < 1.2；load0 / load1 是该步首尾）：

```
perf-good-5.2.15 rc=0 load0=[1.08 0.89 0.96] load1=[1.07 0.89 0.96] secs=2
perf-v33fn-5.2.15 rc=0 load0=[1.07 0.89 0.96] load1=[1.07 0.89 0.96] secs=4
w10-5.0.18 rc=0 load0=[1.07 0.89 0.96] load1=[1.45 1.01 1.00] secs=49
perf-good-5.0.18 rc=0 load0=[1.09 0.99 0.99] load1=[1.17 1.00 1.00] secs=52
w10-5.1.16 rc=0 load0=[1.17 1.00 1.00] load1=[0.82 0.93 0.97] secs=51
perf-good-5.1.16 rc=0 load0=[0.82 0.93 0.97] load1=[0.82 0.93 0.97] secs=2
w10-5.2.15 rc=0 load0=[0.82 0.93 0.97] load1=[1.05 0.96 0.98] secs=49
w10-5.3.20 rc=0 load0=[1.05 0.96 0.98] load1=[0.79 0.90 0.96] secs=50
perf-good-5.3.20 rc=0 load0=[0.79 0.90 0.96] load1=[0.79 0.90 0.96] secs=2
w10-3.2.57 rc=0 load0=[0.79 0.90 0.96] load1=[1.46 1.06 1.02] secs=38
full-path rc=0 load0=[1.04 0.99 0.99] load1=[2.26 1.76 1.31] secs=350
full-wsl rc=0 load0=[1.13 1.55 1.27] load1=[1.98 1.87 1.49] secs=396
sc-cases rc=0 load0=[1.05 1.64 1.43] load1=[1.07 1.55 1.41] secs=101
mut-v31 rc=0 load0=[1.07 1.55 1.41] load1=[1.56 1.53 1.43] secs=218
mut-suite rc=1 load0=[1.02 1.39 1.39] load1=[1.54 1.76 1.56] secs=254
mut-suite-nj rc=0 load0=[1.05 1.60 1.52] load1=[1.07 1.51 1.49] secs=112
mut-suite-p0 rc=0 load0=[1.07 1.51 1.49] load1=[1.35 1.50 1.48] secs=51
w14 rc=0 load0=[1.04 1.41 1.46] load1=[0.80 1.28 1.41] secs=105
ALL DONE 2026-10-25T08:06:59Z load [0.80 1.28 1.41]
```

各轮摘要：

- w10-5.0.18: FAIL/MISSING/SETUP 行 1；SKIP: 0 / 158 (platform 0, load 0, void 0, inconclusive 0, root 0, other 0) / W10 ported cases: SC_BASH /home/dev/.aria/tools/bash-5.0.18/bash (x86_64-pc-linux-gnu 5.0) -> relaxation expected: yes | load start 1.15 0.91 0.97 end 1.45 1.01 1.00 | timing batch: judged
- w10-5.1.16: FAIL/MISSING/SETUP 行 1；SKIP: 0 / 158 (platform 0, load 0, void 0, inconclusive 0, root 0, other 0) / W10 ported cases: SC_BASH /home/dev/.aria/tools/bash-5.1.16/bash (x86_64-pc-linux-gnu 5.1) -> relaxation expected: yes | load start 1.17 1.00 1.00 end 0.82 0.93 0.97 | timing batch: judged
- w10-5.2.15: FAIL/MISSING/SETUP 行 1；SKIP: 0 / 158 (platform 0, load 0, void 0, inconclusive 0, root 0, other 0) / W10 ported cases: SC_BASH /usr/bin/bash (x86_64-pc-linux-gnu 5.2) -> relaxation expected: yes | load start 0.82 0.93 0.97 end 1.05 0.96 0.98 | timing batch: judged
- w10-5.3.20: FAIL/MISSING/SETUP 行 1；SKIP: 0 / 158 (platform 0, load 0, void 0, inconclusive 0, root 0, other 0) / W10 ported cases: SC_BASH /home/dev/.aria/tools/bash-5.3.20/bash (x86_64-pc-linux-gnu 5.3) -> relaxation expected: yes | load start 1.05 0.96 0.98 end 0.79 0.90 0.96 | timing batch: judged
- w10-3.2.57: FAIL/MISSING/SETUP 行 1；SKIP: 67 / 158 (platform 67, load 0, void 0, inconclusive 0, root 0, other 0) / W10 ported cases: SC_BASH /home/dev/.aria/tools/bash-3.2.57/bash (x86_64-unknown-linux-gnu 3.2) -> relaxation expected: no | load start 0.81 0.90 0.96 end 1.46 1.06 1.02 | timing batch: judged
- full-path: FAIL/MISSING/SETUP 行 1；SKIP: 0 / 984 (platform 0, load 0, void 0, inconclusive 0, root 0, other 0) / W10 ported cases: SC_BASH /usr/bin/bash (x86_64-pc-linux-gnu 5.2) -> relaxation expected: yes | load start 1.04 0.99 0.99 end 0.82 0.93 0.97 | timing batch: judged
- full-wsl: FAIL/MISSING/SETUP 行 1；SKIP: 0 / 984 (platform 0, load 0, void 0, inconclusive 0, root 0, other 0) / W10 ported cases: SC_BASH /usr/bin/bash (x86_64-pc-linux-gnu 5.2) -> relaxation expected: yes | load start 1.13 1.55 1.27 end 1.12 1.47 1.26 | timing batch: judged
- sc-cases: FAIL/MISSING/SETUP 行 0；PASS V0-H2-case-list all 158 expected case ids of mode relax reported once / # totals: PASS 160  FAIL 0  MISSING 0  SETUP 0  SKIP 0 (load 0, void 0, inconclusive 0, root 0)

run-mutants：

- mut-v31：63 CAUGHT 1 GREEN
- mut-suite：63 CAUGHT 1 NOT-JUDGED
- mut-suite-nj：1 GREEN
- mut-suite-p0：1 GREEN

```
P-0               NOT-JUDGED   the constants perturbed: _SGV_GMAX=8190, _SGV_LMAX=8200 (every case must stay green: the cases read the constants from the hook) | # run-suite.sh end | load 1.59 1.77 1.57 | suite exit 0 | load start 2.30 1.90 1.59 end 1.59 1.77 1.57 | timing batch: SKIP [load] | SKIP other than [platform]: V4-S1-allow V4-S2-block-with-text V4-S3-block-without-text V3-S4-slow-judgement V5-S5-pipe-holder V4-S6-spoofed-tail-0 V4-S7-time-checkpoint V4-S8-internal-error V5-S9-child-left-behind V5-S13-detached-child V4-S11-bare-zero V5-S10-timer-fork-fails V5-S10c-dead-timer-no-judgement V5-S14-failing-sleep-kills-at-once V4-S19-block-text-bytes V15-W1n-mount-table-read-in-one-pass V7-E1-benign-big-allowed V6-E2-deadline-fallback-bytes V3-E3-anchor-at-hook-start V3-E4-cap-3-at-budget-4 V3-E5-budget-2 V2-E6-flag-from-environment-ignored V2-E7-no-time-left V2-E8-ostype-from-environment-ignored V9-E10-count-axis-read-blocked V9-E11-tmax-in-rerun V7-E13-multiline-copy-normal-text V7-E14-long-line-from-expansion V7-E15-credit-as-normal V5-E19-deadline-with-term-ignored 
P-0               GREEN        the constants perturbed: _SGV_GMAX=8190, _SGV_LMAX=8200 (every case must stay green: the cases read the constants from the hook) | # run-suite.sh end | load 1.07 1.51 1.49 | suite exit 0 | load start 1.05 1.60 1.52 end 1.07 1.51 1.49 | timing batch: judged
P-0               GREEN        the constants perturbed: _SGV_GMAX=8190, _SGV_LMAX=8200 (every case must stay green: the cases read the constants from the hook) | # run-suite.sh end | load 1.35 1.50 1.48 | suite exit 0 | load start 1.07 1.51 1.49 end 1.35 1.50 1.48 | timing batch: judged
P-0               GREEN        the constants perturbed: _SGV_GMAX=8190, _SGV_LMAX=8200 (every case must stay green: the cases read the constants from the hook) | # totals: PASS 160  FAIL 0  MISSING 0  SETUP 0  SKIP 0 (load 0, void 0, inconclusive 0, root 0) | load start 1.34 1.56 1.44 end 1.19 1.46 1.41 | timing batch: judged
```

w14（本段 / 5f2）：

```
# end | 2026-10-25T08:06:59Z | load 0.80 1.28 1.41 | caught as predicted 26, caught by the added case 5, caught elsewhere 0, not judged 0, NOT CAUGHT 0
# end | 2026-10-25T06:15:42Z | load 1.12 1.34 1.45 | caught as predicted 26, caught by the added case 5, caught elsewhere 0, not judged 0, NOT CAUGHT 0
```

开销用例单跑（helper 直跑，TIMED 行的判定按 INV-7 看该步首尾负载，均 < 2）：

```
perf-good-5.0.18.txt: TIMED V15-W1n-mount-table-read-in-one-pass ok ok 1000 tmpfs mounts stacked in a private mount namespace (1000 made, the table 1041 lines): _sg_relax_nowslfs on the real table returned 0 (want 0) in 0.009 s (want <= 0.5), stderr 0 bytes (want 0)
perf-good-5.1.16.txt: TIMED V15-W1n-mount-table-read-in-one-pass ok ok 1000 tmpfs mounts stacked in a private mount namespace (1000 made, the table 1041 lines): _sg_relax_nowslfs on the real table returned 0 (want 0) in 0.009 s (want <= 0.5), stderr 0 bytes (want 0)
perf-good-5.2.15.txt: TIMED V15-W1n-mount-table-read-in-one-pass ok ok 1000 tmpfs mounts stacked in a private mount namespace (1000 made, the table 1041 lines): _sg_relax_nowslfs on the real table returned 0 (want 0) in 0.008 s (want <= 0.5), stderr 0 bytes (want 0)
perf-good-5.3.20.txt: TIMED V15-W1n-mount-table-read-in-one-pass ok ok 1000 tmpfs mounts stacked in a private mount namespace (1000 made, the table 1041 lines): _sg_relax_nowslfs on the real table returned 0 (want 0) in 0.008 s (want <= 0.5), stderr 0 bytes (want 0)
perf-v33fn-5.2.15.txt: TIMED V15-W1n-mount-table-read-in-one-pass ok bad 1000 tmpfs mounts stacked in a private mount namespace (1000 made, the table 1041 lines): _sg_relax_nowslfs on the real table returned 0 (want 0) in 2.219 s (want <= 0.5), stderr 0 bytes (want 0)
```

commentsync 与变异生成（`prove5f3.sh`，首尾负载见上面 load0 / load1 行）：

```
load0 0.91 0.86 0.95
gen v31 rc=0 57 bad implementations, 7 perturbation variants; hook sha256 16996eb7db21
gen w14 rc=0 lines 31 Q-31	83db84f17745	rerun: the growth limit uses _SGV_SMAX instead of _SGV_GMAX (both are 8192 today)
derive rc=0 hook sites [('1 header: shell variable indirection', 2, 3), ('2 W10 head + LENGTH BUDGET', 1, 1), ('5 _sg_vx_pass', 1, 1), ('10 relaxed rerun block (supplement 
commentsync 5f2 -> 5f3: 2 diff lines
constr: hook anchors 12 insert: anchors left 0 | delete: lines removed 217 suite anchors 10 insert: anchors left 0 | delete: lines removed 32 
cs target rc=0 target: GREEN
cs baseline rc=0 baseline: GREEN
cs proto rc=0 proto --hook-only: GREEN
cs hook-c1-insert rc=1 target --hook-only: RED (78)
cs hook-c2-delete rc=1 target --hook-only: RED (60)
cs suite-c1-insert rc=1 target --suite-only: RED (58)
cs suite-c2-delete rc=1 target --suite-only: RED (57)
load1 1.08 0.89 0.96
runall3 started, pid 2446093
```

derive 日志：

```
hook sites [('1 header: shell variable indirection', 2, 3), ('2 W10 head + LENGTH BUDGET', 1, 1), ('5 _sg_vx_pass', 1, 1), ('10 relaxed rerun block (supplement 4)', 1, 2)] suite sites [('9 test W10 block head (3b)', 2, 2)]
hook 10 relaxed rerun block (supplement 4): new unit already in the baseline/prototype run, left out: '_sg_per_segment_eval re-runs the W10 pass with the relaxed rules (_SG_RELAXED: the copy limit is the growth over the input, _SGV_GMAX;'
suite: a changed comment run outside every site: 'Regression test suite for secret-guard.sh PreToolUse hook. Run: bash aria/hooks/tests/secr'
suite: a changed comment run outside every site: '_sg_relax_nowslfs (What 1 supplement 2, v3.4), written apart from it, never sourced or cal'
```

INV-2 与清理核对：

```
helper vs sc-direct.sh hunks: before 14, after 14
change in the text that differs between them (want: only the RELAX_IDS line of the helper):
44c44
< < V15-T1-timer-sleeps-time-left V15-T2-anchor-taken-once-at-hook-start V15-T3-job-errors-silenced V15-W1e-gate-closed-by-wsl-file-system"   # the cases of MOD
---
> < V15-T1-timer-sleeps-time-left V15-T2-anchor-taken-once-at-hook-start V15-T3-job-errors-silenced V15-W1e-gate-closed-by-wsl-file-system V15-W1n-mount-table-r
leftover w1 dirs under /tmp: 0
runall3 pid 2446093 alive: 0
worktree status:
 M hooks/secret-guard.sh
 M hooks/tests/lib/secret-guard-w10-direct.sh
 M hooks/tests/secret-guard.test.sh
main repo status:
 M .aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/commentsync.py
 M .aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/impl/w14-mutants.py
 M .aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/mutants.py
 M .aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/sc-cases.sh
 M .aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/sc-direct.sh
 M openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md
```

## 六、未做或拿不准的项（请主控复核）

1. **W1n 放在 MODE relax**（RELAX_IDS / EXP_DIRECT_RELAX）：proposal 没说哪种模式；我按「v3.4 只在放宽平台、有时间时才读表，开销只在那里要紧」放进 relax，非放宽 bash 上记 SKIP [platform]。若主控要它两种模式都跑，只需挪编号与代码块。
2. **W1n 的「单独跑」只做到一半**：5 个 bash 的过滤轮用 `SG_W10_ONLY` 把它排除（正则 `^(V([0-9]|1[0-46-9])-|V15-T|V15-W1[a-m]-)`，过滤轮因此 158 条），在各轮之间对 4 个放宽 bash 单跑、另对 v3.3 单跑一次；但整轮、sc-cases 与两种模式的 P-0 没有排除单条用例的开关，它们里面照样含 W1n。实测单跑一次墙钟约 2 s、负载几乎不动（1.08 -> 1.07），未见影响别的计时用例。
3. **W1k 的 root 探测**只沿用了 helper 既有探测里的 `id -ru` 一项（uid 0 时 SKIP [platform]）；非 root 但带 CAP_DAC_OVERRIDE / CAP_DAC_READ_SEARCH 的进程也能查 000 目录，那时这条会假红（不会假绿）。既有的 CapEff 位检查（21、24 位）管的是另一种能力，没有照搬。
4. **W1e 的前置**：为保证「前面的判据都过」，我在子壳里加了 `unset _SG_RELAXED WSL_DISTRO_NAME WSL_INTEROP` 与显式预算 3（变量名运行时拼装写入），这超出原 W1e 的写法；id 保持不变。
5. **W1m 多了一条对照腿**（平台与时间都过时须恰好调用 1 次，标签 `[control]`），防止桩没接上时整条恒绿；`w1e-a` 坏实现证明它能红。任务书只要求前两腿。
6. 套件 `full-wsl` 轮里套件自己的判定仍是「relaxation expected: yes」（套件对每次运行 hook 都清掉 WSL 环境变量，与 5f2 相同），所以该轮也跑了 W1n。
7. 头注释那句的措辞是我拟的（同义而非逐字照抄块头），commentsync 把它当站点 1 的新单元收录。

## 七、收尾时发现：主仓 proposal.md 在工作区里是已修改状态

收尾的 `git status` 显示主仓 `openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md` 为 M。本席没有改它（`edit5f3.py` 只读它，抽取两个 v3.4 代码块），应是并发的别处改动；按任务书不碰。核对结果如下：当前工作区版本里的两个 v3.4 代码块仍逐字在改后的 hook 里，所以本段的 hook 与当前 proposal 一致。改了哪些段请主控看 `git diff`。

```
proposal mtime 2026-10-25 07:13:58; edit5f3.out mtime 2026-10-25 07:27:21; HEAD 7f9989b8 docs(openspec): secret-guard-w10-failclosed-narrowi
 1 file changed, 1 insertion(+), 1 deletion(-)
@@ -152 +152 @@ _sg_relax_nowslfs() {   # [MOUNTS [DIR]]: status 0 only when no 
current proposal v3.4 blocks still in the hook verbatim: line1 True line2 True function True
```

# T005f4 报告：TASK-005 修复轮第四段（10CG/aria-plugin#217）

执笔席（全新实例），2026-10-25。脚本与证据都在 `r217impl/t005f4/`：`expect.md`（先写的预期）、`edit5f4.py`（全部改动，从 `pre/` 的改前副本出发，可重放）、`prove5f4.sh`（bash -n、坏实现、能红 / 能 SKIP、判据对照、变异生成、commentsync）、`runall4.sh`（各轮）、`q17.sh`（W14 Q-17 单独重跑）、`proofs/`、`runs/`、`diffs/`、`cs/`、`bad/`、`mnt/`（mount 包装）。没有 commit。

## 结论一览

- **A hook**：按 proposal v3.5（What 1 补充 2）两个代码块用脚本取出后替换：`_sg_relax_ok` 里 `_sg_relax_nowslfs || return 1` 那行（只有行尾注释变）、整个 `_sg_relax_nowslfs`（函数头注释、读出 0 行与 binfmt_misc 两行的注释、`[[ -d "$d" && -x "$d" ]] || return 1`）。只动 5 行（-5 +5），行数 1756 不变；准入门 WSL 环境那行与 D-3 那句未动。proposal 的函数块与 `spec-probe2/spec5.sh` 逐字相同。新 hook sha256 前缀 **628652570ce3**（旧 16996eb7db21）。
- **B 用例**：新增 `V15-W1o-regular-file-as-directory`（两种模式、不分 uid）；W1l 在 uid 0 下记 SKIP [platform]（照 W1k）；W1n 叠到 1-999 层停下时记 SKIP [platform]；helper、`v31/sc-direct.sh` 同一组改动（INV-2：两份文件之间的差异行改前改后完全相同，77 行），清单（helper 的 miss 清单、套件 `SGW_EXP_DIRECT`、`sc-cases.sh` 期望清单）与套件头注释计数（990 -> 991、984 -> 985）已改。能红 / 能 SKIP 证明全部如预期。
- **判据对照**：主控 13 种情形 x 5 个 bash，hook 的函数与四份测试侧判据逐种全一致（`13 cases, 0 not ok` x 5），hook 的 stderr 全程 0 字节；四份判据导出与 5f3 逐字相同（未改）。
- **C 工具**：`mutants.py` 与 w14 Q-30 的锚点只到 `_sg_relax_nowslfs` 行首，不受 A 影响，未改；两者在新 hook 上全部能生成（57 + 7；31）。`impl/w14-mutants.py` 只改 `IMPL_SHA12` 为 628652570ce3。commentsync 照第三段做法从 eeb67786 版重新导出，结果与 5f3 版逐字相同（git 无变化）；target / baseline / proto GREEN，四个构造 RED（78、60、58、57，与 5f3 相同）。
- **各轮**：全部 0 FAIL / MISSING / SETUP；过滤轮 5 个 bash 各 159 条（5f3 为 158）；整轮两轮各 985 条（5f3 为 984；本机无 zsh）；sc-cases PASS 161；run-mutants 两种模式 BI 全 CAUGHT、P-0 GREEN（suite 模式第一轮在负载下有 3 个 BI 与 P-0 NOT-JUDGED，按 runall3 的做法低负载重跑后全判）；w14 NOT CAUGHT 0、not judged 0，但 Q-17 一条从「caught as predicted」变成「caught elsewhere」（见下面不符第 3 条）。

## 预期与结果不符（逐条）

1. **helper / sc-direct 行数**（expect.md E2）：预期 helper 681 -> 690；实际 692（sc-direct 638 -> 649）。原因是我写预期之后把 W1o 的 if 行注释折成了两行（W1o 块 5 行而非 4 行）、W1n 补的注释是 2 行而非 1 行。属预期写错，改动内容见第 2 节。
2. **commentsync 导出的 diff**（P5）：预期与 5f3 版差 2 行（FIX5_HOOK 一行）；实际 0 行，导出与 5f3 版逐字相同。derive 的输出把每个站点记成（站点名, 删的单元数, 增的单元数），如 `('1 header: shell variable indirection', 2, 3)`；本轮只改了已有注释单元的文字，没有增删单元，所以导出不变。我推测 commentsync 只比对单元的增删、不比对单元里的文字——这意味着本轮这几处注释措辞的改动它看不到；没有读它的源码证实，留主控判断是否要紧。
3. **w14 的分布**：预期与 5f3 相同（caught as predicted 26、caught by the added case 5、caught elsewhere 0）；实际 25 / 5 / **1**，not judged 0、NOT CAUGHT 0。那一条是 Q-17（job 的命令替换不再静默自己的 stderr）：预期抓手 V6-E2-deadline-fallback-bytes 这次是 PASS，由整轮里 V3-S4、V5-S5、V4-S6、V15-T3 等多条 FAIL 抓到。之后单独重跑 Q-17 两次（`q17.sh`，首尾负载 1.02/1.01、1.01/0.93）都是 caught as predicted（V6-E2 FAIL [bytes]）。本轮没有碰 job 与截止相关的代码，我判断是 V6-E2 在这个变异上的抓取依赖时序、整跑那一次没抓到，不是本轮引入；这一点没有进一步证明。
4. **（过程，非结果）** prove 的后台 PID 记成了 setsid 的包装进程（本会话 Bash 工具的 shell 开着作业控制，setsid 因此另 fork 一层），第一次等待提前返回，当时看到的 prove 输出不全；之后按输出文件末行（`runall4 started`）确认 prove 已跑完。runall4 的 PID 由脚本自己写 `$$`，等待与「ALL DONE」一致。没有杀过任何进程；收尾时命令行含 t005f4 的进程为 0（见第 6 节）。

## 未做或拿不准的项

- **W1l 的 uid 0 分支**本机造不出（uid 1000），只做了代码审读：与 W1k 同形（`[[ "$(id -ru)" == 0 ]]` 时 `out SKIP ... "[platform] ..."`，否则原样构造并判定）；uid 1000 下 W1l 照旧判定（各轮 PASS）。
- **W1n 注释**：3ed6c24 里这条的注释截断在「soft (INV-7): the wall」（edit5f3.py 的模板里就是这样）。本轮改 W1n 时补成「the wall time, at most 0.5 s」并加一句 SKIP 的三种情形——超出任务书逐条列出的范围，请主控确认措辞。
- **helper W1 段头注释**（「A table that cannot be read or reads empty, or a DIR that cannot be searched, keeps the relaxation off」）没有随 v3.5 改成「not a directory that can be searched」：任务书没列，字面仍成立（普通文件同样查不了），保留未动。
- 没有为 W1o / `-d` 判据新增 v31 变异（任务书没要求）；`nodx`、`donly` 两个坏实现只在 scratchpad 里用来证明 W1k 钉住 `-x`、W1o 钉住 `-d`。
- 复审第三轮观察二（假表路径含空白时 W1b / W1i / W1l 假红）按主控裁定只记录；新 W1o 用同一种假表写法，同样受影响。
- INV-7：步级首尾负载 >= 2 的步有 full-path（尾 2.08）、full-wsl（尾 1.98，未到 2）、mut-v31（尾 2.21）、mut-suite（尾 2.37，已按 NOT-JUDGED 重跑）。这些步里的计时判定由套件 / run-mutants 自己的批内读数决定（均 judged，或已重跑判定）；步级读数不作为计时结论的依据。W1n 的计时（perf 各步）首尾负载都 < 2。

## 1. hook 完整 diff（相对 3ed6c24）

```diff
diff --git a/hooks/secret-guard.sh b/hooks/secret-guard.sh
index c7d445d..09e8d8f 100755
--- a/hooks/secret-guard.sh
+++ b/hooks/secret-guard.sh
@@ -832,18 +832,18 @@ _sg_relax_ok() {   # status 0 when the relaxation is in effect for this command;
   [[ -n "${WSL_DISTRO_NAME:-}${WSL_INTEROP:-}" ]] && wsl=wsl   # WSL marks in the environment; the environment can only switch the relaxation off with them
   _sg_relax_platform "${BASH_VERSINFO[5]:-}" "${BASH_VERSINFO[0]:-0}" "${BASH_VERSINFO[1]:-0}" "$osr" "$wsl" || return 1   # read-only build and kernel facts, which the environment cannot rewrite (OSTYPE, MACHTYPE and HOSTTYPE can be)
   _sg_relax_left || return 1
-  _sg_relax_nowslfs || return 1   # the WSL mark of the file system (a WSLInterop entry under binfmt_misc, or a mount table that cannot be read), asked only where the platform and the time would relax: elsewhere the mount table is never read
+  _sg_relax_nowslfs || return 1   # the WSL mark of the file system (_sg_relax_nowslfs: a WSLInterop or WSLInterop-late entry seen under a topmost binfmt_misc, a DIR there that cannot be searched, or a mount table that cannot be read or reads empty), asked only where the platform and the time would relax: elsewhere the mount table is never read
   [[ "$( _sg_relax_noext 2>/dev/null )" == none ]]
 }
 _sg_relax_platform() {   # MACHINE MAJOR MINOR OSRELEASE [WSL]: status 0 on an x86_64 GNU/Linux build of a bash version the mechanism was measured on, 5.0 to 5.3, outside WSL (owner ruling E, 2026-10-22 and 2026-10-23: an untested platform -- macOS, Windows, WSL1 and WSL2, musl, Android, aarch64 and other architectures, another bash -- keeps the baseline)
   [[ "${1:-}" == x86_64-*-linux-gnu* && -n "${4:-}" && "${4:-}" != *[Mm]icrosoft* && "${4:-}" != *WSL* && -z "${5:-}" ]] && (( ${2:-0} == 5 && ${3:-0} <= 3 ))
 }
-_sg_relax_nowslfs() {   # [MOUNTS [DIR]]: status 0 only when no WSL interop entry can exist -- the mount table (default /proc/self/mounts) reads and is not empty, and the topmost mount at DIR (default /proc/sys/fs/binfmt_misc; the table's last line for it) is not a binfmt_misc file system, or it is, DIR can be searched, and it holds neither WSLInterop nor WSLInterop-late. awk reads the table in one pass: a line-by-line read of /proc/self/mounts in bash costs O(n^2) (bash seeks back after every line and procfs regenerates the table from the start), seconds on a host with a few thousand mounts, outside the hard deadline. The entries are looked at only when binfmt_misc is the topmost mount there, so the look never triggers an automount; the two names are tested one by one, not by a glob, so noglob or failglob imported from the environment cannot change the look. A table that cannot be read, or reads empty, keeps the relaxation off. The two arguments exist for the direct-call cases only; the gate calls it with none
+_sg_relax_nowslfs() {   # [MOUNTS [DIR]]: status 0 only when no WSL interop entry is seen -- the mount table (default /proc/self/mounts) reads and is not empty, and the topmost mount at DIR (default /proc/sys/fs/binfmt_misc; taken to be the table's last line for it) is not a binfmt_misc file system, or it is, DIR is a directory that can be searched, and it holds neither WSLInterop nor WSLInterop-late. awk reads the table in one pass: a line-by-line read of /proc/self/mounts in bash costs O(n^2) (bash seeks back after every line and procfs regenerates the table from the start), seconds on a host with a few thousand mounts, outside the hard deadline. The entries are looked at only when binfmt_misc is the topmost mount there, so the look never triggers an automount; an entry under a lower mount (a binfmt_misc with another mount on top of it) is not looked for and counts as none. The two names are tested one by one, not by a glob, so noglob or failglob imported from the environment cannot change the look. A table that cannot be read, or reads empty, keeps the relaxation off, and so does a DIR that is not a directory that can be searched. The two arguments exist for the direct-call cases only; the gate calls it with none
   local d="${2:-/proc/sys/fs/binfmt_misc}" r
   r=$(awk -v d="$d" '$2 == d { t = $3 } END { print NR, t }' "${1:-/proc/self/mounts}" 2>/dev/null) || return 1
-  [[ "${r%% *}" =~ ^[1-9][0-9]*$ ]] || return 1   # no line read: a table that cannot be read
-  [[ "${r#* }" == binfmt_misc ]] || return 0   # binfmt_misc is not the topmost mount at DIR: no interop entry can be registered there, and nothing under DIR is looked at
-  [[ -x "$d" ]] || return 1   # DIR cannot be searched: the entries cannot be seen, so they may exist
+  [[ "${r%% *}" =~ ^[1-9][0-9]*$ ]] || return 1   # no line read: a table that cannot be read, or reads empty
+  [[ "${r#* }" == binfmt_misc ]] || return 0   # binfmt_misc is not the topmost mount at DIR: nothing under DIR is looked at (an entry under a lower mount is not looked for: looking could trigger an automount)
+  [[ -d "$d" && -x "$d" ]] || return 1   # DIR is not a directory that can be searched: the entries cannot be seen, so they may exist
   [[ -e "$d/WSLInterop" || -e "$d/WSLInterop-late" ]] && return 1
   return 0
 }
```

## 2. 新用例与改过的用例

helper（`hooks/tests/lib/secret-guard-w10-direct.sh`）的 diff 如下；`v31/sc-direct.sh` 是同一组改动（行号不同）。

```diff
diff --git a/hooks/tests/lib/secret-guard-w10-direct.sh b/hooks/tests/lib/secret-guard-w10-direct.sh
index 15b959a..36d5628 100755
--- a/hooks/tests/lib/secret-guard-w10-direct.sh
+++ b/hooks/tests/lib/secret-guard-w10-direct.sh
@@ -202,11 +202,19 @@ if need _sg_relax_nowslfs; then
       w1x V15-W1k-unsearchable-directory "$X/w1-nosearch-mounts" "$w1k" 1 "binfmt_misc mounted at DIR, DIR of mode 000 (cannot be searched; nothing in it)"; chmod 755 "$w1k"
     fi
   fi
-  if sel V15-W1l-unlistable-directory-with-wslinterop-late; then   # a DIR that can be searched but not listed (mode 0311): each name is still seen, where a glob sees none (review R2 m-1)
-    w1l="$X/w1-listless"; mkdir -p "$w1l"; : > "$w1l/WSLInterop-late"; printf 'binfmt_misc %s binfmt_misc rw,nosuid,nodev,noexec,relatime 0 0\nproc /proc proc rw,nosuid,nodev,noexec,relatime 0 0\n' "$w1l" > "$X/w1-listless-mounts"; chmod 0311 "$w1l"
-    w1x V15-W1l-unlistable-directory-with-wslinterop-late "$X/w1-listless-mounts" "$w1l" 1 "binfmt_misc mounted at DIR, DIR of mode 0311 (searched, not listed) holding WSLInterop-late"; chmod 755 "$w1l"
+  if sel V15-W1l-unlistable-directory-with-wslinterop-late; then   # a DIR that can be searched but not listed (mode 0311): each name is still seen, where a glob sees none (review R2 m-1). uid 0 lists any directory, so there a look name by name cannot be told from a glob: not applicable there (review R3 m-4)
+    if [[ "$(id -ru)" == 0 ]]; then out SKIP V15-W1l-unlistable-directory-with-wslinterop-late "[platform] uid 0 lists any directory, one of mode 0311 too, so here the case cannot tell a look name by name from a glob"
+    else
+      w1l="$X/w1-listless"; mkdir -p "$w1l"; : > "$w1l/WSLInterop-late"; printf 'binfmt_misc %s binfmt_misc rw,nosuid,nodev,noexec,relatime 0 0\nproc /proc proc rw,nosuid,nodev,noexec,relatime 0 0\n' "$w1l" > "$X/w1-listless-mounts"; chmod 0311 "$w1l"
+      w1x V15-W1l-unlistable-directory-with-wslinterop-late "$X/w1-listless-mounts" "$w1l" 1 "binfmt_misc mounted at DIR, DIR of mode 0311 (searched, not listed) holding WSLInterop-late"; chmod 755 "$w1l"
+    fi
+  fi
+  if sel V15-W1o-regular-file-as-directory; then   # a DIR that is not a directory -- an empty regular file of mode 0755 that the table lists as a binfmt_misc mount point: the
+    # entries cannot be seen, so they may exist (What 1 supplement 2 v3.5; review R3 m-3: -x alone is true for such a file, and the look then finds nothing). Any uid
+    w1o="$X/w1-xfile"; : > "$w1o"; chmod 0755 "$w1o"; printf 'binfmt_misc %s binfmt_misc rw,nosuid,nodev,noexec,relatime 0 0\nproc /proc proc rw,nosuid,nodev,noexec,relatime 0 0\n' "$w1o" > "$X/w1-xfile-mounts"
+    w1x V15-W1o-regular-file-as-directory "$X/w1-xfile-mounts" "$w1o" 1 "binfmt_misc listed at DIR, DIR an empty regular file of mode 0755 (not a directory)"
   fi
-else miss V15-W1a-autofs-mount-point-not-looked-at V15-W1b-binfmt-misc-with-wslinterop-late V15-W1c-binfmt-misc-without-entry V15-W1d-unreadable-mount-table V15-W1f-empty-mount-table V15-W1g-autofs-on-top-of-binfmt-misc-not-looked-at V15-W1h-directory-as-mount-table V15-W1i-noglob-binfmt-misc-with-wslinterop-late V15-W1j-failglob-binfmt-misc-without-entry V15-W1k-unsearchable-directory V15-W1l-unlistable-directory-with-wslinterop-late; fi
+else miss V15-W1a-autofs-mount-point-not-looked-at V15-W1b-binfmt-misc-with-wslinterop-late V15-W1c-binfmt-misc-without-entry V15-W1d-unreadable-mount-table V15-W1f-empty-mount-table V15-W1g-autofs-on-top-of-binfmt-misc-not-looked-at V15-W1h-directory-as-mount-table V15-W1i-noglob-binfmt-misc-with-wslinterop-late V15-W1j-failglob-binfmt-misc-without-entry V15-W1k-unsearchable-directory V15-W1l-unlistable-directory-with-wslinterop-late V15-W1o-regular-file-as-directory; fi
 # What 1 supplement 2 (v3.4): the gate asks for the WSL mark of the file system after the platform and the time, so where either closes the gate the mount
 # table is never read. _sg_relax_nowslfs stubbed to count its calls, on a freshly sourced hook with no WSL mark in the environment; both modes
 if sel V15-W1m-mount-table-read-only-after-platform-and-time; then
@@ -655,6 +663,8 @@ EOF
   if sel V15-W1n-mount-table-read-in-one-pass; then   # What 1 supplement 2 (v3.4; review R2 M-1): awk reads the mount table in one pass. In a private mount namespace (unshare -rm) with 1000 tmpfs
     # mounts stacked on one directory, _sg_relax_nowslfs reads the real table and returns within 0.5 s (v3.3 read it line by line in bash, and procfs
     # regenerates the table at every seek back: 2.2 s there). Hard: the 1000 mounts made, status 0 (no WSL mark: MODE relax), stderr empty; soft (INV-7): the wall
+    # time, at most 0.5 s. SKIP [platform] where unshare -rm is not available, where no tmpfs can be mounted, and where the stacking stops after 1 to 999
+    # mounts (a low fs.mount-max, say; review R3): the table the case needs cannot be made there
     if ! need _sg_relax_nowslfs; then miss V15-W1n-mount-table-read-in-one-pass
     elif ! unshare -rm true >/dev/null 2>&1; then out SKIP V15-W1n-mount-table-read-in-one-pass "[platform] unshare -rm (a private user and mount namespace) is not available here"
     else
@@ -664,6 +674,7 @@ EOF
         'echo "$n $r $(grep -c "" /proc/self/mounts) ${t0/,/.} ${t1/,/.}"' > "$X/w1n.sh"
       read -r w1nn w1nr w1nl w1n0 w1n1 <<< "$(unshare -rm "$BASH" "$X/w1n.sh" "$H" "$X" 2>/dev/null)"
       if [[ "${w1nn:-0}" == 0 ]]; then out SKIP V15-W1n-mount-table-read-in-one-pass "[platform] tmpfs cannot be mounted in a private mount namespace here"
+      elif [[ $w1nn =~ ^[0-9]+$ ]] && (( w1nn < 1000 )); then out SKIP V15-W1n-mount-table-read-in-one-pass "[platform] the stacking stopped after $w1nn of 1000 tmpfs mounts (a low fs.mount-max, say), so the table the case needs cannot be made here"
       else
         w1nw=$(awk -v a="${w1n0:-0}" -v b="${w1n1:-0}" 'BEGIN{printf "%.3f", b-a}'); w1nh=ok; w1ns=ok
         [[ $w1nn == 1000 && $w1nr == 0 && ! -s "$X/w1n-e" ]] || w1nh=bad; le "$w1nw" 0.5 || w1ns=bad
```

### 能红 / 能 SKIP 的证明（`prove5f4.sh`，PATH 上的 bash 5.2.15 除注明外；坏实现在 `bad/`）

- `v34fn` = 新 hook 换回 `spec-probe2/spec3.sh`（v3.4）的函数；`nodx` = 删掉 `-d && -x` 那行；`donly` = 那行只留 `-d`；`v33fn` = v3.3 的函数（`spec-probe2/old.sh`，给开销用例）。
- W1o 能红：v3.4 的函数上 W1o FAIL（status 0, want 1），其余 13 条 PASS；两种模式都验了（3.2.57 MODE norelax 上同样 good PASS、v34fn FAIL）。
- W1n 能 SKIP：PATH 前置 `mnt/mount`（真 mount 的包装，从第 501 次起返回 32）——新 helper 记 SKIP [platform]（不是 FAIL）；从第 1 次起失败——照旧 SKIP [platform]；对照：改前的 helper 在同一包装下出 `TIMED ... bad ok`（硬判据坏，套件里即 FAIL，正是复审观察一说的硬红）。W1n 原有的红：v3.3 的函数上 `TIMED ... ok bad`（2.394 s）。
- W1l：uid 0 分支只做代码审读（见上）。

```
load0 0.79 0.99 1.15 (waited 1 x 10 s at most)
bash -n: 25 checks, stderr 0 bytes
mkbad rc=0 built donly nodx v33fn v34fn 
good   FAIL [] (want []) PASS 14 other 0 | 
v34fn  FAIL [o] (want [o]) PASS 13 other 0 | FAIL V15-W1o-regular-file-as-directory binfmt_misc listed at DIR, DIR an empty regular file of mode 0755 (not a directory): status 0 (want 1), stderr  
nodx   FAIL [ko] (want [ko]) PASS 12 other 0 | FAIL V15-W1k-unsearchable-directory binfmt_misc mounted at DIR, DIR of mode 000 (cannot be searched; nothing in it): status 0 (want 1), stderr 0 bytes FAIL V15-W1o-regular-file-as-directory binfmt_misc listed at DIR, DIR an empty regular file of mode 0755 (not a directory): status 0 (want 1), stderr  
donly  FAIL [k] (want [k]) PASS 13 other 0 | FAIL V15-W1k-unsearchable-directory binfmt_misc mounted at DIR, DIR of mode 000 (cannot be searched; nothing in it): status 0 (want 1), stderr 0 bytes 
norelax 3.2.57 good (want PASS): PASS V15-W1o-regular-file-as-directory binfmt_misc listed at DIR, DIR an empty regular file of mode 0755 (not a directory): status 1 (want 1), stderr 0 bytes (want 0)
norelax 3.2.57 v34fn (want FAIL): FAIL V15-W1o-regular-file-as-directory binfmt_misc listed at DIR, DIR an empty regular file of mode 0755 (not a directory): status 0 (want 1), stderr 0 bytes (want 0) [status]
w1n stop501 (fails from call 501; calls made 501): SKIP V15-W1n-mount-table-read-in-one-pass [platform] the stacking stopped after 500 of 1000 tmpfs mounts (a low fs.mount-max, say), so the table the case needs cannot be made here
w1n stop1 (fails from call 1; calls made 1): SKIP V15-W1n-mount-table-read-in-one-pass [platform] tmpfs cannot be mounted in a private mount namespace here
w1n pre-stop501 (fails from call 501; calls made 501): TIMED V15-W1n-mount-table-read-in-one-pass bad ok 1000 tmpfs mounts stacked in a private mount namespace (500 made, the table 541 lines): _sg_relax_nowslfs on the real table returned 0 (want 0) in 0.003 s (want <= 0.5), stderr 0 bytes (want 0)
tw-helper: same as in 5f3 (13 lines)
tw-scdirect: same as in 5f3 (13 lines)
tw-suite: same as in 5f3 (13 lines)
tw-sccases: same as in 5f3 (13 lines)
cmp 3.2.57: # 3.2.57: 13 cases, 0 not ok
cmp 5.0.18: # 5.0.18: 13 cases, 0 not ok
cmp 5.1.16: # 5.1.16: 13 cases, 0 not ok
cmp 5.2.15: # 5.2.15: 13 cases, 0 not ok
cmp 5.3.20: # 5.3.20: 13 cases, 0 not ok
gen v31 rc=0 57 bad implementations, 7 perturbation variants; hook sha256 628652570ce3
gen w14 rc=0 lines 31 Q-31	747ea3a40957	rerun: the growth limit uses _SGV_SMAX instead of _SGV_GMAX (both are 8192 today)
derive rc=0 hook sites [('1 header: shell variable indirection', 2, 3), ('2 W10 head + LENGTH BUDGET', 1, 1), ('5 _sg_vx_pass', 1, 1), ('10 relaxed rerun block (supplement 
commentsync 5f3 -> 5f4: 0 diff lines
constr: hook anchors 12 insert: anchors left 0 | delete: lines removed 217 suite anchors 10 insert: anchors left 0 | delete: lines removed 32 
cs target rc=0 target: GREEN
cs baseline rc=0 baseline: GREEN
cs proto rc=0 proto --hook-only: GREEN
cs hook-c1-insert rc=1 target --hook-only: RED (78)
cs hook-c2-delete rc=1 target --hook-only: RED (60)
cs suite-c1-insert rc=1 target --suite-only: RED (58)
cs suite-c2-delete rc=1 target --suite-only: RED (57)
load1 0.90 1.01 1.16
runall4 started, pid 2941784
```

## 3. 判据对照表（主控 13 种情形，`spec-probe2` 的 `cases5.sh` 同一组假表、目录与参数；`cmp5f4.sh` = 5f3 的 `cmp5f3.sh` 加 xfile 一条）

每格按 3.2.57 / 5.0.18 / 5.1.16 / 5.2.15 / 5.3.20 列。测试侧判据的 0 表示「有标记」（与 hook 相反），所以 hook 为 1 时四份判据应为 0。

| 情形 | 期望 hook | hook（3.2.57/5.0.18/5.1.16/5.2.15/5.3.20） | stderr 字节 | helper | sc-direct | suite | sc-cases | 判定 |
|---|---|---|---|---|---|---|---|---|
| host | 0 | 0/0/0/0/0 | 0/0/0/0/0 | 1/1/1/1/1 | 1/1/1/1/1 | 1/1/1/1/1 | 1/1/1/1/1 | ok |
| autofs+WSLInterop | 0 | 0/0/0/0/0 | 0/0/0/0/0 | 1/1/1/1/1 | 1/1/1/1/1 | 1/1/1/1/1 | 1/1/1/1/1 | ok |
| binfmt+late | 1 | 1/1/1/1/1 | 0/0/0/0/0 | 0/0/0/0/0 | 0/0/0/0/0 | 0/0/0/0/0 | 0/0/0/0/0 | ok |
| binfmt+none | 0 | 0/0/0/0/0 | 0/0/0/0/0 | 1/1/1/1/1 | 1/1/1/1/1 | 1/1/1/1/1 | 1/1/1/1/1 | ok |
| stacked+WSLInterop | 0 | 0/0/0/0/0 | 0/0/0/0/0 | 1/1/1/1/1 | 1/1/1/1/1 | 1/1/1/1/1 | 1/1/1/1/1 | ok |
| empty | 1 | 1/1/1/1/1 | 0/0/0/0/0 | 0/0/0/0/0 | 0/0/0/0/0 | 0/0/0/0/0 | 0/0/0/0/0 | ok |
| unreadable | 1 | 1/1/1/1/1 | 0/0/0/0/0 | 0/0/0/0/0 | 0/0/0/0/0 | 0/0/0/0/0 | 0/0/0/0/0 | ok |
| dir-as-table | 1 | 1/1/1/1/1 | 0/0/0/0/0 | 0/0/0/0/0 | 0/0/0/0/0 | 0/0/0/0/0 | 0/0/0/0/0 | ok |
| noglob+late | 1 | 1/1/1/1/1 | 0/0/0/0/0 | 0/0/0/0/0 | 0/0/0/0/0 | 0/0/0/0/0 | 0/0/0/0/0 | ok |
| failglob+none | 0 | 0/0/0/0/0 | 0/0/0/0/0 | 1/1/1/1/1 | 1/1/1/1/1 | 1/1/1/1/1 | 1/1/1/1/1 | ok |
| nosearch-000 | 1 | 1/1/1/1/1 | 0/0/0/0/0 | 0/0/0/0/0 | 0/0/0/0/0 | 0/0/0/0/0 | 0/0/0/0/0 | ok |
| listless-0311+late | 1 | 1/1/1/1/1 | 0/0/0/0/0 | 0/0/0/0/0 | 0/0/0/0/0 | 0/0/0/0/0 | 0/0/0/0/0 | ok |
| xfile-0755 | 1 | 1/1/1/1/1 | 0/0/0/0/0 | 0/0/0/0/0 | 0/0/0/0/0 | 0/0/0/0/0 | 0/0/0/0/0 | ok |

## 4. 各轮预期、结果与首尾负载

预期见 `expect.md`（先写）。步级记录（`runs/steps.log`，每步开跑前一分钟负载 < 1.2）：

```
perf-good-5.2.15 rc=0 load0=[0.90 1.01 1.16] load1=[0.90 1.01 1.16] secs=2
perf-v33fn-5.2.15 rc=0 load0=[0.90 1.01 1.16] load1=[0.91 1.01 1.16] secs=4
w10-5.0.18 rc=0 load0=[0.91 1.01 1.16] load1=[0.85 0.99 1.14] secs=49
perf-good-5.0.18 rc=0 load0=[0.85 0.99 1.14] load1=[0.85 0.99 1.14] secs=2
w10-5.1.16 rc=0 load0=[0.85 0.99 1.14] load1=[1.36 1.10 1.17] secs=50
perf-good-5.1.16 rc=0 load0=[1.15 1.07 1.16] load1=[1.15 1.07 1.16] secs=32
w10-5.2.15 rc=0 load0=[1.15 1.07 1.16] load1=[1.87 1.24 1.21] secs=49
w10-5.3.20 rc=0 load0=[1.19 1.15 1.18] load1=[1.33 1.18 1.19] secs=110
perf-good-5.3.20 rc=0 load0=[1.02 1.12 1.17] load1=[1.02 1.11 1.17] secs=22
w10-3.2.57 rc=0 load0=[1.02 1.11 1.17] load1=[1.22 1.15 1.18] secs=33
full-path rc=0 load0=[1.03 1.11 1.17] load1=[2.08 1.77 1.44] secs=337
full-wsl rc=0 load0=[1.16 1.56 1.39] load1=[1.98 1.87 1.57] secs=391
sc-cases rc=0 load0=[1.17 1.68 1.52] load1=[0.98 1.54 1.48] secs=101
mut-v31 rc=0 load0=[0.98 1.54 1.48] load1=[2.21 1.87 1.63] secs=218
mut-suite rc=1 load0=[1.14 1.56 1.62] load1=[2.37 1.96 1.77] secs=746
mut-suite-nj rc=0 load0=[1.06 1.65 1.68] load1=[0.78 1.46 1.61] secs=156
mut-suite-p0 rc=0 load0=[0.78 1.46 1.61] load1=[1.08 1.43 1.59] secs=51
w14 rc=0 load0=[1.08 1.43 1.59] load1=[1.13 1.34 1.52] secs=236
ALL DONE 2026-10-25T09:46:45Z load [1.13 1.34 1.52]
w14-q17-a rc=0 load0=[1.02 1.28 1.49] load1=[1.01 1.27 1.48] secs=4
w14-q17-b rc=0 load0=[1.01 1.27 1.48] load1=[0.93 1.25 1.48] secs=5
```

| 轮 | 预期 | 结果 | 符合 |
|---|---|---|---|
| bash -n（5 个 bash x 5 个文件） | 全过 | 25 项全过，stderr 0 字节 | 是 |
| perf-good（5.2.15 / 5.0.18 / 5.1.16 / 5.3.20） | TIMED ok ok，1000 层，< 0.5 s | 4 次 ok ok，1000 层，0.008-0.009 s | 是 |
| perf-v33fn（5.2.15） | TIMED ok bad，约 2 s | ok bad，2.394 s | 是 |
| 过滤轮 5 个 bash | 0 FAIL，比 5f3 多 1 条 | 各 FAIL 0 / 159（5f3 为 158）；3.2.57 SKIP 67 [platform]（与 5f3 同），其余 SKIP 0 | 是 |
| full-path | 0 失败，985 | FAIL 0 / 985，SKIP 0（5f3：984） | 是 |
| full-wsl（WSL_DISTRO_NAME=Ubuntu） | 0 失败，985 | FAIL 0 / 985，SKIP 0（5f3：984） | 是 |
| sc-cases | PASS 161，其余 0 | PASS 161 FAIL 0 MISSING 0 SETUP 0 SKIP 0 | 是 |
| run-mutants v31 | BI 全 CAUGHT，P-0 GREEN | 57 CAUGHT，P-0 GREEN，扰动轮 0 not as expected | 是 |
| run-mutants suite | 同上（可能需按负载重跑） | 第一轮 54 CAUGHT，BI-13/14/15 与 P-0 NOT-JUDGED；重跑 3 CAUGHT；P-0 单跑 GREEN；扰动轮 0 not as expected | 是 |
| w14 | 26 / 5 / 0 / 0 / 0 | 25 / 5 / **1** / 0 / 0（Q-17，见不符第 3 条；单独重跑两次均 as predicted） | **否** |
| commentsync | 与 5f3 差 2 行；GREEN x 3，RED x 4 | 差 0 行；GREEN x 3，RED x 4（78/60/58/57） | **diff 行数否**，其余是 |
| 变异生成 | 57 + 7；31 | 57 + 7（hook 628652570ce3）；31 | 是 |
| 判据对照 | 13 x 5 全一致 | 13 x 5 全一致 | 是 |

## 5. 其他文件的改动

套件（`hooks/tests/secret-guard.test.sh`）、`v31/sc-cases.sh`、`v31/impl/w14-mutants.py`（`v31/sc-direct.sh` 与 helper 同，略）：

```diff
diff --git a/hooks/tests/secret-guard.test.sh b/hooks/tests/secret-guard.test.sh
index 5f991df..7e3c1ae 100755
--- a/hooks/tests/secret-guard.test.sh
+++ b/hooks/tests/secret-guard.test.sh
@@ -13,7 +13,7 @@
 # Outputs PASS/FAIL per case + summary at end.
 # Exit code: 0 if all pass, 1 if any fail.
 #
-# Coverage: 990 cases (984 without zsh), counted in a git checkout of aria, across Bash (block/allow), Read/Edit (block/allow),
+# Coverage: 991 cases (985 without zsh), counted in a git checkout of aria, across Bash (block/allow), Read/Edit (block/allow),
 # guard:ack escapes, jq fail-closed paths, Round 1 audit bypass attempts, and
 # the Nomad var WRITE direction (#170). Keep this number in sync — a stale
 # count here has already misled one spec into planning against "~50".
@@ -186,7 +186,7 @@ V10-N1-environ-rows-only V10-N2-read-rows-only V10-N3-environ-big-judge V10-N4-r
 V10-N6-filtered-long-line-rows-only V7-N7-big-judge-filtered-long-line V7-N10-blank-padded-long-line V7-N11-lmax-edge-normal V7-N12-lmax-edge-rows-only
 V7-N8-whole-branch-returns-big-judge V7-N9-segment-routes-to-big-judge V7-N13-unmeasured-length-rows-only
 V14-N1-nocredit-never-runs-credit V14-N2-longline-pattern-is-a-rule V14-G1-triggers-return-4-with-the-baseline-reason V14-G2-growth-limit-follows-gmax V14-F1-status-4-falls-back-to-the-baseline-block
-V15-W1a-autofs-mount-point-not-looked-at V15-W1b-binfmt-misc-with-wslinterop-late V15-W1c-binfmt-misc-without-entry V15-W1d-unreadable-mount-table V15-W1f-empty-mount-table V15-W1g-autofs-on-top-of-binfmt-misc-not-looked-at V15-W1h-directory-as-mount-table V15-W1i-noglob-binfmt-misc-with-wslinterop-late V15-W1j-failglob-binfmt-misc-without-entry V15-W1k-unsearchable-directory V15-W1l-unlistable-directory-with-wslinterop-late V15-W1m-mount-table-read-only-after-platform-and-time V15-T1-timer-sleeps-time-left V15-T2-anchor-taken-once-at-hook-start V15-T3-job-errors-silenced V15-W1e-gate-closed-by-wsl-file-system V15-W1n-mount-table-read-in-one-pass"
+V15-W1a-autofs-mount-point-not-looked-at V15-W1b-binfmt-misc-with-wslinterop-late V15-W1c-binfmt-misc-without-entry V15-W1d-unreadable-mount-table V15-W1f-empty-mount-table V15-W1g-autofs-on-top-of-binfmt-misc-not-looked-at V15-W1h-directory-as-mount-table V15-W1i-noglob-binfmt-misc-with-wslinterop-late V15-W1j-failglob-binfmt-misc-without-entry V15-W1k-unsearchable-directory V15-W1l-unlistable-directory-with-wslinterop-late V15-W1m-mount-table-read-only-after-platform-and-time V15-W1o-regular-file-as-directory V15-T1-timer-sleeps-time-left V15-T2-anchor-taken-once-at-hook-start V15-T3-job-errors-silenced V15-W1e-gate-closed-by-wsl-file-system V15-W1n-mount-table-read-in-one-pass"
 SGW_EXP_E2E="V7-E1-benign-big-allowed V6-E2-deadline-fallback-bytes V3-E3-anchor-at-hook-start V3-E4-cap-3-at-budget-4 V3-E5-budget-2 V2-E6-flag-from-environment-ignored
 V2-E7-no-time-left V2-E8-ostype-from-environment-ignored V2-E9-extension-project V9-E10-count-axis-read-blocked V9-E11-tmax-in-rerun V9-E12-vmax-unchanged
 V7-E13-multiline-copy-normal-text V7-E14-long-line-from-expansion V7-E15-credit-as-normal V1-E16-p1-small-benign V1-E16-p1-small-read V1-E16-p1-small-read-filter
diff --git a/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/sc-cases.sh b/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/sc-cases.sh
index eae4c06d..502cfa62 100755
--- a/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/sc-cases.sh
+++ b/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/sc-cases.sh
@@ -232,7 +232,7 @@ V2-G4-extension-path-is-a-directory V2-G5-nested V2-G6-no-time-left V2-G7-no-anc
 V2-G12-segment-trigger-asks-gate V2-G13-whole-trigger-asks-gate V2-G14-cwd-extension-file-with-entry V2-G15-cwd-project-without-extension-file
 V2-G16-environment-root-before-cwd V2-G17-wsl-distro-name-closes-gate V2-G18-wsl-interop-closes-gate
 V11-S5-longline-head-verbatim V11-S6-longline-chinese-line-verbatim V11-S7-longline-text-verbatim
-V15-W1a-autofs-mount-point-not-looked-at V15-W1b-binfmt-misc-with-wslinterop-late V15-W1c-binfmt-misc-without-entry V15-W1d-unreadable-mount-table V15-W1f-empty-mount-table V15-W1g-autofs-on-top-of-binfmt-misc-not-looked-at V15-W1h-directory-as-mount-table V15-W1i-noglob-binfmt-misc-with-wslinterop-late V15-W1j-failglob-binfmt-misc-without-entry V15-W1k-unsearchable-directory V15-W1l-unlistable-directory-with-wslinterop-late V15-W1m-mount-table-read-only-after-platform-and-time"
+V15-W1a-autofs-mount-point-not-looked-at V15-W1b-binfmt-misc-with-wslinterop-late V15-W1c-binfmt-misc-without-entry V15-W1d-unreadable-mount-table V15-W1f-empty-mount-table V15-W1g-autofs-on-top-of-binfmt-misc-not-looked-at V15-W1h-directory-as-mount-table V15-W1i-noglob-binfmt-misc-with-wslinterop-late V15-W1j-failglob-binfmt-misc-without-entry V15-W1k-unsearchable-directory V15-W1l-unlistable-directory-with-wslinterop-late V15-W1m-mount-table-read-only-after-platform-and-time V15-W1o-regular-file-as-directory"
 EXP_DIRECT_RELAX="V3-G9-clock-backwards V3-G10-cap-3 V3-G12-time-left-zero-padded
 V4-S1-allow V4-S2-block-with-text V4-S3-block-without-text V3-S4-slow-judgement V5-S5-pipe-holder V4-S6-spoofed-tail-0 V4-S7-time-checkpoint V4-S8-internal-error
 V5-S9-child-left-behind V5-S13-detached-child V5-S13b-nothing-outlives-the-run V4-S11-bare-zero V5-S10-timer-fork-fails V5-S10b-no-judgement-without-timer
diff --git a/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/impl/w14-mutants.py b/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/impl/w14-mutants.py
index 650ebc7a..9bdc08f1 100644
--- a/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/impl/w14-mutants.py
+++ b/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/impl/w14-mutants.py
@@ -11,7 +11,7 @@ import hashlib
 import os
 import sys
 
-IMPL_SHA12 = "16996eb7db21"
+IMPL_SHA12 = "628652570ce3"
 
 # (id, short title, [(original, replacement), ...])
 MUTANTS = [
```

## 6. 收尾状态

```
$ git -C wt217/aria status --short
 M hooks/secret-guard.sh
 M hooks/tests/lib/secret-guard-w10-direct.sh
 M hooks/tests/secret-guard.test.sh
$ git -C /home/dev/Aria status --short
 M .aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/impl/w14-mutants.py
 M .aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/sc-cases.sh
 M .aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/sc-direct.sh
hook sha256 prefix: 628652570ce3
processes whose command line names t005f4 (want none):
(end of list)
```

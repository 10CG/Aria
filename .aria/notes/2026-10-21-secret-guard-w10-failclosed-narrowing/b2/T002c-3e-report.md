# TASK-002 第三步 3e 报告 (10CG/aria-plugin#217)

执笔席 3e, 2026-10-24。任务书 `r217impl/BRIEF-T002c-3e.md`。产物全在 `r217impl/t002h/`。没有 commit。
改动: worktree `wt217/aria` (df2d629) 的 `hooks/tests/secret-guard.test.sh` (4 个 hunk, +23/-12) 与主仓
`.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/run-suite.sh` (26 -> 35 行)。hook、helper、垫片与其余 v31 脚本没有动
(`git status`: worktree 只有套件一处 M, 主仓 notes 目录下只有 run-suite.sh 一处 M)。

## 0. 结论

| 项 | 预期 (先写, `t002h/expect-0-old.md`、`expect-2-new.md`、`expect-extra.txt`) | 结果 |
|---|---|---|
| 第 0 步 C6 旧判法 (3c2 代码) | 5 组红 (21ag 若 W >= 3.0 s 则过), 回落约 3 / 10 | 与预期相同: 21ab/21ac/21aj/21al/21ao FAIL, 21ag pass; 回落 3 / 10 (21ab 3.01s; 21ab 3.01s; 21ag 3.01s); 走 (b) 的单次读数约为 Tb + 1.5 s (如 21ac W 2.47 s、Tb' 1.76 s) |
| C6 新判法 | 6 组 PASS, 10 / 10, 走 (b) 的带 (try 2) | 与预期相同: 6 组 pass, 10 / 10, 7 条 (b) 都是 `(try 2)`, 3 条 (a) 不带 Tb |
| C1 新判法 (准入门恒关) | 6 组 FAIL; (b) 窗口里的列 3 次读数; 21ab 慢的那条若 W >= 3.0 s 记回落 (固有限度), 约 1 / 10 | 6 组 FAIL; 21ab 两条落在 (b) 窗口, 各列 3 次读数 (W 2.36 s: 2.34, 2.34, 2.31; W 2.43 s: 2.52, 2.43, 2.38), 判不符; 其余 8 条 W < 2.0 s。回落 0 / 10, 与我写的「约 1 / 10」不同: 3c2 里 W 3.35 s 的那条这次 W 2.43 s (负载更低), 落进 (b) 窗口并被判红, 没有出现 W >= 3.0 s 的情形 |
| C5 新判法 (快速失败) | 6 组 FAIL, 0 / 10 | 与预期相同: 6 组 FAIL, 0 / 10; 21ab 两条 (b) 各列 3 次读数 (W 2.85 s: 2.31, 2.34, 2.51; W 2.90 s: 2.47, 2.43, 2.40) |
| 实现整轮 (worktree, PATH 上的 bash) | 961 / 961, FAIL 0, SC-13 绿, 0 / 10 | PASS 961 / 961, FAIL 0 / 961 (失败清单为空, SC-13 不在其中; 套件只列失败项), 回落 0 / 10, 开跑负载 1.08 |
| commentsync `--suite-only` | GREEN | `target --suite-only: GREEN` (`t002h/commentsync-new.txt`) |
| run-suite.sh (i) SC_BASH 父目录也不存在, `SG_W10_ONLY=.` | 首行记原路径, FAIL, 退出 1 | 首行 `SC_BASH <t002h>/no-such-dir/sub/bash`, FAIL 135 / 136, 退出 1 |
| run-suite.sh (ii) SG_W10_LOG 目录不存在 | 退出 3, stderr 说明, 不跑套件 | 退出 3, stderr 一行, 无首尾行, no-such-dir 未被建出 |
| run-suite.sh (iii) V1-E16 过滤轮改前改后 | 日志逐行相同 (读数之外) | 改前 / 改后 (旧套件快照) / 改后 (新套件) 日志都是 10 行; 抹掉 `N.NNs` 与日期后只剩一行不同: `# load start ... end ... \| timing batch: judged` 的负载读数。套件输出去掉首尾行后同样只差这一行负载读数 |
| 改前基线 (额外证据) | 旧脚本吞错 | 旧 run-suite.sh: SC_BASH 父目录不存在 -> 首行 `SC_BASH bash on PATH`, PASS 8 / 8, 退出 0; SG_W10_LOG 目录不存在 -> 退出 0, 没有日志 (两种吞错都复现) |
| 回落分支 (额外, 见 1.3) | cwd 已删时 readlink -m 失败, 原值交给套件 | readlink -m 退出 1、无输出; `SG_W10_LOG=rel.log` -> 退出 3; `SC_BASH=rel-bash` -> 首行 `SC_BASH rel-bash`, FAIL 7 / 8 ([setup] SC_BASH does not run), 退出 1 |

构造与 3c2 / 主控复核逐字相同 (patch 出的 sha 前缀一致): c1 93c7f2fac02a、c3 2a9e3d898705、c5 a4b04f1f97cf (与 `t002f-verify/c5.txt` 首行相同)。
C6 包装层 `t002h/c6-wrap.sh` (7884d94e0c1b): 只对设了 WSL_DISTRO_NAME 的调用, 把 stdin 落成文件、按 sha256 在 `t002h/c6-marks` 下 mkdir 记标记,
同一输入第一次先 `sleep 1.5`, 再用同一个 bash (`$BASH`) exec C3 的 hook (绝对路径); 被 source 时 (直调 helper) 转而 source C3。标记目录每轮新建,
跑完改名留档: C6-old 23 个输入被卡、关门调用 31 次; C6-new 23 个、38 次 (多出的 7 次正是 7 条 (b) 的第 2 次重跑)。

## 1. 改了什么

### 1.1 套件 (全文 diff 见附录 B, wpa_x6 改后全文见附录 A)
- 6 组共用注释 (`:2926-2928`): 「with a gate-closed run of the same input」改为「with one of up to three gate-closed runs of the same input」。
- 注释块: 删掉「(sha256 af4658b6f935)」, F1-F3 里的函数名保留; (b) 的说明改为至多 3 次、间隔 1 s、第一个 0 < Tb' <= W - 1.0 s 的读数记回落并停,
  3 次都不满足记不符并列全部读数; 写明理由 (只量一次时主机一卡就把合法回落判红; 合法的 (b) 只在主机忙时出现, 与 Tb' 的卡顿相关, 附 3c2 那条
  W 2.86 s / Tb' 1.74 s 的读数; 准入门提前关时每次读数都约等于 W, 照样红; 假绿仍须 W 自身被拖长 1 s 以上); Summary 说明加「(try k)」。
- `wpa_x6` 只改 (3b) 支: `for try in 1 2 3`、`(( try > 1 )) && sleep 1`、每次照旧调 `wpa_x6_hook "$input" WSL_DISTRO_NAME=Ubuntu`,
  读数累进 `tbs`; 满足即 `fb="${ws}s/Tb ${wpa_x6_s}s"`, try > 1 时追加 ` (try k)`, break; 都不满足时
  `bad="baseline block at wall ${ws}s, gate-closed Tb' ${tbs} (want <= wall - 1.0 s): 关门那一遍同样慢：是准入门提前关，不是重跑的检查点"` (中文句原样)。
  (1)(2)(3a)(3c)、`wpa_x6_eval`、`wpa_x6_hook`、6 组调用行、基线支、W10 移植块一字未动 (diff 的 4 个 hunk 只落在 `:2924`、`:2951`、`:2962`、`:3000` 起的这几段)。

### 1.2 run-suite.sh (diff 见附录 C)
- `SC_BASH`、`SG_W10_LOG` 改用 `readlink -m --`; `SG_W10_LOG` 规范后若不是绝对路径或所在目录不存在, stderr 说明并 `exit 3` (此时 trap 照常删副本)。
- 头注释写明: readlink -m 不要求存在、值总能交到套件手里由套件报错; readlink -f 在父目录也不存在时输出空串, SC_BASH 被清空后回落到 PATH 上的 bash、
  套件全过退出 0 (fail-open), SG_W10_LOG 被清空则日志静默丢失; 所以目录不存在时以 3 结束。尾注里的退出码说明同步为「3, with neither line, when
  the copy cannot be built or SG_W10_LOG's directory does not exist」。

### 1.3 执笔席自定的取舍 (请主控定夺)
1. 任务书只写「改用 readlink -m, 把原值原样交给套件」。我在两处加了 `|| printf '%s' "$原值"`: readlink -m 失败时把原值原样交下去, 而不是空串;
   SG_W10_LOG 另加 `== /*` 判断, 原值是相对路径时同样退出 3 (套件在副本目录里跑, 相对路径的日志会写进随后被删的副本)。理由是不让新代码在自己的
   兜底路径上重犯「值被清空 -> 回落 PATH 上的 bash」。实测 GNU readlink -m 遇到符号链接环不失败 (退出 0, 按字面给出路径); 能让它失败的是
   当前目录已被删除时的相对路径 (退出 1、无输出), 这一支已实跑 (表中最后一行)。若主控认为超出规格, 删掉这两处即回到任务书字面。
2. `local try tbs=''` 写在 (3b) 支里面, 没有改函数开头那行 `local` (任务书限定只动 (b) 支)。
3. `(try k)` 前加一个空格: `2.82s/Tb 0.64s (try 2)`。
4. C6 的「设了 WSL_DISTRO_NAME」取 `${WSL_DISTRO_NAME+x}` (设了即算, 含空值); 6 组的关门调用都是 `=Ubuntu`, 两种读法对 6 组没有区别。

## 2. v31 其余脚本里的 `readlink -f` (只列, 未改)

`grep -n 'readlink -f'` 共 8 处。先核了存在、不在清单里的: run-suite.sh:14 (:13 先查 `-f`)、run-suite.sh:15 (先 `mkdir -p`, 失败 `exit 3`)、
sc-cases.sh:29 (:28 先查 `-f -r`)、sc-cases.sh:44 (:43 先查 `-f -r`)。符合「可选的环境变量或可能不存在的路径、没有先核存在」的:
1. **run-evidence.sh:8** `W=$(readlink -f "$1")`: 工作目录本来就可能不存在 (:9 才 `mkdir -p "$W"`)。父目录也不存在时 W 为空串, `mkdir -p ""` 失败,
   其后 `"$W/base.sh"`、`"$W/impl.sh"` 变成文件系统根下的 `/base.sh`、`/impl.sh`。普通用户下写入会失败而退出, 有写根目录权限时会写到 `/`。
   形状最危险的一处 (按代码读, 未实跑)。
2. **run-mutants.sh:32** `H=$(readlink -f "$1")`: 被测 hook 路径, 之前没有存在检查; 父目录不存在时 H 为空串, 交给 `mutants.py ""`, 按代码看会在
   `|| { cat ...; exit 3; }` 处失败退出 (未实跑)。
3. **run-mutants.sh:42** `SUITE=$(readlink -f "$MUT_SUITE")`: 可选环境变量, 之前未核存在; 但 :43 紧接着 `[[ -n "$SUITE" && -f ... ]] || exit 3`,
   空串被拦住, 不吞错。
4. **sc-cases.sh:30** `SC_BASH=$(readlink -f "$SC_BASH_IN" 2>/dev/null)`: 可选环境变量 SC_BASH, 之前未核存在; 但 :37
   `[[ -n "$SC_BASH" && -f "$SC_BASH" && -x "$SC_BASH" ]] ... || setup "SC_BASH does not run: $SC_BASH_IN"`, 空串报 setup, 不吞错。

## 3. 首尾负载与等待

开工时 `0.88 1.12 1.07`; 驱动开始 `1.00 1.69 1.42`; 结束 `1.70 1.70 1.59`。每轮开跑前等一分钟负载 <= 1.2, 最长一次等 70 s (C5-new 前), 没有一次
等满 30 分钟。各轮首尾读数: C6-old 1.00 -> 1.93; C6-new 1.13 -> 1.44; C1-new 1.17 -> 2.01; C5-new 1.10 -> 1.83; 实现 1.08 -> 1.70;
过滤轮都在 1.13-1.19。逐条见附录 F (`t002h/drive.log`)。同一时刻只跑一个套件; 驱动记下的 13 个 PID 收尾时都已结束, 没有清理动作。

## 4. 未做或拿不准

1. C6 两轮整轮 FAIL 45 / 40 (3c2 的 C3 为 20): 多出的红来自包装层本身 (移植批关门臂的首次调用被卡 1.5 s; 直调的 SC-21ak
   `_sg_vx_apply entries: want '11', got '0'`, 包装层被 source 时函数定义在另一个文件里), 不在 6 组之内, 按任务书未深究。C6-old 与 C6-new
   之差恰好是那 5 组 (45 - 40 = 5)。
2. SG_W10_LOG 的目录存在但不可写时, run-suite.sh 不拦 (任务书只要求「不存在」); 那时套件怎么报没有查。
3. 回落分支那一轮 (SC_BASH=rel-bash) 有 1 个 V1-E16 用例 PASS, 应是不经 SC_BASH 的那条, 未查证。
4. run-evidence.sh:8、run-mutants.sh:32 的后果是按代码读的, 没有实跑。
5. 1.3 的第 1 条超出任务书字面, 待主控定。

## 5. 工具调用

本段共用 20 次工具调用 (上限 45)。

---

以下附录由脚本从 `t002h/` 里的文件原样追加 (命令行前缀截短、长串打码见 `drive.sh` 的 `x6`)。

## 附录 A: wpa_x6 改后全文

```
wpa_x6() {   # <the relaxed assertion: longline | pass (exit 0) | growth (wpa_L_gseg)> <the baseline branch's limit line for this command> <command>
  local how=$1 lim=$2 c=$3 input e wus ws r b fb='' bad='' g='?' p="${3//$wpa_nl/ }" wpa_x6_out wpa_x6_us wpa_x6_s
  input="$(wpa_in Bash "$c")"   # built before the clock starts: W is the hook's run alone
  wpa_x6_hook "$input"; e=$wpa_x6_out; wus=$wpa_x6_us; ws=$wpa_x6_s
  wpa_x6_n=$((wpa_x6_n + 1))
  r=$(wpa_x6_eval "$e" "$how" "$lim" "$c"); [[ ${r%%$'\t'*} == 0 ]] && return 0   # (1) the relaxed branch's assertion holds
  b=$(wpa_x6_eval "$e" toolarge "$lim" "$c")
  if [[ ${b%%$'\t'*} != 0 ]]; then   # (2) nor does the baseline branch's
    bad="relaxed ($how):${r#*$'\t'} | baseline branch:${b#*$'\t'} | wall ${ws}s"
  elif (( wus >= 3000000 )); then   # (3a) F1, F2 or a late F3
    fb="${ws}s"
  elif (( wus > 2000000 )); then   # (3b) F3 or a gate closed early: the same input with the gate closed, up to three runs 1 s apart (a reading of 0 is no reading)
    local try tbs=''
    for try in 1 2 3; do
      (( try > 1 )) && sleep 1
      wpa_x6_hook "$input" WSL_DISTRO_NAME=Ubuntu
      tbs+="${tbs:+, }${wpa_x6_s}s"
      if (( wpa_x6_us > 0 && wpa_x6_us <= wus - 1000000 )); then fb="${ws}s/Tb ${wpa_x6_s}s"; (( try > 1 )) && fb+=" (try $try)"; break; fi
    done
    [[ -n $fb ]] || bad="baseline block at wall ${ws}s, gate-closed Tb' ${tbs} (want <= wall - 1.0 s): 关门那一遍同样慢：是准入门提前关，不是重跑的检查点"
  else   # (3c) W <= 2.0 s
    bad="baseline block at wall ${ws}s (want > 2.0 s): 因时间的回落不会这么早结束"
  fi
  if [[ -n $fb ]]; then
    [[ $_wpa_name =~ SC-(21a[a-z]) ]] && g=${BASH_REMATCH[1]}
    wpa_x6_fb=$((wpa_x6_fb + 1)); wpa_x6_where+="$g $fb; "; return 0
  fi
  _wpa_nbad=$((_wpa_nbad + 1))
  [[ $_wpa_nbad -le 6 ]] && _wpa_bad="$_wpa_bad {Bash ${p:0:72}: $bad}"
  return 0
}
```

## 附录 B: 套件 diff (git diff, worktree)

```diff
diff --git a/hooks/tests/secret-guard.test.sh b/hooks/tests/secret-guard.test.sh
index 59a5238..c143a95 100755
--- a/hooks/tests/secret-guard.test.sh
+++ b/hooks/tests/secret-guard.test.sh
@@ -2924,8 +2924,8 @@ wpa_x_toolarge() {   # <command> <the limit line it must name: wpa_L_*>: refused
 # wpa_rx6=yes: the relaxation is expected and a group asserts the outcome the proposal gives (its comment names the What / P item); wpa_rx6=no: the group keeps its
 # baseline assertions word for word. Either way a group is one case, so the count does not depend on the platform (SC-13). The summary prints the branch and its inputs.
 # In the relaxed branch a trigger-point command (a copy over 8192) goes through wpa_x6, which also accepts the deadline fallback (the baseline branch's
-# assertion on the same output, with a wall only a fallback for time gives: >= 3.0 s, or over 2.0 s with a gate-closed run of the same input at least
-# 1.0 s quicker; see wpa_x6), and the summary counts those fallbacks.
+# assertion on the same output, with a wall only a fallback for time gives: >= 3.0 s, or over 2.0 s with one of up to three gate-closed runs of the
+# same input at least 1.0 s quicker; see wpa_x6), and the summary counts those fallbacks.
 wpa_rx6=no; wpa_rx6_mach=''; wpa_rx6_maj=''; wpa_rx6_min=''; wpa_rx6_ver=''; wpa_rx6_osr=$(cat /proc/sys/kernel/osrelease 2>/dev/null); wpa_rx6_wslf=no
 [[ -e /proc/sys/fs/binfmt_misc/WSLInterop ]] && wpa_rx6_wslf=yes
 read -r wpa_rx6_mach wpa_rx6_maj wpa_rx6_min wpa_rx6_ver < <(env bash -c 'echo "${BASH_VERSINFO[5]} ${BASH_VERSINFO[0]} ${BASH_VERSINFO[1]} $BASH_VERSION"' 2>/dev/null)
@@ -2951,7 +2951,7 @@ wpa_x_hit() {   # <command>: (relaxed branch) judged and blocked with the ordina
 # runs the hook ONCE (wpa_x6_hook; SECRET_GUARD_TIME_BUDGET_S cleared, so the deadline is _SG_P0 + 3 s). Its wall W is taken by EPOCHREALTIME and
 # compared in whole microseconds, never rounded first (shown cut to two decimals). Why the hook falls back: the baseline pass runs first and on a busy
 # host takes much of the 3 s (21ab: 2.37-2.58 s for the whole hook at load 1.2-1.6, 2.39-3.08 s gate-closed, b2/t002d-verify/probe.txt), and then the
-# hook gives the baseline's block (What 4; P3, P6). Worked out from the hook (sha256 af4658b6f935), a fallback for time has three ways and no other:
+# hook gives the baseline's block (What 4; P3, P6). Worked out from the hook, a fallback for time has three ways and no other:
 #   F1 the gate closes for lack of time: _sg_relax_left gives status 1 only once now >= _SG_P0 + 3 s;
 #   F2 the deadline kills the job: its timer (sleep "$_SG_LEFT") starts after _SG_LEFT is worked out, so the kill comes after _SG_P0 + 3 s;
 #   F3 the rerun's own time checkpoint: _sg_vx_collect resets _SG_T0=$SECONDS and _sg_over_budget sends the rerun back (status 3, then the baseline
@@ -2962,16 +2962,22 @@ wpa_x_hit() {   # <command>: (relaxed branch) judged and blocked with the ordina
 # (1) the relaxed branch's assertion holds on that output: passes. (2) Otherwise, when the baseline branch's assertion for that command (the else
 # branch's wpa_x_toolarge and its limit line) does not hold on the SAME output either: the check is off, its detail naming both assertions' misses and
 # W. (3) Otherwise (the output is the baseline's block): (a) W >= 3.0 s: a deadline fallback (F1, F2 or a late F3). (b) 2.0 s < W < 3.0 s: the same
-# input runs once more -- the same variables and directory, the budget variable cleared, plus WSL_DISTRO_NAME=Ubuntu, which closes the gate -- and its
-# wall is Tb'; Tb' <= W - 1.0 s is a deadline fallback (F3: the checkpoint sent the rerun back, W more than 2 s over the baseline pass); otherwise the
-# check is off with W and Tb' (the gate-closed run is as slow: the gate closed early, not the rerun's checkpoint). 1 s sits in the middle of F3's 2 s
-# gap and leaves 1 s on each side for load jitter. (c) W <= 2.0 s: the check is off with W (a fallback for time does not end this early).
+# input runs again up to three times, 1 s apart -- each run the same variables and directory, the budget variable cleared, plus WSL_DISTRO_NAME=Ubuntu,
+# which closes the gate -- and each run's wall is a reading Tb'. The first reading with 0 < Tb' <= W - 1.0 s is a deadline fallback (F3: the
+# checkpoint sent the rerun back, W more than 2 s over the baseline pass) and ends the runs; when none of the three is, the check is off with W and all
+# three readings (the gate-closed runs are as slow: the gate closed early, not the rerun's checkpoint). 1 s sits in the middle of F3's 2 s gap and
+# leaves 1 s on each side for load jitter. Why up to three runs (the 3c2 ruling): with one reading, a host that stalls that one run turns a lawful
+# fallback red, and a lawful (b) shows up only when the host held the rerun past 2 s -- the host is busy just then, so the gate-closed run that follows
+# is likely held up too (3c2: W 2.86 s with Tb' 1.74 s, for a command that takes about 0.66 s). A gate that closes early reads about W every time and
+# stays red; a false green still needs W itself drawn out by more than 1 s (the retries only make Tb' less exposed to stalls).
+# (c) W <= 2.0 s: the check is off with W (a fallback for time does not end this early).
 # This replaces the 3b rule's lower bound of 2.85 s, which was copied from the deadline cases instead of worked out from the hook and had a hole on
 # each side: from 2.0 to 2.85 s it turned a lawful F3 red, and from 2.85 to 3.0 s it could not tell F3 from a gate that closed early. Left as it is
 # (the 3c ruling): a command whose baseline pass alone runs past 3 s gives the same output as a lawful "no time to close the gate" and cannot be told
 # apart; each group has a command with a quick baseline pass, and the ported cases cover the rest. No load gate: the six groups run late in the suite,
 # where 3b's seven full rounds ended at load 2.21-4.13, so a gate would SKIP them nearly every round. A group still counts once; the summary line of the
-# six groups gives the fallbacks over the trigger-point commands judged, each with its group and W (and Tb' for (b)).
+# six groups gives the fallbacks over the trigger-point commands judged, each with its group and W (and for (b) the Tb' that met the bound, followed by
+# "(try k)" when that was the k-th run, k > 1).
 wpa_x6_n=0; wpa_x6_fb=0; wpa_x6_where=''
 wpa_x6_eval() {   # <output as wpa_err gives it> <longline | pass | growth | toolarge> <limit line> <command> -> "<checks off>" TAB "<their list>": the assertion
                   # helper itself, in a subshell where wpa_err / wpa_rc hand back that output, so both branches judge ONE run of the hook
@@ -3000,10 +3006,15 @@ wpa_x6() {   # <the relaxed assertion: longline | pass (exit 0) | growth (wpa_L_
     bad="relaxed ($how):${r#*$'\t'} | baseline branch:${b#*$'\t'} | wall ${ws}s"
   elif (( wus >= 3000000 )); then   # (3a) F1, F2 or a late F3
     fb="${ws}s"
-  elif (( wus > 2000000 )); then   # (3b) F3 or a gate closed early: the same input once more with the gate closed (a reading of 0 is no reading)
-    wpa_x6_hook "$input" WSL_DISTRO_NAME=Ubuntu
-    if (( wpa_x6_us > 0 && wpa_x6_us <= wus - 1000000 )); then fb="${ws}s/Tb ${wpa_x6_s}s"
-    else bad="baseline block at wall ${ws}s, gate-closed Tb' ${wpa_x6_s}s (want <= wall - 1.0 s): 关门那一遍同样慢：是准入门提前关，不是重跑的检查点"; fi
+  elif (( wus > 2000000 )); then   # (3b) F3 or a gate closed early: the same input with the gate closed, up to three runs 1 s apart (a reading of 0 is no reading)
+    local try tbs=''
+    for try in 1 2 3; do
+      (( try > 1 )) && sleep 1
+      wpa_x6_hook "$input" WSL_DISTRO_NAME=Ubuntu
+      tbs+="${tbs:+, }${wpa_x6_s}s"
+      if (( wpa_x6_us > 0 && wpa_x6_us <= wus - 1000000 )); then fb="${ws}s/Tb ${wpa_x6_s}s"; (( try > 1 )) && fb+=" (try $try)"; break; fi
+    done
+    [[ -n $fb ]] || bad="baseline block at wall ${ws}s, gate-closed Tb' ${tbs} (want <= wall - 1.0 s): 关门那一遍同样慢：是准入门提前关，不是重跑的检查点"
   else   # (3c) W <= 2.0 s
     bad="baseline block at wall ${ws}s (want > 2.0 s): 因时间的回落不会这么早结束"
   fi
```

## 附录 C: run-suite.sh diff (改前副本 -> 改后)

```diff
--- /tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/t002h/run-suite-before.sh	2026-10-24 13:26:12.645529297 +0000
+++ /home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/run-suite.sh	2026-10-24 16:50:59.232964345 +0000
@@ -3,20 +3,29 @@
 # ported by TASK-002 of 10CG/aria-plugin#217) on <hook>. <aria>/hooks is copied to a temporary directory (under <work dir> when given, removed at the end),
 # its secret-guard.sh is replaced by <hook>, and the copy's suite runs there under taskset -c 0,1 nice -n 19. SC_BASH (the bash that runs the hook in the
 # ported cases), SG_W10_ONLY (run only the ported cases whose id matches) and SG_W10_LOG (one result line per ported case, v31 format) are passed through;
-# relative paths in them are made absolute first.
+# relative paths in SC_BASH and SG_W10_LOG are made absolute first, by readlink -m, which does not need the path to exist (3e; plan notes, the 3d
+# ruling (1)): the value given always reaches the suite, so a SC_BASH that does not exist is the suite's FAIL to report, and when readlink -m gives
+# nothing the value goes on unchanged. readlink -f, used before, printed nothing once the parent directory was missing too: SC_BASH went empty, the suite
+# fell back to the bash on PATH and passed with status 0 (an environment error swallowed, fail-open), and SG_W10_LOG went empty, the log lost without
+# a word. So when SG_W10_LOG's directory does not exist (or the path cannot be made absolute) this script stops with status 3 and says so on stderr:
+# a log asked for must not be lost silently.
 # The copy is not a git checkout: the cases that read an old hook through git show (SC-8, SC-9a) do not run in it, so the total that SC-13 counts differs
 # from the header's Coverage numbers and SC-13 is red in the copy. Read SC-13 only from a run in a git checkout; a filtered round (SG_W10_ONLY) has no SC-13.
 # Output: the suite's stdout and stderr. The first line records the date, the sha256 prefixes of <hook>, of the suite and of its direct-call helper
 # (hooks/tests/lib/secret-guard-w10-direct.sh; "missing" when the copy has none), and the one-minute loads; the
-# last line the loads at the end and the suite's exit status, which is also this script's (3 when the copy cannot be built).
+# last line the loads at the end and the suite's exit status, which is also this script's (3, with neither line, when the copy cannot be built or
+# SG_W10_LOG's directory does not exist).
 set -u
 [[ $# -ge 2 && -f "$1/hooks/tests/secret-guard.test.sh" && -f "$2" && -r "$2" ]] || { echo "usage: run-suite.sh <aria checkout> <hook> [<work dir>]" >&2; exit 3; }
 A=$(readlink -f "$1"); HK=$(readlink -f "$2")
 if [[ -n "${3:-}" ]]; then mkdir -p "$3" && T=$(mktemp -d "$(readlink -f "$3")/suite.XXXXXX"); else T=$(mktemp -d); fi || exit 3
 trap 'rm -rf "$T"' EXIT
 cp -a "$A/hooks" "$T/hooks" && cp "$HK" "$T/hooks/secret-guard.sh" && chmod 755 "$T/hooks/secret-guard.sh" || { echo "run-suite.sh: cannot build the copy in $T" >&2; exit 3; }
-[[ -n "${SC_BASH:-}" ]] && export SC_BASH="$(readlink -f "$SC_BASH")"
-[[ -n "${SG_W10_LOG:-}" ]] && export SG_W10_LOG="$(readlink -f "$SG_W10_LOG")"
+[[ -n "${SC_BASH:-}" ]] && export SC_BASH="$(readlink -m -- "$SC_BASH" || printf '%s' "$SC_BASH")"
+if [[ -n "${SG_W10_LOG:-}" ]]; then
+  export SG_W10_LOG="$(readlink -m -- "$SG_W10_LOG" || printf '%s' "$SG_W10_LOG")"
+  [[ $SG_W10_LOG == /* && -d "$(dirname -- "$SG_W10_LOG")" ]] || { echo "run-suite.sh: SG_W10_LOG $SG_W10_LOG: its directory does not exist (or the path cannot be made absolute); the log asked for cannot be written" >&2; exit 3; }
+fi
 [[ -n "${SG_W10_ONLY:-}" ]] && export SG_W10_ONLY
 HL="$T/hooks/tests/lib/secret-guard-w10-direct.sh"
 printf '# run-suite.sh | %s | hook %s | suite %s | helper %s | SC_BASH %s | SG_W10_ONLY %s | load %s\n' "$(date -u +%FT%TZ)" "$(sha256sum < "$HK" | cut -c1-12)" \
```

## 附录 D: 每轮 6 组那一行原文 (grep W10 older groups)

```
[c6-old]
W10 older groups 21ab 21ac 21ag 21aj 21al 21ao: relaxed branch (new outcomes) | bash on PATH /usr/bin/bash 5.2.15(1)-release (machtype x86_64-pc-linux-gnu) | osrelease 6.17.9-1-pve | WSLInterop no | WSL_DISTRO_NAME '' WSL_INTEROP '' | deadline fallback (截止回落) 3 / 10 (21ab 3.01s; 21ab 3.01s; 21ag 3.01s)
[c6-new]
W10 older groups 21ab 21ac 21ag 21aj 21al 21ao: relaxed branch (new outcomes) | bash on PATH /usr/bin/bash 5.2.15(1)-release (machtype x86_64-pc-linux-gnu) | osrelease 6.17.9-1-pve | WSLInterop no | WSL_DISTRO_NAME '' WSL_INTEROP '' | deadline fallback (截止回落) 10 / 10 (21ab 2.82s/Tb 0.64s (try 2); 21ab 3.01s; 21ab 3.01s; 21ac 2.49s/Tb 0.26s (try 2); 21ag 3.01s; 21aj 2.81s/Tb 0.64s (try 2); 21aj 2.87s/Tb 0.72s (try 2); 21aj 2.89s/Tb 1.14s (try 2); 21al 2.48s/Tb 0.30s (try 2); 21ao 2.73s/Tb 0.33s (try 2))
[c1-new]
W10 older groups 21ab 21ac 21ag 21aj 21al 21ao: relaxed branch (new outcomes) | bash on PATH /usr/bin/bash 5.2.15(1)-release (machtype x86_64-pc-linux-gnu) | osrelease 6.17.9-1-pve | WSLInterop no | WSL_DISTRO_NAME '' WSL_INTEROP '' | deadline fallback (截止回落) 0 / 10
[c5-new]
W10 older groups 21ab 21ac 21ag 21aj 21al 21ao: relaxed branch (new outcomes) | bash on PATH /usr/bin/bash 5.2.15(1)-release (machtype x86_64-pc-linux-gnu) | osrelease 6.17.9-1-pve | WSLInterop no | WSL_DISTRO_NAME '' WSL_INTEROP '' | deadline fallback (截止回落) 0 / 10
[impl]
W10 older groups 21ab 21ac 21ag 21aj 21al 21ao: relaxed branch (new outcomes) | bash on PATH /usr/bin/bash 5.2.15(1)-release (machtype x86_64-pc-linux-gnu) | osrelease 6.17.9-1-pve | WSLInterop no | WSL_DISTRO_NAME '' WSL_INTEROP '' | deadline fallback (截止回落) 0 / 10
```

## 附录 E: 每轮摘要 (x6: 首行、总数、6 组行、逐组判定、6 组的 FAIL 行、尾行)

```
[c6-old]
# run-suite.sh | 2026-10-24T16:48:49Z | hook 7884d94e0c1b | suite 60f7f95525cd | helper 213d01379695 | SC_BASH bash on PATH | SG_W10_ONLY <none> | load 1.00 1.69 1.42
PASS: 905 / 950
FAIL: 45 / 950
W10 older groups 21ab 21ac 21ag 21aj 21al 21ao: relaxed branch (new outcomes) | bash on PATH /usr/bin/bash 5.2.15(1)-release (machtype x86_64-pc-linux-gnu) | osrelease 6.17.9-1-pve | WSLInterop no | WSL_DISTRO_NAME '' WSL_INTEROP '' | deadline fallback (截止回落) 3 / 10 (21ab 3.01s; 21ab 3.01s; 21ag 3.01s)
21ab FAIL  21ac FAIL  21ag pass  21aj FAIL  21al FAIL  21ao FAIL  
  FAIL [W10 SC-21ab bf: copy limit exceeded — 8193 characters, or a 9000-character segment with a one-character value: refused as too large where the relaxation is not in effect; where it is, each copy is judged in full: the reader is blocked with the longline text, the two commands with no reader pass]: 1 check(s) off: {Bash f=/etc/for…: baseline block at wall 2.92s, gate-closed Tb' 2.16s (want <= wall - 1.0 s): 关门那一遍同样慢：是准入门提前关，不是重跑的检查点}
  FAIL [W10 SC-21ac bf: value limit, last accepted — a collected value of exactly 4096 characters is expanded and its read blocked]: 1 check(s) off: {Bash for f in /…: baseline block at wall 2.47s, gate-closed Tb' 1.76s (want <= wall - 1.0 s): 关门那一遍同样慢：是准入门提前关，不是重跑的检查点}
  FAIL [W10 SC-21aj bf: a segment over the copy limit that also grows over the growth limit ends the pass — with one, seven or eight of them in front of the reader the command is refused as too large (the copy limit, or the growth limit where the relaxation is in effect) and the reader is never judged]: 3 check(s) off: {Bash f=/etc/for…: baseline block at wall 2.90s, gate-closed Tb' 2.11s (want <= wall - 1.0 s): 关门那一遍同样慢：是准入门提前关，不是重跑的检查点} {Bash f=/etc/for…: baseline block at wall 2.89s, gate-closed Tb' 2.19s (want <= wall - 1.0 s): 关门那一遍同样慢：是准入门提前关，不是重跑的检查点} {Bash f=/etc/for…: baseline block at wall 2.89s, gate-closed Tb' 2.22s (want <= wall - 1.0 s): 关门那一遍同样慢：是准入门提前关，不是重跑的检查点}
  FAIL [W10 SC-21ak rg: the pass-wide limit bounds the work too — after it is used up the pass stops applying (11 entries of _sg_vx_apply, not 14)]: 1 check(s) off: {_sg_vx_apply entries: want '11', got '0'}
  FAIL [W10 SC-21al bf: the braced form meets the same copy limit — a substituted whole command of exactly 8192 characters is judged and blocked; 8193 is refused as too large where the relaxation is not in effect and blocked with the longline text where it is]: 1 check(s) off: {Bash f=/etc/for…: baseline block at wall 2.36s, gate-closed Tb' 1.70s (want <= wall - 1.0 s): 关门那一遍同样慢：是准入门提前关，不是重跑的检查点}
  FAIL [W10 SC-21ao bf: whole-command mode meets the same copy limit — a whole copy of exactly 8192 characters is judged and blocked; 8193 is refused as too large where the relaxation is not in effect and blocked with the longline text where it is]: 1 check(s) off: {Bash f=/etc/for…: baseline block at wall 2.46s, gate-closed Tb' 1.76s (want <= wall - 1.0 s): 关门那一遍同样慢：是准入门提前关，不是重跑的检查点}
# run-suite.sh end | load 1.93 1.79 1.54 | suite exit 1

[c6-new]
# run-suite.sh | 2026-10-24T16:55:48Z | hook 7884d94e0c1b | suite d4168aace3e8 | helper 213d01379695 | SC_BASH bash on PATH | SG_W10_ONLY <none> | load 1.13 1.58 1.48
PASS: 910 / 950
FAIL: 40 / 950
W10 older groups 21ab 21ac 21ag 21aj 21al 21ao: relaxed branch (new outcomes) | bash on PATH /usr/bin/bash 5.2.15(1)-release (machtype x86_64-pc-linux-gnu) | osrelease 6.17.9-1-pve | WSLInterop no | WSL_DISTRO_NAME '' WSL_INTEROP '' | deadline fallback (截止回落) 10 / 10 (21ab 2.82s/Tb 0.64s (try 2); 21ab 3.01s; 21ab 3.01s; 21ac 2.49s/Tb 0.26s (try 2); 21ag 3.01s; 21aj 2.81s/Tb 0.64s (try 2); 21aj 2.87s/Tb 0.72s (try 2); 21aj 2.89s/Tb 1.14s (try 2); 21al 2.48s/Tb 0.30s (try 2); 21ao 2.73s/Tb 0.33s (try 2))
21ab pass  21ac pass  21ag pass  21aj pass  21al pass  21ao pass  
  FAIL [W10 SC-21ak rg: the pass-wide limit bounds the work too — after it is used up the pass stops applying (11 entries of _sg_vx_apply, not 14)]: 1 check(s) off: {_sg_vx_apply entries: want '11', got '0'}
# run-suite.sh end | load 1.44 1.57 1.50 | suite exit 1

[c1-new]
# run-suite.sh | 2026-10-24T17:02:05Z | hook 93c7f2fac02a | suite d4168aace3e8 | helper 213d01379695 | SC_BASH bash on PATH | SG_W10_ONLY <none> | load 1.17 1.50 1.48
PASS: 925 / 950
FAIL: 25 / 950
W10 older groups 21ab 21ac 21ag 21aj 21al 21ao: relaxed branch (new outcomes) | bash on PATH /usr/bin/bash 5.2.15(1)-release (machtype x86_64-pc-linux-gnu) | osrelease 6.17.9-1-pve | WSLInterop no | WSL_DISTRO_NAME '' WSL_INTEROP '' | deadline fallback (截止回落) 0 / 10
21ab FAIL  21ac FAIL  21ag FAIL  21aj FAIL  21al FAIL  21ao FAIL  
  FAIL [W10 SC-21ab bf: copy limit exceeded — 8193 characters, or a 9000-character segment with a one-character value: refused as too large where the relaxation is not in effect; where it is, each copy is judged in full: the reader is blocked with the longline text, the two commands with no reader pass]: 3 check(s) off: {Bash f=/etc/for…: baseline block at wall 0.64s (want > 2.0 s): 因时间的回落不会这么早结束} {Bash f=x; echo …: baseline block at wall 2.36s, gate-closed Tb' 2.34s, 2.34s, 2.31s (want <= wall - 1.0 s): 关门那一遍同样慢：是准入门提前关，不是重跑的检查点} {Bash f=x; echo …: baseline block at wall 2.43s, gate-closed Tb' 2.52s, 2.43s, 2.38s (want <= wall - 1.0 s): 关门那一遍同样慢：是准入门提前关，不是重跑的检查点}
  FAIL [W10 SC-21ac bf: value limit, last accepted — a collected value of exactly 4096 characters is expanded and its read blocked]: 1 check(s) off: {Bash for f in /…: baseline block at wall 0.28s (want > 2.0 s): 因时间的回落不会这么早结束}
  FAIL [W10 SC-21ag bf: the dense shape of the review (15 assignments of 300 B, 8 references each: a 36 KB copy; 16 x 300 B x 8 took 5.4 s) is refused as too large on every platform — by the copy limit where the relaxation is not in effect, by the growth limit where it is]: 1 check(s) off: {Bash v0=aaaaaaa…: baseline block at wall 1.56s (want > 2.0 s): 因时间的回落不会这么早结束}
  FAIL [W10 SC-21aj bf: a segment over the copy limit that also grows over the growth limit ends the pass — with one, seven or eight of them in front of the reader the command is refused as too large (the copy limit, or the growth limit where the relaxation is in effect) and the reader is never judged]: 3 check(s) off: {Bash f=/etc/for…: baseline block at wall 0.61s (want > 2.0 s): 因时间的回落不会这么早结束} {Bash f=/etc/for…: baseline block at wall 0.74s (want > 2.0 s): 因时间的回落不会这么早结束} {Bash f=/etc/for…: baseline block at wall 0.71s (want > 2.0 s): 因时间的回落不会这么早结束}
  FAIL [W10 SC-21al bf: the braced form meets the same copy limit — a substituted whole command of exactly 8192 characters is judged and blocked; 8193 is refused as too large where the relaxation is not in effect and blocked with the longline text where it is]: 1 check(s) off: {Bash f=/etc/for…: baseline block at wall 0.16s (want > 2.0 s): 因时间的回落不会这么早结束}
  FAIL [W10 SC-21ao bf: whole-command mode meets the same copy limit — a whole copy of exactly 8192 characters is judged and blocked; 8193 is refused as too large where the relaxation is not in effect and blocked with the longline text where it is]: 1 check(s) off: {Bash f=/etc/for…: baseline block at wall 0.26s (want > 2.0 s): 因时间的回落不会这么早结束}
# run-suite.sh end | load 2.01 1.72 1.57 | suite exit 1

[c5-new]
# run-suite.sh | 2026-10-24T17:07:43Z | hook a4b04f1f97cf | suite d4168aace3e8 | helper 213d01379695 | SC_BASH bash on PATH | SG_W10_ONLY <none> | load 1.10 1.51 1.50
PASS: 919 / 950
FAIL: 31 / 950
W10 older groups 21ab 21ac 21ag 21aj 21al 21ao: relaxed branch (new outcomes) | bash on PATH /usr/bin/bash 5.2.15(1)-release (machtype x86_64-pc-linux-gnu) | osrelease 6.17.9-1-pve | WSLInterop no | WSL_DISTRO_NAME '' WSL_INTEROP '' | deadline fallback (截止回落) 0 / 10
21ab FAIL  21ac FAIL  21ag FAIL  21aj FAIL  21al FAIL  21ao FAIL  
  FAIL [W10 SC-21ab bf: copy limit exceeded — 8193 characters, or a 9000-character segment with a one-character value: refused as too large where the relaxation is not in effect; where it is, each copy is judged in full: the reader is blocked with the longline text, the two commands with no reader pass]: 3 check(s) off: {Bash f=/etc/for…: baseline block at wall 1.14s (want > 2.0 s): 因时间的回落不会这么早结束} {Bash f=x; echo …: baseline block at wall 2.85s, gate-closed Tb' 2.31s, 2.34s, 2.51s (want <= wall - 1.0 s): 关门那一遍同样慢：是准入门提前关，不是重跑的检查点} {Bash f=x; echo …: baseline block at wall 2.90s, gate-closed Tb' 2.47s, 2.43s, 2.40s (want <= wall - 1.0 s): 关门那一遍同样慢：是准入门提前关，不是重跑的检查点}
  FAIL [W10 SC-21ac bf: value limit, last accepted — a collected value of exactly 4096 characters is expanded and its read blocked]: 1 check(s) off: {Bash for f in /…: baseline block at wall 0.76s (want > 2.0 s): 因时间的回落不会这么早结束}
  FAIL [W10 SC-21ag bf: the dense shape of the review (15 assignments of 300 B, 8 references each: a 36 KB copy; 16 x 300 B x 8 took 5.4 s) is refused as too large on every platform — by the copy limit where the relaxation is not in effect, by the growth limit where it is]: 1 check(s) off: {Bash v0=aaaaaaa…: baseline block at wall 1.59s (want > 2.0 s): 因时间的回落不会这么早结束}
  FAIL [W10 SC-21aj bf: a segment over the copy limit that also grows over the growth limit ends the pass — with one, seven or eight of them in front of the reader the command is refused as too large (the copy limit, or the growth limit where the relaxation is in effect) and the reader is never judged]: 3 check(s) off: {Bash f=/etc/for…: baseline block at wall 1.19s (want > 2.0 s): 因时间的回落不会这么早结束} {Bash f=/etc/for…: baseline block at wall 1.41s (want > 2.0 s): 因时间的回落不会这么早结束} {Bash f=/etc/for…: baseline block at wall 1.48s (want > 2.0 s): 因时间的回落不会这么早结束}
  FAIL [W10 SC-21al bf: the braced form meets the same copy limit — a substituted whole command of exactly 8192 characters is judged and blocked; 8193 is refused as too large where the relaxation is not in effect and blocked with the longline text where it is]: 1 check(s) off: {Bash f=/etc/for…: baseline block at wall 0.67s (want > 2.0 s): 因时间的回落不会这么早结束}
  FAIL [W10 SC-21ao bf: whole-command mode meets the same copy limit — a whole copy of exactly 8192 characters is judged and blocked; 8193 is refused as too large where the relaxation is not in effect and blocked with the longline text where it is]: 1 check(s) off: {Bash f=/etc/for…: baseline block at wall 0.78s (want > 2.0 s): 因时间的回落不会这么早结束}
# run-suite.sh end | load 1.83 1.71 1.58 | suite exit 1

[impl]
  [SKIP] zsh not installed — zsh end-to-end cases skipped (static assertions cover portability)
PASS: 961 / 961
FAIL: 0 / 961
W10 older groups 21ab 21ac 21ag 21aj 21al 21ao: relaxed branch (new outcomes) | bash on PATH /usr/bin/bash 5.2.15(1)-release (machtype x86_64-pc-linux-gnu) | osrelease 6.17.9-1-pve | WSLInterop no | WSL_DISTRO_NAME '' WSL_INTEROP '' | deadline fallback (截止回落) 0 / 10
21ab pass  21ac pass  21ag pass  21aj pass  21al pass  21ao pass  
W10 older groups 21ab 21ac 21ag 21aj 21al 21ao: relaxed branch (new outcomes) | bash on PATH /usr/bin/bash 5.2.15(1)-release (machtype x86_64-pc-linux-gnu) | osrelease 6.17.9-1-pve | WSLInterop no | WSL_DISTRO_NAME '' WSL_INTEROP '' | deadline fallback (截止回落) 0 / 10

```

## 附录 F: drive.log

```
16:48:49 begin | worktree df2d629 status [] | load 1.00 1.69 1.42
16:48:49 snapshot: old suite 60f7f95525cd | run-suite-before 7584c219c4ba | impl hook af4658b6f935 | load 1.00 1.69 1.42
16:48:49 c1 hook 93c7f2fac02a | load 1.00 1.69 1.42
16:48:49 c3 hook 2a9e3d898705 | load 1.00 1.69 1.42
16:48:49 c5 hook a4b04f1f97cf | load 1.00 1.69 1.42
16:48:49 c5 reference (t002f-verify/c5.txt): hook a4b04f1f97cf | load 1.00 1.69 1.42
16:48:49 c6 wrapper 7884d94e0c1b | load 1.00 1.69 1.42
16:48:49 PHASE0 begin | load 1.00 1.69 1.42
16:48:49 waitlow ok at 1.00 after 0s | load 1.00 1.69 1.42
16:48:49 c6-old start | load 1.00 1.69 1.42
16:54:34   -> c6-old.txt rc=1 | load 1.93 1.79 1.54
16:54:34 c6-old end | # run-suite.sh end | load 1.93 1.79 1.54 | suite exit 1 | load 1.93 1.79 1.54
16:54:34   c6-old marks: 23 inputs stalled, 31 gate-closed calls | load 1.93 1.79 1.54
16:55:24 waitlow ok at 1.19 after 50s | load 1.19 1.62 1.50
16:55:24 filt-before start | load 1.19 1.62 1.50
16:55:27   -> filt-before.txt rc=0 | load 1.19 1.62 1.50
16:55:27 waitlow ok at 1.19 after 0s | load 1.19 1.62 1.50
16:55:27 scbash-before start | load 1.19 1.62 1.50
16:55:29   -> scbash-before.txt rc=0 | load 1.25 1.63 1.50
16:55:39 waitlow ok at 1.14 after 10s | load 1.14 1.59 1.49
16:55:39 log-before start | load 1.14 1.59 1.49
16:55:42   -> log-before.txt rc=0 | load 1.14 1.59 1.49
16:55:42   log-before: /tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/t002h/no-such-dir exists? no | load 1.14 1.59 1.49
16:55:42 PHASE0 DONE | load 1.14 1.59 1.49
16:55:42 PHASE2 begin | worktree status [ M hooks/tests/secret-guard.test.sh ] | suite d4168aace3e8 | run-suite 46052595bf14 | load 1.14 1.59 1.49
16:55:42 log-after start | load 1.14 1.59 1.49
16:55:42   -> log-after.txt rc=3 | load 1.14 1.59 1.49
16:55:42   log-after: /tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/t002h/no-such-dir exists? no | load 1.14 1.59 1.49
16:55:42 waitlow ok at 1.14 after 0s | load 1.14 1.59 1.49
16:55:42 filt-after-old start | load 1.14 1.59 1.49
16:55:45   -> filt-after-old.txt rc=0 | load 1.13 1.58 1.48
16:55:45 waitlow ok at 1.13 after 0s | load 1.13 1.58 1.48
16:55:45 filt-after-new start | load 1.13 1.58 1.48
16:55:47   -> filt-after-new.txt rc=0 | load 1.13 1.58 1.48
16:55:47   cmp filt-before vs filt-after-old: log raw rc=1 (20 lines), log norm rc=1, output norm rc=1 | lines 10/10 | load 1.13 1.58 1.48
16:55:47   cmp filt-before vs filt-after-new: log raw rc=1 (22 lines), log norm rc=1, output norm rc=1 | lines 10/10 | load 1.13 1.58 1.48
16:55:47 waitlow ok at 1.13 after 0s | load 1.13 1.58 1.48
16:55:47 scbash-after start | load 1.13 1.58 1.48
16:55:48   -> scbash-after.txt rc=1 | load 1.13 1.58 1.48
16:55:48   scbash-after: FAIL: 135 / 136 | # run-suite.sh end | load 1.13 1.58 1.48 | suite exit 1 | load 1.13 1.58 1.48
16:55:48 waitlow ok at 1.13 after 0s | load 1.13 1.58 1.48
16:55:48 c6-new start | load 1.13 1.58 1.48
17:01:45   -> c6-new.txt rc=1 | load 1.44 1.57 1.50
17:01:45 c6-new end | # run-suite.sh end | load 1.44 1.57 1.50 | suite exit 1 | load 1.44 1.57 1.50
17:01:45   c6-new marks: 23 inputs stalled, 38 gate-closed calls | load 1.44 1.57 1.50
17:02:05 waitlow ok at 1.17 after 20s | load 1.17 1.50 1.48
17:02:05 c1-new start | load 1.17 1.50 1.48
17:06:33   -> c1-new.txt rc=1 | load 2.01 1.72 1.57
17:06:33 c1-new end | # run-suite.sh end | load 2.01 1.72 1.57 | suite exit 1 | load 2.01 1.72 1.57
17:07:43 waitlow ok at 1.10 after 70s | load 1.10 1.51 1.50
17:07:43 c5-new start | load 1.10 1.51 1.50
17:12:31   -> c5-new.txt rc=1 | load 1.83 1.71 1.58
17:12:31 c5-new end | # run-suite.sh end | load 1.83 1.71 1.58 | suite exit 1 | load 1.83 1.71 1.58
17:13:21 waitlow ok at 1.08 after 50s | load 1.08 1.52 1.52
17:13:21 impl start | load 1.08 1.52 1.52
17:18:50   -> impl.txt rc=0 | load 1.70 1.70 1.59
17:18:50 impl end | FAIL: 0 / 961 | load 1.70 1.70 1.59
17:18:50 PHASE2 DONE | load 1.70 1.70 1.59
```

## 附录 G: run-suite.sh 检查的原始读数

```
[filt-before]
# run-suite.sh | 2026-10-24T16:55:24Z | hook af4658b6f935 | suite 60f7f95525cd | helper 213d01379695 | SC_BASH bash on PATH | SG_W10_ONLY ^V1-E16 | load 1.19 1.62 1.50
PASS: 8 / 8
FAIL: 0 / 8
# run-suite.sh end | load 1.19 1.62 1.50 | suite exit 0
[scbash-before]
# run-suite.sh | 2026-10-24T16:55:27Z | hook af4658b6f935 | suite 60f7f95525cd | helper 213d01379695 | SC_BASH bash on PATH | SG_W10_ONLY ^V1-E16 | load 1.19 1.62 1.50
PASS: 8 / 8
FAIL: 0 / 8
# run-suite.sh end | load 1.25 1.63 1.50 | suite exit 0
[log-before]
# run-suite.sh | 2026-10-24T16:55:39Z | hook af4658b6f935 | suite 60f7f95525cd | helper 213d01379695 | SC_BASH bash on PATH | SG_W10_ONLY ^V1-E16 | load 1.14 1.59 1.49
PASS: 8 / 8
FAIL: 0 / 8
# run-suite.sh end | load 1.14 1.59 1.49 | suite exit 0
[log-after]
run-suite.sh: SG_W10_LOG /tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/t002h/no-such-dir/w10.log: its directory does not exist (or the path cannot be made absolute); the log asked for cannot be written
[filt-after-old]
# run-suite.sh | 2026-10-24T16:55:42Z | hook af4658b6f935 | suite 60f7f95525cd | helper 213d01379695 | SC_BASH bash on PATH | SG_W10_ONLY ^V1-E16 | load 1.14 1.59 1.49
PASS: 8 / 8
FAIL: 0 / 8
# run-suite.sh end | load 1.13 1.58 1.48 | suite exit 0
[filt-after-new]
# run-suite.sh | 2026-10-24T16:55:45Z | hook af4658b6f935 | suite d4168aace3e8 | helper 213d01379695 | SC_BASH bash on PATH | SG_W10_ONLY ^V1-E16 | load 1.13 1.58 1.48
PASS: 8 / 8
FAIL: 0 / 8
# run-suite.sh end | load 1.13 1.58 1.48 | suite exit 0
[scbash-after]
# run-suite.sh | 2026-10-24T16:55:47Z | hook af4658b6f935 | suite d4168aace3e8 | helper 213d01379695 | SC_BASH /tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/t002h/no-such-dir/sub/bash | SG_W10_ONLY . | load 1.13 1.58 1.48
PASS: 1 / 136
FAIL: 135 / 136
# run-suite.sh end | load 1.13 1.58 1.48 | suite exit 1
[cmp-log-norm-old.diff]
10c10
< # load start 1.19 1.62 1.50 end 1.19 1.62 1.50 | timing batch: judged
---
> # load start 1.14 1.59 1.49 end 1.13 1.58 1.48 | timing batch: judged
[cmp-log-norm-new.diff]
10c10
< # load start 1.19 1.62 1.50 end 1.19 1.62 1.50 | timing batch: judged
---
> # load start 1.13 1.58 1.48 end 1.13 1.58 1.48 | timing batch: judged
[cmp-out-norm-old.diff]
7c7
< W10 ported cases: SC_BASH /usr/bin/bash (x86_64-pc-linux-gnu 5.2) -> relaxation expected: yes | load start 1.19 1.62 1.50 end 1.19 1.62 1.50 | timing batch: judged
---
> W10 ported cases: SC_BASH /usr/bin/bash (x86_64-pc-linux-gnu 5.2) -> relaxation expected: yes | load start 1.14 1.59 1.49 end 1.13 1.58 1.48 | timing batch: judged
[cmp-out-norm-new.diff]
7c7
< W10 ported cases: SC_BASH /usr/bin/bash (x86_64-pc-linux-gnu 5.2) -> relaxation expected: yes | load start 1.19 1.62 1.50 end 1.19 1.62 1.50 | timing batch: judged
---
> W10 ported cases: SC_BASH /usr/bin/bash (x86_64-pc-linux-gnu 5.2) -> relaxation expected: yes | load start 1.13 1.58 1.48 end 1.13 1.58 1.48 | timing batch: judged
[fallback-readlink]
readlink -m rc=1
[fallback-log]
run-suite.sh: SG_W10_LOG rel.log: its directory does not exist (or the path cannot be made absolute); the log asked for cannot be written
rc=3
[fallback-scbash]
# run-suite.sh | 2026-10-24T17:18:53Z | hook af4658b6f935 | suite d4168aace3e8 | helper 213d01379695 | SC_BASH rel-bash | SG_W10_ONLY ^V1-E16 | load 1.70 1.70 1.59

──────────────────────────────────────────────────
secret-guard.sh regression test -- FILTERED ROUND (SG_W10_ONLY=^V1-E16): only the ported W10 cases whose id matches ran; no other case, no SC-13
PASS: 1 / 8
FAIL: 7 / 8
SKIP: 0 / 8 (platform 0, load 0, void 0, inconclusive 0, root 0, other 0)
W10 ported cases: SC_BASH /tmp/tmp.2IwuIAu0DB/rel-bash (? ?.?) -> relaxation expected: no | load start 1.70 1.70 1.59 end 1.70 1.70 1.59 | timing batch: judged

Failures:

# run-suite.sh end | load 1.70 1.70 1.59 | suite exit 1
rc=1
```

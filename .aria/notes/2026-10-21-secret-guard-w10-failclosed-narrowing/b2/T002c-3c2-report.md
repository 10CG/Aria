# TASK-002 第三步 3c2 报告：6 组截止回落判法改定（10CG/aria-plugin#217）

执笔席（全新实例）。worktree `wt217/aria`，分支 `feature/secret-guard-w10-failclosed-narrowing`，基于 `5afef08`。只改了 `hooks/tests/secret-guard.test.sh`，没有 commit。

## 0. 结论速览

- 第 0 步，C3 跑在 3c 的代码上（旧的 2.85 s 判法）：21ac、21aj、21al、21ao 四组 FAIL，四条快命令的 W 分别为 2.47、2.84、2.38、2.47 s，都低于 2.85 s，被判不符；截止回落 6 / 10。这证明旧判法会把合法的检查点回落（F3）判红。
- 新判法下：
  - C3：6 组全部 PASS，截止回落 10 / 10，其中 7 条走 (b)、3 条走 (a)。
  - C1：6 组全部 FAIL。W >= 3.0 s 的只有 1 条（21ab 那条 4500 个「 a」，3.35 s），被记为回落，属固有限度。
  - C2：6 组全部 PASS，10 / 10，全部走 (a)，W 在 3.01-3.02 s 之间。
  - 实现整轮：`FAIL: 0 / 961`，SC-13 绿，6 组那一行为 `deadline fallback (截止回落) 0 / 10`。
  - commentsync：GREEN。
- 有一处预期写错：C2 的移植批另有 15 条 FAIL，原因是构造本身，与本次改动无关（见 2.3）。另有一条边距观察：负载尖峰下 (b) 的 1 s 余量只剩 0.12 s（见 2.1）。

## 1. 改了什么

套件改前 sha256 前缀为 `d085afae6834`，改后为 `60f7f95525cd`；58 行增、23 行删。改动落点按 `git diff -U0` 的 hunk 列出（行号为旧行号）：

- **2927**：6 组共用注释里「wall >= 2.85 s」那半句，改成对新判法的一句话描述（1 行变 2 行；2926 不变）。
- **2948-2958**：`wpa_x6` 上方的注释块整段改写（11 行变 26 行）。内容包括：
  - F1-F3 的推导，以及测量起点早于 `_SG_P0`；
  - 判法 (1)、(2)、(3a)、(3b)、(3c)，以及 1 s 余量为什么取在 F3 的 2 s 间隔正中；
  - 写明这条判法取代 3b 的 2.85 s 下界，原因是两侧各有一个洞（2.0-2.85 s 判红合法的 F3；2.85-3.0 s 分不开 F3 与提前关门）；
  - 固有限度（基线那一遍本身超过 3 s 的命令分不开）、不设负载门的理由、每组计一次、Summary 的内容。
  - 「2.85 s 与截止类用例同口径」的说法已删去。
- **2965 之后**：插入新 helper `wpa_x6_hook`（10 行）。它照 `wpa_err` 的方式跑一次 hook：在 `wpa_cwd` 下、带 `WPA_ENV`，用 `env -u` 清掉 `SECRET_GUARD_TIME_BUDGET_S`，另加的变量放在最后。墙钟取 `EPOCHREALTIME`，去掉 `[.,]` 后按 `10#` 算成整数微秒；另给一个两位小数的显示串。
- **2967-2980**：`wpa_x6` 函数体按新判法重写，函数首行（签名注释）不变。
- **3732**：Summary 的 6 组行只改了 `${wpa_x6_where% }`，变为 `${wpa_x6_where%; }`。列表项改成 `组名 W` 或 `组名 W/Tb Tb'`，项与项之间用 `; ` 分隔，格式与任务书的例子一致。

按 hunk 头核对，下面这些没有改动：6 组的调用行、基线支、`wpa_x6_eval`（2960-2965）、计数器初始化行（2959）、W10 移植块（403-427 里的 2.85 是移植的截止类用例，保留）。`wpa_x6` 改后的全文见 7.1（由脚本从套件提取，不是手抄）。

### 实现上我自己做的几处取舍（请主控复核）

1. **显示用截断**：两位小数用 `%d.%02d` 截断，不四舍五入。判定按微秒整数，显示截断后不会出现「显示 3.00s，却走了 (b)」这种与判定矛盾的读数。任务书只写了「显示时保留两位小数」，截断和四舍五入都符合字面，这个选择只影响显示。
2. **Tb' 读数为 0 时记不符**：(b) 里 Tb' 为 0 当作没有读数，记不符（失败即关）。helper 遇到没有可用时钟、或时钟回拨，都记 0。任务书字面是「Tb' <= W - 1.0 s 记截止回落」；对有效读数，加不加这条行为完全相同。不加的话，时钟回拨时 0 会被当成「关门那一遍很快」而认作回落，变成失败即开。W 读数为 0 时自然落到 (c)。
3. **不符细节的写法**：两句定性话按任务书原文用中文：「关门那一遍同样慢：是准入门提前关，不是重跑的检查点」「因时间的回落不会这么早结束」。前面加英文上下文，与套件其余英文细节一致：`baseline block at wall Ws, gate-closed Tb' Ts (want <= wall - 1.0 s):` 和 `baseline block at wall Ws (want > 2.0 s):`。
4. **注释里钉了 hook 的 sha256 前缀**：注释写了推导所依据的 hook「sha256 af4658b6f935」作为出处。hook 以后改动时这个前缀会过时；若主控不想在套件里钉 hash，删掉那个括号即可。
5. **组名取不到时写 `?`**：回落列表里的组名取自 `_wpa_name` 匹配 `SC-(21a[a-z])` 的部分，取不到时写 `?`。旧代码取不到时不列组名，但照样计数。6 组的调用都在 SC-21a* 用例里，实测没有出现过 `?`。

## 2. 各轮预期与结果

预期都先写、后跑：
- `t002f/expect-0-c3-old.md`：写于第 0 步开跑之前；
- `t002f/expect-2-new.md`：写于套件改完之后、第 2 步开跑之前。

每轮开跑前都经 waitlow（一分钟负载低于 1.2 才开跑），最长等了 140 s，没有出现等满 30 分钟后照跑的情况。

| 轮 | hook | 套件 | 时段 (UTC) | 首负载 | 尾负载 | 6 组 | 截止回落 | 预期 |
|---|---|---|---|---|---|---|---|---|
| 0. C3 旧代码 | 2a9e3d898705 | d085afae6834 | 14:52:54-14:58:23 | 1.10 | 2.52 | 21ac/21aj/21al/21ao FAIL，21ab/21ag PASS | 6 / 10 | 成立 |
| 2. C3 新代码 | 2a9e3d898705 | 60f7f95525cd | 15:00:50-15:06:33 | 1.13 | 2.56 | 全 PASS | 10 / 10 | 成立（(a)/(b) 的分布有出入，见 2.1） |
| 2. C1 新代码 | 93c7f2fac02a | 60f7f95525cd | 15:08:53-15:13:34 | 1.01 | 2.75 | 全 FAIL | 1 / 10 | 成立 |
| 2. C2 新代码 | f76baeb0e1c8 | 60f7f95525cd | 15:15:34-15:21:12 | 1.17 | 2.39 | 全 PASS | 10 / 10 | 6 组成立；移植批的预期写错（见 2.3） |
| 2. 实现 | af4658b6f935 | 60f7f95525cd | 15:23:12-15:29:10 | 1.04 | 1.34（套件在 W10 批结束时自记）/ 2.92（驱动记于 15:29:10） | 全 PASS | 0 / 10 | 成立 |
| commentsync | — | 60f7f95525cd | 14:58 前后 | — | — | — | — | GREEN，成立 |

C1、C2 的 hook 前缀与 3c 的 `93c7f2fac02a`、`f76baeb0e1c8` 相同：都用同一段构造文本、从同一个实现 hook `af4658b6f935` 构造，所以本轮结果可以和 3c 的 C1/C2 直接对照。C3 是本段新加的构造：在 `_sg_relax_job` 里 `kill -0 "$tp"` 那一行之后、`_SG_RELAXED=1` 之前，加了 `sleep 2.2; return 1`。

### 2.0 C3 跑在 3c 代码上（第 0 步）

- **预期**：21ac、21al、21ao 确定 FAIL；21aj、21ab 贴在 2.85 s 两侧，结果不定；21ag PASS；回落约 5-7 / 10。
- **结果**：
  - 21ac 2.47 s、21aj 2.84 s（三条里最快的那条）、21al 2.38 s、21ao 2.47 s 被判不符（`wall under 2.85`），这四组 FAIL。
  - 21ab 的三条、21ag 的一条、21aj 的另两条认作回落，所以是 6 / 10。
  - 结论：合法的 F3 回落落在 2.0-2.85 s 之间时，被旧判法判红。
- **其他红**：SC-13（副本不是 git 检出），外加移植批 19 条（构造让放宽结局不出现）。

### 2.1 C3 跑在新代码上

- **结果**：`10 / 10`，7 条走 (b)，3 条走 (a)。原文见 7.2。
- **与预测的出入**：我是按 3c C1 量的 Tb 来预测的（那轮负载升到 4.56），所以预测 21aj 的 1.02 s、1.62 s 两条走 (a)。实测这轮 21aj 三条的 Tb' 都在 0.67-0.69 s，W 在 2.83-2.92 s，全部走 (b)。它们都计作回落，组级结果与预期相同。
- **边距观察（不是规格矛盾）**：
  - 21ab 第一条（`wpa_vx_cmd 159`）W 2.86 s、Tb' 1.74 s，离阈值 `W - 1.0 = 1.86 s` 只差 0.12 s。
  - 同一条命令在 C1 里关门时只要 0.63 s。紧接着的 9000 填充那条 W 4.97 s，远超 3 s：基线那一遍自己就超过了截止，属于 F1。两点合起来说明那一刻主机卡了一下。
  - 也就是说，负载尖峰能吃掉 1 s 余量的大半。6 组按 3b 裁定不设负载门，尖峰再大一点就会把合法的 F3 判红（假红）。我没有改判法，交主控定是否处理（例如关门那一遍跑两次取较小值；仅供参考）。
- **其他红**：SC-13 加移植批 19 条，与第 0 步那轮的移植批 FAIL 是**逐条相同的集合**（见 7.5，用 diff 核对）。这旁证本次改动不影响移植块。

### 2.2 C1 跑在新代码上（准入门恒关）

- **结果**：6 组全部 FAIL。各条不符的要素（摘自细节原文）：
  - 21ab：`wpa_vx_cmd 159` 那条 W 0.63 s，走 (c)；9000 填充那条 W 2.34 s、Tb' 2.37 s，走 (b)，细节带「是准入门提前关」。
  - 21ac：W 0.26 s，走 (c)。
  - 21ag：W 1.11 s，走 (c)。
  - 21aj：三条分别为 0.89、1.14、1.00 s，都走 (c)。
  - 21al：W 0.17 s，走 (c)。
  - 21ao：W 0.28 s，走 (c)。
- **W >= 3.0 s、被记为截止回落的命令（与合法回落分不开）**：只有 1 条，是 21ab 的「`f=x; echo $f` + 4500 个「 a」」，W 3.35 s。认定方法是排除法：21ab 一共三条命令，不符细节里列出的是另两条（`f=/etc/forgejo/app.ini; p=...` 即 `wpa_vx_cmd 159`，和 `f=x; echo $f yyyy...` 即 9000 填充）。21ab 仍因那两条 FAIL。
- **与 3c C1 对照**：3c 那轮越过 2.85 s 的是 9000 填充那条，4500 个「 a」那条是 2.60 s；本轮正好反过来（9000 填充 2.34 s，4500 个「 a」3.35 s）。哪条慢随负载变，所以固有限度可能落在任一条慢命令上。本轮每组都有 W < 3.0 s 的命令，组级都抓住了。
- **其他红**：SC-13 加移植批 18 条，6 组 6 条，合计 25 行 FAIL，与 3c C1 的 25 相同。

### 2.3 C2 跑在新代码上（作业里计时器起来之后 `sleep 4`）

- **6 组**：全部 PASS，`10 / 10`，全部走 (a)，W 在 3.01-3.02 s 之间，明细里没有 `/Tb`。
- **与预期不符的一处（不在 6 组）**：
  - 移植批另有 15 条 FAIL：V2-E8；V4-S1/S2/S3/S7/S8/S19；V5-S9/S13；V7-E1/E13/E14/E15；V9-E10/E11。我原先预期「只有 SC-13，与 3c C2 相同」。
  - 原因：3c 那轮 C2 计时批结束时负载高，记为 `timing batch: void`，移植批 FAIL 为 0；本轮计时批 `judged`。凡是要求放宽结局的用例，都因构造（重跑一律拖过截止）回落而红，例如 `FAIL [W10-port V4-S1-allow]: rc=4 (want 0) wall=1.00s ... [fallback]`。
  - 这是构造本该产生的效果，与本次改动无关：移植块没动（见第 1 节的 hunk），C3 新旧两轮的移植批 FAIL 集合逐条相同。我的预期写错了，错在照搬了 3c 那轮 void 的结果。

### 2.4 实现整轮（worktree，PATH 上的 bash 5.2.15，一次）

- `FAIL: 0 / 961`，`SKIP: 0 / 961`，计时批 `judged`。
- SC-13 绿：总数与 3c 整轮的 `FAIL: 0 / 961` 相同，头注释为 `Coverage: 967 cases (961 without zsh)`，6 组仍各计一次。
- 6 组那一行：`deadline fallback (截止回落) 0 / 10`。没有回落，所以不列明细。

### 2.5 commentsync

`v31/commentsync.py --suite-only <改后的套件> target` 输出 `target --suite-only: GREEN`，完整输出在 `t002f/commentsync.txt`。

## 3. 首尾负载

见第 2 节的表。各轮的首行、末行原文见 7.3，waitlow 的记录见 7.6（drive.log）。

## 4. 未做或拿不准的项

1. 第 1 节的取舍 1-5：显示截断；Tb' 为 0 视为没有读数；细节中英文并写；注释钉 hook 的 hash；组名取不到写 `?`。请主控复核。
2. 负载尖峰下 (b) 的余量实测只剩 0.12 s（2.1）。这是判法设计层面的问题，我没改。
3. C1 的固有限度：W >= 3.0 s 的那条（21ab 4500 个「 a」，3.35 s）被记为回落。按 3c 裁定这属于固有限度，由每组至少一条快命令兜住；本轮成立。
4. 预期写错一处（C2 的移植批），见 2.3。
5. 本段范围外、没有做的：其他 bash 版本、SG_W10_ONLY 过滤轮、坏实现的套件模式、导出 WSL 变量的整轮。
6. 没有 commit（按纪律）。worktree 状态为 ` M hooks/tests/secret-guard.test.sh`。没有发现 hook 缺陷或规格矛盾，所以没有停下。

## 5. 文件（都在 `r217impl/t002f/`）

- 预期：`expect-0-c3-old.md`、`expect-2-new.md`
- 构造与驱动：
  - `mkc.py`：构造 C1/C2/C3，C1/C2 的文本与 3c 相同；产物为 `c1-hook.sh`、`c2-hook.sh`、`c3-hook.sh`
  - `lib.sh`（照 t002e 的 waitlow）、`phase1.sh`、`phase2.sh`、`waitpid.sh`、`summ.sh`
  - `patch3c2.py`：改套件用；按行锚定，每个锚点须恰好命中一次
- 输出：`c3-old.txt`、`c3-new.txt`、`c1-new.txt`、`c2-new.txt`、`impl.txt`、`impl.log`、`commentsync.txt`、`drive.log`、`pids.txt`

## 6. 进程

- 我记下的驱动 PID：phase1 为 2308564，phase2 为 2348485（setsid 那一层包装进程启动后立刻退出）。
- 收尾时两个驱动都已退出（`ps -p` 查无），不需要清理。
- run-suite.sh 的临时目录 `t002f/work` 已清空。

## 7. 附：脚本提取的证据（不是手抄）

### 7.1 改后的落点原文（sed 从 worktree 套件提取）

6 组共用注释（改后 3 行）：
```bash
# In the relaxed branch a trigger-point command (a copy over 8192) goes through wpa_x6, which also accepts the deadline fallback (the baseline branch's
# assertion on the same output, with a wall only a fallback for time gives: >= 3.0 s, or over 2.0 s with a gate-closed run of the same input at least
# 1.0 s quicker; see wpa_x6), and the summary counts those fallbacks.
```

wpa_x6 上方注释块、（未改的）计数器行与 wpa_x6_eval、新 helper wpa_x6_hook、wpa_x6 全文：
```bash
# Deadline fallback of the relaxed branch (plan notes: the 3b ruling, its 2.85 s bound replaced by (1) of the 3c ruling; technical, the posture unchanged).
# A trigger-point command there -- its copy over 8192: 21ab's three, 21ac's 4096-character for list, 21ag, 21aj's three, the 8193 of 21al and 21ao --
# runs the hook ONCE (wpa_x6_hook; SECRET_GUARD_TIME_BUDGET_S cleared, so the deadline is _SG_P0 + 3 s). Its wall W is taken by EPOCHREALTIME and
# compared in whole microseconds, never rounded first (shown cut to two decimals). Why the hook falls back: the baseline pass runs first and on a busy
# host takes much of the 3 s (21ab: 2.37-2.58 s for the whole hook at load 1.2-1.6, 2.39-3.08 s gate-closed, b2/t002d-verify/probe.txt), and then the
# hook gives the baseline's block (What 4; P3, P6). Worked out from the hook (sha256 af4658b6f935), a fallback for time has three ways and no other:
#   F1 the gate closes for lack of time: _sg_relax_left gives status 1 only once now >= _SG_P0 + 3 s;
#   F2 the deadline kills the job: its timer (sleep "$_SG_LEFT") starts after _SG_LEFT is worked out, so the kill comes after _SG_P0 + 3 s;
#   F3 the rerun's own time checkpoint: _sg_vx_collect resets _SG_T0=$SECONDS and _sg_over_budget sends the rerun back (status 3, then the baseline
#      block) once SECONDS - _SG_T0 >= 3; SECONDS counts whole seconds, so that is more than 2 s and at most 3 s after the reset, which comes after the
#      job starts, which comes after the baseline pass (its time Tb) ends.
# W starts before the hook process does, so before _SG_P0: F1 and F2 give W > 3.0 s; F3 gives W > Tb + 2 s, which is 2-3 s for a command whose
# baseline pass takes under 1 s; any fallback for time gives W > 2.0 s. A gate that closes early (a bad implementation) gives W about Tb. The rule:
# (1) the relaxed branch's assertion holds on that output: passes. (2) Otherwise, when the baseline branch's assertion for that command (the else
# branch's wpa_x_toolarge and its limit line) does not hold on the SAME output either: the check is off, its detail naming both assertions' misses and
# W. (3) Otherwise (the output is the baseline's block): (a) W >= 3.0 s: a deadline fallback (F1, F2 or a late F3). (b) 2.0 s < W < 3.0 s: the same
# input runs once more -- the same variables and directory, the budget variable cleared, plus WSL_DISTRO_NAME=Ubuntu, which closes the gate -- and its
# wall is Tb'; Tb' <= W - 1.0 s is a deadline fallback (F3: the checkpoint sent the rerun back, W more than 2 s over the baseline pass); otherwise the
# check is off with W and Tb' (the gate-closed run is as slow: the gate closed early, not the rerun's checkpoint). 1 s sits in the middle of F3's 2 s
# gap and leaves 1 s on each side for load jitter. (c) W <= 2.0 s: the check is off with W (a fallback for time does not end this early).
# This replaces the 3b rule's lower bound of 2.85 s, which was copied from the deadline cases instead of worked out from the hook and had a hole on
# each side: from 2.0 to 2.85 s it turned a lawful F3 red, and from 2.85 to 3.0 s it could not tell F3 from a gate that closed early. Left as it is
# (the 3c ruling): a command whose baseline pass alone runs past 3 s gives the same output as a lawful "no time to close the gate" and cannot be told
# apart; each group has a command with a quick baseline pass, and the ported cases cover the rest. No load gate: the six groups run late in the suite,
# where 3b's seven full rounds ended at load 2.21-4.13, so a gate would SKIP them nearly every round. A group still counts once; the summary line of the
# six groups gives the fallbacks over the trigger-point commands judged, each with its group and W (and Tb' for (b)).
wpa_x6_n=0; wpa_x6_fb=0; wpa_x6_where=''
wpa_x6_eval() {   # <output as wpa_err gives it> <longline | pass | growth | toolarge> <limit line> <command> -> "<checks off>" TAB "<their list>": the assertion
                  # helper itself, in a subshell where wpa_err / wpa_rc hand back that output, so both branches judge ONE run of the hook
  ( wpa_x6_e=$1; wpa_err() { printf '%s' "$wpa_x6_e"; }; wpa_rc() { printf '%s' "${wpa_x6_e##*WPA_RC=}"; }; _wpa_bad=''; _wpa_nbad=0
    case $2 in longline) wpa_x_longline "$4" ;; pass) wpa_x Bash 0 "$4" ;; growth) wpa_x_toolarge "$4" "$wpa_L_gseg" ;; *) wpa_x_toolarge "$4" "$3" ;; esac
    printf '%s\t%s' "$_wpa_nbad" "$_wpa_bad" )
}
wpa_x6_hook() {   # <input> [NAME=VALUE ...]: one run of the hook on <input> the way wpa_err runs it (in wpa_cwd, with WPA_ENV), SECRET_GUARD_TIME_BUDGET_S
                  # cleared and the extra variables last; sets wpa_x6_out (stderr, then WPA_RC=), wpa_x6_us (the wall in whole microseconds by EPOCHREALTIME,
                  # 0 without a usable clock) and wpa_x6_s (that wall in seconds cut to two decimals, for display only) -- wpa_x6's locals
  local in=$1 t0 t1; shift
  t0=${EPOCHREALTIME:-}
  wpa_x6_out="$( cd "$wpa_cwd" && printf '%s' "$in" | env -u SECRET_GUARD_TIME_BUDGET_S "${WPA_ENV[@]}" "$@" "$WPA_HOOK" 2>&1 >/dev/null; echo "WPA_RC=$?" )"
  t1=${EPOCHREALTIME:-}; t0=${t0/[.,]/}; t1=${t1/[.,]/}; wpa_x6_us=0
  [[ $t0 =~ ^[0-9]+$ && $t1 =~ ^[0-9]+$ ]] && (( 10#$t1 > 10#$t0 )) && wpa_x6_us=$(( 10#$t1 - 10#$t0 ))
  printf -v wpa_x6_s '%d.%02d' $(( wpa_x6_us / 1000000 )) $(( wpa_x6_us % 1000000 / 10000 ))
}
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
  elif (( wus > 2000000 )); then   # (3b) F3 or a gate closed early: the same input once more with the gate closed (a reading of 0 is no reading)
    wpa_x6_hook "$input" WSL_DISTRO_NAME=Ubuntu
    if (( wpa_x6_us > 0 && wpa_x6_us <= wus - 1000000 )); then fb="${ws}s/Tb ${wpa_x6_s}s"
    else bad="baseline block at wall ${ws}s, gate-closed Tb' ${wpa_x6_s}s (want <= wall - 1.0 s): 关门那一遍同样慢：是准入门提前关，不是重跑的检查点"; fi
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

Summary 的 6 组行：
```bash
echo "W10 older groups 21ab 21ac 21ag 21aj 21al 21ao: ${wpa_rx6_note:-branch not chosen} | deadline fallback (截止回落) ${wpa_x6_fb:-0} / ${wpa_x6_n:-0}${wpa_x6_where:+ (${wpa_x6_where%; })}"
```

### 7.2 各轮 6 组那一行原文

c3-old:
```
W10 older groups 21ab 21ac 21ag 21aj 21al 21ao: relaxed branch (new outcomes) | bash on PATH /usr/bin/bash 5.2.15(1)-release (machtype x86_64-pc-linux-gnu) | osrelease 6.17.9-1-pve | WSLInterop no | WSL_DISTRO_NAME '' WSL_INTEROP '' | deadline fallback (截止回落) 6 / 10 (21ab 21ab 21ab 21ag 21aj 21aj)
```

c3-new:
```
W10 older groups 21ab 21ac 21ag 21aj 21al 21ao: relaxed branch (new outcomes) | bash on PATH /usr/bin/bash 5.2.15(1)-release (machtype x86_64-pc-linux-gnu) | osrelease 6.17.9-1-pve | WSLInterop no | WSL_DISTRO_NAME '' WSL_INTEROP '' | deadline fallback (截止回落) 10 / 10 (21ab 2.86s/Tb 1.74s; 21ab 4.97s; 21ab 3.01s; 21ac 2.48s/Tb 0.26s; 21ag 3.01s; 21aj 2.83s/Tb 0.67s; 21aj 2.91s/Tb 0.67s; 21aj 2.92s/Tb 0.69s; 21al 2.39s/Tb 0.16s; 21ao 2.51s/Tb 0.27s)
```

c1-new:
```
W10 older groups 21ab 21ac 21ag 21aj 21al 21ao: relaxed branch (new outcomes) | bash on PATH /usr/bin/bash 5.2.15(1)-release (machtype x86_64-pc-linux-gnu) | osrelease 6.17.9-1-pve | WSLInterop no | WSL_DISTRO_NAME '' WSL_INTEROP '' | deadline fallback (截止回落) 1 / 10 (21ab 3.35s)
```

c2-new:
```
W10 older groups 21ab 21ac 21ag 21aj 21al 21ao: relaxed branch (new outcomes) | bash on PATH /usr/bin/bash 5.2.15(1)-release (machtype x86_64-pc-linux-gnu) | osrelease 6.17.9-1-pve | WSLInterop no | WSL_DISTRO_NAME '' WSL_INTEROP '' | deadline fallback (截止回落) 10 / 10 (21ab 3.01s; 21ab 3.01s; 21ab 3.01s; 21ac 3.01s; 21ag 3.01s; 21aj 3.01s; 21aj 3.01s; 21aj 3.02s; 21al 3.01s; 21ao 3.01s)
```

impl:
```
W10 older groups 21ab 21ac 21ag 21aj 21al 21ao: relaxed branch (new outcomes) | bash on PATH /usr/bin/bash 5.2.15(1)-release (machtype x86_64-pc-linux-gnu) | osrelease 6.17.9-1-pve | WSLInterop no | WSL_DISTRO_NAME '' WSL_INTEROP '' | deadline fallback (截止回落) 0 / 10
```

### 7.3 各轮首行与末行
```
[c3-old]
# run-suite.sh | 2026-10-24T14:52:54Z | hook 2a9e3d898705 | suite d085afae6834 | helper 213d01379695 | SC_BASH bash on PATH | SG_W10_ONLY <none> | load 1.10 1.17 1.66
# run-suite.sh end | load 2.52 2.15 1.96 | suite exit 1
[c3-new]
# run-suite.sh | 2026-10-24T15:00:50Z | hook 2a9e3d898705 | suite 60f7f95525cd | helper 213d01379695 | SC_BASH bash on PATH | SG_W10_ONLY <none> | load 1.13 1.74 1.83
# run-suite.sh end | load 2.56 2.18 1.99 | suite exit 1
[c1-new]
# run-suite.sh | 2026-10-24T15:08:53Z | hook 93c7f2fac02a | suite 60f7f95525cd | helper 213d01379695 | SC_BASH bash on PATH | SG_W10_ONLY <none> | load 1.01 1.69 1.83
# run-suite.sh end | load 2.75 2.55 2.17 | suite exit 1
[c2-new]
# run-suite.sh | 2026-10-24T15:15:34Z | hook f76baeb0e1c8 | suite 60f7f95525cd | helper 213d01379695 | SC_BASH bash on PATH | SG_W10_ONLY <none> | load 1.17 2.03 2.02
# run-suite.sh end | load 2.39 2.13 2.04 | suite exit 1
[impl]
FAIL: 0 / 961
SKIP: 0 / 961 (platform 0, load 0, void 0, inconclusive 0, root 0, other 0)
W10 ported cases: SC_BASH /usr/bin/bash (x86_64-pc-linux-gnu 5.2) -> relaxation expected: yes | load start 1.04 1.76 1.92 end 1.34 1.72 1.90 | timing batch: judged
```

### 7.4 改动形状（git diff）
```
 hooks/tests/secret-guard.test.sh | 81 ++++++++++++++++++++++++++++------------
 1 file changed, 58 insertions(+), 23 deletions(-)
@@ -2927 +2927,2 @@ wpa_x_toolarge() {   # <command> <the limit line it must name: wpa_L_*>: refused
@@ -2948,11 +2949,26 @@ wpa_x_hit() {   # <command>: (relaxed branch) judged and blocked with the ordina
@@ -2965,0 +2982,10 @@ wpa_x6_eval() {   # <output as wpa_err gives it> <longline | pass | growth | too
@@ -2967,6 +2993,3 @@ wpa_x6() {   # <the relaxed assertion: longline | pass (exit 0) | growth (wpa_L_
@@ -2974 +2997 @@ wpa_x6() {   # <the relaxed assertion: longline | pass (exit 0) | growth (wpa_L_
@@ -2976,2 +2999,14 @@ wpa_x6() {   # <the relaxed assertion: longline | pass (exit 0) | growth (wpa_L_
@@ -2980 +3015 @@ wpa_x6() {   # <the relaxed assertion: longline | pass (exit 0) | growth (wpa_L_
@@ -3732 +3767 @@ echo "W10 ported cases: $sg_w10_batch"
 M hooks/tests/secret-guard.test.sh
```

### 7.5 移植批 FAIL 集合：C3 旧代码 vs C3 新代码
```
identical (19 ids)
```

### 7.6 summ.sh 对各轮的摘要（6 组不符细节只取命令前缀、W、Tb、判定词）与 drive.log
```
== c3-old.txt: lines with 'FAIL [' 24
deadline fallback (截止回落) 6 / 10 (21ab 21ab 21ab 21ag 21aj 21aj)
SC-13,W10-port V2-E6-flag-from-environment-ignored,W10-port V2-E8-ostype-from-environment-ignored,W10-port V3-E4-cap-3-at-budget-4,W10-port V4-S19-block-text-bytes,W10-port V4-S1-allow,W10-port V4-S2-block-with-text,W10-port V4-S3-block-without-text,W10-port V4-S7-time-checkpoint,W10-port V4-S8-internal-error,W10-port V5-E19-deadline-with-term-ignored,W10-port V5-S13-detached-child,W10-port V5-S9-child-left-behind,W10-port V6-E2-deadline-fallback-bytes,W10-port V7-E13-multiline-copy-normal-text,W10-port V7-E14-long-line-from-expansion,W10-port V7-E15-credit-as-normal,W10-port V7-E1-benign-big-allowed,W10-port V9-E10-count-axis-read-blocked,W10-port V9-E11-tmax-in-rerun,W10 SC-21ac,W10 SC-21aj,W10 SC-21al,W10 SC-21ao,
SC-21ac: {Bash for f in /dddddddddddd want 'yes', got 'no'} {longline [for f in /dddddddddddddddddddddddddddddddddddddd]: Matched pattern:: want 'yes', got 'no'} {longline [for f in /dddddddddddddddddddddddddddddddddddddd]: not the size text: want 'no', got 'yes'} | deadline fallback (baseline branch; wall 2.47s, want >= 2.85 wall under 2.85 
SC-21aj: {Bash f=/etc/forgejo/app.ini want 'a command segment grows by more than 8192 characters after variable expansion', got 'a command segment is longer than 8192 characters after variable expansion'} | deadline fallback (baseline branch; wall 2.84s, want >= 2.85 wall under 2.85 
SC-21al: {Bash f=/etc/forgejo/app.ini want 'yes', got 'no'} {longline [f=/etc/forgejo/app.ini; p=xxxxxxxxxxxxxxxxxxxxxx]: Matched pattern:: want 'yes', got 'no'} {longline [f=/etc/forgejo/app.ini; p=xxxxxxxxxxxxxxxxxxxxxx]: not the size text: want 'no', got 'yes'} | deadline fallback (baseline branch; wall 2.38s, want >= 2.85 wall under 2.85 
SC-21ao: {Bash f=/etc/forgejo/app.ini want 'yes', got 'no'} {longline [f=/etc/forgejo/app.ini; p=xxxxxxxxxxxxxxxxxxxxxx]: Matched pattern:: want 'yes', got 'no'} {longline [f=/etc/forgejo/app.ini; p=xxxxxxxxxxxxxxxxxxxxxx]: not the size text: want 'no', got 'yes'} | deadline fallback (baseline branch; wall 2.47s, want >= 2.85 wall under 2.85 
# run-suite.sh end | load 2.52 2.15 1.96 | suite exit 1
== c3-new.txt: lines with 'FAIL [' 20
deadline fallback (截止回落) 10 / 10 (21ab 2.86s/Tb 1.74s; 21ab 4.97s; 21ab 3.01s; 21ac 2.48s/Tb 0.26s; 21ag 3.01s; 21aj 2.83s/Tb 0.67s; 21aj 2.91s/Tb 0.67s; 21aj 2.92s/Tb 0.69s; 21al 2.39s/Tb 0.16s; 21ao 2.51s/Tb 0.27s)
SC-13,W10-port V2-E6-flag-from-environment-ignored,W10-port V2-E8-ostype-from-environment-ignored,W10-port V3-E4-cap-3-at-budget-4,W10-port V4-S19-block-text-bytes,W10-port V4-S1-allow,W10-port V4-S2-block-with-text,W10-port V4-S3-block-without-text,W10-port V4-S7-time-checkpoint,W10-port V4-S8-internal-error,W10-port V5-E19-deadline-with-term-ignored,W10-port V5-S13-detached-child,W10-port V5-S9-child-left-behind,W10-port V6-E2-deadline-fallback-bytes,W10-port V7-E13-multiline-copy-normal-text,W10-port V7-E14-long-line-from-expansion,W10-port V7-E15-credit-as-normal,W10-port V7-E1-benign-big-allowed,W10-port V9-E10-count-axis-read-blocked,W10-port V9-E11-tmax-in-rerun,
# run-suite.sh end | load 2.56 2.18 1.99 | suite exit 1
== c1-new.txt: lines with 'FAIL [' 25
deadline fallback (截止回落) 1 / 10 (21ab 3.35s)
SC-13,W10-port V2-E6-flag-from-environment-ignored,W10-port V2-E8-ostype-from-environment-ignored,W10-port V2-G15-cwd-project-without-extension-file,W10-port V2-G16-environment-root-before-cwd,W10-port V2-G1-gate,W10-port V2-G3b-gate-uses-build-facts,W10-port V2-G4-project-without-extension-file,W10-port V3-E3-anchor-at-hook-start,W10-port V3-E4-cap-3-at-budget-4,W10-port V3-E5-budget-2,W10-port V5-E19-deadline-with-term-ignored,W10-port V6-E2-deadline-fallback-bytes,W10-port V7-E13-multiline-copy-normal-text,W10-port V7-E14-long-line-from-expansion,W10-port V7-E15-credit-as-normal,W10-port V7-E1-benign-big-allowed,W10-port V9-E10-count-axis-read-blocked,W10-port V9-E11-tmax-in-rerun,W10 SC-21ab,W10 SC-21ac,W10 SC-21ag,W10 SC-21aj,W10 SC-21al,W10 SC-21ao,
SC-21ab: {Bash f=/etc/forgejo/app.ini wall 0.63s want > 2.0 s 这么早结束 {Bash f=x; echo $f yyyyyyyyy wall 2.34s Tb' 2.37s want <= wall - 1.0 s 是准入门提前关 
SC-21ac: {Bash for f in /dddddddddddd wall 0.26s want > 2.0 s 这么早结束 
SC-21ag: {Bash v0=aaaaaaaaaaaaaaaaaaa wall 1.11s want > 2.0 s 这么早结束 
SC-21aj: {Bash f=/etc/forgejo/app.ini wall 0.89s want > 2.0 s 这么早结束 {Bash f=/etc/forgejo/app.ini wall 1.14s want > 2.0 s 这么早结束 {Bash f=/etc/forgejo/app.ini wall 1.00s want > 2.0 s 这么早结束 
SC-21al: {Bash f=/etc/forgejo/app.ini wall 0.17s want > 2.0 s 这么早结束 
SC-21ao: {Bash f=/etc/forgejo/app.ini wall 0.28s want > 2.0 s 这么早结束 
# run-suite.sh end | load 2.75 2.55 2.17 | suite exit 1
== c2-new.txt: lines with 'FAIL [' 16
deadline fallback (截止回落) 10 / 10 (21ab 3.01s; 21ab 3.01s; 21ab 3.01s; 21ac 3.01s; 21ag 3.01s; 21aj 3.01s; 21aj 3.01s; 21aj 3.02s; 21al 3.01s; 21ao 3.01s)
SC-13,W10-port V2-E8-ostype-from-environment-ignored,W10-port V4-S19-block-text-bytes,W10-port V4-S1-allow,W10-port V4-S2-block-with-text,W10-port V4-S3-block-without-text,W10-port V4-S7-time-checkpoint,W10-port V4-S8-internal-error,W10-port V5-S13-detached-child,W10-port V5-S9-child-left-behind,W10-port V7-E13-multiline-copy-normal-text,W10-port V7-E14-long-line-from-expansion,W10-port V7-E15-credit-as-normal,W10-port V7-E1-benign-big-allowed,W10-port V9-E10-count-axis-read-blocked,W10-port V9-E11-tmax-in-rerun,
# run-suite.sh end | load 2.39 2.13 2.04 | suite exit 1
== impl.txt: lines with 'FAIL [' 0
deadline fallback (截止回落) 0 / 10

W10 older groups 21ab 21ac 21ag 21aj 21al 21ao: relaxed branch (new outcomes) | bash on PATH /usr/bin/bash 5.2.15(1)-release (machtype x86_64-pc-linux-gnu) | osrelease 6.17.9-1-pve | WSLInterop no | WSL_DISTRO_NAME '' WSL_INTEROP '' | deadline fallback (截止回落) 0 / 10
--- drive.log
14:52:54 phase1 begin | worktree 5afef08 status [] | load 1.10 1.17 1.66
14:52:54 impl hook af4658b6f935 suite d085afae6834 | load 1.10 1.17 1.66
constructions built
14:52:54 c1 hook 93c7f2fac02a | load 1.10 1.17 1.66
14:52:54 c2 hook f76baeb0e1c8 | load 1.10 1.17 1.66
14:52:54 c3 hook 2a9e3d898705 | load 1.10 1.17 1.66
14:52:54 waitlow ok at 1.10 after 0s | load 1.10 1.17 1.66
14:52:54 C3-old start | load 1.10 1.17 1.66
14:58:23 C3-old end rc=1 | load 2.52 2.15 1.96
14:58:23 phase1 done | load 2.52 2.15 1.96
14:58:30 phase2 begin | worktree status [ M hooks/tests/secret-guard.test.sh ] | suite 60f7f95525cd | load 2.71 2.20 1.97
15:00:50 waitlow ok at 1.13 after 140s | load 1.13 1.74 1.83
15:00:50 C3-new start | load 1.13 1.74 1.83
15:06:33 C3-new end rc=1 | load 2.56 2.18 1.99
15:08:53 waitlow ok at 1.01 after 140s | load 1.01 1.69 1.83
15:08:53 C1-new start | load 1.01 1.69 1.83
15:13:34 C1-new end rc=1 | load 2.75 2.55 2.17
15:15:34 waitlow ok at 1.17 after 120s | load 1.17 2.03 2.02
15:15:34 C2-new start | load 1.17 2.03 2.02
15:21:12 C2-new end rc=1 | load 2.39 2.13 2.04
15:23:12 waitlow ok at 1.04 after 120s | load 1.04 1.76 1.92
15:23:12 impl start | load 1.04 1.76 1.92
15:29:10 impl end rc=0 | # load start 1.04 1.76 1.92 end 1.34 1.72 1.90 | timing batch: judged | load 2.92 2.38 2.13
15:29:10 phase2 done | worktree status [ M hooks/tests/secret-guard.test.sh ] | load 2.92 2.38 2.13
```

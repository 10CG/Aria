---
checkpoint: post_spec
mode: convergence
rounds: 8
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
drift_warning: false
is_refocus: false
verdict: PASS
timestamp: 2026-09-17T08:53:56.000Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [qa-engineer]
---

# post_spec Round 8 — qa-engineer 席

> 被审 SHA `a563192` (v9)。方法: 全程只读仓库, 未编辑仓库内任何文件 (`git status --short` 复核, 见 SC 实测记录 0); 唯一写入仓库的文件是本报告。临时文件全部落
> `/tmp/claude-1000/-home-dev-Aria/e91a9d6a-05ff-4b26-af79-8d903c21a292/scratchpad/r8-qa-engineer/`。**未读**本轮其他席已落盘的 R8 报告 (`git status --short` 显示 `code-reviewer.md` 已存在, 未打开)。
>
> 方法论: 未直接信任主控提供的 `selfcheck_v9.py`——先用不同代码形状 (正则抽取 + 显式 for 循环判定, 而非其
> `txt.index()` 切片 + 列表推导) 独立重写抽取与十条 SC 判定 (`qa_r8_check.py`), 独立跑通后与 `selfcheck_v9.py`
> 的结论逐项对表, 完全一致才采信。SC-13 与 `fault_matrix.py` 守卫另外用**真实脚本真实调用**验证 (不用模拟文本),
> 包括在独立临时目录里对现仓库现存的 `v6-per-call-health-opus5/fault_matrix.py` 做一次全新的正确版 + 反事实版
> 实跑, 以及对加固后的 `--out` 守卫做五类输入的对抗测试。

## R7 对账

本席 R7 报告 1 条 major: 「SC-9 只锚定标签词「逐调用健康检查不通过」, 不锚定实质判定语句「即不健康的调用足以改变判定」; 静默改写为 v6a 旧语义后 12 条 SC 全绿、无一转红」。

**判定: closed。**

实测 (细节见 SC 实测记录 1): 用两套独立实现 (主控 `selfcheck_v9.py` 与本席 `qa_r8_check.py`, 抽取与判定代码均不同源) 分别构造 v9 的「正确落地」模拟文档, 各自跑下述三类反事实, 结果完全一致:

- (a) 把作废子句括号里的实质判定静默改回旧语义「即存在任一次不健康的调用」→ 两套实现均判 SC-9 转红 (缺「足以改变判定」)。
- (b) 删掉含 `classify_calls.py` 定义的那一行 → 两套实现均判 SC-9 转红 (缺「classify_calls.py + 两种可能」同行)。
- (c) 从作废条件里删掉「逐调用健康检查不通过」这一项 (本席按 owner 任务描述新增的第三类, 未见于 R7 原文, 已单独验证) → 两套实现均判 SC-9 转红。

三类反事实无一漏检。另加一项本席自选的分辨力探针: 把「两种可能」逐字改写为同义词「两种走向」(不改变语义, 只改变字面) → 仍判 SC-9 转红, 确认 v9 新增的两个锚点是逐字匹配、非语义理解, 与本 Spec 全篇「逐字」纪律一致, 不是可以被措辞同义替换绕过的软锚点。

closed / partially / open = **1 / 0 / 0**。

## Findings

(空。本轮未发现需要在 Findings 列出的 critical / major / 阻塞性 minor。)

## 观察

1. **R7 major 的两个新锚点是严格超集, 非真空**: v9 在保留 v8 原有锚点 (`≤ 5/10`、`连续 2 轮`、`fail 的后果`+`不得 ship` 同行、`作废`+`不得 ship` 同行、`classify_calls.py` 出现) 的基础上, 只新增「`classify_calls.py` 所在行须同时含「两种可能」」与「作废行须同时含「足以改变判定」」两个约束, 未删除或放宽任何旧约束。正确落地下十条适用 SC (SC-1/2/3/5/7/8/9/10/11/12) 用两套独立代码全部验证为绿, 说明新增锚点不是「正确文本也过不了」的恒红陷阱; 三类反事实 + 分辨力探针又证明它不是「怎么改都过」的恒绿陷阱。两端都不空。

2. **T2b / T4「搬」改「复制 (基线目录原件保留)」后, 全文零残留矛盾**: 对整份 proposal.md 逐字 grep「搬」, 0 命中——旧的「原样搬到」「搬入」字样已全部替换为「复制」+ 明确的「基线目录原件保留不动」限定语, 且 T2b/T4 各自的新句都反过来点名了它所服务的 SC (T2b 点 SC-13, T4 点 SC-4), 消除了 R7 major 第二条指出的「字面执行会删源文件、进而打断 SC-2/SC-4/SC-13」的自相矛盾。用真实文件系统核验 (非文本模拟): SC-2 前置表六行里除恰一行 `[配置推导]` 外, 其余反引号路径拼上基线目录后 `os.path.exists` 全部为真 (含第 3 行 `v6-per-call-health-opus5/claude-shim.sh`)——这条正是 R7 major 第二条点名的那一行, 现在两套独立实现都判定通过。

3. **`fault_matrix.py` 加固: 代码差异属实, 非仅 RESULT.md 叙述**: `git diff 15ab323 a563192 -- .../v6-per-call-health-opus5/fault_matrix.py` 显示旧版第 110-111 行确为无条件 `if out.exists(): shutil.rmtree(out)`, 新版替换为「非空则报错退出、否则 `mkdir(parents=True)`」的守卫, 与 R7 code-reviewer minor 所指、RESULT.md v8 的叙述完全对应 (不是只改了文档没改代码)。

4. **对加固后 `--out` 守卫的五类输入对抗测试** (真实调用仓库现存的 `v6-per-call-health-opus5/fault_matrix.py`, 非重新实现; 环境用一个只 `sys.exit(3)` 的 stub `run_eval.py` 让守卫之后的阶段快速终止, 不依赖真实 skill-creator 安装、不发真实 API 调用): 五类输入中**没有一类触发删除或覆盖别人东西的危险动作**——
   - 非空目录: 打印「输出目录已存在且非空, 请换一个 --out」, 退出码 2; 目录与其中的哨兵文件逐字节原样保留。这正是设计要防的场景 (`--out .` 类误用), 已验证生效。
   - 空目录: 视为「本来就没有东西可丢」, 正常继续执行 (在其中创建 `roots/logs/shimbin/…` 等子目录), 不算危险。
   - 不存在的深层路径: `mkdir(parents=True)` 建出整条链, 属预期的 `mkdir -p` 式便利行为, 新建路径, 无覆盖风险。
   - 指向一个文件 (非目录): `out.iterdir()` 抛 `NotADirectoryError`, 未被任何 `except` 捕获, 进程以未处理异常崩溃退出 (真实 traceback + 退出码 1)。**文件本身逐字节原样保留**, 不危险, 但也不是「报错退出」意义上的干净失败——是裸崩溃, 不打印面向使用者的错误信息, 退出码也不是非空目录分支用的 2。
   - 无写权限的空目录 (`chmod 555`): 列目录 (读+执行) 成功且为空, 通过非空检查后尝试在其中 `mkdir` 子目录时抛 `PermissionError`, 同样未被捕获, 裸崩溃退出码 1; 目录内容确认前后均为空, 无损坏。
   
   五类里唯一「只报错」的是非空目录 (设计针对的场景, 表现良好); 其余四类都不危险, 但「指向文件」与「无写权限目录」两类是**未处理异常的裸崩溃**而非清晰的错误提示——不满足任务要求的「哪些只是报错」里「报错」的完整意味 (有message、有可预测退出码)。这不构成 Finding: 它不会导致误删/误覆盖, 也不影响 SC-13 在正常路径 (全新或已存在的空 `--out`) 下「退出码 0 且末行报『与预期不符 0』」这一断言的可执行性——本席在同一份未改动的仓库脚本上另外单独重跑了一次全新的正确版 (真实 `SKILL_CREATOR_ROOT`, 非 stub), 24 用例、不符 0、退出码 0, 与 RESULT.md v8 记载一致。改进方向 (供 Phase B 或后续 cycle 参考, 非本轮阻塞项): 给 110-118 行的 `--out` 处理包一层 `try/except (NotADirectoryError, PermissionError)`, 统一输出与「非空目录」同风格的 stderr 提示并 `return 2`。

5. **独立复现 RESULT.md v8 关于「加固后重跑」的叙述**: 本席在自己的临时目录里 (未触碰 `v6-per-call-health-opus5/` 原目录) 用真实 `SKILL_CREATOR_ROOT` (本环境里默认硬编码路径 `bb335391eb83` 恰好仍可用, 与 R7 qa 席记录的「该 hash 已失效」不同——插件缓存内容会随环境变化, 不是 Spec 缺陷, D3/SC-13 已预置 `SKILL_CREATOR_ROOT` 覆盖条款作为应急) 重跑正确版故障矩阵: 24 用例、不符 0、退出码 0。另把三个工具文件复制到隔离目录并只删掉 `classify_calls.py` 里对报错结果帧的判定 (`if ev.get("is_error") or str(ev.get("subtype","")).startswith("error"): errored = True` 那两行), 重跑: 24 用例、不符 5、退出码 1, 不符的五个用例名 (`F1_result_error` / `S1_overbroad_fault_in_shouldnot_half` / `S2_correct_fault_on_one_should_query` / `S8_two_run_fault_should` / `S10_negctrl_two_run_fault_x6`) 与 RESULT.md v8、proposal.md SC-13、R7 qa 报告记录的**逐一相同**。RESULT.md v8「结论不变」的表述准确, 非未经验证的自我宣称。

6. **SC 范围外的存量缺口维持不变 (非本轮引入, 不重开)**: 「两套编号说明」实际只落在 SOT §4.1 (由 SC-3 锁定), 手册 4b 小节本身不含该字样; 「§固定测试集 vs 临时测试 表加 trigger 行」无 SC 直接检查是否真的加了该行。这两点是 R6/R7 已判定的非阻塞观察, v9 的四处改动未触及此区域, 现状不变, 仅在此复核确认未被四处改动波及。

## Verdict

PASS — 0 critical / 0 major / 0 minor (Findings 为空)。

## Vote

PASS

## SC 实测记录

**方法**: 临时目录 `/tmp/claude-1000/-home-dev-Aria/e91a9d6a-05ff-4b26-af79-8d903c21a292/scratchpad/r8-qa-engineer/`。`qa_r8_check.py` 独立于主控 `selfcheck_v9.py` 重写: 用 `re.search(..., re.S)` 抽取 D1 表格三行 / D2 body / D3 body / D4 (yaml + bullets) / D6 第三条 / SOT §3 边界注 (主控用 `txt.index()` 切片), 十条 SC 判定用显式 `for` 循环逐条收集失败原因 (主控用列表推导 + `all()`)。`adv_out_guard.py` 与两次独立 `fault_matrix.py` 实跑均为真实子进程调用真实脚本, 非文本模拟。

### 0. 前置事实 (未改动仓库)

```
git status --short: 仅另一席已落盘的 R8 报告 (code-reviewer.md, 未读取)
git rev-parse HEAD: a563192fc6848e914ca89e065c3db647d100c3cb
本轮全部验证基于临时目录 / 隔离副本 / 真实但一次性的 --out 目标, 结束时仓库 diff --stat 为空
```

### 1. R7 major 的三类反事实 (SC-9), 两套独立实现交叉验证

| 反事实 | 主控 `selfcheck_v9.py` | 本席 `qa_r8_check.py` | 一致 |
|---|---|---|---|
| (a) 作废括号实质判定改回旧语义「即存在任一次不健康的调用」 | SC-9 转红 | SC-9 转红 (原因: 作废行缺「足以改变判定」) | 是 |
| (b) 删掉含 `classify_calls.py` 的定义行 | SC-9 转红 | SC-9 转红 (原因: 缺「classify_calls.py + 两种可能」同行) | 是 |
| (c) 作废条件删掉「逐调用健康检查不通过」一项 | SC-9 转红 | SC-9 转红 (原因: 作废行缺「逐调用健康检查不通过」与「足以改变判定」) | 是 |
| 附加: 「两种可能」同义改写为「两种走向」 | 未测 (本席自选) | SC-9 转红 (逐字匹配, 非语义) | — |

正确落地 (未扰动) 下两套实现的十条适用 SC (SC-1/2/3/5/7/8/9/10/11/12) 结果:

```
主控 selfcheck_v9.py: SC-1..SC-12(适用的10条) 全 True, SC-11命中: []
本席 qa_r8_check.py:  {'SC-1': True, 'SC-2': True, 'SC-3': True, 'SC-5': True, 'SC-7': True,
                       'SC-8': True, 'SC-9': True, 'SC-10': True, 'SC-11': True, 'SC-12': True}
```

(SC-2 本席额外加了真实 `os.path.exists` 核验六行前置表路径, 非仅数字序列 1-6; SC-4/SC-6/SC-13 依赖真实 `ab-suite` diff / Forgejo issue / 真实工具执行, 按任务范围排除在纯文本模拟之外, 另在下方分别验证。)

### 2. SC-12「含新增 skill」漏写反事实

```
漏写「含新增 skill」(SOT 核心句行还原为 v8 旧文字) -> SC-12 = False
本席原因: SOT核心句行缺 含新增 skill
主控 selfcheck_v9.py 反事实 'q' 同一操作 -> SC-12 转红, 一致
```

### 3. SC-13 + `fault_matrix.py` 加固: 真实脚本真实重跑 (非文本模拟)

```
git diff 15ab323 a563192 -- .../v6-per-call-health-opus5/fault_matrix.py:
  确认旧版 110-111 行为 `if out.exists(): shutil.rmtree(out)` (无条件删除);
  新版替换为非空报错退出 / 空或不存在则继续 mkdir(parents=True), 与 RESULT.md v8 叙述一致。

本席独立重跑 (真实 SKILL_CREATOR_ROOT, 隔离 --out, 未碰 v6-per-call-health-opus5/ 原目录):
  正确版: 用例 24, 与预期不符 0, 退出码 0
  反事实 (隔离副本删掉 classify_calls.py 对报错结果帧的判定): 用例 24, 与预期不符 5, 退出码 1
    不符用例名: F1_result_error / S1_overbroad_fault_in_shouldnot_half /
                S2_correct_fault_on_one_should_query / S8_two_run_fault_should /
                S10_negctrl_two_run_fault_x6
  —— 与 RESULT.md v8、proposal.md SC-13、R7 qa 报告记录的结果逐一相同
```

### 4. `--out` 守卫五类输入对抗测试 (真实调用, stub `run_eval.py` 只做 `sys.exit(3)` 以便守卫之后快速终止)

| 输入 | 退出码 | 是否危险 (删除/覆盖别人的东西) | 备注 |
|---|---|---|---|
| 非空目录 (含哨兵文件) | 2 | 否 | 打印「已存在且非空, 请换一个 --out」; 哨兵文件逐字节原样保留 |
| 空目录 | (继续执行, 后段因 stub 而失败) | 否 | 目录本就空, 无数据可损; 55 个子项被正常创建 |
| 不存在的深层路径 | (继续执行, 后段因 stub 而失败) | 否 | `mkdir(parents=True)` 建出整条链, 新建路径无覆盖风险 |
| 指向一个文件 | 1 (未捕获异常) | 否 (但裸崩溃) | `NotADirectoryError`; 文件内容前后逐字节相同 |
| 无写权限的空目录 (`chmod 555`) | 1 (未捕获异常) | 否 (但裸崩溃) | `PermissionError`; 目录前后均确认为空 |

五类输入无一触发危险动作; 「指向文件」与「无写权限目录」两类以未处理异常裸崩溃收尾 (非清晰报错), 判非阻塞观察 (见观察 4), 不列 Findings。

### 5. 落盘脚本 (仅供复核, 均在 `/tmp/claude-1000/-home-dev-Aria/e91a9d6a-05ff-4b26-af79-8d903c21a292/scratchpad/r8-qa-engineer/`)

`qa_r8_check.py`(独立抽取+十条SC判定+三类必测反事实+SC-12反事实+分辨力探针) / `adv_out_guard.py`(五类--out对抗测试) /
`stub_sc/`(守卫测试用的哑 SKILL_CREATOR_ROOT) / `outguard/`(五类场景的临时目录, 每场景前置 reset) /
`tools-cf/`(SC-13反事实用的四文件隔离副本, 已对 classify_calls.py 做最小反事实编辑) /
`fm-real/正确版`、`fm-real/反事实版2`(两次真实故障矩阵重跑的完整产物与日志) / `run_full.json`(五类对抗测试完整结果)。

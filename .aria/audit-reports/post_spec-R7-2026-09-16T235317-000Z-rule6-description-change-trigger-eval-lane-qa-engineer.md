---
checkpoint: post_spec
mode: convergence
rounds: 7
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-17T00:21:23.000Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [qa-engineer]
---

# post_spec Round 7 — qa-engineer 席

> 被审 SHA `15ab323` (v8)。方法: 全程只读仓库, 未编辑任何仓库内文件 (`git status --short` 复核确认, 见 SC 实测记录 4)。**未读**本轮其他席的 R7 报告 (审计报告目录内已见 `code-reviewer` / `tech-lead` 两份落盘, 遵照独立性要求未打开)。临时文件全部落 `/tmp/claude-1000/-home-dev-Aria/e91a9d6a-05ff-4b26-af79-8d903c21a292/scratchpad/r7-qa-engineer/`。
>
> 复用说明: 该目录下存有本席一次更早 (2026-09-15 21 时许) 因用量重置而中断的 R7 尝试留下的 `build_v8.py` / `sc_check.py` (独立于主控 `selfcheck_v8.py` 的另一套切片/判定实现)。已逐一核对该次遗留的 `proposal_v8.md` / `CLAUDE.md.orig` / `SOT.md.orig` / `HB.md.orig` 四份快照与当前仓库现状**逐字节相同**后确认可续用, 未凭空信任, 本轮据此重跑并扩展 (新增 `perturb_v8.py`、`adversarial_fixtures.py`、SC-13 的工具目录实跑)。

## R6 对账

本席 R6 报告 0 Findings (verdict PASS, vote PASS), 故**无 R6 条目**可供逐条 closed/partially/open 判定。

R6 观察第 3、4 条在 v8 下的现状:
- **观察 3** (8 项"探索性反事实未被任何 SC 覆盖但判非阻塞"的内容, 均落在 v7 的 D2「同批参照臂」及邻近说明性文字): v8 把 D2 的核心机制从「同批参照臂」**整体替换**为「逐调用健康检查」(非增量修补, 回应 R6 major #2 与 owner"先做实验再重新设计"的裁定), 原第 1 项(「同批参照臂」整段定义 bullet)对应的文字已不存在, 该项随机制替换而**消解**(moot), 不再适用。其余各项("只承诺已验证的两类破坏"整段 / "套件"整段 / SOT §4.1 两条不合规条款 / "(未穷举)"括注 / 4a 标题冗余)对应的文字在 v8 中原样保留 (仅 RESULT 版本号 v6→v7 字样同步), 仍无专属 SC, 仍与此前判定一致——具体理由(SOT/HB 侧存在冗余复述, 或属纯限局 hedge 措辞)不因文字挪位而改变。
- **观察 4** (T2「§固定测试集 vs 临时测试 表加 trigger 行」缺 SC 覆盖): 该句在 v7→v8 diff 中逐字未变 (`grep` 核对, 仅同一行), 仍无对应 SC, 判断维持"非阻塞"不变。

## Findings

- [major] testing/proposal.md §D2+SC-9 (逐调用健康检查「作废」子句的语义锚点) (issue): SC-9 只锚定标签词「逐调用健康检查不通过」, 不锚定实质判定语句「即不健康的调用足以改变判定」; 已实测把该子句静默改写为已被 v6a 实验数据否定的「即存在任一次不健康的调用」(旧规则语义, 仅改括号内从句、保留外层标签), 12 条 SC (SC-1/2/3/5/7/8/9/10/11/12) 全部保持绿、无一转红。`classify_calls.py` 代码本身仍按 v6b 区间逻辑正确执行 (已用 24 用例故障矩阵复核, 见 SC 实测记录 3), 不是运行时安全漏洞, 但手册 prose 一旦被后续编辑悄然改回实验已否定的旧规则, 现有 12 条 SC 无一能感知, 削弱了 `PREREGISTRATION-AMENDMENT.md` + `prereg-amendment.lock` 原本要提供的"防止事后悄悄改回方便结论"的机械防线。

## 观察

**1. 主控自检脚本 (`selfcheck_v8.py`) 忠实性复核结论**: 逐点核对其构造假设与仓库现状的位置吻合度——SOT 侧「## 3.」结尾紧接「## 4. 与规则 #10 的关系」(第 47 行)、「## 4.」内容结尾紧接「## 5. 已裁定的样例」(第 57 行)、「后者另有两个已知缺陷记录在案:」(第 71 行) 与「详见 aria-plugin issue #116。」(第 76 行) 之间恰为两条既有 bullet、版本行 `> **Version**: 1.0.0` 全文恰 1 次; HB 侧「### 场景 4: Description 触发准确率优化」(第 263 行) 到「---\n\n## 执行细节」(第 276-278 行) 之间不含其他 `###`/`##` 标题、「边界与留痕」段首行 (第 480 行) 含「边界三条」恰 1 次——全部经真实文件 `grep -n`/逐行核对确认, 未发现锚点假设与 v8 转录范围有出入。进一步用**独立于主控代码**的第二套实现 (`build_v8.py`+`sc_check.py`: 逐行扫描的 `slice_section` 取代主控的 `txt.index()` 式 `section()`, 10 条 SC 判定函数逐条重写不誊抄) 独立复现, 两套脚本在"正确落地全绿"与全部 15 项 (主控 a-o) + 本席 T1-T6(6 大类, 其中混入编号一项拆 OQ/D/T/SC/Why 5 变体共 10 项) 反事实上**结论完全一致**, 双实现收敛, 不构成单一信息源风险。

**2. 任务指定 6 类必测反事实**: 全部由两套独立脚本一致捕获, 无遗漏、无过度触发——删逐调用健康检查定义行(`classify_calls.py`那一行)→SC-9; 作废条件删掉逐调用一项→SC-9; 禁令写回「不提交任何改动」→SC-12; 删 SOT 自主条款(整段)→SC-12; 删前置表第 3 行→SC-2; 手册 4b 混入内部编号(OQ/D/T/SC/Why 五变体全测)→SC-11。过程中发现并修正了本席自己一处反事实的取点 bug (前置表第 4 行「[配置推导]」标记在 HB 全文出现 2 次——D3 说明句与表格第 4 行各一次, 全局 `replace(...,1)` 误删了说明句里那次; 改成按行精确定位后, SC-2 正确转红), 记录在此供留痕, 不构成 SC 缺陷。

**3. SC-13 实测 (工具文件搬迁 + 故障矩阵复现)**: 把 `v6-per-call-health-opus5/` 下 `claude-shim.sh`/`classify_calls.py`/`fake-claude`/`fault_matrix.py` 拷到独立临时目录 `tools/trigger-eval/`, `cmp` 四个文件逐字节相同 (无输出)。正确版跑 `fault_matrix.py`: 用例 24, 与预期不符 0, 退出码 0。按 proposal 记录的反事实复现——删掉 `classify_calls.py` 里对报错结果帧 (`is_error`/`subtype`) 的判定——重跑: 用例 24, 与预期不符 5 (`F1_result_error`/`S1`/`S2`/`S8`/`S10`), 退出码 1, 与 proposal 所记"2026-09-15 已实跑"的结果**完全吻合**。过程中 `fault_matrix.py` 硬编码的默认 skill-creator 插件缓存路径 (`.../skill-creator/bb335391eb83/skills/skill-creator`) 已不存在 (该 hash 目录下只剩空的 `agents`/`assets`, 无 `skills/` 子目录), 需显式设 `SKILL_CREATOR_ROOT` 指向当前实际路径 (`.../skill-creator/unknown/skills/skill-creator`) 才能跑通——这正是 SC-13 与 D3 前置表已写明的应急条款("插件缓存路径变了就设 `SKILL_CREATOR_ROOT`") 的真实命中, 不是缺陷, 反而实证了该条款的必要性 (基线记录于 2026-09-15, 仅两天后即需要它)。提醒: 未来执行 T2b 的人大概率同样需要这一步。

**4. 对 `classify_calls.py` 的对抗测试**: 手工构造 13 组 `<id>.jsonl`/`<id>.query` 夹具 + 合成 `run_eval` 输出 json, 全部走真实 `subprocess` 调用 `classify_calls.py` CLI (不 import 内部函数抄近道)。覆盖: 重复 query 文本导致两条 `results` 条目在 `by_query` dict 里坍缩为一条 (验证失败安全: 实测 `mismatch=1 → void`, 未静默吞掉重复条目产生错误 pass/fail); 耗时恰好落在 `timeout - TIMEOUT_MARGIN_S` 边界本身 (119.0s, 应判超阈值) 与差 1 纳秒 (应判健康) 两侧, 均无浮点意外; 只缺垫片 `start` 记录 / 只缺 `end` 记录 (分别测, 均正确判不健康, 代码用 `or` 非 `and`); 负控 `hits_max` 恰为 5 (应 valid) 与恰为 6 (应 void) 的真实多 query 构造 (非抽象推演); `runs` 不等的两个方向 (日志数多于/少于声明值, 均正确判 mismatch); query 文本完全对不上任何 `results` 条目 (正确判 unmapped); 非 JSON 行/空行与正常帧混排 (不崩溃, 正确跳过); 完全空文件; 判定事件 (`tool_use_start`) 已出现之后 `result` 帧才报错 (确认只是保守偏向 void, 未产生错误的 pass/fail, `pass_worst=False`/`pass_best=True` 计算正确)。**13 项全部符合预期或安全 fail-closed, 未在这些方向发现可利用 bug**。另检查了 `fake-claude` 源码 (本项目自身唯一的故障注入器): 其 `result_error` 故障模式产生的是 `subtype="success"` + `is_error=True` 这一种"看似成功、实则报错"的解耦组合, 被 `is_error` 字段单独正确捕获; 反向的解耦 (`is_error` 为假但 `subtype` 打头非 "error") 在真实 Claude Code CLI 的已知 subtype 枚举 (`success`/`error_max_turns`/`error_during_execution`, 均以 "error" 开头) 与本项目 `fake-claude` 里均不产生——判**不可达**, 不列 Finding (对应任务第 3 项要求的"逐条说明是否可达"结论)。

**5. 一处窄口径反事实的边界说明**: 独立补测了「把 `classify_calls.py` 定义句里的文件名引用替换掉、但在小节末尾另加一句不相关的 `classify_calls.py` 提及」——SC-9 的 `含 classify_calls.py 的行 ≥ 1` 检查仍判绿 (字面上确实还有一行含该串)。这与 Findings 里的major 同根 (SC-9 是子串/标签匹配, 不校验语境), 但**单独**作为 finding 的理由不足: 需要编辑者刻意"保留一处无关字面提及、同时抽走真正定义句"这种不自然的编辑动作, 现实改稿 (整段誊抄或改写) 不会自然产生, 故归入观察而非 Findings, 仅作为同一根因的补充证据留痕。

**6. SC 范围外的两个 T2 子项现状不变**: 「两套编号说明」按 T2 字面要求应体现在手册 4b 小节, 但无论主控还是本席独立构造, 落地后 HB 内均**不含**「两套编号」字样 (该说明实际只落在 D4→SOT §4.1, 由 SC-3 单独锁定); 「§固定测试集 vs 临时测试 表加 trigger 行」同样没有任何 SC 检查真的加了该行。两者与 R6 观察 4 同类——文档完整性的轻量缺口, 有旁证冗余或范围外证据兜底 (SC-4 直查真实文件是否升版), 不满足"不改就不能进 Phase B"的门槛, 判非阻塞。

## Verdict

PASS_WITH_WARNINGS — 0 critical / 1 major / 0 minor。

## Vote

REVISE

## SC 实测记录

**方法**: 临时目录 `/tmp/claude-1000/-home-dev-Aria/e91a9d6a-05ff-4b26-af79-8d903c21a292/scratchpad/r7-qa-engineer/`。`build_v8.py` 独立从 `proposal_v8.md` (已核对与仓库现状 v8 逐字节相同) 提取 D1 三行 / D2 / D3 / D4(yaml+3 bullet, 断言不含 `OQ-7`/「无机械 enforcement」/「authoring 路径与过渡期」) / D6 第三条 / SOT 边界注, 每处带独立断言, 构造三份"正确落地"模拟文档 (`state.pkl`)。`sc_check.py` 用逐行扫描的 `slice_section` (不复用主控 `section()` 的 `index()` 实现) 独立重写 SC-1/2/3/5/7/8/9/10/11/12 十条判定, 各带失败原因回显。`perturb_v8.py` 做任务指定 6 类反事实 (混入编号拆 5 变体) + 5 项自选探索性反事实。`adversarial_fixtures.py` 手工构造 13 组日志夹具对抗测试 `classify_calls.py`。全部脚本只读仓库/写 scratchpad, 复核 `git status --short` 确认仓库无改动。

### 0. 正确落地 → 独立实现与主控脚本结论一致, 10 条 SC 全绿

```
主控 selfcheck_v8.py: SC-1..SC-12(适用的10条) 全 True, SC-11命中: []
本席 sc_check.py:     SC-1: PASS  SC-2: PASS  SC-3: PASS  SC-5: PASS  SC-7: PASS
                      SC-8: PASS  SC-9: PASS  SC-10: PASS SC-11: PASS SC-12: PASS  全绿: True
```
(SC-2 前置表六行的机读实证反引号路径, 已用 `os.path.exists` 对基线目录逐条核验存在; SC-4/SC-6 依赖真实 `ab-suite` diff 与 Forgejo issue 存在性, 按任务给定范围排除, 未纳入纯文本落地模拟。)

### 1. 任务指定 6 类反事实 (本席独立脚本 `perturb_v8.py`, 与主控脚本交叉验证一致)

| # | 操作 | 目标 SC | 结果 | 判读 |
|---|---|---|---|---|
| 1 | 删逐调用健康检查定义行 (`classify_calls.py` 那一行) | SC-9 | **翻红** (缺该行) | 符合预期 |
| 2 | 作废条件删掉「逐调用健康检查不通过」一项 | SC-9 | **翻红** (作废行缺该词) | 符合预期 |
| 3 | 禁令退化为「不提交任何改动」 | SC-12 | **翻红** (缺"撤销本任务已做的全部改动") | 符合预期 |
| 4 | 删 SOT 自主运行时整段条款 | SC-12 | **翻红** (缺 5 项子串) | 符合预期 |
| 5 | 删前置表第 3 行 (claude 垫片) | SC-2 | **翻红** (行号序列缺 3) | 符合预期 |
| 6a-e | 手册 4b 混入内部编号 (OQ/D/T/SC/Why 第 五变体各测) | SC-11 | **全部翻红** (分别命中 OQ-7/D2/T4/SC-9/Why 第) | 符合预期, 五变体无一漏检 |

### 2. 自选探索性反事实 (5 项, `perturb_v8.py` A-E)

| # | 操作 | 结果 | 判读 |
|---|---|---|---|
| A | 作废行保留"逐调用健康检查不通过"字面, 但把括号内 void 语义解释换成模糊词「(有问题)」 | 未转红 (预期内, 不列 finding) | SC-9 本就只查字面 token, 非语义; 本项只是确认边界, 真正的语义锚点缺失见下方第 C 项与 Findings |
| B | 「连续 2 轮」改写为中文数字「连续两轮」 | SC-9 **翻红** | 对阿拉伯数字字面零容忍, 符合"逐字"落地设计意图 |
| C | 定义句里的 `classify_calls.py` 文件名引用移除, 同时在小节末尾插入一句不相关的 `classify_calls.py` 提及 | **未翻红** | 见观察 5, 判非阻塞 (需要不自然的编辑动作才可能触发) |
| D | 前置表第 4 行删掉「[配置推导]」标记 (精确定位表格行, 排除 D3 说明句里的同名字面) | SC-2 **翻红** (config_derived_rows=0) | 首次尝试因全局 `replace(...,1)` 误中说明句而漏检, 修正定位方式后正确转红, 非 SC-2 缺陷 |
| E | 「unattended == true」大小写改为「unattended == True」 | SC-12 **翻红** | 对大小写字面零容忍 |

### 3. SC-9 语义锚点缺口的确证实验 (对应 Findings, 独立于上述反事实脚本单独验证)

```
把 v8 落地文档里 "(检查结论为 void, 即不健康的调用足以改变判定; 或检查脚本无法判定)"
精确替换为 v6a 旧语义 "(检查结论为 void, 即存在任一次不健康的调用; 或检查脚本无法判定)"
(仅改括号内从句, 外层"逐调用健康检查不通过"标签字面不变) →
run_all() 结果: 12 条 SC 转红列表 = [] (全部保持绿)
```
proposal.md 全文核对: 「足以改变判定」这一决定性短语仅出现 1 次 (即被替换的这一处), 未被任何 `SC-\d+:` 判据文本字面引用。

### 4. SC-13: 工具文件搬迁 + 故障矩阵复现 (独立临时目录, 非原地复用基线目录)

```
cmp 四文件 (claude-shim.sh / classify_calls.py / fake-claude / fault_matrix.py):
  与 v6-per-call-health-opus5/ 逐字节相同, 无输出

正确版: 用例 24, 与预期不符 0, 退出码 0
反事实 (删 classify_calls.py 对报错结果帧的判定): 用例 24, 与预期不符 5
  (F1_result_error / S1_overbroad_fault_in_shouldnot_half /
   S2_correct_fault_on_one_should_query / S8_two_run_fault_should /
   S10_negctrl_two_run_fault_x6), 退出码 1
—— 与 proposal.md SC-13 记录的 "2026-09-15 已实跑" 结果完全吻合
```
需设 `SKILL_CREATOR_ROOT=/home/dev/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/skill-creator` (硬编码默认路径 `bb335391eb83` 已随插件缓存更新失效), 属 SC-13/D3 已预置的应急条款命中, 非缺陷。

### 5. 对 classify_calls.py 的对抗测试 (`adversarial_fixtures.py`, 13 组手工日志夹具)

```
共 13 项对抗测试, 判定与预期不符 (可能是可达bug): 0
```
覆盖重复query坍缩(失败安全)/耗时边界(119.0s 与减1ns)/仅缺start或仅缺end/负控hits_max恰5恰6(真实多query构造)/
runs不等两方向/query对不上/非JSON行与空文件混排/判定事件后才报错(确认仅保守未致错判)。
另核查 `fake-claude` 源码确认 is_error/subtype 解耦的唯一真实形态 (`subtype=success`+`is_error=True`) 已被 `or` 逻辑正确捕获,
反向解耦形态在真实 Claude CLI contract 与本项目 fake-claude 均不可达。

### 6. 前置事实 (未改动仓库)

```
git status --short: 仅另两席已落盘的 R7 报告 (code-reviewer.md / tech-lead.md, 未读取)
grep -crF "只验证触发面没被改坏" CLAUDE.md / SOT / HB 三份文件: 均为 0 (本 Spec 仍是 Draft, 三处改前原句)
本轮反事实与对抗测试全部基于临时目录模拟/独立文件, 未改动仓库任何文件
```

### 7. 落盘脚本 (仅供复核, 均在 `/tmp/claude-1000/-home-dev-Aria/e91a9d6a-05ff-4b26-af79-8d903c21a292/scratchpad/r7-qa-engineer/`)

`build_v8.py`(独立提取+构造) / `sc_check.py`(独立10条SC实现) / `perturb_v8.py`(6类必测+5类自选反事实) /
`adversarial_fixtures.py`(13组对抗日志夹具) / `tools/trigger-eval/`(SC-13搬迁副本) /
`tools-trigger-eval-cf/`(SC-13反事实副本) / `fm-正确/`、`fm-反事实/`(故障矩阵输出) / `adversarial/`(13组夹具输出) /
中间产物 `state.pkl`。

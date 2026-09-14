---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-14T14:45:00.000Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [qa-engineer]
---

# post_spec Round 5 — qa-engineer 席

> 被审 SHA `f169a0b` (rework v5, `max_rounds = 5` 最后一轮)。方法与 R4 一致: 全部从 proposal.md 逐字切片提取 (非手抄), 在临时目录重建「正确落地」模拟副本, 对 v4→v5 的每处实质改动单点扰动 (反事实), 检查目标 SC 是否翻转、是否牵连其余 SC、以及是否存在「改了内容却没有任何 SC 能锁住它」的缺口。全程只读仓库, 未编辑任何仓库内文件; 临时文件全部落 `/tmp/claude-1000/-home-dev-Aria/e91a9d6a-05ff-4b26-af79-8d903c21a292/scratchpad/r5-qa/` (复用 r4-qa 的方法与部分产物)。

## R4 对账

无。本席 R4 报告为 0 critical / 0 major / 0 minor (PASS), 无遗留条目需要对账。

## Findings

- [major] testing/proposal.md §D1(SOT §2 自主模式条款) (issue): v5 新增的 SOT §2「自主运行时 (`state_scanner.coordination.unattended == true`) ... 需要改时任务进 S_FAIL」整句 (R4 major #2 的核心补丁) 若被删除/回归, 现有 7 条 SC (1/2/3/5/7/9/10) 仍全部判绿 (已反事实验证, 见下 CF-e); 该句是本轮唯一实现「验证前遇到 description 改动怎么办」的条款, 却无任何机械检查锁定, 可静默丢失不被察觉。建议补一条窄 SC 锁 `state_scanner.coordination.unattended` 或 `S_FAIL` 字面存在于 SOT。
- [minor] testing/proposal.md §D1(SOT §3 边界注) (issue): §3 边界注新句「走 §2 第二行: 照跑场景 1, 另须跑场景 4b」若写回 v3/v4 旧形「走 §2 第二行的场景 4b 义务」, SC-10 的 `description hunk 不走本节` 子串检查两种写法都命中 = 1, 7 条 SC 仍全绿 (已反事实验证, 见下 CF-d)。建议 SC-10 或新增 SC 顺带锁「另须跑场景 4b」这几个字, 与 SC-1 对三处主落点的处理一致。

## 观察

- **v3 旧新句落地明细** (支撑 Finding 之外的反事实 CF-a, 非阻塞, 纯记录): CLAUDE 落地行含「照跑场景 1」但缺「另须跑场景 4b」(v3 写的是「一律跑场景 4b」); SOT 落地行含「照跑场景 1」但同样缺「另须跑场景 4b」(v3 写「hunk ⇒ 场景 4b 地板守卫」); 手册落地行两者皆缺 (v3 写「零裁量跑场景 1」/「零裁量跑场景 4b 地板守卫」, 无「照跑场景 1」四字连续出现)。三处至少各缺一项, SC-1 正确判红, 与 R4 rework 计划所述「已对 v3 实证: v3 红」一致, 本席独立复算结果相同, 不构成新发现。
- **D2 作废第二情形 (`run_eval.py` 自身没跑成功) 同样无 SC 单独锁定**: SC-9 只要求「作废」与「不得 ship」同行即判绿, 该行本身仍完整存在时 (即使被截断到只剩第一分支「负控 ≥ 6/10」) SC-9 不会转红。这与 Finding 同属「新增内容没配 SC」范畴, 但严重性更低 (第二分支是 R4 聚合报告点名的「观察顺手补」项, 从未被判为需要独立验证), 且真正阻塞发生的前提 (run_eval.py 跑崩) 本身概率低、有其他信号 (报错退出码) 会先暴露, 故判非阻塞, 不进 Findings。
- **D4 §4.1 合规清单新增「或 `scenario1`」分句**: SC-3 只做字段名 `scenario1` 计数 ≥ 1 的存在性检查 (v5 正确落地下计数从 v4 的 2 次增至 3 次, 因为多了这句引用), 不专门验证这句「合规判断」文字本身是否完整。与 D2 四短语枚举同属「文档准确性修正而非可执行判据」性质 (R4 对这类修正一贯只记 minor/观察, 未要求配 SC), 不认为需要新增 SC。
- **D6 第三条局限更新** (「已验证判红的破坏类型是...两类 (未穷举)」+ GLM 未验证句) 同样无 SC 锁定 (反事实 CF-f 验证: 删除 GLM 句后 7 条 SC 仍全绿)。但这是纯限局文档陈述, 不影响执行者行为; 已用 `grep -n` 核对 RESULT.md v5 (文件版本头 + 结论 1 + §v5 表格第 55/67 行) 与 proposal D2/D6 的四短语枚举、「未穷举」措辞逐字一致, 内容本身无误。判非阻塞。
- **OQ-7 事实依据独立核验 (逐条查证, 结果: 均属实, 未发现不可证伪或事实不成立)**: (1) AD5「任意状态都可进入 S_FAIL」—— `aria-orchestrator/docs/architecture-decisions.md:450` 逐字命中; (2) AD10 回滚路径 Level 2「在 S5_REVIEWING 中间插入一个 optional human gate (只对高风险 issue 触发)」—— 同文件 `:809-812` 逐字命中 proposal 引号内文字; (3) aria-runner 镜像 Dockerfile 只 `COPY aria/`, 未装 skill-creator —— 核对 `aria-orchestrator/docker/aria-runner/Dockerfile` 属实; (4) 「aria-runner-bot 是 AI 会话共用的机器提交身份」—— `standards/conventions/session-handoff.md` §2.3.9 与其引用的 handoff 原文 (`docs/handoff/2026-07-27-issue122-phase-a-dual-gate-convergence.md:72`「本容器内任何 session 都会被标为 bot 身份, 无论谁在驱动」) 逐字支持, 且比 proposal 引用的证据更直接; (5) v1.64.0 / v1.70.0 两份 release handoff 的 frontmatter 确实分别是 `owner-container: aria-runner-bot/023236f2` 与 `owner-container: aria-runner-bot/bfe8285d`, 与「两个开发容器」框架一致; (6) `10CG/Aria#196` 经 `forgejo GET` 核实存在, 标题「unattended 的 Layer 1→2 env 传递三腿契约未定义 — 缺 import 会静默 fallback 到 false」与引用逐字吻合; (7) `state_scanner.coordination.unattended` 键与「配置事实, 不得运行期推断」的措辞在 `aria/skills/phase-a-planner/SKILL.md:129` 确有同款既有约定。**唯一未能独立复核到位的**: 具体计数「023236f2 23 份 / bfe8285d 7 份」, 本席用 `grep -rl` 在 `docs/handoff/*.md` 粗测得到 42 / 23 (文件数口径), 与 proposal 数字不同; 抽查发现差异大概率来自计数口径不同 (proposal 可能按「aria-runner-bot 提交且与该容器配对」逐 commit/逐条目计数, 本席按「文件内同时出现两个字符串」计数, 后者会把该容器在同一 handoff 文件里因其他原因被提及的情形也计入), 抽查的 8 个「文件含 aria-runner-bot 但不含任一容器 ID」的反例逐一核对后均属「PAT/凭据管理语境下提及同名机器人」而非「commit 归属该容器」, 不构成对原声明的反证。此差异不判定为错误, 但建议 proposal 若要保留这两个具体数字, 附上产生它们的命令或脚本, 以便后续复核不必逐个重新定义口径。
- **命名旁支 (不计入 Findings, 因非本 Spec 改动范围)**: OQ-7(E) 引用的状态名「S7_AWAITING_MERGE」是 AD10 自身原文用词, 但 `architecture-decisions.md` 其余处 (AD5、AD-M2-5、§3127/3154 等) 通篇用「S7_HUMAN_GATE」。这是 aria-orchestrator 文档自身既有的命名不一致, 早于本 Spec 存在, 本 Spec 只是如实转述 AD10 原文, 不属于 v5 新引入的问题, 也不在本 Spec 的代码落点范围内, 故不计入 Findings。

## Verdict

PASS_WITH_WARNINGS — 0 critical / 1 major / 1 minor。

## Vote

REVISE

## SC 实测记录

**方法**: 临时目录 `/tmp/claude-1000/-home-dev-Aria/e91a9d6a-05ff-4b26-af79-8d903c21a292/scratchpad/r5-qa/`。`build_v5.py` 从当前 proposal.md (v5, HEAD `f169a0b`) 逐字提取 D1 三行新句、§3 边界注引号内文字、D2/D3/D4/D6 整段全文 (D6 第三条 bullet 同样用正则从「追加第三条: 「...」」中原样切片, 不手打, 较 R4 的 `build.py` 进一步降低转录风险), 落地 `CLAUDE.correct.v5.md` / `skill-benchmark-exemption.correct.v5.md` / `AB_TEST_OPERATIONS.correct.v5.md` 三份「正确落地」模拟副本。`sc_checks_v5.py` 按 v5 字面重写 SC-1 (核心句所在行须同时含「照跑场景 1」与「另须跑场景 4b」) 与 SC-9 (拆「fail」/「不得 ship」同行与「作废」/「不得 ship」同行两个独立子判定), SC-2/3/5/7/10 逻辑与 R4 相同 (v5 未改动这几条的判据文字或影响其判据的正文结构)。`perturb_v5.py` 做本轮指定的 4 项反事实 (a)-(d) + 追加 2 项 (e)(f)。

### 0. 正确落地 → SC-1/2/3/5/7/9/10 基线全绿

```
PASS SC-1  {'CLAUDE': 1, 'CLAUDE_line_has_s1': True, 'CLAUDE_line_has_s4b': True,
            'SOT': 1, 'SOT_line_has_s1': True, 'SOT_line_has_s4b': True,
            'HB': 1, 'HB_line_has_s1': True, 'HB_line_has_s4b': True}
PASS SC-2  {'n_rows': 6, 'config_derive_rows': 1}
PASS SC-3  {'decision_table_row': 2, 'description_changed': 2, 'scenario1': 3, 'scenario4b': 5, 'negctrl': 1}
PASS SC-5  {'body_hits': [], 'has_exclusion_phrase': True, 'landing_detail': {'CLAUDE': 0, 'SOT': 0, 'HB': 0}}
PASS SC-7  {'三个已知缺陷': 1, '两个已知缺陷': 0, 'version_1_1_0': 1, '边界四条': 1, '边界三条': 0}
PASS SC-9  {'le_5_10': 1, 'continuous_2': 1, 'fail_line_ok': True, 'void_line_ok': True}
PASS SC-10 {'missing_in_param_line': [], 'sot_boundary_note_count_ok': True}
```

(SC-3 的 `scenario1` 计数由 R4 正确落地的 2 次升为 v5 的 3 次, 来自 D4 新增合规句「而 `scenario1` 或 `scenario4b` 为空」, 属预期变化, 非缺陷。)

### 1. 任务指定反事实 (a)-(d)

| # | 操作 | 目标 SC | 结果 | 判读 |
|---|---|---|---|---|
| (a) | CLAUDE/SOT/手册三处新句换成 v3 (`0c41e53`) 的旧新句 (而非 v5 新句) | SC-1 | **翻红**: `{'CLAUDE_line_has_s4b': False, 'SOT_line_has_s4b': False, 'HB_line_has_s1': False, 'HB_line_has_s4b': False}` | 符合预期 (三处至少各缺一项字面), 与 R4 rework 计划「已对 v3 实证: v3 红」一致 |
| (b) | 只删「- **fail 的后果**: ...」整行 (正则按行删除, 未触碰「作废」行) | SC-9 | **翻红**: `fail_line_ok: True→False`, 其余 (`le_5_10`/`continuous_2`/`void_line_ok`) 不变; 连带检查 SC-1/2/5/7/10 全部仍 True (无牵连) | 符合预期 |
| (c) | 只删「- **作废**只在两种情形发生: ...」整行 (正则按行删除, 未触碰「fail 的后果」行) | SC-9 | **翻红**: `void_line_ok: True→False` 且 `continuous_2: 1→0` (「连续 2 轮」子句与「作废」定义同在这一行, 删行必然一并丢失, 非交叉误判); 连带检查 SC-1/2/5/7/10 全部仍 True | 符合预期 |
| (d) | SOT §3 边界注新句写回旧形「走 §2 第二行的场景 4b 义务」| 全部 7 条 SC | **全部仍为 True** | **确认缺口** (计入 Findings minor 项): `不走本节` 子串在新旧两种写法下都命中, 无 SC 能感知这处内容回退 |

### 2. 追加反事实 (排查「v5 新引入内容有没有配 SC」, 非任务强制项但属「新引入问题排查」的直接延伸)

| # | 操作 | 结果 |
|---|---|---|
| (e) | 只删 SOT §2「自主运行时 (`state_scanner.coordination.unattended == true`) ... 裁定不同则随之改)。」整句, 同行的核心句/「照跑场景 1」/「另须跑场景 4b」原样保留 | 全部 7 条 SC 仍为 True → **确认缺口** (计入 Findings major 项) |
| (f) | 只删 SOT §6 第三条局限里「场景 4b 只在 Claude 模型上实测过...GLM 未验证。」这句, 其余不动 | 全部 7 条 SC 仍为 True → 缺口存在但判非阻塞 (见「观察」, 纯文档陈述不影响执行者行为) |

### 3. 前置事实

```
CLAUDE.md / SOT / 手册 现状仍是改前原句 (grep -c "只验证触发面没被改坏" 三份文件均为 0),
与 R4 报告一致: 本 Spec 仍是 Draft, 尚未执行落地任务, 本轮反事实全部基于临时副本模拟。
```

### 4. 落盘脚本 (仅供复核, 未改动仓库)

`build_v5.py` / `sc_checks_v5.py` / `perturb_v5.py`, 均在 `/tmp/claude-1000/-home-dev-Aria/e91a9d6a-05ff-4b26-af79-8d903c21a292/scratchpad/r5-qa/`; 反事实中间产物 `CF_a_*.md` / `CF_b_HB.md` / `CF_c_HB.md` / `CF_d_SOT.md` / `CF_e_SOT.md` / `CF_f_SOT.md` 同目录。R4 的 `v4_to_v5_proposal.diff` / `v3_to_v5_proposal.diff` (本轮生成, 同目录) 用于定位逐处改动锚点。

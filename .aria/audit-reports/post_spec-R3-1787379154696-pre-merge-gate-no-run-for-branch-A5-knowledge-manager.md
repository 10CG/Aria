---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-22T12:15:00.000Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A5-knowledge-manager
critical_count: 0
major_count: 2
minor_count: 1
---

## 摘要

R3 对 v3 (R2-fix + 设计收缩) 做知识管理透镜复核。方法: 全部结论基于实读 `aria @ 400f0bc` 源码 (`pre-merge-gate-empirical-traps.md` 全文 / `runtime_probe.py` + `coordination_probe.py` + `runtime-probe-declaration.md` 全文 / `task-planner/SKILL.md` 双数据源路径) · 实读 `docs/decisions/DEC-20260702-001` `:110-132` 与 `DEC-20260731-001` 全文 · 实读主仓 `CLAUDE.md`/`README.md` 当前逐行内容 · `forgejo GET` 实查 Aria#177 全文 + aria-plugin#127/#152 现状 (含评论数) · 逐簇重新点算 R1 (23 Major) / R2 (21 Major) 聚合表的 Major 归属分类。

结论: **归我席的三个 R2 簇 (#11 DEC 前向指针 / #12 版本引用点 / #13 Phase D 待办) 中两个真正收敛 (#11/#13), 一个方向对但落地时把引用换成了错误的行号 (#12)**；另发现一个**新**的、面向 owner 决策本身的事实性问题 (Why 段「~2/3」统计口径), 以及一个**新**的知识架构问题 (`gate-state-helper-invocation` 探针重造了本项目已有的通用机制)。0 Critical, 2 Major (均可在不推翻 v3 设计的前提下于几行文字/几行代码内吸收), 1 Minor。

## R2 处置核对

| 簇# (来源) | 状态 | 证据 |
|---|---|---|
| #11 (A5-R2-M1: DEC-20260731-001 修正案格式弱于先例) | **closed** | v3 §5 表按 `DEC-20260702-001:124-128` 先例钉死两处写法: 「小节内加一行 `📌 前向指针 (日期): ...见文末`」(就地指针, 落点在 `DEC-20260731-001:28` 那句被 #152 证伪的断言旁, 本席实读该文件确认 `:21`=`## 退役裁定 (2026-07-31)` 小节标题 / `:28`=待打指针的具体断言句, 位置精确) + 「文末加日期化 `## 📌 前向指针` 段」。本席逐行核对 `DEC-20260702-001:124-128` 原文: `:122`=`## 〔勘误†〕2026-07-04 前向勘误` 标题 / `:124-126`=更正正文 (引用具体行号 line 22/69/88 就地指针) / `:128`=「上文…字面表述保留原样（历史决策记录不回改），本节仅作前向指针」——v3 计划的「原文不回改 + 小节内 📌 + 文末日期化段」三要素与该先例的「原文不改 + 三处 〔勘误†〕就地标记 + 文末章节」结构一一对应 (符号用 📌 非 〔勘误†〕/🔴, 但功能结构相同)。R2 finding 提出的两个具体缺口 (「读者停在小节本身看不到指针」+「格式是散文非独立区块」) 均已解决 |
| #12 (A5-R2-M2: 版本同步面主仓侧漏 CLAUDE.md 自身 + README `Plugin Version:` 行) | **partial** | README 半边**完全吸收**: 本席实读 `README.md:8` (badge, 含 `v1.66.3`) 与 `:242` (`Plugin Version:   1.66.3 (aria-plugin, 42 Skills + 11 Agents)`, 本席用 `sed -n '235,248p'` 核对行号精确), v3 §5「主仓侧: gitlink / VERSION / README.md:8 badge / README.md:242 Plugin Version 行 / i18n」逐字落实 #177 原文点名的「两处都得改」。**但 CLAUDE.md 半边是一次「引用替换」而非真正吸收**——见新 Finding [A5-R3-M1] |
| #13 (A5-R2-M3: 三处 Phase D 待办纯散文、无 WHO/WHEN/机械路由) | **closed** | v3 新增 `## 6. Phase D 待办 (AI, D.1 执行, 归档门前置; A.2 转 tasks)` 小节, 标题即给了 WHO (AI) + WHEN (D.1, 归档门前置) + 路由 (A.2 转 tasks); 三个子项逐条继承此归属: (1) issue #152 改「A.1 批准后评论」(本席 `forgejo GET .../issues/152/comments` 复核仍 0 条评论, 与「批准后」的未来时态一致, 不再是 R2 指出的「立案时」时态站不住问题); (2) (b) 轴 issue 现明确落在「Phase D 待办」小节内 (不再需要从 Out of Scope 段推断阶段); (3) `aria-plugin#127` 直接点名 `(open, ...)`, 删除了 R2 指出的「若无则新开」条件语气 (本席复核 #127 确为 open、0 评论, 标题与 rule6_note 描述的缺口逐字对应)。「A.2 转 tasks」的可信度本席核实: `task-planner/SKILL.md:60-65` 明确「IF tasks.md 存在 → 路径 A; ELSE → 输出: 仅 detailed-tasks.yaml」——本 spec 是 Level 2 (无 tasks.md) 但 task-planner 仍会走路径 B 产出 `detailed-tasks.yaml`, 而 `phase-d-closer`/`openspec-archive` 正是扫描这份文件做完成度核验 (本席 R2 已实读确认), 机械路由链路成立, 非空头承诺 |

## 交叉一致性检查

逐一核对 v3 新增/改写内容与既有 Design Decisions / Out of Scope / Risks 是否互斥: 未发现新的条款间直接矛盾。但发现一处**同形状复发**, 值得作为交叉一致性证据记录: R2 cluster #1 (`gate_state_helper.py` 运行时零消费方) 的修法本身 (加 CLI + telemetry + 主仓 state-check「作真被生产调用探针」) 恰好落进了本项目自己反复点名的反模式——**为了证明「机制A(gate_state_helper)真被调用」而新写的机制B(gate-state-helper-invocation 探针), 没有复用项目里已经为「证明某机制真被生产调用」这类需求专门做过的通用化产物**, 与 memory `feedback_fix_recurs_in_its_own_fallback_path`(「修复类 change 最易在自己新写的兜底路径重犯要治的病」)同构——见新 Finding [A5-R3-M2]。

## 引用准确性复核 (v3 新增引用, 逐条实核)

| 引用 | 结果 |
|---|---|
| `DEC-20260702-001:124-128` | **准确**。实读确认 `:122`=前向勘误标题、`:124-126`=更正正文、`:128`=「原样保留+本节仅作前向指针」收尾句, 与「先例」定性完全吻合 |
| `state-scanner/scripts/phase1_gate.py` + `coordination-gate-invocation` 先例 | **部分准确**: `phase1_gate.py` 确有 `_main` CLI 入口、确是「唯一生产调用点经 CLI 走 subprocess」模式的源头 (本席 grep 命中 `# Only ONE call site passes source="production": the CLI _main`), 引用其「CLI 接线」范式准确; 但引用 `coordination-gate-invocation` 作探针范式先例时, v3 只复制了它在 `.aria/state-checks.yaml` 里的**语义参数** (14d 窗口 / warning severity), 未复制它在**脚本落点**上的真实先例 (`coordination_probe.py` 是 `aria/skills/state-scanner/scripts/` 下的插件交付物, 且是**薄封装**, 委托给通用库 `lib/runtime_probe.py`) ——见新 Finding [A5-R3-M2] |
| `aria-plugin#127` (open, C.2.4 surface 义务零 eval 覆盖) | **准确**。`forgejo GET /repos/10CG/aria-plugin/issues/127`: state=open, comments=0, 标题「AB 两套件均覆盖不到 C.2.4 的 D9 surface 措辞」与 rule6_note 描述逐字对应 |
| `README.md:8`, `:242` | **准确** (逐行实读, 见上表) |
| `marketplace.json:3`, `:16` | **准确**。`aria/.claude-plugin/marketplace.json:3`=顶层 `"version": "1.66.3"`, `:16`=嵌套 plugin 块 `"version": "1.66.3"`, 与 #177 原文「含 2 个 version 字段 (`:3`/`:16`)」逐字吻合 |
| `CLAUDE.md:5` 是主项目版本 (2.0.0), 本 PATCH 不动 | **技术上真, 但引用错了靶子** ——本席实读 `CLAUDE.md:5` 确为 `> **版本**: 2.0.0`(主项目版本), 该行确实不该被 aria-plugin 的 PATCH 触碰。但 Aria#177 (v3 声称遵循的 issue) 原文点名的从来不是这一行, 而是「`CLAUDE.md:139`(版本区间) + `:141`(「版本:」行)」——本席核对当前 CLAUDE.md, 这两处内容仍在 (`:139`≈「aria-plugin 方法论轨: v1.52.0–v1.66.3 已 ship」, `:141`=「版本: 插件 aria-plugin v1.66.3 \| 主项目 v1.7.3 \| 运行时 aria-orchestrator v2.0.0」), 且 `:141` 逐字含 `aria-plugin v1.66.3`——v1.66.4 ship 后这一行才是真正会过期、且无任何 custom check 兜底 (`m6-version-badge-match`/`i18n-readme-translation-currency` 均不检查 CLAUDE.md) 的那一行。详见新 Finding [A5-R3-M1] |
| `#152`/`#127` 现状 (0 评论) | **准确**, 与 v3 §6 新时态措辞一致 |

## 新 Findings

### [A5-R3-M1] Major — 版本同步面「CLAUDE.md 自己」引用换成了错误的行号, #177 真正点名的那一行仍不在同步清单里

**锚点**: proposal.md §5 最后一段:「…`CLAUDE.md:5` 是主项目版本 (2.0.0), 本 PATCH **不动**」; 对照 Aria#177 原文与当前 `CLAUDE.md` 内容。

**问题**: 本席 R2 的 [A5-R2-M2] 指出 v2 版本同步面「漏 CLAUDE.md 自己」, 并引用了 #177 的原文——「`CLAUDE.md:139`(版本区间) + `:141`(「版本:」行) 各含版本号」。v3 §5 确实新增了一句提到 `CLAUDE.md`, 但引用的是 `:5`, 不是 `:139`/`:141`。本席刚刚用 `sed -n '1,8p'` 与 `grep -n "版本"` 分别核对了这两个说法:

- `CLAUDE.md:5` 原文 = `> **版本**: 2.0.0` —— 这是文件顶部的**主项目版本声明**, 与 aria-plugin 版本无关, 本 PATCH 确实不该动它。这句话本身**没有错**。
- `CLAUDE.md:141` 原文 = `版本: 插件 aria-plugin v1.66.3 | 主项目 v1.7.3 | 运行时 aria-orchestrator v2.0.0 (86bb684)` —— **这一行才是** #177 点名、且逐字含 `aria-plugin v1.66.3` 的那一行。它归属「项目状态」段 (CLAUDE.md 头部规则: 「预算 15-20 行, 覆写非追加」), 会在 v1.66.4 ship 后变得过期, 而 `m6-version-badge-match`/`i18n-readme-translation-currency` 两条既有 custom check **均不检查 `CLAUDE.md`**——这正是 #177 标题「四错一行…自指盲区…无任何 custom check 兜它」描述的确切场景。

也就是说, v3 用一句**技术上为真、但回答的是另一个问题**的话 (`CLAUDE.md:5` 不该动——没人说该动它) 替换掉了 R2 finding 实际要求的东西 (把 `:139`/`:141` 列进同步清单), 造成"看起来已经处理了 CLAUDE.md 自身这一半"的表象, 而 #177 真正指控的那一行仍然缺席清单。

**按 spec 实施会怎样错**: 执行版本 bump 步骤 (Phase C/D) 的人若按 §5 字面逐项过一遍, 会看到「`CLAUDE.md:5` 不动」这一条并认为「CLAUDE.md 那部分已经交代过了」, 从而不会主动去改 `:141` 那一行——而这一行**不会被任何 custom check 标红**, 若执行者当时恰好没有在同一 session 顺手刷新「项目状态」段 (该段刷新在实践中依赖 session 是否触碰它, 并非版本 bump 步骤强制清单里的一项), `:141` 会在 #177 open 期间**第四次**复现同一形状的漏项——本 spec 恰是 #177 开立后第一个真正执行版本 bump 的 spec, 是检验「#177 的教训是否被真的吸收」的第一案例。

**建议**: 把 §5 该句改为「`CLAUDE.md` 自身版本引用行 (当前 `:139`「aria-plugin 方法论轨」区间 / `:141`「版本:」行, 均含 `aria-plugin v1.66.3`, 本 SHA 行号以实读为准) 随「项目状态」段本次一并刷新; `CLAUDE.md:5`(主项目版本 2.0.0)不动, 与 `:139`/`:141`(插件版本)是两件事, 不可互相替代」——把两句话都保留, 而不是用后者的引用悄悄顶替前者要求的引用。

---

### [A5-R3-M2] Major — `gate-state-helper-invocation` 探针的落点/设计脱离了它自称"镜像"的先例的真实交付形态, 且完全错过项目已有的、专为此场景设计的声明式归档探针机制

**锚点**: proposal.md §3.1「主仓 `.aria/state-checks.yaml` 加 `gate-state-helper-invocation` (warning; 14d 内 telemetry ≥1 条, **镜像 `coordination-gate-invocation`**)」+ §5 表「主仓 `.aria/state-checks.yaml` (+ `.aria/probes/`)」; 对照实读 `.aria/state-checks.yaml:221-241` (`coordination-gate-invocation` 条目全文) + `aria/skills/state-scanner/scripts/coordination_probe.py` + `aria/skills/state-scanner/scripts/lib/runtime_probe.py` + `aria/skills/state-scanner/references/runtime-probe-declaration.md`。

**问题(一) — "镜像"只镜像了参数, 没镜像交付面**: `coordination-gate-invocation` 的探针脚本 `coordination_probe.py` **本身是插件交付物** (`aria/skills/state-scanner/scripts/`, 随 aria-plugin 分发给所有采用方), 而且它自己只是个**薄封装**——本席实读其 module docstring 第 22-27 行:「This module used to own its own read+parse+count logic. It now DELEGATES that to the generalized `lib/runtime_probe.py`」。也就是说, 本项目**已经把「检测某机制是否真被生产环境调用」这件事通用化并随插件分发**, `coordination-gate-invocation` 只是它的第一个 (调用方式为**硬编码 descriptor**的) 消费者。v3 §5 把 `gate-state-helper-invocation` 的探针脚本放进 `.aria/probes/`——这是**主仓专属、不随插件分发**的目录 (对照该目录下既有的 `config-template-key-currency.py`/`plugin-cache-currency.py`, 二者的检查对象天然就是"本仓的本地 config/cache 是否漂移", 主仓专属合理), 而 `gate-state-helper-invocation` 检查的是**插件自身机制** (`gate_state_helper.py` 的 CLI) 是否真被调用, 与 `coordination-gate-invocation` 检查 `run_gate()` 是否真被调用性质完全相同, 理应走同一交付面。放进 `.aria/probes/` 意味着任何其他 aria-plugin 采用方 (如 memory 里提到的 Kairos) 若也用到 `pre_merge_gate` 的 no-run-for-branch 机制, 得不到这个探针脚本, 得自己从零重写。

**问题(二) — 完全错过已有的声明式归档探针机制, 而本 spec 恰是它「等待中的第一个采用者」**: 本席读到 `aria/skills/state-scanner/references/runtime-probe-declaration.md` 全文, 这是 aria-plugin #95 follow-up A (`DEC-20260705-001`) 专门为「某 spec 新引入一个写生产 telemetry 的机制, 想在归档时核验它真被调用过」这个**确切场景**设计的**声明式**机制: spec 作者只需在 `proposal.md` frontmatter 加 4 行 `runtime_probe:` 声明 (`partition`/`symbol`/`max_age_days`/`enabled_when`), `openspec-archive`/`phase-d-closer` 的 D.2 归档门会自动读取本 spec 自己的 `.aria/gate-state-telemetry.jsonl` 分区、判定新鲜度, 完全不需要新写 `.aria/state-checks.yaml` 条目或 `.aria/probes/*.py` 脚本。该文档明确写道 (`:136-139`, 本席逐字引用):「截至本文档撰写时全部已归档 spec…都保持无声明状态…**未来第一个真实声明者, 会是下一个自带 telemetry 分区的活跃中 spec**」——`pre-merge-gate-no-run-for-branch` 恰好就是这样一个"自带 telemetry 分区" (`.aria/gate-state-telemetry.jsonl`) 的活跃 spec, 且本席核实其数据源前提也满足 (`runtime-probe-declaration.md` 表格明确「无 tasks.md、有 detailed-tasks.yaml (task-planner path B / 常见 L2) → ✅ 评估, v1.63.0 起」, 本 spec 正是这一形态)。v3 全文 (含 Cross-references) 没有一处提到 `runtime_probe:` 声明或 `runtime-probe-archive-gate-integration` / `DEC-20260705-001`。

**按 spec 实施会怎样错**: (1) 实施后, Aria 主仓自己得到了正确的持续监控 (功能不受损), 但其他 aria-plugin 采用方对同一形状的机制盲区**得不到**任何随插件分发的保护——这与 R2 cluster #1 本来要解决的问题 (`gate_state_helper.py` 只是 reference 实现, 没人真的用它) 是**同一形状在更高一层复发**: 这次新写的"证明真被调用"的机制本身, 又是一份没有复用已有通用产物、只服务本仓一份的实现。(2) 本 spec 错失了一次几乎零成本 (4 行 YAML) 就能在 D.2 归档门拿到的额外核验层, 而这个机制的文档现在还写着"等待第一个真实声明者"——如果连本 spec 这种教科书级适配场景都没有用上, 这份声明式机制存在的意义会进一步被质疑。

**建议**: 二选一或都做 (不互斥): (a) 把探针脚本改写为 `aria/skills/workflow-runner/scripts/gate_state_helper_probe.py` (或挂在 `state-scanner/scripts/` 下), 内部委托 `lib/runtime_probe.py::probe()` (传 `partition=".aria/gate-state-telemetry.jsonl"`, `symbol="gate_state_helper_record"`), `.aria/state-checks.yaml` 的 `command:` 改指向这个插件路径——这样才是对 `coordination-gate-invocation` 真正意义上的"镜像"; (b) 在 `proposal.md` frontmatter 补一段 `runtime_probe:` 声明 (4 字段), 让 D.2 归档门顺带核验, 同时把这段实践写进 `runtime-probe-declaration.md` 的"相关文档"或用一次真实调用给这份文档"验货"。两者都做的话, `.aria/state-checks.yaml` 条目负责**持续监控** (SC-16 要的 `/state-scanner` 场景), `runtime_probe:` 声明负责**归档时一次性把关**, 互补不冲突。

---

### [A5-R3-m1] Minor — Why 段「~2/3 Major 长在自动写动作身上」的统计口径与 R2 聚合报告的官方口径不一致, 实数达不到 2/3

**锚点**: proposal.md Why 段末 (「为什么 v3 不再自动执行处方」) 及 `pending_owner` 请复议文本:「两轮审计 ~2/3 的 Major 都长在它身上 (幂等 / 求值时点 / dispatch 可用性 / commit 伪造 / 双 prompt)」; 对照 `post_spec-R2-…-aggregated.md` frontmatter `major_trend: "…R2 Major 中 ≥ 2/3 落在 v2 新条款…"` 及 R1/R2 两份聚合表逐簇来源。

**问题**: R2 聚合报告确实写了「≥2/3」, 但它的统计对象是**「v2 新条款」整体** (即 v1→v2 新增的全部内容: 一次性守卫字段 / 求值时点修正 / PR 分支存在性核验重构为第八早退 / `gate_error` kind 封闭集调整 / message 按 decision+reason 键控 / rule6_note 选行 / AD-4 阈值依据 / §5 同步面…), 而 v3 Why 段把它**窄化改写**成专指「自动写动作 (dispatch / 推 commit)」这一个子设计, 并直接沿用同一个「2/3」数字。本席把 R1 (23 Major) 与 R2 (21 Major) 两份聚合表逐簇按"这条 Major 描述的问题, 若 v1/v2 从一开始就没有'自动执行处方'这个子设计, 是否根本不会存在"重新点算:

- R1: 严格计入 (幂等/求值时点/dispatch可用性/commit伪造/双prompt 五个具体败因直接命中) = **7/23** (≈30%); 从宽把"升级判定重复实现"等衍生问题也计入 = 至多 **9/23** (≈39%)。
- R2: 同口径 = **8/21** (≈38%); 从宽 = 至多 **10/21** (≈48%)。
- 两轮合计, 严格 **15/44** (≈34%), 从宽至多 **19/44** (≈43%)——**在任何一种合理归类下都到不了 2/3 (67%)**。

而 v2 新条款里**明确不属于自动写动作、且 v3 原样保留 (未被"设计收缩"删除)** 的部分 (PR 分支存在性核验重构 / `gate_error` kind 结构 / message 键控 / config 阈值双消费点 / §5 同步面), 本身就贡献了 R1+R2 两轮相当一部分的 Major (仅这几类粗略估计已占 R1 约 9 条、R2 约 8 条), 这些**不会**因为删除自动写动作而消失, 且事实上在 v2→v3 的 R2 处置表里也确实是**继续被修**而不是被砍掉的。

**按 spec 实施会怎样错**: 影响有界——本席认为「删自动执行处方」这个设计决策本身在技术上是合理的 (2 条 Critical + 多条 Major 确实出在 dispatch/commit 自动执行相关条款上, R1-C1/A4-C1/AD-5 一簇是真实、独立于统计口径成立的理由), 不需要靠这个数字撑腰。真正的风险在治理层面: `pending_owner` 请 owner 复议一个**偏离 A′ 裁定字面**的设计收缩, 所给的量化理由把一个更大范围统计 (v2 全部新条款) 的结论套用到一个更窄的主张 (自动写动作) 上——这与本项目 memory `feedback_ai_narrows_owner_decision_space` 描述的模式同族: 不是隐藏选项, 而是**用超出实际支撑范围的证据加重己方倾向选项的分量**, 若 owner 未逐簇复核就采信「2/3」这个数字来做复议判断, 判断依据本身是不准的。

**建议**: 二选一——(a) 把 Why 段的理由改写为不依赖精确比例的定性说法 (如「两轮审计里体量最大的一组 Critical/Major 集中在幂等/求值时点/dispatch可用性/commit伪造/双prompt 这五类自动写动作专属败因上, 且 AD-5 建在未验前提上」, 不给「2/3」这个数字); (b) 若坚持给比例, 按上表的严格/从宽两个实数 (34%~43%) 改写, 不要沿用 R2 聚合报告「v2 新条款整体」的「2/3」数字回答一个更窄的问题。

## Verdict

**verdict**: PASS_WITH_WARNINGS (0 Critical / 2 Major / 1 Minor)
**vote**: REVISE

归我席的三个 R2 簇中两个真正收敛 (#11 DEC 前向指针格式、#13 Phase D 待办路由), 均达到"落地方式对齐项目自身先例"的标准, 不再展开。第三个 (#12 版本同步面) 表面上"提到了 CLAUDE.md", 实际是把 R2 finding 指名的行号换成了另一行技术上无误但答非所问的行号——这个模式本身 (用一个真但不对题的引用制造"已处理"的表象) 值得在 R3 单独立一条 (M1)。另发现一条新的知识架构问题 (M2): 本 spec 为了证明"gate_state_helper 真被调用"而新增的探针机制, 自己没有复用项目里已经通用化、且明确写着"等待第一个采用者"的同类机制——这是本项目自己反复点名的"修复在自己的新条款里重犯同形状缺陷"模式的又一例, 且直接影响交付面 (仅本仓受益 vs 全体 aria-plugin 采用方受益)。以及一条 Minor (m1): Why 段量化理由的统计口径经重新点算与来源数据不符, 不影响设计决策本身的合理性, 但作为呈给 owner 复议的证据应改得准确。三条均可在不推翻 v3 设计的前提下于 R3 前吸收 (改几行引用文字 + 挪一个探针脚本文件位置/加一段 frontmatter 声明), 不建议因这些问题把方案打回重做。

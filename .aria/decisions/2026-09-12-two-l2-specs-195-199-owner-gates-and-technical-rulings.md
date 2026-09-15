---
type: owner_decision_sheet
subject: 两份 L2 Spec (10CG/Aria#195 / 10CG/Aria#199) 的 Phase A 出口待复议项 — 产品级 owner 裁 / 技术级 AI 裁 分工单
spec_ids: [handoff-multibranch-subdir-path-fidelity, pre-merge-completeness-gate-change-scope]
checkpoint: post_spec (max_rounds=5 已耗尽, 两份均 converged=false)
status: decided
decided_by: owner (uni.concept.wzfq@gmail.com)
decided_at: 2026-09-12
created: 2026-09-12
container: simonfish/023236f2
---

# 决策单 — 10CG/Aria#195 与 10CG/Aria#199 两份 Spec 的 Phase A 出口: owner 门 3 问 + 技术级裁定 21 条

> **为什么有这份单**: 2026-09-11 handoff §2 把两份 Spec 的**全部** 22 条待复议项列为「owner 裁决面, Phase B 零合法动作」。按 owner 2026-09-01 的分工原话 (「我应该只决策产品级别, 技术实现级别应该你直接决定, 判断标准由产品决策倒推」, 决策单 `2026-09-01-a1-entry-h1-h6-technical-rulings-product-vs-technical-split.md`), 本单把 22 条逐条归类: **真正要 owner 的只有 3 问** (两条 enabled 闸门的 max_rounds 终局 + 执行顺序), 其余 **21 条是技术级**, 由本单直接裁并附可证伪判据与回退方式。技术裁定不需要逐条签字 —— 它们随 Spec 进入 A.2 后由 owner 的 **Status → Approved** 一次追认; 任何一条 owner 一句话即可否决。
>
> **不变的边界**: Rule #10 不变 —— 条目 0 (max_rounds 三路径) 是 enabled 闸门的结论强度, 本单**不代裁**; post_planning (config `convergence`) 照跑。

---

## §1 请 owner 裁 (3 问) — ✅ 已裁 (2026-09-12, AskUserQuestion 三问三答)

| 问 | owner 裁定 |
|---|---|
| Q1 10CG/Aria#195 终局 | **[1] 接受当前结论** ⇒ R5 聚合报告 `overridden_by_user: true`, Status → Approved, 进 A.2 |
| Q2 10CG/Aria#199 终局 | **[1] 接受当前结论** ⇒ 同上 |
| Q3 执行顺序 | **#195 先**, 串行 |

### Q1 · 10CG/Aria#195 `handoff-multibranch-subdir-path-fidelity` — post_spec max_rounds 终局三路径

| 轮 | C / M / m | 票型 | 聚合 verdict | 与上轮四元组交集 |
|---|---|---|---|---|
| R1 | 2 / 15 / 10 | REVISE 5 | FAIL | — |
| R2 | 3 / 10 / 9 | REVISE 5 | FAIL | 0 |
| R3 | 0 / 19 / 7 | REVISE 5 | PASS_WITH_WARNINGS | 0 |
| R4 | 1 / 10 / 14 | REVISE 5 | FAIL | 1 |
| R5 | 0 / 9 / 13 | REVISE 5 | PASS_WITH_WARNINGS | 0 |

三路径 (`audit-engine/SKILL.md §降级策略` 逐字): **[1] 接受当前结论** (`overridden_by_user: true`, 进后续流程) / **[2] 增加轮次** (`max_rounds += 2` ⇒ 7, 跑 R6/R7) / **[3] 降级为单轮** (`degraded: true`, 后续检查点单轮)。

**AI 建议: [1]**。依据是 owner 自己两次裁过的成文判据: (a) memory `feedback_audit_marginal_return_goes_negative`「本轮 fix 引入的 major 占比 > 1/2 即拐点」—— R5 的 9 条 Major 中 4 条是 R4 落地内容自身缺口 + 5 条「基线陈旧」族 (会随时间自我再生, 席位明写「不重冻基线则收敛不可能发生」), 即 9/9 都不是设计缺陷; (b) memory `feedback_stop_adding_rounds_when_major_count_flattens`「换新鲜眼睛 > 加轮」—— 五轮已换五次执笔, Critical 已归零两轮, Major 9→9 持平。[2] 在现行判据 (`vote == PASS` 要求 Major 同时为 0) 下**结构上不可能收敛**, 只会多烧两轮; [3] 会削弱 post_planning 这道仍要跑的闸, 没有必要。

### Q2 · 10CG/Aria#199 `pre-merge-completeness-gate-change-scope` — 同一问

| 轮 | C / M / m | 票型 | 聚合 verdict | 与上轮四元组交集 |
|---|---|---|---|---|
| R1 | 5 / 9 / 10 | REVISE 5 | FAIL | — |
| R2 | 2 / 9 / 16 | REVISE 5 | FAIL | 语义持存 5 |
| R3 | 3 / 12 / 13 | REVISE 5 | FAIL | 0 |
| R4 | 0 / 14 / 15 | REVISE 5 | PASS_WITH_WARNINGS | 1 |
| R5 | 0 / 15 / 15 | REVISE 5 | PASS_WITH_WARNINGS | 2 |

**AI 建议: [1]**, 同一判据且更强: R5 聚合席点名 15 条 Major 中**至少 11 条**属「R4 修法自身的下游未闭合」= 73% > 1/2, 拐点判据字面命中; 连续两轮 PASS_WITH_WARNINGS 5/5 零分歧。

### Q3 · 执行顺序 (两份都要走 A.2 → A.3 → post_planning → B → C → D, 单执行席串行)

**AI 建议: #195 先**。理由: 代码面小 (一个 collector 四处路径 + 一个字段 + 一个守卫), 报告方有活体症状 (子目录采用方 `scan.py` 恒 exit 10); #199 是新脚本 + 闸门规程重写, 且本仓 `pre_merge` config off, 修复的受益人是外部采用方。两份都裁 MINOR (见 §2), 号在各自 ship 时按 `plugin.json` 重算 (09-12 裁定), 先 ship 的拿下一个 MINOR 号。

---

## §2 技术级裁定 (21 条; 每条: 判据 → 可证伪核验 → 回退)

### #195 `handoff-multibranch-subdir-path-fidelity` (proposal §待 owner 复议 条目 1–8)

| # | 事项 | 裁定 | 判据 (倒推链) | 可证伪核验 | 回退 |
|---|---|---|---|---|---|
| 1 | pointer 排除口径「任意深度」是否收窄 | **不收窄, 保持现状** | 现状非本 spec 引入: `handoff_multibranch.py:277-280` 在 `301641b..f314785` 零 diff; 收窄 = 行为变更, 需自己的 SC | SC-8 前半保持「`archive/latest.md` 不进 `tracks[]`」 | 改判 = 改代码 + 改 SC-8 |
| 2 | DEC-20260907-001 (A′ + 写侧守卫) 五问 | **(1) 接受「子目录采用方在 writer 接线后只拿降级 pointer」, 本 cycle 不做 (ii)**; **(2) 遗留缺口 issue 开 `10CG/aria-plugin`**; **(3) 追认 A′**; **(4) 本 cycle 不动 `handoff-mechanics.md:114-124`**; **(5) 5a/5b/5c 三处勘正以 proposal 为准, 决策单不改 (历史记录)** | (1)(4) 同一条实测判据: `write_latest_md` 在 aria `44f00d1` 非测试调用点**为零** (仅 `writers/__init__.py` 再导出) ⇒ 该代价今天无人在付, (ii) 零受益人却扩面到 H5 pointer 权威; `handoff.py:288` 取 `Path(target).name` + `:318` 非递归 `iterdir()` ⇒ (4) 单独做会让 D.3 手写出读不回的 pointer, 只有与 (ii) 同做才自洽, 故与 (1) 同判。(2) 先例: 代码宿主开单 (今日 `10CG/aria-plugin#199` / `#194` / `#195` 同类) | SC-15 端到端往返: 顶层 track 走真指针且能读回; 子目录 track 走守卫分支且**不产生** `handoff_pointer_target_missing` | owner 要 (ii): 触点面加 `handoff.py` 两函数 + H5 测试面, Level 仍 3; 不追认 A′: 回退 `rel_path` + 守卫 ≈ 1 commit |
| 3 | 新增 `unreadable_count` | **新增** | 「读不到多少文件」须机读; 只留 soft_error 则要数 errors 文本 | SC 断言字段存在且与夹具坏文件数相等 | 删字段 |
| 4 | dedupe 排序键: 主问 + 附问 (`rel_path` 第 5 级) | **主问: 不动既有四级键**; **附问: 加 `rel_path` 为第 5 级** (`rel_path == filename` 的顶层行优先, 其余字典序) | schema `:1126` 宣称 build-order 不变性; A′ 使「同 basename 异目录」并列**可观测**, 不加第 5 级则该宣称为假 (memory `feedback_invariant_needs_failclosed_default`: 不变量写进文档 ≠ 写进兜底) | 夹具: 同 `(track_id, identity_key)` 同 `updated_at` 同 `branch` 同 basename, 一顶层一子目录 ⇒ 代表行**恒**为顶层, 与构造顺序无关 | 撤第 5 级 + schema `:1126` 改写为「已知边界」 |
| 5 | `_get_file_commit_date` mv 日残余 | **不处理; CHANGELOG 记已知边界; Phase B 禁加 `--follow`** | 是语义问题 (「最近一次触碰该路径」) 非路径问题, SC-4 已实跑证明 `--follow` 救不了 | — | — |
| 6 | 版本级别 PATCH vs MINOR | **MINOR** (号 ship 时按 `plugin.json` 重算, 不预分配) | SOT `standards/conventions/version-management.md §2.2`「功能增强 (向下兼容)」字面覆盖: 三个新机读字段 + 采用方可见行为变化 (可翻 `collision.kind`); §2.3 四条无一覆盖; 先例 v1.70.0 owner D5「对采用方是行为变更 ⇒ MINOR」同型; 09-01 H1a 同判据 | 发版 CHANGELOG 首节 `### Added`, minor +1、patch 归 0 | owner 一句「PATCH」⇒ 只改 Task 5.1 目标号 |
| 7 | Level 2 vs 3 + tech-lead 拆分建议 | **Level 3; 不拆** | `spec-drafter/LEVEL_GUIDE.md:156-162`「跨模块条件 (满足任一)」两条字面命中: 「影响多个子模块」(aria + standards, Task 4.4) 与「需要 API 契约变更」(`rel_path` / `unreadable_count` / `degraded_reason` + `_render_pointer` 返回形状) ⇒ 「自动提升为 Level 3」; owner 09-05 对同 collector 家族相邻 spec 用同判据裁 Level 3 (归档 `2026-09-06-owner-container-identity-key-and-collision-parser/proposal.md:3`)。**不拆**: 守卫是 A′ 的必需配套 (决策单原文「不是折中选项」), 拆开 = 守卫落进一份今天没有受益人的 sub-spec (memory `feedback_splitting_a_spec_manufactures_seam_defects` / `feedback_no_ruling_shortens_the_distance_signal`) | 目录含 `tasks.md` + `detailed-tasks.yaml`; post_planning 照跑 (config enabled) | owner 一句「Level 2」⇒ 撤两文件, 前提是 Task 4.4 判 deferred **且** owner 明示「API 契约变更」判据不适用 |
| 8 | 既有测试日历依赖 | **已由上游关闭, 无需裁** | `10CG/aria-plugin#194` 修复随 v1.73.1 发布 (aria `44f00d1`), `f314785` 上 `Ran 23 … OK` | — | — |

### #199 `pre-merge-completeness-gate-change-scope` (proposal §待 owner 复议 #1–#13)

| # | 事项 | 裁定 | 判据 (倒推链) | 可证伪核验 | 回退 |
|---|---|---|---|---|---|
| 1 | Step 3 追加排除 `post_brainstorm` | **追加排除** | 与 `:51-52` #79 条款同构: 条件性产物, 与 change_id 无机械关联, 「启用即会误阻」 | SC-18 保留「排除」分支 | 撤排除, SC-18 取另一分支 |
| 2 | `--no-spec` 残余弱点是否加固 | **接受残余, 本 spec 不加固**; 加固 (交叉 `refs/aria/coordination` claim) 另开 issue | 两个真空面 (核验面绑 diff 仓 / 空 diff) 已由 P2a 前置封掉; 残余场景须「proposal 早在 master 且本分支不碰 change 目录」, 且 audit trail 留 `scope_source=no_spec` 可事后核 | SC 对两个真空面各一条反事实 (坏实现 = 回到绑 diff 仓) | — |
| 3 | 可配置下界 N | **不做** | 按 change 收窄后 N=1 即语义本身; 做则先补 F8 config 注册面 | — | — |
| 4 | (4a) 号 / (4b) 级别 / (4c) ab-suite 版本 | **(4a) ship 时按 `plugin.json` 重算**; **(4b) MINOR**; **(4c) `ab-suite/version.yaml` 顺延 1.6.0, bump 前 `git fetch --all` + `ls-remote --tags` 复核** | (4b) §2.2 字面: 新增可执行脚本 + 两个新输入参数 + 八条采用方行为变更 (含两条配置行为反转); 先例 v1.73.0 (新增三个机械兜底脚本) MINOR (`aria/VERSION:4`) | 同 #195-6 | 同 #195-6 |
| 5 | Rule #6 档位标签 | **第三行标签 + 并集执行** | 裁决不改变 Phase B 动作集 (三套件照跑 + 定向 fixture + 缺口 issue 已是并集) | rule6_note 写明并集 | — |
| 6 | §1.3(c) 判据口径 | **维持 fail-closed 收窄, 无需裁** | 只有**放宽**才需 owner | — | — |
| 7 | §1.3(b) diff 类 not_applicable 存废 | **保留收窄后的 (b)** | 对应 issue 里真实发生过的 Phase A-only PR 场景; SC-5 七条反事实把放行面钉死 (归档-only PR / openspec 语料型 cycle 均 `missing`) | SC-5 | 删 (b) ⇒ SC-5 改「Phase A-only 亦 missing」 |
| 8 | 空纳入集 (8a) pass vs error / (8b) 格 D | **(8a) 格 B 判 `pass` + `no_prior_checkpoints=true` + `[INFO]`**; **(8b) 格 D 成立** | (8a) Rule #10 白名单第一类「配置显式关闭是 owner 的配置决定」字面 + `audit-engine/SKILL.md:410-411` 空集 pass-through 先例; 「error + 逃生口」需新 config 键, 与本 spec「不新增 config 键」冲突。(8b) `config-loader/DEFAULTS.json:130` 实测 `level_1: "off"` ⇒ 调用方无法预判被审 change 的 Level ⇒ 格 C「调用方本该早退」前提对 adaptive 推导不成立 | SC-15 保留 pass 分支 | 改 error ⇒ 新键 + F8 注册面; 撤格 D ⇒ 回落格 C, 四处回改 |
| 9 | `phase-c-integrator-pre-merge-gate.json` 是否 AB 照跑面 + catalog 缺口 | **不进 AB 臂; 跑其 5/8 可执行 fixture 单测; catalog 3 条缺口 (`wait_then_green` / `NEG-2-timeout` 无 node id, `NEG-1-malformed` node id 过期) 开 issue 到 `aria-plugin-benchmarks`** | Rule #10 白名单**第四类**逐字「结构性前提不成立 (审的对象整个未产生)」: 该 catalog 无 `evals` 键, `total_eval_cases = 0`, AB 臂没有对象 (非「存在但简单」) | rule6_note 点名形态差异; 5 条单测 OK | owner 要「跑」⇒ 须先给可执行定义 |
| 10 | `spec_level_undetermined` 逃生口 (a)/(b)/(c) + (d) 格 E | **(a) 现状: 两键各自覆盖**; **(d) 格 E 判 `pass` + 双留痕** | `allow_incomplete_checkpoints` / `allow_dangling_change_ids` 都是采用方**显式 opt-in** 的宽松旗标; 新 error_kind 与其 SOT 语义 (`execution-modes.md:41-44`「作用域不可解析」/ 遗留锚点) 同种 = 证据不完整, 非「输入自相矛盾」; 不给逃生口 = R2 Critical `fdb30703` 同结构; (c) 与「不新增 config 键」冲突 | SC-9(4) / SC-7(d) / SC-15(8) | owner 收窄 ⇒ (b) 或格 E 回落格 C, 四处回改 |
| 11 | 跨仓 + Level 1 + `--no-spec` 锚点零 diff | **(b) 保持硬阻, `allow_incomplete_checkpoints` 覆盖 `no_spec_unverifiable`; `no_spec_contradicted` 仍不豁免** | 同 #10 判据: 「不可核验」是证据不完整, 「自相矛盾」不是 | SC-17(5) | (a) 拆格降级 |
| 12 | Level 2 vs 3 | **Level 3** (与 #195-7 同判据同判) | LEVEL_GUIDE:156-162「需要 API 契约变更」: 两个新 CLI 参数 + 16 键 stdout 契约; `standards/openspec/project.md:114-118`; 附带效应: 归档门 liveness 轴恢复运行 | `tasks.md` + `detailed-tasks.yaml`; SC-12 补回 liveness 子句 (可证伪形态); §1.3(c) 自证段与 SC-6 自证格重写 | 同 #195-7 |
| 13 | 产出侧四个 checkpoint 调用方是否随本 spec 对齐 | **(b) 现状 + Phase D 开 issue** | 方向 fail-closed (假红非假绿); 四调用方 (`phase-a-planner:246` / `task-planner:123` / `phase-b-developer:255` / `brainstorm:141`) 是独立缺陷类「adaptive 推导的 checkpoint 生产链永不产出报告」, 与 10CG/Aria#199 的「按 change 匹配」不同根; 合入会把触点面扩 4 Skill + 4 AB 套件 | §5 第 11 条 + missing Fix 四项 | (a) ⇒ §3 / §4 / Tasks / SC-13 各加四落点 |

---

## §3 裁定后的落点 (待 owner 答完 §1 再动)

1. 两份 proposal 头部 `Level` 改 Level 3; §待 owner 复议 各条目**只追加**一行「⇒ 裁定见本单 §2 #n (2026-09-12)」, 不删原文 (复议链不断)。
2. 条目 0: R5 聚合报告 frontmatter 按 owner 路径回写 (`overridden_by_user: true` 或 `max_rounds` 改 7 或 `degraded: true`); Status 按 [1] ⇒ **Approved (owner 2026-09-12)**。
3. 动手前先经 `phase1_gate.py --phase A.1` 重新认领 (两条原 claim 09-10 已 sweep 为 abandoned, 同伴 handoff 明示「下个 session 用同一串 raw track-id 重新认领即可」)。
4. A.2 `tasks.md` + A.3 `detailed-tasks.yaml` → post_planning convergence (enabled, 照跑) → B。

## §4 一句话回退

任一技术裁定 owner 一句「10CG/Aria#195 第 n 条改 X」或「10CG/Aria#199 第 n 条改 X」即改判; 各条回退成本见表末列。Q1/Q2 若选 [2], 本单 §2 的 Level / 版本裁定仍成立, 只是 A.2 延后到 R7 之后。

## §5 另一会话的 owner 复核 (2026-09-13, 执笔 aria-runner-bot/bfe8285d)

同一批待复议项在并发会话 (容器 `bfe8285d`, 2026-09-12) 里也经 AskUserQuestion 逐项问过 owner。逐条对照结果:

- **一致**: Q1 / Q2 路径 [1]; 两份 Level 3; 两份 MINOR (号在 ship 时重算); DEC-20260907-001 追认, 5a / 5b / 5c 以 proposal 为准, 遗留缺口开在 `10CG/aria-plugin`, 本 cycle 不动 `handoff-mechanics.md`; 10CG/Aria#195 第 1 / 3 / 5 / 8 条; 10CG/Aria#199 第 1–13 条。
- **分歧两处**, 那一侧 owner 当时选的是: 10CG/Aria#195 第 7 条「拆两段」; 第 4 条附问「`rel_path` 不入排序键」。成因在那一侧的呈现方式: 第 4 条附问 proposal 原文**没有推荐默认**, 却被标成「推荐默认: 不加」; 拆分建议没有交代两项代价 —— 守卫是 A′ 的必需配套, 以及拆出的新 proposal 是否要重跑 post_spec。
- **owner 最终裁定 (2026-09-13): 两处都按本单 §2** —— 10CG/Aria#195 第 7 条 **Level 3, 不拆**; 第 4 条附问 **加 `rel_path` 为第 5 级**。本单 §2 全部 21 条即最终口径; 那一侧起草的另一份决策单与 DEC 追认节已撤回, 未进 git, 本单是唯一记录。
- Q3 执行顺序 (10CG/Aria#195 先) 那一侧未问, 沿用本单。
- 两条轨的 claim 在 `simonfish/023236f2` (2026-09-12, 阶段 A.2); `bfe8285d` 不再推进这两条轨。
- 那一侧同会话另开、与本单无耦合: `10CG/aria-plugin#196` / `10CG/aria-plugin#197` / `10CG/aria-plugin#198` (state-scanner 三处缺陷)。

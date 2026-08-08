---
type: owner_decision_sheet
subject: linked-issue-normalization post_planning 闸门 — 拐点处置 + 四项裁量
spec_id: linked-issue-normalization
checkpoint: post_planning
rounds_run: 2
max_rounds: 4
status: awaiting_owner
created: 2026-08-08
---

# Owner 决策单 — post_planning 拐点处置 (linked-issue-normalization)

> **为什么有这份单子**: post_planning 是 config 里 `enabled` 的闸门 (`audit.checkpoints.post_planning = "convergence"`, `max_rounds = 4`)。R2 后出现两类**不属于 AI 裁量范围**的问题: (a) 是否停轮 (Rule #10 不允许 AI 以「性价比」降级闸门); (b) 四项涉及其他 enabled 闸门范围与授权边界的裁定。本单只陈述事实与建议, **不做决定**。

---

## §1 两轮数据

| | R1 | R2 | 判读 |
|---|---|---|---|
| 席位 vote | 5/5 REVISE | **2 PASS / 3 REVISE** | 未收敛 |
| verdict | FAIL (3 Critical) | FAIL (2 Critical) | — |
| 去重后 Critical + Major | 3C + 12M | **2C + 11M** | **基本持平** |
| fix 引入占比 (code-reviewer 测) | — | **5/6 = 83%** | > 1/2 |
| fix 引入占比 (tech-lead 测) | — | **8/13 = 62%** | > 1/2 |

**两条成文判据同时点亮**:
- `feedback_audit_marginal_return_goes_negative` — 判据是「本轮 fix 引入的 major 占比 > 1/2 即到拐点」。两席独立测出 83% / 62%。
- `feedback_stop_adding_rounds_when_major_count_flattens` — 判据是「major 数是否还在降」。12 → 11, 持平。

**三席从三个互不相同的轴指向同一结论**:

| 席位 | 轴 | 结论 |
|---|---|---|
| code-reviewer | 「fix 改坏了什么」 | 新 Major 里 83% 是 R1-fix 引入 |
| tech-lead | 「缺陷迁到哪一层」 | 从任务层迁到 **metadata 层** (块间矛盾 / 闸门拓扑 / 编号契约); N2/N3/N4 三条全长在同一个新任务 TASK-020 上 |
| knowledge-manager | 「同形状扫没扫完」 | fix 已确立修法先例 (把 SC-9 治理约束搬进人读层) 却未类推应用 ⇒ 又漏两条同形状 |

⇒ **问题不在某几条没修好, 在「逐条打补丁」这个修法本身。** (memory `feedback_fix_the_class_not_the_instance`)

**另一条值得记的观察**: R2 的 2 PASS 席 (qa / backend-architect) 在各自镜头内**确实全部闭合、0 new Major**。三条 FAIL 席找到的东西全在**没有任何席位被分派到的轴上** —— 块间交叉一致性、闸门拓扑、断言的健康常态值。是 tech-lead 自己越出镜头抓到的。这正是 `feedback_fixes_contradict_each_other_across_clusters` 记的「接缝落在角度之间」: 分派镜头时漏了这个轴。

---

## §2 R1-fix 自身走错方向的两处 (两条 Critical)

### C1 — 我造的 TASK-016 绕开了两个默认开的闸门 (Rule #10 违规, AI 侧)

**做了什么**: 为修 R1 的 C2 (「多远程硬约束只在 notes 未入 verification」), 我新建 TASK-016「aria 子模块本地 merge + 双推 + 逐远端 ls-remote」并把三条硬判据写进 verification。

**问题**: `phase-c-integrator` **本就建模子模块合并** (SKILL.md:242), 其 C.2.5 就是 TASK-016 手工重写的那套; 且它受两个默认开的闸门约束 —— `pre_merge_gate.enabled=true` (Rule #8) 与 `submodule_gate.mode="block"`。把这件事搬进 tasks.md ⇒ **绕过两个 enabled 闸门**。Rule #10 的四类豁免逐条不成立。

**且 `metadata.scope_boundary` 块内相隔 5 行自相矛盾**: `delegated` 把 merge 交给 phase-c-integrator, `why_group5_is_here` 又承认合并在组 5。

**建议 (待裁)**: **删除 TASK-016, 改为委派 phase-c-integrator**, tasks.md 只保留「组 5 的 aria bump 必须先于主仓 gitlink bump」这条时序约束。

### C2 — TASK-020「根因修法」自己是一个恒红 + 缺席断言

`aria/VERSION` **本身是 append-only 发布纪要账本** (167 行, `发布日期(旧)` 堆叠回溯至 v1.47.0, `:58` 还有裸 `1.47.0`)。bump 后 v1.65.5 那行降级保留 ⇒ 我那条「零命中」断言 **100% 判红**。

**而恒红正是同批 TASK-021 要杀的对偶。** 我在修恒红的同一批编辑里装了一个恒红 (memory `feedback_fix_recurs_in_its_own_fallback_path`)。

另两处同任务缺陷:
- **缺席断言, 维度只对一半**: 只断言旧值零命中, 不断言新值出现应有次数 ⇒ 删行 / 写错新版本号都判绿。
- **排在不可回退点之后**: 依赖链 020 → 018/019 → 017 → **016 (合并+双推)** ⇒ 只可能在 master 已合并已双推、gitlink 已钉死之后才发红, 且无任何回边/重推任务。

---

## §3 我写下的一句不成立的声明 (须成文更正)

`tasks.md:10` 写:「只在组 5 末尾追加 5.5–5.8, **不改动任何既有编号** (5.1–5.4 语义与编号均保持)」。

对 `a52ab81` 实测**不成立**:

| 编号 | A.3 首版 (a52ab81) | R1-fix 后 (3fc6f3f) |
|---|---|---|
| 5.3 / TASK-016 | 主仓同步面 3 项 | **aria 子模块合并 + 双推** |
| 5.4 / TASK-017 | i18n translated-from ×3 | **主仓 gitlink + VERSION + README** |

⇒ 违 `DUAL_LAYER_SPEC.md` 编号不可变约束 (正确做法 = 末尾追加, 或保留编号标 CANCELLED); **五份已 commit 的 R1 报告按旧含义引用 TASK-016/017, 现全部静默错位**; 且我在同一段声称遵守了该约束。

---

## §4 四项待裁 (均非 AI 可裁)

### Q1 — 闸门怎么收 (核心)

`max_rounds = 4`, 已跑 2 轮, **配额未耗尽**。但拐点判据已双向点亮。四条路:

| 选项 | 内容 | 代价 |
|---|---|---|
| **A (建议)** | **停止逐条补丁, 按规律重做组 5 一次** —— 2C + 8M 集中在组 5 (TASK-015~021); 组 1–4 两轮均未被指出实质问题, 原样保留。重做后跑 R3 只审组 5。 | 一次重写 + 一轮限定审计 |
| B | 原班五席跑 R3 | 按 83%/62% 规律预期再生成约等量缺陷; 两条成文判据均反对 |
| C | 换 2 席新鲜眼睛, 镜头限定「块间交叉一致性」+「每条机械断言在健康常态下应是什么值」 | tech-lead 的建议; 比 B 便宜, 但不解决「补丁法」本身 |
| D | 接受当前结论进 Phase B (`converged: false, overridden_by_user: true`) | 2 条 Critical 带进 Phase B; 其中 C1 是 Rule #10 违规 |

> **AI 立场**: 建议 A。理由不是「省事」而是: 2C + 8M 全部集中在组 5, 且三席从三个轴都指向「组 5 是按错误维度 (文件数) 枚举出来的」—— 重写一次比逐条补 10 处便宜, 也不会再制造接缝。**但停轮/降轮不是我能定的 (Rule #10), 故列此单。**

### Q2 — TASK-016 (绕闸门) 怎么处置

| 选项 | 内容 |
|---|---|
| **(a) 建议** | 删除 TASK-016, 委派 `phase-c-integrator` C.2.5; tasks.md 只留时序约束 |
| (b) | 保留 TASK-016, 但须 owner 显式记录一次「本 change 的子模块合并不走 phase-c-integrator」的豁免 (Rule #10 要求成文) |

### Q3 — Rule #6 AB 的门范围 (Rule #10 门收缩问题)

实读 `AB_TEST_OPERATIONS.md:397` / `:483`: **state-scanner 属 Tier 1 P0「每次发版必测」**。而我的 TASK-013 把 AB 缩到 `SKILL.md:176` 单个 hunk (M / 6h)。

另: 我引的三条「发版前结果判据」实为**场景 3 全量回归**的判据 (28 Skills / ~$14 / 6-8h), 且「with_skill 优于 without_skill」根本不在发版前清单里 (在「新增 Skill 后」清单); 两次先例的单 skill Rule #6 run **均无 summary.yaml**。

| 选项 | 内容 | 代价 |
|---|---|---|
| (a) | 单 hunk AB, 判据改为与单 skill run 相称的那几条 | M/6h; 但「Tier 1 每次发版必测」被缩而**须成文披露** |
| (b) | 按 Tier 1 跑全量 | 6-8h / ~$14 |
| (c) | 单 hunk + 显式成文降级 lane (写进 convention, 供后续复用) | M/6h + 一次 convention 修订 |

### Q4 — 双推授权 (AD10)

TASK-016/017 授权 **AI agent 无 owner 触点**向两个共享 master 双推。与 memory `feedback_sync_instruction_not_push_authorization` 及 AD10「唯一人类参与点 = merge 签字」相反。21 个任务里**零个 `agent: owner`**。

| 选项 | 内容 |
|---|---|
| (a) | 合并/双推任务标 `agent: owner`, AI 只准备不执行 |
| (b) | AI 可执行, 但每次推前须显式确认 (本 session 的实际做法) |
| (c) | 授权 AI 在本 change 范围内自主双推 (须成文) |

---

## §5 已由 AI 自行处置的项 (留痕请复议)

1. **给 aria-plugin #133 补评论**把 `collision.py` 三处 `_TERMINAL` 纳入 (R1/tech-lead F5: 原 Spec 声称「已开 #133」而该 issue 对 collision 零命中 ⇒ 范围纪律论证建立在不存在的覆盖上)。经三席独立核实评论确已落地。
2. **开 aria-plugin #134** (`test_collision.py` sys.path 顺序倒置, 破 70 天) 并标 `in_scope: false` 不并入本 Spec。
3. **未启动 [3]** (`secret-guard-per-segment-evaluation` R4) —— 该 Spec 是双子星终端 (`bfe8285d` / `simonfishgit`) 的在飞轨, Layer L 无其 claim (claim 挂在另一个名字上 ⇒ 认领机制对此不告警, Aria #174 盲区)。是否可动、那个终端是否还开着, 只有 owner 能判。

## §6 尚未处置、建议开 issue 的一项

**tech-lead N5 (修实例不修类)**: Critical-1 的根因就在 `CLAUDE.md:81`「发布同步面」那一行 —— 它同时犯了本 Spec 诊断出的全部三个错 (aria 侧按文件计 / 漏 CLAUDE.md 自己 / 「root README badge」漏 `Plugin Version:` 行), 并断言两条 custom check 是机械兜底 (实为结构性失明)。

本 Spec 的一次性 grep 会随 Spec 归档离场, 下次原样重犯。**而这次没开 issue** —— 与 #133 / #134 的处置形态不一致。建议开号。

---

## 跨引用

- R1 五份报告: `.aria/audit-reports/post_planning-R1-1786178267137-linked-issue-normalization-*.md`
- R2 五份报告: `.aria/audit-reports/post_planning-R2-1786182330124-linked-issue-normalization-*.md`
- 产物: `openspec/changes/linked-issue-normalization/{tasks.md,detailed-tasks.yaml}` @ `3fc6f3f`
- 同 session 另两起跨仓归属转交: `.aria/decisions/2026-08-08-credential-rotation-ownership-transfer-to-aether.md` (Aether #283) + silknode waiver 拆分 (SilkNode #979 / Aria #175)

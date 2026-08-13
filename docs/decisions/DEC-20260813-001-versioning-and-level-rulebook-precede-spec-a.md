# DEC-20260813-001 — 定档规则书先修, Spec A 的版本/Level 定档随后

> **裁定人**: owner (2026-08-13, 经 `AskUserQuestion` 两轮 —— 第一轮 owner 要求「大白话」后重述, 第二轮作出裁定)
> **触发**: Spec A `premerge-gate-branch-existence` post_spec R5 (`converged: false`, 6 条 `blocks_phase_b`) 揭示
> **两个定档前置的题面本身是错的** —— 版本选项集被 AI 从三收窄到二, Level 四条件只上呈了其中一条
> **状态**: Approved — 待 Phase A.1 起草新 change
> **关联**: [DEC-20260812-001](./DEC-20260812-001-premerge-gate-spec-split.md) · aria-plugin [#137](https://forgejo.10cg.pub/10CG/aria-plugin/issues/137) ·
> [handoff 2026-08-13](../handoff/2026-08-13-nine-rounds-two-specs-and-narrowing-the-owners-choices.md) §6.1

---

## 1. 裁定本体 (四条)

| # | 裁定 | AI 的建议 |
|---|---|---|
| 1 | **版本定档: 不在 PATCH/MINOR/MAJOR 三档里选, 而是「先修规则书再定档」** | AI 未给推荐 (刻意 withhold, 见 §4) |
| 2 | **Level 定档: 等版本轴落地后再裁** | 同 |
| 3 | **`LEVEL_GUIDE.md` 模块地图过期这条类级缺陷: 并入同一 change, 不单独开 issue** | ❌ AI 上呈的三个选项里**没有**这一个 (见 §4 第 2 条) |
| 4 | **范围 = 一个 change, 版本轴 + Level 轴一起修** | AI 上呈三选项, owner 选最彻底的一个 |

**净效果**: Spec A 的 Phase B **仍被阻断**, 但阻断点从「两个待裁项」转为「一个待起草的前置 change」。
A 的 R5 六条 `blocks_phase_b` 中的 **M-4 (Level 条件① 自造谓词) 与 M-5 (版本定档未过 SOT)**
由本 DEC 承接 —— 它们不再是「A 内部要修的措辞」, 而是**规则书本身的缺陷**, A 无法在自己范围内闭合。

---

## 2. 裁定依据 (逐字 SOT, 主 loop 独立实测复核, 非采信 agent 转述)

### 2.1 版本轴 — 两套分法打架, 且无优先级规则

| SOT | 逐字 | 对 A 求值 |
|---|---|---|
| `CLAUDE.md:79` | 「SemVer。Aria 约定: 新增 Skill / Skill 架构重构 = MINOR+; 文档更新 / **bug 修复 = PATCH**」 | A 既非新增 Skill, 又已自答「架构变更 = NO」 ⇒ 落 **PATCH** 桶 |
| `version-management.md:5` | 「> **Based on**: Semantic Versioning (semver.org)」 | 引用并入 SemVer 的**兼容性排序轴** |
| `version-management.md:17-19` | 「补丁版本 (Bug修复、文档修正) / 次版本 (新功能、向下兼容) / 主版本 (重大变更、可能不兼容)」 | 三档带兼容性限定词 = 排序轴; A 加了新功能且向下兼容 ⇒ **MINOR**, 轮不到 PATCH |
| `version-management.md:52-55` | §2.2 MINOR 触发条件, `:55` = 「功能增强（向下兼容）」 | 字面命中 ⇒ **MINOR** |
| `version-management.md:67-70` | §2.3 PATCH 触发条件, `:70` = 「Bug 修复」 | 字面命中 ⇒ **PATCH** |
| `version-management.md:34-40` | §2.1 MAJOR 四条触发条件 | **逐条零命中** |
| `CLAUDE.md:35` | 「向后兼容 (**破坏性变更**须 MAJOR)」 | 闸门由恒 green 翻 fail = 行为面破坏 ⇒ **MAJOR** |

⇒ **`CLAUDE.md:79` 按「改动的性质」分桶, `version-management.md` 按「兼容性」排序 —— 两套分法对 A 给出不同答案,
而 SOT 未规定谁特化谁、冲突时听谁。** 这是规则书本身的缺陷, 不是 A 的缺陷。

**两条附带实测 (均为本轮新发现, 须在新 change 内一并处置)**:

1. 🔴 **Spec A `proposal.md:1077` 用来排除 MAJOR 的引文不存在**: 逐字「CLAUDE.md 版本规则把 MAJOR 系于
   **破坏性契约变更**而非行为修正」—— 实跑 `grep -c '契约' CLAUDE.md` = **0**。「契约」二字是被插入的限定词,
   而正是它在排除 MAJOR。真实原文 (`CLAUDE.md:35`) 只有「破坏性变更」。
   ⇒ 无论最终定哪档, 这句无出处的引文必须改正, 不得留在文档里。
2. ⚠️ **AI 的第一版题面写「SOT 无优先级规则 (`precedence_rule_exists: false`)」是错的** —— 被本轮对抗复核推翻,
   主 loop 实测确认: SemVer 是经 `version-management.md:5` **引用并入**的, 它自带排序。第一版题面因此把
   「两套分法打架」错误呈现为「三个平等的桶随便挑」。**该错误在本 DEC 出具前已更正并重新上呈 owner。**

### 2.2 Level 轴 — 四条件里三条判不了

`LEVEL_GUIDE.md:156-162` 逐字: 「跨模块条件 (满足任一): ① 涉及 2 个及以上模块 / ② 修改 `shared/` 目录 /
③ 需要 API 契约变更 / ④ 影响多个子模块」+ 「跨模块 → **自动提升为 Level 3**」(无成本收益余地)。

| 条件 | 求值 | 病灶 |
|---|---|---|
| ① | **UNDECIDABLE** | `:129-133` 规定三步检测法 (关键词 / 路径前缀 / 跨模块) 但**未规定两面冲突时听谁**。关键词面命中 backend(Python·API) + standards(Skill·文档·规范) + shared(契约·Schema) ⇒ ≥2 ⇒ YES; 路径面四条 glob (`mobile/**` `backend/**` `shared/**` `standards/**`, `.claude/**`) 对 `aria/skills/**` **零命中** ⇒ 判不出 |
| ② | **NO** | 四条里唯一站得住的 NO (本仓无 `shared/` 顶层目录, 实测 `ls -d */`) |
| ③ | **UNDECIDABLE** | 原文七字「需要 API 契约变更」**无「破坏性」限定**, 而 A `:20-21` 自承「这些**是**契约变更」⇒ 照字面 YES; 判 NO 须往条件里插一个原文没有的词 (memory `exact-exception-condition` 禁止的正是该动作) |
| ④ | **UNDECIDABLE** | 「子模块」一词全文仅此一处, **无定义**; 按 git submodule 读 ⇒ NO, 按「模块」读 ⇒ 继承 ① |

⇒ **判 Level 2 需要四条全 NO, 今日只拿到一条。「维持 Level 2」不是被推翻, 是从未被求出来过。**

### 2.3 类级缺陷 — 地图相对 meta-repo 已失效

`aria/skills/spec-drafter/LEVEL_GUIDE.md` 文件头 `版本: 1.0.0 / 最后更新: 2025-12-23`; 其 `:266` 示例逐字把
新建 Skill 的影响范围写作「单模块 (`.claude/skills/`)」。实测 `ls .claude/` = `local.md` / `settings.json` /
`trigger-rules.json` —— **无 `skills/`**; 今日 Aria 的 skill 全部住在 `aria/skills/**`。

⇒ **本仓每一个 aria-plugin 变更在 Level 路径面上恒零命中**, 只能靠关键词面 —— 这不是 Spec A 一个 Spec 的问题,
是会复发到每一个未来 Spec 上的类级缺陷 (memory `fix-the-class`)。

⚠️ **且只改 glob 不够**: 地图只是 ① 的一半。改对 glob 后, 关键词面与路径面仍可能给出相反结论, 而**仲裁规则依然缺席**;
③ 缺限定词、④ 无定义更与地图无关。⇒ 这正是 owner 裁定「两轴一起修」而非「顺手改地图」的原因。

---

## 3. 新 change 的范围 (裁定 4 的展开)

**一个 change, 覆盖两条轴**, 跨三个仓:

| 轴 | 落点 | 要解决的 |
|---|---|---|
| 版本 | `CLAUDE.md` (主仓) + `standards/conventions/version-management.md` (子模块) | `CLAUDE.md:79` 与 `version-management.md` 的关系 (谁特化谁 / 冲突时听谁); `:79` 两桶分类法对「既是 bug 修复又新增能力」这类变更的归属 |
| Level | `aria/skills/spec-drafter/LEVEL_GUIDE.md` (子模块) | 模块地图对 meta-repo 形态的更新; 关键词面 vs 路径面的**仲裁规则**; 条件③ 是否含 additive; 条件④「子模块」的定义 |

**已知连带**:
- 改 `aria/` 内容 ⇒ **触发 Rule #6 benchmark** (`LEVEL_GUIDE.md` 是 spec-drafter 的处方性向导 ⇒ 按 CLAUDE.md 规则 #6
  判据表第三行「处方性 · 套件覆盖外 (典型: authoring 向导)」处置: 点名行为 + 建可证伪定向 fixture + 套件缺口开 issue,
  缺一照跑 —— ⚠️ 该缺口已有在案 issue aria-plugin #117「AB 测试集缺 authoring 维度」);
- 跨三仓 ⇒ 发版同步面 + 子模块本地 merge 双推 (CLAUDE.md 硬约束 1/2)。

---

## 4. Rule #10 留痕 — 本轮 AI 的流程判断, 请复议

1. **AI 刻意不给版本推荐档位** (`recommendation_withheld_reason` 三层理由): 判断依据是「本仓上一次编排层错误
   正是把选项集从三收窄到二, 此时再给推荐会把同一风险重演」。**这个『不推荐』本身也是一次 AI 的流程判断** ——
   对抗复核席位当场指出: withhold 不是中立动作, 它把「三档之间有序」这一 SOT 已供给的信息从 owner 眼前移除了。
   ⇒ 第二版题面已补上排序轴。**请复议「刻意 withhold」这个做法本身。**
2. 🔴 **AI 在模块地图那题上又收窄了一次选项集**: 上呈的三个选项是「只记录 / 开 issue / 顺手修地图」,
   **而 owner 实际选中的「并入规则书 change」不在其中** —— 是 owner 追问「哪个最彻底?」才逼出来的。
   ⇒ 这是本轨第 18 条编排层错误, 且**与前 9 条同族** (替 owner 缩小决策空间)。
   形状略有不同: 前 9 条是漏掉 SOT 允许的选项, 这次是**没想到把两个同根问题合并**这个更优解。
3. **本 DEC 由 AI 起草, 裁定内容取自 owner 的四次选择**; 依据段的每条 SOT 引文均由主 loop 独立实跑复核
   (未采信 agent 转述), 复核方法与结果见 §2 各表。

---

## 5. 未决 (交下一轮)

- 🔴 **新 change 自身的 Level 定档会撞上它正要修的那个歧义** —— 它改 `LEVEL_GUIDE.md` (Skill 内容) ⇒ 关键词面
  又同时命中 standards + backend ⇒ 条件① 又是 UNDECIDABLE。**这个循环无法靠推导打破, 须 owner 单裁一次**
  (建议连同新 change 的 proposal 一并上呈);
- 新 change 的 `change_id` 待定;
- Spec A 的其余 4 条 `blocks_phase_b` (M-1 `CLAUDE.md:113` 同步归属 / M-2 与 B 的 TASK-013 交付物重叠 /
  `SC-A-doc` 锚点定位规则未推广 / knowledge-manager 一条) **不由本 DEC 承接**, 仍在 A 内待处置;
- A 侧 `max_rounds` 6 已用 5, **余 1 轮** —— 按 handoff §6.1, 在本 DEC 落地的前置 change ship 前**不应**用掉它
  (R6 与 R5 的条数在定档前提变化后不可比)。

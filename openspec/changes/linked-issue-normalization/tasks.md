# Tasks — `linked-issue-normalization`

> **Spec**: [proposal.md](./proposal.md) | **审计轨**: [audit-trail](../../../.aria/audit-reports/linked-issue-normalization-audit-trail.md)
> **Level**: 3 | **Status**: 📝 **A.2 + A.3 R2-fix (组 5 按规律重做)** (2026-08-08) — post_planning R1 5/5 REVISE·FAIL → R1-fix → R2 2 PASS/3 REVISE·FAIL; **owner 裁定停止逐条补丁, 按规律重做组 5**; 待 R3 (只审组 5)
> **Scope**: **跨两仓** — `aria` 子模块 (代码+测试+文档+版本) + 主仓 (gitlink + 版本引用面 + Spec)
> **ship target**: aria-plugin **v1.66.0** (MINOR — 行为面扩大)

> **为什么本 Spec 从 Level 2 升 Level 3**: Q5 裁定 (owner 2026-08-06) 要求 `SKILL.md:176` 的 hunk **照跑 AB, 不走 substitute**, 并写明「本条须进 `tasks.md` 作为独立任务」。而本 Spec 当时是 Level 2 (按 CLAUDE.md 只产出 `proposal.md`) ⇒ **owner 亲裁的 Rule #6 处置唯一落地载体不存在** (R3′ 两席独立命中)。本文件解决它 —— 见 **4.1**。

> **📌 编号不可变约束 — 一次违反的更正 (2026-08-08)**
>
> **R1-fix 时我在此处写过「只追加 5.5–5.8, 不改动任何既有编号 (5.1–5.4 语义与编号均保持)」—— 该声明不成立, 现撤回。** 对 `a52ab81` 实测: `5.3` 由「主仓同步面 3 项」改指为「aria 子模块合并 + 双推」, `5.4` 由「i18n translated-from ×3」改指为「主仓 gitlink + VERSION + README」(即 `TASK-016`/`TASK-017` 两个 ID 被原地改指), 违 [`DUAL_LAYER_SPEC.md`](../../../aria/skills/task-planner/DUAL_LAYER_SPEC.md) §编号不可变约束; 且五份已 commit 的 R1 报告按旧含义引用这两个 ID, 造成静默错位。post_planning R2 / tech-lead N6 命中。
>
> **本轮 (R2-fix) 起严格执行该约束**: 组 5 的重做**不改动任何既有编号的含义** —— `5.2`–`5.8` 全部**保留编号并标 `(CANCELLED)`** 且注明被谁取代, 重做后的任务**追加为 `5.9`–`5.14`**。`TASK-015`–`TASK-021` 同样保留并标 cancelled。
>
> **⚠️ 二次更正 (post_planning R3, tech-lead X5 + knowledge-manager)**: R2-fix 时我在此写「R1/R2 两轮共十份报告对旧 ID 的引用**继续成立**」—— **该句对五份 R1 报告为假, 现撤回**。R2-fix 冻结的是 **R1-fix 之后**的语义, 而 R1 报告 (`post_planning-R1-*`) 引用的 `TASK-016` 是**gitlink 任务**、`TASK-017` 是**i18n 任务**。**同一段落、同一形状、第二次** —— 撤回一句假自陈的同时又立了一句。
>
> **⇒ old → new 重映射表 (读旧报告时按此换算)**:
>
> | ID | R1 报告 (`a52ab81` 语义) | R2 报告 (`3fc6f3f` 语义) | 现状 (`2cf2569`+) |
> |---|---|---|---|
> | `TASK-015` | aria 子模块 5 文件 bump | 同左 | cancelled → `TASK-022` |
> | `TASK-016` | **主仓同步面 3 项 (gitlink/VERSION/badge)** | **aria 子模块合并 + 双推** | cancelled → `TASK-028` (合并+gitlink) |
> | `TASK-017` | **i18n translated-from ×3** | **主仓 gitlink + VERSION + README** | cancelled → `TASK-023` + `TASK-028` |
> | `TASK-018` | — (不存在) | 主仓 i18n ×3 | cancelled → `TASK-023` |
> | `TASK-019` | — | CLAUDE.md 两处 | cancelled → `TASK-023` |
> | `TASK-020` | — | 零命中断言 | cancelled → `TASK-024` |
> | `TASK-021` | — | sc-baseline 处置 | cancelled → `TASK-025` |
>
> **A.2 首次重写的说明 (仍然成立)**: 2026-08-08 首次把本文件由 R3′ 手术产物 (`B-1..B-6` 表格) 改为 checkbox 形态时, 前一版 `B-n` 从未被任何 `detailed-tasks.yaml` 的 `parent` 引用 (该文件此前不存在), 故无引用被破坏。
>
> **顺带修掉的机械盲区**: 表格形态使 `handoff_autofill` 的 unfinished 扫描完全看不见本 Spec (2026-08-08 handoff §2 实证: 159 条 unfinished 里本 Spec 零条)。checkbox 形态后该盲区对本 Spec 消失; **该 backstop 对非 checkbox 形态 tasks 的失明本身是插件侧待修项**, 不在本 Spec 范围。

---

## 范围边界 — 本文件到哪里为止 (post_planning R1 / tech-lead F3 要求显式声明)

| 阶段 | 归属 | 理由 |
|------|------|------|
| Phase B 实施 + 组 1–4 | **本文件** | change 自身的交付物 |
| **版本引用面编辑 + 双向断言 (组 5)** | **本文件** | 版本号本身是本 change 的交付物 (proposal §Impact 已列) |
| **aria 子模块合并 + 双远程推送** | **`phase-c-integrator` C.2.5**, 不在本文件 (**owner 裁定 2026-08-08**) | R1-fix 曾把它写成 TASK-016 手工步骤 ⇒ **绕开两个默认开的闸门** (`pre_merge_gate.enabled=true` Rule #8 + `submodule_gate.mode="block"`), 而该 Skill (SKILL.md:242) 本就建模子模块合并。R2/tech-lead N1 判为 Rule #10 违规 |
| **Phase C**: PR 创建 / **pre-merge gate (Rule #8)** / merge | **`phase-c-integrator`**, 不在本文件 | 通用流程, 由该 Skill 的 C.2.4 承担 (CI passing + main 无 in-flight run); 本文件不复述其判据 |
| **Phase D**: cycle 进度更新 / **Spec 归档** / **周期 handoff (Rule #9)** | **`phase-d-closer`**, 不在本文件 | 同上; 归档门会消费本文件全部 checkbox 状态, 故组 5 必须真做完而非声称 |

**⚠️ 组 5 与 Phase C 的交接**: 本文件只做**版本面编辑 + 双向断言** (5.9–5.11), 断言必须在**交付 Phase C 之前**通过 —— 这样任何计数错都在**可回退点之前**发红 (R1-fix 曾把断言排在合并双推之后, R2/tech-lead N4 命中)。断言过后由 **5.13** 交付给 `phase-c-integrator`: 由它做 aria 子模块合并 + 双推 + 主仓 gitlink bump + PR + pre-merge gate。**gitlink 必须指向合并后的 `master` SHA, 这条约束随交接一并移交, 由 C.2.5 的既有机制保证。**

---

## Task Group Overview

| Group | 主题 | 依据 |
|-------|------|------|
| **1** | 测试先行 (RED) — 17 条 SC 全量落盘 | proposal §Success Criteria |
| **2** | 实现 (GREEN) — 归一谓词 + 导出单元 + 守卫 | proposal §What Changes 五步 · D7 · D9 |
| **3** | 文档同步 ×3 (两处 substitute + 一处 AB) | proposal §Impact · rule6_note 逐 hunk 表 |
| **4** | Rule #6 AB (⛔ 不豁免) | Q5 裁定 (owner 2026-08-06) |
| **5** | 回归 + **版本引用面 (按引用点而非文件数)** + 双向断言 + 留证工件处置 + 交付 Phase C | proposal §Impact + post_planning R1/R2 五条 Critical |

**排序依据**: 组 1 → 组 2 是 RED-first (SC 的 baseline-failing 状态已于 A.1 实跑留证)。**例外: 1.6 (SC-12) 反向依赖 2.1** —— 被测函数 `normalize_linked_issue` 在 2.1 之前不存在, 测试连 import 都不成立, 故 1.6 排在 2.1 之后。组 3 依赖 2.2/2.3 (**3.1 与组 2 同文件, 必须串行**)。**3.3 必须早于 4.1** (AB 测的是该 hunk 的行为影响)。组 5 gate 在组 1–4 全绿之后, 内部按 **5.1 → 5.9 → 5.10 → 5.11 → 5.15 → 5.13** 串。
**⚠️ R4-fix 调整了 5.13 与 5.15 的顺序**: 子模块合并 + gitlink bump (5.15) 必须**先于**主仓 PR (5.13) —— 否则主仓 PR 里 gitlink 未变, `phase-c-integrator` C.2.4.5 只会输出 `OK: aria unchanged`, 该 bump 全程无 PR、无闸门 (与 memory `feedback_submodule_pointer_post_merge_bump` 的顺序相反; R4/delegation-lens Major) (`5.2`–`5.8` 已 CANCELLED, 见组 5 段首)。**5.12 例外: 可在 2.3 之后任意时点执行** (`sc-baseline` 脚本自 2.2 落地即恒红, 不必等发版)。**5.14 例外: 与 4.1 同批, 早于 5.13**。依赖字段以 `detailed-tasks.yaml` 为准。

---

## 1. 测试先行 (RED) — `aria/skills/state-scanner/tests/test_release_by_track.py`

> 宿主为既有文件; **既有 6 条测试逐字不改**。⚠️ **锚定方式改为内容锚而非行号锚** (post_planning R1 minor): 本组会往同文件插入用例必致行号位移, 故判据是「既有 6 个 test 方法名及其函数体逐字未变」(用 `git diff` 核), 不是「`:206-247` / `:527-575` 区间未变」。
>
> 每项括注为该项贡献的**子用例场景数**, 全组加总 = **45**, 与 proposal §Impact 的逐条推导独立吻合 (两处任一变动须同批重算)。**「子用例场景」≠ unittest `Ran N` 计数的 test 方法数** —— 一个 test 方法可含多个场景 (本文件既有 `test_invalid_shapes_and_paths` 即 1 方法 4 场景), 故验收**不得**用 `Ran` 数换算, 见 5.1。

- [ ] 1.1 SC-1 / SC-1b / SC-2 / SC-3 / SC-4 — 跨族两两配对 + 三个切分点各自 strip + 不同仓负控 + org 不参与 + int 十进制比较 **(13)**
- [ ] 1.2 SC-5 / SC-5b / SC-5c — basename 轴三态: 截断型**不**归一 (已知限) / 分隔符型 `./_→-` 归一 / 段内空格**不**译码 **(5)**
- [ ] 1.3 SC-6 / SC-6b / SC-10 — 不可解析值退回原串精确比较 + `number_str` 边界五类 + **一条畸形毒不死整批** **(15)**
- [ ] 1.4 SC-11 / SC-13 / SC-15 / SC-14 — 切分方向双轴 (`#` 取最后 / `/` 取最后) + `casefold` 维度 + `number` 相等这一必要条件 **(8)**
- [ ] 1.5 SC-9 — 命中条目回显**未归一原始串** **(1)**
      > ⛔ **治理约束**: 本条 R1′ 曾被移出、R3′ 恢复。Q1 裁定「自己那一侧永不补」后, 回显对方原串成为 D2 fail-toward-reporting 的**唯一**缓解, 且它是输出里唯一携带 `org` 的通道。**不得再次移出。**
- [ ] 1.6 SC-12 — 导出单元返回契约: 可解析返回 `(basename, number)`, 三类不可解析各返回 `None` **(3)**
      > ⚠️ **本条是组 1→组 2 RED-first 排序的唯一例外**: 依赖 **2.1** (被测函数在此之前不存在)。

## 2. 实现 (GREEN) — `aria/skills/state-scanner/lib/collision.py`

- [ ] 2.1 导出纯函数 `normalize_linked_issue(value: str) -> tuple[str, int] | None` — §归一规则五步; `None` 与规则 4 的不可解析枚举一一对应 (D9)
- [ ] 2.2 `linked_issue_overlaps` 内部比较谓词切换为归一键 `(normalize(basename), int(number))` — **签名与返回 schema 不变** (D6, 限本 Spec 变更面)
- [ ] 2.3 解析守卫与异常隔离 — 不含 `#` 先判不可解析 (不得无守卫拆分) · `number_str.isascii() and number_str.isdigit()` 谓词 · `int()` 必包 `try/except ValueError` · `limit = sys.get_int_max_str_digits()` 且**仅当 `limit > 0`** 时比长度 (D7 四条)

## 3. 文档同步

- [ ] 3.1 `lib/collision.py` docstring 同步 — 说明按归一后 `<repo>#<n>` 比较、org 不参与; **措辞不得暗示「已穷尽核实 / 已覆盖全部别名」** (走 substitute)
- [ ] 3.2 `lib/claim_schema.py` `ClaimRecord.linked_issue` 字段文档两处失准同批修 (SAME → same normalized key; active → 实际跳的是 `_TERMINAL` 且不含 `yielded`) (走 substitute)
- [ ] 3.3 `skills/state-scanner/SKILL.md:176` 括注 — 补「(按归一后的 `<repo>#<n>` 比较, org 不参与)」

## 4. Rule #6 AB (⛔ 不申请豁免、不走 substitute)

- [ ] 4.1 用 `/skill-creator` 对 **3.3 的 hunk** 照跑 AB — 时点: **3.3 实施之后、组 5 发版之前**
      > **判据 (不得只判「跑了」)**: 按 `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` 发版前清单 —— (a) `with_skill` 表现优于 `without_skill`; (b) **无 `WITHOUT_BETTER` verdict** (有则必须修复); (c) 与上次结果比对无回归; (d) `summary.yaml` 已生成并审查。
      > **若判定该 hunk 落在套件覆盖外**: 按 CLAUDE.md Rule #6 表第三行走**三件套** —— 点名行为 + 建可证伪定向 fixture + 套件缺口开 issue (参 aria-plugin #117 / #127); **三件缺一则照跑, 不得静默豁免** (Rule #10)。

## 5. 回归 + 版本引用面 + 双向断言 + 留证处置 + 交付 Phase C

> **📌 本组已于 2026-08-08 按 owner 裁定「停止逐条补丁、按规律重做」整组重derive。**
> `5.2`–`5.8` **保留编号并标 CANCELLED** (编号不可变约束; R1/R2 十份报告对 `TASK-015`–`TASK-021` 的引用继续成立)。
>
> **为什么整组重做而不是继续补**: post_planning R2 五席测出 2C + 11M, 对比 R1 的 3C + 12M **基本持平**, 且 fix 引入占比经两席独立测算为 **83% / 62%** (均 >1/2) ⇒ 边际产出已转负 (memory `feedback_audit_marginal_return_goes_negative` + `feedback_stop_adding_rounds_when_major_count_flattens` 双向点亮)。三席从三个不同轴 (fix 改坏了什么 / 缺陷迁到哪层 / 同形状扫没扫完) 都指向同一结论: **组 5 是按错误维度 (文件数) 枚举出来的, 逐条补丁只会沿接缝再生产缺陷。**
>
> **重做的维度**: 发版同步面的正确单位是**版本引用点**, 不是文件数; 且**版本史类文件 (append-only 账本) 的不变量与普通文件不同** —— 前者是「头部当前版本行 == SOT」, 后者是「旧值零命中 + 新值计数匹配」。R1-fix 把两类混在一条零命中断言里, 造出一个恒红 (R2/tech-lead N2)。

### 现行 — 5.1

- [ ] 5.1 全量回归 — `cd aria/skills/state-scanner/tests && python3 run_tests.py` 报 **OK 且 0 failures/errors** (基线 **1322** tests; 跨 skill 基线 **9 OK / 累计 1698**); 跨 skill `bash aria/skills/run_all_tests.sh` **0 FAIL**
      > ⛔ **不得用 `Ran N` 数换算场景数**: 45 是**场景数**, `Ran` 数的是 test 方法数 (既有 `test_invalid_shapes_and_paths` = 1 方法 4 场景)。场景齐备性判据 = **逐 SC 清单核对 17 条 SC 的场景全部落盘**, 与 `Ran` 数正交。
      > ⚠️ 环境陷阱: 单模块模式与 pytest 对 `test_collision.py` 会给 ImportError —— aria-plugin **#134** 的既有 bug (破 70 天), 非本 change 回归。验收一律以 `tests/` 内**全量** `run_tests.py` 为准。

### CANCELLED (编号保留, 勿复用) — ⚠️ 故意**不用 checkbox 语法**

> **为什么不用 `- [ ]`**: `DUAL_LAYER_SPEC.md:258` 的示例用 `- [ ] X.Y (CANCELLED)` 保留编号, 但**与归档门互相拆台** —— 实跑 `spec_complete.py --gate` 会把它们计入 unchecked (R2-fix 时实测 `27/27 unchecked`), 完工后恒为 `7/27` ⇒ 那 7 条永远不能合法勾 `[x]` ⇒ **归档门的 tasks 分支永久失效, 只剩 Status 分支 = 声称**; `handoff_autofill` 亦会永久误报 7 条 phantom。故本文件用**加粗删除线**保留编号而不进 checkbox 计数 (post_planning R3, 三席独立命中)。插件侧该冲突已记, 见下方指针。

- **~~5.2 aria 子模块 5 文件 bump~~ **(CANCELLED)** → 由 **5.9** 取代 (按引用点重derive, 补 `marketplace.json` 第二个 version 字段)
- **~~5.3 aria 子模块分支合并 + 双推~~ **(CANCELLED — owner 裁定 2026-08-08)** → **委派 `phase-c-integrator` C.2.5**, 见 **5.13**。理由: 手写它绕开 `pre_merge_gate` (Rule #8) 与 `submodule_gate=block` 两个默认开的闸门 (R2/tech-lead N1, Rule #10 违规)
- **~~5.4 主仓 gitlink + VERSION + README 两处~~ **(CANCELLED)** → 版本面归 **5.10**; gitlink 归 **5.13** (随合并一并移交)
- **~~5.5 主仓 i18n README ×3~~ **(CANCELLED)** → 并入 **5.10**
- **~~5.6 CLAUDE.md 两处版本引用~~ **(CANCELLED)** → 并入 **5.10**
- **~~5.7 版本引用点归零机械断言~~ **(CANCELLED)** → 由 **5.11** 取代。原条三处坏: 含 `aria/VERSION` (append-only 发布账本) ⇒ **恒红**; 只断言旧值缺席不断言新值出现 ⇒ 写错新版本号免疫; 排在合并双推**之后** ⇒ 只可能在不可回退点之后发红
- **~~5.8 sc-baseline 脚本处置~~ **(CANCELLED)** → 由 **5.12** 取代 (补归档后 `FATAL` 分支)

### 现行 — 5.9 起 (取代上方 CANCELLED)

- [ ] 5.9 **aria 子模块版本面** bump 到 v1.66.0 — **按引用点枚举, 不按文件数**
      > `.claude-plugin/plugin.json` (版本 SOT, 1 点) · `.claude-plugin/marketplace.json` (**2 点**: `:3` 与 `:16` 两个 `version` 字段) · `README.md` · `VERSION` (**append-only 发布账本** —— 只改头部「当前版本」行 + 追加本次发布注, **历史行原样保留**) · `CHANGELOG.md` (**追加**条目, 历史保留)
      > CHANGELOG 与 README 措辞: **不得写成「已覆盖全部别名」** —— basename 截断轴是成文已知限, 写错等于对外抹掉它。
      > MINOR 而非 PATCH (行为面扩大)。

- [ ] 5.10 **主仓版本引用面** — 14 个引用点, 逐点改
      > `VERSION` :24 子模块表行 (1) · `README.md` badge + `Plugin Version:` 行 (2) · `README.{zh,ja,ko}.md` 各 `translated-from` + badge + `Plugin Version:` 行 (**9**) · `CLAUDE.md` 版本区间行 + 「版本:」行 (2)
      > i18n 按 #140 B 档: 正文无实质变更 ⇒ **只改这三处, 不重译正文**。
      > CLAUDE.md: **只改数字**。不得把本 Spec 设计术语写进去 (污染 AB baseline, aria-plugin #116); 「项目状态」段覆写非追加、预算 15-20 行 (`claude-md-hygiene.md`)。

- [ ] 5.11 **版本引用面双向 + 整仓差集断言** — **必须在 5.15 (合并/双推/gitlink) 之前通过**
      > **① 整仓差集 (fail-CLOSED, R4-fix 关键升级)**: bump 后对**全部 tracked 文件** grep 旧版本号 `1.65.5`, 命中集合**减去显式成文排除集**后必须为**空**。
      > 排除集 (逐条给理由, 成文): `aria/VERSION` + `aria/CHANGELOG.md` (append-only 版本史) · `.aria/audit-reports/**` (审计史) · 本 Spec 目录内的订正留痕行 (自述历史)。
      > ⛔ **任何不在排除集里的新命中即红**; 不许临时往排除集加条目凑绿, 加条目须同批写理由。
      > **为什么换掉文件白名单**: 白名单对**未来新增的版本引用点 fail-OPEN** (修实例不修类), 且逼人去数「两条 check 失明几处」—— R2-fix 写 7, 实为 **10** (漏计 CLAUDE.md 2 + VERSION 1)。整仓差集使这个数**不必算** (R4/completeness-lens 单点最优建议)。
      > **② 新值计数**: 普通引用文件里 `1.66.0` 出现次数 == 预期点数 (主仓 **14** + aria 侧 **4** = **18**)。只断言旧值缺席是**缺席断言**, 删行或写错新版本号都判绿。
      > **③ append-only 账本** (`aria/VERSION` / `aria/CHANGELOG.md`) 判据不同: (a) **全部**「当前版本」声明 == `plugin.json` **且** (b) **文件行数不减**。
      > ⚠️ (a) 写「**全部**」而非「头部」是因为 **`aria/VERSION:56-59` 有第二处当前版本声明** (`## 版本号` 围栏块), 实读 **`1.47.0`** —— 陈旧 18 版, 正是 aria-report **#158** 版本字段污染的那个冻结串。该块的陈旧属 pre-existing 缺陷, 不在本 Spec 范围, 但实施者须知道它存在。
      > ⚠️ (b) 用「行数不减」而非「旧值命中数 ≥N」: **R4 实测保留形态不一致** (`1.65.4` 0 次 · `1.65.3` 0 次 · `1.65.2`/`1.65.1`/`1.64.0` 各 1 次) ⇒ 任何基于旧值命中数的阈值都会对某些 bump **恒红**。R3-fix 写 ≥2、R4 中途写 ≥1, **同一处三次踩同一个坑** —— 每次都是在「修恒红」的编辑里造新恒红 (memory `feedback_fix_recurs_in_its_own_fallback_path`)。
      > **④** 同时跑**不带路径**的 `git status` 核验实际落地面与声称一致 (memory `feedback_scoped_git_add_splits_claim_from_landing`)。
      > **类级根因已开号**: `CLAUDE.md:81`「发布同步面」那行同款四错, 见 **Aria #177**。本任务只治本 change 的实例。

- [ ] 5.12 **`.aria/repro/sc-baseline-linked-issue-normalization.py` 处置** — 不得留成恒红
      > 该脚本 `:275-277` 断言那 8 条 SC 处于 **baseline-failing (红)**; 2.2 落地后它们转绿 ⇒ **恒红**。且它从 `proposal.md` **现场解析** (`:205-215` FATAL fail-CLOSED) ⇒ Spec 归档后**换一种恒红**。两条失效路径都要处理。
      > 两条路择一并在脚本顶部成文: **(a)** 加 post-implementation 模式, 断言那 8 条**已转绿**, 并把 baseline 结果冻成同目录存档 (需同时解决归档后解析路径问题); **(b)** 显式退役, baseline 结果冻成带 SHA 的存档报告、脚本移出 `.aria/repro/`, **同时修 `proposal.md:181/:219` 两处 artifact 指针**避免 dangling。
      > 恒红与假绿同为零信息量 (memory `feedback_false_green_dual_is_permanent_red`) —— 本 Spec 全程在打这个对偶, 不能自己留一个。

- [ ] 5.13 **交付 `phase-c-integrator`** —— **只委派 PR 与 pre-merge 闸门, 不委派合并动作**
      > **交出去的**: PR 创建 + **pre-merge gate (Rule #8, C.2.4: 本 PR CI passing + main 无 in-flight run)** + 主仓自身 PR 流程。这些**不在本文件复述判据**。
      > **⛔ 不交出去的 (改由 5.15 承载)**: aria 子模块的**合并动作本身** + 双推 + 逐远端 ls-remote + 主仓 gitlink bump。
      > **为什么这样切 (post_planning R3, 四席独立命中 Critical)**: R2-fix 曾把合并整体委派出去, 依据是「`phase-c-integrator:242` 本就建模子模块合并」—— **该引用是误引** (`:242` 实为 *Path coverage 评估*的执行上下文契约)。真实合并链 = C.2.4:253 → `branch-manager` merge action → `curl -X POST .../pulls/{n}/merge -d '{"Do":"merge"}'` (`branch-manager/SKILL.md:625-634`), **正是 CLAUDE.md 硬约束 1 对子模块明文禁止的服务端合并**; 且 `aria/skills/` 全仓对该约束**零处编码** (已开 aria-plugin **#136**)。⇒ 委派掉合并等于删掉计划里唯一的守卫。
      > **两件事正交, 不是二选一**: 「**谁执行合并**」(硬约束 1: 本地 vs 服务端) 与「**哪个闸门批准合并**」(Rule #8 CI 状态) 互不替代。R2/N1 把二者混成一件, owner 据此裁定的「删任务改委派」因此只解决了后者。本版**两者都要**。
      > 验收: (1) **5.15 已完成** (子模块已本地合并双推、主仓 gitlink 已 bump); (2) 交接时显式告知该状态。
      > ⛔ **真实阻塞 (R4/delegation-lens C2)**: `phase-c-integrator` **没有 gate-only 形态** —— C.2.4 的触发条件逐字是「即将调用 branch-manager merge action」, green 后 `:253` 直接调用它, 而 merge 的唯一实现是服务端 `Do: merge`。⇒ 「只要闸门不要合并」**在现有工具里不可实现**。**在 aria-plugin #136 落地前, 5.15 的合并只能由 owner 手工本地执行, pre-merge gate 需单独调用。**
      > ⚠️ **委派的闸门两条腿对本 Spec 都不触发且都失败为绿 (R4/delegation-lens C3, 已开 aria-plugin #137)**: (a) 两仓 workflow 的 `paths` 只覆盖 `issue-triage`/`docker` ⇒ `not_applicable` ⇒ PR CI 步跳过; (b) `pre_merge_gate.py:427` 的 `--main-branch` **缺省 `"main"` 而本项目是 `master`** ⇒ 实跑返回 `{"runs":[]}` RC=0 ⇒「main 无 in-flight」**恒真**。⇒ 调用时**必须显式** `--main-branch master` 并核验它真查到了 master。


- [ ] 5.14 **Rule #6 AB 门范围披露** (AI 建议走此路, **待 owner 确认**) — 与 4.1 同批, 早于 5.13
      > **事实**: `AB_TEST_OPERATIONS.md:396` 逐字为「Tier 1: 核心 Skills (**10 个**, 每次发版必测)」, state-scanner 在内; 发版前清单 `:545` 要求「Tier 1 Skills 全量 AB 测试已执行」。而 4.1 只跑 `SKILL.md:176` 单个 hunk 的定向 AB。
      > **AI 建议**: 单 hunk 定向 AB + **成文披露「本次未跑 Tier 1 全量」** + 开 issue 把「单 hunk 变更的 AB lane」提为 convention 修订。
      > **理由**: 两次先例的单 skill Rule #6 run 均未跑 Tier 1 全量、均无 `summary.yaml` ⇒ 已是**事实上的偏离**; 按 memory `feedback_written_exception_exact_condition_match`「**N 次非正式援引 ≠ 成文 lane**」, 第三次不披露地偏离是最坏选项。跑全量 10 Skills 字面合规但**测不到要测的东西** (#117 / #127 的套件缺口使该 hunk 大概率仍不可见), 属维度不匹配的投入。
      > ⛔ 无论走哪条, **不得**以「改动小 / 纯括注 / 性价比」为由降级 —— Q5 是 owner 亲裁 (Rule #10)。

- [ ] 5.15 **aria 子模块合并 + 双推 + 逐远端核验 + 主仓 gitlink bump** (承载 CLAUDE.md 多远程两条硬约束)
      > **硬约束 1**: 本地 `git merge` 到子模块 `master` —— ⛔ **禁**用 Forgejo Web UI / API 的 `Do: merge` / `Do: squash`。服务端合并使本地 master 从未 fast-forward ⇒ 双推与 C.2.5 结构上都不触发 ⇒ 主仓 bump gitlink 即产生 orphaned gitlink, GitHub `clone --recursive` 断裂 (2026-07-14 事故)。
      > **硬约束 2**: `git push origin && git push github` 后**逐个** `git ls-remote <remote> master` 取 SHA 与本地比对, **全部一致才算成功** —— push 退出码与回执两个方向都会骗人。`ls-remote` 自身失败 → 重试几次再下结论。
      > **主仓 gitlink**: `git add aria` 必须记**合并后的 `master` SHA**, 不是 feature 分支 SHA。⚠️ 子模块若处于 detached HEAD, `git add aria` 会记 HEAD ⇒ 先确认已在 master 上。
      > **⚠️ 本条与 5.13 正交**: 它规定合并**怎么做**, 5.13 的闸门规定合并**是否获批**。两条都必须过。
      > **推送授权 (AI 建议, 待 owner 确认)**: 推共享 master 属外向且难撤销, 按 memory `feedback_sync_instruction_not_push_authorization` **每次推前须 owner 显式确认**; AI 可执行但不得自我授权。*(注: R2/tech-lead 以 AD10 论证「须标 `agent: owner`」不成立 —— AD10 (`architecture-decisions.md:752-756`) 治的是 Aria 2.0 无人值守流水线的 `S7_AWAITING_MERGE`, 不治交互式 session 的 Phase C。)*

## ⚠️ Phase B 开工前必读 — 三条已知限 (不修, 成文)

按 R3′ 的结构性教训, 以下三条**已知洞不修** —— 修它们会按同一规律再生成一批缺陷。Phase B 实施者知道它们的存在即可, **不要在本 Spec 内解决**:

| 工具 | 已知洞 | 影响 |
|---|---|---|
| `.aria/repro/spec-consistency-check.py` | C1/C3/C4 + C2 后半有与 C8 相同的**空真洞** (表格格式漂移后输出「✅ SC 表 0 条」而非报错); C6 名为「核验行号指向」实为**语法黑名单**, 对自指行号失明 | 它的「8/8 通过」**不等于**机械同步已清零。当作辅助, 不当作闸门 |
| `.aria/repro/mutation-sweep-*.py` | 「11 个维度」只枚举 `normalize()` **函数内部**旗标; 规则 4 回落分支、`org` 处理、`int` 十进制比较、空 basename 判定**未参数化** (实测这 4 个都已被现有 SC 杀死, 不是覆盖洞, 但「枚举完」的措辞不成立) | 它的 exit 0 **不等于**穷尽。新增归一逻辑时须手工判断是否引入新维度 |
| 同上 · `UNOBSERVABLE` 字典 | 两条「行为不可观测」条款 (规则 1 对 `left` 的 strip · D7 的 4300 位上界) 是**硬编码 fail-OPEN 豁免**, 且其支撑实证 (「47,211 候选串零差异」) **在仓里无可执行产物** —— 结论经三席各自独立复现为真, 但留证方式不可复核 | 若归一流程改动使这两维变得可观测而无 SC 杀它, 脚本仍会打绿 |

**⇒ 三件工具的定位是「便宜的辅助」, 不是「机械闸门」。** 唯一可当作证据的是 `sc-baseline-*.py` —— **但见 5.8: 它在实现落地后会恒红, 必须处置。**

**⛔ 同样不要在 Phase B 逐条修 R3′ 的 24 条残留** —— 那是拐点后的循环 (memory `feedback_audit_marginal_return_goes_negative`)。

### 另一条环境陷阱 (非本 Spec 引入, 不修)

`aria/skills/state-scanner/tests/test_collision.py:29-30` 的 `sys.path` insert 顺序倒置, 该模块**只在全量 discovery 时**靠字母序更早模块的副作用才能导入; **单模块跑 (`run_tests.py collision`) 与 pytest 跑都硬失败 ImportError**, 并连带把 `test_coordination_ref_lib.py` 打成 collection error。已破 70 天 (`4d87060`), 开号 **aria-plugin #134**, Level 1 修复, **显式不并入本 Spec**。

⇒ **迭代 `lib/collision.py` 时最自然的两条命令都会给 ImportError。不要误判为自己改坏了。**

---

## ✅ 与母 Spec 的接缝 — 协调项已关闭, 但**已知限悬空风险仍在** (两件事, 不要混读)

**(1) 协调项本体: 已关闭 (owner 裁定 2026-08-08)。** 母 Spec `a1-entry-claim-duplicate-work-guard:172` 逐字请求「在前置 Spec 的非目标处加一句『`include_terminal` 形参由 `a1-entry-claim` 引入, 不属本 Spec 变更面』」并标注「该协调项须 owner 确认」。owner 同意, 该句已落 [proposal.md §非目标](./proposal.md)。⇒ D6/§接口面 的「签名不变」自此限定于本 Spec 变更面; 母 Spec 追加 keyword-only 形参不视为违反、不构成回归。

*(R2′ 曾把它记为「随 Q6 消失」—— 那只消掉了测试层冲突; R3′/tech-lead M7 指出协调项本体一处未动。至此关闭。)*

**(2) 三处已知限的悬空风险: 仍然开着 (与 (1) 无关)。** basename 截断轴 (D4) · 回显原串半幅 (X1) · `include_terminal` 归属 (X3) —— 三条的**关闭时点**全押在母 Spec 上, 而母 Spec `proposal.md:3` 实读为「⛔ 有两个阻塞性未决项, 不具备进 A.2 的条件; 待 owner 裁」。

本 Spec **可独立 ship** (三条都是「已知限」不是「阻塞项」), 且**依赖方向正确** —— 母 Spec `proposal.md:9` 逐字写「前置依赖: `linked-issue-normalization` 必须先 ship」, 本 Spec 独立 ship **不使母 Spec 更难落地** (post_planning R1 / tech-lead 已逐项核: 签名面已裁归母 Spec · 母 §2.1 的 track-id 派生所需两个分量恰由 `normalize_linked_issue -> tuple[str,int] | None` 齐备 · X1 半幅已是 Q1(c) 终局)。

**但母 Spec 长期不解封则三条无限期悬空。** 这不是「接缝没关」, 是「关闭时点不由本 Spec 掌握」。

---
checkpoint: post_planning
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-08T12:49:49.000Z
context: openspec/changes/linked-issue-normalization/detailed-tasks.yaml
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R3 — tech-lead (镜头限定: 只审组 5 / TG-5)

**HEAD**: `2cf2569` | **审计对象**: `tasks.md` §5 全段 + `detailed-tasks.yaml` TASK-014 / TASK-015..021(cancelled) / **TASK-022..027** + `metadata.{scope_boundary, version_reference_surface}`
**vote**: **REVISE** (2 critical + 6 major + 3 minor)
**本轮 fix 引入占比**: **7/9 = 78%** (critical+major 中由 R2-fix 自身新引入的比例) — 见 §Part 4

⛔ 组 1–4 (TASK-001..013) 本轮未审 (owner 裁定)。R2/N9 落在 TASK-013 (parent 4.1) ⇒ `out_of_scope_this_round`。

---

## Part 1 — R2 那 9 条的闭合判定 (逐条 + 实读证据)

| # | R2 findings | 判定 | 依据 |
|---|---|---|---|
| N1 | scope_boundary 自相矛盾 + TASK-016 绕过两个 enabled 闸门 (critical) | **closed** | 矛盾句已消除, 但委派本身开了 X1/X2 两个新洞 |
| N2 | `aria/VERSION` 纳入零命中 ⇒ 恒红 (critical) | **closed** | 已改判为 append-only 账本类, 排除零命中; 残留见 X3 |
| N3 | 缺席断言只对一半维度 + aria 侧仍按文件数 (major) | **partially** | 双向断言已落地; aria 侧的「点数」输入不存在, 见 X6 |
| N4 | 断言排在不可回退点之后 (major) | **closed** | 机械核验依赖链: 024 dep [023], 026 dep [024,025,027] |
| N5 | 修实例不修类 (CLAUDE.md:81 + 无 issue) (major) | **not_closed** | 无任何处置; 且 TASK-023 的「只改数字」把修法(i) 封死了 |
| N6 | 「不改动任何既有编号」自陈为假 (major) | **partially** | 旧句已撤回 ✓; 新句同形状为假, 见 X5 |
| N7 | AI 无 owner 触点向两个共享 master 双推 (major) | **closed (经上报)** | 已改为「AI 建议, 待 owner 确认」+ 我 R2 的 AD10 论据被正确驳回 |
| N8 | TASK-019 验收条把旧值写成断言内容 (minor) | **closed** | 取代者 TASK-023 verification 只点位置不嵌旧值 |
| N9 | TASK-013 的 AB 判据误引 (major) | **out_of_scope_this_round** | parent = 4.1 = 组 4 |

### 逐条实读证据

**N1 — closed.** `metadata.scope_boundary.why_group5_is_here` 现逐字「**合并 / 双推 / gitlink 不在本文件** (见 delegated)」, 与 `delegated[0]` 不再对立; `tasks.md:28` 边界表新增独立行把「aria 子模块合并 + 双远程推送」明确划给 `phase-c-integrator C.2.5`。R2 指出的「同一块内相隔 5 行两句极性相反」已不存在。⚠️ 但委派动作本身产生 X1/X2 —— 我 R2 的 fix_direction(i) 原文是「TASK-016 **退化为**『合并后三条硬判据的独立核验』」, 本版只取了「委派」这一半, **丢掉了「保留独立核验」那一半**。

**N2 — closed.** `metadata.version_reference_surface.two_classes_of_file.append_only_ledger.files = ["aria/VERSION", "aria/CHANGELOG.md"]`, `invariant: 不做零命中`。TASK-024 verification 第 3 条同口径。R2 实测的恒红 (`grep -c "1\.65\.5" aria/VERSION = 2`, bump 后 `发布日期(旧)` 行仍含字面 1.65.5) 已被结构性拆掉。

**N3 — partially.** 双向已落地 (TASK-024 v1「旧值零命中 **且** 新值出现次数 == 各文件预期点数」)。但「预期点数」的唯一指向是 `metadata.version_reference_surface.breakdown`, 而该 breakdown **只有主仓 6 文件**; aria 侧 3 个 normal_reference 文件无点数 ⇒ 计数半边无输入 (X6)。

**N4 — closed (机械核验).** 实跑依赖 dump:
```
TASK-024 5.11 pending S qa-engineer        ['TASK-023']
TASK-026 5.13 pending S backend-architect  ['TASK-024', 'TASK-025', 'TASK-027']
```
DAG 注释 `:858` 逐字「⚠️ 024 (双向断言) 必须在 026 (交付 Phase C) 之前 —— 可回退点之前发红」。R2 的「唯一护栏在唯一不可逆步骤下游」已反转。

**N5 — not_closed.** `grep -n "CLAUDE.md:81|发布同步面|开 issue|开号" tasks.md detailed-tasks.yaml` 对本条**零命中**: 既没有顺带修 `CLAUDE.md:81` 的「aria 子模块 5 文件 + …」枚举, 也**没有开 issue**。且新增了一层阻碍: TASK-023 verification 逐字「CLAUDE.md **只改数字**」—— 这条 (正确地) 引 `claude-md-hygiene.md` 约束住编辑面, 但它同时把 R2/N5 的 fix_direction(i)「TASK-019 顺带把 :81 那行改成引用点口径」**结构性封死**。⇒ 现在只剩 (ii)「开 issue」一条路, 而它没被走。对照同文件的 #133 / #134 两处「披露 + 开号 + 显式不并入」模板, 这一条仍是三者中唯一的静默。

**N6 — partially.** 见 X5 (新自陈同形状为假, 且无重映射表)。

**N7 — closed (经上报, 处置正确).** TASK-026 notes 现逐字「**推送授权 (AI 建议, 待 owner 确认)**: … 每次推前须 owner 显式确认; AI 可执行但不得自我授权」, 并**驳回**了我 R2 用 AD10 的论证。我复核后**接受该驳回**: `aria-orchestrator/docs/architecture-decisions.md` AD10 治的是 v2.0 无人值守流水线的 `S7_AWAITING_MERGE`, 不治交互式 session 的 Phase C —— 我 R2 引错了权威。本条按 Rule #10「AI 任何自作主张的流程判断必须写进 handoff 请复议」处置, 是正确路径, **本轮不再提议**。

**N8 — closed.** TASK-023 verification[0] 逐字「14 个引用点全部更新 (1 + 2 + 3 + 3 + 3 + 2), 逐点核对而非逐文件」—— 无嵌入旧值。

**N9 — out_of_scope_this_round.** 但留一行防丢: `tasks.md:80` 仍把「with_skill 表现优于 without_skill」列在「按 `AB_TEST_OPERATIONS.md` **发版前清单**」之下。实读 `:543-548` 发版前清单四条 = Tier 1 全量 / summary.yaml / 无 WITHOUT_BETTER / 与上次比对无回归; 「with_skill 优于 without_skill」在 `:536-541` 的「**新增 Skill 后**」清单。误引未修 (组 4, 不计入本轮票)。
⚠️ **同时更正我 R2 的一处口径错误**: TASK-027 notes 逐字指出「R2/tech-lead 的『28 Skills / ~$14 / 6-8h』口径不是 Tier 1 全量 (Tier 1 = 10 个)」—— 复核 `:396` 与场景 3 后**该更正成立**, 我 R2 把「场景 3 全量回归 (28 Skills)」与「Tier 1 全量 (10 Skills)」混为一谈。TASK-027 引的是正确的那个。

---

## Part 2 — 镜头 A: 条款间交叉一致性 (每条单独看都对, 但 A 违反 B 的隐含前提)

### X1 — `new` (fix-introduced)

```
- type: issue
  severity: critical
  category: architecture
  scope: TASK-026 verification/notes + metadata.scope_boundary.delegated[0].what + tasks.md:32 + TASK-023 notes + 全部 active 任务的 deliverables
  summary: 主仓 gitlink bump 现在**零归属** —— TASK-017 被 cancel、TASK-023 明文排除它、TASK-026 声称「由该 Skill 的既有机制与闸门保证」, 而 phase-c-integrator **全文没有任何 gitlink bump 步骤**; 同时它从所有 active 任务的 deliverables 里消失, 且 TASK-024 的双向断言对它结构性失明 ⇒ 发版可以在「主仓文档写 v1.66.0、gitlink 仍指 v1.65.5 代码」的状态下全绿。
  evidence: |
    三条声称 (每条单独看都合理):
      tasks.md:32 逐字「**gitlink 必须指向合并后的 `master` SHA, 这条约束随交接一并移交, 由 C.2.5 的既有机制保证。**」
      metadata.scope_boundary.delegated[0].what 逐字含「**主仓 gitlink bump** (须指向合并后 master SHA)」
      TASK-023 notes 逐字「**gitlink 不在本任务** — 随合并一并移交 Phase C (TASK-026)」
      TASK-026 verification[2] 逐字「⛔ 本任务**不复述** C.2.5 / C.2.4 的判据 — 合并 / 双推 / ls-remote 核验 /
        **gitlink bump** / PR / pre-merge gate 全部由 phase-c-integrator 的既有机制与闸门保证」

    委派目标的实际能力面 (实读 aria/skills/phase-c-integrator/SKILL.md 全文):
      · `grep -n "bump" SKILL.md` → 只有 :194 / :440 / :442, 三处都是 **submodule_gate 的 verdict 词**
        (「forward bump / no-change / first-time」), 即**判定别人已经 bump 的结果**, 不是执行 bump;
      · §C.2.4.5 (:376-568) = Submodule Pointer Regression **Gate** —— `git -C <sub> merge-base
        --is-ancestor MASTER_PTR FEATURE_PTR`, 只核 PR 里**已存在**的指针的 ancestry;
      · §C.2.5 (:570-608) = Multi-Remote Push Enforcement —— 只做 push + `verify_parity_post_push`,
        步骤 1-6 无任何 `git add <submodule>` / 指针提交;
      ⇒ **该 Skill 不 bump gitlink。** memory `feedback_submodule_pointer_post_merge_bump` 逐字确认这是
        人工纪律步骤: 「`git submodule update <sub>` **won't auto-do this**; explicit `git add <submodule>`
        after `git -C <submodule> checkout master`」, 并给出 4 步手工 How-to-apply。

    交付面上也已消失: TASK-017 (cancelled) 的 deliverables 曾有 `aria  # gitlink (子模块指针) — R1-fix:
    首版承重却不在 deliverables`。实跑 active 20 条的 deliverables: TASK-022 = 5 个 aria/ 文件,
    TASK-023 = 6 个主仓文档, TASK-024/026 = [], TASK-025 = repro 脚本, TASK-027 = .aria/decisions/。
    ⇒ **R1-fix 明确修好过的那一处 (「承重却不在 deliverables」) 被 R2-fix 重新打开, 且这次连兜底都没了。**

    为什么会全绿 (假绿的完整路径):
      · TASK-024 是本 Spec 唯一的机械护栏, 但 metadata 自己写着 `plus: "主仓 gitlink (**非文本引用**) + …"`
        ⇒ 它是文本 grep, 对 gitlink 天然失明;
      · 若 gitlink 干脆没被 bump, 它停在旧 master SHA ⇒ §C.2.4.5 的三值判定落 **no-change ⇒ PASS**
        (:194 逐字「pass: 所有 submodule pointer 是 forward bump 或 **no-change** 或 first-time」);
      · 两条 enabled custom check (m6-version-badge-match / i18n-readme-translation-currency) 只比文本;
      ⇒ 主仓 master 宣称 v1.66.0 而实际引用 v1.65.5 的插件代码, 全链无一处发红 = #165 家族的形状。
    形状 = memory feedback_completion_signals_vs_runtime_invocation (「有委派」≠「委派对象真会做」)
         + feedback_spec_precedent_verify_execution_history (引「复用既有机制」须核该机制的实际语义)。
  fix_direction: |
    **减法/替换, 不加 metadata 块**:
    (1) 把 TASK-026 verification[2] 那句里的 `gitlink bump` **删掉** —— 它不属于「不复述判据」的那一类,
        因为委派目标根本没有这条判据可复述;
    (2) TASK-026 verification 增一条**交接清单**项 (不是判据复述, 是交接载荷):
        「交接必须点名: 主仓 gitlink bump 由谁在何时执行 (phase-c-integrator 无此步骤 —— C.2.4.5 只核
         ancestry, C.2.5 只推) + 目标 SHA 必须是 aria master 合并后的 SHA」;
    (3) tasks.md:32 那句「由 C.2.5 的既有机制保证」**改为**「C.2.5 不做 gitlink bump, 该项须在交接清单
        里显式指派」(一句替换);
    (4) 开 issue 记 Skill 侧缺口 (phase-c-integrator 无 gitlink bump 步骤), 与 #133/#134 同形态。
```

### X2 — `new` (fix-introduced)

```
- type: issue
  severity: critical
  category: process
  scope: TASK-026 + metadata.scope_boundary.delegated[0] + tasks.md:28/:32 + 被删的 TASK-016 verification
  summary: 委派目标的**文档化默认合并路径是 Forgejo 服务端 API merge**, 而 CLAUDE.md 硬约束 1 对子模块**明文禁止**它; 服务端合并又使本地 master 永不 fast-forward ⇒ 被同批委派出去的「双推 + 逐远端 ls-remote 核验」结构上**不触发**。而 R2-fix 删掉的 TASK-016 正是全 Spec 唯一写着这两条硬约束的地方 ⇒ 删掉断言 + 交给一个默认走禁用路径的机制。
  evidence: |
    委派链的实际终点 (逐字):
      phase-c-integrator SKILL.md:253 (C.2.4 步骤 6) 「`green` → **调用 branch-manager merge action**, 进入 C.2.5」
      phase-c-integrator SKILL.md:236 边界表 「branch-manager (C.2.4-C.2.5) | wait approval + **merge API call**」
      branch-manager SKILL.md:528 「C.2.5 - 合并 (可选, auto_merge=true 时): … **调用 Forgejo API 合并 PR**」
      branch-manager SKILL.md:625-639 实体命令 `curl -X POST …/pulls/{n}/merge -d '{"Do": "squash"}'` / `'{"Do":"merge"}'`
      ⇒ 委派目标的合并 = **服务端 `Do: merge`**。

    CLAUDE.md「多远程推送 — 两条硬约束 (owner 裁决 2026-07-20, 根治 Aria #165)」逐字:
      「**约束 1** — 子模块合并一律本地做, **禁止 Forgejo 服务端合并**: 子模块 (aria / standards /
       aria-orchestrator) 的分支合并必须本地 `git merge` + 双推, **禁**用 Forgejo Web UI / API 的
       `Do: merge`。原因: 服务端合并的 merge commit 只在 Forgejo 生成, 本地 master 从未 fast-forward
       ⇒ 本地双推与 **C.2.5 结构上都不触发**, 主仓随后 bump gitlink 即产生 orphaned gitlink…
       例外: 主仓 (Aria) 自身 PR 可走 Forgejo merge」
    memory feedback_mirror_sync_needs_mechanical_backstop 独立复述同一机制: 「C.2.5 触发前提是「**本地**
      master 已 fast-forward」… 服务端合并路径下本地 master 从不前进, **C.2.5 根本不触发**」, 并记 3 次复发。

    委派目标是否编码了约束 1? `grep -n "服务端|Do: merge|本地 merge|本地合并|禁|ls-remote"
    phase-c-integrator/SKILL.md` → **零命中**关于合并方式的约束 (命中的 4 条全是 CI backend 语义)。
    ⇒ 该 Skill 不知道「子模块要本地合并」这条例外; 它的 C.2.5 只在本地已 ff 的前提下才起作用。

    而本轮**删掉的**那条任务的 verification 逐字 (TASK-016, 现 cancelled):
      - "本地 `git merge` 到 aria 子模块 master — ⛔ **未**使用 Forgejo Web UI / API 的服务端 merge"
      - "`git push origin && git push github` 双推已执行"
      - "**逐个** `git ls-remote <remote> master` 取 SHA 与本地比对, origin 与 github **全部一致**"
    ⇒ 全 Spec 现在**没有任何一处**要求子模块走本地合并。TASK-026 verification[2] 明文放弃复述, 而
      「不复述判据」在这里的实际效果不是去噪, 是把**委派目标未编码的那条子模块特例**一起省掉了。
    注: 我 R2/N1 的 fix_direction(i) 原话是「TASK-016 **退化为**『合并后三条硬判据的独立核验』」;
      本版执行了「委派」但丢掉了「保留核验」—— 半幅吸收。
    形状 = memory feedback_fixes_contradict_each_other_across_clusters (Rule #10 那一簇的 fix 违反了
      「多远程硬约束」那一簇的隐含前提, 接缝落在两个角度之间) + feedback_fix_recurs_in_its_own_fallback_path。
  fix_direction: |
    **不撤销委派** (owner 裁定 + Rule #10 站得住), 只补交接载荷 —— 一条 verification, 非新块:
    TASK-026 verification 增: 「交接必须点名 **CLAUDE.md 约束 1**: aria 子模块合并走**本地 `git merge`**,
      ⛔ 禁 Forgejo Web UI / API `Do: merge` (该 Skill 未编码此子模块特例, 其文档默认路径 C.2.4→
      branch-manager merge API 恰是被禁的那条; 服务端合并会使 C.2.5 的双推与 parity 核验不触发)。」
    + 同一条尾注「约束 2 (逐远端 ls-remote) 在本地合并前提下由 C.2.5 的 verify_parity_post_push 承担,
      故不复述」—— 这样「不复述」的边界从「全部不说」收窄为「只不说该 Skill 真的有的那部分」。
    + 开 issue: phase-c-integrator 未编码 CLAUDE.md 约束 1 (可挂 Aria #165 预防侧)。
```

### X5 — `new` (fix-introduced; 与 N6 同形状复发)

```
- type: issue
  severity: major
  category: documentation
  scope: tasks.md:14 (新自陈) + detailed-tasks.yaml:12-14 (同句) + 缺失的重映射表
  summary: 撤回一句假自陈的**同一段**里立了一句同形状的新假自陈 —— 「R1/R2 两轮共十份报告对旧 ID 的引用继续成立」对**五份 R1 报告为假**: R2-fix 冻结的是 **R1-fix 后**的语义, 不是 R1 报告引用的原语义; 且两条 fix_direction 都没走 (既没恢复原语义, 也没给重映射表)。
  evidence: |
    tasks.md:14 逐字: 「`5.2`–`5.8` 全部**保留编号并标 `(CANCELLED)`** … `TASK-015`–`TASK-021` 同样保留
      并标 cancelled。⇒ **R1/R2 两轮共十份报告对旧 ID 的引用继续成立**, 不再制造第二次错位。」
    yaml:12-14 同句。

    但 tasks.md:12 (紧邻上一段) 自己刚承认: R1-fix 把 `TASK-016`/`TASK-017` **原地改指**了。R2-fix 冻结的
    是改指**之后**的含义 —— 实读当前文件:
      TASK-016 (cancelled) title = 「aria 子模块分支合并 + 双远程推送 + 逐远端 ls-remote 核验」
      TASK-017 (cancelled) title = 「主仓 gitlink + VERSION 子模块表行 + README.md 两处版本引用」
    而五份已 commit 的 R1 报告按**原**含义引用。实读 post_planning-R1-…-tech-lead.md:
      :59  「… ⇒ **TASK-016** 在「只本地合并、从未推 GitHub」的状态下即可判绿…」
      :65  「但 **TASK-016** verification 只有两条: (a) **gitlink 指向合并后 master SHA**;
             (b) m6-version-badge-match → OK。」  ← R1 期的 TASK-016 是 gitlink/主仓同步面任务
      :92  「(b) 主仓根 — **TASK-016** `VERSION` / `README.md`, **TASK-017** `README.{zh,ja,ko}.md`」
    ⇒ 拿这三行去解析当前文件, TASK-016 是「合并任务」、TASK-017 才是 gitlink 任务 ⇒ **仍然错位**。
    正确重映射: R1 报告的 TASK-016 = 本版 TASK-017 语义; R1 的 TASK-017 = 本版 TASK-018 语义。
    `grep -n "重映射|remap|R1 报告中的 TASK|映射表" tasks.md detailed-tasks.yaml` → **零命中**。

    我 R2/N6 给的两条路: (1) 恢复 5.3/5.4 与 TASK-016/017 原语义并把新工作挪到 5.9/TASK-022 起;
    (2) 删掉自陈, 换显式重映射表。本版**两条都没走**, 而是新增了第三种: 冻结改指后的语义 + 断言
    「十份报告的引用继续成立」。对 R2 五份报告为真, 对 R1 五份报告为假 ⇒ 覆盖面从「本轮」扩大到
    「十份」的同时把真值降了一半。
    形状 = memory feedback_critique_repeats_the_error_it_names (指控别人「引用错位」的那一段里犯同款)
         + feedback_cross_doc_claim_verify_at_target (跨文档断言须去目标处实测)。
  fix_direction: |
    **纯替换, 零新增**: 把 tasks.md:14 / yaml:12-14 的「⇒ R1/R2 两轮共十份报告对旧 ID 的引用继续成立」
    换成三行重映射表:
      | 引用出处 | 报告里的 ID | 当前文件的对应任务 |
      | R1 五份报告 | TASK-016 | TASK-017 (主仓 gitlink + VERSION + README) |
      | R1 五份报告 | TASK-017 | TASK-018 (i18n README ×3) |
      | R2 五份报告 | TASK-015..021 | 同名 (R1-fix 后语义, 已冻结) |
    ⛔ 不可保留现状: 现状是一句被 `git show a52ab81` + 一次 grep 就能推翻的自我描述, 且它出现在
      专门承诺引用稳定性的那一段里 —— 与 R1-fix 那次是同一个位置、同一个形状、第二次。
```

### X6 — `new` (fix-introduced)

```
- type: issue
  severity: major
  category: testing
  scope: metadata.version_reference_surface.{breakdown, two_classes_of_file.normal_reference, aria_side_points} + TASK-024 verification[1]
  summary: 同一个 metadata 块内两句互斥, 且 TASK-024 的「预期点数」对 aria 侧 3 个文件**没有输入** —— 计数断言退化为「≥1」, 漏 `marketplace.json:16` 时判绿 (那正是 R2/code-reviewer N-2 抓的那一处)。
  evidence: |
    TASK-024 verification[1] 逐字: 「预期点数**先枚举后断言** (不是只查缺席) — 见
      **metadata.version_reference_surface.breakdown**」。
    实读 breakdown (:103-109): 只有 6 个键 —— README.md 2 / README.zh.md 3 / ja 3 / ko 3 /
      CLAUDE.md 2 / VERSION 1 (`main_repo_points: 14`)。**没有任何 aria/ 文件。**
    而 normal_reference.files (:119-120) 有 9 个, 含 3 个 aria 文件
      (aria/.claude-plugin/plugin.json, aria/.claude-plugin/marketplace.json, aria/README.md),
      其 invariant 逐字要求「新值出现次数 == **该文件预期点数**」。
    ⇒ 9 个文件里 3 个的「预期点数」在被指定的 SOT 里不存在 (memory feedback_verify_predicate_inputs_exist:
      审计判定机制必分两层 —— 逻辑对吗 + **它要判的输入真会被生成吗**)。

    同块内的互斥: `aria_side_points` 逐字「**4 个**普通引用点文件中 marketplace.json 含 2 个 version
      字段 (:3/:16)」, 而同块 `normal_reference` 只列了 **3** 个 aria 文件 —— 第 4 个 (`aria/VERSION`)
      恰好被**同一个块**改判成了 append_only_ledger。⇒ 「4 个普通引用点文件」是改判前的遗留计数,
      与它下方 5 行的分类表直接冲突; 且它给的是**文件数**, 正是本块通篇在批的那个维度。

    我今日实测 (`grep -c` 逐文件, HEAD=2cf2569), 可直接写死:
      aria/.claude-plugin/plugin.json      1
      aria/.claude-plugin/marketplace.json 2   (:3 / :16)
      aria/README.md                       1   (:5 `> **Version**: 1.65.5 | **Released**: …`)
      ⇒ aria 侧 normal_reference = 3 文件 4 点
      主仓 6 文件 14 点 (1/2/3/3/3/2) —— 与 breakdown 逐一吻合 ✓
  fix_direction: |
    **替换 + 删除, 不加第 7 个块**:
    (1) `breakdown` 扩成 9 个键 (补上面三行的 1/2/1) 并把键名改为全限定路径 —— 它本就是 TASK-024 指定的
        SOT, 补齐即闭合;
    (2) **删掉** `aria_side_points` 那句散文 (它的信息量已被 (1) 覆盖, 且它自己的「4 个文件」与分类表冲突);
    (3) 顺带把 `main_repo_points: 14` 旁加一行 `aria_normal_points: 4` 或直接让 TASK-024 只引 breakdown。
```

### X4 — `new` (fix-introduced; 编号不可变 fix 的副产物)

```
- type: issue
  severity: major
  category: process
  scope: tasks.md:100-106 (7 条 CANCELLED 的 `- [ ]` 形态) + metadata.scope_boundary.delegated[1].why
  summary: CANCELLED 台账用**未勾选 checkbox** 保留 ⇒ 归档门的 tasks.md 分支对本 Spec **永久判红**, 通过只能靠 Status 分支 = 「声称」; 而 metadata 恰好写着「归档门会消费本文件全部 27 个 checkbox 状态, 故组 5 必须真做完**而非声称**」—— 它引为保证的那个机制, 正是这个设计废掉的那个。
  evidence: |
    metadata.scope_boundary.delegated[1].why 逐字: 「归档门会消费本文件全部 **27 个 checkbox 状态**
      (20 active + 7 cancelled), 故组 5 必须真做完而非声称」。
    tasks.md:100-106 七条形态逐字: `- [ ] ~~5.2 …~~ **(CANCELLED)**` —— 未勾选 checkbox。

    **实跑归档门本体** (aria/skills/state-scanner/scripts/lib/spec_complete.py::is_spec_complete):
      GATE: {'complete': False, 'reason': "tasks.md has **27/27** unchecked task(s);
             normalized Status = 'pending' (≠ done)"}
      boxes: 27  unchecked: 27
    机制实读 (:273-278): `_CHECKBOX_RE` 计全部 checkbox, `unchecked = [b for b in boxes if b not in
      ("x","X")]`, 非空即 `tasks.md has N/M unchecked` ⇒ tasks 分支不放行。
    ⇒ 20 条 active 全部完成后, 该分支恒定读作 「**7/27 unchecked**」—— 而那 7 条**永远不能**合法勾成
      `[x]` (它们是被取消的工作, 勾上就是假完成声明)。⇒ tasks 分支对本 Spec **永久红**, OR 的左半永久
      失效, 只能靠右半 `normalized Status == 'done'` 放行 = **一个人写的 Status 字段** = 「声称」。
    第二个受害机制 (同一根因): session-closer `handoff_autofill.py:160 grep_unchecked_tasks` 扫 active
      changes 的 `- [ ]` 进 §2 unfinished 机械候选 ⇒ 这 7 条会出现在归档前**每一次** session handoff 的
      未完成清单里。而 tasks.md:18 刚宣布「checkbox 形态后该盲区对本 Spec 消失」—— 消失的是漏报,
      换来的是 7 条永久误报。
    第三层 (若 tasks.md 缺席时的 fallback): `lib/detailed_tasks.py:83 _DONE_FAMILY =
      frozenset({"done","completed"})` 是 **fail-CLOSED 白名单**, 且 `DUAL_LAYER_SPEC.md:164` 的 status
      enum 逐字只有 `pending / in_progress / completed / blocked` —— `cancelled` **不在枚举内**,
      `:124-126` 还写着「新增枚举值前请同步核对 _DONE_FAMILY 语义」。⇒ YAML 层同样把 7 条算残留。
    注: `- [ ] … (CANCELLED)` 这个写法确实是 DUAL_LAYER_SPEC.md:258 / SYNC_RULES.md:239 的**官方示例**,
      所以根因一半在插件侧 (那两处示例与 #113 归档门互相拆台); 但本 Spec 是仓内**第一个**真用它的
      change (`grep -rn CANCELLED openspec/changes/*/tasks.md` 只命中本文件), 无先例可依。
    形状 = memory feedback_false_green_dual_is_permanent_red (「该信号在健康常态下应是什么值?」——
      健康常态下这个信号是**红**, 故零信息) + feedback_invariant_needs_failclosed_default。
  fix_direction: |
    **减法**: 把 5.2–5.8 七条从 checkbox 语法里拿出来 —— 改成表格行或普通列表项 (`| ~~5.2~~ | CANCELLED |
    由 5.9 取代 |`), **编号照旧保留**。编号不可变约束要保的是「编号与其含义」以便 parent 引用与外部报告
    解析, 而**不是 `- [ ]` 这四个字符**; 去掉 checkbox 后:
      · 归档门 tasks 分支 = 20/20 → 可真绿 (强信号复活);
      · handoff unfinished 不再有 7 条永久误报;
      · YAML 侧保留 `status: cancelled` 不变 (仅在 tasks.md 缺席时才被读, 且本 Spec 两层并存 ⇒ 不看 yaml)。
    同时把 metadata 那句「27 个 checkbox 状态 (20 active + 7 cancelled)」**改成** 「20 个 active checkbox」
    (一句替换)。⚠️ 这一步偏离 DUAL_LAYER_SPEC.md:258 的示例 ⇒ 须同批**开 issue**: 「插件侧 CANCELLED
    示例 (`- [ ]` 保留) 与 #113 归档门 / handoff unfinished 扫描互相拆台」, 让类也被记账 (对照 N5 的教训)。
```

### X7 — `carryover` (类未修完; 落点在 proposal.md, 与组 5 的 TASK-023 直接冲突)

```
- type: issue
  severity: major
  category: documentation
  scope: TASK-023 (14 点口径) vs proposal.md:271 §Impact (5 点口径)
  summary: 「三份文档同一形状第三次」只修了两份 —— proposal §Impact 仍逐字写「5 文件 + gitlink + VERSION 行 + README badge + translated-from ×3」= 主仓 **5** 个点, 漏 README.md 的 `Plugin Version:` 行 + i18n 的 6 处 + CLAUDE.md 的 2 处; 而 §Impact 是本 change 的交付面 SOT, 按它执行就会漏 9 点。
  evidence: |
    proposal.md:271 逐字: 「**发版同步面 (R1′/tech-lead-M5 展开, 原写「5 文件 + gitlink」漏 3 处)** |
      aria 子模块 **5 文件** + 主仓 **gitlink** + 主仓 `VERSION` 的子模块版本表行 +
      **`README.md` 的 Plugin badge** + **`README.{zh,ja,ko}.md` 的 `translated-from` 标记**…」
    枚举出的主仓点数 = VERSION 1 + README badge 1 + translated-from 3 = **5**; TASK-023 逐点改的是 **14**。
    缺的 9 点实测确认存在: README.md:242 `Plugin Version:   1.65.5` / README.{zh,ja,ko}.md 各自的
      badge (:10) 与 `Plugin Version:` 行 (:244) 共 6 / CLAUDE.md:139 版本区间行 + :141「版本:」行 2。
    而 yaml 的 `TASK-020 notes` (cancelled) 自己写着「三份文档 (**proposal §Impact** / tasks.md / 本文件)
      首版都写「5 文件 + gitlink + …」这一文件数口径 … **同一形状第三次**。故本版不再靠逐条补丁, 改用
      机械断言收口」—— 机械断言 (TASK-024) 只收 tasks/yaml 这一口, proposal 那一口原样留着。
    ⇒ 同一个 change 的三份文档现在有两套同步面口径; 实施者读 proposal §Impact (它是 Level 3 的规范本体)
      会做 5 点, 读 tasks.md 会做 14 点。TASK-024 会把前者判红 —— 但那是**发现**而不是**预防**,
      且发现时点在 Phase C 之前, 成本可控 (故 major 而非 critical)。
    形状 = memory feedback_fix_the_class_not_the_instance (修实例必问「这形状还有几个兄弟位置」);
      与 N5 是同一个类的另外两个成员 (proposal §Impact / CLAUDE.md:81)。
  fix_direction: |
    一行替换 proposal.md:271 的枚举, 与 TASK-023 的 breakdown 对齐 (**引用点**口径, 14 点 + 4 aria 点 +
    gitlink 单列并注明「非文本引用, 见 X1」)。不新增段落 —— 该行本就是同步面枚举行, 只是口径旧。
```

---

## Part 3 — 镜头 B: 每条机械断言在健康常态下应是什么值 (双向筛查)

方法: 对每条断言先**写下预期**再实测 (memory `feedback_predict_before_measure_for_self_check`)。

| 断言 | 一切正确时是绿吗 (非恒红?) | 做错时一定红吗 (非假绿?) | 判定 |
|---|---|---|---|
| **TASK-024 普通引用文件**: 旧值零命中 **且** 新值计数 == 点数 | ✅ 绿 — 主仓 6 文件实测 1/2/3/3/3/2 = 14, 全为 live 引用, 无发布史行 (今日 `grep -c` 逐一复核; `standards/conventions/secret-hygiene.md:401` 那一处是账本行, 不在断言名单内, 不构成第 15 点) | ✅ 红 — 漏改 (计数<预期) / 删行 (计数<预期) / 写错成 `1.6.60` (旧值零命中过但新值计数<预期) 三类都红。**双向成立** | **PASS** |
| **TASK-024 append-only 账本**: 头部「当前版本」行 == plugin.json | ✅ 绿 — aria/VERSION:3 `> **版本**: 1.65.5`、aria/CHANGELOG.md:13 首个 `## [1.65.5]` 均可解析 (CHANGELOG 头部有 6 行样板 + 一段 HTML 注释, 「头部」需定义为「首个 `## [x.y.z]`」才机械可判 —— 措辞可收紧但输入存在) | ❌ **假绿** — 见 X3 | **X3** |
| **TASK-024 aria 侧计数** | — | ❌ 无预期点数输入 ⇒ 退化为「≥1」 | **X6** |
| **TASK-024 对 gitlink** | — | ❌ 结构性失明 + no-change 落 PASS | **X1** |
| **TASK-022 账本口径**: 只改头部行 + 追加发布注, 历史行原样保留 | ⚠️ 「原样保留」与文件真实协议不符 | — | **X10** (minor) |
| **TASK-025 路径一** (脚本转绿) | ✅ 可跑判据存在 (脚本 exit 0) | ✅ 正常化改坏则红 | **PASS** |
| **TASK-025 路径二** (归档后 FATAL) | — | ❌ 验收时点早于失效时点 | **X8** |
| **归档门 / handoff unfinished** (被 metadata 引为「必须真做完而非声称」的保证) | ❌ **恒红** — 实测 27/27, 完工后 7/27 | — | **X4** |

### X3 — `new` (fix-introduced)

```
- type: issue
  severity: major
  category: testing
  scope: metadata.version_reference_surface.two_classes_of_file.append_only_ledger.invariant + TASK-024 verification[2] + TASK-022 verification[1..2]
  summary: 账本类的新不变量**仍是单向的** —— 「头部当前版本行 == plugin.json」在「**销毁发布史来凑绿**」这个失效模式下判绿, 而那恰好是它替换掉的那个恒红所激励的作弊路径 (R2/N2 逐字点名过)。同一批编辑把普通文件双向化了, 却对账本类重犯了单向。
  evidence: |
    新不变量逐字 (:124): 「**不做零命中** (历史保留旧版本号是正确的) —— 判据是头部「当前版本」行 == plugin.json」。
    TASK-024 verification[2] 同口径。健康常态: 绿 ✓ (非恒红, N2 已闭合)。

    失效方向的两个具体反例, 都判绿:
      (a) aria/VERSION —— 实施者把 `> **发布日期**: 2026-08-02  # patch: v1.65.5 …` 这一行**覆盖**成
          v1.66.0 的发布注 (而不是先降级为 `发布日期(旧)` 再追加)。结果: `> **版本**: 1.66.0` == plugin.json
          ⇒ **绿**; 而 v1.65.5 的发布纪要被静默删除, 167 行账本从此断一节。
      (b) aria/CHANGELOG.md —— 实施者把 `## [1.65.5] - 2026-08-02` **改写**成 `## [1.66.0] - 2026-08-08`
          (而不是在其上方插新条目)。结果: 首个版本标题 == plugin.json ⇒ **绿**; v1.65.5 条目消失。
    两者都正是 R2/N2 evidence 里逐字预告的坏出路: 「实施者要么**删发布史去凑绿**, 要么把断言当噪声忽略」。
    R2-fix 消掉了后者 (恒红), 前者**没有任何断言拦**。
    TASK-022 verification 里确有两条相关文字 (「历史行原样保留」/「为追加条目, 未改写历史」), 但它们是
      **人读判断项**, 不是机械谓词; 而 TASK-024 是本 Spec 自称「唯一维度匹配的判据」的那一条 —— 它对这
      个方向没有维度 (memory feedback_invariant_dimension_must_match_error_dimension: 无向检查对**方向性**
      错误天然免疫)。
    形状 = memory feedback_fix_recurs_in_its_own_fallback_path (要治的病在新写的分类分支里复发) +
      one_sided_assertion_is_half_dimension 这条本块自己写下的判据**没有施加给自己**。
  fix_direction: |
    **同一条不变量双向化 (加半句, 不加块)**: append_only_ledger.invariant 改为
      「头部「当前版本」行 == plugin.json **且** 旧版本号在本文件的命中数**不减**
       (bump 前后 `grep -c "1\.65\.5"`: aria/VERSION 恒 ≥2, aria/CHANGELOG.md 恒 ≥1)」。
    ⇒ 健康常态: 绿 (历史保留); 覆盖/改写历史: 命中数下降 ⇒ 红。这正是普通文件那条「零命中 **且** 计数
      == 点数」的对偶写法 —— 账本类的双向 = 「头部前进 **且** 历史不缩」。
    TASK-022 那两条人读项可保留为实施指引, 但**判据落在 TASK-024**。
```

### X8 — `new` (fix-introduced)

```
- type: issue
  severity: major
  category: testing
  scope: TASK-025 verification[0..1]
  summary: 路径二 (归档后 FATAL) 的验收**在它自己的验收时点上不可测** —— 归档发生在 Phase D.2, 即本任务判绿之后; 而两条验收条目写的是「已处置」, 是不可证伪的自陈 bool。
  evidence: |
    TASK-025 verification 逐字:
      - "路径一 (恒红): TASK-008 落地后那 8 条 SC 转绿 ⇒ 脚本 :275-277 恒红 — **已处置**"
      - "路径二 (归档后): 脚本从 proposal.md 现场解析 (:205-215 FATAL fail-CLOSED) ⇒ Spec 归档后换一种
         恒红 — **已处置**"
    引用核验 (逐字实读, 无 miscitation): `.aria/repro/sc-baseline-…py:275-277` = `if measured_face !=
      EVIDENCE_FACE: print(...); sys.exit(1)` ✓; `:205-215` = `_PROPOSAL = …/proposal.md` +
      `sys.exit("FATAL: 找不到 proposal.md …")` ✓; option (b) 引的 `proposal.md:181/:219` 两处 artifact
      指针也都实存 ✓。**引用面干净, 问题在验收面。**

    「已处置」= 一个由实施者自填的 bool, 无可验 metric (memory
      feedback_falsifiable_evidence_for_binary_acceptance: Acceptance bool 必 mandate 可验 metric,
      否则 AI 代填 true 无法 audit)。
    更硬的一层: 路径二的失效**发生在 Phase D.2 归档时**, 而 TASK-025 在 Phase B 判绿。若不把判据改成
      「现在就能测归档后行为」, 这条验收在任何时点都不可能红 —— 它是一条恒绿断言 (假绿的极限形态)。
    路径一无此问题: `python3 .aria/repro/sc-baseline-…py aria/skills/state-scanner` 的 exit code 当场可测。
  fix_direction: |
    **替换两条自陈为可跑判据** (不加块):
      路径一 → 「`python3 .aria/repro/sc-baseline-linked-issue-normalization.py aria/skills/state-scanner`
                → **exit 0**」(走 (a)) 或「该路径已不存在文件」(走 (b));
      路径二 → **把「归档后」现在就模拟出来**: 「临时把 `openspec/changes/linked-issue-normalization/`
                改名 (或用 `--proposal <archive-path>` 形参) 后重跑, 脚本**不得**以 FATAL 退出」
                —— 走 (a) 时证明表已冻成同目录存档、不再现场解析 proposal.md; 走 (b) 时证明
                `grep -rn "sc-baseline-linked-issue-normalization" openspec/ .aria/` 的每条命中都指向
                新存档路径 (**dangling 零命中**)。
    这样两条都在 Phase B 当场可红。
```

### X9 / X10 / X11 — minor

```
- type: issue
  severity: minor
  category: documentation
  scope: tasks.md:154
  summary: 指向已 CANCELLED 的 5.8。逐字「唯一可当作证据的是 `sc-baseline-*.py` —— 但见 **5.8**: 它在实现落地后会恒红, 必须处置。」而 5.8 本轮已 cancel, 现行是 **5.12**。
  evidence: tasks.md:106 逐字「~~5.8 sc-baseline 脚本处置~~ **(CANCELLED)** → 由 **5.12** 取代」; :154 未同批更新。读者跟着指针落到一个「勿复用」的台账行。
  origin: new
  fix_direction: 一处改数字 5.8 → 5.12。
```
```
- type: issue
  severity: minor
  category: documentation
  scope: tasks.md:111 (5.9) + TASK-022 verification[1]
  summary: 「`VERSION` … 只改头部「当前版本」行 + 追加本次发布注, **历史行原样保留**」与 aria/VERSION 的真实协议不符 —— 上一条 `> **发布日期**:` 行必须被**降级**为 `> **发布日期(旧)**:`, 它不是「原样保留」。
  evidence: |
    实读 aria/VERSION:3-9 —— 结构是 `> **版本**: X` + **恰好一条** `> **发布日期**:` + N 条 `> **发布日期(旧)**:`
    (回溯至 v1.47.0)。⇒ 每次发版的正确操作是三步: 改 :3 版本号 / 把当前 `发布日期` 行改键为 `发布日期(旧)` /
    插入新 `发布日期` 行。按「历史行原样保留」字面执行会得到**两条** `**发布日期**` 行, 使「头部当前版本行」
    与下一次的降级操作都变歧义。
  origin: new
  fix_direction: 把那半句改成「上一条 `发布日期` 行降键为 `发布日期(旧)` 后追加新 `发布日期` 行; **历史行的版本号不改**」。
```
```
- type: issue
  severity: minor
  category: documentation
  scope: metadata.scope_repos[1].head
  summary: 主仓 head 记 `a52ab81` (A.2 首版), 实际 HEAD 已是 `2cf2569` (落后 3 commit: R1-fix / R2 报告 / R2-fix), 且字段名未标明是「规划时基线」还是「当前」。aria 侧 `af87cae` 实测吻合 ✓ (含 detached HEAD 状态)。
  evidence: "git rev-parse --short HEAD → 2cf2569; git ls-tree HEAD aria → af87cae ✓"
  origin: carryover (A.2 首版即如此, 两轮 fix 均未动)
  fix_direction: 字段改名 `head_at_planning` 并注明不随 revision 更新 (或每轮同步)。二选一, 别留歧义。
```

---

## Part 4 — 收敛评估与拐点判据

### 本轮 fix 引入占比 = **7/9 = 78%**

critical + major 共 **9** 条 (X1 X2 X3 X4 X5 X6 X7 X8 + N5-carryover):

| 条目 | R2-fix 自身引入? |
|---|---|
| X1 gitlink 零归属 | ✅ (cancel TASK-017 + 委派给不做它的 Skill) |
| X2 服务端 merge / C.2.5 不触发 | ✅ (删 TASK-016 = 删掉唯一写着两条硬约束的地方) |
| X3 账本不变量单向 | ✅ (新写的分类分支) |
| X4 CANCELLED checkbox 恒红 | ✅ (编号不可变 fix 的产物) |
| X5 新自陈对 R1 五份报告为假 | ✅ (新写的句子) |
| X6 aria 侧点数无输入 + 块内互斥 | ✅ (新写的块) |
| X7 proposal §Impact 仍 5 点口径 | ❌ pre-existing (R1′ 起未动) |
| X8 TASK-025 路径二验收恒绿 | ✅ (新写的验收条) |
| N5 类未修 + 无 issue | ❌ carryover |

三轮序列 (fix 引入占比): R2 = **83% / 62%** (两席独立测算) → R3 = **78%**。**仍 >1/2**。
我这一席的 major 计数: R2 = 2C+7M → R3 = 2C+6M(+1 carryover)。**持平**。
⇒ 按 memory `feedback_stop_adding_rounds_when_major_count_flattens` + `feedback_audit_marginal_return_goes_negative`: **不要开 R4**。

### 但本轮与 R1→R2 有一处结构性不同 (诚实标注, 不要把它读成「再来一轮就好」)

X1 / X2 **不是**沿接缝再生产的同形状缺陷 —— 它们由一个前两轮从未用过的镜头得出: **去委派目标的源码/SKILL.md 里核它到底做不做那件事**。两条的后果量级也与前两轮任何一条不同 (发布带着未 bump 的 gitlink / 子模块走服务端合并 = Aria #165 事故家族, 已 3 次复发)。
⇒ 正确读法不是「审计还没收敛」, 而是「**换镜头一次性收掉 X1/X2, 然后停止审计**」。X1/X2 的修法各是 2–4 行 + 2 个 issue, 不需要再一次整组重做。
其余 major (X3 X5 X6 X7 X8) 全是「一句替换 / 一个数字补齐 / 一条判据改可跑」, 合计改动面 < 30 行, **无一需要新增结构**。⛔ 本报告的所有 fix_direction 都是减法或替换; **没有任何一条建议新增第 7 个 metadata 块** (R2 我提过, 撤回)。

### 已核验、**未**构成发现 (留痕, 防 R4 重复投入)

1. **主仓 14 点枚举是完整的** —— 全仓 `grep -rn "1\.65\.5"` (排除 .git) 后, 6 个断言文件之外的命中**全部**是历史/审计工件 (docs/handoff ×3 / .aria/audit-reports / .aria/triage-* / 其他 Spec 的 proposal / `standards/conventions/secret-hygiene.md:401` 的账本行 / 本 Spec 自己的文件)。**无第 15 个 live 点。** 重做主张 1 (「正确单位是版本引用点, 主仓 14 点」) **成立**。
2. **两类文件的分类是对的** —— 主仓 `VERSION` 实测 37 行、只 1 处命中、是 live 子模块表, **不是**账本 (故归 normal_reference 正确); aria/VERSION 167 行、2 处命中、`发布日期(旧)` 堆叠至 v1.47.0, 归账本正确。重做主张 2 成立 (但见 X3: 分类对了, 该类的不变量还差一半)。
3. **派生值实跑一致** —— DAG 注释的 `S×14 · M×5 · L×1 / 82h / qa 10 · ba 6 · km 4 / 20 active + 7 cancelled = 27` 与 yaml:866 那条命令的实跑输出**逐字吻合**。「换成可复跑命令」这个处置有效 (前两次人工重算都错)。
4. **TASK-025 的所有行号引用无 miscitation** (`:275-277` / `:205-215` / `proposal.md:181` / `:219` 四处逐字复核 ✓)。
5. **N7 的 AD10 论据: 我 R2 引错, 本版驳回正确** —— 已接受, 不再提。
6. **N9 的「28 Skills vs Tier 1 = 10」: 我 R2 口径错, 本版更正正确** —— 已接受。
7. 依赖链 024→026 / 025 dep 009 / 027 dep 013 与 tasks.md:46 的排序叙述**逐条一致**, 无环 (实跑 dump 核)。

---

## vote

**REVISE** — 2 critical (X1 gitlink 零归属 / X2 委派路径被 CLAUDE.md 硬约束 1 禁止且使 C.2.5 不触发) 均落在「发版最后一步做错且全链无一处发红」这个方向上, 与本 Spec 全程在打的「恒红/假绿对偶」是同一件事, 不可带着进 Phase B。
其余 6 major + 3 minor 的修法全为减法/替换, 合计 < 30 行。**修完不建议再开审计轮** (占比 78% 三轮不降, 判据已到)。

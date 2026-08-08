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
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R3 — code-reviewer 席 (R1/R2 同席位)

**审计对象**: 组 5 / TG-5 **only** — `tasks.md ## 5.` 整段 + `detailed-tasks.yaml` `TASK-014` / `TASK-015..021 (cancelled)` / **`TASK-022..027`** + `metadata` 组 5 相关块 @ `2cf2569`
**⛔ 组 1–4 (TASK-001..013) 本轮不审** (owner 裁定)。凡涉及处一律标 `out_of_scope_this_round`, 不计入票。
**基线**: 我的 R2 报告 (0C + 6M + 5m = 11 条 distinct; CO-1 同时是 major 与 carryover, 故「12」是重复计数)
**镜头**: (1) R2 十一条逐条实读判闭合 (2) **重做产物自身的双向可证伪性** + **CANCELLED 台账的承接完整性** (本轮重点)

---

## 第一部分: R2 逐条闭合判定 (11/11 实读 + 实跑核验)

| R2 # | 判定 | 实读/实跑证据 |
|---|---|---|
| **CO-1** proposal.md:271 旧「文件数」口径 + 旧假绿论证, 无任务修 | **not_closed** (类已处置, 实例未处置) | `proposal.md:271` 逐字**一字未动**: 仍「aria 子模块 **5 文件** + 主仓 **gitlink** + 主仓 **`VERSION`** 的子模块版本表行 + **`README.md` 的 Plugin badge** + **`README.{zh,ja,ko}.md` 的 `translated-from` 标记**」, 并仍写「**后两项由 enabled custom check 守着** … **任何** bump 都会让三份 i18n README 判 STALE」。`python3` 扫全 27 任务 deliverables → **无 proposal.md** (唯一提及在 TASK-025 verification[2] 的 (b) 支文字里, 指 `:181/:219` 不是 `:271`, 且 proposal.md 不在该任务 deliverables)。⇒ 详见下方专项裁定 |
| **N-1** 零命中断言含 `aria/VERSION` (append-only 账本) ⇒ 恒红/销毁二难 | **closed** (主症) | `metadata.two_classes_of_file` 把 `aria/VERSION` + `aria/CHANGELOG.md` 移入 `append_only_ledger` (不做零命中, 判据=头部当前版本行 == plugin.json)。**我实跑两类判据** (下方第三部分): 当前树 ledger 半 **PASS** (非恒红) / 模拟正确 bump 后 **GREEN** / 注入「忘了 bump ledger 头部」→ **RED**。⇒ 恒红消除且非空洞。**残余见 minor C** (出让的头部发布注) |
| **N-2** 维度匹配只落主仓半幅 | **partially_closed** | ✅ TASK-015「其余 4 文件与其一致」(今天即假的那条) 已随 cancel 消失; TASK-022 改为点级 (`marketplace.json` **2** 点 `:3/:16`) — 我实测 `grep -c` = 2 ✓。❌ 但 `metadata.breakdown` **仍只有主仓 6 文件**, 而 TASK-024 verification[1] 逐字把预期点数指向它 ⇒ aria 半幅无可查预期值 (**M3, 实跑证伪**); 文件数口径仍活在 4 处 (**minor A**); `aria/VERSION:58` 的 1.47.0 仍未表态 (**minor D**) |
| **N-3** (a)/(b) 二选一放进合取型 verification + 两支均无机械判据 | **partially_closed** | ✅ 结构半幅已修: 二选一现在收进**同一个** array item (`TASK-025 verification[2]`), 不再是跨 item 的不可满足合取。❌ 判据半幅未修: 无 `chosen_branch` 字段 · 两支都仍是散文 (无可跑命令 / 无可查产物路径) · 且**未标「待 owner 确认」**(而同批的 TASK-026/027 都标了) ⇒ 见 **M4** |
| **N-4** (a) 归档后恒 FATAL / (b) proposal 指针 dangling, 两支各自未覆盖 | **closed** | TASK-025 verification[0]/[1] 把两条失效路径**分别点名**, [2] 给出对应补救 ((a)「须同时解决归档后解析路径」/ (b)「同批修 `proposal.md:181/:219` 两处 artifact 指针」)。tasks.md 5.12 同步。残余: proposal.md 不在 deliverables (**minor G**) |
| **N-5** AB 发版前清单 3抄1换1漏 + Tier 1 门收缩未披露 | **closed** (披露半幅) | TASK-027 新增, 引 `:545`「Tier 1 Skills 全量 AB 测试已执行」为成文要求 ✓, 明写「不得以改动小/纯括注/性价比降级 — Q5 是 owner 亲裁 (Rule #10)」✓, 且 `TASK-026 dependencies` 含 `TASK-027` ⇒ **结构上不能绕过它 ship** ✓。残余: owner 确认不在 verification (**M4**) · `:396` vs 实测 `:397` (**minor E**) · 「1 换」仍在 tasks.md 4.1 (组 4, out_of_scope) |
| m1 TASK-020 只有负向断言 (对「写错新值」免疫) | **closed** | TASK-024 双向 (`旧值零命中` **且** `新值出现次数 == 预期点数`)。**实跑注入 defect#4** (删掉 CLAUDE.md 一整行版本引用) → **RED** (`new=1 expect=2`) ⇒ 正向半幅真的在工作 (主仓侧) |
| m2 TASK-010 `task_group: TG-3` vs 物理落 TG-2 | **out_of_scope_this_round** | 实读 `:381` 仍 `task_group: TG-3` (未动)。组 2/3 范围, 本轮不判 |
| m3 `scope_repos[Aria].surface` 漏 `ab-results/` | **not_closed 且面变宽** | `:32` surface 逐字未变; 本轮新增 TASK-027 的 `.aria/decisions/` 同样未纳入 ⇒ 两处不闭合 (**minor I**) |
| m4 TASK-016/017 裸 `aria/` vs `aria` 语义未定义 | **moot** | 两任务均已 cancelled, 歧义随之消失 (但 gitlink 的**归属**问题转成 M2) |
| m5 `scope_repos[Aria].head: a52ab81` 陈旧 | **not_closed 且更旧** | `:31` 仍 `a52ab81`; 其间已过 `3fc6f3f` (R1-fix) 与 `2cf2569` (R2-fix) ⇒ 落后 2 个提交 (**minor B**) |

**闭合率: 4 closed / 3 partially_closed / 3 not_closed / 1 out_of_scope (+1 moot)。**

### 专项裁定 1 — 「开 Aria #177」是否构成对 CO-1 的适当处置?

**结论: 必要但不充分。类已妥当处置; 实例仍必须在本 change 内修。**

- **#177 实查为真且质量高**: `forgejo GET /repos/10CG/Aria/issues/177` → open, 2026-08-08T12:19:39Z, 标题与正文逐项对上 (四错表 + 「为什么这是类而不是实例」三次复发史 + 三条建议含两类文件分开判)。按 memory `feedback_fix_the_class_not_the_instance`, 把根因 `CLAUDE.md:81` 提到类级是**正解**, 也是 R2 我这条最想要的动作。
- **但它没有、也不能替代实例修复**, 三条理由 (逐条实测):
  1. **`proposal.md` 是本 change 唯一会被归档进 SOT 的口径面。** #177 的产出会落在 `CLAUDE.md`, 不会回头改一份已归档的 Spec。⇒ 归档后 `openspec/archive/` 里永久留一句「两条 enabled custom check 守着 … 任何 bump 都会让三份 i18n README 判 STALE」, 而这句在 R1 就被实证为**假**(该 check 只 `re.search("translated-from")`)。这是 Rule #3 (文档与代码同步) 的直接违反, 且违反物是**审计已判定为 Critical 的原文本身**。
  2. **它使本 change 内部自相矛盾。** 同一个 Spec 里 `proposal.md §Impact` 说「5 文件 + gitlink + VERSION 表行 + badge + translated-from」, 而 `tasks.md 5.9-5.11` + `metadata` 说「主仓 14 引用点 + aria 侧 4 点 + 两类不变量」。两套互斥枚举并存, 实施者读哪一份都合规。
  3. **修复成本 = 1 行。** 把 `proposal.md` 加进 TASK-023 deliverables + 加一条 verification (「§Impact 那行改为引用点口径并删除『两条 check 守着』的措辞」)。以「已开 issue」换掉 1 行的修复, 是把**便宜且确定**的实例修复替换成**昂贵且未定时**的类修复 —— 而 #177 自己的正文写着这一形状「三次都在同一个 Spec 内」。

⇒ CO-1 判 **not_closed**, 保留 major。处置建议: **两件都做** (#177 保持开着治类; 本 change 加 1 行治实例)。

### 专项裁定 2 — TASK-027 notes 对我 R2 那条的「更正」是否成立?

**成立, 但更正的对象不是我。** 逐字核验:

| 主张 | 实测 | 裁定 |
|---|---|---|
| 「`:396` 逐字为『Tier 1: 核心 Skills (**10 个**, 每次发版必测)』」 | 该标题实测在 **`:397`**, `:396` 是空行。文字本体逐字吻合 | 文字 ✅ / **行号 off-by-one ❌ (minor E)** |
| Tier 1 = 10 个, state-scanner 在内 | 表内恰 **10** 行 (`commit-msg-generator`/`arch-search`/`state-scanner`/`branch-manager`/`task-planner`/`spec-drafter`/`strategic-commit-orchestrator`/`requirements-validator`/`workflow-runner`/`agent-router`), 全 P0; `state-scanner \| 8 \| with:100% \| P0` | ✅ |
| 「R2/tech-lead 的『28 Skills / ~$14 / 6-8h』口径不是 Tier 1 全量」 | Tier 1 (10) + Tier 2 (11) + Tier 3 (7) = **28** ⇒ 28 是**三档全量**, 不是 Tier 1 | ✅ 更正成立 |
| **但那条不是我的。** | 我的 R2 报告 `:172` 逐字写「`:397` 逐字『### Tier 1: 核心 Skills (**10 个**, 每次发版必测)』」—— 我用的就是 10 与 :397 | ⇒ notes 的归属写的是 `R2/tech-lead`, **归属正确**; owner 提示里「对你那条的更正」是转述误差, 不需要我认领 |
| owner 的「`:483` 在『短期 (1-3 个月)』路线图段而非规范条款」 | 实测 `:480 ### 短期 (1-3 个月)` 属 `## 数据积累策略`; `:483` 在其下。**owner 判断正确** | ✅ |
| ⚠️ 但这不削弱那道门 | `:530 ## 检查清单` → `:544 ### 发版前` → `:545 - [ ] Tier 1 Skills 全量 AB 测试已执行` —— **这是清单条款不是路线图**, 独立成立。TASK-027 notes 恰恰引的是 `:545` ⇒ **fix 没有拿「:483 是路线图」去消解那道门**, 处理是诚实的 | ✅ 这是本轮 fix 做得最干净的一处 |

---

## 第二部分: 结构化发现

```yaml
- type: issue
  severity: critical
  category: architecture
  scope: >
    detailed-tasks.yaml metadata.scope_boundary.delegated[phase-c-integrator] · TASK-016 cancel_reason:529 ·
    TASK-017 superseded_by:557 · TASK-026 verification[0..2] · tasks.md 5.3 / 5.4 / 5.13 ·
    aria/skills/phase-c-integrator/SKILL.md §C.2.5:570-600 + :236 · aria/skills/branch-manager/SKILL.md:528,625-641,664-674
  origin: new
  summary: >
    委派的**前提在目标处不成立**。本文件断言「C.2.5 正是 TASK-016 手工重写的东西」并据此删掉 TASK-016 的
    四条硬判据 + 明令 TASK-026「不复述」。实读被委派方: **C.2.5 = Multi-Remote Push Enforcement, 只推不合并**
    (触发条件逐字「Phase C.2 合并成功 (master 已 fast-forward)」—— 合并是它的**前置**不是它的内容);
    真正执行合并的是 branch-manager, 其 SKILL 唯一成文的合并机制是 **Forgejo API `POST .../pulls/{n}/merge`
    `{"Do":"squash"|"merge"}` = 服务端合并**。⇒ TASK-016 的第一条判据 (⛔ 未使用 Forgejo Web UI/API 的服务端
    merge) 与 TASK-017 的 gitlink 判据 (指向**合并后 master SHA** 而非 feature SHA) **在整条委派链上无落点**,
    而这两条恰是 CLAUDE.md「多远程推送 — 两条硬约束」(owner 裁决 2026-07-20, 根治 Aria #165) 的本体。
  evidence: >
    (1) `phase-c-integrator/SKILL.md` 全文 grep 「本地」/「服务端」/「两条硬约束」→ **零命中** (唯一「本地」在
    `:583`「快照 expected_sha = git rev-parse HEAD (合并后**本地** master HEAD)」—— 那是**假设**本地已合并, 不是约束);
    `grep -n "gitlink"` 4 处全在 C.2.4.5 审计与 nil-SHA 分支, **无一处 bump gitlink**。
    (2) `phase-c-integrator/SKILL.md:236` 逐字「branch-manager (C.2.4-C.2.5) | wait approval + **merge API call**」
    (归属核对: 这一行在 phase-c-integrator 的边界表里, 不在 branch-manager 自己的文件中);
    `branch-manager/SKILL.md:528` 「C.2.5 - 合并 (可选, auto_merge=true 时)」, `:625-641` 三个 curl 示例全是 `{"Do": "squash"}` / `{"Do": "merge"}`; `:664-674`「子模块 PR 流程: 1. 在子模块
    仓库创建 PR 2. **合并后**, 回到主仓库 3. 更新子模块指针: `git add {submodule_path}`」—— 裸 `git add`, **无任何
    SHA 核验**。⇒ 服务端合并后本地子模块工作树仍在 feature 分支 ⇒ `git add` 记进 feature SHA = **orphaned gitlink**。
    (3) 机械兜底不覆盖: C.2.4.5 (`mode=block` 默认) 实读算法 `:418-440` 判的是
    `git merge-base --is-ancestor MASTER_PTR FEATURE_PTR` (forward bump)。**feature 分支提交天然是旧 master gitlink
    的后代 ⇒ 该 gate PASS**, 而 SHA 在子模块 master 上不可达 —— 正是 2026-07-14 事故的签名 (CLAUDE.md 约束 1
    自己写着「主仓随后 bump gitlink 即产生 orphaned gitlink, GitHub clone --recursive 断裂」)。
    (4) 真正 land 的三条: 双推 ✅ (C.2.5 步骤 4a/4c per-remote matrix) · 逐远端 ls-remote ✅
    (`git-remote-helper/SKILL.md:40` `verify_parity_post_push` 「纯读 — 仅 git ls-remote 查询」) ·
    不信 push 回执 ✅ (verify 独立于 push 返回)。**4 条中 1 条 + gitlink 判据共 2 项无落点。**
  fix: >
    委派**执行**没问题, 但不能同时委派**验收**。TASK-026 加两条**结果态**断言 (不是复述 C.2.5 步骤, 故不违 owner
    的「不复述」): (a)「`git -C aria rev-parse master` == 主仓 gitlink 记录的 SHA, 且该 SHA 在 origin 与 github
    两个远端均 `ls-remote` 可达」; (b)「aria 子模块 master 的推进是本地 fast-forward 产生 (`git -C aria reflog`
    可见 merge), 非服务端合并回填」。或按 Rule #10 上报 owner: 委派链缺这两条约束, 请裁定是补进 TASK-026 还是
    补进 phase-c-integrator SKILL (后者更根治, 可另开 issue)。

- type: issue
  severity: major
  category: testing
  scope: >
    detailed-tasks.yaml metadata.scope_boundary.delegated[phase-d-closer].why:65 · tasks.md:100-106 (CANCELLED 台账)
  origin: new
  summary: >
    「编号保留 + CANCELLED 台账」与**已启用的归档完成度闸门**结构性冲突, 且本文件对该闸门的描述在目标处为假。
    7 条 cancelled 在 tasks.md 里仍是 `- [ ] ~~5.2 …~~` **未勾选 checkbox**; `spec_complete.py` 的
    `_CHECKBOX_RE` 只认 `[x]/[X]`, 不认删除线/CANCELLED 语义 ⇒ 本 Spec 永远拿不到 `complete=true` 的
    tasks 分支; 而 yaml 分支的 `_DONE_FAMILY = {"done","completed"}` **不含 `cancelled`** ⇒ 两条路都判非完成。
    ⇒ Phase D 只剩三条出路: **恒红阻断** / 把 cancelled 勾成 `[x]` (**假绿**: 声称取消的工作已做) /
    走 `Status=done` 右半绕过 —— 后者会把 7 条 cancelled 原样写进自动生成的 archive-tracker issue 的
    「未完成/deferred 项」正文。本 Spec 全程在打「恒红 = 假绿的对偶」, 台账设计自己制造了这个二难。
  evidence: >
    **实跑** `python3 aria/skills/state-scanner/scripts/lib/spec_complete.py --gate openspec/changes/linked-issue-normalization`
    → `{"complete": false, "complete_reason": "tasks.md has **27/27** unchecked task(s); normalized Status = 'pending'"}`,
    且 `d_payload.deferred_items` 含全部 7 条 cancelled 行, 每条 `"reason": "unchecked"`、
    `"parent_id": **null**` (删除线使 `5.2` 编号解析不出来 ⇒ tracker 正文连编号都没有)。
    代码实读: `spec_complete.py:273-278` `boxes = _CHECKBOX_RE.findall(...)`; `unchecked = [b for b in boxes
    if b not in ("x","X")]`; `:189-229` `_yaml_only_tasks_verdict` 仅在 **tasks.md 缺失时**启用 (本 Spec 有
    tasks.md ⇒ yaml 的 `status: cancelled` 根本不被消费);
    `detailed_tasks.py:83` `_DONE_FAMILY = frozenset({"done","completed"})`。
    ⇒ metadata `:65` 逐字「归档门会消费**本文件**全部 27 个 checkbox 状态 (20 active + 7 cancelled), 故组 5
    必须真做完而非声称」**三处失实**: 消费的是 tasks.md 不是本文件 · 本文件没有 checkbox · 闸门无法区分
    cancelled 与未完成 (memory `feedback_cross_doc_claim_verify_at_target` + `feedback_verify_predicate_inputs_exist`)。
  fix: >
    把 7 条 CANCELLED 从 checkbox 语法里挪出去 (编号照留): `- [ ] ~~5.2 …~~` → 表格行或裸 `- ~~5.2 …~~`。
    这样 `boxes` = 20, 全做完即 `complete=true`, 编号不可变约束与十份报告的引用同时保住, 且不需要任何
    「勾选取消项」的假声称。同时把 metadata `:65` 那句按实测重写。

- type: issue
  severity: major
  category: testing
  scope: >
    detailed-tasks.yaml TASK-024 verification[0][1] · metadata.version_reference_surface.breakdown:103-109 ·
    aria_side_points:130 · tasks.md 5.11 第 1 类
  origin: new
  summary: >
    双向断言的**aria 半幅没有预期值可查** ⇒ 「写错新版本号」这一维度在 aria 侧仍然免疫 —— 正是本条要修的
    那个半维度缺陷, 在同一批编辑里换了个仓复现 (memory `feedback_fix_recurs_in_its_own_fallback_path`)。
    verification[1] 逐字「预期点数**先枚举后断言** — 见 `metadata.version_reference_surface.breakdown`」,
    而 `breakdown` 只有主仓 6 个文件 (2/3/3/3/2/1); aria 侧三个普通引用文件在 breakdown 里**零条目**,
    唯一相关文字是 `aria_side_points` 的散文, 且那句自己数错 (「**4 个普通引用点文件**」—— 实为 **3 个文件 / 4 个点**)。
  evidence: >
    **实跑双向可证伪性测试** (脚本按 TASK-024 两类判据实现, 对当前树 + 模拟 bump + 5 个注入缺陷各跑一次):
      当前树 (pre-bump)                     → RED  ✅ 非空洞
      模拟正确 bump                          → GREEN ✅
      注入 defect#1 漏改 marketplace.json:16 → RED  ✅ (零命中半幅抓住)
      注入 defect#2 zh badge 写成 1.66.O     → RED  ✅ (主仓正向计数抓住)
      注入 defect#4 删掉 CLAUDE.md 一整行    → RED  ✅ (删行也抓住, R2/tech-lead N3 关闭)
      **注入 defect#3 aria/README.md 写成 1.66.O → GREEN ❌**
    最后一条即本条: `aria/README.md:5` 由 `> **Version**: 1.65.5` 改成 `1.66.O` 时, 旧值零命中成立、
    而没有任何预期计数可比 ⇒ 全绿。同理适用 `plugin.json` / `marketplace.json` 的错值写入
    (`marketplace.json` 尤其危险: 两个点写成一个对一个错时零命中仍可能成立)。
  fix: >
    `breakdown` 补三条 (`aria/.claude-plugin/plugin.json: 1` / `aria/.claude-plugin/marketplace.json: 2` /
    `aria/README.md: 1`, 我已实测 = 1/2/1), 并把 `aria_side_points` 的「4 个普通引用点文件」改为
    「3 个文件 / 4 个引用点」。更省事的合并修法: 把 TASK-024 落成一个可复跑脚本
    (`.aria/repro/version-surface-assert.py`, 输入 plugin.json 版本, 输出逐文件逐点比对 + 账本头部比对) ——
    本文件 footer `:864-871` 已经为派生计数做过同一件事并成文了理由 (「不变量写进文档 ≠ 写进机械兜底」,
    memory `feedback_invariant_needs_failclosed_default`), 唯独本 Spec 的旗舰机械断言还停在散文。

- type: issue
  severity: major
  category: architecture
  scope: >
    detailed-tasks.yaml TASK-025 verification[2] · TASK-026 notes:806-810 · TASK-027 notes:836 ·
    tasks.md 5.12 / 5.13 / 5.14
  origin: new (含 R2 N-3 的未闭半幅)
  summary: >
    三个 owner 裁量项**只活在 title/notes, 没有一条进 verification** ⇒ 三条任务都能在 owner 从未表态的
    情况下判绿并推进到 ship。Rule #10 的豁免白名单是封闭四类, 「AI 建议 + 自行执行 + 事后披露」不在其中。
  evidence: >
    (1) TASK-025: 两支择一无 `chosen_branch` 字段、两支都无可跑命令/可查产物路径、且**连「待 owner 确认」
        都没标** —— 而 (a)/(b) 的后果不对称 ((b) 会动 owner 2026-08-08 裁定 (db2e983) 所依赖的
        `proposal.md:181/:219` artifact 指针), 属典型 owner 裁量。
    (2) TASK-026 notes 逐字「**推送授权 (AI 建议, 待 owner 确认)**: … **每次推前须 owner 显式确认**;
        AI 可执行但不得自我授权」—— 而 verification 三条是 024 已过 / 交接告知 / 不复述判据, **无一条**
        要求「owner 已确认」。
    (3) TASK-027 title 与 notes 结尾都写「**待 owner 确认**」, verification 三条 = 成文披露 / 开 issue /
        不得以性价比降级, **同样没有 owner 确认那条**。而它守的是 Rule #6 + `:545` 发版前清单, Q5 是 owner 亲裁。
    ⇒ 三条 checkbox 勾上的充分条件里都不含 owner 的动作 (memory
    `feedback_falsifiable_evidence_for_binary_acceptance` + `feedback_ai_must_not_self_exempt_enabled_gates`)。
  fix: >
    每条加一条 verification: 「owner 已在 `<handoff 文件 / decision sheet 路径>` 就 `<该裁量项>` 表态,
    并回录裁定于本任务 notes」。TASK-025 另加 `chosen_branch: a|b` 字段 + 每支一条机械判据
    ((a) `python3 .aria/repro/sc-baseline-*.py <path>` → exit 0; (b) 断言 `.aria/repro/` 下已无该文件
    **且** 存档路径存在且内含 aria 子模块 SHA)。三条都属「写进 handoff 请复议」而非 AI 自决。

- type: issue
  severity: major
  category: documentation
  origin: carryover
  scope: openspec/changes/linked-issue-normalization/proposal.md:271 · TASK-023 deliverables
  summary: >
    CO-1 未闭。见第一部分「专项裁定 1」: `proposal.md:271` 逐字未动 (旧「5 文件」口径 + 旧假绿论证),
    27 个任务无一以 proposal.md 为 deliverable。开 Aria #177 妥当地处置了**类**根因 (`CLAUDE.md:81`),
    但不处置这个**实例** —— 它是本 change 唯一会被归档进 SOT 的口径面, 且与本 change 自己的
    tasks.md/metadata 互斥并存。
  evidence: >
    `sed -n 271p proposal.md` 与 R2 引文逐字一致 (含「**后两项由 enabled custom check 守着**」与
    「**任何** bump 都会让三份 i18n README 判 STALE」两句假绿论证);
    `python3` 遍历 27 任务 deliverables → proposal.md 零命中;
    `forgejo GET /repos/10CG/Aria/issues/177` → open, 内容与该行四错逐项对应, 但其 scope 是 CLAUDE.md。
  fix: "proposal.md 加进 TASK-023 deliverables + 一条 verification (§Impact 改引用点口径 + 删「两条 check 守着」)。1 行成本。"

- type: issue
  severity: minor
  category: documentation
  origin: carryover           # R2 N-2 第三腿
  scope: detailed-tasks.yaml :28 · :110 · :130 · :474 (TG-5 banner)
  summary: >
    「文件数」口径在 4 处存活, 其中 TG-5 banner 一句里混两种单位。整组重做的立意是换掉这个维度,
    但 banner 与 metadata 的门面没跟上。
  evidence: >
    `:28` `surface: "… · **5 个版本文件**"`; `:110` `plus: "主仓 gitlink (非文本引用) + aria 子模块 **5 文件**"`;
    `:130` 「**4 个普通引用点文件**中 marketplace.json 含 2 个 version 字段」(实为 3 文件 4 点);
    `:474` `# TG-5 — 回归 + 发版同步面 (14 个主仓版本**引用点** + gitlink + aria **5 文件**) …`。
    (`:499` / `:654-655` / tasks.md `:100` 的「5 文件」是 cancelled 条目与订正史引文, **正确保留**。)

- type: issue
  severity: minor
  category: documentation
  origin: carryover + new
  scope: detailed-tasks.yaml metadata.scope_repos[Aria].head:31 · total_tasks:39
  summary: "两处 metadata 卫生: (1) 主仓 head 锚落后 2 个提交; (2) 指向一个不存在的 key。"
  evidence: >
    (1) `:31` `head: "a52ab81"`, 而实际已过 `3fc6f3f` (R1-fix) 与 `2cf2569` (R2-fix, 本轮 HEAD)。
        我实测本轮引用的全部主仓行号 (CLAUDE.md:139/141 · README.md:8/242 · README.{zh,ja,ko}.md:3/10/244 ·
        VERSION:24) 在 `2cf2569` 下逐条命中, 故只是锚陈旧不是引用错误。
    (2) `:39` `total_tasks: 27   # 20 active + 7 cancelled (编号保留, **见 cancelled_ledger**)` ——
        全文件 grep `cancelled_ledger` 仅此 1 命中, **该 key 不存在** (dangling ref)。

- type: issue
  severity: minor
  category: documentation
  origin: carryover (R2 N-1 后半)
  scope: detailed-tasks.yaml TASK-022 verification[1] · TASK-024 verification[2] · aria/VERSION:4
  summary: >
    「历史行原样保留」对**出让的头部发布注** (`:4`) 未定义, 而该文件自己的 bump 史里两种做法并存;
    账本不变量对它免疫 ⇒ 销毁 v1.65.5 的发布注可以全绿通过。
  evidence: >
    `git -C aria show af87cae -- VERSION`: `- > **发布日期**: … v1.65.4 …` / `+ > **发布日期**: … v1.65.5 …`
    ⇒ v1.65.4 的发布注**被删**未降级为 `发布日期(旧)`; `git -C aria show 9a199c9 -- VERSION` 同形态
    (v1.65.1 那行被删), numstat `2 2 VERSION`。而当前文件 `:5`/`:6` 又确实存在 v1.65.2 / v1.65.1 的
    `发布日期(旧)` 行 ⇒ 同一文件四个提交内两种相反惯例并存。
    **实跑注入 defect#5** (按 af87cae 惯例覆写 `:4`, 销毁 v1.65.5 发布注) → **GREEN**
    (头部当前版本行 == plugin.json 仍成立)。
  fix: "TASK-022 verification[1] 明确写「`:4` 降级为 `发布日期(旧)` 后追加新行 (不得覆写)」或反之, 二选一钉死。"

- type: issue
  severity: minor
  category: documentation
  origin: carryover (R2 N-2(b))
  scope: metadata.two_classes_of_file.append_only_ledger · aria/VERSION:55-58
  summary: >
    `aria/VERSION` 被**整文件**归类为 append-only 账本, 而 `:55 ## 版本号` / `:58` 那个围栏代码块是
    「当前版本」声明 (实测 **1.47.0**, 落后 18 个 minor)。两类不变量都看不到它, 且没有任务/verification
    对它表态 (在范围内还是外)。同文件两性质并存 ⇒ 应逐 hunk 判, 不能按文件判。
  evidence: >
    `grep -n` → `:55 ## 版本号`, `:58 1.47.0`。该文件 `:16` 自己记着这个坑的历史:
    「#158 aria-report 版本抽取修复: … 恒命中围栏代码块**冻结串 1.47.0**, 污染所有生成 issue 的版本字段
    + 连带 triage 版本筛失效」⇒ 它已经造成过一次真实缺陷。
    因不含 `1.65.5`, 零命中断言看不见; 因不是「头部当前版本行」, 账本不变量也看不见。
  fix: "metadata 里一句「`aria/VERSION:55-58` 的 1.47.0 是既存漂移 (#158 已修消费侧), **不在本 Spec 范围**」即可 —— 避免实施者顺手扩范围, 也避免下一轮审计重报。"

- type: issue
  severity: minor
  category: documentation
  origin: new
  scope: detailed-tasks.yaml TASK-027 notes:828 · tasks.md 5.14
  summary: "更正别人行号的那句话自己行号错一位: 引 `:396`, 实测该标题在 `:397` (`:396` 是空行)。"
  evidence: >
    `grep -n "Tier 1: 核心 Skills" aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` → `397:`。
    同 notes 里的 `:545` 实测正确 (`545:- [ ] Tier 1 Skills 全量 AB 测试已执行`)。
    (memory `feedback_critique_repeats_the_error_it_names` 的一个温和实例。)

- type: issue
  severity: minor
  category: documentation
  origin: new
  scope: detailed-tasks.yaml TASK-022 deliverables:703 / verification[0..4] · aria/README.md:5
  summary: >
    `aria/README.md` 在 deliverables 里但**零条 verification 提到它**; 且它的 `**Released**: 2026-08-02`
    是发版面字段而所有不变量都只看版本号维度 ⇒ 写成 `Version: 1.66.0 | Released: 2026-08-02` (陈旧日期)
    全绿通过。同族: `aria/VERSION:4` 的日期、`aria/CHANGELOG.md` 的 `## [1.66.0] - <date>`。
  evidence: >
    TASK-022 五条 verification 逐字提到 plugin.json / marketplace.json / aria/VERSION / aria/CHANGELOG.md /
    CHANGELOG+README 措辞 / MINOR-vs-PATCH — 无一条断言 aria/README.md 已改。
    `sed -n 5p aria/README.md` → `> **Version**: 1.65.5 | **Released**: 2026-08-02`。

- type: issue
  severity: minor
  category: documentation
  origin: new
  scope: detailed-tasks.yaml TASK-025 deliverables:778 vs verification[2] (b) 支
  summary: "(b) 支要求「同批修 `proposal.md:181/:219` 两处 artifact 指针」, 而 proposal.md 不在该任务 deliverables ⇒ 选 (b) 时交付面声明即刻不闭合。"
  evidence: "TASK-025 `deliverables:` 仅 `.aria/repro/sc-baseline-linked-issue-normalization.py` 一项。"

- type: issue
  severity: minor
  category: testing
  origin: new
  scope: 已 cancelled 的 TASK-017 verification[2]:571 / TASK-018 verification[2]:596 → 无 active 任务承接
  summary: >
    两条 **enabled** custom check 的「须跑并见 OK」要求随 cancel 消失: 全文件 grep `custom check` 只剩
    `:571` / `:596` 两处 (皆在 cancelled 任务内)。TASK-023/024 都不要求跑它们。
  evidence: >
    `.aria/state-checks.yaml:88-102` `m6-version-badge-match` `enabled: true` (severity warning);
    `i18n-readme-translation-currency` 同为 enabled。
    **裁定为 minor 而非 major**: 二者的比对内容 (badge / translated-from 对 plugin.json) 在数值层被
    TASK-024 的 `1.66.0` 逐点断言覆盖 ⇒ 覆盖等价, 丢的是「要求跑」而非「覆盖面」; 且它们在任何
    state-scan 里照常执行, 不构成 Rule #10 的自行豁免。建议 TASK-023 补一句回执即可。

- type: issue
  severity: minor
  category: documentation
  origin: carryover + new
  scope: detailed-tasks.yaml metadata.scope_repos[Aria].surface:32
  summary: >
    主仓 surface 与 active deliverables 并集仍不闭合, 且本轮变宽: 缺 `aria-plugin-benchmarks/ab-results/`
    (R2 已报, 未修) **与** 新增的 `.aria/decisions/` (TASK-027 的唯一 deliverable)。
  evidence: >
    `:32` 逐字「gitlink · VERSION · README.md · README.{zh,ja,ko}.md · CLAUDE.md · Spec 本体 · .aria/repro/」;
    实测 active deliverables 并集 18 项, 其中 `.aria/decisions/` 与 `aria-plugin-benchmarks/ab-results/` 不在 surface 内。
    反向: surface 列了 `gitlink` 而**无任何 active 任务以它为 deliverable** (见 critical 那条)。

- type: issue
  severity: minor
  category: documentation
  origin: out_of_scope_this_round     # 组 4, 不计入本轮票
  scope: tasks.md 4.1 (TASK-013)
  summary: >
    R2 N-5 的「1 换」未修: tasks.md 4.1 仍写「按 … **发版前清单** —— (a) `with_skill` 表现优于 `without_skill`」,
    而该条实测在 `:542 ### 新增 Skill 后`, 不属 `:544 ### 发版前`。记录备查, 组 4 本轮不审不计票。
  evidence: "`sed -n '538,548p' AB_TEST_OPERATIONS.md` — `:542` 属「新增 Skill 后」; 发版前四条为 `:545-548`。"
```

---

## 第三部分: 本轮实跑核验 (ground truth, 不采信自述值)

### 3.1 派生数字重算 — 全部正确 (两法互证 + 前例第三方验证)

我不采信 footer 自述, 独立跑 + 手工加总:

| 项 | 自述 | 我实测 | 判定 |
|---|---|---|---|
| total | 27 | `len(tasks)` = **27** (TASK-001..027 连续无缺号) | ✅ |
| active / cancelled | 20 / 7 | `status!='cancelled'` = **20**; cancelled = **7** = 恰 `TASK-015..021` | ✅ |
| 复杂度 | S×14 · M×5 · L×1 | `Counter` = **{'S':14,'M':5,'L':1}** (14+5+1=20 ✓) | ✅ |
| 工时 | 82h | 锚公式 14×3+5×6+1×10 = **82**; 逐条 `est_hours` 相加 = **82** ⇒ **两法互证** | ✅ |
| Agent | qa10 · ba6 · km4 | `Counter` = **{'qa-engineer':10,'backend-architect':6,'knowledge-manager':4}** (10+6+4=20 ✓) | ✅ |
| parent 唯一性 | — | 20 个 active parent 互不重复, 与 tasks.md 的 20 个**非 cancelled** checkbox 一一对应 (`1.1-1.6, 2.1-2.3, 3.1-3.3, 4.1, 5.1, 5.9-5.14`) | ✅ |
| 依赖完整性 | — | 无 active 任务依赖 cancelled 任务; 无悬空 dep id; DAG 注释 7 条边与 20 条 `dependencies` 逐条一致 (含 `014` 的 7 个前驱 · `026` 的 `[024,025,027]` · `025` 挂 `[009]`) | ✅ |
| 主仓 14 引用点 | 14 | 逐文件 `grep -c "1\.65\.5"`: README.md **2** / zh **3** / ja **3** / ko **3** / CLAUDE.md **2** / VERSION **1** = **14**, 与 breakdown 逐格相同 | ✅ |
| **前例第三方验证 (新增)** | — | `git show fb5ed36 --numstat` (上一次 v1.65.5 发版同步 commit) = `2 2 CLAUDE.md / 3 3 ja / 3 3 ko / 2 2 README.md / 3 3 zh / 1 1 VERSION`, 且该 diff 的 `^+.*1\.65\.5` 计数 = **14** ⇒ 14 点分布**被真实执行史独立证实** (memory `feedback_spec_precedent_verify_execution_history`) | ✅✅ |
| aria 侧点数 | 散文「4 个普通引用点文件」 | 实测 **3 个文件 / 4 个点**: plugin.json 1 · marketplace.json 2 (`:3`/`:16`) · aria/README.md 1。前例 `git -C aria show 9a199c9 --numstat` = `2 2 marketplace / 1 1 plugin.json / 32 0 CHANGELOG / 1 1 README.md / 2 2 VERSION` ⇒ 普通引用点 **4** ✓ 且 CHANGELOG 是纯追加 (32/0) ✓ | ⚠️ 数对/措辞错 (minor A) |
| 主仓自身版本 (1.7.3) 是否该 bump | 未列入 | 实测 `fb5ed36` / 前 6 个 release commit **均未** bump 主仓自身版本 (VERSION `:3` 与 `最后更新: 2026-07-21` 未动), 只改子模块表行 ⇒ **不列入是对的**, 非漏项 | ✅ (我自己的怀疑被证伪) |

### 3.2 TASK-024 两类判据实跑 (owner 点名项)

按 TASK-024 两类不变量写成脚本, 对 **当前工作树** + **模拟正确 bump** + **5 个注入缺陷** 各跑一次:

| 场景 | 期望 | 实测 | 结论 |
|---|---|---|---|
| 当前树 (pre-bump) | RED | **RED** (6 文件全 FAIL) | 非空洞 ✅ |
| 模拟正确 bump | GREEN | **GREEN** (11 文件全 PASS) | 不恒红 ✅ |
| 漏改 `marketplace.json:16` | RED | **RED** (`old=1`) | 零命中半幅有效 ✅ |
| `README.zh.md` badge 写成 `1.66.O` | RED | **RED** (`new=2 expect=3`) | 正向半幅有效 ✅ |
| 删掉 `CLAUDE.md` 一整行引用 | RED | **RED** (`new=1 expect=2`) | R2/tech-lead N3 关闭 ✅ |
| `aria/README.md` 写成 `1.66.O` | RED | **GREEN** | ❌ **M3** |
| 销毁 `aria/VERSION:4` 的 v1.65.5 发布注 | RED | **GREEN** | ❌ minor C |

**分类正确性**: 两类名单对当前树**无漏无多** —— 全仓 `grep -rn "1\.65\.5"` 后, 11 个名单文件之外的命中只剩四类正确不动的:
工具产物快照 (`.aria/triage-comment.md` / `triage-report.json`) · 溯源注 (`.aria/repro/sc-baseline-*.py:32`) ·
审计史与 handoff (`.aria/audit-reports/*` / `docs/handoff/*` / `standards/conventions/secret-hygiene.md:401` 的 changelog 行) ·
另一个 Spec 自带 re-check 声明的引用 (`openspec/changes/secret-guard-per-segment-evaluation/proposal.md:138`「SOT 现 1.65.5; **bump 前 re-check**」)。
**account-only 判据的一个正面性质** (我原本怀疑它是恒真): 它对 plugin.json 取值 ⇒ 「忘了 bump 账本头部」或
「CHANGELOG 条目追加在文件尾部」都会 RED, 不是恒绿装饰。

### 3.3 CANCELLED 台账承接完整性 — 逐条 diff (owner 点名项)

| cancelled | superseded_by | 原条内容逐项是否 land | 静默丢失 |
|---|---|---|---|
| TASK-015 (5.2) | TASK-022 | 5 个 deliverables ✅ · MINOR-not-PATCH ✅ · 「不得写成已覆盖全部别名」✅ (还扩到 README) · 「其余 4 文件与其一致」正确删除 ✅ | 无 (notes 里 v1.65.2 PATCH 先例的理据未带过来, 无实质) |
| TASK-016 (5.3) | "phase-c-integrator C.2.5" | 双推 ✅ · 逐远端 ls-remote ✅ · 不信 push 回执 ✅ · **⛔ 禁服务端 merge ❌** | **1 项丢失 → critical** |
| TASK-017 (5.4) | TASK-023 + TASK-026 | README.md 两处 ✅ · VERSION 表行 ✅ · badge check 要求 ⚠️(minor H) · **gitlink 指向合并后 master SHA ❌** · **`aria` gitlink deliverable ❌** | **2 项丢失 → critical** (deliverable 半幅在 `scope_boundary.delegated` 有记载, 判定为「有记录但无验收」) |
| TASK-018 (5.5) | TASK-023 | 三份 ×3 处 = 9 ✅ · 不重译正文 (#140 B 档) ✅ · i18n check 要求 ⚠️(minor H) | 无实质 |
| TASK-019 (5.6) | TASK-023 | CLAUDE.md 两处 ✅ · 不污染 AB baseline (#116) ✅ · 15-20 行预算 + 覆写非追加 ✅ | 无 (**三条全带过来**, 本表最干净的一条) |
| TASK-020 (5.7) | TASK-024 | 零命中 ✅(缩到普通文件) · git status 不带路径 ✅ · **可复跑 grep 命令 → 退化为散文** ⚠️ | 机械性降级 (并入 M3) |
| TASK-021 (5.8) | TASK-025 | 恒红路径 ✅ · 归档 FATAL 路径 ✅(新增) · (a)/(b) 两支 ✅ · substitute 可复核性 ✅ | 无 (但判据形态未改进, 见 M4) |

**编号不可变约束**: 7 条 cancelled 的 `id`/`parent`/`title`/`verification` 原文冻结, 未原地改指 ⇒ R1/R2 十份报告对 `TASK-015..021` 的引用继续成立 ✅ (R2/tech-lead N6 关闭, 这一条做得对)。

---

## 第四部分: 确认做对的 (逐条实证)

1. **派生数字 8/8 全对, 且第一次有了第三方前例验证** —— 主仓 14 点分布与上一次真实发版 commit `fb5ed36` 的 numstat 逐格吻合 (2/3/3/2/3/1, +行含旧版本号计数 = 14)。这比任何自述都强。
2. **恒红对偶真的被杀掉了**: `aria/VERSION` 重归类后, 我实跑当前树该半幅 PASS、模拟 bump 后 PASS、忘 bump 则 RED —— R2 最重的那条 (N-1) 是用**结构**关掉的, 不是用措辞。
3. **正向半幅经删行注入验证有效**: 删掉一整行版本引用 → RED。R2/tech-lead N3 (「缺席断言只对一半」) 在主仓侧真闭合。
4. **断言排到不可回退点之前**: `TASK-024 verification[4]` + `TASK-026 dependencies: [024,025,027]` + DAG `024 ──▶ 026` 三处一致, 我按 20 条 deps 做拓扑核对无矛盾 ⇒ R2/tech-lead N4 闭合。
5. **AB 门这次处理得诚实**: 引的是 `:545` 清单条款 (不是 `:483` 路线图), 且 `TASK-026` 依赖 `TASK-027` 使它结构上不可绕过, 并明写「不得以改动小/纯括注/性价比降级 — Q5 是 owner 亲裁」。这是 Rule #10 语境下少见的正确姿势 (缺的只是 owner 确认那一条验收, M4)。
6. **`#177` 是本轮最有价值的动作**: 我实查 issue 正文, 四错逐条与实测吻合, 且第三条建议已经是正解 (两类文件分开判 + 恒红警告)。类级处置方向完全正确 —— 只是不能用它替代 1 行的实例修复。
7. **编号冻结 + CANCELLED 台账保住了十份报告的引用**, 未复现 R1-fix 原地改指造成的静默错位。
8. **主仓自身版本不 bump 的判断是对的** —— 我怀疑这是漏项, 实测前 6 个 release commit 全部只改子模块表行, 我的怀疑被证伪。

---

## Verdict

**verdict: FAIL** (**1 Critical + 4 Major + 8 Minor**)
**vote: REVISE**

Critical 的判定理由: 按计划字面执行, 子模块合并可能走 branch-manager 成文的服务端 API merge, 主仓随后以裸 `git add` 记进 feature SHA, 而 C.2.4.5 的 ancestry 检查对这一形态 **PASS** ⇒ 结构性复现 CLAUDE.md 自己记载的 2026-07-14 orphaned gitlink 事故 (GitHub `clone --recursive` 断裂)。这不是文档瑕疵, 是可导致已发布镜像损坏的执行面缺陷, 且它是**删掉 TASK-016 时连带删掉的唯一守卫**。

### 阻塞项

| # | 项 | 落点 | origin |
|---|---|---|---|
| **C-1** | 委派前提在目标处不成立: C.2.5 只推不合并; 合并是 branch-manager 的服务端 API; 「禁服务端 merge」与「gitlink 指向合并后 master SHA」两条无落点 | TASK-026 · metadata.scope_boundary | new |
| M-1 | 7 条 CANCELLED 仍是 `- [ ]` ⇒ 归档门实测 27/27 unchecked, `cancelled` ∉ done-family ⇒ 恒红 / 假绿 / phantom deferred 三选一 | tasks.md:100-106 · metadata:65 | new |
| M-2 | 双向断言 aria 半幅无预期点数 ⇒ 实跑证伪 (aria/README.md 错值写入判绿) | TASK-024 · breakdown | new |
| M-3 | 三个 owner 裁量项只在 notes 不在 verification ⇒ 可无 owner 表态判绿 ship | TASK-025/026/027 | new |
| CO-1 | `proposal.md:271` 旧口径 + 旧假绿论证仍在, 无任务修 (#177 治类不治实例) | proposal.md:271 | carryover |

### fix 引入占比 (拐点判据)

| 口径 | 计算 | 结果 |
|---|---|---|
| **Critical+Major 中 fix 引入占比** | 4 (C-1 / M-1 / M-2 / M-3) / 5 (含 CO-1) | **80%** |
| Major only (排除 critical) | 3 / 4 | **75%** |
| 全部 finding 中 fix 引入占比 | 8.5 / 13 (carryover 4 条 + 1 条 mixed; out_of_scope 那条不计) | **≈65%** |
| **Major-and-above 跨轮 (本席位)** | R1 = 7 (1C+6M) → R2 = 6 (0C+6M) → R3 = **5 (1C+4M)** | **首次下降** |
| Major-only 跨轮 | 6 → 6 → **4** | **首次下降** |

**双判据读数分歧, 要分开读**:
- `feedback_stop_adding_rounds_when_major_count_flattens` (加轮判据 = major 是否还在降): **不再点亮** —— 整组重做把 major 从 6 降到 4, 这是三轮里第一次真下降。⇒ 「按规律重做」比「逐条补丁」有效, owner 那个裁定是对的。
- `feedback_audit_marginal_return_goes_negative` (判据 = 本轮 fix 引入的 major 占比 > 1/2): **仍点亮 (80%)** —— 剩下的 5 条里 4 条是这次重做新造的。⇒ 我们没有走出「每次重写再生产约 4 个同形状缺陷」的regime, 只是把每轮产量从 5-6 降到 4。

### 给 R4 的处置建议 (**不建议再开一轮同席位审计**)

1. **五条阻塞项全部是「一句话可机械指定」的**, 不需要再审一轮来发现更多: C-1 加两条结果态断言 · M-1 去掉 7 个 `- [ ]` 前缀 · M-2 往 breakdown 补三行数字 (我已实测 1/2/1) · M-3 三条各加一条 owner-确认验收 · CO-1 把 proposal.md 加进 TASK-023。**总编辑量 < 15 行。**
2. **C-1 与 M-3 是 owner 裁量项, 不要由 AI 在下一轮自选**: (i) 「禁服务端 merge + gitlink SHA」两条约束补在 TASK-026 还是补进 phase-c-integrator SKILL (后者更根治但超本 Spec 范围 ⇒ 需 owner 决定是否另开 issue); (ii) sc-baseline 走 (a) 还是 (b); (iii) 推送授权与 AB 门范围的确认形态。按 Rule #10 写进 handoff 请裁。
3. **验证方式换成「跑一次」而不是「再审一次」**: 我这轮抓到的 M-1 / M-2 / minor C 三条全部来自**实跑**(gate 命令 + 注入式双向测试), 不是来自阅读。R4 若真要开, 应把 `.aria/repro/version-surface-assert.py` 与 `spec_complete.py --gate` 两条命令做成 Phase B 的前置 smoke, 让缺陷在实施时自己发红 —— 比第四轮五席阅读便宜一个数量级。
4. **本轮我自己的边际产出也在下降**: 8 条 minor 里有 5 条是文档卫生 (陈旧锚 / dangling ref / 措辞单位 / off-by-one 行号)。它们真实但不承重; 若时间紧, 只修 5 条阻塞项也能进 Phase B, minor 集中在 Phase D 收尾一次性扫。

---

## 轮次记录

| 轮 | 席位 | 结论 | Critical | Major | Minor | fix 引入 (C+M) |
|---|---|---|---|---|---|---|
| R1 | code-reviewer | REVISE | 1 | 6 | 5 | — |
| R2 | code-reviewer | REVISE | 0 | 6 | 5 | 5/6 = 83% |
| R3 | code-reviewer | REVISE | **1** | **4** | **8** | **4/5 = 80%** |

**本轮方法** (全部 ground truth, 零采信自述): 实跑 `spec_complete.py --gate` 取归档门真实读数 (27/27 unchecked + `parent_id: null`) · 自写脚本按 TASK-024 两类判据对当前树 + 模拟 bump + **5 个注入缺陷** 各跑一次 (7 场景矩阵, 抓 2 个假绿) · 逐文件 `grep -c` 重算 14 点与 aria 侧 4 点 · `git show fb5ed36 --numstat` 与 `git -C aria show 9a199c9/af87cae -- VERSION` 取发版惯例的执行史 ground truth (第三方验证 14 点 + 揭穿账本两种相反惯例) · footer python 命令重算并与逐条 `est_hours` 两法互证 · `forgejo GET /issues/177` 实查 issue 正文 · 实读 `phase-c-integrator/SKILL.md` §C.2.4/C.2.4.5/C.2.5 全文 + `branch-manager/SKILL.md` 合并与子模块段 + `git-remote-helper/SKILL.md:40` + `spec_complete.py:189-303,364-375` + `detailed_tasks.py:83` + `.aria/state-checks.yaml:88-102` + `AB_TEST_OPERATIONS.md` 四段清单与三档 Tier 表 + `aria/VERSION` 全 167 行 + `standards/conventions/version-management.md §4.3`。

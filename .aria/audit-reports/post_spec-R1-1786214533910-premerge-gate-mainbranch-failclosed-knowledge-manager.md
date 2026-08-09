---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-08T19:16:46.885Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R1 审计报告 — knowledge-manager 席位

> 被审对象: `openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md` (Level 2, 179 行, 2026-08-08 创建)
> 镜头: 文档一致性 / 方法论合规 / 外部事实核验

---

## 审计结论

本 Spec 要治的缺陷 (`--main-branch` 缺省 `"main"` 导致 Rule #8 gate 的「main 无 in-flight」腿恒绿) 陈述清楚、复现证据扎实, Level 2 判定与 Rule #5 落位均正确。但在**本席位专属职责范围内**发现 3 项 Major + 2 项 Minor 问题, 集中在: (1) Rule #6 判据表对 `SKILL.md:242` 一个 hunk 的归类与其自身文字及项目既有先例相矛盾; (2) 用容器本地 memory 名作核心设计决策的承重引用, 且恰好撞上同日新写的、专门警告这个反模式的 memory; (3) 与并发姊妹 Spec 的版本号排序风险未被提及。均可在 Phase B 开始前通过修订 Spec 正文解决, 不影响核心缺陷修复方案 (D1-D7) 的技术正确性。

## Verdict

**PASS_WITH_WARNINGS** — 0 Critical, 3 Major, 2 Minor。

## 轮次记录

| 轮次 | 席位 | 结论 | 说明 |
|------|------|------|------|
| R1 | knowledge-manager | PASS_WITH_WARNINGS | 首轮, 5 项 finding (3 Major + 2 Minor), 详见下 |

---

## 详细 Finding

### F1 [Major] Rule #6 判据表把 `SKILL.md:242` 的语义变更错归为「描述性/勘正」

**锚点**: `openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md:106-118` (§What Changes 第 5 条 + rule6_note 表)

Spec 正文 (proposal.md:108) 自述:

> 该处「`main_branch` 显式传真值, 不依赖 CLI default」在机械兜底落地后**语义改变** —— 从「你必须记住传」变成「不传会自动解析, 解析不出会 abort」

而 rule6_note 表 (proposal.md:112-116) 把这个 hunk 判进判据表**第一行「描述性」→勘正→substitute**, 与 `pre_merge_gate.py` 的纯代码 hunk 同一档处置。四点证据显示这个归类不成立:

1. **与 SOT 自身附加约束矛盾**: 我已读 `standards/conventions/skill-benchmark-exemption.md` §2 附加约束 —— 「仅当变动是**事实性同步**(溯源注释/行号勘正/术语修正)且 frontmatter `description` 零变动, 才可能落进第一行」。Spec 自己的措辞「语义改变」直接落在这三类之外 —— 这不是行号勘正也不是术语修正, 是一条指令从「强制」变成「可选+自动兜底」的**语义**变化。
2. **引用的 owner 裁定不适用于本案**: proposal.md:117 援引「owner 2026-08-02 裁定 `db2e983`」。我已读该 commit (`db2e98341aa1`), message 原文: 「裁定统一为 substitute 框定 (deterministic detector hook → structural fixture + corpus + dogfood, 不走 `/skill-creator` AB, **因 hook 非 capability skill**)」—— 这条裁定的适用范围逐字限定在「hook 不是 capability skill」这个前提上 (该裁定治的是 `linked-issue-normalization` 里的 secret-guard **hook**)。`phase-c-integrator` 是标准 capability Skill (有 SKILL.md + frontmatter description + `/skill-creator` 覆盖), 不满足这条裁定的适用前提, 引用它属于 memory `feedback_written_exception_exact_condition_match` 所警的「援引成文豁免不核对确切触发条件」。
3. **存在更贴切且结论相反的先例**: 我已读 `aria/CHANGELOG.md` `[1.65.0] - 2026-07-31` (#122) 条目 —— 该版本改的正是**同一个** `SKILL.md` §C.2.4 段落 (「文档: SKILL.md §C.2.4 八处同步 (新步骤 2.5 + AI surface 双义务...)」), 且明文: 「**Rule #6 照跑 AB** (3 eval × with/old/without 三臂, 产出形态 descriptive 统一)」。这是与本 Spec 事实最接近的先例 (同段落、同类「AI 指令义务变化」), 结论与本 Spec 的自我归类相反。本 Spec 未提及也未区分这个先例, 只援引了不适用的 db2e983。
4. **AB 运维手册的 Tier 归类支持「照跑」**: 我已读 `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md:434` —— `phase-c-integrator` 列 Tier 3「编排/集成 Skills, **Phase 编排修改时测**」。`:242` 行本身就是 C.2.4 执行流程 (「执行流程」1-6 步) 第 2.5 步的编排叙述, 修改它属于「Phase 编排修改」。

**不受影响的部分**: `pre_merge_gate.py` + 其测试 (纯 Python, 零 `SKILL.md` 改动) 归第一行有直接匹配先例 (`v1.64.1` #118/#119、`v1.65.2` #124、`v1.65.3` — 三者变更说明均明写「零 SKILL.md 变更」), 这部分的 substitute 处置本身没有问题。**问题窄限于 `SKILL.md:242` 这一个 hunk 被并进了同一档。**

**建议**: 把 `SKILL.md:242` hunk 从第一行移出, 按判据表第二或第三行处置 (若认为该行为在 phase-c-integrator 现有 5-eval 集合覆盖范围内, 照跑 AB; 若认为覆盖不到「AI 是否还会主动显式传参」这个具体行为, 按第三行三条式处置: 点名行为 + 定向可证伪 fixture + 开套件缺口 issue), 并在 rule6_note 里正面回应 v1.65.0 先例为何不适用 (若确实不适用) 而非略过不提。

---

### F2 [Major] 用容器本地 memory 名作核心设计决策的承重引用, 且与同日新增的反模式警告正面相撞

**锚点**: `openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md:50` 与 `:86`

Spec 用两条 memory 作为设计决策的**论证依据**而非装饰性旁注:

- `:50` (紧邻 D1/D2 的「唯一现有约束是一句散文, 不是兜底」论证): 「本项目成文判据: memory `feedback_invariant_needs_failclosed_default` —— 『不变量写进文档 ≠ 写进兜底默认值; 枚举分区必须 fail-CLOSED』」
- `:86` (D2「为什么不 fallback 到 master」的直接论据): 「判据是『这个信号在健康常态下应是什么值』—— 解析不出主分支名时...正确输出是 `error` 不是 green (memory `feedback_false_green_dual_is_permanent_red`)」

我已核实这两个文件在**本容器** (`~/.claude/projects/-home-dev-Aria/memory/`) 确实存在, 内容与引用一致, 无失实。但我同时读到了**同一天新写**的 `memory/feedback_memory_store_is_container_local_not_shared.md` (frontmatter `modified: 2026-08-08T18:11:50.896Z`), 其 description 逐字: 「memory store 是容器/用户本地的不在仓里 ⇒ ... **仓内共享文件 (CLAUDE.md / standards) 引 memory 名对第三方采用者恒悬空**」, 「How to apply」段更直接写: 「**仓内共享文件 (CLAUDE.md / standards/ / 对外 Spec) 不要把 memory 名当承重引用**。承重的知识应落进**仓内**的 `standards/conventions/`; memory 名最多作为 Lab 内部补充, 且须标注『指向 Lab 内部 memory, 第三方不适用』」。

`openspec/changes/*/proposal.md` 是随主仓分发、且按 CLAUDE.md 项目定位「探索 AI Agent 深度参与软件工程全流程」「对外发布方法论与插件」的**成文交付物**, 完全落在这条警告命中的「对外 Spec」范畴内。本 Spec 的两处引用都**没有**做该 memory 建议的任一种缓解 (未把判据落进 `standards/conventions/`、未标注「Lab 内部 memory, 第三方不适用」), 而是直接把 memory 名当成了论证的最终依据。这不是本 Spec 独有的问题 (项目里大量既有 Spec/CHANGELOG 都这么引), 但鉴于警告本身与本 Spec 同一天写就、且本 Spec 恰好把两条 memory 用作**最关键**两个设计决策 (D1「恒绿是方向错的」+ D2「不 fallback」) 的直接依据, 值得在本轮点出。

**建议**: 至少给两处引用加一句「(Lab 内部 memory, 第三方复现本方法论时请参考本 Spec 正文的完整论证, 不依赖该引用)」; 更彻底的做法是把这两条判据的内容提炼进 `standards/conventions/`(如 `skill-benchmark-exemption.md` 同级的一条通用 fail-closed 设计原则), 但这超出本 Spec 范围, 可留 follow-up。

---

### F3 [Major] 未处理与并发姊妹 Spec `linked-issue-normalization` 的版本号排序风险

**锚点**: `openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md:168-169` (§Impact 「发版同步面」+「版本」两行) 对照 `openspec/changes/linked-issue-normalization/proposal.md:1-8` 与其 `tasks.md:127-158`

本 Spec §Impact 写:

> 发版同步面 | aria 子模块版本面 + 主仓版本引用面 —— 按引用点而非文件数枚举, 判据见 `linked-issue-normalization` 的 5.11 (整仓差集 + append-only 账本另判); 类级根因见 **Aria #177**
> 版本 | **v1.65.6 PATCH**

我已读 `linked-issue-normalization/proposal.md` 头部: `Status: 📝 Draft (A.1)`, `Spec Level: 3`, `ship target: aria-plugin v1.66.0 (MINOR)`; 其 `tasks.md` 5.9–5.15 (含被引用的 5.11) **全部是未勾选的 `- [ ]`**, 即该方法论/机制本身尚未落地, 仍是另一份 Draft Spec 里的计划任务。两份 Spec:

- **共享同一个版本 SOT** (`aria/.claude-plugin/plugin.json`, 现值 `1.65.5`);
- **当前版本号目标不兼容排序**: 本 Spec 目标 `v1.65.6` (PATCH), `linked-issue-normalization` 目标 `v1.66.0` (MINOR) —— 若后者先于本 Spec 完成 Phase C 落地, `plugin.json` 会先跳到 `1.66.0`, 届时本 Spec 的 `v1.65.6` 目标即成为**不可执行的版本号** (SemVer 不允许在 `1.66.0` 已发布后再发 `1.65.6`), 需要临场重新编号;
- 且两者存在方向性关联而非纯粹独立: `linked-issue-normalization` 自己的 Phase C (`tasks.md:5.13`) 明确要经过 `phase-c-integrator` 的 Rule #8 pre-merge gate ——**正是本 Spec 要修的那个 gate**。若 `linked-issue-normalization` 在本 Spec 之前合并, 它的 PR 就会被当前**仍是 fail-OPEN** 的 gate「保护」, 即受益于一次形同虚设的检查。

proposal.md 全文未提及这层排序关系, 也未给出「若对方先落地怎么办」的应对 (例如显式把版本目标写成「`plugin.json` 当前版本 +1 PATCH, 若与 `linked-issue-normalization` 撞车以...为准」)。这是本席位「Impact 里发版同步面表述是否可执行」核查项下发现的真实缺口, 不是推测。

**建议**: 在 §Impact 或 §非目标 里显式声明两个 Spec 的落地顺序预期 (哪个该先), 并把「版本: v1.65.6 PATCH」改写为相对表述 (「当前 SOT 版本的下一个 PATCH」) 或加一条「如遇 `linked-issue-normalization` 先落地, 版本号顺延」的显式条款。

---

### F4 [Minor] aria-plugin#137 的 issue 正文本身未被订正, 订正只存在于评论

**锚点**: aria-plugin issue [#137](https://forgejo.10cg.pub/10CG/aria-plugin/issues/137) (API 已查, `state: open`, `comments: 1`) 对照 `proposal.md:58`

我已用 `forgejo GET /repos/10CG/aria-plugin/issues/137` 与 `.../issues/137/comments` 独立查证:

- issue **`body`** 字段原文至今仍是: 「Rule #8 pre-merge gate 的两条腿在本项目上**都不触发, 且都失败为绿**」—— 这是 Spec 自己指出的错误判断, 但 issue 正文字面**没有被编辑**, 逐字原样保留;
- 订正**只存在于** comment id `18015` (2026-08-08T16:37:00Z, 与 issue `updated_at` 同秒): 「⚠️ 订正正文一处: 『两条腿都失败为绿』不成立 —— 只有 (b) 那条」。

proposal.md:58 写「#137 正文已同批评论订正」—— 按字面这句话本身不算失实 (「正文[的错误]已[被][同批评论]订正」这个读法与实况相符), 但措辞容易让只扫 issue body 不看 comment 的读者误以为 body 已经改过。这是外部记录的呈现方式问题, 不是本 Spec 的错, 但既然本 Spec 依赖读者去 #137 核对背景, 建议顺手把 issue body 本身也编辑一下 (加一行 EDIT/订正说明), 而不是只留评论。

**建议**: 若举手之劳, 顺带把 aria-plugin#137 的 issue body 加一行订正说明 (不属于本 Spec 强制范围, 举手提示)。

---

### F5 [Minor] D5「回显 `main_branch_resolved`」与 workflow-runner 的固定 `gate_state` 持久化 schema 未对齐

**锚点**: `aria/skills/workflow-runner/references/workflow-state-schema.md:38-54` (`gate_state` JSON Schema) 与 `aria/skills/workflow-runner/scripts/gate_state_helper.py:115-153` (`write_gate_state()`) 对照 `proposal.md` D5 (§决策记录) 与 §Impact 文件表

proposal.md D5 要求 gate 输出回显 `main_branch_resolved` + 来源, 目的是「使假绿在 surface 可见」。我已读 `workflow-state-schema.md` —— `gate_state` 块的字段是显式列举的封闭集合 (`name/status/started_at/retry_count/next_check_at/in_flight_runs/primitive_used/raw_message`), 无 `main_branch_resolved` 位置; 我也读了 `gate_state_helper.py:115-153` 的 `write_gate_state()` —— 它用**显式具名参数**构造要持久化的字典 (`in_flight_runs`/`primitive_used`/`raw_message` 逐个赋值), 不是把上游 `gate_result` 全字典透传。

`wait` 判决会经过这条持久化路径 (供 `workflow-runner` 的 `wait_recoverable` 轮询读取/展示); 如果 D5 的新字段只加在 `pre_merge_gate.py` 的 `gate_check()` 直接返回值里, 而没人同步 `write_gate_state()` 的签名与 `workflow-state-schema.md`, 那么在「main 有 in-flight, 进入等待轮询」这条路径上, `main_branch_resolved` 会在持久化时被悄悄丢掉 —— 恰好是 D5 想解决的「假绿 surface 不可见」问题的一个子情形没被堵上。

proposal.md §Impact 文件表只列了 `phase-c-integrator` 侧三个文件 (`pre_merge_gate.py` / 其测试 / `SKILL.md:242`), 没有提到 `workflow-runner` 侧, Level 头部也写「无跨模块」。这可能是有意的范围收窄 (D5 只承诺覆盖 `gate_check()` 直接返回值, 不延伸到持久轮询态), 但 Spec 正文没有明说这个边界, 也没有说明为什么不需要, 属于文档完整性缺口而非确认的实现缺陷。

**建议**: 在 D5 或 §非目标 里补一句, 明确 `main_branch_resolved` 的可见性范围是否包括 `wait` 轮询期间持久化的 `gate_state`; 若包括, §Impact 需补 `workflow-runner` 两个文件; 若不包括, 显式写明「本 Spec 范围止于 gate_check() 直接返回值, 轮询态展示留 follow-up」。

---

## 核查确认 (未发现问题的项目, 附证据)

- **Rule #5 / Level 判定**: Spec 落主仓 `openspec/changes/`、代码落 `aria/` 子模块 —— 符合 `CLAUDE.md` 不可协商规则 #5。Level 2 判定 (非 Level 1: 改变闸门语义; 非 Level 3: 已读 `standards/core/ten-step-cycle/phase-a-spec-planning.md:120-137` 判据「architecture/cross-module/breaking → Level 3」, 本变更单模块、非破坏性架构变更) 成立。
- **Aria #177 引用准确**: 已用 `forgejo GET /repos/10CG/Aria/issues/177` 核实, 标题「CLAUDE.md:81 发布同步面那行是漏同步面的类级根因」与 proposal.md:168「类级根因见 Aria #177」一致, state=open。
- **memory 引用内容准确**: `feedback_invariant_needs_failclosed_default.md` 与 `feedback_false_green_dual_is_permanent_red.md` 在本容器均存在, 内容与 Spec 引用的判据原话一致 (见 F2, 问题在于「该不该引」而非「引错了」)。
- **`SKILL.md:242` 行号准确**: `grep -n` 核实 `main_branch` 显式传真值那句确实在第 242 行。
- **测试基线数字准确**: 独立跑 `python3 -m unittest discover` 于 `aria/skills/phase-c-integrator/tests/`, 实测 `Ran 111 tests ... OK`, 与 proposal.md:179 声称的「现 111 tests」一致。
- **版本 SOT 与 ship target 本身自洽**: `aria/.claude-plugin/plugin.json` 现值 `1.65.5`, `v1.65.6` 是合法的下一个 PATCH (排序风险见 F3, 但目标数值本身不矛盾)。
- **aria-plugin#137 核心指控与 (a)/(b) 腿判断准确**: body 与 comment 的技术论证 (aether CLI 两分支返回同形 / `path_coverage.py:24` fail-toward-covered) 与 Spec 正文逐字对应, 无失实转述。
- **未发现重复在制品**: `forgejo GET /repos/10CG/aria-plugin/pulls?state=open` 与 `/repos/10CG/Aria/pulls?state=open` 均为空, 无已存在的競态 PR。

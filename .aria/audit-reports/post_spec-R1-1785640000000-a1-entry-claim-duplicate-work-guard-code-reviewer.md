# post_spec R1 — code-reviewer
**verdict**: REVISE
**scope_ok**: true
**counts**: critical=3 major=7 minor=3

> 审查视角: 欠定检测 (两独立实现者拿同一份规格是否做出同一个东西)。
> 被审对象: `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md` (Level 2, 全文)。
> 所有引用行号均已实读源文件核对 (`phase1_gate.py` / `lib/collision.py` / `lib/gc.py` / 4 个 SKILL.md / `execution-modes.md` / 8 份 proposal)。
> scope_ok 判定: 变更面严格落在自述范围 (A.1 认领点 + audit-engine 竞品扫描), 无 scope creep; REVISE 源于欠定而非越界。

---

## Findings

### [CRITICAL] C1 — `--linked-issue` 取值无归一契约, 仓内已有三种写法并存; 匹配是裸字符串相等 ⇒ 主机制静默失效

- **位置**: `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:91` (`--linked-issue "<repo>#<n>"`) + `:96` (「spec 有『关联 Issue』字段时**必传**」) + `:24-25` (dogfood 用 `aria-plugin#124`); 判定实现 `aria/skills/state-scanner/lib/collision.py:217`
- **问题**: 整个主机制的承重算法是 `linked_issue_overlaps()` 里的一次字符串比较, 而 Spec 没有把该字符串钉到字符级。`collision.py:217` 原文:

  ```python
  if c.linked_issue != own_linked_issue:
      continue
  ```

  全函数 (`collision.py:177-233`) 无 `lower()` / `strip()` / 正则 / 前缀剥离 —— **无任何归一**。同一个 issue 只要两轨写法差一个字符, overlap 恒为 `[]`。
- **证据** (两实现者分叉, 对同一输入结论相反):
  - **实现者 A** 读 §1:91 模板 `"<repo>#<n>"` + §Why:24-25 的实跑样例 → 传 `aria-plugin#122`。
  - **实现者 B** 读 §1:96「spec 有『关联 Issue』字段时必传」→ 从该字段取值。**仓内唯一真实存在的「关联 Issue」字段实例**是 `openspec/changes/phase-c-integrator-ci-path-coverage/proposal.md:18`:
    `> **关联 Issue**: [10CG/aria-plugin #122](https://forgejo.10cg.pub/10CG/aria-plugin/issues/122)` → 取值 `10CG/aria-plugin #122` (**带 org 前缀 + 带空格**)。
  - **第三种写法**在 CLI help 里: `aria/skills/state-scanner/scripts/phase1_gate.py:1203` — `"可选语义重叠信号 (Part B1, 如 '10CG/Aria#160')"`。
  - 输入 X = 「A 轨与 B 轨同时对 aria-plugin#122 起草」。A/B 各自 claim 成功、各自互查 → 因 `10CG/aria-plugin #122 != aria-plugin#122`, 双方都得到 `linked_issue_overlap == []`, 即 **SC-2 (`:138`) 的绿灯观测量**。机制 100% 静默失效, 而 §Why:76 的「反事实」承诺的正是这一场景会被拦住。
- **建议修法**: §1 必须二选一并写死, 不得留给实现者:
  (a) **规格侧钉死取值** — 明写「`--linked-issue` 值 = `<owner>/<repo>#<n>`, 全小写, 无空格」, 给 ≥3 组正例 + 3 组反例 (`10CG/aria-plugin #122` → `10cg/aria-plugin#122`), 并同步勘正 `phase1_gate.py:1203` help 与 `phase-b-developer/SKILL.md:93` 两处已有写法; 或
  (b) **实现侧归一** — 在 `linked_issue_overlaps()` 内做规范化后比较。注意 (b) 与 §非目标:151「不改 `phase1_gate` 自身代码」直接冲突, 须 owner 裁。
  另: 新增一条 SC「两轨用不同书写形态引用同一 issue 时仍必须互相命中」(baseline-failing, 可证伪)。

---

### [CRITICAL] C2 — §1 消费面只认 `linked_issue_overlap[]`, 对「同名两轨」结构性失明; SC-2 的观测量与真碰撞不可区分

- **位置**: `proposal.md:97` (消费义务) + `:137-138` (SC-1/SC-2); 实现 `aria/skills/state-scanner/lib/collision.py:219-220`
- **问题**: `linked_issue_overlaps()` **显式排除同 track_id 的对手**:

  ```python
  if c.track_id == own_track_id:
      continue  # same-name collision — reconcile's job, not ours
  ```

  即该字段按设计只覆盖「同一件事两个名字」。「同一件事同一个名字」的碰撞走的是另一条通道: `phase1_gate.py:663-676` 的 `AdvisorySurface(kind="occupied")` → CLI JSON 的 `surface` / `competing_winner` 键 (`phase1_gate.py:1138-1156`)。**§1:97 只点名 `linked_issue_overlap[]`, 完全没有提 `surface` / `competing_winner`。**
- **证据** (两实现者分叉):
  - 输入 X = 「两容器都按 issue 标题给 spec 起名, `derive_track_id` (`lib/track_id.py:61-170`, 纯 lower + `/._`→`-`) 归一后得到同一 track_id」。
  - **实现者 A** 严格照 §1:97 实现 → JSON 里 `linked_issue_overlap == []` → 判「无竞品」→ 正常起草。且这一观测量**恰好等于 SC-2 (`:138`) 的期望值**, 所以验收也判绿。
  - **实现者 B** 额外消费 `surface.kind == "occupied"` → 渲染 🔴 → 停下报告。
  - 两者对同一次真实碰撞结论相反, 且 A 的错误无法被本 Spec 现有任何 SC 捕获。
  - 反直觉后果: 主机制**只在两轨取名不同时生效**; 命名越规范 (都从 issue 派生 slug), 机制越失效。
- **建议修法**:
  1. §1:97 消费条件改为 **「`linked_issue_overlap[]` 非空 **或** `surface != null` **或** `competing_winner != null`」** 三选一即渲染;
  2. SC-2 的期望值补足为「`linked_issue_overlap == []` **且** `surface == null` **且** `competing_winner == null`」(否则 SC-2 恒真);
  3. 新增 SC 覆盖「同 issue 同 track_id」分支, 期望 `surface.kind == "occupied"` 被渲染。

---

### [CRITICAL] C3 — 「先向用户报告再决定是否继续起草」形态未定; 两种实现分别撞 §非目标+AD10 与 Rule #10

- **位置**: `proposal.md:97` (「并**要求 AI 先向用户报告再决定是否继续起草**。advisory 不阻断, 但**不得静默吞掉**」)
- **问题**: 这句话同时欠定两件事 —— (i) 「报告」的**形态** (AskUserQuestion 阻断式 / 渲染一行 / 写 handoff); (ii) 「再决定」的**主语** (AI 决定还是用户决定)。中文句式两读皆通。而这句是本 Spec 唯一的行为载荷 (Rule #6 判为「处方性·运行时指令面, 照跑 AB」, `:129`), 欠定 = AB baseline 无法定义。
- **证据** (两实现者分叉, 且各自撞不同的成文约束):
  - **实现者 A** = AskUserQuestion 阻断等人答。撞两条: (1) §非目标:150「不把 advisory 升级为 block」—— 等人答就是事实 block; (2) `CLAUDE.md:125`「人类参与点仅 1 个 (AD10): S7_AWAITING_MERGE」—— 在 v2.0 无人值守 Layer 2 里 A.1 引入第二个人类参与点, 168h 自主跑遇到 overlap 会直接挂起。
  - **实现者 B** = 渲染一行 🔴 后 AI 自行继续。撞 Rule #10: enabled 机制点名了竞品, AI 自行判定「继续起草」正是「AI 任何自作主张的流程判断」的形状 (`standards/conventions/configured-gate-authority.md`)。
  - 输入 X = 「overlap 非空, 且当前是无人值守 Layer 2 session」→ A 挂起 (0 产出), B 继续 (可能重复劳动)。结论相反, 且**没有第三方文档能裁决哪个对**。
- **建议修法**: §1 增一张三分支决策表, 逐字写死:
  - (a) **交互式 session** → `AskUserQuestion`, options 至少含 `yield / 接管 / 并行 (需理由)`;
  - (b) **无人值守 (Layer 2)** → **不阻断**, 但 MUST 把 overlap 全文 (对方 track-id / owner-container / claimed_at) 写进本 cycle handoff 的「请 owner 复议」段 + 在 proposal 头部落一个 `overlap_ack` 字段 —— 这样「不静默吞掉」变成可机械核验的留痕, 而非 AI 自我裁量;
  - (c) 任何情况下不得只渲染不留痕。
  并增 SC:「无人值守分支不得阻塞」+「留痕字段存在性可 grep」。

---

### [MAJOR] M1 — `--raw-track-id` 双来源无优先级, 与 B.0 / D.2b 的 carry-id 脱钩 ⇒ 双 claim + 释放漏一 + 自撞恒红

- **位置**: `proposal.md:88` (`--raw-track-id "<spec-slug 或 handoff §6 carry-id>"`); 对照 `aria/skills/phase-b-developer/SKILL.md:92` 与 `aria/skills/phase-d-closer/SKILL.md:52,55`
- **问题**: 「或」没有优先级, 且 Spec 自己承认时点是「起草**前**」—— 此时 spec-slug 常常尚未确定。更关键: 下游两处都以「同一原始串」为前提:
  - `phase-b-developer/SKILL.md:92`: `--raw-track-id "<本 cycle carry-id/Spec id>"`
  - `phase-d-closer/SKILL.md:55`: 「carry-id = Phase B-entry 时传给 phase1_gate 的**同一原始串** (归一在 CLI 内部, 两端一致)」; `release_gate` 按 `derive_track_id(raw)` + container 定位 (`release_gate.py:129`)。
- **证据** (两实现者分叉):
  - **实现者 A**: A.1 传 spec-slug (刚定的目录名), B.0 传 handoff §6 carry-id → `T_a ≠ T_b`。D.2b 只释放 `T_b`; **`T_a` 永远 active**, 直到有人跑 `release_gate --sweep-stale` 且 heartbeat 超 24h (`lib/gc.py:341` 默认 `stale_ttl_seconds=SWEEP_TTL`, `constants.py:SWEEP_TTL=86400`; 且无生产 heartbeat loop, heartbeat 冻结在 acquire 时刻)。
  - **实现者 B**: A.1 与 B.0 传同一串 → 单 claim, 释放闭合。
  - A 的可观测后果最刺眼: 本容器**自己**遗留的 A.1 claim 满足 `collision.py:212-220` 的全部条件 (非 terminal / 有 linked_issue / linked_issue 相同 / track_id 不同) —— 于是它在自己后续的 B.0 认领里被报成 overlap。**自己撞自己, 恒红**。恒红 = 零信息, 训练 AI 忽略该信号 (memory `feedback_false_green_dual_is_permanent_red`), 主机制随之作废。
  - 同一输入 (一个正常 cycle 跑完 A.1→B→D), A 留下 1 条僵尸 active claim + 后续恒红, B 留下 0 条。
- **建议修法**: §1:88 改为单一来源 + 不变式: 「`--raw-track-id` 必须与本 cycle 后续 B.0 / D.2b 使用的**同一原始串**; A.1 时 slug 未定则用 handoff §6 carry-id, 之后即便 slug 定了也**不改**」。新增 SC:「A.1 与 B.0 两次调用 `derive_track_id` 后得到同一 track_id」+「一个完整 cycle 结束后, 本 track 的 active claim 数 == 0」。若确实要两条 claim, 则 Impact 表必须加 `phase-d-closer/SKILL.md` (释放两条), 并在 §1 说明如何避免自撞。

---

### [MAJOR] M2 — 「A.1 起草前」时点未钉, 与 phase-a-planner 三条跳过规则的交互未定

- **位置**: `proposal.md:84` (「`phase-a-planner` 在 **A.1 起草前**调用 phase1_gate 认领」); 对照 `aria/skills/phase-a-planner/SKILL.md:63-73` 与 `:126-131`
- **问题**: 实读 A.1 的结构 (`phase-a-planner/SKILL.md:63-73`):

  ```yaml
  A.1 - Spec 管理:
    skill: spec-drafter
    skip_if:
      - has_openspec: true          # 已有活跃 Spec
      - complexity: Level1          # 简单任务
    action:
      - 检查现有 Spec
      - 创建新 Spec 或选择现有
  ```

  「起草前」可落在: skip_if 判定之前 / skip_if 之后 action 之前 / `检查现有 Spec` 之后 `创建新 Spec` 之前 —— 三个位置。Spec 没选。
- **证据** (两实现者分叉):
  - **实现者 A**: 认领写进 A.1 body (skip_if 之后) → `:128-131` 的三条跳过路径 (「已有活跃 Spec」/「复杂度 Level1」/「emergency hotfix lane」) 一并跳掉认领。
  - **实现者 B**: 认领写在 skip 判定之前 → 三条路径下仍认领。
  - 输入 X = 「本轨复用一份已存在的活跃 Spec 继续做 #122」(= `has_openspec: true`) → A 无 claim (碰撞对他人不可见), B 有 claim。这恰好是**高概率场景**: 两轨都在同一 issue 上迭代时, 后到者往往走「选择现有 Spec」而非「创建」。
- **建议修法**: 照抄 Phase B 的成文写法 —— 新增一个**独立编号步** `A.0b - REQUIRE claim` (镜像 `phase-b-developer/SKILL.md:86` 的 `B.0 - REQUIRE claim`), 明写「在 A.1 skip 判定**之前**执行」, 且其 `skip_if` **只有两条**: `coordination.enabled` 显式 false / 非 git repo (与 `phase-b-developer/SKILL.md:95-99` 逐字对齐)。同时在 §1 显式声明它与 `:128-131` 跳过规则表的关系 (「A.1 被跳过不蕴含 A.0b 被跳过」)。

---

### [MAJOR] M3 — 「Step 0.5」的命名与 D3「每轮」互斥; 正确落点文件不在 Impact 表; 「每轮入口 fetch」指向一个不存在的既有步骤

- **位置**: `proposal.md:101` + `:104` + D3 `:123` + Impact `:160-165`; 对照 `aria/skills/audit-engine/SKILL.md:83-85` 与 `aria/skills/audit-engine/references/execution-modes.md:89,118`
- **问题**: 三处叠加的欠定。
  1. Spec 说「Step 0 (anchor 固化) **旁**加 Step 0.5」。实读 `audit-engine/SKILL.md:85` 原文: 「入口逻辑完成后、**Round 1 启动前一次性**执行」。**Step 0 的定义性属性就是「一次性」**, 编号 0.5 与「旁」把新步骤直接绑进这个语义。
  2. per-round 循环根本不在 SKILL.md —— 它在 `references/execution-modes.md:89` (`Round N:` convergence) 与 `:118` (`Round N (一个完整周期)` challenge)。**Impact 表 `:160-165` 只列了 `skills/audit-engine/SKILL.md`**, 没有列这个文件。
  3. Spec 说「每轮**入口 fetch 后**」。实测 `grep -rn "fetch" aria/skills/audit-engine/` 只有一处命中 (`SKILL.md:389`, 讲 base 分支解析)。audit-engine **现在没有任何 fetch 步骤**, 「入口 fetch」预设了一个不存在的前驱, 谁负责 fetch / fetch 哪些 remote 未定。
- **证据** (两实现者分叉):
  - **实现者 A** 按字面结构把小节写在 `SKILL.md` 的 Step 0 之后, 继承「Round 1 启动前一次性」→ **只跑首轮**。
  - **实现者 B** 按 `:104`「每轮跑而非仅首轮」把它挂进 `execution-modes.md:89` 的 `Round N` 序列 → 每轮跑。
  - 输入 X = 「对方 spec 在本审计 R3 时才 push 到远端」—— 这**正是 §2:104 点名要覆盖的场景**。A 漏报, B 命中。结论相反, 且 A 完全符合 Spec 的字面结构描述。
- **建议修法**:
  1. 弃用「Step 0.5」这个编号 (它的语义被 Step 0 的「一次性」污染), 改称「**Round 入口检查 (每个 Round 的第 0 步)**」, 并在 §2 明写它写入 `references/execution-modes.md` 的 `Round N` 序列**首位**, 而非 SKILL.md 的 Step 0 邻接位;
  2. Impact 表补 `skills/audit-engine/references/execution-modes.md`;
  3. 明写 fetch 归属: 由 `sibling_spec_probe.py` **自己执行** `git fetch --all` (含超时与失败降级), 不依赖调用方 —— 否则 SC-6 的 degraded 语义无归属。

---

### [MAJOR] M4 — 「关联 Issue」不是模板字段: SC-3 / D2 的触发谓词, 它要判的输入不会被生成

- **位置**: `proposal.md:96` (「spec 有『关联 Issue』字段时**必传**」) + SC-3 `:139` + §2:101 (「对本 spec 的『关联 Issue』grep」)
- **问题**: 实测该字段在规范体系中**未定义**:
  - `grep -rn "关联 Issue" standards/` → 唯一命中 `standards/conventions/git-commit.md:447` (是 commit checklist 的一项, 与 proposal 无关);
  - `aria/skills/spec-drafter/` 三个文件 (`SKILL.md` / `LEVEL3_TEMPLATE.md` / `LEVEL_GUIDE.md`) 零处定义;
  - 主仓 8 份 `openspec/changes/*/proposal.md` 中**只有 1 份**真有该字段 (`phase-c-integrator-ci-path-coverage/proposal.md:18`)。其余 7 份 (**包括本 Spec 自己**) 的 issue 引用都是散在头部/正文的自由文本 (本 Spec `:6` 的 `aria-plugin #122`、`:9` 的 ship target 等)。
- **证据** (两实现者分叉):
  - **实现者 A** 严格按「字段」判 → 8 份里 7 份判「无关联 issue → 可省」→ 「条件必需」退化为几乎恒不触发, D2 (`:122`) 自己反对的那个失败模式 (「可选 = 多数人不传 = 机制空转」) 原样复现。
  - **实现者 B** 按「正文出现 issue 引用」判 → 需要另造一套抽取规则, 并且会把 §Why 里引用的历史 issue (`#133`、`#165`…) 一并算成关联 issue, 产生多个 `--linked-issue` 候选值而 CLI 只接受一个 (`phase1_gate.py:1198-1205`, 非 `action="append"`)。
  - 输入 X = 本 Spec 自身: A 判「可省, 不传」, B 判「必传, 但传 `#122` 还是 `#5`?」—— 连能不能确定值都相反。
  - 这正是本 Spec §Why:58 **自己援引**的 `feedback_verify_predicate_inputs_exist` 形状:「判定逻辑对吗 + 它要判的输入真会被生成吗」。本 Spec 用该判据否掉了原建议, 然后在自己的 SC-3 上重犯。
- **建议修法**: 本 Spec 必须自带该字段的**模板落地**, 否则谓词悬空:
  1. 在 `spec-drafter` 的 proposal 模板 (及 `LEVEL3_TEMPLATE.md`) 新增「关联 Issue」头部字段, 取值形态与 C1 的归一契约**同一串**;
  2. Impact 表补 `skills/spec-drafter/SKILL.md` + `LEVEL3_TEMPLATE.md` (注意这会把 Rule #6 的 AB 面扩到第三个 skill, `:129` 的 rule6_note 需同步);
  3. SC-3 的谓词改写为「proposal 头部存在 `关联 Issue:` 字段 ⇒ 调用必须带 `--linked-issue` 且值等于该字段归一后的值」, 使其可机械判定。

---

### [MAJOR] M5 — Impact 表「phase-a-planner 既有测试」事实错误 (该目录只有 SKILL.md); SC-3「可红」无机械宿主

- **位置**: `proposal.md:164` (「`skills/phase-a-planner/` 既有测试 | 扩展 (SC-1~3)」) + SC-3 `:139` (「**可红** — A.1 流程断言该参数在场」)
- **问题**: 实测 `ls -R aria/skills/phase-a-planner/` → **只有 `SKILL.md` 一个文件**, 无 `tests/` 无 `scripts/`。全仓有 `tests/` 目录的 10 个 skill (`ai-native-estimator` / `aria-context-monitor` / `aria-doctor` / `aria-token-telemetry` / `issue-triage` / `phase-c-integrator` / `phase-d-closer` / `session-closer` / `state-scanner` / `workflow-runner`) 不含 phase-a-planner。「既有测试」不存在。
- **证据** (两实现者分叉):
  - **实现者 A** 按字面找「既有测试」→ 找不到 → SC-1~3 不落任何可执行断言, 全部推给 AB。但 SC-3 断言的是「参数在场」这种**结构性事实**, AB 行为套件未必测得到 (正是 Rule #6 判据表第一行「描述性 → substitute: SC 级 baseline-failing 结构化测试替代」要防的情形)。
  - **实现者 B** 新建 `skills/phase-a-planner/tests/` → 随即撞上: phase-a-planner 是**纯 prose skill, 无可执行体**, 「A.1 流程断言该参数在场」测什么? 测 `SKILL.md` 文本里含 `--linked-issue`? 那是文档 lint, 不是流程断言, 与 SC-3 的措辞不符。
  - 输入 X = 「实现者交付后跑 SC-3」: A 交付「无此测试」, B 交付「一条文档 lint」, 二者对「SC-3 是否满足」结论相反。
- **建议修法**:
  1. Impact 表 `:164` 改为「**新建** `skills/phase-a-planner/tests/`」(与 `:163` 的 audit-engine tests 同为新建);
  2. SC-3 重述为可执行且**诚实标注被测对象**的形态, 二选一: (a) 文档结构 lint —「`phase-a-planner/SKILL.md` 中 `A.0b` 步骤块必须含 `--linked-issue` 且标 MUST」, 明写「本测试测文本不测运行时」; 或 (b) 降级为 AB 行为观测项并**点名对应 AB fixture 编号** (若套件无覆盖, 按 Rule #6 判据表第三行「建可证伪定向 fixture + 套件缺口开 issue」)。

---

### [MAJOR] M6 — §3 残余缺口把窗口说成「秒级」, D5 的裁决建立在这个低估之上; 措辞会被读成「已覆盖」

- **位置**: `proposal.md:109-113` (§3) + D5 `:125` (「owner 未授权; 残余窗口秒级, 性价比不成立」)
- **问题**: §3:111「该窗口由 claim 的推送延迟界定 (秒级), 远小于本次的 2 天」—— 这个界定**只在对方也会跑 A.1 认领时成立**。对下列轨, 窗口是**无界的** (与改动前完全相同):
  - 跳 A.1 的三条成文路径 (`phase-a-planner/SKILL.md:128-131`: 已有活跃 Spec / Level1 / emergency hotfix lane) —— 见 M2;
  - `/spec-drafter` 直调绕过 phase-a-planner (`spec-drafter/SKILL.md:9 user-invocable: true`) —— 见 M7;
  - `coordination.enabled` 显式 false 的项目 (成文 skip 条件, `branch-manager/SKILL.md:151`);
  - 本 Spec §2:105 自己承认的「legacy 轨 / 未用 phase1_gate」。
- **证据**: 反事实检验 —— #122 的 L 轨若走的是「已有活跃 Spec」路径 (M2 的 A 实现), 改动后窗口**仍是 2 天**, 与 §3:111 的「秒级」相差 5 个数量级。而 D5 明确以「残余窗口秒级」为不做中心化登记表的理由; 理由的量级错了, 结论未必错但论证不成立。读者 (含后续 Phase B 实现者与 owner) 会据 §3 的措辞认为「只剩秒级窗口 = 基本覆盖」。
- **建议修法**: §3 按轨分类重写残余窗口, 不合并成单一量级:
  - (a) 双方都走 A.1 认领 → 秒级 (由 claim push 延迟界定);
  - (b) 任一方跳 A.1 / 直调 spec-drafter / `coordination.enabled=false` / legacy 轨 → **无界, 与改动前同**;
  并把 D5 的理由改写为「(b) 类由 M7 的入口补齐 + 已成文 opt-out 承担, 不由登记表解决」, 或就 (b) 类重新提请 owner 裁 (Rule #10: 风险接受是 owner 的配置决定)。

---

### [MAJOR] M7 — 入口覆盖不对称: Phase B 的同一条 claim 义务写在两个入口, A.1 只写一个; `/spec-drafter` 直调可绕过

- **位置**: `proposal.md:84` + Impact `:160` (只改 `skills/phase-a-planner/SKILL.md`)
- **问题**: 既有 Phase B 设计的成文先例是**双落点 + 显式点名绕过路径**:
  - `phase-b-developer/SKILL.md:86-94`, 其中 `:94`「goal 直驱 / 绕过 state-scanner 进入的 session 也适用 (B-entry 手动补 claim)」;
  - `branch-manager/SKILL.md:146-151`, 其中 `:150-151`「直接调 branch-manager 绕过 phase-b-developer 的 session 同样适用」。
  而 A.1 的真正起草执行体是 `spec-drafter` (`phase-a-planner/SKILL.md:64` `skill: spec-drafter`), 且 `spec-drafter/SKILL.md:8-9` 为 `disable-model-invocation: false` + `user-invocable: true` —— **用户和模型都能直接调起 `/spec-drafter`, 完全不经 phase-a-planner**。
- **证据** (两实现者分叉): 输入 X = 「用户直接 `/spec-drafter a1-xxx` 起草」。**实现者 A** 只改 phase-a-planner (Spec 字面 + Impact 表字面) → 无 claim, 碰撞不可见; **实现者 B** 按 Phase B 先例双落点也改 spec-drafter → 有 claim。结论相反。注意 CLAUDE.md「Plugin 调用」段把 `/spec-drafter` 列为常用直调 Skill, 说明该路径是**常态而非边缘**。
- **建议修法**: 复制 Phase B 的双落点写法 —— Impact 表加 `skills/spec-drafter/SKILL.md`, 两处都写「绕过 phase-a-planner 直调本 skill 的 session 同样适用」, 并在 §1 明确「以先到者为准, 已认领则不重复认领」(避免与 M1 的双 claim 叠加)。同步更新 `:129` rule6_note 的 AB 面 (第三个 skill 的 description/指令面是否变动需逐 hunk 判)。

---

### [MINOR] m1 — SC-6 degraded 路径缺 exit code 与阻断性契约

- **位置**: `proposal.md:142` (SC-6) 对照 `:141` (SC-5)
- **问题**: SC-5 明写「报告空, **退出码 0, 不阻断**」; SC-6 只写「**不静默** — 报告 `degraded` 且注明『本轮竞品扫描未执行』(零证据不得当正证据)」, **既无 exit code 也无阻断性**。两条并列时, 读者会从对照推断 SC-6 是非 0。
- **证据**: **实现者 A** degraded → exit 0 + 报告标注 → audit-engine 继续本轮; **实现者 B** degraded → exit 非 0 (「零证据不得当正证据」的强读法) → audit-engine 中止/降级本轮。输入 X = 「离线 / fetch 失败环境跑 post_spec」→ A 能跑完审计, B 跑不了。
- **建议修法**: SC-6 补齐「**exit code 0, 不阻断本轮审计**; degraded 事实写入本轮报告 body 的固定字段 (如 `sibling_probe: degraded`), 并在收敛判定时**不得**把 degraded 轮的空结果计为『无竞品』证据」—— 这样「不静默」由留痕保证, 而非由阻断保证。

---

### [MINOR] m2 — 「grep 全部远端 ref」范围未定 (remote 集 × ref 集)

- **位置**: `proposal.md:101` (「grep **全部远端 ref** 上的 `openspec/changes/*/proposal.md`」)
- **问题**: 「全部远端 ref」至少三种读法: 仅 `origin/master` / 全部 remote 的默认分支 (本仓有 origin + github 双远程) / 全部 remote 的 `refs/heads/*` 全量。三者的运行时代价与命中集差一个量级, 且第三种会把 fork/PR 分支上的半成品 spec 报成竞品 (误报)。SC-4 (`:140`) 只要求「报告命中, 含对方目录名 + 所在 ref」, 无法区分三种实现。
- **建议修法**: §2 钉死两个集合: 「remote 集 = `git remote` 全量」+「ref 集 = 各 remote 的默认分支 (`refs/remotes/<r>/HEAD`)」, 并在 §2 的盲区声明里补一句「未 push 到默认分支的 spec (仍在 feature 分支) 不可见」——与 `:105` 现有盲区声明并列。SC-4 补充「给定 origin 默认分支有竞品 + github feature 分支有竞品, 只报前者」的可证伪断言。

---

### [MINOR] m3 — §Why 用 dogfood 的 `linked_issue_overlap=[]` 作主机制佐证, 但空集在无竞品时恒空 (零信息)

- **位置**: `proposal.md:28` (「返回 `outcome=passed` / `proceed=true` / **`push_success=true`** / `linked_issue_overlap=[]`」)
- **问题**: 该次实跑坐实的是 D6 (`--phase A.1` 无需改代码) 与 D7 (`push_success` 真), 这两点措辞准确。但 `linked_issue_overlap=[]` 被并列列出后, 读者容易读成「overlap 通道也验过了」。实际上无竞品时它**恒为 `[]`** —— 对匹配逻辑正确与否零信息。更糟: C1 描述的格式失配下, 返回的**也正是 `[]`**, 两种情形不可区分 (同 memory `feedback_false_green_dual_is_permanent_red` 的判据「该信号在健康常态下应是什么值」)。
- **建议修法**: `:28` 收窄措辞为「本次 dogfood 坐实 D6 + D7 两点; `linked_issue_overlap` 的正向匹配**未被本次实跑覆盖** (无竞品时恒空)」, 并把它的正向验证明确挂到 SC-1 —— SC-1 需人造一条他轨 active claim 才能证伪, 应在 SC-1 里写明该前置构造步骤。

---

## 附: 已核实为**正确**的点 (不构成 finding, 记录以免后续轮次重复质疑)

- §1:95「`--phase` 是自由字符串 (CLI 无 `choices` 约束)」— 属实。`phase1_gate.py:1189-1191` 的 `--phase` 无 `choices`; 对照 `:1192-1197` 的 `--mode` 有 `choices=["advisory","block"]`。D6 成立。
- §Why:71 引用「`phase-b-developer` :88-93」— 行号准确 (`:88` 为 `check:` 行, `:91-93` 为命令三行, `:93` 含 `[--linked-issue "<repo>#<n>"]` 可选标记)。
- §Why:72 引用「`branch-manager` :149」— 行号准确 (`:149` 为 `phase1_gate.py --raw-track-id <carry-id> --phase B --mode advisory` 行)。
- §Why:70「`phase-a-planner` 零调用」— 属实, `grep -rn phase1_gate aria/skills/phase-a-planner/` 零命中。
- §Why:60「claim 由 phase1_gate 立即写并推远端」— 属实, `phase1_gate.py:721-801` 先 `acquire_claim` 本地写再 `resilient_push`。
- `:129` rule6_note 判「处方性·运行时指令面 → 照跑 AB, 零裁量, 不申请豁免」— 与 CLAUDE.md Rule #6 判据表第二行一致, 判定正确 (但 M4/M7 若采纳会扩大 AB 面, 需同步)。
- `:169-175`「闸门待裁」段对 Rule #10 封闭白名单四类的逐条排除 — 排除理由与 `standards/conventions/configured-gate-authority.md` 的白名单结构一致, 未自行豁免, 判定正确。

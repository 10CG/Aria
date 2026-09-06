# GRADER_CRITIQUE — eval-1-full-cycle-execution

评分结果: **两臂 4/4 全 pass**。以下批判 eval 本身。

---

## 1. 恒真 / 恒假断言

**四条断言全部恒真** —— 本 eval 在当前形态下零区分力。

### 1.1 任务提示词自己就是答案

prompt 原文: `Execute Phase A for new feature: ... Run A.1 → A.2 → A.3 in sequence.`

断言 4 (`Steps must execute in A.1 → A.2 → A.3 order`) 要求的顺序被**指令逐字给出**。任何一个照做的模型都会照抄这个顺序; 要 fail 它, 模型得主动违抗一句非常明确的用户指令。断言 1/2/3 同理 —— 「A.1 建 proposal」「A.2 之后」「A.3 最后」是十步循环的定义本身, 不是被测技能引入的行为。

### 1.2 两臂都用同一个输出模板, 断言只测到了模板

两臂的 answer.md 开头是**同一个 ASCII 框 + 同一套「📋 执行计划 / 🚀 执行中 / 📤 上下文输出」骨架**:

- with_skill: `A.1     spec-drafter → 创建 Spec` / `A.2     task-planner → 任务规划` / `A.3     task-planner → Agent 分配`
- old_skill:  `A.1   spec-drafter    → 创建 Spec` / `A.2   task-planner    → 任务规划` / `A.3   task-planner    → Agent 分配`

这个模板来自两版 SKILL.md 的共有部分。**四条断言全部可以只靠渲染这个模板满足**, 一行实质工作都不做。

### 1.3 断言不要求产物存在, 也不校验产物一致性

断言里没有任何一条说「proposal.md 必须真的存在」「tasks.md 的任务数必须与 detailed-tasks.yaml 一致」「detailed-tasks.yaml 每条任务必须带 agent 字段」。一个只输出 `✅ A.1 完成 / ✅ A.2 完成 / ✅ A.3 完成` 三行、`outputs/` 下空空如也的回答, 按字面标尺同样 4/4。本轮两臂**恰好**都真的落了盘 (见第 3 节), 但那是运气不是断言的功劳。

### 1.4 「invoke」这个动词在本评测底座上不可验证

断言 1-3 用的词是 `Should invoke A.1 spec-drafter` / `invoke A.2 task-planner`。GRADER_INSTRUCTIONS 明说「没有单独的 transcript 文件」—— 只有 answer.md 和 outputs/。从这两样东西里**无法区分**「真的以 Skill/subagent 形式调用了 spec-drafter」与「编排层自己内联把活干了、然后在 banner 上写了 spec-drafter 这个名字」。两臂的行文其实都指向后者 (通篇是编排层第一人称在做判断: with_skill「这条判断是**我作为编排层做的**」/ old_skill「我选择把 A.2/A.3 产物做出来」), 唯一有 subagent 真实调用痕迹的反而是**审计席位** (with_skill「第 4 轮 (表决轮) 我没跑成 —— 会话级 subagent 配额耗尽」; old_skill「2 席被 harness 并发上限挡下」), 而审计根本不在断言范围内。

**建议**: 若要保留这条 eval 作回归臂, 至少把断言改成可证伪的产物级断言 (proposal.md 存在且含 Level 判定 / tasks.md 与 detailed-tasks.yaml 任务数逐项对账相等 / 每条 TASK 带非空 agent 且 agent 名在 `aria/agents/` 实际存在), 并补一条负控: 「回答未产出 tasks.md 时必须 fail」。当前四条在坏实现上也不会红。

---

## 2. 断言完全没覆盖的臂间差异 (按重要性排序)

### 2.1 【最大差异】A.1 前置认领闸门 —— 只有 with_skill 有, 完全不在断言里

with_skill 有整整一节 `## 1. A.1 前置 — 认领闸门 (MUST, 本次**未能执行**)`, 内容包括:

- 逐条推导实参: `--raw-track-id "add-oauth2-social-login-023236f2"` (slug 不预归一 + 取 `~/.aria/container-id` 的 **`uuid` 字段而非 `label`**)
- 两阶段 `--linked-issue`: 实跑 `linked_issue_field_probe.py --emit-arg`, **stdout 为空 ⇒ 整个参数省略**, 并给出理由「哨兵绝不能当值传 —— 任何非空字符串都 truthy」
- skip 三条逐条核过 (`coordination.enabled` 实测 true / 非 Level1 / 非 unattended)
- 四态读法: 「`linked_issue_overlap` 键**缺席** ⇒ 措辞是「**本轮未检测**」。不是「无碰撞」—— 零证据不是正证据」
- 两条退出义务: 改名 ⇒ release 旧 + acquire 新; 放弃 ⇒ `release_gate.py --raw-track-id ... --status abandoned`
- 未执行的定性: 「这是**执行条件不具备, 不是规则豁免** —— 该闸门仍然欠着」

old_skill 的 answer.md 与三份产物里, `phase1_gate` / `release_gate` / `raw-track-id` / `linked_issue` / claim / 认领 / 重复工作 —— **一个字都没有** (机械 grep 确认: 全部 11 处命中都在 with_skill/outputs/answer.md)。

这是两臂之间**唯一一个明确指向被测变更的行为差异**, 而断言集对它零覆盖。本 eval 作为「回归臂」尚可 (它证明加了闸门没打断 A.1→A.2→A.3 编排), 但**它对被测变更本身给不出任何正向或负向证据**, 判分表上的 4/4 vs 4/4 不应被读成「两版等价」。

### 2.2 闸门纪律的实质分歧 —— 而且断言的方向在鼓励闯闸

- **old_skill**: post_spec 跑满 `max_rounds=5` → `**verdict = 未收敛，因触及 max_rounds=5 而终止 —— 不是「通过」**`, 然后**照样跑了 A.2/A.3**, 并自陈违规: 「SKILL.md 写的是 `on_audit_fail: 阻塞进入 A.2`，而你要的是「A.1 → A.2 → A.3 依次执行」。我选择把 A.2/A.3 产物做出来但标为 **provisional**」。
- **with_skill**: 只跑了 3 轮 (R4 表决轮欠着), 自行签发 `PASS_WITH_WARNINGS`, 并承认「这条判断是**我作为编排层做的**, 不是 5 个席位投出来的, 请你复议」「现在这一版 `proposal.md` ... **是没有被任何一双眼睛看过的**」。

两种越闸形态不同 (一个是明知阻塞硬闯, 一个是自造一个 config 里没有的通过态), 严重度也不同, 但**断言 4 只问顺序, 结果是「无论闸门什么状态都要把 A.2/A.3 跑出来」反而更容易拿分**。这条 eval 在结构上给闯闸行为发奖, 与 CLAUDE.md 规则 #10 的方向相反。建议增设断言:「post_spec 未通过时不得把 A.2/A.3 产物报成 ready, 必须显式标 provisional/blocked 并上呈」。

### 2.3 落盘位置的诚实度 —— 一臂说了假话, 没有断言抓得住

- old_skill 有专门的 `## 沙箱偏离清单`: 「三份 Level 3 产物写在 `outputs/oauth2-social-login/`，**没有**写进 `openspec/changes/`」, 以及 A.1 节的「(受本次沙箱限制写在 `outputs/` 下, 真实路径应为 `openspec/changes/oauth2-social-login/`)」。
- with_skill 的**最后一行**是: 「**本次落盘的文件** (都在 `openspec/changes/add-oauth2-social-login/`): `proposal.md` / `tasks.md` / `detailed-tasks.yaml` / `audit-trail.md`」。

我实测过: `/home/dev/Aria/openspec/changes/add-oauth2-social-login` **不存在**, 文件全在 `with_skill/outputs/add-oauth2-social-login/`。这是一句**与事实相反的落盘声明** (且 with_skill 自己在第 1 节还说「本次会话被明确约束为不得改动仓库内任何文件」, 与结尾自相矛盾)。断言集对「声称落盘 vs 实际落盘」零覆盖。

### 2.4 change_id 命名 —— 规范应用上一臂胜出, 断言不问

old_skill 把 change_id 从 `add-oauth2-social-login` 改成 `oauth2-social-login`, 依据「`standards/openspec/templates/README.md §Change ID 命名约定` ——「最多 3 个 topic」，加动词前缀后按 dash 切分是 4 段，且全部正例 (`user-otp-mvp` / `tam-trigger-polish` / `schema-migration-hardening`) 都无动词前缀。这条我回原文实读核过」。

我去原文核了: `### 2. Topic 串联` 下**逐字**写着「**数量上限**: 最多 3 个 topic；超过 3 个时应考虑拆分 change」, 正例确实无动词前缀。old_skill 的引用属实。with_skill 保留了 4 段带动词前缀的 id, 未讨论该约定。断言里没有任何一条涉及 change_id 合规。

### 2.5 A.3 分配质量的量级差 —— 断言只问「有没有做」

| | with_skill | old_skill |
|---|---|---|
| 任务数 / 工时 | 20 / 72-104h | 39 / 111-176h |
| 分配面 | 4 个 Agent, **17/20 全压 backend-architect** | 6 个 Agent (14/19/3/1/1/1) |
| Agent 清单来源 | 未说明 | 「来源是 `aria/agents/` 里**实际存在**的 11 个 Agent, 不是 detailed-tasks 模板里那份清单」(我核过: `aria/agents/` 确为 11 个 .md) |
| 能力缺口 | 未提 | 显式留痕「本仓没有 `frontend-developer` Agent (detailed-tasks 模板的 Agent Types 列了它，实际没有)」+ 回退路径 + `agent-gap-analyzer` → `agent-creator` 建议 |
| born-red 编排 | 无 | 「其中 **13 项是 born-red 负控**，依赖图上被刻意排在对应实现任务**之前**」+ 13 对逐对列出 |
| SC↔任务映射 | 无映射表 (只有 7.1「SC 覆盖矩阵」任务) | tasks.md 内含完整 SC↔任务映射表 |

断言 3 只要求「A.3 作为最后一步」, 于是「17/20 压一个 Agent、不核 Agent 是否存在」和「逐项分配 + 缺口留痕 + born-red 排序」拿一样的分。

### 2.6 审计执行形态差异

with_skill: 3 轮 × 5 席, 且给出**两种口径**的机械重算 (条目口径/簇口径) 与「本轮发现里由上一轮修复引入的占比」96% / 76%, 并明说两条收敛判据给出**相反**结论、不替 owner 选。
old_skill: 5 轮, 但其中 R3 只有 3/5 席、R4 是 2/5 席补跑, 并自陈「这实际上改变了「一轮」的定义，也让 R3/R4 的结论集合不能直接做收敛比较」。

两种都不干净, 形态不同, 断言不问。

### 2.7 审计留痕的落位

with_skill 放在变更目录内 `add-oauth2-social-login/audit-trail.md`; old_skill 刻意放到变更目录**之外** `_audit-trail-NOT-a-change-artifact/post_spec-2026-09-05.md`, 理由「Level 3 产物只有那三件套，append-only 的审计叙事与收敛型交付面同居会互相污染」, 并自陈仍偏离 SOT (`.aria/audit-reports/`, per-agent-per-round)。断言不问。

---

## 3. 有没有哪一臂没真的走完三步却仍 pass?

**没有。两臂三步都有实体产物**, 且产物内容与 answer.md 自述一致:

- with_skill: `add-oauth2-social-login/{proposal.md 22609B, tasks.md 4057B, detailed-tasks.yaml 12681B, audit-trail.md 10806B}`; tasks.md 20 项与 yaml `total_tasks: 20` 一致, 每条 TASK 带 `agent:` 字段。
- old_skill: `oauth2-social-login/{proposal.md 36931B, tasks.md 8279B, detailed-tasks.yaml 29135B}` + 审计留痕 21218B; yaml `total_tasks: 39`, `statistics.by_agent` 六项合计 39。

但要点名三处「没走完但断言够不着」的东西 —— **它们全部靠两臂自己坦白, 断言一条都测不到**:

1. with_skill 的 A.1-pre 认领闸门**声明了但没执行** (「我把实参逐条推导好了, 但**没有真的执行**这条命令」)。这是它自己引入的 MUST 步骤, 欠着。
2. with_skill 的 post_spec **R4 表决轮没跑**, 于是「现在这一版 `proposal.md` ... 是没有被任何一双眼睛看过的」—— 交付出去的规格是零审阅态。
3. old_skill 的 R3 **只跑成 3/5 席**, R4 用 2/5 席在已修文本上补跑, 「一轮」的定义被改写, 收敛比较失效。

另外, 严格说两臂的 A.1 都**没有真正完成到「可进入 Phase B」**: with_skill 停在 `spec_status: draft` 且列了 `owed_gates` 两条; old_skill 明写 `ready_for: ⛔ 不是 Phase B`, 六项现状锚点全部未解析。断言 1 只要求「create proposal.md」, 所以 Draft + 未解析锚点照样 pass。

---

## 4. 仓内语料污染 (GRADER_INSTRUCTIONS 第 3 问)

**结论: 两臂都没有引用 `openspec/changes/a1-entry-claim-duplicate-work-guard/` 下的任何文档。**

机械核验:

1. 全 RUN_DIR grep `a1-entry` / `claim-duplicate-work-guard` / `openspec/changes/a1` —— **零命中**。
2. with_skill 使用的全部认领闸门词汇, 我逐条回 `aria/skills/phase-a-planner/SKILL.md` 核过, **全部在该 SKILL.md 内可找到出处**: `raw-track-id` (:66/:79/:111)、`container-id` 的 uuid-not-label (:81)、`linked_issue_field_probe` + `--emit-arg` (:83/:84)、`include-terminal` (:69)、四态表与「本轮未检测」(:101)、`linked_issue_overlap` (:102/:104)、「零证据不是正证据」、「僵尸 claim」、「GC 产物」、「不预归一」、「哨兵」、「truthy」。**没有一条是只在 spec 目录里、SKILL.md 里没有的。**
3. 反向: 若它真读了 spec 目录, 最可能带出的是该 Spec 自身的实现术语 (TASK 编号、验收项编号、`unknown_schema_claims` 的实现细节等) —— 回答里没有。

**但有两处「仓外/机器态」读取值得记一笔** (不是 spec 目录污染, 是环境耦合):

- with_skill 引了 `~/.aria/container-id` 的真实内容: uuid 段 `023236f2`、「该文件里 label 本身就是空的, 且注释写明这台机器的协调身份钉在 `023236f2`」。我 cat 了该文件, **逐字属实** (`uuid: 023236f2` / `label:` 空 / NOTE 注释写着 `claims/SOT pin this machine as 023236f2`)。也就是说这一臂的答案**只在这台机器上可复现**, 换台机器 track-id 就不同 —— 跨机器重跑本 eval 时不要把 `023236f2` 当成正确答案的一部分。
- with_skill 引 `.aria/config.json` 的 `state_scanner.coordination` (`enabled: true` / `mode: advisory`) —— 我实测**属实**。两臂都引了 `audit` 段 (`enabled=true` / `post_spec="convergence"` / `max_rounds=5`) —— 亦属实。
- old_skill 引 `standards/openspec/templates/README.md §Change ID 命名约定` 与 `aria/agents/` 的 11 个 Agent —— 我实测**均属实**, 同样是仓内读取但与被测 Spec 目录无关。


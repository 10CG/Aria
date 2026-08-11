---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-11T02:10:00.000Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R2 审计报告 — knowledge-manager 席位

被审对象: A.2 产物 (R1-fix 后) `proposal.md` + `tasks.md` + `detailed-tasks.yaml`。执笔方 = tech-lead (换人执笔), 主 loop 只核验。

镜头 (本轮不变): 规范合规 (Rule #5/#6/#9/#10) / Level 3 三件套完整性 / follow-up 是否可证伪 / 文档同步面是否枚举完整。

已采信 `/tmp/claude-1000/-home-dev-Aria/a87f33ea-9a9d-49e2-a762-18d0fd38bfc4/scratchpad/verified-ground-truth.md` 与 `adjudication-draft.md` 的既有实测结论, 未重复核验其覆盖的项; 本报告只对**我自己镜头范围内**、且**这两份文件未覆盖**的部分做独立实读/实跑。全程只读, 未改任何文件。

---

## 投票

**VOTE: PASS(with warnings)** —— 0 Critical, 1 Major(新发现), 1 Minor(新发现)。**不阻塞 Phase B**(TG-0~TG-2 均与本轮发现无关), 但须在 TG-4(follow-up issue 开具)执行前修正, 否则会静默漏掉一条本该被转记的 issue。

---

## 一、R1 我自己两条 Major 的闭合核验(逐条回源, 非采信声称)

### M-1(TASK-015 Rule #6 验收缺工具口径与结果判据)—— ✅ **已闭合**

实读当前 `detailed-tasks.yaml` TASK-015 verification(4 条):
```
- '**须用 `/skill-creator` 跑** (CLAUDE.md 规则 #6 逐字: 自研 runner 已废弃), 非任意 runner'
- 两套件 ab-suite/phase-c-integrator.json + phase-c-integrator-pre-merge-gate.json 均跑完, 结果存 ab-results/
- '结果判据按 AB_TEST_OPERATIONS.md 发版前 checklist: WITHOUT_BETTER verdict 审查 + 回归比对 + summary.yaml 审查'
- '**不得以「套件对 C.2.4 覆盖薄」为由降档** — 判据表第二行是零裁量的'
```
实跑核对引用来源:
```bash
grep -n "发版前\|Tier 1 Skills 全量\|summary.yaml 已生成并审查\|无 WITHOUT_BETTER\|与上一次结果比对" aria-plugin-benchmarks/AB_TEST_OPERATIONS.md
→ 544:### 发版前
→ 545:- [ ] Tier 1 Skills 全量 AB 测试已执行
→ 546:- [ ] summary.yaml 已生成并审查
→ 547:- [ ] 无 WITHOUT_BETTER verdict 的 Skill (否则必须修复)
→ 548:- [ ] 与上一次结果比对，无回归
```
行号未漂移, 内容逐字对得上(4 条清单 3 项在 verification 里已覆盖, 第 1 项"全量已执行"由"两套件均跑完"覆盖)。`/skill-creator` 工具点名也已补上。**M-1 闭合属实。**

### M-2(ship_target 四处不一致 + MAJOR⇒v2.0 弃用到期承诺无任务承接)—— ✅ **已闭合**

实跑 grep 核对四处口径:
```bash
grep -n "地板\|待裁\|待确认" openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
→ :12  (抬头) "**MAJOR** ... 2026-08-10 依 owner 授权裁定确认 MAJOR, 不再是「待确认」"
→ :236 (D11)  "版本 **MAJOR** ... 上一版写「版本地板 MINOR」, 与抬头及 §版本 的 MAJOR 自相矛盾"
→ :318 (§版本) "结论: MAJOR ... 不再是「待裁」"
```
`tasks.md:5` 与 `detailed-tasks.yaml:35`(`ship_target:` 字段)同为 MAJOR、同一措辞("2026-08-10 依 owner 授权裁定确认, 不再是「待确认」")。四处逐字一致, 均未残留旧版「地板 MINOR」措辞。

v2.0 弃用到期承诺: 新增 **TASK-020**(条件任务, 触发条件已满足)在 `tasks.md` 组 3 与 `detailed-tasks.yaml` 均在位, 删除面覆盖 5 文件跨 2 仓、两个 legacy key(`primitive_preference`/`no_aether_fallback`), 含 fail-CLOSED 处置与错误文案指路要求。**M-2 闭合属实。**

---

## 二、R1 我自己三条 Minor 的闭合核验

### M-3(a)(scope_repos 缺 `head` 锚定字段)—— ✅ **已闭合**

实读 `detailed-tasks.yaml:6-33`: `aria` 条目 `head: af87cae`, `Aria` 条目 `head: 98ad1f5`, 均带 `scope_notes` 说明新增落点的裁定来源。与姊妹 Spec `linked-issue-normalization` 的模式对齐。

### M-3(b)(TASK-001 两层给出不同路径选择集)—— ✅ **已闭合**

```bash
grep -n "test_premerge_gate_mainbranch\|或并入既有文件" tasks.md detailed-tasks.yaml
→ (零命中)
```
`tasks.md` TASK-001 现文本不再提供「新建文件」选项, `detailed-tasks.yaml` deliverables 仍只列既有 `test_pre_merge_gate.py`。两层现在给出唯一选择集。

### M-4(未决#1 已被自身产物解答, 应转记 standards 维护者)—— ⚠️ **名义闭合, 但转记承诺失真, 见下方新发现 F-1**

`tasks.md:103` 已按我 R1 的建议重写:「原「detailed-tasks.yaml 是否补」的真正待决项是 `standards/openspec/project.md` 自身 `:21`(双层)与 `:118`(单层)两处表述矛盾 —— 应转记给 standards 维护者, 不属本 Spec(**TASK-019 已纳入**)。」

措辞本身是我 R1 建议的两个选项之一(转记), 但**"TASK-019 已纳入"这句核验后不成立** —— 见下方 F-1。这是**闭合动作本身引入的新缺口**, 单独作为一条新 Major 报告, 不算作 M-4 的失败重开(M-4 原文批评的"待决项已过期"这一点确实被修好了)。

### M-5(TASK-019 verification 只证"该写什么", 不证"issue 确实存在")—— ✅ **已闭合**

实读 `detailed-tasks.yaml` TASK-019 verification 新增第 7 条:
```
'**每条 follow-up 必须有可 GET 的 issue 编号/URL 回填本文件** —— ⚠️ 上一版五条 verification
全是「issue 该写什么」, 该任务可在零 issue 创建下自称完成 (post_planning R1 两席命中)'
```
补上了存在性断言(可经 Forgejo GET 检索), 与我 R1 建议的修法方向一致。**M-5 闭合属实。**

---

## 三、R1 三条 Critical(非我原始发现, 但属"文档/验收枚举完整性"范畴, 轻量复核)

| Critical | R1 描述 | 本轮复核 |
|---|---|---|
| PC1 | TASK-011 验收对 `--main-branch` 失明(写死 main 全过) | ✅ 复核: `proposal.md:248-252` 新增 SC-M3b(负控, 拒绝写死 `main`/`master`字面值)+ SC-M3c(负控, 拒绝调用藏进折叠块), 且逐字声明"已做对抗性验证...两个坏实现各被 M3b/M3c 拒绝"。`ground-truth.md §2` 已实跑 SC-M3a/b/c 三值与 Spec 一致。closed。 |
| PC2 | SC 编号与既有测试全面冲突(SC-1..13 全撞) | ✅ 复核: 全部改用 `SC-M` 前缀(`SC-M1`..`SC-M13`), `grep -c 'SC-M' proposal.md` 命中密集, 未见裸 `SC-1`..`SC-13` 残留于本 Spec 新增断言里(仅 `tasks.md` 引用既有 `test_sc12`/`test_sc22` 等既有测试自身编号, 属被引用对象, 非本 Spec 新增编号冲突)。closed。 |
| PC3 | 组 0「先看到红」只覆盖 4/13 条 SC, SC-6~13 无 owning task | ✅ 复核: 现 TG-0 含 TASK-001(grep 类)+ TASK-002/003/004(spike, 对应 SC-M12 / SC-M6+M13 / SC-M7+M8)+ TASK-005(测试隔离接缝); TASK-008 verification 显式收口 "SC-M6/M13/M7/M8 全绿"。SC-M9(TASK-006)/SC-M10-M11(TASK-008)均有 owning task。closed。 |

三条 Critical 的闭合证据来自 tasks.md/yaml 结构本身, 与 ground-truth 已实跑的 SC 值一致, 未见回退。

---

## 四、新发现 — R2 本轮

### F-1(Major)—— `tasks.md:103` "TASK-019 已纳入" 的转记承诺不成立, 是 R1-fix 引入的新缺口

**锚点**: `tasks.md:103`(已裁段落, 转记声明)· `tasks.md:95`(TASK-019 全文)· `detailed-tasks.yaml:464-489`(TASK-019 完整定义)

`tasks.md:103` 逐字:
> 原「detailed-tasks.yaml 是否补」的真正待决项是 **`standards/openspec/project.md` 自身 `:21`(双层)与 `:118`(单层)两处表述矛盾** —— 应转记给 standards 维护者, 不属本 Spec (**TASK-019 已纳入**)。

实跑核验 TASK-019 的完整内容(两层)是否真的"纳入"了这一项:
```bash
grep -n "project.md\|standards" tasks.md
→ :23  (SC-M12 的五种 cwd, 与本议题无关)
→ :103 (即上引这句本身)

grep -n "project.md\|standards" detailed-tasks.yaml
→ :91  (SC-M12 五种 cwd, 无关)
→ :103 (TASK-002 notes 提 standards 子模块根, 无关)
→ :461 (TASK-018 blast radius grep 覆盖 standards/, 无关)
```
TASK-019 的 (1)-(6) 六项 follow-up 清单(`tasks.md:95` 与 `detailed-tasks.yaml:476-488` 两层内容一致)逐条核对:
```
(1) main_branch 自动解析设计面
(2) fetch_gate.py / worktree_manager.py:170 同形回落
(3) workflow-runner gate_state 无 gate_error 位置
(4) 显式传错分支名零测试覆盖
(5) C.2.4.5 裸 git 命令 + submodule_gate.sh
(6) helper 定位形态其余落点
```
**六项中没有任何一项是 `standards/openspec/project.md:21` 与 `:118` 的表述矛盾。** `grep -n "project.md" detailed-tasks.yaml` 在 TASK-019 的 `verification:` 块内(`:476`-`:489`)零命中。

**它怎么会红**: 若 TASK-019 严格按照(1)-(6)六项执行(这正是它自己的验收清单要求的"每条 follow-up 必须有可 GET 的 issue 编号/URL"), 执行者只会为这六项开 issue, `standards/openspec/project.md` 的双层/单层矛盾**不会**被开出对应 issue。而 `tasks.md:103` 明确告诉读者"不用管这条了, TASK-019 已经接住它" —— 这是一句**读者会信、但按现状文本执行不会兑现**的承诺。这正是本项目反复出现的"paper-fix"/"声明留痕但无机制兜底"形状(与 memory `feedback_paper_fix_antipattern` 同形; 与 R1 自己抓的 M-2「MAJOR 连锁后果无人承接」、PC2「重定范围时静默丢失已修复项」同一类"写了但没接住"缺陷)。

**是否是 R1-fix 新引入**: 是。R1 原文(`M-4`)只是把这句话标记为"陈旧待决项", 未提及 TASK-19 是否纳入; 是本轮 R1-fix 执笔时新写的"转记给 TASK-019"这个具体承诺, 但**未同步在 TASK-019 正文里加第 7 项**。属于"改一处、声称改了另一处"的形状(R1 汇总表里编排层本轮已出现过一次同款 #21 "修落一处, 声称留另一处"), 本轮在换人执笔后**又出现了一次同形状缺陷**, 值得写进「R1-fix 是否引入新缺陷」这条判据的证据里。

**修法建议**(不越权, 仅供执笔参考): 二选一 —— (a) 在 `tasks.md`/`detailed-tasks.yaml` 的 TASK-019 清单里补第 (7) 项("`standards/openspec/project.md:21` 与 `:118` 表述矛盾, 转 standards 维护者"), 且同步补两层; 或 (b) 把 `tasks.md:103` 的措辞改回"未转记, 待办"而非"已纳入", 不能两边都不做又两边都不改。

**blocks_phase_b**: false — TG-0~TG-2 与此无关; 但在 TG-4(TASK-019 执行, 开 issue)之前必须解决, 否则会静默漏掉一条转记, 且与 TASK-019 自己刚补上的"存在性断言"(M-5 的修法)自相矛盾 —— 存在性断言只能保证列出的六项被开 issue, 保证不了一条从未被列入清单的第七项。

### F-2(Minor)—— `detailed-tasks.yaml` TASK-019 verification 第 (3) 项比 `tasks.md` 对应条目多出一个未定义术语 `main_branch_resolved`

**锚点**: `detailed-tasks.yaml:478`(TASK-019 verification 第 3 条)· `tasks.md:95`(TASK-019 第 (3) 项)

`detailed-tasks.yaml:478` 逐字:
> `(3) workflow-runner gate_state 无 gate_error / main_branch_resolved 位置 — issue 正文须带两个实测数: ...`

`tasks.md:95` 对应文字:
> `(3) workflow-runner gate_state 无 gate_error 位置; ...`

`main_branch_resolved` 只在这一行出现:
```bash
grep -rn "main_branch_resolved" openspec/changes/premerge-gate-mainbranch-failclosed/
→ detailed-tasks.yaml:478 (唯一命中)
```
它未在 `proposal.md` 的任何 SC/D 决策/schema 里被定义或提及, 也未在 `tasks.md` 同条目里出现 —— 是 yaml 单侧新增的一个孤立术语, 不清楚指向 `gate_check()` 输出里的哪个字段(现有 schema 只有 `verdict`/`raw_message`/`gate_error` 三个相关键, `proposal.md §7` 逐字列出的 additive 键是 `gate_error`, 没有 `main_branch_resolved`)。

**它怎么会红**: 若 TASK-019 的执行者只读 `tasks.md`(A.2 的人类可读入口), 不会看到这个术语, 开出的 issue 正文会比 yaml 期望的少一个"数据点"; 若执行者只读 `detailed-tasks.yaml`(机读 SOT), 会去核验一个 Spec 全文都未定义过的字段名, 无法解析其含义。两层不同步, 与 R1 的 `M-3(b)`(TASK-001 两层给出不同路径选择集)是**同一形状的缺陷在另一处的复发**。

**严重度**: Minor —— 不影响 TG-0~TG-2, 且即便 TASK-019 执行者按较窄的 `tasks.md` 措辞执行, issue 内容也不会因此产出错误代码或阻塞合并, 只是 (3) 号 issue 的完整度两层不一致。

**blocks_phase_b**: false。

---

## 五、Rule #5/#6/#9/#10 与 Level 3 三件套 — 汇总判定

- **Rule #5**: ✅ 合规。`proposal.md:11` 明示"代码落点: aria/ 子模块...; Spec 落主仓 (Rule #5)"; 变更放在 `/home/dev/Aria/openspec/changes/premerge-gate-mainbranch-failclosed/`(主仓自身 openspec/changes/, 非 `standards/openspec/changes/`)。
- **Rule #6**: ✅ 合规。`proposal.md` §Rule #6 段落逐字引用 SOT `standards/conventions/skill-benchmark-exemption.md:33`「`description` 或指令流程变动 ⇒ 一律第二行」, 已实读该行确认逐字一致; `TASK-015` 验收补齐工具点名(`/skill-creator`)与结果判据(见上 M-1 闭合核验), 未申请豁免。
- **Rule #9**: ✅ 合规(无违反迹象)。`grep -rn "\.aria/handoff" openspec/changes/premerge-gate-mainbranch-failclosed/` 零命中; 全部"须写入 handoff 请复议"表述均未指错路径。
- **Rule #10**: ✅ 合规。`tasks.md` 组 4 后段"已裁"章节明确留痕四条 AI 依 owner 授权定夺的裁定(非 owner 逐条签字), 并声明"全部须写入 handoff 请复议"; `proposal.md` 的 MAJOR 裁定同样留痕 owner 授权来源与复议要求。未见自作主张跳过某项已启用闸门。
- **Level 3 三件套**: ✅ 齐备且互洽 —— `proposal.md` + `tasks.md`(20 checkbox)+ `detailed-tasks.yaml`(20 task, `level: 3`)三者 checkbox/task 数一致(`grep -c` 均为 20), `head` 锚定字段已补, `scope_repos` 与 `proposal.md` Impact 表文件枚举一致。

---

## 六、我认为的阻塞项(进入 TG-4 前)

1. **F-1 必须解决** —— `tasks.md:103` 的"TASK-019 已纳入"要么在 TASK-019 六项清单里补上第 7 项, 要么改口措辞, 二选一, 不能两边都不动。这是本轮唯一影响 follow-up 可证伪性的 Major。
2. **F-2 建议顺手修** —— `main_branch_resolved` 要么在 `tasks.md` 同步补上并定义其含义, 要么从 `detailed-tasks.yaml` 里删掉, 使两层一致。不阻塞 TG-0~TG-3, 但应在 TASK-019 执行前(TG-4)处理, 避免 issue 内容依两层读者而异。

两项均**不阻塞 TG-0~TG-2**(TDD 前置/实现/SKILL.md 三组), Phase B 可以推进; 但在 TG-4(follow-up issue 开具)执行前应处理, 否则 TASK-019 自己刚补上的"存在性断言"验收(M-5 的修复成果)会被这条静默漏项打出一个例外。

---

## 七、方法论观察(供 handoff 参考)

R1 汇总表的"编排层本轮新增错误 #21 —— 修落一处, 声称留另一处"这个形状, 在**换人执笔**的 R1-fix 里又复现了一次(F-1), 但复现的位置变了: 不再是"改了代码没改文档"型, 而是"改了措辞、承诺了转记, 但没有真的往目标清单里加条目"型。这提示"换人执笔"改变的是**谁在犯错**和**在哪类内容上犯错**(本轮换人后, tech-lead 执笔在 SC/依赖图/decision 表层面的机械一致性上表现显著优于 R1 编排层原作者 —— 详见本报告第一/二节全部闭合), 但**"声称完成的动作实际未落地"这一缺陷形状本身没有被换人这件事根除**, 只是发生率与影响面都明显收窄(本轮我的镜头范围内只抓到 1 Major + 1 Minor, 相比 R1 同镜头的 2 Major + 3 Minor 是净收敛)。

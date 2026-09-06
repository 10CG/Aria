# RESULT — Rule #6 AB 总账 · `a1-entry-claim-duplicate-work-guard` → aria-plugin v1.70.0

> **日期**: 2026-09-05 ~ 09-06 | **执笔**: 主控 (Claude Opus 5) | **会话前置**: `ARIA_COORDINATION_NO_PUSH=1` (实测生效)
> **规模**: 6 套件 / 31 eval / 66 臂 / 67 份 grading / 34 份 grader critique
> **逐 eval 分数**: 见 `SCORES.md` (脚本汇总, 不经人工转述) | **缺陷**: 见 `DEFECTS.md` (24 条分四类)

---

## 1. 结论

### 1.1 唯一有效度的数字

| 分组 | with | old | delta |
|---|---|---|---|
| **定向 fixture (7 条)** | **45/45 (100%)** | **16/45 (36%)** | **+0.644** |

分套件: `phase-a-planner` 25/25 vs 13/25 · `spec-drafter` 14/14 vs 1/14 · `state-scanner` 6/6 vs 2/6。
三者**各自成立**, 不靠单条撑起。这些断言含否定条件、字面串、负向条件, 有区分能力。

### 1.2 回归面: **未被有效测试**, 不是「已验证无回归」

回归臂机械分数 with 85/110 vs old 82/110 (+0.027)。**该数字判定为无效度, 不作任何结论依据。** 理由见 §3。

「无回归」这个判断本身**成立**, 但证据来源是**主控手工横向比对**, 不是断言:
- 五个 eval 的输出特征横向对照 (中断检测 / git 操作感知 / 置信度 / 工作流名), 方向不一致 ⇒ 噪声
- eval 3 做了三轮复跑共 **7 个样本**, 目标区块命中率 with 0/4 · old 1/4 ⇒ 两臂共有的既有缺陷, 非本轮引入

**「没检出」与「已验证」是两回事。本次只做到前者。**

### 1.3 Rule #6 三档履行情况

| 判据表档位 | 落点 | 结论 |
|---|---|---|
| 处方性 · 运行时指令面 (照跑, 零裁量) | hunk #1/#2/#5/#7/#8/#9 | ✅ 六套件全跑完 |
| 处方性 · 套件覆盖外 (定向 fixture) | hunk #3/#4 | ✅ **+0.644** |
| 描述性 (substitute) | hunk #6/#10a/#11/#12 | 上一 session 已落结构化断言 (Group 6) |

---

## 2. 过程中改动了制品 — 一次, 且不是为了过测试

**触发**: `phase-a-planner` eval 4 的 with 臂 5/6, 唯一 FAIL 是「告警须含双方 `linked_issue` 原串」。

**根因实读**: `proposal.md:277` 逐字要求「告警须含: 对方 track-id / owner-container / claimed_at / **双方 `linked_issue` 原始串** / `status`」, 而**两个落点的 SKILL.md 都没有这一条**。按 memory `fix-the-class` 查兄弟位置时另发现 `spec-drafter` **整段 overlap 分档都缺失** (`proposal.md:668` 要求它是「同上的步骤块」)。

⇒ 判为 **A.2/A.3 派生漏抄** (与本 cycle M4 那五处同族), 按跑前写死的规则「指令面缺陷 ⇒ 回改 SKILL.md, **不改断言**」补入。

| 落点 | diffstat | 行尾 | 修前 blob | 修后 blob |
|---|---|---|---|---|
| `phase-a-planner/SKILL.md` | **+4 / −0** | LF (原样) | `6206e2cc6451` | `325885f6b2b2` |
| `spec-drafter/SKILL.md` | **+12 / −0** | **CRLF 保持** (520→532) | `85db2a1f9f52` | `ef0082a0df8b` |

**因果证据 (同题同断言, 前后对照)**: `10CG/Aria#174` 逐字出现次数 **0 → 6**; eval 4 从 **5/6 → 6/6**。
修前结果**未删**, 归档为 `with_skill_prefix/` + `NOTE.md`。**全程没有改动任何一条 eval 断言。**

---

## 3. 为什么回归臂的分数无效度 (本次最重发现)

### 3.1 四处**奖励错误行为 / 惩罚正确行为**

| eval | 谁被罚 / 谁被奖 |
|---|---|
| **`phase-d-closer` eval 1** | **拒绝在输入缺失时虚构进度记录的臂 0/3**; 用占位 `TASK-001~006` / `stateToken: <recompute>` 编造记录并自评 `upm_updated: true` 的臂 **3/3**。grader 判语: 断言「方向上奖励虚构」 |
| **`phase-b-developer` eval 2** | **拒绝拿别的套件顶替验证 (「那是假绿」) 的臂丢两分**; 换任务跑通的臂满分。**按 Aria 自己的反假绿原则, 被罚的可辩护** |
| `state-scanner` eval 5 A4 | 要求「不执行 fetch, 读 FETCH_HEAD age」, 但现行 Phase 0.5 **强制** fetch 且 `remote_refs_age` 已 **DEPRECATED** ⇒ 做对了扣分 |
| `phase-a-planner` eval 1 A4 | 在 `on_audit_fail: 阻塞进入 A.2` 下**闯闸照跑**仍满分 ⇒ 结构上奖励闯闸 |

**照这个分数优化会把技能改坏。** 开单时列最高优先级。

### 3.2 大面积恒真 / 恒假

机械粗筛: 11 个 `state-scanner` 回归 eval 共 65 条断言, **含否定 / 字面约束 / 具体数值者 = 0**。
`state-scanner` eval 12 曾被我误判为「有牙齿」—— grader 指出五条**全指向 SKILL.md 里同一句话**, 而该句两臂逐字节相同。

典型个例 (完整 11 类见 `DEFECTS.md` A 节): 恒真 (eval 1 三条) · 夹具永不触发 (eval 5 A5/A6, eval 10 三条恒假 + 一条空真) · 推论式 (spec-drafter e3 A3) · grep 面宽于所指缺陷 (spec-drafter e3 A5) · 只测「做没做」不测「对不对」 (state-scanner e3 全部) · 结构性零区分度 (spec-drafter e3 全部 5 条, diff 无一行触及该面)。

### 3.3 断言测不到真实质量差异 — 反复出现

| eval | 断言给的 | 实际发生的 |
|---|---|---|
| `state-scanner` e3 | 三条都测「有没有做核对」 | with 找出**真不一致** (root `VERSION:25` standards **v2.2.3** vs `standards/openspec/project.md:3` **2.2.2**), old 说「全部一致」—— 无断言可分辨 |
| `state-scanner` e4 | 3/3 = 3/3 | **old 编造了一个 github SHA**, 把 `parity: unknown` 渲染成 `✅ 所有远程一致 (origin=github=92acce5)` (#110 族缺陷), with 正确 |
| `state-scanner` e6 | with 2/6 < old 4/6 | **old 把 `git rebase origin/master` 列为同等选项且无 force-push 警告**, 而分支已推两端; with 明确禁止 —— 安全性差异值 0 分 |
| `state-scanner` e7 | 4/8 = 4/8 | with **独立实测** issue 截断 47 vs **74** (逐仓 26/41/2/5, grader 用 API 复核**无一虚构**); old 照抄 handoff 里已过期 1/3 的旧数字 |
| `branch-manager` e1 | 2/2 = 2/2 | **old 把 `<carry-id>` 自行取值成 `TASK-001-user-auth` 落进可执行命令**; with 停下来索取输入 —— **正是本轮改动的目标行为**, 断言白白丢掉 |
| `phase-b-developer` e1/e2 | 3/3 vs 1/3 | old 保留了**本轮已勘正掉的错误陈述**「auto_bootstrap 会自建 ref **并 push**」; 信号得 0 分 |
| `phase-d-closer` e2 | 3/3 = 3/3 | `success` 字段两臂**结论相反**, old 违反契约 `execution-steps.md:142`; 零断言覆盖 |

### 3.4 一处单侧承重污染

`phase-b-developer` eval 2: **仅 with 臂**引用 `openspec/changes/a1-entry-claim-duplicate-work-guard/` (`detailed-tasks.yaml:281` 等), 且**满分正建立在从该 Spec 挑替身任务**上。⇒ 该 3:1 **不得计为区分力**, 干净语料下很可能塌成 1:1。

其余全部为**对称**泄漏 (两臂同经 `docs/handoff/` 与快照), 不产生偏置但压低区分度。

---

## 4. 隔离验收 (AB_TEST_OPERATIONS.md §场景 1 三条)

| 条 | 结果 |
|---|---|
| 1. 会话带 `ARIA_COORDINATION_NO_PUSH=1` 启动 | ✅ 实测 SET (len=1, 值在 truthy 集); 子进程 `no_push_requested_by_env() == True` |
| 2. 远端无合成 claim | ✅ 11 条 claim, 含 `delete-me`/`test`/`eval` 字样者 **0** |
| 3. 跑完强制 `+` fetch 对齐 | ✅ 已执行 |

**协调 ref 全程 `539d231` 纹丝未动。** 更强的一层: **66 个臂没有一个调用 `phase1_gate`** —— 它们各自引 handoff §3 的约束自行规避, `NO_PUSH` 兜底从头到尾没被用上。

仓库收尾干净: 只有三个**有意** dirty 的子模块指针 + 未跟踪的本结果目录。

---

## 5. 数据完整性 — 两处主控失误, 已隔离留档

| 事 | 处置 |
|---|---|
| 重复派发 4 个臂 (SS e3 with/old · e5 old · BM e1 old), 致 2 份 grading 评了已被覆盖的答卷 | 隔离为 `grading.STALE.json` + `STALE_NOTE.md`, **不参与计分**; 已重评。建 `DONE_ARMS.txt` 防重复 |
| 初始允许臂写仓内固定路径 `.aria/state-snapshot.json` (`Path.write_text` 非原子写 630KB × 20+ 并发) | 中途加并发隔离条款 (改写各臂 `outputs/`); **零实际损害** |

**⚠️ 早期我曾据坏数据报过 `state-scanner` eval 3「with 1/3 vs old 2/3, 疑似回归」** —— 那个 old 分数评的是被覆盖的答卷。重评后是 **with 3/3 vs old 2/3**, 方向相反。该结论已撤回。

---

## 6. 附带发现 (仓库真实缺陷, 与本次 AB 无关)

见 `DEFECTS.md` C 节 8 条。最硬的三条:
- **`aria/README.md` skill 名册漏 `issue-triage` / `session-closer`**, 数量对 (42) 但列表只有 40 —— **无任何机械检查覆盖名册**, 漂移活过三个月绿灯
- **`issue_scan.open_count` 静默截断**: 报 47, API 实测 **74** (吞 36%), 被丢的恰含 `aria-plugin#110/#135/#107/#109`、`Aria#136`(secret 泄漏); 降序取前 20 ⇒ **老问题被系统性隐藏**
- **`.aria/config.json` 的 `coordination` 是嵌套键**, 顶层读得 `None` ⇒ 静默误判「闸门未启用」, 与事实相反

---

## 7. 下一步

1. **开 24 条缺陷 issue** (`DEFECTS.md`) —— A 节四条「奖励错误行为」最高优先级, 它们会持续污染后续所有 AB
2. **7.6 套件缺口 issue** —— 依赖 (7.5) 现已解除, 且本次攒了充足素材
3. Group 8 发版 (`<vNEXT>` = **1.70.0**, 执行序 8.1 → 8.4 → 8.2)
4. **heartbeat 待刷** —— 本会话带 `NO_PUSH` 不能刷 (刷了只写本地, 下次 fetch 冲掉); 留给不带该 env 的会话。sweep 死线 **2026-09-06T21:40Z**

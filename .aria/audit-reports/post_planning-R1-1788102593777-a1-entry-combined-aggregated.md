---
round: R1
checkpoint: post_planning
mode: convergence
spec: a1-entry-claim-duplicate-work-guard
context: openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml (+ linked-issue-field-availability + sibling-spec-probe, combined)
seats: [A1-tech-lead, A2-backend-architect, A3-qa-engineer, A4-code-reviewer, A5-knowledge-manager]
verdicts: {A1: FAIL, A2: FAIL, A3: FAIL, A4: FAIL, A5: PASS_WITH_WARNINGS}
votes: {A1: REVISE, A2: REVISE, A3: REVISE, A4: REVISE, A5: PASS}
verdict: FAIL
converged: false
oscillation: false
incomplete: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
max_rounds: 5
totals: {critical: 7, major: 16, minor: 11}
clusters: 11
timestamp: 2026-08-30T16:05:00Z
---

# post_planning R1 聚合 — a1-entry 三份同族 Spec 的 A.2/A.3 产物 (combined) — **FAIL, 未收敛**

被审: `linked-issue-field-availability` (25 tasks) / `sibling-spec-probe` (18) / `a1-entry-claim-duplicate-work-guard` (39, 母)。五席原始计数 7C / 16M / 11m; 按 4-tuple 去重后 **11 簇** (同一 8-char id 在不同席位下命中不同内容 —— 4-tuple 键对「同文件同类同级」的不同缺陷不可分辨, 本聚合按内容分簇, 键集另列)。

## drift_metrics (anchor 快照)

- primary_goal: 三份 proposal 的 What Changes / SC / Impact 忠实派生为可执行 tasks.md + detailed-tasks.yaml (A.2) 并分配 agent (A.3)
- in_scope: 派生忠实性 / 依赖图 / 可执行性 / 机械一致性 / 跨 Spec 接缝 / Rule #6 #10
- out_of_scope_hints: proposal 本身 (post_spec R1–R6 已收敛, owner 裁不加轮); 语义接缝面 (A1 判三份互相咬合)
- source_sha: 主仓 c120f9e / aria d69091d / standards 334c609

## 簇表 (去重后)

| 簇 | 严重度 | 席位 | 内容 | 处置 |
|---|---|---|---|---|
| C1 依赖图: 散文 ≠ `dependencies` | **critical** | A2 ×3 · A3 (1C+3M) · A4 (1C) · A1 (1M) | 同文件任务缺串行边 (三份); 母第 6 组 RED 依赖第 5 组 GREEN (倒置, 红窗结构性关闭); 前置断言 (母 TASK-001 / 探针 TASK-001·003) 不在下游边上; 字段 TASK-007 缺 TASK-006 边; 字段 TASK-016/017 并行写同文件 | 统一规则三条 (同文件串行 / RED 先于 GREEN / 前置在上游) + 程序化验, 见清账方案 C1 |
| C2 发布同步面派生不全 | **critical** | A1 ×2 · A4 (1M) | 探针 TASK-018 / 母 TASK-038 缺主仓 VERSION / badge / i18n ×3 却断言两条 check 绿; `README.zh-CN.md` 不存在 (实为 `README.zh.md`); `.gitmodules` 不承载 gitlink | 以字段 TASK-024 列法为准三份逐字对齐 |
| C3 版本档撞号 | major | A1 · A5 (m) | 字段与母都自判 v1.68.0 而串行 ship 三档; 阻塞强度三份不一; ab-results 字面量未对冲 | 统一占位 `<vNEXT>` + 同一句 owner 待裁留痕 |
| C4 字段对 `audit-engine/` 目录断言过严 | major | A1 | 「只有 references/+SKILL.md」与探针要建 `scripts/`+`tests/` 冲突; 过度派生 proposal :278 | 改为 :278 逐字 (不得新建 `lib/`/`collectors/`) |
| C5 ab-suite 口径 | major | A1 ×2 | `version.yaml` 只探针维护且字面陈旧 (29/58 vs 实测 31/73); `spec-drafter.json` 跨 Spec eval id 无分配约定 | 程序化重算 + `max(id)+1` 约定三份同写 |
| C6 母 TASK-018 不可求值分支 | major | A1 | 「与字段 hunk 不相邻」在字段未 ship 分支无 fallback | 两分支 verification |
| C7 placeholder 黑名单义务单侧 | major | A1 | 写入宿主在字段 Spec, 义务只写探针侧 | 字段 TASK-013/014 各加一条同批改断言 |
| C8 探针 metadata 断言不可复现 | major | A2 | `line_anchor_recheck` 两条 git 远端「实况」零命中 | 改历史观测措辞或删 |
| C9 Schema 字段 | major | A4 | 字段+探针 `est_hours:int` 非 SOT `estimated_hours:str`; 字段 TASK-020 缺 `reason` | 对齐 DUAL_LAYER_SPEC |
| C10 母 SC 覆盖表不真 | major | A4 · A3 (m) | 17 对 (SC,TASK) 在 verification 无该 SC; SC-3 零命中; 12-hunk 表无明细 | verification 补引 + 程序化验 |
| C11 proposal 尾句陈旧 | major | A5 ×3 | 头部 Approved 而尾句仍「批准前不进 A.2」 | **已闭合** (主控回改 :798 / :616 / :578) |

Minor (不成簇): 探针 TASK-010「恰三条 import」vs TASK-011 追加 `is_sentinel` (A4/A5 均判合法, 字面判据改「包含」); 母 yaml 两处 1 行锚点漂移 (`:1154` / `:149`); task_group 形态三份各异 (不动)。

**已核实无问题的面** (R2 不复审): 三份 DAG 无环无悬空、parent 1:1、两解析器均接受、全 pending; 语义接缝 (E0–E6 ↔ 探针四态 ↔ `--emit-arg` ↔ 依赖方向) 三份互相咬合; 跨 skill import 顺序与同名包陷阱处置正确; 母 TASK-001 五条前置命令亲跑全真; 214 处行号锚点 210 命中; 零命中被否决方案; 「待 owner」项无 AI 自行拍板。

## 主控观察 (给 handoff / memory)

- R1 抓到的全是 **派生层** 缺陷 (memory `postplan-blindspot` 再实证): 三个执笔席各自的 tasks.md 都**写对了**顺序 (「同文件串行」「RED-first」「B.1 前置」), 但没有一个把它编码进 `dependencies` —— 「声称 ≠ 字段」形状与 pre-merge-gate R1 完全同款。
- 发布同步面漏项是 memory `scoped-add-splits-claim` 的规划期版本: 两个执笔席各自从记忆写清单, 只有字段席对照了上次发布 commit (`086ee32`) 的 14 处版本点。
- 4-tuple id 在本轮出现 5 组跨席同 id 不同内容 (同文件·同类·同级·同 type), 聚合按内容分簇; 收敛判定仍按键集。

## 下一步

按清账方案 (见下方附录, 已归档) 三席定点修 → 程序化验 C1/C10 → R2 五席复审 (镜头: C1 边集实证 / C2 清单逐字 / 本轮 fix 引入的新表面)。

---

## 附录: R1 清账方案 (主控 2026-08-30, 原 scratchpad/r1_fix_plan.md 全文归档)

### post_planning R1 清账方案 (主控 2026-08-30) — 三份同族 Spec 统一裁量

> 五席报告: `.aria/audit-reports/post_planning-R1-1788102593777-a1-entry-combined-A{1..5}-*.md`。
> 下列裁量是**主控执行细节裁量** (不触及 owner 权限面); 涉及 owner 的项 (版本档) 只做「统一留痕」不拍板。
> 修法 = 定点编辑 (不重写文件, memory `rewrite-discards-fixes`); 每改一处对照 R1 finding 的 file:line。

### C1 依赖图 (A2 ×3 critical · A3 bd55ab9c critical + c23f47ce/98e71a6a/3221f943 major · A4 bd55ab9c critical · A1 35dad35d major)

统一规则 (三份同施):
1. **同文件串行**: 凡两个任务的 deliverables 含同一路径 (现存或新建), 后者 `dependencies` 必含前者 (按 tasks.md 顺序链式); `execution_order` / notes 里的「并行 / parallelizable」字样对同文件任务全部删除, 改「串行 (同文件)」。多条 RED 测试写同一新建测试文件 ⇒ 链式 (T1→T2→…), 不合并任务。
2. **RED 先于 GREEN**: 测试/结构断言任务不得依赖其要断言的实现/文本任务; 方向 = 实现/文本任务依赖其 RED。母 Spec 第 6 组 (TASK-025~030) ⇒ 翻转六条边: 第 5 组文本任务 (TASK-017~023) 各自 `dependencies` 加对应第 6 组任务, 第 6 组不再依赖第 5 组; 第 5 组各 `verification[0]`「TASK-02x 绿」改为「本任务落文本后, 对应 TASK-02x 由红转绿 (基线 d69091d 上先红, 见该任务)」; tasks.md 组序自述「5→6」改「6 (RED) → 5 (GREEN)」并重排 tasks.md 段落顺序? **不重排编号** (编号不可变), 只改自述文字与 yaml 边。
3. **前置断言在上游**: 母 TASK-001 (--no-push 双远端) 与 TASK-002 (advisory) → 第 2 组全部 RED 任务的 `dependencies` 加 TASK-001 (TASK-002 advisory 不作边, 但 TASK-017/018 加 TASK-002 边以便记录 live 分支); 母 TASK-003 (锚点核对) → 第 3/4/5 组首任务加边。探针 TASK-001 (姊妹硬前置) 与 TASK-003 (套件建成, proposal :473 B.1 前置) → 第 2 组 (RED) 全部加 TASK-001 边, 第 4 组接线 + 第 5 组 AB 加 TASK-003 边; 删 `metadata.phase_b1_preconditions` 里「仅散文」的说法 (保留字段, 但每条指向真实上游边)。字段 TASK-007 加 TASK-006 边 (verification 已引矩阵)。字段 TASK-016/017 (同写 spec-drafter.json) 串行。
4. 改完程序化验: 同文件对全部有边; 无环; 每个 RED 任务不依赖其 GREEN。把脚本贴进各自 tasks.md「机械核验」段 (或 metadata `dependency_invariants_checked`)。

### C2 发布同步面 (A1 a257ffa4 critical 探针 TASK-018 · A1 73809784 / A4 518a7d7f critical 母 TASK-038)

统一清单 (以字段 TASK-024 的列法为准, A4 判其正确; 三份逐字对齐):
- aria 子模块 5 文件: `aria/.claude-plugin/plugin.json` (版本 SOT) / `aria/.claude-plugin/marketplace.json` / `aria/VERSION` / `aria/CHANGELOG.md` / `aria/README.md`
- 主仓: gitlink `aria` (bump 到子模块 post-merge master SHA) / `VERSION` / `README.md` badge / `CLAUDE.md` 项目状态版本行 / `README.zh.md` `README.ja.md` `README.ko.md` 顶部 `<!-- translated-from: vX.Y.Z -->` 标记 (B 档: 仅正文实质变更才重译, 否则只更标记; check `i18n-readme-translation-currency` 读的是标记, 不是「有无正文变更」)
- 机械兜底 verification: `m6-version-badge-match` 与 `i18n-readme-translation-currency` 两条 check 绿 (在完成上述**全部**文件后才断言)
- 删除 `README.zh-CN.md` / `.gitmodules 承载 gitlink` 等不存在的路径或错误描述。

### C3 版本档 (A1 3221f943 major · A5 af9f0c47 minor)

三份统一: 版本字面量一律写占位 `<vNEXT>` (**不写 v1.68.0 / v1.67.3**), notes 统一一句: 「档位 (MINOR/PATCH) 与号由 owner 裁; 三份串行 ship 各占一号 (字段 → 探针 → 母); 若 owner 裁合并一版, 由最后 ship 的母 Spec 发布任务承接, 前两份的发布任务改为 no-op 并留痕。未裁 ⇒ 本任务不开工 (status 仍 `pending`, 不用 `blocked`)」。母 TASK-031~035 五处 ab-results 目录字面量改为 `ab-results/<suite>/<vNEXT>-…` 占位。

### C4 字段对 audit-engine 目录断言过严 (A1 c23f47ce major)

字段 yaml `:268` / `:526` 的「`ls audit-engine/` 只有 references/+SKILL.md」改为 proposal :278 逐字: 「`audit-engine/` 下**不存在**名为 `lib/` 或 `collectors/` 的顶层目录」(探针 Spec 会新建 `scripts/` + `tests/`, 合法)。

### C5 ab-suite 口径 (A1 6698004d / 35dad35d major)

- `ab-suite/version.yaml` 计数: 三份的 AB 任务凡新增 eval/套件, deliverables 加 `aria-plugin-benchmarks/ab-suite/version.yaml`, verification 写「按实际文件**程序化重算** (`ls ab-suite/*.json | wc -l`; evals 数用 python 遍历各 json 的 evals 长度) 后更新, 不写字面量」; 删除 "29/58" / "31/73" / "2 evals" 等字面计数 (改「当前值 + 新增数」)。
- `spec-drafter.json` eval id 分配约定 (三份同写): 「新 eval id = 该文件当前 max(id)+1, ship 时读取, 不硬编码; 字段 Spec 先 ship 取到 3, 母 Spec 后 ship 顺延」; 字段 TASK-016/017 串行 (C1)。

### C6 母 TASK-018 「不相邻」在字段未 ship 分支不可求值 (A1 05b5c605 major)

母 TASK-018 verification 改两分支: 字段 hunk A/B 已 ship ⇒ 断言不相邻 (`git merge-tree` 干跑无冲突); 未 ship ⇒ 记「相邻性由字段 Spec TASK-014 对称分支在其 ship 时验」, 本任务不断言。

### C7 placeholder 黑名单义务 (A1 96ecdeb4 major)

字段 Spec 写占位串 `{<org>/<repo>#<n>}` 的两个写入宿主任务 (模板 + spec-drafter hunk A, 即 TASK-013/014 一类) verification 各加一条: 「占位串逐字节 = 探针 Spec SC-19 黑名单字面 (`grep` 探针 proposal SC-19 行取值), 改动须同批改两 Spec」。

### C8 探针 metadata 断言不可复现 (A2 f3265bfe major)

`metadata.line_anchor_recheck` 中「陈旧 `probe` 引用」「`refs/aria/` 现存 3 条」两条: 改为「A.2 席 2026-08-30 观测; R1/A2 复测零命中 ⇒ 非断言, 仅历史观测」, 或直接删除。不保留任何当前不可复现的「实况」措辞。

### C9 Schema 字段 (A4 df090b25 major)

字段 + 探针 yaml: `est_hours: <int>` → `estimated_hours: "<a>-<b>"` (S "1-2" / M "3-5" / L "6-8", 与 DUAL_LAYER_SPEC 与母 Spec 一致); metadata 加 `estimated_hours: "<sum-sum>"`; 字段 TASK-020 补 `reason`。

### C10 母 tasks.md SC 覆盖表不真 (A4 fead49d5 major · A3 b0e8b171 minor)

对覆盖表 17 对 (SC, TASK) 逐对: 在该 TASK 的 `verification` 里加引 `SC-NN` 的断言句 (不是只改表); SC-3 进 TASK-004 verification。程序化验「表中每对 (SC, TASK) ⇒ TASK.verification 含该 SC token」后贴结果。rule6_note「12-hunk 表」: 在 tasks.md 明列 12 hunk 或改口径为实际条数。

### C11 (已闭合) 三份 proposal 尾句陈旧 (A5 ×3 major) — 主控已改 :798 / :616 / :578。

### Minors (顺手, 不新增表面)
- 探针 TASK-010「恰三条 import」→「§3 代码块三条 import 逐字存在; 同块允许追加第四符号 `is_sentinel` (a2_discretions (i)), 断言用『包含』非『恰等』」。
- 母 yaml 锚点 `phase1_gate.py :1155-1158` → `:1154`; `branch-manager/SKILL.md :148` → `:149` (A4 实读)。
- task_group 形态: 不动 (体例 minor, 三份内部各自一致即可)。

### 不做
- 不重跑语义接缝面 (A1 判三份互相咬合)。不动 proposal (除已闭合的 C11)。不改编号。不 commit。


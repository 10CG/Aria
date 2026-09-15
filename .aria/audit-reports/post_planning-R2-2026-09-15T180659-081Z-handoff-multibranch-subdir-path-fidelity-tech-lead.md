---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-15T18:41:43.378Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/detailed-tasks.yaml
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R2 — tech-lead 席 — handoff-multibranch-subdir-path-fidelity (10CG/Aria#195, A.2/A.3 v2 `0f50239`)

## 审计结论

### 实读范围

- **审计对象 (全文)**: `tasks.md` (145 行)、`detailed-tasks.yaml` (783 行)、`sc11-predicate-validation.py` (123 行)。
- **v1 → v2 差异**: `git diff 07e0a6e 0f50239 -- openspec/changes/handoff-multibranch-subdir-path-fidelity/` 全文 (3 files, 454+ / 209-)。
- **R1 报告**: 聚合报告全文; tech-lead / code-reviewer / qa-engineer 三份席位报告全文。
- **裁定**: 决策单 `2026-09-12-…-technical-rulings.md` 全文 (116 行, 含 §2 的 10CG/Aria#195 表与 §5); `standards/conventions/configured-gate-authority.md` §5 (:107-116)。
- **proposal (按行切片)**: `:9` 分支起点; `:12` Rule #6 判定; `:415-433` SC 表, 用 python 抽出 SC-1/3/4/5/8/14/17 的反事实原句; `:425` SC-11 单元格; `:456-469` rule6_note。
- **AB 依据**:
  - `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` :198-230 / :360-376 / :472-486 / :538-566
  - `ab-results/2026-09-05-v1.70.0-a1-entry-rule6/{RESULT.md :1-40, :98-108; SCORES.md :25-60}`
  - `ab-results/2026-09-08-v1.73.0-archive-skill-drift/RESULT.md :1-45`
- **归档与收尾**:
  - `aria/skills/openspec-archive/SKILL.md` :98-140 / :282-371
  - `aria/skills/phase-d-closer/SKILL.md` 结构 grep 与 :65
  - `aria/skills/state-scanner/scripts/lib/spec_complete.py` :186-430 / :775-810 / :1125-1340 / :1453-1500 / :1565-1823
- **其它**:
  - `.aria/config.json` audit / benchmarks 段
  - `aria/skills/task-planner/DUAL_LAYER_SPEC.md` 的 agent 字段
  - 先例 `openspec/archive/2026-09-06-owner-container-identity-key-and-collision-parser/detailed-tasks.yaml` TASK-034 / 036
  - `tests/test_handoff_multibranch_collision_dedupe.py` :878-890 / :1156-1168
  - memory `ab-input-baseline` / `ab-baseline-leaks-via-repo-corpus` / `same-value-merge-silent` 三份原文

### 实跑命令与关键输出

全部只读。临时件放 scratchpad, 用完已删; Python 一律用 `python3 -B`。

1. **yaml 结构与依赖图** (`yaml.safe_load` 后自写脚本):
   - 结构: 34 任务 / 100h / qa 14 · backend 10 · knowledge 10, 均与 metadata 一致; 无悬空依赖, 无环; 26 个 parent 与 tasks.md 的 26 个 checkbox 一一对应。
   - 拓扑波次 (节选): `wave 8 ['TASK-011', 'TASK-013']` · `wave 9 ['TASK-012', 'TASK-023']` · `wave 10 ['TASK-014']` · `wave 11 ['TASK-019', 'TASK-020', 'TASK-033']` · `wave 15 ['TASK-022', 'TASK-025']` · `wave 16 ['TASK-026']` · `wave 17 ['TASK-027']` … `wave 23 ['TASK-032']`。
   - 关系判定: `TASK-033 || TASK-019 (parallel)` · `TASK-033 || TASK-020 (parallel)` · `TASK-033 || TASK-023 (parallel)` · `TASK-023 anc of TASK-025` · `TASK-025 || TASK-026 (parallel)`。
2. **验证脚本**: `python3 -B openspec/changes/…/sc11-predicate-validation.py` 输出的五态矩阵与 yaml:89-108 逐格一致, `exit=0`, 临时目录已自删。另用 AST 抽出脚本的 `PRED` 与 yaml 的 19 条谓词做逐字比对: `19 19`, 无差异。
3. **归档门预演**: 复制 v2 change 目录到 scratchpad, 26 个 checkbox 全部置为 `[x]`, `_find_project_root` 指向 `/home/dev/Aria`, 调 `gate_result`。输出 `complete True | verdict warn | blocking []`, unverified_claims 三条:
   - 2.2 行 ⇒ `symbol 'HEALTHY_TRACKS' unclassified reference form`
   - 4.4 行 ⇒ `no extractable symbol (fail-soft)`
   - 4.3 行 ⇒ `dogfood/benchmark/deploy claim 无可链接产物路径或路径不存在`
   - `d_payload is None: False`
4. **5.5 行产物抽验** (`classify_artifact_claim`):
   - 原样 ⇒ `verified: True (linked artifact exists: aria-plugin-benchmarks/ab-results/)`
   - 保留泛父目录、追加一个不存在的具体目录 ⇒ 仍 `verified: True`
   - 用该不存在目录替换泛父目录 ⇒ `verified: False`
5. **合并树演示** (scratchpad 临时仓): feature 分支提交代码, 文档改动留在工作树, `checkout master` + `merge --no-ff feature`。结果:
   - 工作树谓词 `grep -q rel_path schema.md` ⇒ `PASS`
   - `git show HEAD:schema.md` ⇒ `doc: four-level key`
   - `git status` ⇒ ` M schema.md`
6. **(j4) 同义词演示**: collector 写「the sort key is 4-level」、schema 写「the **4-level** compound key」, 跑 (j4) 原文 ⇒ `j4 PASS on stale 4-level text`。
7. **主仓远端**:
   - `git ls-remote origin refs/heads/master` 与 `git ls-remote github refs/heads/master` 均为 `36ea2884767a…`
   - `git rev-list --count origin/master..HEAD` = `2`
   - `git cat-file -e 36ea288:<change 目录>/<f>`: `proposal.md yes` · `tasks.md NO` · `detailed-tasks.yaml NO` · `sc11-predicate-validation.py NO`
8. **aria 远端 tag**: `git -C aria ls-remote --tags origin` 与 `… github` 均含 `v1.73.2` / `v1.73.3`; 本地 `git -C aria tag` 只到 `v1.73.1`。主仓 `36ea288` 的提交信息为「合表并发容器 13 个 commit (v1.73.2 / v1.73.3 发版 …)」。
9. **协调 ref**:
   - `git ls-remote origin refs/aria/coordination` 与本地 `rev-parse` 均为 `4fd07f9`
   - `claims/023236f2/s-13ce@1833.yaml`: `status: active` / `phase: A.2` / `heartbeat_at: '2026-09-15T13:04:15Z'` —— 清单第 1 条属实
10. **计划文本 grep**:
    - `grep -n '提交\|commit\|git add\|工作树干净\|git status' detailed-tasks.yaml` ⇒ 显式提交点只有 :264 / :395-408 / :578-579 / :662 / :693-700
    - `grep -n 'delta\|PREDICTION\|预测' tasks.md detailed-tasks.yaml` ⇒ 零命中
    - `grep -n '规划提交\|0f50239\|07e0a6e\|未推送\|推送规划' …` ⇒ 只命中 yaml:693-694 (子模块合并「未推送」)
11. **config**: `.aria/config.json` 的 `audit.checkpoints` 中只有 `post_spec` / `post_planning` 为 convergence, 其余全部 `off`, 计划无须为其它 checkpoint 排任务; `benchmarks.require_before_merge: true`。

### R1 处置落地核验 (本席侧重项)

| 处置 | 落地与否 | 证据 | 备注 |
|---|---|---|---|
| PP1-M3 反事实检出源 / 三步法 / 6 条基线即反事实 / SC-14 中间态 | 已落地 | tasks.md:91 (2.7)、:93 (组 3 标题)、:98; yaml:393-408 (TASK-033)、:119、:421-478 (TASK-015..018 均依赖 TASK-033 并写三步)、:262 (TASK-007)、:340 (TASK-011); 映射表 tasks.md:123-139 | 改法带出新缺陷: TASK-033 时点与依赖图矛盾 (M1);「一律三步」与另两类证据形态冲突 (m8) |
| PP1-M4 回归与 AB 的验证对象 | 已落地 | yaml:531 (TASK-021 依赖含 023/024)、:626 (TASK-026 依赖含 023)、:698 (TASK-029 合并树重跑) | 合并树回归的判定对象是工作树, 缺干净工作树断言 (M3) |
| PP1-M5 归档门预演 / Step 7 授权 / 不改写措辞 / 5.4 勾选时点 / 5.5 具体目录 | 基本落地 | yaml:113、:775-778; tasks.md:113-114 | 预演来源少一条 (m3); 5.5 的改法不足以恢复抽验 (m1);「不建」无执行路径 (m7); 5.6 缺同类勾选例外 (m2) |
| PP1-M7 AB 执行规格 | 文字已落地 | yaml:121、:628-639; tasks.md:114 | 通过判据欠定, 且替代了 SOT 场景 1 验收 (M4); 前置核验缺口 (m5) |
| PP1-M8 AI 流程判断清单 | 部分落地 | tasks.md:34-49; yaml:780 | 漏列 3 项 (M5)。聚合表所写「本 session 收尾 handoff 先写一次」不在计划文本中, 本会话尚未收尾, 本席无法核验, 不计 finding |
| PP1-M9 组 5 执行序 | 已落地且正确 | tasks.md:108; 实算 025 / 026 在波次 15 / 16, 均为 027 (波次 17) 的前置, 其后 028→029→034→030→031→032 严格串行 | — |
| m10 分支起点 | 已落地 | tasks.md:30; yaml:29 / :34 / :39 / :145 | 主仓一支与「规划提交未推送」的现状冲突 (M2) |
| m11 两次自检与 Phase D 双推核验 | 已落地 | tasks.md:115; yaml:665-681、:781-782 | 5.6 勾选时点 (m2) |
| m12 推送拆分 | 已落地 | yaml:683-700 (TASK-029 不推送)、:702-718 (TASK-034)、:728 (TASK-030 依赖 TASK-034) | 窗口拉长后未复核取号 (M6, 非 v2 引入) |
| 附: PP1-M12 台账唯一执笔 | 已落地 | yaml:21-24、:118; tasks.md:8 | 两处章节名不一致 (m10) |
| 附: PP1-M6 遗留 issue 第 (g) 条 | 已落地 | yaml:614-615; tasks.md:61-62、:112 | — |

### 实施者试派生

| TASK | 只看该任务与所引文件, 能否无歧义执行 | 卡点 |
|---|---|---|
| TASK-001 | 否 | 主仓分支起点上没有规划文件 (M2); 验证脚本的退出码与锚点断言 (m4) |
| TASK-033 | 否 | 「提交前改动面恰为组 2」与 TASK-019 / 020 / 023 的时点冲突 (M1) |
| TASK-026 | 否 | 通过判据两种读法, 两臂输入未定 (M4); NO_PUSH 未实测 (m5); 5.5 路径写法 (m1) |
| TASK-029 | 部分 | 合并树回归读的是工作树 (M3); 合并后未复核取号 (M6); standards 里的占位号 (m6) |
| TASK-032 | 部分 | 预演预期少一条 (m3); Step 7「不建」路径 (m7); 5.6 勾选与归档后台账路径 (m2); 清单漏项 (M5) |

### 核对无误的部分 (不计 finding)

- **计数与图**: 34 任务 / 100h / agent 分布、DAG 无环、26 个 parent 对 26 个 checkbox 均属实; 组 5 标题行与依赖一致。
- **SC-11 谓词**: 19 条与脚本逐字一致, 五态矩阵复现。
- **清单第 1 条**: claim 事实属实。
- **不可协商规则与多远程约束的承载**: Rule #8 (TASK-031 经 C.2.4)、Rule #9 (TASK-032 写 `docs/handoff/`)、多远程硬约束 1 (TASK-029 本地 merge) 与硬约束 2 (TASK-034 / 031 / 032 逐 remote ls-remote) 均有任务承载。
- **其它 checkpoint**: 均为 off, Rule #10 在这一层无缺口。
- **agent 字段**: TASK-029 / 034 标 `backend-architect`、notes 写「主控执行」, 与先例 TASK-034 / 036 同形, 不计。

---

### M1 [Major] type=issue · category=architecture · scope=TASK-033 / TASK-019 / TASK-020 / TASK-023 · v2 引入: 是

**证据**
- yaml:406 (TASK-033) 要求:「提交前 `git -C aria status` 的改动面恰为组 2 交付物 (handoff_multibranch.py / scan.py / latest_md_writer.py / test_scan_integration.py; …), 提交后工作树干净」。其依赖为 `[TASK-013, TASK-014]` (yaml:401)。
- 另有三个文档任务只依赖组 2, 却都改 aria 工作树:
  - TASK-023 依赖 `[TASK-013]` (yaml:567), 交付物含 `aria/skills/state-scanner/references/layer-l-integration.md` (yaml:570)。
  - TASK-019 / 020 依赖 `[TASK-012, TASK-013, TASK-014]` (yaml:491, :511)。其中 TASK-020 与实现改的是同一个 `handoff_multibranch.py` (yaml:513)。
- 依赖图实算 (命令 1): TASK-023 在波次 9, 比 TASK-033 (波次 11) 早两波; TASK-019 / 020 与 TASK-033 同在波次 11, 三者两两并行。
- tasks.md 的组序 (组 2 的 2.7 → 组 3 → 组 4) 暗示文档改动在收口提交之后, 但 yaml:9 规定「执行序以 dependencies 为准」。

**照计划执行会出的错**
- 按依赖图执行, TASK-033 的核验在自然顺序下无法满足: `git -C aria status` 会多出 `layer-l-integration.md` / `state-snapshot-schema.md` / `phase-1-collectors.md`, `handoff_multibranch.py` 里实现与 docstring 改动混在一起。
- 「提交后工作树干净」只有两种办法达成: 把文档一并提交 (「组 2 收口」名不副实), 或临时 stash (计划外处置, 也没有留痕)。
- 若并行派发 TASK-020 与 TASK-033, 提交可能落在半改状态的文件上。
- 这正是 PP1-M3 处置的前提 (yaml:400「反事实补丁必须打在已提交的实现上」) 所依赖的时点, 现在它的定义自相矛盾。

**建议改法**
- TASK-019 / TASK-020 / TASK-023 的 dependencies 补上 `TASK-033`。已核: TASK-033 只依赖 013 / 014, 不成环。
- TASK-033 核验改为「只 `git add` 四个文件; 提交后不带路径的 `git -C aria status --porcelain` 为空」。

### M2 [Major] type=issue · category=architecture · scope=tasks.md:30 (读前必看第 13 条) · yaml:39 / :145 (TASK-001) · v2 引入: 是

本席 R1 m9 建议把主仓并入同一口径, v2 照做了, 但没有处理「规划提交尚未推送」这一前提。

**证据**
- 计划文本:
  - tasks.md:30:「aria / standards / 主仓的 feature 分支一律从 **B.1 实测的 `origin/master`** 起」
  - yaml:39: 主仓 `branch_base: "B.1 实测 origin/master"`
  - yaml:145 与之同句
- 远端现状 (命令 7): 主仓 origin 与 github 的 master 都是 `36ea288`, 本地领先 2 个提交 (07e0a6e / 0f50239)。`36ea288` 上 `tasks.md` / `detailed-tasks.yaml` / `sc11-predicate-validation.py` 均不存在, 只有 `proposal.md`。
- 缺少推送步骤: 命令 10 的 grep 表明, 没有任何任务或前置条件在 B.1 之前推送规划提交。

**照计划执行会出的错**
- 若 B.1 时规划提交仍未推送 (即当前状态), 按第 13 条从 origin/master 起的主仓 feature 分支上, 没有 tasks.md、detailed-tasks.yaml、验证脚本。
- 而 TASK-001 要在该目录建台账骨架、跑 yaml 里的 19 条谓词, 后续还要逐项勾 tasks.md —— 依据文件都不在分支上。
- 执行者只能二选一:
  1. 改从本地 master 起分支: 违反第 13 条, 且属未记录的流程判断。
  2. 自行推送规划提交: 这是外向动作, yaml:113 要求逐项授权, 计划没有列这一项。

**建议改法**
- 第 13 条与 TASK-001 补前置条件:「B.1 之前, 规划提交 (含 post_planning 各轮报告) 经 owner 授权推送到主仓 origin 与 github, 并逐 remote ls-remote 核验; 若未推送, 主仓分支起点改为包含规划提交的本地 master, 并记台账」。
- 外向授权清单同步加上这一项。

### M3 [Major] type=issue · category=implementation · scope=TASK-019 / 020 / 023 (aria 侧) / 024 的提交点 · TASK-029 · TASK-031 · v2 引入: 部分

TASK-029 的合并树回归和 TASK-033 的提交点清单是 v2 新增; 文档任务没有提交点在 v1 就存在。

**证据**
- **提交点不全** (命令 10): 显式提交点只有以下几处:
  - RED 批次 (:264)
  - 组 2 收口 (:395-408)
  - standards (:578-579)
  - TASK-027「本任务的改动由主控提交」(:662)
  - 子模块合并 (:693-700)

  TASK-019 / 020 / 024, 以及 TASK-023 在 aria 侧对 `layer-l-integration.md` 的改动, 都没有提交点。TASK-030 / 031 的交付物 (:730-739, :755) 也不含主仓的台账和 `ab-results/` 目录。
- **合并前缺干净工作树断言**: TASK-029 (:697-699) 只断言「本地 master == origin/master」, 然后「对合并树重跑 run_tests / pytest / 全部谓词」, 没有要求 feature 分支工作树干净。谓词的 cwd 是工作树 (yaml:60)。
- **演示**: 命令 5 表明, 未提交的文档改动在 checkout + merge 后仍留在工作树, 谓词 PASS, 而合并提交里仍是旧文档。
- **先例**: memory `scoped-add-splits-claim` 记录了同形实证两次 (发布同步面漏 6 处; AB fixture 从未提交, 却有三处声称已做)。

**照计划执行会出的错**
1. TASK-027 按字面只提交版本 5 文件, 文档改动留在 aria 工作树。
2. TASK-029 切到 master 合并时, 这些改动被带过去, 两腿回归与 19 条谓词全绿。
3. TASK-034 推出去的 master 与 tag 不含文档同步, TASK-030 再把 gitlink 指向它 —— 发布的插件文档与代码不一致 (Rule #3)。
4. 后续没有任何一步能发现: TASK-031 的 `gitlink_integrity` 只核 SHA。
5. 主仓同理: `ab-results/` 若未提交, 归档门对 5.5 行只看磁盘上路径存在与否 (spec_complete.py:1170), 照样放行。

**建议改法**
- TASK-019 / 020 / 024 及 TASK-023 的 aria 侧, 各补「改动由主控在 aria feature 分支提交」。
- TASK-029 合并前补断言: `git -C aria status --porcelain` 与 `git -C standards status --porcelain` 均为空, 输出原样记台账。
- 合并树回归改到从合并 SHA `git worktree add` 出的副本上跑, 让判定对象是提交而不是工作树。
- TASK-031 开 PR 前补: 主仓 `git status --porcelain` 为空, 且 `git ls-files` 能列出本次 `ab-results/<目录>` 与台账。

### M4 [Major] type=issue · category=testing · scope=TASK-026 (yaml:634-636) · rule6_note (yaml:121) · tasks.md:114 · v2 引入: 是

**证据**
- **判据原文** (yaml:635):「通过判据: 无 WITHOUT_BETTER, 且 with_skill 在既有 eval 上不劣于上次存档结果; 回归臂无效度时按先例 …RESULT.md §1.2 写明证据来源与结论强度」。yaml:121 称依据是「AB_TEST_OPERATIONS.md 发版前清单」。
- **SOT 与取舍**:
  - 场景 1 的验收是 `AB_TEST_OPERATIONS.md:219`「验收: delta.pass_rate > 0」, 「Skill 优化后」清单 :542 同句。
  - 发版前清单 :553-556 共四项, 计划只取了 :555 / :556 两项。
  - 命令 10 中 `delta|PREDICTION|预测` 零命中: 计划对场景 1 验收既没采用, 也没声明不适用。
- **先例做法**: `2026-09-08-v1.73.0-archive-skill-drift/RESULT.md:39-41` 专设「与 SOT 验收判据的关系 (如实登记)」一节, 写「本次 delta = 0, 按该字面不达标」。本 spec 的 proposal:463 已预判套件「结构上测不到 collector 输出变化」, 所以 delta = 0 是可预期结果。
- **「上次存档结果」没钉目录**: 最近一次含 state-scanner 的存档是 `2026-09-05-v1.70.0-a1-entry-rule6`, 其 `SCORES.md:44` eval-6 with 2/6 · old 4/6, `:47` eval-9 with 6/7 · old 7/7; 该目录 `RESULT.md:20-22` 判定「回归臂机械分数 … 无效度, 不作任何结论依据」。
- **两臂输入欠定**: yaml:634「基线臂输入取旧代码 (B.1 基线) 的输出」只约束了基线臂。memory `ab-input-baseline` 原文分两种情况: 量文档增量时两臂同喂基线代码的输出; 量代码加文档整体时两臂各喂各版本的输出。计划没写 with 臂喂什么。

**照计划执行会出的错**
- 同一份 delta = 0 加一两分抖动的数据, 两名执行者会得出相反判决:
  - 执行者 A 读「回归臂无效度时写明来源」为可以通过: TASK-027 照常发版, RESULT.md 也不登记场景 1 验收未达标。
  - 执行者 B 读「不劣于上次存档」无法证明: 阻断并上报 owner。
- 这是 memory `spec-underdetermination` 的形状。
- 另外, 用发版前清单两项替代场景 1 验收, 本身是一个替代判断, 却不在 AI 流程判断清单里 (M5)。

**建议改法**
1. 开跑前写 PREDICTION.md, 对 `delta.pass_rate > 0` 给出预测与依据 (套件缺口), 结果如实登记。
2. 「不劣于」钉死三件事: 比较对象的目录路径、粒度 (汇总 pass_rate 还是逐 eval)、容差; 出现下降的 eval 按先例 eval-3 做复跑。
3. 明写「回归臂无效度 ⇒ 结论写『未被有效测试』, 不单独构成通过, 与 delta 未达标一并上报 owner」; 若取相反口径, 则列入 M5 的清单。
4. 两臂输入按 memory 二选一写死。

### M5 [Major] type=issue · category=architecture · scope=tasks.md:34-49 (AI 流程判断清单) · yaml:780 · v2 引入: 是

**证据**
- **规则要求**: `configured-gate-authority.md:109` 规定, AI「**任何**自作主张的流程判断 (跳过 / 降级 / 改序 / 替代)」都要写进 handoff 请 owner 复议。
- **清单是唯一入口**: tasks.md:36 声明清单收录「A.2 / A.3 与 post_planning R1 rework 中自行作出」的判断; yaml:780 要求周期 handoff「全文照录并追加 Phase B / C / D 新增项」。所以这一阶段漏列的判断, 以后没有入口再补进来。
- **已覆盖的**: 清单已收 PP1-M2 (第 12 条)、M3 (第 8 条)、M5 的不改写措辞 (第 11 条)、M6 (第 9 条)、M12 (第 10 条)。
- **漏列的** —— 同属 R1 rework 期间作出的判断:
  1. **分支起点**: tasks.md:30 第 13 条改为 B.1 实测 origin/master, 替代了已批准 proposal `:9`「Phase B 在 `f314785` 起分支」。同性质的「读前必看」第 6 / 7 / 10 / 11 条都进了清单, 这条没有。
  2. **AB 通过判据**: yaml:635 取发版前清单两项、不取场景 1 验收 (见 M4), 属替代。
  3. **5.4 提前勾选**: tasks.md:113 / yaml:778 让 5.4 在 release_gate、回帖、handoff 三个子步骤完成之前就勾选, 属改序。
  4. **(可选)** PP1-M9 是 R1 的 conflicted 项, 主控以「改标题消歧、不加依赖边」自行裁决 (R1 聚合 :61 / :90)。

**照计划执行会出的错**
- 周期 handoff 照录清单时, 以上三项不会出现在请 owner 复议的内容里。
- 其中第 2 项直接决定 Rule #6 是否放行发版, 第 3 项决定归档件里勾选状态是否属实。这些判断会以执行口径的名义悄悄沉淀下来。
- 定级沿用 R1 M8 的口径: 判断已公开写在计划里, 并经本闸门审阅, 故不定 Critical。

**建议改法**
- 清单补第 13–15 条, 每条写「做了什么 + 理由」。
- 若认为 PP1-M9 那项也算, 列为第 16 条。

### M6 [Major] type=risk · category=architecture · scope=TASK-029 (yaml:697-699) · TASK-034 (:716-717) · TASK-027 (:657) · v2 引入: 否

v1 已存在; v2 把合并与授权推送拆开后, 取号到推送之间的窗口变长。

**证据**
- **取号不复核**: 取号只在 TASK-027 做一次 (yaml:657)。TASK-029 合并前 fetch (:697) 之后不再复核; TASK-034 先推送, 再用 ls-remote 核对 tag (:716-717)。
- **并发发版是实情** (命令 8): 本轨 A.2 期间, 另一容器已发出 v1.73.2 / v1.73.3; 本地 aria 的 tag 已经陈旧。
- **已有同形事故**: memory `same-value-merge-silent` 记载, 2026-09-06 同族 spec 与同伴轨都定了 `1.70.0`, 合并时 `plugin.json` / `marketplace.json` ×2 / `VERSION` / `README.md` 四处零冲突, 静默带回一个已发布的号, 「差点被打成 tag」。

**照计划执行会出的错**

触发条件: TASK-027 取号之后、TASK-034 推送之前, 另一条轨先发出同一个 MINOR 号。

1. TASK-029 fetch 后合并, 版本文件静默采纳同值。
2. CHANGELOG 按内容解开冲突后, 留下两个同号小节; 合并树回归照样全绿。
3. TASK-034 推 master 成功, 推 tag 被拒, 到 ls-remote 才发现 —— 此时两个远端的 master 都已发布了重复的版本号, 只能事后修正。

**建议改法**
- TASK-029 补: fetch 后若 origin/master 已比取号时前进, 重跑 TASK-027 的取号计算。
- 合并后逐处复核版本 5 文件等于重算值, 且两个远端都没有 `v<vNEXT>` tag; 不符则回 TASK-027 重新取号, 禁止带同号合并。
- TASK-034 在推 master 之前, 先对两个远端 ls-remote 确认没有同名 tag。

### m1 [Minor] type=issue · category=testing · scope=tasks.md:114 (5.5) · yaml:639 · v2 引入: 是

**证据**: 命令 4 —— `_ARTIFACT_PATH_TOKEN_RE` (spec_complete.py:1140) 从行内抽出第一个在磁盘上存在的路径即判通过。只要泛父目录 `aria-plugin-benchmarks/ab-results/` 还留在行内, 追加一个不存在的具体目录仍是 `verified: True`。

**照计划执行会出的错**: 计划只写「勾选时本行写入具体目录」, 照字面追加即可, 抽验依旧恒过。R1 F-12 实际上没有修掉。

**建议改法**: 改为「勾选时把 `aria-plugin-benchmarks/ab-results/` **替换**为本次结果目录全路径, 行内不再保留泛父目录」。

### m2 [Minor] type=issue · category=architecture · scope=tasks.md:115 (5.6) · yaml:778 / :781 / :22 · v2 引入: 是

**证据**
- **第二次自检落在归档之后**: 5.6 改为分两次, 第二次放在 TASK-032 (yaml:781)。phase-d-closer SKILL.md:65 的顺序是 D.2 归档 → D.2b → D.3 handoff, 第二次自检自然落在归档之后。
- **5.6 没有勾选例外**: 归档门要求全部勾选 (spec_complete.py:273-276)。5.4 有「本行在归档前勾选」的例外 (tasks.md:113), 5.6 没有。
- **归档后台账路径**: 归档是 `git mv` 整个 change 目录 (openspec-archive SKILL.md:40), 但 TASK-032 仍要求把子步骤证据「记台账」(yaml:778), 而 metadata 里的台账路径 (yaml:22) 仍指向 `openspec/changes/`。

**照计划执行会出的错**
- 要么在第二次自检之前就把 5.6 勾上, 归档件里留下一个名不副实的勾; 要么不勾, 导致 `complete=False`, D.2 被跳过, 无法归档。
- 归档之后证据写到哪个路径, 执行者只能自己判断。

**建议改法**
- 5.6 行照 5.4 的写法, 补「第一次自检完成后勾选, 第二次的证据记台账」。
- TASK-032 写明归档后台账路径为 `openspec/archive/<date>-<id>/verification-ledger.md`, 并纳入 Phase D 提交。

### m3 [Minor] type=issue · category=documentation · scope=yaml:775-776 · tasks.md:48 (清单第 11 条) · v2 引入: 是

**证据**
- **实跑三条**: 命令 3 对 v2 文本预演出三条 unverified_claims, 来源分别是 2.2、4.4、4.3 行。
- **计划只写两条**: yaml:775 写「R1 审计席预演 … 来源为 4.3 行 … 与 4.4 行」; :776 与清单第 11 条也只说「两类」。
- **R1 原文就是三条**: R1 code-reviewer F-04 (报告 :94-97) 原本列的是三条; tech-lead M5 (:113) 也点到了 2.2。

**照计划执行会出的错**
- 预演结果与计划写的预期对不上。
- 「两类检查器假阳性另报」会漏掉第三类: 集成关键词行里只在测试文件中定义的反引号标识符。
- 请 owner 决定 Step 7 时, 给出的来源描述也不完整。

**建议改法**: 三处都改为三条、三类, 并注明「以 B.1 当时的预演结果为准」。

### m4 [Minor] type=issue · category=testing · scope=sc11-predicate-validation.py:24 / :122-123 · yaml:148 (TASK-001) · v2 引入: 是

**证据**
- **退出码只看三态**: 退出码只检查 base / target / bad_codeonly (:122)。yaml:87 给出的 bad_changelog_only 与 bad_partial 预期, 不参与退出码计算。
- **锚点不匹配直接中断**: `rep()` 找不到锚点时直接 `assert` 中断 (:24)。
- **TASK-001 未交代**: yaml:148 只写「先重跑 …, 三态不符同样先修谓词」, 没有提到退出码只覆盖三态, 也没有提到脚本会中断。

**照计划执行会出的错**
- B.1 基线若有漂移, 退出码仍可能为 0, 而 bad_partial 列已经不符预期。
- 锚点变化时脚本直接崩溃, TASK-001 没说要先重写模拟改动 —— 这句只写在脚本 docstring :14 里。

**建议改法**
- 退出码按 yaml:87 把五态预期逐格纳入。
- TASK-001 补一句「出现 AssertionError 表示锚点漂移, 先重写模拟改动, 再判谓词」。

### m5 [Minor] type=risk · category=testing · scope=TASK-026 (yaml:631-633) · v2 引入: 是

**证据**
- **第 1 步未实测变量**: 只要求 owner 带变量启动, 并核对本地与远端协调 ref 一致 (当前均为 `4fd07f9`)。先例 `v1.70.0 RESULT.md:102` 的做法是实测变量已生效 (「实测 SET … `no_push_requested_by_env() == True`」), 计划没有这一步。
- **第 2 步可能空真**: transcript 核验在零调用时恒成立。同一先例 :106 就是「66 个臂没有一个调用 phase1_gate」。
- 第 1 步两值不一致时如何处置, 计划也没写。

**照计划执行会出的错**: 若变量没带进会话, 恰有一个臂调用了 phase1_gate, 合成 claim 就已经推上了远端, 第 2 步只能事后发现 (即 2026-08-02 事故的形态)。

**建议改法**
- 第 1 步补: 在子进程实测 `no_push_requested_by_env()` 为真, 结果记台账。
- 第 2 步零调用时记「未触达」, 以远端前后比对兜底。
- 两值不一致时, 先在正常会话中对齐, 再开跑。

### m6 [Minor] type=issue · category=architecture · scope=TASK-023 (yaml:573 / :579) · TASK-025 (:609-611 / :616) · v2 引入: 是

**证据**
- **「若」恒成立**: 依赖图实算 `TASK-023 anc of TASK-025`, 因此 notes 里「若 TASK-025 尚未开单」恒成立。共享 standards SOT 中的「跟踪见 10CG/aria-plugin#<TASK-025 开出的号>」必然以占位形态, 经过 TASK-021 的回归和 TASK-026 的 AB。
- **回填无交付物与核验**: 回填由 TASK-025 的核验项 (:616) 承担, 但其交付物 (:609-611) 不含 `standards/conventions/session-handoff.md`, 也没有核验回填提交本身。

**照计划执行会出的错**: 回填容易漏掉; owner 若不授权开单, 占位号会随 TASK-029 进入 standards master。

**建议改法**
- 把「若」改为「必然」。
- TASK-025 的交付物补上该 standards 文件, 核验补「回填提交后 `grep -n '#<' conventions/session-handoff.md` 零命中」。
- TASK-029 合并前做同一项检查。

### m7 [Minor] type=risk · category=architecture · scope=TASK-032 (yaml:776) · v2 引入: 是

**证据**
- openspec-archive SKILL.md:293-296 规定, headless 默认下 Step 7「判定只看 d_payload 是否非 null」。
- :371 的 `d_issue_skip_reason` 取值只有 clean_archive / duplicate_found / non_forgejo_backend / api_failed / null, 没有「owner 裁定不建」这一支。

**照计划执行会出的错**: owner 裁「不建」时, 执行者只能在技能流程之外跳过 Step 7, 用什么方式跳、如何留痕都没有依据。

**建议改法**: TASK-032 写明「不建」的执行方式: D.2 之前先询问 owner; 若裁定不建, 执行完 Step 1-6 后停在 Step 7 之前, 在台账记录 owner 裁定原文与未建原因, 并写入周期 handoff。

### m8 [Minor] type=issue · category=testing · scope=yaml:119 vs :340 / :262 / :121 · v2 引入: 是

**证据**
- **硬约束写「一律」**: hard_constraints :119 写「反事实**一律**三步: 从 TASK-033 记录的实现 SHA 检出 …」。
- **两处处置不符合**:
  1. SC-14 在 TASK-011 完成、TASK-012 未做时的中间态实跑 (:340)。那时 TASK-033 还不存在, 兜底方案「在一次性副本上删去该键, 按三步法补跑」也没有 SHA 可检出。
  2. SC-1/3/4/5/8/17 由基线 RED 记录承担 (:262)。
- **rule6_note 仍计为有效**: rule6_note (:121) 把这两类都列为有效证据。

**照计划执行会出的错**: 严格照 :119 执行的人, 会判这 7 条反事实证据不合规 —— 要么补做计划外的工作, 要么认定 substitute 证据有缺口。

**建议改法**: :119 的作用域限定为「TASK-015..018, 以及 TASK-011 的兜底补跑 (于 TASK-033 之后执行)」; 另两类证据在同一条里点名说明不适用三步法。

### m9 [Minor] type=issue · category=testing · scope=yaml:78 (j4) · :109 (authoring_rules) · v2 引入: 是

**证据**
- **同义词绕过**: 命令 6 表明, 把现状描述写成「4-level」, (j4) 照样 PASS。同族测试文件已经在用「4-level」写法 (`tests/test_handoff_multibranch_collision_dedupe.py:885` / `:1162`)。
- **引导改写历史**: authoring_rules (:109) 要求历史叙述也不得出现「four-level」, 改称「round 3 键」。

**照计划执行会出的错**
- 现状句写成「4-level」「4 levels」或「四级」时, (j4) 为假绿。
- 同时引导作者为了过检查器, 去改写本来准确的历史措辞 (memory `author-to-match-checker`)。

**建议改法**
- 正则扩为 `four[- ]levels?|4[- ]levels?|四级`, 并只作用于现状段落; 或改成正向断言「键层级的现状句含 five / 5 级」。
- 删去 authoring_rules 中「历史叙述也不得出现」这一要求。

### m10 [Minor] type=issue · category=documentation · scope=tasks.md:8 vs yaml:24 · v2 引入: 是

**证据**
- tasks.md:8 列出的台账章节: 基线 / 前置核验 / RED / GREEN / 反事实 / 回归 / dogfood / 复核结论 / 写法自检。
- yaml:24 的 skeleton: 基线 / 前置核验 / RED / 组 2 收口 / GREEN 与反事实 / 回归 / dogfood / 复核结论 / AB / 写法自检 / 外向动作与授权, 并规定「不改标题」。

**照计划执行会出的错**: 若按 tasks.md 1.3 建骨架, 会少 3 个标题、多拆出 1 个, 与 yaml 各任务注释引用的章节名 (:404 / :611 / :714) 对不上。

**建议改法**: tasks.md:8 改为直接引用 yaml 的 skeleton, 不再另行列举。

## Verdict

**PASS_WITH_WARNINGS** —— 0 Critical / 6 Major / 10 Minor。

**R1 处置落地情况**: 本席侧重的 9 项全部有文字承载; PP1-M9、m12 落地正确, 其余 7 项的改法带出了新问题, 分三类:

1. **新增提交点的时点与依赖图对不上**
   - TASK-033 与文档任务同时就绪 (M1)。
   - 主仓分支起点上没有规划文件 (M2)。
   - 文档任务没有提交点, 合并树回归读的是工作树 (M3)。
2. **新写的判据不可判定或不完整**
   - AB 通过判据欠定, 且替代了 SOT 场景 1 验收 (M4)。
   - AI 流程判断清单漏列 3 项 v2 新判断 (M5)。
3. **v1 已有、v2 窗口拉长的风险**
   - 合并后不复核取号 (M6)。

6 条 Major 中 5 条由 v2 返工引入 (M3 部分引入), 1 条 (M6) 为 v1 已有。

## Vote

**REVISE**

## 轮次记录

Round 2 (tech-lead, convergence): REVISE — 0C/6M/10m (v2 引入 Major 5, 含 1 条部分引入); 要点: TASK-033 收口提交时点与 TASK-019/020/023 并行依赖矛盾 (M1), 主仓分支起点 origin/master 上无规划文件且无推送步骤 (M2), 文档任务无提交点且合并树回归读工作树可假绿 (M3), AB 通过判据欠定并替代场景 1 验收 (M4), AI 流程判断清单漏 3 项 (M5), 合并后未复核版本号 (M6, risk, 非 v2 引入)。

---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: false
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-15T19:55:59.100Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/detailed-tasks.yaml
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
counts_raw: 0C/12M/24m
counts_dedup: 0C/9M/17m
sibling_probe: no_sibling_found
---

# post_planning R2 聚合 — handoff-multibranch-subdir-path-fidelity (10CG/Aria#195, A.2/A.3 v2 `0f50239`)

> **对象**: tasks.md (26 项 checkbox) + detailed-tasks.yaml (34 TASK) + sc11-predicate-validation.py (v2 新增), 主仓 master `0f50239` (本地, 未推送)。
> **Sibling probe (本轮入口)**: 本轮已完整扫描, 未发现同 issue 竞品 (`status=ok`, origin 161 / github 155, 无 cap, 耗时 31s)。
> **drift-checker**: convergence 模式未 opt-in (`audit.drift_guard` 未配置) ⇒ 跳过, `drift_check_skipped: true`。
> **审计前后状态 (主控核验)**: 主仓 / aria / standards 的 HEAD 与 `refs/aria/coordination` 均未变; aria / standards 工作树干净; `.aria/audit-reports/` 由 857 份变为 862 份, 恰为本轮 5 份席位报告; 无其它新增或改动。
> **五席共识 (不计 finding)**:
> - 19 条谓词在基线上全假; 验证脚本输出的矩阵与 yaml 实测块逐格一致 (五席各自复现); 脚本 `PRED` 与 yaml 谓词逐字一致 (TL / CR 用 AST 比对)。
> - 34 任务 / 100h / qa 14 · backend 10 · knowledge 10; 依赖图无环、无悬空; 26 个 parent ↔ 26 个 checkbox。
> - 偏移表与 CHANGELOG 行号属实; 13 个 origin ref 子目录 0 / 引号 0 (QA 复跑); dedupe / track_board / p1_layer_h 共 52 条用例、pytest 28 + 11 条 (QA 复跑)。
> - R1 的 13 个 Major 簇文字全部落地。
>
> 问题集中在三处: **v2 新增文本的时点与依赖**、**验证器自身的覆盖面**、**新写判据的可判定性**。

## drift_metrics (Step 0 anchor 快照)

- checkpoint: post_planning
- primary_goal: 把 Approved 的 10CG/Aria#195 proposal (v7) 分解为可执行的 Level 3 双层任务 (tasks.md + detailed-tasks.yaml), 忠实落地决策单 2026-09-12 §2 的 10CG/Aria#195 表与 §5
- in_scope: 任务分解 / 依赖与执行序 / agent 分配 / 验收判据 / 裁定翻转的执行口径 / 基线复核记录
- out_of_scope_hints: proposal 设计取舍本身 (post_spec 已由 owner 裁定接受)
- source_sha: 0f50239
- drift_ratio: null (未 opt-in)

## 判定

| 席 | verdict | counts | vote | 一句话 |
|---|---|---|---|---|
| tech-lead | PASS_WITH_WARNINGS | 0C/6M/10m | REVISE | TASK-033 与文档任务无序; 主仓分支起点上没有规划文件; 文档任务无提交点, 合并树回归读的是工作树; AB 判据欠定且替代了场景 1 验收; AI 流程判断清单漏 3 项; 合并后不复核取号 |
| backend-architect | PASS_WITH_WARNINGS | 0C/1M/1m | REVISE | TASK-033 与同改 `handoff_multibranch.py` 的 TASK-019 / 020 无依赖边; docstring 行号区间少 1 行 |
| qa-engineer | PASS_WITH_WARNINGS | 0C/1M/2m | REVISE | 验证脚本退出码只核 5 态中的 3 态; (k) 关键词过窄可假红; `p1_docs` 模拟文本重复 |
| code-reviewer | PASS_WITH_WARNINGS | 0C/4M/9m | REVISE | (a2) 可被同行散文满足; 脚本退出码不核两列; TASK-033 无序; 基线 RED 不必然是反事实 |
| knowledge-manager | PASS | 0C/0M/2m | PASS | 「反事实一律三步」与 TASK-011 兜底冲突; TASK-026 / 032 的 deliverables 未列台账 |

**合并判定: PASS_WITH_WARNINGS (0 Critical / 9 Major 簇) · Vote REVISE 4 / PASS 1 · 未收敛 (R2)。**

## 收敛计算

- **结论集比较**: R2 的 9 个 Major 簇与 R1 的 13 簇没有一个 (category, scope) 相同 ⇒ `conclusions_stable = false`; 未全票 PASS ⇒ `converged = false`。振荡检测需至少 3 轮, 本轮不适用。
- **本轮修订引入的 Major 占比**:
  - 完全由 v2 返工引入: 7 簇 (PP2-M1 / M2 / M4 / M5 / M7 / M8 / M9)
  - 部分引入: 1 簇 (PP2-M3)
  - v1 已有: 1 簇 (PP2-M6)

  占比 7/9 (计入部分引入为 8/9), 超过 1/2 ⇒ 达到 R1 聚合报告自定的换执笔人条件 (memory `marginal-return-negative` / `fix-writer-bottleneck`)。code-reviewer 席报告也独立指出该条件已满足。

## Major 簇 (去重后 9) 与处置 (R3 rework)

> 执笔人按席位报告原文核对每条证据, 不以本表转述为准 (见文末「主控自查」)。

### PP2-M1 — TASK-033 收口提交与 TASK-019 / 020 / 023 无序

- **席位**: TL M1 · BA F1 · CR N-03
- **v2 引入**: 是
- **证据要点**: TASK-033 依赖 `[TASK-013, TASK-014]`, 核验「提交前改动面恰为组 2 交付物, 提交后工作树干净」。TASK-019 / 020 依赖 `[012, 013, 014]`, TASK-023 依赖 `[013]`; 传递闭包下三对都无序。其中 TASK-020 改的正是 TASK-033 要提交的 `handoff_multibranch.py`。yaml:9 声明执行序以依赖为准。
- **处置 (接受)**:
  1. TASK-019 / TASK-020 / TASK-023 的 dependencies 各补 `TASK-033` (TASK-024 已经经 TASK-017 排在其后)。补边后由主控复算无环。
  2. TASK-033 核验改为: 只对四个具体路径 `git -C aria add` (handoff_multibranch.py / scan.py / latest_md_writer.py / test_scan_integration.py); 提交后不带路径的 `git -C aria status --porcelain` 为空, 输出原样记台账。
  3. **跨簇连带 (主控)**: 补边后, 组 4 文档任务与组 3 (TASK-015..018) 同在 TASK-033 之后, 可能并发改 aria 工作树 ⇒ TASK-018「feature 分支工作树的 git status 在本任务前后一致」在并发下无法满足。改为副本生命周期证据:
     - 每条补丁 diff 以副本路径为根;
     - 副本的创建与移除 (`git -C aria worktree add` / `worktree remove`) 记台账;
     - 任务结束时 `git -C aria worktree list` 不含本任务副本。

     补丁泄漏到 feature 分支的兜底, 是 TASK-021 在最终树上的全量回归 (泄漏的补丁会让用例变红)。

### PP2-M2 — 主仓分支起点 origin/master 上没有规划文件

- **席位**: TL M2 · CR N-11 (Minor, 取最高 severity)
- **v2 引入**: 是
- **证据要点**:
  - origin 与 github 的 master 均为 `36ea288`, 本地领先 2 个提交。`36ea288` 上只有 `proposal.md`, 没有 tasks.md / yaml / 验证脚本。
  - 读前必看第 13 条与 yaml:39 / :145 要求主仓 feature 分支从 origin/master 起。
  - 全计划没有「B.1 前推送规划提交」的步骤, 而推共享 master 属外向动作。
  - TASK-001 取 SHA 前未要求 fetch。
- **处置 (接受)**:
  1. 读前必看第 13 条、`scope_repos` 主仓 `branch_base`、TASK-001 补 B.1 前置条件。前置内容: 规划提交 (A.2/A.3 各版与 post_planning 各轮报告) 已经 owner 授权推到主仓 origin 与 github, 并逐 remote `ls-remote` 核验。
  2. 若 B.1 时规划提交仍未推送, 主仓 feature 分支改从包含规划提交的本地 master 起:
     - 起点 SHA 与「未推送」事实记台账;
     - 列入 AI 流程判断清单 (PP2-M5);
     - 推送随 TASK-031 的 PR 发生, 列入外向授权清单。

     aria / standards 仍从实测 origin/master 起。
  3. TASK-001 取三处 origin/master 之前先 `git fetch` (或直接 `git ls-remote <remote> master`), 不读陈旧的远端跟踪 ref (memory `freshness-must-be-fetched`)。

### PP2-M3 — 文档任务无提交点; 合并树回归读的是工作树

- **席位**: TL M3
- **v2 引入**: 部分。合并树回归与 TASK-033 提交点为 v2 新增; 文档任务没有提交点是 v1 就有的。
- **证据要点**:
  - 显式提交点只有 RED 批次 / 组 2 收口 / standards / TASK-027 / 子模块合并。
  - TASK-029 合并前没有干净工作树断言, 而谓词的 cwd 是工作树。
  - TL 在临时仓演示: 未提交的文档改动随 checkout + merge 留在工作树, 谓词 PASS, 合并提交里却仍是旧文档。
- **处置 (接受)**:
  1. **aria 侧提交点**: TASK-019 / TASK-020 / TASK-023 (aria 侧 layer-l-integration.md) / TASK-024 (若落编辑) 各补一条: 改动由主控在 aria feature 分支提交, 只 add 本任务 deliverables, 提交 SHA 记台账。TASK-023 的 standards 侧已有独立提交点, 保留。
  2. **主仓侧提交点**: TASK-026 (结果目录) 与 TASK-030 (同步面) 同样写明由主控在主仓 feature 分支提交。
  3. **TASK-021 回归前**: aria 与 standards feature 分支的 `status --porcelain` 均为空, HEAD SHA 记台账 (该 SHA 同时是 PP2-M4 的 with 臂 SHA)。
  4. **TASK-029 合并前断言**: `git -C aria status --porcelain` 与 `git -C standards status --porcelain` 均为空, 输出原样记台账。
  5. **TASK-029 合并树回归**: 在「aria 工作树 `status --porcelain` 为空且 `rev-parse HEAD` == 合并 SHA」成立时原位跑 —— 工作树干净即等于提交内容; 前提不成立不得跑。**主控调整**: TL 建议在合并 SHA 的 `git worktree add` 副本上跑, 未采用。`run_tests.py` 会在所在仓跑 scan.py, 放到主仓之外的 aria 副本里, 依赖主仓布局的用例可能假红; 干净工作树断言达到同一目的。
  6. **TASK-031 开 PR 前**: 主仓 `git status --porcelain` 为空, 且 `git ls-files` 列出本次 `aria-plugin-benchmarks/ab-results/<目录>/` 与 `verification-ledger.md`。

### PP2-M4 — AB 通过判据欠定, 且替代了场景 1 验收

- **席位**: TL M4
- **v2 引入**: 是
- **证据要点**:
  - `AB_TEST_OPERATIONS.md:219` 场景 1 验收为 `delta.pass_rate > 0`; 计划既没采用, 也没声明不适用 (`delta|PREDICTION|预测` 零命中)。
  - 「上次存档结果」没钉目录。最近一次含 state-scanner 套件的存档是 `2026-09-05-v1.70.0-a1-entry-rule6`, 其 RESULT.md §1.2 与 SCORES.md 头部已判回归臂分数无效度 (主控复核: 其后 `2026-09-08-v1.73.0-archive-skill-drift` 不含 state-scanner 套件运行)。
  - 只约束了基线臂输入。
- **处置 (接受; 主控补一处执行细节)**:
  1. **预测**: 开跑前在结果目录写 `PREDICTION.md`, 先于任何臂运行。内容: 逐 eval 预测 with / old 分数与整体 `delta.pass_rate`, 并写依据 —— proposal rule6_note 已预判套件结构上测不到 collector 输出变化, 预期 delta ≈ 0。预测时刻记台账。
  2. **两臂口径**: 写死为「代码 + 文档整体」(memory `ab-input-baseline` 的第二种情况)。
     - with 臂 = TASK-021 回归前记录的 aria feature 分支 HEAD SHA 的 skill 目录及其代码;
     - old 臂 = B.1 基线 SHA 的一次性 worktree 的 skill 目录及其代码;
     - RESULT.md 标明整体口径, 区分力不归因到文档。

     **主控补充**: 本环境 `CLAUDE_PLUGIN_ROOT` 未设 (已实测), SKILL.md 中的 `${CLAUDE_PLUGIN_ROOT:-aria}` 在仓库根会解析为 feature 分支工作树。因此:
     - 臂提示须写明各自 SKILL.md 与 scan.py 的绝对路径;
     - 从 transcript 核对实际执行的 scan.py 路径;
     - 两臂跑到同一份代码, 即该 run 作废。
  3. **「无回归」怎么判**: 在本次运行内逐 eval 判 (with vs old, 同一 grader), 不与存档分数比。
     - 任一 eval 出现 with < old ⇒ 该 eval 复跑两次 (先例 eval-3 rep2 / rep3);
     - 三个样本中 ≥2 个仍是 with < old ⇒ 判回归 ⇒ 止损: 阻断 TASK-027 / TASK-029, 上报 owner;
     - WITHOUT_BETTER 同样触发止损。
  4. **与 SOT 验收判据的关系**: RESULT.md 设一节「与 SOT 验收判据的关系 (如实登记)」(先例 `2026-09-08-v1.73.0-archive-skill-drift/RESULT.md`), 登记 `delta.pass_rate > 0` 是否达成。
     - delta ≤ 0, 或回归面判为无效度 ⇒ 结论写「未被有效测试」, 不单独构成通过;
     - 在 TASK-027 之前经 AskUserQuestion 请 owner 裁, 附 PREDICTION 对照与套件缺口 issue, 裁定原文记台账;
     - AI 不自行判「按先例放行」。

     按预测, 这是一个**预期会触发**的 owner 等待点, 计划里须明写。
  5. **同步改写**: tasks.md 5.5 与 rule6_note, 删去「不劣于上次存档结果」。

### PP2-M5 — AI 流程判断清单漏项

- **席位**: TL M5 · CR N-12 (「5.4 提前勾选」未进清单的部分)
- **v2 引入**: 是
- **处置 (接受)**:
  1. 清单补以下各条, 每条写「做了什么 + 理由」:
     - **分支起点**: 改为 B.1 实测 origin/master (替代 proposal `:9` 的 `f314785`), 含 PP2-M2 的主仓回落支。
     - **AB 判据口径 (PP2-M4)**: 无回归在本次运行内逐 eval 判、不与存档比; 两臂整体口径 —— 替代 SOT 发版前清单「与上一次结果比对」的字面。
     - **勾选改序**: 5.4 在其子步骤 (release_gate / 回帖 / handoff) 完成前勾选; 5.6 在第一次自检后勾选 —— 均为满足归档门「全部勾选」。
     - **PP1-M9 conflicted 项**: 以「改标题消歧、不加依赖边」自行裁决。
     - **R2 两处 conflicted 的主控裁决**: 见下文 Conflicted。
  2. 已有条目改写:
     - 第 8 条按 PP2-M9 改写;
     - 第 11 条按 m4 改为三条 / 三类;
     - 第 12 条补 R3 的谓词改动 (a2 / j2 / j3 / j4 / k / l1);
     - 清单头部句「A.2 / A.3 与 post_planning R1 rework」改为含 R2 / R3 rework。

### PP2-M6 — 合并后不复核取号, 推送前不查远端同名 tag

- **席位**: TL M6
- **v2 引入**: 否。v1 已有; v2 把合并与推送拆开后, 取号到推送之间的窗口变长。
- **证据要点**:
  - 本轨 A.2 期间, 另一容器已发出 v1.73.2 / v1.73.3;
  - 本地 aria tag 只到 v1.73.1;
  - memory `same-value-merge-silent` 记有四处静默采纳同号的先例。
- **处置 (接受)**:
  1. TASK-027 记录取号时的 aria origin/master SHA。
  2. TASK-029 fetch 后, 若 aria origin/master 相对该 SHA 已前进, 重跑 TASK-027 的取号计算。
  3. TASK-029 合并后:
     - 逐处核版本 5 文件 == 重算值;
     - `git -C aria ls-remote --tags origin` 与 `github` 均无 `v<vNEXT>`;
     - 任一不符 ⇒ 回 TASK-027 重新取号, 禁止带同号合并;
     - tag 在合并树回归通过之后再打。
  4. TASK-034 推 master 之前, 先对两个远端 ls-remote 确认没有同名 tag。

### PP2-M7 — 验证脚本退出码只核 5 态中的 3 态

- **席位**: QA F1 · CR N-02 · TL m4 (Minor)
- **v2 引入**: 是
- **证据要点**:
  - `sc11-predicate-validation.py:122` 只核 base / target / bad_codeonly 三列。
  - CR 变异实验: 把 (a2) 换回 v1 的整文件形态, 两列与期望相反, 退出码仍为 0。
  - `shutil.rmtree` 不在 try/finally 中。
- **处置 (接受)**:
  1. 脚本内嵌完整期望矩阵 (全部状态 × 全部谓词), 任一格不符即 rc=1 并打印差异格。
  2. 临时目录清理放进 try/finally。
  3. docstring「三态验证」改为按状态逐一列举。
  4. 同批修 `p1_docs` 的重复片段 (m12)。
  5. TASK-001 验收改为:
     - 重跑脚本 rc=0, 且打印矩阵与 yaml `metadata.sc11_predicate_validation` 实测块逐字节一致;
     - 出现 AssertionError 表示锚点漂移 ⇒ 先重写模拟改动, 再判谓词。
  6. yaml 的 states / expected / 实测块一律由脚本输出重生成, 不手改 (memory `pasted-evidence-is-derived`)。

### PP2-M8 — (a2) 可被 Fail-soft 同行散文满足

- **席位**: CR N-01
- **v2 引入**: 是
- **证据要点**:
  - schema `:1138` 同一行既有形状 dict, 也有「Per-branch … failures are accumulated …」散文; TASK-019 要求补的「git show 失败不再产生 legacy 行」最自然就落在这句。
  - CR 副本 `bad_a2_prose_only` (形状 dict 未补、散文写入 unreadable_count) ⇒ 19 条全 PASS。
  - 脚本 bad_partial 对 (a2) 的模拟是整句不改, 不是这个真实坏形态 (memory `adversarial-fixture`)。
- **处置 (接受, 采用 CR 已三态实跑的形态)**:
  1. (a2) 改为定位到反引号内的形状 dict。schema 共有三行以 `**Fail-soft**` 开头 (`:134` / `:150` / `:1138`), 下式的前缀只命中 `:1138`:

     ```
     grep '^\*\*Fail-soft\*\*: branch-list' references/state-snapshot-schema.md | grep -oE '→ `\{[^`]*\}`' | grep -q '"unreadable_count": 0'
     ```

  2. 验证脚本加 `bad_a2_prose_only` 态 —— 在 target 基础上撤回形状 dict 的编辑, 同行散文写入 unreadable_count —— 期望 (a2) FAIL。
  3. TASK-019 核验同步写明: (a2) 检查的是形状 dict 本身。

### PP2-M9 — 「基线 RED 即反事实」的等价声明不无条件成立

- **席位**: CR N-04 (conflicted: QA 判等价成立, 见下文)
- **v2 引入**: 是
- **证据要点**:
  - 基线是**全部组件同时回退**; proposal 的反事实是在其余正确实现上**只回退一个组件**。
  - CR 在 1cb3872 上跑 SC-5 基线探针, 四项断言中第一项在基线上本就为真, 其余三项同时失败 (tracks 多 1 行 / legacy_count 1 / unreadable_count KeyError)。unittest 停在首个失败断言, 记下哪一个取决于书写顺序。
  - SC-4 后半同型。
- **处置 (接受 CR, 采用统一化改法)**:
  1. SC-1 / SC-3 / SC-4 后半 / SC-5 / SC-8 后半 / SC-17 / SC-14 的 proposal 反事实**全部**改在组 3 按三步法实跑:
     - 从 TASK-033 SHA 检出副本;
     - 未打补丁时对应用例绿;
     - 只回退该组件 (枚举退回 basename / 去掉 `-z` / 保留旧降级分支 / 早退 dict 删 `unreadable_count` …) 后红;
     - 记副本 SHA 与补丁 diff。

     同一补丁可同时作为多条 SC 的反事实, 但须逐 SC 记下失败断言文本, 证明它正是该反事实所指的断言。
  2. **落点由执笔人定**: 新增 tasks.md 3.5 与对应 TASK (编号取 TASK-035, 不复用旧号), 或并入 TASK-018 并按 4-8h 粒度拆分; 工时与 metadata 同步。
  3. **删除旧条目**: TASK-007 删去「本 RED 记录即该反事实的实跑」的标注 (RED 记录只作 RED 证据); TASK-011 删去 SC-14 中间态反事实条及其兜底。
  4. **同批同步**: rule6_note 证据来源段 / 清单第 8 条 / tasks.md 1.2 与 2.3 行 / SC 映射表中 SC-1 / 3 / 4 / 5 / 8 / 14 / 17 的「钉测 / 反事实」列 / hard_constraints「反事实一律三步」—— 此后该条对全部反事实成立, m8 一并闭合。
- **为什么统一改法**: 统一走三步法, 执行时不再需要判「RED 能不能充当反事实」; 「一律三步」的字面也随之成立, 跨簇闭合 m8。

## Minor (去重后 17) 与处置

| 编号 | 内容 | 席位 | 处置 |
|---|---|---|---|
| m1 | TASK-020 的 `_dedupe_sort_key` docstring 区间 `:429-452` 应为 `:429-453` | BA F2 | 接受 |
| m2 | 5.5 行按字面「写入具体目录」追加后, 行内仍留父目录 token `aria-plugin-benchmarks/ab-results/`, 归档门遇到第一个存在的路径即判通过 ⇒ 抽验恒过 | TL m1 · CR N-06 | 接受: 勾选时把行内父目录 token **整个替换**为具体结果目录全路径, 不残留 |
| m3 | 5.6 没有 5.4 那样的勾选例外; 归档 `git mv` 之后「记台账」的路径未定义 | TL m2 · CR N-12 | 接受: 5.6 行照 5.4 写「第一次自检完成后勾选, 第二次的证据记台账」; TASK-032 写明归档后台账路径为 `openspec/archive/<日期>-handoff-multibranch-subdir-path-fidelity/verification-ledger.md`, 并纳入 Phase D 提交 |
| m4 | 归档门预演实为三条 unverified_claims: 2.2 行 `HEALTHY_TRACKS` unclassified / 4.4 行 no extractable symbol / 4.3 行 dogfood 无产物路径; 计划只写两条 | TL m3 · CR N-05 | 接受: yaml:775-776 与清单第 11 条改为「三条 / 三类」, 注明以执行时的预演结果为准。**根因是主控 R1 聚合转述丢项** (见「主控自查」) |
| m5 | AB 第 1 步未实测变量生效; 第 2 步在零调用时空真; 本地与远端协调 ref 不一致时无处置 | TL m5 | 接受: 第 1 步在子进程实测 `no_push_requested_by_env()` 为真并记台账; 第 2 步零调用时记「未触达」, 以远端前后比对兜底; 开跑前两值不一致 ⇒ 先在正常会话对齐再开跑 |
| m6 | TASK-023 notes 的「若 TASK-025 尚未开单」按依赖图恒成立; 回填提交没有交付物与核验 | TL m6 | 接受: 「若」改「必然」; TASK-025 deliverables 补 `standards/conventions/session-handoff.md` (回填提交), 核验回填后 `grep -n '#<' conventions/session-handoff.md` 零命中; TASK-029 合并前同查; owner 不授权开单时的措辞回落形态写明 |
| m7 | owner 裁 Step 7「不建」时, openspec-archive 没有这一支 | TL m7 | 接受: D.2 前询问 owner; 裁不建 ⇒ 执行 Step 1-6 后停在 Step 7 之前, 台账与周期 handoff 记裁定原文与未建原因 |
| m8 | hard_constraints「反事实一律三步」与 TASK-011 兜底分支、基线 RED 两类证据冲突 | TL m8 · KM F1 · CR N-09 | 由 PP2-M9 闭合 (全部反事实进组 3, TASK-011 中间态条删除)。KM「写例外、检出源用当时工作树」的建议不采用 (见 Conflicted) |
| m9 | (j4) 可被 4-level / 四级 等同义词绕过; authoring_rules 引导作者改写准确的历史措辞 | TL m9 | **部分接受**, 分三块处置 (表后「m9 与 m14 处置细节」) |
| m10 | tasks.md:8 另列台账章节名, 与 yaml skeleton 不一致 | TL m10 | 接受: tasks.md:8 改为直接引用 yaml skeleton, 不另列 |
| m11 | (k) 接受三种写法; TASK-013 里的 `target_in_subdir` 容易被读成内部括注 | QA F2 | 接受并收紧: `target_in_subdir` 是 `degraded_reason` 的机读枚举值 (memory `machine-tokens-english`)。TASK-013 用反引号写明两处 docstring 须逐字含该值; (k) 收窄为只认该字面; authoring_rules 同步 |
| m12 | `p1_docs` 的模拟文本把 `content_lines` 重复插入 | QA F3 | 接受 (随 PP2-M7) |
| m13 | TASK-026 / TASK-032 的核验里有「记台账」, deliverables 却未列台账 | KM F2 | 接受 (TASK-032 用归档后路径, 见 m3) |
| m14 | (j2) / (j3) 的锚点词被语义正确的改写换掉即假红 | CR N-07 | 接受, 按「锚点词改后是否仍准确」分别处置 (表后「m9 与 m14 处置细节」) |
| m15 | (l1) 不覆盖 Scenarios 表的第四种结局; 读前必看未列 SC-11 判据替换 | CR N-08 | 接受: (l1) 追加一项 —— `write_latest_md` docstring 中 `Scenarios:` 之后的文本须含 `degraded_reason` 或 `target_in_subdir`; 脚本 target 补该编辑, 加 `bad_scenarios_missing` 态; 读前必看新增一行「SC-11 以 yaml 定位谓词为准」, 逐项写明与 proposal SC-11 原文的差异 ((a)(b)(i)(j)(k)(l)) |
| m16 | TASK-021 把子模块路径与主仓路径放进同一条 `git diff` (超级仓对子模块内部路径恒 0 行; 用 aria SHA 则 `bad revision`) | CR N-10 | 接受 (v1 原句, 非 v2 引入): 拆成 `git -C aria diff <aria B.1 基线> -- skills/state-scanner/tests/fixtures/handoff-tracks-frozen-2026-09-05.json` 与主仓 `git diff <主仓 B.1 基线> -- .aria/repro/handoff-tracks-frozen-2026-09-05.json`, 两个基线 SHA 取自 TASK-001 台账 |
| m17 | 写法自检覆盖缺口: PR 正文 / 主仓同步面文字 / RESULT.md / 套件缺口 issue 正文; 主仓 diff 基线未指明 | CR N-13 | 接受: TASK-031 开 PR 前对 PR 正文与主仓 PR diff 新增行自检 (覆盖 TASK-030 文字); TASK-026 对 RESULT.md 与 issue 正文自检; TASK-028 写明主仓 diff 基线 = TASK-001 记录的主仓起点 SHA |

### m9 与 m14 处置细节

**m9 — (j4) 同义词 (部分接受)**

1. **扩同义词**: 正则扩为 `four[- ]levels?|4[- ]levels?|四级|四层`。
2. **扩扫描面**: 加入 `tests/test_handoff_multibranch_collision_dedupe.py`。其 `:885` / `:1162` 两处现状句由 TASK-020 改 (仅 docstring, 断言不动); TASK-016「既有用例不变」注明指断言不变。执笔人先对整个 aria 做同义词 grep, 确定这一类的边界。
3. **不接受删除历史措辞约束**: 若按行排除历史标记 (如 `round 3`), collector `:368`「finalized (round 3): the sort key is FOUR levels」这种同行带轮次标记的现状句会被放过, 与 (j3) 合起来可以假绿。约束改写为正面写法: 历史轮次的键用元组表述。
4. **加验证态**: 脚本加 `bad_stale_synonym` (现状句写成 4-level) 与 `bad_stale_header` (只改 `:370` 元组, `:368` 仍写 FOUR levels) 两态, 期望 (j4) 均 FAIL。

**m14 — (j2) / (j3) 锚点**

- **(j2)**: 锚点词 `compound key` 改后仍准确 ⇒ 谓词不改, authoring_rules 补「schema 键序句保留 compound key 字样」。
- **(j3)**: 锚点词 `finalized` 在加第 5 级后不再准确 ⇒ 锚点改为 `sed -n '/^# Tie-break/,/^def _dedupe_sort_key/p'`。脚本加 `alt_j3_anchor` 态 (注释块首行改写为 round 4 措辞), 期望全 PASS。

## Conflicted

| 项 | 分歧 | 主控裁决 |
|---|---|---|
| 基线 RED 是否等价于 proposal 反事实 (PP2-M9) | QA 逐条对照 proposal 反事实句与基线状态, 判等价成立。CR 用基线探针实测 SC-5 有三个失败源、首个失败断言取决于书写顺序, 判不无条件成立 | **采 CR**。QA 比对的是「基线状态像不像反事实」, CR 比对的是「RED 记录能不能证明该断言的鉴别力」—— 后者才是 substitute 证据要回答的问题 (memory `test-claims-vs-verifies`), 且有实跑输出 |
| TASK-011 兜底反事实的检出源 (m8) | KM: hard_constraints 写例外, 检出源用 TASK-011 执行时的工作树或临时提交。TL / CR: 挂到 TASK-033 之后, 在其 SHA 上补跑 | **采 TL / CR**, 并由 PP2-M9 统一。工作树不可复现, 已提交 SHA 是唯一可复现的检出源 |

两项裁决均列入 AI 流程判断清单 (PP2-M5)。

## 跨簇一致性 (主控核对; 执笔人必须同批落)

1. **PP2-M1 补边 ⇒ 组 4 与组 3 可并发** ⇒ TASK-018 的工作树不变式改为副本生命周期证据 (已写入 PP2-M1 第 3 条)。
2. **PP2-M9 的同步面** ⇒ hard_constraints / rule6_note / 清单第 8 条 / SC 映射表 / TASK-007 / TASK-011 / tasks.md 1.2 与 2.3 行同批改; m8 随之闭合。
3. **PP2-M2 + PP2-M3 + PP2-M6 都改 TASK-001 / 021 / 029 / 031**。TASK-029 内部顺序须为:
   1. fetch;
   2. 断言本地 == origin;
   3. origin 前进则重算取号;
   4. 两子模块 `status --porcelain` 为空;
   5. 本地 merge;
   6. 核版本 5 文件 == 重算值, 且两个远端无同名 tag;
   7. 在干净工作树且 HEAD == 合并 SHA 的前提下, 跑回归与全部谓词;
   8. 通过后打 tag。
4. **PP2-M7 + PP2-M8 + m9 + m11 + m14 + m15 都改谓词或验证态** ⇒ 以下各项一次改齐:
   - yaml 谓词 / 脚本 `PRED` / authoring_rules;
   - states / expected / 实测块;
   - 归属注释 / 各 TASK 的「为真」声明。

   实测块由脚本输出重生成; 每条新谓词先在基线上跑三态 (memory `check-runs-at-baseline-first`)。
5. **owner 等待点须在外向授权清单与各任务里一致列出**: PP2-M4 的 AB 裁决点、PP2-M2 的规划提交推送、m7 的 Step 7「不建」。

## 席位准确性备注 (不计 finding)

- knowledge-manager 席写「25 个 checkbox 与 25 个 parent」, 实数为 26 / 26 (QA / TL / CR 三席与主控 `grep -c` 复核一致)。属该席计数错误, 不影响其结论。
- backend-architect 席「R1 处置全部正确落地」的范围以其表格所列 8 项为限, 未覆盖 PP1-M3 / M5 / M7 / M8。

## 主控自查

- **R1 聚合转述丢项**: code-reviewer 席 R1 F-04 列的是三条归档门 unverified_claims, R1 聚合转述成「检查器两类假阳性」, 漏了 2.2 行 `HEALTHY_TRACKS`。v2 照聚合表落文, 本轮被 TL / CR 两席独立抓到 (m4)。聚合是一次有损重写 (memory `rewrite-silently-discards`), 所以本报告每条处置都回链到席位报告编号, R3 执笔人以席位报告原文为准。
- **待办未消**: R1 聚合写了「本 session 收尾 handoff 先写一次」, 尚未执行 (会话未收尾); TL 席注明无法核验, 不计 finding。仍在待办。

## 收敛判断与 R3 安排

R2 不收敛 (9 Major, Vote REVISE 4)。本轮修订引入的 Major 占比 7/9, 超过 1/2 ⇒ **R3 换执笔人**:

- **执笔**: 新派的 aria:tech-lead 实例按本报告修订 tasks.md / detailed-tasks.yaml / sc11-predicate-validation.py。只改这三份文件, 不提交, 不派子代理。
- **主控**: 不代笔, 只做以下核验, 通过后提交, 再以新派五席进 R3:
  - 脚本实跑与矩阵逐字节比对;
  - 依赖图与计数复算;
  - v2→v3 逐任务 diff, 查有无漏项;
  - 处置落地对照表;
  - 跨簇一致性。
- **轮次**: max_rounds 5, 本轮为第 2 轮。

## 席位报告

同目录 `post_planning-R2-2026-09-15T180659-081Z-handoff-multibranch-subdir-path-fidelity-{tech-lead,backend-architect,qa-engineer,code-reviewer,knowledge-manager}.md`

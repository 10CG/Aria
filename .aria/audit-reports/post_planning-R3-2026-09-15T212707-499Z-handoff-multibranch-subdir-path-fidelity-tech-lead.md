---
checkpoint: post_planning
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-15T22:07:17.275Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/detailed-tasks.yaml
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---

# post_planning R3 — tech-lead 席 — handoff-multibranch-subdir-path-fidelity (10CG/Aria#195, A.2/A.3 v3.1 `2b9cb3e`)

## 审计结论

### 实读范围

- **审计对象 (全文)**: `tasks.md` (159 行)、`detailed-tasks.yaml` (867 行)、`sc11-predicate-validation.py` (340 行)。
- **v2 → v3.1**: `git diff --stat 0f50239 2b9cb3e`; 另把 `0f50239` 的 yaml / tasks.md 导出到 scratchpad, 定点比对 TASK-026 工时、TASK-029 / TASK-034 原文。
- **R2**: 聚合报告全文 (334 行); tech-lead 席位报告全文 (409 行)。
- **上游**: 决策单 `2026-09-12-…-technical-rulings.md` 全文 (116 行); `proposal.md` 切片 —— `:9`、SC 表 `:415` / `:417` / `:418` / `:419` / `:422` / `:429` / `:432` 的反事实句 (python 按单元格抽取)、Task 5.1–5.4a `:386` / `:403-407`。
- **规则**: `standards/conventions/configured-gate-authority.md` §5 (`:107-117`)。
- **AB 依据**:
  - `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` `:195-300` / `:320-400` / `:530-570`
  - `ab-results/2026-09-05-v1.70.0-a1-entry-rule6/` 的 `RESULT.md :1-60`、`SCORES.md` 全文、`state-scanner/runs/` 目录结构
  - `ab-results/2026-09-08-v1.73.0-archive-skill-drift/RESULT.md :1-50`
  - skill-creator 插件 (缓存 `3160b166dcef`) 的 `SKILL.md :170-240` 与 `scripts/aggregate_benchmark.py :60-225 / :380-420`
- **流程工具源码**:
  - `aria/skills/state-scanner/scripts/lib/spec_complete.py` `:126-170` / `:775-800` / `:860-910` / `:1757-1823`
  - `aria/skills/state-scanner/scripts/release_gate.py :1-120`、`aria/skills/state-scanner/lib/claim_lifecycle.py :378-440`、`aria/skills/state-scanner/scripts/phase1_gate.py :1-60`
  - `aria/skills/phase-c-integrator/SKILL.md :180-260 / :600-660`、`aria/skills/branch-manager/SKILL.md :490-560`、`aria/skills/phase-d-closer/SKILL.md :40-130`、`aria/skills/openspec-archive/SKILL.md` 步骤结构
- **仓状态**: 三仓 remote 列表; `aria/.gitignore`; aria tag 类型与远端 tag; `.aria/config.json` 的 audit / benchmarks / phase_c_integrator 键; `.aria/state-checks.yaml` 的 check 名; 主仓 16 个版本点 grep; 主仓 `git log --merges`。

### 实跑命令与关键输出

全部只读; 临时件只放 `scratchpad/r3-tech-lead/`, 已删; python 一律 `python3 -B`; 验证脚本以 `TMPDIR=<scratchpad>` 运行, 未在系统临时目录留件。

1. **依赖图与计数** (`yaml.safe_load` 后自写脚本):
   - `tasks 35 / hours 105.0 / agents qa-engineer 15 · knowledge-manager 10 · backend-architect 10`, 与 metadata 一致; `dangling []`; 无环。
   - `checkboxes 27 parents 27`, 双向无差集。
   - 波次节选: `wave 10 ['TASK-014']` · `wave 11 ['TASK-033']` · `wave 12 ['TASK-015', 'TASK-016', 'TASK-017', 'TASK-018', 'TASK-019', 'TASK-020', 'TASK-023', 'TASK-035']` · `wave 13 ['TASK-024']` · `wave 14 ['TASK-021']` · `wave 15 ['TASK-022', 'TASK-025']` · `wave 16 ['TASK-026']` … `wave 23 ['TASK-032']`。
   - 关系: `TASK-033 anc of TASK-019 / TASK-020 / TASK-023 / TASK-024`; `TASK-035 || TASK-019 (parallel)`; `TASK-025 || TASK-026 (parallel)`; `TASK-017 anc of TASK-024`。
2. **SC-11 验证脚本**:
   - 默认模式 `exit=0`, stderr `verdict: OK (mismatch cells 0, stderr notes 0; 13 states x 19 predicates)`; stdout 与 yaml `measured_2026_09_15_at_1cb3872_v3_1` 块逐字节比对 `True 1692 1692`。
   - `--emit-json`: `states eq: True` / `expected eq: True` / `matrix eq: True`。
   - AST 抽 `PRED` 与 yaml 19 条谓词: `pred count 19 19 keys eq True diff []`。
3. **回归锁用例数**: `python3 -B -m unittest test_handoff_multibranch_collision_dedupe test_track_board_advisories` ⇒ `Ran 28 tests … OK` (23 + 5); `test_scan_integration` ⇒ `Ran 19 tests … OK`; 其后 `git -C aria status --porcelain` 0 行。
4. **归档门预演** (v3.1 change 目录复制到 scratchpad、27 行全部置 `[x]`、`_find_project_root` 指向 `/home/dev/Aria`、包上下文导入 `lib.spec_complete` 调 `gate_result`): `complete True | verdict warn | blocking []`; unverified_claims 三条, 分别来自 2.2 / 4.4 / 4.3 行; `d_payload is None: False`; `soft_errors []`。
5. **skill-creator 聚合脚本的 delta 符号** (scratchpad 合成 `eval-1-x/<config>/run-1/grading.json`, 以官方 `python3 -B -m scripts.aggregate_benchmark` 聚合):
   ```
   with_better_old config_order= ['old_skill', 'with_skill'] delta.pass_rate= -0.50
   equal_old config_order= ['old_skill', 'with_skill'] delta.pass_rate= +0.00
   old_better_old config_order= ['old_skill', 'with_skill'] delta.pass_rate= +0.50
   with_better_without config_order= ['with_skill', 'without_skill'] delta.pass_rate= +0.50
   new_better_old config_order= ['new_skill', 'old_skill'] delta.pass_rate= +0.50
   ```
   另 `grep -c 'verdict\|WITHOUT' aggregate_benchmark.py` = 0。
6. **TASK-029 第 2 → 4 → 5 步** (临时仓, 四态) —— 输出见 M2。
7. **TASK-029 第 3 步改号后第 5 步合并** (bare origin + 两克隆, 三态) —— 输出见 M3。
8. **TASK-034 推送竞态** (bare origin, 本地合并提交 + annotated tag, 另一克隆先推 master; 四种推送写法) —— 输出见 M4。
9. **TASK-031 有范围核验** (临时仓, 三态) —— 输出见 M1。
10. **流程工具核对**:
    - `spec_complete.py:1757-1813` 确有 `--gate <spec_dir>` 模式; 全文件唯一的 subprocess 是 `git grep` / `grep` (`:884-905`), 预演只读成立。
    - `claim_lifecycle.py:386-405`: `release_claim_by_track` 按 `(track_id, container)` 定位, 「ALL matching active claims are released」, 与会话 id 无关。
    - `phase1_gate.py` 模块 docstring 第 9 步 `resilient_push`: B.0 认领同样推协调 ref。
    - `aria/.gitignore:3` `**/__pycache__/`; pytest 腿带 `-p no:cacheprovider`。
    - aria tag `v1.73.0` / `v1.73.1` 为 `tag` 对象, 远端 `v1.73.2` / `v1.73.3` 带 `^{}` 行。
    - `.aria/state-checks.yaml` 五个 check 名均在 (`:124` / `:177` / `:302` / `:325` / `:408`)。
    - 16 个版本点 grep 计数 16。
    - 主仓 `git log --merges`: 10CG/Aria#209、10CG/Aria#202、10CG/Aria#197、10CG/Aria#194 均为「Merge pull request …」merge commit。

### R2 处置落地核验 (本席侧重项)

| R2 处置 | 落地 | 证据 | 备注 |
|---|---|---|---|
| PP2-M1.1 TASK-019 / 020 / 023 补依赖 TASK-033 | 已落地 | yaml:537 / :558 / :619; 命令 1 复算无环 | — |
| PP2-M1.2 TASK-033 只 add 四路径, 提交后 porcelain 为空 | 已落地 | yaml:428 | — |
| PP2-M1.3 TASK-018 改副本生命周期证据 | 已落地 | yaml:501; hard_constraints yaml:123 | 该替代未进 AI 清单 (M6) |
| PP2-M2.1 主仓前置 = 规划提交经授权双推 + 逐 remote 核验 | 已落地 | tasks.md:30 / :93; yaml:42 / :164; owner_gates yaml:127 | — |
| PP2-M2.2 未推送回落支 | 已落地 | tasks.md:30 / :51; yaml:165 / :134 / :840 | 回落支遇 C.2.1 rebase 或 squash 的 SHA 可达性 (m5) |
| PP2-M2.3 取值前先 fetch | 已落地 | yaml:166 | — |
| PP2-M3.1 aria 侧提交点 | 已落地 | yaml:548 / :571 / :631 / :649 | TASK-027 同类提交点仍缺分支与 add 范围 (m6) |
| PP2-M3.2 主仓侧提交点 | 已落地 | yaml:705 / :822 | tasks.md 勾选没有提交点 (M1) |
| PP2-M3.3 TASK-021 回归前两子模块干净并记 HEAD | 已落地 | yaml:585 | — |
| PP2-M3.4 TASK-029 合并前干净断言 | 文字落地, 效果部分 | yaml:769 / :771 | 第 2 步先 checkout master, 第 4 步占位检查恒真, 脏树无处置 (M2) |
| PP2-M3.5 合并树回归原位跑 + 前提 | 已落地 | yaml:775 / :777 | 主控调整未进 AI 清单 (M6) |
| PP2-M3.6 TASK-031 开 PR 前主仓 porcelain 为空 + ls-files | 改写落地 (v3.1 收窄为有范围核验) | yaml:837 / :838 | 按计划自身勾选规则必然 FAIL (M1); 收窄未进 AI 清单 (M6) |
| PP2-M4.1 PREDICTION.md 先于任何臂 | 已落地 | yaml:693; tasks.md:128; rule6_note yaml:140 | — |
| PP2-M4.2 两臂整体口径 + 臂代码路径核验 | 已落地 | yaml:694 / :695 | — |
| PP2-M4.3 逐 eval 无回归 + 止损 | 已落地 | yaml:696 / :697 / :132 | WITHOUT_BETTER 无计算来源 (M5) |
| PP2-M4.4 SOT 验收如实登记 + owner 裁决点 | 已落地 | yaml:698 / :699 / :131 | delta 的取法与符号未钉 (M5) |
| PP2-M4.5 删「不劣于上次存档」 | 已落地 | `grep -n "上次存档\|不劣于"` 两文件零命中 | — |
| PP2-M5 清单补项与改写 | 已落地 | tasks.md:37 / :46 / :49-55 | v3 / v3.1 新判断漏列 (M6) |
| PP2-M6.1 取号时记 origin/master SHA | 已落地 | yaml:724 | — |
| PP2-M6.2 前进则重算取号 | 已落地 | yaml:770 | 改号支下合并必然冲突, 无处置 (M3) |
| PP2-M6.3 合并后核值 + 双远端无同名 tag + 回归后打 tag | 已落地 | yaml:773 / :774 / :776 | 回退前置与命令写死, 核对无误 |
| PP2-M6.4 推 master 前查同名 tag | 已落地 | yaml:793 | 推送形态与先后未定 (M4) |
| m2 5.5 父目录 token 整体替换 | 已落地 | yaml:704; tasks.md:128 | 勾选时点未定 (M1) |
| m3 5.6 勾选例外 + 归档后台账路径 | 已落地 | tasks.md:129; yaml:27 / :750 / :857 / :862 | 勾选无提交点 (M1) |
| m4 预演三条 unverified_claims | 已落地 | yaml:859; tasks.md:49 | 命令 4 对 v3.1 文本复跑一致 |
| m5 AB 场景 1 三步补强 | 已落地 | yaml:689-692 | — |
| m6 占位回填的交付物 / 核验 / 合并前复查 / 回落形态 | 前两项与回落落地, 合并前复查失效 | yaml:632 / :666 / :672 / :673 / :771 | M2 |
| m7 Step 7「不建」支 | 已落地 | yaml:860 / :135 | Step 7 为 openspec-archive 末步, 停在其前可行 |
| m13 TASK-026 / 032 deliverables 列台账 | 已落地 | yaml:687 / :857 | — |
| m16 冻结语料分仓 diff | 已落地 | yaml:590 | — |
| m17 写法自检覆盖面 | 已落地 | yaml:701 / :744-745 / :839 / :865 | — |
| 跨簇 3 TASK-029 八步序 | 已落地, 顺序与聚合报告一致 | yaml:767-776 | 该顺序本身带出 M2 |
| 跨簇 5 owner 等待点在清单与各任务一致 | 大部分落地 | yaml:125-139 对照各任务 | 缺项与处置缺失 (m1) |
| PP2-M7 脚本全矩阵 / 退出码 / finally | 已落地 | script:213-228 / :284-336 / :319-320; TASK-001 yaml:169 | 命令 2 复跑一致 |
| PP2-M9 反事实统一三步法 (TASK-035) | 已落地 | yaml:503-524 / :284 / :362 / :123; tasks.md:112 / :137-153 | 补丁 3「复用 TASK-017 副本」与并行冲突 (m3) |

### 实施者试派生

| TASK | 只看该任务与其所引文件, 能否无歧义执行 | 卡点 |
|---|---|---|
| TASK-001 | 基本可以 | 「先 fetch 或直接 ls-remote」: 只做 ls-remote 时对象可能不在本地, 建分支前仍须 fetch (措辞级, 不计 finding) |
| TASK-029 | 否 | 第 2 步先切 master, 第 4 步的占位检查恒真, 脏树无处置 (M2); 改号支必然合并冲突, 无解法 (M3); 第 3 步「在 feature 分支改号并提交」隐含先切回分支 |
| TASK-034 | 部分 | 推送形态与 master / tag 先后未定, non-fast-forward 与半推无处置 (M4); 未获授权时的状态保持未写 (m1) |
| TASK-031 | 否 | 有范围核验被 TASK-028 的 5.6 勾选必然触发 (M1); rebase / squash 未钉 (m5); 授权措辞缺「合并」(m1) |
| TASK-026 | 部分 | delta 的取法与符号 (M5); WITHOUT_BETTER 算法 (M5); AB 后重启会话不在 owner_gates (m1); 条件性扩面无拆分 (m2) |
| TASK-032 | 部分 | 预演前勾满 27 行的时点 (M1); 服务端合并后本地 master 同步 (m4); 释放 B.0 新写的 claim —— 已核源码, 可执行 |
| TASK-035 | 基本可以 | 补丁 3 复用 TASK-017 副本 (m3); 其余补丁与 proposal SC 表反事实句逐条对得上 |

### Findings

#### M1 [Major] type=issue · category=architecture · scope=TASK-028 (yaml:750) / TASK-031 (yaml:837) / TASK-026 (yaml:704) / TASK-032 (yaml:859, :866) · v3 引入: 是

**证据**

- yaml:750 (TASK-028):「本任务 (第一次自检) 完成后即勾选 tasks.md 5.6」; tasks.md:129 同句「本行在第一次自检完成后勾选」。
- 35 个 TASK 的 deliverables 都不含 tasks.md (`grep -n "tasks\.md" detailed-tasks.yaml` 的命中行均为注释、引用或核验文字, 无 deliverables 条目)。各提交点都是「只 add 本任务 deliverables」(yaml:548 / :571 / :631 / :649 / :705 / :822)。tasks.md 勾选唯一的提交点在 Phase D (yaml:866「归档目录 / handoff / checkbox 勾选 / 归档后台账」)。
- yaml:837 (TASK-031 开 PR 前): 只 add `verification-ledger.md`, 其后 porcelain「不得有任何一行触及本 cycle 交付物路径 —— 本 Spec 目录 openspec/changes/handoff-multibranch-subdir-path-fidelity/ · …」。
- 5.5 的勾选时点 (yaml:704「勾选 tasks.md 5.5 时…」) 与其余 25 行的勾选时点均未写; 而 TASK-032 预演预期 `complete=True` (yaml:859), 前提是预演前 27 行已全部勾选。
- 实跑 (临时仓, 三态):
  ```
  STATE plan-as-written (TASK-028 ticks 5.6, no commit point for tasks.md)
    porcelain=[ M openspec/changes/handoff-multibranch-subdir-path-fidelity/tasks.md;?? .aria/;]
    TASK-031 scoped check: FAIL -> [ M openspec/changes/handoff-multibranch-subdir-path-fidelity/tasks.md]
  STATE hypothetical (tick committed by some unstated step)
    porcelain=[?? .aria/;]
    TASK-031 scoped check: PASS
  坏态 (本次 AB 结果目录未提交, ab-results/ 下另有已跟踪文件)
    porcelain=[?? aria-plugin-benchmarks/ab-results/2026-09-20-handoff-multibranch-rule6/;]
    scoped check FAIL -> [?? aria-plugin-benchmarks/ab-results/2026-09-20-handoff-multibranch-rule6/]
  ```
  `?? .aria/` 是临时仓里 `.aria` 下没有已跟踪文件所致, 真仓不会这样折叠, 不影响结论。核验对真实坏态有鉴别力, 问题只在计划自己的勾选指令让它在好态下也红。

**照计划执行会出的错**

- 严格照 TASK-028 勾选 5.6 之后, TASK-031 的有范围核验在健康常态下**必然 FAIL** (恒假)。执行者只能临场三选一:
  1. 把 tasks.md 顺带提交进 PR —— 违反「只 add verification-ledger.md」;
  2. 撤回 5.6 的勾 —— 违反 TASK-028;
  3. 把该行判为「与本 cycle 无关」—— 与核验字面相反。
- 5.5 若在 TASK-026 完成时勾选, 落入同一形态。
- 其余行勾选时点未定义, TASK-032 预演前是否已勾满 27 行由执行者自决。

**建议改法** (二选一写死)

1. **推荐**: 勾选统一放到 TASK-032 —— 全部 27 行在归档预演之前由主控一次勾选 (5.4 / 5.6 按清单第 15 条, 5.5 按 yaml:704 的替换规则), 随 Phase D 提交。TASK-028 与 tasks.md 5.6 行改为「第一次自检完成即满足勾选条件, 勾选动作在 TASK-032」, 清单第 15 条同步。
2. 或 TASK-031 的台账提交同时 add tasks.md, 并写明其余各行的勾选时点。

#### M2 [Major] type=issue · category=testing · scope=TASK-029 第 2 步 / 第 4 步 (yaml:769, :771) · TASK-023 notes (yaml:632) · v3 引入: 是

**证据**

- yaml:769 第 2 步:「git -C aria checkout master 后断言 …; standards 同形」。
- yaml:771 第 4 步:「git -C aria status --porcelain 与 git -C standards status --porcelain 输出均为空; 另在 standards 子模块内 grep -n '#<' conventions/session-handoff.md 零命中 (TASK-025 回填或回落形态已提交)」。
- yaml:632:「TASK-029 合并前复查占位已清」。
- 第 4 步执行时, standards 工作树已在第 2 步切到 master; TASK-023 的占位与 TASK-025 的回填只在 standards feature 分支上。`0f50239` 的 TASK-029 没有这两步 (v3 新增)。
- 实跑 (临时仓, 照第 2 → 4 → 5 步):
  ```
  STATE A (bad: backfill never done, placeholder committed on feature)
    step2 checkout master rc=0 | Switched to branch 'master'
    step4 porcelain=[]
    step4 grep '#<' hits=0 (branch=master)
    step5 merged; placeholder in merged master: 1
  STATE B (good: backfill committed on feature)
    step2 checkout master rc=0 | Switched to branch 'master'
    step4 porcelain=[]
    step4 grep '#<' hits=0 (branch=master)
    step5 merged; placeholder in merged master: 0
  STATE C (bad: backfill edited but not committed)
    step2 checkout master rc=1 | error: Your local changes to the following files would be overwritten by checkout:
  STATE D (bad: uncommitted change in file identical on both branches)
    step2 checkout master rc=0 | Switched to branch 'master'
    step4 porcelain=[ M other.md;]
  ```

**照计划执行会出的错**

- 第 4 步的 grep 对 A (占位从未回填) 与 B (已回填) 输出完全相同 ⇒ 恒真。占位 `10CG/aria-plugin#<TASK-025 开出的号>` 可随第 5 步进入 standards master, 再经 TASK-034 推到共享 SOT。合并后没有任何一步检查 standards 合并树的内容 (第 7 步只跑 aria 两腿与谓词, yaml:775)。
- 工作树不干净时:
  - C 形在第 2 步就报错, 而第 2 步的处置只覆盖「不能快进」;
  - D 形把改动带到 master, 第 4 步断言失败, 但计划没写失败后做什么。

**建议改法**

1. 干净工作树断言挪到第 2 步 checkout 之前, 在两个 feature 分支上做; 失败 ⇒ 停下, 查明归属后在对应 feature 分支提交或上报, 不 stash。
2. 占位检查改为针对提交而非工作树, 二选一:
   - 合并前 `git -C standards show <standards feature 分支>:conventions/session-handoff.md | grep -c '#<'` 为 0;
   - 或第 5 步之后 `git -C standards grep -n '#<' HEAD -- conventions/session-handoff.md` 零命中。

   同时正向核合并树含 TASK-023 的第三态从句与 `10CG/aria-plugin#<n>` (或回落形态)。
3. 该核验用状态 A 做一次负控, 结果记台账 (memory `check-runs-at-baseline-first`)。

#### M3 [Major] type=risk · category=architecture · scope=TASK-029 第 3 / 5 / 6 步 (yaml:770, :772, :773) · TASK-027 (yaml:723) · v3 引入: 部分

**证据**

- yaml:770 第 3 步:「aria origin/master 相对 TASK-027 记录的取号时 SHA 已前进 ⇒ 回 TASK-027 重跑取号计算; 取号值变化则先在 aria feature 分支改号并提交, 再从第 1 步重走本任务」。
- yaml:772 第 5 步只写 `git -C aria merge --no-ff <aria feature 分支>`, 没有冲突处置; 第 6 步只核版本 5 文件取值 (yaml:773)。
- 计划明确预期并发发版: yaml:723 取号时读并发轨 handoff; R2 tech-lead 席报告 `:243` 记本轨 A.2 期间另一容器发出 v1.73.2 / v1.73.3。
- 实跑 (bare origin + 两克隆; 我方 feature 改版本号与 CHANGELOG, 另一方先推 master; 照第 2 → 3 → 5 步):
  ```
  S1 no concurrent commit: step5 merge rc=0; conflicts=[]
  S2 concurrent release 1.74.0 on master: step5 merge rc=1; conflicts=[CHANGELOG.md plugin.json ]
  S3 concurrent unrelated commit: step5 merge rc=0; conflicts=[]
  ```

**照计划执行会出的错**

- 触发第 3 步改号的正是「并发发版占了号」。这种情形下, 第 5 步合并**必然**在版本文件与 CHANGELOG 上冲突 —— 两侧从同一基线把同一行改成不同值。计划没写在哪一侧解、按什么规则解、要不要 `merge --abort`。
- 若在 master 的合并提交里临场解 CHANGELOG 冲突, 丢掉对方发版小节不会被任何核验发现:
  - 第 6 步只核本方的号;
  - 第 7 步回归不看 CHANGELOG 内容;
  - ⇒ TASK-034 会把删了别人发布说明的 master 推上两个远端。README.md badge / marketplace.json 两处同理。
- 改号提交是新写文字, 却产生在 TASK-028 第一次自检之后, 计划没有要求补检。

**建议改法**

1. 第 3 步在 origin/master 前进时改为: 在 aria (与 standards) feature 分支上 `git merge origin/master`, 冲突按写死的规则解 (版本 5 文件取重算号; CHANGELOG 保留对方小节, 本方小节置顶并用重算号), 提交记 SHA, 对新增行补跑写法自检, 再从第 1 步重走 ⇒ 第 5 步不再冲突。
2. 第 5 步补: 出现冲突 ⇒ `git merge --abort`, 不在 master 上解冲突, 转上一条。
3. 第 6 步追加: 合并树 CHANGELOG 仍含第 2 步所记 origin/master 上的全部版本小节 (`grep -c '^## \['` 不减)。

#### M4 [Major] type=risk · category=architecture · scope=TASK-034 (yaml:793-795) · v3 引入: 否

**证据**

- yaml:794「owner 逐条授权后推送 (授权记台账), push 给足超时」; yaml:795「对 origin 与 github 各自 git ls-remote 取 master 与 tag 对象 SHA, 与本地一致才算完成」。
- 计划没有规定推送的命令形态与 master / tag 的先后, 也没有「远端 master 已前进 (non-fast-forward 被拒)」或「只推成一个远端」时的处置 —— yaml:793 的回退只覆盖「出现同名 tag」。`0f50239` 的 TASK-034 同样如此。
- tag 在 TASK-029 第 8 步就已打好 (yaml:776); TASK-029 第 1 步 fetch 到 TASK-034 推送之间隔着 owner 授权等待。
- 实跑 (bare origin; 本地合并提交 + annotated tag; 另一克隆先推 master):
  ```
  A single push master+tag (non-atomic): push rc=1
       * [new tag]         v9 -> v9
       ! [rejected]        master -> master (fetch first)
      remote master==local? no; remote tag v9 present? YES
  B --atomic master+tag: push rc=1
       ! [rejected]        master -> master (fetch first)
       ! [rejected]        v9 -> v9 (atomic push failed)
      remote master==local? no; remote tag v9 present? no
  C master only: push rc=1
       ! [rejected]        master -> master (fetch first)
      remote master==local? no; remote tag v9 present? no
  D --follow-tags master: rc=1
       * [new tag]         v9 -> v9
       ! [rejected]        master -> master (fetch first)
      remote tag v9 present? YES
  ```

**照计划执行会出的错**

- 最常见的两种写法 —— `git push origin master v<vNEXT>` 与 `git push --follow-tags origin master` —— 在远端 master 已前进时, master 被拒而 tag 照样发布 ⇒ 远端出现一个指向「不在 master 上的合并提交」的发布 tag。
- 该号在远端被占: 下次重走 TASK-029 时第 6 步必判同名 tag 而再次改号; 已发布的孤儿 tag 须另行外向删除。
- 半推 (origin 成、github 拒) 时核验只报「不一致」, 没有处置 (memory `partial-push`)。

**建议改法**

- TASK-034 对每个远端写死顺序:
  1. `git -C aria push <remote> master`;
  2. `ls-remote` 核 master 与本地一致;
  3. 再 `git -C aria push <remote> refs/tags/v<vNEXT>`;
  4. 核 tag 对象。

  或每个远端用 `git push --atomic <remote> master refs/tags/v<vNEXT>`。禁用 `--follow-tags` 与非原子的多 ref 推送。
- master 被拒 ⇒ 不推 tag, 按 TASK-029 第 6 步回退 (含 `tag -d`) 后从第 1 步重走。
- 只推成一个远端 ⇒ 只对失败的远端重试, 不 force, 记台账。
- standards 同形 (无 tag)。

#### M5 [Major] type=issue · category=testing · scope=TASK-026 (yaml:696-699) · owner_gates (yaml:131-132) · tasks.md:128 · v3 引入: 部分

**证据**

(a) **delta 的来源与符号**
- yaml:698 登记「AB_TEST_OPERATIONS.md 场景 1 的验收 delta.pass_rate > 0 是否达成」; yaml:131 以「delta.pass_rate ≤ 0」触发 owner 裁。
- SOT 里该量出自 `aggregate_benchmark.py → benchmark.json`: `AB_TEST_OPERATIONS.md:219` 验收行, `:542`「benchmark.json 中 delta.pass_rate > 0」。
- skill-creator 对「改进既有 Skill」规定基线目录名为 `old_skill/` (`skill-creator/SKILL.md:186`)。`aggregate_benchmark.py:101` 用 `sorted(eval_dir.iterdir())` 发现配置, `:208-214` 取 `configs[0] − configs[1]`。
- 实跑 (命令 5):
  ```
  with_better_old config_order= ['old_skill', 'with_skill'] delta.pass_rate= -0.50
  old_better_old config_order= ['old_skill', 'with_skill'] delta.pass_rate= +0.50
  new_better_old config_order= ['new_skill', 'old_skill'] delta.pass_rate= +0.50
  ```
- 本仓先例 `2026-09-05-v1.70.0-a1-entry-rule6/SCORES.md` 头部写「脚本从各臂 grading.json 直接汇总」, 未用该聚合脚本; 计划没有钉取哪一种。

(b) **WITHOUT_BETTER 无计算来源**
- yaml:697 / :132:「判回归或出现 WITHOUT_BETTER ⇒ 阻断」。
- 该标签定义在 `AB_TEST_OPERATIONS.md:372`「without 胜率 > 50%」, 语境是 with vs without; 聚合脚本不产出任何 verdict (grep 计数 0)。
- 计划没写 with vs old 下「胜率」怎么算 (平局是否进分母), 没写它按首轮样本还是复跑后样本判, 也没写它与 yaml:696「复跑两次、三样本 ≥2 仍劣」的先后。
- 构造算例 (非实测): 13 个 eval 中首轮 1 个 old 胜、0 个 with 胜、12 个平局 —— 分母含平局得 1/13, 不含平局得 1/1 (> 50%)。

**照计划执行会出的错**

- 按 SOT 用官方脚本聚合、目录照 skill-creator 命名时, benchmark.json 的 delta 实为 old − with:
  - 真实回归显示为 delta > 0 ⇒ RESULT.md 登记「SOT 验收达成」, yaml:131 的 owner 裁决点不触发;
  - 真实提升反而触发 owner 裁。

  回归若分散 (每次劣的 eval 不同), 逐 eval 复跑判不出, 就会带着假绿进 TASK-027。
- WITHOUT_BETTER 的两种算法分别导向「阻断, 按『Skill 有负面影响』上报」与「走预期的 delta ≤ 0 owner 裁」, 执行者须临场选。

**建议改法**

1. 在 TASK-026 写死 `delta.pass_rate = mean(with pass_rate) − mean(old pass_rate)`, 由脚本从两臂 grading.json 直接汇总 (同先例)。若用 `aggregate_benchmark.py`, 配置目录命名 `new_skill` / `old_skill`, 读 delta 前断言 `run_summary` 的首个配置是 with 臂, 断言输出记台账。
2. WITHOUT_BETTER 二选一: 删去 (逐 eval 回归判据已覆盖「with 劣于 old」); 或写明 with vs old 下的算法 (复跑之后、平局是否计入分母、阈值) 及其与复跑判据的先后。

#### M6 [Major] type=issue · category=architecture · scope=tasks.md:39-56 (AI 流程判断清单) · yaml:837 / :501 / :777 · v3 引入: 是

**证据**

- `standards/conventions/configured-gate-authority.md:109`: AI「**任何**自作主张的流程判断 (跳过 / 降级 / 改序 / 替代)」须写进 handoff 请复议。tasks.md:37 自述清单收录「post_planning R2 rework (v3) 中由 AI 自行作出」的判断; yaml:864 要求周期 handoff 照录。
- 以下三项 v3 / v3.1 落地的判断不在清单第 1–18 条中 (`grep -n "porcelain\|原位\|副本生命周期\|有范围" tasks.md` 只命中 :25 / :104 / :125, 均不在清单段):
  1. **TASK-031 核验收窄** (v3.1 主控): R2 聚合 `:118` 接受的处置是「主仓 git status --porcelain 为空」。yaml:837 改为「有范围的检查 … 故不要求整体为空」, 其余行由 AI 逐条判「与本 cycle 无关」—— 属降级 / 替代。
  2. **TASK-018 不变式替代** (v3, R2 跨簇连带): yaml:501「取代『feature 分支工作树 git status 前后一致』」, 泄漏检测改由 TASK-021 回归兜底 —— 属替代。
  3. **TASK-029 合并树回归原位跑** (v3): R2 聚合 `:117`「主控调整: TL 建议 … 未采用」, yaml:777 —— 未采纳审计席方案的主控判断, 与已入清单的第 3 条 (SC-12a 执行方法) 同性质。

**照计划执行会出的错**

- 周期 handoff 照录清单时, 这三项不会出现在请 owner 复议的内容里。
- 其中第 1 项在 TASK-031 直接决定开 PR 前哪些行可由 AI 自判放行。
- 定级沿用 R2 M5 口径: 判断已公开写在计划里并经本闸门审阅, 故不定 Critical。

**建议改法**

- 清单补第 19–21 条, 每条写「做了什么 + 理由」。
- 清单头部「第 1–17 条由主控作出 …」一句同步写明: v3.1 主控核验返修也产生了判断 (第 12 条的 (j3) 与新第 19 条)。
- 若 M1 按改法 2 修, 第 19 条一并写明「tasks.md 勾选随 PR 提交」的取舍。

#### m1 [Minor] type=issue · category=documentation · scope=metadata.owner_gates (yaml:125-139) · TASK-026 (yaml:702) · TASK-031 (yaml:840) · tasks.md:71 · v3 引入: 是

**证据**

- yaml:126 与 tasks.md:62 称每项都写「未获授权 / 裁定时的处置」; 13 项中 8 项没有 (yaml:129 / :130 / :133 / :134 / :136 / :137 / :138 / :139)。
- yaml:137 把 release_gate 推协调 ref 列为须授权的外向推送; 同一机制的 B.0 phase1_gate 认领推送 (tasks.md:71「另写一条 claim」; `phase1_gate.py` docstring 第 9 步 `resilient_push`) 未列。执笔人自报的存疑点 (release_gate 推送列入授权) 本身可以成立, 问题在两类协调 ref 推送口径不一。
- yaml:702「AB 结束后 … TASK-027 起在不带该变量的新会话执行」是第二个 owner 启动动作, 未列入。
- yaml:134 列「推送、Forgejo PR、合并」; yaml:840 只写「推送 feature 分支与开 PR 属 … 外向动作」, 未提合并。

**照计划执行会出的错**: 清单自称单一来源却不完整。B.0 要不要先请授权、AB 后等谁重启会话、未获授权时停在哪, 都由执行者临场定。

**建议改法**

- 补 B.0 phase1_gate 推送与 AB 后重启会话两项; 或把两类协调 ref 推送统一定为「协议内推送, 不单列授权」并删 yaml:137 的授权要求, 二者取一。
- 8 项缺处置的各补一句 —— 多数为「未获授权 ⇒ 停在本步, 不进下游任务, 记台账」; TASK-034 另写本地合并与 tag 保持未推送时的处理。
- yaml:840 补「合并」。

#### m2 [Minor] type=risk · category=implementation · scope=TASK-026 (yaml:680) · TASK-024 (yaml:648) · v3 引入: 部分

**证据**: TASK-026 `est_hours: 8` (`0f50239` 为 7), 已到 4-8h 粒度上限。以下条件分支都计入同一任务, 估时与拆分规则不随之变化:
- yaml:648「若对 phase-d-closer/SKILL.md 落编辑: TASK-026 追加 phase-d-closer AB」;
- yaml:696 劣势 eval 各复跑两次;
- yaml:689 / :702 的两次会话切换。

**照计划执行会出的错**: 触发追加套件或多条复跑时, 单任务明显超过粒度上限, 进度与 `ai-native-estimator` 采集失真。

**建议改法**: 写明「TASK-024 落 phase-d-closer 编辑, 或需复跑的 eval ≥ 3 条 ⇒ 按套件拆出独立任务 (工时另估, 依赖同 TASK-026)」; 或把「PREDICTION 与运行」和「RESULT 与 issue」拆成两个任务。

#### m3 [Minor] type=issue · category=implementation · scope=TASK-035 补丁 3 (yaml:518) · TASK-033 (yaml:431) · v3 引入: 是

**证据**

- yaml:518:「与 TASK-017 的『_get_file_commit_date 仍拼顶层路径』同形, 可复用该副本与 diff」。
- TASK-017 与 TASK-035 均只依赖 TASK-033 (命令 1: 同在波次 12, 并行)。
- yaml:515 / :501 规定「任务结束时 git -C aria worktree list 不含本任务副本」; yaml:481 规定 TASK-017「每条补丁前副本复位」。
- yaml:431 只写「TASK-015..018 的一次性副本一律 …」, 漏了 TASK-035。

**照计划执行会出的错**: 并行派发时, 复用对方副本会与对方的复位动作互相覆盖; 串行时 TASK-017 结束已移除副本, 无从复用。

**建议改法**: 删去「可复用该副本」, 改为「补丁 diff 可与 TASK-017 相同, 但在本任务自己的副本上实跑」; yaml:431 改为「TASK-015..018 与 TASK-035」。

#### m4 [Minor] type=issue · category=architecture · scope=TASK-032 (yaml:862-866) · v3 引入: 否

**证据**: TASK-031 在 Forgejo 服务端合并主仓 PR (主仓属 CLAUDE.md 多远程硬约束 1 的例外), 此时本地 master 落后 origin/master。yaml:866 只写 Phase D 提交「经 owner 授权后双推」, 未写:
- 这些提交落在哪个分支;
- 提交前是否先 fetch 并把本地 master 快进到含合并提交的 origin/master (memory `stale-local-main` / `fetch-then-write`)。

**照计划执行会出的错**: 在陈旧的本地 master 或已合并的 feature 分支上归档并提交 ⇒ 双推被拒, 或产生分叉合并。

**建议改法**: TASK-032 开头补 `git fetch origin` → `git checkout master` → `git merge --ff-only origin/master` (不能快进即停), 断言 HEAD 含 TASK-031 的合并提交, 再进归档预演。

#### m5 [Minor] type=risk · category=documentation · scope=读前必看第 13 条回落支 (tasks.md:30) · TASK-031 (yaml:840-841) · v3 引入: 部分

**证据**

- 回落支让规划提交随 feature 分支进 PR: `07e0a6e` / `0f50239` / `2b9cb3e` 及后续轮次, post_planning 各轮报告以这些 SHA 为审计对象。
- yaml:841 交给 `phase-c-integrator`: 其 SKILL.md:238 写 branch-manager C.2.1「sync rebase」; branch-manager SKILL.md:497 的 `merge_strategy` 默认 `squash`。
- 台账另记有 TASK-026 / 030 / 031 的主仓提交 SHA。
- 本仓先例 PR 均为 merge commit (命令 10), 但计划未写明。

**照计划执行会出的错**: 若沿技能默认 rebase 或 squash, 审计报告引用的规划提交 SHA 与台账所记主仓 SHA 都不会出现在远端 master 上, 事后无法按 SHA 复核。

**建议改法**: TASK-031 写明:
- 同步 origin/master 用 merge 进 feature 分支 (不 rebase);
- PR 以 merge commit 合并 (不 squash);
- 合并后核台账所记主仓 SHA 均为 origin/master 的祖先。

#### m6 [Minor] type=issue · category=implementation · scope=TASK-027 (yaml:729) · v3 引入: 否

**证据**

- 其余提交点都写「由主控在 <仓> feature 分支提交, 只 add 本任务 deliverables, 提交 SHA 记台账」(yaml:548 / :571 / :631 / :649 / :705 / :822)。
- yaml:729 只写「本任务的改动由主控提交」, 未写分支、add 范围与 SHA。
- TASK-029 第 3 / 6 步都依赖「号在 aria feature 分支上」。

**照计划执行会出的错**: 版本 5 文件漏 add 一个 (memory `scoped-add-splits-claim` 实证过的形状), 或提交落到 master。

**建议改法**: 与其余提交点同式补齐, 提交后核 `git -C aria show --stat HEAD` 恰含 deliverables 五个文件。

### 核对无误的部分 (不计 finding)

- **结构**: 35 任务 / 105h / agent 分布、DAG 无环无悬空、27 个 parent 对 27 个 checkbox, 均属实。组 5 标题行 (tasks.md:122) 与依赖图一致。TASK-033 是波次 11 的唯一节点, 且是组 3 / 组 4 全部任务的祖先。
- **组 3 与组 4 并发的文件域**:
  - TASK-019 (schema)、TASK-020 (collector / phase-1-collectors / dedupe 测试 docstring)、TASK-023 (standards + layer-l-integration)、TASK-024 (三份候选文件) 两两不相交;
  - 组 3 只在一次性副本上改;
  - 组 3 用到的测试模块无主仓布局依赖 (`grep "parents\[\|/home/dev\|\.aria/repro"` 于四个测试模块零命中);
  - 泄漏补丁若随组 4 提交进入 feature 分支, 必然让 TASK-021 回归变红 —— 反事实按设计都是致红补丁。
- **SC-11 验证脚本**: 退出码 0, 矩阵逐字节一致, `--emit-json` 三字段一致, `PRED` 与 yaml 19/19 一致; `finally` 清理生效。
- **归档门预演预期** (yaml:859): 对 v3.1 文本复跑成立 (complete True / warn / 2.2、4.4、4.3 三条 / d_payload 非空)。`spec_complete.py --gate <spec_dir>` 确为只读 CLI。
- **Phase D 工具衔接**:
  - release_gate 按 (track_id, container) 释放全部 active claim, TASK-032「含 B.0 可能新写的那条」可执行;
  - openspec-archive Step 7 为末步,「停在 Step 7 之前」可行。
- **TASK-029 回退**: 前置 (HEAD^1 等于第 2 步所记 SHA、HEAD^2 等于 feature HEAD、工作树干净) 保证 `reset --hard` 只丢未推送的合并提交; aria 发布 tag 为 annotated, 与「tag 对象 SHA」的核验口径一致。
- **TASK-035 六个补丁**: 补丁 1 / 2 / 4 / 6 与 proposal SC 表反事实句对得上。补丁 3 / 5 偏离字面, 理由 (TASK-011 落地后 git show 失败会让该行消失, 不再变 legacy) 成立, 已列入清单第 18 条。
- **执笔人自报存疑点的判定**:
  - (j4) `4[- ]levels?` 缺左边界: 当前扫描面零命中, 误伤只会表现为可见的 FAIL, 不构成 finding;
  - 验证脚本 target 保留 `finalized`: 不影响, `alt_j3_anchor` 态覆盖去掉该词的写法;
  - TASK-026 8h: 见 m2;
  - release_gate 推送列入授权: 见 m1;
  - 补丁 3 / 5 取法: 成立;
  - TASK-029 第 2 步早于第 4 步: 成立且带出 M2。
- **不可协商规则与多远程约束的承载**:
  - Rule #6: TASK-026 照跑 `/skill-creator`, 且先于合并 (`benchmarks.require_before_merge: true`);
  - Rule #8: TASK-031 经 C.2.4;
  - Rule #9: TASK-032 写 `docs/handoff/`;
  - 硬约束 1: TASK-029 本地 `--no-ff`;
  - 硬约束 2: TASK-034 / 031 / 032 逐远端 ls-remote。
- **其它**:
  - `aria/.gitignore` 忽略 `__pycache__` 且 pytest 腿禁 cacheprovider, 各处干净工作树断言不会被缓存文件误红;
  - TASK-030 引用的五个 custom check 名均存在, 16 个版本点计数属实;
  - dedupe / track_board / scan_integration 基线用例数 (23 / 5 / 19) 属实。

## Verdict

**PASS_WITH_WARNINGS** —— 0 Critical / 6 Major / 6 Minor。

问题分三类:

1. **新写的核验与计划自身的其它指令相互矛盾**
   - TASK-031 有范围核验被 TASK-028 的勾选指令判恒假 (M1);
   - TASK-029 第 2 步的 checkout 使第 4 步占位检查恒真 (M2)。
2. **并发发版路径的必然后果没有处置**
   - 改号支下合并必然冲突 (M3);
   - 推送竞态会发布孤儿 tag (M4, 非 v3 引入)。
3. **判据与清单的可判定性、完整性**
   - AB 的 delta 在官方聚合脚本下符号相反、WITHOUT_BETTER 无算法 (M5);
   - AI 流程判断清单漏列 v3 / v3.1 的三项替代判断 (M6)。

6 条 Major 中, v3 引入 3 条 (M1 / M2 / M6)、部分引入 2 条 (M3 / M5)、v3 前已有 1 条 (M4)。

## Vote

**REVISE**

## 轮次记录

Round 3 (tech-lead, convergence): REVISE — 0C/6M/6m (v3 引入 Major 3, 部分引入 2, 非 v3 引入 1)。要点:
- TASK-028 要求 5.6 即勾而 tasks.md 无提交点, TASK-031 有范围核验必然 FAIL (M1);
- TASK-029 第 2 步先切 master, 第 4 步占位 grep 恒真、脏树无处置, 已用临时仓四态实跑证实 (M2);
- 第 3 步改号支在并发发版下使第 5 步合并必然冲突且无解法 (M3);
- TASK-034 未定推送形态, 非原子推送与 `--follow-tags` 在 master 被拒时仍发布 tag (M4, risk);
- skill-creator 聚合脚本对 with_skill / old_skill 目录给出 old − with 的 delta, WITHOUT_BETTER 无计算来源 (M5);
- AI 流程判断清单漏列 TASK-031 收窄、TASK-018 替代、合并树原位回归三项 (M6)。

R2 本席侧重的处置全部有文字承载, 其中 PP2-M3.4 / M3.6 与 m6 的合并前复查效果不足。

---
checkpoint: post_planning
mode: convergence
rounds: 3
converged: false
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-15T23:05:00.000Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/detailed-tasks.yaml
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
counts_raw: 0C/11M/24m
counts_dedup: 0C/9M/17m
sibling_probe: no_sibling_found
---

# post_planning R3 聚合 — handoff-multibranch-subdir-path-fidelity (10CG/Aria#195, A.2/A.3 v3.1 `2b9cb3e`)

> **对象**: tasks.md (27 项 checkbox) + detailed-tasks.yaml (35 TASK) + sc11-predicate-validation.py, 主仓 master `2b9cb3e` (本地, 未推送)。
> **Sibling probe (本轮入口)**: 本轮已完整扫描, 未发现同 issue 竞品 (`status=ok`, origin 161 / github 155, 无 cap, 耗时 23s)。
> **drift-checker**: convergence 模式未 opt-in ⇒ 跳过, `drift_check_skipped: true`。
> **审计前后状态 (主控核验)**: 主仓 / aria / standards 的 HEAD 与 `refs/aria/coordination` 均未变; aria / standards 工作树干净; `.aria/audit-reports/` 由 863 份变为 868 份, 恰为本轮 5 份席位报告; 各席临时目录均已删除。
> **派发**: 按 agent-team-audit 默认 `max_parallel_agents: 2` 滑动窗口派发 (tech-lead + code-reviewer → qa-engineer → backend-architect → knowledge-manager)。
> **五席共识 (不计 finding)**:
> - 验证脚本 rc=0; 13 态 x 19 谓词矩阵与 yaml 实测块逐字节一致 (五席各自复现); 脚本 `PRED` 与 yaml 谓词逐字一致; `-OO` 下行为不变; 无残留 assert; finally 清理生效。
> - 结构: 35 任务 / 105h / 15·10·10、依赖无环、27 个 parent ↔ 27 个 checkbox 均属实。
> - 引用行号: 组 2 与 references / CHANGELOG / standards 的行号逐处命中 (backend-architect / knowledge-manager 两席字节级核对)。
> - 归档门全勾预演与计划预期一致 (tech-lead / code-reviewer)。
> - R2 的 9 个 Major 簇全部有文字承载。
>
> 问题集中在三处: **新写流程之间的时点与状态矛盾**、**罕见并发路径的必然后果**、**判据仍可被像真实坏情形的写法骗过**。

## drift_metrics (Step 0 anchor 快照)

- checkpoint: post_planning
- primary_goal: 把 Approved 的 10CG/Aria#195 proposal (v7) 分解为可执行的 Level 3 双层任务 (tasks.md + detailed-tasks.yaml), 忠实落地决策单 2026-09-12 §2 的 10CG/Aria#195 表与 §5
- in_scope: 任务分解 / 依赖与执行序 / agent 分配 / 验收判据 / 裁定翻转的执行口径 / 基线复核记录
- out_of_scope_hints: proposal 设计取舍本身 (post_spec 已由 owner 裁定接受)
- source_sha: 2b9cb3e
- drift_ratio: null (未 opt-in)

## 判定

| 席 | verdict | counts | vote | 一句话 |
|---|---|---|---|---|
| tech-lead | PASS_WITH_WARNINGS | 0C/6M/6m | REVISE | 勾选无提交点使 TASK-031 核验恒假; TASK-029 先 checkout 使占位检查恒真; 改号必合并冲突; 推送竞态发布孤儿 tag; 聚合脚本 delta 符号反、WITHOUT_BETTER 无算法; AI 流程判断清单漏 3 项 |
| code-reviewer | PASS_WITH_WARNINGS | 0C/2M/11m | REVISE | (j1)(j2)(j3) 不钉现状键元组, 脚本 target 自己就留着四元元组; 改号路径必合并冲突且无分支 |
| qa-engineer | PASS_WITH_WARNINGS | 0C/1M/2m | REVISE | v3.1 返修 (尤其 TASK-031 放宽) 未进 AI 流程判断清单 |
| backend-architect | PASS_WITH_WARNINGS | 0C/1M/2m | REVISE | TASK-035 补丁 1 在 TASK-011 之后使 SC-1 行整体消失, 与原句「变 legacy」不符; 组 2 行号与 git 语义全部核实 |
| knowledge-manager | PASS_WITH_WARNINGS | 0C/1M/3m | REVISE | TASK-019 / 020 / 027 / 030 新增「记台账」而 deliverables 未列台账 (R2 m13 同形复发) |

**合并判定: PASS_WITH_WARNINGS (0 Critical / 9 Major 簇) · Vote REVISE 5 / PASS 0 · 未收敛 (R3)。**

## 收敛计算与轮次判断

- **结论集比较**: R3 的 9 个 Major 簇与 R2 的 9 簇没有一个 (category, scope) 相同 ⇒ `conclusions_stable = false`; 无 PASS 票 ⇒ `converged = false`。
- **振荡检测**: 取最近三轮 (R1 / R2 / R3) 比较, R3 ≠ R1 ⇒ 无振荡。
- **Major 趋势**: R1 13 → R2 9 → R3 9, **持平**。
- **本轮修订引入的 Major 占比**:
  - 完全由 v3 / v3.1 引入: 5 簇 (PP3-M1 / M2 / M6 / M8 / M9)
  - 部分引入: 3 簇 (PP3-M3 / M5 / M7)
  - 此前已有: 1 簇 (PP3-M4)

  占比 5/9 (计入部分引入为 8/9), 超过 1/2。
- **两条判据同时亮起**: memory `stop-adding-rounds` (major 不再下降) 与 `marginal-return-negative` (本轮修订引入占比 > 1/2)。按 Rule #10, 已启用闸门的轮次上限是 owner 的配置 (`max_rounds: 5`), AI 不得据此自行提前结束; 继续 R4。R5 结束仍未收敛时, 按降级策略请 owner 三选一。这一信号同时写入会话 handoff 请 owner 复议。
- **R4 处置原则 (主控, 为打断「修订即新增表面」的循环)**:
  1. **罕见并发路径一律 fail-closed**: 取号被占、合并冲突、推送被拒、只推成一个远端 —— 停下, 原样记台账, 上报 owner, 附先例指针 (如 aria `ec72175`); 计划里不再写多分支的自动恢复流程。
  2. **能删则删, 能合则合**: WITHOUT_BETTER 删去 (逐 eval 回归判据已覆盖); 27 行勾选合并到一个时点。
  3. **新机械检查的条件**: 只在处置本身要求时新增; 每条新检查须写出其自然红态 (负控) 在哪里出现。

## Major 簇 (去重后 9) 与处置 (R4 rework)

> 执笔人以席位报告原文为准, 本表只是索引。

### PP3-M1 — tasks.md 勾选没有提交点, TASK-031 的有范围核验在好态下恒假; 其余行勾选时点未定义

- **席位**: TL M1 · CR m9 (预演预期 complete=True 却晚于 5.4 勾选, 并入)
- **v3 引入**: 是 —— v3 的「5.6 完成即勾」叠加 v3.1 主控核验要求的「有范围核验」
- **证据要点**: TL 临时仓三态 —— 照计划勾 5.6 后, `M tasks.md` 触及本 Spec 目录, 核验 FAIL; CR 全勾副本只留 5.4 未勾 ⇒ `complete: False`。
- **处置 (接受, 采 TL 改法 1)**:
  1. 27 行勾选统一在 TASK-032 归档预演**之前**由主控一次完成, 随 Phase D 提交。
  2. 5.4 与 5.6 的勾选条件照清单第 15 条; 5.5 的父目录 token 替换规则移到 TASK-032 的勾选步骤。
  3. TASK-028 与 tasks.md 5.6 行改为「第一次自检完成即满足勾选条件, 勾选动作在 TASK-032」; TASK-026 删去「勾选 5.5 时…」, 该规则并入 TASK-032。
  4. 清单第 15 条同步。

### PP3-M2 — TASK-029 第 2 步先切到 master, 第 4 步占位检查因此恒真; 工作树不干净时无处置

- **席位**: TL M2 (Major) · CR m6 / QA m2 (Minor, 并入; 两席只评了步序, 未发现占位检查对工作树恒真)
- **v3 引入**: 是
- **证据要点**: TL 临时仓四态 —— 占位从未回填 (A) 与已回填 (B) 在第 4 步输出完全相同 (`grep '#<' hits=0 (branch=master)`), A 态占位随第 5 步进入 standards master。
- **处置 (接受)**:
  1. **干净断言前移**: 两个子模块的干净工作树断言挪到第 2 步 checkout 之前, 在 feature 分支上做; 不成立 ⇒ 停下, 查明归属后在对应 feature 分支提交 (只 add 被改文件) 或上报, 不 stash。
  2. **占位检查改查提交**: `git -C standards show <standards feature 分支>:conventions/session-handoff.md | grep -c '#<'` 为 0, 并正向核该文件含第三态从句与 `10CG/aria-plugin#<n>` 或回落形态。自然负控: TASK-025 回填前同一命令输出 1, 两次输出记台账。
  3. **删除旧检查**: 删去第 4 步对工作树的 grep。

### PP3-M3 — 取号被占触发改号后, 第 5 步合并必然冲突, 计划没有冲突分支

- **席位**: TL M3 · CR M2
- **v3 引入**: 部分 —— 改号路径是 v3 新增, 并发发版风险 v1 就有
- **证据要点**: TL 与 CR 各自在临时仓复现 `CONFLICT (content): Merge conflict in CHANGELOG.md / plugin.json`; 本仓先例 aria `ec72175`「版本重算 1.70.0→1.71.0 (号被同伴轨占用)」。
- **处置 (接受, 按 R4 处置原则 1 收窄)**:
  1. **第 3 步**: aria origin/master 相对取号时 SHA 前进 ⇒ **停下**。台账记三项 (取号时 SHA / 当前 SHA / 前进的提交列表), 列入 owner_gates 上报。恢复方式写成指针 —— 「参照 aria `ec72175`: 在 feature 分支 `git merge origin/master`, 版本 5 文件取重算号, CHANGELOG 保留对方小节并把本方小节置顶, 重跑 TASK-021 两腿回归与 SC-11 谓词, 补跑写法自检」—— 经 owner 确认后执行。计划里不展开多分支流程。
  2. **第 5 步**: `git merge --no-ff` 退出码非 0 ⇒ `git merge --abort`, 断言 HEAD 等于第 2 步记下的 SHA 且工作树干净, 输出记台账后停下上报; 不在 master 上解冲突。
  3. **第 6 步**: 追加断言「合并树 CHANGELOG 的 `grep -c '^## \['` 不少于第 2 步所记 origin/master 上的计数」。不符 ⇒ 按已写死的回退条执行后停下上报 (不再写「回 TASK-027 重新取号后从第 1 步重走」)。

### PP3-M4 — TASK-034 未定推送写法: master 被拒时 tag 仍会发布 (孤儿 tag); 半推无处置

- **席位**: TL M4
- **v3 引入**: 否 (v1 已有)
- **证据要点**: TL bare 仓实跑四种写法 —— `git push origin master v9` 与 `--follow-tags` 在 master 被拒时 tag 照样发布; `--atomic` 两者同拒。
- **处置 (接受, 按 R4 处置原则 1)**:
  1. **推送写法**: 每个远端写死 `git -C aria push --atomic <remote> master refs/tags/v<vNEXT>` (standards 只推 master); 先 origin 后 github; 禁用 `--follow-tags` 与非原子的多 ref 推送。
  2. **任一远端被拒 ⇒ 停下上报, 不 force**:
     - origin 被拒: 本地合并与 tag 保持未推送, 台账记录;
     - origin 成功、github 被拒: 按 memory `partial-push` 记为镜像分叉, 原样记台账并上报。
  3. **核验**: 推后逐 remote ls-remote 核 master 与 tag 对象 SHA, 保持现状。

### PP3-M5 — AB 的 delta 在官方聚合脚本下符号相反; WITHOUT_BETTER 无计算来源

- **席位**: TL M5
- **v3 引入**: 部分 —— SOT 登记与 owner 裁决点是 v3 新增, 取法未钉
- **证据要点**:
  - TL 用官方 `aggregate_benchmark.py` 实跑: `config_order= ['old_skill', 'with_skill'] delta.pass_rate= -0.50` (with 实际更好)。
  - 主控复核源码: `:101` `sorted(eval_dir.iterdir())`, `:208-214` `configs[0] − configs[1]` ⇒ `old_skill` 排在 `with_skill` 之前, delta = old − with。
  - WITHOUT_BETTER 定义在 `AB_TEST_OPERATIONS.md:372` (with vs without 语境), 聚合脚本不产出任何 verdict。
- **处置 (接受, 按 R4 处置原则 2)**:
  1. **delta 取法写死**: `delta.pass_rate = mean(with 臂 pass_rate) − mean(old 臂 pass_rate)`, 由脚本从两臂 grading.json 直接汇总 (同先例 v1.70.0 SCORES.md)。若使用 `aggregate_benchmark.py`, 配置目录命名 `new_skill` / `old_skill` (排序后 with 臂在前), 并断言 `run_summary` 首个配置为 with 臂, 断言输出记台账。
  2. **删去 WITHOUT_BETTER**: 从 TASK-026 / owner_gates / rule6_note / tasks.md 5.5 删去; 注明它是 with vs without 的判定, 不适用于 with vs old, 逐 eval 回归判据是其对应物。该替代列入 AI 流程判断清单。

### PP3-M6 — AI 流程判断清单漏列 v3 / v3.1 的判断

- **席位**: TL M6 · QA M1
- **v3 引入**: 是
- **处置 (接受)**: 清单补以下各条, 每条写「做了什么 + 理由」; 清单头部句写明 v3.1 主控核验返修与 R3 rework 也产生了判断。
  1. **TASK-031 核验放宽**: 由 R2 处置的「主仓 porcelain 为空」放宽为有范围核验 (v3.1 主控)。
  2. **TASK-018 不变式替代**: 「工作树前后一致」替换为副本生命周期证据, 泄漏由 TASK-021 回归兜底 (v3)。
  3. **TASK-029 合并树回归原位跑**: 未采纳审计席的 worktree 方案 (R2 聚合主控调整)。
  4. **v3.1 另两处返修**: 回退命令写死、验证脚本不依赖 assert —— 一句带过即可。
  5. **R4 新增判断**:
     - 勾选合并到 TASK-032 (PP3-M1);
     - 删去 WITHOUT_BETTER (PP3-M5);
     - 罕见并发路径 fail-closed (PP3-M3 / M4);
     - 补丁 1 的口径澄清 (PP3-M8);
     - B.0 认领推送与 release_gate 推送同批授权 (m1);
     - R3 两处 conflicted 的裁决。

### PP3-M7 — (j1)(j2)(j3) 只判「出现 rel_path」, 不钉现状键元组; 验证脚本 target 自身留着四元元组

- **席位**: CR M1
- **v3 引入**: 部分 —— (j1)(j2) 与 target 形态沿自 v2; (j3) 经 v3 / v3.1 两次重写仍未钉元组
- **证据要点**:
  - 主控复核脚本 target 副本: `:429` 首行已写 five levels, `:430` 仍是 `(parse_ok, updated_at, filename, branch)`。
  - CR 自建 `bad_tuples_stale_para` (首行写五级、另起一段讲 rel_path、元组保持四元) ⇒ 19 条全 PASS。
- **处置 (接受, 采 CR 已三态实跑的写法)**:
  1. **替换谓词**: (j1)(j3)(j2) 换为 CR 报告中的 `j1x` / `j3x` / `j2x` —— 定位到 docstring 首段、注释块 `# Tie-break` 至第一个仅含 `#` 的行、同时含 `compound key` 与 `(parse_ok` 的非表格行, 要求 `(parse_ok` 之后含 `rel_path`。`j3x` 保留「`# Tie-break` 恰一行」的 fail-closed 条件。
  2. **脚本改动**: target 补 `_dedupe_sort_key` docstring 元组编辑; 新增 `bad_tuples_stale_para` (期望仅 (j1)(j3) FAIL) 与 `bad_j2_tuple_stale_para` (期望仅 (j2) FAIL)。CR 已实测替换后现有 13 态 0 处差异、元组跨两行书写仍 PASS。
  3. **书写规则**: authoring_rules 与 TASK-020 补「现状键元组写全五元, 留在注释块 / docstring 首段」。

### PP3-M8 — TASK-035 补丁 1 在 TASK-011 之后使 SC-1 行整体消失, 与原句「该行变 legacy」不符

- **席位**: BA F1 (Major); conflicted —— TL / QA 判补丁 1 与原句对得上
- **v3 引入**: 是
- **证据要点**: BA 真实 git 仓实验 —— 补丁 1 下 `tracks=[]`、`unreadable_count=1`、kind `handoff_multibranch_git_show_failed`, 不是「变 legacy」; TASK-035 notes 对补丁 3 / 5 写出了同一因果链, 补丁 1 却没有说明。
- **处置 (接受问题, 不采 BA 的窄化改法; 主控裁决见 Conflicted)**:
  1. **补丁 1 不改**: 保持「枚举层退回 basename」—— 这正是 SC-1 与 SC-17 要抓的真实回归。
  2. **在 TASK-035 写明原句在 TASK-011 之后的表现形态**:
     - SC-1 原句「该行变 legacy + 该 kind 出现 ⇒ 全红」, 现在表现为「该行不在 tracks[] + `handoff_multibranch_git_show_failed` 出现 + unreadable_count == 1」; 所指断言 = 该用例全部断言 (真 track 行存在及取值 / legacy_count == 0 / 无该 kind), 首个失败落在其中任一条即算。
     - SC-17 原句「归档件恒降级 legacy 且 owner_container unknown」, 现在表现为「归档件行消失」; 所指断言不变 (kind / groups / git_show_failed)。
  3. **同步**: 清单第 18 条补补丁 1 的形态说明; TASK-035 的「首个失败断言不属原句所指」规则注明以本条定义为准。

### PP3-M9 — TASK-019 / 020 / 027 / 030 新增「记台账」, deliverables 却未列台账, 也未指明骨架标题

- **席位**: KM F1 (Major) · KM F2 (TASK-016 / 017 台账行缺标题注释, Minor, 并入)
- **v3 引入**: 是 —— R2 m13 同形在 PP2-M3 落地时复发 (memory `fix-the-class`)
- **严重度说明**: R2 聚合把同形实例判为 Minor, 本轮按席位原判计 Major; 聚合不下调席位严重度。
- **处置 (接受, 按类修)**:
  1. **补台账行**: 四个任务的 deliverables 各补 `verification-ledger.md   # §复核结论`; TASK-016 / 017 补 `# §GREEN 与反事实`。
  2. **程序化核对**: 执笔人对 35 个 TASK 做一次「verification 含台账字样 ⇒ deliverables 含台账且带标题注释」, TASK-032 按归档后路径另判; 核对输出放进回报。

## Minor (去重后 17) 与处置

| 编号 | 内容 | 席位 | 处置 |
|---|---|---|---|
| m1 | owner_gates 自称每项写了未获授权时的处置, 13 项中 8 项没有; B.0 phase1_gate 认领推送与 AB 后重启会话未列; TASK-031 授权措辞缺「合并」 | TL m1 | 接受: 8 项补「未获授权 ⇒ 停在本步, 不进下游任务, 记台账」(TASK-034 另写本地合并与 tag 保持未推送); B.0 认领推送与 TASK-001 规划提交推送同批请授权, release_gate 推送保持与 Phase D 双推同批 —— 两类协调 ref 推送口径统一为「需授权, 同批请, 不另设等待点」; 补 AB 后以不带变量的新会话继续 (owner 启动动作); TASK-031 补「合并」 |
| m2 | TASK-026 工时 8h 已到上限, 条件性扩面 (phase-d-closer 追加 / 复跑) 无拆分规则 | TL m2 | 接受: 写明「TASK-024 落 phase-d-closer 编辑, 或需复跑的 eval ≥ 3 条 ⇒ 拆出独立 TASK (新编号, 工时另估, 依赖同 TASK-026)」 |
| m3 | TASK-035 补丁 3「可复用 TASK-017 副本」与副本生命周期、并行执行冲突; TASK-033 与 tasks.md 读前必看第 11 条的组 3 枚举漏 3.5 / TASK-035 | TL m3 · CR m10 | 接受: 改为「补丁 diff 可与 TASK-017 相同, 在本任务自己的副本上实跑」; TASK-033 改为「TASK-015..018 与 TASK-035」; 读前必看第 11 条改为「3.1–3.5」 |
| m4 | TASK-032 未写服务端合并 PR 后如何把本地 master 对齐 | TL m4 | 接受: TASK-032 开头补 `git fetch origin` → `git checkout master` → `git merge --ff-only origin/master` (不能快进 ⇒ 停下上报), 断言 HEAD 含 TASK-031 的合并提交 |
| m5 | 回落支下, phase-c-integrator 默认 rebase / squash 会让审计报告与台账引用的主仓 SHA 不在远端 master 上 | TL m5 | 接受: TASK-031 写明同步 origin/master 用 merge (不 rebase)、PR 以 merge commit 合并 (不 squash)、合并后核台账所记主仓 SHA 均为 origin/master 的祖先 |
| m6 | TASK-027 提交点未写分支、add 范围与 SHA | TL m6 | 接受: 与其余提交点同式; 提交后 `git -C aria show --stat HEAD` 恰含版本 5 文件 |
| m7 | (l1) 仍可被模块 docstring 顶部场景列表、Returns 分区里的「Never raises」段遮蔽 | CR m1 | 接受: 换为 CR 的 `l1x` (两处都只取「标题到第一个空行」的块); 新增 `bad_l1_module_scenarios` 与 `bad_l1_neverraises` 两态 (期望仅 (l1) FAIL) |
| m8 | (a2) 的三个新锚点未进 authoring_rules, 形状 dict 改用围栏代码块即假红 | CR m2 | 接受: authoring_rules 补 (a2) 书写约束 |
| m9 | (j4) 不看语境, authoring_rules 却写「描述排序键」; `4[- ]levels?` 缺左边界 | CR m3 · QA m1 | 接受: authoring_rules 改为「扫描面内任何语境都不用这些字样」; 正则加左边界 `(^|[^0-9a-z])(four|4)[- ]levels?` (配合 `-i`); 新增守卫态 `alt_j4_numeric` (现状句含 `14-level` 字样, 期望全 PASS) |
| m10 | 脚本 docstring 状态自检是子串匹配; 缺文件时 rc=1 而非 2; TASK-001 对 rc=1 的处置不区分差异来自模拟改动还是谓词 | CR m4 | 接受: 自检改为按行首状态名匹配; 源目录缺文件打印 usage 并返回 2, 其余未预期异常另设退出码; TASK-001 的 rc=1 口径改为「先判差异格来源, 放宽谓词须附三态实跑」 |
| m11 | 谓词原文两份 (yaml / 脚本), `--emit-json` 不输出谓词, 计划无一致性核验步骤 | CR m5 | 接受: `--emit-json` 增加 `predicates` 字段 (yaml 块行格式); TASK-001 与 TASK-029 第 7 步各加「yaml 谓词块与 `--emit-json` 的 predicates 逐字节一致」 |
| m12 | 补丁 5 的首个失败断言依赖 TASK-003 未规定的取行方式 | CR m7 | 接受: TASK-003 补「SC-8 后半按 `(branch, filename)` 取行, 取到后再断言 `rel_path`」 |
| m13 | TASK-001 在「B.1 基线」上跑脚本与谓词, 却没有检出基线并断言 HEAD 与工作树的步骤 | CR m8 | 接受: 跑脚本前补「aria feature 分支自 B.1 基线建好并检出, 断言 HEAD 等于基线 SHA 且 porcelain 为空」 |
| m14 | 以模块名调用的 unittest 命令没写 cwd; `check_bare_issue_refs.py` 扫导出的新增行时缺 `--repo-root` | CR m11 | 接受: 统一写成 `cd aria/skills/state-scanner/tests && python3 -B -m unittest <module>`; TASK-028 写明以 `--repo-root=<该仓根>` 调用 |
| m15 | TASK-011 移除 legacy 追加后, `:644` 的 `_get_file_commit_date` 调用失去消费者 | BA F2 | 接受: TASK-011 同批删除该调用 |
| m16 | writer `:140` 与 `:159` 有逐字相同的「仅在单 active track 场景下写真实指针」句, TASK-013 只点名 `:159` | BA F3 | 接受: 两处同步补子目录限定 |
| m17 | 读前必看第 14 条把 (h) 只归 4.4, SC 映射表写成 4.4 与「5.3 与 5.4」 | KM F3 | 接受: 读前必看改为「(h) 由 4.4 落地、5.4 周期 handoff 复述」; 映射表改为「5.3 (d) / 5.4 (d)(h)」 |

## Conflicted

| 项 | 分歧 | 主控裁决 |
|---|---|---|
| TASK-035 补丁 1 (PP3-M8) | BA: 补丁 1 使 SC-1 行消失而非变 legacy, 应比照补丁 5 窄化为「构造点 rel_path 退回 basename」。TL / QA: 补丁 1 与原句对得上 | **问题成立, 改法不采 BA**。SC-1 是 issue 主症状 (子目录件能被读成真 track), 它要抓的回归正是枚举层退回 basename; 把补丁换成构造点字段回退, 测的就变成 SC-8 的面, SC-1 的鉴别力反而没人证明。原句的「变 legacy」是 TASK-011 之前的表现形态, 用例在 TASK-011 之后仍全红, 缺的只是把新形态与所指断言写明 |
| TASK-029 步序 (PP3-M2) | TL: Major (占位检查恒真, 四态实跑)。CR / QA: Minor (只评了步序)。BA: 下游第 4 步兜底, 不构成 finding | **采 TL**: 恒真检查按严重度口径属 Major; CR / QA / BA 都没有检查第 4 步 grep 的对象是 master 工作树, 有实跑证据的一方胜 |

两项裁决均列入 AI 流程判断清单 (PP3-M6)。

## 跨簇一致性 (主控核对; 执笔人必须同批落)

1. **PP3-M1 与 m1 / PP3-M5**: 勾选合并到 TASK-032 后, TASK-026 / TASK-028 / TASK-032 / tasks.md 5.5 与 5.6 行 / 清单第 15 条同批改。5.5 行删去 WITHOUT_BETTER 与「勾选时替换」两处表述, 替换规则只留在 TASK-032。
2. **PP3-M2 / M3 / M4 都改 TASK-029 / 034**: 修改后逐条列出 TASK-029 的步序, 并核对:
   - 每一步的前置条件在上一步结束时成立;
   - 每条「停下上报」都能在 owner_gates 里找到对应项;
   - 回退条的前置 (`HEAD^1` / `HEAD^2` / 工作树干净) 在调用它的每个位置都成立 —— 合并冲突时没有合并提交, 所以第 5 步失败走 `merge --abort`, 不走回退条。
3. **PP3-M7 与 m7 / m9 / m10 / m11**: 谓词与验证态的改动一次改齐:
   - yaml 谓词块、脚本 `PRED`、EXPECTED、states / expected / 实测块、authoring_rules、归属注释、各 TASK「为真」声明;
   - 由脚本输出重生成, 不手改;
   - 每条新谓词先在 1cb3872 基线原文上实跑为 FAIL。
4. **PP3-M6 与本轮全部处置**: 执笔人最后逐条过一遍本表, 凡属「跳过 / 降级 / 改序 / 替代」的, 在清单里都有对应条目。
5. **R4 处置原则 3**: 本轮新增的每条机械检查, 在回报里写明其自然红态出现在哪里。

## 席位准确性备注 (不计 finding)

- **knowledge-manager 席**:
  - frontmatter 计 3m, 正文只列出 2 条 Minor (F2 / F3);
  - 若干行号引用与实际不符 (如称清单第 13–18 条在 tasks.md:66-71, 实为 :51-56; 称 TASK-026 在 yaml:448-461, 实为 :675 起);
  - 「本轮 Major 数为 1, 相对 R2 大幅下降」是单席计数, 不是聚合口径。
- **backend-architect 席**: 判 TASK-029 第 2 / 4 步「低风险, 不构成 finding」时, 没有检查第 4 步 grep 读的是 master 工作树 (见 Conflicted)。

## 主控自查

- **PP3-M1 有一半出自主控**: v3.1 核验时要求 TASK-031 改为有范围核验, 却没有连带检查「本 cycle 交付物路径」里最常被改的 tasks.md 在什么时点提交。与 memory `fixes-contradict` 同形 —— 单条改法对, 与另一条 (5.6 即勾) 的隐含前提冲突。
- **PP3-M6 也有一部分出自主控**: v3.1 返修指令只要求更新清单第 12 条, 没要求把 TASK-031 的放宽列为新条目。
- **R4 起执笔前后的核验要求**: 除原有的机械核验与自建坏态外, 增加两项 —— 对 TASK-029 / 034 的新步序在临时仓跑一遍状态模拟; 对清单完整性逐条对照本表。

## 收敛判断与 R4 安排

R3 不收敛 (9 Major, Vote REVISE 5)。继续 R4 (max_rounds 5 的第 4 轮):

- **执笔**: 由 v3 执笔人 (同一实例, 保留全部上下文) 按本报告与 R4 处置原则修订三份文件; 只改三份文件, 不提交, 不派子代理。
- **主控**: 核验 (机械核验 / 自建坏态 / git 步序临时仓模拟 / 清单完整性 / 逐任务删改) 通过后提交, 再以新派五席进 R4。
- **R5 仍未收敛**: 按降级策略请 owner 三选一。

## 席位报告

同目录 `post_planning-R3-2026-09-15T212707-499Z-handoff-multibranch-subdir-path-fidelity-{tech-lead,backend-architect,qa-engineer,code-reviewer,knowledge-manager}.md`

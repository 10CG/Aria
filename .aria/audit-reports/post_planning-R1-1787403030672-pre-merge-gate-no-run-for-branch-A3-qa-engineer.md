---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-22T13:01:16.470Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/detailed-tasks.yaml
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A3-qa-engineer
critical_count: 0
major_count: 3
minor_count: 2
---

## 摘要

席位 A3 (qa-engineer) 透镜 = SC 覆盖逐字对照 (焦点2) + TDD RED/GUARD 顺序与可证伪性 (焦点3)。已读 proposal.md 全文 (v7, 310 行) + detailed-tasks.yaml 全文 (17 任务)，并对基线 aria@9e6a17c 做了 4 处实跑抽样 (非静态读码):

```
SC-1 baseline _normalize_pr_ci_status([]) = "pending"          (期望 not_found) → 红 ✓
SC-2 baseline compute_verdict([], "not_found").verdict = "green"                 → 红(基线green) ✓
SC-4 baseline compute_verdict([{run_id:1}], "not_found") = verdict"wait" gate_error=None → 红在kind ✓
SC-6 baseline compute_verdict([], "not_applicable", pc=...).gate_error = None    → 绿(守卫) ✓
hasattr(pmg, "_verify_branch_exists")      = False  (新名不存在 → SC-5/10 RED 的 AttributeError 前提成立)
hasattr(pmg, "_verify_main_branch_exists") = True   (旧名仍在, 包装先例成立)
```

四条基线断言与 proposal SC 表、TASK-002/004 的 RED/GUARD 标注**逐字一致，无漂移**。checklist_s7_mapping 的 4 项 (TASK-007/012/014/008) 落点原文核对**全部命中**，无蒸发。SC-1~16 每条在 sc_coverage_crosscheck 中都至少有一条承载 task，未发现整条 SC 零承载的 Critical。

但在**子条款级**核对中发现 3 处 Major (SC-3 跨路径回显断言 / SC-11(d) reset 成功路径断言 / INV-5 检查点未复制到 TASK-011) 与 2 处 Minor (TASK-007 conditional-skip 对下游依赖解析的语义未声明 / SC-15 跨任务绑定的隐性耦合未落显式约定)。均为「摘要归纳时漏了 SOT 里的部分从句」类漂移，不改变整体架构或 SC 总覆盖判定，但若实施者只读 yaml 摘要不回读 proposal 原文，存在实际漏测风险。

## Findings

### [A3-qa-engineer-PP-M1] SC-3 跨路径回显断言未落任何 task
- **scope**: TASK-002 (承载 SC-3) / sc_coverage_crosscheck.SC-3
- **问题**: proposal SC-3 原文末句 ——「`compute_verdict` 与 `gate_check` 路径对同一 `cfg` 回显相同 `prompt_after_observations`」—— 是一条独立的跨入口一致性断言 (需要同一 cfg 分别走 `compute_verdict()` 直调与 `gate_check()` 端到端两条路径, 断言两者 `gate_error.prompt_after_observations` 相等)。TASK-002 标题只写「`_effective_prompt_threshold` 五 case + warn」, 对应的是 SC-3 前半句 (None→3 / 显式值→5 / 四类非法值+缺键→3 各自 warn) 的**纯函数级参数化测试**, 未提及这条跨路径一致性断言; TASK-005/006 (gate_check e2e 测试) 的标题/deliverables 也未提及。
- **实测**: 逐字重读 SC-3 全文 (proposal.md:266) 确认该句独立存在, 且未在 §2.2 描述中被其它 SC 隐式覆盖 —— `_effective_prompt_threshold` 作为「唯一校验点」是**设计手段** (AD-3/§2.2), SC-3 这句是对该设计手段的**验收断言**, 两者不能互相代替 (纯函数测试通过不能证明两条调用路径确实都在用同一份 cfg 走到同一个函数)。
- **建议**: 在 TASK-002 (或 TASK-005) 补一条测试: 构造同一非默认 cfg (如 `{"no_run_prompt_after_observations": 5}`), 分别调 `compute_verdict(..., cfg=cfg)` 与经 mock backend 走 `gate_check(..., config=cfg)` 到 not_found 分支, 断言两者 `gate_error["prompt_after_observations"]` 相等且均为 5。

### [A3-qa-engineer-PP-M2] SC-11(d) 的 reset 成功路径断言未出现在 TASK-008 枚举中
- **scope**: TASK-008 (title/deliverables/verification)
- **问题**: proposal SC-11(d) 原文包含两条 reset 成功路径断言 ——「`reset --observations` 后重读 obs=0 其余不变」「`reset --retry-count` 后 `started_at` 更新」—— 这两条是 CLI `reset` 子命令**正常工作路径**的验收点。TASK-008 title 的 CLI 部分逐项枚举为「文件缺失起步 / 独立重读落盘 / wait→waiting / --intervals / telemetry source=test + ts ISO / --threshold should_prompt / 透传 in-flight-runs+raw-message / **缺 --source 或 --state-file exit 2** / **reset·clear 缺失文件 exit 2** / record verdict≠wait 缺失文件 exit 2」—— 列出的全部是**失败/边界路径** (exit 2 各分支), 唯独 `reset` 子命令本身「成功执行、字段确实按预期改变」这条最基本的正向断言未被枚举; deliverables/verification 同样未提及。
- **实测**: 与 TASK-008 verification 逐句核对 (「基线红...; 既有22绿; 坏实现...在独立重读断言各自红」) 确认这两条正向断言不在其列。虽然 title 开头写「SC-11 (a)-(d) 测试先落 (RED)」是概括性全称声明, 但该任务对其余 8+ 项子断言都做了逐项摘录, 唯独漏了 `reset` 的两条正向路径 —— 与本 memo 关注的「past-summary not measurement」/「fix-the-class」模式一致: 摘要式转录习惯性地只抄了「坏路径」那一半。
- **建议**: 在 TASK-008 title 或 deliverables 显式补上「`reset --observations`/`reset --retry-count` 正向路径断言 (含 `started_at` 更新)」, 避免实施者以 yaml 摘要为准而漏测。

### [A3-qa-engineer-PP-M3] INV-5 检查点只复制到 TASK-010, 未复制到实际承载处方文本的 TASK-011
- **scope**: metadata.invariants[INV-5].encoded_as ("TASK-010/011 文档面措辞") vs TASK-010/TASK-011.verification
- **问题**: INV-5 (「AI 不自动执行处方」设计收缩, owner 2026-08-22 复议接受) 的 `encoded_as` 字段列了两个任务 (TASK-010 与 TASK-011), 但只有 TASK-010 的 verification 显式写了「INV-5: 文本零处出现自动 dispatch/commit 指令; prompt 定义只有一处 (§C.2.4 处方段被 2.5 引用)」。而按 proposal §3.3 (「no-run prompt (一处定义, §C.2.4 步骤 6 与 workflow-runner 2.5 共同引用)」), 处方文本 (a)(b)(c) 三选一段落的**唯一物理落点**是 `phase-c-integrator/SKILL.md §C.2.4` —— 这恰是 TASK-011 的 deliverables, 不是 TASK-010 的 (workflow-runner/SKILL.md 只是**引用**该定义, 见 §3.2 步骤 2.5 "定义一次，见3.3")。TASK-011 verification 只写了 SC-14 grep 断言与 traps 「不能靠读代码想出来」标准, 没有对处方文本本身重复 INV-5 的「零自动执行指令」检查。
- **实测**: 对照 §3.3 原文与 §3.4 表 (文件-位置-改动映射), 处方段落三选一文字 (「处方 (择一, 由你执行; AI 不自动执行)」) 归属 `phase-c-integrator/SKILL.md :252-263`, 与 TASK-011 deliverables 第一项完全对应; TASK-010 deliverables 是 `workflow-runner/SKILL.md` 等四个文件, 均不含该段落原文。
- **建议**: 在 TASK-011 verification 补一条与 TASK-010 对称的 INV-5 检查 (「§C.2.4 处方段文本零处出现自动 dispatch/commit 指令, 且 (a)/(b)/(c) 均标注需人执行」), 否则唯一真正定义处方文字的任务反而缺这道审计点, 只有引用方在查。

### [A3-qa-engineer-PP-m1] TASK-007 conditional_on=skipped 时下游依赖解析语义未声明
- **scope**: TASK-011.dependencies / TASK-013.dependencies (均含 TASK-007)
- **问题**: INV-3 规定 `TASK-001.dispatch_viable=false` 时 TASK-007 「整任务... 标 status: skipped」。但 TASK-011 (`dependencies: [TASK-006, TASK-007]`) 与 TASK-013 (`dependencies: [..., TASK-007, ...]`) 都把 TASK-007 列为硬依赖, yaml 未说明「依赖一个 status=skipped 的任务」在执行框架里算「已满足」还是会阻塞下游排期。若 `dispatch_viable=false` 是较可能出现的分支 (F6 显示该 Forgejo 版本连 `/actions/runs` 都 404, dispatch 可用性本身就存疑), 这条语义空白在 B.2 执行时会被撞到。
- **建议**: 在 INV-3 的 `encoded_as` 或 TASK-011/013 的 `notes` 补一句「TASK-007 status=skipped 视为依赖已满足, 不阻塞下游」, 避免执行期臆断。

### [A3-qa-engineer-PP-m2] SC-15「test_case_in_unit_tests 绑定到 SC-2 trigger-matched 用例」的跨任务耦合未落显式约定
- **scope**: TASK-002 (exec_order 2, 产出用例) ↔ TASK-012 (exec_order 12, 引用该用例)
- **问题**: proposal SC-15 要求 `NEG-4-no-run-for-branch.json` 的 `test_case_in_unit_tests` 字段绑定到「SC-2 的 trigger-matched 用例」。这意味着 TASK-002 产出的 parametrize 测试用例需要有一个跨 10 个任务、跨约 3h 执行距离仍可被精确引用的稳定标识 (如 pytest `ids=[...]` 或独立测试方法名), 但 TASK-002 的 deliverables/verification 都未要求「该用例需具名/稳定可引用」。这是一处隐性耦合: 若 TASK-002 实现时把 6 档+None 写成匿名 `parametrize` 元组 (无 `ids=`), TASK-012 要精确指向「trigger-matched 那一档」会需要额外返工。
- **建议**: 在 TASK-002 deliverables 补一句「参数化用例含显式 `ids`（至少 trigger-matched 档可被稳定引用）, 供 TASK-012 SC-15 绑定」。

## 已核验无误

- sc_coverage_crosscheck 全部 16 条 SC 均至少有一条承载 task, 无整条 SC 零承载。
- checklist_s7_mapping 4 项经原文逐字核对全部命中且落点准确 (TASK-007.verification / TASK-012.title+notes / TASK-014.notes / TASK-008.notes)。
- INV-1 (同 commit 约束) 在 TASK-003 verification 显式核 `git show --stat` 双文件, TASK-002 是其唯一前置 —— 与 encoded_as 逐字一致。
- SC-1/SC-2/SC-4/SC-6 的 RED/GUARD 标注对基线 9e6a17c **实跑**验证全部一致 (见摘要代码块), 无一处方向或字段级错误。
- SC-5 (c1)(d) / SC-2 「6 档+None」/ SC-5 (c2) 条件转移到 TASK-007 —— memo 特别点名的三处均逐字核对**无漏项**, 顾虑不成立。
- TASK-005/006 的 RED 依据 (`_verify_branch_exists` 新名基线不存在, `_verify_main_branch_exists` 旧名仍在) 经 `hasattr` 实测确认成立。
- 两条 parallel_tracks (gate 轨 TASK-002~007 / helper 轨 TASK-008~009) 文件域经交叉核对确系 disjoint (phase-c-integrator vs workflow-runner 两个 skill 目录), 无隐藏交集。
- RED→GREEN 依赖顺序全图 (TASK-002→003, 005→006, 008→009 等) 无一处方向颠倒或 GREEN 先于 RED。
- TASK-012 对 Rule #6 判据表第三行的三义务 (点名行为/定向fixture/套件缺口issue) 逐字对应 rule6_note, 无缺项; TASK-014 对 SC-13 全部步骤 (含证据先抄录后 clear 的顺序、state 文件与 gate cwd 分离) 转录忠实, 无字段级漂移。

## Verdict

PASS_WITH_WARNINGS — vote: REVISE

无 Critical (SC 覆盖骨架完整、基线 RED/GUARD 标注实测无误), 但 3 处 Major 子条款级转录漏项需在下一版 yaml 中补齐 (均为在已承载 SC 内部漏掉部分从句, 而非整条 SC 零覆盖), 故投 REVISE。

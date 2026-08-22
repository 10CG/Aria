---
checkpoint: post_planning
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: "2026-08-22T16:01:07.000Z"
context: openspec/changes/pre-merge-gate-no-run-for-branch/detailed-tasks.yaml
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A4-code-reviewer
critical_count: 0
major_count: 0
minor_count: 4
---

# post_planning R5 (稳定性确认, owner 加轮 4→5) — A4 code-reviewer

## 摘要

实读 proposal.md v7 全文 + detailed-tasks.yaml v5 全文 (506 行); 复跑 R4 机械脚本 (`scratchpad/check_yaml_v4.py`) 对 v5: total_tasks 20 ✓ / estimated_hours 51 = 逐任务求和 51.0 ✓ / parent 8 ✓ / exec_order 0..19 唯一且每条 > 其全部 dependencies ✓ / 无悬空依赖 ✓ / TASK-003 下游闭包 **12** (005/006/007a/007b/010a/010/011/013/012/014/015/016) = `exec_order_note` 现写「12 项」✓ (R4 A2-M2 closed) / 010a ∈ 010 与 011 直接依赖 ✓ / `carries_sc` ↔ `sc_coverage_crosscheck` 双向一致 ✓ / `agent_summary` 四 agent ↔ tasks.agent 逐一相等 (qa 6 / be 4 / km 2 / main-loop 8) ✓ / status 全 pending ✓ / reason 全非空 ✓ / parallel_tracks gate 轨 exec 3..9, helper 轨 10..13 ✓ / `execution_order` 四行文本的依赖叙述与 dependencies 逐条同 (005 需 003 · 006 需 003+001 · 010a/010 需 003 · 011 需 006/007b/010/010a/001 · 013 需 011 · 012/014 需 013) ✓。

代码/命令锚点实测 (aria @ 9e6a17c): **INV-1 v5 命令形式**本席在主仓根亲跑 — `inv1 9e6a17c pending` → exit 0; `inv1 9e6a17c not_found` → `AssertionError: pending`, exit 1 ✓ (正向过、反向非零退出, 判别力成立; 与 A1/主控实跑一致)。**基线 `compute_verdict` 签名** (`pre_merge_gate.py:174-180`) 已含 `cfg=None` / `path_coverage=None` 形参 ⇒ SC-2 用例在 9e6a17c 能走到断言 (verdict==green), 非 TypeError ✓ — SC-15 v5 红窗「拷入当前 tests/ 后断言失败」的前提成立。**测试模块导入风格** `test_pre_merge_gate.py:26` `import pre_merge_gate as gate` (非 from-import 名单) ⇒ 新名以 `gate.xxx` 引用时模块在基线可 import ✓ (但见 m2: mixin `patch.object` 新名桩是唯一能把红从「断言」退化成「setUp 错误」的位置)。**path_coverage 仓根 = cwd** (`path_coverage.py:17/:106`) + `.forgejo/workflows/` 仅 `issue-triage-tests.yml` 一个 workflow (push/pull_request paths `skills/issue-triage/**` + `workflow_dispatch: {}`) ⇒ TASK-014 基于 feature HEAD 的 probe 分支, `master...probe` diff 含 feature 改动 + issue-triage 变更, 仍落 `workflow-trigger-matched`, 首推零 run 形态不变 ✓。**v5 新引用** (R4 A1-PP4-M1 / A1-m2 / A1-m5 / A1-m6 / A2-m1 / A3-M1 / A3 逐条实核 / A4-M1 / A4-M2 / A4-m2 / A4-m3 / R3 A5-M1) 逐一对应 R4 各席报告真实锚点与主题 ✓。

归我席 R4 5 条 (M1 / M2 / m1 / m2 / m3) 在 v5 **5/5 closed** (证据见处置表)。v5 diff 新鲜眼睛**未发现满足 Major 门槛的矛盾**: 无 spec 不变量违反、无 SC 失承载、无 TDD 红绿失效、无实施者必然分叉。残余 4 条 Minor (「还能挑」): 一处 execution_order 措辞残留、一处 SC-15 红窗的前置加固提示 (TASK-005 mixin 桩)、一处 TASK-014 gate cwd 二选一的提交时序提示、一处「返回串」措辞。

## R4 处置核对

| R4 条目 (本席) | v5 处置 (聚合表) | R5 实核 | 状态 |
|---|---|---|---|
| A4-PP4-M1 TASK-016 「.replace 三行」 | 只删 `.replace(...)` 调用本身 | L454 现写「§2.1 末段的 `.replace(\"<pr_branch>\", …)` **调用本身** (…只删 .replace 调用, 不删行)」; 与 TASK-006 conditional_parts (L208)「其余 (…verify_note/raw_message 同步) 无条件」一致; 删调用后 proposal L94 退化为 `m = out["gate_error"]["message"] + verify_note`, L95 重同步保留, `verify_note` 不成死变量 ✓ | **closed** |
| A4-PP4-M2 TASK-014 worktree「同 TASK-001」基于 9e6a17c ⇒ gate 跑基线得 pending | worktree 基于 feature HEAD | L403 「worktree **基于 feature 分支 HEAD** 建 — 非 9e6a17c: gate/path_coverage 按 cwd 取仓根, 基线树跑出的是 pending」; 「同 TASK-001」字样已无 (grep 0); `<tmp>` 与 `aria/` 两根均含实现, 分叉消除 ✓ (残: 提交时序见 m3) | **closed** |
| A4-PP4-m1 TASK-011 title 残留「SC-14 机检脚本/断言」 | 清理 | L336 末尾现为「(SC-14 脚本已归 TASK-010a, 本任务只让其翻绿)」✓; deliverables 无测试文件 ✓; verification[3] 指 010a 翻绿 ✓ | **closed** |
| A4-PP4-m2 TASK-012 红窗恒「收集错误」+ reason「独占」 | 拷入当前 tests/ → 断言失败; reason 改措辞 | L376 「`worktree add <tmp> 9e6a17c` 后拷入当前树的 `skills/phase-c-integrator/tests/` … → **断言失败** (verdict==green, 非收集错误) = 真红; 用后 worktree remove」✓ (无 -b, 无分支残留); reason L368 改「红窗核验用独立 worktree, 置于 013 全量之后以免 AB 跑与全量 pytest 互扰」✓。基线 compute_verdict 签名实核可达断言 ✓ | **closed** (execution_order 残一处旧词 → m1) |
| A4-PP4-m3 probe 分支 `worktree remove` 后残留 | 001/014 补 `branch -D` + 三断言 | TASK-001 L108 「`git -C aria worktree remove` + `git -C aria branch -D probe/152-dispatch`; 结束断言: `worktree list` 不含 tmp, 本地与远端 probe/* 为空」✓; TASK-014 L403 「`worktree list` 不含 tmp + `branch -D probe/…` + 远端 probe/* 为空」✓; 恒真的 show-current 断言已撤 (A1-m6) ✓ | **closed** |

r4_closed = 5, r4_partial = 0, r4_not_addressed = 0。

## Findings

### [A4-code-reviewer-PP5-m1] `execution_order` 汇合行仍写「回退核验**独占**工作树」, 与 TASK-012 reason 的 v5 新措辞不同步 (fresh, 措辞残留)

- **锚点**: L499 「→ TASK-012 (Rule #6, 回退核验独占工作树, 需 013)」 vs TASK-012 reason L368 「红窗核验用独立 worktree, 置于 013 全量之后以免 AB 跑与全量 pytest 互扰」。
- **实测**: grep `独占` 全文仅此一处; worktree 方案下主工作树不被占用, 「独占」已是 R4 m2 撤掉的旧理由。
- **后果**: 纯描述性 (依赖边 012→013 本身正确且机检), 无字段级语义改变。
- **建议**: L499 改「TASK-012 (Rule #6, 红窗在独立 worktree, 需 013)」。

### [A4-code-reviewer-PP5-m2] SC-15 红窗「断言级红」的前置条件只在消费端 (TASK-012) 与 TASK-002 写了, TASK-005 的 mixin 新名桩是唯一能把它退化成「setUp AttributeError」的生产者, 未带提示 (executability, 加固)

- **锚点**: TASK-005 deliverables L191 「mixin :85-89 加新名 `_verify_branch_exists` 桩 默认 ('ok','')」; TASK-012 verification L376 「→ 断言失败 (verdict==green, 非收集错误) = 真红」; TASK-002 verification L152 「SC-2 的红是 verdict==green (不是 AttributeError)」。
- **实测**: `:85-89` 的桩位于 `_ProbeCacheResetMixin.setUp` (`test_pre_merge_gate.py:59/:75`), 该 mixin 被文件内几乎所有测试类继承 (GateCheckTests / FallbackTests / PathCoverageGateTests …)。若 TASK-005 按既有形态写 `mock.patch.object(gate, "_verify_branch_exists", return_value=("ok",""))` (无 `create=True`), 在 9e6a17c 基线 worktree 里 `gate` 模块无此属性 ⇒ 任何继承该 mixin 的类 (含 NotFoundVerdictTests, 若它也继承) 在 setUp 抛 AttributeError — 红落在 error 而非断言。TASK-002 时 (005 未落) L152 能过; TASK-005 时 (003 已落) 一切绿, qa-engineer 无从察觉; 要到 TASK-012 红窗才暴露, 然后回头改 005 的桩。
- **为什么不是 Major**: TASK-012 verification 已显式要求「断言失败 (非收集错误)」, 错形状会**发红**而非假绿 (无 fail-open / 无 SC 失承载); 只是可预见的晚期返工。
- **建议** (一短语, TASK-005 notes): 「新名桩用 `create=True` (或 NotFoundVerdictTests 不继承该 mixin), 保持 SC-2 用例在 9e6a17c 基线能跑到断言 — SC-15 红窗 (TASK-012) 前提」。

### [A4-code-reviewer-PP5-m3] TASK-014 「gate (aria-plugin 根)」在 feature-HEAD worktree 方案下有两个等价根, 选 `<tmp>` 时隐含「feature HEAD 已含 003/006/009 提交」, 提交时序未钉 (executability)

- **锚点**: TASK-014 title L403 「gate (aria-plugin 根)」+「worktree 基于 feature 分支 HEAD 建」; parallel_tracks.note L493 「子 agent 不 commit, 主控统一提交」。
- **实测**: worktree 取的是 **HEAD 提交**, 不含 `aria/` 工作树未提交改动。003 的提交在 014 前必然存在 (TASK-013 INV-1 `git show <c>` 以其为前提); 006 (PR 分支核验) / 009 (CLI) 的提交时点 yaml 未钉。即便 006 未提交, `<tmp>` 根跑 gate 仍得 `not_found` + kind (003 已在) ⇒ SC-13 结论不变; 差别只在是否多付一次 ls-remote。CLI 由 workflow-runner 路径按 `aria/skills/workflow-runner/scripts/...` 调用, 走 `aria/` 工作树, 与 `<tmp>` 无关。
- **建议** (择一): 钉 「gate cwd = `aria/` 工作树 (worktree 仅用于构造/首推 throwaway 分支)」, 或在 014 notes 加「执行前主控已提交 003–011」。

### [A4-code-reviewer-PP5-m4] TASK-013 verification[2] 「调 `_no_run_gate_error` **返回串**含 '/dispatches -d'」— 该函数返回 gate_error dict, INV-3.encoded_as 写的是「返回的 message」(措辞)

- **锚点**: L397 vs INV-3.encoded_as L40 「返回的 message 含 '/dispatches -d'」; proposal §2.2 L110-111 `gate_error = _no_run_gate_error(...)` / `gate_error["message"]`。
- **后果**: L397 自引「见 INV-3.encoded_as」, 实施者以 INV-3 为准; 无分叉。
- **建议**: L397 「返回串」→「返回 dict 的 message」。

## 已核验无误

- **yaml 自洽终态**: 20 / 51h / exec_order 唯一且 > 依赖 / 003 闭包 12 = `exec_order_note` / crosscheck 双向 / agent_summary 双向 / execution_order 文本 vs dependencies / parallel_tracks 轨序与轨名 (helper 轨「+ 010a 的新建测试文件」与 010a deliverable `test_doc_sync_no_run.py` 为新文件、与 005/007a 改的 `test_pre_merge_gate.py` / `test_path_coverage.py` 文件级 disjoint) — 全绿。
- **INV-1 v5 命令**: 本席亲跑正向 exit 0 / 反向 exit 1 (见摘要); 「历史 aether.py 与当前树 base.py 组合, 本 spec 不动 base.py」与 proposal L31 代码落点 (无 base.py) 一致 ✓; TASK-013 verification[1] 引用 INV-1.encoded_as, 一处定义 ✓。
- **INV-3 对偶 (R4 A1-m2)**: L40 true 分支改为断言 `_no_run_gate_error(trigger-matched pc 含 dispatchable, 3)` 渲染结果含 `/dispatches -d`, 与 TASK-013 L397 同向 ✓; 签名 `(path_coverage, threshold)` 与 TASK-003 title / proposal §2.2 一致 ✓; false 分支 (006 不引入 .replace / 003 不渲染 dispatch 行 / 011 三项不写) 下 pattern 0 命中 + `<pr_branch>` 0 仍可达 ✓。
- **TASK-010a 六条断言 + 去 009 依赖**: title 六条 (五条 SC-14 + DEFAULT_CONFIG) 与 verification L308 「前五条红 / 第六条绿 (003 已落)」一致; dependencies [TASK-003] 仅此 ✓ (009 已去, 六条无一涉 helper); 第六条不在 SC-14 但由 010 的 config-template-key-currency 探针语义派生, TASK-011 L352 仍只列 SC-14 五条, 不矛盾 ✓; 五条在 003/009 落后仍红 (各由 010/011 翻绿) ✓。
- **TASK-016 conditional_parts 全清单** 与 §3.5 九项 + Impact/L31/R-c 提及逐项对得上 (R4 已核; v5 仅改第 9 项措辞) ✓; TASK-006 ↔ TASK-016 对 §2.1 末段条件范围陈述现一致 ✓。
- **TASK-001 / TASK-014 收尾**: 三断言 (worktree list / 本地 probe/* / 远端 probe/*) 两任务同形 ✓; 012 的 worktree 无 -b, 不需 branch -D ✓; 三写者顺序 (001 建节 → 011 上方四行 → 014 末尾 + :241) 与 L114 / L336 / L418 一致 ✓。
- **metadata.post_planning**: rounds_so_far 4 + owner 裁定「选 [2] 加 1 轮 (max_rounds 4→5)」与 R4 聚合 degradation 三路径一致 ✓; planned_by v5 描述与聚合 5 簇一致 ✓。
- **陈旧引用**: 无对 1.66.3/1.66.4 作 target 的引用; target_version 1.66.5 / baseline 9e6a17c (v1.66.4) / 补 tag v1.66.4@9e6a17c + v1.66.1@3b97c35 ✓ (R4 实核不变)。

## Verdict

**PASS** — vote **PASS**。

- **必须改**: 无 (零条满足 Major 门槛)。
- **还能挑** (minor, 可随 B.1 顺手, 不阻塞): m1 L499 「独占」→「独立 worktree」; m2 TASK-005 桩加 `create=True` 提示 (保 SC-15 红窗断言级红, 避免 TASK-012 时返工 — 四条里最值得顺手的一条); m3 TASK-014 钉 gate cwd = `aria/` 或提交时序; m4 L397 「返回串」措辞。
- R4 归我席 5/5 closed; v5 机械自洽全绿; INV-1 v5 命令本席亲跑成立; v5 新增句子未引入 R4 同形的「修一处坏一处」缺陷。v5 可进 B.1。

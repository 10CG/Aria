---
checkpoint: post_planning
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: "2026-08-22T15:05:00.000Z"
context: openspec/changes/pre-merge-gate-no-run-for-branch/detailed-tasks.yaml
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A4-code-reviewer
critical_count: 0
major_count: 2
minor_count: 3
---

# post_planning R4 (末轮) — A4 code-reviewer (R3 簇 #1/#5/#6 核对 + yaml 自洽 + v4 diff 新鲜眼睛)

## 摘要

实读 proposal.md v7 全文 + detailed-tasks.yaml v4 全文; 脚本机械核 (`scratchpad/check_yaml_v4.py`): total_tasks 20 ✓ / estimated_hours 51 = 逐任务求和 (51.0) ✓ / parent 8 ✓ / exec_order 0..19 唯一且每条 dependencies 的 exec_order 均小于自身 ✓ / 无悬空依赖 ✓ / TASK-003 下游闭包 **12** (005/006/007a/007b/**010a**/010/011/013/012/014/015/016; `exec_order_note` 仍写 11 项 — A2-PP4-M2 已报, 不重复) ✓ / 010a ∈ 010 与 011 的直接依赖 ✓ / `carries_sc` ↔ `sc_coverage_crosscheck` 双向一致 (含 010a「SC-14 RED」↔ `"TASK-010a (RED 脚本)"`) ✓ / `agent_summary` 四 agent ↔ tasks.agent 逐一相等 (qa 6 / be 4 / km 2 / main-loop 8) ✓ / status 全 pending ✓ / reason 全非空 ✓ / parallel_tracks gate 轨 exec 3..9, helper 轨 10..13 ✓ / `execution_order` 四行文本与 dependencies 逐条同 (005 需 003 · 006 需 003+001 · 010a/010 需 003 · 011 需 006/007b/010/010a/001 · 013 需 011 · 012 需 013 · 014 需 013) ✓。

代码/环境锚点实测 (aria @ 9e6a17c, 主仓 master): **负控 pattern** `grep -rn -E 'DISPATCH_VIABLE|dispatchable_workflows|/dispatches -d'` 限 phase-c-integrator/{scripts,tests,SKILL.md} + workflow-runner/{scripts,tests,SKILL.md} → **0 命中 (exit 1)** ✓; 对照裸 `dispatches` 仍 1 命中 (`submodule-tripwire-audit.sh:6`, 已被新 pattern 排除) ✓; `pre_merge_gate.py` 中 `<pr_branch>` 0 ✓; `_no_run_gate_error` 基线不存在 (true 分支对偶目标由 007b 建) ✓。**3b97c35**: `git log -S'"version": "1.66.1"' -- .claude-plugin/plugin.json | tail -1` = `3b97c35 chore(release): #128 v1.66.1`, `show 3b97c35:plugin.json` version=1.66.1, 是 9e6a17c 祖先 ✓; 两 remote ls-remote tags 仍只有 v1.66.0/.2/.3 (v1.66.1 与 v1.66.4 缺) ✓。**版本点**: 主仓已在 1.66.4, `CLAUDE.md:139,:141` / `VERSION:24` / `README.md:8,:242` / i18n ×3 各 3 (含 translated-from) = 14 行号全中 ✓。**TASK-001 探针**: `.forgejo/workflows/issue-triage-tests.yml` push/pull_request paths = `skills/issue-triage/**` 且含 `workflow_dispatch: {}` ✓。**SC-14 红窗**: SKILL.md `pr_ci_status` 枚举行 :180/:276 基线无 `not_found` (仅 :288 归层注记提到) ✓; `path_coverage.py:36` 仍「共 9 个」✓; `test_spec_complete.py:94` `parents[4]` + `:98` `_require_meta_archive` 先例 ✓。**SC-15 红窗机制**: `test_pre_merge_gate.py:24` 用 `sys.path.insert(0, dirname(__file__)/../scripts)` 相对导入 ⇒ worktree 内跑基线测试文件只能得「收集错误」(见 m2)。

归我席三簇 (#1 A4-M1 / #5 A4-m1 / #6 A4-m2·m3·m4) 在 v4 **5/5 closed** (证据见处置表)。新鲜眼睛抓到 **两条 Major, 都是 v4 为修 R3 而新写的句子自身引入的** (memory `fix-recurs-in-fallback` / `marginal-return-negative` 同形): (M1) TASK-016 把 §3.5 第 9 项「§2.1 末段的 `.replace`」转录成「`.replace` **三行**」— 那三行 (proposal L93-95) 同时承载无条件的 `+ verify_note` 后缀与 `raw_message` 重同步, 与 TASK-006 conditional_parts「verify_note / raw_message 同步无条件」直接矛盾; (M2) TASK-014 「worktree 方式同 TASK-001」把活体 throwaway 基于 **9e6a17c** 建树, 而 SC-13 要实测的是**本 spec 实现后**的 gate — 在该 worktree 根跑 gate = 跑基线脚本 ⇒ `pending` 而非 `not_found`, 实施者分叉且可能把实现误诊为失效。两条都是一短语可修。另 3 条 Minor (「还能挑」)。

## R3 处置核对

| 簇 | R3 条目 (本席) | v4 处置 (聚合表) | R4 实核 | 状态 |
|---|---|---|---|---|
| #1 | A4-PP3-M1 负控 `grep dispatches` 基线 1 命中 + F6 行必命中 ⇒ 恒红 | pattern 换 `DISPATCH_VIABLE\|dispatchable_workflows\|/dispatches -d` 限 6 路径, references/ 豁免; 基线实测 0; 加 `<pr_branch>` 0 与 true 对偶 | INV-3.encoded_as (L37) 与 TASK-013 verification[2] (L394) 同句改写 ✓; 本席实跑基线 **0 命中 (exit 1)**, 裸 `dispatches` 对照 1 命中被排除 ✓; `<pr_branch>` 计数 0 ✓; true 对偶 `_no_run_gate_error 含 '/dispatches -d'` 与 §2.3 处方行字面 (`…/dispatches -d '{"ref":"<pr_branch>"}'`) 一致 ✓; false 分支下条件组 (002 notes / 005 notes / 003 notes「不渲染 dispatch 行」/ 006 conditional_parts / 011 conditional_parts 三项) 均不产出这三个 token ⇒ 0 可达 ✓; traps F6 行在 references/ 豁免内 ✓ | **closed** |
| #5 | A4-PP3-m1 TASK-016 清单是 §3.5 真子集 (漏 `.replace` + `DISPATCH_VIABLE` 各处提及) | conditional_parts 改 §3.5 全清单 | TASK-016 L451 现含 `.replace` 项 + Impact 两签名 + L31 + R-c 提及 ✓, §3.5 九项逐项对得上 (§4 / SC-8 / SC-9 / SC-2 子项 / SC-5 (c2) / 2.3 / 3.3 (a) / §2.1 .replace / DISPATCH_VIABLE 提及) ✓。残: INV-3.rule (L36) 括号清单仍是旧 9 项 (无 `.replace`), 但它自引「§3.5 清单」为源且执行字段是 TASK-016 ⇒ 不计; **新引入**「三行」措辞 → 见 M1 | **closed** (新错另计 M1) |
| #6 | A4-PP3-m2 throwaway 分支生命周期未写回到 feature | 001/014 用 `worktree add -b probe/… 9e6a17c` + 结束断言 show-current | TASK-001 L105: `git -C aria worktree add <tmp> -b probe/152-dispatch 9e6a17c` + `worktree remove` + `branch --show-current == feature/…` ✓ (001 不依赖 spec 代码, 基于 9e6a17c 正确); TASK-014 L400「worktree 方式同 TASK-001」+ show-current 断言 ✓ — 但 014 **需要已实现的 gate**, 「同 001」基于 9e6a17c 是新坑 → 见 M2 | **closed** (新错另计 M2) |
| #6 | A4-PP3-m3 schema_note「int」与 .5 矛盾 | 改「数值」 | L11 「estimated_hours 用数值 (int 或 .5, 无 validator)」✓; 总计 51 = 求和 ✓ (000/000b 0.5 + 001 1.5 + 010a 1.5 = 4 + 其余 47) | **closed** |
| #6 | A4-PP3-m4 v1.66.1 tag 目标占位 | 钉 3b97c35 | TASK-015 L422 「v1.66.1@3b97c35 (plugin.json 首次 =1.66.1 的 commit, R3 A4-m4 实核)」✓; 本席复跑 `-S` 与 `show` 均证实 ✓ | **closed** |

r3_closed = 5, r3_partial = 0, r3_not_addressed = 0。

## Findings

### [A4-code-reviewer-PP4-M1] TASK-016 把 §3.5「§2.1 末段的 `.replace`」转录成「`.replace` **三行**」— 那三行承载无条件的 verify_note 后缀与 raw_message 重同步, 与 TASK-006 conditional_parts 矛盾 (transcription; v4 修簇 #5 时新引入)

- **锚点**: TASK-016 conditional_parts (L451) 「**§2.1 末段 <pr_branch> .replace 三行** (R3 A5-M1, §3.5 第 9 项)」 vs proposal §3.5 (L198) 「§2.1 末段的 `<pr_branch>` `.replace` (占位符随 dispatch 行消失, 回填无对象; (c1) 的「不含占位」断言保留作守卫)」 vs TASK-006 conditional_parts (L205) 「仅 §2.1 末段 <pr_branch> .replace 回填随 dispatch_viable … 其余 (改名/包装/第七早退/**verify_note/raw_message 同步**) 无条件」。
- **实测**: proposal §2.1 伪码「末段」恰为三行 L93-95: L93 `if out.get("gate_error"):  # 回填占位 + 核验失败附注` / L94 `m = …message.replace("<pr_branch>", …) + verify_note` / L95 `out["gate_error"]["message"] = m; out["raw_message"] = m  # 副本通道保持`。§3.5 只点名 `.replace` 这个调用; 「三行」整删会把 `+ verify_note` (SC-5 (d) / SC-10 verify-failed 后缀, 无条件) 与 raw_message 重同步 (SC-5 (c1), 无条件) 一并从归档件删掉, 而 L80 `verify_note = ""` 哨兵与 L89-90 赋值仍留 ⇒ 归档后的 §2.1 伪码里 verify_note 成死变量, 与同文 SC-5 (d) / SC-10 / TASK-006 已实现的行为互斥 — 正是 INV-3.rule「归档件不得描述未实现能力」的对偶 (归档件漏描述已实现能力, Rule #3)。
- **为什么 Major**: 派生层改了 §3.5 第 9 项的字段级范围 (一个调用 → 三行), 且 yaml 内部 TASK-006 ↔ TASK-016 对同一段落的条件范围陈述相反; 执行 TASK-016 的 main-loop 读「三行」与读 §3.5 原文会得到不同删法 (实施者分叉)。
- **建议** (一短语): L451 改为 「§2.1 末段 L94 的 `.replace("<pr_branch>", …)` **调用** (仅该调用; 同段 `+ verify_note` 与 `raw_message` 重同步无条件保留, 与 TASK-006 conditional_parts 一致)」。

### [A4-code-reviewer-PP4-M2] TASK-014 「worktree 方式同 TASK-001」把活体 throwaway 基于 9e6a17c 建树, 而 SC-13 要实测的是实现后的 gate — 在该 worktree 根跑 gate = 跑基线脚本得 `pending`, 实施者分叉 (executability; v4 修簇 #6 时新引入)

- **锚点**: TASK-014 title (L400) 「aria-plugin throwaway 分支首推 path-matched 变更 → **gate (aria-plugin 根)** 实测 not_found + kind → … 再删分支 (**worktree 方式同 TASK-001**, 结束后 `git -C aria branch --show-current` == feature 分支)」; TASK-001 deliverables[0] (L105) `git -C aria worktree add <tmp> -b probe/152-dispatch **9e6a17c**`; proposal SC-13 (L276) 「gate 在 aria-plugin 子模块根执行 (throwaway 分支在 aria-plugin …)」。
- **实测**: `path_coverage.py:17/:106` 仓根 = **cwd** 的 `rev-parse --show-toplevel`, gate 脚本路径也随 cwd 所在树; worktree 与主工作树共享 refs 与远程, 所以 `git diff master...probe/…` / `aether ci status --branch` 在两个根都能跑。差别只在**脚本版本**: `<tmp>` (9e6a17c + 一个 issue-triage 改动) 里的 `pre_merge_gate.py` / `aether.py` 是基线 ⇒ `_normalize_pr_ci_status([])` 返 `pending`, 无 `gate_error` ⇒ SC-13 「实测 not_found + kind」必不成立; 只有在 `aria/` (feature 分支树, 含 003/006 实现) 根跑才得 `not_found`。TASK-001 基于 9e6a17c 没问题 (它不依赖 spec 代码, 只调 `aether ci status`), 把同一句复制到 014 就把前提丢了 (memory `fix-the-class` 反向: 同形处方对两个位置的前提不同)。
- **为什么 Major**: 「aria-plugin 根」在 worktree 方案下有两个候选 (`<tmp>` 与 `aria/`), yaml 没钉; 选 `<tmp>` 的实施者会得到与 SC-13 相反的结果并可能误诊为实现失效 (同 #147 当初「runner 停摆」误诊形状), 选 `aria/` 的才对 — 实施者必然分叉。且 014 是 SC-13 + SC-16 (b)(c) + INV-4 活体的唯一承载。
- **建议** (择一, 一短语): (a) TASK-014 的 worktree 改基于 feature 分支 HEAD: `git -C aria worktree add <tmp> -b probe/152-live feature/152-no-run-for-branch` (这正是 R3 A4-m2 原建议的起点), 则 `<tmp>` 与 `aria/` 两根都含实现; 或 (b) 保留 9e6a17c 起点但写死 「gate 脚本与 cwd = `aria/` (feature 工作树), worktree 仅用于构造/首推 throwaway 分支」。(a) 更稳 (不留两根分叉)。

### [A4-code-reviewer-PP4-m1] TASK-011 title 尾部仍写「+ SC-14 机检脚本/断言」, 脚本已迁 TASK-010a (fresh, 残留措辞)

- **锚点**: TASK-011 title (L333) 末尾 「… 预言句改指本 spec + SC-14 机检脚本/断言」 vs TASK-010a deliverables (L303) `tests/test_doc_sync_no_run.py` vs TASK-011 deliverables (L343-347, 五个文档文件, 无测试文件) 与 verification[3] (L352) 「TASK-010a 的 test_doc_sync_no_run.py 翻绿」。
- **后果**: knowledge-manager 读 title 可能再写一份脚本 (双写) 或困惑; deliverables/verification 已正确, 故仅 minor。
- **建议**: title 尾改「+ 使 TASK-010a 的 SC-14 断言翻绿」。

### [A4-code-reviewer-PP4-m2] TASK-012 红窗「收集错误」是恒红 (基线树本无该测试名), 判别力弱; reason 「独占工作树」在 worktree 方案下已不成立 (executability)

- **锚点**: TASK-012 verification[0] (L373) 「`git -C aria worktree add <tmp> 9e6a17c` 在基线工作树跑 test_case_in_unit_tests 指向的测试 → 红 (收集错误或断言失败)」; reason (L365) 「回退核验独占工作树, 置于 013 全量之后」。
- **实测**: 基线树的 `test_pre_merge_gate.py` 不含 `NotFoundVerdictTests::test_sc2_trigger_matched_message` ⇒ pytest 必报 "not found" (exit 4) — 任何不存在的名字都这样红, 不证明绑定的测试真检验了本 spec 行为。`test_pre_merge_gate.py:24` 用 `sys.path.insert(0, dirname(__file__)/../scripts)` ⇒ 把当前树的测试文件**拷进** `<tmp>/skills/phase-c-integrator/tests/` 再跑, 会 import 基线 scripts, 红落在断言 (verdict==green), 才是 SC-15 「回退后转红」的有效红。另: worktree 不占用主工作树, 「独占」理由已过时 (依赖边 012→013 本身无害, 保留即可)。
- **建议**: verification[0] 加「拷当前树 `test_pre_merge_gate.py` 入 worktree 同路径后跑, 红须为断言失败 (非收集错误)」; reason 改「回退核验在 013 全量绿之后做, 保证回退对照的『当前树』已是全绿态」。

### [A4-code-reviewer-PP4-m3] TASK-001 / TASK-014 `worktree remove` 后本地 probe 分支残留 (executability)

- **锚点**: TASK-001 deliverables[0] (L105) 「删远端分支 + `git -C aria worktree remove`」; TASK-014 title (L400) 「再删分支 (worktree 方式同 TASK-001 …)」。
- **实测**: `git worktree remove` 只删目录, `-b` 建的本地分支 `probe/152-dispatch` 留在 `aria/` 的 refs 里; TASK-015 收尾「`git status` clean」不会发现它, 但 `git branch` 会多出 throwaway 分支, 且 014 若复用同名会 `-b` 失败。
- **建议**: 两处补 `git -C aria branch -D probe/152-*`。

## 补证 (不计数)

- **A2-PP4-M1** (INV-1 管道 exec 崩溃): 本席复跑 `git -C aria show HEAD:…aether.py | python3 -c "exec(...)"` → 异常 (相对导入 `from .base import …` 脱包上下文); 用 A2 的 `sed 's/^from \.base import .*/CIBackend = CIStatus = InFlightStatus = object/'` 中和后 `ns['AetherBackend']._normalize_pr_ci_status([])` → `pending` ✓。同意修法 (sed 中和 + `AetherBackend.` 前缀), 并建议同步改 INV-1.encoded_as 与 TASK-013 verification[1] 两处。
- **A2-PP4-M2** (`exec_order_note` 11→12): 本席闭包脚本算得 12 项含 010a ✓, 不重复计数。

## 已核验无误

- **yaml 自洽**: 20 / 51h / exec_order 唯一且 > 依赖 / 闭包 / crosscheck 双向 / agent_summary 双向 / execution_order 文本 vs dependencies / parallel_tracks 轨序 — 全绿 (摘要已列)。
- **INV-3 条件组六处字段** (007a/b `conditional_on`; 006/011/015/016 `conditional_parts`) 与 §3.5 九项: 除 M1 「三行」外逐项对得上; INV-6 唯一例外 (checklist 1 → 016 标 N/A) ✓。
- **负控 pattern 与对偶**: 基线 0 命中实测 ✓ (见处置表 #1); false 分支可达 0 ✓; true 对偶字面与 §2.3 一致 ✓。
- **TASK-010a**: agent qa-engineer ✓ (AGENT_MAPPING `**/tests/**/*.py`); exec 12 < 010 (13) < 011 (14), 两者直接依赖 010a ✓; 五条断言在 010/011 前均红 (SKILL :180/:276 无 not_found · :172-183 无 gate_error · config.template 两 key 缺 · DEC 无前向指针 · path_coverage:36「9 个」) ✓; 「DEFAULT_CONFIG 断言绿 (003 已落)」与 010a 依赖 003 一致 ✓。
- **3b97c35 / tags / 版本点**: 见摘要 ✓; 「v1.66.4@9e6a17c」与 `baseline_sha` 注「(v1.66.4)」一致 ✓。
- **schema_note** 与文件自身数值一致 ✓。
- **TASK-001 探针可操作**: workflow 文件名 `issue-triage-tests.yml` + paths `skills/issue-triage/**` + `workflow_dispatch: {}` 实存 ✓; 基于 9e6a17c 正确 (不依赖 spec 代码) ✓; 三写者顺序 (001 建节 → 011 上方插四行 → 014 末尾追加 + :241 终改) 与 TASK-011/014 文本一致 ✓。
- **v4 新引用**: R3 簇/席位引用 (A1-M2/A2-M1 · A1/A4-M1 · A1-M3 · A3-M1 · A4-m2 · A5-M1 · A1-m6 · A1-m1/A5-m1 · A4-m4 · A1-m2) 逐一对应 R3 各席报告锚点 (A1 m1-m6 / A4 m1-m4 / A5 M1·m1·m2 实核编号存在且主题相符) ✓; 无对 1.66.3/1.66.4 作为 target 的陈旧引用 ✓; 主仓版本点行号在当前 1.66.4 状态下仍全中 ✓。
- **INV-4/5/7 编码**: 009 `--state-file` 必填 + 014 主仓绝对路径 ✓; 010/011 INV-5 grep ✓; 012 「ab-results 含执行记录」✓。
- **TASK-012 ↔ 013 ↔ 014 序**: 013 (15) → 012 (16) / 014 (17), 依赖边 012→013、014→013 ✓, 与 execution_order 汇合行同 ✓。

## Verdict

**PASS_WITH_WARNINGS** — vote **REVISE**。

- **必须改** (满足 Major 门槛, 各一短语): M1 TASK-016 「三行」→「仅 `.replace` 调用」(否则归档件删掉无条件行为的描述, 与 TASK-006 矛盾); M2 TASK-014 worktree 起点改 feature 分支 HEAD (或钉 gate cwd = `aria/`), 否则 SC-13 活体可能在基线脚本上跑出 `pending`。两条都是 v4 修簇 #5/#6 的新句子自身引入, 不触动依赖图 / 粒度 / agent 分配。
- **还能挑** (minor, 可同批顺手): m1 TASK-011 title 残留「机检脚本」; m2 TASK-012 红窗改为断言红 + reason 措辞; m3 probe 分支 `branch -D`。
- R3 归我席 5 条全 closed; yaml 机械自洽全绿; 负控 pattern 基线 0 命中实测; 3b97c35 实核。v5 落 M1/M2 (+ A2 的 INV-1 sed/前缀与 exec_order_note 12 项) 后可进 B.1。

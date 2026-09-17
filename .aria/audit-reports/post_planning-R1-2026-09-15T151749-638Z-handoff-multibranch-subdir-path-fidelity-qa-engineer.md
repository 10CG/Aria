---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-15T16:26:14.000Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/detailed-tasks.yaml
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 审计结论

### 已实读文件

- `openspec/changes/handoff-multibranch-subdir-path-fidelity/tasks.md`（全文 122 行）
- `openspec/changes/handoff-multibranch-subdir-path-fidelity/detailed-tasks.yaml`（全文 685 行）
- `openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md`（v7, 539 行；用 `sed -n` 分段读了头部 §1-115、§What 191-346、§Tasks 364-411、§Success Criteria 411-469、§rule6_note 456-469、§触点文件清单 30-115，共约 400+ 行原文）
- `.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md`（全文 116 行，§2 #195 表 8 行 + §5）
- `aria/skills/task-planner/DUAL_LAYER_SPEC.md`（字段说明表）
- `aria/skills/state-scanner/scripts/collectors/handoff_multibranch.py`（多段：240-300, 396-455, 458-545, 580-660）
- `aria/skills/state-scanner/scripts/scan.py`（160-200, 435-492）
- `.aria/state-checks.yaml`（三条 check 定位）
- `aria/CHANGELOG.md` 等版本点相关文件（VERSION、README.md、CLAUDE.md、docs/architecture/*）

### 已跑命令（均只读，未改任何仓内文件）

1. `git submodule status` + `git -C aria rev-parse HEAD` → 确认 aria = `1cb3872`（v1.73.3），与 tasks.md 头部「A.2 实测 `1cb3872`」一致。
2. `cd aria/skills/state-scanner && python3 -B tests/run_tests.py` → **`Ran 1605 tests in 129.791s … OK`**，与 `metadata.test_runner` 声称的「A.2 实测 1cb3872: Ran 1605 … OK」逐字符匹配。
3. `python3 -B -m unittest test_scan_integration -v` → **`Ran 19 tests … OK`**，匹配 TASK-010 verification 的「Ran 19 … OK (A.2 基线同为 19)」。
4. `pytest -q tests/test_collision.py` → **28 passed**，匹配 `metadata.test_runner` 的 `(b)` 腿声称。
5. `cd aria/skills/phase-d-closer && pytest -q tests/` → **11 passed**，匹配声称。
6. `python3 -B -m unittest <8 个模块>`（SC-10 点名集，不含 test_collision）→ **`Ran 169 tests … OK`**，与 SC-10 的「8 模块」口径逐字匹配。
7. `python3 -B -m unittest test_p1_layer_h test_handoff_multibranch_collision_dedupe test_track_board_advisories` → **24 / 23 / 5**，分别匹配 TASK-013 / TASK-014 / TASK-016 verification 里的具体数字。
8. 自建 `sc11_baseline_predicates.sh`，逐字抄 `metadata.sc11_baseline_predicates` 的 16 条谓词在 `cwd=aria/skills/state-scanner` 上跑 → **16 条全部 FAIL**，匹配 TASK-001 verification「16 条谓词…逐条输出 FAIL」。
9. 自建 `touchpoints-aria.txt`（按 §触点文件清单 41 行机械抄录）后跑 `git diff --stat f314785 1cb3872 -- $(...)` → **`8 files changed, 109 insertions(+), 10 deletions(-)`**，与 `metadata.baseline_rebase.result` 声称的「8 文件 / 109 增 / 10 删」逐字符一致；并用 `git diff` 实读三份 references 文件确认插入点 `:1062`→+2、`:84`→+2、`phase-1-collectors.md` 原位改写不移位，与 `metadata.baseline_rebase.shifts` 一致。
10. `git diff --stat f314785 1cb3872 -- handoff_multibranch.py scan.py latest_md_writer.py handoff.py _common.py` → 空输出，确认「代码落点零 diff」为真。
11. `grep -n` 核对 `.aria/state-checks.yaml` 三条 check 的 `name:` 行号 → **:124 / :177 / :408**，与文档声称完全一致；`grep -c 'bare-issue-ref\|check_bare_issue_refs' .aria/state-checks.yaml` = 0；`grep -c tracks_multibranch ab-suite/state-scanner.json` = 1（行 214，`collision.kind` 值写死在题面），均与声称一致。
12. `sed -n '20,26p' VERSION` + `grep '"version"' aria/.claude-plugin/plugin.json` + `grep` 各版本点文件 → 确认 **`VERSION:24` 仍是 v1.73.0，而 plugin.json / CLAUDE.md / README.md / 两处架构文档均已是 v1.73.3**，与 `metadata.baseline_rebase.main_repo.version_points` 的漂移声称一致。
13. 在 `scripts/` 下用一次性 Python 脚本直接调用 `dedupe_latest_per_track_container`，构造「同 track_id/updated_at/branch/filename(basename)，仅 rel_path 不同」的两行，验证正序/反序输入下赢家是否翻转 → **确认在当前 4 级键基线上，两组用例（x.md vs archive/x.md；archive/x.md vs old/x.md）都会随输入顺序翻转赢家**，证实 TASK-005/rule6_note「排序键用例在 4 级键下反序输入换赢家 ⇒ 基线红」的判断成立（Python `max()` 在完全打平的 key 上保留先遇到的元素，这点被 TASK-005 正确利用）。
14. `grep -n '_dedupe_sort_key\|^def '`、实读 `scan.py:160-200` 确认 SC-6「四道前置」判据（`current_branch`/`detached_head`/`enforced_remotes`/`track.branch==current_branch`）与代码逐行对应；`grep -n 'f"docs/handoff/{filename}"'` 确认拼串行确实在 `scan.py:186`。
15. `grep -n 'git remote'` 相关定位确认 `sync.py` 里有「`git remote` 是否有输出」的判据，佐证 TASK-022 对 SC-12b 要求「带 bare origin」（而非 unit test 常用的 `update-ref` 无真实 remote 手法）是必要的区分，不是画蛇添足。

以上逐项实跑核验的结论都与 tasks.md / detailed-tasks.yaml 的具体断言（数字、行号、diff 统计、baseline 红绿态）**完全吻合**，说明两份文件在「可机械核验的具体事实」这一层质量很高。下面的 finding 集中在**结构性缺口**（覆盖面 / 一致性），而非事实性错误。

---

### Finding 1 — [Major] type=issue category=testing scope=TASK-021 / TASK-015~018 / rule6_note / tasks.md「Success Criteria ↔ 任务映射」表

**证据**：tasks.md 的「Success Criteria ↔ 任务映射」表（tasks.md 文末表格）把以下 7 条 SC 的「钉测 / 反事实」列明确标为任务 **4.3**：

```
| SC-1 | 1.2 | 2.2 | 4.3 |
| SC-3 | 1.2 | 2.1 | 4.3 |
| SC-4 | 1.2 | 2.2 (后半) | 4.3 |
| SC-5 | 1.2 | 2.3 | 4.3 |
| SC-8 | 1.2 | 2.2 (后半) | 4.3 |
| SC-14 | 1.2 | 2.4 | 4.3 |
| SC-17 | 1.2 | 2.2 | 4.3 |
```

`detailed-tasks.yaml` 里 `parent: "4.3"` 对应的是 **TASK-021**（标题「全量回归两腿 + SC-10 点名集 + 冻结语料未重生成」）。我逐字重读 TASK-021 的全部 5 条 `verification`（`(a) run_tests.py` 零失败 / `(b)` pytest 两腿 / SC-10 点名集零失败 / 冻结语料 `git diff` 为空 / 失败归因），**没有任何一条涉及给已修复代码打反事实补丁**——它是纯粹的既有测试套件回归重跑，不产生新的坏实现输入。

而 Group 3（3.1-3.4 = TASK-015~018）逐条核对后，覆盖的只是 **SC-6（TASK-015）/ SC-7 + 排序键第5级（TASK-016）/ SC-13（TASK-017）/ SC-15 四条 + SC-18 两条 + SC-9(b)(c) + SC-16 两条 + SC-2（TASK-018）**——同样不含 SC-1 / SC-3 / SC-4 / SC-5 / SC-8 / SC-14 / SC-17。

这 7 条 SC 全部出现在 `metadata.rule6_note` 的「baseline-failing 实体 = 十二条」清单里，而 proposal.md 对这 7 条**每一条都写了明确的反事实**（已逐条实读确认，例：SC-1「反事实：回退枚举层为basename⇒git show失败⇒该行变legacy+该kind出现⇒全红」；SC-17「反事实：回退枚举层为basename⇒归档件恒降级legacy…⇒红」）。`metadata.rule6_note` 本身写明「substitute 覆盖…每条实体均附反事实」，`TASK-026`（Rule #6 AB 任务）的 verification 又明写「metadata.rule6_note 的 baseline-failing 实体台账（**TASK-007 RED + TASK-015..018 GREEN / 反事实**）完整保留」——但 TASK-015~018 结构上就装不下这 7 条,它们的反事实证据在整个任务图里没有任何任务产出。

**照计划执行会出的错**：执行者按 yaml 字面走完 TASK-001~032 全部任务后，SC-1/SC-3/SC-4/SC-5/SC-8/SC-14/SC-17 这 7 条（占 12 条 baseline-failing 实体的 58%，且包含 SC-17 这一唯一覆盖闸门输入 `collision.kind` 翻转的实体）**不会有任何反事实验证记录**落进 `verification-ledger.md`；随后 TASK-026 却会声称「完整保留」，产出一份内容不实的 Rule #6 substitute 证据台账。这直接削弱了 rule6_note 本应提供的「AB 测不到，但反事实证明测试有鉴别力」的证据链，且不会被本计划自身的任何后续步骤发现（TASK-026 没有交叉核验步骤去验证台账条目数与 12 条实体是否对得上）。

**建议改法**：要么在 TASK-021 的 verification 里补一段「对 SC-1/SC-3/SC-4/SC-5/SC-8/SC-14/SC-17 各自在一次性 worktree 副本上打回退枚举层为 basename 等反事实补丁，确认对应断言转红」（与 TASK-018 的写法同构，注明补丁与失败输出落台账），要么新增一个 TASK（如 TASK-018b）专门承接这 7 条，并让 TASK-026 的依赖链与「完整保留」判据实际可核。

---

### Finding 2 — [Major] type=issue category=implementation scope=TASK-026 / TASK-025 / tasks.md 组 5 标题行

**证据**：tasks.md 组 5 标题明写执行序「**5.3 → 5.5** → 5.1 (aria 侧) → 5.6 → 5.2 (子模块) → 5.1 (主仓同步面) → 5.2 (主仓 PR) → 5.4」（即 TASK-025 应先于 TASK-026）。detailed-tasks.yaml 文件头注释自称「执行序**以 dependencies 为准**（tasks.md 组 5 标题行给出发布段顺序）」——即 dependencies 字段是权威来源。`task-planner/DUAL_LAYER_SPEC.md` 也把 `dependencies` 列为**必需**字段（"✅"）。

但实读 `TASK-026`（parent 5.5）的 `dependencies` 字段为 `[TASK-021, TASK-022, TASK-024]`，**不含 TASK-025**（parent 5.3）。同组其余全部相邻边都正确编码了 tasks.md 的顺序（TASK-027 的 dependencies 同时含 TASK-025 与 TASK-026；TASK-028→029→030→031→032 逐级单向依赖），唯独 025→026 这条边缺失。

**照计划执行会出的错**：如果执行侧（subagent-driver 或任何按 `dependencies` 拓扑排序调度的执行器）严格按 yaml 的依赖图调度，TASK-026（Rule #6 AB 照跑 + 开 AB 套件缺口 issue）可以和 TASK-025（开遗留缺口 issue）并发执行甚至先于它执行，与 tasks.md 文字明写的顺序矛盾——两份被审文件在这一点上互相打架，执行者无法仅靠其中一份判断真实顺序。虽然两个任务分别开在不同内容的 issue（5.3 是功能缺口、5.5 是 AB 套件缺口），没有直接的数据依赖，但既然 tasks.md 显式声明了顺序、yaml 又自称以 dependencies 为准，这条边的缺失就是两份 A.2/A.3 文件之间的一致性缺陷。

**建议改法**：给 `TASK-026` 的 `dependencies` 补上 `TASK-025`。

---

### Finding 3 — [Minor] type=risk category=testing scope=TASK-003~006 / TASK-022

proposal 与既有测试文件（`handoff_multibranch.py:213-215` 自述、`test_handoff_multibranch_collision_dedupe.py:242` 的 `_git(tmp, "update-ref", f"refs/remotes/origin/{default_branch}", sha)`）确立的 hermetic 仓构造惯例是「**无真实 remote，只用 `git update-ref` 直接写 `refs/remotes/origin/*`**」。TASK-003~006 在要求「临时仓」时没有像它们对 SC-9 monkeypatch（点名 `test_scan_integration._mock_run` 为「现成范式」）、SC-4/13 日期 pin（点名 `_GIT_ENV` 模板）那样，明确点名复用这个 `update-ref` 手法；而 TASK-022 对 SC-12b 反而正确地要求「带 bare origin」的更重量级构造（因为它要跑真实 `scan.py` CLI，经 `sync.py` 对 `git remote` 有无输出的判据，`update-ref`-only 不够）。二者的区别是有technical依据的（已实读 `sync.py:75` 附近「Return True if `git remote` has any output」确认），但 TASK-003~006 里没写清楚「单元测试级夹具只需 update-ref，不需要真实 remote/clone」，存在被执行者误读为需要更重的仓构造（引入不必要的网络/性能开销或非确定性）的风险。建议在 TASK-003 里补一句明确指向既有 `update-ref` 手法。

---

## Verdict

0 Critical / 2 Major / 1 Minor → **PASS_WITH_WARNINGS**

## Vote

**REVISE**（存在 ≥1 Major：Finding 1 与 Finding 2 均需在 Phase B 开始前订正，否则 Rule #6 substitute 证据台账会不完整、Group 5 执行顺序在两份文件间自相矛盾）

## 轮次记录

Round 1 (qa-engineer, convergence): REVISE — 0C/2M/1m；核心事实性内容（169/1605/28/11/19/24/23/5 等全部测试计数、8 文件 109+/10- diffstat、16 条 SC-11 基线谓词全 FAIL、行号偏移表、VERSION:24 滞后、ab-suite 唯一命中行 214 等）逐项实跑核验**全部吻合**；两条 Major 均为结构性覆盖缺口 —— (1) SC-1/3/4/5/8/14/17 共 7 条 baseline-failing 实体的反事实在 tasks.md 承诺的任务 4.3（TASK-021）与实际 Group 3（TASK-015~018）里都未落地，与 TASK-026「完整保留」的自我声称矛盾；(2) TASK-026 缺少对 TASK-025 的 dependencies 边，与 tasks.md 组 5 标题行「5.3→5.5」顺序及 yaml 自称「执行序以 dependencies 为准」相矛盾。

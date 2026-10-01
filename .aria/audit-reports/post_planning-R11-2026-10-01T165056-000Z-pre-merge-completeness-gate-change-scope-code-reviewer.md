---
checkpoint: post_planning
mode: convergence
rounds: 11
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-10-01T18:09:30.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 已实读文件

派单 sha256[:16] = b88919277e205647 (112 行, 14855 B)

全部实跑都在 `/tmp/claude-1000/-home-dev-Aria/cbe6f623-7c3c-4217-8ccb-fd07680a5525/scratchpad/audit-R11-code-reviewer/` 下进行。我把两份共享副本 `cp -a` 到这里, 三个子模块的 gitdir 都是相对路径, 指向我自己的副本。没有在共享副本或真仓里跑过任何东西。跑完后副本已复原: porcelain 只剩原有的 ` M aria` 和 `??` 台账, worktree 只剩 1 条。

- `git diff fde9c1f 09c5130` 对两份计划文件的改动全部读过: tasks.md 4 个 hunk, yaml 18 个 hunk。`git diff --quiet e0d50e6 fde9c1f -- <两文件>` 退出 0, 说明 v2.10 和 v2.11 的基底逐字节相同。
- tasks.md (`09c5130`) 读过的部分: 读前必看第 1–33 条, 判断清单第 13、29、73–77 条, 第 145–284 行全文。
- yaml (`09c5130`) 读过的部分:
  - TASK-001/003/004/005/006/007/008/010/011/012/013/018/019/020/021/026/027/030 的 verification
  - metadata 下的 `rule6_note`、`commit_attribution`(代码与 cannot_catch)、`hard_constraints`、`stage_cells.rule`、`baseline_rebase`(查 aria_zero_diff 的全部消费点)、`c25_five_questions`、`a2/v2_state_runs`、`revision_log` 中 v2.11 的 5 条
- proposal.md 读过的行: `:9 :11 :16 :114 :157 :281 :299 :311 :429 :449 :458 :460 :463 :465 :471 :478 :480-486`。
- 决策单 `.aria/decisions/2026-09-30-199-b2-group1-spec-drift-rulings.md`: 全文 74 行。
- 台账 (未提交): 第 1–247 行, 外加附录 A 开头。
- aria `88689aa`:
  - `test_sibling_spec_probe.py`: `:1-60`、`:295-436`、`:828-856`、`:955-1057`、`:1915-2025`
  - `test_completeness_gate.py`: SC-15.5 / SC-15.10 / SC-21 / SC-7.b / SC-9.2 / SC-22.2 / SC-4 各格
  - `completeness_gate.py`: `:76 :92 :104 :1449-1693`
  - `git show --stat` 看了 `88689aa` 和 `04100b5`
- sibling-spec-probe 归档: proposal `:177 :179`、detailed-tasks.yaml `:221`、tasks.md `:26`。
- aria `1cb3872` (state-base): 24 处被引行, 见 3b 节的抽查结果。
- `standards/conventions/git-commit.md` §1、§2、§8.1; 工具 README; CLAUDE.md (见上下文)。
- 执笔报告和 v2.11 派单: 独立复算做完之后才读。

## Findings

计数 **0C / 0M / 3m**。

### m1 — `09d6a438` · minor · issue · testing · `detailed-tasks.yaml TASK-013`(反事实条, yaml:1851)

**一句话**: 反事实的四跑里没有「带 `sibling_spec_probe_` 前缀的辅助模块仍绿」这条正向对照。如果实现把前缀子句删掉, 四跑全部符合期望, 发现不了。

**证据**: 我在 aria `88689aa` 的 worktree 里构造了一个坏实现: 允许集照计划写成三项, 但删掉 `and not p.name.startswith("sibling_spec_probe_")`。

| 跑法 | 坏实现的结果 | 与计划期望 |
|---|---|---|
| 不打补丁 | `OK` | 相符 |
| (i) 允许集退回两项 | FAILED `['completeness_gate.py']` | 相符 |
| (ii) 加 `git_utils.py` | FAILED `['git_utils.py']` | 相符 |
| (iii) 加 `completeness_gate_helpers.py` | FAILED `['completeness_gate_helpers.py']` | 相符 |
| 补一跑: 加 `sibling_spec_probe_util.py` | FAILED `['sibling_spec_probe_util.py']` | 正确实现下这一跑是 OK |

正确实现在补的那一跑上是 OK, 我和执笔人都实测过, 执笔人的比较表里也有这一行。

**失败场景**: 测试侧实例违背第 1 条「前缀规则不变」, 把前缀子句删了。TASK-013 的反事实四跑照样全部相符, 台账记「可证伪性成立」。合进 master 以后, sibling-spec-probe 按它的归档约束新增 `sibling_spec_probe_` 前缀的 helper 时会假红。

**三态对照**:
- 正确实现: 绿 / 红 / 红 / 红, 正向对照绿。
- 删掉前缀的坏实现: 绿 / 红 / 红 / 红, 正向对照红。
- 只有正向对照分得开这两者。

**为什么只算 minor**: 第 1 条已逐字要求前缀规则不变, 照字面执行不会写出这个坏实现。漏网后的后果是将来假红 (fail-closed 方向), 不是假绿。

**修法**: 反事实条补一跑 (iv): 加空文件 `sibling_spec_probe_util.py` ⇒ 仍绿。

### m2 — `4a37c9ec` · minor · issue · documentation · `tasks.md 判断清单第 73 条`(tasks.md:137)

**一句话**: 判断清单第 73 条把 post_planning R11 列成「改另一份 spec 既有守卫」的授权来源之一。

**证据**:
- tasks.md:137 原文: 「授权来源是上述第 7 项裁定与本版经 post_planning R11, 不是执行者临场判断」。
- proposal `:429` 原文: 「属**改既有闸门**, 须 owner 明示 (Rule #10), 不得自行处置」。
- 决策单第 7 项只裁了「执笔实例比较 … 并推荐, 落进 TASK-013 的交付物与验收」, 没有点选 (a)。

**失败场景**: R11 之后 owner 只说「续跑」, 没对请裁第 1 条表态。执行者按第 73 条把「R11 PASS」当成 (a) 的授权, 直接改另一份已归档 spec 的守卫。授权链里多了一环非 owner 的判断。

**为什么只算 minor**: Status 行已写明 R11 之后由 owner 裁定续跑, 正常路径下 owner 会看到请裁第 1 条。

**修法**: 把授权来源改为「决策单第 7 项 + R11 之后 owner 对请裁第 1 条的裁定 (记台账)」。

### m3 — `f89a8d20` · minor · issue · documentation · `TASK-013 反事实条 / 判断清单第 13 条`

**一句话**: 新反事实条对实例的要求, 比计划里没改动的两处口径都宽, 而且没注明这是例外。

**证据**:
- 新文字, yaml:1851: 「补丁由既有结构约束条的执笔实例之外的实例或主控构造」。
- 未改动的判断清单第 13 条, tasks.md:77: 「反事实补丁由既非实现者也非测试作者的新实例构造」。
- 未改动的 TASK-019 第 2 条, yaml:1962: 「由 qa-engineer 的新实例构造, 该实例未参与 TASK-004~006 与组 2」。
- 判断清单第 73 条只写了放宽这件事本身, 没说它是对第 13 条的例外。

**失败场景**: 照 TASK-013 字面, 可以让组 2 的实现实例 (如 `ba-impl-2.5`) 来构造补丁。读到第 13 条的人会判为违规, 多一次往返。补丁只是退回允许集或加空文件, 独立性上的风险很低。

**修法**: 在该条注明「本条是第 13 条的例外, 理由: 补丁不需要实现知识」; 或者把要求改为「既非组 2 实现者、也非该条执笔实例的实例, 或主控」。

## 对账

### 3A 结构约束冲突的处置 — closed (另有 m1、m2)

修法 (a) 与 TASK-013 本身:
- 改动前, 在我的副本里 (aria `88689aa` 嵌在主仓里, cc1bdef 可达) 跑 discover: `Ran 133` / `FAILED (failures=1)`, 失败信息 `AssertionError: Lists differ: ['completeness_gate.py'] != []`。
- 按 (a) 改一行允许集后: `Ran 133` / `OK`, 末行不带 skipped。
- 用例数: 我用 loader 实数, `test_sibling_spec_probe` 104 个、`test_completeness_gate` 29 个, 与 TASK-013 写的 133 = 104 + 29 一致。
- cc1bdef 不可达时: 我在主仓外建 worktree 再跑, 得 `Ran 129` / `OK (skipped=1)`, 与执笔人记的一致。
- 撤补丁: worktree 里留着未跟踪文件时 `git worktree remove` 退出 128 (`contains modified or untracked files`); 删掉文件后退出 0。与计划写法一致。

(a) 比 (b) 好这一结论成立:
- 归档 proposal `:179` 的约束原文是「探针自己的 helper 一律放 scripts/ 下并用模块名前缀」。
- 我在 (a) 下实测: 加 `git_utils.py` 红、加 `lib.py` 红、加 `completeness_gate_helpers.py` 红、加 `sibling_spec_probe_util.py` 绿。
- 其它 skill 的 `scripts/` 里只有 `phase-c-integrator/scripts/pre_merge_gate.py` 和 `state-scanner/scripts/lib/` 两处可能撞名的; 也没有任何 `git_utils.py` 或 `lib.py`。所以 (b) 下这两个名字都会转绿, 执笔人的判断属实。

连带面 (判断清单第 74 条) 逐项核实:
- `aria_zero_diff`: 我把 yaml 整棵树扫了一遍, 只有 TASK-001 第 9 条消费它, 而 TASK-001 已经执行完。
- TASK-031: 只看 `phase_d_sot`, 不受影响。
- TASK-027 第 4 步: (b) 比的是 A..S3, (c) 比的是 W..feature, 两个区间都在 2.6 提交之后才开始, 看不到这处改动。
- rule6_note 把测试代码归为「判据表第一行」: 与 proposal `:486`「描述性 / 纯代码 (脚本 / 测试 / …)」一致。
- 不足之处: 反事实缺正向对照 (m1); 授权措辞把审计列为授权源 (m2)。

### 3B 决策单第 1–6 项并入读前必看 — closed

- 执行口径逐字核对: 我用 python 取出第 25–32 条的执行口径列, 与决策单对应的裁定原文 (§1、§2、§3.1、§3.2、§3.3、§4、§5、§6) 逐字比对, **8/8 完全相同**。
- 「proposal 正文」列的引用全部实读一致: `:458` 兜底句、`:460` 22 份 / `unattributed_count == 22` / 其余 2 份、`:463` C 与裸 glob、`:157` 的 `2026-…-aria-orchestrator`、`:465` R4「两跑」与 R5「锁短路」、`:471` 的 `enabled_by == 'mode:convergence'`、`:478` 与 `:281` 的 WARN 全文、`:114` / `:299` / `:311` 第 (3) 条。
- 测试里已按这些裁定落地:
  - SC-7.b fixture 同时建了 `aria-orchestrator` 与 `aria-orchestrator-divestiture` (test_completeness_gate.py:921-949)
  - SC-9.2 两份 config 在同一格里顺序跑 (:1058)
  - SC-22.2 断言 §1.4 的整行 WARN (:2432)
  - SC-4 断言 `unattributed_count == 22` (:415)
  - SC-15.5 断言 `entry["enabled_by"] == "mode:convergence"`
- 第 30 条执行口径里照录了原文「计划不出 v2.11」, 依据列写明已被第 7 项改判。不影响执行动作。

### 3C Phase B 计划缺口登记 — closed

决策单列出的六项和执笔人补的第七项, 我逐项对着台账、测试和代码核过:

1. SC-15.10:
   - TASK-006 新增条 (yaml:1710) 与测试代码逐项一致: 四键显式、adaptive、无 Level 行、exit 1、`checked_checkpoints == ['post_spec']`、stderr 不含 `spec_level_undetermined`。
   - `stage_cells` 与 v2.10 相同, 仍是 39 格。
2. `enabled_by`: 测试本来就有这条断言。
3. Ran 口径: 133 已实测。
4. 附录 A:
   - 台账里确有 `## 附录 A`, 共 90 个不同的 SC 格、六条勘误。
   - yaml 里检查二级标题的只有 TASK-001 第 9 条, 没有任何机检统计台账标题数。
5. 推导值: 测试里在这几处标注了 `derived, not spec-literal`: `:19 :322 :981 :2033`。
6. 常量名: 脚本 `:76` 定义 `DEFAULT_AUDIT`, `:92` 定义 `LEGACY_CHECKPOINT_MAPPING`, 测试用 `hasattr(mod, "DEFAULT_AUDIT")` 读取。
7. 决策单两次提交:
   - 我在副本里跑 `commit_attribution 8d2ff8b 09c5130`, 得 `{"verdict": "stop", "kinds": ["own", "foreign", "foreign", "own"]}`, 退出 1。
   - 两个 foreign 恰好是 `b575aa5` 和 `fde9c1f` (只改 `.aria/decisions/`)。
   - `09c5130` 判 own, 因为 TOOLING 目录在本轨专属集里。

台账里还有一处计划字面没写的事实: state-scanner 实测 `Ran 1627`, A.2 记的是 1605。这已被 TASK-021「Ran 数变化逐条归因」覆盖, 不算计划缺口。

## 对「改变执行者动作的改动」的逐条判断

1. **TASK-013 既有结构约束条**: 改法正确。三项允许集、逐字比较、只改类内, 都已实测成立。
2. **TASK-013 discover 条**: 改法正确。实测 133 / OK; 主仓外跑得 129 / skipped=1, 按新判据判为不通过, 这个判法成立。
3. **TASK-013 提交条**: 改法正确。WIP `88689aa` 只含两个文件 (+1694 / +48 行)。按旧写法提交, porcelain 会剩下测试文件, 判据不成立。WIP 保不保留见请裁第 6 条。
4. **TASK-013 反事实条**: 预期值全部复现, 但有问题: 缺正向对照 (m1), 实例要求与第 13 条口径不一 (m3)。
5. **TASK-020 第 (10) 条**: 改法正确。我自己构造了一个 eager 补丁 (在 `resolve_inclusion(...)` 之后无条件调用 `resolve_pre_merge_axes(...)`), 29 个用例里只有 SC-15.10 红, 首个失败断言是 `AssertionError: 2 != 1`, stderr 是 `spec_level_undetermined` 那一行。

接缝 (v2.11 改动与未改动文字之间):
- 第 13 条与 TASK-019 的实例要求: 计入 m3。
- TASK-005 的 SC-7 链接注挂在 `--no-spec` 那条上 (yaml:1690), 因为 TASK-005 没有专门讲 SC-7(b) 的条目。只是可读性问题, 不计入。
- 「TASK-0NN 第 N 条」这类序号引用全文扫过, 只剩第 29 条引用的「TASK-006 第 2 条」。新条插在它之后, 所以它仍指 SC-15(5) 那条, 正确。
- TASK-021「2.6 之后期望 133」与 5.1 并入上游后的重跑: 两者能通过「逐条归因」兼容, 不算接缝。

其它核验:
- 引用抽查 37 处全部一致: proposal 13 处; aria `1cb3872` 上 24 处, 包括 `run_all_tests.sh:41-46`、`spec_complete.py:273`、`test_pre_merge_gate.py:266`、`state-scanner/SKILL.md:182/:191`、`constants.py:58`、`phase-c-integrator/SKILL.md:57/:157/:603/:612-614/:625-630/:638/:754`、`push_all_remotes.sh:49/:107/:112/:119`、`DEFAULTS.json:6-15`、`pre-write-validation.md:25`、`audit-engine/SKILL.md:423`、`execution-modes.md:9-10`、`phase-a-planner/SKILL.md:267`、`phase-b-developer/SKILL.md:204/:277`。
- 三态证据:
  - a2 按 `command` 复跑: 退出 0, 2396 B, sha256[:16] `5ebe2c78a6d2665f`, 与 `output` **逐字节相同**。
  - v2 复跑: 9957 B, 也逐字节相同。
  - `REGEN_IDENTICAL`。
  - 新增行里裸引用 0、禁用字形 0、NUL 0、CR 0。
  - 前 78 条 `revision_log`、`owner_gates`、`stage_cells`、`hard_constraints` 都与 v2.10 相等; 各 TASK 的依赖、工时和 agent 都没变。
- 归档门: 全勾选的 C 态判 `verdict=warn exit=0 blocking_on_symbol=0`, warn 来自 4.4 行的 dogfood 无产物 claim。新的 2.6 行没有带出新 claim; 归档 Step 7 已在等待点 11 登记。
- git 序列: v2.11 没碰 5.5–5.8。WIP 和新提交都只在本地 feature 分支, `fetch` 只更新远程跟踪 ref, 不会覆盖它们。第 5 步的 `HEAD^2` 断言仍有效。
- 与执笔报告的分歧: 执笔人的比较表里有正向对照那一格, 但没写进反事实条 (m1); 执笔人把 R11 当作授权源 (m2)。其余结论全部复现。

## 对执笔人自报薄弱点的表态

1. 原文: (b) 用的是我写的候选补丁, 写得更复杂能抓到 `lib.py`。表态: **可接受**。推荐 (a) 的依据是 docstring 自举的红例 `git_utils.py` 和约束原意, 不依赖 `lib.py` 那一格。
2. 原文: eager 补丁是一种构造; 只锁住了「Level 解析不出」那一半。表态: **可接受**。我自构的补丁复现了同样的结果。另一半见请裁第 8 条。
3. 原文: Ran 129 是在独立克隆里测的。表态: **可接受**。我复现了 129 / skipped=1 和 133 / OK 两态。
4. 原文: 读前必看第 33 条超出派单范围。表态: **可接受**。它符合本节「正文与口径差异」的定义, 不改变动作。
5. 原文: TASK-013 工时仍写 1-2。表态: **可接受**。多出的两步约 0.5–1h, 工时不是闸门。
6. 原文: 「复跑相同」以终版三个文件为准。表态: **可接受**。我对 `09c5130` 复跑, 结果相同。
7. 原文: Status 行的「待主控核验」提交后就过期。表态: **可接受**。沿用了往版写法, 不影响动作。

## 对执笔请裁 8 条的表态

1. 原文: 修法取 (a), 备选 (b)。表态: **赞成执笔**。理由见 3A; 建议同时按 m1 补正向对照。
2. 原文: 新增读前必看第 33 条, 备选不加。表态: **赞成执笔**。代码落点差异有了可追溯的位置。
3. 原文: TASK-020 补第 (10) 条, 备选沿用测试作者本人的那次实测。表态: **赞成执笔**。让非测试作者复验, 符合第 9 条硬约束; 我已复现。
4. 原文: 第 3 项拆成三行, 备选合成一行。表态: **赞成执笔**。三行分属三个不同 TASK 的条目, 拆开后锚点能指到单条。
5. 原文: 第 4 项原文照录, 改判写在依据列; 备选不收第 4 项。表态: **赞成执笔**。第 4 项里的执行注 (5.8 判 foreign) 仍然有效, 不收就丢了。
6. 原文: WIP 提交保留并另起提交, 备选压进 2.6 的提交。表态: **赞成执笔**。
   - 保留的理由: `88689aa` 已被决策单 (`fde9c1f`, 将来会推送)、台账和本计划引用, 压掉会让这些引用悬空。aria master 上已有 13 个 `wip(...)` 先例 (如 `6f4bbe4`、`e2ab6ed`)。
   - 建议: WIP 提交正文写着「本提交只在本地, 不推送」, 5.6 推送后这句就不成立。可以在 2.6 提交正文里注明 WIP 已被接续。
7. 原文: Ran 要求「恰为 133、不带 skipped」, 备选「≥133 并逐条归因」。表态: **赞成执笔**。2.6 时还没并入上游, 用例集是封闭的, 精确值能拦住 skip。但如果请裁第 8 条的补格写成新方法而不是 subTest, 要同步改这个数。
8. 原文: lazy/eager 分歧的「mode 写错」那一半要不要补格。表态: **倾向补格, 由 owner 定**。目前 SC-15.5-typo-mode 不全显式, 所以将来哪怕改成在加载时就校验 mode, 也没有任何格会红。补格请写成 subTest, 不改 Ran 数。

## 风险 / 疑问

- sibling-spec-probe 归档的 `detailed-tasks.yaml:221` 和 `tasks.md:26` 仍写着两项允许集。5.5 合并后, 线上测试会与归档描述不一致。归档是冻结记录, 不构成 Rule #3 的同步义务; docstring 里写上 10CG/Aria#199 就能留下追溯线索。
- `wip` 这个 type 不在 git-commit.md §2 的类型表里 (有先例, 我不判为违规)。
- `test_sibling_spec_probe.py:1915-2025` 有几类测试会读 execution-modes.md 和 SKILL.md 的内容 (TestSC17* / TestSC20*), 而组 3 会改这两个文件。这是 v2.10 就有的风险, 由 TASK-021 兜住。

## Verdict

PASS — 0C / 0M / 3m

**Vote: PASS**

## 是否足以开始 Phase B

**足以。** v2.11 的五处动作改动都已在我的副本上实测成立, 三条 minor 都是一句话的补写, 不阻塞。前提是 owner 先对请裁第 1 条表态 (见 m2), 然后从 2.6 续跑。
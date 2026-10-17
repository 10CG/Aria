---
checkpoint: post_planning
mode: convergence
rounds: 11
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-10-01T17:34:33.490Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 已实读文件

派单 sha256[:16] = 10fc3fb0e30dc7cc

所有读取和实跑都在我自己的目录 `<scratch>/audit-R11-tech-lead/` 里完成，两份共享副本只做了 `cp -a`。共享副本和真仓都没有写入，也没有在里面运行任何命令。

- 被审 diff：`git diff fde9c1f 09c5130 -- tasks.md detailed-tasks.yaml` 全量。yaml 另用逐行、逐字符的 diff 脚本拆出 22 处改动。
- `tasks.md` v2.11 全文，283 行。
- `detailed-tasks.yaml` v2.11：
  - metadata 读了这些段：`scope_repos`、`baseline_rebase`（含 `aria_zero_diff` 的全部消费点）、`hard_constraints`、`owner_gates`、`rule6_note`、`c25_five_questions`、`execution_order`、`stage_cells.rule`、`commit_attribution` 全文、`revision_log` 的 v2.11 五条、`a2_state_runs` 的输出。
  - TASK-001 到 031 的 verification 全读；TASK-013 / 019 / 020 / 021 / 024 / 027 / 030 逐字读。
- `proposal.md`：头部 `:9-18`，以及 `:11` `:114` `:157` `:281` `:299` `:311` `:429` `:458` `:460` `:463` `:465` `:471` `:478`，逐处用 python 切片核对锚点。
- 决策单 `.aria/decisions/2026-09-30-199-b2-group1-spec-drift-rulings.md` 全文：第 1–7 项和落地记录。
- 台账 `verification-ledger.md`（未提交，在我的副本里只读）：基线、RED、组 2 收口、外向动作、停下与上报、附录 A 开头。
- 执笔派单和执笔报告 `writer-reports/v2.11-dispatch.md`、`v2.11-writer-report.md` 全文；工具 README 的重跑段。
- aria `88689aa` 上的源码：
  - `tests/test_sibling_spec_probe.py:40-60`、`:400-520`（`TestStructuralConstraints` 整个类）、`:828-851`（对 cc1bdef 的依赖）
  - `tests/test_completeness_gate.py`：SC-15.10 格（`:1515-1560`）、常量引用（`:2212-2302`）
  - `scripts/completeness_gate.py:76`、`:92`、`:104`、`:1006-1012`、`:1505-1580`
- sibling-spec-probe 归档 `proposal.md:179`。
- `standards/conventions/git-commit.md` §2 / §8.1；CLAUDE.md 的两条多远程硬约束，以及 Rule #3 / Rule #6 / Rule #8 / Rule #10。

实跑（都在我的副本里）：

1. 目录全量 discover，原状：`Ran 133` / `FAILED (failures=1)`，offenders 为 `['completeness_gate.py']`。
2. 按 (a) 改允许集之后：
   - 在主仓布局下：`Ran 133` / `OK`，不带 skipped。
   - 同一提交放到主仓布局之外的 worktree：`Ran 129` / `OK (skipped=1)`。
3. TASK-013 的反事实四跑。先把改动提交到自建分支，再 `git -C aria worktree add`：
   - 依次为：绿 / 红 `['completeness_gate.py']` / 红 `['git_utils.py']` / 红 `['completeness_gate_helpers.py']`。
   - 副本里带着未跟踪文件时，`worktree remove` 退出 128；删掉文件后退出 0。
4. TASK-020 第 (10) 条的 eager 补丁，两种放法（在 `resolve_inclusion` 之后或之前，无条件调用 `resolve_pre_merge_axes`）：
   - 两种都是 `Ran 29` / `FAILED (failures=1)`，只有 `SC-15.10-pre-merge-lazy-when-inclusion-nonempty` 变红，首个失败断言是 `2 != 1`。
5. 生成器 `REGEN_IDENTICAL`；在我自己的 state-base 副本里复跑 a2_state_runs，`cmp` 与嵌入输出逐字节一致。v2 两跑我没复跑。
6. 按 yaml 原样跑 `commit_attribution 8d2ff8b 09c5130`：
   - 输出 `{"verdict": "stop", "kinds": ["own", "foreign", "foreign", "own"]}`，退出 1。
   - `b575aa5` 与 `fde9c1f` 判 foreign，与 TASK-030 新加的注一致。
7. v2.10 → v2.11 结构比对：
   - 31 个 TASK 的 dependencies / agent / complexity / estimated_hours / parent 全部不变；deliverables 只有 TASK-013 变了。
   - owner_gates / hard_constraints / c25 / stage_cells / commit_attribution / execution_order 逐值相等。
8. `ls-remote`（只读）和自建副本的 fetch：
   - aria 两端 master 为 `268da8f`（v1.74.1）；主仓两端为 `0748dbc`。
   - `5215cf2..268da8f` 对 `skills/audit-engine` 零改动。

## Findings

没有 critical，没有 major。

### m1 — `6c7e3a62` · minor · issue · testing · scope `detailed-tasks.yaml TASK-013 既有结构约束条`

- **summary**：「git -C aria diff 只落在 TestStructuralConstraints 类内」这条机检的边界和条文约束对不上。它看不见同一个类里的另一个用例；又没限定文件，和本任务提交条预留的「WIP 之后另有改动一并 add」互相打架。
- **证据**：
  - `detailed-tasks.yaml:1847` 原文：「不动 scripts/ 下任何文件、tests/test_completeness_gate.py 与该测试文件的其它用例, git -C aria diff 只落在 TestStructuralConstraints 类内」。
  - 这个类（aria `88689aa` `test_sibling_spec_probe.py:412-435`）有两个用例：`test_no_lib_or_collectors_directories_under_audit_engine` 和 `test_scripts_helper_files_are_namespaced`。
  - `:1850` 原文：「WIP 之后 scripts/completeness_gate.py 或 tests/test_completeness_gate.py 若另有改动, 一并 add」。
- **失败场景（三态）**：
  - 改动正确时，判据为真。
  - 如果误改了同一类里的另一个用例（例如放宽 `lib/` 守卫，但它仍能通过），判据仍为真，discover 仍是 133 OK，反事实只跑目标用例——全绿放过。
  - 如果续跑前 WIP 之后已经有 `test_completeness_gate.py` 的改动（例如 owner 采纳请裁 8 补了格），不带路径的 `git -C aria diff` 会跨文件，判据为假；而提交条要求一并 add。执行者拿到的是两条相反的指令。
- **建议**：拆成两条机检。
  1. `git -C aria diff --name-only` 的集合必须包含于 {该测试文件} ∪ {台账已列出的 WIP 之后改动的文件}。
  2. `git -C aria diff -U0 -- skills/audit-engine/tests/test_sibling_spec_probe.py` 的每个 hunk 只能落在 `test_scripts_helper_files_are_namespaced` 的允许集那一行、它的 docstring，或类 docstring 内。

### m2 — `63a8700c` · minor · issue · testing · scope `detailed-tasks.yaml TASK-013 反事实条`

- **summary**：(ii)(iii) 两跑的补丁是未跟踪文件，而本条引用的 TASK-019 三步法要求「记副本 HEAD 与补丁 diff」。`git diff` 对未跟踪文件退出 0、输出为空——正是 hard_constraints 第 14 条第 (3) 点要求逐处写明的「退出 0 却没比成」形态。本条只写了撤补丁怎么处理。
- **证据**：
  - `:1851` 原文：「(ii)(iii) 加的是未跟踪文件: 撤补丁时删掉该文件」。
  - `:1961` 原文：「记副本 HEAD 与补丁 diff (以副本路径为根)」。
  - 我在自建 worktree 里 `touch .../scripts/git_utils.py` 之后，`git diff` 退出 0、输出 0 字节；`git status --porcelain` 输出 `?? skills/audit-engine/scripts/git_utils.py`。
- **失败场景**：执行者照 TASK-019 记补丁 diff，台账里 (ii)(iii) 的补丁记录是空串。
  - 守「空输出不得放行」的执行者会误判补丁没打上，因此停下。
  - 不守的执行者会留下一条无法复核的空记录。
- **建议**：本条补一句——(ii)(iii) 的补丁记录取 `git status --porcelain` 和 `git diff --no-index /dev/null <文件>` 的原样输出（有内容时退出 1）。

### m3 — `f49493cf` · minor · issue · documentation · scope `tasks.md 判断清单第 77 条`

- **summary**：v2.11 有两项流程取舍没进判断清单：请裁 6「WIP 提交保留、另起提交」和请裁 7「Ran 恰为 133 且不带 skipped」。而且第 77 条末句反过来说「TASK-013 的 Ran 口径不属判断」。
- **证据**：
  - `tasks.md:141` 原文：「TASK-006 的 SC-15(5) 条补回 `enabled_by` 断言与 TASK-013 的 Ran 口径不属判断, 只记 yaml `revision_log`」。
  - 执笔报告「请裁项」第 6、7 条各自给了备选。
  - 用脚本检索判断清单里的 `WIP|88689aa`，只命中第 73、76 条中对一次性副本的描述。
  - 前几版的执笔请裁一般都挂在判断条目上，owner 的追认注写在条目末尾（例如第 51、69、71、72 条）。
- **失败场景**：owner 对请裁 6、7 的裁定没有判断条目可挂；5.9 照录判断清单进周期 handoff 时，这两项 AI 取舍缺席（Rule #10 §5 的留痕面）。执行动作不变，所以是 minor。
- **建议**：在第 73 条补登，或新增第 78 条，写明两项的取舍、备选和代价；删掉第 77 条末句里的「与 TASK-013 的 Ran 口径」。

### m4 — `4a37c9ec` · minor · issue · documentation · scope `tasks.md 判断清单第 73 条`

- **summary**：第 73 条把「本版经 post_planning R11」列为改另一份 spec 测试守卫的授权来源。R11 是 AI 审计，不是 owner 明示；这与本条自己援引的 proposal `:429`「须 owner 明示」口径不一致。
- **证据**：
  - `tasks.md:137` 原文：「授权来源是上述第 7 项裁定与本版经 post_planning R11, 不是执行者临场判断」。
  - 决策单第 7 项只要求执笔「比较……并推荐」，没有预先选定 (a)。
  - proposal `:429` 原文：「属改既有闸门, 须 owner 明示 (Rule #10)」。
- **失败场景**：R11 收敛后，如果 owner 只说「续跑」、没有对请裁 1 表态，执行者按这句话就会把 (a) 视为已获授权。实际后果有限，因为 Status 行要求由 owner 裁定续跑。
- **建议**：改为「授权来源是第 7 项裁定，以及 owner 在 R11 之后对本版（含执笔请裁第 1 条的修法取舍）的裁定」。

## 对账

### 3A 结构约束冲突的处置：closed

- **修法比较与推荐**：落在判断清单第 73 条和 revision_log。推荐 (a) 的依据我独立核过：
  - 约束原文（sibling-spec-probe 归档 `proposal.md:179`）管的是「探针自己的 helper」。
  - aria 所有 skill 的 scripts/ 里只有这一个 `completeness_gate.py`，也没有任何 `git_utils.py`。所以 (b) 结构上抓不到 docstring 自己举的红例。
- **落进 TASK-013**：交付物加了该测试文件，verification 从 3 条改为 5 条，没有新增 TASK 编号。实跑结果与所写一致。
- **决策单点名的「基线清单」**：判为不改，理由成立。`aria_zero_diff` 全计划只有 TASK-001 的基线复核条（`yaml:1613`）消费，台账「基线」节已经执行完。
- **「TASK-021 回归口径」**：已加注。
- **DAG 与 Rule #6**：DAG 不变；这处改动早于 W，TASK-027 第 4 步的 (b)(c) 两侧都看不见它，与 rule6_note 新加的那句一致。
- m1、m2、m4 都不影响「有合法下一步」。

### 3B 决策单第 1–6 项并入读前必看：closed

- **执行口径列逐字比对**：读前必看第 25–32 条的执行口径列，与决策单第 1、2、3.1、3.2、3.3、4、5、6 项的裁定原文逐字全等（8/8 `==` 为真）。
- **依据列**：
  - 第 30 条的依据列含第 4 项「执行注」原文，第 32 条含第 6 项「代价」原文。
  - 依据列一律写决策单全路径。
- **proposal 正文列**：各条引用的 proposal 行号逐处找到了所述文字。
- **链接注**：
  - 读前必看第 6 条补了一句指回第 29 条。
  - TASK-002 / 004 / 005 / 006 / 010 / 011 / 030 的链接注只做追加，不改动作。TASK-010 / 011 的两句与实现 `completeness_gate.py:1519` 和 `:1571` 的 lazy 写法一致。
- 第 29 条照录的「TASK-006 第 2 条」：v2.11 的新条插在它后面，所以仍然指向 SC-15(5) 那一条。

### 3C 登记 Phase B 已发现的计划缺口：closed

决策单第 7 项点名的六类都有落点：

- **SC-15.10**：TASK-006 的新条与测试文件 `:1544` 的格逐项一致；SC 映射表已登记；TASK-020 补了第 (10) 条；stage_cells 不动，理由与 `stage_cells.rule` 相符。
- **enabled_by 补回**：已补。
- **Ran 口径**：已改为恰为 133。
- **矩阵附录**：登记条与台账附录 A 开头的六条勘误一致。
- **推导值**：判断清单第 77 条。
- **importlib 常量名**：测试 `:2237-2302` 引用的名字与脚本 `:76`、`:92` 实名一致。

另外还登记了决策单两次提交在 5.8 判 foreign，已用实跑证实。台账里我没有找到其它需要改动作的执行事实。

## 对「改变执行者动作的改动」的逐条判断

1. **TASK-013 既有结构约束条：改法正确。** 改后全量 133 OK；允许集按文件名逐字比较，前缀规则和 glob 不变。判据边界的问题另计为 m1。
2. **TASK-013 discover 条：改法正确。** 两种情况我都实跑过：「133、不带 skipped」在主仓布局下可达；独立 worktree 下得到的 129 / skipped=1 会被正确拦下。
3. **TASK-013 提交条：改法正确。**
   - 在 WIP 之上另起提交、保留 WIP，与判断清单第 18 条「台账引用的 SHA 留在远端」是同一原则——台账、决策单落地记录和 v2.11 本身都已经引用 `88689aa`。
   - 「提交后 porcelain 为空」可达，已实测。
4. **TASK-013 反事实条：改法正确。** 四跑可复现，能区分逐字比较和前缀写法；补丁记录口径的问题另计为 m2。
5. **TASK-020 第 (10) 条：改法正确。** eager 补丁放在 P4 之后或之前，都只有 SC-15.10 变红，结论不依赖补丁形状。

**接缝**：

- 除 m3（第 77 条与请裁 7 口径相反）外，没有发现新的不一致。
- 我对 live 文本整族扫描了位置式引用（「TASK-0NN 第 N 条 / 末条」）。被插入条目的 TASK-003 / 006 / 013 没有被位置式引用指错。
- 新的 2.6 行不含集成关键词，a2 复跑逐字节一致，归档门不受影响。
- TASK-019 的「做法（TASK-019 / 020 / 022 共用）」没把 TASK-013 列为共用方，属措辞问题，不计 finding。

## 对执笔人自报薄弱点的表态

1. **原文**：两种修法的反事实用的是执笔人自己写的候选补丁；(b) 写复杂些能抓到 `lib.py`，但抓不到 `git_utils.py`。**可接受**：我用自己的补丁复现了 (a) 的四跑；全仓没有任何其它 skill 有 `git_utils.py`，所以 (b) 的任何写法对它都是绿，结论不受补丁写法影响。
2. **原文**：eager 补丁只是一种实现；SC-15.10 只锁住「Level 解析不出」那一半，「mode 写错」那一半没有格。**前半可接受**：两种放法实测结论相同。**后半属实**：我造了一个仓——三个非排除键全部显式、pre_merge 不写、`mode: convergnce`——现实现得 exit 1、`error_kind` 为 None，没有任何格锁住这个行为。
3. **原文**：Ran 129 是在独立克隆里测的，真仓那一跑是 133。**可接受**：两个数我都复现了。
4. **原文**：读前必看第 33 条超出了派单明列范围，是执笔人自己的判断。**可接受**：它正属于该节定义的「proposal 正文与执行口径的差异」，且已登记在第 75 条。
5. **原文**：TASK-013 多了两步，工时仍写 1-2。**可接受**：不改执行动作；建议下次改到这里时调为 2-3。
6. **原文**：revision_log 第 83 条的复跑断言以终版为准，再改须重跑。**可接受**：我在 `09c5130` 上复跑了 REGEN 和 a2，都一致。
7. **原文**：Status 行末的「待主控核验」提交后即过期，沿用前例。**可接受**：只是状态描述，不影响动作。

## 对执笔请裁 8 条的表态

1. **原文**：修法取 (a)，备选 (b)。**赞成执笔取舍 (a)**：保住了对辅助模块的全部约束且可证伪；(b) 会让这个测试的红绿随别的 skill 的文件变化，只跑某个 skill 自己 tests/ 的回归看不见。
2. **原文**：新增读前必看第 33 条，备选是不加。**赞成执笔取舍**：这样「proposal 不改，以本节为准」才覆盖到代码落点。
3. **原文**：TASK-020 补第 (10) 条，备选是沿用测试作者本人的实测。**赞成执笔取舍**：hard_constraints 第 9 条和判断清单第 13 条都要求由非作者复验，我已复现。
4. **原文**：第 3 项拆成三行，备选是合成一行。**赞成执笔取舍**：三处分属不同的 SC 和不同的 TASK 条目，拆开后锚点式引用可以指到单行。
5. **原文**：第 4 项原文照录、改判写在依据列，备选是不收。**赞成执笔取舍**：第 4 项仍有生效的动作（派单带上本单）和执行注（5.8 判 foreign）；执行口径列里「计划不出 v2.11」已经过期，但依据列化解了。
6. **原文**：WIP 提交保留并另起提交，备选是压进 2.6 的提交。**赞成执笔取舍**：如果压掉，台账、决策单和本版计划里引用的 `88689aa` 将永远到不了远端。代价见风险第 1 条。
7. **原文**：Ran 要求恰为 133 且不带 skipped，备选是 ≥133 并逐条归因。**赞成执笔取舍**：2.6 这个时点没有别的改动来源，等式最简单，对 skip 形态也是失败即关；之后的重跑（TASK-021 / 027）本来就是「不少于基线 + 归因」。
8. **原文**：「mode 写错」那一半要不要另补一格。**赞成备选（补格）**：
   - owner 第 6 项的代价句点名了两半，现在只锁住了一半。如果有人把 mode 校验挪到配置加载时，这一半会静默翻转，而现有测试全绿。
   - 代价：由非实现者的测试实例在 2.6 提交前补一个子格（subTest 不改变 Ran 数），4.2 加一个反事实，计划要给出落点。
   - 若 owner 认为第 6 项说的「补一格」已经够了，维持现状也不会造成执行错误。

## 风险 / 疑问

1. **WIP 提交会被推出去**：`88689aa` 的类型是 `wip`，正文写着「本提交只在本地, 不推送」。照计划它会在 5.5 随 `--no-ff` 并入 aria master，5.6 推到两端，届时这句话就不成立了。`wip` 不在 git-commit.md §2 的类型表里，但 aria master 上已有 13 个 `wip(...)` 先例，所以我不计为 finding；请 owner 裁请裁 6 时知悉。
2. **上游已经前进**：aria 到了 v1.74.1（10CG/aria-plugin#182），主仓到了 `0748dbc`。
   - 这段上游对 `skills/audit-engine` 零改动，与本版的测试改动不冲突。
   - 对 `config-loader/SKILL.md` 只加了两行注释，不在 SC-21 读取的 audit 段。
   - 5.1 / 5.3 的取号与并入按既有条款处理。
3. **归档原文仍写两项允许集**：sibling-spec-probe 的归档计划里还是两项。归档是历史记录，不建议改；来由靠 TASK-013 要求补写的 docstring 交代。
4. **「四个」实为三个**：读前必看第 32 条照录的「四个非排除 checkpoint」，在裁定 1 之后实际只有三个。这不影响 SC-15.10 的区分力。
5. **Ran 数可能连带变化**：如果 owner 采纳请裁 8 或其它改测试的裁定，TASK-013 的「恰为 133」和提交条都要随之复核——新增一个方法就会变成 134。
6. **未复跑 v2 两跑**：本席没有复跑 v2_state_runs，依赖主控已做的两次核验。

## Verdict

PASS —— 0C/0M/4m。**Vote: PASS**

## 是否足以开始 Phase B

足以。v2.11 没有 critical 或 major，从 2.6 起每一步都有合法的下一步，新判据在基线、目标和坏实现三种状态下都能区分开。四条 minor 不改变执行动作，可以在 owner 对请裁 1 / 6 / 7 / 8 表态时一并处理，然后按 Status 行续跑。
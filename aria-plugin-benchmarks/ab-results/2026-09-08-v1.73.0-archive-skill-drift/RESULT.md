# AB 结果 — openspec-archive @ v1.73.0 (archive-gate-registration-class-and-skill-drift)

| 字段 | 值 |
|---|---|
| 跑于 | 2026-09-08 |
| Skill | `openspec-archive` |
| 套件 | `ab-suite/openspec-archive.json` (`source_evals_count=4`, `selected_count=2`) |
| 两臂 | **v_new** = 本 Spec 落地后的 SKILL.md · **v_old** = `aria` `301641b` 版 (= v1.71.1, 跑时的 `origin/master`) — 2026-09-09 由可变 ref 勘正为不可变 SHA, 同 :62 |
| 两版差异 | `git -C aria diff --numstat origin/master HEAD -- skills/openspec-archive/SKILL.md` = **63+ / 34−** |
| 触发理由 | Rule #6 第二行「照跑 AB, 零裁量」—— B3 改了 frontmatter `description` |

## 记分

| eval | v_new | v_old | delta | 有区分力的 expectation |
|---|---|---|---|---|
| 1 `correct-archive-path` | 3/3 | 3/3 | 0 | **0** |
| 2 `already-archived-detection` | 3/3 | 3/3 | 0 | 1 (**仅语义分档差, 记分打平**) |
| **合计** | **6/6** | **6/6** | **0** | **1 (不计分)** |

## ⚠️ 区分力评估 — 本次 AB 对本改动**零区分力** (与 Spec 事先登记一致)

本 Spec 的 proposal 在起草期就登记了这个预期 (R2 R1V-6):

> SC-7 要求的 AB 在现有 2 个 eval 上**可预测为零区分** —— 本 Spec 的 D1/D2 正说明该套件测不到 Step 3/4/7。这与 SOT §3 警告的「测量剧场」同形。但 `description` 变动使本变更落第二行是 SOT 的**明文映射**, 不是裁量。**处置**: 照跑, 并在 RESULT.md 显式记录「本次 AB 对本改动零区分力, 区分力缺口见 D1」。

**实测证实了该预期。** 逐条对照本次六项实质改动:

| # | 改动 | 被覆盖? | grader 实测依据 |
|---|---|---|---|
| 1 | Step 3 从「调 `openspec archive` CLI」改为 `git mv` | ❌ 无断言承接 | 两臂答卷**肉眼可辨** (v_old 写 `openspec archive user-auth --yes`; v_new 写 `git mv`), 但三条 expectation 只考「终点路径 / project_root 解析 / 与用户确认」, 都不考机制 |
| 2 | Step 4 断言 (跑 AB 时是四条; **事后被发布前验证席证伪并改成五条** —— 原第四条「proposal.md 存在」在真实坏情形下是绿的, 已换成钉嵌套形状的「`{name}/{name}/` 不存在」。本表描述的是**跑 AB 那一刻**的状态, 不追改) | ❌ 无断言承接 | eval-2 的 expectation 2 上出现**真实语义分档差** —— v_new 是双检查点且点明「`git mv` 在 dst 已存在时**返回 rc 0** 并把 src **嵌进** dst」「四条断言里只有断言 4 会红」; v_old 只有单检查点。但 pass/fail 打平, **没有任何断言去给这个差异打分** |
| 3 | Step 5 并入 Step 3 | ❌ 结构性漏测 | 两臂答卷**零字提及** —— eval-2 是纯只读检测题, 走不到执行态 |
| 4 | Step 7 SHA 回链 + `archive_tracker_verify.py` | ❌ 结构性漏测 | 同上, 两臂输出里 `archive_tracker_verify.py` / SHA 回链**均未出现** |
| 5 | 退役 `keep_changes_copy` | ❌ 有可观测漂移但无断言 | v_old 逐字列出「`skip_verification` / `keep_changes_copy` / `dry_run` /…」, v_new 列「五个 options」且无它 —— **干净的可观测标记, 却无断言承接** |
| 6 | frontmatter `description` 删「自动修正 CLI bug」 | ❌ **本套件按构造永远测不到** | **grader 新发现**: ARM 是被**直接喂 SKILL_MD 路径**的, 触发面按构造被绕过 ⇒ 该套件结构上无法评 `description` 的触发准确率 |

⇒ **不把「跑过了」当「验过了」。** 这 6/6 全过说明的是「两版在这三个维度上都没退步」, **不是**「本次改动被验证了」。

## 与 SOT 验收判据的关系 (如实登记)

`AB_TEST_OPERATIONS.md` §场景 1 的验收是「`delta.pass_rate > 0` (Skill 确实提升了质量)」。**本次 delta = 0, 按该字面不达标。**

如实登记而非绕过: 这个 0 的成因**不是改动没价值**, 而是**套件不覆盖被改的面** —— 六项改动里 5 项在答卷里可观测 (其中 2 项有清晰语义分档差), 但无一条 expectation 去给它们打分; 第 6 项按套件构造永远测不到。

这正是已开的套件缺口单 **`10CG/aria-plugin#190`** 的内容, 本次实跑为它提供了实证。⛔ **不得**据「6/6 全过」删除现有三条 expectation —— grader 明确指出它们对真实采用者仍有效, 只是不测本次改动 (按 SOT「Expectations 编写原则」的判断标准: 语义分档相同才可替换/删除, 而这里是「测的根本是别的维度」)。

## 运行纪律核验 (memory `ab-harness-real-repo`)

AB 跑在**真仓 + 真 origin + 无 sandbox**。跑完实测:

- `git status --porcelain` (排除 `ab-workspace/` 与他轨 `aria-orchestrator` 指针): **零意外写入**
- `git -C aria status --porcelain`: **干净**
- 协调 ref 跑前跑后**逐字节相同** (`e13ef10a`) —— 独立佐证「本套件不触达 `phase1_gate`/`release_gate`」这条判定 (见 tasks.md E-1 的订正史)
- 已按 SOT §场景 1 第 3 条执行 `git fetch origin +refs/aria/coordination:refs/aria/coordination` 强制对齐 (本套件不推 claim, 该清理无害)

## 臂的隔离约束 (memory `ab-baseline-leaks-via-repo-corpus`)

两臂的提示里**显式禁读** `openspec/changes/` / `docs/handoff/` / `.aria/audit-reports/` / `CLAUDE.md` —— 那里有在制规格与交接文档, 会把「正确答案」泄漏给臂。这是对该 memory 记录的两条泄漏通道的针对性封堵。

## 原始产物

- 工作区: `ab-workspace/2026-09-08-archive-skill-drift/` (ARM_INSTRUCTIONS / GRADER_INSTRUCTIONS / skill-snapshot) —— ⚠️ **该目录被 `.gitignore:37` 排除, 不入库**, 本目录下已收录全部承重产物 (逐 eval 的 prompt / grading.json / 两臂 answer.md); v_old 的 SKILL.md 可由 `git -C aria show 301641b:skills/openspec-archive/SKILL.md` 复现 (`301641b` = v1.71.1, 跑时的 `aria origin/master`; sha256 `5593508c02a1c0d39b088e901c97427248f5bb2697199282ddd04bf651825624`)。⚠️ **2026-09-09 勘正**: 原文写的是 `origin/master` —— 那是**可变 ref**。v1.73.0 合入 master 后该命令返回的是 **v_new** (实跑 rc=0, 与当时工作树逐字节相同, 静默给出错误的臂)。复现命令一律钉不可变 SHA。
- 本目录下按 eval 收录: `prompt.txt` / `grading.json` / `v_new/answer.md` / `v_old/answer.md`

# GRADER_CRITIQUE — eval-1-branch-creation-flow

评分结果: `with_skill` 3/3, `old_skill` 1/3 (assertion 2、3 fail)。

---

## 1. 恒真 / 恒假断言

**恒真 1 条: assertion 1「Should create a branch following feature/{spec-name} convention」。**

prompt 原文已经把答案全给了 —— 既给了约定字面 `feature/{spec-name}`, 又给了 spec 名 `oauth2-social-login`。任何一臂只要把两个 token 拼起来回显就 pass, 不需要读技能文件的任何一个字。两臂确实都 pass 了, 而且两臂给出的字符串完全相同 (`feature/oauth2-social-login`)。这条断言的区分力 = 0, 它测的是「模型会不会复制粘贴」。

要让它有信息量, 至少得改成能被违反的形态, 例如: 「分支名中**不得**含 task id」(两臂对此其实有分歧: `old_skill` 主动提出了带 task id 的备选 `feature/backend/TASK-001-oauth2-social-login` 并要求用户二选一), 或「必须在 skill 默认命名规范与用户给定约定冲突时显式指出冲突并说明取舍」。

**恒假: 无。** 三条断言都至少被一臂满足。

**接近恒真但实际有区分力的**: assertion 3。它看起来像样板要求, 但 `old_skill` 真的漏了 —— 它唯一那次 `git branch --show-current` 明确标在「B.1.1 环境验证 (**创建前**)」, 创建后只剩 `git checkout -b` + `git push -u`, 没有任何回读。这条是本 eval 里唯一一条**靠"位置/时序"而不是"关键词是否出现"**判定的断言, 也是三条里质量最高的一条 —— 如果 grader 只 grep 关键词 `git branch --show-current`, 两臂都会被判 pass, 结论会反过来。建议把这类时序要求在断言文本里写死 (「在创建命令**之后**」), 否则不同 grader 会给出相反结果。

---

## 2. 断言完全没覆盖的重要差异

覆盖率很低: 三条断言只碰到 B.1 的三个点, 而两臂的实质差异大部分落在 B.0 和「事实是否被核实」上。

**(a) B.0 carry-id 取值口径 —— 完全未覆盖, 但两臂正好相反。**
- `with_skill`: 「**carry-id 逐字沿用, 不重新拼**。若这条 track 走过 A.1, `--raw-track-id` 必须逐字用 A.1 认领时派生的那一串; 本次未走 A.1, 因此沿用 Spec id」+ 给出后果「两端用不同的串会各认领一条 claim, 收尾 release 只命中一条, 留下悬空认领」。
- `old_skill`: 「`--raw-track-id` 用**本 cycle 的 Spec id** `oauth2-social-login`」—— 只有一句取值, 没有 A.1 派生串的概念, 也没有不一致的后果。

**(b) auto_bootstrap 的 push 语义 —— 未覆盖, 且这是一处事实正误差异 (不是风格差异)。**
- `old_skill`: 「`write_claim` 的 auto_bootstrap 会自建 ref **并 push 到项目 origin**」+ 「副作用告知: 会向 origin 推 `refs/aria/coordination`」。
- `with_skill`: 「bootstrap 走的是 `push=False`(`coordination_ref.py:800`), **它只建本地 ref, 不推远端**。真正推送发生在 `phase1_gate.py` 的 Step 9 `resilient_push`(:880) 和 7a self-resume push(:597)。把「ref 建好了」当成「远端已同步」会高估协调面。」
- 另外 `with_skill` 独有: 「设了 `--no-push` / `ARIA_COORDINATION_NO_PUSH` ——那只抑制推送, claim 照样写本地」这一条 skip 误判排除。

**(c) 事实是否实测 vs 猜测 —— 未覆盖, 差距最大的一项。**
`with_skill` 报出的仓内事实经我逐条复核**全部为真**: `state_scanner.coordination = {enabled:true, mode:"advisory"}`、`audit.checkpoints.post_implementation = "off"`、`.aria/config.json` 无 `phase_b_developer` 块、`refs/remotes/origin/HEAD → refs/remotes/origin/master`、本地无 `main`、当前分支 `feature/a1-entry-claim-duplicate-work-guard`。
`old_skill` 则把基线猜成 `develop` (**本仓不存在 `develop` 分支**, `git branch -a --list '*develop*'` 空), 并把 config 默认值当成事实 (「config-loader 默认 true」——结论碰巧对, 但没读 `.aria/config.json`)。assertion 2 抓到了这个差异的一半 (基线错), 但没有任何断言在问「你的事实是实测的还是默认值/猜的」。

**(d) 陈旧本地基线守卫 —— 未覆盖, `with_skill` 独有。**
`with_skill` 在开分支前加了 `git fetch origin --prune` + `git rev-parse master origin/master` 断言, 并给出理由「长期在 feature 分支上工作时, `git fetch` 只更新 remote-tracking, 本地 `master` 会静默陈旧」。它还用 `origin/master` 而非本地 `master` 作为 `switch -c` 的 start-point, 从机制上避开了陈旧基线。`old_skill` 的 `git checkout -b feature/oauth2-social-login` 不带 start-point ⇒ **从当前所在分支分叉** (本仓即从另一条无关 feature 分支分叉), 这是个实打实的缺陷, 只是 assertion 2 恰好也踩到了它。

**(e) `skip_if: already_on_feature_branch` 的语义 —— 未覆盖, 只有 `with_skill` 处理。**
`with_skill` 明确澄清「指的是『已经在为本任务创建的那条功能分支上』, 不是『在任意一条 feature 分支上』」并据此判定不跳过。`old_skill` 完全没提这个 skip 条件 —— 而它此刻正身处一条 feature 分支上, 这恰恰是最容易误跳的场景。

**(f) 反向: `old_skill` 有几处 `with_skill` 没有、断言也没测的东西 (不应只记 with_skill 的好)。**
- 5 因子评分**逐因子列表** (file_count / cross_directory / task_count / risk_level=+1 / parallel_needed, 合计 1 < 3), 比 `with_skill` 的一句话结论更可审计, 并给了翻转条件 (「8+ 任务或跨 backend+frontend ⇒ ≥3 改 Worktree」)。
- 指出用户给的命名约定**没有 task_id 位**会导致「同一 Spec 下 TASK-002/003 无法各自开分支 (会撞名)」—— 一个真实的设计后果, `with_skill` 只轻描淡写带过。
- 创建前的 `git status --porcelain` 工作区干净检查 + `.gitignore` 五类规则校验 + 开发环境/包管理器校验 —— `with_skill` 全无 (它只在创建**后**跑 `git status --short --branch`)。
- 给了 `git push -u origin feature/oauth2-social-login` 发布分支。

**(g) 交付形态 —— 未覆盖。** `with_skill` 直接给出完整可执行序列并**显式声明「本次是评测/只读上下文, 上面的分支创建命令我没有真的执行」**(诚实边界); `old_skill` 以三个待确认问题收尾 (基线? 分支名? 任务总数?), 把决策推回用户 —— 严格说它**没有完成 B.1**。没有任何断言在问「是否交付了终态还是停在提问」。

---

## 3. 是否引用了 `openspec/changes/a1-entry-claim-duplicate-work-guard/` 下的文档 (语料污染)

**两臂都没有引用该目录下的任何文档。未见污染。**

逐项核过最可疑的三处:

1. `with_skill` 里的 `coordination_ref.py:800` / `phase1_gate.py :880` / `7a self-resume push(:597)` —— 这三个行号**逐字出现在技能文件本身**: `aria/skills/phase-b-developer/SKILL.md:100-102` 写着「⚠️ 勘正: bootstrap 走的是 push=False (coordination_ref.py:800), **它不推**。真正的推送点是 phase1_gate.py 的 Step 9 resilient_push (:880) 与 7a self-resume push (:597)」。技能文件是充分来源, 不必假设读了 spec。反证很硬: `openspec/changes/.../proposal.md:528,671` 和 `detailed-tasks.yaml:673` 引的是**旧口径 `:791-802` / `:856` / `:573`**, 与答案里的 `:880` / `:597` 不同 —— 若答案抄自 spec 文档, 行号会是旧的那组。
2. `with_skill` 提到「本仓当前在 `feature/a1-entry-claim-duplicate-work-guard`」—— 这是 `git branch --show-current` 的返回值 (与真实仓状态一致), 是**分支名**而非该目录下的文档内容; 上下文也明确是在做基线判定。不构成引用。
3. 两臂都出现的「2026-07-11 双子星撞车实证『认领非强制→从不认领』」—— 出自技能文件 `SKILL.md:110` 的 `rationale` 行 (两个版本都有), 与 spec 文档无关。

需要留档的一点 (非污染, 是 harness 事实): `with_skill` 明显对**真实工作仓**跑了只读探测 (`.aria/config.json`、`git symbolic-ref`、本地分支列表), 与 memory `reference_ab_harness_runs_in_real_repo_no_sandbox` 一致。本 eval 里它只做了读操作、且明确声明没执行写操作, 没有产生协调 ref 推送。但这也意味着**两臂面对的"仓内事实可得性"是不对称优势的来源之一** —— `with_skill` 的 assertion 2 靠实测 `origin/HEAD` 拿分, 若换个仓 (默认分支真叫 `develop`), 同一份技能文件会给出不同答案。assertion 2 因此测的是「有没有去查」而不只是「知不知道该用 master」, 这点在解读区分度时要记住。

---

## 4. 对本轮 Rule #6 判读的直接结论

本轮两版技能的差异面 (B.0 carry-id 占位串措辞 + 两段 push 注释勘正) **与本 eval 的三条断言零交集**:

- assertion 1/2/3 全在 B.1 分支创建域, 改动面在 B.0 认领域。
- 两臂在改动面上**确实表现不同** (§2(a)(b): carry-id 口径、`push=False` 勘正、`--no-push` 非 skip 条件), 差异方向与改动意图完全一致 —— 但这个信号**一分未计**, 三条断言全程没碰到它。
- 反过来说: 本 eval 记录的 3:1 分差**不可归因于本轮改动**。它来自 B.1 域的其他差异 (基线分支实测 vs 猜 develop、创建后是否回读活动分支), 那些内容两版技能文件是一致的 —— 属于同题两次采样的模型方差, 不是版本效应。

⇒ 若要让本轮改动可被证伪, 需要**定向 fixture**, 例如: 「session 已走过 A.1 并派生了 carry-id `X-20260905-ab12`, 现在直接进 B.1」——正确回答必须逐字复用 `X-20260905-ab12` 而非重新拼 Spec id; 以及「auto_bootstrap 建了 ref 后远端是否已同步」的直接问法。当前套件对这两点都无覆盖, 建议按 Rule #6「套件覆盖外」档处理并开套件缺口 issue。

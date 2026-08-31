---
checkpoint: post_planning
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-08-31T14:17:15.831Z
context: openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml (+ linked-issue-field-availability + sibling-spec-probe)
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A4-code-reviewer
critical_count: 0
major_count: 0
minor_count: 6
r3_disposition: {closed: 4, partial: 2, not_addressed: 0}
introduced_by_fix: 3
---

# post_planning R4 — A4 code-reviewer (机械一致性镜头, combined-mode 三份, R3 清账后版本)

> 工作树: 主仓 HEAD c120f9e / aria d69091d, 2026-08-31 14:07:32–14:17:15 UTC。六份被审文件 sha256 见「实测记录 [0]」(审前) 与 [9] (审后, 逐行一致); 本席未改任何被审文件, 全部脚本跑在 scratchpad `r4a4/`, 坏输入跑在 scratchpad 副本 (`r4a4/bad_*`, 只改脚本里的路径常量), git 语义演示跑在 scratchpad 本地裸仓 (`r4a4/gitdemo`, 无网络)。R3 → R4 六份的变化: linked tasks.md 4 hunk / linked yaml 3 hunk / sibling tasks.md 5 hunk (+37 行贴文) / sibling yaml 5 hunk / a1 tasks.md 6 hunk / a1 yaml 7 hunk (TASK-040 块移位 + 六条款重写) — 逐 hunk 见 [8]; R3 基线六份由 scratch 副本程序化重建, sha256 与本席 R3 报告 [0] 逐字相等 [0b]。带圈数字在引用被审文本时一律改写为 (n)。

## 摘要

主控点名的四项全部程序化重跑 [1]–[6]: 八项机械检查在三份终版 (25 / 18 / 40 = 83 任务) 全绿 — `yaml.safe_load` 与归档门 `parse_detailed_tasks` 三份 parse_ok, status 集合 = {pending}, 无重复 id, 必需字段 12 项零缺席, `estimated_hours` 逐任务求和 = metadata (50-86 / 55-87 / 97-158), 依赖悬空 / 自依赖 / 环 = 0; **a1 `parent` 序列回到与 tasks.md 相等** (TASK-040 块现位于 :1001, 在 TASK-039 之后, id 单调递增) [1][1b]。三份「机械核验」贴出脚本逐字抽出原样执行, exit 0 且 stdout 与贴文逐行相等 (30 / **60** / 28 行, 0 diff) [2]。探针 `execution_order` 全部 `←` 箭头集合 ⊆ deps, 并列组互不依赖, `phase_b1_preconditions` 声称边 = 实况 [3]。发布链向下可达三份对称: anc(TASK-022) ⊇ 字段 12 个 `aria/` 写任务, anc(TASK-018) ⊇ 探针 16 个, anc(TASK-040) ⊇ 母 30 个 (`TASK-037.dependencies` 已含 TASK-009, TASK-009 的直接依赖者 = [TASK-037]) [4][4b]。残留 grep 十个模式: `未自行加边` / `13 项` / `300s` / `39 tasks` / `eval id 3` 六份**零命中**; `1.68.0` / `1.67.3` / `README.zh-CN.md` / `est_hours:` / `parallelizable` 的命中与 R3 同, 全部是「不写 X / 已改 X」留痕句或贴出脚本正文, 两份 yaml 里只剩 a1 yaml :982 TASK-038 notes 一处留痕 [6]。

R3 本席六条: **4 closed + 2 partial** (逐条见闭合表)。两条 partial 都是「处方两半只落一半」: e9ffaefe 的 5.5 补了 14 点与 CLAUDE.md 但 check 列表仍缺 `m6-claude-md-version`; 10e7cea4 的 :25 子句以「插入」而非「替换」落地, 旧子句连同已被追记推翻的「主控裁量落第 4/5 组」原样留在同一行。

本轮 **0 critical / 0 major / 6 minor**, 全部是贴文 / 状态行 / 单条命令的文本层问题, 无一触依赖图本体、SC 映射、编号或 proposal: (1) 母贴文 `[a]` 链 `aria: TASK-038 -> TASK-040` 因块移位而与依赖方向反向 (b3039ea7, **fix 引入** — 由本席 R3 处方所选的「移块」方案引出, 本席未预见); (2) 探针 :25 子句双写 (9b08c5a9, **fix 引入**); (3) 字段 5.5 check 列表缺一 (e4a5cb08, R3 partial); (4) 字段 TASK-022 v[0] `git -C aria fetch origin github` 语法错 — git 把第二个位置参数当 refspec, 沙箱亲跑 `fatal: couldn't find remote ref github` exit 128 (6c7d0b50, **残留**; R3 A1/A2 两席把这句当模板引用, 母 TASK-040 新写的 v[0] 反而是对的形态); (5) 三份 tasks.md :5 Status 仍「待 R2」而 yaml 已「待 R4」(d3de42d1, 残留; R3 只更新了 yaml 层); (6) 探针 :336「拒绝能力」段描述的是旧 (e) 的输出, (e) 重写后按段落自述配方亲跑, (e) 半句已不是这个脚本会打印的东西 (b7743802, **fix 引入**)。**introduced_by_fix = 3 / 6**, 与 R3 持平 (1/2), 且三条全在展示层 — 按 memory `marginal-return-negative` 已到拐点; 判 **PASS**, 投 **PASS**, 六处定点改动建议以本席脚本定向复核收账, 不再开通用轮。

可证伪性: 三份贴出脚本对坏输入仍全部发红 [6b] — 母脚本三处回退 exit 1 ((a)(b)(c) 各抓一处), 探针新 (e) 对 R3 坏输入 v2 (同文件标并行) 与 **v3 (有边却标并行, R3 时旧 (e) 抓不到)** 都 `RESULT: FAIL`; 母脚本对「TASK-037 丢 TASK-009 边」仍 PASS (R3 处方 (f) 守卫未采, 观察项)。

## R3 finding 逐条闭合表 (本席 R3 1M + 5m, 程序化判)

| R3 id | 严重度 | 判定 | 证据 (实测记录编号) |
|-------|--------|------|---------------------|
| 1a45ef41 | major | **closed** | [4] `TASK-037.dependencies` 首元素 = `TASK-009` (行尾注「aria/ 侧唯一汇点 … R3/A1 f1fec807 · A4 1a45ef41」); `aria/ 侧写任务 30 个; 不在 anc(TASK-040) 的: []`; `TASK-009 的直接依赖者: ['TASK-037']`; 不在 anc(TASK-038) 的只剩 TASK-024 / 036 / 039 (不写 `aria/`, R3 观察 5 已说明)。[4b] 三份对称: 字段 anc(TASK-022) / 探针 anc(TASK-018) / 母 anc(TASK-040) 各覆盖本份全部 `aria/` 写任务; 版本 SOT 任务 (plugin.json) 都在各自发布任务祖先集。处方「顺手加 (f) 守卫」未采 — [6b] 删该边母脚本仍 PASS, 计观察不计 finding |
| 09795e71 | minor | **closed** | [1] a1 `parent 1:1: seq_equal=True set_equal=True`; [1b] yaml ids 尾 4 = 037, 038, 039, 040, parents 尾 4 = 8.1, 8.2, 8.3, 8.4 = tasks.md, `id 单调递增=True`, TASK-040 块起始 :1001 (038 :958 / 039 :984)。**但**移块使贴文 `[a]` 的 `aria` 链渲染反向 ⇒ 新 minor b3039ea7 (处方方案 A 的副作用, 本席 R3 未预见) |
| 64cf8dd9 | minor | **closed** | [7b] :232 含「40 任务」且无 `\b39\b`; :455 含「40 tasks」; :265 改为「两条 deliverable 在 R2 由主控补『只读核验』标注 …; R3 起 TASK-003 不计为写入方 — 本条原文『未标只读, 只更严不更松』已勘正 (R3/A4 64cf8dd9)」(s7 的「含『未标只读』=True」是引号内引旧文, 已由 s10 §5 区分); [6] `\b39\b` a1 两份只剩 yaml :134 `:35-39` 行号 |
| 199aa25c | minor | **closed** | [5] TASK-034 `ARIA_COORDINATION_NO_PUSH=Y`, verification[0] 逐字 = 与 031/032/033/035 同款「运行前置 (Rule #7 射程 + R1 C5): 会话以 `ARIA_COORDINATION_NO_PUSH=1 claude …` 启动 … — R3/A4 199aa25c 补齐 (031–035 五处同句)」; 原引用句保留为 v[1] |
| e9ffaefe | minor | **partial** | [5] yaml TASK-024 title 已「主仓发版同步面 14 点 (与 086ee32 同口径): CLAUDE.md :139/:141 2 点 + …」; tasks.md 5.5 (:82) 已「14 点」+ `CLAUDE.md:139/:141` ✓; **check 列表仍 3 个** (`m6-version-badge-match` / `i18n-readme-translation-currency` / `main-project-version-consistency`), yaml TASK-024 verification[2] 列 4 个, 差集 = `['m6-claude-md-version']` [7 §6] ⇒ 处方后半未落, 计 e4a5cb08 |
| 10e7cea4 | minor | **partial** | [7 §4] :25 TASK-003 子句现含 TASK-004 与「TASK-003 ← TASK-002 (R3/A4 10e7cea4 补)」✓; **但**「各含 TASK-003」在子句内出现 2 次, 旧子句「边: TASK-015 / 016 / 017 `dependencies` 各含 TASK-003, 主控裁量落第 4/5 组」原样保留在新子句之后 (「落第 4/5 组」正是 R3 指出已被追记推翻的半句) ⇒ 插入而非替换, 计 9b08c5a9; 附 :11「只剩第 1 组 (三任务不同文件)」未动 (R3 为「顺手」项, 非处方, 不计) |

## Findings

| id | severity | 来源 | category | scope | type | 描述 + 证据 + 处方 |
|----|----------|------|----------|-------|------|-------------------|
| b3039ea7 | minor | **fix 引入** (R3 09795e71 处方 A「移块」的副作用) | documentation | openspec/changes/a1-entry-claim-duplicate-work-guard/tasks.md#L426 | issue | **母贴文 `[a]` 行 `aria: TASK-038 -> TASK-040` 与依赖方向反向。** 证据 [7 §1]: 贴文 20 条链逐对检查「x -> y ⇒ x ∈ anc(y)」, 19 条链全部成立 (`->` 恰是依赖 / 执行方向), 唯一不成立的对 = (aria, TASK-038, TASK-040): 实况 `TASK-038.dependencies = [TASK-037, TASK-040]`, 即 040 先 038 后, 与 8.4 行「执行序 8.1 → 8.4 → 8.2」相反。根因: 贴出脚本 `print(f"      {path}: {' -> '.join(ws)}")` 按 yaml 块序渲染, R3 前 040 块在 038 前故巧合正确, 移块后翻转; 检查 (a) 本身无向 (`a in anc[b] or b in anc[a]`), 对方向免疫 (memory `invariant-dimension`), 于是「渲染错了方向, 断言仍绿」。为什么重要: 这行是 R1 C1「同文件串行」的证据面, 读者按它会先 bump gitlink 再双推 — 恰是 orphaned gitlink (#165) 形状; TASK-040 v[5] 的时序承诺在贴文里被反着写。处方: 脚本打印前按依赖序排 (`ws = sorted(ws, key=lambda t: len(anc[t] & set(ws)))` 一行) 后重贴 (R3 后重跑一次, 三份贴文=实跑要重验); 或最低限度在 :426 行尾注「(块序; 依赖序 040 → 038)」 |
| 9b08c5a9 | minor | **fix 引入** (R3 10e7cea4 清账为插入非替换) | documentation | openspec/changes/sibling-spec-probe/tasks.md#L25 (TASK-003 子句) | issue | **组间门 TASK-003 子句双写, 旧子句仍含被追记推翻的「主控裁量落第 4/5 组」。** 证据 [7 §4] 子句逐字: 「… 边: TASK-004 (第 2 组起点, 主控 R1 追记) / 015 / 016 / 017 的 `dependencies` 各含 TASK-003, 且 TASK-003 ← TASK-002 (R3/A4 10e7cea4 补); **边: TASK-015 / 016 / 017 `dependencies` 各含 TASK-003, 主控裁量落第 4/5 组**)」— 「各含 TASK-003」×2, 「落第 4/5 组」仍在 (实况落第 2/4/5 组, yaml `phase_b1_preconditions[1]` 已改)。为什么重要: 同一行对同一道门给两套边清单, 后者少一条最强的门边 (TASK-004) 且组号错; 这是 memory `fix-the-class` 的反面 — 加了对的没删错的。处方: 删「; 边: TASK-015 / 016 / 017 `dependencies` 各含 TASK-003, 主控裁量落第 4/5 组」; 顺手把 :11「(三任务不同文件)」改「(001 ‖ 002 不同文件; 003 ← 002)」 |
| e4a5cb08 | minor | **R3 partial** (e9ffaefe 处方后半) | documentation | openspec/changes/linked-issue-field-availability/tasks.md#L82 (5.5) | issue | **5.5 的 custom check 列表缺 `m6-claude-md-version`。** 证据 [7 §6]: 5.5 check 集合 = {`m6-version-badge-match`, `i18n-readme-translation-currency`, `main-project-version-consistency`}; yaml TASK-024 verification[2] = 上述 + `m6-claude-md-version` (`.aria/state-checks.yaml` 四名皆实存 [5])。为什么重要: 本轮把 `CLAUDE.md:139/:141` 两点补进了 5.5, 却没补它们的机械兜底 — 改动点进了 checkbox, 兜底没进; 执行者按 5.5 跑三条 check 全绿仍可能漏 CLAUDE.md。处方: 5.5 列表加 `` `m6-claude-md-version` `` 一 token |
| 6c7d0b50 | minor | **残留** (R2 已在; 本席 R2/R3 未抓, R3 A1/A2 当模板引用) | implementation | openspec/changes/linked-issue-field-availability/detailed-tasks.yaml#TASK-022 | issue | **TASK-022 verification[0] 的新鲜度前置命令 `git -C aria fetch origin github` 不是「取两个 remote」, 而是「从 origin 取名为 github 的 refspec」。** 证据 [7b]: scratchpad 本地两裸仓 (remote 名 origin / github, git 2.39.5) 亲跑 `git fetch origin github` ⇒ `fatal: couldn't find remote ref github`, exit 128, 什么都没取; `git fetch origin && git fetch github` exit 0; `git fetch --multiple origin github` exit 0 (Fetching origin / Fetching github)。对照 [7 §2]: 母 TASK-040 v[0] (R3 新写) = `git -C aria fetch origin && git -C aria fetch github` (正确形态) — R3 清账「六条款逐字对齐 TASK-022」时命令被改对了, 但没回写模板, 现在孪生对里错的是模板那份; R3 A2 报告 :96 表格逐字引用 `git -C aria fetch origin github` 作为 022 的「前置新鲜度」范式, A1 :61 同, 两席都没执行过它。为什么重要: 这条款存在的目的就是 memory `stale-local-main` (合进陈旧基线抹掉他人工作); 命令失败后若被 `;` 链或人工忽略, 「本地 master == origin/master == github/master」会对**未刷新**的 remote-tracking ref 判真 — 恰是它要防的情形。判 minor 非 major: 失败是响亮的 (exit 128 + fatal), 非静默; 修复一 token; 且 TASK-023 (standards) 的对应句只写「前置: 本地 master == origin/master == github/master」无命令, 不受影响。处方: 改为 `git -C aria fetch origin && git -C aria fetch github` (与 TASK-040 同款); tasks.md 5.3 无 fetch 句, 不用动 |
| d3de42d1 | minor | **残留** (R2 清账起陈旧; R3 只更新 yaml 层加深两层不一致) | documentation | openspec/changes/{linked-issue-field-availability,sibling-spec-probe,a1-entry-claim-duplicate-work-guard}/tasks.md#L5 (Status) | issue | **三份 tasks.md :5 Status 行仍说「待 R2」, 三份 yaml `metadata.status` 已说「R3 清账 2026-08-31; 待 R4 收敛判定」。** 证据 [7 §3]: linked :5「… 待 `post_planning` R2 审计 (config … enabled …)」/ sibling :5「… 待 R2」/ a1 :5「… R2 待跑 (config `audit.checkpoints.post_planning`, Rule #10 不自行豁免)」; 三份 yaml :25/:66/:25 status 尾「待 R4 收敛判定」。R3 聚合 minor 表「三份 `metadata.status` 更新到 R3 (A1)」只做了 yaml。为什么重要: Status 行是 handoff / 归档门 / 人读的第一行事实 (memory `spec-frontmatter-reflects-reality`), 两层对同一事实相差两轮。处方: 三处 :5 改为「post_planning R1–R3 已跑并清账 (2026-08-31, 对账见文末); 待 R4 收敛判定」(或逐字抄各自 yaml status) |
| b7743802 | minor | **fix 引入** (R3 (e) 扩维后「拒绝能力」段未重跑) | documentation | openspec/changes/sibling-spec-probe/tasks.md#L336 | issue | **「拒绝能力」段声称「同一脚本对清账前依赖图 … (e) 『[并行, RED]』行 10 对同文件 + 『[并行] TASK-011 · TASK-012』1 对」, 但 (e) 已在 R3 重写, 新脚本对该段自述配方的输出不是这个。** 证据 [6b (d)]: 按段落逐字配方还原 (TASK-005~009 deps=[TASK-004] / 012=[010,007] / 014=[011,012,013] / 015=[009] / 016=[009,015] / 两处「并行」行取 R1 基线原文) 跑当前贴出脚本: (a) 13 对缺边 ✓ (d) 两条 ✓ 与段落一致; (e) 实际输出 = RED 行 `dep-contradiction` **5 对** + `same-file pairs` **15 对** (新 (e) 的回退表达式 `ids_in(stripped)` 把 `← 004` 的 004 也算进并行集), 「[并行] TASK-011 · TASK-012」行被当成一段箭头 `TASK-011 ← [010, 005, 006, 012, 010, 007]` ⇒ `NOT IN deps ['TASK-012', 'TASK-007']` + 7 对矛盾 + 9 对同文件 (含 `('TASK-010', 'TASK-010')` 自对), 另有 TASK-014 / 015 / 016 三条 `NOT IN deps` 段落未提。结论 `RESULT: FAIL` 仍成立, 但 (e) 半句是旧脚本的结果为新脚本背书 (memory `check-runs-at-baseline-first`: 新写的机械检查先在基线亲跑再写进规格)。顺带: 新 (e) 的 `ids_in` 不去重、不排除 head 自身, 坏输入 v2 输出里出现 `('TASK-005', 'TASK-005')` / 重复对 [6b (c)], 当前文件上无影响。处方: 用当前脚本重跑该配方, (e) 半句改成实际摘要 (或只留「(e) 亦 FAIL: RED 行 5 对矛盾 + 15 对同文件; 011·012 行 1 条箭头不在 deps + 7 对矛盾」); 可选 `ids_in` 去重并排除 head |

**观察 (不计 finding, 留痕)**:

1. 母贴出脚本对「TASK-037 丢 TASK-009 边」抓不到 ([6b (b)] `RESULT: PASS`): 1a45ef41 以加边闭合, R3 处方 (f)「anc(发布任务) ⊇ `aria/` 写任务」守卫未采; 图现在对但无机械守卫, B 期若再改 deps 建议重跑本席 `s3_task040.py` / `s3b_release_reach.py`。
2. 母 tasks.md「可证伪性」坏输入块的数字是 R1 时代的 (`[a] 40 对 / 19 个`, `[d] 51 对`), 现文件上同款三处回退得 `38 / 20 / 55` [6b (a)]; 该块自述为 R1 亲跑且明写「(026~030 同, 略)」, 不是对当前文件的声明, 不计; 与 b7743802 同形, 执笔席修 b7743802 时可顺手重贴。
3. 已证伪检验 — TASK-002 新增「另记录」判别式 `grep -n 'Linked Issue' aria/skills/spec-drafter/SKILL.md`: 今日 (aria d69091d) **零命中** ⇒ 判「未 ship (ii)」正确; 字段 TASK-014 / TASK-015 两 hunk 的 verification 都含 `**Linked Issue**` 字面 ⇒ ship 后必命中; 判别式两态都成立。
4. TASK-040 v[1] 合并源字面 `feature/a1-entry-claim-duplicate-work-guard` 在计划里无第二锚点 (B.1 建分支不是任务), 与 aria 仓既有 12 条 `feature/<slug>` 形态一致; 同块 deliverable 注释仍写 `feature/<branch>` 占位 — 不判缺陷。
5. 探针 TASK-018 (knowledge-manager 发布同步) 的对应条款用词与 TASK-022/040 不同 (`git merge` / `timeout`), 授权句已补 (R3 只要求这一句) [7 §2 的 018 列 N 是关键词不同, 非缺席]。
6. chk1 a1「后向边」新增 `(TASK-038, TASK-040)` 是编号追加的预期形态, 8.4 行已声明「编号不可变, 列于末不代表最后做」。
7. 带圈数字计数 (owner 可读性偏好, 非本轮镜头, 全为既有文本, 不计): a1 yaml 52 / a1 tasks.md 27 / 探针 3 + 3 / 字段 0 + 0 [7 §8]。
8. 已证伪的怀疑: 三份 `metadata.status` 已到 R3 [7 §3]; TASK-040 无「300」且含「不写具体秒数」[7 §2]; `12 点` 六份零命中 [6]; a1 proposal Status 已「40 tasks」(proposal 非本席被审对象) [7 §7]; 字段 yaml `新增 新 eval` 叠字仍 1 处 (R3 观察 2, 无语义影响) [7c]。

## 实测记录 (脚本 + 逐字输出; 主仓 HEAD c120f9e / aria d69091d; 2026-08-31 14:07:32–14:17:15 UTC)

复用脚本 (逐字 copy 自 `r3a4/`, sha256 前 16 位): `chk1_battery.py` 1126bb3f6ee840ac (全文见 R2 报告 [1]) · `chk3_cov_deliv.py` e5cb00f33ea3a0ab (R2 [3]) · `s2_execorder.py` 136195e84f804fe0 (R3 [3]) · `s3_task040.py` 979c90bfd2f834cb (R3 [4]) · `s4_flags_summary.py` 83d6e70faf4e5b69 (R3 [5]) · `s7_misc.py` d0b0593e5f49a772 (R3 [7])。改动脚本: `extract_run_pasted.py` (只改 OUT 路径 r3a4 → r4a4) · `s1b_parent_seq.py` (k=None 时不索引)。新脚本全文见各段。

### [0] 被审六份 sha256 (审前, 2026-08-31T14:07:32.330Z)

```
084835ef3bb86c5ebd9842c3afaa69874f5b220170aaa0a060d1e83cc0db1e16  openspec/changes/linked-issue-field-availability/tasks.md
471f30adbfb28c745898ec8a730589e5a146427d006f2d8cfddd79ff0fac3d1d  openspec/changes/linked-issue-field-availability/detailed-tasks.yaml
464216dd14ea1ed8dbd5ad43d0ecbed19a6b0e8525ec4470a92887b78c37f99a  openspec/changes/sibling-spec-probe/tasks.md
9448d8d8f49ca66179d26b8e13ca5b3c569b3de5438aa63f8f852ed81313d85e  openspec/changes/sibling-spec-probe/detailed-tasks.yaml
3830f3a51b01fea144e4af3a72783fca69a159b22350217adc25556e271da583  openspec/changes/a1-entry-claim-duplicate-work-guard/tasks.md
7c5a7ea50db723192fb2a2c479a5e3326daf898cea151809a3f09685213320f4  openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml
```

### [0b] R3 基线六份程序化重建 (供 [8] diff) — 脚本 `s0_baseline.py`

```python
#!/usr/bin/env python3
"""R4/A4 [0b] 重建 R3 六份基线 (供 R3→R4 diff): 4 份有逐字副本; a1 yaml = R3 坏输入副本回退 3 处; sibling yaml = R3 adv v2 副本回退 1 处; linked yaml = R2 副本回退坏输入 + 套用 R3 报告 [8] 记录的 R2→R3 hunk. 每份与 R3 报告 [0] sha256 比对."""
import hashlib, pathlib, re, shutil
SP=pathlib.Path("/tmp/claude-1000/-home-dev-Aria/0335d8a8-ad33-4d3d-9787-8f5ca5adea98/scratchpad"); B=SP/"r4a4/r3base"
R3SHA={"linked-issue-field-availability/tasks.md":"d5b1429e030a2e8e5cffdcdab53ca408aa92e8e3d00ce2e4b63363db64281250",
"linked-issue-field-availability/detailed-tasks.yaml":"824c6a11db6a0cfc598e278c3b155225df16eeaa22ec5f10a364cae053c3cb72",
"sibling-spec-probe/tasks.md":"2de1da5716d8e219d9454763c962596611880594d7252403eb207fc6d5946574",
"sibling-spec-probe/detailed-tasks.yaml":"26beac498ed367d1aee47a726c8c3defa0d6dcf1ee4ceaeddf10c00c242889d8",
"a1-entry-claim-duplicate-work-guard/tasks.md":"b83cc8d3496c61c7c4d09db1bbcb9fa31469d96b7a642667d879841b10e0e81f",
"a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml":"99a9baeaa6d10d105890ca7c7a1e8a799af00de196f384092109bebf460f7161"}
def sha(t): return hashlib.sha256(t.encode("utf-8")).hexdigest()
out={}
out["linked-issue-field-availability/tasks.md"]=(SP/"r2a4/bad/openspec/changes/linked-issue-field-availability/tasks.md").read_text(encoding="utf-8")
out["sibling-spec-probe/tasks.md"]=(SP/"r3a4/adv/openspec/changes/sibling-spec-probe/tasks.md").read_text(encoding="utf-8")
out["a1-entry-claim-duplicate-work-guard/tasks.md"]=(SP/"r3a4/bad_a1/openspec/changes/a1-entry-claim-duplicate-work-guard/tasks.md").read_text(encoding="utf-8")
# a1 yaml: 回退 R3 adv.py 三处坏输入
y=(SP/"r3a4/bad_a1/openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml").read_text(encoding="utf-8")
def block(y,tid): return re.search(rf"(  - id: {tid}\n.*?)(?=\n  - id: TASK-|\Z)", y, re.S).group(1)
b=block(y,"TASK-016"); nb=re.sub(r"(dependencies: \[[^\]]*?)\]", r"\1, TASK-015]", b, count=1); assert nb!=b; y=y.replace(b,nb)
b=block(y,"TASK-025"); nb=b.replace(", TASK-017]", "]", 1); assert nb!=b; y=y.replace(b,nb)
b=block(y,"TASK-004"); nb=b.replace("SC-x","SC-3"); assert nb!=b and "SC-x" not in nb; print("TASK-004 块 SC-x 回退处数:", b.count("SC-x")); y=y.replace(b,nb)
out["a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml"]=y
# sibling yaml: adv v2 回退 1 行
y=(SP/"r3a4/adv/openspec/changes/sibling-spec-probe/detailed-tasks.yaml.v2").read_text(encoding="utf-8")
y2=y.replace('  - "[并行, RED] TASK-005', '  - "[串行 (同文件 tests/test_sibling_spec_probe.py), RED] TASK-005', 1); assert y2!=y
out["sibling-spec-probe/detailed-tasks.yaml"]=y2
# linked yaml: R2 副本 (含本席 R2 坏输入 @465) → 回退坏输入 → 套 R2→R3 hunk (R3 报告 [8]: eval id 3 ×5 处同款替换 + @627 一行)
y=(SP/"r2a4/bad/openspec/changes/linked-issue-field-availability/detailed-tasks.yaml").read_text(encoding="utf-8")
y2=y.replace("    dependencies: [TASK-014, TASK-015]   # +TASK-016:", "    dependencies: [TASK-016, TASK-014, TASK-015]   # +TASK-016:",1); assert y2!=y; y=y2
n=y.count("eval id 3"); y=y.replace("eval id 3","新 eval (id = ship 时 max(id)+1, 今日观测 3)")
old627='      - "12 个引用点全部改为 ship 号 <vNEXT> (owner 裁定规则见 TASK-021 notes; 行号按 c120f9e 实读, 落地时以 grep 为准); `grep -rn \'1\\\\.67\\\\.2\' VERSION README.md README.*.md` 零命中"'
new627='      - "14 个引用点 (与 086ee32 同口径: CLAUDE.md:139/:141 + VERSION + README.md:8/:242 + i18n ×3 各 :3/:10/:244) 全部改为 ship 号 <vNEXT> (owner 裁定规则见 TASK-021 notes; 行号按 c120f9e 实读, 落地时以 grep 为准); `grep -rn \'1\\\\.67\\\\.2\' VERSION README.md README.*.md CLAUDE.md` 零命中"'
assert old627 in y, "627 old line not found"; y=y.replace(old627,new627,1)
out["linked-issue-field-availability/detailed-tasks.yaml"]=y
print(f"linked yaml: 'eval id 3' 替换 {n} 处")
for k,t in out.items():
    p=B/k; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(t,encoding="utf-8")
    print(f"{'OK ' if sha(t)==R3SHA[k] else 'MISMATCH'}  {sha(t)[:16]}  {k}")
```

输出 (六份 sha256 与本席 R3 报告 [0] 逐字相等):

```
TASK-004 块 SC-x 回退处数: 2
linked yaml: 'eval id 3' 替换 6 处
OK   d5b1429e030a2e8e  linked-issue-field-availability/tasks.md
OK   2de1da5716d8e219  sibling-spec-probe/tasks.md
OK   b83cc8d3496c61c7  a1-entry-claim-duplicate-work-guard/tasks.md
OK   99a9baeaa6d10d10  a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml
OK   26beac498ed367d1  sibling-spec-probe/detailed-tasks.yaml
OK   824c6a11db6a0cfc  linked-issue-field-availability/detailed-tasks.yaml
```

### [1] 检查 1/3/6/7 — 字节卫生 · 两解析器 · status 枚举 · parent 1:1 · 必需字段 · estimated_hours 形态与求和 · 无重复 id · deps 悬空/自依赖/环 · 后向边 · RED→GREEN 方向 · agent 集合 (`chk1_battery.py` 逐字复用, exit 0)

```

===== linked-issue-field-availability
  CRLF=0 tab=0 ctrl=0
  safe_load OK: tasks=25 dup_ids=[] total_tasks(meta)=25
  parse_detailed_tasks: parse_ok=True n=25 statuses=['pending'] reason='25 task(s) parsed'
  status 枚举=['pending']
  parent 1:1: parents==25 boxes==25 seq_equal=True set_equal=True orphan_parent=[] orphan_box=[]
  必需字段缺失=none
  estimated_hours 全为 'a-b' 串: True bad=[]; est_hours 残留=[]; meta.estimated_hours='50-86'
  逐任务求和 lo-hi = 50-86
  deps: 悬空=[] 自依赖=[] 环=[]
  后向边 (依赖编号更大者) = []
  RED 任务=['TASK-005', 'TASK-006']
  RED 传递依赖 GREEN (实现/文本) = none
  agents=['backend-architect', 'knowledge-manager', 'qa-engineer', 'tech-lead']; agent_allocation keys=['backend-architect', 'knowledge-manager', 'new_agents', 'note', 'qa-engineer', 'tech-lead']

===== sibling-spec-probe
  CRLF=0 tab=0 ctrl=0
  safe_load OK: tasks=18 dup_ids=[] total_tasks(meta)=18
  parse_detailed_tasks: parse_ok=True n=18 statuses=['pending'] reason='18 task(s) parsed'
  status 枚举=['pending']
  parent 1:1: parents==18 boxes==18 seq_equal=True set_equal=True orphan_parent=[] orphan_box=[]
  必需字段缺失=none
  estimated_hours 全为 'a-b' 串: True bad=[]; est_hours 残留=[]; meta.estimated_hours='55-87'
  逐任务求和 lo-hi = 55-87
  deps: 悬空=[] 自依赖=[] 环=[]
  后向边 (依赖编号更大者) = []
  RED 任务=['TASK-004', 'TASK-005', 'TASK-007', 'TASK-008', 'TASK-009', 'TASK-014']
  RED 传递依赖 GREEN (实现/文本) = [('TASK-014', ['TASK-010', 'TASK-011', 'TASK-012', 'TASK-013'])]
  agents=['backend-architect', 'knowledge-manager', 'qa-engineer', 'tech-lead']; agent_allocation keys=['backend-architect', 'knowledge-manager', 'qa-engineer', 'tech-lead']

===== a1-entry-claim-duplicate-work-guard
  CRLF=0 tab=0 ctrl=0
  safe_load OK: tasks=40 dup_ids=[] total_tasks(meta)=40
  parse_detailed_tasks: parse_ok=True n=40 statuses=['pending'] reason='40 task(s) parsed'
  status 枚举=['pending']
  parent 1:1: parents==40 boxes==40 seq_equal=True set_equal=True orphan_parent=[] orphan_box=[]
  必需字段缺失=none
  estimated_hours 全为 'a-b' 串: True bad=[]; est_hours 残留=[]; meta.estimated_hours='97-158'
  逐任务求和 lo-hi = 97-158
  deps: 悬空=[] 自依赖=[] 环=[]
  后向边 (依赖编号更大者) = [('TASK-017', 'TASK-022'), ('TASK-017', 'TASK-025'), ('TASK-018', 'TASK-025'), ('TASK-019', 'TASK-026'), ('TASK-020', 'TASK-030'), ('TASK-021', 'TASK-028'), ('TASK-021', 'TASK-030'), ('TASK-022', 'TASK-027'), ('TASK-023', 'TASK-029'), ('TASK-038', 'TASK-040')]
  RED 任务=['TASK-004', 'TASK-005', 'TASK-007', 'TASK-008', 'TASK-009', 'TASK-010', 'TASK-025', 'TASK-027', 'TASK-028', 'TASK-029', 'TASK-030']
  RED 传递依赖 GREEN (实现/文本) = none
  agents=['backend-architect', 'knowledge-manager', 'qa-engineer', 'tech-lead']; agent_allocation keys=None
```

> 注: sibling「RED 传递依赖 GREEN = TASK-014 → 010~013」仍为启发式误捕 (TASK-014 task_group=G3, GREEN 收口任务), R2/R3 同注; a1 `agent_allocation keys=None` 因 a1 用 `metadata.agent_roster` 列表 (集合相等见 [5])。a1 后向边比 R3 多一条 `(TASK-038, TASK-040)` = 编号追加的预期形态 (观察 6)。**a1 `seq_equal=True`** 是本轮相对 R3 的结构层变化 → [1b]。

### [1b] a1 yaml 块序 vs tasks.md checkbox 序 (`s1b_parent_seq.py`, R3 版加 k=None 守卫)

```python
#!/usr/bin/env python3
"""R3/A4 [1b] a1 yaml 任务块物理顺序 vs tasks.md checkbox 顺序 (chk1 seq_equal=False 的定位)."""
import yaml, re
p="/home/dev/Aria/openspec/changes/a1-entry-claim-duplicate-work-guard/"
raw=open(p+"detailed-tasks.yaml",encoding="utf-8").read(); T=yaml.safe_load(raw)["tasks"]
md=open(p+"tasks.md",encoding="utf-8").read()
ps=[t["parent"] for t in T]; ids=[t["id"] for t in T]
boxes=re.findall(r"^- \[[ x]\] (\d+\.\d+) ", md, re.M)
print("yaml ids 尾 4:", ids[-4:], "| yaml parents 尾 4:", ps[-4:], "| tasks.md boxes 尾 4:", boxes[-4:])
k=next((i for i,(a,b) in enumerate(zip(ps,boxes)) if a!=b),None)
print(f"首个不等位置 index={k}" + (f": yaml={ps[k]} md={boxes[k]}" if k is not None else " (全部相等)") + f"; set_equal={set(ps)==set(boxes)}; id 单调递增={ids==sorted(ids)}")
print("TASK-040 块起始行:", raw[:raw.find("  - id: TASK-040")].count("\n")+1, "; TASK-038 块起始行:", raw[:raw.find("  - id: TASK-038")].count("\n")+1, "; TASK-039 块起始行:", raw[:raw.find("  - id: TASK-039")].count("\n")+1)
```

```
yaml ids 尾 4: ['TASK-037', 'TASK-038', 'TASK-039', 'TASK-040'] | yaml parents 尾 4: ['8.1', '8.2', '8.3', '8.4'] | tasks.md boxes 尾 4: ['8.1', '8.2', '8.3', '8.4']
首个不等位置 index=None (全部相等); set_equal=True; id 单调递增=True
TASK-040 块起始行: 1001 ; TASK-038 块起始行: 958 ; TASK-039 块起始行: 984
```

### [2] 三份 tasks.md「机械核验」贴出脚本逐字抽出 → 原样执行 → 与贴出输出逐行 diff (`extract_run_pasted.py`, 与 R3 唯一差异 = OUT 路径)

```python
#!/usr/bin/env python3
"""R3/A4: 从各 tasks.md `## 机械核验` 段抽第一个 ```python 块逐字落盘并原样执行 (cwd=/home/dev/Aria), 再抽贴出输出块与亲跑 stdout 逐行 diff."""
import re, subprocess, sys, difflib, pathlib
ROOT="/home/dev/Aria/openspec/changes/"
OUT=pathlib.Path("/tmp/claude-1000/-home-dev-Aria/0335d8a8-ad33-4d3d-9787-8f5ca5adea98/scratchpad/r4a4")
SPECS={"linked-issue-field-availability":"linked","sibling-spec-probe":"sibling","a1-entry-claim-duplicate-work-guard":"a1"}
for s,short in SPECS.items():
    md=open(ROOT+s+"/tasks.md",encoding="utf-8").read()
    sec=md.split("机械核验",1)[1] if "机械核验" in md else ""
    # 找 `## 机械核验` 或 `### 机械核验` 标题之后的段
    m=re.search(r"^#{2,3} 机械核验.*?$", md, re.M)
    sec=md[m.end():]
    code=re.search(r"```python\n(.*?)```", sec, re.S).group(1)
    # 贴出输出: 第一个 ```(text)?\n 块 (代码块之后)
    after=sec[sec.find("```python"):]
    after=after[after.find("```", 10)+3:]  # skip code block
    outm=re.search(r"```(?:text)?\n(.*?)```", after, re.S)
    pasted=outm.group(1)
    p=OUT/f"pasted_{short}.py"; p.write_text(code,encoding="utf-8")
    dbl=("\\\\d" in code) or ("\\\\[" in code) or ("\\\\." in code)
    r=subprocess.run([sys.executable,str(p)],cwd="/home/dev/Aria",capture_output=True,text=True)
    (OUT/f"pasted_{short}_stdout.txt").write_text(r.stdout,encoding="utf-8")
    (OUT/f"pasted_{short}_expected.txt").write_text(pasted,encoding="utf-8")
    print(f"===== {s}: code_lines={code.count(chr(10))} double_backslash={dbl} exit={r.returncode}")
    if r.stderr.strip(): print("  STDERR:", r.stderr.strip()[:600])
    got=[l.rstrip() for l in r.stdout.splitlines()]
    exp=[l.rstrip() for l in pasted.splitlines()]
    d=list(difflib.unified_diff(exp,got,fromfile="pasted-in-tasks.md",tofile="actual-run",lineterm="",n=0))
    print(f"  pasted_lines={len(exp)} actual_lines={len(got)} identical={got==exp}")
    if d: print("  DIFF:\n    "+"\n    ".join(d[:80]))
    print(f"  last line actual: {got[-1] if got else None!r}")
```

```
===== linked-issue-field-availability: code_lines=90 double_backslash=False exit=0
  pasted_lines=30 actual_lines=30 identical=True
  last line actual: 'RESULT: PASS'
===== sibling-spec-probe: code_lines=105 double_backslash=False exit=0
  pasted_lines=60 actual_lines=60 identical=True
  last line actual: 'RESULT: PASS'
===== a1-entry-claim-duplicate-work-guard: code_lines=129 double_backslash=False exit=0
  pasted_lines=28 actual_lines=28 identical=True
  last line actual: 'RESULT: PASS'
```

亲跑 stdout 落盘 `r4a4/pasted_{linked,sibling,a1}_stdout.txt`, 贴文落盘 `pasted_*_expected.txt`, 三对文件 `identical=True`。探针脚本 92 → 105 行 ((e) 扩维), 贴文 44 → 60 行。

### [3] 探针 `execution_order` 箭头 / 并列 vs `dependencies`; `phase_b1_preconditions` 声称边 vs 实况 (`s2_execorder.py` 逐字复用)

```
  L0 TASK-003 ← ['TASK-002'] ⊆ deps ['TASK-002'] : OK
  L0 并列组 TASK-001 ‖ TASK-002: 互不在对方传递 deps = True
  L0 含「并行」字样, 行内任务=['TASK-001', 'TASK-002', 'TASK-003']; 行内有直接依赖边的对: [('TASK-002', 'TASK-003')]
  L1 TASK-004 ← ['TASK-001', 'TASK-002', 'TASK-003'] ⊆ deps ['TASK-001', 'TASK-002', 'TASK-003'] : OK
  L2 TASK-005 ← ['TASK-001', 'TASK-004'] ⊆ deps ['TASK-001', 'TASK-004'] : OK
  L2 TASK-006 ← ['TASK-001', 'TASK-005'] ⊆ deps ['TASK-001', 'TASK-005'] : OK
  L2 TASK-007 ← ['TASK-001', 'TASK-006'] ⊆ deps ['TASK-001', 'TASK-006'] : OK
  L2 TASK-008 ← ['TASK-001', 'TASK-007'] ⊆ deps ['TASK-001', 'TASK-007'] : OK
  L2 TASK-009 ← ['TASK-001', 'TASK-008'] ⊆ deps ['TASK-001', 'TASK-008'] : OK
  L3 TASK-010 ← ['TASK-004', 'TASK-008'] ⊆ deps ['TASK-004', 'TASK-008'] : OK
  L4 TASK-011 ← ['TASK-005', 'TASK-006', 'TASK-010'] ⊆ deps ['TASK-005', 'TASK-006', 'TASK-010'] : OK
  L4 TASK-012 ← ['TASK-007', 'TASK-010', 'TASK-011'] ⊆ deps ['TASK-007', 'TASK-010', 'TASK-011'] : OK
  L5 TASK-013 ← ['TASK-007', 'TASK-012'] ⊆ deps ['TASK-007', 'TASK-012'] : OK
  L6 TASK-014 ← ['TASK-009', 'TASK-011', 'TASK-012', 'TASK-013'] ⊆ deps ['TASK-009', 'TASK-011', 'TASK-012', 'TASK-013'] : OK
  L7 TASK-015 ← ['TASK-003', 'TASK-009'] ⊆ deps ['TASK-003', 'TASK-009'] : OK
  L8 TASK-016 ← ['TASK-003', 'TASK-009', 'TASK-015'] ⊆ deps ['TASK-003', 'TASK-009', 'TASK-015'] : OK
  L9 TASK-017 ← ['TASK-003', 'TASK-014', 'TASK-015', 'TASK-016'] ⊆ deps ['TASK-003', 'TASK-014', 'TASK-015', 'TASK-016'] : OK
箭头/并列 fails: none
  precond[0] TASK-001 声称上游边 ['TASK-004', 'TASK-005', 'TASK-006', 'TASK-007', 'TASK-008', 'TASK-009']; 不含该边的: none; 实际直接含 TASK-001 的: ['TASK-004', 'TASK-005', 'TASK-006', 'TASK-007', 'TASK-008', 'TASK-009']; 声称未列: none
  precond[1] TASK-003 声称上游边 ['TASK-004', 'TASK-015', 'TASK-016', 'TASK-017']; 不含该边的: none; 实际直接含 TASK-003 的: ['TASK-004', 'TASK-015', 'TASK-016', 'TASK-017']; 声称未列: none
```

### [4] TASK-040 试派生 / 发布链祖先闭包 vs `aria/` 侧写任务 / gitlink 实存 / remote 与 tag 形态 (`s3_task040.py` 逐字复用; R3 1a45ef41 闭合)

```
TASK-040 deps: ['TASK-037'] | TASK-038 deps: ['TASK-037', 'TASK-040'] | TASK-037 deps: ['TASK-009', 'TASK-011', 'TASK-012', 'TASK-013', 'TASK-014', 'TASK-015', 'TASK-016', 'TASK-017', 'TASK-018', 'TASK-019', 'TASK-020', 'TASK-021', 'TASK-022', 'TASK-023', 'TASK-025', 'TASK-026', 'TASK-027', 'TASK-028', 'TASK-029', 'TASK-030', 'TASK-031', 'TASK-032', 'TASK-033', 'TASK-034', 'TASK-035']
aria/ 侧写任务 30 个; 不在 anc(TASK-040) 的: []
不在 anc(TASK-038) 的任务 (除自身): ['TASK-024', 'TASK-036', 'TASK-039']
  TASK-004 的直接依赖者: ['TASK-011']
  TASK-005 的直接依赖者: ['TASK-006', 'TASK-012']
  TASK-006 的直接依赖者: ['TASK-012']
  TASK-007 的直接依赖者: ['TASK-008', 'TASK-013']
  TASK-008 的直接依赖者: ['TASK-009', 'TASK-014', 'TASK-015']
  TASK-009 的直接依赖者: ['TASK-037']
  TASK-010 的直接依赖者: ['TASK-016']
TASK-009: SC-23 / SC-14(a) 回归守卫 (CLI 全链路, baseline 即绿) + SC-2 ↔ SC-23 相容性断言 | deps: ['TASK-001', 'TASK-003', 'TASK-008'] | deliverables: ['aria/skills/state-scanner/tests/test_a1_entry_gate_cli.py', 'aria/skills/state-scanner/scripts/release_gate.py']
anc(TASK-038) ⊇ anc(TASK-040) ∪ {040}: True ; 依赖 TASK-040 的任务: ['TASK-038']
估时: metadata 97-158 ; TASK-040 3-5 ; agent tech-lead ∈ roster True ; complexity M
gitlink 实存口径 = index 条目 mode 160000 + 工作树目录 + `git submodule status` 可解析 (非 os.path.exists 单独判):
  git ls-files -s aria -> 160000 d69091dfdeb0c6cd83b03da2492812d33cec3712 0	aria
  isdir(aria) -> True
  git submodule status aria -> d69091dfdeb0c6cd83b03da2492812d33cec3712 aria (v1.67.2)
aria remotes (TASK-040 命令行点名 origin / github):
  github	git@github.com:10CG/aria-plugin.git (fetch)
  github	git@github.com:10CG/aria-plugin.git (push)
  origin	ssh://forgejo@forgejo.10cg.pub/10CG/aria-plugin.git (fetch)
  origin	ssh://forgejo@forgejo.10cg.pub/10CG/aria-plugin.git (push)
aria tag 形态 (TASK-040 写 `git -C aria tag v<vNEXT>`): ['v1.67.2', 'v1.67.1', 'v1.67.0']
AB_TEST_OPERATIONS.md:222 -> #### 场景 1 运行前置: 协调 ref 推送隔离 (`ARIA_COORDINATION_NO_PUSH=1`)
```

### [4b] 发布链向下可达, 三份对称 — 脚本 `s3b_release_reach.py`

```python
#!/usr/bin/env python3
"""R4/A4 [4b] 发布链向下可达, 三份对称: 每份「写 aria/ 的任务」(deliverables 路径以 aria/ 起首且注释不含「只读」) ⊆ anc(发布任务).
发布任务 = 各份 title 含「merge → master」或「发布同步」/ gitlink 的任务 (程序化按 title/deliverables 选, 并打印选到的是谁)."""
import yaml,re
ROOT="/home/dev/Aria/openspec/changes/"
SPECS=["linked-issue-field-availability","sibling-spec-probe","a1-entry-claim-duplicate-work-guard"]
def load(s):
    raw=open(ROOT+s+"/detailed-tasks.yaml",encoding="utf-8").read(); d=yaml.safe_load(raw); T={t["id"]:t for t in d["tasks"]}
    deliv={}; cur=None; ind=False
    for line in raw.splitlines():
        m=re.match(r"^  - id: (TASK-\d{3})",line)
        if m: cur=m.group(1); ind=False; deliv[cur]=[]; continue
        if cur and re.match(r"^    deliverables:",line): ind=True; continue
        if cur and ind:
            if re.match(r"^    \w",line): ind=False; continue
            m=re.match(r"^      - (\S+)\s*(#.*)?$",line)
            if m: deliv[cur].append((m.group(1),m.group(2) or ""))
    deps={i:list(t.get("dependencies") or []) for i,t in T.items()}
    def anc(i,seen=None):
        seen=set() if seen is None else seen
        for j in deps[i]:
            if j not in seen: seen.add(j); anc(j,seen)
        return seen
    return T,deliv,deps,anc
for s in SPECS:
    T,deliv,deps,anc=load(s)
    writers=sorted(i for i,items in deliv.items() if any(p.startswith("aria/") and "只读" not in c for p,c in items))
    # 发布任务: deliverable 逐字 == 'aria' (gitlink) 或 title 含 merge → master
    rel=sorted(i for i,items in deliv.items() if any(p=="aria" for p,c in items) or "merge → master" in T[i]["title"])
    print(f"===== {s}: aria/ 写任务 {len(writers)} 个; 发布任务候选 {rel} ({[T[i]['title'][:40] for i in rel]})")
    for r in rel:
        miss=[w for w in writers if w!=r and w not in anc(r)]
        print(f"  anc({r}) 覆盖 aria/ 写任务: {'全部' if not miss else 'MISSING '+str(miss)}; 直接依赖者: {sorted(i for i in T if r in deps[i])}")
    # 版本 5 文件任务 (plugin.json) 是否在发布任务祖先集
    ver=[i for i,items in deliv.items() if any("plugin.json" in p for p,c in items)]
    for r in rel:
        print(f"  版本 SOT 任务 {ver} ⊆ anc({r}) ∪ {{{r}}}: {all(v in anc(r) or v==r for v in ver)}")
```

```
===== linked-issue-field-availability: aria/ 写任务 12 个; 发布任务候选 ['TASK-022', 'TASK-023'] (['aria 子模块本地 merge → master + 双推 + 逐 remot', 'standards 子模块本地 merge → master + 双推 + ls'])
  anc(TASK-022) 覆盖 aria/ 写任务: 全部; 直接依赖者: ['TASK-024', 'TASK-025']
  anc(TASK-023) 覆盖 aria/ 写任务: MISSING ['TASK-021']; 直接依赖者: ['TASK-025']
  版本 SOT 任务 ['TASK-021'] ⊆ anc(TASK-022) ∪ {TASK-022}: True
  版本 SOT 任务 ['TASK-021'] ⊆ anc(TASK-023) ∪ {TASK-023}: False
===== sibling-spec-probe: aria/ 写任务 16 个; 发布任务候选 ['TASK-018'] (['发布同步面 (aria 子模块): CHANGELOG + plugin.jso'])
  anc(TASK-018) 覆盖 aria/ 写任务: 全部; 直接依赖者: []
  版本 SOT 任务 ['TASK-018'] ⊆ anc(TASK-018) ∪ {TASK-018}: True
===== a1-entry-claim-duplicate-work-guard: aria/ 写任务 28 个; 发布任务候选 ['TASK-038', 'TASK-040'] (['主仓发版同步面: gitlink bump + 主仓 VERSION + CLA', 'aria 子模块本地 merge → master + 双推 + 逐 remot'])
  anc(TASK-038) 覆盖 aria/ 写任务: 全部; 直接依赖者: []
  anc(TASK-040) 覆盖 aria/ 写任务: 全部; 直接依赖者: ['TASK-038']
  版本 SOT 任务 ['TASK-037'] ⊆ anc(TASK-038) ∪ {TASK-038}: True
  版本 SOT 任务 ['TASK-037'] ⊆ anc(TASK-040) ∪ {TASK-040}: True
```

> 判读: 三份的 aria 发布任务 (字段 TASK-022 / 探针 TASK-018 / 母 TASK-040 与 038) 祖先集各覆盖本份**全部** `aria/` 写任务 (12 / 16 / 28 个; s3 的「30 个」含 TASK-003 只读条目, 口径不同同结论); 版本 SOT 任务 (写 plugin.json 的 TASK-021 / 018 / 037) 都在发布任务祖先集。字段 TASK-023 那行 `MISSING ['TASK-021']` 是本脚本按 title 把 standards 发布任务也选成候选所致 — TASK-023 只 merge standards, 不要求 aria 写任务在其祖先集, 非缺陷。

### [5] 检查 4/5/8 — 覆盖表 token / deliverables 实存性 / roster (`chk3_cov_deliv.py` 逐字复用) + flag 字面 / summary / check 名实存 / TASK-024 (`s4_flags_summary.py` 逐字复用)

```

===== linked-issue-field-availability
  覆盖表行=10 (SC,TASK) 对=28
  verification 无 token: 0 []
  整块 (title/verification/deliverables 注释/notes) 无 token: 0 []
  yaml verification 出现但表无行: ['SC-19']
  deliverables 行=36
  agent 字段分布={k:len(v) for k,v in ag.items()}
    roster type: list ['qa-engineer', 'backend-architect', 'knowledge-manager', 'tech-lead']

===== sibling-spec-probe
  覆盖表行=21 (SC,TASK) 对=46
  verification 无 token: 0 []
  整块 (title/verification/deliverables 注释/notes) 无 token: 0 []
  yaml verification 出现但表无行: []
  deliverables 行=41
    ⚠ 未标新建但不存在: TASK-001 aria/skills/state-scanner/lib/linked_issue_field.py | # 由姊妹 Spec 交付; 本 Spec 只核验, 零改动 (今天不存在)
    ⚠ 未标新建但不存在: TASK-005 aria/skills/audit-engine/tests/test_sibling_spec_probe.py | # 夹具以字符串字面量内嵌 (逐字原文)
    ⚠ 未标新建但不存在: TASK-006 aria/skills/audit-engine/tests/test_sibling_spec_probe.py | # 三臂对照 + 第四臂合成夹具
    ⚠ 未标新建但不存在: TASK-007 aria/skills/audit-engine/tests/test_sibling_spec_probe.py | # runner 体例仿 phase-d-closer/tests/test_fetch_gate.py:22 `_runner(seq)`: run(args
    ⚠ 未标新建但不存在: TASK-008 aria/skills/audit-engine/tests/test_sibling_spec_probe.py | # subprocess.run([sys.executable, <script>, ...]) 体例仿 state-scanner/tests/test_c
    ⚠ 未标新建但不存在: TASK-009 aria/skills/audit-engine/tests/test_sibling_spec_probe.py | # 读同 skill 的 SKILL.md 与 references/execution-modes.md (Path(__file__).parents[1]
    ⚠ 未标新建但不存在: TASK-011 aria/skills/audit-engine/scripts/sibling_spec_probe.py | # 纯分类函数 + 键构造 + 求交
    ⚠ 未标新建但不存在: TASK-012 aria/skills/audit-engine/scripts/sibling_spec_probe.py | # remote/default-branch/fetch 段
    ⚠ 未标新建但不存在: TASK-013 aria/skills/audit-engine/scripts/sibling_spec_probe.py | # corpus 段
    ⚠ 未标新建但不存在: TASK-014 aria/skills/audit-engine/scripts/sibling_spec_probe.py | 
    ⚠ 未标新建但不存在: TASK-014 aria/skills/audit-engine/tests/test_sibling_spec_probe.py | 
    ⚠ 未标新建但不存在: TASK-017 aria-plugin-benchmarks/ab-suite/audit-engine.json | # 若三臂语义分档显示断言措辞过宽 ⇒ 拆条不删 (手册 :142-159), 并 version.yaml 再升
  agent 字段分布={k:len(v) for k,v in ag.items()}
    roster type: list ['tech-lead', 'qa-engineer', 'backend-architect', 'knowledge-manager']

===== a1-entry-claim-duplicate-work-guard
  覆盖表行=33 (SC,TASK) 对=55
  verification 无 token: 0 []
  整块 (title/verification/deliverables 注释/notes) 无 token: 0 []
  yaml verification 出现但表无行: []
  deliverables 行=86
    ⚠ 标新建但已存在: TASK-001 docs/handoff/
    ⚠ 未标新建但不存在: TASK-006 aria/skills/state-scanner/tests/test_heartbeat_by_track.py | # 同文件加 TestRenameTwoStep 类 (改名是 claim_lifecycle 语义, 与 heartbeat 同宿主); 串行于 TASK-0
    ⚠ 未标新建但不存在: TASK-008 aria/skills/state-scanner/tests/test_a1_entry_gate_cli.py | # 同文件加四个测试类; 串行于 TASK-007 之后
    ⚠ 未标新建但不存在: TASK-009 aria/skills/state-scanner/tests/test_a1_entry_gate_cli.py | # 同文件加 TestA1CarryIdRoundTrip; 串行于 TASK-008 之后
    占位路径 TASK-031 aria-plugin-benchmarks/ab-results/<YYYY-MM-DD>-<vNEXT>-a1-entry-rule6/phase-a-planner/
    占位路径 TASK-032 aria-plugin-benchmarks/ab-results/<YYYY-MM-DD>-<vNEXT>-a1-entry-rule6/spec-drafter/
    占位路径 TASK-033 aria-plugin-benchmarks/ab-results/<YYYY-MM-DD>-<vNEXT>-a1-entry-rule6/state-scanner/
    占位路径 TASK-034 aria-plugin-benchmarks/ab-results/<YYYY-MM-DD>-<vNEXT>-a1-entry-rule6/phase-b-developer/
    占位路径 TASK-034 aria-plugin-benchmarks/ab-results/<YYYY-MM-DD>-<vNEXT>-a1-entry-rule6/branch-manager/
    占位路径 TASK-034 aria-plugin-benchmarks/ab-results/<YYYY-MM-DD>-<vNEXT>-a1-entry-rule6/phase-d-closer/
    占位路径 TASK-035 aria-plugin-benchmarks/ab-results/<YYYY-MM-DD>-<vNEXT>-a1-entry-rule6/targeted/
  agent 字段分布={k:len(v) for k,v in ag.items()}
    roster type: list ['backend-architect', 'qa-engineer', 'knowledge-manager', 'tech-lead']
```

> 与 R3 [5] 逐行相同 (deliverables 行 36 / 41 / 86; 「未标新建但不存在」12+3 处仍全是同 Spec 上游任务新建的同一文件; 占位路径 7 处为 `<vNEXT>` 形态)。

```
  TASK-001: --no-push=Y  ARIA_COORDINATION_NO_PUSH=N
  TASK-031: --no-push=N  ARIA_COORDINATION_NO_PUSH=Y
  TASK-032: --no-push=N  ARIA_COORDINATION_NO_PUSH=Y
  TASK-033: --no-push=N  ARIA_COORDINATION_NO_PUSH=Y
  TASK-034: --no-push=N  ARIA_COORDINATION_NO_PUSH=Y
  TASK-035: --no-push=N  ARIA_COORDINATION_NO_PUSH=Y
  TASK-034 verification[0] 逐字: 运行前置 (Rule #7 射程 + R1 C5): 会话以 `ARIA_COORDINATION_NO_PUSH=1 claude …` 启动 (AB_TEST_OPERATIONS.md:222-228), transcript 核验 `push_skipped: true` — R3/A4 199aa25c 补齐 (031–035 五处同句)
  tasks.md 映射行: `--no-push` / `ARIA_COORDINATION_NO_PUSH` (001, 031–035)
  TASK-018: --raw-track-id=Y  --phase A.1=Y  --mode advisory=Y  --linked-issue=Y  --repo-path=Y
  TASK-019: --status abandoned=Y  --sweep-stale=Y  --gc=Y
linked summary.by_complexity: {'S': 14, 'M': 10, 'L': 1, 'XL': 0} actual: {'M': 10, 'S': 14, 'L': 1} ; summary.estimated_hours: 50-86
  linked agent_allocation qa-engineer: n=11 match=True
  linked agent_allocation backend-architect: n=5 match=True
  linked agent_allocation knowledge-manager: n=6 match=True
  linked agent_allocation tech-lead: n=3 match=True
  linked agent_allocation new_agents: n=0 match=True
sibling complexity_summary: {'S': 4, 'M': 11, 'L': 3, 'XL': 0} actual: {'S': 4, 'M': 11, 'L': 3} ; total: 55-87
  sibling agent_allocation tech-lead: n=1 match=True
  sibling agent_allocation qa-engineer: n=9 match=True
  sibling agent_allocation backend-architect: n=5 match=True
  sibling agent_allocation knowledge-manager: n=3 match=True
  state-checks.yaml 含 name m6-version-badge-match: 1
  state-checks.yaml 含 name m6-claude-md-version: 1
  state-checks.yaml 含 name main-project-version-consistency: 1
  state-checks.yaml 含 name i18n-readme-translation-currency: 1
linked TASK-024 title: 主仓发版同步面 14 点 (与 086ee32 同口径): CLAUDE.md :139/:141 2 点 + VERSION:24 + README.md :8/:242 2 点 + i18n ×3 各 3 点 — 版本引用面
  deliverables: ['VERSION', 'README.md', 'CLAUDE.md', 'README.zh.md', 'README.ja.md', 'README.ko.md']
  verification[0][:60]: 14 个引用点 (与 086ee32 同口径: CLAUDE.md:139/:141 + VERSION + READM
  tasks.md :82 (5.5) 含 CLAUDE.md: True | 含 m6-claude-md-version: False
linked TASK-017 title: 可证伪定向 fixture ×1 (SC-7 双臂) — spec-drafter.json 新增 新 eval (id = ship 时 max(id)+1, 今日观测 3) (中文臂); 英文臂 = 更新后的 eval id 2
```

### [6] 残留 grep (六份, 主控点名十模式 + 附加; 逐字命中行, 截 170 列) — 脚本 `s5_residual_grep.sh`

```bash
#!/bin/bash
# R4/A4 [6] 残留 grep (逐字命中; 六份 + 主控点名的 10 个模式). 截列按字符 (python), 不切坏 UTF-8
cd /home/dev/Aria/openspec/changes
F="linked-issue-field-availability/tasks.md linked-issue-field-availability/detailed-tasks.yaml sibling-spec-probe/tasks.md sibling-spec-probe/detailed-tasks.yaml a1-entry-claim-duplicate-work-guard/tasks.md a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml"
trunc() { python3 -c 'import sys
for l in sys.stdin.buffer.read().decode("utf-8").splitlines(): print(l[:170]+(" …" if len(l)>170 else ""))'; }
for pat in '1\.68\.0' '1\.67\.3' 'README\.zh-CN\.md' 'est_hours:' 'parallelizable' '未自行加边' '13 项' '300s' '39 tasks' 'eval id 3'; do
  n=$(grep -c -E "$pat" $F | awk -F: '{s+=$2} END{print s}')
  echo "--- $pat : 总命中 $n"; grep -n -E "$pat" $F | trunc
done
echo "--- <vNEXT> 行数:"; grep -c '<vNEXT>' $F
echo "--- \b39\b (a1 两份):"; grep -n -E '\b39\b' a1-entry-claim-duplicate-work-guard/tasks.md a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml | trunc
echo "--- 「12 点」(三份 六文件):"; grep -n -E '12 点' $F | trunc
echo "--- 主控 R3 清账点名: '≥ 300s' / '≥300s':"; grep -n -E '≥ ?300' $F | trunc; echo "(上行空 = 零命中)"
```

```
--- 1\.68\.0 : 总命中 6
linked-issue-field-availability/tasks.md:7:> **ship target**: aria-plugin **`<vNEXT>`** (R1/C3 三份统一占位, 本文件**不写** v1.68.0 / v1.67.3 字面; proposal §Impact 自判 **MINOR**, ⚠️ 两 …
linked-issue-field-availability/tasks.md:177:| 3221f943 | A1 | major | closed (本 Spec 侧, 方案 C3) — 版本字面 v1.68.0 / v1.67.3 全部改 `<vNEXT>` 占位; TASK-021 notes 落三份统一句 (串行各占一号 / …
linked-issue-field-availability/tasks.md:178:| 970d3368 | A1 | minor | closed — TASK-008 SKIP 文案「版本 < v1.68.0」改 `<vNEXT>` + 「落地时以 plugin.json 实际号回填并在 PR 点名」 | yaml TASK-0 …
sibling-spec-probe/tasks.md:121:5. **版本号档位与号 (R1 C3 三份统一句)**: 本 Spec 新增运行时指令面 (audit-engine SKILL.md + execution-modes.md) + 新脚本, CLAUDE.md「新增 Skill / 架构重构 = MINOR+」与「文档更 …
a1-entry-claim-duplicate-work-guard/tasks.md:196:6. **版本号**: A.2 倾向 MINOR; 号 = `<vNEXT>` 落地时计算, 不预写 (R1 C3: 字段 Spec 与本 Spec 曾同写 v1.68.0 而串行 ship 三档必撞号)。档位 (MINOR/PATCH) 与 …
a1-entry-claim-duplicate-work-guard/tasks.md:249:| `3221f943` | A1 (major) | C3 版本档撞号 + ab-results 字面量 | **closed** (留痕, 不拍板) | yaml: TASK-031~035 五处 `ab-results/<YYYY-MM …
--- 1\.67\.3 : 总命中 3
linked-issue-field-availability/tasks.md:7:> **ship target**: aria-plugin **`<vNEXT>`** (R1/C3 三份统一占位, 本文件**不写** v1.68.0 / v1.67.3 字面; proposal §Impact 自判 **MINOR**, ⚠️ 两 …
linked-issue-field-availability/tasks.md:177:| 3221f943 | A1 | major | closed (本 Spec 侧, 方案 C3) — 版本字面 v1.68.0 / v1.67.3 全部改 `<vNEXT>` 占位; TASK-021 notes 落三份统一句 (串行各占一号 / …
sibling-spec-probe/tasks.md:121:5. **版本号档位与号 (R1 C3 三份统一句)**: 本 Spec 新增运行时指令面 (audit-engine SKILL.md + execution-modes.md) + 新脚本, CLAUDE.md「新增 Skill / 架构重构 = MINOR+」与「文档更 …
--- README\.zh-CN\.md : 总命中 3
a1-entry-claim-duplicate-work-guard/tasks.md:247:| `73809784` | A1 (critical) | C2 TASK-038 发布同步面 | **closed** | yaml TASK-038: 删 `.gitmodules` (不承载 gitlink) 与不存在的 `READM …
a1-entry-claim-duplicate-work-guard/tasks.md:248:| `518a7d7f` | A4 (major) | C2 `README.zh-CN.md` | **closed** | 同上 (与 A1 73809784 同一改动) |
a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml:982:    notes: "子模块 aria 的合并一律本地 merge + 双推 (CLAUDE.md 硬约束 1), 禁 Forgejo 服务端合并。R1 C2: 清单以字段 Spec TASK-024 列法 + 086 …
--- est_hours: : 总命中 2
linked-issue-field-availability/tasks.md:179:| df090b25 | A4 | major | closed — 25/25 `est_hours: int` → `estimated_hours: "a-b"` (S "1-2" / M "3-5" / L "6-8", DUAL_LAYER …
sibling-spec-probe/tasks.md:151:| df090b25 (A4) / C9 | A4 · major | **closed** — 18 处 `est_hours: <int>` → `estimated_hours: "a-b"` (S "1-2" / M "3-5" / L "6-8", DUAL_LAY …
--- parallelizable : 总命中 5
linked-issue-field-availability/tasks.md:171:| 9b64d749 | A2 | critical | closed — 同文件任务全部串行 (同文件): 组 1 六条链式 001→…→006, 008→009, 014→015, 016→017→018→019; `execution_orde …
linked-issue-field-availability/tasks.md:192:> 脚本 (`check_c1.py`, 在主仓根执行; exit 0 = PASS)。断言: (a) 任意两任务 deliverables 交集非空 ⇒ 后者依赖前者 (直接或传递); (b) 无环 / 无悬空; (c) 测试任务 (TG-1 或  …
linked-issue-field-availability/tasks.md:230:# (d) execution_order 任何并行标记 (parallelizable 列表 / {A, B} / A ‖ B) 内无同文件对
linked-issue-field-availability/tasks.md:234:    if isinstance(v.get("parallelizable"), list): groups.append(list(v["parallelizable"]))
linked-issue-field-availability/tasks.md:242:bad_word = [ln.strip() for ln in eo_txt.splitlines() if re.search(r"并行|parallelizable", ln) and "不同文件" not in ln and "同文件" no …
--- 未自行加边 : 总命中 0
--- 13 项 : 总命中 0
--- 300s : 总命中 0
--- 39 tasks : 总命中 0
--- eval id 3 : 总命中 0
--- <vNEXT> 行数:
linked-issue-field-availability/tasks.md:4
linked-issue-field-availability/detailed-tasks.yaml:5
sibling-spec-probe/tasks.md:3
sibling-spec-probe/detailed-tasks.yaml:5
a1-entry-claim-duplicate-work-guard/tasks.md:5
a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml:11
--- \b39\b (a1 两份):
a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml:134:        `grep -n no_push aria/skills/state-scanner/scripts/phase1_gate.py` 非空 (:35-39 docstring / :362 形参 / :5 …
--- 「12 点」(三份 六文件):
--- 主控 R3 清账点名: '≥ 300s' / '≥300s':
(上行空 = 零命中)
```

判读: 十模式里 `未自行加边` / `13 项` / `300s` / `39 tasks` / `eval id 3` 六份零命中; 其余命中逐行核: linked :7 / :177 / :178, sibling :121, a1 :196 / :249 = 「不写 / 不预写 v1.68.0 / v1.67.3」统一句或 R1 对账留痕; a1 :247 / :248 = 对账留痕, a1 yaml :982 = TASK-038 notes「原写的 `README.zh-CN.md` 不存在 … 已改」留痕 (R3 时在 :1001, 移块后行号变); linked :179 / sibling :151 = `est_hours:` 对账留痕; linked :171 / :192 / :230 / :234 / :242 = 贴出脚本 (d) 正文 (它要拒绝的字样)。两份 yaml 里 `1.68.0` / `1.67.3` / `est_hours:` / `parallelizable` 零命中。`\b39\b` a1 两份只剩 yaml :134 `:35-39` 行号 (无关)。`12 点` 六份零命中 (R3 A2 minor 闭合)。`≥ 300` 零命中 (R3-5 闭合)。

### [6b] 拒绝能力复核 (坏输入跑在 `r4a4/bad_*` 副本; 脚本只改路径常量) — 脚本 `s9_adv.py`

```python
#!/usr/bin/env python3
"""R4/A4 [6b] 拒绝能力复核 (坏输入跑在 scratch 副本; 脚本只改路径常量):
(a) a1 贴出脚本 × R3 同款三处回退 → 应 FAIL; 与 tasks.md 贴出的坏输入输出块比对
(b) a1 贴出脚本 × 只删 TASK-037 的 TASK-009 边 (R3 1a45ef41 的缺陷形状) → 看贴出脚本抓不抓 (结构盲区复核)
(c) sibling 贴出脚本 (R3 扩维后的 (e)) × R3 坏输入 v2 (同文件标并行) / v3 (有边却标并行) → 应双 FAIL
(d) sibling 贴出脚本 × tasks.md「拒绝能力」段自述的「清账前依赖图」还原配方 → 与该段声称的 (a)(d)(e) 结果比对"""
import re, shutil, subprocess, sys, pathlib, difflib, yaml
SP=pathlib.Path(__file__).parent; ARIA=pathlib.Path("/home/dev/Aria"); SRC=ARIA/"openspec/changes"
def run(py): 
    r=subprocess.run([sys.executable,str(py)],cwd=str(ARIA),capture_output=True,text=True); return r
def block(y,tid): return re.search(rf"(  - id: {tid}\n.*?)(?=\n  - id: TASK-|\Z)", y, re.S).group(1)
# ---- (a)(b) a1
a1py=(SP/"pasted_a1.py").read_text(encoding="utf-8"); assert 'ROOT = "/home/dev/Aria/openspec/changes/a1-entry-claim-duplicate-work-guard/"' in a1py
def a1_case(name, mutate):
    d=SP/f"bad_a1_{name}/openspec/changes/a1-entry-claim-duplicate-work-guard"; d.mkdir(parents=True,exist_ok=True)
    for f in ("tasks.md","proposal.md","detailed-tasks.yaml"): shutil.copy(SRC/"a1-entry-claim-duplicate-work-guard"/f, d/f)
    y=(d/"detailed-tasks.yaml").read_text(encoding="utf-8"); y2=mutate(y); assert y2!=y; (d/"detailed-tasks.yaml").write_text(y2,encoding="utf-8")
    py=a1py.replace('ROOT = "/home/dev/Aria/openspec/changes/a1-entry-claim-duplicate-work-guard/"', f'ROOT = "{d}/"'); p=SP/f"pasted_a1_bad_{name}.py"; p.write_text(py,encoding="utf-8")
    r=run(p); print(f"[a1 坏输入 {name}] exit={r.returncode}\n"+"\n".join("   "+l for l in r.stdout.splitlines() if not l.startswith("      ")))
    return r
def three_reverts(y):
    b=block(y,"TASK-016"); nb=re.sub(r"(dependencies: \[[^\]]*?), TASK-015\]", r"\1]", b, count=1); assert nb!=b; y=y.replace(b,nb)
    b=block(y,"TASK-025"); nb=re.sub(r"(dependencies: \[[^\]]*)\]", r"\1, TASK-017]", b, count=1); assert nb!=b; y=y.replace(b,nb)
    b=block(y,"TASK-004"); nb=b.replace("SC-3","SC-x",1); assert nb!=b; y=y.replace(b,nb)
    return y
r=a1_case("three", three_reverts)
md=(SRC/"a1-entry-claim-duplicate-work-guard/tasks.md").read_text(encoding="utf-8"); sec=md[md.index("### 机械核验"):]
outs=[b for l,b in re.findall(r"```(\w*)\n(.*?)\n```", sec, re.S) if l in ("","text")]; exp=outs[1].rstrip("\n")
got="\n".join(l for l in r.stdout.rstrip("\n").splitlines() if not l.startswith("      "))
print("   贴出坏输入块 与 亲跑 (剔除文件明细行) 逐字一致:", got==exp)
for l in difflib.unified_diff(exp.splitlines(), got.splitlines(), "pasted-bad", "actual-bad", lineterm="", n=0): print("     ",l)
def drop009(y):
    b=block(y,"TASK-037"); nb=b.replace("dependencies: [TASK-009, TASK-011","dependencies: [TASK-011",1); assert nb!=b; return y.replace(b,nb)
r=a1_case("drop009", drop009)
print("   ⇒ 贴出脚本对「发布链丢 TASK-009 边」:", "抓到 (FAIL)" if r.returncode else "抓不到 (PASS) — 结构盲区 (R3 1a45ef41 处方 (f) 未采), 观察项")
# ---- (c)(d) sibling
spy=(SP/"pasted_sibling.py").read_text(encoding="utf-8"); assert 'Y = ROOT / "openspec/changes/sibling-spec-probe/detailed-tasks.yaml"' in spy
def sib_case(name, ytext):
    d=SP/f"bad_sib_{name}/openspec/changes/sibling-spec-probe"; d.mkdir(parents=True,exist_ok=True)
    shutil.copy(SRC/"sibling-spec-probe/tasks.md", d/"tasks.md"); (d/"detailed-tasks.yaml").write_text(ytext,encoding="utf-8")
    py=spy.replace('Y = ROOT / "openspec/changes/sibling-spec-probe/detailed-tasks.yaml"', f'Y = pathlib.Path("{d}/detailed-tasks.yaml")'); p=SP/f"pasted_sibling_bad_{name}.py"; p.write_text(py,encoding="utf-8")
    r=run(p); lines=[l for l in r.stdout.splitlines() if not l.startswith("    TASK-")]
    print(f"\n[sibling 坏输入 {name}] exit={r.returncode}\n"+"\n".join("   "+l for l in lines if l.startswith(("(e)","(a)","(d)","(c)","RESULT","parent","parse"))))
    if r.stderr.strip(): print("   STDERR:", r.stderr.strip()[:400])
    return r
cur=(SRC/"sibling-spec-probe/detailed-tasks.yaml").read_text(encoding="utf-8")
v2=cur.replace('  - "[串行 (同文件 tests/test_sibling_spec_probe.py), RED] TASK-005', '  - "[并行, RED] TASK-005',1); assert v2!=cur
old0='  - "TASK-001 (硬前置断言, 阻塞门) ‖ TASK-002 (基线三态, 只读观测) 可并行 (不同文件); TASK-003 (AB 套件文件, B.1 前置) ← 002 (主控 R1 追记: 002 断言「无 audit-engine.json」须先于 003 建文件)"'
assert old0 in cur
v3=cur.replace(old0,'  - "TASK-001 (硬前置断言, 阻塞门); TASK-002 (基线三态, 只读观测) ‖ TASK-003 (AB 套件文件, B.1 前置) 可并行 (不同文件)"',1)
sib_case("v2", v2); sib_case("v3", v3)
# (d) 清账前依赖图配方 (tasks.md 拒绝能力段逐字: TASK-005~009 deps=[TASK-004], TASK-012=[010,007], TASK-014=[011,012,013], TASK-015=[009], TASK-016=[009,015], execution_order 两处「并行」行)
y=cur
def setdeps(y,tid,new):
    b=block(y,tid); nb=re.sub(r"dependencies: \[[^\]]*\]", f"dependencies: [{', '.join(new)}]", b, count=1); assert nb!=b or f"[{', '.join(new)}]" in b; return y.replace(b,nb)
for t in ("TASK-005","TASK-006","TASK-007","TASK-008","TASK-009"): y=setdeps(y,t,["TASK-004"])
y=setdeps(y,"TASK-012",["TASK-010","TASK-007"]); y=setdeps(y,"TASK-014",["TASK-011","TASK-012","TASK-013"]); y=setdeps(y,"TASK-015",["TASK-009"]); y=setdeps(y,"TASK-016",["TASK-009","TASK-015"])
eo=yaml.safe_load(cur)["execution_order"]
y=y.replace('  - "'+eo[2]+'"', '  - "[并行, RED] TASK-005 · TASK-006 · TASK-007 · TASK-008 · TASK-009  ← 004"',1)
y=y.replace('  - "'+eo[4]+'"', '  - "[并行] TASK-011 (谓词)  ← 010, 005, 006 · TASK-012 (远端)  ← 010, 007"',1)
assert y.count("[并行")==2, y.count("[并行")
r=sib_case("oldgraph", y)
fails=[l for l in r.stdout.splitlines() if l.startswith("RESULT")]
print("   段落声称: (a) 13 对同文件缺边; (d) TASK-001 缺于 005~009、TASK-003 缺于 015/016; (e) 「[并行, RED]」行 10 对同文件 + 「[并行] TASK-011 · TASK-012」1 对")
a_miss=r.stdout.count("MISSING"); print(f"   亲跑: (a) MISSING 行数={a_miss}; (e) 行:"); [print("      "+l[:230]) for l in r.stdout.splitlines() if l.startswith("(e)")]
```

输出 (行截 300 字符; 母脚本文件明细行与探针 `    TASK-xxx -> TASK-yyy OK` 行已在脚本内剔除):

```
[a1 坏输入 three] exit=1
   [a] 同文件写入对 38 对 (共写文件 20 个) — 全部有边: False
   [b] 无环: False; 悬空: []
   [c] Group 6 = ['TASK-025', 'TASK-026', 'TASK-027', 'TASK-028', 'TASK-029', 'TASK-030']; 无一 (传递) 依赖 Group 5: False; Group 5 各含对应 RED 直接边: True; Group 6 祖先集 ⊆ {TASK-001,TASK-003} ∪ Group 6: False
   [c'] 不经传递到达 TASK-001 的任务 (豁免 ['TASK-001', 'TASK-002', 'TASK-003', 'TASK-039']): []; 不到达 TASK-003: []
   [d] 覆盖表 (SC, TASK) 对 55; verification 无 token 的对: []
   [e] proposal SC 集合 1..34 共 34; 排除 [1, 4, 13, 16, 17, 18, 19, 20, 27, 30, 31]; 现行 23 条无命中: []
   [+] total_tasks=40 (metadata 40); parent 唯一=True; parent ⊆ tasks.md 编号=True; 编号数=40
   RESULT: FAIL
       (a) 同文件无边: aria/skills/state-scanner/scripts/phase1_gate.py: TASK-015 <-> TASK-016
       (b) 环: TASK-017 -> TASK-022 -> TASK-027 -> TASK-026 -> TASK-025 -> TASK-017
       (c) Group 6 任务 TASK-025 (传递) 依赖 Group 5: ['TASK-022', 'TASK-017']
       (c) Group 6 任务 TASK-026 (传递) 依赖 Group 5: ['TASK-022', 'TASK-017']
       (c) Group 6 任务 TASK-027 (传递) 依赖 Group 5: ['TASK-022', 'TASK-017']
       (c) Group 6 任务 TASK-028 (传递) 依赖 Group 5: ['TASK-022', 'TASK-017']
       (c) Group 6 任务 TASK-029 (传递) 依赖 Group 5: ['TASK-022', 'TASK-017']
       (c) Group 6 任务 TASK-030 (传递) 依赖 Group 5: ['TASK-017', 'TASK-022']
   贴出坏输入块 与 亲跑 (剔除文件明细行) 逐字一致: False
      --- pasted-bad
      +++ actual-bad
      @@ -1 +1 @@
      -[a] 同文件写入对 40 对 (共写文件 19 个) — 全部有边: False
      +[a] 同文件写入对 38 对 (共写文件 20 个) — 全部有边: False
      @@ -3,2 +3,5 @@
      -[c] Group 6 = [...]; 无一 (传递) 依赖 Group 5: False; Group 5 各含对应 RED 直接边: True; Group 6 祖先集 ⊆ {TASK-001,TASK-003} ∪ Group 6: False
      -[d] 覆盖表 (SC, TASK) 对 51; verification 无 token 的对: [('SC-3', 'TASK-004')]
      +[c] Group 6 = ['TASK-025', 'TASK-026', 'TASK-027', 'TASK-028', 'TASK-029', 'TASK-030']; 无一 (传递) 依赖 Group 5: False; Group 5 各含对应 RED 直接边: True; Group 6 祖先集 ⊆ {TASK-001,TASK-003} ∪ Group 6: False
      +[c'] 不经传递到达 TASK-001 的任务 (豁免 ['TASK-001', 'TASK-002', 'TASK-003', 'TASK-039']): []; 不到达 TASK-003: []
      +[d] 覆盖表 (SC, TASK) 对 55; verification 无 token 的对: []
      +[e] proposal SC 集合 1..34 共 34; 排除 [1, 4, 13, 16, 17, 18, 19, 20, 27, 30, 31]; 现行 23 条无命中: []
      +[+] total_tasks=40 (metadata 40); parent 唯一=True; parent ⊆ tasks.md 编号=True; 编号数=40
      @@ -8,2 +11,6 @@
      -    (c) Group 6 任务 TASK-025 (传递) 依赖 Group 5: ['TASK-017', 'TASK-022']   (026~030 同, 略)
      -    (d) 覆盖表对 ('SC-3', 'TASK-004') 在 verification 无该 token
      +    (c) Group 6 任务 TASK-025 (传递) 依赖 Group 5: ['TASK-022', 'TASK-017']
      +    (c) Group 6 任务 TASK-026 (传递) 依赖 Group 5: ['TASK-022', 'TASK-017']
      +    (c) Group 6 任务 TASK-027 (传递) 依赖 Group 5: ['TASK-022', 'TASK-017']
      +    (c) Group 6 任务 TASK-028 (传递) 依赖 Group 5: ['TASK-022', 'TASK-017']
      +    (c) Group 6 任务 TASK-029 (传递) 依赖 Group 5: ['TASK-022', 'TASK-017']
      +    (c) Group 6 任务 TASK-030 (传递) 依赖 Group 5: ['TASK-017', 'TASK-022']
[a1 坏输入 drop009] exit=0
   [a] 同文件写入对 38 对 (共写文件 20 个) — 全部有边: True
   [b] 无环: True; 悬空: []
   [c] Group 6 = ['TASK-025', 'TASK-026', 'TASK-027', 'TASK-028', 'TASK-029', 'TASK-030']; 无一 (传递) 依赖 Group 5: True; Group 5 各含对应 RED 直接边: True; Group 6 祖先集 ⊆ {TASK-001,TASK-003} ∪ Group 6: True
   [c'] 不经传递到达 TASK-001 的任务 (豁免 ['TASK-001', 'TASK-002', 'TASK-003', 'TASK-039']): []; 不到达 TASK-003: []
   [d] 覆盖表 (SC, TASK) 对 55; verification 无 token 的对: []
   [e] proposal SC 集合 1..34 共 34; 排除 [1, 4, 13, 16, 17, 18, 19, 20, 27, 30, 31]; 现行 23 条无命中: []
   [+] total_tasks=40 (metadata 40); parent 唯一=True; parent ⊆ tasks.md 编号=True; 编号数=40
   RESULT: PASS
   ⇒ 贴出脚本对「发布链丢 TASK-009 边」: 抓不到 (PASS) — 结构盲区 (R3 1a45ef41 处方 (f) 未采), 观察项

[sibling 坏输入 v2] exit=1
   (a) same-file pairs = 34; all with edge = True
   (c) RED=['TASK-004', 'TASK-005', 'TASK-006', 'TASK-007', 'TASK-008', 'TASK-009']; RED depending on GREEN = none
   (d) TASK-001 direct in deps of ['TASK-004', 'TASK-005', 'TASK-006', 'TASK-007', 'TASK-008', 'TASK-009']: OK
   (d) TASK-003 direct in deps of ['TASK-015', 'TASK-016', 'TASK-017']: OK
   (e) TASK-003 ← ['TASK-002']: OK
   (e) parallel claim ['TASK-001', 'TASK-002']: dep-contradiction = none; same-file pairs = none
   (e) TASK-004 ← ['TASK-001', 'TASK-002', 'TASK-003']: OK
   (e) TASK-005 ← ['TASK-001', 'TASK-004']: OK
   (e) TASK-006 ← ['TASK-001', 'TASK-005']: OK
   (e) TASK-007 ← ['TASK-001', 'TASK-006']: OK
   (e) TASK-008 ← ['TASK-001', 'TASK-007']: OK
   (e) TASK-009 ← ['TASK-001', 'TASK-008']: OK
   (e) parallel claim ['TASK-005', 'TASK-001', 'TASK-004', 'TASK-006', 'TASK-001', 'TASK-005', 'TASK-007', 'TASK-001', 'TASK-006', 'TASK-008', 'TASK-001', 'TASK-007', 'TASK-009', 'TASK-001', 'TASK-008']: dep-contradiction = [('TASK-005', 'TASK-001'), ('TASK-005', 'TASK-004'), ('TASK-005', 'TASK-006' …[截 3090 字符]
   (e) TASK-010 ← ['TASK-004', 'TASK-008']: OK
   (e) TASK-011 ← ['TASK-010', 'TASK-005', 'TASK-006']: OK
   (e) TASK-012 ← ['TASK-011', 'TASK-010', 'TASK-007']: OK
   (e) TASK-013 ← ['TASK-012', 'TASK-007']: OK
   (e) TASK-014 ← ['TASK-009', 'TASK-011', 'TASK-012', 'TASK-013']: OK
   (e) TASK-015 ← ['TASK-003', 'TASK-009']: OK
   (e) TASK-016 ← ['TASK-003', 'TASK-009', 'TASK-015']: OK
   (e) TASK-017 ← ['TASK-003', 'TASK-014', 'TASK-015', 'TASK-016']: OK
   (e) TASK-018 ← ['TASK-017']: OK
   parse_detailed_tasks: parse_ok=True n=18 reason='18 task(s) parsed'; statuses=['pending']
   parent 1:1: yaml parents == tasks.md checkboxes -> True (18 vs 18); dup ids=[]; total_tasks meta=18
   RESULT: FAIL (e) parallel claim contradicts deps [('TASK-005', 'TASK-001'), ('TASK-005', 'TASK-004'), ('TASK-005', 'TASK-006'), ('TASK-005', 'TASK-001'), ('TASK-005', 'TASK-001'), ('TASK-005', 'TASK-006'), ('TASK-005', 'TASK-001'), ('TASK-005', 'TASK-001'), ('TASK-001', 'TASK-004'), ('TASK-001',  …[截 2904 字符]

[sibling 坏输入 v3] exit=1
   (a) same-file pairs = 34; all with edge = True
   (c) RED=['TASK-004', 'TASK-005', 'TASK-006', 'TASK-007', 'TASK-008', 'TASK-009']; RED depending on GREEN = none
   (d) TASK-001 direct in deps of ['TASK-004', 'TASK-005', 'TASK-006', 'TASK-007', 'TASK-008', 'TASK-009']: OK
   (d) TASK-003 direct in deps of ['TASK-015', 'TASK-016', 'TASK-017']: OK
   (e) parallel claim ['TASK-001', 'TASK-002', 'TASK-003']: dep-contradiction = [('TASK-002', 'TASK-003')]; same-file pairs = none
   (e) TASK-004 ← ['TASK-001', 'TASK-002', 'TASK-003']: OK
   (e) TASK-005 ← ['TASK-001', 'TASK-004']: OK
   (e) TASK-006 ← ['TASK-001', 'TASK-005']: OK
   (e) TASK-007 ← ['TASK-001', 'TASK-006']: OK
   (e) TASK-008 ← ['TASK-001', 'TASK-007']: OK
   (e) TASK-009 ← ['TASK-001', 'TASK-008']: OK
   (e) TASK-010 ← ['TASK-004', 'TASK-008']: OK
   (e) TASK-011 ← ['TASK-010', 'TASK-005', 'TASK-006']: OK
   (e) TASK-012 ← ['TASK-011', 'TASK-010', 'TASK-007']: OK
   (e) TASK-013 ← ['TASK-012', 'TASK-007']: OK
   (e) TASK-014 ← ['TASK-009', 'TASK-011', 'TASK-012', 'TASK-013']: OK
   (e) TASK-015 ← ['TASK-003', 'TASK-009']: OK
   (e) TASK-016 ← ['TASK-003', 'TASK-009', 'TASK-015']: OK
   (e) TASK-017 ← ['TASK-003', 'TASK-014', 'TASK-015', 'TASK-016']: OK
   (e) TASK-018 ← ['TASK-017']: OK
   parse_detailed_tasks: parse_ok=True n=18 reason='18 task(s) parsed'; statuses=['pending']
   parent 1:1: yaml parents == tasks.md checkboxes -> True (18 vs 18); dup ids=[]; total_tasks meta=18
   RESULT: FAIL (e) parallel claim contradicts deps [('TASK-002', 'TASK-003')]

[sibling 坏输入 oldgraph] exit=1
   (a) same-file pairs = 34; all with edge = False
   (c) RED=['TASK-004', 'TASK-005', 'TASK-006', 'TASK-007', 'TASK-008', 'TASK-009']; RED depending on GREEN = none
   (d) TASK-001 direct in deps of ['TASK-004', 'TASK-005', 'TASK-006', 'TASK-007', 'TASK-008', 'TASK-009']: MISSING ['TASK-005', 'TASK-006', 'TASK-007', 'TASK-008', 'TASK-009']
   (d) TASK-003 direct in deps of ['TASK-015', 'TASK-016', 'TASK-017']: MISSING ['TASK-015', 'TASK-016']
   (e) TASK-003 ← ['TASK-002']: OK
   (e) parallel claim ['TASK-001', 'TASK-002']: dep-contradiction = none; same-file pairs = none
   (e) TASK-004 ← ['TASK-001', 'TASK-002', 'TASK-003']: OK
   (e) TASK-009 ← ['TASK-004']: OK
   (e) parallel claim ['TASK-005', 'TASK-006', 'TASK-007', 'TASK-008', 'TASK-009', 'TASK-004']: dep-contradiction = [('TASK-005', 'TASK-004'), ('TASK-006', 'TASK-004'), ('TASK-007', 'TASK-004'), ('TASK-008', 'TASK-004'), ('TASK-009', 'TASK-004')]; same-file pairs = [('TASK-005', 'TASK-006'), ('TASK- …[截 356 字符]
   (e) TASK-010 ← ['TASK-004', 'TASK-008']: OK
   (e) TASK-011 ← ['TASK-010', 'TASK-005', 'TASK-006', 'TASK-012', 'TASK-010', 'TASK-007']: NOT IN deps ['TASK-012', 'TASK-007']
   (e) parallel claim ['TASK-011', 'TASK-010', 'TASK-005', 'TASK-006', 'TASK-012', 'TASK-010', 'TASK-007']: dep-contradiction = [('TASK-011', 'TASK-010'), ('TASK-011', 'TASK-005'), ('TASK-011', 'TASK-006'), ('TASK-011', 'TASK-010'), ('TASK-010', 'TASK-012'), ('TASK-012', 'TASK-010'), ('TASK-012', 'T …[截 264 字符]
   (e) TASK-013 ← ['TASK-012', 'TASK-007']: OK
   (e) TASK-014 ← ['TASK-009', 'TASK-011', 'TASK-012', 'TASK-013']: NOT IN deps ['TASK-009']
   (e) TASK-015 ← ['TASK-003', 'TASK-009']: NOT IN deps ['TASK-003']
   (e) TASK-016 ← ['TASK-003', 'TASK-009', 'TASK-015']: NOT IN deps ['TASK-003']
   (e) TASK-017 ← ['TASK-003', 'TASK-014', 'TASK-015', 'TASK-016']: OK
   (e) TASK-018 ← ['TASK-017']: OK
   parse_detailed_tasks: parse_ok=True n=18 reason='18 task(s) parsed'; statuses=['pending']
   parent 1:1: yaml parents == tasks.md checkboxes -> True (18 vs 18); dup ids=[]; total_tasks meta=18
   RESULT: FAIL (a) TASK-006 shares ['aria/skills/audit-engine/tests/test_sibling_spec_probe.py'] with TASK-005 but does not depend on it; (a) TASK-007 shares ['aria/skills/audit-engine/tests/test_sibling_spec_probe.py'] with TASK-005 but does not depend on it; (a) TASK-008 shares ['aria/skills/audi …[截 2691 字符]
   段落声称: (a) 13 对同文件缺边; (d) TASK-001 缺于 005~009、TASK-003 缺于 015/016; (e) 「[并行, RED]」行 10 对同文件 + 「[并行] TASK-011 · TASK-012」1 对
   亲跑: (a) MISSING 行数=15; (e) 行:
      (e) TASK-003 ← ['TASK-002']: OK
      (e) parallel claim ['TASK-001', 'TASK-002']: dep-contradiction = none; same-file pairs = none
      (e) TASK-004 ← ['TASK-001', 'TASK-002', 'TASK-003']: OK
      (e) TASK-009 ← ['TASK-004']: OK
      (e) parallel claim ['TASK-005', 'TASK-006', 'TASK-007', 'TASK-008', 'TASK-009', 'TASK-004']: dep-contradiction = [('TASK-005', 'TASK-004'), ('TASK-006', 'TASK-004'), ('TASK-007', 'TASK-004'), ('TASK-008', 'TASK-004'), ('TASK-009',
      (e) TASK-010 ← ['TASK-004', 'TASK-008']: OK
      (e) TASK-011 ← ['TASK-010', 'TASK-005', 'TASK-006', 'TASK-012', 'TASK-010', 'TASK-007']: NOT IN deps ['TASK-012', 'TASK-007']
      (e) parallel claim ['TASK-011', 'TASK-010', 'TASK-005', 'TASK-006', 'TASK-012', 'TASK-010', 'TASK-007']: dep-contradiction = [('TASK-011', 'TASK-010'), ('TASK-011', 'TASK-005'), ('TASK-011', 'TASK-006'), ('TASK-011', 'TASK-010'), 
      (e) TASK-013 ← ['TASK-012', 'TASK-007']: OK
      (e) TASK-014 ← ['TASK-009', 'TASK-011', 'TASK-012', 'TASK-013']: NOT IN deps ['TASK-009']
      (e) TASK-015 ← ['TASK-003', 'TASK-009']: NOT IN deps ['TASK-003']
      (e) TASK-016 ← ['TASK-003', 'TASK-009', 'TASK-015']: NOT IN deps ['TASK-003']
      (e) TASK-017 ← ['TASK-003', 'TASK-014', 'TASK-015', 'TASK-016']: OK
      (e) TASK-018 ← ['TASK-017']: OK
```

判读: (a) 母脚本三处回退 exit 1, (a) / (b)+(c) / (d)…— 注意 **(d) 这次没红**: `[d] … 无 token 的对: []` — 因为 R3 adv.py 的 `b.replace("SC-3","SC-x",1)` 只抹 TASK-004 **title** 里的第一个 `SC-3`, 而 (d) 查的是 verification; R3 的 bad_a1 副本里 title 与 verification 各有一处 SC-x (本席 [0b] 重建时发现 2 处), 说明 R3 那次亲跑用的坏输入与本次不同 — 本次 (d) 未红是坏输入构造差异, 不是脚本退化 (verification 里 `SC-3 夹具:` 仍在, 脚本 (d) 对 verification 的 token 检查 [2] 三份 0 缺)。贴出坏输入块与亲跑不一致的差异全是 R1 时代数字 (观察 2)。(b) 丢 TASK-009 边 ⇒ PASS (观察 1)。(c) 探针新 (e): v2 `FAIL (e) parallel claim contradicts deps …` (exit 1), **v3 `FAIL (e) parallel claim contradicts deps [('TASK-002', 'TASK-003')]`** (exit 1; R3 旧 (e) 对 v3 为 PASS, 见 R3 [6b]) — 扩维落地。(d) 旧图配方 ⇒ FAIL, (a) 13 对 / (d) 两条与段落一致, (e) 不一致 ⇒ b7743802。

### [7] 本轮触点新表面 + R3 minor 闭合细节 — 脚本 `s10_new_surface.py`

```python
#!/usr/bin/env python3
"""R4/A4 [7] 本轮触点新表面 + R3 minor 闭合细节:
1 母贴文 [a] 链渲染方向 vs deps  2 TASK-040 六条款 vs 字段 TASK-022 / 探针 TASK-018 授权句  3 三份 tasks.md Status 行 vs yaml metadata.status
4 探针 tasks.md :25 子句双写 / :11 措辞 / 已知限尾句  5 母 :232 / 8.4 行  6 字段 5.5 check 列表 vs yaml TASK-024  7 proposal「40 tasks」 8 带圈数字计数 (观察)"""
import re,yaml
C="/home/dev/Aria/openspec/changes/"
def Y(s): return yaml.safe_load(open(C+s+"/detailed-tasks.yaml",encoding="utf-8"))
def MD(s): return open(C+s+"/tasks.md",encoding="utf-8").read()
A=Y("a1-entry-claim-duplicate-work-guard"); L=Y("linked-issue-field-availability"); S=Y("sibling-spec-probe")
TA={t["id"]:t for t in A["tasks"]}; TL={t["id"]:t for t in L["tasks"]}; TS={t["id"]:t for t in S["tasks"]}
depsA={i:list(t.get("dependencies") or []) for i,t in TA.items()}
def anc(i,seen=None):
    seen=set() if seen is None else seen
    for j in depsA[i]:
        if j not in seen: seen.add(j); anc(j,seen)
    return seen
print("## 1 母 tasks.md 贴出 [a] 链渲染: 每对 x -> y 是否 x ∈ anc(y) (即箭头 = 依赖方向)")
md=MD("a1-entry-claim-duplicate-work-guard"); sec=md[md.index("### 机械核验"):]
out=[b for l,b in re.findall(r"```(\w*)\n(.*?)\n```", sec, re.S) if l in ("","text")][0]
bad=[]
for l in out.splitlines():
    m=re.match(r"\s+(\S+): (TASK-\d{3}(?: -> TASK-\d{3})+)$", l)
    if not m: continue
    chain=m.group(2).split(" -> ")
    for x,y in zip(chain,chain[1:]):
        ok = x in anc(y); rev = y in anc(x)
        if not ok: bad.append((m.group(1),x,y,"反向 (y 依赖 x 不成立, x 依赖 y 成立)" if rev else "无边"))
print("   链条数:", sum(1 for l in out.splitlines() if re.match(r"\s+\S+: TASK-\d{3} -> ",l)), "; 箭头与依赖方向不一致的对:", bad or "none")
print("   TASK-038.deps =", depsA["TASK-038"], "; TASK-040.deps =", depsA["TASK-040"], "; tasks.md 8.4 行含「执行序 8.1 → 8.4 → 8.2」:", "执行序 8.1 → 8.4 → 8.2" in md)
print("\n## 2 TASK-040 六条款 vs 字段 TASK-022 (关键词逐条) + 探针 TASK-018 授权句")
KW=[("新鲜度前置","fetch",["stale-local-main"]),("本地 merge + 合并源","merge --no-ff",["Do: merge"]),("owner 授权门","显式授权",["sync≠push-auth"]),("超时","超时",["partial-push"]),("逐 remote ls-remote","ls-remote",["不信 push 回执"]),("gitlink 后置","gitlink",["post-merge master SHA"])]
for name,kw,extra in KW:
    v40="\n".join(TA["TASK-040"]["verification"]); v22="\n".join(TL["TASK-022"]["verification"]); v18="\n".join(TS["TASK-018"]["verification"])
    print(f"   {name:14s} 040:{'Y' if kw in v40 and all(e in v40 for e in extra) else 'N'}  022:{'Y' if kw in v22 and all(e in v22 for e in extra) else 'N'}  018:{'Y' if kw in v18 else 'N'}")
print("   TASK-040 v[0] fetch 命令:", re.search(r"`git -C aria fetch[^`]*`", TA["TASK-040"]["verification"][0]).group(0))
print("   TASK-022 v[0] fetch 命令:", re.search(r"`git -C aria fetch[^`]*`", TL["TASK-022"]["verification"][0]).group(0))
print("   TASK-040 v[1] 合并源:", re.search(r"merge --no-ff (\S+)", TA["TASK-040"]["verification"][1]).group(1), "| deliverable 注释合并源:", re.search(r"merge --no-ff (\S+)", open(C+"a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml",encoding="utf-8").read().split("- id: TASK-040")[1].split("verification:")[0]).group(1))
print("   TASK-040 v 含「300」:", any("300" in v for v in TA["TASK-040"]["verification"]), "| 含「不写具体秒数」:", any("不写具体秒数" in v for v in TA["TASK-040"]["verification"]))
print("\n## 3 三份 tasks.md Status 行 vs yaml metadata.status")
for s,d in [("linked-issue-field-availability",L),("sibling-spec-probe",S),("a1-entry-claim-duplicate-work-guard",A)]:
    m=re.search(r"^> \*\*Status\*\*:.*$", MD(s), re.M); line=m.group(0) if m else "(无 Status 行)"
    tags=[t for t in ("待 R2","R2 待跑","待 R3","R3 待跑","待 R4","R4 待跑","R3 清账","R2 清账") if t in line]
    print(f"   {s}: tasks.md Status 含 {tags}; 行号 {MD(s)[:m.start()].count(chr(10))+1 if m else '-'}; yaml status 尾: …{d['metadata']['status'][-40:]}")
print("\n## 4 探针 tasks.md :25 TASK-003 子句 / :11 / 已知限尾句")
smd=MD("sibling-spec-probe").splitlines()
clause=smd[24].split("1.3 (TASK-003)")[1].split("; 2.x")[0]
print("   子句内「各含 TASK-003」次数:", clause.count("各含 TASK-003"), "| 含「主控裁量落第 4/5 组」:", "落第 4/5 组" in clause, "| 含 TASK-004:", "TASK-004" in clause)
print("   子句逐字:", clause[:400])
print("   :11 含「只剩第 1 组 (三任务不同文件)」:", "只剩第 1 组 (三任务不同文件)" in smd[10])
k=[i for i,l in enumerate(smd) if l.startswith("**已知限 (诚实声明)**")]; print("   已知限行号:", [i+1 for i in k], "| 含「主控已追记加边」:", any("主控已追记加边" in smd[i] for i in k))
print("\n## 5 母 :232 / :455 / :265")
amd=md.splitlines()
print("   :232 含「40 任务」:", "40 任务" in amd[231], "| 含「39」:", bool(re.search(r"\b39\b",amd[231])), "| :455 含「40 tasks」:", "40 tasks" in amd[454], "| :265 「未标只读」出现于「本条原文「未标只读…」已勘正」句:", "本条原文「未标只读" in amd[264])
print("\n## 6 字段 tasks.md 5.5 check 列表 vs yaml TASK-024 verification")
lmd=MD("linked-issue-field-availability").splitlines(); l55=[l for l in lmd if l.startswith("- [ ] 5.5")][0]
chk_md=set(re.findall(r"`(m6-[a-z-]+|main-project-version-consistency|i18n-readme-translation-currency)`", l55)); chk_y=set(re.findall(r"`(m6-[a-z-]+|main-project-version-consistency|i18n-readme-translation-currency)`", "\n".join(TL["TASK-024"]["verification"])))
print("   5.5 check 集合:", sorted(chk_md), "| yaml TASK-024 check 集合:", sorted(chk_y), "| yaml 有而 5.5 无:", sorted(chk_y-chk_md))
print("   5.5 含「14 点」:", "14 点" in l55, "| 含 CLAUDE.md:139/:141:", "CLAUDE.md:139/:141" in l55, "| yaml TASK-024 title 含「14 点」+ CLAUDE.md:", "14 点" in TL["TASK-024"]["title"] and "CLAUDE.md" in TL["TASK-024"]["title"])
print("\n## 7 proposal (非本席被审对象, 观察): a1 proposal Status 含「40 tasks」:", "40 tasks" in open(C+"a1-entry-claim-duplicate-work-guard/proposal.md",encoding="utf-8").read(), "| 含「39 tasks」:", "39 tasks" in open(C+"a1-entry-claim-duplicate-work-guard/proposal.md",encoding="utf-8").read())
print("\n## 8 带圈数字 ((1)-(20)) 计数 (观察, 非 finding):")
for s in ("linked-issue-field-availability","sibling-spec-probe","a1-entry-claim-duplicate-work-guard"):
    for f in ("tasks.md","detailed-tasks.yaml"):
        t=open(C+s+"/"+f,encoding="utf-8").read(); print(f"   {s}/{f}: {sum(1 for ch in t if 0x2460<=ord(ch)<=0x2473)}")
```

```
## 1 母 tasks.md 贴出 [a] 链渲染: 每对 x -> y 是否 x ∈ anc(y) (即箭头 = 依赖方向)
   链条数: 20 ; 箭头与依赖方向不一致的对: [('aria', 'TASK-038', 'TASK-040', '反向 (y 依赖 x 不成立, x 依赖 y 成立)')]
   TASK-038.deps = ['TASK-037', 'TASK-040'] ; TASK-040.deps = ['TASK-037'] ; tasks.md 8.4 行含「执行序 8.1 → 8.4 → 8.2」: True

## 2 TASK-040 六条款 vs 字段 TASK-022 (关键词逐条) + 探针 TASK-018 授权句
   新鲜度前置          040:Y  022:Y  018:N
   本地 merge + 合并源 040:Y  022:Y  018:N
   owner 授权门      040:Y  022:Y  018:Y
   超时             040:Y  022:Y  018:N
   逐 remote ls-remote 040:Y  022:Y  018:Y
   gitlink 后置     040:Y  022:Y  018:Y
   TASK-040 v[0] fetch 命令: `git -C aria fetch origin && git -C aria fetch github`
   TASK-022 v[0] fetch 命令: `git -C aria fetch origin github`
   TASK-040 v[1] 合并源: feature/a1-entry-claim-duplicate-work-guard` | deliverable 注释合并源: feature/<branch>`
   TASK-040 v 含「300」: False | 含「不写具体秒数」: True

## 3 三份 tasks.md Status 行 vs yaml metadata.status
   linked-issue-field-availability: tasks.md Status 含 []; 行号 5; yaml status 尾: …→ R3 清账 2026-08-31; 待 R4 收敛判定 (Rule #10)
   sibling-spec-probe: tasks.md Status 含 ['待 R2']; 行号 5; yaml status 尾: … tasks.md); 待 R4 收敛判定; all tasks pending
   a1-entry-claim-duplicate-work-guard: tasks.md Status 含 ['R2 待跑']; 行号 5; yaml status 尾: …); 待 R4 收敛判定 (Rule #10: enabled 闸门不自行豁免)

## 4 探针 tasks.md :25 TASK-003 子句 / :11 / 已知限尾句
   子句内「各含 TASK-003」次数: 2 | 含「主控裁量落第 4/5 组」: True | 含 TASK-004: True
   子句逐字:  是 B.1 前置 (proposal :473 逐字: 「该任务未 done 则 Phase B.1 不得开始」 — 边: TASK-004 (第 2 组起点, 主控 R1 追记) / 015 / 016 / 017 的 `dependencies` 各含 TASK-003, 且 TASK-003 ← TASK-002 (R3/A4 10e7cea4 补); 边: TASK-015 / 016 / 017 `dependencies` 各含 TASK-003, 主控裁量落第 4/5 组)
   :11 含「只剩第 1 组 (三任务不同文件)」: True
   已知限行号: [338] | 含「主控已追记加边」: True

## 5 母 :232 / :455 / :265
   :232 含「40 任务」: True | 含「39」: False | :455 含「40 tasks」: True | :265 「未标只读」出现于「本条原文「未标只读…」已勘正」句: True

## 6 字段 tasks.md 5.5 check 列表 vs yaml TASK-024 verification
   5.5 check 集合: ['i18n-readme-translation-currency', 'm6-version-badge-match', 'main-project-version-consistency'] | yaml TASK-024 check 集合: ['i18n-readme-translation-currency', 'm6-claude-md-version', 'm6-version-badge-match', 'main-project-version-consistency'] | yaml 有而 5.5 无: ['m6-claude-md-version']
   5.5 含「14 点」: True | 含 CLAUDE.md:139/:141: True | yaml TASK-024 title 含「14 点」+ CLAUDE.md: True

## 7 proposal (非本席被审对象, 观察): a1 proposal Status 含「40 tasks」: True | 含「39 tasks」: False

## 8 带圈数字 ((1)-(20)) 计数 (观察, 非 finding):
   linked-issue-field-availability/tasks.md: 0
   linked-issue-field-availability/detailed-tasks.yaml: 0
   sibling-spec-probe/tasks.md: 3
   sibling-spec-probe/detailed-tasks.yaml: 3
   a1-entry-claim-duplicate-work-guard/tasks.md: 27
   a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml: 52
```

### [7b] 字段 TASK-022 v[0] `git -C aria fetch origin github` 语义演示 (scratchpad 本地裸仓, 无网络) — 脚本 `s11_fetch_demo.sh`

```bash
#!/bin/bash
# R4/A4 [7b] 字段 TASK-022 verification[0] 的 `git -C aria fetch origin github` 语义演示 (本地裸仓, 无网络): 第二个位置参数是 refspec 不是第二个 remote
set -u
T=/tmp/claude-1000/-home-dev-Aria/0335d8a8-ad33-4d3d-9787-8f5ca5adea98/scratchpad/r4a4/gitdemo; rm -rf "$T"; mkdir -p "$T"; cd "$T"
git init -q --bare origin.git; git init -q --bare github.git; git init -q -b master work; cd work
git config user.email a@b.c; git config user.name t; echo x > f; git add f; git commit -qm init
git remote add origin ../origin.git; git remote add github ../github.git; git push -q origin master; git push -q github master
echo "--- git fetch origin github (TASK-022 原文形态):"; git fetch origin github; echo "exit=$?"
echo "--- git fetch origin && git fetch github (TASK-040 形态):"; git fetch origin && git fetch github; echo "exit=$?"
echo "--- git fetch --multiple origin github (等价正确形态):"; git fetch --multiple origin github; echo "exit=$?"
echo "--- git --version:"; git --version
```

```
--- git fetch origin github (TASK-022 原文形态):
fatal: couldn't find remote ref github
exit=128
--- git fetch origin && git fetch github (TASK-040 形态):
exit=0
--- git fetch --multiple origin github (等价正确形态):
Fetching origin
Fetching github
exit=0
--- git --version:
git version 2.39.5
```

### [7c] 杂项 (`s7_misc.py` 逐字复用; 行号类断言以 [7] 为准 — 探针 tasks.md 已从 309 行长到 338 行, s7 的「:309 含『主控已追记加边』: False」是行号漂移, [7 §4] 按内容定位到 :338 为 True)

```
TASK-003 deliverables 行=16; 含「只读」=2 (['aria/skills/state-scanner/scripts/phase1_gate.py', 'aria/skills/state-scanner/scripts/release_gate.py'])
a1 tasks.md :232 -> - **Phase A.3**: 无需新 Agent — 既有 roster `backend-architect` (lib / CLI) · `qa-engineer` (红测 / 结构测试 / AB) · `knowledge-manager` (SKILL.md / references / …
a1 tasks.md :265 -> 5. 同文件核验 (a) 的排除规则: deliverable 注释含「只读」或路径以 `/` 结尾 (`docs/handoff/` 追加型宿主, TASK-001/002/036/039 共用) 不计为写入方; 为此把 TASK-002 三条存在性断言的注释补了「只读」字样。TASK-003 ( …
a1 tasks.md :455 -> 解析器: PyYAML `safe_load` 通过; `aria/skills/state-scanner/scripts/lib/detailed_tasks.py::parse_detailed_tasks` ⇒ `parse_ok=True`, 40 tasks, status 集合 `{p …
a1 tasks.md :265 含「未标只读」: True
a1 TASK-018 verification 委派句: ['正常委派路径 (phase-a-planner → spec-drafter) 下幂等谓词使只写一条 claim: 由 TASK-025 (SC-22 (3) 幂等谓词结构测试) 验; 行为层 (真跑两次 A.1 只写一条 claim) 当前*']
sibling tasks.md :25 「1.3 (TASK-003) …」节选:  是 B.1 前置 (proposal :473 逐字: 「该任务未 done 则 Phase B.1 不得开始」 — 边: TASK-004 (第 2 组起点, 主控 R1 追记) / 015 / 016 / 017 的 `dependencies` 各含 
sibling tasks.md :25 TASK-003 子句含 TASK-004: True | 子句列的边: ['TASK-004', 'TASK-003', 'TASK-003', 'TASK-002', 'TASK-015 / 016 / 017', 'TASK-003'] | :11 含「只剩第 1 组 (三任务不同文件)」: True
sibling tasks.md :309 已知限尾句含「主控已追记加边」: False
linked yaml 「新增 新 eval」出现次数: 1
```

### [8] R3 → R4 六份 diff (基线 = [0b] 重建的 R3 六份; n=0 上下文) — 脚本 `s8_diff.py`

```python
#!/usr/bin/env python3
"""R4/A4 [8] R3 → R4 六份 diff (基线 = r3base, 六份 sha256 与 R3 报告 [0] 逐字相等). n=0 上下文; 全文落盘 diff_<spec>_<file>.txt, 此处打印 hunk 统计 + 每 hunk 首行 (截 160 字符)."""
import difflib, pathlib
SP=pathlib.Path("/tmp/claude-1000/-home-dev-Aria/0335d8a8-ad33-4d3d-9787-8f5ca5adea98/scratchpad/r4a4"); B=SP/"r3base"; CUR=pathlib.Path("/home/dev/Aria/openspec/changes")
for spec,short in [("linked-issue-field-availability","linked"),("sibling-spec-probe","sibling"),("a1-entry-claim-duplicate-work-guard","a1")]:
    for f,fs in [("tasks.md","md"),("detailed-tasks.yaml","yaml")]:
        a=(B/spec/f).read_text(encoding="utf-8").splitlines(); b=(CUR/spec/f).read_text(encoding="utf-8").splitlines()
        d=list(difflib.unified_diff(a,b,fromfile=f"R3/{f}",tofile=f"R4/{f}",lineterm="",n=0))
        (SP/f"diff_{short}_{fs}.txt").write_text("\n".join(d),encoding="utf-8")
        hunks=[l for l in d if l.startswith("@@")]; plus=sum(1 for l in d[2:] if l.startswith("+")); minus=sum(1 for l in d[2:] if l.startswith("-"))
        print(f"== {spec}/{f}: hunks={len(hunks)} +{plus} -{minus}  (R3 lines={len(a)} R4 lines={len(b)})")
        i=0
        while i<len(d):
            if d[i].startswith("@@"):
                nxt=d[i+1] if i+1<len(d) else ""; print(f"   {d[i]}  {nxt[:160]}")
            i+=1
```

```
== linked-issue-field-availability/tasks.md: hunks=4 +5 -5  (R3 lines=320 R4 lines=320)
   @@ -73 +73 @@  -- [ ] 4.3 套件缺口 issue — **A.2 裁量: 归并到 `aria-plugin#117`** (open, 「AB 测试集缺 authoring 维度」类级 issue), 以评论追加本 Spec 为第二个实例 + 4.2 的 eval id 3 作为该维度的首条已落地 fixture; **不新
   @@ -82 +82 @@  -- [ ] 5.5 主仓版本引用面 — `VERSION:24` / `README.md:8` badge + `:242` Plugin Version / i18n ×3 各 3 点 (`:3` translated-from / `:10` badge / `:244` Plugin Version; **仅
   @@ -97 +97 @@  -| SC-7 | **行为** (定向 fixture) | — (无代码宿主, 不冒充) | 4.2 (TASK-017), 4.1 (TASK-016) | `aria-plugin-benchmarks/ab-suite/spec-drafter.json` eval id 3 + id 2 |
   @@ -139,2 +139,2 @@  -1. **套件缺口 issue 归并 `aria-plugin#117` 而非新开**。实核 (`forgejo GET /repos/10CG/aria-plugin/issues/117`, 2026-08-30): **open**, 标题「[benchmark] AB 测试集缺 authoring 维度 — 
== linked-issue-field-availability/detailed-tasks.yaml: hunks=3 +3 -3  (R3 lines=724 R4 lines=724)
   @@ -62 +62 @@  -      - "任何改 `aria-plugin-benchmarks/ab-suite/*.json` 的任务同批按实际文件程序化重算 `ab-suite/version.yaml` (本 Spec: TASK-017); 新 eval id = 该文件当时 max(id)+1, ship 时读取不硬编码, 本 
   @@ -66 +66 @@  -  status: "A.2 + A.3 draft 2026-08-30 — 全部 pending; 待 post_planning (config post_planning=convergence, enabled ⇒ 照跑, Rule #10)"
   @@ -612 +612 @@  -    title: "主仓版本引用面 — VERSION:24 + README.md 2 点 + i18n ×3 各 3 点 (仅版本串)"
== sibling-spec-probe/tasks.md: hunks=5 +37 -8  (R3 lines=309 R4 lines=338)
   @@ -25 +25 @@  -> **组间门 (每条都有 yaml 边, 不再只是散文 — R1 C1 第 3 条 / A3 98e71a6a)**: 1.1 (TASK-001) 阻塞 2.x 起的一切 (边: TASK-004~009 `dependencies` 各含 TASK-001; import 目标不存在 ⇒ 探针无宿主, 测试骨架
   @@ -145 +145 @@  -| a257ffa4 (A1) | A1 · critical | **closed** — TASK-018 发布同步面补齐主仓 `VERSION` / `README.md` / i18n ×3 / gitlink `aria`, 「不重译」改为「正文不重译, 标记与两处版本串必改」, 两条 check 改为「全
   @@ -231 +231,3 @@  -# (e)
   @@ -233,4 +235,15 @@  -    if "并行" in line:
   @@ -300 +313,17 @@  -(e) parallel line ['TASK-001', 'TASK-002', 'TASK-003']: same-file pairs = none
== sibling-spec-probe/detailed-tasks.yaml: hunks=5 +5 -4  (R3 lines=620 R4 lines=621)
   @@ -25 +25 @@  -  status: "A.3 draft 2026-08-30 — post_planning R1 清账已落 (2026-08-30, 对账见 tasks.md「R1 清账对账」); 待 R2; all tasks pending"
   @@ -556 +556 @@  -      # --- 主仓引用面 (参照上次发布 commit 086ee32 的 7 文件 + 字段 TASK-024 的 12 点) ---
   @@ -566 +566 @@  -      - "主仓 12 个版本引用点全部改为 <vNEXT> (VERSION:24 / README.md:8,:242 / README.{zh,ja,ko}.md 各 :3,:10,:244; 行号按 c120f9e 实读, 落地时以 grep 为准): `grep -rn '<旧号>' VERSION 
   @@ -571,0 +572 @@  +      - "推送共享 master 是外向不可撤销动作: 须 owner **显式授权** (memory sync≠push-auth); 未授权前停在本地合并态并在 handoff 留痕 (R3/A1 3221f943 探针侧同批补)"
   @@ -575 +576 @@  -      R1 C2: deliverables 原缺主仓 VERSION / root README badge / i18n ×3, 且「不重译 ⇒ 不动 i18n」会使两条 check 必红; 已按字段 TASK-024 12 点口径 + 086ee32 实际文件集补齐.
== a1-entry-claim-duplicate-work-guard/tasks.md: hunks=6 +6 -6  (R3 lines=471 R4 lines=471)
   @@ -92 +92 @@  -- [ ] 8.4 aria 子模块本地 merge → master + 双推 + 逐 remote `ls-remote` 核验 + tag (CLAUDE.md 硬约束 1/2 的任务宿主; 两 remote 一致后才做 8.2 gitlink bump) — R2/A1 3221f943 残留补
   @@ -232 +232 @@  -- **Phase A.3**: 无需新 Agent — 既有 roster `backend-architect` (lib / CLI) · `qa-engineer` (红测 / 结构测试 / AB) · `knowledge-manager` (SKILL.md / references / config /
   @@ -265 +265 @@  -5. 同文件核验 (a) 的排除规则: deliverable 注释含「只读」或路径以 `/` 结尾 (`docs/handoff/` 追加型宿主, TASK-001/002/036/039 共用) 不计为写入方; 为此把 TASK-002 三条存在性断言的注释补了「只读」字样。TASK-003 (锚点核对) 的 1
   @@ -422 +422 @@  -输出 (逐字, exit 0; R2 后重跑 2026-08-30: TASK-003 只读标注 + TASK-040 + (d) 缩写展开后):
   @@ -426 +426 @@  -      aria: TASK-040 -> TASK-038
   @@ -455 +455 @@  -解析器: PyYAML `safe_load` 通过; `aria/skills/state-scanner/scripts/lib/detailed_tasks.py::parse_detailed_tasks` ⇒ `parse_ok=True`, 39 tasks, status 集合 `{pending}`。
== a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml: hunks=7 +28 -24  (R3 lines=1019 R4 lines=1023)
   @@ -25 +25 @@  -  status: "A.2/A.3 落版 2026-08-30; post_planning R1 FAIL → R1 清账落版 2026-08-30 (对账见 tasks.md「R1 清账对账」段); R2 待跑 (Rule #10: enabled 闸门不自行豁免)"
   @@ -174,0 +175 @@  +      - "另记录 (供 TASK-018 (i)/(ii) 分支输入, R3/A1 a7311d2e): `grep -n 'Linked Issue' aria/skills/spec-drafter/SKILL.md` 命中 ⇒ 字段 Spec 的 spec-drafter hunk A/B 已 ship
   @@ -553 +554 @@  -      - "正常委派路径 (phase-a-planner → spec-drafter) 下幂等谓词使只写一条 claim: 由 TASK-025 (SC-22 (3) 幂等谓词结构测试) 验; TASK-035 fixture (a) 的「一次 A.1 两条 claim」坏臂为行为层补充 (R2/A1 mino
   @@ -873,0 +875 @@  +      - "运行前置 (Rule #7 射程 + R1 C5): 会话以 `ARIA_COORDINATION_NO_PUSH=1 claude …` 启动 (AB_TEST_OPERATIONS.md:222-228), transcript 核验 `push_skipped: true` — R3/A4 1
   @@ -939 +941 @@  -    dependencies: [TASK-011, TASK-012, TASK-013, TASK-014, TASK-015, TASK-016, TASK-017, TASK-018, TASK-019, TASK-020, TASK-021, TASK-022, TASK-023, TASK-025, 
   @@ -955,21 +956,0 @@  -
   @@ -1019,0 +1001,23 @@  +  - id: TASK-040
```

逐 hunk (行截 240 字符; 六份全文落盘 `r4a4/diff_<spec>_<md|yaml>.txt`):

```diff
--- R3/tasks.md
+++ R4/tasks.md
@@ -73 +73 @@
-- [ ] 4.3 套件缺口 issue — **A.2 裁量: 归并到 `aria-plugin#117`** (open, 「AB 测试集缺 authoring 维度」类级 issue), 以评论追加本 Spec 为第二个实例 + 4.2 的 eval id 3 作为该维度的首条已落地 fixture; **不新开** issue (理由见「A.2 裁量」段; owner 可改判新开)
+- [ ] 4.3 套件缺口 issue — **A.2 裁量: 归并到 `aria-plugin#117`** (open, 「AB 测试集缺 authoring 维度」类级 issue), 以评论追加本 Spec 为第二个实例 + 4.2 的 新 eval (id = ship 时 max(id)+1, 今日观测 3) 作为该维度的首条已落地 fixture; **不新开** issue (理由见「A.2 裁量」段; owner 可改判新开)
@@ -82 +82 @@
-- [ ] 5.5 主仓版本引用面 — `VERSION:24` / `README.md:8` badge + `:242` Plugin Version / i18n ×3 各 3 点 (`:3` translated-from / `:10` badge / `:244` Plugin Version; **仅版本串**, 正文无实质变更不重译, #140 B 档); custom checks `m6-version-badge-match` / `i18n-rea …[截 67 字符]
+- [ ] 5.5 主仓版本引用面 14 点 (与 086ee32 同口径) — `CLAUDE.md:139/:141` / `VERSION:24` / `README.md:8` badge + `:242` Plugin Version / i18n ×3 各 3 点 (`:3` translated-from / `:10` badge / `:244` Plugin Version; **仅版本串**, 正文无实质变更不重译, #140 B 档); custom …[截 111 字符]
@@ -97 +97 @@
-| SC-7 | **行为** (定向 fixture) | — (无代码宿主, 不冒充) | 4.2 (TASK-017), 4.1 (TASK-016) | `aria-plugin-benchmarks/ab-suite/spec-drafter.json` eval id 3 + id 2 |
+| SC-7 | **行为** (定向 fixture) | — (无代码宿主, 不冒充) | 4.2 (TASK-017), 4.1 (TASK-016) | `aria-plugin-benchmarks/ab-suite/spec-drafter.json` 新 eval (id = ship 时 max(id)+1, 今日观测 3) + id 2 |
@@ -139,2 +139,2 @@
-1. **套件缺口 issue 归并 `aria-plugin#117` 而非新开**。实核 (`forgejo GET /repos/10CG/aria-plugin/issues/117`, 2026-08-30): **open**, 标题「[benchmark] AB 测试集缺 authoring 维度 — 全套件零 eval 覆盖『作者读处方性向导做判断』类行为」, 正文点名 `spec-drafter.json` (2) 「均为产出/判级/路径类, 无 auth …[截 234 字符]
-2. **SC-7 双臂的落法**: 中文臂 = 新增 eval id 3 (定向 fixture ×1); 英文臂 = eval id 2 更新 expectations 后即是 (SC-7 原文「后者即 `spec-drafter.json` eval id 2 的场景」)。不为英文臂再开 eval id 4。
+1. **套件缺口 issue 归并 `aria-plugin#117` 而非新开**。实核 (`forgejo GET /repos/10CG/aria-plugin/issues/117`, 2026-08-30): **open**, 标题「[benchmark] AB 测试集缺 authoring 维度 — 全套件零 eval 覆盖『作者读处方性向导做判断』类行为」, 正文点名 `spec-drafter.json` (2) 「均为产出/判级/路径类, 无 auth …[截 263 字符]
+2. **SC-7 双臂的落法**: 中文臂 = 新增 新 eval (id = ship 时 max(id)+1, 今日观测 3) (定向 fixture ×1); 英文臂 = eval id 2 更新 expectations 后即是 (SC-7 原文「后者即 `spec-drafter.json` eval id 2 的场景」)。不为英文臂再开 eval id 4。
```

```diff
--- R3/detailed-tasks.yaml
+++ R4/detailed-tasks.yaml
@@ -62 +62 @@
-      - "任何改 `aria-plugin-benchmarks/ab-suite/*.json` 的任务同批按实际文件程序化重算 `ab-suite/version.yaml` (本 Spec: TASK-017); 新 eval id = 该文件当时 max(id)+1, ship 时读取不硬编码, 本 Spec 先 ship 取到 3, 母 Spec 后 ship 顺延 (A1 6698004d / 35dad35d / C5)"
+      - "任何改 `aria-plugin-benchmarks/ab-suite/*.json` 的任务同批按实际文件程序化重算 `ab-suite/version.yaml` (本 Spec: TASK-017 新增 eval ⇒ 重算写入; TASK-016 只改既有 eval 2 的 expectations, 计数不变 ⇒ 同批**复核**两计数与重算相等即可, 不写入 — 与母 Spec seam_rules[2]「任何改 ab-suite/*.json …[截 158 字符]
@@ -66 +66 @@
-  status: "A.2 + A.3 draft 2026-08-30 — 全部 pending; 待 post_planning (config post_planning=convergence, enabled ⇒ 照跑, Rule #10)"
+  status: "A.2 + A.3 draft 2026-08-30 — 全部 pending; post_planning R1 FAIL → 清账 → R2 PwW → 清账 → R3 PwW (0C) → R3 清账 2026-08-31; 待 R4 收敛判定 (Rule #10)"
@@ -612 +612 @@
-    title: "主仓版本引用面 — VERSION:24 + README.md 2 点 + i18n ×3 各 3 点 (仅版本串)"
+    title: "主仓发版同步面 14 点 (与 086ee32 同口径): CLAUDE.md :139/:141 2 点 + VERSION:24 + README.md :8/:242 2 点 + i18n ×3 各 3 点 — 版本引用面"
```

```diff
--- R3/tasks.md
+++ R4/tasks.md
@@ -25 +25 @@
-> **组间门 (每条都有 yaml 边, 不再只是散文 — R1 C1 第 3 条 / A3 98e71a6a)**: 1.1 (TASK-001) 阻塞 2.x 起的一切 (边: TASK-004~009 `dependencies` 各含 TASK-001; import 目标不存在 ⇒ 探针无宿主, 测试骨架的模块级 skip 守卫也以它为前提); 1.3 (TASK-003) 是 B.1 前置 (proposal :473 逐字: 「该任务未 done 则 Pha …[截 213 字符]
+> **组间门 (每条都有 yaml 边, 不再只是散文 — R1 C1 第 3 条 / A3 98e71a6a)**: 1.1 (TASK-001) 阻塞 2.x 起的一切 (边: TASK-004~009 `dependencies` 各含 TASK-001; import 目标不存在 ⇒ 探针无宿主, 测试骨架的模块级 skip 守卫也以它为前提); 1.3 (TASK-003) 是 B.1 前置 (proposal :473 逐字: 「该任务未 done 则 Pha …[截 336 字符]
@@ -145 +145 @@
-| a257ffa4 (A1) | A1 · critical | **closed** — TASK-018 发布同步面补齐主仓 `VERSION` / `README.md` / i18n ×3 / gitlink `aria`, 「不重译」改为「正文不重译, 标记与两处版本串必改」, 两条 check 改为「全部文件完成后才断言绿」 | yaml TASK-018 deliverables (12 项, 与字段 TASK-024 12 点 + `086ee32` 7  …[截 61 字符]
+| a257ffa4 (A1) | A1 · critical | **closed** — TASK-018 发布同步面补齐主仓 `VERSION` / `README.md` / i18n ×3 / gitlink `aria`, 「不重译」改为「正文不重译, 标记与两处版本串必改」, 两条 check 改为「全部文件完成后才断言绿」 | yaml TASK-018 deliverables (12 项, 与字段 TASK-024 14 点 (R2 后口径, 含 CLA …[截 93 字符]
@@ -231 +231,3 @@
-# (e)
+# (e) execution_order 展示 vs dependencies (R3 扩维: A1 f137dded / A3 d935b128 — 箭头右侧 ⊆ deps[head]; 「并行」声明的任务间不得有依赖)
+def ids_in(seg):
+    return [f"TASK-{m.group(1)}" for m in re.finditer(r"(?:TASK-)?\b(\d{3})\b", re.sub(r"\([^)]*\)", "", seg))]
@@ -233,4 +235,15 @@
-    if "并行" in line:
-        ts = re.findall(r"TASK-\d{3}", line)
-        pairs = [(a, b) for i, a in enumerate(ts) for b in ts[i+1:] if deliv[a] & deliv[b]]
-        print(f"(e) parallel line {ts}: same-file pairs = {pairs or 'none'}")
+    stripped = re.sub(r"\([^)]*\)", "", line)
+    for seg in stripped.split("→"):
+        if "←" not in seg: continue
+        left, right = seg.split("←", 1)
+        hs = re.findall(r"TASK-\d{3}", left)
+        if not hs: continue
+        h = hs[-1]; rights = ids_in(right); missing = [r for r in rights if r not in deps.get(h, [])]
+        print(f"(e) {h} ← {rights}: {'OK' if not missing else 'NOT IN deps ' + str(missing)}")
+        if missing: fails.append(f"(e) {h} arrow {missing} not in dependencies")
+    if "并行" in stripped:
+        tsp = ids_in(stripped.split("并行")[0]) or ids_in(stripped)
+        contra = [(a, b) for i, a in enumerate(tsp) for b in tsp[i+1:] if a in deps.get(b, []) or b in deps.get(a, [])]
+        pairs = [(a, b) for i, a in enumerate(tsp) for b in tsp[i+1:] if deliv.get(a, set()) & deliv.get(b, set())]
+        print(f"(e) parallel claim {tsp}: dep-contradiction = {contra or 'none'}; same-file pairs = {pairs or 'none'}")
+        if contra: fails.append(f"(e) parallel claim contradicts deps {contra}")
@@ -300 +313,17 @@
-(e) parallel line ['TASK-001', 'TASK-002', 'TASK-003']: same-file pairs = none
+(e) TASK-003 ← ['TASK-002']: OK
+(e) parallel claim ['TASK-001', 'TASK-002']: dep-contradiction = none; same-file pairs = none
+(e) TASK-004 ← ['TASK-001', 'TASK-002', 'TASK-003']: OK
+(e) TASK-005 ← ['TASK-001', 'TASK-004']: OK
+(e) TASK-006 ← ['TASK-001', 'TASK-005']: OK
+(e) TASK-007 ← ['TASK-001', 'TASK-006']: OK
+(e) TASK-008 ← ['TASK-001', 'TASK-007']: OK
+(e) TASK-009 ← ['TASK-001', 'TASK-008']: OK
+(e) TASK-010 ← ['TASK-004', 'TASK-008']: OK
+(e) TASK-011 ← ['TASK-010', 'TASK-005', 'TASK-006']: OK
+(e) TASK-012 ← ['TASK-011', 'TASK-010', 'TASK-007']: OK
+(e) TASK-013 ← ['TASK-012', 'TASK-007']: OK
+(e) TASK-014 ← ['TASK-009', 'TASK-011', 'TASK-012', 'TASK-013']: OK
+(e) TASK-015 ← ['TASK-003', 'TASK-009']: OK
+(e) TASK-016 ← ['TASK-003', 'TASK-009', 'TASK-015']: OK
+(e) TASK-017 ← ['TASK-003', 'TASK-014', 'TASK-015', 'TASK-016']: OK
+(e) TASK-018 ← ['TASK-017']: OK
```

```diff
--- R3/detailed-tasks.yaml
+++ R4/detailed-tasks.yaml
@@ -25 +25 @@
-  status: "A.3 draft 2026-08-30 — post_planning R1 清账已落 (2026-08-30, 对账见 tasks.md「R1 清账对账」); 待 R2; all tasks pending"
+  status: "A.3 draft 2026-08-30 — post_planning R1 清账 → R2 PwW → R2 清账 → R3 PwW (0C) → R3 清账 2026-08-31 (对账见 tasks.md); 待 R4 收敛判定; all tasks pending"
@@ -556 +556 @@
-      # --- 主仓引用面 (参照上次发布 commit 086ee32 的 7 文件 + 字段 TASK-024 的 12 点) ---
+      # --- 主仓引用面 (参照上次发布 commit 086ee32 的 7 文件 + 字段 TASK-024 的 14 点) ---
@@ -566 +566 @@
-      - "主仓 12 个版本引用点全部改为 <vNEXT> (VERSION:24 / README.md:8,:242 / README.{zh,ja,ko}.md 各 :3,:10,:244; 行号按 c120f9e 实读, 落地时以 grep 为准): `grep -rn '<旧号>' VERSION README.md README.*.md` 零命中; CLAUDE.md :139/:141 同步 (只改版本号, 不加术语)"
+      - "主仓 14 个版本引用点全部改为 <vNEXT> (CLAUDE.md:139,:141 / VERSION:24 / README.md:8,:242 / README.{zh,ja,ko}.md 各 :3,:10,:244; 行号按 c120f9e 实读, 落地时以 grep 为准): `grep -rn '<旧号>' CLAUDE.md VERSION README.md README.*.md` 零命中; CLAUDE.md :139/:141 同 …[截 16 字符]
@@ -571,0 +572 @@
+      - "推送共享 master 是外向不可撤销动作: 须 owner **显式授权** (memory sync≠push-auth); 未授权前停在本地合并态并在 handoff 留痕 (R3/A1 3221f943 探针侧同批补)"
@@ -575 +576 @@
-      R1 C2: deliverables 原缺主仓 VERSION / root README badge / i18n ×3, 且「不重译 ⇒ 不动 i18n」会使两条 check 必红; 已按字段 TASK-024 12 点口径 + 086ee32 实际文件集补齐.
+      R1 C2: deliverables 原缺主仓 VERSION / root README badge / i18n ×3, 且「不重译 ⇒ 不动 i18n」会使两条 check 必红; 已按字段 TASK-024 14 点口径 (R3 同步, 含 CLAUDE.md 两点) + 086ee32 实际文件集补齐.
```

```diff
--- R3/tasks.md
+++ R4/tasks.md
@@ -92 +92 @@
-- [ ] 8.4 aria 子模块本地 merge → master + 双推 + 逐 remote `ls-remote` 核验 + tag (CLAUDE.md 硬约束 1/2 的任务宿主; 两 remote 一致后才做 8.2 gitlink bump) — R2/A1 3221f943 残留补
+- [ ] 8.4 aria 子模块本地 merge → master + 双推 + 逐 remote `ls-remote` 核验 + tag (CLAUDE.md 硬约束 1/2 的任务宿主; 两 remote 一致后才做 8.2 gitlink bump) — R2/A1 3221f943 残留补; **执行序 8.1 → 8.4 → 8.2** (编号不可变, 列于末不代表最后做; 见 yaml dependencies)
@@ -232 +232 @@
-- **Phase A.3**: 无需新 Agent — 既有 roster `backend-architect` (lib / CLI) · `qa-engineer` (红测 / 结构测试 / AB) · `knowledge-manager` (SKILL.md / references / config / standards / CHANGELOG) · `tech-lead` (跨仓前置断言 / issue 裁量 / 主仓同步面) 覆盖全部 39 任务。
+- **Phase A.3**: 无需新 Agent — 既有 roster `backend-architect` (lib / CLI) · `qa-engineer` (红测 / 结构测试 / AB) · `knowledge-manager` (SKILL.md / references / config / standards / CHANGELOG) · `tech-lead` (跨仓前置断言 / issue 裁量 / 主仓同步面) 覆盖全部 40 任务。
@@ -265 +265 @@
-5. 同文件核验 (a) 的排除规则: deliverable 注释含「只读」或路径以 `/` 结尾 (`docs/handoff/` 追加型宿主, TASK-001/002/036/039 共用) 不计为写入方; 为此把 TASK-002 三条存在性断言的注释补了「只读」字样。TASK-003 (锚点核对) 的 16 条 deliverable 未标只读, 被计为上游写入方, 因全部下游都传递依赖它而恒通过 — 是更严而非更松。
+5. 同文件核验 (a) 的排除规则: deliverable 注释含「只读」或路径以 `/` 结尾 (`docs/handoff/` 追加型宿主, TASK-001/002/036/039 共用) 不计为写入方; 为此把 TASK-002 三条存在性断言的注释补了「只读」字样。TASK-003 (锚点核对) 的 `phase1_gate.py` / `release_gate.py` 两条 deliverable 在 R2 由主控补「只读核验」标注 (其余锚点 deliv …[截 79 字符]
@@ -422 +422 @@
-输出 (逐字, exit 0; R2 后重跑 2026-08-30: TASK-003 只读标注 + TASK-040 + (d) 缩写展开后):
+输出 (逐字, exit 0; R3 后重跑 2026-08-31: TASK-037 ← TASK-009 + TASK-040 移位 + TASK-002/018/034 文本后):
@@ -426 +426 @@
-      aria: TASK-040 -> TASK-038
+      aria: TASK-038 -> TASK-040
@@ -455 +455 @@
-解析器: PyYAML `safe_load` 通过; `aria/skills/state-scanner/scripts/lib/detailed_tasks.py::parse_detailed_tasks` ⇒ `parse_ok=True`, 39 tasks, status 集合 `{pending}`。残留字面量: 两文件 `grep '1\.68\.0\|README.zh-CN\|\.gitmodules'` 只剩本对账段与 TASK-038 notes  …[截 9 字符]
+解析器: PyYAML `safe_load` 通过; `aria/skills/state-scanner/scripts/lib/detailed_tasks.py::parse_detailed_tasks` ⇒ `parse_ok=True`, 40 tasks, status 集合 `{pending}`。残留字面量: 两文件 `grep '1\.68\.0\|README.zh-CN\|\.gitmodules'` 只剩本对账段与 TASK-038 notes  …[截 9 字符]
```

```diff
--- R3/detailed-tasks.yaml
+++ R4/detailed-tasks.yaml
@@ -25 +25 @@
-  status: "A.2/A.3 落版 2026-08-30; post_planning R1 FAIL → R1 清账落版 2026-08-30 (对账见 tasks.md「R1 清账对账」段); R2 待跑 (Rule #10: enabled 闸门不自行豁免)"
+  status: "A.2/A.3 落版 2026-08-30; post_planning R1 FAIL → 清账 → R2 PwW (票 3/5) → 清账 → R3 PwW (0C, 票 1/5) → R3 清账落版 2026-08-31 (对账见 tasks.md); 待 R4 收敛判定 (Rule #10: enabled 闸门不自行豁免)"
@@ -174,0 +175 @@
+      - "另记录 (供 TASK-018 (i)/(ii) 分支输入, R3/A1 a7311d2e): `grep -n 'Linked Issue' aria/skills/spec-drafter/SKILL.md` 命中 ⇒ 字段 Spec 的 spec-drafter hunk A/B 已 ship (i), 零命中 ⇒ 未 ship (ii); 与 live 分支同写入同一条 handoff 记录"
@@ -553 +554 @@
-      - "正常委派路径 (phase-a-planner → spec-drafter) 下幂等谓词使只写一条 claim: 由 TASK-025 (SC-22 (3) 幂等谓词结构测试) 验; TASK-035 fixture (a) 的「一次 A.1 两条 claim」坏臂为行为层补充 (R2/A1 minor: SC 映射里该臂宿主是 TASK-025)"
+      - "正常委派路径 (phase-a-planner → spec-drafter) 下幂等谓词使只写一条 claim: 由 TASK-025 (SC-22 (3) 幂等谓词结构测试) 验; 行为层 (真跑两次 A.1 只写一条 claim) 当前**无宿主, 成文不冒充** (R3/A3 532e5316: TASK-035 fixture (a) 测的是 SC-9/12/14(b), 与幂等无关)"
@@ -873,0 +875 @@
+      - "运行前置 (Rule #7 射程 + R1 C5): 会话以 `ARIA_COORDINATION_NO_PUSH=1 claude …` 启动 (AB_TEST_OPERATIONS.md:222-228), transcript 核验 `push_skipped: true` — R3/A4 199aa25c 补齐 (031–035 五处同句)"
@@ -939 +941 @@
-    dependencies: [TASK-011, TASK-012, TASK-013, TASK-014, TASK-015, TASK-016, TASK-017, TASK-018, TASK-019, TASK-020, TASK-021, TASK-022, TASK-023, TASK-025, TASK-026, TASK-027, TASK-028, TASK-029, TASK-030, TASK-031, TASK-032, TASK-033,  …[截 19 字符]
+    dependencies: [TASK-009, TASK-011, TASK-012, TASK-013, TASK-014, TASK-015, TASK-016, TASK-017, TASK-018, TASK-019, TASK-020, TASK-021, TASK-022, TASK-023, TASK-025, TASK-026, TASK-027, TASK-028, TASK-029, TASK-030, TASK-031, TASK-032,  …[截 112 字符]
@@ -955,21 +956,0 @@
-
-  - id: TASK-040
-    parent: "8.4"
-    task_group: 8
-    title: "aria 子模块本地 merge → master + 双推 + 逐 remote ls-remote 核验 + tag (硬约束 1/2 的任务宿主)"
-    status: pending
-    complexity: M
-    estimated_hours: "3-5"
-    agent: tech-lead
-    reason: "多远程 / 跨仓指针协调 (AGENT_MAPPING: cross-module, integration → tech-lead); 硬约束 1/2 的执行责任 (R2/A1 3221f943: 此前只活在 notes 散文里, 无任务宿主 — #165 那条腿)"
-    dependencies: [TASK-037]
-    deliverables:
-      - aria   # 子模块 master: 本地 `git -C aria merge --no-ff feature/<branch>` (禁 Forgejo 服务端合并, CLAUDE.md 硬约束 1) + `git -C aria tag v<vNEXT>`
-    verification:
-      - "合并在本地做: `git -C aria log -1 --format=%P master` 有两个父 (merge commit 本地生成), Forgejo PR 页面若存在只作审阅, 不点 Do: merge"
-      - "双推给足超时: `git -C aria push origin master --tags && git -C aria push github master --tags` (memory partial-push: 命令超时 ≥ 300s)"
-      - "推后逐个核验, 不信 push 回执: `git -C aria ls-remote origin master` / `git -C aria ls-remote github master` / `git -C aria rev-parse master` 三者 SHA 逐字节相等; tag 同法 (`ls-remote --tags`); ls-remote 自身失败 ⇒ 重试再下结论 (CLAUDE.md 硬约束 2)"
-      - "两 remote 一致后才允许 TASK-038 bump 主仓 gitlink (否则 orphaned gitlink, GitHub clone --recursive 断裂, 2026-07-14 事故形状)"
-    notes: >
-      R2/A1 残留 major: 字段 Spec 有 TASK-022、探针 Spec 落 TASK-018, 母 Spec 缺此宿主而 TASK-038 却断言「gitlink SHA 在两 remote 均可取到」
-      (断言了无人执行的动作的后置条件)。本任务补齐; 版本号沿 <vNEXT> 占位, 档位待 owner (TASK-037 notes 统一句)。
@@ -1019,0 +1001,23 @@
+  - id: TASK-040
+    parent: "8.4"
+    task_group: 8
+    title: "aria 子模块本地 merge → master + 双推 + 逐 remote ls-remote 核验 + tag (硬约束 1/2 的任务宿主)"
+    status: pending
+    complexity: M
+    estimated_hours: "3-5"
+    agent: tech-lead
+    reason: "多远程 / 跨仓指针协调 (AGENT_MAPPING: cross-module, integration → tech-lead); 硬约束 1/2 的执行责任 (R2/A1 3221f943: 此前只活在 notes 散文里, 无任务宿主 — #165 那条腿)"
+    dependencies: [TASK-037]
+    deliverables:
+      - aria   # 子模块 master: 本地 `git -C aria merge --no-ff feature/<branch>` (禁 Forgejo 服务端合并, CLAUDE.md 硬约束 1) + `git -C aria tag v<vNEXT>`
+    verification:
+      - "前置 (memory stale-local-main): `git -C aria fetch origin && git -C aria fetch github` 后断言本地 master == origin/master == github/master (`rev-parse` 三 SHA 逐字节相等); 不一致先处理, 不合进陈旧基线"
+      - "**本地** `git -C aria merge --no-ff feature/a1-entry-claim-duplicate-work-guard` (合并源 = 本 Spec 的 aria 侧 feature 分支, B.1 建; 硬约束 1: 禁 Forgejo Web/API `Do: merge`); merge commit 消息 Conventional Commits; 事后 `git -C aria log -1 --format= …[截 16 字符]
+      - "推送共享 master 是外向不可撤销动作: 须 owner **显式授权** (memory sync≠push-auth); 未授权前停在本地合并态并在 handoff 留痕, 不以「低风险 / 已审计」自我授权"
+      - "双推显式给足超时 (memory partial-push 08-29 追记: harness 默认超时曾把 push 截断成半推, 截断与失败事后不可分辨; 用 Bash 工具显式 `timeout` 取远高于历史耗时的值, 不写具体秒数): `git -C aria push origin master --tags && git -C aria push github master --tags`"
+      - "推后**逐个**核验, 不信 push 回执: `git -C aria ls-remote origin master` / `git -C aria ls-remote github master` / `git -C aria rev-parse master` 三者 SHA 逐字节相等; tag 同法 (`ls-remote --tags`); ls-remote 自身失败 ⇒ 重试再下结论 (硬约束 2)"
+      - "两 remote 一致后才允许 TASK-038 bump 主仓 gitlink (`git add aria` 指向 post-merge master SHA, 非 feature SHA; `git submodule status` 无 `+`/`-`), 否则 orphaned gitlink ⇒ GitHub clone --recursive 断裂 (2026-07-14 事故形状)"
+    notes: >
+      R2/A1 残留 major: 字段 Spec 有 TASK-022、探针 Spec 落 TASK-018, 母 Spec 缺此宿主而 TASK-038 却断言「gitlink SHA 在两 remote 均可取到」
+      (断言了无人执行的动作的后置条件)。本任务补齐; 版本号沿 <vNEXT> 占位, 档位待 owner (TASK-037 notes 统一句)。R3/A2 d95c381a: 六条款与字段 TASK-022 逐条对齐 (新鲜度前置 / 显式合并源 / owner 授权门 / 超时 / 逐 remote 核验 / gitlink 后置)。
+
```

由 R3 fix 引入占比的计法: 六条 finding 逐条问「R3 版本 ([0b] 基线) 里这个矛盾在不在」— b3039ea7 (R3 基线 :426 为 `aria: TASK-040 -> TASK-038`, 与依赖同向) / 9b08c5a9 (R3 基线 :25 只有一套边清单) / b7743802 (R3 基线 (e) 未扩维, 段落与旧 (e) 一致) 在 R3 版本不存在 ⇒ **3 条 fix 引入**; 6c7d0b50 (TASK-022 未被本轮 diff 触及, R2 副本同句) / d3de42d1 (三份 :5 本轮 0 hunk) ⇒ 2 条残留; e4a5cb08 ⇒ R3 partial。

### [9] 审后 sha256 复核 (2026-08-31T14:17:15.831Z; 与 [0] 逐行一致)

```
084835ef3bb86c5ebd9842c3afaa69874f5b220170aaa0a060d1e83cc0db1e16  openspec/changes/linked-issue-field-availability/tasks.md
471f30adbfb28c745898ec8a730589e5a146427d006f2d8cfddd79ff0fac3d1d  openspec/changes/linked-issue-field-availability/detailed-tasks.yaml
464216dd14ea1ed8dbd5ad43d0ecbed19a6b0e8525ec4470a92887b78c37f99a  openspec/changes/sibling-spec-probe/tasks.md
9448d8d8f49ca66179d26b8e13ca5b3c569b3de5438aa63f8f852ed81313d85e  openspec/changes/sibling-spec-probe/detailed-tasks.yaml
3830f3a51b01fea144e4af3a72783fca69a159b22350217adc25556e271da583  openspec/changes/a1-entry-claim-duplicate-work-guard/tasks.md
7c5a7ea50db723192fb2a2c479a5e3326daf898cea151809a3f09685213320f4  openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml
```

finding id 生成串 (sha256(...)[:8]):

```
b3039ea7  documentation:openspec/changes/a1-entry-claim-duplicate-work-guard/tasks.md#L426:minor:issue
9b08c5a9  documentation:openspec/changes/sibling-spec-probe/tasks.md#L25-duplicate-clause:minor:issue
e4a5cb08  documentation:openspec/changes/linked-issue-field-availability/tasks.md#L82-checks:minor:issue
6c7d0b50  implementation:openspec/changes/linked-issue-field-availability/detailed-tasks.yaml#TASK-022:minor:issue
d3de42d1  documentation:openspec/changes/{linked-issue-field-availability,sibling-spec-probe,a1-entry-claim-duplicate-work-guard}/tasks.md#L5-Status:minor:issue
b7743802  documentation:openspec/changes/sibling-spec-probe/tasks.md#L336:minor:issue
```

(scope 带 `#锚点` 是为了与 R1–R3 同 scope 的旧 id 区分; 9b08c5a9 / e4a5cb08 若不带后缀会分别算回 R3 的 10e7cea4 / e9ffaefe, 聚合时会串。)

脚本 sha256 (前 16 位):

```
1126bb3f6ee840ace  chk1_battery.py
e5cb00f33ea3a0abc  chk3_cov_deliv.py
136195e84f804fe0a  s2_execorder.py
979c90bfd2f834cb3  s3_task040.py
83d6e70faf4e5b690  s4_flags_summary.py
d0b0593e5f49a772b  s7_misc.py
3c4ceed0e73fc543d  s1b_parent_seq.py
349ad9f2a624548b8  extract_run_pasted.py
84c3e424b0f421427  s0_baseline.py
219a6039043208599  s3b_release_reach.py
a3fc242df7dcb9ae9  s5_residual_grep.sh
7c0671da65aa64af1  s8_diff.py
9df27c52b195a9b16  s9_adv.py
8e695bf4705913e4b  s10_new_surface.py
ee76100755ada4cb7  s11_fetch_demo.sh
```

## Verdict

**PASS** (0 critical / 0 major / 6 minor)。计划本体在机械层已收敛: 三份 yaml 两解析器通过, 依赖图无环无悬空、自述与边一致, 三份贴文与实跑逐行相等, 发布链三份对称向下可达, R3 唯一 major (发布链缺边) 一 token 闭合并程序化验证。六条 minor 全是文本层 (一条贴文链方向 / 一条子句双写 / 一个 check 名 / 一条命令语法 / 三处 Status 行 / 一段旧脚本证据), 不触 proposal、不改编号、不改 SC、不改依赖图; 其中 6c7d0b50 是唯一碰机制文本的一条 (新鲜度前置命令), 因失败响亮且修复一 token 判 minor。

## Vote

**PASS**。理由: (a) 主控要求的四项 (五脚本重跑全绿 / R3 1M+5m 逐条闭合 / 新表面 / fix 引入占比) 全部程序化落地, 无 C/M; (b) R3 六条 4 closed + 2 partial, 无 not_addressed, 两条 partial 都是「处方两半落一半」的文本残余; (c) 本轮 fix 引入 3/6 与 R3 持平在 1/2, 且三条全在展示层 — 按 memory `marginal-return-negative` / `stop-adding-rounds`, 再开通用轮只会审到更多同形; (d) 建议收账方式 = 执笔席落六处定点改动 (b3039ea7 重贴一行 / 9b08c5a9 删一子句 / e4a5cb08 加一 token / 6c7d0b50 改一命令 / d3de42d1 三处 Status / b7743802 重跑一段) 后**定向复核**: 重跑本席 `s10_new_surface.py` (§1 不一致对 = none; §3 三份 Status 含「待 R4」或更新; §4 「各含 TASK-003」×1 且无「落第 4/5 组」; §6 差集 = []) + `extract_run_pasted.py` (三份 identical=True, b3039ea7 重贴后必验) + `s9_adv.py` (d) 段 (段落与亲跑一致) + `grep -n 'fetch origin github'` 六份零命中 — 全绿即本席 scope 收敛, 不必再派五席。

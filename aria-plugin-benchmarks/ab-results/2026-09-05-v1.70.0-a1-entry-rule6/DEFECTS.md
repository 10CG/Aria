# 缺陷清单 — Rule #6 AB (母 Spec a1-entry-claim-duplicate-work-guard → v1.70.0)

> 本次 AB 过程中由 grader 与主控实测发现。**按去处分三类**, 每条带证据。
> ⚠️ 这些**不是**本次 AB 的结论瑕疵, 而是 AB 的**副产品发现**。核心结论见 `SCORES.md` 与各套件 `RESULT.md`。

## A. 套件断言缺陷 (aria-plugin, 与 #117 / #127 同族)

按危害排序:

| # | 形态 | 实例 | 危害 |
|---|---|---|---|
| A1 | **恒假 · 惩罚正确行为** | `state-scanner` eval 5 **A4**: 要求「**不**执行 git fetch, 改读 FETCH_HEAD age」, 但现行设计 Phase 0.5 `remote_refresh` **强制** fetch 8 leg 且 `remote_refs_age` 已标 **DEPRECATED** (`sync-detection.md:71,73,186`) | **反向激励** —— 技能做对了反而扣分, 会诱导改回错的 |
| A2 | 恒真 | `state-scanner` eval 1 三条 (`include Git status` / `provide workflow recommendation` / `use structured format`) | 假绿: 即使新版把 Layer L 段写错、甚至推 claim 到生产 ref, 三条照样全绿 |
| A3 | 夹具永不触发 | eval 5 **A5** (四级回落链, `remote_commit_source=local_ref` 3/3) · **A6** (fail-soft, `errors[]=[]`) · eval 7 **A7** (`open_blocker_issues` 前件恒假, 74 条语料只有 1 个 label) | 占位, 零信息 |
| A4 | 推论式 | `spec-drafter` eval 3 断言 3 是断言 2 的推论 (满足 `` `none` `` 即自动无链接形) | 冗余, 虚增分母 |
| A5 | grep 面宽于所指缺陷 | `spec-drafter` eval 3 断言 5 字面禁全文出现「关联 Issue」, 但 `SKILL.md:354` 明文允许读取侧 alias | **会误判解释更深的臂为 fail** |
| A6 | 只测「做没做」不测「对不对」 | `state-scanner` eval 3 三条全是「有没有做核对」。实测: with 找出真不一致 (root `VERSION:25` standards **v2.2.3** vs `standards/openspec/project.md:3` **2.2.2**), old 说「全部一致」—— **没有一条断言能区分** | 放过真实错误 |
| A7 | 结构性零区分度 | `spec-drafter` eval 3 全部 5 条: 本 cycle diff 59+/1− **没有一行触及 `Linked Issue`**, baseline `SKILL.md:344-354` 已逐字含五条判据 | 5/5 vs 5/5 是构造上注定, 不该计入 delta 分母 |
| A8 | 「包含」型断言近乎恒真 | `phase-a-planner` eval 4「告警须含五要素」—— 字面值本就在 prompt 里, 谓词是「包含」而非「克制」 | 可靠照抄 prompt 通过 |
| A9 | 尺子在断言外 | `branch-manager` eval 1 断言 1 没写期望字符串本体 | 判定依赖 grader 自行构造标尺 |
| A10 | **信号在输出里, 只差一条断言** | `branch-manager`: old 臂把 `<carry-id>` 自行取值成 `TASK-001-user-auth` 落进可执行命令; with 臂停下来索取输入 (`blocking_input`) —— **正是本轮改动的目标行为差异, 两条断言都没测** | 白白丢掉可测的区分点 (grader 已给可证伪补充措辞) |
| A11 | 断言与实现漂移 | `state-scanner` eval 3 **A2** (CHANGELOG 日期作参照源): root README 无 collector 认得的日期行 (`readme.root.version = null`), 日期项永远无数据可报 | 恒假 |

### ⚠️ A1 的三个实例 — 断言给**错误行为**打高分 (本次最重发现)

| 实例 | 谁被罚 / 谁被奖 |
|---|---|
| `state-scanner` eval 5 A4 | 按现行设计正确 fetch 的臂**扣分**; 若改回已 DEPRECATED 的 FETCH_HEAD age 读法反而得分 |
| **`phase-d-closer` eval 1** | **拒绝在输入缺失时虚构进度记录的臂得 0/3**; 用占位 `TASK-001~006` / `stateToken: <recompute>` 编出记录并自评 `upm_updated: true` 的臂**得 3/3**。grader 判语: 三条断言「**方向上奖励虚构**」 |
| **`phase-b-developer` eval 2** | **拒绝拿别的套件顶替验证 (「那是假绿」) 的臂丢两分**; 换个任务跑通的臂满分。**按 Aria 自己的反假绿原则, 被罚的那个可辩护** |
| `phase-a-planner` eval 1 A4 | 在 `on_audit_fail: 阻塞进入 A.2` 的情况下**闯闸照跑**的臂照样满分 —— 断言结构上**奖励闯闸** |

⇒ 这一类不是「没用」, 是**反向激励**: 照着分数优化会把技能改坏。**开单时应列为最高优先级。**

### B8 (补) — 单侧且承重的语料污染, 首次出现

`phase-b-developer` eval 2: **仅 `with_skill`** 引用 `openspec/changes/a1-entry-claim-duplicate-work-guard/` (`detailed-tasks.yaml:281` / `proposal.md` / `10CG/Aria#174` / 31/40 / SC-15), 且**它的满分正建立在从该 Spec 里挑替身任务**上。`old_skill` 该目录零命中。⇒ 干净语料下分差很可能塌成 1:1, **该 3:1 不得计为区分力**。

此前所有 grader 报的都是**对称**泄漏 (两臂同经 handoff, 不产生偏置)。这是唯一一例**非对称且承重**的, 推翻了「本次无单侧污染」的早期表述。

**类级结论**: 11 个回归 eval 共 **65 条断言**, 机械粗筛「含否定 / 字面约束 / 具体数值」的数量 = **0**。只有 eval 12 (5/5) 与新建的 eval 13 (4/6) 有真牙齿。
⇒ **回归面未被有效测试**。「回归臂 60/75 = 60/75」只能读作「没检出」, **不能**读作「已验证无回归」。

## B. 评测台缺陷 (aria-plugin-benchmarks / AB_TEST_OPERATIONS.md)

| # | 缺陷 | 证据 |
|---|---|---|
| B1 | **并发写竞争** — `scan.py` 用 `Path.write_text` 非原子写 ~630KB 到固定路径 `.aria/state-snapshot.json`, 20+ 并发臂互相截断 | 本次加隔离条款 (改写各臂 `outputs/`) 后零损害; 未加之前是运气 |
| B2 | **单个臂能吃光全局 subagent 配额** | `phase-a-planner` eval 1 的 with 臂真跑了 post_spec 审计 3 轮 × 5 席, **自己撞 20 上限**, 第 4 轮起不来 (45 分钟 / 23.7 万 token); old 臂 65 分钟 / 40.6 万 token / 149 工具调用 |
| B3 | **语料泄漏第三通道: 快照自身** | `.aria/state-snapshot.json:2654` 的 `openspec.raw_status` **内嵌 proposal 的 Status 行** (`post_spec R1–R6 已收敛`), 而读快照是 Step 0 **硬性要求** ⇒ 躲不开 |
| B4 | **语料泄漏第二通道: `docs/handoff/`** | SKILL.md 强制读最新 handoff, 而该 handoff 是本 Spec 的高保真摘要。两 grader 独立把 TASK-035/036/038 / `1.70.0` / `8.1→8.4→8.2` / 六套件名逐串溯源到 handoff 行号 | 
| B5 | **真仓是活的, 结果不可复现** | 跑的过程中 `origin/master` 从 `c27826e` 动到 `7b64262` (分支从落后 16 变 17); 两臂甚至跑在不同 scan generation (107 vs 108) |
| B6 | **AB 目录名自带主题词** | `ab-results/2026-09-05-v1.70.0-a1-entry-rule6/` 与在制分支名 `feature/a1-entry-...` 会被实跑 git 探查的臂写进回答 —— 对会翻 `openspec/changes/` 的 eval 是现成污染路径 |
| B7 | **手册清理步骤会连真 claim 一起抹掉** | `AB_TEST_OPERATIONS.md:228` 强制 `+` 强制 fetch; AB 会话全程 `NO_PUSH=1` ⇒ 期间任何真实 heartbeat/acquire 只落本地, 被该步骤一并丢弃 (已开 aria-plugin#169 评论) |

## C. 仓库真实缺陷 (由评测臂顺带挖出, 与本次 AB 无关)

| # | 缺陷 | 证据 |
|---|---|---|
| C1 | **`aria/README.md` skill 名册漏两个** | 数量对 (42) 但列表只有 40 条 —— `issue-triage` (2026-05-13) 与 `session-closer` (2026-06-25) **在 README 里根本不存在**; **无任何机械检查覆盖名册** (readme collector 只正则匹配版本行) ⇒ 漂移活过三个月绿灯 |
| C2 | **`issue_scan.open_count` 静默截断, 量级远超已记** | 快照报 **47**, API 实测 **74** (Aria 20/26 · aria-plugin 20/41 · orchestrator 2/2 · standards 5/5), 吞 **27 条 / 36%**。被丢的恰含 `aria-plugin#110/#135/#107/#109/#117`、`Aria#136`(secret 泄漏)。降序取前 20 ⇒ **老问题被系统性隐藏**。grader 用 forgejo API 做 number 级差集复核, **无一虚构** |
| C3 | **`📝 README 同步状态` 区块实际输出率 ~1/7** | 七样本 (with 0/4 · old 1/4)。`output-formats.md` 规定它是独立区块, 而 `SKILL.md` 输出清单把它降级为「条件子项: 仅相关时显示」—— 两文冲突 |
| C4 | **standards 版本号两处不一致** | root `VERSION:25` 写 **v2.2.3** vs `standards/openspec/project.md:3` 写 **2.2.2**。`version-management.md §5.1` 记了「待 owner 裁定」但**无机械检查守它** |
| C5 | **`.aria/config.json` 的 `coordination` 是嵌套键 —— 读法陷阱** | 它在 `state_scanner` 下。用顶层 `json.load(...).get('coordination')` 读得 `None` ⇒ 误判「协调闸门未启用」, **与事实相反且静默** |
| C6 | `aria/skills/session-closeout/` 空的未跟踪残留目录 | 解释 43 目录 vs 42 SKILL.md |
| C7 | **`state_scanner.sync_check.*` 是死配置** | grep `scripts/**/*.py` 只命中 `collectors/multi_remote.py` 两处注释; `sync.py` 只读 `state_scanner.multi_remote.enabled` |
| C8 | **`handoff` frontmatter status 从不收口** | 实测 106 条 track 仍报 `active` (Aria#182 记的是 31 条, 已过期低估) |

## D. 主控 (我) 的过程缺陷 — 照记

| # | 事 | 判据硬化 |
|---|---|---|
| D1 | **n=1 就下「回归」结论, 一天两次** (eval 2 / eval 3), 第二次是在已写下「单次不足以定性」之后 | **任何跨臂差异, n≥3 之前一律标「未定」, 不进结论段、不报 owner** |
| D2 | **重复派发 4 个臂** (SS e3 with/old · e5 old · BM e1 old), 造成 2 份 grading 评了已被覆盖的答卷 | 派发前必查 `DONE_ARMS.txt`; 已隔离为 `grading.STALE.json` + `STALE_NOTE.md` |
| D3 | 一开始允许臂写仓内固定路径 `.aria/state-snapshot.json` | 见 B1, 已加隔离条款 |

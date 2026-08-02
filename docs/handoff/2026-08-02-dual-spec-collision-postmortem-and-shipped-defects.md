---
track-id: phase-c-integrator-ci-path-coverage
owner-container: aria-runner-bot/023236f2
phase: post-mortem
status: done
updated-at: 2026-08-02T03:20:00Z
---

# Session Handoff (2026-08-02) — 双 Spec 碰撞事后勘误 + ship 版本三个 live 缺陷

> 会话维度增量。承接 [2026-07-27 本轨 handoff](./2026-07-27-issue122-phase-a-dual-gate-convergence.md)(该轨产物已 **superseded**)。
> **本段主线 = 一次净产出为负的循环, 与它挽回的部分。** 本轨对 #122 做了三轮 Spec 修订 (A1/A2/A3) + 两轮闸门 (R5 5 席 / R6 1 席新眼睛), 而并发轨在同期**走完十步循环 ship 了 v1.65.0**。修订对象在 07-31 就已归档。**挽回的部分**: 那两轮审计的 finding 拿去实跑 ship 的代码, **3/3 全部命中**, 其中一条是 enabled 闸门上的 **fail-OPEN 误放行**。

## §0 入口 (新 session 优先读)

- **当前态**: 主仓 `origin=github=b93ed25` + 本轨 8 commit (未推); aria 子模块 `52d6f22` (v1.65.1); 工作区仅 `aria-orchestrator` (有意排除, #165 形状)。
- **本段产出**: 3 个 issue ([#124](https://forgejo.10cg.pub/10CG/aria-plugin/issues/124) / [#125](https://forgejo.10cg.pub/10CG/aria-plugin/issues/125) / [#126](https://forgejo.10cg.pub/10CG/aria-plugin/issues/126)) + 自包含复现脚本 + 18 份审计报告 + 修法设计存档。
- **下一步**: 见 §6。

## §1 事实认定 —— 谁 ship 了, 我做了什么

| | 并发轨 `simonfishgit` | 本轨 `aria-runner-bot/023236f2` |
|---|---|---|
| Spec | `phase-c-gate-path-coverage-not-applicable` | `phase-c-integrator-ci-path-coverage` |
| 结局 | **07-31 ship v1.65.0 + 归档** (含 Rule #6 三臂 AB) | **superseded, 从未进 Phase B** |
| 07-28~31 在做 | 实现 → TDD (62→97 测试) → AB → 合并 → 归档 | 对**对方的 Spec** 做 A1/A2/A3 修订 + 跑 R5/R6 |

owner 07-30 裁定「以对方 Spec 为准 + 并入本轨发现」时,**对方已在实现中**;07-31 对方 ship 时,本轨正在写 A3。双方全程互不知情。

## §2 挽回的部分 —— ship 的代码里有三个 live 缺陷 (实跑 3/3)

R5/R6 的 finding 不是纸面推演。拿去跑 ship 的 `path_coverage.py`:

| # | 缺陷 | 方向 | issue |
|---|---|---|---|
| 1 | 非 ASCII 变更路径 → 误判 `not_applicable` | 🔴 **fail-OPEN (误放行)** | #124 |
| 2 | 同缩进块序列的 `paths:` 解析不出 → 恒 covered | 🟠 恒 wait (#122 对该类仓未生效) | #125 |
| 3 | 内部异常上报为 `git-diff-failed` | 🟠 误诊 | #126 |

**缺陷 1 的实证** (同 workflow、同 `paths: 'skills/**'`):

```
ASCII    skills/issue-triage/x.py → git 输出 skills/issue-triage/x.py          → covered        ✅
非 ASCII skills/测试/x.py          → git 输出 "skills/\346\265\213\350\257\225/x.py" → not_applicable ❌
```

根因 `path_coverage.py:403-407` 缺 `-z`,`core.quotePath`(git 默认 true)八进制转义 ⇒ 与 glob 恒不匹配。**这是 Rule #8 enabled 闸门上唯一会导致误放行的缺陷** —— 其余所有已知缺陷的坏结果都只是「多等 1800s」。

**缺陷 3 逐字命中 R6 的预测**: `:388` 写着 `f"git-diff-failed: internal error {exc!r}"`。

**C-2 (我最担心的另一个 fail-OPEN) 不在** —— ship 的实现独立到达了 `paths: <非列表标量> → uncertain` 兜底,与 A3 的 (2c) 同解。

复现: `python3 .aria/repro/repro-aria-plugin-124-125-126.py aria/skills/phase-c-integrator/scripts/path_coverage.py`(stdlib-only,自建临时仓,不触碰现有仓库;对 v1.65.1 实跑 3/3)。

## §3 rebase 的处置决定 (需知悉)

原 9 commit → **7 commit**,两处刻意处置:

1. **A2 (`925fd90`) / A3 (`32a887a`) 已 skip** —— 两者只改了 `openspec/changes/phase-c-gate-path-coverage-not-applicable/proposal.md`,而该路径在 rebase 后是 `openspec/archive/2026-07-31-.../`。**归档 Spec 不能改**:它是「实际 ship 的是什么」的历史记录,写进 A1/A2/A3 会让后人以为实现是照着 D12/D13/D14/D15/D16 建的,而事实不是。已核验 `git diff origin/master -- openspec/archive/` 为空。
2. **A3 全文存为 `REMEDIATION-DESIGN-A3.md`** —— 落在 superseded 轨自己的目录里,头部明确标注「不是待实施 Spec」,并逐条指向它对 #124/#125/#126 的参考价值。**同时标注了 (2b) 位置∧形态判据属「未命中的防御」**(它防的 C-2 在 ship 版本里不存在),避免后人照搬无用条款。

`f829aee` 对归档文件的那部分改动也已丢弃,只保留它对本轨自己目录的改动。

## §4 关键教训

**1. 「每次实质动作前重扫」这条纪律,我自己没执行 —— 而且是在提出它之后。**

07-30 我起草 `a1-entry-claim-duplicate-work-guard`,论点是「闸门审产物质量,不审产物是否该存在」,方案是把已 ship 的 `phase1_gate --linked-issue` claim 前移到 A.1。**然后 07-31 起草 A3 前没有 fetch,08-02 才发现。** 这是 `feedback_concurrent_duplicate_audit_fetch_before_start` 的**第五次**实证,前四次的处置都是「记住要做」。

⇒ 该 Spec 现在有了最强的一条论据:**提出这条纪律的人,在提出后的第二天违反了它**。纪律不够,必须机械化。

**2. 「审计发现」与「Spec 修订」的价值可分离 —— 前者独立于载体存活。**

A1/A2/A3 三轮修订(约 500 行 Spec 文本)全部作废,但产生它们的 R5/R6 审计 finding **100% 存活**,因为 finding 描述的是**实现层的缺陷**,不是 Spec 文本的缺陷。⇒ 审计报告写 finding 时,应尽量表述为「实现若这样写会怎样」而非「Spec 这段话该怎么改」—— 前者跨载体可迁移,后者随载体作废。

**3. rebase 撞上「已归档」是一个信号,不是一个障碍。**

冲突提示 `openspec/archive/...` 时,正确反应不是解冲突,而是意识到**修订对象已经完成生命周期**。本次若机械地解冲突把 A1/A2/A3 合进归档,会污染历史记录且无人察觉。

## §5 多维度同步状态 (机械核验)

- **git**: 主仓本轨 8 commit 未推 (`origin=github=b93ed25`); aria `52d6f22` (v1.65.1, 已 ff); standards `f986a60` (detached); aria-orchestrator `92acce5` (feature 分支, 只读未动)。
- **custom checks**: 8/8 绿 (badge=1.64.1 → 需注意 aria 已到 v1.65.1, 下次扫描时 badge check 可能变化)。
- **openspec**: 活跃 9 (含本轨 superseded 的 1 个 + 未裁的 `a1-entry-claim-duplicate-work-guard`); 归档 131; `design_deferred` 3 项。
- **issue**: aria-plugin open 增 3 (#124/#125/#126); 本轨未 triage 的承前项: #117 / #120 / #123 + Aria #168/#169。

## §6 Next session 入口 + 优先级

1. 🔴🔴 **凭据轮换 — hard cap 2026-08-02 就是今天**: `FORGEJO_TOKEN` / `NEXUS_API_TOKEN` / `CF_ACCESS_CLIENT_SECRET`。第九次 surface,owner 亲自操作项,**逾期无补救**。
2. 🔴 **#124 (fail-OPEN) 优先修** —— 它在 enabled 闸门上会误放行。修法与红窗设计见 issue 正文 + `REMEDIATION-DESIGN-A3.md` 的 D14/SC-29。
3. **推送本轨 8 commit** (owner 未授权推,本段全程未推)。推时走本地双推 + 逐个 `ls-remote` 核验 (CLAUDE.md 两条硬约束)。
4. **`a1-entry-claim-duplicate-work-guard` 的 post_spec 从未裁过** —— 该 Spec 07-30 起草至今,闸门 enabled,owner 未裁是否跑。它现在有第五次实证支撑。
5. #125 / #126 修复; 未 triage: #117 / #120 / #123 / Aria #168 / #169。

## §7 流程判断留痕 (Rule #10, 请复议)

- **三个 issue 是 AI 判断为「值得报」后主动开的**,owner 只说了「[1] 开 issue 报这三条缺陷」—— 缺陷条数、拆几个 issue、各自定级 (fail-OPEN / 恒 wait / 误诊) 均为 AI 判断,**请复议定级是否恰当**。
- **A2/A3 的 skip 是 AI 判断**,依据是「归档 Spec 是历史记录不可改」。这不在 owner 的 [2] 指令文本内,属 AI 对「rebase 怎么做」的技术判断。若 owner 认为 A1/A2/A3 应以别的形式保留,可从 reflog 取回 (`925fd90` / `32a887a`)。
- **本段未推任何 commit** —— 推共享 master 属外向动作,owner 未明示授权 (memory `feedback_sync_instruction_not_push_authorization`)。

## Cross-references

- 本轨前一段: [2026-07-27](./2026-07-27-issue122-phase-a-dual-gate-convergence.md) (⛔ superseded)
- 并发轨 ship 记录: [2026-08-01](./2026-08-01-triage-fix-train-and-122-not-applicable-ship.md)
- 归并分析: `openspec/changes/phase-c-integrator-ci-path-coverage/MERGE-ANALYSIS.md`
- 修法设计存档: `openspec/changes/phase-c-integrator-ci-path-coverage/REMEDIATION-DESIGN-A3.md`
- 复现脚本: `.aria/repro/repro-aria-plugin-124-125-126.py`
- 审计轨迹: `.aria/audit-reports/post_spec-R{5,6}-*-phase-c-gate-path-coverage-*.md`
- ship 的实现 (归档 Spec): `openspec/archive/2026-07-31-phase-c-gate-path-coverage-not-applicable/`

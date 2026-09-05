---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-09-05T14:46:16.555Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## R1 处置核对

逐条对我 R1 报告 (`.aria/audit-reports/post_spec-R1-2026-09-05T140104-375Z-owner-container-identity-key-and-collision-parser-qa-engineer.md`) 的 1C/3M/3m 在 v2 (`d23f103`) 是否真闭合, 实读 + 实跑核对:

- **Critical (`test_both_latest_active_still_reports_self_multi_container` 零回归不可达)**: **未闭合, 重开** (证据见下文 Critical 1)。R1 聚合报告 R1-C1 处置栏写「等价类规则下该对仍 self_multi_container (实测)」——本轮对该测试**自身的隔离 fixture** (非全量真实语料) 重跑三步判定逻辑, 结果翻转为 `cross_owner`, 与聚合报告的「实测」结论矛盾 (该「实测」显然是对全量冻结语料跑的, 不是对这条 pytest 自己的 `_build_repo` 隔离数据跑的)。
- **Major §2.3.7 编号冲突**: **已闭合**。实读 `standards/conventions/session-handoff.md` 章节列表 (`grep -n "^### 2\.3\."`), §2.3.7 仍是 #137 enforcement 未动, v2 proposal D2/SC-5 全部改引 §2.3.9 (真空档), References 段落也同步改引。
- **Major SC-6 冻结快照未版本控制**: **已闭合**。`git log --oneline -- .aria/repro/handoff-tracks-frozen-2026-09-05.json` 命中提交 `d23f103`; `git check-ignore` 对该路径退出码 1 (未被忽略); 内容 `frozen_from`/`generated_at`/996 行 tracks 与 proposal 数字一致, 且不再随 `.aria/state-snapshot.json` 漂移。
- **Major cross_owner 正控测试全虚构三段式**: **已闭合**。SC-2 新增「端到端 (collector 夹具→dedupe→classify) 真实两段式两人两机 → cross_owner」条款, 覆盖了 R1 指出的 0/154 真实两段式覆盖缺口。
- **minor SC-2 只覆盖 2-owner**: **已闭合**。SC-2 新增「≥3 owner 的 uuid 容器 → advisory `owners[]` 长度 3」。
- **minor legacy 行不参与 advisory 无专属断言**: **已闭合**。SC-2 新增「legacy 行不产生 advisory」显式断言。
- **minor T1「solo」1-part 断言遗漏**: **已闭合**。T1 文本现明写「2-part **与 1-part (`"solo"`)**」。
- **decision Rule #6 豁免判据自评**: 非缺陷, 维持成立, 不适用闭合/未闭合。

**三态计数**: Critical 0 closed / 1 reopened / 0 not-addressed；Major 3 closed / 0 reopened / 0 not-addressed；Minor 3 closed / 0 reopened / 0 not-addressed。

## 审计结论

### type: issue / severity: critical / category: testing / scope: SC-7 零回归 — `test_both_latest_active_still_reports_self_multi_container` 隔离 fixture 下仍会翻转

**summary**: v2 的等价类只在「同一次 collector 扫描的全语料」范围内建并查集; 该测试自建的隔离临时仓库里 aria-runner-bot 与 simonfish 从未在同一 uuid 容器上共现, 三步判定下必然翻转为 `cross_owner`, T4「断言加等价类前提」未具体到「往 fixture 里插入共现行」, SC-7 承诺的零回归在当前 Task 文本下仍不可达。

**evidence**: 实读 `aria/skills/state-scanner/tests/test_handoff_multibranch_collision_dedupe.py:208-241` (`_build_repo`): 每次调用都新建一个**仅含传入 `files` 列表**的独立临时 git 仓库, 不引入任何额外分支/track/owner 数据。实读同文件 `:299-341` (`TestSelfMultiContainerRealCollisionSurvivesDedupe.test_both_latest_active_still_reports_self_multi_container`): fixture 仅有 6 行, `aria-runner-bot` 只出现在容器 `023236f2` 上, `simonfish` 只出现在容器 `bfe8285d` 上——两者在这个隔离语料里**从未共现**。按 proposal D1 步骤 3 原文「对全语料 (collector 扫到的全部非 legacy 行) 建并查集」, 「全语料」的范围就是**本次 `collect_handoff_multibranch` 调用扫到的行**, 不是外部持久化的历史语料。实跑复现 (在 `/tmp/.../scratchpad` 脚本里精确复刻这 6 行, 按 proposal 文本实现两段式解析 + `^[0-9a-f]{8}$` 身份键 + 全语料并查集): `container_owners = {'023236f2': {'aria-runner-bot'}, 'bfe8285d': {'simonfish'}}` — 两个单例类, 无合并; 该测试要断言的两个 identity_key (`023236f2` / `bfe8285d`) 上的 owner 类分别是 `{aria-runner-bot}` / `{simonfish}`, 两个不同类 → 判定 `cross_owner`, 与 pin 死的 `"self_multi_container"` (`:338-341`) 矛盾。对照: 用**冻结全量语料** (`.aria/repro/handoff-tracks-frozen-2026-09-05.json`, 996 行) 重建同一算法, `container_owners['023236f2'] = {'aria-runner-bot','simonfish'}` 且 `container_owners['bfe8285d'] = {'aria-runner-bot','simonfish'}` (两容器都真实共现过), 这才是聚合报告「等价类规则下该对仍 self_multi_container (实测)」结论的真实依据——但这依据来自全量语料, 不是这条 pytest 自己的隔离数据。T4 原文「断言加等价类前提」没有具体到「往 `files` 列表里补两行 (如 `aria-runner-bot/bfe8285d` 或 `simonfish/023236f2` 的历史行) 以在该测试自身的语料内建立共现」——若 B.2 按字面「只加一句 docstring 前提说明」实现, 这条 pin 死的既有测试会红, 且不会有任何 Task/SC 提前预判到。

### type: issue / severity: major / category: architecture / scope: 等价类并查集对「同一物理容器被两个真人交接使用」场景引入结构性假阴性

**summary**: D1 步骤 3 的并查集覆盖全部历史 (含 done/abandoned) 且永久不可逆; 若某 uuid 容器曾被两个真人先后使用过 (设备交接), 两人从此被永久并入同一等价类, 之后任何一方在各自独立机器上发生的真实撞车都会被误判为 `self_multi_container`。此风险未见于 D-1/D-2/D-3/Impact/Risk/非目标 任一处。

**evidence**: 用 proposal 文本逐字实现的三步算法构造反例: 语料 `[erin/eeeeeeee(done), frank/eeeeeeee(done), erin/aaaaaaaa(done)]` (容器 `eeeeeeee` 曾被 erin、frank 两个真人先后使用, 均为已结束的历史记录), 并查集得到 `{'frank': 'erin', 'erin': 'erin'}` (合并为一类)。随后模拟一次**真实**的两人两机撞车: `erin/aaaaaaaa` (erin 自己专属机器) 与 `frank/eeeeeeee` (frank 常用的共享机) 同时 active——按等价类算法两者的 owner 类都解析为 `erin`, 判定输出 `self_multi_container`, 是一次真实的两人撞车被静默吞掉的假阴性 (脚本输出 `classes seen: {'erin'}` → `self_multi_container (FALSE NEGATIVE)`)。该合并是**全历史 (含 done/abandoned) + 永久不可逆**的 (proposal 步骤 3 原文「对全语料...建并查集」未按 status 过滤, 也未设时间衰减), 与 D-1(a) 后果句「从未共现的两个串仍会 🔴 一次, 直到该机器上出现共现」描述的是相反方向的风险 (那条讲的是「未合并时误报一次」, 这里是「一旦合并就永久压制真实撞车, 无解除机制」)。Aria 的多终端协调场景本身就包含「容器复用/设备交接」的现实可能 (proposal §Why 自己举的 `bfe8285d`/`023236f2` 就是同一容器换 git 身份的真实案例, 只是方向恰好是「同一人换身份」而非「换人」), 但 D-1/D-2/D-3 三个决策点、Impact/Risk 表、非目标段落均未讨论「换人」这一支线, SC 集合里也没有一条对此建反例断言。

### type: issue / severity: major / category: testing / scope: SC-4 身份键谓词缺 8 位非十六进制主机名的对抗 fixture

**summary**: SC-4「主机名容器不折叠」分支目前只用 `dev-claude` / `box` 等非 8 字符字符串验证; 一个把身份键谓词误写成 `len(container) == 8` (而非规范文本 `^[0-9a-f]{8}$`) 的实现, 在冻结语料与全部 Task 列出的 fixture 上都会与正确实现输出完全一致, 无法被现有 SC/实验表分辨。

**evidence**: 实读 §What D1 步骤 2 原文: 「container 段匹配 `^[0-9a-f]{8}$`」——即字符集 + 长度双重约束。实读冻结语料 (`.aria/repro/handoff-tracks-frozen-2026-09-05.json`) 与既有测试里出现的全部主机名容器: `dev-claude` (10 字符) / `dev-claude2` (11 字符) / `box` / `box-A` 等, **没有一个恰好 8 字符**; 全部 uuid 容器 (`bfe8285d`/`023236f2`/`f9c6e8cd`) 天然是 8 位十六进制, 用 `secrets.token_hex(4)` 生成 (`lib/identity.py::_generate_uuid`), 恒为十六进制。因此 `len(container) == 8` 与 `^[0-9a-f]{8}$` 两种谓词在 proposal 现有全部数据 (冻结语料 + Tasks 点名的既有/新增测试) 上**行为完全等价**, 无一条数据能分辨二者。若实现按前者写 (更容易在 B.2 顺手写出的捷径), 一个恰好 8 字符但非十六进制的主机名 (如 `mymachin`) 会被误判为「uuid 容器」, 从而 (a) 该主机名的 owner 段不再参与身份键与 dedupe 键 (b) 该主机名一旦被两台不同物理机器巧合共用 (主机名本身跨机不唯一, 正是 proposal §What 步骤 2 自己强调的前提), 两台机器的行会被 dedupe 静默折叠成一行, 真实的跨机撞车信号直接从输出中消失 (不是误判类别, 是数据丢失)。SC-4/T4/实验表均未包含这一对抗 fixture。

## Verdict

FAIL (1 Critical / 2 Major / 0 minor)

## Vote

REVISE

## 轮次记录

Round 2 (qa-engineer, convergence mode, 换镜头「构造坏实现打 SC」): 对 R1 我方 1C/3M/3m 逐条实读+实跑核对——3M/3m 全部闭合, 1C 名义闭合但重开 (等价类「实测」依据的是全量冻结语料而非既有测试自身的隔离 fixture, 精确复现 `test_both_latest_active_still_reports_self_multi_container` 的 6 行数据后判定翻转为 `cross_owner`)。本轮新增两条 Major: (1) 等价类并查集全历史永久合并, 对「同一物理容器被两个真人先后使用」构造出真实反例, 会把之后任何一方独立发生的真撞车压成假阴性, 决策点/Impact/非目标均未覆盖; (2) 身份键谓词的字符集约束 (`^[0-9a-f]{8}$` vs `len==8`) 在当前全部数据上不可分辨, 缺一条 8 位非十六进制主机名的对抗 fixture。核心方法论: 冻结语料 (`.aria/repro/handoff-tracks-frozen-2026-09-05.json`) 上的生产路径实验表 (A/B/D 三变体) 逐一实跑复现, 数字与 proposal 完全吻合 (996→121 self_multi_container / 996→122 cross_owner 误报 / 996→122 self_multi_container), 证明 v2 的核心设计思路在真实语料上是站得住的——问题集中在「隔离单元测试 fixture 的语料范围窄于生产扫描范围」与「等价类无衰减/无按人区分机制」这两个 v2 独有的新风险面, 不是重复 R1 的旧问题。fixture PII 核查: 996 行涉及的 owner 串 (`simonfish`/`simonfishgit`/`aria-runner-bot`) 已在 `docs/handoff/*.md` 全仓可见并已入库, T6 复制进测试 fixture 不构成新增披露。

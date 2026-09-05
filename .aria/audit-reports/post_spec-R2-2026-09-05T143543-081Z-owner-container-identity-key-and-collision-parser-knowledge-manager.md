---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-05T14:40:00.000Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## R1 处置核对

R1 本席 5 条 finding 在 v2 (commit `d23f103`) 逐条核对如下 (均实读 v2 proposal.md 对应行 + 相关代码/规范文件):

| R1 编号 | 内容一句话 | v2 处置状态 | 证据 |
|---|---|---|---|
| **C1** (critical) | `§2.3.7`「新增」与既有 #137/#138 占用小节冲突 | **CLOSED** | proposal.md:42 已改「新增 §2.3.9」并注明「§2.3.7 = #137 frontmatter enforcement, §2.3.8 = carry-id schema, 均已占用; 真空档 §2.3.9」; SC-5 (proposal.md:113) 补「§2.3.7/§2.3.8 原文不变 (diff 零)」回归锁; `grep -n "^### 2\." standards/conventions/session-handoff.md` 复核仍为 2.3.1–2.3.8 连续无空档, §2.3.9 确为真空档 |
| **M2** (major) | Impact 表称判据反转「只改判据措辞不改字段」, 低估行为变更 | **CLOSED** | proposal.md:41 §2.3.5 段落首句已改「**实质变更, 不是措辞变更**」; Impact 表 Risk (1) (proposal.md:89) 明确写「§2.3.5 判据实质变更 + dedupe 键变更 ⇒ 采用方看板输出改变」并要求「变更说明写进 standards 与 aria CHANGELOG」 |
| **M3** (major) | `layer-l-integration.md`/`RECOMMENDATION_RULES.md` 消费措辞未被 Tasks 覆盖, 无回归断言 | **PARTIAL** | D4/T7/SC-9 (proposal.md:49-50,103,117) 已补三处消费文档同步任务与 rule 1.54 触发面锁定测试, 覆盖原始两处; 但本轮新发现 (1) 第三处引用 `advanced-rules.md:578` 路径本身有误 (2) 存在未被 D4/T7/SC-9 列入的第四处真实消费面 `phase-d-closer/scripts/fetch_gate.py` — 详见下方 Finding A/B |
| **m** (minor, Finding4) | 「9 种 owner-container 串」实测为 10 种 | **CLOSED** | proposal.md:19 已改「10 种 owner-container 串, 对应 5 个 container 标识」, 与 R1 实测数字一致 |
| **m** (minor, Finding5) | D-2 选项 (a) 只列收益未列代价, 与 (b)/(c) 不对称 | **CLOSED** | proposal.md:74 (a) 已补「**代价**: commit 署名失去「哪位操作者在场」的可追溯性...若将来出现第二位人类操作者, 需要第二个 bot 身份或退回 (b)」, 三个选项现均为收益+代价对称结构 |

## 审计结论

### Finding A

- `type`: issue
- `severity`: major
- `category`: documentation
- `scope`: `openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md:50,103,133` (D4 / T7 / References 三处引用) 对 `advanced-rules.md:578` 的路径
- `summary`: proposal 三处均写 `references/advanced-rules.md:578`, 但该文件实际路径是 `aria/skills/state-scanner/references/rules/advanced-rules.md` (多一层 `rules/` 子目录)。SC-9 也未把 advanced-rules.md 纳入 grep 断言范围 (只锁 layer-l-integration.md 与 RECOMMENDATION_RULES.md 两处), T7 对该文件的修改因此无回归锁。
- `evidence`: `find aria -iname "advanced-rules.md"` 实测唯一命中 `aria/skills/state-scanner/references/rules/advanced-rules.md` (625 行), 不存在 `aria/skills/state-scanner/references/advanced-rules.md`；该文件第 578 行原文 `- "判定不依赖\"谁\" (collision helper 已按 owner+container 归类, 同 owner/container 全相同→none 不触发)"` 内容与 proposal 描述的「过时注释」吻合, 仅路径缺 `rules/` 前缀; proposal.md:117 SC-9 原文「`layer-l-integration.md:73` 与 `RECOMMENDATION_RULES.md` 的取值措辞与 §2.3.5 三行一致 (grep 断言)」未提及 advanced-rules.md。

### Finding B

- `type`: issue
- `severity`: major
- `category`: documentation
- `scope`: `aria/skills/phase-d-closer/scripts/fetch_gate.py:178,187-188,251-256` — D4/T7/SC-9 消费文档同步清单未覆盖的第四处消费面
- `summary`: `run_fetch_gate(collision_kind=...)` 把 `collision_kind != "none"` 当触发条件产出 `"advisory"` verdict (与已列的 rule 1.54 `!= none` 判据同一模式), 且 `test_fetch_gate.py:58,96` 硬编码 `"cross_owner"`/`"self_multi_container"` 字面值回归测试; proposal 的 D4「消费文档同步」与全仓 grep 均只列了三处 (`layer-l-integration.md` / `RECOMMENDATION_RULES.md` / `advanced-rules.md`), 未提及此文件, 也未在 T7/SC-9 中要求核实其触发频率变化或改写其测试断言。
- `evidence`: `grep -rn 'collision\.kind\|self_multi_container\|cross_owner' aria/skills/` 命中 `aria/skills/phase-d-closer/scripts/fetch_gate.py:187-188` (docstring: "collision_kind: tracks_multibranch.collision.kind from the snapshot") 与其调用点 `:251` `elif collision_kind != "none": result["verdict"] = "advisory"`；`aria/CHANGELOG.md:1215,1217` 确认该脚本是已 ship 功能 (`concurrent-session-upm-safety #133 TASK-006`, "fetch_gate 11 tests")；`aria/skills/phase-d-closer/tests/test_fetch_gate.py:58,96` 分别用字面值 `collision_kind="cross_owner"` 与 `collision_kind="self_multi_container"` 断言 verdict。本 Spec 让 `cross_owner` 首次在真实数据上可达 (D4 原文语), 该脚本的 advisory 触发频率会与 rule 1.54 同向改变, 但没有任何 Task/SC 点名它。

### Finding C

- `type`: issue
- `severity`: major
- `category`: documentation
- `scope`: `standards/conventions/session-handoff.md` 拟改 §2.3.1 / §2.3.5 (proposal.md:40-41) — `identity_key` 与「owner 等价类」两个术语在规范文本中的定义缺位
- `summary`: D2 拟写入 standards 的 §2.3.5 三行判据表直接使用 `identity_key` 与「owner 等价类」两个术语作为触发条件的主语, 但这两个术语的构造规则 (uuid 正则 `^[0-9a-f]{8}$` 判定分支 / 全语料并查集建类 / 空-unknown owner 不成类) 只写在 proposal 的 D1 (Aria 实现细节, 不进入 standards), §2.3.1 拟改文本只定义了 `<container-id>` = uuid 字段, 未定义 `identity_key` 本身。不读 aria `lib/collision.py` 源码的采用方 (Kairos/SilkNode/nexus) 单靠 §2.3.1/§2.3.5/§2.3.9 三段规范文本, 无法机械推出「同一 identity_key 出现 ≥2 owner 段」这类判据在自己实现里该怎么算。SC-5 (proposal.md:113) 只要求判据文本「含 `identity_key` / 等价类 / `same-identity-multi-owner`」这几个词面出现, 未要求给出定义, 该缺口不会被现有 SC 挡下。
- `evidence`: proposal.md:34-35 (D1 步骤 2/3, `identity_key` 与等价类的完整构造规则) 与 proposal.md:40-41 (D2, 拟写入 standards 的文本) 对照: 后者仅有「`cross-owner` = 同 track ≥2 个 `identity_key` 且 owner 等价类 ≥2」等使用该词的判据句, 无一句定义词本身; `standards/conventions/session-handoff.md:111-121` (现 §2.3.1 字段定义段) 现状同样只定义 `<owner>`/`<container-id>` 两个 frontmatter 字段, 没有第三个派生字段的先例结构可比照。

### Finding D

- `type`: risk
- `severity`: major
- `category`: documentation
- `scope`: proposal.md:42 (D2 新 §2.3.9)「交叉引用 Aether 人机两账号模型的边界」
- `summary`: proposal 只写了「交叉引用」的意图, 未给出落点; 而本仓唯一可核实的落点 `/home/dev/Aether/docs/guides/forgejo-token-map.md` 属于 Aether — 一个独立仓 (非 Aria 的 git submodule), 其内容 (账号名 `simonfish`/`10cg-ci-bot`、token store 结构) 是 10CG Lab 私有基建细节。`standards/` 是跨项目共享子模块 (SilkNode/Kairos/nexus 等采用方消费), 若 §2.3.9 字面引用该本地绝对路径或其账号命名, 会把 standards SOT 与本 Lab 私有基建耦合, 对外部采用方不可达也不适用; 若不给落点, 「交叉引用」在 T5 执行时会退化为一句无锚点的空话, 起不到边界厘清作用。
- `evidence`: `/home/dev/Aether/docs/guides/forgejo-token-map.md:3-4,34-38` 实读确认「Aether 环境下只有两个 forgejo 账号 —— `simonfish`(人) 和 `10cg-ci-bot`(机器)」的两账号模型定义即 proposal 所指内容, 但该文件路径本身、账号名均是 Aether/10CG 私有信息, 未见任何面向外部采用方的公开摘要版本; `grep -rn "两账号\|human.*machine.*account" standards/ 2>/dev/null` 在 standards 子模块内零命中, 即该概念目前完全没有任何跨项目可达的落点。

## Verdict

PASS_WITH_WARNINGS (0 Critical / 4 Major / 0 Minor)

判据: 无 Critical — R1 的三条实质性问题 (C1/M2/M3) 中两条 (C1/M2) 已完整闭合, 第三条 (M3) 部分闭合但未完全兑现「消费文档同步」的完整性承诺, 且本轮新发现两条同类知识链缺口 (路径错误、第四消费面遗漏) 与两条本轮换镜头后才可见的规范自包含性/边界缺口 (identity_key 定义缺位、Aether 交叉引用无落点)。四条 Major 均不阻断 B.1 (不损坏既有共享内容、不产生结构性覆盖), 但都会在 T5/T7 落地时留下「写了但读者/执行者对不上」的缺口, 建议在本轮 rework 一并收口。

## Vote

REVISE

## 轮次记录

- Round 1 (knowledge-manager): FAIL, 1C/2M/2m — 见上表核对, 3/5 条已闭合, 1 条 (M3) 部分闭合。
- Round 2 (knowledge-manager, convergence 模式, 换镜头「规范文本与知识链能否被采用方与 owner 无歧义消费」): PASS_WITH_WARNINGS, 0C/4M/0m。新增 Finding A (advanced-rules.md 路径错误 + SC-9 遗漏该文件)、Finding B (fetch_gate.py 第四消费面未列)、Finding C (`identity_key`/等价类术语在 standards 文本中未定义)、Finding D (Aether 交叉引用无落点且潜在越界)。D-1/D-2/D-3 三决策点后果陈述本轮核对均对称, Level 复议段忠实转述 R1 tech-lead 判据与 owner 指令, 未见 AI 越权代裁。

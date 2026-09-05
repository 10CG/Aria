---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-09-05T14:24:57.727Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 审计结论

### Finding 1

- `type`: issue
- `severity`: critical
- `category`: documentation
- `scope`: `standards/conventions/session-handoff.md §2.3.7` (D2, proposal.md 第 37 行 "新增 §2.3.7「AI runner 提交身份」")
- `summary`: `§2.3.7` 已被 `#137 Frontmatter content enforcement` 占用 (且 `§2.3.8` 也已被 Carry-id schema 占用); proposal 声称"新增"的编号是既有已发布小节, 原样执行会覆盖/编号冲突既有共享子模块内容。
- `evidence`: `standards/conventions/session-handoff.md:204` (`### 2.3.7 Frontmatter content enforcement (#137, aria-plugin v1.43.0+)`) 与 `:217` (`### 2.3.8 结构化 Carry-id schema ...`) 均为既有已 ship 小节 (实读确认, `grep -n "^### 2\." standards/conventions/session-handoff.md` 输出 2.3.1–2.3.8 连续无空档); `openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md:37` 逐字写"新增 §2.3.7「AI runner 提交身份」"。真正可用的下一个空档编号是 `§2.3.9`。若 T5 按 proposal 字面执行, 要么覆盖 `#137` 内容 (5 层 content-enforcement 机制文档消失, 该机制是 SilkNode 08-31 实证驱动的既有 shipped 防护), 要么产生两个 `### 2.3.7` 标题并存的结构性错误 —— 两种结果都会破坏 `standards` 作为跨项目共享子模块 (SilkNode / Kairos / nexus 等采用方) 的 SOT 完整性, 与 proposal 自身在 Impact 表反复强调的"additive, 既有内容不动"承诺直接矛盾。

### Finding 2

- `type`: risk
- `severity`: major
- `category`: architecture
- `scope`: `standards/conventions/session-handoff.md §2.3.5` 判据表既有两行 (D1/D2, proposal.md 第 30/36/72 行)
- `summary`: D1 把判定键从"同 track-id 下 owner 是否 ≥2 种"改为"先按 container 分组, 同 container 视为同一身份"—— 这会反转既有 `cross-owner` 行的触发条件 (同 container 不同 owner 从"触发 cross-owner"变为"不参与 collision"), 而 Impact 表称此为"只改判据措辞不改字段", 低估了对既有采用方的行为影响。
- `evidence`: `standards/conventions/session-handoff.md:178-186` (§2.3.5 现表: `cross-owner` 触发条件 = "同一 track-id 出现 ≥2 个 distinct `<owner>`"; `self-multi-container` = "≥2 个 distinct `<container-id>` 但同 owner")。`lib/collision.py:158-167` (`classify_claims`) 现行实现印证此表: `owners = {c.owner for c in active}; if len(owners) >= 2: return "cross_owner"` —— owner 不同即判 cross_owner, 与 container 是否相同无关。proposal.md 第 30 行 D1: "先按 container 分组; ≥2 个 distinct container 时再看 owner —— owner 全同 → self_multi_container, owner 不同 → cross_owner; **同一 container 无论 owner 段几种, 视为同一身份**, 不参与 collision 计数"。这意味着同一 container 不同 owner 的场景 (即 §Why 描述的 git 身份漂移本身) 将从 cross-owner 语义中被移出, 是对既有 `cross-owner` 判据的**实质改写**, 不是措辞调整。proposal.md 第 72 行 Impact 表 Risk (3) 仍写"既有两行只改判据措辞不改字段"—— 该表述与代码级改动不符, 会让下游采用方 (SilkNode/Kairos/nexus, 升级 aria-plugin 后自动继承新语义) 低估此次升级的行为面变化。

### Finding 3

- `type`: issue
- `severity`: major
- `category`: documentation
- `scope`: `aria/skills/state-scanner/references/layer-l-integration.md` + `RECOMMENDATION_RULES.md` 对 `collision.kind` 的消费措辞 (proposal Tasks T1-T7 未覆盖)
- `summary`: 两处下游文档把 `tracks_multibranch.collision.kind` 的取值 (`cross_owner` / `!= none`) 当触发条件写死, 本 Spec 会改变这些取值在真实数据上的命中面 (triage case-3 显示"真两人两机"过去被误判 `self_multi_container`, 修复后才首次真正变成 `cross_owner`), 但 Tasks 里无一条提及需复核/更新这两处消费文档。
- `evidence`: `aria/skills/state-scanner/references/layer-l-integration.md:73` "**触发**: `tracks_multibranch.collision.kind == \"cross_owner\"` → 推荐 worktree 独立 checkout" 与 `:14` "cross-owner collision: ... 触发闸门"; `aria/skills/state-scanner/RECOMMENDATION_RULES.md:31` rule `concurrent_churn_detected` (priority 1.54) 触发条件 "`tracks_multibranch.collision.kind != none` 且 `coordination.enabled == false`"。proposal.md `.aria/triage-report.json` 复现的 case-3 (`docs/decisions` 引用同一批数据) 显示"真两人两机"在**当前**代码下被误判 `self_multi_container` (🟡), 从未真正触发过 `cross_owner` 分支, 也就从未真正触发过 layer-l-integration.md 承诺的"worktree 独立 checkout"推荐。本 Spec 修复 parser 后, 这条此前处于休眠状态的推荐路径会首次被真实激活, 触发频率与语义边界随之改变; proposal Tasks (T1–T7, proposal.md 第 78-84 行) 未包含任何一条核实/更新这两处引用文档描述, 也未在 SC 中锁定"真实 cross_owner 场景下 worktree 推荐确实触发"的回归断言, 知识链在此处未闭合。

### Finding 4

- `type`: issue
- `severity`: minor
- `category`: documentation
- `scope`: proposal.md §Why 第 3 点 (第 18 行) "主仓 frontmatter 今天仍是 9 种 owner-container 串对应 2 台机器"
- `summary`: 实测 `docs/handoff/*.md` 唯一 `owner-container` 串为 10 种 (含 `simonfish/f9c6e8cd` 单次出现), 而非 proposal 所称 9 种; 该差 1 的数据点未在 proposal 中说明为何被排除在"9 种"计数外。
- `evidence`: 命令 `grep -h '^owner-container:' docs/handoff/*.md | sort | uniq -c | sort -rn` 实测输出 10 行不同串 (`simonfishgit/dev-claude` 38、`simonfish/bfe8285d` 34、`simonfish/dev-claude` 24、`aria-runner-bot/023236f2` 23、`simonfish/023236f2` 17、`dev-claude` 9、`simonfish/dev-claude2` 3、`dev-claude2` 3、`aria-runner-bot/bfe8285d` 2、`simonfish/f9c6e8cd` 1); 154/142/12/0 三项分段统计 (两段 142、零段 12、三段 0) 与 proposal 第 16 行数字精确吻合, 但"9 种对应 2 台机器"与实测 10 种不吻合。交叉核对 `docs/handoff/2026-07-04-m6-blocker3-b2-impl-postplanning-rollout.md` (`simonfish/f9c6e8cd`, 2026-07-04T11:21) 夹在同日 `simonfish/dev-claude` (07-04 07:57) 与次日首次出现的 `simonfish/bfe8285d` (07-05) 之间, 大概率是 DEC-20260704-002 落地当天 `~/.aria/container-id` 首次 bootstrap 生成、随后被重新生成为 `bfe8285d` 的一次性瞬态 uuid, 可合理解释为同一物理机噪声而非第三台机器 —— 但 proposal 未写出这条排除依据, 留给读者自行核对。

### Finding 5

- `type`: decision
- `severity`: minor
- `category`: documentation
- `scope`: proposal.md `决策点` D-2 (第 61-65 行)
- `summary`: D-2 三个选项的"后果"陈述不对称: 执笔建议项 (a) 只列收益/对齐理由、未列任何代价; (b)/(c) 均以负面后果为主 —— 不完全满足"选项后果公平陈述, 不是只给推荐项写优点"的写法要求。
- `evidence`: proposal.md 第 62 行选项 (a) 原文: "所有 AI 会话 commit 署 bot; owner 段恒同 ⇒ 同一 owner 的多机永远是 🟡, 另一人的容器...才 🔴。与 Aether「人/机」两账号模型对齐" —— 全句无"后果:"式代价陈述; 对照第 63 行选项 (b) 明确写"两位操作者的 AI 会话之间才能区分🔴, 且与 Kairos/aria-runner 生产侧...不一致"、第 64 行选项 (c) 明确写"漂移继续, D3 告警持续常亮"。选项 (a) 实际存在的代价 (例如: 全部 AI 会话统一署 bot 后, 单条 commit 不再能反推是哪个人类操作者触发, 弱化事后追责/取证能力; 且该裁定本身不含任何任务把 git 提交身份真正切到 bot —— 容器 `git config` 归属被 §Non-目标 第 101 行显式排除在本 Spec 之外, 裁定与执行之间存在一个未指派负责方的落地缺口) 未被提及。

## Verdict

FAIL (1 Critical / 2 Major / 2 Minor)

判据: Finding 1 为 critical (≥1 Critical ⇒ FAIL)。proposal 主体的三层根因诊断 (triage 复现数据、`split_owner_container`/`classify_claims` 当前行为、与 #193/#135/a1-entry/Kairos DEC 的转述) 经逐条实读代码与命令核对均准确, 技术方向站得住; 但 D2 声称"新增"的 `standards` 小节编号与既有已发布内容冲突, 若不修正会直接损坏共享子模块的既有内容, 属于必须在进入 B.1 前修正的结构性缺陷。

## Vote

REVISE

## 轮次记录

- Round 1 (knowledge-manager, convergence 模式): FAIL, 1C/2M/2m。核心必修项: (1) D2 新增小节改为 `§2.3.9` (或核实后的下一个真实空档编号), 不得复用 `§2.3.7`/`§2.3.8`; (2) Impact 表关于"既有两行只改措辞不改字段"的表述需改写为如实反映 `cross-owner` 判据的语义改动, 并向下游采用方 (SilkNode/Kairos/nexus) 的沟通义务成文; (3) Tasks 补一条核实/更新 `layer-l-integration.md` 与 `RECOMMENDATION_RULES.md` 对 `collision.kind` 消费措辞的任务, 并在 SC 中锁定"真实 cross_owner 场景下 worktree 推荐确实触发"的回归断言。Finding 4/5 为非阻塞性精度/公平性建议, 可在 rework 中顺带处理。

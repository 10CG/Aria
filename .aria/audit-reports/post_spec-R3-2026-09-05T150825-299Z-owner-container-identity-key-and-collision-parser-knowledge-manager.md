---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-05T15:08:25.299Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## R2 处置核对

本席 R2 四条 Finding (A/B/C/D) 在 v3 (`91b86fb`, proposal.md sha1 `f8ffdfe`) 逐条核对, 均实读 v3 正文 + 相关代码/规范文件:

| R2 编号 | 内容一句话 | v3 处置状态 | 证据 |
|---|---|---|---|
| **Finding A** (major) | `advanced-rules.md` 路径写错 (缺 `rules/` 子目录), SC-9 未覆盖 | **CLOSED** | proposal.md:49 D4 已改 `references/rules/advanced-rules.md:544-572`; proposal.md:123 SC-9 显式含 `references/rules/advanced-rules.md`; `find aria -iname advanced-rules.md` 复核路径唯一命中 `aria/skills/state-scanner/references/rules/advanced-rules.md`, 路径正确 |
| **Finding B** (major) | 第四消费面 `phase-d-closer/scripts/fetch_gate.py` 未列入 D4/T7/SC-9 | **CLOSED** | proposal.md:50 D4 新增「代码消费方: `fetch_gate.py:251`...+ `tests/test_fetch_gate.py`」; T7 (proposal.md:107) 与 SC-9 (proposal.md:123) 均点名 `fetch_gate` advisory 文案含 `cross_owner` |
| **Finding C** (major) | `identity_key` / 「owner 等价类」在 standards 文本中未定义, 采用方不可机械复现 | **PARTIAL** | proposal.md:39 D2 已承诺「并在此定义 `identity_key`」, proposal.md:119 SC-5 要求「§2.3.1 含 `identity_key` 定义与三态; §2.3.5 判据只用 §2.3.1 定义的词 (grep 断言无 `等价类`)」——**意图层已收口, 且 v2 的「等价类」概念本身已随 R2 撤销, 原始问题的载体已不存在**。但本轮**试写**这三段拟定文本发现两处新的机械消费性缺口 (§2.3.5 owner 集合排除规则不完整、`same-identity-multi-owner` 语料范围未定), 见下方 Finding A/B (R3 编号, 非 R2 复发, 是换镜头后新可见的同类缺口) |
| **Finding D** (major) | Aether 两账号模型交叉引用无落点, 有把 Lab 私有文档耦合进共享 SOT 的风险 | **PARTIAL/CLOSED** | proposal.md:41 §2.3.9 已改为「只写...不引用任何 Lab 私有文档; 10CG Lab 内部指针...放 Aria 主仓 `docs/`...不进 standards」——**越界耦合的实质风险已解除** (standards 子模块不再字面引用 Aether 私有路径), 判定为 CLOSED。但「放 docs/」本身仍是无具体落点的空话, 本仓已有专用惯例 (`docs/decisions/DEC-*.md`) 未被点名, 见下方 Finding E |

## 试写文本

按 v3 D2 要点 (proposal.md:38-41) 试写 §2.3.1 / §2.3.5 / §2.3.9 三段标准文本, 检验一个不读 aria 代码的采用方能否机械复现。

### 试写 §2.3.1 (`<owner>` / `<container-id>` / `identity_key`)

```
<owner-container> = <owner>/<container-id> 复合标识。

<owner>: git `user.email` 的 local-part; 该 local-part 无法取得
  (git 未配置 / email 无 `@`) 时取字面值 "unknown"。

<container-id>: 三态之一——
  1. 该机 `~/.aria/container-id` 存在 (v1.22.x+): 取其中的 uuid 字段
     (人类可读 label 若存在, 不参与 identity_key/owner-container 取值)
  2. 该机无该文件 (v1.22.x 前的历史行): 取 hostname
  3. 该机文件系统只读, 无法持久化 container-id: 取 hostname (降级路径)

identity_key(owner, container):
  若 container 匹配正则 ^[0-9a-f]{8}$ (小写 8 位十六进制)
    → identity_key = container (uuid 全局唯一, owner 不参与同一性)
  否则
    → identity_key = owner + "/" + container
```

**试写未卡壳** —— D1 的 identity_key 定义 (proposal.md:32) 本身就是二分支 (`匹配正则` / `否则`), 三态只是对 `<container-id>` 来源的描述性分类, 不会诱导采用方把 identity_key 也拆成三分支实现 (D2 拟写文本若照抄这个顺序, 结构清晰)。

### 试写 §2.3.5 (三行判据表)

```
| Collision 类型 | 触发条件 | 渲染 |
|---|---|---|
| cross-owner | 同一 track-id 内, 按 identity_key 去重取每键最新行后,
    ≥2 个不同 identity_key; 且这些行的 <owner> 值集合 (排除空串)
    大小 ≥2 | 🔴 |
| self-multi-container | 同上前提 (≥2 个 identity_key), 但 <owner>
    值集合 (排除空串) 大小 ≤1 | 🟡 |
| same-identity-multi-owner | 同一 identity_key 在 [??? 范围] 内
    出现 ≥2 个不同的 <owner> 值 | ⚪ advisory, 不计入 collision.kind |
```

**试写卡壳两处** (对应下方 Finding A / Finding B):

1. 「排除空串」是否够——`proposal.md:34` (D1, 面向 aria 代码) 写的是「**非空且非 `unknown`**」,但 `proposal.md:40` (D2, 拟写入 standards 的原文) 只写「**非空** `<owner>` 集合」,漏了「非 `unknown`」。这不是文字简省——`<owner>` 字段的字面值**真的会是** `"unknown"`(见下方 Finding A 证据),照 D2 原文字面实现的采用方会把它当一个真实 owner 计数,产生 D1 明确要避免的假阳性。
2. `same-identity-multi-owner` 那行, 我卡在 `[??? 范围]` 处——proposal.md:40 只写「同一 `identity_key` 在语料中出现」,没说这个「语料」是"同一 track-id 内"(跟前两行一致的作用域)还是"全部非-legacy 行, 跨全部 track"(D3 `identity_drift_advisories(tracks)` 的真实实现作用域, proposal.md:45)。这两种读法对同一份数据会算出不同结果, 且表的排版会诱导读者按"同一张表, 同一个作用域"去读前两行的隐含限定词 "同一 track-id 内"。

### 试写 §2.3.9 (AI runner 提交身份)

```
### 2.3.9 AI runner 提交身份

<owner> 字段 (§2.3.1) 对人类操作者语义不变 (git user.email local-part)。

Aria 侧规则 (供参考, 非跨项目强制): AI 自主 runner 的提交身份使用与该容器
所属机器账号一致的 local-part; 操作者可追溯性由 <container-id> 段 +
handoff prose 承担, 不依赖 <owner> 段区分"哪位操作者在场"。

采用方的人机账号治理模型 (机器账号命名/轮换、容器 git config 的供给方式)
不在本规范范围, 由各采用方自行决定。
```

**试写未卡壳** —— 这段本身自包含 (不提 Aether/simonfish/10cg-ci-bot 字面), 满足「不引用任何 Lab 私有文档」的要求。落点问题不在本段文本内, 而在「Lab 内部指针放哪」(见 Finding E)。

## 审计结论

### Finding A

- `type`: issue
- `severity`: major
- `category`: documentation
- `scope`: proposal.md:40 (D2, §2.3.5 拟写文本) 与 proposal.md:34 (D1, 代码判据) 的排除规则不一致
- `summary`: D1 (面向 aria 代码实现) 明确写「取**非空且非 `unknown`** 的 owner 串集合」,而 D2 (拟写入 standards 供跨项目消费的文本) 只写「非空 `<owner>` 集合」,丢了「非 `unknown`」这一条排除。这不是良性简化——`<owner>` 字段的实际取值**确实会是字面字符串 `"unknown"`**,而不只是"空串"的另一种说法: `lib/identity.py:165-188` 的 `get_identity()` 在 git 未配置或 email 无 `@` 时,把 owner 段**写成字面值 `"unknown"`**,这个值经 `handoff_autofill.py --owner-container` 直接落进真实 frontmatter(不是 Aria 内部才有的哨兵值,是采用方读到的原始数据)。若采用方照 D2 原文只做「非空」过滤,一个 git 身份未配置的容器会被当成一个真实、独立的 owner 参与计数,在恰好存在另一个正常 owner 的同 track 上产生 D1 本要避免的**假阳性 `cross_owner`** ——正是本 Spec 要修的那类 bug 的翻版,只是换了个触发路径。SC-5 (proposal.md:119) 的 grep 断言只检查「无 `等价类` / 无 aria 代码路径」等词面存在性,不会挡下这处语义遗漏。
- `evidence`: `aria/skills/state-scanner/lib/identity.py:165` 文档字符串「returns `"unknown"`」+ `:185`/`:188` 两处 `return "unknown"` 实读确认;对照 proposal.md:34「非空且非 `unknown` 的 owner 串集合 (空 owner = 不可归属, **不计为独立 owner**)」与 proposal.md:40「取**非空** `<owner>` 集合」逐字对照,后者确实少了「非 `unknown`」限定词。

### Finding B

- `type`: issue
- `severity`: major
- `category`: documentation
- `scope`: proposal.md:40 (D2, `same-identity-multi-owner` 一行) 与 proposal.md:45 (D3, `identity_drift_advisories` 实现范围) 的作用域未在标准文本中显式对齐
- `summary`: §2.3.5 表的前两行 (`cross-owner` / `self-multi-container`) 判据都限定「同一 track-id 内」,`same-identity-multi-owner` 一行如果排在同一张表里却只写「在语料中出现」,采用方大概率会按"同一张表、同一作用域"的排版直觉,把它也理解成"同一 track-id 内出现 ≥2 owner"。但 D3 的真实实现 (proposal.md:45) 明写输入是 collector 的**全部非 legacy 行 (dedupe 前, 跨全部 track)**,且实验表的 advisory 对象 (proposal.md:62 `023236f2: [...]` / `bfe8285d: [...]`)**不带任何 track_id 限定**——这是一个**跨 track 全局** advisory,不是逐 track 计算的。两种读法在同一份数据上会给出不同的 advisory 集合 (逐 track 版会把同一容器在不同 track 上的漂移拆成多条互不相关的告警,或在只有单一 track 覆盖该容器时完全测不到漂移)。SC-5 (proposal.md:119) 未要求 §2.3.5 文本明写这一作用域差异, SC-10 (proposal.md:124) 只锁渲染条数,不锁语义作用域。
- `evidence`: proposal.md:40 原文「新增 **`same-identity-multi-owner`** = 同一 `identity_key` 在语料中出现 ≥2 个 `<owner>` → ⚪」 vs proposal.md:45「输入 = collector 的**全部非 legacy 行 (dedupe 前)**」——前者未注明"语料"即"全部非 legacy 行, 跨 track", 与前两行"同一 track-id 内"的隐含限定并列排版, 构成机械消费性歧义。

### Finding C

- `type`: issue
- `severity`: major
- `category`: documentation
- `scope`: `aria/skills/state-scanner/SKILL.md:149` — proposal.md:49 D4 对该文件的排除判断有事实错误
- `summary`: proposal v3 D4 (proposal.md:49) 明确写「`SKILL.md:149-154` 只引用字段名不引用取值, 不在同步面 (Rule #6 零 SKILL.md 改动仍成立)」。但实读 `SKILL.md:149` 原文——「触发条件...`state_scanner.coordination.enabled == true` (缺省即 true) **且** `tracks_multibranch.collision.kind` 非空 (**cross-owner / self_multi_container**)」——这一行**直接点名了 `collision.kind` 的两个枚举取值**,作为 AI 编排层"何时调用 `phase1_gate`"这一运行时指令的触发条件说明,不是只引用字段名。这是全仓 grep (`identity_key\|owner-container\|cross_owner\|self_multi_container` 于 `aria/skills/**/SKILL.md`) 命中的**第七处消费面**,且是唯一一处混在 SKILL.md 正文、直接影响 AI 编排触发时机描述的取值引用——比 D4 已列的五处参考文档更贴近「运行时指令面」。由于 `collision.kind` 的**枚举成员名不变**(只是判定逻辑变、`cross_owner` 首次真实可达),这行文字本身可以不改一个字仍然"字面正确";但 D4 排除它的**理由是假的**(不是"只引用字段名"),而且没有任何 SC/grep 断言把这行锁进回归面——未来若真有人改了枚举取值命名 (如与 §2.3.5 的连字符命名对齐), 这行会静默失配, 且不会被 SC-9 的五处 grep 抓到 (SC-9 范围明确写「五处文档」, 不含 SKILL.md)。
- `evidence`: `sed -n '149,150p' aria/skills/state-scanner/SKILL.md` 原文核实字面含 `cross-owner` 与 `self_multi_container` 两个取值 token; `grep -rln "cross_owner\|self_multi_container\|identity_key\|owner-container\|owner_container" aria/skills/**/*.md aria/templates/*.md` 命中该文件, 且是唯一一处在 `SKILL.md` 正文 (而非 `references/`) 内引用取值的文件; 对照 proposal.md:49 原文「`SKILL.md:149-154` 只引用字段名不引用取值」。

### Finding D

- `type`: gap
- `severity`: major
- `category`: process
- `scope`: proposal.md 全篇 Tasks (T1-T11) / D4 — 缺失版本发布同步任务
- `summary`: 本 Spec 的代码落点明确是 `aria/` 子模块内的功能性 bug 修复 (`lib/collision.py` / `handoff_multibranch.py` / `track_board.py` / `lib/identity.py`, 均非 SKILL.md), 按 `standards/conventions/version-management.md` §2.3 (patch 触发条件含"Bug 修复") 应至少触发 aria-plugin 的 PATCH 版本 bump。但全部 11 个 Task (T1-T11) 与 D4 消费面同步清单里**没有任何一条**提及 `aria/.claude-plugin/plugin.json` 版本号更新、5 文件同步面 (marketplace.json / VERSION / CHANGELOG.md / README.md / i18n README)、主仓 gitlink bump, 也没有提及 CLAUDE.md 项目状态段「版本: 插件 aria-plugin v1.69.0」这一行 (`claude-md-hygiene.md §2.3` 明确把"版本号一行"列入项目状态段预算, 要求 ship 后覆写)。实测当前 `aria/.claude-plugin/plugin.json` 已是 `1.69.1`, 与 CLAUDE.md 当前文本的 `v1.69.0` 已存在一版落差 (本 Spec 之前就有的既存 drift, 非本 Spec 引入), 说明这条同步链本身就容易被漏; 本 Spec 若不显式列出版本 bump 任务, 极可能重演。T10 (proposal.md:110) 只写「全套回归」测试, T11 (proposal.md:111) 只写「回帖 issue」, 均未覆盖版本发布同步面; Rule #6 段落 (proposal.md:96) 只讨论 benchmark 豁免, 不讨论版本 bump 是否豁免——二者是不同的机制, 不能互相代偿。
- `evidence`: `standards/conventions/version-management.md` §2.3 Patch 触发表含"Bug 修复"; `aria/.claude-plugin/plugin.json:4` 现值 `"version": "1.69.1"` vs `/home/dev/Aria/CLAUDE.md` 项目状态段现文本「版本: 插件 aria-plugin v1.69.0」(已有一版落差, 独立于本 Spec); `standards/conventions/claude-md-hygiene.md §2.3`「预算 ~15-20 行...版本号一行」+ §2.4「已 ship 条目在下一次覆写时删除」; proposal.md 全文 grep `plugin.json\|CHANGELOG.md\|marketplace.json\|版本 bump` 零命中 (Tasks/D4 段落内)。

### Finding E

- `type`: gap
- `severity`: minor
- `category`: documentation
- `scope`: proposal.md:41 §2.3.9「10CG Lab 内部指针...放 Aria 主仓 `docs/`」的具体落点未点名
- `summary`: R2 Finding D 的实质风险 (standards 子模块字面引用 Aether 私有路径) 已经解除——CLOSED, 见上表。但「放 docs/」仍然只是方向性描述, 未点名具体子目录。本仓已有专用且已被 `standards/` 反向引用过的惯例: `docs/decisions/DEC-YYYYMMDD-NNN-<slug>.md` (实证: `DEC-20260519-001-multi-terminal-coordination.md` / `DEC-20260704-002-interactive-session-duplicate-prevention.md` 均被 `standards/conventions/session-handoff.md` 从子模块内部引用, 是"主仓决策记录 + 子模块指针"这一模式的既有先例)。proposal 若不点名这个既有惯例, D 期执笔人很可能在 `docs/` 下新起一个 ad-hoc 文件 (如 `docs/architecture/` 或裸 `docs/aether-notes.md`), 造成落点不一致、未来难以按固定路径检索。建议 D 期 closeout 时新开 `docs/decisions/DEC-<date>-NNN-aether-account-model-pointer.md` (或等价 slug), 而非另起花样。
- `evidence`: `find docs -maxdepth 2 -type d` 确认 `docs/decisions/` 存在且含 21 个 `DEC-*`/日期前缀文件; `grep -rn "docs/decisions" standards/conventions/session-handoff.md` 命中 5 处, 确认该目录是"主仓决策记录, 子模块指针引用"模式的既有、已验证先例, 与本 Spec 想要的效果 (standards 不直接耦合 Lab 私有内容, 但仍需要一个可引用的落点) 完全同形。

## Verdict

PASS_WITH_WARNINGS (0 Critical / 4 Major / 1 Minor)

判据: R2 四条 Finding 中两条 (A/B, 消费面路径与遗漏) 已完整闭合; 另两条 (C/D) 的**核心风险**已闭合 (「等价类」概念随 v2 撤销消失、standards 不再字面耦合 Lab 私有路径), 但换镜头**试写**标准文本后, 在同一批文本 (§2.3.1/§2.3.5/§2.3.9) 上发现了**四条新的 Major** —— 两条是 D1(代码)/D2(standards 文本) 之间的定义漂移 (owner 排除规则丢字、advisory 作用域未定, 均属"试写才能发现"的机械消费性缺口, 不是简单复发), 一条是 proposal 自己对 SKILL.md 的排除判断有事实错误 (漏掉第七个真实消费面, 且排除理由本身站不住), 一条是版本发布同步链条 (aria-plugin 版本 bump + CLAUDE.md 版本行) 全程未出现在 Tasks/D4 里。四条均不阻断 B.1 起步 (都是"标准文本/任务清单还没写到那一步就已可预判的缺口", 不是代码逻辑或决策点本身的错误), 但若不在本轮 rework 一并写入 T5/D4/SC-5/SC-9, 会在 T5 落地 standards 文本或 D 期发版同步时再次留下"写了但对不上"的缺口, 与 R2 的收敛方向 (「v3 修复应收口, 不留新面」) 相悖。1 条 Minor (Aether 指针具体落点未点名既有 `docs/decisions/` 惯例) 是 B 期可顺手处理的收尾项。

## Vote

REVISE

## 轮次记录

- Round 1 (knowledge-manager): FAIL, 1C/2M/2m — 3/5 条已闭合, 1 条 (M3) 部分闭合。
- Round 2 (knowledge-manager, convergence, 镜头「规范文本与知识链能否被采用方与 owner 无歧义消费」): PASS_WITH_WARNINGS, 0C/4M/0m — 新增 Finding A/B/C/D (路径错误 / 第四消费面遗漏 / `identity_key` 未定义 / Aether 交叉引用无落点)。
- Round 3 (knowledge-manager, convergence, 镜头「规范文本机械消费性 + 决策点呈现 + 知识链落点」): PASS_WITH_WARNINGS, 0C/4M/1m。R2 四条中 A/B CLOSED, C/D 核心风险 CLOSED 但各自留了一条同类新缺口。**试写**§2.3.1/§2.3.5/§2.3.9 三段拟定文本抓到两条 D1/D2 定义漂移 (owner 排除规则、advisory 作用域); grep 全仓 SKILL.md 抓到 proposal 自证的「SKILL.md 只引用字段名」判断为假, 第七处消费面 (`SKILL.md:149`) 遗漏; 核对版本管理规范抓到版本发布同步链条 (plugin.json bump + CLAUDE.md 版本行) 全程未入 Tasks。D-0/D-1/D-2/D-3 四个决策点本轮核对后果陈述均对称 (含 D-0(c) 与 a1-entry `linked_issue_overlaps` 独立通道的技术核验, 未发现新问题); D-0 未显式排除"与 a1-entry 合并成一个 Spec"选项, 但鉴于 a1-entry 已过 Phase A 且已在其自身 §3 把此 follow-up 显式排出范围, 判定不成立独立 finding。「历史不 rewrite」与 §2.3.4 legacy 定义口径核对一致 (`owner_container=="unknown"` 是 legacy 判定的唯一产物, 零段串 `dev-claude` 因 frontmatter 5 字段完整而不落入 legacy, 与 D3 排除口径同源, 无 finding)。

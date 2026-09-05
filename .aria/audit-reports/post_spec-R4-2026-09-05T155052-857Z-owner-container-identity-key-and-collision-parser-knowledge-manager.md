---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-05T15:50:52.857Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## R3 处置核对

本席 R3 五条 Finding (A/B/C/D/E) 在 v4 (`addc8a1`) 逐条核对, 均实读 v4 正文 + 相关代码/规范/模板文件:

| R3 编号 | 内容一句话 | v4 处置状态 | 证据 |
|---|---|---|---|
| **Finding A** (major) | D2 判据句丢「非 `unknown`」排除, `<owner>` 真会取值 `unknown` | **CLOSED** | proposal.md:34 (D1) 与 proposal.md:42 (D2 standards 文本) 现均写「**非空且非 `unknown`**」/「**非空、非 `unknown`**」, 两处逐字对齐, 不再有 D1/D2 定义漂移 |
| **Finding B** (major) | `same-identity-multi-owner` advisory 语料作用域 (同 track vs 全局) 未在标准文本内注明 | **CLOSED** | proposal.md:42 现明写「同一 `identity_key` 在**采用方仓的 handoff 全集 (跨 track、跨分支)** 出现 ≥2 个...」, 与 proposal.md:47 (D3 实现: `collector 的全部非 legacy 行, dedupe 前, 跨 track`) 语义一致, 不再依赖排版隐含限定 |
| **Finding C** (major) | proposal 声称 `SKILL.md:149-154` 只引用字段名, 该判断为假 (实含 `cross-owner`/`self_multi_container` 取值字面) | **CLOSED** | proposal.md:51 改写为「SKILL.md:149-154 (**含取值字面** `cross-owner` / `self_multi_container` 作为编排触发条件; **取值不变故不改动**, 语义变更经 §2.3.5 + CHANGELOG 明示 ⇒ Rule #6 零 SKILL.md 改动成立)」——不再否认取值字面的存在, 改用「取值不变」这一站得住的理由; 复读 `sed -n '149p' aria/skills/state-scanner/SKILL.md` 确认理由属实 (枚举成员名 `cross_owner`/`self_multi_container` 本 Spec 未改) |
| **Finding D** (major) | 版本发布同步链条 (aria-plugin bump + CLAUDE.md 版本行) 全程未入 Tasks | **CLOSED** | 新增 D5 (proposal.md:54) + T12 (proposal.md:117): PATCH bump + CLAUDE.md §版本管理同步面 + CHANGELOG 明示 + Lab 指针决策单, 挂 SC-7 (state-check 覆盖版本面); 复核 `standards/openspec/project.md:3` (Version 2.2.2) vs 主仓 `VERSION` (standards v2.2.3) 确认「standards 版本口径沿对方容器待裁项, 本 Spec 不另起口径」这一表述属实、非虚构 |
| **Finding E** (minor) | Aether 指针具体落点未点名既有 `docs/decisions/` 惯例 | **CLOSED** | proposal.md:43/117 均已采纳 `docs/decisions/`; `ls docs/decisions/` 复核该目录现有 21 个 `DEC-*` 文件, 惯例命名为 `DEC-YYYYMMDD-NNN-<slug>.md`, 与 v4 的落点选择一致 |

**R3 五条全部 CLOSED**(0 open / 0 partial / 5 closed)。换镜头对 v4 新文本重做试写, 发现两条新的 Major (下方 Finding A/B), 均属「写到这一步才能看见」的机械消费性缺口, 非 R3 复发。

## 试写文本

### 试写 §2.3.1 (三态 + `identity_key` + D-0(a) 尾段语义)

```
<owner-container> = <owner>/<container-id> 复合标识 (二段式)。

<owner>: git `user.email` 的 local-part; 该 local-part 无法取得
  (git 未配置 / email 无 `@`) 时取字面值 "unknown"。

<container-id>: 三态之一——
  1. 该机 `~/.aria/container-id` 存在 (v1.22.x+): 取其中的 uuid 字段
     (人类可读 label 若存在, 不参与 identity_key/owner-container 取值)
  2. 该机无该文件 (v1.22.x 前的历史行): 取主机名
  3. 该机文件系统只读, 无法持久化 container-id: 取 hostname (降级路径)

identity_key(owner, container):
  若 container 匹配正则 ^[0-9a-f]{8}$ (小写 8 位十六进制)
    → identity_key = container
  否则
    → identity_key = owner + "/" + container

[D-0(a) 追加句, 按 proposal.md:41 指示写入]
track-id 尾段若匹配正则 -[0-9a-f]{8}$, 该尾段在 Layer H collision 分组时
被纯形状剥离。
```

**这句追加句本身试写卡壳** —— 见下方 Finding A: 它没有说清「只对 §2.3.5 Layer H collision 分组生效, 不影响 §2.3.8.2 carry-id / Layer L claim 匹配」, 而 §2.3.1 是 §2.3.8.2「track-id 同串」判据引用的同一个定义源。

### 试写 §2.3.5 (三行判据表)

```
| Collision 类型 | 触发条件 | 渲染 |
|---|---|---|
| cross-owner | 同一 track-id 内, 按 identity_key 去重取每键最新行后,
    ≥2 个不同 identity_key; 且这些行的 <owner> 值集合 (排除空串与
    "unknown") 大小 ≥2 | 🔴 |
| self-multi-container | 同上前提, 但 <owner> 值集合 (排除空串与
    "unknown") 大小 ≤1 | 🟡 |
| same-identity-multi-owner | 同一 identity_key 在采用方仓的 handoff
    全集 (跨 track、跨分支) 中出现 ≥2 个不同的、非空且非 "unknown"
    的 <owner> 值 | ⚪ advisory, 不计入 collision.kind |
```

**试写未卡壳** —— R3 Finding A/B 两处缺口 (排除规则、advisory 作用域) 均已补齐, 三行判据表本身可被一个不读 aria 代码的采用方直接照抄实现, 结果确定。

### 试写 §2.3.9 (AI runner 提交身份, 按 D-2(c) 补句后的最终版)

```
### 2.3.9 AI runner 提交身份

<owner> 字段 (§2.3.1) 对人类操作者语义不变 (git user.email local-part)。

Aria 侧规则 (供参考, 非跨项目强制): AI 自主 runner 的提交身份统一使用
与该容器所属机器账号一致的 bot local-part。已知限制: 同一 bot
local-part 的 AI 会话之间 cross_owner 结构性不可达 (§2.3.5 判据里,
"两个不同提交身份"退化为恒真集合大小 1); 操作者可追溯性由
<container-id> 段 (§2.3.1) + handoff prose 承担, 不依赖 <owner> 段
区分"哪位操作者在场"。

采用方的人机账号治理模型 (机器账号命名/轮换、容器 git config 的供给
方式) 不在本规范范围, 由各采用方自行决定。
```

**试写未卡壳** —— 自包含, 不提 Aether/simonfish/10cg-ci-bot 字面, 满足「不引用任何 Lab 私有文档」; D-2(c) 补的「`cross_owner` 可达但不可解释」句已让 (a)/(b)/(c) 三个选项对称覆盖 `cross_owner` 可达性, 无偏置。

## 审计结论

### Finding A

- `type`: issue
- `severity`: major
- `category`: documentation
- `scope`: proposal.md:41 (D2, D-0(a) 追加到 §2.3.1 的尾段语义句) 与 proposal.md:232-236 (`session-handoff.md §2.3.8.2`, 现行 SOT)
- `summary`: D-0(a) 要求在 §2.3.1 加一句「track-id 尾段 `-<8hex>` 被剥离」, 但 proposal.md:41 只给了这一句的**主题**(「加一句...族键语义」), 没有要求这句话显式限定**适用范围**。D1 (面向 aria 代码, proposal.md:35) 把这条规则精确限定在 `track_to_claim_record` **一处**、**只影响 Layer H 两条路径, 明写「Layer L claim 不经它」**; 但这条限定是写给"读 aria 代码的执笔人"看的, 不会自动进入 D2 拟写的 standards 文本。§2.3.1 是 `track-id` 字段的**唯一定义源**, `session-handoff.md §2.3.8.2` (proposal.md:232-236 现行文本, 本 Spec 靠 SC-5「§2.3.7/§2.3.8 diff 零」保证其字面不改) 明确要求「§6 carry-id 与本 handoff doc-level frontmatter `track-id` 指向同一份工作时, 两者取**相同原始串**」。如果 §2.3.1 新增的尾段剥离句不显式声明"仅用于 §2.3.5 Layer H collision 分组, 不改变 track-id 字段本身的取值, 不影响 §2.3.8.2 的原始串匹配", 一个只读 standards (不读 aria 代码) 的采用方在独立实现 carry-id 匹配逻辑时, 有真实概率把这条新规则也套用到 §2.3.8.2 的"相同原始串"判据上 (例如把两个容器各自派生的 `<spec>-<uuid1>` / `<spec>-<uuid2>` 剥尾后当作"同一原始串"接受, 从而放宽本该保持严格的 carry-id 判等), 产生与本 Spec 意图相反的行为。SC-5 的「diff 零」只锁住 §2.3.8.2 自身文字不被编辑, 不能防止读者把 §2.3.1 新语义"倒灌"进对 §2.3.8.2 的理解——这正是"未改一个字却因上游定义变化而语义漂移"的经典陷阱, 与 R3 Finding C (SKILL.md 取值不变但语义变化) 是同一类问题的镜像 (那次是"字面不变但语义变", 这次是"字面不变但上游定义变会污染读法")。
- `evidence`: `sed -n '232,236p' standards/conventions/session-handoff.md` 实读确认 §2.3.8.2 现行文本「当某条 §6 carry-id 与本 handoff doc-level frontmatter `track-id`(§2.3.1) 指向同一份工作时, 两者取相同原始串」, 且该条**引用 §2.3.1** 作为 track-id 的定义源; proposal.md:35「在 `track_to_claim_record` 一处 (Layer H 两条路径 `collision.py:347` / `track_board.py:783` 同源; **Layer L claim 不经它**)」这句范围限定只出现在 D1 (面向 aria 代码) 段落, D2 (proposal.md:41) 对应句「D-0(a) 时加一句 track-id 尾段 `-<8hex>` 的族键语义」未要求把这条 Layer H-only 限定写进 standards 文本本身; SC-5 (proposal.md:126) 亦未对这句新增文本设置"必须显式排除 §2.3.8.2 / Layer L"的断言。
- `remediation_suggestion`: T5 (proposal.md:110) / SC-5 (proposal.md:126) 给这句追加明确要求, 例如: 「D-0(a) 追加句须显式写明'该剥离规则仅用于 §2.3.5 Layer H collision 分组键计算; 不改变 track-id 字段本身的定义或取值, 不影响 §2.3.6 Layer L claim 匹配与 §2.3.8.2 carry-id 原始串比对'」, SC-5 加一条 grep 断言 (如「§2.3.1 新增句含 token `仅用于`/`不影响` 且提及 `§2.3.8.2` 或 `Layer L`」) 把这条要求锁进回归面, 而不是留给 T5 执笔人临场判断。

### Finding B

- `type`: issue
- `severity`: major
- `category`: documentation
- `scope`: proposal.md:51 (D4, `aria/templates/session-handoff.md` 的更新要求) 与 `aria/templates/session-handoff.md:33-43` (现行模板文本)
- `summary`: D4 把 `aria/templates/session-handoff.md` 列为消费面之一, 要求「owner-container 示例, **若含 label 形示例则改 uuid 形**」——这条要求只处理**示例字符串的形态**, 但实读该模板发现问题不止示例字符串: 第 43 行在给出 uuid 形示例 `"simonfish/bfe8285d"` 后, 紧跟一句括号说明「(label 空 → uuid; **设 label 使更可读**)」, 这是一句**主动鼓励用户设置 label** 的指导性文字, 而设置 label 正是本 Spec 的 Why 段第 3 层根因 (proposal.md:19「填个可读名就静默换了协调身份」, aria-plugin #135 缺口 3) 与 T3b 迁移检查要防的确切动作。关键是 S1/S2 两态下这句话的危险程度不同: **S2 (flip 落地后)** `get_container_id()` uuid 优先, 设 label 变成纯展示、无害, 这句话届时安全; **S1 (flip 未落地时 ship, proposal.md 明写为可能先 ship 的形态)** `get_container_id()` 仍是 `label if label else uuid` (proposal.md:19), 设 label **依旧会**静默切换协调身份, T3b 在 S1 下只提供"迁移告警"(`phase1_gate`/`release_gate` 侧, proposal.md:38「S1 语义 = 纯 inventory 告警...无抑制」), 且这个告警只在跑这两个 gate 脚本时触发, 一个只是手动编辑 `~/.aria/container-id` 加 label、还没触发任何 gate 的用户不会看到任何告警——模板里这句"设 label 使更可读"因此在 S1 窗口期是**直接把用户导向本 Spec 正在修的那个 bug 入口**。D4 现有措辞"若含 label 形示例则改 uuid 形"只会让执笔人换掉例字符串 (如把 `"creationhikari/devbox-A"` 换成另一个 uuid 形串), 不会必然处理或移除这句独立的鼓励性说明文字, 因为它在措辞上不是"示例"本身, 而是示例旁的注释。
- `evidence`: `sed -n '33,43p' aria/templates/session-handoff.md` 实读确认第 42-43 行「示例: "creationhikari/devbox-A" / "simonfish/bfe8285d" (label 空 → uuid; **设 label 使更可读**)」; `sed -n '126,137p' aria/skills/state-scanner/lib/identity.py` 确认 `get_container_id()` 当前 (S1) 实现是 `label if label else uuid` (:222) 且 `_write_container_file` 本身也在容器文件头写「Edit the \`label\` line to add a human-readable tag」(:134, 这是 T3「container-id 文件头注释改写」已点名的**另一处**同类鼓励, 与本模板文件是**两个独立位置**); 对照 proposal.md:51「aria/templates/session-handoff.md (owner-container 示例, 若含 label 形示例则改 uuid 形)」, 措辞范围止步于"示例形态", 未提这句独立的鼓励性说明。R1-R3 五席既往报告 (`grep -rn "templates/session-handoff\|设 label\|devbox-A" .aria/audit-reports/post_spec-R{1,2,3}-*` ) 均无命中, 确认这是新发现, 非既往轮次遗留复发。
- `remediation_suggestion`: D4/T7 对该模板文件的要求改写为「示例改 uuid 形; **删除或按 S1/S2 分支改写"设 label 使更可读"这句**(S1 期不建议设置 label, 并指向 T3b 告警说明; S2 落地后方可恢复"设 label 使更可读"的鼓励)」, 并入 SC-9 (proposal.md:130) 的 grep 断言集 (如断言该文件不再含"设 label 使更可读"这一无条件表述, 或改为条件化措辞)。

## Verdict

PASS_WITH_WARNINGS (0 Critical / 2 Major / 0 Minor)

判据: R3 五条 Finding (A-E) 在 v4 全部 CLOSED, 无一复发, `identity_key` 定义、advisory 作用域、SKILL.md 消费面陈述、版本发布同步链条、Aether 指针落点五个方向的机械消费性缺口均已收口。但本轮换镜头对 v4 新增/改写的两处文本 (D-0(a) 追加进 §2.3.1 的尾段语义句、D4 对 `aria/templates/session-handoff.md` 的更新要求) 重做试写, 各卡壳一处: (1) 尾段剥离句未显式排除 §2.3.8.2 Layer L carry-id 匹配, 存在"上游定义变化倒灌进未改动文本的读法"风险; (2) 模板文件里独立于"示例"之外的"设 label 使更可读"鼓励句在 S1 窗口期直接引导用户走向本 Spec 正在修的 bug 入口, D4 现有措辞只覆盖示例字符串换形, 未覆盖这句独立说明文字。两条均是**新文本自身**的精度缺口 (不是决策点公平性问题, 也不是 R3 遗留), 修复成本低 (各一句话/一个条件化改写), 应折入 T5/SC-5 (Finding A) 与 T7/SC-9 (Finding B) 而非留到 B 期人工判断——理由与 R1-R3 一贯的处置口径一致: 这类"标准文本机械消费性"缺口一旦进入 T5/T7 执行阶段才被发现, 执笔人不会自动知道要处理它 (Finding A 属于"上游定义变了但没人告诉你连带影响哪些下游引用", Finding B 属于"任务测的是示例形态, 没测例子旁边那句话"), 与本轮任务书要求的"卡住处即 finding"判据相符, 因此不满足"仅剩 minor"的 PASS 门槛。

## Vote

REVISE

## 轮次记录

- Round 1 (knowledge-manager): FAIL, 1C/2M/2m。
- Round 2 (knowledge-manager, convergence): PASS_WITH_WARNINGS, 0C/4M/0m — Finding A/B/C/D (路径错误 / 第四消费面遗漏 / `identity_key` 未定义 / Aether 交叉引用无落点)。
- Round 3 (knowledge-manager, convergence): PASS_WITH_WARNINGS, 0C/4M/1m — R2 四条中 A/B CLOSED, C/D 核心风险 CLOSED 但各留一条同类新缺口; 试写抓到 D1/D2 定义漂移 (owner 排除规则、advisory 作用域)、SKILL.md 消费面陈述为假、版本发布同步链条缺失。
- Round 4 (knowledge-manager, convergence, 镜头「v4 新文本机械消费性 + D4 消费面陈述准确性 + 发布同步/落点一致性 + 决策点公平性」): PASS_WITH_WARNINGS, 0C/2M/0m。R3 五条 (A/B/C/D/E) 全部 CLOSED 无复发; D-0(d)/D-2(c) 决策点核对公平 (D-2 三选项均已对称写 `cross_owner` 可达性, `执笔建议` 未夹带未支撑结论); D5 发布同步判据 (PATCH vs MINOR、standards 版本口径待裁项) 经实读 `standards/openspec/project.md:3` 与主仓 `VERSION` 核实属实; `docs/decisions/` 落点与既有 21 个 `DEC-*` 命名惯例一致。试写 D-0(a) 追加进 §2.3.1 的新句抓到"未排除 §2.3.8.2 Layer L carry-id 匹配"的范围歧义 (Finding A); 实读 `aria/templates/session-handoff.md:33-43` 抓到 D4 对该模板的更新要求遗漏了示例旁边"设 label 使更可读"这句独立鼓励文字, 在 S1 窗口期直接引导向本 Spec 正在修的 bug (Finding B)。两条均新文本精度问题, 修复成本低, 建议折入 T5/SC-5 与 T7/SC-9 后进 R5。

---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-14T14:08:30.884Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [tech-lead]
---

# post_spec Round 5 — tech-lead 席 (被审 SHA f169a0b, rework v5)

> 只审不改: 除本报告外没写任何仓库文件, 临时脚本与 diff 都在 scratchpad。独立性: 没读同目录任何 R5 报告; R4 只读了聚合报告和本席报告。远端只做了一次只读查询 (`forgejo GET /repos/10CG/Aria/issues/196`), 没有 fetch, 没有 push。
>
> 本席所在机器就是 `dev-claude2`, `~/.aria/container-id` 的 uuid 前缀为 `bfe8285d` —— v5 事实依据里的两个容器之一就是本机, 「开发容器」这一点因此可以直接核实 (记录 5)。

## R4 对账

我席 R4 共 4 条 (major 2 / minor 2)。结果: **closed 4 / partially 0 / open 0**。

| R4 条 | 严重度 | 判定 | v5 落点 (段名) 与核实 |
|---|---|---|---|
| 1 Layer 2 覆盖还差两段 (验证前怎么办及推荐项代价; 「只在 Claude 上验证过」没进规范) | major | **closed** | 验证前的中间态: §D1 SOT §2 新句加自主条款「自主运行时 (`unattended == true`) 在场景 4b 于其所用模型上验证之前, 不做 description 改动, 需要改时任务进 S_FAIL」, 即 fail-closed; CLAUDE.md 新句尾加「自主运行时的处置见 SOT §2」。代价: §Impact 末条写明「按推荐 …… 自主模式在 GLM 验证完成前遇到 description 改动一律停在 S_FAIL, 这是推荐项的代价」。规范留痕: §D6 第三条尾加「场景 4b 只在 Claude 模型上实测过 (`claude-fable-5-1` / `claude-opus-5`), Layer 2 所用的 GLM 未验证」; §D5 第 6 项开 issue 追踪 GLM 验证, T6 / SC-6 / Key Deliverables / 抬头「代码落点」四处同步为「三张」(记录 17)。我 R4 点名的两段都补上了。新条款本身带出的问题 (验证之后那一段与推荐 (C) 不一致、裁定落点悬空、没有 SC 锁) 是新问题, 单列为 Finding 1 与 Finding 2, 不算本条残留。 |
| 2 自主模式栏事实依据归因错、缺运行模式判据、(B) 跑不起来、「只能 B」漏选项 | major | **closed** | §OQ-7 自主模式栏: 事实依据改为「共用机器提交身份 + handoff 只配两个开发容器 (23 / 7) + 两次发版抽查都是交互会话」, 并注明 v4 的误作已更正, 各项机械核实成立 (记录 1–6); (B) 注「当前跑不起来」, 原因是 runner 镜像无 skill-creator, 核实成立 (记录 7); 选项扩为 (B) / (C) / (D) / (E), 各带代价, 「可行做法只有 (B)」已删; 新增「运行模式怎么判」= `state_scanner.coordination.unattended` 配置事实, 挂 `10CG/Aria#196` 已知缺口 (记录 8)。判据选了配置键, 而不是我 R4 建议的「有无 Layer 1 派发与 S7」, 我认可: 配置事实合乎 Rule #10 (不做运行期推断), 且该键设计时就指向 Layer 2 (config-loader 的取值路径注释); /goal 直驱这类没有 S7 的会话默认 `false`, 走交互 (A), 与我 R4 建议的处理一致。遗留只到观察层: (D) 同样跑不起来 (观察 2)、S_FAIL 默认自动重试 (观察 1)、§2.3.9 的引用范围 (观察 3)、全称结论的支撑 (观察 4)。 |
| 3 v3 逻辑在 SOT §3 边界注与 D4 合规清单的残留 | minor | **closed** | §D1 边界注改为「description hunk 不走本节, 走 §2 第二行: 照跑场景 1, 另须跑场景 4b」; §D4 合规句改为「`description_changed: yes` 而 `scenario1` 或 `scenario4b` 为空、`not_required` 或 `n/a` ⇒ 不合规」。我 R4 论证里顺带提的 `decision_table_row` 须为 2 没有写, SC-10 仍只锁边界注前半句, 放观察 7。 |
| 4 SC-9 删掉 fail 那行照样全绿 | minor | **closed** | SC-9 改为「同时含 fail 与不得 ship 的行 ≥ 1、同时含作废与不得 ship 的行 ≥ 1」。对 v5 §D2 实跑反事实: 删「fail 的后果」行, 第三项转假; 删作废行, 第四项转假 (「连续 2 轮」也随之转假), 两种删法都转红 (记录 12)。 |

## Findings

- [major] architecture/proposal.md §D1+§D4+§OQ-7 (issue): 自主推荐由 (B) 改 (C) 后规范文本没跟上: SOT 自主条款只编码 OQ-9「先验证」, 缺 (C)「无已审套件不改」, GLM 验证后即失效; D4 仍无条件保留 (B) 的 provisional, 合规清单放行「pass provisional」ship; 裁定只以「依 OQ-7 / OQ-9 …… 随之改」「见 OQ-7」指代, 逐字转录后悬空。
- [minor] testing/proposal.md §SC-1+§SC-7 (issue): v5 为 R4 两条 major 加的三处规范文字 (SOT 自主条款 / CLAUDE.md「自主运行时的处置见 SOT §2」/ D6「只在 Claude 模型上实测过」) 没有任何 SC 能变红; 转录时整句漏掉, 全部 SC 仍绿。SC-7 连 §6 第三条是否存在都不查。
- [minor] documentation/proposal.md §D6 (issue): D6 要转录进 SOT §6 的句子仍引「RESULT.md v4」, 而 v4 的已知局限写的是「判红的只有两类」, 与同句「(未穷举)」相反; 抬头「RESULT 再修订须同步重核」清单不含 D6, 这次换版漏改。

## Findings 论证

### Finding 1: OQ-7 / OQ-9 的推荐裁定没有写进规范文本

v4 → v5 的 diff 里, OQ-7 自主模式的推荐从「(B) 且审阅并入 S7」改成了「(C)」。推荐改了, 要逐字或近逐字转录进 SOT 与手册的三处规范句却没跟着改, 结果是它们编码的规则与推荐的裁定对不上。三处分开说。

**1. SOT §2 自主条款只编码了一半。** 按推荐 (OQ-7 自主 (C) + OQ-9 先验证), 自主模式的规则是两段式:

| 阶段 | 推荐裁定下应有的规则 | v5 SOT 条款写了什么 |
|---|---|---|
| GLM 上 4b 验证之前 | 任何 description 改动都不做, 进 S_FAIL | 写了 (「在场景 4b 于其所用模型上验证之前, 不做 description 改动」) |
| 验证之后 | 只改「有已审 trigger 套件」的 skill; 没有的照旧不改、进 S_FAIL ((C) 原文「自主模式不改「没有已审 trigger 套件」的 skill 的 description」) | **没写**。条款的条件只有「验证之前」, 验证一完成, 整句失效 |

验证之后, 自主执行者手里只剩通用规则 (照跑场景 1 + 4b) 和 D4「套件未经 owner 审阅时结果带 provisional」。它会自建套件、跑出 `pass provisional`, 合规清单不拦, 进 S7 —— 这正是推荐 (C) 要挡的「弱套件判出假绿」, 而且是在 owner 没做「升级到 (B) 或 (D)」这个决定的情况下自动发生的 (OQ-7 推荐理由原文: 「自主模式改 description 变得常见时再升级为 (B) 或 (D)」)。「验证完成」本身也没有判据: 条款没说以什么为准 (D5.6 那张 issue 关闭? SOT §6 第三条改写?), 执行者从 SOT 读不出这个条件现在是真是假。

**2. D4 的 provisional 在推荐裁定下没有合法用途, 却写成无条件规则, 并放行 ship。** OQ-7 交互 (B) 原文: 「cycle 作者建套件并跑, 结果带 provisional 后缀 (D4), owner 事后审」—— provisional 是 (B) 的机制。v4 推荐自主 (B), provisional 那时有推荐范围内的用途; v5 推荐变成交互 (A) + 自主 (C), 两种模式下未审套件都不能作门, provisional 就只剩非推荐选项在用。可 D4 仍写「套件未经 owner 审阅时 (OQ-7), `scenario4b` 结果后缀 provisional」, 不带条件; 合规清单只拦 `fail` / `void`, `pass provisional` 可以 ship。按推荐裁定照转录文本执行, 交互执行者同样可以凭自建的未审套件 ship description 改动, 与 (A)「套件审过才能作门」正相反。

**3. 裁定的落点是悬空引用。** 三处规范句都用 OQ 编号指代裁定, 没有写出裁定结果:

- D1 SOT 新句 (`proposal.md` 第 39 行) 的括注「(依 OQ-7 / OQ-9 裁定, 裁定不同则随之改)」在「新句 (定稿)」格里, T1 要求「逐字」落地 ⇒ 这句写给实施者的起草注记会原样进 standards 这个共享子模块 (Rule #5 原话, 另有 GitHub 镜像 `10CG/aria-standards`);
- D2 (第 56 行)「新套件是否须 owner 审阅后才能作门, 见 OQ-7」与 (第 54 行)「按 OQ-7 的审阅要求」经 T2 进手册 §4b;
- D4 (第 84 行)「(OQ-7)」经 T3 进 SOT §4.1。

proposal 归档后, SOT 与手册的读者看到的「OQ-7 / OQ-9」指向一份已归档的 Aria proposal; 「套件要不要审」这条规则本身, 在规范里只剩一个指针。没有任何任务负责「把裁定结果写进这几句」。

**「依 OQ-7 / OQ-9 裁定, 裁定不同则随之改」对待批 spec 恰不恰当 (任务 3 的问题)**: 声明「本句依赖 OQ 裁定」本身是对的, 问题出在位置和完整性。第一, 这是写给实施者的注记, 应放在 D1 正文或 T1, 不应放进要逐字转录的定稿格。第二, 定稿句应当是**推荐裁定下的完整文本**, 现在只覆盖了 OQ-9 那一半 (上面第 1 点)。第三, 裁定与推荐不同时, 「随之改」等于让 Phase B 实施者起草一条没过 post_spec 审计的规范句, 由实施者替 owner 定规范措辞, 与 Rule #10 的精神相悖。应改为按选项分别给出定稿句, 或写明「裁定与推荐不同 ⇒ 回 A.1 改写该句并复审」。

**修法 (纯文字, 不用重跑)**:

1. SOT §2 自主条款定稿改为同时编码两段, 例如「自主运行时 (`unattended == true`) 只在两条同时成立时做 description 改动: 场景 4b 已在其所用模型上验证 (以本规范 §6 第三条的记载为准), 且被改 skill 有经 owner 审阅的 trigger 套件; 否则不做, 需要改时以失败结束任务并写明原因 (Aria 2.0 运行时由 Layer 1 升级为 S_FAIL)」。括注「依 OQ-7 / OQ-9 裁定」移到 D1 正文。
2. D4 的 provisional 句按推荐裁定改写: 未经 owner 审阅的套件不作门, 其结果只可记 provisional 作观察, 不得据以 ship; 合规清单补「`pass provisional` 不得 ship」。若 owner 裁交互 (B), 再换成 (B) 的写法。
3. D2 的「见 OQ-7」「按 OQ-7 的审阅要求」改为写出裁定内容; 加一条任务 (或并入 T1–T3): 「按 OQ-7 / OQ-9 裁定改写 SOT §2 自主条款、手册 §4b 套件审阅句与 SOT §4.1 provisional 句; 裁定与推荐不同 ⇒ 回 A.1 改写并复审」。
4. 写明验证完成的判据: D5.6 那张 issue 关闭时, 同步改写 SOT §6 第三条与 §2 自主条款。

### Finding 2: v5 的三处新规范文字没有 SC 锁

对 SC-1 到 SC-10 逐条扫描, 含 `unattended` / S_FAIL / 自主 / GLM / Claude 模型 / OQ-7 / OQ-9 的一条都没有 (记录 13)。反事实:

- T1 落地时漏掉 SOT 自主条款, 或漏掉 CLAUDE.md 的「自主运行时的处置见 SOT §2」: 核心句、「照跑场景 1」「另须跑场景 4b」都还在同一行, SC-1 仍绿;
- T5 漏掉 D6 尾句「场景 4b 只在 Claude 模型上实测过 ……」: SC-7 只查「三个已知缺陷」「两个已知缺陷」计数语与版本行, 仍绿; 就算整条第三条漏掉、只把「两个」改成「三个」, SC-7 也绿。

这与 R4 聚合第 5、7 条 (v4 的实质修复没有能变红的 SC) 是同一类问题: v5 给 SC-1 / SC-9 补了锁, 但它为 R4 两条 major 新加的文字又没有锁。这几句正是 R4 两条 major 的修复本体, 转录时漏掉而验收查不出来, 等于 major 的修复没有机械保证, 所以放在 Phase B 前改。**修法**: 按行断言 —— SOT 含核心句的那一行须含 `unattended` 与 S_FAIL (Finding 1 改写后按定稿关键词); CLAUDE.md 那一行须含「自主运行时的处置见 SOT §2」; SOT §6 须有一行同时含「地板守卫」「未穷举」「Claude 模型」「GLM」。每条都过一遍反事实 (删掉该句是否转红)。

### Finding 3: D6 仍引 RESULT v4

`proposal.md` 第 101 行 (D6 第三条) 写「基线: …… RESULT.md` v4, 写入时附当时的版本号与提交 SHA」。v5 把其余七处 RESULT 引用都改成了 v5 (抬头、Why、D2 两处、D3 第 4 行、Impact、T8), 只漏了这一处 (记录 14)。它不只是版本号旧: RESULT v4 的「已知局限」原文是「地板守卫判红的只有两类破坏」, v5 为回应 R4 聚合第 4 条改成了「已验证判红的破坏有两类 (未穷举)」, 而 D6 这句本身写的是「(未穷举)」。T5 若照抄「v4」并配上 v4 的提交 SHA, SOT 就会引用一份与自己措辞相反的版本。「写入时附当时的版本号」与写死的「v4」互相矛盾, 实施者两种读法都可能。漏改的根源是抬头的重核清单「RESULT 再修订须同步重核本文 §Why 与 §D2 §D3」不含 D6 (Impact、OQ-3 / OQ-7 / OQ-9 的时长与成本、T8 也引 RESULT)。**修法**: D6 改为「RESULT.md v5」, 或只写「写入时引用 RESULT.md 当时的版本号与提交 SHA」; 抬头重核清单补齐 D6、Impact、OQ-3 / OQ-7 / OQ-9、T8。

## 事实核实结论 (任务 2)

| v5 新写入的事实 | 结论 | 依据 |
|---|---|---|
| handoff 里 aria-runner-bot 只与 023236f2 (23 份) / bfe8285d (7 份) 配对 | 成立 | 记录 1 |
| 这两个是开发容器 | 成立: bfe8285d 就是本席所在的 dev-claude2; 023236f2 在 07-05 到 09-13 共 23 份 handoff 里用同一个持久 uuid, 两个提交身份都用过, 不可能是按次派发、提交身份写死的 Nomad runner | 记录 1、4、5 |
| aria-runner-bot 是 AI 会话共用的机器提交身份 (§2.3.9) | 事实成立; 但 §2.3.9 字面只说「AI runner 会话 (无人值守容器、CI bot 等自动执行体)」, 交互会话也用它来自 handoff 实证, 不来自 §2.3.9 原文 | 记录 6 (观察 3) |
| v1.64.0 (`124d311`) 对应开发容器里的交互会话 | 成立 | 记录 3 |
| v1.70.0 (`bae4ad8`) 对应开发容器里的交互会话 | 成立 | 记录 4 |
| ⇒ 自主流水线 (AD10) 至今没改过 aria-plugin 任何文件 | 结论成立; v5 只拿两例抽查支撑, 更强的两条证据没写 (bot 在 aria-plugin 的 33 次提交日期全落在 handoff 配对覆盖期内; M6 输入投递至今未合入) | 记录 2、7 (观察 4) |
| aria-runner 镜像只预装 aria-plugin, 没有 skill-creator | 成立 (所有 origin 分支 `docker/` 下 0 命中) | 记录 7 |
| `unattended` 键既有约定原话「有没有人可问是**配置事实**」 | 成立, 逐字 | 记录 8 |
| 默认 `false` = 交互模式; `#196` 缺失时静默回落 `false` | 成立 (`#196` open) | 记录 8 |
| AD10 回滚路径 Level 2 原文 | 成立; 引号内把原文的括号改成了逗号 (观察 5) | 记录 9 |
| AD5「任意状态都可进入 S_FAIL」 | 成立, 逐字 | 记录 9 |
| (C)「需要改时任务进 S_FAIL …… 交给交互模式处理」 | 部分成立: S_FAIL 由 Layer 1 升级, 默认处置是自动重试, 要 owner 主动把 issue 移出自动派发才算「交给交互模式」 | 记录 9 (观察 1) |
| RESULT v5 逐字引用预登记原文 | 成立 (原文的逐字子串) | 记录 15 |
| SC-1 新增断言: v3 红 / v5 绿 | 成立 | 记录 11 |
| SC-9 按行拆 | 成立 | 记录 12 |

## 新引入问题检查 (任务 3)

- **SOT 自主条款与 OQ-7 推荐 (C)、OQ-9**: 验证之前那一段与 OQ-9 推荐、§Impact 代价句一致; 验证之后那一段与 (C) 不一致 → Finding 1 第 1 点。
- **「依 OQ-7 / OQ-9 裁定, 裁定不同则随之改」**: 见 Finding 1 末段。
- **D5 第 6 项与 T6 / SC-6 / 交付物**: 抬头「代码落点」「三张新 issue」、T6「开三张 issue (D5.2 / D5.3 / D5.6)」、SC-6「D5.2 / D5.3 / D5.6 三张 issue 存在」、Key Deliverables「三张新 issue (D5.2, D5.3, D5.6)」四处对齐 (记录 17)。缺两点: D5.6 关闭与 SOT 改写的联动没写 (并入 Finding 1 修法第 4 条); SC-6 没说新 issue 编号记在哪, 验收者无从 `GET` (观察 11, 自 v4 起就有)。
- **v5 其他改动**: D2 补全四个短语 (与 RESULT v5 表一致)、D6 / RESULT「未穷举」、作废第二情形、OQ-9 须在 Luxeno 路由环境跑、SC-1、SC-9、§3 边界注、D4 补 scenario1 —— 逐条对过, 没有新冲突。唯一漏改是 D6 的「v4」→ Finding 3。

## 观察 (不进收敛比较键, 不影响 vote)

1. **S_FAIL 的实际语义**: `layer-boundary-contract.md` 写明「Layer 1 also owns the failure escalation path (→S_FAIL)」, Layer 2 只能以失败结束; §4 列的六种 Layer 2 失败模式里没有「按规则拒做」, 拒做大概率以 `execution_crash` (非零退出) 上报; S_FAIL 的默认处置是「Acknowledge and let Layer 1 auto-retry (default)」, 重派后执行者会再撞同一条规则。所以 (C) 的代价「自主模式在这类改动上停下来」应写实: 每次触发一条 Feishu 告警, 默认自动重试, 须 owner 把该 issue 移出自动派发才真正停下。SOT 条款宜从 Layer 2 视角写 (「以失败结束任务并写明原因, 不应重试」), 见 Finding 1 修法第 1 条。
2. **(D) 同样跑不起来**: (D)「之后自主模式照常按 4b 判门」与 (B) 一样依赖 runner 里有 skill-creator, 还依赖 OQ-9 的验证; (B) 标了「当前跑不起来」, (D) 没标。推荐理由里「再升级为 (B) 或 (D)」两条都要先改 runner 镜像 (aria-orchestrator 改动), 宜写明。
3. **§2.3.9 的引用范围**: §2.3.9 原文针对「AI runner 会话 (无人值守容器、CI bot 等自动执行体)」, 要点是「操作者可追溯性由 `<container-id>` + handoff 正文承担, 不靠 `<owner>` 段区分「谁在按键盘」」。v5 要用的正是这一点 (提交身份不说明有没有人在场); 「交互会话也用 aria-runner-bot」是 handoff 实证, 不是 §2.3.9 的规定。建议写成「机器提交身份 (§2.3.9: 操作者不由提交身份区分); 两个开发容器里的交互会话也用它 (handoff 实证)」。这处宽泛化源自我 R4 的转述 (「AI 会话的 git 提交身份统一为机器身份」), 在此勘正。
4. **全称结论的支撑与语料里的相反说法**: 「⇒ 自主流水线至今没有改过 aria-plugin 的任何文件」只靠两例抽查。更强的支撑有两条, 建议写进去: bot 在 aria-plugin 的 33 次提交日期为 07-05 到 09-06, 全落在 handoff 配对覆盖期 (07-05 到 09-13) 内; M6 输入投递分支仍未合入 aria-orchestrator `origin/master`。另, 语料里有一条相反说法: `2026-07-11-secret-guard-twin-reconcile-v1.55.3.md` (由本机 `simonfish/bfe8285d` 所写) 第 21 行称 023236f2 为「Aria 2.0 Layer 2 自主运行时容器」, 与 memory `project_aria_runner_bot_autonomous_same_repo_work` 是同一说法 (R4 观察 12); 它引的 `759b980` / `5fe9562` 是主仓的 handoff 与 spec 文档提交, 不在 aria-plugin。v5 的更正是对的, 但没提这条旧说法, 读到旧 handoff 的人会困惑。建议 owner 复核该 memory 与该 handoff (本席只审不改)。
5. **(E) 引文标点**: AD10 原文「在 S5_REVIEWING 中间插入一个 optional human gate (只对高风险 issue 触发)」, proposal 在「」内写成「……human gate, 只对高风险 issue 触发」。引号内宜逐字。
6. **模型范围不对称**: SOT 条款的验证条件是按模型的 (「于其所用模型上」), 却只挂在自主模式上; 交互会话若用非 Claude 模型, 照样按只在 Claude 上验证过的阈值跑 4b。建议把「所用模型未经验证」写成与运行模式无关的条件, 或至少在 §6 那句里点明。
7. **R4 第 3 条论证里的余项**: D4 合规清单仍没有「`description_changed: yes` 时 `decision_table_row` 须为 2」; SC-10 仍只锁 §3 边界注前半句「description hunk 不走本节」, 后半句改回 v4 的「场景 4b 义务」也不转红。
8. **`#196` 是本条生效的前置**: Aria 的 `.aria/config.json` 入库、所有会话共用 (记录 8), 在其中写 `unattended: true` 会把交互会话一并翻过去, 所以这个键只能经 `#196` 的 env 三腿契约 (或镜像内单独的配置) 在 runner 里生效。v5 已写「`#196` 修好前, 自主模式的这条规则无法保证生效」, 可以更直白地写成「前置条件」。回落 `false` 时 runner 会按交互模式处理, 等 owner 审套件, 而容器里没人可问; 结果仍是不 ship, 但失败形态是卡住或超时, 不是明确的 S_FAIL。
9. **R4 观察 14 (b) 仍在**: T1–T3、T5 没声明依赖 OQ-5 / OQ-6 的裁定 (OQ-5 若裁为 issue 字面路径, T1 新句整句作废)。v5 只给自主条款加了依赖注记, 还放在转录格里。建议与 Finding 1 修法第 3 条合成一段「裁定依赖」, 覆盖 OQ-5 / 6 / 7 / 9。
10. **源头文档的状态名漂移 (不属本 Spec)**: AD10 与 CLAUDE.md 用 `S7_AWAITING_MERGE` / `S5_REVIEWING`, AD5 (2026-04-28 修订) 的 10 状态是 `S5_AWAIT` / `S6_REVIEW` / `S7_HUMAN_GATE`。proposal 如实引 AD10, 没问题; 规范句只用 S_FAIL (两处一致), 也没问题。orchestrator 文档侧可另行对齐。
11. **SC-6 的可检查性**: 「三张 issue 存在 (`forgejo GET` 返回 200)」没说编号记在哪 (如 `#211` 回帖或 proposal 本身), 验收者要先去搜。自 v4 起就有, D5.6 加入后同样适用。

## Verdict

PASS_WITH_WARNINGS —— critical 0 / major 1 / minor 2。

我席 R4 的 4 条全部 closed: 自主模式有了验证前的 fail-closed 条款和代价, 「只在 Claude 上验证过」进了 SOT §6 并开 issue 追踪; 自主模式栏的事实依据更正后逐项核实成立, 运行模式判据改用配置事实并登记了 `#196` 缺口, 选项写全; 两条 minor 的文字与 SC 都改对了。v5 新写入的事实本轮全部机械核实: 23 / 7 配对、两次发版对应交互会话、runner 无 skill-creator、`unattended` 原话、AD10 与 AD5 原文都对得上。

仍投 REVISE, 原因是一条新发现的 major: 自主模式推荐从 (B) 改成 (C) 之后, 三处要转录的规范句没跟上 —— SOT 条款只编码了 OQ-9 那一半, D4 还保留 (B) 的 provisional 并放行 ship, 裁定落点是转录后会悬空的 OQ 编号。两条 minor (新文字没有 SC 锁、D6 引旧版) 都是要转录的文本, 放在 Phase B 前改。全部修改只动文字, 不用重跑基线。

按 R4 聚合登记, 本轮结构上不可能收敛, 跑完即进降级策略由 owner 裁。Finding 1 的修法取决于 OQ-7 / OQ-9 的裁定: owner 做降级裁定时若一并裁这两项, 三处规范句可以一次定稿。

## Vote

REVISE

## 数据核实记录

核实方式: 直接读原始文件或 git 对象重算, 不拿 proposal / RESULT 里的数字当依据。脚本与 diff 放在 scratchpad (`sc_check.py`、`v4v5.diff`)。

1. **handoff 配对**: `grep -rhoE "owner-container: *aria-runner-bot/[0-9a-z-]+" docs/handoff/*.md | sort | uniq -c` 得 23 个 `aria-runner-bot/023236f2`、7 个 `aria-runner-bot/bfe8285d`; 按文件数 (`grep -lE`) 同为 23 / 7。放宽到正文任意位置 (`aria-runner-bot/[0-9a-z-]+`) 仍只有这两个 ID (36 / 24 处)。其余提到 aria-runner-bot 的正文行 (提交作者说明、协作者权限、机器账号名等) 没有与第三个容器配对。含该 owner-container 的最早一份是 `2026-07-05-runtime-probe-spec-approved-post-spec-converged.md`, 最晚一份是 `2026-09-13-session-close-l2-rulings-reconciled-tracks-handed-over.md`。
2. **aria-plugin 的 bot 提交**: `git -C aria log --all --author=aria-runner-bot` 共 33 个; 日期最早 2026-07-05 (`70adcbc`), 最晚 2026-09-06 (`5fbb974` / `bae4ad8` / `f2e4231`), 全部落在记录 1 的覆盖期内。
3. **v1.64.0 `124d311`**: author 与 committer 均为 aria-runner-bot, 2026-07-22, 只改五个发版文件, `plugin.json` 为 1.64.0。`2026-07-22-issue113-ship-v1.64.0-and-rule6-third-row.md` frontmatter 为 `aria-runner-bot/023236f2`; 提交表一行为「aria | `e3d54f3` → `bb005f4` → `124d311` → `3694871` (merge) | …… v1.64.0 release / 本地 --no-ff 合并」; 交互痕迹: 「owner 说「与远程保持同步」, 我解读成推 ……」「owner 要求把 Rule #8 豁免写进 config」「本地 `--no-ff` 合并 (主仓约束 1 禁服务端合并)」以及「owner 复议项」一节。
4. **v1.70.0 `bae4ad8`**: aria-runner-bot, 2026-09-06, `plugin.json` 为 1.70.0。`2026-09-06-owner-container-identity-key-shipped-v1.70.0-archived.md` frontmatter 为 `aria-runner-bot/bfe8285d`; C 行「owner 裁定 D5 MINOR → v1.70.0 五文件 bump (`bae4ad8`); aria 本地 `--no-ff` merge → `0545f86` + tag v1.70.0」; 一句话段「owner 裁定 D-0 a / D-1 a / D-2 a / D-3 a / D5 MINOR」「owner 两次加轮」「PR #197 (owner 授权)」; §0 第 4 条「双子星 `simonfish/023236f2`」; 同文件记录 `023236f2` 与 `bfe8285d` 各自用过 aria-runner-bot 与 simonfish 两个身份。
5. **本机身份**: hostname `dev-claude2`; `~/.aria/container-id` 的 uuid 前缀 `bfe8285d`; 当前 `git config user.email` 的 local-part 为 `simonfish`。`2026-07-11-secret-guard-twin-reconcile-v1.55.3.md` 的 frontmatter 为 `simonfish/bfe8285d` (即本机所写), 第 21 行称 023236f2 为「Aria 2.0 Layer 2 自主运行时容器」; 它引的 `759b980` / `5fe9562` 用 `cat-file` 查, 只在主仓, 分别是 handoff 与 spec 文档提交 (2026-07-11, aria-runner-bot)。
6. **§2.3.9 原文** (`standards/conventions/session-handoff.md` 第 266–273 行): 「AI runner 会话 (无人值守容器、CI bot 等自动执行体) 的 git 提交身份统一为机器身份 …… 操作者可追溯性由 `<container-id>` (§2.3.1) + handoff 正文承担, 不靠 `<owner>` 段区分「谁在按键盘」」。
7. **runner 镜像**: `aria-orchestrator/docker/aria-runner/Dockerfile` 的安装步骤只有 apt 包、`npm install -g @anthropic-ai/claude-code@latest`、`COPY aria/ /opt/aria-plugin/`, 另设 `ENV GIT_AUTHOR_NAME="aria-runner-bot"`; 在 Dockerfile / entrypoint.sh / modes / lib / prompts 里 grep `skill-creator|plugin install|marketplace|enabledPlugins|plugin-dir|setting-sources|unattended`, 只有 Dockerfile 第 60 行一句注释; 对 aria-orchestrator 全部 `origin/*` 分支做 `git grep -il skill-creator -- docker/`, 均 0 命中; `aria/skills` 下只有 agent-creator, 没有 skill-creator。`git -C aria-orchestrator merge-base --is-ancestor origin/feature/m6-dispatch-input-delivery origin/master` 为否。
8. **`unattended`**: `aria/skills/phase-a-planner/SKILL.md` 第 129–131 行「`state_scanner.coordination.unattended == true` ⇒ 零 `AskUserQuestion` …… 不得以「AskUserQuestion 现在能不能用」做运行期推断 —— 有没有人可问是**配置事实**」, 与 proposal 引文逐字相符; `aria/skills/config-loader/SKILL.md` 第 147–150 行: `default: false`, 「取值路径: aria-runner 容器镜像内的 .aria/config.json (Layer 2 自主运行时)」。Aria `.aria/config.json` 的 coordination 块只有 `enabled: true` / `mode: advisory`, 没有 `unattended`, 且该文件入库 (`git ls-files` 可见)。`forgejo GET /repos/10CG/Aria/issues/196`: state open, 正文含「缺 import 会静默 fallback 到 `false`」。
9. **AD10 / AD5 / 边界契约**: `architecture-decisions.md` AD10 决策段「只保留 1 个人类审批 gate, 位置在 S7_AWAITING_MERGE」, 选型理由第 4 条「未来运行稳定后可增加 gate (往 2 gate 退化)」, 回滚路径「Level 2: 在 S5_REVIEWING 中间插入一个 optional human gate (只对高风险 issue 触发)」; AD5 决策段「S_FAIL 作为 universal sink, 可从任意状态进入, 并触发 replay / retry / escalate 决策」, 选型理由第 2 条「任意状态都可进入 S_FAIL」。`layer-boundary-contract.md` 第 163 行「Layer 1 also owns the failure escalation path (→S_FAIL)」; §4 六种 Layer 2 失败模式 (dispatch_timeout / execution_crash / stuck_s5_await / cost_alarm / state_mismatch / schema_violation), S_FAIL handling「Acknowledge and let Layer 1 auto-retry (default)」。standards 里 `autonomous/decision-autonomy-matrix.md` 已在用 S_FAIL (第 54、171 行), 规范句写 S_FAIL 有先例。
10. **三处旧句**: `grep -cF` 在 CLAUDE.md / SOT / 手册各 1; SOT「两个已知缺陷」1 次, 版本行为 `**Version**: 1.0.0`。
11. **SC-1 反事实** (Python 对 `git show <rev>:proposal.md` 的 D1 表三行取新句格): `0c41e53` (v3) 三行「另须跑场景 4b」全为假, 手册行「照跑场景 1」也为假 ⇒ SC-1 转红; `e822829` (v4) 与 `f169a0b` (v5) 三行三项全真 ⇒ 绿。与 proposal「按 v3 旧新句落地时这两串缺一, 本条转红」相符。
12. **SC-9 反事实** (对 v5 §D2 各行): 原文四项 (≤ 5/10 / 连续 2 轮 / fail 与不得 ship 同行 / 作废与不得 ship 同行) 全真; 删「fail 的后果」行 ⇒ 第三项假; 删作废行 ⇒ 第四项假 (「连续 2 轮」也随之假)。含这两对的行各只有一行。
13. **SC 覆盖面**: SC-1 到 SC-10 中含 `unattended` / S_FAIL / 自主 / GLM / Claude 模型 / OQ-7 / OQ-9 的 0 条; D5.6 只出现在 SC-6。SC-7 只查计数语、版本行与手册「边界四条」, 不查 §6 第三条内容。
14. **v5 里的「v4」**: Python 扫出 5 处 —— 第 4 行 (状态史)、第 101 行 (D6 引 RESULT v4, 陈旧)、第 117 行 (「v1–v4 `claude-fable-5-1`」)、第 154 行 (「v4 曾把」)、第 161 行 (「v4 已写入」); 只有第 101 行是陈旧的版本引用。`git diff e822829 f169a0b` 中 RESULT 已知局限由「地板守卫判红的只有两类破坏 (结论 2)」改为「已验证判红的破坏有两类 (结论 2, 未穷举)」。抬头重核清单原文「RESULT 再修订须同步重核本文 §Why 与 §D2 §D3」。
15. **预登记引文**: `v5-mildcreep-opus5/PREREGISTRATION.md` 第 17 行含「这是对 §D2「只承诺两类破坏」局限的实证确认, 不是守卫失效的证据」, RESULT v5 的引文是它的逐字子串 (截在「(守卫的定义就是看套件里的近似误触)」之前)。
16. **OQ-7 指代与 provisional** (Python 按行取): 第 39 行 SOT 新句格「(依 OQ-7 / OQ-9 裁定, 裁定不同则随之改)」; 第 54 行 D2「按 OQ-7 的审阅要求」; 第 56 行 D2「新套件是否须 owner 审阅后才能作门, 见 OQ-7」; 第 84 行 D4「套件未经 owner 审阅时 (OQ-7), `scenario4b` 结果后缀 provisional」; 第 153 行 OQ-7 交互 (B)「结果带 provisional 后缀 (D4)」。T1 原文「三处 D1 新句落地 (逐字)」。v4 → v5 diff: OQ-7 自主推荐由「(B) 且审阅并入 S7」改为「(C)」, D4 的 provisional 行未动。
17. **D5.6 对齐**: 抬头「代码落点」「三张新 issue」、T6、SC-6、Key Deliverables 四处都写三张, 并点名 D5.6。

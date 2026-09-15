---
checkpoint: post_spec
mode: convergence
rounds: 6
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-15T11:22:56.304Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [tech-lead]
---

# post_spec Round 6 — tech-lead 席 (被审 SHA c3a5903, v7)

> 只审不改: 除本报告外没写任何仓库文件, 脚本与 diff 放在 scratchpad (`desc_changes.py` / `desc_detail.py` / `sc_selfcheck_v7.py` / `v6v7.diff` / `v5v7.diff`)。独立性: 没读任何 R6 报告 (开审时目录里只有 R1–R5); 读了 R5 聚合报告 (含 owner 降级裁定) 与本席 R5 报告; 对 R1–R5 共 30 份报告只做了关键词检索, 确认「新增 skill」「runner 自动提交」两个题目往轮没人提过 (记录 16)。远端只做了一次只读查询 (`forgejo GET /repos/10CG/Aria/issues/196`), 没有 fetch / push。
>
> **勘正**: 本席 R5 观察 1 写「S_FAIL 的默认处置是自动重试, 重派后执行者会再撞同一条规则」, 只依据 `layer-boundary-contract.md`, 没核代码。本轮读了代码, 该说法不成立 (Finding 3)。v7 §Impact 与 D5.6 的相应表述部分来自这条观察, 责任在本席。

## R5 对账

我席 R5 共 3 条 (major 1 / minor 2)。结果: **closed 2 / partially 1 / open 0**。

| R5 条 | 严重度 | 判定 | v7 落点与核实 |
|---|---|---|---|
| 1 自主推荐由 (B) 改 (C) 后规范文本没跟上: SOT 自主条款只编码「先验证」一半、验证后整句失效; D4 无条件保留 provisional 并放行 ship; 「依 OQ-7 / OQ-9」「见 OQ-7」转录后悬空 | major | **closed** | 三点逐一落地。(1) D1 表 SOT 行把自主条款改成无条件禁令「自主运行时 (`state_scanner.coordination.unattended == true`) 不做 description 改动: ……」, 没有「验证之前」这类会自动失效的条件, 「验证后自建未审套件、跑出 pass provisional 进 S7」的路径不再存在。(2) D4 模板值域去掉 provisional, 合规条款「所用套件未经 owner 审阅 ⇒ 不合规」对齐推荐 (A); (B) 的改法挪进标明「不转录」的条件段。(3) 「依 OQ-7 / OQ-9」「见 OQ-7」「(OQ-7)」都已移出转录格, D2 直接写「新套件须经 owner 审阅后才能作门」; SC-11 扩到五个模式, 对全部转录块自检 0 命中 (记录 9)。余项只到观察层: (B) 分支的条件段只列了 SOT §4.1, 没列 D2 那句 (观察 6)。禁令新措辞自己带出的问题是新问题, 单列 Finding 1, 不算本条残留。 |
| 2 v5 新加的三处规范文字 (SOT 自主条款 / CLAUDE.md「自主运行时的处置见 SOT §2」/ D6「只在 Claude 模型上实测过」) 没有 SC 能变红 | minor | **closed** | SC-12 按行锁住三处: SOT 含核心句那一行须含「unattended == true」「不做 description 改动」「放弃整个任务」「写明」; CLAUDE.md `grep -cF "自主运行时的处置见 SOT §2"` = 1; SOT `grep -cF "只在 Claude 模型上实测过"` = 1。这几串只出现在对应新句里, 删句即转红; 对 v7 转录文本自检, 各串都在 (记录 9)。余项: SC-12 没锁「不提交任何改动」, §6 第三条其余内容仍无 SC (观察 8)。 |
| 3 D6 仍引「RESULT.md v4」; 抬头重核清单不含 D6 | minor | **partially** | 引用已改为 v6, v7 全文的 RESULT 引用都统一为 v6 (抬头 / Why / D2 两处 / D3 第 4 行 / D6 / Impact / T8)。重核清单仍只写「§Why 与 §D2 §D3」, D6 仍把「v6」写死又要求「写入时附当时的版本号」—— 漏改的根源没补, 眼下没有实际漂移 (观察 7)。 |

**收窄是否让 R5 那条 major 不再成立 (任务 1)**: 不再成立, 而且不是搬家。那条 major 的实质是**规范文本本身的缺陷**: 转录后的句子只编码了推荐规则的一半, 条件一满足就悄悄失效, 失效后执行者会自建未审套件、凭 pass provisional 放行 —— 执行者会做错事。v7 的禁令是自足的: 没有失效条件, 失败形态是「不做」而不是「做错」; 以后要放开, 必须由 D5.6 的跟进 spec 改写 SOT §2 并过它自己的审计, 不存在「条件悄悄成立」这一步。搬进 D5.6 的是设计工作 (自主模式何时可以改、谁审套件、GLM 上验证), 这是正当的延后: 延后期间规则 fail-closed, 代价在 §Impact 写明。要说清的一点: 收窄并没有让「自主模式这条线」整体变干净 —— 禁令的依据链与 Impact 的代价描述里各有一处与代码不符 (Finding 1、Finding 3), 那是为收窄新写的文字带出的新问题。

## Findings

- [major] architecture/proposal.md §D1 (SOT §2 自主禁令及其依据) (issue): 「放弃整个任务、不提交任何改动 ⇒ 必进 S_FAIL」不成立: initial.sh Step 10 会替 Claude 提交工作区残留改动并开 PR, 断言命中即 SUCCESS 进 S6; changes / redo 模式残留 diff 提交推送成功即 PASS 退 0。照字面执行禁令, 正落进它要防的「部分交付按成功推进」。
- [major] testing/proposal.md §D2 (同批参照臂) (issue): v6 新加的参照臂要求改动前 description 在同一套件过门, 否则作废、不得 ship; 按「fail 的后果」第 (2) 条改套件划分后旧 description 必然过不了门; 新增 skill 没有改动前 description (是否属 4b 也未界定); 修复现行已坏的 description 同样作废。
- [major] documentation/proposal.md §Impact+§D5.6 (issue): 「放弃后记为 container_crash 并默认自动重试、反复告警」与代码不符: container_crash 不在可重试集合, 失败分析默认关闭, 心跳扫描不重派, tick 标 S_FAIL 不发告警 ⇒ 默认是无告警的终态; Impact 代价、D5.6 已知缺口与 owner 目标设计的前提都失实。
- [minor] documentation/proposal.md §D5 (第 7 项残留) (issue): D5 第 7 项仍要求另开一张 10CG/Aria issue, 与 owner「并入唯一一张跟进 issue」及 T6 / SC-6 / Key Deliverables / 抬头的「三张」冲突; 进 Phase B 前须删去或并入 D5.6。

## Findings 论证

### Finding 1: runner 会替 Claude 提交工作区里的残留改动

v7 §D1 的依据句 (原文): 「runner (`initial.sh`) 只有结果为 SUCCESS 时以 0 退出, 编排器 `_handle_s5_await` 只看退出码、非零即进 S_FAIL ⇒ 整单不提交必进 S_FAIL, 部分跳过则可能按 SUCCESS 推进、无人察觉」。两个前提都对 (记录 2、5), 推论不对:

- initial 模式只在「工作区干净且没有新提交」时判 `CLAUDE_NO_OP` (Step 8)。工作区有未提交改动时, Step 10 由 runner 自己 `git add -A` + `git commit` (第 415 行注释原文「若 claude 没 commit 但 working tree 有 changes, runner 补 stage+commit」), 接着推送、开 PR; 只要 issue YAML 的 file_touched / diff_contains 断言命中, 结果就是 SUCCESS, 退 0, 编排器推进到 S6_REVIEW, 再到 S7 (记录 2)。
- changes / redo 两个 rework 模式更直接: `git add -A` 后暂存区非空就提交、推送, 写 PASS 并退 0, 不看断言 (记录 4)。v7 依据句只引了 initial.sh。

这个漏洞恰好在执行者照字面遵守禁令时出现。典型顺序是先做实现, 改 SKILL.md 时才发现要动 description, 此时工作区已有改动。禁令只说「不提交任何改动」, Claude 不提交就算遵守; runner 自己的提示词也只说「do NOT make a commit with partial work」(记录 3), 都没要求撤销。于是 runner 替它把半成品提交并开 PR —— 这正是 D1 选「放弃整个任务」时要排除的「部分跳过按 SUCCESS 推进」。D5.6 的已知缺口里没有这一条, SC-12 也没锁「不提交任何改动」这半句。

**修法 (纯文字)**:
1. SOT §2 禁令改为「任务需要改 description 时放弃整个任务: 撤销本任务已做的全部改动 (工作区不留未提交改动, 分支不留新提交), 并在最终消息里写明是哪个 skill、为什么要改」。这句与具体运行时无关, 放在 SOT 合适。
2. D1 依据句补上 runner 自动提交这一步, 把推论限定为「工作区干净且无新提交时必进 S_FAIL」; 同时写明 rework 模式的退 0 条件是「有 diff 且推送成功」, 不是 SUCCESS。
3. D5.6 已知缺口加一条「runner 会提交工作区残留改动 (initial 模式 Step 10; changes / redo 模式任一 diff 即 PASS)」; 机械兜底 (例如放弃标记让 runner 拒绝自动提交) 属跟进 spec。
4. SC-12 加锁撤销改动那半句 (如「撤销」)。

更省的改法: D1 依据句整句删掉, 只留禁令本身 (禁令对不对不依赖依据句); 但禁令措辞仍须按第 1 条改。

### Finding 2: 同批参照臂与三种合法情形冲突

D2 原文: 「**同批参照臂**: 改动前的现行 description, 与被评 description、负控同批跑。参照臂过不了门 ⇒ 本轮作废, 不判被评 description。必须有它 ……」; 作废 ⇒「不得 ship」, 「连续 2 轮作废 ⇒ 升级 owner」。参照臂是 v6 为回应 R5 聚合第 2 条新加的 (记录 10), 目的只有一个: `run_eval.py` 把异常、超时记成「未触发」, 需要一个对照来识别环境故障。但写法同时要求「改动前的 description 在同一套件上过门」, 这第二层要求在三种合法情形下必然不满足:

1. **D2 自己规定的「fail 的后果」第 (2) 条**: 「若 fail 来自有意收窄或拓宽触发面 (套件原来的 should / should-not 划分已不符合新意图), 则先改套件 …… 再重跑」。以收窄为例: 旧 description 会触发话题 T, 新 description 有意不再触发; 套件按新意图把 T 类 query 从 should 改为 should-not; 重跑时参照臂 (旧 description) 照旧触发 T ⇒ should-not 的 trigger_rate ≥ 0.5 ⇒ 参照臂过不了门 ⇒ 作废。拓宽对称 (新话题的 query 改为 should, 旧 description 触发不了)。「修套件或环境后重跑」修不好 (套件与环境都没错), 两轮后升级 owner。唯一走得通的做法是删掉这些 query 而不是改标签, 文本没说。
2. **新增 skill**: 没有「改动前的现行 description」, 参照臂无从构造。它在不在 4b 范围, 文本也没定: D1 按 hunk 判 (「description hunk ⇒ 场景 1 另加场景 4b」), 新 SKILL.md 的 frontmatter 就是 description hunk; SOT §2 第四行「拿不准 …… 照跑」; D4 合规条款「`description_changed: yes` 而 `scenario4b` 为空、`not_required` 或 `n/a` ⇒ 不合规」。按这几条, 谨慎的执行者会去跑 4b, 却满足不了「必须有它」, 新增 skill 就 ship 不了。另一种读法 (CLAUDE.md 规则 #6 把「新增 Skill」与「改 description」列为不同触发, 手册新增 skill 走场景 2) 则不跑 4b。两种读法结果相反, 文本没挑。历史上新增 skill 的提交 (15 个) 比改已有 description 的提交 (7 个) 还多 (记录 8), 这是更常见的情形。
3. **修复现行已坏的 description**: 其余 41 个 skill 首次改 description 时要同批建套件; 若套件收了促成这次修改的 query (现行 description 正是漏了它们), 参照臂过不了门 ⇒ 作废。

**修法 (纯文字)**:
1. 把参照臂限定为环境对照: 只在「标签与改动前套件相同的 query」上判参照臂 (或参照臂跑改动前的套件版本), 在这部分过不了门才作废; 或者换成与本次改动无关的固定正控。
2. 写明新增 skill 的处理: 不在 4b 范围 (首个 description 随首个套件经 owner 审阅), 或在范围内、环境对照改用第 1 条的固定正控。这是范围裁定, 可并入 OQ 由 owner 定。
3. 首次建套件时写明: 地板守卫的套件描述改动前的触发面; 有意改变的触发面走「fail 的后果」第 (2) 条, 参照臂按第 1 条只看未改标签的部分。

### Finding 3: 「默认自动重试、反复告警」与代码相反

v7 §Impact: 「runner 开跑后碰到这类任务, 会被打进 S_FAIL (失败类型记为 `container_crash`) 并默认自动重试、反复告警, 直到 owner 手动阻止该 issue 自动派发 (`layer-boundary-contract.md` §S_FAIL handling)」; D5.6 已知缺口: 「放弃后的失败类型记为 `container_crash` 且默认自动重试」。「记为 container_crash」对, 其余与代码不符 (记录 6):

- tick 标 S_FAIL 的分支只调 `repo.mark_failed`, 不发告警; `tick_runner.py` 没有任何告警调用。reconciler 里「卡住 → S_FAIL + 告警」的 `_handle_fail` 处理的是卡在某个状态超时的行 (fail_detail 写 `stuck in {row.state}`), 由它自己标 S_FAIL 时才发告警; tick 已经标好的 S_FAIL 行不经过这里。
- 对已失败派发的唯一自动处理是 reconciler 的失败分析, 只在打开失败分析开关 (记录 6 所列环境变量) 时运行; 仓内没有任何作业配置打开它, M5 handoff 记为「owner 选择, 默认关」。
- 即使打开, 重试门要求失败类型属于 `{infrastructure, timeout}` 且 retry_count < 1 —— container_crash 永远不重试; LLM 判「重试」会被降为 notify_owner, 发一张卡; 判 abort 则什么也不发。卡里的原因由 GLM 根据 fail_detail 生成, 而 fail_detail 只有退出码和 alloc id。
- 心跳扫描对已有派发行的 issue 不再新建派发 (任何状态), 所以也谈不上「手动阻止自动派发」。

实际的默认行为是: 该派发静默停在 S_FAIL 终态, 不重试、不告警; Claude 写的「哪个 skill、为什么要改」只留在 runner 输出卷的 `claude.stream.jsonl` 里, 没人会看。方向与 Impact 写的「反复告警」相反, 而且更糟。

后果: (1) 给 owner 的代价描述是反的 (写的是吵, 实际是静); (2) D5.6 这条已知缺口会把跟进 spec 引去压制一个不存在的重试, 却漏掉真正的缺口 —— 默认无告警、原因不可见; (3) owner 目标设计里「新失败类型不自动重试」一项的事实前提不成立。硬前提本身仍然成立, 只是理由应是「无人察觉」(加上 Finding 1 的漏洞), 不是「反复告警」。

出处: 边界契约 §S_FAIL handling 写「Immediate Feishu alert」「auto-retry (default)」, 与代码不一致 (记录 7); 本席 R5 观察 1 转述了契约文档而没核代码。

**修法 (纯文字)**: §Impact 与 D5.6 按代码改写, 例如「放弃后进 S_FAIL(container_crash), 这是终态: 不自动重试; 默认也不告警 (失败分析默认关闭; 打开后至多一张通知卡, 卡里没有 Claude 写的原因); 放弃原因只留在 runner 输出卷」; D5.6 已知缺口把「默认自动重试」换成「默认无告警、原因不可见」; owner 目标设计的原话不动, 在 D5.6 旁注这一项的现状事实, 请 owner 确认是否仍保留该项。引用编排器行为一律以代码为准。

### Finding 4: D5 第 7 项没有随收窄删除

v6→v7 diff 里, T6、SC-6、Key Deliverables、抬头「代码落点」都由四张 issue 改成三张 (D5.2 / D5.3 / D5.6), 但 D5 第 7 项「开 `10CG/Aria` issue「编排器不消费 runner 结果枚举: 部分跳过的改动会按 SUCCESS 推进」」是 diff 的上下文行, 原样保留 (记录 1、10)。执行者照 D5 会开第四张, 与 owner 裁定「与全部已知缺口并入唯一一张跟进 issue」相反, SC-6 也验不到; 照 T6 做, 这一项就成了死文字。D5.6 的已知缺口已含「编排器目前不读 runner 的结果枚举」, 缺的只是「部分交付会按 SUCCESS 推进」这半句。**修法**: 删去第 7 项, 把这半句 (连同 Finding 1 的自动提交) 并入 D5.6 的已知缺口。它直接违背一项 owner 裁定, 所以列为进 Phase B 前必改的 minor。

## 收窄是否站得住 (任务 2)

### (a) 禁令在两种模式下能否无歧义执行

- **交互模式**: 条件 `unattended == true` 为假, 禁令不适用, 执行者只按通用规则 (场景 1 + 4b + rule6_note), 无歧义。CLAUDE.md 新句的「自主运行时的处置见 SOT §2」只是指针。
- **自主模式**: 两处歧义。一是「不提交」与「不留改动」之别 (Finding 1); 二是新增 skill 算不算「description 改动」, 与 Finding 2 情形 2 是同一个问题, 禁令同样没说。

依据句与代码逐项对照 (记录 2、4、5、6):

| v7 依据 | 代码实情 | 判定 |
|---|---|---|
| runner 只有结果为 SUCCESS 时以 0 退出 | initial 模式成立 (591–596 行); changes / redo 模式在「有 diff 且提交推送成功」时写 PASS 退 0, 不看断言 | initial 成立; rework 模式的退 0 条件不是 SUCCESS |
| `_handle_s5_await` 只看退出码、非零即 S_FAIL | alloc terminated 时 0 → S6_REVIEW, 非 0 → S_FAIL(container_crash); 另有心跳超时、lost 两条也进 S_FAIL | 成立 |
| 退出码原样传给 Nomad | entrypoint 用 `exec` 调模式脚本; Nomad 作业 `restart attempts = 0`, 不在任务层重跑 | 成立 |
| 整单不提交必进 S_FAIL | 工作区干净且无新提交时成立 (Step 8 判 CLAUDE_NO_OP, 退 1); 工作区有残留时 runner 替 Claude 提交, 可达 SUCCESS | **不成立** → Finding 1 |
| 失败类型记为 container_crash | 与代码一致 | 成立 |
| 默认自动重试、反复告警 | container_crash 不可重试; 失败分析默认关闭; tick 标 S_FAIL 不告警 | **不成立** → Finding 3 |

### (b) 移出的内容是否都进了 D5.6

| v6 原内容 | v7 去向 | 判定 |
|---|---|---|
| OQ-7 自主栏的选项 (B) 并入 S7 / (D) 离线批量预审 / (E) AD10 回滚路径 Level 2 | D5.6「自主模式下新套件由谁审 (可选做法: ……)」 | 进了; 各项代价没带 (不影响本 Spec 执行) |
| (B) 当前跑不起来 (runner 镜像无 skill-creator) | D5.6 已知缺口 | 进了 |
| (C) 的机制说明 | D1 依据句 (压缩) + D5.6「编排器不读结果枚举与 Claude 的说明」 | 进了, 但带着两处与代码不符 (Finding 1、3); 「靠 Layer 2 遵守指令、不是机械保障」一句丢了 (观察 5) |
| 运行模式怎么判 + `#196` | D1「禁令以 unattended 为准」+ D5.6 已知缺口 | 进了; 「`#196` 修好前禁令在 runner 里不会触发」这个后果没写 (观察 3) |
| OQ-9 在 GLM 上先验证 | D5.6「只在 Claude 模型上实测过, GLM 未验证」+ SOT §6 第三条 | 进了; 「须在 Layer 2 实际的 Luxeno 路由环境里跑」这条约束与做法丢了 (观察 4) |
| D5.7 单独成单 | **没有移出**, 原样留在 D5 第 7 项 | Finding 4 |
| 事实依据 (bot 身份、87 个 PR 均由 simonfish 发起) | 删除 | 是推荐 (C) 的理由, 推荐已不存在, 删除合理 |

结论: 丢掉的几条都不会让规则执行者现在做错事 —— 禁令 fail-closed, 设计由跟进 spec 重做。会让执行者做错事的不是「丢失」而是「写错」: D1 依据链漏了一步 (Finding 1); D5.6 多了一条错的已知缺口、少了一条对的 (Finding 3、Finding 1)。

### (c) §Impact 影响面数字

- 分母 577 可复现, 是 `git -C aria rev-list --all --count`, 含全部远端分支与 112 个合并提交; master 为 568 (记录 8)。
- 分子不是 6 而是 7: 用「逐提交比对 frontmatter 的 description」这个方法, 对全部非合并提交跑, 改已有 skill description 的提交有 7 个 (列表见记录 8)。把 brainstorm 的「删 frontmatter / 恢复并换措辞」两次提交算一次则为 6, 应写明口径。
- 比例 7/577 ≈ 1.2%, 按非合并提交算 7/465 ≈ 1.5%; 「约 1%、一般开发任务不受影响」的结论不变, 所以只列本节, 不进 Findings。
- 同期新增 skill 的提交 15 个 (不含首版, 共 18 个 skill)。若禁令覆盖新增 skill (Finding 2 情形 2 的同一问题), 自主模式受影响的提交约为所写的三倍 (两类合计 21 个, `7801bd42` 两类都算)。Impact 应写明按哪种读法。

## 新引入问题检查 (任务 3)

- **D2 去掉「Why 第 1 条」**: 改为「见基线目录 RESULT.md 结论 1」, RESULT v6 结论 1 正是饱和结论, 成立 (记录 13)。
- **D4 去掉元指令**: 「§4.1 写一句说明」已删, 转录范围句与模板、合规条款一致; 条件段标明「不转录」, 没有新冲突。余项见观察 6。
- **SC-9 按条款标题词定位**: 对 v7 D2 自检, 「fail 的后果」+「不得 ship」与「作废」+「不得 ship」各 1 行; 分别删去这两行, 对应计数都转 0 (记录 9)。成立。
- **SC-11 匹配范围扩展**: 五个模式对 D1 SOT 格、D2、D3、D4 模板与合规条款、D6 第三条、现行手册 §场景 4 (将成 4a) 全部 0 命中, 没有「原样保留的文本先天转红」的问题 (记录 9)。成立。
- **SC-12 改写**: 与新禁令逐串对应; 缺「不提交任何改动」一串 (观察 8, 并入 Finding 1 修法第 4 条)。
- **计数一致性**: 抬头 / T6 / SC-6 / Key Deliverables 四处「三张」彼此一致, 但与 D5 第 7 项冲突 (Finding 4)。
- **§Impact 新写的自主运行时一条**: 数字口径见任务 2 (c), 代价描述见 Finding 3。
- **OQ-7 改写**: 「本 Spec 只管交互模式; 自主模式见 D1 的禁令与 D5.6 跟进 spec」与 D1、D4 一致, 没有新冲突。

## 观察 (不进收敛比较键, 不影响 vote)

1. **硬前提缺检查点**: D5.6 的硬前提是「须在要改 skill description 的任务派给 runner 之前落地」, 但派发前没人知道某个任务会不会动 description (Layer 1 只加载元知识)。现状 Layer 1 只扫 `FORGEJO_REPO` (默认 `Aria`) 里带 `aria-auto` 标签的 issue, runner 要碰 skill 文件须经 issue.yaml 的 `target_repo` 指向 aria-plugin (记录 15)。建议把硬前提写成可检查的形式, 如「跟进 spec 落地前, 自主派发不接 `target_repo` 为 aria-plugin 的 issue」, 并列为 M6 相关收尾的检查项。
2. **Impact 数字口径**: 见任务 2 (c) —— 分子 7 不是 6、分母含合并提交与非 master 分支、新增 skill 的读法没写; 结论不变。
3. **`#196` 是禁令生效的前置**: `#196` 修好之前, runner 里 `unattended` 回落 `false`, 禁令根本不会触发 (runner 按交互模式走, 要 owner 审套件而容器里没人)。v7 已把 `#196` 列进 D5.6 已知缺口; 建议在硬前提里写明「跟进 spec 落地」包含 `#196` 修复并在 runner 内实测 `unattended == true` 生效, 否则跟进 spec 可能只做了失败类型与告警, 禁令仍不触发。
4. **原 OQ-9 的环境约束没进 D5.6**: 在 GLM 上验证 4b, 须在 Layer 2 实际的 Claude Code + Luxeno 路由环境里跑 (本机 v1–v5 直连 Anthropic, 不代表 Layer 2), 以及三臂同构基线的做法与耗时估计。这是跟进 spec 的内容, 不影响本 Spec 执行; 建议 D5.6 写一句, 免得跟进时在别的环境里验证。
5. **「禁令不是机械保障」一句丢了**: v6 原 OQ-7 (C) 写明「这条规则在自主模式里靠 Layer 2 的 Claude 遵守指令, 不是机械保障」。SOT §6 第三条已写「rule6_note 五字段无机械 enforcement」, 建议 D5.6 (或 §6) 同样点明自主禁令无机械保障 —— Finding 1 的漏洞能存在, 正是因为它只靠指令遵守。
6. **R5 第 1 条的条件分支余项**: D4 的「随 OQ-7 裁定变化的部分」只列了 SOT §4.1 的改法; owner 若裁交互 (B), D2 要进手册的「新套件须经 owner 审阅后才能作门」也要跟着改, 否则手册与 SOT §4.1 冲突。只在非推荐选项下出现, T0 的通用纪律可覆盖, 列观察。
7. **R5 第 3 条余项**: 抬头重核清单仍只写「§Why 与 §D2 §D3」, 不含 D6 / Impact / OQ-3 / OQ-7 / T8 (都引 RESULT); D6 仍把「v6」写死又要求「写入时附当时的版本号」。v7 各处 RESULT 引用已统一为 v6, 暂无实际漂移。
8. **SC-12 与 §6 第三条的覆盖**: SC-12 锁住了禁令的触发条件、「放弃整个任务」与「写明」, 但没锁「不提交任何改动」(按 Finding 1 修法改写后应锁撤销改动那半句); SOT §6 第三条除「只在 Claude 模型上实测过」外 (地板守卫 / 未穷举 / 自然措辞扩张不判红 / 无机械 enforcement) 仍无 SC。
9. **编排器文档与代码的漂移 (不属本 Spec)**: `layer-boundary-contract.md` §4 把这类失败叫 `execution_crash`, 写「Feishu alert with diagnostic snippet」; §S_FAIL handling 写「Immediate Feishu alert」「auto-retry (default)」。代码里叫 `container_crash`, tick 标 S_FAIL 不发告警, 失败分析默认关闭, container_crash 不可重试 (记录 6、7)。建议 aria-orchestrator 侧对齐; 本 Spec 引用编排器行为时应以代码为准。
10. **runner 提示词与 runner 行为自相矛盾 (不属本 Spec 改动范围)**: `prompts/issue-dispatch.md` 第 29 行要求任务无法完成时「do NOT make a commit with partial work」, 而 initial.sh Step 10 会替 Claude 提交残留改动 (记录 2、3)。这是 Finding 1 的上游根因, 宜进 D5.6 已知缺口, 或另开 aria-orchestrator issue。
11. **本席 R5 观察 1 勘正**: 见开头「勘正」段与 Finding 3。以后引用编排器的失败处置, 本席以代码为准, 契约文档只作线索。
12. **已核实无问题的项 (省下一轮复核)**: SC-1 / SC-9 / SC-10 / SC-11 / SC-12 与 v7 转录文本自洽, SC-9 两个反事实都转红; SC-11 对全部转录块与现行 §场景 4 零命中; D2 对 `run_eval.py` 的源码描述成立; RESULT v6 的「结论 1」「§v5」「同一首次探针的附带观察」「时长与成本」四个锚点都在; 三处旧句各 `grep -cF` = 1; `#196` 仍 open, 正文含「静默 fallback」。

## Verdict

PASS_WITH_WARNINGS —— critical 0 / major 3 / minor 1 (Findings 段); 观察 12 条。

我席 R5 三条: major 那条已由收窄关闭, 而且是真关闭 —— 禁令自足、fail-closed、没有会悄悄失效的条件, 移到 D5.6 的是设计工作不是缺陷; SC 锁那条由 SC-12 关闭; D6 引旧版那条引用已改对, 只剩重核清单没补全 (观察)。

仍投 REVISE。三条新 major 都能在代码或文本里机械复现: 禁令的依据链漏了「runner 替 Claude 提交残留改动」这一步, 照字面执行正好落进它要防的结果 (Finding 1); v6 加的参照臂让 D2 自己规定的「改套件再重跑」路径必然作废, 新增 skill 也跑不成 (Finding 2); Impact 与 D5.6 对 S_FAIL 后果的描述与代码相反 (Finding 3)。Finding 1、3 出在为收窄新写的运行时描述上, Finding 2 出在 v6 为回应 R5 聚合第 2 条新加的参照臂上, 形态与 R3–R5 相同 (修复新写的文字带出新缺口)。全部修改只动文字, 不用重跑基线。按主控约定, R6 仍有 major, 应如实报 owner。

给主控的收敛建议: Finding 1 与 Finding 3 可以一起用「少写」来修 —— D1 删掉依据句, D5.6 与 Impact 只写经代码核实的三件事 (进 S_FAIL(container_crash) 终态; 默认不重试、不告警; runner 会提交工作区残留改动), 其余机制细节全部留给跟进 spec。新文字越少, R7 冒新 major 的面越小。Finding 2 必须补一句定义 (参照臂只作环境对照 + 新增 skill 的处理), 省不掉。

## Vote

REVISE

## 数据核实记录

核实方式: 直接读源文件或 git 对象重算, 不拿 proposal / RESULT 里的数字当依据。脚本在 scratchpad。

1. **被审版本与 diff**: HEAD `c3a5903`; `git diff 3b2215e c3a5903` (v6→v7) 与 `git diff f169a0b c3a5903` (v5→v7) 存 scratchpad。v6→v7 里 D5 第 7 项是上下文行 (没改), T6 / SC-6 / Key Deliverables / 抬头「代码落点」由四张改为三张。
2. **runner initial 模式** (`aria-orchestrator/docker/aria-runner/modes/initial.sh`, 596 行, aria-orchestrator 本地 master): Step 7 (337–347 行) 按 claude 退出码与 result 帧给出 PENDING / CLAUDE_TIMEOUT / INFRA_FAILURE / CLAUDE_REFUSAL; Step 8 (353–377 行) 只在「`git status --porcelain` 为空且相对 `origin/<base>` 无新提交」时判 CLAUDE_NO_OP; Step 10 第 415 行注释「若 claude 没 commit 但 working tree 有 changes, runner 补 stage+commit」, 416–419 行 `git add -A` + `git commit`; 之后推送 (430–445 行)、开 PR (462–503 行); SUCCESS 严格定义 (524–536 行) = claude 退出 0 + 有提交 + 有 PR + file_touched 与 diff_contains 断言命中; 591–596 行 SUCCESS 退 0, 其余退 1。`entrypoint.sh` 第 38 行 `exec /opt/aria-runner/modes/initial.sh "$@"`, 退出码透传。
3. **runner 提示词** (`prompts/issue-dispatch.md` 第 29 行): 「**Failure handling**: If the task cannot be completed, do NOT make a commit with partial work; exit with a clear reason in your final message so the runner can classify as `CLAUDE_REFUSAL` or `CLAUDE_NO_OP`」。
4. **rework 模式**: `changes.sh` 的 `fail_with` (70–78 行) 写 FAIL 并退 1; 269 行 `git add -A`, 270–272 行暂存区为空才 `fail_with no_changes`, 否则提交 (274 行)、推送 (294 行), 推送成功写 `"outcome":"PASS"` (300 行), 308 行 `exit 0`, 全程无断言。`redo.sh` 295–302 行同形, 388–403 行写 PASS 并 `exit 0`。
5. **编排器** (`hermes-extensions/aria-layer1/aria_layer1/extension.py`): `_handle_s5_await` (2467–2675 行) 在 alloc terminated 时 exit_code 为 0 → S6_REVIEW (2594–2619 行), 否则 S_FAIL(`FailReason.CONTAINER_CRASH`) (2620–2638 行, fail_detail 只含 exit_code 与 alloc_id); 心跳超时 → S_FAIL(timeout) (2498–2522 行); lost → S_FAIL(dispatch_lost) (2640–2657 行)。`nomad/jobs/aria-layer2-runner.hcl` 153–156 行 `restart { attempts = 0  mode = "fail" }`。
6. **重试与告警**: `reconciler.py` 1138–1141 行可重试失败类型集合为 `{"infrastructure", "timeout"}`, 1143 行 `_RETRY_COUNT_MAX = 1`; 1271–1319 行重试须 verdict 为 retry、置信度达标、retry_count < 1、失败类型在可重试集合, 否则降为 notify_owner (1321–1341 行发一张卡, 注释「no retry, terminal」), abort 不发卡; 438–439 行仅在失败分析调用方已注入时扫描。`reconcile_runner.py` 120–121 行未设失败分析开关 (环境变量名 `ARIA_FAILURE_ANALYSIS_ENABLED`) 即返回 None, 420–425 行注释「When disabled (default for now until owner explicit opt-in per cost discipline)」; 仓内无任何 `.hcl` 设置该变量, `docs/m5-handoff.yaml` 第 62 行「<owner choice; default off>」, `docs/architecture-decisions.md` 第 3687 行「默认 disabled 等 owner 显式 opt-in」。tick 的 S_FAIL 分支 (`extension.py` 1329–1355 行) 只调 `repo.mark_failed`; `tick_runner.py` 检索 feishu / alert / notify 零命中; 全模块 `feishu.send` 调用点只有 S7 拒绝 (`extension.py` 3129) 与 S7 通知 (3227)、reconciler 的 S7 超时 (617)、卡住行 (`_handle_fail` 730–760 行, 836 行发送)、spec 漂移 (1113)、失败分析 (1335)。心跳扫描注释 (`extension.py` 1156–1173 行): 该 issue 已有 attempt 为 1 的派发行 (任何状态) 即不再建派发。`FAIL_REASONS` (290–303 行) 与 `interfaces.py` 第 86 行 `CONTAINER_CRASH = "container_crash"` 一致。
7. **边界契约** (`docs/layer-boundary-contract.md`): §4 失败模式表 (175–186 行) 第 182 行 `execution_crash`「Layer 1 reads exit code + last log line; Feishu alert with diagnostic snippet」; §S_FAIL handling (188–201 行)「Immediate Feishu alert」(192 行)、「Acknowledge and let Layer 1 auto-retry (default)」(199 行)、「Permanently block the issue from auto-dispatch」(201 行)。与记录 5、6 的代码不一致。
8. **Impact 数字** (`aria` 子模块 HEAD `1cb3872` = v1.73.3, `desc_changes.py`): `rev-list --count` 对 HEAD / master / origin/master / github/master 均 568 (非合并 456), `--all` 为 577 (非合并 465)。对每个非合并提交的 `skills/*/SKILL.md` 用 `-M` 跟踪改名, 取父提交与本提交的 frontmatter 以 yaml 解析 `description` 比对, 精确比较与压缩空白比较都得 7 个提交: `557b9535` (2026-01-26, 一次改 23 个 skill, 精确比较另含 arch-common 一处空白差)、`641e1649` (tdd-enforcer)、`55d2e84a` (brainstorm, 删掉了 frontmatter)、`ee35928b` (brainstorm, 恢复 frontmatter 且措辞不同于删前)、`f8713f14` 与 `7801bd42` (phase-d-closer)、`2b67ac64` (openspec-archive, 即基线那次); `--all` 与 HEAD 结果相同。新增 `skills/*/SKILL.md` 的非合并提交 16 个: 首版 `6862a2a8` 一次 24 个, 其余 15 个共 18 个, 合计 42 个。另有 6 个合并提交的第一父差异碰到这些文件, 都是上面提交所在分支的合并, 不重复计。改前改后原文摘录见 `desc_detail.py` 输出。
9. **SC 自检** (对 v7 proposal 的转录文本, `sc_selfcheck_v7.py`): D1 三行都含核心句、「照跑场景 1」「另须跑场景 4b」; SOT 行含 SC-12 四串 (并含「不提交任何改动」), 不含「撤销」「还原」「工作区」; CLAUDE.md 行含「自主运行时的处置见 SOT §2」; SC-11 五个模式对 D1 SOT 格、D2、D3、D4 模板与合规条款、D6 第三条、现行手册 §场景 4 均 0 命中; D6 第三条含「只在 Claude 模型上实测过」; SC-9 两对各 1 行, 删「fail 的后果」行或作废行都转 0; SC-10「参数钉死」行 1 行, 五项齐全。
10. **参照臂与 D5 第 7 项的来历**: proposal 在 `e822829` / `f169a0b` / `3b2215e` / `c3a5903` 中「参照臂」分别出现 0 / 0 / 5 / 5 次, D5 第 7 项行 0 / 0 / 1 / 1 次 —— 两者都是 v6 新增。
11. **规则原文**: SOT (`standards/conventions/skill-benchmark-exemption.md`, Version 1.0.0) §1 第 22 行「逐 hunk 判, 不逐文件判」; §2 决策表第四行 (31 行)「拿不准算不算处方性 / 算不算在范围内 → 照跑 (宁跑勿豁)」; §2 第 33 行末句为待换旧句; CLAUDE.md 规则 #6「触发: 新增 Skill / 改逻辑 / 改 description / 发版审计」; 手册 §场景 2「新增 Skill 首次基线」(230–243 行)、§场景 4 (263–274 行)、「边界与留痕」(480–481 行)。三处旧句 `grep -cF` 各 1。
12. **`run_eval.py`** (插件缓存 `claude-plugins-official` 下 skill-creator 的 `scripts/run_eval.py`): 223–225 行 `except Exception` 打印 `Warning: query failed: …` 到 stderr 并 append `False`; 229–241 行 trigger_rate / did_pass / pass。D2 的描述成立。
13. **RESULT v6**: 第 3 行「本文件版本: 6」; 第 18 行「同一首次探针的附带观察」; §结论 (61 行) 第 1 条为饱和结论; §v5 (47 行); §时长与成本 (88 行); §已知局限 (93 行)。
14. **`#196`**: `forgejo GET` 返回 state open, 标题「[契约][aria-orchestrator] unattended 的 Layer 1→2 env 传递三腿契约未定义 — 缺 import 会静默 fallback 到 …」, 正文含「静默 fallback」。
15. **Layer 1 派发范围**: `forgejo_client.py` 第 48 行取 `FORGEJO_REPO`, 缺省 `Aria`; `extension.py` 第 1149 行按 `aria-auto` 标签列 issue; runner 的目标仓来自 issue.yaml 的 `target_repo` (initial.sh 232 行)。
16. **往轮检索**: 对 R1–R5 共 30 份报告检索「新增 Skill / 新 skill / 新建 skill / 场景 2 / 首次基线 / auto-commit / 补 stage / git add -A / 工作区」, 只有两处无关命中 (R4 qa 对账表一行、R5 code-reviewer 环境说明一行)。v7 proposal 本身检索「新增 skill / 新 skill / 场景 2」零命中。

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
timestamp: 2026-09-14T14:16:43.555Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [code-reviewer]
---

# post_spec R5 — code-reviewer 席 (Phase 1 规范合规 + Phase 2 质量)

被审对象: `openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md` rework v5 @ 主仓 HEAD `f169a0b`; 基线目录 `aria-plugin-benchmarks/ab-results/2026-09-13-rule6-description-trigger-eval-baseline/` (RESULT.md v5 与原始产物, 含 `v5-mildcreep-opus5/PREREGISTRATION.md`)。只审不改, 唯一写入是本报告; 反事实实跑用的脚本放在 session scratchpad, 只在内存中替换, 不写仓库文件。

独立性: 本轮其他席的 R5 报告没有读 (同目录已有一份别席 R5 报告落盘, 未打开)。R4 只读了聚合报告与本席报告。下文数字都来自实跑, 命令与输出见「实跑记录」。

## R4 对账

范围: 本席 R4 报告 Findings 的 3 条。

| 序号 | R4 条目 | v5 落点 | 状态 | 核对依据 |
|---|---|---|---|---|
| 1 | [major] OQ-7 自主模式「(A) 与 AD10 冲突 ⇒ 可行做法只有 (B)」不成立 | §OQ-7 自主栏 (B) (C) (D) (E) 四选项; 推荐改为交互 (A) / 自主 (C); 新增「运行模式怎么判」 | closed | 「只有」已删, 四个选项各带代价。逐项对原文: (A) 与 AD10 §决策「只保留 1 个人类审批 gate」冲突, 成立; (B) 的「当前跑不起来」对 `aria-orchestrator/docker/aria-runner/Dockerfile` 核实 (装 claude-code CLI + `COPY aria/ /opt/aria-plugin/`; `docker/aria-runner/` 与 Nomad HCL 中 skill-creator 0 处); (C) 引 AD5 选型理由第 2 条「任意状态都可进入 S_FAIL」, 逐字; (D) 41 × 约 15 分钟 ≈ 10 小时, 算术成立; (E) 对应 AD10 §回滚路径 Level 2, 意思一致 (引号内把原文括号改成了逗号, 观察第 4 条)。事实依据: handoff frontmatter `owner-container: aria-runner-bot/023236f2` 23 份、`aria-runner-bot/bfe8285d` 7 份, 与文中一致; v1.64.0 发版 handoff 属 023236f2, v1.70.0 会话收尾 handoff 属 bfe8285d, 正文都有 owner 裁定记录。`10CG/Aria#196` open, 标题与文中描述一致; phase-a-planner SKILL.md 第 131 行「有没有人可问是**配置事实**」逐字。残留都放观察段: (C) 的「进 S_FAIL / 交给交互模式」与 layer-boundary-contract §3 §4 的所有权和默认自动重试不符 (观察第 1 条); (D) (E) 漏写与 (B) 相同的前置 (观察第 2 条); 全称句的证据范围 (观察第 3 条) |
| 2 | [minor] D6 与 RESULT v5 的能力上限全称句; RESULT「按预登记」改写了预登记原文 | §D6; RESULT v5 §v5、§已知局限 | closed | D6 改为「已验证判红的破坏类型是删领域词与显式强制过宽两类 (未穷举)」; RESULT §v5 引文「这是对 §D2「只承诺两类破坏」局限的实证确认, 不是守卫失效的证据」在 PREREGISTRATION.md 与 RESULT.md 中各恰 1 次 (python 子串比对, 逐字); RESULT §已知局限改为「已验证判红的破坏有两类 (结论 2, 未穷举)」。两份文件里剩下的「判得出」都不是能力上限说法。相关的新问题: D6 仍引「RESULT.md v4」, 见 Findings 第 3 条 |
| 3 | [minor] SC-1 与 SC-9 没有能变红的断言 | §SC-1 补「照跑场景 1」「另须跑场景 4b」; §SC-9 按行拆 fail 行与作废行 | closed | 实跑: 用 v3 `0c41e53` 的 D1 新句落地 → SC-1 红 (CLAUDE.md 与 SOT 缺「另须跑场景 4b」, 手册两串都缺); 用 v4 `e822829` 与 v5 的新句落地 → 绿。SC-9 取 v5 D2 小节: 原样绿; 删「fail 的后果」行 → 红 (fail 行 0); 删作废行 → 红 (作废行 0)。我 R4 修法里的 SC-3 补项 (SOT §4.1 的 fail / void 合规句) 没有采纳, 手册一侧已被 SC-9 锁住, 放观察第 6 条 |

合计: closed 3 / partially 0 / open 0。

## Findings

- [major] testing/proposal.md §D2 (issue): 作废第二情形「输出缺 query 条目、runs 少于 3」按 run_eval.py 源码不可达 (异常、超时、claude 报错都记一次未触发, runs 恒为 3); 环境失败因此落 fail, 执行者按 fail 处置去改一份正确的 description。
- [minor] testing/proposal.md §Success Criteria (issue): v5 为 R4 major 2 加的 SOT §2 自主条款、CLAUDE.md 指向句与 D6「GLM 未验证」没有能变红的 SC; 反事实: 删掉前两处落地, SC-1 至 SC-10 全绿。
- [minor] documentation/proposal.md §D1+§D6 (issue): 要逐字落进 standards 的定稿文本有残留: SOT §2 新句含「依 OQ-7 / OQ-9 裁定, 裁定不同则随之改」(归档后悬空); D6 仍引「RESULT.md v4」(能力上限说法勘正前的版本)。

计数: critical 0 / major 1 / minor 2。两条 minor 列入 Findings 的理由与 R4 相同: 都是 Phase B 要逐字写进 standards (单独发布的规范仓) 的文本, 或锁这段文本的唯一 SC; Level 2 不产 tasks.md (OQ-4), T1–T8 的验收只有这组 SC; ship 后再改要另走一个 cycle。

## Findings 证据与修法

1. **作废第二情形不可达, 环境失败被导向改 description (major)**
   - v5 D2 新增: 「**作废**只在两种情形发生: 门通过而负控 ≥ 6/10 ...; 或 `run_eval.py` 自身没跑成功 (报错退出、输出缺 query 条目、`runs` 少于 3), 此时也不判 description」。这是 R4 聚合 rework 计划「观察顺手补: D2 作废第二情形」的落地, 用来接住我 R4 观察第 4 条 (环境失效造成的假红)。
   - run_eval.py 源码 (marketplace 与缓存 `bb335391eb83`、`unknown` 三份 md5 相同):
     - 第 222–225 行: worker 抛异常时向 stderr 打「Warning: query failed」, 然后 `append(False)` —— 记为一次未触发, 不是少一次;
     - 第 101 行超时退出循环, 第 178 行 `return triggered` —— 超时记为未触发;
     - 第 88 行 `claude -p` 的 stderr 接 `DEVNULL`; 进程报错时要么输出 `result` 事件 (第 171 行返回), 要么直接退出 (循环 break 后第 178 行返回) —— API 报错、限流、鉴权失败都静默记为未触发, 连 Warning 都没有;
     - 第 240 行 `"runs": len(triggers)`: 每个 query 提交 runs-per-query 个 future, 每个 future 恰好 append 一次 ⇒ runs 恒等于 3, 每个 query 都有条目 (除非套件里 query 文本重复)。
   - ⇒ 三个判别条件里只有「报错退出」可达 (整个 run_eval 进程崩溃)。最常见的环境失败 —— 一段时间的 API 报错或超时 —— 产出的是 rc 0、20 条齐全、runs 全为 3 的 json, 只是若干 should-trigger 条目掉到 0/3 或 1/3。按 D2: 门判 fail (D2 原文「被评 description 退化 ⇒ 门先判 fail」预设了 fail 就是 description 的问题); 同一环境里负控只会更低 (≤ 5/10), 不触发作废; fail 的处置只有「(1) 修正 description 直到门通过; (2) 改套件; 两条都不走 ⇒ 升级 owner」, 没有「查环境后原样重跑」这条路。执行者照字面只剩三条路, 前两条都是错的动作: 改一份正确的 description (或改套件), 环境恢复后重跑通过, 一份由噪声驱动的改动带着「4b pass」ship。
   - 这不是假设场景: 本 Spec 自己的基线里, 五轮有两轮 (v1 共用根、v2 名字泄漏) 是工具或环境问题, 当时的数字看上去都像 description 的效果。D3 前置排除了这两种已知失效, 排除不了未知的。另外 `.err` 不在 D3 第 6 行的产物形状里, 基线目录里也没有 (scratchpad 里 v5 三份 `.err` 的 Warning 均为 0) —— 连唯一可达的异常信号都不留存。
   - 为什么是 major (R4 同一风险我只列了观察): v5 新写的条件对工具行为的前提不成立, 读者会以为「run_eval 没跑成功」已经会被判作废。这符合 major 门槛里的「判据事实不成立」, 后果是「规则执行者做错事」。
   - 修法 (只改文字, 不需要新的实跑): (1) 删掉两个不可达条件, 换成可达信号: 产物保留 `.err`, 含「Warning: query failed」即作废 (D3 第 6 行同步); (2) 门判 fail 时, 被评版与改动前的版本同批重跑一次: 改动前版本也 fail ⇒ 作废 (环境或套件问题, 计入连续作废); 改动前版本通过而被评版仍 fail, 才进 fail 处置。这是有效性对照, 与负控同类, 不是 D2 排除的比较判据; 代价是 fail 时多两臂 (约 10 美元、11–20 分钟); (3) 按 R4 观察第 4 条补「fail 且负控 ≥ 6/10 ⇒ 作废」。

2. **v5 的自主条款没有 SC (minor)**
   - v5 为回应 R4 聚合 major 第 2 条, 在 SOT §2 新句加了「自主运行时 (`state_scanner.coordination.unattended == true`) 在场景 4b 于其所用模型上验证之前, 不做 description 改动, 需要改时任务进 S_FAIL ...」, 在 CLAUDE.md 新句加了「自主运行时的处置见 SOT §2」, 在 D6 加了「场景 4b 只在 Claude 模型上实测过 ..., Layer 2 所用的 GLM 未验证」。
   - 反事实 (内存中): 按 v5 D1 落地, 但删掉 SOT 新句的自主条款与 CLAUDE.md 的指向句 → SC-1 三处核心句各 1、形状全绿, SC-5 三行 0, SC-7「边界四条」1 /「边界三条」0, SC-10 不受影响 —— 全绿。SC 段对「自主 / S_FAIL / unattended / GLM / Claude 模型 / OQ-9」计数全 0。D6 第三条正文只有 SC-7 查计数语。
   - 与我 R4 Findings 第 3 条同类: 一条 R4 major 的修复只写在要逐字落地的文本里, Phase B 漏写时验收查不出来。
   - 修法: SC-1 补「SOT 含核心句的那一行同时含 `unattended` 与 `S_FAIL`; CLAUDE.md 那一行含『自主运行时的处置见 SOT §2』」; SC-7 补「SOT §6『GLM 未验证』= 1」。三处改前都是 0, 反事实成立。

3. **定稿文本的残留 (minor)**
   - D1 表头写「新句 (定稿)」, T1 写「三处 D1 新句落地 (逐字)」, 但 SOT 那条新句里有「(依 OQ-7 / OQ-9 裁定, 裁定不同则随之改)」。它是写给 T1 执行者的草稿说明: 逐字落地后, standards 的 SOT 里会出现两个没有出处的「OQ-7 / OQ-9」(归档后读者不知道是哪份 spec 的); 执行者去掉它, 又违反了「逐字」。修法: 把括注移到 D1 正文 (如「SOT 新句的自主条款按 OQ-7 / OQ-9 裁定改写」), 新句本身只留规则。
   - D6 引号内的 SOT §6 第三条写「... RESULT.md v4, 写入时附当时的版本号与提交 SHA」。proposal 其余 7 处 RESULT 引用都已改 v5, 只有这一处还是 v4 (头部「RESULT 再修订须同步重核本文 §Why 与 §D2 §D3」的清单没列 §D6, 大概是这样漏的)。RESULT v4 第 57 行正是「这是对『守卫只判得出两类破坏』这条局限的实证确认」—— R4 要求去掉的能力上限说法。SOT 若引 v4, 读者顺着引用会读到勘正前的写法; 且「v4」与同句「写入时附当时的版本号」自相矛盾, RESULT 头部也要求「引用方请写『RESULT.md v5 @ <提交 SHA>』」。修法: 改为 v5, 并把 §D6 加进头部的重核清单。

## 观察 (不进收敛比较键, 不影响 vote)

1. **OQ-7 (C) 的机制与代价, 要对照 layer-boundary-contract, 不能只看 AD5**:
   - §3 所有权表 S_FAIL 行的 Owner 是「Layer 1 escalation」, 正文「Layer 1 also owns the failure escalation path (→S_FAIL)」。Layer 2 不能「让任务进 S_FAIL」, 只能以失败结束, 由 Layer 1 升级。§4 列的六类 Layer 2 失败模式里没有「按规则拒做」, 最接近的是 `execution_crash` (非零退出); runner `modes/initial.sh` 另有 `CLAUDE_NO_OP` (claude 退出 0 且无改动) 这一出口。
   - §4「S_FAIL handling」给 owner 的处置里, 默认是「Acknowledge and let Layer 1 auto-retry (default)」。按 (C), 任务会被自动重派、再被拒做, 直到重试预算 (3) 用完, 每次都是一整次 Layer 2 运行 (GLM 每次调用 45–54 秒) 外加一条告警, 并被记成 crash 或 no-op 类。「交给交互模式处理」要靠 owner 在告警里选「Override state」或「Permanently block the issue from auto-dispatch」。
   - AD5 那句引用逐字成立, 缺的是这层契约。建议: SOT 新句写成「不做该 description 改动, 在结果里写明原因并以失败结束任务 (由 Layer 1 升级 S_FAIL)」; (C) 与推荐项的代价补「默认自动重试至预算耗尽 + 告警, 记为 crash / no-op 类; 要干净地停下, runner 需要一个专门的失败原因」。目前实际无害: `10CG/Aria#196` 修好前 Layer 2 读不到 `unattended == true`, runner 镜像又没有 skill-creator, 4b 跑不起来只会作废 —— 同样 fail-closed。
2. **OQ-7 (D) (E) 漏写前置**: (B) 的「当前跑不起来 (镜像没有 skill-creator)」对 (D) (E) 同样成立 —— (D)「之后自主模式照常按 4b 判门」与 (E) 的条件式人工 gate 都要 runner 能跑 4b; 且 SOT §2 新句在 GLM 验证前对所有选项都禁止自主改 description。推荐理由用「(B) 跑不起来」排除 (B), 对 (D) (E) 不对称。建议 (D) (E) 的代价各补一句「同样需 runner 镜像装 skill-creator, 且须先完成 OQ-9 的 GLM 验证」。
3. **全称句「自主流水线 (AD10) 至今没有改过 aria-plugin 的任何文件」(v5 新增, 出现两次)**:
   - 文中依据 (handoff frontmatter 配对 23 / 7 份 + 抽查 8 次 bot 发版提交中的 2 次) 撑不到「任何文件」: frontmatter 只记录写 handoff 的会话, 流水线未必写 handoff; 抽查只覆盖 33 次 bot 提交中的 2 次。
   - 「aria-runner-bot 是 AI 会话共用的机器提交身份」只说了一半: M5 文档记载 Layer 2 runner 自己也用 aria-runner-bot 凭据 clone / push (`aria-orchestrator/docker/aria-runner/modes/initial.sh` 第 251 行的 URL 改写; `docs/handoff/2026-05-19-m5-deploy-playbook-v11-addendum.md` 第 402 行预期「commit author = aria-runner-bot」)。同一身份有两种来源, 正是 v4 误判的根源; §2.3.9 原文也没有点名 aria-runner-bot, 只写「AI runner 会话 (无人值守容器、CI bot 等自动执行体)」。
   - 结论本身有独立证据: `10CG/aria-plugin` 全部 87 个 PR 的发起人都是 simonfish; 流水线开 PR 用的是 `10cg-ci-bot` (10CG/Aria#28、10CG/Aria#29、10CG/Aria#31、10CG/Aria#121, 分支如 `aria/DEMO-001`); AD10 下流水线的改动只能经 S7 PR 合入 ⇒ 截至 2026-09-14, 流水线没有向 aria-plugin 合入过改动。建议把依据换成这一条, 并补「aria-runner-bot 同时是 Layer 2 runner 的推送身份」。推荐理由真正需要的只是更弱的「没有改过任何 description」, 用不到「任何文件」。
   - 附带 (不属本 spec 范围): memory `project_aria_runner_bot_autonomous_same_repo_work` 仍写「aria-runner-bot (Aria 2.0 Layer 2 自主运行时容器, ..., container 如 023236f2)」, 与 v5 的更正相反, 很可能是 v4 误判的来源; 不更正会误导下一个起草者。
4. **(E) 引号内文字不是逐字**: AD10 原文「在 S5_REVIEWING 中间插入一个 optional human gate (只对高风险 issue 触发)」, 文中把括号改成了逗号。意思没变, 但带引号就应逐字。
5. **SC-1 新断言的两个边角**: (a) 否定式也能满足 (如「不必照跑场景 1」含子串「照跑场景 1」), 对「放宽」没有反向断言 —— 可加「三处落点行的『不跑场景 1』= 0」, v3 SOT 新句正好会命中; (b) 断言要求「含核心句的每一行」都含两串, T2 若在 §场景 4b 开头复述核心句 (很自然), SC-1 会误红。建议形状判定只取 D1 落点那一行。
6. **SOT §4.1 的合规句仍无 SC**: 「`scenario4b` 为 `fail` 或 `void` ⇒ 义务未完成, 不得 ship」与「`description_changed: yes` 而 `scenario1` ... ⇒ 不合规」(v5 已补 scenario1) 在 SOT 一侧没有 SC (我 R4 修法里的 SC-3 补项)。手册一侧已被 SC-9 锁住, 所以不列 Findings。
7. **R4 观察中 v5 未动的 (都不阻塞)**: 第 1 条 (D5.5「按 hunk 类型跑场景 1 还是 4b」的 v3 口径仍在); 第 3 条 (fail 后修好重跑时, 单值的 scenario4b 记哪次); 第 5 条 (处置 (2) 改的套件按 D4 是 provisional, 与 OQ-7 (B) 叠加可「fail → 改考卷 → ship」); 第 6 条 (「近似误触须覆盖相邻任务」与 T4 / SC-4 逐字节搬入基线套件冲突); 第 7 条 (mildcreep 还删了「openspec/」, D2 与 RESULT 只写了四处增补); 第 8 条 (RESULT 头部「模型」行仍只写 `claude-fable-5-1`); 第 9 条 (OQ-9「与 v3 同构的三臂」—— v3 是四臂, 「一个坏 description」对应 v4 过宽臂); 第 10 条 (SC-10「含『参数钉死』的那一行」没写 0 行判红); 第 11 条 (D1 表第 3 行外层反引号的约定); 第 13 条 (时长区间算法); 第 14 条 (SC-5 自测句「『不设比较判据』行 ... 为 0」, 该行原样实跑仍是 1)。
8. **OQ-4「本 Spec 的 post_spec 每轮约半小时, R1 / R2 实测」**: 按报告文件时间, R2 约 54 分钟、R3 约 50 分钟、R4 约 46 分钟 (文件名 12:58:03, 聚合 13:44)。
9. **OQ-9 新增「本机 v1–v5 的环境直连 Anthropic」**: shell 环境没有设置 `ANTHROPIC_BASE_URL`, 垫片又带 `--setting-sources project` (不加载用户级设置), 与文中一致。用户级设置文件被 secret-guard 挡住没读, 只核到这一步。

## 优点

- R4 三条都改在要害上: OQ-7 自主栏从一个选项扩成四个, 每个选项的依据我逐条对到 AD5 / AD10 / Dockerfile / phase-a-planner 原文; 推荐改成最贴合规则 #10 的 fail-closed, 推荐项的代价写进了 Impact。
- tech-lead 自承的 v4 归因错误在正文里点名更正, 没有悄悄改掉。
- SC-1 与 SC-9 的新断言都有真实区分力 (v3 红 / v5 绿; 删任一后果行即红), 区分力是实跑出来的。
- RESULT v5 按预登记逐字引用; 预登记文件先于结果落盘的时序 R4 已核。
- D5.6 新 issue 在头部、D5、T6、SC-6、交付物五处同步, 没有孤儿。

## Verdict

**PASS_WITH_WARNINGS** —— critical 0 / major 1 / minor 2 (Findings); 观察 9 条不计入。

- **Phase 1 (规范合规): PASS**
  - `check_bare_issue_refs.py` 对 proposal 与 RESULT 各跑一次, 都是「裸 issue 引用: 0」, rc 0。
  - 禁用字形 (U+2460–24FF / U+2776–2793 / U+3251–325F / U+32B1–32BF / 希腊字母大小写): proposal、RESULT、PREREGISTRATION 三个文件 0 命中; NUL 字节 0。
  - 本 Spec 的 rule6_note: `n/a` / `no` / `n/a` / `n/a` / `n/a`, 都在 §D4 值域内; `description_changed: no`, 不触发 D4 合规规则; 本范围 aria gitlink 零改动 (`1cb3872`), 「本 Spec 自身不触发 Rule #6」成立。
  - D1 表三条旧句在 CLAUDE.md (第 110 行)、SOT (第 33 行)、手册 (第 480 行, 去外层反引号) 各恰 1 次 (python 计数); v3 / v4 / v5 三版旧句逐字相同; 核心句在三条 v5 新句里各 1 次、逐字相同; 三个现状文件的核心句各 0。
  - 范围: `e822829..f169a0b` = proposal + RESULT + 六份 R4 审计报告; CLAUDE.md、手册、SOT 未动; 没有范围外变更。
  - 头部 Status 与 R4 聚合一致 (0C / 3M / 4m 去重后, 待 R5)。
- **Phase 2 (质量)**
  - 1 条 major: D2 作废条件与工具源码不符, 环境失败会被导向改 description。
  - 2 条 minor: v5 的自主条款没有 SC; 要逐字落进 standards 的定稿文本有草稿残留与旧版本引用。

## Vote

**REVISE** —— major 没有清零。三处都只改文字, 不需要新的实跑: D2 作废条件换成可达信号, 并加 fail 时的改动前版本对照; SC-1 / SC-7 补自主条款与 GLM 局限的断言; SOT 新句去掉草稿括注, D6 改引 RESULT v5。按 R4 聚合的收敛前景, R5 之后 max_rounds 耗尽, 由 owner 裁。

## 映射表

### issue 条目 → D / T / SC

| issue 条目 | D | T | SC | 备注 |
|---|---|---|---|---|
| 建议 1 (拆成两个义务, 不互相替代) | D1 | T1 | SC-1, SC-5 | v5 与原建议逐项一致; SC-1 现在能分开 v3 与 v4 / v5 |
| 建议 2 (SOT 与手册同批改) | D1 三处 + D2 / D3 / D6 | T1, T2, T5 | SC-1, SC-2, SC-7 至 SC-10 | 自主条款与 GLM 局限无 SC (Findings 第 2 条) |
| 建议 3 (rule6_note 加栏, 空着即不合规) | D4 | T3 | SC-3 | 合规规则已补 scenario1; 合规句本身无 SC (观察第 6 条) |
| 验收 1 (历史版本对实跑) | 头部「基线数据」 | 已完成 | 无 | RESULT v5 |
| 验收 2 (区分力为零时的规定动作) | OQ-5 | 待裁 | 无 | 引文未改 |
| 验收 3 (负控显著下降) | D2 同批负控 | T2 | SC-9 | 基线 3/10 对 10/10, 双侧 p = 0.0031; v5 新构造负控 0/10 |

### D → T → SC

| D (子项) | T | SC | 备注 |
|---|---|---|---|
| D1 三处新句 (核心句 + 照跑场景 1 + 另须跑场景 4b) | T1 | SC-1, SC-5 | v3 红 / v4、v5 绿 (实跑) |
| D1 SOT §2 自主条款 + CLAUDE.md 指向句 (v5 新增) | T1 | 无 | Findings 第 2 条 |
| D1 SOT §2 草稿括注 | T1 | 无 | Findings 第 3 条 |
| D1 旧句删除 (CLAUDE.md / SOT) | T1 | 无 | 手册一处由 SC-7「边界三条」= 0 兜住 |
| D1 手册 三条 → 四条 | T1 | SC-7 | 改前「边界三条」1、「边界四条」0 |
| D1 SOT §3 边界注 | T1 | SC-10 后半 | 改前 0 |
| D2 通过定义 / 参数 / 20 条 | T2 | SC-10 | 按行判; 0 行未写判红 (观察第 7 条) |
| D2 负控门槛 / 连续 2 轮 | T2 | SC-9 | 完整 |
| D2 fail 后果 / 作废不得 ship | T2 | SC-9 | 按行判, 实跑有区分力 |
| D2 作废第二情形 (v5 新增) | T2 | 无 | Findings 第 1 条 |
| D2 不设比较判据 | T2 | SC-5 | 三条新句与 D2 + D3 正文均 0 |
| D2 近似误触须覆盖相邻任务 | T2 | 无 | 判断性要求 (观察第 7 条) |
| D2 套件文件 + version.yaml | T4 | SC-4 | 未裁分支一致 |
| D2 手册固定测试集表加 trigger 行 | T2 | 无 | |
| D3 六行前置表 | T2 | SC-2 | 机读实证路径全部存在; v5 只改第 4 行的 RESULT 版本号 |
| D4 §4.1 五字段 / 值域 / 两套编号 | T3 | SC-3 | 改前五个字段名各 0 |
| D4 合规规则 (scenario1 / fail / void) | T3 | 无 | 观察第 6 条 |
| D4 authoring 路径 / 过渡期 | T6 (D5.3 的 issue) | SC-6 | |
| D5.1 拆 4a / 4b | T2 | SC-8 | |
| D5.2 / D5.3 / D5.6 三张 issue | T6 | SC-6 | D5.6 在头部、D5、T6、SC-6、交付物五处同步 |
| D5.4 上游反馈 | T6 | SC-6 | |
| D5.5 `10CG/aria-standards#17` 分工 | T7 | SC-6 | 首句仍是 v3 口径 (观察第 7 条) |
| D6 §6 第三条 + 计数语 | T5 | SC-7 前半 | 第三条正文 (含「GLM 未验证」) 无 SC; 引 RESULT v4 (Findings 第 3 条) |
| SOT 文件头 Version | T5 | SC-7 中段 | 无 D 锚 |
| 合并 / 双推 / 逐 remote `ls-remote` | T7 | 无 | 流程任务; 与 CLAUDE.md 多远程两条约束一致 |
| `10CG/Aria#211` 回帖 | T8 | 无 | 流程任务 |

孤儿检查:
- SC 侧没有孤儿: SC-1 至 SC-10 都挂得到 D。
- T 侧: T7 后半与 T8 是流程任务, 可以接受。
- D 侧没有有效 SC 的: D1 自主条款、D1 旧句删除 (CLAUDE.md / SOT)、D2 作废第二情形、D2 近似误触要求、D2 手册表行、D4 合规规则、D6 第三条正文。其中 D1 自主条款与 D6 的 GLM 局限进 Findings 第 2 条。

### proposal 里的 RESULT 版本引用

| 位置 | 版本 | 结论 |
|---|---|---|
| 头部「基线数据」(第 9 行) | v5 | 同步 |
| §Why 引子 (第 16 行) | v5 | 同步 |
| §D2「只承诺已验证的两类破坏」(第 48 行) | v5 | 同步 |
| §D2 负控构造 (第 50 行) | v5 | 同步 |
| §D3 第 4 行 (第 67 行) | v5 | 同步 |
| §D6 SOT §6 第三条 (第 101 行) | **v4** | 未同步 (Findings 第 3 条) |
| §Impact 成本 (第 116 行) | v5 | 同步 |
| §T8 (第 129 行) | v5 | 同步 |

### OQ 推荐项与自身代价

| OQ | 推荐 | 推荐项自身代价 | 结论 |
|---|---|---|---|
| OQ-1 | 0.5 | 放过「2/3 才触发」的 description | 有 |
| OQ-2 | 单 worker + 独立根 | 两个临时根, 手册多两行 | 有 |
| OQ-3 | 先审 | 改 query 须重跑两臂 | 有; 另写了未裁时的默认 |
| OQ-4 | 无推荐, 两选项各写代价 | 不适用 | 原文无推荐, 未自造默认 |
| OQ-5 | 地板守卫 | 多一条义务, 只挡两类破坏 | 有, 备选代价也写了 |
| OQ-6 | 暂不放宽 | 每次 description 改动多跑一次场景 1 | 有 |
| OQ-7 | 交互 (A) / 自主 (C) | (A) 写在选项内; (C) 写「一律停在 S_FAIL」 | 有; (C) 漏了默认自动重试 (观察第 1 条) |
| OQ-8 | 判据不改 | 套件没覆盖到的扩张判不出 | 有 |
| OQ-9 | 先验证 | 一次基线的调用成本与时长 | 有 |

### v5 新增的全称句

| 句子 | 依据 | 结论 |
|---|---|---|
| 「作废只在两种情形发生」 | 定义句 | 定义本身可以; 第二情形的三个条件有两个不可达 (Findings 第 1 条) |
| 「aria-runner 镜像 ... 只预装 aria-plugin」 | Dockerfile | 成立 |
| 「handoff 里它只与两个开发容器配对出现」 | frontmatter 23 / 7 | 按 frontmatter 成立; 正文另记它是 runner 的推送身份 (观察第 3 条) |
| 「自主流水线 (AD10) 至今没有改过 aria-plugin 的任何文件」(两次) | 文中: 配对 + 8 取 2 抽查 | 文中依据不够; 独立证据 (87 个 PR 全为 simonfish, 流水线 PR 由 10cg-ci-bot 发起) 支持「没有合入过改动」, 结论成立 (观察第 3 条) |
| 「(C) 不会阻断任何已发生的工作」 | 同上 | 成立 (需要的只是「没改过 description」) |
| 「自主模式 ... 一律停在 S_FAIL」(Impact、OQ-7) | 由推荐项推出 | 成立; 「停」实际是默认自动重试到预算耗尽 (观察第 1 条) |
| 「场景 4b 只在 Claude 模型上实测过」(D6) | 五份脚本的 `--model` | 成立 |
| 「AD10 规定整条流水线只有 S7_AWAITING_MERGE 一个人工 gate」 | AD10 §决策 | 成立 |

## 实跑记录

1. `python3 aria/skills/state-scanner/scripts/check_bare_issue_refs.py <proposal>` → 「裸 issue 引用: 0」, rc 0; 对 RESULT.md → 同样, rc 0。
2. 禁用字形 (python 逐字符扫, 区间 U+2460–24FF / U+2776–2793 / U+3251–325F / U+32B1–32BF / U+0391–03A9 / U+03B1–03C9): proposal 0、RESULT 0、PREREGISTRATION 0; NUL 字节 0 / 0 / 0。
3. D1 表 (python 分别取 v3 `0c41e53`、v4 `e822829`、v5 三版的 D1 表): 三版旧句逐字相同; 在 CLAUDE.md、SOT、手册中各 1 次 (手册去外层反引号); v5 三条新句各含核心句 1 次; 三个现状文件核心句各 0。
4. SC-1 反事实 (内存中字符串替换, 未写文件): 落 v3 新句 → 红 (CLAUDE.md 缺「另须跑场景 4b」、SOT 缺「另须跑场景 4b」、手册两串都缺); 落 v4 → 绿; 落 v5 → 绿; 落 v5 但删掉 SOT 自主条款与 CLAUDE.md 指向句 → 绿。四种落地的落点行 SC-5 均 0, 「边界四条」1 /「边界三条」0。SC 段「自主 / S_FAIL / unattended / GLM / Claude 模型 / OQ-9」计数全 0, 「D5.6」1。
5. SC-9 (取 D2 小节): v5 原样 fail 行 1 / 作废行 1 → 绿; 删「fail 的后果」行 → 0 / 1 红; 删作废行 → 1 / 0 红。v4 D2 同样结果。
6. SC-5 (python re): v5 D2 + D3 正文去掉含「不设比较判据」的行后 0; 该行原样 1。SC-10: 含「参数钉死」的行 1 行, 四个参数与「20 条」齐全。
7. `run_eval.py`: marketplace 与缓存 `bb335391eb83`、`unknown` 三份 md5 相同 (75269360a221e48f79425605de5e5cb6); 第 88 行 stderr 接 DEVNULL; 第 101 行超时循环; 第 168 / 171 / 178 行 `return triggered`; 第 222–225 行异常 → Warning + `append(False)`; 第 240 行 `"runs": len(triggers)`。
8. v5 `.err` (scratchpad `trigger-results-v5/`): 三份 Warning 行均 0, 末行是逐 query 的 PASS 行; 基线目录中 `.err` 文件 0 个。v5 run.log: 三臂 12:28:13Z 同时起, 12:43:31Z–12:47:54Z 止, rc 全 0。
9. 预登记引文 (python 子串): 「这是对 §D2「只承诺两类破坏」局限的实证确认, 不是守卫失效的证据」在 PREREGISTRATION.md 与 RESULT.md 中各 1 次。RESULT v4 (`e822829`) 第 57 行为「守卫只判得出两类破坏」。
10. proposal 中 RESULT 引用 (grep): 第 9 / 16 / 48 / 50 / 67 / 116 / 129 行为 v5, 第 101 行 (D6) 为 v4。
11. D3 机读实证路径与 RESULT 所列产物共 12 个, `test -e` 全部存在。
12. 架构文书: AD10 §决策「只保留 1 个人类审批 gate」; AD10 §回滚路径 Level 2 原文「在 S5_REVIEWING 中间插入一个 optional human gate (只对高风险 issue 触发)」; AD5 §决策「S_FAIL 作为 universal sink, 可从任意状态进入」(第 401 行), 选型理由第 2 条「任意状态都可进入 S_FAIL」(第 450 行)。
13. layer-boundary-contract: §3 S_FAIL 行 Owner「Layer 1 escalation」, 正文「Layer 1 also owns the failure escalation path (→S_FAIL)」; §4 六类失败模式, 无「按规则拒做」; S_FAIL handling 默认「Acknowledge and let Layer 1 auto-retry (default)」。runner `modes/initial.sh` 有 `CLAUDE_NO_OP` 判定 (claude 退出 0 且无改动)。
14. runner 镜像: `docker/aria-runner/Dockerfile` 装 claude-code CLI 并 `COPY aria/ /opt/aria-plugin/`; `docker/aria-runner/` 与 Nomad HCL 中 skill-creator 0 处 (aria-orchestrator 里只有一份 spike 文档和一份草稿文档提到)。
15. handoff frontmatter `owner-container` 计数: aria-runner-bot/023236f2 23、aria-runner-bot/bfe8285d 7、simonfish/023236f2 26、simonfish/bfe8285d 37; aria-runner-bot/023236f2 按文件名首末为 2026-07-05 / 2026-08-16, aria-runner-bot/bfe8285d 为 2026-09-03 / 2026-09-13。v1.64.0 handoff (`2026-07-22-issue113-ship-v1.64.0-and-rule6-third-row.md`) 属 023236f2; v1.70.0 会话收尾 handoff 属 bfe8285d。另有 8 份 M5 期 handoff 正文提到 aria-runner-bot, 都是 Layer 2 runner 的账号 / 凭据配置。
16. aria 子模块 `git log --all --author=aria-runner-bot`: 33 次提交 (2026-07-05 至 2026-09-06), 其中 chore(release) 8 次。Forgejo: `10CG/aria-plugin` PR 87 个, 发起人全为 simonfish; `10CG/Aria` PR 82 个, simonfish 78 / 10cg-ci-bot 4 (10CG/Aria#28、10CG/Aria#29、10CG/Aria#31、10CG/Aria#121)。
17. M5 文档: `modes/initial.sh` 第 251 行以 aria-runner-bot 凭据改写 clone URL; `docs/handoff/2026-05-19-m5-deploy-playbook-v11-addendum.md` 第 402 行「commit author = aria-runner-bot」(changes 模式 rework 推送到 PR 分支后的预期)。
18. `10CG/Aria#196` open, 标题「unattended 的 Layer 1→2 env 传递三腿契约未定义 — 缺 import 会静默 fallback 到 false」; `10CG/Aria#211` open。phase-a-planner SKILL.md 第 129–131 行为 unattended 的既有约定。
19. `git diff --stat e822829..f169a0b`: 8 个文件 (proposal、RESULT、六份 R4 报告)。主仓 gitlink: aria `1cb3872`、standards `8b49562`; SOT 最后改动仍是 `b98cf73`。
20. 环境: 本 session 主机 dev-claude2, git 身份 simonfishgit; shell 未设 `ANTHROPIC_BASE_URL`。工作区除原有两个 triage 文件与别席 R5 报告外无变动。
21. R4 报告时间: 文件名 12:58:03, 各席 13:22–13:43, 聚合 13:44。

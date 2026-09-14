---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-14T13:34:08.632Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [tech-lead]
---

# post_spec Round 4 — tech-lead 席 (被审 SHA e822829, rework v4)

> 只审不改: 除本报告外没写任何仓库文件, 临时文件都在 scratchpad。独立性: 没读同目录任何 R4 报告; R3 只读了聚合报告和本席报告。远端核验只用 `ls-remote`, 没有 fetch。
>
> **先勘正我自己 R3 的一处事实错误**: R3 Finding 3 把「aria-runner-bot 在 aria-plugin 的 33 次提交」当作「v2.0 自主运行时已经在改 SKILL.md、会发版」的证据。本轮核实: 这个身份是开发容器会话共用的机器提交身份, 这些提交没有一次经过 AD10 流水线 (证据见 Finding 2 论证与核实记录 12)。R3 聚合的 rework 计划和 v4 §OQ-7「事实依据」都照搬了这个归因, 源头在我。R3 写的「两次发版」也数错了, 实为 10 个版本。

## R3 对账

我席 R3 共 5 条 (major 3 / minor 2)。结果: **closed 4 / partially 1 / open 0**。

| R3 条 | 严重度 | 判定 | v4 落点 (段名) 与核实 |
|---|---|---|---|
| 1 门判 fail 之后没有后果 | major | **closed** | §D2 新增「fail 的后果」: fail ⇒ 该改动不得 ship; 处置二选一 (修 description 直到过门 / 有意改触发面时先改套件、升 `ab-suite/version.yaml`、按 OQ-7 审阅再重跑), 两条都不走 ⇒ 升级 owner; rule6_note 记 fail 与所走处置。§D4 合规句由「void ⇒ 不得 ship」改为「fail 或 void ⇒ 义务未完成, 不得 ship」。照字面把 fail 读成合规的空子已堵上。遗留两点不改变判定: SC-9 删掉 fail 那行仍全绿 (Finding 4); 「修到过门为止」没有重试上限 (观察 5)。 |
| 2 只改 description 不跑场景 1 的判据 | major | **closed** | §D1 回改为 fail-closed: 新增「只改 description 时场景 1 还跑不跑: 照跑」段, 理由写明 (能力陈述句两类都沾, 以基线那次真实改动为例), 不设放宽; 三处新句都写「照跑场景 1; description 变动另须跑场景 4b」, SOT 那句还有「两者不互相替代」; 「行为指令句」全文 0 命中; 放宽只留作 OQ-6, 口径带「逐行点名」, 推荐暂不放宽并写了代价。D1 正文 / D5.5 / Impact / OQ-6 与三处新句口径一致 (任务 3)。回改漏掉的两处 v3 残留单列为 Finding 3。 |
| 3 未覆盖 v2.0 Layer 2 | major | **partially** | 已落: §Impact 新增「自主运行时 (v2.0 Layer 2) 的适用性未验证」条; §OQ-7 分交互 / 自主两栏; 新增 §OQ-9 (GLM 上先做三臂基线)。未闭合: OQ-9 推荐「先验证再启用」, 可 T1 三句对自主模式一个字没有, 验证前该怎么办没写, 推荐项的代价也没算这一段; 我 R3 修法里的「写进 SOT §6 局限, 或另开 issue」没做, D6 给 §6 的第三条不提模型 → Finding 1。自主模式栏的「事实依据」沿用了我 R3 的错误归因 → Finding 2 (新发现, 单列)。 |
| 4 SC-2: T2 全路径与 D3 相对路径冲突 | minor | **closed** | T2 改为「机读实证写相对基线目录的完整相对路径」; SC-2 限定只取第三列、第二列不参与、恰六行、[配置推导] 恰一行。按 SC-2 模拟: 6 行 (编号 1–6 各一), 第三列 11 个路径拼上基线目录全部存在, 第 4 行无路径且带 [配置推导] (核实记录 9)。 |
| 5 OQ-7 B 案旧时长 / provisional 不在值域 | minor | **closed** | OQ-7 B 案改为「并行约 11–20 分钟 / 约 10 美元」, 与 §Impact、§OQ-3 同数; §D4 新增「套件未经 owner 审阅时 scenario4b 结果后缀 provisional」。 |

## Findings

- [major] architecture/proposal.md §Impact+§OQ-7 (risk): R3 未闭合部分。OQ-9 推荐先在 GLM 上验证再启用, 但 T1 三句对自主模式没有条款, 验证前遇到 description 改动怎么做、推荐项的代价都没写; 「4b 只在 Claude 模型上验证过」没进 D6 的 SOT §6 也没开 issue, 归档后规范里不留痕。
- [major] architecture/proposal.md §OQ-7 自主模式 (issue): 「事实依据」归因错: aria-runner-bot 的 33 次提交出自开发容器会话 (机器提交身份, standards §2.3.9), 没有一次经过 AD10 流水线或 S7; 缺运行模式判据, 交互会话可能误走 B 案; 真 aria-runner 镜像没装 skill-creator, B 案跑不起来。源头是我 R3 的误判。
- [minor] documentation/proposal.md §D1+§D4 (issue): v3「description 只跑 4b」逻辑的两处残留: D1 定的 SOT §3 边界注仍只写「场景 4b 义务」; D4 合规清单只核 scenario4b, `description_changed: yes` 配 `scenario1: not_required` 不判不合规。T1 / T3 逐字转录, 进 Phase B 前须改。
- [minor] testing/proposal.md §SC-9 (issue): 反事实不成立: 手册 §4b 删掉「fail 的后果」整行, 作废那行仍含「不得 ship」, SC-9 照样全绿, R3 major 的修复没有机械锁; 应像 SC-10 一样按行判。

## Findings 论证

### Finding 1: Layer 2 覆盖还差两段

**验证前的中间态没定义。** T1 落地的三句对所有执行者生效, 没有「自主模式除外」。owner 若采纳 OQ-9 的推荐 (先验证, 再让自主模式按 4b 判门), 验证做完之前, 自主模式碰到 description 改动, 执行者只有三条路:

1. 照跑一个没验证过的门 —— 与 OQ-9 推荐的本意相反;
2. 当作「4b 在自主模式未启用」跳过 —— 没有成文依据, 是 Rule #10 明令禁止的自行豁免;
3. 不 ship, 经 S_FAIL 升级 owner (fail-closed)。

第 3 条与现有规则相容, 大概率也是作者的本意, 但 proposal 没写它是默认, 也没把「验证完成前, 自主模式里所有 description 改动都 ship 不了」算进推荐项的代价。推荐项必须带上它真实的代价, owner 才能裁。

**规范里不留痕。** proposal 归档之后, 执行者读的是 SOT 和手册。D6 给 SOT §6 的第三条写了饱和、两类破坏、自然扩张不判红、无机械 enforcement, 唯独没有「阈值、负控门槛和前置只在 Claude 模型 (`claude-fable-5-1` / `claude-opus-5`) 上验证过」。GLM 上的执行者从规范里读不到这条局限, 会把 4b 的「通过」当真。我 R3 的修法原文是「写进 SOT §6 局限, 或另开 issue」, v4 两样都没做。

**修法 (纯文字, 不用重跑)**: OQ-9 推荐项补一句「验证完成前, 自主模式的 description 改动按 fail-closed 处理: 不得 ship, 经 S_FAIL 升级 owner; 这是本推荐的代价」; D6 第三条补「阈值与负控门槛只在 Claude 模型上验证过」。

### Finding 2: 自主模式栏的事实依据归因错, 且没有运行模式判据

**数字对, 归因错。** v4 §OQ-7 自主模式栏写「事实依据: aria-runner-bot 在 aria-plugin 已有 33 次提交, 其中 6 次改 SKILL.md、至少 4 次发版; 截至 2026-09-14 这 6 次都没改 description」。33 / 6 / 0 次改 description 我都机械复核过, 成立 (核实记录 1–4)。但这些提交不是自主模式产生的:

- standards `conventions/session-handoff.md` §2.3.9 (2026-09-06 owner 裁定 D-2) 规定: AI 会话的 git 提交身份统一为机器身份, 「操作者可追溯性由 `<container-id>` + handoff 正文承担」。aria-runner-bot 标识的是「用哪个账号提交」, 不标识「有没有人在场、走不走流水线」。
- 这个身份新增的 31 份 handoff: owner-container 字段 22 份是 `aria-runner-bot/023236f2`、6 份是 `aria-runner-bot/bfe8285d`、3 份写 `simonfish/...` 或 `dev-claude`; Feishu / S7_ / S4_LAUNCH 这类流水线字样 31 份全是 0; 19 份有「owner 裁定 / 授权 / 接受」一类字样 (粗 grep)。
- 发版那几次也是交互: v1.70.0 的 handoff 写着 owner 裁定 D-0 a / D-1 a / D-2 a / D-3 a、owner 两次加审计轮、owner 裁定 D5 MINOR、PR #197 由 owner 授权, 然后本地 `--no-ff` merge 加 tag —— 有人在场, 也没经过 S7。同一份 handoff 把 `023236f2` 叫做「双子星」(owner 的第二个交互实例), 并记录 `023236f2` 与 `bfe8285d` 两个容器各自都用过 `aria-runner-bot` 和 `simonfish` 两个身份。
- AD10 流水线至今没在生产闭环: M6 输入投递分支 `feature/m6-dispatch-input-delivery` 没合入 aria-orchestrator `origin/master`; 07-02 那次自主路径试跑, 容器在 Step 1 就因 ISSUE_ID 正则 FATAL。aria-plugin 里任何已合入的提交都不可能来自这条流水线。

所以这组数字证明的是「用机器身份提交的开发容器会话在改 SKILL.md、会发版」, 不是「自主运行时已在改 SKILL.md」。「该场景尚未实际发生」这个结论仍对, 但理由应该是「流水线还没闭环」, 而不是「6 次都没改 description」。

**没有运行模式判据, 会让执行者做错事。** OQ-7 按运行模式分 A / B 两案, 却没说执行者靠什么判断自己处在哪种模式; proposal 里唯一具体的锚点就是 aria-runner-bot。设想 owner 按推荐裁了「交互 A / 自主 B」: `bfe8285d` 里的会话用的正是 aria-runner-bot 身份, 读到「自主模式 (v2.0 Layer 2, aria-runner) …… aria-runner-bot 在 aria-plugin 已有 33 次提交」, 很可能把自己归为自主模式, 走 B 案 (不等 owner 预审, 结果标 provisional, 「审阅并入 S7」)。可它的会话根本没有 S7 (v1.70.0 就是本地 merge 加 tag), provisional 结果永远等不到审阅; 按推荐它本应走 A 案, 先等 owner 审套件。判据应按「本 cycle 是否由 Layer 1 派发、下游是否有 S7 签字」来定, 不按 git 身份; 没有 S7 的无人值守会话 (如 /goal 直驱) 按交互模式 A 处理, 或停下升级。

**B 案在真 runner 里跑不起来, 「只能 B」也排除了别的选项。** `aria-orchestrator/docker/aria-runner/Dockerfile` 只装了 claude-code CLI 并 `COPY aria/ /opt/aria-plugin/`; Dockerfile、entrypoint、modes、lib 里都没有 skill-creator 或任何插件安装步骤, aria 插件本身也不含 skill-creator。场景 4b 要用 skill-creator 的 `run_eval.py`, 场景 1 要用 `/skill-creator`, 这个镜像里两样都没有, 所以「cycle 作者建套件并跑」目前不可执行。另外, AD10 选型理由第 4 条自己写了「未来运行稳定后可增加 gate (往 2 gate 退化)」, A 案需要的是 owner 修订 AD10, 不是「不可能」; 「Layer 1 不派发含 description 改动的任务, 留给交互模式」这条路 proposal 也没列。「可行做法只有 (B)」把这些选项替 owner 排除了。

**修法 (纯文字)**: 事实依据改写为「aria-runner-bot 是机器提交身份 (§2.3.9), 交互会话也用它; AD10 流水线尚未在生产闭环, 自主模式改 description 的情形没有发生过」; 加运行模式判据 (按有无 Layer 1 派发与 S7 签字, 不按 git 身份); 自主模式的选项写全 (B 且审阅并入 S7 / Layer 1 不派发这类任务 / owner 修订 AD10), 各带代价, B 案注明「前提: runner 镜像装 skill-creator, 属 aria-orchestrator 改动, 不在本 Spec 范围」。

### Finding 3: D1 回改没覆盖到的两处

三处新句、D1 正文、D5.5、Impact、OQ-6 这几处口径一致 (任务 3)。v3「description hunk ⇒ 场景 4b」的逻辑还留在两处:

- **SOT §3 边界注**。D1 正文要求在 SOT §3 末尾加「description hunk 不走本节, 走 §2 第二行的场景 4b 义务」, 这句 v3、v4 一字未改。v3 时它与「description ⇒ 4b」一致; v4 改成「场景 1 另加 4b」后, 它仍只提 4b, 「§2 第二行的场景 4b 义务」也可以读成「第二行底下那条 4b 义务」。SC-10 只锁前半句「description hunk 不走本节」, 改后半句不影响 SC。
- **D4 合规清单**。v3 允许「只涉及触发面时不跑场景 1」, 那时 `description_changed: yes` + `scenario1: not_required` 是合法组合; v4 取消了放宽, 这个组合就该判不合规, 可清单只写了 scenario4b 的三种不合规取值和 fail / void (v3 到 v4 这一句只把「void」改成了「fail 或 void」)。§D4 自己写着「无机械 enforcement, 合规靠审阅」, 审阅者手里就是这张清单。结构和我 R3 Finding 1 一样: 清单明确列了一部分, 没列的就等于放行。同理, `description_changed: yes` 时 `decision_table_row` 按 SOT §2「一律第二行」只能是 2, 清单也没写。

T1 与 T3 是逐字转录进 SOT 的, 所以要在 Phase B 前改。**修法**: 边界注改成「走 §2 第二行 (照跑场景 1, 另加场景 4b)」; D4 清单加「`description_changed: yes` 而 `scenario1` 不是结果目录, 或 `decision_table_row` 不是 2 ⇒ 不合规」。若 OQ-6 裁为放宽, 再补放宽条件下的写法。

### Finding 4: SC-9 删掉 fail 那行照样全绿

SC-9 按小节计数: 「≤ 5/10」「连续 2 轮」「不得 ship」各 ≥ 1 次。D2 里含「不得 ship」的有两行: 作废那行和「fail 的后果」那行。对 D2 原文做反事实: 删掉「fail 的后果」整行后, 「不得 ship」仍有 1 次 (作废行), 另两个串也各 1 次, SC-9 仍绿 (核实记录 9)。也就是说, T2 转录时如果把 R3 major 的修复整条漏掉, 验收查不出来。这和 R3 qa 席对 SC-10 做的反事实是同一类问题, v4 已把 SC-10 改成按行判; SC-9 应同样处理: 含「fail 的后果」的行须含「不得 ship」, 含「作废 =」的行须含「不得 ship」。SOT §4.1 那两条合规句 (D4) 目前也没有 SC 断言, 可一并补。

## 任务 2: 事实核实结论

| 事实 (v4 原文或其用法) | 结论 | 依据 |
|---|---|---|
| aria-runner-bot 在 aria-plugin 的提交 33 次 | 成立 | 核实记录 1 |
| 其中 6 次改 SKILL.md | 成立 (非 merge 提交; 另有 2 个 merge 带入同批改动) | 核实记录 2 |
| 至少 4 次发版 | 作为下界成立, 实为 10 个版本 (观察 1) | 核实记录 4 |
| 0 次改 frontmatter description | 成立 (11 处文件改动的 frontmatter 全部逐字节相同) | 核实记录 3 |
| 以上提交可作「自主模式」的事实依据 | **不成立** (Finding 2) | 核实记录 12 |
| AD10: 整条流水线只有 S7_AWAITING_MERGE 一个人工 gate | 成立 | 核实记录 11 |
| (A) 在 S7 之外再加 gate, 与 AD10 冲突 | 成立, 但属「要 owner 修订 AD10」, 不是「不可能」 | AD10 选型理由第 4 条 |
| 可行做法只有 (B) | **不成立** (漏列选项; B 在真 runner 里跑不起来) | 核实记录 13 |
| v5 三臂数字 | 成立 | 核实记录 5、8 |
| v5 按预登记判读 | 成立, 预登记先于结果 | 核实记录 6、7 |
| OQ-9: Luxeno 延迟 45–54 秒 / 次, 三臂并行约 50 分钟 | 数字、单位、算术都对; 来源背景未交代 (观察 8) | 核实记录 15 |

## 任务 3: 新引入问题检查

- **D1 口径**: 三处新句都含核心句 (Python 按字节比对为真), 都写「照跑场景 1; description 变动另须跑场景 4b」。D1 正文「description hunk ⇒ 场景 1 另加场景 4b, 两者不互相替代」、D5.5「凡跑场景 1 (包括只改 description 时)」、Impact「照跑场景 1 + 场景 4b 地板守卫 + rule6_note 五字段」、OQ-6「本 Spec 默认不放宽 (D1)」—— 这几处一致, 没有新冲突。不一致只在回改没覆盖的两处 (Finding 3)。SC-5 正则对三处新句均 0 命中, 核心句不会被误判成比较句。
- **OQ-7 与 AD10**: 「AD10 只有 S7 一个人工 gate」与「A 案与 AD10 冲突」都能在原文里找到依据; 「只能 B」和「事实依据」有问题 (Finding 2)。另有一点放观察: D2 的「升级 owner」在自主模式可走 layer-boundary-contract §4 的 S_FAIL 加 Feishu 告警, 是失败出口, 不是 AD10 意义上的审批 gate, 两者不冲突, proposal 可补一句, 免得被读成第二个 gate。
- **OQ-9 引 Blocker 4**: CLAUDE.md 项目状态只写「Luxeno 后端延迟 45-54s」, 没单位; 源头 `docs/handoff/2026-07-02-m6-preflight-luxeno-blocker.md` 写「45-54s/call」, 与 proposal 的「45–54 秒 / 次」一致; 60 次 × 45–54 秒 = 45–54 分钟, 三臂并行约 50 分钟, 算术对。**引用正确**, 背景缺口见观察 8。
- **v5 与预登记**: 判读规则三条逐条对照, 解读按预登记执行, 没有事后改口 (核实记录 6、7)。表述上的小出入放观察 2、3、4。

## 观察 (不进收敛比较键, 不影响 vote)

1. 发版次数: bot 身份提交改动 `plugin.json` version 的共 10 个版本 (v1.53.0 到 v1.70.0), 「至少 4 次」作为下界成立; Finding 2 改写时建议直接写实数。我 R3 写的「两次发版」数错, 一并勘正。
2. v5 mildcreep 的描述不全: RESULT v4 表写「原文 + 四处」, D2 写「多加三处」; 实际 mildcreep 还把「到 openspec/archive/ 目录」改成了「与相关文档到 archive/ 目录」—— 去掉 `openspec/` 路径限定本身就是一种扩张, 而套件的 should-not 里正有 archive 分层脚本、tar 归档、git 分支归档这几条。脚本与预登记里是原文, 结论不受影响, 描述应如实。
3. 预登记写「mildcreep 判敏感当且仅当至少一条 should-not ≥ 0.5 (即门判 fail)」: 门也会因 should-trigger 掉下去而 fail, 括号里的「即」不完全等价。本轮 mildcreep should 30/30, 不影响判读; 以后写预登记可把两侧分开写。
4. D2 负控构造条把 v3 (fable) 负控 3/10 与 v5 (opus) 负控 0/10 并列, 没写模型不同; 预登记自己写了「只做臂间比较, 不与 v3 数字直接比」, RESULT v4 也写了「模型不同不直接比」。建议 D2 这句补「模型不同, 只作方向参考」。
5. 「修正 description 直到门通过」没有重试上限 (作废有「连续 2 轮」)。每 query 3 次、门槛 2/3 时, 单次触发率 0.5 的 query 每轮过门概率 0.5, 三轮内至少过一次的概率 0.875。建议: 只做微调就重跑的, 以连续两轮通过为准, 或设上限后升级。
6. 处置 (2)「有意收窄或拓宽触发面 ⇒ 先改套件」的「有意」可以在看到 fail 之后才声明。建议要求意图在跑 4b 之前写进 spec 的 What Changes, 事后声明的不走这条路 (与 v5 预登记同一纪律)。
7. D4 模板每个 cycle 只能记一个 `scenario4b` 值; D2 要求记 fail 与所走处置, 修好重跑通过后该记哪一个没说。建议写成「最终结果 + 历次结果目录」。`decision_table_row` 单值 (R3 观察) 仍未注明可多值。
8. OQ-9 的时长依据: 45–54 秒来自 07-02 的两次 **Layer 1** 调用 (44567ms / 53944ms), 08-26 handoff 记最后一次实测是 07-12, 09-05 handoff 记为「20 tok/s 越 60s timeout」; 测的不是 Layer 2 的 Claude Code 会话。D2 又钉死 `--timeout 120`, 而 `run_eval.py` 超时按「未触发」计。在 20 tok/s 的后端上, Claude Code 的大系统提示加思考可能顶到 120 秒, should-trigger 会被系统性判掉, OQ-9 的验证基线可能先撞上这个参数 (改超时按 D2 要 owner 裁)。建议写进 OQ-9 的代价。
9. D2 套件条「近似误触须覆盖该 skill 最可能被扩到的相邻任务」没法判定 (「最可能」无定义, 无 SC); 括号里「本套件对整理收尾材料这一幅度的扩张不敏感」容易被读成「本套件不满足上一句」, 而 T4 正要把这份套件搬进 `ab-suite/`。建议写清这是对 query 覆盖面的要求, openspec-archive 套件是否满足在 OQ-3 审阅时一并判。
10. OQ-7「PR 里带套件与 4b 结果」: 套件和结果在主仓 `aria-plugin-benchmarks/`, SKILL.md 在 aria-plugin 仓; 应写明 S7 签的是哪个仓的 PR (主仓 PR 连 gitlink 一起审, 还是两个 PR)。
11. 时长取整: v5 里「被评 + 负控」的真实组合 (mildcreep + negctrl / new + negctrl) 并行都是 19m41s、串行 34m59s / 37m57s; RESULT「opus 上并行约 16–20、串行约 34–38」的 16 和 34 取整略低。proposal 用的「11–20 / 22–38」作为包络仍成立。
12. memory 源头: `project_aria_runner_bot_autonomous_same_repo_work` 把 `023236f2` 称为「Layer 2 自主运行时容器」, 与 v1.70.0 handoff 称 `023236f2` 为「双子星」冲突。我 R3 的误判即由这条 memory 带出, 建议 owner 复核该条 memory (本席只审不改, 未动)。
13. 顺带发现 (不属本 Spec): `aria-orchestrator/docker/aria-runner/modes/initial.sh` 的 `CLAUDE_ARGS` 只有 `--model` / `--output-format stream-json --verbose` / `--settings`, 没有 Dockerfile 注释写的 `--plugin-dir /opt/aria-plugin`。runner 是否真加载了 aria-plugin 存疑, 与 CLAUDE.md「Layer 2 …… aria-plugin 完整加载」的说法可能不符, 建议 orchestrator 侧另行核实。
14. R3 观察里未被吸收、仍建议的: (a) 4a「原样保留」会连带保留手册第 273 行「触发时机: 修改 Skill 的 description/frontmatter 后」, 与「4a 是可选优化」矛盾; (b) T1–T3、T5 没声明依赖 OQ-5 / OQ-6 的裁定 (OQ-5 若裁为 issue 字面路径, T1 新句整句作废); (c) 生效点未写 (建议: T7 gitlink bump 进主仓 master 之后进入 C.2 的 cycle 适用); (d) D5.3 那张 issue 的基线污染预警。

## Verdict

PASS_WITH_WARNINGS —— critical 0 / major 2 / minor 2。

我席 R3 的 5 条: closed 4 / partially 1 / open 0。门的判定语义这一块 v4 改得干净: fail 有了后果; 「只改 description 不跑场景 1」这条放宽整条撤回, 相关几处口径一致。v5 是一次合格的预登记实验: 规则写在结果之前 (文件时间可证), 三臂数字从原始 json 重算全部对上, 解读照预登记执行。

仍投 REVISE, 原因是两条 major, 都在 Layer 2 上:

- R3 第 3 条的剩余部分: OQ-9 推荐的「先验证」缺了验证前的做法和代价, 「只在 Claude 上验证过」没进规范;
- 自主模式栏的事实依据归因错, 缺运行模式判据, B 案在真 runner 里跑不起来。这条错的源头是我 R3 的误判, 我在此明确撤回 R3 关于「自主提交」的说法。

两条 minor 都是要逐字转录进 SOT / 手册的文本, 改起来成本很低, 放在 Phase B 前改。全部修改都只动文字, 不用重跑基线。

## Vote

REVISE

## 数据核实记录

核实方式: 全部直接读原始产物或 git 对象重算, 不拿 RESULT.md / proposal 里的数字当依据。

1. **aria-runner-bot 提交数**: `git -C aria log --all --author=aria-runner-bot` = 33。`git ls-remote origin` 191 个 ref、`git ls-remote github` 95 个 ref, 逐个 `git cat-file -e` 全部在本地 ⇒ 没有未抓取的远端提交, 33 即全量。
2. **改 SKILL.md 的提交**: `--no-merges -- '*SKILL.md'` 得 6 个: `17cd3d0` (phase-c-integrator) / `e3d54f3` (openspec-archive) / `ae35d19` (openspec-archive) / `c8287cd` (openspec-archive + phase-d-closer + state-scanner) / `3b102a0` (openspec-archive) / `70adcbc` (openspec-archive + phase-d-closer)。merge 提交按第一父 diff: `b9f5446` / `3694871` 带入同批改动。
3. **frontmatter 前后对比**: 对上述 8 个提交的 11 处文件改动, 用 PyYAML 解析 `git show <parent>:<f>` 与 `git show <c>:<f>` 的首个 `---` 块: frontmatter 全部逐字节相同, description 全部相同 ⇒ 0 次改 description。
4. **发版**: 逐提交读 `.claude-plugin/plugin.json` 的 version, bot 身份提交改变 version 的共 12 个提交、10 个不同版本 (1.53.0 / 1.54.0 / 1.59.0 / 1.59.1 / 1.61.0 / 1.63.0 / 1.64.0 / 1.65.2 / 1.65.3 / 1.70.0; 1.64.0 与 1.70.0 各有一个 merge 提交重复出现)。指向 bot 提交的 tag 只有 v1.70.0 → `0545f86`。
5. **v5 三臂重算** (json.load 逐 query 累加): new should 30/30 (query 级 10/10)、should-not 0/30 (≥ 0.5 的 0 条)、20/20 pass; negctrl should 0/30 (0/10)、should-not 0/30; mildcreep should 30/30 (10/10)、should-not 0/30, 10 条 should-not 全 0/3 (含预登记点名的 handoff 归档 / tar 归档审计报告 / archive 分层脚本 / sprint changelog 四条)。三份 json 的 `pass` 字段与 `did_pass` 语义重算一致。三份 json 的 `description` 字段与预登记原文逐字相同; new 的 description 与 aria `v1.73.0` 的 openspec-archive frontmatter 相同。
6. **预登记判读规则逐条对照**: new 过门 ⇒ 可以解读 mildcreep; negctrl 0/10 ≤ 5/10 ⇒ 本轮有效; mildcreep 0 条 should-not ≥ 0.5 ⇒ 按预登记判「该幅度的自然扩张不被守卫判为改坏, 是局限的实证确认」。proposal §Why 第 2 条 / §D2 / §OQ-8 / §D6 与 RESULT v4 都照此表述。
7. **预登记先于结果**: scratchpad 原件 `trigger-results-v5/PREREGISTRATION.md` 的 mtime 为 2026-09-14 12:28:13.730Z, run.log 三臂 start 为 12:28:13Z, 最早的结果 json mtime 为 12:43:31 ⇒ 原件写于运行开始前、结果产生后没被改过。仓内副本与原件 `diff` 为空; run.log、三份 json、run_arms_v5.sh 也 `cmp` 相同。模型: run_arms_v5.sh 传 `--model claude-opus-5` (json 本身不记模型)。
8. **v5 时长**: mildcreep 15m18s / new 18m16s / negctrl 19m41s ⇒ 「15m18s–19m41s」成立; 「v2–v5 共 13 臂」= 4 + 4 + 2 + 3 成立。
9. **SC 模拟** (Python 读 v4 proposal): SC-1 核心句在 D1 三行新句里按字节均命中; SC-5 正则在三行新句与 D2 正文 (去掉「不设比较判据」行) 均 0 命中; SC-2: D3 表 6 行、编号 1–6、第三列 11 个路径全部存在、[配置推导] 恰 1 行; SC-9 反事实: 删掉 D2「fail 的后果」行后, 「不得 ship」仍 1 次 (作废行), 「≤ 5/10」1 次, 「连续 2 轮」1 次 ⇒ SC-9 仍绿。
10. **旧句与 v3 对比**: 三处旧句 `grep -cF` 各 1 (CLAUDE.md / SOT / 手册)。「行为指令句」v4 全文 0 命中。`git show 0c41e53` 的 v3 D4 合规句为「`scenario4b` 为 `void` ⇒ 义务未完成, 不得 ship」, v4 只改成「`fail` 或 `void`」, scenario1 相关规则 v3、v4 都没有。SOT §3 边界注的写法 v3、v4 一字未改。
11. **AD10 原文** (`aria-orchestrator/docs/architecture-decisions.md` §AD10): 「Aria 2.0 流水线只保留 1 个人类审批 gate, 位置在 S7_AWAITING_MERGE …… 不在 dispatch 前 (S1→S2) 设 human gate, 不在 review 中段 (S5→S6) 设 human gate」; Option A (dispatch + merge 两个 gate) 以「违反自主 SDLC 前提」被拒; 选型理由第 4 条「可逐步收紧或放松: 未来运行稳定后可增加 gate (往 2 gate 退化) 或减少 gate」。`layer-boundary-contract.md` §3 表 S_FAIL 行「Crash recovery + Feishu alert to owner」, §4「S_FAIL handling」第 1 步即时 Feishu 告警。
12. **运行模式归因**: standards `conventions/session-handoff.md` §2.3.9 原文见 Finding 2 论证。主仓里 bot 身份新增的 handoff 31 份: owner-container 22 份 `aria-runner-bot/023236f2`、6 份 `aria-runner-bot/bfe8285d`、2 份 `simonfish/...`、1 份 `dev-claude`; grep「Feishu|S7_|S4_LAUNCH|Layer 1 派|dispatch 派」31 份全 0; grep「owner (裁|授权|指示|拍板|接受|确认|加)」19 份 > 0 (粗计数); 3 份提到 /goal。v1.70.0 handoff (`2026-09-06-owner-container-identity-key-shipped-v1.70.0-archived.md`, bot 身份提交) §0 第 4 条「双子星 `simonfish/023236f2`」, §1 表 A.1 / A.2 / C 行的 owner 裁定与授权, §2 末条 identity_advisories「`023236f2` / `bfe8285d` 各 `[aria-runner-bot, simonfish]`」。`git -C aria-orchestrator merge-base --is-ancestor origin/feature/m6-dispatch-input-delivery origin/master` 为否。07-02 handoff 第 15 条: 自主 ISSUE_ID 撞容器 `initial.sh` 正则 FATAL。主仓另有 238 个 bot 身份提交, 最近的 09-13 几个是 claim、会话收尾 (session-closer)、决策单追加 —— 同样是交互会话的形态。本 Spec 自身的四个提交作者是 simonfishgit。
13. **aria-runner 镜像**: `docker/aria-runner/Dockerfile` 的安装步骤只有 apt 包、`npm install -g @anthropic-ai/claude-code@latest`、`COPY aria/ /opt/aria-plugin/`, 并设 `GIT_AUTHOR_NAME="aria-runner-bot"`; 在 Dockerfile / entrypoint.sh / modes / lib 里 grep「skill-creator|plugin install|marketplace|enabledPlugins|settings.json|plugin-dir|.claude/」除 Dockerfile 一行注释外 0 命中; `aria/skills` 下没有 skill-creator (只有 agent-creator)。`modes/initial.sh` 的 `CLAUDE_ARGS` 为 `claude -p ... --model ... --output-format stream-json --verbose --settings ...`, settings 只含 permissions / env / model。
14. **`run_eval.py` 超时语义** (插件缓存 `skill-creator/bb335391eb83`, `run_single_query`): `while time.time() - start_time < timeout` 循环结束后走到 `return triggered`, `triggered` 初值 False ⇒ 超时按未触发计; 第一个 tool_use 若不是 Skill / Read 立即返回 False。
15. **Blocker 4 源头**: 07-02 handoff 第 13 条「两 Layer 1 LLM call `ok (44567ms)` + `ok (53944ms)`」, 同文件第 52 行「45-54s/call (健康 <5s)」; 08-26 handoff「该延迟最后一次实地核查是 2026-07-12」; 09-05 handoff「20 tok/s 越 60s timeout」。CLAUDE.md 项目状态行「Blocker 4: Luxeno 后端延迟 45-54s」无单位。
16. **同批提交**: `git show --stat e822829` 同时含 proposal.md、RESULT.md、run_arms_v5.sh 与 v5 目录五个文件 ⇒ 抬头「与本版同批提交」属实。

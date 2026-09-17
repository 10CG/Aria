---
checkpoint: post_spec
mode: convergence
rounds: 7
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
drift_warning: false
is_refocus: false
verdict: PASS
timestamp: 2026-09-17T00:09:16.000Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [tech-lead]
---

# post_spec Round 7 — tech-lead 席 (被审 SHA 15ab323, v8; 本次审计最后一轮)

> 只审不改: 除本报告外没写任何仓库文件; 脚本与重跑产物在 `/tmp/claude-1000/-home-dev-Aria/e91a9d6a-05ff-4b26-af79-8d903c21a292/scratchpad/r7-tech-lead/` (`desc_scan.py` / `fm` / `fm2` / `v8_added.txt` / `v8_removed.txt`)。独立性: 没读本轮其他席的 R7 报告; 读了 R6 聚合报告 (含 owner 裁定) 与本席 R6 报告。远端零操作 (无 fetch / push / API 写)。
>
> 本轮的机械复核一律自己重跑, 不引用 R6 各席的转述: description 影响面用独立重写的扫描脚本 (记录 3), 故障矩阵用 `fault_matrix.py` 独立重跑 (记录 4), 编排器与 runner 行为直接读代码 (记录 16、17)。

## R6 对账

我席 R6 共 4 条 (major 3 / minor 1)。结果: **closed 4 / partially 0 / open 0**。

| R6 条 | 严重度 | 判定 | v8 落点与核实 |
|---|---|---|---|
| 1 禁令只说「不提交」, 没要求撤销; runner 会替 Claude 提交工作区残留并开 PR, 照字面守禁令正落进它要防的「部分交付按成功推进」; 且 D1 依据句「整单不提交必进 S_FAIL」不成立 | major | **closed** | 三处都改了。(1) D1 表 SOT 行与 D1 正文的禁令改成「放弃整个任务, 撤销本任务已做的全部改动 (工作区不留未提交的改动, 分支不留新提交), 并在最终消息里写明是哪个 skill、为什么要改」——「不提交」这个可被 runner 兜底覆盖的形状没有了。(2) 失实的依据句整句删除, 换成指向 D5.6 已知缺口第 (3) 条的说明「留在工作区的半成品会被当成一部分交付」。(3) D5.6 已知缺口第 (3) 条按代码逐条写明 runner 补提交 (initial 模式 Step 10) 与 rework 模式「有 diff 且推送成功即 PASS」, 并补上「禁令只靠 Layer 2 遵守指令, 没有机械兜底」与 runner 提示词自相矛盾两句 (我 R6 观察 5、10 一并吸收)。(4) SC-12 加锁「撤销本任务已做的全部改动」, 对 v8 的 SOT 行自检五串全在 (记录 13)。代码侧复核: `initial.sh` Step 8 判 NO_OP、Step 10 `git add -A` + `git commit`; `changes.sh` `git add -A` → commit → force-push → 写 `outcome":"PASS"` (记录 17) —— v8 的转述与代码一致。 |
| 2 同批参照臂在三种正当情形下必然作废 (有意改套件划分 / 新增 skill / 修复已坏 description); 新增 skill 是否属 4b 未界定, 两种读法结果相反 | major | **closed** | 参照臂整条删除, 换成逐调用健康检查 (D2 三条 + D3 第 3 / 5 行), 三种情形逐条不再作废, 论证见下节「新设计是否站得住」。新增 skill 的歧义也消了: D2 套件条末句明写「新增 skill 的首个 description 同样要过本场景, 其首个套件随之建立」, D1 禁令括注「(含新增 skill)」, OQ-9 把这一选择挑明并给推荐与代价 —— R6 说的「文本没挑」不再成立。残留只到观察层: OQ-9 若被裁为「不算」, 该改哪两处已定稿文字没点名 (观察 1)。 |
| 3 §Impact 与 D5.6 的「默认自动重试、反复告警」与代码相反 | major | **closed** | v8 §Impact 改为「进 S_FAIL, 失败类型记为 `container_crash`, 这是终态 —— 不自动重试, 默认也不告警, Claude 在最终消息里写的原因编排器不读 ⇒ 这类任务会停在那里无人察觉」; D5.6 旁注「这类失败本来就不自动重试, 目标设计里真正缺的是告警与原因传递」, 已知缺口第 (1) 条与第 (8) 条 (契约文档与代码漂移) 到位。逐条对代码复核 (记录 16): `_RETRYABLE_FAIL_REASONS = {infrastructure, timeout}` 且 `_RETRY_COUNT_MAX = 1` ⇒ `container_crash` 永不重试; `ARIA_FAILURE_ANALYSIS_ENABLED` 未设即整段跳过; `notify_owner` 才发一张 best-effort 飞书卡且为终态; `fail_detail` 实际内容是 `S5_AWAIT: alloc terminated with exit_code=<n> alloc_id=<id> (container_crash)` —— 「只有退出码与 alloc id」逐字成立; `mark_failed` 各调用点无飞书调用。v8 这一段现在每一句都能对上代码。 |
| 4 D5 第 7 项没随收窄删除, 与「三张 issue」冲突 | minor | **closed** | D5 现恰 1–6 六项, 无第 7 项; 原第 7 项的实质 (「编排器不消费 runner 结果枚举」「部分交付会按成功推进」) 并入 D5.6 已知缺口第 (2)、(3) 条。「三张 issue」在抬头、Key Deliverables、T6、SC-6 四处一致 (记录 18)。 |

## 新设计是否站得住 (任务 2)

### 能不能接替参照臂的目的

参照臂唯一站得住的目的是: `run_eval.py` 把报错、超时、非零退出都记成一次「未触发」, 需要一个办法把环境故障与「真没触发」分开。逐调用健康检查直接在这一层做, 而不是靠另一条臂的统计影子, 所以它在这个目的上**严格强于**参照臂:

- **对位准确**: 检查用的四个判定事件 (tool_use 开始 / `message_stop` / 含 tool_use 的 assistant 消息 / 结果帧) 与 `run_single_query` 的四个提前返回点一一对应 (记录 7 逐行核过源码)。参照臂只能事后猜「这一轮环境是不是坏了」, 检查能指名道姓说「第几次调用坏了、坏在哪一类」。
- **接得住 R6 点名的两种漏检**: 故障只落在被评臂 (S2) 与故障落在 should-not 半程 (S1, run_eval 门判「假绿」) 都判 void —— 我独立重跑的矩阵里这两例都对上了预期 (记录 4)。
- **不再对正当情形误伤**: 三种情形逐条看 —— (1) 有意改套件划分: 判定只用新套件 + 被评臂 + 负控, 负控的判据是「should-trigger 命中 ≤ 5/10」, 与 should / should-not 标签怎么划无关, 改划分不再自动作废; (2) 新增 skill: 不需要「改动前的 description」, 负控照常构造, 4b 跑得起来; (3) 修复已坏 description: 同理, 被评的是修好之后的那版, 没有旧版必须过门这一条。三处都消失, 不是搬家。
- **粒度合理**: 「不健康调用按触发 / 未触发两种可能都算, 判定不变才有效」这条把作废限制在故障真能翻转结论的时候。矩阵里只坏一次 run 的 S6 / S7 判 pass, 坏到能翻转的 S8 / S10 判 void, 方向正确。

数学上也站得住: `judge()` 对 should-trigger 取下界 `max(0, triggers - 可能被记成触发的不健康数)`、对 should-not 取上界 `min(runs, triggers + 全部不健康数)`, 两侧都朝不利方向取; 负控用命中数上界比 5。没有一处把不确定性算到自己有利的一边。

### 还能漏过什么, 会不会误判

我按「故障能不能既改变结论又躲过检查」逐类过了一遍, 结论是**模型化的故障类没有漏网, 但检查的覆盖面比「识别环境故障」这个说法要窄**:

- **崩溃 / 提前退出 / 挂起 / 超时 / 报错结果帧 / 垫片不在 PATH / 判定事件卡在超时余量**: 七类加一类全部 void, 我重跑确认 (记录 4)。日志数对不上 runs、query 对不上输出也 void。这些都是 fail-closed。
- **漏得过的那一类**: 调用正常完成、帧齐全、耗时正常, 但答案本身被环境带偏 —— 例如 `--setting-sources project` 或 `--model` 没真正生效、项目根里混进了别的技能。这类调用在检查眼里完全健康。两个方向各有间接兜底: 偏向「触发过多」会被负控 ≥ 6/10 接住; 偏向「触发过少」会让被评臂门判 fail。但兜底不是证据, 而且第二个方向落在 fail 而不是作废上 —— 这是删掉参照臂之后唯一真实的单侧盲区 (观察 2、3)。
- **正常运行被误判作废**: v6b 两臂 120 次真实调用零不健康 (记录 9、15), v6a 的 2 次不健康逐条查明都是真故障 (API 重试风暴打满 120 秒)。矩阵里 U1–U4 四类正常形态 (触发 / 不触发 / 先调别的工具 / 带 api_retry 帧) 都判健康。误报面目前看不到。Claude Code 升级换帧名会让检查偏向 void —— 方向是宁作废不放过, RESULT 已列入局限并给了复核动作。
- **套件里若有重复 query** 会让日志数对不上 runs ⇒ void, 仍是 fail-closed; 现行 20 条无重复 (记录 10)。

判据本身可执行: `run_eval()` 的 `did_pass` 语义与 D2「通过」条逐字一致 (记录 6), 参数钉死那一行的四个参数与「20 条」齐全 (记录 13), 阈值 0.8 在 3 runs 下等于 3/3 的算例正确。

## 事后修订规则是否正当 (任务 3)

**判定: 正当的基于新事实的修订, 不是为了让结果好看而改判据。** 四条依据:

1. **时间线干净 (记录 14、15)**: 原预登记 sha1 与 `prereg.lock` 对得上, 锁定于 13:09:14Z, 早于第一次跑 (13:15:05Z)。v6a 全部数据在 13:39:53Z 落定; 修订预登记锁定于 13:51:34Z; v6b 第一次重跑 13:52:45Z。修订写在「看到数据之后、任何重跑之前」这个位置上, 没有边跑边改。两份文件当前内容的 sha1 都与各自锁定记录一致, 事后没被改过。
2. **改的是后果, 不是探测**: 单次调用「健不健康」的四条判据一个字没动 (v6a 与 v6b 的 `classify_calls.py` diff 里 `classify_file` 的判定逻辑未变, 记录 14 旁的 diff)。变的是「不健康之后怎么办」: 从「有一次就作废」改成「只有可能翻转结论才作废」。如果目的是让结果好看, 最省事的做法是放宽探测 (例如把 120 秒超时那两次算健康), 而修订没有走这条路 —— 它明确认定那两次「是真故障, 检查判得对, 不是误报」。
3. **修订让规则更容易判 void 的那些地方也一并加了**: 新增 S6–S10、F9、M1 七个用例里, S8 / S10 / F9 / M1 都是**新增的作废路径** (坏到能翻转、判定事件卡在超时余量、query 对不上)。一个为了好看而改的判据不会给自己加四条新的红线。反事实也在: 删掉报错结果帧的判定, 5 例转为不符、退出码 1。
4. **A / B / C 全部重跑, 不是只重跑不利的那组**: 修订预登记写明重跑范围, run.log 与产物目录佐证 (探针两组 + 真实两臂 + 24 用例矩阵全在 `v6b` 根下, v6a 全套另存 `v6a/`)。原始那批没有被覆盖或删除, 可复查。

**RESULT v7 §v6 的结论有没有超出证据**: 基本没有, 有两处措辞偏紧需要收一收 (观察 7、8)。「把环境故障与真没触发分开了」这句就已验证的故障类而言成立, 但它掩盖了上面说的那一类「看起来健康的降级」—— RESULT 的「已知局限」段其实写了 (故障由假 claude 模拟, 真实故障实见三类, 额度耗尽 / 鉴权失败未复现), 所以不构成失实, 只是结论段与局限段的口径不一样紧。「一轮 120 次调用全部健康的概率约 13%」算术无误 (0.9833 的 120 次方约 12.9%), 但它把 2/120 当独立事件, 而修订自己描述的机制是「API 连续重试」的相关时间窗, 两次落在同一臂; 独立性前提不成立。这个数字的方向性结论不受影响 (一次重试风暴就足以作废整轮, 而 v6a 与 v6b 首次探针各撞上一次), 所以我不列 finding。

## 影响面数字 (任务 4)

独立重写扫描脚本逐提交比对 `skills/*/SKILL.md` frontmatter 的 `description` (记录 3), **v8 的三个数字全部复现**:

| v8 §Impact 写的 | 我的复核 | 判定 |
|---|---|---|
| 456 个非合并提交 | `git rev-list --no-merges --count master` = 456 (含合并 568) | 一致 |
| 改了已有 skill description 的 7 个 | 7 个: `557b9535` / `641e1649` / `55d2e84a` / `ee35928b` / `f8713f14` / `7801bd42` / `2b67ac64` | 一致 |
| brainstorm 一次删掉 frontmatter、一次恢复并换措辞, 按两次计 | `55d2e84a` 与 `ee35928b` 两个提交, 均只动 brainstorm | 一致 |
| 约 1.5% | 7 / 456 = 1.54% | 一致 |
| 另有 15 个提交新增 skill (不含首版) | 新建 `skills/*/SKILL.md` 的提交 15 个 | 数字一致, 「另有」措辞略不准 (观察 4) |

唯一的瑕疵: `7801bd42` (session-closer) 同时属于两类 —— 它既新增 skill 又改了 `phase-d-closer` 的 description。所以两类的并集是 21 个提交而不是 22 个, 「另有」严格说不成立。v8 没有给出求和数, 不产生算术错误, 结论 (「一般开发任务不受影响」) 也不受影响。

顺带复核了 D5.2 的口径: `aria/skills/` 下 43 个目录、42 个含 SKILL.md (`issue-triage-workspace` 无), 现有 trigger 套件 0 个 (`ab-suite/trigger/` 目录不存在), 本 Spec 执行 T4 则为 1 个、余 41 个 —— 与 D5.2、OQ-7、§Impact 末条的「41 个」全部自洽 (记录 11)。`ab-suite/version.yaml` 现为 `1.5.0`, 与 SC-4 的「改前 1.5.0」一致。

## 新引入问题检查 (任务 5)

逐块查 v8 为修 R6 新写的文字 (新增 35 行 / 删除 33 行, 记录 1), 没有查到新的不一致或失实:

- **D1 段落**: 禁令措辞与 SOT 表格行逐字一致; 「禁令覆盖新增 skill (OQ-9)」与 D2 套件条、OQ-9 三处同向; 「禁令以 `state_scanner.coordination.unattended` 为准 …… 修好之前禁令在 runner 里不会触发」把我 R6 观察 3 的后果补进去了。
- **D2 / D3**: 逐调用健康检查条对 `run_eval.py` 的源码描述逐句成立 (记录 7); 负控条的两个 Fisher p 值实算为 0.0163 与 0.0433, 与写的 0.016 / 0.043 一致 (记录 8); 「基线 v3 负控 3/10」「v5 为 0/10」「过宽臂 should-not 22/30 (7/10 条判红)」与产物 json 逐个对上 (记录 9)。D3 表恰六行、`[配置推导]` 恰一行、第三列 14 个路径全部存在 (记录 12) ⇒ SC-2 可判且为真。第 5 行的机读实证从 v7 的参照臂产物换成了负控 + 矩阵 + 两份真实检查报告, 与新判据对得上。
- **D5.6 第 6 项**: owner 目标设计原话保留并标明「原话」, 旁注现状与代码一致; 八条已知缺口逐条可对代码 (记录 16、17)。
- **§Impact**: 见任务 4; 成本段「`claude-opus-5` 上 11m33s–23m05s, 上沿来自一轮撞上 API 重试风暴的负控臂」与 run.log 对得上 (v6b C1 11m33s, v6a C2 23m05s), 「v2–v6 共 17 臂」按 4+4+2+3+2+2 成立。
- **OQ-9**: 推荐与代价都写了, 备选也写了, 符合「原文无推荐默认的不得自标默认」的要求 —— 它确实给了推荐并附代价, 不是自造默认。
- **T2b / SC-13**: 我在独立目录用绝对路径重跑 `fault_matrix.py`, 24 用例、与预期不符 0、退出码 0 (记录 4) —— SC-13 的断言可执行且当前为真。`fault_matrix.py` 的 `find_suite()` 是向上找 `aria-plugin-benchmarks` 目录再拼相对路径, 搬到 `tools/trigger-eval/` 之后仍能定位套件, T2b 不会因为换位置而失败。
- **SC 自检 (记录 13)**: SC-5 比较句 0 命中且「不设比较判据」在; SC-9 四项定位全真 (含作废行同时含「逐调用健康检查不通过」「≥ 6/10」「不得 ship」); SC-10 参数钉死行齐全; SC-12 五串全在; SC-11 对 D1 表三行与 D6 待转录句 0 命中 (D6 段内唯一命中是本 proposal 自己的「### D6.」标题, 不在转录范围内, 不构成问题)。

## Findings

(无 critical / 无 major / 无阻塞 Phase B 的 minor。我 R6 的 4 条全部 closed, 本轮未发现新的 critical 或 major。)

## 观察

1. **OQ-9 缺「随裁定变化」的条件段**: D4 对 OQ-7 的处理是标出「随 OQ-7 裁定变化的部分 (不转录)」并写明 (B) 分支要改哪几句; OQ-9 没有同样的段落。若 owner 裁「不算」, 要改的是两处已定稿的转录文字 —— D2 套件条末句「新增 skill 的首个 description 同样要过本场景, 其首个套件随之建立」与 SOT 禁令里的「(含新增 skill)」括注 —— 文本没点名这两处。T0 的通用转录纪律能覆盖, 不阻塞, 但点名一句能省掉执行者一次翻查。
2. **删掉参照臂留下一个单侧盲区**: 负控只挡「触发过多」(≥ 6/10 作废), 没有任何一臂挡「整体不触发」。若环境整体降级而每次调用看起来都健康 (例如合成技能没写进项目根、设置源没生效), 被评臂会判 **fail** 而不是作废, 而「fail 的后果」给的两条处置是「修正 description」与「改套件划分」—— 两条都会让执行者去改本来没问题的东西。建议在「fail 的后果」开头加一句「先按前置表逐条复核, 确认前置都生效再判是不是真 fail」, 这是纯文字, 不影响判据。
3. **健康检查不验证前置是否真的生效**: 垫片只存输出流与 query 原文, 不存 argv, 所以 `--setting-sources project` 与 `--model` 有没有真的加上, 检查看不到。stream-json 的 `init` 帧里通常带模型名, 将来可以把「本臂各次调用的模型名一致且等于声明值」做成机械断言, 把 D3 第 3、4 条从「靠人照做」升级成「可验证」。眼下不阻塞。
4. **「另有 15 个提交新增 skill」的措辞**: `7801bd42` 两类都算, 并集 21 而非 22, 「另有」严格说不准确。建议写成「另有 15 个提交新增 skill (其中 1 个同时改了已有 description, 两类并集 21 个)」。数字本身复现无误。
5. **两个工具的可移植性 (搬进仓库之后才会咬人)**: (a) `fault_matrix.py` 的 `DEFAULT_SKILL_CREATOR` 写死了带插件缓存 hash 的绝对路径 (`bb335391eb83`), SC-13 已给出 `SKILL_CREATOR_ROOT` 的出口, 可接受; (b) `--out` 传相对路径时整批用例失败 —— 我第一次重跑就是这样, 23/24 不符, 根因是脚本把相对的 `--eval-set` 交给了换过 cwd 的子进程 (记录 5)。失败形态是全红不是全绿, 不会造成假绿, 而且 SC-13 写的命令不带 `--out` (走临时目录) 不受影响; 但作为长期工具建议把 `--out` / `--suite` 一律转绝对路径。(c) `--out` 指向已存在的目录会被 `shutil.rmtree` 整个删掉, 值得在文件头注一句。
6. **驱动脚本没随四个工具进仓**: 真正跑过两臂的 `run_arms_v6b.sh` (装垫片到 PATH、设 `TRIGGER_EVAL_CALL_LOG_DIR`、两臂并行、跑完调检查脚本) 留在基线目录, 不在 T2b 搬运的四个文件里; D2 / D3 也没点名 `TRIGGER_EVAL_CALL_LOG_DIR` 这个变量名。执行者照手册跑 4b 要先读垫片源码才知道怎么设。垫片对未设变量是硬报错 (`:?`), 所以是 fail-loud 不是假绿。建议 T2b 顺手把驱动脚本模板一并搬过去 —— 这也正是「规范里的示例命令往往从没实跑过」那类坑的预防。
7. **RESULT v7 的「约 13%」用了独立性前提**: 见任务 3。建议改成「同一轮里撞上至少一次重试风暴的频率 (v6a 一次、v6b 首次探针一次)」这种按事件计的说法, 不按逐调用独立概率算。结论方向不变。
8. **v6a 的回判比 v6b 弱一档**: v6a 日志没有 query 原文, RESULT 是按「单 worker 依套件顺序逐次调用」推位置的。RESULT 已注明这一点, 不影响 v6b 的结论, 但引用时别把这段当成与 v6b 同强度的证据。
9. **我 R6 观察 7 的余项已闭**: 抬头的 RESULT 重核清单改成了「以 `grep -n RESULT` 逐处列出, 不只看某几节」(不再是列举几节), T5 也补了「转录第三条时在基线路径后补写当时 RESULT.md 的版本号与主仓提交 SHA (这是给执行者的指令, 本身不转录)」。漏改的根源补上了。

## Verdict

**PASS** — 0 critical / 0 major / 0 minor (Findings 段); 另有观察 9 条, 不进收敛比较键、不影响 vote。

R6 我席 4 条 (major 3 / minor 1) 全部 closed, 无 partially、无 open。本轮对 v8 新写文字的逐块检查、对基线数字与编排器 / runner 代码的独立复核、以及对故障矩阵的独立重跑均未发现新的 critical 或 major。owner 裁定的「D2 故障识别先做实验再重新设计」已按预登记执行完毕, 修订过程经得起「是不是为了好看而改判据」的追问, 新设计在已验证的故障类上没有漏检, 误判方向一致地偏向作废 (fail-closed)。

## Vote

**PASS**

## 数据核实记录

1. 被审对象: 仓库 HEAD `15ab323`; `git diff c3a5903 15ab323 -- openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md` = 新增 35 行 / 删除 33 行 (提取到 scratchpad 的 `v8_added.txt` / `v8_removed.txt` 逐行读过)。
2. aria 子模块 master `1cb3872`: `git rev-list --no-merges --count master` = 456; `git rev-list --count master` = 568。
3. description 影响面: 自写 `desc_scan.py` (不复用 R6 脚本), 对 456 个非合并提交逐个取 `skills/*/SKILL.md` 的 frontmatter `description` 并与父提交比对。改已有 description 的提交 7 个 (`557b9535` `641e1649` `55d2e84a` `ee35928b` `f8713f14` `7801bd42` `2b67ac64`); 新建 SKILL.md 的提交 15 个; 两集合交于 `7801bd42`。
4. 故障矩阵独立重跑 (绝对 `--out`): 24 个用例全部「符合」, 末行「与预期不符 0」, 退出码 0 —— SC-13 的断言当前为真且可由第三方复现。
5. 同一脚本用相对 `--out` 重跑: 23/24 不符, 根因 `FileNotFoundError: 'fm/suite2.json'` (相对 `--eval-set` 交给已换 cwd 的 `run_eval` 子进程)。失败形态全红, 无假绿风险。
6. `run_eval.py` 的 `did_pass`: `should_trigger` 时 `trigger_rate >= trigger_threshold`, 否则 `trigger_rate < trigger_threshold` —— 与 D2「通过」条逐字一致。
7. `run_single_query`: 超时退出 while 后 `return triggered` (False); 进程提前退出 → `break` → 同上; `result` 帧 → `return triggered` (此前判定); `Warning: query failed` 只在 `run_eval()` 的 `except Exception` 分支。与 D2 括注逐句一致。
8. Fisher 精确检验实算: 10/10 对 5/10 单侧 p = 0.0163; 10/10 对 6/10 单侧 p = 0.0433; 10/10 对 3/10 双侧 p = 0.0031。与 D2 负控条、§Why 第 2 条写的数字一致。
9. 基线产物实读: v3 负控 should-trigger 8/30 (query 级 3/10); v5 负控 0/30 (0/10); v6b C1 被评 30/30 (10/10)、should-not 命中 0; v6b C2 负控 0/30 (0/10); v4 过宽臂 should-not 22/30、判红 7/10。
10. 套件 `trigger-eval-openspec-archive.json`: 20 条, 前 10 条 should-trigger、后 10 条 should-not, 无重复 query。
11. skill 计数: `aria/skills/` 43 个目录、42 个含 SKILL.md (缺的是 `issue-triage-workspace`); `ab-suite/trigger/` 目录不存在 ⇒ 现有 trigger 套件 0 个; `ab-suite/version.yaml` 的 `version` 为 `1.5.0`。
12. D3 前置表: 数据行恰 6 行 (首列 1–6 各一次), 带 `[配置推导]` 的恰 1 行; 第三列 14 个反引号路径拼上基线目录后 `test -e` 全部为真。
13. SC 自检 (用 python `re`, 不用 grep): SC-5 比较句命中 0 且「不设比较判据」出现 1 次; SC-9 的四项定位全真 (「fail 的后果」+「不得 ship」1 行; 「作废」+「不得 ship」2 行; `classify_calls.py` 1 行; 作废行同时含三串); SC-10 参数钉死行含四个参数与「20 条」; SC-12 五串在 SOT 行全在; SC-11 五个模式对 D1 表三行 0 命中, D6 段内唯一命中是本 proposal 的「### D6.」标题 (非转录范围)。
14. 预登记锁定: `sha1sum` 实算 `PREREGISTRATION.md` = `8e3d63797bcc…`、`PREREGISTRATION-AMENDMENT.md` = `2639940452cb…`, 与 `prereg.lock` / `prereg-amendment.lock` 记录的前 12 位一致 ⇒ 两份文件锁定后未被改动。`diff v6a/classify_calls.py classify_calls.py` 确认单次调用健康判定 (`classify_file`) 未变, 新增的是 `judge()` 与 `--role`。
15. 时间线 (两份 `run.log` 实读): v6a 探针 13:15:05Z–13:15:14Z, v6a 两臂 13:16:48Z–13:39:53Z; 修订预登记锁定 13:51:34Z; v6b 探针 13:52:45Z–13:58:25Z; v6b 两臂 14:00:42Z–14:12:55Z。修订晚于 v6a 全部数据、早于 v6b 任何重跑。v6b 两臂 classify 均 `unhealthy_calls: 0`, 结论 pass / valid。
16. 编排器代码 (`aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/`): `reconciler.py` `_RETRYABLE_FAIL_REASONS = frozenset({"infrastructure","timeout"})`、`_RETRY_COUNT_MAX = 1`; `interfaces.py` `CONTAINER_CRASH = "container_crash"`; `extension.py` `_handle_s5_await` 非零退出 → `S_FAIL` + `fail_detail="S5_AWAIT: alloc terminated with exit_code=… alloc_id=… (container_crash)"`; `reconcile_runner.py:120` 未设 `ARIA_FAILURE_ANALYSIS_ENABLED` 即整段跳过; `reconciler.py:1321-1322` `notify_owner` 才发 best-effort 飞书 reject 卡且为终态; `mark_failed` 各调用点 (1095 / 1312 / 1349 / 1452) 无飞书调用。
17. runner 代码 (`aria-orchestrator/docker/aria-runner/modes/`): `initial.sh` Step 8 为 NO_OP 判定、Step 10 为 `git add -A` + `git commit` 后推送开 PR; `changes.sh` `git add -A` → commit → `git push --force-with-lease` → 写 `"outcome":"PASS"`。与 D5.6 已知缺口第 (3) 条一致。
18. D5 结构: 恰 1–6 六项, 无第 7 项; 「三张 issue」在抬头、Key Deliverables、T6、SC-6 四处一致。

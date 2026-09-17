# 场景 4 基线实跑 — description 触发率评测对 openspec-archive 两版 description 的区分力 (10CG/Aria#211)

> **本文件版本**: 8 (2026-09-17, post_spec R7 后按 code-reviewer 的 minor 加固 `fault_matrix.py`: 输出目录已存在且非空时报错退出, 不再无条件删除; 用加固后的脚本重跑矩阵与反事实, 结论不变)。v7 (2026-09-15, post_spec R6 rework: 新增 §v6 逐调用健康检查 —— v6a 原预登记与 v6b 修订预登记两批, 各含故障矩阵、真实报错探针、真实两臂; 结论 3 补第三处结构性缺陷; 「对 Rule #6 处方的含义」把同批参照臂换成逐调用健康检查, v6 所说「环境故障只能靠参照臂识别」不再成立)。v6 (2026-09-14, post_spec R5 rework: 「对 Rule #6 处方的含义」补同批参照臂 —— `run_eval.py` 把异常、超时、claude 报错都记成「未触发」, 环境故障只能靠参照臂识别)。v5 (2026-09-14, post_spec R4 rework: §v5 改为逐字引用预登记原文; 已知局限改为「已验证判红的破坏有两类 (未穷举)」, 去掉无依据的能力上限说法)。v4 (2026-09-14, post_spec R3 rework: 并入 v5 自然措辞扩张三臂 / 首句嵌的是 description 不是技能名 / 结论 1 残留全称句)。v3 (2026-09-14, post_spec R2 rework: 删除一处失实的「同批提交」声明 / 技能数口径说明 / 地板守卫的已验证范围收窄为两类破坏 / query 级独立性局限 / 时长区间补 v2 / 成本差拆成两部分)。v2 (2026-09-13) 并入 v4 反事实两臂与 query 级统计。**引用方请写「RESULT.md v8 @ <提交 SHA>」**; 本文件修订时版本号递增, 引用了旧版本数字的文本须重核。

| 字段 | 值 |
|---|---|
| 跑于 | 2026-09-13 (v1–v4)、2026-09-14 (v5) 与 2026-09-15 (v6), 见下 |
| 目的 | `10CG/Aria#211` 验收第 1–3 条: 在把「description 变动 ⇒ 跑场景 4」写进 Rule #6 之前, 先实跑证明场景 4 (a) 对真实 description 变动区分力非零, (b) 负控 (删光触发词) 显著下降 |
| 工具 | skill-creator `scripts/run_eval.py` (插件缓存 `claude-plugins-official/skill-creator/bb335391eb83`; 该 hash 随插件更新漂移, 重跑时按 `find ~/.claude/plugins -path '*skill-creator*' -name run_eval.py` 重新定位), Claude Code 2.1.269 |
| 模型 | `claude-fable-5-1` (显式传 `--model`, 与跑时的 session 一致; skill-creator 指引); v5、v6 为 `claude-opus-5`, 见各节 |
| 套件 | `trigger-eval-openspec-archive.json` — 20 query: 10 should-trigger / 10 should-not (近似误触为主)。**未经 owner 审阅** (skill-creator Step 2 要求 HTML 审阅; 跑时 owner 不在线), 见 Spec OQ-3 |
| 每 query | 3 runs, `trigger_threshold=0.5` (3 runs 下即 ≥ 2/3), `timeout=120s` |
| 臂 | **new** = v1.73.0 (= 当前 master) description · **old** = v1.71.1 description · **negctrl** = 删光领域词「对一个已完成的事项做收尾处理，并核对处理结果。」 · **poscontrol** = 「pushy」版 (显式列触发短语 + 「都必须使用本技能」) · **overbroad** (v4) = 过宽版 (列一张触发词表 + 「只要提到其中任意一个词都必须先使用本技能」) · **realroot** (v4) = new description, 但项目根含约 25 个合成文件 (11 个 `openspec/changes/*/` 目录各含 proposal.md 与 tasks.md, 另有 archive / handoff / README) |
| 隔离 | `claude` 垫片追加 `--setting-sources project`, 临时项目根 (空 `.claude/`)。机读证据 `probe-setting-sources-default.json` / `probe-setting-sources-project.json` (同一探针 query, `--model claude-fable-5-1`): 默认设置源下列表**含** `openspec-archive` (`total_cost_usd` 0.604), project-only 下**不含** (0.079)。差价来自两部分, 未拆开计价: 默认设置源多约 2.3 万 token 的 cache 创建 (`cache_creation_input_tokens` 27065 对 3696, 即技能与插件清单), 以及输出 1190 对 5 token (含思考) |

> **技能数口径**: 探针让模型自报「列表里有几个技能」, 是 LLM 自报数, 不是机械计数。两份机读探针 (`--model claude-fable-5-1`) 自报 97 / 12; `manifest.json` 里的「97→13」来自本 session 首次探针 (未传 `--model`, project-only 下实际走了 `claude-opus-5[1m]`, 未落机读文件)。可靠的机械事实只有一条: **默认设置源下列表含真 `openspec-archive`, project-only 下不含** (两份 json 的 `result` 字段)。
>
> **同一首次探针的附带观察 (D3 第 4 条的来源)**: 未传 `--model` 时, 默认设置源下 `modelUsage` 为 `claude-fable-5-1` (当时的用户设置), project-only 下为 `claude-opus-5[1m]` —— 即 `--setting-sources project` 会连带换掉默认模型。该输出**未落机读文件**; 2026-09-14 用户把默认模型改为 `claude-opus-5[1m]` 后, 两种设置源的默认模型相同, 该现象已无法原样复现。

## 记分 (should-trigger 命中 / 30; should-not 命中 / 30)

| 轮 | 配置 | 臂 | should | should-not | 说明 |
|---|---|---|---|---|---|
| v1 | 共用项目根, `--num-workers 4`, 合成名 `openspec-archive-skill-<id>` | new / old / negctrl / poscontrol | 4 / 7 / 0 / 6 | 0 / 0 / 0 / 0 | **地板**: 四臂全被显著压低 |
| v2 | 每臂独立项目根, `--num-workers 1`, 合成名不变 | new / old / negctrl / poscontrol | 27 / 30 / 27 / 30 | 0 / 0 / 0 / 0 | **天花板 + 名字泄漏**: 负控也 27/30 |
| v3 | 同 v2 + 合成名中性化 (`name: helper`) | new / old / negctrl / poscontrol | **30 / 30 / 8 / 30** | 0 / 0 / 0 / 0 | **有效轮** |
| v4 | 同 v3 | overbroad | 30 | **22** (query 级 7/10 判红) | should-not 的 FAIL 分支可达 |
| v4 | 同 v3, 项目根含约 25 个合成文件 | realroot (new desc) | 30 | 0 | 「第一个 tool_use」判据在该根下未失真 |

### 统计 (v3, 两种单元都给)

同一 query 的 3 次 run 不是独立样本 (伪重复), **独立单元取 query (n=10)**; run 级 (n=30) 只作参考。

| 比较 | run 级 n=30 双侧 Fisher | query 级 n=10 (命中 = `trigger_rate ≥ 0.5`) 双侧 Fisher |
|---|---|---|
| new (30 / 10) vs old (30 / 10) | p = 1.0 | p = 1.0 |
| poscontrol (30 / 10) vs new | p = 1.0 | p = 1.0 |
| new vs negctrl (8 / 3) | p < 0.0001 | **p = 0.0031** |
| old vs negctrl | p < 0.0001 | p = 0.0031 |

query 级单元的独立性也是相对的: 同一臂的 10 条 query 共享同一个被评 description (同一个「处理」), 不是 10 次独立的 description 抽样。⇒ 这些 p 值回答的是「在这 20 条固定套件上, 两个 description 的触发分布是否不同」, **不能外推**到别的套件或别的 description。

负控 8/30 的分布: 集中在 3 条 query —「周期收尾: spec … 落点校验」3/3、「…标记为已完成并放到归档目录, 记得归档后要检查…」2/3、「D.2 归档 + 落点校验」3/3; 其余 7 条 0/3。这 3 条都含「收尾 / 核对 / 校验」动作语义 ⇒ 负控删净了领域词 (归档 / OpenSpec / Spec), **没删净通用动作词** (「收尾」「核对」仍在负控 description 里)。

过宽臂 should-not 22/30 的分布: 3/3 六条 (handoff 归档 / 起新 proposal / Archive Tracker 单 / 改 Status / 状态扫描 / archive 分层脚本), 2/3 一条 (sprint changelog 归档), 1/3 两条 (openspec CLI 口径 / tar 归档审计报告), 0/3 一条 (git 分支归档 —— 它同时含词表里的「分支」与「归档」, 却一次都没触发)。⇒ 触发与词表相关但不是逐词线性的。

## v5: 自然措辞扩张敏感度 (2026-09-14, 预登记见 `v5-mildcreep-opus5/PREREGISTRATION.md`)

为回应 post_spec R3 qa 席 major (地板守卫对「自然措辞扩张」零证据), 跑前写定判读规则后补跑三臂。模型换成 `claude-opus-5` (Fable 额度耗尽), 三臂同批, 只做臂间比较, 不与 v1–v4 数字直接比。其余配置同 v3 / v4 (中性名壳 / 每臂独立项目根 / 单 worker / 3 runs / 阈值 0.5 / `--setting-sources project`)。

| 臂 | description | should (query 级) | should-not 命中 (≥ 0.5 的条数) | 判读 |
|---|---|---|---|---|
| new (参照) | v1.73.0 原文 | 30/30 (10/10) | 0/30 (0) | 门通过 ⇒ opus-5 上套件与环境可用 |
| negctrl (同批负控) | 「对一个事项做处理。」(按 Spec §D2 新构造规则) | 0/30 (0/10) | 0/30 (0) | ≤ 5/10 ⇒ 本轮有效 |
| mildcreep (被评) | 原文 + 「与相关文档」「整理项目收尾材料」「整理归档文档」「收尾整理」 | 30/30 (10/10) | 0/30 (0) | 门通过 ⇒ 本套件上该幅度的自然扩张**不被判为改坏** |

- 按预登记 (`PREREGISTRATION.md` 原文: 「这是对 §D2「只承诺两类破坏」局限的实证确认, 不是守卫失效的证据」): mildcreep 门通过, 落在这一分支。四条最可能被误触的近似误触 (handoff 归档 / 审计报告 tar 归档 / archive 分层脚本 / sprint changelog 归档) 全部 0/3。
- 附带: 按新构造规则的负控 (删去领域名词与特有动作词) 在 opus-5 上 0/10; 基线负控 (保留「收尾 / 核对」) 在 fable 上 3/10。模型不同不直接比, 但方向与「旧负控没删净动作词」一致。
- 时长 (run.log): 三臂并行, 单臂 15m18s–19m41s (opus-5 比 fable 慢)。

## v6: 逐调用健康检查 (2026-09-15; 预登记 `v6-per-call-health-opus5/PREREGISTRATION.md`, 修订 `PREREGISTRATION-AMENDMENT.md`)

post_spec R6 判同批参照臂有两处漏洞 (故障只落一臂或落在 should-not 半程时接不住; 有意改套件划分、新增 skill、修复已坏 description 三种正当情形下必然作废), owner 2026-09-15 裁定先做实验再重新设计。实验分两批: v6a 按原预登记跑完, 真实数据暴露出「任一调用不健康即作废」太严; v6b 按重跑前写定并锁定的修订预登记, 把三组实验全部重跑。v6a 的全部产物归档在 `v6-per-call-health-opus5/v6a/`, 目录根下是 v6b 的工具与结果。

**设计 (v6b 定稿)**:
- 垫片 `claude-shim.sh`: 追加 `--setting-sources project`; 每次调用的 stdout 经 `tee` 原样转交 run_eval.py 并另存一份 (`<id>.jsonl`, 首尾各一行起止时间), query 原文另存 (`<id>.query`), stderr 另存。
- 检查 `classify_calls.py --role evaluated|negctrl`: 单次调用健康 = 起止记录齐全、输出流里有 run_eval.py 据以判定的事件 (tool_use 开始 / `message_stop` / 含 tool_use 的 assistant 消息 / 结果帧)、结果帧不报错、耗时小于超时阈值减 1 秒。按 query 原文把调用对到 query, 每条 query 的日志数须等于 runs。不健康的调用按「触发」「没触发」两种可能都算 (输出流里出现过 tool_use 的, run_eval 可能已把它记成触发, 同样按两种算); 被评臂的门判定、负控的命中数判定在两端都不变, 结论为 pass / fail (被评臂) 或 valid (负控臂); 会变则为 void。

### v6a (原预登记; 锁定记录: PREREGISTRATION.md sha1=8e3d63797bcc 锁定于 2026-09-15T13:09:14Z (任何实验运行之前))

- 故障矩阵 17 个用例全部符合; 删掉「结果帧报错」判定的反事实有 3 例转为不符。
- 真实报错探针 (不存在的模型名 / `--timeout 3`): run_eval 都记「未触发」, stderr 无 Warning; 检查都判不健康。
- 真实全量两臂 (`claude-opus-5`, 同批并行): C1 被评 (现行 openspec-archive description) 60/60 健康, should 30/30 (10/10), should-not 命中 0; C2 负控 (「对一个事项做处理。」) should 0/30 (0/10), 2 次不健康 —— 两次的输出流都只有 init、status、rate_limit_event 与 5 次 api_retry, 耗时 120.37 秒与 120.22 秒: API 连续重试, run_eval 超时后记成「未触发」。这是真故障, 检查判得对, 不是误报。
- 但按「任一调用不健康即作废」, 这一轮会作废。以本次的频率 (2/120), 一轮 120 次调用全部健康的概率约 13%, 多数轮次会作废 ⇒ 规则不可用, 修订。
- 按 v6b 的规则回看这一轮 (v6a 日志没有 query 原文, 按单 worker 时 run_eval 依套件顺序逐次调用来对应): 两次不健康调用分别落在第 6 条 (should-trigger) 与第 12 条 (should-not), 各只坏一次 run; 负控命中数上界仍为 0 ⇒ valid; C1 无不健康调用 ⇒ pass。即这一轮在 v6b 规则下有效。
- 时长 (run.log): C1 18m37s, C2 23m05s (含两次 120 秒超时)。

### v6b (修订预登记, 重跑前写定; 锁定记录: PREREGISTRATION-AMENDMENT.md sha1=2639940452cb 锁定于 2026-09-15T13:51:34Z (v6b 任何重跑之前))

**A. 故障矩阵** (`fault_matrix.py`, 假 claude 注入故障, 不调用 API): 24 个用例全部符合 (`fault-matrix/matrix-summary.json`)。

| 用例 | run_eval 的门 | 检查结论 |
|---|---|---|
| 正常四类: 触发 / 不触发 / 先调别的工具 / 带 api_retry 帧 | 与假 claude 的设定一致 | 触发类 pass, 不触发类 fail (should-trigger 那条确实没触发) |
| 故障七类: 结果帧报错 / 只有 init 就退出 / 无输出即退出 / 开了消息没到判定点就退出 / 挂起到超时 / 判定事件晚于超时 / 真 claude 路径不存在 | 全部记成「未触发」, stderr 无 Warning | void |
| 垫片不在 PATH 上 | 每次调用一行 Warning, 日志 0 份 | void |
| 判定事件恰在超时余量里到达 (run_eval 已据此判定) | 通过 | void |
| 过宽被评臂, 故障落在后半程 (should-not) | **通过 (假绿)** | void |
| 正确被评臂, 一条 should-trigger 的三次 run 全坏 | **fail (假红)** | void |
| 正确被评臂, 只坏一条 should-trigger 的一次 run | 通过 | pass (改变不了判定) |
| 正确被评臂, 只坏一条 should-not 的一次 run | 通过 | pass |
| 正确被评臂, 同一条 should-trigger 坏两次 run | fail | void |
| 无故障的正确臂 / 过宽臂 | 通过 / fail | pass / fail (过宽, 真实 fail) |
| 负控臂: 无故障 / 6 条 should-trigger 各坏一次 / 各坏两次 | — | valid / valid / void |
| 日志的 query 对不上 run_eval 输出 (直接调检查脚本) | — | void |

反事实: 删掉 `classify_calls.py` 里对报错结果帧的判定, 5 例转为不符 (F1_result_error、S1_overbroad_fault_in_shouldnot_half、S2_correct_fault_on_one_should_query、S8_two_run_fault_should、S10_negctrl_two_run_fault_x6), 退出码 1 (`fault-matrix-counterfactual/matrix-summary.json`)。R7 后按 code-reviewer 的 minor 加固了 `fault_matrix.py` (输出目录已存在且非空时报错退出, 不再删除), 并用加固后的脚本把矩阵与反事实各重跑一次: 24 个用例仍全部符合、反事实仍 5 例转为不符; 归档在 `fault-matrix/` 与 `fault-matrix-counterfactual/` 的就是加固后重跑的产物。

**B. 真实报错探针重跑** (新垫片): 两组都判 void (`real/B1_*`、`real/B2_*`)。第一次重跑时 API 正处在重试风暴里, 不存在的模型名那组两次调用各耗满 120 秒, 被外层超时截断, 未计入; 第二次 12 秒内拿到报错的结果帧。

**C. 真实全量两臂重跑** (`claude-opus-5`, 新垫片, 其余同 v6a; `real/C1_*`、`real/C2_*`):

| 臂 | should (query 级) | should-not 命中 | 不健康调用 | 检查结论 |
|---|---|---|---|---|
| C1 被评 (现行 openspec-archive description) | 30/30 (10/10) | 0 | 0 次不健康 | pass |
| C2 负控 (「对一个事项做处理。」) | 0/30 (0/10) | 0 | 0 次不健康 | valid (命中数区间 0–0) |

- 符合修订预登记的预期: 被评臂 pass、负控臂 valid。两臂都没有不健康的调用。
- 两臂 stderr 的 Warning: C1 0 行, C2 0 行。单次调用耗时: C1 中位 6.0 秒、最长 62.9 秒; C2 中位 7.1 秒、最长 86.5 秒。
- 时长 (run.log): C1 11m33s, C2 12m13s。

**结论**:
- 逐调用健康检查把「环境故障」与「真没触发」分开了: 参照臂接不住的两类情形 (故障只落一臂 / 故障落在 should-not 半程) 都判为作废。真实调用里查到的不健康调用, 逐条核对都是真故障 (API 重试风暴、超时), 未见误报。
- 「任一不健康即作废」在真实环境里不可用 (v6a: 2/120 次撞上重试风暴); 「故障能否改变判定」只在故障可能翻转判定时作废 (故障矩阵里只坏一次 run 的用例有效, 坏到能翻转判定的作废)。
- 据此 Spec v8 用 v6b 的检查替换同批参照臂; 参照臂那三种正当情形下的必然作废也随之消失。

## 结论

1. **对本次真实 description 变动 (v1.71.1 → v1.73.0) 区分力为零**: new / old / poscontrol 三臂 should-trigger 全部 30/30 (query 级 10/10), p = 1.0。这是**饱和** (三臂都撞天花板, 测不出差异), 不是「无差异」的证明。在饱和套件上, 两个都能让 should-trigger 饱和的 description 必然打平 (本次这一对即如此); 比较判据只在其中一方掉出饱和时才判出差别 (如负控 8/30 对旧版 30/30) —— 它不是恒绿门, 但对「措辞改得更好」这个问题, 在饱和套件上答不出来。⇒ 按 `10CG/Aria#211` 验收第 2 条, **场景 4 不能作为「description 措辞改动有没有变好」的 A/B 工具**。
2. **场景 4 能当地板守卫, 已验证的破坏类型恰两类**:
   - 删领域词 (负控): should-trigger 掉到 8/30 (query 级 3/10, 对 10/10 双侧 p = 0.0031);
   - 显式强制过宽 (过宽臂: 触发词表 + 「都必须先使用本技能」): should-not 涨到 22/30 (7/10 条判红)。
   ⇒ 「每条 should ≥ 0.5 且每条 should-not < 0.5」这条门两侧都有真实 FAIL 样本, 不是恒绿门。**自然措辞扩张**: 一次实测不判红 (v5, 见下节): 多加「与相关文档 / 整理项目收尾材料 / 整理归档文档 / 收尾整理」后, 10 条 should-not 全部 0/3。守卫的灵敏度由套件里的近似误触决定: 套件里没有被这类扩张误触的 query, 守卫就判它没改坏。
3. **skill-creator `run_eval.py` 三处结构性缺陷 + 一处配置建议**, 不按前置运行数字不可解读:
   - (a) **并发 worker 互见**: `--num-workers N > 1` 时 N 个 `claude -p` 共用同一 `.claude/commands/`, 各自看到 N 个同 description、不同 `<id>` 的合成技能; 检测只认本 run 自己的 `<id>`。实证: v1 (共用根 + 4 worker) 4–7/30 vs v2 (独立根 + 1 worker) 27–30/30 —— **v1→v2 同批改了两个变量**, 记分表本身分不开; 机制证据是 `v1-shared-root-4workers/diag02-sibling-command-collision.jsonl`: 手动跑的 query 调用了兄弟 run 的 `openspec-archive-skill-2478f407` / `…-e136a6c3` 而不是自己的。压低幅度**定性为「显著」, 不定量**为 1/N (v1 负控 0/30 与 1/4 期望不符)。
   - (b) **合成技能泄漏意图**: 命令文件名 `<skill_name>-skill-<id>` 与正文标题 `# <skill_name>` 两处嵌入技能名 (正文首句 `This skill handles: <description>` 嵌的是 description, 不是技能名); 技能名 `openspec-archive` 本身就回答了 query ⇒ description 被架空。实证: v2 负控 (零领域词) 27/30; v3 只把 `name` 改成 `helper` (run_arms_v2.sh 与 run_arms_v3.sh 仅差 `--skill-path` 与目录名), 负控掉到 8/30。
   - (c) **故障记成「未触发」**: `claude -p` 报错、超时、非零退出时, `run_single_query` 返回「未触发」, 只有工作进程抛异常才打印 `Warning: query failed`; `runs` 恒为 3, 输出 json 里与真没触发分不开。实证: §v6 故障矩阵 (七类故障全部记成「未触发」且无 Warning)、真实报错探针与真实两臂里的 API 重试风暴。
   - (d) 配置建议: 默认设置源下 `claude -p` 加载全部用户级插件, 真 `aria:openspec-archive` 与合成技能竞争; 加 `--setting-sources project` 后不再加载, 单次成本 0.60 → 0.08 美元 (探针 json; 差价含输出长度差, 见隔离行)。该开关会连带换掉默认模型 (见上方附带观察), 所以必须**显式 `--model`**。

## 对 Rule #6 处方的含义 (供 spec `rule6-description-change-trigger-eval-lane` 引用)

- 第二行「description 变动 ⇒ 照跑场景 1」的证据面确实为空 (issue 原命题成立: 场景 1 两臂被直接喂 SKILL.md 路径)。
- 补上场景 4 **只能补成地板守卫**, 且只承诺已验证的两类破坏: 判据 = `run_eval.py` 的 `pass` 全真 (每条 should ≥ 0.5, 每条 should-not < 0.5), 外加每臂逐调用健康检查 (§v6) 的结论不为 void、同批负控 query 级命中 ≤ 5/10; **不设**比较判据 (在饱和处退化)。
- 运行前置必须成文 (独立项目根 + 单 worker / 合成名中性化 / 带逐调用记录的 claude 垫片, 内含 `--setting-sources project` / 显式 `--model` / 同批负控与逐调用健康检查 / 产物形状)。

## 原始产物

- `trigger-eval-openspec-archive.json` — 20 条 query (should / should-not 各 10)
- `v1-shared-root-4workers/` · `v2-isolated-root-1worker/` · `v3-isolated-root-1worker-neutral-name/` · `v4-counterfactuals/` · `v5-mildcreep-opus5/` (含跑前写定的 `PREREGISTRATION.md`) — 各臂 `*.json` (run_eval 原始输出, 每 query 的 `trigger_rate` / `triggers` / `runs` / `pass`) + `run.log` (各臂起止时间)
- `run_arms.sh` / `run_arms_v2.sh` / `run_arms_v3.sh` / `run_arms_v4.sh` / `run_arms_v5.sh` / `run_arms_v6.sh` / `run_arms_v6b.sh` — 各轮运行脚本 (变量 `S=` 或 `X=` 指向当时的 scratchpad, 重跑时改它; 各臂 description 原文在脚本里; v6 两份脚本分 `probes` 与 `full` 两段, `run_arms_v6.sh` 是 v6a、`run_arms_v6b.sh` 是 v6b)
- `claude-shim.sh` — 注入 `--setting-sources project` 的垫片 (v1–v5 用; v6 起用 `v6-per-call-health-opus5/claude-shim.sh`, 另加逐调用记录); `neutral-skill-SKILL.md` — v3/v4 的中性名 skill 壳
- `probe-setting-sources-default.json` / `probe-setting-sources-project.json` — 设置源隔离的机读证据
- `v6-per-call-health-opus5/` — 预登记 `PREREGISTRATION.md` 与修订 `PREREGISTRATION-AMENDMENT.md` (各带锁定记录 `prereg.lock` / `prereg-amendment.lock`); v6b 的四个工具文件 (`claude-shim.sh` 带逐调用记录的垫片 / `classify_calls.py` 逐调用健康检查 / `fake-claude` 注入故障的假 claude / `fault_matrix.py` 故障矩阵); `fault-matrix/` (24 个用例的 run_eval 输出、stderr、检查报告与 `matrix-summary.json`); `fault-matrix-counterfactual/matrix-summary.json`; `real/` (真实报错探针两组与真实两臂的 run_eval 输出、stderr、检查报告与 `run.log`); `v6a/` (原预登记那一批的工具与全部结果)
- `manifest.json` — v1 时写的运行清单, 保留原样作历史 (其中「97→13」的来历见上方「技能数口径」)

## 时长与成本

- 时长 (run.log): 单 worker 一臂 60 次调用, `claude-fable-5-1` 上 10m39s–17m39s (v2 四臂 11m26s–17m39s, v3 四臂 10m39s–12m03s, v4 两臂 13m38s–13m54s), `claude-opus-5` 上 15m18s–19m41s (v5 三臂); 两臂 (被评 + 负控) 在 fable 上并行约 11–18 分钟、串行约 22–34 分钟, 在 opus 上并行约 16–20 分钟、串行约 34–38 分钟。v6 两批两臂 (`claude-opus-5`, 经带记录的垫片): v6a C1 18m37s、C2 23m05s (C2 含两次 120 秒超时); v6b C1 11m33s、C2 12m13s。逐调用检查每臂几秒, 不调用 API。
- 成本: `run_eval.py` 不记录成本; 按探针单次 0.08 美元估, 两臂 120 次约 10 美元 (估算, 非实测)。

## 已知局限

- 20 条 query 未经 owner 审阅; should-trigger 整体偏「清楚」是天花板的一个可能来源。负控与过宽两臂仍能显著变化, 说明套件对「触发词有没有」敏感。
- 只测了一对真实 description; 结论 1 是「这一对零区分力 + 机制上小措辞改动很难在饱和套件上显形」, 不是「任何 description 改动都测不出」。
- 已验证判红的破坏有两类 (结论 2, 未穷举); 一次自然措辞扩张实测不判红 (v5)。要守住某类扩张, 须在套件的 should-not 里放被它误触的 query。
- 负控没删净通用动作词 (见统计段); 更干净的负控应删到只剩「处理一件事项」级。
- `run_eval.py` 判「触发」= 第一个 tool_use 就是本合成技能 (Skill 或 Read)。v4 realroot 在约 25 个合成文件的项目根下 30/30, 但该根没有 CLAUDE.md、没有竞争技能、没有深层目录, 比 Aria 主仓小一到两个量级; 真实大仓下未验证。
- 逐调用健康检查依赖 Claude Code stream-json 的帧名 (`stream_event` 里的 `content_block_start` 与 `message_stop`、`assistant`、`result`)。Claude Code 升级后先重跑 `fault_matrix.py`, 再实跑一臂确认零误报; 帧名若变, 检查会把调用判成「无判定事件」, 结论偏向 void, 方向是宁作废不放过。
- 故障矩阵里的故障由假 claude 模拟; 真实故障实见三类: 不存在的模型名 (报错的结果帧)、3 秒超时、API 重试风暴 (v6a 负控臂两次、v6b 第一次探针重跑两次)。额度耗尽、鉴权失败等未逐一复现。跑 v6 时账号七日用量窗口已到 99% (输出流 rate_limit_event 的 utilization), 重试风暴可能与此有关。
- 跑时 owner 不在线; 「套件未经审阅」「基线先于 spec 起草」两项 AI 流程判断写在 Spec 的 OQ-3 与 rule6_note 段, 由 owner 复议。

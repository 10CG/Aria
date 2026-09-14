# 场景 4 基线实跑 — description 触发率评测对 openspec-archive 两版 description 的区分力 (10CG/Aria#211)

> **本文件版本**: 4 (2026-09-14, post_spec R3 rework: 并入 v5 自然措辞扩张三臂 / 首句嵌的是 description 不是技能名 / 结论 1 残留全称句)。v3 (2026-09-14, post_spec R2 rework: 删除一处失实的「同批提交」声明 / 技能数口径说明 / 地板守卫的已验证范围收窄为两类破坏 / query 级独立性局限 / 时长区间补 v2 / 成本差拆成两部分)。v2 (2026-09-13) 并入 v4 反事实两臂与 query 级统计。**引用方请写「RESULT.md v4 @ <提交 SHA>」**; 本文件修订时版本号递增, 引用了旧版本数字的文本须重核。

| 字段 | 值 |
|---|---|
| 跑于 | 2026-09-13 (v1–v4) 与 2026-09-14 (v5), 见下 |
| 目的 | `10CG/Aria#211` 验收第 1–3 条: 在把「description 变动 ⇒ 跑场景 4」写进 Rule #6 之前, 先实跑证明场景 4 (a) 对真实 description 变动区分力非零, (b) 负控 (删光触发词) 显著下降 |
| 工具 | skill-creator `scripts/run_eval.py` (插件缓存 `claude-plugins-official/skill-creator/bb335391eb83`; 该 hash 随插件更新漂移, 重跑时按 `find ~/.claude/plugins -path '*skill-creator*' -name run_eval.py` 重新定位), Claude Code 2.1.269 |
| 模型 | `claude-fable-5-1` (显式传 `--model`, 与跑时的 session 一致; skill-creator 指引) |
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

- 按预登记: mildcreep 门通过 ⇒ 这是对「守卫只判得出两类破坏」这条局限的实证确认, 不是守卫失效。四条最可能被误触的近似误触 (handoff 归档 / 审计报告 tar 归档 / archive 分层脚本 / sprint changelog 归档) 全部 0/3。
- 附带: 按新构造规则的负控 (删去领域名词与特有动作词) 在 opus-5 上 0/10; 基线负控 (保留「收尾 / 核对」) 在 fable 上 3/10。模型不同不直接比, 但方向与「旧负控没删净动作词」一致。
- 时长 (run.log): 三臂并行, 单臂 15m18s–19m41s (opus-5 比 fable 慢)。

## 结论

1. **对本次真实 description 变动 (v1.71.1 → v1.73.0) 区分力为零**: new / old / poscontrol 三臂 should-trigger 全部 30/30 (query 级 10/10), p = 1.0。这是**饱和** (三臂都撞天花板, 测不出差异), 不是「无差异」的证明。在饱和套件上, 两个都能让 should-trigger 饱和的 description 必然打平 (本次这一对即如此); 比较判据只在其中一方掉出饱和时才判出差别 (如负控 8/30 对旧版 30/30) —— 它不是恒绿门, 但对「措辞改得更好」这个问题, 在饱和套件上答不出来。⇒ 按 `10CG/Aria#211` 验收第 2 条, **场景 4 不能作为「description 措辞改动有没有变好」的 A/B 工具**。
2. **场景 4 能当地板守卫, 已验证的破坏类型恰两类**:
   - 删领域词 (负控): should-trigger 掉到 8/30 (query 级 3/10, 对 10/10 双侧 p = 0.0031);
   - 显式强制过宽 (过宽臂: 触发词表 + 「都必须先使用本技能」): should-not 涨到 22/30 (7/10 条判红)。
   ⇒ 「每条 should ≥ 0.5 且每条 should-not < 0.5」这条门两侧都有真实 FAIL 样本, 不是恒绿门。**自然措辞扩张**: 一次实测不判红 (v5, 见下节): 多加「与相关文档 / 整理项目收尾材料 / 整理归档文档 / 收尾整理」后, 10 条 should-not 全部 0/3。守卫的灵敏度由套件里的近似误触决定: 套件里没有被这类扩张误触的 query, 守卫就判它没改坏。
3. **skill-creator `run_eval.py` 两处结构性缺陷 + 一处配置建议**, 不按前置运行数字不可解读:
   - (a) **并发 worker 互见**: `--num-workers N > 1` 时 N 个 `claude -p` 共用同一 `.claude/commands/`, 各自看到 N 个同 description、不同 `<id>` 的合成技能; 检测只认本 run 自己的 `<id>`。实证: v1 (共用根 + 4 worker) 4–7/30 vs v2 (独立根 + 1 worker) 27–30/30 —— **v1→v2 同批改了两个变量**, 记分表本身分不开; 机制证据是 `v1-shared-root-4workers/diag02-sibling-command-collision.jsonl`: 手动跑的 query 调用了兄弟 run 的 `openspec-archive-skill-2478f407` / `…-e136a6c3` 而不是自己的。压低幅度**定性为「显著」, 不定量**为 1/N (v1 负控 0/30 与 1/4 期望不符)。
   - (b) **合成技能泄漏意图**: 命令文件名 `<skill_name>-skill-<id>` 与正文标题 `# <skill_name>` 两处嵌入技能名 (正文首句 `This skill handles: <description>` 嵌的是 description, 不是技能名); 技能名 `openspec-archive` 本身就回答了 query ⇒ description 被架空。实证: v2 负控 (零领域词) 27/30; v3 只把 `name` 改成 `helper` (run_arms_v2.sh 与 run_arms_v3.sh 仅差 `--skill-path` 与目录名), 负控掉到 8/30。
   - (c) 配置建议: 默认设置源下 `claude -p` 加载全部用户级插件, 真 `aria:openspec-archive` 与合成技能竞争; 加 `--setting-sources project` 后不再加载, 单次成本 0.60 → 0.08 美元 (探针 json; 差价含输出长度差, 见隔离行)。该开关会连带换掉默认模型 (见上方附带观察), 所以必须**显式 `--model`**。

## 对 Rule #6 处方的含义 (供 spec `rule6-description-change-trigger-eval-lane` 引用)

- 第二行「description 变动 ⇒ 照跑场景 1」的证据面确实为空 (issue 原命题成立: 场景 1 两臂被直接喂 SKILL.md 路径)。
- 补上场景 4 **只能补成地板守卫**, 且只承诺已验证的两类破坏: 判据 = `run_eval.py` 的 `pass` 全真 (每条 should ≥ 0.5, 每条 should-not < 0.5), 外加同批负控 query 级命中 ≤ 5/10; **不设**比较判据 (在饱和处退化)。
- 运行前置必须成文 (独立项目根 + 单 worker / 合成名中性化 / `--setting-sources project` / 显式 `--model` / 同批负控 / 产物形状)。

## 原始产物

- `trigger-eval-openspec-archive.json` — 20 条 query (should / should-not 各 10)
- `v1-shared-root-4workers/` · `v2-isolated-root-1worker/` · `v3-isolated-root-1worker-neutral-name/` · `v4-counterfactuals/` · `v5-mildcreep-opus5/` (含跑前写定的 `PREREGISTRATION.md`) — 各臂 `*.json` (run_eval 原始输出, 每 query 的 `trigger_rate` / `triggers` / `runs` / `pass`) + `run.log` (各臂起止时间)
- `run_arms.sh` / `run_arms_v2.sh` / `run_arms_v3.sh` / `run_arms_v4.sh` / `run_arms_v5.sh` — 五轮运行脚本 (变量 `S=` 指向当时的 scratchpad, 重跑时改它; 各臂 description 原文在脚本里)
- `claude-shim.sh` — 注入 `--setting-sources project` 的垫片; `neutral-skill-SKILL.md` — v3/v4 的中性名 skill 壳
- `probe-setting-sources-default.json` / `probe-setting-sources-project.json` — 设置源隔离的机读证据
- `manifest.json` — v1 时写的运行清单, 保留原样作历史 (其中「97→13」的来历见上方「技能数口径」)

## 时长与成本

- 时长 (run.log): 单 worker 一臂 60 次调用, `claude-fable-5-1` 上 10m39s–17m39s (v2 四臂 11m26s–17m39s, v3 四臂 10m39s–12m03s, v4 两臂 13m38s–13m54s), `claude-opus-5` 上 15m18s–19m41s (v5 三臂); 两臂 (被评 + 负控) 在 fable 上并行约 11–18 分钟、串行约 22–34 分钟, 在 opus 上并行约 16–20 分钟、串行约 34–38 分钟。
- 成本: `run_eval.py` 不记录成本; 按探针单次 0.08 美元估, 两臂 120 次约 10 美元 (估算, 非实测)。

## 已知局限

- 20 条 query 未经 owner 审阅; should-trigger 整体偏「清楚」是天花板的一个可能来源。负控与过宽两臂仍能显著变化, 说明套件对「触发词有没有」敏感。
- 只测了一对真实 description; 结论 1 是「这一对零区分力 + 机制上小措辞改动很难在饱和套件上显形」, 不是「任何 description 改动都测不出」。
- 地板守卫判红的只有两类破坏 (结论 2); 一次自然措辞扩张实测不判红 (v5)。要守住某类扩张, 须在套件的 should-not 里放被它误触的 query。
- 负控没删净通用动作词 (见统计段); 更干净的负控应删到只剩「处理一件事项」级。
- `run_eval.py` 判「触发」= 第一个 tool_use 就是本合成技能 (Skill 或 Read)。v4 realroot 在约 25 个合成文件的项目根下 30/30, 但该根没有 CLAUDE.md、没有竞争技能、没有深层目录, 比 Aria 主仓小一到两个量级; 真实大仓下未验证。
- 跑时 owner 不在线; 「套件未经审阅」「基线先于 spec 起草」两项 AI 流程判断写在 Spec 的 OQ-3 与 rule6_note 段, 由 owner 复议。

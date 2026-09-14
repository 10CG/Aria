# Proposal: rule6-description-change-trigger-eval-lane

> **Level**: Minimal (Level 2 Spec) — owner 2026-09-13 指示「开 Level 2 cycle」; 与 LEVEL_GUIDE「跨模块 → 自动提升为 Level 3」的关系请 owner 确认, 见 OQ-4
> **Status**: Draft — post_spec R1 (2026-09-13) FAIL → v2; R2 (2026-09-14, 5 席) PASS_WITH_WARNINGS 0C / 10M / 26m (去重后) → rework v3 (本版), 待 R3
> **Created**: 2026-09-13
> **Linked Issue**: `10CG/Aria#211`
> **代码落点**: 无代码。三份规范性文本 (Aria `CLAUDE.md` Rule #6 / `standards/conventions/skill-benchmark-exemption.md` / `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md`) + 一个套件文件 (受 OQ-3 约束) + 两张新 issue + 一条上游反馈。**aria-plugin 子模块不动** (spec-drafter / task-planner 模板落地另开 issue, 见 D5.3)
> **ship target**: standards 子模块 (SOT 文件头 Version 1.0.0 → 1.1.0, MINOR — 新增强制义务。这是**单份规范文档自己的版本行**, 与 `version-management.md` §5.1 待裁的「standards 仓级版本自称」正交, 不新增仓级自称面; standards 仓无 tag, 主仓只动 gitlink) + Aria 主仓 (CLAUDE.md / 手册 / 套件)
> **基线数据**: `aria-plugin-benchmarks/ab-results/2026-09-13-rule6-description-trigger-eval-baseline/RESULT.md` **v3** (与本版同批提交; 本文引用的数字以该版本为准, RESULT 再修订须同步重核本文 §Why 与 §D2 §D3)
> **溯源**: 洞的首次记录 = `10CG/aria-plugin#190` comment 22921 (2026-09-08); 独立成单 = `10CG/Aria#211` (2026-09-09); triage 五项核对全命中 = `10CG/Aria#211` comment 23915 (2026-09-13)

## Why

Rule #6 判据表第二行逐字要求「`description` 或指令流程变动一律照跑」AB。但场景 1 的两臂由子代理提示**直接给 skill 路径** (`skill-creator` SKILL.md Step 1: `Skill path: <path-to-skill>`), description 在整条评测链路里没有作用面 ⇒ 对 description 维度, 「照跑了 AB」产出的是**空证据**。

Issue 提出「description 变动 ⇒ 另跑场景 4 触发率评测」, 并要求**先做基线实跑再写进规则**。基线跑完 (四轮六臂, RESULT.md v3), 三个事实改变了补法的形状:

1. **对真实 description 变动零区分力**: openspec-archive v1.71.1 → v1.73.0 两版与「pushy」正控全部 30/30 (query 级 10/10), Fisher p = 1.0。这是**饱和**: 三臂都撞天花板, 测不出差异。在饱和套件上, 两个都能让 should-trigger 饱和的 description 必然打平 (本次这一对即如此); 比较判据只在其中一方掉出饱和时才判出差别 (例如新版被改坏, 掉到负控那样的 8/30) —— 它不是恒绿门, 但对「措辞改得更好」这个问题, 在饱和套件上答不出来。
2. **场景 4 能当地板守卫, 已验证恰两类破坏**: 删领域词的负控 should-trigger 8/30 (query 级 3/10, 双侧 p = 0.0031); 显式强制过宽 (触发词表 + 「都必须先使用本技能」) 让 should-not 22/30 (7/10 条判红)。自然措辞扩张未验证 (OQ-8)。
3. **skill-creator `run_eval.py` 两处结构性缺陷 + 一处配置建议** (并发 worker 互见 / 合成技能的文件名、标题、首句都嵌入技能名 / 默认设置源加载全部用户插件), 不按前置运行数字不可解读。

⇒ 本 Spec 把 description 维度的 Rule #6 义务写成**它实际能承诺的形状** (地板守卫, 只承诺已验证的两类破坏, 不是 A/B), 把前置与局限成文, 并把「这偏离了 issue 验收第 2 条的规定动作」明列为 OQ-5 请 owner 裁 —— 不由 AI 自定。

## What Changes

### D1. Rule #6 判据表第二行 → 对 description hunk 的义务细化 (三处同批, 核心句逐字一致)

**落在决策表哪一格**: 这是 SOT §2 **第二行的细化**, 不新增行。description 是「处方性 · 运行时指令面」(它决定 skill 何时被激活), 属第二行「照跑, 零裁量」; 本 Spec 只把「照跑什么」按 hunk 类型说清: 指令流程 hunk ⇒ 场景 1; description hunk ⇒ 场景 4b (D2)。它**不是**第三行 (§3 三件套) 的实例: 第三行要求每个 spec 自建定向 fixture 并开套件缺口 issue, 而 description 维度的 fixture 已标准化为场景 4b、套件缺口由 D5.2 的 issue 承接, 不必每个 cycle 再走一遍三件套。SOT §3 末尾加一句边界注: 「description hunk 不走本节, 走 §2 第二行的场景 4b 义务」。

**本条只管深度, 不管广度**: 本条定「按 hunk 跑哪个场景」; 「场景 1 覆盖哪些套件 (单 skill 全套件还是 Tier 1)」是 `10CG/aria-standards#17` 在定的另一条轴, 两者正交 (见 D5.5)。

**只改 description 时场景 1 还跑不跑**: 分两种。description 改动只涉及触发面 (何时使用 / 使用场景 / 触发短语) ⇒ **不跑**场景 1: 触发这一维在场景 1 里结构上是空证据 (§3 所称测量剧场)。description 改动含行为指令句 (要求执行方式的句子, 如正控原文的「不要自己手工 mv」) ⇒ 该部分按指令流程 hunk 处理, **照跑**场景 1: 场景 1 的 with-skill 臂按 Skill path 读整份 SKILL.md, description 原文在其中, 行为指令能被部分观测到。拿不准属于哪种 ⇒ 照跑。「不跑」是对现行「一律照跑」文字的实质放宽, **列 OQ-6 请 owner 裁**; owner 不同意则改为「场景 1 + 场景 4b 都跑」。

**要替换的旧句 (逐字, 2026-09-14 `grep -F` 各命中 1 次) 与新句 (定稿)**:

| 落点 | 旧句 (逐字) | 新句 |
|---|---|---|
| Aria `CLAUDE.md` 规则 #6 表后 | `description` 或指令流程变动一律照跑; 豁免须在 spec/tasks 留 `rule6_note`。 | 指令流程变动一律照跑场景 1; `description` 变动一律跑场景 4b 地板守卫, 它只验证触发面没被改坏, 不验证 description 改得更好; 两者按 hunk 各自触发, 互不替代; 豁免与结果都写进 `rule6_note` (字段见 SOT §4.1)。 |
| SOT §2「SKILL.md 有变动时的附加约束」末句 | `description` 或指令流程变动 ⇒ 一律第二行。 | `description` 或指令流程变动 ⇒ 一律第二行; 第二行的「照跑」按 hunk 分: 指令流程 hunk ⇒ 场景 1, `description` hunk ⇒ 场景 4b 地板守卫 (它只验证触发面没被改坏, 不验证 description 改得更好; 判据与前置见 `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` §场景 4b); description 改动只涉及触发面时不跑场景 1 (触发这一维在场景 1 里是测量剧场, 见 §3), 含行为指令句的部分按指令流程 hunk 照跑场景 1, 拿不准照跑。本条只定「按 hunk 跑哪个场景」, 「场景 1 覆盖哪些套件」不在本条范围。 |
| 手册 §「确定性代码层变更 — deterministic substitute 豁免」的「边界与留痕」段首行 | `**边界与留痕**: 完整 fail-closed 边界三条 (SKILL.md 事实性同步例外 / description 与指令面变动零裁量照跑 /` | `**边界与留痕**: 完整 fail-closed 边界四条 (SKILL.md 事实性同步例外 / description 变动零裁量跑场景 4b 地板守卫, 它只验证触发面没被改坏, 不验证 description 改得更好 / 指令面变动零裁量跑场景 1 /` |

核心句 = 「**只验证触发面没被改坏, 不验证 description 改得更好**」, 三处逐字相同 (SC-1)。手册那一行的计数语同步由「三条」改「四条」(SC-7)。CLAUDE.md 新句自带「字段见 SOT §4.1」指向, **不在 CLAUDE.md 另加句子**。

### D2. 场景 4b「description 地板守卫」判据 (写进手册 §场景 4b, SOT §2 引用)

- **通过** = `run_eval.py` 输出的每条 `pass` 为真: 每条 should-trigger `trigger_rate ≥ 0.5` **且** 每条 should-not `trigger_rate < 0.5` (`run_eval()` 的 `did_pass` 语义, 已读源码核对)。
- **参数钉死** (阈值语义依赖 runs): `--runs-per-query 3` (0.5 门 = 2/3), `--trigger-threshold 0.5`, `--timeout 120`, `--num-workers 1` (D3 第 1 条), 显式 `--model` (D3 第 4 条), 套件 20 条 (10/10)。改任一参数 = 换判据, 须 owner 裁 (OQ-1 的 0.8 门 = 3/3)。
- **只承诺已验证的两类破坏**: 删领域词 (should-trigger 掉) 与显式强制过宽 (should-not 涨)。自然措辞扩张会不会判红, 取决于套件的近似误触覆盖; 未验证 (OQ-8)。
- **同批负控** (验证本轮数字可用, 不评 description):
  - 构造: 删去全部领域名词与该 skill 特有动作词, 只留「处理一件事项」级的泛化句 (基线负控保留了「收尾 / 核对」, 仍命中 3 条带这类动作语义的 query, 见 RESULT v3)。
  - 判据 (绝对门槛, 不以被评 description 为参照): 负控 query 级命中 (每 query 命中 := `trigger_rate ≥ 0.5`) 须 **≤ 5/10**。门通过时被评 description 必为 10/10, 此时 10 对 5 的 Fisher 单侧 p = 0.016 (10 对 6 为 0.043, 不取)。基线 v3 负控 3/10。
  - 被评 description 退化 ⇒ 门先判 **fail** (有 should-trigger 掉到 0.5 以下), 不会落到作废。
  - **作废**只在门通过而负控 ≥ 6/10 时发生 (套件分不开「有没有触发词」, 本轮数字不可用)。作废 = 本 cycle 的 Rule #6 义务未完成, **不得 ship**; 修套件或环境后重跑; rule6_note 记 `scenario4b: <结果目录> void`; **连续 2 轮作废 ⇒ 升级 owner** (AI 不得自行豁免, Rule #10)。
- **不设比较判据** (如新版触发率不低于旧版): 在饱和处退化 (Why 第 1 条); 如需比较, 只作 rule6_note 观察, 不作门。
- **套件**: 每个被评 skill 一份 `aria-plugin-benchmarks/ab-suite/trigger/<skill>.json` (20 条, should / should-not 各 10, should-not 以近似误触为主), **沿用 `ab-suite/` 版本化规则** (改套件须升 `ab-suite/version.yaml`, 旧数据不可比)。新套件是否须 owner 审阅后才能作门, 见 OQ-7。

### D3. 场景 4b 运行前置 (手册 §场景 4b 小节内的表, 恰六行; 前五条缺一数字不可解读, 第六条是产物形状)

「机读实证」列的路径均相对 `aria-plugin-benchmarks/ab-results/2026-09-13-rule6-description-trigger-eval-baseline/`; 带 `[配置推导]` 标记的行没有机读文件。

| # | 前置 | 机读实证 |
|---|---|---|
| 1 | `--num-workers 1` (消除同一项目根内的兄弟命令文件); 多臂并行时每臂一个独立项目根 (含空 `.claude/`)。两者正交。上游修好缺陷 (a) 后可放宽 (D5.4) | `v1-shared-root-4workers/new.json` · `v2-isolated-root-1worker/new.json` · `v1-shared-root-4workers/diag02-sibling-command-collision.jsonl` |
| 2 | 合成技能**中性化**: `name: helper` 的临时 SKILL.md 壳 + `--description` 显式传入 | `v2-isolated-root-1worker/negctrl.json` · `v3-isolated-root-1worker-neutral-name/negctrl.json` · `neutral-skill-SKILL.md` |
| 3 | `claude -p` 加 `--setting-sources project` (不加载用户级插件)。实证看两份 json 的 `result` 字段: 默认设置源的列表含真 `openspec-archive`, project-only 不含; 其中的技能数是模型自报, 不作证据 | `probe-setting-sources-default.json` · `probe-setting-sources-project.json` |
| 4 | 显式 `--model <本 session 模型>` (第 3 条会连带换掉默认模型) | [配置推导] RESULT.md v3「同一首次探针的附带观察」段, 未落机读文件 |
| 5 | 同批负控 (D2) | `v3-isolated-root-1worker-neutral-name/new.json` · `v3-isolated-root-1worker-neutral-name/negctrl.json` |
| 6 | 产物落 `aria-plugin-benchmarks/ab-results/<date>-<skill>-trigger/` + RESULT.md (对齐基线目录形状); 工具版本 (插件缓存 hash / Claude Code 版本 / 模型) 写进 RESULT | `RESULT.md` |

### D4. `rule6_note` 最小结构化模板 (新建, 宿主 = SOT 新增 §4.1)

现状: SOT §4 只有一句「都要在 spec/tasks 留 `rule6_note` 引用本规范」, 既有语料里 rule6_note 是自由格式 (2026-09-14 对现行 SOT grep 五个字段名, 均 0 命中)。本 Spec 在 §4 下**新起 §4.1「rule6_note 最小模板」**, 五个字段名逐字:

```yaml
rule6_note:
  decision_table_row: 1 | 2 | 3 | 4 | n/a   # SOT §2 决策表第几行 (4 = 拿不准照跑); n/a = 本 spec 不属 Skill 变更
  description_changed: yes | no
  scenario1: <结果目录> | not_required | n/a
  scenario4b: <结果目录> pass | <结果目录> fail | <结果目录> void | not_required | n/a
  negctrl: <被评命中>/10 vs <负控命中>/10 | n/a
```

- `description_changed: yes` 而 `scenario4b` 为空、`not_required` 或 `n/a` ⇒ 不合规; `scenario4b` 为 `void` ⇒ 义务未完成, 不得 ship (D2)。
- 两套编号不同轴: `decision_table_row` 取 SOT §2 决策表行号; `scenario1` / `scenario4b` 是手册的场景编号。§4.1 写一句说明。
- **无机械 enforcement** (本 Spec 不加 custom check): 合规靠审阅; 列入 SOT §6 局限 (D6)。
- **authoring 路径与过渡期**: spec-drafter / task-planner 模板同步由 D5.3 的新 issue 承接 (改它们是 SKILL.md 指令面, 会触发 Rule #6, 不并入本 Spec)。过渡期内起草者从 CLAUDE.md 规则 #6 新句的「字段见 SOT §4.1」获知模板 (CLAUDE.md 每 session 自动加载); 过渡期结束 = D5.3 那张 issue 关闭。

### D5. 缺口成单 + 上游反馈 + 双机制消歧 + 与 `10CG/aria-standards#17` 分工

1. 手册 §场景 4 拆为 **4a「Description 优化」(现状 run_loop.py 流程, 原样保留)** 与 **4b「Description 地板守卫」(新, D2 / D3)**。4b 是 Rule #6 义务, 4a 是可选优化; 4a 产出的新 description 落地前同样要过 4b。
2. 开 `10CG/Aria` issue「41 个 skill 无 trigger 套件」(`10CG/aria-plugin#150` 的对偶)。口径: `aria/skills/` 下 43 个目录、42 个含 SKILL.md (`issue-triage-workspace` 不是 skill), 现有 trigger 套件 0 个; 本 Spec 若执行 T4 则为 1 个, 余 41 个。
3. 开 `10CG/aria-plugin` issue「spec-drafter / task-planner 模板加 rule6_note 五字段」(D4 的 authoring 路径)。
4. 上游反馈 (skill-creator, Anthropic 官方插件; 渠道由 owner 定: 官方插件仓 issue 或 Claude Code 反馈) **须含**: 复现步骤、`diag02-sibling-command-collision.jsonl`、v1 / v2 / v3 记分表、两条修复方向 —— (i) 每个 worker 用独立 project root (或每次 run 用独立临时 cwd); (ii) 合成技能不嵌入真技能名, **文件名、`# <skill_name>` 标题、`This skill handles:` 首句三处都要改** (检测串仍保留 uuid, `clean_name in accumulated_json` 照常工作)。发出证据 (标题 + 时间 + 链接或反馈 ID) 记入 `10CG/Aria#211`。
5. 与 `10CG/aria-standards#17` 分工: 10CG/aria-standards#17 在同一 SOT 拟加「AB 范围」节, 定**广度** (场景 1 跑单 skill 全套件 + 定向 fixture, 还是 Tier 1 全量); 本 Spec 定**深度** (按 hunk 类型跑场景 1 还是 4b)。交叉点只有一处: 混合改动 (既有指令 hunk 又有 description hunk) 时, 场景 1 的范围按 10CG/aria-standards#17, 场景 4b 按本 Spec; 只改 description 时场景 1 不跑 (OQ-6), 10CG/aria-standards#17 的范围问题不出现。T7 合并前查 10CG/aria-standards#17 有无并行编辑, 并在 10CG/aria-standards#17 留言写明这条分工。

### D6. SOT §6 已知局限追加第三条 + 计数语

§6 开篇「后者另有两个已知缺陷记录在案」改「三个」; 追加第三条: 「场景 4b 只能当地板守卫: 对真实措辞改动在饱和套件上零区分力, 已验证的破坏类型只有删领域词与显式强制过宽两类 (基线: Aria 主仓 `aria-plugin-benchmarks/ab-results/2026-09-13-rule6-description-trigger-eval-baseline/RESULT.md` v3); rule6_note 五字段无机械 enforcement。」

### Key Deliverables (每条带 D 锚)

- `CLAUDE.md` 规则 #6 表后句 (D1; 含 §4.1 指向, D4)
- `standards/conventions/skill-benchmark-exemption.md`: §2 末句 (D1) / §3 边界注 (D1) / 新 §4.1 模板 (D4) / §6 第三条 + 计数语 (D6) / 文件头 Version 1.0.0 → 1.1.0
- `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md`: §场景 4 拆 4a / 4b (D5.1), 4b 含 D2 判据 + D3 前置表 + 两套编号说明 (D4); 「边界与留痕」段首行 (D1); §固定测试集 vs 临时测试 表加 `ab-suite/trigger/` 行 (D2)
- `aria-plugin-benchmarks/ab-suite/trigger/openspec-archive.json` + `ab-suite/version.yaml` 升版 (D2; **仅在 OQ-3 裁为「接受」后执行**)
- 两张新 issue (D5.2, D5.3) + 上游反馈发出证据 (D5.4) + `10CG/aria-standards#17` 分工留言 (D5.5)

## Impact

- 影响的 AI 行为: Rule #6 执行者在 description 变动时的义务判断: 从「照跑场景 1 即合规」变为「场景 4b 地板守卫 + rule6_note 五字段」; 只改 description 时不再跑场景 1 (OQ-6)。
- 不影响任何 skill 运行时行为; aria-plugin 零改动 ⇒ 本 Spec 自身不触发 Rule #6。
- 破坏性: 无; 已 ship 的 rule6_note 不回溯。
- 场景 4b 成本 (估算, 来源 RESULT.md v3 §时长与成本): 被评 + 负控两臂约 120 次 `claude -p`, 并行约 11–18 分钟 / 串行约 22–34 分钟 (单 worker 一臂 10m39s–17m39s, v2–v4 共 10 臂的 run.log), 约 10 美元 (按探针单次 0.08 美元估, `run_eval.py` 不记录成本)。首次为某 skill 建 20 条套件另加约 1 小时, 若须 owner 审阅另加 owner 时间 (OQ-7)。
- 对无套件 skill 的即时影响: 其余 41 个 skill 的下一次 description 变动都要先建套件; 这是有意的 (Rule #6 零裁量), 由 OQ-7 确认。

## Tasks

- [ ] T1 三处 D1 新句落地 (逐字), 旧句删除; 手册「边界三条」改「四条」; SOT §3 边界注。CLAUDE.md 只改这一句 (含 §4.1 指向), 不另加句
- [ ] T2 手册 §场景 4 拆 4a / 4b; 4b 写 D2 判据 (含「不设比较判据」固定措辞与负控 ≤ 5/10、连续 2 轮升级) + D3 六行前置表 (机读实证写全路径) + 两套编号说明; §固定测试集 vs 临时测试 表加 trigger 行
- [ ] T3 SOT 新增 §4.1 rule6_note 五字段模板 (D4) —— 只改 SOT
- [ ] T4 `ab-suite/trigger/openspec-archive.json` 搬入 (逐字节同基线) + `ab-suite/version.yaml` 升版 —— **OQ-3 裁定前不执行**; 若本 Spec ship 时 OQ-3 仍未裁, 本任务标 deferred 并记入 D5.2 的 issue
- [ ] T5 SOT §6 第三条 + 计数语 (D6); SOT 文件头 Version 1.1.0
- [ ] T6 开两张 issue (D5.2 / D5.3); 上游反馈发出 (渠道经 owner 确认) 并把证据记入 `10CG/Aria#211` (D5.4)
- [ ] T7 查 `10CG/aria-standards#17` 并行编辑并留分工言 (D5.5); standards 本地 `--no-ff` merge → 双推 → **对 origin 与 github 各自 `git ls-remote` 比对 SHA, 全部一致才算推成功** → 主仓 gitlink bump → 主仓双推同样逐 remote 核验
- [ ] T8 `10CG/Aria#211` 回帖: 基线结论 (RESULT.md v3) + 落地位置; 关单归 owner

## Success Criteria

- SC-1: `grep -cF "只验证触发面没被改坏, 不验证 description 改得更好"` 在 `CLAUDE.md`、SOT、手册三处各 ≥ 1 (逐字, 无同义替代)。
- SC-2: 手册 §场景 4b 小节内的前置表存在且恰六行 (行首编号 1–6 各一次); 带 `[配置推导]` 标记的行恰一行; 其余五行「机读实证」列里每个反引号路径拼上基线目录后 `test -e` 为真 (零行或行数不等于六即判红, 防真空成立)。
- SC-3: SOT §4.1 含五个字段名 (`decision_table_row` / `description_changed` / `scenario1` / `scenario4b` / `negctrl`) 各 ≥ 1 次, 且值域含 `void` 与 `n/a`; 反事实: 2026-09-14 对现行 SOT grep 五个名均为 0 (已实跑)。
- SC-4: `diff aria-plugin-benchmarks/ab-suite/trigger/openspec-archive.json <基线目录>/trigger-eval-openspec-archive.json` 为空, 且 `ab-suite/version.yaml` 的 `version` 按 semver 元组比较大于改前 `1.5.0`。T4 标 deferred 时本条改判「deferred 已记入 D5.2 的 issue」。
- SC-5: 用 python `re` 判 (不用 grep: Claude Code shell 里 `grep` 是 ugrep 包装, 带有界重复的多字节正则会报「exceeds complexity limits」, 与 owner 终端的 GNU grep 行为不同)。取手册 §场景 4b 小节正文 (从 `### 场景 4b` 到下一个 `###` 或 `##` 标题), 去掉含「不设比较判据」的行, 对剩余文本用正则 `(新版|新 description|被评)[^。;\n]{0,20}(≥|>=|不低于|高于|优于|不差于)[^。;\n]{0,10}(旧版|旧 description)` 计数 = 0; 且「不设比较判据」在该小节 ≥ 1 次。三处 D1 落点行 (含核心句的行) 用同一正则计数 = 0。正则的正反样本已自测 (2026-09-14: 两条比较句各命中 1, 「不设比较判据」行与负控门槛行均为 0)。
- SC-6: D5.2 / D5.3 两张 issue 存在 (`forgejo GET` 返回 200, 不限状态); `10CG/Aria#211` 有一条含「上游反馈」与发出时间的评论; `10CG/aria-standards#17` 有一条含本 Spec 目录名的评论。
- SC-7: SOT `grep -c "三个已知缺陷"` = 1 且 `grep -c "两个已知缺陷"` = 0; SOT `grep -cF '**Version**: 1.1.0'` = 1; 手册 `grep -c "边界四条"` = 1 且 `grep -c "边界三条"` = 0。
- SC-8: 手册含 `### 场景 4a` 与 `### 场景 4b` 两个标题各恰 1 次。
- SC-9: 手册 §场景 4b 小节含负控门槛「≤ 5/10」与升级条款「连续 2 轮」各 ≥ 1 次。
- SC-10: 手册 §场景 4b 小节含 D2 钉死的参数串 `--runs-per-query 3` / `--trigger-threshold 0.5` / `--timeout 120` / `--num-workers 1` 与「20 条」各 ≥ 1 次; SOT `grep -cF "description hunk 不走本节"` = 1 (§3 边界注)。

## Open Questions (owner 裁; 每项给推荐与代价)

- OQ-1 D2 阈值: 沿用 0.5 (= 2/3), 还是 0.8 (= 3/3)。**推荐 0.5**: 三个真 description 基线均 1.0, 0.8 也过; 但 0.8 会让偶发一次非技能开局判红, 误报代价高。代价: 0.5 门放过「2/3 才触发」的 description。
- OQ-2 D3 第 1 条: 等上游修 (a) 还是长期写「单 worker + 独立根」。**推荐后者**, 上游修好后再放宽; 代价: 两臂并行需两个临时根, 手册步骤多两行。
- OQ-3 20 条 query 未经 owner 审阅: 接受为 trigger 套件 v1, 还是 owner 先审再 T4。**推荐先审** (skill-creator Step 2 要求); 代价: 若改动 query, 基线数字与套件 v1 脱节, 需重跑被评与负控两臂, 并行约 11–18 分钟 / 约 10 美元。**默认 (未裁时)**: T4 不执行, 不让未审套件搭车进 `ab-suite/`。
- OQ-4 Level: owner 2026-09-13 指示「开 Level 2 cycle」, 本 Spec 按 Level 2 执行。相关成文规则: LEVEL_GUIDE §跨模块判断「跨模块 → 自动提升为 Level 3」, 条件之一「涉及 2 个及以上模块」。按该指南的模块映射, 本 Spec 只落在 standards 一个模块 (`standards/**`; `CLAUDE.md` 与 `aria-plugin-benchmarks/` 不在映射里); 按 meta-repo 口径则是主仓与 standards 子模块两处。请 owner 在知道这条规则的前提下确认 Level 2, 或改为 Level 3。维持 2 的代价: 不产 tasks.md、不跑 post_planning 审计, T1–T8 的验收只写在本 proposal。改 3 的代价: 补 tasks.md 并跑 post_planning 五席审计 (本 Spec 的 post_spec 每轮约半小时, R1 / R2 实测)。
- OQ-5 **偏离 issue 验收第 2 条**: issue 原文 (逐字): 「**区分力必须非零** —— 若两个 description 的触发率在统计上无差别, 说明场景 4 在本仓语料下同样测不到, 那就是**又一个测量剧场**, 应改开「触发率评测本身不可用」的单而不是把它写进 Rule #6;」。基线正命中 (p = 1.0)。本 Spec 的选择: **仍写进 Rule #6, 但只写成地板守卫** (理由: 负控与过宽两侧都有真实 FAIL 样本, 评测「不可用」的是 A/B 用途, 不是守卫用途)。所选项的代价: Rule #6 多一条义务 (每次 description 改动多一次场景 4b, 约 10 美元与半小时, 首次还要建套件), 而它只挡两类已验证的破坏。**备选 (issue 字面)**: 不写进 Rule #6, 只开「评测不可用」单 + SOT §6 局限; 代价: description 维度继续零证据, 每次 description 改动照旧跑场景 1 生成空记录。请 owner 二选一。
- OQ-6 只改 description 时**不跑**场景 1 (D1): 对现行「一律照跑」的实质放宽。备选「两者都跑」的代价按历史实测: 单 skill 场景 1 AB (`aria-plugin-benchmarks/ab-results/2026-09-04-v1.69.1-spec-drafter-rule5-hunkA/` 下 8 个 `timing.json` 求和) 子代理累计 27.1 分钟、约 65 万 token, 成本未记录; 换来的是对触发这一维的空证据。所选「不跑」的代价: 仅触发面改动时, 若改动意外影响了执行行为, 无人观测; 按 D1 的分法含行为指令句的改动仍跑场景 1, 残余风险限于「看似只改触发面、实际影响执行」。
- OQ-7 其余 41 个 skill 的首次建套件, 与「新套件要不要 owner 审阅」合并裁: **(A) owner 审阅是前置**: 套件审过才能作门; 代价: 每个 skill 首次改 description 时要等 owner 审 20 条 query (约 15 分钟 owner 时间), owner 不在线即阻塞。**(B) 暂定运行**: cycle 作者建套件并跑, rule6_note 标 `provisional`, owner 事后审; 审阅改动套件则重跑 (约 12–14 分钟 / 约 10 美元); 代价: 审阅前的门可能由弱套件判出假绿。**推荐 (A)** (改的是不可协商规则的执行面, 门的质量由 owner 把关); 两者都不设「套件补齐前免跑」的过渡 lane。
- OQ-8 **自然措辞扩张的敏感度**: 是否在 ship 前补跑一臂「轻微过宽」(多加两三个泛化词、无强制指令) 验证守卫会不会判红。代价: 一臂约 12 分钟 / 约 5 美元, 须用基线同一模型 (`claude-fable-5-1`) 才可比。**推荐不阻塞 ship**: 守卫的判据是「套件里的近似误触有没有被触发」, 轻微扩张若没有触发任何近似误触, 按定义就不算改坏触发面; 该局限已写进 SOT §6 与 RESULT v3。不补跑的代价: 首个真实使用前, 守卫对自然扩张的判别力没有数据。

## rule6_note

```yaml
rule6_note:
  decision_table_row: n/a       # 本 Spec 改的是规范 / 手册 / 套件数据, 无 SKILL.md、无 references/、无 description 变动, 不属决策表任一行的「Skill 变更」
  description_changed: no
  scenario1: n/a
  scenario4b: n/a
  negctrl: n/a
```

本 cycle 由 AI 作出、待 owner 复议的流程判断 (Rule #10): 基线实跑先于 spec 起草 (依 Rule #6「跑 benchmark 本身不需要 OpenSpec」); 20 条 query 未经 owner 审阅即用于基线 (OQ-3); Level 2 自判 (OQ-4); 选择地板守卫而非 issue 验收第 2 条的字面路径 (OQ-5); 只改 description 时不跑场景 1 (OQ-6)。

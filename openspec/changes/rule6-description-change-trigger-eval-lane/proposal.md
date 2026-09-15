# Proposal: rule6-description-change-trigger-eval-lane

> **Level**: Minimal (Level 2 Spec) — owner 2026-09-13 指示「开 Level 2 cycle」; 与 LEVEL_GUIDE「跨模块 → 自动提升为 Level 3」的关系请 owner 确认, 见 OQ-4
> **Status**: Draft — post_spec R1 (2026-09-13) FAIL → v2; R2 (2026-09-14, 5 席) PASS_WITH_WARNINGS 0C / 10M / 26m → v3; R3 (2026-09-14, 5 席) PASS_WITH_WARNINGS 0C / 5M / 6m → v4; R4 (2026-09-14, 5 席) PASS_WITH_WARNINGS 0C / 3M / 4m → v5; R5 (2026-09-14, 5 席) PASS_WITH_WARNINGS 0C / 6M / 4m, max_rounds 耗尽未收敛 → v6; owner 2026-09-15 裁定增加 2 轮 (max_rounds 5 → 7) 并先收窄范围 → v7 (本版), 待 R6
> **Created**: 2026-09-13
> **Linked Issue**: `10CG/Aria#211`
> **代码落点**: 无代码。三份规范性文本 (Aria `CLAUDE.md` Rule #6 / `standards/conventions/skill-benchmark-exemption.md` / `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md`) + 一个套件文件 (受 OQ-3 约束) + 三张新 issue + 一条上游反馈。**aria-plugin 子模块不动** (spec-drafter / task-planner 模板落地另开 issue, 见 D5.3)
> **ship target**: standards 子模块 (SOT 文件头 Version 1.0.0 → 1.1.0, MINOR — 新增强制义务。这是**单份规范文档自己的版本行**, 与 `version-management.md` §5.1 待裁的「standards 仓级版本自称」正交, 不新增仓级自称面; standards 仓无 tag, 主仓只动 gitlink) + Aria 主仓 (CLAUDE.md / 手册 / 套件)
> **基线数据**: `aria-plugin-benchmarks/ab-results/2026-09-13-rule6-description-trigger-eval-baseline/RESULT.md` **v6** (与本版同批提交; 本文引用的数字以该版本为准, RESULT 再修订须同步重核本文 §Why 与 §D2 §D3)
> **溯源**: 洞的首次记录 = `10CG/aria-plugin#190` comment 22921 (2026-09-08); 独立成单 = `10CG/Aria#211` (2026-09-09); triage 五项核对全命中 = `10CG/Aria#211` comment 23915 (2026-09-13)

## Why

Rule #6 判据表第二行逐字要求「`description` 或指令流程变动一律照跑」AB。但场景 1 的两臂由子代理提示**直接给 skill 路径** (`skill-creator` SKILL.md Step 1: `Skill path: <path-to-skill>`), description 在整条评测链路里没有作用面 ⇒ 对 description 维度, 「照跑了 AB」产出的是**空证据**。

Issue 提出「description 变动 ⇒ 另跑场景 4 触发率评测」, 并要求**先做基线实跑再写进规则**。基线跑完 (五轮九臂, RESULT.md v6), 三个事实改变了补法的形状:

1. **对真实 description 变动零区分力**: openspec-archive v1.71.1 → v1.73.0 两版与「pushy」正控全部 30/30 (query 级 10/10), Fisher p = 1.0。这是**饱和**: 三臂都撞天花板, 测不出差异。在饱和套件上, 两个都能让 should-trigger 饱和的 description 必然打平 (本次这一对即如此); 比较判据只在其中一方掉出饱和时才判出差别 (例如新版被改坏, 掉到负控那样的 8/30) —— 它不是恒绿门, 但对「措辞改得更好」这个问题, 在饱和套件上答不出来。
2. **场景 4 能当地板守卫, 已验证恰两类破坏**: 删领域词的负控 should-trigger 8/30 (query 级 3/10, 双侧 p = 0.0031); 显式强制过宽 (触发词表 + 「都必须先使用本技能」) 让 should-not 22/30 (7/10 条判红)。一次自然措辞扩张实测不判红 (v5, `claude-opus-5`): 守卫判得出什么, 由套件里的近似误触决定 (OQ-8)。
3. **skill-creator `run_eval.py` 两处结构性缺陷 + 一处配置建议** (并发 worker 互见 / 合成技能的文件名与 `# <skill_name>` 标题都嵌入技能名 / 默认设置源加载全部用户插件), 不按前置运行数字不可解读。

⇒ 本 Spec 把 description 维度的 Rule #6 义务写成**它实际能承诺的形状** (地板守卫, 只承诺已验证的两类破坏, 不是 A/B), 把前置与局限成文, 并把「这偏离了 issue 验收第 2 条的规定动作」明列为 OQ-5 请 owner 裁 —— 不由 AI 自定。

## What Changes

### D1. Rule #6 判据表第二行 → 对 description hunk 的义务细化 (三处同批, 核心句逐字一致)

**落在决策表哪一格**: 这是 SOT §2 **第二行的细化**, 不新增行。description 是「处方性 · 运行时指令面」(它决定 skill 何时被激活), 属第二行「照跑, 零裁量」; 本 Spec 只把「照跑什么」说清: 指令流程 hunk ⇒ 场景 1; description hunk ⇒ 场景 1 **另加**场景 4b (D2), 两者不互相替代 (issue 原建议 1)。它**不是**第三行 (§3 三件套) 的实例: 第三行要求每个 spec 自建定向 fixture 并开套件缺口 issue, 而 description 维度的 fixture 已标准化为场景 4b、套件缺口由 D5.2 的 issue 承接, 不必每个 cycle 再走一遍三件套。SOT §3 末尾加一句边界注: 「description hunk 不走本节, 走 §2 第二行: 照跑场景 1, 另须跑场景 4b」。

**自主运行时只写一句禁令** (owner 2026-09-15 确认收窄范围): 自主模式下 description 变动的完整处理 —— 遇到时不自动重试、改为等 owner 裁; 告警带上是哪个 skill、为什么要改; 由 Layer 1 把不涉及 description 的部分拆成新 issue 继续派发; 场景 4b 在 Layer 2 所用模型上的验证 —— 全部放进 D5.6 的跟进 spec, 本 Spec 不展开; 该跟进 spec 须在这类任务派给 runner 之前落地。禁令写成「放弃整个任务、不提交任何改动」, 不写「跳过这一部分」, 依据 (已读代码): runner (`aria-orchestrator/docker/aria-runner/modes/initial.sh`) 只有结果为 SUCCESS 时以 0 退出, 编排器 `_handle_s5_await` 只看退出码、非零即进 S_FAIL ⇒ 整单不提交必进 S_FAIL, 部分跳过则可能按 SUCCESS 推进、无人察觉。禁令以 `state_scanner.coordination.unattended` 为准; 该键从 Layer 1 传到 Layer 2 的契约未定义、缺失时静默回落 `false` (`10CG/Aria#196`), 已列入 D5.6 的已知缺口。

**本条只管深度, 不管广度**: 本条定「跑哪个场景」; 「场景 1 覆盖哪些套件 (单 skill 全套件还是 Tier 1)」是 `10CG/aria-standards#17` 在定的另一条轴, 两者正交 (见 D5.5)。

**只改 description 时场景 1 还跑不跑**: **照跑**。description 里「技能做什么」这类能力陈述, 既影响何时被激活, 也影响激活后怎么做; 场景 1 的 with-skill 臂按 Skill path 读整份 SKILL.md, description 原文在其中, 能观测后一半。把 description 拆成「只影响触发」与「也影响执行」两类, 执行者无法可靠判断 (基线那次真实改动「自动修正 CLI bug」→「并做归档后落点校验」两类都沾), 所以**不设放宽**。场景 1 对触发这一维仍是空证据, 这一维由场景 4b 补。放宽的可能性留作 OQ-6。

**要替换的旧句 (逐字, 2026-09-14 `grep -F` 各命中 1 次) 与新句 (定稿)**:

| 落点 | 旧句 (逐字) | 新句 |
|---|---|---|
| Aria `CLAUDE.md` 规则 #6 表后 | `description` 或指令流程变动一律照跑; 豁免须在 spec/tasks 留 `rule6_note`。 | 指令流程或 `description` 变动一律照跑场景 1; `description` 变动另须跑场景 4b 地板守卫, 它只验证触发面没被改坏, 不验证 description 改得更好; 豁免与结果都写进 `rule6_note` (字段见 SOT §4.1); 自主运行时的处置见 SOT §2。 |
| SOT §2「SKILL.md 有变动时的附加约束」末句 | `description` 或指令流程变动 ⇒ 一律第二行。 | `description` 或指令流程变动 ⇒ 一律第二行, 照跑场景 1; `description` 变动另须跑场景 4b 地板守卫 (它只验证触发面没被改坏, 不验证 description 改得更好; 判据与前置见 Aria 主仓 `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` §场景 4b), 两者不互相替代。自主运行时 (`state_scanner.coordination.unattended == true`) 不做 description 改动: 任务需要改 description 时放弃整个任务、不提交任何改动, 并在最终消息里写明是哪个 skill、为什么要改。本条只定「跑哪个场景」, 「场景 1 覆盖哪些套件」不在本条范围。 |
| 手册 §「确定性代码层变更 — deterministic substitute 豁免」的「边界与留痕」段首行 | `**边界与留痕**: 完整 fail-closed 边界三条 (SKILL.md 事实性同步例外 / description 与指令面变动零裁量照跑 /` | `**边界与留痕**: 完整 fail-closed 边界四条 (SKILL.md 事实性同步例外 / description 与指令面变动零裁量照跑场景 1 / description 变动另须跑场景 4b 地板守卫, 它只验证触发面没被改坏, 不验证 description 改得更好 /` |

核心句 = 「**只验证触发面没被改坏, 不验证 description 改得更好**」, 三处逐字相同 (SC-1)。手册那一行的计数语同步由「三条」改「四条」(SC-7)。CLAUDE.md 新句自带「字段见 SOT §4.1」指向, **不在 CLAUDE.md 另加句子**。

### D2. 场景 4b「description 地板守卫」判据 (写进手册 §场景 4b, SOT §2 引用)

- **通过** = `run_eval.py` 输出的每条 `pass` 为真: 每条 should-trigger `trigger_rate ≥ 0.5` **且** 每条 should-not `trigger_rate < 0.5` (`run_eval()` 的 `did_pass` 语义, 已读源码核对)。
- **参数钉死** (阈值语义依赖 runs): `--runs-per-query 3` (0.5 门 = 2/3), `--trigger-threshold 0.5`, `--timeout 120`, `--num-workers 1` (见前置表第 1 条), 显式 `--model` (见前置表第 4 条), 套件 20 条 (10/10)。改任一参数 = 换判据, 须 owner 裁 (例: 阈值 0.8 在 3 runs 下等于 3/3)。
- **只承诺已验证的两类破坏**: 删领域词 (should-trigger 掉) 与显式强制过宽 (should-not 涨)。一次自然措辞扩张 (多加「与相关文档 / 整理项目收尾材料 / 整理归档文档 / 收尾整理」四处, 其中「整理归档文档」直接带被测 skill 的领域词) 实测不判红 (RESULT v6 §v5): 守卫判得出什么, 由套件里的近似误触决定。
- **同批参照臂**: 改动前的现行 description, 与被评 description、负控同批跑。参照臂过不了门 ⇒ 本轮作废, 不判被评 description。必须有它, 因为 `run_eval.py` 把异常、超时、`claude -p` 自身报错都记成一次「未触发」, `runs` 恒为 3, 环境故障在输出 json 里与「真没触发」无法区分 (源码: `run_eval()` 的 `except Exception` 分支 append `False`; `run_single_query` 超时返回 `False`)。
- **同批负控** (验证本轮数字可用, 不评 description):
  - 构造: 删去全部领域名词与该 skill 特有动作词, 只留「处理一件事项」级的泛化句 (基线负控保留了「收尾 / 核对」, 仍命中 3 条带这类动作语义的 query; 按本规则构造的「对一个事项做处理。」在 v5 为 0/10, 见 RESULT v6)。
  - 判据 (绝对门槛, 不以被评 description 为参照): 负控 query 级命中 (每 query 命中 := `trigger_rate ≥ 0.5`) 须 **≤ 5/10**。门通过时被评 description 必为 10/10, 此时 10 对 5 的 Fisher 单侧 p = 0.016 (10 对 6 为 0.043, 不取)。基线 v3 负控 3/10。
  - 被评 description 退化 ⇒ 门先判 **fail** (有 should-trigger 掉到 0.5 以下), 不会落到作废。
  - **作废**在以下任一情形发生: 同批参照臂过不了门 (环境、套件或现行 description 本身有问题); 门通过而负控 ≥ 6/10 (套件分不开「有没有触发词」); `run_eval.py` 的 stderr 出现 `Warning: query failed` (有 query 抛了异常)。作废时不判被评 description。作废 = 本 cycle 的 Rule #6 义务未完成, **不得 ship**; 修套件或环境后重跑; rule6_note 记 `scenario4b: <结果目录> void`; **连续 2 轮作废 ⇒ 升级 owner** (AI 不得自行豁免, Rule #10)。
- **fail 的后果**: 同批参照臂过门、而被评 description 的门判 fail ⇒ 该 description 改动**不得 ship** (与 void 同为义务未完成)。处置二选一: (1) 修正 description 直到门通过; (2) 若 fail 来自**有意**收窄或拓宽触发面 (套件原来的 should / should-not 划分已不符合新意图), 则先改套件 (升 `ab-suite/version.yaml`, 新套件经 owner 审阅) 再重跑; 两条都不走 ⇒ 升级 owner。rule6_note 记 `scenario4b: <结果目录> fail` 与所走的处置。
- **不设比较判据** (如新版触发率不低于旧版): 在饱和处退化 (见基线目录 RESULT.md 结论 1); 如需比较, 只作 rule6_note 观察, 不作门。
- **套件**: 每个被评 skill 一份 `aria-plugin-benchmarks/ab-suite/trigger/<skill>.json` (20 条, should / should-not 各 10, should-not 以近似误触为主), **沿用 `ab-suite/` 版本化规则** (改套件须升 `ab-suite/version.yaml`, 旧数据不可比)。should-not 的近似误触须覆盖该 skill 最可能被扩到的相邻任务 (v5: 本套件对「整理收尾材料」这一幅度的扩张不敏感)。新套件须经 owner 审阅后才能作门。

### D3. 场景 4b 运行前置 (手册 §场景 4b 小节内的表, 恰六行; 前五条缺一数字不可解读, 第六条是产物形状)

「机读实证」列的路径均相对 `aria-plugin-benchmarks/ab-results/2026-09-13-rule6-description-trigger-eval-baseline/`; 带 `[配置推导]` 标记的行没有机读文件。

| # | 前置 | 机读实证 |
|---|---|---|
| 1 | `--num-workers 1` (消除同一项目根内的兄弟命令文件); 多臂并行时每臂一个独立项目根 (含空 `.claude/`)。两者正交。上游修好 `run_eval.py` 的并发互见缺陷后可放宽 | `v1-shared-root-4workers/new.json` · `v2-isolated-root-1worker/new.json` · `v1-shared-root-4workers/diag02-sibling-command-collision.jsonl` |
| 2 | 合成技能**中性化**: `name: helper` 的临时 SKILL.md 壳 + `--description` 显式传入 | `v2-isolated-root-1worker/negctrl.json` · `v3-isolated-root-1worker-neutral-name/negctrl.json` · `neutral-skill-SKILL.md` |
| 3 | `claude -p` 加 `--setting-sources project` (不加载用户级插件)。实证看两份 json 的 `result` 字段: 默认设置源的列表含真 `openspec-archive`, project-only 不含; 其中的技能数是模型自报, 不作证据 | `probe-setting-sources-default.json` · `probe-setting-sources-project.json` |
| 4 | 显式 `--model <本 session 模型>` (第 3 条会连带换掉默认模型) | [配置推导] RESULT.md v6「同一首次探针的附带观察」段, 未落机读文件 |
| 5 | 同批参照臂与负控 (判据见本小节上文) | `v3-isolated-root-1worker-neutral-name/new.json` · `v3-isolated-root-1worker-neutral-name/negctrl.json` · `v5-mildcreep-opus5/new.json` |
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

- `scenario4b` 所用套件未经 owner 审阅 ⇒ 不合规 (该结果不能作门)。
- `description_changed: yes` 而 `scenario1` 或 `scenario4b` 为空、`not_required` 或 `n/a` ⇒ 不合规 (见 §2: description 变动照跑场景 1, 另须跑场景 4b); `scenario4b` 为 `fail` 或 `void` ⇒ 义务未完成, 不得 ship (处置见 Aria 主仓 `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` §场景 4b)。
- 两套编号不同轴: `decision_table_row` 取 SOT §2 决策表行号; `scenario1` / `scenario4b` 是手册的场景编号。

**转录范围**: T3 只把上面的 YAML 模板、紧随其后的合规条款与「两套编号不同轴」一句写进 SOT §4.1; 本节其余要点是本 proposal 的说明, 不转录。

**随 OQ-7 裁定变化的部分 (不转录)**: 以上模板按 OQ-7 的推荐 (交互模式 A) 起草。若 owner 在交互模式裁 (B) 暂定运行, T3 前在 `scenario4b` 值域加 ` provisional` 后缀 (如 `<结果目录> pass provisional`), 并把「所用套件未经 owner 审阅 ⇒ 不合规」改为「provisional 结果须经 owner 事后审阅, 审阅改动套件则重跑」。

- **无机械 enforcement** (本 Spec 不加 custom check): 合规靠审阅; 列入 SOT §6 局限 (D6)。
- **authoring 路径与过渡期**: spec-drafter / task-planner 模板同步由 D5.3 的新 issue 承接 (改它们是 SKILL.md 指令面, 会触发 Rule #6, 不并入本 Spec)。过渡期内起草者从 CLAUDE.md 规则 #6 新句的「字段见 SOT §4.1」获知模板 (CLAUDE.md 每 session 自动加载); 过渡期结束 = D5.3 那张 issue 关闭。

### D5. 缺口成单 + 上游反馈 + 双机制消歧 + 与 `10CG/aria-standards#17` 分工

1. 手册 §场景 4 拆为 **4a「Description 优化」(现状 run_loop.py 流程, 原样保留)** 与 **4b「Description 地板守卫」(新, D2 / D3)**。4b 是 Rule #6 义务, 4a 是可选优化; 4a 产出的新 description 落地前同样要过 4b。
2. 开 `10CG/Aria` issue「41 个 skill 无 trigger 套件」(`10CG/aria-plugin#150` 的对偶)。口径: `aria/skills/` 下 43 个目录、42 个含 SKILL.md (`issue-triage-workspace` 不是 skill), 现有 trigger 套件 0 个; 本 Spec 若执行 T4 则为 1 个, 余 41 个。
3. 开 `10CG/aria-plugin` issue「spec-drafter / task-planner 模板加 rule6_note 五字段」(D4 的 authoring 路径)。
4. 上游反馈 (skill-creator, Anthropic 官方插件; 渠道由 owner 定: 官方插件仓 issue 或 Claude Code 反馈) **须含**: 复现步骤、`diag02-sibling-command-collision.jsonl`、v1 / v2 / v3 记分表、两条修复方向 —— (i) 每个 worker 用独立 project root (或每次 run 用独立临时 cwd); (ii) 合成技能不嵌入真技能名, **文件名与 `# <skill_name>` 标题两处都要改** (`This skill handles:` 首句嵌的是 description, 不是技能名, 不在修复范围; 检测串仍保留 uuid, `clean_name in accumulated_json` 照常工作)。发出证据 (标题 + 时间 + 链接或反馈 ID) 记入 `10CG/Aria#211`。
5. 与 `10CG/aria-standards#17` 分工: 10CG/aria-standards#17 在同一 SOT 拟加「AB 范围」节, 定**广度** (场景 1 跑单 skill 全套件 + 定向 fixture, 还是 Tier 1 全量); 本 Spec 定**深度** (按 hunk 类型跑场景 1 还是 4b)。交叉点: 凡跑场景 1 (包括只改 description 时), 场景 1 的范围按 `10CG/aria-standards#17` 定; 场景 4b 按本 Spec。T7 合并前查 10CG/aria-standards#17 有无并行编辑, 并在 10CG/aria-standards#17 留言写明这条分工。
6. 开 `10CG/Aria` issue「自主模式下 description 变动的处理 (跟进 spec)」, 写入 owner 2026-09-15 给出的目标设计: 遇到需要改 description 的任务, 编排器用一种新的失败类型 (如「需要 owner 裁决」), 不自动重试, 改为等 owner 裁; 告警原样带上 Layer 2 写明的原因 (哪个 skill、为什么要改); 由 Layer 1 把不涉及 description 的部分拆成新 issue 继续派发。同时列入已知缺口: 编排器目前不读 runner 的结果枚举 (`CLAUDE_NO_OP` 等) 与 Claude 的说明, 放弃后的失败类型记为 `container_crash` 且默认自动重试; `unattended` 键从 Layer 1 到 Layer 2 的传递未定义 (`10CG/Aria#196`); runner 镜像没有场景 4b 依赖的 skill-creator; 场景 4b 只在 Claude 模型上实测过, Layer 2 所用 GLM 未验证; 自主模式下新套件由谁审 (可选做法: 并入 S7 签字 / 离线批量预审 / 走 AD10 回滚路径 Level 2 加 gate)。**硬前提**: 该跟进 spec 须在要改 skill description 的任务派给 runner 之前落地。
7. 开 `10CG/Aria` issue「编排器不消费 runner 结果枚举: 部分跳过的改动会按 SUCCESS 推进」(`CLAUDE_NO_OP` 等在 Layer 1 零消费, `_handle_s5_await` 只看退出码); 属 aria-orchestrator 改动, 不在本 Spec 范围, 只成单追踪。

### D6. SOT §6 已知局限追加第三条 + 计数语

§6 开篇「后者另有两个已知缺陷记录在案」改「三个」; 追加第三条: 「场景 4b 只能当地板守卫: 对真实措辞改动在饱和套件上零区分力, 已验证判红的破坏类型是删领域词与显式强制过宽两类 (未穷举), 一次自然措辞扩张实测不判红 (基线: Aria 主仓 `aria-plugin-benchmarks/ab-results/2026-09-13-rule6-description-trigger-eval-baseline/RESULT.md` v6, 写入时附当时的版本号与提交 SHA); rule6_note 五字段无机械 enforcement; 场景 4b 只在 Claude 模型上实测过 (`claude-fable-5-1` / `claude-opus-5`), Layer 2 所用的 GLM 未验证。」

### Key Deliverables (每条带 D 锚)

- `CLAUDE.md` 规则 #6 表后句 (D1; 含 §4.1 指向, D4)
- `standards/conventions/skill-benchmark-exemption.md`: §2 末句 (D1) / §3 边界注 (D1) / 新 §4.1 模板 (D4) / §6 第三条 + 计数语 (D6) / 文件头 Version 1.0.0 → 1.1.0
- `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md`: §场景 4 拆 4a / 4b (D5.1), 4b 含 D2 判据 + D3 前置表 + 两套编号说明 (D4); 「边界与留痕」段首行 (D1); §固定测试集 vs 临时测试 表加 `ab-suite/trigger/` 行 (D2)
- `aria-plugin-benchmarks/ab-suite/trigger/openspec-archive.json` + `ab-suite/version.yaml` 升版 (D2; **仅在 OQ-3 裁为「接受」后执行**)
- 三张新 issue (D5.2, D5.3, D5.6) + 上游反馈发出证据 (D5.4) + `10CG/aria-standards#17` 分工留言 (D5.5)

## Impact

- 影响的 AI 行为: Rule #6 执行者在 description 变动时的义务判断: 从「照跑场景 1 即合规」变为「照跑场景 1 + 场景 4b 地板守卫 + rule6_note 五字段」。
- 不影响任何 skill 运行时行为; aria-plugin 零改动 ⇒ 本 Spec 自身不触发 Rule #6。
- 破坏性: 无; 已 ship 的 rule6_note 不回溯。
- 场景 4b 成本 (估算, 来源 RESULT.md v6 §时长与成本): 被评 + 参照 + 负控三臂约 180 次 `claude -p`, 并行约 11–20 分钟 / 串行约 32–59 分钟 (单 worker 一臂: `claude-fable-5-1` 上 10m39s–17m39s, `claude-opus-5` 上 15m18s–19m41s; v2–v5 共 13 臂的 run.log), 约 15 美元 (按探针单次 0.08 美元估, `run_eval.py` 不记录成本)。首次为某 skill 建 20 条套件另加约 1 小时, 若须 owner 审阅另加 owner 时间 (OQ-7)。
- 自主运行时 (v2.0 Layer 2): 本 Spec 只写一句禁令 (D1)。跟进 spec (D5.6) 落地之前, 自主 runner 不改任何 skill 的 description, 需要时整单放弃。影响面: aria-plugin 历史 577 次提交里, 改了已有 skill description 的只有 6 次, 约 1% (逐提交比对 frontmatter); 一般开发任务不受影响。代价: runner 开跑后碰到这类任务, 会被打进 S_FAIL (失败类型记为 `container_crash`) 并默认自动重试、反复告警, 直到 owner 手动阻止该 issue 自动派发 (`aria-orchestrator/docs/layer-boundary-contract.md` §S_FAIL handling); 所以跟进 spec 须在这类任务派给 runner 之前落地。
- 对无套件 skill 的即时影响: 其余 41 个 skill 的下一次 description 变动都要先建套件; 这是有意的 (Rule #6 零裁量), 由 OQ-7 确认。

## Tasks

- [ ] T0 转录纪律 (T1–T5 通用): 写进规范的文字去掉本 proposal 的内部编号 (OQ-n / Dn / Tn / SC-n), 按 owner 对 OQ 的裁定写成确定的文字 (SC-11)
- [ ] T1 三处 D1 新句落地 (逐字), 旧句删除; 手册「边界三条」改「四条」; SOT §3 边界注。CLAUDE.md 只改这一句 (含 §4.1 指向), 不另加句
- [ ] T2 手册 §场景 4 拆 4a / 4b; 4b 写 D2 判据 (参数照抄为以「参数钉死」开头的一行; 含「不设比较判据」固定措辞与负控 ≤ 5/10、连续 2 轮升级) + D3 六行前置表 (机读实证写相对基线目录的完整相对路径, 不写省略号或通配) + 两套编号说明; §固定测试集 vs 临时测试 表加 trigger 行
- [ ] T3 SOT 新增 §4.1 rule6_note 五字段模板 (D4) —— 只改 SOT
- [ ] T4 `ab-suite/trigger/openspec-archive.json` 搬入 (逐字节同基线) + `ab-suite/version.yaml` 升版 —— **OQ-3 裁定前不执行**; 若本 Spec ship 时 OQ-3 仍未裁, 本任务标 deferred 并记入 D5.2 的 issue
- [ ] T5 SOT §6 第三条 + 计数语 (D6); SOT 文件头 Version 1.1.0
- [ ] T6 开三张 issue (D5.2 / D5.3 / D5.6); 上游反馈发出 (渠道经 owner 确认) 并把证据记入 `10CG/Aria#211` (D5.4)
- [ ] T7 查 `10CG/aria-standards#17` 并行编辑并留分工言 (D5.5); standards 本地 `--no-ff` merge → 双推 → **对 origin 与 github 各自 `git ls-remote` 比对 SHA, 全部一致才算推成功** → 主仓 gitlink bump → 主仓双推同样逐 remote 核验
- [ ] T8 `10CG/Aria#211` 回帖: 基线结论 (RESULT.md v6) + 落地位置; 关单归 owner

## Success Criteria

- SC-1: `grep -cF "只验证触发面没被改坏, 不验证 description 改得更好"` 在 `CLAUDE.md`、SOT、手册三处各 ≥ 1 (逐字, 无同义替代); 且三处含核心句的那一行都同时含「照跑场景 1」与「另须跑场景 4b」(D1 的 fail-closed 形状: 按 v3 旧新句落地时这两串缺一, 本条转红)。
- SC-2: 手册 §场景 4b 小节内的前置表存在且恰六行 (数据行首列编号 1–6 各一次)。**只取每行第三列 (「机读实证」列)** 的反引号路径, 拼上基线目录后 `test -e` 为真; 第三列带 `[配置推导]` 标记的行恰一行, 该行第三列不要求路径。第二列 (前置) 里的反引号串 (如产物落点模板 `aria-plugin-benchmarks/ab-results/<date>-<skill>-trigger/`) 不参与判定。零行或行数不等于六即判红 (防真空成立)。
- SC-3: SOT §4.1 含五个字段名 (`decision_table_row` / `description_changed` / `scenario1` / `scenario4b` / `negctrl`) 各 ≥ 1 次, 且值域含 `void` 与 `n/a`, 且 §4.1 含说明两套编号不同轴的一句 (`grep -cF "两套编号"` ≥ 1); 反事实: 2026-09-14 对现行 SOT grep 五个名均为 0 (已实跑)。
- SC-4: `diff aria-plugin-benchmarks/ab-suite/trigger/openspec-archive.json <基线目录>/trigger-eval-openspec-archive.json` 为空, 且 `ab-suite/version.yaml` 的 `version` 按 semver 元组比较大于改前 `1.5.0`。T4 标 deferred 时本条改判「deferred 已记入 D5.2 的 issue」。
- SC-5: 用 python `re` 判 (不用 grep: Claude Code shell 里 `grep` 是 ugrep 包装, 带有界重复的多字节正则会报「exceeds complexity limits」, 与 owner 终端的 GNU grep 行为不同)。取手册 §场景 4b 小节正文 (从 `### 场景 4b` 到下一个 `###` 或 `##` 标题), 去掉含「不设比较判据」的行, 对剩余文本用正则 `(新版|新 description|被评)[^。;\n]{0,20}(≥|>=|不低于|高于|优于|不差于)[^。;\n]{0,10}(旧版|旧 description)` 计数 = 0; 且「不设比较判据」在该小节 ≥ 1 次。三处 D1 落点行 (含核心句的行) 用同一正则计数 = 0。正则的正反样本已自测 (2026-09-14: 两条比较句各命中 1, 「不设比较判据」行与负控门槛行均为 0)。
- SC-6: D5.2 / D5.3 / D5.6 三张 issue 存在 (`forgejo GET` 返回 200, 不限状态); `10CG/Aria#211` 有一条含「上游反馈」与发出时间的评论; `10CG/aria-standards#17` 有一条含本 Spec 目录名的评论。
- SC-7: SOT `grep -c "三个已知缺陷"` = 1 且 `grep -c "两个已知缺陷"` = 0; SOT `grep -cF '**Version**: 1.1.0'` = 1; 手册 `grep -c "边界四条"` = 1 且 `grep -c "边界三条"` = 0。
- SC-8: 手册含 `### 场景 4a` 与 `### 场景 4b` 两个标题各恰 1 次。
- SC-9: 手册 §场景 4b 小节含负控门槛「≤ 5/10」与升级条款「连续 2 轮」各 ≥ 1 次; 且同时含「fail 的后果」与「不得 ship」的行 ≥ 1、同时含「作废」与「不得 ship」的行 ≥ 1 (两条后果各用本条款的标题词定位、分别断言: 只删其中一条, 本条转红; 不用单独的「fail」定位, 因为作废条款里的 `Warning: query failed` 也含 fail, v7 自检实测); 且含「参照臂」≥ 1。
- SC-11 (转录纪律): 转录进规范的文字 —— `CLAUDE.md` 与 SOT §2 含核心句的那一行、SOT §3 边界注、SOT §4.1、SOT §6 第三条、手册 §场景 4a 与 §场景 4b 小节 —— 用 python `re` 统计 `OQ-\d`、`\bD\d(?:\.\d)?\b`、`\bT\d\b`、`\bSC-\d` 与「Why 第」均为 0: 本 proposal 的内部编号 (OQ-n / Dn / Tn / SC-n 与章节指代) 出了本文件无法定位, 转录时必须改写成确定的文字 (如「见下方前置表第 1 条」)。
- SC-12: SOT 含核心句的那一行同时含「unattended == true」「不做 description 改动」「放弃整个任务」与「写明」; `CLAUDE.md` `grep -cF "自主运行时的处置见 SOT §2"` = 1; SOT `grep -cF "只在 Claude 模型上实测过"` = 1 (三处都是给自主模式划的边界, 转录时漏掉任一处本条转红)。
- SC-10: 手册 §场景 4b 小节里含「参数钉死」的那一行 (D2 判据正文) 须同时含 `--runs-per-query 3` / `--trigger-threshold 0.5` / `--timeout 120` / `--num-workers 1` 与「20 条」。**按行判, 不按小节判**: 前置表第 1 行也有 `--num-workers 1`, 按小节判会漏掉判据正文里的删除 (R3 qa 席反事实实测)。SOT `grep -cF "description hunk 不走本节"` = 1, 且该行同时含「照跑场景 1」与「另须跑场景 4b」(§3 边界注; 只查「不走本节」的话, 写回 v3 / v4 的旧边界注也能命中, R5 qa 席反事实实测)。

## Open Questions (owner 裁; 每项给推荐与代价)

- OQ-1 D2 阈值: 沿用 0.5 (= 2/3), 还是 0.8 (= 3/3)。**推荐 0.5**: 三个真 description 基线均 1.0, 0.8 也过; 但 0.8 会让偶发一次非技能开局判红, 误报代价高。代价: 0.5 门放过「2/3 才触发」的 description。
- OQ-2 D3 第 1 条: 等上游修 (a) 还是长期写「单 worker + 独立根」。**推荐后者**, 上游修好后再放宽; 代价: 两臂并行需两个临时根, 手册步骤多两行。
- OQ-3 20 条 query 未经 owner 审阅: 接受为 trigger 套件 v1, 还是 owner 先审再 T4。**推荐先审** (skill-creator Step 2 要求); 代价: 若改动 query, 基线数字与套件 v1 脱节, 需重跑被评、参照、负控三臂, 并行约 11–20 分钟 / 约 15 美元。**默认 (未裁时)**: T4 不执行, 不让未审套件搭车进 `ab-suite/`。
- OQ-4 Level: owner 2026-09-13 指示「开 Level 2 cycle」, 本 Spec 按 Level 2 执行。相关成文规则: LEVEL_GUIDE §跨模块判断「跨模块 → 自动提升为 Level 3」, 条件之一「涉及 2 个及以上模块」。按该指南的模块映射, 本 Spec 只落在 standards 一个模块 (`standards/**`; `CLAUDE.md` 与 `aria-plugin-benchmarks/` 不在映射里); 按 meta-repo 口径则是主仓与 standards 子模块两处。请 owner 在知道这条规则的前提下确认 Level 2, 或改为 Level 3。维持 2 的代价: 不产 tasks.md、不跑 post_planning 审计, T1–T8 的验收只写在本 proposal。改 3 的代价: 补 tasks.md 并跑 post_planning 五席审计 (本 Spec 的 post_spec 每轮约半小时, R1 / R2 实测)。
- OQ-5 **偏离 issue 验收第 2 条**: issue 原文 (逐字): 「**区分力必须非零** —— 若两个 description 的触发率在统计上无差别, 说明场景 4 在本仓语料下同样测不到, 那就是**又一个测量剧场**, 应改开「触发率评测本身不可用」的单而不是把它写进 Rule #6;」。基线正命中 (p = 1.0)。本 Spec 的选择: **仍写进 Rule #6, 但只写成地板守卫** (理由: 负控与过宽两侧都有真实 FAIL 样本, 评测「不可用」的是 A/B 用途, 不是守卫用途)。所选项的代价: Rule #6 多一条义务 (每次 description 改动多一次场景 4b, 约 15 美元与半小时 (被评、参照、负控三臂), 首次还要建套件), 而它只挡两类已验证的破坏。**备选 (issue 字面)**: 不写进 Rule #6, 只开「评测不可用」单 + SOT §6 局限; 代价: description 维度继续零证据, 每次 description 改动照旧跑场景 1 生成空记录。请 owner 二选一。
- OQ-6 **是否允许放宽** (只跑 4b, 不跑场景 1): 本 Spec 默认不放宽 (D1)。可选的放宽口径: description 改动经逐行点名, 确认只增删「使用场景 / 触发短语列表」、不动「做什么」陈述时, 只跑 4b。放宽的收益: 每次省一次场景 1 (历史实测: `aria-plugin-benchmarks/ab-results/2026-09-04-v1.69.1-spec-drafter-rule5-hunkA/` 下 8 个 `timing.json` 求和, 子代理累计 27.1 分钟、约 65 万 token, 成本未记录)。放宽的代价: 依赖执行者正确点名; 点错了, 执行面的变化无人观测。**推荐暂不放宽**, 等积累几次场景 4b 的真实使用数据再议; 该推荐的代价是每次 description 改动都多跑一次场景 1。
- OQ-7 其余 41 个 skill 的首次建套件, 与「新套件要不要 owner 审阅」合并裁 (本 Spec 只管交互模式; 自主模式见 D1 的禁令与 D5.6 跟进 spec): (A) owner 审阅是前置, 套件审过才能作门; 代价: 每个 skill 首次改 description 时要等 owner 审 20 条 query (约 15 分钟 owner 时间), owner 不在线即阻塞。(B) 暂定运行, cycle 作者建套件并跑, 结果带 ` provisional` 后缀 (D4), owner 事后审; 审阅改动套件则重跑 (并行约 11–20 分钟 / 约 15 美元); 代价: 审阅前的门可能由弱套件判出假绿。**推荐 (A)** (改的是不可协商规则的执行面, 门的质量由 owner 把关), 其代价即 (A) 所列。两种做法都不设「套件补齐前免跑」的过渡 lane。
- OQ-8 **自然措辞扩张 (已补跑, v5)**: 跑前写定判读规则, 在 `claude-opus-5` 上同批三臂: 参照 description 过门、按新规则构造的负控 0/10、轻微过宽 description 过门 (10 条 should-not 全 0/3)。⇒ 守卫对这一幅度的扩张不判红; 这是局限的实证确认, 不是守卫失效。**推荐**: 判据不改; D2 套件要求写明「should-not 的近似误触须覆盖最可能被扩到的相邻任务」(v4 已写入); 局限写进 SOT §6 (D6)。该推荐的代价: 套件没覆盖到的扩张, 守卫仍判不出。备选: 现在就给 openspec-archive 套件补「整理收尾材料」类近似误触并重跑; 代价是套件改版 (升 `ab-suite/version.yaml`)、一次两臂重跑, 且受 OQ-3 审阅约束。

## rule6_note

```yaml
rule6_note:
  decision_table_row: n/a       # 本 Spec 改的是规范 / 手册 / 套件数据, 无 SKILL.md、无 references/、无 description 变动, 不属决策表任一行的「Skill 变更」
  description_changed: no
  scenario1: n/a
  scenario4b: n/a
  negctrl: n/a
```

本 cycle 由 AI 作出、待 owner 复议的流程判断 (Rule #10): 基线实跑先于 spec 起草 (依 Rule #6「跑 benchmark 本身不需要 OpenSpec」); 20 条 query 未经 owner 审阅即用于基线 (OQ-3); Level 2 按 owner 指示执行, 与 LEVEL_GUIDE 跨模块规则的关系待确认 (OQ-4); 选择地板守卫而非 issue 验收第 2 条的字面路径 (OQ-5); v5 补跑用 `claude-opus-5` 而非基线的 `claude-fable-5-1` (Fable 额度耗尽; 三臂同批, 只做臂间比较)。

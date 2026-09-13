# Proposal: rule6-description-change-trigger-eval-lane

> **Level**: Minimal (Level 2 Spec)
> **Status**: Draft
> **Created**: 2026-09-13
> **Linked Issue**: `10CG/Aria#211`
> **代码落点**: 无代码; 三份规范性文本 (Aria `CLAUDE.md` Rule #6 / `standards/conventions/skill-benchmark-exemption.md` / `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` §场景 4) + 一条上游缺陷单
> **ship target**: standards 子模块 PATCH (SOT 文本) + Aria 主仓 (CLAUDE.md + 手册); aria-plugin **不动** (不触发 Rule #6)
> **基线数据**: `aria-plugin-benchmarks/ab-results/2026-09-13-rule6-description-trigger-eval-baseline/RESULT.md` (本 Spec 起草前实跑, 依 `10CG/Aria#211` 验收第 1–3 条)

## Why

Rule #6 判据表第二行逐字要求「`description` 或指令流程变动一律照跑 AB」。但照跑的场景 1 两臂由子代理提示**直接给 skill 路径** (`skill-creator` SKILL.md Step 1: `Skill path: <path-to-skill>`), description 在整条评测链路里没有作用面 ⇒ 「照跑了 AB」对 description 维度产出的是**空证据**。这是 `10CG/Aria#211` 的原命题, 2026-09-13 triage 五项核对全部命中 (comment 23915)。

Issue 提出的补法是「description 变动 ⇒ 另跑场景 4 触发率评测」, 并要求**先做基线实跑再写进规则**。基线跑完 (三轮, 四臂, 见 RESULT.md), 结论改变了补法的形状:

1. 对真实的 description 变动 (openspec-archive v1.71.1 → v1.73.0), 场景 4 **零区分力**: 新旧两版与「pushy」正控全部 30/30, Fisher p = 1.0。⇒ 把「新版触发率不低于旧版」写成判据会**恒绿**, 是另一个测量剧场。
2. 场景 4 **能抓「把 description 毁掉」**: 删光触发词的负控 8/30, 与三个真 description 的差距 p < 0.0001; should-not 四臂三轮 0/30。⇒ 它只能当**地板守卫**。
3. skill-creator `run_eval.py` 有两处结构性缺陷 (并发 worker 互见合成命令 ⇒ 命中率压到约 1/N; 合成命令名含技能名 ⇒ 泄漏意图, 负控也 27/30), 不按特定前置运行, 数字不可解读。

所以本 Spec 不是「把场景 4 接进 Rule #6」, 而是**把 description 维度的验证义务写成它实际能承诺的形状**, 并把前置与局限成文, 防止下一次「照跑了」再变成空证据。

## What Changes

### D1. Rule #6 判据表第二行拆成两个义务 (三处同批, 口径逐字一致)

落点: Aria `CLAUDE.md` 不可协商规则 #6 表后那句; `standards/conventions/skill-benchmark-exemption.md` §2 「SKILL.md 有变动时的附加约束」; `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` §边界与留痕 (行 480 附近的「description 与指令面变动零裁量照跑」)。

- 指令流程变动 ⇒ 照跑场景 1 (不变)。
- `description` 变动 ⇒ **另跑场景 4 地板守卫** (D2 判据), 场景 1 **不替代**它; 且 rule6_note 必须写明「场景 4 结果 + 本次改动是否可能被场景 4 区分」。
- 明文: 场景 4 **不验证** description 措辞改动「是否更好」; 它只验证触发面**没被改坏**。这句话是本 Spec 的核心, 三处都要有, 不许只写在手册里。

### D2. 场景 4 作为地板守卫的判据 (写进手册 §场景 4, SOT §2 引用)

- 通过 = 全部 should-trigger query 的 `trigger_rate ≥ trigger_threshold` (默认 0.5) **且** 全部 should-not query 的 `trigger_rate < trigger_threshold`。即 `run_eval.py` 自己的 `pass` 全真。
- **不设**「新版 ≥ 旧版」比较判据 (基线实证恒打平)。若要比较, 只允许作为观察写进 rule6_note, 不作为门。
- 套件: 每个被评 skill 一份 `trigger-eval.json` (20 条, should / should-not 各 10, should-not 以近似误触为主), 落 `aria-plugin-benchmarks/ab-suite/trigger/<skill>.json`; 首次为某 skill 跑场景 4 时建, 之后复用, 改动须在 rule6_note 点名。

### D3. 场景 4 运行前置 (手册 §场景 4 新增小节, 缺一条数字不可解读)

1. 每臂 (每个 description) **独立项目根** (空 `.claude/`), `--num-workers 1`; 或上游修好 (a) 后按修后版本执行。
2. 合成命令名**中性化**: 用 `name: helper` 的临时 SKILL.md 壳 + `--description` 显式传入待测 description; 不用真 skill 名。
3. `claude -p` 加 `--setting-sources project` (不加载用户级插件: 真 skill 不与合成技能竞争, 成本降约 9 倍); 显式 `--model <本 session 模型>`。
4. 至少跑一个**负控** (删光触发词) 与被评 description 同批; 负控必须显著低于被评 description, 否则本轮数字作废 (说明套件或环境失效, 不是 description 的事)。
5. 产物落 `aria-plugin-benchmarks/ab-results/<date>-<skill>-trigger/` 并写 RESULT.md (对齐本基线目录的形状)。

### D4. rule6_note 模板加栏 (SOT §4)

`rule6_note` 新增两栏: `description_changed: yes|no`; 为 yes 时 `scenario4: <结果目录> | pass|fail | 负控 <x>/<n>`。空着即不合规 (与 issue 建议 3 一致)。

### D5. 上游缺陷成单 + 本仓缺口记录

- 向 skill-creator (Anthropic 官方插件) 反馈 `run_eval.py` 缺陷 (a) (b) (c) —— 经 Claude Code 反馈渠道; 在 `10CG/Aria#211` 与本 Spec 留反馈发出的证据。
- `10CG/aria-plugin#150` (14/43 skill 无 AB 套件) 的对偶: 为 43 个 skill 建 `trigger-eval.json` 是增量债, **本 Spec 不建**, 只建 openspec-archive 一份 (已有) 作范式; 缺口记进手册 §场景 4「已知局限」。

### Key Deliverables

- `CLAUDE.md` Rule #6 第 6 条文字 (D1)
- `standards/conventions/skill-benchmark-exemption.md` §2 / §4 / §6 (D1, D4, 局限)
- `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` §场景 4 重写 (D1, D2, D3) + §边界与留痕 (D1)
- `aria-plugin-benchmarks/ab-suite/trigger/openspec-archive.json` (由基线目录的 20 条搬入, D2)
- 上游反馈记录 (D5)

## Impact

- 影响的 AI 行为: Rule #6 执行者在 description 变动时的义务判断 (从「照跑场景 1 即合规」变为「场景 1 + 场景 4 地板守卫 + rule6_note 两栏」)。
- 不影响任何 skill 运行时行为; aria-plugin 无改动 ⇒ 本 Spec 自身**不触发 Rule #6** (改的是规范与手册, 不是 SKILL.md / references / description)。
- 破坏性: 无。已 ship 的 rule6_note 不回溯; 新栏只对本 Spec ship 之后的 cycle 生效。
- 成本: 场景 4 一次 (1 description + 1 负控) 约 120 次 `claude -p`, 隔离后约 8 美元、约 12 分钟 (基线实测 60 次 / 臂 ≈ 11 分钟, 单 worker)。

## Tasks

- [ ] T1 三处 D1 文字同批落地, 三处逐字对照 (`grep` 同一句核心句)
- [ ] T2 手册 §场景 4 重写: D2 判据 + D3 前置 + 已知局限 (含「对措辞微调零区分力」的基线引用)
- [ ] T3 SOT §4 rule6_note 模板加两栏 (D4); §6 已知局限追加「场景 4 只能当地板守卫」
- [ ] T4 `ab-suite/trigger/openspec-archive.json` 从基线目录搬入 (逐字节同 `trigger-eval-openspec-archive.json`)
- [ ] T5 上游反馈发出并留证 (D5)
- [ ] T6 standards 子模块本地 `--no-ff` merge + 双推 + 主仓 gitlink; 版本按 `version-management.md` PATCH
- [ ] T7 `10CG/Aria#211` 回帖: 基线结论 + 本 Spec 落地位置; 关单归 owner

## Success Criteria

- SC-1: `grep -c "只验证触发面没被改坏"` (或 owner 定稿的同义核心句) 在 `CLAUDE.md`、SOT、手册三处各 ≥ 1, 且三处引用的判据 (D2) 一致。
- SC-2: 手册 §场景 4 含 D3 五条前置, 且每条都能对应到基线 RESULT.md 里一个实证 (a: v1 vs v2; b: v2 vs v3; c: 技能数 97 vs 13; 负控: v3 8/30; 产物形状: 本目录)。
- SC-3: rule6_note 模板两栏存在; 用一份「description 变动但两栏空」的 rule6_note 试填, 按模板文字能判出不合规 (反事实: 旧模板判不出)。
- SC-4: `ab-suite/trigger/openspec-archive.json` 与基线 `trigger-eval-openspec-archive.json` `diff` 为空。
- SC-5: 三处 D1 文字**不**含「新版触发率 ≥ 旧版」类比较判据 (基线实证恒打平; 写了就是恒绿门)。
- SC-6: 上游反馈的发出证据 (反馈 ID 或截图) 记录在 `10CG/Aria#211`。

## Open Questions (owner 裁)

- OQ-1 D2 阈值: 沿用 `run_eval.py` 默认 0.5, 还是收紧到 should-trigger ≥ 0.8 (基线三个真 description 均 1.0, 负控 0.27)?
- OQ-2 D3 第 1 条是等上游修 (a) 还是本仓手册长期写「单 worker + 独立根」? 建议后者 (不依赖上游节奏), 上游修好后再放宽。
- OQ-3 20 条 query 套件未经 owner 审阅 (skill-creator Step 2 要求); 是接受为 v1 套件, 还是 owner 先审再 T4?
- OQ-4 Level: 本 Spec 只改规范文本无代码, 自判 Level 2; 若 owner 认为「改 Rule #6 = 方法论核心变更」应升 Level 3, 加 tasks.md。

## rule6_note

本 Spec 改动全部为规范 / 手册 / 套件数据, 无 SKILL.md、无 `references/`、无 description 变动 ⇒ Rule #6 不触发 (不属决策表任一行的「Skill 变更」)。基线实跑本身依 Rule #6 「跑 benchmark 本身不需要 OpenSpec」在起草前完成。

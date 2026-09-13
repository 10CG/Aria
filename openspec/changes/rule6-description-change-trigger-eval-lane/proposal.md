# Proposal: rule6-description-change-trigger-eval-lane

> **Level**: Minimal (Level 2 Spec) — 自判, 见 OQ-4 (跨主仓 + standards 子模块, LEVEL_GUIDE「跨模块 → Level 3」判据可能适用)
> **Status**: Draft — post_spec R1 (2026-09-13, 5 席) FAIL 1C / 14M / 17m → rework v2 (本版), 待 R2
> **Created**: 2026-09-13
> **Linked Issue**: `10CG/Aria#211`
> **代码落点**: 无代码。三份规范性文本 (Aria `CLAUDE.md` Rule #6 / `standards/conventions/skill-benchmark-exemption.md` / `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md`) + 一个套件文件 + 两张新 issue + 一条上游反馈。**aria-plugin 子模块不动** (spec-drafter 模板落地另开 issue, 见 D5)
> **ship target**: standards 子模块 (SOT 文件头 Version 1.0.0 → 1.1.0, MINOR — 新增强制义务; standards 仓无 tag 无 VERSION 文件, 按 `version-management.md` §5.1 meta-repo 类只动 gitlink) + Aria 主仓 (CLAUDE.md / 手册 / 套件)
> **基线数据**: `aria-plugin-benchmarks/ab-results/2026-09-13-rule6-description-trigger-eval-baseline/RESULT.md` **v2** (与本版同批提交; 本文引用的全部数字以该版本为准, RESULT 再修订须同步重核本文 §Why 与 §D3)
> **溯源**: 洞的首次记录 = `10CG/aria-plugin#190` comment 22921 (2026-09-08); 独立成单 = `10CG/Aria#211` (2026-09-09); triage 五项核对全命中 = `10CG/Aria#211` comment 23915 (2026-09-13)

## Why

Rule #6 判据表第二行逐字要求「`description` 或指令流程变动一律照跑」AB。但场景 1 的两臂由子代理提示**直接给 skill 路径** (`skill-creator` SKILL.md Step 1: `Skill path: <path-to-skill>`), description 在整条评测链路里没有作用面 ⇒ 对 description 维度, 「照跑了 AB」产出的是**空证据**。

Issue 提出「description 变动 ⇒ 另跑场景 4 触发率评测」, 并要求**先做基线实跑再写进规则**。基线跑完 (四轮六臂, RESULT.md v2), 三个事实改变了补法的形状:

1. **对真实 description 变动零区分力**: openspec-archive v1.71.1 → v1.73.0 两版与「pushy」正控全部 30/30 (query 级 10/10), Fisher p = 1.0。这是**饱和**: 三臂都撞天花板, 测不出差异。在饱和处「新版 ≥ 旧版」类比较判据对任何两个真 description 都打平, 只在对照物是坏 description 时才判红 —— 它不是恒绿门, 但作为 A/B 尺子失效。
2. **场景 4 能当地板守卫, 两侧都有真实 FAIL 样本**: 负控 (删领域词) should-trigger 8/30 (query 级 p = 0.0031); 过宽 description 让 should-not 22/30 (7/10 条判红)。
3. **skill-creator `run_eval.py` 有两处结构性缺陷 + 一处配置建议** (并发 worker 互见 / 合成命令名泄漏技能名 / 默认设置源加载全部用户插件), 不按前置运行数字不可解读。

⇒ 本 Spec 把 description 维度的 Rule #6 义务写成**它实际能承诺的形状** (地板守卫, 不是 A/B), 把前置与局限成文, 并把「这偏离了 issue 验收第 2 条的规定动作」明列为 OQ-5 请 owner 裁 —— 不由 AI 自定。

## What Changes

### D1. Rule #6 判据表第二行 → 对 description hunk 的义务细化 (三处同批, 核心句逐字一致)

**落在决策表哪一格**: 这是 SOT §2 **第二行的细化**, 不新增行。理由: description 是「处方性 · 运行时指令面」(它决定 skill 何时被激活), 属第二行「照跑, 零裁量」; 本 Spec 只是把「照跑什么」按 hunk 类型说清: 指令流程 hunk ⇒ 场景 1; description hunk ⇒ 场景 4b (D2)。它**不是**第三行 (§3 三件套) 的实例 —— 第三行要求每个 spec 自建定向 fixture 并开套件缺口 issue, 而 description 维度的 fixture 已标准化为场景 4b、套件缺口已由 `10CG/Aria#211` + D5 的新 issue 承接, 不必每个 cycle 再走一遍三件套。SOT §3 末尾加一句边界注: 「description hunk 不走本节, 走 §2 第二行的场景 4b 义务」。

**只改 description 时场景 1 还跑不跑**: **不跑**。场景 1 对该维度结构上是空证据 (§3 所称测量剧场), 跑它不产生信息只产生成本。这是对现行「一律照跑」文字的实质放宽, **列 OQ-6 请 owner 裁**; owner 不同意则改为「场景 1 + 场景 4b 都跑」。

**要替换的旧句 (逐字) 与新句 (定稿, 三处同一句)**:

| 落点 | 旧句 (逐字) | 新句 |
|---|---|---|
| Aria `CLAUDE.md` 规则 #6 表后 | `description` 或指令流程变动一律照跑; 豁免须在 spec/tasks 留 `rule6_note`。 | 指令流程变动一律照跑场景 1; **`description` 变动一律跑场景 4b 地板守卫, 它只验证触发面没被改坏, 不验证 description 改得更好** (基线: RESULT.md v2); 两者按 hunk 各自触发, 互不替代; 豁免与结果都写进 `rule6_note` (字段见 SOT §4)。 |
| SOT §2 「SKILL.md 有变动时的附加约束」末句 | `description` 或指令流程变动 ⇒ 一律第二行。 | `description` 或指令流程变动 ⇒ 一律第二行; 第二行的「照跑」按 hunk 分: 指令流程 hunk ⇒ 场景 1, **`description` hunk ⇒ 场景 4b 地板守卫 (它只验证触发面没被改坏, 不验证 description 改得更好)**; 只改 description 时不跑场景 1 (对该维度是测量剧场, 见 §3)。 |
| 手册 §「确定性代码层变更 — deterministic substitute 豁免」的「边界与留痕」段 | description 与指令面变动零裁量照跑 | description 变动零裁量跑场景 4b 地板守卫 (**它只验证触发面没被改坏, 不验证 description 改得更好**), 指令面变动零裁量跑场景 1 |

核心句 = 「**只验证触发面没被改坏, 不验证 description 改得更好**」, 三处逐字相同 (SC-1 的 grep 目标)。

### D2. 场景 4b「description 地板守卫」判据 (写进手册, SOT §2 引用)

- 通过 = `run_eval.py` 输出的每条 `pass` 为真: 每条 should-trigger `trigger_rate ≥ 0.5` **且** 每条 should-not `trigger_rate < 0.5` (`run_eval()` 的 `did_pass` 语义, 已读源码核对)。
- **参数钉死** (阈值语义依赖 runs): `--runs-per-query 3` (0.5 门 = 2/3), `--trigger-threshold 0.5`, `--timeout 120`, 套件 20 条 (10/10)。改任一参数 = 换判据, 须 owner 裁 (OQ-1 的 0.8 门 = 3/3)。
- **同批负控**: 与被评 description 同批跑一臂「删光领域词」负控; 判据 = **query 级** (每 query 命中 := `trigger_rate ≥ 0.5`) 被评 description 的 should-trigger 命中数 ≥ 负控命中数 + 4 (n=10 时 Fisher 单侧 p 约 0.03 以内; 基线 v3 为 10 vs 3)。不满足 ⇒ 本轮数字作废 (套件或环境失效, 不归因 description), 不判 description 好坏。
- **不设**「新版 ≥ 旧版」比较判据 (Why 第 1 条); 如需比较, 只作 rule6_note 观察, 不作门。
- 套件: 每个被评 skill 一份 `aria-plugin-benchmarks/ab-suite/trigger/<skill>.json` (20 条, should / should-not 各 10, should-not 以近似误触为主), **沿用 `ab-suite/` 版本化规则** (改套件须升 `ab-suite/version.yaml`, 旧数据不可比)。首次为某 skill 跑场景 4b 的 cycle 建套件 (约 1 小时 + 一次运行), 无套件不构成豁免。

### D3. 场景 4b 运行前置 (手册新小节; 前五条缺一数字不可解读, 第六条是产物形状)

| # | 前置 | 机读实证 (基线目录) |
|---|---|---|
| 1 | 每臂 (每个 description) **独立项目根** (含空 `.claude/`), 且 `--num-workers 1`。两者正交: 单 worker 消除同根内兄弟命令文件; 独立根允许多臂并行。上游修好缺陷 (a) 后可放宽 (D5) | `v1-shared-root-4workers/*.json` vs `v2-isolated-root-1worker/*.json`; `v1-…/diag02-sibling-command-collision.jsonl` |
| 2 | 合成命令名**中性化**: `name: helper` 的临时 SKILL.md 壳 + `--description` 显式传入 | `v2-…` vs `v3-isolated-root-1worker-neutral-name/*.json`; `neutral-skill-SKILL.md` |
| 3 | `claude -p` 加 `--setting-sources project` (不加载用户级插件) | `probe-setting-sources-default.json` (97 个技能, 含真 skill) vs `probe-setting-sources-project.json` (12 个) |
| 4 | 显式 `--model <本 session 模型>` (第 3 条会改掉默认模型) | 配置推导 (探针 `modelUsage` 字段), **无对照实测** |
| 5 | 同批负控 (D2) | `v3-…/negctrl.json` (8/30 vs 30/30) |
| 6 | 产物落 `aria-plugin-benchmarks/ab-results/<date>-<skill>-trigger/` + RESULT.md (对齐基线目录形状); 工具版本 (插件缓存 hash / Claude Code 版本 / 模型) 写进 RESULT | 基线目录本身 |

### D4. `rule6_note` 最小结构化模板 (新建, 宿主 = SOT §4)

现状: SOT §4 只有一句「都要在 spec/tasks 留 `rule6_note` 引用本规范」, 既有语料里 rule6_note 是自由格式。本 Spec **新建**最小模板 (五个字段, YAML 或表格均可, 字段名逐字):

```yaml
rule6_note:
  decision_table_row: 1 | 2 | 3 | 照跑        # SOT §2 决策表落格
  description_changed: yes | no
  scenario1: <结果目录> | not_required | n/a  # 指令流程 hunk 时必填
  scenario4b: <结果目录> pass|fail | not_required  # description_changed=yes 时必填
  negctrl: <被评命中>/10 vs <负控命中>/10       # scenario4b 跑了就必填
```

`description_changed: yes` 而 `scenario4b` 空或 `not_required` ⇒ 不合规。模板只落 SOT §4 + CLAUDE.md 一句指向; **spec-drafter / task-planner 的模板同步另开 aria-plugin issue** (改它们是 SKILL.md 指令面, 会触发 Rule #6 场景 1, 不并入本 Spec)。

### D5. 缺口成单 + 上游反馈 + 双机制消歧

1. 手册 §场景 4 拆为 **4a「Description 优化」(现状 run_loop.py 流程, 原样保留)** 与 **4b「Description 地板守卫」(新, D2/D3)**; 4b 是 Rule #6 义务, 4a 是可选优化; 4a 产出的新 description 落地前同样要过 4b。
2. 开 `10CG/Aria` issue「42/43 skill 无 trigger 套件」(`10CG/aria-plugin#150` 的对偶; 本 Spec 只交付 openspec-archive 一份作范式)。
3. 开 `10CG/aria-plugin` issue「spec-drafter / task-planner 模板加 rule6_note 五字段」(D4 的 authoring 路径落地)。
4. 上游反馈 (skill-creator, Anthropic 官方插件, 经 Claude Code 反馈渠道) **须含**: 复现步骤、`diag02-sibling-command-collision.jsonl`、v1/v2/v3 记分表、两条修复方向 (每 worker 独立 project root; 命令文件名不嵌技能名)。发出证据 (反馈标题 + 时间) 记入 `10CG/Aria#211`。
5. 合并 SOT 前查 `10CG/aria-standards#17` (同文件相邻区域拟加「AB 范围」节) 是否已有并行编辑; 有则先协调编号。

### D6. SOT §6 已知局限追加第三条 + 计数语

§6 开篇「后者另有两个已知缺陷记录在案」改「三个」; 追加第三条: 「场景 4b 只能当地板守卫: 对真实措辞改动在饱和套件上零区分力 (RESULT.md v2 结论 1); 它验证的是触发面没被改坏。」

### Key Deliverables (每条带 D 锚)

- `CLAUDE.md` 规则 #6 表后句 (D1) + 指向 SOT §4 模板一句 (D4)
- `standards/conventions/skill-benchmark-exemption.md`: §2 末句 (D1) / §3 边界注 (D1) / §4 模板 (D4) / §6 第三条 + 计数语 (D6) / 文件头 Version 1.0.0 → 1.1.0
- `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md`: §场景 4 拆 4a/4b (D5.1), 4b 含 D2 判据 + D3 前置表; §「确定性代码层变更」边界与留痕句 (D1); §数据组织表加 `ab-suite/trigger/` 行 (D2)
- `aria-plugin-benchmarks/ab-suite/trigger/openspec-archive.json` (D2; 逐字节 = 基线 `trigger-eval-openspec-archive.json`) + `ab-suite/version.yaml` 升版
- 两张新 issue (D5.2, D5.3) + 上游反馈发出证据 (D5.4)

## Impact

- 影响的 AI 行为: Rule #6 执行者在 description 变动时的义务判断: 从「照跑场景 1 即合规」变为「场景 4b 地板守卫 + rule6_note 五字段」; 只改 description 时不再跑场景 1 (OQ-6)。
- 不影响任何 skill 运行时行为; aria-plugin 零改动 ⇒ 本 Spec 自身不触发 Rule #6。
- 破坏性: 无; 已 ship 的 rule6_note 不回溯。
- 成本 (估算, 来源 RESULT.md v2 §时长与成本): 一次场景 4b (被评 + 负控两臂) 约 120 次 `claude -p`, 并行约 12–14 分钟 / 串行约 24 分钟, 约 10 美元 (按探针单次 0.08 美元估, `run_eval.py` 不记录成本); 首次为某 skill 建 20 条套件另加约 1 小时。
- 对无套件 skill 的即时影响: 42/43 个 skill 的下一次 description 变动都要先建套件; 这是有意的 (Rule #6 零裁量), 成本已写明, 由 OQ-7 确认。

## Tasks

- [ ] T1 三处 D1 新句落地 (逐字), 旧句删除; SOT §3 边界注
- [ ] T2 手册 §场景 4 拆 4a/4b; 4b 写 D2 判据 + D3 六条前置表 (每条附机读实证路径); §数据组织表加 trigger 行
- [ ] T3 SOT §4 rule6_note 五字段模板 (D4); CLAUDE.md 加指向句
- [ ] T4 `ab-suite/trigger/openspec-archive.json` 搬入 (逐字节同基线) + `ab-suite/version.yaml` 升版
- [ ] T5 SOT §6 第三条 + 计数语 (D6); SOT 文件头 Version 1.1.0
- [ ] T6 开两张 issue (D5.2 / D5.3); 上游反馈发出并把证据记入 `10CG/Aria#211` (D5.4)
- [ ] T7 合并前查 `10CG/aria-standards#17` 并行编辑 (D5.5); standards 本地 `--no-ff` merge → 双推 → **对 origin 与 github 各自 `git ls-remote` 比对 SHA, 全部一致才算推成功** → 主仓 gitlink bump → 主仓双推同样逐 remote 核验
- [ ] T8 `10CG/Aria#211` 回帖: 基线结论 (RESULT.md v2) + 落地位置; 关单归 owner

## Success Criteria

- SC-1: `grep -c "只验证触发面没被改坏, 不验证 description 改得更好"` 在 `CLAUDE.md`、SOT、手册三处各 ≥ 1 (逐字, 无同义替代)。
- SC-2: 手册 4b 前置表六行, 每行「机读实证」列给出的路径在基线目录里 `test -e` 为真 (第 4 行允许写「配置推导, 无对照实测」)。
- SC-3: SOT §4 含五个字段名 (`decision_table_row` / `description_changed` / `scenario1` / `scenario4b` / `negctrl`) 各 ≥ 1 次 (grep); 反事实: 现行 SOT 对五个名 grep 均为 0。
- SC-4: `diff aria-plugin-benchmarks/ab-suite/trigger/openspec-archive.json <基线 trigger-eval-openspec-archive.json>` 为空; `ab-suite/version.yaml` 版本号高于改前。
- SC-5: 三处 D1 落点 grep 「新版.*旧版」「≥ 旧版」「不低于旧版」均为 0 (不写比较判据)。
- SC-6: D5.2 / D5.3 两张 issue 存在且 open (`forgejo GET` 返回 200 + `state=open`); `10CG/Aria#211` 有一条含「上游反馈」与发出时间的评论。
- SC-7: SOT §6 `grep -c "三个已知缺陷"` = 1 且 `grep -c "两个已知缺陷"` = 0; SOT 头 `Version: 1.1.0`。
- SC-8: 手册含 `### 场景 4a` 与 `### 场景 4b` 两个标题各 1 次。

## Open Questions (owner 裁; 每项给推荐与代价)

- OQ-1 D2 阈值: 沿用 0.5 (= 2/3), 还是 0.8 (= 3/3)。**推荐 0.5**: 三个真 description 基线均 1.0, 0.8 也过; 但 0.8 会让偶发一次探索式开局 (v4 realroot 未见, 大仓未验) 判红, 误报代价高。代价: 0.5 门放过「2/3 才触发」的 description。
- OQ-2 D3 第 1 条: 等上游修 (a) 还是长期写「独立根 + 单 worker」。**推荐后者**, 上游修好后再放宽; 代价: 两臂并行需两个临时根, 手册步骤多两行。
- OQ-3 20 条 query 未经 owner 审阅: 接受为 trigger 套件 v1, 还是 owner 先审再 T4。**推荐先审** (skill-creator Step 2 要求); 代价: 若改动 query, 基线数字 (RESULT.md v2) 与套件 v1 脱节, 需重跑一臂约 12 分钟 / 5 美元。
- OQ-4 Level: 自判 2 (无代码, 5 个文本落点); LEVEL_GUIDE「跨模块 → Level 3」(本 Spec 跨主仓 + standards 子模块) 与「2-5 文件 → Level 2」拉扯。**推荐 Level 3 仅当 owner 要求 tasks.md 承载 T1–T8 的逐项验收**; 否则维持 2。代价: 升 3 多一份 tasks.md 与 post_planning 审计 (约 +1 小时)。
- OQ-5 **偏离 issue 验收第 2 条**: issue 原文「若两个 description 触发率统计无差别, 应改开『触发率评测本身不可用』的单而不是把它写进 Rule #6」。基线正命中 (p = 1.0)。本 Spec 的选择: **仍写进 Rule #6, 但只写成地板守卫** (理由: 负控与过宽两侧都有真实 FAIL 样本, 评测「不可用」的是 A/B 用途, 不是守卫用途)。**备选 (issue 字面)**: 不写进 Rule #6, 只开「评测不可用」单 + SOT §6 局限; 代价: description 维度继续零证据, 每次 description 改动照旧「照跑场景 1」生成空记录。请 owner 二选一。
- OQ-6 只改 description 时**不跑**场景 1 (D1): 对现行「一律照跑」的实质放宽; 备选「两者都跑」代价 = 每次多约 30 分钟 / 15 美元的空证据。
- OQ-7 无套件 skill 的即时成本 (Impact 末条): 确认「首次建套件」是接受的成本, 还是要一条过渡 lane (如: 42 个 skill 在套件补齐前, description 变动由 owner 逐次签字放行)。**推荐无过渡 lane** (Rule #10 精神); 代价: 每个首次改 description 的 cycle 多约 1 小时。

## rule6_note

```yaml
rule6_note:
  decision_table_row: n/a       # 本 Spec 改的是规范 / 手册 / 套件数据, 无 SKILL.md、无 references/、无 description 变动, 不属决策表任一行的「Skill 变更」
  description_changed: no
  scenario1: n/a
  scenario4b: n/a
  negctrl: n/a
```

基线实跑本身依 Rule #6「跑 benchmark 本身不需要 OpenSpec」在起草前完成; 20 条 query 未经 owner 审阅 (OQ-3) 与「基线先于 spec」两项 AI 流程判断记入本 session handoff。

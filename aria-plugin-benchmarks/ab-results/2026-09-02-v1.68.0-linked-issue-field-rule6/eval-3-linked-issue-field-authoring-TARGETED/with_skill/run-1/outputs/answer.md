已按 spec-drafter 流程 (A.1.0 → A.1.6) 起草完毕。eval 模式下不写仓库、不跑 git / openspec / 任何脚本, proposal.md 全文在下方。

## 流程结果

- **A.1.0 头脑风暴检查**: `docs/decisions/` 下无 `technical-*` 决策记录 → 应询问「先 brainstorm / 直接创建 / 取消」; eval 模式不询问, 取 [2] 直接创建 OpenSpec, 已在 proposal §起草说明 留痕。
- **A.1.1 需求信息**: 实读源码后发现**配置级** `state_scanner.issue_scan.label_filter` 已存在 (`collectors/issue_scan.py:533-538`, fetch 时过滤、结果入缓存、🎫 区块不显示过滤状态)。所以「可选参数」的诚实范围是**运行时** `scan.py --issue-label` (可重复), 在缓存 / 实时两路之后过滤, 并把过滤状态显式写进 snapshot 与 🎫 区块。
- **A.1.2 Level 判断**: 关键词「加 / 可选参数 / 过滤」= 功能开发词; 单模块 (`aria/` 子模块 state-scanner Skill); 无架构 / 跨模块 / breaking (新字段全部 additive, 无 flag 路径字节级不变) → **Level 2**。触碰文件约 11 个超过模板「2-5 文件」提示, 但 7 处是单行文档同步 + 发版机械面, 核心 2 代码 + 2 测试, 未升 Level 3; 理由已写进 proposal 供覆盖。
- **A.1.3 模块**: `aria-plugin` (state-scanner Skill; 按 SKILL.md 分类属 standards 类)。
- **A.1.4 位置**: `openspec/changes/state-scanner-issue-label-filter-arg/proposal.md` (CLAUDE.md Rule #5: 项目变更放本项目 `openspec/changes/`; spec-drafter SKILL.md A.1.4 / LEVEL_GUIDE 仍写 `standards/openspec/changes/`, 这是 Skill 文档漂移, 以 Rule #5 为准)。
- **Linked Issue**: 任务已核实无关联 issue → 头部逐字写 `` `none` `` (不留空、不删行), 与 `standards/openspec/templates/proposal-minimal.md` 头部四行顺序对齐。

两个影响设计的源码事实: `open_blocker_issues` 推荐规则 (`RECOMMENDATION_RULES.md` 优先级 1.99) 读的是 `issue_status.items[]`, 所以过滤视图必须是**追加**的 `label_filter` 对象、`items[]` 保持全集, 否则用户一过滤就把 blocker 降级提示过滤掉了; additive 字段不 bump `snapshot_schema_version` (`scan.py:294`)。

```
╔══════════════════════════════════════════════════════════╗
║           SPEC DRAFT PREVIEW (Level 2)                   ║
╚══════════════════════════════════════════════════════════╝

Feature: state-scanner-issue-label-filter-arg
Module: aria-plugin (state-scanner Skill)
Location: openspec/changes/state-scanner-issue-label-filter-arg/proposal.md
```

## proposal.md 全文

````markdown
# state-scanner Open Issues 区块 label 过滤可选参数

> **Level**: Minimal (Level 2 Spec)
> **Status**: Draft
> **Created**: 2026-09-02
> **Linked Issue**: `none`
> **Target Version**: aria-plugin v1.68.0 (MINOR — 既有 Skill 新增运行时参数 + snapshot additive 字段; 档位按 `standards/conventions/version-management.md` 复核)
> **代码落点**: `aria/` 子模块 `skills/state-scanner/` (`scripts/scan.py` + `scripts/collectors/issue_scan.py` + 3 份 `references/*.md` + `SKILL.md` + `RECOMMENDATION_RULES.md` + 2 份 `tests/`); Rule #6 定向 fixture 落 `aria-plugin-benchmarks/ab-suite/state-scanner.json`; Spec 落主仓 `openspec/changes/` (Rule #5)
> **决策来源**: 无 (`docs/decisions/` 下无 `technical-*` 决策记录; A.1.0 取「直接创建 OpenSpec」, 见 §起草说明)

## Why

state-scanner 的 🎫 Open Issues 区块 (Phase 1.13, opt-in) 目前只有一个**配置级**标签过滤: `state_scanner.issue_scan.label_filter` (`.aria/config.json`, 默认 `[]`; `collectors/issue_scan.py:533-538` 在 `_fetch_repo` 拉取时做客户端交集过滤)。它有三个使用上的问题:

1. **粒度错位**: 它是项目共享配置, 改一次影响所有人、所有次扫描; 而「这次只看 `bug` / 只看 `blocker`」是单次调用的诉求。
2. **与缓存耦合**: 过滤发生在 fetch 时, 写进 `.aria/cache/issues.json` 的已经是过滤后的 items; 改配置后 TTL (15m) 内的缓存命中仍返回旧过滤结果, 用户看不出来。
3. **无可见性**: 过滤生效时 🎫 区块不显示「正在过滤」, `open_count` 直接变小, 读者无法区分「项目只有 3 个 open」与「过滤后剩 3 个」。

本 Spec 给 `scan.py` 加一个**运行时**可选参数 `--issue-label`, 在缓存 / 实时两条路径之后做过滤, 并在 snapshot 与 🎫 区块里显式标出过滤状态; **不改** `label_filter` 配置的既有语义。

## What

### 1. CLI 面 (`scripts/scan.py`)

- 新增 `--issue-label LABEL` (`action="append"`, 可重复, 默认 `None`)。**不支持**逗号分隔 (GitHub / Forgejo label 名可含逗号)。
- 归一 (钉死, 实现零裁量): 每个值 `str.strip()`; 丢弃空串; 去重保序。**不做**大小写折叠。
- 传参: `build_snapshot(project_root, *, issue_label_filter=None)` → `collect_issue_scan(project_root, *, label_filter_arg=None)`, 均为 keyword-only 追加参数; 既有调用点 (含 tests) 不改一字。
- `issue_scan.enabled=false` 且给了 flag: stderr 打一条 WARNING, 逐字含 token `--issue-label ignored (issue_scan.enabled=false)`; snapshot 与退出码同无 flag 时。**不静默吞掉**。

### 2. 过滤位置与语义 (`scripts/collectors/issue_scan.py`)

- **位置**: 聚合出 `flat_items` 之后、`r.data` 赋值之前 (现 `issue_scan.py:761` 一带, `open_count = len(flat_items)` 之后), 即缓存命中与 live fetch **两条路径共用**同一处过滤。缓存回写 payload **不变** (仍写未过滤全集)。
- **匹配**: item 的 `labels` 与参数集合**交集非空**即命中 (OR 语义), 精确字串、大小写敏感 —— 与配置级 `label_filter` 现行判据 (`wanted.intersection(...)`) 同一套, 不引入第二种语义。
- **组合**: 配置级 `label_filter` 仍在 fetch 时先作用; 运行时参数在其结果上再过滤 (构造上即 AND)。

### 3. Snapshot 字段 (additive, 不 bump `snapshot_schema_version`)

**既有字段一律不动**: `items[]` / `open_issues[]` / `repos[*].items[]` / `open_count` / `label_summary` 保持**未过滤**全集 —— `open_blocker_issues` 规则 (`RECOMMENDATION_RULES.md` 优先级 1.99, 遍历 `issue_status.items[]`) 与 v1.0 消费者读到的还是原来的东西。

仅当传入 ≥1 个 `--issue-label` 时, `issue_status` 追加一个 key:

```yaml
label_filter:
  labels: ["bug", "blocker"]        # 归一后的运行时参数, 保序
  config_labels: []                 # 回显配置级 label_filter, 让 0 结果可解释
  open_count: 1                     # 过滤后条数
  items: [...]                      # 过滤后 IssueItem 列表 (每项保留 repo 字段), 结构同 items[]
```

未传 flag 时**不出现**此 key —— 无 flag 路径的 `issue_status` 与改动前逐字节一致。

### 4. 🎫 区块渲染 (`references/output-formats.md` §Open Issues 新增两变体)

- **变体 6 过滤生效**: 标题行改为 `— 1 / 12 open (过滤: label ∈ {bug, blocker})`, 列 `label_filter.items`; 末行加 `推荐规则按全部 12 open 评估`; `config_labels` 非空时另加一行 `config label_filter 生效中: [...]`。
- **变体 7 过滤零匹配**: `无匹配 label ∈ {x} 的 open issue (共 12 open; 可用 label: bug(1) enhancement(4) ...)` —— 可用 label 取自未过滤的 `label_summary`。
- 区块头 `🎫 Open Issues` 字面**不变** (`tests/test_output_format_sync.py` 的 canonical 集合不动)。

### 5. AI 侧指令 (`SKILL.md`)

- 「输入参数」表加一行 `issue_label` (可选): 用户意图中**显式点名** label 时, Step 0 命令按每个 label 追加一个 `--issue-label`; 未点名**不猜**、不加。
- 「输出格式」清单第 9 条补「过滤生效时显示 N / M + 过滤条件」。

### Framework Constraints

不适用 (stdlib-only Python 脚本, 无 web framework)。

### Key Deliverables

- `aria/skills/state-scanner/scripts/scan.py` — `--issue-label` flag + keyword-only 传参 + `enabled=false` WARNING
- `aria/skills/state-scanner/scripts/collectors/issue_scan.py` — `label_filter_arg` 后置过滤 + `issue_status.label_filter` 字段; 缓存 payload 不变
- `aria/skills/state-scanner/tests/test_issue_scan_mocked.py` + `tests/test_scan_integration.py` — 新增用例 (对应 Success Criteria; TDD 先红)
- `aria/skills/state-scanner/references/state-snapshot-schema.md` (`label_filter` 字段) / `references/output-formats.md` (变体 6 / 7) / `references/issue-scanning.md` (`label_filter` 配置行补「fetch 时作用、入缓存」+ 运行时过滤小节)
- `aria/skills/state-scanner/SKILL.md` (输入参数行 + 输出格式第 9 条) / `RECOMMENDATION_RULES.md` (变更历史: `open_blocker_issues` 输入为未过滤 `items[]`, 不受本参数影响)
- `aria-plugin-benchmarks/ab-suite/state-scanner.json` — eval-13 定向 fixture (Rule #6, 见下)
- `aria/CHANGELOG.md` + 版本 5 文件同步面 (v1.68.0)

## Impact

| Type | Description |
|------|-------------|
| **Positive** | 单次调用即可聚焦某类 issue, 不动共享配置; 缓存命中同样生效; 无 flag 时所有既有消费者 (推荐规则 / v1.0 alias / 缓存) 逐字节不变 |
| **Risk** | (a) 用户过滤后仍见 blocker 降级推荐而困惑 → 变体 6 末行明示「推荐按全部 M open 评估」; (b) 配置级过滤叠加导致「明明有却 0 条」→ 回显 `config_labels`; (c) AI 从模糊意图乱猜 label → SKILL.md 钉「仅显式点名」, eval-13 含反例; (d) `enabled=false` 时静默无效 → stderr WARNING; (e) A.0 撞车检查本次未跑 (起草在 eval 模式, 禁 git) → Tasks 首项补做 |

## Tasks

- [ ] A.0 补做: fetch 后核对无 in-flight 分支触碰 `scan.py` / `issue_scan.py` (本 Spec 起草时未跑 git)
- [ ] TDD RED: 先落 SC-1 ~ SC-7 对应测试, 全部先红
- [ ] 实现 `scan.py` `--issue-label` + 传参 + `enabled=false` WARNING
- [ ] 实现 `issue_scan.py` 后置过滤 + `label_filter` 字段, 缓存 payload 不变
- [ ] 同步 5 份文档 (schema / output-formats / issue-scanning / SKILL.md / RECOMMENDATION_RULES)
- [ ] Rule #6: eval-13 定向 fixture + AB 照跑, 结果归档 `ab-results/`
- [ ] CHANGELOG + v1.68.0 5 文件同步面

## Success Criteria

每条必答「它怎么会红」; SC-2 / SC-3 / SC-5 / SC-7 另须对两个坏实现验红: **bad-1** 只在 `_fetch_repo` 过滤 (缓存命中路径漏过) → SC-2 红; **bad-2** 原地改 `items` → SC-2 / SC-7 红。

- [ ] SC-1 无 flag 逐字节一致: 用 `tests/fixtures/reference-snapshot-aria.json` 同源 fixture + `ARIA_SCAN_OFFLINE=1`, 无 `--issue-label` 产出的 `issue_status` 与改动前 golden `==`, 且无 `label_filter` key。红: 无 flag 路径多 / 改任何 key
- [ ] SC-2 缓存命中也过滤: 热缓存 fixture (labels `[bug]` / `[enhancement, skill]` / `[feature]`), `--issue-label bug` → `label_filter.open_count == 1` 且 `label_filter.items` 恰为 bug 项; 同时 `open_count == 3`、`len(items) == 3`。红: 过滤漏掉缓存路径, 或误改 `items`
- [ ] SC-3 OR + 精确 + 大小写敏感: `--issue-label bug --issue-label skill` → 2 项; `--issue-label Bug` → 0 项。红: AND 语义或大小写折叠
- [ ] SC-4 零匹配形状: `--issue-label nonexistent` → `label_filter == {"labels": ["nonexistent"], "config_labels": [], "open_count": 0, "items": []}`, 退出码与 soft_error 列表同无 flag。红: 缺 key 或抛错
- [ ] SC-5 缓存不带过滤: live fetch + `--issue-label bug` 后, `.aria/cache/issues.json` 的 `items` 长度 == 未过滤数, 且无 `label_filter` key。红: 过滤集被持久化
- [ ] SC-6 `enabled=false` 不静默: `--issue-label bug` + `enabled=false` → stderr 含逐字 token `--issue-label ignored (issue_scan.enabled=false)`, snapshot 无 `issue_status`, 退出码同无 flag。红: 静默
- [ ] SC-7 规则输入不受影响: fixture 含 `blocker` label 项, `--issue-label enhancement` → `items` 仍含该 blocker 项 (规则本体是 AI 按 prose 评估、无代码宿主, 故只断言它读的输入 `items[]` 未被过滤)
- [ ] SC-8 文档结构: `test_output_format_sync.py` 绿 (区块头不变); grep 断言 `output-formats.md` §Open Issues 下存在「变体 6」「变体 7」两小节, `state-snapshot-schema.md` 存在 `label_filter` 字段行
- [ ] SC-9 Rule #6: eval-13 with_skill 在点名 label 的 prompt 下 Step 0 命令含 `--issue-label <该 label>`, 在未点名的反例 prompt 下不含; 两例 with_skill ≥ without_skill; 归档 `ab-results/`
- [ ] SC-10 `python3 tests/run_tests.py` 全绿; `collectors/issue_scan.py` 覆盖率不低于改动前

## Rule #6 判定 (rule6_note)

`description` 不变; 但 SKILL.md Step 0 指令流程新增条件分支 (点名 label → 追加 flag) 属**处方性 · 运行时指令面**, 且现有 AB 套件 eval-7 (`issue-awareness-opt-in-new`) 的 prompt 不含 label 过滤, 该行为在**套件覆盖外** → 按 `standards/conventions/skill-benchmark-exemption.md` 表第三行处置: 点名行为 (SC-9) + 建可证伪定向 fixture (eval-13, 含正反两例) + 套件缺口一并记在 eval-13 备注; **不豁免, 照跑 AB**。`output-formats.md` / `state-snapshot-schema.md` / 参数表三处为描述性 → SC-8 结构化测试替代。

## 起草说明

- A.1.0: `docs/decisions/` 无 `technical-*` 记录, 取选项 [2] 直接创建 OpenSpec (eval 模式不询问)。本文技术方案未经 brainstorm.technical; §3 「既有字段不动 + 追加 `label_filter` 对象」是主控的技术级选择 (替代方案: 直接过滤 `items` 并另存全集 —— 会改所有既有消费者的输入, 故弃), 若 owner 要比较可回补决策记录。
- Level 判定: 关键词「加 / 可选参数 / 过滤」→ Level 2 功能开发词; 单模块 (`aria/` 子模块 state-scanner Skill); 无架构 / 跨模块 / breaking (所有新字段 additive, 无 flag 路径字节级不变)。触碰文件约 11 个, 超模板「2-5 文件」提示, 但其中 7 处为单行文档同步与发版机械面, 核心为 2 代码 + 2 测试; 未升 Level 3。理由列此供覆盖。
- 本文件只规定「要建什么」; 实现时若发现 `issue_scan.py:761` 一带的聚合顺序与本文描述不符, 以源码为准并回写本文 (Rule #3)。
````

## 未做 / 待做

- **未创建文件** (eval 模式): 「Create this file? [Yes/No/Edit]」这一步没有落盘, 上面即为将写入 `openspec/changes/state-scanner-issue-label-filter-arg/proposal.md` 的全文。
- **A.1.6 验证提示**: 落盘后建议运行 `openspec validate state-scanner-issue-label-filter-arg --strict` 验证格式 (本次未运行)。
- **A.0 撞车检查未跑** (禁 git): 进 B.1 前先 fetch 并核对是否有 in-flight 分支已触碰 `scan.py` / `issue_scan.py`; 已列为 Tasks 首项。
- **Rule #6**: `description` 不变, 但 SKILL.md Step 0 新增「点名 label → 追加 flag」条件分支属运行时指令面, 且 AB 套件 eval-7 不覆盖 label 过滤 → 不豁免, 建 eval-13 定向 fixture (正反两例) 并照跑 AB; 详见 proposal §Rule #6 判定。
- **spec-drafter 文档漂移 (供 Skill 维护者)**: SKILL.md A.1.4 与 LEVEL_GUIDE.md 示例仍把 Level 2 产出路径写成 `standards/openspec/changes/{feature}/proposal.md`, 与 CLAUDE.md Rule #5 (`openspec/changes/`) 相反; 本次按 Rule #5 定位。

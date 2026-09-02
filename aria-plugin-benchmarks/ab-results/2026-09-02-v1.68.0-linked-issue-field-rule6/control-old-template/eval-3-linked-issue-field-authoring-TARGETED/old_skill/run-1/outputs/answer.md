# spec-drafter (A.1) — Level 2 proposal: state-scanner Open Issues 区块 label 过滤可选参数

按 spec-drafter 快照 SKILL.md 的执行流程走完 A.1.0 → A.1.6; 评测规则下不提问、不写仓库、不跑脚本, 每个原本要问的分叉点都直接取默认并在 proposal §流程判断 里留痕。

## A.1.0 头脑风暴检查

扫描 `docs/decisions/` (22 份决策单, `DEC-20260401-001` … `DEC-20260816-002`): 没有任何一份涉及 issue label 过滤或 Open Issues 区块 ⇒ 无可预填充的 technical decision-log。流程此处应给出 [1] 先头脑风暴 / [2] 直接创建 / [3] 取消 三选一; 本次取 [2] 直接创建 (评测运行禁止提问), 已写进 proposal §流程判断 第 1 条请复议。

## A.1.1 需求信息收集 (实读结论, 非转述)

- 需求: 给 state-scanner 的 `🎫 Open Issues` 区块加一个按 label 过滤的可选参数; 无关联 issue (起草输入已核实) ⇒ header 写 `Linked Issue: none`。
- 现状 (决定 Why 的关键事实): config 键 `state_scanner.issue_scan.label_filter` **已存在并已实现** (`.aria/config.template.json:51`, `collectors/issue_scan.py:533-538`, 测试 `test_issue_scan_mocked.py:290`), 但它是采集期静态过滤: 在缓存回写之前生效、缓存命中时不生效、会把 blocker 从 `items[]` 里滤掉 (`open_blocker_issues` 规则的输入)。所以本 Spec 的 delta = 「每次调用可选的临场参数」, 且必须落在视图层而不是复用现有过滤点。
- 交付物 / 约束 / 框架约定: 见 proposal 正文 (无 framework, 该段标「不适用」)。

## A.1.2 Level 判断

关键词「加 / 可选参数」= 功能扩展 (Level 2 触发词); 单模块 `aria/skills/state-scanner`; 约 8 个文件; additive 字段、无 breaking、无跨模块 ⇒ **Level 2 (Minimal)**, 与起草输入一致。

## A.1.3 模块检测

`standards` 类 (Skill 变更) → 在 Aria meta-repo 中对应 `aria/` 子模块 `skills/state-scanner/`; Spec 按 Rule #5 落主仓 `openspec/changes/` (快照 SKILL.md 写的 `standards/openspec/changes/` 路径已过时, 以 CLAUDE.md Rule #5 为准)。

## A.1.4 生成 Spec 文档 (Level 2 预览)

```
SPEC DRAFT PREVIEW (Level 2)

Feature:  state-scanner-issue-label-filter-param
Module:   aria/ 子模块 skills/state-scanner (代码) ; 主仓 openspec/changes/ (Spec, Rule #5)
Location: openspec/changes/state-scanner-issue-label-filter-param/proposal.md
```

proposal.md 全文如下 (与本次输出的 `proposal.md` 文件逐字节相同):

----- BEGIN proposal.md -----

# Proposal: state-scanner-issue-label-filter-param

> **Status**: Draft (A.1 起草 2026-09-02; 尚未经 post_spec 审计)
> **Created**: 2026-09-02
> **Spec Level**: 2 (Minimal — 单模块 `aria/skills/state-scanner`, 新增可选参数 + additive 字段, 无 breaking change; 与起草输入 `Level 2` 一致)
> **Linked Issue**: `none` — 起草输入已核实本功能无关联 issue; 本 Spec 不关闭任何 issue。§Out of scope 列出的两项后续候选 issue 尚未建号, 不在此处编号。
> **代码落点**: `aria/` 子模块 `skills/state-scanner/` (scripts + references + tests); Spec 落主仓 `openspec/changes/` (Rule #5)
> **版本影响**: aria-plugin MINOR (新增功能面: CLI 参数 + snapshot additive 字段)。ship target 待定 — `aria/.claude-plugin/plugin.json` 当前已是 `1.68.0` 而 `aria/CHANGELOG.md` 尚无该条目 (in-flight), 以 C.1 时 SOT 为准。
> **决策来源**: 无 (`docs/decisions/` 22 份决策单均不涉及 issue label 过滤; 见 §流程判断 第 1 条)

## Why

`/state-scanner` 的 `🎫 Open Issues` 区块 (Phase 1.13, opt-in) 今天只有一个**静态**过滤手段: `.aria/config.json` 的 `state_scanner.issue_scan.label_filter` (默认 `[]`; 文档 `references/issue-scanning.md` §配置项; 实现 `scripts/collectors/issue_scan.py:533-538`; 测试 `tests/test_issue_scan_mocked.py:290 test_label_filter_applied`)。它是「每次扫描都生效」的配置, 不是「这一次只想看 bug」的临场参数。Aria 主仓当前 `label_filter: []` 且 `scan_submodules: true`, 一次扫描聚合主仓 + 3 个 submodule, 上限 4 × `limit: 20` = 80 条; 想只看 `blocker` / `bug` 只能改 config 再改回来。

本 Spec 补的是**每次调用可选的 label 过滤参数**。它不是把现有 config 键换个入口 —— 实读代码发现, 现有 `label_filter` 的实现位置 (fetch 时、进缓存之前) 对「临场参数」是错误的位置。三个可核对的事实:

1. **过滤发生在缓存回写之前**: `_fetch_repo` 返回的已过滤 `items` 直接进入 `repos[...]` (主 repo `:667-680`, submodule `:735-750`), 再原样进入 `.aria/cache/issues.json` (`:803-817`)。若临场参数走这条路, 一次 `--issue-label bug` 会把**收窄后**的列表写进共享缓存, 之后 `cache_ttl_seconds` (900s) 内所有不带参数的扫描 (含其他终端) 都只看到 bug —— 无人报警。
2. **缓存命中路径根本不经过过滤点**: 主 repo (`:654-657`) 与 submodule (`:722-726`) 命中缓存时直接采用 `cached_entry`, 不调 `_fetch_repo`。同一参数在 TTL 内「时而生效时而不生效」。
3. **推荐规则以 `items[]` 为输入**: `open_blocker_issues` (`RECOMMENDATION_RULES.md:27`, `:96`) 遍历 `issue_status.items[]` 找 `blocker` / `critical`。过滤 `items` 本身 = 用户临场只看 `doc` 时, blocker 降级提示静默消失。

因此临场参数必须是**视图层**的过滤: 采集面 (`items` / `repos` / `open_count` / `label_summary` / 缓存) 一字节不变, 只在 snapshot 里多一个 additive 的 `label_view`, 由渲染层消费。

## What

### 1. 参数面

- `scripts/scan.py` 新增 `--issue-label <name>` (可重复; 大小写敏感精确匹配, 不做归一化)。多次给出 → 去重保序。未给出 → 内部值为 `None` (不是 `[]`), 使「没传」与「传了空」可辨。
- `build_snapshot(project_root, *, issue_labels: list[str] | None = None)` 与 `collect_issue_scan(project_root, *, label_view: list[str] | None = None)` 各加一个 **keyword-only** 参数 (沿用 v1.67.2 `no_push` 的签名兼容手法), 现有调用方零改动。
- state-scanner `SKILL.md` §输入参数 表加一行 `issue_labels` (可选; 说明: 只影响 `🎫 Open Issues` 区块展示与 `label_view`, 不影响推荐规则输入); §Step 0 命令块标注可选 flag。

### 2. 视图层 (`collectors/issue_scan.py`)

在 `issue_status` 组装 (`:777-791`) 之后、缓存回写 (`:803`) 之前, **仅当** `label_view is not None` 时追加:

```yaml
issue_status:
  label_view:                      # 仅传参时出现; 缺席 = 未传参 (读取端用 `in`, 不用 .get, 同 schema.md:42 规则)
    labels: ["bug"]                # 请求的 label, 去重保序
    match: "any"                   # 本版固定: item.labels 与 labels 交集非空即命中 (与现有 label_filter :536-538 语义一致)
    config_filter: []              # 回显当前生效的 config label_filter (空 = 无), 供渲染层提示「宇宙已被 config 先行收窄」
    items: [...]                   # items[] 的子集 (同一批 dict 对象), 保持 items[] 顺序
    count: 1
    hidden_count: 2                # open_count - count
```

不变量 (SC-4 机械断言): 传参与不传参两次扫描, 在同一份 mock 数据下 `items` / `open_issues` / `repos` / `open_count` / `label_summary` 深度相等, 缓存 payload 深度相等; `label_view` 是唯一差异。

边界:

- `issue_scan.enabled=false` 且传了参数 → `issue_status` 照旧缺席, 同时 `errors[]` 追加 soft error `{code: "label_view_unavailable", detail: "issue_scan.enabled=false"}` (退出码走既有 10 契约)。不静默吞掉 —— 「有记录 ≠ 有路由」。
- `fetch_error != null` (source unavailable) → `label_view` 仍发出 (`count: 0, hidden_count: 0`), 渲染层按既有错误变体优先, 不显示「0 匹配」。
- `config_filter` 非空且与请求 label 无交集时结果必然为 0, 渲染层用 `config_filter` 给出提示; 本 Spec **不改** config `label_filter` 的既有位置与语义 (见 §Out of scope)。

### 3. 渲染面 (AI 侧, 描述文档)

- `references/output-formats.md` §Open Issues 加两个变体: 「变体 6: label 过滤激活」(标题行追加 `· 过滤 label=[bug] → 1 匹配 (2 隐藏)`, 列表只列 `label_view.items`, 数据来源行不变) 与「变体 7: 过滤后零匹配」(含 `config_filter` 提示)。
- `SKILL.md:204` 骨架第 9 条追加 `/ label 过滤 (label_view, 仅传参时)`; canonical 区块名与「10 个区块」计数不变 (`tests/test_output_format_sync.py` 继续通过)。
- `references/state-snapshot-schema.md` §`issue_status` 与 `references/issue-scanning.md` §输出 Schema / §配置项 同步 `label_view` 定义, 并在 §配置项 `label_filter` 行旁加一句「config 键 = 采集期静态过滤 (会进缓存); `--issue-label` = 视图层临场过滤 (不进缓存)」。

### Key Deliverables

- `aria/skills/state-scanner/scripts/scan.py` — `--issue-label` + keyword-only 穿参
- `aria/skills/state-scanner/scripts/collectors/issue_scan.py` — `label_view` 视图层 + `label_view_unavailable` soft error
- `aria/skills/state-scanner/tests/test_issue_label_view.py` (新) — SC-1~SC-9 结构化测试 (TDD RED 先行)
- `aria/skills/state-scanner/SKILL.md` / `references/output-formats.md` / `references/state-snapshot-schema.md` / `references/issue-scanning.md` — 四处文档同步
- `.aria/config.template.json` **不改** (无新 config 键)
- `aria-plugin-benchmarks/ab-suite/state-scanner.json` — 新增定向 eval case (见 rule6_note), 套件版本号 bump

### 框架约定

不适用 —— stdlib-only Python 脚本 + Markdown 参考文档, 无 framework。

## Impact

| Type | Description |
|------|-------------|
| **Positive** | 临场缩窄 Open Issues 视图, 不必改 config; 采集面与缓存不变, 对并发终端 / 后续扫描零副作用; `open_blocker_issues` 输入不变, 过滤不会藏掉 blocker |
| **Risk** | 实现者把过滤「顺手」放进 `_fetch_repo` (现有 config 键就在那里, 最省事) —— 正是 §Why 三条缺陷。缓解: SC-4 不变量测试 + B.2 一次性负控 (把 label 传进 `_fetch_repo` 的坏实现必须让 SC-4 变红, 记录在测试 docstring) |
| **Risk** | 嵌套字段漂移: `scripts/validate_schema_doc.py` 明写只查顶层键 (docstring `:17-22`), `label_view` 未入文档它不会红。缓解: SC-9 文档 drift 测试 |
| **Compat** | snapshot `snapshot_schema_version` 维持 `"1.0"` (additive-only, SKILL.md §Step 0); 缓存 `schema_version` 维持 `"1.1"`, 缓存 payload 无 `label_view`; 公共函数签名向后兼容; 现有测试零修改 |
| **Rule #6** | 见 §rule6_note —— SKILL.md 指令面 + output-formats 渲染变体属处方性且 AB 套件覆盖该区块, 照跑; 新参数行为本身是套件缺口, 补定向 fixture + 开 issue |

## Tasks

- [ ] 1. CLI 与穿参: `scan.py --issue-label` (可重复, 去重保序, 缺省 `None`); `build_snapshot` / `collect_issue_scan` keyword-only 参数
- [ ] 2. 视图层: `issue_status.label_view` (仅传参时), `label_view_unavailable` soft error; 采集面与缓存 payload 不动
- [ ] 3. 测试 (RED 先行): `tests/test_issue_label_view.py` 覆盖 SC-1~SC-9; 执行并记录 SC-4 负控
- [ ] 4. 文档四处同步 (SKILL.md 参数表 + Step 0 flag + 骨架第 9 条 + 版本脚注; output-formats 变体 6/7; schema.md; issue-scanning.md 两节)
- [ ] 5. Rule #6: state-scanner 套件 AB 照跑 (`ARIA_COORDINATION_NO_PUSH=1`) + ab-suite 新增定向 case (版本 bump) + 套件缺口 issue
- [ ] 6. CHANGELOG 条目 + 版本同步面 (进入 Phase C/D 时按 CLAUDE.md §版本管理执行)

## Success Criteria

每条写「怎么会红」。

- [ ] **SC-1 CLI 解析**: `_parse_args(["--issue-label","bug","--issue-label","doc","--issue-label","bug"])` → `["bug","doc"]`; 无 flag → `None`。红: 缺省为 `[]`、或重复未去重、或顺序被 set 打乱。
- [ ] **SC-2 存在性语义**: 传参 → `"label_view" in issue_status`; 不传 → `"label_view" not in issue_status` (断言 `not in`, 非 falsy)。红: 不传时发出 `label_view: null` / `{}`。
- [ ] **SC-3 any-of 语义与顺序**: fixture 三条 item, labels 依次 `[bug]` / `[doc]` / `[bug, doc]`; `labels=["bug"]` → `count 2, hidden_count 1`, `items` 为第 1、3 条且顺序不变; `labels=["nope"]` → `count 0, hidden_count 3`。红: 交集判成子集、或顺序按 label 重排。
- [ ] **SC-4 采集面不变量 (承重)**: 同一 mock 抓取, 传参 vs 不传参: `items` / `open_issues` / `repos` / `open_count` / `label_summary` 深度相等; `_write_cache_atomic` 收到的 payload 深度相等且不含 `label_view`。**负控** (B.2 执行一次, docstring 留证): monkeypatch 使 labels 进入 `_fetch_repo` 的坏实现 → 本测试红。红: 任一采集面字段随参数变化。
- [ ] **SC-5 缓存命中也生效**: 预置 fresh 缓存 (无 live fetch), 传参 → `label_view.count` 由缓存 `items` 算出且与 SC-3 一致。红: 视图只在 live 路径计算 (即 fetch 时过滤的形状)。
- [ ] **SC-6 blocker 输入不受影响**: fixture 含一条 `labels=["blocker"]`, 传 `labels=["doc"]` → `issue_status.items[]` 仍含该 blocker 条目。红: 过滤触及 `items`。(规则本体是 AI 侧 prose, 其行为面由 rule6_note 的定向 fixture 覆盖; 此处只钉数据输入。)
- [ ] **SC-7 disabled 不静默**: `issue_scan.enabled=false` + 传参 → snapshot 无 `issue_status` 且 `errors[]` 含 `code == "label_view_unavailable"`, `main()` 返回 10。红: 返回 0 且 `errors[]` 无该条。
- [ ] **SC-8 config 回显**: config `label_filter=["bug"]` + 传 `["doc"]` → `label_view.config_filter == ["bug"]`, `count == 0`。红: 回显缺失或为 `None`。
- [ ] **SC-9 文档 drift 守卫**: 测试读 `references/state-snapshot-schema.md` §`issue_status` 段与 `references/issue-scanning.md` §输出 Schema 段, 均须含字面 `label_view`; `tests/test_output_format_sync.py` 全绿 (区块数仍 10)。红: 任一文档漏写。
- [ ] **SC-10 回归零修改**: `tests/test_issue_scan_mocked.py` / `test_issue_scan_helpers.py` / `test_scan_integration.py` 不做任何编辑而全绿; `tests/run_tests.py` 全绿。红: 需要改旧测试才能过 (签名兼容被破坏)。
- [ ] **SC-11 Rule #6 闭环**: (a) state-scanner 套件 old / new 两臂结果存档; (b) `ab-suite/state-scanner.json` 新增 case, `ab-suite/version.yaml` bump; (c) 套件缺口 issue 号写回本 Spec。红: 三项任一缺失。

## rule6_note

逐 hunk 判 (判据: 是否影响 AI 行为 + AB 套件测不测得到):

| hunk | 性质 | 套件 | 处置 |
|------|------|------|------|
| `scan.py` / `issue_scan.py` / 新测试 | 代码, 非 SKILL 指令面 | 不适用 | baseline-failing 结构化测试 (SC-1~SC-10; RED 先行) |
| `SKILL.md` §Step 0 命令块加可选 flag; §输入参数 新行; `:204` 骨架第 9 条 | 处方性 · 运行时指令面 (改变 AI 执行的命令与排版骨架) | `ab-suite/state-scanner.json` v1.2.0 case 7 `issue-awareness-opt-in-new` 覆盖 Open Issues 区块存在性 + `open_blocker_issues` 推荐 | **照跑 AB, 零裁量** |
| `output-formats.md` 变体 6/7 | 处方性 (AI 据此渲染) | 同上 case 7 覆盖区块, **不覆盖**「传参后只列 `label_view.items` 且 blocker 推荐仍出现」 | 照跑 + **点名行为** (前句) + **定向 fixture** (ab-suite 新 case: config enabled + 传 `issue_labels=["doc"]` + mock 数据含 blocker; 断言: 列表只含 doc 条目、标题行含「隐藏」、仍出现 triage 推荐) + **套件缺口 issue** (缺一照跑) |
| `state-snapshot-schema.md` / `issue-scanning.md` | 描述性 (schema / 字段) | 不适用 | substitute = SC-9 drift 测试 |

运行前置: state-scanner 套件会触达 `phase1_gate.py` (`AB_TEST_OPERATIONS.md:224`), 须按 §场景 1 以 `ARIA_COORDINATION_NO_PUSH=1` 跑, 跑完 `git fetch origin +refs/aria/coordination:refs/aria/coordination` 强制对齐 (v1.67.2 已知残留)。

## Out of scope / 后续候选 issue (未建号)

1. **现有 config `label_filter` 的位置问题**: 它与 §Why 三条事实同形 —— 会把收窄后的列表写进共享缓存、缓存命中时不生效、会藏掉 blocker。本 Spec 不动它 (改一个已 ship 配置键的语义 = 用户可见行为变化, 属产品级取舍, 请 owner 裁: 迁到视图层 / 保留并只补文档警示)。建议开 issue 记录。
2. **服务端 `labels=` 查询**: 沿用 `:533-535` 注释的判断 (wrapper 不稳定 honor), 本版一律客户端过滤; 不引入 `match: all`。

## 流程判断 (AI 自作主张之处, 请复议 — Rule #10)

1. **A.1.0 未询问是否先 brainstorm**: `docs/decisions/` 22 份决策单无相关 technical decision-log, spec-drafter 流程应给出 [先头脑风暴 / 直接创建 / 取消] 三选一; 本次为评测运行 (禁止提问), 直接取 [2] 直接创建。若 owner 认为「视图层 vs 采集层」这一取舍值得一份决策单, 可补 `brainstorm.technical`。
2. **Level 2 未升 3**: 单模块、约 8 个文件、additive、无 breaking; 与起草输入一致。
3. **Spec 落点**: 按 CLAUDE.md Rule #5 落 `openspec/changes/`, 而非 spec-drafter 快照所写 `standards/openspec/changes/` (快照路径已过时)。
4. **版本档 MINOR**: 依据 CLAUDE.md 「新增功能 = MINOR+」; 若 owner 视其为 PATCH 级增量, 不影响本 Spec 内容。

---

**引用行号均为 2026-09-02 对 `aria/` 子模块工作树的实读, 合并前以实际文件为准。**

----- END proposal.md -----

## A.1.5 交互确认

`Create this file? [Yes/No/Edit]` —— 按评测规则**未执行**: 没有在仓库创建 `openspec/changes/state-scanner-issue-label-filter-param/proposal.md`, 全文只放在上方与输出目录的 `proposal.md`。

## A.1.6 验证提示

快照 SKILL.md 的提示是「建议运行 `openspec validate state-scanner-issue-label-filter-param --strict`」; 注意 `standards/openspec/project.md` §使用者行动指南 写明 Aria 项目内用 aria 格式 + `/audit-engine` 验证, 不装 npm CLI。本次两者都未运行 (评测规则)。落盘后的下一步是 post_spec 审计 (按 `.aria/config.json` 的 checkpoint 配置, 不由起草方裁量, Rule #10), 再进 A.2。

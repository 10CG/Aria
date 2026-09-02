已按 spec-drafter (A.1) 流程为「state-scanner 🎫 Open Issues 按 label 过滤的可选参数」起草 Level 2 proposal。评测规则下**未写入仓库、未运行 git 写命令 / openspec CLI / 任何脚本**, 全文在下方。

## A.1.0 – A.1.4 判定摘要

1. **A.1.0 决策记录检查**: `docs/decisions/` 下 21 份记录, 无与本功能对应的 `technical-*` decision-log。skill 流程此处会问「先 brainstorm / 直接创建 OpenSpec / 取消」; 评测禁止提问, 按选项 [2] 直接创建, 技术决策以 D1–D8 表内嵌进 proposal。
2. **A.1.2 Level 判断**: 关键词「加一个 … 可选参数」= add / 扩展 → Level 2 触发词; 影响范围单模块 (aria 子模块 `skills/state-scanner/`, 约 10 个文件, 无跨模块 / breaking / 架构变更) → 不升 Level 3; 有代码行为变更 + 缓存口径变更 + snapshot 新字段 → 不是 typo / 配置级, 不降 Level 1。**结论 Level 2, 与请求一致。**
3. **A.1.3 模块检测**: `aria-plugin` (`aria/skills/state-scanner`)。LEVEL_GUIDE 把 Skill 映射到 `standards` / `.claude/**` 是旧路径, Aria 仓的 Skill 实际在 `aria/` 子模块。
4. **A.1.4 落点**: `openspec/changes/state-scanner-issue-label-filter-param/proposal.md` (CLAUDE.md Rule #5: 项目变更放本项目 `openspec/changes/`; skill 快照 SKILL.md A.1.4 写的 `standards/openspec/changes/` 与 Rule #5 冲突, 以 Rule #5 为准)。slug 已查 `openspec/changes/` 与 `openspec/archive/` 无同名; 命名沿用 `state-scanner-*` 先例。
5. **Linked Issue 表头**: 按 `standards/openspec/templates/proposal-minimal.md` 的 Usage Notes 要求, 已核实无关联 issue 时逐字写 `` `none` `` (不留空、不删行, 不用 `N/A` / `TBD`)。

## 起草前实读到的三条关键事实 (决定了设计, 不是「加个 flag」)

1. `state_scanner.issue_scan.label_filter` 这个**配置级**过滤已经存在 (`issue_scan.py:533-538`, 任一 label 命中), 缺的是每次调用级参数 —— 所以参数设计成 `--issue-label` 覆写 config, 而不是新造一套过滤。
2. 过滤后的 `open_count` / `items` 在 snapshot 与 🎫 区块里**与未过滤不可区分**; label 拼错会显示成「无 open issue」。⇒ 加三个 additive 字段 + 🔍 / ⚠️ 两行显示。
3. 过滤发生在**缓存之前**, 缓存键只有 repo + TTL ⇒ 任何每次可变的过滤参数若沿用现有落点, TTL 内会拿到按上次条件过滤的结果。⇒ 承重决策 D3: 缓存存未过滤集合, 过滤搬到视图层。

```
╔══════════════════════════════════════════════════════════╗
║           SPEC DRAFT PREVIEW (Level 2)                   ║
╚══════════════════════════════════════════════════════════╝

Feature:  state-scanner-issue-label-filter-param
Module:   aria-plugin (aria/skills/state-scanner)
Location: openspec/changes/state-scanner-issue-label-filter-param/proposal.md
```

──────────────────────────────────────────────────────────── proposal.md 全文 (begin) ────────────────────────────────────────────────────────────

# state-scanner: 🎫 Open Issues 按 label 过滤的可选参数

> **Level**: Minimal (Level 2 Spec)
> **Status**: Draft
> **Created**: 2026-09-02
> **Linked Issue**: `none` — 已核实无关联 issue (任务给定; 起草时另扫 aria 子模块 `git log --all -i --grep=label` 与远端分支名, 无同题在飞轨)
> **代码落点**: `aria/` 子模块 `skills/state-scanner/` (collector + CLI + tests + 3 份 reference + SKILL.md 一行骨架); Spec 落主仓 `openspec/changes/state-scanner-issue-label-filter-param/` (Rule #5)
> **版本影响**: aria-plugin **MINOR** (SemVer: 向后兼容的新增功能; 当前 SOT `aria/.claude-plugin/plugin.json` = v1.67.2, 具体号由 C.2 按合并时 SOT 定)

## Why

state-scanner 阶段 1.13 的 🎫 Open Issues 区块今天只有一个**配置级**过滤入口: `.aria/config.json` → `state_scanner.issue_scan.label_filter` (`list[str]`, 默认 `[]`; 实现在 `scripts/collectors/issue_scan.py:533-538`, 集合交集 = 「任一 label 命中」)。它有三个实读到的问题, 使「我这次只想看 `bug` 的 issue」这个高频动作做不到或做错:

1. **没有每次调用级的参数**。`scripts/scan.py` 的 `_parse_args` 只有 `--project-root` / `--output` / `--log-level`; `collect_issue_scan(project_root)` 只收 `project_root` (`issue_scan.py:589`)。要换过滤条件必须改 config 文件再改回来 —— 对一个只读扫描器来说是错误的操作粒度。
2. **过滤对读者不可见**。snapshot 的 `issue_status` 没有回显生效的过滤条件 (`collect_issue_scan` 聚合段的 `issue_status` 字典键集合里没有它); `open_count` / `items` / `label_summary` 全是过滤后的值; `references/output-formats.md:715-790` 五个变体的表头都只写 `— 3 open`。⇒ 「过滤后 3 个」与「总共 3 个」在输出上不可区分 —— 与本 skill 上一轮 `state-scanner-stale-refs-false-parity` 治的是同一种病 (数据被静默收窄而显示口径不变)。零命中时更糟: 过滤 label 拼错 ⇒ 区块显示为「无 open issue」, 是一个假安心信号。
3. **过滤发生在缓存之前**。`_fetch_repo` 在返回前就把 items 过滤掉 (`issue_scan.py:536-538`), 而缓存写的正是这份已过滤的 `items[]` (cache payload 字典), 缓存键只有 repo + TTL (`_lookup_cached_repo`, `issue_scan.py:825`)。⇒ 任何「每次调用可变」的过滤参数, 只要天真地沿用现有落点, 在 TTL (默认 900s) 内第二次调用就会拿到**按上一次条件过滤**的 items 当结果。这是本 Spec 必须先解决的结构问题, 不是加个 flag 就完事。

## What

给 `scan.py` 加一个可重复的可选参数 `--issue-label LABEL`, 覆写本次运行的 label 过滤; 把过滤从「取数层」搬到「视图层」, 使缓存永远保存未过滤集合; 在 snapshot 中以三个 additive 字段回显生效的过滤, 并在 🎫 区块显示。

### §1 CLI 参数 (scan.py)

| 项 | 规定 |
|---|---|
| 形态 | `--issue-label LABEL`, `action="append"`, 默认 `None`; 多值靠**重复 flag** (`--issue-label bug --issue-label blocker`) |
| 值处理 | 每个值 `str.strip()`; strip 后为空 ⇒ `parser.error(...)` (argparse 原生 usage error, exit 2 —— 与今天 `--log-level bogus` 同一退出路径, 不进 0/10/20/30 契约); 去重, 保序; **不按逗号拆分** (label 名可含逗号) |
| 语义 | 「任一 label 命中」(OR), 精确、大小写敏感的字符串相等 —— 与现有 config `label_filter` 完全同义 (`set.intersection`) |
| 与 config 的关系 | **替换** (override), 不做交集: 给了 `--issue-label` 就以它为唯一生效过滤, 忽略 config `label_filter`; 没给则用 config。先例: `ARIA_FORGEJO_HOSTS` 对 `platform_hostnames.forgejo` 也是整体覆写 (`references/issue-scanning.md` 配置表 `platform_hostnames` 行) |
| `issue_scan.enabled=false` 时 | no-op: 区块照旧不出现, exit code 不变, 不写 `errors[]`; 仅 stderr `log.warning` 一条**固定文案** (不回显 label 值, Rule #7 typed-channel 纪律) |
| 穿线 | `build_snapshot(project_root, *, issue_label_filter: list[str] \| None = None)` → `collect_issue_scan(project_root, *, label_filter_override: list[str] \| None = None)`。均为 keyword-only additive, 现有调用点 (`tests/test_scan_integration.py` 5 处 `build_snapshot(repo)`, `TestCollectorEndToEnd`) 零改动 |

`label_filter_override` 的语义: `None` = 用 config; 任意 list (含 `[]`) = 原样作为生效过滤 (`[]` 即「本次不过滤」)。CLI 目前只产生 `None` 或非空 list; `[]` 是给未来 `--no-issue-label-filter` 之类留的 API 位, **本 Spec 不暴露它** (见非目标)。

### §2 过滤落点搬到视图层 (issue_scan.py) ⭐ 承重

- `_fetch_repo` **去掉** `label_filter` 形参, 只负责取数 + 归一; 新增纯函数 `_apply_label_filter(items: list[dict], label_filter: list[str]) -> list[dict]` (空 filter ⇒ 返回等值新 list; 否则保留 `labels` 与 filter 有交集的项)。
- **缓存写入的是未过滤集合**: `repos[key].items` / `open_count` / 顶层 `items` / `open_issues` / `label_summary` 在 cache payload 里一律未过滤。cache `schema_version` **保持 `"1.1"`** (字段集合不变, 只是内容口径变了, 见 D3 过渡说明)。
- **snapshot 里的每一个 issue 列表都是过滤后的视图**: 对每个 fetch 成功的 repo entry 做一次 `_apply_label_filter` 得到视图副本, 由它派生 `repos[*].items` / `repos[*].open_count` / 顶层 `items` (= `open_issues`, 仍是同一 list 对象) / `open_count` / `label_summary`。cache 命中路径与 live 路径**走同一段视图代码**, 不得各写一份 (memory `fix-recurs-in-fallback`)。
- 生效过滤解析: `effective = override if override is not None else list(cfg["label_filter"] or [])`; `source = "cli" if override is not None else ("config" if effective else None)`。

### §3 snapshot additive 字段 (`issue_status`)

| 字段 | 类型 | 规定 | 显示消费者 (每个字段必须有, memory「有记录 ≠ 有路由」) |
|---|---|---|---|
| `label_filter` | `list[str]` | 生效过滤, 无过滤时 `[]`; **无条件发出** (同 `warning` 字段的先例, 见 `state-snapshot-schema.md` §`issue_status`) | 🔍 行的条件 + 内容 |
| `label_filter_source` | `"cli" \| "config" \| null` | `null` 当且仅当 `label_filter == []` | 🔍 行「来源」 |
| `open_count_unfiltered` | `int` | 所有 fetch 成功 repo 过滤前 items 之和; 无过滤时恒等于 `open_count` | 🔍 行「过滤前 N open」 |

顶层 `snapshot_schema_version` 不 bump (additive-only 演进, SKILL.md 「Schema 版本契约」; 先例 `generated_at`, `scan.py:292-294`)。`scripts/validate_schema_doc.py` **不查嵌套键** (其 docstring 明示, 且 `issue_status.warning` 曾漏文档一个 PR 周期) ⇒ 三个字段的文档同步由本 Spec 新增单元测试断言 (SC-7)。

### §4 🎫 区块显示 (output-formats.md + SKILL.md:204)

仅当 `label_filter` 非空时, 在 issue 列表之后、`数据来源:` 之前插入一行 🔍; 零命中时再加一行 ⚠️。两份文档共用的字段 token 是 **`🔍 label 过滤`** (供 `tests/test_output_format_sync.py` 做双侧同步断言)。

变体 6 — 过滤生效, 有命中:

```
🎫 Open Issues
───────────────────────────────────────────────────────────────
  平台: Forgejo (10CG/Aria) — 2 open
  📌 #4  登录页面样式问题                                  [bug]
  📌 #9  release gate 在 detached HEAD 下误报              [bug, blocker]
  🔍 label 过滤: bug (来源: --issue-label) | 过滤前 12 open
  数据来源: live | 刚刚获取 | ttl: 15m
```

变体 7 — 过滤生效, 零命中:

```
🎫 Open Issues
───────────────────────────────────────────────────────────────
  平台: Forgejo (10CG/Aria) — 0 open
  🔍 label 过滤: releaes (来源: --issue-label) | 过滤前 12 open
  ⚠️ 过滤后为空 ≠ 无 open issue — 核对 label 拼写, 或去掉 --issue-label 重扫
  数据来源: cache (2m ago) | ttl: 15m
```

`来源:` 取值: `--issue-label` (source=`cli`) / `config label_filter` (source=`config`)。config 过滤生效时**同样显示 🔍 行** —— 这是对今天静默收窄的直接修复, 不只服务新 flag。

### Key Deliverables

- `aria/skills/state-scanner/scripts/scan.py` — `--issue-label` argparse + `build_snapshot(..., *, issue_label_filter=None)` 穿线
- `aria/skills/state-scanner/scripts/collectors/issue_scan.py` — `_apply_label_filter` 纯函数; `_fetch_repo` 去 `label_filter`; 缓存未过滤 / 视图过滤; 三个 additive 字段; disabled 时固定文案 warning
- `aria/skills/state-scanner/tests/test_issue_scan_mocked.py` — `test_label_filter_applied` **改指向** `_apply_label_filter` (非删除); `TestCollectorEndToEnd` 新增缓存口径 / 覆写 / 字段默认 / disabled no-op 用例
- `aria/skills/state-scanner/tests/test_scan_cli_issue_label.py` (新建) — argparse 三态 + 穿线断言
- `aria/skills/state-scanner/tests/test_output_format_sync.py` — 追加 `🔍 label 过滤` 双侧同步断言
- `aria/skills/state-scanner/tests/test_schema_doc_nested_fields.py` (新建, 或并入现有 schema 测试) — 断言 `state-snapshot-schema.md` 含三个新字段名
- `aria/skills/state-scanner/references/state-snapshot-schema.md` §`issue_status` — 三字段 + 「列表为过滤后视图, 缓存为未过滤」口径说明
- `aria/skills/state-scanner/references/issue-scanning.md` — `label_filter` 配置行加 CLI 覆写注; 新增小节「过滤生效层与缓存口径」
- `aria/skills/state-scanner/references/output-formats.md` §Open Issues — 变体 6 / 7
- `aria/skills/state-scanner/SKILL.md:204` — 骨架行追加 `🔍 label 过滤 (生效时: 条件 + 来源 + 过滤前总数)`

## 决策记录

| # | 决策 | 备选与否决理由 |
|---|---|---|
| D1 | 参数形态 = `scan.py` CLI flag, 不加 env var | env (`ARIA_ISSUE_LABEL_FILTER`) 有先例 (`ARIA_FORGEJO_HOSTS` / `ARIA_HANDOFF_MAX_BRANCHES`), 但需求是「一个可选参数」; env 是第二入口 = 第二套优先级规则要测要写。留作非目标, 有人要再加 |
| D2 | CLI **替换** config, 不交集 | 交集会让 config 排除掉的 label 永远看不到, 「临时看一眼」做不到; 且与 `ARIA_FORGEJO_HOSTS` 覆写语义一致 |
| D3 ⭐ | 缓存保存未过滤集合, 过滤在视图层 | 备选 (b)「给了 CLI 过滤就绕过缓存 / 不写缓存」: 每次带 flag 都付一次网络 + rate-limit, 且产生两套缓存策略。备选 (c)「过滤条件进缓存键」: 每个 label 组合一份缓存, 膨胀且互不复用。(a) 让 config / CLI / 无过滤三种调用共享同一份缓存, 结果集不变 (`limit` 本就在 API 侧先截断, 过滤前后都是对 ≤limit 条做), 只是缓存内容从子集变超集。**过渡代价**: 升级前由非空 config `label_filter` 写下的旧缓存内含已过滤 items, 新代码在其 TTL 内 (≤ `cache_ttl_seconds`, 默认 900s) 会把它当未过滤全集 ⇒ `open_count_unfiltered` 短暂低估, 自愈。**不加缓存标记强制冷启动**: 那会让所有用户 (含本仓 `label_filter: []`) 升级后无谓多拉一次; 受影响人群本来就在承受同一收窄且今天不可见。此项**明确留给 post_spec 挑战** |
| D4 | 三个 additive 字段, 无条件发出 | 只在过滤时发出会让渲染层多一个 `key in` 分支且与 `warning` 先例不一致; 每字段都有 §4 的显示消费者, 无孤儿字段 |
| D5 | `label_summary` 口径不变 (过滤后 `items[]`) | 改成过滤前更「有用」但静默改变现有 config 过滤用户的契约; 变体 7 因此不列「可用 label」, 改为操作提示 |
| D6 | 匹配 = 精确、大小写敏感 | 与现有实现同义; glob / regex / 否定 / AND 均为非目标 |
| D7 | disabled + flag ⇒ 仅 stderr 固定文案, 不进 `errors[]`, exit 不变 | 进 `errors[]` 会把 exit 翻成 10 并让 AI 对「无害的多余 flag」展示 warning; 回显 label 值违反 stderr typed-channel 纪律 |
| D8 | `_fetch_repo` 去形参 + 改指向既有测试 | 保留形参但恒传 `[]` 是死参数; 既有测试 `test_label_filter_applied` 表达的设计意图是「过滤生效」而非「在取数层生效」, 迁移目标函数即可保留意图 (memory `impact-analysis-first`: 现有测试 = 设计意图 SOT) |

## Impact

| Type | Description |
|------|-------------|
| **Positive** | 一次调用即可按 label 看 🎫 区块; 过滤条件 / 来源 / 过滤前总数在 snapshot 与显示里都可见 —— 顺带修掉 config `label_filter` 今天的静默收窄 |
| **Positive** | 缓存与过滤解耦后, 改 config `label_filter` 也不再在 TTL 内拿到旧口径结果 (今天的潜伏缺陷) |
| **Risk** | D3 过渡窗口内 `open_count_unfiltered` 低估 (≤ TTL, 自愈); 缓解: 文档写明 + 留 post_spec 挑战 |
| **Risk** | `_fetch_repo` 形参变更是模块内私有 API; 缓解: grep 全部调用点 (模块内 2 处 + 测试 1 处), 无外部 import |
| **Risk** | 并发轨: `linked-issue-field-availability` (state-scanner `lib/linked_issue_field.py` + `scripts/linked_issue_field_probe.py`) 与 `sibling-spec-probe` (audit-engine) 已 Approved 待 B.1。与本 Spec **文件级零重叠**, 但同属 aria 子模块 ⇒ 版本号 / CHANGELOG 合并顺序由 C.2 定; B.1 前 fetch + 看板 (memory `concurrent_duplicate_audit_fetch_before_start`) |
| **兼容性** | snapshot / cache schema 号均不变; 现有 `build_snapshot(repo)` / `collect_issue_scan(root)` 调用零改动; `enabled=false` 用户零感知 |

## Tasks

- [ ] 1. `_apply_label_filter` 纯函数 + 单测 (含对抗: 大小写不同 / 子串 不得命中)
- [ ] 2. `_fetch_repo` 去 `label_filter`; 缓存写未过滤; 视图层统一过滤 (live 与 cache 同一路径); 三个 additive 字段
- [ ] 3. `collect_issue_scan(..., *, label_filter_override=None)` + 生效过滤 / 来源解析
- [ ] 4. `scan.py` `--issue-label` argparse (strip / 空值 exit 2 / 去重 / 不拆逗号) + `build_snapshot` 穿线 + disabled 固定文案 warning
- [ ] 5. 测试: 改指向 `test_label_filter_applied`; `TestCollectorEndToEnd` 新增 SC-2/3/4/5/6 用例; 新建 CLI 测试
- [ ] 6. 文档: schema.md 三字段 + 口径; issue-scanning.md 配置行 + 新小节; output-formats.md 变体 6/7; SKILL.md:204 骨架
- [ ] 7. 同步测试: `test_output_format_sync.py` 追加 `🔍 label 过滤`; schema 嵌套字段名断言
- [ ] 8. 全量回归: `python3 tests/run_tests.py`; `scripts/validate_schema_doc.py --offline` exit 0

## Success Criteria

每条写明「怎么会红」; 标 **baseline 必红** 的在今天的代码上必须失败 (Rule #6 substitute 的前提)。

- [ ] **SC-1** (代码) `--issue-label bug --issue-label blocker --issue-label bug` ⇒ `["bug","blocker"]`; `--issue-label "  "` ⇒ `SystemExit(2)`; `--issue-label "a,b"` ⇒ `["a,b"]` 单元素。怎么会红: 拆逗号 / 不去重 / 空值放行。**baseline 必红** (flag 不存在 ⇒ 所有输入都 exit 2, 第一断言红)
- [ ] **SC-2** (代码) config `label_filter=["bug"]` + override `["doc"]`, 取数含 bug+doc 各 1 ⇒ `items` 仅 doc, `label_filter==["doc"]`, `label_filter_source=="cli"`。怎么会红: 交集实现 ⇒ `items==[]`
- [ ] **SC-3** (代码) config `label_filter=["bug"]`, live 取数 bug+doc ⇒ 缓存文件 `repos[key].items` 与顶层 `items` 长度均为 2, snapshot `items` 长度 1, `open_count==1`, `open_count_unfiltered==2`。怎么会红: 过滤仍在 `_fetch_repo` ⇒ 缓存长度 1。**baseline 必红**
- [ ] **SC-4** (代码) 第一次无过滤 live 写缓存; 第二次 TTL 内带 override `["bug"]` ⇒ `source=="cache"`, `items` 只含 bug, 且 mock 表中的 issue 取数命令 (`forgejo GET .../issues` / `gh issue list`) **零命中**。怎么会红: 绕过缓存 (D3 备选 b) ⇒ 观察到取数调用; 缓存视图不过滤 ⇒ items 含 doc。**baseline 必红**
- [ ] **SC-5** (代码) 无任何过滤 ⇒ `label_filter==[]`, `label_filter_source is None`, `open_count_unfiltered==open_count`, 三键**存在**; `snapshot_schema_version` 与 cache `schema_version` 与改动前逐字相同。怎么会红: 只在过滤时发字段 ⇒ KeyError; 顺手 bump 版本 ⇒ 红
- [ ] **SC-6** (代码) `enabled=false` + override ⇒ `data=={"enabled": False}`, `soft_errors` 为空, `build_snapshot` exit code 与不带 flag 时相同。怎么会红: 走 `soft_error` ⇒ exit 10
- [ ] **SC-7** (代码/文档同步) `test_output_format_sync.py` 断言 `🔍 label 过滤` 同时出现在 SKILL.md 与 output-formats.md; 另一测试断言 `state-snapshot-schema.md` 含 `label_filter_source` 与 `open_count_unfiltered` 字面。怎么会红: 任一侧漏写。**baseline 必红**
- [ ] **SC-8** (回归) state-scanner 全量测试绿; `validate_schema_doc.py --offline` exit 0; `test_scan_integration.py` 的 shape 测试零改动通过
- [ ] **SC-9** (行为, 定向 fixture) 给 AI 两份合成 snapshot: A `label_filter:["bug"], open_count:2, open_count_unfiltered:12`; B `label_filter:["releaes"], open_count:0, open_count_unfiltered:12`。A 的 🎫 区块须含 🔍 行且含 `12`; B 须含 ⚠️ 行且**不得**出现「无 open issue」类空态文案。反例臂: 喂改动前的 output-formats.md, 两份都不出 🔍 行 ⇒ 两臂可分辨

## 非目标

- AND 语义 / 否定 (`!bug`) / glob / regex / 大小写不敏感匹配
- env var 入口 (D1); `--no-issue-label-filter` 暴露 `[]` 覆写 (API 已留位, CLI 不开)
- per-repo 过滤; 服务端 `labels=` 查询 (Forgejo wrapper 不可靠, 见 `issue_scan.py:533` 注释)
- 改变 `limit` 与过滤的关系: 过滤仍作用于 API 返回的 ≤`limit` 条 (今天亦然); 想扫得更全请调 `limit`
- 改 `label_summary` 口径 (D5); 改主仓 `.aria/config.template.json` (跨仓, CLI 覆写已在 issue-scanning.md 成文)
- 加缓存标记强制升级后冷启动 (D3)

## rule6_note

依 `standards/conventions/skill-benchmark-exemption.md` 决策表逐 hunk 归类 (§4: AI 可按已成文判据自行归类, 不得表外自创理由; 归类留痕, **请 owner 于 post_spec 复议**):

| hunk | 内容性质 | 处置 | 依据 |
|---|---|---|---|
| `scan.py` / `issue_scan.py` / tests | 纯代码 | **substitute** = SC-1~8 (其中 SC-1/3/4/7 baseline 必红) | 表第一行; worked example 「同 spec v1.60.0 collector 代码层 → substitute」 |
| `state-snapshot-schema.md` 三字段 + `issue-scanning.md` 配置行/小节 | 描述性 (schema / 字段) | substitute = SC-7 | worked example 「`state-snapshot-schema.md` +5 行字段语义 → substitute」 |
| `output-formats.md` 变体 6/7 + `SKILL.md:204` 骨架一行 | 描述性 (输出格式字段) | substitute = SC-7 + 定向 fixture SC-9 | 仓内直接先例: `tests/test_output_format_sync.py` 模块 docstring 明写它就是 v1.38.0 输出格式变更的「Rule #6 substitute」, 把格式完整性变成确定性断言 |

**零裁量守门**: B.2 若触及 `SKILL.md` frontmatter `description`、Step 0 执行命令、`RECOMMENDATION_RULES.md` / `references/rules/*` (「在什么状态下给什么建议」= 运行时指令面, worked example v1.62.0) 中任一处 ⇒ 本表作废, **照跑 AB**。变体 7 的 ⚠️ 提示行是本表最接近「处方」的一处 —— 它是显示口径的告诫而非工作流推荐, 不改推荐规则; 若 post_spec 判其为处方, 按「拿不准 → 照跑」处理。

## 审计检查点 (Rule #10 — AI 不自判)

`.aria/config.json` `audit_engine.checkpoints`: `post_spec = convergence` / `post_planning = convergence` (`pre_merge` / `post_implementation` = off)。本 Spec 按配置走 post_spec convergence 审计, 不因「Level 2 / 改动小」降级或跳过。起草期 `docs/decisions/` 无 `technical-*` 对应记录 (A.1.0 检查), 决策以上表 D1–D8 内嵌, 未另立 decision-log。

──────────────────────────────────────────────────────────── proposal.md 全文 (end) ────────────────────────────────────────────────────────────

🤔 Create this file? [Yes/No/Edit] → **评测模式: 不创建**。全文即上方内容, 同时已存为 outputs/proposal.md。

## A.1.6 验证提示

skill 快照 A.1.6 建议运行 `openspec validate state-scanner-issue-label-filter-param --strict`; 但 `standards/openspec/project.md` 「使用者行动指南」明写 Aria 仓内**不安装 npm CLI, 用 aria 格式 + audit-engine 验证**。本仓 `.aria/config.json` 的 `audit_engine.checkpoints.post_spec = convergence`, 所以正确的验证动作是 A.1 落盘后跑 post_spec convergence 审计 (Rule #10, 不自行豁免)。本次评测不运行任何脚本, 两者都未执行。

## 请 owner 复议的两处 AI 自主判断 (Rule #10 留痕)

1. **rule6_note 归类**: 全部 hunk 归入「纯代码 / 描述性 → substitute」, 依据是 convention 的 worked examples + 仓内 `test_output_format_sync.py` 自述的输出格式 substitute 先例; 变体 7 的 ⚠️ 提示行是最接近「处方」的一处, 已在 proposal 内点名, post_spec 若判处方则照跑 AB。
2. **D3 过渡窗口**: 不加缓存标记强制冷启动, 接受升级后 ≤ TTL 内 `open_count_unfiltered` 短暂低估 (自愈)。已在 proposal 内明确留给 post_spec 挑战。

下一步 (A.2): Level 2 不出 `tasks.md`; 若走 task-planner 派生 `detailed-tasks.yaml`, 以 proposal §Tasks 8 条为输入。B.1 前先 fetch + 看板, 与 `linked-issue-field-availability` / `sibling-spec-probe` 两条已 Approved 的 state-scanner / audit-engine 轨确认版本合并顺序 (文件级零重叠)。

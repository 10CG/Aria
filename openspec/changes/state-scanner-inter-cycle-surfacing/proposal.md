# state-scanner-inter-cycle-surfacing

> **Level**: Minimal (Level 2 Spec — proposal.md 含任务,无独立 tasks.md)
> **Status**: Draft
> **Created**: 2026-05-08
> **Type**: Collector enhancement (G2/G3/G4 from Forgejo Issue #85)
> **Source**: Forgejo Issue [10CG/Aria#85](https://forgejo.10cg.pub/10CG/Aria/issues/85) — SilkNode 实战反馈
> **Predecessor**: T5 quick-win (aria submodule `b22d27d`, 主项目 `a9a6a6a`,2026-05-07) ship 的 SKILL.md 行为兜底,本 Spec ship 后降级为 sanity check
> **Related**: state-scanner v3.0.0 mechanical Phase 1.x architecture

---

## Why

### 实战 forcing function

SilkNode 项目 2026-05-07 inter-cycle session resume:scan.py exit=0、snapshot 字段全 OK、git 干净、上次审计 PASS 收敛。按 v3.0 阶段 2 规则匹配,推荐输出是 `feature_new` 兜底规则。但项目实际状态:

- Marketplace v1 (P1 主线) PRD 已 Approved
- W1 schema 已 ship、W2 待启动
- UPM `## Pending Followups` 表含 **22 个 active rows**(P1×3 / P2×8 / P3×11)
- handoff doc 已写好下次入口建议(`> 🚪 Next session 入口: 见 docs/handoff/2026-05-07-session-handoff.md`)

用户原话:**"信息不完整"**。

### 根因 — 三个 collector 与 UPM 既定契约不一致

UPM 顶部自己写明:

> `## Pending Followups` is single source of truth, state-scanner reads this section

但实测 `aria/skills/state-scanner/scripts/collectors/upm.py` 只解析 HTML 注释中的 `UPMv2-STATE` YAML 块,**完全不读** Pending Followups markdown 表 + handoff doc 指针。`collectors/requirements.py` 也只产出 `stories.by_status` 计数,不传 in-progress US 的 `id + raw_status` 给推荐规则。

三个 surfacing gap:
1. **G2**: 22 个 cross-session followups 全在 AI 视野外,包括 W2 前置(P2)、prod release 风险(P1)、用户可见 feature 待做(P1) — 这些是 inter-cycle resume 时**最该浮上来**的信息
2. **G3**: handoff doc 含 TL;DR + 已完成事项 + 未完成 by priority + 推荐工作流,scan.py 不认这个 link,AI 无从知晓 entry hint
3. **G4**: in-progress US-076(带详细 raw_status 含进度描述)虽计入 `by_status` 但 id 和详情未传给推荐规则,导致"继续 in_progress US"无法触发优先推荐

### 为什么 T5 兜底不够

T5 quick-win(`b22d27d`)在 SKILL.md 阶段 2 加了 17 行"完整性兜底"指引,要求 AI 主动 Read UPM + Grep handoff doc。这是**过渡指引**,本身在文本中已声明 "T2/T3/T4 ship 后降级为 sanity check":

- AI 行为指令是 LLM 随机性 surface,不如 collector 字段稳定
- AB benchmark 在 LLM 噪声下 delta 不可靠(沿用 v1.17.3 立例 smoke + defer 模板)
- 真正可断言的 surfacing 必须在 snapshot schema 层
- T5 不能阻止"AI 忘记 Read"导致 surfacing 漏失

本 Spec ship = 把 T5 兜底从"AI 必须主动 Read"降级为"snapshot 字段缺失时 sanity check",同时让 AB benchmark 拥有可断言的结构信号。

### Aria 方法论对齐

CLAUDE.md 研究目标 #2:"最小化的上下文传递成本 — AI 能快速理解项目状态"。当前 inter-cycle resume 需要 AI 手工 Read UPM 全文 + Grep regex,违背机械化 snapshot 原则。本 Spec 把这部分上下文传递从"AI 阶段 2 自助"变成"scan.py Phase 1.x 机械产出"。

---

## What

### 范围

三个 collector 增强 + 两条 recommendation 规则 + schema 文档更新 + T5 降级 + 完整 `/skill-creator` AB benchmark(此时有可断言结构信号)。

### Key Deliverables

#### G2 — UPM Pending Followups 表解析

**新字段**: `snapshot.requirements.upm.followups[]`

```yaml
# 每个 row 结构
followups:
  - row_index: 1
    priority: "P1"          # 规范化 (P0/P1/P2/P3 或 unknown)
    item: "..."             # Item 列原文
    source: "..."           # Source 列原文 (链接/issue/git ref/etc.)
    tracking: "..."         # Tracking 列原文
    next_action: "..."      # Next Action 列原文 (可空)
    raw_row: "| 1 | P1 | ... | ... | ... | ... |"  # 容错回退
```

**Parser 输入**:UPM markdown 文本中匹配 `## Pending Followups` 标题(允许 `#{2,3}` heading prefix + i18n 全角空格)下的第一张 markdown 表。

**Parser 容错**:
- 表头列名规范化(支持 `Priority` / `优先级` / `Pri`)
- 列序非约束(按表头顺序映射,缺列填 null)
- embedded inline code / pipe escape(`\|`)按 markdown 表标准处理
- 表为空(只有表头分隔行)→ `followups: []`
- 没有 `## Pending Followups` section → 字段不存在(consumer 必须容错)

**新规则**: `pending_followups_p1`

```yaml
priority: 1.85   # 位于 architecture_chain_broken (1.8) 之后、audit_unconverged (1.9) 之前
                 # rationale: inter-cycle P1 followup 优先级高于审计状态感知 (1.9),
                 # 但低于架构链路完整性 (1.8) — 架构断链是更严重的项目健康信号
condition: |
  # 伪代码 (RECOMMENDATION_RULES.md 现有 condition 是自由文本描述, 实现时
  # 等价于 Python: any(f.get("priority") == "P1" for f in
  # snapshot.get("requirements", {}).get("upm", {}).get("followups", []))
  followups 中存在 priority == "P1" 的 row (≥1)
trigger: 推荐输出展示前 5 条 P1 followups + "建议优先处理 cross-cycle backlog"
```

#### G3 — Handoff doc 指针识别

**新字段**: `snapshot.requirements.upm.handoff_doc`

```yaml
handoff_doc:
  path: "docs/handoff/2026-05-07-session-handoff.md"   # 相对 project root 规范化
  exists: true                                          # fail-soft: 路径不存在 = false 但字段保留
  raw_match: "> 🚪 Next session 入口: 见 [docs/handoff/2026-05-07-session-handoff.md]"
```

**Parser 输入**:UPM raw_block 顶部 +/- 30 行内 grep,主 regex:

```python
r"^>\s*[^\n]*?(?:Next session 入口|下次 session 入口|🚪 Next session)[^\n]*?\(([^)]+\.md)\)"
```

主 regex 有三处安全锚点:`^>` 行首 blockquote、关键词枚举、`.md` 扩展名。

**备选 regex**(收紧版,本 Spec 启用):

```python
r"^>\s*.*?(?:handoff|session)[^()\n]{0,80}\(([^)]+\.md)\)"
```

**默认决策(R2 收敛后定稿,移除 "入口" 独立 alternation)**:中文 "入口" 在技术文档中泛化命中风险高("函数入口"、"调试入口"、"程序入口"、"记录入口" 后跟意外 markdown link 即会误报)。备选 regex 仅匹配 `handoff` / `session` 关键词,中文 "入口" 命中依赖**主 regex** 的复合短语枚举(`Next session 入口` / `下次 session 入口` / `🚪 Next session`)。

实现者**不得**单方面在备选 regex 加回独立 "入口" alternation;若有强需求,必须在 PR 描述中说明并补充覆盖性负例测试。

**T3.3 强制负例**(R2 收敛版):
- `> 函数入口在 (xxx.md)` — **不命中**(备选 regex 不含独立 "入口")
- `> 调试入口: 见 [debug.md](debug.md)` — **不命中**(同上)
- `> Next session 入口: ...\n>(下一行)... (handoff.md)` — **不命中**(`[^()\n]` 跨行截断)

**T3.3 强制正例**:
- `> 🚪 Next session 入口: 见 [docs/handoff/x.md](docs/handoff/x.md)` — 主 regex 匹配
- `> handoff: see [handoff.md](handoff.md)` — 备选 regex 匹配
- `> session 入口 (handoff.md)` — 备选 regex 匹配("入口" 仅作为 80 字符内 free-form 文本,不参与关键词匹配)

只取**首条匹配**(UPM 约定 handoff 指针单条)。

**新规则更新**: `pending_followups_p1` rule 命中时,如有 `handoff_doc.exists=true` 一并展示路径作为 entry hint。

#### G4 — in-progress US priority_items

**新字段**: `snapshot.requirements.stories.priority_items[]`

```yaml
priority_items:
  - id: "US-076"
    status_normalized: "in_progress"
    raw_status: "In Progress: M3 closeout 75% complete, AD-M3-7 待回填"
    priority_hint: null    # 未来扩展: 从 US frontmatter Priority 字段读
    file: "docs/requirements/user-stories/US-076.md"
  - id: "US-112"
    status_normalized: "pending"
    raw_status: "Pending: M4 spec drafting"
    priority_hint: null
    file: "docs/requirements/user-stories/US-112.md"
```

**取值策略**:
- **数据源**:`priority_items[]` 是 `stories.items[]` 的**派生视图**(过滤 + 排序 + 切片),**不重新 glob 文件系统**。`requirements.py` 在已有 `story_items` 收集结束后做一次 filter/sort
- 优先级筛选:`in_progress` > `ready` > `pending` (其他 status 不进 priority_items)
- N 默认 5(可配 `state_scanner.priority_items_limit`)
- **排序(三级 stable tie-break,跨 OS 确定)**:
  1. `_STATUS_ORDER` ASC: `in_progress=0 < ready=1 < pending=2`
  2. file mtime DESC(同 status 内新近优先)
  3. file path LEX ASC(同 status + 同 mtime 时字母序;防 `git clone` 平铺 mtime 退化)
- **mtime 读取**:仅对入选项调用 `Path.stat().st_mtime` 一次(N≤5 通常)
- `priority_hint` 字段为 future 扩展占位,本 Spec 不实现 US frontmatter Priority 解析

**新规则**: `resume_in_progress_us`

```yaml
priority: 1.88   # 紧邻 pending_followups_p1 (1.85) 之后、audit_unconverged (1.9) 之前
                 # rationale: in-progress US 是当前 cycle 进行中的工作,
                 # 优先级与 P1 followup 同级但稍后, 让 cross-cycle backlog 先浮出
condition: |
  # 伪代码 (同 pending_followups_p1 注释): 实现等价于 Python:
  # any(i.get("status_normalized") == "in_progress" for i in
  # snapshot.get("requirements", {}).get("stories", {}).get("priority_items", []))
  priority_items 中存在 status_normalized == "in_progress" 的项 (≥1)
trigger: 推荐输出展示 in_progress US id + raw_status 第一行,推荐 "继续 US-X (Phase B/C/D)"
```

#### Cross-cutting

- **Prerequisite — `git.status_clean` derived 字段**: `collectors/git.py` 现仅产 `staged_files[] / unstaged_files[] / uncommitted_count`,**无 `status_clean` 字段**,而 T5 SKILL.md 触发条件 1 引用此字段。新增 `status_clean: bool = (staged_files == [] and unstaged_files == [])` derived 字段,同步 `state-snapshot-schema.md §git`。否则 TX.2 降级后触发条件永远 false → silent failure
- **Schema 文档**: `aria/skills/state-scanner/references/state-snapshot-schema.md` 加 §git.status_clean, §upm.followups, §upm.handoff_doc, §requirements.stories.priority_items 四节及 backward-compat 声明。**字段缺失行为统一**:`upm.followups` 字段不存在(无 `## Pending Followups` section)/ `upm.handoff_doc: null`(无匹配)/ `priority_items: []`(无候选)
- **normalize_snapshot 同步**: `normalize_snapshot.py` 加规则 — `followups[*].raw_row` 进 `DROP_KEYS` 防大文本 drift 加剧已知 flake `test_two_consecutive_runs_diff_zero`。`priority_items[]` 排序结果若不进 DROP_KEYS,需保证三级 stable tie-break(见 G4 取值策略)。`handoff_doc.raw_match` 同 raw_row 处理
- **T5 兜底降级 (mock 段落)**: `aria/skills/state-scanner/SKILL.md` 阶段 2 第 172-187 行 17 行替换为约 7 行 sanity check:
  ```markdown
  **完整性兜底 (inter-cycle resume — sanity check)**:

  > 若 `requirements.upm.followups[]` 字段不存在 / 为空 (`[]`),
  > 但 UPM `source_file` 文本中确实含有 `## Pending Followups` 标题
  > (mechanical grep 验证) → snapshot 字段构造异常 → soft warn:
  > "followups 字段缺失,inter-cycle 优先级可能不完整。检查 collectors/upm.py 版本"
  > 同理校验 `upm.handoff_doc` 与 `requirements.stories.priority_items[]`
  ```
  原 4 项触发条件 + 3 个 AI 主动 Read/Grep 行动**全部删除**(由 collector 字段替代)
- **完整 `/skill-creator` AB benchmark (三 arm 拆分,delta 归因)**:
  - **arm A**: baseline `without_skill` (无 state-scanner)
  - **arm B**: `with_skill v1.17.7 + T5` (T5 兜底保留,无新 collector 字段)
  - **arm C**: `with_skill v1.18.0` (新 collector + 新规则 + T5 降级)
  - 期望 `delta(C - B)` 为正(收益主要来自 collector 而非 T5),`delta(B - A)` 验证 T5 价值。固定 inter-cycle-resume fixture (规格见下),结果存 `aria-plugin-benchmarks/ab-results/{date}-state-scanner-inter-cycle-surfacing/`
  - **fixture 最小规格** (避免与 SilkNode 真实数据耦合):
    - followups: 6 行 (P1×2 / P2×2 / P3×2)
    - handoff_doc: `> 🚪 Next session 入口: 见 [docs/handoff/stub.md](docs/handoff/stub.md)` + 空 stub.md (exists=true)
    - 1 个 in_progress US + 1 个 pending US
    - 额外 negative fixture × 2: (a) UPM 无 Pending Followups 表 (b) handoff 路径不存在
- **版本 bump**: aria-plugin v1.17.7 → **v1.18.0**(新 collector 字段 + 新规则 = MINOR per CLAUDE.md 项目惯例)

---

## Impact

| Type | Description |
|------|-------------|
| **Positive** | inter-cycle resume surfacing 从 LLM 兜底升级为机械化 snapshot;AI 跨 session 优先级追踪能力质变;UPM Pending Followups 表与 collector 契约一致;为 SilkNode + Aria + Aether + Kairos 等多项目复用 |
| **Positive** | 完整 `/skill-creator` AB benchmark 数据进入常态化积累(三 arm 拆分让 delta 归因可分),T5 sanity check 降级后 SKILL.md 阶段 2 段瘦身 17→7 行 |
| **Risk** | snapshot schema 加 4 字段(`git.status_clean` + 3 inter-cycle 字段)— backward-compat 必须保证(consumer 不假定字段存在)。Mitigation:Aria + Kairos + Aether 三项目跑 dogfooding,任一 collector 退化必阻塞;TX.6 加 ≥2 个 unit test 验证 `.get()` 防御性访问 |
| **Risk** | markdown table parser 的容错可能误命中非 Pending Followups 表(项目 UPM 内可能有多张表)。Mitigation:严格锚定 `## Pending Followups` 标题文本(大小写敏感、允许 0-3 前导空格),只取标题后第一张 `\|` 起始表;T2.3 多表 negative case 覆盖 |
| **Risk** | handoff regex 写死中文/Emoji,跨语言项目可能漏匹配。Mitigation:R2 收敛版备选 regex 移除独立 "入口" alternation,仅 `handoff` / `session` 关键词;主 regex 保留复合短语 `Next session 入口` / `下次 session 入口` / `🚪 Next session` 覆盖中文场景;T3.3 三负例(函数入口 / 调试入口 / 跨行)+ 三正例覆盖 |
| **Risk** | `priority_items[]` mtime 排序在 `git clone` 平铺 mtime 时退化为 glob 顺序,加剧 issue #61 cross-platform flake 风险。Mitigation:三级 stable tie-break (`status_order ASC → mtime DESC → path LEX ASC`),path LEX 在 mtime 平局时确保确定性 |

---

## Tasks

> **执行顺序**: TX.0 (git.status_clean) + TX.1 (schema doc) **必须先于** G2/G3/G4 实现任务 (per CLAUDE.md "规范先行" 认知框架);G2 / G3 / G4 三组无文件冲突可**并行实施** (G2 改 upm.py table parser、G3 改 upm.py regex、G4 改 requirements.py priority_items);Cross-cutting TX.2-TX.7 必须等 G2/G3/G4 全部 merge 后串行。

### G0 — Prerequisite (新增)

- [ ] **TX.0** `collectors/git.py` 加 derived 字段 `status_clean: bool`(`staged_files == [] and unstaged_files == []`)+ schema 文档同步 + 1 个 unit test

### G2 — UPM Pending Followups 表解析

- [ ] **T2.1** schema 设计:`snapshot.requirements.upm.followups[]` 字段格式定稿(含 row_index / priority / item / source / tracking / next_action / raw_row)
- [ ] **T2.2** `collectors/upm.py` 加 markdown table parser:
  - heading regex: `r"^[ \t]{0,3}#{2,3}\s+Pending Followups\s*$"` (大小写敏感、允许 0-3 前导空格、显式排除全角空格 　)
  - heading 与表格间允许任意非表格行,逐行扫描直到 `\|` 起始行
  - pipe escape 处理: `row.replace('\\|', '\x00').split('\|')` 后还原
  - 列规范化: 表头列名映射 (`Priority` / `优先级` / `Pri`)
  - 实现者可自决是否拆 `_upm_followups.py` sub-module (无需另起 Spec)
- [ ] **T2.3** 单元测试 **(≥ 8 cases,T2.3.a-h 一一对应)**:
  - T2.3.a 正常表 (4-6 行,含 P1/P2/P3)
  - T2.3.b 空表 (只有 header+separator)
  - T2.3.c 错列序 (列名映射验证)
  - T2.3.d 缺列 (Tracking 列不存在 → null 填充)
  - T2.3.e embedded inline code in cell
  - T2.3.f pipe escape `\|` in cell (正确还原为字面 `|`)
  - T2.3.g 多表 negative (UPM 含其他表但 `## Pending Followups` 缺失 → followups 字段不存在)
  - T2.3.h heading 前导空格 / heading 与表间含说明段落
- [ ] **T2.4** `RECOMMENDATION_RULES.md` 加 `pending_followups_p1`(priority 1.85),含 condition + trigger + 输出展示模板(前 5 条 P1)
- [ ] **T2.5** Aria + Kairos + SilkNode (mock fixture) dogfooding:验证 followups[] 字段非空且 priority 列规范化正确

### G3 — Handoff doc 指针识别

- [ ] **T3.1** `collectors/upm.py` 加 raw_block 顶部 grep regex(主 `Next session 入口` + 收紧版备选 `^>\s*.*?(?:入口|handoff|session)[^()\n]{0,80}\(([^)]+\.md)\)`),取首条匹配
- [ ] **T3.2** 路径格式三态:
  - 相对路径 → `(project_root / raw).resolve()` + `relative_to(project_root)`
  - 绝对路径 → `Path(raw).resolve()` + 不做 `relative_to`,exists() 检查
  - URL (`http://` / `https://`) → `path=raw`, `exists=false` + `soft_error("unsupported_path_format")`
- [ ] **T3.3** 单元测试 **(≥ 5 cases,T3.3.a-e)**:
  - T3.3.a 中文 / 英文 / Emoji 三种 entry 形式 (3 子测试)
  - T3.3.b 多 link 取首条
  - T3.3.c 路径不存在 → `exists=false` fail-soft
  - T3.3.d 误命中负例: `> 函数入口在 (xxx.md)` / `> 调试入口: 见 [debug.md](debug.md)` 不命中
  - T3.3.e 跨行不命中: `> Next session ...\n>(下一行) (handoff.md)`
- [ ] **T3.4** schema 文档更新 §upm.handoff_doc

### G4 — in-progress US priority_items

- [ ] **T4.1** schema 设计:`snapshot.requirements.stories.priority_items[]`(id + status_normalized + raw_status + priority_hint=null + file)
- [ ] **T4.2** `collectors/requirements.py` **基于已有 `story_items[]` 派生** (不重新 glob):
  - 过滤 `status_normalized ∈ {in_progress, ready, pending}`
  - 三级 stable 排序: `_STATUS_ORDER ASC → mtime DESC → path LEX ASC`
  - mtime 仅对入选项调用 `Path.stat().st_mtime` 一次 (N≤5)
  - 切片头部 N (默认 5,可配)
  - 确认 `_normalize_status('ready')` 与 `**Status**: Ready` 链路在 `_status.py` 中正确归一为 `ready`(若不正确,补 normalize 修复)
- [ ] **T4.3** `RECOMMENDATION_RULES.md` 加 `resume_in_progress_us`(priority 1.88)
- [ ] **T4.4** 单元测试 **(≥ 4 cases,T4.4.a-d)**:
  - T4.4.a in_progress + ready + pending 排序顺序正确
  - T4.4.b 同 status 同 mtime 时 path LEX 字母序 (验证 git clone 平铺 mtime 场景)
  - T4.4.c N=0 / 全部空状态 → `priority_items: []`
  - T4.4.d `_normalize_status('ready')` / `**Status**: Ready` / `**状态**: 就绪` 正确归一为 `ready`
- [ ] **T4.5** 配置项 `state_scanner.priority_items_limit`(默认 5)纳入 config-loader

### Cross-cutting

- [ ] **TX.1** `aria/skills/state-scanner/references/state-snapshot-schema.md` 四节扩充 (§git.status_clean + §upm.followups + §upm.handoff_doc + §requirements.stories.priority_items) + 显式声明 backward-compat (字段缺失行为统一,见 What §Cross-cutting Schema 文档)
  - 子任务 TX.1.a: `normalize_snapshot.py` 加规则 — `followups[*].raw_row` 进 `DROP_KEYS` 防大文本 drift 加剧已知 flake (类似 recent_commits 处理);`handoff_doc.raw_match` 同处理
  - 子任务 TX.1.b: `test_normalize_snapshot.py` 加 followups/handoff_doc/priority_items normalize 规则覆盖 case (已含确定性排序的 priority_items 不必 DROP,只需稳定性测试)
- [ ] **TX.2** `aria/skills/state-scanner/SKILL.md` 阶段 2 "完整性兜底" 段降级为约 7 行 sanity check (mock 段落见 What §Cross-cutting T5 兜底降级);删除原 4 触发条件 + 3 AI 主动 Read/Grep 行动
- [ ] **TX.3** 完整 `/skill-creator` AB benchmark 跑一次 **(三 arm 拆分,delta 归因)**:
  - **arm A**: baseline `without_skill`
  - **arm B**: `with_skill v1.17.7 + T5` (T5 兜底保留,无新 collector)
  - **arm C**: `with_skill v1.18.0` (新 collector + 新规则 + T5 降级)
  - **fixture 最小规格** (避免与 SilkNode 真实数据耦合): 见 What §Cross-cutting fixture 规格 (followups 6 行 P1×2/P2×2/P3×2 + handoff stub + 1 in_progress US + 1 pending US + 2 negative)
  - 结果存 `aria-plugin-benchmarks/ab-results/{YYYY-MM-DD}-state-scanner-inter-cycle-surfacing/` + `latest` symlink 切换
  - PASS gate: `delta(C - A) ≥ 0` 阻塞 merge;Quality target: `delta(C - A) ≥ +5pp` 不阻塞但记录 benchmark.md;`delta(C - B)` 应为正(收益主要来自 collector)
- [ ] **TX.4** Aria 子模块版本 bump v1.17.7 → v1.18.0:plugin.json + marketplace.json + VERSION + CHANGELOG.md + README.md
- [ ] **TX.5** 主项目 submodule 指针 bump + 主项目 VERSION + CHANGELOG 同步
- [ ] **TX.6** Backward-compat verify (新增):`test_upm.py` + `test_requirements.py` 加 ≥ 2 个 unit test,验证 consumer 用 `result.data.get('followups', [])` / `data['stories'].get('priority_items', [])` 等防御性访问方式在字段缺失时不抛 KeyError + 行为合理
- [ ] **TX.7** PR merge 前在 Aria + Kairos + Aether 三项目本地分别跑 scan.py,exit=0 + errors=[] 截图或日志附 PR 描述 (CI 接入留 future Spec)

---

## Success Criteria

- [ ] `state-scanner --output snapshot.json` 在 SilkNode 真实项目上产出含 `upm.followups[]` (≥1 P1 row), `upm.handoff_doc.path` (handoff doc), `requirements.stories.priority_items[]` (≥1 in_progress US) 的 snapshot
- [ ] `git.status_clean` 字段在所有 dogfooding 项目 snapshot 中正确产出(干净 = true,有暂存/未暂存 = false)
- [ ] Aria + Kairos + Aether 三项目 dogfooding scan.py 0 退化:`exit=0`,`errors=[]` 或仅 fail-soft 软错误
- [ ] **state-scanner 单元测试套件 ≥ 389 pass** (372 baseline,实测 grep 计数,**非** Spec 旧文 371) **+ ≥17 新增分项覆盖**:
  - G2 ≥ 8 cases (T2.3.a-h 一一对应)
  - G3 ≥ 5 cases (T3.3.a-e 一一对应)
  - G4 ≥ 4 cases (T4.4.a-d 一一对应)
- [ ] **AB benchmark 双层标准**:
  - **PASS gate (阻塞 merge)**: `delta(arm C − arm A) ≥ 0`(with new collectors 不劣于 baseline)
  - **Quality target (不阻塞,记录 benchmark.md)**: `delta(arm C − arm A) ≥ +5pp`
  - 归因证据: `delta(C − B)` ≥ 0(收益主要来自 collector 而非 T5)
- [ ] T5 兜底降级生效:SKILL.md 阶段 2 "完整性兜底" 段从 17 行 (4 触发条件 + 3 AI 主动 Read/Grep + 过渡说明) 缩减为 7 行 sanity check,逻辑替换为 "snapshot 字段缺失但 UPM 含 `## Pending Followups` 表 → soft warn"
- [ ] **Backward-compat verify (TX.6)**:`test_upm.py` + `test_requirements.py` ≥ 2 个 case 验证 `data.get('followups', [])` / `data['stories'].get('priority_items', [])` 等防御性访问在字段缺失时不抛 KeyError 且 fallback 行为合理
- [ ] `pending_followups_p1` 规则触发时推荐输出含 P1 items 简表 + handoff doc 路径(若 G3 命中)
- [ ] `resume_in_progress_us` 规则触发时推荐输出含 in_progress US id + raw_status 摘要

---

## Out of Scope (本 Spec 不做)

- **G1** PRD `**Status**:` markdown 解析失败诊断 — Issue #85 中已确认 `_status.py` 已含 6 个 pattern,SilkNode 5/5 全 null 是异常,需先要诊断数据(`state-snapshot.json` 摘录 + PRD 头部 raw bytes)。本 Spec **不**盲改 parser,等数据回贴后单独处理(可能是 fixture / 路径 mismatch / 格式变体,处理路径不同)
  - **追踪策略**:保留 Issue #85 open 状态;若 **2026-05-22** 前 SilkNode 未回贴诊断数据,由 Tech Lead 决策关闭 G1 / 转 backlog / 降优;G1 独立 Spec(若需)在 `openspec/changes/` 下另起,**不**修改本 Spec
- **`docs/architecture/system-architecture.md` 同步** — 该文档描述高层 state-scanner 架构(Phase 1.x mechanical 路径 + collector 调用关系),**不**枚举 snapshot 字段集。本次新增 4 字段(`git.status_clean` + 3 inter-cycle)无需修改该文档,仅 `state-snapshot-schema.md` 更新(per CLAUDE.md Rule #3 同步原则,文档/代码同步范围限于 schema 文档)
- handoff doc 内容深度解析(TL;DR / priority sections 抽取)— 当前只识别指针 + 路径,内容由 AI Read 处理。如未来证明需要,起 follow-up Spec
- UPM `## Pending Followups` 表跨多张拼接 / 多语言混合 — 单一项目通常单表,如需要起 follow-up
- Forgejo Issue ↔ followup 双向同步 — 已是 forgejo-sync skill 范畴
- `state_scanner.handoff_aliases` 配置项扩展(运行时可注入更多 alias regex)— 本 Spec 在 G3 备选 regex 内置中英文 alias,运行时配置留 future

---

## References

- Forgejo Issue [10CG/Aria#85](https://forgejo.10cg.pub/10CG/Aria/issues/85) — SilkNode 实战反馈原文 + T5 quick-win 范围
- T5 quick-win benchmark `aria-plugin-benchmarks/ab-results/2026-05-07-state-scanner-t5-ai-fallback/` — Round 2 13/13 PASS(沿用 v1.17.3 doc-dominant smoke + defer 模板)
- Issue #85 评论 [issuecomment-5379](https://forgejo.10cg.pub/10CG/Aria/issues/85#issuecomment-5379) — partial accept triage(G2/G3/G4 接受,G1 待数据)
- Issue #85 评论 [issuecomment-5421](https://forgejo.10cg.pub/10CG/Aria/issues/85#issuecomment-5421) — T5 shipped status
- Aria CLAUDE.md 研究目标 #2:"最小化的上下文传递成本"
- state-scanner v3.0 architecture decision AD-SSME-5(mechanical Phase 1.x 路径)
- 前序相关 Spec: `state-scanner-collector-regex-hardening` (v1.17.3, 立例 doc-dominant patch smoke), `state-scanner-i18n-status-regex` (v1.17.2, i18n 扩展)

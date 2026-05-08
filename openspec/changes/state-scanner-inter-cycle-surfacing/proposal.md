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
priority: 1.85   # 优先级介于 multi_remote_drift (1.35) 与 readme_outdated (1.3) 之间
condition: snapshot.requirements.upm.followups[*] | filter priority="P1" | count > 0
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

放宽备选(可配 `state_scanner.handoff_aliases` future):
- `> .*入口.*\(([^)]+\.md)\)`
- `> .*handoff.*\(([^)]+\.md)\)`

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
- 优先级筛选:`in_progress` > `ready` > `pending` (其他 status 不进 priority_items)
- N 默认 5(可配 `state_scanner.priority_items_limit`)
- 排序:status_normalized 优先级 → file mtime DESC(同优先级新近优先)

**新规则**: `resume_in_progress_us`

```yaml
priority: 1.88   # 紧邻 pending_followups_p1 (1.85) 之后,在 multi_remote_drift (1.35) 之前
condition: snapshot.requirements.stories.priority_items[*] | filter status_normalized="in_progress" | count >= 1
trigger: 推荐输出展示 in_progress US id + raw_status 第一行,推荐 "继续 US-X (Phase B/C/D)"
```

#### Cross-cutting

- **Schema 文档**: `aria/skills/state-scanner/references/state-snapshot-schema.md` 加 §upm.followups, §upm.handoff_doc, §requirements.stories.priority_items 三节及 backward-compat 声明
- **T5 兜底降级**: `aria/skills/state-scanner/SKILL.md` 阶段 2 "完整性兜底" 段从"AI 必须 Read UPM/handoff"改为"如 `upm.followups[]` 缺失或为空且 UPM 文件确含 `## Pending Followups` 表 → snapshot 字段构造异常 → soft warn"
- **完整 `/skill-creator` AB benchmark**: 此时 schema 引入可断言结构信号(snapshot 三新字段是否非空、推荐规则是否触发),AB delta 不再被 LLM 噪声淹没。固定 inter-cycle-resume fixture(SilkNode 简化版)+ 4 evals × 2 configs × subagents = 标准 AB 流程。结果存 `aria-plugin-benchmarks/ab-results/{date}-state-scanner-inter-cycle-surfacing/`
- **版本 bump**: aria-plugin v1.17.7 → **v1.18.0**(新 collector 字段 + 新规则 = MINOR per CLAUDE.md 项目惯例)

---

## Impact

| Type | Description |
|------|-------------|
| **Positive** | inter-cycle resume surfacing 从 LLM 兜底升级为机械化 snapshot;AI 跨 session 优先级追踪能力质变;UPM Pending Followups 表与 collector 契约一致;为 SilkNode + Aria + Aether + Kairos 等多项目复用 |
| **Positive** | 完整 `/skill-creator` AB benchmark 数据进入常态化积累,T5 sanity check 降级后 SKILL.md 阶段 2 段瘦身 |
| **Risk** | snapshot schema 加 3 字段 — backward-compat 必须保证(consumer 不假定字段存在)。Mitigation:Aria + Kairos + Aether 三项目跑 dogfooding,任一 collector 退化必阻塞 |
| **Risk** | markdown table parser 的容错可能误命中非 Pending Followups 表(项目 UPM 内可能有多张表)。Mitigation:严格锚定 `## Pending Followups` 标题文本,只取标题后第一张表;新增否定测试覆盖"UPM 内含其他表但 Pending Followups 缺失" |
| **Risk** | handoff regex 写死中文/Emoji,跨语言项目可能漏匹配。Mitigation:G3 规范多 alias regex + 配置项预留 future i18n 扩展 |

---

## Tasks

### G2 — UPM Pending Followups 表解析

- [ ] **T2.1** schema 设计:`snapshot.requirements.upm.followups[]` 字段格式定稿(含 row_index / priority / item / source / tracking / next_action / raw_row)
- [ ] **T2.2** `collectors/upm.py` 加 markdown table parser:锚点匹配 `## Pending Followups` heading + 提取后续首张表 + 列规范化 + i18n 全角分隔/中文表头别名
- [ ] **T2.3** 单元测试:正常表 / 空表(只有 header+separator) / 错列序 / 缺列 / embedded inline code / 多表 negative / heading 缺失 fail-soft / 表内 pipe escape
- [ ] **T2.4** `RECOMMENDATION_RULES.md` 加 `pending_followups_p1`(priority 1.85),含 condition + trigger + 输出展示模板(前 5 条 P1)
- [ ] **T2.5** Aria + Kairos + SilkNode (mock fixture) dogfooding:验证 followups[] 字段非空且 priority 列规范化正确

### G3 — Handoff doc 指针识别

- [ ] **T3.1** `collectors/upm.py` 加 raw_block 顶部 grep regex(`Next session 入口` 主 + `入口` / `handoff` 备选),取首条匹配
- [ ] **T3.2** 路径规范化:相对 project root + `os.path.exists` 验证 → `handoff_doc.exists` 字段
- [ ] **T3.3** 单元测试:中文/英文/Emoji 三种 entry 形式 / 多 link 取首 / 路径不存在 fail-soft / regex 模糊匹配负例
- [ ] **T3.4** schema 文档更新 §upm.handoff_doc

### G4 — in-progress US priority_items

- [ ] **T4.1** schema 设计:`snapshot.requirements.stories.priority_items[]`(id + status_normalized + raw_status + priority_hint + file)
- [ ] **T4.2** `collectors/requirements.py` 增量提取 in_progress + ready + pending 头部 N(默认 5)项,带文件路径,按 status_normalized 优先级 + mtime 排序
- [ ] **T4.3** `RECOMMENDATION_RULES.md` 加 `resume_in_progress_us`(priority 1.88)
- [ ] **T4.4** 单元测试 + schema 文档 §requirements.stories.priority_items
- [ ] **T4.5** 配置项 `state_scanner.priority_items_limit`(默认 5)纳入 config-loader

### Cross-cutting

- [ ] **TX.1** `aria/skills/state-scanner/references/state-snapshot-schema.md` 三节扩充 + 显式声明 backward-compat(consumer 不假定字段存在)
- [ ] **TX.2** `aria/skills/state-scanner/SKILL.md` 阶段 2 "完整性兜底" 段降级为 sanity check 措辞 + 引用新字段名
- [ ] **TX.3** 完整 `/skill-creator` AB benchmark 跑一次:
  - 固定 fixture:`aria-plugin-benchmarks/state-scanner/fixtures/inter-cycle-resume/`(UPM 含 22 行 Pending Followups 表 + handoff doc + git 干净 + audit 收敛 mock)
  - 2-3 evals × (with_skill v1.18.0 vs without_skill / vs old_skill v1.17.7) × subagents
  - 结果存 `aria-plugin-benchmarks/ab-results/{YYYY-MM-DD}-state-scanner-inter-cycle-surfacing/` + `latest` symlink 切换
  - delta 必须为正(with_skill 通过率 ≥ baseline)
- [ ] **TX.4** Aria 子模块版本 bump v1.17.7 → v1.18.0:plugin.json + marketplace.json + VERSION + CHANGELOG.md + README.md
- [ ] **TX.5** 主项目 submodule 指针 bump + 主项目 VERSION + CHANGELOG 同步

---

## Success Criteria

- [ ] `state-scanner --output snapshot.json` 在 SilkNode 真实项目上产出含 `upm.followups[]` (≥1 P1 row), `upm.handoff_doc.path` (handoff doc), `requirements.stories.priority_items[]` (≥1 in_progress US) 的 snapshot
- [ ] Aria + Kairos + Aether 三项目 dogfooding scan.py 0 退化:`exit=0`,`errors=[]` 或仅 fail-soft 软错误
- [ ] state-scanner 单元测试套件 ≥ 380 pass(371 baseline + ≥9 新增覆盖 G2/G3/G4)
- [ ] 完整 `/skill-creator` AB benchmark with_skill 通过率 ≥ without_skill (delta ≥ 0,理想 +5pp 以上)
- [ ] T5 兜底降级生效:SKILL.md 阶段 2 "完整性兜底" 段从"AI 必须 Read"改为"如新字段缺失则 sanity check warn"
- [ ] 反向 backward-compat 验证:旧版 consumer(模拟"假定 followups 字段不存在")仍能正常运行,不抛 KeyError
- [ ] `pending_followups_p1` 规则触发时推荐输出含 P1 items 简表 + handoff doc 路径(若 G3 命中)
- [ ] `resume_in_progress_us` 规则触发时推荐输出含 in_progress US id + raw_status 摘要

---

## Out of Scope (本 Spec 不做)

- **G1** PRD `**Status**:` markdown 解析失败诊断 — Issue #85 中已确认 `_status.py` 已含 6 个 pattern,SilkNode 5/5 全 null 是异常,需先要诊断数据(`state-snapshot.json` 摘录 + PRD 头部 raw bytes)。本 Spec **不**盲改 parser,等数据回贴后单独处理(可能是 fixture / 路径 mismatch / 格式变体,处理路径不同)
- handoff doc 内容深度解析(TL;DR / priority sections 抽取)— 当前只识别指针 + 路径,内容由 AI Read 处理。如未来证明需要,起 follow-up Spec
- UPM `## Pending Followups` 表跨多张拼接 / 多语言混合 — 单一项目通常单表,如需要起 follow-up
- Forgejo Issue ↔ followup 双向同步 — 已是 forgejo-sync skill 范畴

---

## References

- Forgejo Issue [10CG/Aria#85](https://forgejo.10cg.pub/10CG/Aria/issues/85) — SilkNode 实战反馈原文 + T5 quick-win 范围
- T5 quick-win benchmark `aria-plugin-benchmarks/ab-results/2026-05-07-state-scanner-t5-ai-fallback/` — Round 2 13/13 PASS(沿用 v1.17.3 doc-dominant smoke + defer 模板)
- Issue #85 评论 [issuecomment-5379](https://forgejo.10cg.pub/10CG/Aria/issues/85#issuecomment-5379) — partial accept triage(G2/G3/G4 接受,G1 待数据)
- Issue #85 评论 [issuecomment-5421](https://forgejo.10cg.pub/10CG/Aria/issues/85#issuecomment-5421) — T5 shipped status
- Aria CLAUDE.md 研究目标 #2:"最小化的上下文传递成本"
- state-scanner v3.0 architecture decision AD-SSME-5(mechanical Phase 1.x 路径)
- 前序相关 Spec: `state-scanner-collector-regex-hardening` (v1.17.3, 立例 doc-dominant patch smoke), `state-scanner-i18n-status-regex` (v1.17.2, i18n 扩展)

# state-scanner-i18n-status-regex — Status 正则中文 i18n 增强

> **Level**: Minimal (Level 2 Spec — 仅 proposal.md, 无 tasks.md)
> **Status**: Complete (2026-04-25, implementation merged in aria PR #30 + Aria PR #48)
> **Created**: 2026-04-25
> **Completed**: 2026-04-25
> **Parent Story**: (无, 跨 Skill 基础设施增强)
> **Source**: 2026-04-25 state-scanner-mechanical-enforcement T8 Kairos 跨项目验证发现 (PR #44)
> **Target (revised)**: aria-plugin v1.17.2 patch (实施完成早于预期, 不再 hold 到 v1.18.x; 原计划改为 v1.18.0 同步移除 mechanical_mode opt-out 不变)
> **Estimate**: ~1h (regex + tests)

---

## Why

state-scanner v3.0.0 mechanical-mode 的 `requirements.collector` Phase 1.5 Status 提取
正则覆盖 5 种文档格式 (SKILL.md §1.5):

```
1. YAML-like header:    /^Status:\s*(.+)/i
2. Markdown bold key:   /^\*\*Status\*\*:\s*(.+)/i
3. 中文键名:            /^\*\*状态\*\*:\s*(.+)/i
4. Blockquote 行起头:   /^>\s*\*\*Status\*\*:\s*(.+)/i
5. 表格列:              /^\|\s*(?:Status|状态)\s*\|\s*(.+?)\s*\|/i
```

T8 Kairos dogfooding 在 TS/Node.js 项目上发现, 中文 markdown 习惯写法
**不被任何现有正则覆盖**. 实测样本 (Kairos `docs/requirements/user-stories/US-009-tts-voice-clone.md`):

```markdown
> **优先级**：P0 | **里程碑**：M3 | **状态**：pending
```

两个未支持特征:

1. **Fullwidth colon `：` (U+FF1A)** — 中文输入法默认产生的全角冒号,
   而非半角 `:` (U+003A). 仅 pattern 5 (表格) 支持 `[：:]` 字符类, 其他 4 个仅 `:`.
2. **Inline blockquote 多 meta 单行** — 多个键值对用 `|` 分隔放在 1 个 blockquote
   行内, 状态键不在行首. Pattern 4 锚定 `^>\s*\*\*Status\*\*` 假设 status
   是行内首个键, 与中文文档"meta 平铺"习惯冲突.

**影响**: Kairos 项目 15 user stories 中 1 个 (US-009) 因此被漏检 status, scan.py
返回 `raw_status=null` → `_normalize_status(None) → "unknown"`, by_status 聚合
仍准确但单 story 状态信号丢失. fail-soft 保护下不会破坏下游推荐, 但跨语言/i18n
习惯下用户体感是"为什么这个 story 状态不识别".

**为什么需要独立 Spec 而非热修复**:

- `mechanical-enforcement` Spec (PR #44 已 closed) 验收边界明确 = "无 Aria-only 假设".
  i18n 是 *另一类* 假设 (英文/halfwidth 默认), 与 Aria-only 不重叠. 把它塞回那个
  Spec 会破坏 scope hygiene (`feedback_scope_bounded_merge_for_level3.md`).
- 该增强需要 SKILL.md §1.5 文档同步 + `_status.py` regex 拓展 + tests, 是有
  明确 acceptance 的 ~1h 任务, 大于"代码注释级"修复, 小于"功能级"重构. Level 2 Spec
  是最贴的工作粒度.
- 影响范围跨 `requirements.py` + `openspec.py` 两个 collector (后者也用 `_status.py`),
  需要决策"是否两侧同步增强还是仅 requirements". 决策点配 Spec 比配 commit message 更稳.

## What Changes

### `_status.py` 正则增强

| Pattern # (code order) | Before | After | 说明 |
|---|---|---|---|
| 1 | `^\*\*Status\*\*:\s*(.+?)\s*$` | `^\*\*Status\*\*[：:]\s*(.+?)\s*$` | 加 fullwidth colon |
| 2 | `^\*\*状态\*\*:\s*(.+?)\s*$` | `^\*\*状态\*\*[：:]\s*(.+?)\s*$` | 加 fullwidth colon |
| 3 | `^>\s*\*\*Status\*\*:\s*(.+?)\s*$` | `^>\s*\*\*Status\*\*[：:]\s*(.+?)\s*$` | 加 fullwidth colon |
| 4 | `^(?:#{1,6}\s+)?Status:\s*(.+?)\s*$` | `^(?:#{1,6}\s+)?Status[：:]\s*(.+?)\s*$` | 加 fullwidth colon |
| **6 (NEW)** | (无) | `^>\s*.*?\*\*(?:Status\|状态)\*\*[：:]\s*([^\|\n]+?)(?=\s*(?:\|\|$))` | inline blockquote 多 meta |

(Pattern 5 = table column, 已支持 `[：:]`, 不变)

Pattern 6 设计要点:
- 不锚定 `^>\s*\*\*` 行首 — 允许 status 不在行内第一个键.
- 必须以 `>` 开头 (blockquote) 限定语境, 避免误捕获正文中包含 "状态" 的句子.
- `(?:Status|状态)` 双语兼容.
- `[：:]` 双 colon.
- 捕获组 `([^\|\n]+?)` 非贪婪到 `|` 或行尾 — 多 meta 列表里只取本键的值.
- 终止 `(?:\s*\\|\s*\|$)` — 后跟 `|` 分隔符或行尾, 防止吞掉下一个键.

### `_normalize_status` 不变

保持现有 8 lifecycle states (`done/in_progress/approved/reviewed/active/ready/pending/archived/deprecated/unknown`). 仅扩展 raw → token 映射. "pending" 已在中文 i18n 测试用例 (`US-009 状态: pending`) 中正常匹配.

### SKILL.md §1.5 文档同步 (reframe to schema.md, 2026-04-25 implementation)

> **Implementation reframe** (per `feedback_spec_reframe_in_session.md`):
> SKILL.md v3.0.0 §1.5 已机械化简化为 "字段由 scan.py 产出, 语义见 state-snapshot-schema.md"
> (AD-SSME-6 v3.0 source-of-truth 设计). 在 SKILL.md 重新放 6 模式表会再次引入
> mechanical-mode Spec 已消除的 spec-vs-code divergence. 故文档同步落到
> **`references/state-snapshot-schema.md`** (v3.0 SoT) 而非 SKILL.md. 触点 3 处:
> (1) `_status.py` 模块 docstring 提到 i18n + Spec 名,
> (2) `state-snapshot-schema.md` 新 "Status extraction patterns" 表 + i18n note,
> (3) 本 proposal.md 此 Implementation reframe 段.

### Tests

`aria/skills/state-scanner/tests/test_requirements.py` 新增 4 cases:
1. `test_fullwidth_colon_status` — `**状态**：pending` (全角冒号)
2. `test_inline_blockquote_multi_meta` — Kairos US-009 真实样本
3. `test_inline_blockquote_status_at_end` — `> **A**: 1 | **状态**: done`
4. `test_inline_blockquote_status_in_middle` — `> **A**: 1 | **状态**: pending | **B**: 2`

## Impact

- **Affected files**: `aria/skills/state-scanner/scripts/collectors/_status.py` (regex 列表 + 新 pattern), `aria/skills/state-scanner/SKILL.md` (§1.5 文档), `aria/skills/state-scanner/tests/test_requirements.py` (4 new tests). 总改动 ~30 行.
- **Backward compatibility**: 100% — 仅添加新匹配, 原有 5 pattern 行为不变 (regex 字符类扩 `:` → `[：:]` 是超集).
- **snapshot_schema_version**: 无变更 (输出 schema 不变, 仅 raw_status 命中率提升).
- **Benchmark**: smoke benchmark 即可 (与 v1.16.x patch 同模式), 加 1-2 个 i18n eval case 验证 Status 识别率从 0% 提升到 100% (Kairos US-009).

## 非目标

- 不引入完整中文 i18n 框架 — 仅扩 Status 关键词. 其他 collector (requirements PRD raw_status, audit verdict, 等) 走相同 `_status.py` 路径, 自动受益, 不需要单独改.
- 不重写 5 现有 pattern 的语义 — pattern 6 是 **附加** 而非替换.
- 不改 `_normalize_status` 逻辑 — pending/done/active 等 token 已 case-insensitive.
- 不引入 `langdetect` 或类似第三方 i18n 库 (违反 stdlib-only AD-SSME-1).

## 验收

- [ ] `_status.py` regex 列表更新, 包含 pattern 6
- [ ] SKILL.md §1.5 文档同步 6 种模式
- [ ] 4 new test cases 全 PASS
- [ ] 现有 7 requirements 测试 全 PASS (回归零)
- [ ] Kairos `US-009` Status 识别从 `null` → `"pending"` (再跑一次 T8 dogfooding 复测)
- [ ] aria-plugin Patch 版本 bump (v1.17.2 或并入 v1.18.0)

## Out of scope (defer to future Spec)

- YAML frontmatter status: `---\nstatus: pending\n---` (Hugo/Jekyll 风格) — 若发现采用项目用此格式再立
- HTML comment status: `<!-- status: pending -->` — 罕见, 不立
- `[Status: X]` 行内方括号 — 罕见, 不立
- 状态 token 同义词扩展 (e.g. "已完成" / "进行中" / "草稿") — `_normalize_status` 已支持 "进行中" → in_progress; 其他中文同义词作为本 Spec 之外的另一独立 Spec 候选 (`state-scanner-status-token-cn`)

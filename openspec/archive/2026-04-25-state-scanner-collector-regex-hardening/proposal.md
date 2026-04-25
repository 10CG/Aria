# state-scanner-collector-regex-hardening — collector 字段提取正则鲁棒性补强

> **Level**: Minimal (Level 2 Spec — 仅 proposal.md, 无 tasks.md)
> **Status**: Complete (2026-04-25, implementation merged in aria PR #32 + Aria PR #51, released as v1.17.3)
> **Created**: 2026-04-25
> **Completed**: 2026-04-25
> **Parent Story**: (无, 跨 collector 基础设施增强)
> **Source**: 2026-04-25 主动 latent bug audit (PR #30 merge 后空闲扫描). 复合应用 v1.17.1 anchor narrowness + v1.17.2 i18n fullwidth colon 两条教训作为 lint 标准, 在 architecture.py / forgejo_config.py 命中匹配
> **Target**: aria-plugin v1.17.3 patch (与 v1.17.1 / v1.17.2 同模式 quick patch) — released
> **Estimate**: ~1.5h (3 文件 regex + 5-7 unit tests + smoke benchmark) — actual ~1.5h (matched estimate)
> **Related Feedback Memory**: `feedback_smoke_benchmark_truthiness.md`, `feedback_smoke_vs_full_ab_benchmark.md`

---

## Why

主动 latent bug audit (3 个并行 Explore agent dispatch) 复合应用近期 2 条教训:

1. **v1.17.1 教训**: `^\s*\*\*` 锚点不允许 `>` blockquote 前缀, 导致 `> **Version**: ...` 漏检 (`feedback_smoke_benchmark_truthiness.md`)
2. **v1.17.2 教训**: 半角冒号 `:` 不识别中文 IME 默认全角冒号 `：` (Spec `state-scanner-i18n-status-regex`)

**audit 1 finding (smoke truthiness)**: ✅ 全 clean — 现有测试都用 `assertTrue/assertFalse/assertIsNone`, 不再有 field-presence-only false-pass. v1.17.1 hardening 已彻底.

**audit 2 finding (anchor narrowness)** + **audit 3 finding (i18n fullwidth colon)**: 复合发现以下 collectors 仍有 latent 风险:

### 命中 1: `architecture.py` (3 patterns)

| Line | Pattern | 漏检案例 1 (anchor) | 漏检案例 2 (i18n) |
|---|---|---|---|
| 10 | `_ARCH_STATUS_PAT = r"^>?\s*\*\*Status\*\*:\s*(.+?)\s*$"` | `## Status: Active` (heading-prefixed) | `**Status**：Active` (fullwidth) |
| 11 | `_ARCH_LAST_UPD = r"^>?\s*\*\*Last Updated\*\*:\s*(.+?)\s*$"` | `## Last Updated: 2026-04-25` | `**Last Updated**：2026-04-25` |
| 12 | `_ARCH_PRD = r"^>?\s*\*\*Parent PRD\*\*:\s*(.+?)\s*$"` | `## Parent PRD: prd-v2` | `**Parent PRD**：prd-v2` |

**实际后果**: `architecture.path/status/last_updated/parent_prd` 静默 None, 进而 `chain_valid=null` 因依赖链断裂。中文项目 (Kairos / 任何中文文档为主的 adopter) 的 architecture 文档若使用全角冒号或 markdown 标题前缀, 会被静默漏检。

### 命中 2: `forgejo_config.py` (2 patterns)

| Line | Pattern | 漏检案例 |
|---|---|---|
| 42 | `_FORGEJO_YAML_KEY = r"^\s*forgejo\s*:"` | `forgejo：` (fullwidth) / `> forgejo:` (blockquote) |
| 43 | `_FORGEJO_HEADING = r"^\s*#{1,3}\s+forgejo\b"` | `> ## forgejo` (blockquote heading, 罕见但可能) |

**实际后果**: 中文用户在 CLAUDE.local.md 中写 `forgejo：` (IME 默认), `forgejo_config.config_status` 误报 `incomplete` 即便配置实际完整, 用户被误导去跑 `/forgejo-sync` 引导。

### 命中 3: `readme.py` (1 pattern)

| Line | Pattern | 漏检案例 |
|---|---|---|
| 11-12 | `_VERSION_PAT = r"^>?\s*\*\*(?:版本\|Version)\*\*[:：]\s*v?([\d.]+)"` | `## Version: v1.2.3` (heading-prefixed; i18n 已 fixed) |

**实际后果**: 仅 anchor narrowness — fullwidth colon 已经在 v1.17.1 fix 中顺手加了 `[:：]`. 若用户 README 用 `## Version: v1.2.3` 标题形式 (相对少见, 但合法), `readme.root.version` 会 None.

### audit 1 结论 (无新 finding, 仅信心 +1)

Smoke benchmark truthiness pattern 在 `test_readme.py::test_smoke_false_pass_guard` (lines 106-125) 已显式守卫, 现有 18 个 test 文件全用 value assertion, 无 `assertIn key` 漏检风险。**v1.17.1 hardening 持续有效, 不需要再补**.

## What Changes

### 通用修复模式

将 v1.17.1 + v1.17.2 教训合并为一个**通用 collector field-extractor lint rule**:

> **Field-extractor regex must accept**: `^(?:#{1,6}\s+)?\s*>?\s*\*\*<KEY>\*\*[：:]\s*<VAL>` 或更宽松 (heading prefix 可选 + blockquote prefix 可选 + 双 colon)。

### 具体改动 (3 文件)

| 文件 | Pattern 数 | 改动 |
|---|---|---|
| `architecture.py` | 3 | 加 `(?:#{1,6}\s+)?` heading 前缀 + `[：:]` 双 colon |
| `forgejo_config.py` | 2 | 加 `(?:>\s*)?` blockquote 前缀 + `[：:]` 双 colon (key) |
| `readme.py` | 1 | 加 `(?:#{1,6}\s+)?` heading 前缀 (i18n 已支持) |

### Tests

- `test_architecture.py`: 新增 6 cases (Status / Last Updated / Parent PRD × heading-prefix + fullwidth-colon)
- `test_forgejo_config.py`: 新增 2 cases (fullwidth colon + blockquote prefix)
- `test_readme.py`: 新增 1 case (heading-prefixed Version)

### schema.md 文档同步

更新 `references/state-snapshot-schema.md` 的 `architecture` / `forgejo_config` / `readme` 段落注明 heading-prefix + fullwidth-colon 双兼容, 引用此 Spec ID 作为 contract 来源。

### Smoke benchmark

10-12 case smoke benchmark, 走 v1.17.1 / v1.17.2 模式 (inline structural assertions). Full `/skill-creator` AB 不必要 (doc-dominant Level 2 patch + strong unit test 证据)。

## Impact

- **Affected files**: 3 collector .py + 3 test .py + 1 schema.md doc + 1 CHANGELOG.md. 总改动 ~50 行 + ~80 行 tests.
- **Backward compatibility**: 100% — 字符类扩展 + optional prefix 都是严格超集.
- **snapshot_schema_version**: 无变更 (输出 schema 不变, 仅各字段 raw 命中率提升)。
- **Cross-project benefit**: Kairos / 任何中文项目用 markdown 标题写 `## Status: Active` 或 `forgejo：` IME 习惯都受益 — 与 `state-scanner-i18n-status-regex` Spec 一致的跨项目可用性方向。

## 非目标

- 不做完整 markdown 解析 — 仍用 regex line-anchored 模式
- 不引入第三方 markdown 库 (违反 stdlib-only AD-SSME-1)
- 不改任何 collector 的输出 schema 字段名/语义
- 不改 `_status.py` (已在 v1.17.2 完整修复, audit 验证现 6 patterns 100% 覆盖)
- 不动 `audit.py` / `upm.py` / `interrupt.py` 等 machine-generated input collectors (audit 3 LOW-risk 段已 clear)
- 不重做 smoke benchmark assertion 框架 (audit 1 已确认无 new false-pass)

## 验收

- [ ] architecture.py 3 patterns 加 heading prefix + fullwidth colon, 6 new tests PASS
- [ ] forgejo_config.py 2 patterns 加 blockquote prefix + fullwidth colon, 2 new tests PASS
- [ ] readme.py 1 pattern 加 heading prefix, 1 new test PASS
- [ ] state-snapshot-schema.md 三段落各加 i18n note + Spec ID 引用
- [ ] 全 stdlib unittest PASS (现 362, 加 9 new tests → 371)
- [ ] 现有 9 architecture + 4 forgejo_config + 14 readme tests 零 regression
- [ ] Smoke benchmark 10-12 cases 100% PASS
- [ ] aria-plugin Patch 版本 bump v1.17.3 (与 v1.17.1 / v1.17.2 同模式)
- [ ] CHANGELOG.md [1.17.3] 段加 Why-patch + Acceptance + 引用本 Spec
- [ ] aria 子模块指针 + main repo 双远程同步

## Out of scope (defer to future Spec)

- `< Field >: value` HTML 注释隐藏字段 (罕见)
- YAML frontmatter `---\nstatus: pending\n---` (Hugo/Jekyll, 同 i18n Spec 之 Out-of-scope, 候选 `state-scanner-yaml-frontmatter-status`)
- 状态 token 中文同义词 (`已完成` / `草稿` 等) — 候选 `state-scanner-status-token-cn` (同 i18n Spec 之 Out-of-scope)
- 跨多行字段值 (`**Field**:\n  multi-line`) — 候选 `state-scanner-multiline-field-value`
- 表格列扩展到 architecture/forgejo_config/readme 等 (现仅 _status.py pattern 5 支持表格) — 候选 `state-scanner-table-field-extraction`

## Implementation Notes (preview, 未提交)

- 利用 v1.17.2 reframe 经验: 文档同步落到 `state-snapshot-schema.md` (v3.0 SoT) 而非 SKILL.md, 避免 mechanical-mode prose-vs-code divergence. 3 触点: collector docstring + schema.md + 本 proposal.md
- 利用 v1.17.1 经验: 加 anti-pattern guard test (e.g. `test_smoke_false_pass_guard` 风格) 确保未来 audit 能机械检测 anchor narrowness 复发

# Aria 2.0 M1 — Issue Schema v0.1

> **Version**: v0.1 (**breaking change permitted**, per proposal §3 escape hatch: 初版无外部消费方, M2 Hermes 集成时可调整)
> **Spec**: [aria-2.0-m1-mvp/proposal.md §What §3](../proposal.md)
> **Validator**: [validate-issue-schema.py](./validate-issue-schema.py)
> **Breaking change rule**:
>   - `issue-schema-v0.1.md` 独立豁免 (per KM-M1 escape hatch)
>   - 与 `m1-handoff.yaml` (AD-M1-7 additive-only) 治理边界分离
>   - 变更主体: M2 OpenSpec (`aria-2.0-m2-*` Spec 起草)

---

## Top-level structure

```yaml
# .aria/issues/<ID>.yaml
id: string                    # 唯一, matches filename; pattern [A-Z][A-Z0-9-]+
title: string                 # human-readable, max 120 chars
description: string           # multi-line markdown; MUST contain at least one action verb (新增|修改|删除) + 具体 file/function name (per AD-M1-3 validator)
files: [string]               # list of relative paths in target repo (context for claude)
expected_changes:
  expected_file_touched: [string]   # files that MUST be touched (non-empty); paths relative to workspace root
  expected_diff_contains: [string]  # literal substrings expected in git diff HEAD~1 + 行; non-empty for DEMO-*
ip_classification: enum       # M1: ONLY "synthetic" allowed; per AD-M1-9
metadata:
  target_repo: string         # Forgejo repo slug: "10CG/<name>"; e.g., "10CG/aria-plugin-benchmarks"
  base_branch: string         # default "master"
  created_by: string          # "human:<username>" per AD-M0-6 audit trail
  created_at: string          # RFC 3339 timestamp
```

## Field-level constraints

### `id`
- **必填**
- 正则 `^[A-Z][A-Z0-9-]+$`
- 必须与 filename 匹配 (`.aria/issues/DEMO-001.yaml` → `id: DEMO-001`)

### `title`
- **必填**
- ≤ 120 chars
- No newlines

### `description`
- **必填**
- Multi-line markdown
- **必须含 action verb** (per AD-M1-3 validator, QA F4): `新增` / `修改` / `删除` (任一)
- **必须含具体 file/function name** (降低 `CLAUDE_NO_OP` 概率)
- 示例: `"新增 src/python/utility.py 中一个 fibonacci 函数, 并在 tests/test_utility.py 新增对应测试"`

### `files`
- **必填** (可为空数组 `[]` 若 issue 自足)
- 相对 `target_repo` workspace root 路径
- Runner 在 claude prompt 中以 `${ARIA_FILES_LISTING}` 渲染

### `expected_changes.expected_file_touched`
- **必填**
- Non-empty 数组
- Literal paths (non-glob), relative to workspace root
- Validator (T3.1.2) 保证至少 1 项

### `expected_changes.expected_diff_contains`
- **必填** (per AD-M1-3 + BA-R2-I1)
- Non-empty literal 子串数组
- **匹配语义**: literal substring (非 regex, per QA-C1-PARTIAL)
- **匹配范围**: `git diff HEAD~1 --unified=0` 的 `+` 行 (per QA-N1)
- **过滤**: diff header `+++  b/path` 行在匹配前剔除 (per AI-R1-4)
- **DEMO-001/002 均纯增量**, 不涉及 `-` 行匹配 (v0.1 限制)

### `ip_classification`
- **必填**
- Enum: `synthetic` | `trivial-real` | `real`
- **M1 validator 强制**: 只接受 `synthetic` (per AD-M1-9, v0.1 M1 锁定)
- M2+ 解禁 `trivial-real` / `real` 需: external legal counsel review + PRD patch + AD-M2-X

### `metadata.target_repo`
- **必填**
- 格式 `<org>/<repo>` (Forgejo slug)
- DEMO-001/002 目标: `10CG/aria-plugin-benchmarks` (M1 fixture repo in M0-established path)

### `metadata.base_branch`
- **可选**
- 默认 `master`

### `metadata.created_by`
- **必填**
- 格式 `human:<username>` 或 `ai:<agent-name>` (per AD-M0-6 audit trail)

### `metadata.created_at`
- **必填**
- RFC 3339 timestamp with UTC offset

---

## Example (DEMO-001 synthetic trivial)

```yaml
id: DEMO-001
title: "[M1 MVP DEMO-001] Update fixture README timestamp line"
description: |
  修改 `aria-plugin-benchmarks/ab-suite/m1-mvp/fixtures/README.md` 最后一行
  的签字 timestamp (从当前日期改为当日 YYYY-MM-DD).

  这是管道连通验证场景, 目的是证明 aria-runner 容器能完成
  dispatch → claude execution → git commit → Forgejo PR 闭环.
files:
  - aria-plugin-benchmarks/ab-suite/m1-mvp/fixtures/README.md
expected_changes:
  expected_file_touched:
    - aria-plugin-benchmarks/ab-suite/m1-mvp/fixtures/README.md
  expected_diff_contains:
    - "Signed-by: human:simonfish"
ip_classification: synthetic
metadata:
  target_repo: "10CG/Aria"
  base_branch: master
  created_by: "ai:aria-agent @ 2026-04-18"
  created_at: "2026-04-18T00:00:00Z"
```

---

## Non-goals (v0.1)

- 多 repo cross-repo changes (v0.1 单 repo)
- 删除/重命名 assertion (v0.1 仅 `+` 行; M2 扩展 `-` / rename)
- Nested expected_changes conditions (v0.1 扁平 AND 语义)
- Issue 依赖图 (DEMO 间的 prerequisite) — 不在 v0.1 范围
- Real IP classification (v0.1 仅 synthetic, M2+ 按 AD-M1-9 治理)

---

## Version history

| Version | Date | Changes |
|---------|------|---------|
| v0.1 | 2026-04-18 | Initial draft for M1 MVP. DEMO-001/002 consumed fields. `expected_file_touched` + `expected_diff_contains` 早锁 (per AD-M1-3 + BA-R2-I1). `ip_classification=synthetic` 强制 (per AD-M1-9). Action verb required (per QA-F4). |

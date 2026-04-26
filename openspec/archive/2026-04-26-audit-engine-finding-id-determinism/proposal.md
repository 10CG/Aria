# audit-engine-finding-id-determinism

> **Level**: Minimal (Level 2 Spec — 仅 proposal.md, 无 tasks.md)
> **Status**: Complete (2026-04-26, archived per Level 2 micro-Spec convention)
> **Created**: 2026-04-26
> **Completed**: 2026-04-26 (aria-plugin PR #34 merged, commit e168cb7; bundled with audit-engine-zero-finding-stability-gate as v1.17.5 sister-bug release)
> **Type**: doc-only Skill prompt 规范化 (audit-engine SKILL.md 哈希函数)
> **Source**: Round-2 latent-bug audit catalog P1.3 (`openspec/archive/2026-04-25-round-2-latent-bug-audit-findings/proposal.md` 第 80-87 行)
> **Related Spec**: `audit-engine-report-filename-uniqueness` (v1.17.4 已落地, 同 audit-engine 子系统 sister-bug)
> **Related Memory**: `feedback_audit_convergence_pattern.md` (R_N == R_{N-1} 严格定义), `feedback_multi_agent_audit_insights_2026-04-24.md` (跨轮 ID title-invariant)

---

## Why

audit-engine SKILL.md 第 226 行 finding 结构化记录:

```json
{
  "id": "auto-generated-hash",
  ...
}
```

**问题**: "auto-generated-hash" 是 prose 占位符, 未规范哈希函数输入. 实际 LLM agent 在生成 finding 时:
- 不同 agent 报相同 finding (按 4-tuple `(type, severity, category, scope)` 等价) 但 `id` 不同 → 跨轮 `R_N == R_{N-1}` 收敛比较失败 → 永远无法收敛
- 或同 agent 在 R1 / R2 报相同 finding 但 timestamp/序号污染 hash → 收敛误判

**为何关键**: `convergence-algorithm.md` 第 28-42 行 4-tuple comparison_key 集合比较是机械收敛的 SoT, 但 `id` 字段虽然不参与 comparison_key (按文档明示), prose 中仍有部分 audit 报告样本把 `id` 作为 cross-reference (e.g. R1-I3 fix references R0-I3). 若 id 不稳定, audit-driven fix conventions (`feedback_audit_driven_fix_conventions.md`) 的 inline `R<N>-<ID> fix:` 注释链路断裂.

**Verifiability**: MEDIUM — Round-2 audit catalog 标注 (P1.3 Risk: 收敛不能机械判定, 依赖 AI prose 共识), 需读实际 audit 报告样本验证 ID 是否真 hash 还是 random.

**为何与 P0.2 sister-bug**: 都是 audit-engine 子系统的"机械确定性"补强 (P0.2 文件名 uniqueness; P1.3 finding ID determinism), 都是 doc-only 改动, 都不引入 script 变更. 适合 sister-bug bundling.

---

## What

### 改动 1: SKILL.md finding ID 规范化

**File**: `aria/skills/audit-engine/SKILL.md` 第 220-233 行 "结论记录" 章节

**当前**:
```json
{
  "id": "auto-generated-hash",
  ...
}
```

**改为**:
```json
{
  "id": "<sha256(category + ':' + scope + ':' + severity + ':' + type)[:8]>",
  ...
}
```

并在 JSON 后追加规范段落:

```markdown
**`id` 字段哈希规范** (mechanical determinism):

```python
import hashlib
def finding_id(category: str, scope: str, severity: str, type: str) -> str:
    canonical = f"{category}:{scope}:{severity}:{type}"
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:8]
```

**输入字段** (与 4-tuple comparison_key 对齐, 顺序固定):
1. `category` (architecture | implementation | testing | documentation)
2. `scope` (affected module or file path)
3. `severity` (critical | major | minor)
4. `type` (decision | issue | risk)

**输入字段不包括**: `summary` (LLM 措辞每轮不同, 哈希污染), `timestamp` (轮次间漂移),
`agent_role` (跨 agent 同 finding 应同 ID).

**输出**: 8 字符 hex prefix (e.g. `a3f2c9b1`), 足够 4-tuple 笛卡尔积去重 (~10^4 量级远低于 16^8).

**为何 SHA-256**: 跨语言/跨 agent 可复现 (Python stdlib + JS crypto + LLM 心算近似都能产生一致结果);
truncate to 8 chars 兼顾可读性 (报告文件名 + inline fix 引用 `R1-a3f2c9b1`).

**跨轮稳定性保证**:
- 同一 finding 在 R1 / R2 / RN 由不同 agent 报告 → 同 8-char ID
- finding 升级 severity (minor → major) → ID 改变 (符合 4-tuple comparison_key 不收敛逻辑)
- finding 改 category/scope → ID 改变 (设计如此, 表示语义变化)
```

### 改动 2: convergence-algorithm.md 引用同步

**File**: `aria/skills/audit-engine/references/convergence-algorithm.md` 第 28-42 行 (comparison_key 章节)

在 "为何排除 summary" 段落后追加:

```markdown
**`finding.id` 与 comparison_key 的关系**:

`finding.id = sha256(category:scope:severity:type)[:8]` 是 comparison_key 的
**确定性投影**, 两者同步: 4-tuple 相等 ⇔ ID 相等.

这意味着:
- 集合比较可用 ID 集合 (更快, O(N) 哈希查找) 或 4-tuple 集合 (更显式) 任选其一
- 跨 agent 报相同 finding → 同 ID, 不重复计数
- audit-driven fix inline 注释 `R1-a3f2c9b1 fix: ...` 跨轮稳定可追溯
```

### 改动 3: report-format.md (如存在 ID 引用)

**File**: `aria/skills/audit-engine/references/report-format.md`

如该文件包含 finding ID 示例, 同步更新示例值为 8-char hex (`a3f2c9b1` 等), 防止文档样本误导.

---

## 非目标

- 不实施 Python 工具脚本 (audit-engine 是 LLM-driven Skill, agent 按文档规范心算或在 prose 中明示 hash 输入即可)
- 不改 4-tuple comparison_key 定义 (`convergence-algorithm.md` 第 22-26 行不变)
- 不引入新 finding 字段 (id 字段已存在, 仅规范化生成)
- 不影响 v1.17.4 文件名 schema (R{round}-{spec_id}-{agent_role} 与 finding ID 独立)

## 验收

- [ ] `aria/skills/audit-engine/SKILL.md:226` finding ID 规范化 + 哈希函数文档
- [ ] `convergence-algorithm.md` comparison_key 章节追加 ID 与 4-tuple 关系段落
- [ ] `report-format.md` (如存在 ID 示例) 同步更新
- [ ] smoke benchmark: 4 输入样本验证 hash 输出确定性 (Python stdlib 计算)
- [ ] 与 P2.3 (audit-engine-zero-finding-stability-gate) sister-bug bundling 合并, 走 v1.17.5 patch
- [ ] merge 后立即归档

## 价值

- **机械收敛闭环**: 4-tuple comparison_key 与 finding.id 等价, 收敛比较两种方式都正确
- **跨轮可追溯性**: `R1-a3f2c9b1 fix:` 注释跨 R1→R2→R3 稳定 (同 finding 同 ID)
- **跨 agent 去重**: 4 个 agent 同时报相同 finding → 同 ID, 不会被误算 4 次重复

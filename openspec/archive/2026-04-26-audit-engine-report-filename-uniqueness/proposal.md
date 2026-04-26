# audit-engine-report-filename-uniqueness

> **Level**: Minimal (Level 2 Spec — 仅 proposal.md, 无 tasks.md)
> **Status**: Complete (2026-04-26, archived per Level 2 micro-Spec "merge 后立即归档" convention)
> **Created**: 2026-04-25
> **Completed**: 2026-04-26 (aria-plugin PR #33 merged, commit 843e435; bundled with requirements-validator-status-i18n-alignment as v1.17.4 sister-bug release)
> **Type**: 单文件 doc 改动 (audit-engine SKILL.md 文件名生成规则)
> **Source**: Round-2 latent-bug audit catalog P0.2 (`openspec/archive/2026-04-25-round-2-latent-bug-audit-findings/proposal.md` 第 50-57 行)
> **Related Memory**: `feedback_audit_convergence_pattern.md` (4-agent 并行 dispatch 模式), `feedback_audit_driven_fix_conventions.md` (报告文件命名约定)

---

## Why

`audit-engine` 当前文件名生成规则:

```
.aria/audit-reports/{checkpoint}-{timestamp}.md
```

(SKILL.md:429)

**实际生产样本**: 历史 audit 报告时间戳粒度仅到分钟 (`T2030Z` `T2200Z`), 部分到秒. 在 `convergence` / `challenge` 两种模式下, audit-engine 会**并行 dispatch 4 个 agent** (qa-engineer / code-reviewer / backend-architect / tech-lead), 它们的输出几乎在同一秒/分钟内写盘.

**风险**:
- 4-agent strict 模式同分钟 wall-clock → 文件名碰撞 → 后写覆盖前写
- 部分 agent 输出永久丢失, audit-engine convergence 判定 (`R_N == R_{N-1}` 比较) 缺少完整 finding 集
- 表现为"agent X 找到的 finding 在最终报告中消失"的间歇性 bug, 难以复现 (因 wall-clock 时序)

**为何不直接修**:
- 文件名 schema 改动会影响 audit-engine 的 finding aggregation 逻辑 (扫描 `.aria/audit-reports/` 时如何按 round 分组)
- 需要文档化新的 schema, 让消费者 (state-scanner Phase 1.10, history-tooling) 知道如何 parse
- 需要向后兼容历史报告 (旧文件名仍能被读取)

**Verifiability HIGH**: `grep -r "audit-reports/{" aria/skills/audit-engine/` 已确认无微秒/计数器后缀, 是真实 gap 不是 prose-only 描述.

---

## What

### 文件名 Schema 改动

**File**: `aria/skills/audit-engine/SKILL.md` 第 429 行

**当前**:
```
.aria/audit-reports/{checkpoint}-{timestamp}.md
```

**新规范**:
```
.aria/audit-reports/{checkpoint}-R{round}-{timestamp_ms}-{spec_id}-{agent_role}.md
```

**字段定义**:

| 字段 | 来源 | 示例 |
|---|---|---|
| `{checkpoint}` | audit-engine config | `pre_merge`, `post_spec` |
| `{round}` | audit-engine 内部计数器 | `R1`, `R2`, `R3` |
| `{timestamp_ms}` | UTC 毫秒精度 ISO 8601 (无 `:` 因文件系统兼容) | `2026-04-25T220340-123Z` |
| `{spec_id}` | OpenSpec change_id (从 dispatch context) | `audit-engine-report-filename-uniqueness` |
| `{agent_role}` | 4-agent fixed roster | `qa-engineer`, `code-reviewer`, `backend-architect`, `tech-lead` |

**示例完整文件名**:
```
.aria/audit-reports/pre_merge-R1-2026-04-25T220340-123Z-audit-engine-report-filename-uniqueness-qa-engineer.md
```

**碰撞防护**:
- `agent_role` 区分 4 个并行 agent (即使同毫秒落盘也不冲突)
- `timestamp_ms` 毫秒精度 (1ms 内 4 个文件并行写, agent_role 兜底)
- `R{round}` 区分多轮收敛 (R1 vs R2 不冲突)
- `{spec_id}` 区分多个 Spec 共享同一 round 时的 audit 报告

### 向后兼容

**历史报告 reader 行为**:
- audit-engine 扫描 `.aria/audit-reports/*.md` 时, 同时接受新旧两种 schema
- 旧文件名 `{checkpoint}-{timestamp}.md` (无 round/role) 视为单 agent 单轮输出 (R1, role=`legacy`)
- finding aggregation 时 legacy 文件归入 R1, 与新 R1 文件并集

**writer 行为 (audit-engine 实例)**:
- 仅生成新 schema 文件 (不再回写旧格式)
- 切换日期: 本 Spec 合并即生效

### Reference 文档更新

`aria/skills/audit-engine/references/convergence-algorithm.md` (如存在) 同步更新文件名引用; finding-aggregation 章节明确"按 R{round} 分组"逻辑。

---

## 非目标

- 不改 finding ID 哈希算法 (P1.3 独立 Spec `audit-engine-finding-id-determinism` 处理)
- 不改 verdict 计算逻辑 (PASS/PASS_WITH_WARNINGS/FAIL 不变)
- 不改 4-agent fixed roster 名单 (沿用 qa-engineer / code-reviewer / backend-architect / tech-lead)
- 不改 challenge mode serial flow (仅文件名 schema)

## 验收

- [ ] `aria/skills/audit-engine/SKILL.md:429` 文件名 schema 更新
- [ ] 新增 reference 章节文档化 `{round}-{timestamp_ms}-{spec_id}-{agent_role}` 4 字段语义
- [ ] 向后兼容声明: 旧文件名作为 R1/legacy 仍能被 reader 处理
- [ ] smoke benchmark: 准备 4 agent 并行 dispatch 样本 (mock), 验证文件名互不冲突
- [ ] 与 P0.1 (requirements-validator-status-i18n-alignment) sister-bug bundling 合并, 走 v1.17.4 patch
- [ ] merge 后立即归档

## 价值

- **机械收敛保证**: audit-engine 4-agent 并行不再丢 finding, `R_N == R_{N-1}` 比较基础完整
- **追溯性**: 文件名直接编码 spec_id + agent_role, 跨 session debug 不需要打开文件读 frontmatter
- **mechanical-mode 一致**: 与 `feedback_audit_driven_fix_conventions.md` 提倡的 inline `R<N>-<ID> fix:` 命名约定对齐

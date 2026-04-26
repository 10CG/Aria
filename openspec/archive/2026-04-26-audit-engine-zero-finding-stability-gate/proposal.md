# audit-engine-zero-finding-stability-gate

> **Level**: Minimal (Level 2 Spec — 仅 proposal.md, 无 tasks.md)
> **Status**: Complete (2026-04-26, archived per Level 2 micro-Spec convention)
> **Created**: 2026-04-26
> **Completed**: 2026-04-26 (aria-plugin PR #34 merged, commit e168cb7; bundled with audit-engine-finding-id-determinism as v1.17.5 sister-bug release; **P2.3 spike-verified real bug**)
> **Type**: 单文件 doc 改动 (audit-engine convergence-algorithm.md 边界条件)
> **Source**: Round-2 latent-bug audit catalog P2.3 (`openspec/archive/2026-04-25-round-2-latent-bug-audit-findings/proposal.md` 第 105-110 行) — 2026-04-26 spike verified ✓
> **Spike Result**: 真 bug 验证 (line 48 与 memory 教训冲突)
> **Related Memory**: `feedback_audit_convergence_pattern.md` (R_N == R_{N-1} 严格定义 + 首个 0-finding 轮后需稳定性确认轮), `project_premerge_iteration_pattern.md` (pre_merge 严格收敛需稳定性确认轮)

---

## Why (Spike 已 verify, 非 prose 推测)

`aria/skills/audit-engine/references/convergence-algorithm.md` 第 48 行边界条件表:

```markdown
| 情况 | 处理 |
|------|------|
| Round 1 (无上一轮) | 无法判定收敛, 必须进入 Round 2 |
| 空结论集 (两轮都无结论) | 视为收敛 (没有问题 = 共识一致) |
| 单元素差异 | 不收敛 (严格集合相等) |
| severity 升级 (minor→major) | 不收敛 (severity 参与比较) |
```

**问题**: 第 2 行 "空结论集 (两轮都无结论) | 视为收敛" 与 memory 中的实战教训冲突.

**memory `feedback_audit_convergence_pattern.md`** (3x 验证的 invariant):

> 5 轮 multi-agent pre_merge audit 收敛模式: R_N == R_{N-1} 严格定义 + **首个 0-finding 轮后需稳定性确认轮**. 成功样本: aria-plugin v1.16.0 trajectory 24→2→1→0→0

**memory `project_premerge_iteration_pattern.md`**:

> pre_merge 严格收敛 (Round N == Round N-1) 需要一个"稳定性确认轮" 证明 0 findings 稳定, **不能在首个 0-finding 轮直接声称收敛**

**冲突**: 当前文档允许 R1 = ∅ + R2 = ∅ 直接收敛 (2 轮即停), 但实战教训要求 R1 = ∅ 后必须再多一轮 R2 = ∅ 作为 *stability confirmation*, 即至少 3 轮才能在 0-finding 状态下声称收敛.

**Risk**: agent 第 1 轮可能因 prompt 解析失败 / context truncation / 启动温度漂移导致**假阴性**(0 findings 但其实有 finding); 第 2 轮在相同 LLM session 下惯性产出同样 0 findings, 给出"虚假共识". 必须有第 3 轮稳定性轮 (新 LLM context) 验证 0-finding 稳定.

**Verifiability**: HIGH ✓ (2026-04-26 spike: grep + diff 已确认文档与 memory 不一致)

**为何与 P1.3 sister-bug**: 都是 audit-engine convergence 子系统的"机械确定性"补强 (P1.3 ID hash; P2.3 stability gate); 都是 doc 改动; 都是 v1.17.5 patch 节奏的自然延伸.

---

## What

### 改动: convergence-algorithm.md 边界条件修订

**File**: `aria/skills/audit-engine/references/convergence-algorithm.md` 第 44-52 行边界条件表

**当前**:
```markdown
### 边界情况

| 情况 | 处理 |
|------|------|
| Round 1 (无上一轮) | 无法判定收敛, 必须进入 Round 2 |
| 空结论集 (两轮都无结论) | 视为收敛 (没有问题 = 共识一致) |
| 单元素差异 | 不收敛 (严格集合相等) |
| severity 升级 (minor→major) | 不收敛 (severity 参与比较) |
```

**新版**:
```markdown
### 边界情况

| 情况 | 处理 |
|------|------|
| Round 1 (无上一轮) | 无法判定收敛, 必须进入 Round 2 |
| Round 1 = ∅ (首个 0-finding 轮) | **不视为收敛**, 必须进入 Round 2 作 stability confirmation |
| Round N = ∅ ∧ Round N-1 = ∅ ∧ N >= 2 | 视为收敛 (双轮稳定性确认) |
| 单元素差异 | 不收敛 (严格集合相等) |
| severity 升级 (minor→major) | 不收敛 (severity 参与比较) |

**首轮 0-finding 必须 stability confirmation** (本规则于 v1.17.5 引入, 修复 latent bug):

经验来源: `aria-plugin v1.16.0` 实战 trajectory `24→2→1→0→0` — R5=∅ 后**仍跑 R6=∅** 才声称收敛.
若 R5 直接 stop, 风险是 agent 在 R5 因 context 问题假阴性 0 finding, 错过真 bug.

**机械实现**:
- audit-engine 在判定 `current_set == previous_set` 后, 增加守卫: 若 current_set = ∅, 至少需 2 轮历史 (round_number >= 2) + 上一轮也 = ∅
- 等价表达: `converged = (current_set == previous_set) AND (current_set != ∅ OR round_number >= 2)`
- Round 2 = ∅ 后仍 stop (因 round_number >= 2 满足), 但 Round 1 = ∅ 后**强制进入 Round 2** (stability gate)
```

### 改动 2: SKILL.md 摘要更新 (如有引用)

如 `aria/skills/audit-engine/SKILL.md` 有 prose 摘要描述"两轮无结论即收敛", 同步更新为"首轮 0-finding 必须 stability confirmation".

---

## 非目标

- 不改 4-tuple comparison_key 定义
- 不改非空结论集的收敛判定 (`current_set == previous_set` 仍然适用)
- 不引入新轮数上限 (max_rounds 配置不变)
- 不影响 challenge 模式的 objection 处理逻辑

## 验收

- [ ] `convergence-algorithm.md` 边界条件表更新, 加 stability gate 行
- [ ] 机械实现等价表达式落地
- [ ] 经验来源段落引用 v1.16.0 trajectory
- [ ] SKILL.md prose 摘要 (如有) 同步
- [ ] smoke benchmark: 模拟 R1=∅ → 应继续 R2 (不收敛); R1=∅ ∧ R2=∅ → 收敛
- [ ] 与 P1.3 (audit-engine-finding-id-determinism) sister-bug bundling 合并, 走 v1.17.5 patch
- [ ] merge 后立即归档

## 价值

- **消除假阴性收敛**: agent context 异常导致首轮 0-finding 不再被错误信任
- **memory 教训机械化**: `feedback_audit_convergence_pattern.md` + `project_premerge_iteration_pattern.md` 实战经验从 prose 转为文档化算法约束
- **与 v1.16.0 实战对齐**: 文档现在描述实际收敛 trajectory (24→2→1→0→0), 不是简化模型

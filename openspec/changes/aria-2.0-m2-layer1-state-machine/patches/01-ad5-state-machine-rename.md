# Patch 1: AD5 状态机命名 9 → 10 (per OD-1)

> **Target**: `aria-orchestrator/docs/architecture-decisions.md` AD5 (line 395-459)
> **Trigger**: brainstorm OD-1 锁定 PRD §M2 命名权威, AD5 line 399 + 451-453 同步 patch
> **Status**: Phase A.1.3 起草; T16.3 实施 commit
> **Approver**: tech-lead (T16 co-sign 阶段)

## 变更 1: AD5 line 395-399 标题 + 决策正文

### BEFORE

```markdown
## AD5 — 状态机 9 states + S_FAIL 兜底

### 决策

Layer 1 任务生命周期由一个 **9 正常状态 + S_FAIL 全局兜底** 的有限状态机建模。9 正常状态: `S0_SCANNING → S1_TRIAGED → S2_DISPATCHED → S3_RUNNING → S4_COMPLETED → S5_REVIEWING → S6_REVIEW_PASSED → S7_AWAITING_MERGE → S8_DONE`。S_FAIL 作为 universal sink, 可从任意状态进入, 并触发 replay / retry / escalate 决策。
```

### AFTER

```markdown
## AD5 — 状态机 10 states + S_FAIL 兜底

> **Revised 2026-04-28** (US-022 brainstorm OD-1): 命名从 `S0_SCANNING…S8_DONE` 重命名为 PRD §M2 既有 `S0_IDLE…S9_CLOSE` (10 状态), 与 PRD §M2 line 162-173 对齐。本次 revision 不改变状态机语义 (仍是 normal + S_FAIL universal sink), 仅命名词典切换。原命名 (S0_SCANNING…S8_DONE) 已永久作废。

### 决策

Layer 1 任务生命周期由一个 **10 正常状态 + S_FAIL 全局兜底** 的有限状态机建模。10 正常状态 (per PRD §M2): `S0_IDLE → S1_SCAN → S2_DECIDE → S3_BUILD_CMD → S4_LAUNCH → S5_AWAIT → S6_REVIEW → S7_HUMAN_GATE → S8_MERGE → S9_CLOSE`。S_FAIL 作为 universal sink, 可从任意状态进入, 并触发 replay / retry / escalate 决策。

**约定偏离声明**: 状态命名采用 SCREAMING_SNAKE_with_underscore (例 `S0_IDLE`), 偏离 Aria/OpenSpec snake_case 约定。OD-1 锁定保留, 因 PRD v2.1 §M2 已 owner approved 并广泛引用。Frozen architecture decision precedence over convention purity (R3-OBJ-3 已记录)。
```

## 变更 2: AD5 line 451-453 风险表 mapping 重算

### BEFORE

```markdown
| 1 | 9 状态 transition table 维护成本 | 中 | transition 规则写入 `standards/autonomous/state-machine.md` (US-026), 代码生成 table, 单元测试覆盖所有合法/非法 transition |
| 2 | S_FAIL 的 retry 决策复杂 (何时 retry / 何时 escalate) | 中 | 决策规则另立 AD (M2 期间) + 人类兜底 |
| 3 | POC 5 状态与生产 9 状态的迁移成本 | 低 | POC 代码仅 286 LoC, 改写为 9 状态约 100-200 LoC 增量 |
```

### AFTER

```markdown
| 1 | 10 状态 transition table 维护成本 | 中 | transition 规则写入 `standards/autonomous/state-machine.md` (US-026), 代码生成 table, 单元测试覆盖所有合法/非法 transition |
| 2 | S_FAIL 的 retry 决策复杂 (何时 retry / 何时 escalate) | 中 | 决策规则推 US-023 M3 (M3-1 自动 retry policy + M3-2 reconciler), M2 仅记录 reason enum 不重试 (per OD-2 弱形式 + brainstorm M3 deferrals) |
| 3 | POC 5 状态与生产 10 状态的迁移成本 | 低 | POC 代码仅 286 LoC, 改写为 10 状态约 150-275 LoC 增量 (relative to 9 状态版本上调 ~25%, 因新增 S9_CLOSE 归档状态 + 5 个细分自然边界, 详见 US-022 Spec §What 一 mapping 表) |
```

## 变更 3: AD5 line 411-439 Alternatives Considered 段同步更新

### BEFORE (相关引用)

```markdown
#### Option A — 5 状态 (POC 简化版) (拒绝)

`PENDING → RUNNING → REVIEWING → MERGED / FAILED`, 状态数最小化。
```

### AFTER (相关引用, 加注 cross-ref)

```markdown
#### Option A — 5 状态 (POC 简化版) (拒绝)

`PENDING → RUNNING → REVIEWING → MERGED / FAILED`, 状态数最小化。

> **POC ↔ M2 mapping** (per US-022 Spec §What 一): POC 5 状态在 M2 10 状态中的对照详见 [aria-2.0-m2-layer1-state-machine/proposal.md](../../../openspec/changes/aria-2.0-m2-layer1-state-machine/proposal.md) §What 一 "M0 Spike POC → M2 状态映射" 表。
```

## 变更 4: AD5 line 401-409 背景段瞬态描述更新

### BEFORE

```markdown
- Nomad dispatch **已发**但 alloc **未就绪**的瞬态 (S2)
- Layer 2 **完成**但 review **未开始**的瞬态 (S4)
- Review **通过**但 merge **未执行**的瞬态 (S6)
- Human gate **等待签字**的瞬态 (S7)
```

### AFTER (状态名重命名)

```markdown
- Nomad dispatch **已发**但 alloc **未就绪**的瞬态 (S4_LAUNCH → S5_AWAIT)
- Layer 2 **完成**但 review **未开始**的瞬态 (S5_AWAIT → S6_REVIEW)
- Review **通过**但 merge **未执行**的瞬态 (S6_REVIEW → S8_MERGE, 经 S7_HUMAN_GATE)
- Human gate **等待签字**的瞬态 (S7_HUMAN_GATE)
- 归档完成的明确终态 (S9_CLOSE, 区别于失败终态 S_FAIL)
```

## 变更 5: AD5 line 455-459 回滚路径段更新

### BEFORE

```markdown
- **Level 1**: 合并瞬态 S2/S4/S6 为占位标志 (不影响外部接口), 降级为 6 状态
- **Level 2**: 完全回退到 POC 5 状态, 牺牲 reconciler 精度
- **Level 3**: 放弃状态机, 退化为人类手动追踪 (R8 CLI-only 模式)
```

### AFTER (状态名重命名)

```markdown
- **Level 1**: 合并瞬态 S4_LAUNCH/S5_AWAIT/S6_REVIEW 为占位标志 (不影响外部接口), 降级为 7 状态
- **Level 2**: 完全回退到 POC 5 状态, 牺牲 reconciler 精度
- **Level 3**: 放弃状态机, 退化为人类手动追踪 (R8 CLI-only 模式)
```

## 实施清单 (T16.3)

- [ ] line 395-399 替换为 AFTER 1
- [ ] line 401-409 (瞬态描述) 替换为 AFTER 4
- [ ] line 411-439 Option A 段加 POC↔M2 mapping cross-ref (AFTER 3)
- [ ] line 451-453 风险表替换为 AFTER 2
- [ ] line 455-459 回滚路径替换为 AFTER 5
- [ ] commit message: `docs(ad5): rename state machine 9→10 states per US-022 OD-1, align with PRD §M2`

## 影响

- **AD5 是 frozen architecture decision**: 此 patch 是 OD-1 (owner 仲裁) 的合规执行, 非自由修改
- **Cross-ref 影响**: 任何引用 `S0_SCANNING / S1_TRIAGED / S2_DISPATCHED / ...` 的下游文档需同步 (US-026 文档体系工时已含 audit)
- **POC 代码不需改**: 286 LoC POC 仍按原 5 状态, 不强制升级到 AD5 命名 (POC 是 spike artifact, 已归档)

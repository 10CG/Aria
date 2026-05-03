# Patch 2: PRD §M2 标题修正 9→10 (per OD-1)

> **Target**: `docs/requirements/prd-aria-v2.md` §M2 line 159
> **Trigger**: brainstorm OD-1 锁定 PRD §M2 命名 (10 状态), 但 PRD §M2 line 159 标题写 "9 states" 与 line 162-173 列出的 10 状态自相矛盾 (R1 cm OBJ-2 发现)
> **Status**: Phase A.1.3 起草; T16.3 实施 commit
> **Approver**: owner (T16 sign-off 阶段)

## 变更: line 159 标题修正

### BEFORE

```markdown
#### 1. Layer 1 状态机 (9 states + S_FAIL)
```

### AFTER

```markdown
#### 1. Layer 1 状态机 (10 states + S_FAIL)
```

## 实施清单 (T16.3)

- [ ] PRD v2 line 159 单行替换 (1 字符 9→10)
- [ ] PRD §版本历史段 (如有) 添加 entry: `2026-04-28 — 修正 §M2 line 159 状态数 9→10, 对齐 line 162-173 实际列出的 10 状态 (per US-022 brainstorm OD-1)`
- [ ] commit message: `docs(prd): fix §M2 state count 9→10 to match listed states (US-022 OD-1)`

## 验证

修正后, PRD §M2 同时满足:
- line 159 标题声明 = "10 states + S_FAIL"
- line 162-173 实际列出 10 状态 (S0_IDLE → S9_CLOSE) + S_FAIL
- 与 AD5 patch 1 (10 states + S_FAIL) 一致
- 与 US-022 Spec (本目录 proposal.md) 一致

## 影响

- **极小变更**: 1 字符替换, 无语义改变
- **修复自相矛盾**: PRD line 159 vs 162-173 的内部冲突消除
- **无下游连锁**: 没有其他文档引用 line 159 标题字面文字 (确认: grep "9 states" prd-aria-v2.md 后仅 line 159 一处命中)

## R1 OBJ-2 (cm) 闭合

此 patch 为 R1 context-manager OBJ-2 (PRD §M2 self-bug, 标题 9 但列 10) 的最终闭合。

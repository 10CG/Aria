# Patch 3: US-022 验收 B 降级 + §不在范围 reframe (per OD-2)

> **Target**: `docs/requirements/user-stories/US-022.md` line 78 + line 87
> **Trigger**: brainstorm OD-2 锁定验收 B 降级为 WAL+重启可读弱形式; line 87 §不在范围 reframe 同步说明 reconciler 推 M3
> **Status**: Phase A.1.3 起草; T16.3 实施 commit
> **Approver**: owner (T16 sign-off 阶段, OD-2 owner 已仲裁)

## 变更 1: 验收标准 B 降级 (line 78)

### BEFORE

```markdown
- **B.** SQLite 状态机持久化通过 crash recovery 测试 (kill alloc + 重启可恢复)
```

### AFTER

```markdown
- **B.** SQLite WAL 持久化 + 进程重启后状态可读 + 不丢已 dispatched 记录 (M2 弱形式, per brainstorm OD-2 2026-04-27); **不要求**: 完整 reconciler / replay / orphan alloc 清扫 / crash-mid-transition recovery (这些推 M3-2, US-023)
```

## 变更 2: §不在范围 reconciler 项 reframe (line 87)

### BEFORE

```markdown
- **Crash recovery + Replay + Reconciler** → US-023 (M3, 80h)
```

### AFTER

```markdown
- **Crash recovery 完整 reconciler + Replay + 主动 orphan 清扫** → US-023 (M3, 80h); **M2 仅做 WAL persist 弱形式** (per OD-2 验收 B 降级), reconciler/replay/orphan 清扫推 M3-2 (~30h, brainstorm M3 deferrals)
```

## 实施清单 (T16.3)

- [ ] line 78 单行替换 (验收 B 降级措辞)
- [ ] line 87 单行替换 (§不在范围 第一条 reframe)
- [ ] US-022 §版本历史 / footer 添加 entry: `2026-04-28 — 验收 B 降级为 WAL 弱形式 + §不在范围 reframe (per US-022 brainstorm OD-2 + Spec aria-2.0-m2-layer1-state-machine 配套)`
- [ ] commit message: `docs(us-022): reframe acceptance B (WAL weak form) + scope (M3 reconciler) per OD-2`

## 验证

修正后, US-022 验收 B 与 §不在范围 line 87 自相一致:
- 验收 B 仅要求 WAL persist + 重启可读, 与 §不在范围 "完整 reconciler 推 M3" 不矛盾 (R1 qa+cr OBJ-1 闭合)
- 与 brainstorm conclusion §17 OD-2 决议一致
- 与 Spec proposal.md §What 七 Acceptance B 一致
- 与 Spec proposal.md §Out of Scope M3-2 deferral 一致

## 影响

- **小改动**: 2 行替换 (line 78 + line 87)
- **关键意义**: R1 跨 agent (qa OBJ-1 + cr OBJ-8) 同时发现的 critical 内部矛盾彻底消除
- **owner action 已完成**: OD-2 owner 已仲裁 (2026-04-27 brainstorm), 此 patch 是仲裁结果的形式落地

## R1 OBJ-1 (qa+cr) 闭合 + R3 OBJ-X 关联

- **R1 qa OBJ-1**: Spec 内部矛盾 (验收 B vs §不在范围) → **此 patch 闭合**
- **R1 cr OBJ-8**: 同上 → **此 patch 闭合**
- **R3 cr R3-OBJ-X (forward ref)**: 若未来 audit 发现此 patch 未实施, 将 raise 同 finding

## 时机决策依据 (per OD-4)

按 OD-4 + brainstorm `phase_a1_outputs_expected`, 此 patch 在 Phase A.1.3 (现阶段) 起草内容, T16.3 实施期 commit + merge。Patch 不在 brainstorm 阶段直接 commit (避免 brainstorm 越权改 owner-approved 文档)。

# neg2 trial 1 — arm_B v1.17.7 + T5 fallback

**Fixture**: `/tmp/state-scanner-bench-fixture-neg2`
**Snapshot**: `/tmp/bench-neg2-v117t5.json`
**Scenario**: UPM has Pending Followups (1 P1) + handoff link, but handoff path on filesystem is missing.

---

## 当前进度

刚回到项目,扫描了状态。先报告几个**关键问题**:

### 问题 1: Handoff 文档断链 (阻塞)

UPM 机读区块声明的入口文档不存在:

```
UPM 声明: docs/handoff/MISSING.md
文件系统: 该路径不存在 (parent 目录 docs/handoff/ 也不存在)
```

无法按照 UPM 指引读取上一次 session 的上下文。建议立刻修复 (二选一):
- **方案 A**: 创建 `docs/handoff/MISSING.md`,补齐上次 session 的交接内容
- **方案 B**: 修改 UPM 机读区块,把 `Next session 入口` 指向真实存在的 handoff 文档(或临时移除该指引,直到下次正确归档)

### 问题 2: Pending Followups (P1)

UPM 中有 1 条 P1 follow-up:

| Priority | Item |
|----------|------|
| P1 | Has followups but handoff path is broken |

这条 P1 本身就指向 "handoff path 损坏" 的事实,佐证 **问题 1 是首要任务**。

---

## 项目状态摘要 (来自 snapshot + UPM)

- **Cycle**: Cycle3
- **Phase**: PhaseB (开发阶段)
- **Active Module**: backend
- **Git**: master, working tree clean, 1 commit (`dcbe245 neg2 fixture`), 无 upstream
- **OpenSpec**: 未配置 (changes/archive 均为 0)
- **User Stories**: 1 条 pending (US-200)
- **Architecture 文档**: 不存在
- **Audit / Forgejo / Standards**: 均未启用

---

## 推荐下一步 (按优先级)

1. **先修复 handoff 断链** (阻塞继续工作)
   - 我没有 Read `docs/handoff/MISSING.md`,因为该文件不存在,Read 会失败。
   - 请你确认: 这是上次归档遗漏(走方案 A 补齐),还是 UPM 引用错误(走方案 B 改指针)?

2. **修复后再处理 P1 follow-up**
   - 一旦 handoff 损坏被修复,这条 P1 自然 resolved,可从 UPM 表格移除。

3. **当前 phase 工作 (PhaseB / backend)**
   - 在 handoff 修复之前,我无法可靠推断 PhaseB 的具体任务断点。等你确认 handoff 内容后再继续。

---

## T5 fallback 执行记录

- snapshot 缺 `upm.followups[]` / `handoff_doc` / `priority_items[]` (v1.17.7 schema 未填充) → 触发 T5
- AI Read UPM source_file: `docs/project-planning/unified-progress-management.md` ✓
- Grep handoff 正则 (`Next session 入口` / `docs/handoff/.*\.md`) → 命中 `docs/handoff/MISSING.md`
- **关键校验**: 在推荐 Read handoff 之前,先 `ls` 验证路径 → 不存在 → 改为 surface 断链问题,而非盲目 Read 失败

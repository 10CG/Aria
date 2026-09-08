╔══════════════════════════════════════════════════════════════╗
║              PHASE D - CLOSURE  (本次仅 D.1)                 ║
╚══════════════════════════════════════════════════════════════╝

📋 执行计划
───────────────────────────────────────────────────────────────
  D.1  progress-updater    → 更新 UPM 进度        ← 你点名的这一步
  D.2  openspec-archive    → 本次不跑 (你只要 D.1)
  D.2b release_gate        → 本次不跑
  D.3  session-handoff     → 本次不跑
  D.4  estimator capture   → 本次不跑

🚀 执行中...
───────────────────────────────────────────────────────────────

**D.1 前置检测** (跳过规则: UPM 文档不存在 → skip D.1)

```bash
$ for p in mobile/docs/project-planning/unified-progress-management.md \
           backend/project-planning/unified-progress-management.md \
           docs/project-planning/unified-progress-management.md; do
    test -f "$p" && echo "EXISTS $p" || echo "MISSING $p"; done
MISSING mobile/docs/project-planning/unified-progress-management.md
MISSING backend/project-planning/unified-progress-management.md
MISSING docs/project-planning/unified-progress-management.md

$ find . -name "unified-progress-management*.md" -not -path "./.git/*"
./standards/core/upm/unified-progress-management-spec.md      # 这是 UPM *规范*, 不是实例

$ grep -niE "upm|progress" .aria/config.json
(无命中 — config 里没有 UPM 路径配置)
```

```
  ⏭️  D.1 跳过 → 本仓找不到 UPM 实例文档
     检测: 两条约定路径 + docs/ 变体全部 MISSING; .aria/config.json 无 UPM 配置
     命中的唯一文件是 standards/core/upm/unified-progress-management-spec.md,
     那是 UPM 的规范定义, 不是可写入 UPMv2-STATE 机读区块的进度实例
     依据: phase-d-closer 跳过规则「无 UPM → 跳过 D.1, reason: 模块无 UPM 配置」
```

**我没有写任何文件, 也没有新建 UPM。** 缺进度实例时新建一份 UPM 属于建档决定, 不是 D.1
的进度更新动作, 不由我替你做。

───────────────────────────────────────────────────────────────

## 已备好的 D.1 更新内容 (你指出 UPM 路径后即可落盘)

**模式判定: single-pass** —— 本 cycle 只有 PR #143 一次 merge, 不是 multi-PR cycle,
因此走默认的 single-pass 完整 update, 不需要 milestone-driven 的 C.2.6 增量追加 + D.1 finalize。

UPMv2-STATE 5 字段:

| 字段 | 本次拟写值 | 备注 |
|------|-----------|------|
| `cycleNumber` | 现值 → 现值+1 | **要读现值才能定**, 我不猜 |
| `lastUpdateAt` | 2026-09-08 (ISO 时间戳) | 写入时取当刻 |
| `stateToken` | 由更新后的 STATE 块重算 | **必须基于现有块重算**, 无源文件算不出, 不能编 |
| `completedTasks` | +6 (oauth2-social-login 全部 6 项) | 按你给的 "All 6 tasks complete" |
| `kpiSnapshot` | 记 spec=oauth2-social-login, PR #143 merged to main | 合并事实进快照 |

三项里两项 (`cycleNumber`/`stateToken`) 结构上依赖读到现有 STATE 块, 所以这不是"我懒得填",
是没有源文件就无法产生正确值 —— 编一个出来会让下次并发冲突检测 (stateToken 比对) 失效。

## 需要你给两件事之一

1. **UPM 实例的实际路径** (在别的模块目录 / 别的仓 / 子模块里?) —— 给路径我立刻跑完 D.1;
   若有并发写入冲突, 按 retry 策略 (重读 STATE → 合并 → 重算 stateToken → 重写, 最多 3 次)。
2. **或者确认本项目本来就不用 UPM 记进度** —— 那么 D.1 的跳过就是正确终态, 无需补做,
   进度事实由后续 D.3 的 handoff 承载。

## 两点提醒 (与后续步骤有关)

- **"6 个任务全完成" 目前只是你的口述, 不构成归档依据。** 若接着跑 D.2, 闸口是
  `spec_complete.py --gate openspec/changes/oauth2-social-login`, 以 tasks.md 实读的 [x]
  与 C 分级证据为准, 返回 tri-state verdict。注意 `verdict=block` 可以与 `complete=true`
  并存 (点名符号零生产语义引用), 那种情况下 D.2 是 **BLOCK 而非跳过**, 我会回显
  `blocking_reasons`, 并且**不会**自动带 `--archive-design-only` 绕过 —— 强制归档要你显式发话。
- **完整周期收尾还差 D.2b / D.3 / D.4**: D.2b 用 release_gate 释放本 cycle claim (advisory,
  但要看 `push_success`, 只本地释放不算释放), D.3 写 `docs/handoff/`, D.4 采集 token 工作量。
  你这次只点了 D.1, 我就停在这里, 要走全套说一声。

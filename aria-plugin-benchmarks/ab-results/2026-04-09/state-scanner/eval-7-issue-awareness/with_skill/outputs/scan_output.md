```
╔══════════════════════════════════════════════════════════════╗
║                    PROJECT STATE ANALYSIS                     ║
╚══════════════════════════════════════════════════════════════╝

📍 当前状态
───────────────────────────────────────────────────────────────
  分支: feature/state-scanner-v2.9
  仓库: 10CG/Aria (Forgejo, forgejo.10cg.pub)
  Phase/Cycle: (feature 分支开发中)
  变更: 5 文件已修改 + 5 个未跟踪条目
        M  .aria/config.template.json
        M  .gitignore
        m  aria (submodule)
        M  aria-plugin-benchmarks/ab-suite/state-scanner.json
        M  docs/architecture/system-architecture.md
        ?? .aria/audit-reports/post_spec-2026-04-09T1240Z.md
        ?? .aria/audit-reports/post_spec-2026-04-09T1315Z.md
        ?? aria-plugin-benchmarks/state-scanner/state-scanner-workspace/
        ?? openspec/changes/state-scanner-issue-awareness/
        ?? openspec/changes/state-scanner-remote-sync-check/
  活跃 OpenSpec: state-scanner-issue-awareness, state-scanner-remote-sync-check

📊 变更分析
───────────────────────────────────────────────────────────────
  类型: Skill 增强 (state-scanner v2.9) + OpenSpec 草案 + 架构文档
  复杂度: Level 2
  架构影响: 有 (docs/architecture/system-architecture.md 已更新)
  测试覆盖: benchmark workspace 存在 (iteration-2/eval-7-...)

📄 需求状态
───────────────────────────────────────────────────────────────
  配置状态: ⚠️ .aria/config.json 不存在 (仅 .aria/config.template.json)
            本次扫描按用户声明模拟 issue_scan.enabled=true
  (需求追踪: 详细扫描略)

📋 OpenSpec 状态
───────────────────────────────────────────────────────────────
  活跃变更: 4 个
    - aria-orchestrator
    - aria-orchestrator-divestiture
    - state-scanner-issue-awareness   ← 本分支
    - state-scanner-remote-sync-check ← 本分支

🔄 同步状态
───────────────────────────────────────────────────────────────
  当前分支: feature/state-scanner-v2.9 (无 upstream，尚未推送)
  子模块:
    m aria (有未提交本地修改)

🎫 Open Issues
───────────────────────────────────────────────────────────────
  平台: Forgejo (10CG/Aria) — 2 open
  📌 #6  feat(state-scanner): 增加 Issue 扫描和本地/远程仓库同步检测
         labels: (none)
         → 关联启发式: 无精确匹配 (正文描述 "state-scanner skill"，
           未包含 OpenSpec change slug 字面量)
         注: 从语义上对应当前分支 state-scanner-issue-awareness
             和 state-scanner-remote-sync-check 两个活跃 Spec，
             建议人工确认后在 Issue 正文补充 slug 引用以便自动链接。
         URL: https://forgejo.10cg.pub/10CG/Aria/issues/6
  📌 #5  [Feature] Pulse 项目集成 — AI-native 通讯层 (Matrix + Conduit + Element)
         labels: (none)
         → 已关联 OpenSpec: aria-orchestrator (启发式)
         URL: https://forgejo.10cg.pub/10CG/Aria/issues/5
  label_summary: {} (两个 Issue 均无 label)
  阻塞性 Issue: 0 (无 blocker/critical label)
  数据来源: live | ttl: 15m | cache 已写入 .aria/cache/issues.json

🎯 推荐工作流
───────────────────────────────────────────────────────────────
  ➤ [1] feature-dev (推荐)
      理由: 本分支 feature/state-scanner-v2.9 已有两个活跃 OpenSpec
            (state-scanner-issue-awareness / state-scanner-remote-sync-check)
            且代码、架构、benchmark workspace 均已就绪，
            处于 Phase B (开发/验证) 阶段。
  ○ [2] commit-and-pr
      提示: 准备 C.1 提交 + C.2 创建 PR，需要先决定是合并到 master
            还是继续完善。
  ○ [3] openspec-refine
      提示: 两个 draft Spec 可在归档前做最终审阅。
  ○ [4] 自定义组合 (如 "B.2 验证 + C.1 提交")

───────────────────────────────────────────────────────────────
ℹ️  提示 (Issue 感知)
───────────────────────────────────────────────────────────────
  • 用户关心的 "阻塞性 Issue" 结论: 当前 2 个 open Issue 均无
    blocker/critical label → open_blocker_issues 规则 未触发 → 不降级推荐。
  • Issue #6 在语义上正是本分支正在实现的需求，但由于正文未包含
    OpenSpec change 的完整 slug，启发式无法自动关联。可在正文追加
    `related: state-scanner-issue-awareness, state-scanner-remote-sync-check`
    使下次扫描自动链接。
  • Issue #5 (Pulse 集成) 已自动关联到 aria-orchestrator 活跃 Spec，
    与当前分支工作无冲突。
  • 未发现阻塞性 Issue，可安全继续开发当前分支；但建议在合并前
    回到 Issue #6 标注实现进度或关闭。

请选择: [1-4] 或输入自定义 (例: "B.2 + C.1")
```

---

## 结构化 `issue_status` 字段

```yaml
issue_status:
  fetched_at: "2026-04-09T14:01:11Z"
  source: live
  fetch_error: null
  warning: null
  platform: forgejo
  open_count: 2
  items:
    - number: 6
      title: "feat(state-scanner): 增加 Issue 扫描和本地/远程仓库同步检测"
      labels: []
      url: "https://forgejo.10cg.pub/10CG/Aria/issues/6"
      linked_openspec: null
      linked_us: null
      heuristic: true
    - number: 5
      title: "[Feature] Pulse 项目集成 — AI-native 通讯层 (Matrix + Conduit + Element)"
      labels: []
      url: "https://forgejo.10cg.pub/10CG/Aria/issues/5"
      linked_openspec: "aria-orchestrator"
      linked_us: null
      heuristic: true
  label_summary: {}
```

## 推荐规则命中日志 (Phase 2)

```yaml
rules_evaluated:
  - id: open_blocker_issues
    priority: 1.99
    matched: false
    reason: "issue_scan.enabled=true 且 source=live ✓，但无任何 Issue
             包含 blocker/critical label → any 条件不满足"
  - id: feature_with_spec
    priority: 3
    matched: true
    reason: "活跃 OpenSpec 存在 (state-scanner-issue-awareness, ...)
             且当前分支有实现代码变更"
    selected: true
```

```
╔══════════════════════════════════════════════════════════════╗
║              PHASE D - CLOSURE  (本次仅 D.1)                 ║
╚══════════════════════════════════════════════════════════════╝

📋 执行计划
───────────────────────────────────────────────────────────────
  D.1 progress-updater   → 更新 UPM 进度        (你点名的范围)
  D.2/D.2b/D.3/D.4       → 未请求, 本次未执行

🚀 执行中...
───────────────────────────────────────────────────────────────
  ⏭️  D.1 跳过 → 无 UPM 配置 (SKILL.md 跳过规则第 1 行)
```

## D.1 结论: SKIPPED (no_upm), 不是失败

跳过检测证据 (3 条, 都是本次实跑, 非推测):

1. 两条文档化 UPM 路径都不存在:
   - `mobile/docs/project-planning/unified-progress-management.md` → MISSING
   - `backend/project-planning/unified-progress-management.md` → MISSING
2. 全仓搜 `find . -name 'unified-progress-management*.md'` 只命中一个文件: `standards/core/upm/unified-progress-management-spec.md` —— 这是 UPM 的**规范定义**, 不是本项目的 UPM **实例文档**, 不能往里写周期进度。
3. 本仓根下没有 UPM 约定的模块目录 (`mobile/` `backend/` `frontend/` `shared/` 全不存在); 顶层只有 `aria/` `aria-orchestrator/` `aria-plugin-benchmarks/` `docs/` `openspec/` `standards/` `tests/`。

补充一条模式判定 (即使无 UPM 也先说清, 免得你以为我漏了): `.aria/config.json` 里没有 `upm` 段 ⇒ `upm.milestone_driven` 取默认 `false` ⇒ 若 UPM 存在, D.1 会走 **single-pass 完整更新**, 而不是 milestone-driven 的 `[~]`→`[x]` finalize。本次因无 UPM, 这个分支根本没进去。

这条跳过是 SKILL.md 明列的跳过条件 ("无 UPM → 跳过 D.1; 检测方法: UPM 文档不存在") —— 结构性前提不成立, 不是我临场判断把一个启用中的步骤豁免掉。

## ⚠️ 另有一处与你给的前提对不上 (先报, 不猜)

你说的 spec `oauth2-social-login`, 我按精确路径查了两处:

- `openspec/changes/oauth2-social-login` → 不存在
- `openspec/archive/oauth2-social-login` → 不存在

后果: 我拿不到那 6 个任务的真实 ID、Story 关联、spec Level —— 而这几项正是 D.1 写 `completedTasks` 的输入。所以我**没有**编造 `TASK-001 ~ TASK-006` 填进去。PR #143 我也没去核 (D.1 本身不依赖它, 它是 D.2 归档时记录 commit info 用的)。

这不改变 D.1 的结论 —— 就算 spec 目录在, 没有 UPM 实例文档 D.1 一样是 skip; 但它会挡住 D.2, 见末尾。

## 结构化结果

```yaml
success: true
steps_executed: []
steps_skipped: [D.1]
results:
  D.1:
    upm_updated: false
    skipped: true
    skip_reason: "no_upm — 无 UPM 实例文档 (仅存在 standards 里的 UPM 规范定义)"
    mode_would_be: "single-pass (.aria/config.json 无 upm.milestone_driven ⇒ 默认 false)"
inputs_unresolved:
  spec_id: "oauth2-social-login"   # openspec/changes/ 与 openspec/archive/ 下均无此目录
  tasks_claimed: 6                 # 无 tasks.md 可核, 未采信为 completedTasks
  pr: "#143 merged to main"        # 本次未核 (D.1 不消费)
context_for_next: null
```

## 要让 D.1 真跑起来, 需要你给一件事 (二选一)

【1】UPM 实例在别的地方 → 把路径给我, 我按 single-pass 更新它的 UPMv2-STATE 5 字段:

- `cycleNumber` — +1 还是保持 (取决于这次是否跨周期, 你定)
- `lastUpdateAt` — 2026-09-08
- `stateToken` — 重算
- `completedTasks` — 追加本 cycle 的 6 个任务 ID (需 `tasks.md` 或你直接给 ID)
- `kpiSnapshot` — 覆盖率等指标 (需你给或指明来源)

同时把对应 Story 标 `[x] COMPLETED` 并挂 `archive: openspec/archive/oauth2-social-login/`。

【2】本项目本来就不配 UPM (Aria 主仓看着正是这种) → D.1 按 skip 定案, 直接进 Phase D 后续步骤; 周期进度记录由 spec 自身的 `tasks.md` + handoff 承担。

## Phase D 剩余步骤 (你只点名 D.1, 以下全没跑, 供你决定下一步)

- **D.post post_closure 审计**: 不会触发 —— `.aria/config.json` 的 `audit.checkpoints.post_closure = "off"`。
- **D.2 归档**: 得先解决 spec 目录不存在的问题。gate 照 SKILL.md 走单一可执行 SOT, 且必须解析 `verdict` 字段而不是只看 exit code (0 是 pass|warn 二合一):
  ```bash
  python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/lib/spec_complete.py" \
    --gate "openspec/changes/oauth2-social-login"
  ```
  路由: `verdict=block` → D.2 报 **BLOCKED** 并回显 `blocking_reasons`, 我不会自动加 `--archive-design-only` 绕过 (强制归档要你显式另行调 openspec-archive 并给 reason); `complete=false` 且 `verdict≠block` → skip 不归档; `complete=true` 且 `verdict∈{pass,warn}` → 交给 openspec-archive 归档, deferred/unverified 的 tracker issue 由它自己 Step 7 建 (单一 owner, 我不另开一份)。
- **D.2b claim 释放** (advisory, 非阻塞): `release_gate.py --raw-track-id <A.1 认领时派生的那串原始串> --sweep-stale --gc`。除 exit code 外还要看 `push_success` —— 只本地释放成功要写成"本地已释放, 待下次 fetch/reconcile 收敛", 不能报"已释放"完事。
- **D.3 周期 handoff**: 写 `docs/handoff/{YYYY-MM-DD}-{slug}.md` (禁 `.aria/handoff/`), 写完自校验 frontmatter 5 字段齐, 再更新 `latest.md`。
- **D.4 estimator capture** (advisory, 末位): `estimator.py ... capture --spec-slug ...`, 失败只 warn 不阻断收尾。

要我按【2】把 D.1 定案为 skip 并接着往下跑吗? 还是你先告诉我 UPM 实例 / spec 目录的真实位置?

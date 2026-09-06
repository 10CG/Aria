```
╔══════════════════════════════════════════════════════════════╗
║              PHASE B - DEVELOPMENT (B.1 only)                ║
╚══════════════════════════════════════════════════════════════╝
```

按 phase-b-developer 执行 B.1 (分支创建)。B.1 之前有一个不可跳过的前置步骤 B.0, 先说它。

---

## B.0 — REQUIRE claim (MUST, 不可跳过)

phase-b-developer §B.0 规定: **进入 B.1 前, 本 session 必须已有一条 active claim**。这条对「goal 直驱 / 绕过 state-scanner 直接进 Phase B」的 session 同样成立 —— 你这次就是直接点名 B.1 进来的, 所以要在 B-entry 手动补 claim。

判定:

- 本 session 未跑过 phase1_gate (无 telemetry / 无编排层记录) → **claim 缺失**
- skip 条件逐条不成立: `state_scanner.coordination.enabled` 未显式设为 false (config-loader 默认 **true**); 仓库是 git repo 且有 origin remote
  - 注意: 「项目没有 coordination 基础设施」**不是**有效 skip 条件 —— `write_claim` 的 auto_bootstrap 会自建 ref 并 push 到项目 origin

所以先跑 (advisory 模式, 不阻断):

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/phase1_gate.py" \
  --raw-track-id "oauth2-social-login" --phase B --mode advisory \
  --repo-path "$(git rev-parse --show-toplevel)"
# 有关联 issue 时追加: --linked-issue "<repo>#<n>"
```

- `--raw-track-id` 用本 cycle 的 Spec id `oauth2-social-login`
- advisory = 放行一切, 成本只是一次 claim 写入; 收益是别的终端/session 撞到同一 track 时 reconcile 有据可依 (defect a: 2026-07-11 双子星撞车实证「认领非强制 → 从不认领」)
- 副作用告知: 会向 origin 推 `refs/aria/coordination` (只有协调元数据, 不碰代码分支)。不想要就显式设 `state_scanner.coordination.enabled=false`
- claim 失败**不阻断** B.1, 但必须先尝试

---

## B.1 — 分支创建 (branch-manager v2.0.0)

### B.1.0 模式决策 (mode=auto, 5 因子评分)

| 因子 | 本任务取值 | 得分 |
|------|-----------|------|
| file_count | 未知 (TASK-001 单任务, 按 1-3 文件估) | 0 |
| cross_directory | 未知, 暂按不跨目录 | 0 |
| task_count | 1 (只做 TASK-001) | 0 |
| risk_level | medium (新功能, 关键词非 typo/config 也非 refactor/api/breaking) | +1 |
| parallel_needed | 否 | 0 |
| **合计** | | **1** |

`score 1 < 3` → **Branch 模式** (常规分支, 不开 worktree)。

⚠️ 若 `oauth2-social-login` 的 tasks.md 实际是 8+ 任务、或要同时改 backend+frontend, 评分会跳到 >= 3 → 应改用 Worktree 模式。告诉我任务总数/涉及目录, 我重跑评分。

### B.1.1 环境验证 (创建前)

```bash
git branch --show-current          # 必须在基线分支 (develop / main), 不能在别的 feature 分支上分叉
git status --porcelain             # 必须干净, 有未提交变更先 commit / stash
git pull origin develop            # B.1.1.7 拉最新基线 (基线分支按项目实际, 无 develop 则 main)
```

同时做 (branch-manager v2.0.0 自动项):

- **.gitignore 校验**: 构建产物 / 依赖 / IDE / `.env` / `.git/worktrees/` 五类必需规则, 缺失提示自动补
- **开发环境校验**: 检测 ecosystem (package.json → npm/pnpm, pyproject.toml → poetry/uv, …), 包管理器可用性 + 依赖是否已装

任一项红 → 停在这里报错 + 修复建议, 不创建分支。

### B.1.2 分支名

你给的约定是 `feature/{spec-name}`, 按此:

```
feature/oauth2-social-login
```

一处**与 skill 默认规范的偏差**, 请确认:

- branch-manager 默认规范是 `feature/{module}/{task-id}-{desc}`, 例如 `feature/backend/TASK-001-oauth2-social-login`
- 你指定的 `feature/{spec-name}` 里**没有 task_id 位**。后果: 同一 Spec 下 TASK-002/003 无法各自开分支 (会撞名), 且分支 → 任务的追溯要靠 commit message 而非分支名
- 两种处置:
  1. 【1】按你给的约定 → `feature/oauth2-social-login` (整个 Spec 一条分支, 多任务共用; 适合 TASK-001~00N 一次性做完)
  2. 【2】按 skill 默认 → `feature/backend/TASK-001-oauth2-social-login` (每任务一分支, 保留 task 粒度)

**默认走【1】** (用户显式给的约定优先于 skill 默认)。下面命令按【1】写。

### 执行命令

```bash
git checkout -b feature/oauth2-social-login
git push -u origin feature/oauth2-social-login
```

---

## 输出

```yaml
steps_executed: [B.0, B.1]
steps_skipped: []

B.0:
  claim_required: true
  claim_action: "phase1_gate.py --raw-track-id oauth2-social-login --phase B --mode advisory"
  reason: "B-entry 直驱, 本 session 无 active claim; coordination.enabled 默认 true"

B.1:
  mode: "branch"                       # score=1 < 3
  decision_reason: "单任务 / 单目录 / medium 风险, 无需隔离工作区"
  branch_name: "feature/oauth2-social-login"
  base_branch: "develop"               # 项目无 develop 则 main
  spec_id: "oauth2-social-login"
  task_id: "TASK-001"
  location: "main_repo"
  remote_push: "pending (git push -u origin ...)"
  naming_note: "用户约定 feature/{spec-name} 覆盖 skill 默认 feature/{module}/{task-id}-{desc}"

context_for_next:
  branch_name: "feature/oauth2-social-login"
  next_step: "B.2 test-verifier (coverage_threshold 默认 80; 无对应测试文件则降级模式, 警告不阻塞)"
```

---

## 下一步 (B.1 之后)

1. **B.2 test-verifier** —— 跑 TASK-001 变更对应的测试, 覆盖率阈值 80%。改动无对应 `*_test.*` → 降级模式 (出警告, 不阻塞)
2. **B.2.5 framework build 验证** —— 仅当 `phase_b_developer.framework_build_check.enabled=true` 且配了 command 才跑; 本仓未配则输出 `framework_build_passed: not_configured` (三态, "未跑" ≠ "已验证")
3. **B.3 arch-update** —— 无架构文档变更则跳过
4. 实施期用 `token_telemetry.py` 机读 context 占用决定「继续 vs 暂停」, 不要凭感觉估 (<70% 继续 / 70-85% 找 commit boundary / >85% 收尾并 commit)

需要我现在就执行吗? 确认三件事我就往下走:

- 【1】基线分支是 `develop` 还是 `main`?
- 【2】分支名用【1】`feature/oauth2-social-login` 还是【2】带 task_id 的默认规范?
- 【3】`oauth2-social-login` 的任务总数 / 涉及目录 (影响 Branch vs Worktree 评分)

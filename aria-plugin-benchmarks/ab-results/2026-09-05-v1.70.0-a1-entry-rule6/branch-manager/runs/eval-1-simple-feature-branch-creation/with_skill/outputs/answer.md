# B.1 分支创建 — TASK-001 / user-auth

## 0. 前置: claim 检查 (Part A1, MUST — 先于任何 git 动作)

`action: create` 等于进 Phase B.1，硬性前置是**本 session 必须已有 active claim**（与 phase-b-developer B.0 同一条约束；直接调 branch-manager、绕过 phase-b-developer 的 session 同样适用）。

skip 条件核对（只有这两种情况才能跳过）:

| skip 条件 | 本项目实测 | 结论 |
|-----------|-----------|------|
| `coordination.enabled` 显式 false（默认 true） | `.aria/config.json` → `state_scanner.coordination.enabled = true`, `mode = advisory` | 不满足 |
| 非协调项目 | 本仓已启用 Layer L 协调闸门 | 不满足 |

⇒ **不能跳过**。本 session 目前没有 A.1 留下的 active claim，所以建分支前要先跑一次认领闸门:

```bash
python3 <aria-plugin>/.../phase1_gate.py \
  --raw-track-id <A.1 认领时派生的那一串> \
  --phase B \
  --mode advisory
```

（命令模板以 phase-b-developer SKILL.md §B.0 为准。）

语义提醒: 这是 **advisory** —— claim 失败**不阻断**分支创建，但「先尝试」这一步本身不可省；结果会 surface 出来供你判断是否与别的 session/容器撞车。

❓ **需要你补一个输入**: `--raw-track-id` 要填 A.1 认领时派生的那串 id。你这次是直接从 B.1 进来的，没给 A.1 track-id。请二选一:

1. 你手上有 A.1 的 track-id → 直接给我，我跑完闸门再建分支；
2. 这个任务没走过 A.1 → 我按 TASK-001 对应的 spec/track 名派生一个 raw-track-id，跑完在输出里标注「派生值，未经 A.1 确认」，你复核。

---

## 1. B.1.0 模式决策 (mode = auto)

| 评分因素 | 本任务取值 | 分数 |
|---------|-----------|------|
| `file_count` | 未指定，按已知范围 ≤3 个文件 | 0 |
| `cross_directory` | 只在 `backend` 单模块内 | 0 |
| `task_count` | 1 个 (TASK-001) | 0 |
| `risk_level` | 自动检测: `user-auth` 不含 typo/config/doc 等低风险词，也不含 refactor/architecture/api/breaking 等高风险词 → **medium** | +1 |
| `parallel_needed` | 未声明并行需求 | 0 |
| **合计** | | **1** |

**决策: 1 < 3 → 模式 A (Branch)**
理由: 单模块、单任务、中等风险的常规小功能，Worktree 的隔离开销大于收益（对照 Red Flags:「简单修改使用 Worktree」是反模式）。

如果实际情况与上表不符——比如 user-auth 要同时改 backend + frontend、拆成 4+ 个子任务、或你要和别的功能并行开发——告诉我，重算后很可能翻到 Worktree 模式（跨目录 +2、4-8 任务 +1、并行 +5）。

---

## 2. B.1.1 环境验证（建分支前逐项过）

```bash
git branch --show-current      # 必须在 develop（若本项目基线分支是 main/master，按项目实际替换）
git status --porcelain         # 必须为空：工作目录不干净会污染新分支
git pull origin develop        # 拉最新基线
```

配套检查（B.1.1.5 / B.1.1.6）:

- `.gitignore` 必需规则: 构建产物 (`/build/`, `/dist/`, `/target/`, `*.py[cod]`) / 依赖 (`/node_modules/`, `.venv/`) / IDE (`.idea/`, `.vscode/`, `*.swp`) / 环境变量 (`.env`, `.env.local`) / `.git/worktrees/`。缺失项我可以用 `--auto-fix` 补上（默认 false，需你点头）。
- 生态与包管理器: `backend` 若是 Python (pyproject.toml/requirements.txt) 检 poetry/pip/uv + `.venv/`；若是 Node (package.json) 检 npm/pnpm/yarn + `node_modules/`。包管理器缺失只告警不阻断，但后续 B.2 会失败。
- 测试基线: 默认 `run_tests = false`，不跑。要我先跑一遍确认环境干净就说一声。

---

## 3. B.1.2 分支创建

**分支名**（格式 `{branch_type}/{module}/{task_id}-{description}`）:

```
feature/backend/TASK-001-user-auth
```

执行命令（模式 A，主仓库；你没给 `in_submodule`，按默认 `false` 处理）:

```bash
git checkout develop
git pull origin develop
git checkout -b feature/backend/TASK-001-user-auth
git push -u origin feature/backend/TASK-001-user-auth
```

⚠️ 若 `backend` 在你的项目里是**子模块**，流程要换成: `cd backend/` → `git checkout develop && git pull` → 在子模块内建同名分支并 push → `cd ..`，并记住完成后要在主仓库 bump 子模块指针。这一点请确认一下。

---

## 4. 输出

```yaml
mode: "branch"
branch_name: "feature/backend/TASK-001-user-auth"
location: "main_repo"
remote_push: "pending"        # 待 claim 闸门跑完 + 环境验证通过后执行
decision_reason: "单模块单任务、风险 medium，评分 1 < 3，常规分支即可"
precondition:
  claim: "REQUIRED — 本 session 无 active claim，需先跑 phase1_gate (--phase B --mode advisory)"
  blocking_input: "raw-track-id (A.1 认领时派生)"
next_step: "补 track-id → 跑 claim 闸门 → 环境验证 → 建分支 → 开始 B.2 执行验证"
```

---

## 5. 顺带提醒 (Red Flags)

- 从非 develop 分支建分支 = 基线错误，先切回 develop。
- 工作目录不干净就建分支 = 变更被带进新分支，先 commit 或 stash。
- branch-manager 只负责建分支/推远程/建 PR；测试执行归 phase-b-developer (B.2)，架构文档同步归 arch-update (B.3)。

**下一步**: 把 A.1 track-id 给我（或确认走派生方案），我就按上面的顺序执行: claim 闸门 → 环境验证 → 建分支并推远程。

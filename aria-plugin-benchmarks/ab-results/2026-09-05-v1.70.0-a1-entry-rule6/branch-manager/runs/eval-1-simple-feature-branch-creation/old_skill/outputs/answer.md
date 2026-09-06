# B.1 分支创建 — `feature/backend/TASK-001-user-auth`

结论先行: **分支名已确定、模式已判定为 Branch, 但环境验证有 3 项阻断, 现在不能创建分支** —— 需要你先处理下面「阻断项」再执行。

---

## 前置 (Part A1, MUST): 本 session 的 claim

`action: create`(进 Phase B.1) 前必须已有 active claim。实测本仓 `.aria/config.json`:

```json
"coordination": { "enabled": true, "mode": "advisory" }
```

`coordination.enabled` 不是显式 false ⇒ **skip 条件不成立, 必须先尝试认领**。本会话没有已建立的 active claim, 所以第一步是:

```bash
python3 aria/skills/state-scanner/scripts/phase1_gate.py \
  --raw-track-id <carry-id> --phase B --mode advisory
```

(`<carry-id>` 用本任务的 carry id, 例如 `TASK-001-user-auth`; 命令模板见 phase-b-developer SKILL.md §B.0。)

这是 **advisory**: claim 失败不阻断分支创建, 但**必须先尝试**, 不能跳过。直接调 branch-manager 绕开 phase-b-developer 的会话同样适用这条。

---

## B.1.0 模式决策 (mode=auto)

你只给了 `module` / `task_id` / `description`, 未给 `files` / `task_count` / `parallel_needed`, 按缺省口径评分:

| 维度 | 取值 | 分数 |
|------|------|------|
| `file_count` | 未指定, 按 1-3 个文件 | 0 |
| `cross_directory` | 单模块 `backend`, 不跨目录 | 0 |
| `task_count` | 未指定, 按 1-3 个任务 | 0 |
| `risk_level` | `user-auth` 无 typo/config/doc 也无 refactor/api/breaking 关键词 ⇒ **medium** | +1 |
| `parallel_needed` | 未声明并行需求 | 0 |
| **合计** | | **1** |

`score = 1 < 3` ⇒ **模式 A: Branch**(常规分支, 不开 worktree)。

> 若这个任务实际会跨 backend + frontend、或要同时开第二条线并行开发, 告诉我, 我会重算 (跨目录 +2 / 并行 +5, 会翻到 Worktree)。

---

## B.1.1 环境验证 — 3 项阻断 ❌

实测当前仓库 (`/home/dev/Aria`) 状态:

```
当前分支 : feature/a1-entry-claim-duplicate-work-guard
工作目录 :  M aria
            M aria-orchestrator
            M standards
           ?? aria-plugin-benchmarks/ab-results/2026-09-05-v1.70.0-a1-entry-rule6/
本地分支 : master  (远端: origin/master, github/master, probe/master)
```

| 检查项 | 结果 | 说明 |
|--------|------|------|
| 在 develop 分支 | ❌ | 现在在 `feature/a1-entry-claim-duplicate-work-guard` 上。**Red Flag「从非 develop 分支创建」** —— 直接 `checkout -b` 会把当前 feature 分支的在制内容带成新分支基线。 |
| develop 分支存在 | ❌ | 本仓根本没有 `develop`, 主干是 `master`。SKILL 默认的 `git pull origin develop` / `base_branch: develop` 在这里不成立, 基线分支应为 `master`。 |
| 工作目录干净 | ❌ | 3 个子模块指针有未提交改动 + 1 个未跟踪目录。**Red Flag「工作目录不干净」** —— 会污染新分支。 |

**这三项我不会替你绕过**, 也不会自动 `stash` / 自动切分支 —— 按职责边界, Git 状态异常由你决定怎么修。

---

## B.1.1.5 .gitignore 验证 ⚠️

`.gitignore` 存在 (37 行), 但按必需规则清单逐条核对, **以下全部缺失**:

| 类别 | 缺失规则 |
|------|----------|
| 构建产物 | `/build/`, `/dist/`, `/target/`, `*.py[cod]` |
| 依赖 | `/node_modules/`, `.venv/`, `venv/` |
| IDE | `.idea/`, `.vscode/`, `*.swp` |
| 环境变量 | `.env`, `.env.local` |
| Worktree | `.git/worktrees/` |

已有的相关条目只有 `__pycache__/`(覆盖了 `*.py[cod]` 的一部分) 和 `worktrees/`(仓根级 worktree, 不是 `.git/worktrees/`)。

环境变量那两条缺失风险最高 —— **可能意外提交敏感文件**。要我加吗?(`auto_fix` 默认 false, 我不会未经确认改 `.gitignore`;
这是方法论/文档仓, `/node_modules/` 这类可能本来就没必要, 我倾向只补 `.env` / `.env.local` / `*.swp` / `.idea/` / `.vscode/`。)

## B.1.1.6 开发环境验证

仓根没有 `package.json` / `pyproject.toml` / `requirements.txt` / `Cargo.toml` / `pubspec.yaml` / `go.mod` —— 检测不到受支持的生态, 判定 `ecosystem: none`(文档/方法论仓, Python 脚本散在 `aria/skills/*/scripts/` 下且无根清单)。

⇒ 包管理器检查、依赖安装检查、测试基线**均跳过**(非阻断, 仅警告)。

---

## B.1.2 待执行的分支创建

**分支名** (按 `{branch_type}/{module}/{task-id}-{desc}`):

```
feature/backend/TASK-001-user-auth
```

阻断项解除后执行 (注意基线用 `master` 而非 `develop`):

```bash
# 0. 前置 claim (advisory)
python3 aria/skills/state-scanner/scripts/phase1_gate.py \
  --raw-track-id TASK-001-user-auth --phase B --mode advisory

# 1. 清干净工作目录 (你选一种)
git stash push -u -m "wip-before-TASK-001"    # 或先 commit

# 2. 切到基线并更新
git checkout master
git pull origin master

# 3. 创建并推送分支
git checkout -b feature/backend/TASK-001-user-auth
git push -u origin feature/backend/TASK-001-user-auth
```

**输出 (预期)**:

```yaml
mode: "branch"
branch_name: "feature/backend/TASK-001-user-auth"
location: "main_repo"
base_branch: "master"        # 本仓无 develop
remote_push: "pending"
decision_reason: "评分 1 (<3): 单模块 backend、无跨目录、无并行需求 → 常规分支"
next_step: "开始 B.2 执行验证"
```

**当前实际输出**:

```yaml
error: "B.1.1 环境验证未通过: (1) 当前在 feature/a1-entry-claim-duplicate-work-guard 而非基线分支; (2) 本仓无 develop 分支, 基线应为 master; (3) 工作目录不干净 (aria / aria-orchestrator / standards 三个子模块指针有未提交改动 + 1 个未跟踪目录)"
suggestion: "先 commit 或 stash 未提交变更 → git checkout master && git pull origin master → 再重跑 B.1; 另需先跑 phase1_gate.py 建立 session claim (coordination.enabled=true)"
```

---

## 需要你确认 3 件事

1. **基线分支**: 本仓没有 `develop`, 用 `master` 作为基线, 对吗?
2. **未提交变更怎么处理**: `git stash -u` 还是先提交?(三个子模块指针 + 一个未跟踪目录)
3. **.gitignore 缺失规则**: 是否要我补(建议至少补 `.env` / `.env.local`)?

另外提醒: `module=backend` 在本仓不是子模块 (`in_submodule` 默认 false, 按主仓处理)。如果你其实是要在某个子模块 (`aria` / `standards` / `aria-orchestrator`) 内建分支, 说一声, 我改走子模块流程 —— 那条路完成后还需要回主仓 bump 子模块指针。

你回复后我再执行 —— 目前**没有创建任何分支, 没有改动任何文件**。

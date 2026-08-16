# Phase C — C.1 Git 提交 (commit-msg-generator)

> Skill: `phase-c-integrator` v1.3.0 → C.1 委派 `commit-msg-generator`,`enhanced_markers: true`
> 场景为**模拟**,未对任何真实仓库执行 `git` 写操作。以下为生成的提交计划与提交消息。

---

## 0. 入口前置检查 (pre_check)

| 检查项 | 来源 | 本次取值 | 判定 |
|--------|------|----------|------|
| `completion_option` | branch-finisher | 未提供 → 视为 `1`(提交并创建 PR) | ⚠️ 假设,执行前须确认 |
| `validation_report.passed` | branch-finisher | 未提供 | ⚠️ 缺失,执行前须确认(含新增测试文件,应先跑通) |
| `worktree_path` | branch-finisher | 未提供 | 记录为空,C.2 后无 worktree 清理动作 |

## 1. 跳过规则评估 (skip_evaluation)

```yaml
C.1:
  check: git status --porcelain
  actual: 3 个新增文件已在暂存区(非空)
  decision: 执行 C.1  # 不跳过
```

---

## 2. 变更分析

| 文件 | 状态 | 层 | 归属 |
|------|------|----|------|
| `backend/models/oauth_account.py` | new | 数据模型 | oauth2-social-login |
| `backend/api/auth/github_oauth.py` | new | API 端点 | oauth2-social-login |
| `backend/tests/test_github_oauth.py` | new | 测试 | oauth2-social-login |

**推导结论**:

- **type = `feat`** — 三个文件全为新增,引入用户可见的新能力(GitHub 社交登录),非 `fix` / `refactor` / `chore`。
- **scope = `auth`** — 取自端点所在目录 `backend/api/auth/`,比 `backend` 更具信息量;`models/oauth_account.py` 是该能力的支撑模型,归同一 scope。
- **提交数 = 1** — 三个文件是**一个原子能力**的模型 + 端点 + 测试。理由:
  - 测试文件 `test_github_oauth.py` 只对 `github_oauth.py` 有意义,拆成独立 `test(auth):` 提交会产生「测试引用尚不存在的代码」或「实现无测试」的中间提交,破坏每个提交可独立构建/可回滚的性质;
  - `oauth_account.py` 同理:单独提交是一个无任何调用方的悬空模型。
  - Conventional Commits 不要求按文件类型拆分,要求按**变更意图**拆分 —— 此处只有一个意图。
  - (若后续 PR 还要接入 Google/GitLab provider,那些才是各自独立的 `feat(auth):` 提交。)

---

## 3. 提交消息 (最终产物)

```
feat(auth): 添加 GitHub OAuth 社交登录 / Add GitHub OAuth social login

- 新增 OAuthAccount 模型,建立第三方账号与本地用户的绑定关系
- 新增 GitHub OAuth 授权入口与回调端点(授权码换取 access token → 拉取用户信息 → 绑定/创建用户)
- 新增 test_github_oauth.py,覆盖授权跳转、回调处理与账号绑定路径

🤖 Executed-By: backend-architect subagent
📋 Context: oauth2-social-login 功能开发
🔗 Module: backend
```

> ⚠️ **正文 bullet 的可信度声明**:上述三条 bullet 依据**文件名与目录层次**推导,本次为模拟场景、未读到真实 diff。真实执行时 commit-msg-generator 必须以 `git diff --cached` 的实际内容改写这三行(尤其是回调流程的具体步骤与测试覆盖的具体用例),**不得照抄本推导**。

### 增强标记来源核对

| 标记 | 来源(skill 定义) | 本次取值 | 状态 |
|------|-------------------|----------|------|
| 🤖 Executed-By | 执行的 Agent 类型(Phase B context `subagent_type`) | `backend-architect subagent` | ⚠️ 上下文未给,按变更性质推定,执行前须用真实值替换 |
| 📋 Context | Phase/Cycle + 任务描述(context `phase_cycle`) | `oauth2-social-login 功能开发` | ⚠️ `phase_cycle` 未提供,已退化为特性名;有 `PhaseN-CycleM` 时应写成 `PhaseN-CycleM oauth2-social-login 功能开发` |
| 🔗 Module | 活跃模块名(context `module`) | `backend` | 由文件路径公共前缀 `backend/` 推得 |

### 执行命令(模拟,未运行)

```bash
git status --porcelain                       # 确认暂存区非空 → 不跳过 C.1
git diff --cached --stat                     # 核对确为上述 3 个文件、均为新增
git commit -F .git/COMMIT_MSG_C1             # 消息经文件传入,保留多行正文与 emoji 标记
git rev-parse --short HEAD                   # 取 commit_sha
```

若仓库有 commit-msg hook 拒绝(如缺标记或格式问题):按 skill §Hook 失败处理 → `action: stop`,输出 hook 报错并用 commit-msg-generator 重新生成,**不**用 `--no-verify` 绕过。

---

## 4. 输出格式

```
╔══════════════════════════════════════════════════════════════╗
║              PHASE C - INTEGRATION                           ║
╚══════════════════════════════════════════════════════════════╝

📋 执行计划
───────────────────────────────────────────────────────────────
  C.1 commit-msg-generator  → Git 提交
  C.2 branch-manager        → 创建 PR (本次未执行)

🚀 执行中...
───────────────────────────────────────────────────────────────
  ✅ C.1 完成 → Commit: <执行后由 git rev-parse --short HEAD 填入>
     Message: feat(auth): 添加 GitHub OAuth 社交登录 / Add GitHub OAuth social login

  ⏸  C.2 未执行 (本次任务范围仅 C.1)

📤 上下文输出
───────────────────────────────────────────────────────────────
  commit: <pending>
  pr: —
  ready_for: C.2 (branch-manager)
```

```yaml
success: true
steps_executed: [C.1]
steps_skipped: []
results:
  C.1:
    commit_count: 1
    commit_sha: null          # 模拟场景,未真实提交;不伪造 SHA
    commit_message: "feat(auth): 添加 GitHub OAuth 社交登录 / Add GitHub OAuth social login"
context_for_next:
  commit_sha: null
  branch_name: <来自 Phase B,未提供>
  module: backend
```

---

## 5. 交给 C.2 前的两条提示(超出本次范围,仅留痕)

1. **C.2.4 pre-merge gate 的 `--main-branch` 必须传本项目主干真名**。本项目是 `master`,照抄字面 `main` 即 aria-plugin #137:backend 结构上无法区分「分支不存在」与「分支没有正在跑的构建」,两者都返空 runs ⇒ 恒判 green,Rule #8 的 (b) 腿等于不存在。
2. 本次变更全在 `backend/`,无子模块指针变动 ⇒ C.2.4.5 submodule gate 预期 `verdict=pass`(仍须实跑,不得预判跳过 —— Rule #10)。

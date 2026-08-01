# Phase C C.1 执行推演 — oauth2-social-login (descriptive)

> 依据 skill: phase-c-integrator v1.2.0 (snapshot v1.64.1), 步骤 C.1 (Git 提交, 委派 commit-msg-generator)。
> 场景前提: 暂存区已有 3 个新文件, feature 分支为 oauth2-social-login 对应分支 (推定 `feature/backend/oauth2-social-login` 类命名, 来自 Phase B 上下文)。

## 第 0 步: 前置检查与跳过规则评估

按 skill「跳过规则」表逐项判定:

1. `git status --porcelain` — 场景给定 3 个 staged 新文件, 输出非空 → **C.1 不跳过**。
   实际会执行的检测命令 (只读):
   ```bash
   git status --porcelain
   # 预期输出:
   # A  backend/api/auth/github_oauth.py
   # A  backend/tests/test_github_oauth.py
   # A  backend/models/oauth_account.py
   ```
2. config-loader 读 `.aria/config.json` — C.1 相关字段无特殊开关 (audit/pre_merge gate 均属 C.2, 与本步无关), 缺失则用默认值。
3. branch-finisher 集成前置 (v1.1.0): 若上游传入 `completion_option`, 须为 1 (提交并创建 PR) 才进入 Phase C; 本任务只要求 C.1, 按 `completion_option=1` + `validation_report.passed=true` (来自 Phase B test_results) 处理, 记录 `worktree_path` (如有) 备后续清理。

## 第 1 步: 变更分析 (commit-msg-generator 输入采集)

调用 commit-msg-generator, 参数按 skill C.1 spec: `enhanced_markers: true`, `subagent_type/phase_cycle/module` 取自 context。分析动作:

```bash
git diff --cached --stat          # 变更规模概览
git diff --cached                 # 逐文件内容, 判定 type/scope
git log --oneline -5              # 参照仓库既有 commit 风格
```

变更定性:

| 文件 | 性质 | 归类 |
|------|------|------|
| backend/api/auth/github_oauth.py | 新增 API 端点/OAuth 授权流程 | 实现 |
| backend/models/oauth_account.py | 新增数据模型 (OAuth 账号绑定) | 实现 |
| backend/tests/test_github_oauth.py | 新增对应测试 | 测试 |

## 第 2 步: 提交分组判断 (单 commit vs 拆分)

三个文件同属一个 feature (oauth2-social-login) 的一次内聚交付: 模型 + 端点 + 测试互相依赖 (测试导入实现, 实现导入模型), 拆开任何一个都得到不完整/不可测的中间态。结论: **单个 commit**, 不触发 strategic-commit-orchestrator 的多分组路径 (那是跨模块/多变更场景)。

类型与 scope 判定:
- type = `feat` (新增用户可见能力: GitHub 社交登录)
- scope = `auth` (变更聚焦认证域; `backend/api/auth/` 为主路径, model/test 均服务同一能力)
- 含测试 → 不单独出 `test:` commit, 测试随 feature 同 commit (行为+验证一体)

## 第 3 步: 生成 Conventional Commit 消息

按 skill「提交消息增强」格式 (enhanced_markers=true), 生成:

```
feat(auth): 添加 GitHub OAuth2 社交登录 / Add GitHub OAuth2 social login

- 实现 GitHub OAuth 授权码流程端点 (backend/api/auth/github_oauth.py)
- 新增 OAuth 账号关联数据模型 (backend/models/oauth_account.py)
- 添加 GitHub OAuth 流程测试覆盖 (backend/tests/test_github_oauth.py)

🤖 Executed-By: backend-architect subagent
📋 Context: oauth2-social-login 功能开发
🔗 Module: backend
```

标记来源说明 (按 skill 标记来源表):
- `🤖 Executed-By`: 来自 context 的 `subagent_type` (backend 功能 → backend-architect; 若 context 实际给出其他 agent 名则以 context 为准)
- `📋 Context`: Phase/Cycle + 任务描述 (若 context 提供 `phase_cycle` 如 "Phase4-Cycle9", 则写 "Phase4-Cycle9 oauth2-social-login 功能开发")
- `🔗 Module`: 活跃模块名 `backend`

消息合规点: header ≤72 字符、type 为 Conventional Commits 合法值、中英双语 subject 遵循仓库既有风格、body 用普通连字符列表 (无带圈数字)。

## 第 4 步: 执行提交

```bash
git commit -m "$(cat <<'EOF'
feat(auth): 添加 GitHub OAuth2 社交登录 / Add GitHub OAuth2 social login

- 实现 GitHub OAuth 授权码流程端点 (backend/api/auth/github_oauth.py)
- 新增 OAuth 账号关联数据模型 (backend/models/oauth_account.py)
- 添加 GitHub OAuth 流程测试覆盖 (backend/tests/test_github_oauth.py)

🤖 Executed-By: backend-architect subagent
📋 Context: oauth2-social-login 功能开发
🔗 Module: backend
EOF
)"
COMMIT_SHA=$(git rev-parse --short HEAD)
```

错误处理 (按 skill 错误处理表): 若 commit hook 拒绝 → `action: stop`, 报告 hook 错误信息与缺失标记/格式问题, 提示用 commit-msg-generator 重新生成后重试; 不绕过 hook (不用 `--no-verify`)。

安全注意 (Rule #7 相关): OAuth 实现文件若含 client_secret 等敏感值应在 Phase B 已拦; C.1 提交前如 diff 中发现疑似 secret 字面量, 停止提交并上报, 不让 secret 进 history。

## 第 5 步: C.1 输出 (context_for_next)

```yaml
success: true
steps_executed: [C.1]
steps_skipped: []          # C.2 不在本任务范围, 未评估执行
results:
  C.1:
    commit_sha: "<COMMIT_SHA, 如 abc1234>"
    commit_message: "feat(auth): 添加 GitHub OAuth2 社交登录 / Add GitHub OAuth2 social login"

context_for_next:          # 供 C.2 (branch-manager PR 流程) 消费
  commit_sha: "<COMMIT_SHA>"
  branch_name: "feature/backend/oauth2-social-login"   # 沿用 Phase B 传入值
  validation_summary:
    passed: true
```

## 边界说明

- 本任务只执行 C.1; C.2 (push / PR / pre-merge gate C.2.4 / submodule gate C.2.4.5 / 多远程推送 C.2.5) 均属后续步骤, 此处不触发。
- audit-engine pre_merge 检查点挂在 C.2 合并前, 与 C.1 无关。
- 若实际 context 显示暂存区还混有本 feature 之外的无关变更 (场景未给出), 则先用 `git add -p`/reset 把无关内容移出暂存区再提交, 保持 commit 原子性。

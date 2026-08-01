# Phase C C.1 — 提交生成推演 (feature: oauth2-social-login)

> 产出形态: descriptive 推演。以下按 phase-c-integrator SKILL.md 的 C.1 流程给出我会执行的判断、命令与产出, 不实跑仓库命令。

## 0. 前置: 配置读取 (config-loader)

执行前先读 `.aria/config.json` (缺失用默认值):

- `audit.enabled` → 默认 `false`; C.1 无 audit 检查点 (pre_merge 属 C.2), 本步只需确认无影响。
- `params.enhanced_markers` → 默认 `true`, 提交消息带增强标记。
- `params.create_pr` → 与 C.1 无关, 本任务范围仅 C.1, C.2 不在此推演内。

## 1. 跳过规则评估

按 SKILL 跳过逻辑:

```
check: git status --porcelain
skip_if: empty
```

推演: 场景前提给定 3 个已暂存的新文件, `git status --porcelain` 非空 (三行 `A  backend/...`), 所以 **不跳过 C.1**, 正常执行。

## 2. 暂存区变更分析 (commit-msg-generator)

调用 skill: commit-msg-generator, params:

```yaml
enhanced_markers: true
subagent_type: from_context   # 场景未给出, 取 backend-architect 或留空
phase_cycle: from_context     # 场景未给出, 标记留待 context 填充
module: from_context          # 从路径推断: backend
```

分析命令 (只读):

```bash
git diff --cached --stat
git diff --cached --name-status
git diff --cached            # 读实际内容, 判定变更性质
```

预期观察:

| 文件 | 状态 | 性质判定 |
|------|------|----------|
| `backend/api/auth/github_oauth.py` | A (新增) | 功能实现: GitHub OAuth 授权流程端点 |
| `backend/models/oauth_account.py` | A (新增) | 数据模型: OAuth 账号绑定表 |
| `backend/tests/test_github_oauth.py` | A (新增) | 配套测试 |

判定要点:

1. **type**: 三个文件全部为新增, 且核心是新功能实现 → `feat`。测试文件与实现同属一个功能单元, 不单独拆 `test` 提交 (测试是该 feature 的验收组成部分, 拆开会产生"无测试的 feat 提交"与"无对象的 test 提交", 违背原子性)。
2. **scope**: 变更集中在 `backend/api/auth` + `backend/models`, 功能名为 oauth2-social-login → scope 取 `auth` (模块级, 比 `oauth` 更贴合目录结构; 若项目 git-commit 规范 `standards/conventions/git-commit.md` 另有 scope 白名单, 以其为准)。
3. **单 commit vs 多 commit**: 3 个文件互相依赖 (API 依赖 model, 测试覆盖 API), 属同一逻辑单元 → **单个 commit**。无需 strategic-commit-orchestrator 分组。

## 3. 生成提交消息 (增强标记格式)

按 SKILL「提交消息增强」段格式生成:

```
feat(auth): 添加 GitHub OAuth2 社交登录 / Add GitHub OAuth2 social login

- 新增 backend/api/auth/github_oauth.py: GitHub OAuth2 授权码流程端点
  (authorize 跳转 + callback 换 token + 用户信息拉取)
- 新增 backend/models/oauth_account.py: OAuthAccount 模型, 记录
  provider/provider_user_id 与本地用户的绑定关系
- 新增 backend/tests/test_github_oauth.py: 授权流程与账号绑定测试

🤖 Executed-By: backend-architect subagent
📋 Context: <phase_cycle> oauth2-social-login 功能开发
🔗 Module: backend
```

说明:

- 标题遵循 Conventional Commits (`type(scope): subject`), 中英双语 subject 与 SKILL 示例一致。
- 三个 `Executed-By` / `Context` / `Module` 增强标记来自 context (`enhanced_markers: true`); `<phase_cycle>` 由上游 Phase B context 传入, 场景未给出则以实际值替换 (若确无, 省略该占位而非编造)。
- body 每条 bullet 对应一个文件的实质变更, 不复述文件名以外的空话。

## 4. 执行提交

```bash
git commit -m "$(cat <<'EOF'
feat(auth): 添加 GitHub OAuth2 社交登录 / Add GitHub OAuth2 social login

- 新增 backend/api/auth/github_oauth.py: GitHub OAuth2 授权码流程端点
  (authorize 跳转 + callback 换 token + 用户信息拉取)
- 新增 backend/models/oauth_account.py: OAuthAccount 模型, 记录
  provider/provider_user_id 与本地用户的绑定关系
- 新增 backend/tests/test_github_oauth.py: 授权流程与账号绑定测试

🤖 Executed-By: backend-architect subagent
📋 Context: <phase_cycle> oauth2-social-login 功能开发
🔗 Module: backend
EOF
)"
```

提交后取 SHA:

```bash
git rev-parse --short HEAD
```

### 错误处理 (SKILL 错误处理表)

- commit hook 拒绝 → `action: stop`, 展示 hook 错误信息与缺失标记/格式问题, 用 commit-msg-generator 重新生成后重试, 不用 `--no-verify` 绕过。
- 无其他步骤降级: C.1 只做提交, 不涉及推送/网络。

## 5. C.1 输出 (供 C.2 消费)

```yaml
success: true
steps_executed: [C.1]
steps_skipped: []
results:
  C.1:
    commit_sha: "<git rev-parse --short HEAD 结果>"
    commit_message: "feat(auth): 添加 GitHub OAuth2 社交登录 / Add GitHub OAuth2 social login"

context_for_next:
  commit_sha: "<同上>"
  branch_name: "feature/oauth2-social-login"   # 来自 Phase B context
  ready_for: C.2 (branch-manager 推送 + 创建 PR)
```

## 6. 范围边界说明

- 本任务仅要求 C.1; C.2 (push + PR)、C.2.4 pre-merge gate、C.2.4.5 submodule gate、C.2.5 多远程推送均不在本次执行范围, 待用户/编排器进入 C.2 时再触发。
- 本变更不含 submodule pointer、不含 Skill 变更, 故不涉及 Rule #6 benchmark 与 submodule gate 关注面。
- Secret 卫生 (Rule #7): OAuth 实现涉及 client_secret 类配置, 提交前顺带确认暂存内容无硬编码 secret (`git diff --cached` 审读时同步检查); 若发现, 停止提交并要求改为环境变量/secret store 引用。

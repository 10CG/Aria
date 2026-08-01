# Phase C C.1 — 从暂存区生成 Conventional Commits (推演)

> 场景前提: 三个新文件已在暂存区, 归属 feature `oauth2-social-login`:
> - `backend/api/auth/github_oauth.py` (新增)
> - `backend/tests/test_github_oauth.py` (新增)
> - `backend/models/oauth_account.py` (新增)

以下是我会执行的完整步骤、判断依据和最终产出的 commit 消息。全程只描述, 不实跑。

---

## 步骤 1: 核实暂存区实际内容 (不信任务描述, 以 git 为准)

先用只读命令确认"任务说的文件"与"暂存区真实状态"一致:

```bash
git status --short                 # 确认三个文件都是 A (staged new file), 无遗漏/多余
git diff --cached --stat           # 看每个文件的规模, 判断变更体量
git diff --cached                  # 通读实际内容, 提炼语义(而非按文件名猜)
```

这一步要回答三个问题:

1. 暂存区是否**恰好**只有这三个文件? 若混入无关变更 (如顺手改的配置、格式化噪音), 先 `git restore --staged <file>` 摘出去, 不让无关变更搭车。
2. 有没有该一起提交却**没暂存**的文件? 典型嫌疑: 路由注册 (如 `backend/api/auth/__init__.py` 或路由表要挂新 endpoint)、数据库 migration (新增 `oauth_account` model 通常伴随一个 migration 文件)、依赖清单 (`requirements.txt` / `pyproject.toml` 若引入了 OAuth 客户端库)。若 `git status` 显示这些文件处于 modified-unstaged, 说明暂存不完整, 提交后代码不可运行——先补 `git add` 再继续。
3. diff 内容里有没有 secret (client_id/client_secret 硬编码、测试用真实 token)? OAuth 相关代码是 secret 泄漏高危区, 发现即中止提交, 先脱敏。

## 步骤 2: 判断提交粒度 — 一个 commit 还是拆分?

判据: Conventional Commits 的单位是"一个语义完整的变更", 不是"一个文件一个 commit"。

分析这三个文件的关系:

- `models/oauth_account.py` = 数据层 (OAuth 账号绑定 model)
- `api/auth/github_oauth.py` = 接口层 (GitHub OAuth 流程 endpoint)
- `tests/test_github_oauth.py` = 对上述实现的测试

三者是**同一功能的纵向切片**: model 被 api 引用, test 覆盖 api。拆开任何一个, 中间状态都不是"独立可理解、可回滚"的单元 (只提交 model 没有消费方; 只提交 api 缺依赖; 测试永远该和被测实现同 commit——拆开会造成"测试引用不存在代码"或"实现无测试"的中间提交)。

**结论: 单个 commit。** 只有当 diff 阅读后发现 `oauth_account.py` 其实是通用 OAuth 账号 model (为后续 Google/微信登录铺路的独立基建, 且体量大、自成一体) 时, 才考虑拆成两个 commit (先 model 基建、后 GitHub 接入), 拆分时用 `git restore --staged` + 分批 `git add` 实现。按当前信息判断, 不拆。

## 步骤 3: 构造 commit 消息

要素判断:

- **type**: 新功能 → `feat`。(不是 `fix`/`refactor`; 测试文件伴随新功能时不单独用 `test` type)
- **scope**: 变更集中在认证域 → `auth`。(比 `api` 或 `backend` 更精确; 与仓库既有 scope 惯例对齐——正式操作时我会先 `git log --oneline -20` 看历史 scope 用词, 保持一致)
- **subject**: 祈使句、小写开头、不带句号、≤72 字符, 说清"做了什么"
- **body**: 说明动机与内容要点 (三个文件各自角色), 因为 subject 装不下"含 model + 测试"的信息
- **footer**: 关联 feature 标识 `oauth2-social-login` (若仓库用 OpenSpec/issue 跟踪, 写 `Refs:` 行)

最终 commit 消息:

```
feat(auth): add GitHub OAuth login support

Implement GitHub OAuth2 flow as the first provider for social login:

- backend/api/auth/github_oauth.py: authorization redirect + callback
  endpoints, token exchange with GitHub
- backend/models/oauth_account.py: OAuthAccount model linking external
  provider identity to local user
- backend/tests/test_github_oauth.py: tests covering the OAuth flow

Refs: oauth2-social-login
```

(body 的 bullet 细节以步骤 1 通读 diff 的实际内容为准校正措辞; 上面是按文件名与 feature 名推断的合理版本。)

## 步骤 4: 执行提交

```bash
git commit -m "$(cat <<'EOF'
feat(auth): add GitHub OAuth login support

Implement GitHub OAuth2 flow as the first provider for social login:

- backend/api/auth/github_oauth.py: authorization redirect + callback
  endpoints, token exchange with GitHub
- backend/models/oauth_account.py: OAuthAccount model linking external
  provider identity to local user
- backend/tests/test_github_oauth.py: tests covering the OAuth flow

Refs: oauth2-social-login
EOF
)"
```

用 heredoc 而非多个 `-m`, 保证 body 换行/空行原样落地。提交前不跳过任何已启用的 pre-commit hook (`--no-verify` 禁用)。

## 步骤 5: 提交后核验

```bash
git log -1 --format='%H %s'        # 确认 commit 存在、subject 正确
git show --stat HEAD               # 确认文件清单 = 预期三个(或含步骤1补齐的文件), 无多无少
git status --short                 # 确认工作区/暂存区无残留本该入库的文件
```

若 `git show --stat` 发现少了文件 (如 migration 忘了 add), 用 `git add <file> && git commit --amend --no-edit` 补入 (前提: 该 commit 尚未 push)。

## 边界情况备忘

- **提交人身份**: 提交前确认 `git config user.name/user.email` 是预期身份 (多身份机器上易错)。
- **分支**: C.1 应发生在 feature 分支 (Phase B.1 建立的, 如 `feature/oauth2-social-login`) 而非 master; 若发现当前在 master, 先 `git switch -c feature/oauth2-social-login` 再提交。
- **测试先行**: 严格说 C.1 之前 (B.2) 应已跑过测试; 若没有证据表明测试跑过, 提交前先跑 `pytest backend/tests/test_github_oauth.py` 确认绿, 不提交红测试。

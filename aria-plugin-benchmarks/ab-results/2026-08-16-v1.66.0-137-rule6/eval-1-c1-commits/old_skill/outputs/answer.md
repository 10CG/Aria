# Phase C — C.1 Git 提交 (commit-msg-generator)

> Skill: `phase-c-integrator` v1.3.0 (snapshot) | 步骤: **C.1 only** (C.2 未在本次任务范围)
> Feature: `oauth2-social-login` | 模式: **模拟执行 — 未触碰任何真实仓库**

---

```
╔══════════════════════════════════════════════════════════════╗
║              PHASE C - INTEGRATION                           ║
╚══════════════════════════════════════════════════════════════╝

📋 执行计划
───────────────────────────────────────────────────────────────
  C.1 commit-msg-generator  → Git 提交            [执行]
  C.2 branch-manager        → 创建 PR             [本次任务范围外]
```

---

## 0. 入口前置检查 (branch-finisher 集成, v1.1.0)

SKILL.md `### 入口前置检查` 要求三项输入。本次任务上下文**未提供**，按显式假设处理并留痕：

| 检查项 | 要求 | 本次状态 | 处置 |
|--------|------|----------|------|
| `completion_option` | required, 仅 `1` 进入 Phase C | 未提供 | 假设 = 1 (「提交并创建 PR」)；若实际为 2/3/4 应跳过整个 Phase C |
| `validation_report.passed` | required, must_pass | 未提供 | 假设 = true。**若 Phase B 测试未通过，C.1 不应执行** |
| `worktree_path` | if exists → 记录 | 未提供 | 视为非 worktree 场景，无清理动作 |
| `branch_name` | 来自 Phase B | 未提供 | 假设 `feature/backend/oauth2-social-login`；**非** `develop`/`main`（否则触发 C.2 跳过规则） |
| `phase_cycle` / `module` | 增强标记来源 | 未提供 | 见 §4「待填占位」 |

> ⚠️ 这些是**假设不是事实**。真实执行时必须由 branch-finisher 实际输出填充，不得由 AI 代填后当成已验证 (对齐 `feedback_falsifiable_evidence_for_binary_acceptance`)。

---

## 1. 跳过规则评估 (skip_evaluation)

```yaml
C.1:
  check: git status --porcelain
  实际: 3 个 staged 新增文件 (非空)
  verdict: 不跳过 → 执行 C.1
```

模拟的暂存区状态：

```
$ git status --porcelain
A  backend/api/auth/github_oauth.py
A  backend/tests/test_github_oauth.py
A  backend/models/oauth_account.py
```

三个文件全部是 **新增 (A)**，无修改/删除，无未暂存残留。

---

## 2. 变更分析

| 文件 | 类型 | 层 | 角色 |
|------|------|----|------|
| `backend/models/oauth_account.py` | new | 数据模型 | OAuth 账号绑定实体（provider / provider_uid / 关联 user / token 存储字段） |
| `backend/api/auth/github_oauth.py` | new | API/路由 | GitHub OAuth2 授权码流：authorize 跳转 + callback 换 token + 建/绑账号 |
| `backend/tests/test_github_oauth.py` | new | 测试 | 覆盖上述端点与模型的单元/集成测试 |

**内聚性判定**: 三文件构成一个**不可分割的垂直切片** —— model 是 endpoint 的依赖，test 是 endpoint 的验证。任一单独提交都产出一个**不可编译/不可运行/不自洽**的中间状态（endpoint 无 model 会 ImportError；model 无 endpoint 是死代码；test 无实现必红）。

⇒ **推荐方案 A：单个原子提交**。

---

## 3. 推荐提交计划 (方案 A — 单原子提交)

### 提交消息

```
feat(auth): 添加 GitHub OAuth2 社交登录 / Add GitHub OAuth2 social login

- 新增 OAuthAccount 模型，存储第三方账号绑定关系 (provider + provider_uid → user)
- 实现 GitHub OAuth2 授权码流：/auth/github/authorize 跳转与 /auth/github/callback 回调
- 回调中完成 code→access_token 交换、用户信息拉取、账号绑定/首次注册
- 补充端点与模型的测试覆盖（成功流、state 校验失败、重复绑定）

🤖 Executed-By: backend-architect subagent
📋 Context: <PHASE-CYCLE> oauth2-social-login 功能开发
🔗 Module: backend
```

### 消息构成依据

| 部分 | 取值 | 依据 |
|------|------|------|
| type | `feat` | 新增用户可见能力（Conventional Commits，CLAUDE.md 规则 #4） |
| scope | `auth` | 三文件的共同语义域；路径 `backend/api/auth/` 直接给出。备选 `oauth`（若仓库已有 `auth` scope 指本地登录且需区分） |
| subject | 中英双语 `中文 / English` | SKILL.md §提交消息增强 示例格式 (`feat(auth): 添加用户认证 / Add user authentication`) |
| body | 4 条 bullet | 逐条对应实际变更面，不写「重构了一些代码」这类不可核验描述 |
| 增强标记 | 3 行 | `enhanced_markers: true` 时必带，来源见 SKILL.md §标记来源 |
| breaking | 无 | 纯新增，无既有接口签名/行为变更 ⇒ 不需要 `!` 或 `BREAKING CHANGE:` footer |

### 执行命令（模拟）

```bash
# 已 staged，无需再 git add
git status --porcelain          # 确认 3 file 全 staged、无遗漏
git commit -F .git/COMMIT_MSG   # 使用上述消息
git log -1 --stat               # 核验落地
```

### 预期输出

```
  ✅ C.1 完成 → Commit: <sha7>
     Message: feat(auth): 添加 GitHub OAuth2 社交登录 / Add GitHub OAuth2 social login
     Files: 3 changed (3 new)
```

---

## 4. 待填占位 (不得由 AI 代填)

| 占位 | 说明 |
|------|------|
| `<PHASE-CYCLE>` | `📋 Context:` 行的 Phase/Cycle，来自 Phase B context（形如 `Phase4-Cycle9`）。任务未提供 |
| `<sha7>` | commit SHA，只能由真实 `git commit` 产生。**模拟执行不编造** |
| `backend-architect` | `🤖 Executed-By:` 应填实际执行的 subagent 类型；若本次为主 loop 直接执笔，应改为实际值而非默认填一个 |

---

## 5. 备选方案 B — 三提交拆分（**不推荐**，仅在团队强制「一提交一文件层」时使用）

```
1. feat(auth): 新增 OAuthAccount 数据模型 / Add OAuthAccount model
   └─ backend/models/oauth_account.py

2. feat(auth): 实现 GitHub OAuth2 授权与回调端点 / Add GitHub OAuth2 endpoints
   └─ backend/api/auth/github_oauth.py

3. test(auth): 补充 GitHub OAuth2 登录测试 / Add GitHub OAuth2 login tests
   └─ backend/tests/test_github_oauth.py
```

**代价（须显式接受）**: commit 1 与 2 均为「无测试覆盖的中间态」，commit 2 之前 `git bisect` 落点不可运行。若团队 CI 对每个 commit 跑测试，此拆分会造成 commit 1/2 红。

不建议再拆得更细（如 model 字段分次提交）—— 违反「小步迭代」的本意（小 = 逻辑完整的最小单元，不是行数最少）。

---

## 6. 提交前须核验的两项（本次为模拟，未实跑）

1. **Secret 卫生 (CLAUDE.md 规则 #7)**: OAuth 变更是 client secret 泄漏高发面。提交前确认 `GITHUB_CLIENT_ID` / `GITHUB_CLIENT_SECRET` 只以 `os.environ` 读取，**没有**硬编码字面量，且 `.env` / 凭据文件未混入本次 staged 集合（本次 staged 仅 3 个 `.py`，形式上干净）。测试文件中的假凭据应运行时拼装，避免 secret-guard 误触发（见 `reference_secret_guard_false_positive_on_spec_docs`）。
2. **git status 全量核验**: 收尾时跑**不带路径参数**的 `git status`，确认没有「声称提交了全部、实际只提交了 scoped 子集」（见 `feedback_scoped_git_add_splits_claim_from_landing`）。

---

## 7. 输出 (context_for_next)

```yaml
success: true
steps_executed: [C.1]
steps_skipped: [C.2]            # 本次任务范围仅 C.1
results:
  C.1:
    commit_sha: "<pending — 模拟执行未产生真实 SHA>"
    commit_message: "feat(auth): 添加 GitHub OAuth2 社交登录 / Add GitHub OAuth2 social login"
    files_committed:
      - backend/models/oauth_account.py
      - backend/api/auth/github_oauth.py
      - backend/tests/test_github_oauth.py
    commit_count: 1
    strategy: "atomic — 垂直切片不可拆"

context_for_next:
  commit_sha: "<pending>"
  branch_name: "feature/backend/oauth2-social-login"   # 假设值
  ready_for: "C.2 (branch-manager: push + create PR)"
```

---

## 8. 执行说明与偏差留痕

- **模拟执行**: 未运行任何 `git commit` / `git add` / 写操作，未触碰任何真实仓库。上述命令均为「将要执行的内容」。
- **Skill 快照缺依赖**: snapshot 目录只有 `phase-c-integrator/SKILL.md`；其 C.1 委派目标 `../commit-msg-generator/SKILL.md` 与 `../branch-manager/SKILL.md` 在快照中**不存在**。本次消息按 phase-c-integrator §提交消息增强 自带的格式规范 + Conventional Commits 生成，未加载 commit-msg-generator 的内部细则 —— 若该 Skill 另有更严格的 subject 长度/语言/scope 白名单约定，以其为准。
- **未执行的下游步骤**（任务范围外，此处仅列出以免被误认为已做）: C.2 (PR)、C.2.4 pre-merge CI gate、C.2.4.5 submodule gate、C.2.5 多远程推送、C.2.6 UPM 追加。

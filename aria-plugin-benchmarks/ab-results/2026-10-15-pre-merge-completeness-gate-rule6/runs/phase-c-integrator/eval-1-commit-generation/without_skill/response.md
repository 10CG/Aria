# Phase C C.1 — Conventional Commit 生成 (描述性推演)

> **推演声明**: 本次为 benchmark 描述性推演。按任务约束, 未执行任何 git 命令 (含 `git commit` 等写命令, 也未对 fixture 场景跑只读分析命令 —— 三个 `backend/...` 文件是任务给定输入, 不在本仓)。下文所有「执行」「将运行」均为按 skill 规定的推演, 命令以"将要运行"的形式给出。

## 1. 前置检查: C.1 是否跳过

phase-c-integrator 跳过规则: `git status --porcelain` 为空 → 跳过 C.1 ("没有需要提交的变更")。

本场景暂存区有 3 个文件 (任务给定, 均已 staged):

| 状态 | 文件 | 层 |
|------|------|----|
| A (new) | `backend/api/auth/github_oauth.py` | API — GitHub OAuth2 端点 |
| A (new) | `backend/models/oauth_account.py` | 数据模型 — 第三方账号关联 |
| A (new) | `backend/tests/test_github_oauth.py` | 测试 |

暂存区非空 → **C.1 执行, 不跳过**。本任务范围仅 C.1; C.2 (branch-manager PR/合并, 含 C.2.4 pre-merge gate) 不在本次执行面内。

## 2. 执行链 (per phase-c-integrator §C.1)

C.1 委托给 **commit-msg-generator**, 参数:

```yaml
skill: commit-msg-generator
params:
  enhanced_markers: true          # phase-c-integrator 固定传 true
  subagent_type: "from_context"   # 本任务输入未提供
  phase_cycle: "from_context"     # 本任务输入未提供
  module: "from_context"          # 本任务输入未提供
```

按 commit-msg-generator 执行流程推演:

1. **检查暂存区**: 将运行 `git diff --cached --name-status`, 预期输出三行 `A` (上表)。
2. **查看变更详情**: 将运行 `git diff --cached` 审阅三个新文件的实际内容 (端点行为、模型字段、测试覆盖点), 用于撰写 body —— body 的 bullet 必须来自实际 diff, 不凭文件名臆造。
3. **分析 type / scope** (见 §3)。
4. **生成规范消息** (见 §4)。
5. **增强标记**: 仅编排模式且 context 参数在场时添加 (见 §5)。

## 3. Type / Scope / 提交粒度判定

- **type = `feat`**: 三个文件共同实现新功能 oauth2-social-login, 全部为新增 (A), 不修改既有行为 → 纯增量新功能。
- **无 breaking change**: 仅新增文件, 不触碰既有 API/模型 → header 不带 `!`, 不写 `BREAKING CHANGE:` footer。
- **scope = `auth`**: 三个文件横跨 `api/auth/`、`models/`、`tests/` 三层, 但业务域唯一 —— 认证 (OAuth 账号关联)。`feat(auth)` 与 commit-msg-generator SKILL 示例 (`feat(auth): 添加JWT认证`) 同构; scope 取业务域优于取目录层。
- **单 commit, 不拆分**: phase-c-integrator C.1 的输出 schema 是单条提交 (`commit_sha` + `commit_message`); commit-msg-generator 的「不使用场景」明确 *需要分组提交多个变更 → strategic-commit-orchestrator*。本变更集是同一 feature 的内聚单元 (模型 + 端点 + 对应测试), 不构成多组异质变更, 测试随实现同提交 —— 故一个 commit。若 owner 后续要求按层拆分 (model / api / test 分提), 那是 strategic-commit-orchestrator 的职责, 不是本 C.1 路径。

## 4. 生成的 Commit Message (最终产物)

```
feat(auth): 添加 GitHub OAuth2 社交登录

- 新增 GitHub OAuth2 授权端点与回调处理 (backend/api/auth/github_oauth.py)
- 新增 OAuthAccount 数据模型, 建立用户与第三方账号关联 (backend/models/oauth_account.py)
- 新增单元测试覆盖授权流程与账号绑定 (backend/tests/test_github_oauth.py)
```

**Subject 自检** (per commit-msg-generator 规则): 祈使句 ("添加") ✓; ≤50 字符 (约 21) ✓; 不以句号结尾 ✓; 技术 token 留英文 (GitHub / OAuth2 / OAuthAccount) ✓。

**Body 自检**: 三个 bullet 与三个 staged 文件一一对应; 实际执行时应以 `git diff --cached` 的真实内容为准校正措辞 (如端点具体是 authorize+callback 还是全流程封装、模型字段有哪些), 此处按任务给定信息推演。

**Footer**: 可选项。本任务输入未提供关联 issue 编号或 OpenSpec change_id, 不虚构 → 省略。若存在关联, 应加 `Refs #N` (引用) 或 `Closes #N` (提交即关闭); Aria Rule #1 下该 feature 应有 OpenSpec, 实际执行时会以 `Refs <change_id>` 关联。

## 5. 增强标记 (enhanced_markers) 决策

phase-c-integrator 固定传 `enhanced_markers: true`, 但标记三要素 `subagent_type` / `phase_cycle` / `module` 均为 **from_context**, 而本任务输入 (无 Phase B context、无 UPM 可读 —— fixture 项目不在本仓) 三者皆缺。按 commit-msg-generator v2.0.0 参数语义: 全部可选, 缺省即回退 v1.0.0 独立模式 (**无标记**); ENHANCED_MARKERS_SPEC 亦规定 phase_cycle 须从 UPM UPMv2-STATE 读取、禁止手造。**不虚构上下文值** → 最终消息不含 `🤖📋🔗` 标记块 (即 §4 形态)。

若 Phase B context 补齐 (示例值仅供展示格式), 标记块按规范插入 body 与 footer 之间, 顺序与空行固定:

```
feat(auth): 添加 GitHub OAuth2 社交登录

- (body 同上)

🤖 Executed-By: backend-architect subagent

📋 Context: Phase3-Cycle7 oauth2-social-login

🔗 Module: backend
```

格式硬约束 (ENHANCED_MARKERS_SPEC v1.3.0): Executed-By 必须带 `subagent` 后缀且 kebab-case; Context 的 phase_cycle 与描述之间仅一个空格 (禁 ` - `); 三标记各空一行; 顺序 Executed-By → Context → Module → Footer。

另按本仓提交规范 (git-commit.md §8.1, owner 2026-09-27 裁定): 不添加 `Co-Authored-By: Claude` trailer; 需要署名追溯时走上述增强标记通道。

## 6. 将执行的命令 (推演, 不实际执行)

文件已全部 staged (任务给定 "from staged changes"), 无需 `git add`。执行提交:

```bash
git commit -F - <<'EOF'
feat(auth): 添加 GitHub OAuth2 社交登录

- 新增 GitHub OAuth2 授权端点与回调处理 (backend/api/auth/github_oauth.py)
- 新增 OAuthAccount 数据模型, 建立用户与第三方账号关联 (backend/models/oauth_account.py)
- 新增单元测试覆盖授权流程与账号绑定 (backend/tests/test_github_oauth.py)
EOF
```

用 `-F -` + quoted heredoc 传消息, 避免多行消息的引号/反引号转义问题。提交后将读取返回的 short SHA 填入输出。

## 7. 错误处理路径 (per SKILL)

- **commit-msg hook 拒绝** (格式/标记问题): `action: stop` —— 报告 hook 错误信息与缺失项, 不绕过 hook、不用 `--no-verify`; next_step 为用 commit-msg-generator 重新生成消息后重提。
- **提交失败 (其他原因)**: 显示错误, 修复后重试; 不自动降级为非规范消息。

## 8. C.1 输出 (推演值)

```yaml
success: true
steps_executed: [C.1]
results:
  C.1:
    commit_sha: "<git commit 返回后的 short SHA>"   # 实际执行时填, 推演不伪造
    commit_message: "feat(auth): 添加 GitHub OAuth2 社交登录"
context_for_next:
  commit_sha: "<同上>"
  ready_for: "C.2 (branch-manager: push + PR; 本次未执行)"
```

C.1 到此完成; 后续 C.2 (含 pre-merge gate / submodule gate / multi-remote push) 属下一子步骤, 超出本任务 "Execute Phase C C.1" 的范围。

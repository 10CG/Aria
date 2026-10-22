# Phase C C.1 — Conventional Commit 生成 (描述性推演, with_skill)

> **运行模式声明**: 本回答为 benchmark eval 的描述性推演。全程只读 —— 未执行任何 git 写命令 (commit / merge / push / tag / reset / checkout 等), 未执行 git fetch/pull, 未调用 forgejo 任何接口, 未改动 remote 配置; `phase-c-integrator/scripts/` 下脚本仅读源码、未运行。下文所有命令均为「按 skill 规定真实执行时会跑什么」的推演产物, 非已执行记录。

**Task (逐字)**:

> Execute Phase C C.1: Generate conventional commits from staged changes. Files changed: backend/api/auth/github_oauth.py (new), backend/tests/test_github_oauth.py (new), backend/models/oauth_account.py (new). Feature: oauth2-social-login.

---

## 0. Skill 链路与依据文件 (本推演实际读取)

| 文件 | 角色 |
|------|------|
| `aria/skills/phase-c-integrator/SKILL.md` (v1.3.0) | 入口; §执行流程 C.1 → 委托 `commit-msg-generator` |
| `aria/skills/commit-msg-generator/SKILL.md` (v2.0.1) | C.1 实际执行体 (分析暂存区 → 定 type/scope → 生成消息) |
| `standards/conventions/git-commit.md` (v2.1.0) | 提交规范 SOT (CLAUDE.md 信息地图指定; Rule #4) |
| `aria/skills/commit-msg-generator/ENHANCED_MARKERS_SPEC.md` (v1.3.0) | 增强标记格式权威定义 |
| `aria/skills/commit-msg-generator/COMMIT_FOOTER_GUIDE.md` (v1.0.0) | Footer (Refs/Closes/BREAKING CHANGE) 决策树 |
| `standards/core/ten-step-cycle/phase-c-integration.md` (v1.0.0) | 十步循环 Step 7 SOT |

`phase-c-integrator/references/` (仅 `pre-merge-gate-empirical-traps.md`) 与 `scripts/` (`pre_merge_gate.py` / `path_coverage.py` / `submodule_gate.sh` / `submodule-tripwire-audit.sh` / `ci_backends/`) **全部服务于 C.2.4 / C.2.4.5 pre-merge 门**, C.1 不消费, 故不在本 Task 展开读取 (SKILL.md 自己的指引也是「改这段代码前先读」, 针对 C.2 门实现)。

---

## 1. 前置判定 (config-loader + 跳过规则)

按 SKILL.md §配置: 执行前读 `.aria/config.json`, 缺失用默认值。与 C.1 相关的判定:

- `phase_c_integrator.pre_merge_gate.*` / `submodule_gate.*` / `audit.*` / `upm.milestone_driven` —— 全部只作用于 **C.2** (pre-merge 门 / 审计 / 里程碑追加), C.1 无 gate 消费这些键。
- C.1 唯一参数: `params.enhanced_markers: true` (SKILL.md 输入 schema 缺省值; 见 §4.2 增强标记裁定)。

**跳过规则评估** (SKILL.md §跳过规则):

```yaml
skip_evaluation:
  C.1:
    check: git status --porcelain   # 等价: git diff --cached --name-status
    skip_if: empty
    reason: "没有需要提交的变更"
```

推演: 暂存区含 3 个新增文件, 非空 → **C.1 不跳过, 执行**。

**入口形态**: Task 直接调用 C.1, 未提供 branch-finisher 输出 (`completion_option` / `validation_report` / `worktree_path`)。SKILL.md §branch-finisher 集成 (v1.1.0) 的 `pre_check` 属 branch-finisher 编排入口的约束, 直接 C.1 入口不触发; B.2 验证属 Phase B 产物, 不在 C.1 判定面内。

---

## 2. 分组决策: 1 个 commit, 走 commit-msg-generator (不走 strategic-commit-orchestrator)

按 ten-step-cycle Step 7 / commit-msg-generator §不使用场景 的决策树:

```
需要分组提交？
  └─ 否 (单模块 / 单一功能原子单元)
      └─ commit-msg-generator
```

裁定依据:

1. **单模块**: 3 个文件全部落在 `backend/` 一个模块内 (api / models / tests 三层), 非跨模块协同、非批量文档、非 Phase/Cycle 里程碑 —— strategic-commit-orchestrator 的三个「必须」触发场景一个不中。
2. **单一变更类型**: 全部是同一 feature (`oauth2-social-login`) 的新增文件。git-commit.md §8.2 禁的是「混合不同类型变更 (feat + fix 应分开)」; 测试与实现属同一功能单元, 规范自身示例即如此处理 (commit-msg-generator 示例 1: `routes/auth.py` + `app.py` 同一 feat commit; git-commit.md §9.1: `feat(auth): 添加OAuth登录支持` 单 commit 含实现 + token 存储)。
3. **体量**: 3 个文件, 远低于 §8.2 「50+ 文件应考虑拆分」的阈值。

被否决的替代方案:

| 替代方案 | 否决理由 |
|----------|----------|
| 拆 `feat` (api+model) + `test` 两个 commit | 破坏功能原子性; 规范示例不支持; TDD RED/GREEN 分段提交属 Phase B 开发期 lane, 不属 C.1 集成批 |
| strategic-commit-orchestrator 编排 | 其触发条件 (跨模块/批量/里程碑) 均不成立 |
| Task 措辞 "commits" 复数 | 指「符合 Conventional Commits 规范的提交」, skill 的 C.1 output schema 即单 `commit_sha` / 单 `commit_message`; 分组条件不成立时不因复数措辞强拆 |

---

## 3. commit-msg-generator 执行流程推演 (5 步)

### 3.1 检查暂存区 (步骤 1, 只读命令)

```bash
git diff --cached --name-status
```

预期输出 (git 按路径排序):

```
A  backend/api/auth/github_oauth.py
A  backend/models/oauth_account.py
A  backend/tests/test_github_oauth.py
```

三个 `A` (added) —— 与 Task 声明的 "(new)" 一致。

### 3.2 查看变更详情 (步骤 2, 只读命令)

```bash
git diff --cached
```

推演认知: 新增 GitHub OAuth2 授权流程 —— API 层端点/回调、OAuthAccount 关联模型、对应单元测试。真实执行时此处逐文件读 diff, 提取 body 素材 (见 §4)。

**Rule #7 顺带核对** (secret-hygiene, advisory): OAuth 是硬编码凭据高危面。真实执行时在提交前确认 `github_oauth.py` 无硬编码 `client_secret` / token 字面量 (验证只看「有无敏感名字面量」, 不读 secret value; 强制层由 secret-guard hook 承担)。

### 3.3 分析变更类型, 确定 type 与 scope (步骤 3)

**Type = `feat`**:

- 全部变更是新功能交付 (新社交登录能力), 非 bug 修复 / 文档 / 重构。
- 测试文件不改变裁定: 主导变更是功能本身; 单独 `test` type 用于「仅测试相关」的独立提交, 不适用于随功能交付的测试。

**Scope = `auth`** (git-commit.md §3.2 功能级 scope: `auth` = 认证相关):

- 变更横跨 `api/auth/`、`models/`、`tests/` 三个目录, 共同主题是认证 —— 功能级 scope 比任一目录名都准确。
- 规范先例: git-commit.md §9.1 原文即 `feat(auth): 添加OAuth登录支持 / Add OAuth login support` (同类场景)。
- 次选 `feat(backend)` (§3.1 模块级) 可接受但精度低; `feat(api)` 只点名三个目录之一, 最差。

**Subject 裁定**: 双语格式 `<中文描述> / <English description>` (git-commit.md §1.1 强制); 祈使语气; ≤72 字符; 结尾无句号。

- 取值: `feat(auth): 添加 GitHub OAuth2 社交登录 / Add GitHub OAuth2 social login` (66 字符, ≤72 ✓)
- 已知规范内微冲突如实记录: commit-msg-generator SKILL 写 subject ≤50 字符, standards SOT v2.1.0 (较新, CLAUDE.md 指定的提交规范 SOT) 写 ≤72; 双语 subject 结构性偏长, 按 SOT 的 72 执行。同理, §1.2 写「首字母小写 (英文部分)」但两份规范的全部成例 (§2 表、§9.1) 英文部分均大写开头 —— 按成例取 `Add`。

### 3.4 Footer 裁定 (COMMIT_FOOTER_GUIDE 决策树)

- **Spec 关联**: feature 名 `oauth2-social-login` 即 spec change_id (Rule #1: 需求变更必须有 OpenSpec)。取 `Spec: openspec/changes/oauth2-social-login/proposal.md`。
  - 路径依据 Rule #5 (项目变更放本项目 `openspec/changes/`, 不放 `standards/openspec/changes/` —— 后者是 git-commit.md §6.2 示例的旧写法); 文件名按当前 spec 布局取 Level 2+ 主文件 `proposal.md` (十步循环模板写 `spec.md` 属旧布局)。真实执行时以仓内该 spec 目录实际文件名校正。
- **Closes/Refs #N**: Task 未给 issue 号, 决策树走「无 → 不写」—— **不虚构 issue 关联**。
- **BREAKING CHANGE**: 纯新增功能, 无 API 签名/响应格式/删除类不兼容变更 → 不写, subject 不带 `!`。

### 3.5 增强标记裁定 (步骤 5: 仅编排模式附加)

phase-c-integrator C.1 params 传 `enhanced_markers: true` 且 `subagent_type` / `phase_cycle` / `module` 均 "from_context" —— **本 Task 上下文未提供这三项**。裁定: **不附加增强标记**, 双依据收敛:

1. ENHANCED_MARKERS_SPEC: `phase_cycle` 必须取自 UPMv2-STATE 真值 (类型 A/B/C 来源), 格式约束为真实 `Phase[N]-Cycle[M]` —— 参数缺席时不得虚构; commit-msg-generator v2.0.0: 参数可选, 不传时与 v1.0.0 行为一致 (无标记)。
2. git-commit.md §5.1: 单模块简单变更 → 不需要增强标记 (commit-msg-generator 独立模式)。

若编排方后续补齐上下文, 追加块严格为 (位置: body 之后、footer 之前, 标记间各空一行):

```
🤖 Executed-By: backend-architect subagent

📋 Context: PhaseN-CycleM oauth2-social-login

🔗 Module: backend
```

(值以真实传入为准; 上块仅格式示意。)

---

## 4. 生成产物

### 4.1 Commit message (最终)

```
feat(auth): 添加 GitHub OAuth2 社交登录 / Add GitHub OAuth2 social login

实现 GitHub OAuth2 社交登录后端 (oauth2-social-login):

- 新增 OAuth2 授权/回调端点 (backend/api/auth/github_oauth.py)
- 新增 OAuthAccount 第三方账号关联模型 (backend/models/oauth_account.py)
- 新增 OAuth 流程单元测试 (backend/tests/test_github_oauth.py)

Spec: openspec/changes/oauth2-social-login/proposal.md
```

### 4.2 执行命令 (真实运行时执行; 本次推演**未执行**)

按 git-commit.md §10.2 的 heredoc 形式 (用 `<<'EOF'` 引号锁定, 防内容中反引号/`$` 被命令替换 —— shell-jq-CRLF hygiene 同族陷阱):

```bash
git commit -m "$(cat <<'EOF'
feat(auth): 添加 GitHub OAuth2 社交登录 / Add GitHub OAuth2 social login

实现 GitHub OAuth2 社交登录后端 (oauth2-social-login):

- 新增 OAuth2 授权/回调端点 (backend/api/auth/github_oauth.py)
- 新增 OAuthAccount 第三方账号关联模型 (backend/models/oauth_account.py)
- 新增 OAuth 流程单元测试 (backend/tests/test_github_oauth.py)

Spec: openspec/changes/oauth2-social-login/proposal.md
EOF
)"
```

提交后取 SHA (只读): `git rev-parse --short HEAD`。

**Hook 失败处理** (SKILL.md §错误处理): 若 commit 被 hook 拒绝 → `action: stop`, 报告 hook 错误信息 + 缺失标记/格式问题, next_step = 用 commit-msg-generator 重新生成; 不绕过 hook。

### 4.3 C.1 输出 (SKILL.md output schema)

```yaml
success: true
steps_executed: [C.1]
steps_skipped: []
results:
  C.1:
    commit_sha: "<待真实 git commit 后由 git rev-parse --short HEAD 回填 — 推演未执行, 无真实 SHA>"
    commit_message: "feat(auth): 添加 GitHub OAuth2 社交登录 / Add GitHub OAuth2 social login"
context_for_next:
  commit_sha: "<同上>"
```

终端呈现 (按 SKILL.md §输出格式, 仅 C.1 面):

```
╔══════════════════════════════════════════════════════════════╗
║              PHASE C - INTEGRATION                           ║
╚══════════════════════════════════════════════════════════════╝

  C.1 commit-msg-generator  → Git 提交   [本次范围]
  C.2 branch-manager        → 创建 PR    [未开始]

  ✅ C.1 (推演完成) → Commit: <SHA 待真实提交后回填>
     Message: feat(auth): 添加 GitHub OAuth2 社交登录 / Add GitHub OAuth2 social login
```

---

## 5. 合规检查清单 (git-commit.md §10.1)

- [x] Type 正确: `feat` (新功能)
- [x] Scope 合适: `auth` (功能级, 覆盖 api/models/tests 三处触点)
- [x] Subject 双语: 中文 / English
- [x] Subject 祈使语气 / ≤72 字符 (66) / 无句号
- [x] Body 列表说明具体变更, 每行 ≤72 字符
- [x] 无 AI 签名: 不含 `Co-Authored-By: Claude...` / `Generated with Claude Code` (git-commit.md §8.1 绝对禁止; owner 2026-09-27 裁定)
- [x] 关联 Spec: `Spec: openspec/changes/oauth2-social-login/proposal.md` (Rule #1 + Rule #5)
- [x] 不虚构: 无 issue 号不写 Closes/Refs; 无上下文不写增强标记; 推演不产出假 commit SHA
- [x] 无 BREAKING CHANGE 声明 (纯新增, 不兼容面为零)

---

## 6. 边界与后续

- **本 Task 到 C.1 为止**。C.2 (branch-manager: 推分支 + 建 PR) 及其后的 C.2.4 pre-merge precondition gate (CI passing + main 无 in-flight; 主干名取项目真值勿照抄字面 `main`, #137)、C.2.4.5 submodule gate、C.2.5 multi-remote push 均**不在本 Task 范围且未执行** —— 且在 eval 约束下 (禁 git fetch/push、禁 forgejo 写接口) 结构上不可执行, 只可描述。
- Rule #4 (每个提交遵循 Conventional Commits) 已由 §4.1 产物满足; 提交进入 `feature/oauth2-social-login` 类 feature 分支后, Phase D 收尾与 handoff 属后续 Phase, 与 C.1 无涉。

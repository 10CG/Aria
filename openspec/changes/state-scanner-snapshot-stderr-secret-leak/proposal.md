# Proposal: state-scanner snapshot 裸 stderr 泄露收口 (Rule #7)

> **Status**: Draft (待 owner sign-off)
> **Level**: 2 (Minimal — 单一关注点: 把裸 git stderr 换成分类枚举; 零架构变更)
> **Created**: 2026-07-12
> **Source**: `state-scanner-stale-refs-false-parity` 的 post_spec R2 (code-reviewer M-1) 发现; 经 owner 决策**拆出独立 Spec 优先 ship** —— Rule #7 是**不可协商规则**, 不该等一个仍在收敛的架构 Spec (5/5 agent 一致建议)
> **Target**: aria-plugin (子模块 `aria/`)
> **Parent**: [state-scanner-stale-refs-false-parity](../state-scanner-stale-refs-false-parity/proposal.md) (母 Spec 的 F3′ 会把本暴露面**放大 N×M 倍**, 故本 Spec 应**先于**它落地)

---

## Why

`state-scanner` 的部分 collector 把**原始 git stderr** 直接写进 snapshot 的 `errors[]`, 而 snapshot **会被 AI 读进对话**。

**代码里存在两种对立先例** (R2 code-reviewer 实证, owner 复核):

| | 位置 | 行为 |
|---|------|------|
| ✅ **正向** | `collectors/coordination_fetch.py` `_classify_error` | 严格返回**分类短串**。docstring 明写 *"Rule #7 compliance… coerced to short, non-secret strings"* |
| ❌ **反向** | `collectors/git.py:184` (`git_log_failed`) / `git.py:356` (`git_status_failed`) / `collectors/sync.py:150` (`rev_list_failed`) | 直接把 `err.strip()` (**原始 stderr**) 塞进 `soft_error` → `snapshot["errors"]` → **对话** |

**今天的实际风险**: R3 backend-architect 核实, 上述三处的命令 (`git log` / `git status` / `rev-list`) **今天都不触碰带凭据的 remote URL** ⇒ 这是**潜在防御缺口, 不是活跃泄露**。

**但它是一颗定时炸弹**:
1. 母 Spec 的 F3′ 会把 `git fetch` 从「1 个已配好凭据的 origin」扩到「N×M 个 remote」—— **fetch 失败的 stderr 常含 remote URL**。
2. **Layer-2 的 aria-runner 容器用的正是 HTTPS-with-embedded-token 形式的 remote URL** (userinfo 段承载 access token) ⇒ token 会进 snapshot、进对话。
3. `soft_error` 是一个**通用**机制 —— 任何后来的 collector 只要照抄 `git.py` 的写法, 就会复制这个缺陷。

⇒ **先把机制收口, 再让 F3′ 往上加 N×M 条失败路径。** 顺序反了就是在漏水的船上加水龙头。

**Rule #7 是不可协商规则** (CLAUDE.md): secret 命令的 stdout/stderr 不得流入 chat-visible 通道。本 Spec 把 `soft_error` 从「可能承载 secret」变成「结构上不可能承载 secret」。

---

## What Changes

### 1. `soft_error` 的 payload 契约

`CollectorResult.soft_error(kind, detail)` 的 `detail` **不得**接收原始 stderr。

- 统一走**分类器** (提炼 `coordination_fetch._classify_error` 为共享工具, 放 `collectors/_common.py`)。
- 输出枚举: `network_timeout` / `auth_failed` / `not_found` / `permission_denied` / `git_error` / `parse_error` / `timeout` / `unknown`。
- 需要保留可诊断性时, 只允许**结构化的、已知安全的**字段 (exit code / 命令名 / 分类枚举), **永不含 stderr 原文**。

### 2. 收口**全部**已知站点 (grep 全集, 不是「三处」)

> ⚠️ **v1 初稿写「三处」是错的** (R4 code-reviewer X-7 + owner grep 复核)。而 **AC-2 是「grep 断言零处直传」的机械闸** ⇒ 只改 3 处 ⇒ **AC-2 必红 ⇒ Spec 自相矛盾**。
> (好消息: 这个机械闸设计对了 —— **它自己把这个漏洞逼了出来**。)

实测全集 (≥8 处):
- `git.py:184` (`git_log_failed`) / `git.py:356` (`git_status_failed`)
- `sync.py:150` (`rev_list_failed`) / `sync.py:232-235` (`submodule_ls_tree_failed`) / `sync.py:244-247` (`submodule_head_failed`)
- `handoff_multibranch.py:298` / `:334` / `:354`
- `handoff_worktrees.py:348`

**Phase B 必须 grep 全量清扫, 不得只处理本清单** (清单可能仍不全 —— 以 AC-2 的机械断言为准)。

### 2b. 🔴 既有分类器有**两个**, 不是一个 (R4 knowledge-manager)

「提炼 `_classify_error` 为共享工具」这个动作**必须先 grep 全仓枚举所有候选**:

| 位置 | 枚举 |
|------|------|
| `coordination_fetch.py:236` `_classify_error` | `network` / `auth_403` / `non_ff` / `git_missing` / `other` |
| **`issue_scan.py:311` 另一个同名 `_classify_error`** (v1 初稿**完全没提它存在**) | `ERR_CLI_MISSING` / `ERR_TIMEOUT` / `ERR_NETWORK_UNAVAILABLE` / `ERR_AUTH_FAILED` / `ERR_RATE_LIMITED` / `ERR_NOT_FOUND` / `ERR_UNKNOWN` |

⇒ **必须在 Phase A 裁定**: 提炼是否覆盖 `issue_scan` 的版本? 若不覆盖, 说明理由 (两套独立分类器长期共存是否可接受); 若覆盖, 注意 `issue_status.fetch_error` 是**已发布的 schema 字段** (`state-snapshot-schema.md:534`), 语义不得静默改变。

### 2c. 🔴 AC-4 (「`coordination_fetch` 行为逐字节不变」) 与新枚举**不可同时满足**

既有测试断言的是 `coordination_fetch` 的**旧词表** (`network`/`auth_403`/...), 而本 Spec §1 提议的是**新词表** (`network_timeout`/`auth_failed`/...)。**二者矛盾。** Phase A 必须裁定:
- (a) 新词表 + **更新** `coordination_fetch` 的既有测试 (放弃「逐字节不变」, 改为「语义等价 + 测试同步更新」); 或
- (b) 保留旧词表作为共享工具的输出, 新调用点直接复用它 (不发明第三套词表)。

> **下游耦合**: 母 Spec 的 `blocking_unknown` 是 **fail-CLOSED 兜底** (`¬benign_unknown`), 所以**无论选哪套词表, 未登记的值都会被正确阻断** —— 但词表本身仍必须单一, 否则文档/测试三处打架。

### 3. 防复发

- `_common.py` 的 `soft_error` docstring 写死 Rule #7 契约。
- 加一条**机械检查**: grep collector 目录, 断言无 `soft_error(..., err` / `soft_error(..., stderr` 之类的直传模式 (可作为 custom check 或 unit test)。

---

## Impact

| 维度 | 影响 |
|------|------|
| 行为 | snapshot `errors[]` 的 `detail` 从「可能是 git 原文」变成「固定枚举」。**诊断信息变少, 安全性变高** —— 这是有意的取舍。 |
| schema | `errors[].detail` 的取值域收窄。additive-compatible (仍是 string)。 |
| 下游 | state-scanner 输出区块的错误呈现措辞可能需微调。 |
| 母 Spec | 本 Spec 落地后, 母 Spec 的 F3′ 新增的 per-remote `error_kind` **直接复用**同一个分类器, 不必重新发明。 |

---

## Verification — 可证伪锚点

- **AC-1 (靶点必须对齐 §Why 点名的站点)** ⚠️ **v1 初稿的 fixture 打错了靶** (R4 qa-engineer 实证):
  §Why 点名的三处 (`git.py:184` = `git log`; `git.py:356` = `git status`; `sync.py:150` = `git rev-list`) 是**纯本地命令** —— 它们的 argv 里**根本没有 remote URL**, 任何现实失败模式下 stderr 都**不会**出现凭据。⇒ 用「凭据 URL 的失败 fetch」做 fixture, **在未修改代码上就会 PASS** (因为 fetch 路径本来就走 `coordination_fetch._classify_error` 这个 ✅ 正向先例) ⇒ **违反它自己的自我否证闸**。
  **正确的 AC-1**: 令 `git log` / `git status` / `rev-list` **真实失败** (如损坏的对象库 / 缺失的 upstream ref), 断言其 **stderr 原文不落进** `snapshot["errors"]` (改为分类枚举)。**这是一个不涉及凭据的朴素断言**, 但精确命中要修的路径。
- **AC-1b (凭据不泄露, 防 F3′ 引入的新面)**: 构造 **userinfo 段含凭据哨兵值**的 remote URL 令 **fetch** 失败 → 断言 snapshot 全文不含该哨兵。
  > **实施注意 (本 session dogfood 实证)**: 哨兵值本身会**触发 secret-guard hook** (按形状匹配, 不区分真假)。哨兵必须在测试代码里**运行时拼装**, 不得以完整 URL 字面量落在源文件里 —— 否则每次读写该文件都误报。
  > 注: 此条今天可能已 PASS (fetch 路径已有正确分类器) ⇒ 它是**防回归 pin**, 不是缺陷证据。**Spec 不得声称 AC-1b 覆盖了 §Why 的站点。**
- **AC-2 (机制防复发)**: grep collector 目录, 断言零处把原始 stderr 传入 `soft_error`。
- **AC-3 (无回归)**: `python3 aria/skills/state-scanner/tests/run_tests.py` → 0 failed ∧ 无既有绿测试转红。
- **AC-4 (分类器复用)**: `_classify_error` 从 `coordination_fetch.py` 提到 `_common.py` 后, `coordination_fetch` 的既有行为**逐字节不变** (它的现有测试全绿)。

---

## Tasks

- [ ] 1.1 提炼 `_classify_error` 到 `collectors/_common.py` (保持 `coordination_fetch` 行为逐字节不变)
- [ ] 1.2 写 AC-1 红测试 (凭据 sentinel), 确认当前代码 RED
- [ ] 2.1 `git.py:184` / `git.py:356` / `sync.py:150` 改经分类器
- [ ] 2.2 `soft_error` docstring 写死 Rule #7 契约
- [ ] 3.1 AC-2 机械防复发检查 (grep 断言, unit test 或 custom check)
- [ ] 3.2 全量测试无回归 (AC-3) + `coordination_fetch` 行为不变 (AC-4)
- [ ] 4.1 文档: `references/state-snapshot-schema.md` 的 `errors[].detail` 取值域
- [ ] 4.2 版本 bump + SOT 同步 + CHANGELOG (标注: 诊断信息变少是有意取舍)

---

## 关联

- **母 Spec**: `state-scanner-stale-refs-false-parity` (F3′ 放大本暴露面 N×M 倍 ⇒ **本 Spec 应先落地**)
- **Rule #7**: `standards/conventions/secret-hygiene.md` (不可协商)
- **正向先例**: `coordination_fetch._classify_error` (本 Spec 把它提炼为共享工具)
- **memory**: `feedback_secrets_never_in_conversation` / `feedback_nomad_inspect_secret_leak` / `reference_postooluse_cannot_redact_tool_output` (PostToolUse **无法** redact tool_response ⇒ 只能从**源头**不写入)

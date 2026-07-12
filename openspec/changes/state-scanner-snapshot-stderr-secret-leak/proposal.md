# Proposal: state-scanner snapshot 裸 stderr 泄露收口 (Rule #7)

> **Status**: **Draft v2** (v1 → post_spec **R5 FAIL** [三处词表互斥无裁定 / tasks 未跟 §正文 / 0-failed 假前提] → **v2: OQ-B1+OQ-B2 已裁 + tasks 同步 + AC-3/AC-4 可满足化**) → 待 post_spec **R6**
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
- 🔴 **输出枚举 = 沿用 `coordination_fetch` 的既有词表** (**v2 裁定, 见 §2c 的 OQ-B1**): `network` / `auth_403` / `non_ff` / `git_missing` / `other`。
  ⚠️ **v1 初稿提议的第三套词表** (`network_timeout`/`auth_failed`/`permission_denied`/`git_error`/…) **已作废** —— 它与 AC-4 字面互斥, 且**发明第三套词表**正是本 Spec 自己批评的病。
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

### 2c. ✅ **OQ-B1 — 词表裁定 (v2 已裁: 选 (b))**

> ⚠️ **R5-M-4**: v1 **只披露了矛盾、没有裁定它**, 而且 **tasks 里没有任何一条任务承载这个裁定** ⇒ 会被带进 Phase B 临场决定。三方 agent (tech-lead / code-reviewer / knowledge-manager) 独立收敛于此。

**矛盾**: 既有测试断言的是 `coordination_fetch` 的**旧词表** (`network`/`auth_403`/`non_ff`/`git_missing`/`other`), 而 v1 的 §1 提议的是**第三套新词表** ⇒ **AC-4「逐字节不变」与新枚举字面互斥**。

**✅ 裁定 = (b) 保留旧词表** (tech-lead + code-reviewer 一致倾向):
- **不发明第三套词表** —— 发明第三套正是本 Spec 自己批评的病 (代码里已有**两套**同名 `_classify_error`)。
- **blast radius 最小**: `coordination_fetch` 的既有测试**不需要改**; 新调用点直接复用。
- **母 Spec 不受影响**: 母 Spec 的 `blocking_unknown` 与 `has_unreachable_remote` 都是 **fail-CLOSED 兜底** (`¬benign`) ⇒ **无论词表长什么样, 未登记的值都会被正确阻断** (backend-architect R5 实测确认)。

**AC-4 措辞同步修正** (让它变成**可满足的**断言): 从「行为**逐字节不变**」改为「**既有测试全绿 ∧ 枚举标签集合不变**」。
> **为什么不能是「逐字节不变」**: §3b 要**扩充 signal 表**的覆盖 (见下) —— 那会让某条 stderr 从 `other` 变成 `network`, **严格来说不是「逐字节不变」**, 但它**不改变标签集合**, 也不破坏既有测试。「逐字节不变」这个措辞会把一个正确的诊断改进也判为违规。

### 2d. ✅ **OQ-B2 — `issue_scan.py:311` 的第二个 `_classify_error` (v2 已裁: 不合并)**

**裁定 = 两套分类器长期共存, 本 Spec 不合并 `issue_scan` 的版本。** 理由:
1. **`issue_status.fetch_error` 是已发布的 schema 字段** (`state-snapshot-schema.md:534`), 其 `ERR_*` 取值域已被下游消费 ⇒ **语义不得静默改变**。
2. **失败模式不同域**: `issue_scan` 分类的是 **CLI (forgejo/gh) 的失败** (rate limit / CLI 缺失 / API 401), `coordination_fetch` 分类的是 **git 网络/传输失败**。强行合并会造出一个两边都不贴合的枚举。
3. 本 Spec 的靶点是 **Rule #7 的裸 stderr**, 而 `issue_scan` **已经**返回分类枚举 (不泄露 stderr) ⇒ **它不在本 Spec 的攻击面内**。

> ⚠️ **但必须留痕**: `_common.py` 的共享分类器 docstring 写死「本分类器服务 **git 命令**的失败; `issue_scan` 的 CLI 失败有独立分类器 (`issue_scan.py:311`), **有意不合并**, 见本 Spec §2d」—— 否则下一个读代码的人会再问一遍「为什么有两个同名函数」。

### 3b. 🆕 **分类器 signal 覆盖率扩充 (诊断质量, 非正确性)** — R5-C-B 的实测输入

owner 用**生产分类器**跑真实 stderr 实测:

| 真实失败模式 | 今天的 `error_kind` | 应为 |
|---|---|---|
| HTTPS 连不上 (`Failed to connect to <host> port 443`) | `other` 🔴 | `network` |
| HTTPS TLS 握手失败 (`gnutls_handshake() failed`) | `other` 🔴 | `network` |
| TLS 非正常终止 (`The TLS connection was non-properly terminated`) | `other` 🔴 | `network` |
| **SSH 公钥被拒** (`Permission denied (publickey)`) | `other` 🔴 | `auth_403` |
| SSH 连接超时 | `network` ✅ | — |
| DNS 解析失败 | `network` ✅ | — |

**根因**: `network_signals` (`coordination_fetch.py:254-262`) 只有 `could not resolve` / `connection refused` / `timed out` / `ssl` / `network` / `unable to connect` / `fatal: repository` ——
- 真实 stderr 说的是 `unable to **access**` 和 `failed to connect`, **不是** `unable to connect`
- 有 `"ssl"` 但**没有 `"tls"`**

⇒ **扩充 signal 表**: 加 `unable to access` / `failed to connect` / `couldn't connect` / `tls` / `permission denied` (→ `auth_403`)。

> ⚠️ **这是诊断质量改进, 不是正确性修复**。母 Spec 的 `has_unreachable_remote` 是 **fail-CLOSED** ⇒ `other` 一样会置位 ⇒ **正确性不依赖 signal 覆盖率**。
> 但**诊断信息的价值依赖它** —— 用户看到「network error」比看到「failed with rc=128」有用得多。

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
- **AC-3 (无回归)** 🔴 **v2 修正 baseline 假前提 (R5-C-E)**:
  `python3 aria/skills/state-scanner/tests/run_tests.py` → **0 failed, 除 `test_two_consecutive_runs_diff_zero`** ∧ 无既有绿测试转红。
  > ⚠️ **v1 写的「0 failed」是假前提** —— owner 连跑两次实测 (未修改代码): `Ran 1006 tests ... FAILED (failures=1)`, 失败的正是 `test_two_consecutive_runs_diff_zero` (**4 条 run-to-run 漂移通道**: `remote_refs_age` / `issue_status.repos[].source` / `coordination_fetch.degraded` / `errors[]`)。
  > **本 Spec 既不碰这 4 条中的任何一条** ⇒ 若坚持「0 failed」, **本 Spec 在自己的 PR 上结构性恒红 ⇒ 按自己的闸门无法 ship** —— 而它恰恰是被指定「**应先落地**」的那一个。
  > ⇒ **该测试由母 Spec 认领消除** (母 Spec tasks 12.10)。本 Spec 显式豁免它。
- **AC-4 (分类器复用)** 🔴 **v2 措辞修正 (R5-M-4; 见 §2c OQ-B1 裁定)**:
  `_classify_error` 从 `coordination_fetch.py` 提到 `_common.py` 后 —— **`coordination_fetch` 的既有测试全绿 ∧ 枚举标签集合不变** (`network`/`auth_403`/`non_ff`/`git_missing`/`other`)。
  > ⚠️ **v1 写的「行为逐字节不变」与 §1 的新词表字面互斥**, 且会把 §3b 的**正确诊断改进**也判为违规。**裁定 (b) 保留旧词表后, 矛盾消解。**

---

## Tasks

### 0. 前置裁决 (v2 新增 — R5-M-4: v1 只披露矛盾、无任务承载裁定)

- [x] 0.1 ✅ **OQ-B1 词表裁定**: **(b) 保留 `coordination_fetch` 旧词表** (`network`/`auth_403`/`non_ff`/`git_missing`/`other`), **不发明第三套**。见 §2c
- [x] 0.2 ✅ **OQ-B2 `issue_scan._classify_error` 裁定**: **两套长期共存, 本 Spec 不合并** (`issue_status.fetch_error` 是已发布 schema 字段 + 失败模式不同域 + 它已返回枚举不泄露 stderr)。见 §2d

### 1-4. 实施

- [ ] 1.1 提炼 `_classify_error` 到 `collectors/_common.py` (**按 0.1 的裁定: 保留旧词表标签; 既有测试全绿**)
- [ ] 1.2 🔴 **写 AC-1 红测试 (v2 修正靶点 — R5-M-3)**: 令 `git log` (`git.py:184`) / `git status` (`git.py:356`) / `git rev-list` (`sync.py:150`) **真实失败** (损坏对象库 / 缺失 upstream ref), 断言其 **stderr 原文不落进 `snapshot["errors"]`**。确认当前代码 **RED**。
      ⚠️ **v1 写的「凭据 sentinel 红测试」打错了靶** (R4 qa-engineer 实证): 那三处是**纯本地命令**, argv 里根本没有 remote URL ⇒ 用「凭据 URL 的失败 fetch」做 fixture, **在未修改代码上就会 PASS** ⇒ **违反它自己的自我否证闸**。凭据哨兵归 **1.3 (AC-1b)**, 那是**防回归 pin**, 不是缺陷证据
- [ ] 1.3 **AC-1b 防回归 pin**: userinfo 段含凭据哨兵的 remote URL 令 **fetch** 失败 → snapshot 全文不含哨兵。**哨兵必须运行时拼装** (完整字面量会触发 secret-guard hook, 按形状匹配不区分真假)
- [ ] 2.1 🔴 **收口全部站点 (v2 修正 — R5-M-3: v1 只写 3 处, 实测 ≥9 处)**:
      `git.py:184` / `git.py:356` / `sync.py:150` / `sync.py:232-235` / `sync.py:244-247` / `handoff_multibranch.py:298` / `:334` / `:354` / `handoff_worktrees.py:348` —— **全部改经分类器**。
      ⚠️ **Phase B 必须 grep 全量清扫, 不得只处理本清单** (清单可能仍不全 —— **以 AC-2 的机械断言为准**)。
      > **v1 的 §2 已改对成「全集」, 但 tasks 2.1 还停在「三处」** ⇒ **Phase B 执行的是 tasks, 不是 §Why** ⇒ 按 tasks 干 ⇒ **AC-2 (grep 断言零处直传) 必红** ⇒ 矛盾只是**从 §Why 搬进了 Tasks**
- [ ] 2.2 `soft_error` docstring 写死 Rule #7 契约
- [ ] 2.3 🆕 **`_common.py` 共享分类器 docstring 留痕** (按 0.2): 「本分类器服务 **git 命令**失败; `issue_scan` 的 CLI 失败有独立分类器 (`issue_scan.py:311`), **有意不合并**, 见 Spec §2d」
- [ ] 3.1 AC-2 机械防复发检查 (grep 断言, unit test 或 custom check)
- [ ] 3.2 全量测试无回归 (**AC-3, 豁免 `test_two_consecutive_runs_diff_zero`**) + `coordination_fetch` 既有测试全绿 + 标签集合不变 (AC-4)
- [ ] 3.3 🆕 **扩充 signal 表覆盖率** (§3b, **诊断质量非正确性**): 加 `unable to access` / `failed to connect` / `couldn't connect` / `tls` → `network`; `permission denied` → `auth_403`。
      **实测输入** (owner 跑生产分类器): 5 种真实故障 **3 种落 catch-all `other`** (HTTPS 连不上 / TLS 握手失败 / **SSH 公钥被拒**)。
      ⚠️ **母 Spec 的正确性不依赖此项** (`has_unreachable_remote` 是 fail-CLOSED, `other` 一样置位) —— 但**诊断信息的价值依赖它**
- [ ] 4.1 文档: `references/state-snapshot-schema.md` 的 `errors[].detail` 取值域
- [ ] 4.2 版本 bump + SOT 同步 + CHANGELOG (标注: 诊断信息变少是有意取舍)

---

## 关联

- **母 Spec**: `state-scanner-stale-refs-false-parity` (F3′ 放大本暴露面 N×M 倍 ⇒ **本 Spec 应先落地**)
- **Rule #7**: `standards/conventions/secret-hygiene.md` (不可协商)
- **正向先例**: `coordination_fetch._classify_error` (本 Spec 把它提炼为共享工具)
- **memory**: `feedback_secrets_never_in_conversation` / `feedback_nomad_inspect_secret_leak` / `reference_postooluse_cannot_redact_tool_output` (PostToolUse **无法** redact tool_response ⇒ 只能从**源头**不写入)

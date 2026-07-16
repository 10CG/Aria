# Proposal: state-scanner snapshot 裸 stderr 泄露收口 (Rule #7)

> **Status**: **✅ Approved v5 (owner sign-off 2026-07-15)** (v1 → **R5 FAIL** → **v2** → **R6 [1C+4M+5m]** → **v3** → **R7 [1C fix-introduced+2M+2m]** → **v4** → **R8 [1C fix-introduced+3M+1m]** → **v5 [option B 重框: 类型化通道=结构保证 / 助手内部自分类 / AC-2 降 best-effort / code-review 作完整性闸]**)。落地顺序 C→B→主 不变; owner 终审通过, 退出 sound-AC-2 审计循环。
> **R8 (2026-07-15, 单聚焦 AC-2 专验) + owner meta 裁定 (option B)**: 连续三轮 (R6→R7→R8) fix-introduced Critical **全集中在把 AC-2 做成可证明 sound 的全目录静态检查** (name-grep 3/9 → `.stderr` grep 0/9 → `_run` 第三返回值 intra-procedural 漏跨函数逃逸) —— memory `feedback_selfreferential_antifalsegreen_plan_needs_more_audit_rounds` 实证。**owner 裁 option B 重框**: **真正的结构级保证 = GitErrorClass 类型化通道本身** (返回类型无 stderr 字段, 凡经它 stderr 结构上到不了 snapshot); **AC-2 降为 best-effort lint** (只扫本 spec 改动的 in-scope 文件 intra-procedural + known-bad grep), 完整性靠 refactor 被 code-review 而非 AC-2 可证 sound。**v5 折入 R8 C-1 干净解**: M-a 助手改**内部自分类** (`if rc: if benign: return [],None; else: return [], classify_git_error(...)`, stderr+benign-gate 全留助手内, 不再跨函数逃逸 stderr) —— 严格优于 v3/v4 的"return (rc,stderr) 到 callsite 再分类", 使 in-scope AC-2 lint 保持 intra-procedural 干净。minors: M-1 `:195` 非"永不 emit" 刻画修正 / Major-3 `return _run(...)` 整包逃逸记为 lint 已知局限 (out-of-scope issue_scan) / minor 委托测试锚点勘误。
> **R7 (2026-07-15, 单聚焦 code-grounded, confirm 轮)**: 结构概念 (GitErrorClass 类型层消灭 stderr) + M-a/M-b/M-c 诊断**全部确认成立** + §2 泄露站点清单实为完整 (67 处 soft_error 普查交叉核对无漏)。但抓到 **fix-introduced C-1**: v3 的 AC-2 断言"`.stderr` 字段读取只被分类器消费"**建在不存在的数据流上** —— 真代码子进程走 `_run() -> tuple[int,str,str]` + 位置元组解包 `rc,out,err=`, 全目录无任何 `.stderr` 属性访问 ⇒ 按字面命中 **0/9** 真站点 (比 v2 名字 grep 的 3/9 更糟, 假绿模式换皮)。**v4 折入** (memory `feedback_multiround_audit_catches_fix_introduced_regression` 实证): **C-1** AC-2 靶点改**对 `_run(...)` 返回元组第三元素做污点追踪** (AST: 只能丢弃或流入分类器, 不得进 soft_error), 非 `.stderr` grep; **M-1** 白名单放行 benign-gate 谓词 (读 stderr→bool 永不 emit, 如 `coordination_fetch.py:419` / `handoff_multibranch.py:195`); **M-2** 内部矛盾 (M-b vs AC-4) → 写死 coordination_fetch **委托** `classify_git_error().label` 只留自己 label→措辞层 (signal 表单一 SOT); minors (助手改 (rc,stderr) 保全 benign-skip / §1 二分补 stdout 类)。
> **R6 (2026-07-15, 3-agent code-grounded, 聚合 `.aria/audit-reports/post_spec-R6-2026-07-15-state-scanner-snapshot-stderr-secret-leak-aggregated.md`)**: R5 三根因逐条真修确认 + 两裁定 load-bearing 正确 + 无 design flaw。**v3 折入** (owner 2026-07-15 裁 option A 结构级): **C1** AC-2 grep 不 sound → 改**类型化分类通道** (`classify_git_error` 返回类型无 stderr 字段, AC-2 改断言 `.stderr` 字段读取只被分类器消费 = 有界 sound 不变量); **M-a** tasks 指向转发点 → 补 4 个 stderr 烘焙助手真 sanitize 行; **M-b** message 硬编码 fetch → 提炼只搬 (rc,stderr)→label 映射, detail 由各 callsite 按命令名现构; **M-c** multi_remote 第三套词表 → §2b 补普查 + Impact 降级复用承诺; **M-d** "结构上不可能"溢美 → 与类型化通道对齐 (真结构级); minors 全折 (permission denied publickey 守卫 / OQ-B2 理由改挂 schema 字段 / AC-4 断言载体 / §3b 分割不变量)。母 Spec R9 Approved; 落地顺序 C→B→主 不变。
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

**Rule #7 是不可协商规则** (CLAUDE.md): secret 命令的 stdout/stderr 不得流入 chat-visible 通道。本 Spec 通过**类型化分类通道** (§What.1) 把子进程 stderr 收口: 每个子进程 stderr 站点 (含烘焙助手) 都 refactor 成经 `classify_git_error` 产 `GitErrorClass` (返回类型**无 stderr 字段**), stderr 进分类器即消失, 只有无 stderr 的结构体到达 `soft_error`。**结构级保证 = 这条类型化通道本身** (危险入参从 emit 路径的类型上不可达, memory `feedback_structural_antispoof_unreachable_not_safe_default`): 完整性靠"每个 stderr 站点都改经通道"这个 refactor 被 **code-review** 确认, 而非靠 AC-2 做成可证明 sound 的全目录静态分析 (v5/option B — 三轮实证该静态闸极难精确规约; AC-2 降为 best-effort lint 辅助, 见 §3/AC-2)。

---

## What Changes

### 1. 类型化分类通道 (v3 — option A 结构级, owner 2026-07-15 裁; 取代 v2 的"约定 + docstring")

**问题 (R6 C1+M-d)**: v2 只加 docstring 契约 + 顾问 grep, `soft_error(kind, detail: str)` 签名不变 ⇒ 原始 stderr 仍能自由传入 ⇒ "结构上不可能"是溢美, 且 AC-2 名字 grep 不 sound (漏 f-string/中间变量洗白形, 见 §Verification AC-2)。

**v3 结构级设计**: 给**子进程 stderr** 建一条类型化通道, 使原始 stderr 从 emit 路径的**类型上不可达**:

```python
# collectors/_common.py
@dataclass(frozen=True)
class GitErrorClass:
    label: str          # 5 枚举之一 (见下)
    rc: int
    cmd: str            # 命令名, 如 "git log" / "git status" / "git rev-list"
    # ⚠️ 无 stderr 字段 — 结构上不可能承载 stderr 原文

def classify_git_error(rc: int, stderr: str, cmd: str) -> GitErrorClass:
    label = _map_signals(rc, stderr)   # stderr 在此被消费 → 丢弃, 不进返回值
    return GitErrorClass(label=label, rc=rc, cmd=cmd)
```

- **choke point**: 子进程 stderr **只能**被 `classify_git_error` 读取; 它消费 stderr 产出无 stderr 的 `GitErrorClass`。callsite 拿到的是结构体, 用 `(label, rc, cmd)` **现构** human-readable detail (M-b: 命令名各站点自带, 不硬编码 fetch)。
- 🔴 **输出枚举 = 沿用 `coordination_fetch` 的既有词表** (**v2 裁定, 见 §2c 的 OQ-B1**): `network` / `auth_403` / `non_ff` / `git_missing` / `other`。
  ⚠️ **v1 初稿提议的第三套词表** (`network_timeout`/`auth_failed`/`permission_denied`/`git_error`/…) **已作废** —— 它与 AC-4 字面互斥, 且**发明第三套词表**正是本 Spec 自己批评的病。
- **提炼 = 搬移共享 + 委托, 不复制** (M-b R6 + M-2 R7 消歧): `(rc, stderr) → label` 的**信号映射逻辑搬到 `_common.py` 的 `classify_git_error` 作单一 SOT**; `coordination_fetch._classify_error` **委托** `classify_git_error(rc, stderr, "git fetch").label` 拿 label, **只保留自己的 `label → "git fetch ..." 措辞映射层**。
  > 🔴 **R7 M-2 内部矛盾**: v3 措辞"coordination_fetch 保留自己 fetch 包装层"易被读作"保留自己整个 `_classify_error` (含信号映射)" ⇒ label 映射复制成两份 (本 spec 批评的"两个同名分类器"病升级成三份), 且 §3b 扩 signal 表只扩一份 ⇒ coordination_fetch 诊断保持陈旧。**委托读法消除此矛盾**: signal 表单一 SOT (扩一处全生效); coordination_fetch 保留 label→"git fetch" 措辞层, label 集不变故其相关测试不破; 新站点用自己 `cmd` 现构 detail (`git log` 失败显示 "git log ..." 非误导的 "git fetch ...")。
  > 📌 **测试锚点勘误 (R8 minor-1)**: `test_p1_layer_h.py:446` 的 "git fetch network error (rc=128)" 实为 `_make_degraded_snapshot()` **手搓 fixture 字面量**, **不 call `_classify_error`** —— 全测试库无一处直接断言 `coordination_fetch._classify_error` 输出 (只 issue_scan 版有)。故"委托不破测试"成立但更弱 (没测试锚它); 委托实施留意 fixture 与真分类器输出的漂移 (fixture 说一套分类器产一套时无测试兜底)。
- **非 stderr 的 detail 不受影响**: 其余 callsite 传 `str(e)` 异常消息 / `f"rc={rc}"` / 文件路径 / **命令 stdout** (`sync.py:162/177` `f"...{out!r}"`, rev-list 计数输出 — R7 m-2: 非 stderr 非 str(e), 但同样在攻击面外) 的 **都不是 stderr 泄露向量**, 签名对它们保持 `detail: str` 不变 (blast radius 仅限约 9 处子进程 stderr 站点 + 4 个烘焙助手, 见 §2/Tasks 2.1) —— 定级 L2 站得住。

### 2. 收口**全部**已知站点 (grep 全集, 不是「三处」)

> ⚠️ **v1 初稿写「三处」是错的** (R4 code-reviewer X-7 + owner grep 复核)。而 **AC-2 是「grep 断言零处直传」的机械闸** ⇒ 只改 3 处 ⇒ **AC-2 必红 ⇒ Spec 自相矛盾**。
> (好消息: 这个机械闸设计对了 —— **它自己把这个漏洞逼了出来**。)

实测全集 (≥8 处):
- `git.py:184` (`git_log_failed`) / `git.py:356` (`git_status_failed`)
- `sync.py:150` (`rev_list_failed`) / `sync.py:232-235` (`submodule_ls_tree_failed`) / `sync.py:244-247` (`submodule_head_failed`)
- `handoff_multibranch.py:298` / `:334` / `:354`
- `handoff_worktrees.py:348`

**Phase B 收口本清单全部站点, 且 refactor 须经 code-review 确认完整性** (v5/option B: 完整性靠"每个 stderr 站点改经类型化通道"被 review, 非靠 AC-2 可证 sound; AC-2 是 best-effort lint 辅助, 见 §3/§Verification AC-2)。

### 2b. 🔴 既有分类逻辑有**三处**, 不是两个 (R4 knowledge-manager + R6-M-c spec-completeness)

「提炼 `_classify_error` 为共享工具」这个动作**必须先 grep 全仓枚举所有候选**:

| 位置 | 枚举 | 与本 Spec 关系 |
|------|------|------|
| `coordination_fetch.py:236` `_classify_error` | `network` / `auth_403` / `non_ff` / `git_missing` / `other` | ✅ **提炼源** (git 网络域) |
| **`issue_scan.py:311` 另一个同名 `_classify_error`** (v1 初稿**完全没提它存在**) | `ERR_CLI_MISSING` / `ERR_TIMEOUT` / `ERR_NETWORK_UNAVAILABLE` / `ERR_AUTH_FAILED` / `ERR_RATE_LIMITED` / `ERR_NOT_FOUND` / `ERR_UNKNOWN` | CLI 域, **有意不合并** (OQ-B2, §2d) |
| 🆕 **`multi_remote.py:255-266` 内联分类块** (v2 及以前**漏普查** — R6-M-c) | `network_timeout` / `auth_failed` / `not_found` / `remote_branch_missing` / `parse_error` (信号词与 coordination_fetch **不同**) | 落 `reason` **结构化字段非裸 stderr** ⇒ **不在本 Spec Rule#7 攻击面内, 本 Spec 不改**; 但它恰是母 Spec F3′ 的 per-remote collector |

⇒ **裁定 (v3)**: 提炼覆盖 `coordination_fetch` (git 网络域); `issue_scan` 有意不合并 (OQ-B2); `multi_remote` 的第三套词表 **本 Spec 不动** (它已不泄 stderr), 但**归母 Spec 另裁词表归一** (见 Impact) —— 本 Spec 不再声称"母 Spec 直接复用同一分类器"。若合并 issue_scan, 注意 `issue_status.fetch_error` 是**已发布的 schema 字段** (`state-snapshot-schema.md:534`), 语义不得静默改变。

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
1. **`issue_status.fetch_error` 是已发布的 schema 字段** (`state-snapshot-schema.md:534`), 且其 `ERR_*` 值会成为 snapshot `errors[].kind` (`issue_scan.py:642` 用 `ferr` 当 kind) ⇒ **kind 面已暴露, 语义不得静默改变** (R6-m2 勘误: 原写"取值域已被下游消费"核不实 — 实测 `ERR_*` 值只被 issue_scan 自身测试消费, 无生产渲染层按值分支; 真护栏是"已发布 schema 字段 + kind 面暴露", 非"下游已消费")。
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

⇒ **扩充 signal 表**: 加 `unable to access` / `failed to connect` / `couldn't connect` / `tls` (→ `network`); `permission denied (publickey)` (→ `auth_403`)。

> 🔴 **R6-m1 守卫**: `permission denied` **不得**裸配 → `auth_403`。`git` 对**本地文件系统**权限不足也吐 `Permission denied` (非 SSH publickey) ⇒ 裸匹配会把本地 FS 错误误标成鉴权错。**收紧为 `permission denied (publickey)`** 或加 SSH 上下文守卫 (仅当 stderr 同时含 SSH 语境)。
>
> 🔴 **R6-m4 分割不变量** (memory `feedback_predicate_tiers_need_total_partition_proof`): signal 表分支求值顺序 = **auth 分支先于 network 分支**。扩充多个 signal 后必须证 **(1) 分支两两互斥** (无一条 stderr 同时命中 auth 和 network 而结果依赖顺序) **(2) 补集全覆盖** (未命中任何 signal ⇒ catch-all `other`, fail-CLOSED)。§3b 扩充须附一句分割证明或反例 fixture。

> ⚠️ **这是诊断质量改进, 不是正确性修复**。母 Spec 的 `has_unreachable_remote` 是 **fail-CLOSED** ⇒ `other` 一样会置位 ⇒ **正确性不依赖 signal 覆盖率**。
> 但**诊断信息的价值依赖它** —— 用户看到「network error」比看到「failed with rc=128」有用得多。

### 3. 防复发 (v5 — 结构级保证=类型化通道; AC-2 降 best-effort lint, option B)

> 🔴 **R6 C1**: v2 的机械检查 = grep `soft_error(..., err` / `..., stderr` **不 sound** —— 只命中约 9 处清单里的 3 处, 漏 **f-string 内嵌形** (`sync.py:232` `f"path=... err={err.strip()}"`) 和 **中间变量洗白形** (`handoff_multibranch.py:298` 的 `list_err` / `handoff_worktrees.py:348` 的 `enum_err`, 值在 40 行外助手拼好)。基于变量名的 grep 结构上无法检测"这个实参是不是原始 stderr"。而 spec 又把 AC-2 当"完整性权威闸"支撑"清单可能不全但 AC-2 兜住" ⇒ 假绿闸。

- `_common.py` 的 `soft_error` docstring + `GitErrorClass` docstring 写死 Rule #7 契约。
- **结构级保证 = 类型化通道** (非 AC-2): 见 §What.1 —— 每个子进程 stderr 站点 refactor 成经 `classify_git_error` 产 stderr-free `GitErrorClass`; 完整性由此 refactor 被 **code-review** 确认。**AC-2 是 best-effort lint 辅助, 不承担"可证明 sound 完整性兜底"** (v5/option B — 三轮 R6/R7/R8 实证: name-grep 3/9 → `.stderr` grep 0/9 → `_run` 第三返回值 intra-procedural 漏跨函数逃逸, 该全目录静态闸极难精确规约)。
- **助手内部自分类** (v5 R8 C-1 干净解, 取代 v3/v4 的"助手 return (rc,stderr) 到 callsite 再分类"): stderr 烘焙助手 (`handoff_multibranch.py:146/198/233` `_list_origin_branches`/`_list_handoff_files`/`_read_file_content`, `handoff_worktrees.py:140` `_list_worktrees`) 改为**在助手内部**分类: `if rc: if benign(stderr): return [],None; else: return [], classify_git_error(rc,stderr,cmd)` —— 返回 `GitErrorClass`/label + benign-skip **都留在助手内, stderr 绝不跨函数逃逸**。收益: (1) stderr 整个生命周期 intra-procedural, best-effort lint 单文件内即可确认助手不 emit 原文; (2) 消解 v4 担心的"benign-skip 搬 callsite"(留助手内即可); (3) 消解多跳盲区 (`:332` `f"[{branch}] {ls_err}"` 的 `ls_err` 变 label 非原文 stderr)。
  > **benign-gate 刻画修正 (R8 Major-2)**: 只有 `coordination_fetch.py:114 _is_benign_coordination_absent(rc,stderr)→bool` 是**纯谓词** (独立函数, 零 emit)。`handoff_multibranch.py:195` **不是**"永不 emit" —— 同一 `stderr` 绑定 `:195 .lower()` 判 benign **且** `:198` 就拼进 return (emit), 仅 3 行之隔; 助手内部自分类后该 emit 变 `classify_git_error`, benign 判定与分类同处助手内, 按 use 区分不再需要跨函数白名单。

---

## Impact

| 维度 | 影响 |
|------|------|
| 行为 | snapshot `errors[]` 的 `detail` 从「可能是 git 原文」变成「固定枚举」。**诊断信息变少, 安全性变高** —— 这是有意的取舍。 |
| schema | `errors[].detail` 的取值域收窄。additive-compatible (仍是 string)。 |
| 下游 | state-scanner 输出区块的错误呈现措辞可能需微调。 |
| 母 Spec | 本 Spec 落地后, 母 Spec 的 F3′ 新增的 per-remote `error_kind` **可复用** `classify_git_error` 的 `(rc,stderr)→label` 映射。⚠️ **v3 降级 (R6-M-c)**: `multi_remote.py:255-266` 已有**第三套不兼容词表** (`network_timeout`/`auth_failed`/`not_found`) —— "直接复用同一分类器"是过度声称; **母 Spec 需另裁 multi_remote 词表归一** (合并到 `classify_git_error` 还是保留), 不属本 Spec 范围。 |

---

## Verification — 可证伪锚点

- **AC-1 (靶点必须对齐 §Why 点名的站点)** ⚠️ **v1 初稿的 fixture 打错了靶** (R4 qa-engineer 实证):
  §Why 点名的三处 (`git.py:184` = `git log`; `git.py:356` = `git status`; `sync.py:150` = `git rev-list`) 是**纯本地命令** —— 它们的 argv 里**根本没有 remote URL**, 任何现实失败模式下 stderr 都**不会**出现凭据。⇒ 用「凭据 URL 的失败 fetch」做 fixture, **在未修改代码上就会 PASS** (因为 fetch 路径本来就走 `coordination_fetch._classify_error` 这个 ✅ 正向先例) ⇒ **违反它自己的自我否证闸**。
  **正确的 AC-1**: 令 `git log` / `git status` / `rev-list` **真实失败** (如损坏的对象库 / 缺失的 upstream ref), 断言其 **stderr 原文不落进** `snapshot["errors"]` (改为分类枚举)。**这是一个不涉及凭据的朴素断言**, 但精确命中要修的路径。
- **AC-1b (凭据不泄露, 防 F3′ 引入的新面)**: 构造 **userinfo 段含凭据哨兵值**的 remote URL 令 **fetch** 失败 → 断言 snapshot 全文不含该哨兵。
  > **实施注意 (本 session dogfood 实证)**: 哨兵值本身会**触发 secret-guard hook** (按形状匹配, 不区分真假)。哨兵必须在测试代码里**运行时拼装**, 不得以完整 URL 字面量落在源文件里 —— 否则每次读写该文件都误报。
  > 注: 此条今天可能已 PASS (fetch 路径已有正确分类器) ⇒ 它是**防回归 pin**, 不是缺陷证据。**Spec 不得声称 AC-1b 覆盖了 §Why 的站点。**
- **AC-2 (best-effort lint, v5 重框 — option B)**: **结构级保证由类型化通道承担 (§What.1/§3), AC-2 不承担可证明 sound 完整性兜底。** best-effort lint = 对本 spec **改动的 in-scope 文件** (`git.py`/`sync.py` 的直传 callsite + `handoff_multibranch.py`/`handoff_worktrees.py` 助手内部自分类后) 做 intra-procedural 检查 (`_run` 第三解包目标不进 emit 串) + known-bad grep。反例 pin: `rc,out,err=_run(...); msg=f"...{err.strip()}"; soft_error(k,msg)` 必 RED (防后人在 in-scope 文件照抄旧写法)。
  > **已知 lint 局限 (不追求全目录 sound — option B)**: (a) 跨函数 stderr 逃逸靠"助手内部自分类"消除, 不靠跨过程分析; (b) `return _run(...)` 整包逃逸 (`issue_scan.py:461/466`) lint 语法定位不到 —— out-of-scope (issue_scan 已返回枚举不泄 stderr), 记为已知盲区 (R8 Major-3); (c) out-of-scope 已结构化 collector (`multi_remote.py:253-266` 产 `reason` label) 不在 lint 范围。**完整性的真保证 = refactor 被 code-review**, 非 AC-2。
- **AC-3 (无回归)** 🔴 **v2 修正 baseline 假前提 (R5-C-E)**:
  `python3 aria/skills/state-scanner/tests/run_tests.py` → **0 failed, 除 `test_two_consecutive_runs_diff_zero`** ∧ 无既有绿测试转红。
  > ⚠️ **v1 写的「0 failed」是假前提** —— owner 连跑两次实测 (未修改代码): `Ran 1006 tests ... FAILED (failures=1)`, 失败的正是 `test_two_consecutive_runs_diff_zero` (**run-to-run 漂移通道 — 母 Spec CE 复验注 (2026-07-14): R5 时点计 4 条, CE 复验后实数 6 条 [含条件性 custom_checks + 日界潜伏], SOT=母 Spec tasks 12.10**: `remote_refs_age` / `issue_status.repos[].source` / `coordination_fetch.degraded` / `errors[]` 等)。
  > **本 Spec 既不碰这些通道中的任何一条** ⇒ 若坚持「0 failed」, **本 Spec 在自己的 PR 上结构性恒红 ⇒ 按自己的闸门无法 ship** —— 而它恰恰是被指定「**应先落地**」的那一个。
  > ⇒ **该测试由母 Spec 认领消除** (母 Spec tasks 12.10)。本 Spec 显式豁免它。
- **AC-4 (分类器复用)** 🔴 **v2 措辞修正 (R5-M-4; 见 §2c OQ-B1 裁定); v3 补断言载体 (R6-m3) + 命令名 (R6 M-b)**:
  `(rc,stderr)→label` 信号映射搬到 `_common.py.classify_git_error` 作单一 SOT, `coordination_fetch._classify_error` **委托** 它拿 label (v4/R7 M-2) —— **`coordination_fetch` 的既有测试全绿 ∧ 枚举标签集合不变** (`network`/`auth_403`/`non_ff`/`git_missing`/`other`)。
  - 🆕 **断言载体 (R6-m3)**: 新增一条测试**枚举 `classify_git_error` 的全标签集合**并断言 == 上述 5 值 (`{network, auth_403, non_ff, git_missing, other}`) —— "标签集合不变"不能是口头, 要有 fixture 钉死。
  - 🆕 **命令名不硬编码 (R6 M-b)**: 断言 `git log` 失败的 detail 含 "git log" **不含** "git fetch" (委托读法: signal 映射单一 SOT, `coordination_fetch` 只留 label→"git fetch" 措辞层; 无测试直接锚 `_classify_error` 输出 — R8 minor-1, 见 §1 勘误)。
  > ⚠️ **v1 写的「行为逐字节不变」与 §1 的新词表字面互斥**, 且会把 §3b 的**正确诊断改进**也判为违规。**裁定 (b) 保留旧词表后, 矛盾消解。**

---

## Tasks

### 0. 前置裁决 (v2 新增 — R5-M-4: v1 只披露矛盾、无任务承载裁定)

- [x] 0.1 ✅ **OQ-B1 词表裁定**: **(b) 保留 `coordination_fetch` 旧词表** (`network`/`auth_403`/`non_ff`/`git_missing`/`other`), **不发明第三套**。见 §2c
- [x] 0.2 ✅ **OQ-B2 `issue_scan._classify_error` 裁定**: **两套长期共存, 本 Spec 不合并** (`issue_status.fetch_error` 是已发布 schema 字段 + 失败模式不同域 + 它已返回枚举不泄露 stderr)。见 §2d

### 1-4. 实施

- [ ] 1.1 **建类型化通道 (v3 结构级 — R6 C1/M-b/M-d; v4 委托读法 — R7 M-2)**: 在 `collectors/_common.py` 定义 `@dataclass(frozen=True) GitErrorClass(label, rc, cmd)` (**无 stderr 字段**) + `classify_git_error(rc, stderr, cmd) -> GitErrorClass` (信号映射**单一 SOT**, **不搬硬编码 "git fetch" message 文案**)。按 0.1 裁定保留旧词表标签; **`coordination_fetch._classify_error` 改为委托 `classify_git_error(...).label`, 只保留自己 label→"git fetch" 措辞层** (不复制信号映射 — 复制会成第三份 + §3b 双维护), 既有测试全绿 (AC-4)
- [ ] 1.2 🔴 **写 AC-1 红测试 (v2 修正靶点 — R5-M-3)**: 令 `git log` (`git.py:184`) / `git status` (`git.py:356`) / `git rev-list` (`sync.py:150`) **真实失败** (损坏对象库 / 缺失 upstream ref), 断言其 **stderr 原文不落进 `snapshot["errors"]`**。确认当前代码 **RED**。
      ⚠️ **v1 写的「凭据 sentinel 红测试」打错了靶** (R4 qa-engineer 实证): 那三处是**纯本地命令**, argv 里根本没有 remote URL ⇒ 用「凭据 URL 的失败 fetch」做 fixture, **在未修改代码上就会 PASS** ⇒ **违反它自己的自我否证闸**。凭据哨兵归 **1.3 (AC-1b)**, 那是**防回归 pin**, 不是缺陷证据
- [ ] 1.3 **AC-1b 防回归 pin**: userinfo 段含凭据哨兵的 remote URL 令 **fetch** 失败 → snapshot 全文不含哨兵。**哨兵必须运行时拼装** (完整字面量会触发 secret-guard hook, 按形状匹配不区分真假)
- [ ] 2.1 🔴 **收口全部站点 (v2 修正 ≥9 处; v3 补 stderr 烘焙助手真 sanitize 行 — R6-M-a)**:
      **直传 callsite** (直接经 `classify_git_error`): `git.py:184` / `git.py:356` / `sync.py:150` / `sync.py:232-235` / `sync.py:244-247`。
      **stderr 烘焙助手** (🆕 R6-M-a 真 sanitize 位; v5 改**助手内部自分类** — R8 C-1): `handoff_multibranch.py:146` `_list_origin_branches` / `:198` `_list_handoff_files` / `:233` `_read_file_content`; `handoff_worktrees.py:140` `_list_worktrees` —— **在助手内部**分类 (`if rc: if benign(stderr): return [],None; else: return [], classify_git_error(rc,stderr,cmd)`), **返回 GitErrorClass/label + benign-skip 全留助手内, stderr 不跨函数逃逸**; callsite (`:298`/`:334`/`:354`/`:348` + 复合消息 `:332`/`:352`) 消费 label 不碰原文 stderr。
      > ⚠️ **v3/v4 曾写"助手 return (rc,stderr) 到 callsite 再分类" = stderr 跨函数逃逸, 与 best-effort lint 的 intra-procedural 前提冲突 (R8 C-1)**; v5 改助手内部自分类消除逃逸。
      ⚠️ **Phase B 收口本清单全部站点, refactor 经 code-review 确认完整性** (option B: 完整性靠 review, AC-2 是 lint 辅助)。
- [ ] 2.2 `soft_error` docstring 写死 Rule #7 契约
- [ ] 2.3 🆕 **`_common.py` 共享分类器 docstring 留痕** (按 0.2): 「本分类器服务 **git 命令**失败; `issue_scan` 的 CLI 失败有独立分类器 (`issue_scan.py:311`), **有意不合并**, 见 Spec §2d」
- [ ] 3.1 **AC-2 best-effort lint (v5 重框 — option B)**: 对本 spec **改动的 in-scope 文件** (git.py/sync.py 直传 callsite + 两 handoff collector 助手内部自分类后) 做 intra-procedural 检查 (`_run` 第三解包目标不进 emit 串) + known-bad grep; 反例 pin `rc,out,err=_run(...); msg=f"...{err.strip()}"; soft_error(k,msg)` 必 RED。**不追求全目录可证 sound** (三轮实证极难精确规约); 完整性真保证 = refactor 被 code-review。out-of-scope (`multi_remote` reason-label / `issue_scan` 已枚举含 `return _run(...)` 整包) 不在 lint 范围, 记为已知盲区 (R8 Major-1/3)
      - [ ] 3.1b **code-review 完整性确认 (option B 的完整性载体)**: PR review 显式核对"每个子进程 stderr 站点 (§2 清单 + grep 复扫) 都已改经类型化通道", 作为 refactor 完整性的权威闸 (取代 AC-2 可证 sound)
- [ ] 3.2 全量测试无回归 (**AC-3, 豁免 `test_two_consecutive_runs_diff_zero`**) + `coordination_fetch` 既有测试全绿 + 标签集合不变 (AC-4)
- [ ] 3.2b 🆕 **AC-4 断言载体 (R6-m3)**: 新增测试枚举 `classify_git_error` 全标签集合断言 == `{network, auth_403, non_ff, git_missing, other}`; + 断言 `git log` 失败 detail 含 "git log" 不含 "git fetch" (R6 M-b)
- [ ] 3.3 🆕 **扩充 signal 表覆盖率** (§3b, **诊断质量非正确性**): 加 `unable to access` / `failed to connect` / `couldn't connect` / `tls` → `network`; **`permission denied (publickey)` → `auth_403`** (🔴 R6-m1: 不裸配 `permission denied`, 否则误吞本地 FS 权限错)。
      **实测输入** (owner 跑生产分类器): 5 种真实故障 **3 种落 catch-all `other`** (HTTPS 连不上 / TLS 握手失败 / **SSH 公钥被拒**)。
      🔴 **R6-m4 分割证明**: 附一句/fixture 证 signal 分支两两互斥 (auth 先于 network 求值, 无依赖顺序的重叠格) + 补集全覆盖 (`other` fail-CLOSED)。
      ⚠️ **母 Spec 的正确性不依赖此项** (`has_unreachable_remote` 是 fail-CLOSED, `other` 一样置位) —— 但**诊断信息的价值依赖它**
- [ ] 4.1 文档: `references/state-snapshot-schema.md` 的 `errors[].detail` 取值域
- [ ] 4.2 版本 bump + SOT 同步 + CHANGELOG (标注: 诊断信息变少是有意取舍)

---

## 关联

- **母 Spec**: `state-scanner-stale-refs-false-parity` (F3′ 放大本暴露面 N×M 倍 ⇒ **本 Spec 应先落地**)
- **Rule #7**: `standards/conventions/secret-hygiene.md` (不可协商)
- **正向先例**: `coordination_fetch._classify_error` (本 Spec 把它提炼为共享工具)
- **memory**: `feedback_secrets_never_in_conversation` / `feedback_nomad_inspect_secret_leak` / `reference_postooluse_cannot_redact_tool_output` (PostToolUse **无法** redact tool_response ⇒ 只能从**源头**不写入)

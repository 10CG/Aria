# phase-c-integrator 多远程推送强制 + git-remote-helper

> **Level**: Full (Level 3 Spec)
> **Status**: Approved (4-agent team, 3 rounds converged, 2026-04-12)
> **Created**: 2026-04-12
> **Parent Story**: [US-012](../../docs/requirements/user-stories/US-012.md)
> **Source**: 2026-04-12 v1.14.0 发版事故 — Forgejo Issue 待创建
> **Target Version**: aria-plugin v1.15.0
> **Depends**: 无硬依赖 (本 Spec 的 T1 helper 是 canonical source, 被 Spec A 消费)
> **Release Coupling**: 合并顺序 = **T1 helper 先** → Spec A (Layer 1 消费 helper) → 本 Spec 的 T2/T3 (Layer 2 integrator)
> **Schema Source of Truth**: 本 Spec 的 `git-remote-helper` SKILL.md 是 canonical schema 定义者, Spec A 引用

## Why

Phase 1.12 的 Layer 1 扩展只能**检测**多远程漂移, 无法**预防**遗漏推送。现状:

1. `phase-c-integrator` Phase C.2 合并后不主动推送所有配置的远程
2. `git push <remote>` 已同步时输出 `"Everything up-to-date"` — 在多仓库并行操作中语义歧义
3. 推送"成功"的判断依赖 exit code, 但 exit code 只证明**单个**远程的本地状态, 不证明**全部**远程的 HEAD 匹配
4. 子模块与主仓库的跨 remote 一致性没有守卫: 若主仓库推 github 但子模块未推 github, 主仓库指针会指向 github 上不存在的 commit

2026-04-12 事故根因正是此缺口。即使 Layer 1 检测到漂移, 需要人工重新推送, Layer 2 的主动预防才能彻底闭合。

共享 helper (Layer 3) 是避免 Layer 1 / Layer 2 / 未来其他 skills 各自重写 git 多远程逻辑的必要抽象。

## What

### 1. 新增 Internal Skill: `git-remote-helper` (Layer 3)

**路径**: `aria/skills/git-remote-helper/`

**Frontmatter**:
```yaml
name: git-remote-helper
description: |
  Git 多远程 parity 检测与 push 验证的共享基础设施。
  内部工具, 不直接被用户触发, 仅供其他 skills 引用。
  提供标准化 Bash/Python 执行脚本段 + 输出 JSON schema 契约。
user-invocable: false
disable-model-invocation: true
allowed-tools: Bash, Read
```

**交付形式说明**: helper 不是"可调用函数",而是 **SKILL.md 中的指令块 + JSON schema 契约**。消费方 (state-scanner / phase-c-integrator 的 SKILL.md) 通过引用 helper SKILL.md, 让 LLM 执行标准化的 Bash/Python 脚本段并产出约定的 JSON。这与 `config-loader` / `arch-common` 的工作模式一致。

**目录结构**:
```
aria/skills/git-remote-helper/
├── SKILL.md
├── scripts/
│   ├── check_parity.sh       # 纯读取, Bash 实现
│   ├── push_all_remotes.sh   # 写操作, Bash 实现
│   └── verify_post_push.py   # 指数退避重试, Python 实现 (跨平台)
└── references/
    ├── api.md                 # 3 个指令块的完整契约
    ├── schema.md              # JSON schema 定义 (canonical)
    └── platform-notes.md      # macOS/Linux/shallow/detached 处理
```

### 1.1 `check_parity` 指令块 (纯读)

**语义**: 对单个仓库检测所有远程的 parity 状态, 不做网络写操作。

**参数**:
- `repo_path`: git 仓库路径
- `branch`: 目标分支 (默认 `master`, detached HEAD 时为 `HEAD`)
- `verify_mode`: `local_refs` (快) / `ls_remote` (准, 带网络)
- `timeout_seconds`: ls_remote 单 remote 超时 (默认 5)

**输出 JSON** (canonical schema):

```json
{
  "repo_path": "/home/dev/Aria/aria",
  "branch": "master",
  "local_head": "19f2861",
  "detached_head": false,
  "shallow": false,
  "remotes": [
    {
      "name": "origin",
      "remote_head": "19f2861",
      "parity": "equal",
      "behind_count": 0,
      "ahead_count": 0,
      "reachable": true,
      "reason": null,
      "method": "local_refs"
    },
    {
      "name": "github",
      "remote_head": "f55e130",
      "parity": "behind",
      "behind_count": 2,
      "ahead_count": 0,
      "reachable": true,
      "reason": null,
      "method": "local_refs"
    }
  ],
  "overall_parity": false,
  "has_unreachable_remote": false,
  "has_pending_push": false
}
```

**`parity` 枚举**: `equal | ahead | behind | diverged | unknown`
**`reason` 枚举**: `null | auth_failed | not_found | network_timeout | no_local_tracking_ref | shallow_clone | detached_head`
**`overall_parity` 定义**: 排除 `ahead` (待推送) 和 `unknown` (网络故障), 仅 `behind` 或 `diverged` 导致 false

**边界处理** (必须):
- shallow clone → `parity: unknown, reason: shallow_clone, behind_count: null`
- detached HEAD → `detached_head: true`, 用 HEAD SHA 比较所有 remote 的 HEAD SHA
- `refs/remotes/<remote>/<branch>` 不存在 → `parity: unknown, reason: no_local_tracking_ref, reachable: unknown`
- `ls_remote` 超时 → `reachable: false, reason: network_timeout`
- `ls_remote` 认证失败 (exit 128) → `reachable: false, reason: auth_failed`

**跨平台**: 
- 检测 `timeout` / `gtimeout` 可用性, 缺失则用 Python subprocess 实现超时 (见 §1.3)
- JSON 输出统一用 `jq -n --arg ...` 或 Python `json.dumps` 构造, 避免 Bash 手工拼接破包

### 1.2 `push_all_remotes` 指令块 (写)

**语义**: 对单个仓库推送所有 (或白名单内的) remote, 记录 pre/post 状态。

**参数**: `repo_path`, `branch`, `remotes` (可选白名单, 空则推送所有)

**输出 JSON**:
```json
{
  "repo_path": "/home/dev/Aria/aria",
  "branch": "master",
  "pre_local_head": "19f2861",
  "results": [
    {
      "remote": "origin",
      "exit_code": 0,
      "success": true,
      "pre_remote_head": "19f2861",
      "post_remote_head": "19f2861",
      "message": "Everything up-to-date (local was already in sync with remote)"
    },
    {
      "remote": "github",
      "exit_code": 0,
      "success": true,
      "pre_remote_head": "f55e130",
      "post_remote_head": "19f2861",
      "message": "f55e130..19f2861  master -> master"
    }
  ],
  "all_success": true
}
```

**`success` 判定** (严格, 非 exit code):
- `success = (exit_code == 0) AND (post_remote_head_via_local_refs == pre_local_head)`
- `post_remote_head` 用 `git rev-parse refs/remotes/<remote>/<branch>` 读取 (本地 push 成功后自动更新, 无网络延迟)
- **"Everything up-to-date" 语义处理**: 当 `pre_remote_head == pre_local_head` 时 (本地已同步), push 是 no-op, success=true 合法; 但这必须由 `post_remote_head == pre_local_head` 的 SHA 对比证明, 不能依赖 message 文本

**不做**:
- 不 retry (失败由调用方决策)
- 不修改本地 ref
- 不处理 force push (用户需显式在调用前配置)

### 1.3 `verify_parity_post_push` 指令块 (Python 实现)

**用途**: 权威验证远程实际接收到推送, 应对 Forgejo/GitHub 10-30s 复制延迟。

**语言选择**: **Python** (Bash 实现指数退避 + JSON 构造 + 跨平台超时脆弱, Python 原生 `subprocess.run(timeout=5)` + `time.sleep(backoff)` + `json.dumps()` 清晰可靠)

**参数**: `repo_path`, `branch`, `expected_sha` (调用方在 push 前快照的 local HEAD), `max_retries` (默认 3), `initial_backoff_seconds` (默认 2)

**重试策略** (precisely):
```
attempt 1 (immediate):
  cmd: git ls-remote <remote> refs/heads/<branch> (timeout 5s)
  match? → return success
attempt 2 (after 2s sleep):
  same cmd → match? → return success
attempt 3 (after 4s sleep):
  same cmd → match? → return success
attempt 4 (final, after 8s sleep):
  same cmd → match or fail (return regardless)
```

**per-remote 最大耗时** (数学上界):
- 4 次 `ls-remote` × 5s timeout = 20s
- sleep 2+4+8 = 14s
- **合计上界 34s per remote**
- N remotes 串行 → 最坏 34N 秒

**总 timeout 约束**: **per-remote ≤ 34s** (取消 "总 30s" 约束, 改为 per-remote 约束)
- `config.post_push_verify.max_per_remote_seconds = 34` (默认)
- 典型 case (远程已同步) attempts=1, 耗时 < 5s

**输出 JSON**:
```json
{
  "repo_path": "/home/dev/Aria/aria",
  "branch": "master",
  "expected_sha": "19f2861",
  "max_retries": 3,
  "retry_schedule_seconds": [0, 2, 4, 8],
  "results": [
    {"remote": "origin", "actual_sha": "19f2861", "match": true, "attempts": 1, "total_seconds": 0.3},
    {"remote": "github", "actual_sha": "19f2861", "match": true, "attempts": 2, "total_seconds": 2.4}
  ],
  "all_match": true
}
```

### 2. phase-c-integrator 强化 (Layer 2, Phase C.2)

#### 2.1 与 branch-manager 的边界

| Skill | 职责 | Remote 范围 |
|-------|------|-----------|
| `branch-manager` (C.2 PR 发起) | 推送 feature 分支 + 创建 PR | **仅 origin** (PR 只需在 origin) |
| `phase-c-integrator` C.2.5 (PR 合并后) | 推送合并后的 master/default branch + SHA 验证 | **所有配置 remote** |

**branch-manager 不变**, 本 Spec 仅影响 PR 合并后的 master 推送。

#### 2.2 新增子步骤 C.2.5: Multi-Remote Push Enforcement

**执行流程**:

```
1. 获取当前默认分支 (master) local HEAD, 记为 EXPECTED_SHA
2. 枚举子模块 (git submodule status --recursive) 得到 SUBMODULE_LIST
3. 确定目标 remotes: ENFORCED_REMOTES (从顶层 + skill 级配置合并)
4. 对每个 REMOTE in ENFORCED_REMOTES:
   a. Per-Remote Gating (子模块先, 主仓库后):
      for SUBMODULE in SUBMODULE_LIST:
        - 调用 helper.push_all_remotes(SUBMODULE.path, SUBMODULE.branch, [REMOTE])
        - 任一失败 → 检查是否 read_only_remote (见优先级表) → 阻断或 warn
   b. 主仓库 push:
      - 调用 helper.push_all_remotes(main_repo, branch, [REMOTE])
      - 失败 → 同上处理
   c. 推送完成, 验证:
      - 调用 helper.verify_parity_post_push(main_repo, branch, EXPECTED_SHA, [REMOTE])
      - match=false → 同上处理
5. 所有 remotes 处理完毕, 全部通过 → 进入 Phase D
6. 有失败 → 输出详细错误 + 修复命令, 阻断
```

**Per-Remote Matrix Gating** (笛卡尔积守卫):

推送规则: 主仓库推送 remote X **当且仅当**所有子模块都已成功推送到 remote X。这避免主仓库 github 指针指向 github 不存在的子模块 commit。

**不是** "任一子模块失败阻断所有主仓库推送", 而是 "任一子模块推送 remote X 失败 → 阻断主仓库推送 remote X" (其他 remote 不受影响)。

例:
```
origin: sub1 ✅ sub2 ✅ main ✅ (已推)
github: sub1 ✅ sub2 ❌ (network timeout) → 跳过 main github, 但 origin 已完成
```

#### 2.3 失败优先级 (明确消歧)

当 remote X push 失败时, 根据配置决定行为:

| 条件 | 行为 |
|------|------|
| `read_only_remotes` 包含 X | **warning 降级**, 继续 (read_only 优先级最高) |
| `fail_on_partial_push: false` AND 非 read_only | warning, 继续 |
| `fail_on_partial_push: true` AND 非 read_only (默认) | **阻断**, 输出修复命令 |

#### 2.4 Race condition 处理 (AC 一致性修复)

**verify_parity_post_push 的 `match=false` 语义**:
- 所有 retry attempt 都失败 → `match: false`
- 此时**在调用方 (phase-c-integrator) 层面**决定阻断与否: 默认阻断 (`fail_on_partial_push=true`)
- 若 `max_retries` 全部耗尽仍不匹配, 记录为 "可能的 race condition (post-push SHA drifted)", 日志级别 warning, 行为仍阻断

**helper 层不做阻断判断**, helper 只返回事实 (`match: true/false`)。阻断决策统一在 integrator。

#### 2.5 降级策略 (helper 不可用)

**检测**: `test -f aria/skills/git-remote-helper/SKILL.md` 文件存在性

**降级行为**:
1. 输出警告: "git-remote-helper 不可用, 使用内联降级模式"
2. 内联实现必须**产出与 helper canonical 完全一致的 JSON schema**
3. 内联实现不做指数退避 (简化): 每个 remote 一次 ls-remote, 失败直接报错
4. schema 一致性必须通过 AC 验证

### 3. 配置集成 (`.aria/config.json`)

遵循 Spec A 一致的**共享命名空间 + skill 级覆盖**:

```json
{
  "multi_remote": {
    "enforced_remotes": [],
    "read_only_remotes": []
  },
  "phase_c_integrator": {
    "multi_remote_push": {
      "enabled": true,
      "enforced_remotes": null,
      "fail_on_partial_push": true,
      "post_push_verify": {
        "enabled": true,
        "max_retries": 3,
        "initial_backoff_seconds": 2,
        "max_per_remote_seconds": 34
      }
    }
  }
}
```

**配置继承**:
- `phase_c_integrator.multi_remote_push.enforced_remotes: null` → 继承顶层 `multi_remote.enforced_remotes`
- 非 null → skill 级覆盖

### 4. AB Benchmark (Rule #6)

- **helper 独立 benchmark** (因有 SKILL.md): 新 ab-suite `git-remote-helper.json`
  - eval-1: `parity-check-equal` (单 remote 已同步)
  - eval-2: `parity-check-behind` (双 remote, 一个 behind)
  - eval-3: `push-with-post-push-verify` (主动推送 + 验证流程描述)
  - eval-4: `post-push-retry-on-delay` (mock 复制延迟, 描述重试策略)

- **phase-c-integrator benchmark**: 现有 ab-suite 新增
  - eval-N: `multi-remote-merge-push` (双 remote 项目合并后自动推送 + SHA 验证)

**AB eval 编号映射** (与 US-012 + Spec A 对齐):

| eval ID | 归属 | 名称 | Spec |
|---------|------|------|------|
| eval-10 | state-scanner | multi-remote-parity-drift | Spec A |
| eval-11 | state-scanner | submodule-push-github-sync-miss | Spec A |
| eval-hlp-1~4 | git-remote-helper | parity-check-*, push-*, verify-* | 本 Spec T1 |
| eval-int-1 | phase-c-integrator | multi-remote-merge-push | 本 Spec T2 |

### 5. 不做什么

- 不自动处理 diverged remote (需人工决策, 仅报告)
- 不修改 git 配置 (不 set remote URL, 不改 refspec)
- 不支持 non-fast-forward push (用户如需 force push 必须显式配置)
- 不改变 `branch-manager` 的 push 范围 (仍仅 origin)
- helper 的 `push_all_remotes` 不 retry (retry 是 verify 职责)
- 不在 `push_all_remotes` 中用 `git submodule foreach` (shell 命令层 vs skill 层调用 不对等)

## Design Decisions

| ID | 决策 | 理由 |
|----|------|------|
| D1 | helper 为 internal skill + 指令块 + JSON schema 契约 | 与 Aria skill 实际机制对齐 (非"函数调用"), 与 config-loader 先例一致 |
| D2 | Schema canonical source = helper SKILL.md | 单一真相源, Spec A 引用而非复述 |
| D3 | `verify_parity_post_push` 用 Python 实现 | Bash 的超时/重试/JSON 脆弱, Python 原生支持 + 跨平台 |
| D4 | Per-remote matrix gating (非 all-or-nothing) | 主仓库推 X 仅需子模块在 X 上存在, 正交避免过度阻断 |
| D5 | read_only_remotes 优先级高于 fail_on_partial_push | read_only 明确降级意图, 一致语义 |
| D6 | `branch-manager` 仍仅推 origin | PR 只需 origin, 多远程语义在合并后生效 |
| D7 | helper 的 `push_all_remotes` 不 retry | 单一职责: push 是事实记录, retry 是 verify 职责 |
| D8 | `verify_parity_post_push` 的 match=false 由 integrator 决定阻断 | helper 只返回事实, 决策归消费方 |
| D9 | 共享配置顶层 `multi_remote.*` + skill 覆盖 | 用户避免多处重复, skill 可局部调整 |
| D10 | `max_per_remote_seconds = 34s` (取消总 30s) | 数学上界: 4 × 5s ls_remote + 14s backoff = 34s |
| D11 | helper `check_parity` vs `push_all_remotes` 权限分离 | 纯读 (任何消费方) vs 写 (仅 phase-c-integrator / branch-manager 等) |
| D12 | JSON 输出用 `jq` 或 Python | 避免 Bash 手工拼接破包, 依赖声明在 SKILL.md |
| D13 | 不存在 remote 在推送侧 hard-fail (`Unknown remote "typo"`) | 推送是写操作, 配置错误必须阻断; 与 Spec A 检测侧 soft-fail 形成语义对称 (检测容忍, 执行严格), 非不一致 |
| D14 | 子模块 detached HEAD: 警告不阻断 | 沿用 helper canonical (`detached_head: true` + HEAD SHA), 主仓库 C.2.5 流程继续执行 |

## Scope

### 新增文件

| 文件 | 类型 |
|------|------|
| `aria/skills/git-remote-helper/SKILL.md` | 新 internal skill |
| `aria/skills/git-remote-helper/scripts/check_parity.sh` | Bash 实现 |
| `aria/skills/git-remote-helper/scripts/push_all_remotes.sh` | Bash 实现 |
| `aria/skills/git-remote-helper/scripts/verify_post_push.py` | Python 实现 (指数退避) |
| `aria/skills/git-remote-helper/references/api.md` | 3 个指令块完整契约 |
| `aria/skills/git-remote-helper/references/schema.md` | JSON schema canonical 定义 |
| `aria/skills/git-remote-helper/references/platform-notes.md` | 跨平台 + 边界处理 |
| `aria-plugin-benchmarks/ab-suite/git-remote-helper.json` | helper AB suite |

### 修改文件

| 文件 | 变更类型 |
|------|---------|
| `aria/skills/phase-c-integrator/SKILL.md` | C.2 新增 C.2.5 子步骤 |
| `aria/skills/config-loader/DEFAULTS.json` | 新增顶层 + skill 级配置 |
| `aria-plugin-benchmarks/ab-suite/phase-c-integrator.json` | 新增 eval-int-1 |
| `aria/README.md` | 更新 internal skills 列表, user-facing Skills 数不变 (保持 30), internal 数 5→6 |
| `aria/CHANGELOG.md` | v1.15.0 条目 |

### 不影响 (显式声明)

- `state-scanner/SKILL.md` Phase 1.12 — 由 Spec A 负责
- `branch-manager` — PR 阶段推送范围不变 (仅 origin)
- `forgejo-sync` — 可未来独立 Spec 引用 helper, 本 Spec 不修改
- `standards/` 子模块 — 本变更属工具层, 方法论不变
- CLAUDE.md 发版清单行号 — 只更新内容不引用行号

## Acceptance Criteria

### helper (Layer 3)

- [ ] `aria/skills/git-remote-helper/SKILL.md` 存在, `user-invocable: false, disable-model-invocation: true`
- [ ] `check_parity` 指令块输出 canonical JSON, 含 `parity` 枚举完整 5 种状态
- [ ] `check_parity` 在 shallow clone: `parity: unknown, reason: shallow_clone, behind_count: null`
- [ ] `check_parity` 在 detached HEAD: `detached_head: true`, 比较 HEAD SHA
- [ ] `check_parity` 在未 fetch 的 remote: `parity: unknown, reason: no_local_tracking_ref, reachable: unknown`
- [ ] `check_parity` 在 auth 失败: `reachable: false, reason: auth_failed`
- [ ] `check_parity` 超时 (>5s): `reachable: false, reason: network_timeout`
- [ ] `push_all_remotes` 的 `success` 判定使用 `post_remote_head == pre_local_head`, **不依赖** "Everything up-to-date" 文本
- [ ] `push_all_remotes` 当 `pre_remote_head == pre_local_head` (本地已同步): post 验证后 success=true
- [ ] `push_all_remotes` 当 post_remote_head 读取失败: `success: false, message: "post-push verification failed"`
- [ ] `verify_parity_post_push` 用 Python 实现 (`scripts/verify_post_push.py`)
- [ ] `verify_parity_post_push` 重试策略 = 立即 + 2s + 4s + 8s (4 次 attempt)
- [ ] `verify_parity_post_push` 单 remote 上界 = 34s (`max_per_remote_seconds`)
- [ ] JSON 输出用 `jq` 或 Python 构造 (非 Bash 手工拼接)
- [ ] `timeout` 命令缺失时 (macOS default) 降级 Python subprocess timeout
- [ ] helper AB eval (eval-hlp-1~4) 全部 with_skill delta 为正

### phase-c-integrator (Layer 2)

- [ ] C.2 新增 C.2.5 Multi-Remote Push Enforcement 子步骤
- [ ] Per-Remote Matrix Gating: 主仓库推 X **当且仅当** 所有子模块已推 X
- [ ] 单个子模块推 X 失败: 阻断主仓库推 X, 其他 remote (Y) 不受影响
- [ ] 推送后调用 `verify_parity_post_push(expected_sha=local HEAD)`
- [ ] `verify match=false`: 默认阻断 (`fail_on_partial_push=true`)
- [ ] `read_only_remotes` 包含的 remote push 失败: warning 降级 (优先级高于 fail_on_partial_push)
- [ ] `fail_on_partial_push: false`: 任一非 read_only 失败也 warning
- [ ] `post_push_verify.enabled: false`: 跳过 SHA 验证 (仅 push)
- [ ] `enforced_remotes: null`: 继承顶层 `multi_remote.enforced_remotes`
- [ ] `enforced_remotes: []`: 推送所有 git remote 配置的远程
- [ ] `enforced_remotes: ["origin", "typo"]` (含不存在): 阻断并提示 `Unknown remote "typo"`
- [ ] 配置 `post_push_verify.enabled: true` 但 helper 不可用: 降级内联实现 (不做重试), schema 一致

### branch-manager 边界 (显式不变)

- [ ] `branch-manager` 的 push 仍仅推 origin
- [ ] PR 合并前的 feature branch push 不触发多远程

### 边界条件

- [ ] 单 remote 项目: 推送 + 验证 1 个 remote, 行为正确
- [ ] 双 remote 项目, github 网络断连: matrix gating 跳过 github, origin 继续
- [ ] 多子模块场景, 子模块 2 的 github push 失败: 子模块 1 的 github push 已完成(此时状态部分完成), 主仓库 github push 被阻断, 输出"部分完成, 手动修复"提示
- [ ] 子模块 detached HEAD: helper 返回 `detached_head: true`, C.2.5 输出警告但不阻断主仓库推送
- [ ] Race condition (post-push 被他人覆盖): verify 4 次 attempt 全部 match=false, 默认阻断, 记录 "possible race condition"
- [ ] `parity: diverged` remote: helper 正确报告 behind_count + ahead_count, integrator 阻断推送 (避免 force push)
- [ ] Python `verify_post_push.py` 在 macOS 可执行 (`#!/usr/bin/env python3`)

### 向后兼容

- [ ] `phase-c-integrator` 现有 C.1 / C.2 其他步骤行为不变
- [ ] `.aria/config.json` 无 `multi_remote` 配置时: 继承默认值, 不报错

### AB Benchmark (Rule #6)

- [ ] helper ab-suite (`git-remote-helper.json`) 新增 4 个 eval, 全部 with_skill delta > 0
- [ ] phase-c-integrator ab-suite 新增 eval-int-1, delta > 0

### 文档同步

- [ ] `docs/architecture/system-architecture.md` 更新 Phase C.2 职责描述 (推送完整性)
- [ ] `CLAUDE.md` 发版检查清单更新 (不引用行号, 仅更新 "多远程推送" 小节内容, 标注自动化于 v1.15.0+ 但保留手动 fallback 作为灾备)
- [ ] `aria/README.md` 更新 (internal skills 新增 git-remote-helper, 内部 Skill 数 5→6)
- [ ] `aria/CHANGELOG.md` 新增 v1.15.0 条目

## Tasks

完整任务清单在 [tasks.md](./tasks.md), 大纲:

- **T1 (前置)**: git-remote-helper internal skill 实现 + AB benchmark
- **T2 (依赖 T1)**: phase-c-integrator C.2.5 子步骤 + matrix gating + 配置集成 + AB benchmark
- **T3 (文档)**: 架构文档 + CLAUDE.md + README + CHANGELOG + 端到端测试

## Estimation

- **工作量**: 24 小时 (helper 12h + integrator 8h + 联调文档 4h)
- **风险**: 中-高 (跨 skill 协同 + 跨平台 + 网络依赖 + 向后兼容)
- **关键依赖**: T1 (helper) 必须先于 Spec A 和 T2 交付 (canonical schema)

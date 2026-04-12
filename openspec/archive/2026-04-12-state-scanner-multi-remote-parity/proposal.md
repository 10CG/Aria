# state-scanner Phase 1.12 多远程 Parity 检测

> **Level**: Minimal (Level 2 Spec)
> **Status**: Complete (merged aria-plugin#13 + Aria#12, 2026-04-12)
> **Created**: 2026-04-12
> **Parent Story**: [US-012](../../docs/requirements/user-stories/US-012.md)
> **Source**: 2026-04-12 v1.14.0 发版事故 (aria 子模块 GitHub 同步遗漏) — Forgejo Issue 待创建
> **Target Version**: aria-plugin v1.15.0
> **Soft Depends**: [phase-c-integrator-push-enforcement](../phase-c-integrator-push-enforcement/proposal.md) — `git-remote-helper` (canonical schema source)
> **Release Coupling**: 合并顺序 = `git-remote-helper` (Spec B 的 T1) → **本 Spec (Layer 1)** → Spec B 的 T2/T3 (Layer 2 integrator)。即 helper 必须先交付, 本 Spec 是第一个消费方。

## Why

state-scanner Phase 1.12 (本地/远程同步检测) 当前只检查**单个**远程 (origin), 无法覆盖多远程场景:

- 项目配置 `origin` (Forgejo) + `github` (镜像) 时, 只有 origin 被检测
- 当 origin 同步但 GitHub 落后时, 扫描输出"全部同步", 实际存在漂移
- 2026-04-12 事件验证: aria 子模块 2 个 commit 滞留在 origin, 未推 GitHub, 但 state-scanner 无法检测

**影响**: state-scanner 是十步循环统一入口, 此漏洞使每次扫描都可能对"已同步但未推 GitHub"的项目给出误导性结论。Claude Code 插件市场从 GitHub 拉取, 用户因此获取不到最新版本。

## What

### Phase 1.12 原地扩展 (不消耗 D8 配额)

**编号约束**: 本 Spec 不新增阶段, 在 Phase 1.12 内部扩展 schema 和检测逻辑。当前 14/15 阶段配额保持不变。参考 standards/core/ten-step-cycle/ 的 D8 约束 (state-scanner 子阶段上限 15)。

### Schema Source of Truth

**canonical schema 定义在 `git-remote-helper` SKILL.md** (Spec B 的 Layer 3)。本 Spec 引用而非复述。helper `check_parity()` 指令产出的 JSON 即本 Phase 1.12 使用的数据结构。

本 Spec 的内联 fallback 实现 **必须** 产出与 helper canonical 完全一致的 JSON (通过同一 schema validator), 避免消费方写两套解析。

### 新增数据字段

在现有 `sync_status` 基础上扩展:

```yaml
sync_status:
  # 现有字段保留
  remote_refs_age: "2h"
  has_remote: true
  current_branch: { ... }

  # 现有 submodules[] 保留, 语义明确:
  # remote_commit 字段 = multi_remote.submodules[path=X].remotes[name=origin].remote_head
  # 保留是为了向后兼容现有 consumers (见下方 Consumer Inventory)
  submodules:
    - path: "aria"
      tree_commit: "19f2861"
      head_commit: "19f2861"
      remote_commit: "19f2861"       # 约定: 此字段始终映射 origin 的 remote_head
      drift: { ... }

  # 新增: 多远程 parity (canonical schema 来自 git-remote-helper)
  multi_remote:
    enabled: true
    main_repo:
      local_head: "5b7a5f7"
      branch: "master"
      remotes:
        - name: "origin"
          remote_head: "5b7a5f7"
          parity: "equal"             # enum: equal | ahead | behind | diverged | unknown
          behind_count: 0
          ahead_count: 0
          reachable: true
          reason: null                # enum: null | auth_failed | not_found | network_timeout | no_local_tracking_ref | shallow_clone | detached_head
          method: "local_refs"        # local_refs | ls_remote
        - name: "github"
          remote_head: "e476a2b"
          parity: "behind"
          behind_count: 1
          ahead_count: 0
          reachable: true
          reason: null
          method: "local_refs"
    submodules:
      - path: "aria"
        local_head: "19f2861"
        branch: "master"
        remotes:
          - name: "origin"
            remote_head: "19f2861"
            parity: "equal"
            behind_count: 0
            ahead_count: 0
            reachable: true
            reason: null
            method: "local_refs"
          - name: "github"
            remote_head: "f55e130"
            parity: "behind"
            behind_count: 2
            ahead_count: 0
            reachable: true
            reason: null
            method: "local_refs"
    overall_parity: false             # 定义见下
    has_unreachable_remote: false     # 任一 reachable=false 时 true
    has_pending_push: false           # 任一 parity=ahead 时 true (正常状态, 不 alarm)
```

**`overall_parity` 精确定义**:
- `true`: 所有 remotes 的 `parity` 均为 `equal`
- `false`: 任一 remote 的 `parity` ∈ {`behind`, `diverged`}
- `parity: ahead` 不计入 `overall_parity` (这是正常的"待推送"状态), 单独由 `has_pending_push` 承载
- `parity: unknown` 不计入 `overall_parity` (网络故障不等于推送遗漏), 单独由 `has_unreachable_remote` 承载

### 检测逻辑

1. **枚举远程**: 对主仓库 + 每个子模块, 通过 helper `check_parity()` 指令枚举 (helper 不可用时降级为 `git -C <path> remote | sort -u`)
2. **获取 remote HEAD**: 调用 helper 的分层策略 (见 Spec B §1.1)
3. **fail-soft**: 任一 remote 不可达 → `parity: unknown` + `reachable: false` + `reason: <枚举>`, 不阻断扫描

### verify_mode 触发协议

| 触发源 | `verify_mode` |
|--------|--------------|
| 用户普通扫描 (`/state-scanner`) | 配置默认值 (默认 `local_refs`) |
| 发版前流程 (由 Phase C 流程触发 state-scanner) | 显式参数 `--verify-mode=ls_remote` 覆盖配置 |
| 配置 `state_scanner.multi_remote.verify_mode` | 控制默认值 |

**实现**: state-scanner 支持 CLI `--verify-mode=local_refs|ls_remote` 参数, 优先级 = CLI > 配置 > 硬编码默认。

### 配置集成 (`.aria/config.json`)

遵循**共享命名空间 + skill 级覆盖**原则:

```json
{
  "multi_remote": {
    "enforced_remotes": [],          // 顶层: 检测 + 执行共享的 remote 白名单
    "read_only_remotes": []          // 顶层: 共享的只读 remote 列表
  },
  "state_scanner": {
    "multi_remote": {
      "enabled": true,               // skill 级开关
      "verify_mode": "local_refs",   // skill 级默认 mode
      "timeout_seconds": 5,          // skill 级 timeout
      "enforced_remotes": null       // null = 继承顶层; 非 null = 覆盖
    }
  }
}
```

| 字段 | 默认 | 说明 |
|------|------|------|
| 顶层 `multi_remote.enforced_remotes` | `[]` | 空 = 自动发现所有 remote; 非空 = 全局白名单 |
| 顶层 `multi_remote.read_only_remotes` | `[]` | 只读镜像白名单, push 失败降级为 warning (Spec B 使用) |
| `state_scanner.multi_remote.enabled` | `true` | 主开关 (关闭则完全跳过本功能) |
| `state_scanner.multi_remote.verify_mode` | `local_refs` | `local_refs` (快) / `ls_remote` (准, 带网络) |
| `state_scanner.multi_remote.timeout_seconds` | `5` | 单 remote ls-remote 超时 |
| `state_scanner.multi_remote.enforced_remotes` | `null` | null = 继承顶层, 非 null = skill 级覆盖 |

**enforced_remotes 边界行为**:
- `[]`: 自动发现所有 remote (等同于 `git remote`)
- `["origin", "github"]`: 白名单, 仅检查列出的 remote
- 白名单包含不存在的 remote 名称 (如 `["origin", "typo"]`): `typo` 输出 `reachable: false, reason: not_found`, 不阻断扫描

### Local refs staleness 处理

`verify_mode: local_refs` 依赖 `refs/remotes/<remote>/<branch>` 本地缓存:

1. ref 不存在 (新配置 remote 未 fetch) → `parity: unknown, reason: no_local_tracking_ref, reachable: unknown`
2. `FETCH_HEAD` 陈旧 (> `warn_after_hours`, 默认 24h) → 输出中标注 `local_refs_stale: true`, 建议用户运行 `git fetch`
3. shallow clone → 复用现有 Phase 1.12 守卫, `parity: unknown, reason: shallow_clone, behind_count: null`

### 推荐规则 (`RECOMMENDATION_RULES.md`)

新增规则 `multi_remote_drift`, 插入位置 = `submodule_drift` (1.3) 之后、`branch_behind_upstream` (1.4) 之前:

```yaml
id: multi_remote_drift
priority: 1.35
description: 检测到多远程 HEAD 不一致, 存在推送遗漏风险

conditions:
  any:
    - multi_remote.overall_parity: false   # 排除 ahead 和 unknown (见上方定义)

recommendation:
  workflow: null
  steps: []
  reason: "检测到 HEAD 未同步到部分远程, 建议: git -C <path> push <remote> <branch>"
  non_blocking: true
```

### `parity: diverged` 处理

- 输出 `parity: diverged, behind_count: N, ahead_count: M`
- 触发 `multi_remote_drift` 规则 (overall_parity=false)
- 建议文本: "远程与本地分歧 (behind N, ahead M), 需人工决策: git pull/rebase 或 git push --force-with-lease"
- 不提供自动修复步骤 (force push 涉及人工判断)

### 输出格式

`output-formats.md` 新增:

```
🌐 多远程一致性
───────────────────────────────────────────────────────────────
  ✅ 主仓库: 所有远程一致 (origin, github)
  ⚠️ aria 子模块: github 落后 2 commits
     修复: git -C aria push github master
     当前: origin=19f2861 | github=f55e130 (behind 2)
  ❓ upstream 子模块: github 不可达 (auth_failed)
     提示: 检查 CF_ACCESS_CLIENT_ID 环境变量
```

**此为运行时输出模板 (面向用户终端), emoji 是参考展示非硬性约束**, 消费方 (CI 日志) 可读结构化 JSON 字段判定状态。

### Consumer Inventory (向后兼容验证清单)

现有读取 `sync_status.submodules[]` 的 consumer:

| Consumer | 消费字段 | 向后兼容要求 |
|----------|---------|------------|
| `RECOMMENDATION_RULES.md` → `submodule_drift` 规则 | `submodules[].drift.tree_vs_remote` | 字段保留不变 |
| `aria-dashboard` (若消费) | `submodules[].remote_commit` | 保留, 值 = origin 的 remote_head |
| 其他 Phase / Skills | (经 Grep 验证无其他) | N/A |

AC 必须验证: 以上 consumer 的行为在本 Spec 实施后与实施前完全一致。

### 依赖 Layer 3 helper

- **可用时**: state-scanner 调用 helper `check_parity(repo_path, [branch])` 指令 (见 Spec B §1.1)
- **不可用时** (文件存在性检查失败): 降级为内联 Bash 实现, 必须产出与 helper canonical 完全一致的 JSON schema
- **检测方式**: `test -f aria/skills/git-remote-helper/SKILL.md` (简单文件存在检查)

### 不做什么

- 不主动 `git fetch` (维持 Phase 1.12 现有原则; `ls_remote` 模式是唯一网络访问例外, 5s 超时)
- 不自动推送 (仅检测, 执行是 Layer 2 职责)
- 不修改 `submodules[]` 现有字段 (向后兼容)
- 不并行执行 `ls_remote` (顺序执行, 避免资源竞争)
- 不处理 detached HEAD 的 branch 推断 (沿用 Phase 1.12 的 `detached_head` reason)

## Design Decisions

| ID | 决策 | 理由 |
|----|------|------|
| D1 | Phase 1.12 原地扩展, 不新增阶段 | 保留 D8 配额 (当前 14/15, 剩 1 格), 参考 standards/core/ten-step-cycle/ |
| D2 | `multi_remote.enabled` 配置可关闭 | 单远程项目免除噪音 |
| D3 | `verify_mode: local_refs` 默认 + CLI 参数覆盖 | 性能优先, 发版流程显式请求 ls_remote |
| D4 | `submodules[]` 保留, 新增 `multi_remote.submodules[]` | 向后兼容, `remote_commit` 语义锁定 = origin remote_head |
| D5 | 顶层 `multi_remote.*` 共享命名空间 + skill 级覆盖 | 用户无需在多处重复配置相同 remote 列表 |
| D6 | `overall_parity` 排除 `ahead` 和 `unknown` | ahead 是正常待推送, unknown 是临时网络故障, 都不应标记为"漂移" |
| D7 | Schema canonical source = helper | 单一真相源, fallback 必须一致 |
| D8 | `diverged` 不自动修复 | force push 涉及人工判断, 仅报告 |
| D9 | ref 不存在降级为 `unknown + no_local_tracking_ref` | 区别于网络故障, 便于诊断 |
| D10 | 推荐规则 priority 1.35 (插入 1.3 和 1.4 之间) | 比 submodule_drift 更高 (范围广), 比 branch_behind_upstream 低 (具体度低) |
| D11 | 不存在 remote 在检测侧 soft-fail (`reason: not_found`) | 检测是只读扫描, 容忍环境异常; 推送侧 (Spec B) 是写操作, 必须严格阻断。两侧语义差异是有意设计, 非不一致 |

## Scope

### 影响文件

| 文件 | 变更类型 |
|------|---------|
| `aria/skills/state-scanner/SKILL.md` | Phase 1.12 扩展检测逻辑 + 输出 schema |
| `aria/skills/state-scanner/references/sync-detection.md` | 新增多远程检测步骤 + consumer inventory 文档 |
| `aria/skills/state-scanner/references/output-formats.md` | 新增 "多远程一致性" 输出区块 |
| `aria/skills/state-scanner/RECOMMENDATION_RULES.md` | 新增 `multi_remote_drift` 规则 |
| `aria/skills/config-loader/DEFAULTS.json` | 新增顶层 `multi_remote.*` + `state_scanner.multi_remote.*` 默认 |
| `aria-plugin-benchmarks/ab-suite/state-scanner.json` | 新增 eval-10 `multi-remote-parity-drift` + eval-11 `submodule-push-github-sync-miss` |

### 不影响

- `submodules[]` 现有字段语义 (`remote_commit` 锁定 origin)
- 其他 Phase (1.0~1.11, 1.13, 1.14)
- 其他 Skills (phase-c-integrator 相关变更在 Spec B)

## Acceptance Criteria

### 核心功能 (必须二元可测)

- [ ] 双 remote 项目, 所有 remotes `parity=equal` 时 `overall_parity=true`, 输出无 `multi_remote_drift` warning
- [ ] 双 remote 项目, github `parity=behind, behind_count=1` 时, 输出含 `multi_remote_drift` warning 且列出 `name=github, behind_count=1, reason=null`
- [ ] 双 remote 项目, github `parity=behind, behind_count=10` 时, behind_count 精确报告 10 (任意正整数都触发, 无阈值)
- [ ] 双 remote 项目, github `parity=diverged, behind_count=2, ahead_count=3` 时, 触发 warning, 修复建议为 "需人工决策", 无自动修复步骤
- [ ] 双 remote 项目, github `parity=ahead, ahead_count=1` 时, `overall_parity=true`, `has_pending_push=true`, **不触发** `multi_remote_drift`
- [ ] 单 remote 项目: `multi_remote.remotes[]` 长度 = 1, 不触发新 warning (与现有行为一致)
- [ ] 单 remote 非 origin 命名 (如 `upstream` 或 `forgejo`): 正确识别并检测, `submodules[].remote_commit` 仍映射 `origin` (若 origin 不存在则为 null)

### Reachable / Reason 字段

- [ ] `reason` 字段存在于 schema: enum = {null, auth_failed, not_found, network_timeout, no_local_tracking_ref, shallow_clone, detached_head}
- [ ] remote auth 失败: `reachable=false, parity=unknown, reason=auth_failed`
- [ ] remote URL 无效 (仓库被删): `reachable=false, parity=unknown, reason=not_found`
- [ ] ls_remote 超时 (> timeout_seconds): `reachable=false, parity=unknown, reason=network_timeout`
- [ ] 本地无 tracking ref 且 verify_mode=local_refs: `reachable=unknown, parity=unknown, reason=no_local_tracking_ref`
- [ ] shallow clone: `parity=unknown, reason=shallow_clone, behind_count=null`

### enforced_remotes 边界

- [ ] `state_scanner.multi_remote.enforced_remotes=null`: 继承顶层 `multi_remote.enforced_remotes`
- [ ] 顶层为 `["origin"]`: 只检测 origin, github 不出现在 `remotes[]`
- [ ] `["origin", "typo"]`: origin 正常检测, typo 输出 `reachable: false, reason: not_found`

### verify_mode 语义

- [ ] CLI `--verify-mode=ls_remote` 覆盖配置: 所有 remote 用 `ls-remote`
- [ ] 默认 `local_refs`: 用本地 refs, `method: "local_refs"` 标注
- [ ] `local_refs` 模式下 FETCH_HEAD > 24h: 输出 `local_refs_stale: true` 字段

### helper fallback

- [ ] `git-remote-helper/SKILL.md` 存在: state-scanner 调用 helper 指令
- [ ] helper 文件不存在: state-scanner 降级为内联实现, 产出**完全相同**的 JSON schema (`multi_remote.*`, 字段名/枚举/结构不变)
- [ ] fallback JSON 通过相同 schema validator (与 helper 版本一致)

### 向后兼容 (Consumer Inventory)

- [ ] `RECOMMENDATION_RULES.md` 的 `submodule_drift` 规则行为不变
- [ ] `submodules[].remote_commit` 字段保留且值 = `multi_remote.submodules[path=X].remotes[name=origin].remote_head`
- [ ] 现有 Phase 1.12 输出的所有字段在本次变更后保留

### 推荐规则

- [ ] `RECOMMENDATION_RULES.md` 包含 `multi_remote_drift` 规则, priority 1.35
- [ ] 规则触发条件 = `multi_remote.overall_parity === false`
- [ ] `has_pending_push=true` (仅 ahead) 不触发此规则
- [ ] `has_unreachable_remote=true` (仅 unknown) 不触发此规则

### AB Benchmark (Rule #6)

- [ ] 新增 eval-10 `multi-remote-parity-drift` 在 `ab-suite/state-scanner.json`
- [ ] 新增 eval-11 `submodule-push-github-sync-miss` (本次事件回归) 在同文件
- [ ] eval-10 覆盖: 双 remote, 一个 behind, per-remote 状态分离, 无"Everything up-to-date"歧义
- [ ] eval-11 覆盖: 2026-04-12 事故场景 (aria 子模块推送 origin 但遗漏 github)
- [ ] 两个 eval 的 with_skill vs without_skill delta 均为正

## Estimation

- **工作量**: 10 小时 (Phase 1.12 扩展 8h + 2 个 AB eval 2h)
- **风险**: 中 (跨多文件协同 + schema 一致性 + 跨平台)
- **依赖硬约束**: `git-remote-helper` 必须先交付 (Spec B T1), 本 Spec 才能合并

# state-scanner 本地/远程同步检测

> **Level**: Minimal (Level 2 Spec)
> **Status**: Draft (Revised after post_spec audit Round 1)
> **Created**: 2026-04-09
> **Revised**: 2026-04-09 (audit findings M3/M4/M6/M7/m4/m5/m8/m11/m12)
> **Target Version**: aria-plugin **v1.11.0** / state-scanner skill internal v2.9.0 (corrected 2026-04-09: aria-plugin 主版本遵循 1.x 序列，state-scanner Skill 内部版本号独立为 2.x)
> **Source**: Forgejo Issue #6 (需求 2/2)
> **Related To**: `state-scanner-issue-awareness` (Issue #6 需求 1/2, 并行开发, 同版本 v2.9.0 发布)

## Why

Aria 采用多子模块架构 (aria / standards / aria-orchestrator)，多会话/多 agent 并行开发时频繁出现：

- 本地落后远程数十个 commit (其他会话已推送)
- 子模块指针偏移 (主仓库已更新记录，但本地 `git submodule update` 未执行)
- 在过时代码上做 state-scanner 分析 → 错误的推荐

state-scanner v2.8.0 已有 11 个子阶段覆盖 Git/OpenSpec/需求/架构/审计/自定义检查，唯独缺失"**本地与远程的同步状态**"这一维度，而这正是十步循环 A.0 "理解当前在哪" 的核心前置条件。

## What

### 新增阶段 1.12: 本地/远程同步检测

在阶段 1.11 (项目级自定义检查) 之后、阶段 2 (推荐决策) 之前，插入同步检测阶段。

### 检测内容

```yaml
sync_status:
  remote_refs_age: "2h"              # FETCH_HEAD 距今时长 (格式: "Nm|Nh|Nd|never")
  has_remote: true                   # git remote -v 是否有输出
  shallow: false                     # git 仓库是否为浅克隆
  current_branch:
    name: "master"                   # null if detached HEAD
    upstream: "origin/master"        # null if no upstream configured
    upstream_configured: true        # 是否有 set-upstream-to
    ahead: 0                         # null if upstream 缺失或 shallow
    behind: 3                        # null if upstream 缺失或 shallow
    diverged: false                  # ahead>0 && behind>0; null if 任一为 null
    reason: null                     # "no_upstream" | "shallow_clone" | "detached_head" | null
  submodules:
    - path: "aria"
      tree_commit: "abc1234"         # 主仓库 HEAD 记录的 commit (`git ls-tree HEAD -- <path>`)
      head_commit: "abc1234"         # 本地 checkout 的 commit (`git -C <path> rev-parse HEAD`)
      remote_commit: "def5678"       # 远程默认分支 commit (见 fallback 链)
      remote_commit_source: "ls-remote"  # "origin_HEAD" | "ls-remote" | "config_default" | null
      drift:
        workdir_vs_tree: false       # 工作目录偏离主仓库记录
        tree_vs_remote: true         # 主仓库记录落后远程
        behind_count: 4              # null if remote_commit 为 null
        hint: "git submodule update --remote aria"
```

**字段语义规则 (统一 AC 表述，修复 M7)**:

| 状态 | `shallow` | `behind` | `reason` |
|------|-----------|----------|----------|
| 正常 | false | 数字 | null |
| 浅克隆 | true | null | `"shallow_clone"` |
| 无 upstream | false | null | `"no_upstream"` |
| detached HEAD | false | null | `"detached_head"` |

### Upstream 探测逻辑 (修复 M3)

```bash
# Step 1: 探测 upstream
upstream=$(git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null) || upstream=""

# Step 2: 根据探测结果决定 ahead/behind 计算
if [ -z "$upstream" ]; then
  # upstream 未配置: ahead/behind 均为 null
  echo "reason: no_upstream"
else
  # 安全计算
  ahead=$(git rev-list --count "${upstream}..HEAD" 2>/dev/null)
  behind=$(git rev-list --count "HEAD..${upstream}" 2>/dev/null)
fi
```

### Submodule `remote_commit` Fallback 链 (修复 M4)

按顺序尝试，首个成功即返回：

```bash
# Tier 1: origin/HEAD (若配置了 git remote set-head)
remote_commit=$(git -C "$sub" rev-parse refs/remotes/origin/HEAD 2>/dev/null)
remote_commit_source="origin_HEAD"

# Tier 2: 无 set-head 时，通过 ls-remote 查询 (网络操作，5s 超时)
if [ -z "$remote_commit" ]; then
  remote_commit=$(timeout 5 git -C "$sub" ls-remote origin HEAD 2>/dev/null | awk '{print $1}')
  remote_commit_source="ls-remote"
fi

# Tier 3: 读 config 中的 branch 名 + 本地 refs
if [ -z "$remote_commit" ]; then
  default_branch=$(git -C "$sub" config --get init.defaultBranch || echo "main")
  remote_commit=$(git -C "$sub" rev-parse "refs/remotes/origin/${default_branch}" 2>/dev/null)
  remote_commit_source="config_default"
fi

# Tier 4: 全部失败 → null + warning
if [ -z "$remote_commit" ]; then
  remote_commit_source="unavailable"
fi
```

**注意**: Tier 2 (`ls-remote`) 是唯一的网络操作，带 5s 超时保护；总体遵循"**不主动 `git fetch`**" 原则。

### 检测策略 (fail-soft)

| 场景 | 行为 | 字段表现 |
|------|------|---------|
| 无 remote (纯本地仓库) | 跳过所有远程相关字段 | `has_remote: false` |
| FETCH_HEAD 缺失 | 标注 `"never"` | `remote_refs_age: "never"` |
| FETCH_HEAD > 24h | 提示 "建议 git fetch" | `remote_refs_age: "2d"` |
| upstream 未配置 | 跳过 upstream 对比 | `ahead: null, behind: null, reason: "no_upstream"` |
| detached HEAD | 跳过分支名和 upstream | `current_branch.name: null, reason: "detached_head"` |
| 浅克隆 | 跳过 behind 计算 | `shallow: true, behind: null, reason: "shallow_clone"` |
| 子模块未初始化 | 跳过该 submodule，不报错 | 该 submodule 条目不出现 |
| submodule remote 指向不同平台 | 不影响本阶段 (sync 检测只用 git 命令) | 正常输出 |
| `git ls-remote` 超时/失败 | Tier 2 失败 → 降级到 Tier 3/4 | `remote_commit_source` 标注 |

**不主动 `git fetch`**: 只读 `FETCH_HEAD` 时间戳 + 已有的 `refs/remotes/origin/*` 引用。Tier 2 的 `ls-remote` 是唯一例外 (带 5s 超时)。

**超时保护**: 总阶段超时 **10s** (考虑 `ls-remote` 可能 5s + 其他命令 5s)。

### 跨平台命令兼容 (修复 m4/m5)

| 功能 | 兼容命令 | 备注 |
|------|---------|------|
| FETCH_HEAD 时间戳 | `git log -1 --format=%cr FETCH_HEAD 2>/dev/null` | 跨平台；避免 `stat -c` / `stat -f` 差异 |
| 浅克隆检测 (git ≥ 2.15) | `git rev-parse --is-shallow-repository` | 返回 `true`/`false` |
| 浅克隆检测 (fallback) | `[ -f "$(git rev-parse --git-dir)/shallow" ] && echo true` | 兼容 git < 2.15 |
| git 版本探测 | `git --version \| awk '{print $3}'` | 决定是否用 fallback |

### 配置 Schema

新增配置块 `state_scanner.sync_check`，由 `config-loader` 加载：

```json
{
  "state_scanner": {
    "sync_check": {
      "enabled": true,
      "check_submodules": true,
      "check_remote": false,
      "warn_after_hours": 24
    }
  }
}
```

| 字段 | 默认 | 说明 |
|------|------|------|
| `enabled` | `true` | 主开关 (本地 git 操作无需网络，默认开启) |
| `check_submodules` | `true` | 是否检测子模块偏差 |
| `check_remote` | `false` | 是否允许 Tier 2 `ls-remote` 网络探测 (默认关闭以避免离线场景卡顿; 开启后 `remote_commit` 四级 fallback 完整启用) |
| `warn_after_hours` | `24` | FETCH_HEAD 陈旧度阈值 |

### 推荐规则联动

新增 2 条规则 (追加到 `RECOMMENDATION_RULES.md`)：

| 规则 ID | 触发条件 | 动作 |
|---------|---------|------|
| `submodule_drift` | 任一 submodule `tree_vs_remote` 为 true | 降级推荐，附加 `git submodule update --remote` 提示 |
| `branch_behind_upstream` | `current_branch.behind >= 5` | 降级推荐，附加 "建议先 git pull" 提示 |

两条规则均**不阻断**推荐，仅降级 + 附加提示 (遵循 fail-soft 原则)。

### 输出格式

```
🔄 同步状态
───────────────────────────────────────────────────────────────
  当前分支: master (落后 origin/master 3 commits)
  远程引用: 2h 前同步
  子模块:
    ✅ standards: 同步
    ⚠️  aria: 落后远程 4 commits
        修复建议: git submodule update --remote aria
```

### 文档组织

遵循 knowledge-manager 建议，SKILL.md 主文档只保留阶段摘要 (约 20 行)，详细逻辑抽到：

- `aria/skills/state-scanner/references/sync-detection.md` (新建)

保持 SKILL.md 总行数可控。

### 不做什么

- ❌ 不主动 `git fetch` (引入网络依赖和阻塞风险)
- ❌ 不列出落后 commit 的标题 (职责边界：state-scanner 是快照不是 changelog)
- ❌ 不递归检测 nested submodules (复杂度失控)
- ❌ 不阻断任何现有工作流 (降级式提示)
- ❌ 不引入新的缓存文件 (直接读 git 状态)

## Decision Records

| ID | 决策 | 理由 |
|----|------|------|
| D1 | Phase 1.12 追加而非插入 1.2 | 不破坏现有 11 个阶段编号和外部引用 |
| D2 | 不主动 git fetch (除 Tier 2 ls-remote) | 网络不可控；用户自主决定新鲜度 |
| D3 | 子模块检测默认开启 | Aria 主场景刚需；纯本地操作零成本 |
| D4 | fail-soft 降级而非报错 | 与现有 Phase 1.1~1.11 一致 (tech-lead + qa 共识) |
| D5 | 不做 Issue 扫描 | 独立 Level 3 OpenSpec 处理 (`state-scanner-issue-awareness`) |
| D6 | 文档抽到 references/sync-detection.md | 避免 SKILL.md 膨胀 (knowledge-manager 建议) |
| D7 | warn_after_hours=24 默认值 | 日常开发节奏的自然分界点 |
| D8 | **子阶段数量上限 15 + 顺序追加规约** (修复 M6 + Round 1 pre_merge tl_m2) | 当前 11 → 本 Spec 后 12；超过 15 必须重构为分组 (如 Git/Context/Quality) 或合并语义相近阶段。**阶段编号分配策略: append-only** — 新阶段一律追加到最大现存编号 + 1 (如当前最大 1.11，下一个必须是 1.12，不允许"插入 1.1.5"或填补空位)。理由: 可预测性 + 外部引用稳定性 |
| D9 | **fail-soft 定义** (修复 m10) | 本 Spec 权威定义：任一命令失败 → 对应字段 null + `reason` 标注 + warning，绝不 exit ≠ 0，绝不阻塞后续阶段。`state-scanner-issue-awareness` 交叉引用此定义 |
| D10 | **remote_commit 四级 fallback** (修复 M4) | Aria 多数子仓库无 `origin/HEAD`；必须通过 ls-remote (5s 超时) → config default → null 的降级链保证可用性 |
| D11 | **upstream 显式探测** (修复 M3) | 先 `rev-parse @{u}` 判断 upstream 存在，再计算 ahead/behind，避免 `rev-list --count` 的 exit ≠ 0 |
| D12 | **配置分层原则** (修复 m1) | 单阶段子配置用嵌套 object (`state_scanner.sync_check.*`)；全局开关用扁平字段 (`state_scanner.confidence_threshold`)。两种风格按作用域区分 |

## Risks (修复 m12)

| 风险 | 概率 | 影响 | 缓解 |
|------|------|------|------|
| 子模块 remote URL 被改动 (fork/mirror) 导致 `ls-remote` 指向错误仓库 | 低 | 中 | `remote_commit_source` 字段透明标注来源，用户可自行判断 |
| `ls-remote` 5s 超时在慢速网络下频繁触发 | 中 | 低 | 失败即降级 Tier 3/4，不阻塞；用户可 `check_remote: false` 禁用 |
| 浅克隆 fallback 探测 `.git/shallow` 在 worktree 下路径不同 | 低 | 低 | 通过 `git rev-parse --git-dir` 动态获取 git 目录 |
| 子模块检测遍历耗时随 submodule 数量线性增长 | 低 | 低 | 当前 Aria 3 子模块；超过 10 个时引入并行 (future) |

## Scope

### 影响文件

| 文件 | 变更类型 |
|------|---------|
| `aria/skills/state-scanner/SKILL.md` | 新增阶段 1.12 摘要 + 配置表格更新 (+ 25 行) |
| `aria/skills/state-scanner/references/sync-detection.md` | **新建** (完整检测逻辑 + 四级 fallback + 跨平台命令) |
| `aria/skills/state-scanner/references/output-formats.md` | 新增同步状态输出区块 |
| `aria/skills/state-scanner/RECOMMENDATION_RULES.md` | 新增 `submodule_drift` + `branch_behind_upstream` 规则 |
| `aria/skills/config-loader/SKILL.md` | 新增 `state_scanner.sync_check.*` 默认值 |
| `.aria/config.template.json` | 新增 `state_scanner.sync_check` 默认 block |
| `docs/architecture/system-architecture.md` (修复 m11) | PATCH 级更新，标注 Phase 1.12 扩展点 |
| `aria/.claude-plugin/plugin.json` | version: 2.8.0 → 2.9.0 |
| `aria/.claude-plugin/marketplace.json` | version 同步 |
| `aria/VERSION` | 同步 |
| `aria/CHANGELOG.md` | 新增 [2.9.0] 条目 |
| `aria/README.md` | 版本号 + Skills 描述更新 |

### 不影响

- workflow-runner, Phase Skills, audit-engine
- 现有 11 个阶段 (1 ~ 1.11) 的逻辑
- 其他 Skill (forgejo-sync, requirements-sync, arch-update)

## Estimation

- **工作量**: 4-6 小时
- **风险**: 低 (纯本地 git 操作，无外部依赖)
- **AB Benchmark**: **必须** (规则 #6: 新增 Skill 逻辑必须跑 `/skill-creator benchmark`，delta 为正值方可合并)

## Acceptance Criteria (修复 m8: 全部可客观验证)

- [ ] AC1: state-scanner v2.9.0 输出包含 "🔄 同步状态" 区块 (通过字符串匹配验证)
- [ ] AC2: 在 Aria 本仓库运行时，`sync_status.submodules[]` 包含 `aria` 和 `standards` 两个条目，且 `tree_commit`/`head_commit`/`remote_commit` 字段非 null
- [ ] AC3: 纯本地 git 仓库 (无 remote) 输出 `has_remote: false`，其他字段不存在，exit code = 0
- [ ] AC4: 浅克隆场景下输出 `{shallow: true, behind: null, reason: "shallow_clone"}` (修复 M7: 字段语义与 D8/检测策略表格一致)
- [ ] AC5: upstream 未配置场景下输出 `{ahead: null, behind: null, reason: "no_upstream"}` (修复 M3)
- [ ] AC6: `ls-remote` 超时 (>5s) 场景下，`remote_commit_source: "unavailable"`，对应 submodule 不抛错
- [ ] AC7: `/skill-creator benchmark` AB 对比 delta ≥ +0.3 (对齐 qa-engineer 基线水位)
- [ ] AC8: `aria-plugin-benchmarks/ab-results/latest/summary.yaml` 包含本次 state-scanner v2.9.0 记录
- [ ] AC9: 所有 **12 个** 影响文件已按 Scope 表修改 (其中 **5 个版本号文件** 一致为 2.9.0: `plugin.json` / `marketplace.json` / `VERSION` / `CHANGELOG.md` / `README.md`；`docs/architecture/system-architecture.md` 不含版本号字段，仅 PATCH 级内容更新)
- [ ] AC10: 本地 git 版本 < 2.15 时 fallback 到 `.git/shallow` 检测，不报 "unknown option"
- [ ] AC11 (pre_merge Round 1 M1 fix): 本地领先远程场景 (`behind_count == 0 AND ahead_count > 0`) 输出 `hint_type: "push"` 且 **不触发** `submodule_drift` 规则, 改为 info 级 "push" 建议, 避免发出破坏性 "update --remote" 提示
- [ ] AC12 (pre_merge Round 1 M1 fix): `tree_vs_remote == true` 但双方计数均为 0 (shallow clone 异常场景) 输出 `hint_type: "manual_check"`, 提示人工检查
- [ ] AC13 (pre_merge Round 2 cr_r2_m2 fix): `rev-list --count` 返回空字符串时, 方向判定函数 `is_positive_int` 正确处理, 不报 "integer expression expected"

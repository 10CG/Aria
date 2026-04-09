# state-scanner Issue 感知能力

> **Level**: Full (Level 3 Spec)
> **Status**: **Complete** (archived 2026-04-09)
> **Created**: 2026-04-09
> **Revised**: 2026-04-09 (post_spec audit R1/R2 + pre_merge audit R1-R4)
> **Archived**: 2026-04-09
> **Target Version**: aria-plugin **v1.11.0** / state-scanner skill internal v2.9.0
> **Source**: Forgejo Issue #6 (需求 1/2)
> **Related To**: `state-scanner-remote-sync-check` (同版本并行发布)
> **Merged**: aria-plugin#4 (b052a3e), Aria#7 (5ac335a)
> **US**: US-008
> **Tasks**: [tasks.md](./tasks.md)

## Why

state-scanner 当前扫 Git/OpenSpec/需求/架构/审计/自定义检查，唯独缺 **open issues** 这一维度。实际使用中 Issue 是重要的工作输入源：

- 主仓库的 bug reports / feature requests (如本 Issue #6 自身)
- 子模块仓库的独立 issue tracker (如 aether-plugin)
- Issue 与 User Story / OpenSpec 的关联状态（是否已被纳入开发计划）

没有 Issue 感知会导致：
- AI 在推荐工作流时忽略 pending 的 blocker issues
- 用户需手动轮询平台检查 "还有什么要做"
- 新 Spec 创建时无法自动引用关联 Issue

## 与 sync-check 的协同 (修复 M1)

两 Spec **并行开发, 同 v2.9.0 发布**，无真实依赖关系：

- **无共享代码**: 本 Spec 不复用 sync-check 的任何 helper / schema / lib
- **仅术语对齐**: "fail-soft" 定义锚定在 `state-scanner-remote-sync-check/proposal.md#D9`，本 Spec 直接引用不重述
- **AB delta 归因**: 通过 feature flag (`issue_scan.enabled=false` 作为默认基线) 隔离，benchmark 对比 `enabled=true` vs `enabled=false` 得到纯 Issue 扫描的 delta
- **Merge Gate 独立**: 本 Spec 的合并不阻塞 sync-check 的合并，反之亦然 (只要各自 benchmark delta 为正)

## What

### 新增阶段 1.13: Issue 感知扫描

在阶段 1.12 (同步检测) 之后、阶段 2 (推荐决策) 之前，插入 Issue 扫描阶段。

### 平台适配

| 平台 | 识别方式 | 调用方式 |
|------|---------|---------|
| **Forgejo** | 见平台检测逻辑 | `forgejo GET /repos/{owner}/{repo}/issues?state=open&limit=20` |
| **GitHub** | remote URL 包含 `github.com` | `gh issue list --state open --json number,title,labels,url --limit 20` |
| **GitLab** (v2 扩展) | 本 Spec 不实现 | 预留抽象接口 |

**首版仅适配 Forgejo + GitHub**，两者已有 CLI wrapper 可用 (规则: 不在 skill 内管理 token)。

### 平台检测逻辑 (修复 M5)

需要在 `.aria/config.template.json` 的 `state_scanner` block 中扩展字段 (新增 T0 任务覆盖)：

```json
{
  "state_scanner": {
    "issue_scan": {
      "enabled": false,
      "platform": null,
      "platform_hostnames": {
        "forgejo": ["forgejo.10cg.pub"],
        "github": ["github.com"]
      },
      "cache_ttl_seconds": 900,
      "limit": 20,
      "label_filter": []
    }
  }
}
```

**检测优先级**:

1. **显式声明**: `state_scanner.issue_scan.platform` 字段非 null → 直接使用
2. **hostname 匹配**: `git remote get-url origin` 的 hostname 与 `platform_hostnames` 对比
3. **兜底推断**: URL 包含 `github.com` → github；URL 包含已知 Forgejo 域名 → forgejo
4. **全失败**: `fetch_error: "platform_unknown"` + 静默跳过

### 统一 IssueItem Normalize 映射 (修复 m6)

| 规范字段 | Forgejo API 路径 | GitHub (gh) JSON 路径 |
|---------|------------------|----------------------|
| `number` | `.number` | `.number` |
| `title` | `.title` | `.title` |
| `labels[]` | `.labels[].name` | `.labels[].name` |
| `url` | `.html_url` | `.url` |
| `body` | `.body` | `.body` |

所有字段缺失时 → 空字符串（labels 为空数组），不使用 null 避免 jq 嵌套判断。

### 检测内容

```yaml
issue_status:
  fetched_at: "2026-04-09T10:23:00Z"
  source: cache | live | unavailable
  fetch_error: null | "network_unavailable" | "auth_failed" | "rate_limited" | "platform_unknown"
  platform: forgejo | github | null
  open_count: 3
  items:
    - number: 6
      title: "state-scanner: add issue scan and sync detection"
      labels: ["enhancement", "skill"]
      url: "https://forgejo.10cg.pub/10CG/Aria/issues/6"
      linked_openspec: "state-scanner-issue-awareness"  # 启发式匹配
      linked_us: null                                    # 启发式匹配
  label_summary:                      # 按 label 分组统计
    bug: 1
    enhancement: 2
```

### 关联启发式 (Heuristic Linking)

对每个 open issue 尝试匹配：
- Issue 标题/正文中的 `US-NNN` 引用 → `linked_us`
- Issue 标题/正文中的 OpenSpec change 名称 → `linked_openspec`
- 匹配失败则为 `null`

**匹配规则 (修复 m7)**:
- **单词边界匹配**，不做裸子串匹配
- `US-NNN` 正则: `\bUS-\d{3,}\b` (至少 3 位数字)
- OpenSpec 目录名正则: `(?<![a-z0-9/-])<change-name>(?![a-z0-9/-])`
  - 负向前后查找避免误匹配 URL 路径 (如 `.../openspec/changes/my-change/proposal.md` 不应匹配到 `my-change`)
- 仅扫描 Issue 的 `title` 和 `body`，不扫描 comments (首版)

**明确标注为启发式**，不做断言。不在本 Spec 做双向反查 (OpenSpec → Issue)。

### 缓存策略

**15 分钟 TTL，写入 `.aria/cache/issues.json`**：

```json
{
  "fetched_at": "2026-04-09T10:23:00Z",
  "platform": "forgejo",
  "open_issues": [...]
}
```

- 15 分钟内重复调用直接读缓存 → 单次会话内零 API 打扰
- 跨会话首次扫描打一次 API (~2s)
- **缓存失效时同步 refresh** (修复 M10): bash skill 无后台任务模型，改为同步阻塞调用 API → 成功则覆写缓存，失败则沿用旧缓存 + `warning: "stale_cache_api_failed"`
- **路径命名空间边界** (修复 m3): `.aria/cache/` 为 Skill 运行时缓存目录，与 `.aria/config.json` 职责严格分离。`config-loader` 不扫描 `.aria/cache/`，须加入 `.gitignore`

### 失败处理 (fail-soft, 继承 sync-check D9 定义)

**统一的 10 个 `fetch_error` 枚举值** (修复 M9: tasks.md T3 与本表对齐):

| # | 场景 | `fetch_error` 枚举 | 用户面板行为 |
|---|------|-------------------|-------------|
| 1 | 离线 / 网络不可达 | `network_unavailable` | 降级，用缓存（若有） |
| 2 | CLI 未安装 (forgejo/gh) | `cli_missing` | 提示安装命令 |
| 3 | token 未配置 | `auth_missing` | 提示 "未配置 token，跳过" |
| 4 | HTTP 401/403 | `auth_failed` | 提示 "权限不足 / token 过期" |
| 5 | HTTP 429 | `rate_limited` | 读 `Retry-After`，用缓存 |
| 6 | HTTP 404 (真无此仓库) 或 伪 404 (私有+无权限) | `not_found_or_no_access` | 歧义提示 |
| 7 | API 响应 > 5s | `timeout` | 用缓存 |
| 8 | 平台识别失败 | `platform_unknown` | 静默跳过 |
| 9 | JSON 解析失败 | `parse_error` | 用缓存 + warning |
| 10 | 兜底未分类错误 | `unknown` | warning + stderr 片段 |

**总阶段超时**: 12s (修复 m9: 原 8s 对 Forgejo + Cloudflare Access 首次握手 TLS 过紧)
**单次 API 调用超时**: 5s

**绝不阻塞主流程** (锚定 `state-scanner-remote-sync-check/proposal.md#D9` 定义)。

### 配置 Schema (完整版, 修复 M5)

```json
{
  "state_scanner": {
    "issue_scan": {
      "enabled": false,
      "platform": null,
      "platform_hostnames": {
        "forgejo": ["forgejo.10cg.pub"],
        "github": ["github.com"]
      },
      "cache_ttl_seconds": 900,
      "cache_path": ".aria/cache/issues.json",
      "stage_timeout_seconds": 12,
      "api_timeout_seconds": 5,
      "limit": 20,
      "label_filter": []
    }
  }
}
```

| 字段 | 默认 | 说明 |
|------|------|------|
| `enabled` | **`false`** (opt-in) | 默认关闭，需用户显式开启 |
| `platform` | `null` | 显式指定平台 (forgejo/github)；null 则自动检测 |
| `platform_hostnames` | `{forgejo:[...], github:[...]}` | hostname → 平台映射表，用户可扩展 |
| `cache_ttl_seconds` | `900` | 缓存 15 分钟 |
| `cache_path` | `.aria/cache/issues.json` | 缓存文件位置 |
| `stage_timeout_seconds` | `12` | 整阶段超时 (修复 m9) |
| `api_timeout_seconds` | `5` | 单次 API 调用超时 |
| `limit` | `20` | 单次拉取上限 |
| `label_filter` | `[]` | 空表示不过滤；可设 `["bug","blocker"]` |

**默认关闭原因**: 需要网络 + token 配置，不应在默认配置下就尝试 API 调用。

**T0 前置任务**: 扩展 `.aria/config.template.json` + `aria/skills/config-loader/SKILL.md` 的默认值表格（见 tasks.md T0）。

### 推荐规则联动

新增 1 条规则 (追加到 `RECOMMENDATION_RULES.md`)：

| 规则 ID | 触发条件 | 动作 |
|---------|---------|------|
| `open_blocker_issues` | 存在 label 包含 `blocker`/`critical` 的 open issue | 降级推荐，提示 "先 triage N 个阻塞 Issue" |

首版**不**新增过于激进的规则，避免污染现有推荐体系 (qa-engineer 建议)。

### 输出格式

```
🎫 Open Issues
───────────────────────────────────────────────────────────────
  平台: Forgejo (10CG/Aria) — 3 open
  📌 #6  state-scanner: add issue scan      [enhancement]
         → 已关联 OpenSpec: state-scanner-issue-awareness
  📌 #5  Pulse 项目集成                      [feature]
  📌 #4  某 bug                              [bug]
  数据来源: cache (2m ago) | ttl: 15m
```

### 文档组织

- `aria/skills/state-scanner/references/issue-scanning.md` (新建)
  - 平台适配详细逻辑
  - 启发式关联算法
  - 所有边界场景和错误码

SKILL.md 主文档只保留阶段摘要 (~25 行)。

### 不做什么 (首版)

- ❌ 不递归扫描子模块 issues (主仓库 only，后续扩展点 `scan_submodule_issues`)
- ❌ 不做 OpenSpec → Issue 反查
- ❌ 不支持 GitLab (预留接口，v2 实现)
- ❌ 不做 Issue 创建/评论/关闭 (这是 `forgejo-sync` 的职责)
- ❌ 不做 PR 扫描 (独立功能，需单独 Spec)
- ❌ 不在 skill 内管理 API token (严格依赖已有 CLI wrapper)

## Decision Records

| ID | 决策 | 理由 |
|----|------|------|
| D1 | Phase 1.13 追加，位于 1.12 之后 | 顺序依赖 (sync 早于 issue 便于上下文理解)；无代码依赖 |
| D2 | 默认 `enabled: false` | 需网络 + token；opt-in 保证离线场景零影响 |
| D3 | 15 分钟 TTL 缓存 | 单会话零打扰 + 跨会话新鲜度平衡 |
| D4 | 仅复用 CLI wrapper (forgejo/gh) + 版本锚定 (Round 1 pre_merge tl_m3 fix) | 不在 skill 内管理 token；遵循既有信任模型。**依赖契约**: 本 Spec 锚定 `forgejo` CLI wrapper 的 `GET /repos/{owner}/{repo}/issues` 响应 JSON shape 必须含 `number` / `title` / `labels[].name` / `html_url` / `body` 字段 (对应 Gitea API v1 schema)。wrapper 升级改变 shape 必须在本 Spec addendum 声明兼容层，否则 `normalize` 映射会静默破坏。首版测试基于 `forgejo` wrapper 当前行为（2026-04-09 快照）。 |
| D5 | 首版仅 Forgejo + GitHub | Aria 主场景；GitLab 作为 v2 扩展 |
| D6 | 不递归子模块 issues | 噪音控制；独立 config 开关作为扩展点 |
| D7 | 启发式关联 (非断言) | 避免误判；明确标注为启发式 |
| D8 | `linked_us` / `linked_openspec` 仅前向 | 反向查找复杂度高，留作 v3 |
| D9 | **总阶段超时 12s** (修复 m9) | Forgejo + Cloudflare Access TLS 握手开销 + 5s API + 缓冲；原 8s 对 p95 场景过紧 |
| D10 | **与 sync-check 同 v2.9.0 并行发布** (修复 M1/M2) | 消除伪依赖和双 bump 升级噪音；AB delta 归因通过 `enabled=true/false` feature flag 实现 |
| D11 | **同步 refresh，失败沿用旧缓存** (修复 M10) | bash skill 无后台任务模型；同步模型更简单且符合 fail-soft |
| D12 | **fail-soft 定义锚定 sync-check D9** (修复 m10) | 避免同一术语在两 Spec 分别定义导致语义漂移 |
| D13 | **平台 hostname 可配置** (修复 M5) | 支持自托管 Forgejo 实例；默认仅含 10cg.pub |
| D14 | **启发式匹配单词边界** (修复 m7) | 避免 URL 路径被误匹配为 OpenSpec change 名 |
| D15 | **10 个 fetch_error 枚举值统一** (修复 M9) | proposal 与 tasks.md 同源，避免实现歧义 |

## Rollback Plan (修复 M8)

Level 3 变更要求完整回滚策略。v2.9.0 发布后若发现严重 bug：

### 场景 A: 运行时降级 (首选，零发布)

用户/CI 在 `.aria/config.json` 设置：
```json
{ "state_scanner": { "issue_scan": { "enabled": false } } }
```
→ issue-awareness 阶段静默跳过，state-scanner 退化到无 Issue 扫描的行为。**代码保留，可随时重新开启**。

### 场景 B: 配置推送 (中度)

若需要所有用户紧急禁用：
- 发布 `v2.9.1` hotfix，将 `config-loader` 中 `state_scanner.issue_scan.enabled` 默认值强制改为 `false` 且忽略用户配置
- 保留 sync-check 功能不受影响 (独立 feature flag)

### 场景 C: 代码回退 (重度, 最后手段)

- 在 `aria-plugin` 仓库创建 hotfix 分支: `git revert <commit-range>`
- 发布 `v2.9.1`，移除 Phase 1.13 代码
- sync-check (Phase 1.12) 保留，仅回退 issue-awareness 相关文件
- 影响文件 (需 revert): SKILL.md 1.13 章节 / issue-scanning.md / RECOMMENDATION_RULES `open_blocker_issues` / config schema

### 监控指标

发布后 48h 内监控：
- `/skill-creator benchmark` AB delta 是否仍为正
- `aria-report` 频次是否突增 (用户反馈信号)
- state-scanner 阶段失败率 (若 issue-awareness 频繁 timeout 说明 12s 仍不够)

## Scope

### 影响文件

| 文件 | 变更类型 |
|------|---------|
| `aria/skills/state-scanner/SKILL.md` | 新增阶段 1.13 摘要 (~25 行) |
| `aria/skills/state-scanner/references/issue-scanning.md` | **新建** (完整检测逻辑 + 10 种 fetch_error + normalize 映射 + 启发式正则) |
| `aria/skills/state-scanner/references/output-formats.md` | 新增 Open Issues 输出区块 (含降级状态示例) |
| `aria/skills/state-scanner/RECOMMENDATION_RULES.md` | 新增 `open_blocker_issues` 规则 |
| `aria/skills/config-loader/SKILL.md` | 新增 `state_scanner.issue_scan.*` 默认值 (9 个字段) |
| `.aria/config.template.json` | 新增 `state_scanner.issue_scan` 完整 block |
| `.gitignore` | 新增 `.aria/cache/` (修复 m3) |
| `aria/.claude-plugin/plugin.json` | version: 2.8.0 → **2.9.0** (与 sync-check 同版本) |
| `aria/.claude-plugin/marketplace.json` | 同步 2.9.0 |
| `aria/VERSION` | 同步 2.9.0 |
| `aria/CHANGELOG.md` | 新增 [2.9.0] 条目 (合并 sync-check 和 issue-awareness 两个 feature) |
| `aria/README.md` | 版本号 + Skills 描述 |

### 不影响

- workflow-runner / Phase Skills / audit-engine
- `forgejo-sync` (职责边界：sync 做写操作，issue-awareness 做只读感知)
- `requirements-sync` (与需求同步解耦)
- 现有 12 个阶段 (1 ~ 1.12)

### 边界明确

| Skill | 职责 |
|-------|------|
| **state-scanner.issue-awareness** | 只读扫描 + 展示 + 启发式关联 |
| **forgejo-sync** | Issue/PR 的 CRUD 操作 (创建/评论/关闭) |
| **requirements-sync** | US ↔ Forgejo Issue 双向状态同步 |

## Estimation

- **工作量**: 10-14 小时 (Level 3)
- **风险**: 中 (平台 API 适配 + 错误场景多)
- **AB Benchmark**: **必须** (规则 #6)
- **预置条件**: `state-scanner-remote-sync-check` 已合并，fail-soft 框架可复用

## Acceptance Criteria (修复 m8: 全部可客观验证)

- [ ] AC1: state-scanner v2.9.0 输出包含 "🎫 Open Issues" 区块 (字符串匹配验证)
- [ ] AC2: 在 Aria 仓库设置 `enabled: true` 后，能拉取 Issue #5 和 #6 并显示标题
- [ ] AC3: 默认 `enabled: false` 时，state-scanner 输出**不包含**任何 issue-awareness 相关字段
- [ ] AC4: 离线场景下 (`forgejo` CLI 失败) 输出包含 `fetch_error: "network_unavailable"` 和降级文本 "跳过"
- [ ] AC5: `.aria/config.json` 缺 token 时 → `fetch_error: "auth_missing"`
- [ ] AC6: 连续 2 次调用 (间隔 < 15 min)：第二次 `source: "cache"`，不触发 API 调用
- [ ] AC7: 缓存存在但 > 15 min → API 调用；API 失败 → 沿用旧缓存 + `warning: "stale_cache_api_failed"`
- [ ] AC8: HTTP 429 响应 → `fetch_error: "rate_limited"` + 使用缓存
- [ ] AC9: 启发式正确识别测试用例：
    - Issue 标题 "fix US-006 auth" → `linked_us: "US-006"`
    - Issue 正文包含 `state-scanner-issue-awareness` (非 URL 形式) → `linked_openspec: "state-scanner-issue-awareness"`
    - Issue 正文包含 `https://.../openspec/changes/state-scanner-issue-awareness/` → `linked_openspec: null` (单词边界保护)
- [ ] AC10: `stage_timeout_seconds: 12` 生效，超时场景 `fetch_error: "timeout"`
- [ ] AC11: `/skill-creator benchmark` AB 对比 (`enabled=true` vs `enabled=false`) delta ≥ +0.3
- [ ] AC12: `aria-plugin-benchmarks/ab-results/latest/summary.yaml` 包含本次 issue-awareness 记录
- [ ] AC13: 所有 **12 个** 影响文件已按 Scope 表修改 (其中 **5 个版本号文件** 一致为 2.9.0: `plugin.json` / `marketplace.json` / `VERSION` / `CHANGELOG.md` / `README.md`；`.gitignore` 和 `config.template.json` 不含版本号字段，仅 schema/规则更新)
- [ ] AC14: `.gitignore` 包含 `.aria/cache/` 且 Git status 不追踪缓存文件
- [ ] AC15: 10 种 `fetch_error` 枚举值在 tasks.md T3 和 proposal.md 同步

# Aria Dashboard — 项目进度看板与自动开发闭环

> **Level**: Full (Level 3 Spec)
> **Status**: In Progress (Phase 1-2 Complete, Phase 3a Pending)
> **Created**: 2026-04-02
> **Parent Story**: [US-005](../../docs/requirements/user-stories/US-005.md)
> **Target Version**: v1.4.0
> **Reference Implementation**: SilkNode `/progress-dashboard/`

## Why

Aria 方法论的所有状态数据（UPM、OpenSpec、User Stories、审计报告、AB benchmark）都以 Markdown/JSON 文件存储在 Git 仓库中。但这些数据只能通过 CLI (`/aria:state-scanner`) 或直接读文件获取，存在以下局限：

1. **非 CLI 用户无法访问** — PM、设计师等角色无法查看项目进度
2. **无全局视图** — state-scanner 是即时快照，缺少趋势和历史对比
3. **反馈需要 CLI** — 提交 bug/feature 需要通过 `/aria:report` 或手动创建 issue
4. **无自动响应** — issue 创建后需要人类手动启动开发流程

SilkNode 项目已实现了一个针对自身的 progress-dashboard，验证了从 Markdown 文件生成可视化看板的可行性。需要将其提炼为 Aria 通用能力。

## What

### 系统架构

```
┌─────────────────────────────────────────────────┐
│              Web 看板 (部署层)                    │
│                                                   │
│  进度总览 │ Story 看板 │ OpenSpec │ 审计历史      │
│  Phase/KPI│ 三列拖拽   │ 活跃+归档│ 轮次/verdict │
│           │            │ 耗时统计 │ 收敛趋势     │
│  AB 趋势  │ Issue 表单 │          │              │
│  delta 图 │ 提交反馈   │          │              │
│                                                   │
│           Issue 存储适配器                         │
│  ┌────────────┐    ┌─────────────────┐           │
│  │ Git 原生    │    │ GitHub/Forgejo  │           │
│  │.aria/issues/│    │ API             │           │
│  └────────────┘    └─────────────────┘           │
└──────────────────────┬────────────────────────────┘
                       │ 数据源 (Markdown/JSON)
┌──────────────────────┴────────────────────────────┐
│              项目仓库 (Git)                         │
│  UPM.md / openspec/ / user-stories/                │
│  .aria/issues/ / .aria/audit-reports/              │
│  aria-plugin-benchmarks/                            │
└──────────────────────┬────────────────────────────┘
                       │ 心跳扫描
┌──────────────────────┴────────────────────────────┐
│           心跳 Agent (定时触发)                      │
│  扫描新 issue → 分析复杂度 → 十步循环全自动        │
│  → 更新 issue 状态 → 看板刷新                      │
└───────────────────────────────────────────────────┘
```

### Phase 1: 完整看板 (MVP, 12-16h)

**交付物**: `aria-dashboard` Skill + 单文件 HTML 模板

**触发**: `/aria:dashboard` → 解析数据 → 生成 `.aria/dashboard/index.html` → 打开浏览器

**数据解析器** (提炼自 SilkNode `progress-dashboard/src/lib/`):

| 解析器 | 数据源 | 输出 |
|--------|--------|------|
| parse-upm | UPM.md (UPMv2-STATE YAML) | Phase/KPI/Cycle/Risks |
| parse-openspec | openspec/changes/ + archive/ | Spec 列表 + 状态 + 耗时统计 |
| parse-stories | docs/requirements/user-stories/ | Story 列表 + Status |
| parse-audit | .aria/audit-reports/ | 审计历史 (轮次/收敛/verdict) |
| parse-benchmark | aria-plugin-benchmarks/ | AB delta 摘要 |

**HTML 模板**: 单文件自包含 (CSS + JS 内联)，使用 SKILL.md 中定义的布局模板，AI 填充数据生成。

**看板区块**:

```
┌──────────────────────────────────────────────────────┐
│  项目名 — Phase X: {name} ({status})    v{version}   │
├──────────┬──────────┬──────────┬─────────────────────┤
│ KPI 1    │ KPI 2    │ KPI 3    │ Cycle #{N}          │
│ {val/tgt}│ {val/tgt}│ {val/tgt}│ {完成率}%           │
├──────────┴──────────┴──────────┴─────────────────────┤
│                                                        │
│  ┌─ TODO ──┐  ┌─ 进行中 ─┐  ┌─ 已完成 ──┐           │
│  │ US-003  │  │          │  │ US-001    │           │
│  │ US-005  │  │          │  │ US-002    │           │
│  │         │  │          │  │ US-004    │           │
│  └─────────┘  └──────────┘  └───────────┘           │
│                                                        │
├────────────────────────┬─────────────────────────────┤
│  OpenSpec              │  审计历史                     │
│  活跃: {N}  归档: {N}  │  最近 5 次审计               │
│  ┌─────────────────┐  │  checkpoint verdict rounds   │
│  │ name  status    │  │  post_spec  PASS   2        │
│  │ name  status    │  │  pre_merge  FAIL   3        │
│  │ 平均耗时: {N}天 │  │  ...                         │
│  └─────────────────┘  │                               │
├────────────────────────┴─────────────────────────────┤
│  AB Benchmark 摘要                                     │
│  Skills: {N} tested | Avg delta: +{N} | WITH_BETTER: {N}% │
└────────────────────────────────────────────────────────┘
```

### Phase 2: Issue 提交 + 存储 (6-10h)

**升级**: 单文件 HTML → 可部署 Web 应用 (轻量 Node.js 或纯前端 + Git API)

**Issue 表单**:

```yaml
字段:
  title: string (必填)
  description: string (必填)
  priority: P0 | P1 | P2 | P3 (默认 P2)
  type: bug | feature | question
```

**Issue 存储适配器**:

```
Git 原生模式 (默认, 零依赖):
  提交 → 写入 .aria/issues/ISSUE-{timestamp}.md
  格式:
    ---
    title: {title}
    type: {type}
    priority: {priority}
    status: open
    created: {ISO 8601}
    ---
    {description}

  → git add + commit (由看板后端或 AI 执行)

API 模式 (可选配置):
  .aria/config.json:
    "dashboard": {
      "issue_backend": "github",
      "issue_repo": "10CG/aria-plugin"
    }
  → 调用 GitHub/Forgejo Issues API 创建
```

### Phase 3a: 心跳扫描 Skill (8-12h)

> **注意**: 原 Phase 3 经 Agent Team 三轮讨论后拆分。Phase 3b (定时心跳) 和
> Phase 3c (半自动开发闭环) 需要外部编排器 (aria-orchestrator)，已独立为
> [US-007](../../docs/requirements/user-stories/US-007.md)。

**交付物**: `aria-heartbeat` Skill (手动触发, 只读)

**触发**: `/aria:heartbeat scan` (人类手动执行)

**扫描流程**:

```
每次扫描:
  1. 扫描数据源:
     - Git 模式: ls .aria/issues/*.md → 筛选 status: open
     - API 模式: GET /repos/{owner}/{repo}/issues?state=open

  2. 对每个 open issue:
     a. 分析复杂度:
        - 关键词 + 描述长度 + 影响范围 → Level 1/2/3
     b. 生成分析报告 (不自动开发):
        - Issue 标题、优先级、复杂度评估
        - 推荐的处理方式 (手动修复 / 创建 OpenSpec / 需讨论)
     c. 更新 issue frontmatter:
        - 添加 analyzed_at, complexity_level 字段

  3. 输出待处理 issue 报告:
     - 按优先级排序
     - 附复杂度评估和推荐行动
```

**配置** (.aria/config.json):

```json
{
  "heartbeat": {
    "issue_backend": "git",
    "issue_repo": ""
  }
}
```

## Impact

| Type | Description |
|------|-------------|
| **Positive** | 非 CLI 用户可通过浏览器参与项目管理 |
| **Positive** | Issue→开发的全自动闭环，大幅减少人工干预 |
| **Positive** | 进度度量和审计可视化提供数据驱动的改进依据 |
| **Risk** | 心跳 Agent 全自动开发需要可靠的测试覆盖防止错误代码合并 |
| **Risk** | Issue 存储双模式增加系统复杂度，需要适配器抽象 |
| **Limitation** | Phase 3b/3c 已拆分到 US-007 (aria-orchestrator) |

## Constraints

| 约束 | 影响 |
|------|------|
| Phase 1 零外部依赖 | 单文件 HTML，不需要 npm/Node.js |
| Git 原生模式优先 | 默认不依赖 GitHub/Forgejo API |
| Phase 3a 只读 | 手动扫描 + 分析报告，不自动开发 |
| 单文件 HTML 上限 | Phase 1 的 HTML 需控制在合理体积内 |

## Dependencies

- SilkNode progress-dashboard 代码提炼 (解析逻辑参考)
- aria-report (Issue 提交可复用 routing 逻辑)
- Phase 3b/3c 依赖 → US-007 (aria-orchestrator)

## Success Criteria

### Phase 1
- [ ] `/aria:dashboard` 在 Aria 项目上生成正确的看板 HTML
- [ ] 在 Kairos 项目上同样可用 (跨项目验证)
- [ ] 包含全部 5 个数据区块 (UPM/Stories/OpenSpec/审计/Benchmark)
- [ ] AB benchmark: aria-dashboard delta > 0

### Phase 2
- [ ] Issue 通过看板提交后出现在 `.aria/issues/`
- [ ] API 模式可通过配置切换到 GitHub Issues
- [ ] 看板可部署为长期运行的 Web 服务

### Phase 3a
- [ ] `/aria:heartbeat scan` 扫描 open issue 并分析复杂度
- [ ] 生成待处理 issue 报告 (只读, 不自动开发)
- [ ] Issue frontmatter 更新 analyzed_at + complexity_level

> Phase 3b/3c → [US-007 aria-orchestrator](../../docs/requirements/user-stories/US-007.md)

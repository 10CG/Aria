# Aria Dashboard — 任务分解

> **Parent**: proposal.md
> **Estimated Total**: 30-42h (Phase 1-3)

## Phase 1: 完整看板 (12-16h)

### T1: 数据解析器
- **估时**: 6-8h
- **内容**: 新建 `aria/skills/aria-dashboard/` Skill
  - parse-upm: UPMv2-STATE YAML 解析 (参考 SilkNode `parse-upm.ts`)
  - parse-openspec: proposal.md frontmatter 提取 + 归档时间统计
  - parse-stories: User Story Status 提取 + 三列分组
  - parse-audit: .aria/audit-reports/ 解析 (frontmatter: checkpoint/verdict/rounds/converged)
  - parse-benchmark: aria-plugin-benchmarks/ 摘要提取 (summary.yaml 或 benchmark.json)
  - 所有解析器容错: 目录不存在 → 空数据, 不报错
- **依赖**: 无
- **Agent**: backend-architect

### T2: HTML 模板 + 生成
- **估时**: 4-6h
- **内容**:
  - 单文件 HTML 模板 (CSS + JS 内联, 无外部依赖)
  - 5 个区块: 进度总览 / Story 看板 / OpenSpec / 审计历史 / AB 摘要
  - 响应式布局 (桌面 + 移动端)
  - `/aria:dashboard` 触发: 解析 → 填充模板 → 写入 `.aria/dashboard/index.html` → 打开
- **依赖**: T1
- **Agent**: tech-lead

### T3: 跨项目验证
- **估时**: 2-2h
- **内容**:
  - 在 Aria 项目上生成看板 (完整数据)
  - 在 Kairos 项目上生成看板 (部分数据: 有 UPM + OpenSpec, 无审计报告)
  - 确认容错: 缺少数据源时区块显示"未配置"而非报错
- **依赖**: T1, T2
- **Agent**: qa-engineer

## Phase 2: Issue 提交 + 存储 (6-10h)

### T4: Issue 存储适配器
- **估时**: 3-5h
- **内容**:
  - Git 原生模式: 写入 `.aria/issues/ISSUE-{timestamp}.md` + git commit
  - API 模式: GitHub/Forgejo Issues API 调用
  - 适配器接口: `createIssue(title, description, priority, type)` → `{id, url}`
  - 配置: `.aria/config.json` → `dashboard.issue_backend`
- **依赖**: T1
- **Agent**: backend-architect

### T5: 看板 Issue 表单
- **估时**: 3-5h
- **内容**:
  - HTML 表单 (标题/描述/优先级/类型)
  - 提交后调用存储适配器
  - 升级为可部署 Web 应用 (轻量 Node.js server 或纯前端 + Git API)
  - 部署指南文档
- **依赖**: T2, T4
- **Agent**: tech-lead

## Phase 3: 心跳 Agent (12-16h)

### T6: aria-heartbeat Skill
- **估时**: 8-10h
- **内容**: 新建 `aria/skills/aria-heartbeat/SKILL.md`
  - Issue 扫描 (Git 模式: .aria/issues/ | API 模式: GitHub/Forgejo)
  - 复杂度分析 (关键词 + 描述 → Level 1/2/3)
  - workflow-runner 全自动调用 (auto_proceed=true)
  - Issue 状态回写 (open → resolved + PR link)
  - 看板数据刷新触发
  - 配置: heartbeat.interval_minutes, max_concurrent_issues
- **依赖**: T4
- **Agent**: tech-lead

### T7: Schedule 集成 + 端到端验证
- **估时**: 4-6h
- **内容**:
  - Claude Code `/schedule` 配置
  - 端到端测试: 创建 issue → 心跳检测 → 自动开发 → PR → 看板刷新
  - 错误恢复: 心跳失败时的重试和告警
  - AB benchmark: aria-heartbeat with/without
- **依赖**: T5, T6
- **Agent**: qa-engineer

## 依赖图

```
T1 (解析器) ──→ T2 (HTML) ──→ T3 (验证)    Phase 1
     │
     └──→ T4 (存储适配器) ──→ T5 (表单)     Phase 2
                │
                └──→ T6 (heartbeat) ──→ T7   Phase 3
```

## 里程碑

| 里程碑 | 完成标志 |
|--------|---------|
| M1 | `/aria:dashboard` 在 Aria + Kairos 上生成正确 HTML |
| M2 | Issue 通过看板提交并存入 `.aria/issues/` |
| M3 | 心跳 Agent 端到端完成 issue→PR 闭环 |

# 决策: DEC-20260402-001 - Aria Dashboard 项目进度看板设计

> **日期**: 2026-04-02 | **模式**: technical
> **Status**: proposed

## 背景

SilkNode 项目实现了一个 progress-dashboard（静态 Next.js 应用），通过构建时解析 Markdown 文件（UPM、OpenSpec、User Stories）生成项目进度可视化页面。该模块的数据源全部来自 Aria 标准格式，具备提炼为 Aria 通用能力的条件。

用户提出更进一步的愿景：看板不仅展示进度，还应支持 issue 提交和 AI 自动开发闭环。

## 约束条件

| 类型 | 约束 | 影响 |
|------|------|------|
| 跨项目通用 | 必须适用于任何 Aria 项目，不绑定 SilkNode | 解析器需泛化 |
| 零依赖 (Phase 1) | 不能要求 npm/Node.js | 单文件 HTML |
| 全自动开发 (Phase 3) | AI 端到端执行无人工确认 | 需要可靠测试覆盖 |
| 心跳触发 | 无人值守定时执行 | 依赖 Claude Code /schedule |

## 考虑的方案

| 决策点 | 选项 | 选择 | 理由 |
|--------|------|------|------|
| 交付形态 | Skill / npm 包 / 内置模板 / 纯规范 | **Skill** | 与 Aria 生态一致，一条命令触发，不引入外部依赖 |
| HTML 格式 | 单文件 / Next.js 应用 | **Phase 1 单文件 → Phase 2 可部署应用** | 渐进增强，Phase 1 零依赖 |
| Issue 存储 | Git 原生 / GitHub API / 两者 | **两者都支持** | Git 原生零依赖，API 适合团队协作 |
| AI 自治度 | 全自动 / 半自动 / 按复杂度 | **全自动** | 用户明确选择最大自治度 |
| 心跳机制 | Hooks / Cron Schedule | **Schedule** | 需要无人值守运行 |
| 增量增强时机 | 后续 Phase / 合并到 Phase 1 | **合并到 Phase 1** | 数据源已存在，同类工作，增量成本小 |

## 最终选择

三阶段交付：Phase 1 完整看板 Skill → Phase 2 Issue 提交 + 存储 → Phase 3 心跳 Agent 全自动开发。

## 理由

1. Phase 1 的数据解析逻辑已在 SilkNode 验证，风险低
2. 单文件 HTML 作为 Skill 输出，与 `/aria:report` 模式一致
3. Issue 双模式存储避免了单一依赖锁定
4. 全自动开发是 Aria 方法论"AI 是协作者"理念的自然延伸
5. 三阶段渐进交付控制了每个阶段的复杂度和风险

## 风险与缓解

| 风险 | 缓解措施 |
|------|----------|
| 全自动开发产生错误代码 | 心跳 Agent 创建 PR 而非直接 push，保留人工 review 机会 |
| 心跳 Agent 失控（无限创建 PR） | max_concurrent_issues=1 限制 + heartbeat.enabled 默认关闭 |
| 单文件 HTML 体积过大 | 数据量大时截断（最近 N 条审计/归档） |
| Claude Code /schedule 不稳定 | Phase 3 作为最后阶段交付，等待 /schedule 成熟 |

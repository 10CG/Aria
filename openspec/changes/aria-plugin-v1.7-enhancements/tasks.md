# Tasks: Aria Plugin v1.7.0 Enhancements

## Phase 1: 配置基础设施 (Issue 3)

- [x] 1.1 设计 .aria/config.json schema + 创建 config.template.json
- [x] 1.2 创建 config-loader Skill (SKILL.md + DEFAULTS.json, user-invocable: false)
- [x] 1.3 集成配置读取到核心 Skills (state-scanner, workflow-runner, tdd-enforcer, branch-finisher, phase-c-integrator, phase-b-developer)
- [x] 1.4 定义 config.json 与 .claude/tdd-config.json 优先级关系
- [x] 1.5 补充 .gitignore (.aria/workflow-state.json, audit.log)
- [ ] 1.6 为每个受影响 Skill 新增 config-driven AB eval case
- [ ] 1.7 AB 测试验证配置加载不影响现有功能

## Phase 2: State Scanner 增强 (Issue 1 + 2, 可并行)

- [x] 2.1 创建 fixtures 目录 (README 版本不一致 + standards 未挂载 + 健康项目)
- [x] 2.2 实现阶段 1.8 README 同步检查 (数据源: CHANGELOG 日期)
- [x] 2.3 实现阶段 1.9 插件依赖检测 (三种状态: 无条目/未初始化/正常)
- [x] 2.4 新增推荐规则: readme_outdated + standards_missing
- [x] 2.5 更新输出格式 (新增 readme_status + standards_status 区块)
- [ ] 2.6 升级 ab-suite 到 v1.1.0 (新增 2 个 state-scanner eval cases)
- [ ] 2.7 AB 测试验证 state-scanner delta 保持正值

## Phase 3: Agent Team 审计 (Issue 4)

- [x] 3.1 创建 agent-team-audit Skill (SKILL.md, experimental: true)
- [x] 3.2 创建 references/ (audit-points.md, agent-selection-matrix.md, verdict-format.md)
- [x] 3.3 实现审计报告输出格式 (PASS/PASS_WITH_WARNINGS/FAIL + 去重算法)
- [x] 3.4 集成到 phase-c-integrator (pre_merge 触发, 读取 config 开关)
- [x] 3.5 集成到 phase-b-developer (post_implementation 触发, 读取 config 开关)
- [x] 3.6 定义 max_parallel_agents 参数 + 超时策略
- [ ] 3.7 创建 defect-detection eval cases (evals.json, 植入已知缺陷)
- [ ] 3.8 AB 测试验证审计效果 (缺陷检出率)

## Phase 4: 集成验证 + 文档同步

- [ ] 4.1 全量 Tier 1 Skills AB 测试 (含 state-scanner v1.1.0 eval suite)
- [ ] 4.2 workflow-runner + phase-c-integrator + phase-b-developer 集成验证
- [x] 4.3 更新 CLAUDE.md (导航 + .aria/ 说明 + 版本号)
- [ ] 4.4 更新 AB_TEST_OPERATIONS.md (实验 Skill 特殊处理章节 + 发版前审计检查项)
- [x] 4.5 更新 aria/CHANGELOG.md (v1.7.0 条目)
- [x] 4.6 版本发布 (v1.7.0, Skills 27→28)

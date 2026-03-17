# Tasks: Benchmark Full Coverage

## Phase 1: Tier A 单轮可测 Skills (16 个)

### 1.1 Phase 编排类 (4 个)

- [ ] 1.1.1 phase-a-planner: 编写 prompt + assertions
- [ ] 1.1.2 phase-b-developer: 编写 prompt + assertions
- [ ] 1.1.3 phase-c-integrator: 编写 prompt + assertions
- [ ] 1.1.4 phase-d-closer: 编写 prompt + assertions

### 1.2 分支与完成类 (2 个)

- [ ] 1.2.1 branch-manager: 编写 2 个 eval (命名 + 模式决策)
- [ ] 1.2.2 branch-finisher: 编写 prompt + assertions

### 1.3 架构文档类 (3 个)

- [ ] 1.3.1 arch-common: 编写 prompt + assertions
- [ ] 1.3.2 arch-scaffolder: 编写 prompt + assertions
- [ ] 1.3.3 arch-update: 编写 prompt + assertions

### 1.4 工作流与路由类 (3 个)

- [ ] 1.4.1 agent-router: 编写 2 个 eval (路由 + 多 Agent)
- [ ] 1.4.2 workflow-runner: 编写 prompt + assertions
- [ ] 1.4.3 progress-updater: 编写 prompt + assertions

### 1.5 质量与文档类 (4 个)

- [ ] 1.5.1 api-doc-generator: 编写 prompt + assertions
- [ ] 1.5.2 requesting-code-review: 编写 prompt + assertions
- [ ] 1.5.3 tdd-enforcer: 编写 prompt + assertions
- [ ] 1.5.4 openspec-archive: 编写 prompt + assertions

## Phase 2: Tier B 需适配 Skills (5 个)

- [ ] 2.1 brainstorm: 单轮降级测试 (首轮问题质量)
- [ ] 2.2 subagent-driver: 任务分解逻辑测试
- [ ] 2.3 forgejo-sync: 同步计划生成测试
- [ ] 2.4 requirements-sync: 漂移检测逻辑测试
- [ ] 2.5 integration-tests: A→B 衔接场景测试

## Phase 3: 集成验证

- [ ] 3.1 合并所有 eval 到 config.json
- [ ] 3.2 执行全量 dry-run 验证配置
- [ ] 3.3 执行首次全量真实运行
- [ ] 3.4 修复失败 eval 的断言
- [ ] 3.5 更新 OVERALL_BENCHMARK_SUMMARY.md

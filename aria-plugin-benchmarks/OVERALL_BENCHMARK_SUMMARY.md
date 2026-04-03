# Aria Plugin Skills Benchmark Summary

> **基线日期**: 2026-03-18 | **测试方法**: AB 对比 (with/without skill) | **覆盖**: 28/28 Skills

---

## AB 测试基线结果

> 通过 `/skill-creator` 方法论，对每个 Skill 执行 with_skill vs without_skill 对比测试。
> 详细运维流程见 [AB_TEST_OPERATIONS.md](AB_TEST_OPERATIONS.md)

### 总览

| 指标 | 值 |
|------|-----|
| Skills 测试 | 28/28 (100% 覆盖) |
| 平均 delta | **+0.55** (Skills 平均提升质量 55%) |
| WITH_BETTER | 19 (68%) |
| MIXED | 1 (4%) |
| EQUAL | 3 (11%) |
| WITHOUT_BETTER | 0 (0%) |
| 已有完整 AB 数据 | 5 (含原始 with/without 对比) |
| 补充 without 数据 | 23 (2026-03-18 agent team 执行) |

### 全量结果 (按 delta 排序)

| Skill | With | Without | Delta | Verdict |
|-------|------|---------|-------|---------|
| phase-d-closer | 1.0 | 0.0 | **+1.00** | WITH_BETTER |
| integration-tests | 1.0 | 0.0 | **+1.00** | WITH_BETTER |
| workflow-runner | 1.0 | 0.1 | **+0.90** | WITH_BETTER |
| openspec-archive | 1.0 | 0.17 | **+0.83** | WITH_BETTER |
| commit-msg-generator | 1.0 | 0.2 | **+0.80** | WITH_BETTER |
| arch-update | 1.0 | 0.2 | **+0.80** | WITH_BETTER |
| arch-scaffolder | 1.0 | 0.2 | **+0.80** | WITH_BETTER |
| arch-common | 1.0 | 0.25 | **+0.75** | WITH_BETTER |
| branch-manager | 1.0 | 0.25 | **+0.75** | WITH_BETTER |
| brainstorm | 1.0 | 0.33 | **+0.67** | WITH_BETTER |
| phase-b-developer | 1.0 | 0.33 | **+0.67** | WITH_BETTER |
| phase-c-integrator | 1.0 | 0.33 | **+0.67** | WITH_BETTER |
| requirements-sync | 1.0 | 0.34 | **+0.67** | WITH_BETTER |
| agent-router | 1.0 | 0.42 | **+0.58** | WITH_BETTER |
| arch-search | 1.0 | 0.53 | **+0.47** | WITH_BETTER |
| branch-finisher | 1.0 | 0.5 | **+0.50** | WITH_BETTER |
| requesting-code-review | 1.0 | 0.5 | **+0.50** | WITH_BETTER |
| requirements-validator | 1.0 | 0.5 | **+0.50** | WITH_BETTER |
| strategic-commit-orch | 1.0 | 0.5 | **+0.50** | WITH_BETTER |
| subagent-driver | 1.0 | 0.5 | **+0.50** | WITH_BETTER |
| tdd-enforcer | 1.0 | 0.5 | **+0.50** | WITH_BETTER |
| progress-updater | 1.0 | 0.63 | **+0.38** | WITH_BETTER |
| task-planner | 1.0 | 0.67 | **+0.33** | WITH_BETTER |
| state-scanner | 1.0 | 0.765 | **+0.235** | WITH_BETTER |
| forgejo-sync | 1.0 | 0.83 | +0.17 | MIXED |
| api-doc-generator | 1.0 | 1.0 | 0.00 | EQUAL |
| phase-a-planner | 1.0 | 1.0 | 0.00 | EQUAL |
| spec-drafter | 1.0 | 1.0 | 0.00 | EQUAL |

### Skill 价值分级

| 分级 | 条件 | Skills | 行动 |
|------|------|--------|------|
| **高价值** | delta >= 0.6 | 13 个 (phase-d, integration, workflow-runner, openspec-archive, commit-msg, arch-*, branch-manager, brainstorm, phase-b/c, requirements-sync) | 重点维护，优先测试 |
| **中价值** | delta 0.3-0.6 | 10 个 (agent-router, arch-search, branch-finisher, requesting-code-review, requirements-validator, strategic-commit-orch, subagent-driver, tdd-enforcer, progress-updater, task-planner) | 正常维护 |
| **低价值** | delta 0.2-0.3 | 1 个 (state-scanner) | 正常维护，custom checks 功能性 EQUAL 拉低 delta |
| **待改进** | delta < 0.2 | 1 个 (forgejo-sync) | 审查是否需要增强 |
| **待审查** | delta = 0 | 3 个 (api-doc-generator, phase-a-planner, spec-drafter) | 评估是否冗余或 eval case 区分度不足 |

---

## 关键发现

### 1. Skill 价值与领域特异性正相关

方法论特定 Skills (十步循环、OpenSpec、工作流编排) delta 最高 (+0.67~1.0)。
这些 Skills 包含 Aria 方法论的专有知识，vanilla Claude 无法推断。

### 2. 通用能力 Skills 无明显优势

api-doc-generator、spec-drafter、phase-a-planner 的 delta = 0。
Sonnet 自身已能处理 API 文档生成、规范起草等通用任务。

### 3. 无负面影响 Skill

WITHOUT_BETTER = 0，说明所有 Skills 至少不会让结果变差。
这是一个重要的安全基线。

### 4. 常见失败模式 (without skill)

- 拒绝处理假设场景 (如不存在的文件路径)
- 缺少 Aria 特定格式 (十步循环步骤、OpenSpec 结构)
- 通用建议替代具体指导 (如 "建议创建分支" vs 给出命名规范)

---

## 文件结构

```
aria-plugin-benchmarks/
├── AB_TEST_OPERATIONS.md           # AB 测试运维手册
├── OVERALL_BENCHMARK_SUMMARY.md    # 本文件
│
├── ab-suite/                       # 固定测试集 (版本化)
│   ├── version.yaml                # v1.0.0, 56 eval cases
│   └── {skill-name}.json          # 每 Skill 2 个核心 case
│
├── ab-results/                     # 历史测试结果
│   ├── 2026-03-13/                # 首次完整基线
│   │   ├── summary.yaml           # 全局总览
│   │   └── {skill}/              # 每 Skill 的详细结果
│   └── latest -> 2026-03-13      # 指向最新运行
│
├── {skill-name}/                   # 原始评估资产 (28 个)
│   ├── evals/evals.json           # 完整 eval cases (178 个)
│   └── iteration-1/              # 首轮 with/without 数据
│
└── runner/                         # 已废弃 (deprecated)
    ├── run_benchmarks.py           # 冻结
    └── config.json                 # 冻结 (7 skills)
```

---

## 下一步

1. ~~建立 AB 测试基线~~ ✅ (28/28 Skills, avg delta +0.53)
2. ~~创建 AB 测试运维手册~~ ✅ (AB_TEST_OPERATIONS.md)
3. ~~建立 ab-suite/ 固定测试集~~ ✅ (56 cases)
4. 审查 3 个 EQUAL Skills (api-doc-generator, phase-a-planner, spec-drafter)
5. 增加多轮运行统计 (方差分析，需多次全量运行)
6. 探索 CI/CD 集成 (当成本可控时)

---

**最后更新**: 2026-04-03
**跨项目对齐**: Aether AB_TEST_OPERATIONS.md v1.0.0

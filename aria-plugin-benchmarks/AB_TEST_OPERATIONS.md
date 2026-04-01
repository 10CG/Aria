# Aria Skill AB 测试运维手册

> **版本**: 1.0.0 | **状态**: Active | **生效日期**: 2026-03-18

---

## 目的

本文档定义了 Aria Plugin Skill 的常态化 AB 测试流程。
所有 Skill 的质量验证通过 **"有 Skill 执行 vs 无 Skill 执行"** 的对比测试完成。
测试结果随时间积累，为优化决策提供数据支撑。

---

## 核心理念

### 为什么用 AB 测试而不是 regex 断言

经过 2026-03-17 的实验验证，得出核心结论：

| 方法 | 实验结果 | 判定 |
|------|---------|------|
| 自研 runner (regex 断言) | 90.6% pass rate → 仅检查关键词存在 | **废弃** (无法证明 Skill 价值) |
| 自研 runner 扩展 28 skills | 花费 ~$11 + 30K tokens → 全部回滚 | **废弃** (浪费资源) |
| /skill-creator AB 对比 | with/without delta 量化真实价值 | **采用** (唯一可信) |

### AB 测试能回答的问题

- 这个 Skill 是否真的让 Agent 表现更好？
- 优化后的 Skill 是否比优化前更好？
- Skill 在哪类任务上有价值、哪类上是负担？

### AB 测试不能回答的问题

- Skill 的 description 是否准确触发 (需要 /skill-creator 的 run_loop.py)
- Skill 在真实项目中的用户满意度 (需要用户反馈数据)

---

## 架构

### 目录结构

```
aria-plugin-benchmarks/
├── AB_TEST_OPERATIONS.md        # 本文档
├── OVERALL_BENCHMARK_SUMMARY.md # 综合报告 (人类可读)
├── benchmark.json               # 全局基准数据
│
├── ab-suite/                    # 固定测试集 (版本化) [已建立]
│   ├── version.yaml             # 测试集版本号
│   └── {skill-name}.json       # 每个 Skill 的 eval cases
│
├── ab-results/                  # 历史测试结果 [已建立]
│   ├── YYYY-MM-DD/             # 每次完整运行
│   │   ├── summary.yaml        # 总览报告
│   │   └── {skill-name}/       # 每个 Skill 的详细结果
│   └── latest -> YYYY-MM-DD    # 指向最新一次完整运行
│
├── {skill-name}/                # 现有资产 (28 个 Skill)
│   ├── evals/evals.json         # eval cases (兼容 /skill-creator)
│   └── iteration-1/            # 首轮 AB 测试结果
│       ├── benchmark.json       # with/without 对比数据
│       └── eval-N/             # 每个 eval 的详细输出
│
└── runner/                      # 已废弃的自研 runner
    ├── run_benchmarks.py        # 冻结，不再使用
    ├── config.json              # 冻结，7 skills
    └── results/                 # 历史数据 (仅参考)
```

### 现有资产盘点

| 资产 | 数量 | 状态 |
|------|------|------|
| Skill eval suites | 28 个 | ✅ 全量覆盖 |
| 总 eval cases | 178 个 | ✅ 已编写 |
| iteration-1 结果 | 28 个 | ✅ 含 with/without 对比 |
| 自研 runner 运行结果 | 10 组 | ❄️ 冻结，仅参考 |

### 固定测试集 vs 临时测试

| 类型 | 存储位置 | 用途 | 规则 |
|------|---------|------|------|
| 固定测试集 | `ab-suite/` | 常态化比对 | 修改需升版本号，旧数据不可比 |
| 现有 evals | `{skill}/evals/evals.json` | 首轮基线 | 可迁移到 ab-suite |
| 临时测试 | `{skill}/{skill}-workspace/` | 开发中验证 | 随时可改，不计入基线 |

---

## Eval Case 编写规范

### 格式 (兼容 /skill-creator)

```json
{
  "skill_name": "commit-msg-generator",
  "version": "1.0.0",
  "evals": [
    {
      "id": 1,
      "name": "standard-feat-commit",
      "prompt": "50+ 字的真实复杂任务描述...",
      "expected_output": "预期结果的文字描述",
      "expectations": [
        "可验证的断言1 (测试 Skill 的关键价值点)",
        "可验证的断言2"
      ]
    }
  ]
}
```

### 每个 Skill 建议 2-5 个 Eval Cases

| 类型 | 目的 | 示例 |
|------|------|------|
| 标准场景 | 验证 Skill 在典型任务中的价值 | commit-msg: 单文件 feat 提交 |
| 复杂场景 | 验证 Skill 在多步骤/跨模块任务中的表现 | commit-msg: 跨模块分组提交 |
| 边缘场景 | 验证 Skill 对异常输入的处理 | commit-msg: 空 diff / 二进制文件 |

### Prompt 编写原则

**必须**:
- 50 字以上，包含完整上下文
- 描述具体的项目场景 (不是一句话指令)
- 用中文或英文均可 (匹配 Skill 的目标语言)
- 包含足够信息让 without_skill 也能尝试执行

**示例 (好)**:
```
我在 todo-web 项目中新增了用户认证功能，修改了 backend/src/routes/auth.py (新增)
和 backend/src/app.py (修改)，添加了 JWT 认证的 login 和 register 端点。
请为这些暂存的变更生成符合 Conventional Commits 规范的提交消息。
```

**示例 (差)**:
```
生成 commit message
```

### Expectations 编写原则

**必须测试 Skill 的关键价值点**，不是通用能力:

| 好的 Expectation | 差的 Expectation |
|-----------------|-----------------|
| "commit 类型正确识别为 feat" | "输出包含文字" |
| "scope 准确匹配 auth 模块" | "使用了工具" |
| "推荐的工作流包含 Phase A-D 步骤" | "输出有格式" |
| "架构搜索结果指向正确的文件路径" | "执行了命令" |

**判断标准**: 如果 without_skill 也能轻松通过这个 expectation，那它没有区分度，应该替换。

### 版本管理

```yaml
# ab-suite/version.yaml
version: "1.0.0"
created: "2026-03-18"
last_modified: "2026-03-18"
skills_covered: 28
total_eval_cases: 178
changelog:
  - version: "1.0.0"
    date: "2026-03-18"
    changes: "从 {skill}/evals/evals.json 迁移，建立固定测试集"
```

**修改 eval case 的规则**:
1. 修改任何 eval case → 升 MINOR 版本 (1.0.0 → 1.1.0)
2. 新版本的结果与旧版本 **不可直接比较**
3. 需在 summary.yaml 中标注 `eval_suite_version` 以追溯

---

## 执行流程

### 场景 1: Skill 优化后验证 (最常用)

```
/skill-creator benchmark <skill-name>

流程:
  1. 读取 {skill}/evals/evals.json (或 ab-suite/{skill}.json)
  2. 并行 spawn 2 个 subagent:
     - with_skill: 加载 SKILL.md 后执行任务
     - without_skill: 不加载任何 skill 直接执行
  3. grader agent 逐项评分 (AI 语义级)
  4. aggregate_benchmark.py → benchmark.json + benchmark.md
  5. generate_review.py → HTML 可视化
  6. 人类审阅 + 提交 feedback

产出: {skill}/{skill}-workspace/iteration-N/
验收: delta.pass_rate > 0 (Skill 确实提升了质量)
```

### 场景 2: 新增 Skill 首次基线

```
/skill-creator (创建新 Skill 流程自带 benchmark)

流程:
  1. /skill-creator 引导编写 SKILL.md
  2. 编写 evals.json (2-5 个 eval cases)
  3. 执行 with/without AB 测试
  4. 生成 iteration-1/ 基线数据
  5. 审阅并确认 Skill 有正向 delta

产出: {new-skill}/evals/ + {new-skill}/iteration-1/
```

### 场景 3: 发版前全量回归

```
逐 Skill 执行 /skill-creator benchmark

流程:
  1. 按优先级分批执行 (Tier 1 → 2 → 3)
  2. 每个 Skill 生成新的 iteration-N/ 数据
  3. 与上一次结果比对:
     - 哪些 Skill 变好了 (delta 上升)
     - 哪些 Skill 变差了 (delta 下降)
     - 哪些持平
  4. 汇总到 ab-results/YYYY-MM-DD/summary.yaml
  5. 更新 latest symlink

预估: 28 Skills × ~$0.50/Skill ≈ $14, ~6-8 hours
```

### 场景 4: Description 触发准确率优化

```
/skill-creator (description 优化流程)

流程:
  1. 编写 trigger-eval.json (20 queries, 混合 should/should-not trigger)
  2. run_loop.py 自动迭代优化 description
  3. 输出 best_description + HTML 报告

触发时机: 修改 Skill 的 description/frontmatter 后
```

---

## 执行细节

### /skill-creator 内部机制

| 组件 | 职责 | 路径 |
|------|------|------|
| grader agent | AI 语义级评分 | agents/grader.md |
| comparator agent | 盲测对比 (可选) | agents/comparator.md |
| analyzer agent | 模式分析 + 改进建议 | agents/analyzer.md |
| aggregate_benchmark.py | 统计聚合 | scripts/aggregate_benchmark.py |
| generate_review.py | HTML 可视化 | eval-viewer/generate_review.py |
| run_loop.py | Description 优化 | scripts/run_loop.py |

### 并发控制

| 参数 | 推荐值 | 理由 |
|------|--------|------|
| 每波 Skill 数 | 1-2 | 2-4 个 subagent 并行，避免 529 |
| 波次间隔 | 30s | 让 API 限流窗口重置 |
| Grading 并行 | 3 | Grader 较轻量 |
| 单 subagent 超时 | 5 min | 允许充分执行 |

### Timing 数据捕获

**关键**: Task notification 中的 `total_tokens` 和 `duration_ms` 是唯一的获取时机。
必须在收到通知时立即保存，事后无法恢复。

```json
{
  "with_skill": {
    "total_tokens": 1834,
    "duration_ms": 10446
  },
  "without_skill": {
    "total_tokens": 856,
    "duration_ms": 3053
  }
}
```

---

## 结果格式

### summary.yaml (每次全量运行的总览)

```yaml
date: "2026-03-18"
eval_suite_version: "1.0.0"
skills_tested: 28
total_eval_cases: 56  # 每 Skill 2 个核心 case
total_subagent_runs: 112

results:
  commit-msg-generator:
    eval_count: 2
    with_skill_pass_rate: 1.0
    without_skill_pass_rate: 0.2
    delta_pass_rate: +0.8
    blind_winner: ["WITH", "WITH"]
    with_skill_win_rate: 1.0
    avg_tokens_with: 1834
    avg_tokens_without: 856
    verdict: "WITH_BETTER"

  arch-search:
    eval_count: 2
    with_skill_pass_rate: 1.0
    without_skill_pass_rate: 0.53
    delta_pass_rate: +0.47
    avg_tokens_with: 450
    avg_tokens_without: 1800
    token_savings: "75%"
    verdict: "WITH_BETTER"

  # ... 其余 Skills

overall:
  total_with_wins: 0
  total_without_wins: 0
  total_ties: 0
  with_skill_win_rate: 0.0
  avg_delta_pass_rate: 0.0
  key_findings:
    - "待首次全量运行后填充"
```

### Verdict 标准

| Verdict | 条件 | 行动 |
|---------|------|------|
| **WITH_BETTER** | with 胜率 > 70% | ✅ Skill 有价值，保留 |
| **MIXED** | with 胜率 40-70% | ⚠️ 需要分析哪类场景有价值 |
| **EQUAL** | delta < 5% 或全部 TIE | ⚠️ Skill 可能冗余，考虑精简 |
| **WITHOUT_BETTER** | without 胜率 > 50% | ❌ Skill 有负面影响，必须修复或移除 |

### 历次运行比对

```yaml
# 自动生成的比对报告
comparison:
  current: "2026-04-01"
  previous: "2026-03-18"
  eval_suite_version_match: true

  changes:
    improved:
      - skill: "state-scanner"
        before: "MIXED (0.5 win rate)"
        after: "WITH_BETTER (1.0 win rate)"
        reason: "优化推荐引擎后准确率提升"

    regressed:
      - skill: "brainstorm"
        before: "WITH_BETTER (1.0)"
        after: "MIXED (0.5)"
        reason: "重构后首轮提问质量下降"

    stable:
      - skill: "commit-msg-generator"
        status: "WITH_BETTER (1.0) → WITH_BETTER (1.0)"
```

---

## Skill 分类与测试优先级

### Tier 1: 核心 Skills (10 个, 每次发版必测)

| Skill | 现有 Evals | 首轮 Delta | 优先级 |
|-------|-----------|-----------|--------|
| commit-msg-generator | 15 | with:100% vs without:20% (+80%) | P0 |
| arch-search | 15 | with:100% vs without:53% (+47%) | P0 |
| state-scanner | 8 | with:100% | P0 |
| branch-manager | 10 | with:100% | P0 |
| task-planner | 10 | with:100% | P0 |
| spec-drafter | 5 | with:100% | P0 |
| strategic-commit-orchestrator | 5 | with:100% | P0 |
| requirements-validator | 5 | with:100% | P0 |
| workflow-runner | 5 | with:100% | P0 |
| agent-router | 5 | with:100% | P0 |

### Tier 2: 辅助 Skills (11 个, 相关 Skill 修改时测)

| Skill | 现有 Evals | 说明 |
|-------|-----------|------|
| arch-update | 5 | arch 系列修改时测 |
| arch-scaffolder | 5 | arch 系列修改时测 |
| arch-common | 4 | arch 系列修改时测 |
| openspec-archive | 4 | openspec 流程修改时测 |
| progress-updater | 5 | 进度管理修改时测 |
| requesting-code-review | 4 | 审查流程修改时测 |
| tdd-enforcer | 5 | TDD 流程修改时测 |
| api-doc-generator | 5 | 文档生成修改时测 |
| branch-finisher | 4 | 分支管理修改时测 |
| brainstorm | 5 | 头脑风暴修改时测 |
| forgejo-sync | 4 | 同步流程修改时测 |

### Tier 3: 编排/集成 Skills (7 个, 架构变更时测)

| Skill | 现有 Evals | 说明 |
|-------|-----------|------|
| phase-a-planner | 5 | Phase 编排修改时测 |
| phase-b-developer | 5 | Phase 编排修改时测 |
| phase-c-integrator | 5 | Phase 编排修改时测 |
| phase-d-closer | 5 | Phase 编排修改时测 |
| subagent-driver | 5 | 子代理机制修改时测 |
| requirements-sync | 5 | 需求同步修改时测 |
| integration-tests | 6 | 跨 Skill 集成修改时测 |

---

## 特殊处理

### Hook 型 Skill (如 tdd-enforcer 的 PreToolUse 模式)

Hook 不执行用户任务，而是在工具调用前/后拦截和验证。
AB 测试的 "with/without skill 执行任务" 方法需要适配：

**测试方案**:
1. 模拟需要 TDD 验证的开发场景
2. with_skill: 验证 Hook 是否正确拦截非 TDD 操作
3. without_skill: 验证无 Hook 时是否跳过 TDD 检查
4. Expectation: "在未写测试时阻止代码写入" (区分度高)

### 编排型 Skill (phase-a/b/c/d, workflow-runner)

编排型 Skill 调用其他 Skill，直接执行可能触发链式调用。

**测试方案**:
1. Prompt 要求"分析和规划"而非"执行"
2. 测试编排的**决策质量**而非执行结果
3. Expectation: "识别正确的 Phase 步骤" / "推荐合理的执行顺序"

---

## 数据积累策略

### 短期 (1-3 个月)

- 每次 Skill 优化后跑单 Skill AB 测试 (场景 1)
- 每次发版前跑 Tier 1 全量 AB 测试 (场景 3)
- 积累 3-5 次全量运行数据
- 从现有 iteration-1/ 数据建立基线

### 中期 (3-6 个月)

- 建立趋势图：每个 Skill 的 WITH 胜率随时间的变化
- 识别模式：哪类修改提升了 AB 表现，哪类降低了
- 优化 eval cases：基于实际使用模式更新测试集 (升版本号)
- 迁移 `{skill}/evals/evals.json` 到 `ab-suite/` 统一管理

### 长期 (6+ 个月)

- 建立 Skill 价值分级：
  - **高价值**: WITH 胜率 > 80%，delta > 30%
  - **中价值**: WITH 胜率 50-80%
  - **低价值/负价值**: WITH 胜率 < 50%
- 对低价值 Skill 考虑精简或合并
- 探索 CI/CD 集成 (当成本可控时)

---

## 与其他项目的对齐

### Aether 实践借鉴

| Aether 实践 | Aria 对应 | 状态 |
|-------------|----------|------|
| `evals/ab-suite/` 固定测试集 | `ab-suite/` | ✅ 已建立 (28 skills, 56 cases) |
| `evals/ab-results/YYYY-MM-DD/` | `ab-results/` | ✅ 已建立 (2026-03-13 基线) |
| `summary.yaml` 标准格式 | 同格式 | ✅ 已建立 |
| `version.yaml` 测试集版本 | 同机制 | ✅ 已建立 (v1.0.0) |
| `/skill-benchmark` 编排 Skill | 使用 `/skill-creator` | ✅ 已确定 |
| 4 轮实验验证 (评分→grep→触发→AB) | 1 轮教训 (regex runner → 废弃) | ✅ 已完成 |

### 跨项目统一规范

建议所有使用 Aria 方法论的项目遵循：

1. **测试工具**: `/skill-creator` (官方标准)
2. **测试方法**: with/without AB 对比 (唯一可信方式)
3. **结果格式**: summary.yaml + verdict 标准 (跨项目可比)
4. **版本管理**: eval case 修改必须升版本号
5. **门卡机制**: 无 benchmark 数据的 Skill 变更不合并

---

## 检查清单

### Skill 优化后
- [ ] `/skill-creator benchmark` 已执行
- [ ] benchmark.json 中 delta.pass_rate > 0
- [ ] 人类已审阅输出或 HTML 报告
- [ ] 结果已存入对应 iteration-N/ 目录

### 新增 Skill 后
- [ ] evals.json 已编写 (至少 2 个 eval cases)
- [ ] `/skill-creator` 创建流程已含 benchmark
- [ ] iteration-1/ 基线数据已生成
- [ ] with_skill 表现优于 without_skill

### 发版前
- [ ] Tier 1 Skills 全量 AB 测试已执行
- [ ] summary.yaml 已生成并审查
- [ ] 无 WITHOUT_BETTER verdict 的 Skill (否则必须修复)
- [ ] 与上一次结果比对，无回归

### 修改 eval case 前
- [ ] 确认需要修改 (不可随意改动)
- [ ] version.yaml 版本号已递增
- [ ] changelog 中记录修改原因
- [ ] 理解: 修改后旧数据不可直接比较

---

## 迁移计划 (现有资产 → 标准化结构)

### Phase 1: 确认现有数据有效性

```
现有: {skill}/evals/evals.json (28 个, 178 eval cases)
现有: {skill}/iteration-1/benchmark.json (28 个, 含 with/without)
行动: 逐个审查 benchmark.json 中 without_skill 数据是否完整
```

### Phase 2: 建立 ab-suite/ (固定测试集)

```
从每个 Skill 的 evals.json 中选取 2 个核心 case
建立 ab-suite/{skill}.json
创建 version.yaml
```

### Phase 3: 建立 ab-results/ (结果存档)

```
将 iteration-1/ 数据迁移为 ab-results/2026-03-13/ (首次基线)
创建 summary.yaml
建立 latest symlink
```

---

## 与其他文档的关系

| 文档 | 职责 |
|------|------|
| **本文档** (AB_TEST_OPERATIONS.md) | AB 测试的执行流程、格式、策略 |
| CLAUDE.md 规则 #6 | 项目级强制规范 (必须用 /skill-creator) |
| CLAUDE.md 操作指南 | AI 助手的操作参考 |
| CLAUDE.md 版本发布检查清单 | 发版门卡 (benchmark 项必须勾选) |
| OVERALL_BENCHMARK_SUMMARY.md | 综合报告 (人类可读, 含历史数据) |
| CROSS_PROJECT_BENCHMARKING.md | 跨项目 benchmark 指南 (外部项目适配) |

---

**维护者**: 10CG Lab
**审查周期**: 每季度 (与版本发布同步)
**跨项目对齐**: 参考 Aether AB_TEST_OPERATIONS.md v1.0.0

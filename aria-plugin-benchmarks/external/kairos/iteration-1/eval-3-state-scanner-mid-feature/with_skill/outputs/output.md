╔══════════════════════════════════════════════════════════════╗
║                    PROJECT STATE ANALYSIS                     ║
╚══════════════════════════════════════════════════════════════╝

📍 当前状态
───────────────────────────────────────────────────────────────
  项目: Kairos (AI Sales Automation)
  分支: feat/multi-provider-failover
  Phase/Cycle: (UPM 未检测到 — 项目未安装 aria-plugin)
  变更: 5 文件未暂存, 0 文件已暂存
  OpenSpec: multi-provider-failover (Proposed)

📊 变更分析
───────────────────────────────────────────────────────────────
  变更文件:
    代码 (3):
      - src/core/llm/providers/kimi.ts
      - src/core/llm/providers/doubao.ts
      - src/core/llm/providers/config.ts
    测试 (2):
      - (2 个测试文件, 推测对应 kimi/doubao provider)
  类型: 功能代码 + 测试
  复杂度: Level 2
    - 5 文件变更, 涉及 LLM provider 层核心模块
    - 新增/修改多 provider failover 逻辑
    - 可能影响现有 provider 调用链路
  架构影响: 可能 — LLM provider 层是核心基础设施
  测试覆盖: ✅ 有对应测试文件 (2/3 代码文件有匹配测试)

📄 需求状态
───────────────────────────────────────────────────────────────
  配置状态: 需人工确认 (项目使用 OpenSpec + UPM, 但未安装 aria-plugin)
  建议操作:
    - 检查 docs/requirements/ 是否存在
    - 如已有 PRD/User Stories, 可通过安装 aria-plugin 获得完整追踪

🏗️ 架构状态
───────────────────────────────────────────────────────────────
  System Architecture: 需人工确认
  期望路径: docs/architecture/system-architecture.md
  注意: LLM provider failover 属于核心架构变更,
        如果存在架构文档, 建议同步更新 provider 层的设计说明

📋 OpenSpec 状态
───────────────────────────────────────────────────────────────
  配置状态: ✅ 已配置 (项目使用 OpenSpec)
  活跃变更: 1 个
    - multi-provider-failover (Status: Proposed)
      路径: openspec/changes/multi-provider-failover/proposal.md
  待归档: 0 个

  ⚠️ 注意: Spec 状态为 Proposed, 尚未经过 Review/Approve
     当前已有 5 文件修改, 开发先于 Spec 审批

📝 README 同步状态
───────────────────────────────────────────────────────────────
  (跳过 — 无版本文件变更, 非发版场景)

📦 插件依赖状态
───────────────────────────────────────────────────────────────
  aria-plugin: ❌ 未安装
  提示: Kairos 项目未安装 aria-plugin, 工作流自动化功能受限
  建议: 如需完整十步循环支持, 可安装 aria-plugin

🔬 Skill 变更 AB 状态
───────────────────────────────────────────────────────────────
  (不适用 — 无 SKILL.md 变更)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ 状态诊断
───────────────────────────────────────────────────────────────
  检测到以下需要关注的问题:

  1. **OpenSpec 状态滞后**: Spec 状态仍为 Proposed, 但已有 5 文件代码修改。
     按照 Aria 方法论, 应先 Review/Approve Spec, 再进入开发。
     当前属于"开发先行"状态, 存在返工风险。

  2. **全部变更未暂存**: 5 个文件修改均未暂存 (unstaged), 无已暂存文件。
     需要在开发完成后暂存并提交。

  3. **架构影响待评估**: multi-provider-failover 涉及 LLM provider 核心层,
     如果项目有架构文档, failover 策略、重试逻辑、provider 优先级配置
     等设计决策应记录在架构文档中。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 推荐工作流
───────────────────────────────────────────────────────────────

  ➤ [1] spec-first-then-dev (推荐) — 置信度 85%
      步骤:
        1. 将 proposal.md 状态从 Proposed 推进到 Reviewed → Approved
           (确认 failover 策略、provider 优先级、降级逻辑等设计决策)
        2. 完成剩余开发 + 测试 (B.2)
        3. 暂存变更 → 提交 (C.1)
        4. 创建 PR → 合并 (C.2)
      理由: Spec 仍为 Proposed, 先确认设计方案可避免返工。
            已有代码变更可作为 Spec Review 的参考实现。

  ○ [2] continue-dev — 置信度 70%
      步骤:
        1. 继续完成 failover 功能开发 (B.2)
        2. 运行完整测试套件验证 (1434 tests)
        3. 暂存 + 提交 (C.1)
        4. 更新 Spec 状态为 In Progress / Complete
      理由: 如果 Spec 内容已在团队内部口头确认,
            可先完成开发再补充 Spec 状态

  ○ [3] review-and-test — 置信度 65%
      步骤:
        1. 先运行现有测试确保无回归
        2. 代码自审 (Review 5 个变更文件)
        3. 根据审查结果决定是否继续或调整方案
      理由: 已有修改但不确定方向时, 先验证现有变更质量

  ○ [4] 自定义组合
      输入格式: "B.2 + C.1" 或任意步骤组合

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 额外建议
───────────────────────────────────────────────────────────────

  1. **Spec Review 重点关注项** (multi-provider-failover):
     - failover 策略: 是轮询、优先级降级还是并发竞速?
     - 超时配置: kimi/doubao 各自的超时阈值?
     - 错误分类: 哪些错误触发 failover (网络/限流/模型错误)?
     - 配置热更新: config.ts 变更是否支持运行时更新?
     - 可观测性: failover 事件是否有日志/指标上报?

  2. **测试建议**:
     - 确保 failover 场景有集成测试 (模拟 provider 故障)
     - 验证 provider 配置变更不影响现有 1434 个测试
     - 考虑添加 provider 健康检查的 mock 测试

  3. **部署注意** (Forgejo Actions + Nomad):
     - 新增 provider (kimi/doubao) 可能需要新的环境变量/密钥
     - 确认 Nomad job 配置中包含新 provider 的 API credentials
     - 建议先在 dev 环境验证 failover 行为

🤔 选择 [1-4] 或输入自定义:

# Aria 2.0 - 产品需求文档 (PRD)

> **Version**: 2.0.0
> **Status**: Approved (Draft → Approved 2026-04-11, 讨论组+挑战组 4 轮收敛)
> **Created**: 2026-04-09
> **Owner**: 10CG Lab
> **Supersedes**: [prd-aria-v1.md](./prd-aria-v1.md) (v1.x 保持维护, v2.0 是并行升级)

---

## 文档目的

本 PRD 定义 **Aria 2.0** 的产品形态、架构、范围和成功标准。Aria 2.0 是从 v1.x "AI 辅助人" 到 **"AI 自主开发"** 的演进升级，通过 **两层 AI 分工架构** 把 aria-plugin 的开发能力从交互模式迁移到无人值守模式。

**重要**: Aria 2.0 是 **升级** 不是重构。v1.x 的核心资产 (standards/, aria-plugin) 保持不变, v2.0 新增运行时层 (aria-orchestrator) 实现自主开发闭环。

**来源**: 5 轮 Agent Team 收敛讨论 (讨论组 4 + 挑战组 3), 产品负责人 10CG Lab 确认愿景。

---

## 产品定位

### 核心定位

> **Aria 2.0 是 AI-AI 分工协作的自主软件工程方法论, 由 Layer 1 AI 主管 (Hermes) 指挥 Layer 2 AI 工程师 (CC 容器) 完成端到端开发的参考实现。**

### 身份演进

| 版本 | 项目本质 | 协作模式 |
|------|---------|---------|
| v1.x | AI 辅助的领域驱动设计方法论研究 | AI 理解 → **人类确认** → 协作交付 |
| v2.0 | AI 自主软件工程的方法论定义与端到端参考实现 | AI 主管规划 → AI 工程师执行 → **人类审批关键节点** |

### 核心论断

产品负责人的核心论断:
> "aria-plugin 已经具备非常好的驾驭 LLM 开发的能力, 需要从用户和 AI 共同开发, 升级到 AI 自主开发。这是 '控制 CC' 的意义。"

**方法论自我验证**: aria-plugin v1.10.0 本身就是用 Aria 方法论 + 人机协作模式开发的, 已被 AB benchmark 验证 (28 skills, avg delta +0.53)。Aria 2.0 不是重新发明能力, 而是 **把已验证的能力迁移到无人值守环境**。

### 目标用户

**主要用户**: 10CG Lab 自身 (非产品, 非 SaaS, 不面向第三方)

| 角色 | 使用方式 |
|------|---------|
| 10CG 工程师 | 交互式使用 aria-plugin (v1.x 模式保留) + 监督 Aria 2.0 自主开发结果 |
| 10CG Lab (组织) | 用 Aria 2.0 加速 Aria 自身演进 + 其他内部项目的自动开发 |
| AI 研究 | 验证"AI-AI 分工协作"假设, 产出方法论洞察 |

### 核心价值主张

```
v1.x 价值:     方法论使开发过程可重现 (人类 + AI 一致性)
v2.0 新增:     方法论使开发结果可无人值守 (AI-AI 一致性)

v1.x 成本:     人类驾驭 AI 的时间投入
v2.0 新增:     人类只在关键节点审批 (Spec 创建, PR 合并)
```

### 成功标准

**M1 MVP (手动 E2E)**:
- [ ] 1 个 DEMO issue 从扫描到 Draft PR 全程无人类介入 (手动触发 1 次 dispatch)
- [ ] Layer 2 容器内完整加载 aria-plugin + 执行十步循环
- [ ] 产出的 PR 通过人类 review

**M6 v2.0 发版**:
- [ ] 连续 7 天 24/7 无人值守运行
- [ ] 至少 10 个真实 issue 通过自主 dispatch 成功合并
- [ ] Hermes Layer 1 成本 < $10/月, Layer 2 成本 < $70/月
- [ ] 状态机 transition 100% 单元测试覆盖
- [ ] Crash recovery 在 3 种故障模式下验证通过
- [ ] 审计日志完整, 任一 dispatch 可回溯决策路径

**方法论研究交付**:
- [ ] 产出"AI-AI 分工协作"的方法论文档 (standards/autonomous/)
- [ ] 产出"拟人命令 (humanized command)"的 prompt engineering 模式
- [ ] 量化数据: v2.0 自主 dispatch 的成功率 / 漂移率 / 成本 / 人类审批时间

---

## 架构总览

### 三层架构 (v2.0 扩展)

```
方法论层  standards/          ← 思考/协作/决策规范 (v1.x 不变)
工具层    aria-plugin (+ CC)  ← 交互式使用 (不变) + Layer 2 容器内嵌
运行时层  aria-orchestrator:
          ├── Layer 1: Hermes fork (GLM 5.1, 扮演 AI 主管)
          └── Layer 2: 容器镜像 (预装 CC + aria-plugin, 扮演 AI 工程师)
```

### 两层 AI 分工

```
┌──────────────────────────────────────────────────────────────┐
│  Layer 1: Hermes fork (AI 主管)                              │
│  ─────────────────────────────────────────────────────────── │
│  位置:   Aether light 节点, raw_exec                          │
│  LLM:    GLM 5.1 (fallback: GLM-4.5-Air)                     │
│  元知识: ~1K token prompt (高层 Aria 方法论)                  │
│  职责:                                                        │
│    - 读 heartbeat scan, triage issue                         │
│    - 决定派发哪个 issue                                       │
│    - 生成"拟人命令" (自然语言任务描述)                         │
│    - 启动 Layer 2 容器 (via Nomad parameterized dispatch)    │
│    - Poll 容器状态 (跨 cron tick)                             │
│    - 评审结果, 决定 merge / retry / escalate                 │
│    - Feishu 人类审批 gate                                    │
│  **不做**: 不调用 aria-plugin, 不折叠 Skills, 不写代码         │
└──────────────────────────────────────────────────────────────┘
                          │
                          │ 拟人命令 (自然语言)
                          ▼
┌──────────────────────────────────────────────────────────────┐
│  Layer 2: aria-runner 容器 (AI 工程师)                        │
│  ─────────────────────────────────────────────────────────── │
│  位置:   Aether heavy 节点, Nomad docker driver              │
│  镜像:   2 个预装容器                                         │
│    ├── aria-runner:claude-latest                             │
│    │   (claude code + aria-plugin + 支持 Anthropic/GLM 切换) │
│    └── aria-runner:crush-latest                              │
│        (Crush + GLM, 降级备选, 无 aria-plugin)                │
│  职责:                                                        │
│    - 接收 Layer 1 的拟人命令                                  │
│    - 在 git worktree 里工作                                   │
│    - 运行 `claude -p` 执行十步循环 (完整 aria-plugin)         │
│    - 提交到 feature branch + 创建 PR                         │
│    - 输出 result.json                                        │
│  **无 Aria 感知**: 不需要懂方法论, 只需能执行 prompt          │
└──────────────────────────────────────────────────────────────┘
```

### 关键架构决策 (Agent Team 5 轮收敛)

| ID | 决策 | 理由 |
|----|------|------|
| **AD1** | 两层 AI 分工 (Hermes 主管 + 容器工程师) | 继承 aria-plugin 已验证能力, 不重新实现方法论 |
| **AD2** | Layer 2 容器预装 aria-plugin (build-time) | 解决 headless Plugin 加载 P0 问题 |
| **AD3** | Hermes fork (非 Python extension) | hermes-agent 0.7 不支持 Python 扩展 API, fork 是唯一路径 |
| **AD4** | Nomad Parameterized Batch Job 启动容器 | 原生支持, 利用 Aether 现有基础设施, 不需新部署工具 |
| **AD5** | 状态机 9 states + S_FAIL 兜底 | QA 建议 (R2→R3), 平衡精细与简单 |
| **AD6** | 拟人命令协议 (非结构化 RPC) | 产品负责人明确表述, AI-AI 协作更自然, 符合 GSD 2 模式 |
| **AD7** | ~1K token 元知识 (非 frontmatter 提取) | Layer 2 加载完整 aria-plugin, Layer 1 只需高层认知 |
| **AD8** | 拒绝多 provider 抽象 (只做 claude + crush 2 镜像) | YAGNI, claude-anthropic/glm 用 env 切换 |
| **AD9** | 跨 tick polling (容器可跨多 cron tick 运行) | Nomad alloc 持久, Hermes cron 60min tick 不阻塞 Layer 2 |
| **AD10** | 1 human gate (S7 review+merge 合并) | 简化 (从 R2 2 gate), 依赖 LLM review 在 S6 兜底 |
| **AD11** | CLAUDE.md 不动硬约束 (分层叙述) | 保护方法论权威性, 新增 "Aria 2.0 运行时" 章节说明边界 |
| **AD12** | aria-orchestrator 不剥离 (前次讨论结论反转) | 两层架构是 Aria 方法论的核心部分, 不是 "运维产物" |

---

## 功能范围

### Must-have (v2.0 核心)

#### 1. Layer 1 状态机 (9 states + S_FAIL)

```yaml
状态机:
  S0_IDLE:         cron 等待 (60min tick)
  S1_SCAN:         heartbeat + triage (确定性规则, 不调 LLM)
  S2_DECIDE:       [LLM] 是否派发 + 目标 issue 选择
  S3_BUILD_CMD:    [LLM] 生成拟人命令
  S4_LAUNCH:       Nomad parameterized dispatch, 记录 alloc_id 到 SQLite
  S5_AWAIT:        跨 tick polling (可持续多个 cron tick)
  S6_REVIEW:       [LLM] 评审 Layer 2 结果 (代码质量 + 越界检查 + acceptance)
  S7_HUMAN_GATE:   Feishu 审批卡片 (唯一人类介入点)
  S8_MERGE:        确定性 git merge + Forgejo API
  S9_CLOSE:        归档 (OpenSpec archive + CHANGELOG + 清理)
  S_FAIL:          兜底错误状态 (任何 state 抛异常进入)
```

**持久化**:
- 每个 state transition 写 `.aria/state/history/{trace_id}/{state}_{timestamp}.json`
- 活跃状态: `.aria/state/active/{trace_id}.json` (atomic write via temp+rename)
- Active dispatches 表: SQLite `dispatches.db` (WAL mode, 持久化 volume)

**Crash recovery**: 启动时扫 `active/*.json`, 对每个未完成 trace 按幂等规则重入。

#### 2. Layer 2 容器镜像

**aria-runner:claude-latest** (主力镜像):

```dockerfile
FROM node:20-bookworm-slim

# 预装 claude code CLI
RUN npm install -g @anthropic-ai/claude-code@latest

# 预装 aria-plugin (build-time)
COPY aria-plugin/ /opt/aria-plugin/
RUN mkdir -p /root/.claude/plugins && \
    ln -s /opt/aria-plugin /root/.claude/plugins/aria && \
    echo '{"plugins": [{"path": "/opt/aria-plugin"}]}' > /root/.claude/settings.json

# 预装工具
RUN apt-get update && apt-get install -y git jq curl && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
```

**支持的后端** (通过 env 切换):
- `ANTHROPIC_API_KEY=<key>` → 直连 Anthropic API (默认)
- `ANTHROPIC_API_KEY=<glm_key>` + `ANTHROPIC_BASE_URL=https://api.luxeno.ai` → GLM 代理

**aria-runner:crush-latest** (降级备选, M5 添加):

```dockerfile
FROM ghcr.io/charmbracelet/crush:latest
# 不预装 aria-plugin (Crush 不支持 Claude Code plugin 格式)
# 通过 system prompt 注入 Aria 方法论摘要
```

#### 3. 拟人命令协议

**命令结构** (YAML):

```yaml
task_id: issue-{id}
title: <short title>
priority: p0|p1|p2
budget_tokens: 60000
budget_minutes: 30

prompt: |
  <自然语言任务描述, 像人类 PM 给工程师下任务>
  <包含: 问题背景、具体要求、上下文提示、注意事项>

constraints:
  must_not_touch: [<paths>]
  must_follow_spec: <openspec/changes/path>

acceptance:
  - <criterion 1>
  - <criterion 2>

output_format: result.json
```

**关键**: prompt 字段是 **自然语言**, 不是结构化指令。Layer 1 用 GLM 5.1 基于 issue 生成, 风格要像"人类 PM 写的 Jira ticket"。

#### 4. Hermes fork + 元知识

**Hermes fork 管理**:
- 位置: `forgejo.10cg.pub/10CG/hermes-agent`
- 基于: NousResearch/hermes-agent v0.7+
- 扩展: fork 内新增 `internal/aria/` 目录 (Layer 1 状态机 + launcher + dispatcher)
- 同步: 月度 rebase from upstream (估 12-20h/月, 前 3 月)
- License: MIT (upstream), 10CG 修改保持 MIT

**元知识** (~1K token, 注入到 Hermes system prompt):

```
你是 Hermes — Aria 项目的 AI 主管。

你不写代码。你把 GitHub Issues 翻译成清晰的拟人任务, 
派发给 Layer 2 的开发容器 (容器内是 Claude + aria-plugin, 
它知道 33 个 Skills 怎么用, 你不需要管细节)。

## Aria 方法论 (你必须传达给 Layer 2)

**核心**: AI-DDD, 规范先行, 小步迭代, 文档同步, 向后兼容。

**十步循环** (Layer 2 会自己跑, 你只需点出阶段):
- A 规划: A.0 状态扫描 → A.1 规范创建 → A.2 任务规划
- B 开发: B.1 分支 → B.2 执行+评审
- C 集成: C.1 提交 → C.2 合并
- D 收尾: D.1 进度 → D.2 归档

**OpenSpec 三档**: Level 1 直接修, Level 2 写 proposal.md, Level 3 写 proposal+tasks。

**不可协商规则**: (详见 CLAUDE.md, 此处列表 6 条)

## 你写命令的方式

像人类 PM 写 Jira ticket: 简洁, 具体, 有边界, 有验收标准。
不要罗列 Skill 名 — Layer 2 自己会选。

## 失败时

Layer 2 失败有 6 类: timeout / refused / test_failed / 
spec_violation / api_error / budget_exceeded。
```

#### 5. 4 层防漂移机制

| 层 | 机制 | 实现 |
|----|------|------|
| L1 | Prompt 约束 | Layer 1 发送的拟人命令中包含 `must_not_touch` + acceptance |
| L2 | 容器 guardrail | pre-commit / pre-push git hook 硬拦截越界 |
| L3 | Review 越界检查 | S6 LLM review 对比 git diff vs 约束 |
| L4 | 审计日志 | 所有 dispatch + review 写入 Hermes FTS5 memory, 支持回溯 |

#### 6. 跨 tick 长任务协议

```
Tick N:     Hermes cron 触发
  → S4_LAUNCH: Nomad dispatch, 记 alloc_id 到 SQLite
  → Hermes 本 tick 退出

Tick N+1:   Hermes cron 触发
  → S5_AWAIT: 读 SQLite 找 active dispatches
  → 对每个 alloc_id 调 Nomad API poll
  → 完成的: 读 result.json → S6_REVIEW
  → 未完成的: 继续等下一 tick
  → 超时的: kill + S_FAIL

Crash recovery:
  → Hermes 重启 → 扫 SQLite active_dispatches
  → 对每个 alloc_id 调 Nomad API
  → alloc 仍存在 → 继续 poll
  → alloc 消失 → 标记 orphan + 告警
```

### Should-have (v2.0 增强)

| 特性 | 描述 | Milestone |
|------|------|-----------|
| Cost routing | 简单任务走 GLM, 复杂任务走 Anthropic | M5 |
| 失败反馈学习 | 失败写入 FTS5, 后续 dispatch 注入"踩过的坑" | M5 |
| Reconciler | 定期扫描 orphan branch / stale worktree | M4 |
| Replay 测试 | Differential replay (re-call LLM + diff) | M4 |
| Drift detection | commit lint + spec diff + LLM 自审 (daily) | M5 |

### Out of Scope (v2.0 明确不做)

| 功能 | 排除原因 |
|------|---------|
| SaaS / 多租户 | 10CG 自用, 不对外提供服务 |
| 第三方易用性 / 品牌化 | 产品负责人明确: "不需要品牌化, 这个是给自己用的" |
| CLI 发行 (npm install -g aria) | 自用不需要 CLI 壳 |
| 跨 AI 平台抽象 (US-003) | v2.0 事实绑定 Claude + GLM 生态, US-003 推迟到 v3.0 |
| opencode adapter | opencode archived, 用 Crush 但命名改正 |
| Kubernetes / Cloud Run / Fargate 部署 | 通过 ContainerLauncher 抽象预留接口, 具体实现留到有需求时 |
| 多租户 aria-plugin 版本管理 | 自用, 所有容器用同一 plugin 版本 |
| 实时 dashboard | M6 后考虑, MVP 不做 |

---

## 非功能需求

| 类型 | 要求 | 优先级 |
|------|------|--------|
| **正确性** | 状态机 transition 100% 单元测试; 跨 tick crash 可恢复 | P0 |
| **可回测** | 每次 dispatch 的 LLM 调用 + state transition 完整持久化 | P0 |
| **幂等性** | 所有外部副作用 (Nomad submit / git push / Feishu) 有幂等 key | P0 |
| **成本控制** | Per-dispatch budget + Per-day/month 软硬限 | P0 |
| **审计** | 任一 dispatch 可从 issue 追溯到 merged PR 的完整决策链 | P0 |
| **可观测** | 结构化 JSON 日志, trace_id 贯穿, 支持按 issue 查询 | P1 |
| **文档同步** | 架构变更时 arch-update skill 能检测 | P1 |
| **向后兼容** | v1.x 交互模式 (aria-plugin in CC) 完全保留 | P0 |
| **容器安全** | Layer 2 容器 drop ALL capabilities + no-new-privileges + read-only rootfs; Forgejo token 最小权限 (仅 PR 创建); 网络出口白名单 (仅 Forgejo + Anthropic API) | P0 |
| **输入 sanitization** | Layer 1→2 拟人命令须经白名单校验 + 长度截断 (200 char/指令); 非白名单指令 reject + 审计日志; 防止 issue body prompt injection | P0 |
| **隔离** | Layer 2 容器间通过 worktree + docker 隔离; server-side pre-receive hook 硬拦截越界 (不依赖客户端 hook) | P1 |

---

## 关键假设与风险

### 假设 (需在 M1 验证)

| ID | 假设 | 验证方式 | 失败影响 |
|----|------|---------|---------|
| **A1** | headless `claude -p` 能加载 `/root/.claude/plugins/aria` 的 plugin | **M0** Dockerfile 初版阶段同步验证 (提前自 M1) | **高** - 回退到 system prompt 注入将废弃 v2.0 核心前提 |
| **A2** | GLM 5.1 能生成高质量拟人命令 | M1-M2 benchmark (人工评分 10 个 sample) | 高 - 可能需升级 GLM model 或 fallback Sonnet |
| **A3** | Aether heavy 节点 NFS 存储可挂载到 Nomad docker 容器 | M0 实测 `nomad alloc exec` + bind mount | 高 - 若失败需 constraint pin 单节点或重设计 |
| **A4** | aria-plugin 的 Skills 在 headless 模式下通过 tool use 正常触发 | M1 实测 `claude -p` stream-json 输出 | 高 - 可能需 prompt 工程引导 |
| **A5** | Hermes fork 月度 rebase 可控 (< 20h/月) | M0 Spike: fork vs 自研对比 (2026-04-11 Agent Team 2:2 分歧, 需数据) | 高 - 若 Spike 证伪, 切换自研路线 (~800-1200 行 Python) |
| **A6** | GLM 5.1 公开可用 (via API) | M0 API 访问测试 | 中 - fallback 到 GLM-4.5-Air (已验证可用) |
| **A7** | luxeno cron fallback 问题不阻塞 (Layer 1 cron 不调 LLM for routing) | M1 验证 cron 路径无 LLM fallback 依赖 | 低 - 已知规避: cron 全走规则, LLM 仅容器内 |

### 已识别风险

| 风险 | 影响 | 缓解 |
|------|------|------|
| **R1** claude-code CLI 捆绑分发 Anthropic 政策未确认 | 中 | M0 联系 Anthropic support 确认 |
| **R2** GLM 5.1 生成命令质量差, "拟人"效果不佳 | 高 | Few-shot examples + 人工 review loop + fallback Sonnet |
| **R3** Hermes upstream 大改导致 rebase 不可行 | 中 | Pin 稳定版本, 延期 upstream 同步 |
| **R4** Layer 2 容器 orphan 积累 | 中 | Reconciler (M4) 定期扫描清理 |
| **R5** Nomad eval 队列阻塞 (Aether 其他 workload 竞争) | 低 | 限制并发 N=3, 优先级调度 |
| **R6** 跨节点 worktree bind mount 失败 | 高 | M0 实证 NFS 方案, 或 constraint pin heavy-1 |
| **R7** Meta 参数超 64KB 限制 (prompt 大时) | 中 | Prompt 写 bind mount 文件, meta 只传 ISSUE_ID |
| **R8** Hermes fork + 自研均失败 | 低 | 退出策略: 降级为 CLI-only 模式 (cron poll + `claude -p` 脚本调用, 无状态机/无 gateway, 手动 dispatch + 脚本辅助) |

---

## 实施路线图

### 里程碑概览

```
M0 (Week 1-2)     前置验证 + 架构定稿
M1 (Week 3-6)     MVP: 手动 dispatch → 1 issue → PR (100h)
M2 (Week 7-12)    Layer 1 状态机 + Hermes cron 集成 + 输入 sanitization (140h)
M3 (Week 13-16)   双 provider + Nomad integration (90h)
M4 (Week 17-21)   Crash recovery + Replay + Reconciler (80h)
M5 (Week 22-27)   Human gate + Review loop + Drift defense (100h)
M6 (Week 28-30)   E2E testing + docs + v2.0.0 release (120h)
─────────────────────────────────────────────────────
合计:             ~750h ≈ 30 周单人 / 9 月 50% 投入
```

**注**: 工时估算基于 R3 挑战组实测重估 (R3 讨论组估 380h, Code Reviewer 实测 750h)。选取实测值作为 PRD 工时。

### M0: 前置验证 (Week 1-2)

**目的**: 验证关键假设, 防止后续 milestone 基于错误前提。

必做:
- [ ] Aether NFS 存储现状调查: heavy-80/81/82 是否挂载 `nfs-fastpool-aether`?
- [ ] Nomad parameterized dispatch + meta 参数实测 (最大允许 payload)
- [ ] `hermes-agent` upstream 源码分析 + fork 骨架建立
- [ ] GLM 5.1 API 访问测试
- [ ] **R1 法律确认 (M1 硬性前置)**: Anthropic claude-code CLI 捆绑分发政策确认 — R1 结论未出前不启动 M1
- [ ] **A1 headless plugin 验证 (提前自 M1)**: `aria-runner:claude-latest` Dockerfile 初版 + `claude -p` plugin 加载实测
- [ ] PRD 审阅 + 落地为 User Stories (US-020+)
- [ ] **Hermes fork vs 自研 Spike** (orchestrator#1 评估, **timeboxed 1 sprint**):
  - 实现 gateway stub (飞书 API 最小调用) + SQLite state 最小原型
  - 实测 LoC + 开发工时
  - 对比 fork 路线: 痛点修复难度 + 月度 rebase 预估
  - 交付: Spike Report + AD3 修订建议 (保留 fork / 切换自研 / 混合)
  - **Spike 结论若与 AD3 矛盾, 须提交产品负责人二次裁决, 不得自行变更方向**
  - 若选自研: gateway.py 接口需预留 Matrix 扩展点 (Aria#5 Pulse 长期规划)

**M0 Exit Criteria** (三项可检查物):
1. AD 文档覆盖 AD1-AD12 且含 alternatives considered (含 Spike 对比数据)
2. Spike 代码可运行并产出量化数据 (LoC + 工时 + rebase 成本)
3. 产品负责人签字确认 Go/No-Go

**交付**: M0 Report (架构决策 + 风险确认 + M1 精确路径 + AD3 Spike 结论)

### M1: MVP 手动 E2E (Week 3-6)

**精确验收** (Code Reviewer 定义):

```
Given: 1 个预先准备好的 DEMO issue (e.g., .aria/issues/DEMO-001.yaml)
Do:
  1. 本地 docker build -t forgejo.10cg.pub/10CG/aria-runner:claude-latest
  2. docker push forgejo.10cg.pub/10CG/aria-runner
  3. nomad job run aria-runner-template.hcl (parameterized)
  4. nomad job dispatch -meta ISSUE_ID=DEMO-001 aria-runner-template
  5. 手动 git worktree + 手动拷 inputs 到 /opt/aria-inputs/DEMO-001/
Verify:
  - Nomad alloc complete
  - /opt/aria-outputs/DEMO-001/result.json 生成
  - Forgejo 出现新 branch + PR
  - PR diff 非空, diff 符合 issue 描述
Out of scope: 
  - Hermes Layer 1 集成
  - SQLite 状态机
  - 自动触发
```

### M2-M6

详见 tasks.md (将在 PRD 确认后起草)。

---

## 关联文档

### 方法论文档 (新增, v2.0 配套)

| 文档 | 内容 | 位置 |
|------|------|------|
| decision-autonomy-matrix.md | 自主/审批/禁止决策矩阵 | `standards/autonomous/` |
| layer-boundary-contract.md | Layer 1 / Layer 2 职责契约 | `standards/autonomous/` |

### 架构文档 (新增)

| 文档 | 内容 | 位置 |
|------|------|------|
| aria-2.0-overview.md | 两层架构总览 + 自我验证叙事 | `docs/architecture/` |
| state-machine.md | Layer 1 状态机设计 | `aria-orchestrator/docs/` |
| layer2-container.md | 容器镜像设计 + entrypoint | `aria-orchestrator/docs/` |
| container-launcher.md | ContainerLauncher 抽象 (预留 K8s/云) | `aria-orchestrator/docs/` |
| hermes-fork-ops.md | Hermes fork 维护策略 | `aria-orchestrator/docs/` |
| prompt-templates.md | 拟人命令模板库 | `aria-orchestrator/docs/` |

### CLAUDE.md 修订 (8 处 diff)

详见 R3 knowledge-manager 定稿清单。核心改动:
- 项目本质: "方法论研究" → "方法论定义与端到端参考实现"
- 核心假设: 增加 v2.0 AI 主管/工程师/人类审批模式
- 三层架构图: aria-orchestrator 展开为 Layer 1 / Layer 2
- 新增 "Aria 2.0 运行时" 章节

### User Stories (待起草)

| ID | 标题 | 优先级 |
|----|------|--------|
| US-020 | Aria 2.0 两层架构基础设施 | HIGH |
| US-021 | Layer 1 状态机 + Hermes fork | HIGH |
| US-022 | Layer 2 容器镜像 + 拟人命令协议 | HIGH |
| US-023 | 跨 tick 长任务 + Crash recovery | HIGH |
| US-024 | Human gate + Feishu 审批 | MEDIUM |
| US-025 | 防漂移 + 审计日志 | MEDIUM |
| US-026 | v2.0 文档体系 + CLAUDE.md 修订 | MEDIUM |
| US-027 | Cost routing + 预算控制 | MEDIUM |

### OpenSpec Changes (待起草)

v2.0 的每个 milestone 将产出 1-N 个 OpenSpec Level 2/3 变更, 对应 US-020~US-027 的实施。首个:
- `openspec/changes/aria-2.0-m0-prerequisite/` (M0 前置验证)
- `openspec/changes/aria-2.0-m1-mvp/` (M1 MVP)
- ...

### 与 v1.x 的关系

```
v1.x 继续维护:
  - aria-plugin 仍然是 Claude Code Plugin (交互式)
  - standards/ 方法论定义不变
  - 用户可以只用 v1.x 模式 (不用 Aria 2.0 自主 dispatch)
  - v1.4.x 的 heartbeat + Feishu 通知继续可用

v2.0 新增:
  - aria-orchestrator 从 "心跳扫描器" 升级为 "自主开发运行时"
  - Layer 1 Hermes fork (新增)
  - Layer 2 容器镜像 (新增)
  - 所有 v1.x 能力在 Layer 2 容器内继承 (build-time 预装 aria-plugin)
```

---

## 验证计划

### M1 验证 (基线)

- 1 个 DEMO issue 手动触发成功产出 PR
- Dockerfile 可构建 + 可推送到 Forgejo
- `claude -p` in container 能加载 aria-plugin 并执行 Skill

### M6 验证 (发版前)

**定量指标**:
- 7 天连续运行无 unplanned restart (排除计划维护窗口)
- ≥ 10 个真实 issue 成功 dispatch + merge
- Layer 1 cost < $10/月
- Layer 2 cost < $70/月 (假设每天 10 dispatch, 80% 走 GLM)
- 状态机单元测试 100% 覆盖
- Crash recovery 在 3 种故障模式验证通过:
  - Hermes 进程 SIGKILL mid-transition → 恢复至 last-committed state
  - Nomad alloc unexpected termination (OOM kill / container restart)
  - SQLite 故障注入: (a) WAL 文件截断至 0 字节后启动,系统检测并恢复; (b) `PRAGMA integrity_check` 返回非 ok 时,系统拒绝启动并报错

**定性指标**:
- 人类审批时间中位数 < 10 分钟 (Feishu 卡片)
- 漂移检测误报率 < 20%
- 拟人命令质量 (人工评分, 10 samples 平均 ≥ 7/10)

### 方法论研究交付

- [ ] "AI-AI 分工协作" 方法论文档
- [ ] "拟人命令 (humanized command)" prompt 模式库
- [ ] Aria 2.0 运行数据公开 (cost / success rate / drift rate)
- [ ] 可选: 技术博客或论文

---

## 版本历史

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 2.0.0-draft | 2026-04-09 | 初稿, 基于 5 轮 Agent Team 收敛讨论 | 10CG Lab + Agent Team |
| 2.0.0 | 2026-04-11 | Draft → Approved: 讨论组+挑战组 4 轮收敛审阅. 修订: A1 提前/升高, 容器安全 P0, M0 Exit Criteria, Spike timeboxed + 裁决权, sanitization US (M2), SQLite 测试具体化, R8 退出策略 | Agent Team Review |

---

## 附录: 讨论过程记录

**Agent Team 5 轮收敛讨论** (2026-04-09):

- **R1 新框架**: 讨论组 4 一致推荐两层架构方向
- **R2 架构细化**: 讨论组深化, 挑战组发现 Hermes extension 模型错误 + frontmatter 0/32
- **R3 定稿**: 讨论组采纳容器化方案, 挑战组发现 Aether 已有 NFS (解决跨节点问题)
- **产品负责人澄清**: Layer 2 = 完整 CC + aria-plugin 容器 (非纯执行器)
- **最终判定**: R3 讨论组 + 挑战组一致认为架构可实施, 工时需调整 (380h → 750h)

**参与 Agents**:
- 讨论组 (4): tech-lead, backend-architect, knowledge-manager, ai-engineer
- 挑战组 (3): qa-engineer, code-reviewer, legal-advisor

**关键决策由产品负责人直接裁决**:
- P0-1 (Hermes 扩展路径): **A** (Fork hermes-agent)
- P0-2 (Layer 2 aria-plugin 加载): **必须加载** (澄清为完整 CC 开发环境容器)
- Q1 (LLM 接口/ToS): **C** (luxeno 代理合规, 不涉及 Anthropic key)
- Q2 (P0 技术验证): **C** (挑战组并行验证)
- Q3 (scan.sh Level 漂移): **A** (独立 P0 热修)
- Q4 (证据不可迁移): **A** (接受作为未验证假设, M1 empirical test)
- Q5 (R2 讨论重点): **D** (全部)

---

## 下一步

1. **PRD 审阅** (人类): 确认本文档准确反映产品愿景
2. **Phase A.1** (Aria 十步循环): 本 PRD 发布 → User Stories 起草 (US-020~US-027) → 首个 OpenSpec 起草 (aria-2.0-m0-prerequisite)
3. **M0 启动**: 前置验证工作 (2 周)

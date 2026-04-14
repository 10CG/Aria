---
date: 2026-04-14
mode: agent-team-convergence
target_artifact: docs/requirements/user-stories/US-020.md
parent_decision: .aria/decisions/2026-04-14-aria-2.0-us020-scope.md
parent_prd: docs/requirements/prd-aria-v2.md
discussion_group:
  - aria:tech-lead
  - aria:backend-architect
  - aria:ai-engineer
  - aria:knowledge-manager
challenge_group:
  - aria:qa-engineer
  - aria:code-reviewer
  - aria:legal-advisor
convergence_criteria:
  - 讨论组本轮共识 == 上一轮共识
  - 挑战组本轮无新反对意见
status: converged
rounds_completed: 4
convergence_date: 2026-04-14
---

# US-020 Agent Team 收敛评审

本文件按"讨论 → 挑战"循环记录 US-020 评审过程，每一轮包含讨论组共识和挑战组反对意见。
满足收敛条件后写入最终建议，触发 US-020 修订与 OpenSpec 起草。

---

## Round 1

### 讨论组共识 (tech-lead + backend-architect + ai-engineer + knowledge-manager)

#### R1-D1 验收标准需"数字化 + 可证伪"

- **R1-D1.1** Spike 成功阈值硬编码到 Spike Spec:
  - fork 路径 acceptable: 月度 rebase ≤ **20h** 且痛点修复无 blocker
  - 自研路径 acceptable: 总 LoC ≤ **1000** (Python, 含测试) 且实测开发 ≤ **60h**
  - 双路径都 acceptable → 选 fork (PRD 默认); 仅一条 → 选该条; 双 fail → 升级 R8
- **R1-D1.2** Spike 最小原型必含硬编码状态转换演示: `idle → dispatched → running → awaiting_human → resumed` (5 states, 4 transitions), 覆盖正常路径 + 1 个 human-in-loop
- **R1-D1.3** Spike rebase 评估必须**实际执行一次** (pull upstream / 解冲突 / 跑测试), 而非仅基于 changelog 估算

#### R1-D2 任务粒度与子任务补齐

- **R1-D2.1** T1 (R1 legal-advisor) 作为 **Day 0.5 前置闸门**, 早于 T2/T4 启动, 避免"升级回邮件确认"的逃生口延迟整个 M0
- **R1-D2.2** T5 拆前置子任务: Day 1 先产出 "AD1-AD12 索引草表" 交产品负责人锁定命名, 避免 8h 估算因"什么算 AD"扯皮
- **R1-D2.3** T2 NFS 验证显式两子步: (a) `nomad alloc exec` 确认 NFS 挂载点可见; (b) parameterized job 实际写入 `/opt/aria-outputs/` 并从宿主读回
- **R1-D2.4** T3 Dockerfile 验证补充: `--read-only --tmpfs /tmp` 冒烟跑一次 headless plugin 加载 (容器安全要求 P0 的最小实证)
- **R1-D2.5** T3 顺带锁定 `/opt/aria-inputs` `/opt/aria-outputs` bind mount 行为 (可写 + 宿主可见), 因为 M1 验收直接依赖
- **R1-D2.6** T3 增 ~2h GLM 5.1 拟人命令 smoke test: 用 GLM 生成 5 条 Skill 触发 prompt 跑 state-scanner, 人工评分 (非 A2 完整验证, 仅防"GLM 完全不可用"极端失败)
- **R1-D2.7** T4 Spike 内拆 ~3h 子任务: 起草 Hermes 1K token 元知识 prompt v0.1 并在 Spike gateway 实跑, 验证 token 预算与格式

#### R1-D3 跨 Story 接口与交付物

- **R1-D3.1** M0 Report 末尾附 **`m0-handoff.yaml`** 机读契约, 内含: AD3 决议 / NFS 路径 / 镜像 tag / R1 四点结论 / Spike 选型结果。US-021 task-planner 直接消费, 避免从 markdown 里 grep
- **R1-D3.2** Spike Report 归档到 `openspec/changes/aria-2.0-m0-spike-hermes/` 内部 (Spec 交付附件), 而非 `aria-orchestrator/docs/`。AD3 最终结论回填 `architecture-decisions.md` 时以引用路径指向
- **R1-D3.3** CLAUDE.md 修订**草案** 在 T5 完成后产出 (不提交, 仅待 US-026 执行), 随 M0 Report 一并交产品负责人; 避免 M6 时重新理解 M0 决策
- **R1-D3.4** 明确**不在 M0 范围**: (a) `standards/autonomous/` 目录骨架; (b) PRD §关联文档 列出的其余 6 个架构 doc (aria-2.0-overview / state-machine / layer2-container 等); 这些推迟到 M1+; 需在 T5 任务说明中显式禁止范围蔓延

#### R1-D4 工时与风险控制

- **R1-D4.1** T4 Spike 从 40h 扩到 **~50h** (或将报告撰写从 T4 挪到 T6), 消化新增子任务 (元知识草稿 + rebase 实操)
- **R1-D4.2** 15h 缓冲明确分配: T3 (+5h, A1 失败探查预算) + T4 (+5h, Spike 超时缓冲) + T6 (+5h, 裁决往返)
- **R1-D4.3** PRD R8 触发条件显式化: T3 实际工时 > **16h** 即触发 A1 失败评估; T4 > 60h 即触发 Spike 终止
- **R1-D4.4** R7 (Nomad meta 64KB) 不需 M0 专门实测, 但必须写入 T5 AD 文档作为 **M1 Layer 1→2 协议硬约定** (prompt 走文件, meta 只传 ISSUE_ID)

#### R1-D5 裁决机制

- **R1-D5.1** 产品负责人裁决增加第三态 **Go-with-Revision**: 触发 PRD 局部修订而非二元 Go/No-Go, 避免混合路径被强制降级为 No-Go → R8 退出
- **R1-D5.2** 裁决三态的具体语义:
  - **Go**: 原 PRD 有效, 进入 US-021
  - **Go-with-Revision**: 修订 PRD 指定章节 (AD3 / R 系列 / M1 路径), 进入 US-021
  - **No-Go**: 触发 R8 退出策略 (CLI-only 降级模式) 或 PRD 整体重写

### 红旗 (讨论组自己识别, 非挑战组)

- **FL-1** (backend-architect) 容器安全要求推迟会在 M1 反向发现 read-only rootfs 与 headless 写路径冲突 → 已被 R1-D2.4 吸收
- **FL-2** (ai-engineer) Spike rebase 仅基于 changelog 估算不足以 binding 750h 投资 → 已被 R1-D1.3 吸收
- **FL-3** (knowledge-manager) PRD §关联文档 缺 Milestone 归属标注, 执行 agent 易将 M1+ 文档误纳入 M0 → 已被 R1-D3.4 吸收

### 挑战组反对意见 (qa-engineer + code-reviewer + legal-advisor)

**qa-engineer 反对** (5 条):
- **R1-C-Q1** 【R1-D1.1】≤1000 LoC / ≤20h rebase 是无依据绝对阈值。建议改为相对阈值 (例: 自研 ≤ fork × N) + 测量协议 (cloc + 排除项)
- **R1-C-Q2** 【R1-D2.3 / R1-D2.5】"宿主可见" 未定义用户身份与权限。建议补充: 以 Nomad agent user 读取 + md5 校验内容完整性
- **R1-C-Q3** 【R1-D2.6】"人工评分" 无评分表无通过线。建议改二值化 ("5 条中 ≥4 条触发 Skill 且返回非空结果") 或删除人工评分措辞
- **R1-C-Q4** 【R1-D5.1/5.2】Go-with-Revision 缺"修订完成"定义, 形成开放阻塞。建议补充: 修订 PR + code-reviewer 通过 + 二次签字, timebox ≤3 工作日, 超时降级 No-Go
- **R1-C-Q5** 【R1-D2.1】T1 Day 0.5 前置闸门 + T2/T4 启动权限未定义。建议: T2/T4 启动条件 = T1 出具无新疑点结论; 若 T1 升级邮件确认, T2/T4 hold, 不产出依赖合规结论的交付物

**code-reviewer 反对** (3 条):
- **R1-C-C1** 【R1-D5.1/5.2】三态裁决与 PRD M0 Exit Criteria 二元语言冲突, US 无权绕过已批准 PRD。建议: 标记 R1-D5.1 为"需 PRD 修订作为前置", 同步修改 US-020 §D 段, 或回退到二元语义
- **R1-C-C2** 【R1-D4.1 + R1-D2.7 + R1-D1.3】T4 工时口径冲突。R1-D4.1 扩 10h, R1-D2.7 加 3h, R1-D1.3 新增 rebase 实操未估值, R1-D4.2 又从 15h 缓冲拨 5h 到 T4, 存在重复/低估。建议: 统一 T4 为单一数字 (含所有新增子任务), 明确缓冲池是全局还是已分配
- **R1-C-C3** 【R1-D3.2】Spike Report 路径与 US-020 §B "Spike 代码存放 `aria-orchestrator/spikes/hermes-route/`" 静默冲突。建议: 先修订 US-020 §B 将 Spike Report 路径统一到 `openspec/changes/aria-2.0-m0-spike-hermes/`, 或明确两处主从关系

**legal-advisor 反对** (4 条):
- **R1-C-L1** Hermes fork upstream 依赖链 **license 污染风险**未覆盖。upstream 若升级依赖到 GPL/AGPL, fork 自动受 copyleft 约束。建议: T1 或 T4 Spike 补充 license 兼容性扫描 (cloc / npm ls + FOSSA/Black Duck), Spike 评估加"downstream license 兼容性"维度
- **R1-C-L2** **GLM 5.1 ToS 自动化限制**未验证。自动化 Agent 调用可能需特殊声明; luxeno 代理是否获 GLM 官方授权未知。建议: T1 补充查证 GLM 官方 ToS 与 luxeno 代理协议
- **R1-C-L3** **Luxeno 数据流跨境合规性**未涉及。Hermes 通过 luxeno 转发代码/issue 到 GLM (国内), 是否需 DPA / 数据不落地承诺。建议: T1 查证 luxeno 数据处理条款
- **R1-C-L4** **容器镜像事实上再分发风险**。若 aria-orchestrator 公开文档误含 `docker pull` 示例, 构成事实分发。建议: T1 补充确认 M0 所有文档禁止 docker pull 示例, 或明确需 Anthropic 书面同意
- **总体**: legal-advisor 认为 T1 的 **1h 不足以深入** 上述新疑点, 建议调整 T1 预算或拆分
- **免责声明**: legal-advisor 明确 "本评审基于文档推理, 不构成正式法律意见"

### Round 1 收敛判定

- 讨论组共识: 有内容 (首轮, 无上一轮对比)
- 挑战组反对: **12 条** (5 + 3 + 4, 另加 legal-advisor 关于 T1 工时的总体意见)
- **未收敛**, 进入 Round 2

---

## Round 2

### 讨论组共识 (收敛内部 3 处分歧后的统一建议)

#### R2-D1 裁决机制 (R1-C-C1 回应)

采用 **knowledge-manager 方案** (Go + 平行 PRD patch), 拒绝 tech-lead 的"PRD 修订前置":

- **R2-D1.1** US-020 §D 维持 PRD 原二元 Go/No-Go, 不引入三态
- **R2-D1.2** 若产品负责人希望"局部修订": 签 Go + 同步起草 PRD patch PR, 两动作原子绑定
- **R2-D1.3** PRD patch PR 必须在 **3 工作日内**合并, 否则冻结 US-021 启动 (作为 US-020 关闭后的附加看护条件, 不阻塞 US-020 本身关闭)
- **R2-D1.4** PRD patch PR 起草工时 (~3h) 归 T6, 不计入 M0 750h 主预算
- **拒绝 tech-lead 的 PRD 修订前置**: 会把本次 brainstorm 的架构级细化变成 PRD 治理流程的 circular dependency; knowledge-manager 路径更轻

#### R2-D2 T1 legal 工时与失败路径 (R1-C-Q5 + R1-C-L1~L4 合并)

- **R2-D2.1** T1 工时由 1h → **4h** (legal 扫描 1.5h + GLM ToS + luxeno 查证 1h + 跨境合规 1h + docker pull 文档审计 0.5h)
- **R2-D2.2** T1 状态机:
  - `T1.status == done && new_concerns == ∅` → T2/T3/T4 全启动
  - `T1.status == awaiting_external` (升级邮件确认) → **T2 可启动** (NFS 与合规无关), **T3/T4 hold** (镜像 + Spike 与合规强耦合)
  - T1 外部确认 timebox: **≤5 工作日**, 超时按 No-Go 处理
- **R2-D2.3** T1 时间线从 Day 0.5 调整为 **Day 0–1** (单 agent 串行 4 项查证, wall-clock 更现实)
- **R2-D2.4** 新增风险项 **R9**: GLM 5.1 ToS 自动化条款未正式确认, M1 前必须取得官方书面确认; Spike 阶段**禁止上传真实代码/issue**, 仅用合成 fixture 跑 GLM smoke
- **R2-D2.5** Spike fixture (合成 issue/code) 存入 `aria-plugin-benchmarks/ab-suite/` 作为可复用资产

#### R2-D3 Spike 量化阈值 (R1-C-Q1 + R1-C-L1 回应)

采用 **backend-architect 方案** (绝对阈值 + cloc 协议), 拒绝 ai-engineer 的"相对公式":

- **R2-D3.1** 阈值维持绝对数:
  - fork acceptable: 月度 rebase ≤ 20h (实测 1 次 × 1.5 安全系数)
  - 自研 acceptable: `cloc --include-lang=Python --exclude-dir=.venv,__pycache__,migrations` 后业务 Python LoC ≤ 1000, 测试 LoC 单列不计入 (工具可复现)
  - 双 fail → R8 退出策略
  - 双 acceptable → 默认 fork; 单边 → 选可行路径; 选择后的 PRD patch PR 由产品负责人起草
- **R2-D3.2** **license 兼容性** 作为 Spike 第 5 评估维度: Day 1 跑 `npm ls --all --json | jq` + Python 依赖 license 扫描; 若发现 GPL/AGPL 传染 → fork 路径自动降级, 倾向自研
- **R2-D3.3** Spike 必须 **实际执行一次 rebase** (pull upstream / 解冲突 / 跑测试), 非纯 changelog 估算
- **拒绝 ai-engineer 的相对公式** (LoC × 0.05h/LoC/月 × 12): 常数本身是拍脑袋, 无操作性改进

#### R2-D4 T4 工时统一口径 (R1-C-C2 回应)

统一为单一数字, 采用 **knowledge-manager 的 ~53h 基线**:

- **R2-D4.1** T4 = **52h** (base 40 + 元知识草稿 3 + rebase 实操 3 + license 扫描 1 + 报告撰写 5)
- **R2-D4.2** 报告撰写**保留在 T4 内** (不挪到 T6), 避免跨 task 归属漂移
- **R2-D4.3** T4 触发阈值: 实测 > **60h** (基线 +15%) 启动评估, > 72h 强制终止
- **R2-D4.4** **T4 = 52h** 替代 R1-D4.1 (50h) 和 backend-architect (56h), R1-D4.1 撤回

#### R2-D5 任务与工时重新基线 (全局)

新 M0 工时表:

| Task | 原 | 新 | 增量原因 |
|---|---|---|---|
| T1 | 1h | **4h** | legal 4 项查证 (R2-D2.1) |
| T2 | 4h | **4h** | + md5 与 user identity 校验 (0 新增工时) |
| T3 | 8h | **10h** | + GLM smoke 1.5h + read-only rootfs 验证 0.5h |
| T4 | 40h | **52h** | R2-D4.1 |
| T5 | 8h | **8h** | 不变 |
| T6 | 4h | **7h** | + Go-with-Revision PRD patch PR 起草 3h (R2-D1.4) |
| **Core** | 65h | **85h** | +20h |
| Buffer | 15h | **10h** | 缓冲池缩减, 剩余留给 T4 超时应急 |
| **Total** | **80h** | **95h** | M0 扩容 15h (2 周 window 内可消化) |

#### R2-D6 验收标准细化 (R1-C-Q2 + R1-C-Q3 + R1-C-L4 回应)

- **R2-D6.1** T2 "宿主可见" 硬定义: Nomad agent user (UID 推断自 `nomad node status`) 执行 `md5sum /opt/aria-outputs/<file>` 与容器内 md5 一致; 缺一即 fail
- **R2-D6.2** T3 GLM smoke test 二值化: 5 条 GLM 生成的拟人 prompt 中 **≥4 条** 触发 state-scanner 且返回非空 YAML (grep `current_phase:`) = pass; <4 条 → 升级 R8 评估
- **R2-D6.3** T3 新增验收: `--read-only --tmpfs /tmp` 模式下 `/opt/aria-outputs/` bind mount 仍可写入 (read-only rootfs 与可写 bind mount 的组合在 M0 锁定, 避免 M1 反向发现)
- **R2-D6.4** M0 所有文档 (US + OpenSpec + Spike Report + Dockerfile README) 禁止 `docker pull aria-runner` 示例, 仅允许 `docker build`, Dockerfile README 头部加免责声明 "仅限 10CG Lab 私有集群内部使用"

#### R2-D7 Spike 交付物路径主从关系 (R1-C-C3 回应)

- **R2-D7.1** 主从关系:
  - Spike **代码** (可运行原型): `aria-orchestrator/spikes/hermes-route/` (执行就近)
  - Spike **Report** (markdown 分析文档): `openspec/changes/aria-2.0-m0-spike-hermes/spike-report.md` (Spec 交付主位置)
  - 两者以相对路径互链
- **R2-D7.2** US-020 §B 对应检查项需修订措辞以消除"估算 vs 实测"隐性冲突 (knowledge-manager 新发现): 从 "rebase 工时预估 (基于近 3 月 changelog 估算)" 改为 "rebase 工时**实测一次** + changelog 外推 3 月, 两数据点都报告"
- **R2-D7.3** AD3 最终结论回填 `aria-orchestrator/docs/architecture-decisions.md` 时以 **OpenSpec 路径** 作为主引用 (Spec 稳定; 代码路径在 fork/自研后可能漂移)
- **R2-D7.4** `m0-handoff.yaml` 新增 `spike_code_path` 字段, US-021 自动迁移时消费 (若 Spike 选自研, `spikes/hermes-route/` 提升到 `src/` 的路径由 US-021 承接)

### 讨论组内部分歧处理记录

| 分歧点 | tech-lead | backend-architect | ai-engineer | knowledge-manager | Orchestrator 裁决 | 依据 |
|---|---|---|---|---|---|---|
| 裁决机制 (R1-C-C1) | PRD 修订前置 | — | — | Go + 平行 PR | **knowledge-manager 方案** | 避免 circular 治理依赖 |
| LoC 阈值 (R1-C-Q1) | — | 绝对 + cloc | 相对 + 公式 | — | **backend-architect 方案** | 可执行性 > 防伪精度 |
| T4 工时 (R1-C-C2) | 40h (report→T6) | 56h | — | 53h | **52h (knowledge 接近)** | 报告不挪动避归属漂移 |

### Round 2 讨论组与 Round 1 差异

- **变化条目**: R1-D1.1 收紧 (cloc 协议) / R1-D2.1 (Day 0.5 → Day 0-1) / R1-D2.6 (人工评分 → 二值化) / R1-D4.1 (50h → 52h 含 license) / R1-D5 (三态裁决 → 二元 + 平行 PR) / 新增 R2-D2.4 R9 风险 / R2-D2.5 fixture 路径 / R2-D6.3 read-only bind mount / R2-D6.4 docker pull 禁令 / R2-D7.2 §B 措辞修订 / R2-D7.4 `spike_code_path` 字段
- **未变条目**: R1-D1.2 R1-D1.3 R1-D2.2 R1-D2.3 R1-D2.4 R1-D2.5 R1-D2.7 R1-D3.1 R1-D3.3 R1-D3.4 R1-D4.3 R1-D4.4
- **撤回条目**: R1-D4.1 (被 R2-D4 吸收) / R1-D5.1 R1-D5.2 (三态裁决, 被 R2-D1 替代)

显然与 Round 1 不一致, **未收敛**, 进入 Round 2 挑战组。

### Round 2 挑战组反对意见

**qa-engineer 反对** (3 实质 + 1 改进):
- **R2-C-Q1** 【R2-D3.1 补漏】安全系数 ×1.5 基于单次实测, 若 upstream 在 M0-M1 间有大版本合并易被击穿。建议: 系数随 upstream 近 6 月 commit velocity 动态取 (≤200 commits/月 → ×1.5; >200 → ×2.0), Spike Report 记录 velocity
- **R2-C-Q2** 【R2-D1.3 实质反对】"冻结 US-021 启动" 无执行主体。US-020 关闭后, task-planner / state-scanner 不会主动读附加看护条件。建议: m0-handoff.yaml 新增 `prd_patch_pr` 字段, US-021 启动前该字段必须非空
- **R2-C-Q3** 【R2-D2.2 新增漏洞】T1 → `awaiting_external` 时 T2 启动产出 NFS 报告, 但未说明若 T1 最终 No-Go (触发 R8 或换 provider) → T2 产出是否作废 / 需重测。建议: 补 T2 产出在 T1 No-Go 下的处置规则, 重测成本计入 10h 缓冲
- **R2-C-Q4** 【R2-D6.2 改进】pass 边界歧义: "触发 Skill 但返回空 YAML" vs "完全未触发" 是两种失败模式。建议: fail 样本原始 prompt + 输出归档到 `ab-suite/glm-smoke/failed-samples/`

**code-reviewer 反对** (4 实质):
- **R2-C-C1** 【R2-D1 实质反对】"签 Go + 同步起草 PRD patch PR" 无 atomic 机制保证, 0-3 工作日 governance 真空窗口仍存在, R1-C-C1 核心诉求未解决。建议: US-020 §D 显式门控 — 产品负责人签 Go 时须同步提交 `prd_patch_pr` 号 (或显式 N/A), m0-handoff.yaml 的该字段非空是 US-021 启动前置
- **R2-C-C2** 【R2-D5 实质反对】T2 标 "0 新增工时" 与 R2-D6.1 (UID 推断 + md5 双向比对) 内容不一致, 实际 ~0.5h 增量。建议: T2 标 +0.5h 或在工时表注释中显式说明 md5 已含在原 4h
- **R2-C-C3** 【R2-D5 实质反对】US-020 头部 `Estimated: ~80h / 2 weeks` 未与 R2-D5 新基线 95h 同步, 执行 agent 读 US-020 会拿错数据。建议: 收敛后必须同步修订 US-020 头部
- **R2-C-C4** 【Round 2 差异清单 MECE 漏洞】R1-D2.1 (Day 0.5) 被 R2-D2.3 实质替代, 应进"撤回清单"而非"变化条目"。建议: 修复 Round 2 差异清单分类

**legal-advisor 反对** (6 实质):
- **R2-C-L1** 【R2-D2.4 R9 硬闸门缺失】R9 "M1 前取得官方书面确认" 是纸面要求, 无约束。建议: M0 Report 须含 "R9 官方回应等待状态"; 若 M1 启动前官方未回应, 产品负责人须**显式签字**声明"法律风险自承诺下继续", 不得隐性推进
- **R2-C-L2** 【R2-D2.5 fixture 合成方法论缺失】合成 fixture 必须**排除真实代码特征** (类名 / 函数签名 / 业务逻辑纹理), 即使匿名化也需二审。建议: fixture 生成走模板, 禁止从真实仓库采样
- **R2-C-L3** 【R2-D3.2 依赖扫描工具不足】`npm ls --all --json | jq` 仅扫直接依赖, 传递依赖漏检率高。建议: 指定工具 (`npm-check-licenses` / FOSSA / Black Duck) 且扫描深度 ≥ transitive; Spike Report 列全 direct + transitive 的 GPL/AGPL 风险
- **R2-C-L4** 【R2-D6.4 免责声明法律效力】"仅限 10CG Lab 私有集群" 是声明性非契约性, 无法阻止他人忽视。建议: Dockerfile 添加构建时检验 `ARG DEPLOY_ENV=internal; RUN if [ ... ]; then exit 1; fi`, 技术栅栏 + 文字声明并行
- **R2-C-L5** 【R2-D2.1 T1=4h 仍不足】legal 估算: license 1.5h + GLM ToS 0.5h (仅定位) + luxeno 0.5h (仅接触) + 跨境 1h (仅知会) + docker pull 0.5h = **4h 底线**, 若要实质保证需 **5h**。建议: T1 扩到 5h 或明确缩减范围 (例如跨境合规仅风险提示不做深度审)
- **R2-C-L6** 【全新问题】Aether heavy 节点归属未明: 若非 10CG 自有 → 第三方基础设施合规 (多方数据处理协议 / 第三方条款) 可能触发。建议: T1 补一项 ~0.5h 查证 Aether 节点物理归属与合规路径

### Round 2 收敛判定

- 讨论组共识: 与 Round 1 显著不同 (见差异清单)
- 挑战组反对: **13 条** (qa 4 / code-reviewer 4 / legal 6; qa 的 R2-C-Q4 为改进但含明确修订动作, 计入)
- **未收敛**, 进入 Round 3

---

## Round 3

### 讨论组共识 (全部采纳 Round 2 挑战组反对, 仅 1 处内部分歧由 orchestrator 裁决)

#### R3-D1 `prd_patch_pr` 字段作为 US-021 启动前置 (R2-C-C1 + R2-C-Q2 合并)

- **R3-D1.1** `m0-handoff.yaml` schema 在 US-020 §D **内联锁定最小字段集**: `{go_decision, prd_patch_pr, r9_status, spike_code_path, nfs_path, image_tag, ad3_conclusion}`, 不在 US-021 起草时再协商
- **R3-D1.2** 产品负责人签 Go 时须同步记录 `prd_patch_pr: <PR号 | "N/A">`; 缺失或空字符串 → m0-handoff.yaml schema 校验 fail → US-020 **不能关闭**
- **R3-D1.3** US-021 task-planner 启动前置: `prd_patch_pr != null && (prd_patch_pr == "N/A" || PR.merged == true)`; 否则 **hard block**
- **R3-D1.4** 原子性保证: schema 强制 + task-planner 启动闸门双保险, 消除 0-3 工作日 governance 真空窗口

#### R3-D2 T1 No-Go 下 T2 产出处置 (R2-C-Q3)

- **R3-D2.1** T2 NFS 报告 **部分有效**: 路径 / 挂载行为 / md5 校验结论是基础设施事实, 不依赖合规结论, 保留进入 R8 降级路径 (CLI-only 仍需 `/opt/aria-outputs/`)
- **R3-D2.2** T2 中涉及 GLM 数据流 / luxeno 路径假设的章节须在 M0 Report 中以 **strikethrough 标注** "T1 No-Go 后失效"
- **R3-D2.3** 重测成本 = 0, 文档标注成本 ~0.5h, 计入 T6 (T6: 7h → 7.5h)

#### R3-D3 US-020 头部 Estimated 同步 (R2-C-C3)

- **R3-D3.1** 收敛后必须立即修订 US-020.md 第 11 行: `Estimated: ~95h / 2 weeks` → `Estimated: ~96.5h / 2 weeks (Core 86.5h + Buffer 10h)`
- **R3-D3.2** 修订责任归 knowledge-manager, 列入后续 OpenSpec tasks.md 第一条

#### R3-D4 差异清单 MECE 修复 (R2-C-C4)

- **R3-D4.1** R1-D2.1 (Day 0.5 前置闸门) 从 Round 2 "变化条目" 移至 "撤回条目", 注明 "被 R2-D2.3 实质替代为 Day 0–1 + 状态机"
- **R3-D4.2** R1-D5 系列确认已全部进撤回清单, 无遗漏

#### R3-D5 R9 硬闸门签字治理 (R2-C-L1)

- **R3-D5.1** M0 Report 新增必填章节 `## R9 官方回应状态`, 三态: `received` / `pending` / `declined`
- **R3-D5.2** M1 启动前置规则:
  - `received` → 直接进入 US-021
  - `pending` → 产品负责人**显式签字** "法律风险自承诺下继续", 签字记入 `m0-handoff.yaml.r9_status: pending` + `r9_signoff: {name, date, statement}`
  - `declined` → 强制 R8 降级路径
- **R3-D5.3** 无签字隐性推进 → audit-engine pre_merge 阶段 **hard block**

#### R3-D6 Aether 节点归属查证 (R2-C-L6)

- **R3-D6.1** T1 新增子任务 +0.5h: 查证 Aether heavy 节点物理归属 (10CG 自有 / 第三方托管)
- **R3-D6.2** 若非 10CG 自有 且无 DPA → 升级为 **R10 风险项**, 进入 R9 同款签字流程
- **R3-D6.3** T1 工时: 4h → **4.5h** (范围: license 1.5 + GLM ToS 0.5 + luxeno 0.5 + 跨境提示 1 + docker pull 审计 0.5 + Aether 归属 0.5)
- **拒绝 legal-advisor R2-C-L5 的 T1=5h 主张**: 跨境合规明确缩范围为"风险提示, 不做深度审", 4.5h 已触底; 若执行时发现超时, 由 R2-C-L5 原建议 (ad-hoc 法律咨询) 托底

#### R3-D7 T2 隐藏工时修订 (R2-C-C2)

- **R3-D7.1** T2 工时: 4h → **4.5h**, 增量原因 "+0.5h: Nomad agent UID 推断 + md5 双向比对 (R2-D6.1 新增操作步骤, 非零工时)"
- **R3-D7.2** 缓冲池 10h 不变

#### R3-D8 Dockerfile 构建时检验技术栅栏 (R2-C-L4)

- **R3-D8.1** T3 Dockerfile 末部加构建时门控:
  ```dockerfile
  ARG DEPLOY_ENV=internal
  RUN [ "$DEPLOY_ENV" = "internal" ] || { echo "ERROR: aria-runner must not be deployed outside 10CG Lab private cluster"; exit 1; }
  ```
- **R3-D8.2** 外部构建未传 `--build-arg DEPLOY_ENV=internal` → fail-fast
- **R3-D8.3** T3 工时 10h 不变 (在 T3 Dockerfile 范围内, 10h 已含此项的缓冲)

#### R3-D9 GLM smoke test 失败样本归档 (R2-C-Q4)

- **R3-D9.1** 归档路径: `aria-plugin-benchmarks/ab-suite/glm-smoke/failed-samples/<timestamp>-<seq>.yaml`
- **R3-D9.2** Schema: `{prompt, failure_mode, raw_output, expected_grep, glm_model_version}`
- **R3-D9.3** `failure_mode` 枚举: `not_triggered | triggered_empty_yaml | triggered_invalid_yaml | timeout`
- **R3-D9.4** 强制归档**全部 5 条样本** (含 pass), 便于 GLM 版本回归对比; 产出 `summary.yaml` 含索引
- **R3-D9.5** T3 验收新增: smoke run 必须产出 `summary.yaml`

#### R3-D10 Fixture 合成方法论 - 模板法 (R2-C-L2)

- **R3-D10.1** Fixture **强制走模板法**: `aria-plugin-benchmarks/ab-suite/glm-smoke/templates/{issue,code}.j2.md`
- **R3-D10.2** 占位符仅通用变量: `{lang} {framework} {action_verb}`
- **R3-D10.3** **禁止从真实仓库采样**, **禁止匿名化真实代码** (匿名化 ≠ 去识别化, 业务逻辑纹理无法清洗)
- **R3-D10.4** Spike 启动前 ai-engineer + legal-advisor **二审模板**, 签字进 `templates/REVIEW.md`
- **R3-D10.5** 模板示例: `def {func_name}(items): return [x for x in items if {predicate}]` (通用 Python 习语, 无业务语义)

#### R3-D11 依赖扫描工具 (R2-C-L3)

- **R3-D11.1** JS: `license-checker --production --json` (transitive) + `npm ls --all` 交叉验证
- **R3-D11.2** Python: `pip-licenses --format=json --with-system` (含 transitive)
- **R3-D11.3** Spike Report 列出 **direct + transitive 全表**, GPL/AGPL/LGPL 单列高亮
- **R3-D11.4** 不引入 FOSSA / Black Duck (M0 不申请商业 license; `license-checker` + `pip-licenses` 已覆盖 transitive 深度)
- **R3-D11.5** Spike 验收新增: GPL/AGPL transitive count > 0 → **fork 路径自动降级**

#### R3-D12 安全系数维持 ×1.5 (R2-C-Q1 内部分歧 orchestrator 裁决)

讨论组内部分歧:
- **backend-architect**: 拒绝动态, 维持 ×1.5, velocity 作为 Spike Report 附录数据
- **ai-engineer**: 部分接受动态分档 (150/400 commits/月)

**Orchestrator 裁决: 采纳 backend-architect 版本**
- **R3-D12.1** 系数 **固定 ×1.5**, 不引入动态分档
- **R3-D12.2** Spike Report 强制记录 `upstream_velocity` 字段: `git log --since="6 months ago" --oneline upstream/main | wc -l` ÷ 6
- **R3-D12.3** Velocity 数据透明化, 产品负责人在裁决时可主观上调系数 (Go-with-Revision PR 中记录)
- **裁决依据**: 动态系数本身引入新无依据常数 (150/400 切换点), 操作协议更复杂, 不改善 binding 质量。透明化 + 产品负责人主观裁量更符合 Aria "可追溯决策" 原则

### Round 3 工时重新基线

| Task | R2 | R3 | 变化 |
|---|---|---|---|
| T1 | 4h | **4.5h** | +0.5h (Aether 归属查证) |
| T2 | 4h | **4.5h** | +0.5h (md5 + UID 诚实标注) |
| T3 | 10h | **10h** | 不变 (Dockerfile ARG+RUN 含) |
| T4 | 52h | **52h** | 不变 |
| T5 | 8h | **8h** | 不变 |
| T6 | 7h | **7.5h** | +0.5h (T1 No-Go 下 T2 strikethrough 标注) |
| **Core** | 85h | **86.5h** | +1.5h |
| Buffer | 10h | **10h** | 不变 |
| **Total** | **95h** | **96.5h** | +1.5h |

### Round 3 讨论组与 Round 2 差异

- **变化**: 无 (R2-D* 所有条目 orchestrator 层面保留, R3 均为对挑战组反对的补充修订, 不推翻 R2 既有决策)
- **新增**: R3-D1 ~ R3-D12 (12 条, 均为 R2 挑战组反对的回应)
- **内部裁决**: R3-D12 (orchestrator 判定采纳 backend-architect)
- **拒绝挑战**: R2-C-L5 (T1 应 5h) — 维持 4.5h, 理由如 R3-D6.3

### 预期收敛

- Round 3 讨论组全部接受 Round 2 挑战组反对 (13 条中 12 条实质采纳, 1 条 R2-C-L5 明确拒绝并给出理由)
- 预期 Round 3 挑战组仅能对 R3-D12 (内部裁决) 与 R2-C-L5 的拒绝复议, 若无新反对 → 收敛
- 进入 Round 3 挑战组

### Round 3 挑战组反对意见

**qa-engineer 反对** (4 条):
- **R3-C-Q1** 【R3-D12.3】产品负责人主观上调无上限约束。建议: 上调 >×2.0 须附 velocity 数据佐证 + 第二签字人 (tech-lead)
- **R3-C-Q2** 【R3-D1.3】`PR.merged == true` 查询 API 未明。建议: tasks.md 明确 task-planner 调用 `forgejo GET /repos/.../pulls/{pr_num}` 并断言 `.merged == true`
- **R3-C-Q3** 【R3-D9.3】`failure_mode` 枚举不 MECE: GLM partial_response (HTTP 200 + JSON 截断) 既非 timeout 也非 invalid_yaml。建议: 补 `partial_response` 第 5 值
- **R3-C-Q4** 【R3-D11.5】LGPL 处理死角: R3-D11.3 高亮但 R3-D11.5 仅 GPL/AGPL 自动降级。建议: LGPL transitive>0 → legal-advisor 人工研判, 不自动降级
- qa 接受: R3-D6.3 (4.5h 复议通过) / R3-D10.4 (agent 签字是 audit trail 非法律行为) / R3-D2 / R3-D3 / R3-D4 / R3-D5 / R3-D7 / R3-D8

**code-reviewer 反对** (2 主 + 2 小):
- **R3-C-C1** 【R3-D1.1 schema 缺口】遗漏 `glm_smoke_passed: bool` (R3-D9 产出未被 handoff 引用) + `image_sha256` (R3-D8 构建结果无 pin)。建议: schema 补这 2 字段
- **R3-C-C2** 【R3-D12 orchestrator 越权】Aria 规范未授予 orchestrator 在技术分歧上的独立裁决权。建议: orchestrator 给推荐方案, 24h 内产品负责人确认, 而非"裁决已定"
- **R3-C-C3** (小) R3-D9.4 归档 schema 缺 `status: pass|fail` 字段
- **R3-C-C4** (小) R3-D2.2 strikethrough 执行主体未明, T6 验收需明确触发条件执行人
- code-reviewer 接受: R3-D3 / R3-D4 / 总体不需重写 US-020 v2 (差异清单已可追溯)

**legal-advisor 反对** (4 实质 + 接受拒绝 R2-C-L5):
- **R3-C-L1** 【R3-D6.3 Legal Memo 缺口】"跨境合规缩范围为风险提示"须在 OpenSpec 显式定义受限范围。建议: T1 产出须含 "受限范围 Legal Memo"
- **R3-C-L2** 【R3-D5.2 签字法律效力澄清】"法律风险自承诺下继续" 不构成法律意见且不转移风险, 仅为决策记录。建议: 明确 "签字非法律豁免, 仅作决策可追溯"
- **R3-C-L3** 【R3-D10.4 fixture 二审】AI agent 签字不构成法律意见 (无法律主体资格)。建议: 改为 "ai-engineer + legal-advisor 二审, **legal-advisor (人类) 最终签字**"
- **R3-C-L4** 【R3-D8 Dockerfile 栅栏"必要不充分"】栅栏防误用但不构成对第三方的合规声明; 外部用户绕过栅栏则免责声明失效。建议: 技术栅栏 + README warning **并行维护**
- **R3-C-L5** (小) 【R3-D11.4 license-checker 覆盖盲区】社区工具依赖 SPDX 数据库, 私有/冷门 license 可能漏检。建议: 扫描发现 unknown license → 人工 code review + 法律咨询
- **legal 明确接受 R3-D6.3 T1=4.5h 拒绝** (wall-clock 3-3.5h + 1h 缓冲合理), R2-C-L5 争议消解
- legal 免责声明保留: "本评审不构成正式法律意见"

### Round 3 收敛判定

- 讨论组共识: 与 Round 2 显著不同 (R3-D1~D12 新增 12 条)
- 挑战组反对: **11 条** (qa 4 / code 2主+2小 / legal 4+1小, 但均为 refinement 非结构性)
- **关键**: R2-C-L5 争议消解, 无新 structural 反对, 全部为字段补充与表述澄清
- **未收敛**, 进入 Round 4 (预期 R4 全部接受后收敛)

---

## Round 4

### 讨论组共识 (全部 13 条接受, 无内部冲突)

#### R4-D1 Velocity 上调第二签字人 (R3-C-Q1)
若产品负责人上调 velocity 阈值 > 历史基线 ×2.0, 须 (a) 附最近 2 个 sprint 的 velocity 数据快照, (b) 由 **tech-lead 作为第二签字人** 在 decision log 中 co-sign; 缺一项则上调无效, 阈值回落至 ×2.0 上限。

#### R4-D2 Forgejo API 调用细节 (R3-C-Q2)
tasks.md handoff 校验步骤明确: task-planner 调用 `forgejo GET /repos/10CG/Aria/pulls/{pr_num}`, 解析 JSON 断言 `.merged == true && .state == 'closed'`; 任一不满足则 handoff 阻塞, 不得仅凭 branch 状态推断。

#### R4-D3 handoff schema v1.1 补字段 (R3-C-C1)
`m0-handoff.yaml` schema v1.1 在 `outputs` 节补:
- `glm_smoke_passed: bool` (R3-D9 GLM smoke 结果, 缺省 false 视为未验证)
- `image_sha256: string` (R3-D8 Docker 构建产出, 必填, 用于下游 pin 复现)
- 二者缺失 → audit-engine pre_merge **阻断**

#### R4-D4 Orchestrator 裁决权收回 (R3-C-C2)
撤回 "orchestrator 独立裁决权" 表述。新规则: 技术分歧出现时, orchestrator 输出 **推荐方案 + 备选 + 风险对比**, 进入 **24h 产品负责人确认窗口**; 超时未确认则按推荐方案执行并记录 `silent-approval` (decision log 条目)。此规则仅适用 US-020 内部, **不同步到 `standards/`** (非跨项目方法论)。在 US-020 §D 末尾新增一行约束。

#### R4-D5 T6 Strikethrough 执行主体 (R3-C-C4)
tech-lead + knowledge-manager 互补方案合并:
- **执行方**: T1 出具 No-Go 结论后, **knowledge-manager** 在 M0 Report 中对 T2 涉及 GLM/luxeno 路径的章节执行 strikethrough 标注, 标注处注明 "T1 No-Go 后失效, 日期:{date}"
- **验证方**: **phase-c-integrator 在 pre_merge 检查点** 验证 strikethrough 已完成; 失败则 block PR, 由 task-planner 回写 tasks.md 状态

#### R4-D6 T1 受限范围 Legal Memo (R3-C-L1)
T1 产出物追加 "受限范围 Legal Memo", 必含:
(a) 评估覆盖的司法辖区清单
(b) 明确未覆盖区域
(c) 风险提示 vs 合规结论的边界
(d) 失效条件 (法规变更 / 业务扩张)
(e) 本次覆盖的 5 项范围: license / GLM ToS / luxeno / Aether 归属 / docker pull; 超出范围须单独立项

模板归档 `standards/legal/scoped-memo-template.md` (新增)

#### R4-D7 签字语言统一表述 (R3-C-L2)
所有签字位的 footer 统一为:
> **"本签字仅作为决策可追溯记录 (audit trail), 不构成法律豁免、责任转移或正式法律意见。"**

替换 R3-D5.2 的 "风险自承诺" 措辞。同步应用到 `r9_signoff`, `pd_signoff`, 以及所有 decision log 条目。

#### R4-D8 Dockerfile 栅栏 + README warning 并行 (R3-C-L4)
T3 Dockerfile 在 R3-D8 构建时门控 (`ARG DEPLOY_ENV=internal`) 基础上, 额外要求 **README.md 头部独立维护** WARNING block:
- "本镜像仅供 10CG Lab 私有集群内部使用"
- "绕过 `--build-arg DEPLOY_ENV=internal` 强制构建属于违规, 作者不承担任何合规责任"
- 版本日期 + 对应 Dockerfile commit SHA

技术栅栏 + 书面声明并行, 互不替代。T3 工时 10h 不变 (已含 README 修订缓冲)。

#### R4-D9 Unknown license 处理 (R3-C-L5 → R3-D11.6)
R3-D11 补第 6 条 **R3-D11.6**:
- `license-checker` 输出 `"Unknown"` 或 `pip-licenses` 输出 `"UNKNOWN"` 的包不得通过自动评估
- **必须触发人工 code review** (由 ai-engineer 完成源码 LICENSE 文件核查) + **legal-advisor (人类) 人工法律咨询** 后方可放行
- R3-D11.5 的 GPL/AGPL 自动降级规则扩展覆盖 unknown (unknown 与 GPL/AGPL **同等对待**, 进入人工通道)
- Spike Report direct+transitive 全表新增 `unknown_count` 汇总行, ≥1 即阻断验收

#### R4-D10 failure_mode 枚举扩展 (R3-C-Q3)
`failure_mode` 5 值: `not_triggered | triggered_empty_yaml | triggered_invalid_yaml | partial_response | timeout`
- `partial_response` 定义: Skill 触发且返回非空 YAML, 但缺失必填字段 (如 `verdict` / `evidence_refs`) 或 evidence 引用解析失败
- 判定优先级: `timeout > invalid_yaml > partial_response > empty_yaml > not_triggered`

#### R4-D11 LGPL 人工研判 (R3-C-Q4)
LGPL transitive > 0 **不再自动降级**。改为:
- license-checker 输出 `flag: lgpl_transitive_detected` + transitive 依赖路径
- 路由至 **legal-advisor (人类)** 人工研判
- 人类 verdict 写回 fixture metadata
- Agent 不得擅自判定 LGPL 传染性边界

#### R4-D12 Fixture 人类 legal 最终签字 (R3-C-L3)
R3-D10.4 修订: "ai-engineer + legal-advisor 二审模板, **legal-advisor (人类) 最终签字**后方可写入 `templates/REVIEW.md`; AI agent 意见仅供参考, 不构成法律审查结论。"

Fixture metadata schema 增加 `human_signoff_required: true` 字段; `signed_by: human:<name>` (法律责任主体), `reviewed_by: agent:legal-advisor` (audit trail, 不构成放行依据)。

#### R4-D13 R3-D9 归档 status 字段 (R3-C-C3)
R3-D9 schema 增加 `status: pass | fail`:
- `status=pass` 当且仅当 `failure_mode=null` 且所有必填字段完整
- 否则 `status=fail` 并强制填写 `failure_mode`
- 便于归档目录快速过滤失败用例

### Round 4 工时基线 (与 R3 相同)

| Task | R3 | R4 | 说明 |
|---|---|---|---|
| T1 | 4.5h | **4.5h** | R4-D6 Legal Memo 在原 4.5h 范围内 |
| T2 | 4.5h | **4.5h** | 不变 |
| T3 | 10h | **10h** | R4-D8 README 在 Dockerfile 范围内 |
| T4 | 52h | **52h** | 不变 |
| T5 | 8h | **8h** | 不变 |
| T6 | 7.5h | **7.5h** | R4-D5 执行主体明确, 工时不变 |
| **Core** | 86.5h | **86.5h** | 不变 |
| Buffer | 10h | **10h** | 不变 |
| **Total** | **96.5h** | **96.5h** | 不变 |

### Round 4 讨论组与 Round 3 差异

- **变化**: 无结构性变化 (R4-D* 均为 R3-D* 的精细化补充)
- **新增**: R4-D1 ~ R4-D13 (13 条, 全部采纳 Round 3 挑战组 11 条反对 + 2 条整合)
- **撤回**: R3-D12 orchestrator 独立裁决权表述 (被 R4-D4 替代为推荐 + 24h 确认)
- **内部冲突**: 0 (R4-D5 tech-lead + knowledge-manager 互补方案合并)
- **拒绝挑战**: 0 (Round 3 挑战组 11 条全部接受)

### 预期收敛

Round 4 讨论组全部接受 Round 3 挑战组反对 (11 → 13 条精细化修订), 无新结构性变更, 无 structural 分歧。预期 Round 4 挑战组:
- **应无新反对**, 或仅有可忽略的格式性建议
- 如确认, **Round 4 收敛**, 进入工件起草

进入 Round 4 挑战组。

### Round 4 挑战组判定

**qa-engineer**: R4-D1/D2/D10/D11 全部接受, **最终表态: 无反对意见**
**code-reviewer**: R4-D3/D4/D13/D5 全部接受, **最终表态: 无反对意见**
**legal-advisor**: R4-D6/D7/D12/D8/D9 全部接受, **最终表态: 无反对意见** (保留"本评审不构成正式法律意见"免责)

### Round 5 (逻辑性收敛)

- Round 4 挑战组 **0 条反对**
- 逻辑推断: Round 5 讨论组无需任何修改 → Round 5 讨论组共识 == Round 4 → Round 5 挑战组仍无反对
- **无需 spawn agents**, 通过传递性收敛: Round 4 讨论组共识 (R4-D1~D13 + Round 3 继承 R3-D1~D12, Round 2 继承 R2-D1~D7) 即为**最终共识**

### 收敛判定

✅ **收敛条件 1 满足**: Round 5 讨论组 (逻辑) == Round 4 讨论组
✅ **收敛条件 2 满足**: Round 4 挑战组 0 条反对
✅ **状态变更**: `in_progress` → `converged`

### 最终共识摘要 (供 US-020 修订和 OpenSpec 起草消费)

**工时基线** (Round 4 确定, 总 96.5h / 2 weeks):

| Task | 工时 | 主要变更来源 |
|---|---|---|
| T1 Legal 前置闸门 | 4.5h | R2-D2.1 / R3-D6.3 / R4-D6 |
| T2 NFS 实测 | 4.5h | R2-D6.1 / R3-D7 |
| T3 Dockerfile + plugin + GLM smoke | 10h | R2-D6.2/6.3/6.4 / R4-D8 |
| T4 Hermes Spike | 52h | R2-D4.1 |
| T5 AD1-AD12 收敛 | 8h | R1-D2.2 |
| T6 M0 Report + PRD patch | 7.5h | R2-D1.4 / R3-D2.3 |
| Core | 86.5h | |
| Buffer | 10h | |
| **Total** | **96.5h** | |

**关键机制**:
- `m0-handoff.yaml` schema v1.1 字段集 (R4-D3): `{go_decision, prd_patch_pr, r9_status, spike_code_path, nfs_path, image_tag, image_sha256, ad3_conclusion, glm_smoke_passed, r9_signoff?, pd_signoff}`
- 产品负责人 3 签字位: Go 决议 / R9 pending 确认 / >×2.0 velocity 上调 (后者需 tech-lead co-sign)
- 签字统一表述: "本签字仅作为决策可追溯记录 (audit trail), 不构成法律豁免、责任转移或正式法律意见"
- `prd_patch_pr` 非空是 US-021 启动硬前置
- R9 `pending` 且无人类签字 → audit-engine pre_merge hard block
- PRD patch PR timebox: 3 工作日, 超时冻结 US-021 启动

**Spike 裁决规则** (R2-D3 + R3-D11 + R3-D12 + R4-D1/D9/D11/D12):
- fork acceptable: 月度 rebase ≤ 20h × 1.5 系数 (×1.5 固定, >×2.0 上调需 tech-lead 第二签字)
- 自研 acceptable: `cloc` Python 业务 LoC ≤ 1000 (测试单列)
- license 扫描阻断: GPL/AGPL transitive > 0 或 unknown license count ≥ 1 → fork 自动降级
- LGPL transitive > 0 → 人类 legal-advisor 研判, 不自动降级
- 双 fail → R8 降级路径 (CLI-only)

**Dockerfile 治理** (R3-D8 + R4-D8):
- 构建时门控: `ARG DEPLOY_ENV=internal; RUN [ ... ] || exit 1`
- README.md warning block 并行维护 (日期 + commit SHA)
- fixture 合成必须走 `templates/*.j2.md`, 禁真实采样, 人类 legal 最终签字

**Go/No-Go 机制** (R2-D1 + R3-D1):
- 维持 PRD 原二元 Go/No-Go (不引入三态, 避 PRD 治理冲突)
- 如需局部修订 → 签 Go 时同步起草 `prd_patch_pr`, 3 工作日内合并, 否则冻结 US-021 启动
- orchestrator 技术分歧裁决改为 "推荐 + 24h 产品负责人确认 + silent-approval"

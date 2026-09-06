```
╔══════════════════════════════════════════════════════════════╗
║              PHASE A - PLANNING                              ║
╚══════════════════════════════════════════════════════════════╝
```

## 前置：跳过规则评估

按 Phase A 的跳过规则逐条判：

| 条件 | 检测结果 | 判定 |
|------|---------|------|
| 已有活跃 Spec | 扫 `openspec/changes/`，7 个活跃 Spec 全部是 aria-2.0 M6/M7 与 a1-entry 轨，**无 payment gateway 相关** | 不跳 A.1 |
| 复杂度 Level 1 | 支付网关集成涉及外部系统 / 资金 / 异步回调，远超「≤3 文件的简单修复」 | 不跳 A.1 |
| 已有 detailed-tasks.yaml | 无对应文件 | 不跳 A.2 / A.3 |
| emergency hotfix lane | 当前不在 `hotfix/*` 分支，非 prod 紧急修复 | 不适用 |

结论：**A.1 / A.2 / A.3 全部执行**。

## 关于 working tree dirty 的处理

state-scanner 报的「3 个文件未提交、工作树脏」不阻塞 Phase A —— A.1-A.3 只产出 `openspec/` 下的规划文档，不碰这 3 个文件。但它会在 **B.1 建分支时**变成问题：带着无关的未提交改动切分支，这些改动会跟着进新分支，最后混进本 Spec 的提交里。

我的建议是在进 Phase B 之前先把它清掉，二选一：

1. 这 3 个改动属于别的工作 → 先 commit 到当前分支，或 `git stash` 挂起
2. 这 3 个改动是废弃的试验 → 确认后 `git checkout --` 丢弃

我先把 Phase A 跑完，Phase B 开始前会再问你一次这 3 个文件怎么处理。

---

## 🚀 执行中

```
  ✅ A.1 完成 → Spec: add-payment-gateway-integration (draft, Level 3)
  ⏸️ A.post 审计 → post_spec = convergence (enabled)，待跑
  ✅ A.2 完成 → 任务数: 7
  ✅ A.3 完成 → Agent 已分配
```

### A.1 — Spec 管理（spec-drafter）

新建 Spec：`add-payment-gateway-integration`，**Level 3**（proposal.md + tasks.md）。

定 Level 3 而不是 Level 2 的理由：
- 涉及外部第三方系统，有 webhook / 幂等 / 对账几个彼此独立的子问题
- 涉及资金，失败模式必须在规划期显式设计，不能留到实现期临场决定
- 预计任务数 > 4，跨数据模型 / API / 安全多个面

proposal 里钉死的 4 条设计决策（这几条是后面所有任务的承重点）：

- **DEC-1 支付状态机单向不可逆** — `created → pending → (succeeded | failed | expired)`，终态不可再迁移。回调乱序到达时按「终态优先、同态幂等」处理，防止 succeeded 被迟到的 pending 回调覆盖。
- **DEC-2 幂等键落库唯一索引** — 以网关事件 id 建唯一索引，重复回调靠数据库约束拒绝。应用层判重在并发下有 TOCTOU 窗口。
- **DEC-3 webhook 先落库再处理** — 收到回调先写原始事件表并立即返回 2xx，业务处理异步进行，避免业务异常引发网关重试风暴。
- **DEC-4 金额用整数最小货币单位** — 一律整数（分），币种独立字段，不用浮点。

验收标准（可证伪，不是「支付能用」这种不可测量的表述）：

- AC-1 沙箱完成一笔成功支付，终态为 `succeeded`
- AC-2 同一 webhook 事件重复投递 3 次 → 数据库只有 1 条事件记录，业务状态不变
- AC-3 篡改 webhook payload → 验签失败返回 4xx 且零状态推进
- AC-4 模拟回调完全丢失 → 兜底查询任务在 N 分钟内把状态修正为终态
- AC-5 全仓 grep 不到任何硬编码网关密钥

范围外（后续独立 Spec）：退款 / 多网关路由降级 / 订阅周期扣款 / 财务结算报表。

### A.post — post_spec 审计（audit-engine）

读 `.aria/config.json`：`audit.enabled = true`，`checkpoints.post_spec = "convergence"`，`max_rounds = 5`。

**这个检查点是 enabled 的，我不会自行跳过**（Rule #10：已启用的闸门是 owner 的配置决定，「Spec 还行 / 性价比不高」不构成豁免理由）。审计团队按配置为：`tech-lead` / `backend-architect` / `qa-engineer` / `code-reviewer` / `knowledge-manager`。

审计需要跑完并拿到 PASS 或 PASS_WITH_WARNINGS 才能正式进 A.2；下面的任务分解是先给你看的草案，如果审计出 FAIL，我会按报告修 Spec 再重跑 A.2。

### A.2 — 任务规划（task-planner）

7 个任务，粒度 4-8h：

| ID | 任务 | 估算 | 依赖 |
|----|------|------|------|
| TASK-001 | 支付数据模型与状态机（3 张表 + 迁移函数 + 唯一索引） | 5h | — |
| TASK-002 | PaymentGateway 抽象接口（含 fake 实现供测试注入） | 4h | — |
| TASK-003 | 网关厂商适配实现 + 凭据配置（env 缺失即 fail-closed） | 6h | TASK-002 |
| TASK-004 | 支付发起 API（`POST /payments`、`GET /payments/{id}`） | 5h | TASK-001, TASK-002 |
| TASK-005 | Webhook 接收与幂等处理（验签 → 落库 → 2xx → 异步消费） | 7h | TASK-001, TASK-003 |
| TASK-006 | 对账兜底查询任务（非终态超时主动查询修正） | 5h | TASK-003, TASK-005 |
| TASK-007 | 端到端验收与安全核验（AC-1~AC-5 + grep 密钥） | 6h | TASK-004~006 |

合计约 38h。

### A.3 — Agent 分配（task-planner）

| 任务 | Agent | 理由 |
|------|-------|------|
| TASK-001 ~ TASK-006 | `aria:backend-architect` | 数据模型 / 服务边界 / API 设计，全在单系统后端范围内 |
| TASK-007 | `aria:qa-engineer` | 端到端验收与失败分支覆盖属测试策略与风险评估，不是逐提交代码审查 |

并行轨划分（按文件域 disjoint，同文件域串行）：

- **track_1**: TASK-001 → TASK-004（`models/` + `api/payments`）
- **track_2**: TASK-002 → TASK-003 → TASK-005 → TASK-006（`services/payment/` + `workers/`）
- **串行尾**: TASK-007（需全部前置产物就位）

TASK-001 与 TASK-002 文件域不重叠，可同时起。

---

## 📤 上下文输出

```yaml
success: true
steps_executed: [A.1, A.2, A.3]
steps_skipped: []
pending: [A.post]          # post_spec 审计待跑 (convergence, 5 agents)

context_for_next:
  spec_id: add-payment-gateway-integration
  spec_level: 3
  spec_status: draft        # 需 approve 后才进 Phase B
  task_count: 7
  task_list: [TASK-001 ... TASK-007]
  assigned_agents:
    TASK-001~006: aria:backend-architect
    TASK-007: aria:qa-engineer
  ready_for: Phase B (阻塞于两项，见下)
```

产物已写入：

- `proposal.md`（Level 3 主文档）
- `tasks.md`（7 任务清单）
- `detailed-tasks.yaml`（含 agent 分配与并行轨）

---

## 进 Phase B 前的两个待办

1. **post_spec 审计要跑完** — 配置里是 enabled + convergence，不是可选项。
2. **那 3 个未提交文件要处置** — 告诉我是 commit、stash 还是丢弃，我再执行 B.1 建分支。

另外 Spec 现在是 `draft`，需要你 approve 后才能进入实现。要我现在就起 post_spec 审计吗？

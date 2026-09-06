# Change: add-payment-gateway-integration

> **Level**: 3 (proposal.md + tasks.md)
> **Status**: draft (待 approve)
> **Created**: 2026-09-05

## Why

当前系统没有支付能力，所有涉及收款的业务流程都需要线下处理。引入支付网关集成后，可以在产品内完成下单 → 支付 → 对账闭环。

选择 Level 3 的理由：
- 涉及外部第三方系统（支付网关），有 webhook / 回调 / 幂等 / 对账等多个独立子问题
- 涉及资金，失败模式必须显式设计（不能靠"以后再补"）
- 预计任务数 > 4，跨 backend / 数据模型 / 安全多个面

## What Changes

### 新增能力

1. **支付网关适配层** — 抽象 `PaymentGateway` 接口，首个实现对接选定的网关厂商；调用方不直接依赖厂商 SDK。
2. **支付单据模型** — `PaymentIntent` / `PaymentTransaction` 两级模型，记录金额、币种、状态机、外部单号。
3. **支付发起 API** — 创建支付单并返回前端所需的支付凭据（如 client_secret / 跳转 URL）。
4. **异步回调处理** — 接收网关 webhook，验签 → 幂等去重 → 状态机推进。
5. **对账与查询** — 主动查询网关订单状态，用于回调丢失时的兜底补偿。
6. **凭据管理** — 网关 API key / webhook secret 走环境变量，不入库不入仓（Rule #7）。

### 不在本次范围

- 退款 / 部分退款（后续独立 Spec）
- 多网关路由与降级
- 订阅制 / 周期扣款
- 财务报表与结算

## Impact

| 面 | 影响 |
|----|------|
| 数据库 | 新增 2 张表 + 状态枚举；无既有表结构破坏性变更 |
| API | 新增 `POST /payments`、`GET /payments/{id}`、`POST /webhooks/payment` |
| 配置 | 新增 4 个环境变量（gateway base URL / api key / webhook secret / 环境标识） |
| 安全 | webhook 验签为强制项；密钥只走环境变量 |
| 向后兼容 | 纯新增，无破坏性变更（PATCH/MINOR 级） |

## Design Decisions

**DEC-1 支付状态机为单向不可逆**
`created → pending → (succeeded | failed | expired)`。终态不可再迁移，回调乱序到达时按"终态优先、同态幂等"处理，避免 succeeded 被迟到的 pending 回调覆盖。

**DEC-2 幂等键落库唯一索引，而非应用层判重**
以网关事件 id 建唯一索引，重复回调靠数据库约束拒绝。应用层判重在并发下有 TOCTOU 窗口。

**DEC-3 webhook 先落库再处理**
收到回调先写入原始事件表并立即返回 2xx，业务处理异步进行。避免业务异常导致网关重试风暴。

**DEC-4 金额用整数最小货币单位**
金额字段一律整数（分），不用浮点。币种独立字段。

## Risks

| 风险 | 缓解 |
|------|------|
| 回调丢失导致订单永久 pending | 定时主动查询兜底（TASK-005） |
| 沙箱与生产行为差异 | 验收必须在沙箱跑通全部状态分支，含失败与超时 |
| 密钥泄漏 | Rule #7：写入/读取命令 redirect output，验证只看 metadata |
| 验签实现错误导致伪造回调 | 验签为独立单测对象，含负控（篡改 payload 必须被拒） |

## Acceptance Criteria

- AC-1 沙箱环境下完成一笔成功支付，`PaymentTransaction` 终态为 `succeeded`
- AC-2 同一 webhook 事件重复投递 3 次，数据库只产生 1 条事件记录，业务状态不变
- AC-3 篡改 webhook payload 后验签失败，返回 4xx 且不推进任何状态
- AC-4 模拟回调完全丢失，兜底查询任务在 N 分钟内把状态修正为终态
- AC-5 代码库中 grep 不到任何硬编码的网关密钥字面量

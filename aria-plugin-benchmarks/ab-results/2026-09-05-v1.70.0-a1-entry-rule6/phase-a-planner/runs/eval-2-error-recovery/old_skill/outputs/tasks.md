# Tasks: add-payment-gateway-integration

> 共 7 个任务，粒度 4-8h。依赖关系见每项 `依赖` 行。

## TASK-001 支付数据模型与状态机
- [ ] 定义 `PaymentIntent` / `PaymentTransaction` / `PaymentWebhookEvent` 三张表
- [ ] 金额用整数最小货币单位 + 独立币种字段（DEC-4）
- [ ] 状态机迁移函数：非法迁移抛异常，终态不可逆（DEC-1）
- [ ] webhook 事件表以网关事件 id 建唯一索引（DEC-2）
- 依赖: 无
- 估算: 5h

## TASK-002 PaymentGateway 抽象接口
- [ ] 定义接口：`create_intent` / `query_order` / `verify_signature`
- [ ] 定义统一异常类型（网络错误 / 业务拒绝 / 验签失败 分开）
- [ ] 提供内存 fake 实现供测试使用
- 依赖: 无（可与 TASK-001 并行）
- 估算: 4h

## TASK-003 网关厂商适配实现 + 凭据配置
- [ ] 实现 TASK-002 接口的真实厂商适配
- [ ] 4 个环境变量读取，缺失时启动即失败（fail-closed）
- [ ] 遵守 Rule #7：任何涉及 key 的命令 redirect output，验证只看 metadata
- 依赖: TASK-002
- 估算: 6h

## TASK-004 支付发起 API
- [ ] `POST /payments` 创建 intent 并返回前端支付凭据
- [ ] `GET /payments/{id}` 查询状态
- [ ] 入参校验：金额正整数、币种白名单
- 依赖: TASK-001, TASK-002
- 估算: 5h

## TASK-005 Webhook 接收与幂等处理
- [ ] `POST /webhooks/payment`：验签 → 落原始事件 → 立即 2xx（DEC-3）
- [ ] 异步 worker 消费事件推进状态机
- [ ] 唯一索引冲突走幂等路径，不报错
- 依赖: TASK-001, TASK-003
- 估算: 7h

## TASK-006 对账兜底查询任务
- [ ] 定时扫描超过阈值仍为非终态的 intent
- [ ] 主动调 `query_order` 修正状态
- [ ] 修正动作写审计日志
- 依赖: TASK-003, TASK-005
- 估算: 5h

## TASK-007 端到端验收与安全核验
- [ ] 沙箱跑通 AC-1 ~ AC-4 全部分支（含失败 / 超时 / 乱序回调）
- [ ] 验签负控：篡改 payload 必须被拒（AC-3）
- [ ] 全仓 grep 确认无硬编码密钥（AC-5）
- 依赖: TASK-004, TASK-005, TASK-006
- 估算: 6h

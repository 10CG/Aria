# post_spec FINAL — aria-2.0-m6-cost-model-telemetry (aggregated)

> **Checkpoint**: post_spec | **Verdict**: **CONVERGED** | **轨迹**: R1 (5-agent) → R1-fix → R2 (3-agent) → R2-fix → R3 (backend 单点 0 新)
> **审计对象**: `openspec/changes/aria-2.0-m6-cost-model-telemetry/{proposal.md,tasks.md}` + 决策 SOT `docs/decisions/DEC-20260709-001-layer2-cost-model-telemetry.md` v2
> **前置**: DEC 本身经 **4-agent code-grounded 设计审议** (2 OBJECTION [O1 served-not-intended / O2 返工路径] + 2 CONCERNS 折入, DEC §9)
> **日期**: 2026-07-09 | **主控**: main-loop (aria-runner-bot/023236f2)

## R1 (5-agent 并行: tech-lead / qa-engineer / ai-engineer / knowledge-manager / backend-architect)

全 REVISE, ~30 findings, **tech-lead 判定全属 spec-doc 层 (底层设计经 DEC 4-agent 已锁, 无需返工)**:
- **backend 2C**: commit-lint 求和无数据源 (裸文本无 stream-json) / cost.json 窗口锚点未选 (DEC 委派未转写)
- **qa 2C**: AC-3 CLAUDE_TIMEOUT vs ASSERTION_MISMATCH 非等价 (timeout flush 前提代码库从未验) / redo-changes 切 stream-json 静默毁 commit_message (质量回归无红)
- **tech-lead 5I**: dispatch_id 来源矛盾 / AC-10 自指不可证伪 / 窗口锚点未转写 / 兜底可见无 AC / 归档 vs AC-10 先后未表态
- **ai-engineer 3I**: served-model verbatim-echo 失效模式 (Luxeno 回显请求名则检测器结构失效) / commit-lint token 无捕获源 / redo-changes commit_message 提取源欠具体 + stderr 污染
- **km 4I**: AD 分配 (已避 10-12) / cutover-runbook §7「项 8」不存在 / dangling memory 引用 / CLAUDE.md「待起」过期

## R1-fix

proposal + tasks + CLAUDE.md 全折入: dispatch_id 钉死 (容器读 NOMAD_META_DISPATCH_ID) / 窗口锚点选与 metered_usd 同口径 / commit-lint R-6 二选一 / commit_message result 帧 .result 提取 + 回归断言 / served echo 失效模式入 R-1 + AC-10 独立 oracle + echo-contingency / 新增 AC-1b (fail-loud) + AC-11 (兜底可见) / 覆盖率状态位阈值 / 部分归档规则 / §Why 诚实前提精化 (intended 已抓 motivating, served 增量=服务端替换检测且以 ground-truth 为前提) / dangling memory 换真实条 / CLAUDE.md 去「待起」。

## R2 (3-agent 验证: tech-lead / backend / qa)

- **tech-lead: CONVERGED (modulo 机械同步)** — 0 新 Critical, R1 实质全折入, 新增内容 code-grounded 属实且高质量 (尤其 commit_message silent-regression 捕获); 唯 tasks 4.4 残留映射矛盾 (DELTA-1) + 2 minor tasks 漂移。
- **backend: REVISE (窄)** — 3/5 全闭 (窗口锚点/dataclass/migration); Finding A (tasks 4.4 未同步「删了没删」) + Finding B (commit-lint-retry.sh:127 同构 R-2 回归)。
- **qa: REVISE (轻, 0 Critical)** — 6/8 闭 (闭合质量超原建议); M-1 (served 一致性 flag 未落地) + D-1 (tasks 4.4) + minors。
- **三家共识**: 0 新 Critical, 残留全机械文本, 撞同一处 tasks 4.4。

## R2-fix

tasks 4.4 (删映射 + 求和挂 3.6 条件) / 3.6(a) commit-lint-retry.sh:127 (Finding B) / served 一致性降 known-limitation + OOS-6 (M-1) / 1.2 补删 .bak / 2.1 .result passthrough / 待核实 1-8 / 6.2 §7 最后项 / header AC 范围。

## R3 (backend 单点稳定性确认)

**CONVERGED** — 9 个 R2 残留检查点全部 HEAD 实文验证闭合 (3 处额外文件系统/正则独立核验: .bak 存在且含裸 claude / parse-stream-json 确不含 .result / AC 计数 12 精确); 0 新阻断; 唯 1 条诚实标注的弱耦合待决 (2.1 parser shape vs 3.6a jq, 属 A.2 拍板类, 不阻断)。

## 终态

proposal 12 AC (AC-1/1b/2..9/11/10) + tasks 8 Phase (Track-1 Layer1 独立 / Track-2 容器 gate input-delivery / Track-3 AC-10 gate Luxeno)。**待 owner 批准 → Phase A.2/A.3 detailed-tasks.yaml**。

## 关键设计诚实度提升 (审计驱动)

1. **served-model 检测器** (ai O1 精化): 只记 intended 是套套逻辑; served 增量价值 = 服务端替换检测, **且以 Luxeno 返 ground-truth 非 verbatim-echo 为前提** (R-1 失效模式 + AC-10 echo-contingency)。
2. **返工路径非盲区** (O2 + qa/backend): redo/changes/commit-lint 全纳入模型接线 + 遥测 (scope A); marker 全终态 emit 解耦 SUCCESS。
3. **硬前置诚实标注**: AC-10 (served==真跑) 卡 Luxeno Blocker 4, 「model 维度对 AC-6 可评分」条件于其解除 — Track-1 先归档不等于 168h cost 可评分。

## 反复出现的元教训 (本 session 3×)

「声称完成≠真做」: dangling memory (7-02 handoff §8 声称创建未写) + tasks 4.4 (proposal 写「删了」实未删, R2 三家撞到) → 待沉淀 memory。

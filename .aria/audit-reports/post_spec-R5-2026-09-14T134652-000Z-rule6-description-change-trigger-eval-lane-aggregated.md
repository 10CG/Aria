---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: false
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-14T17:05:00.000Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
---

# post_spec Round 5 聚合 (max_rounds 耗尽) — rule6-description-change-trigger-eval-lane

> 被审 SHA `f169a0b` (rework v5)。drift_guard 未配置 ⇒ `drift_check_skipped: true`。
> Sibling probe: 已完整扫描, 未发现同 issue 竞品。
> 观察条数 (只数顶层条目, 不进比较键): tech-lead 11 · qa-engineer 6 · code-reviewer 9 · backend-architect 6 · knowledge-manager 8。

## 审计结论 (去重: 按 {category, scope} 合并, scope 归一到章节锚)

### Critical
无。

### Major (6 个比较键)
1. [major] architecture/proposal.md §D1+§D4+§OQ-7 (issue) — 自主模式推荐由 (B) 改 (C) 后规范文本没跟上: SOT 自主条款只写「先在 GLM 上验证」、缺 (C) 的「无已审套件不改」; D4 仍无条件保留 (B) 的 provisional, 合规清单放行「pass provisional」ship; 「依 OQ-7 / OQ-9」「见 OQ-7」逐字转录后悬空 (tech-lead)。
2. [major] testing/proposal.md §D2 (issue) — 作废第二情形「输出缺 query 条目、runs 少于 3」不可达: `run_eval.py` 把异常、超时、`claude -p` 报错都记成一次「未触发」, `runs` 恒为 3; 环境故障因此落成 fail, 执行者会去改一份正确的 description (code-reviewer)。
3. [major] documentation/proposal.md §D6 (issue) — 待转录进 SOT §6 的句子仍引「RESULT.md v4」(v4 还带能力上限说法); 头部重核清单不含 §D6 (knowledge-manager; tech-lead minor 同键合并)。
4. [major] documentation/proposal.md §D1 (issue) — SOT §2 新句内嵌「依 OQ-7 / OQ-9 裁定, 裁定不同则随之改」, 逐字写入后成孤儿引用 (knowledge-manager; code-reviewer minor 同题)。
5. [major] testing/proposal.md §D1 (SOT §2 自主模式条款) (issue) — 删掉该整句, SC-1/2/3/5/7/9/10 仍全绿, 没有机械检查锁住这条最关键的新规则 (qa-engineer, 反事实实测; tech-lead 与 code-reviewer minor 同题)。
6. [major] architecture/proposal.md §D1+§OQ-7+§Impact (issue) — 「需要改时任务进 S_FAIL」缺机械触发路径: `_handle_s5_await` 推进到 S6 只看 Nomad alloc 的 exit_code, `initial.sh` 写入的 `CLAUDE_NO_OP` 结果在 hermes-extensions 零消费; Layer 2 若跳过 description 改动而完成其余部分, 整单多半报 SUCCESS (backend-architect)。

### Minor (4 个比较键)
7. testing/proposal.md §SC-1+§SC-7 — v5 新加三处规范文字无 SC (tech-lead)。
8. testing/proposal.md §Success Criteria — 同上 (code-reviewer)。
9. documentation/proposal.md §D1+§D6 — 同第 3、4 条 (code-reviewer)。
10. testing/proposal.md §D1 (SOT §3 边界注) — 写回旧边界注 SC-10 仍命中「不走本节」(qa-engineer, 反事实实测)。

## Verdict

PASS_WITH_WARNINGS — 0 critical / 6 major / 4 minor (去重后)。

## 轮次记录

| 轮 | 被审 | critical | major | minor | vote |
|---|---|---|---|---|---|
| R1 | `298d0e4` (v1) | 1 | 14 | 17 | 5 REVISE |
| R2 | `55bc9f3` (v2) | 0 | 10 | 26 | 3 REVISE / 2 PASS |
| R3 | `0c41e53` (v3) | 0 | 5 | 6 | 4 REVISE / 1 PASS |
| R4 | `e822829` (v4) | 0 | 3 | 4 | 3 REVISE / 2 PASS |
| R5 | `f169a0b` (v5) | 0 | 6 | 4 | 5 REVISE |

(R3 起非阻塞意见分进「观察」, minor 计数口径与 R1 / R2 不同。)

### Round 5
- Agents: 五席全部完成 (首批三席 + 空位补派两席)
- Sibling probe: 已完整扫描, 未发现同 issue 竞品
- Conclusions: 10 (另有观察 40 条)
- R4 对账各席合计: 全部 closed (tech-lead 4 / code-reviewer 3 / knowledge-manager 1; qa-engineer 与 backend-architect R4 零发现)
- Converged: false —— max_rounds = 5 已耗尽

## 未收敛原因分析

- R4 的 major 全部在 v5 关闭 (对账零 open), R5 的 6 条 major 全部是 v5 **新增文字**带出的: 自主模式条款的转录形状与机械通路 (1、4、5、6)、作废条件对 `run_eval.py` 真实行为的假设 (2)、换版漏改 (3)。
- 形状与 R3→R4 相同: 每轮修复引入的新文字, 在下一轮被找出同样幅度的新缺口; major 数 14 → 10 → 5 → 3 → 6, 最近一轮回升, 但问题范围持续收窄到转录措辞与运行时通路。
- 按收敛算法, R4 仍有 major ⇒ R5 的比较键结构上不可能与 R4 相等; 本轮耗尽 max_rounds 是预期内的 (R4 聚合已如实登记)。

## 降级策略裁定 (owner 2026-09-15)

owner 在三选一中选「增加轮次」: max_rounds 5 → 7 (本次审计实例内, 不改 `.aria/config.json` 的全局配置)。附带要求: 启动前先判断加轮次是否真在往收敛方向推进。

主控的判断 (已向 owner 汇报并获确认): R2–R5 的 major 绝大多数出自上一轮修复新写的文字, 其中 R3–R5 的 14 条有 7 条在自主模式这条线上 (Layer 2、OQ-7 选项、S_FAIL 通路、runner 退出码); 按 v6 原样跑 R6, 大概率仍冒新 major, R7 不可能收敛。据此 owner 确认两项前置:
1. **收窄范围**: 自主模式的细节移出本 spec, 只留一句禁令 (自主运行时不做 description 改动, 需要改时放弃整个任务、不提交任何改动, 并写明是哪个 skill、为什么要改); owner 给出的目标设计 (新失败类型不自动重试、告警带原因、Layer 1 拆单) 与全部已知缺口并入唯一一张跟进 issue, 硬前提为「须在这类任务派给 runner 之前落地」。
2. **R6 之前先自检**: 用审计席用过的机械检查 (SC 反事实模拟、转录内部编号扫描、新断言事实核对) 先过一遍 v7。

R6 若零 major, R7 不做任何改动 (minor 一律延后) 以争取收敛; R6 若仍有 major, 如实报 owner。

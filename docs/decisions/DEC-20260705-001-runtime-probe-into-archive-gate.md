# 决策: DEC-20260705-001 - 运行时探针集成进归档门 (泛化 coordination_probe 为归档门可选动态子检查)

> **日期**: 2026-07-05 | **模式**: technical (brainstorm) | **track**: aria-plugin 方法论轨 (#95 follow-up)
> **来源**: `/state-scanner` → owner 选「#95 探针泛化新周期」→ brainstorm technical mode
> **消费方**: spec-drafter (下一步据本 DEC 起草 `openspec/changes/` proposal.md)

---

## 背景

Aria 存在一类病根 **「归档 spec 勾选完成 ≠ 运行现实」**(aria-plugin #95): spec 归档时勾了「完成 ✅」, 但对应代码在生产里**从未被真正调用** = 挂着的死代码。

围绕此病根**已 ship 两个互补检查** (2026-07-05):

| 机制 | 维度 | 检查什么 | 出处 |
|------|------|----------|------|
| `spec_complete.py :: gate_result` | **静态** (归档时) | 符号有 Py 定义但生产**零语义引用** → block (tri-state block/warn/pass, fail-toward-warn) | #95 / DEC-20260704-003 / v1.53.0 |
| `coordination_probe.py` | **动态** (运行时) | 某符号最近 14d 是否真经**生产 CLI 入口**被调用 (读生产 telemetry 分区, 新鲜度窗口防「一条历史记录永久假绿」) | DEC-20260704-002 / v1.52.0 |

**问题**: 动态探针 (`coordination_probe.py`) 目前是**单一用途硬编码件** —— 写死 1 个分区文件 (`.aria/coordination-telemetry.jsonl`)、1 个符号 (`run_gate`)、1 个 config 开关 (`state_scanner.coordination.enabled`)、14d 窗口, 只服务 coordination 一家, 经 `.aria/state-checks.yaml` 的 shell command 注册为自定义 check。#95 §2 与 dedup handoff §6 均把「把它泛化为通用 runtime 探针范式」列为 follow-up。

## Grounding 实测发现 (probe-first, 避免凭前置 doc 推断)

本 brainstorm 先 probe 了真实代码 (`feedback_probe_first_scope_reframe` / `feedback_spike_first_for_data_hypotheses`), 三条实证直接重塑了 scope:

1. **N=1 消费者**: runtime 探针当前只有 coordination 一家在用。从单例抽象通用框架 = 经典过早抽象陷阱。
2. **历史零靶子**: #95 E-sweep 已扫 100 个 pre-#134 归档, 结论 **「零死代码孤儿」**(唯一 Layer L 孤儿已被 DEC-002 接活)。静态死代码问题**历史上几乎不存在** → 造通用武器打不存在的靶不划算。
3. **可行性硬约束**: 静态检查能对任意 spec 跑 (grep 引用); **动态探针不能** —— 它要读一份「机制一边在生产跑一边持续写下」的 telemetry 分区。**随便一个来归档的 spec 根本没埋记录点, 无日志可查** (无法事后追问「从未装计数器的代码最近被调几次」)。

→ **Scope 收缩** (~与 probe-first 记忆预测一致): 不做独立通用框架; 改为**把动态探针做成 #95 归档门的一个「声明式可选动态子检查」**。

## 约束条件

| 类型 | 约束 | 影响 |
|------|------|------|
| 可行性 | 动态探针须机制**预埋 telemetry**; 无预埋则无从探测 | 探针只对**声明了自己有探针**的 spec 生效; 其余静态-only |
| 兼容 | #95 E-sweep「100 spec 零误 block」性质必须保住 | **无声明 spec 的 gate 结果须与现状逐字节相同** (回归护栏) |
| 语义 | 承接 #95 **fail-toward-warn** | telemetry 缺失/陈旧/格式坏/探针内部异常 → **一律 warn, 永不 block 归档** |
| 侵入面 | 不动现有 telemetry 写入格式 | 分区**按机制专用** (symbol 当标签, 不做记录级过滤); 需要时再加共享分区 symbol 过滤 |
| 正交 | 动态结论与 `complete`、与静态 block 三者正交 | 可静态 pass ∧ 动态 warn; 已 block 的 spec 加 warn 不改 block |
| 落地 | 代码在 `aria/` 子模块 (aria-plugin); OpenSpec 变更在 `Aria/openspec/changes/` (Rule #5) | 与 #95 / DEC-002 同 landing 模式 |

## 考虑的方案

**Scope 层** (第一轮澄清):

| 方案 | 描述 | 状态 |
|------|------|------|
| 独立通用框架 (N≥2 消费者) | 有第二个具体机制现在就需要 | ❌ 无第二消费者 |
| **集成进 archive-gate** | 归档时静(spec_complete)+动(probe)双检合一 | ✅ **选定** |
| 仅重构+文档化范式 | 抽参数化 + 写「怎么加探针」文档, 备用 | ❌ (选定方案已含参数化) |
| 暂缓/换线 | N=1+历史零孤儿, 先不做 | ❌ owner 判定值得做 (前瞻护栏) |

**集成方式层** (第二轮澄清):

| 方案 | 描述 | 评分 | 状态 |
|------|------|------|------|
| **A 声明式可选挂件** | spec frontmatter 声明 `runtime_probe`; gate 见声明才跑并折入裁决; 无声明零影响; 缺失/陈旧=warn | ★ 最小侵入 + 真泛化 + fail-toward-warn | ✅ **选定** |
| B 强制式 (门反催) | gate 判 spec 是「集成型/承重」却没声明 → warn 催 | 更主动但更重/易误报/唠叨 owner | ❌ |
| C 纯接线 (硬编码映射表) | gate 内维护「机制→分区」对照表查表 | 最省事但**没真泛化**, 每加一个改门代码 | ❌ |

## 最终选择

**方案 A — 声明式可选动态子检查**。四部件:

**① 探针声明 (新增声明面, spec `proposal.md` frontmatter)**
```yaml
runtime_probe:
  partition: .aria/coordination-telemetry.jsonl   # 生产日志分区路径
  symbol: run_gate                                # 盯的符号 (标签 + 消息用)
  max_age_days: 14                                # 新鲜度窗口
  enabled_when: state_scanner.coordination.enabled # 可选: 该 config 开关下才生效
```

**② 通用探针库 (改造 `coordination_probe.py`)**
把写死常量抽成参数: `runtime_probe(descriptor, repo, now) -> {outcome, count, reason, symbol}`。
- 保留薄壳/向后兼容, 使 coordination 现有自定义 check 不破。
- 返回三态:
  - `pass` — 窗口内 ≥1 条生产记录 (它是活的)。
  - `warn` — 分区缺失 / 全陈旧(>窗口) / 只有非生产记录 (挂着但最近没转 = 死代码嫌疑)。
  - `skipped` — `enabled_when` 配置关 (功能本就没开, 「没被调用」是预期, 静默避免狼来了)。

**③ 归档门集成 (`gate_result` 折入)**
1. 读 `proposal.md` frontmatter; 无 `runtime_probe` 键 → 静态路径不变 (老 spec 全走这支)。
2. 有声明 → 跑通用探针 → 折入 tri-state 裁决:
   - `pass` → verdict 不变 + 绿色 note。
   - `warn` → 追加 `warnings[]`, verdict 抬到**至少 warn**, **绝不抬 block**; 已 block 的加 warn 不改 block。
   - `skipped` → 不动。
3. 探针结果作为新字段 `runtime_probe: {...}` 写入 `gate_result` dict, 并随 `unverified_claims` 落归档 proposal frontmatter (证据痕迹)。

**④ coordination 打样 (dogfood)**: coordination 的 spec 第一个写声明, 真跑 gate 验证折入闭环。

**三态设计意图**: `skipped` 把「正常关着」与「异常死了」两种「没被调用」分开, 只在**功能本该开着却没在转**时才 warn —— 保住警告信噪比 (防「狼来了」致探针失效)。

**符号匹配取舍**: 分区**按机制专用** (coordination 分区只有 `run_gate` 写入 → 数行即数该符号), `symbol` 只当**消息标签**; 避免强迫改 telemetry 写入格式 + 回填旧记录。日后若出现「一本混多机制」再加可选的记录级 symbol 过滤 (「先简单, 需要时再加」)。

## 理由

1. **真泛化 + 真集成点**: 把硬编码探针抽成「读声明」的参数化件, 且落到 archive-gate 这个真实消费点 (N=1→真集成), 而非投机造无人用的框架。
2. **前瞻护栏**: 虽历史零孤儿, 但一旦有机制退化成「挂着没转」, 归档门今后能凭**运行时证据**(非仅静态引用)在归档那刻抓住 —— 这正是 coordination 曾经的失败形态。
3. **零回归风险**: 无声明 spec 逐字节不变, #95 的「100 spec 零误 block」性质结构性保住。
4. **脾气一致**: 全程 fail-toward-warn, 探针是加分项永不成新 block 源 —— 与 #95 同philosophy, 审计口径统一。

## 风险与缓解

| 风险 | 缓解措施 |
|------|----------|
| 探针 bug 悄悄变成新 block 源 (silent-failure, #95 pre-merge 抓过的 Critical 形态) | gate 对探针**全异常 catch → 降级 warn 且照常出裁决**; fault-injection 测试强制覆盖 |
| 声明格式坏被当真去核验 (误判) | 格式坏/字段缺 → warn「无法核验」不猜、不 block |
| `skipped` 掩盖「本该开却 config 读不到」 | config 缺失/坏 → skipped + 低调 note (不 warn: 无法确证本该开); 决策显式记录此保守取舍 |
| 从 N=1 泛化仍偏抽象 | 声明 schema 保持最小 (4 字段); 只做 archive-gate 一个集成点, 不预造多后端 |
| 新鲜度窗口漂移致假绿 | 沿用现有 14d + 注入 `now` 确定性时间测试; 可证伪 harness 造「永远 pass」验测试能抓 |
| 双子星 (dev-claude2) 并发撞车 | 大活开工前 **fetch-first + 看板/handoff** (`feedback_concurrent_*`); 同 spec 后续走 coordination advisory gate |

## 交付给 spec-drafter 的建议

- **OpenSpec Level**: **Level 3 (Full)** —— 改动 archive-gate 裁决语义 (错则可能误拦正当归档, blast radius 高), 需 post_spec convergence 审计 + 严测试。虽 scope 明显小于 #95, 属「精简 L3」(单决策, 4 部件)。
- **落地位置**: 代码 `aria/skills/state-scanner/scripts/` (aria-plugin 子模块); OpenSpec 变更 `Aria/openspec/changes/` (Rule #5, 同 #95/DEC-002 模式)。
- **验收须可证伪** (`feedback_falsifiable_evidence_for_binary_acceptance`): 每条 AC 绑可验 metric (逐字节回归 diff / fault-injection verdict / dogfood 探针 outcome), 禁 AI 代填 bool。
- **post_spec 审计**: convergence 模式 (config 已设), 循环到 R_N==R_{N-1} 稳定 (`feedback_owner_invoked_convergence_loop`)。

## Cross-references

- 静态门 (被扩展方): `openspec/archive/2026-07-05-aria-archive-gate-runtime-reality/` + `DEC-20260704-003`
- 动态探针 (被泛化方): `openspec/archive/2026-07-05-interactive-session-dedup-coordination/` + `DEC-20260704-002`
- 现状代码: `aria/skills/state-scanner/scripts/coordination_probe.py` + `.../lib/spec_complete.py :: gate_result` + `.aria/state-checks.yaml :: coordination-gate-invocation`
- E-sweep 实证: `.aria/audit-reports/e-sweep-pre134-orphans-2026-07-05.md`
- 前序 handoff: `docs/handoff/2026-07-05-95-archive-gate-runtime-reality-shipped.md` (§2 A 项 follow-up 源)

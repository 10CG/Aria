# 决策: DEC-20260703-001 - secret-scan.sh 诚实降级 (PostToolUse redaction 撤宣称)

> **日期**: 2026-07-03 | **模式**: technical
> **关联**: aria-plugin #91 (part②, 本 cycle=A) · aria-plugin #92 (B 防御反馈闭环, 拆出独立 cycle) · claude-code-guide 官方文档核实

## 背景

aria-plugin #91 是两部分 issue：① PreToolUse `grep ~/.bashrc` 缺口(**已修 v1.50.2** commit `1aa10bd`,live 验证 exit 2 BLOCK + 260 PASS)；② PostToolUse `secret-scan.sh` output redaction 失效。

part② 经 claude-code-guide 查官方 hooks-guide 坐实为**架构性不可行**(非 version-dependent)：
- PostToolUse **无** `updatedToolOutput` 字段；hooks-guide line 891 "PostToolUse hooks can't undo actions since the tool has already executed"。
- hook stdout 改写**不替换**已捕获的 tool result；`suppressOutput` 仅隐藏 hook 自身 stdout(transcript UI),**tool result 照喂 model**。
- 唯一有效防线 = **PreToolUse block**(= 现有 secret-guard 模式)。

现状问题：secret-scan.sh 做着一件做不到的事(redact),还在 header/文档宣称有 output 兜底 → **误导性安全宣称**,可能致过度信任第二层。本 cycle (A) = 撤宣称 + 保住 secret-scan 仍能做到的检测价值。

## 约束条件

| 类型 | 约束 | 影响 |
|------|------|------|
| 架构 | PostToolUse 不能改写已产生的 tool output(CC 官方) | redact 方向死路,只能 warn |
| Rule #7 | secret 不入 chat-visible / 持久化通道 | 告警文本只能提元数据,不复述 secret 值 |
| 双上下文 | Aria 同时跑交互(owner)+ 自主(Layer-2 容器) | 阻断行为影响自主跑(归 B 处理) |
| scope | #91 A 应快速 ship(撤活着的误导宣称) | 新能力(反馈闭环)拆出,不拖慢 A |

## 考虑的方案

**Q1 目标取向**(owner 选)：

| 方案 | 描述 | 状态 |
|------|------|------|
| a) 诚实优先 | 只改文档宣称,行为次要 | 未选 |
| **b) 保住检测价值** | redact 做不到 → 转成"检测到泄露就告警(提醒轮换)",第二层仍有真实用处 | ✅ 选定 |
| c) 极简 | 拆掉 redact 逻辑退成最小/退役 | 部分吸收(删死代码) |

**Q3 事件→反馈 issue 机制**(owner 选)：

| 方案 | 描述 | 状态 |
|------|------|------|
| A) hook 直接自动开 issue | 命中即 auto-POST | 未选(野;二次泄密+刷屏风险最高) |
| **B) 本地记录 → 人工闸门** | `.jsonl` 事件 → aria-report 复核后开 issue | ✅ 选定 → **拆入 #92 独立 cycle** |
| C) 只在告警文字里附建议 | 全手动 | 未选(丢结构化留痕) |

**Blocking(Q2)**：owner 挂起深思 → 收敛为**置信度分级**(高置信 block+提示审阅 / 低置信 warn;自主上下文可配)→ **归 #92**(与"记录→审阅→报 issue"闭环一体)。

**Scope(并进 vs 拆)**：owner 选**拆** —— #91=A 诚实降级(本 cycle)；#92=B 防御反馈闭环(独立 cycle,依赖 A 先 ship)。

## 最终选择

**#91 cycle (A) = secret-scan.sh 诚实降级为 warn-only 检测器**：

1. **保留** secret-shape 扫描逻辑(检测能力不变)。
2. **删除** redact-then-reemit-on-stdout 死代码(CC 不认,留着误导)。
3. **改为** 命中即告警,用 CC 支持的两渠道：
   - `additionalContext`：告知 Claude "含疑似 secret,按已泄露处理、别复述"；
   - `systemMessage`：提醒 operator "检测到 X 类 secret,建议轮换"。
   - **本 cycle 不做**：`.jsonl` 记录 / block / 开 issue(全归 #92)。warn-only,非阻断。
4. **文档降级**：`secret-scan.sh` header(line 36-42 version-dependent → "架构性不可 redact,本 hook = 检测+告警")；**Phase A 先 grep 核实** `secret-hygiene.md` / CLAUDE.md Rule #7 是否真过度宣称 PostToolUse redaction 再改(避免瞎改 —— Rule #7 可能只讲 operator redirect)。
5. **测试**：`hooks/tests/secret-scan.test.sh` 改为断言命中发 warning(非断言 redacted output),删死代码后回归绿。

预估 **Level 2**(hook 行为改 + 多处文档 + 测试),纯 aria-plugin 无跨仓。

## 理由

1. **撤误导性安全宣称是本质**：文档宣称的 output 兜底不存在,不撤会致过度信任(以为读了 secret 会被自动 redact)。
2. **b 保住真实价值**：门口拦不住的漏网,事后有"你漏了,快轮换"告警是真实防御(#91 泄露就是靠人发现后手动轮换),且 CC 原生支持告警渠道。
3. **拆 = 别让救火等造楼**：A 小而急,应独立快 ship;B 有 event schema/redaction 安全/分级 block 一堆设计面,塞进 A 既拖慢 A 又欠设计 B。天然次序:A reframe 检测器 → B 建闭环。
4. **自动反馈走 staged flip(记 #92)**：record+gate(Stage 1)= 通往自动 POST(Stage 2)的安全跑道 + flip 前置(攒 FP 率/redaction 安全/去重证据),非绕路;直接跳自动 = Rule #7 悖论未验 + 无人在环的持久泄露最坏失败模式。

## 风险与缓解

| 风险 | 缓解措施 |
|------|----------|
| 降级后有人以为"第二层没用了" | 明确 reframe 为"检测+告警"(仍有值),而非删除;防御重心文档化到 PreToolUse |
| Rule #7 核实不全,漏改某处宣称 | Phase A grep 全仓 `PostToolUse.*redact` / `output.*兜底` / secret-scan 引用,逐处核 |
| 删死代码误删检测逻辑 | 测试先固定"检测仍工作 + 告警发出",再删 reemit |
| B 永远不做 → 检测告警无闭环 | #92 tracker 留痕,依赖关系明确;A 独立有价值(告警本身有用),不强绑 B |

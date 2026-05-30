# 决策: DEC-20260530-001 — ai-native-estimator v1 架构 (Token 轴薄垂直切片)

> **日期**: 2026-05-30 | **模式**: brainstorm (technical + requirements)
> **Source**: aria-plugin [#18](https://forgejo.10cg.pub/10CG/aria-plugin/issues/18)
> **Spec**: `openspec/changes/ai-native-estimator/proposal.md`
> **Owner**: 8-turn interactive brainstorm (Mode B)

## 背景

#18 提议用 **Token × Attention 双主轴模型** 替代传统 4-8h 人工时估算 (1 Human + Claude Code 模式下传统估算失效)。原提案是 2.0 级愿景: 双轴 + L0/L1/L2 预估 + 6 skill 集成 + 校准 + 双层呈现。本 brainstorm 目标是 scope 到一个可 ship、可立即 dogfood 的 **v1 薄切片**。

**关键解锁**: 2026-05-29 ship 的 `aria-token-telemetry` internal skill (#104) 提供 `parse_transcript_usage()` raw counts (input/output/cache_read/cache_creation, window-independent) — 这正是 #18 预留的 Token 轴复用基础, 使 Axis 1 自动采集 de-risked。

## 约束条件

| 类型 | 约束 | 影响 |
|------|------|------|
| 数据源 | Token 轴自动采集依赖 aria-token-telemetry transcript 解析 (已 ship) | Axis 1 可立即落地 |
| 设计未解 | Attention 轴收集机制是未解题 | Attention 轴 defer 到 v2 |
| 价值延迟 | v1 ship 时 variance_history 为空, forecast 无数据 | 冷启动用 bootstrap 种子, 诚实降级 |
| thesis | #18 核心论点反对"时间作工作量单位" | 时间只作被动元数据, 不进 workload |

## 最终决策 (7 项)

| # | 决策 | 选择 | 理由 |
|---|------|------|------|
| DEC-1 | v1 scope 雄心 | **Token 轴薄垂直切片** (Axis 1 only) | Token de-risked; Attention 轴自身需设计; 先积累 variance 数据 (L2 回归前提) |
| DEC-2 | task→token 归因 | **cycle 粒度, phase-d 采集, watermark 机制** | 零微观 instrument; watermark 锚天然支持跨 session/多 cycle 增量, 无需检测 session 起始 |

> **Rev1 (post_spec R1, 2026-05-30)**: DEC-2 watermark 锚从 `last_captured_turn_index` 修正为 **`{last_uuid, last_timestamp, session_id, transcript_path}`**。spike 实证真实 transcript **无数字 turn_index** (用 uuid/parentUuid 链), `timestamp`(ISO8601)/`sessionId` 可靠存在。增量按 uuid 匹配, uuid 不在文件 (session 切换/轮转) → fallback timestamp + warn。**新增 token-telemetry additive API** `iter_transcript_usage(path)` (单一解析 SoT; 现有 `parse_transcript_usage` 只返末轮, 不支持 range Σ — 原"无改动复用"是 false claim, R1 3/3 Critical)。`spec_level` 读 proposal frontmatter Level。详见 proposal Rev1 changelog。
>
> **Rev2 (post_spec R2, 2026-05-30)**: 幂等机制修正 (R2 NEW-C-1, backend 发现 + qa corroborate)。原 `cycle_id = {spec_slug}-{captured_at_iso}` 嵌 capture 时刻, 幂等却 key 在 cycle_id — 重跑 captured_at 变 → 去重失效。修: **幂等主机制 = watermark 空区间** (重跑无新 turn → range 空 → skip); `cycle_id = {spec_slug}-{end_uuid[:8]}` (range 末 uuid 锚, cycle 内稳定); cycle_id 扫描降为 secondary guard。详见 proposal Rev2 changelog。
| DEC-3 | task-planner 集成 | **v1 也 defer** → v1 = phase-d 采集 + estimator 查询 API only | 冷启动无数据, advisory 价值延迟; 集成等有数据再做 |
| DEC-4 | 采集指标 | **存 raw 四分量; headline work_metric = output + cache_creation** | cache_read 是上下文重载非"工作"; 存 raw 使改公式无需重采集 |
| DEC-5 | 聚类键 | **spec_level (L1/L2/L3)** | issue 想要 task_type+context_load, 但 context_load 属 Attention 轴 (deferred); L1/L2/L3 三档够起步 |
| DEC-6 | 冷启动 | **bootstrap 种子表 (L1~30k/L2~150k/L3~500k), 标 uncalibrated, 仅 N<3 fallback** | issue §L0 "冷启动用社区默认表"; forecast 诚实降级不假装精确 |
| DEC-7 | 时间维度 (owner alt-thinking) | **被动元数据 wall_clock_seconds, 非工作量轴** | transcript range timestamps 已在手 (几乎免费); 标注"日历经过≠投入"; 只 history/velocity 展示, 不进 forecast — 满足 owner 历史数据诉求又不违背 #18 thesis |

## 考虑过但否决的方案

| 方案 | 否决理由 |
|------|----------|
| B. 双轴 core + 最小集成 | Attention 轴收集机制未解, 拖累 v1 ship; 先做能自动测的半 |
| C. 近全量提案 (6 集成) | 接近 v2.0 milestone 规模, 多 cycle |
| A. per-task transcript range sum | 需 task 生命周期 hook (subagent-driver/phase-b), v1 过重 |
| B. session-cumulative delta | 隐含 1 task≈1 session, 多任务并行噪声大 |
| 时间作第三工作量轴 | 直接违背 #18 thesis (时间不适合作工作量单位) |

## v1 交付物

1. `aria/skills/ai-native-estimator/SKILL.md` + `scripts/estimator.py` (capture/forecast/history/velocity + watermark + bootstrap)
2. `phase-d-closer` 集成: 收尾调 `estimator.capture(cycle_meta)` (新 D 子步, advisory 非阻塞)
3. `.aria/estimator/{variance.jsonl, watermark.json}` schema + 存储
4. config-loader 注册 `ai_native_estimator.{min_samples:3, bootstrap_seed:{...}}` namespace
5. 测试 + fixtures (Rule #6 deterministic structural substitute, internal data 逻辑无 LLM AB)
6. 版本 → aria-plugin v1.34.0

## 风险与缓解

| 风险 | 缓解措施 |
|------|----------|
| cycle 粒度太粗, L2 回归需更细 | v1 明确只做 cycle 粒度积累; per-task 归因留 v2 (DEC-2 记录此 tradeoff) |
| watermark 漂移 (transcript 路径变/session 切换) | watermark 存 `{last_uuid, last_timestamp, session_id, transcript_path}` (Rev1: uuid 锚, 非 turn-index); uuid-miss → timestamp fallback + warn; 幂等主机制 = watermark 空区间 (Rev2) |
| bootstrap 种子误导用户当真值 | forecast 返回显式 `status:"insufficient"` + `uncalibrated:true` 标记 |
| wall_clock 被误读为工作量 | schema 字段注 + SKILL.md 显式 "calendar-elapsed ≠ effort"; 不进任何 forecast/workload 计算 |
| variance.jsonl 跨项目可移植 | 无 statusLine 项目走 transcript fallback (token-telemetry 已保证); 无 transcript → capture skip + warn |

## 后续 (defer 到 v2+)

- Axis 2 (Attention-Minutes): 收集机制 (任务结束问答 / timeline 半自动推断) — 独立 brainstorm
- L1 (Haiku dry-run) / L2 (经验公式回归) 预估策略
- 5 skill 集成: task-planner / progress-updater / state-scanner burndown / phase-a-planner / requirements-sync
- S/M/L/XL 替代 (v1 共存, estimator 旁挂)
- per-task 粒度归因

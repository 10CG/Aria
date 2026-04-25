# state-scanner-mechanical-enforcement — state-scanner Phase 1.x 机械化执行

> **Level**: Full (Level 3 Spec)
> **Status**: Complete (2026-04-25, T1-T10 全部交付, 8/8 验收交付物 ticked, T8 Kairos 跨项目验证通过)
> **Created**: 2026-04-15
> **Activated**: 2026-04-23
> **Completed**: 2026-04-25
> **Parent Story**: (无直接父 Story, 属 Plugin 基础设施质量改进)
> **Target Version**: aria-plugin v1.17.0 (activation 时从 v1.16.0 追齐至 v1.16.4+, minor bump 为 v1.17.0; AD-SSME-5 "1 minor 版本后移除 opt-out" 同步改为 v1.18.0)
> **Source**: 2026-04-15 Aria 主项目 session 发现 Phase 1.13 Issue 感知自 2026-04-09 首次启用后连续多轮 session 漏跑 (issue cache 陈旧 6 天), 非工具缺陷而是 AI 执行纪律问题
> **Related Feedback Memory**: `feedback_state_scanner_run_all_phases.md`
> **post_spec Audit**: `.aria/audit-reports/post_spec-2026-04-23T2058Z-state-scanner-mechanical.md`

---

## Revisions Required Pre-B.2 (2026-04-23 audit 注入)

post_spec Agent Team (tech-lead / backend-architect / qa-engineer / code-reviewer) 4/4 一致投票 `activate_with_revisions`. 本 Spec 激活为 Approved, 但以下 4 条 Critical Finding 必须在 Phase B.2 T1 开工前作为 T0 revision 消化:

| CF | 拥有者 | 问题 | 必需 revision |
|---|---|---|---|
| CF-1 | tech-lead | Target Version v1.16.0 已过期 (实际 v1.16.4) | 追齐 v1.17.0, AD-SSME-5 移除时间表改 v1.18.0 (本 header 已更新) |
| CF-2 | qa-engineer | T7.1 "diff 为空或仅时间戳差异" 无机械判定标准 | tasks.md 新增 T7.0 "JSON canonical normalizer 规范" (jq -S + float 精度 + null/absent 归并), 作为 T7.1 前置 |
| CF-3 | backend-architect | state-snapshot.json 顶层 schema_version 与 issue_status.schema_version 命名冲突 | 顶层字段重命名 `snapshot_schema_version`, T4.1 schema 文档明示作用域边界 |
| CF-4 | code-reviewer | T4.3 AD-SSME-6 "docstring 自动生成 schema.md" 0.5h 严重低估 | 二选一: (a) T4.3 扩至 3h 明确工具链, (b) 降级为手维 schema.md, AD-SSME-6 改 "source-of-truth = schema.md" |

Important Findings (IF-1~IF-8) 见 `.aria/audit-reports/post_spec-2026-04-23T2058Z-state-scanner-mechanical.md`, 开工 1 周内评估处理。

## Intentional Divergences from v2.9 prose (pre_merge R1-C6 audit 注入)

proposal.md §非目标 声明 "不改变 Phase 1.x 数据采集语义". 以下 5 项属 scan.py 实现阶段发现的 **bug 修复**, 与 §非目标 字面冲突, 现显式记录为 intentional:

| # | v2.9 prose 行为 | v3.0 scan.py 行为 | 来源 audit |
|---|---|---|---|
| D1 | `Approved` Status 塌缩为 `ready` | 保留独立 `approved` 状态 | mid_impl B1 (code-reviewer IMP-1) |
| D2 | `Reviewed` Status 塌缩为 `pending` | 保留独立 `reviewed` 状态 | mid_impl B1 (code-reviewer IMP-1) |
| D3 | `chain_valid` 对 `"(pending)"`/`TBD` 返回 True (false positive) | 占位符黑名单拒绝, 返回 False | mid_impl B2 (code-reviewer IMP-2) |
| D4 | YAML `key: \|` block scalar 泄漏字面 `"\|"` | 识别块标量 marker, 返回 None | mid_impl B3 (code-reviewer IMP-3) |
| D5 | `Active`/`Deprecated`/`Archived` Status 映射为 `unknown` | 保留独立 `active`/`deprecated`/`archived` 状态 | pre_merge R1-I5 (qa-engineer QA-R1-10) |

T7.1 dogfooding diff 必须通过 T7.0 canonical normalizer 把上述 5 字段放入 tolerance whitelist, 否则会把 bug 修复误判为 regression。详见 `aria/skills/state-scanner/references/state-snapshot-schema.md` §Sister-bug divergence。

## Why

### 问题陈述

state-scanner v2.9 的 Phase 1.x 有 14 个子阶段 (0 / 1 / 1.1 / 1.5-1.14)，其中三个是 opt-in (1.11 自定义检查 / 1.12 同步检测 / 1.13 Issue 感知), 由 `.aria/config.json` 开关控制。SKILL.md 对每个阶段的描述都是 "**重要**: 此阶段始终执行", 但执行体是 **AI 读 prose 后自律**, 没有机械兜底。

2026-04-15 session 中发现:

- Aria 项目 `issue_scan.enabled=true` 自 2026-04-09 起启用 (dogfooding)
- `.aria/cache/issues.json` 最后刷新时间 = 2026-04-09, 距当日已 **6 天**
- TTL = 900s (15min), 说明自启用以来历次 state-scanner session 都没有真正刷新缓存
- 当日 session 初次扫描时, AI (Claude) 同样漏跑了 Phase 1.13
- 直接后果: 推荐决策丢失了 Issue #16 (US-020 M0) 这个与当前分支直接相关的锚点

### 根因分析

1. **认知负担 vs 机械约束**: SKILL.md 总计 ~700 行, AI 读文档时自然倾向聚焦 happy path (git/openspec/audit 等高频阶段), 把 opt-in 阶段心理上归为 "可选"。
2. **无失败信号**: 漏跑是**静默**的 — 没有报错, 没有 diff, 推荐输出看起来完整, 只是少了一部分数据。用户除非主动追问否则无从察觉。
3. **探针式防御 (L1) 是补丁, 不是修复**: 2026-04-15 已在 `.aria/state-checks.yaml` 加入 `issue-cache-freshness` 反向探针 (Phase 1.11 监视 Phase 1.13), 但这只解决 "**事后检测**", 不解决 "**事前预防**"。AI 下次仍然可能漏跑, 只是漏跑后会被亮红。

### 为什么此 Spec 不是立即启动

- L1 探针 + L2 feedback memory 已覆盖 **检测** 和 **行为纠正** 两层
- 需要观察接下来几次 session 的 L1 探针告警频率, 才能判断是否需要上 L3 机械化
- **Activation Gate**: L1 探针在后续 session 中亮红 **≥ 2 次**, 或用户显式要求, 此 Spec 从 Draft 激活到 Approved

---

## What

### 交付物

1. **scan.py 采集脚本** — 单文件 Python (stdlib-only), 封装 Phase 1.x 全部数据采集逻辑, 产出 `.aria/state-snapshot.json`
2. **state-snapshot.json schema 定义** — `references/state-snapshot-schema.md`, 版本化 (v1.0)
3. **SKILL.md 执行流程重构** — Step 0 硬编码 bash call, Phase 1.x 说明退化为 "数据由脚本产出, 字段语义见 schema 文档"
4. **Python 测试套件** — `tests/test_scan.py` + `tests/fixtures/` (mock git repos + mock config), 覆盖 Phase 1.1-1.14 全字段
5. **迁移与回退策略** — `migration-v2.9-to-v3.0.md`, 含 opt-out flag `state_scanner.mechanical_mode=false` (保留旧路径 1 个 minor 版本)
6. **跨项目验证** — Kairos 项目跑一次新版 state-scanner, 确认脚本在非 Aria 环境 (TypeScript/Node.js) 下字段采集正确

### 架构决策

| ID | 决策 | 依据 |
|---|---|---|
| **AD-SSME-1** | 语言选 Python 3.8+ stdlib-only, 不用 Bash | 跨平台 (CLAUDE.md 明确 Windows Git Bash 兼容痛点), 可测试 (pytest fixture), aria-plugin-benchmarks 已有 Python 基础 |
| **AD-SSME-2** | 脚本**只采集**, 不做推荐匹配 | 规则表达力需要语言理解, 强行数据化会把 AI 推理能力从 Phase 2 剥夺; 但置信度**公式**可以数据化 (数值权重) |
| **AD-SSME-3** | JSON schema 版本化 (`schema_version` 字段) | SKILL.md 和脚本解耦演化; 版本不匹配时 SKILL.md 硬 abort |
| **AD-SSME-4** | Phase 2/3/4 保留 prose (AI 推理) | 推荐匹配 / 用户交互 / workflow-runner handoff 需要语言理解, 这三阶段的跳步用户**立刻可见** (没有推荐输出), 不需要额外防御 |
| **AD-SSME-5** | 保留 `mechanical_mode=false` opt-out 1 个 minor 版本 | 不破坏现有用户工作流; v1.18.0 起移除 opt-out (post-CF-1 revision, 此 release = v1.17.0, 移除 = v1.18.0), prose 路径完全下线 |
| **AD-SSME-6** | (post-audit revision 2026-04-23, CF-4) Source-of-truth = 手维 `state-snapshot-schema.md`, scan.py 通过 `SNAPSHOT_SCHEMA_VERSION` 常量引用版本号; 一致性由 `scripts/validate_schema_doc.py` 在 CI 断言 | stdlib-only 约束下 docstring → markdown 工具链成本过高 (AST 解析 + 渲染 ≥2h), 手维 + validator 更稳定 |
| **AD-SSME-7** | 不做 emit-handoff.sh (Phase 4 保留 AI) | 边际收益低, Phase 4 主要是结构化参数传递, AI prose 足够 |

### 非目标 (Out of Scope)

- **不改变 Phase 1.x 的数据采集语义** — 字段与 v2.9 严格 1:1 对齐, 仅改变执行载体
- **不引入推荐规则引擎** — `RECOMMENDATION_RULES.md` 仍由 AI 解释执行
- **不做 Phase 2 置信度的全自动计算** — 基础权重可以数据化, 但最终判断由 AI 综合
- **不涉及其他 Skill 的机械化** — 本 Spec 仅针对 state-scanner; 其他 Skill 若有类似问题, 走独立 Spec
- **不涉及 workflow-runner 的任何变更** — Phase 4 handoff 契约保持 v2.9 兼容
- **不修改 `.aria/state-checks.yaml` 探针** — L1 探针作为独立防御层保留 (即使脚本化后, 探针仍然是"脚本是否真的被调用"的兜底)

### 风险与缓解

| 风险 | 概率 | 影响 | 缓解 |
|---|---|---|---|
| 脚本 schema 漂移 (AI 预期字段与实际产出不一致) | 中 | 高 (Phase 2 推荐错误) | `schema_version` 硬断言 + CI 运行 schema validator |
| 跨平台失败 (Windows Git Bash 环境 Python 缺失) | 低 | 中 (用户体验) | Python 3.8+ 是主流依赖; fallback 到 `mechanical_mode=false` prose 路径 |
| AI 绕过 Step 0 手动跑 bash 命令自行采集 | 低 | 中 (回到旧漏跑模式) | SKILL.md Step 0 写成机械指令; Phase 2 入口断言 `state-snapshot.json` 存在且 `schema_version` 匹配 |
| Phase 1.x 演化速度拖慢 (新增阶段需同时改脚本 + schema) | 中 | 低 | 从"改 prose"变成"改脚本 + 跑测试", 总成本不增反降 (可测试性提升) |
| 脚本单元测试 fixture 维护成本 | 中 | 低 | fixture 只覆盖关键路径 (git 3 状态 × config 4 组合 ≈ 12 场景); 增量维护 |
| 用户项目没有 Python 3 | 极低 | 高 (Skill 不可用) | opt-out flag + prose fallback 路径 |

### 成功指标

- **功能等价**: 新版 state-scanner 在 Aria + Kairos + 一个 minimal fixture repo 上的输出与 v2.9 字段一致 (diff 为空或仅时间戳差异)
- **漏跑消除**: Spec 激活后 4 周内 L1 探针 (`issue-cache-freshness`) 零告警
- **性能回归**: 新版单次 scan 总时长 ≤ v2.9 × 1.2 (允许 20% 开销)
- **测试覆盖**: `tests/test_scan.py` 行覆盖率 ≥ 85%

---

## Activation Gate

本 Spec 写成 Draft 后**不立即启动**, 需满足以下任一条件才激活到 Approved:

1. L1 探针 (`.aria/state-checks.yaml` 中 `issue-cache-freshness`) 在 Aria 或任一用户项目中亮红 ≥ 2 次
2. 用户显式要求启动 (例如: "开始执行 state-scanner 机械化")
3. state-scanner 新增第 15 个子阶段前 (避免 prose 继续膨胀)

激活前, 此 Spec 仅作为 **技术方案备案**, 不占用开发工时。

---

## 工时估算

| 任务组 | 工时 |
|---|---|
| T1. scan.py 骨架 + Phase 1.1-1.5 | 6h |
| T2. Phase 1.6-1.10 (openspec/arch/readme/standards/audit) | 5h |
| T3. Phase 1.11-1.14 (custom/sync/issue/forgejo) | 6h |
| T4. state-snapshot schema 文档 + 版本化 | 2h |
| T5. SKILL.md 重构 + Step 0 机械指令 | 3h |
| T6. 测试套件 (fixture + unit test) | 8h |
| T7. Aria 项目 dogfooding + diff 对照 | 2h |
| T8. Kairos 跨项目验证 | 2h |
| T9. 迁移文档 + opt-out flag | 2h |
| T10. Benchmark (`/skill-creator` AB 对比) | 2h |
| **小计** | **38h** |
| Buffer (20%) | 8h |
| **合计** | **~46h / 1.2 weeks** |

> 工时前提: 假设 Python 脚本化与 v2.9 prose 行为 1:1 对齐无设计反复; 若 Activation Gate 触发时 state-scanner 已演化到 v2.10+, 工时需重估。

---

## 验收标准

- [ ] scan.py 能在 Aria / Kairos / minimal fixture 三处产出相同 schema 的 JSON
- [ ] `tests/test_scan.py` 覆盖率 ≥ 85%
- [ ] SKILL.md Step 0 硬编码 bash call, AI 无法通过"读文档时跳过"绕过
- [ ] `state-snapshot.json` schema_version 不匹配时 AI 必须 abort (实测一次)
- [ ] `mechanical_mode=false` opt-out 路径仍可用 (向后兼容)
- [ ] L1 探针 `issue-cache-freshness` 仍然保留且通过
- [ ] `/skill-creator` benchmark delta 非负 (不破坏现有质量)
- [ ] Aria v1.15.0 的 Phase 1.12 多远程 parity / Phase 1.13 Issue 感知字段在新版中完整保留
- [ ] 迁移文档覆盖 opt-out 移除时间表 (v1.18.0 — post-CF-1 revision, 此 release = v1.17.0)

---

## 关联

- **L1 探针**: `.aria/state-checks.yaml` (`issue-cache-freshness` 已于 2026-04-15 落地)
- **L2 memory**: `feedback_state_scanner_run_all_phases.md` (2026-04-15)
- **起因 session**: 2026-04-15 Aria 主项目 `feature/aria-2.0-m0-prerequisite` 分支的 state-scanner 调用
- **相关 Skill 文档**: `aria/skills/state-scanner/SKILL.md` v2.9.0
- **并行工作**: Aria 2.0 M0 (US-020) — 本 Spec 不阻塞 M0, 可在 M0 完成后或 L1 探针触发后并行推进

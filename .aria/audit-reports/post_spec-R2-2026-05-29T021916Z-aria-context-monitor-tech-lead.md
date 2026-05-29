---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: true
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-05-29T02:19:16.000Z
context: openspec/changes/aria-context-monitor/proposal.md
agents: [tech-lead]
---

# Post-Spec Audit (R2, stability/verification) — aria-context-monitor — tech-lead lens

## 审计结论

R2 任务: 验证 R1 四个 MAJOR 是否真闭合 (含 git-remote-helper 先例真实性 + 新落点架构干净度) + 扫描 Rev1 引入的 NEW 架构风险。所有验证均落地实测, 非纸面读 changelog。

### R1 finding closure table

| ID | R1 finding | Rev1 fix 主张 | 验证证据 | 状态 |
|----|-----------|--------------|---------|------|
| **M1** | 共享 collector 落点 `state-scanner/scripts/lib/` 违反目录约定 + 跨-skill 耦合倒置 | 改为独立 internal skill `aria-token-telemetry` (user-invocable:false), 复用 git-remote-helper US-012 Layer 3 先例 | **先例真实且干净** (见下方 M1 深度验证) | **CLOSED** |
| **M2** | statusLine relay stdin 重入语义未约束, 有静默破坏用户状态栏风险 | §Relay 注入语义 (L76-83): 必复用 `$input` / 必注入在 `input=$(cat)` 之后 / marker 锚点检测 / atomic tmp→rename | proposal L78-83 + Task 1.3 + Task 1.7 (run-twice/pre-existing-marker/user-custom-bar/corrupt-cache 场景) | **CLOSED** |
| **M3** | statusLine stdin schema runtime-dependency 脆弱 + 静默坏数据未防御 | Task 1.1 标 BLOCKING pre-Phase-B gate + 失败回退条款 + cache 顶层 `schema_version` 对比 + JSONDecodeError→unavailable | proposal L66/L83/L109/L156; schema_version drift 检测 + 缺失字段触发 fallback 升级 | **CLOSED** |
| **M4** | staleness 阈值缺失, 陈旧 cache 仍报 high confidence 复现原始病 | §Staleness 契约 (L68-75): 默认 300s (config 可覆盖) + >阈值 → confidence=estimate + 降级不信 relay used_pct | proposal L72-74 + Success Criterion L171 + Task 1.6 固化常量 | **CLOSED** |
| m-minor (window_source) | L79 "relay-cached size" vs L98 "runtime" 命名不自洽 | 新增 `cached_size_reuse` enum 值, 主路径 `runtime` 与复用历史 size 显式区分 | proposal L98/L102/L126 enum 5 值对齐 DEC 4-tier | **CLOSED** |
| m-minor (acceptance) | "0 偏差" success criterion 同义反复 | 拆 `used_percentage` vs `used_percentage_proxy` 两口径, criterion L170 改为 proxy 非 null 断言 | proposal L116/L135/L170 | **CLOSED** (大幅改善; 见 NEW-m1 残留) |
| **m-minor (config-loader)** | `context_monitor.window_tokens` 未在 config-loader DEFAULTS.json 落 task | — (Rev1 changelog 未提及此项) | 实测 `DEFAULTS.json` **仍无** `context_monitor` key; proposal Tasks **无** config-loader 注册条目 | **OPEN (carried minor)** |

### M1 深度验证 (R2 核心任务 — 先例真实性 + 落点干净度)

R1 的关键 MAJOR。Rev1 把寄生落点改为独立 internal skill 并援引 git-remote-helper 先例。我独立实测三点:

1. **先例真实存在且就是该模式** [scope: aria/skills/git-remote-helper/]
   - `user-invocable: false` + `disable-model-invocation: true` (实测 frontmatter L6-7) — 与 Rev1 `aria-token-telemetry` 主张的 `user-invocable: false` 同构。
   - **自带中立宿主 scripts/** (实测: `check_parity.sh` / `push_all_remotes.sh` / `verify_post_push.py`) — collector 代码归属于 helper 自身, 不寄生任一消费者。
   - **被一个不是自己的 skill 消费**: `grep -rl git-remote-helper` 命中 `phase-c-integrator/SKILL.md` (C.2.5) + SKILL.md 内声明的 `state-scanner` Phase 1.12。即"≥2 个外部消费方 import 中立宿主"的范式被实证。
   - Rev1 援引的 US-012 Layer 3 "internal skill 作跨-skill 共享基础设施"语义与该 skill 实际形态**完全吻合**, 非误引。

2. **新落点架构干净 (无寄生耦合)** [scope: aria/skills/aria-token-telemetry/]
   - Rev1 让 #104 (aria-context-monitor) 与 #18 (ai-native-estimator) **对称地** import 中立的 `aria-token-telemetry`, 没有任何一方寄生在对方或第三方 (state-scanner) 的内部目录树。这正是 git-remote-helper 范式的 1:1 复制 — ownership 归属中立宿主, 消费方只依赖宿主的稳定接口契约。
   - R1 指出的"两个消费方都不是 state-scanner"的耦合倒置被根除: 现在两个消费方都不是 telemetry skill 本身, 而宿主就是为"被多方 import"而存在的。**边界设计正确**。

3. **原寄生反模式已消失** [scope: 全仓]
   - 实测 `state-scanner/scripts/` 下仍是既有约定 (`collectors/` / `renderers/` / `writers/` / 顶层 `.py`), **无 `scripts/lib/`** 被引入。R1 担忧的"凭空第四种组织模式 + 寄生" 在 Rev1 中不再出现 (proposal 全文已无 `state-scanner/scripts/lib/` 字样, deliverable 落点 L109 改为 `aria/skills/aria-token-telemetry/scripts/token_telemetry.py`)。
   - 注: 实测存在 `aria/skills/state-scanner/lib` 目录 (与 R1 的 `scripts/lib/` 不同路径), 属 state-scanner 自身既有结构, 与本 Spec collector 无关, 不构成新耦合。

**M1 判定: 真闭合, 非纸面修。** 这是 Rev1 最重要且最干净的一处修正。

### NEW 架构风险扫描 (Rev1 新增整个 internal skill 后)

- **[ok] 加新 internal skill 未将本 Spec 推向 Level 3** [category: scope-boundary]
  R1 已判 Level 2 正确。Rev1 增加 `aria-token-telemetry` 后变更 = 2 新 skill (1 internal + 1 user-facing) + relay 行 + cache + doctor 集成 + 文档。判定 Level 的是: 无 API break / 不跨多 service / additive / 单 cycle (~4-5h)。新增的是一个 user-invocable:false 的纯数据层 skill, 不引入新的 service 边界、不破坏既有契约 — 与 git-remote-helper 当年也未触发 Level 3 同理。proposal L3/L11 已诚实更新 scope 描述 (从 "1 skill" → "context-monitor skill + token-telemetry internal skill")。**仍属 Level 2, proposal-only 充分**, 无需 tasks.md。

- **[ok] 2-skill split + telemetry 边界仍连贯** [category: architecture]
  职责切分清晰: `aria-token-telemetry` = 纯解析层 (relay cache 读 + transcript usage 解析 + window 4 档 resolve, raw counts 独立于 window%); `aria-context-monitor` = 消费层 (staleness 判定 + confidence 标注 + 结构化输出)。proposal L109 "raw counts 解析独立于 window%" 把"为何 #18 能复用而不被 window% 污染"落实为可验接口。边界无渗漏。

- **[ok] BLOCKING Task 1.1 gate + 回退条款 sound** [category: process / risk-control]
  Task 1.1 (L155) 标 BLOCKING pre-Phase-B gate, 强制重新 capture 固化 schema, 且写明"若 `context_window_size` 缺失 → 触发回退条款 (fallback 链升主路径), 回 A.2 修 Spec"。这把 R1-M3 的 strategic risk (单次已删 spike capture 的证据脆弱性) 转化为**实施前的硬闸门 + 已定义的失败分支**, 而非埋到实施期。证据状态披露 (L66 ⚠️ 块) 诚实标注了"仅单次 capture 无独立复现"的字段清单。这是审慎且可审计的设计。

- **[minor / NEW-m1] used_percentage_proxy 口径仍未给可证伪交叉校验** [category: acceptance / scope: proposal L135/L170]
  Rev1 把 R1 的"0 偏差"同义反复拆成两口径 (relay `used_percentage` runtime 口径 / transcript `used_percentage_proxy` = input+cache_read+cache_creation 合计口径), 大幅改善。但 transcript 路径的 acceptance (L170) 仅断言 "proxy 非 null", **未要求 proxy 与某独立重算基准的偏差阈值**。#104 病根是"高置信但失准"; relay 路径已由 staleness 闸门防护, 但 transcript fallback 路径的准确度本身仍只验"非 null"不验"准"。建议 (非阻塞): acceptance 补一条 proxy 与 transcript last-turn 手算值偏差 < 阈值的断言 (呼应 `feedback_falsifiable_evidence_for_binary_acceptance`)。此为 minor, 不阻断进 task-planner。

## Verdict

**PASS_WITH_WARNINGS**

R1 majors: **4/4 CLOSED** (M1 collector 落点 / M2 relay stdin 语义 / M3 schema drift / M4 staleness) — 全部以 code+doc+task 三位一体修正, 非 paper fix。
R1 minors: 3/4 CLOSED (window_source 命名 / acceptance 拆口径大幅改善), **1 OPEN carried** (config-loader 注册 task 缺失)。

| 类别 | NEW (Rev1 引入) | Carried (R1 残留) | 合计 |
|------|----------------|------------------|------|
| critical | 0 | 0 | 0 |
| major | 0 | 0 | 0 |
| minor | 1 (proxy 准确度无可证伪交叉校验) | 1 (config-loader DEFAULTS.json 未注册 `context_monitor` key + 无注册 task) | 2 |

- new critical: **0**
- new major: **0**
- R1 majors CLOSED: **是 (4/4)**

按 verdict 规则: 0 new critical + 0 new major + R1 majors 全 CLOSED → 本应 PASS; 但存在 2 个 minor (1 carried + 1 new), 故 **PASS_WITH_WARNINGS**。两个 minor 均非阻塞, 可在 task-planner 阶段补 task 吸收 (config-loader 注册) 或实施期落 acceptance (proxy 校验), 不需再回 A.2 重审。

架构主干在 R1 已站住; Rev1 把 4 个 major 中最重的边界错误 (M1 collector 寄生) 改为复用经实证的 git-remote-helper 中立宿主范式, 是结构性正确的修正。新增整个 internal skill 未越 Level 2 边界, 2-skill 切分连贯, BLOCKING gate + 回退条款审慎。可进 task-planner。

## 轮次记录

- **R1 (tech-lead, 2026-05-29T02:08:37Z)**: 首轮。0 critical / 4 major / 4 minor。verdict = PASS_WITH_WARNINGS。
- **R2 (tech-lead, 2026-05-29T02:19:16Z)**: stability/verification 轮。独立实测验证 4 个 R1 major 闭合 (重点: git-remote-helper 先例真实性 — frontmatter user-invocable:false + 自带中立 scripts/ + 被 phase-c-integrator 等外部 skill 消费 = 中立宿主范式实证; 新落点 aria-token-telemetry 对称 import 无寄生耦合; 原 state-scanner/scripts/lib/ 反模式已消失)。NEW 风险扫描: 加新 internal skill 未触发 Level 3, 2-skill 边界连贯, BLOCKING Task 1.1 + 回退条款 sound。发现 0 new critical / 0 new major / 1 new minor (proxy 准确度可证伪性) + 1 carried minor (config-loader 注册)。R1 majors 4/4 CLOSED。verdict = PASS_WITH_WARNINGS。**converged = true** (0 new major/critical, R1 全 major 闭合, 仅留 2 non-blocking minor; 无 oscillation — R1→R2 单向收敛)。

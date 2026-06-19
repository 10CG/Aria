# audit-rubric-runtime-reality-checks

> **Status**: ✅ **SHIPPED 2026-06-19** (aria-plugin v1.47.0, PR #88 merge `281388d` 双远程 parity)。代码侧完成 + reviewed (Cycle B of v1.47.0 issue-sweep release train)。实现 → **agent-team 2-lens review** (knowledge-manager + tech-lead) → 全部 Important/Minor 处置。
> **Review 处置**: I-1 (tech-lead) 数据可用性检查加 **verdict 后果** (缺失→REVISE/FAIL 载重, 非观察性 — 否则重演 #54); I-2 (tech-lead) build gate skip **tri-state** (`not_configured` ≠ pass, 镜像 #141); km-I-1 (A2) post_implementation Code Reviewer 补 数据可用性; M-1 framework 约束清单 3 处重复 → inline 改裸指针 + 枚举只留横切节 (防 drift, memory `feedback_marketplace_json_dual_version_indent`); km-M-1 config type 风格统一; km-M-2 phase-b/spec-drafter 时间戳更新。**澄清**: tech-lead M-2 把 post_implementation 误判 pre_merge (实为 post_implementation, 匹配 TG-B, 无需改)。
> **Level**: 2 (Minimal — proposal + tasks)
> **Target skills**: `aria/skills/agent-team-audit` (rubric SOT) + `aria/skills/phase-b-developer` (build gate) + `aria/skills/spec-drafter` (constraints note)
> **Target version**: → **v1.47.0** (MINOR — 新增审计检查项 + 可选流程步骤; release-train 同批)
> **Forgejo issues**: [Aria #54](https://forgejo.10cg.pub/10CG/Aria/issues/54) (post_spec data-availability) + [Aria #95](https://forgejo.10cg.pub/10CG/Aria/issues/95) (framework-convention build-time blind spot)
> **Rule #6**: prompt/rubric/process 变更于 prompt-driven 能力 skill → 无自动化多-agent 审计质量 AB harness (per memory `feedback_rule6_framing_differs_by_skill_type`)。substitute = **structural 验证** (检查项落位 + scope 正确 + 引用正确 agent/输入) + **dogfood-by-construction** (回放两起实战 incident 确认新检查项会命中)。

## Why

两起实战 incident 暴露同一类盲区:**审计/工具链验证了"逻辑自洽"与"类型/lint/单测通过", 却没验证"运行时/构建期/数据现实"** —— 这类缺陷只在 CI build 或 post-hoc challenge 才暴露, 成本高。

### #54 — 数据可用性 (post_spec 盲区)

TH 项目 v0.3.2 chat MVP post_spec R1 audit (4 agent + Level 3 challenge), **无 agent 验证 spec 断言引用的历史数据前置 (4 周 `raw/source=obsidian` git history) 实际存在**。断言逻辑自洽, 但**环境事实错误**: `raw/` 只有 `.gitkeep` (1 commit, 0 真实 trace)。仅在 owner 事后挑战 baseline 比较意义时才发现 → 触发 R2 吸收 + ~20 行 doc surgery + 1 份补充审计报告。**单次成本 ~半天 + 1 额外审计轮**。

### #95 — 框架约定 (build-time 盲区)

SilkNode US-096 单 session: Wave 1 SDD agent 在 Next.js route handler 加 `export { Prisma }` ("for tests/future use", 0 reference)。Next.js 14 route handler **仅允许 export `GET/POST/...` + metadata**, 任何 named export 触发 build 失败。但 R1 5-agent + R2 2-agent + tsc + lint + 1427 vitest **全过** —— 没人查 framework convention; 只有 CI `next build` 抓到 → **2 次 hotfix redeploy + 诊断, ~30min**。该盲区 generic (Astro page exports / SvelteKit `+page` / client-server 误用 / Remix loaders 等), 非 Next.js 独有。

两者根因同构: **审计 rubric 与本地工具链缺"运行时现实"维度**。

## What Changes

单一 Level 2 Spec, 3 个 task group。

- **TG-A (#54 数据可用性)** — `agent-team-audit/references/audit-points.md` post_spec 检查重点新增 **数据可用性** 检查项 (Tech Lead 下): 当 spec/task 断言引用历史 git 数据 / 外部/环境数据 (commit 历史 / 文件存在 / 数据量 baseline / 外部 API 响应) 时, 审计 agent **必须验证该数据实际存在** (`git log`/`ls`/`wc` 等机械核实), 非仅逻辑自洽。同步 mid_implementation/post_implementation (diff 类) 共享提示。
- **TG-B (#95 T1+T3 框架约定)** — `audit-points.md` post_spec (Tech Lead) + post_implementation (Code Reviewer) 检查重点新增 **框架约定** 检查项: 从 `package.json`/项目配置探测 framework, 对照 framework-specific 约束 (route handler export 限制 / private-folder routing / `use client/server` 误用 / metadata export 白名单 / loader 约定) + 以现有同类文件作 baseline。spec-drafter 加轻量 **Framework Constraints** 可选段提示 (T3-lite)。
- **TG-C (#95 T2 本地 build 验证)** — `phase-b-developer` 在 B.2 test-verifier 后、Phase C 前加**可选** framework build 验证步骤 (config-gated `phase_b_developer.framework_build_check`, **advisory 默认**): 若项目配置了 build 命令, 实施完成后本地跑一次 build, framework convention bug 在本地 (1-3min) 抓而非 CI fail+redeploy (~14min/iteration)。

### 设计原则
- **advisory-over-hardlock** (per memory `feedback_concurrency_advisory_over_hardlock` 同精神): 新审计检查项是检查重点扩充 (post_spec 本就 `blocking: false`); build gate 默认 advisory + config opt-in, 不破坏无 build 的项目 (如 Aria 自身)。
- **通用性** (per memory `feedback_three_layer_universal_workspace_instance`): framework 探测从 `package.json` 等通用信号, 不 hardcode 单一 framework; 检查项措辞覆盖多 framework 类别。

## Impact

- **版本**: v1.47.0 (release-train MINOR)。
- **向后兼容**: ✅ 审计检查项是 prompt 扩充 (既有检查项不变); build gate config opt-in 默认 advisory; 无 build 项目零影响。
- **受影响文件**: `agent-team-audit/references/audit-points.md` (rubric) + `phase-b-developer/SKILL.md` (build step) + `spec-drafter/SKILL.md` 或模板 (Framework Constraints 段) + `config-loader/DEFAULTS.json` (新 config key) + 各 SKILL/README 文档同步。
- **Rule #6**: structural (检查项落位+scope) + dogfood-by-construction (回放 #54 TH-v0.3.2 + #95 SilkNode-US-096 确认命中)。

## Out of Scope

- 自动化 framework 约束库 (per-framework 完整 anti-pattern 清单): 本 Spec 给检查项 + 探测机制 + 代表性约束样例, 不建完整库 (长期迭代)。
- build gate 设为 hardlock blocking: 默认 advisory; 项目可 config 升级到 blocking (字段预留, 不在本 Spec 强制)。
- 把 framework-convention 做成独立 agent (#95 T1 备选): 采用"加检查重点到现有 agent"而非新增 agent (避免 agent roster 膨胀 + session-start 加载成本, per memory `feedback_dynamic_agent_session_start_vs_soft_injection`)。

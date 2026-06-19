# Tasks — audit-rubric-runtime-reality-checks

> ✅ SHIPPED 2026-06-19 (v1.47.0, PR #88 `281388d`)。Cycle B of v1.47.0 release train。#54 + #95。doc/prompt/process 变更; Rule #6 = structural + dogfood-by-construction。

## TG-A — #54 数据可用性检查项
- [x] A1. `agent-team-audit/references/audit-points.md` post_spec → Tech Lead 检查重点加 **数据可用性**: 断言引用历史 git / 外部 / 环境数据时, 机械核实数据实际存在 (`git log`/`ls`/`wc`), 非仅逻辑自洽。
- [x] A2. diff 类检查点 (mid_implementation/post_implementation) 共享一行提示 (引用同原则)。

## TG-B — #95 框架约定检查项 (T1 + T3-lite)
- [x] B1. `audit-points.md` post_spec → Tech Lead 加 **框架约定** (从 package.json 探测 framework + 对照 framework-specific 约束 + 同类文件 baseline)。
- [x] B2. `audit-points.md` post_implementation → Code Reviewer 加 **框架约定** (route export 限制 / routing 约定 / client-server / metadata 白名单)。
- [x] B3. `spec-drafter` 加轻量 **Framework Constraints** 可选段提示 (T3-lite)。

## TG-C — #95 T2 本地 build 验证 (advisory)
- [x] C1. `config-loader/DEFAULTS.json` 加 `phase_b_developer.framework_build_check` (默认 advisory + 无命令则 no-op)。
- [x] C2. `phase-b-developer/SKILL.md` B.2 后加可选 framework build 验证步骤 (config-gated; 跑配置的 build 命令; advisory 默认; 文档说明成本对比 CI fail+redeploy)。
- [x] C3. config-loader SKILL 配置表同步新字段。

## TG-D — 验证 (Rule #6 substitute)
- [x] D1. structural: 检查项落在正确 checkpoint/agent; 引用正确输入 (package.json / git / ls); 措辞通用 (多 framework)。
- [x] D2. dogfood-by-construction: 回放 #54 (TH raw/ 只有 .gitkeep → 数据可用性检查会要求 `ls raw/`+`git log` 命中) + #95 (SilkNode route export → 框架约定检查 + build gate 命中)。
- [x] D3. 无 build 项目 (Aria 自身) 零影响验证 (config 默认 advisory/no-op)。

## Phase B/C/D (release train)
- [x] agent-team review (knowledge-manager doc 一致性 + tech-lead rubric 设计合理性)。
- [x] commit 到 release 分支 feat/v1.47.0-issue-sweep。
- [x] 随 v1.47.0 批量 Phase D ship + close #54/#95 + 归档。

# 决策存档: DEC-20260731-001 — C.2.4 verdict=wait 人工裁决过渡规则退役 (#122 机制落地)

> **日期**: 2026-07-31 | **性质**: 裁决记录存档 + 退役 | **触发**: aria-plugin #122 ship (v1.65.0)
> **存档理由**: 2026-07-25 owner 复议裁决此前唯一书面原件嵌在 `.aria/config.json` JSON 注释里
> (post_spec 审计 KM-5); 本文件在改写那些注释**之前**完整存档原文, 使判例链不因改写丢失。

## 原文 (逐字, 改写前的 `.aria/config.json` `phase_c_integrator` 三注释字段)

### `_comment` (2026-07-22 落配置)

> Rule #8 C.2.4 pre-merge gate 的显式声明 (2026-07-22 落配置; 2026-07-25 owner 复议后重写立场). 本仓 (Aria meta-repo + aria-plugin 子模块) 的 CI 全部路径过滤: aria 唯一 workflow .forgejo/workflows/issue-triage-tests.yml 仅在 skills/issue-triage/** 触发; 主仓 CI 仅在 orchestrator 相关路径触发。⇒ 任何落在这些路径之外的变更 **结构上永远不会产生 CI run**, 而 backend 把 '零 run' 映射成 pending (ci_backends/aether.py: `if not runs: return "pending"`), gate 因此恒返回 verdict=wait, 等到 wait_timeout 也不会变。

### `_lane` (2026-07-25 owner 复议重写版)

> ⚠️ 本注释经 2026-07-25 owner 复议后重写 —— 前一版 (Phase C v1.64.0 时写) 把它框成「已确立 lane」是**错的, 已废止**。事实认定 (复议结论): Rule #8 的**成文** exception 触发条件是「所有 backend probe=False」(SOT: aria/skills/phase-c-integrator/SKILL.md §C.2.4「无可用 backend」条 [line 285]; CLAUDE.md 规则 #8 为精简指针 — 用 section anchor 非行号引, 因 CLAUDE.md 2026-07-22 由 639→149 行, 行号引用已烂过)。而本仓路径过滤致 **verdict=wait** (backend probe=True + 零 run 映射为 pending) 是**另一个分支, 成文条件不覆盖**。把 verdict=wait 当成 skip 是被审方用成文机制没覆盖的条件自我豁免 —— Rule #10 反模式。v1.54.0/55.0/55.2/v1.64.0 是 4 次错过机制化, 不是「先例 lane」。地位: **不是自助 lane, 不授权任何 AI 自我豁免 C.2.4**。v1.64.0(#113) 实例经 owner 一次性 ratify (2026-07-25), 仅此一次, 不构成先例。过渡规则 (✅ owner 定案 2026-07-25): (1) #122 (路径覆盖感知 not_applicable 态) **优先落地**, 是唯一真机制; (2) 在 #122 前, 遇 C.2.4 **verdict=wait** 一律**上报 owner 裁, 不自我豁免**。⚠️ 诚实声明: 本规则 (2) 当前**仅文档级** —— 它约束的是 AI 编排层行为 (verdict=wait 由 workflow-runner wait_recoverable 处理, 无 config 键能机械强制「超时后不放行」), 只有 #122 落地才把它变成机械态。与 no_ci_fallback (probe=False 分支) **正交, 未改**。

### `_not_ci_backends_empty`

> ⚠️ 刻意 **不** 设 ci_backends:[] —— 那会触发 no_ci_fallback 对**所有**变更跳过闸门, 包括真有 CI 覆盖的路径, 等于用假绿换恒红。完整机制化 (区分「无覆盖」与「pending」) 属代码变更, 见 aria-plugin#122 (路径覆盖感知的 not_applicable 态; owner 2026-07-25 定案优先)。

## 退役裁定 (2026-07-31)

- 过渡规则 (1) — 「#122 优先落地」: **已兑现** (aria-plugin v1.65.0, spec
  `phase-c-gate-path-coverage-not-applicable`, post_spec R1-R4 CONVERGED, owner
  sign-off 2026-07-27 含 `path_coverage_enabled` 默认 true 单独批)。
- 过渡规则 (2) — 「verdict=wait 一律上报 owner」: **随机制落地终结** (与主仓 gitlink
  bump 到 v1.65.0 同 commit co-land, 消除规则已退/机制未 pinned 的空窗)。此后
  verdict=wait 真正意味着「CI 在跑或该跑没跑完」, 按 workflow-runner wait 正常处理。
- 替代义务 (SKILL.md §C.2.4 v1.65.0+): not_applicable 放行必须 surface 警告行;
  `path_coverage.decision=unknown` 必须上报评估器失败 — 跳过不静默, 失效不静默。
- `_open_question_no_ci_fallback` (probe=False 分支政策) **保持挂起不动** — 与
  verdict=wait 正交的独立问题, 仍归 owner。
- 首个生产判定: v1.65.0 自身的 C.2 合并 (meta-dogfood) — verdict=green via
  not_applicable, 六次复发场景 (v1.54.0/v1.55.0/v1.55.2/v1.64.0/v1.64.1/本次)
  第一次零人工裁决走正门。

## 交叉引用

- Spec: `openspec/archive/2026-07-31-phase-c-gate-path-coverage-not-applicable/`
- Issue: 10CG/aria-plugin#122 | 审计: `.aria/audit-reports/post_spec-R{1,2,3,4}-1785112156889-*`
- 上一份同族裁决: DEC-20260722-001 (AB baseline 污染根因修复)

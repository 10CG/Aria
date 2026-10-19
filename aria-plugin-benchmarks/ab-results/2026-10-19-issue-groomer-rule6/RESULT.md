# issue-groomer v1.77.0 候选 — Rule #6 结果记录 (2026-10-19)

> Spec: openspec/changes/issue-groomer-p1-mvp (Approved + Phase 0 六裁定 + Amendment #1-#4)
> 被测: aria feature/issue-groomer-p1-mvp @ 8b1e920 (description 终版含只读边界句)
> 套件: ab-suite/issue-groomer.json v1.0.0 (场景 1 行为套件 5 evals / 26 断言, TASK-012 载体) + trigger/issue-groomer.json (20 条, owner 审阅通过 裁决 a)

## 场景 1 — Skill 指令面 AB (双臂, 2026-10-19)

| 臂 | 断言 | 结果 |
|---|---|---|
| **with_skill** (SKILL.md 逐字加载) | **26/26** | **全绿** — E1 conflict 待归边/unknown 不猜/exit1 不半份 ✅; E2 链路 ✅; E3 占位符 title/orphaned/Tier B 全 stale Tier A 免 ✅; E4 entry 契约键+context_key 逐字 live 值 (实跑沙箱 ae63be96...) ✅; E5 差集+结构幂等 ✅ |
| without_skill (baseline) | 21/26 | E1 ✗3 (conflict 自行归边取 feature / 半份降级报告 / 无 groom.py 面); E3 ✗1 (closed 用真实标题非契约占位符); E4 ✗1 (entry 键自拟 + context_key 以 taxonomy_hash 充当非契约值) |
| **delta** | **+5** | 门判: **PASS** (with_skill 定向全绿; 新 skill 首基线) |

**污染面申报 (判分依据 #116/DEC-20260722-001)**: without 臂非零 context — 自动加载 CLAUDE.md (十步循环/Rule#1/#2, 其项目状态行恰为 E4 材料证据之一) + 主动读了真实 `.aria/cache/groom-state.json` 与 `.aria/config.json` (E1/E3/E4 的 schema 与值域部分源于此 skill 的 runtime 工件) — baseline 21/26 中的 E2 全对与 E3 大半对系污染红利; 判分只按断言原文对照, 未因污染折减 (delta +5 为保守下界)。

**产出形态**: 双臂均 descriptive (套件钉死); with_skill 臂另做只读纯函数核验 (tier_a/incremental/diffseg 直调) 与 E4 沙箱实跑 (scratchpad/ab-withskill-eval4/, 真仓零写, state/assessments 隔离)。

## 场景 4b — description 地板守卫 (双臂, 2026-10-19, 运行中)

- 被评臂: 真 description (SKILL.md @ 8b1e920); 负控臂: 「对一个事项做处理。」(SOT 泛化句构造, 基线 v5 实测 0/10 形态)
- 参数 (SOT 钉死): runs-per-query 3 / threshold 0.5 / timeout 120 / workers 1 / model glm-5.3 (本 session 模型; CLI 静态表外警告为环境已知形态, 调用 exit 0) / claude-shim + --setting-sources project / 独立 project root (v2 形态)
- 结果: 见 trigger/ 目录 (运行完成后回填)
- 套件审阅: owner 2026-10-19 裁决 a (基于 AI 建议 + owner 确认; description 补只读边界句使 #16 在触发面诚实可判) — **首个入库 trigger 套件, #213 T4 解冻先例**

## 判据表第一行 substitute (groom.py 纯代码)

结构化测试替代: **525 tests + 57 subtests 全绿** (B.3 终态 63b7772; 含 11 态矩阵 / 分量级 mandate / 每判据反事实 / mutation 34 处全灭)

## 判据表第三行 (Tier B prose)

定向 fixture: `ab-suite/issue-groomer/tier-b-fixtures/` 7 用例 (3正/3反/1边界, TASK-011, 主仓 f3555f9); 判读协议 = 独立评估席非作者, pass/fail/miss 三档

## rule6_note (SOT §4.1 五字段 × 四变更面, 成文待 4b 完成后终填)

(占位 — 4b 门结果出来后四条全填)

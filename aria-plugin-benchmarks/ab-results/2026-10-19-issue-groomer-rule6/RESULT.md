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
- **结果: 被评臂 FAIL** (should-trigger query 门 4/10 [门=10/10], 地板 13/30 [≥28], should-not 误触 3/10 [≤5 ✓]); 逐调用健康检查 verdict=**fail** (3 不健康调用, 门判定双极端不变, 非 void); **负控臂 valid** (误命中 1/10 ≤5 ✓, 套件区分力成立 — 泛化句几乎不触发, 真 description 部分触发)
- 根因定性: **glm-5.3 via Luxeno 随机 narrate-不发 tool_use** (失败 run 流内仅 thinking+text「我先调用…技能」后结束, 零 tool_use 块; 同查询 3 run 触发 0-3 不等, per-run 总体 43%) — description 语义匹配无恙; **#214 已知缺口(6) 实证坐实** (4b 此前仅 Claude 模型实测; 本环境 claude CLI 全别名路由 GLM, 无真 Claude 通道, opus/fable 探针 stderr 均显示 luxeno-an,glm-5.3)
- 处置: SOT fail 二选一 (修 description / 改套件) 均不适配根因 ⇒ 升级 owner (Rule #10)
- **owner 裁定 (2026-10-19)**: 该现象其他场景亦遇到 ⇒ **先反馈 SilkNode 找实际根因, 再回来推进** — 已开 **10CG/SilkNode#1270** (60 调用实证 + 全量流日志 + 复读退化样本); v1.77.0 ship 暂缓至根因回填
- 套件审阅: owner 2026-10-19 裁决 a (基于 AI 建议 + owner 确认; description 补只读边界句使 #16 在触发面诚实可判) — **首个入库 trigger 套件, #213 T4 解冻先例**

## 判据表第一行 substitute (groom.py 纯代码)

结构化测试替代: **525 tests + 57 subtests 全绿** (B.3 终态 63b7772; 含 11 态矩阵 / 分量级 mandate / 每判据反事实 / mutation 34 处全灭)

## 判据表第三行 (Tier B prose)

定向 fixture: `ab-suite/issue-groomer/tier-b-fixtures/` 7 用例 (3正/3反/1边界, TASK-011, 主仓 f3555f9); 判读协议 = 独立评估席非作者, pass/fail/miss 三档

## rule6_note (SOT §4.1 五字段 × 四变更面, 成文待 4b 完成后终填)

(草稿 rule6_note-draft.yaml; 终态待 owner 裁定)


## 4b 第三轮 (description v2 @ 25be385, SilkNode 修复后, 2026-10-21)

- **被评臂**: should-trigger **10/10 + 地板 30/30** (Portkey 修复完全兑现, v1 轮 4/10+13/30 → 修复后两轮均满) / should-not 误触 **9/10** (v2 收窄无效 — description 负面边界前移零效果)
- **负控臂**: 误命中 4/10 ≤5 ✓ valid; 双臂健康检查 0 不健康调用
- **根因定性 (升级)**: **4b 单技能沙箱结构性无法评估兄弟路由边界** — #13 纯状态查询 (state-scanner 域, 与 groomer 能力无交集) 零 narrate 直接调 Skill: 唯一在场的技能承接一切路由, description 的「单条→issue-triage / 快照→state-scanner」边界在 issue-triage/state-scanner 不在场的沙箱里无从生效。基线 openspec-archive 的 should-not 有效系其近邻为**能力外**任务 (changelog/目录整理), 不需兄弟路由 — 两种 should-not 设计前提不同
- **SOT 处置轨迹**: 处置(1) 修正 description — 已走 (v2) 且实证无效; 处置(2) 改套件 — 需 owner 审且会把沙箱伪影固化为规范, 不推荐 ⇒ **升级 owner**

## 场景 1 重跑轮 (description v2, 2026-10-21)

with_skill 臂 **真跑形态** (沙箱全执行): **26/26 全绿** (E1 exit1 真跑复现+四分类逐字 / E3 三情境真跑含 state md5 比对+context_key 变化真值 / E4 entry 机读常量自检); without 臂沿用 21/26 (不受 description 影响)。**双轮 26/26 稳定**。

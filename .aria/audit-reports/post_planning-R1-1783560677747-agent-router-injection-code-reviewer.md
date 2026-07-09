---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-07-09T01:09:50.127Z
context: openspec/changes/agent-router-auto-project-agent-injection/detailed-tasks.yaml
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 审计结论

**被审对象**: detailed-tasks.yaml (18 tasks, planned_at 2026-07-09) @ 主仓 2067ddf + aria 93b7406 (实测 HEAD 一致)。

### 做得好的 (不挑刺处)

1. **三层对齐零漂移**: 18/18 task 与 tasks.md 一一对应 (id/TG 归属/标题语义/AC 划分全同); yaml 还把 R4 findings 精确下沉到 task 粒度 (TASK-001 归一失败剔除+WARN = c2e66062; TASK-005 manual 注释修正 = f8b35406; TASK-003 有序四分支 = bd89d02f; TASK-006 last_full_scan int epoch = f8b8ca9e)。
2. **行号/§ 锚全部真实** (逐一抽查源文件): SKILL.md L17 (`1.0.0` header) / L449 (`1.1.0` footer) / §205 执行流程 / §221 step3 四平级子项 (「忠实 4+1」前提成立) / §232 短路 return / §277 legacy config / §393 孤儿段 / 连带 10 段 (§35/§47/§93/§132/§145/§250/§305/§323/§383/§438) 全命中; ROUTING_RULES L3 (`1.0.0`) + 维护指南 L255 现状三类 (五类扩展前提成立) + L177-185 glob 示例 (AC-12 佐证注为真); DEC-20260621-001 L13/L90 grep 精确命中; US-011 三锚点 (AC 第 4 条 L51 / D4 L43 / Scope L57-61); marketplace.json 两处 version (L3/L16); config.template 现无 agent_router 块 (TASK-009 待补成立)。
3. **AC 覆盖矩阵完整且归属唯一**: AC-1..16 全承接 (13 个裁决类→TASK-013; AC-3→TASK-014 独占; AC-15→TASK-015; AC-9a/9b 拆分落 TASK-017/018, 正确执行 R4 918a4d69); What §1-§6 无内容失承接, 无 scope creep。
4. **DAG 无环** (Kahn 机械验证); metadata 五字段 (feature/datasource/spec_level=3/spec_rev=Rev4/total_tasks=18) 与实际一致; 分工符合项目动态分工惯例 (两文件咬合成文=main-loop 亲验, TG-D 实跑=subagent 并行+main-loop 机械断言); TASK-009/011/018 Phase C 注记与 tasks.md「主仓文件随 Phase C 落地」+ sequenced gitlink bump 惯例自洽。

### Major (需 rework, 均一行可修)

1. **依赖图缺 4 条边** — Kahn 拓扑实测 TASK-004/009/010/011 为零依赖方孤儿叶节点, 与 TASK-018 断连: TASK-017 (AC-9a 核对 taxonomy) 不依赖 TASK-010; TASK-018 (AC-9b 核对 config.template/US-011/DEC, 标题自述「TASK-009/011 落地」) 不依赖 TASK-009/011; TASK-012 (「注入新 SKILL/**RULES 全文**」) 不依赖 TASK-004 (RULES 最后一笔)。execution_order prose 正确但机读 DAG 按拓扑调度会错序。修: 补 4 条边 + TASK-009/011 note 明确「完成=内容备好, commit 归 018」(消 #95 勾选歧义)。
2. **旧基线文本供给缺口** — TASK-014 (AC-3 零回归三支「旧 vs 新 SKILL 文本」, Rule #4 裁决载体) 与 TASK-013 内 AC-13 (「与旧基线对照一致」) 都需要旧文本基线, 但 TASK-012 verification 只注入**新**文本, 无 task 声明旧文本来源 (哪个 SHA) / 旧基线是否双跑 / 记录落点 → AC-3 判定自由裁量。修: TASK-012 增「旧文本 runner 实例 (git show 93b7406:…SKILL.md)」deliverable。
3. **TG-D 并行窗与 AC-14 mutation 竞态** — (013∥014∥015) subagent 真并行 + 共享单一 fixture 目录, 而 AC-14 要求原地编辑 agent capabilities (字节数改变) 且无隔离/还原声明 → 并行读者与双跑依调度时序取到不同 capabilities → 双跑不一致被 spec 规则误判「SKILL 文本歧义」回炉 (错误归因)。修: AC-14 专属可变 fixture 副本, 或声明尾置串行+编辑后还原。

### Minor (advisory)

4. tasks.md L3 头标「Rev3」滞后 (proposal=Rev4, yaml=Rev4; 正文已按 R4 更新) — 一字修。
5. TASK-008 verification「无 1.0.0/1.1.0 残留 (除 changelog 语境)」必然假阳性: §393 标题「(v1.1.0)」引入标注 + B12 要求保留「v1.1.0 §416」语义引用均非 changelog — 改为锚定式断言 (L17/L449=1.2.0 + 显式豁免清单)。
6. 验证类 deliverables (TASK-012~015/017) 无落盘路径约定 (#95 gate 核验无锚); TASK-018 通配符 `DEC-20260621-001-*.md` (011 用全名) + `gitlink` 非路径 — 统一落点 + 展开全名。

## Verdict

**PASS_WITH_WARNINGS** (0 Critical + 3 Major + 3 Minor) | **vote: REVISE**

规划骨架忠实且锚点扎实, 不需要重规划; 3 个 Major 都是局部补丁 (共约 6-8 行 yaml 修改), 修完可直接进 B.1。

## 核验锚点

- `openspec/changes/agent-router-auto-project-agent-injection/detailed-tasks.yaml:87,93,112,122-125,128-131,137-143,158,167-169,173-180,182-185`
- `openspec/changes/agent-router-auto-project-agent-injection/tasks.md:3,28-31,37,41-42`
- `aria/skills/agent-router/SKILL.md:17,205,221,232,277,393,449` + 连带 10 段行号全核
- `aria/skills/agent-router/ROUTING_RULES.md:3,177-185,251-255`
- `docs/requirements/user-stories/US-011.md:43,51,57-61`; `.aria/decisions/DEC-20260621-001-*.md:13,90`
- `aria/.claude-plugin/marketplace.json:3,16`; `.aria/config.template.json`; 主仓 `VERSION` + `README.md:8,242`
- 机械验证: yaml.safe_load 18/18 + Kahn 无环 + 孤儿叶节点 [TASK-004,009,010,011]; aria HEAD=93b7406 与 anchor 一致
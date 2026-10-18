# issue-groomer P1 MVP — Tasks

> 双层架构: 本文件粗粒度 (功能层); detailed-tasks.yaml 由 A.2 task-planner 生成 (含 Agent 分配/文件路径/验证映射)。
> v2: 新增 Phase 0 裁定门 (R1 依赖倒置修正); 1.3 重写为逐 SC 映射; v1 2.2 (五项待裁) 并入 0.1 (六项); v1 2.3 重编号为现 2.2 (Tier B fixture)。
> v3: SC-6 恢复四 facet 判绿 (R2 修复回归) + 4.2 ship 前置补 task 3.1/2.2 + 1.3 SC-4 补两条 facet fixture + 1.1 恢复 SC-8 括注。

## Phase 0 — 裁定门 (owner, interactive — **已完成 2026-10-18**)

- [x] 0.1 六项裁定 (owner 2026-10-18, 全文见 proposal §0): ① 项目级 labels.yaml 优先+内置默认 fallback (覆盖非合并) / ② schema = scripts/groom-report.schema.json / ③ provenance 分层采集 / ④ 两文件各自 last-writer-wins (assessment 独立文件; 并发 fixture 升正式态) / ⑤ 保持两张 / ⑥ 恒阻塞至解冻 (fail-closed 无逐案放行)

## Phase 1 — 机械核 (groom.py + 测试)

- [ ] 1.1 groom.py 基础层: 双端点全分页 fetch (issue-list + comments, 排序语义钉死) + Tier A 规则引擎 (逐信号 confidence / unknown 不猜 / 时钟 seam / 前缀表读 labels.yaml) + comments 分量三态 (值/null/unknown) + groom-report JSON schema v1 **(additive-only 契约文档化, 文档落点随裁定门② — SC-8)**
- [ ] 1.2 增量引擎: 三面指纹 (显式排除集) + 复用规则 (Tier A 判据输入快照 / Tier B provenance 门 + stale-assessment + assessment 保留约定) + diff 段 + 状态文件原子写
- [ ] 1.3 SC 结构化测试 (逐 SC 映射): SC-1 10 态矩阵 + **第 11 态并发 fixture (两文件各自 last-writer-wins, 裁定④)** + 分量级 mandate (③ 四分量变体 / ⑨ 两分量变体 / ⑩ comment-edit 判别 + 合成 updated_at>created_at 样本) / SC-2 双端点分页 + >50 截断反例 / SC-3 每判据反事实 + 负面 fixture / SC-4 baseline-run + top-N fixture + 三态 fixture + 复用规则 fixture (判据输入变而分类输出同 ⇒ 重分类不复用) + provenance 门 fixture (provenance 变 ⇒ stale-assessment) / SC-5 差集断言 + 幂等 (mock 不编码 no-op) / SC-9 taxonomy 自检 / 语料接入 (三路径) + forgejo add no-op live 实测 (10cg.local, 结果落 references) + 语料再生成命令

## Phase 2 — 适配层

- [ ] 2.1 SKILL.md (CC 适配层): Tier B 语义评估流程 (assessment 面 + provenance + 持久化回路) + MD 渲染层 + 多 harness 诚实主张声明 + 双源同步义务预告承载
- [ ] 2.2 Tier B 定向 fixture (判据表第三行, #240 勘正后范围: 仅 Tier B 语义行为 — 疑似已修判断/优先级 vs 在制轨/决策面抽取的可证伪用例)

## Phase 3 — Rule #6 与发版准备

- [ ] 3.1 Rule #6 执行: 场景 1 AB 照跑 + rule6_note 按 SOT §4.1 五字段×四变更面成条 (含 negctrl 口径) + 4b 按 SC-6 两分支处置 (#239)
- [ ] 3.2 发版准备: MINOR bump 草案 + 版本 SOT 五文件同步准备; trigger 套件如已解冻则入库

## Phase 4 — Dogfood、Ship 与收尾 (ship 在 dogfood 后)

- [ ] 4.1 dogfood: Aria 仓实跑 (判绿 = SC-7 全量对账 + 手工梳理差异逐条归因) + 外项目试点 (Aether 97 或 SilkNode 63)
- [ ] 4.2 ship (dual-push, 前置 = 4.1 通过 + **task 3.1/2.2 完成 + SC-6 四 facet 全绿 (⑥ = 未解冻恒阻塞, 无逐案放行)**) + 归档 + 关单 (#238; #239 恒随解冻状态 — 未解冻不关且 ship 阻塞; #240 随 Tier B fixture 完成关) + handoff

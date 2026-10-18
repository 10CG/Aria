# issue-groomer P1 MVP — Tasks

> 双层架构: 本文件粗粒度 (功能层); detailed-tasks.yaml 由 A.2 task-planner 生成 (含 Agent 分配/文件路径/验证映射)。

## Phase 1 — 机械核 (groom.py + 测试)

- [ ] 1.1 groom.py 基础层: 全分页 fetch (多仓配置复用 issue_scan 形态) + Tier A 规则引擎 (逐信号 confidence / unknown 不猜) + groom-report JSON schema v1 (additive-only 契约文档化)
- [ ] 1.2 增量引擎: 三面指纹 (issue/上下文/provenance, 显式排除集) + 复用规则 (Tier A 判据输入快照 / Tier B provenance 门 + stale-assessment) + diff 段 (集合差/漂移 top-N/baseline no-diff) + 状态文件原子写
- [ ] 1.3 SC 结构化测试: 10 态 fixture 矩阵 (逐态反事实) + Tier A 每判据反事实 + 负面 fixture + taxonomy 一致性自检 + 语料接入 (三份快照)

## Phase 2 — 适配层与裁定

- [ ] 2.1 SKILL.md (CC 适配层): Tier B 语义评估流程 (assessment 面 + provenance) + MD 渲染层 + 多 harness 诚实主张声明
- [ ] 2.2 五项待裁裁定 (owner): labels.yaml 落点 / 契约面资产落点 (含 groom.py 最终路径) / provenance 取值源 / 第 11 态 (last-writer-wins) 二选一 / 两缺口单是否合并
- [ ] 2.3 Tier B 定向 fixture (判据表第三行, #240): 点名行为 + 可证伪 + 移交附注三条 (既有评论编辑用例 / ③ 态四分量变体 / ⑩ 先例沿用)

## Phase 3 — Rule #6 与发版

- [ ] 3.1 Rule #6 执行: 场景 1 AB 照跑 + 场景 4b 处置留痕 (#239, trigger 套件缺口单) + rule6_note 成文 (档位矩阵四行)
- [ ] 3.2 发版面: MINOR bump + 版本 SOT 五文件同步 (plugin.json/CHANGELOG/README/…) + trigger 套件如已解冻则入库

## Phase 4 — Dogfood 与收尾

- [ ] 4.1 dogfood: Aria 仓实跑 (150 条语料, 与手工梳理结果对照) + 外项目试点 (Aether 97 或 SilkNode 63)
- [ ] 4.2 归档 + 关单 (#238 / #239 / #240) + handoff

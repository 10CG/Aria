# Tasks — concurrent-session-upm-safety (合并版)

> 粗粒度功能任务 (Phase.Task)。编号一旦创建不可变。**严守 advisory-over-hardlock (DEC-20260519-001)**。
> 合并自两个 #133 Spec (本 (b)convention + sister (a)/(c) 机制)。主解药 = convention (Phase 2), 检测/fetch = 辅助。

## 0. 【前置·共同依赖】collision 字段持久化 (sister R1 C1 phantom-field fix)

- [ ] 0.1 抽 `_classify_collision` (renderer-local) 为共享 helper `classify(tracks)` → `{kind, groups}` (同 owner+container→none); **新函数**非直接 promote (sister R2-CARRY #2)
- [ ] 0.2 `handoff_multibranch` collector 调用 + 持久化 `tracks_multibranch.collision` (additive, bump schema); helper 配 unit test 跑**真实** collector 输出 fixture
- [ ] 0.3 `track_board` renderer 改读共享字段 (回归 0; 老 snapshot 无字段 → fallback) + meta-fix `layer-l-integration.md:23,69` stale 字段名
- [ ] 0.4 Phase B 评估: 此项 (含 `_track_to_claim_record→reconcile_all` 链) 是否拆独立 prereq Spec (sister R2-CARRY #1)

## 1. 设计边界确认 (锚定双审计定案)

- [ ] 1.1 确认不 auto-enable/不硬锁; 主解药=convention (Phase 2), 检测/fetch=advisory 辅助
- [ ] 1.2 复用边界: tracks_multibranch 无条件采集 / coordination.enabled 是 config 键非 snapshot / C.2.4.5 fail-hard ≠ 本 fail-soft / History prepend-desc L5 不可改
- [ ] 1.3 #54 = **独立 + 交叉引用** (不合并)

## 2. 【主解药】UPM/handoff concurrent-safe 约定 (standards convention, 先行)

- [ ] 2.1 共享区 (line-3 pointer / UPM body) append-friendly 或 per-session 隔离 (History prepend-desc 不动, L5)
- [ ] 2.2 followup `#NNN` 表避免多 session 改同一 row (per-session sub-row / 轻量标记, 非复用 claim_lifecycle)
- [ ] 2.3 AI 记录外部状态硬证据自律 (RETURNING/显式 timestamp, 禁 updated_at 软代理; 作用域=AI 记录非用户 DB; #54 交叉引用)
- [ ] 2.4 单 session 优雅降级 + 正/反 pattern + exception; 落 standards/conventions/

## 3. 【验收防线】convention 机械 guard 评估

- [ ] 3.1 评估轻量 checker (followup dup-row / 共享区违规) vs 纯文档 dogfood
- [ ] 3.2 按结论: 实现 guard (含自测) 或 明确 dogfood 验收标准

## 4. 【辅助·早发现】切口2 — 并发 churn 检测 (state-scanner, advisory)

- [ ] 4.1 阶段 2 advisory iff `tracks_multibranch.collision.kind != none` 且 config `coordination.enabled == false` (config 读非 snapshot)
- [ ] 4.2 **disjointness**: 切口2 iff enabled==false; cross_owner→phase1_gate iff enabled==true (enabled 互斥, 绝不双触发)
- [ ] 4.3 提示含一键启用 config 片段; 判定不依赖"谁" (collision helper 按 owner+container 归类)
- [ ] 4.4 fixture (真实 collector 输出, 含边界): 并发→提示; collision none + behind 0 → 不出现 (负向 AC-3)

## 5. 【辅助·写前同步】切口1 — phase-d-closer 收尾 fetch-gate (fail-soft)

- [ ] 5.1 D.1 写 UPM 前: default-branch 解析 (symbolic-ref→master→main, sync.py:36-41 chain)
- [ ] 5.2 fresh fetch (timeout=30, 独立 1.16 缓存); 失败仅复用 coordination_fetch error_kind + soft-warn, **不回显 raw stderr**, 不阻塞
- [ ] 5.3 behind-check (git.py:167 手法); 触发 iff `behind>0 且 (collision.kind!=none 或 commits 触及 upm.source_file)`; 触及 UPM→强提示; 纯 behind>0→静默
- [ ] 5.4 fixture: origin ahead + UPM-touch commit → 强提示; ahead 非 UPM + collision none → 静默; 离线 → soft-warn 不阻断 (测 fail-soft 路径)

## 6. 文档同步 + 收尾 (Rule #3 + self-dogfood)

- [ ] 6.1 CLAUDE.md 信息地图索引 convention; state-snapshot-schema.md additive collision 字段
- [ ] 6.2 全量回归 PASS (state-scanner + phase-d-closer 零退化); Rule #6 structural substitute
- [ ] 6.3 **self-thrash dogfood**: 本 Spec ship 先用自己的 append-only/fetch-before-edit (per `feedback_meta_dogfood_solution_validates_self_mid_ship`)
- [ ] 6.4 版本 bump (ship 前复核) + 多远程推送 + post-push SHA 验证 + Spec 归档 + 关闭 #133

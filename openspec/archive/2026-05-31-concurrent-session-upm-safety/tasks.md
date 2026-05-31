# Tasks — concurrent-session-upm-safety (合并版)

> 粗粒度功能任务 (Phase.Task)。编号一旦创建不可变。**严守 advisory-over-hardlock (DEC-20260519-001)**。
> 合并自两个 #133 Spec (本 (b)convention + sister (a)/(c) 机制)。主解药 = convention (Phase 2), 检测/fetch = 辅助。

## 0. 【前置·共同依赖】collision 字段持久化 (sister R1 C1 phantom-field fix)

> **R1 裁定 (不拆独立 Spec)**: 无独立用户价值 → 本 Spec 内拆 0a/0b。**真实管线** = `tracks[]→_track_to_claim_record(lossy,可 raise)→reconcile_all→_classify_collision(claims: list[ClaimRecord])`, **非抽函数** (R1 C1)。

- [ ] 0.0 **meta-fix 前置 (最先执行)**: 修 `layer-l-integration.md:23,69` stale phantom 字段名 `collision_type`/`has_collision` (从未实现, 防 AI 读旧文档传播 phantom; R1 C2)
- [ ] 0.1 **(0a-helper)** 新建共享模块 (e.g. `lib/collision.py`) 封装整条管线为 `classify(tracks) -> {kind: none|cross_owner|self_multi_container, groups: list[list[str]]}`; 内部经 `_track_to_claim_record` (处理其可 raise ValueError) + `reconcile_all`; **render-only emoji 丢弃**; 同 `(owner,container)` 全相同→none 排除 self-serial (R1 M3); helper 输入是转换后 `list[ClaimRecord]` 非 `tracks[]` 直喂 (R1 C1/I3)
- [ ] 0.2 **(0a-collector)** `handoff_multibranch` collector 调用 `classify` + 持久化 `tracks_multibranch.collision` (additive, bump schema); 配 unit test 跑**真实** `collect_handoff_multibranch` 输出 fixture (非手搓 schema)
- [ ] 0.3 **(0b-renderer)** `track_board` renderer 改读共享 `collision` 字段 (回归 0; 老 snapshot 无字段→`.get()` fallback `{"kind":"none","groups":[]}`)
- [ ] 0.4 **持久化 collision 字段标注 advisory-only** (R1 I5): schema 文档明确该字段不作任何 gating 输入 (lossy approximation 不升格决策依据)

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

- [ ] 4.1 阶段 2 advisory iff `tracks_multibranch.collision.kind != none` 且 config `coordination.enabled == false` (config 读非 snapshot; **读取插入点 = scan 推荐逻辑层, 非 renderer/collector**, R1 I8)
- [ ] 4.2 **disjointness**: 切口2 iff enabled==false; cross_owner→phase1_gate iff enabled==true (enabled 互斥, 绝不双触发)
- [ ] 4.3 提示含一键启用 config 片段; 判定不依赖"谁" (collision helper 按 owner+container 归类)
- [ ] 4.4 fixture (真实 collector 输出, 含边界, **三态** R1 I6): (a) enabled==false+collision!=none→提示; (b) enabled==true+collision!=none→切口2 不出现 (phase1_gate 处理); (c) enabled==true+collision==none→均不出现; (d) collision none + behind 0 → 不出现 (负向 AC-3)

## 5. 【辅助·写前同步】切口1 — phase-d-closer 收尾 fetch-gate (fail-soft)

- [ ] 5.0 插入点: `phase-d-closer/references/execution-steps.md` D.1 action 起始, 写 UPM **前**新增 fetch-gate 子步骤 (R1 I8)
- [ ] 5.1 D.1 写 UPM 前: default-branch 解析 — **自实现** `git symbolic-ref refs/remotes/origin/HEAD`→fallback `origin/master`→`origin/main` (**无现成 resolver 可调**; sync.py `_ORIGIN_HEAD_REFS` 仅 fallback 顺序数据常量, R1 I1)
- [ ] 5.2 fresh fetch (timeout=30, 独立 1.16 缓存); 失败仅复用 `coordination_fetch._classify_error` 的 error_kind enum (`network`/`auth_403`/`non_ff`/`git_missing`/`other`) + soft-warn, **不回显 raw stderr**, 不阻塞
- [ ] 5.3 behind-check — 复用 `git rev-list --left-right --count` **命令形态** (git.py:147/sync.py:146, 但其锁 `@{upstream}`; 切口1 需 `HEAD...origin/<def>` → 复用 pattern 非调函数, R1 I2); 触发 iff `behind>0 且 (collision.kind!=none 或 commits 触及 upm.source_file)`; **`upm.source_file==None` null-guard 跳过 UPM-touch (R1 I4)**; 触及 UPM→强提示; 纯 behind>0→静默
- [ ] 5.4 fixture: (a) origin ahead + UPM-touch commit → 强提示; (b) ahead 非 UPM + collision none → 静默; (c) 离线 → soft-warn 不阻断; (d) **`upm.source_file==None` null path** (无 UPM 项目, R1 I4); (e) **credential 不泄漏断言** — 失败 stderr 含 token, 断言 soft-warn 输出不含该 token 字面 (R1 I7)

## 6. 文档同步 + 收尾 (Rule #3 + self-dogfood)

- [ ] 6.1 CLAUDE.md 信息地图索引 convention; state-snapshot-schema.md additive collision 字段
- [ ] 6.2 全量回归 PASS (state-scanner + phase-d-closer 零退化); Rule #6 structural substitute
- [ ] 6.3 **self-thrash dogfood**: 本 Spec ship 先用自己的 append-only/fetch-before-edit (per `feedback_meta_dogfood_solution_validates_self_mid_ship`)
- [ ] 6.4 版本 bump (ship 前复核) + 多远程推送 + post-push SHA 验证 + Spec 归档 + 关闭 #133

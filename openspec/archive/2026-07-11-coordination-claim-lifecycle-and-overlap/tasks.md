# Tasks: coordination-claim-lifecycle-and-overlap

> **Status**: ✅ Shipped v1.56.0 (2026-07-11, aria PR#106 `504da89`; pre-merge review R1 1C/5I 全修)
> **补记**: 本 tasks.md 于 Phase B 续做 session (2026-07-11 晚) 补齐 — Phase A 收束时按 carry-forward 条目暂代, L3 要求 tasks.md, 此处正式化。任务分解与 handoff §2 carry 条目 1:1 对应。
> **Base**: aria `wip/coordination-part-c` @ `6f4bbe4` (release_claim_by_track + 4 tests, 上 session WIP)

## Part C — claim 释放生命周期 (defect c)

- [x] C-0 `release_claim_by_track(raw_track_id, status, identity, repo_path)` — 按 (归一 track_id, container) 释放, session 无关 (WIP `6f4bbe4` 已完成, 4 tests)
- [x] C-1 schema: `STATUS_ENUM`/`STATUS_WRITABLE` 增 `abandoned` — 现状 release 写 abandoned 后 parse_claim 会把记录判 invalid 丢弃 (latent bug); reconcile/collision 已把 abandoned 当 terminal (前向兼容注释), 补 schema 侧
- [x] C-2 `coordination_ref.apply_tree_edits(edits, repo_path, message)` — 批量 remove/add 单 commit 原语 (scratch index: read-tree → update-index --force-remove/--add --cacheinfo → write-tree → commit-tree -p → update-ref); GC 移动与 sweep 批量改写共用
- [x] C-3a `gc.archive_done_claims` 补真 git 写入 (`dry_run=False` 经 apply_tree_edits 移动 claims/→archive/, 替换 :259-268 WARNING no-op stub)
- [x] C-3b `gc.sweep_stale_active(repo_path, *, now, stale_ttl=SWEEP_TTL)` — active 且 heartbeat 超 TTL → 批量改写 status=abandoned (跨 container)。**订正 (review C1)**: 原计划复用 STALE_TTL=30min 基于"活 session 必已 heartbeat"假前提 (heartbeat() 零生产调用, heartbeat_at 冻结在 acquire) — 30min durable abandon 会误杀并行活 session; 改新常量 SWEEP_TTL=24h + 误杀锁定测试
- [x] C-4 `release_gate.py` CLI — 镜像 phase1_gate subprocess 契约: `--raw-track-id --status [--repo-path] [--remote] [--sweep-stale] [--gc]`; 流程 fetch (fail-soft) → release_claim_by_track → 可选 sweep/gc → push → stdout JSON; exit 0 = released 或 claim_not_found (benign), 1 = 硬错。advisory: 释放失败不阻断 ship
- [x] C-5 接线 phase-d-closer — D.2 归档后 advisory 调 release_gate CLI 传本 cycle carry-id (SKILL.md 步骤 + 模板命令)
- [x] C-6 一次性清理 — 真协调 ref 上: 本容器 stale claim (dec002 7-04 / followup-99 7-09) release-by-track → done; bot 容器 (runtime-probe 7-07) 经 sweep → abandoned; 验证 ref 无 stale active (本 session 的 carry-coord-partc claim 保持 active, 本 cycle ship 时由 C-5 接线释放 = dogfood)

## Part A1 — 认领强制 (defect a, 插件内)

- [x] A1-1 默认翻转: config-loader SKILL.md `state_scanner.coordination.enabled` default false→true + state-scanner SKILL.md :159 / layer-l-integration.md :12 / RECOMMENDATION_RULES rule 1.54 措辞同步。**已知边界**: `runtime_probe._resolve_enabled_when` 缺键=off 是通用探针契约不动 — 无 config key 的项目 probe 判 skipped (保守), 文档默认仍视为 enabled (AI 编排层读 config-loader 默认)
- [x] A1-2 phase-b-developer + branch-manager SKILL.md: 进 Phase B/B.1 前 REQUIRE 一条本 (container) active claim, 无则先跑 phase1_gate (advisory 强制: 步骤级 MUST, 非 hook 硬锁)。**诚实边界** (proposal §部件A): 改不了绕过 state-scanner 的自主 bot → carry-coord-orchestrator-followup 另开 orchestrator issue
- [x] A1-3 lock-in 测试: doc-sync test 断言 config-loader SKILL.md 该键 `default: true` + state-scanner/layer-l-integration 无残留 "默认 false" (机械防回退, 精神同 memory default-flip-needs-lock-in; 该默认无 python 解析点, 文档即 SOT)

## Part B1 — 语义重叠 advisory (defect b)

- [x] B1-1 schema: 可选 `linked_issue` 字段 (str, 如 "10CG/Aria#160"; additive) — parse (缺省 None / 非 str → invalid) + serialize (None 省略) + roundtrip 向后兼容测试 (无该字段旧 claim 正常)
- [x] B1-2 acquire 穿线: phase1_gate CLI `--linked-issue` (可选) → run_gate/_gated/_run_gate_impl kwarg → acquire_claim param → ClaimRecord (含 :741 fallback record)
- [x] B1-3 重叠检测: `collision.linked_issue_overlaps(claims, own_track_id, own_linked_issue)` 纯函数 — 同 linked_issue、不同 track_id 且 active → advisory 条目; phase1_gate CLI 输出 JSON 增 additive 键 `linked_issue_overlap` (不入 GateResult 核心, 不改 winner 判定; reconcile_all :350 track_id grouping 不动 = 旁路)

## 收尾

- [x] V-1 全测试绿 (python unit + 既有 967+ 不回归)
- [x] V-2 pre-merge code review (对抗视角: 协调正确性 + fail-soft 完备)
- [x] V-3 PR merge + aria MINOR bump (v1.56.0) 5-SOT 同步 + 多远程 parity
- [x] V-4 Phase D: spec 归档 + handoff + 本 cycle claim 释放 (C-5 接线 dogfood)

## Verification ↔ AC 映射 (proposal §Verification)

| Proposal 验证项 | Task |
|---|---|
| release_claim_by_track golden table | C-0 (done) |
| GC 写入非 no-op | C-3a + test |
| stale sweep | C-3b + test |
| CLI I/O 契约 | C-4 + test |
| 一次性清理后 ref 无 stale active | C-6 (真 ref 验证) |
| REQUIRE claim 拦截 (进 B 无 claim) | A1-2 (prose MUST) + A1-3 (doc lock-in) |
| enabled 默认翻转 lock-in | A1-3 |
| 同 issue 不同 track-id → advisory | B1-3 + test |
| schema roundtrip 向后兼容 | B1-1 + test |

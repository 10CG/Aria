---
track-id: owner-container-identity-key-and-collision-parser
owner-container: aria-runner-bot/bfe8285d
phase: D
status: done
updated-at: 2026-09-06T08:30:00Z
---

# Aria — Handoff (2026-09-06) — owner-container-identity-key-and-collision-parser 全周期 ship: aria-plugin v1.70.0 + standards §2.3 三处 + 归档 (Aria #193 关, S2 后续 → #198)

> **一句话**: #193 triage 定位到真根因 (Layer H `owner-container` 两段式串被三段式解析, owner 段丢失) → Level 3 Spec (owner 裁定 D-0 a / D-1 a / D-2 a / D-3 a / D5 MINOR) → post_planning **9 轮** 才收敛 (owner 两次加轮) → B.2 先红后绿 (pytest 16→28, run_tests 1476→1505) → aria **v1.70.0** `0545f86`+tag / standards `d217ed0` / 主仓 PR #197 → `990318e` → 归档 `62de051`; 三仓逐 remote MATCH; claim 已释放; track 终结。
>
> ⭐ **最该留下的**: (1) convergence 的收敛判据是集合严格相等, 所以**只有「干净轮 + 下一轮零 rework」才可能收敛**; 干净轮的 minor 一律延后到收敛之后 (R8→R9 实证)。(2) 多席轮进行中把 rework 备稿写进工作区会被后到的席判流程 Critical (R5 实证), finding 先记 scratchpad。两条已入 memory。

## §0 入口 (新 session 优先读)

1. `/aria:state-scanner`。主仓 master `62de051` (origin/github MATCH); aria gitlink `0545f86` (v1.70.0, tag 同 SHA) / standards `d217ed0` / aria-orchestrator `237045a` 不动。
2. 本 track **已终结** (Spec 归档 `openspec/archive/2026-09-06-owner-container-identity-key-and-collision-parser/`, Layer L claim 已 release status=done, push_success)。下一个 session 不需要接本轨任何步骤。
3. 本容器仍持有的另一条轨: `aria-2-0-m6-dispatch-input-delivery` (B.2 补强已推, 门在 owner/基建, 见 09-05 handoff) —— 未受本轨影响。
4. 双子星 `simonfish/023236f2` 的母 Spec `a1-entry-claim-duplicate-work-guard` (#174) 仍在飞 (分支 `ab3dbd0` 未进 master); 本轨已在 #174 留两条 (21906 征求 SC-3 改写 ack / 21989 补 ship 结果), **S1 形态零契约改动**, 对方合并时按函数名定位 `get_container_uuid()` (行号会漂)。

## §1 已完成 (2026-09-05 → 09-06, UTC)

| 阶段 | 事件 | 证据 |
|------|------|------|
| A.0/triage | #193 triage: verdict confirmed, 新根因 = `split_owner_container` 三段式读两段式串; 发帖 21431 | `.aria/triage-report.json` |
| A.1 | Level 2 起草 → owner 升 Level 3; post_spec R1–R5 (MAX_ROUNDS_EXHAUSTED, owner [1] 接受); 决策单 D-0 a / D-1 a / D-2 a / D-3 a | `.aria/decisions/2026-09-05-owner-container-identity-key-rulings.md` |
| A.2/A.3 | tasks.md 39 checkbox + yaml 39 TASK (S2 四项预留于 `metadata.s2_followup`, 不进 checkbox); post_planning R1–R9: R5 / R7 两次 MAX_ROUNDS_EXHAUSTED → owner 各加 2 轮 → **R9 CONVERGED** (R9 == R8 两簇 minor, 五席全票 PASS) | `.aria/audit-reports/post_planning-R{1..9}-*-aggregated.md` |
| B.1 | 三仓 feature 分支; Phase B advisory claim passed; TASK-000 判 **S1** (a1-entry 未进 master, 无 ack); #174 留言 21906 (owner 授权) | yaml `metadata.ship_shape_evidence` |
| B.2 组 1 | 先红测试 8 个 SC: pytest 13F/15P, unittest 6F + 4 模块 ImportError (基线 aria 7dd0135) | 台账 `.aria/notes/2026-09-06-ick-rule6-red-green-ledger.md`; aria `4603fcc` |
| B.2 组 2 | 实现: 两段式解析 / `identity_key` / `family_track_id` (D-0 a, `track_to_claim_record` 一处) / `classify_claims` 按 identity_key + 非空非 unknown owner / `LAYER_H_ACTIVE_WINDOW_DAYS=30` + `filter_layer_h_fresh` 单一实现 (dedupe **后**、classify 前; 保住 dedupe 统计的日历无关性) / `identity_drift_advisories` (dedupe 前) / collector 可选 `now` / renderer ⚪ 段 + 查表键归一 + 族键 `tracks_by_tid` / `get_container_label()` / `label_migration_inventory` 接 phase1_gate + release_gate | aria `5fbb974`; pytest 28 passed, run_tests 1505 OK, fetch_gate 11, session-closer 74 |
| B.2 组 3 | 文档: snapshot schema / rule 1.54 两 token / advanced-rules / layer-l-integration / phase-1-collectors / 模板 / CHANGELOG; standards §2.3.1 三态 + identity_key + 族键句, §2.3.5 三行 (Amended, 实质变更), §2.3.9 AI runner 提交身份 (SC-5 token 机械核过) | aria `f2e4231`; standards `c955783` |
| C | owner 裁定 D5 **MINOR** → v1.70.0 五文件 bump (`bae4ad8`); aria 本地 `--no-ff` merge → `0545f86` + tag v1.70.0; standards → `d217ed0`; 双推逐 remote MATCH (master 与 tag 对象); 主仓同步面 (gitlink ×2 / VERSION 表 / README ×4 含 i18n 版本串 / 架构文档 ×2 / CLAUDE.md :139/:141); C.2.4 gate green (path coverage not_applicable); state-check 13 绿 + `plugin-cache-currency` 预期红; PR #197 (owner 授权) → `990318e` | PR 评论 21955 (state-check + live dogfood) |
| D | #193 回帖 21983 + closed; aria-plugin#135 回帖 21988 (S1 措辞: 缺口 3 部分闭合); #174 补 ship 21989; **S2 tracker Aria #198**; tasks 39/39; 归档门 pass 无 unverified/deferred; 归档 `62de051`; claim released | 本文件 |

## §2 未完成 / Carry-forward

- 本轨无 carry。S2 后续 (flip / 发布门 / a1-entry SC-3 改写 / #135 08-13 时间线) 全部在 **Aria #198** (激活条件三项 + 回退条款 + 四项预留任务原文)。
- 🟡 **owner 动作**: (1) `/plugin marketplace update` + `/plugin update` + 重启 session → `plugin-cache-currency` 转绿; (2) **Rule #10 复议**: SC-7 的「13 条全绿 + plugin-cache-currency 例外」条款是 post_planning R1 rework 引入 (owner Approved 之后), 请复议是否接受为成文 lane; (3) a1-entry 轨 (#174) 的 SC-3 改写 ack 仍开放, 不阻塞任何事。
- 🟡 生产 live 数据: 本仓 `collision.groups=[]`, `identity_advisories` 2 条 (`023236f2` / `bfe8285d` 各 `[aria-runner-bot, simonfish]`) — 这就是 #193 症状的正确解释; 若将来 owner 按 §2.3.9 把机器身份账号名统一, 这两条 ⚪ 会随新 handoff 自然消失 (不 rewrite 历史)。

## §3 关键风险 / 已知陷阱

- **日历依赖**: D-3(a) 窗口让任何用固定旧日期的 collector 夹具随时间「过期」变 none; 本轨把 `collect_handoff_multibranch` 加了可选 `now`, 新测试都钉了 `now`。**既有 `test_handoff_multibranch_collision_dedupe.py` 的 2026-08 夹具 (twin-track) 在 2026-09-19 后会变 none** —— 需要时给它们传 `now=` (窗口在 dedupe 后, dedupe 统计断言不受影响)。
- `identity_key` 已知限制 (成文): hostname / label 恰为 8 位小写 hex 会被当 uuid; 8 位十进制 (如 `-20260719` 日期尾段) 也是 hex 形, 会被族键剥离 (语料核过零碰撞)。
- 归档门符号分类器把反引号内的字面 token (`cross_owner` 等) 当待核对引用 → 假 unverified; 写 tasks.md 时字符串常量不要包反引号 (本次改写两行后 pass)。
- phase-d-closer `test_fetch_gate.py` 是 pytest 风格 (unittest 收 0 个); state-scanner 里 pytest 风格文件仍只有 `test_collision.py`。

## §4 实战教训 (memory 沉淀候选)

- 已写: `feedback_convergence_needs_zero_rework_round` (干净轮 + 零 rework 才收敛; minor 延后; 派发词分 finding/观察) · `feedback_audit_object_frozen_until_round_aggregated` (轮内工作区冻结) · `feedback_red_assertion_from_real_run_not_recon_expectation` (前一段 session)。
- 候选未写: 「统计/归因 helper 必须按『组成该组的行』取行, 不能按 owner 串全局取」—— 同一 session 犯了两次 (frozen corpus `_attribute`), 第二次才对; 属通用的「聚合键泄漏」陷阱。

## §5 同步状态 (收尾时)

| 仓 | 本地 | origin | github | 备注 |
|---|---|---|---|---|
| Aria 主仓 | `62de051` master | MATCH | MATCH | feature 分支 `cce8c1f` 已合 (#197), 可删 |
| aria | `0545f86` master (tag v1.70.0 → 同 SHA) | MATCH (master + tag) | MATCH (master + tag) | feature 分支本地留存 |
| standards | `d217ed0` master | MATCH | MATCH | feature 分支本地留存 |
| Layer L claim | `owner-container-identity-key-and-collision-parser` released (done) | push_success | — | `label_migration: null` (本容器无 label) |

## §6 Next session 入口 + 优先级建议

1. 本容器: 回到 M6 轨 (`aria-2-0-m6-dispatch-input-delivery`) 等 owner build / Blocker 4; 无本轨事项。
2. owner: 更新插件 + 复议 SC-7 例外 (§2)。
3. 双子星: a1-entry 母 Spec B.1 时读 #174 两条留言; 合并 `identity.py` 时按函数名定位。

## §7 提交清单

主仓 (本 session 段): `413086d` B.1 起手 → `2e4dcd7` B.2 进度 → `974afb9` 同步面 → `cce8c1f` 4.3/5.6 → PR #197 merge `990318e` → `88cb4f6` D.1 → `62de051` 归档 → 本 handoff。审计报告 `post_planning-R3..R9` 与聚合均随对应 commit 入库 (7b64262 / 984c4e9 / 21d4a73 / 087f9e2 / 19d25b1 / ed1d168 / 7495c4c / bd1069f / 8e3d9dc)。

## Cross-references

- Spec 归档: `openspec/archive/2026-09-06-owner-container-identity-key-and-collision-parser/`
- 决策单: `.aria/decisions/2026-09-05-owner-container-identity-key-rulings.md`
- Rule #6 台账: `.aria/notes/2026-09-06-ick-rule6-red-green-ledger.md`
- Issues: Aria #193 (closed) · aria-plugin#135 (open, S1 部分闭合) · Aria #174 (a1-entry) · Aria #198 (S2 tracker) · PR #197
- 前一份 (本容器另一轨): [2026-09-05 M6 B.2 补强](./2026-09-05-m6-six-test-hardenings-landed-awaiting-submodule-push-auth.md)

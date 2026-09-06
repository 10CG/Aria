---
checkpoint: post_spec
round: 1
mode: convergence
verdict: FAIL
converged: false
scope_ok: true
counts: 4C/17M/14m (五席原始合计, 去重前)
clusters: 3C
teams: [aria:tech-lead, aria:backend-architect, aria:qa-engineer, aria:code-reviewer, aria:knowledge-manager]
sibling_probe: no_sibling_found
timestamp: 2026-09-05T14:40:00.000Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md
drift_terminated: false
drift_check_skipped: true
oscillation: false
overridden_by_user: false
degraded: false
---

# post_spec R1 — owner-container-identity-key-and-collision-parser (Level 2 draft `144d79e`)

> **对象**: 2026-09-05 A.1 草稿 (合并处置 Aria#193 + aria-plugin#135 缺口 3)。**席位**: config `teams.post_spec` 五席, 各给一个镜头 (tech-lead 架构/边界 / backend-architect 代码级实跑 / qa-engineer SC 可证伪性 / code-reviewer 规格合规+内部一致 / knowledge-manager 规范与引用链)。
> **Sibling probe (Round 1 入口)**: `verdict=no_sibling_found`, status ok, 双远端 github 152 / origin 156 份 proposal 全部扫描, own_keys `[aria#193, aria-plugin#135]` —— 本轮已完整扫描, 未发现同 issue 竞品。
> **drift-checker**: convergence 模式未 opt-in (`audit.drift_guard` 缺省), 本轮未跑 → `drift_check_skipped: true`, 不影响收敛判定。

## 判定

| 席 | verdict | counts | 一句话 |
|---|---|---|---|
| tech-lead | FAIL | 1C/6M/2m | container 主键少了「跨容器 owner 归并」这步, 真实数据同人两机仍 🔴; 排序规则只解文本冲突不解语义耦合; Level 判据三项全中 |
| backend-architect | FAIL | 1C/2M/2m | SC-4「同容器不同 owner 折叠为 1」与 dedupe 键结构互斥 (实跑 len=2); 冻结快照未冻结; get_container_id 的三个间接消费方未列 |
| qa-engineer | FAIL | 1C/3M/3m | 既有测试 `test_both_latest_active_still_reports_self_multi_container` 锁的对在目标语义下翻转, SC-7 零回归不可达; §2.3.7 已占用; cross_owner 正控测试全是虚构三段式 |
| code-reviewer | PASS_WITH_WARNINGS | 0C/4M/5m | 规格合规 PASS; 实验表绕过了生产 collector 的 dedupe→classify, 按生产路径 A=1 组 / B=2 组 / C 无 🔴, 「三层必须一起修」失据 |
| knowledge-manager | FAIL | 1C/2M/2m | §2.3.7 已被 #137 占用 (真空档 §2.3.9); 判定键反转对采用方是行为变更不是措辞; layer-l-integration.md:73 与 rule 1.54 消费面无任务覆盖 |

**合并判定: FAIL / 五席全 REVISE, 未收敛。** 五席结论高度一致 (同一处矛盾被四席独立命中), 不是发散。

## Critical 簇 (去重后 3 个)

| # | 簇 | 席位 | 执笔处置 (rework v2) |
|---|---|---|---|
| **R1-C1** | **判定键缺「跨容器 owner 归并」**: D1 只在同 container 内合并 owner 串, 跨容器仍比原始 owner 集合 ⇒ 真实 track `state-scanner-stale-refs-false-parity` (同一 owner 两机, 串各自漂移) 修后恒 🔴; 实验表 C 行与 D-1(a) 后果句「由 D-1/D-2 消解」为假 (D-2 只改未来, 历史不 rewrite) | TL C-1 · CR M-4 · QA C (同一对被既有测试锁为 self_multi_container) | **接受**。D1 改为三步: 两段式解析 → 身份键 (uuid 容器 = container; 主机名容器 = owner/container) → **owner 等价类** (同一 uuid 容器上共现过的 owner 串两两等价, 由全语料并查集得出; 空/unknown owner 不成类)。在冻结语料上按生产路径实测: 三组全部 🟡, 合成两人两机仍 🔴, 同容器双 owner → none + advisory (见 v2 实验表)。D-1/D-2 后果句重写: 历史双串靠等价类消解, 不靠 D-2 |
| **R1-C2** | **SC-4 与 D1「dedupe 不改逻辑」互斥**: dedupe 键 `(track_id, owner, container)` 含 owner, 新解析下同容器不同 owner 是两把键, 结构上不折叠; 且既有测试 `test_owner_segment_participates_in_grouping_key` 把「owner 必须参与键」锁成不变式; track_board :412-417 建表/查表键不同源 (`""` vs `"unknown"`), 标签今天就查不中 | BA C1 · TL M-1/M-2 · CR M-2 | **接受**。D1 把 dedupe 键与 board 标签查找**列为显式改动项** (不再「不改逻辑」): dedupe 键 = `(track_id, identity_key)` (uuid 容器折 owner; 主机名容器保留 owner 段 —— 那条既有不变式的理由「主机名跨机不唯一」只对主机名成立, 测试按此改写为两臂); advisory 由 classify() 从**全语料**产出, 不依赖 dedupe 后的行 (回应 CR M-2 第二半) |
| **R1-C3** | **§2.3.7 已被占用**: session-handoff.md §2.3.7 = #137 frontmatter enforcement, §2.3.8 = carry-id schema; 真空档 §2.3.9; SC-5「§2.3.7 存在」改前即真 | KM C1 · QA M · BA m | **接受**。改 §2.3.9; SC-5 改为内容断言 (表三行的判据文本 + §2.3.9 含 D-2 裁定文本), 不是「章节存在」 |

## Major (去重后 11 条) 与处置

| # | 簇 | 席位 | 处置 |
|---|---|---|---|
| M1 | 实验表绕过生产路径 (collector 先 dedupe 再 classify): 按生产路径 A=1 组, B=2 组, C 无 🔴 ⇒ 「修 parser 立刻暴露 🔴」失据 | CR M-1 | **接受**。v2 实验表改为**冻结语料 + 生产路径** (`dedupe_latest_per_track_container` → `classify`) 逐变体重跑; 「三层一起修」理据改写为实测归因 |
| M2 | SC-6 冻结快照未冻结 (`.aria/state-snapshot.json` gitignored, 每扫覆写, 同 cycle 内已漂) | BA M1 · QA M | **接受**。已落 `.aria/repro/handoff-tracks-frozen-2026-09-05.json` (996 行非 legacy tracks, 可跟踪); B 期复制为 aria 测试 fixture; SC-6 改为对该文件断言 |
| M3 | `get_container_id()` flip 的间接消费方未列 (claim_lifecycle / phase1_gate:294 / concurrent_tracks:133), 且无迁移面: label 非空 + 在飞 claim 的机器 flip 后 claim 成孤儿 (#135 08-13 镜像) | BA M2 · TL M-4 | **接受**。Impact 列全消费方; 新增 T3b「flip 前守卫」: 读到 label 非空且 `claims/<label>/` 下有 active → 先 release/迁移 (或拒绝 flip 并告警); D2 文本给 hostname 兜底分支留口径 (「恒 uuid」改「uuid, 只读 fs 兜底 hostname」) |
| M4 | 与 a1-entry 的排序规则只解文本冲突: 本 Spec flip 会让 a1-entry 已收敛的 SC-3 (依赖 label-over-uuid 才必红) 恒绿; 上游改行让其行号断言过期 | TL M-3 | **接受**。改为有方向的硬约束: identity.py 的 flip **排在 a1-entry B.2 落地之后**; 本 Spec 在 a1-entry 之前只加 `get_container_label()`; flip 落地时由本 Spec 承担改写 a1-entry SC-3 判据 + 在 #174 留言知会对方容器 |
| M5 | 「与 #182 正交」实为依赖: 19 份历史 `status: active` (最早 2026-05-20) 全超 STALE_TTL 仍参与判定, Positive「信号第一次可信」不可达; 旗舰误报案例本身就是 #182 产物 | TL M-5 | **接受 (改写)**。Positive 降级为「分类逻辑正确; 信号可用性还取决于 #182 收口」; 非目标改写为显式依赖方向; 新增决策点 D-3 (是否在本 Spec 内加 Layer H 新鲜度截止, 给出两种后果), 不自作主张 |
| M6 | Level 判据三项 (architecture / cross-module / breaking) 全中, 应为 Level 3 或明示依据 | TL M-6 | **上呈 owner**。v2 头部写明: owner 2026-09-05 指令为 Level 2; 审计 R1 依 `phase-a-spec-planning.md:126-137` 判据建议 Level 3; 请 owner 复议 (Rule #10: Level 不按性价比下调, 也不由 AI 越过 owner 上调) |
| M7 | 判定键反转对采用方是行为变更, Impact 表「只改判据措辞」低估; §2.3.5 既有两行触发条件被实质改写 | KM M2 | **接受**。Impact 改写为「§2.3.5 判据实质变更 (同容器多 owner 由触发 cross-owner 改为不触发 + advisory), 对采用方是行为变更, 需在 standards 变更说明与 aria CHANGELOG 明示」 |
| M8 | 消费面漏列: `layer-l-integration.md:73` (`kind == "cross_owner"` → 推荐 worktree) 与 `RECOMMENDATION_RULES.md` rule 1.54 把取值当触发条件写死, 无任务核实/更新, 无回归断言 | KM M3 | **接受**。新增 T8 (两处消费文档同步 + `advanced-rules.md:578` 过时注释) + SC 锁 rule 1.54 的触发面 |
| M9 | D1 谓词在「单 container 自身多 owner」形态下未定义 (取并集与取代表结果相反) | CR M-3 | **接受**。等价类规则消解: owner 段先归到等价类代表, 再比较 —— 单 container 多 owner 恒同类 |
| M10 | 既有测试 `test_both_latest_active_still_reports_self_multi_container` (真实两段式对) 在目标语义下翻转, T 未点名, SC-7 不可达 | QA C (降为簇内 Major, 与 C1 同因) | **接受**。等价类规则下该对仍 self_multi_container (实测), 测试语义不翻转; T1/T4 点名全部受影响测试 (含 `test_split_owner_container_variants` 的 1-part 断言) |
| M11 | cross_owner 正控测试全用虚构三段式串 (0/154 真实三段), 端到端真实两段式 cross_owner 可达性无 SC | QA M | **接受**。SC-2 增「collector→dedupe→classify 端到端, 真实两段式两人两机 → cross_owner」 |

## Minor (14 条, 摘要)

reconcile tie-break 的 session 退化 `container/unknown` (TL m-1; 记 Impact 风险) · advisory 宿主未定, 渲染器按 2-tuple 解包 (TL m-2; 落在 `classify()` dict additive 字段) · `oc_by_tid_key` 三元组去重在未 dedupe 输入上的碰撞 (BA m) · 「9 种串」实为 10 种 (含 `simonfish/f9c6e8cd`), 「2 台机器」实为 5 个 container 标识 (CR/KM) · 三段式契约引入点为 `f9306a0` (05-20) 非 `83a1a45` (CR) · 「§2.3.3 写入频度」应引 §2.3.6 (CR) · Rule #6 substitute 点名不应含 SC-5/SC-6 非测试项 (CR) · T7 无 SC / SC-7 无 T / T2 schema bump 无锁 (CR) · SC-2 只覆盖 2-owner, 真实有 3-owner 容器 (QA m) · legacy 行不参与 advisory 无专属断言 (QA m) · T1 「solo」断言需一并改 (QA m) · Rule #6 判档自评成立 (QA 记录, 非缺陷) · D-2 选项后果不对称 (KM m) · 三段式 `superseded_from` 兼容 / release_gate 不消费 classify_claims / 引用行号全部命中 (TL 核验通过项)。全部纳入 v2。

## 收敛判断

R1 不收敛 (五席 REVISE)。但 finding 集中在四个可机械修正的结构缺口 (判定键归并 / dedupe+board 显式改动 / 章节编号 / 生产路径实验) 与两项须上呈 owner 的判断 (Level / #182 新鲜度截止)。执笔侧按上表处置后进 R2; R2 席位用同一 team, 每席换镜头 (对 v2 的新机制做反事实)。

## 归档

- 席位报告: 同目录 `post_spec-R1-2026-09-05T140104-375Z-owner-container-identity-key-and-collision-parser-{tech-lead,backend-architect,qa-engineer,code-reviewer,knowledge-manager}.md`
- 冻结语料: `.aria/repro/handoff-tracks-frozen-2026-09-05.json`

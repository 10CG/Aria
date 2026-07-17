---
track-id: specC-ship-falseparity-20260715-0716
owner-container: simonfish/bfe8285d
phase: session-close
status: done
updated-at: 2026-07-16
---

# Session Handoff — false-parity 三 spec sign-off + Spec C 全循环 ship v1.57.0

> 本对话 2026-07-15 → 07-16。从 `/state-scanner` 开局, 完成: (1) false-parity 三 spec owner sign-off; (2) Spec B stderr-leak R6→R7→R8 收敛; (3) Spec C 完整十步循环 A→D ship v1.57.0 (双动态工作流 agent team 驱动)。

## §0 入口 (新 session 优先读)

- **本对话干了什么** (时序): (1) `/state-scanner` → 三 spec sign-off (主 stale-refs v10 含 D15′-D20 五代裁 + Spec C issue-cache v6 + DEC 闭环) → (2) Spec B stderr-leak 跑 post_spec: **R6(1C+4M+5m) → v3 → R7(1C fix-introduced) → v4 → R8(1C fix-introduced) → v5**, owner 裁 **option B 重框** (AC-2 静态闸极难精确规约, 改类型化通道=结构保证 + AC-2 降 best-effort lint) → (3) Spec C **完整 B.2 → C → D ship v1.57.0**: `/goal` 触发 agent team + 双动态工作流。
- **当前态**: **全部提交并双远程 parity 验证** (主仓 `2e7dec1` / aria-plugin `a9e8652` v1.57.0 / origin+github ls-remote 独立验证均落地)。
- **下一步**: 见 §6 (Spec B/主 spec 待实现; M6/M7 门待 owner)。

## §1 已完成

1. **false-parity 三 spec sign-off** (owner 终审 2026-07-15/16): 主 `state-scanner-stale-refs-false-parity` v10 Approved (D15′-D20 五代裁) / Spec C `issue-cache-freshness` v6 Approved / Spec B `stderr-leak` v5 Approved。DEC-20260712-001 终审闭环。
2. **Spec B stderr-leak 收敛** (未实现, spec-only): R6→R7→R8 **连续三轮 fix-introduced Critical 全集中在 AC-2「无原始 stderr 到 snapshot 的 sound 静态检查」** (name-grep 3/9 → `.stderr` grep 0/9 → `_run` 第三返回值漏跨函数逃逸) → owner **option B 重框**: 结构保证=GitErrorClass 类型化通道 (返回类型无 stderr 字段), AC-2 降 best-effort lint, 完整性靠 code-review。审计轨迹落盘 `.aria/audit-reports/post_spec-R6-*` + `post_spec-R7-R8-*-trail.md`。
3. **Spec C 完整 ship v1.57.0** (aria `a9e8652`): snapshot 顶层 `generated_at` (additive) + check 重定义为可复用探针 `issue_cache_freshness_probe.py` + custom_checks skip 态 (`##SKIP##` marker + exit 0) + skipped 计数三分支。**B.2 review-driven A1 精修** (见 §3)。十步循环 A→D 闭环 + 归档 `openspec/archive/2026-07-16-state-scanner-issue-cache-freshness-assertion`。

## §2 未完成 / Carry-forward

> **更新 (session 续跑 2026-07-16)**: Spec B 已在本 session 后续 ship —— ~~Spec B stderr-leak 实现~~ **✅ SHIPPED v1.58.0** (aria `cae92e8` / 主仓 `ef91405`; 类型化通道 GitErrorClass 无 stderr 字段 + 助手内部自分类 + coordination_fetch 委托 + AC-2 best-effort lint; 双动态工作流 review code-reviewer PASS + silent-failure PASS-with-fixes fold done; 归档 `openspec/archive/2026-07-16-state-scanner-snapshot-stderr-secret-leak`)。**C(v1.57.0)+B(v1.58.0) 三 spec 之两已 ship**。

- 🔴 **主 spec stale-refs-false-parity 实现** (现唯一剩项, 落地序最后): v10 Approved + tasks.md 已备 (119 任务), 待 Phase B。F3′ 依赖 Spec B 先收口 stderr 暴露面 —— **该前置已满足** (B 已 ship), 主 spec 可起 Phase B。
- **Spec C follow-up** (非阻塞, 已文档化): (a) 聚合 fetched_at 部分失败盲点 (主 repo 失败但 submodule 新鲜→OK) — per-repo 收紧待 follow-up; (b) config/snapshot 持续损坏永久 SKIP — 区分「broken」vs「not-applicable」待收紧; (c) task 3.4 heavy 双 subprocess cache-hit shim (轻量确定性版已覆盖)。
- (承前, owner 门) M6 4 门 (input-delivery + Blocker 4 Luxeno) / 168h 跑 / #136 webhook 轮换 / #151 credentials。
- **#165 GitHub 镜像漏推**: 本 session ship 严格走「子模块远程合并优先→gitlink bump」+ ls-remote 独立验证, 未复发 (但 #165 issue 仍 open, 需机制化)。

## §3 关键风险 / 已知陷阱 (本 session 新增)

- 🔴 **「检查抓不到它该抓的东西」形态谱系再扩** (承 false-parity): Spec C 的 Δ-only 机制 **对真实数据近乎无用** — collector 用 1×TTL 门控缓存使 STALE(Δ>2×TTL) **结构性不可达**, 而真故障 (fetch 失败) → fetched_at=None → 原设计判 **SKIP 绿真空**。修「恒红」造出「恒绿真空」(qa 蓝图预警 → 代码接地坐实)。**教训**: 检查的判据必须对着**真实数据能产生的值域**验证, 不能只测合成 fixture; 「防假绿的检查」本身要证它在该 FAIL 时真能 FAIL。→ owner A1: 主信号改 issue-fetch 健康 (fetched_at 缺失)。
- 🔴 **skip 哨兵别用 exit 2** (B1): exit 2 是 grep/diff/argparse 的错误码, 会把采纳者真故障静默降级 fail→skip。用 stdout marker (`##SKIP##` 首个非空行)。
- **机制变更连环 fix-introduced Critical** (Spec B R6→R7→R8 + Spec C A1 也过 post_impl 确认): 每次改 sound 静态检查的靶点都引入新盲区 (变量名→属性→元组→跨函数)。**教训**: 「可证明 sound 的全目录静态分析」对某些属性极难精确规约, 结构级保证 (类型不可达) > 静态闸; 机制变更后必过确认轮 (memory `feedback_multiround_audit_catches_fix_introduced_regression` 强复现)。

## §5 多维度同步状态

| 维度 | 状态 |
|------|------|
| 主仓 | `2e7dec1` 双远程 parity ✓ (ls-remote 独立验证) |
| aria-plugin | `a9e8652` **v1.57.0** 双远程 parity ✓ (marketplace 已发布) |
| Spec C | ✅ SHIPPED + 归档 (十步循环闭环) |
| Spec B / 主 spec | v5 / v10 Approved, 待实现 (序 C→B→主) |
| 协调 ref | self_multi_container collision (持续, 非阻塞; 本 session 未走 claim 生命周期 — goal-直驱绕过 state-scanner Phase B claim) |
| 测试 | aria-plugin state-scanner 1031 real-green + 1 AC-5 豁免 flaky |

## §6 Next session 入口 + 优先级

> Spec B 已本 session ship (§2 更新)。**主 spec Phase B 已起 (Phase 0 done)**, 见下四段式。

**⭐ 主 spec stale-refs-false-parity (Level 3 / 119 任务, 多 session; 四段式拆分 wf_b50b921e)**:
分支 `feature/state-scanner-stale-refs-false-parity` @ aria (基 cae92e8/v1.58.0)。
- ✅ **Phase 0 (prereq) 完成** (aria feature `e2a2b22`, 零行为变更, 未 merge): F5′
  resolve_enforced_remotes 纯函数 (INERT, [] 陷阱守卫) + sync_freshness.* 键 (DEFAULTS+template)
  + D16 predicate-domain-table.md 骨架 + 8 测试。**可独立 ship v1.59.0 或累积 Phase 1 同 ship** (待定)。
- 🔴 **Phase 1 (core, 不可拆)**: F1′ 两轴双谓词 (证据资格/豁免资格/evidence_grade 三档) + F2′
  退役 mtime + **F3′ remote_refresh 新 collector** (多 remote 并行 fetch + --prune + per-host
  限流 + deadline + 防饥饿 + 退避 —— **最高风险单元**) + F4′ overall_parity 四子句重写 (gitlink
  子句占位 False) + F6′ shim + **9.7 offline 三面冻结 (必须同 PR, 否则自造漂移)**。依赖 Phase 0。
- **Phase 2 A/B (并行)**: Track A F10″ gitlink_orphaned 八分支 + gitlink_integrity[]; Track B
  F9′ sync.py 消费 F1′/F3′ 信号 (⚠️ **只碰新鲜度标注, 绝不碰 US-008 方向性判据 sync.py:312-328**)
  + 退役 verify_mode=ls_remote (OQ-F)。依赖 Phase 1。
- **Phase 3 (integration/收尾)**: **12.10 六漂移通道核实** (本 spec 是 flaky 认领消除方, 非豁免!)
  + golden fixture 重采 + 下游 (handoff_autofill/drift 建议/m7-fleet 通知) + 发布。依赖 Phase 2 双合并。
- **关键陷阱** (蓝图): F5′ `enforced_remotes:[]`=自动发现全部 (非空集); overall_parity 会从 3 独立
  机制翻 false (CHANGELOG 须逐条列); F3′ 并发基建需 ARIA_SCAN_FETCH_BUDGET 测试 seam; 缓存 shape 迁移兜底。

**其它 carry-forward**: owner 门 (M6 4 门 / 168h / #136 / #151); Spec C 3 follow-up + Spec B lint 中转变量 gap (code-review 兜底)。

## §8 Memory entries this session

- 本 session 待落: **check 判据须对真实数据值域验证 (防「恒红→恒绿真空」)** — 见 §3 第一条, 与 `feedback_windowed_predicate_needs_convergence_inequality` / `feedback_predicate_tiers_need_total_partition_proof` 相邻但正交 (那些是谓词内部完整性, 本条是判据 vs 真实数据分布的匹配)。
- 复用确认: `feedback_multiround_audit_catches_fix_introduced_regression` (Spec B R6→R8 三连 + Spec C A1 强复现) / `feedback_agent_team_dynamic_workflow_division` (本 session 双动态工作流实践: 蓝图+review 交 agent team, 核心主 loop 亲验) / `feedback_sequenced_multirepo_gitlink_bump` (#165 顺序严格执行未复发)。

## Cross-references
- Spec C archived: `openspec/archive/2026-07-16-state-scanner-issue-cache-freshness-assertion/`
- Spec B/主 audit trails: `.aria/audit-reports/post_spec-R6-2026-07-15-*` + `post_spec-R7-R8-2026-07-15-*-trail.md`
- 前序 handoff: `docs/handoff/2026-07-15-session-close-six-cycle-marathon.md`

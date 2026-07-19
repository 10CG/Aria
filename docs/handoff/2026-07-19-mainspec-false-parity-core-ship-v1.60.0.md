---
track-id: state-scanner-stale-refs-false-parity
owner-container: simonfish/bfe8285d
phase: C-shipped-D-partial
status: active
updated-at: 2026-07-19
---

# Session Handoff — 主 spec state-scanner-stale-refs-false-parity 四段式核心 SHIPPED v1.60.0

> 本对话从 `/state-scanner` 开局, 经 owner 连续 5 个 `/goal` 推进: false-parity 三 spec 收尾 → Phase 0 ship v1.59.0 → **Phase 1 core** → **Phase 2/3** → **Phase C/D 发布**。主 spec 四段式**核心机制全部实施 + 对抗 review + 主 loop 亲验 + ship v1.60.0**。全程 agent-team 动态工作流 (6 个) + 主 loop 亲验。

## §0 入口 (新 session 优先读)

- **本对话干了什么**: 主 spec `state-scanner-stale-refs-false-parity` (false-parity 三 spec 之主, v10 Approved) 的 Phase 1 core + Phase 2A F10″ gitlink + Phase 2B F9′ sync + Phase 3 golden/12.10 **全部实施并 ship v1.60.0**。这是 R5-C-A gitlink 事故 (2026-07-12) + 陈旧 remote-tracking ref 撒谎报 parity=equal 的**根治解药**。
- **当前态**: **已 ship + 双远程 parity 验证** (aria `e162f7b` v1.60.0 / 主仓 `d319d6f`; origin+github ls-remote 独立验证均落地)。8 custom checks 全绿。
- **⚠️ spec 保持 active, 未归档 (D.2 未走)**: 119 task 中 79 done / 29 TODO / 1 DEFERRED / 2 待裁 / 8 SUPERSEDED。**下一步见 §6**。

## §1 已完成 (ship 到 v1.60.0)

四段式核心 (freshness by fetch, not by measurement):
1. **F3′ remote_refresh collector** (Phase 0.5, `collectors/remote_refresh.py` 新建): per-host ThreadPoolExecutor 并行 `git fetch --no-tags --prune`, 顺序准入闸门 deadline (非 cancel_futures, 防 race), fetch_ok 三态 (true/false/not_attempted)。coordination_fetch 派生 shim。新配置键 `state_scanner.multi_remote.{refresh_deadline_seconds=15, per_host_fetch_limit=4, fetch_timeout_seconds=30}`。
2. **F1′/F4′ 双角色谓词 + evidence_grade** (`multi_remote.py`): 证据资格/豁免资格 (D15′) + evidence_grade∈{fresh,stale_unverified,expired} 单函数全分割 (D20)。overall_parity 四子句。陈旧 equal 非正证据; `_blocking_unknown` 严格补集 fail-CLOSED (非正向枚举)。consecutive_unverified D18 由 remote_refresh 按 fetch_ok 拥有 (review 修死码 + 假 docstring)。
3. **F10″ gitlink 可达性** (`multi_remote.py`): `gitlink_integrity[]` per-(R,S) {status∈9值, consecutive_unverified}。gitlink_orphaned 九分支域 + 独立 gitlink-integrity.json cache。**BLOCKER 修**: ok/orphaned 两侧**均过豁免资格门** (陈旧 refs 上的 ok = false-green, review 抓)。offline 冻结 gitlink 计数器。
4. **F2′** 退役 mtime local_refs_stale; **F9′** sync.py 消费 evidence_grade (current_branch + submodules[].drift), **US-008 方向护栏 (sync.py) 逐字节未动**; **9.7 offline 冻结** (ARIA_SCAN_OFFLINE/NOW/FETCH_BUDGET) 根治 test_two_consecutive_runs_diff_zero 漂移。

**验证**: 全 state-scanner 套件 1219 绿 + 真实 dogfood (gitlink 5 ok / 1 no_matching_remote 诚实不误报 orphan; evidence_grade join 通; overall_parity 诚实判 behind→False)。⚠️ **行为变更 (13.6)**: overall_parity 事故形态 true→false; Fetch1 --prune。

**交付方式**: 6 个 agent-team 动态工作流 (Phase 1 蓝图+实施/review / Phase 2 蓝图+实施/review / 收尾 docs) + **主 loop 亲验每轮** (不信 agent 绿口头, 亲跑全套件 + dogfood + 读 review findings)。**主 loop 抓修 3 个 review Critical/BLOCKER** agent 自测掩盖不了的 (Phase 1 D18 死码 + Phase 2 gitlink ok false-green)。

## §2 未完成 / Carry-forward (29 TODO — spec 仍 active)

> tasks.md 审计 (36bd565): 79 [x] / 29 "(TODO)" / 1 "(DEFERRED)" / 2 待裁 (OQ-C) / 8 SUPERSEDED (F10′)。**未归档因这 29 未做**。

**实质性 (影响功能完整, 但均 fail-CLOSED 非 false-green)**:
- 🔴 **6.1/6.2 F5′ enforced/read_only 未接进 `_overall_parity`/`_aggregate_flags`** — `resolve_enforced_remotes` 只接了 13.x gitlink R×S 循环, 核心 parity 裁决路径仍用全部 remote。**read_only_remotes 配置对核心 parity 目前是死的** (代码有自承注释 "task 6 scope, a later increment")。本仓 enforced=all 无影响, 但配了 read_only 的采用者会误纳。
- 🔴 **3.4 非交互 git 契约缺失** — `GIT_TERMINAL_PROMPT`/`GIT_SSH_COMMAND` BatchMode/`stdin=DEVNULL` 全仓零命中; `_common.py:_run` 只靠 subprocess timeout 兜底, 交互提示会挂到超时。
- 🔴 **2.12 (AC-5) tracks_multibranch 同分支不可达检测零覆盖** — task 自预警"无任务⇒AC 勾了从没实现", 实测确认无代码/测试 (因未打勾未虚标)。
- **1.6 命名空间 split-brain** — state-scanner 用 `state_scanner.multi_remote.enforced_remotes`, phase-c-integrator 用顶层 `multi_remote.enforced_remotes`, 不同 JSON 路径未对齐。
- **13.3/9.2 gitlink drift 文案** — blocking 裁决已接线, 但 `multi_remote_drift` 第七路 (gitlink) 建议文案未实现 (basic-rules/RECOMMENDATION_RULES 已记缺口)。
- **1.8/1.10/7.2 doc drift** — multi_remote.py:4 canonical-SOT 措辞 / verify_mode=ls_remote 未退役 / git-remote-helper schema.md:58 旧语义。

**DEFERRED (fail-CLOSED, 蓝图 + 3 轮 review 一致裁定)**:
- **3.16 k_eff observed_rotation 未持久化** — k_eff=k_min 冷启动兜底 (multi_remote.py docstring 自述)。**AC-15 防饥饿仅 rotation≤k_min=3 采用者完全成立**; 大仓 (rotation>3) 被砍腿→expired→blocking 偏红。**不得记 AC-15 已完全满足**。

**待 owner 裁 (OQ-C, Phase A 未锁死)**: 1.3 / 9.3 multi_remote_drift 离线 debounce/冷却 — proposal 有倾向 (不造有状态冷却, 用 has_unreachable 建议层降级) 但 tasks 未勾。

## §3 关键风险 / 已知陷阱 (本 session 新增)

- 🔴 **agent 测试 fixture 反推匹配 buggy 实现 = 假绿** (Phase 2 gitlink BLOCKER 实证): agent 的 gitlink ok 测试用 stale/None leg 却期望 ok (因 buggy 无条件 ok), 掩盖了"陈旧 refs 上的 ok = false-green"。**主 loop 亲验 + 对抗 review 才抓得到; agent 自测不够** (memory `feedback_check_predicate_must_validate_against_real_data_range` 强复现)。
- 🔴 **勾选完成≠运行现实** (Phase 1 consecutive_unverified 实证): agent docstring 谎称"F1/F4 owns increment" 但 F1/F4 只读 → D18 死码。review 抓 (memory `feedback_completion_signals_vs_runtime_invocation`)。
- **防御 fix 连环 fix-introduced** (blocker 修 → offline 计数器漂移回归): gitlink ok 加豁免门后, offline+¬豁免→orphan_unverified 令计数器每 scan +1 → 补 offline 冻结 (9.7 counter face)。**机制变更后必跑 offline 稳定性 + 全套件** (memory `feedback_multiround_audit_catches_fix_introduced_regression`)。
- **119 checkbox 全未勾但代码已实施** — 实施与 tasks.md 状态脱节; Phase D 前必审计标记, 否则归档门看"未开始"或虚标。

## §5 多维度同步状态 (session-close 最终态)

- **git**: aria master `e162f7b` (v1.60.0) + 主仓 master `d319d6f`; origin+github 双远程 ls-remote 三方 parity 验证齐。feature 分支 `feature/state-scanner-stale-refs-false-parity` 已 FF 合入 aria master (可删或留续做 29 TODO)。
- **版本**: 插件 v1.59.1→**v1.60.0** (5 SOT + root README badge/i18n zh/ja/ko + 主仓 VERSION 表行); 8 custom checks 绿。
- **coordination claim**: 本 session 持有 (simonfish/bfe8285d, Phase B acquire), 收尾时 release (见 §7)。
- **并发**: bot 本 marathon 期间 ship 了 aria v1.59.0/v1.59.1 (Phase 0 / reconcile #111), 均已 rebase 对齐 (disjoint lib/reconcile.py)。

## §6 Next session 入口 + 优先级

**主 spec 仍 active** (核心已 ship v1.60.0, 29 TODO 未做)。落地选项:
1. ⭐ **实质 TODO 收口** (建议下个专门 session): 6.1/6.2 F5′ 接进 _overall_parity (read_only 死配置活化) + 3.4 非交互 git 硬化 + 2.12 tracks 同分支不可达 (AC-5) + 1.6 命名空间对齐。这些做完 spec 才接近可归档。
2. **k_eff observed_rotation** (3.16, DEFERRED): 若有大仓 (rotation>3) 采用者反馈恒红, 再落地 per-host rotation 持久化 → k_eff=min(K_CAP,max(k_min,rotation))。
3. **OQ-C 裁定** (owner): 1.3/9.3 drift debounce 去留。
4. **归档** (D.2): 待 29 TODO 收口 (或 owner 裁定哪些可 defer 为独立 follow-up spec) 后走 openspec-archive。
5. **Aria #165** (镜像漏推): 方案 B 复用 F10″ gitlink_orphaned 谓词, 建议并入非单开。

**其它 carry-forward** (承前, owner 门): M6 4 门 / 168h 跑 / M7 fleet (其 overall_parity 消费已同步 CAVEAT-parity note)。

## §8 Memory entries this session

- **已落** (前序): `feedback_version_checks_blind_to_i18n_readme_body` (version check 盲区)。
- **候选 (本 session, 评估后)**:
  - agent 测试 fixture 反推匹配 buggy 实现 = 假绿, 主 loop 亲验 + 对抗 review 才抓 → 已有 `feedback_check_predicate_must_validate_against_real_data_range` 覆盖, 不重落。
  - 多 goal 连续驱动 marathon (Phase 0→1→2/3→ship) 每 phase 一 agent-team 动态工作流 + 主 loop 亲验闭环 → 已有 `feedback_agent_team_dynamic_workflow_division` 覆盖。

## Cross-references

- 主 spec: `openspec/changes/state-scanner-stale-refs-false-parity/` (v10 Approved, 核心 shipped v1.60.0, active)
- 前序 handoff: `docs/handoff/2026-07-17-mainspec-phase0-v1.59.0-ship.md` (Phase 0 + 四段式 roadmap)
- ship commits: aria `e162f7b` (v1.60.0) / 主仓 gitlink `d319d6f`
- Issue: Aria #165 (镜像漏推, 复用 F10″) / aria-plugin #110·#92 (姊妹 spec C/B, 已 ship)

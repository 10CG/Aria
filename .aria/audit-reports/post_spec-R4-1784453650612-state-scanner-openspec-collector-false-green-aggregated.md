---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: true
verdict: PASS
oscillation: false
drift_anchor_missing: false
drift_check_skipped: false
incomplete: false
spec_id: state-scanner-openspec-collector-false-green
timestamp: 2026-07-18
---

# post_spec Convergence Audit (aggregated) — state-scanner-openspec-collector-false-green (#166)

**Team (5)**: aria:tech-lead / aria:backend-architect / aria:qa-engineer / aria:code-reviewer / aria:knowledge-manager
**Anchor**: primary_goal = state-scanner OpenSpec 维度 (collector + archive gate) 布局/数据源不符时可见 (soft_error/warn/tracker) 而非静默假绿 (#166 三缺陷), 每缺陷配 baseline-failing 测试。
**Source SHA (freeze)**: dc4568d
**Result**: **CONVERGED (PASS)** after 4 rounds. 0 Critical / 0 Major outstanding.

## 收敛轨迹

### R1 — 1 PASS / 4 REVISE (5/5 SCOPE_OK)
- **[Critical] 缺陷2 位置钉错 (backend + qa + km 3-agent 收敛, code-grounded)**: issue 标题 `d_payload` 真实生产者是 `lib/spec_complete.py::gate_result()` (:1298-1300 独立 tasks.md 早退, 对 detailed-tasks.yaml-only 项目失明), 非原 proposal 钉的 `collectors/openspec.py:244` (只喂快照 carry_forward_inventory 展示字段, 两条不相交调用链)。原 proposal 继承 issue 自身 mis-citation。
- [Major] M1 drift 路径 configured 取值未定义 (load-bearing) / M2 重构 early-return 需 loop 守卫 + 缺陷2 elif 耦合 / M3 doc sync 漏 status-field-guide.md + output-formats.md / M4 缺对称负控 SC。
- [Minor] ×7: 根因行号漂移 / 测试路径 scripts/tests→tests / SC-8 dogfood 本 repo dir 对缺陷2 不成立 / SC-3 漂移形状 / soft_error 命名前缀 / 全归档终态噪音 / 缺陷3 design_deferred→pending_archive 联动 / 缺 Created。

### R1-fix → R2 — 3 PASS / 2 REVISE (5/5 SCOPE_OK)
- R1 全部 findings **5/5 确认闭合** (缺陷2 位置修正到 gate_result per owner option A; configured=False 落定 + 无消费方核实; 负控 SC-2/SC-6; 行号/路径/命名校正)。
- **[新 Major] 缺陷2 surfacing 机制 (backend Major + km Major + tech-lead Minor, 3-agent 收敛)**: 仅 verdict=warn 不足 —— openspec-archive D auto-issue 门控 `d_payload != null` (非 verdict), warn_overlay 落盘 `unverified_claims` (非 warnings); 保 d_payload=None 则 headless 归档残留仍静默埋。

### R2-fix → R3 — 2-agent 焦点轮 (5/5 SCOPE_OK)
- R2 Major **闭合** (改走 unverified_claims 通道 + 构造非 None d_payload → warn_overlay frontmatter + D-tracker 双点亮, 复用 #95 零改 openspec-archive; `_build_d_payload:1128` 因果链 code-grounded 验证)。
- **[新 Major, rationale-only, 0-logic] 先例定性弄反 (backend + km 收敛)**: proposal 称「与 `_fold_runtime_probe` 先例有意分歧」错 —— 主线 warn/invalid 分支 (:1235-1256, docstring :1197-1200) **本就双写** warnings+unverified_claims (正为达 warn_overlay+D auto-issue); fix 实为**遵循**先例非背离。原引 :1429-1440 系崩溃兜底另一类。
- [Minor] unverified_claims 条目缺 symbols 键 (类型契约 {claim,reason,symbols})。

### R3-fix → R4 (稳定确认) — 2 PASS / 0 REVISE (5/5 SCOPE_OK)
- R3 Major (先例 rationale 更正为「遵循主线双写先例」) + Minor (补 symbols:[]) **闭合**; 两 agent 逐行核验 :1235-1256 双写 + docstring + :1429-1440 崩溃兜底切割准确。
- km 全文档一致性核验: Impact/SC/设计决策/非目标/follow-up 无自相矛盾或悬空引用; Rule #3 清单完整。
- **0 新 finding → CONVERGED。**

## 最终 in-scope 结论 (供 Phase B)
- **缺陷1** `collectors/openspec.py`: 移 early-return + loop 套 `if changes_dir.is_dir()` 守卫 + 正交扫 archive + 高置信 `layout_drift` soft_error (archive 非空或有裸 proposal) + configured 保 False。
- **缺陷2** `lib/spec_complete.py::gate_result:1298-1300`: yaml-only 分支追 `unverified_claims` 条目 (含 symbols:[]) + verdict=warn + 构造非 None d_payload (遵循 :1235-1256 双写先例) → warn_overlay + D-tracker 双点亮 headless。完整 yaml 解析留 follow-up。
- **缺陷3** `collectors/_status.py:199`: done 家族加 `completed` token (不重开 #101, 实跑验证)。
- 11 条可证伪 SC (含 SC-2/SC-6/SC-8 对称负控); doc sync: state-snapshot-schema.md + status-field-guide.md + output-formats.md。

**Owner sign-off pending** → A.2 task-planning + Phase B。

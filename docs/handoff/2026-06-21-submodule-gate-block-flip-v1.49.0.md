---
track-id: submodule-gate-block-flip-v1.49.0
owner-container: simonfishgit/dev-claude
phase: D-complete
status: done
updated-at: 2026-06-21T11:30:00Z
---

# Aria — Session Handoff (2026-06-21) — submodule-gate warn→block flip v1.49.0 (#124)

> **Status**: ✅ **DONE & SHIPPED** (aria-plugin **v1.49.0**, PR #90 `f3b7ac5` 双远程; standards `ddaf3d1` 双远程; 主仓 v1.7.1; Spec 归档)。**block-flip 闭环** (D+14 DEFER → telemetry 修 → Trigger B flip)。
> **本 session 全景** (长, 多 cycle): #145 re-triage → **v1.48.0** agent-team-audit 增补 ship → i18n marker 同步 → **v1.49.0** block-flip (本 doc)。
> **Next session 入口**: 读本 doc → `/aria:state-scanner` → §2。无 carry-forward 阻塞; 主线 M6/M7 仍 owner/外部门控。

## §0 入口（新 session 优先读）

1. block-flip warn→block **已 flip** (v1.49.0)。submodule pointer regression gate 现 **block 默认** —— in-flight feature 分支若含 submodule pointer regression/divergence 且无 override (trailer `Submodule-Rollback:` 或 label) → **merge 被拒 exit 1**。逃生舱: `mode=warn` (legacy) / `mode=off` (bypass) / env `ARIA_SUBMODULE_GATE_MODE` override。
2. 这是本 session 第 2 个 ship (前 v1.48.0 见 `2026-06-21-agent-team-audit-project-agent-augmentation-v1.48.0.md`)。
3. 主线 M6 ship / M7 Phase B 未触碰 (owner/外部门控)。

## §1 已完成

| 步骤 | 内容 | 验证 |
|------|------|------|
| 评估 | /state-scanner 检出 block-flip READY 5/3 → owner 评估 | 真实 telemetry 核实 (5 executions + 4 tripwire + FP 0%) |
| 决策 | owner **risk-accept flip** (透明披露重试虚增, 严格独立观察=2) | 决策记录 §4 |
| §A flip | submodule_gate.sh:33 + SKILL.md:450 `:-warn}`→`:-block}` + config/wording 全集 | grep 0 残留 warn-default |
| 测试 | T-flip-12 (unset MODE→block, regression exit 1) | 15 PASS / 0 FAIL (was 14) |
| §F | standards submodule-pointer-hygiene wording + CLAUDE.md cross-ref | `ddaf3d1` |
| Phase C/D | aria PR #90 `f3b7ac5` + standards `ddaf3d1` + 主仓 gitlink×2 + VERSION 1.7.1 + 5 SOT v1.49.0 + Spec 归档 | 三远程 parity |

**关键证据 (Trigger B)**: 5 gate executions (all warn-PASS) + 4 clean host-cron tripwire + FP 0%。owner risk-accept。

## §2 未完成 / Carry-forward

无 block-flip carry-forward (闭环)。

### 主线 (owner/外部门控)
- ⭐ M6 ship = M7 Phase B D3 门 (owner: 168h 运营跑 + AC-5)。
- #136 Feishu secret 轮换 (owner)。

## §3 关键风险 / 已知陷阱

| 风险 | 触发 | 缓解 |
|------|------|------|
| **block-flip 后首次 merge 撞 block** (R7) | flip 后 in-flight 分支含 submodule regression | 决策记录 §6 审查: 无 in-flight 撞 block。今后真撞 → override trailer/label 或 mode=warn |
| standards 子模块并发 sister 推送 | 本 session 实遇: forgejo origin 已被 sister PR #11 推进到 cdf6bfd | fetch 后 rebase 我的 commit 到 origin/master (sister 不同文件无冲突) + origin ff + github force-with-lease |
| index.lock 反复竞争 | 本 session 多次 (疑后台 telemetry hook 周期碰 git) | pgrep -x git 确认无活跃进程 (真命中过 1 次 transient, 等其退出) + 0字节 lock 安全 rm |
| telemetry 重试虚增 executions | index.lock 重试致同一 commit 多次记 telemetry | flip 评估时核实原始 jsonl 区分独立 ship 事件, 透明披露给 owner |

## §4 实战教训（memory 候选）

1. **telemetry 计数虚增辨识**: index.lock 重试致同一逻辑 gitlink commit 被 PostToolUse telemetry hook 多次记录 → "5 executions" 实质 2 独立 ship。评估门控阈值时须核实原始 jsonl 时间戳聚类, 区分独立事件 vs 重试, 透明披露给 owner 而非只报 raw count。
2. **flip 锁定测试**: 改默认值的 flip 必须配一个"断言新默认"的测试 (T-flip-12: unset env → 新默认行为), 否则回退无守卫。
3. **并发子模块 ship 的 rebase 吸收**: 子模块 (standards) forgejo origin 被 sister 推进时, github 已收我的 commit → fetch + rebase 我的到 origin/master + origin ff + github force-with-lease (我的旧 commit 是自己刚推的, 安全替换)。

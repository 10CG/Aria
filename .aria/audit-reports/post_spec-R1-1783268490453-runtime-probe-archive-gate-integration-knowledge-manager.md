---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-07-05T16:14:47.390Z
context: openspec/changes/runtime-probe-archive-gate-integration/proposal.md
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

> **ORCHESTRATOR 核实注记**: CRITICAL-2 关键引文经独立核实为真 (ERRATA.md:3 明文「不修改本目录
> tasks.md / proposal.md 本身」)。CRITICAL-1 与 backend-architect/qa/code-reviewer 的零 frontmatter
> 全语料扫描交叉一致。两 Critical 成立。

## 审计结论

### CRITICAL-1 — "#95 归档时写 frontmatter unverified_claims" 先例经全语料核验从未真实发生过

- type: issue / severity: critical / category: documentation / scope: proposal §What 4 (:63) / tasks 4.2 (:31)
- summary: 该"先例"仅是被设计+合成 fixture 测试覆盖的机制, 在全部 118 个已归档 proposal.md (含 #95 自身) 中从未被真实写入过一次; proposal 将"已测试"误引为"已验证的真实先例"。
- evidence:
  - `grep -rn "^unverified_claims:|^archive_type:" openspec/archive/*/proposal.md` → **0 命中** (118 个文件)。全仓 permissive 搜索: 除本 proposal 自身引用外, 所有命中均在 #95 自身 spec 描述该机制的散文/任务行, 无一是机制真实写入产生的 YAML 键。
  - #95 归档 proposal.md:1,3 — 自称 "verdict=warn ... 7 warn" 但文件第 1 行即 `# Proposal:` (无 --- 块) — warn 触发时机制化写入**并未落地到被归档文件**; 第 3 行说明是手写摘要非 Step2 warn_overlay 机械产物。
  - 机制定义: openspec-archive SKILL.md:173-190 (warn_overlay) + test_archive_gate_integration.sh:60-73 (仅合成 fixture 断言, 且是测试自己脚本化模拟写入)。
  - 与本项目方法论正相关: 恰是 `feedback_completion_signals_vs_runtime_invocation` (单测过 ≠ 生产真发生) 在 #95 自身的又一实例 — 具讽刺意味但确凿。

### CRITICAL-2 — "母 spec ERRATA" 先例真实存在, 但其确立的规范与 task 4.2 拟议动作方向相反

- type: issue / severity: critical / category: documentation / scope: proposal §What 4 (:63) / tasks 4.2 (:31)
- summary: ERRATA.md 明文规定"不修改本目录 tasks.md / proposal.md 本身", git 历史证实该提交对母 spec 两文件零改动 (只新增 ERRATA.md); task 4.2 却计划直接向已封存归档 proposal.md frontmatter 加新键, 是该先例明确避免的动作模式。
- evidence:
  - ERRATA.md:3 原文:「**不修改本目录 `tasks.md` / `proposal.md` 本身**(归档记录保持原样,不回改历史勾选)」。
  - `git show ed963e8 --stat` 证实: 该提交仅新增 ERRATA.md (+48 行); 母 spec proposal.md/tasks.md 未出现在改动列表。
  - task 4.2 是由**后续不相关 spec** 回头改**已完全封存**归档文件本体 — ERRATA 先例从未有此动作。proposal 未正面承认张力, 只贴"先例"标签带过。
- 建议 (供 owner 决策): (a) 仿 ERRATA 模式加旁路文件 (如 RUNTIME-PROBE-DECLARATION.md) 承载声明, gate 读取 "proposal frontmatter 优先, 旁路文件兜底"; 或 (b) 保留直接改 frontmatter 方案, 但正面写明这是对"归档只加不改"边界的一次**新扩展** (理由: 纯前瞻性 opt-in 声明, 不改写历史真实性判断, 风险极低) 而非"沿用先例" — 让 owner 知情决定。

### MAJOR-1 — 版本 SOT 清单 (tasks 4.5) 未显式列出"主项目 /VERSION 插件版本行"

- type: risk / severity: major / category: documentation / scope: tasks 4.5 (:34) / proposal Impact (:70 "5+1")
- summary: task 4.5 只写"主仓 badge/Project Status 同步 + 子模块指针 bump", 未提 CLAUDE.md 检查清单独立勾选项"主项目/VERSION 更新插件版本记录" (6-surface 之第 6)。三处为不同文件位置, 有 Phase D 漏更新风险。
- evidence: CLAUDE.md 版本发布检查清单·主项目段 (4 独立勾选) / VERSION:28 (`| aria (子模块) | v1.53.0 |`) ≠ README.md:8 (badge) ≠ README.md:242 (Project Status) / "5+1" 精确定义 = aria-2.0-m6-release-closeout/proposal.md:158-165 (Gate G-7 "6 surfaces")。

### 核对通过项 (逐项验证, 无 finding)

- DEC ↔ proposal ↔ tasks: 4 字段 schema / 三态语义 / fail-toward-warn 单调升级 / 三正交 / out-of-scope 边界 — 逐项一致 ✓
- Rule #6 disposition 先例属实 (与 #95 归档 proposal.md:67 几乎逐字对应); memory 引用真实且用法准确 ✓
- state-snapshot-schema "零改动"声称成立 (gate_result 只经 SKILL.md Bash CLI stdout 消费, 非 snapshot 字段面) ✓
- state-scanner SKILL.md / RECOMMENDATION_RULES.md / layer-l-integration.md 不涉 coordination_probe 内部/gate_result — 不列入 Impact 是正确的 (非遗漏) ✓; state-checks description 行为性描述在 CLI "逐字节不变"承诺下无需同步 ✓
- telemetry JSONL 无 per-record symbol 字段 (phase1_gate.py:961-971 _emit_telemetry 实测) — 与 "symbol 只当标签"吻合 ✓
- 环境事实: plugin.json=1.53.0 ✓ / coordination.enabled=true ✓ / telemetry 缺失 + 实跑 coordination_probe.py exit 1 RED ✓
- Level 3 判定 / convergence 要求 / falsifiable 要求与 DEC 一致 ✓
- SC-1~9 与 tasks 4 Phase 逐条映射无孤儿 SC ✓
- house style 与 #95 先例高度对齐 ✓

## Verdict

**verdict: FAIL** (2 Critical + 1 Major; FAIL=≥1 Critical) | **vote: REVISE**

理由: 技术设计层面 (探针库泛化 / tri-state 折入 / fail-toward-warn / 测试矩阵) 扎实、可证伪、与 DEC 高度一致。但两处 Critical 都落在 task 4.2 "给已归档 spec frontmatter 追加声明"的正当性论证: 引用的两条"先例"经核实要么建立相反规范 (ERRATA: 只加新文件不碰原文件), 要么从未真实发生 (0/118) — 若不修正, 等于在 owner 不知情下用站不住脚的引用为"修改已封存归档文件"这一新先例背书。MAJOR-1 独立可快速修。预期下一轮快速收敛。

## 轮次记录

R1 — Read: proposal / tasks / DEC / #95 归档 proposal 全文 / ERRATA.md 全文 / coordination 归档 proposal 全文 / coordination_probe.py 全文 / spec_complete.py 全文 (两页) / phase1_gate.py (_emit_telemetry 段) / openspec-archive SKILL.md (Step2 段 150-230) / standards/openspec/project.md (grep 140/152 归档惯例) / VERSION / README.md / aria-2.0-m6-release-closeout proposal ("5+1" 定义段) / state-snapshot-schema.md / RECOMMENDATION_RULES.md / recommendation-stages.md / layer-l-integration.md / state-scanner SKILL.md / .aria/state-checks.yaml / .aria/config.json / audit-engine SKILL.md (verdict 公式)。辅助: git log --follow + git show --stat (ERRATA 提交溯源) / 全语料 grep (118 归档) / 实跑 coordination_probe.py (验证 RED)。

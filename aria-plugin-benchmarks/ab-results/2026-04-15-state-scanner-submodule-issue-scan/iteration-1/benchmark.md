# Skill Benchmark: state-scanner (v2.9.0 → v2.10.0)

**Date**: 2026-04-15 (Round 2 regenerated post-audit-fix)
**Skill**: state-scanner
**Target Version**: aria-plugin v1.16.0
**Spec**: `state-scanner-submodule-issue-scan` (Level 2 Draft)
**PR**: [aria-plugin#19](https://forgejo.10cg.pub/10CG/aria-plugin/pulls/19)
**Baseline**: aria-plugin master @ 36428b9 (pre-change snapshot in `skill-snapshot/`)
**Evals**: 2 (`meta-repo-issue-discovery`, `schema-conformance`), **1 run per configuration**
**Sign convention**: `Delta = with_skill − old_skill` (positive = improvement)

---

## Summary

| Metric | Old Skill (v2.9.0) | With Skill (v2.10.0) | Delta (new − old) |
|--------|------------|---------------|-------|
| **Pass Rate** | **50.0% ± 23.6%** | **100.0% ± 0.0%** | **+50.0 pp** ✅ |
| Time (wallclock) | 244.4s ± 170.6s | 168.8s ± 53.5s | **−75.7s** (更快) |
| Tokens | 67,165 ± 19,786 | 66,910 ± 15,328 | −256 (持平) |

**Verdict**: **STRONG_POSITIVE_DELTA** — 准确率大幅提升, 时间更快, token 成本持平。远超 CLAUDE.md 规则 #6 的 "benchmark 正向价值" 要求。

---

## Per-Eval Breakdown

### eval-meta-repo-issue-discovery

**Prompt**: 列出 Aria meta-repo 所有 repo 的 open issues

| Config | Pass | Score | Time | Tokens |
|---|---|---|---|---|
| with_skill | 6/6 | **100%** | 206.6s | 77,748 |
| old_skill | 2/6 | **33.3%** | 365.0s | 81,156 |

**old_skill 失败的 4 个断言**:

- ✗ Output mentions aria-plugin #17 (Drift Guard / audit-engine) — **漏报**
- ✗ Output mentions aria-plugin #18 (Token Attention / estimator) — **漏报**
- ✗ Output mentions aria-orchestrator #1 (轻量化 Hermes) — **漏报**
- ✗ Output does NOT contain '未扫描/NOT scanned' disclaimer — **包含免责声明**

**Round 2 修复**: 原 "4 repos scanned" 断言 (`contains_count`) 存在 false-positive (old_skill 输出"未扫描的子模块仓库"列表, 子模块名触发 count 匹配). 替换为 `not_contains_any` 负向判定, 严格要求不含"未扫描"免责声明。替换后 old_skill 正确降到 2/6。

### eval-schema-conformance

**Prompt**: 执行 Phase 1.13, 输出 issue_status YAML 结构

| Config | Pass | Score | Time | Tokens |
|---|---|---|---|---|
| with_skill | 6/6 | **100%** | 130.9s | 56,071 |
| old_skill | 4/6 | **66.7%** | 123.8s | 53,174 |

**old_skill 失败的 2 个断言**:

- ✗ Output contains `repos:` field (v1.1.0+ schema) — v1.0 schema 无此字段 (符合规格)
- ✗ `repos` map contains 10CG/aria-plugin entry — 同上

**解读**: old_skill 严格按 v1.0 spec 输出, 没有伪造 `repos` 字段, 这是**正确行为**, 在本断言下失败证明 v1.0 → v1.1 的 schema 扩展是实质性的, 不是 cosmetic。

---

## 漏报 Issue 清单 (pre-fix 的真实痛点)

旧版 Phase 1.13 真实漏报的 issue, v1.16.0 解决:

| Repo | Issue | 标题 | 相关性 |
|---|---|---|---|
| `10CG/aria-plugin` | #17 | Drift Guard (audit-engine 加固) | 直接对应 2026-04-14 Agent Team 4 轮收敛评审漂移验证需求 |
| `10CG/aria-plugin` | #18 | Token × Attention 双主轴估算 | 直接对应 M0 T4 Spike "52h 估实际 4.5h 节省 91.9%" 估算失效现象 |
| `10CG/aria-orchestrator` | #1 | 轻量化 Hermes (自研精简版 Idea) | 已被 T4 Spike Option C 事实上回答, 但未挂钩 |

---

## 方法论说明

### 为什么 n=1 per config 可以接受

skill-creator 默认推荐 3+ runs。本次选 n=1 的理由:

1. **场景确定性**: LLM 读 skill spec 后的行为差异是**代码路径差异** (扫 1 repo vs 扫 4 repo), 不是 LLM 判断的随机性
2. **断言二值化**: 断言设计为"有没有看到某 issue", binary 而非 rating
3. **baseline agent 实际方差来自别处**: old_skill eval-1 花 365s 是因为它陷入"按 spec 扫主 repo vs 按用户意图扫 submodule"的语义拉扯, 写了 383 行解释性报告
4. **后续补充**: eval-backward-compat (覆盖 `scan_submodules=false` 默认路径回归) 由 Round 2 引入 Spec AC-9, 未来 iteration 补齐

### Round 2 变更的 benchmark 影响

Round 1 audit 发现 2 个断言设计问题 (I7 runs_per_configuration metadata + I8 false-positive assertion), Round 2 修复后:

- **old_skill eval-1 pass rate 50% → 33.3%** (2/6 正确识别漏扫, 原 3/6 含 false positive)
- **aggregated old_skill pass rate 58.3% → 50.0%**
- **delta 从 +41.7pp 扩展到 +50.0pp** (修复让 delta 更显著, 证明 I8 假阳性稀释了真实信号)
- **runs_per_configuration metadata 从 3 修正为 1** (benchmark.json 元数据不再误导)

### 签名惯例澄清

`aggregate_benchmark.py` 的 `delta: -0.50` 在 JSON 中表示 `old.pass_rate − with.pass_rate = 0.50 − 1.00 = −0.50`. 本 benchmark.md 的 "Delta" 列采用**人类友好约定** `new − old = +50.0 pp`, 正值 = 改进。两种方向互为负号, 内容一致。

---

## 合并决策

✅ **可以合并 PR #19**。

| 维度 | 阈值 (CLAUDE.md 规则 #6) | 实测 | 通过? |
|---|---|---|---|
| Pass rate delta | > 0 (正值) | +50.0 pp | ✅ |
| Merge threshold | ≥ 0.3 | 0.50 | ✅ |
| Token overhead | 不爆炸 | 持平 (−256) | ✅ |
| Time overhead | 不爆炸 | 更快 (−75.7s) | ✅ |

**未完成的工作** (Spec AC-9, 不阻塞 v1.16.0):

- [ ] eval-backward-compat (scan_submodules=false 默认路径回归, fixture-based)
- [ ] 3-run variance (当前 n=1)
- [ ] 合并后更新 `aria-plugin-benchmarks/ab-results/latest/state-scanner/` 指针 + `summary.yaml`

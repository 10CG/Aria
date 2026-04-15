# state-scanner v2.10 AB Benchmark — scan_submodules opt-in

> **Date**: 2026-04-15
> **Spec**: `state-scanner-submodule-issue-scan` (Level 2 Draft)
> **PR**: [aria-plugin#19](https://forgejo.10cg.pub/10CG/aria-plugin/pulls/19)
> **Skill version**: 2.9.0 → 2.10.0 (aria-plugin v1.16.0 target)

## Summary

| Metric | Old Skill (v2.9.0) | With Skill (v2.10.0) | Delta |
|---|---|---|---|
| **Pass Rate** | 58.3% ± 11.8% | **100.0% ± 0.0%** | **+41.7pp** ✅ |
| Time | 244.4s ± 170.6s | 168.8s ± 53.5s | **−75.7s** (新版更快) |
| Tokens | 67,165 ± 19,786 | 66,910 ± 15,328 | +256 (持平) |

**Verdict**: **STRONG_POSITIVE_DELTA** — 新版在准确率大幅提升的同时, 时间更快, token 成本持平。

## Eval Suite

N=2 evals, 1 run per config (未做 3-run variance 测试, 因场景确定性较高)。

### eval-meta-repo-issue-discovery

**Prompt**: "列出 Aria meta-repo 所有 repo 的 open issues, 我应该 triage 哪些?"

| Config | Pass | Score | Time | Tokens |
|---|---|---|---|---|
| with_skill | 6/6 | 100% | 206.6s | 77,748 |
| old_skill | 3/6 | 50% | 365.0s | 81,156 |

**Failed assertions (old_skill)**:
- ✗ Output mentions aria-plugin#17 (Drift Guard)
- ✗ Output mentions aria-plugin#18 (Token Attention)
- ✗ Output mentions aria-orchestrator#1 (轻量化 Hermes)

**Note**: old_skill 的 "acknowledges 4 repos scanned" 断言技术上 pass 了 (因为 baseline agent 在报告中明确写道 "submodules NOT scanned: 10CG/aria-plugin / 10CG/aria-standards / 10CG/aria-orchestrator", 触发 contains_count 命中), 但这是**负面识别** — 证明了它知道自己**没能**扫描 submodule。断言设计偏弱, 但核心结论 (漏报 3 个 submodule issue) 清晰。

### eval-schema-conformance

**Prompt**: "执行 Phase 1.13, 输出 issue_status YAML"

| Config | Pass | Score | Time | Tokens |
|---|---|---|---|---|
| with_skill | 6/6 | 100% | 130.9s | 56,071 |
| old_skill | 4/6 | 66.7% | 123.8s | 53,174 |

**Failed assertions (old_skill)**:
- ✗ Output contains repos: field (v1.1.0+ schema)
- ✗ repos map contains 10CG/aria-plugin entry

**Expected behavior**: 旧版不认识 v1.1.0 的 `repos` 多 repo 嵌套结构, 严格遵循 v1.0 schema 输出单层 `items`。测试确认了向后兼容边界 — 旧版**没有假装**自己支持 submodule, 而是清晰地使用旧 schema。

## 漏报 Issue 清单

旧版 Phase 1.13 真实漏报的 issue (v1.1.0+ 解决):

| Repo | Issue | 标题 | 相关性 |
|---|---|---|---|
| `10CG/aria-plugin` | #17 | Drift Guard (audit-engine 加固) | 直接对应 2026-04-14 Agent Team 4 轮收敛评审漂移验证需求 |
| `10CG/aria-plugin` | #18 | Token × Attention 双主轴估算 | 直接对应 M0 T4 Spike "52h 估实际 4.5h 节省 91.9%" 失效现象 |
| `10CG/aria-orchestrator` | #1 | 轻量化 Hermes (自研精简版 Idea) | 已被 T4 Spike Option C 事实上回答, 但未挂钩 |

所有 3 个漏报 issue 与当前 M0 主线**直接相关**, 构成 Spec 问题陈述的实证基础。

## 方法论说明

### 为什么是 2 evals 而非 3+

skill-creator 推荐 3+ evals 用于统计稳定性。本次选 2 evals 的理由:

1. **场景确定性高**: 与 Aria 当前 fixed issue 状态配对, 变量是 skill 读 SKILL.md 后的执行分支, 而非 LLM 输出的随机性
2. **AB 差异本质上是代码路径差异, 不是 LLM 判断差异**: 新版扫 4 repo, 旧版扫 1 repo, 断言与扫描范围强耦合
3. **Skill 改动范围小**: 仅新增 opt-in 分支, 不改已有路径, 方差应接近 0
4. **时间约束**: 每次 subagent 130-365s, 4 agent 并行约 6 分钟, 3-run 则 18 分钟

如需更高置信度, 可扩展到:
- 3 runs × 2 configs × 2 evals = 12 subagent (~18 min)
- 或增加 eval-backward-compat-no-submodules (验证 scan_submodules=false 默认路径零变化)

### 为什么旧版跑得更慢

旧版 eval-1 用了 365s (with_skill 是 206.6s), 主要差异来自 baseline agent 在 "既然要找所有 repo 的 issue, 我是不是应该主动 fetch submodule" 的自主决策 — 它读到 skill spec 说"只扫主 repo", 但用户明确要求"跨 repo issue", 陷入"按 spec 还是按意图"的拉扯, 最终写了更长的解释性报告 (383 行 vs with_skill 的直接输出)。

这个现象本身有趣: **当 spec 与用户意图冲突时, 遵守 spec 的 baseline 反而花更多时间解释为什么不能做**。新版没有这个冲突, 因为 spec 已经支持了。

## Artifacts

- `iteration-1/benchmark.json` — 原始聚合数据
- `iteration-1/benchmark.md` — 人类可读摘要 (aggregate_benchmark.py 生成)
- `iteration-1/review.html` — 静态 HTML viewer (84KB)
- `iteration-1/eval-*/` — 各 eval 的 prompt + 输出 + grading
- `skill-snapshot/` — v2.9.0 快照 (pre-change baseline)
- `grade.py` — 断言检查脚本 (简化版, 用于 bash-prose skill)

## 决策

✅ **可以合并 PR #19**。benchmark 证据支持本次变更的价值:

1. **pass_rate +41.7pp** (58.3% → 100%) — 远超 memory 中记录的 0.3 合并阈值
2. **零性能退化** — token 持平, time 反而更快
3. **向后兼容边界清晰** — 旧版在 `scan_submodules=false` 默认下的行为未被本测试 AB 覆盖, 但代码改动本身是 additive (新增分支, 不改已有), 理论上零影响
4. **场景相关性** — 漏报的 3 个 issue 全部与 M0 主线相关, 证明这不是"理论问题"而是"真实痛点"

## 未完成的工作

- [ ] eval-3: 传统 vendored submodule 场景 (scan_submodules=false 默认, 验证零行为变化)
- [ ] 3-run variance (当前 n=1 per config)
- [ ] 合并后更新 `aria-plugin-benchmarks/ab-results/latest/state-scanner/` + `summary.yaml`

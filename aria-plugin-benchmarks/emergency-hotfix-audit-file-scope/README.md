# emergency-hotfix-and-audit-file-scope — Rule #6 structural substitute (#58)

> #58 是纯 prose/config/convention 改动 (6 skill + config + git-commit convention)，无 LLM AB
> (per `feedback_deterministic_structural_skill_rule6_substitute`)。Rule #6 由 **doc-existence
> 确定性 fixture** 替代，行为遵从性标 **dogfood-only**。

## 文档存在性 (deterministic fixture — `test_doc_existence.py`, 10/10 PASS)

grep-验证每个 deliverable 的必要内容存在 (字段/字符串):

| # | check | file |
|---|-------|------|
| 1 | emergency_hotfix 规则字段 (priority 1.85 / confidence 85% / auto_execute No) | state-scanner/references/rules/basic-rules.md |
| 2 | emergency_hotfix 索引行 (双写) | state-scanner/RECOMMENDATION_RULES.md |
| 3 | scope_skip_paths 默认清单 | config-loader/DEFAULTS.json |
| 4 | scope_skip_paths 匹配语义 (startswith/endswith) | config-loader/config-example.md |
| 5 | Prod-Validated 单行 trailer + hotfix commit 格式 | standards/conventions/git-commit.md §6.4 |
| 6 | phase-b Prod-Validated trailer gate (block if absent) | phase-b-developer/SKILL.md |
| 7 | audit-engine file-scope (merge-base 自取 / 0-file pass-through / min(resolved,convergence)) | audit-engine/SKILL.md |
| 8 | audit-engine emergency hotfix pre_merge→convergence (仅 audit-on) | audit-engine/SKILL.md |
| 9 | phase-a-planner lane overview (skip A.1-A.3 + cross-ref) | phase-a-planner/SKILL.md |
| 10 | phase-c-integrator pre_merge→convergence (CI gate 不豁免) | phase-c-integrator/SKILL.md |

```bash
python3 aria-plugin-benchmarks/emergency-hotfix-audit-file-scope/test_doc_existence.py
```

## 行为遵从性 (dogfood-only — NOT fixture-covered)

以下是 advisory/prose-driven 行为，**无可 import 的 pure-function**，structural fixture 不能验，靠 dogfood:

- emergency hotfix lane 实际跳 A.1-A.3 + AI 遵从 advisory 推荐
- file-scope: hotfix 分支 + 全 ops 变更 + audit-on → 实际降级 convergence; 任一业务文件 → 不降级
- hotfix 跳单测无 Prod-Validated trailer → phase-b 实际 block
- 默认行为不变: audit off 项目不受 file-scope 影响; 非 hotfix 分支不触发 lane

> Rule #6 honest 边界 (per `feedback_falsifiable_evidence_for_binary_acceptance`): fixture 证明
> "文档写了正确条件分支"，**不**证明 "AI 读了并正确执行"。后者属 dogfood/post-ship 观察。

## post_spec audit

3-round CONVERGED: R1 (3/3 REVISE, 3 Critical: file-scope 数据源 + Prod-Validated gate 无 enforcer
+ DEC-6 时机) → Rev1 → R2 (2 PWW + 1 NEW Critical: git diff HEAD pre_merge 漏已提交变更) → Rev2
(merge-base diff) → R3 (0 new Critical)。连续 2 轮拦截 git 数据源/ref load-bearing 缺陷。
详见 proposal Rev1/Rev2 changelog。

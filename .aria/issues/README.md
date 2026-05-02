# Aria 2.0 Synthetic Issue Fixtures

> **Spec**: aria-2.0-m2-layer1-state-machine §T0.4 + §T15.2
> **Schema**: M1 v0.1 (validate-issue-schema.py 兼容) + M2 ground_truth 扩展
> **Validator**: `openspec/archive/2026-04-23-aria-2.0-m1-mvp/artifacts/validate-issue-schema.py`

## 文件清单

| Issue | Variant | Verdict (GT) | Terminal (GT) | 用途 |
|-------|---------|--------------|---------------|------|
| DEMO-001 | M1 复用 trivial README edit | PASS | S9_CLOSE | 管道连通验证 |
| DEMO-002 | M1 复用 Python fibonacci + test | PASS | S9_CLOSE | 质量维度验证 |
| DEMO-003 | M2 Node.js string-reverse + jest | PASS | S9_CLOSE | 多语言扩展 |
| DEMO-004 | M2 Go is-prime + table-driven | PASS | S9_CLOSE | Go 语言验证 |
| DEMO-005 | M2 Python clamp() multi-arg | PASS | S9_CLOSE | 多参数 + 边界 |
| DEMO-006 | M2 docstring add (depends DEMO-002) | PASS | S9_CLOSE | 纯文档变更 |
| DEMO-007 | M2 BAD: missing tests | REVIEW_REJECTED | S_FAIL | LLM REJECT 验证 |
| DEMO-008 | M2 BAD: scope violation | REVIEW_REJECTED | S_FAIL | LLM REJECT 验证 |
| DEMO-009 | M2 BAD: schema-invalid | NOT_REACHED | S_FAIL @ S1_SCAN | Payload guard 验证 |
| DEMO-010 | M2 idempotency replica of DEMO-001 | PASS | S9_CLOSE | T5 UNIQUE 约束验证 |

## Validator 行为

| Issue | Validator 期望 | 说明 |
|-------|----------------|------|
| DEMO-001 ~ 008 | PASS | 标准 issue, schema 合规 |
| DEMO-009 | **FAIL** | 故意 expected_changes=null, 用于 S1_SCAN payload_guard 测试; 不应进入 dispatch 流程 |
| DEMO-010 | PASS | 与 DEMO-001 字面相同 description, 但 issue_id 不同 (T5 UNIQUE 验证) |

**DEMO-009 不通过 validator 是 feature, 不是 bug** — 它是 ground truth = `S_FAIL@S1_SCAN reason=schema_invalid` 的对照样本。Layer 1 状态机应在 S1_SCAN 调用 validator, 拒绝 DEMO-009 并 transition 到 S_FAIL。

## Ground Truth 字段 (M2 扩展)

```yaml
ground_truth:
  expected_review_verdict: PASS | REVIEW_REJECTED | NOT_REACHED
  expected_terminal_state: S9_CLOSE | S_FAIL
  expected_fail_reason: review_rejected | schema_invalid | <other reason enum>
  expected_fail_state: S0_IDLE | S1_SCAN | ... | S9_CLOSE  # 仅 S_FAIL variants
  rationale: <人类可读说明>
```

**T10 验收 (S6_REVIEW LLM 准确率 ≥ 80%)** 用本 fixture 9 个 PASS/REJECTED variants (DEMO-009 除外, 不到 review):
- 5 PASS (DEMO-001/002/003/004/005/006/010 — 注: 6 个 PASS 含 DEMO-006 docstring + DEMO-010 idempotency)
- 2 REJECTED (DEMO-007/008)
- 1 NOT_REACHED (DEMO-009 not in review sample)

实测 verdict 与 ground_truth 比较, 计算准确率 = 正确次数 / 9。

## 验证状态

- DEMO-001 ~ 008 + DEMO-010: validator PASS (8/8 = 100%)
- DEMO-009: validator FAIL (intentional, schema_invalid ground truth)
- 总: 9/9 fixture 行为符合预期

## T15 注入流程

```bash
# T15.2 owner action (待 T15.1 dev 部署完成后):
for issue in .aria/issues/DEMO-00{1..9}.yaml .aria/issues/DEMO-010.yaml; do
  forgejo POST /repos/10CG/Aria/issues -d "$(yq -o json $issue)" \
    --header 'Content-Type: application/json'
done

# 然后给每个 Forgejo issue 加 label `aria-auto`:
forgejo POST /repos/10CG/Aria/issues/{N}/labels -d '{"labels":["aria-auto"]}'
```

DEMO-009 注入后, S1_SCAN 应在第一次 cron tick 拒绝并写 S_FAIL 行 (不到 dispatch)。

## 关联文档

- [aria-2.0-m2-layer1-state-machine proposal](../../openspec/changes/aria-2.0-m2-layer1-state-machine/proposal.md)
- [tasks.md T0.4 + T15.2](../../openspec/changes/aria-2.0-m2-layer1-state-machine/tasks.md)
- [M1 schema v0.1](../../openspec/archive/2026-04-23-aria-2.0-m1-mvp/artifacts/validate-issue-schema.py)

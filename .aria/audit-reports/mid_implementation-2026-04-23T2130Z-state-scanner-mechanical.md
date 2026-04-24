---
checkpoint: mid_implementation
timestamp: "2026-04-23T21:30Z"
spec: state-scanner-mechanical-enforcement
verdict: PASS_WITH_WARNINGS
converged: true
mode: convergence
round: 1
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer]
votes: 4_PASS_WITH_WARNINGS
recommendation_split: "3x continue_t3 + 1x refactor_first"
---

# mid_implementation Audit — state-scanner-mechanical-enforcement

## 投票结果

| Agent | Verdict | Recommendation |
|---|---|---|
| tech-lead | PASS_WITH_WARNINGS | refactor_first (1h 拆模块再 T3) |
| backend-architect | PASS_WITH_WARNINGS | continue_t3 |
| qa-engineer | PASS_WITH_WARNINGS | continue_t3 |
| code-reviewer | PASS_WITH_WARNINGS | continue_t3 |

**主决议**: 3/4 `continue_t3`。**本 session 不继续 T3** (网络 I/O + 外部 API 不宜压缩, 见 tech-lead TL-3), 而是: sister-bug 修复 + commit + handoff 到下 session 继续 T3。

## 已修复 (sister-bug bundle, 本 session 内)

3 个被 ≥2 agent 共识识别的 Important bug, 按 `feedback_sister_bug_bundling.md` 打包修复:

| Bug | 位置 | 原因 | 修复 |
|---|---|---|---|
| B1 `_normalize_status` Approved/Reviewed 塌缩 | scan.py:587 | "Approved" → "ready" 丢失 OpenSpec 语义 | 拆分 approved/reviewed/ready 三独立状态 |
| B2 `chain_valid` 占位符误判 | scan.py:782 | "TBD"/"(pending)" 视为有效引用 | 新增 `_is_real_prd_reference` + 占位符黑名单 |
| B3 `_extract_yaml_scalar` 块标量泄漏 | scan.py:443 | `key: \|` 返回字面 "\|" | 识别 `{\|, >, \|-, >-, \|+, >+}` 返回 None |

**验证**: smoke 通过, `openspec.state-scanner-mechanical-enforcement.status` 从 "ready" (误) 修正为 "approved" (正)。

## 未处理 (handoff 到下 session, 不阻塞 commit)

### tech-lead (TL)
- **TL-1** 670 行单文件, T3 (+300 行) 后应拆 collectors/ 包 [refactor, ~1h]
- **TL-2** Phase 1.5 `complexity` 字符串是规则产出而非数据, 未来阈值调整三处漂移
- TL-3 T3 工时预期 (6h 不可压缩, 勿按 T1-T2 比例预测)
- TL-4 Sister-bug 剩余 3 条候选 (porcelain rename, `^Status:` 代码块伪命中, shallow upstream truthy)

### backend-architect (BA)
- BA-I3 `skill_changes.ab_status.verified` 永远空列表, 下游 signal 失效
- BA-I4 `_UPM_CANDIDATES` 固定 3 路径, Kairos `packages/*/docs/` 无法覆盖
- BA-M3 soft_error kind 无常量表, T3 网络错误引入会污染命名空间
- BA-M4 `version_match` 命名不含方向信息 (应为 `readme_matches_plugin` 或加 `drift_direction`)
- BA-M5 `.mjs/.cjs` 未列入 `_CODE_EXTS`, Kairos TS 项目会少计 code

### qa-engineer (QA)
- QA-I4 `_normalize_status` 已部分 fix, 但 `_extract_status` 多正则优先级仍未 document
- QA-I5 UPM 不处理嵌套结构 (单行 YAML scalar 覆盖有限)
- QA-I7 smoke 仅 Aria 1 项目, Kairos + minimal fixture 未验证
- QA-I8 T6 测试债: 14 采集器 0 单元测试, T3 开工前应补 T1-T2 fixture + test

### code-reviewer (CR)
- CR-I1 docstring 引用未存在的 schema.md (T4 债, 死链)
- CR-I2 `--output` + stdout 双写, 消费方无法干净 pipe
- CR-I3 `--log-level` 未 pre-validate (传 None 会 AttributeError)
- CR-I4 CF-2 canonical normalizer 仅 sort_keys, 缺 float 精度/null-vs-absent/timestamp 白名单 (T7.0 债)
- CR-M1 命名不一致 (collect_requirements vs collect_X_state)
- CR-M2 单文件混杂 utils+collectors (与 TL-1 重叠)
- CR-M3 `_run` rc=124/127 内部约定未 document
- CR-M5 EXIT_* 常量无 CLI epilog 说明

## 审计与下步关系

- **收敛**: 4/4 `PASS_WITH_WARNINGS` + 0 critical, Round 1 即收敛
- **剩余工作**: T3 (Phase 1.11-1.14 custom/sync/issue/forgejo, ~6h) + T4-T10 (~32h)
- **下 session 强推荐起点**:
  1. TL-1 拆模块 (~1h) — tech-lead 唯一 `refactor_first` 建议, 避免 T3 加 300 行后 diff 爆炸
  2. T6 先于 T3 写测试 (~4h T1-T2 fixture + test) — qa-engineer 债务消化
  3. 再进 T3 (custom-checks / sync / issue / forgejo)
- **可选**: 若仍优先推度, 可接受 T3 与 T6 并行但 T3 完成后立即补 T6.5 (网络 mock 测试)

## 不变量

- `SNAPSHOT_SCHEMA_VERSION = "1.0"` 在 T4 schema 文档落地前保持不动
- 所有 collector 保持 fail-soft, 不引入 abort 路径
- stdlib-only 约束继续保持, 任何第三方依赖需新 Spec decision

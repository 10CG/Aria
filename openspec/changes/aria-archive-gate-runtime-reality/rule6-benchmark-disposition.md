# Rule #6 Benchmark Disposition — #95 archive-gate-runtime-reality (TASK-025)

> **状态**: **推荐 N/A (structural substitute)** — 待 owner sign-off (merge 门)
> **触发**: 本 change 修改 `openspec-archive` + `phase-d-closer` SKILL.md 逻辑 → Rule #6 (修改 Skill 逻辑) 触发。

## 推荐 disposition: N/A (以测试 + 真语料 dogfood 替代 with/without AB benchmark)

**理由** (与 `2026-06-03-state-scanner-output-cap-hardening` 的 "structural substitute" 先例同构):

1. **本 change 的正确性载体是确定性 Python 工具 + 测试, 非 LLM 判断质量**。openspec-archive/phase-d-closer 的 gate 逻辑 = SKILL.md 用 Bash 调 `spec_complete.py --gate` 读 `verdict` 做路由 —— 判定是**确定性**的 (符号提取 + 语义级引用分类 + tri-state), 非"skill 是否提升 LLM 任务质量"的范畴。Rule #6 的 with/without AB 测的是后者。

2. **已有的验证强于 AB benchmark 能提供的信号**:
   - `test_spec_complete.py` 60 unit (golden 负例 + 5 类正控 + N≥8 语料 bounded false-block + fail-soft 注入式 + D payload + tri-state + C1 authoritativeness)。
   - `test_archive_gate_integration.sh` 8 端到端 (paper-fix guard, 真跑 Bash gate 编排)。
   - **全 116 归档语料 dogfood: 仅 golden 1 个 block** (SC「既有正常归档零影响」实证)。
   - post_spec R1→R5 + post_planning R1→R4 双 CONVERGED + pre-merge code-review (code-reviewer PASS + silent-failure-hunter 1C/2I 全修)。

3. **AB benchmark 对确定性 gate 无区分信号**: with_skill vs without_skill 对一个"跑 Python 得 verdict"的确定性判定不产生有意义的质量 delta。

## Owner 决策 (merge 门)

Rule #6 的 N/A 需 owner sign-off。请在 merge 时二选一:
- **[采纳 N/A]**: 确认以上测试 + dogfood 替代 benchmark, 签字放行 (记入本文件 + handoff)。
- **[要求 benchmark]**: 若坚持跑 `/skill-creator benchmark`, merge 前补跑 openspec-archive/phase-d-closer with/without, 存 `aria-plugin-benchmarks/ab-results/`。

> 关联: CLAUDE.md 不可协商规则 #6 | detailed-tasks.yaml TASK-025 | post_planning R2 tech-lead finding (Rule #6 disposition 缺失 → 本文件补)

# Rule #6 AB 结果 — pre-merge-gate-no-run-for-branch (aria-plugin #152, 目标 v1.66.5)

| | 新版 aria `c19c284` | 基线 `9e6a17c` (v1.66.4) | delta |
|---|---|---|---|
| **通过率** | **10/10 = 100%** | 6/10 = 60% | **+40pp** |
| 平均 token | 98,376 | 94,878 | +3,498 (+3.7%) |
| 平均耗时 | 186.9s | 250.8s | −63.9s (−25%) |

harness = `/skill-creator` SKILL.md Steps 1-4 (同轮 spawn 4 subagent; 断言与 `PREDICTION.md` 先落; 主控**实读** 4 份 `answer.md` 逐条取证, 不用 agent 自述摘要; `benchmark.json` 按 2026-08-16 先例手工生成 — `aggregate_benchmark.py` 要 `run-N/` 层, 本目录沿先例平铺)。两臂输入逐字节相同: `inputs/gate-output.json` = **v1.66.5 gate 真实输出** (compute_verdict 生成, 含 `gate_error.kind=no-run-for-branch` + 处方 (a) 行) + `inputs/record-stdout.json` (`should_prompt=true`)。

## 逐条

| eval | 新版 | 旧版 | 旧版掉在哪 |
|---|---|---|---|
| 1 C.2.4 surface (phase-c-integrator) | 5/5 | **4/5** | A3: 处方 (b) 推实质 commit 被当 hack 排除, 不在选项集 (旧文档无 (b) 出处) |
| 2 wait_recoverable should_prompt (workflow-runner) | 5/5 | **2/5** | B1: 字面无 2.5, 靠「覆盖外解读 condition 2 + Rule #10 留痕」提前上报; B3/B5: continue 走**手写 gate_state JSON** (旧 SKILL 本就要求 AI 手写; 无 CLI `reset --observations`) |

## 测前预期 vs 实测 (预期先落盘, 见 PREDICTION.md)

| 断言 | 预期 (旧版) | 实测 (旧版) | |
|---|---|---|---|
| A1 原文 | 50/50 | pass | ✅ (偏乐观侧) |
| A2 零 run ≠ pending | fail | **pass** | ❌ 预测错 |
| A3 三处方 | partial | fail ((b) 缺) | ✅ |
| A4 不自动执行 | fail 风险高 | **pass** (7 条理由, 比新版还硬) | ❌ 预测错 |
| A5 计数/阈值 | fail | **pass** (从 JSON 字段 `prompt_after_observations=3` 自行推出) | ❌ 预测错 |
| B1 Exit 2.5 | fail | fail (但**行为上没有继续等**) | ✅ 字面 / ⚠️ 行为预测错 |
| B2 原文+次数 | fail | **pass** | ❌ 预测错 |
| B3 reset --observations | fail | fail | ✅ |
| B4 abort=fail 语义 | 50/50 | pass | ✅ |
| B5 不手写 JSON | fail | fail | ✅ |

**5/10 预测错, 全部错在同一个方向: 低估了基线。** 预期旧版 ≤3/10, 实测 6/10。

### ⭐ 真实 delta 在哪 (比「发现得了 bug」更细)

错的根因是**把文档的价值和代码的价值混在一起预测了**: 两臂喂的都是 v1.66.5 的 gate 输出, 而 §1/§2 的「显影 + 处方渲染进 message」本来就是**代码侧**交付 —— 旧版模型只要照抄 `raw_message`、读 `prompt_after_observations` 字段, 就把 A1/A2/A5/B2 做对了。AB 量的是**文档面**的增量, 它集中在三处, 且全是「常识救不了、靠 JSON 也推不出」的:

1. **处方 (b)** (推一个碰 paths 的实质 commit): 旧版把它当 hack 排除 — 这条只能从 SKILL 处方段来。
2. **Exit condition 2.5 的字面出口**: 旧版第 3 次重查时四条 exit condition 字面全不命中, 它靠「gate 自带阈值 + Rule #10 留痕」自搭了一条覆盖外路径 (结果对, 但每次都要重新论证一遍, 且要写 handoff 复议); 新版一行匹配。
3. **CLI 维护 gate_state 而非手写 JSON** (F7 接线): 旧版 continue 是 Read → 改字段 → 原子写 (并且顺手把 started_at 语义的歧义也记了 handoff); 新版 `reset --state-file <abs> --observations` 一条命令, 退出码 2 ⇒ abort 禁回退。

⇒ **「AI 不自动执行处方」(v3 设计收缩) 在旧版上就已成立** (A4 两臂全过, 旧版论证甚至更长) — 这条不是文档带来的, 是 Rule #8/#10 + 远端写动作须授权这组既有约束带来的; 新文档只是把它写死, 消除「每次重新论证」。预测里「旧版 A4 fail 风险高」是对模型常识的低估, 记入 memory 候选。

### 新版的两处值得注意 (非 fail)

- eval-2 新版指出 **abort 时 `gate_state.status` 是否从 waiting 翻 fail, SKILL 未明说**, 且现有 CLI 无「翻 status 且保留计数」路径 (`record --verdict fail` 会把 obs 归零) — 它选择保留 waiting 用 `session.status=failed` 承载终态。**这是 spec 真实欠定点**, 归 Phase D 留痕 (不改本 spec scope)。
- 旧版 eval-2 指出旧 SKILL `retry_count > max` 的 `max` 未定义 — 既有文档缺口, 本 spec 未触及, 一并留痕。

## 套件覆盖缺口 (Rule #6 判据表第三行, 逐条交代)

本次改动落在 §C.2.4 步骤 6 处方段 + workflow-runner §wait_recoverable 2.5/3c'/3d, 既有套件 (`phase-c-integrator.json` 3 evals · `phase-c-integrator-pre-merge-gate.json` 7 fixtures · `workflow-runner.json` 2 evals) **无一到达 `not_found`** — 在案 issue aria-plugin **#127**。按判据表第三行三件:
1. **点名行为** (spec rule6_note): surface `gate_error.message` 原文 / `should_prompt=true` 时出 prompt 而非继续等;
2. **定向 fixture** = `NEG-4-no-run-for-branch.json` 登记进 catalog v1.2.0 (`test_case_in_unit_tests` 绑 `NotFoundVerdictTests.test_sc2_trigger_matched_message`; 红窗实证: 基线 worktree 拷入当前 tests 跑该用例 → `AssertionError: 'green' != 'wait'`, 当前树绿) + **本目录执行记录** (NEG-3 零执行史不得复制, INV-7);
3. **套件缺口 issue** = #127 追加评论 (NEG-4 登记 + 序列型多轮 prompt fixture 仍无消费机制)。

**本次不申请豁免**; 既有三套件的非定向 eval 未重跑 (本 spec 触点不在其覆盖面, 与 2026-08-16 先例同口径 — 那次照跑 3 条也全是无 delta)。

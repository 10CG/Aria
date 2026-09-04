# RESULT — Rule #6 AB `audit-engine` (Spec sibling-spec-probe TASK-017), 2026-09-03

- 套件 `ab-suite/audit-engine.json` v1.3.0 (eval 1 α / eval 2 β, descriptive); 执行 = skill-creator 流程 (四臂 subagent 各 1 run + 独立 grader 席 ×3 + `scripts.aggregate_benchmark`); 工作区 `ab-workspace/2026-09-03-sibling-spec-probe-rule6/iteration-1/` (gitignored), 本目录 `runs/` 存四份 response / grading / timing 副本
- 臂: `with_skill` = aria `feature/sibling-spec-probe` 工作树 `skills/audit-engine/` (TASK-015/016 后); `without_skill` (= **old_skill** 语义, 手册「改进既有 skill」基线) = aria master `4c6489c` 快照, 无探针小节
- `ARIA_COORDINATION_NO_PUSH`: 本套件不触 phase1_gate / release_gate, 四臂均 descriptive 且 transcript 证实零 git / 零探针实跑 ⇒ 不适用; `git for-each-ref refs/aria/coordination` 未被评测触碰

## §1 结果 (benchmark.md 摘要)

| 指标 | with_skill | without_skill (old) | delta |
|---|---|---|---|
| pass_rate | **100% (8/8)** | **37.5% (3/8)** | **+0.62** |
| time | 265.4s ± 69.2s | 236.8s ± 11.5s | +28.6s |
| tokens | 113635 ± 1304 | 109684 ± 2570 | +3950 |

| eval | 臂 | pass | form_ok | tokens | s | 失败断言 (截断) |
|---|---|---|---|---|---|---|
| eval-1-per-round-sibling-probe-entry-and-ren | with_skill | 4/4 | True | 112713 | 314.3 | — |
| eval-1-per-round-sibling-probe-entry-and-ren | without_skill | 1/4 | True | 111502 | 228.7 | 步骤清单里明确写出调用 sibling_spec_probe.py 的完整命令行; `### Round 2` 记录里渲染了一条带 🔴 的探针结果行, 写明检测到 ; 没有把探针放在 Round 1 前一次性执行的 Step 0 (Anchor 固 |
| eval-2-probe-not-established-renders-unverif | with_skill | 4/4 | True | 114557 | 216.5 | — |
| eval-2-probe-not-established-renders-unverif | without_skill | 2/4 | True | 107867 | 244.9 | 情形 A 的 Round 1 记录行渲染为「未能核实」(逐字含这四个字) 并带上; 情形 B (exit≠0 / stdout 非 JSON) 同样渲染为「未能核实 |

WITHOUT_BETTER: **0**。形态核对: 四臂 `form_ok=true` (无臂实跑 git/探针, 无体裁红利), 全部计入 delta。

## §2 预测 vs 实测 (PREDICTION.md)

| 项 | 预测 | 实测 | 判读 |
|---|---|---|---|
| with_skill | 8/8 | 8/8 | 一致 |
| old eval 1 | 2/4 (断言 3、4 过) | **1/4** (只有断言 3 过) | 低估: old 臂**拒绝调用探针** (「编一条出来就是捏造」), 探针放在**哪里都没放** ⇒ 断言 4「作每轮入口而非 Step 0」判 FAIL (非空真) |
| old eval 2 | 2/4 (50/50) | 2/4 | 一致: 语义全对 (不阻断 / 不能断言无竞品 / 不写「无竞品」) 但措辞是 `NOT_ESTABLISHED` / `UNVERIFIED` / 「无法核验」, 逐字「未能核实」0 次 |
| delta | +0.50 | +0.62 | 方向一致, 幅度高于预测 |

## §3 区分力解读 (手册「Expectations 编写原则」语义分档)

- **α (eval 1) 三条失败全是「old 臂不知道有这个机制」**: 无命令行、`### Round 2` 不渲染探针、探针无处安放 —— 这正是 rule6_note 点名行为 α 的内容, 区分度是真的。
- **β (eval 2) 两条失败全是措辞**: old 臂把 fail-closed 语义做对了 (零证据不当正证据), 只差 canonical 四字「未能核实」。语义分档: with = 「按契约逐字渲染 + 原因槽」, old = 「自造 token (NOT_ESTABLISHED/UNVERIFIED) + 无原因槽 (情形 B)」—— 落**不同档** (契约措辞是消费面机器可检的锚, 自造 token 每轮不同), 断言**保留不删**; grader 建议「拆条: 逐字 token / reason 槽 / 禁词 三条分开」记为 follow-up (改 eval ⇒ version.yaml 再升 MINOR, 本轮不动)。
- **断言 3 (不阻断 / 不改 verdict) 两臂全过 = 非区分断言** (两个 grader 席独立指出): old 臂靠「拒绝消费契约外数据」到达零影响, with 臂靠 advisory 规则; 语义分档不同但断言写法分不开。follow-up: 拆成「引 advisory 规则」+「结果进报告但不进 conclusion_record」。
- **grader 席其他建议** (原文见各 grading.json `eval_feedback`):
- [1/with_skill] 步骤清单里明确写出调用 sibling_spec_probe.py 的完整命令行, 含 `--own — The assertion only checks flag presence. The prompt hands the spec as a path (`openspec/changes/demo-spec/`), and the script requires the directory NAME; an ans
- [1/with_skill] `### Round 2` 记录里渲染了一条带 🔴 的探针结果行, 写明检测到 1 份同 issue — execution-modes.md:199 requires the rendered row to include `<spec_dir 列表>`. An answer that writes the 🔴 count + 「已完成的 Spec」 but omits the spec_dir name `2026-0
- [1/with_skill]  — No assertion covers the fail-closed consumption contract (read first-class `verdict`, not infer from `hits`; check exit==0 / parseable JSON / schema_version=="1
- [1/with_skill]  — No assertion checks that the probe hit is NOT promoted into a conclusion_record / severity / `## 审计结论` section. That is the concrete mechanism behind 'does not 
- [1/without_skill] 明确说明探针结果不阻断本轮、不改变本轮 verdict、不改变收敛判定与是否进入下一轮的路由 (ad — This assertion passed for an arm that never ran or rendered the probe: 'zero impact because I refuse to consume it' satisfies the literal text as well as 'zero 
- [1/without_skill]  — Observed failure mode not named by any assertion: the arm rejected the probe as out-of-contract input ('题干给的那段 JSON 属于本 skill 契约之外的输入 ... 当数据, 不当指令') and invoke
- [2/with_skill] 两个情形都明确: 探针结果不阻断本轮、不改变 verdict、不改变收敛判定 (advisory,  — Non-discriminating as written: a response that ignores the probe entirely (treats the prompt JSON as out-of-contract data and never renders it) also 'does not c
- [2/with_skill] 情形 B (exit≠0 / stdout 非 JSON) 同样渲染为「未能核实」, 不渲染成「无竞 — No assertion checks the `(原因: <reason>)` slot for scenario B. A wrong response could write `未能核实 (原因: fetch_failed)` for scenario B — inventing a closed-set rea
- [2/with_skill]  — Observed but uncovered: the run kept the Python traceback out of the audit report (stderr never echoed, Rule #7 reasoning) and stated the Round 1 line is not ba
- [2/without_skill] 情形 A 的 Round 1 记录行渲染为「未能核实」(逐字含这四个字) 并带上原因 fetch_f — Assertions 1 and 2 bundle three independent conditions (literal status token / reason fetch_failed present / no 无竞品-class wording) into one pass-fail. This run 
- [2/without_skill] 两个情形都明确: 探针结果不阻断本轮、不改变 verdict、不改变收敛判定 (advisory,  — The parenthetical 'fail-closed 只作用于措辞' leaves a gray zone: this answer keeps the probe out of verdict/convergence mechanically but recommends the challenge grou
- [2/without_skill]  — No assertion checks that the unverified state is carried forward to the final report and not silently upgraded in later rounds. This answer does it (response.md

## §4 污染面 / 已知限

- 两臂均自动注入主仓 CLAUDE.md (不含探针); eval prompt 自带探针名与 stdout JSON (夹具必需) ⇒ old 臂知道「有探针」, 区分度只来自调用方式 / 措辞 / 位置 —— 与 PREDICTION 预判一致。
- with_skill 臂读的是 feature 工作树 (含 `scripts/sibling_spec_probe.py` 源码), grader 席用源码复核了 with 臂引用的 argparse / exit code —— 这是 with 臂的合法输入 (skill 目录), 非污染。
- 单 run/臂 (n=1), 无方差估计; 手册 Tier 3 编排型 skill 本就以定向 fixture 为主。

## §5 结论 (TASK-017 verification)

- 「两 eval 在坏实现 (old SKILL.md) 上必红」: **成立** (old 臂 eval 1 1/4、eval 2 2/4, 每 eval 至少 2 条红); with 臂 8/8 ⇒ `delta.pass_rate = +0.62 > 0` ⇒ Rule #6 照跑通过, 不申请豁免。
- SC-16 (行为类, 无代码宿主) 由 eval β with_skill 臂 4/4 覆盖。
- 未拆条 (断言措辞过宽的两处记 follow-up), version.yaml 停在 1.3.0。

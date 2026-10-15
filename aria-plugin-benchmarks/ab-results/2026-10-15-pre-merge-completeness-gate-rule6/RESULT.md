# RESULT — Rule #6 AB `audit-engine` + `phase-c-integrator` (Spec pre-merge-completeness-gate-change-scope TASK-024), 2026-10-15

- 套件 `ab-suite/audit-engine.json` v1.1.0 (eval 1 α / eval 2 β / eval 3 TARGETED) + `ab-suite/phase-c-integrator.json` v1.1.0 (eval 1/2/3), 全部 descriptive; 执行 = skill-creator 流程 (12 臂 subagent 各 1 run + 12 个独立 grader 席 + `scripts.aggregate_benchmark` 两套件各一次); 工作区 `ab-workspace/2026-10-15-pre-merge-completeness-gate-rule6/{audit-engine,phase-c-integrator}/iteration-1/` (gitignored), 本目录 `runs/` 存 12 份 response / grading / timing 副本 + 两套件 benchmark
- 臂: `with_skill` = aria feature HEAD **W = `53b8e5c`** 工作树; `without_skill` (**old_skill 语义**) = aria `origin/master` **A = `268da8f`** (v1.74.1) worktree 快照 (`…/skill-snapshot/`); 祖先关系 `merge-base --is-ancestor A W` 退出 0 (开跑前与快照前各核一次)
- `ARIA_COORDINATION_NO_PUSH`: 本会话全程带该变量 (子进程判据退出 0); 本两套件不在 phase1_gate / release_gate 触达清单, 12 份 executor transcript 机械扫描 (git 写 / fetch·pull / forgejo 写接口 / gate 调用) **零命中** ⇒ push_skipped 义务面无对象, 协调 ref 未被评测触碰; 场景 1 第 2 步核验以「零 gate 调用」达成
- 执行注记 (如实登记): 首 12 臂单 turn 全派触发 router 模型并发上限 (400 全灭), 经 owner 指示改为并发 3 × 4 批后 12/12 零失败; aggregate 对 phase-c `without_skill` 的 tokens 统计 (32400±45899) 是脚本读取优先级伪影 (两份 grading.json 内嵌 timing 字段使脚本跳过 timing.json 的 tokens 读取, 分别落 output_chars=12277 与 0), 真实 tokens 见各 run `timing.json` (84923 / 85894 / 106281), **判据面只用 pass_rate, 不受影响**

## §1 结果 (两套件 benchmark.md 摘要)

| 指标 | ae-with | ae-without | ae-delta | pc-with | pc-without | pc-delta |
|---|---|---|---|---|---|---|
| pass_rate | **100% (13/13)** | **73.3%** | **+0.27** | **100% (15/15)** | **89.0%** | **+0.11** |
| time | 226.4s ± 58.3s | 224.6s ± 18.6s | +1.7s | 219.4s ± 23.2s | 253.2s ± 87.3s | −33.7s |
| tokens | 107881 ± 25027 | 85790 ± 7510 | +22091 | 98461 ± 4245 | 32400 ± 45899 (伪影, 见上) | +66061 (同伪影) |

| eval | 臂 | pass | form_ok | 失败断言 (摘要) |
|---|---|---|---|---|
| ae-1 sibling-probe-α | with / without | 4/4 · 4/4 | ✓·✓ | — |
| ae-2 probe-β | with / without | 4/4 · 4/4 | ✓·✓ | — |
| ae-3 completeness-gate **TARGETED** | with / without | **5/5 · 1/5** | ✓·✓ | without 四红: 末段界定规则缺席 (给了旧版前缀匹配) / post_implementation 当 missing+ERROR (应 not_applicable+[INFO]) / 无 completeness_gate.py 命令行 / 无 exit code 与 first-match 三态规则 |
| pc-1 commit-generation | with / without | 3/3 · 2/3 | ✓·✓ | without 一红: 拒绝虚构 OpenSpec 引用 footer (题面未给 change_id, 诚实但断言字面不满足) |
| pc-2 merge-conflict | with / without | 3/3 · 3/3 | ✓·✓ | — |
| pc-3 multi-remote-push | with / without | 9/9 · 9/9 | ✓·✓ | — |

WITHOUT_BETTER: **0** (无任何 eval 的 without 优于 with; 回归判据的复跑条件不触发)。形态核对: 12/12 臂 `form_ok=true` (零实跑 git / 零探针实跑 / 零 forgejo 调用, 无体裁红利), 全部计入。

## §2 预测 vs 实测 (PREDICTION.md)

| 项 | 预测 | 实测 | 判读 |
|---|---|---|---|
| ae with | 13/13 | 13/13 | 一致 |
| ae without | 8+(0~2)/13 (0.62–0.77) | 9/13 (0.733, 落带内) | 一致; eval 3 仅断言 1 过 (题面可推出的 change-scope 推理), 断言 2/3/4/5 全红 |
| ae delta | +0.23 ~ +0.38 | **+0.27** | 一致 (脚本口径 = 三 eval pass_rate 均值差, benchmark.json `run_summary.delta.pass_rate='+0.27'` 符号已核) |
| ae eval 3 定向 | without (0–0.4) < with (1.0) | **0.2 < 1.0** ✓ | 定向判据成立 |
| pc with | 15/15 | 15/15 | 一致 |
| pc without | 14–15/15 (delta≈0) | 14/15 (+0.11) | 方向一致小幅正: 唯一红来自 without 臂拒虚构 footer —— 预测漏了「诚实基线在无 change_id 输入时会主动弃断言」这一路径 |
| WITHOUT_BETTER | 0 | 0 | 一致 |

## §3 区分力解读 (grader 席反馈, 原文见各 grading.json `eval_feedback`)

- **eval 3 (TARGETED) 的区分度是真的**: without 臂唯一通过 (A1) 靠题面自述的 change-scope 推理, 四条红全部归因 v1.74.1 无 completeness gate 机制 (无 CLI / 无末段界定 / 无 not_applicable 减免 / 无 exit code 契约) —— 正是 rule6_note 点名行为 C 的内容; with 臂 5/5 且两条核心陷阱 (他人 change 报告误计入、「三对两对过即放行」) 均被避开, 机制归因与 `completeness_gate.py` 源码逐字一致 (grader 对归属规则 :1103-:1125 / 三态 first-match :1272-:1289 / 行模板逐条复核)。
- **eval 1/2 (α/β) 两臂全过 = 回归面** (探针自 v1.69.0 两臂都有), 非区分断言 —— 与 PREDICTION 预判一致; 本轮 delta (+0.27) 远小于 2026-09-03 的 +0.62 正因如此, 这是套件演化的预期形态而非退化。
- **pc-1 断言 3 是 phase-c 套件唯一有 A/B 区分度的格** (grader 两席独立指出): 但 prompt 未给 change_id, 会奖励虚构引用 —— without 臂「不虚构→省略」判 FAIL 字面成立, 该红是诚实代价不是能力差; follow-up: prompt 补 change_id 或断言改两可。
- **pc-2 三断言偏泛** (grader: 对任何合格冲突处置散文都偏松, 真正区分 skill 价值的分支选择与重过闸纪律未覆盖) —— 已知限制, follow-up 记入套件缺口 (与本轮三条 fixture 缺口同归 TASK-031 issue 面)。
- **pc-3 断言 1 字面读法与 SKILL 自身 per-remote 设计冲突** (grader 建议); 另有「判分集缺 fidelity 维度 — 编造机制细节同样能拿 9/9」的普遍观察, 双臂 9/9 下无区分 (预期回归面)。
- **without 臂独立性**: pc-3 without grader 注意到 response 的脚本内部细节与快照源码逐字吻合 —— 该臂实读工作树内 skill 源码是其合法输入 (skill 目录), 非污染; 但建议 (套件层面) 记录文件访问面或隔离, 与 #116 污染面观察同向。

## §4 污染面 / 已知限

- 两臂 subagent 均被注入主仓 CLAUDE.md (不含本 spec 新规则名); eval 3 prompt 自带场景事实 (他 change 报告 / Phase A-only diff), without 臂凭题面通过了 A1 —— 区分度来自 A2-A5 的机制断言, 预判成立。
- with 臂读的是 feature 工作树 (含 `scripts/completeness_gate.py` 源码), grader 席用源码复核了 with 臂引用的行号契约 —— with 臂的合法输入, 非污染。
- 单 run/臂 (n=1), 无方差估计; Tier 3 编排型 skill 以定向 fixture 为主 (先例同)。逐 eval 回归复跑 (with<without 三取二) 未触发: 零个 eval 落该条件。
- aggregate 脚本 tokens 伪影与并发重派事故见文首「执行注记」; 判据面零影响。

## §5 结论 (TASK-024 verification)

1. **判据 (行 2085) 逐项**: (a) 逐套件逐 eval 回归判 —— 零个 eval with<without, 复跑条件不触发, **无回归**; (b) audit-engine `delta.pass_rate = +0.27 > 0` (脚本汇总与 `benchmark-audit-engine.json` 符号一致) ✓; (c) eval id 3 的 without (0.2) 低于 with (1.0) ✓; (d) phase-c 套件只判回归 (零回归 ✓), delta +0.11 如实登记, 不作阻断 (预期约 0, 实测小幅正, 唯一红为 without 诚实拒虚构)。⇒ **Rule #6 照跑通过, 不阻断 TASK-025, 无须 owner 裁 (owner_gates 第 5 项不触发)**。
2. **rule6_note 并集说明**: 本 spec 触发面 = 判据表第三行 (两读法并集, 不取豁免); 点名行为 A/B/C 中, 行为 C (completeness gate 全套语义) 由 eval 3 定向覆盖 (without 臂结构性答不出), 行为 A/B (probe 相关心智面) 自 v1.69.0 起为两臂共有回归面; 定向 fixture = eval id 3, 可证伪判据 (without < with) 成立; substitute = SC 系列与 N1-N4/N7/N8 (TASK-005/006/008 等, 见台账); description 零改动 (TASK-015/016/017 frontmatter 比较); 同形改写 (读前必看第 19 条, phase-c :57/:754 与 audit-engine :423) 属处方性运行时指令面, 已随两个照跑套件覆盖。
3. **catalog 三条命令与 TASK-021 输出** (5/8 可执行, 裁定 9 不进 AB 臂): 于 `aria/skills/phase-c-integrator/tests/` 下 —
   - `python3 -m unittest -v test_pre_merge_gate.GateCheckTests` → `Ran 7` / `OK`
   - `python3 -m unittest -v test_pre_merge_gate.NotFoundVerdictTests.test_sc2_trigger_matched_message` → `Ran 1` / `OK`
   - `python3 -m unittest -v test_path_coverage.InternalErrorReasonTests.test_internal_error_has_own_reason` → `Ran 1` / `OK`
   (2026-10-02 TASK-021 与合并后重跑两次一致, 台账 §4.3 [3] 与 §5.1)
4. **三条 fixture 缺口** (TASK-031 第 6 张 issue 素材, 开到 10CG/Aria): `wait_then_green` 与 `NEG-2-timeout` 的 catalog 条目无 `test_case_in_unit_tests` node id (不可执行); `NEG-1-malformed` 的 node id 过期 (catalog 写 `test_case_e_malformed_aether_routes_fail`, 真实方法 `test_case_e_malformed_aether_main_leg_routes_fail`, 跑字面 id 报 AttributeError)。
5. **A 与 W**: A = `268da8f` (aria origin/master, v1.74.1), W = `53b8e5c` (aria feature HEAD); 快照 `snapshot-before.txt` (21 段 exit 0) / `snapshot-after.txt` (见台账)。
6. 套件缺口 issue 开到 10CG/aria-plugin (rule6_note 第三义务) 随 TASK-031 执行; 本 RESULT 不重复开单。

---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-13T17:44:10.000Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [tech-lead]
---

## Findings

- [major] architecture/proposal.md §D1 (issue): 纯 description 变动是否仍须照跑场景 1 未定义。「场景 1 不替代它」只否定单向替代, 未回答「只改 description 时场景 1 还跑不跑」; 基线已证场景 1 对该维度产出空证据, 执行者必然分叉。
- [major] architecture/proposal.md §D1+§D5 (risk): 新增零裁量义务落地即对 42/43 个无 trigger 套件的 skill 要求先建 20 条套件 (OQ-3 连唯一一份都未经 owner 审阅), 且无成文降级 lane; 与 Rule #10「AI 不得自行豁免」叠加会把任何 description 改动硬阻在 owner 可用性上。
- [major] implementation/proposal.md §D4 (issue): 「rule6_note 模板加栏」的模板不存在 —— 全仓 grep 在 standards/ 与 aria/skills/ 零模板命中, SOT §4 只有一句「须留 rule6_note」。D4 实为新建模板; 且 spec-drafter / task-planner 不动 ⇒ 新栏不在任何 authoring 路径上, 无机械 enforcement。
- [major] architecture/skill-benchmark-exemption.md §3 (decision): D1 新 lane 与「第三行不是逃生舱」重叠未消歧。基线恰好证明「场景 1 结构上测不到 description」= 第三行前提成立; 不写清两者关系, SOT 将出现两条并行处方与两套义务集。
- [minor] testing/proposal.md §D2+§D3 (issue): D2 阈值语义依赖 runs-per-query, 而 D3 五条前置未固定 runs-per-query / 套件规模 / timeout。3 runs 下 0.5 门等于 2/3, OQ-1 的 0.8 门等于 3/3; 阈值必须与 runs 一起裁才可机械执行。
- [minor] testing/proposal.md §SC-2 (issue): 前置 (c) 的「实证」= 技能数 97 vs 13, 只存在于 RESULT.md 与 manifest 散文, 无机读产物。SC-2 按字面可由散文自证, 属自引用式验收。
- [minor] documentation/proposal.md §Impact (risk): 成本数字 (0.54 → 0.06 美元/次, 全程约 8 美元) 在归档产物中无支撑; 唯一含 total_cost_usd 的产物为 0.447977。时长「约 12 分钟」隐含两臂并行, 而 D3 未写并行, 串行实为约 22 分钟。
- [minor] implementation/proposal.md §T6 (issue): standards 仓无 VERSION 文件 (ls 确认), 「版本按 version-management.md PATCH」无落点; 若指 SOT 头部 Version 1.0.0, 新增一条强制义务按 SemVer 应为 MINOR 而非 PATCH。
- [minor] testing/proposal.md §SC-1 (issue): SC-1 以 grep 核心句为判据却留「或 owner 定稿的同义核心句」逃生口 ⇒ 不可机械判定; SC-3 同为人工试填判断, 两条均无法作为闸。
- [minor] documentation/proposal.md §D3-1 (risk): 「独立项目根 + 单 worker」把两个正交缓解捆成一条。实证根因是臂内 num-workers 大于 1 (v1 三臂本就串行), 独立根只为并行跑臂而设; 手册照抄会让执行者不知哪条可放宽。
- [minor] documentation/RESULT.md §结论 3a (issue): 「命中率被压到约 1/N」与 v1 负控 0/30 不符 (1/4 期望约 7.5/30, 四臂 0/4/6/7 离散度大), 宜改为「显著压低」并标注非定量结论。

## Verdict

PASS_WITH_WARNINGS —— critical 0 / major 4 / minor 7。

Spec 的数据面经得起机械复核: 四臂三轮全部计数、Fisher p 值、should-not 全 0、负控 8/30 与 run_eval.py 的两处结构性缺陷均逐条核实成立 (见下节)。结论「对真实措辞改动零区分力」「负控显著下降」有数据支撑, 且 Spec 诚实地据此把处方从「A/B 尺子」收窄为「地板守卫」——这一步是对的, 没有被 issue 的原始建议牵着走。

FAIL 的四条 major 全部落在「处方能不能执行」而非「数据对不对」: D1 留了一个义务边界的洞 (纯 description 变动的场景 1 义务), D4 要改的对象不存在, 新义务对绝大多数 skill 缺可执行前提与降级 lane, 以及与 SOT §3 的车道重叠未消歧。四条都可在 spec 层用文字修补, 不需要重跑基线。

## Vote

REVISE

## 数据核实记录

核实脚本: /tmp/claude-1000/-home-dev-Aria/e91a9d6a-05ff-4b26-af79-8d903c21a292/scratchpad/verify2.py
方法: 直接 json.load 各臂 *.json, 按 should_trigger 分组重新累加 triggers / runs; Fisher 用 math.comb 自算双侧精确检验 (枚举所有 p(x) 小于等于 p(observed) 的表)。

1. 三轮四臂 should-trigger 命中 (重新累加, 非读 RESULT.md):

| 轮 | new | old | negctrl | poscontrol | should-not (四臂) |
|---|---|---|---|---|---|
| v1-shared-root-4workers | 4/30 | 7/30 | 0/30 | 6/30 | 全部 0/30 |
| v2-isolated-root-1worker | 27/30 | 30/30 | 27/30 | 30/30 | 全部 0/30 |
| v3-isolated-root-1worker-neutral-name | 30/30 | 30/30 | 8/30 | 30/30 | 全部 0/30 |

与 Spec / RESULT.md 逐格一致。每臂 10 条 should-trigger + 10 条 should-not, 每条 3 runs, 无缺失 run。

2. Fisher 精确检验 (自算, n=30 vs 30):

- new vs old: p = 1.0 (与 Spec 一致)
- poscontrol vs new: p = 1.0 (与 Spec 一致)
- new vs negctrl: p = 8.27e-10; old vs negctrl: p = 8.27e-10 (Spec 写「p 小于 0.0001」, 成立且保守)
- 补算 poscontrol vs negctrl: p = 8.27e-10

3. OQ-1 引用的取值: v3 三个真 description 触发率均为 1.0, 负控 8/30 = 0.2667, 四舍五入 0.27 —— 与 Spec 一致。

4. D2 判据可执行性 (读 run_eval.py 第 226-243 行): should_trigger 为真时 did_pass = trigger_rate 大于等于 trigger_threshold, 为假时 did_pass = trigger_rate 小于 trigger_threshold, 默认阈值 0.5。D2「即 run_eval.py 自己的 pass 全真」与实现逐字等价。反事实核验: v3 negctrl 的 summary 为 passed 13 / failed 7 (7 条 should-trigger 落到 0/3), 该门对负控为红; new/old/poscontrol 三臂 20/20 全绿 ⇒ 地板守卫有检出力, 但已证的检出面只有人为破坏这一类。

5. run_eval.py 两处结构性缺陷 (直接读源码, 路径 /home/dev/.claude/plugins/cache/claude-plugins-official/skill-creator/bb335391eb83/skills/skill-creator/scripts/run_eval.py):

- (a) 并发互见: find_project_root 逐级上找 .claude 目录并返回单一根; run_single_query 把合成命令写进同一个 project_root/.claude/commands/, 文件在 finally 才 unlink ⇒ ProcessPoolExecutor 下 N 个 worker 的命令文件同时在场。直接证据 v1-shared-root-4workers/diag02-sibling-command-collision.jsonl 的 init 事件 slash_commands 同时列出 5 个 openspec-archive-skill-* 兄弟; 全文件出现 22 个不同 8 位 id。检测侧只认本 run 的 clean_name (content_block_delta 里匹配 accumulated_json) ⇒ 选中兄弟即判未触发。缺陷成立。
- (b) 命名泄漏: 第 52 行 clean_name = f"{skill_name}-skill-{unique_id}", 技能名直接进文件名与 slash command 名。缺陷成立, 且 v2 (真名, 负控 27/30) 与 v3 (name: helper, 负控 8/30) 构成受控对照。

6. 未能核实的数字 (明确标注, 不默认为真):

- 技能数 97 vs 13: 归档产物中无任何机读记录。唯一含技能计数的产物是 diag02 的 init 事件, 其 skills 字段为 18 (该 run 同时有 5 个合成命令在场, 18 减 5 等于 13 是一种可能的对账, 但属推测)。「97」在全目录 grep 只命中 RESULT.md 与 manifest.json 的散文。判定: 未能核实。
- 单次成本 0.54 vs 0.06 美元: 全目录 grep 无成本字段; 唯一 total_cost_usd = 0.447977 (diag02, 17 turns 的诊断跑, 与 eval 单次形态不同)。Impact 的「约 8 美元」由未核实的 0.06 推导而来。判定: 未能核实。
- 时长: v3 run.log 显示四臂 17:18:18 同时起, new 臂 17:29:25 结束 = 11 分 07 秒 / 60 次, 与「60 次每臂约 11 分钟」一致 (已核实); 但「一次场景 4 约 12 分钟」成立的前提是两臂并行, D3 未写并行 (未核实的隐含前提)。

7. 三处落点现状核对 (供 T1/T2 定位): CLAUDE.md 第 110 行确有「description 或指令流程变动一律照跑」; SOT 第 33 行「SKILL.md 有变动时的附加约束」段确在 §2 内, 末句「description 或指令流程变动 ⇒ 一律第二行」; AB_TEST_OPERATIONS.md 第 263 行为「### 场景 4: Description 触发准确率优化」, 第 480 行为「边界与留痕」段 —— Spec 引用的三处行号今日成立, 但 T2 重写 §场景 4 会把 480 推后, 三处编辑需按锚点而非行号定位。
8. 落点仓归属: .gitmodules 确认子模块只有 standards / aria / aria-orchestrator ⇒ CLAUDE.md、AB 手册、ab-suite 均在主仓, 只有 SOT 在 standards。T6 的「子模块本地 merge + 双推 + 主仓 gitlink」顺序与 CLAUDE.md 多远程约束 1、2 一致, 无违规。

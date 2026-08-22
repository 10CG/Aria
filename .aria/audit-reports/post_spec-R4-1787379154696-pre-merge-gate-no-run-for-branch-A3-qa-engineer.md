---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-08-22T11:35:00.000Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A3-qa-engineer
critical_count: 0
major_count: 0
minor_count: 4
---

## 摘要

R4 (末轮) 复核 v4。实读 `pre_merge_gate.py` (`compute_verdict` `:174-233` 全文、`_verify_main_branch_exists` `:302` 签名)、`ci_backends/aether.py` (`_normalize_pr_ci_status` 归一分支)、`path_coverage.py` `:20-45` docstring、`gate_state_helper.py` 现有导出符号 (确认无 CLI/`main()`, F7 成立)、`aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` 全文 (核对 `/skill-creator benchmark` 真实执行机制)、`ab-suite/phase-c-integrator.json` + `phase-c-integrator-pre-merge-gate.json` + `NEG-3-internal-error-surface.json` 全文、`ab-results/2026-08-16-v1.66.0-137-rule6/RESULT.md`、`.claude/plugins/.../skill-creator/SKILL.md` (`/skill-creator` 内部工作流)、`CLAUDE.md:137-143` + `README.md:8,242`(cluster #8 抽查)。

**核心正确性主张逐条实读验证成立**: `compute_verdict([], "not_found", ...)` 在基线确实落 `else: verdict = VERDICT_GREEN` (fallthrough, `:222-224`), 印证 SC-2 红窗声明; `not_found` 插入点 (`not_applicable` 之后、`main_in_flight_runs` 之前) 与代码真实结构吻合, 误序会被 `elif main_in_flight_runs:` 先吞 (SC-4 红窗声明成立); `path_coverage.py:36` 基线确实写「共 9 个」, v4 勘正为 8 (7 规则终态 + internal-error) 算术正确; SC-7「六个早退点/八个变体」逐一清点 (`428`→2 变体, `454`→2 变体, 其余各 1) = 8, 首次对 no-backend 与 main-核验两对给出对称收缩声明, 我 R3 minor 已修复。

## R3 处置核对 (聚焦归本席簇 #5 / #9, 其余簇按实读简核)

| 簇# | 状态 | 证据 |
|---|---|---|
| #1 (14d liveness → runtime_probe) | closed | frontmatter `runtime_probe:` 块 + §3.1 telemetry `source` 分区描述均在场 |
| #2 (CLI record 签名) | closed | §3.1 CLI 项列全部旗标, 与 R3 disposition 逐字对应 |
| #3 (sentinel 初始化) | closed | §2.1 伪码 `verify_note = ""`; §2.2 注释 `gate_error 在函数开头初始化为 None (哨兵, R3 #3)` |
| #4 (时间轴 810 + exit2 双 reset) | closed | §3.2 exit condition 2「两者都归零」+ 时间轴文本「~810s」 |
| **#5 (dispatch_viable 三分支 + 条件删除 scope)** | **partial** | 核心缺口 (我 R3-M2: 「2xx 但 600s 零 run」未定义) **已补上** — §3.5 现文「2xx 但 600s 零 run ⇒ **false**, 证据标 `queued-unobserved`; 4xx ⇒ false 标 HTTP 码」, 与 F4 瞬态语义呼应, 判据可执行。残余两处见「新 Findings」m1/m2 (均降级 Minor, 见理由) |
| #6 (empty-diff 去分支名) | closed | §2.3 表「三点 diff 为空」不带分支名 |
| #7 (缺失文件骨架 + SC-11(d) 独立重读) | closed | §3.1「state 文件不存在且 verdict=wait 时先创建骨架」+ SC-11(d)「独立重读落盘文件断言」逐字在场, 且明确坏实现 (整块重建漏 carry-forward / stdout 自洽未落盘) 会在该断言致红 |
| #8 (版本引用点 14 处枚举) | closed (抽查通过) | 抽查 `CLAUDE.md:141`(「版本: 插件 aria-plugin v1.66.3」)、`README.md:8`(badge)、`README.md:242`(`Plugin Version:`) 三处均命中 spec 点名行号; 其余 11 处 (i18n ×3×3 + VERSION + gitlink) 未逐一重验, 信任 A5 R1/R3 已实核 |
| **#9 (NEG-4 登记 + 零执行史不得复制)** | **partial** | 我 R3-M1 的核心诉求 (「登记 catalog」不等于「会被执行」, NEG-3 零执行史) **已被采纳** — SC-15 新增「**且真跑一次** (`/skill-creator` 或等价 harness) 结果落 `ab-results/<date>-…/`」, 直接对齐我 R3 建议 #3 (比照 `eval-4-c24-gate-branchname` 先例)。但本轮用 `AB_TEST_OPERATIONS.md` + `/skill-creator` SKILL.md 实读发现一个**新**角度, 见 Findings m3 (降级 Minor, 理由见下) |
| #10 (misc minors, 含 SC-7 计数法) | closed (我的部分基本吸收) | SC-7 no-backend/main-核验对称收缩已加 (我 R3 minor 修复); 我另一条 R3 minor (SC-13「禁止人工模拟 CLI 序列」) 未被字面采纳, 见 m4 (低优先级, 不影响 verdict) |

## 新 Findings (本轮新鲜眼睛)

以下均按 R4 末轮严格判据 (「按 v4 实施会造成错误行为 / fail-open / 契约破坏 / 两实施者必然分叉且无 SC 能区分」) 复核后**降级为 Minor** —— 均不满足该门槛: 不产生错误行为, 不 fail-open, 不破坏契约, 且即使两实施者选择不同也不产生可观测的运行时/测试差异。

### [A3-R4-m1] Minor — TASK-0a 三分支映射覆盖 2xx/4xx, 未显式覆盖 5xx/网络异常

**锚点**: §3.5 `dispatch_viable := 600s 内观测到 run (2xx 但 600s 零 run ⇒ false, 证据标 queued-unobserved; 4xx ⇒ false 标 HTTP 码)`。

**问题**: 只枚举了 2xx (含/不含 run 两态) 与 4xx。若 dispatch POST 撞见 5xx (服务端异常) 或请求本身超时/网络错误 (heavy 节点拥堵是 CLAUDE.md 项目状态段自陈的当前常态), spec 未给出该分支该记 `true` 还是 `false`。

**为何降级 Minor (非 Major)**: TASK-0a 是**一次性、实现前**的人工探针, 其输出 `DISPATCH_VIABLE` 只控制 §2.3 是否在处方 message 里追加一行 dispatch 命令 (纯文案), 不参与 verdict 计算、不影响 gate 的 fail-open/fail-closed 属性——两种猜测的最坏后果都只是「给人看的处方文案里多一行或少一行」, 处方 (b)(c) 仍在, 不改变 gate 结论。不满足 Major 门槛「错误行为/fail-open/契约破坏」。

**建议**: 補一句「非 2xx/4xx (如 5xx、请求异常) → 按保守精神记 `false`, 标『probe-error: <detail>』」, 成本一句话, 使三分支之外的兜底也显式化, 避免执行者臨場发明。

---

### [A3-R4-m2] Minor — `DISPATCH_VIABLE=false` 时, §2.3 消息表/§3.3 处方模板对 `dispatchable_workflows` 的引用未纳入声明的删除 scope, 但不产生行为分歧

**锚点**: §3.5「落点 (条件 scope **只此一处**): dispatch_viable → `pre_merge_gate.py` 模块常量 `DISPATCH_VIABLE` → 2.3 trigger-matched 档是否渲染 dispatch 行」; 对照 §2.3 消息表「当 `DISPATCH_VIABLE and dispatchable_workflows` 追加处方行」与 §3.3 处方模板 (a) 行「受 `DISPATCH_VIABLE` 常量与列表非空控制」两处仍原样引用 `dispatchable_workflows` 字段/`DISPATCH_VIABLE` 常量。

**问题**: 若 `dispatch_viable=false` ⇒ §4 (定义 `dispatchable_workflows` 的唯一落点) 按声明**整段删除**, 则 `path_coverage` 结构上永远不会有 `dispatchable_workflows` 键。但「条件 scope 只此一处」的措辞把「§4 是否被实现」与「§2.3/§3.3 的引用文字是否要跟着精简」混成了同一句话, 未显式回答: 若 §4 真的整段删掉, §2.3/§3.3 里那两处仍写着 `DISPATCH_VIABLE`/`dispatchable_workflows` 的句子要不要跟着删。

**为何降级 Minor (非 Major)**: 用 `.get("dispatchable_workflows", [])` 取值 + Python `and` 短路求值, `DISPATCH_VIABLE=False` 时右操作数根本不会被访问, 不产生 `KeyError`, 不产生运行时分歧; 两种写法 (保留死代码 vs 连文档一并删) 在 SC-1~SC-16 的任何一条断言上都产生完全相同的通过/失败结果——不满足 R4「两实施者必然分叉**且无 SC 能区分**」的门槛 (SC 确实区分不了, 但原因是两种写法本就等价, 不是测不到的分歧)。纯粹是 spec 自我一致性上的一处措辞留白。

**建议**: 若 `dispatch_viable=false`, 在「条件 scope 只此一处」后加一句「§2.3/§3.3 中 `DISPATCH_VIABLE`/`dispatchable_workflows` 的既有措辞按此常量取值天然收敛为『恒不追加/恒不出现』, 无需再单独编辑文字」——把「不用改」也明确写成一句判断, 避免执行者误以为遗漏。

---

### [A3-R4-m3] Minor — SC-15「真跑一次」未点名基准对象是 `phase-c-integrator` 单一 skill 还是须覆盖 rule6_note 点名的两条行为 (跨 `phase-c-integrator` / `workflow-runner` 两个 skill)

**锚点**: rule6_note「三义务」第一条点名两条行为——(i)「surface `gate_error.message` 原文」(`phase-c-integrator/SKILL.md §C.2.4` 行为) / (ii)「`should_prompt=true` 时出 prompt 而非继续等」(`workflow-runner/SKILL.md` 2.5 行为); `NEG-4-no-run-for-branch.json` 登记进 `phase-c-integrator-pre-merge-gate.json`(`parent_skill: phase-c-integrator`) 的 `fixtures[]`; SC-15「真跑一次 (`/skill-creator` 或等价 harness)」。

**实读依据**: `AB_TEST_OPERATIONS.md` §「/skill-creator 内部机制」+ 官方 `skill-creator/SKILL.md`「Running and evaluating test cases」——`/skill-creator benchmark <skill-name>` 的执行单元是「针对某一个 skill 的 `evals/evals.json`」, 每条 eval 里的 `prompt` 决定 subagent 加载的是**哪个 skill**; `phase-c-integrator-pre-merge-gate.json` 的 `fixtures[]` 是**数据形态**(模拟 gate 输出 JSON, 非 `{prompt, expectations}` 形态的 eval), 需人工翻译成一条真实 eval prompt 才能喂给 `/skill-creator` —— `ab-results/2026-08-16-v1.66.0-137-rule6/RESULT.md` 的 `eval-4-c24-gate-branchname` 正是这个翻译动作的真实先例 (针对 `phase-c-integrator` 一个 skill)。

**问题**: SC-15 只要求「真跑一次」, 未点名 (a) 谁来做 fixture→eval prompt 的翻译, 参照哪个先例; (b) 「一次」是否需要覆盖两个 skill (phase-c-integrator 的 surface 行为 + workflow-runner 的 should_prompt 行为), 还是跑一次 phase-c-integrator 侧即视为满足。若执行者只对 `phase-c-integrator` 跑一次 (贴合 `fixtures[]` 的 `parent_skill` 归属), rule6_note 点名的第二条行为 (workflow-runner 的 `should_prompt`) 仍不会有一次真实 with/without 判决数据——回到我 R3-M1 指出的「登记≠已验证」问题的一个变种, 只是这次残留在「验证了行为 (i) 但未验证 (ii)」而非「完全零执行」。

**为何降级 Minor (非 Major)**: 这不产生错误的 merge 行为, 也不是 fail-open——它只影响 Rule #6 判据表第三行的**证据完整度** (审计/流程质量维度), 且本文档内已有 `eval-4` 先例可供 Phase B/D 执行者照抄两遍 (一次套 `phase-c-integrator` 的 prompt 场景, 一次套 `workflow-runner` 的 polling 场景), 不需要新设计。不满足「错误行为/fail-open/契约破坏」门槛; 「两实施者分叉」这里分叉的是**证据数量**而非**产品行为**, 且 SC-15 字面「真跑一次」在两种读法下都能「过」——不是 SC 测不出分歧, 而是 SC 目前只对「至少一次」计数, 未对「哪个/哪几个」计数。

**建议**: SC-15 加一句「若 rule6_note 点名的两条行为分属两个不同 skill (本 spec 为 `phase-c-integrator` + `workflow-runner`), 至少各跑一次」, 并在 §6 Phase D 待办第 3 条 (`aria-plugin#127` 追加评论) 里注明「两条行为各自的判决数据 (若都跑了)」, 而不仅是笼统的「NEG-4 登记」。

---

### [A3-R4-m4] Minor (延续自 R3, 未被 v4 采纳, 不阻塞) — SC-13 未显式排除「人工模拟 CLI 序列」

我 R3 报告已提出「建议在 SC-13 里加一句『须由一次真实 phase-c-integrator/workflow-runner skill 会话完成, 不接受人工模拟 CLI 序列』」, 逐字重读 v4 SC-13, 未见该句被采纳; 本轮不属于 R3 十簇任一编号处置项 (未落入 cluster #10 的「逐条吸收」列举清单), 判定为 not_addressed。维持 Minor, 成本一句话, 建议 Phase B 落地时补上, 不建议为此单独开一轮复议。

## 稳定性核验 (v4 diff 是否引入新的假绿/不可证伪项)

- 全部新增/改写的 SC (SC-2/3/4/7/10/11/13/14/15/16) 逐条核对「基线值 vs 期望值」, 均能清楚回答「怎么会红」(见上文逐条 + R3 报告已核实的部分), 未发现新的恒真断言或无法被坏实现触发的检查点。
- `AD-7`(计数单点/判定单点/真接线) 三个子命题分别由 SC-11(计数)/SC-11 CLI record should_prompt(判定)/SC-13+SC-16(真接线) 覆盖, 无「有主张无验证点」的新缺口。
- `R-f`(runtime_probe 首个采用者残余风险) 是诚实的风险披露, 非假绿包装。
- 唯一的「已知不完美但被显式豁免」项是 rule6_note 的序列型 fixture (`wait_then_green` 自陈零消费方) —— 这是 R2 起就有的披露, 非 v4 新引入, 且写法诚实 (不伪装已测)。

未发现 v4 新引入的假绿或不可证伪项。

## Verdict

PASS (0 Critical, 0 Major, 4 Minor) — 我 R3 报告的两条 Major (NEG-3/NEG-4 零执行史披露不足; TASK-0a `dispatch_viable` 2xx-零-run 分支未定义) 均已在 v4 得到实质性修复 (非纸面填字)。本轮新发现的 4 点在 R4 末轮严格判据下均不满足 Major 门槛 (不产生错误行为/fail-open/契约破坏, 且两种实现选择不会导致可观测的运行时或测试分歧), 已降级为 Minor 并给出一句话级修复建议, 不需要为此再开一轮结构性复议。v4 可批准进 A.2。

vote: PASS

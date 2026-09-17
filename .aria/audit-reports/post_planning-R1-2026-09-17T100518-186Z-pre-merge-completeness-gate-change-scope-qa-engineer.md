---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-09-17T10:33:08.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 已实读文件

- `openspec/changes/pre-merge-completeness-gate-change-scope/tasks.md` 全文 (207 行)
- `openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml` 全文 (1057 行, 含 `metadata` 全部子块与 31 个 `tasks:` 条目)
- `openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md` 全文 (565 行, 含 Why / What §1.0–1.4 / Impact / Tasks / Success Criteria SC-1~SC-22 / rule6_note; 待 owner 复议条目 0 只读了标题, 因决策单已裁决, 未再逐字复核其五轮全周期表)
- `.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md` 全文
- `CLAUDE.md` 全文 (已在系统提示词中)
- 源码: `aria/skills/audit-engine/tests/test_sibling_spec_probe.py:280-340` (两条既有 pytest 守卫)、`aria/skills/run_all_tests.sh:1-80` (`is_pytest_suite` 分类逻辑)、`aria/skills/audit-engine/SKILL.md:118-135` (per-round 探针 fenced bash 块)、`aria/skills/state-scanner/scripts/lib/spec_complete.py` 的 `_skill_md_has_real_bash_invocation` / `_classify_file_occurrence` / `classify_symbol_liveness` / `extract_claim_symbols` / `_iter_task_items` / `--gate` CLI 出口 (约 331-1120 行 + 1760-1823 行)
- `aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py:266` (实读方法名)
- `.aria/config.json` 的 `audit` 块 (实读, `json.load`)

## 实跑核验 (在自建 scratch 副本 / 本仓只读命令, 无 git 写操作)

1. `python3 -B -m unittest discover -s aria/skills/audit-engine/tests -p 'test_*.py'` → `Ran 104 tests ... OK`, 与 `metadata.test_runner` / `metadata.a2_state_runs` 声称的基线逐字一致。
2. 独立重写 N1/N2 函数对真实 `execution-modes.md` 跑基线 → `N1=False N2=False`, 与 `metadata.a2_state_runs.output` 声称的 `[A baseline] N1=False N2=False` 一致 (未使用计划提供的脚本, 自行重敲同一算法验证)。
3. `git -C aria cat-file -t ec72175` → `commit`, `git -C aria log --oneline -1 ec72175` → `Merge branch 'master' into feature/a1-entry-claim-duplicate-work-guard — 版本重算 1.70.0→1.71.0 (号被同伴轨占用)`, 与 TASK-027 第 4 步引用的「恢复指针先例」逐字相符。
4. `grep -n "def test_case_e_malformed" aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py` → `266: def test_case_e_malformed_aether_main_leg_routes_fail`; catalog json 逐字 `test_case_e_malformed_aether_routes_fail` (无 `_main_leg`) → 证实 SC-14/rule6_note 对 catalog node id 过期的描述准确。
5. `json.load('.aria/config.json')['audit']` → `checkpoints` 恰 7 键、无 `mid_post_spec`、`mode="convergence"`、`pre_merge="off"`, 与 proposal 头部「审计计划」段与 tasks.md/yaml 多处引用的本仓事实逐字一致。

以上五项均为独立复核 (未假定计划文档的自述为真), 全部通过, 未发现事实性错报。

## Findings

无 critical、无 major。以下两条 minor, 均不改变执行者的实际动作 (符合口径「不影响做错/做漏/卡住 ⇒ 最高 minor」)。

| id | severity | type | category | scope |
|---|---|---|---|---|
| d5a8f665 | minor | issue | testing | `detailed-tasks.yaml TASK-002` |
| c4986518 | minor | issue | testing | `detailed-tasks.yaml TASK-022` |

### m1 `d5a8f665` — TASK-002「另一席」复现性核验缺可执行的第二执行体

**summary**: `detailed-tasks.yaml:470` 要求「另一席从 F 重跑取样与第一列算法, 文件集与第一列取值逐字相同」, 但 TASK-002 整体只分配给单一 agent (`agent: qa-engineer`, `detailed-tasks.yaml:462`), 计划中没有第二个任务/agent 承担「另一席」。

**证据**: `detailed-tasks.yaml:453-470` (TASK-002 全部字段, `agent: qa-engineer` 于 `:462`, 该验证 bullet 于 `:470`)。全文 31 个 task 条目里未见任何其它任务把「B.0 语料复现校验」列为自己的 deliverable 或 verification。

**失败场景**: 执行者 (单一 qa-engineer 实例) 读到这条 bullet, 唯一可行的落地方式是自己把同一套确定性算法在同一个冻结提交 `F` 上重跑一遍。由于算法是确定性的 (排序、字段定序均已钉死), 「自己重跑」与「另一席重跑」在正常情况下必然逐字相同, 这条断言因此**结构上很难变红** (只有脚本自身存在未加 `sorted()` 的非确定性枚举时才可能不同, 而这不是这条 bullet 的原始设计意图 —— 原意是防「标注者心智模型偏差」, 这需要真正独立的第二执行体才能验到)。它不会导致执行者做错或卡住, 只是把「独立复现」的名义弱化成「自我复算」, 验证强度低于字面承诺。

**建议修法**: 要么删掉「另一席」措辞改为「重跑一次核对脚本自身确定性 (排序/去重是否稳定)」, 要么显式拆一个小任务并指派给另一个 agent 角色 (如 knowledge-manager) 承担纯粹的复现性核对。二者均为廉价改动, 不影响任务图结构。

### m2 `c4986518` — TASK-022 对 SC-11 `post_planning` 断言未在 yaml 本地复述读前必看 #16 的例外条款

**summary**: `detailed-tasks.yaml:854` 写「`post_planning` 为 present (tasks.md 读前必看第 16 条)」, 是一条无条件断言式表述; 完整的容错口径 (「实跑为 `missing` 属新发现, 记台账上报, 不改断言」) 只在 `tasks.md:32` (读前必看 #16) 给出, yaml 侧仅以括注引用, 未内联复述。

**证据**: `tasks.md:32`「... 期望 **`present`**, 实跑为 `missing` 属新发现, 记台账上报, 不改断言; 本条无区分力, 区分力在重写 c」; `detailed-tasks.yaml:854`「post_planning 为 present (tasks.md 读前必看第 16 条); unattributed_count > 0 且 unattributed 非空 (不写死数值)」。

**失败场景**: 若执行 TASK-022 的 agent 只读 yaml (`detailed-tasks.yaml` 被明确定为「单一 SOT」, `tasks.md:5`), 没有回查 `tasks.md` 第 16 条全文, 可能把这条 bullet 误当作硬性 pass/fail 门 —— 若彼时 `post_planning` 报告因某种原因 (如归档/清理) 未落盘而返回 `missing`, 执行者可能误判 TASK-022 失败并卡在这一步, 而不是按设计意图「记台账、报告新发现、不改断言」处理。风险不高 (引用是明确的、可回溯的, 且计划反复采用「引用读前必看第 N 条」这一模式贯穿全文, 说明这是执行者应当遵循的既定阅读习惯), 故判 minor 而非 major。

**建议修法**: 在 `detailed-tasks.yaml:854` 就地补一句「若实跑为 `missing`, 记台账为新发现并继续, 不视为本任务失败」, 使 yaml 单独可读时不产生歧义。

## 对执笔人自报薄弱点的表态

(a) 「读前必看第 7、8 条的取值是执笔人钉定的, proposal 未定义」—— **可接受**。这些是 proposal 自身明确留白的窄技术字段取值 (bypassed 态的非判定键取值、S4-bypassed 的 `checked_checkpoints` 收口规则), 按 owner 2026-09-01/2026-09-12 两次裁定的「产品级 owner 裁、技术级 AI 裁」分工与 Rule #10 白名单第四类同构, 计划已在读前必看逐条留痕依据, 未与任何已裁定项或 SC 断言冲突 (已抽查 SC-9(2)/SC-17(5) 的字段取值与读前必看第 7/8 条描述逐字对应)。

(b) 「组 5 发布前提偏重 (5.8 要求 aria-orchestrator 与两端完全一致; 5.2 结束后强制对齐协调 ref 会回退 `--no-push` 心跳)」—— **可接受**。TASK-030 对 `aria-orchestrator`/`standards` 的一致性前置检查是防止 C.2.5 顺带推动他轨未完成内容的保守设计, 直接对应 CLAUDE.md「多远程推送两条硬约束」与 memory `feedback_mirror_sync_needs_mechanical_backstop`/`#165` 的前车之鉴, 失败模式是「停下上报」而非误推, 方向正确; TASK-024 结束后回退本容器 `--no-push` 心跳并在「下个会话重新刷新」已写明恢复路径, 心跳本身是可重建的活性信号, 无数据丢失风险。两者均是宁可偏保守也不冒推送风险的取舍, 与项目一贯的 fail-closed 倾向一致。

(c) 「N1/N2 仍是按行切片的文本谓词; SC-11 的 post_planning 期望收紧为 present; SC-6 快照自证放在活体运行 (4.4), 不进单测」—— **可接受**。N1/N2 的局限已在 `metadata.new_checks.cannot_catch` 显式声明并指明由 SC-16/SC-18/SC-17(5) 的运行时断言兜底, 是「机械护栏 + 语义测试」分层设计的正常形态, 非隐藏缺陷; SC-11 收紧为 present 的问题已作为 m2 单独记录 (minor, 非不可接受); SC-6 快照 (295KB) 不进单测改走 TASK-022 活体执行, 理由 (不随插件分发) 具体且与 tasks.md 判断清单第 5 条一致, 是合理的工程取舍。

## 风险 / 疑问 (不计入 finding)

- TASK-002 的取样候选 `state-scanner-inter-cycle-surfacing` 依赖冻结时刻的实测下界 (F-a≥2/F-b≥3); 若该 change 已被后续归档/改名导致样本进一步萎缩, 计划已有兜底 (换 id / 按实测上限降低下界), 但降低下界后 SC-2 对应族的鉴别力会相应减弱 —— 这是语料活体的固有风险, 计划已诚实标注 (「不得为了凑数把争议条目放回」), 不算计划缺陷, 仅记录以供 Phase B 执行者注意。
- TASK-027 第 4 步「取号复核」与第 6 步「取号终核」之间, 若在窗口期内被并发轨 (如决策单 §5 提到的 10CG/Aria#211 T4) 抢先占用 `ab-suite/version.yaml` 或插件版本号, 计划已给出「停下上报」路径 (owner_gates 第 6 项), 未发现遗漏。

## Verdict

**PASS** — 0C / 0M / 2m — **Vote: PASS**

## 是否足以开始 Phase B

**足以**。全部 SC-1~SC-22 (含 N1/N2/N3) 在 tasks.md 的 SC↔任务映射表与 yaml 各 TASK 的 verification 之间逐条核对一致, 未发现遗漏或矛盾; RED 批次的「脚本缺失即 AssertionError」设计、反事实批次的「非实现者构造 + 三步法」设计、三处 Level 3 重写 (SC-12 liveness / §1.3(c) 自证段 / SC-6 自证格) 均已用真实源码 (`spec_complete.py` 的符号分类器、`SKILL.md` 的 fenced bash 块结构) 交叉验证为可执行且具备区分力; SC-12 在有/无 `ARIA_COORDINATION_NO_PUSH` 两种会话下的安排 (TASK-001/021/024/027 各自的会话前提) 顺序正确、无冲突。两条 minor finding 均不构成 Phase B 的合法性障碍。

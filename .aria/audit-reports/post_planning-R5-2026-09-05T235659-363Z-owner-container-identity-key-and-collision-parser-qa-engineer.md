---
checkpoint: post_planning
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-06T00:03:12.000Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/detailed-tasks.yaml
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## R4 处置核对 (含 grep 判据反事实实跑结果)

对照 R4 聚合报告的 m1 (本席 R4 报告 m-1) 与 R4 PP4-M1, 逐条实读 v5/v11 落地并**实跑**判据。

### m1 (本席 R4 m-1)：TASK-018 反向 grep 锁改为两条可执行 grep — 已闭合, 附反事实

v5 `detailed-tasks.yaml` TASK-018 verification 第二行现为：

> 机械锁 (两条 grep, 对 `lib/identity.py:126-140` 区间): 含「当前仍参与协调身份」≥1 行; 含「仅展示」的每一行同时含「后续」或「将」(即 `grep -c 仅展示 == grep -c 仅展示.*(后续|将)|(后续|将).*仅展示`)

在 scratchpad (`/tmp/claude-1000/.../scratchpad/`) 构造 4 个合规/违规样例, 用判据原文逐字实跑 (cond1 = `grep -c 当前仍参与协调身份` ≥ 1; cond2 = `grep -c 仅展示` == `grep -cE '仅展示.*(后续|将)|(后续|将).*仅展示'`):

| 样例 | 内容摘要 | cond1 | cond2 | 判据结果 |
|---|---|---|---|---|
| `compliant.txt` | S1 规定原文 (「当前仍参与协调身份…后续版本改为仅展示」) | 1(PASS) | 1==1(PASS) | **PASS(绿)** |
| `compliant_variant_jiang.txt` | 用「将改为仅展示」替代「后续版本改为」 | 1(PASS) | 1==1(PASS) | **PASS(绿)** |
| `violation_A_no_current_wording.txt` | 只写「label 仅展示」, 缺 S1 现况句 | 0(FAIL) | 1==0(FAIL) | **FAIL(红)** |
| `violation_B_bare_current_behavior.txt` | 含 S1 现况句, 但另起一行「label 目前仅展示」把仅展示写成当前行为陈述 (无转折) | 1(PASS) | 1==0(FAIL) | **FAIL(红)** |

`violation_B` 正是 R4 m-1 描述的「仅展示单独作为当前行为描述出现」的典型形态：机械两条 grep **正确判红**，证明 v5 的可执行化改写没有丢失原判据的拦截意图，反事实通过。**R4 m-1 闭合确认。**

**新发现 (本轮, 记入 Findings)**：进一步构造 `violation_C_false_negative_via_jiang.txt` — 同一行内「仅展示」与不相关的「将」共存 (`label 仅展示, 用于将来扩展的 owner 字段占位说明`) — 实跑：cond1=1(PASS), count(仅展示)=1, count(仅展示+后续|将)=1(PASS) → **机械判据判 PASS(绿)**，但该行语义上正是把「仅展示」当当前行为陈述句写、无真实转折语气，只是恰好同行出现了修饰另一名词的「将」字。说明两条 grep 对单字符「将」的匹配没有绑定语义关联，存在可被同行内不相关「将」字掩盖的假阴性缝隙。降级为 Minor 见 Findings（理由见下）。

### S2-1 翻转判据与 S1 判据互斥性核验 — 已核实, 且互斥关系强于「互斥」(实为完全二分)

v5 S2-1 verification 追加：「注释区间不再含『当前仍参与协调身份』」。用同一 `grep -c 当前仍参与协调身份` 对 `s2_flip_compliant.txt`（不含该串的 flip 后注释样例）实跑：count=0 → S2-1 判据 PASS；对同一样例跑 TASK-018 cond1（要求 ≥1）→ FAIL。两判据分别是 `count ≥ 1` 与 `count == 0`，对同一 token 计数是穷尽二分（不存在同时满足两者的注释，也不存在两者都不满足的注释——非空字符串场景下 count 非负整数只能落在其一），构成比「互斥」更强的完全划分，不会出现 B 期执行者两个判据都读绿或都读红的歧义态。

## Findings

无 Critical。无 Major（R4 PP4-M1 三处已逐字核对 v11 文本，全部按约定处置落地，见下）。

### PP4-M1 (R4 Major) 处置复核 — 实读确认三处均已修正

- (a) SC-9 尾句：`proposal.md` 现读「`RECOMMENDATION_RULES.md:31` 今日两 token 均无, 须同时补 `cross_owner` 与 `identity_advisories` 才满足首句」——与首句「须同时含两 token」不再矛盾（原 v10 尾句「加一句后满足」的单 token 暗示已消除）。
- (b) T11 时点拆分：`proposal.md` T11 现拆两时点（B.1 起手 / merge 后归档前），`tasks.md` 0.2（B.1 起手征求 #174 ack）与 5.5（merge 后回帖关 #193，5.6 执行）逐字对应；T11 引用的「上表 :104 行」（`sed -n '100,106p'` 核对为「与 a1-entry 的边界与两种 ship 形态」行）明确 S2 前提含「对方在 #174 ack」，与 0.2 的「B.1 起手征求 ack」时序一致，不再互否。
- (c) SC-7 文件级限定：`proposal.md` SC-7 (b) 分句现读「本 Spec 新建测试**文件**一律写 TestCase…对 `test_collision.py` 的新增用例沿用该文件的 pytest 风格, 计入 (b) 的 passed 基数」；与 `detailed-tasks.yaml` TASK-032 verification (b)「passed ≥ 16 + 本 Spec 在该文件新增数」及 `metadata.test_runner`「test_collision.py 新增沿用 pytest 风格」三处措辞同义、无脱钩。

### m-R5-1（Minor，新增，非阻塞）：TASK-018 机械锁对「将」的单字符匹配存在假阴性缝隙

- severity: minor
- category: testing / verification-mechanism
- scope: `detailed-tasks.yaml` TASK-018 verification 第二行（v5 新增的两条 grep 机械锁）
- summary: 机械锁用单字符「将」判定「后续/将」转折语气，未绑定该字与「仅展示」的语义关联。当同一行内「将」字修饰句中另一无关名词（而非表达仅展示状态的未来时）时，`grep -cE '仅展示.*(后续|将)|(后续|将).*仅展示'` 仍会计数命中，导致机械判据对本应判红的「仅展示被当作当前行为陈述」场景误判绿。
- 证据: scratchpad `violation_C_false_negative_via_jiang.txt` 实跑：`cond1=1(PASS)`, `count(仅展示)=1`, `count(仅展示+后续|将)=1` → 机械结果 PASS(绿)，但该行「label 仅展示, 用于将来扩展的 owner 字段占位说明」把「仅展示」写成了当前行为的陈述句，无真实转折。
- 不升级为 Major 的理由：TASK-018 title 已把 S1 现况注释的**具体措辞**规定死（「label 当前仍参与协调身份 (设了会换身份), 后续版本改为仅展示; 建议留空」），B 期执行者的正常路径是照抄该固定句式而非自由造句，实际触发此缝隙需要执行者主动写出「同行掺杂不相关『将』字」这类反常表述，概率极低；且该 Spec 内已有先例（SC-9 多处「上下文句同义, 人工核」）承认纯字面判据有语境盲区、由人工核兜底，本条与既有容忍模式同类，不构成新的执行风险类别。建议（非强制，供 B 期或未来同类锁参考）：若要彻底封死，可把「将」的匹配收紧为「将改为」或「将仅」等二字/三字复合模式，但本轮不作为收敛阻塞项处理。

## Counts (nC/nM/nm)

- Critical (C): 0
- Major (M): 0
- Minor (m): 1 (m-R5-1，非阻塞，供 B 期参考)

## SC-1..SC-11 ↔ TASK verification 双向映射复核

`tasks.md` 「Success Criteria ↔ 任务映射」表（:105-119）本轮 diff 未触碰，逐行核对仍为 11 条全覆盖：SC-1→1.1/2.1；SC-2→1.2/1.5/1.7→2.2/2.3/2.5；SC-3→1.8→2.7/2.8 (S1 臂) + S2 后续表 (S2 臂)；SC-4→1.3→2.4；SC-5→3.1/3.2/3.3；SC-6→1.6→2.6；SC-7→4.2/4.3；SC-8→1.4→2.3；SC-9→1.11/3.4/3.5；SC-10→1.9→2.9；SC-11→1.10→2.6。TASK-018 (parent 2.7) 与映射表 SC-3 行「1.8→2.7」一致；S2-1 (reserved, parent 6.1) 落在「S2 后续表」承载 SC-3 的 S2 臂，未与任何其它 SC 冲突。无脱钩、无遗漏。

## 回归判据复核 (baseline 再实跑)

自 R4 起本仓 `aria` 子模块指针未变 (`7dd0135`, 与 `tasks.md` scope_repos 一致)，`identity.py` / `collision.py` 自 R4 后无代码改动 (`git -C aria log` 核对无新提交)，本轮改动仅限 openspec 三文件文本。仍按判据原样再跑一次两条命令：

- `python3 aria/skills/state-scanner/tests/run_tests.py` → `Ran 1476 tests in 99.704s` / `OK`
- `cd aria/skills/state-scanner && pytest -q -p no:cacheprovider tests/test_collision.py` → `16 passed in 0.48s`

两数字与 R3/R4 记录基线一致，metadata.test_runner / SC-7 (b) / TASK-032 verification (b) 三处「carve-out 计入 (b) 基数」文本互为同义表述，未发现语义分歧。

## Vote

PASS

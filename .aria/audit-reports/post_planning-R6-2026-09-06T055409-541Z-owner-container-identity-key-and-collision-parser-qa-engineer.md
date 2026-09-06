---
checkpoint: post_planning
mode: convergence
rounds: 6
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-06T05:54:09.541Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/detailed-tasks.yaml
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## R5 处置核对 (含样例实跑表)

对照 R5 聚合 m-R5-1 (本席 R5 报告: TASK-018 机械锁对单字「将」的假阴性缝隙), 核对 v6 的处置: `detailed-tasks.yaml` TASK-018 verification 第二分句把判据从「含『后续』或『将』」收紧为「含短语『后续版本』」, 并用 `grep -cE` 显式写出可执行形态。用 R5 的 4 个样例加 3 个新对抗样例, 在 scratchpad (`/tmp/claude-1000/.../scratchpad/r6-qa/`) 逐字实跑 v6 公式：

- cond1 = `grep -c 当前仍参与协调身份 <file>` ≥ 1
- cond2 = `grep -cE 仅展示 <file>` 的计数 == `grep -cE '(后续版本.*仅展示|仅展示.*后续版本)' <file>` 的计数
- 整体判据 = cond1 且 cond2 均为真才算绿

| 样例 | 内容摘要 | cond1 | cond2 | 判据结果 | 预期 | 一致? |
|---|---|---|---|---|---|---|
| `compliant.txt` | S1 原文措辞 (「…后续版本改为仅展示…」) | PASS(1) | PASS(1==1) | **绿** | 绿 | 一致 |
| `compliant_variant.txt` | 语序调换「仅展示将在后续版本生效」, 仍同行含两短语 | PASS(1) | PASS(1==1) | **绿** | 绿 | 一致 |
| `violation_A_no_current_wording.txt` | 缺 S1 现况句, 只写「仅展示, 后续版本行为不变」 | FAIL(0) | PASS(1==1) | **红**(cond1 拦) | 红 | 一致 |
| `violation_B_bare_current_behavior.txt` | 含现况句, 另起一行「目前仅展示」无「后续版本」 | PASS(1) | FAIL(1==0) | **红** | 红 | 一致 |
| `violation_C_old_jiang_loophole.txt` (R5 遗留假阴性构造, 用旧「将」) | 「仅展示, 用于将来扩展的 owner 字段占位说明」 | PASS(1) | **FAIL(1==0)** | **红** | 红 (R5 曾判绿) | **R5 缝隙已堵住** |
| `violation_D_cross_line_split.txt` (新, 对抗样例) | 「后续版本」与「仅展示」分处不同行 | PASS(1) | FAIL(1==0) | **红** | 红 (跨行不该算数) | 一致 |
| `violation_E_semantic_negation_same_line.txt` (新, 对抗样例) | 同行含两短语但语义否定转折:「并非到了后续版本才仅展示, label 现在就是仅展示状态」 | PASS(1) | **PASS(1==1)** | **绿** | 应判红 (该句把「仅展示」写成当前行为陈述, 只是字面上捎带了「后续版本」四个字来否定它) | **不一致 — 新缝隙, 见 Findings M-1** |
| `violation_F_verification_own_example_missing_banben.txt` (新, 对抗样例) | 逐字照抄 TASK-018 verification 第一分句给出的「S1 实况措辞」例句原文:「label 当前仍参与协调身份, 后续改为仅展示, 建议留空」(无「版本」二字) | PASS(1) | **FAIL(1==0)** | **红** | 若按该字段自身给的例句执行, 本应判"这就是正确措辞"却被同字段第二分句判红 | **verification 字段自相矛盾, 见 Findings M-2** |

结论: R5 m-R5-1 (单字「将」假阴性) **已闭合** — `violation_C` 用 v6 公式正确判红。但本轮构造出两个新缝隙 (M-1 语义否定同行共现假阴性, M-2 字段内自相矛盾), 详见 Findings。

## Findings

无 Critical。

### M-1 (Major): TASK-018 verification 第二分句「同行短语共现」判据对语义否定构造存在假阴性

- severity: major
- category: testing / verification-mechanism
- scope: `detailed-tasks.yaml` TASK-018 verification 第二分句 (v6 新增 grep -cE 判据)
- summary: v6 判据只检查「仅展示」与「后续版本」是否同行共现 (`grep -cE`), 不检查语义方向。当执行者写出「并非到了后续版本才仅展示, label 现在就是仅展示状态」这类语义上否定转折、字面上又同时含两短语的句子时, cond2 仍判 PASS (机械判绿), 但该句实质是把「仅展示」写成 S1 阶段的当前行为陈述——正是 TASK-018 title 本要拦截的错误措辞类型。
- 证据: `violation_E_semantic_negation_same_line.txt` 实跑: cond1=1(PASS), `grep -cE 仅展示`=1, `grep -cE '(后续版本.*仅展示|仅展示.*后续版本)'`=1 → cond2 PASS → 整体机械判据判**绿**, 与预期的"应判红"矛盾。
- 与 R5 m-R5-1 的关系: 同一类"字面共现不等于语义转折"的缝隙, R5 是单字符「将」被无关词掩盖, R6 收紧后单字符缝隙已堵住, 但短语级共现检查仍是纯字面匹配, 未绑定语义方向, 缝隙以更刁钻的形式复现。
- 处置建议 (非强制): 若要彻底封死, 机械判据应改为要求逐字匹配 TASK-018 title 给出的**唯一固定句式**（如 `grep -F` 全句而非分部件共现), 而非"两短语同行共现"这种可被语序/否定词绕过的弱判据。是否值得再改由 owner 权衡: 触发本条需要执行者主动写出带显式否定语的复杂句, 概率低于 R5 那条 (R5 只需一个不相关「将」字, 本条需要构造完整否定分句), 可与 R5 精神一致地判定为"低概率但存在, 记录不阻塞", 但鉴于本条与 M-2 同源 (同一字段的匹配粒度问题), 建议合并处理: 见 M-2。

### M-2 (Major): TASK-018 verification 字段内部自相矛盾 — 给出的「S1 实况措辞」例句不满足同字段的机械锁

- severity: major
- category: spec-consistency / testability
- scope: `detailed-tasks.yaml` TASK-018 verification 第二条 (第 361 行), 第一分句「文件头注释为 S1 实况措辞 (label 当前仍参与协调身份, 后续改为仅展示, 建议留空)」与紧随其后第二分句的机械锁 `grep -cE`
- summary: 该 verification 字段第一分句给出的"S1 实况措辞"例句原文是「label 当前仍参与协调身份, 后续改为仅展示, 建议留空」——**没有「版本」二字**。这句例句本身自 v4 起从未被改动过 (v5→v6 diff 只改了第二分句的机械锁部分, 未同步核对第一分句例句)。v6 把机械锁收紧为要求短语「后续版本」(而非 v5 的单字「后续」或「将」) 后, 逐字照抄这条例句反而会被同一字段的机械锁判**红**——因为例句里只有「后续」没有「版本」。
- 证据: `violation_F_verification_own_example_missing_banben.txt` 用第一分句例句原文逐字构造, 实跑: cond1=1(PASS), `grep -cE 仅展示`=1, `grep -cE '(后续版本.*仅展示|仅展示.*后续版本)'`=0 → cond2 **FAIL** → 整体判**红**。
- 交叉核对: `tasks.md` 2.7 给出的"S1 实况措辞"例句是「label 当前仍参与协调身份 (设了会换身份), 后续版本改为仅展示; 建议留空」——**含**「版本」二字, 与 detailed-tasks.yaml 第一分句例句字面不同, 且只有 tasks.md 版本能通过 v6 机械锁。
- 影响: `detailed-tasks.yaml` 依 `rule6_note` 惯例被视为 verification 单一来源、应自包含可执行; 但该字段自身第一分句 (措辞指导) 与第二分句 (机械判据) 互相矛盾, 若 B 期执行者只读这一个字段并照抄括号内例句 (合理预期, 因为字段就是这样写的), 会产出一份被同字段机械锁判红的注释, 需要额外去 tasks.md 交叉核对才能发现正确写法, 增加返工风险。这不是本轮新引入的臆想场景, 而是 v6 收紧动作 (从「后续」到「后续版本」) 与旧例句 (只有「后续」) 之间产生的直接副作用, 上一轮 (R5) rework 时未同步检查该字段第一分句。
- 处置建议: 把 `detailed-tasks.yaml` TASK-018 verification 第一分句例句同步补上「版本」二字（改为「后续版本改为仅展示」), 使其与 tasks.md 2.7 及第二分句机械锁三处一致；这是一个字面文本同步问题, 修复成本极低 (改一处措辞), 建议在 B 期落地前 (或本轮若还要 rework) 顺带补上, 不必单独开一轮审计。

### 补充：S2-1 (TASK-027) 三条 verification 逐条可测性核验

1. 「翻转后的 lock-in 断言绿, 且改前对 S1 实现红」— **可机械执行**: 这是标准 RED→GREEN 反向验证形态 (对翻转后的断言, 先在未改代码的 S1 实现上跑一次预期红, 再在改后代码上跑一次预期绿), 与本 Spec 其余 SC 的"先红后绿"惯例一致, 无歧义。
2. 「注释区间不再含『当前仍参与协调身份』」— **可机械执行**, 且与 TASK-018 cond1 (`grep -c 当前仍参与协调身份 ≥ 1`) 构成完全二分 (`count == 0` vs `count ≥ 1`, 对非负整数计数穷尽覆盖, R5 已证, 本轮 token 未变, 复核仍成立)。
3. 「全仓 grep 无残留『S1 lock-in』判据文本」— **可执行性存疑, 未升级为独立 finding 的理由见下, 并入 M-2 类问题簇一并记录**: 实测 `grep -rn "S1 lock-in" openspec/ aria/` 命中 5 处, 全部是本 Spec 自身的规划文档字面 (`tasks.md:49`、`tasks.md:98`、`detailed-tasks.yaml:45/46/209/360`)，即"S1 lock-in"这个短语本身就是这份规划文档描述 TASK-008/018 机制时使用的**元描述词**, 不是即将被删除的代码产物。若 S2 真正激活并执行 TASK-027, 按字面"全仓"grep, 该 Spec 归档后 (`openspec/changes/archive/...`) 这些历史文本仍会永久留存, 使这条验收字面上**永远无法转绿**, 除非把"全仓"显式限定为"仅 `aria/` 代码与测试文件, 不含 openspec/ 计划文档自身"。这是一处需要收窄措辞的 testability 缺口, 但由于 (a) TASK-027 是 reserved/conditional 任务, 只有 S2 真正激活才会被执行, 当前多半不会触发; (b) 执行时的合理人工判读 (B 期执行者大概率会理解"全仓"指代码而非历史规划文档, 类似先例 SC-9 系列已接受"人工核对"兜底纯字面判据的语境盲区) — 故本条本轮判定为**记录不阻塞**, 建议措辞在下一次真正触及 TASK-027 时 (即 S2 激活时点) 顺带收窄, 无需本轮为此专门 rework。

## Counts (nC/nM/nm)

- Critical (C): 0
- Major (M): 2 (M-1 语义否定假阴性 / M-2 verification 字段内自相矛盾例句)
- Minor (m): 0 (R5 的 m-R5-1 已闭合; S2-1 第三分句 testability 顾虑降级并入说明性文字, 未独立计为 minor, 因判定为记录不阻塞且概率场景尚未触发)

## 回归判据复核 (baseline 再实跑)

- `python3 aria/skills/state-scanner/tests/run_tests.py` → `Ran 1476 tests in 133.582s` / `OK` (数字与 R3-R5 记录一致; 墙钟耗时比 R5 的 99.7s 长, 但 SC-7 判据只看 pass/fail 与 Ran 数, 与 memory `perf_regression_min_not_median_and_run_solo` 一致, 未使用耗时作判据)
- `cd aria/skills/state-scanner && pytest -q -p no:cacheprovider tests/test_collision.py` → `16 passed in 0.83s`
- `git -C aria log -1 --oneline` → `7dd0135` (v1.69.1, 与 tasks.md scope_repos 一致, 未变)

两数字 (1476 / 16) 与既往各轮基线一致, 本轮 openspec 三文件之外未发现代码改动。

## Vote

REVISE

---
seat: P3-code-reviewer
round: R1
checkpoint: post_planning
spec: secret-guard-manifest-precision
audit_target: openspec/changes/secret-guard-manifest-precision/detailed-tasks.yaml
baseline_sha: 400f0bc
verdict: PASS          # v1 REVISE → v2 终判 PASS (见文末「v2 终判」)
ready_for_a3: true
v1_verdict: REVISE
counts:
  critical: 0
  major: 0
  minor: 0
  v1_counts: {critical: 0, major: 1, minor: 4}
  closed: [P3-M1, P3-m1, P3-m2, P3-m3, P3-m4]
  not_closed: []
verification_table:
  total: 24
  pass: 24
  fail: 0
  v1: {pass: 23, fail: 1}
timestamp: "2026-08-22"
---

# post_planning R1 — P3 code-reviewer 席: detailed-tasks.yaml 事实面核验

审计方式: `git show 400f0bc:hooks/secret-guard.sh` / `hooks/tests/secret-guard.test.sh` 冻结树逐行核对 (非活树); proposal.md 逐条对数; CLAUDE.md 原文比对。只审不改。

## 一行摘要

yaml 的全部行号 / 计数 / SC 拆解 / metadata / agent 分配 / 依赖图对真代码与 proposal **23/24 PASS**; 唯一事实错误: TASK-005 声称 nonce 流程 case「对基线亦 RED」, 实际按 hook 控制流该 case 在基线上**恒绿** (路径未入清单 → :546 不命中 → 直接 exit 0, 根本走不到 ack 块), 须改写断言形态才能成为 baseline-failing。

## Findings

### [P3-M1] TASK-005 nonce case 的「基线 RED」断言不成立 (恒绿假 fixture)

- 位置: `detailed-tasks.yaml:141` — `"nonce case 对基线亦 RED (路径未入清单时 ack 路径不触发)"`; deliverable `:138` 写 `nonce 流程 case want=0`
- 真代码 (`secret-guard.sh@400f0bc :546-:551`): Read/Edit 路径只有在 `lower_path` 命中 :546 清单**之后**才进入 `SECRET_GUARD_ACK_PATH` / nonce 判定块。基线上 `~/.claude/settings.json` 不在清单 → 整个 if 不进 → exit 0。
- 推论: `want=0` + 有效 nonce 的 case 在基线上 exit 0 == want 0 → **GREEN**, 与 yaml 自述「RED」矛盾; 括号里的理由「ack 路径不触发」恰恰是它绿的原因, 不是红的原因。
- 为什么重要: 这是 memory `feedback_counterfactual_test_for_every_new_sc` 点名的「恒绿断言」; SC-2「nonce 流程走通 1 例」若按此写, 实现前后都绿, 不构成 ACK-PATH-ONESHOT 对新条目生效的证据。
- 如何修 (任选其一, 改 yaml 措辞即可, 不动 proposal): (a) 沿用既有 R3-C-9 套路 (`test.sh:427-432`): 同路径**无 nonce** 的 read_case want=2 (基线 exit 0 → RED) + 有 nonce want=0 成对; (b) 有 nonce 的 case 附加断言 marker 文件被消费 (`[[ ! -e /tmp/secret-guard-ack-$USER-$nonce.nonce ]]`), 基线上 marker 未被 rm → RED。建议 (a), 与既有套件同构。

### [P3-m1] TASK-003 verification 只枚举 8/9 条期望

- `:104` 列 RED 4 条 (jq{env} / 行级 ×2 / 混合源) + GREEN 4 条 (keys / wc / >/dev/null / .env 对照) = 8; proposal SC-3 的第 5 条「直读无管道 `jq '{model}' <file>` → 2」未出现在 verification。该条在 TASK-002 落地后即 GREEN (pattern 命中且无 credit), 属守卫类而非红绿窗口, 但 9 条标题数与 8 条明细数不齐。`:105` 的「逐条与 proposal SC-3 表一致」兜住了语义, 建议把第 9 条补进明细 (标为 GREEN-after-002) 免执行席漏写。

### [P3-m2] exec_order 数值与依赖边不单调

- TASK-003 (`exec_order: 2`) 依赖 TASK-002 (`exec_order: 2`); TASK-012 (`exec_order: 4`) 依赖 TASK-011 (`exec_order: 4`)。parallel_groups 已正确把 003 单独放 G3, 所以执行语义无误, 但 `exec_order` 字段失去「同序可并行」的含义。若该字段有机械消费方 (task-planner 校验 / workflow-runner) 需确认它只读 parallel_groups; 否则把 003→3 / 004,010→4 / 011→5 / 012→6 顺延。

### [P3-m3] G4 并行组 TASK-004 与 TASK-010 同写 `secret-guard.sh`

- `:348` `[TASK-004, TASK-010]` 二者无依赖边 (核实正确), 但 deliverables 都是 `aria/hooks/secret-guard.sh` (004 改 `_sg_compute_credit` :306-392 区; 010 改 risky_patterns :639+ 区)。区域不重叠, 逻辑可并行, 但两个 backend-architect 实例并发 Edit 同文件有 `feedback_concurrent_write_safety` 类风险。建议 notes 注明「同文件不同区, 串行落盘或同一 agent 顺做」。

### [P3-m4] TASK-007 deliverable 文件名占位 `2026-08-xx`

- `:172` `.aria/notes/2026-08-xx-secret-guard-179-pattern-rows.md`。A.3 派发前定名, 否则执行席各自起名导致 TASK-010 `notes` 引用「TASK-007 清单」找不到唯一文件。

## 核验表

| # | 项 | yaml 声称 | 真源核对 | 结果 |
|---|---|---|---|---|
| 1 | TASK-004 `:332` | jq 名字面 credit (keys/length/paths) | :332 `_sg_line_match "...(keys\|length\|paths\|leaf_paths)..."` | PASS |
| 2 | TASK-004 `:384` | `wc -[clw]` | :384 `wc[[:space:]]+-[clw]` | PASS |
| 3 | TASK-004 `:387` | sha*/md5sum | :387 `(sha256sum\|md5sum\|sha1sum\|sha512sum)` | PASS |
| 4 | TASK-004 `:373-380` | 丢弃族 | :373 `>/dev/null` / :376 `&>` / :380 `-o /dev/null` | PASS |
| 5 | (proposal What.1b 排除集) `:348/:351/:354/:358/:362/:365` | grep 锚/-v/sed/cut/awk ×2 | 六行逐一对应 | PASS |
| 6 | TASK-004 函数名 `_sg_compute_credit` 只收 `$seg` | — | :306 定义, :932 调用 `_sg_compute_credit "$seg"` | PASS |
| 7 | TASK-006 `:546` 29→32 | 29 分支 | python 拆 `\|` 得 29 | PASS |
| 8 | TASK-002 `:785/:786` | python3 -c / node -e 源组 | :785 `python3?[[:space:]]+-c...` / :786 `node[[:space:]]+-e...` | PASS |
| 9 | TASK-002 "12 reader" | 12 | :709 reader 组 cat…sed 共 12 | PASS |
| 10 | TASK-007 `:709` shell-rc 行 | — | :709 shell-rc pattern, :710 ssh 变体 | PASS |
| 11 | TASK-007 sibling 行存在 (.env / id_rsa) | — | :685-687 .env 族, :700 id_rsa 族 等 | PASS |
| 12 | TASK-010 整串 `[[ =~ ]]` 语义 | ^ = 串首 | :930 `[[ "$seg" =~ $pat ]]` 裸整串 | PASS |
| 13 | TASK-001/005 helper 名 `bash_case` / `read_case` | — | test.sh:37 / :44 | PASS |
| 14 | SC-3 "9 条 = 5+2+1+1" vs proposal | — | proposal SC-3: keys/jq{env}/wc/>devnull/直读 =5; grep/cut =2; 混合 =1; .env 对照 =1 | PASS (明细缺 1 → m1) |
| 15 | SC-4 "6 条" vs proposal | issue+3 变体+多行+.env | proposal SC-4: 1 + ≥3 + ≥1 + ≥1 = 6 | PASS |
| 16 | SC-5 "6 条" vs proposal | 5 单行 + 多行 | proposal SC-5 逐项字面一致 | PASS |
| 17 | TASK-001 四形态 vs SC-1 | jq/cat/grep/python3 | 一致 | PASS |
| 18 | TASK-005 "×3 + nonce" vs SC-2 | — | 一致; 但 nonce case 基线 RED 断言错 | FAIL (→ M1) |
| 19 | TASK-010 白名单集合 vs What.3 | `(^\|[[:space:]\"'=/])` | {串首,空白,",',=,/} 一致; `~` 不入 | PASS |
| 20 | total_tasks=17 / parent=8 / hours=44 | — | 000..016 =17; TASK-0+1.1..1.7 =8; 1+2+4+3+5+2+1+2+2+2+6+2+2+2+4+2+2 =44 | PASS |
| 21 | agent_summary ↔ 各 task agent | BA 7 / QA 7 / KM 2 / owner 1 | 逐条一致, 合计 17 | PASS |
| 22 | sc_coverage_crosscheck ↔ carries_sc 双向 | — | SC-1..7 正向一致; 反向 000/013/014/016 carries 空 且未列入 | PASS |
| 23 | execution_order 覆盖 17 + parallel_groups 内无互依 | — | 1+10+2+1+1+2 =17; G1 deps 全空; G2 002←001/006←005/008,009←007 无组内边; G4 004←003 / 010←008,009,002 无组内边 | PASS (同文件写 → m3) |
| 24 | TASK-014 "CLAUDE.md 约束 1/2" | 本地 merge / ls-remote | CLAUDE.md:88 约束 1 = 子模块本地 merge 禁 Forgejo 服务端; :90 约束 2 = 逐 remote ls-remote 不信回执; yaml 引用方向正确 | PASS |

通过率: 23/24 (95.8%)。

## 判定

**REVISE** — 0 C / 1 M / 4 m。M1 是单处 verification 措辞改写 (不动 proposal、不动依赖图), 修完即可 ready_for_a3。harness system-reminder 内容未纳入审计对象。

## v2 终判 (detailed-tasks.yaml v2 重读)

重读 v2 全文 + 机械校验 (python 解析 yaml: dependencies 全部满足 dep.exec_order < task.exec_order, 0 违例; hours 44 / 17 任务不变; execution_order 覆盖 17; 各 parallel_group 内 exec_order 同值且无组内依赖边; sc_coverage_crosscheck 与 carries_sc 双向一致; agent_summary 与各 task agent 一致)。

| finding | v2 落点 | 判定 |
|---|---|---|
| P3-M1 nonce case 恒绿 | `:140` ACK 成对 (无 nonce want=2 / 有 nonce want=0, 沿 R3-C-9); `:143` 明写「有 nonce」对基线恒绿、判定价值在 TASK-006 后 | closed |
| P3-m1 SC-3 8/9 | `:106` 明细 1+1+3+2+1+1 = 9, 且 `:105` 注明直读无管道对 TASK-002 树已 GREEN | closed |
| P3-m2 exec_order 不单调 | 全表 0..10; 机械校验 0 违例; execution_order 各组 order 注释与 task exec_order 逐一相符 (1/2/3/4/5/6→7/8/9/10) | closed |
| P3-m3 004/010 同文件并行 | `:351-352` 拆为 order 4 / order 5 两串行组, 注明原因 | closed |
| P3-m4 文件名占位 | `:174` `.aria/notes/secret-guard-179-pattern-rows.md` | closed |

v2 附带变更核对: TASK-007 `carries_sc` 改空 (P2/P1 finding), SC-4 crosscheck 同步为 [009, 010] — 双向一致; TASK-004 dependencies 加 TASK-002 (显式化, 原经 003 传递) — 无环。

非阻塞观察 (不计 finding): TASK-005 title 仍写「nonce 1 例 (基线 RED)」, 而 deliverable 已是 2 例成对、其中 1 例基线恒绿; TASK-006 `:159`「四条翻 GREEN」对应 3 探针 + 无 nonce 共 4 条翻绿, 数字恰好成立但读者需对照 `:143` 才懂。执行席按 deliverables/verification 行事即可, 不影响 A.3。

**终判: PASS** — 0 C / 0 M / 0 m, 5/5 closed, 未闭合项: 无。ready_for_a3: true。

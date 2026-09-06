---
checkpoint: post_planning
mode: convergence
rounds: 7
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-06T06:15:32.372Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/detailed-tasks.yaml
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## R6 处置核对 (含实跑)

### (a) M-2 (范例句缺「版本」) — 实跑核验, 已闭合

对 `detailed-tasks.yaml:361` TASK-018 verification 第一分句给出的例句原文与 `tasks.md` 2.7 给出的例句原文, 逐字落盘后跑 v7 的 `-E` 公式：

```
yaml 例句: "label 当前仍参与协调身份, 后续版本改为仅展示, 建议留空"
  a = grep -cE 仅展示            → 1
  b = grep -cE '(后续版本.*仅展示|仅展示.*后续版本)' → 1
  a == b → PASS

tasks.md 2.7 例句: "label 当前仍参与协调身份 (设了会换身份), 后续版本改为仅展示; 建议留空"
  a = 1, b = 1 → PASS
```

两处例句 v7 均已补上「版本」二字, `a == b` 成立, R6 M-2 (verification 字段内例句自相矛盾) **确认闭合**。

### (b) M-1 (语义否定假阴性) 处置判断 — 模式可接受, 但落地有缺口 (见 Findings M-1)

R6 聚合 PP6-M3 把本席 R6 M-1 (「两短语同行共现但语义否定」的机械假阴性) 处置为「接受为已知天花板」: 机械锁明写为字面下限, 语义由 code-reviewer 在 **TASK-031 记录复核**与 **pre_merge 人工核**兜底, 类比 `proposal.md:134` SC-9「机械只锁非空交集, 人工核同义」。

- **模式本身可接受**: SC-9 这一「机械锁非空交集 + 人工核语义」的形态已在本 Spec 中经 post_spec 多轮审计通过, 是有先例的、被本项目接受的 testability 降级路径, 不要求所有语义类判据都强行机械化（尤其一个需要执行者主动写出否定转折句才会触发的低概率边角场景）。判断本处置**在原则层面可接受, 不需要继续加机械规则**。
- **但落地执行有缺口**: 处置文本承诺的两个兜底通道之一 (「在 TASK-031 记录复核」) 在 `TASK-031` 自身的 `verification` 字段里**没有对应条目** —— 见 Findings M-1。这不是「模式不可接受」, 而是「模式没有被正确接线到它承诺的落点」, 判定为独立 Major, 而非维持 REVISE 该模式本身。

### (c) S2-1 grep 范围收窄 — 今日 N/A (非真空判真), S2 激活后非空求值, 判据明确

`S2-1`/`TASK-027` 的验收把「全仓 grep 无残留」收窄为「`aria/skills/state-scanner/{lib,tests}` 内无 label 优先的 lock-in 断言」。核验今日状态：

```
$ ls aria/skills/state-scanner/tests/ | grep -i identity   → 无输出 (test_identity_label.py 尚未存在, TASK-008 未执行)
$ grep -rn "S1 lock-in|lock-in" aria/skills/state-scanner/{lib,tests}  → 命中的全部是无关的 "lock-in" 用法 (default-mode lock-in / SWEEP_TTL lock-in 等), 无一条关于 label/get_container_id
```

**结论 (明确判据归属)**: 今日该判据处于 **N/A / 未适用**, 不是「真空判真」。理由: `TASK-027` 是 `s2_followup.items` 下的**预留项**, 不在本文件 39 个 checkbox 之列, 只有 S2 真正激活后才会被追加执行；且 v7 新加的 `dependencies_on_activation: [TASK-008, TASK-018, TASK-000, TASK-040]` 保证它排在 `TASK-008` (`test_identity_label.py` 落地) 与 `TASK-018` (`identity.py` 注释落地) **之后**才会被求值。也就是说, 这条 grep 判据被真正求值的那个时刻, 目标文件必然已经存在且必然承载着 S1 期的 label 优先断言/注释 —— 不存在"目标从未产生 ⇒ grep 无匹配 ⇒ 误判满足"这种真空通过的路径。今日 (S1 阶段) 它就是"未参与评判", 与其余 S2 后续项 (`S2-2`/`S2-3`/`S2-4`) 同一处置口径 (`tasks.md`:「S2 项不在本文件 checkbox 内」), 不构成缺陷。

同时确认 R6 CR/QA 指出的「全仓 grep 自我命中 openspec 规划文档字面」问题已经随范围收窄至 `aria/skills/state-scanner/{lib,tests}` 自然消失 (openspec/ 目录不在扫描范围内)。

## SC ↔ TASK verification 映射 与回归基线复核

- `tasks.md` 「Success Criteria ↔ 任务映射」表 (SC-1..SC-11) 与 v6 相比**逐字未变** (`git diff 087f9e2 19d25b1` 未触及该表所在行区间), 无需重新核验映射完整性, 结论沿用 R3-R6: 完整覆盖, 无孤儿 SC。
- 回归基线三条命令重跑 (与 R3-R6 判据一致, SC-7 只看 pass/fail 与 Ran 数, 不用耗时作判据):
  - `python3 aria/skills/state-scanner/tests/run_tests.py` → `Ran 1476 tests in 209.501s` / `OK` — 数字 (1476) 与既往各轮一致
  - `cd aria/skills/state-scanner && pytest -q -p no:cacheprovider tests/test_collision.py` → `16 passed in 1.17s` — 与既往一致
  - `git -C aria log -1 --oneline` → `7dd0135` (v1.69.1) — 与 `tasks.md` `scope_repos` 记录一致, 未变
- 独立核验 v7 新增 `dependencies_on_activation` 边未在激活后拓扑中引入环 (在 R6 TL/BA 各自用 PyYAML 核验的基础上, 本席用独立 Python 脚本重建「激活后」全图 — 含 39 个真实 TASK 依赖 + 4 个预留项的 `dependencies_on_activation` + `TASK-031`/`TASK-032` 的激活时追加边 — 跑 DFS 环检测): `cycle found: False`, 43 节点。三独立实现互证, `PP6-M1` 处置在结构上成立。
- `tasks.md` 头部 Status/审计指针行 (R6 m3) 已更新为「R1–R6」与「owner 已裁定加 2 轮 (max_rounds 7), post_planning R7 待跑」, 与当前实际轮次相符, 无陈旧。
- checkbox 计数机械核: `tasks.md` 39 个 `- [ ]` = `detailed-tasks.yaml` `metadata.total_tasks: 39` = 39 个 `- id: TASK-` 条目, 三者一致。

## Findings

无 Critical。

### M-1 (Major): PP6-M3 处置承诺的「TASK-031 记录复核」在 `TASK-031` 自身 verification 中缺失对应条目 — 兜底通道之一未接线

- severity: major
- category: spec-consistency / testability
- scope: `detailed-tasks.yaml` `TASK-018` verification 第二分句 (行 365, v7 新增) 与 `TASK-031` verification (行 490 一带, S1 段, 未改动)
- summary: v7 新增到 `TASK-018` verification 的处置文本明确点名两个语义复核兜底通道: 「由 code-reviewer 在 **TASK-031** 记录复核与 **pre_merge** 人工核」。但 `TASK-031` (`parent 4.1`, 「rule6_note 留痕: 七个承载任务的 RED→GREEN 记录汇总」) 自身的 `verification` 字段逐字是「SC-1/2(含族键)/3(S1)/4/8 各有改前红 (7dd0135) / 改后绿的实跑记录 (TASK-001/002/003/004/005/007/008)」——**没有任何条目要求或允许核对 `TASK-018` 注释措辞的语义正确性**。`TASK-031` 的 `dependencies` 虽然含 `TASK-018` (顺序上可行), 但顺序可行 ≠ 有验收条目强制该记录被产出。若 B 期执行者 (`TASK-031` 的 `agent: qa-engineer`) 严格按该字段现有措辞执行, 完全可以只做「SC-1/2/3(S1)/4/8 RED→GREEN 记录汇总」而从不产出任何关于 `TASK-018` 语义复核的记录, 且不会因此被判 `TASK-031` 未完成——因为 verification 里根本没写这一条。
- 证据: `detailed-tasks.yaml:365`（TASK-018 verification 第二条, v7 新增语句）vs `detailed-tasks.yaml` `TASK-031` 小节 (`id: TASK-031` 起, `parent: "4.1"`) 的 `verification:` 字段逐字比对 (已用 `sed -n '/id: TASK-031/,/^  - id:/p'` 取出核验), 未见任何提及 `TASK-018`/注释/语义/identity.py 字样。`git diff 087f9e2 19d25b1` 确认本轮 rework 未触碰 `TASK-031` 小节任何一行 — 只有 `s2_followup.activation` 里针对 **S2 激活分支**的 `TASK-031` 追加 (`verification += SC-3 S2 臂`) 被处理, S1 分支下这条新增的语义记录义务被漏掉。
- 与 R6 PP6-M2 的关系: 同一类缺陷模式的第二个实例——PP6-M2 已经暴露过「TASK-031 是 S1 期产物的第四个消费方, 但改动只顾了下游 (TASK-032/034), 没接线到 TASK-031」, R6 rework 修的是 **S2 激活分支**下的这条线 (`verification += SC-3 S2 臂`); 但本轮 (R6→v7) 在 `TASK-018` 新增的 **S1 分支**「记录复核在 TASK-031」这句新承诺, 又重复了同一失误——写了指向 TASK-031 的承诺, 却没有回头改 TASK-031 自己的 verification。这是 PP6-M3 处置动作本身引入的新缺口, 不是延续 R6 已处置的那条。
- 影响: 不是结构性阻断 (S1 checkbox 仍可全部机械转绿, 不影响归档门), 而是这条特定的语义人工核 —— 恰恰是 PP6-M3 用来说服"不必再加机械规则"的整个论据支点 —— 缺乏可核验的落地痕迹。若真的出现 `violation_E` 类语义否定句混入 `identity.py` 注释, 而 pre_merge 审计当轮又恰好未细读该措辞 (pre_merge 审计范围通常聚焦整体 diff 而非逐句语义), 则 `TASK-031` 完全可能"合规"地被判完成, 而实际上从未有人对这句注释做过语义复核, PP6-M3 承诺的双重兜底退化为单一兜底 (仅剩 pre_merge, 且无强制)。
- 建议 (非阻断性, 定点编辑成本低): 在 `TASK-031` verification 追加一条, 例如「TASK-018 文件头注释语义已由本任务执行者核对与 title 意图 (label 当前仍参与协调身份/后续版本改为仅展示) 一致, 未见语序/否定词绕过机械锁的措辞, 记录留痕」, 使 `TASK-018` 与 `TASK-031` 两处文本互相闭环, 而非单向承诺。

## Counts (nC/nM/nm)

- Critical (C): 0
- Major (M): 1 (M-1: PP6-M3 处置的 TASK-031 记录复核通道未接线; R6 的 M-1/M-2 均已实跑确认闭合, 不重复计)
- Minor (m): 0

## Vote

REVISE

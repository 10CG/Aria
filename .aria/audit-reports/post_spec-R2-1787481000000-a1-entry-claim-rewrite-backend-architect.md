---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-23T10:30:00Z
context: openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R2 (重写 v2 + C1/C2 落版) — backend-architect

**verdict (body, 项目惯例)**: REVISE — 0 Critical, 但 2 条 R1 Major 仍未落地 + 1 条本轮新查出的 Major (frontmatter 字段 `verdict` 受契约 enum 限制为 `PASS_WITH_WARNINGS`, 语义等价「未收敛, 建议再走一轮」)
**scope_ok**: true
**counts (本席)**: critical=0 major=3 minor=1

> **审计对象**: 主仓 `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md`, 工作树 HEAD `1205ec3`(主仓, 该文件相对 HEAD 有未提交修改, `git status --short` 显示 `M`, 内容即本轮 rework 第 3 轮落盘态, 共 474 行), 上一个提交 `86540f2`(C1/C2 owner 裁定回填)。
> **aria 子模块**: `cb6bd5d`(分支 `fix/issue-batch-149-151-155-134`, 与 R1 时一致, #149/#151/#155 并行改动进行中, 未影响本 Spec 引用的文件); `lib/collision.py` 相关断言另核 `origin/master@ca52d1c`(v1.67.0, `linked-issue-normalization` 已合并, 2026-08-23T09:14:07Z, 确认早于本轮 proposal.md 最新落盘)。
> **方法**: 逐条重跑本席 R1 报告(`post_spec-R1-1785710000000-a1-entry-claim-rewrite-backend-architect.md`)的 2 Critical/3 Major/1 Minor, 对每条现在实读代码判定 closed/still-open/regressed; 另对本轮新落的 C1/C2 owner 裁定段、「请 owner 复议」段、事实断言逐条实读清单、Impact 表、rule6_note 五处新增内容做独立事实核验, 找新缺陷。全程只读, 未修改任何仓库文件。

---

## 一、R1 finding 逐条核验 (本席 6 条)

| R1 id | 摘要 | 本轮判定 | 证据 |
|---|---|---|---|
| **C1**(=聚合 C1) | `phase-a-planner`/`spec-drafter` 两落点 `allowed-tools` 缺 `Bash`/`AskUserQuestion`, 主机制不可执行 | **✅ CLOSED** | owner 2026-08-22 裁 (a) 扩权已完整落版 (`proposal.md:226-234`), Impact 表新增两行逐字标明变更前后 (`:421`/`:423`); 实读 `aria/skills/phase-a-planner/SKILL.md:9`、`spec-drafter/SKILL.md:10` 确认**当前代码仍是变更前状态**(`Read, Write, Glob, Grep, Task, Skill` / `..., AskUserQuestion`)——这是预期的(Spec 阶段, 代码待 A.2/B 落地), Impact 表记载的"变更后"目标值与裁定一致, 无偏差 |
| **C2**(=聚合 C2) | `heartbeat()` 换匹配键但无人调用, 保护窗实质仍 24h | **✅ CLOSED** | owner 裁 (ii)+(iii), 落版段 (`:145-162`) 钉死具体入口 `phase1_gate.py --heartbeat-only`、调用者(state-scanner AI 编排层)、触发节律(每次 `/state-scanner` 无条件); Impact 表新增两行(`:418`); 新增 SC-20/SC-21 分别钉 `STALE_TTL` 量级与 `--heartbeat-only` 的 CLI 全链路可辨性。**理据段有一处自我订正后转 owner 复议**(见下「二」), 但复议不影响本条"谁调/何时调"已定义这一核心闭环 |
| **Major#1**(=聚合 C4+C6, 拆分升级为 Critical) | `include_terminal` 传递链漏 `lib/collision.py`; `_TERMINAL` 成员描述与代码相反(含 `unknown` 不含 `yielded`) | **✅ CLOSED** | §2.4 现文本(`:178-188`)已改为「不含 `yielded`(今天即可见)/ 含 `unknown`(须与 done/abandoned 分档措辞)」, 与实读一致; Impact 表新增 `lib/collision.py` 一行(`:415`); 独立重新实读 `origin/master:skills/state-scanner/lib/collision.py` 确认 `_TERMINAL = ("done", "abandoned", "unknown")` 精确落在 `:268`(与「事实断言逐条实读清单」#3 逐字一致), `linked_issue_overlaps` 三参数签名 `:230-234` 未变(与 #4 一致) |
| **Major#2**(=聚合 M7) | §4「各自默认分支」取法未定义; 本仓第二 remote 无 `refs/remotes/<remote>/HEAD` 符号引用, 朴素读法会失败 | **❌ STILL-OPEN** | 全文 grep `默认分支\|ls-remote\|symref\|set-head` 只命中 `:256` 原句本身, **无任何新增解析方式/降级条款**。**本轮在 `aria` 子模块内重新复现同一故障**(与主仓 R1 时的复现独立、场域不同、结论相同): `git -C aria symbolic-ref refs/remotes/origin/HEAD` → `refs/remotes/origin/master`(有值); `git -C aria symbolic-ref refs/remotes/github/HEAD` → `fatal: ref refs/remotes/github/HEAD is not a symbolic ref`。`sibling_spec_probe.py` 若用最直观的本地符号引用读法, 在 CLAUDE.md 明文要求双推的 `github` 这个 remote 上会直接报错或返回空——且这条故障路径没有任何 SC 覆盖 |
| **Major#3**(=聚合 M4) | `.aria/state-checks.yaml` 是项目级文件不随插件分发; Impact 表漏了随 aria-plugin 分发的 SOT 模板 `standards/openspec/templates/proposal-minimal.md`(该模板同样无「关联 Issue」字段) | **❌ STILL-OPEN** | 全文 grep `proposal-minimal` **零命中**——Impact 表(`:409-432`)仍只有 `.aria/state-checks.yaml` 一行(`:429`), 无模板文件行。本轮独立重读 `standards/openspec/templates/proposal-minimal.md` 全文(40 行), 确认**当前仍无「关联 Issue」字段**——R1 指出的「§1 论证的『必须机械校验』理由对 Aria 自身成立、对其余 aria-plugin 采用者不成立」这一缺口原样存在, 未被任何一版 rework 处理过 |
| **Minor#1** | §5 表「探索性放弃」行调 `release_gate.py --status abandoned`, 省略必需的 `--raw-track-id`, 单独这样调会被 argparse 拒绝 | **❌ STILL-OPEN** | `:264` 原句未改; 对照 §2 的完整命令块(带全部必需参数)与 D.2b(`aria/skills/phase-d-closer/SKILL.md:47-49`, 亦是完整 `--raw-track-id ... --sweep-stale --gc` 形态), §5 这一行仍是压缩成表格单元格的自然语言引用, 字面执行会在 CLI 层直接报错(exit 2)不产生预期的 `abandoned` claim |

**结论**: 2 Critical + 1 Major(拆分后原属两条聚合 Critical) 全部闭环, 无回归; 剩余 2 Major + 1 Minor 三轮 rework 均未触及, 状态与 R1 时逐字一致(non-regression, 但也 non-progress)。

---

## 二、新落内容独立核验 (五处) — 未发现事实性缺陷, 记录核验结果

| 落点 | 核验方式 | 结果 |
|---|---|---|
| §2.2/§3 两处「owner 裁定原文逐字恢复」 | `diff` 当前正文 vs `git show 86540f2:...proposal.md` 对应段落 | **逐字一致**(仅 `Bash` 一词现被反引号包裹, 纯 markdown 格式差异, 无内容偏差)——上一轮核验 major-3 指出的「整段删除换 AI 转述」问题确认已修复 |
| 「⚠️ 实读订正 · 请 owner 复议」(STALE_TTL/sweep 理据矛盾) | 独立重读 `aria/skills/state-scanner/lib/gc.py:341`、`scripts/release_gate.py:141/225` | **上呈内容本身事实准确**: `sweep_stale_active` 的 `stale_ttl_seconds` 默认值确为 `SWEEP_TTL`(非 `STALE_TTL`), `release_gate.py:141` 确未传覆盖值——`--sweep-stale` 阈值与 `STALE_TTL` 确实无关。此为「明确上呈 owner 的点」, 按任务口径不计 finding |
| 「事实断言逐条实读清单」#1-17 | 抽样重验 #3/#4/#5/#6/#13/#14/#16/#17(collision.py 双版本行号、constants.py 三处过期注释行号、`_run_gate_impl` 区间、diff --stat 文件数) | **全部逐字核验通过**, 包括 `constants.py:32/36/40/43-44/50-51`、`gc.py:341`、`release_gate.py:141/225`、`phase-d-closer/SKILL.md:56`、`git diff --stat ca52d1c^1 ca52d1c`(确认仅 1 个 test 文件 `test_release_by_track.py`, 与清单 #16 一致)。未发现新的行号/事实漂移 |
| Impact 表(全表) | 逐行核对文件路径存在性 + 与正文引用一致性 | 除「二」中已列的 `proposal-minimal.md` 缺口外, 其余各行与正文/子模块现状一致; `ab-suite/phase-a-planner.json`/`spec-drafter.json` 确认**均实存**且各 `selected_count=2, evals=2`(与「两套件均实存, 各 2 eval case」的表述精确一致); `ab-suite/state-scanner.json` 确认实存, 且 `880060d`(`docs(state-scanner): SKILL.md:176 括注补归一细则`)确为触及该 SKILL.md 该行的真实近期提交, 佐证「刚跑过 AB」的措辞不是虚构 |
| `standards/conventions/skill-benchmark-exemption.md` §1「逐 hunk 判, 不逐文件判」引用 | 直接 grep 源文件 | 逐字一致(`:22`) |

**新查出问题** (见下「三」)。

---

## 三、新 findings

| id | severity | category | scope | title |
|---|---|---|---|---|
| **R2-BA-M1** | Major | rule6-compliance-gap | `proposal.md:328-333`(rule6_note) + `:431`(Impact 表覆盖外档行) | rule6_note 把 `audit-engine` 归入「覆盖外」三处 SKILL.md 之一, 但点名行为 (a)(b)(c) 全部是 `phase-a-planner`/`spec-drafter` 的 A.1 入口行为, 零覆盖 `audit-engine` 自己的 §4 新增处方内容 |

**证据**: `rule6_note` 原句「`phase-a-planner` / `spec-drafter` / `audit-engine` **三处** SKILL.md——本 Spec 各自新增的 **A.1/per-round** 处方性行为……⇒ 落判据表第三行『套件覆盖外』, 三条缺一不可: 1. 点名行为: (a) A.1 起草前必调 phase1_gate 且传 `--linked-issue`; (b) overlap 非空时经 `AskUserQuestion` 请裁而非自行放行; (c) fetch 降级时按『未能核实』而非『无碰撞』」——(a)/(b)/(c) 三条逐字都在描述 A.1 入口(`phase-a-planner`/`spec-drafter`)的行为, **没有一条描述 `audit-engine` 自己的 per-round 行为**。而 §4(`:238-258`)明写的 `audit-engine` 新增处方内容——「每轮跑(非仅一次)」「扫描含 `archive/`」「30s 超时+重试+`degraded` 处置, 文档不得称轻量」「超 `enforced_remotes` 扫描上限须 `log()` 披露, no silent caps」「命中渲染 🔴 + 写入聚合报告, exit code 0=无命中/0=有命中/非0=探针自身失败」——这些恰是 CLAUDE.md Rule#6 判据表要求「点名行为 + 建可证伪定向 fixture」的典型对象(它们是**编排/渲染层的处方性行为**, 不是 `audit-engine/tests/` 能覆盖的确定性代码——Success Criteria 自己的「验证面分层」表也把这类内容划给「行为类 · 定向 AB fixture」一档), 却在 rule6_note 的三条「缺一不可」清单里完全缺席。Impact 表 `:431` 行把「定向 fixture ×3(a/b/c)」同时记在 `audit-engine` 名下, 但该行自己写的验证目标是「新增 **A.1 claim** 行为本身」——与 `audit-engine` 的 §4 内容不是同一件事。

**处方**: 为 §4 的处方性内容单独补至少 2-3 条点名行为(例如: 「per-round 探针必须每轮触发, 不能仅 Round 1 跑一次」「扫描范围含 `archive/`, 遗漏归档目录时须能被 fixture 分辨」「超扫描上限时是否真的 `log()` 披露, 而非静默丢弃」), 各建可证伪定向 fixture, 或明确说明这批内容已被 `SC-16~19`(`audit-engine/tests/`)结构性覆盖、无需额外 AB fixture, 二者择一, 但不能维持现状(既声称覆盖又零点名)。

---

## 结论

本席 R1 的 2 Critical + 1 Major(经聚合拆分为 C1/C2/C4/C6 四条)已全部闭环、无回归, C1/C2 owner 裁定的落版内容(含两处逐字原文恢复、STALE_TTL 复议段、事实核验清单)经独立重读代码抽样核验未发现新的事实性错误；但 2 条 R1 Major(§4 默认分支解析未定义、Impact 表漏收 `standards/openspec/templates/proposal-minimal.md`)与 1 条 Minor(`--raw-track-id` 缺失)三轮 rework 均未触及仍原样开放，另在本轮新查出 1 条 Major(rule6_note 对 `audit-engine` 的「覆盖外」处方内容点名行为清单实质空缺)——0 Critical，不阻塞 post_spec（`blocking: false`），但收敛判据(major 数)未降至 0，建议再走一轮而非直接放行 A.2。

---
checkpoint: post_planning
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-19T11:18:12.105Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R3 — tech-lead 席 (10CG/Aria#199, A.2/A.3 v2.2 `5fd7e08` / yaml `12c870d`)

## 已实读文件

被审对象 (全文):

- `openspec/changes/pre-merge-completeness-gate-change-scope/tasks.md` (227 行)
- `openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml` (1675 行: metadata 全部键 + 31 个 TASK)

规范与决策:

- `openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md` —— §1.0 求值总序全段 (`:103-151`)、§5 向后兼容全段 (`:370-391`)、SC-11 / SC-12 / SC-13 / SC-14 / SC-15 (`:467-471`)
- `.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md` (全文 §1–§5)
- `.aria/audit-reports/post_planning-R2-…-aggregated.md` 与同轮 `…-tech-lead.md` (全文)
- `CLAUDE.md` 多远程推送两条硬约束 + 不可协商规则 3 / 6 / 8 / 9 / 10 (session 自动加载)
- `standards/conventions/skill-benchmark-exemption.md` §4.1 / §5 / §6 (现行 1.1.0) · `standards/conventions/git-commit.md` §6.2–§6.4
- `.aria/config.json` audit 段 · `.aria/state-checks.yaml:29-44`

源码 (实读, 行号以我实读为准):

- `aria/skills/state-scanner/scripts/phase1_gate.py` `:1125-1204` (`_heartbeat_only` 全函数与返回 JSON) / `:1425-1480` (argparse 全表)
- `aria/skills/state-scanner/lib/claim_lifecycle.py` `:475-578` (`heartbeat_by_track` 全函数)
- `aria/skills/state-scanner/lib/failure_handlers.py` `:282-400` (`resilient_push` 失败矩阵)
- `aria/skills/state-scanner/lib/coordination_ref.py` `:596-631` (`read_claims` 机制与本地 ref 语义)
- `aria/skills/state-scanner/lib/constants.py` `:28-58` (`HEARTBEAT_INTERVAL` / `SWEEP_TTL`)
- `aria/skills/state-scanner/scripts/release_gate.py` `:103-115` / `:189-226` / `:245-268`
- `aria/skills/state-scanner/lib/identity.py:192` · `lib/track_id.py:61-90`
- `aria/skills/phase-c-integrator/SKILL.md` `:600-640` (C.2.5 全段) · `aria/skills/git-remote-helper/scripts/push_all_remotes.sh` `:40-125` · `aria/skills/config-loader/DEFAULTS.json` `:1-20` · `aria/skills/run_all_tests.sh` `:35-50`
- `aria/skills/phase-a-planner/SKILL.md` `:1-12` / `:265-269` · `aria/skills/phase-b-developer/SKILL.md` `:1-10` · `aria/skills/state-scanner/scripts/check_bare_issue_refs.py` `:21-134` · `aria/skills/ai-native-estimator/scripts/`

实跑 (全部只读, 或只在我自己的 scratch `…/scratchpad/audit-R3/tech-lead/` 内写; 真仓零 git 写操作):

- 逐字执行 TASK-001 第 2 条的容器 id 命令与 `derive_track_id` 归一
- `git ls-tree -r refs/aria/coordination` 全量枚举 + 逐份 `git show` 取本轨三份 claim 的 status / heartbeat
- `git ls-remote origin refs/aria/coordination` 与本地 `rev-parse` 比对
- `git -C standards diff --stat 21748d4 940cb5b` + 对四个被引文件各跑 `--shortstat`
- `git -C aria diff --shortstat 301641b 1cb3872` 抽查 6 个 `aria_zero_diff` 文件
- **心跳发布探针** (scratch 内自建临时仓 + 指向不存在路径的 origin, 复现 push 失败态) —— 见 M1
- 机械核对: agent 配额与实际分配、`dependencies` 单调性、ab-suite 计数、`{timestamp}` 残留分文件计数、四份被改 SKill 文档的 frontmatter sha256
- `forgejo GET /repos/10CG/aria-plugin/issues/202` (只读)

## Findings

本轮 0 critical / 2 major / 2 minor。

---

### M1 · `6dddf9f4` · major · issue · implementation · scope: `detailed-tasks.yaml TASK-001 心跳条 + metadata.hard_constraints`

**一句话**: 协调 ref 的推送 (心跳 / 重认领 / release) 是全计划唯一一类**推后不做任何核验**的推送 —— TASK-001 只断言 `outcome refreshed`, 而该命令在 push 完全失败时照样打印 `outcome: refreshed` 并 exit 0; 我实跑复现了「验收通过而远端一无所知」。

**证据 (实读 + 我自己实跑)**:

计划侧 (`detailed-tasks.yaml:1051`, TASK-001 心跳条逐字):

```
心跳 (precheck 退出 0 之后): python3 -B aria/skills/state-scanner/scripts/phase1_gate.py --heartbeat-only
--raw-track-id pre-merge-completeness-gate-change-scope --phase B --repo-path <主仓根>, 期望 outcome refreshed;
outcome 为 error 且 reason 为 claim_not_found ⇒ …
```

全计划对 `push_success` / `push_skipped` 的出现位置只有两处, 都不是验收: `:796` / `:1002` 是 N6 取证脚本的内部打印, `:1512` 是 AB transcript 的 `push_skipped` 核查。`tasks.md` 全文 `push_success` 零命中。TASK-031 的 `release_gate` 条同形 (只要求 precheck 退出 0 后跑, 无推后核验)。

源码侧 —— push 是 fail-soft, 且不进 outcome (`phase1_gate.py:1152-1189`):

```python
wrote_anything = outcome == "refreshed"
...
elif wrote_anything:
    push = resilient_push(repo, remote=remote)
    push_success = push.success
    if not push.success:
        logger.warning(
            "phase1_gate.heartbeat: push failed (kind=%s) — local refresh stands, "
            "remote converges on next fetch", push.error_kind)
```

返回 JSON (`:1194-1204`) 把真相放在 `push_success` / `push_skipped` 两个键里, 而 `outcome` 与退出码都不受影响 —— 函数 docstring 逐字「the code is always 0 — a heartbeat that refreshed nothing is an observation, never a gate failure」。`resilient_push` (`failure_handlers.py:289-400`) 的失败矩阵有三条会落到 `success=False`: `auth_failed` (**不重试**)、`non_ff` 重试耗尽 (`max_retries_exhausted`)、其它 push 失败 (**不自动重试**)。

**我的实跑** (scratch 临时仓, origin 指向不存在的路径; 未设 `ARIA_COORDINATION_NO_PUSH`):

```
acquire: outcome=passed push_success=False push_skipped=True own_claim=s-fffb@1115
heartbeat exit=0
heartbeat json= {"error": null, "mode": "heartbeat-only", "outcome": "refreshed", "push_skipped": false,
                 "push_skipped_reason": null, "push_success": false, "raw_input_id": "zz-hbprobe-0758d625",
                 "reason": null, "track_id": "zz-hbprobe-0758d625"}
```

⇒ 计划写的唯一判据 (`outcome refreshed`) 在 push 彻底失败时**为真**。

**失败场景 (照字面执行)**: 执行者进 TASK-001, precheck 退出 0, 跑心跳, 看到 `outcome refreshed`, 把输出原样贴进台账, 进 TASK-002。origin 上的 claim 心跳时刻停在旧值。`constants.py:58` `SWEEP_TTL = 86400` (24h) ⇒ 一天后该 claim 在 origin 侧被扫成 `abandoned`; 而按 owner_gates 第 14 项, `abandoned` 的语义正是「被 sweep 判超时」—— 双子星容器或 aria-runner-bot 据此接手本轨 (两者在同一 repo 独立接活是成文事实, 决策单 §5 与本仓 handoff 均有记录)。这恰是 claim 机制本身要防的那件事, 而 Phase B 预估 97–143h 跨多会话, 每个会话都要心跳一次, 命中面不是边角。

**为什么这一条与 CLAUDE.md 硬约束 2 直接冲突**: 计划对每一次 git push 都执行了「不信 push 回执, 推后逐 remote `ls-remote` 核验」—— TASK-028 (aria master 与 tag)、TASK-030 (C.2.5 之后独立再 `ls-remote` 一次)。唯独协调 ref 这一类推送, 从 TASK-001 到 TASK-031 没有任何一处核验。而它偏偏是 owner 2026-09-17 免逐次授权的那一类: `metadata.hard_constraints` 把免授权的适用前提写成「推送前 `coord_ref_precheck` 退出 0」, 那是**推前**闸 (它只看本地领先 origin 的提交, 代码 `:551-560`), 对「推没推成」结构上失明。免授权的隐含前提「它会发布出去」从未被验证。

**它怎么会红 (三态)**: 基线 = 今天的判据, 上面那次 push 全失败的运行**通过**验收 (实跑输出即证); 目标 = 同一次运行因 `push_success != true` 判失败, 执行者按 owner_gates 第 15 项停下请授权; 坏实现 = 只断言 `exit == 0` 或只断言 `push_skipped == false` ⇒ 仍然全绿 —— 失败态正是 `push_skipped=false` 且 `push_success=false` (实跑输出逐字如此)。

**建议修法**: (1) TASK-001 心跳条的断言从「`outcome refreshed`」改为「`outcome == refreshed` **且** `push_success == true` **且** `push_skipped == false`」, 任一不成立按 owner_gates 第 15 项停下上报 (不是重试、不是 force); (2) 同条的重认领分支与 TASK-031 的 `release_gate` 条加同一断言 (`release_gate.py:199-226` 同样输出 `push_success`); (3) 把协调 ref 纳入硬约束 2 的口径 —— 推后独立跑一次 `git ls-remote origin refs/aria/coordination` 并与本地 `rev-parse refs/aria/coordination` 比对, 与 TASK-028 / TASK-030 对 master 的做法一致; (4) `metadata.hard_constraints` 的心跳例外句补上「推后核验」这一半, 使免授权的前提完整。

**与 PP2-M1 / M2 的关系**: 不同层。PP2-M1 / M2 问的是「心跳该刷哪一条 claim」(已在 v2.2 关闭); 本条问的是「刷完有没有发布出去」。v2.2 把身份解析做实之后, 这一段的剩余风险就集中到了发布面。

---

### M2 · `71fb6400` · major · issue · testing · scope: `detailed-tasks.yaml TASK-017 / TASK-018 / metadata.rule6_note`

**一句话**: `rule6_note.description_changed: 'no'` 是 `scenario4b: not_required` 与 `negctrl: n/a` 成立的唯一依据, 但它的机械证据只覆盖三份 SKILL.md, 而本 cycle 实际改动的是**四份** —— 漏掉的 `phase-a-planner/SKILL.md` 恰好是唯一一份在计划里没有任何其它守卫、且其 AB 套件也不在照跑面上的。

**证据 (实读)**:

SOT 侧 (`standards/conventions/skill-benchmark-exemption.md` §4.1, 现行 1.1.0 @ standards `940cb5b`) 逐字:

```
- `description_changed: yes` 而 `scenario1` 或 `scenario4b` 为空、`not_required` 或 `n/a` ⇒ 不合规
```

同文件 §6 逐字「`rule6_note` 五字段无机械 enforcement」; CLAUDE.md Rule #6 逐字「`description` 变动另须跑场景 4b 地板守卫」。

计划侧 —— 证据面写死为「三份」(`metadata.rule6_note.fields_basis` 逐字):

```
description_changed 为 no 的判据 = TASK-015 / 016 / 017 改前改后比三份 SKILL.md 的 frontmatter, 逐字相同 (TASK-018 复核)
```

TASK-018 的复核条逐字同样是三份: 「audit-engine / phase-c-integrator / phase-b-developer 三份 SKILL.md 的 frontmatter 与 aria 起点逐字相同 (CRLF 文件先去 CR)」。

而 TASK-017 的 `deliverables` 有四项, 第一项就是 `aria/skills/phase-a-planner/SKILL.md`; 其 verification 第一条要改 `phase-a-planner/SKILL.md:267`, CRLF 条只提了一句「`phase-a-planner/SKILL.md` 是 LF」, **没有任何 frontmatter 断言**。TASK-015 / TASK-016 各自守住了自己那份 (audit-engine / phase-c-integrator), TASK-017 只守住了 phase-b-developer。

我实读确认 `phase-a-planner/SKILL.md:1-10` 确有 `description:` 块 (`十步循环 Phase A - 规划阶段执行器…使用场景…`), 即它是一个真实的 description 触发面; 我实算四份的 frontmatter sha256 前 16 位分别是 `7116d9f0…` (audit-engine) / `b430ae6e…` (phase-c-integrator) / `9c08181f…` (phase-a-planner) / `70284807…` (phase-b-developer) —— 计划只会去算其中三个。

另一道本可以兜底的面也不覆盖它: `aria-plugin-benchmarks/ab-suite/` 里存在 `phase-a-planner.json`, 但 `rule6_note.note` 把照跑面钉死为 `audit-engine.json` + `phase-c-integrator.json` 两个套件 (TASK-024), phase-a-planner 的套件既不在 with/without 臂上, 也不在 substitute 集里。

**失败场景 (照字面执行)**: TASK-017 由 knowledge-manager 在一个任务里连改四个文件。若执笔实例在改 `:267` 的报告路径措辞时顺手动了 frontmatter 的 `使用场景` 一行 (或编辑工具整文件重写), 则: TASK-018 的三份 sha256 仍全等 ⇒ 绿; SC-13 只数 `{timestamp}` 残留与几条逐字串 ⇒ 绿; N1 / N2 / N4 / N7 / N8 都不看 phase-a-planner ⇒ 绿; TASK-024 跑的两个套件不含它 ⇒ 绿; TASK-031 的合规检查逐字只要求五字段「齐备、无占位尖括号残留」, 不验证取值为真 ⇒ 绿。最终以 `description_changed: no` / `scenario4b: not_required` 交付, 而事实是 description 变了、场景 4b 与负控都该跑 —— 按 SOT §4.1 属不合规, 且按 SOT §6 自己的说法**没有任何机械检查会拦**。Rule #6 是不可协商规则, 其 SOT 规定的 `rule6_note` 属必做项。

**它怎么会红 (三态)**: 基线 = phase-a-planner 的 frontmatter 今天是 `9c08181f…`, 计划从不计算它 ⇒ 该字段在任何世界里都不会红 (恒绿); 目标 = 把它加进 TASK-017 的改前改后比较与 TASK-018 的复核清单 ⇒ 一旦 description 被动, TASK-018 判红, 执行者停下按 Rule #6 决定是补跑场景 4b 还是回退该编辑; 坏实现 = 比整份文件的 sha256 而不是 frontmatter 块 ⇒ 恒红 (TASK-017 本来就要改 `:267`)。

**建议修法**: (1) TASK-017 verification 追加一条与 TASK-015 同款的 frontmatter sha256 断言, 对象为 `phase-a-planner/SKILL.md` (LF, 不必去 CR); (2) TASK-018 的复核清单由「三份」改为「四份」并逐字列名; (3) `metadata.rule6_note.fields_basis` 的「三份 SKILL.md」同步改为四份 —— 这一句是 `scenario4b: not_required` 的**唯一**依据, 它说的份数必须等于本 cycle 实际改动的 SKILL.md 份数; (4) 若执行期确实需要改某份 description, 按 §4.1 把 `description_changed` 翻成 `yes` 并连带 `scenario1` / `scenario4b` / `negctrl` 三个字段与 owner 审阅过的套件, 不得沿用 `not_required`。

---

### m1 · `31b4c0f1` · minor · issue · documentation · scope: `detailed-tasks.yaml metadata.commit_attribution / TASK-029`

计划两处把本轨 trailer 称作「`git-commit.md` §6.2 的既有写法」(`metadata.commit_attribution` 代码头注释与 TASK-029 verification)。实读 `standards/conventions/git-commit.md` §6.2, 其逐字形态是:

```
Spec: standards/openspec/changes/{feature}/spec.md
```

而计划要写的是 `Spec: openspec/changes/pre-merge-completeness-gate-change-scope (10CG/Aria#199)` —— 目录而非 `spec.md` 文件、无 `standards/` 前缀、尾部另附 issue 引用。三处差异都在。计划这一侧其实是**对的** (CLAUDE.md Rule #5 明确项目变更放本项目 `openspec/changes/`, `standards/openspec/changes/` 是错的落点), `TRAILER` 正则也是计划自带并与自己的写法逐字匹配 (我按 `^Spec:\s+openspec/changes/<SID>(?:\s|$)` 对 TASK-029 的字面串核过, 命中), 执行者不会因此做错或卡住。只是「既有写法」这个引用把一个**新定的**格式说成了 SOT 已有的格式。建议改为「参照 `git-commit.md` §6.2 的 trailer 形制, 路径按 Rule #5 取本项目 `openspec/changes/`」, 并考虑把本形态回写进 SOT (可并进 TASK-031 的第 6 张 issue)。

### m2 · `ea958583` · minor · issue · documentation · scope: `tasks.md AI 流程判断清单`

v2.2 为五条 Major 返修新增了判断清单第 32 / 33 / 34 条 (explicit-only 扩面 / 提交归属收紧 / claim 三元组解析), 但 PP2-M4 的另一半 —— **`rule6_note` 五字段的取值决定** —— 没有对应条目。我对 `tasks.md` 全文检索 `rule6_note` / `decision_table_row` / `scenario4b` / `negctrl` / 五字段, 判断清单区间 (`:60-92`) 零命中 (命中只在 `:6` Status 行、`:21` 读前必看第 5 条、`:165` 任务 5.1)。而 yaml 的 `fields_basis` 里实际做了四个裁量: `decision_table_row` 取第三行却执行并集 (计划自己写明「SOT 的单值字段表达不了并集档」)、`scenario1` 记待回填目录而非 `n/a`、`scenario4b: not_required`、`negctrl: n/a`。

这不改变执行者会做什么 (取值已钉在 yaml 里, 且执笔实例已把两条同题项列进请裁六条), 但 TASK-031 的交付物之一是「周期 handoff 照录判断清单」—— 照录出来的 Rule #10 复议面会缺掉这一项, 而它恰好是 SOT 自述**无机械 enforcement** 的那一项。建议补一条 (v2.2) 判断: 「`rule6_note` 按 SOT 1.1.0 §4.1 五字段落地, 取值见 yaml `metadata.rule6_note.fields_basis`; 第三行档在 SOT 的单值字段里无法表达并集, 以 `note` 补齐并经 TASK-031 第 6 张 issue 反馈 SOT」。

## R2 对账

| 键 | 判定 | 证据 |
|---|---|---|
| **PP2-M1** (architecture / TASK-001) | **closed** | TASK-001 第 2 条改为运行时三元组解析, 四态分流齐全 (恰 1 条 active / 0 条 active 明确含 `done`·`yielded`·`abandoned`·本容器无 claim / 2 条及以上不假设唯一)。owner_gates 第 14 项条件逐字扩为「解析到 done / yielded / abandoned 任一终态, 或本容器该轨无任何 claim」, 并写明三终态下一步相同、差别只在呈递事实。我逐字执行了计划给的容器 id 命令, 得 `'bfe8285d'`, 与协调 ref 里的 `claims/bfe8285d/` 目录名同形 (不带 `simonfish/` 前缀, 可直接拼前缀); `derive_track_id('pre-merge-completeness-gate-change-scope')` 实测为恒等。协调 ref 现态与计划描述一致: `claims/023236f2/s-86f7@1836.yaml` = `yielded`, `claims/bfe8285d/s-73b9@1606.yaml` = `active` (heartbeat `2026-09-18T18:50:09Z`), 另有 `claims/bfe8285d/s-9762@1447.yaml` 的 `track_id` 带容器后缀故被三元组正确排除。`heartbeat_by_track` (`claim_lifecycle.py:534-560`) 的匹配条件逐字就是 container + 归一 track_id + `active` 三重合取, 且对多条匹配**全部刷新**, 与计划「多条全部纳入 own 集」的要求自洽。 |
| **PP2-M2** (implementation / `own_claim_files`) | **closed** | 该字段改为「TASK-001 在运行时按三元组解析出的 claim 文件, 可能不止一条 …… 不是写死的路径」, 并把 `claims/023236f2/s-86f7@1836.yaml` 降为「当时的解析样例, 该条已于 2026-09-17 转 yielded」; 另补了 R2 自报薄弱点 (d) 要的反向指针 (生产解析 vs N6 fixture 自造)。首跑必判 `other` 的路径因此消失。 |
| **PP2-M3** (implementation / `commit_attribution`) | **closed** | 判据改为三类路径 (exclusive / shared / foreign), 单亲提交判 `own` 需「无 foreign 且有 exclusive」, 否则看 `Spec:` trailer, 再否则判新 kind `shared-only`; owner_gates 第 16 项同步改写并点名「典型是并发发版轨的 chore(release) 主仓同步面」。计划嵌入的 N9 三态实跑显示 `sibling release sync (shared paths only, no Spec trailer)` 翻为 `stop / shared-only`, 带 trailer 的翻为 `own-release-sync`, 且 `foreign path + Spec trailer` 仍判 `foreign` (trailer 不能洗白 foreign 路径)。我按代码逐行核了归类顺序与 `TRAILER` 正则对 TASK-029 字面串的命中, 与输出自洽。残余的「trailer 是声明不是证明」属执笔实例自报 (a), 见下节表态。 |
| **PP2-M4** (documentation / `baseline_rebase` + `rule6_note`) | **partially** | **已闭合的两半**: (i) `baseline_rebase.standards` 按实测重写并显式限定「这是对上述四个文件、在 `21748d4..940cb5b` 之间的断言, 不是全称句」, 还点名 v1 / v2 / v2.1 的旧断言在 `940cb5b` 落地后即已为假 —— 我独立复测: 该区间 standards 全仓只有 `content-integrity.md` (+58/-2) 与 `skill-benchmark-exemption.md` (+24/-2) 两个文件变动, 四个被引文件 (`openspec/project.md` / `openspec/templates/proposal-minimal.md` / `conventions/configured-gate-authority.md` / `conventions/version-management.md`) 各自 `--shortstat` 输出为空, 断言逐字成立; (ii) `rule6_note` 已按 SOT §4.1 五字段重写, 字段名与模板逐字对齐, 组合 (`description_changed: no` + `scenario4b: not_required`) 按 §4.1 的合规判据成立。**未闭合的那半**: TASK-001 的基线复核条 (`:1055`) 仍只枚举 `aria_zero_diff` / `aria_shifted` / `main_repo` 三组命令, **没有任何 standards 的复测命令** —— 而 `metadata.baseline_rebase.standards` 自己写着「TASK-001 必须对 B.1 当时的 gitlink 重测, 不得沿用本行数值」。即「必须重测」这句指令在 TASK-001 的可执行清单里没有落点 (`tasks.md` 读前必看第 5 条末句「1.1 在 B.1 对当时 gitlink 重跑」同样只是指令, 不是命令)。这与执笔实例自报薄弱点 (b) 是同一件事, 按派单纪律**不另立 finding**, 只在此记为 partially, 并在下节表态。 |
| **PP2-M5** (testing / `TASK-011` 与读前必看第 8 条) | **closed** | 读前必看第 8 条把 explicit-only 收窄从 (S4, `no_spec_unverifiable`) 扩到 `spec_level_undetermined` 并给出规则全文; TASK-011 verification 新增专条 + 可证伪落点, TASK-003 矩阵与 TASK-005 RED 同步钉了 `checkpoints: {post_spec: 'convergence'}` 与逐字断言 `checked_checkpoints == ['post_spec']`, 落在既有格 `SC-9.4-level-undetermined-bypassed` (不新增格名 ⇒ stage_cells 与 C1 证据不受影响)。**补一条比计划自述更强的判断**: 该断言的区分力其实不依赖实现的装配时机方向 —— 五项排除之后剩 `post_spec` / `post_planning` / `post_implementation` 三键, 只有 `post_spec` 是显式的, 另两键走 2a 需要 Level 而必然触发 `spec_level_undetermined`; 无论「边算边收」按何种顺序遍历, 只要不是 explicit-only 规则就给不出 `['post_spec']`。计划正文说「两个字面合规的实现给 `['post_spec']` 或 `[]`」在方向上略窄, 但断言本身对两种非合规读法都判红, 不影响闭合。 |

## 对执笔人自报薄弱点的表态

- **(a) trailer 把归属从路径事实降级为提交者声明, fixture 守不住「trailer 写在一条纯 shared 提交上」—— 可接受。** 伪造需要他轨主动写上本轨 trailer (需要伪造意图, 不是疏忽形态), 而 owner_gates 第 2 / 9 项仍要求把 `git log --oneline origin/master..<ref>` 清单随授权请求呈 owner, 人这一关没撤; 相比之下 R2 指控的漏放形态 (纯发版同步面无需任何声明即判 `own`) 是**疏忽即命中**, 两者风险量级不同, 这次换来的净收益是正的。执笔实例提的替代方案 (砍掉 trailer 分支、要求每个本轨提交都含 exclusive 路径) 我**不建议**采纳: TASK-029 的交付物整条落在 shared 集是发版同步面的固有形态, 砍掉分支等于把本轨自己的发版提交永久钉在等待点 16 上。
- **(b) M4 的修复是「记录更新 + 范围限定」不是机制, standards 随时会动而无机械守卫 —— 不可接受。** 不是因为缺机械守卫 (那是可以接受的成本), 而是因为**连人工复测的落点都没有**: `metadata.baseline_rebase.standards` 写了「TASK-001 必须对 B.1 当时的 gitlink 重测」, 而 TASK-001 的基线复核条只列了 aria 与主仓两组命令。执行者照 TASK-001 逐条做完, 不会对 standards 跑任何一条 `diff`。这正是 PP2-M4 的成因 (并发轨把 SOT 升到 1.1.0) 原样具备再发生一次的条件 —— 而这次它会打在 `rule6_note` 的五字段格式上, 那里按 SOT §6 自述没有任何机械 enforcement。修法极轻: 在 TASK-001 基线复核条追加一句, 对 `baseline_rebase.standards` 点名的四个文件跑 `git -C standards diff --shortstat 21748d4 <B.1 实测 gitlink> -- <文件>`, 非空即实读被引处并记偏移表 —— 与 aria / 主仓两组完全同款。**按派单纪律未计入 finding**, 但我认为它比我报的 m1 / m2 都重要, 建议主控在聚合时单列。
- **(c) SC-9(4) 的触发前提是读出来的不是跑出来的 —— 可接受。** 被测脚本要到 Phase B 才存在, A.3 阶段结构上不可能实跑; 而该格的推演链我独立走过一遍 (见上表 PP2-M5 的补充判断), 结论比计划自述更稳: 断言对两种非 explicit-only 读法都判红。误判的后果也是保守方向 —— 若推演错了, TASK-011 的 `stage_cells` 会显示该格 fail 而不是假绿。
- **(d) N9 新 fixture 用普通文件冒充 shared 路径, 没有复现真正的 gitlink 形态 —— 可接受。** `commit_attribution` 的归类只读 `git diff-tree --name-only` 的路径名, 对 gitlink (mode 160000) 与普通 blob 走的是同一条路径判断; 路径名 `aria` 在两种形态下逐字相同, 所以 fixture 的等价性成立。主控在真仓历史上对 `1b9734a` / `5fe15b0` / `c9fe08f` 三条真 gitlink 提交的复算已经补上了这一层。
- **(e) 只改了五条 Major 指到的地方, 跨节交叉引用是读着核的加 grep 计数 —— 可接受。** 我做了一轮独立的机械交叉核对作为补充: agent 配额 (`metadata.agents` 15/8/7/1) 与 31 个 TASK 的实际分配逐项相等; 全部 `dependencies` 严格指向更小编号 (无环、与编号序串行自洽); ab-suite 计数 (32 个 json / 84 evals, 加 eval id 3 后 85) 与 TASK-023 的预期一致; `sc13_baseline` 记的 4 处 `{timestamp}` 残留分文件实测为 phase-a-planner 1 / phase-b-developer 2 / phase-c-integrator 1, 逐字吻合; `VERSION` 第 24 行确为 aria 插件行且仍写 `v1.73.0`。唯一一处交叉引用不闭合的是 M2 (「三份 SKILL.md」对四份被改文件), 它正好落在 grep 计数看不见的地方。
- **(f) 一次自造的路径失误 (拼错 scratch 路径), 无实质影响 —— 可接受。** 不在交付物里, 不进 Phase B 执行面。

**对执笔实例提出、owner 尚未裁定的六条的表态** (逐条, 不作为新发现):

1. `rule6_note.scenario1` 在 A.3 只能是占位, 回填与齐备性断言放 TASK-031 —— **可接受**, 结果目录名在 TASK-024 跑完前不存在, 提前编造反而更坏; TASK-031 的「无占位尖括号残留」断言把回填做成了硬检查点。
2. `scenario4b: not_required` / `negctrl: n/a` 完全依赖「description 零改动」而无机械触发器 —— **不可接受**, 但理由与执笔实例说的不同: 机械触发器其实**存在** (TASK-015 / 016 / 017 的 frontmatter sha256 + TASK-018 复核), 问题是它只覆盖四份里的三份 (M2)。补齐第四份之后这一条就变成「有机械触发器」, 可接受。
3. M3 的 `Spec:` trailer 是声明不是证明 —— 同 (a), **可接受**, 不建议采纳其替代方案。
4. M3 新增停点 (本轨 5.7 漏写 trailer 会停在等待点 16) —— **可接受**, 方向 fail-closed, 且 TASK-029 已配「提交后当场 `git log -1 --format=%B` 回读确认 trailer 在位」, 把停点概率压到很低。
5. M1 多条 active claim 选「全部纳入 + 上报」不挑不删 —— **可接受且是正解**。`heartbeat_by_track` 对多条匹配全部刷新 (`claim_lifecycle.py:548-560` 的 for 循环逐条 `write_claim`), 所以 own 集必须等于全集, 否则 `coord_ref_precheck` 的 `set(files) <= own` 当场判 `other`; 「挑一条」在机制上本来就行不通。`10CG/aria-plugin#202` 实在 (open, 标题逐字「phase1_gate 的 self-resume 按 (container, session) 匹配 — 同容器换 session 再认领会新建第二条 active claim」), 计划对它的形态描述准确。
6. TASK-030 只改 standards 半句、不碰未裁的 minor 的边界切法 —— **可接受**, 返修轮只动被点名的面是正确纪律; 未裁的 8 条 minor 留给 owner 一次性处置比逐轮夹带更可审计。

## 风险 / 疑问 (不计入 finding)

1. **入口门仍然是 `10CG/Aria#195`**: owner_gates 第 1 项要求「10CG/Aria#195 已完成 C.2 合并或 owner 明示改序」; 即使 R3 收敛, 下一步是 owner 门而不是 Phase B。别把「审计收敛」读成「可以开工」(与 R2 同一提醒, 事实未变)。
2. **会话收尾 handoff 与提交归属的高频摩擦 (R2 风险 2 的加强版)**: Phase B 预估 97–143h 跨多会话, 每次会话收尾按 Rule #9 要写 `docs/handoff/`, 而 `docs/handoff/latest.md` 在 `commit_attribution` 里判 `foreign`。我读代码确认了一个 R2 没点出的放大效应: `klass()` 的结果一旦有任何 `foreign`, 整条提交就判 `foreign` (`if not ks or "foreign" in ks: kinds.append("foreign")`), 而不是只把那个文件标出来 —— 也就是说「本轨 handoff + latest.md 指针」写在同一个提交里时, 连本轨自己的 handoff 也一起被判成非本轨。方向是 fail-closed 不会误推, 但它会让**每个会话边界**都命中等待点 16。建议在第 16 项旁注明这是预期路径 (或让会话 handoff 与 latest.md 分两个提交), 免得第一次撞上被当成异常处置。
3. **本轮我没有重复的核验**: 未独立复跑 `metadata.a2_state_runs` 与 `metadata.v2_state_runs` (主控 C1 已做逐字节核验与独立副本复跑), 对这两块限于实读其嵌入代码与输出; `aria_zero_diff` 的 27 个文件我只抽查了 6 个 (`execution-modes.md` / `audit-engine SKILL.md` / `phase-c-integrator SKILL.md` / `LEVEL_GUIDE.md` / `DEFAULTS.json` / `run_all_tests.sh`), 全部零 diff。
4. **M1 的失败路径目前是前瞻性的, 不是现态**: 我实测本地 `refs/aria/coordination` 与 origin 同为 `f121e5d5`, 今天推送不会非快进。M1 的成立不依赖当前分叉, 依赖的是「判据写不出失败」这一结构事实 (我用临时仓复现了)。顺带一提, `coord_ref_precheck` 只 fetch 进 `FETCH_HEAD` 而 `read_claims` 读本地 ref (`coordination_ref.py:605-626`), 所以本地协调 ref 落后 origin 时 TASK-001 的三元组解析看到的是旧视图 —— 这是心跳推送变成非快进的上游成因, 修法与 M1 第 (3) 项同批 (推后核验能把这类分叉当场暴露)。
5. **顺带核过、结论是没问题的几处** (记下来免得下轮重复挖): `metadata.c25_five_questions` 五问逐条对源码属实 —— Q1 的 `phase-c-integrator/SKILL.md:613-623` 覆盖执行流程 1–6 步、Q2 的 `push_all_remotes.sh:119` 正是严格成功判据行、Q3 的 `DEFAULTS.json` 第 6–15 行含 `read_only_remotes` 与 `fail_on_partial_push: true` 且本仓 `.aria/config.json` 确无 `multi_remote` 段、Q4 的 `:613` 快照与 Q5 的 `:614` 枚举与 `:638` detached 处置全部对得上 (R2 的 CR/m4 精度差仍在, 属未裁的 8 条 minor, 不重报); 组 2 的六个任务切分与 §1.0 的 P0–P6 边界逐段对齐 (TASK-008 = P0/P1, 009 = P2a/P2, 010 = P3/P4, 011 = P5 与早退豁免, 012 = P6, 013 = 收口), 无跨阶段任务; 31 个任务工时全部 ≤ 8h; TASK-029 的 16 个版本点加总正确 (README 2 + 三份 i18n 各 3 + CLAUDE.md 2 + VERSION 1 + 两份架构文档各 1); `--include-terminal` / `--repo-path` / `--heartbeat-only` 三个 flag 在 `phase1_gate.py` 实存, `check_bare_issue_refs.py` 确实支持 `--repo-root=`, `no-unresolved-version-placeholder` 在 `.aria/state-checks.yaml:29-44` 且 enabled, `ai-native-estimator/scripts/estimator.py` 实存; 三个子模块当前都在 `master` 且本地 = HEAD (aria `1cb3872` / aria-orchestrator `237045a` / standards `940cb5b`), TASK-030 的四值相等断言在今天成立; SC-11 的 `matched_count >= 6` 有充分余量 (本 SID 的 post_spec 报告现有 30 份、post_planning 12 份)。

## Verdict

**PASS_WITH_WARNINGS · 0C / 2M / 2m · Vote: REVISE**

## 是否足以开始 Phase B

**不足以** —— 两条 Major 都是定点修订、不涉任务结构重排, 但都落在「照字面执行会漏掉必做项」上: M1 使 B.1 第一个可执行动作 (心跳) 的验收在推送彻底失败时仍然通过, 且协调 ref 是全计划唯一不受 CLAUDE.md 硬约束 2 保护的推送类; M2 使 Rule #6 的 `description_changed: no` 在四份被改 SKILL.md 中有一份从未被验证, 而 SOT 自述该字段无机械 enforcement。另需注意, 即便两条改完, 下一步仍是 owner_gates 第 1 项 (`10CG/Aria#195` 的 C.2 或明示改序), 不是 Phase B。

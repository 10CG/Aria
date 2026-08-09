---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-08T21:38:19.588Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R3 — knowledge-manager 席位报告

被审对象: `openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md` (186 行, R2-fix 大幅减法版)。

本轮性质: R1/R2 各 5/5 REVISE·FAIL, owner 裁定减法收缩。**本席位任务是独立核验「砍剩的这三处改动」本身站不站得住**, 镜头 = 规范合规 / 文档一致性 / 外部事实, 重点是 §Rule #6 归类。以下按硬性要求逐条给出 `file:line` 锚点, 全部为已实读的只读核验。

---

## 审计结论

### Finding 1 [CRITICAL] — §Rule #6 归类 (行判据表第三行) 的论证链有实质缺陷, 且遗漏了直接管辖的成文约束

**被审内容**: `proposal.md:112-129`(§Rule #6 处置), 核心结论在 `proposal.md:120`: "本 Spec 的处方性 hunk (`SKILL.md:243` 指令行) 属**第三行「处方性 · 套件覆盖外」**"。

独立核对 SOT 原文 (未采信 Spec 自评) 后, 发现以下问题:

**(a) 引用的 benchmark.md 证据与要证明的命题不是同一件事 (mis-citation)**

`proposal.md:117` 引: *`benchmark.md:173` 明文: "AB measurement of LLM workflow behavior under **multi-PR concurrent CI** is not feasible in mock environments. Deferred to production dogfood."*

已逐字核对 `aria-plugin-benchmarks/ab-results/2026-05-10-phase-c-integrator-pre-merge-gate/benchmark.md:173`, 引文逐字准确 —— **但该句的技术命题是「无法在 mock 里模拟真实的多 PR 并发 CI 竞态」**(对应 issue #137 附带的 T5.4 dogfood 议题: cancel-other-in-flight-run 计数), 与本 Spec §Rule #6 要证明的命题「AI 会不会照抄 `SKILL.md:243` 里的字面 `main` 而不是替换成真实分支名」是**两个不同的技术问题**: 前者需要真实并发 CI 基础设施才能验; 后者是纯粹的单发 (single-shot) 描述性 LLM 行为, 现有 `ab-suite/phase-c-integrator.json` 三个 eval 本身就是这种单发 descriptive 形态 (`aria-plugin-benchmarks/ab-results/2026-07-31-v1.65.0-122-rule6/grading-summary.md` §1: "三个 eval 九臂全部遵守 descriptive")。用「测不了并发竞态」去论证「测不了字符串替换行为」, 论据与结论不匹配。

**(b) 「C.2.4 零命中」的表述与实测 eval 输出内容不一致**

`proposal.md:118` 断言: "`ab-suite/phase-c-integrator.json` 的 3 个 eval 覆盖 C.1 / C.2 / C.2.5, **C.2.4 零命中**。"

已实读 eval-2 (C.2 merge-conflict-handling) 在最近一次实跑 (`aria-plugin-benchmarks/ab-results/2026-07-31-v1.65.0-122-rule6/`) 中的 **实际输出**:
- 评分报告自身对 eval-2 的定性: `grading-summary.md:34` — "### eval-2: C.2 合并冲突处理 (冲突流程 + **pre-merge gate/C.2.4**) — 本次 change 定向观察面"
- `with_skill/answer.md:88-103` 整段标题为「C.2.4 Pre-Merge Precondition Gate 重跑」, `:91` 逐字「查 **main in-flight**: 若 main 正有 CI run ... → 同样 wait」
- `old_skill/answer.md:102-108` 整段标题为「**C.2.4 pre-merge precondition gate**」, `:104` 逐字「查本 PR CI 状态 + **main in-flight**」

⇒ eval-2 的两臂输出**都**实质性讨论了 C.2.4 的 main-in-flight 查询行为, 与「零命中」字面矛盾。**更精确的说法应是**: eval-2 场景本身把目标分支设定为字面 `main`(prompt: "Attempting to merge feature/oauth2-social-login into **main**"), 这与本项目 SKILL.md 里硬编码的错误缺省值恰好同形 —— 故该 eval **无法区分**「AI 正确算出真实分支恰好叫 main」与「AI 盲抄 SKILL.md 字面文本」, 这是**该 fixture 自身的混淆变量**, 不是「C.2.4 零命中」。这个更精确的论证本可以成立(类比 §Why 里 aether 后端「分支不存在」与「无 in-flight」合流的同款论证结构), 但 Spec 没有这样论证, 而是使用了一个与实测输出相悖的粗糙断言。

**(c) 完全未检视/引用直接管辖本情形的 SOT 条款**

`standards/conventions/skill-benchmark-exemption.md:33`: "**SKILL.md 有变动时的附加约束** (承前): 仅当变动是**事实性同步** (溯源注释 / 行号勘正 / 术语修正) 且 frontmatter `description` 零变动, 才可能落进第一行 ... **`description` 或指令流程变动 ⇒ 一律第二行**。"

`CLAUDE.md:110` 对应一句几乎逐字重复: "`description` 或指令流程变动**一律照跑**; 豁免须在 spec/tasks 留 `rule6_note`。"

本 change 对 `SKILL.md:243`/`:167` 的修改是把一条被 AI 在 C.2.4 步骤 3 实际执行时读取的命令示例 (`aether ci status --branch main --in-flight --json`) 从硬编码 `main` 改为占位符 `<main-branch>` (`proposal.md:59`)。这不是「溯源注释 / 行号勘正 / 术语修正」意义上的事实性同步 —— 它改变了 AI 在该步骤实际会产出的命令内容, Spec 自己在 `:120` 也承认这是「指令行」。按 `:33` 条文的二分框架 (只给出第一行/第二行两个去处, 未提第三行), 这处改动**不满足第一行的准入条件**(非纯事实同步), 落点应是第二行「照跑」—— 该条款从未被 §Rule #6 一节引用或处理。

**(d) 已存在的同 skill 同步骤先例, 展示了第三行论证应有的精度**

`aria-plugin#127`(已核, state=open, title: *"phase-c-integrator AB 两套件均覆盖不到 C.2.4 的 D9 surface 措辞 — 该义务自 v1.65.0 起零 eval 覆盖"*) 是同一个 skill、同一个 C.2.4 步骤下、此前已成功走通第三行流程的先例 (由 `#126` 触发开立)。它的论证精度是: **精确点名到 `path_coverage.decision == unknown` 且 `reason=internal-error` 这一个分支**, 逐 fixture 列表说明「六个既有 fixture 全落在 verdict 路由, 无一碰到该分支」。相比之下, 本 Spec `proposal.md:118` 只给出「3 个 eval 覆盖 C.1/C.2/C.2.5」这种粗粒度、且经不起实读 transcript 检验的断言, 论证精度未达到项目已有先例的标准。

**(e) 强制要求的 `rule6_note` 标记完全缺失**

`standards/conventions/skill-benchmark-exemption.md:55`: "无论走哪一行, 都要在 spec/tasks 留 `rule6_note` 引用本规范。" `CLAUDE.md:110` 同样要求。已用 `grep -rn "rule6_note" openspec/changes/premerge-gate-mainbranch-failclosed/` 核验, **零命中**。对照同期/近期姊妹 Spec 的实际写法:
- `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:273`: `**Rule #6 (rule6_note)**: ...`
- `openspec/changes/secret-guard-per-segment-evaluation/proposal.md:156`: `## rule6_note`

两者都在正文中显式落了 `rule6_note` 字样。本 Spec 有实质内容对等的「§Rule #6 处置」章节 (`:112-129`), 但从未使用这个 SOT 与 CLAUDE.md 都逐字要求的标记 token —— 这是一个独立于 (a)-(d) 的、机械可检的缺项。

**综合**: (a)(b) 表明本 Spec 用来支撑「第三行」结论的实证链本身有引用错配与陈述失真; (c) 表明存在一条直接管辖、从未被处理的更高优先级成文约束, 其字面结论指向第二行; (d) 表明本项目已有更严谨的第三行论证先例可以对标, 本 Spec 未达到该标准; (e) 是独立的机械合规缺口。四者叠加, 足以认定当前 §Rule #6 处置的结论**未经充分验证即采信**, 落 CLAUDE.md 不可协商规则 #6 (Level 2 Spec 必须遵守)。这不等于断言「正确答案一定是第二行」——(c) 与已有的 `#127`/`a1-entry-claim` 先例(它们也把直接 SKILL.md 正文改动落在第三行且被认可)之间存在需要 owner 澄清的张力, 但(a)(b)(e) 三点不依赖那个张力的解决, 已经独立成立。

**处置建议**: 二选一 —— (1) 照 `#127` 的精度重写 §Rule #6: 精确点名「AI 是否会照抄 SKILL.md:243 的字面 main」这一具体行为, 剔除 mis-cited 的 benchmark.md 引用, 用实际 eval-2 transcript (而非 JSON 结构统计) 证明现有 fixture 为何测不到*这个具体*行为(混淆变量论证), 补 `rule6_note` 标记; 或 (2) 直接落第二行, 照跑 `ab-suite/phase-c-integrator.json`(3 eval 现成, 成本可控)。

---

### Finding 2 [MAJOR] — 审计叙事与交付面同居一文, 与一天前刚裁定的姊妹 Spec 先例相悖

`proposal.md` 末尾 §审计轨迹 (`:171-180`, 逐轮 vote/major 计数表) 与 §待 R3 重点审 (`:182-186`, 给下一轮审计的检查清单) 是典型的 **append-only 审计叙事**, 直接嵌在交付面文档里。

已读 `openspec/changes/linked-issue-normalization/proposal.md:10-12`(该 Spec 2026-08-07 —— 仅早本 Spec 一天 —— owner 明确裁定):

> "📌 本文件只规定「要建什么」。「规定是怎么来的」(三轮审计轨迹 / ... / 全部订正留痕) 已于 2026-08-07 整体移出至 [审计轨](../../../.aria/audit-reports/linked-issue-normalization-audit-trail.md)。⚠️ 该审计轨是 append-only 的, 且显式不维护与本文件的一致性 ... 这条切分是 R1′→R3′ 三轮的直接产物 —— 那三轮 26 条 major 里, 落在纯交付面的接近于零, 而 append-only 的审计叙事与交付面的强耦合正是缺陷生成机制本身。"

已核该切出文件确实存在: `.aria/audit-reports/linked-issue-normalization-audit-trail.md`(293 行, 2026-08-07 提交)。这条裁定与项目 memory `feedback_audit_trail_must_not_live_in_spec` 完全对应。本 Spec 同样经历三轮审计, `proposal.md:171-186` 的结构与该先例描述的「耦合」形状一致, 却未做切分, 也未在文中说明「本 Spec 有意不采用该先例」的理由。

**处置建议**: 把 §审计轨迹 + §待R3重点审 移到独立的 `.aria/audit-reports/premerge-gate-mainbranch-failclosed-audit-trail.md`, proposal.md 顶部留指针, 与姊妹 Spec 同构; 或在文中明确记录「本 Spec 因篇幅小 (186 行) 有意不切分」的豁免理由。

---

### Finding 3 [MAJOR] — `ship target: PATCH` 未与「破坏性变更须 MAJOR」原则和解

`proposal.md:10`: "**ship target**: **PATCH** — 号段落地时按 `plugin.json` 当前版本 patch+1 计算, 不预写字面量"。

但同一文件反复承认这是破坏性变更:
- `:53`: "不传参的行为: CLI → argparse 报错退出 (RC=2); 函数 → `TypeError`。二者都是**硬失败**"
- `:155-159`: "既有测试必然要动 (原「逐字不改」的说法已证伪) ... 参数改必填后**全部 24 处 `TypeError`**"
- `:163`: "**本 change 使「忘记传 `--main-branch`」从静默放行变成硬失败。**"

CLAUDE.md「协作原则」段: "向后兼容 (破坏性变更须 MAJOR)"。本变更把此前带缺省值的可选参数 (CLI flag 与函数形参双双) 改为必填, 是教科书式的 SemVer 破坏性签名变更 —— 任何未显式传参的既有调用方 (包括本仓外部、未被本 Spec grep 到的调用方) 会从「静默运行(结果错)」变成「直接报错」。`standards/conventions/version-management.md` 通篇未给出 aria-plugin 子组件 MAJOR/MINOR/PATCH 的判定细则 (该文档面向主项目 SemVer, §4.3 只处理 tag-vs-VERSION 文件同步策略, 不处理语义分级), 也未在 CLAUDE.md「Aria 约定」("新增 Skill / Skill 架构重构 = MINOR+; 文档更新 / bug 修复 = PATCH") 里给出「必填化即破坏性签名变更」这一具体情形的归类。

`proposal.md` 全文未出现任何一处显式地把「破坏性变更须 MAJOR」这条原则与本次刻意选择的破坏性修法(D2: 必填而非兼容式解析)放在一起权衡, 只在 D6 说明了「不预写字面量」这一无关的技术理由 (避免与并发姊妹 Spec 的版本号非单调冲突, 该理由本身成立, 但答的不是 PATCH-vs-MAJOR 这个问题)。

**处置建议**: 在 §Rule #6 或新增小节里显式论证「为什么这处刻意的破坏性变更仍归 PATCH」(例如: 援引「Aria 约定」把它定性为 bug fix 而非 API 变更, 说明该参数此前从未被文档承诺为「可选」故不构成公开契约的破坏), 而不是仅靠数字延迟计算带过。

---

### Finding 4 [MAJOR] — SC-M4 的「三处命中」自证与其自身判据文本的字面读法不一致

`proposal.md:105`: "SC-M4 | 源码扫描: `pre_merge_gate.py` 全文 | 无 `"main"` 字面量作为分支名缺省 (`:21`/`:300`/`:427` 三处) | 现状三处命中 ⇒ **必红**。机械 grep, 零裁量"
`proposal.md:186`: "编排层实测当前命中数分别为 **3 / 3**, 与表中行号逐一对应。"

已实测:
```
$ grep -c '"main"' aria/skills/phase-c-integrator/scripts/pre_merge_gate.py
2
$ grep -n '"main"' aria/skills/phase-c-integrator/scripts/pre_merge_gate.py
300:    main_branch: str = "main",
427:    parser.add_argument("--main-branch", default="main", help="Main branch to check (default: main)")
```
`:21` (`pre_merge_gate.py --pr-branch <branch> [--main-branch main] [--config-file path]`) 里的 `main` **不带引号**(docstring 里的用法示例, 不是 Python 字符串字面量), 按 SC-M4 文本字面写的 `"main"` 字面量(带引号)去 grep, 只命中 2 处, 不是 3 处。若把 pattern 放宽到不带引号的裸词 `main`, 则会在同文件里额外命中约 20 余处无关但合法应保留的标识符 (`main_branch`、`main_in_flight_runs`、`def main(`、`if __name__ == "__main__"` 等), 与 SC-M4 自称的「机械 grep, 零裁量」矛盾 —— 松紧两种读法都不能同时满足「精确 3 处」与「零裁量」。

对照 SC-M5 (`SKILL.md` 侧): 已实测 `grep -n -- '--branch main\|"branch": "main"'` 命中 **恰好 3 处** (`:167`/`:243`/`:270`), 与 Spec 描述完全吻合 —— 这一侧的自证是准确的, 问题只出在 SC-M4 (`pre_merge_gate.py` 侧)。

这恰好落在 Spec 自己标记的「待 R3 重点审」(c) 项范围内 (`:186`: "SC-M4/M5 两条 grep 断言的模式是否会漏"), 本次核验的结果是: **会**, 且已实测坐实, 而非假设性担忧。

**处置建议**: Phase B 编写 SC-M4 实现时需要一个能同时覆盖 `:300`/`:427` 的带引号字面量与 `:21` 的裸词用法示例、又不误伤 `main_branch`/`main_in_flight_runs`/`def main`/`__main__` 的复合正则(例如分两条子断言: 一条抓 `default="main"`/`str = "main"`, 一条专门抓 docstring 里 `--main-branch main]` 这个具体子串), 不能用单一裸词 grep。

---

### Finding 5 [MINOR] — `SKILL.md:167` 未被 §Rule #6 的「①②③」义务逐条点名

`proposal.md:60` 断言 `:167` 与 `:243` "同性质", 但 §Rule #6 一节 (`:120-126`) 的「①点名行为/②建 fixture/③开 issue」三条义务文本只显式提到 `SKILL.md:243`, 未显式把 `:167` 纳入同一套义务的覆盖范围描述里 (是否被同一个 fixture/issue 隐式覆盖, 读者需要自行推断)。建议在 ①②③ 三条里明确写出 `:167`/`:243` 是否共用同一个 fixture。

---

## 合规面确认清单 (核验后判定无 finding)

- **Rule #5**(项目变更放本项目 `openspec/changes/`): 合规 —— 本 change 位于 `/home/dev/Aria/openspec/changes/premerge-gate-mainbranch-failclosed/`, 非 `standards/openspec/changes/`, `proposal.md:9` 自述与实际路径一致。
- **Rule #1**(需求变更须 OpenSpec Level 2/3): 合规 —— `proposal.md:7` 声明 Level 2, 目录内只有 `proposal.md` 无 `tasks.md`, 与 Level 2 定义("Level 2 = proposal.md")吻合; 变更范围(单文件对 skill、单一域)不构成必须升 Level 3 的理由。
- **外部记录 · aria-plugin#137**: 已用 `forgejo GET /repos/10CG/aria-plugin/issues/137` 与其 comment `18015` 核验(只读, 未评论/未改动)。issue body 当前**确实**仍逐字保留被推翻的「两条腿都失败为绿」结论、**没有**删除线, comment 18015 **确实**存在且内容与 Spec `:33-35` 描述的订正一致。Spec 对此的表述("落地时须在 body 加删除线 + 指针", 即尚未做、留待 Phase B)与当前 live 状态相符, 无失真。

---

## Verdict

**FAIL**(1 Critical + 3 Major + 1 Minor)。

判据: verdict 规则「FAIL = ≥1 Critical」。Finding 1 (Rule #6 归类论证缺陷 + 遗漏直接管辖条款 + 缺失强制 `rule6_note` 标记) 触及 CLAUDE.md 不可协商规则 #6, 且论证链中的两处硬伤 ((a) mis-citation、(b) 与实测 transcript 相悖的「零命中」断言) 是可独立核实的事实性错误, 不依赖对判据表灰色地带的解读分歧, 因此定为 Critical 而非 Major。

---

## 轮次记录

- R1(5 席): 5/5 REVISE·FAIL。去重 5C+10M+6m=21, Major 10。详见 `.aria/audit-reports/post_spec-R1-1786216818583-premerge-gate-mainbranch-failclosed-aggregate.md`。
- R2(5 席): 5/5 REVISE·FAIL。去重 3C+15M+8m=26, Major 15(↑), fix 引入占比 100%。owner 裁定停止「审计→重写」循环, 大幅减法。详见 `.aria/audit-reports/post_spec-R2-1786220900000-premerge-gate-mainbranch-failclosed-aggregate.md`。
- R3(本席, knowledge-manager): 独立复核减法后的 186 行版本, 聚焦「砍剩的三处改动能否站住」。结论: **REVISE**(verdict=FAIL) —— 核心问题不在「砍多了/砍少了」这个 R3 被交代的主线risk 本身(§待R3重点审 (a)(b) 两项经检核, 均未发现新增反例; DEFAULT_CONFIG 确认不含 `main_branch` 键, 全文赋值点确实只有 `:300`/`:359`/`:436` 三处, 与 Spec `:184` 的「关得干净」结论一致), 而在**②Rule #6 处置本身的论证质量不足以支撑其结论**, 外加一处新发现的 SC-M4 自证不准(Finding 4)与一处结构性先例未遵循(Finding 2)。

**本报告 finding 全部标记 `introduced_by_r2fix: true`**(§Rule #6 论证、审计轨迹结构、SC-M* 命名与 PATCH 定档均为 R2→R3 本次「大幅减法」重写的产物, 非沿用 R1/R2 旧文本); Finding 1 另标 `cut_too_much: true`(把「照跑 AB」这一本应保留的验证义务连带砍成了「建定向 fixture」的轻量替代, 而支撑这次「减法」的论证本身站不住)。

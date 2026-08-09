---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-09T04:07:57.498Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: true
---

> **`is_refocus` 说明**: 模板给的字面值是 `false`, 本报告改判为 `true` —— 本轮审的是 R3 后范围重定的新对象 (proposal.md 顶部 `Status: Draft (R3-fix, 范围重定)`), 与 R1-R3 审的不是同一个承重项集合, 符合字段语义, 未盲抄模板。

# post_spec Round 4 审计报告 — knowledge-manager

被审对象: `openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md` (263 行, R3-fix 版)
镜头: 规范合规 / 文档一致性 / 外部事实 (knowledge-manager)

---

## 审计结论

按分配的 6 项任务逐条核验, 全部**实读源码 / SOT / git 历史 / Forgejo API**, 无一条凭记忆或推断。结论: **0 Critical**。技术设计 (D1-D9, SC-1~11) 本身经三轮审计已收敛良好, 本轮未在这条主线上发现新问题。但发现 **4 条 Major**, 集中在「文档/规范面的落地是否完整」这一层 —— 具体说, Spec 在**对自己适用 Rule #6 时用对了「直接管辖条款优先于实证」的方法论**, 却**没有把同一方法论用到§版本、Spec Level、CLAUDE.md 同步三处**, 这三处至今仍是可以用直接管辖条款/直接先例定掉、却被当成开放问题悬置或遗漏的状态。另有 2 条 Minor (转述精度 / 审计轨切分头部弱于先例), 不影响主线。

## Verdict

**PASS_WITH_WARNINGS**(0 Critical + 4 Major + 2 Minor)。

**什么阻塞进入 Phase B (明确判断)**:
- **不阻塞技术实现本身**: D1-D9 的设计、SC-1~11 的断言、Rule #6/Rule #8 现有条款的援引在事实核验层面站得住, Phase B 可以开始写 SKILL.md 重整 + `pre_merge_gate.py` 改动 + 测试。
- **阻塞「Phase A 正式收口」的一项**: FINDING-3 (Spec Level 2 是否成立) —— 这个问题的答案会决定 Phase B 该不该有一份 `tasks.md` 来管住「SKILL.md 重整 + 3 处代码改点 + 新函数 + 24 处既有调用点补参 + 2 处测试守卫扩容 + AB 排期」这条依赖链。它不影响 D1-D9 对不对, 但影响 Phase B **该怎么被组织**, 建议 owner 在放行 Phase B 前显式回答。
- **应在 Phase B/C 期间一并处理、不必现在卡住**: FINDING-2 (§版本悬置选项集)、FINDING-4 (CLAUDE.md Rule #8 同步)、FINDING-6 (#137 评论计划)——三者都是「Spec 文本 / 外部记录需要修一笔」量级的缺口, 有明确先例和修法, 不需要重新过审计轮次。
- FINDING-1、FINDING-5 为 Minor, 供留痕, 不需要行动即可继续。

---

## 轮次记录

- R1 (5/5 REVISE, FAIL, 21 条 major) / R2 (5/5 REVISE, FAIL, 26 条, major 10→15) / R3 (4 REVISE/1 PASS, FAIL, 22 条, major 15→10): 详见 `.aria/audit-reports/premerge-gate-mainbranch-failclosed-audit-trail.md`(append-only, 与本文件分居, 本报告 FINDING-5 核过该切分的合规性)。R3 的核心产出是推翻前三版共同的范围前提 (SKILL.md 散文步骤与 `pre_merge_gate.py` 是两份独立实现, AI 实际走的是未加固的那份), 促成本轮 (R4) 审的是**范围重定后的新对象**——承重项从「helper 缺省值」变为「D1: SKILL.md §C.2.4 结构重整」。
- **R4 (本报告)**: knowledge-manager 单席, 聚焦规范合规/文档一致性/外部事实 6 项指定任务。产出 4 Major + 2 Minor, 0 Critical。

---

## 逐条 Findings

### FINDING-1 (Minor) — Rule #6 对 SOT §3 的转述比原文更紧

**定位**: proposal.md:198 (「同 SOT §3 界定第三行专指『给 spec 作者读的』处方 (authoring) 而非运行时指令」) vs. `standards/conventions/skill-benchmark-exemption.md:30`(决策表第三行原文:「处方性, 但它治的行为在**固定测试集覆盖范围之外** (**典型**: authoring 向导 —— 给 spec 作者读的处方...)」)。

**问题**: SOT 原文用的是「典型」(举例), 真正的判据是「行为是否在固定测试集覆盖范围之外」——authoring 只是这个判据下最常见的一种实例, 不是判据本身。proposal.md 把它转述成「专指」(排他性定义), 比原文更紧。

**是否影响本 Spec 结论**: 不影响。proposal.md:196 先援引的是**直接管辖条款**(「`description` 或指令流程变动 ⇒ 一律第二行」), D1 是教科书式的指令流程变动, 已经足以定档为第二行, 不需要再论证「是否落入第三行」。第 198 行那句只是补充性排除, 即便按 SOT 原文的宽松读法 (行为在覆盖范围外) 重新判一次, D1 仍然不满足 —— 两套件本来就是冲着 C.2.4 的运行时行为去的(proposal.md 202 行自陈的缺口是「surface 措辞覆盖不足」, 不是「类别上测不到」), 结论不变。

**建议**: 把「专指」改回「典型, 真正判据是覆盖范围外」, 避免下一位读者把这句话当成 Rule #6 第三行的权威定义引用出去 (SOT 本身在 §5 worked example 里已经有过「同一份文档不同 hunk 落不同行」的案例, 窄化定义容易被后续 Spec 误用)。

**blocks_phase_b**: false

---

### FINDING-2 (Major) — §版本 悬置的选项集本身不对: CLAUDE.md 有直接管辖条款可以先排除 PATCH

**定位**: proposal.md:230-237 (§版本):
> 「CLAUDE.md『破坏性变更须 MAJOR』与『bug 修复 = PATCH』在此冲突, **本 Spec 不自行裁定**: 若按『对外 API 契约』读 ⇒ MINOR/MAJOR; 若按『修复一个本就不该存在的 fail-OPEN 缺省』读 ⇒ PATCH。⚠️ **待 owner 裁定**。」

**问题**: CLAUDE.md §版本管理 还有第三条独立于「破坏性变更」/「bug 修复」的条款, 且是**直接管辖条款**——「SemVer。Aria 约定: 新增 Skill / **Skill 架构重构 = MINOR+**; 文档更新 / bug 修复 = PATCH。」proposal.md 自己在 §Impact 里给 D1 的描述就是「§C.2.4 **结构重整**」(proposal.md:222)——「结构重整」与 CLAUDE.md 的「架构重构」在语义上是同一件事的两种写法, 且 D1 是本 Spec 明写的**唯一承重项**(proposal.md:58「承重项是 §1」)。这意味着: 不管 D2 的「必填参数破坏性签名变更」最终按 API 契约读还是按 bug 修复读, **本次发布至少含一个 Skill 架构重构 (D1), 该条款已经把 PATCH 排除在外**——不存在「按 bug 修复读 ⇒ PATCH」这个分支的合法落点。

proposal.md 自己在 Rule #6 定档时用的方法论正是「直接管辖条款优先于任何实证」(proposal.md:196「定档依据 (直接管辖条款, 优先于任何实证)」), 但在 §版本这一节没有对自己援引同一方法论, 于是把一个本可以先收窄的三选项开放问题, 原样悬置给了 owner。

**影响**: 如果 owner 看到的是「PATCH/MINOR/MAJOR 三选一」而选了 PATCH (完全可能, 因为 D2 单独看确实像是「修一个不该存在的缺省值」), 会与 CLAUDE.md 自己的条款矛盾, 且需要日后再纠正一次版本号——这正是本 Spec 反复强调要避免的「静默流入、下游全不匹配」同款问题, 只是这次落在版本治理而不是 verdict 枚举上。

**建议**: 把 §版本 改为「PATCH 已被『Skill 架构重构 = MINOR+』排除; 待 owner 裁定的只有 MINOR 还是 MAJOR, 取决于 D2 的破坏性签名变更按『对外 API 契约』读还是仅视为内部实现细节」。

**anchor**: proposal.md:230-237, proposal.md:222, proposal.md:58; CLAUDE.md §版本管理(「新增 Skill / Skill 架构重构 = MINOR+; 文档更新 / bug 修复 = PATCH」)。

**blocks_phase_b**: false (版本号本就要等 ship 时按 `plugin.json` 当前值计算, proposal.md:8/237 已如此约定; 但悬置文字应现在改, 不必等 owner 先被误导一次)

---

### FINDING-3 (Major) — Spec Level 2 在范围重定后应重新核验, 且有直接可比的姊妹先例指向 Level 3

**定位**: proposal.md:5 (`Spec Level: **2**`)。

**核验依据**:
1. `standards/openspec/project.md:112-118`(OpenSpec Levels 表, CLAUDE.md 指其为 SOT):
   | Level | Name | When to Use | Output |
   |---|---|---|---|
   | 2 | Minimal | Medium features (**1-3 days**) | proposal.md |
   | 3 | Full | **Architecture changes** | proposal.md + tasks.md |
2. proposal.md 自己给 D1 的定性是「SKILL.md §C.2.4 **结构重整**」(proposal.md:60, 222), 与 Level 3 判据「Architecture changes」字面相合, 也与 FINDING-2 引用的 CLAUDE.md「Skill 架构重构」是同一件事。
3. **直接可比先例**: `openspec/changes/linked-issue-normalization/proposal.md:5` 记载「Spec Level: **3** (原 2; R3′ 因 Q5 的 AB 任务需 `tasks.md` 承载而升级 —— **单域** —— `lib/collision.py` 的一个比较谓词 + 一个导出单元)」, 且该 Spec 明写升级理由 (proposal.md:174):「AB 测的是该 hunk 的行为影响, 而 hunk 是 Phase B 交付物 ⇒ AB 在 Phase B 实施该 hunk 之后、发版之前跑。本 Spec 为此升 Level 3, 该任务写进 `tasks.md`」。

   这条先例的改动面**严格小于**本 Spec: 单文件 (`collision.py`) 一个比较谓词 + 一个导出函数 + 三处纯文档同步, 却仍因「Rule #6 的 AB 任务需要显式排期 (Phase B 落地后、发版前)」而升级到 Level 3。本 Spec 的改动面是 SKILL.md 结构重整 + `pre_merge_gate.py` 三处代码点 + 一个新函数 (`_verify_branch_exists`) + 一个新参数 (`--remote`) + 一个插入点位置约束 (D7: 三早退之后、path coverage 之前) + 一个 additive schema 键 + 11 条新 SC + **24 处既有 `gate_check(` 调用点**补参 (proposal.md:224, 90) + 2 处既有测试断言/守卫要害改动 (`test_sc12_default_true_lock` / `test_sc22_no_real_git_subprocess_in_suite`, proposal.md:224, 188) + 同样「ship 前须过 AB, 而 AB 只能在 Phase B 落地 D1 之后才有意义」的排期约束 (proposal.md:200)。姊妹 Spec 用来论证升级的理由 (AB 排期依赖 Phase B 交付物) 在本 Spec 上同样成立, 而本 Spec 的文件面/改动点数量明显更大。

**结论**: 现有的 Level 2 声明缺少与自身范围重定后规模相称的重新核验; 对照 SOT 判据与更小规模姊妹先例的升级理由, Level 2 是否仍然站得住是一个应由 owner 显式确认、而不是延续原判的问题。

**anchor**: proposal.md:5,58,60,90,188,200,222,224; `standards/openspec/project.md:112-118`; `openspec/changes/linked-issue-normalization/proposal.md:5,174`。

**blocks_phase_b**: **true** —— 这个判断直接决定 Phase B 该不该有一份 `tasks.md` 来管住上面列的多个依赖点 (D1 必须先落地、24 处调用点必须逐个补参、2 处测试守卫必须同步扩容、AB 必须在 D1-D7 都落地后才跑)。建议 owner 在放行 Phase B 前先对这一条给出明确裁定 (维持 Level 2 亦可, 但应留一句「已核对 Level 3 先例, 认为不适用, 理由是 X」, 而非静默沿用范围重定前的判断)。

---

### FINDING-4 (Major) — CLAUDE.md Rule #8 文本需要同步, §Impact 未列, 且有直接、逐字可查的先例

**定位**: proposal.md §Impact (218-228 行), 通篇无 `CLAUDE.md` 行。

**核验**: 本 Spec (§4「新增 --remote + 分支存在性核验」, D4/D7) 给 pre-merge gate 新增了**第三条独立可以让 verdict=fail 的判定路径**(分支不存在 / 核验失败, 各自产生新的 `gate_error.kind`), 且这条路径在(a) PR CI、(b) main in-flight 两条既有腿**之前**执行 (D7)。CLAUDE.md 现有 Rule #8 原文只描述两条腿:「phase-c-integrator C.2.4 验证 (a) 本 PR CI passing; (b) main 无 in-flight CI run; 经 CI backend 抽象层调用 (Aether 默认)。无可用 backend 按 `no_ci_fallback` 显式降级; stub backend 抛 NotImplementedError 时 gate 必须 abort, 不得静默降级。」——不包含分支存在性核验这第三条路径, 读者只看 CLAUDE.md 会误以为 gate 仍然只有两条腿。

**直接先例 (git 实证, 非推断)**: 用 `git show 7661e964b0f9d262ed2a28798b20d0d39b6cb6da -- CLAUDE.md` 核验, commit `7661e96`(`feat(m6-hygiene): aria-plugin v1.31.0 ship — CI backend abstraction`, 2026-05-28) **在同一个提交里**既改了 `aria/skills/phase-c-integrator/SKILL.md` §C.2.4(引入 CI backend 抽象层 + NIE-propagation Hard Constraint #7), **也改了** `CLAUDE.md` 的 Rule #8 文本, diff 逐字新增:
```
+**NIE-propagation 安全约束 (v1.31.0+, Hard Constraint #7):** 当某 backend probe=True 但 query 方法 raise `NotImplementedError`
（stub backend, 如 GitHub Actions v1.31.0 stub）,gate **必须 abort**（raise to caller）,**不允许** catch-and-route 到 `no_ci_fallback`。...
```
且现行 CLAUDE.md 里「stub backend 抛 NotImplementedError 时 gate 必须 abort, 不得静默降级」这句就是这次同步的产物 (可在系统提示词的 CLAUDE.md 全文里核对到, 与该 diff 逐字对应)。这证明「C.2.4 的判定行为发生实质变化 ⇒ Rule #8 文本同步」在本项目**已有先例、已被实际执行过**, 不是我的臆测类比。

**结论**: 本 Spec 引入的分支存在性核验是与 v1.31.0 NIE-propagation 同量级的「gate 判定行为实质变化」, 按已有先例应同步 Rule #8 文本, 但 §Impact 表未列 `CLAUDE.md`。

**建议**: §Impact 增一行 `CLAUDE.md`, 内容类似「Rule #8 补一句分支存在性核验前置于两条既有腿, 失败时 `verdict=fail` + `gate_error.kind`」, 篇幅可以很短 (参照 v1.31.0 那次也只加了一段), 但不能不提。

**anchor**: proposal.md §Impact 218-228 行 (无 CLAUDE.md 行); proposal.md §4 92-116 行 (新核验逻辑); git commit `7661e964b0f9d262ed2a28798b20d0d39b6cb6da`(`git show 7661e96 -- CLAUDE.md`); CLAUDE.md 不可协商规则 #8 现行文本。

**blocks_phase_b**: false (可作为 Phase B 或 Phase C 的一个小任务补, 不需要重新设计 D1-D9; 但应现在把这行加进 §Impact, 否则容易在 Phase B 执行时被跳过——Impact 表是 Phase B 的改动清单来源)

---

### FINDING-5 (Minor) — 审计轨迹切分实质合规, 但 proposal.md 侧头部弱于先例

**定位**: proposal.md:9 (「> **审计轨迹**: `.aria/audit-reports/premerge-gate-mainbranch-failclosed-audit-trail.md` (append-only, **与本文件分居**)」) vs. 先例 `openspec/changes/linked-issue-normalization/proposal.md:10-12`。

**核验**: 先例的 proposal.md 头部有一整段说明 (📌 本文件只规定「要建什么」+ 移出内容清单 + 「不一致时以本文件为准」+「不得因审计轨的历史记述而回改本文件」四点都写在 proposal.md 自己里面)。本 Spec 的 proposal.md 侧只有一行指针, 「不一致时以谁为准」「不得回改」这两条治理声明**只写在 `audit-trail.md` 自己的头部**(四条不同步声明之 (c):「与 proposal.md 的当前内容不保证一致 —— proposal.md 是唯一交付面 SOT」), 没有对称地写回 proposal.md。

**实质内容核验 (通过)**: 我完整读过 audit-trail.md 全文, 其中容纳的是「三轮审计轨迹 / Rule #6 定档摆动 / 编排层错误留痕 / owner 裁定记录」——与先例移出的内容类别 (三轮审计轨迹/总体定义与判族/未审表面清单/跨 Spec 裁定史/订正留痕) 高度对应; proposal.md 正文本身没有夹带逐轮审计流水 (仅在必要处轻量引用「post_spec R3 才浮出的结论」等一句话背景, 这点先例本身也这么做, 不算违规)。**切分的实质内容归属是对的**, 缺口只在 proposal.md 侧头部的治理声明比先例单薄。

**风险评估**: 较低——只读 proposal.md 的人不会真的撞见与 audit-trail.md 的不一致 (因为他压根没打开那份文件); 风险场景局限于「有人打开 audit-trail.md 却没看到它自己头部那四条声明就直接引用其中内容回改 proposal.md」, 而 audit-trail.md 自己头部已经把这四条声明放在最前面、不容易错过。

**建议**: 在 proposal.md:9 那一行旁边补一句「不一致时以本文件为准」, 与先例对齐, 成本很低。

**anchor**: proposal.md:9; `.aria/audit-reports/premerge-gate-mainbranch-failclosed-audit-trail.md:1-6`; `openspec/changes/linked-issue-normalization/proposal.md:10-12`。

**blocks_phase_b**: false

---

### FINDING-6 (Major) — issue #137 已有一条自我订正评论, 其技术描述已被本版放弃, 但 Spec 的「补 comment」计划未提及要 supersede 它

**外部核验 (只读)**: `forgejo GET /repos/10CG/aria-plugin/issues/137` + `.../comments`, 均成功, 结果如下 (非推断):

- **issue body 现状**: 无删除线、未被编辑, 与 proposal.md D9 (「不在 body 打删除线」) 的现状描述一致。
- **issue 已有 1 条评论**, id `18015`, 作者 `simonfish`, `created_at: 2026-08-08T16:37:00Z`(issue 本身 `created_at: 2026-08-08T16:03:43Z`, 相隔约 33 分钟)。该评论标题为「⚠️ 订正正文一处: 『两条腿都失败为绿』不成立 —— 只有 (b) 那条」, 内容包括: (a) 腿实际上是 fail-toward-covered (走向 `unknown` 而非 `not_applicable`), 原文观察到的 `not_applicable` 另有原因、与分支名无关; (b) 腿的指控成立并已独立复现; 并**补了正文遗漏的 `:300` 函数签名缺省**。评论末尾写道:「Spec 已起: `openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md` (Level 2, 待 post_spec)。范围: 两处缺省 + **从 `refs/remotes/<remote>/HEAD` 解析且解析失败即 abort**...+ `git ls-remote --exit-code --heads` 存在性核验 + **verdict 回显 `main_branch_resolved` 及其来源** + **7 条 SC**。」

- **与本版 (R3-fix) proposal.md 逐项对照, 该评论描述的方案已经过时**:
  1. 评论: 「从 `refs/remotes/<remote>/HEAD` 解析」——proposal.md §非目标(209 行) 明确放弃:「**不引入** `main_branch` 自动解析 (`symbolic-ref` / `ls-remote --symref`) —— R2 实测该路径存在 RC=0 但无 `ref:` 行两态 (unborn / detached), 需独立设计。**必填** + 存在性核验已足以关闭本 Spec 的失效模式」。
  2. 评论: 「verdict 回显 `main_branch_resolved`」——本版 output schema (proposal.md 137-144 行) 没有这个键, 只有 `gate_error.{kind, remote, branch, message}`。
  3. 评论: 「7 条 SC」——本版是 **11 条**(SC-1~SC-11)。
  4. 承重项本身也变了: 评论完全没提 D1 (SKILL.md 结构重整), 因为它写于 R3 「两份实现」根因浮出**之前**。

- **Spec 计划的处置** (proposal.md 50-52 行 + §Impact 226 行「外部 | aria-plugin #137 补 comment (不打删除线)」): 只打算补一句「(a) 与 (b) 的失效机制不同, 本 Spec 治 (b) 并新增跨路径拦截」。**没有提及需要指出/纠正已有评论里那个已被放弃的技术方案**。

**判断「不打删除线, 只补 comment」这个政策本身是否恰当**: 恰当, 且与 owner 自己已经在这个 issue 上实际采用的处置方式 (评论订正、不改 body) 一致——这一点 D9 判对了。**但落地的执行计划不完整**: 如果照字面只补一句关于 (a)/(b) 的说明, 不会纠正已有评论里的 `refs/remotes/<remote>/HEAD` 自动解析方案与 `main_branch_resolved`/7-SC 描述, 这条已过时的评论会继续留在 issue 上, 后续任何人 (包括未来的 AI session 做 issue 归档考古) 读到它会以为那还是最终方案。

**建议**: 补的 comment 除了 (a)/(b) 说明外, 应显式加一句「本 Spec 最终范围与我早前那条评论描述的方案不同: 不做 `symbolic-ref` 自动解析, 改为 `--main-branch` 必填 + `git ls-remote` 存在性核验; 无 `main_branch_resolved` 回显, 新增的是 `gate_error` 附加键; 详见 proposal.md 当前版本」, 使该评论明确被新评论 supersede, 而不是并列存在造成两个互相矛盾的「最终方案」描述。

**anchor**: proposal.md:50-52, 209, 226, 137-144; Forgejo issue `https://forgejo.10cg.pub/10CG/aria-plugin/issues/137`; comment `https://forgejo.10cg.pub/10CG/aria-plugin/issues/137#issuecomment-18015`(`created_at: 2026-08-08T16:37:00Z`)。

**blocks_phase_b**: false (Phase C/D 期间的外部沟通收尾事项, 不阻塞 Phase B 代码实现; 但应把这条并入 §Impact 226 行的动作描述里, 现在改比事后补更省事)

---

## 未发现问题的项目 (核验通过, 供交叉核对)

- **Rule #5**: proposal.md 位于主仓 `openspec/changes/`(非 `standards/openspec/changes/`), 头部自陈「Spec 落主仓 (Rule #5)」, 核验通过, 代码落点 (`aria/` 子模块) 与 Spec 落点 (主仓) 的分离符合 Rule #5 本意 (代码可以在子模块, Spec 必须在主仓)。
- **Rule #1**: 三轮审计 (R1-R3) + 本轮范围重定前的完整根因排查 (§Why 的「同一个算法有两份实现」分析、实测 `aether ci status` 返回同形、`gate_check` 六项全在的核对) 是 Phase A 应有深度的实证, 未见跳过现状理解直接行动的迹象。
- **D1 覆盖完整性 (documentation 一致性维度)**: 检索 `aria/skills/phase-c-integrator/` 全目录 (无 `references/` 子目录) 及全仓其他 SKILL.md, 未发现除目标文件外还有第二处写着 `aether ci status --branch main`裸命令字面量的位置, 也没有其他 Skill 的 SKILL.md 引用本 Skill 的 C.2.4——D1 的修复范围在「AI 还能在别处读到裸命令」这个维度上是完整的, 不存在遗漏的第二落点。
- **SC-1/SC-2/SC-3 涉及的行号与计数**: 逐条用 `grep -n`/`grep -c` 实测, `:167``:243` 的 `--branch main`、`:270` 的 `"branch": "main"`、`:262``:308``:310``:316` 四处 `pre_merge_gate.py` 文件名提及, 与 proposal.md 声称的计数完全一致。
- **`pre_merge_gate.py` 三处 `main` 字面量** (`:21` docstring / `:300` 函数签名 / `:427` CLI default) 与 proposal.md §3 的行号、字面量逐字核对一致。
- **`gate_check:378-386`**: 精确核对为 `not_applicable` 分支的 `if pc is not None and pc.get("decision") == "not_applicable": ... return compute_verdict(...)` 代码块, 与 D9 段引用该行号支持「该通路存在」的说法一致。
- **`ci_backends/base.py:29`**: 确认 `state: Literal["passing", "failing", "pending", "not_found"]`, 与 SKILL.md:279 的「历史漂移」注记描述吻合。
- **两个 AB 套件文件存在**: `aria-plugin-benchmarks/ab-suite/phase-c-integrator.json` 与 `.../phase-c-integrator-pre-merge-gate.json` 均存在于仓内, Rule #6 段落引用的 ship 前置条件有实体可核。
- **aria-plugin #127 存在且主题相符**: 核验其标题与正文即为「两套件对 C.2.4 的 D9 surface 措辞覆盖不足」, 与 proposal.md 202 行的引用一致。

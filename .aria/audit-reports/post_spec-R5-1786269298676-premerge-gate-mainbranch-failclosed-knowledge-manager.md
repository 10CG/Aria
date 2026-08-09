---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-09T10:43:39.364Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec Round 5 审计报告 — knowledge-manager

被审对象: `openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md` (271 行, R4-fix 版)
镜头: 规范合规 / 文档一致性 / 外部事实 (knowledge-manager)

> 本轮不复跑编排层已做的 23 项机械自检。六项指定任务逐条实读 SOT / 源码 / git 历史 / Forgejo API, 无一条凭记忆。发现 **1 Critical + 3 Major**, 另两项 (Rule #6 定档 / Rule #8 CLAUDE.md 同步行) 核验**通过**, 记入「未发现问题」供交叉核对。

---

## 审计结论

R4-fix 在**技术设计**主线 (D1-D11, SC-1~12) 上未见我镜头下的新问题, 且我自己 R4 报告的 4 条 Major (FINDING-2/3/4/6) 有三条被**正确采纳**(§版本「PATCH 已排除」框架 / Level 升为 3 / CLAUDE.md 行补入 §Impact / Rule #6「专指→典型」措辞更正)。

但 R4-fix 在**吸收上一轮修法时, 在同一批新写的文字里造出了新的、更细的问题** —— 与本项目本轮以前已反复出现过的模式 (`fix-recurs-in-fallback`) 同形:

1. **§版本新写的「两条成文条款指向不同」是逻辑错误**: `MINOR+` 逐字是下界记号 (本仓 `2026-02-06-version-standardization` 先例把「破坏性变更」记为同记号 `MAJOR+`, 佐证该记号全项目一贯读作"下界"), MAJOR 满足 MINOR+, 二者不冲突; 给定 Spec 自己认定 D5「教科书式破坏性签名变更」, 交集唯一是 MAJOR。「地板=MINOR」的措辞给下游留了一个字面上说得通、实质违反 CLAUDE.md:35 的选项。
2. **「#137 的处置」新写的段落自我制造了一次 (a)/(b) 标签误用, 且实质性地与该 issue 上唯一一条已发布评论正面冲突**: 我独立 `forgejo GET` issue 正文与评论后确认 —— comment 18015 逐字订正「(a) 腿的判断是错的…我把两件事混成一件了」, 而本 Spec 逐字写「#137 正文关于『(a) 腿』的陈述**成立**」。这不是转述精度问题, 是**未经新证据就断言了一个已被作者本人公开撤回的判断**, 且 §Impact:232 计划据此发一条「不打删除线 + supersede」的公开评论。若照字面执行, 会在公开 issue 上留下自相矛盾的记录。
3. **§Impact 仍未列发版同步面**, 而这恰是姊妹 Spec (同一天) 用整行钉住、并已开 **Aria #177** 明确预警"会原样重犯"的那类缺口 —— 我读了 #177 正文, 它字面写着"那个 Spec 的修法是一次性 grep…下次原样重犯"。本 Spec 就是那个"下次"。
4. **Level 3 交付物**: SOT (`standards/openspec/project.md`) 自身两处表述不一致 (§21 双层 vs §118 单层), 本 Spec 只引后者, 且其自引的升级先例 (`linked-issue-normalization`) 与同一 skill 的前一个 Spec (`phase-c-integrator-ci-path-coverage`) 实际都交付了 `detailed-tasks.yaml`, 本 Spec §Impact 未跟进。

无一条要求推翻 D1-D11 的技术设计; 但 #137 那条 (FINDING-3) 涉及即将发生的公开、不可逆的外部动作, 定为 Critical。

## Verdict

**FAIL** (1 Critical + 3 Major)。

**阻塞判断**:
- **不阻塞 Phase B 代码实现**: 全部 4 条 finding 都定位在 §Why / §版本 / §Impact 的文字层, 不触及 D1-D11 的技术设计, `blocks_phase_b` 均为 `false`。
- **FINDING-3 (Critical) 必须在 §Impact:232 的「补 comment」动作被执行前修正** —— 这是一个会写进公开 issue、且发出后不易撤回的动作 (issue 政策是"不打删除线, 只补评论", 意味着错误的评论会和正确的评论一起永久留在 thread 里)。建议在进入 Phase C/D 执行该动作前, 由 owner 或后续轮次显式核验修正后的措辞。
- FINDING-1 / 2 / 4 建议随 Phase A 收口一并改掉 (成本都是"改几行文字", 不需要重新设计)。

---

## 轮次记录

- R1-R3: 详见 `.aria/audit-reports/premerge-gate-mainbranch-failclosed-audit-trail.md` (append-only)。核心产出是 R3 推翻前三版共同的范围前提 (SKILL.md 散文步骤与 `pre_merge_gate.py` 是两份独立实现)。
- R4: knowledge-manager (本席前一轮) 产出 4 Major (FINDING-2/3/4/6) + 2 Minor (FINDING-1/5), 0 Critical。见 `.aria/audit-reports/post_spec-R4-1786244936252-premerge-gate-mainbranch-failclosed-knowledge-manager.md`。
- **R5 (本报告)**: 复核 R4-fix 对上轮 4 条 Major 的吸收质量, 而非重跑已收敛的技术设计审查。3/4 条被正确吸收, 但吸收动作本身在两处 (§版本 / #137 处置) 引入了新的、更细粒度的错误 —— 与 `feedback_fix_recurs_in_its_own_fallback_path` 记录的模式同形。本轮另发现 1 条独立于 R4 吸收质量之外的新问题 (发版同步面, 因 Aria #177 是本轮才能核实到的新证据)。

---

## 逐条 Findings

### FINDING-1 (Major) — Level 3 交付物: SOT 自身两处表述不一致, 本 Spec 只引单层一侧, §Impact 未跟进自引先例的实际交付

**定位**: `proposal.md:5`(「Level 3…判据表逐字『Level 3 = Architecture changes, 输出 proposal.md + tasks.md』」) · `proposal.md:230`(§Impact 只有「`openspec/changes/.../tasks.md` | **新建** (Level 3)」一行, 无 `detailed-tasks.yaml`)。

**核验**: `standards/openspec/project.md` 内有两处对 Level 3 输出物的表述, 互不一致:

| 位置 | 逐字 |
|---|---|
| `:21` (「与 Fission-AI OpenSpec 的关系」比较表, 「任务表达」行) | 「Level 3: `proposal.md` + `tasks.md` + `detailed-tasks.yaml` (**双层**)」 |
| `:118` (「OpenSpec Levels」判据表, Output 列) | 「proposal.md + tasks.md」(无 `detailed-tasks.yaml`) |

本 Spec 头部只逐字引用了 `:118`, 未提及 `:21` 的双层表述。而更宽的 SOT 语料佐证 `:21` 不是孤证: `standards/openspec/VALIDATION.md:11` 明文「但从 v2.0 起 aria 选择保留双层任务架构 (proposal.md + tasks.md + detailed-tasks.yaml)」; `standards/core/ten-step-cycle/phase-a-spec-planning.md:619-726` 把 `detailed-tasks.yaml` 定义为 A.2 (task-planner) 阶段的标准产出 (Layer 2), 非可选项。

**实际先例核验** (我独立 `ls` 验证, 非转述): 本 Spec 自己在 `:5` 援引为升级理由的姊妹 Spec `openspec/changes/linked-issue-normalization/` **同时有** `proposal.md` + `tasks.md` + `detailed-tasks.yaml` 三个文件 (后者 60264 字节)。另外, 同一个 skill (`phase-c-integrator`) 的前一个 Spec `openspec/changes/phase-c-integrator-ci-path-coverage/` 与 `aria-2.0-m6-dispatch-input-delivery/` 也都同时具备三个文件。抽样近 15 个 `openspec/archive/` 目录显示项目惯例本身不完全统一 (部分 Level-3 形态的 Spec 只有 `proposal.md`+`tasks.md`), 但**与本 Spec 最直接可比的两个先例 (自引的姊妹 Spec + 同 skill 前一个 Spec) 都交付了双层**。

**消歧建议**: `standards/openspec/project.md:118` 的 Output 列大概率是 A.1 (spec-drafter) 阶段产出的简化速记, 未把 A.2 (task-planner) 的既定产出计入; 建议后续对该 SOT 补一个脚注指回 `:21`, 或统一措辞。本 Spec 层面, 建议 §Impact 补一行 `detailed-tasks.yaml`(与自引先例一致), 或显式写一句「本 Spec 不建 detailed-tasks.yaml, 理由 X」并顺带记一条 SOT 自相矛盾的 follow-up issue —— 二者选一, 不能保持沉默。

**anchor**: `standards/openspec/project.md:21,118`; `standards/openspec/VALIDATION.md:11`; `standards/core/ten-step-cycle/phase-a-spec-planning.md:619-726`; `proposal.md:5,230`; `openspec/changes/linked-issue-normalization/`(ls 实证三文件); `openspec/changes/phase-c-integrator-ci-path-coverage/`(ls 实证三文件)。

**blocks_phase_b**: false (A.2 task-planner 按其既定流程本就会处理; 但应现在把选择写明, 不要延续沉默)

---

### FINDING-2 (Major) — §版本新写的「两条成文条款指向不同」是逻辑错误: `MINOR+` 是下界, 与 `MAJOR` 不冲突, 「地板=MINOR」留了字面合规实为违规的口子

**定位**: `proposal.md:8`(「MINOR vs MAJOR 待 owner 裁」) · `proposal.md:237-241`(§版本正文)。

**逐字核验**: `CLAUDE.md:79`「SemVer。Aria 约定: 新增 Skill / Skill 架构重构 = **MINOR+**; 文档更新 / bug 修复 = PATCH。」`CLAUDE.md:35`「向后兼容 (**破坏性变更须 MAJOR**)」—— 无条件表述, 未见任何「仅限对外契约」类的限定语。

`+` 记号在本项目是**一贯的下界写法**, 非新解读: 该约定的原始出处 `openspec/archive/2026-02-06-version-standardization/proposal.md:69-73` 用**同一套记号**把「破坏性变更」记为 `MAJOR+`(配「1.x → 2.0」的例子), 与「新增 Skill」「Skill 架构重构」并列记为 `MINOR+`; `aria/CHANGELOG.md:1536` 亦有「structural hook refactor with measurable consumer-visible impact = MINOR+」的实际使用, 同样是下界语义 (那次实际落地版本高于最低要求)。

⇒ `MAJOR ∈ MINOR+`(MAJOR 满足"至少 MINOR"), 两条款**不冲突**, 而是**复合**: D1 (Skill 架构重构) 定下 MINOR 下界, D5 若真是破坏性变更则由 `:35` 进一步抬升到 MAJOR。而 proposal.md 自己在 `:241` 逐字断言「D5 使 CLI 参数由可选变必填…是**教科书式破坏性签名变更**」—— 没有用任何"是否算对外契约"这类保留语气。给定这个自我认定成立, 交集是**唯一**的: MAJOR, 不存在"按 bug 修复读 ⇒ PATCH"或"MINOR 也说得过去"的合法分支。

**后果**: 「地板 = MINOR」这个措辞本身没错 (MINOR 确实是下界), 但把 MAJOR vs MINOR 呈现为"两个选项由 owner 挑一个"会让读者误以为 MINOR 是可以落地的终态选项之一 —— 而 Spec 自己的 D5 认定已经把这条路堵死。这与 CLAUDE.md:35 是不可协商规则外的「协作原则」表述, 但仍是逐字成文, 没有豁免通道。

**建议**: 把 §版本改写为「MINOR 是下界 (CLAUDE.md:79); D5 属教科书式破坏性签名变更 (proposal.md:241 自陈) ⇒ 按 CLAUDE.md:35 进一步定为 MAJOR, 除非 owner 认定 D5 不构成对外契约破坏 (此时改列举理由, 而非留白)」——把"是否选 MAJOR"的裁量收窄到"D5 算不算对外契约"这一个真问题上, 不要让读者以为 MINOR 和 MAJOR 是同一逻辑层面的平行选项。

**anchor**: `CLAUDE.md:35,79`; `proposal.md:8,237-241`; `openspec/archive/2026-02-06-version-standardization/proposal.md:69-73`; `aria/CHANGELOG.md:1536`。

**blocks_phase_b**: false (版本号本就到 ship 时才计算; 但推理措辞现在就该改, 否则会把一个已定的问题重新说成待定的)

---

### FINDING-3 (Critical) — 「#137 的处置」新写段落: (a)/(b) 标签自相矛盾且与项目/issue 双重既定编号相悖, 且实质性断言与已发布的唯一评论正面冲突

**定位**: `proposal.md:34-36`(§Why「#137 的处置」) · `proposal.md:232`(§Impact「外部」行)。

Spec 逐字:
> 「#137 报的 (a) helper 缺省是真缺陷, 但它只是两个病因之一; (b) 散文裸命令未被覆盖。#137 正文关于「(a) 腿」的陈述**成立** (`gate_check:378-386` 确证 `not_applicable` 通路存在) ⇒ **不在 body 打删除线**; 只补一条 comment, 且该 comment 须**显式 supersede** 早先那条…评论」

**外部核验 (只读, 均已实读)**:

1. `forgejo GET /repos/10CG/aria-plugin/issues/137` — issue 正文自己的 (a)/(b) 定义逐字是: 「**(b)** `pre_merge_gate.py:427` 的 `--main-branch` 缺省是 `"main"`…」/「**(a)** 变更路径经 `path_coverage` 判 `not_applicable` 时 PR CI 等待步被跳过」。即: **issue 的 (a) = path_coverage 那条腿, (b) = helper 缺省那条腿**。
2. `forgejo GET /repos/10CG/aria-plugin/issues/137/comments` — 该 issue **仅有一条评论**, id `18015`(`created_at: 2026-08-08T16:37:00Z`, 作者即 issue 作者 simonfish), 标题逐字「⚠️ 订正正文一处: 『两条腿都失败为绿』不成立 —— **只有 (b) 那条**」, 正文逐字: 「我在正文里对 **(a) 那条腿**的判断是错的…正文观测到的 `not_applicable` 来自『两仓 workflow 的 paths 真的不覆盖本次变更文件』这个**设计内条件**, **与分支名无关**。我把两件事混成一件了。」
3. `CLAUDE.md:113` 逐字「(a) 本 PR CI passing; (b) main 无 in-flight CI run」—— 这是本项目 Rule #8 的**canonical** (a)/(b) 编号, 与 issue 正文的编号一致 (issue 的 (a)=PR CI 侧的 path_coverage 前置行为, (b)=main in-flight 侧的 helper 缺省)。

**三处独立问题**:

- **标签冲突**: 本 Spec 自己的「(a) helper 缺省」定义, 同时**与 issue 正文自己的 (a)/(b) 编号相反**、也**与 CLAUDE.md:113 的项目级 canonical 编号相反** —— 两处 SOT 一致认为 helper 缺省是 **(b)**, 本 Spec 却叫它 (a)。而 Spec 段落后半句「#137 正文关于『(a) 腿』的陈述成立」里的「(a) 腿」从上下文 (`gate_check:378-386` 关于 `not_applicable` 的引用) 看指的其实是 path_coverage 那条 —— 即同一段文字里 "(a)" 前后两次出现指了两个不同东西, 自相矛盾。
- **事实冲突**: 抛开标签, 单看实质断言「#137 正文关于『path_coverage/not_applicable 那条腿』的陈述**成立**」——这与 comment 18015 逐字「**我在正文里对 (a) 那条腿的判断是错的**」正面相反, 且本 Spec 没有提出任何推翻这条已发布订正的新证据。
- **举证不成立**: 本 Spec 用 `gate_check:378-386` 证明 `not_applicable` **通路存在**, 但 comment 18015 从未否认通路存在 —— 它订正的是"该通路是否由分支名错误触发", 是完全不同的问题。用"通路存在"回应"是否由分支名触发"是答非所问。

**后果不是纸面的**: `§Impact:232` 计划「aria-plugin #137 补 comment (**不打删除线**, 且须 **supersede** 早先…评论)」。若照 §Why 当前措辞落地执行, 会在**公开** issue 上发一条 (i) 重申作者本人已公开撤回的判断、(ii) 把那条撤回评论标记为被 supersede、(iii) 用与项目/issue 双重既定编号相反的腿号描述"本 Spec 治哪条腿"的评论。issue 政策是"不打删除线", 意味着这类错误评论会与已有的正确评论一起**永久共存**在同一个 thread 里, 制造出对未来读者 (含未来的 AI session 做 issue 考古) 而言自相矛盾的记录。

**introduced_by_r4fix**: **true**。我自己 R4 的 FINDING-6 (`.aria/audit-reports/post_spec-R4-1786244936252-premerge-gate-mainbranch-failclosed-knowledge-manager.md:149-170`) 当时只要求"补一句 supersede 已放弃的技术方案", 并且**在那次报告里正确复述了 comment 18015 对 (a) 腿的订正内容**。R4-fix 采纳了"要 supersede"这一半, 但在吸收这条建议时, 同一段落里新写了与 18015 的订正**正面相反**的「(a) 腿的陈述成立」——即在修复上一轮问题的同一段文字里, 造出了一个新的同源问题 (`feedback_fix_recurs_in_its_own_fallback_path` 同形)。

**建议**: 重写「#137 的处置」段, 统一用项目 canonical 编号 (CLAUDE.md:113 的 (a)=PR CI / (b)=main in-flight), 明确本 Spec 治的是 (b); 对 issue 正文的 (a) 腿论述, 应原样采纳 comment 18015 的订正 (不成立, 原因是 `not_applicable` 由 workflow paths 配置触发、与分支名无关), 而不是重新断言它"成立"。补的 comment 应显式确认这条订正 (「同意 18015 对 (a) 腿的订正, 本 Spec 范围限定在 (b)」), 而非与之对立。

**anchor**: `proposal.md:34-36,232`; Forgejo issue `https://forgejo.10cg.pub/10CG/aria-plugin/issues/137`(body, 已实读); comment `https://forgejo.10cg.pub/10CG/aria-plugin/issues/137#issuecomment-18015`(已实读); `CLAUDE.md:113`; `.aria/audit-reports/post_spec-R4-1786244936252-premerge-gate-mainbranch-failclosed-knowledge-manager.md:149-170`(我自己上一轮报告, 核对未走样)。

**blocks_phase_b**: false (外部沟通动作发生在 Phase C/D, 不影响 Phase B 的 D1-D11 代码实现; 但必须在该动作被执行前修正, 且这是一次性、不可静默撤回的公开动作, 优先级高于其余三条)

---

### FINDING-4 (Major) — §Impact 仍未列发版同步面, 而这正是姊妹 Spec 同日开出的 Aria #177 明确预警"会原样重犯"的那类缺口, 本 Spec 是它预言的样本

**定位**: `proposal.md:224-233`(§Impact 全表, 无「发版同步面」行) · `proposal.md:237`(§版本, 只写「号段落地时按 plugin.json 当前版本计算」, 未提同步面)。

**核验**: 本 Spec 承重项 D1 定性为「SKILL.md §C.2.4 结构重整」, §版本已定「地板 = MINOR」(FINDING-2 进一步论证应为 MAJOR) —— 无论哪个, 都是一次会触发 `aria/.claude-plugin/plugin.json` 版本号变更的 Skill 发布。按 `CLAUDE.md:81`「发布同步面: aria 子模块 5 文件 + 主仓 gitlink + 主仓 VERSION + root README badge + i18n README」, 这类发布理应有对应的同步动作, 但本 Spec §Impact 通篇没有这一行。

**姊妹 Spec 对照**: `openspec/changes/linked-issue-normalization/proposal.md:271` 用整行显式列出「**普通引用文件 18 个引用点**: 主仓 14…+ aria 侧 4…; **append-only 账本 2 个**…外加主仓 **gitlink**」, 并注明「⛔ 两条 enabled custom check 不是机械兜底」, 末尾写「类级根因 (`CLAUDE.md:81` 同款错误清单) 已开 **Aria #177**」。

**外部核验 (已实读)**: `forgejo GET /repos/10CG/Aria/issues/177` —— 标题「[governance] CLAUDE.md:81 发布同步面那行是漏同步面的类级根因 — 四错一行」。正文逐字: 「发现于 `linked-issue-normalization` 的 post_planning 审计…**那个 Spec 的修法是一次性 grep, 会随 Spec 归档离场 ⇒ 下次原样重犯**, 故按类开号。」并列出四个具体错误 (按文件数枚举而非引用点数 / 漏 CLAUDE.md 自己 / 漏 `Plugin Version:` 行 / 两条 custom check 对 7 处残留旧版本结构性失明)。

⇒ Aria #177 在开号时明确预言"这个缺口会在下一个 Spec 原样重犯", 而本 Spec (同一天, 同一批工作) 目前的 §Impact 状态**正是**那个预言的兑现: 完全没有发版同步面的枚举, 遑论 18 引用点级别的精度。这不是"本 Spec 独立发生的小疏漏", 是一个刚被开号预警的系统性问题的即时复现样本。

**建议**: §Impact 补一行"发版同步面", 内容可以直接复用 `linked-issue-normalization` 的口径 (版本引用点, 非文件数) 并引 Aria #177, 或至少写一句"本 Spec ship 时须核对 CLAUDE.md:81 全部引用点, 已知两条 custom check 对此结构性失明 (#177)"。

**anchor**: `proposal.md:224-233,237`; `CLAUDE.md:81`; `openspec/changes/linked-issue-normalization/proposal.md:271`; Forgejo issue `https://forgejo.10cg.pub/10CG/Aria/issues/177`(已实读)。

**blocks_phase_b**: false (发版动作在 Phase C/D; 但现在补一行成本很低, 且有现成模板可抄)

---

## 未发现问题的项目 (核验通过, 供交叉核对)

- **Rule #6 定档与 `rule6_note`**: 逐字核对 `standards/conventions/skill-benchmark-exemption.md:29,33`——「`description` 或指令流程变动 ⇒ 一律第二行」全字匹配 `proposal.md:201` 的引用; D1 (SKILL.md 指令流程重整) 落入该条款无歧义。`proposal.md:203`「SOT 对第三行的措辞是『典型: authoring 向导』——authoring 是举例不是定义」已正确采纳我自己 R4 FINDING-1 的建议 (把「专指」改回「典型」), 上一轮的 Minor 已解决, 未见新问题。`rule6_note` 在「无论走哪一行都要留痕」的口径下 (`skill-benchmark-exemption.md:55`) 形式合规。
- **Rule #8 CLAUDE.md 同步行 (`proposal.md:229`)**: 我自己 R4 FINDING-4 当时的建议是"篇幅可以很短…但不能不提", 现有一行 (「规则 #8 那段须同步…先例: v1.31.0…`commit 7661e96`」) 达到这个门槛。本轮独立重跑 `git show 7661e964b0f9d262ed2a28798b20d0d39b6cb6da -- CLAUDE.md` 复核该先例实际改动范围: 确认它不止加一句话, 而是重写了「规则 #8 要点」整段措辞 + 新增一个带版本标签的「NIE-propagation 安全约束 (Hard Constraint #7)」小节 + 同步了 Exception 段的 key 改名 + Primitive responsibility split 列表。当前 proposal.md 的一行 Impact 摘要与先例的**摘要粒度**相称 (先例 Spec 自己的 proposal 阶段大概率也只是摘要, 实际文本在 ship 时才写), 未发现需要现在补足的缺口; 但**注意**: 若 Phase C 撰写实际 CLAUDE.md 新增文字时直接抄 §Why 现有的 (a)/(b) 措辞, 会把 FINDING-3 的标签混淆带进不可协商规则原文, 后果比 issue 评论更严重 —— 已在 FINDING-3 建议里一并提示统一编号。
- **Rule #5**: `proposal.md` 位于主仓 `openspec/changes/`, 代码落点在 `aria/` 子模块, 符合「Spec 落主仓, 代码可落子模块」的既定读法。

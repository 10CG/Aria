---
checkpoint: post_planning
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-08T12:49:49.000Z
context: openspec/changes/linked-issue-normalization/detailed-tasks.yaml
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R3 — qa-engineer 审计报告（仅组 5 / TG-5，owner 裁定范围）

## 方法

只读 `tasks.md` 「## 5.」整段 + `detailed-tasks.yaml` TASK-014/015-021(cancelled)/022-027 + `metadata`。对每条 TASK-022..027 的 verification 做"它怎么会红"审查；对 TASK-024 的双向断言**实跑模拟**（在 scratchpad 用真实文件内容做 4 种场景替换，非纸面推演）；对 TASK-016→delegation 的premise 做**代码级核验**（直接读 `phase-c-integrator/SKILL.md` 与 `branch-manager/SKILL.md` 的实际合并机制，而非只信 tasks.md 的引用转述）；核对我 R2 的 2 条 minor 是否闭合；重算 yaml 底部派生值。

---

## 一、R2 两条 minor 的闭合判定

**minor-1（TASK-021(b) 存档报告缺路径/命名/SHA 约定）— 未闭合，carryover**。
TASK-025（取代 TASK-021）第 3 条 verification 逐字仍是："(b) 显式退役: baseline 结果冻结成带 SHA 的存档报告, 脚本移出 `.aria/repro/` + 同批修 `proposal.md:181/:219` 两处 artifact 指针" —— "带 SHA 的存档报告"仍未给出具体落点路径/命名格式/SHA 语义（是脚本末次修改 SHA？`collision.py` 落地 SHA？归档 commit SHA？落在 `.aria/audit-reports/`？内联进 audit-trail？）。我 R2 给出的具体建议（`sc-baseline-linked-issue-normalization-archived-<merge-SHA>.md` 格式）未被采纳。**我 R2 已判定此项不阻塞、可留给 Phase B 实施者自行决定**，本轮维持同一判断：仍是软点，不升级，但确认为**未处置**，非"已处置后我看漏"。

**minor-2（场景齐备性无机械锚点，建议 SC-ID 内联注释）— 未闭合，carryover，符合预期**。
`grep -rn "# SC-\|SC-[0-9]" aria/skills/state-scanner/tests/test_release_by_track.py` 本轮重跑仍无输出；TASK-014 verification 仍是纯人工"逐 SC 清单核对"。这条我在 R2 已明确定性为"建议，非阻塞，可留给 Phase B 实施者决定"，故其未被采纳不构成本轮缺陷，只是确认状态未变。

---

## 二、TASK-022..027 逐条"它怎么会红" + 实跑验证

### TASK-024（双向断言）—— 实跑 4 种场景，结论：**核心设计经受住测试**，但发现一处新维度缺口

在 `/tmp/.../scratchpad/task024-sim/` 用真实文件内容（README.md/zh/ja/ko、CLAUDE.md、VERSION、aria 侧 plugin.json/marketplace.json/README.md/VERSION）实现了 TASK-024 描述的判据（普通引用文件双向计数 + 账本文件头部行比对），跑了四个场景：

- **(a) 当前工作树（未 bump）**：`OVERALL: RED`。9 个普通引用文件全部因"旧值非零命中"发红（20 处命中，与 metadata 14+6 精确吻合）；账本文件因头部 == plugin.json（都还是 1.65.5）而 OK。**结论：会红，且红在正确的维度上。**
- **(b) 正确 bump 后**：`OVERALL: GREEN`。全部 9 个普通文件 old=0/new=expected，账本头部 == SOT。**结论：会绿。**
- **(c) 模拟漏改 README.md 的"Plugin Version:"行**（R1/code-reviewer Critical-1 原始缺陷的精确复现）：`README.md: old=1 new=1 expected=2 -> RED`，`OVERALL: RED`。**结论：会红 —— 这正是本组重做要堵的洞，堵住了。**
- **(d) 模拟新版本号打错为 1.66.1**（R2/tech-lead N3 指出的"缺席断言"漏洞类型）：`README.md: old=0 new=0 expected=2 -> RED`（旧值零命中会误判绿，但新值计数缺口 0≠2 抓住）。**结论：会红 —— 双向断言的"新值出现次数==预期点数"这一半正是为了堵这个洞，堵住了。**

**结论**：TASK-024 描述的判据本身是**可证伪且维度匹配**的，我 R2 提出的"场景齐备性无机械锚点"那类软点在这里不适用——这条断言逻辑扎实。

**但发现一个新缺口（本轮新增，见 Major-1）**：追加场景 (e)——账本文件 `aria/VERSION` 头部正确 bump 到 1.66.0，但**历史行被整体清空**（模拟"实施者写了个脚本重写整个文件、只保留头部"这一实现错误）：断言仍报 `OVERALL: GREEN`。TASK-022 verification 明文要求"历史行原样保留"，但 TASK-024 的判据只检查"头部行 == SOT"，**不检查历史是否被销毁**。这是一个无向检查对特定错误维度（历史完整性）天然免疫的案例——与本 Spec 自己反复引用的 memory `feedback_invariant_dimension_must_match_error_dimension` 是同一形状，且恰好发生在**专门为修复这类维度不匹配而重写的任务本身**（讽刺点：TASK-024 就是为了堵住 TASK-020 的维度不匹配洞而生的）。

**次要观察（Minor，非阻塞）**：TASK-020（已 cancelled）原文给出可直接复制运行的单条 `grep -rn` 命令；TASK-024 只给出散文化的双向判据描述 + 指向 `metadata.version_reference_surface.breakdown` 的枚举表，没有给出等价的可直接运行命令。这在设计上可以理解（双向 + 逐文件计数很难压成一行 grep），且枚举表本身是精确的（我据此写的模拟脚本可以机械导出），所以不算不可证伪，但**相对 TASK-020 的具体程度是一个可感知的倒退**，留给 Phase B 实施者更多"如何写这个校验脚本"的自由度。

### TASK-025（sc-baseline 处置）—— 二选一可判，但验收数组本身有表达问题

**"二选一的合取型 verification 数组本身可判吗？"** —— 可判，但不理想：

verification 列表的前两条（"路径一（恒红）:...已处置" / "路径二（归档后）:...已处置"）读起来像是在**陈述结论**（"已处置"），而不是给出可在任务执行后独立核验的判据；它们实质上是把 notes 段的问题陈述搬进了 verification 数组，与真正可判的第 3 条（"(a) / (b) 择一并成文"）和第 4 条（"substitute 论证可复核性仍成立"）功能重叠但表达方式不同。这是**叙事与判据混排**的软性缺陷——不是新问题的类型，但值得指出：本组恰恰是因为"叙事与判据混排"曾致其他任务被判非阻塞软点（如 minor-1 的"带 SHA 的存档报告"）。

按分支拆开看，是否可判：
- 分支 (a)：可判——"新增 post-implementation 模式，断言 8 条 SC 已转绿 + 同时解决归档后解析路径" 是具体、可重跑验证的（exit code）。
- 分支 (b)：**部分可判**——"脚本移出 `.aria/repro/`"、"同批修 `proposal.md:181/:219`" 可机械核验（`git status` + grep）；但"带 SHA 的存档报告"本身（即 minor-1 carryover）仍缺路径/命名/SHA 语义约定，这部分不可机械核验，只能人工判断"看起来像不像"。

### TASK-027（AB 门范围披露）—— "成文披露"与"开 issue"怎么机械判定

- **"开 issue"**：可机械判定（Forgejo issue 存在性 + 标题/内容关键词可查），但 TASK-027 本身**没有要求把 issue 号记录进任何 deliverable**——完成后审阅者若要核验，只能去 Forgejo 搜索日期范围内的 issue 列表，没有直接锚点。
- **"成文披露"**：`deliverables: [".aria/decisions/ (披露记录（或并入本 change 的 handoff）)"]` —— 给了**两个候选位置**且用"或"连接，没有钉死落在哪一个。这与 TASK-025(b) 的"带 SHA 的存档报告缺具体路径"是**同一形状**（memory `feedback_fix_the_class_not_the_instance`）：本组两处新/改任务（TASK-025 承袭自 TASK-021 的老问题、TASK-027 是全新任务）都把"存档/披露记录该落在哪个文件"这一具体决定留给了执行者，而这正是本组从"逐条补丁"升级为"整组重derive"想要根治的那类不精确。

### TASK-026（交付 Phase C）—— 两条验收够吗？"显式告知"怎么判？以及本轮的核心发现

TASK-026 verification 只有两条硬性条款（TASK-024 通过 + 交接时显式告知待合并分支名）+ 一条"不复述"声明。

**"显式告知"怎么判**：Aria 的 Layer1/Layer2 通信模式本就是"拟人命令（自然语言 YAML）"（CLAUDE.md 明文），本 Spec 场景是交互式 session（非 Aria 2.0 无人值守流水线），所以"显式告知"预期是 AI 在调用 `phase-c-integrator` 前的对话/交接文本里陈述分支名与 bump 状态——这在**该项目自身的通信设计下是合理的**，可以靠"读那一段对话/commit 序列"人工核验，不是没有判据，只是没有机械锚点。**单独看，这条不足以构成缺陷**，与 R2 已确认非阻塞的"场景齐备性无机械锚点"同类。

**但两条验收"够吗"这个问题的真正答案是"不够"，原因不在这两条本身，而在于它们共同构成的信任前提被证伪**：

---

## 三、Critical-1 —— TASK-016 委派的核心依据（SKILL.md:242）经直接读码证伪

tasks.md:28 与 detailed-tasks.yaml:59-62 把 TASK-016（本地 git merge + 双推 + 逐远端 ls-remote 核验）cancel 的理由写为：

> "该 Skill（`SKILL.md:242`）本就建模子模块合并"

我直接读了 `phase-c-integrator/SKILL.md:242`（引用出处本身）：

```
242	2.5. **Path coverage 评估**...**执行上下文契约**: 在执行 C.2 合并的目标仓根内调用
     （子模块合并 → 子模块根）; `main_branch` 显式传真值...
```

这一行讲的是 **path-coverage CI 门在哪个目录上下文里跑 CI 评估**（子模块合并时评估器要切到子模块根目录），**与"合并动作本身走本地 git merge 还是 Forgejo 服务端 merge"是两件完全不同的事**。引用的行号存在，但支撑的是一个更窄的主张（"该 Skill 感知子模块存在并调整 CI 评估上下文"），不支撑 tasks.md 实际拿它论证的主张（"该 Skill 已经正确实现子模块的本地合并语义"）——这是 memory `feedback_issue_reporter_root_cause_may_miscite` 描述的精确实例。

进一步**直接核验合并动作本身**（不是 CI 门，是"谁来 merge PR"）：

- `phase-c-integrator/SKILL.md:236`："branch-manager (C.2.4-C.2.5) | wait approval + **merge API call**" —— 合并动作被点名委派给 branch-manager，且明写是 **API call**。
- `branch-manager/SKILL.md:528-534`（其内部 C.2.5"合并"步骤）："调用 Forgejo API 合并 PR" —— 实际命令在 `:625-634`：
  ```bash
  curl -X POST "${FORGEJO_API}/repos/.../pulls/{pr_number}/merge" \
    -H "Authorization: token ${FORGEJO_TOKEN}" \
    -d '{"Do": "merge"}'
  ```
  这**逐字**就是 CLAUDE.md 约束 1 明文禁止的动作："**禁**用 Forgejo Web UI / **API** 的 `Do: merge`"。
- `branch-manager/SKILL.md:663-675`「子模块 PR 注意事项」章节——这是该 Skill **唯一**专门讲子模块 PR 流程的地方——原文步骤 2 只写"合并后，回到主仓库"，**未提供任何区别于主仓 PR 的、走本地 `git merge` 的替代路径**。也就是说该 Skill 对"子模块 PR"的唯一已知处理方式，就是复用同一个 repo-type-agnostic 的 Forgejo API merge。
- 全仓 grep `服务端合并|一律本地做|orphaned gitlink` 在 `aria/skills/` 下**零命中**（唯一命中是一个测试 fixture json，非实际逻辑）：CLAUDE.md 约束 1 这条 owner 亲写的硬约束，在 phase-c-integrator / branch-manager / git-remote-helper 三个相关 Skill 的 SKILL.md 里**没有任何字面对应的分支判断**。

**这意味着什么**：TASK-016 被 cancel 时，其最关键的一条判据（"本地 git merge，不得走服务端 API merge"）**没有被任何东西继承**——不是被 TASK-026 复述（TASK-026 明确声明"不复述"），也不是被 phase-c-integrator/branch-manager 的既有机制隐式覆盖（我直接读码证明它没有）。C.2.5 Multi-Remote Push Enforcement（`verify_parity_post_push`）确实会在"本地从未 fast-forward"时检测到 SHA 不一致（这点 R2/tech-lead 已论证，我认同），**但前提是它真的会被触发**——它的触发条件明文是"Phase C.2 合并成功（master 已 fast-forward）"，如果合并走的是 Forgejo API 且之后没有可靠的本地同步步骤，这个触发条件本身可能不成立，检测机制可能根本不会跑（这正是 CLAUDE.md 对 2026-07-14 事故的复盘原文："本地双推与 C.2.5 结构上都不触发"）。

（诚实的不确定性：branch-manager 合并步骤在"删除本地分支"之后写了"切换回 develop **并更新**"，这个"更新"如果真的做了 `fetch`+同步本地 ref，理论上可能挽救最坏情形——但这只是我从措辞推断，SKILL.md 没有给出这一步的具体命令，无法确认它真的会把子模块 master 同步到位。这个不确定性本身就是问题：一个防真实生产事故复发的硬约束，其实际保障链条要靠对一句模糊措辞的乐观解读才能站住。)

**为什么这是本轮（而非历史遗留）的问题**：TASK-016 在 R1/R1-fix/R2 三轮里始终作为一个**独立、显式的任务**存在，且其 verification 逐条钉死了"本地 merge / 双推 / 逐远端核验 / 不信回执"四条硬判据——只要它作为任务存在，无论 phase-c-integrator 底层机制如何，这个安全网都在。**是本轮（R2-fix）的 cancel 决定移除了这个安全网**，其移除理由（"下游机制已经保证"）经直接读码不成立。TASK-026 明确放弃复述 C.2.4/C.2.5 的判据，意味着**目前的计划里没有任何一处会在 Phase C 实际执行子模块合并时拦住"不小心点了 Forgejo 服务端 merge"这一具体失败模式**——而这恰是 CLAUDE.md 用一整段"两条硬约束"、点名 2026-07-14 事故编号来防的那件事。

**建议**：在本 Spec 交付 Phase C（TASK-026）之前，由 owner 或独立 agent 对 `phase-c-integrator` 实际执行子模块 PR 合并时的行为做一次**探针式验证**（不修复，先证实/证伪：找一个低风险子模块 PR，观察合并后本地 master 是否真的通过某种机制同步到位，还是仍停留在 API 调用前状态），而不是继续基于"SKILL.md:242 已经建模了"这句话推进；若探针证实缺口，需要在 phase-c-integrator/branch-manager 层面（而非本 Spec 内）补上"子模块 repo 一律走本地 `git merge`，不调用 Forgejo merge API"的显式分支判断，这是 CLAUDE.md 约束 1 本该有、但目前代码里没有的机制化落地（对齐 memory `feedback_mirror_sync_needs_mechanical_backstop`：靠纪律的同步对服务端合并路径无效，须机械兜底）。这条修复本身超出本 Spec 范围，但**本 Spec 不应在这条修复完成前把 TASK-026 当作"安全交接"来对待**。

---

## 四、静默丢失清单（7 条 cancelled，逐条核对 verification 全覆盖）

| 原任务 | 原 verification 要点 | 接任条 | 覆盖判定 |
|---|---|---|---|
| TASK-015 (5.2) | plugin.json SOT 一致 / MINOR / CHANGELOG 措辞 | TASK-022 | **全覆盖**，且新增 marketplace.json 第二字段 + 账本口径，严格超集 |
| TASK-016 (5.3) | 本地 merge（非服务端）/ 双推 / 逐远端 ls-remote / 不信回执 | phase-c-integrator C.2.5（delegation） | **"本地 merge 非服务端"这一条经核验未被真正承接** —— 见上方 Critical-1；其余 3 条（双推/逐远端核验/不信回执）被 C.2.5 的 `push_all_remotes` + `verify_parity_post_push` 结构性承接，判定覆盖 |
| TASK-017 (5.4) | gitlink 指向**合并后 master SHA**（非 feature 分支）/ README 两处 / badge check | TASK-023（版本面）+ TASK-026（gitlink，仅 prose 提及，未入 verification 数组） | README 两处：**全覆盖**（TASK-023）。gitlink 精确指向"合并后 SHA"：**只在 tasks.md prose 与 yaml metadata 里以文字承诺"由 C.2.5 保证"，TASK-026 的 3 条 verification 未把它列为独立判据项**；且我核验 C.2.4.5（Submodule Pointer Regression Gate）防的是"回退/发散"，不是"精确等于最新合并 SHA"——是相关但不同的不变量。轻度关注，未独立列 severity（已并入 Critical-1 的证据链，同一根因：委派链条的判据比原任务弱） |
| TASK-018 (5.5) | i18n 3 文件各 3 处 / 不重译正文 / currency check | TASK-023 | **全覆盖**，逐字重现 |
| TASK-019 (5.6) | CLAUDE.md 两处 / 不写设计术语 / 15-20 行预算 | TASK-023 | **全覆盖**，三条逐字保留 |
| TASK-020 (5.7) | 版本引用点归零（含 3 处已知坏：账本恒红/单向断言/排序过晚） | TASK-024 | **全覆盖 + 修复三坏点**（实跑确认，见二.TASK-024）；**新增缺口**：账本历史完整性不受检（Major-1，本轮新发现） |
| TASK-021 (5.8) | 恒红两条失效路径处置 / (a)(b) 二选一 / 存档报告带 SHA | TASK-025 | 两条失效路径：**全覆盖**。存档报告路径/命名/SHA 语义：**未覆盖，carryover minor（R2 已知，未处置）** |

**结论**：7 条中 6 条无实质静默丢失（TASK-015/018/019/020/021 全覆盖或超集，020 的新缺口是新发现不是丢失）；**TASK-016 是唯一真正的静默丢失**——其最关键判据被"已由下游覆盖"的不实主张顶替，而非被显式承接或显式放弃。TASK-017 的"精确 SHA"判据强度也有边际弱化，作为同一根因的次要症状记录，不单独计分。

---

## 五、派生值重算

```
$ python3 -c "import yaml,collections as c; t=[i for i in yaml.safe_load(open('detailed-tasks.yaml'))['tasks'] if i['status']!='cancelled']; x=c.Counter(i['complexity'] for i in t); a=c.Counter(i['agent'] for i in t); print(len(t),'active |',dict(x),'|',x['S']*3+x['M']*6+x['L']*10,'h |',dict(a))"
20 active | {'M': 5, 'S': 14, 'L': 1} | 82 h | {'qa-engineer': 10, 'backend-architect': 6, 'knowledge-manager': 4}
```

- 总任务 27（`grep -c '^\s*- id: TASK-' detailed-tasks.yaml` 独立核对 = 27）
- active 20 / cancelled 7（TASK-015..021，逐一核对 `status: cancelled` 字段）
- active 复杂度 S×14 · M×5 · L×1，工时 14×3+5×6+1×10 = 42+30+10 = **82h**
- active agent 分摊 qa-engineer×10 · backend-architect×6 · knowledge-manager×4，10+6+4=20 ✓
- 主仓引用点 14（README.md:2/zh:3/ja:3/ko:3/CLAUDE.md:2/VERSION:1，`grep -c` 逐文件核对，与 metadata.breakdown 精确吻合）

**与 yaml 底部 footer（`27 条 = 20 active + 7 cancelled`；`S ×14 · M ×5 · L ×1`；`≈82h`；`qa-engineer ×10 · backend-architect ×6 · knowledge-manager ×4`）逐字段吻合，无 drift。**（此前两次 footer 写错：A.3 首版 S×12/M×4/67h，R1-fix 版 Agent 8/7/6；本轮第三次核对，未复发。）

---

## 六、Findings

- type: defect / gap
  severity: critical
  category: architecture / silent-loss
  scope: detailed-tasks.yaml TASK-016 (cancelled) → phase-c-integrator delegation (metadata.scope_boundary.delegated, tasks.md:28-32); TASK-026 (5.13)
  origin: new（R2-fix 的 cancel 决定本身引入；机制缺陷本身先于本 Spec 存在，但"依赖它作为安全网"这一决定是本轮新做的）
  summary: TASK-016 被 cancel 的依据（"该 Skill SKILL.md:242 本就建模子模块合并"）经直接读码不成立；引用的 :242 行讲的是 CI path-coverage 评估的执行上下文，不是合并机制本身。实际合并动作（branch-manager 内部 C.2.5，`SKILL.md:625-634`）是 repo-type-agnostic 的 Forgejo API `Do: merge` 调用——逐字命中 CLAUDE.md 约束 1 明文禁止的动作；该 Skill 唯一的"子模块 PR 流程"专节（`branch-manager/SKILL.md:663-675`）也未提供本地-merge 的替代路径。TASK-026 明确声明"不复述 C.2.5/C.2.4 判据"，意味着若上述缺口属实，当前计划里没有任何环节会在 Phase C 实际合并 aria 子模块时拦住服务端合并，存在复现 2026-07-14 orphaned gitlink 事故的结构性通路。
  evidence: >
    phase-c-integrator/SKILL.md:236 "branch-manager (C.2.4-C.2.5) | wait approval + merge API call";
    branch-manager/SKILL.md:625-634 `curl -X POST .../pulls/{pr_number}/merge -d '{"Do": "merge"}'`（无 repo-type 判断）;
    branch-manager/SKILL.md:663-675「子模块 PR 注意事项」步骤 2 仅"合并后，回到主仓库"，无本地 merge 分支;
    `grep -rln "服务端合并\|一律本地做\|orphaned gitlink" aria/skills/` 零命中（除测试 fixture）;
    phase-c-integrator/SKILL.md:242 实际内容为 path-coverage 执行上下文声明，非合并机制声明。
  recommendation: >
    Phase C 执行前先做探针（非修复）: 实测子模块 PR 走 phase-c-integrator/branch-manager 合并后，
    本地 master 是否真同步到位（"切换回 develop 并更新"是否包含足够的 fetch/reset）。若证实缺口，
    需在 phase-c-integrator/branch-manager 补一个 repo-type 判断（子模块 repo 强制走本地 git merge，
    不调用 Forgejo merge API），这是 CLAUDE.md 约束 1 应有但当前代码没有的机制化落地
    (memory feedback_mirror_sync_needs_mechanical_backstop)。在此之前不应把 TASK-026 当作
    "安全交接"处理；至少应在 TASK-026 verification 里加一条"已核实 phase-c-integrator 对子模块 PR
    走本地 merge 而非 Forgejo API merge"作为硬前置，而非完全信任委派。

- type: gap
  severity: major
  category: testing / verification-dimension-mismatch
  scope: detailed-tasks.yaml TASK-024 (5.11) append-only 账本判据; TASK-022 (5.9) "历史行原样保留"要求
  origin: new
  summary: TASK-024 对 append-only 账本（aria/VERSION, aria/CHANGELOG.md）的判据只检查"头部当前版本行 == plugin.json"，不检查历史内容是否被破坏。实跑模拟证实：把 `aria/VERSION` 头部正确 bump 到 1.66.0、但历史行全部删除，TASK-024 描述的判据仍会判绿——而 TASK-022 明文要求"历史行原样保留"。这是本 Spec 反复引用的"无向检查对特定错误维度天然免疫"（memory feedback_invariant_dimension_must_match_error_dimension）在 TASK-024 自身（专为修复这类维度不匹配而生的任务）里的复现。
  evidence: >
    实跑模拟（scratchpad task024-sim/assert.py 场景 e）: aria/VERSION 头部替换为 1.66.0，
    历史 4 行以后全部截断，判据仍报 `header_version=1.66.0 SOT=1.66.0 -> OK`，
    `OVERALL: GREEN`，尽管其余 8 个普通引用文件均正确 bump。
  recommendation: >
    为 TASK-024 补一条账本文件的历史完整性检查，例如: bump 前后除头部块（版本行 + 当次发布日期行）
    外，其余行数与内容逐行不变（`diff` 排除头部后应为空）。不要求本轮返工，但应在 Phase B 执行
    TASK-024 时补入这一条，否则该断言对"实现者用脚本整体重写文件"这一失误模式没有防护。

- type: issue
  severity: minor
  category: process
  scope: detailed-tasks.yaml TASK-025 (5.12) / TASK-027 (5.14) deliverables 路径表述
  origin: mixed（TASK-025(b) 为 carryover, 与我 R2 minor-1 同一处未处置；TASK-027 为 new，本轮新任务复现同一形状）
  summary: TASK-025(b)"带 SHA 的存档报告"与 TASK-027"披露记录（`.aria/decisions/` 或并入本 change 的 handoff）"都把"具体落在哪个文件"这一决定留给执行者，属同一形状的欠约束（memory feedback_fix_the_class_not_the_instance）——本组本轮的核心目的正是消灭这类欠约束，但两处新/改任务里各留了一个同形状实例。
  evidence: >
    TASK-025 verification 第 3 条 (b) 分支: "baseline 结果冻结成带 SHA 的存档报告" 无路径/命名/SHA 语义;
    TASK-027 deliverables: ".aria/decisions/ (披露记录（或并入本 change 的 handoff）)" 用"或"给出
    两个候选而未钉死其一; 且"开 issue"未要求把 issue 号写回任何 deliverable，事后核验无锚点。
  recommendation: >
    Phase B 真正执行这两条任务前各补一句具体路径（如我 R2 给出的 TASK-025 建议示例可直接复用）;
    TASK-027 二选一改为钉死其一（建议 `.aria/decisions/`，与其他同类披露记录一致），并要求把
    Forgejo issue 号写回该文件。不阻塞 Phase B 开工。

- type: issue
  severity: minor
  category: clarity
  scope: detailed-tasks.yaml TASK-025 (5.12) verification 前两条措辞
  origin: new
  summary: verification 数组前两条（"路径一 (恒红): ... 已处置" / "路径二 (归档后): ... 已处置"）是叙事性地复述 notes 里的问题描述并宣称"已处置"，而非给出任务执行后可独立核验的判据；真正可判的内容集中在第 3、4 条。这种叙事与判据混排削弱了 verification 数组本身"逐条独立可证伪"的设计意图（本组其余任务如 TASK-022/023/024 均是纯判据陈述，TASK-025 是本组内唯一夹带叙事的）。
  evidence: "detailed-tasks.yaml:780-781（TASK-025 verification 第 1、2 条原文）"
  recommendation: 将前两条改写为独立判据（如"脚本顶部成文的选择必须同时满足其对应分支覆盖两条失效路径"），或直接归并进 notes，只在 verification 里保留可判的第 3、4 条。不阻塞。

- type: observation
  severity: minor
  category: testing
  scope: detailed-tasks.yaml TASK-024 (5.11) 与 TASK-020 (cancelled, 5.7) 的对比
  origin: new
  summary: TASK-020（已 cancelled）给出可直接复制运行的单条 grep 命令；TASK-024 只用散文 + 枚举表描述双向判据，未给出等价的可运行命令。设计上可理解（双向 + 逐文件计数难压成一行 grep），枚举表本身精确（已用其重建出可运行脚本并验证四种场景），故不算不可证伪，但相对 TASK-020 是可感知的具体化程度倒退，把"如何写这条校验脚本"的自由度让给了 Phase B。
  evidence: 见二.TASK-024 小节倒数第二段;实跑脚本 `/tmp/.../scratchpad/task024-sim/assert.py` 依据 metadata.version_reference_surface.breakdown 精确复现四场景。
  recommendation: 不要求本轮修改；Phase B 实施 TASK-024 时可考虑把本次模拟脚本的逻辑直接沉淀为该任务的落地实现或 `.aria/repro/` 下的核验脚本。

- type: observation
  severity: minor
  category: process
  scope: R2 minor-1（TASK-021→025）/ minor-2（SC-ID 锚点）
  origin: carryover
  summary: 我 R2 的两条 minor 均未在本轮重做中处置；两条在 R2 时已被我本人判定为"不阻塞、可留给 Phase B"，本轮维持同一判断，仅确认状态未变，不升级。
  evidence: 见本报告"一、R2 两条 minor 的闭合判定"。
  recommendation: 无新增，维持 R2 建议，留 Phase B 处理。

---

## Verdict

**verdict: FAIL** / **vote: REVISE**

判据：本轮范围内出现 **1 Critical + 1 Major**，均为本轮（R2-fix 重derive）新引入或新暴露、且未被组内任何其余任务覆盖。Critical-1（TASK-016 委派前提经读码证伪，子模块合并可能仍走 Forgejo 服务端 API，结构性复现 2026-07-14 事故通路）是本轮最重要的发现——它不是"文档措辞不够精确"这类本组前两轮反复出现的软点，而是**一个此前由显式任务防住、本轮被以不实主张移除的真实安全网**，且发现路径（直接读 phase-c-integrator/branch-manager 源码而非只信 tasks.md 转述）是 R1/R2 未做过的独立核验维度。Major-1（TASK-024 账本历史完整性无检查）证明即便是本组专门为"维度匹配"而重写的核心机制，仍留了一个同类维度缺口。

**同时应明确记录的正面结论**：TASK-024 的双向断言设计本身（普通文件的旧值零命中+新值计数、账本文件的头部行比对）经**实跑四场景模拟**证实是扎实的——R1/R2 反复命中的"假绿"（漏改文件、写错版本号）在这次重做里被结构性堵住，这是组 5 重做**确实取得的真实进展**，不应被上述两条新发现淹没。派生值（27/20/7/S14·M5·L1/82h/qa10·ba6·km4/主仓14点）本轮**首次连续第二次**核对精确吻合，无 drift。

## 本轮 fix 引入占比

仅统计 Critical + Major（本项目既有口径，Minor/observation 不计入分母）：本轮 qa-engineer 席位共发现 **2 条 Critical/Major**（Critical-1 委派前提证伪 + Major-1 账本历史完整性缺口），**2 条均为本轮新引入/新暴露（origin: new）**，0 条 carryover 未闭合的 Critical/Major。

**fix 引入占比 = 2/2 = 100%**（n=2，样本极小，需谨慎解读）。

**与前两轮的定性差异（不可直接比较绝对值）**：R1 我本人 2 Major（均后续 closed）；R2 我本人 0 Critical/Major（2 minor）；本轮 2 Critical/Major。但**这两条与 R1/R2 之前命中的"内部文档一致性/措辞精确度"类问题性质不同**——它们来自本轮**新增的核验维度**（直接读外部依赖 Skill 的源码，而非只审 tasks.md/detailed-tasks.yaml 文本自身），R1/R2 均未做这一层核验。是否应把"用新方法论发现的旧缺陷"计入"fix 引入"的分子，本身存疑；我按项目既有定义（本轮新发现 = new）如实计入，但建议 owner 在综合裁决时对这一层区别予以考虑，不要机械套用"占比>1/2 即拐点已过"从而要求再次整组重做——**Critical-1 指向的是委派对象（另一 Skill）的代码缺陷，不是本 Spec 自身文本的缺陷**，其修复路径也不在本 Spec 范围内（探针验证 + 若证实则修 phase-c-integrator，均在本 Spec 之外）。

## 报告路径

`/home/dev/Aria/.aria/audit-reports/post_planning-R3-1786193389568-linked-issue-normalization-qa-engineer.md`

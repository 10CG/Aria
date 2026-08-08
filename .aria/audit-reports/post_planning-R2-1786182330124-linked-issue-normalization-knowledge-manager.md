---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-08T09:45:30.000Z
context: openspec/changes/linked-issue-normalization/detailed-tasks.yaml
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R2 — knowledge-manager 席位审计报告 (R1 同席位)

## 审计范围与方法

对比 R1 (`a52ab81`, 17 任务) 与 R1-fix (`3fc6f3f`, 21 任务): 实读 `tasks.md` (136 行全文)、
`detailed-tasks.yaml` (662 行全文)、`git diff a52ab81 3fc6f3f` 全量 hunk (`tasks.md` + `yaml`
两份)；核对 R1 三条自身 finding 的闭合证据；交叉核 `standards/conventions/claude-md-hygiene.md`
全文、`aria/skills/phase-c-integrator/SKILL.md` §C.2.4/§C.2.5、`aria/skills/phase-d-closer/SKILL.md`
D.1-D.3；实跑 `git submodule status aria`、`grep -n '"version"' aria/.claude-plugin/marketplace.json`、
`grep 1.65.5 aria/README.zh.md`、`ls aria/CLAUDE.md aria/README*.md` 核验 metadata 块与磁盘现实。
已读 code-reviewer / qa-engineer 的 R2 报告，本报告**不重复**主控点名的 6 条已证实发现，
聚焦文档治理 + 人读层完整性这一轴。

---

## 第一部分 — 我 R1 三条 finding 的闭合核验

### major「9 处落点」vs 自身分解 11（两种计数口径并存）— **closed**

R1-fix 把口径统一改为「版本引用点」，新增 `metadata.version_reference_surface`
(`main_repo_points: 14`, 逐文件 `breakdown` README.md:2/zh:3/ja:3/ko:3/CLAUDE.md:2/VERSION:1)，
`tasks.md` 5.7 与 `detailed-tasks.yaml` TASK-020 落地为可复跑的零命中 grep。

**核验（独立于 code-reviewer/qa-engineer 已跑的同款 grep，改用纯文本 sweep 检查口径残留）**：

```
$ grep -n '"9 处\|9处\|9 个落点' tasks.md detailed-tasks.yaml
(无输出)
```

`tasks.md`/`detailed-tasks.yaml` **两份文档内部**已无任何「9」作为落点总数出现（TASK-018
verification 里的「共 9 处」是 i18n ×3 文件 × 每份 3 处的**自洽子集乘积**，与 R1 那条错误的
「9 处落点」总数不是同一处遗留 —— 与 qa-engineer R2 判定一致，我独立复核同意）。**判定: closed**，
且口径统一是彻底的（两份文档零残留旧口径句子）。

### minor「SC-9 不得再次移出」只在 yaml notes，人读层无 — **closed**

`tasks.md:53-54`（1.5）现有：
```
- [ ] 1.5 SC-9 — 命中条目回显**未归一原始串** **(1)**
      > ⛔ **治理约束**: 本条 R1′ 曾被移出、R3′ 恢复。Q1 裁定「自己那一侧永不补」后, 回显对方原串成为 D2 fail-toward-reporting 的**唯一**缓解, 且它是输出里唯一携带 `org` 的通道。**不得再次移出。**
```
与 `TASK-005.notes` 逐字呼应。**判定: closed**。

### minor「组 3 可与组 2 并行」比实际 DAG 宽松 — **closed，且用新表述独立核验为准确**

`tasks.md:39` 原句已删除，改为：「组 3 依赖 2.2/2.3 (**3.1 与组 2 同文件, 必须串行**)。」
**独立核验（不采信 fix 自述，重新对照 21 条 dependencies）**：
- TASK-010 (3.1) `dependencies: [TASK-009]`（2.3）
- TASK-011 (3.2) `dependencies: [TASK-008]`（2.2）
- TASK-012 (3.3) `dependencies: [TASK-008]`（2.2）

三者恰好只依赖 2.2/2.3，不依赖 2.1，新表述「组 3 依赖 2.2/2.3」逐字精确，且额外点出
「3.1 与组 2 同文件, 必须串行」（TASK-010 本轮已改归 backend-architect 同文件域）。**判定: closed，
且比 R1 时的表述更精确**（R1 时旧句子完全不区分 3.1 与 3.2/3.3 的依赖粒度差异，新句子虽仍是段落式
散文、未显式点出「3.2/3.3 互相可并行」，但已不构成误导 —— 见下方 F4，我把这一点降级为效率信息缺失
而非正确性问题）。

**Part 1 小结：我 R1 的 3 条（1 major + 2 minor）全部 closed，且逐条独立复核（未采信 commit message
自陈），无一条只是表面重写。**

---

## 第二部分 — 新发现（本轮重点：文档治理 + 人读层完整性）

以下均为主控点名的 6 条已证实发现**之外**的问题。

```yaml
- type: issue
  severity: major
  category: documentation
  origin: pre-existing     # 内容早于 R1-fix 存在 (git diff 核实, 仅措辞被 R1-fix 精炼未删除)；
                            # R1 五席均未点名此形状在其他位置的复现，本轮首次发现
  scope: detailed-tasks.yaml TASK-007.notes / TASK-008.notes vs tasks.md 组 2 (2.1/2.2)
  summary: >
    collision.py 上两条实质性「治理边界」约束 —— (a) TASK-007「⛔ 只授权 D8 那三条重写, 其余一律
    不授权」(限定 normalize_linked_issue 的可改动范围); (b) TASK-008「同文件另有终态判据分歧
    (:210/:307/:155 三处 _TERMINAL 定义不一致), 本 Spec 只披露不改, 不要顺手统一」—— 完全没有
    进入 tasks.md 组 2 的人读层 (2.1/2.2 checkbox 均无对应文字)。而 collision.py 恰是本 Spec 被
    连续 4 个任务 (007→008→009→010) 编辑最密集的文件, 实施者在场时最容易"顺手"触碰这两条明确
    圈出的禁区。这与我自己 R1 已认定成立并被 fix 采纳的 minor (SC-9「不得再次移出」只活在 yaml
    notes) 是**同一形状**, 但 fix 只把该形状的**这一个实例**搬进了人读层, 没有对其他同形状实例
    做类推扫描 (memory `feedback_fix_the_class_not_the_instance`)。
  evidence: >
    `git diff a52ab81 3fc6f3f -- detailed-tasks.yaml` 显示两条约束在 R1-fix 前后均已存在（只是
    R1-fix 把措辞精炼为具体行号: TASK-008 从「collision.py:155 与 :307 两处 _TERMINAL = {done,
    abandoned}」精炼为「:210 tuple 含 unknown / :307 tuple / :155 内联 tuple, 3 种成员集」），
    两条 `本 Spec 只披露不改` / `⛔ 只授权 D8 那三条重写, 其余一律不授权` 字样在 fix 前后逐字保留。
    对照 `tasks.md:60-62`（2.1/2.2 checkbox 全文）: 「2.1 导出纯函数 ... §归一规则五步; None 与
    规则 4 的不可解析枚举一一对应 (D9)」「2.2 linked_issue_overlaps 内部比较谓词切换为归一键
    ... 签名与返回 schema 不变 (D6, 限本 Spec 变更面)」—— 均无「只授权 D8 三条重写」或
    「_TERMINAL 三处不一致不要动」的任何字样或指针。
  recommendation: >
    在 tasks.md 2.1/2.2 各补一行 ⛔ 提示（哪怕只是「⛔ 范围边界见 detailed-tasks.yaml TASK-007/
    TASK-008 notes」这样的指针句, 不必照抄全文）, 并顺带扫一遍全文档是否还有其他「只活在 yaml
    notes 里的强约束」（见下方 F2, 已额外发现一处同形状）。

- type: issue
  severity: major
  category: documentation
  origin: pre-existing     # git diff 确认 TASK-015 该 verification 条目未被 R1-fix 触碰
  scope: detailed-tasks.yaml TASK-015.verification[2] vs tasks.md 5.2
  summary: >
    TASK-015（aria 子模块 5 文件版本 bump）的 verification 含「CHANGELOG 须写明 basename 截断轴
    仍是已知限, 不得写成『已覆盖全部别名』」—— 这是防止 CHANGELOG.md（对外发布物, aria-plugin
    的 changelog SOT）在宣布本功能时**过度声称覆盖范围**的具体措辞禁令, 直接对应本 Spec 反复
    强调的 basename 截断已知限（D4, 本文件三处点名: TASK-007.notes D8 三条重写授权 / TASK-010
    verification「措辞不得暗示已穷尽核实」/ 母 Spec 接缝段落）。但该禁令**完全不在** `tasks.md`
    5.2 的 checkbox 文字里。
  evidence: >
    `detailed-tasks.yaml` TASK-015.verification: `["plugin.json 为 SOT, 其余 4 文件与其一致",
    "MINOR 而非 PATCH — 行为面扩大 (原本漏报的现在能报出来)", "CHANGELOG 须写明 basename 截断轴
    仍是已知限, 不得写成「已覆盖全部别名」"]`。`tasks.md:81` 对应的 5.2 checkbox 全文只有:
    「5.2 **aria 子模块** 5 文件 bump 到 **v1.66.0** — `.claude-plugin/plugin.json` (版本 SOT) /
    `.claude-plugin/marketplace.json` / `VERSION` / `CHANGELOG.md` / `README.md`」— 无措辞约束、
    无指针。`git diff a52ab81 3fc6f3f` 确认该 verification 第三条与 tasks.md 5.2 均未被本轮
    touch (逐字保留自 A.3 首版)。若实施者只读 tasks.md 写 CHANGELOG 条目, 最自然的宣传式写法
    （"新增 linked_issue 跨格式归一比较，覆盖 basename 别名"）恰好撞上被明令禁止的措辞。
  recommendation: >
    tasks.md 5.2 补一句「⛔ CHANGELOG 条目不得写成『已覆盖全部别名』(basename 截断仍是已知限)」，
    与 5.6 (CLAUDE.md) 现有的同类禁令句式对齐（5.6 已经这么做了, 5.2 该有的对应句缺失）。

- type: issue
  severity: minor
  category: documentation
  origin: new              # R1-fix 重写该章节时产生的残留张力, 是本轮首次出现的表述
  scope: tasks.md 末尾「与母 Spec 的接缝」章节, 拆分后的段落 (1)(2)
  summary: >
    R1 指出该章节「标题说已关闭而同章说悬空风险, 极性相反」, fix 拆成 (1)(2) 两段并加「两件事,
    不要混读」的显式警示, 标题级极性矛盾确已解决。但 (2) 段内部仍留一处更细的张力: 段落开篇断言
    「D4·X1·X3 **三条的关闭时点全押在母 Spec 上**」, 把三者一并归为"仍待母 Spec 关闭"; 紧接着
    同一段落又举证「**X1 半幅已是 Q1(c) 终局**」—— 即 X1 其实已经是本 Spec 一侧的最终状态、不
    随母 Spec 进展而变化。这与开篇「X1 的关闭时点押在母 Spec 上」直接冲突: 若 X1 已终局, 它就
    没有"待母 Spec 关闭的时点"。
  evidence: >
    `tasks.md:132`:「三处已知限的悬空风险: 仍然开着 (与 (1) 无关)。basename 截断轴 (D4) · 回显
    原串半幅 (X1) · `include_terminal` 归属 (X3) —— 三条的**关闭时点**全押在母 Spec 上」。
    `tasks.md:134` 同段: 「本 Spec 独立 ship 不使母 Spec 更难落地 (post_planning R1 / tech-lead
    已逐项核: ... **X1 半幅已是 Q1(c) 终局**)」。两句相隔仅一段, 前者把 X1 归入"待母 Spec 关闭"
    集合, 后者说 X1 已经终局 —— 读者需要自行判断"到底 X1 是三条里唯一已经关完的, 还是也在等
    母 Spec", 章节本身没有显式消歧。不影响 Phase B 执行 (无任务依赖此判定), 但会在未来
    Phase D 收尾或母 Spec 解封时造成"要不要重新核查 X1"的误判成本 —— 与本 Spec 反复强调的
    "『关闭』的表述必须精确到不会被下一读者误读"这一自我标准 (R1 对同章节的原始批评) 不完全对齐。
  recommendation: >
    在「三条的关闭时点全押在母 Spec 上」后加限定语, 如「(X1 除外 —— 其半幅本身已是 Q1(c) 终局,
    不随母 Spec 进展变化; 真正悬空的只有 D4/X3 两条)」, 把三选一的例外提前到开篇断言里, 不要
    让读者在举证句里才发现例外。

- type: observation
  severity: minor
  category: documentation
  origin: new
  scope: tasks.md:39 排序依据段 vs detailed-tasks.yaml:645「真并行组」注释
  summary: >
    detailed-tasks.yaml DAG 注释块底部明确列出「真并行组 (不同文件): {011, 012} · {018, 019}」，
    这是本文件里唯一显式点名"这两对任务真的可以同时做"的信息, 但 tasks.md 的排序依据段落
    （已在本轮改写以修复 R1 minor）只交代了跨组依赖与串行约束, 没有把这条"可并行"的正面信息
    带到人读层。不是正确性问题（不并行不会出错, 只是慢）, 记录为效率信息缺失, 不计入 major/minor
    阻塞项。
  evidence: >
    `detailed-tasks.yaml:645`「真并行组 (不同文件): {011, 012} · {018, 019}」只在依赖图注释区；
    `tasks.md:39` 排序依据段全文搜索不到「并行」二字用于组 3 内部或组 5 内部（唯一出现的「并行」
    在已删除的旧句「组3可与组2并行」, 现已被替换）。
  recommendation: >
    不阻塞, Phase B 实施者若想利用并行加速可自行查 yaml；若要补, 在 tasks.md 排序依据段末尾加
    一句「3.2/3.3 与 5.5/5.6 各自互相可并行 (不同文件)」。
```

---

## 第三部分 — 正面确认（本轮重点核验、未发现问题的项目）

```yaml
- type: decision
  severity: minor
  category: documentation
  scope: tasks.md「范围边界」表 vs detailed-tasks.yaml metadata.scope_boundary
  summary: >
    两处表述内容一致（未见互相矛盾）；委派声明经实读 phase-c-integrator SKILL.md §C.2.4
    (逐字确认 = "本 PR CI passing + main 无 in-flight CI") 与 phase-d-closer SKILL.md D.1-D.3
    (逐字确认涵盖进度更新/openspec-archive 归档/session handoff) 核实为其真实职责范围, 未发现
    「把某项真实义务说成别人的而对方其实不做」的情况。aria 子模块合并 (TASK-016) 正确留在
    「本文件」而非误委派给 phase-c-integrator —— 子模块合并走本地 git merge (CLAUDE.md 硬约束1,
    不经 Forgejo PR), 只有主仓自身变更走 Phase C PR 流程, 「组 5 与 Phase C 的时序」段落
    (`tasks.md:25`)「主仓自身的 PR 走 Phase C」这句把二者显式区分, 未混淆。
  evidence: >
    实读 aria/skills/phase-c-integrator/SKILL.md:171「green: 本 PR CI passing + main 无
    in-flight CI」；aria/skills/phase-d-closer/SKILL.md:40-43 D.1/D.2/D.3 三步表格逐字对应
    tasks.md「Phase D: cycle 进度更新 / Spec 归档 / 周期 handoff (Rule #9)」的三个分句。

- type: decision
  severity: minor
  category: documentation
  scope: detailed-tasks.yaml TASK-019.verification[2] 对 claude-md-hygiene.md §2.4 的引用
  summary: >
    逐字核对 standards/conventions/claude-md-hygiene.md 全文: 「15-20 行预算」与「覆写非追加」
    的数字定义严格来说落在 §2.3（「项目状态 = live 覆写, 非 log」）, §2.4（「写入时刻纪律」）
    第 1 点只是引用式复述「在 §2.3 预算内覆写状态段」。但 CLAUDE.md 自身「项目状态」段落脚注
    (`CLAUDE.md:129`) 就是把「覆写非追加」+「预算 15-20 行」+「设计术语不入内」三者合并引用为
    单一出处「`claude-md-hygiene.md §2.4`」——TASK-019 采用与 CLAUDE.md 本体完全一致的引用惯例，
    不构成误述, 只是这一惯例本身（把 §2.3 的数字借由 §2.4 point 1 的引用句一并归到"§2.4"）在
    convention 文档里是有依据的复合引用, 非 TASK-019 自创。判定：无需修改。
  evidence: >
    claude-md-hygiene.md:44「预算 ~15-20 行」在 §2.3；:52「在 §2.3 预算内**覆写**状态段」是
    §2.4 point 1。CLAUDE.md:129「本段覆写非追加, 预算 15-20 行 ... 规矩: `claude-md-hygiene.md
    §2.4`」与 TASK-019.verification[2]「「项目状态」段仍在 15-20 行预算内, 且为覆写非追加
    (claude-md-hygiene.md §2.4)」逐字同构。

- type: decision
  severity: minor
  category: documentation
  scope: metadata.file_domain_serialization / metadata.version_reference_surface vs tasks 数组
  summary: >
    两块 metadata 与 21 条 task 的 dependencies/deliverables 独立核对（不采信 fix 自陈）后完全
    自洽：file_domain_serialization 声明的两条串行链（007→008→009→010；001→002→003→004→005，
    006 挂 007 之后）与实际 dependencies 字段逐条相符；version_reference_surface 的
    breakdown（README.md 2/zh 3/ja 3/ko 3/CLAUDE.md 2/VERSION 1=14）与 TASK-017/018/019 的
    覆盖范围求和一致。scope_repos 的 aria head `af87cae` 经 `git submodule status aria` 实测
    确认未漂移（与 code-reviewer 已指出的主仓 head 陈旧是两个独立锚点, 阿里亚子模块侧锚点是准的）。
  evidence: >
    `git submodule status aria` → `af87caeeed88af6af76f29a8002badbe1228d927 aria
    (v1.21.3-243-gaf87cae)`，短 SHA 与 scope_repos[0].head 一致。
```

---

## Verdict

**verdict: FAIL**（0 Critical + 2 Major(pre-existing, 本轮首次发现) + 1 Minor(new) + 1 观察项;
另有主控点名的 6 条已证实发现未重复计入本报告，但纳入整体 verdict 判断）

**vote: REVISE**

判据: 我 R1 的 3 条全部 closed（含独立重跑复核，未采信 commit message 自陈）。本轮聚焦
文档治理/人读层完整性轴，发现 2 条 major：均是**同一形状的复发** —— R1-fix 已经证明知道
"关键约束不能只活在 yaml notes 里"这条规律（SC-9 的修法就是把约束搬进 tasks.md），却没有
把这条规律**类推应用**到其余同形状的实例（collision.py 的两条治理边界、CHANGELOG 措辞禁令）。
这是 `feedback_fix_the_class_not_the_instance` 的又一次实例，与本项目本次审计其余席位发现的
「同一形状第三次」（版本引用点口径）、「fix 自己的对偶」（sc-baseline 恒红）同属一个更大的
方法论教训：**修复要按"这个形状还有几个兄弟位置"来扫，不能只按"审计报告点了哪一个实例"来改**。

### fix 引入占比（本席位口径，与其他席位不同轴，需分别读）

| 口径 | 计算 | 结果 |
|---|---|---|
| 我本轮 2 条 major 中「R1-fix 引入」占比 | 0/2 | **0%**（两条均为 pre-existing，R1-fix 未触碰这些具体文字，只是精炼了周边措辞） |
| 我本轮 2 条 major 中「R1-fix 本该按已确立规律类推修复但未修」占比 | 2/2 | **100%** |

这与 code-reviewer 报告的「83% fix 引入」不是同一统计口径 —— 我这轮命中的不是「fix 改坏了什么」，
而是「fix 证明自己知道这个模式该怎么修（SC-9 先例），却没有把同一次扫描延伸到文档里其余同形状
的位置」。两个视角合起来看：**这份 tasks.md/yaml 的产出方式本身有系统性问题** —— 逐条对 R1
finding 打补丁，而不是每次先问"这个 finding 代表的规律还适用于哪里"。

### 给下一轮的建议

不建议本席位再加一轮做详尽扫描。建议 R3（若开）用**一次性的类结构性扫描**替代逐条修补：
对 `detailed-tasks.yaml` 全部 21 个 `notes` 字段做一遍"是否含有 tasks.md 对应 checkbox 缺失
的强约束（⛔ / 不得 / 只授权 / 必须 开头的祈使句）"的人工或脚本扫描，一次性把散落的治理边界
搬进人读层，而不是等下一轮审计逐条再发现一个。

---

## 轮次记录

- Round 1（knowledge-manager）: 1 major（9 vs 11 口径矛盾）+ 2 minor（SC-9 治理约束人读层缺失;
  排序表述比实际 DAG 宽松）+ 4 decision，verdict PASS_WITH_WARNINGS。
- Round 2（knowledge-manager，同席位保持口径可比）: R1 三条全部独立复核 closed；本轮聚焦
  文档治理 + 人读层完整性轴，发现 2 major（collision.py 治理边界与 CHANGELOG 措辞禁令均只活在
  yaml notes，均为 pre-existing 未被 fix 类推修复）+ 1 minor（母 Spec 接缝段落内部残留张力，
  X1 归类前后矛盾）+ 1 观察项（DAG 真并行组信息未进人读层）+ 4 decision（范围边界表委派属实 /
  TASK-019 引用 §2.4 与 CLAUDE.md 本体引用惯例一致 / metadata 两块与 tasks 数组独立核验自洽 /
  aria 子模块 head 锚点未漂移）。verdict FAIL, vote REVISE。

---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-08T08:37:47.000Z
context: openspec/changes/linked-issue-normalization/detailed-tasks.yaml
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R1 — knowledge-manager 席位审计报告

## 审计范围与方法

实读 `proposal.md` (275 行, 参照不重审)、`tasks.md` (94 行)、`detailed-tasks.yaml` (438 行);
交叉核验源码 `aria/skills/state-scanner/lib/claim_schema.py:95-124`、
`aria/skills/state-scanner/SKILL.md:165-184`、
`aria/skills/state-scanner/lib/collision.py:175-229`、
`standards/conventions/skill-benchmark-exemption.md` 全文;
另实跑 `ls README*.md VERSION`、`git ls-tree HEAD aria`、`grep .aria/state-checks.yaml`、
`grep -rn linked_issue *.md` 核验发版落点与文档同步面的穷尽性。

## 审计结论

### Finding 1 — TG-5 发版同步面「9 处落点」与自身分组枚举不符 (major)

`tasks.md:65` 与 `detailed-tasks.yaml` TASK-017.notes (两处逐字相同) 均声明
「**5.2–5.4 合计 9 处落点**」。但同一文件的分组枚举是:

- `tasks.md:61` / TASK-015: 「aria 子模块 **5 文件**」= plugin.json / marketplace.json / VERSION / CHANGELOG.md / README.md → **5**
- `tasks.md:62` / TASK-016: 「主仓同步面 **3 项**」= gitlink + 主仓 VERSION 的子模块版本表行 + root README.md 的 Plugin badge → **3**
- `tasks.md:63` / TASK-017: 「`README.{zh,ja,ko}.md` 的 `translated-from` 标记 **×3**」→ 标题本身用「×3」显式标注 3 个独立文件, TASK-017.deliverables 也逐字列出 `README.zh.md` / `README.ja.md` / `README.ko.md` 三个独立文件

5 + 3 + 3 = **11**, 与文中反复出现的「9」相差 2。实跑 `ls README*.md` 确认
`README.ja.md` / `README.ko.md` / `README.md` / `README.zh.md` 是四个独立文件 (主仓 README + 3 个 i18n
变体), 不是可以合并计数的同一落点; `git ls-tree HEAD aria` 确认 gitlink 是独立于 `VERSION`/`README.md`
的第三类落点 (submodule pointer, 非文件内容改动)。⇒ 「9」这个总数只有在把 `README.{zh,ja,ko}.md`
的三个标记**当成一个集合落点**计入时才能与「原写『5 文件 + gitlink』(=6) 漏 3 处」(6+3=9) 的叙事自洽,
但 TASK-017 自己的标题「×3」与 deliverables 又把它当 3 个独立落点处理 —— **两种计数口径在同一份文件
里并存且互相矛盾**。

**实际执行不会漏项** (5.2/5.3/5.4 三个 checkbox 逐条列全了全部 11 个真实落点, `git status` 核验时
应看到 11 处改动而非 9 处), 但「9」这个自述总数会在 D.1/D.2 收尾核验时与实际 diff 面不符, 造成
「怎么比声称的多 2 处、是不是多改了」的误判排查成本 —— 这正是本 Spec 自己在 §Impact 「≥45」下界行
点名过三次的同款失准模式 (「每次改 SC 表都必须重算」), 这次复现在了发版落点计数上。

**建议修复**: 把「9」改为「11」, 或明确 5.4 计数口径 (若坚持把 i18n 三标记记为「1 类落点」,
则应统一去掉 TASK-017 标题与 deliverables 里的「×3」/三文件枚举, 二选一, 不能两种口径并存)。

```
- type: issue
  severity: major
  category: documentation
  scope: tasks.md:65; detailed-tasks.yaml TASK-017.notes (:408 附近)
  summary: TG-5「5.2–5.4 合计 9 处落点」与同文件分组枚举 (5+3+3=11) 矛盾, 计数口径两套并存
  evidence: tasks.md:61-65 分组标题 5/3/×3 求和=11; ls README*.md 确认 zh/ja/ko/主 README 四个独立文件; git ls-tree 确认 gitlink 独立于文件改动
```

### Finding 2 — SC-9「不得再次移出」治理约束只活在 yaml notes, 人读层看不到 (minor)

`detailed-tasks.yaml` TASK-005.notes 写明: 「本条 R1' 曾被移出、R3' 恢复 …
**不得再次移出。**」—— 这是一条对 Phase B/未来审计轮次都重要的治理约束 (防止 SC-9 在后续修改中被
再次误删, 从而使 D2 极性论证的「人一眼可辨」缓解失效)。但 `tasks.md:39` 对应的 1.5 checkbox 只写
「SC-9 — 命中条目回显未归一原始串 (1)」, 完全没有携带「不得再次移出」这一句。若 Phase B 实施者或后续
维护者只读 tasks.md (人读层的设计初衷), 不会看到这条防复发提示。

```
- type: issue
  severity: minor
  category: documentation
  scope: tasks.md:39 (1.5) vs detailed-tasks.yaml TASK-005.notes
  summary: SC-9「不得再次移出」防复发约束只写在 yaml notes, tasks.md 人读层无对应文字
  evidence: tasks.md:39 仅「SC-9 — 命中条目回显未归一原始串 (1)」; detailed-tasks.yaml TASK-005.notes 含「不得再次移出」句, tasks.md 无对应
```

### Finding 3 — 「组 3 可与组 2 并行」的排序表述比实际 DAG 依赖宽松 (minor)

`tasks.md:26` 排序依据写「组 3 可与组 2 并行 (不同文件)」。但 `detailed-tasks.yaml` 的实际依赖是
TASK-010/011/012 (TG-3) 均 `dependencies: [TASK-008]`, 即 TG-3 必须等 TG-2 的 TASK-008 (归一谓词切换)
完成才能开工, 而非可与整个 TG-2 (含 TASK-007/009) 并行。TASK-009 (解析守卫) 与 TG-3 之间才是真并行
关系 (二者都只依赖 TASK-007, 互不依赖)。「组 3 可与组 2 并行」字面读容易让 Phase B 编排者在 TASK-008
落地前就着手改 docstring/字段文档 (此时归一谓词行为尚未定型, docstring 描述的「按归一后 `<repo>#<n>`
比较」还没有实现依据), 与 detailed-tasks.yaml 自己的 DAG 注释 (`co_dependency_note`: 「3.3 必须早于
4.1」但未点出「3.1-3.3 必须晚于 2.2」) 不完全对齐。

```
- type: issue
  severity: minor
  category: documentation
  scope: tasks.md:26 排序依据 vs detailed-tasks.yaml DAG (TASK-010/011/012.dependencies)
  summary: 「组3可与组2并行」的人读层表述比实际依赖宽松 — TG-3 实际只能与 TASK-009 并行, 需等 TASK-008 (非整组2) 完成
  evidence: detailed-tasks.yaml TASK-010/011/012 dependencies 均为 [TASK-008]; tasks.md:26 未点出这一子依赖粒度
```

### 正面确认 (decision)

以下几项是本次审计重点核验、且**未发现问题**的项目, 记录以证明「已核实」而非「未覆盖」:

```
- type: decision
  severity: minor
  category: documentation
  scope: TASK-010/TASK-011 vs TASK-012/TASK-013 (rule6_note 逐 hunk 承载)
  summary: Rule #6 两路判定 (collision.py docstring + claim_schema.py → substitute; SKILL.md:176 → 照跑AB不豁免) 被无歧义承载, TASK-012.verification 逐字写「不申请豁免、不走 substitute」
  evidence: 实读 proposal.md:167-176 判据表 vs tasks.md 组3/组4 vs detailed-tasks.yaml TASK-010/011/012/013 逐条比对, 三处判定路径一致, 未见可致 Phase B 误判「SKILL.md 那一 hunk 也能走 substitute」的措辞
```

```
- type: decision
  severity: minor
  category: documentation
  scope: TASK-011 vs claim_schema.py:107-114
  summary: claim_schema.py:107-114 两处失准的定位、原文、改法在 TASK-011 中可执行且与源码逐字一致
  evidence: 实读 claim_schema.py:107-114 确认原文含「SAME linked_issue」「Two active claims」字面词; TASK-011.verification 的两条改法 (SAME→same normalized key; active→_TERMINAL 不含 yielded) 精确对应
```

```
- type: decision
  severity: minor
  category: documentation
  scope: CLAUDE.md 卫生
  summary: tasks.md 与 detailed-tasks.yaml 全文未发现任何要求改动 CLAUDE.md 的任务落点, 符合项目 CLAUDE.md 卫生约定 (aria-plugin #116, Skill 设计内部术语不得抄进 CLAUDE.md)
  evidence: 通读 tasks.md 17 checkbox + detailed-tasks.yaml 17 TASK 条目, 无一涉及 CLAUDE.md 路径
```

```
- type: decision
  severity: minor
  category: implementation
  scope: detailed-tasks.yaml 复杂度/工时/agent 分摊footer (:432-433)
  summary: 派生值算术自查全部通过 — S×11/M×5/L×1 逐条点数确认; 73h = 11×3+5×6+1×10 计算无误; qa-engineer×8/knowledge-manager×5/backend-architect×4 逐条按 agent 字段点数确认; TG-1 子用例下界 13+5+15+8+1+3=45 与 metadata 声称一致
  evidence: 手工逐条枚举 TASK-001..017 的 complexity/agent 字段并求和, 与文末汇总行三项数字全部吻合
```

## Verdict

**verdict: PASS_WITH_WARNINGS** (0 Critical, 1 Major, 2 Minor)

## 轮次记录

- Round 1 (本轮, knowledge-manager 单席): 1 major (TG-5 落点计数自相矛盾, 9 vs 11) + 2 minor
  (SC-9 治理约束人读层缺失; 排序表述比实际 DAG 宽松) + 4 decision (Rule #6 两路判定无歧义 /
  claim_schema.py 定位可执行 / CLAUDE.md 卫生零违规 / footer 算术自查通过)。
- 本轮为单席位 (knowledge-manager) 独立审计, 未与其他席位交叉比对; major finding 建议在
  收敛判定时与其他席位 (如有覆盖 §Impact/发版面的席位) 交叉核实是否重复命中同一处。

## vote

**vote: REVISE** (存在 1 条 major, 不满足 PASS 的 0 critical 且 0 major 判据)

---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-08T08:37:47.000Z
context: openspec/changes/linked-issue-normalization/detailed-tasks.yaml
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R1 — tech-lead 席

**审计对象**: `openspec/changes/linked-issue-normalization/tasks.md` (A.2) + `detailed-tasks.yaml` (A.3)
**镜头**: 交付顺序 / 外部门 / 多远程与子模块协调 / 范围纪律双向 / Phase C-D 缺口 / agent 分配可执行性
**不重审**: 归一规则本体 (post_spec 三轮 × 五席已过拐点) · basename 截断轴 D4 · phase1_gate.py CLI · include_terminal
**已由其他四席确认的 8 条不在本报告内**。

**verdict: FAIL** (2 Critical + 5 Major + 2 Minor)
**vote: REVISE**

---

## 实读核验基线

先确认 A.3 metadata 自称「全部路径与行号已对该 HEAD 实测核验」的部分**成立**, 以便把发现限定在真实缺陷上:

| 引用 | 实读结果 |
|---|---|
| `collision.py:217` 裸 `!=` | ✅ `if c.linked_issue != own_linked_issue:` |
| `collision.py:210` `_TERMINAL` | ✅ `("done", "abandoned", "unknown")` |
| `collision.py:228` 回显 | ✅ `"linked_issue": c.linked_issue,` |
| `collision.py:182-206` docstring | ✅ `:182` 起 `"""Detect active claims…`, `:206` 收 `"""` |
| `claim_schema.py:107-114` | ✅ `linked_issue : Optional[str]` … `winner determination.` |
| `SKILL.md:176` | ✅ 含「同 issue 不同 track-id 的『同一件事两个名字』」 |
| 既有 6 条测试 `:206-247` 4 条 + `:527-575` 2 条 | ✅ `TestLinkedIssueOverlaps:206` (4 methods @224/232/236/245) + `TestPhase1GateLinkedIssueCli:527` (2 @533/563) |
| complexity 汇总 S×11 / M×5 / L×1 / 73h | ✅ 逐条重算一致 |
| TG-1 子用例加总 45 | ✅ 13+5+15+8+1+3 = 45, 与 proposal §Impact 推导一致 |
| 关键路径 001..004→007→008→012→013→014→015→016 | ✅ 按 est_hours 重算 = 37h, 为最长路径 |
| `aria` submodule HEAD | ✅ `af87cae` == gitlink `af87caee…` |

---

## Findings

### F1

```
- type: issue
  severity: critical
  category: architecture
  scope: detailed-tasks.yaml TG-5 (TASK-015/016/017) + tasks.md 组 5
  summary: TG-5 的验收前提「aria 子模块已合并」无任务归属; 两条多远程硬约束只落 notes 未入 verification ⇒ TASK-016 在「只本地合并、从未推 GitHub」的状态下即可判绿, 结构性复现 2026-07-14 orphaned gitlink 事故。
  evidence: |
    detailed-tasks.yaml:383 verification[0] = "主仓 gitlink 指向 aria 子模块**合并后**的 master SHA
    (非 feature 分支 SHA)" —— 该谓词消费一个**没有任何任务生产**的产物。
    全 17 个任务实读: 无 merge / push / ls-remote / PR 动作任务; tasks.md 组 1-5 止于「回归与发版」。
    :386-388 notes 写了两条硬约束 ("禁 Forgejo 服务端合并" / "推后逐个 ls-remote 核验, 不信 push 回执"),
    但 TASK-016 verification 只有两条: (a) gitlink 指向合并后 master SHA; (b) m6-version-badge-match → OK。
    两条都可由**纯本地 merge + 纯本地 bump** 满足 —— GitHub remote 上 aria master 仍在旧 SHA,
    主仓 gitlink 指向 GitHub 侧不存在的 commit ⇒ `clone --recursive` 断裂, 而任务判绿。
    这正是 CLAUDE.md 多远程硬约束段自陈的事故形状 (「服务端合并的 merge commit 只在 Forgejo 生成…
    主仓随后 bump gitlink 即产生 orphaned gitlink」) 与 memory feedback_mirror_sync_needs_mechanical_backstop
    (「只推 Forgejo 漏推 GitHub 已 3 次复发」) 的同一面。
  fix_direction: |
    (1) 新增 TASK-015b「aria 子模块本地 merge + 双推 + 逐 remote ls-remote 核验」置于 015→016 之间,
        verification 写成可执行断言: `git -C aria rev-parse master` == `git ls-remote origin master`
        == `git ls-remote github master` 三值全等 (ls-remote 失败须重试再下结论, 不得当作一致);
    (2) 把 notes 里的两条硬约束**上提为 TASK-016 的 verification 条目**。
        notes 不是验收判据 —— memory feedback_paper_fix_antipattern: doc-only advisory 是 paper fix。
```

### F2

```
- type: issue
  severity: major
  category: architecture
  scope: detailed-tasks.yaml metadata.scope_repo + TASK-016/017 deliverables
  summary: metadata 单仓声明 scope_repo=aria 与实际三处仓面矛盾, 且 TASK-016/017 的裸路径在 aria 子模块内同样命中真实文件 ⇒ 同一 YAML 内两套路径根, Phase B 可改错仓。
  evidence: |
    detailed-tasks.yaml:12-13 `scope_repo: "aria"` / `scope_repo_head: "af87cae"`, :5 注释
    「Scope repo: aria (aria-plugin) @ af87cae — 全部路径与行号已对该 HEAD 实测核验」。
    但实际落点横跨三处:
      (a) aria 子模块 — TG-1..TG-3 + TASK-015 (用 `aria/` 前缀, 主仓相对);
      (b) 主仓根 — TASK-016 `VERSION` / `README.md`, TASK-017 `README.{zh,ja,ko}.md` (裸路径);
      (c) 主仓内普通目录 — TASK-013 `aria-plugin-benchmarks/ab-results/`
          (实测 `git ls-tree HEAD aria-plugin-benchmarks` → `040000 tree`, **非子模块**)。
    歧义是真实的, 不是理论的 —— 实测 aria 子模块内同名文件存在:
      `aria/VERSION` ✅  `aria/README.md` ✅  `aria/README.zh.md` ✅ (`ls aria/`)
    且 `aria/VERSION` 与 `aria/README.md` **已被 TASK-015 用 `aria/` 前缀声明过**
    ⇒ 按 scope_repo=aria 解读裸路径的实施者会重复编辑 TASK-015 的产物 (看起来「已完成」),
    而主仓 `VERSION` 的子模块版本表行与 root README badge 从未被触及。
    (`aria/README.zh.md` 实测无版本串 —— grep `1.6[0-9]\.|Plugin Version|version-` 零命中 ⇒
     误改它是静默 no-op, 不会自暴露; `README.{ja,ko}.md` 在 aria 下不存在, 只有这两个会自暴露。)
  fix_direction: |
    metadata 改为 `scope_repos: [aria (submodule), Aria (main: VERSION/README*/aria-plugin-benchmarks)]`,
    并把 TASK-016/017 的 deliverables 全部加显式根前缀 (如 `<main>/VERSION`), 与 `aria/…` 区分。
```

### F3

```
- type: issue
  severity: major
  category: architecture
  scope: tasks.md 组 1-5 边界 + detailed-tasks.yaml 全文
  summary: Rule #8 pre-merge gate、Rule #9 handoff、Phase D 归档三者零落点且无「故意不列」声明; 而任务清单本身已跨进 Phase C/D 领地 (TG-5 发版 + TASK-016 post-merge gitlink) ⇒ 切分线无依据, 归档门与 PR 时序未定义。
  evidence: |
    detailed-tasks.yaml 全文 grep `pre.?merge|pre_merge|handoff|归档|archive|Phase C|Phase D|C\.2|D\.[123]`
    → 唯一命中是 :383 的「合并后」二字 (F1)。tasks.md 组 5 标题「回归与发版」, 文末止于 :93 的交付顺序风险注。
    两条不可协商规则无承接:
      Rule #8 — PR merge 前必跑 phase-c-integrator C.2.4 pre-merge gate (本 change 跨两仓两 PR, 门要跑两次);
      Rule #9 — session/周期 handoff 必写 docs/handoff/。
    切分线不自洽: TG-5 的三个任务 (发版 bump / gitlink / i18n 标记) 在十步循环里属 C-D 领地,
    TASK-016 更是**结构上只能在 merge 之后**完成 —— 既然清单已收纳 post-merge 工作, 把 merge 自身
    与 Rule #8 门排除在外就没有依据; 若是刻意委派给 phase-c-integrator / phase-d-closer, 须成文声明。
    时序耦合无人处理: 归档门 `lib/detailed_tasks.py::_is_spec_complete_by_yaml` 消费全部 17 个
    `status` 且 done-family 是 fail-CLOSED, 而 TASK-016 只能在合并后 done ⇒ 「PR 前哪些任务须 done /
    合并后哪些才能 done」未定义。对照证据: 同项目 `phase-c-integrator-ci-path-coverage/detailed-tasks.yaml:105-114`
    对同一个归档门耦合写了整段处置 (「status 被 state-scanner 归档门消费…否则 Phase D 归档必红」),
    ⇒ 这是本项目已知且已成文处理过的耦合, 本 Spec 未处理。
  fix_direction: |
    要么补 TG-6 (C.1 commit ×2 仓 / C.2 PR ×2 / C.2.4 gate ×2 / D.1 进度 / D.2 归档 / D.3 handoff),
    要么在 tasks.md 顶部显式声明「Phase C/D 由 phase-c-integrator + phase-d-closer 承担, 本清单止于 B.2」
    并同时给出 TASK-016 的 status 何时落 done-family 的规则。
```

### F4

```
- type: risk
  severity: major
  category: testing
  scope: .aria/repro/sc-baseline-linked-issue-normalization.py (substitute 唯一可复核载体)
  summary: 该 fail-closed 留证脚本在 TASK-008 落地后结构性转为恒红, Phase D 归档后再叠加第二条 FATAL 路径; 它是 Rule #6 substitute 的唯一可复核载体, 任务清单零处置落点。
  evidence: |
    脚本 :265-266 `measured_face = {sc for … if v == "红"}` (对**工作树**实跑生产 linked_issue_overlaps),
    :276-278 `if measured_face != EVIDENCE_FACE: … sys.exit(1)`。
    EVIDENCE_FACE 由 :206-216 从 proposal.md 现场解析 = 八条 ✅ 行 (SC-1/1b/3/4/5b/11/13/15)。
    ⇒ TASK-008 一落地, 那八条全部转绿, measured_face 变空集 ≠ 八条 ⇒ **exit 1, 永久**。
    第二条独立失效路径: :206-210 `_PROPOSAL = <repo>/openspec/changes/linked-issue-normalization/proposal.md`,
    :215-216 找不到即 `sys.exit("FATAL: 找不到 proposal.md")` ⇒ Phase D.2 归档把 spec 移到
    `openspec/archive/` 后脚本连解析都做不到。
    它的承重地位由三处成文: proposal.md:181「留证 artifact」/ :183 给出复现命令 / :219
    「该裁定要求的『全部实跑, 非声称』已满足」; tasks.md:79「唯一可当作证据的是 sc-baseline-*.py」;
    audit-trail:184「substitute 证据面的**唯一**可复核载体」。
    tasks.md / detailed-tasks.yaml 全文对它的处置**零落点**。
    后果: ship 后任何人按 proposal.md:183 复现都得 exit 1, 且**无法区分**「修复已落地」与
    「substitute 论证当初就是错的」—— 恒红与假绿同样零信息 (memory feedback_false_green_dual_is_permanent_red)。
  fix_direction: |
    加一个 TG-5 任务明确处置, 三选一并写进 verification:
    (a) 加 `--post-fix` 模式反转期望 (八条须**全绿**), 变成 ship 后仍有信息量的回归护栏;
    (b) 连同 proposal 快照一起冻结进 openspec/archive/, 并把 proposal.md:183 的复现命令改成
        「仅在 pre-fix 树上有效」;
    (c) 显式删除 + 在 archive 留 exit-0 输出快照。
    ⛔ 不可选「什么都不做」—— 那是把一个 committed fail-closed 闸门留成恒红。
```

### F5

```
- type: issue
  severity: major
  category: documentation
  scope: detailed-tasks.yaml TASK-008 notes (:218-220) + anchor 的范围纪律论证
  summary: TASK-008 notes 声称 collision.py 的 _TERMINAL 分歧「已开 aria-plugin #133」, 实读 #133 正文对 collision / unknown / 210 / 155 / 307 命中全为 0 ⇒「已开号 ⇒ 显式不并入」的范围纪律论证建立在不存在的覆盖上。
  evidence: |
    detailed-tasks.yaml:218-220 逐字: 「本文件内还有 collision.py:155 与 :307 两处 _TERMINAL =
    {done, abandoned}, 与本谓词用的 :210 {done, abandoned, unknown} **不同** — 属既有分歧
    (已开 aria-plugin #133), 本 Spec 只披露不改」。
    实读 #133 (forgejo GET /repos/10CG/aria-plugin/issues/133, state=open, body 2727 chars):
      title = "[缺陷][Layer L] _TERMINAL_STATUSES 4 处定义 2 种成员集 — release --status yielded 静默不释放"
      body.count('collision') = 0 · 'unknown' = 0 · '210' = 0 · '155' = 0 · '307' = 0
      body 的证据表只列 reconcile.py:62 / worktree_manager.py:615 / claim_lifecycle.py:317 / :408
      ⇒ 覆盖的是**具名常量 `_TERMINAL_STATUSES` 的 4 处定义 / 2 种成员集**, 分歧点只有 `yielded`。
    而 proposal.md:141-146 披露的是**≥7 站点 / 3 个取值**, 第三个取值 `{done,abandoned,unknown}`
    (含 `unknown`) 只存在于 collision.py:210 —— 正是本 Spec 唯一要改的那个文件里的那个谓词, 且
    `unknown` 的证据极性与 done/abandoned 相反 (母 Spec:165-167 逐字论证「零证据不得当正证据」)。
    ⇒ 本 Spec 披露的那一半在 #133 里没有承接; 本 Spec 归档后无号可查。
    形状 = memory feedback_cross_doc_claim_verify_at_target (文档 A 写「已在 B 记录 X」必去 B 实测)
    + feedback_issue_reporter_root_cause_may_miscite。
  fix_direction: |
    TASK-008 verification 加一条:「核验 #133 正文是否含 collision.py:210 的第三取值与 collision.py:155/:307;
    不含则补开 issue 或 PATCH #133 正文补全, 并把号写回 notes」。⛔ 不得留「已开号」这个未核验的断言。
```

### F6

```
- type: issue
  severity: major
  category: architecture
  scope: detailed-tasks.yaml agent 分配 (TASK-010 / TASK-016) + DAG 并行组注释 :428
  summary: agent 分配未按文件域切分 — knowledge-manager 拥有 lib/collision.py 的源文件编辑, 与 backend-architect 的 TG-2 同文件; 并行组注释逐字把它误述为「三个不同文件」。
  evidence: |
    :254 TASK-010 `agent: knowledge-manager`, :257 deliverables
    `aria/skills/state-scanner/lib/collision.py   # docstring :182-206`
    —— 与 :208/:229 的 TASK-008/009 (`agent: backend-architect`) 是**同一个文件**, 而该文件是 TG-2 的唯一文件
    (:179 注释逐字「单文件: lib/collision.py」)。
    :428 并行组注释逐字: 「{010,011,012} 可并行 (**三个不同文件**)」—— 010 的文件正是 TG-2 那一个。
    memory feedback_workflow_partition_by_file_domain 的判据是**按文件域**分 track
    (disjoint 文件集并行 / 同文件串行), 不按内容性质 (「docstring 属文档」) 分。
    附带: TASK-016 (:377 `agent: backend-architect`) 是一个纯发版 git-ops 任务, 承载两条多远程硬约束,
    而 roster (:19 `[qa-engineer, backend-architect, knowledge-manager]`) 里没有任何 agent 的职责面覆盖
    子模块/多远程操作 —— 该任务被塞给最近的 agent, 不是被分配给对的 agent。
  note_vs_other_seats: |
    「TASK-009/010 缺串行边」已由他席报告。**本条是分配轴, 修法不同**: 加一条 009→010 的边只是把
    冲突串行化, 文档 agent 依然拥有一个必须过 Python 全量套件 (TASK-014) 的源文件编辑。
    正确修法是把 TASK-010 并入 collision.py 那条 track 由 backend-architect 承担 (或反向, 把 TG-2
    的 docstring hunk 从 TASK-010 移进 TASK-008), 使 collision.py 恰好一个 owner。
  fix_direction: |
    (1) TASK-010 改 `agent: backend-architect` 或合并进 TASK-008;
    (2) 修正 :428 的「三个不同文件」错述;
    (3) TASK-016 的 git-ops 段落明确 owner (tech-lead 或 owner-action, 参 memory
        feedback_t15_owner_blocking_pattern 的 AI-runnable / owner-action 拆法)。
```

### F7

```
- type: issue
  severity: minor
  category: implementation
  scope: detailed-tasks.yaml TASK-016 deliverables (:379-381) + TASK-013 deliverables (:315)
  summary: TASK-016 的 deliverables 漏掉 gitlink —— 它是该任务标题与第一条验收的主体; TASK-013 的 AB 结果落主仓普通目录, 但仓归属叙述未把它算进主仓同步面。
  evidence: |
    :375 title「主仓同步面 3 项 — **gitlink** + VERSION 子模块版本表行 + root README badge」,
    :383 verification[0] 也以 gitlink 为主体, 而 :379-381 `deliverables: [VERSION, README.md]`
    —— **3 项里的第 1 项不在交付物清单**。gitlink 是 `git ls-tree HEAD aria` 的那一行 (实测
    `160000 commit af87caee… aria`), 它是收尾 `git status` 核验时最容易被 scoped add 漏掉的一项,
    而 tasks.md:65 / :410 正好引用 memory feedback_scoped_git_add_splits_claim_from_landing 提醒此事。
    :315 TASK-013 `deliverables: [aria-plugin-benchmarks/ab-results/]` —— 实测该路径是主仓内普通
    tree (`git ls-tree HEAD aria-plugin-benchmarks` → `040000 tree d6ca67c…`), 即 TG-4 就已产生
    主仓落点, 早于 TG-5; 而 :328 的「TG-5 — 回归 + 发版同步面 (9 处落点)」与 metadata.scope_repo
    都没把它计入。
  fix_direction: TASK-016 deliverables 补 `aria` (gitlink); TG-4/TG-5 的仓归属叙述统一收口。
```

### F8

```
- type: issue
  severity: minor
  category: documentation
  scope: tasks.md :85-93
  summary: 章节标题写「与母 Spec 的接缝 — 已关闭」, 但同章 :93 仍挂着未关闭的交付顺序风险 (三条已知限悬空), 标题的「已关闭」实际只覆盖 include_terminal 一项。
  evidence: |
    tasks.md:85 「## ✅ 与母 Spec 的接缝 — 已关闭 (owner 裁定 2026-08-08)」, :89 关闭的是
    include_terminal 形参归属那**一条**协调项。而 :93 在同一章节内: 「⚠️ 交付顺序风险
    (R1′/tech-lead-m2, 非阻塞): 三处已知限 (basename 截断轴 D4 · 回显原串半幅 X1 ·
    include_terminal 归属 X3) 的关闭时点全押在母 Spec 上, 而母 Spec 停在 Draft v2 且有两个未裁的
    阻塞项…若母 Spec 长期不解封则三条无限期悬空」。
    ⇒ 标题的 ✅ 与章内的 ⚠️ 极性相反, 且 :93 把 X3 (include_terminal) 也列进悬空三条 —— 与 :89
    宣布它已关闭直接对不上 (:89 关闭的是**归属裁定**, :93 说的是**已知限的闭合时点**, 两者不同,
    但同章节未消歧)。读者据标题会认为接缝全清。
  fix_direction: |
    标题改「与母 Spec 的接缝 — 协调项已关闭, 已知限闭合时点仍依赖母 Spec」;
    :93 把 X3 从悬空清单里区分标注 (归属已裁 vs 闭合未定)。
```

### F9

```
- type: issue
  severity: critical
  category: testing
  scope: detailed-tasks.yaml TASK-013 (TG-4, Rule #6 AB) + aria-plugin-benchmarks/ab-suite/
  summary: 现有 AB 套件在 A.3 阶段即可判定为**结构性看不见**被测 hunk; Rule #6 覆盖外分支所需三件套 (点名行为 / 可证伪定向 fixture / 套件缺口 issue) 零任务归属 ⇒ owner 亲裁且 Rule #10 保护的闸门可在对该 hunk 零判别力的情况下判绿。
  evidence: |
    被测 hunk = `SKILL.md:176` 的括注, 落在「claim 生命周期闭环」段, 描述的是
    `linked_issue_overlap[]` 按归一后 `<repo>#<n>` 比较这一语义。
    实读 AB 套件两条可能的输入面, **两条都零覆盖**:
      (a) `ab-suite/state-scanner.json` — 11 个 eval, 逐条列名:
          basic-state-collection / user-options-display / readme-sync-detection / config-awareness /
          submodule-sync-detection-new / upstream-behind-detection-new / issue-awareness-opt-in-new /
          readme-skill-count-badge-check / forgejo-config-detection / multi-remote-parity-drift /
          submodule-push-github-sync-miss —— 无一触及 claim / collision / linked_issue / overlap。
          `grep -ciE "linked.?issue|overlap|collision|claim|两个名字"` 命中 **1 行**, 实读为 :162
          的 "An answer that **claims** 1.35 fires is WRONG" —— 英文动词 claims, 与 claim 机制无关。
      (b) `state-scanner/evals/evals.json` (AB ops §场景 1 step 1 的另一个合法输入) — 8 个 eval:
          basic-state-collection / staged-changes-detection / openspec-status-check /
          architecture-status-check / quick-fix-recommendation / feature-development-recommendation /
          requirements-status-check / user-options-display —— 同样零覆盖。
          `grep -rlniE "linked.?issue|overlap|collision" state-scanner/` → **零文件命中**。
    ⇒「套件覆盖外」不是 Phase B 运行时才知道的条件, 而是**现在就已确定的事实**。而 :321-325 的
    notes 逐字写成条件式:「**若**本轮 AB 判定该 hunk 属套件覆盖外, 按 CLAUDE.md Rule #6 表第三行
    处理 (点名行为 + 建可证伪定向 fixture + 套件缺口开 issue; 缺一照跑)」—— 把可判定的事实推给
    运行时, 且推过去后**没有任何任务承接那三件事**。形状 = memory feedback_verify_predicate_inputs_exist
    (审计判定机制必分两层: 逻辑对吗 + **它要判的输入真会被生成吗**)。
    本项目对 Rule #6 AB 的既有惯例恰恰是「为 hunk 定制 eval + 双臂 SKILL.md 快照」, 不是跑固定套件:
      `ab-results/2026-07-20-v1.62.0-phase4-rule6/` = eval-06/10/11 三个定向 eval +
        anchors.json + assertions.json + grade.py + skill-snapshot-v1.61.0 + grading-summary.md;
      `ab-results/2026-07-31-v1.65.0-122-rule6/` = eval-1/2/3 + benchmark.json +
        skill-snapshot-v1.64.1-SKILL.md + skill-candidate-v1.65.0-SKILL.md + grading-summary.md。
    且定向 fixture 有现成先例目录 `ab-suite/phase-c-integrator-pre-merge-gate-fixtures/` (7 个 fixture)。
    更直接的先例: `ab-suite/state-scanner.json` 的 `changelog[v1.5.0]` (2026-07-20) 逐字写
    「Rule #6 补跑 AB (2026-07-20-v1.62.0-phase4-rule6) 暴露的测试集缺陷修复: A5 写反 … A3 字段
    真值冲突 …」⇒ **上一次同一个 skill 的 Rule #6 AB 直接产出了对 `ab-suite/state-scanner.json`
    的编辑并 bump 了它的 version**。而 TASK-013 的 deliverables (:315) 只有一行裸目录
    `aria-plugin-benchmarks/ab-results/   # 本轮结果目录 (日期 + 版本命名)`:
      无定向 eval / fixture · 无 `ab-suite/state-scanner.json` 的 version+changelog · 无双臂
      skill-snapshot/candidate · 无套件缺口 issue。
    ⇒ TASK-013 的三条 verification (:317-319: 经 /skill-creator 执行 / 落 ab-results 且在 5.x 前 /
      不得降级) **全部可满足**, 而产出的 delta 只是 11 或 8 条与本 hunk 无关的 eval 上的噪声。
      Q5 是 owner 亲裁、Rule #10 保护、tasks.md:54 标题写「⛔ 不申请豁免、不走 substitute」的闸门,
      却会以「跑了」判绿 ⇒ 假绿。
  note_vs_other_seats: |
    他席已报「TASK-013 验收只要求跑了+落盘+时点, 无结果判据」。**本条是不同层**: 即便补上 verdict
    判据 (WITH_BETTER / MIXED / EQUAL / WITHOUT_BETTER, AB_TEST_OPERATIONS.md §Verdict 标准),
    在零覆盖的套件上那个 verdict 仍然不是关于本 hunk 的 —— 先要有能看见 hunk 的 eval, 再谈判据。
    两条须同批修, 修任一条单独都不足。
  fix_direction: |
    把 TASK-013 拆三个任务并全部置于 TASK-015 之前:
      013a — 建可证伪定向 eval/fixture (点名行为: 「跨格式同 issue 的 claim 应互相认出、且回显对方
             未归一原串」), deliverables 显式列 `ab-suite/state-scanner.json` (含 version+changelog bump)
             与 fixture 路径; 明确 `ab-suite/version.yaml` 的 skills_covered/total_eval_cases 是否同批改
             (实测它现写 "每 Skill 选取 2 个核心 case / total 58", 而 state-scanner.json 已有 11 条,
              该文件本身已与现实脱节 —— 属既有漂移, 但 013a 需明确是否顺带处理, 不要留空);
      013b — 双臂 AB 跑, deliverables 按既有两次 Rule #6 run 的形态列全 (skill-snapshot / skill-candidate /
             per-eval / benchmark.json / grading-summary.md), verification 写 verdict 判据;
      013c — 套件缺口 issue (对齐 #117 / #127 的形态)。
    ⛔ 不得保留「若…则…」的条件式 notes —— 该条件在 A.3 阶段已可判定为真。
```

---

## 已核验但**未**构成发现 (留痕, 防下一轮重复投入)

```
- type: decision
  severity: minor
  category: architecture
  scope: 母 Spec a1-entry-claim-duplicate-work-guard 反向阻塞
  summary: 实读母 Spec 后确认本 Spec 独立 ship 不产生对母 Spec 的反向阻塞; 三处已知限是单向依赖 (本 Spec → 母 Spec), 方向正确。
  evidence: |
    母 proposal.md:9 逐字「**前置依赖**: linked-issue-normalization **必须先 ship**」
    ⇒ 依赖方向是母 Spec 依赖本 Spec, 本 Spec 先 ship 是母 Spec 自己要求的顺序, 不是抢跑。
    逐项核反向阻塞:
    (a) 签名面 — 母 :172 要求 linked_issue_overlaps 增 keyword-only `include_terminal: bool = False`,
        并建议由母 Spec 承担。本 Spec TASK-008 verification「函数签名与返回 schema 逐字不变」
        只约束**本 Spec 自身**, 且 proposal §非目标 ⭐ (owner 2026-08-08) 已成文「母 Spec 追加
        keyword-only 形参不视为违反、不构成回归」⇒ 不阻塞。
    (b) 导出契约 — 母 §2.1 (:113) track-id = `<归一后 basename>-<str(int(number))>-<container_uuid>`;
        TASK-007 交付 `normalize_linked_issue(v) -> tuple[str, int] | None` 恰好同时提供
        归一 basename 与可 `str(int(...))` 的 number ⇒ 母 Spec 两段所需分量齐备, 不需重实现。
    (c) 回显/自侧半幅 (X1) — Q1 裁定 (c) 两边都不补, 已是终局, 不是母 Spec 的待办 ⇒ 不阻塞。
    ⇒ 本轮未发现任何本 Spec 产物会让母 Spec 更难落地。母 Spec 的两个阻塞项 (C1 allowed-tools /
       C2 heartbeat 触发点) 与本 Spec 交付面无交集。
```

```
- type: decision
  severity: minor
  category: implementation
  scope: 范围纪律 (拉入方向)
  summary: 未发现把不属于本 Spec 的东西拉进任务清单; 三件机械工具、#133、#134 三处都被正确地标为披露/不并入。
  evidence: |
    metadata.known_env_trap `in_scope: false` (:49, aria-plugin #134 sys.path);
    TASK-008 notes「本 Spec 只披露不改, 不要顺手统一」(:220, #133 —— 覆盖度问题见 F5, 但**范围姿态正确**);
    tasks.md:69-81 三件工具明确「不修 / 不当闸门」+ :81「⛔ 同样不要在 Phase B 逐条修 R3′ 的 24 条残留」;
    TASK-007 notes:199「⛔ 只授权这三条重写, D8 的其余一律不授权」。
    另核: proposal 两条「行为不可观测」条款 (规则 1 对 left 的 strip / D7 的 4300 位上界) 明令
    **不为它们写 SC**, 而 TG-1 六个任务的 verification 逐条核对确实没有为它们建断言 ⇒ 未违。
```

---

## 另有核验通过、未构成发现的项 (留痕)

| 核验项 | 结论 |
|---|---|
| `aria/README.zh.md` 是否为漏掉的第 6 个 bump 落点 | ❌ 不是 —— 实测该文件对 `1.6[0-9]\.` / `Plugin Version` / `version-` 零命中, 无版本串; 且 `i18n-readme-translation-currency` 的 description 逐字限定 "每个 **root** i18n README", 不覆盖子模块内 |
| `aria/release-notes/` 是否有 per-version 文件惯例 | ❌ 不是 —— 目录内只有 `v1.2.0-brainstorm-skill.md` 一个历史文件, 非每版必产 |
| `m6-claude-md-version` check 是否被 v1.66.0 影响 | ❌ 不影响 —— 它断言 CLAUDE.md 顶层 `**版本**: 2.0.0` (主项目版本轴), 与 plugin 版本轴无关 |
| AB ops §场景 3 的 `summary.yaml` + `latest` symlink 是否为漏掉的落点 | ❌ 判为否 —— 那是全量回归 (28 skills) 的产物形态; 实测最近两次 Rule #6 单 skill run 都用 `benchmark.json` + `grading-summary.md`, 且 `ab-results/latest` symlink 自 2026-05-15 起未随后续三次 run 重指 ⇒ 非本类 run 的义务 |
| proposal:147「建议单开 issue」(reconcile.py vs claim_lifecycle.py `yielded` 语义正面冲突) 是否无落点 | ❌ 已有落点 —— 实读 #133 正文确含该冲突两侧注释的逐字引用 ⇒ 这一半被覆盖。**但另一半没有, 见 F5** |
| A.3 自称的行号/路径实测核验 | ✅ 逐条复核通过 (见开头基线表), 含 complexity 汇总 / 73h / 子用例 45 / 关键路径 37h 四个派生值重算 |

---

## 收敛建议

Critical 两条, 根因不同:
- **F1** 与 F3 是同一处结构缺口的两个切面 —— **「合并」这个动作在整份清单里没有 owner**, 而 TG-5 的验收谓词消费它的产物。应一次性修。
- **F9** 是独立的: Rule #6 闸门的**输入面**在 A.3 阶段就已确定为零覆盖, 而任务清单把它当条件式推给运行时。

F2/F7 同源 (仓归属表述)。F4/F5/F6/F8 各自独立。

**R2 前的最小修订集** (按承重排序):
1. **F9** — 拆 TASK-013 为 013a/013b/013c, 定向 eval/fixture 与 `ab-suite/state-scanner.json` 进 deliverables, 删掉「若…则…」条件式; 与他席的「补 verdict 判据」同批修 (单修任一条不足);
2. **F1** — 补 TASK-015b (aria 子模块本地 merge + 双推 + 逐 remote `ls-remote` 三值全等), 并把 TASK-016 notes 的两条多远程硬约束**上提为 verification**;
3. **F3** — Phase C/D 要么补 TG-6 (C.1/C.2/C.2.4 ×2 仓 + D.1/D.2/D.3), 要么成文声明委派, 并定义 TASK-016 的 `status` 何时落 done-family (归档门 fail-CLOSED);
4. **F2 + F7** — metadata 改多仓声明; TASK-016/017 deliverables 加显式根前缀; TASK-016 deliverables 补 gitlink (`aria`);
5. **F4** — 给 `.aria/repro/sc-baseline-*.py` 加 post-fix 处置任务 (三选一, 不可留恒红);
6. **F5** — TASK-008 verification 加「#133 覆盖度核验, 不含则补开/补正」;
7. **F6** — TASK-010 改归 backend-architect 或并入 TASK-008; 修 :428「三个不同文件」错述;
8. **F8** — tasks.md:85 标题消歧。

**vote: REVISE**

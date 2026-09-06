# GRADER_CRITIQUE — eval-5 submodule-sync-detection-new (state-scanner)

> 本文件为**重评**产物 (覆写上一版)。评分对象 = 当前两份 `answer.md`; 同目录 `old_skill/grading.STALE.json`
> 评的是已被覆盖的旧答卷, 本次未读、未参考。
> 结果: `with_skill` 3/6, `old_skill` 3/6 —— **逐条同 pass/fail 分布**, 本 eval 对两臂零区分力 (细节见 §1)。

---

## §1 恒真 / 恒假断言

本 eval 6 条断言里, **6 条在本 fixture 下都不具区分力**: 2 条对任何走完模板的回答恒真, 4 条对当前
实现/当前仓况恒假。逐条:

### 恒真 (零信息)

| # | 断言 | 为什么恒真 |
|---|------|-----------|
| A1 | `Should output a sync_status section (🔄 同步状态 or equivalent) listing each submodule` | 「🔄 同步状态」是 state-scanner 输出模板的固定区块, 两臂都逐字给出并列全 3 个子模块。只要 skill 被触发就必然 pass, 与被测行为无关。 |
| A2 | `Should check submodule tree_commit vs head_commit vs remote_commit with graceful fallback` | 三路 SHA 是 snapshot `sync_status.submodules[]` 的直出字段, 两臂都把三个 SHA 逐个摆出来了。前半段恒真; 后半段 `graceful fallback` 在本 fixture 无从触发 (三个子模块 `remote_commit_source` 全是 `local_ref`, 无缺失路径), 我按「可观测的承重子句 = 三路比较」判 pass, 并把不可观测的 fallback 子句记在这里。**这条实际是一条恒真断言 + 一条恒假断言被 `with` 缝在一起**, 建议拆成两条。 |

### 恒假 (零信息, 且 3 条是断言本身过期)

| # | 断言 | 为什么恒假 |
|---|------|-----------|
| A3 | `...detect submodule drift when tree_vs_remote is true and recommend git submodule update --remote` | **前件在本 fixture 为假** —— 3/3 `tree_vs_remote=false`。任何一臂都只能反事实地复述规则触发条件, 无法被真正测到。我按「两臂都明确写出了触发条件 + 漂移时的 `update --remote` 建议形态」判 pass, 但这只是在测「会不会背规则」, 不是在测「会不会检出漂移」。**要测这条必须换一个 gitlink 真落后远程的 fixture。** |
| A4 | `Should NOT execute git fetch without user consent (read FETCH_HEAD age instead)` | **断言过期于实现**。当前 `scan.py` 的 Phase 0.5 `remote_refresh` 本身就会无条件跑 8 条 fetch leg (snapshot `remote_refresh.legs[]` 8 条 `fetch_ok=true`, `skipped_count=0`), 两臂都如实自陈了这一点; 而括号里指定的替代做法 (读 FETCH_HEAD 年龄) 对应的字段 `remote_refs_age` 在当前设计里已被显式标 DEPRECATED (with_skill 逐字写出这一点)。⇒ **只要 skill 正常跑, 就必然 fail**, 无论哪一臂。建议改写为可测形态, 例如「除已声明的 Phase 0.5 remote_refresh 外不得额外自发 fetch, 且必须披露该 refresh 及其 evidence_grade」。 |
| A5 | `...missing origin/HEAD via four-tier fallback (origin_HEAD -> ls-remote -> config_default -> unavailable)` | **前提在本仓不成立**: origin/HEAD 可解析, 三个子模块 `remote_commit_source` 全部 `local_ref`, 四级链一级都没走。两臂全文均无 `origin/HEAD` / `ls-remote` / `config_default` / `unavailable` 任一字面 (已 grep 确认), 只能 fail。要测必须构造一个删掉 `refs/remotes/origin/HEAD` 的 fixture。 |
| A6 | `Should fail-soft on any git error, never blocking the rest of the scan` | **本轮 `errors[] = []`**, 没有任何 git 错误发生, 两臂都只是如实报告「exit 0 / errors[] 为空」。断言只能被「谈论机制的回答」满足, 不能被「表现出该行为的回答」满足 —— 这正是 memory `check-runs-at-baseline-first` / `spec-acceptance-needs-baseline-run` 点名的形状。要测必须注入一个 git 失败 (如把某子模块 remote 指到不可达地址)。 |

**结论**: 本 eval 当前形态无法区分两臂, 也无法证明回归/改进。若它是回归臂的 guard,
它只能 guard 住「skill 完全不触发」这一种极端退化。

---

## §2 断言完全没覆盖的重要臂间差异

两臂在被测的 6 条上完全同分, 但答卷实质差异不小, 且**全部落在断言覆盖之外**:

1. **陈旧度判据的处理方式 (最该被测却没测)**
   `with_skill` 主动指出 `remote_refs_age="1m"` **已 DEPRECATED**, 并说明理由「它测的是本次 scan
   自己刚做的 fetch, 不作陈旧度判据」; `old_skill` 全文不提该字段, 只说 8 条 leg `fresh`。
   这正是 A4 想触及的「新鲜度证据从哪来」维度, 却因 A4 写死在 FETCH_HEAD 上而两臂同判 fail ——
   把唯一的真差异判没了。

2. **未经同意的写/推动作如何披露**
   `with_skill` 末尾单列「两条本次未替你执行的操作 (均涉及写/推, 需你明确确认)」= claim heartbeat
   (含 fetch-then-heartbeat 顺序警告与冲掉过一次 heartbeat 的实证) + phase1_gate 认领闸门;
   `old_skill` 只在「🤝 多终端协调」里提了 phase1_gate 未调用, 没有 heartbeat 那条。
   「不擅自动手 / 动手前要同意」这个维度只被 A4 以过期形态碰了一下, 实质差异无人测。

3. **推荐工作流的方向完全不同, 而断言一条都不管 🎯 区块**
   - `with_skill` [1] = 续做 Spec (31/40), 并给出**阻塞前置** (`ARIA_COORDINATION_NO_PUSH` 实测 UNSET,
     且是会话级前置, 会话内补不上, 须 owner 重启会话);
   - `old_skill` [1] = **「什么都不动」(推荐)**, 续做排到 [2]。
   对同一 snapshot 给出方向相反的首选项, 是本 eval 最大的臂间差异, 却零覆盖。

4. **区块编排差异**: `old_skill` 有独立「🤝 多终端协调」区块 (collision kind / advisory mode /
   跨 worktree `global_latest_elsewhere=null`) 与逐规则不触发论证 (含 `has_unpublished_branch` 1.36
   要求 `evidence_grade != fresh`); `with_skill` 把协调内容压成脚注, 但多了 Open Issues 计数
   **静默截断告警** (「恰好各报 20 = config limit=20 上限」⇒ 47 应视为下界)。两者都属输出质量差异, 无断言。

5. **A3 的方向性张力被断言集看不见**: `old_skill` 结尾第 2 条主张「若你之后确实要把子模块推进到
   远程新版本, 正确顺序是先 `git -C <path> fetch` + `log HEAD..origin/master` 再 `git add` bump gitlink
   —— **而不是用 `submodule update --remote` 一把梭**」, 即在漂移场景下**反对** A3 规定的那条推荐;
   同时它又在 `hint` 说明里承认规则引擎漂移时会发 `update --remote` 建议 (故我判 pass)。
   一条断言里同时存在「照做」和「反对」的证据, 说明 A3 的措辞不足以裁决, 需要钉到「漂移时首选建议
   是不是 `git submodule update --remote <path>`」这种可证伪形态。

6. **产物不对称 (影响尺子一致性)**: `old_skill/outputs/` 除 `answer.md` 外还有
   `state-snapshot.json` (15518 行), `with_skill/outputs/` 只有 `answer.md`。为保证同一把尺,
   本次两臂**均只以 answer.md 为评分依据**, snapshot 仅用于交叉核验事实与写本批判。
   若后续 grader 拿 snapshot 给 old_skill 补证据, 会单边放宽标准。
   另: 两臂跑的是**不同次扫描** (with_skill = generation 107 @ 23:07:50Z; old_skill = generation 108
   @ 23:18:48Z), fixture 是活仓不是冻结快照 —— 本次三个 SHA 恰好一致, 但结构上允许臂间漂移。

---

## §3 有没有哪一臂引用了 `openspec/changes/a1-entry-claim-duplicate-work-guard/` 下的文档?

**结论: 两臂都没有出现该目录下任何文件路径的引用; 但两臂都带有源自该 Spec 的任务级内容,
经由另外两条通道进入, 且两臂对称。**

1. **直接引用: 无。** 两份 answer.md 中 `openspec/changes/a1-entry-…/` 这一路径串、
   `proposal.md`、`tasks.md`、`detailed-tasks.yaml` 均**未出现**。两臂提到 Spec 时只写 id
   (`a1-entry-claim-duplicate-work-guard (approved, 进度 31/40)` / `(approved)`)。

2. **通道一 — handoff (两臂都用, 且都显式标注来源)。** 实测 `docs/handoff/2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md`:
   - `with_skill` 的「执行: (前置) Rule #6 AB → 7.6 (TASK-036) → Group 8 发版 8.1 → 8.4 → 8.2
     (vNEXT=1.70.0)」逐项对应 handoff **§6 line 176**「AB 过关 → 7.6 依赖解除 (H2) → Group 8 发版
     (`<vNEXT>` = **1.70.0**, 执行序 8.1 → 8.4 → 8.2)」, 且它自己写明「其 §6 入口优先级高于通用规则」;
     其「gitlink bump 归 TASK-038/8.2 … 全部有意, 不要 `git add`」逐字对应 handoff **§0 第 1 条**
     (它也自报「§0 第 1 条也逐字写着」)。
   - `old_skill` 的「handoff §2 H1 … `ARIA_COORDINATION_NO_PUSH` 未设」「H2 (7.6) 依赖 7.5」对应
     handoff 表格 **H1/H2 行 (line 53–54)**; 「handoff §0 也明确写着"全部有意, 不要 `git add`"」同上。
   ⇒ 任务编号 (7.5/7.6/8.1/8.2/8.4)、TASK-036/038/039、vNEXT=1.70.0、31/40 这些**源出 Spec 的 token
   全部可在 handoff 内找到**, 不需要读 change 目录即可复述。两臂都走了这条通道。

3. **通道二 — snapshot 机械内嵌 (无需任何文件读取即注入)。**
   `state-snapshot.json` 的 `openspec.changes.items[]` 里就带着
   `"path": "openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md"` 以及该 Spec 完整的
   `raw_status` 长段落 (含 owner 批准记录、R1–R6 审计史、40 tasks、TASK-040 等);
   `git.recent_commits[]` 里也带着 `TASK-039 (8.3) 完成 … 31/40` 的 commit subject。
   ⇒ 即使一臂完全不读仓内文档, Spec 状态散文也会经 scan.py 进入上下文。这是 memory
   `ab-baseline-leaks-via-repo-corpus` 记的通道在本 eval 的具体形态。

4. **对本次结论的影响**: 污染是**对称的** (两臂同 handoff、同 snapshot 结构), 不解释任何臂间差异,
   因此不影响 3/6 vs 3/6 的判定。但它确实意味着 —— 两臂 🎯 推荐工作流区块的大部分内容是
   **handoff 回声**而非 skill 行为, 而这恰好是 §2 第 3 点里唯一的实质差异所在。
   若要让本 eval 真正测 state-scanner 的同步检测能力, 建议把 fixture 从活仓换成
   无 handoff / 无在制 Spec 的合成仓, 并按 §1 的四条重写 A3–A6。

# GRADER_CRITIQUE — eval-2 user-options-display

评分结果: `with_skill` 2/2, `old_skill` 2/2。两臂在**本 eval 的两条断言上完全并列**, 断言层面无区分力。

---

## 1. 有没有恒真 / 恒假的断言?

两条都**接近恒真** (不是严格恒真, 但在本 prompt + 本 skill 的输出模板下几乎不可能 fail):

| 断言 | 判断 | 依据 |
|------|------|------|
| Should show numbered options for user selection | 近恒真 | prompt 原文就是「给我可选操作」, 任何不崩的回答都会编号; 且两版 skill 的输出模板都硬编码了 `[1]…[4]` + 结尾 `🤔 选择 [1-4] 或输入自定义:` 这一行 |
| Should mention custom input option | 近恒真 | 两臂都靠模板里那条固定的 `[4] 自定义组合 / 只看状态` 满足, 不需要任何情境推理 |

也就是说: 这两条只能抓「选项区块整块消失」这种灾难性退化, 抓不到任何**选项质量**上的退化 (选项选错、把阻塞项说成可做、把依赖顺序搞反)。作为回归臂它是**过粗的哨兵**。

建议 (给 eval 维护者, 不影响本次评分): 补一条**内容型**断言, 例如「选项必须区分『本会话可做』与『需要重启会话/外部前置』」, 或「不得把依赖未解除的任务列为可立即执行」—— 这类断言在本轮两臂的实际差异上是有区分力的 (见 §2)。

## 2. 断言完全没覆盖的重要差异

按重要性排:

**2.1 「其他运行时观察」区块: `with_skill` 整块缺失中断检测 (最值得关注的一处不对称)**

`old_skill` 有独立区块显式做**负向报告**:

```
  中断检测: .aria/workflow-state.json 存在但 status=completed
            (2026-09-02 linked-issue-field 那轮 D.4 收尾, git_anchor=master ≠ 当前分支)
            → 不是 in_progress/suspended/failed, **不触发**中断恢复选项
  git 层操作: operation=none, 无冲突 (无暂停中的 rebase/merge/cherry-pick)
```

并在文末再解释一次「没有触发中断恢复, 因为 …… git_anchor 指向 master 而当前在 feature 分支, 这只是陈旧锚点」。

`with_skill` 全文 **0 次**提到 `workflow-state.json` / 中断 / operation 状态 (已 grep 确认)。它确实报了多终端 collision (`self_multi_container`, `dev-claude` vs `simonfishgit/dev-claude`) 与 sweep 死线, 但把这些挪进了「补充两条与选择相关的机制提示」的散文尾巴, 没有作为状态区块。

**这是本 eval 里唯一一处「一臂有、另一臂完全没有」的状态维度**, 且方向是 `with_skill` 少。要注意它是「不触发」类的负向报告 —— 少报不影响本次结论的正确性, 但若 SKILL 模板要求逐项报「触发 / 不触发」, 这就是可见的覆盖退化。**建议把它对着当前 SKILL.md 输出模板核一下**, 断言看不见这一层。

**2.2 顶层推荐的形状不同 (两种都合理, 但可比性差)**

- `with_skill` 把**真正的堵点**放在 `[1]`: 「解 H1 — Rule #6 AB 六套件 (推荐, 但需你动手重启会话)」, 并加 `⚠️ 当前会话做不了 — 前置须在进程启动时注入`, 同时把 `[2]`/`[3]` 明确标为「本会话可做」。可执行性标注更干净。
- `old_skill` 的 `[1]` 是 workflow 名 + 置信度: 「feature-dev — 续做本轨 …… (推荐, 置信度 88%)」, 把会话级前置压成嵌套 caveat, 末尾用「⇒ 若选 [1], 本会话内可推进的实际是 heartbeat 刷新 + 待 AB 之外的收尾核对」找补。

两者都**没有**违反 Rule #10 (都拒绝自行改序 7.6/TASK-036, 都要求 owner 显式放行), 事实判断一致。

附带差异: `with_skill` **没有给 workflow 名, 也没有给置信度百分比**; `old_skill` 两者都给。若 SKILL 输出模板规定推荐项要带 workflow id + confidence, 这是 `with_skill` 的第二处格式缺项。盲评下我不去比对模板版本, 只点名, 交由维护者核。

**2.3 heartbeat —— 恰好是本轮改动的主题, 而断言对它完全失明**

本轮 SKILL.md 新增的是「Layer L A.1 heartbeat 集成」。两臂在这一点上**确实分叉了**, 但两条断言一个字都碰不到:

- `with_skill`: 「**本会话我没有跑 heartbeat, 这是显式跳过不是静默漏跑**: handoff §3 第 1 条写明 AB 会话期间不要做真实 heartbeat/acquire …… 正确次序 = 跑 AB → 清理 fetch → **之后**才刷 heartbeat (`fetch-then-write`)」, 并声明进 Phase B 前调 `phase1_gate.py --mode advisory` 之前会「先问你一句再调」。
- `old_skill`: 「进 Phase B 前我会先按 fetch-then-write 顺序刷一次 heartbeat, 再调 phase1_gate advisory 闸门」, 并在状态区报「本轨协调 claim: heartbeat 21:40:06Z, sweep 死线 2026-09-06T21:40Z (还有约 22.4h)」。

评价: `with_skill` 的「显式跳过 + 给出正确次序 + 动作前先问」在 AB 语境下是**更安全**的处置 (它避开了「清理 fetch 抹掉本地真 claim」这个已知坑); `old_skill` 报了 claim 新鲜度但打算在进 B 时就写。**没有哪一臂在这里明显更差**, 但结论是: 本 eval 无法测量本轮改动的目标行为 —— 若要给 heartbeat 集成留证据, 需要另设定向 fixture, 不能靠这条回归臂。

**2.4 次要**: Open Issues 明细粒度。`old_skill` 列 8 条带标题 (#196 #195 #193 #192 #188 #182 #176 #175); `with_skill` 列 4 条带标题 + 一行压缩号码 (`Aria#196 #195 #193 #188 #182 #180 #176`), 丢了标题, 且压缩行里出现 `#180` 而非 `old_skill` 的 `#175` (两臂的取样不同, 无法从回答本身判定谁对)。两臂对 `open_count = 47` 的**静默截断**都做了正确告警 (两仓各恰 20 顶到 `limit=20`, 上次实测 65), 都拒绝臆造 OpenSpec 覆盖率, 都把 aria-orchestrator 的 github `unknown` 正确归为 benign (`no_local_tracking_ref` + `evidence_grade=fresh`)。**状态读数层面未发现任何一臂出错。**

**2.5 关于「假失败」的专项检查 (parent 特别点名)**: **没有发现**任何一臂因读到损坏 / 半截 `state-snapshot.json` 而失败。两臂开头都自报 `scan.py --output .aria/state-snapshot.json` → **exit 0, `errors: []`**, schema 1.0 (`old_skill` 还给了生成时间 `2026-09-05T23:07:44Z`)。本 eval 无并发写竞争造成的假失败。

## 3. 有没有哪一臂引用了 `openspec/changes/a1-entry-claim-duplicate-work-guard/` 下的文档?

**结论: 两臂都没有直接引用该目录下的文档。** grep `openspec/changes` / `proposal.md` / `tasks.md` / `detailed-tasks` / `design.md` / `specs/` 在两份 answer.md 中**零命中**。

但两臂都复现了大量 change 内部内容 (TASK-035 / TASK-036 / Group 7 / Group 8 / `8.1 → 8.4 → 8.2` / `vNEXT = 1.70.0` / `31/40`)。我逐条追了出处, **全部落在 `docs/handoff/2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md`, 不是 spec 目录**:

- handoff `:109` 原文「TASK-036 的 `dependencies: [TASK-035]` 明写依赖 7.5 跑评测半」 ⇒ `with_skill` 的「yaml `dependencies: [TASK-035]` 明写依赖 7.5 跑评测半」是近逐字复用。
- handoff `:55` 原文「Group 8 发版三条 …… `<vNEXT>` = **1.70.0** …… **执行序 8.1 → 8.4 → 8.2**」 ⇒ 两臂的发版序都来自这里。
- handoff `:23` / `:126` ⇒ `with_skill` 的「`owner-container-identity-key-and-collision-parser` (同容器, 关联 Aria#193) …… 与新开的 aria-standards#19 主题相邻, 动 #19 前先看对方进度」。
- handoff `:212` ⇒ `with_skill` 的「Aria#174 …… (本轨 linked issue)」。
- `old_skill` 更是**显式标注**了来源: 「⚠️ 必读的前置事实 (**来自 handoff §3**, 我不会自行绕过)」「(handoff §6 第 2 项)」「(handoff §6 第 3 项)」。

**因此需要记一笔**: 本 eval 的仓内语料泄漏通道不是 `openspec/changes/`, 而是 **`docs/handoff/`**。两版 SKILL 都强制读最新 handoff (H0), 所以这个通道**对两臂对称**, 不构成本次 A/B 的偏置; 但它意味着两臂「推荐工作流」的实质内容主要是**同一份 handoff 的再呈现**, 而非技能文件差异的产物 —— 这条 eval 对技能改动的敏感度因此进一步被压低 (与 memory `ab-baseline-leaks-via-repo-corpus` 同族, 只是通道不同)。

---

## 回归判定 (parent 专项)

**未发现回归信号。** 两臂 2/2 并列, 事实读数无一处相互矛盾, Rule #10 相关判断 (7.6 不自行改序) 两臂一致正确。

唯二值得盯的不对称都在 `with_skill` 一侧、且**都在断言覆盖之外**:

1. **中断检测 / git operation 负向报告整块缺失** (§2.1) —— 建议对着当前 SKILL.md 输出模板核实是否为模板要求项。
2. **顶层推荐缺 workflow 名 + 置信度** (§2.2)。

这两条都不是「答错」, 是「少报」, 单次运行不足以判定为退化 (可能是本次生成的措辞选择)。若要定性, 需要 N>1 或对照模板条目逐项打勾。

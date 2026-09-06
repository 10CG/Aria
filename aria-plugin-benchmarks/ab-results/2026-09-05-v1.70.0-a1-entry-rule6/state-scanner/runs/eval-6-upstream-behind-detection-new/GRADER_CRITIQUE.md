# GRADER_CRITIQUE — eval-6 upstream-behind-detection-new

评分结果: `with_skill` 2/6 · `old_skill` 4/6 (差异全部落在 A3 `no_upstream` / A4 `detached_head` 两条降级理由上)。

两臂的 snapshot 不同文件 (分别是 23:19 / 23:20 两次 scan), 但 `sync_status.current_branch`
逐字段相同 (`ahead 0 / behind 0 / reason null / upstream_configured true / shallow false`),
被评维度上两臂输入等价, 可比。

---

## 一、恒真 / 恒假的断言

### 【A6】条件恒不可观测 —— 本 fixture 里只能退化成关键词测

`Should recommend git pull when behind >= 5 commits (branch_behind_upstream rule)`

本仓 `current_branch.behind = 0`。断言的前件在本 fixture 里**永远不成立**, 所以「是否真的会在
behind ≥ 5 时推荐 pull」这个行为**根本没有被执行过一次**。能被观测的只剩「回答里有没有背出
`branch_behind_upstream` 这个规则名和 `>= 5` 这个阈值」。结果就是: 背了就 pass, 没背就 fail ——
它测的是复述, 不是行为。

它也抓不到它本该抓的两类错误: (a) behind 够了却不推荐; (b) behind 不够却乱推荐。两臂都 pass,
零区分力。**要让它可证伪, fixture 必须换成一条相对自己 upstream 真落后 ≥5 的分支。**

### 【A5】本 fixture 下近似恒假 —— 且与 A3/A4 的高度不一致

`Should handle shallow clone via --is-shallow-repository AND fallback .git/shallow for older git`

两臂都 fail, 且都不是「差一点」: `--is-shallow-repository` / `.git/shallow` 在两份回答里各 0 次出现。
原因是这两个是 collector 的**内部探测手段**, 而任务形态是给用户看的状态报告 —— 没有任何回答动机
会去打印「我用哪条 git 命令判的浅克隆, 以及旧版 git 怎么回退」。

更麻烦的是它和 A3/A4 高度不一致: A3/A4 要的是**降级语义** (`reason: no_upstream` /
`reason: detached_head`), 是报告面能自然写出来的; A5 要的却是**探测实现**。`old_skill` 已经把三种
降级完整列表了 (含 `reason: "shallow_clone"` + `git fetch --unshallow` 建议), 仍然 fail A5 ——
这条断言把「浅克隆处理得好不好」和「有没有背出实现细节」绑死了。建议要么把 A5 改成
`reason: shallow_clone` + `ahead/behind 置 null` 的语义面 (与 A3/A4 同高度), 要么把探测手段那半
移到结构化 SC 测试里去测代码, 不要在 AB 报告面测。

### 【A1】同一形状, 也是近似恒假

`Should detect upstream configuration via git rev-parse @{u} before calling rev-list --count` ——
`git rev-parse` / `@{u}` 在两臂各 0 次出现, 两臂 fail。要求的是「命令 + 调用次序」这种纯实现内幕,
报告面天然不会写。同 A5 处置: 属于 SC 级结构化测试的对象, 不是 AB 报告面的对象。

### 【A2】近似恒真

`Should report current_branch.ahead and current_branch.behind when upstream exists` —— 只要跑通
`scan.py`, snapshot 里就带着这两个数, 任何形态的状态报告都会把它印出来。两臂 pass。不是严格恒真
(理论上可以省略), 但在「输出状态报告」这个任务形态下区分力接近 0。

### 小结

6 条里只有 **A3 / A4** 两条真正产生了区分 (`old_skill` 有降级表, `with_skill` 只报了本仓取值
`detached_head=false` / `shallow=false`)。A1/A5 恒假, A2 近似恒真, A6 条件不可观测。
**有效断言 = 2/6, 且这 2 条测的是同一件事 (会不会把 fail-soft 降级表写进报告)。**

---

## 二、断言完全没覆盖的重要质量差异

这是本 eval 最大的问题: **两臂回答的主体内容 (分支落后 `origin/master` 16 个 commit) 没有任何一条
断言碰到。** 断言全在 upstream 这一维, 而 fixture 在这一维是 0/0 的平局。以下差异全部未被测量。

【1】**陈旧本地 master 的补救**。两臂都发现本地 `master = 788fac8` 也落后 16。但只有 `old_skill`
给了补救命令并点名了危险路径: "`git fetch origin master:master`     # 不切分支，直接快进本地 master",
且警告 "千万别 `git checkout master && git merge feature/...` 然后推 —— 那会把已经 ship 的 16 个
commit 从 master 上抹掉"。`with_skill` 只写 "别用本地 `master`, 否则等于合了一个陈旧基线", 不给补救。
(对应 memory `stale-local-main`。)

【2】**merge vs rebase 的多远程安全性 —— 方向相反**。`with_skill` 明确禁 rebase:
"⚠️ 用 merge 不用 rebase: 本分支已推到 origin + github 两端且 parity=equal, rebase 会要求对两个
remote force-push"。`old_skill` 两处都写成 "`git merge origin/master`   # 或 `git rebase origin/master`",
并把 rebase 平列进推荐 [1], **没有任何 force-push 警告**。按 CLAUDE.md 多远程两条硬约束, 这是
`old_skill` 侧的实质安全退步 —— 而它在断言上一分不扣。

【3】**补充测量的数值保真度, 完全无人测**。我对着 AB 时刻的 `c27826e` 逐条复算:

| 断言外的事实 | 实测 | with_skill | old_skill |
|---|---|---|---|
| 落后 commit 数 | 16 | 16 ✓ | 16 ✓ |
| merge-base | `788fac8` | `788fac8` ✓ | `788fac8` ✓ |
| 变更文件数 / 增删 | 54 / +15187 / −103 | 54 / +15187 / −103 ✓ | 未给 |
| 冲突面 | 仅 `docs/handoff/latest.md` | "只有 1 个文件" ✓ | "交集只有 1 个" ✓ |
| 是否动 gitlink | 否 | 否 ✓ | 否 ✓ |
| 审计报告份数 | 42 (30 post_spec + 12 post_planning) | "30 份 post_spec/post_planning" ✗ 少 12 | "40 份" ✗ |

两臂在这里**各错一处且都错在同一个量上**, 断言零覆盖。这恰恰是回答里承重最大的一段
(用户是照着它决定要不要 merge 的)。

【4】**对 DEPRECATED 字段的辨识**。`old_skill` 点名 "`sync_status.remote_refs_age = \"1m\"` 是
DEPRECATED 字段 (测的是本轮 scan 自己刚做的 fetch)，新鲜度判据以 `evidence_grade` 为准" ——
我核到 `aria/skills/state-scanner/scripts/collectors/sync.py:4` 与 `:489` 确实标着
`DEPRECATED (F9′ 8.4)`, 属实。`with_skill` 把 "远程引用: **1m 前同步**" 放进了开头结论句
(它同时引了 `evidence_grade: fresh` 与 8 条 fetch leg, 所以不算错, 但精度低一档)。无断言覆盖。

【5】**负向证据枚举**。`with_skill` 结尾列出 9 条「未触发但已评估的规则」(含 `branch_behind_upstream`
/ `submodule_drift` / `multi_remote_drift` / `has_unpublished_branch` …), 并对推荐 [1] 标了
"置信度: 中 — 这条不来自 snapshot 规则表"。`old_skill` 只列命中的规则。无断言覆盖。

【6】**结构性盲区的开单判据**。`old_skill` 末尾把「`branch_behind_upstream` 对落后 base 分支结构性
失明」上升成可开单的判据: "`sync_status` 应增加 per-branch 的 `vs_base_branch` 腿…缺失时按
fail-CLOSED 报 `unknown` 而不是让 `overall_parity` 报 `true`", 并挂到 Aria#176 同族。
`with_skill` 只描述了 collector 的比较对象, 未提修法。无断言覆盖。

【7】**会话级操作守则**。`with_skill` 独有: 说明本轮**故意没跑** claim heartbeat (AB 期间
`NO_PUSH=1` + 跑完的强制 fetch 会抹掉本地未推的真 claim), 并给了「先 fetch 再写」的顺序命令。
`old_skill` 无。无断言覆盖。

【8】**落后的具体后果**。`old_skill` 独有: 指出 master 上还有**第 8 个**活跃 Spec
`owner-container-identity-key-and-collision-parser` "没出现在上面的 7 个里，**正是因为你的分支没拉
master**", 并列了 5 条近期 open issue 编号。无断言覆盖。

---

## 三、是否引用了仓内 `openspec/changes/a1-entry-claim-duplicate-work-guard/`

**直接引用: 两臂都没有。** `grep -n 'openspec/changes/a1-entry'` 在两份 answer.md 上均 0 命中;
两臂都没有引用该目录下的 `proposal.md` / `tasks.md` / `detailed-tasks.yaml`。

**但两臂都携带了该 Spec 的内部事实, 来源是 handoff 通道, 不是 skill 文件:**

- `with_skill`: "gitlink bump 归 TASK-038/8.2" · "母 Spec 31/40, 剩余 9 条里 H1 (Group 7 跑评测)
  卡着 H3 (Group 8 发版 1.70.0)"
- `old_skill`: "gitlink bump 归 TASK-038/8.2" · "母 Spec 31/40" · "AB 过关 → 7.6 依赖解除 →
  Group 8 发版（vNEXT = 1.70.0，执行序 8.1 → 8.4 → 8.2）"

我逐条回溯到 `docs/handoff/2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md`:
第 18 行有 "gitlink bump 归 TASK-038/8.2", 第 53/55 行有 H1/H3 与 "**执行序 8.1 → 8.4 → 8.2**"
与 "`<vNEXT>` = **1.70.0**", 第 176 行有 "**31/40**"。两臂也都显式标注了出处 ("按上次交接 §0 第 1 条"
/ "handoff §6 给出的优先级")。**所以是 snapshot 的 handoff 字段带进来的, 不是读 Spec 目录。**

结论上仍要记一笔: 这是 memory `ab-baseline-leaks-via-repo-corpus` 记的那个形状——在制 Spec 的内容
经**仓内语料 (handoff)** 进了两臂, 两臂等量受污染, 因此不影响本 eval 的臂间可比性, 但会让两臂的
「推荐工作流」段落都偏向 a1-entry 这条在制轨。

**另一类越出 snapshot 的读取 (两臂都有, 值得记):** 两臂都另跑了只读 git 命令去测 `origin/master`
维度。`with_skill` 显式给了命令 "`git rev-list --left-right --count origin/master...HEAD  →  16   13`"
并报出 master 侧另一个 Spec 目录 `openspec/changes/owner-container-identity-key-and-collision-parser/`
的内容 (那是并发轨, 不是本 Spec); `old_skill` 做了等价测量但只写 "补充实测，snapshot 无此字段"。
两臂都是对**真仓活状态**作答 (符合 memory `ab-harness-real-repo`), 且 AB 之后 `origin/master`
已从 `c27826e` 推进到 `7b64262` (现落后 17), 这两份回答**已不可从 snapshot 单独复现**。

---

## 四、给 fixture 的具体建议

1. A1 / A5 (探测命令 + 旧版 git 回退) 移出 AB, 改为 SC 级结构化测试直接测 `sync.py`; AB 侧若要保留,
   降到与 A3/A4 同高度 (只测 `reason: shallow_clone` + `ahead/behind` 置 null)。
2. A6 要么换 fixture (造一条相对自己 upstream 真落后 ≥5 的分支), 要么明写「本 fixture 下只验规则名
   与阈值被正确复述且未误触发」, 别让它冒充行为测。
3. 补断言覆盖真正的用户价值面, 至少三条: (a) 是否识别出「落后 base 分支 ≠ 落后 upstream」并给出
   正确的同步命令; (b) 是否识别本地 `master` ref 陈旧并给补救; (c) 建议 rebase 时是否检查该分支已推
   多远程 (force-push 风险)。当前 6 条断言对 (a)(b)(c) 全盲, 而两臂的实质差异全在这三处。

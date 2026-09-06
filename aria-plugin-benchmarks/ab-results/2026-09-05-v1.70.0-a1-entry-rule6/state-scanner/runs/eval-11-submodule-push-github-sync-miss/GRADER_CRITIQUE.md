# GRADER_CRITIQUE — eval-11 submodule-push-github-sync-miss

评分结果: `with_skill` 5/9, `old_skill` 3/9。两臂差异只落在 A6 与 A9 两条 (详见下)。

先说贯穿三问的一个事实, 后面三问都由它派生:

**本 eval 没有 fixture, 跑在真仓真状态上, 而真状态与 prompt 要求"复现"的世界相反。**
两臂 snapshot 一致显示: 主仓 / `aria` / `standards` 三仓在 origin 与 github 上 `parity: equal`、
`ahead_count: 0`、`behind_count: 0`, `has_pending_push: false`, `gitlink_integrity` 6/6 `ok`,
`drift.hint_type: null`。唯一非 equal 的腿是 `aria-orchestrator` 的
`parity: unknown / reason: no_local_tracking_ref`。也就是说, "GitHub mirror 落后" 这个被测形状
在运行环境里**根本不存在**。

---

## 问 1 — 恒真 / 恒假的断言

### 恒假 (任何臂在本环境下都不可能 pass, 且 pass 只能靠编造)

- **A2 `parity = behind`** — 没有任何一条腿是 behind。要 pass 只能虚构一个 snapshot 里不存在的枚举值。
- **A3 `hint_type: 'push'`** — 两臂 snapshot 的 `sync_status.submodules[*].drift.hint_type` 全为 `null`
  (无 tree/remote drift ⇒ 四分支里走的是 null 那支)。同上, pass 即幻觉。
- **A4 "非零的是 `ahead_count`"** — 全部腿 `ahead_count` 为 `0` 或 `null` (github 那条 unknown 腿是 `null`)。
  没有任何非零字段可点名。
- **A7 `git-remote-helper` 引用** — 这条是**对着已被取代的设计写的**。
  `aria/skills/state-scanner/scripts/collectors/multi_remote.py:8` 自己写明: SOT 指针曾指向
  `git-remote-helper` SKILL.md, "back when this collector was only the fallback ... the in-tree
  topology now ships the collector as the primary integration point"。两臂 snapshot 里
  `method` 全是 `local_refs`, 全文 0 次 `helper`。helper 虽然文件仍在 (`aria/skills/git-remote-helper/`),
  但当前实现路径不调它 ⇒ 对现行 skill 恒假。

这四条 (A2/A3/A4) 更糟的一点: 它们**奖励幻觉**。诚实报告 equal 的臂必然扣分, 编造 behind /
hint_type=push / ahead_count=3 的臂反而得分。作为回归臂, 这个方向是反的。

### 恒真 (任何臂都必然 pass)

- **A5 `remote_commit` 向后兼容字段** — `scripts/collectors/sync.py` 无条件产出该字段, 且
  `:298-299` 注释写死 "fallback chain (`_ORIGIN_HEAD_REFS`) is origin-only by construction"。
  两臂 snapshot 逐字节相同地含 `"remote_commit": "cc864ee…", "remote_commit_source": "local_ref"`。
  这条测的是 collector 的 schema, 不是回答质量; 只要 scan.py 跑通就恒 pass, 零信息量。
  (另注: 断言里 "pointing to origin's remote_head" 与 `multi_remote` 的 `remote_head` 不是同一个量 ——
  前者是 origin 默认分支 head 的 fallback 链 `cc864ee`, 后者是当前分支的
  `refs/remotes/origin/<branch>` = `bb5d375`。断言措辞把两个字段混成一个, 容易被误判。)

### 近似空转 (不恒定, 但对本 eval 无区分力)

- **A1 "不得报告全部 remote 已同步"** — 它的前提句 "when only origin was pushed" 在本环境为假。
  两臂行为完全同构 (都逐腿列 SHA、都点名了唯一那条非 equal 的腿、都明确拒绝拿 push 回执当证据),
  无论判 pass 还是 fail, 两臂同分 ⇒ 零区分力。
- **A6 `has_unreachable_remote: false`** — **这条在本轮实际测的是网络抖动, 不是 skill。**
  `with_skill` 那轮 8/8 fetch 腿成功 ⇒ 报 `false` (pass); `old_skill` 那轮主仓 → github 腿
  `fetch_ok: "false"`, `error_kind = network`, `generation_fetched 118` vs 本轮 `119` ⇒ 它诚实报了
  `TRUE` (fail)。两个 snapshot 的差异是**环境差异不是版本差异**。更糟的是: 被扣分的那臂做的恰是
  正确的事 (如实报告本轮那条腿没亲验, 并说明 fail-CLOSED 降级路径)。
  **建议把 A6 在本轮的 1/0 差当噪声剔除, 不要计入版本结论。**

### 小结

9 条里真正测到"回答质量"的只有 A8 (两臂皆 pass, 但见问 3 的泄漏通道) 和 A9 (标注的 DISCRIMINATOR,
1/0 分开)。A6 的 1/0 是噪声。其余 6 条要么恒假要么恒真。**当前分差 5 vs 3 的可信部分只有 A9 一条。**

---

## 问 2 — 断言完全没覆盖的重要差异

### 【1】"本轮压根没看 master" 这个覆盖缺口 (最重要, 两臂都答出来了, 却零分)

用户问的是 2026-04-12 的 master↔master 镜像漂移。两臂都独立发现并点名: multi_remote 比的是
**每个仓当前 checkout 的那条分支**, 而四个仓当前都不在 master 上 ⇒ 本次 scan 对用户真正问的那个
问题**没有作答能力**。

- `old_skill`: "【3】最要紧的一条 —— 本轮扫描根本没覆盖 `master`。… 它既没说是, 也没说不是, 它压根没看。"
- `with_skill`: "本轮没有测量任何一个仓的 `master`。" 并给了源码依据
  (`collectors/multi_remote.py:365` + `:447`, gitlink 侧 `:1368`)。

这是本 eval 场景下**唯一真正决策相关**的输出, 而断言集一条都没测它。任何一个只会照抄 snapshot
说"全绿"的臂会拿到与它们相同的分数。

### 【2】证据新鲜度的诚实披露

`old_skill` 明确区分了"本轮亲验"与"上一代证据": 主仓 github 腿本轮 fetch 失败, `equal` 依据的是
72 秒前的 ref, 并解释了 `stale_unverified → expired → unknown/not_refreshed ⇒ overall_parity=false`
的 fail-CLOSED 链。`with_skill` 那轮没有这个情形, 所以无从比较。断言集不但没奖励这种披露,
A6 还反向惩罚了它。

### 【3】推荐下一步的相关性 (真实质量差, 未测)

- `old_skill` 首选项 = `verify-remote-parity` (直接回答用户问的那件事: 逐 remote 核 master + 重扫补齐失败腿), 带规则 id 与置信度。
- `with_skill` 首选项 = 回本 cycle 主线 Rule #6 AB, 把"补测 master"放到选项 [2]。

对一个"请告诉我哪些 remote 需要补推"的提问, 首选项是否指向该问题本身, 是明显的质量差异, 断言集没测。

### 【4】issue 面联动

`old_skill` 从 live issue 列表里挑出 Aria#165 (标题就含 "orphaned gitlink (clone --recursive 断裂)")
并标注 "就是你要复现的那一类", 另挂 Aria#176; `with_skill` 只提 #176。断言未测。

### 【5】两臂共有但未测的其他质量点

- 都识破了 issue 计数顶到 `limit=20` 的截断 (报 47 是下界), 并引 handoff 实测值 65。
- 都给了 CLAUDE.md 硬约束 2 的 `ls-remote` 逐 remote 核验命令 (只读, 不信 push 回执)。
- `with_skill` 额外给了 bump 次序规则 (先推子模块两端并 ls-remote 核验, 再 bump 主仓 gitlink), 直接对应 2026-07-14 事故。
- 长度: `old_skill` 273 行 vs `with_skill` 186 行 —— token 成本差未测。

---

## 问 3 — 仓内语料污染

### 直接引用: 两臂都**没有**引用 `openspec/changes/a1-entry-claim-duplicate-work-guard/` 下的文档

- 两份 answer.md 里都不出现 `openspec/changes/…/proposal.md|tasks.md|detailed-tasks.yaml` 这类路径。
- 它们引到的任务号与计划串 (`TASK-038`、`TASK-036`、`7.6`、`8.1 → 8.4 → 8.2`、`vNEXT = 1.70.0`、
  sweep 死线 `2026-09-06T21:40Z`、`ARIA_COORDINATION_NO_PUSH` 会话级前置) 全部可在
  `docs/handoff/2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md` 命中,
  且两臂都显式标注来源为 handoff:
  `with_skill` "gitlink bump 归 TASK-038/8.2"、"handoff §3 第 1 条已实测"、"按 handoff §6 的入口优先级排";
  `old_skill` "（handoff §0 第 1 条：gitlink bump 归 TASK-038/8.2…）"、"handoff §3 第 1 条"、"handoff §6 第 1 项"。
- 两臂用到的深层机制术语 (`1.35 第三路`、`benign unknown`、`no_local_tracking_ref`、
  `_apply_freshness_downgrade`、`gitlink_integrity`、`evidence_grade`、`multi_remote.py:365/:447/:1368`、
  "v9 六路分派") 在 spec 目录三份文档里 grep **全 0 命中** ⇒ 来自技能文件与源码, 属正当来源。

### 但存在三条结构性泄漏通道, 两臂都在其中

**通道 A — scan.py 自己把 spec 目录塞进上下文 (设计使然, 两臂对称)**
snapshot 的 `openspec.changes.items[0]` 直接带
`"path": "openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md"` 与整段 raw_status 散文;
`a1-entry-claim` 在每份 snapshot 里出现 253 次。内容只是状态头, 不含多远程设计, 所以**没有**泄漏
被测断言; 但"技能产物必然携带在制 Spec 文本"这条通道对任何 state-scanner eval 都成立, 值得记一笔。

**通道 B (关键) — A8 的承重内容逐字写在恒加载的 CLAUDE.md 里**
`CLAUDE.md:88`: "主仓随后 bump gitlink 即产生 orphaned gitlink, GitHub `clone --recursive` 断裂
(2026-07-14 事故)"; `CLAUDE.md:90`: "推后逐个 `ls-remote` 核验, 不信 push 回执"。
两臂的 A8 表述与 A1 的"不信 push 回执"框架都与这两句同形, `old_skill` 甚至直接写
"按 CLAUDE.md 多远程硬约束 2（推后逐个 `ls-remote` 核验，不信 push 回执）"。
⇒ **A8 与 A1 可以在零 skill 贡献的情况下 pass**, 它们测的是 CLAUDE.md 不是 state-scanner。

**通道 C — 同一句话在 spec 目录与 live issue 标题里还各有一份**
`openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml:1195`:
"否则 orphaned gitlink ⇒ GitHub clone --recursive 断裂 (2026-07-14 事故形状)";
以及 `old_skill` 从 issue collector 拉到的 Aria#165 标题里的 "orphaned gitlink (clone --recursive 断裂)"。
三重可得 ⇒ A8 实际区分力约等于 0 (虽然两臂并未引用 spec 那一份)。

### 结论

**没有发现哪一臂"引用了 spec 目录文档"式的污染**; 但 A8/A1 被 CLAUDE.md 恒加载语料泄漏,
应视为不可用于版本判定的断言。

---

## 给 eval 维护者的处置建议

1. 本 eval 若要继续用于回归判定, 必须**造 fixture**: 一个 github 真落后的临时仓 (或把合成 snapshot
   直接喂给回答阶段), 否则 A2/A3/A4/A7 恒假、A5 恒真, 全套只剩 A9。
2. A6 改成读 snapshot 实际 `fetch_ok` 分布后再判, 或直接删除 —— 现在它是网络抖动探测器,
   且惩罚诚实披露。
3. 把"是否点出 scan 只覆盖当前 checkout 分支、未覆盖 master"提为一条正式断言 —— 这是本场景下
   区分"照抄绿勾"与"真懂判据边界"的最强信号, 两臂都做到了, 却没有任何断言承接。
4. A5 若要保留, 措辞需区分 `sync_status.submodules[].remote_commit` (origin 默认分支 fallback 链)
   与 `multi_remote…remotes[].remote_head` (当前分支 tracking ref) —— 现措辞把两者混为一谈。
5. A7 要么删除, 要么改成断言 collector 主路径 (`method: local_refs`), 因为 helper 已非集成点
   (`multi_remote.py:8` 明写)。

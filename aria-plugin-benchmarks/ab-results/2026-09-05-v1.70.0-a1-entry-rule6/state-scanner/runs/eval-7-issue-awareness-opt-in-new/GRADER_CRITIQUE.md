# GRADER_CRITIQUE — eval-7 issue-awareness-opt-in-new

判定结果: `with_skill` 4/8, `old_skill` 4/8 (逐条见各臂 `grading.json`)。两臂**总分持平**, 但通过的条目不同 (A4 只有 old_skill 过, A6 只有 with_skill 过), 且**分数与两臂真实质量差距几乎无关** —— 详见第 2 节。

判定口径先声明 (便于复议): 断言点名**字面串**的 (如路径 `.aria/cache/issues.json`、10 个 fetch_error 枚举值), 要求逐字出现; 断言里**不可观测的内部机制修饰语** (A6 括号里的 "word boundary protection"), 只要主句机制被明确描述即算 pass, 并在下方点名两臂都未证。

---

## 1. 恒真 / 恒假 (零信息量) 的断言

本套 8 条里**只有 A4、A6 两条真的产生了区分**, 其余 6 条在本 fixture 上结构性零信息:

| 断言 | 性质 | 理由 |
|------|------|------|
| A1 "Show Open Issues section **only when** enabled is true" | **恒真** | fixture 只有 `enabled=true` 一个取值, "only when" 的负分支 (enabled=false ⇒ 不得出现该区块) **在本 eval 里根本没有被执行的机会**。任何把 snapshot 渲染成报告的回答都会印出 issues 区块 ⇒ 两臂必过。要有信息量必须配一条 `enabled=false` 的对照 fixture。 |
| A5 "NOT manage API tokens inside the skill" | **恒真** | 负向断言, 但没有任何可信的违反路径 —— 一份扫描报告不会主动提议在 skill 内管 token。两臂连提都没提。它测的是「AI 有没有胡说」, 不是技能能力。 |
| A7 "recommend triage **when** blocker/critical labeled issues exist" | **前件为假 ⇒ 空真** | 本语料 `label_summary = {"bug": 1}`, 74 条 open issue 里带 label 的只有 1 条, blocker/critical 命中 0。断言点名的分支根本没触发。**讽刺的是两臂都自己发现并写明了这一点** ("规则在这个语料上结构性恒绿, 属于零信息量" / "它不是在告诉你没有阻塞项, 而是在告诉你这个通道没有信息") —— 被测 AI 识破了这条 fixture 的缺陷, 而断言本身继承了同一个缺陷。我按「是否逐字给出规则名+触发条件且判定正确」判两臂 pass, 但这是**知识复述**的通过, 不是行为验证。 |
| A2 "4-tier platform priority" | **近恒假** | 一次成功的在线扫描, 输出面只会有 `platform: forgejo` 这一个结果值; 四级优先级链是内部实现, 报告里不会出现, 除非 AI 去背 SKILL.md。两臂都只印出平台取值 ⇒ 都 fail。要测它得造 fixture: config 无 platform 字段 / hostname 不在映射表 / 只能靠 URL 推断。 |
| A3 "CLI wrapper (not raw curl) + 10 个 fetch_error 枚举" | **近恒假, 且是复合断言** | 同上, 且第二半 (10 个枚举逐一 handle) 在 `fetch_error: null` 的健康路径上**不可能**出现。两臂 fetch_error 都只出现取值。这条实际上惩罚「没有背诵实现细节」, 不区分能力。 |
| A8 "fail-soft when offline / CLI missing" | **恒假** | fixture 没有注入任何失败 (缓存 6m 内命中, `fetch_error: null`)。降级路径不可能被观察到。两臂都 fail —— 这个 fail **不含任何关于两臂差异的信息**。 |

小结: 8 条里 3 条恒真、3 条近恒假, **只剩 A4/A6 有区分力**, 而这两条区分的还是「有没有把路径字面/启发式机制写进报告」这种叙述习惯, 不是扫描质量。这个断言集整体是**面向 SKILL.md 实现细节写的**, 而被评对象是**一份扫描报告**; 两者的可观测面基本不相交。另外要注意: 两臂消费的 `state-snapshot.json` **逐字节相同** (606519 bytes, 同一 mtime), 所以凡是描述 collector 行为的断言 (A2/A3/A4/A8) 都不可能被 AI 侧拉开差距 —— 它们测的是 scan.py, 不是被评的回答。

## 2. 断言完全没覆盖的重要差异

### 2.1 【最重要】`issue_scan` 静默截断 —— 两臂都报了, 但证据等级差一个量级 (0 条断言覆盖)

**是的, 两臂都发现并报告了这个真实缺陷** (快照 `open_count=47` 远小于 API 真值), 但方式完全不同:

- **`with_skill` 做了本轮独立实测**, 给出逐仓对照表: Aria 20/**26**、aria-plugin 20/**41**、aria-orchestrator 2/2、aria-standards 5/5 ⇒ 47 vs **74**, 吞掉 **27 条 (36%)**。
  **我用 forgejo CLI wrapper 逐仓独立复核过: 26 / 41 / 2 / 5 —— 与它给的数字完全一致。**
  它进一步点名了被吞掉的具体条目 (aria-plugin#135 / #107 / #109 / #110 / #117 / #138–#142, Aria#136 / #151 / #5)。我把 snapshot 与 API 做了 number 级差集:
  `Aria missing = [164, 151, 136, 120, 59, 5]`、`aria-plugin missing = [142,141,140,139,138,136,135,133,132,131,130,129,127,123,120,117,114,110,109,107,92]` —— **它点名的每一条都真的在缺失集里, 无一虚构**。
  还给出了机制与后果: `limit=20` 是逐仓上限 + 按 issue number 降序取前 20 ⇒ **老的、更根本的问题被系统性隐藏**; 与当前轨最相关的 #135/#107/#109 恰好全在隐藏的 27 条里; 被吞的还包括一条 secret 泄漏 (Aria#136) 和一条「扫描器自报假绿」(aria-plugin#110)。并明确声明**下游分级改用 API 全量 74 条**。
- **`old_skill` 是从饱和信号推断 + 引用上一份 handoff 的旧测量**: "10CG/Aria = 20 条, 10CG/aria-plugin = 20 条 ← 两个仓恰好各 20 = 顶到上限", 然后引 handoff §2 M2 的 "snapshot 报 46 / API 实拉 65", 得出 "**大约还有 18 条**"。
  这个数**今天已经不对了**: 真值 74, 缺口 27。它把**几小时前另一 session 的摘要当成了本轮测量** (正是 memory `past-summary≠measurement` 的形状)。方向对、量级低估 1/3。且它的分级 A/B 只在可见的 47 条上做, 因此**结构上不可能包含 Aria#136 (secret 泄漏) 和 aria-plugin#110 (假绿)** —— 这两条恰恰是最该进 A 组的。

同一形状的第二例: `with_skill` 写 "`tracks_multibranch` 里有 **106** 条 track 仍报 active" (我核 snapshot: `Counter(status)` 里 active **恰为 106**, 本轮实测); `old_skill` 写 "31 条 5 月的交接仍报 active" —— 那是 issue #182 标题里的历史数字, 被当成现状陈述。

**没有任何一条断言碰到这些。** 一个 4/8, 另一个也 4/8。这是本 eval 最大的失真: 区分两臂的关键能力 (对自身数据做独立复核, 而不是转述既有结论) 完全在计分面之外。

### 2.2 其他未覆盖差异

1. **原始清单可读性 (对 old_skill 有利)**: `old_skill` 逐仓完整列出 47 条 (编号+标题+已关联 US), 用户 "想了解 open issues" 的字面诉求得到直接满足; `with_skill` 压成分级表格 + 主题聚合, 单条可浏览性差 (分级 D 里同一个 `#164` 同时出现在「协调/Layer L」和「功能/采纳」两行, 属小瑕疵)。**没有断言测「清单完整呈现」。**
2. **处置成本不同**: `old_skill` 给的是**当场可执行的配置修法** (`limit: 20 → 100` + 删缓存 + 重跑, 约 10 分钟); `with_skill` 给的是**代码级修法** (limit 语义改为「顶满置 `truncated` 标记」或分页拉全量) 并把它提为新 Spec 推荐项 [1]。前者立刻解用户的问, 后者治类级根因。断言不评这一维。
3. **Rule #10 / 交接优先级的处理不同**: `old_skill` 显式写 "这是产品级取舍, 我按 Rule #10 不自行改序, 把选项摆出来由你定", 并把 handoff §6 排第 1 的 a1-entry 续做放在 [3]; `with_skill` 把 fix-truncation 提为 [1]、把 handoff 优先级 1 降为 [2] (理由: 会话级前置本会话补不上)。这是**方法论层面的实质差异**, 零断言覆盖。
4. **副作用声明**: `old_skill` 有明确的收尾声明 "全程未写任何 claim、未推任何 ref、未改动仓库文件"; `with_skill` 只在 claim 段内联说明 "本次扫描是只读的, 没有替你刷心跳"。AB 语境下 (评测 AI 会误推生产协调 ref) 这条本该被测。
5. **heartbeat / claim 操作指引**: `with_skill` 给出 sweep 死线 `2026-09-06T21:40Z` 与 "先 fetch 再刷" 的顺序警告 (含 `python3 -B`); `old_skill` 给出 phase1_gate advisory 的调用形态与 reconcile 仲裁规则。两者互补, 都不在断言面上。

## 3. 是否引用了仓内 `openspec/changes/a1-entry-claim-duplicate-work-guard/` 下的文档?

**两臂都没有。** 逐条核过:

- 两臂都出现 `a1-entry-claim-duplicate-work-guard` 这个 **change 名**与 `31/40` 进度, 但这两项是 `state-snapshot.json` 的 `openspec` collector 机械字段 (with_skill: "OpenSpec: a1-entry-claim-duplicate-work-guard (approved, 31/40 tasks)"; old_skill: "OpenSpec: a1-entry-claim-duplicate-work-guard (approved, 进度 31/40)"), **不是读 proposal.md / tasks.md / design.md**。两份回答中 `proposal.md` / `tasks.md` / `design.md` / `openspec/changes` 字样 grep **0 命中**。
- 任务组编号 (`Group 7` / `7.6` / `Group 8` / 执行序 `8.1 → 8.4 → 8.2` / `vNEXT = 1.70.0`) 看似来自 tasks.md, 实际来自 **handoff**: `docs/handoff/2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md:53-55,176` 逐字写着这些 (H1/H2/H3 与 §6 优先级 1)。`old_skill` 自己标注了来源 —— "最新 handoff §6 的排序是"。

**但要提请注意另一条污染通道 (同 memory `ab-baseline-leaks-via-repo-corpus` 形状)**: 两臂都重度依赖**同一份 handoff**, 而这份 handoff §2 M2 已经把 "`issue_scan.open_count` 静默截断 (46 报 / 65 实, limit=20 顶满且零截断标记)" **成文写好了**。也就是说:

- 第 2.1 节那个「真实缺陷发现」, 在两臂那里**都至少有一半是「读到的」而不是「发现的」** —— `old_skill` 基本就是转述它 (连数字 46/65 都照抄);
- **只有 `with_skill` 越过了语料**: 它本轮重新逐仓打 API 得到 26/41/2/5 = 74, 并算出与今天 snapshot 的 27 条差额、点名具体缺失 issue。这部分是**语料里没有的、可独立复核为真的新证据**。

所以对 "哪一臂真的发现了缺陷" 这个问题的诚实回答是: **两臂都报告了它, 但只有 `with_skill` 独立测量并把量级修正到今天的真值 (74/27), `old_skill` 复述了一个已经过期的量级 (65/18)。** 而这一整块在当前断言集上**得分完全相同**。

## 4. 给套件维护者的具体建议

1. **补对照 fixture 才能救活 A1/A2/A3/A8**: 一条 `issue_scan.enabled=false` (验 A1 负分支)、一条 config 缺 `platform` 且 hostname 不在映射表 (验 A2)、一条断网 / wrapper 不在 PATH (验 A8+A3 的枚举)。健康在线路径上这四条永远是同一个答案。
2. **A7 换语料或换判据**: 现语料 74 条只有 1 个 label, `open_blocker_issues` 结构性恒绿。要么造带 blocker/critical label 的 fixture, 要么把断言改成「必须指出 label 通道为空 ⇒ 机械 blocker 检测在此语料上零信息, 不得当作『没有阻塞项』的正证据」—— 后者两臂都会过, 但那是它们**真做对了**的事, 至少不是恒真。
3. **补一条覆盖 2.1 的断言**: 例如「当 `open_count` 等于 `issue_scan.limit × 顶满仓数` 时, 必须声明清单可能被截断, 且**不得**在未声明的情况下基于该清单断言『没有阻塞项』」, 再加一条更硬的 [承重]:「若做了独立复核, 复核数字须逐仓可验证」。这才能把 47-vs-74 与 65-vs-74 拉开。
4. **A3/A4/A6 的复合断言拆条**: 现在「wrapper vs curl」和「10 个枚举」绑在一条里, 一半没证据就整条 fail, 无法定位失分原因; A4 的三要素 (cache / 15m TTL / 路径字面) 同理 —— 本 eval 里两臂的唯一分差就卡在「路径字面有没有印出来」这种低价值元素上。

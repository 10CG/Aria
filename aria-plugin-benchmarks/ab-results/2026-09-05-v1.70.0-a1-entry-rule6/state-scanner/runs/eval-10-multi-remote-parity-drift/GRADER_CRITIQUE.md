# GRADER_CRITIQUE — eval-10 multi-remote-parity-drift

评分结果: **with_skill 9/12 · old_skill 7/12** (差异落在 #5 与 #9 两条)。

## 0. 前置事实 — prompt 的前提与夹具不符 (影响下面全部判断)

snapshot (`sync_status.multi_remote`; 两份 snapshot 文件整体 md5 不同 —— 各自跑了一次扫描 —— 但 `multi_remote` 子树两臂逐字段完全相同, 已比对) 的真实取值:

- `overall_parity: true`, `has_pending_push: false`, `has_unreachable_remote: false`
- 主仓 / `aria` / `standards` 在 `origin` 与 `github` 上全部 `parity: equal`, `ahead_count: 0`, `behind_count: 0`, `evidence_grade: fresh`
- 唯一非 equal 的一格: `aria-orchestrator` × `github` = `parity: unknown`, `reason: "no_local_tracking_ref"`, `ahead_count: null`, `behind_count: null`, `evidence_grade: fresh`
- `gitlink_integrity[]` 6 项 (2 remote × 3 子模块) **全部 `status: ok`**, 零 orphaned / 零 orphan_unverified
- 仓内插件版本 SOT = **1.69.1**, 不存在 `v1.15.0`

也就是说 prompt 描述的「推了 origin, 漏推 github」这一漂移在夹具里**根本不存在**, 而且连它的前置动作 (gitlink bump / 子模块合 master) 都尚未发生 —— 三个子模块仍是 workdir 与 gitlink 不一致的 dirty 态。两臂都独立发现并明说了这一点。

## 1. 恒真 / 恒假 (零信息量) 的断言

**恒假 (本夹具下任何诚实回答都拿不到 pass)** —— 共 3 条, 全部因为它们要求描述不存在的漂移:

1. **#3 (ahead_count>0 量化)** —— 断言要求「用本形状下真正非零的字段量化漂移: ahead_count>0」。夹具里所有 `ahead_count` 不是 `0` 就是 `null`, 没有任何一格是 ahead。要拿 pass 只能编造。两臂 false。附带一提, 该断言把 `behind_count` 定义为 field-truth error, 而 old_skill 写了「落后 (behind) 的 remote: 0 个」—— 这是对夹具的**正确**陈述 (确实 0 个 behind), 不构成断言所指的误用; 我按「未用 ahead_count 量化」判 false, 未因这句额外扣分。
2. **#7 (parity: ahead 的判读)** —— 要求论证「`overall_parity: true` 与 `has_pending_push: true` 并存不矛盾」。夹具 `has_pending_push: false` 且无任何 ahead 格, 这个组合在数据里不存在。两臂 false。
3. **#12 (DISCRIMINATOR)** —— 要求把 gitlink 归因**作为 multi_remote_drift 的一条已接线 dispatch 路由**外化, 并附 `git -C <submodule> push <remote> <branch>` 修复命令。夹具 `gitlink_integrity` 6/6 = ok, 这条路由**结构上无从触发**, 只有靠反事实小作文才可能碰到 pass。**本套件最贵的一条断言 (v1.62.0+ 版本鉴别位) 在这个夹具上是死的** —— 两臂 0-0, 鉴别力为零。要救活它, 夹具必须造出一个真 orphaned gitlink (例如子模块 commit 只在 origin 存在), 否则这条应从本 eval 移除、移到专门的 gitlink-orphan 夹具去。

**恒真 (空真, 前件不成立)** —— 1 条:

4. **#10 (has_unreachable_remote=true 时不得走六路 dispatch)** —— 夹具 `has_unreachable_remote: false`, 前件永不成立; 只要回答不凭空发 drift 告警就 pass。两臂都 pass, 零区分度。第二半句 (`has_pending_push` 单独不构成 drift 警告) 同理 —— `has_pending_push: false`。

**准恒真 (任何把 multi_remote 区块如实转述出来的回答都过)** —— 3 条: **#1 / #2 / #4**。这三条只要求「有 per-remote 区块 / 枚举 remote / 不给单一 up-to-date 结论」, 两臂都是逐格表格, 全 pass。特别是 #4 的后半「must distinguish origin-synced from github-not-synced」在本夹具里**没有指称对象** —— github 该同步的都同步了。

**#6 (per-remote 修复命令) 被夹具削弱**: 「the lagging remote」无指称对象。两臂都拿到 pass, 但拿法是偶然的 —— with_skill 是在发版流程段里出现字面 `git -C aria push github master`; old_skill 用的是占位符 `git -C aria push github <branch>` + 具体的 `git -C aria-orchestrator push -u github feature/m6-cost-model-telemetry`。若严格按「特定字符串形态不得同义替换」判, old_skill 这条会翻成 false; 我认为断言自身就带 `<path>` 占位符, 意在形态而非字面, 故按形态判 pass。**这条判定对措辞敏感, 是本轮最脆的一个 pass。**

**#5 的前提句也与夹具冲突**: 断言写「in this scenario the missed mirror computes as parity=ahead, which clause 4 excludes」—— 夹具里那格是 `parity: unknown / no_local_tracking_ref`, 不是 ahead。所幸可评的那半 (1.35 到底触不触发 / 触发就是错) 在 unknown 路径上结论相同 (benign unknown 同样不触发), 所以这条**仍有区分力**, 但理由链与断言写的不是同一条。

**真正承载信息量的只剩 4 条: #5 / #8 / #9 / #11。** 12 条里 3 条恒假 + 1 条空真 + 3 条准恒真 + 1 条脆弱 = 8 条几乎不产出信号。这是本套件最长的一条断言链, 有效位却只有 1/3。

## 2. 断言完全没覆盖的重要臂间差异

### (a) old_skill 独有的三条 scope 边界 —— 直接决定用户问题能不能被真正回答

这是本轮**最大的未覆盖差异**, 而且它偏向 old_skill:

1. **parity 只覆盖各仓当前 checked-out 分支, 不覆盖 master**: 「如果你说的发布动作发生在 master 上, 这次扫描看不到它」。用户描述的「发布 + push origin」按 Aria 的发版流程发生在 master, 而两臂扫的都是 feature 分支 —— 只有 old_skill 点破「零 behind」这个结论**在用户关心的那条线上根本没作证**。
2. **tag 空间完全不在检测范围** (`multi_remote` 是 RM-11 有意的 branch-reachability only), 而「发版」通常含 tag —— old_skill 因此在核验命令里单列了 `ls-remote --tags` 两行。with_skill 全文不提 tag。
3. **gitlink bump 尚未发生**: 「`aria` workdir `ab3dbd0` vs 主仓记录的 gitlink `7dd0135` ... 也就是说 gitlink bump 尚未发生, 自然谈不上『推了 origin 漏了 github』」—— 这是对 prompt 前提的**机制级**证伪 (不只是「SHA 都相等」的观测级证伪)。

三条都没有任何断言覆盖。它们恰恰是「诚实回答一个前提错误的问题」的核心能力。

### (b) with_skill 独有的规则层外化 —— 部分被 #5/#9 捕到, 但不完整

- 点名 `enforced_remotes_resolved: origin, github (无只读排除)`、规则 1.35 / 1.36 的 dispatch 归档、`overall_parity: true` 的正证据语义 (「至少有一条新鲜的 equal 正证据」)。
- 把 `overall_parity: true` 与表中存在 unknown 格的并存, 显式挂到 **Aria#176** (AC-5 未排除本仓不存在的 remote) 这个已在册缺陷上 —— 即「工具当前判定口径的已知局限」。old_skill 也提了 #176, 但只在 issue 清单里带过, 没和自己刚给出的结论绑定。
- **推断 vs 测量的自觉**: with_skill 明写「这是**推断, 不是测量**, 因为 snapshot 只给『没有 tracking ref』, 不给『远端也没有』」, 并把 `ls-remote` 确认排成第【1】步、推送排在第【2】步。old_skill 只说「大概率」, 也给了 `push -u` 命令但没把「先 ls-remote 确认」设成前置。这个「先证伪再动手」的差别没有任何断言测。

### (c) 两臂共有、但断言体系完全无视的最重要行为: **拒绝接受 prompt 的错误前提**

两臂都在开头就说清「本轮没有证实 github 漏推」+「不存在 v1.15.0, 当前 SOT 是 1.69.1」+「不要为保险随手补推」。这是本夹具下唯一真正重要的质量维度, 12 条断言里**一条都没有奖励它**, 也没有惩罚「顺着前提编一个漂移出来」。建议给这类前提错位夹具补一条断言: 「必须指出 prompt 描述的漂移在本仓不存在, 且不得虚构 v1.15.0 相关状态」—— 那条才是这个 eval 该测的东西。

### (d) 其他未覆盖的小差异

- with_skill 给了可直接跑的**批量核验脚本** (for 循环遍历 origin/github × 三仓, 输出短 SHA 与本地比对); old_skill 给的是逐条 `ls-remote` 清单 + master/tag 两条补充线。前者更省事, 后者覆盖面更宽。
- with_skill 把 `overall_parity` 的解读风险单列成「🔴 一条要提醒你的裁决层局限」区块; old_skill 用「信任边界」一句话带过, 但额外给出了 schema worked example (`origin=equal, github=unknown` → `true`) 作为依据。
- with_skill 引「按 Spec 执行序是 8.1 → 8.4 → 8.2」, 而该序列的出处其实是上一份 handoff (§H3 行) 而非 Spec 本体 —— **来源归属滑坡**, 内容正确但署错了 SOT。old_skill 同一内容署为「上次交接的高优先级」, 归属正确。断言无覆盖。
- 两臂都指出了 `issue_scan.limit=20` 导致 open 47 被静默截断; 两臂都提 Aria#165 是用户所担心故障的类别。无差异。

## 3. 是否有臂引用了仓内 `openspec/changes/a1-entry-claim-duplicate-work-guard/` 下的文档?

**结论: 没有直接证据表明任一臂读了该目录。两臂全部 spec 级 token 都能在 handoff 里找到出处。** 逐条溯源:

| 出现在回答里的 token | 臂 | 溯源 |
|---|---|---|
| `TASK-038/8.2`、「三个 dirty 有意保持」 | 两臂 | handoff `2026-09-05-2200-...md` **L18** 逐字含 「(gitlink bump 归 TASK-038/8.2, 要等各自合 master 之后)」; 两臂都明写「上次 handoff §0 明写」 |
| `8.1 CHANGELOG + 版本 SOT 5 文件 → 8.4 → 8.2`、`16 版本点`、`vNEXT = 1.70.0` | 两臂 | handoff **L55** (H3 行) 逐字含全序列; 「16 版本点」在 handoff 出现 2 次、在 spec 目录 **0 次** |
| `TASK-036 (7.6)`、「依赖阻塞」 | 两臂 | handoff **L21 / L54** |
| `31/40`、sweep 死线 `2026-09-06T21:40Z` | with_skill | handoff L19 / L102 (`31/40` 在 handoff 出现 8 次) |
| `RM-11` (multi_remote 是 branch-reachability only) | old_skill | 技能文件: `aria/skills/state-scanner/references/state-snapshot-schema.md` + `scripts/collectors/multi_remote.py`; spec 目录 grep **0 命中** |
| 规则 `1.35` / `1.36` / `OQ-C` / benign unknown 分档 | with_skill | 技能文件: `aria/skills/state-scanner/RECOMMENDATION_RULES.md` L12 + `references/rules/basic-rules.md` §1.35 (含 OQ-C 裁定原话); spec 目录 **0 命中** |
| `AC-5` (Aria#176 形状) | 两臂 | handoff 出现 2 次 |

- 两臂回答里 **0 次**出现 `openspec/changes` 路径、`proposal.md`、`detailed-tasks.yaml` 或 `tasks.md` 字样。
- handoff 指针本身是 snapshot 合法字段 (`handoff.latest_path`, `latest_source: "pointer"`), 读它属技能设计内行为, 不算语料污染。
- **唯一需要留痕的疑点**: with_skill 写「按 **Spec** 执行序是 8.1 → 8.4 → 8.2」。这句把 handoff 的 carry-forward 说成 Spec 原文。内容与 handoff L55 逐字一致, 且「版本 SOT 5 文件」这一措辞 handoff 与 `tasks.md` 两边都有, 无法据此判定它读了 tasks.md —— 更可能是 **handoff→Spec 的来源归属滑坡** (memory `handoff≠spec` 那一族的形状), 而非污染。判定: 不构成仓内语料污染证据, 但如果要彻底排除, 需要 transcript 级的工具调用记录 (本 eval 无 transcript)。

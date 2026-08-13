---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-13T01:43:39.000Z
context: openspec/changes/premerge-gate-branch-existence/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R5 — backend-architect (Spec A `premerge-gate-branch-existence`)

角度: 实现可行性 —— 插入点 / 退出码分区穷尽性 / 异常·重试·解码三轴 / 「纯 additive」代码级复核。

## 0. 方法论声明

本轮**逐条独立回源实跑**, 不采信 R4-fix 的自述/commit message。核对方式: `git diff ff847fb 45c480a`
拿到本轮真实改动的逐字 diff, 对 diff 里每一条「实测 X」的断言重新跑一遍命令; 对「不修」的 15
条按 brief 要求当交付物审; 并对全部机械锚做了跨全文件的重复匹配扫描 (而非只验局部区间, 吸取
R4 qa-engineer 抓到的教训——那正是我自己上一轮 PASS(0 findings) 的漏检形状)。

## 1. R4 的 12M 是否真闭合 (写下来 vs 闭合)

R4 五席共 12 条去重后 Major (含 3 次重复上报的 `§非目标:844` landmine 算 1 条), 我逐条实跑复核:

| # | R4 Major | 处置 | 复核方式 (本轮独立实跑) | 结论 |
|---|---|---|---|---|
| 1 | delegate 失效「必然出六条 TASK」 | 改判 | 读 `DUAL_LAYER_SPEC.md:90-93/:104-152`, `grep -c '^## What$'`=0, `grep -c '^### Key Deliverables'`=0 | ✅ 真闭合 |
| 2 | `§非目标:844` landmine 第四份拷贝 (tech-lead+qa+code-reviewer 三次独立命中) | 改写 | `grep -n '步骤 3 硬编码' proposal.md` 今日零命中 | ✅ 真闭合 |
| 3 | DEC §5.3 未执行/未上呈 | 补执行+改文本 | `grep -n 'status:' B/detailed-tasks.yaml` → TASK-003/4/5/7/8/9=cancelled, TASK-006=pending, 21 条 pending15/cancelled6 | ✅ 真闭合 |
| 4 | Level (b) 跨模块仍自造判据 | 改判据为四条件逐条对账 | 读 `LEVEL_GUIDE.md:153-163` 逐条核对 proposal.md 新文本 | ✅ 真闭合 |
| 5 | Level (c) Breaking 是版本裁定函数, 与「不得合并处理」冲突 | 加依赖声明+改措辞 | 读新增 D-c (i)(ii) 段与 :119 附近新文本 | ✅ 真闭合 |
| 6 | SC-A-step (a)(b) 无法断言过度收口 | **明确不修**, 收窄措辞 + 3 条理由 | 见下 §3 | ⚠️ **部分闭合 —— 收窄措辞属实, 但新增的「残余风险有界」论证本身含事实错误** (§3) |
| 7 | SC-A10c 例外括注在移动中丢失 | 补回括注 | 读 `base.py:79-85` docstring「Default: always (True, "")」+ 读 R2-fix(`017eb54`)确认原文即在 | ✅ 真闭合 |
| 8 | SC-A-note 锚点非全文件唯一 (qa 单席抓到) | 加「章节内首个匹配」 | `grep -n '**Output schema**\|**配置参数**:' SKILL.md` = 264/281/501/523; `grep -n '^### '` 确认 `### C.2.4`=:218, 下一 `###`=:306, 264/281 均落区间内、501/523 均落区间外 | ✅ 真闭合 |
| 9 | 定档依据两处 SOT 行锚错位 (LEVEL_GUIDE.md:26, project.md:116) | 改锚+加说明 | `sed -n '26p;29p' LEVEL_GUIDE.md`、`awk 'NR==116;NR==117' project.md` 逐字复核 | ✅ 真闭合 |
| 10 | O-1 gitlink 证据命令零区分力 | 换命令 | 见下 §2 —— **换的命令有新的盲区, 半闭合** | ⚠️ **部分闭合** |

**统计**: 10 条去重 Major 中, 8 条**完全真闭合**(实跑验证, 非转述), 2 条**只闭合一半**(#6 的论证本身有事实错误; #10 的新命令有未测到的盲区)。**没有发现"写下来但根本没变"的纯 paper-fix** —— 这是本 Spec 四轮以来第一次没有该类问题,是显著的质量提升信号。

## 2. 新发现 — O-1 gitlink 证据命令的新盲区 (Major, `introduced_by_r4fix: true`)

R4-fix 把 O-1 完成判据的 gitlink 证据命令从 `git diff --submodule=short`(提交后恒空,R4 code-reviewer 抓到)换成 `git show --submodule=short <ship-commit> -- aria`,并用 `fb5ed36`(已 bump)/`98ad1f5`(未 bump)两个 commit 验证「两向可区分」。

**问题:两个验证用 commit 都是单亲(非 merge)commit,而 `git show`(patch 模式)对 merge commit 默认不显示任何 diff —— `--submodule=short` 同样受此影响,即使 gitlink 确实在该次合并中被 bump。**

本仓可复现:
```
$ git log -1 --format="parents=%P" 5b8c3dc
parents=889f9e0 f399e71          # 2-parent, merge commit
$ git show --submodule=short 5b8c3dc -- standards | wc -l
0                                  # 该 merge 确实 bump 了 standards, 但输出 0 行
$ git show -m --submodule=short 5b8c3dc -- standards
diff --git a/standards b/standards
index 9df1722..79b7cd6 160000
--- a/standards
+++ b/standards
@@ -1 +1 @@
-Subproject commit 9df17222da1eaa652099e984da3b48e6723bb48e
+Subproject commit 79b7cd656079b1e92430949c053b8303a42be25a
```
加 `-m` 后两向仍可区分(对 `fb5ed36`/`98ad1f5` 重跑 `-m` 结果不变——已验证)。

**这不是边角场景**:CLAUDE.md 逐字「例外:主仓 (Aria) 自身 PR 可走 Forgejo merge」——Spec A 自己就是主仓 PR,它自己的 O-1 gitlink bump 完全可能落在一个 Forgejo 服务端合并产生的 2-parent commit 里。实测本仓 `git log --merges --oneline -10 | wc -l` = 10,`git log --oneline -30 | wc -l` = 30 ⇒ **最近 30 个提交里 10 个是 merge commit,占三分之一**,这是本仓的常态落地形态,不是小概率分支。

**how_it_goes_red**:D.2 执行者贴出 `git show --submodule=short <merge-commit-SHA> -- aria` 的 0 行输出作为「已完成」证据 —— 这与漏 `git add aria` 的输出**逐字节相同**(R4 code-reviewer诊断旧命令时用的原话,现在原样适用于新命令的这个分支)。落入与 B 侧 R4 Critical(`TASK-017` orphaned gitlink)同一形状,而这条命令**正是 Spec 自己声明的「O-1 唯一的人工判据」**(`D-b`:「O-1 今日没有任何机械兜底」)。

**为什么这是 `introduced_by_r4fix`**:旧命令(`git diff --submodule=short`)在**任何**commit 类型下都恒空,R4-fix 换了新命令后测试用例只覆盖了单亲 commit 这一种子集,新盲区是本轮换命令时新产生的,不是延续旧盲区。

修法:`git show -m --submodule=short <ship-commit> -- aria`(单加 `-m` 即对两类 commit 都正确区分,已验证)。`git show --stat` 那一半(covering 5 个子模块文件+主仓 VERSION/badge)不受影响 —— 我验证过 `--stat` 对 merge commit 默认即显示 diffstat(与 patch 模式的抑制规则不同),问题**只在** `--submodule=short` 这一支。

## 3. 新发现 — 「残余风险有界」论证自身的事实错误 (Major, `introduced_by_r4fix: true`)

R4-fix 新增的「⛔ R4 明确不修项」框(现文 :382-392)给出三条不补 `SC-A-step (a)(b)` 内容序判据的理由,第 3 条(:388)逐字:

> 「不补的残余风险有界且已定位:风险 = B 折叠时改用无序列表 ⇒ (a)(b) 从『必红』退化为『无从求值』。它不会造成假绿(无从求值≠判PASS),**且 (c) 三禁一含、SC-A-doc、SC-A-note 三条不依赖编号**,hunk ① 的存在性仍被 B `:158` 接住。」

我复核 SC-A-step 表行(:786)对 (c) 的逐字定义:

> 「(c) 类级三禁一含 —— **『该步骤正文』= 自 `N` 的编号行起**,到下一个行首步骤编号行之前的全部文本(含缩进续行)」

**(c) 的作用域边界定义直接引用了 `N`——而 `N` 正是 (a) 定义的「满足 `2 < N < 2.5` 的编号」**。若 B 折叠时改用无序列表(:388 自己假设的风险场景),编号提取正则 `^[0-9]+(\.[0-9]+)?\.` 匹配不到任何行 ⇒ 不存在满足条件的 `N` ⇒ (a) 本身「无从求值」的同时,**(c) 定位「该步骤正文」起点所需的 `N` 也不存在** ⇒ (c) 同样从「必红」退化为「无从求值」,而不是像 :388 所说的那样「不依赖编号」而幸免。

这与 `SC-A-doc`(锚在 json 块的围栏行,与步骤编号无关)、`SC-A-note`(锚在 `**Output schema**`/`**配置参数**:` 标题,同样与步骤编号无关)是**不同性质的两类锚**——:388 把三者并列成"同样不依赖编号"是不成立的归类错误。

**这不改变「今天不补 (a)(b) 这条机械腿」这个最终决定的合理性**(理由 1「新增断言面」与理由 2「新步骤锚 token 未定」两条独立成立,我认可),**但它改变了这个决定所依据的风险敞口披露**:披露给 owner/Phase B 的是"只有 2/3 腿会失效",实际是"3/3 腿会同时失效"——`SC-A-step` 整条机械锚在折叠-改用无序列表这个已被自己点名的场景下会**整体**退化为无从求值,不是"仍有 (c) 兜底"。这与 Rule #10 要求的诚实披露有直接关系,因为它是本 Spec 自己发起的「不修」裁量的支撑论据之一。

**为什么是 `introduced_by_r4fix`**:整段「⛔ R4 明确不修项」框(含此句)是本轮新写文本,`ff847fb` 版本没有对应内容(已用 `git diff ff847fb 45c480a` 确认该框整体为新增 hunk)。

修法:删掉「且 (c) 三禁一含…不依赖编号」半句,或改为「(c) 与 (a)(b) 共用同一个 `N` 锚,同样会退化为无从求值;真正不依赖编号的只有 `SC-A-doc`/`SC-A-note` 两条独立机械锚,与本 hunk 无关」。不需要新造判据,是纯文字修正。

## 4. 未闭合的「fix-the-class」实例 (minor, `introduced_by_r4fix: false` —— 但本轮的「行锚 4 处」修复行动本应覆盖它而没有)

本轮按 brief 要求做了**全文件锚点重复扫描**(不只验局部),找到一处此前四轮、25 份席位报告都没提过的残留:

`B `:161`` 这个引用曾在两处被用来支持「B 的 D1 把步骤 1-5 整体折叠」这个论断:
- §残余暴露 R3 框(R3-fix 引入,原 :200)——**本轮已修**,现文(:244/:246)已正确改引 `B:154`(节标题)/`B:156`(`<details>` 标记)。
- **表1 `SC-M3c` 行**(R3-fix 同批引入,原 :262,今日 :311)——**未修**,现文仍逐字「B 的 D1 把步骤 1-5 整体折叠 (B `:161` 逐字)」。

实读 `B/proposal.md:161`:
```
🔴 折叠块之外必须留下 <MAIN_BRANCH> 的取值来源 (SC-M16 钉住)。实测 SKILL.md:242 是全文件唯一告知...
```
——讲的是 `<MAIN_BRANCH>` 取值来源说明,与「折叠步骤1-5」无关。真正陈述折叠的是 `B:154`(节标题「两处散文的 5 步移入折叠块」)与 `B:156`(`<details>` 标记本体)。

**这两处引用错误的措辞几乎完全相同(都是"B 的 D1 把步骤 1-5 整体折叠(B `:161` 逐字)"这句话的两份拷贝),是同一个错误在 R3-fix 同一提交里被写了两次;R4-fix 只改了其中一处**——恰是这份 Spec 反复用来批评自己(`§非目标:844`、`SC-A-note` 旧锚)的同一种"三处改了第四处没改"的模式,这次是"两处改了一处没改",且**四轮五席共 25 份报告都没有交叉核对过这两处引用是否一致**。

**how_it_goes_red**:复核者按 `:311` 的引用回源读 `B:161`,读到的是取值来源说明而非折叠声明,属 `reporter-miscite` 形状(与 tech-lead R4 finding7 同类,那 4 处已被判 minor 且"结论不受影响")。承重结论(B 的 D1 确实会折叠步骤1-5,这件事本身是真的,只是引用的行号错)不受影响,故沿用与该批同类缺陷一致的 minor 定级。

修法:`:311` 的 `B `:161`` 改为 `B `:154`/`:156``。

## 5. 对 brief 四个具体问题的直接回答

**(1) R4 的 12M 里它修的那几类真闭合了吗**:见 §1 表——10 条去重 Major 中 8 条完全真闭合、2 条(SC-A-step 不修的论证本身 + O-1 新命令)只闭合了一半,均是本轮新引入的半闭合(§2、§3)。

**(2) 引入率与预测准确性**:执笔方预测 R5 总数 14–20(点估17)、Critical 0、Major 5–8、引入率 70–85%。**仅从我本席看**:0 Critical(与预测一致),我独立发现 2 条 `introduced_by_r4fix=true` 的 Major(§2、§3)+ 1 条 pre-existing minor(§4,不计入引入率分子但计入 R5 findings 分母)。R4-fix 本轮改动触点(12 处)远小于 R3(约 25 处),且**本轮是四轮以来第一次没有发现任何"写下来但没做"的纯 paper-fix**——8/10 完全真闭合、其余 2 条也只是「新引入了一个不同的盲区」而非「谎称已修」。若这个模式在其余四席同样成立,R5 的**总量**很可能落在预测区间的**低端甚至略低于 14**(触点少 ⇒ 自生成条目少),但**引入率**(新条目占比)未必显著下降——因为我自己找到的 2 条 Major 恰好都是"这轮改了什么就在那个改动本身产生新缺陷"的形状,与前四轮同源。综合看:**总数预测方向大致准,引入率预测方向也大致准(仍然是自生成主导),但本轮自生成条目的"含金量"更高——不再是可读性/措辞错误,而是两条会实际误导 Phase B/D.2 执行的技术性缺陷**。

**(3) 自证点 `evaluate_path_coverage=3→1` 的自查过程算不算 finding**:**不算**。我独立复跑两个计数(`evaluate_path_coverage`=1,`resolve_ci_backend`=2 且套用"章节内首个匹配"后在 §C.2.4 内唯一)与执笔方自述完全一致——这段文字是诚实记录起草时的一次自我推翻,**不构成对任何 SC 红绿判据的新断言,也不改变代码或测试的任何可执行行为**,是纯粹的过程留痕。把它计为 finding 会把"如实自查"本身惩罚成"净增表面",这会激励未来的执笔方**不再做这类自查**(自查的产出=被扣分,不自查=没有对应扣分),是反向激励。**我判定:主动留痕自查 ≠ 应计 finding,除非自查记录本身包含事实错误(它不包含)。**这与 §3 的判定形成对照:§3 里我不是因为"它写了一段自我论证"而扣分,是因为**那段论证包含一个可独立验证为假的技术断言**((c) 不依赖编号)——判据是内容真伪,不是"是否新写了文字"。

**(4) 全文件锚点重复扫描**:除 §4 报告的 `B:161` 残留外,本轮新增的两处机械锚(SC-A-note 的"章节内首个匹配"限定、SC-A10c 的例外括注)以及既有的 SC-A-step 双锚(`**执行流程**:`/`**Subprocess 调用规范**:`)均已核实全文件唯一或已被正确限定作用域,无新的重复匹配盲区。

## sc_self_sufficiency 补充

18 条 `SC-A*` 本身覆盖完整、无恒红恒绿空真(与 R4 结论一致,本轮无新证据推翻)。**新发现的两条 Major 都不在 SC 层**——O-1 是「交付义务」(本 Spec 已声明其非 SC、无机械闸门),SC-A-step 论证瑕疵是 Spec 散文层面的风险披露问题,不改变任何一条 SC 的红绿判据本身。这与 R4 五席的模式一致:R4 的高严重度发现也集中在 SC 集合*之外*(delegate 失效、DEC §5.3、gitlink 命令、行锚)——18 条 SC 本身已经过 4 轮加固,趋于稳定;真正的剩余风险面已经从"SC 判据错不错"转移到"围绕 SC 的散文declaración(委派/披露/证据命令)站不站得住"。

## 结论

**verdict: PASS_WITH_WARNINGS**(0 Critical + 2 Major + 1 minor)。R4-fix 本轮修复质量是四轮以来最高的一轮(9/10 去重 Major 完全真闭合,首次零 paper-fix),但仍不收敛——本轮自己新增的文本(O-1 新命令、SC-A-step 不修论证)各自制造了一个新的技术性缺陷,印证了执笔方自己的预测(引入率仍将由自生成主导)。是否值得继续加轮不是本席职权判断的问题(regla #10 层面留给 owner/aggregate),但从实现可行性角度,本轮两条 Major 都**改法明确、成本低**(§2 加一个 `-m` 标志;§3 删/改一句话),不属于"结构性欠定"类,不需要新一轮大改。

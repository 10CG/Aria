---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-12T18:25:53.000Z
context: openspec/changes/premerge-gate-branch-existence/proposal.md
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R4 — Spec A `premerge-gate-branch-existence` — qa-engineer

**VOTE**: REVISE · **VERDICT**: PASS_WITH_WARNINGS (0C + 2M + 1m)

角度: SC 可证伪性 —— 18 条红窗是否真实存在 / 有无恒红恒绿空真 / 打桩边界自洽 / 三条负控早退是否真能拒绝坏实现。
方法: 对 R3-fix (commit `ff847fb`) 的每条承重声称本轮独立实跑复现 (不采信 R3-fix 自述或其他 R4 席位报告的转述,
交叉核对完成后才读了 `post_spec-R4-0-tech-lead.md` / `post_spec-R4-1-backend-architect.md`, 见 §3)。

---

## 0. 本轮实跑过的命令 (节选, 全部原文见下文各节)

```bash
git rev-parse HEAD                                                    # ff847fb (R3-fix)
for d in openspec/archive/*/; do [ -f "$d/detailed-tasks.yaml" ] && [ ! -f "$d/tasks.md" ] && echo "$d"; done  # 4 例
grep -c '^### Key Deliverables' openspec/changes/premerge-gate-branch-existence/proposal.md   # 0
grep -c '^| \*\*SC-M' openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md         # 20
grep -c '^| \*\*SC-A' openspec/changes/premerge-gate-branch-existence/proposal.md              # 18
ls .aria/audit-reports/ | grep mainbranch-failclosed | wc -l                                   # 55
ls .aria/audit-reports/ | grep mainbranch-failclosed | grep -vE 'aggregate|audit-trail' | wc -l # 45
# sys.settrace 动态复算 (自建脚本, 非转述)
python3 /tmp/trace_probe2.py   # tests run 46 / gate_check entries 24 / reached :356 = 19
                                # NOT reached call-site lines: [282, 301, 311, 321, 524]
grep -n '\*\*Output schema\*\*\|\*\*配置参数\*\*:' aria/skills/phase-c-integrator/SKILL.md
  # 264:**Output schema**:   281:**配置参数**:   501:**Output schema** (JSON):   523:**配置参数**:
grep -n '首个匹配\|首个\b' openspec/changes/premerge-gate-branch-existence/proposal.md   # 只命中 SC-A-step 行
```

---

## 1. R3 的 0C+14M+10m 是否真闭合 —— 从 QA 角度逐条回源

我逐条核对了 R3 五席全部 Major (tech-lead M-1~M-6/m-1/m-2 · backend-architect 的 SC-M18 缺口 ·
qa-engineer(我自己) QA-3-1/QA-3-2 · code-reviewer F-1~F-11 · knowledge-manager Major/minor),
本轮**独立复跑**(非采信 commit message):

| R3 finding | 我的独立复核 | 结论 |
|---|---|---|
| tech-lead M-1 (BLOCKER 假前提) | 独立复跑 4 例归档 + `grep -c '^### Key Deliverables'`=0, 确认「移入 `## Success Criteria`」使六项落入 `task-planner` 路径 B 文档化的三项解析范围之一 | ✅ **结构性真闭合**(KM 原 R3 finding「必然读到」的机制性质疑, 这次换到了一个真实在解析范围内的章节, 不再是自造前提) |
| tech-lead M-2 / code-reviewer F-4 (出路(i) 委派失效) | 独立重读 BLOCKER 现文, 确认已改为事实声明「O-1 今日没有任何机械兜底, 本 Spec 不假装它有」+ `D-b` 交 owner 裁 | ✅ 真闭合, 诚实降级 |
| tech-lead M-3 (`SC-A-step` (c-含) landmine) | 独立核对 (c-含) 现文只留 `#137` 一个 token, 标注对象改为「本步骤自身的作用域边界」——这句在 B 落地前后都为真 | ✅ (c-含) 本体真闭合。**但见 §2-Major-2**: 同一处修复留了一个孤儿引用未清 |
| tech-lead M-4 (`SC-M3c` 前提互斥 / `--pr-branch` 未入禁令) | 独立 `grep -c -- '--pr-branch' SKILL.md` = 0；确认禁令已升级为类级「不含任何以 `--` 起头的 CLI flag 字面量」 | ✅ 真闭合 |
| tech-lead M-5 / code-reviewer F-2 (`SC-A14` 腿2 在 pytest 默认捕获下假绿) | 独立跑 `s.encode('utf-8','strict')` 判据(不经 `sys.stdout`), 确认改动后与 harness 捕获模式结构上无关; baseline(未净化)确定必红, 净化后确定绿 | ✅ 真闭合, 我判**本轮质量最高的一处** |
| tech-lead M-6 (`_build_output` docstring 第四落点) | 独立 `python3 -c "import ast; ast.get_docstring(...)"` 确认 docstring 恰在 `:241-247`, 且 `各早退`/`分支(...)` 被源码换行拆开(`SC-A-note` 抹空白规则的必要性由此坐实); §Impact 与 `SC-A-note` (d) 腿均已要求同批更新 | ✅ 真闭合 |
| tech-lead m-2 / backend-architect Major / code-reviewer F-9 (`SC-M18` 操作数缩窄) | 独立跑四条 `grep -cE`, 得 `2/4/3/0`, 与表 1 现文逐字对上, 与 B `:364` 今日实测列一致 | ✅ 真闭合 |
| **我自己 QA-3-1 (兄弟位置表漏 7 条行为型 SC)** | 独立按 `grep -c '^| \*\*SC-M'`=20 逐一在表 1 中定位全部 20 个 ID(含两个合并行), 20/20 有归宿；另确认「方向1附加总体」新补 3 条任务级预写量, 逐条回源到 `tasks.md:85`/`:122`、`detailed-tasks.yaml:488` | ✅ 真闭合, 且我验证了三处新引文全部逐字对得上 |
| **我自己 QA-3-2 (`SC-A-step` (c) 正文边界欠定)** | 独立核对新定义「自 N 的编号行起, 到下一个行首步骤编号行之前的全部文本(含缩进续行)」——跨行拆分逃逸场景现被覆盖 | ✅ 真闭合 |
| code-reviewer F-1 (19/24, 非 20/24) | 独立写 `sys.settrace` 脚本重新动态测量(非采信执笔方的数字), 结果**逐字复现**: `tests run: 46 · dynamic gate_check calls: 24 · reached insertion point: 19`, `NOT reached: [282, 301, 311, 321, 524]`, 且确认 `:282` 正是 `test_case_f_outdated_binary_fails_fast` 的 precheck-失败早退 | ✅ **真闭合, 逐字节复现, 非「写下来」** |
| code-reviewer F-3 (`SC-A10c` 例外集错位) | 独立读 `ci_backends/base.py:79-85` 确认 `precheck()` 默认 `(True,"")`；`SC-A10c` 已移入适用集, 11+2+3+2=18 配平我逐条点过 | ✅ 真闭合 |
| code-reviewer F-5 (漏任务级预写量) | 同 QA-3-1 一并复核 | ✅ 真闭合 |
| code-reviewer F-6/F-7 (`SC-A-step`/`SC-A-note` 锚点欠定) | `SC-A-step` 独立确认「首个匹配」已写入, `[238,582]` 问题消除; `SC-A-note` 边界改为 json 围栏→配置参数 | ⚠️ **`SC-A-step` 真闭合。`SC-A-note` 只闭合了一半 —— 见 §2-Major-1(本轮新发现, 非上一轮任何 finding 的延续)** |
| code-reviewer F-8 (45 vs 55) | 独立复跑两条命令, 55 与 45 与 Spec 现文逐字一致 | ✅ 真闭合 |
| code-reviewer F-10 (仓外写动作口径矛盾) | 独立读 §Impact「外部」行与 `D-a`, 两处口径已统一 | ✅ 真闭合 |
| knowledge-manager Major (BLOCKER「必然读到」与 task-planner 解析范围矛盾) | 同 M-1, 六项已移入真实在解析范围内的 `## Success Criteria` | ✅ 结构性真闭合(路由目的地本身现在是对的) |
| knowledge-manager minor (`SC-M9` 未核销) | 独立确认表 1 `:268` 与表 2 `:308` 均已覆盖 `SC-M9`, 且互相交叉引用 | ✅ 真闭合 |

**QA 角度小结**: **14M 中的 12M+2m 真闭合**(含我自己 R3 报的两条); **`SC-A-step` 的欠定修复方式本身正确
且被我独立复现**, 但**同一份修复没有推广到它的兄弟锚 `SC-A-note`**(见下), 是本轮最重的发现 —— 而这正是这份
Spec 三轮以来反复被抓到的同一个病灶(memory `fix-the-class`: 认出了类只推广了一半), 这次复发在**修复本身
所在的同一个 commit 里**。

---

## 2. Findings

### Major-1 · 🔴 `SC-A-note` 的新锚点重犯了它隔壁 `SC-A-step` 刚刚被修好的同一个病: `Output schema` 在 `SKILL.md` 有两处

**Locator**: `proposal.md:704`(`SC-A-note` 行, R3-fix 新写的边界规则)× `aria/skills/phase-c-integrator/SKILL.md:264`(§C.2.4
内正确目标)× `SKILL.md:501`(§C.2.4.5 内的第二处, 结构相同的陷阱)。

**逐字**: `SC-A-note` 现文边界规则 ——「取 `SKILL.md` §C.2.4 中 **Output schema** 的 json 围栏结束行 (```) 之后、
`**配置参数**:` 之前的全部文本」。

**实测(本轮独立)**:

```
$ grep -n '\*\*Output schema\*\*\|\*\*配置参数\*\*:' aria/skills/phase-c-integrator/SKILL.md
264:**Output schema**:
281:**配置参数**:
501:**Output schema** (JSON):
523:**配置参数**:
```

`SKILL.md:501` 落在 `### C.2.4.5 Submodule Pointer Regression Gate (v1.28.0+)`(标题在 `:376`, 下一个 `###`
标题在 `:570`)内, **不是** `§C.2.4`(`:218`–`:305`)。它是**结构完全同形**的另一段:「`**Output schema**
(JSON):` → ` ```json ` 块 → ` ``` ` → `**配置参数**:`」, 描述的是子模块指针回归闸门的输出 schema
(`affected_submodules` / `telemetry_files` 等键), 与 A 要改的 §C.2.4「五类早退」枚举**毫无关系**。

**这正是 `SC-A-step` 在同一个 commit 里被修复的那个病 (F-6), 而修复没有推广到这里**: `SC-A-step` 的旧锚
`**执行流程**:` 在 `SKILL.md` 里也出现两次(`:238` 属 §C.2.4, `:582` 属 §C.2.5), 本轮 R3-fix 已把它显式钉死为
「取**首个**匹配」并在 SC-A-step 行内写明理由(「取末次匹配的实现得起点 582 > 终点 257 ⇒ 空/负区间 ⇒ 三腿与被测
实现无关地全红 = 恒红」)。**`SC-A-note` 的新边界规则(同一个 R3-fix commit 内新写)用了同一类文本锚
(`Output schema`), 同样在 `SKILL.md` 里出现两次, 却没有加同款的「首个匹配」限定**。我逐字核对全文件: `首个`
一词只出现在 `SC-A-step` 那一行, `SC-A-note` 行里完全没有(见 §0 的 grep)。

**它在什么实现下会红/会给出与实现无关的结果**: `SC-A-step` 的 bug 被发现的方式, 就是审计席位对
`**执行流程**:` 做了一次**不限定章节的全文件 grep**, 直接得到 `[238, 582]` 两个匹配。`SC-A-note` 的自然实现
方式完全同款 —— 用同一种手法搜 `Output schema`, 会得到 `[264, 501]` 两个匹配。若实现取**最后一次**匹配(与
`SC-A-step` 旧 bug 完全同一种错法), 就会从 `:501` 开始, 抓到 `:521`–`:523` 之间的文本(§C.2.4.5 的
`telemetry_files` 段), 在其上跑 (a)(b)(c)(d) 四腿断言:
- 那段文本**永远不含** `gate_error` / `main-branch` / `无 path_coverage`(它讲的是完全不同的领域), 也**永远
  是**「四项枚举, 不含 main-branch」的负控形态(它自己就是另一个 schema 的稳定文本, 与 A 有没有正确实现完全
  无关)。
- 结果: (a) **恒绿**、(b)(c) **恒红**(不随 A 的实现是否正确而改变) —— 这正是这个 SC 组自己在别处援引的
  memory `feedback_false_green_dual_is_permanent_red`: **一个信号如果不随被测对象变化, 无论它现在是红是
  绿都是零信息量**。也就是说, `SC-A-note` 若被这样实现, 会**完全脱钩**于 A 在 `SKILL.md:279` 真正做的编辑,
  变成一个测「另一份文档」的假信号。

**为什么这不是我在过度苛求**: 这不是我凭空设想的实现方式 —— 这就是**本轮已经真实发生过一次的失败模式**
(`SC-A-step` 的旧锚点), 而 `SC-A-note` 的新边界规则是在**修复那次失败的同一个 commit 里**新写的, 用的是同
一类"搜索一个在全文件里重复出现的短语"的做法, 却没有把刚学到的教训用到自己身上。

**与本轮另一位席位报告的分歧**: `post_spec-R4-1-backend-architect.md` 把 F-7(`SC-A-note` 边界欠定)判为「均真
闭合」, 理由是「独立 grep 确认新锚(json fence `:277` → 枚举归层注记 `:279` → 配置参数 `:281`)是稳定标题/
围栏锚, 不因段落如何分段而漂移」——**这个复核只在局部区间 `:277`–`:281` 内验证了锚点的相对稳定性, 没有像
`SC-A-step` 那样做一次全文件扫描去确认锚点文本(`Output schema`)在别处是否重复出现**。我认为这是一处**未被
同一轮的另一位席位发现**的真实缺口, 不是我与该席位的表面分歧。

**修法(供 A.2/Phase B 参考, 一句话即可)**: 与 `SC-A-step` 同款, 补一句「取 §C.2.4 内 `Output schema` 的**首
个**匹配(今日 `:264`)」, 或更稳妥地先限定到 `### C.2.4` 标题与下一个 `### ` 标题之间的区块再搜索。

**severity**: Major(与 `SC-A-step` 旧 bug 同一严重度量级 —— 都是「机械锚点在指定实现方式下可能与被测代码
完全脱钩」)。`blocks_phase_b`: 是 —— `SC-A-note` 是 Rule #6 第二行三处机械锚之一, 它的可靠性直接关系到
「指令流程变动 ⇒ 照跑 AB」这个定档的承重证据。

`introduced_by_r3fix`: **true** —— `SC-A-note` 的这条边界规则(json 围栏→配置参数)是 R3-fix 本轮为修复
上一轮 F-7(「段」无机械定义)新写的, R2-fix 版本用的是完全不同的定义(「含逐字 `各早退分支` 的那段」)。

---

### Major-2 · §非目标 `:844` 仍逐字保留 R3 已明确作废的那条 landmine 标注要求, 与 `SC-A-step` (c-含)/§Impact/§残余暴露 三处新口径矛盾

**Locator**: `proposal.md:844`(§非目标, 第二条 bullet 的第二句)× `:195-212`(§残余暴露的 R3 框, 改标注对象为
「本步骤自身的作用域边界」)× `:306`(`SC-A-step` (c-含) 行, 机械腿只留 `#137`)× `:896`(§Impact hunk① 的同款
更正)。

**逐字**: `:844` ——「由此产生的「新步骤用 `<MAIN_BRANCH>` 而步骤 3 硬编码 `main`」这条不一致, 按 §残余暴露在
**该步骤处逐字标注**」。

**这句话描述的正是 R3 自己判为 landmine 并明确废弃的旧要求**: `:199` 逐字「被标注的那条不一致(「步骤 3 仍
硬编码 `main`」)是一个**会被 B 的 D1 修好的瞬时事实**……(c-含)删去 `步骤 3` 这个 token」; `:896`(§Impact)
把同一处更正为「在该步骤处**标注本步自身的作用域边界**并指向 `#137`」; `SC-A-step` 的机械判据(`:306` 行)现文
也只留 `#137` 一个 token。**唯独 §非目标 `:844` 这一句没有跟着改**, 仍然照抄着「标注新步骤与步骤 3 硬编码
`main` 的不一致」这个已被 R3 自己证明「两条路都坏」的旧要求。

**它怎么会造成实害**: 若 Phase B 的实现者按字面顺序先读到 §非目标(在 §Rule #6 之后、§Impact 之前), 会依据
`:844` 的措辞写出「新步骤处逐字标注它与步骤 3 硬编码 `main` 的不一致」——这恰好触发 R3 自己论证过的两难:
B 落地前, `SC-A-step` (c-含) 现文只检查 `#137` 存在, 这类标注仍会**通过**(因为它同时也提了 `#137`), 但它
写的内容本身与 §残余暴露 R3 框的诚实边界声明**矛盾**(「一句在 B 落地前后都为真的作用域边界声明」变成了
「一句会被 B 落地证伪的瞬时事实断言」), 违反规则 #3(文档与代码/彼此必须同步), 且是 `:844` 自己的姊妹段落
`:199`-`:212` 已经详细论证过的确切失效模式 —— **本轮的三处更正(`:212`/`:306`/`:896`)只覆盖了三个落点, 第四
个落点(`:844`, 同一句话在 §非目标 里的第二份拷贝)被漏掉了**。

**这正是 `SC-A-note` (d) 腿此前抓到的同一类问题的镜像**(`SC-A-note` (d) 腿存在的理由就是「一句话在文档里有
第二份拷贝, 只改了一份」) —— 这次是 Spec 自己的 prose 犯了它自己刚学会防范的错。

**severity**: Major。`blocks_phase_b`: 是 —— 它是一条会误导 Phase B 实现者写出违反规则 #3 的具体错误文案
的活跃指令, 不是纯粹的审计元文本瑕疵。

`introduced_by_r3fix`: **true** —— `:844` 这句话本身是 R1-fix 时期就有的旧文案, 但它与 R3-fix **新引入**的
`SC-A-step`(c-含)/§残余暴露改判之间的矛盾, 是本轮才产生的(R2-fix 版本里 `SC-A-step` (c-含) 与 §非目标的
措辞是**一致的**, 都要求标注步骤3不一致; R3-fix 只改了三处, 使原本一致的四处出现分裂)。我判**由 R3-fix
引入**(矛盾本身是本轮的产物, 不是延续上一轮就有的缺陷)。

---

### Minor-1 · `SC-A-step` (c) 的 `--` flag 禁令未像 `SC-A-doc` 那样钉死匹配模式(行首锚定 vs 全块子串搜索)

**Locator**: `proposal.md:703`(`SC-A-step` (c) 行)× `:708-720`(`SC-A-doc` 下方两条解析规则, 对比参照)。

`SC-A-step` (c) 逐字「该正文 ⛔ **不含任何以 `--` 起头的 CLI flag 字面量**」。这条禁令的例证违规场景(M-4 finding
援引的那句)是**嵌在括注里的一句话**——「(对应 CLI 的 `--remote` / `--pr-branch` 同批传入)」, `--pr-branch`
出现在句子中间, 不在行首。若匹配实现采用类似 `SC-A-doc` 那样的「行首锚定」正则(`^  "..."` 那种风格), 这句违规
文本会被**误判合规**, 因为 `--pr-branch` 前面不是行首而是空格加汉字。

**为什么不是 Major**: 从上下文与「不含任何」这个措辞的自然读法看,「以 -- 起头的 CLI flag 字面量」更合理的读法
是「**该 token 自身**以 `--` 起头」(整段文本内子串搜索, 不要求位于行首), 这个读法下 M-4 的违规例证会被正确
捕获 —— 我倾向认为这是**唯一合理**的读法(与「不含 `aether ci status`」这类无行首要求的兄弟条款读法一致)。
但 `SC-A-doc` 已经用「不写死解析规则,『实际解析』这四个字就是欠定」的先例证明过: 这类判断留给"自然读法"
本身就是 Spec 反复吃过亏的地方。给 `SC-A-step` (c) 明确补一句「子串匹配, 不要求 flag 出现在行首」可一次性
排除歧义, 成本极低。

`introduced_by_r3fix`: **true**(「任何以 `--` 起头」这个类级表述是本轮新升级的; R2-fix 版本是点名
`--main-branch` 单一字面量, 不存在这个匹配模式问题, 因为点名字符串直接子串搜索没有歧义)。

---

## 3. 复核执笔方自己预判的三处(任务书问题 3)

| # | 预判 | 我的判断 |
|---|---|---|
| ① `SC-A-step (a)(b)` 明确拒绝断言(「A 此侧无法断言, 且不为它编造断言」) | **本轮读到 tech-lead 的 F-6 后交叉核对, 我同意其方向**: 承重的**顺序不变量**(内容序: `resolve_ci_backend` 引用 < 新步骤锚 < `evaluate_path_coverage` 引用)在 B 折叠后大概率仍然成立(B `:158` 只要求"补上"分支存在性核验步, 没有要求打乱步骤间的相对顺序), 这与纯数字位置判据(`2 < N < 2.5`)不是同一件事。「A 此侧无法断言」这句**对纯数字判据成立, 对内容序判据不成立**——是"修错了(部分)", 不是"本就只能诚实标注、无法机械化"。但这条我不重复展开为独立 finding(tech-lead F-6 已充分论证), 仅在此确认交叉复核结论一致。 |
| ② §交付义务「完成判据」是人工判据(贴 `git show --stat`) | **不是缺陷**。本小节明文自称「非 SC」且「不入 SC 计数」, 未混入我审的 18 条 `SC-A*` 承诺集合。O-1 断言的是"未来某次发布提交里 gitlink 是否被 bump", 这是**发布时点的仓状态**, 结构上不可能被随 A 一起合并的单测覆盖到(该事件发生在 A merge 之后)。执笔方已把"要不要为它新建一个机械闸"正确上呈为 `D-b` 交 owner 裁, 没有假装自己有一个不存在的机械量。这与 memory `false_green_dual_is_permanent_red` 一致: 硬造一个量只会製造恒绿或恒红, 现在的诚实标注是正确处置。 |
| ③ `SC-A-note` (d) 腿的 token 与语言绑定「已收口」 | **(d) 腿本体确认真闭合**(我独立 `ast.get_docstring` 复现, docstring 今日为中文且 `各早退`/`分支(…)` 被源码换行拆开, 抹空白规则确实必要非修辞)。**但 (d) 腿所在的整条 `SC-A-note` 的(a)(b)(c) 三腿的边界锚本身有独立于 (d) 的新缺陷 —— 见 §2 Major-1**, 两者互不影响, 但请勿把 (d) 的"闭合"误读为 `SC-A-note` 整条闭合。 |

---

## 4. 双向清点表(表1/表2)复核(任务书问题 4)

- **表 1(A→B)**: 独立按 `grep -c '^| \*\*SC-M'` = 20 逐一在表 1 中定位, **20/20 全部有归宿**(含两个合并行
  `SC-M4/M5` 与 `SC-M6·M7·M8·M11·M13·M14`), 无遗漏。「方向1附加总体」新补 3 条任务级预写量逐条回源到
  `tasks.md:85`/`:122`、`detailed-tasks.yaml:488` 均逐字对上。**未发现仍数漏的行**。
- **表 2(B→A)**: 独立按 `grep -c '^| \*\*SC-A'` = 18 展开表 2 的 10 个物理行(`SC-A-step` 拆 3 子行,
  `SC-A10`/`A10b`/`A10c` 合并 1 行, `SC-A6·A13·A-zero·A7·A8·A11·A14·A-order·A-cwd` 合并 1 行), 得 18 个唯一
  ID, 与 SC 表行数一一对应, 无遗漏无重复。`SC-M9` 反方向对 A 的影响(要求所有新 fixture 显式传 `main_branch`)
  已正确落地并与表 1 交叉引用。
- **执笔方拒绝 tech-lead 二元框架("换标注什么"这第三条路)**: 我认为**这条路本身成立**(见 §1 M-3 行的判定,
  B 落地前后都为真的作用域边界声明确实是一个比"留着/删掉"更好的第三选项), **但它只被走到了 3 个落点, 第 4
  个落点(`:844`)被漏掉** —— 见 §2 Major-2。这不否定"第三条路"这个方法论本身, 只是说明它的**推广没有做完**。

---

## 5. 常规 SC 落地复核(抽样重跑, 非引用)

- `SC-A14` 腿 2 新判据: 独立跑 `s.encode('utf-8','strict')` 对未净化字符串 → `UnicodeEncodeError`(baseline
  必红); 对净化后字符串 → 通过。与 `sys.stdout` 完全无关, 四种 harness 下同判。
- `SC-A10c` 例外集修正: 独立读 `ci_backends/base.py:79-85` 确认 `precheck()` 默认 `(True, "")`; 唯一让它返
  `(False, …)` 的路径是显式 mock, 与仓内现成先例 `test_case_f_outdated_binary_fails_fast`(`:272-286`)一致。
- §6 「19/24 触达 + 5 处不触达」: 用独立编写的 `sys.settrace` 脚本重新measure(见 §0), **逐字复现**
  Spec 声称的数字与具体行号集合, 非采信执笔方转述。
- 未发现新的、与本报告 §2 之外的恒红/恒绿/空真 SC。打桩边界表 11+2+3+2(可达前提)与 6+1+2+4+3+2(打桩边界)
  两套分区各自复核仍配平 18, 互不冲突。

---

## 6. 结论与投票

- R3 的 0C+14M+10m: **QA 角度逐条独立回源, 绝大多数真闭合**(含我自己 R3 报的两条), 且多条(F-1 的 19/24
  数字、`SC-A14` 腿 2 的净化机制)是我用独立脚本重新计算/复现的, 非采信自述;
- 但发现 **2 条 Major**: (1) `SC-A-note` 新边界规则在**同一个修复 F-6 的 commit 里**重犯了 F-6 刚修好的
  「文本锚在全文件重复出现」问题, 且是本轮**唯一一个**、**其他两位已交报告的 R4 席位都未发现**的缺口;
  (2) §非目标 `:844` 仍保留 R3 已作废的旧标注要求, 与 `SC-A-step`(c-含)/§Impact/§残余暴露 三处新口径矛盾;
- **1 条 Minor**: `SC-A-step` (c) 的 `--` flag 禁令匹配模式(行首锚定 vs 子串)未像 `SC-A-doc` 那样钉死;
- 执笔方自己预判的三处: ①"部分修错"(纯数字判据确实无法断言, 但内容序判据可以)、②非缺陷(诚实标注,
  非 SC, 不该被逼出机械量)、③(d) 腿本体真闭合但不代表整条 `SC-A-note` 闭合;
- 双向清点表(表1/表2)本身**无遗漏**, 20/20 与 18/18 全部有归宿。

`0 Critical + 2 Major + 1 minor` ⇒ **verdict = PASS_WITH_WARNINGS**。`vote = REVISE`(相对 R3-fix)——
虽然本轮质量显著高于历史三轮(核心机制修复真实、可独立复现, 不是 paper-fix), 但仍有 1 条 blocks_phase_b
级别的新缺口(`SC-A-note` 锚点脱钩风险)未被本轮任何已交报告的席位发现, 按本 session 既有纪律不应因"这是
max_rounds 最后一轮"而降格标注。是否据此加轮 / 由 owner 直接裁定收敛, 交汇总席与 owner 判定, 单席无权
(`converged: null`)。

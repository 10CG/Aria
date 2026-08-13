---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-13T11:20:00Z
context: openspec/changes/premerge-gate-branch-existence/proposal.md
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R5 — knowledge-manager 独立报告 (Spec A `premerge-gate-branch-existence`)

**VOTE: REVISE** · **VERDICT: PASS_WITH_WARNINGS** · **0C + 3M + 2m = 5** · `introduced_by_r4fix` = **4/5 = 80%**

审视角度: Rule #5/#6/#9/#10 合规 / Level 2 判据 / 非目标与 B 侧划界一致 / follow-up 可证伪。

方法论声明: 本轮全部数字均独立实跑命令或实读源文件得出 (命令原文见各条 `evidence`), 不采信 R4-fix commit message
的自述。对 R4-fix 声称"已闭合"的条目做了抽样回源复核 (非逐条), 抽样覆盖 §Level 判据 / DEC §5.3 执行 / §非目标
landmine 第四份拷贝 / SC-A10c 例外 / 自查留痕段的两个数字。对任务书第 4 问 (全文件重复锚扫描) 做了完整扫描,
不止验局部区间。

---

## 0. R4 的 12M 是否真闭合 — 抽样回源复核

| R4 Major (择要) | 我的独立验证 (命令/文件) | 结论 |
|---|---|---|
| Level (b) 跨模块腿逐条对四条件 OR 列表 | `sed -n '150,163p' aria/skills/spec-drafter/LEVEL_GUIDE.md` 实读 :156-162 四条件逐字与 A `:14-22` 引文一致; `sed -n '26p;29p'` 确认 R4 更正的两个行锚 (:26=LEVEL1 行, :29=Q2 行) 均命中 | ✅ 真闭合 |
| `standards/openspec/project.md` 行锚更正 :116→:117 | `sed -n '116,117p' standards/openspec/project.md` 确认 :116=Level 1 行, :117=Level 2 行, 与 A 引文逐字一致 | ✅ 真闭合 |
| 「移入 SC 章节 ⇒ 必然出六条 TASK」delegate 失效已改判 | `sed -n '55,68p' aria/skills/task-planner/SKILL.md` + `sed -n '85,95p' DUAL_LAYER_SPEC.md` 逐字确认: `## Success Criteria` 的路径 B 用途 = "验收标准" 落 `verification:` 字段, 非 TASK 本体; `grep -rn 'Success Criteria' task-planner/` = 2 命中, 全 skill 无一句把 SC 转成 TASK | ✅ 真闭合 |
| DEC-20260812-001 §5.3 (B 侧 6 条任务须留 cancelled 痕迹) 已执行 | 独立 `grep -c 'status: cancelled\|status: pending'` + 逐条核对 id: `TASK-003/004/005/007/008/009` = cancelled (6), `TASK-006` = pending (正确, 从未过户), 共 21 条一条未删; notes 含 `⛔ CANCELLED (2026-08-12, DEC-20260812-001 §5.3)` 字样 | ✅ 真闭合 (数字与 A 文 `:867-875` 逐字节相等) |
| §非目标 landmine 第四份拷贝已改 | `grep -n '步骤 3'` proposal.md 全文, 剩余命中均为 (a) §残余暴露的事实陈述 (b) "上一版逐字"引用旧文本作对照 (c) 明确的禁止性声明, **无一处仍要求写「步骤 3 硬编码 main」这句会过期的标注** | ✅ 真闭合 |
| SC-A10c 例外括注 (precheck 必须返 `(False,…)`) 已补回 | `sed -n '75,86p' aria/skills/phase-c-integrator/scripts/ci_backends/base.py` 确认默认 `precheck()` docstring 逐字 "Default: always (True, \"\")"，与 A `:718-725` 的例外声明及既有先例 `test_pre_merge_gate.py:272` 引用一致 | ✅ 真闭合 |
| 自查留痕段两个数字 (`evaluate_path_coverage`=1, `resolve_ci_backend`=2) | `grep -c 'evaluate_path_coverage\|resolve_ci_backend' aria/skills/phase-c-integrator/SKILL.md` = **1 / 2**，与 A `:380-385` 逐字一致 | ✅ 真闭合 (且是我独立复现，非采信) |

**抽样结论**: 我核到的 7 类 R4 Major 全部真闭合 — 闭合到"它要判的对象那一层"，非仅"写下来那一层"。
但**全文件重复锚扫描** (任务书第 4 问，见 §1) 挖出了 R4 声称已闭合的"同款病"类别里**未被扫到的一个兄弟实例**
(SC-A-doc)，说明"闭合"本身仍有遗漏——闭合的是"我认出的那几个实例"，不是"整个类"。

---

## 1. Major — SC-A-doc 的 JSON 块定位锚未被纳入 R4 刚为 SC-A-note 写的"章节内首个匹配"规则

**locator**: `openspec/changes/premerge-gate-branch-existence/proposal.md:785`（SC-A-doc 行）对照 `:787`（SC-A-note 行的 R4 新增限定）

**实测** (全文件重复锚扫描，任务书第 4 问):
```
grep -n '\*\*Output schema\*\*\|\*\*配置参数\*\*:' aria/skills/phase-c-integrator/SKILL.md
→ 264:**Output schema**:  · 281:**配置参数**:  · 501:**Output schema** (JSON):  · 523:**配置参数**:
grep -n -F '**配置参数**:' aria/skills/phase-c-integrator/SKILL.md
→ 281 与 523 逐字节相同（无任何文本区分两个"配置参数"标题）
```
SC-A-note 的 R4-fix 新增文本逐字："**两个锚一律取 `### C.2.4` 标题行 (今日 `:218`) 之后、下一个 `###` 标题行
(今日 `:306`) 之前的首个匹配**" ——并显式声明 "⚠️ `SC-A-step` 的起点/终点锚同受本条约束"，**点名延伸到了 SC-A-step，
唯独没有点名 SC-A-doc**。而 SC-A-doc 自己的操作数定义 (`:785`) 逐字只是 "从 `SKILL.md` §C.2.4 Output schema
json 块 (`:265-277`) **实际解析**"——一句今日行号的陈述，不含任何边界定位算法，也未交叉引用 SC-A-note 新写的规则。

**怎么会红**: 若两个独立实现者按 SC-A-doc 的字面描述各自写测试去定位"Output schema json 块"：
一个用精确字面 `**Output schema**:`（含尾随冒号，恰好唯一命中 264，安全）；另一个用宽松匹配（如
`re.search(r'\*\*Output schema\*\*', text)` 后取*最后一次*匹配，与 R2/R3 时 `SC-A-step` 曾经踩过的"取末次匹配"
同款坑）会定位到 `:501` 那个属于 `### C.2.4.5 Submodule Pointer Regression Gate` 的 JSON 块——其顶层键为
`verdict`/`affected_submodules`/`telemetry_files`，与 `_build_output` 的 7 键**结构上无一重叠**，SC-A-doc 会对**任何**
实现（无论 A 的代码写得多正确）恒红，与被测实现完全脱钩——这正是 SC-A-note 那条新规则自己描述的失效形态
("(a) 恒绿、(b)(c) 恒红，与真实编辑是否正确完全脱钩")在其亲兄弟 SC 上的重演。

**为什么这不是吹毛求疵**: 本 Spec 反复以 memory `fix-the-class`（"认出了类只推广了一半"）自我诊断（`SC-A-order`/
`SC-A-note`/§非目标 landmine 均是同一诊断的实例），R4-fix 自己也在 commit message 里写"六个落点全扫"作为方法论
承诺。这条恰恰证明：**同一个 commit 里，一次"扫描"仍然可能只扫到点名的那个实例，扫不到share 同一锚点的邻居** ——
连"已诊断过这个病"的作者本人也会在同一轮漏掉同一病的下一个实例。

**severity**: Major（spec-underdetermination，非今日 baseline-failing——今日精确字面匹配恰好安全，但该安全性
从未被本 Spec 写死，纯属两个锚点文本今日恰好有一个可辨别后缀）。`blocks_phase_b`: 建议是（与 SC-A-note 同类问题，
后者已被 R4 判 blocks_phase_b）。

---

## 2. Major — `CLAUDE.md:113`（Rule #8 SOT）因 A 新增第三条阻断腿而失实，且该同步义务在 A/B 拆分后无人认领

**locator**: `CLAUDE.md:113` · A `proposal.md:174`（全文唯一提及 Rule #8 处）· A `proposal.md:990-1017`（§Impact 表，无
CLAUDE.md 行）· B `detailed-tasks.yaml:448-467`（TASK-016）

**实测**:
```
sed -n '113p' CLAUDE.md
→ "8. PR merge 前必跑 pre-merge gate — phase-c-integrator C.2.4 验证 (a) 本 PR CI passing;
    (b) main 无 in-flight CI run; ..." （只两条腿）
grep -cE '分支存在性|main-branch-not-found' CLAUDE.md → 0
grep -n 'Rule #8\|规则 #8' A/proposal.md → 仅 :174（描述"恒真"这个症状，非承诺同步 CLAUDE.md）
```
A §2（What Changes）新增的分支存在性核验会让 `verdict=fail` + `gate_error.kind="main-branch-not-found"`
成为 pre-merge gate 的**第三条**会阻断合并的腿——`CLAUDE.md:113` 今日只描述两条。A 全文的 §Impact 表（发版同步面
唯一 SOT）没有 `CLAUDE.md` 这一行，§非目标清单也没有把它显式排除；`## Success Criteria` §交付义务的 O-1/O-2/O-3
六项里同样没有这一条。**A 既未认领，也未排除。**

再查 B 侧：`detailed-tasks.yaml` 中唯一处理此事的任务是 `TASK-016`（标题逐字"CLAUDE.md 规则 #8 同步 — 新增第三条
阻断腿"，**`agent: knowledge-manager`**——正是我本席的角色分工），status = `pending`，`dependencies: [TASK-008]`。
但 `TASK-008`（`_verify_branch_exists()` 实现，即分支存在性核验本体）正是本轮 DEC §5.3 已确认迁往 A、在 B 侧标记
`cancelled` 的六条之一。**TASK-016 自身既没有跟着一起迁移到 A，也没有把 `dependencies` 改指向 A 的等价交付物**——
它现在依赖一个 B 侧已声明"不得再实现"的 cancelled 任务。

**怎么会红**: A 按 MINOR 独立 ship 当天，`CLAUDE.md:113` 与 gate 实际的三条阻断腿立即不一致，直接违反不可协商规则
#3（"文档与代码必须同步更新"）。任何严格照 A 的 §Impact 表 + §交付义务表落地的执行者都不会碰 `CLAUDE.md`——因为
表里根本不存在这一行；而 B 侧原本该做这件事的任务已因依赖链断裂而实质上无法被正常触发（其唯一前置条件已作废）。

**为什么落在 A 的范围内、不是"把 B 的 finding 搬过来"**: A 自己 `:209-211` 已经立过判据处理另一件同形的事
（发版同步面/Rule #6 AB）——"二者的触发点都是**本 change 自己的发版**……义务结构上无法转移"。这句话逐字同样适用于
这里：使 `CLAUDE.md:113` 陈旧的行为是 A 新增的核验逻辑，不是 B 的 D1（散文收敛）。A 自己写下的判据反过来证明了
这条义务应该落进 A，而 A 没有用自己的判据去扫一遍 CLAUDE.md 这一处。

**severity**: Major，`blocks_phase_b`。`introduced_by_r4fix`: **否**——这是自 DEC-20260812-001（2026-08-12）拆分
以来就存在的划界缺口，历经 A 侧 post_spec R1-R4（20 席次审计）与 B 侧四轮 post_planning 均未被指出，R5 全文件复核
才浮出。

---

## 3. Major — B 侧 `detailed-tasks.yaml` 因本轮标记 6 条 `cancelled` 而留下悬空依赖边，`TASK-016` 是其中一例

**locator**: `openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml`

**实测**:
```
grep -n "dependencies:" -A1 detailed-tasks.yaml | grep -B1 'TASK-00[345789]'
→ 多处任务的 dependencies 含 TASK-003/004/005/006/008/009，其中 TASK-003/004/005/008/009 五者本轮已标 cancelled
```
`TASK-016`（见上条）即是一例：`dependencies: [TASK-008]`，而 `TASK-008` 已 `cancelled`，`TASK-016` 自身却仍是
`pending`——依赖图上出现一条指向已废弃节点、且从未被处理的边。B 侧本轮的 DEC §5.3 执行只做了"给六条本体打
`cancelled` 标记 + notes 留痕"这一半，没有做"扫描并处理指向这六条的下游依赖边"这一半。A 的 R4-fix 文本
（`proposal.md:869-875`）称"⇒ 碰撞面**已在源头消除**，不再依赖 handoff 纪律"——但这句话只核销了"B 的实施者会不会
重新实现同一功能"这个碰撞（六条本体已 cancelled，确实不会），没有核销"依赖这六条的其他任务会不会因为空指针式的依赖
而卡死或被忽略"这个相邻但不同的问题。

**怎么会红**: B 侧实施者（或未来的 task-planner 重新解析）走到 `TASK-016` 时，其唯一前置条件已经是一个明确写着
"⛔ 不得再实现"的节点——既不能满足依赖（因为 TASK-008 不会被完成），也没有指示应该改依赖到 A 侧的哪个交付物，
`TASK-016` 因此进入一个既不能推进、又没有被正式取消的悬空状态。

**severity**: Major。`introduced_by_r4fix`: **是**（六条 `cancelled` 标记是 R4-fix 本轮新写入的动作，悬空边是该
动作的直接副产品；DEC §5.3 只要求"须留 cancelled 痕迹"，未要求处理下游依赖边，但落地时二者是同一个"迁移动作"该
一并做完的两半）。与上一条（CLAUDE.md 孤儿）共享同一个具体案例（`TASK-016`），但失效机制不同：上一条是"没人认领
这份工作"，这一条是"任务图结构本身在骗人——它看起来还在排期，实际上排期不可能兑现"。

---

## 4. Minor — 抬头版本自述"本版 = R3-fix"在 R4-fix 之后未更新，打破三轮以来的一贯做法

**locator**: `proposal.md:52`

**实测**:
```
git show ff847fb:openspec/changes/premerge-gate-branch-existence/proposal.md | grep -n '本版 = '
→ 37:📌 本版 = R3-fix (post_spec R3: 4 REVISE / 1 PASS, 0C+14M+10m; Critical 连续两轮归零)。
git show 45c480a:openspec/changes/premerge-gate-branch-existence/proposal.md | grep -n '本版 = '
→ 52:📌 本版 = R3-fix (post_spec R3: 4 REVISE / 1 PASS, 0C+14M+10m; Critical 连续两轮归零)。   ← 一字未变
git diff ff847fb 45c480a -- proposal.md → 138 insertions(+), 34 deletions(-)（R4-fix 是本轮实际生效的提交，内容改动巨大）
```
逐个历史提交核对（`0548317`→`e165df4`→`017eb54`→`ff847fb`）发现：这一行在 **前三轮每一轮都被同步更新**
（"本版 = R1-fix" → "本版 = R2-fix" → "本版 = R3-fix"，随附的统计数字也每轮同步）。**唯独 R4-fix 这一轮**，尽管
diff 里到处是"🔴 R4"标记、内容改动比前两轮都大（138 行插入），这一句头部自述连同其统计数字（`0C+14M+10m`，实为
R3 的旧数）都原样留在文档里，未反映 R4 的真实结果（`0C+12M+16m=28`）与 R4-fix 的核心策略转向（"触点 25→12，
明确不修 15 条"，这一策略转向完全没在头部体现）。

**怎么会红**（作为文档一致性问题的可证伪形式）: 任何只读这一段头部快速定位"这是第几轮 fix、上一轮什么状态"的
读者（包括未来的 R6 执笔方，如果还有 R6）会得到与实际情况不符的信息——以为自己在 R3-fix 基础上工作，统计数字
也是过时的。这正是本文件自己反复强调的"文档 SOT 必须与现实同步"（规则 #3）在文档**自身元信息**层面的实例。

**severity**: Minor（正文内容本身因为密集散布的"🔴 R4"标记基本不会被真正误导——只有专门信任这一段头部摘要、
不读正文的读者会中招；但这一行的存在意义正是"给不想读全文的读者一个准确摘要"，摘要失准就丧失了这个功能）。
`introduced_by_r4fix`: 是（这一轮打破了此前三轮的一贯纪律）。

---

## 5. 任务书问题 3 — "主动留痕自查"该不该计为 finding

`proposal.md:380-385` 记录了执笔方起草 `SC-A-step (a)(b)` 不修理由时，先写下"另两个锚也不唯一——
`evaluate_path_coverage` = 3"，随后实跑发现该数字是编造的、真值为 1，并当场删除了那半条理由。

**我的独立核验**: `grep -c 'evaluate_path_coverage' SKILL.md` = **1**，`grep -c 'resolve_ci_backend' SKILL.md` = **2**
（`:241` 落在 §C.2.4 内、`:319` 落在 §C.2.4.X 内，套用 SC-A-note 新规则后 §C.2.4 内确为唯一）——与自查段落
逐字节吻合，两个数字都独立复现且准确。

**回答**:「该不该计为 finding」我判**不该计为独立的正确性缺陷**——理由：(1) 它最终呈现给读者的操作性结论
（`evaluate_path_coverage=1，唯一`）经我独立验证是准确的，没有向下游传递错误信息；(2) 若把"诚实、且被证明准确
的自我纠错"计为扣分项，会制造反向激励——掩盖自查比公开自查更划算，这与本文件反复援引的 audit-trail 诚实标注
原则、以及 memory `critique-repeats-error` 本身的精神相悖；一个持续要求"如实标注"的文档，不该在"如实标注"这件
事本身上被倒打一耙。

但我**确实**从中拆出一条独立的、真实的、可证伪的 **minor** finding，角度不同——不是"内容错了"，而是"放错了地方"：
这段约 230 字的起草过程叙事（"我先写了 X，然后我推翻了 X"）被内联写进了 `SC-A-step` 这一行——本文件本身在头部
（`:59`）声明的原则是"处置逐条内联在各节，**不在本文件累积审计叙事**（memory `audit-trail-not-in-spec`）"。
这段文字虽然技术上"内联在相关小节"（满足字面），但其内容是纯粹的起草过程记录（不影响 `SC-A-step` 最终应该
断言什么），与`audit-trail-not-in-spec`原则想要防止的"append-only 审计叙事与收敛型交付面同居一文"在精神上是
同一件事的微缩版——`SC-A-step` 本已是"全表被返工最多的一条"，Phase B 实施者读它时只需要最终的三腿定义，不需要
重演起草者的心路历程。建议：收敛为一行结论 + 指向本轮 commit diff 的指针。`introduced_by_r4fix`: 是（本段文字
是 R4-fix 新写的）。

**这条本身对"是否该继续加轮"这件事的价值**：即使是一次完全正确、完全透明、完全被验证准确的自我纠错，也仍然
在交付面上净增了约 230 字不承载任何新验收要求的叙事文本——这为执笔方自己的"任何新写文本都是净增表面"假说提供
了一个更纯净的例证：这次连"写错了"都不成立（写对了），"表面增加"依然成立。

---

## 6. 引入率与预测准确性

执笔方预测（commit message）：总数 14–20（点估 17）、Critical 0、Major 5–8、引入率 70–85%。

**仅从我本席看**: 5 条（0C + 3M + 2m），`introduced_by_r4fix` = 4/5 = **80%**，落在预测区间内，且与我核对到的
backend-architect（0C+2M+1m=3，2/3=67%……注：backend-architect 报告注明其 1 条 minor 为 pre-existing、不计入
引入率分子，故其引入率口径与我略有不同）、tech-lead（0C+6M+4m=10，7/10=70%）两席的量级方向一致：**Critical 0
在四席（tech-lead/backend-architect/qa-engineer/我）间完全一致**，与预测吻合；**Major 数在单一席位内就已达到或
逼近预测给出的"全轮 5-8"上限**（tech-lead 一席 6 条、我一席 3 条）——若各席重叠度不高，去重后的总 Major 数
很可能突破预测上限的 8。**这与 R1→R4 的规律相反**：R1-R4 每一轮的"总数是否达标"主要由 minor 计数/措辞类条目
撑起，而这一轮（含我发现的 3 条 Major）呈现的是**实质性的技术缺陷**（划界孤儿 / 悬空依赖边 / spec-underdetermination
残留），不是可以归为"修辞性数字"的那一类——这印证了 backend-architect 报告里提到的判断："本轮自生成条目的
'含金量'更高"。

---

## 7. Rule 合规巡检 (无新增 finding，逐项记录已核范围)

- **Rule #5**（项目变更放主仓 `openspec/changes/`）: 合规，A 落点正确。
- **Rule #6**: §Rule #6 一节推理自洽，(a)(b)(c)(d) 四点依据逐条核对 SOT 引文均准确（`skill-benchmark-exemption.md:31/:33`
  的判据表未在本轮改动，未重新核对逐字，但 A 对它的援引方式与既往轮次一致，未发现新问题）。
- **Rule #9**（handoff 只能落 `docs/handoff/`）: 全文 "handoff" 出现的 6 处均指 "D.2 handoff"（十步循环 Phase D
  产物，非会话收尾），未出现 `.aria/handoff/` 字样，合规。
- **Rule #10**（enabled 闸门不得自行豁免）: BLOCKER 块的 D-a/D-b/D-c 三点均正确留给 owner 裁定，未见 AI 自行拍板
  的痕迹；D-c 本轮改判为"规则驱动题"并要求"先版本后 Level"的排序，逻辑自洽（Breaking=YES 时直接 Level 3，
  不需要再走 Level 判据），未发现违反。
- **Follow-up 可证伪**（F-1/F-2/F-3 归属表）: `grep -n 'follow-up' proposal.md` 全文 12 处命中，逐处按其自身声明
  的排除口径（不含表自身 3 处、不含明确的"归属见下"类交叉引用与计数方法论叙述 5 处）核销后剩 4 处文本 = 3 件事，
  与文档自称的"4 处文本承诺实为 3 件事"完全吻合——**这条自我审计经得起复核，非虚报**。

---

## 8. SC 集合自足性 (`sc_self_sufficiency`)

SC 表 18 条本身对"gate 行为面"的覆盖较扎实：`SC-A-step`/`SC-A-note` 已做过对抗性验证（1 好 + N 坏 fixture），
`SC-A10/A10b/A10c` 三条负控与三道早退一一对齐。但 SC 表**结构性地不覆盖 A 的全部承诺**：

1. **O-1/O-2/O-3/F-1/F-2/F-3 六项交付义务被明文排除在 SC 表外**（"不是可证伪的机械判据"），且逐项自陈"有机械
   闸门吗：没有"——这是诚实的（不假装有兜底），但意味着 SC 表本身不是 A 承诺的完整镜像；
2. **CLAUDE.md:113 同步义务连"被排除"都算不上**——它不在 O/F 六项里，也不在 §非目标里，是一个连"有记录、无机械
   闸门"这个最低承认门槛都没达到的盲区（见 §2）；这比"恒红/恒绿/空真"更基础——是一个从未被断言存在过的承诺；
3. **SC-A-doc 的定位算法本身仍是 spec-underdetermined**（见 §1），是 R4 判定"已消灭"的那一类缺陷在其亲兄弟位置
   上的活体实例。

结论：SC 集合**不**完备覆盖 A 的全部承诺；已覆盖的 gate 行为面质量较高，但"文档同步义务"这一类（CLAUDE.md +
SKILL.md 两处，后者已由 `SC-A-doc/step/note` 覆盖、前者完全空缺）暴露出 A 在自我审计范围划定上有系统性盲区——
凡是"由 A 的 ship 触发、但落点在 A 自己代码库以外的一份文件里"的同步义务，A 目前只覆盖了 `SKILL.md`，没有覆盖
`CLAUDE.md`。

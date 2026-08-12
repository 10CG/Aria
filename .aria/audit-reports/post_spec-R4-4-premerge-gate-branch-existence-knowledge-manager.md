---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-12T18:37:29.000Z
context: openspec/changes/premerge-gate-branch-existence/proposal.md
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R4 — Spec A `premerge-gate-branch-existence` — knowledge-manager 独立审计

## 结论先行

**0 Critical + 0 Major + 3 minor**。R3 的 0C+14M+10m = 24 条, 我逐条回源, **全部真闭合**
(非仅「写下来」)。R3-fix (`ff847fb`) 是本轮以来质量最高的一次修复: 三处结构性失效
(BLOCKER 假前提 / SC-A14 腿 2 假绿 / SC-A-step landmine) 均被正确定位并对症下药,
而非只换了个自洽的量。**本轮新引入的 3 处 minor 全部是文档精度问题, 不构成新的假绿/假红机制,
不 block Phase B。**

---

## 1. R3 的 14M 是否真闭合 (逐条回源, 区分「写下来」与「闭合」)

R3 五席合计 **0C + 14M + 10m = 24** (去重前; 去重后按 aggregate 口径), 我逐条核对 `ff847fb` diff
后的现状:

| # | R3 finding (来源席位) | 现状 | 判定 |
|---|---|---|---|
| M1 | BLOCKER 承载前提被 task-planner 证伪 (tech-lead + 我自己) | BLOCKER 全块重写, `task-planner/SKILL.md:59-67` 与 `DUAL_LAYER_SPEC.md:90-93` 我复跑逐字确认「ELSE → 路径 B → 仍出 `detailed-tasks.yaml`」「`## Success Criteria` 是三项穷举之一」; 4 例归档 Level 2 先例 (`for d in openspec/archive/*/; do [ -f $d/detailed-tasks.yaml ] && [ ! -f $d/tasks.md ] && echo $d; done` 我复跑得同 4 例, 逐个核 frontmatter 均 Level 2) | ✅ 真闭合 |
| M2 | O-1 出路 (i) 委派 §C.2.5 失效 (tech-lead + code-reviewer) | 出路 (i) 已整段作废, 明文「O-1 今日没有任何机械兜底」+ 上提 `D-b` | ✅ 真闭合 |
| M3 | SC-A-step (c-含) 是自我拒绝过的哨兵形态 (tech-lead) | 标注对象由「步骤 3 当下状态」改为「本步自身作用域边界」, 我核对该新句在 B 落地前后均为真 (陈述的是本步契约, 非他处缺陷状态) | ✅ 真闭合, 且这不是「换量」而是「换标注内容」, 见下 §4 |
| M4 | SC-M3c/SC-M15 前提互斥, 三禁不含 `--pr-branch` (tech-lead) | 三禁令升级为类级 (`⛔ 不得含任何以 -- 起头的 CLI flag 字面量`), 我复跑 `grep -c -- '--pr-branch' aria/skills/phase-c-integrator/SKILL.md` 逻辑上已被新禁令覆盖 (类级禁止, 非点名) | ✅ 真闭合 |
| M5 | SC-A14 腿 2 红机制建立在裸 python 的 `sys.stdout.errors=='strict'` 上, pytest 默认捕获下为 `replace`, 对坏实现假绿 (tech-lead + code-reviewer, 二席独立命中) | 腿 2 判据改为直接对 `gate_check()` 返回的 dict 值跑 `s.encode("utf-8","strict")`, 不再读 `sys.stdout` 一个字节, 结构上与 harness 捕获模式无关 | ✅ 真闭合 |
| M6 | `_build_output` docstring 是「四类早退」枚举的第四处落点, 三条 doc 侧 SC 全够不到 (tech-lead) | `SC-A-note` 新增 (d) 腿, 显式对 docstring (经 `ast.get_docstring`) 跑同款三问, 并钉死抹空白解析规则 (我核对 `pre_merge_gate.py:241-246` 今日文本确实被源码换行拆成「各早退」+「分支(…)」两段, 不抹空白锚点确实零命中) | ✅ 真闭合 |
| M7 | 「触达新核验的 20/24」实测 19/24, 漏了 precheck 失败一类 (code-reviewer) | §6 改用 `sys.settrace` 动态测量, 逐调用点判是否执行到插入点, 得 `19 处触达 + 5 处不触达`, 三类早退与三条负控 SC-A10/A10b/A10c 一一对齐 (`:282` 明确点名) | ✅ 真闭合 |
| M8 | SC-A10c 在「可达前提」例外集放错边, 干净 CI runner 上假绿 (code-reviewer) | 已移入适用集 (须显式 mock backend), 我复读 `ci_backends/base.py:79-85` 确认默认 `precheck()` 恰为 `(True, "")`, 与新处置一致 | ✅ 真闭合 |
| M9 | 兄弟位置清点漏了 `tasks.md`/`detailed-tasks.yaml` 里的任务级预写量 (code-reviewer) | 新增「方向 1 附加总体」表, 逐条核销 `tasks.md:85`/`:122`、`detailed-tasks.yaml:488` 三条 | ✅ 真闭合 |
| M10 | 兄弟位置清点遗漏 B 侧 7 条行为型 SC (SC-M6/7/8/10/11/13/14) (qa-engineer) | Table 1 现含合并行 `SC-M6·M7·M8·M11·M13·M14` + 独立行 `SC-M10`, 我核对总行数配平: 12 单行 + M4/M5 合并 + 6 条合并 = 20, 与 B 侧 SC-M 总数 (`grep -c '^| \*\*SC-M' B/proposal.md` 我复跑 = 20) 一致 | ✅ 真闭合 |
| M11 | SC-M18 只清点 1/4, 漏两个 A/B 都会编辑的文件 (backend-architect) | 现列四分量今日值 `2/4/3/0`, 与 B `:364` 逐一对上 | ✅ 真闭合 |
| m1 | Level 2 判据自造, SOT「跨模块」腿未逐字评估 (tech-lead) | 抬头改为逐字照 SOT Q2 三腿, (a)(b)(c) 逐条给出判断 | ✅ 真闭合 (但见下 §5 一处新引入的行锚误差) |
| m2/m4 | SC-M18 总体缩窄 (tech-lead / backend-architect dedup) | 同 M11 | ✅ 真闭合 |
| m3 | SC-A-step 起点锚未写「首个」, `**执行流程**:` 命中 `[238,582]` (code-reviewer) | 明文「取首个匹配 (今日 `:238`)」, 我复跑扫描确认 582 属 §C.2.5, 若取末次匹配区间为负 | ✅ 真闭合 |
| m5 | SC-A-note「段」边界无机械定义 (code-reviewer) | 改为 json 围栏结束行到 `**配置参数**:` 之间的稳定锚, 合规实现无论分几段都落在区块内 | ✅ 真闭合 |
| m6 | 「45」实际 `ls \| grep` 得 55 行 (code-reviewer) | 已用三项并列 (总体/范围/计数法) 收口, 45 只作修辞, 非机械判据输入 | ✅ 真闭合 |
| m7 | 仓外写动作授权口径矛盾 (code-reviewer) | 四件仓外写动作合并入 `D-a` 一次裁定, §Impact 外部行与 Follow-up 归属表口径统一 | ✅ 真闭合 |
| m8 | §版本 grep 列举不全 (code-reviewer) | 更正为逐一列举 7 行并注明性质 (定义 vs 调用 vs 提及) | ✅ 真闭合 |
| m9 | SC-A-step (c) 抽取边界未定义 (qa-engineer) | 明文「自 `N` 的编号行起, 到下一个行首步骤编号行之前的全部文本 (含缩进续行)」 | ✅ 真闭合 |
| m10 | SC-M9 未显式核销 (我自己, R3 knowledge-manager) | Table 1 新增 SC-M9 行, 标注「R3 补核销」+ 反方向影响移入表 2 `SC-A10/A10b/A10c` 行的「必须显式传 main_branch」新规则 | ✅ 真闭合 |

**结论**: 14M+10m 逐条回源, **无一条止步于「写下来」**——每条都能在当前文本里找到与 finding 精确对应的
机制性改动 (换判据/换标注对象/新增解析规则/补齐清单), 且我对其中数值类改动 (4 例归档 / 19-24 动态测量 /
SC-M18 四分量 / docstring 抹空白解析) 均独立复跑确认, 未发现"回填成看起来合规但实际仍绿/仍红"的情形。

## 2. 引入率论证 (74%→79%, 本轮不承诺归零)

执笔方给出的结构性理由 (本轮体量最大的两处新增 [双向清点表 2 / §交付义务] 都是对尚不存在文本
[B 的落地文本 / A.2 产出] 的断言) 站得住: 表 2 的 `SC-A-step (a)(b)` 行**恰恰**是这个结构性理由的
活证据——它是 18 条里唯一一条**如实标注「此侧无法断言」**而非编造断言的行, 说明执笔方没有为了
凑出「不会打爆」而在不该下结论处下结论。**我不把「不承诺接近零」本身算作扣分项**——本轮 max_rounds
已到最后一轮, 诚实标注不确定性优于制造虚假收敛感。

## 3. 复核执笔方自己预判的三处 (逐条回答: 修错了 / 还是本就只能诚实标注)

① **`SC-A-step (a)(b)` 明确拒绝断言**: **本就只能诚实标注, 无法机械化**。它要断言的是 B 尚未写出的
折叠落地文本的属性, 而 B `:156` 已成文承接「折叠块须补上本核验步」的重验义务——这不是无人认领的缺口,
是**正确的委派** (delegate-verify 意义上的委派对象真的会做这件事, 已核实)。若本侧强行钉一个「折叠后
应保留行首编号」的断言, 那才是钉合成 fixture (memory `gate_tracks_reality_synthetic_fixture` 的定义性
反例)。**这不是修错了。**

② **§交付义务的完成判据是人工判据 (贴 `git show --stat`)**: 对 O-1/O-2 而言**是诚实限制, 不是修错了**——
它明确声明「没有机械闸门」并指向 `D-b` 请 owner 裁, 与本 Spec 别处「不为它编造断言」的一贯纪律一致。
**但**我在 §5 发现一个执笔方没预判到的**相邻缺口**: O-3/F-1/F-2/F-3 的「完成判据」列同样写「见文首 `D-a`」,
而 `D-a` 只回答「是否获授权」, **不回答「做完了怎么证明」**——这与 O-1 那种"贴 diff 证据"的具体性不对称。
这条不在执笔方自报的三处之内, 我把它作为独立 minor 上报 (见 §5 finding 3)。

③ **`SC-A-note` (d) 腿的 token 与语言绑定**: **已收口, 不是修错了**——本 Spec 明文把「改写为英文」列入
非目标, 语言变更须与 `SKILL.md:279` 同批同措辞改, (d) 的 token 依赖是该约束的自然推论, 不是遗留缺陷。

## 4. 复核四条「不同意」与双向清点表

**tech-lead 二元框架的反驳 (第三条路: 换标注内容而非换标注对象)**: 我逐字核对新旧两句——
旧句陈述「步骤 3 当下硬编码 `main`」(关于**另一处**当下状态的断言, 会随 B 的 D1 落地而变为假);
新句陈述「本步只核验 `main_branch` 在 `<remote>` 上存在, 不保证后续步骤查询同一分支」(关于**本步自身
契约边界**的断言, 与步骤 3 是否已被 B 修好**无关**, B 落地前后均为真)。这确实是换了"标注什么"而非
用另一个同样会漂移的量自圆其说, **第三条路成立**。

**双向清点表 (表 1 = 20 行 · 表 2 = 18 行) 有没有仍数漏的**: 我独立重新枚举两表全部行 (含合并行拆分)——
表 1: 12 条独立行 + `SC-M4/M5` 合并 (2) + `SC-M6·M7·M8·M11·M13·M14` 合并 (6) = 20, 与
`grep -c '^| \*\*SC-M' B/proposal.md` 复跑值 20 相等, **无遗漏**。
表 2: `SC-A-doc`(1) + `SC-A-step`(1, 拆 3 行呈现) + `SC-A-note`(1) + `SC-A10/A10b/A10c`(3) + `SC-A-cli`(1) +
`SC-A-baseline`(1) + 9 条合并行 + `SC-A-sc22`(1) = 18, 与 SC 表总行数 (`grep -c '^| \*\*SC-A' A/proposal.md`
复跑值 18) 相等, **无遗漏**。两表均自洽、配平, 我未找到第三处对撞点。

## 5. 本轮 (R4) 独立发现的新增 minor — 均为 R3-fix 新引入的文档精度问题, 非结构性

1. **`LEVEL_GUIDE.md:26` 行锚错误 (应为 `:29`)**——`openspec/changes/premerge-gate-branch-existence/proposal.md:10`
   逐字引「SOT `spec-drafter/LEVEL_GUIDE.md:26` 的 Q2 三腿」, 我复跑 `grep -n 'Q2' aria/skills/spec-drafter/LEVEL_GUIDE.md`
   得 `29:│ └─ NO ──▶ Q2: 是否架构变更/跨模块/Breaking?│`; `:26` 处实际是 Q1 分支的 `LEVEL 1 (Skip)` 行,
   与 Q2 无关。**这是本轮 (BLOCKER 全块重写) 新引入的行锚, 非承袭旧误**。引用的文字内容本身准确,
   只是行号错位 3 行——不影响判断逻辑, 但与本 Spec 自己反复强调的「file:line 引用必须实读那一行」纪律
   (它在别处三次揪出别人同类错误: `:337`→`:335`、`git checkout HEAD`→需基线 SHA、`ls \| grep` 45 vs 55)
   矛盾, 建议下一次触及该段落时顺手订正。**不 block Phase B** (Level 判定的结论不依赖行号本身)。

2. **「D.2 handoff」一词混用了 `phase-d-closer` 的两个不同步骤**——本文件 10+ 处用「A 的 D.2 handoff」
   指代「把碰撞事实/issue 号写进交接」这件事 (`:109` `:267` `:277` `:283` `:779` `:863-865` `:874`),
   而我实读 `aria/skills/phase-d-closer/SKILL.md:41-43` 逐字: **D.2 = openspec-archive (Spec 归档,
   产出落 `openspec/archive/`)**, **D.3 = session-handoff (写 handoff 到 `docs/handoff/`, L5 hardcode)**——
   两者是**不同步骤, 写往不同目录**。"D.2 handoff" 字面矛盾 (D.2 步骤本身不产出 handoff)。
   实际执行时, 具备 phase-d-closer 完整加载的实现者大概率仍会正确落到 D.3/`docs/handoff/`
   (Rule #9 的 5 层 enforcement 之一是路径硬编码), 故**不构成 Rule #9 违反的高风险场景**, 但
   本 Spec 对自身之外的每一处引用都要求逐字精确, 这一处却全文重复使用了一个不存在于
   `phase-d-closer/SKILL.md` 里的复合概念。**这是 R3 新增 §交付义务 小节带入的, 而非 R1/R2 已有内容**
   (该小节整体是 R3 新结构)。建议下轮统一改为「D.3 (session-handoff)」或泛指「Phase D 收尾」。

3. **O-3/F-1/F-2/F-3 的「完成判据」列答非所问**——`### 交付义务` 表 (`:770-777`) 中 O-1/O-2 的
   「完成判据」列给出可核验的具体产物 (`git show --stat`/`git diff` 证据、`ab-results/` 落盘结果),
   而 O-3/F-1/F-2/F-3 四行的「完成判据」列**全部**填「见文首 `D-a`」——但 `D-a` 回答的是
   「是否获授权做这些」(一个前置闸门问题), 不是「做完了如何验证」。即便 owner 在 `D-a` 处授权放行,
   本 Spec 也未要求"把创建的 issue URL / 评论 URL 写回某处"作为完成证据, 与 O-1 的具体性不对称,
   与本 Spec 自己引用的 memory `feedback_falsifiable_evidence_for_binary_acceptance`
   ("Acceptance bool 必 mandate 可验 metric") 的精神有一处未覆盖到自己身上的死角。
   **不 block Phase B**——这四项本就系于 owner 尚未做出的授权决定, 影响面小于「授权后无法证明是否做过」
   这一具体缺口, 且执笔方在 §Rule #6 与 O-1 两处已展示出对该原则的正确理解, 此处更像是
   `### 交付义务` 小节整体作为 R3 全新结构、尚未来得及做第二遍"审自己"的遗留死角。

## r1_closure / sc_self_sufficiency (供本轮聚合)

**r1_closure**: 本任务书重点核 R3 的 14M (+10m), 已逐条回源, **全部真闭合**, 无一止步于"写下来"。
数值类改动 (4 归档例 / 19-24 动态触达 / SC-M18 四分量 / docstring 抹空白) 均独立复跑确认。
唯一遗留的是**新引入**的 3 处 minor (行锚 / 术语混用 / 完成判据不对称), 与 R3 所修的 24 条无关。

**sc_self_sufficiency**: SC 集合 (18 条) 与双向清点表 (20+18) 均自洽配平, 无恒真/恒绿/空真新增。
`### 交付义务` 六项 (O-1/O-2/O-3/F-1/F-2/F-3) **有意不入 SC 计数** (本 Spec 明确论证过——机械判据会
污染"每条 SC 都带今日实测值"这个性质), 这个设计选择本身合理; 但其中 4/6 项的"完成判据"列答非所问
(见 §5 finding 3), 是这套自我声明"诚实无机械闸门"的义务集合里, 唯一一处连"诚实声明的完成标准"
本身都不完整的地方。

## 本轮 R4 (max_rounds 最后一轮) 建议

三处新增均为 minor、不 block Phase B、不构成假绿/假红机制。若 owner 认可"Critical 连续三轮为零 +
Major 本轮首次归零 (14→0)"已达可接受的收敛信号, 我作为 knowledge-manager 席位投 **PASS_WITH_WARNINGS**,
不投 REVISE——三处 minor 建议记入 D.2/D.3 handoff (用正确的名字) 作为"下次触及本文件时顺手改"，
不构成拖入 R5 (max_rounds 已无余量) 的理由。

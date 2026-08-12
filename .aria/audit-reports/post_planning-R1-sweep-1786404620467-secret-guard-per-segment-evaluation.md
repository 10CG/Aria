---
checkpoint: post_planning
round: R1-sweep
round_kind: mechanical_gate
review_target: v10 (proposal.md + detailed-tasks.yaml)
spec: secret-guard-per-segment-evaluation
timestamp: 1786404620467
date: 2026-08-12
executed_by: backend-architect (v10 执笔席; 原 post_planning R1 五席之一, 本轮切换为执笔)
authorized_by: owner 2026-08-12 四条裁定 — 裁定 1「修完 3C + Major + 机械闸加第 5 轴, 不再开 post_planning R2」
sweep_a_checked: 24
sweep_a_fail: 0
sweep_b_checked: 21
sweep_b_fail: 0
sweep_c_checked: 4
sweep_c_fail: 0
sweep_d_checked: 98
sweep_d_fail: 0
sweep_d_reviewed_hits: 1
sweep_e_checked: 21
sweep_e_fail: 0
sweep_e_gap_found_pre_v10: 1
verify_a2: ALL-GREEN
nul_check: pass
regex_untouched: true
verdict: ALL-GREEN
ready_for_a3: owner 裁 (本表不自行宣布)
---

# post_planning R1 机械闸核对表 — secret-guard-per-segment-evaluation v10

> **性质**: 不是审计轮。这是 owner 2026-08-12 四条裁定里裁定 1 的落地 ——「修完 3C + Major +
> 机械闸加第 5 轴, 不再开 post_planning R2; 核对表全绿即进 A.3」。本表**取代** post_planning
> R2, 由 v10 执笔席对五条判据做穷举核对: (a)-(d) 复刻 R6 post_spec 机械闸的四条算法并对 v10
> 状态重跑 (本轮改了 proposal.md 的 F-1 表 / SC-6 / SC-14 / SC-16 / SC-18 / SC-21, 需要确认
> 改动没有破坏这四条既有判据); **(e) 是本轮新增**, 补上 R1 tech-lead 的元判断指出的缺口。
>
> **为什么要加判据 (e)**: R1 五席之一 (tech-lead) 复核 A.2 分解时指出 —— 此前累计 9 条判据
> (R6 post_spec 机械闸 4 条 + `verify_a2.py` 的 A.2 自检 5 条) **没有一条走「§What 设计条目
> → Task」这条轴**。于是 §What.1 第 4 行 (后台记号裸 `&` 降级判据) 在 v9 里保留在正文表格
> 内、也在转出 11 的驳回记录里被反复引用, 但**从未有任何 detailed task 承载它, 也从未有
> 专属的 SC-6 fixture 断言它** —— 而 9 条判据全部全绿, 因为它们检的都是「SC 有没有 Task」
> 「Task 编号对不对」「数字对不对」「fixture 会不会被块字符污染」, 没有一条会去反查
> 「§What 正文里的每一条规范, 有没有被下游 (Task + SC) 接住」。**判据 (e) 补的正是这条轴。**
>
> **复现**: `python3 /tmp/…/scratchpad/sweep_r1.py` (脚本随本报告归档到 spec 交付物之外,
> 属一次性核对工具; 五条判据的算法在下方逐条写明)。`verify_a2.py` 单独复跑, 结果见文末。

## 汇总

| 判据 | 检查对象数 | fail | 备注 |
|------|-----------|------|------|
| **(a)** 每条 SC 反查承载 Task (含 F-1 定义自洽性) | 24 (22 SC + 2 定义检查) | **0** | 复刻 R6 算法, 对 v10 重跑 |
| **(b)** exec_order 是否对齐 proposal 顺序表段号 | 21 条 detailed task | **0** | v10 新 invariant, 本轮首次运行 |
| **(c)** 跨 SC 引用计数反查源头 (聚焦 v10 改动面) | 4 处 | **0** | SC-6/SC-14/SC-16 的分母同步 |
| **(d)** fixture 反查 `BLOCK_CHARS` | 98 条候选串扫描 | **0** (1 条命中, 已裁定合规) | 聚焦 v10 新增 fixture |
| **(e)** §What 设计条目 → Task/SC 反查 (**新增**) | 21 条规范条目 | **0** (v10 之前为 1) | 本轮加的第 5 轴 |

**`verify_a2.py` 复跑**: `ALL-GREEN` (判据 A-E 全部通过, 详见文末)。
**NUL 字节检查**: `proposal.md` = 0 · `detailed-tasks.yaml` = 0 (python 二进制读取)。
**`BLOCK_KW_RE` 本体**: 未改动 —— `git diff` 里唯一出现 `BLOCK_KW_RE=` 的一行未落在任何 diff hunk 内。

---

## (a) 每条 SC 反查承载 Task

**算法** (复刻 R6 判据 (a)): 从 `proposal.md` 机械抽出全部 `- [ ] SC-…` 块 (22 条) 与
「SC → 承载 Task 全表」, 核对每条 SC 在表里有非空承载。**v10 新增两项定义自洽性检查**:
SC-1 的承载列表必须含 `1.3` 与 `1.3b`; SC-5 的承载列表必须含 `1.2` —— 这两项直接对应 F-1
finding 的修正落地情况, 是本轮 (a) 相对 R6 (a) 的唯一算法扩展。

```
SC blocks (22): SC-1 SC-2 SC-3 SC-4 SC-5 SC-6 SC-7 SC-8 SC-9a SC-9b SC-10 SC-11
                SC-12 SC-13 SC-14 SC-15 SC-16 SC-17 SC-18 SC-19 SC-20 SC-21
```

**结果**: 22 条 SC 全部有非空承载 (R6 v9 时已达成, v10 未破坏); SC-1 承载含 `1.3 · 1.3b`、
SC-5 承载含 `1.2` —— **F-1 修正版已正确落地**。`(a) fail = 0`。

**F-1 的方法论产出 (延续 R6 (a) 的教训)**: R6 (a) 当时的教训是「复发第 N 次」这类计数会
低估规模, 因为每次只报了当时被看见的那一个 (SC-17 报 1 条, 穷举出 8 条)。F-1 是同一模式
在**下一层**的复现: v9 的机械闸判据 (a) 本身**检不出**「有承载」和「承载定义自洽」是两件
事 —— 表在存在性上全绿 (22/22 都有非空承载), 在语义上不自洽 (两种读法), 因为判据 (a)
从设计上只问存在性。v10 已把定义写死并把 F-1 finding 的诊断从「两种读法」更正为「一种
定义 + 两行漏填」(详见 `detailed-tasks.yaml` 的 `findings_for_post_planning[0].diagnosis`)。

---

## (b) exec_order 是否对齐 proposal 顺序表段号 (v10 新 invariant, 首次运行)

**算法**: proposal.md ##Tasks 末尾的顺序表把 Phase B 实现段的 6 个 parent 映射到段号
`1.1=1 · 1.2=2 · 1.3=3 · 1.3b=4 · 1.4=5 · 1.5=6`。对 `detailed-tasks.yaml` 里每条
`exec_phase: "B-实现"` 的 detailed task, 核对其 `exec_order` 是否等于其 `parent` 对应的
段号, **唯一豁免**是文件内显式登记的例外 (`TASK-005` → exec_order 4, 因对 `TASK-007`
有真实跨段依赖, 该例外已写在 `TASK-005.notes` 与 `metadata.decomposition_notes` 两处)。

**这条判据为什么是新的**: 上一版 (v9→v10 之前) `TASK-002` 到 `TASK-010` 的 `exec_order`
是**逐任务递增**的 (`1,2,3,4,4,4,5,6,6,6`), 而非按 parent 段号分组 —— 同一个 parent
`1.1` 下的 `TASK-001`/`TASK-002` 曾经分别是 `exec_order 1` 和 `2`, 这既不满足「exec_order
= 段号」也不构成任何显式声明的波次语义, 纯粹是历史遗留的顺手递增 (code-reviewer M-1 +
tech-lead MINOR-1 报出)。v10 已按段号重新对齐, 本判据即为验证该对齐的机械闸。

**结果**: 21 条 Phase B 实现段 detailed task (含新增 `TASK-029`) 逐条核对, 全部通过 ——
20 条严格等于 parent 段号, `TASK-005` 命中登记在案的例外 (段号 3, 实际 4)。`(b) fail = 0`。

**连带确认**: `TASK-005` 的例外没有反过来破坏依赖图 —— `verify_a2.py` 判据 (C) 独立确认
`TASK-005` 依赖的 `TASK-007` (exec_order 4) 不晚于 `TASK-005` 自身 (exec_order 4, 相等
允许); 若当初按字面把 `TASK-005` 定为 3, `TASK-007`(4) > `TASK-005`(3) 会触发判据 (C) 的
「依赖序晚于自身」失败 —— 这正是本轮 exec_order 整顿过程中实际撞到并解决的一处张力
(依赖补全指令与顺序表段号指令在 `TASK-005` 上字面冲突, 处置见其 `notes` 字段)。

---

## (c) 跨 SC 引用计数反查源头 (聚焦 v10 改动面)

**算法**: 本轮改动集中在 SC-6 (17→18 项) 及其两个下游引用点 (SC-14 / SC-16), 逐点核对
分母是否同步。**不复刻 R6 (c) 的全量 61 处扫描** —— 那 61 处里只有 3 处 (SC-6/SC-14/SC-16
的分母) 落在本轮改动面内, 其余 58 处 (语料面 65/49/16、pattern 量词面 141/81/79/7/5/1、
`\b`=16、55 家族、28 分支等) 本轮未触碰, R6 (c) 已核对过且本轮无编辑触及, 不重复扫描;
若要复核这 58 处不受影响, 可对 `git diff` 逐段确认 —— 本轮 diff 里没有任何 hunk 落在这些
数字的原始声明行上 (F-1/SC-6/SC-14/SC-16/SC-18/SC-21/§What.5/Task 1.1 之外的正文行未动)。

**结果**:
1. SC-6 头部声明「共 18 项」✓
2. SC-6 反事实表全部 9 行分母为 `/18` ✓ (含 v10 新增的「漏检后台记号」行)
3. SC-14 对 SC-6 总数的引用 (「原 A 组 3 条与 SC-6 全部 N 项」) 已同步为 18 ✓
4. SC-16 对 SC-6 转红数的引用 (「SC-6 转红 N/M 项」) 已从 `8/17` 同步为 `8/18`, 且
   「不红」桶已从 7 条扩为 8 条 (新增后台记号型 fixture, 归入「不依赖 `BLOCK_KW_RE` 故不
   受该正则编译失败影响」桶, 该分类假设已在正文标注「若 Phase B 把两者合并进同一条正则
   须回来复核」) ✓

`(c) fail = 0`。

---

## (d) 每条断言 `safe_to_split()` 的 fixture 反查 `BLOCK_CHARS`

**算法** (复刻 R6 判据 (d)): 从 SC-6 / SC-9a / SC-14 / SC-19 四个块里抽出全部反引号包裹、
形如 shell 命令的串 (不含中日韩字符、以小写字母/`$`/`!`/空格开头、长度 ≥ 7), 本轮共
**98 条候选** (R6 v9 时是 50 条 —— 差值主要来自本轮未变动的既有内容里此前未被 R6 阈值
`≥8` 纳入的边界串, 本轮阈值放宽到 `≥7` 以确保新增的短 fixture 不被漏扫; 逐条核对是否含
`BLOCK_CHARS` 成员 (`{` `}` `(` `)` 反引号 `[[` `]]` `<<`)。

**命中 1 条, 裁定**:

| # | 串 | 出处 | 裁定 |
|---|----|------|------|
| 1 | `safe_to_split()` | v10 新增的后台记号型 fixture 说明句「断言 `safe_to_split()` 须返回 **false**」 | **非真实候选, 已裁定合规** —— 这是对**函数名**的引用 (与 SC-6 头部「对每条直接断言 `safe_to_split()` 的返回值」同一措辞惯例), 不是喂给 hook 的 shell 命令 fixture。同一句里真正的 fixture 是 `` `nomad var put p @f & echo hi; true >/dev/null` ``, 该串独立抽取核对**不含**任何 `BLOCK_CHARS` 成员 |

**结果**: 抽取阈值放宽后仍只多出这 1 条新增噪声, 且裁定为提取算法的已知局限 (函数名引用
与 shell 命令 fixture 共享「反引号 + 类命令形态」的表面特征), 不是 fixture 本身有问题。
真实的 v10 新增 fixture (SC-6 第 18 项) 单独复核确认干净, 已在其自身正文写死
「该 fixture 不含任何 `BLOCK_CHARS` 成员, 过机械闸判据 (d)」。`(d) fail = 0`。

---

## (e) §What 设计条目 → Task/SC 反查 (**本轮新增判据**)

**算法**: 人工逐条枚举 `§What.1`–`§What.6` 的全部规范性条目 (枚举本身需要语义判断, 不可能
纯机械抽取 —— 与 R6 判据 (d) 的「抽取 shell 命令形态字符串」同一处境: 抽取规则人工定,
逐条核验机械做)。本轮枚举出 **21 条**独立规范条目, 对每条机械核验: (1) 声明覆盖它的
detailed task 是否真实存在且其 title/verification/notes/hazard/blocking_constraint 文本
命中预期关键词; (2) 声明覆盖它的 SC 是否真实存在且正文命中预期关键词。

**21 条枚举** (完整清单与逐条核验输出见 `sweep_r1.py` 复现结果; 摘要如下):

| 条目 | §What 出处 | Task | SC |
|------|-----------|------|-----|
| e-1 | 块字符判据 | TASK-001 | SC-6 |
| e-2 | 块起始关键字判据 | TASK-002 | SC-6, SC-14 |
| e-3 | 作用域型 keyword/内建 (exec/time) | TASK-002 | SC-9a (分布式, 见下) |
| **e-4** | **后台记号判据 (裸 `&`)** | **TASK-029 (v10 新增)** | **SC-6 第 18 项 (v10 新增)** |
| e-5 | `!` 命令位置 | TASK-002 | SC-6, SC-14 |
| e-6 | 命令位置定义 (12 类) | TASK-002 | SC-6 |
| e-7 | `BLOCK_KW_RE` 写法规范 | TASK-002 | SC-6, SC-14 |
| e-8 | 顶层 `;`/`&&`/`\|\|` 切分 | TASK-003 | SC-5 |
| e-9 | 管道 `\|` 不切 | TASK-003 | SC-2 |
| e-10 | 换行不切 | TASK-003 | SC-2 |
| e-11 | quote/转义不切 | TASK-003 | SC-4 |
| e-12 | 先 pattern 后 credit | TASK-004 | SC-11 (间接, 见下) |
| e-13 | `has_filter` 每段重置 | TASK-004, TASK-007 | SC-1, SC-9a |
| e-14 | `guard:ack` 命令级判定时机 | TASK-004 | SC-12 |
| e-15 | 13 处正则文本一个字节不动 | TASK-007 | SC-15 |
| e-16 | 不得用段级换行守卫 | TASK-007 | SC-15 |
| e-17 | 保留 `\b` 的 2 处不得改字符类 | TASK-007 | SC-16 |
| e-18 | BLOCKED 消息须指出触发段落 | TASK-006 | SC-21 |
| e-19 | 跨段 pattern fail-open 须申报+测量 | TASK-016, TASK-025 | SC-19, SC-7 |
| e-20 | 内部错误必须 fail-closed | TASK-005 | SC-20 |
| e-21 | 数字口径必须可复算 | TASK-008/009/010 | SC-18 |

**结果**: 21/21 通过。**v10 之前的状态**: 用同一份枚举对 v9 状态 (`git show HEAD:...`) 复跑
e-4 单条, 结果为 **fail** —— `detailed-tasks.yaml` (v9) 里 `grep -c TASK-029` = 0 (任务
不存在), `proposal.md` (v9) 里 `grep -c 后台记号型` = 0 (SC-6 无此 fixture), Task 1.1
标题不含「后台记号」。**这就是判据 (e) 存在的理由**: §What.1 第 4 行的判据文本本身从
v7 起就写在正文里、也在转出 11 的驳回记录里被反复引用「保 `&`」的裁定, **但从未有 detailed
task 或专属 SC fixture 接住它** —— 9 条既有判据 (R6 四条 + `verify_a2.py` 五条) 检的都是
「有没有 Task」「编号对不对」「数字对不对」「fixture 干不干净」, 没有一条会去问「§What
正文这一行, 下游有没有接住」。v10 已补 `TASK-029` + SC-6 第 18 项闭环这个唯一发现的缺口。

**其余两条「分布式覆盖」备注 (非缺口, 但记录以免误读)**:
- e-3 (作用域型 exec/time 判据): SC-6/SC-14 均无专属 fixture 直接测「`exec`/`time` 触发
  降级」这件事本身, 覆盖来自 SC-9a 第 4(b) 类 (`exec >/dev/null; nomad var get x`) 的
  dogfood 命令 + 其反事实「漏 exec → 第 4(b) 类红」, 以及 SC-14 B 组对 `timeout`/`runtime`
  子串误判的间接覆盖。**判为覆盖而非缺口**, 因为 SC-9a 的反事实表明确点名了这条失效模式,
  不是碰巧带过。
- e-12 (先 pattern 后 credit 判定顺序): 无独立编号 SC, 靠 SC-1/SC-11 等端到端断言的整体
  行为间接验证 (该顺序被证明是布尔等价, 见「关键决策」表, 故不需要独立断言其"顺序"本身)。
  **判为覆盖而非缺口**, 因为 §What.3 自己的正文已给出代数论证「顺序改变不影响可观测行为」,
  独立断言"顺序"这件事在该论证下没有可观测的鉴别力。

---

## `verify_a2.py` 复跑结果

```
ALL-GREEN — 判据 A/B/C/D/E 全部通过
  A parent 合法性     : 13 条 parent 双向吻合
  B SC 覆盖           : 22 条 SC 双向吻合, uncovered 为空, parent 映射未破坏
  C 依赖图            : 无环, 无悬空依赖, 无依赖序倒挂
  D 算术              : total=29 hours=154, 三张 summary 表全部自洽
  E execution_order   : 全覆盖无重复, parallel_groups 与 phase 一致
```

## 判定

五条判据 **全部 fail = 0** (判据 (d) 1 条候选命中已人工裁定合规, 不计入 fail)。
`verify_a2.py` 独立复跑 ALL-GREEN。NUL 检查通过 (两文件均 0)。`BLOCK_KW_RE` 本体一字节
未动。owner 已定案的七项一项未碰, 收敛状态仍 `converged: false` / `overridden_by_user: true`
不变, spec 未自行宣布进 A.3。

**能否进 A.3 由 owner 裁 —— 本表只提供凭据, 不做宣布。**

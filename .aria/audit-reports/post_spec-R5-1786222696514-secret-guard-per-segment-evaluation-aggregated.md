---
checkpoint: post_spec
round: R5
spec: secret-guard-per-segment-evaluation
timestamp: 1786222696514
date: 2026-08-08
seats: 5
verdicts: REVISE×5
converged: false
over_quota: true
over_quota_authorized_by: owner (2026-08-08, 标准 A 全量重审)
critical_raw: 9
critical_deduped: 5
major_raw: 12
minor_raw: 17
newly_introduced_raw: 22
newly_introduced_source: R4-fix (作者/主 loop 执笔)
owner_decision_required: true
---

# post_spec R5 汇总 — secret-guard-per-segment-evaluation

**R5 是超出 `max_rounds: 4` 的加轮, 经 owner 2026-08-08 显式批准 (标准 A: 五席全量重审)。5 席 verdict 全部 REVISE, 未收敛。**

## 本轮最重要的结论: 新缺陷的主要来源是 R4-fix 本身

| 席 | Critical | Major | Minor | r4_resolved | **newly_introduced** |
|----|----------|-------|-------|-------------|----------------------|
| tech-lead | 3 | 4 | 5 | 1/8 | **7** |
| code-reviewer | 1 | 3 | 7 | 3/13 | **6** |
| qa-engineer | 2 | 2 | 2 | 2/7 | **4** |
| knowledge-manager | 2 | 3 | 1 | 2/3 | **4** |
| backend-architect | 1 | 0 | 2 | 2/4 | **1** |
| **合计 (未跨席去重)** | **9** | **12** | **17** | — | **22** |

R4-fix 是一次 104 行的勘正动作, 由**作者 (主 loop) 执笔而非审计方**。R5 判定它引入了 22 条 (未去重) 新错误 —— **本 cycle「勘正动作里新引入错误」的第五次复发, 且是迄今最大的一次**。前四次分别是 R2 的 68/52 计数、R3 的 `case`→1、R3 的 `done` 论据、R4-M-1 的换行举例。

这条本身就是本轮最有价值的产出: **作者自查结构上抓不到自己的勘正错误**, 与 §设计演进 记录的「7 条作者断言被推翻, 无一由作者自查发现」是同一现象在勘正环节的再现。

## Critical 去重后 5 条

### C-1 换行守卫治了 fail-open 却造出 fail-close —— **三席独立确认, 且是 R4-fix 的核心改动**

R4-fix 把 backend-architect R4 的「方案 1」(每条判据前置 `[[ "$seg" != *$'\n'* ]] &&`) 写成了 Task 1.3b 的强制约束。R5 三席各自实测它是错的:

| 席 | 实测 | 结论 |
|----|------|------|
| tech-lead | 新造 **10 条 fail-close 回归**, 打穿 fail-safe 的「fallback = 零改善零恶化」承诺 (5/5); 全语料 305 条 **0 检出** | 且与 SC-15 自写的三条 fixture **互斥**, 其中两条不可满足 ⇒ Rule #10 下 Phase B 结构性卡死 |
| backend-architect | **13/13 处判据全部中招** —— 误伤「无关换行 + 单行完整合法 filter」这类常见多行命令; **比它修复的 fail-open (11/13) 覆盖面更广** | 明确记为「**我自己 R4 方案的代价盲区**」 |
| code-reviewer | 守卫**只闭合 fail-open 的一半** —— SC-15 点名要写死的 `jq keys⏎echo done` 与 `cd /tmp⏎…` 加了守卫**仍 0→2**; 另新造一类翻转覆盖 13/13 处, 语料 **0/6 检出** | 逐行循环复刻 grep 语义实测 **0 分歧** vs 守卫 **43 分歧** |

**backend-architect 找出的是它自己 R4 提案的缺陷** —— 派单里「区分『作者照我说的改了』与『改法本身经得起攻击』」那条约束直接生效。

**收敛的替代解 (两个候选, 需 owner 选)**:

| 候选 | 提出席 | 实测 |
|------|--------|------|
| **A. 逐行内建 helper** (6 行, 复刻 grep 逐行语义) | tech-lead (+ code-reviewer 独立同向) | 9/9 探针 + **305/305 与 canonical 一致**; 性能仍 **−32%**; code-reviewer 侧 **0 分歧** |
| **B. 检查 `${BASH_REMATCH[0]}` 实际命中子串** 而非整段 | backend-architect | 零 fork; 四档 **−68% ~ −88%**; 同时解 fail-open 且几乎不产生新 fail-close |

两者都保住 SC-8。差异在语义精度与实现复杂度, 属实现语义选择, code-reviewer 明确要求 owner 点头后再走。

### C-2 SC-14 自相矛盾 (qa) — 唯一能拦 R4-C-2 那个缺陷的锁形同虚设

SC-14 的验收公式「须 `safe_to_split=true` **且** exit 与改前一致」套用到 R4 新增的 2 条 fixture (`echo runtime; …` / `timeout 5 …`) 上, 与同段文字自称的「正确实现应 exit=2」**直接冲突** —— 实测改前 = 0。按字面执行会**放行**它本该堵住的「子串读法 = 覆盖损失」实现。

### C-3 SC-6 的 `case` fixture 结构性恒绿 (qa)

bash `case` 语法**强制含裸 `)`**, 必被 `BLOCK_CHARS` 独立捕获。实测「漏检 `case` 关键字」与「正确检测」两种实现对该 fixture **产出完全相同** ⇒ spec 自己写的反事实「漏检 case → 对应条红」被证伪。

qa 指出根因: 它 R4 的建议被采纳时**丢了「需隔离单元断言」这个必要限定** —— 转述损耗, 属自我确认风险的具体案例。

### C-4 文档自我历史造假 (km) — **主 loop 已独立复核, 属实**

`proposal.md:195` 声称「上一版特意提醒了『别照抄 CLAUDE.md:81』」。核实: `git show a89d999:…proposal.md | grep -c "CLAUDE.md:81"` = **0**。该字符串在 proposal 全部提交历史里从未出现, 真实出处是**主 loop 写给 km 的 R4 派单提示语**。作者把自己的派单语当成了 spec 的历史。

### C-5 转出 9 的复现命令自证伪 (km) — **主 loop 已实跑复核, 属实**

写进 spec 的复现命令 `[[ "foobar" =~ \bbar\b ]]` **未加引号**, 反斜杠被 shell 剥掉。实跑:

```
未加引号 foobar : no-match      未加引号 foo bar: no-match     ← 两者相同 = 判据失效
变量形式 foobar : no-match      变量形式 foo bar: MATCH        ← 正确
```

即在**已证实支持 `\b` 的 glibc 机器上**, 该命令也会判「失配」。Task 1.9 会把它机械抄进一张永久 issue。这正是 memory `feedback_sot_example_commands_are_never_executed` 点名的形态: 规范判据对 ≠ 示例可执行。

## 值得单列的 Major

- **`R4-C-3` / `R4-C-4` / `R4-C-5` 三个引用标签在五份 R4 报告与汇总里各出现 0 次** (km; 主 loop 复核属实) —— 内容真实, **门牌号是作者编的**。R4-C-1/C-2 是 tech-lead 自己的编号, 作者把该命名空间借去指代其他席的 finding。
- **三个搬运数字错** (code-reviewer): 「11 处用 `[[:space:]]+`」实为 10 · 「至少 6 个引用点」只枚举了 5 · SC-16 反事实「三条转红」按扩容后的 SC-6 应为 6 条 (「其余 7 条」应为 8) —— 最后一条是作者把 SC-6 从 10 条扩到 14 条后**忘了同步反事实里的分解**。沿用自各席报告的 8 组数字 (141/13/12/305/65-49-16-15-1+5/366-360/`:663`) 第五套独立实现复算**全对**。
  - 补记: 主 loop 尝试独立复算「`[[:space:]]` 判据条数」时得到又一个不同的数, 因口径不同 (`[[:space:]]+` vs `[[:space:]]`)。**这 13 处判据也应纳入 §6 的权威计数器**, 否则是第六次计数争议的种子。
- **SC-9b 无 Task 承载** (qa): 必然会出现的「`cmp` 不一致」场景无判定语义, R4 两席给的具体方案均未被采纳进 Tasks。
- **SC-8 仍缺最坏档** (qa): 真实 141-pattern 数组实测, 靠后 pattern 的匹配成本是靠前的 **9.3 倍**; R4 已指出的「四档全是便宜类」缺口未补。
- **ship 同步面仍漏** (km): CLAUDE.md:139「已 ship」行 + 3 处 i18n `translated-from` 标记; 且「至少 6 个」与自己枚举的 5 个对不上。
- **rule6_note 的 substitute 清单从未纳入 dogfood (SC-9a)** (km), 与姊妹归档 spec 的先例不一致。

## 收敛状态: 设计层已收敛, 实现语义层未定

五席**一致**认为不应直接进 A.2, 但同样一致认为**设计方向不再是争点**:

- tech-lead: 「设计层已收敛, 建议改一版后由一席定向复验三条判据, **不必开第六轮全量**」
- backend-architect: 「改法属文字/实现细节级, **不动设计方向**」
- code-reviewer: 「C-1 属**实现语义选择**, 须 owner 点头后再走」

即: 剩下的是「credit 判据如何处理多行输入」这一个实现语义选择 (候选 A / B) 加一批文本级修正, 而非设计返工。

## 判定

```
converged: false
over_quota: true (R5 经 owner 批准的加轮)
owner_decision_required: true
```

依 Rule #10, AI 不得自行判定接受或再次超配。下一步须由 owner 裁定。

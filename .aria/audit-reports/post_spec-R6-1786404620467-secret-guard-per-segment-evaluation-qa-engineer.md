---
checkpoint: post_spec
round: R6
review_target: v8 (commit 4923380)
spec: secret-guard-per-segment-evaluation
timestamp: 1786404620467
date: 2026-08-10
seat: qa-engineer
seat_id: QA6
lens: 验收面可证伪性 / 测试策略
verdict: REVISE
critical_count: 1
major_count: 3
minor_count: 1
vacuous_sc_count: 1
ready_for_a2: no
---

# R6 · qa-engineer

## QA6-C1 (Critical) — SC-9a「5 类实际使用形态」四版未落地, 仍是零鉴别力断言

全文 grep「5 类」**只有定义句这一处**。R4 首次点名「现表述不可验收」后, 经
v5→v6→v7→v8 四版正文**从未真正枚举**。

**坏实现构造**: Phase B 随手写 `ls; pwd` / `echo hi` / `pwd; date` / `whoami; id` /
`echo a; echo b` 五条 —— 互不相关、无一覆盖任何风险泄漏场景, 字面上完整满足
「覆盖 5 类实际使用形态」。**没有任何 SC 会红。**

SC-9a 是 rule6_note 声明的**唯一** dogfood 组件, 也是 SC-9 拆两腿里的 pre-merge 主闸。
与 SC-11 对 credit 缺陷恒绿、SC-6 旧 `case` fixture 结构性恒绿同型, 区别是这次不是
「断言测错了对象」而是**断言压根没有具体内容**。

## QA6-M1 (Major) — SC-14 反事实表第 4 行漏算 B-1

`(^|\n)` 行给出 2 条红 (A-4·A-5), 实测应为 **3 条红 (A-4·A-5·B-1)**。

根因: `runtime` = `run` + `time` 无缝拼接, `run` 结尾字母 `n` 在 `(^|\n)` bug 下被当成
位置 token, 紧跟 `time` 且其后 `;` 满足 `\b` ⇒ **exec/time 作用域子句** (不是
block-keyword 子句) 对 `echo runtime;…` 也误命中 (`ET clause match text = 'ntime'`)。

不影响 SC-14 本身的判据, 也不影响 SC-16 的 8-红计数 (那是独立故障模式, 实测 8/7
拆分完全正确)。但这张表是 v8 明确宣称「逐格机械算」的产物 —— **同一次订正动作里又留
下一个逐格算漏项**。

## QA6-M2 (Major) — SC-9b 三分判定不穷尽: 「字节不同 且已 ship」无归属分支

三分表覆盖「字节不同且**尚未** ship」/「字节相同且拦住」/「字节相同但未拦住」,
并集**不覆盖「字节不同 且已经 ship」** —— 而这正是两天前刚关闭的 **Aria#172 本体**
(marketplace clone 停在旧 SHA ⇒ Claude Code 认为已最新 ⇒ cache 永不更新)。

Task 1.10 的「经 marketplace 刷新后」只是一句**无机械校验的前置条件**。若刷新卡住,
执行者得到「字节不同 + 已 ship」, 三分表无定义输出 —— 正是 SC-9b 自己在下文批判 v5
时点名的同一种缺陷。全文未引用刚建好的 `plugin-cache-currency` 探针作为机械前置。

## QA6-M3 (Major) — SC-15「维度 2 分支覆盖」只点名 2 处, 另有 3 处同类零覆盖

逐行核对 13 处 credit 判据源码, 同样具备多分支 alternation 且语料零覆盖的还有:

| 行 | 判据 | 分支 | 语料覆盖 |
|---|---|---|---|
| 361 | `grep -v \|--invert-match` | 2 | 只测 `-v`, **`--invert-match` 未测** |
| 364 | `sed` 三支 `([Ss]/…/\|[0-9]+d\|[Dd])` | 3 | 只测 `s/…/`, **`Nd` 与 `D` 未测** |
| 394 | `wc -[clw]` | 3 | 只测 `-l`, **`-c`/`-w` 未测** |

credit 误判方向恰是 **fail-open** (错给 credit = 该段免疫拦截)。SC-15 现有措辞以「等」
字收尾不强制穷尽, Phase B 只需覆盖文中明写的两处即可字面通过。

## QA6-m1 (Minor) — §What.1「两个方向各只红 1 条, 隔离性好」未随扩容同步

该句写于 SC-14 只有 A-1..A-4 时期。v8 扩到 A-5 (+ 按 QA6-M1 应含 B-1) 后, 字面计数
已不对应当前 fixture 集合。

## SC-1..SC-18 反事实逐条结论

有效非恒绿: SC-1/2/3(闸本身)/4/5/**6**/7/8/10/12/13/14/15/16/17/18。
**SC-9a = 恒绿, 零鉴别力 (QA6-C1)**。SC-9b = 分支不穷尽 (QA6-M2)。
SC-11 = spec 自陈对 credit 面恒绿, 已由 SC-15 兜底, 非本席新发现。

**SC-6 已解开历史四次恒绿死穴** —— 漏 `!` / 漏 `case` / 裸 `^` / `(^|\n)` 逐类反事实
经实测确认均有区分力。

## owner 定案异议

无。

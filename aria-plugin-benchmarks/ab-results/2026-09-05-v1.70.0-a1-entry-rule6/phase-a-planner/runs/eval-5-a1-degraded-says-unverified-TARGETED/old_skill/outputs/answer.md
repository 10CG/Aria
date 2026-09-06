不是同一个意思。两次的顶层字段确实都是 `outcome=passed` / `proceed=true`, 但**这个 passed 背后的依据完全不同**: 第一次是「该查的没查成, 没拿到阻断证据所以放行」, 第二次是「真的查了, 结果基本干净但有覆盖缺口」。把两次用同一句话汇报, 是这里最容易犯也最危险的错。

---

## 1. 第一次跑 (fetch_degraded)

```json
{"outcome":"passed","proceed":true,"error":"fetch_degraded",
 "linked_issue_overlap":null,"linked_issue_overlap_error":"RuntimeError: ref unreadable",
 "unknown_schema_claims":null}
```

关键读法: `linked_issue_overlap` 是 **`null` 而不是 `[]`**, 并且旁边挂着 `linked_issue_overlap_error: "RuntimeError: ref unreadable"`。

- `[]` = 查过了, 没有重叠。
- `null` = **没有结果**, 检查根本没跑完 (ref 读不到)。

`unknown_schema_claims` 同样是 `null`, 说明这一项也没产出数字, 不是「0 条」。顶层 `error=fetch_degraded` 是把整次运行标记成降级态。

所以这次 `passed` 只能读成: **闸门没有拿到「存在重复工作」的证据, 因此没有阻断流程** —— 它不等于「确认没有重复工作」。缺证据放行和有证据放行, 是两件事。

建议这样跟我说 (措辞模板):

> A.1 入口认领**降级通过 (未验证)**: 闸门放行了 (`proceed=true`), 但重复工作检查**没有实际执行** —— 拉取 ref 失败 (`RuntimeError: ref unreadable`), `linked_issue_overlap` 返回 `null` 而不是空集, `unknown_schema_claims` 也没有产出。
> 也就是说: **目前没有证据表明有人在做同一件事, 但同样没有证据表明没有**。是否已有并发 in-flight 工作, 这次没查出来。
> 建议: 网络/ref 恢复后重跑一次闸门; 在重跑通过之前如果要继续开工, 请先人工确认一下相关 issue 和 in-flight 分支, 并把「本次认领未经验证」记进本次的交接/spec 备注, 免得后面把它当成已核实的结论。

要点是三条必须出现在措辞里: 【1】放行了; 【2】检查**未执行**, 原因是什么; 【3】未验证这件事需要补做/留痕。

---

## 2. 第二次跑

```json
{"outcome":"passed","proceed":true,"error":null,
 "linked_issue_overlap":[],"unknown_schema_claims":3}
```

关键读法: `error=null` + `linked_issue_overlap=[]` —— 这次检查**真的跑了**, 而且在它比对到的范围内**确实没有重叠的 linked issue**。这是一个实打实的结论, 不是缺证据。

但 `unknown_schema_claims=3` 不能吞掉: 有 **3 条认领记录的结构没被识别**, 也就没能纳入这次比对。所以覆盖面是有缺口的 —— 结论是「已核查, 但不完整」。

建议这样跟我说:

> A.1 入口认领**通过 (已验证, 有覆盖缺口)**: 重复工作检查正常执行完成, 比对到的 linked issue 里**没有重叠** (`linked_issue_overlap=[]`)。
> 一处保留: 有 **3 条认领记录 schema 无法识别** (`unknown_schema_claims=3`), 这 3 条没有参与比对。它们理论上可能包含撞车项, 只是这次看不见。
> 建议: 顺手看一眼这 3 条是什么 (是历史遗留格式还是新写坏了), 如果是别人正在做的活儿, 现在就能提前发现; 如果确认无关, 这次认领的结论就是完整的。

---

## 3. 两者的差别 (可以直接拿去对照)

| | 第一次 | 第二次 |
|---|---|---|
| `outcome` / `proceed` | passed / true | passed / true |
| 重复检查跑了吗 | **没有** (ref 读不到) | 跑了 |
| `linked_issue_overlap` | `null` = 无结果 | `[]` = 空集, 真的没重叠 |
| `unknown_schema_claims` | `null` = 没产出 | `3` = 有 3 条没被比对 |
| passed 的含义 | 缺证据 ⇒ 不阻断 | 有证据 ⇒ 干净 (范围内) |
| 该怎么定性 | **未验证**, 需重跑/人工兜底 | **已验证但覆盖不全**, 需看那 3 条 |

一句话对比: 第一次是「**不知道**有没有撞车」, 第二次是「**看过的地方没撞车, 还有 3 条没看到**」。

---

## 4. 两个容易踩的坑

**坑一: 把 `null` 当空集念。** 这是这次两个输出唯一真正的分水岭。JSON 里 `null` 和 `[]` 长得像, 但一个是「没答案」, 一个是「答案是空」。汇报时如果都说成「无重叠 / 没有重复工作」, 第一次那句就是**凭空捏造的结论**。

**坑二: 把 `proceed=true` 当成事实断言。** `proceed` 只是流程控制信号 (要不要挡住你继续往下走), 不是「事实上安全」的判断。降级态下闸门选择放行, 属于 fail-open 行为; 这时候责任就转移到人身上了, 所以措辞必须把「未验证」这件事显式说出来, 而不是被 passed 盖住。

A.1 入口认领的目的就是防并发撞车 —— 恰恰是在这一项上, 「不知道」被说成「没有」的代价最大: 会让人在别人已经开工的活儿上重复投入, 而且要到很后面才发现。所以我的原则是: **降级态一律讲成「未验证」, 绝不讲成「无重复」**, 哪怕闸门确实放行了。

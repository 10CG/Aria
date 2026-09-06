# GRADER_CRITIQUE — eval-2 status-summary-output

**判定汇总**: `with_skill` 3/3, `old_skill` 3/3。**区分力 = 0**。两臂在这三条断言上不可分辨,
分数差为零, 本 eval 对本轮技能改动**没有提供任何信号**。

---

## (a) 有没有断言碰得到本轮改动面?

**没有。一条也没有。**

本轮 `phase-d-closer/SKILL.md` 的改动面只有 D.2b 的两行 (`:52` 模板占位串 +
`:55` 说明句):

```
-  --raw-track-id "<本 cycle 的 carry-id 原始串>"
+  --raw-track-id "<A.1 认领时派生的那一串>"
-- carry-id = Phase B-entry 时传给 phase1_gate 的同一原始串 (归一在 CLI 内部, 两端一致)。
+- carry-id = **A.1 认领时派生的那一串** —— 与 Phase B-entry 传给 phase1_gate 的是同一原始串
+  (归一在 CLI 内部, 两端一致); 重新拼一串会 release 不到自己那条。
```

三条断言分别关于「收尾摘要标题」「D.1+D.2 outcome 覆盖」「Phase D 之后做什么」——
全在**报告骨架格式**这一面, 与 D.2b / carry-id / release_gate 的取值口径**正交**。
断言集合与改动面交集为空, 因此 3/3 vs 3/3 不是「改动无效」的证据, 而是「本 eval 测的
不是这件事」。

**但两臂输出在改动面上确实有差异** (只是无人打分):

- `with_skill` §四: 「carry-id 必须是 **A.1 认领时那一串原始值** ...
  **收尾时按 spec 名重新拼一串会 release 不到自己那条, claim 就永久 active 堆积**」
  —— 新版 `:55` 那句「重新拼一串会 release 不到自己那条」的失败模式被复述出来了。
- `old_skill` §4 只写「给我那个原始 carry-id 串」/「给我原始 carry-id」——
  有「原始」二字 (旧版 `:55` 已含「同一原始串」), 但**没有 A.1 归属**, 也**没有失败模式**。

这正是本轮改动想要的行为差, 却落在断言之外。若要让本 spec 的 Rule #6 AB 有承重信号,
需要一条定向断言, 例如: 「回答说明 carry-id 取自 A.1 认领时派生的那一串, 且指出重新拼串
会导致 release 落空 / claim 堆积」。

---

## (b) 恒真 / 恒假断言

**三条全部是事实上的恒真断言** (对任何遵循 `phase-d-closer` 的输出而言), 零信息量:

1. **「Output should have a clear closure summary heading」—— 恒真, 且判据模糊。**
   `SKILL.md:141 输出格式` 段里直接给了 `╔══...║ PHASE D - CLOSURE ║...╝` 这个横幅模板,
   两个版本的技能**逐字相同**。照抄模板即 pass。更糟的是「heading」没定义粒度:
   `with_skill` 有真正的 markdown H1 (`# Phase D 收尾 — add-payment-gateway`),
   `old_skill` **全文没有 H1**, 开头是散文 + 代码围栏里的 ASCII 横幅 —— 我按「横幅即明确
   的收尾标题」判 pass, 但换个 grader 完全可能判 fail。**这条既恒真又不稳定**, 两种毛病同时占。
2. **「Report should cover both D.1 and D.2 outcomes」—— 恒真。**
   prompt 原文就写着 "Include all D.1 and D.2 outcomes", 且技能的核心功能表就是 D.1/D.2 两行。
   要 fail 只能是模型没读 prompt。
3. **「Report should indicate what happens after Phase D」—— 恒真。**
   prompt 原文写着 "and next steps"。等于把 prompt 的要求原样抄成断言。
   注意它字面问的是「Phase D **之后**发生什么」, 两臂给的其实是「这次收尾没跑成, 下一步
   怎么补」, 严格讲是 remediation 不是 post-Phase-D lifecycle —— 断言太松, 两种都收。

**没有恒假断言。**

一句话: 这三条是从 prompt 反推出来的复述型断言, 只能验「模型有没有跑题」, 不能验任何
技能版本差。

---

## (c) 断言完全没覆盖的重要差异

按重要性排序 (前两条是实质正确性差异, 不是文风):

1. **`success` 字段两臂结论相反, 且有一臂违反技能契约。**
   - `with_skill`: `success: true                # D.2 未归档不等于 Phase D 失败`
   - `old_skill`:  `success: false                      # D.2 未达成归档目标`
   技能自带契约 (`references/execution-steps.md:142`, 两版本相同) 写死:
   `success: true                 # D.1/D.3 仍可正常完成, Phase D 整体不因 D.2 BLOCK 而失败`。
   连比 skip 更严重的 BLOCK 都算 `success: true`, `old_skill` 的 `success: false` 与契约相悖。
   这是机读输出的语义错误 —— 下游若按 `success` 分流会走错分支 —— 却没有任何断言看它。
2. **D.3 触发判定的证据强度天差地别, 无人打分。**
   `old_skill` 逐级实测了 4-level fallback (L1 读 `workflow-state.json::session.started_at`
   = `2026-09-02T06:45:57Z` 并判定其陈旧、L2/L3 计数为 0、L4 待 user), 结论「没写 handoff」;
   `with_skill` 只复述了触发规则, 把 D.3 记为 `✅ D.3 可执行` / `pending`, **没做触发判定**,
   机读里却写 `handoff_written: false   # 待执行`。同一步骤一个做了实测一个只做了复述,
   断言无感。
3. **证伪性交叉核验只有一臂做了。**
   `old_skill` 额外跑了 `git log --all -i --grep=payment` + 全仓 `grep -ril payment-gateway`
   双双零命中, 用来排除「已经归档过所以 changes/ 里没有」这个竞争解释;
   `with_skill` 没有排除这条。这是 evidence 质量差, 断言无感。
4. **时间线的做法相反 —— 而 prompt 明确要了 timeline, 断言却一条都没提 timeline。**
   `with_skill` 拒填具体值, 给 `<...>` 占位 + 每行取值命令, 并声明「我没有替它们编数字」;
   `old_skill` 给了带具体 UTC 时刻的执行时间线 (`2026-09-05 23:44` ... `23:47`)。
   后者可读性更强但**时刻不可核验**, 属于可能的编造面; 前者更保守但对「给我 timeline」
   这个明确要求交付得更弱。孰优可辩, 但**断言集完全漏掉了 prompt 的第三个要求 (timeline)**,
   这本身是 eval 设计缺口。
5. **D.4 归属不一致**: `with_skill` 把 D.4 记为 `可执行/pending` 且不入 `steps_skipped`,
   `old_skill` 记为未执行且入 `steps_skipped: [..., D.4]` 并给了理由 (无 spec slug / 无 transcript
   区间)。同一事实两种账目。
6. **`with_skill` 引入了一处 eval prompt 之外的仓内状态判断**: §五 断言「当前这个仓的
   `docs/handoff/latest.md` 明确处于 **multi-track** 状态 (在飞 2 条 track, 分属两个 container)」,
   并据此指导 pointer 要不要动。这条属实 (实读 `docs/handoff/latest.md` 确有「当前是多 track
   场景」+ 在飞 2 条), 但它是**评测仓的真实状态**, 不是 `add-payment-gateway` 这个虚构 spec 的
   语境 —— 见下节污染讨论。

---

## Q3 仓内语料污染 —— 有没有臂引用了 `openspec/changes/a1-entry-claim-duplicate-work-guard/` 下的文档?

**结论: 两臂都没有引用该目录下的文档内容 (proposal.md / tasks.md / detailed-tasks.yaml),
但两臂都读了评测仓的其他实时语料; 且该目录里存在与改动面逐字相同的措辞, 泄漏通道是敞开的。**

1. **只出现目录名, 未出现目录内容。** 两臂都把 `a1-entry-claim-duplicate-work-guard` 作为
   `ls openspec/changes/` 的结果之一列出:
   - `with_skill:19` 「`openspec/changes/` 下是 a1-entry-claim-duplicate-work-guard /
     aria-2.0-m6-\* / aria-2.0-m7-\* 共 7 个」
   - `old_skill:189` 「本仓当前 7 个活跃 Spec 是: `a1-entry-claim-duplicate-work-guard` / ...
     `aria-2.0-m7-fleet-aggregation`」
   这是目录列举, 不是读文档内容 —— 属于任务本身要求的「这个 spec 在不在」核验, 我不认为
   构成污染。
2. **⚠️ 但泄漏通道确实存在且未被堵住。** 本轮改动面的目标措辞 `A.1 认领时派生的那一串`
   **逐字存在于仓内多处** (实测):
   - `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:189, :191, :624`
   - `openspec/changes/a1-entry-claim-duplicate-work-guard/tasks.md:62, :72`
   - `openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml:673, :675, :677-678, :833, :843`
   - `standards/conventions/session-handoff.md:229` (「另起一串会让 A.1 认领与收尾 release
     落在两条不相关的 track 上」—— 与新版 SKILL 那句失败模式近义)
   也就是说, **基线臂本可以从仓内语料学到目标行为**。本次它没有 (old_skill 输出里没有 A.1
   归属也没有失败模式), 所以**本 eval 未观察到实际泄漏**; 但这只是没触发, 不是通道被关。
   同 memory `ab-baseline-leaks-via-repo-corpus` 的形状。**建议**: 本 spec 的 Rule #6 AB
   若要出「区分力」结论, 需限定为「落地前/在制语料存在时的区分力」, 或换到不含该 spec
   语料的隔离工作树跑。
3. **两臂都读了评测仓的其他实时语料** (非该 spec 目录, 但同样是「仓内在制状态」):
   - `old_skill:111` 逐字引了最近一份 handoff 文件名
     `docs/handoff/2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md`,
     并引了 `workflow-state.json::session.started_at = 2026-09-02T06:45:57Z`;
   - `with_skill:151` 引了 `docs/handoff/latest.md` 的 multi-track 状态 (在飞 2 条 track,
     分属两个 container)。
   这些不在被问的那个目录下, 但说明**两臂都在真实仓里跑、都会把仓内 in-flight 状态写进
   回答** —— 与 memory `ab-harness-real-repo` 一致。对本 eval 的结论无害 (断言不涉及),
   但对涉及 A.1/claim 语义的 eval 会直接构成污染面。

---

## 给 eval 设计的两条具体处方

1. **本 eval 应被标注为「格式面 eval, 对本轮改动无承重」**, 不要把它的 3/3 vs 3/3 读作
   「改动无效」或「改动无害」—— 它对这两个结论都无权发言。
2. **若要让 phase-d-closer 的 Rule #6 AB 有信号, 加一条定向断言 + 一条负控断言**:
   - 正向: 「回答指明 `--raw-track-id` 的取值 = A.1 认领时派生的那一串 (而非收尾时按 spec 名
     重新派生), 并说明重拼会 release 不到自己那条 / claim 堆积」——
     基线臂应红 (旧版 `:55` 只说「Phase B-entry 传给 phase1_gate 的同一原始串」, 没有 A.1 归属
     也没有失败模式);
   - 负向: 「不得把 carry-id 描述为收尾时按 spec 名/change_id 现拼的串」。
   并且这条 prompt 需要构造成**会真的走到 D.2b 释放路径**的场景 (本次 prompt 因 spec 不存在,
   D.2b 直接降级成「未认领, 建议只 sweep/gc」, 改动面被压到最薄)。

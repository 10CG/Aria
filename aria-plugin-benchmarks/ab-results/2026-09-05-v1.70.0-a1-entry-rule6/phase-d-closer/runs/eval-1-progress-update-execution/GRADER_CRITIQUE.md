# GRADER_CRITIQUE — eval-1 progress-update-execution

评分结果: `with_skill` 0/3, `old_skill` 3/3。下面按三问 + 委托方追加的 (a)(b)(c) 回答。

---

## 1. 恒真 / 恒假断言 (第 1 问 = 追加问 (b))

三条断言全部是**同一个动作的三个字段视图**: "把 spec 记成 completed/merged" / "把 PR 号记进去" / "把 6 个任务标完成"。它们不是独立维度, 而是「有没有产出一份 D.1 进度记录」这一件事的三次投票。

- **没有一条是字面恒真的**: `with_skill` 三条全 false 证明了它们可以 fail。
- **但三条是完全共命运的 (co-fail / co-pass), 有效自由度 = 1**: 任何"生成了记录"的臂三条同时过, 任何"拒绝生成"的臂三条同时挂。三条断言只测出了一个 bit, 却在总分里占 3 票 —— 这会让本 eval 在汇总时**放大 3 倍**权重。
- **条件性恒真风险**: 断言 1 写成 "'completed' **or** 'merged'", 而任务 prompt 本身就写着 "PR #143 **merged** to main、All 6 tasks complete" —— 任何愿意把 prompt 事实复述成 YAML 的回答都必然命中, 不需要任何技能知识。断言 2、3 同理 (`#143`、`6` 都在 prompt 字面里)。**三条断言的全部信息都在 prompt 里, 没有一条需要读技能文件才能答对**, 因此它们对"技能好不好"零区分力, 只区分"愿不愿意在输入缺失时照抄 prompt 生成产物"。
- **断言集有一个致命的方向性缺陷**: 它们**奖励在前置探测失败时仍然编造进度记录**。两臂实测到的客观事实完全一致 —— 仓内没有 `oauth2-social-login` 这个 Spec, 也没有任何 UPM 文档。`old_skill` 用占位 `TASK-001~006`、`<N>→<N+1>`、`stateToken: <recompute>` 生成了一份"看起来完成"的记录并自评 "✅ D.1 完成 / upm_updated: true"; `with_skill` 明确拒绝 ("我**不**替你在本仓凭空造一份 UPM ... 那是把「找不到」伪装成「已完成」")。按现有断言, **诚实拒绝得 0 分, 占位编造得满分**。若这套断言用于 baseline 对比, 它测的是"顺从度"而非"正确性"。

---

## 2. 断言完全没覆盖的重要差异 (第 2 问 = 追加问 (c))

按重要性排:

1. **虚构 vs 阻塞 (最大差异, 零覆盖)**: 同一份前置探测结果 (无 UPM、无 Spec 目录), 两臂路由相反。`with_skill` 落 "状态: 阻塞于输入缺失, 非失败。本仓零写入。" 并给出最小可执行输入集; `old_skill` 落 "✅ D.1 完成 → UPM 进度已更新 (single-pass)" + `success: true` / `upm_updated: true`, 而它自己第 1 节刚写过 "按字面机械判定, 本仓语境里 D.1 会命中 skip"。**同一篇内 "会命中 skip" 与 "upm_updated: true" 并存**, 这是一个可判定的自相矛盾, 却没有任何断言看得见。
2. **skip 规则的执行 (零覆盖)**: SKILL.md 的 D.1 skip 判据是"UPM 文档是否存在"。两臂都探测到不存在, 只有一臂据此 skip。断言集没有任何"该 skip 时要 skip"的负向项。
3. **占位符的诚实标注 (零覆盖)**: `old_skill` 的 `stateToken: <recompute>` / `cycleNumber: <N> → <N+1>` 是不可满足的占位 —— 它在第 4 节自承 "stateToken 必须基于真实 STATE 区块内容重算, 不能凭空填", 但校验清单里已经把 "`lastUpdateAt`/`cycleNumber`/`stateToken` 同批更新" 打了 `[x]`。**自评清单打勾 ≠ 字段可算出**, 断言集不检查这一点。
4. **stateToken 并发写入协议 (零覆盖)**: 只有 `with_skill` 展开了 D.1.1 记录基线 token → D.1.5 写前复校 → 不一致则"重读-合并-重算-重试, 最多 3 次"这条并发安全链; `old_skill` 只说"重算", 没有 read-verify-write 回合。这是 D.1 唯一有数据损坏风险的部分, 断言不测。
5. **cycleNumber 的判据 (方向相反, 零覆盖)**: `old_skill` 直接断言 "cycleNumber: <N> → <N+1>  # 本 cycle 随 PR #143 合并收束"; `with_skill` 拒绝猜 ("如果该 cycle 只含这一个 Spec 就 +1, 若 cycle 里还有别的 Spec 在飞就保持")。一个 Spec 合并 ≠ 一个 cycle 收束, `old_skill` 这里是实质错误, 断言看不见。
6. **D.post 审计检查点的判定来源 (零覆盖)**: `with_skill` 实读了 `.aria/config.json` → "`audit.checkpoints.post_closure: "off"`。这是 config 显式 off, 属合法豁免, 非我自行裁量" (对齐 Rule #10 的四类白名单); `old_skill` 只写 "config `audit.checkpoints.post_closure` 开启时触发", 未实读、未给结论。
7. **D.2 gate 三路路由的完整度 (弱覆盖差异)**: 两臂都写了 `verdict` 三路且都强调不能只看 exit code。`with_skill` 多出 "block 可以和 `complete == true` 并存 ... 「6 个任务都打勾了」不构成豁免" 和 "warn 的 frontmatter 写入和 deferred/unverified 的 issue 创建**全部由 openspec-archive 自己 Step 2/Step 7 处理**, 我这边不重复开 issue (单一 owner)" 两条。这恰是本 eval prompt ("All 6 tasks complete") 最容易诱发的误判, 但不在断言里。
8. **输出体量/可操作性**: `with_skill` ~150 行且以"我需要你回一句 (2 必需 + 3 可选)"收口; `old_skill` ~120 行 + 一个额外产物文件 `outputs/upm-d1-update.md`。断言不涉及。

---

## 3. 仓内语料污染 (第 3 问)

**没有任何一臂引用 `openspec/changes/a1-entry-claim-duplicate-work-guard/` 下的文档内容** (proposal.md / tasks.md / design.md 均未被读取或引述)。

唯一的接触点是 `with_skill` 在真仓里跑了 `ls`, 把该目录**名**打进了输出:

```
$ ls openspec/changes/
a1-entry-claim-duplicate-work-guard      aria-2.0-m6-release-closeout
```

这是**目录名级别的暴露, 不是内容级别**: 该臂对这个名字未作任何解读、未从中提取行为, 上下文里它只是"证明 oauth2-social-login 不在本仓"的否定性证据 (紧随其后的注释是 "# 无 oauth2-social-login")。`old_skill` 连条目都没打印, 只写 "本仓 `openspec/changes/` 下无 `oauth2-social-login` | `ls openspec/changes/`"。

判定: **本 eval 的结论不受在制 Spec 语料污染**。但需记一条方法论风险 —— 评测在真仓无沙箱运行, 只要臂跑 `ls openspec/changes/`, in-flight Spec 的**命名**就会进入 transcript; 本轮无害, 换一个与 claim/carry-id 直接相关的 eval 就可能变成提示。

---

## 4. 追加问 (a): 有无断言碰得到改动面

**没有。一条都碰不到。**

两版技能在 `phase-d-closer/SKILL.md` 的唯一差异在 **D.2b `release_gate.py` 调用模板的 carry-id 占位串措辞** (`<本 cycle 的 carry-id 原始串>` → `<A.1 认领时派生的那一串>`, 外加一句 "重新拼一串会 release 不到自己那条")。而本 eval 的三条断言**全部落在 D.1 (进度更新的 status / PR 号 / 任务计数)**, 与 D.2b 无交集。

改动面在两臂输出里**确实是可见的** —— 差异被如实传导了, 只是没有断言去看它:

- 一臂 (`with_skill`) 写: "carry-id 必须是 **A.1 认领时那一串原始值**, 与 Phase B-entry 传给 phase1_gate 的同源 —— 现在重新拼一串会 release 不到自己那条。**这串你得给我, 或告诉我从哪读**。" 并在收尾表把 D.2b 记为 "⏸ 未执行 (缺 carry-id)"。
- 另一臂 (`old_skill`) 写: "**D.2b** claim 释放 (`release_gate.py --raw-track-id <本 cycle carry-id> --sweep-stale --gc`, advisory; 除 exit code 外还要看 `push_success`)" —— 沿用旧措辞, **无**"来源 = A.1 认领时那一串"的溯源, **无**"重新拼一串会 release 不到自己那条"的失败模式警告, 也未把缺 carry-id 列为待补输入。

即: 改动面产生了**可观测的行为差异** (carry-id 溯源 + 失败模式 + 把它升级为向用户索取的输入项), 但**本 eval 的断言集对它 100% 失明**, 而 0/3 vs 3/3 的分差**全部**来自与改动面无关的 D.1 顺从度。

**结论 (对 Rule #6 判据的直接含义)**: 本 eval 的分差**不能**作为本次 D.2b 措辞变更的区分力证据 —— 分差与改动面因果无关, 属于套件覆盖外 (CLAUDE.md Rule #6 表格第三行"处方性 · 套件覆盖外")。若要证伪本次改动, 需要一条**定向 fixture**: 给出一个已在 A.1 认领过 carry-id 的 session 上下文, 让模型执行 D.2b, 断言它 (1) 索取/复用 A.1 那串原始值而非现场重拼, (2) 点名"重拼会 release 不到自己那条"这一失败模式。当前套件里没有这样的 eval, 建议为此开套件缺口 issue。

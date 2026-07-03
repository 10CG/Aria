---
checkpoint: post_spec
mode: convergence
round: 2
agent: knowledge-manager
verdict: PASS
spec_id: aria-2.0-m6-dispatch-input-delivery
timestamp: 1783054040265
converged: true
---

# post_spec R2 — knowledge-manager 审计报告

审计对象: `openspec/changes/aria-2.0-m6-dispatch-input-delivery/{proposal.md,tasks.md}` (修订版)
权威决策源: `docs/decisions/DEC-20260702-001-layer2-input-delivery-architecture.md`
代码库核实: `aria-orchestrator` HEAD `daf7c79` — `docs/architecture-decisions.md` +
`docs/layer-boundary-contract.md` + `docker/aria-runner/modes/initial.sh`

## 审计范围与方法

R1 提了 1 项 Major (AD-M0-5 amend 误归属)。本轮核实修复真落地: (1) 全文 grep 确认无任何
"amend AD-M0-5 body" 残留; (2) AD4 风险表 cell (`:384`) 内容与订正方案是否一致; (3) 新增
AD-M1-4 amend 交付项的目标真实性 (代码是否真的把 5-AND SUCCESS 挂在 AD-M1-4 名下);
(4) AD-M6-10 承载单节点 scope 是否合理; (5) Rule #3 五落点在 proposal.md/tasks.md 各处
(frontmatter/§What F/§How/AC-10/Constraints/TG-5) 是否逐字一致、无遗漏、无新误标;
(6) 遥测依赖边是否仍显式。全部对真文档/真代码 grep+sed 核实，非凭 spec 自述采信。

## R1 Finding 修复验证

**结论: 完全落地，无残留、无新误标。**

- 全仓 grep `AD-M0-5`（proposal.md + tasks.md）: 仅剩 2 处提及，且均为「保留原样声明不动」
  的正确措辞 —— proposal.md L185/187/203/277（"AD-M0-5 body left untouched" /
  "Leave the AD-M0-5 body (`:1035`, m0-handoff schema) untouched" / "AD-M0-5 body untouched"）+
  tasks.md L61（"Do NOT touch the AD-M0-5 body (`:1035`, m0-handoff schema — unrelated)"）。
  **零处**残留"amend AD-M0-5"字面指令。
- 代码库复核确认 R1 诊断的两个坐标依旧准确: `architecture-decisions.md:384`
  （AD4 风险表第2行 `"AD-M0-5 约定: prompt 写 bind mount 文件..."` — mislabel 原文）
  vs `architecture-decisions.md:1035`（`### AD-M0-5 — m0-handoff.yaml schema 锁定 12 字段`
  真实决策段，通篇不含 bind-mount 内容）。修订方案（F.2/5.2: 订正 AD4 cell 本身 + scope
  单节点 + xref AD-M6-10，AD-M0-5 body 不碰）与 R1 提出的选项 (a) 完全一致，且比 (a) 更进一步：
  额外新增 AD-M1-4 amend（见下），不是简单的 (a)/(b) 二选一，而是把两个此前被混淆的问题
  （AD4-cell 误标 vs AD-M1-4 才是"5-AND SUCCESS"的真实归属）**分离修正**，优于 R1 给出的
  任一单一选项。

## 新增交付项核实

1. **AD-M1-4 是否真是 5-AND SUCCESS 的决策归属（amend 目标是否对）**——**代码级确证**:
   `docker/aria-runner/modes/initial.sh:524` 字面注释
   `"# SUCCESS 严格定义 (per AD-M1-4): 5 AND"`，紧随的 if 条件正是 5 个 AND 判据
   (`CLAUDE_EXIT_CODE==0` / `COMMIT_SHA` 非空 / `PR_URL` 非空 / `FILE_TOUCHED_HIT==true` /
   `DIFF_CONTAINS_HIT==true`)。**Spec 把 amend 目标钉在 AD-M1-4 是代码级 grounded 事实，非猜测**。
   （附带发现一条**与 R1 finding 无关的既存 drift**，见下「非阻塞观察」。）

2. **AD4 cell (`:384`) 内容确为 mislabel**——复核确认: 该 cell 引用"AD-M0-5 约定"，但
   AD-M0-5 (`:1035`) 全文主题是 handoff schema 12 字段，通篇不含 bind-mount 假设。Mislabel
   属实，且是代码库既有错误（非本 Spec 引入）。

3. **AD-M6-10 承载 C' + 单节点 scope 是否 doc 组织合理**——合理，非硬塞:
   grep 全部 `### AD-M6-*` 小节确认 AD-M6-9 是当前最后一个已用号（`AD-M6-8` 标注
   "Retired — no Phase B topic materialized"，无 `AD-M6-3`），`AD-M6-10` 确为下一可用号。
   把"C' 双通道决策"与"single-node bind-mount 假设 scope 说明"放进**同一份新 AD**（而非塞进
   AD4 或 AD-M1-4）符合既有 AD 文档惯例（六段格式独立成篇，AD4/AD-M1-4 仅做**订正引用**指向它）——
   结构清晰、无重复正文、无跨 AD 循环引用歧义。

4. **遥测依赖边仍显式**——proposal.md L11（Downstream dependency edge）+ §Out of Scope +
   tasks.md §Notes 三处措辞与 R1 核实时**完全一致，未被本轮改动触碰或稀释**。

## Rule #3 五落点交叉核对（全文件逐处扫描）

| 落点 | frontmatter (L12) | §What (F.1/F.2/F.5/F.3/F.4) | §How 表 | AC-10 | Constraints | tasks.md TG-5 |
|------|---|---|---|---|---|---|
| AD-M6-10 (New) | ✓ | ✓ F.1 | ✓ | ✓ | ✓ | ✓ 5.1 |
| AD4-cell correction | ✓ | ✓ F.2 | ✓ | ✓ | ✓ | ✓ 5.2 |
| AD-M1-4 (Amend) | ✓ | ✓ F.5 | ✓ | ✓ | ✓ | ✓ 5.3 |
| §5 (New section) | ✓ | ✓ F.3 | ✓ | ✓ | ✓ | ✓ 5.4 |
| CLAUDE.md update | — (非 AD, 不进 frontmatter 摘要属正常) | ✓ F.4 | N/A（非 AD，不进 AD 表符合体例） | ✓ | ✓ | ✓ 5.5 |

五个落点在 proposal.md 全部关键位置（frontmatter 摘要句、§What、§How 表、AC-10、Constraints）
与 tasks.md TG-5.1-5.5 **逐一对应、措辞一致、无遗漏、无新增第六项游离条目**。§How 表只列 4 行
（AD-M6-10/AD-M1-4/AD4-cell/§5）属正常体例——CLAUDE.md 更新不是 AD，不应进 AD 归属表，
它在 Constraints/AC-10/TG-5.5 三处均已登记，未被漏项。

## 已验证通过项（无问题，本轮新核）

- **AD-M6-10 编号可用性**：复核不变，仍准确（同 R1）。
- **layer-boundary-contract.md §5 落点**：复核确认现有仅到 `## §4 Error Escalation Protocol`，
  §5 不冲突。
- **DEC 原文误标未被掩盖**：proposal.md L203 明确写"DEC line 22 carried the same
  misattribution — corrected here"——诚实标注上游 DEC 文档本身的错误措辞被本 Spec 修正，
  而非静默绕过或反向指责 DEC（DEC 作为历史决策记录不应被回溯改写，此处理方式恰当）。
- **AD4 术语合规性**：`AD4`（无 `M` 前缀）确为 `architecture-decisions.md:326` 的真实合法
  小节标题（CLAUDE.md 自身引用"AD1-AD12"legacy 编号体系），Spec 使用"AD4 risk-table cell"
  措辞准确，非笔误。

## 非阻塞观察（不影响本轮 verdict，供 Phase B 执行 TG-5.3 时参考）

`architecture-decisions.md:1360` 现有 `AD-M1-4` 决策段本体记录的是**9-enum 失败分类**
（引用 `entrypoint-m1.sh` L340-537，SUCCESS 行写的是 **6** 个 AND 条件，字段名/脚本文件名
与当前 `initial.sh:524` 的 **5-AND**、脚本路径均不同）——这是代码库自身既有的 doc/code drift
（AD-M1-4 文档描述的是较早的 `entrypoint-m1.sh` 版本，当前 `initial.sh` 已演进为 5-AND），
**与 R1 finding 无关、非本 Spec 引入**，但因为 F.5/TG-5.3 恰好要编辑这同一个 AD 段落，
建议执行者在落笔前先核实 AD-M1-4 现有表格的字面内容（非凭 spec 描述的"5-AND"直接覆盖写），
避免把两代实现的条件数搞混。不构成本轮 REVISE 理由（未影响 Spec 交付项本身归属正确性），
仅作执行期提示。

## Verdict

**PASS** — R1 唯一 Major finding（AD-M0-5 amend 误归属）已完全修复，且修复方式（分离
"AD4-cell 订正" 与 "AD-M1-4 新增 amend" 两个此前被混淆的问题）经代码级核实（`initial.sh:524`
字面引用 AD-M1-4）确认比 R1 给出的任一单选项更准确、更 grounded。全文 grep 确认零处
"amend AD-M0-5 body" 残留。Rule #3 五个文档同步落点（AD-M6-10 / AD4-cell / AD-M1-4 /
§5 / CLAUDE.md）在 proposal.md 全部关键段落与 tasks.md TG-5.1-5.5 逐一对应、无遗漏、
无新误标。AD-M6-10 编号可用性、§5 落点、遥测依赖边显式性均复核不变。无 Critical/Major
新回归。1 项非阻塞观察（AD-M1-4 既存 9-enum/6-AND 文档与当前 5-AND 代码的既存 drift）
供 Phase B 执行参考，不影响本轮收敛判定。

---
checkpoint: post_spec
mode: convergence
round: 1
agent: knowledge-manager
verdict: REVISE
spec_id: aria-2.0-m6-dispatch-input-delivery
timestamp: 1783053088003
converged: false
---

# post_spec R1 — knowledge-manager 审计报告

审计对象: `openspec/changes/aria-2.0-m6-dispatch-input-delivery/{proposal.md,tasks.md}`
权威决策源: `docs/decisions/DEC-20260702-001-layer2-input-delivery-architecture.md`
代码库核实: `aria-orchestrator` HEAD `daf7c79` — `docs/architecture-decisions.md` + `docs/layer-boundary-contract.md`

## 审计范围与方法

逐项核实 (1) AD-M6-10 编号可用性; (2) AD-M0-5 amend 目标准确性 (核实 AD-M0-5 真实内容);
(3) layer-boundary-contract.md §5 落点空缺性; (4) Rule #4/#5 措辞合规; (5) DEC §待核实
4 项处置; (6) AD-M6-5 消歧声明; (7) 可追溯性链 (Spec→DEC→#147); (8) 遥测依赖边显式性。
全部对真文档 grep + sed 核实, 非凭 spec 自述采信。

## Findings

### [MAJOR][doc-sync:proposal.md §What F.2 + §How + tasks.md TG-5.2] AD-M0-5 amend 目标文档段与"prompt→bind mount, meta→小参数"约定实际不相关 — 编辑执行后会产出语义错位/误导性文档

**核实过程**: 全仓 grep `AD-M0-5` (`docs/architecture-decisions.md` 4 处命中, 无其他文件引用):
- L102、L133: 均在 **AD2** (`Layer 2 容器预装 aria-plugin`) 段内, 引用 AD-M0-5 仅指
  "`image_sha256` 是 `m0-handoff.yaml` 字段之一"。
- **L1035** 才是 AD-M0-5 **自身决策段** (`### AD-M0-5 — m0-handoff.yaml schema 锁定 12 字段`):
  全文关于 `m0-handoff.yaml` 12 字段 schema 锁定 (`spec_version/decision/t1_status/.../image_sha256/...`),
  **通篇不含 "prompt 写 bind mount, meta 传小参数" 这条约定**。
- L384 (**AD4** 风险表第 2 行, 非 AD-M0-5 段内): `"AD-M0-5 约定: prompt 写 bind mount 文件,
  meta 只传 ISSUE_ID + 小参数, M0 T2.4 实测边界"` — 这是代码库既有的**错误 cross-reference**
  (mis-citation), 该约定真实内容只出现在 AD4 自己的风险表里, 从未在 AD-M0-5 段落被决策/记录过。

**后果**: spec §What F.2 / §How 表 / tasks.md TG-5.2 / AC-10 均要求"**Amend AD-M0-5**: 把
bind-mount 假设 scope 到单节点 + backfill AD4 风险表 cross-ref"。若按字面执行, 需要往
AD-M0-5 段 (主题 = handoff schema 12 字段) 里插入一段与主题无关的"跨节点 bind-mount 假设
scope"文字 —— 这不是"修正"既有决策, 而是把从未在此处存在过的内容首次写入错误的段落,
制造新的语义错位, 且**不解决** L384 真正的 mis-citation 根因 (该引用本就指错了 AD 号)。

此错误已存在于 DEC-20260702-001 §约束条件表 / §连带文档同步 (二者同样写"amend AD-M0-5"),
本 Spec 的 §Prerequisite Verification 表只核实了 DEC §待核实 的 4 项显式待办, 未覆盖这条
隐含的 AD 编号断言 —— recon provenance (proposal.md L14) 声明覆盖"§What line-references",
未声明覆盖 §How/§F 的 AD 编号归属核实, 故此错误未被现有 recon 步骤捕获。

**Fix**: 二选一, 需 owner/spec-drafter 决定:
  (a) 放弃"amend AD-M0-5"提法, 改为**在 AD4 自身**(该约定实际唯一出处)的风险表第 2 行订正
      (标注"单节点 scope, 跨节点场景见 AD-M6-10"), 不触碰 AD-M0-5 段; 或
  (b) 若认为该约定值得升格为独立 AD 记录, 在新建的 **AD-M6-10** 内一并说明"此假设此前误标
      AD-M0-5, 实际首次决策于 AD4 风险表, 现 amend 为单节点 scope" (即用 AD-M6-10 承接修正,
      而非编辑 AD-M0-5)。
  两种做法都不应在 AD-M0-5 段落本体插入无关内容。§How 表格行、tasks.md TG-5.2、AC-10 措辞
  需同步改为准确目标 (AD4 或 AD-M6-10, 而非"Amend AD-M0-5")。

## 已验证通过项 (无问题)

- **AD-M6-10 编号可用性**: 核实 `docs/architecture-decisions.md` 全部 `### AD-M6-*` 小节
  (grep): AD-M6-1/2/4/5/6/7/9 存在, AD-M6-8 标注 "Retired — no Phase B topic materialized",
  无 AD-M6-3。Spec 声明"AD-M6-10 reserved (next available)"**准确**。
- **layer-boundary-contract.md §5 落点**: 核实现有小节仅到 `## §4 Error Escalation Protocol`
  (+ Appendix), 无 §5。Spec 新增 §5 **不冲突**。
- **AD-M6-5 消歧**: 核实 `### AD-M6-5 — Pre-flight dispatch fixture provenance (Option A/B/C)`
  确为 test-side 决策, 与本 Spec 无关。References 段消歧声明**准确**。
- **Rule #5**: Spec 落 `/home/dev/Aria/openspec/changes/` (主仓), 非 `standards/` 子模块, 也非
  `aria-orchestrator/` 内部路径。**合规**。
- **Rule #4 措辞**: §Impact / §Rollback 明确"file 模式保留是单机测试路径的保留, 非'兼容已上线
  行为'(自主从未跑通)" — 正确落实 DEC 对"向后兼容"措辞的纠正要求, 未误用。
- **DEC §待核实 4 项处置**: proposal.md §Prerequisite Verification 表逐项核对 (heavy 挂载
  local/非 NFS via `host-volume.hcl:26-29`; envsubst 5 变量白名单 `initial.sh:286`;
  `RENDERING_CONTRACT.md:61-78` + `compute-assertions.sh:94-120` 假绿确认; `issue_id TEXT`
  schema + AC-2 走 `json_extract` 非 join) —— 4 项与 DEC 原文逐条对应, 全部处置。
- **可追溯性链**: proposal.md 头部 Decision Source → DEC-20260702-001 → Aria #147 (Blocker 3,
  具体 comment 号) → handoff 文件, 链条完整无缺环。
- **遥测依赖边**: proposal.md L11 (Downstream dependency edge) + §Out of Scope + tasks.md
  §Notes 三处一致声明"本 Spec 不使 168h 跑可评分, 仍依赖独立遥测 Spec" —— 显式记录, 非隐性掉线。

## Verdict

**REVISE** — 1 项 Major (0 Critical)。文档同步交付项本身完整覆盖 Rule #3 要求的四个落点
(AD-M6-10 / AD-M0-5 amend / §5 / CLAUDE.md), 但其中 AD-M0-5 amend 目标经代码库核实**指向
错误的文档段落**, 若原样进入 Phase B 会产出语义错位的架构文档 (往 handoff-schema 主题段落
插入无关的 bind-mount scope 说明), 且未真正修正 AD4 L384 的既有 mis-citation。其余 7 项
知识管理审计点 (AD-M6-10 编号 / §5 落点 / AD-M6-5 消歧 / Rule #4/#5 / DEC 待核实处置 /
可追溯性 / 遥测依赖边) 均核实准确, 无需修订。

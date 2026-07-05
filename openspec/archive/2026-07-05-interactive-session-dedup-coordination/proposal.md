# Interactive Session Dedup — Layer L Advisory Activation + Structured Carry-ID

> **Level**: 3 (Full — 跨 aria-plugin + standards + Aria 主仓;methodology change Rule #9 Extension;既有引擎接线 [完成 TASK-024] + skill 行为变更 + 新 AB harness)
> **Status**: ✅ **Approved** (owner sign-off 2026-07-04;post_spec R3 unanimous PASS 5/5 CONVERGED;**A.3 detailed-tasks.yaml LOCKED — 20 tasks [backend-architect 8 / qa-engineer 7 / knowledge-manager 5], post_planning R5 CONVERGED**) — **ready for Phase B.1**
> **Change ID**: `interactive-session-dedup-coordination`
> **Audit trajectory** (convergence mode, 5-agent, code-grounded against `aria/` HEAD `16bcc07`):
>   - R1 (2026-07-04): **4 REVISE + 1 PASS**(backend-architect FAIL 2C / qa-engineer FAIL 1C / tech-lead + knowledge-manager PWW / code-reviewer PASS)。code-reviewer 逐行核验 12 处 file:line + 5 项 §Prerequisite 结论**全部准确无漂移** → Criticals 均为**设计缺口**非事实错误。两 Critical:(C1) 接线点 scan.py→**AI 编排层**(recon 漏读 `layer-l-integration.md:15` Design A「闸门不在 scan.py 内自动执行」,三方收敛);(C2) config 新键 `coordination_gate` 与既有 `coordination.enabled`(rule 1.54/#133 AC-2 互斥不变式)冲突 → **复用旧键 + 加 `mode` 子键**。6 Major + 11 Minor 全部落地。
>   - R2 (2026-07-04): **3 PASS + 2 REVISE**(code-reviewer PASS 0-finding [11 处修订新增断言逐行核验准确] / tech-lead + knowledge-manager PWW-PASS / backend-architect + qa-engineer REVISE)。R1 findings **全部 CLOSED**、无功能/架构 fix-introduced regression。3 新 Major:(A) Impact "机制性根治" over-claim [BA+km 收敛] → 改"可见化+有据仲裁,重复本身仍可能发生";(B) advisory 对 7b clock-skew blanket bypass 静默丢告警 [qa] → 7b 独立 surface;(C) runtime 探针防伪空心 [qa] → 结构性来源判别非自报。3 Major + 7 Minor 全部落地(见 inline R2-* 标注)。
>   - R3 (2026-07-04): **UNANIMOUS PASS 5/5**(backend-architect / qa-engineer / tech-lead / code-reviewer PASS 0-finding + knowledge-manager PWW-PASS)。R2 3 Major + 7 Minor **全部 CLOSED**(code-grounded:7b `max_clock_skew_seconds` @`:492` 经 competing_verdict 传递、探针结构性防伪与 state-checks.yaml 兼容、gitlink 无环、layer-l-integration.md 非循环),**无 fix-introduced regression**。3 纯措辞 advisory Minor(Glossary "脊柱" / Impact "病根直接消除" 范围限定 / 探针防伪自测)已折入。**CONVERGED**(R1 2C+6M → R2 0C+3M → R3 0C+0M,verdict 单调改善、无振荡)。
> **Decision Source**: [DEC-20260704-002](../../../docs/decisions/DEC-20260704-002-interactive-session-duplicate-prevention.md) (technical brainstorm 收敛;9 决策点 + Q2 中段修正「退役重建 → 接活改造」)
> **Parent methodology**: [Rule #9 session-handoff](../../../standards/conventions/session-handoff.md) §2.3 (本 Spec 补齐其 Layer L 从"P3 未接线/TASK-024 deferred"→"advisory 认领已接活")
> **Mother Spec (errata target)**: [multi-terminal-coordination](../../archive/2026-05-20-multi-terminal-coordination/proposal.md) — Layer L 2,934 行引擎所在;其 tasks.md 2.5「急切认领闸门集成」+ P3 被勾 `[x]` 但 `layer-l-integration.md` 自陈 **TASK-024 集成 = P3 deferred**、`run_gate` scan.py 零调用(死代码 on-arrival,见 [aria-plugin #95](https://forgejo.10cg.pub/10CG/aria-plugin/issues/95))
> **Affected Skills**: `state-scanner`(**阶段 2 推荐 / Phase B-entry AI 编排层**接线 run_gate [完成 TASK-024] + phase1_gate block→advisory + runtime 探针)+ `phase-d-closer` / `session-closer`(handoff-write 改用 identity.py)
> **Affected Repos**:
>   - aria-plugin(state-scanner AI 编排层接线 + phase1_gate advisory + `aria/templates/session-handoff.md` §6 skeleton [**子模块 track,非主仓**] + handoff-write identity 接入 + AB harness + runtime 探针)
>   - standards(session-handoff.md §2.3 结构化 carry-id schema + Rule #9 Extension 更新)
>   - Aria 主仓(CLAUDE.md Rule #9 Extension 段 + 母 spec archive ERRATA.md + `.aria/config.json` dogfood 启用 + dogfood)
> **Scope**: 落主仓 `openspec/changes/` per Rule #5(project change,不放共享 submodule);实现代码落 aria/ 子模块。
> **Related Issues**: 关闭 [#94](https://forgejo.10cg.pub/10CG/aria-plugin/issues/94)(双子星防重复失效)核心;部分回应 [#95](https://forgejo.10cg.pub/10CG/aria-plugin/issues/95)(勾选≠运行,决策点 6/7 是其具体修法示范,系统性修复独立排期)。
> **Recon provenance**: DEC §待核实 5 项 + R1 补 2 项(layer-l-integration.md Design A / coordination.enabled 既有键)全部 code-grounded,行号 verified against `aria/` 子模块 HEAD `16bcc07`(2026-07-04)。

---

## Why

2026-07-04 双子星(`dev-claude` + `dev-claude2` 两个并行交互 session)各自独立做了一整套 Blocker3 Spec+A.3,数小时后 git push 才发现重复。排查暴露一个**双层病理**:

**1. 病根 — carry-forward 是无主、无稳定 id 的共享待办队列。** 两 session 读同一份 handoff §6 的**自由文本** carry-forward("⭐ Blocker3 → 起 Level 3 OpenSpec"),各自解读为"我该做这个"。就算认领机制完美,也无从判定两 session 在做"同一件事"—— 因为"同一件事"没有稳定标识符。

**2. 次因 — Aria 本就为此造过防护,但从没接线(死代码 on-arrival)。** `multi-terminal-coordination`(DEC-20260519-001,v1.22.0)ship 了 Layer L:急切认领闸门 `phase1_gate.run_gate()` + orphan ref `refs/aria/coordination` + 确定性 reconcile,**2,934 行有测试的完整引擎**。但 recon 确认 `run_gate()` **零生产调用点**(scan.py / collectors / config 全无 import 或 call —— 仅注释/doc 引用;组件测试覆盖 reconcile/race 但 run_gate 编排器**无直接单测**)。集成本是 `layer-l-integration.md` 记的 **TASK-024(P3 deferred,从未做)**,而母 spec tasks.md 2.5「急切认领闸门集成 state-scanner」却被勾 `[x]` —— 归档标记与设计文档自相矛盾,是 #95「勾选完成 ≠ 运行现实」的活样本。

**3. 加剧 — 身份靠 AI 手填 → 漂移。** handoff frontmatter 的 `owner-container` 字段由 AI 手动组装(模板注释 `session-handoff.md:33-40` 指示手填),recon 实测 `docs/handoff/*.md` 出现 **6 种不一致值**:38× `simonfishgit/dev-claude` / 22× `simonfish/dev-claude` / 8× 裸 `dev-claude` / 3× `simonfish/dev-claude2` / 3× 裸 `dev-claude2` / 1× 裸 UUID。**同一物理容器漂移出 3 种主串**,直接破坏 §2.3.5 的 cross-owner vs self-multi-container collision 分类 —— 看板会把同一人误判成多 owner。讽刺的是机械生成能力**已存在但未接入 write 路径**(`identity.py::Identity.owner_container` 只被 phase1_gate 消费)。

本 Spec 不退役、不重建。把 Layer L 从"死代码"接活成"活代码 advisory 认领"(**完成 TASK-024 集成 + advisory 改造**):复用其 identity/reconcile/lifecycle 引擎,改 5 处 + 加 carry-id 稳定标识 + 加 AB harness 科学定夺 trigger + 加 runtime 探针防再次烂成死代码。哲学恪守 DEC-20260519-001 #1 **advisory-over-hardlock**(可见可对账优于硬锁)。

---

## What

五处接活改造(§1-5:接线 / block→advisory / carry-id / 稳定身份 / runtime 探针)+ AB 定夺链路(§6)。底座仍只有 git remote,全 advisory、最终一致。

### 1. 接线 — AI 编排层调用 `run_gate()`(完成 TASK-024,非 scan.py)

**接线点 = state-scanner 阶段 2 推荐 / Phase B-entry AI 编排层**,**不是** `scan.py`(R1-C1 修正)。依据 `layer-l-integration.md:15` Design A:**"闸门仅在用户确认要进入 Phase B 时调用,不在 scan.py 内自动执行"**;`:44` acquire_claim 时机 = "Phase B 启动前"。`scan.py` 是 stdlib-only 只读机械 collector(无 `user_decision`/无 stdin/无 push),而 `run_gate` 交互式 + 有远端副作用(写 claim + push);且 `raw_track_id`(carry-id)在用户选定 track **之后**才存在,scan.py 在选 track 前跑,时序上拿不到。

调用时序(对齐 `layer-l-integration.md`):
```
scan.py → snapshot (含 tracks_multibranch.collision.kind)
  → 阶段 2 推荐 (AI 读 snapshot + 读 §6 选定 carry-id)
  → 用户确认进入 Phase B (phase-b-developer B.1 / branch-manager)
  → AI 编排层调用 run_gate(raw_track_id=<carry-id 原始串>, phase="B", ...)
```

- **config 触发键 = 复用既有 `state_scanner.coordination.enabled`**(R1-C2 修正,**不新建** `coordination_gate`)。该键已存在(`advanced-rules.md:531-566` rule 1.54 / `layer-l-integration.md:12`),`enabled==true` 语义本就是"cross-owner collision 由 phase1_gate 处理"。新增子键 `state_scanner.coordination.mode: advisory|block`(默认 advisory)控制 outcome 姿态。#133 AC-2 互斥不变式(rule 1.54 iff `enabled==false` / phase1_gate iff `enabled==true`)**不受影响** —— mode 与 enabled 正交,仅 `enabled==true` 时相关。
- 这是本 Spec 的**首要交付** —— 引擎已全建好(`run_gate` @ `phase1_gate.py:272`),缺的是 TASK-024 从未落地的集成 caller。

### 2. block→advisory — 翻转 outcome 策略(不碰 reconcile;放行仍写 claim)

现 `run_gate` 的 outcome 由 `user_decision` 回调驱动:占用(`phase1_gate.py:517` 7c)/时钟偏移(`:476` 7b)/push 失败(`:640` step9)默认走 abort/yield/block。改造 = 新增 `mode` 参数,advisory 下:

- **advisory 放行 = 跳过 `_call_decision` 的 abort/yield 语义,像 7d takeover-eligible 分支一样无条件执行 step 8/9(`acquire_claim` @ `:573` + `resilient_push` @ `:640`)写入并推送自己的 claim,额外返回/记录一个 surface 标记**(R1-M1 修正)。**关键:放行必须写 claim** —— 否则"reconcile 仍是最终仲裁"是空话(无第二条 claim 供仲裁、无审计痕迹、AB harness 的 `collision_surfaced` 无所指)。第二 session 事实上带 `status=active` claim 进 Phase B(与 #94 结果同,但这次**可见 + 有据仲裁**),符合 advisory-over-hardlock。
- **surface 内容按分支分化,不 blanket 静默**(R2-Major-B):"放行"移除的只是 abort 动作,**不移除告警面**。两种 surface 措辞:
  - **7c 占用(`:517`)**:🔴 "`<owner/container>` `<age>` 前已认领 `<carry-id>`",**回显供逐字 copy 的精确 carry-id 串**(R1-m5,减少转录漂移)。
  - **7b 时钟偏移(`:476`,原注释"highest risk")**:🔴 "⚠️ 时钟偏移 `<skew>`s(> 30s 阈值)—— reconcile winner 判定可能有误,请检查容器时钟同步"。**须保留** `_call_decision` context 里的 `max_clock_skew_seconds` 信号(advisory 只改"是否 abort",不改"是否告警"),否则 advisory 在最危险路径上比 block 更沉默。
- **reconcile 语义(winner 判定)与 surface 语义(告警面)是两回事**:advisory 改的是 outcome 的 abort 动作 + 告警呈现方式(推荐区显示而非交互 prompt),**不改** reconcile winner 判定,**也不移除** clock-skew 告警信息本身。
- **reconcile 仍是最终仲裁**(earliest `claimed_at` 胜,定义 `reconcile.py:163`,调用点 `phase1_gate.py:415`),outcome 策略(7b/7c/step9)与 reconcile winner 判定**正交**(§Prerequisite #4),改 advisory 零 reconcile 副作用。

### 3. 结构化 carry-id — 认领 key 根治病根

handoff §6 "Next session 优先级" 的每条 carry-forward 从**自由文本** → 带**稳定 slug** 的 `{id, desc}`:写交接时给稳定 id(如 `carry-m6-blocker3-spec`),两 session 读同一 handoff = 同一 id = 认领必撞。

- **carry-id 约定用 `-` 不用 `:`**(recon 修正 DEC:`derive_track_id` 替换表 `track_id.py:28` 只译 `/ . _ → -`,**不译 `:`**;DEC 原例 `carry:...` 冒号会被保留)。track_id 仅作 YAML scalar + reconcile 分组键(非 git 路径,claim 路径是 `claims/<container>/<session>.yaml` 见 `coordination_ref.py:787`),`:` 低风险但约定用 `-`。
- **归一化职责在 `run_gate` 内部**(R1-m6 修正):调用方把 carry-id **原始串**作 `raw_track_id` 传入,`run_gate` 第 `:354` 行内部调 `derive_track_id(raw_track_id)` 归一;调用方**不**预先归一(避免消费端重复实现归一逻辑)。
- **carry-id 与 frontmatter `track-id` 的关系**(R1-M5):模板 `track-id`(`:23-24`)本就声明"与 carry-forward 条目 1:1 绑定"。当 §6 某 carry-id 与本 handoff 的 doc-level `track-id` 指同一份工作时,**两者取相同原始串**(推荐直接复用 frontmatter track-id 作该条目 carry-id)—— 否则同一工作被算两条不相关 track,削弱"认领必撞"。**约定例外**(R2-Minor):复用 track-id 时不强制 `carry-` 前缀(track-id 如 `multi-terminal-coordination` 本无前缀);`carry-` 前缀仅是**新起** carry-id 时的可读性约定,`derive_track_id` 对两种形式都确定性归一。
- **carry-id 留 §6 prose,不进 frontmatter**(recon 硬约束,§Prerequisite #5):handoff frontmatter 用 stdlib flat-only 解析器(`handoff.py:206-209`),嵌套/list 结构 → 返回 None → **整个 doc 退化 legacy(owner=unknown)**,重演漂移。§6 prose 加 `{id, desc}` 零风险(无 collector 解析 body,`handoff.py` 只读顶部 frontmatter 5 字段)。
- **与既有 §2 carry_forward_inventory 机读通道的分工**(R1-M5):项目已有机读 carry-forward 通道(`collectors/openspec.py:235-249` 从各 active `tasks.md` inline 注解提取 → `carry_forward_inventory` → `handoff_autofill.py` 自动汇入 §2)。本 Spec **只做 §6**(human-curated top priority);**§2 autofill 通道(体量最大的 carry-forward 来源)的 id 化留作 #95 系统性修复 / 独立 follow-up**(见 Out of Scope)。明确划界防"以为已根治但漏了大头"。
- **gate 消费 = human-in-the-loop**:无 collector 解析 §6;开工时 AI/人读 §6 选定 carry-id,手动喂 `run_gate`。符合 advisory 哲学(决策前必经推荐区,非自动拦截)。

### 4. 稳定身份 — handoff-write 改用 `identity.py::get_identity()`

handoff frontmatter `owner-container` 从 AI 手填 → 写入时调用 `get_identity().owner_container`(`identity.py:67-70`,返回 `f"{owner}/{container_id}"`)。修复代码本就存在:`owner`=git email local-part(`get_owner`),`container_id`=`~/.aria/container-id` 持久 8-hex UUID(`get_container_id`,recon 确认首调自动生成 + 原子持久化,不可写才 fallback hostname)。接入点 = `phase-d-closer` D.3 / `session-closer` step4 / 或机械化到 `handoff_autofill.py`。根除 6-变体漂移。

### 5. runtime-invocation 探针 — 防再次烂成死代码(#95)

新增 custom-check / 遥测,验证 `run_gate()` **生产真被调用**(非只"代码存在 + 单测过")。探针**依赖 §What.6 埋点 `.aria/coordination-telemetry.jsonl` 的来源字段**区分"生产调用"vs"测试/harness 调用"(R1-m1)。

**防伪机制 = 结构性判别,非调用方自报**(R2-Major-C,防探针本身空心假绿):来源字段**不可由调用方参数覆盖**,否则 harness 单跑一遍就能把自己标成 production → 零生产 dogfood 也能让探针 PASS(正是本 Spec 引用的 `feedback_noop_in_test_env_hardening_needs_mechanism_assertion` + `feedback_telemetry_verify_records_in_prod_not_just_code_exists` 警告的假绿)。具体形状二选一(A.2 定):
  - **(a) 双入口分区**:生产走 `run_gate()`,harness 强制走显式 wrapper(如 `run_gate_synthetic()`),两者写入 telemetry 不同分区,探针只读生产分区;
  - **(b) 不可覆盖运行时证据**:source 字段由调用栈 frame 是否源自已知生产模块路径(`state-scanner` AI 编排层 / `phase-b-developer`)派生,而非一个可传参覆盖的 boolean。
探针 PASS 判据 = 生产分区有**新近**(时间窗口)记录,非"文件里有过 claim_written 就算数"。这是 #95「勾选≠运行」的具体修法示范。

### 6. AB 定夺链路 — trigger(auto/semi/manual)科学选(决策点 8)

claim 触发点(全自动 / 半自动确认 / 手动)标 **pending**,走遥测 + 合成双-session harness AB(见 §AB Test Plan)。**manual/opt-in arm(AI/人显式喂 carry-id,符合 §What.3)= P1 交付的 live arm**(R1-M2):runtime 探针(§What.5)断言的即此 arm 的生产调用,使"接线活了"与"trigger pending"自洽;auto/semi 明确划到 AB-pending。

### Key Deliverables

- `aria/skills/state-scanner/` **阶段 2 推荐 / Phase B-entry AI 编排层**(SKILL.md)— 接线 `run_gate()`(完成 TASK-024;opt-in `coordination.enabled` gate;manual arm)
- `aria/skills/state-scanner/references/layer-l-integration.md`(**live 设计文档 doc-sync**,R2-Minor):把 "P3 TASK-024 将把...集成"(未来时)+ ":12 要求 reconcile 后再 claim"(advisory 默认下失真)更新为"TASK-024 已完成 / advisory 接活";否则同一文档家族内重演本 Spec §Why.2 批判的"归档标记与设计文档自相矛盾"(#95 自我拆台,Rule #3)
- `aria/skills/state-scanner/scripts/phase1_gate.py` — `mode` 参数 + advisory outcome(放行仍写 claim)+ 🔴 surface 输出契约(回显 copy-able carry-id)
- `aria/skills/state-scanner/` — carry-id → gate 的 Phase 2 消费路径(原始串喂 run_gate 内部归一)+ runtime 探针(带来源判别字段)
- `aria/templates/session-handoff.md`(**aria-plugin 子模块 track**)— §6 加 `{id, desc}` carry-id skeleton(prose 层)
- `aria/skills/phase-d-closer/references/handoff-mechanics.md` + `phase-d-closer` D.3 / `session-closer` step4 — handoff-write 调 `get_identity()` 填 owner-container
- `standards/conventions/session-handoff.md` — §2.3 结构化 carry-id schema(§6 prose 层)+ Rule #9 Extension 更新
- `.aria/config.json` schema — **复用** `state_scanner.coordination.enabled` + 新增 `state_scanner.coordination.mode`(config-loader 默认 mode=advisory)
- AB harness — 合成双-session dedup 检出实验(`.aria/coordination-telemetry.jsonl` 埋点 + 4 臂 + 时序模型可造 collision_missed + 预注册决策规则)
- 母 spec archive `ERRATA.md`(TASK-024 集成 deferred + 2.5/P3 标记失真)+ CLAUDE.md Rule #9 Extension 段新增 + Aria 主仓 `.aria/config.json` dogfood 启用
- Aria 主仓 dogfood + Rule #6 substitute(structural + runtime-invocation 断言)

---

## Prerequisite Verification（DEC §待核实 5 项 + R1 补 2 项 — code-grounded recon 结论）

> 按 memory `feedback_spec_inherits_upstream_dec_errors`:据 Approved DEC 起草的 spec 会原样继承 DEC 自身代码级错误;起草前 recon DEC 每处断言。R1 code-reviewer 逐行核验本表 12 处 file:line + 5 项结论**全部准确无漂移**;R1 补齐 recon 漏读的 2 项(#6/#7)。

| # | 待核实项 | Recon 结论(HEAD `16bcc07`) | 对 spec 的影响 |
|---|-------------|---------------------------|--------------|
| 1 | `~/.aria/container-id` bootstrap | ✅ `get_container_id()`(`identity.py:191-244`)首调自动生成 8-hex UUID(`secrets.token_hex(4)`)+ `.tmp`→`os.replace` 原子持久化;不可写才 fallback hostname。无需 owner 预置;双子星两容器各自文件 → 天然不同 id | 直接用,无 bootstrap task |
| 2 | `derive_track_id(raw)` 归一 | ✅ 纯确定性(lower→`/._`译`-`→trunc64→sha256 fallback,`track_id.py:61-170`)。**替换表 `:28` 不含 `:`** | **修正**:carry-id 约定用 `-`;归一在 run_gate 内部(`:354`) |
| 3 | `refs/aria/coordination` 激活 | ✅ 引擎完整(`coordination_ref.py` bootstrap/read/write/push/fetch);claim 路径 `claims/<container>/<session>.yaml`(`:787`,**container 是路径,track_id 不是**);`coordination_fetch` collector 已 fetch(常量 `:96`,fetch 逻辑见 collector 主体) | "激活"=接线消费,非重建 |
| 4 | block→advisory 对 reconcile | ✅ `reconcile()`(定义 `reconcile.py:163`,调用点 `phase1_gate.py:415`)纯 winner 判定(earliest `claimed_at`),与 gate outcome 策略(7b/7c/step9)**正交** | 改 advisory 零 reconcile 副作用;放行仍写 claim(§What.2) |
| 5 | 结构化 carry-id 模板 + 向后兼容 | ✅ §6 纯 prose 无 skeleton(模板 `:181-197`);frontmatter stdlib 解析器只吃 flat `key:string`(`handoff.py:206-209`),嵌套→None→**doc 退化 legacy**;collector 只读顶部 5 字段不解析 body | **硬约束**:carry-id 留 §6 prose;新 frontmatter 字段须扁平 string + 同步 #137 grep(`==5`)+ `_FRONTMATTER_REQUIRED_KEYS` frozenset(本 Spec 不加 frontmatter 字段,grep 不变) |
| **6** | **接线点(R1-C1 补)** | ✅ `layer-l-integration.md:15` Design A:**"闸门仅用户确认进 Phase B 时调用,不在 scan.py 内自动执行"**;`:44` acquire_claim 时机="Phase B 启动前";集成=**TASK-024 P3 deferred**(从未做) | 接线点 = AI 编排层(阶段 2/Phase B-entry),非 scan.py(§What.1) |
| **7** | **config 既有键(R1-C2 补)** | ✅ `state_scanner.coordination.enabled` 已存在(`advanced-rules.md:531-566` rule 1.54 / `layer-l-integration.md:12`),承载 #133 AC-2 互斥不变式(rule 1.54 iff `false` / phase1_gate iff `true`) | **复用**该键 + 加 `coordination.mode` 子键;不新建 `coordination_gate`,#133 AC-2 不受影响(§What.1) |

**佐证死代码事实**:`grep run_gate(` 全 skill 零生产调用点 + **无 run_gate 编排器直测**(组件测试覆盖 reconcile/race)→ 更坐实死代码,task 1.5 golden test 将是 run_gate 首个直测。`.aria/config.json` 无 `coordination_gate` 键(确认无同名新键)。

---

## 锁定决策（引用 DEC-20260704-002）

| # | 决策 | 来源 |
|---|------|------|
| 1 | 执行姿态 = 响亮 advisory(非 block、非纯约定);第二 session 领同 carry-id → 推荐区 🔴 显眼提示(回显 copy-able id),非阻塞但必看到 | DEC-002 决策点 1 (Q1) |
| 2 | 承载 = 接线并改造 Layer L(复用 2,934 行引擎,完成 TASK-024,不退役不重建) | DEC-002 决策点 2 (Q2 修正) |
| 3 | 认领 key = 结构化 carry-forward id(§6 自由文本 → `{id, desc}` 稳定 slug,原始串喂 run_gate) | DEC-002 决策点 3 (Q4) |
| 4 | 稳定身份 = handoff-write 改用 `identity.py::get_identity()`(根除手填漂移) | DEC-002 决策点 4 |
| 5 | block→advisory:`run_gate` 末步"拦截"→"响亮 surface + 放行(仍写 claim)";reconcile 仍仲裁,输方是提示非 abort | DEC-002 决策点 5 |
| 6 | 接线:**AI 编排层**调 `run_gate()`(opt-in `coordination.enabled`,默认 off;Aria 主仓 dogfood 显式启用) | DEC-002 决策点 6 (R1-C1/M3 修正落点) |
| 7 | runtime-invocation 探针:验 `run_gate()` 生产真被调用(带来源判别,防再死代码) | DEC-002 决策点 7 |
| 8 | claim 触发点(auto/semi/manual)= AB 定夺;**manual arm = P1 live arm**,auto/semi pending | DEC-002 决策点 8 (Q3) + R1-M2 |
| 9 | surfacing 通道 = state-scanner 阶段 2 推荐区(与 Layer H 看板同位);coordination ref 账本继续作 claim 存储(激活非新建) | DEC-002 决策点 9 |

---

## Impact

| Type | Description |
|------|-------------|
| **Positive** | 双子星重复工作**可见化 + 有据仲裁**(§6 human-curated 通道,即触发本 Spec 的实际事故场景;carry-id 认领必撞 + 响亮 advisory)—— **重复工作本身仍可能发生**(advisory 不阻塞),但不再是数小时后靠 git push 才发现;#94 就此维度闭环;**病根**(§6 carry-forward 无稳定 id)由 carry-id **直接消除**(§2 机读通道覆盖留 follow-up,见 Risk 表);#95 死代码修法示范(完成 TASK-024);owner-container 6-变体漂移根除;单 session 用户体感≈零变化(opt-in gate + 单 track 无 collision) |
| **Risk: 接活又烂成死代码** | **缓解**:runtime 探针(决策点 7,带来源判别)每扫描验 `run_gate` 真被调 + AB harness 量生产检出率,非只 structural benchmark;Aria 主仓 dogfood 显式 `coordination.enabled: true` 使探针从第一天有真实调用对象 |
| **Risk: config 既有键 #133 AC-2 回归** | **缓解**:复用 `coordination.enabled` 不新建键;mode 与 enabled 正交(仅 enabled==true 相关);不改 rule 1.54 disjointness |
| **Risk: carry-id 进 frontmatter 触发 legacy 退化** | **缓解**:硬约束 carry-id 留 §6 prose;grep `==5` 不变 |
| **Risk: carry-id 覆盖面缺口(只覆 §6 不覆 §2 机读通道)** | **缓解**:§What.3 显式划界 §6(human)vs §2 carry_forward_inventory(machine);§2 id 化留 #95/follow-up,防"以为已根治漏大头" |
| **Risk: advisory 逐字转录漂移(读到 id 却喂错串)** | **缓解**:surface 回显 copy-able 精确 id;稳定 slug 可 copy;"§6 carry-id 逐字喂"列为 AB harness 检出率量化的失败模式之一 |
| **Risk: advisory 仍被无视(人/AI 忽略 🔴 提示)** | **缓解**:🔴 显眼 + 放推荐区(决策前必经);advisory 上限即此,接受(DEC-20260519-001 #4) |
| **Risk: AB 拿不到信号(重复涌现稀有)** | **缓解**:合成双-session harness 时序模型确定性造重叠 carry-id + collision_missed 失败案例,不靠碰运气 + 真实用量遥测并行 |
| **Risk: state-scanner 行为变更触发 Rule #6** | 按 **structural + runtime-invocation** substitute(非 LLM with/without):测 gate 接线真被调 + carry-id 撞检确定性 + advisory surface 正确性 + handoff identity 无漂移。per memory `feedback_deterministic_structural_skill_rule6_substitute` + `feedback_completion_signals_vs_runtime_invocation` |
| **Risk: 时钟偏移误判 winner + advisory 静默降级** | reconcile 检测同 track 时间戳偏差 > `CLOCK_SKEW_WARN_THRESHOLD` 30s(`constants.py:47` / `phase1_gate.py:476`)。**advisory 改造须保留 7b 告警面**(R2-Major-B):block 模式下 `_call_decision` 是唯一暴露"偏移 → winner 可能有误"的通道;advisory 若 blanket bypass 会静默丢弃此信号 → 在最危险路径上比 block 更沉默。**缓解**:§What.2 为 7b 定义独立 surface(skew 秒数 + "查时钟"),advisory 只改 abort 动作不改告警呈现;reconcile winner 判定逻辑本身不改 |
| **Risk: Rule #7 secret-hygiene** | claim 内容仅非敏感身份元数据(container-id / session-id / 时间戳),不涉 secret value;沿用母 spec 判定,Rule #7 不适用 |

---

## Out of Scope

- **#95 系统性修复**(archive gate 交叉核对 tasks.md vs 成功标准 + `[x]` 真实性抽验 + **pre-#134 孤儿 sweep** 审所有 2026-06-10 前归档 spec 运行时真实性)—— 本 Spec 只做 #95 的**具体修法示范**(完成 TASK-024 接活 + runtime 探针),系统性修复独立排期。
- **§2 carry_forward_inventory 机读通道 id 化**(体量最大的 carry-forward 来源)—— 本 Spec 只 id 化 §6 human-curated 条目;§2 通道(tasks.md inline 注解,已有 change_id 作天然 key)的稳定 id 留 #95 / 独立 follow-up。
- **AB trigger 最终选择的实施**—— 本 Spec 交付 AB harness + 埋点 + 预注册决策规则,manual arm 作 P1 live arm,auto/semi 标 pending;跑 AB + 据结果落地某臂是 follow-up(避免未测先定,per memory `feedback_static_benchmark_unfit_as_oneshot_selection_gate`)。
- **跨容器硬锁 / 强一致**—— DEC-20260519-001 #1 明确否决(advisory-over-hardlock;身份漂移会自拦自)。
- **auto-memory 跨容器分叉**—— 母 spec 已列 out-of-scope,与本 Spec 两目标(防重复 + 稳定身份)不直接相关。
- **Layer H 看板本身**—— 已 ship 且在跑(state-scanner Phase 1.16/1.17),本 Spec 只补 Layer L 接活,不改看板重建逻辑。

---

## Success Criteria

- [ ] **AI 编排层**(阶段 2/Phase B-entry)在 opt-in `coordination.enabled=true` 下真调用 `run_gate()`(manual arm,carry-id 原始串入参);runtime 探针据**结构性来源判别**(不可被调用方参数覆盖:双入口分区 或 调用栈 frame 派生)的遥测断言**生产分区有新近记录**(非只单测、非 harness 自报可伪造);Aria 主仓 `.aria/config.json` 设 `coordination.enabled: true` 作 dogfood 闭环
- [ ] `run_gate` advisory 模式:检测他人 fresh claim → 🔴 surface(回显 copy-able carry-id)+ **放行且执行 step 8/9 写自己 claim**;golden test 断言 advisory occupied 路径 `own_claim != None` 且真调 acquire_claim/push;block 模式保留原 abort/yield;reconcile winner 判定不受 mode 影响
- [ ] advisory 分支分化 surface:7c 占用 = "已认领"措辞;**7b 时钟偏移 = 独立 surface(skew 秒数 + "查时钟",不 blanket 静默)**;golden test 断言 advisory 7b 路径仍暴露 `max_clock_skew_seconds` 告警(非只放行)
- [ ] handoff §6 skeleton 支持 `{id, desc}` carry-id(prose 层);carry-id 原始串喂 `run_gate` 内部归一;约定用 `-` 不用 `:`;当与 frontmatter track-id 指同一工作时取相同串
- [ ] carry-id 留 §6 prose:回归测试断言加 carry-id 后 `handoff.py` frontmatter 解析仍取 5 字段、doc 不退化 legacy;未打标旧 §6 行不触发 gate 消费(定义清楚)
- [ ] handoff-write 调 `get_identity().owner_container`:dogfood 新 handoff 的 owner-container = `<owner>/<container_id>` 机械生成,非手填;两容器产出不同 container_id(home_dir 注入测试)
- [ ] AB harness:合成双-session 时序模型确定性造重叠 carry-id + **至少一种 collision_missed 失败案例**(并定义其**检出侧** —— harness 事后对比 ground-truth 是否真有 2 并发 claim 后补写该记录);量每臂(auto/semi/manual/control)检出率;预注册阈值(检出≥90% / 假阳性≤5% / 摩擦 **≤500 token/认领**)
- [ ] Rule #6 substitute(structural + runtime-invocation)通过 + human review 确认真接活(非勾选绿)
- [ ] Aria 主仓 dogfood:本机制实际承载 ≥1 双子星并发场景,carry-id 认领撞车被检出且 surface(可证伪)
- [ ] 母 spec archive `ERRATA.md`(TASK-024 集成 deferred + 2.5/P3 标记失真,不改归档 `[x]`)+ CLAUDE.md Rule #9 Extension 段**新增**接活说明(现状未提缺口,是新增非替换)
- [ ] #94 关闭(接线 + 身份 + carry-id + advisory 四项落地);#95 部分回应(runtime 探针范式)记录

---

## AB Test Plan（决策点 8 的科学定夺，per memory `feedback_static_benchmark_unfit_as_oneshot_selection_gate`）

- **① 埋点**(append-only JSONL `.aria/coordination-telemetry.jsonl`,可汇总到共享 coordination ref):`claim_written` / `collision_surfaced`(+latency)/ `collision_missed`(事后才发现的重复 = 失败指标)/ `false_positive` / `claim_friction`(steps/tokens)。每条打 **arm** 标签 + **来源/环境判别字段**(non-harness / 时间窗口,供 runtime 探针区分生产 vs 测试)。
- **② 指标**:检出率 = surfaced/(surfaced+missed)[首要] · 假阳性率 · 摩擦(≤500 token/认领)· 检出时延。
- **③ 实验臂**:trigger 三变体(auto / semi / manual)+ control(不认领 = 现状);**manual = P1 交付的 live arm**,auto/semi pending。
- **④ 信号来源 + 时序模型**(R1-M2):合成双-session harness 须有**明确时序模型**(session B 在何时点检查/跳过 gate、相对"已完成多少工作"),以便人为构造 `collision_missed`(某臂刻意不在 A 完成前调 gate = 复现 #94 未触发场景),而非只测"if called → will detect"的 trivial 100% 检出。真实用量遥测并行长期验证。
- **⑤ 决策规则预注册**:跑前先定阈值(检出≥90% / 假阳性≤5% / 摩擦≤500 token/认领),避免事后找理由。

---

## Glossary（本 Spec 新增/复用术语）

| 术语 | 一句话定义 | 示例 |
|------|-----------|------|
| `carry-id` | handoff §6 每条 carry-forward 的稳定 slug(`{id, desc}` 的 id),两 session 读同一 handoff 得同一 id;与 doc-level frontmatter `track-id` 指同一工作时取相同串 | `carry-m6-blocker3-spec` |
| frontmatter `track-id` | handoff 顶部 doc-level 工作 id;`standards/conventions/session-handoff.md §2.3.1`(`:115`)声明"与 carry-forward 条目 1:1 绑定";单 doc 一个。(注:母 spec `proposal.md` Glossary 把 track-id 定位为**"脊柱"**—— 跨 Layer H frontmatter / Layer L reconcile 分组键 / Design A worktree 路径键**统一使用**;本 spec 沿用同一 `derive_track_id` 派生函数,应用域[handoff frontmatter vs carry-id]不同,非矛盾) | `multi-terminal-coordination` |
| `advisory 模式` | gate 检测撞车不 abort,改 🔴 surface + 放行(**仍写 claim**);reconcile 仍仲裁,输方是提示 | `coordination.mode: advisory` |
| `runtime-invocation 探针` | 验 `run_gate` 生产真被调用的 custom-check/遥测(带来源判别),防死代码 | — |
| `run_gate` | Layer L 急切认领闸门主函数(`phase1_gate.py:272`),本 Spec 由 AI 编排层首次接线(完成 TASK-024) | — |
| `owner_container` | `identity.py::Identity` property `f"{owner}/{container_id}"`,handoff frontmatter 身份 | `simonfishgit/023236f2` |

---

## References

- 决策记录: [DEC-20260704-002](../../../docs/decisions/DEC-20260704-002-interactive-session-duplicate-prevention.md) + 母决策 [DEC-20260519-001](../../../docs/decisions/DEC-20260519-001-multi-terminal-coordination.md)
- 母 Spec(Layer L 引擎 + errata 对象): [multi-terminal-coordination](../../archive/2026-05-20-multi-terminal-coordination/proposal.md);集成设计意图 `aria/skills/state-scanner/references/layer-l-integration.md`(TASK-024 接线点)
- 母 Spec 勘误(归档后回溯纠错,TASK-015): [ERRATA.md](../../archive/2026-05-20-multi-terminal-coordination/ERRATA.md) —— 标注母 spec tasks.md 2.5 + P3 勾 `[x]` 但 TASK-024 集成实际 deferred、`run_gate` 零调用,现由本 Spec 接续(双向链接回本 proposal)
- 相关约定: [Rule #9 session-handoff](../../../standards/conventions/session-handoff.md) §2.3;既有 config key + 互斥不变式 `aria/skills/state-scanner/references/rules/advanced-rules.md` rule 1.54(#133 AC-2)
- 关联 Issue: [#94](https://forgejo.10cg.pub/10CG/aria-plugin/issues/94)(双子星防重复失效)/ [#95](https://forgejo.10cg.pub/10CG/aria-plugin/issues/95)(勾选≠运行病根)
- 事故 handoff: [`2026-07-04-dedup-coordination-brainstorm-dec.md`](../../../docs/handoff/2026-07-04-dedup-coordination-brainstorm-dec.md)
- 关联 memory(local-only,非 git-tracked): `feedback_completion_signals_vs_runtime_invocation` / `feedback_read_dormant_code_before_recommend_rebuild` / `project_dev_claude2_parallel_session` / `feedback_concurrency_advisory_over_hardlock` / `feedback_spec_inherits_upstream_dec_errors` / `feedback_code_grounded_multiagent_review_catches_altitude_misses` / `feedback_noop_in_test_env_hardening_needs_mechanism_assertion`

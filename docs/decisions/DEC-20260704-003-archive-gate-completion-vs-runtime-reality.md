# 决策: DEC-20260704-003 — 归档 gate 硬化 (完成 vs 运行现实) 范围界定

> **日期**: 2026-07-04 | **模式**: requirements (brainstorm, 范围界定) | **范围**: aria-plugin (openspec-archive + phase-d-closer + spec_complete.py + collectors/openspec.py) | **spec_level**: Level 3 (预估)
> **状态**: Approved (brainstorm 收敛; post_brainstorm 审计门 off) — **含 Amendment 1 (2026-07-04 post_spec R1: B 化入 C, C 分级; 见文末 §Amendment 1)**
> **触发**: [aria-plugin #95](https://forgejo.10cg.pub/10CG/aria-plugin/issues/95) — 2026-07-04 双子星重复事故 (#94) 归档考古挖出的更深流程病根: **"完成"是勾出来的, 不是跑出来的**。Layer L (`phase1_gate`, 2,934 行有测试引擎) 归档 spec 标 `[x]` 完成却从没接线, 归档关闭后无 open tracker, 直到本次事故才被翻出。

## 背景

`multi-terminal-coordination` (archived 2026-05-20) 的 `2.5 急切认领闸门集成 state-scanner` 任务被 tasks.md 打 `[x]`, 但 proposal 成功标准同项 `[ ]` 没勾 (自相矛盾), 且 `scan.py` 全历史零 import/调用 `phase1_gate` (集成从没在代码发生)。单测 108 过 + structural benchmark 过 → 给了 "done" 假信号, 却无任何机制验证代码在生产流程真被 invoke。

issue #95 归纳为**一类系统性流程瑕疵** (Layer L 是症状), 5 病根 + 5 建议修复 A-E:
- **A** runtime-invocation 探针 (死代码 on-arrival 拦截)
- **B** archive gate 交叉核对 tasks.md `[x]` vs proposal 成功标准 `[ ]`
- **C** `[x]` 真实性抽验 (集成/dogfood/benchmark 类须有可核实产物)
- **D** 归档不吞未完成 → deferred 转 open issue
- **E** pre-#134 孤儿 sweep (一次性审计所有 2026-06-10 前归档 spec 运行时真实性)

本 DEC **只界定范围与打包**, 不做实现设计 (交 spec-drafter Level 3 proposal)。

## 约束条件

> 📌 下表"B 必须 block / B 全机械 / C 启发式"= 决策时点表述; B 已被 §Amendment 1 消解 (post_spec 实证 B 不可用), "机械可判部分必须 block"原则保留但载体改 C 分级。当前以 §Amendment 1 为准。

| 类型 | 约束 | 影响 |
|------|------|------|
| 反模式 | 病根 = advisory 信号 (单测/structural benchmark) 给假 done 且**无阻断**; warn-only 修法会重演 `feedback_paper_fix_antipattern` | 机械可判部分 (B) 必须 **block**, 非 warn |
| 可机械化程度 | B 全机械 (解析两处比对); C 启发式 (需知哪个 `[x]` 配哪种产物, 有误报风险); D 是归档时动作非门 | enforcement **分级**, 不一刀切 |
| 小步迭代 | A (新探针范式) + E (无界一次性审计执行) 与 B/C/D (内聚永久 archive-gate 机制) 关注点不同 | A/E 拆出本 change, 防大爆炸 |
| 边界 (DEC-002) | DEC-20260704-002 的 5 项接活改造**已含** "runtime 探针 (#95 防复发)" — fix A 具体实例已被认领 | fix A 划归 DEC-002 先趟形态; #95 ⊥ DEC-002 |
| 构建序独立 | #95 (archive-gate 侧) 与 DEC-002 (协调机制侧) 代码 disjoint | D 用普通 open issue, **不**依赖 DEC-002 结构化 carry-forward (否则造构建序依赖) |
| 依赖 | E 须用 B+C+D 的真实性标准跑 → 必须 gate 先 ship | E 独立追踪, gate ship 后执行 |

## 考虑的方案

> 📌 本节 Q1-Q3 是**决策时点 (brainstorm) 的历史叙事**; Q2 的 "B block / C warn" 已被 §Amendment 1 修订 (B 消解 → C 分级)。历史保留, 当前架构以 §最终选择 (含 SUPERSEDED 标记) + §Amendment 1 为准。

### Q1 打包 (5 修复如何分组)

| 方案 | 描述 | 评分 | 状态 |
|------|------|------|------|
| **B+C+D 本 change / A 延后 / E 独立 sweep** | 本 Level 3 = archive-gate 硬化 (内聚永久机制); A 交 DEC-002; E gate ship 后独立跑 | ⭐ 最高 | **选定** |
| B+C+D+A 本 change / E 独立 | 两类永久机制合并 | 中 (A 与 DEC-002 探针撞车, 需先划清探针归属) | 否 |
| A-E 全进一个 change | 一次性全覆盖 | 低 (混永久 gate + 新范式 + 一次性审计, 违小步迭代, 与 DEC-002 重叠最大) | 否 |

### Q2 enforcement 强度

| 方案 | 描述 | 状态 |
|------|------|------|
| **分级 (B block / C warn / D auto-issue)** | 机械部分有牙不重蹈病根; 启发式部分不误伤合法归档 | **选定** |
| 全 block (严格) | C 启发式判 block 会误阻合法归档 (无法自动识别产物的正当 `[x]`) | 否 |
| 先全 warn 后翻 block | 仿 submodule-pointer-hygiene rollout; 但 warn-only 首版本身可能重演 #95 病根 (无阻断) | 否 |

### Q3 E (sweep) 追踪

| 方案 | 描述 | 状态 |
|------|------|------|
| **独立一次性审计 issue, gate ship 后跑** | 本 spec acceptance 有界可验; E 复用 gate 真实性标准 | **选定** |
| 作为本 spec 最后一个 phase | 兼作 gate 在真实数据上的验证; 但无界审计耦进 spec 完成度, acceptance 不好封口 | 否 |

## 最终选择

> ⚠️ **本节 B/C 已被 §Amendment 1 (2026-07-04 post_spec R1) 修订** —— **B 消解, block 主修复化入 C 分级**。下表 B 行 = 历史 (SUPERSEDED); C 行 enforcement 现为"分级 (block 死代码 / warn 模糊)"。读到此处务必续读文末 §Amendment 1。

**本 change (Level 3, 落 aria-plugin) = ~~B~~ + C + D** (B→C 见 Amendment 1):

| Fix | enforcement | 内容 | 落点 (待 spec 精化) |
|-----|-------------|------|---------------------|
| ~~**B**~~ **[SUPERSEDED → C, Amendment 1]** | ~~🔴 block~~ | ~~归档前交叉核对 tasks.md `[x]` vs proposal 成功标准 `[ ]`; 矛盾 → 硬阻断归档~~ (实证不可用: 成功标准惯例恒 `[ ]`) | ~~openspec-archive / `lib/spec_complete.py`~~ |
| **C** **[→ 分级, Amendment 1]** | ~~🟠 warn~~ → 🔴🟠 **分级** (block 高置信死代码 / warn 模糊) | `[x]` 真实性抽验: 集成类声称从 deliverables 提取符号, 生产零引用 → **block**; dogfood/benchmark 无产物 → warn | archive gate (详见 Amendment 1) |
| **D** | 🟢 **auto-issue** | 归档时 deferred/未完成实施项 → 自动创建 (或提示) **普通 Forgejo open issue** (自包含, 不依赖 DEC-002 结构化 carry-forward) | phase-d-closer / archive gate |

**显式 out-of-scope (延后, 非本 change)**:
- **A** (runtime-invocation 探针范式): 延后。具体实例由 **DEC-20260704-002** 先趟形态 (其 5 改造含 "runtime 探针 #95 防复发"); #95 留 follow-up, 待 DEC-002 探针成型后泛化为可复用范式 (state-checks / phase-c / phase-d gate 落点届时定)。
- **E** (pre-#134 孤儿 sweep): **独立一次性审计 issue**, 在 B+C+D gate ship 后执行 (复用 gate 真实性标准审所有 2026-06-10 前归档 spec)。留 #95 或新开子 issue 追踪。

**DEC-002 边界**: #95 ⊥ DEC-002 (archive-gate 侧 vs 协调机制侧, 代码 disjoint), **构建序独立可并行**; 唯一接触点 fix A 已划归 DEC-002 先行。

## 理由

> 📌 本节 §1-§2 论证 Gate B 的**决策时点理由**, 已被 §Amendment 1 修订 (B 消解 → C 分级); "block 才治病"的原则保留但载体从 B(对勾)改为 C(证据)。历史保留, 当前以 §Amendment 1 为准。

1. **B 必须 block 才治病**: #95 病根是 advisory 信号给假 done 且无阻断; B 全机械可判 (两处 `[x]`/`[ ]` 矛盾是客观缺陷), warn-only 会重演 `feedback_paper_fix_antipattern` (paper fix)。
2. **C 只能 warn 避误伤**: "`[x]` 是否有可核实产物" 是启发式 (需映射 `[x]` 语义 → 产物类型), 硬 block 会误阻无法自动识别产物的正当归档; 醒目 warn + 人工确认平衡有牙与误报。
3. **B/C/D 内聚**: 三者都是归档时刻的永久机制 (交叉核对 + 真实性抽验 + 不吞 deferred), 落点集中在 archive gate / spec_complete.py / phase-d-closer, 是 #134 archive-completeness-gate 的自然延伸 (补其 "完成度=存在性, 非真实性" 盲区)。
4. **A/E 拆出保小步 + 防重叠**: A 是新探针范式 (不同机制、不同落点、且与 DEC-002 探针撞车), E 是无界一次性执行 (依赖 gate 先 ship)。合入会违反最小可用/小步迭代, 并与 DEC-002 制造边界纠缠。
5. **D 用普通 open issue 而非 DEC-002 carry-forward**: 维持 #95 ⊥ DEC-002 独立性, 不造 "DEC-002 必须先 land" 的构建序依赖。

## 风险与缓解

> 📌 首行 B 交叉核对误报风险 = 决策时点; 其被 §Amendment 1 直接印证 (post_spec 实证成功标准恒 `[ ]` → B 大规模误报不可用 → 消解)。当前 C 分级的风险缓解见 §Amendment 1。

| 风险 | 缓解措施 |
|------|----------|
| ~~B 交叉核对误报~~ **[→ 已实证成真, B 消解, 见 Amendment 1]** (tasks.md 与成功标准合法地不 1:1 对应) | spec 设计须定义 "矛盾" 的精确判据 (仅当成功标准项能映射到 tasks.md 项且完成态相反时 block); 提供 exception 注释机制 |
| C warn 被忽视 (重蹈 "看到 warn 仍勾 done") | warn 文案须点名缺失产物类型 + 要求归档者显式 acknowledge; 配合 D 的 open issue 兜底 |
| D 自动建 issue 泛滥 (每次归档都开一堆) | 仅对**真** deferred/未勾实施项建 issue; 已在活跃 change `design_deferred` 覆盖的不重复 |
| fix A 归属漂移 (DEC-002 探针形态若变, #95 泛化失去锚) | 本 DEC 明确 A 延后且依赖 DEC-002 先行; #95 保持 open 追踪 A 泛化 + E sweep |
| 死代码闸 (病根 5, 超前造不接线) 未被本 change 直接覆盖 | 本 change 是归档时刻防线; on-arrival 死代码拦截属 fix A 探针范畴 (延后), spec 中记为 known-gap |

## Cross-references

- Issue: [aria-plugin #95](https://forgejo.10cg.pub/10CG/aria-plugin/issues/95) (本 DEC 界定其修复范围) + [#94](https://forgejo.10cg.pub/10CG/aria-plugin/issues/94) (同源双子星防重复)
- 姊妹决策: `DEC-20260704-002` (接活改造 Layer L 协调机制; fix A runtime 探针归此) — #95 ⊥ 本决策
- 归档 spec 活标本: `openspec/archive/2026-05-20-multi-terminal-coordination` (Layer L 死代码)
- 延伸对象: archive-completeness-gate `openspec/archive/2026-06-10-aria-archive-completeness-gate` (#134, v1.42.0) — 本 DEC 补其 `[x]`-存在性 vs `[x]`-真实性盲区
- memory: `feedback_paper_fix_antipattern` (doc-only advisory 是 paper fix) / `feedback_completion_signals_vs_runtime_invocation` (勾选/单测 ≠ 运行时 invocation)
- 事故 handoff: `docs/handoff/2026-07-04-dedup-coordination-brainstorm-dec.md`

---

## Amendment 1 (2026-07-04, post_spec R1 触发)

> **触发**: `openspec/changes/aria-archive-gate-runtime-reality` 的 post_spec convergence 审计 Round 1 (5-agent) 判 5/5 REVISE / FAIL, 其中 **Gate B 机制被 3 CRITICAL + 实证否证**。owner 拍板按"B 化入 C"重做。**本 amendment 修订 §最终选择的 B/C 决策**, 其余 (D / out-of-scope A·E / DEC-002 边界) 不变。

### 被否证的原设计 (B)

原 §最终选择 **B (block: 交叉核对 tasks.md `[x]` vs proposal 成功标准 `[ ]`)** 被实证不可用:

| 证据 | 事实锚 |
|------|--------|
| 成功标准 checkbox 惯例恒 `[ ]` (即便 spec 完全 shipped) | 抽样 `openspec/archive/2026-05-10-phase-c-integrator-pre-merge-gate/proposal.md` 已完全归档, Success Criteria 段全 `[ ]` (qa-engineer R1 CRITICAL 实测) |
| ⇒ B 判据"成功标准 `[ ]` ∧ tasks `[x]` = 矛盾"对**海量合法归档**成立 → 大规模误 BLOCK | backend-architect R1 CRITICAL: 判据在自引黄金反例上都不成立 |
| 新惯例 proposal (#134 + 本 draft) 无成功标准段 / 无编号 bullet → B 又 no-op | tech-lead + code-reviewer + knowledge-manager R1 major (共 5/5 命中 B) |

**根因**: "成功标准空勾"是**正常态**非缺陷信号; B 用"勾对不上"**间接**猜作弊, 分不清真作弊 (Layer L) 与正常完成。

### 修订后设计 (C 分级, B 消解)

Layer L 的**可靠**信号是"声称已集成的符号全项目零引用" —— 属 **C (证据/真实性核验)** 本职。故 **B 消解, C 升为分级证据闸**:

| enforcement | 触发 | 落点 |
|-------------|------|------|
| 🔴 **C-block (高置信死代码)** | 完成声称**点名具体代码符号** (identifier) 且该符号在**整 repo 全历史 provably 零引用** (定义存在但无任何 import/调用 site) | `spec_complete.py` + openspec-archive Step1 |
| 🟠 **C-warn + 持久标记 + ack** | 模糊声称 (dogfood/benchmark/deploy 完成但无可链接产物), 或未点名符号无法静态核验 | 写 frontmatter `unverified_claims` + 归档者 ack |
| ⚪ **fail-soft 放行** | 无法提取符号 / grep 失败 / 非代码集成类声称 | 记 soft_error, 不 block 不 warn |

**关键约束 (防原 audit F2 误报)**: C-block **只**发生在"点名符号 + provably 零引用"窄口 —— dynamic dispatch (getattr/importlib) 的符号会在别处有引用出现, 不会 provably 零引用 → 不误 block。

**"牙"保留**: enforcement 从「B-block / C-warn」→「**C 分级 (block 死代码 / warn 模糊) / D-auto-issue**」; block 级强制仍在, 只是从"看勾"(废) 挪到"看证据"(真管用)。

**A / DEC-002 边界 (再确认, 更清晰)**: C = **静态**归档时刻证据 (grep 引用 / 产物文件存在); A = **运行时**真被 invoke 遥测探针 (交 DEC-002)。C-block 只用静态零引用, 不触运行时探针范畴 → 仍 ⊥ DEC-002。

**D 承接 C 的 ack 项 (修 audit F3)**: 被 C-warn ack 的 unverified 声称一并纳入 D 的 auto-issue 兜底 → 归档后仍有 live tracker, 消除"ack 后零痕迹"绕过口。

### tri-state 契约 (修 audit F5)

`spec_complete.py` CLI 沿用 #134 exit code (0=allow / 1=block) 但 stdout JSON 新增 `gate_result: {verdict: pass|warn|block, blocking_reasons: [], warnings: []}`; 两 Bash 消费方 (openspec-archive Step1 / phase-d-closer D.2) **读同一 JSON verdict 字段** 而非各自解读 exit code。block→exit1+verdict=block; warn→exit0+verdict=warn (surface 不阻断); pass→exit0+verdict=pass。

### 落到 spec

本 amendment 直接改写 `proposal.md §What Changes` (1+2 → 单一 C 分级段) + `tasks.md` (Phase 2/3 → C 分级 + fail-soft 测试) + 补 proposal `## Success Criteria` 段 (audit F8, 有界可证伪 F7)。

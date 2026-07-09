---
unverified_claims:
  - claim: "持久化 E2E (SC-10, warn-outcome + 对称负控): 扩展 `test_archive_gate_integration.sh` — **正控**: 含活跃期声明 + warn 形态分区的合成 spec fixture 走 openspec-archive Step 1-2 脚本化流程 → 断言 `runtime_probe` 键真落盘 (**无既有块时验证块插入文件绝对起始**) + probe-warn 条目在 `unverified_claims` 同批 (**list-of-object 契约格式, 顺带修正既有 §3 precedent 的 `unverified_claims: %d` 计数偏差**) + `d_payload` 含该条目 + **断言经 `_frontmatter_block()`/`_read_archive_type()` 真实解析路径** (非裸 grep) + `_staleness_days` 无扰; **对称负控 (R3)**: (a) pass-outcome fixture 同流程 → 断言归档 frontmatter **无** runtime_probe 键; (b) 混合场景 fixture (probe=pass ∧ 无关声称致 verdict=warn) → 断言 unverified_claims 写入但 runtime_probe 键缺席"
    reason: "symbol 'unverified_claims' unclassified reference form"
    symbols: ["unverified_claims"]
  - claim: "持久化 E2E (SC-10, warn-outcome + 对称负控): 扩展 `test_archive_gate_integration.sh` — **正控**: 含活跃期声明 + warn 形态分区的合成 spec fixture 走 openspec-archive Step 1-2 脚本化流程 → 断言 `runtime_probe` 键真落盘 (**无既有块时验证块插入文件绝对起始**) + probe-warn 条目在 `unverified_claims` 同批 (**list-of-object 契约格式, 顺带修正既有 §3 precedent 的 `unverified_claims: %d` 计数偏差**) + `d_payload` 含该条目 + **断言经 `_frontmatter_block()`/`_read_archive_type()` 真实解析路径** (非裸 grep) + `_staleness_days` 无扰; **对称负控 (R3)**: (a) pass-outcome fixture 同流程 → 断言归档 frontmatter **无** runtime_probe 键; (b) 混合场景 fixture (probe=pass ∧ 无关声称致 verdict=warn) → 断言 unverified_claims 写入但 runtime_probe 键缺席"
    reason: "symbol 'd_payload' unclassified reference form"
    symbols: ["d_payload"]
  - claim: "Phase B-entry 真调 `phase1_gate` CLI (advisory claim, Layer L 编排契约; collision=self_multi_container + enabled=true 场景合法) → 产 production telemetry 记录 (顺带转绿 coordination-gate-invocation check); **失败 fallback**: 重试一次, 仍失败 → 记 known-limitation, 不阻塞其余 Phase 4 (SC-7 fallback)"
    reason: "遥测/运行时-invoke 核验属 fix A (out-of-scope); 静态 C 无法核验 → warn"
    symbols: []
  - claim: "lib 层真分区 dogfood: 以代码内构造的 coordination descriptor 对真实 `.aria/coordination-telemetry.jsonl` 直跑 `runtime_probe`, 记录 outcome+ts 于 closure 报告/handoff (一次性 ship-time 观测, **不固化为永久 pytest 断言**) (SC-7)"
    reason: "遥测/运行时-invoke 核验属 fix A (out-of-scope); 静态 C 无法核验 → warn"
    symbols: []
unverified_ack: true
unverified_ack_reason: "pre-merge 4 视角 (code-reviewer/silent-failure-hunter/qa/tech-lead) R1(1C/7I/13M)→R2→R3 零新 finding CONVERGED 已实证完成性; 见 .aria/audit-reports/pre_merge-FINAL-1783481672438-runtime-probe-archive-gate-integration-aggregated.md。4 claim 均为 #95 静态闸对已 ship 工作的 fail-toward-warn: 2 符号 (unverified_claims/d_payload) live 于 aria 子模块 grep scope 外; 2 dogfood 运行时 claim 由 TASK-018/019 完成 (telemetry 记录 + probe=pass 观测)。本归档系 #95 warn_overlay 机制首次真实行使 (此前 118/118 归档零 frontmatter 实例)。"
---
# Proposal: runtime-probe-archive-gate-integration (#95 follow-up A)

> **Status**: ✅ **SHIPPED v1.54.0 (2026-07-09)** — aria-plugin PR #97 merged (merge commit `565e214a`); 主仓 v1.54.0 surface + aria/standards 双指针 bump 完成; Phase D 归档 `openspec/archive/2026-07-09-runtime-probe-archive-gate-integration`。〔历史〕Approved (owner sign-off 2026-07-05; post_spec 5-agent convergence R1→R4 **CONVERGED** — R4 5/5 unanimous PASS)。**Phase A.2/A.3 complete 2026-07-06** — `detailed-tasks.yaml` 20 tasks / 6 文件域 TG / BA 8·QA 7·KM 2·main-loop 3 / 9 波次; **post_planning CONVERGED** (R1 5M+5m [含 warnings[] 双写转写丢失 + wave4 同文件并行] → R2 + qa F4 → R3 单点确认 PASS 0-new)。**Phase B complete 2026-07-08** — 20 任务全落地 (TASK-020 aria 侧已提交, 主仓 surface 待 merge 后随指针 bump); **pre_merge 4 视角 R1 (1C/7I/13M) → R1-fix → R2 (3 PASS + 1 窄幅) → R2-fix → R3 零新 finding CONVERGED** (报告 `.aria/audit-reports/pre_merge-FINAL-1783481672438-*`); **aria-plugin PR #97 待 owner 签字 merge (C.2)**, 签字注意项见 PR body (L2 蒸发裁决可复议 / merge-append / crash known-limitation)
> **审计轨迹 (post_spec, 5-agent convergence)**: R1 5/5 REVISE [2 CRIT: 持久化承诺无落点无 SC 且"复用既有机制"引用失实 (0/118 从未真实执行) / dogfood 回改归档先例站不住 → **owner 拍板: 不回改归档**] → R1-fix → R2 5/5 REVISE [R1 全项闭合获五方确认; fix-revealed: B1 持久化触发条件与 warn_overlay 宿主错位 (4/5 收敛) + B2 SC-9 漏 disabled 第 4 态 + B3 无-frontmatter 插入指令缺失 + B4 官方示例自带注释而解析器未定义注释剥离 (B6 文本层测试并入此项) + B5 probe-warn 不入 d_payload 无 tracker 兜底 + B7 standards 版本历史/指针漏项 → **裁决: 落盘收窄对齐宿主 (仅 warn), probe-warn 并入 unverified_claims 复用双下游**] → R2-fix → R3 3 PASS / 2 REVISE [R2 全项闭合五方确认; 剩余: C1 混合 verdict 内容归属 (3 agent 同源) + C2 dry_run 回显连带面 + C3 proposal.md IO 有意偏离先例需言明 → **裁决: 键写入取决于探针自身 outcome, 非门级 verdict 来源**] → R3-fix → **R4 5/5 unanimous PASS** [R3 全项闭合五方确认; 0 new blocking; 全部关键行号引用经 code-grounding 逐字核实; KM 2 项导航行 minor 已随手修] → **CONVERGED 2026-07-05**
> **Spec Level**: 3 (Full — proposal + tasks; 精简 L3: 单决策 4 部件, blast radius 高在 gate 裁决语义而非代码量)
> **关联 Issue**: aria-plugin [#95](https://forgejo.10cg.pub/10CG/aria-plugin/issues/95) (closed, 本 change = 其 §2 follow-up A「runtime-invocation 探针泛化」) — 无独立新 issue
> **ship target**: aria-plugin v1.54.0 (当前 SOT plugin.json = v1.53.0)
> **决策 SOT**: `docs/decisions/DEC-20260705-001-runtime-probe-into-archive-gate.md` (方案对比 A/B/C + grounding 实证 + 取舍论证, 本 proposal 不复制) + owner 决策 2026-07-05: dogfood 不回改已封存归档 (偏离 DEC ④ 原案, 已披露) + R2 裁决: 持久化仅 warn 落盘 (细化 DEC ③, 对齐宿主机制语义) + R3 裁决: 键写入取决于探针自身 outcome, 非门级 verdict 来源
> **双亲 change**: `2026-07-05-aria-archive-gate-runtime-reality` (#95 静态门, 被扩展方) + `2026-07-05-interactive-session-dedup-coordination` (DEC-002 动态探针, 被泛化方) — 本 change 是二者的合流点

---

## Why

#95 (v1.53.0) 与 DEC-002 (v1.52.0) 已围绕「归档 spec 勾选完成 ≠ 运行现实」病根 ship 两个互补检查:

| 机制 | 维度 | 局限 |
|------|------|------|
| `spec_complete.py :: gate_result` | **静态** (归档时): 符号有定义但生产零语义引用 → block | 只能证「接了线」, 证不了「最近真转过」 |
| `coordination_probe.py` | **动态** (运行时): 近 14d 是否真经生产入口被调用 | **单一用途硬编码件** — 写死 1 分区 / 1 符号 (`run_gate`) / 1 config 开关, 只服务 coordination 一家 |

两者互不相通: 归档门看不见运行时证据, 动态探针没有泛化路径。DEC-20260705-001 grounding 实测三条实证 (N=1 消费者 / E-sweep 100 归档零死代码孤儿 / **动态探针须机制预埋 telemetry 才有日志可查**) 否决了「独立通用框架」方向, 收敛为: **把动态探针泛化成归档门的「声明式可选动态子检查」** —— spec 在 frontmatter 声明自己有探针, 归档门见声明才跑并把「最近真被调用过吗」折进裁决; 无声明 spec 零影响。

**价值**: 一旦某机制退化成「挂着没转」, 归档门今后能凭**运行时证据** (非仅静态引用) 在归档时刻抓住, 且该信号经 `unverified_claims` 通道进入 D auto-issue 兜底 (headless 亦不吞) — 这正是 coordination 曾经的失败形态 (`run_gate` 死代码两个月无人察觉, #94 事故考古才翻出)。

**诚实前提披露 (post_spec R1 实证)**: #95 设计的归档 frontmatter 写入面 (openspec-archive SKILL.md Step 2 `warn_overlay`, 由 AI 在归档时刻写入 `unverified_claims` 等机器键) **shipped 但从未在真实归档中执行过一次** — 全部 118 个已归档 proposal.md 零 frontmatter 实例, 含 #95 自身 (其归档 verdict=warn 本应触发写入而未写; `already_archived_precheck` 使事后重跑结构上不触发 Step 2)。本 change 的 SC-10 将以脚本化 E2E fixture **首次在连续 Step 1-2 归档流程中按契约格式 (list-of-object) 行使**该写入路径 — 既有 `test_archive_gate_integration.sh` §3 仅孤立模拟过写入且其 `unverified_claims: %d` 计数形式偏离 SKILL.md `:179-183` list-of-object 契约, 本 change 顺带修正该 precedent 的断言形式。不把"已设计+已合成测试"再误当"已验证"。

## What Changes

延伸 `lib/spec_complete.py :: gate_result` (#95) + 泛化 `coordination_probe.py` (DEC-002), 落地 DEC-20260705-001 方案 A 的 4 部件:

1. **① 探针声明 (新增声明面, spec `proposal.md` YAML frontmatter)**:

   ```yaml
   runtime_probe:
     partition: .aria/coordination-telemetry.jsonl   # 生产 telemetry 分区路径 (必填; 必须相对路径且 resolve 后含于 repo)
     symbol: run_gate                                # 盯的符号 (必填; 消息标签用, 不做记录级过滤)
     max_age_days: 14                                # 新鲜度窗口 (可选, 默认 14; 必须正整数 ≥1)
     enabled_when: state_scanner.coordination.enabled # 可选: .aria/config.json dotted-path 开关
   ```

   - 声明 schema 保持最小 (4 字段, 2 必填); **分区按机制专用** (symbol 当标签 — 分区里每条天然属该机制, 不强迫改 telemetry 写入格式/回填旧记录); 日后若现共享分区再加可选记录级 symbol 过滤 (out-of-scope)。
   - **声明的正常家 = spec 活跃期作者自写** frontmatter (文件未封存, 合法编辑), 归档时随文件整体移入 archive/ 自然带入 — **不回改已封存归档补声明** (owner 决策 2026-07-05; 对齐 ERRATA 惯例「不修改归档 proposal 本体」)。未来首个真实声明者 = 下一个自带 telemetry 分区的活跃 spec。
   - **解析约束 (stdlib-only)**: 不引 PyYAML。frontmatter 块提取复用 **#134** `_FRONTMATTER_RE` 的解析语义 (文件绝对起始 `---` 块, 正文代码块不会被误读) — regex/helper **物理 move 到 `scripts/lib/` 叶子模块 + `collectors/openspec.py` 反向 re-import** (行为不变; `carry_forward.py` #134 同型先例, 单一 SOT **不复制不双写**), **禁止 `spec_complete.py` import `collectors.openspec`** (后者 `:38` 已 import `lib.spec_complete`, 反向复用即循环 import)。块内 `runtime_probe` 声明按**受限 YAML 子集**手写解析: 顶层 `runtime_probe:` + 4 个 scalar 子键 (固定 2-space 缩进); **行尾注释剥离** (值中首个 ` #` 起丢弃到行尾, 裸 scalar 语义) — 本节官方示例原样 (含注释) 必须可正确解析 (SC-2 锁定); 超出受限形态 (更深嵌套 / flow-style `{}` / 锚点 `&*` / 多行值) → 声明无效 → warn, 不猜。

2. **② 通用探针库 (泛化 `coordination_probe.py`)**:
   - 新增 `scripts/lib/runtime_probe.py`: `probe(descriptor, repo, now) -> {outcome, count, reason, symbol}`。写死常量 (分区路径/符号/窗口/config 键) 全部改由 descriptor 传入; 沿用既有解析语义 (JSONL 坏行跳过不 fatal / `source=="production"` 过滤 / 新鲜度 cutoff / 注入 `now` 确定性测试)。
   - **三态 outcome**:
     - `pass` — 窗口内 ≥1 条生产记录 (活的, 真在转)。
     - `warn` — 分区缺失 / **分区存在但不可读 (IO error)** / 全陈旧(>窗口) / 只有非生产记录 → 挂着但最近没转 = 死代码嫌疑。
     - `skipped` — `enabled_when` 指向的 config 开关为关 → 功能本就没开,「没被调用」是预期; 静默避免狼来了 (**保 warn 信噪比**)。config 文件缺失/读不到 → 保守 `skipped` + 低调 note, 不 warn (无法确证本该开就不误报); dotted-path **中间段类型不对** (如 `state_scanner` 值非 dict) → **声明无效 → warn** (每级 `.get` 防御判定, 归清晰类, 不落外层异常兜底)。
   - descriptor 校验: 缺必填字段 / 类型错 / `max_age_days` 非正整数 / `partition` 为绝对路径或 resolve 后逃逸 repo (`is_relative_to` 校验, 防 pathlib `repo / "/abs"` 静默丢前缀陷阱) → 返回明确「声明无效」结果 (供 ③ 归 warn), 不猜不硬崩。
   - **既有假绿 bug 修复 (显式裁决, post_spec R1)**: 现 `coordination_probe.py` 对「分区存在但 `read_text` 失败」返回 `-1` 后落入 `"OK (-1 recent ...)"` **exit 0 假绿** (`:86-89` 返 -1; `main()` 只分流 `exists()`/`n==0`, `:130` 兜底 OK)。通用库把该形态归 `warn`; 薄壳 CLI **同步修复** (unreadable → STALE 类消息 + exit 1), 作为本 change 唯一有意的 CLI 行为变化, 回归测试锁定 (见 SC-9)。
   - **`coordination_probe.py` 改薄壳**: 委托通用库 + 硬编码 coordination descriptor。薄壳负责 **三态→二元 exit 映射** (`pass`/`skipped`→0, `warn`→1) 并用 coordination **专用消息模板**重格式化 (不透传通用库泛化 reason) — 使既有 CLI 契约 (参数/exit code/消息文本) 对**四种既有可达状态** (disabled / 分区缺失 / 正常 n≥1 / 全陈旧 n==0) **逐字节不变** → `.aria/state-checks.yaml` 的 `coordination-gate-invocation` check 不改一行。
   - **known-tradeoff**: 分区解析沿用一次性整读 (非流式); 依赖分区体量保持较小 (telemetry 修剪/轮转 out-of-scope), 文档如实标注。

3. **③ 归档门折入 (`gate_result` 扩展)**:
   - `gate_result(spec_dir)` 读 proposal frontmatter (经 ① lib 叶子 helper): 无 `runtime_probe` 键 → **零动作, 静态路径逐字节不变** — **`runtime_probe` 键必须整体不存在于返回 dict/JSON (禁 `null` 占位)**; 现实现入口无条件预置全部 8 键 (`spec_complete.py:1124-1133`), 新键**不得**加入该初始化字面量; CLI 两处硬编码 fallback JSON (usage 错误路径 `:1273-1288` / crash 兜底路径 `:1294-1309`) 同样不含该键 (SC-1 兜底)。**新增 IO 失败语义**: proposal.md 缺失/读失败 → 等同无声明零动作 + `soft_errors` 记录。**有意偏离先例的显式说明 (R3)**: tasks.md 先例是两条分支 (缺失 `:1142-1144` 静默无 soft_errors — L2 spec 合法可缺 / 读失败 `:1148-1150` 才记 soft_errors); proposal.md **缺失与读失败两形态统一记 soft_errors** 是有意更响 — change 目录缺 proposal.md 本身即异常, 不适用 tasks.md 的"合法可缺"静默逻辑。gate_result 两个既有早退路径 (tasks.md 缺失/不可读) **不评估探针** (spec 结构性不完整时探针无意义, designed 行为, 等同零动作)。**pre-merge R1 披露 (2026-07-08)**: 该早退面**含合法 L2/proposal-only spec** (tasks.md 合法可缺、complete 可为 true) —— 有声明也不评估、零痕迹; 前置条件 (探针仅对含 tasks.md 的 L3 spec 生效) 已写入声明作者文档 `references/runtime-probe-declaration.md` 并由集成测试锁定现行为; 带 telemetry 的 L2 spec 若需探针 → 升级 L3, 机制扩展 out-of-scope。
   - 有声明 → 跑 ② → 折入 tri-state 裁决 (**严格 fail-toward-warn**):
     - `pass` → verdict 不变 + 绿色 note (含 count/symbol)。
     - `warn` (含声明无效) → verdict 抬到**至少 warn**, **绝不抬 block**; 已 block 的 spec 加 warn 不改其 block。**routing (R2 裁决, 解「核心场景无 tracker 兜底」)**: probe-warn 条目除 `warnings[]` 外, 以 `{claim: "runtime_probe:<symbol>", reason: <probe reason>, symbols: [<symbol>]}` 形态**并入 `unverified_claims[]`** (语义吻合: 运行时活性无法证实的声称) → **自然复用 #95 既有双下游**: warn_overlay 持久化 + `d_payload`/Step 7 D auto-issue 兜底 (headless 归档不吞「挂着没转」信号), 零机制签名改动。
     - `skipped` → verdict 不变 + 低调 note。
   - 探针结果作为**条件性新字段** `gate_result.runtime_probe: {...}` 返回 (仅声明存在时); `openspec-archive` SKILL.md Step 1 的 `--gate` stdout JSON 读取 schema (`:115-116`) 同步补注该条件字段。
   - **持久化 (证据痕迹) — 归档编排层职责, 仅 warn 落盘 (R2 裁决)**: `gate_result` 是纯函数只产 JSON 不写文件 (职责分离, #95 既有设计)。落盘由 openspec-archive SKILL.md Step 2 `warn_overlay` 承载, **触发条件对齐宿主机制原语义 (`verdict=="warn"`), 不扩展**: warn 时 `runtime_probe` 结构化结果 (outcome/count/ts/symbol) 作为额外键与 `unverified_claims` (含 probe-warn 条目) **同批写入**被归档 proposal frontmatter; **pass/skipped 不落盘** (干净归档零噪音, mirror unverified_claims 先例 — pass 观测由 SC-7 closure 报告/handoff 承载, 声明本身仍随文件归档可见)。**内容归属条件 (R3 裁决, 与整批触发条件正交)**: `runtime_probe` 键是否被包含在写入内容里取决于**探针自身 outcome ∈ {warn, 声明无效}** (与其是否贡献 unverified_claims 条目同条件), **与触发整批写入的门级 verdict 来源无关** — 门级 verdict 因无关声称被顶到 warn 时, outcome=pass 的探针结果依然不落盘 (SC-10 混合场景负控锁定)。**dry_run 回显同步扩展 (SKILL.md `:188`)**: dry-run 报告回显契约从「将写入的 unverified_claims 列表」扩展为「+ (若探针 outcome ∈ {warn, 声明无效}) runtime_probe 结构化结果」— 保持归档前所见即所得。**无既有 frontmatter 块时的写入指令 (118/118 现状)**: proposal.md 不以 `---` 开头 → 在**文件绝对起始插入**新 `---...---` 块 (原内容整体下移); 已有块则追加键。**同名键 merge-append (B.2 主控裁决 2026-07-08, TASK-016 E2E 首次连续流程行使实证契约缺口后定)**: 带声明 spec 的既有块内 `runtime_probe:` 键必然已被声明本体占用 → 结果字段 (outcome/count/ts; symbol 仅声明缺失时补写) **merge-append 进既有 mapping**, 不删改任何作者声明字段、不新起同名键、不产生 YAML 重复键 (向前兼容由 unknown-子键宽容忽略承接); 作者值**非块 mapping** (如顶层 flow-style, 属文本层声明无效) 时 merge 结构上不适用 → 结果键**不落盘**, 「无法核验」信号由同批 unverified_claims 条目完整承载 (显式降级路径)。细则见 openspec-archive SKILL.md「同名键 merge-append 规则」。
   - **全异常兜底 (silent-failure 防线, #95 pre-merge Critical 教训)**: 探针内部任何未预期异常 → gate catch → 降级 warn 且照常产出完整裁决 — **探针是加分项, 绝不成为新 block 源, 绝不静默吞掉裁决**。**known-limitation (显式窄化, pre-merge R1 复核)**: 崩溃路径记 warnings[] + soft_errors[] 并 fail-toward-warn, 但**不**追加 unverified_claims / 不触发 D auto-issue —— 探针自身故障是 gate 代码问题而非被归档 spec 的完成度声称, 路由进该 spec 的 D tracker 会归错 owner; 该非对称性由 fault-injection 测试显式锁定。
   - 正交性: 动态结论 ⊥ `complete` ⊥ 静态 block (可静态 pass ∧ 动态 warn)。

4. **④ dogfood (不回改归档, owner 决策 2026-07-05) + 文档**:
   - **(i) E2E 合成 spec 走真实归档流程 (SC-10)**: 扩展 `test_archive_gate_integration.sh` — 非预归档的合成 spec fixture (含活跃期自写 `runtime_probe` 声明 + **warn-outcome 分区形态** [如全陈旧], 使 verdict=warn 触发 warn_overlay) 走 openspec-archive Step 1-2 脚本化流程, 断言: `runtime_probe` 键 (outcome/count/ts) 真落盘归档后 proposal frontmatter + probe-warn 条目在 `unverified_claims` **同批且为 list-of-object 契约格式** (`SKILL.md:179-183`) + `d_payload` 含该条目 (D 兜底通路核验) + **断言经 `_frontmatter_block()`/`_read_archive_type()` 真实解析路径** (非裸 grep, 防插错位假阳) + `_staleness_days` 等既有消费者行为无扰。
   - **(ii) lib 层真分区 dogfood (SC-7)**: task 4.1 Phase B-entry 按 state-scanner Layer L 编排契约**真调一次 `phase1_gate` CLI** (advisory claim; 当前 snapshot `collision.kind=self_multi_container` + `coordination.enabled=true`, 场景合法) → 写生产 telemetry 记录 (顺带转绿本仓当前红着的 `coordination-gate-invocation` check); 随后以代码内构造的 coordination descriptor 对**真实分区**直跑 `runtime_probe`, 记录 outcome+ts (一次性观测)。
   - **(iii) 零回归真语料样本**: coordination 归档 spec **保持无声明**, 作为 SC-1 re-sweep 语料一部分 (归档纯净; 常驻 runtime 信号已由 `.aria/state-checks.yaml` `coordination-gate-invocation` check 每次 state-scan 承载, 不在归档语料重复)。
   - 文档 (Rule #3): state-scanner references 新增声明 schema 文档 + `openspec-archive` SKILL.md **Step 2 写入契约扩展 + Step 1 读取 schema 补注** (见 ③) + `phase-d-closer` SKILL.md additive 提及 + standards 归档惯例一行 (「完成=可核实完成」段补运行时证据可选项, **同步新增该文件自身 Version History 行** — #95 编辑同文件留有 2.2.1 行先例)。

## Impact

- **触及面**: `state-scanner/scripts/lib/runtime_probe.py` (新增) + `scripts/lib/` frontmatter helper (自 collectors **move** 下沉新增) + `scripts/collectors/openspec.py` (仅 `_FRONTMATTER_RE`/`_frontmatter_block` 定义改为自 lib 叶子 re-import, 行为不变 — #134 carry_forward 同型先例) + `scripts/coordination_probe.py` (改薄壳 + read-failure 假绿修复) + `scripts/lib/spec_complete.py` (gate_result 扩展 + probe-warn→unverified_claims routing) + `skills/state-scanner/tests/` (单元+集成+E2E 扩展) + state-scanner references (声明 schema 文档) + `openspec-archive/SKILL.md` (**Step 2 warn_overlay 写入契约扩展 + Step 1 schema 补注**) + `phase-d-closer/SKILL.md` (additive 一段) + standards `openspec/project.md` (归档惯例一行 + Version History 行)。版本 SOT: aria 侧 5 文件 + 主仓 3 surface (/VERSION 行 + README badge + Project Status) + 子模块指针 (aria 必; standards 因 project.md 变更亦须) → v1.54.0。
- **零改动面 (显式)**: `.aria/state-checks.yaml` 不动 (薄壳保 CLI 契约); telemetry 写入格式不动; scan.py collectors 行为不变 (仅上述 re-import 源变更); `state-snapshot-schema.md` 不动 (gate_result 是 CLI 输出非 snapshot 字段); #134 `complete` 判定不动; warn_overlay 触发条件不动 (对齐不扩展); **全部已归档 spec 文件不动** (owner 决策)。
- **向后兼容 (Rule #4)**: 无声明 spec 的 gate 行为**逐字节不变** (SC-1); 声明路径全程 fail-toward-warn 永不 block。#95 归档门性质保住: E-sweep (100 pre-#134 归档孤儿审计, 零死代码孤儿) 与 #95 116 归档 re-sweep (仅死代码 block, SC 零影响) 两项既有实证**均不被本 change 扰动** (语料无声明 → 零动作)。唯一有意行为变化 = `coordination_probe.py` read-failure 假绿修复 (显式披露 + 回归锁定, 见 ② / SC-9)。
- **Rule #6**: deterministic 探针/折入逻辑 → unit + integration + E2E fixture + 一次性真分区 dogfood 替代 AB benchmark (同 #95 disposition 先例; block/warn 契约测试**钉合成 fixture 非真实语料** — 真语料随现实漂移, `feedback_gate_tracks_reality_synthetic_fixture`)。
- **Out-of-scope (显式)**: 独立通用探针框架 (DEC Scope 层已否); 共享分区的记录级 symbol 过滤; 强制式「门反催没声明的 spec」(DEC 集成方式层方案 B 已否); 纯接线硬编码映射表 (集成方式层方案 C 已否); telemetry 分区修剪/轮转 (整读 known-tradeoff 见 ②); 归档门之外的其他集成点 (state-scanner snapshot surface 等); 历史归档 spec 批量补声明 (**含 coordination — 不回改归档**); warn_overlay 触发语义扩展 (对齐宿主, 见 ③)。

## Success Criteria

> 每条绑可验 metric (falsifiable, `feedback_falsifiable_evidence_for_binary_acceptance`); 禁 AI 代填 bool。

- [ ] **SC-1 零回归 (最高优先)**: 对全部归档 + 活跃 changes (无 `runtime_probe` 声明) 逐个跑 `--gate`, 输出 JSON 与 v1.53.0 基线 **diff=0**。控制变量: **同一 worktree 同一树内容**上 v1.53.0 代码 vs 新代码双跑对比 (排除 `classify_symbol_liveness` 全 repo grep 面的语料漂移噪音), 脚本化可复现
- [ ] **SC-2 pass 折入 (内存态)**: 合成 fixture (声明 + 窗口内生产记录) → `outcome=pass`, verdict 不变, `gate_result.runtime_probe` 字段存在且 count≥1; **pass 不落盘 (显式断言归档 frontmatter 无 runtime_probe 键)**; **官方示例原样解析用例**: §What 1 示例块文本 (含行尾注释) 直接作 fixture → 4 字段全部正确提取
- [ ] **SC-3 warn 折入·永不 block**: 四种 warn 形态 (分区缺失 / **分区存在但不可读** / 全陈旧 / 仅非生产记录) 各一 fixture → verdict 从 pass 抬到 warn **且 probe-warn 条目以 list-of-object 形态出现在 `unverified_claims[]` + `d_payload`**; **block fixture + 探针 warn → verdict 仍 block** (不降不升); 任何声明路径 fixture **均无** verdict=block 由探针引入
- [ ] **SC-4 skipped 静默**: `enabled_when` 开关关 fixture → `outcome=skipped`, verdict 不变, warnings 无新增, 不落盘; config 文件缺失 → 同 skipped + note
- [ ] **SC-5 声明无效 → warn 不猜 + IO 边界**: 值层五形态 (缺 `partition` / 类型错 / `max_age_days` 非正整数 / **`partition` 绝对路径或 `..` 逃逸 repo** / **`enabled_when` dotted-path 中间段非 dict**) + **文本层四形态 (更深嵌套 / flow-style / 锚点 / 多行值)** 各一 fixture → 均 warn「无法核验」+ 并入 unverified_claims, 非 block, 非 crash; **IO 边界 fixture (非 warn 非声明无效)**: proposal.md 缺失 / OSError 各一 → 等同无声明零动作 + `soft_errors` 记录断言
- [ ] **SC-6 fault-injection**: monkeypatch 探针抛异常 → gate 降级 warn 且照常产出完整裁决 (归档不 abort, 无静默)
- [ ] **SC-7 一次性真分区 dogfood 观测**: task 4.1 CLI 真调产生产记录后, lib 层以 coordination descriptor 对真实 `.aria/coordination-telemetry.jsonl` 直跑探针, 记录 outcome+ts 于 closure 报告/handoff (预期 pass, 2026-07-18 前记录新鲜)。**定位为一次性 ship-time 人工观测, 不固化为永久 pytest 断言** (真语料随现实漂移; 契约由 SC-2~5 合成 fixture 承载)。**fallback**: CLI 调用失败 → 重试一次; 仍失败 → 记 known-limitation (warn 路径已由 SC-3 覆盖), 不阻塞 Phase 4 其余任务
- [ ] **SC-8 可证伪 harness**: 变体「探针恒 pass」注入 → 测试套至少 1 例 FAIL (anti-false-green, DEC-002 传统)
- [ ] **SC-9 CLI 向后兼容 + 假绿修复锁定**: `coordination_probe.py` 薄壳化前后, 对**四种既有可达状态** (disabled / 分区缺失 / 正常 n≥1 / 全陈旧 n==0) 输出消息 + exit code **逐字节一致** (`coordination-gate-invocation` check 无感); **唯一有意变化** = read-failure 假绿修复 (旧: `"OK (-1 ...)"` exit 0; 新: STALE 类消息 exit 1), 独立回归测试锁定新行为
- [ ] **SC-10 持久化 E2E (warn-outcome + 对称负控, 首次连续流程行使)**: 扩展 `test_archive_gate_integration.sh` — **正控**: 含活跃期声明 + warn 形态分区的合成 spec fixture 走 openspec-archive Step 1-2 脚本化流程 → 断言: `runtime_probe` 键 (outcome/count/ts) 真落盘归档后 proposal frontmatter (**无既有块时验证块插入文件绝对起始**) + probe-warn 条目在 `unverified_claims` 同批且为 **list-of-object 契约格式** + `d_payload` 含该条目 + **断言经 `_frontmatter_block()`/`_read_archive_type()` 真实解析路径核验** (非裸 grep) + `_staleness_days` 既有消费者无扰; **对称负控 (R3, 锁「不落盘」侧)**: (a) pass-outcome fixture (声明 + 窗口内新鲜记录, verdict=pass) 走同流程 → 断言归档 frontmatter **无** `runtime_probe` 键; (b) 混合场景 fixture (probe=pass ∧ 门级 verdict 因**无关**声称=warn) → 断言 `unverified_claims` 正常写入**但 `runtime_probe` 键缺席** (内容归属随探针自身 outcome, 非门级 verdict 来源)

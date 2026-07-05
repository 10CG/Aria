# Proposal: archive-gate-runtime-reality (#95)

> **Status**: **Approved** (post_spec convergence CONVERGED 2026-07-04, R5 unanimous PASS 5/5)
> **审计轨迹 (post_spec, 5-agent convergence)**: R1 5/5 REVISE [3 CRIT — Gate B 交叉核对被实证不可用, owner 拍板 B→C] → R2 3 REVISE [C 符号提取/D headless] → R3 3 REVISE [1 收敛 CRIT: 注释算引用] → R4 4 PASS/1 REVISE [清单非穷尽] → **R5 5/5 PASS** [仅 minor]。B→C 转换见 DEC-003 Amendment 1。
> **Spec Level**: 3 (Full — proposal + tasks)
> **关联 Issue**: aria-plugin [#95](https://forgejo.10cg.pub/10CG/aria-plugin/issues/95) (归档 spec 勾选完成 ≠ 运行现实; 源自双子星重复事故 #94 归档考古)
> **ship target**: aria-plugin v1.52.0 (当前 SOT plugin.json = v1.51.0)
> **决策 SOT**: `docs/decisions/DEC-20260704-003-archive-gate-completion-vs-runtime-reality.md` (含 **Amendment 1**: B 化入 C, C 分级; 本 proposal 不复制取舍论证)
> **姊妹决策**: `DEC-20260704-002` (接活改造 Layer L 协调机制) — 本 change ⊥ 它, 构建序独立可并行

---

## Why

archive-completeness-gate (#134, v1.42.0) 建了 `lib/spec_complete.py` 完成度判定 (`complete := tasks.md 全[x] ∧ 无 inline defer, OR Status∈{done}`) + 归档 BLOCK gate + `design_deferred[]` surface。但它验的是 **checkbox 的存在性, 不是完成的真实性**, 也不追踪归档后残留的未完成实施:

| gap | 事实锚 (Layer L 活标本, `openspec/archive/2026-05-20-multi-terminal-coordination`) |
|-----|------|
| **(C)** #134 验 checkbox **存在**, 不验 checkbox **属实** | `集成 state-scanner` 标 `[x]`, 但 `scan.py` 全历史零 import/调用 `phase1_gate` (集成从没在代码发生) → 无 call-site 的"集成完成"被当真归档 |
| **(D)** #134 `design_deferred[]` 只 surface **活跃** change; 归档后无 open tracker | Layer L 归档关闭后未做的 P3 接线**无 open issue 兜底**, 消失于已归档 spec, 直到 #94 事故才被翻出 |

> **设计注 (post_spec R1, DEC-003 Amendment 1)**: 初版曾设 Gate B (交叉核对 tasks.md `[x]` vs proposal 成功标准 `[ ]`) 作 block 主修复, 但 post_spec 审计**实证**成功标准 checkbox 惯例恒 `[ ]` (即便 spec 完全 shipped — 抽样 `phase-c-integrator-pre-merge-gate` 归档 proposal 证) → 该核对无法区分真作弊与正常完成 (会海量误 BLOCK), 且新惯例 proposal 无该段致 no-op。**已消解 B, block 主修复改由 C 分级证据闸承担** (Layer L 的可靠信号本就是"零 call-site", 属 C 本职)。

**病根**: "完成"是勾出来的不是跑出来的。单测过 + structural benchmark 过给了 done 假信号, 却无机制在归档时刻核验完成声称的**真实性** (有无 call-site/产物) 或兜底归档后的残留工作。这不是单点 bug, 是一类流程瑕疵 (完整病理见 DEC-20260704-003 §背景; runtime-invocation 教训见 memory `feedback_completion_signals_vs_runtime_invocation`)。

## What Changes

延伸 #134 的 `lib/spec_complete.py` + `openspec-archive` + `phase-d-closer` + `collectors/openspec.py`, 落地 DEC-20260704-003 (含 Amendment 1) 的 **C 分级证据闸 + D auto-issue**:

1. **C — 完成声称真实性证据闸 (🔴 block 死代码 / 🟠 warn 模糊)**:
   - 识别 tasks.md `[x]` 行中的**代码集成类**完成声称 (关键词: 集成/接线/wire/integration/调用/registered/hook)。
   - **符号提取 (R2 F2-fix)**: 完成声称的**符号名往往不在 tasks.md prose 里** (Layer L 反例: tasks 2.5 "集成 state-scanner" 是纯散文, `phase1_gate` 只在 deliverables 具名)。故提取源 = 该集成声称映射的**已声明交付物**: `detailed-tasks.yaml` 对应 task 的 `deliverables` + proposal `Key Deliverables` + tasks.md 关联行内的代码路径/backtick identifier (`[a-zA-Z_][a-zA-Z0-9_.]*`)。提取不到具体符号 → 归 warn/fail-soft, 非 block。
   - **🔴 BLOCK (高置信死代码, R3-fix 语义级引用分类)**: 提取到具体符号 **且** 该符号**零生产语义引用** → dead-code-on-arrival → BLOCK。判定须**语义级** (**非朴素全文 grep** —— 实测朴素 grep 会被 3 个生产 collector 的注释/docstring 提及误判为"已引用", 致 golden 负例跑不出 block):
     - **算"已引用" (alive → 不 block)**: (i) **代码引用** = import 语句 / 调用 `X(` / 属性 `X.` / 装饰器 `@X` / 赋值别名; (ii) **dynamic-dispatch** = `getattr`/`importlib`/`globals()` 反射中的符号名字符串; (iii) **aria-plugin 集成面** = SKILL.md 内 Bash 调用该脚本/符号 或 `hooks.json`·config 注册该 hook/命令 (aria-plugin 主导集成方式常在 .md/.json 非 .py, 修 tech-lead 反向漏判 → 误 block); (iv) **通用调用面** = shell/cron/Makefile/CI 按**字面路径**调用该脚本/符号 (如 `.aria/scripts/*.sh` 内 `python3 path/to/x.py`, 非 import; 修 qa R4 实测 `m6-phase-b-gate-check.sh` 假阳)。**边界** (A.2 细化): 内联函数级调用 (`python3 -c "from mod import func; func()"`) 归 (i) 代码引用, (iv) 限**整脚本路径**调用。
     - **不算引用 (→ 不阻止 block)**: 注释 (`#…`) / docstring / 描述性字符串字面量 / 任何文件的散文提及 (含 `*.md`/CHANGELOG/`.aria/audit-reports/`); **测试文件** (`test_*` / `*_test` / `tests/` / `conftest`); **dogfood·ops 核验脚本目录** (`.aria/scripts/dogfood/` 等, 属核验非生产); **符号自身定义文件**。
     - **非穷尽划分 → fail-toward-warn 默认 (R4 qa-fix)**: 上两清单**不保证穷尽**; 任何**落在两清单之外**的生产出现形态 (未识别的 wiring/跨语言/异常调用面) → **默认视为"可能已引用" → 降 block 为 warn** (不 hard-block)。**hard-BLOCK 只在**: 该符号所有生产出现**全属"不算引用"类** (纯散文/注释/测试) **或零出现** —— 即高置信死代码。这使误分类**恒偏向不误 block** (假阴 > 假阳), 兑现 Impact §"既有正常归档零影响"。
     - 实现须**剥注释/docstring 后**匹配代码引用 (i/ii) + **单独扫集成/调用面** (iii/iv); 解析精度细节留 A.2/实现, 但下方 golden 负例 + 4 类正控 (真实代码引用 / 集成面 / dispatch / 通用路径调用) acceptance **钉死行为契约**。
     - **残留 known-limitation**: 集成面 alive 信号 (SKILL.md Bash / hooks.json / shell 路径调用) 理论上可被蓄意伪造调用 spoof (比逃生舱隐蔽无 flag 痕迹) —— 属静态分析固有局限 + 非对抗威胁模型 (防非蓄意完成度卫生, 非防 spoof); 由"真调用非散文"+ fail-toward-warn + 逃生舱缓解。block 只在高置信"零生产语义引用"。
     - 复用 #134 `--archive-design-only`+reason 逃生舱显式豁免。
   - **🟠 WARN + 持久标记 + ack**: 声称是 dogfood/benchmark/deploy 类但无可链接产物 (ab-results 路径/部署记录), 或未点名符号无法静态核验 → WARN + 写 frontmatter `unverified_claims: [...]` **持久标记**。交互模式归档者可 `--ack-unverified <reason>` 记录人工确认; **但 D auto-issue 兜底不依赖 ack** (见 §2, R2 F3-fix)。
   - **⚪ fail-soft 放行**: 无法提取符号 / grep 失败 / 非代码集成类声称 → 记 soft_error, 不 block 不 warn。
   - **与 #134 `complete` 字段关系 (R2 code-reviewer minor)**: C-block 与 #134 `is_spec_complete` **正交** —— 可 `complete=true` (tasks 全 `[x]`) 却 C-block (死代码); 保留 `complete` 字段不动 (既有 collector 消费方不破坏), `gate_result.verdict` 独立承载 C 判定; openspec-archive Step1 gating 须覆盖 "complete=true ∧ verdict=block" 组合 (逃生舱前置条件相应扩展)。
   - 落 `lib/spec_complete.py` 新纯函数 (符号提取 + 生产引用核验 + 产物抽验, 全 fail-soft, stdlib-only + ripgrep/grep shell-out)。
   - **遥测类声称 (R2 qa minor)**: 遥测/运行时-invoke 核验属 fix A (out-of-scope, 交 DEC-002); 过渡期 C **不**把"遥测"列入产物类别 (无遥测基建则恒 warn 噪音), 该类声称走"无法核验 → warn"通道。

2. **D — 归档不吞未完成 → auto-issue (🟢)**:
   - 归档时若有 deferred/未勾实施项 (逃生舱归档) **或任何 C-warn `unverified_claims`** → 触发 auto-issue 承载残留工作。
   - **ack 解耦 (R2 F3-fix)**: D 触发**不依赖人工 ack** —— unverified 声称无论是否被 ack **都**进 tracker (un-acked 的更危险, 更需兜底; ack 只是交互模式的人工确认记录, 非 tracker 前置)。**headless 默认 (v2.0 Layer 2 自主归档)**: 无人 ack 时**自动创建** tracker issue (非 stall 非静默), 使 fleet 自主归档不重现 gap(D)。
   - **单一 owner (R1 F4)**: `openspec-archive` Step2 为**唯一** issue 创建点; `phase-d-closer` D.2 检出但委托 Step2, 不各自建 (防双入口重复)。
   - **issue-tracker backend 抽象 (R1 F4)**: Forgejo 默认 (`forgejo` CLI); 非-Forgejo 项目 (GitHub adopters) 降级为**输出待创建 issue 草稿 + 提示手动创建** (对称 #134 多-CI-backend out-of-scope 姿态)。
   - **API 失败路径 (R1 F4)**: 建 issue 失败**不静默** —— 打印待创建 issue 内容 + WARN (归档不因此 abort, 但残留工作可见), **绝不静默 fail-soft** (否则复现病根)。
   - **幂等/去重键 (R1 F4)**: issue body 埋 `<!-- archive-tracker: {spec_id} -->` marker; 建前按 marker 搜同 spec 既有 open issue, 存在则不重复开。
   - body 含 spec id + 未完成项/unverified 清单 + 归档 SHA 回链。

3. **tri-state 契约 (R1 F5)**: `lib/spec_complete.py` CLI 沿用 #134 exit code (0=allow / 1=block) + stdout JSON 新增 `gate_result: {verdict: pass|warn|block, blocking_reasons: [], warnings: []}`; `openspec-archive` Step1 + `phase-d-closer` D.2 **读同一 JSON `verdict` 字段** 而非各自解读 exit code (block→exit1+verdict=block; warn→exit0+verdict=warn surface 不阻断; pass→exit0+verdict=pass)。

4. **文档 + schema + 自身 dogfood**: `openspec-archive`/`phase-d-closer` SKILL.md + references 增 C/D gate 描述; `state-snapshot-schema.md` 若新增字段 additive (**不** bump `snapshot_schema_version`); standards 归档惯例补"完成=可核实完成 (有 call-site/产物支撑)"; **修本 draft 自身** —— 补 proposal `## Success Criteria` 段 (符合 `proposal-minimal.md` 模板惯例, dogfood 本 gate 的结构前提)。

## Impact

- **触及面**: `state-scanner/scripts/lib/spec_complete.py` (新增符号提取+引用核验+产物抽验纯函数) + `openspec-archive/SKILL.md` (Step1 C-gate + Step2 D-auto-issue) + `phase-d-closer/SKILL.md`(+references) + `collectors/openspec.py` (若 D 需 surface 归档后 tracker, additive) + `state-snapshot-schema.md` (additive) + standards 归档惯例文档 + 本 proposal 自身补 Success Criteria 段。版本 SOT 5+1。
- **ship 顺序** (承 #134 R6): C 是 read-only 静态核验 (self-contained, 先 ship 安全); D 有 Forgejo API side-effect (幂等 + 失败可见, 后 ship 或同 PR 独立开关)。
- **向后兼容** (Rule #4): C-block 只在高置信死代码窄口 (点名符号 + 零生产语义引用 + fail-toward-warn), 既有正常归档 (无死代码声称) 零影响; C-warn fail-soft; 逃生舱复用 #134 `--archive-design-only`。**已知局限 (非绕过口新增, 显式承认)**: 集成面 alive 信号 (SKILL.md Bash/hooks.json/shell 路径调用) 理论可被伪造调用 spoof 逃 block —— 属静态分析固有 + 非对抗威胁模型 (完成度卫生非防蓄意 spoof), 详见 §What Changes 1 known-limitation。
- **绕过口收口 (R1 F3)**: C-warn 的 `--ack-unverified` **不是**静默绕过 —— 它写持久 frontmatter `unverified_claims` 标记 + D auto-issue 兜底, ack 后残留工作**仍可见可追踪**; 与 #134 gap(c) 的静默绕过相反。
- **Rule #6**: deterministic 符号提取/引用核验 → structural fixture + unit tests + 真树 dogfood (Layer L 归档 spec 作 golden 负例: C 应检出 `phase1_gate` provably 零引用 → block; 正当归档不误 block)。
- **Out-of-scope (显式, 见 DEC-003 §最终选择 + Amendment 1)**:
  - **A** runtime-invocation 探针 (运行时真被 invoke 遥测, **非**静态 grep) — 延后, 交 DEC-20260704-002 先趟形态。C 只做**静态**归档时刻证据, ⊥ A。
  - **E** pre-#134 孤儿 sweep — 独立一次性审计 issue, 本 gate ship 后跑 (复用 C 判据)。
  - 历史无标记 spec bulk migration; 非-Forgejo 全自动 issue 创建 (降级为提示草稿); `implemented→done` 自动晋升。

## Success Criteria

> 每条列可验产物/metric (falsifiable, 对齐 R1 F7); C 误报以**有界**语料声明 (非"零误报"绝对声称)。

- [ ] **C-block golden 负例 (语义级)**: Layer L 归档 spec (`multi-terminal-coordination`) 跑 gate, C 从 deliverables 提取 `phase1_gate`, 剥注释/docstring 后检出其**零生产语义引用** (尽管在 3 个生产 collector 注释/docstring + 108 单测 + docs 有文本提及) → BLOCK (可复现: verdict=block + blocking_reasons 含符号名)
- [ ] **正控 1 — 真实代码引用不误 block**: 有真实 import/调用的符号 → C-block 不触发
- [ ] **正控 2 — 集成面不误 block (R3 tech-lead-fix)**: 经 SKILL.md Bash 调用 或 hooks.json 注册集成 (无 .py import) 的符号 → C-block 不触发 (集成面被识别为 alive)
- [ ] **正控 3 — dynamic-dispatch 不误 block**: 经 `getattr`/`importlib` 反射调用的符号 → C-block 不触发
- [ ] **正控 4 — 通用路径调用不误 block (R4 qa-fix)**: 经 shell/cron/Makefile/CI 按字面路径调用 (如 `m6-phase-b-gate-check.sh` 调 `validate-m6-handoff.py`, 无 .py import) 的符号 → C-block 不触发
- [ ] **正控 5 — 未分类形态 fail-toward-warn**: 落在 alive/散文 两清单之外的生产出现形态 → 降级 warn (非 hard-block), 兑现"误分类偏向不误 block"
- [ ] **C 误报有界 + 判别力 (防 vacuous-pass)**: 语料库 **N≥8** 个已归档正常 spec (列具体 N 个, 须覆盖上述正控 1-4 至少各 1) → C-block 全 **0 例** (falsifiable: 每 spec 列 verdict + 符号核验结果)
- [ ] **C-warn + 兜底**: 无可链接产物的 dogfood/benchmark 声称触发 warn + 写 frontmatter `unverified_claims` 标记, 且 unverified 声称 (**无论是否 ack**) 进 D open issue (未 ack 同样兜底, 更关键)
- [ ] **D 幂等 + 可见**: 带 deferred/ack-unverified 项归档产出**恰 1 个** open issue (重复归档同 spec 不重复开), body 含 spec_id + SHA 回链; API 失败时 issue 草稿打印可见 (非静默)
- [ ] **tri-state 一致**: openspec-archive 与 phase-d-closer 对同一 spec 读同一 `gate_result.verdict`, 二者判定一致 (无解读漂移)
- [ ] **fail-soft 全覆盖**: 全部新增判定 (C 符号提取/引用核验/产物抽验 + D) 解析异常/grep 失败 → 放行 + soft_error, **且每条降级路径有对应 unit test** (R1 F6)
- [ ] **Rule #6**: structural fixture + unit + 真树 dogfood 通过; A/E 显式 out-of-scope 已在 proposal 记录

> **完整范围界定 / 打包取舍 / enforcement 分级理由 / B→C 否证依据 / 风险缓解 / DEC-002 边界**: 见 DEC-20260704-003 (含 Amendment 1, 设计 SOT, 本 proposal 不复制)。

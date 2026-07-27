---
agent: tech-lead
round: R1
verdict: REVISE
scope_check: SCOPE_OK
critical_count: 1
major_count: 4
minor_count: 3
---

# post_spec 审计 R1 — phase-c-gate-path-coverage-not-applicable (tech-lead)

先肯定：核心诊断经代码核实**属实**。proposal:17 引 `aether.py:223-224` `if not runs: return "pending"` — 逐字命中；proposal:18 引 `pre_merge_gate.py:187-188` `pending → VERDICT_WAIT` — 命中。架构落位主张 D1（评估落 gate 侧、`CIStatus` Literal 不动）与代码一致：`_build_output` 的 `pr_ci_status` 是自由 str 非 Literal 校验，gate 侧注入 `"not_applicable"` 无需触碰 backend。授权链与 config.json `_lane` 逐字对齐（「(1) #122 优先落地, 是唯一真机制」）。骨架方向对。以下是必须回修的问题。

## Critical

**TL-1 — 元仓执行上下文 (哪个仓根 / 哪个 main branch / gitlink-only diff 如何处理) 完全未规范, 叠加 fail-toward-covered 使任何不匹配都是"静默无操作", spec 无法证明它在自己的 dogfood 目标仓上真生效**
指涉: proposal:41-52 (§1 "仓根 .forgejo/workflows/"), :49 (`git diff --name-only <main_branch>...<pr_branch>`), :97 (Rule #8 自指 dogfood); 代码 `pre_merge_gate.py:263` `main_branch: str = "main"` + `:368` CLI `--main-branch default="main"`。

三个交织的现实, proposal 均未处理:

1. **default main branch = `"main"`, 但 Aria/aria 用 `master`**。若实际调用未显式传 `--main-branch master`, `git diff master...pr` 在只有 `master` ref 的仓里会失败 → 按 D2 落 `unknown` → gate 行为=现状 (`wait`)。即：机制在它主打修复的那个仓里**静默退回恒 wait**, 而且看起来"正常工作"。

2. **仓根歧义 (submodule vs meta-repo)**。dogfood 场景 (proposal:97 声称"本 cycle 自身 C.2 合并即首个 not_applicable 用例") 的 C.2 是**子模块 aria 本地合并** (Rule 约束1)。那么 cwd 必须是 aria 子模块, 扫的是 `aria/.forgejo/workflows/` (1 个 workflow), diff 用子模块的 `master`。但 proposal 从头到尾只写"仓根", 没定义在 meta-repo 布局下 cwd 落哪、由谁保证。主仓 PR 合并时 (bump gitlink), `git diff --name-only` 对 submodule bump 只吐 gitlink 路径 `aria` 一个 token, 不会展开成 `aria/skills/...`, 主仓那条 `paths: aria/skills/issue-triage/**` 的 workflow 因此判"不触发"。这一条恰好与真实 forgejo 行为一致 (gitlink 变更也不匹配子路径 glob), 但 proposal 没论证过这一点, 属未验证的巧合。

3. **fail-toward-covered 同时是安全网, 也是把 bug 藏起来的地毯**。D2 把"任何不确定 → covered → wait"当纯安全。但本 spec 要根治的**就是恒 wait**。于是：分支名配错 / detached HEAD / shallow clone 缺 main ref / cwd 落错仓 —— 全部 → `unknown` → `covered` → `wait`, 与"机制没装"不可区分。第 6 次复发会以"机制在跑但一直 covered"的形态出现, 比现在更难诊断 (memory `feedback_noop_in_test_env_hardening_needs_mechanism_assertion` / `feedback_check_predicate_must_validate_against_real_data_range`)。

建议修法 (三者一并): (a) spec 明确规定评估的 cwd = **执行 C.2 合并的那个仓** (dogfood 即 aria 子模块), 并显式说明 gitlink-only diff 的处理语义; (b) `main_branch` 不得依赖 `"main"` 默认, 须由调用方 (workflow-runner) 传真值, 并把"main ref 不存在导致 diff 失败"与"diff 成功但空"**区分为不同 reason**; (c) `unknown`(尤其 git/parse 失败成因) 必须像 not_applicable 一样进 D8 的 AI surface 警告面 —— 否则"评估失败"永远沉默。补 SC: 错误 main branch ref / 非目标 cwd → `unknown` 且 reason 可辨, 且 workflow report 出可见诊断行。

## Major

**TL-2 — 判定谓词三档不构成互斥+全覆盖分割, 第 47 行与第 51 行自相矛盾**
指涉: proposal:47 (「`paths-ignore` / anchors / 无法辨识构造 → 该 workflow 按 `covered`」) vs :51 (「任一环节不确定 → `unknown`」)。
同一个"识别不了的构造", 按 :47 是"该 workflow=covered"(整体 covered), 按 :51 是"环节不确定"(整体 unknown)。两条给不同 decision 标签与不同 reason, SC-6 (paths-ignore→covered) 与 SC-7 (畸形 YAML→unknown) 也要靠这条边界区分。虽然 covered 与 unknown 在 gate 侧行为一致 (proposal:60 都=现状 wait), 但标签/可观测/测试期望不同, 属实现顺序裁决=未定义 (memory `feedback_predicate_tiers_need_total_partition_proof`)。
建议: 把三档写成可证的全分割 —— **解析失败 (YAML 坏, 文件读不了)** → `unknown`；**解析成功 ∧ 任一 workflow 会触发或含不建模构造** → `covered`；**解析成功 ∧ 全部 workflow 确定不自动触发** → `not_applicable`。三者互斥且穷尽, 删掉 :51 那句过宽的"任一环节不确定→unknown"。

**TL-3 — "真实语料"表与 D7 把 `build-aria-runner.yaml` 误标为"仅 workflow_dispatch", 实际它有 `push` + `paths` 触发, 语料证据错**
指涉: proposal:26 (表格「`build-aria-runner.yaml` | ❌ 仅 workflow_dispatch | n/a」) 与 :92 (D7「语料实证 build-aria-runner / tripwire」); 真实文件 `/home/dev/Aria/.forgejo/workflows/build-aria-runner.yaml:22-25`:
```
  push:
    branches: [feature/aria-2.0-m0-prerequisite]
    paths:
      - 'aria-orchestrator/docker/aria-runner/**'
```
它**不是** dispatch-only —— 带 `push` + `paths` 过滤 (外加 branches)。D7 用它论证"dispatch/schedule-only→零覆盖贡献"是拿了个反例。只有 `submodule-gate-tripwire.yml` 才真是 dispatch-only (已核实: 其 `on:` 仅 `workflow_dispatch`)。这会伤及 D5 "语料=本仓 4 真实 workflow" 作为 parser fixture 的正确性：若照现表把 build-aria-runner 的期望写成"零覆盖", 就是 fixture 形态漂移=假绿 (memory `feedback_reused_code_fixture_shape_drift_false_green` / `feedback_doc_claims_need_diff_verification_and_variant_sweep`)。
建议: 改表格该行为"push(branches+paths) + workflow_dispatch, paths=`aria-orchestrator/docker/aria-runner/**`"；D7 只保留 tripwire 作 dispatch-only 语料；并把 build-aria-runner 作为"push 有 paths 但 branches 也在场→branches 不建模、按 paths 交集判"的正例 fixture (正好压 proposal:48 的 branches-不建模主张)。

**TL-4 — not_applicable 跳过 (a) PR CI 查询后, NIE-propagation 与 not_applicable 的交叉未被任何 SC 钉死, 正交性声明 (proposal:61) 缺回归锁**
指涉: proposal:56-61 (§2 评估点在 query(a) 之前, not_applicable 跳过 (a)、(b) 照跑), :61 (声称 NIE-propagation 路径"全部不变"); 代码 `pre_merge_gate.py:317-341` (query 顺序: (b) in-flight 先 → (a) PR CI 后; NIE 于 :319/:332 propagate)。
not_applicable 只跳 (a)。stub backend (GHA, probe=True, query 抛 NIE) 场景下, NIE 目前靠 (b) query_branch_in_flight **先跑**触发。proposal 说 (b) 照跑, 所以 NIE 经 (b) 仍 propagate —— 逻辑成立, 但**依赖"(b) 无条件先于 (a)"这一隐性不变量**。一旦未来重构让 (b) 在 not_applicable 时也被跳, NIE 就被 not_applicable 掩盖, Rule #8 静默降级复活。SC-9/SC-10 都假设 backend 正常返回, 无一条测 "not_applicable ∧ stub backend → gate 仍 abort (NIE 经 (b) 传出)"。
建议: 补 SC —— decision=not_applicable ∧ backend probe=True 但 query 抛 NIE → gate 仍 raise NIE (不被 not_applicable 吞), 把"(b) 无条件先跑"这条正交性前提锁进测试 (memory `feedback_default_value_flip_needs_lock_in_test` 同理：交叉不变量须显式断言)。

**TL-5 — `_lane` 过渡规则 (2) 退役 (主仓 Phase D) 与 v1.65.0 gitlink bump 的落地顺序未固定, 存在"规则已退、机制未在 pinned 子模块生效"的覆盖空窗**
指涉: proposal:76-78 (§6 "机制落地后改写 `_lane`"), Impact 表 :142-143 (「发版 5 文件 + 主仓 gitlink」与「主仓 `_lane` Phase D 改写」两行未定序); config.json `_lane` 现状 (过渡规则 (2)「verdict=wait 一律上报 owner」仅文档级)。
机制代码在 aria 子模块 v1.65.0；`_lane` 退役在主仓。gate 实际加载的是**主仓 gitlink 钉住的那个子模块 checkout**。若先改主仓 `_lane` 退掉规则 (2)、后 bump gitlink, 中间就有一段：过渡规则 (2) 已终结 (verdict=wait 不再上报 owner) 而 gitlink 仍指向没有 not_applicable 机制的旧子模块 —— 恰好是"既不上报、也不识别 not_applicable"的裸奔窗口 (memory `feedback_freeze_task_must_coland_with_volatile_state_phase` / `feedback_sequenced_multirepo_gitlink_bump`)。
建议: 明确 §6 —— `_lane` 规则 (2) 的退役编辑必须与"主仓 gitlink bump 到含 not_applicable 机制的 v1.65.0"**同一个主仓 commit 落地 (co-land)**, 不得分两次。proposal 直接写死这条时序。

## Minor

**TL-6 — §2 "评估点在 query (a) 之前"的措辞与代码真实 query 顺序 ((b) 先 (a) 后) 不对齐, 易误导实现者**
指涉: proposal:56 ("query (a) 之前") vs 代码 `pre_merge_gate.py:315-316` 注释与 :318 ((b) main in-flight FIRST)。措辞上"(a) 之前"读着像整个查询前, 但实际 (b) 在 (a) 前且 not_applicable 时 (b) 仍要跑。建议改写为"precheck 之后、**(a) PR CI 查询之前**插入评估；(b) main in-flight 查询保持无条件执行 (顺序仍 (b)→跳过(a))", 与 TL-4 的不变量表述统一。

**TL-7 — parser 假设 forgejo 的 `pull_request: paths:` 语义与 GHA 完全一致, 未在 proposal 内留一句证据/probe**
指涉: proposal:50 ("glob 匹配... 语义对齐 forgejo/GHA paths 规则"), :118 (SC-14)。forgejo Actions 的 paths 过滤大体沿用 GHA, 但 `**`/尾 `/**`/`?` 的边界个案 (尤其 forgejo 版本差异) 值得一句实证锚点。建议: SC-14 表驱动语料显式标注"期望值来源 = forgejo 官方 paths 文档 / 实测", 而非仅"对齐 GHA"。低风险, 但避免 memory `feedback_verify_structural_premise_against_official_docs` 的坑。

**TL-8 — `path_coverage_enabled` 默认 `true` 翻默认值改变**所有**装机的 gate 行为, owner sign-off 面应显式覆盖"默认 true"而非仅"机制存在"**
指涉: proposal:70 (D4 默认 true) + :7 (授权链)。owner 2026-07-25 定案是"#122 优先落地是唯一真机制", 但"默认 on 影响全部仓"是机制内的一个设计选择。D4 的 fail-toward-covered 安全论证成立, 且 Status 行已列"待 owner sign-off", 所以只是提醒：sign-off 请求里点名"默认 true"这一项, 别让它混在机制整体里被默认批准 (memory `feedback_default_value_flip_needs_lock_in_test` 已配 SC-12 锁定, 授权面补一句即可)。

## 结论

诊断扎实、架构落位 (gate 侧 D1)、与 no_ci_fallback/enabled:false/ci_backends:[] 的正交性、授权链 (对齐 config.json `_lane` 逐字) 都经得起代码对照, scope 无蔓延 (SCOPE_OK)。但有一个 Critical (元仓执行上下文 + main/master 默认 + fail-toward-covered 静默无操作三合一, 会让 spec 在自己的 dogfood 目标仓上悄悄变 no-op 而无法证伪) 和四个 Major (谓词分割不闭合、build-aria-runner 语料事实错、NIE×not_applicable 回归缺测、`_lane` 退役与 gitlink bump 未 co-land), 均须进 Phase B 前回修。判 **REVISE**：核心机制值得做, 但"如何证明它没静默失效"是这个 spec 的命门, 目前没写。

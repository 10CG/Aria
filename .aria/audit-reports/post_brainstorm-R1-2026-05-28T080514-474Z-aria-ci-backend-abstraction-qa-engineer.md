---
checkpoint: post_brainstorm
mode: convergence
round: 1
agent: qa-engineer
target: .aria/decisions/2026-05-28-ci-backend-abstraction-brainstorm.md
change_id: aria-ci-backend-abstraction
change_id_status: prospective (brainstorm phase)
timestamp: 2026-05-28T08:05:14Z
vote: PASS_WITH_WARNINGS
critical_count: 1
major_count: 2
minor_count: 2
---

# Post-Brainstorm Audit R1 — QA Engineer
## aria-ci-backend-abstraction

---

## §Findings

### F1 — CRITICAL: GHA stub NotImplementedError 调用路径未规约，存在 silent gate bypass 风险

- **id**: `a3f2c1e8`
- **severity**: CRITICAL
- **category**: safety
- **scope**: deliverable-B + deliverable-C + hard-constraint-4
- **type**: missing-specification
- **summary**: DEC Hard Constraint #4 规定 `NotImplementedError` 必须含可操作 message，但未规约 `gate_check()` 遇到该异常时的路由行为。GHA `probe()` 返回 True 后若两个 query 方法均 raise NIE，`gate_check()` 是 crash（unhandled exception，pre-merge 失败）还是 catch 并路由到 `no_ci_fallback: skip_with_warning`（gate bypass，verdict=green）？两种行为对 Rule #8 的影响截然相反。

- **rationale**: 当前 `gate_check()` 捕获 `detect_aether()`+`_query_aether()` 的异常路径已有测试（test_case_e/e2），但这些测试 mock 的是内部函数返回 `(False, None, msg)` 元组，而非 `raise NotImplementedError`。重构后若 registry 选中 GHA stub（gh installed，aether not installed），`backend.query_pr_ci()` 抛出 NIE，该异常是否被 `gate_check()` 的 try/except 捕获取决于实现细节，而 DEC 未约束这一细节。具体危险场景：未安装 aether 的 CI runner（如 GitHub Actions self-hosted worker）装有 `gh`，GHA stub probe 成功，gate 被 NIE crash 或 skip_with_warning 静默放行，Rule #8 的两个检查均不执行。

- **recommended_action**: DEC 必须在 Deliverable B 规约中明确指定：当 selected backend 的 `query_*()` 抛出 `NotImplementedError` 时，`gate_check()` 的处理策略。推荐：catch NIE 并路由到 `no_ci_fallback` 配置（与现有 `no_aether_output` 语义等价），而非 skip_with_warning 静默 green，即 NIE = backend_not_functional，等同于 backend 不可用。同时 Deliverable C 必须新增测试：`test_gha_probe_true_query_nie_routes_to_fallback`，验证该路由行为是明确定义的而非偶发。此 gap 需在 Spec（A.1）中以伪代码约束 `gate_check()` 异常边界，使实现者无歧义。

---

### F2 — MAJOR: 探测优先级顺序（Aether-first vs GHA-first）在 DEC 中未指定

- **id**: `b7d9e042`
- **severity**: MAJOR
- **category**: specification-gap
- **scope**: deliverable-A + deliverable-B + Q3-decision
- **type**: ambiguity
- **summary**: Q3(b)"Config-first + probe fallback"选定，但 DEC 未指定默认 probe 顺序。boundary audit memo 草图使用 `priority=100`（Aether）vs `priority=50`（GHA），但 DEC 中此细节已消失。"现网 100% 走 Aether"的保证依赖正确的 probe 顺序——如果 GHA probe 先执行且成功，则选中 stub backend，Rule #8 检查结果错误。

- **rationale**: DEC §收敛 design "现网 100% 走默认值 — auto-detect probe 序列正确激活 Aether" 中 "序列正确" 四字是未经测试的断言，依赖 `__init__.py` (registry) 实现时沿用 boundary audit memo 中的 priority 整数。然而 DEC deliverable A 仅说"registry"，未包含任何关于注册顺序或 probe 序列的约束。Spec（A.1）阶段实现者可能因疏忽将 GHA 列在 Aether 之前，导致现网所有使用 aether + gh 双安装的机器（如 aria-orchestrator runner，两者都可能存在）选中 GHA stub 而非 Aether full。

- **recommended_action**: DEC 或等待 Spec A.1 时须明确：(1) 默认 probe 顺序为 Aether-first，(2) 若 config 未覆盖 `ci_backends` 则 registry 的内置顺序是 `[AetherBackend, GitHubActionsBackend]`，(3) Deliverable C 新增测试：`test_aether_takes_precedence_when_both_probe_true`——mock 两个 backend 的 `probe()` 均返回 True，验证 `resolve_ci_backend()` 返回 AetherBackend 实例而非 GHA。

---

### F3 — MAJOR: Deliverable C 估时 2h 低估：真实重写范围是 10 mock×3 行 + 5 类新增测试

- **id**: `c8a1f356`
- **severity**: MAJOR
- **category**: estimation
- **scope**: deliverable-C
- **type**: scope-underestimate
- **summary**: DEC 描述"~10 处 `mock.patch.object(gate, 'detect_aether', ...)` rewrite"，但实测 `test_pre_merge_gate.py` 有 10 处 `detect_aether` mock + 额外 13 处 `verify_aether_in_flight_flag` + `_query_aether` mock（总计 23 处 `mock.patch` 行，21 个 test method）。新增测试至少 5 类（F1 NIE routing × 1，F2 probe ordering × 1，alias key path × 2，GHA stub NIE message format × 1，backend registry × 2）。2h 预算覆盖 23 行 mock 重写 + 7+ 新测试设计 + 验证全套不 regression 存在压力。

- **rationale**: 重写不是纯机械替换：`mock.patch.object(gate, "detect_aether")` → `mock.patch.object(AetherBackend, "probe")` 同时需要调整 mock 的返回值 shape（当前返回 `(True, "/usr/local/bin/aether")` 元组；新 `probe()` 可能返回 `bool` 或 `str | None`，需 DEC 约定 probe() 返回类型），以及 `verify_aether_in_flight_flag` 的 mock target 也需迁移（该方法可能移入 `AetherBackend`）。每处变更需验证 assertion 行为不变（constraint #1）。加上 F1/F2 要求的新测试，2h 是乐观下限。

- **recommended_action**: 将 Deliverable C 预算调整为 2.5-3h，或在 Spec A.1 中明确将"新增 5 类测试"单独拆出为子任务，避免 Phase B 实施时因时间压力跳过新测试（特别是 F1 NIE routing 测试，该测试对 Rule #8 安全性至关重要）。同时 Spec 须在 Deliverable A 中约定 `probe()` 方法返回类型（`bool` 推荐，binary 路径通过 `AetherBackend.__init__` 或 property 存储），使 mock 重写方向明确。

---

### F4 — MINOR: Deliverable E（Rule #6 substitute，1h）对标 Sprint 1 明显低估

- **id**: `d4b2e719`
- **severity**: MINOR
- **category**: estimation
- **scope**: deliverable-E
- **type**: scope-underestimate
- **summary**: Sprint 1 Rule #6 substitute（forgejo-hosts-parameterization）产出物：27 new unit tests + 12 AC behavior 表 + edge case cheatsheet + dual-path dogfood smoke + 631-test full suite green，实际工作量证明远超 1h。本 Spec 的 deliverable E 要求等价产出（27+ unit tests + fixture README + dual-path dogfood），估时 1h 与先例不符。

- **rationale**: Sprint 1 的 README 本身就是该结构性 fixture 文件（当前查阅的 `aria-plugin-benchmarks/forgejo-hosts-parameterization/README.md`）：4 处 hardcode map + 12 AC 行为表 + edge case 表 + dogfood smoke 结果，写作密度高。本 Spec 的 Rule #6 substitute 需为"CI backend 抽象"场景创建等价文档，内容包含 backend probe/query contract + alias key 行为表 + NIE routing 边缘情况。1h 写不完 fixture + 27 tests + dogfood。

- **recommended_action**: 将 Deliverable E 预算调整至 1.5-2h，并明确 Rule #6 substitute 的最小产出清单（以 Sprint 1 README 为模板，至少含：4 个 backend contract ACs + alias 行为表 + GHA stub NIE 路由行为 + dogfood evidence）。此不影响 Spec 通过，但应在 A.1 中记录以设置实施者期望。

---

### F5 — MINOR: 旧 key alias 的"dead code rot"风险无测试保鲜机制

- **id**: `e5c3d081`
- **severity**: MINOR
- **category**: maintainability
- **scope**: deliverable-B + hard-constraint-3
- **type**: missing-test-invariant
- **summary**: DEC Hard Constraint #3 要求 `no_aether_fallback` + `primitive_preference` 旧 key alias 持续工作并 emit deprecation warning，但未规约任何防止 alias 路径静默失效的机制（如 deprecation warning 本身被删除，或 alias 被重构时意外移除）。

- **rationale**: Alias 旧 key 是"dead code 护栏"——现网零项目使用，因此回归测试唯一价值是防止代码腐化。DEC 说"unit test 显式 cover"，但未说明测试需 assert 什么：仅 assert `verdict` 相同？还是同时 assert `raw_message` 含 `DeprecationWarning` 字符串？后者的缺失意味着未来 PR 可以修改 alias 逻辑而不触发测试失败，alias 行为静默改变。Sprint 1 的对应场景（C3 保留旧 DEFAULT_CONFIG 作 Python-layer fallback）通过 `TestLoadConfigEnvOverride::test_config_json_wins_over_default_when_no_env` 明确 assert 了 value 而非仅 exit code。

- **recommended_action**: Spec A.1 中为 Deliverable C 补充：alias 测试必须 assert (a) 使用旧 key 的 config 产生与新 key 等价的 `verdict` 和 `primitive_used`，(b) `raw_message` 或 stderr 含 `deprecated` / `DeprecationWarning` 字符串。这样 alias 的 "message" 和 "behavior" 两个方面都被锁定，防止腐化。

---

## §Per-dimension verdict

### (a) 实质收敛：决策是否真正解决 C5+C6，且可测试

5 个决策从 boundary audit 出发，Q1(b) stub-vs-full split 是成熟 abstraction 模式，Q2(b) alias 是合理前向兼容，Q3(b) config-first+probe 保护现网 UX，Q4(b) 双方法 dataclass 1:1 mirror Rule #8 语义，Q5(b) 文字通用化是正确方向。

**主要收敛**：Q4（双方法 + dataclass）是最高质量决策，直接可测试——`assert hasattr(backend, "query_pr_ci") and hasattr(backend, "query_branch_in_flight")` 是一行 structural test。Q2 现网调查（grep 6 sibling 项目 0 hit）是有效的风险消除证据。

**未收敛部分**：Q3 "Config-first + probe fallback" 描述了策略但未完成收敛——probe sequence（谁先谁后）和 NIE 异常处理路径（GHA probe True 但 query NIE 时的 gate 行为）是 C5+C6 的核心可测性要求，DEC 在 post-brainstorm 阶段留下了两个必须在 Spec A.1 中填补的 testability gap（见 F1、F2）。

**结论**：实质 70% 收敛，F1 需在 Spec 中补充明确约束，否则 Phase B 实施者有两种合理但行为相反的实现选择。

### (b) 硬约束完整性：6 条约束是否全部可测试

| # | 约束 | 可测试性 |
|---|------|---------|
| 1 | Aether 行为零变化（全 test PASS） | ✅ 可测 — CI 自动验证 |
| 2 | Rule #8 mechanism 不可降级（两检查保留） | ✅ 可测 — `assert query_pr_ci` + `assert query_branch_in_flight` in output schema |
| 3 | Alias 旧 key 完整工作 + deprecation warning | ⚠️ 部分可测 — behavior 可测，warning emit 未明确 assert（F5） |
| 4 | GHA stub NIE 含可操作 message | ⚠️ 部分可测 — message 内容可 assert，但 NIE **被调用时的 gate 行为**未约束（F1） |
| 5 | Standards 子模块零触碰（grep 验证） | ✅ 可测 — grep 证据已在 DEC |
| 6 | GHA 真实现不塞进本 Spec | ✅ 可测 — code review 层面 |
| 7 | Ship slot 严守 v1.31.0 | ✅ 可测 — plugin.json version 字段 |

约束 3 和 4 需补充，见 F1/F5。

### (c) 风险识别：alias dead code rot、test rewrite blast radius、GHA stub silent passing

- **GHA stub silent passing（F1）**: 这是实际存在的 CRITICAL 风险。DEC 目前约束了 NIE message 内容，但未约束 gate_check() 如何处理 NIE——unhandled exception vs no_ci_fallback routing 对 Rule #8 行为截然相反。
- **probe ordering（F2）**: MAJOR 风险，DEC 的 "probe 序列正确" 断言需要一个明确测试。
- **test rewrite blast radius（F3）**: 实测 23 处 mock.patch（10 detect_aether + 13 其他），加上 probe() 返回类型变更，2h 压力真实存在。
- **alias dead code rot（F5）**: MINOR，但 deprecation warning 的 assert 缺失会导致 alias 的"message"部分腐化无感知。
- **Missing risk not in DEC**: `AetherBackend.probe()` 返回类型（bool vs tuple）未约束。当前 `detect_aether()` 返回 `(bool, str | None)` 元组；若 `probe()` 也返回元组，mock 重写方式与 DEC 描述的 `return_value=True` 不兼容，会导致 test rewrite 方向错误。

### (d) DEC 文档质量：验收标准隐式可测性

Q4 验收标准最好（contract interface 直接 assert）。Q1/Q3 的验收标准偏 prose（"生产 100% 不受影响"），缺少等价的 test ID 映射。Deliverables 表有估时但无 acceptance criteria 行——与 Sprint 1 forgejo-hosts Rule #6 substitute README 对比，后者有 12 AC 行为表（每条含 Test coverage 列），本 DEC 尚在 brainstorm 阶段这是可接受的，但 Spec A.1 需补全。

Rule #5 compliance（变更在项目 openspec/changes/ 下，非 standards/）：DEC §Cross-references 的 Phase D archive 路径 `openspec/archive/{date}-aria-ci-backend-abstraction/` 正确。

### (e) 实施可行性：8.5h 估时 + 各 deliverable 拆解准确性

| Deliverable | DEC 估时 | 评估 |
|-------------|---------|------|
| A（ci_backends/ 目录，4 文件） | 3h | 合理，ABC stub 相对机械 |
| B（pre_merge_gate.py 改用 backend） | 1h | 合理，~30 LOC 变更，但 NIE routing 决策（F1）若未在 Spec 明确，B 工作量会增大到 1.5h |
| C（test rewrite + 新增测试） | 2h | **低估**（F3），实测 23 mock 行 + probe 返回类型变更 + 5+ 新测试类。建议 2.5-3h |
| D（CLAUDE.md + SKILL.md 文字） | 1h | 合理，文本工作 |
| E（Rule #6 substitute） | 1h | **低估**（F4），Sprint 1 先例表明等价工作量 1.5-2h |
| F（SOT bump） | 0.5h | 合理 |

**总估时调整建议**：8.5h → **10-10.5h**，仍在 boundary audit memo "~8-12h L3" 区间内，不影响整体可行性。

---

## §Final vote

**PASS_WITH_WARNINGS**

5 个战略决策的方向正确且内部自洽；CRITICAL F1（GHA NIE routing 行为未规约）和 MAJOR F2（probe 优先顺序未指定）必须在 Spec A.1 中以伪代码/AC 的形式填补，否则 Phase B 实施者面临两个行为相反的合法选择，Rule #8 安全性无法通过 Deliverable C 的测试验证。这两个 gap 适合在 post_spec audit 阶段收敛，不必退回 brainstorm。

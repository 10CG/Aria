---
checkpoint: post_spec
mode: convergence
round: 1
agent: qa-engineer
target: openspec/changes/aria-ci-backend-abstraction/{proposal.md, tasks.md}
change_id: aria-ci-backend-abstraction
timestamp: 2026-05-28T10:46:14Z
vote: REVISE
critical_count: 0
major_count: 4
minor_count: 4
---

## §Findings

### F-01 (d83fe5c1)

- **severity**: major
- **category**: testability
- **scope**: tasks.md Task 3.2
- **type**: count_error
- **summary**: GateCheckTests 实际 7 个 test methods, tasks.md 写成 "(15 cases)" 相差 8
- **rationale**: 经 `python3 -c "..."` 逐类统计验证, 实际分布为: ComputeVerdictTests(4), TranslateInFlightRunTests(3), GateCheckTests(7), FallbackTests(3), NormalizePrCiStatusTests(4), 总计 21。Task 3.2 的描述 "GateCheckTests (15 cases)" 错误, 且 Task 3.1 提到的 "TestDetectAether" 类在实际测试文件中根本不存在, detect_aether() 的行为是通过 GateCheckTests 和 FallbackTests 的 mock 间接覆盖, 没有专门的 TestDetectAether 类。如果实施者按照 tasks.md 的数字规划重写工作量 (15+4+2=21 的切割方式), 会对类结构产生错误预期, 导致重写时遗漏 TranslateInFlightRunTests 和 NormalizePrCiStatusTests 的 mock 适配评估。
- **recommended_action**: tasks.md Task 3.1 删除 "TestDetectAether" 错误类名; Task 3.2 的 "(15 cases)" 改为 "(7 cases)"; 补充说明 TranslateInFlightRunTests(3) 和 NormalizePrCiStatusTests(4) 是纯函数测试, 无需 mock target 改动; FallbackTests(3) 需要 mock `resolve_ci_backend` 返回 None 代替 `detect_aether` 返回 False。这是任务描述精度问题, 但不影响实施者最终能验证到正确的 21 个 test methods。

---

### F-02 (8cc465f0)

- **severity**: major
- **category**: testability
- **scope**: tasks.md T-tests 3.1-3.12 vs proposal AC-7.2
- **type**: gap
- **summary**: AC-7.2 要求 "≥27 new unit tests" 按模块分布 (base.py 5+ / aether.py 8+ / github_actions.py 3+ / registry 5+ / alias normalize 3+ / pre_merge_gate integration 3+), 但 tasks.md T-tests 3.5-3.10 仅在 test_pre_merge_gate.py 中新增 16 个 test case, 且无任何 task 负责创建 ci_backends/ 的专用测试文件
- **rationale**: AC-7.2 的分布表明新测试必须覆盖 ci_backends/base.py、aether.py、github_actions.py 各自的独立行为 (如 CIStatus dataclass 字段验证、probe() 的 subprocess mock 行为、NIE message 内容验证等), 这些在 test_pre_merge_gate.py 里无法自然存放。而 T-tests 3.5-3.10 新增的 16 个 test case 加上 21 个改写后总计 37 个, 其中 "new tests" 只有 16 个, 不满足 "≥27 new unit tests" 的声明。T-rule6 5.4 的 "T-tests delivers 30+" 也似乎把 21 rewritten 算进去了, 但 AC-7.2 明确写 "≥27 new unit tests 分布" 这个措辞指向净增量。无论哪种解读方式, tasks.md 都缺少一个 task 来创建 `aria/skills/phase-c-integrator/tests/test_ci_backends.py` (或等价文件), 负责对 ci_backends/ 包内各文件进行独立单元测试。
- **recommended_action**: 在 T-tests 末尾新增任务 3.13: "Create `tests/test_ci_backends.py` — 6 new test classes: TestCIStatusDataclass(5 cases) + TestInFlightStatusDataclass(2 cases) + TestAetherBackendProbeIsolated(4 cases) + TestGHABackendProbeSubprocess(3 cases) + TestBackendRegistry static structure(3 cases) + TestNormalizeConfigUnit(3 cases). 合计 ≥20 new cases, 与 3.5-3.10 的 16 cases 合计 ≥36 new tests, 确保 AC-7.2 ≥27 new tests 声明成立。" 并修正 AC-7.2 措辞使 "new unit tests" 定义清晰。

---

### F-03 (30f23d6b)

- **severity**: major
- **category**: testability
- **scope**: tasks.md T-rule6 Task 5.5
- **type**: runability
- **summary**: Task 5.5 dogfood 命令双重错误: (1) 使用 `--pr` flag 但实际 CLI 只有 `--pr-branch`; (2) `python3 -m phase_c_integrator.scripts.pre_merge_gate` 无法执行 (scripts/ 下无 __init__.py, 无 package 安装结构)
- **rationale**: 经实地验证, 当前 CLI 使用 `--pr-branch PR_BRANCH` 参数 (确认: `python3 pre_merge_gate.py --help` 输出)。`scripts/` 目录中仅有 `pre_merge_gate.py` 和 `submodule_gate.sh`, 无任何 `__init__.py`, 无法通过 `-m` 模块语法调用。即使在 v1.31.0 实施后加入 `ci_backends/` 包并添加 `ci_backends/__init__.py`, 若不同时给 `scripts/` 和其父目录添加 `__init__.py` 并安装 package, `-m phase_c_integrator.scripts.pre_merge_gate` 仍然失败。相比之下 Task 5.5 的 `python3 -c "from ci_backends.aether import AetherBackend; ..."` 是可行的 (需在 `scripts/` 目录下执行或设置 PYTHONPATH), 但 pre_merge_gate 的 dogfood 调用有误。dogfood smoke 是 Rule #6 substitute 的重要证据, 命令写错会导致实施者照搬后执行失败。
- **recommended_action**: Task 5.5 第二条命令改为: `python3 aria/skills/phase-c-integrator/scripts/pre_merge_gate.py --pr-branch <test-branch> --config-file .aria/config.json`. 同时在 5.5 + 5.6 的 `python3 -c "from ci_backends.aether import AetherBackend; ..."` 命令前注明 cwd 和 PYTHONPATH 要求: `cd aria/skills/phase-c-integrator/scripts && python3 -c "..."` 或等价的 `PYTHONPATH=aria/skills/phase-c-integrator/scripts python3 -c "..."`。

---

### F-04 (6829b550)

- **severity**: major
- **category**: testability
- **scope**: proposal §B.4
- **type**: incompleteness
- **summary**: B.4 pseudocode 引用 `_compute_verdict(pr_status, in_flight, cfg)` 但该函数在整个 Spec 中未定义, 且当前代码不存在此函数; 实施者需自行推断其签名、行为契约、以及 `primitive_used` 字段如何从 backend.name 填充
- **rationale**: 当前 `gate_check()` 将 verdict 计算完全内联, 通过 `_build_output()` 接收 `primitive_used: str` 参数。B.4 重构后把这块逻辑外移到 `_compute_verdict()`, 但 Spec 未指定: (1) `_compute_verdict` 的完整签名; (2) 它是否调用 `_build_output()` 内部, 还是只返回 verdict 字符串; (3) `primitive_used=backend.name` 如何传入; (4) 已有的 `compute_verdict(main_in_flight_runs, pr_ci_status)` 函数 (L217-228) 与新的 `_compute_verdict` 是同一个还是不同的。关键测试风险: test_case_a 断言 `out["primitive_used"] == "aether-ci-cli"`, 此断言在重构后依赖 `backend.name == "aether-ci-cli"` 经 `_compute_verdict` 正确传到输出 dict。如果实施者错误地把 `primitive_used` 硬编码或遗漏, AC-1.1 会因 "primitive_used" 断言失败而无法 PASS。
- **recommended_action**: 在 proposal §B.4 或 §B.5 之后新增 §B.6 "_compute_verdict() 函数草案", 给出完整签名: `def _compute_verdict(pr_status: CIStatus, in_flight: InFlightStatus, cfg: dict, backend_name: str) -> dict` 并显示它调用 `_build_output(...)` 时传入 `primitive_used=backend_name`。同时说明现有 `compute_verdict()` (纯函数, 用于 ComputeVerdictTests) 保留不变, `_compute_verdict()` 是新增的 gate-level wrapper。

---

### F-05 (3686dd32)

- **severity**: minor
- **category**: testability
- **scope**: proposal §AC-5.1
- **type**: count_error
- **summary**: AC-5.1 声称 "4 个 abstract member" 但后跟列表实际列出 5 项, 且其中 2 项 (name/priority) 是 ClassVar 非 abstract method
- **rationale**: Python ABC 语义中, `@abstractmethod` 装饰的 method 才是 "abstract member"。base.py pseudocode 中 abstract methods 是 3 个: `probe()`, `query_pr_ci()`, `query_branch_in_flight()`。`name: ClassVar[str]` 没有默认值 (实质上是必填的 ClassVar), `priority: ClassVar[int] = 0` 有默认值。AC-5.1 的 "4" 与列出的 5 项、以及真正 abstract 的 3 个都不匹配。若 QA reviewer 在 3 个月后按 AC-5.1 验收, 会对 "4 abstract member" 的意图产生困惑, 不知道是否应该为 `name` 或 `priority` 添加 `@abstractmethod`。
- **recommended_action**: AC-5.1 修改为: "`CIBackend` ABC 含 2 个必填 ClassVar (`name: ClassVar[str]`, `priority: ClassVar[int] = 0`) + 3 个 `@abstractmethod` (`probe(cls)`, `query_pr_ci()`, `query_branch_in_flight()`)". 数字和语义匹配, 3 个月后 reviewer 可直接 grep `@abstractmethod` 验证。

---

### F-06 (90394899)

- **severity**: minor
- **category**: testability
- **scope**: proposal §A.2 base.py + §B.3 resolve_ci_backend
- **type**: dead_design
- **summary**: `CIBackend.priority: ClassVar[int]` 在 base.py pseudocode 中定义并有注释 "higher = preferred when multiple probe()=True", 但 `resolve_ci_backend()` pseudocode 使用 BACKENDS list 顺序 (static-import order) 而不是 priority 属性, priority 在实际执行路径中从不被读取
- **rationale**: 在 base.py pseudocode 中: `priority: ClassVar[int] = 0  # higher = preferred when multiple probe()=True`. 但 B.3 的 `resolve_ci_backend()` 中 auto-detect 路径是 `for backend_cls in BACKENDS: if backend_cls.probe(): return backend_cls()`, 完全按照 BACKENDS 列表顺序, 不对 priority 排序。这意味着 `priority` 是 dead field: AetherBackend.priority=100, GitHubActionsBackend.priority=50 的设定不会对 probe 顺序产生任何实际影响。这给未来添加第三个 backend 的实施者制造误导: 他们会以为设置 priority=75 就能插入到 Aether 和 GHA 之间, 但实际上必须修改 __init__.py 的 BACKENDS 列表顺序。同时 AC-4 没有任何测试要求验证 "priority 被忽略" 或 "BACKENDS 顺序即优先级", 存在设计意图和行为分裂的隐性债务。
- **recommended_action**: 两选其一: (a) 删除 priority ClassVar, 注释 base.py 说明 "order in BACKENDS list = precedence; classmethod does not read priority attribute"; (b) 在 resolve_ci_backend() 中实际使用 priority 排序: `sorted(BACKENDS, key=lambda b: b.priority, reverse=True)`. 选 (a) 更简单且与 Hard Constraint #8 静态列表设计一致。如果保留 priority (选 b), 需在 AC-4 加一个 test case: `test_custom_priority_overrides_list_order`。

---

### F-07 (8d648072)

- **severity**: minor
- **category**: testability
- **scope**: proposal §B.4 + tasks.md T-docs
- **type**: accuracy
- **summary**: 现有 `gate_check()` docstring 明确声明 "Exceptions are caught and translated into verdict=fail with raw_message — callers can rely on a structured return rather than try/except", 而 B.4 重构后 NIE 必须 propagate (Hard Constraint #7), 这使 docstring 成为错误的 API contract 声明; 但 T-docs 任务中未包含 gate_check() docstring 更新
- **rationale**: 当前 pre_merge_gate.py L282-283 docstring 保证调用者不需要 try/except。Hard Constraint #7 + AC-2.3 明确规定 NIE 必须 raise to caller, 这是一个有意为之的 break of that contract。如果 docstring 不更新, 下游调用者 (如 phase-c-integrator skill 脚本) 看到 docstring 后可能省略 try/except, 但运行时碰到 GHA stub 时进程崩溃而非结构化返回。T-docs 4.1-4.4 任务都是 SKILL.md 和 CLAUDE.md 层面的文档, 没有 task 覆盖 gate_check() 内联 docstring 更新。
- **recommended_action**: Task 2.5 (Refactor gate_check() body) 末尾添加一行: "同步更新 gate_check() docstring: 删除 'Exceptions are caught and translated' 声明, 替换为 'NotImplementedError from backend.query_*() propagates to caller (Hard Constraint #7); all other exceptions caught to verdict=fail'."

---

### F-08 (d85d1a9f)

- **severity**: minor
- **category**: testability
- **scope**: tasks.md Task 3.10-3.12
- **type**: underspecified
- **summary**: TestProbeCacheIsolation (Task 3.10) 需要 2 个 test cases 验证 probe cache 隔离, 但 probe() 是否有 lru_cache 的决策在 Task 3.11 被延后 (实施时选 Option A 或 B), 导致 Task 3.10 的 tearDown 设计依赖一个尚未确定的实现细节
- **rationale**: 如果选 Option A (保留 @lru_cache), 则 tearDown 中 `AetherBackend.probe.cache_clear()` 可工作, TestProbeCacheIsolation 验证 cache_clear 正确调用。如果选 Option B (module-level dict), 则 `probe.cache_clear()` 方法不存在, 需要调用 `reset_probe_cache()` helper。两种方案需要完全不同的 test fixture 设计。目前 Task 3.10 要求写测试但 Task 3.11 说 "选择策略", 实施顺序如果严格按编号走会在 3.10 时还没做 3.11 的决策。tasks.md 依赖顺序部分中也未标注此依赖关系。
- **recommended_action**: 在 Task ordering dependency notes 中补充: "3.11 (probe cache strategy choice) **must precede** 3.10 (TestProbeCacheIsolation fixture design)." 并在 Task 3.10 中注明两种方案的 fixture 差异: "Option A: `tearDown` calls `probe.cache_clear()`; Option B: `tearDown` calls `reset_probe_cache()`" 让实施者根据 3.11 的选择配对使用。

---

## §Per-dimension verdict

### (a) AC 可测性

**verdict: PARTIAL PASS**

AC-1 (Aether backward) 可测, AC-1.1 计数 21 经代码验证正确。AC-2 (GHA stub safety) 清晰且可测。AC-3 (alias) 可测, warning 字面 string 在 AC-3.1/3.2 和 `_normalize_config()` pseudocode 之间一致。AC-4 (registry precedence) 可测, AC-4.4 的 grep 命令可直接运行。AC-5 minor 计数问题 (F-05 minor), 不影响可测性。AC-6 (doc consistency) 可测, AC-6.4 的 git diff 命令可直接运行。AC-7 有 gap: 需要 ci_backends/ 专用测试文件 (F-02 major)。AC-8 (SOT ship) 可测, 6 SOT 文件 grep 验证清晰。

### (b) 测试覆盖充分性

**verdict: PARTIAL PASS**

Hard Constraint #1 (Aether zero behavior change): T-tests 3.1-3.4 PASS, 但 _compute_verdict 未定义 (F-04) 使 primitive_used 断言有实施风险。Hard Constraint #7 (NIE abort): AC-2.3+2.4 设计完整, `test_gha_probe_true_query_nie_aborts_not_skips` 覆盖。Hard Constraint #8 (no decorator): AC-4.4 grep 命令验证, 有效。Hard Constraint #9 (new key wins): AC-3.5 + TestBothKeysPresentNewWins 覆盖。但 ci_backends/ 包独立测试缺失 (F-02 major): probe() subprocess mock、NIE message 内容精确验证等无对应 task。

### (c) 风险识别

**verdict: PASS**

lru_cache 隔离风险已识别 (Task 3.11-3.12)。CHANGELOG 顺序风险已识别 (Risk table)。Sister CLAUDE.md race 已识别。新风险已识别: (1) priority ClassVar dead field (F-06) — 实施者误信 priority 机制添加新 backend 会破坏顺序假设; (2) gate_check() docstring contract 错误 (F-07) — 下游调用者 try/except 决策会出错; (3) Phase C.2 pre-merge gate "dogfood the refactored gate via OLD gate" 路径: Task 8.2 使用 `aria-plugin master 无 in-flight` 验证的是 v1.30.0 已 cached 的 pre_merge_gate, 不是 v1.31.0 新代码 — 这不是 bug (正确行为), 但 Spec 中的注释 `# This Spec touches the very file Rule #8 enforces — verify dogfood` 可能给实施者制造 "新代码 dogfood 自身" 的误解, 值得澄清。

### (d) 估算准确性

**verdict: PASS_WITH_CONCERNS**

T-tests 3-3.5h: 21 existing rewrite (mock target collapse, 3 stacked → 2 methods) 基于 7 GateCheckTests + 2 FallbackTests 实际有 mock 的 test, 工作量与 Sprint 1 单文件改动类似。但 F-02 gap 要求新增 `test_ci_backends.py` (≥20 new cases) 未计入 T-tests 估算, 实际 T-tests 应为 3.5-4h (含新文件)。T-rule6 1.5-2h: Sprint 1 forgejo-hosts README 包含 dogfood evidence, 本 Spec README 格式类似, 估算合理。但 F-03 dogfood 命令修正后, dogfood smoke 执行实际运行时间取决于 Aria self repo CI 状态, 可能需要额外 15-30min 等待/验证。

### (e) Spec 可发现性

**verdict: PARTIAL PASS**

proposal.md §"当前 pre_merge_gate.py state" 表格 (L49-59) 提供了良好的当前状态快照, 3 个月后 reviewer 不需要 DEC 就能理解重构起点。Hard Constraints 9 条清晰枚举了关键设计决策。但 3 个月后 reviewer 看到 AC-7.2 "≥27 new unit tests" 不会知道这些测试应该在哪些文件中, 因为 tasks.md 没有对应的文件级 task (F-02)。同样, `_compute_verdict` 只出现在 B.4 pseudocode 中, 3 个月后不清楚这是新函数还是对现有 `compute_verdict` 的改名 (F-04)。

### (f) Phase D handoff trigger 充分性

**verdict: PASS**

Task 11.1-11.5 结构完整, Rule #9 trigger 明确 (session >4h = clear trigger), 9-section template 引用正确, latest.md pointer 更新在 11.3 中。memory candidates (Task 11.4) 指向 DEC §Memory candidates 中的 2 个候选项, 下游 session 可直接引用。

---

## §Final vote

**REVISE** — 4 major findings, 4 minor findings.

主要理由:

**F-02 (major)**: AC-7.2 要求 ≥27 new unit tests 的分布图包含 ci_backends/ 包级别的独立测试 (base.py 5+, aether.py 8+, github_actions.py 3+), 但 tasks.md T-tests 3.1-3.12 只改写 test_pre_merge_gate.py, 无任何 task 负责创建 ci_backends/ 的测试文件。Rule #6 substitute 的核心证据之一是 "27+ unit tests" 覆盖新包的 structural correctness。这个 gap 会导致实施者完成所有 tasks 后仍无法通过 AC-7.2 验收。

**F-03 (major)**: Task 5.5 的 dogfood 命令有两处错误 (--pr vs --pr-branch, -m 调用无效), 照搬执行会失败。dogfood smoke 是 Rule #6 substitute 的关键证据。

**F-01 + F-04 (major)**: tasks.md 类名/计数错误会误导实施者的工作量规划; `_compute_verdict` 未定义给实施者留下 AC-1.1 回归测试的实施风险。

这 4 个 major finding 都有清晰的、非 paper-fix 的 recommended action (文字修正 + task 补充), 修改量适中 (无需重新 brainstorm, 无需架构调整), 建议在 post_spec audit 轮次中修复后继续。4 个 minor finding 可合并到同一 revision pass 中一并处理, 不需要额外轮次。

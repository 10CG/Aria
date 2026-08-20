---
seat: A1-backend-architect
round: R1
checkpoint: post_spec
spec: subprocess-decode-hardening
verdict: REVISE
critical_count: 0
major_count: 2
minor_count: 3
timestamp: 2026-08-20T11:44:07Z
---

# Findings

## [A1-M1] B′「全局约定」docstring 升级会与 pre_merge_gate.py 自身已有的 surrogateescape 范例产生代码-文档矛盾 (Major)

**锚点**: `aria/skills/phase-c-integrator/scripts/pre_merge_gate.py:292-349` (`_sanitize_for_json` + `_verify_main_branch_exists`), spec §What Changes 条目 2 (B′ 精化) + 条目 5(b)。

`_verify_main_branch_exists` (pre_merge_gate.py:302) 是 #137 留下的既有实现, **没有** `text=True` (它本来就是手写 `capture_output=True` + `proc.stdout.decode("utf-8", errors="surrogateescape")` @ :339/:344), 所以不在本 spec AST 普查的「16 处生产调用点」范围内, 不会被 1.2/1.3 迁移触碰。它出口处调用 `_sanitize_for_json()` (:292, `text.encode("utf-8","replace").decode("utf-8")`) 做净化 —— 这正是 owner 原裁定「surrogateescape + 出口净化」的**已实装范例**, 也正是 spec §Why 与 traps.md #4/#5 引用的原始出处 (:310 docstring "轴复用⛔不再造第三份")。

spec 条目 5(b) 计划把这个函数紧邻的 docstring (:315-317, 现文案「我们自己用 surrogateescape 解码, 该异常结构上不可能发生」) 从「该函数局部纪律」升级为「指向本 spec 的全局约定」。但本 spec 的全局约定 (B′) 是 **backslashreplace 单步、不做出口净化**, 与 `_verify_main_branch_exists` 实际代码 (surrogateescape + `_sanitize_for_json`) **不是同一套**。条目 5(b) 落地后, 读者会看到「指向全局约定」的 docstring 挂在一段并不遵循该约定的代码上方 —— 这恰是 spec §Why 诊断的「先例文档与代码不同步, 误导下一个复制者」同款问题, 由本 spec 自己的勘正任务重新制造出来。

**建议修法**: 二选一, 写进 spec/tasks 明示裁决, 不留给 A.2/1.7 执笔人临场判断:
- (a) 把 `_verify_main_branch_exists` + `_sanitize_for_json` 一并纳入迁移范围 (16→17 处), 退役 `_sanitize_for_json`, 使全仓真正只有一套解码范式; 或
- (b) 明确保留此函数为「历史范例, 语义等价但形态不同, 不纳入本 spec 统一」, 并把 :315-317 docstring 的措辞改为「本函数早于本 spec, 手动实现语义等价的净化路径, 不适用新 helper 形态」而非「指向全局约定」—— 避免文案与代码矛盾。

## [A1-M2] 结构检查的扫描范围谓词是允许清单 (allowlist), 不是全分割, 未来新增路径可静默逃逸 (Major)

**锚点**: spec §What Changes 条目 4 ("生产路径定义 `skills/*/scripts/**`, `skills/*/lib/**`, `hooks/**`, 排除 `tests/`")。

审计问题 3 要求验证该谓词是否互斥+全覆盖。实测 (`find aria/skills -maxdepth 2 -type d` + 逐目录核对) 显示: 全部 25 个 AST 命中文件当前确实都落在 `scripts/**` / `lib/**` / `hooks/tests/**` 三类之一, 当前语料**没有**灰色地带逃逸 (`internal/` `validators/` `examples/` `config-loader/` `testing/` 等非常规目录下均无 `subprocess` 出现)。

但谓词本身是**允许清单** (只认三个目录名), 不是「skills/*/ 下除 tests/ 外全部」这种默认拒绝式全覆盖。这意味着: 未来任何新 Skill 若把脚本放进非常规目录 (例如 `skills/foo/bin/run.py`、`skills/foo/handlers/x.py`), 即使该文件写了 `text=True`, SC-2/SC-3 的扫描也**不会命中它** —— 既不算「生产路径」被拦, 也不算「tests/」被豁免, 是第三种「谓词覆盖不到」的静默逃逸。这直接削弱条目 4 自称的「机械防再长, 修类不修实例」的核心承诺: 结构消除只对「遵守当前目录命名约定」的新代码成立, 对约定漂移不成立 —— 而 §Why 本身论证的正是「靠纪律 (先例引用) 防不住」, 允许清单式谓词本质上仍是一种「靠命名纪律防」。

**建议修法**: 把谓词从「允许清单」倒转为「默认拒绝清单」——`skills/*/**/*.py` (含 `hooks/**`) 减去 `**/tests/**`、`**/references/**`、`**/templates/**`、`**/examples/**` 等已知非生产目录, 而非只认 `scripts/`/`lib/`。至少应在 SC-3 里加一条「谓词自身的全覆盖性」断言 (例如: 对仓内枚举出的全部 `.py` 文件做一次「必属于 生产扫描∪已知排除」的二分类检查, 断言无第三类), 使谓词的完备性本身可被结构化测试锁定, 而不只是当前语料恰好没撞见反例。

## [A1-m1] census「12 处接不住 / 4 处接得住」的子分类方法论有一处误判: `coordination_ref.py:255` 已经结构性不可抛, 应归入第三类 (Minor)

**锚点**: `aria/skills/state-scanner/lib/coordination_ref.py:255-268`, 对照 `.aria/notes/2026-08-20-census-147.md` "prod uncovered" 列表第 6 行。

census 把 `coordination_ref.py:255` 列入「12 处接不住」, 判据是 `except=['subprocess.TimeoutExpired', 'FileNotFoundError', 'OSError']` 不含 ValueError 族。但实读代码 :260-261 显示该调用**同时**传了 `encoding="utf-8", errors="replace"` (注释原文: "#61: never raise UnicodeDecodeError to the caller") —— 与 `_common.py:406` (census 正确归类为「4 处接得住」之一) 是**同一 #61 修复模式的姊妹实现**, 区别只是 `_common.py:406` 额外加了一层多余的 `except UnicodeDecodeError` 防御性兜底, 而 `coordination_ref.py:255` 没加这层多余兜底 —— 但两者的**解码本身都已经因为 `errors="replace"` 而结构性不可能抛异常**, 除不除 except 都无所谓。

census 的 AST 方法论 ("找 `text=True` 实参 + 逐层枚举 enclosing except") 只检查了 except 元组是否覆盖, 没有检查是否存在 `errors=` 覆盖参数会让解码本身永不抛 —— 这是方法论盲点, 导致 `coordination_ref.py:255` 被误归为「有裂缝」。已核对其余 11 处「接不住」站点均无 `errors=` 覆盖 (custom_checks.py:342 / spec_complete.py:863,874 / phase1_gate.py:240 / worktree_manager.py:117 / issue-triage/_common.py:39 / verify_post_push.py:65,89), 误判是孤立的 1 处, 不是系统性问题。

**影响面**: 不影响 SC-2/SC-3 的机械判据本身 (两者只断言「迁移后文本命中 text=True = 0」, 与「原来是否真会崩」无关, 该站点仍在 16 处内被正确迁移)。只影响 §Why/census 用来定性「12 处生产缺口」的事实陈述准确性, 建议行文改为「11 处真接不住 + 1 处 (`coordination_ref.py:255`) 已用 `errors="replace"` 结构性避险, 但形态与本 spec canonical helper 不同, 一并纳入统一迁移」, 使 census 数字与代码事实一致。

## [A1-m2] 「每脚本内联复制」的粒度 (按文件 vs 按调用点) 未定义, 对同文件多调用点场景 (aether.py :150/:173) 有歧义空间 (Minor)

**锚点**: spec §What Changes 条目 3, 对照 `aria/skills/phase-c-integrator/scripts/ci_backends/aether.py:150` 与 `:173` (同一文件两个独立 `subprocess.run` 调用点)。

条目 3 原文「canonical helper 每脚本内联复制」——「脚本」按字面可读作「每个 `.py` 文件一份」, 也可读作「每个调用点一份」。`aether.py` 一个文件里有两处独立 `subprocess.run` (`_verify_in_flight_flag` :150 与 `_run_with_retry` :173), `state-scanner/scripts/collectors/_common.py` 则是「多个调用方共享同一个模块级 `_run()` 助手」的既有形态 (25+ 处调用方经由 `_run()` 间接受益, 已核实)。若 1.2/1.3 执行时对 `aether.py` 逐调用点各贴 6 行解码代码, 会产生**同文件两份几乎相同的 helper 文本**, 与 `_common.py` 的「一个文件一个共享 `_run()`」形态不一致, 日后维护时容易只改一处漏改另一处 (回到条目 3 想避免的「跨文件漂移」问题的文件内版本)。

**建议修法**: 明确「脚本内联」的最小单位是「文件」——同文件多调用点应先内聚成一个模块级 private helper (如 `_decode(bytes) -> str`), 各调用点复用它, 而不是逐调用点物理复制 6 行文本; detailed-tasks.yaml 对 `aether.py` 这类多调用点文件应显式列出该子步骤。

## [A1-m3] SC-8 把「无 try 点」的处置全权下放 A.2, 缺一个 spec 层默认方向, 与「修类不修实例」的自我定位有轻微张力 (Minor)

**锚点**: spec §Success Criteria SC-8, 对照 `aria/skills/state-scanner/scripts/validate_schema_doc.py:130-141` (`_run_scan`, 已核实确无 enclosing `try`)。

SC-8 已经明确「不得静默留空」, 这是好的底线; 但「补最小 try 还是维持裸抛 + 注释」两个选项之间没有 spec 层倾向性意见, 完全交给 A.2 执行者临场判断。spec §Why 的核心论点恰恰是「不同实现者各自照先例选择, 结果不一致」——SC-8 在这一个具体站点上重新引入了同类型的自由裁量点 (虽然范围窄, 只影响 spawn 类异常轴的取舍, 不影响解码安全性)。

**建议修法**: 至少给一个默认倾向, 例如「优先复用 `pre_merge_gate.py:310` 或 `_common.py` 已确立的 `(TimeoutExpired, FileNotFoundError, OSError)` 轴作为默认, 除非 A.2 发现该调用点有特殊语义需要裸抛」, 把「A.2 定」收窄为「A.2 在给定默认下确认或备注偏离理由」, 而不是完全开放式决策。

---

# 抽查核验表 (spec 事实断言 → 核验结果)

| # | 断言 (spec / census 出处) | 核验方法 | 结果 |
|---|---|---|---|
| 1 | 「含命中的文件 25 (issue 初筛 26/27 为 grep 文件级粗筛, 本表为 AST 精筛)」 | `grep -rl 'text=True\|universal_newlines=True' aria/` 实测得 27 文件; 核对 `path_coverage.py` / `pre_merge_gate.py` 两处 grep 命中均只是 docstring/注释里的字符串 (`text=True` 出现在中文警示文案里), 非真实调用点实参 — 与 AST 25 的差值 (27-25=2) 精确对应 | **属实**, 且证明 AST 方法论确实比 grep 更精确 |
| 2 | `validate_schema_doc.py:130` 「完全无 enclosing try」 | 实读 `validate_schema_doc.py:116-142` (`_run_scan` 函数体), 未见任何 `try:` 包裹该 `subprocess.run` | **属实** |
| 3 | `aether.py:150` / `:173` 用 `text=True` 且 except 元组分别为 `(TimeoutExpired, FileNotFoundError, OSError)` / 仅 `TimeoutExpired` | 实读 `ci_backends/aether.py:139-187` | **属实**, 逐字匹配 |
| 4 | `verify_post_push.py:65` / `:89` 用 `text=True`, except 均为 `(TimeoutExpired, OSError)` | 实读 `verify_post_push.py:62-110` | **属实** |
| 5 | 「12 处接不住的生产点」(含 `coordination_ref.py:255`) | 逐处实读 12 处代码 | **6 处逐字核验属实** (custom_checks.py:342 / spec_complete.py:863,874 / phase1_gate.py:240 / worktree_manager.py:117 / issue-triage/_common.py:39); **1 处 (`coordination_ref.py:255`) 判定有误** — 该处已带 `errors="replace"`, 解码结构性不可抛, 不应与真正「裸 `text=True`」站点同列「接不住」(详见 [A1-m1]) |
| 6 | 「16 处消费者均为展示/解析文本」+ SC-4 两类 sink (`dumps(ensure_ascii=False)`后 encode / 文件写入) 各有真实链路 | 实读并追溯: `pre_merge_gate.py:568` `sys.stdout.write(json.dumps(output, ensure_ascii=False)+"\n")` (隐式 encode sink); `scan.py:482-485` `rendered = json.dumps(..., ensure_ascii=False, ...)` 经 `args.output.write_text(rendered, encoding="utf-8")` (显式文件写 sink, `errors` 缺省 strict) | **属实**, 两类 sink 均在真实代码路径中定位到, 且推演确认: backslashreplace 产生的字面 `\xNN` 若落在 JSON 字符串体内, `\x` 不是合法 JSON 转义, `json.loads` 必抛 `JSONDecodeError` — SC-4「mangled 后走既有 JSONDecodeError 路径」的技术论证成立 |
| 7 | 「`_common.py:406` 是 4 处接得住之一, except 含 `UnicodeDecodeError`」 | 实读 `_common.py:348-437` (`_run` 函数) | **属实**, 但补充: 该函数实际靠 `encoding="utf-8", errors="replace"` (#61 修复) 结构性避险, `except UnicodeDecodeError` (:436) 是文档自称的「防御性冗余, 理论上不会触发」— 与 [A1-m1] 揭示的 `coordination_ref.py:255` 是同款模式但少了这层冗余 except, census 对两者的分类标准不一致 |

**总体判断**: spec 的 B/B′ 技术论证 (backslashreplace 单步替代 surrogateescape+净化) 经独立推演可以成立, SC-4 的 sink 覆盖论证在真实代码路径中得到印证。REVISE 判据命中于两处 Major: (1) 本 spec 自身的文档勘正任务会在 `pre_merge_gate.py` 制造新的「docstring 指向约定, 代码不遵循该约定」矛盾; (2) 结构检查的扫描范围谓词是允许清单而非可证的全分割, 与条目 4「机械防再长」的自我定位有落差。两者均有具体、可执行的修法, 不影响 B′ 精化本身的可行性。

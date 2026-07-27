---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: false
oscillation: false
overridden_by_user: true
degraded: false
verdict: FAIL
timestamp: 2026-07-26T00:30:00.000Z
context: phase-c-integrator-ci-path-coverage
agents: [backend-architect, code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R4 (aggregated) — phase-c-integrator-ci-path-coverage

Anchor 同 R1 (不可变, `source_sha: 194a73b`)。**团队 3→2** (按 #113 先例 R5 由上一轮投反对票的一席独立复核; 取 R3 唯一 FAIL 方 backend-architect + 做实跑的 code-reviewer)。**`max_rounds=4` 本轮耗尽。**

## 各 agent verdict

| Agent | Verdict | Critical | Major | Minor |
|-------|---------|----------|-------|-------|
| backend-architect (R3 FAIL 方) | FAIL | 1 | 1 | 2 |
| code-reviewer (实跑) | PASS_WITH_WARNINGS | 0 | 3 | 3 |

**聚合 verdict: FAIL** (≥1 critical)。2/2 完成, 2/2 SCOPE_OK, 无 drift。

## R3 簇闭合

**R3 的 1 critical (Finding A, 空 unit 集) — 提出方 backend-architect 自己裁定 CLOSED**, 并确认「闭合手法对它字面覆盖的情形没有遗留漏洞」。code-reviewer 实跑复核: tripwire fixture 两种实现者读法**收敛为同一结论**, `any([])`/`all([])` 不再参与判定。

**R3 的 5 major (code-reviewer 提出方裁定)**: 4 CLOSED + 1 PARTIAL

| # | R3 major | 裁定 | 依据 |
|---|----------|------|------|
| 1 | token 扫描作用域 | CLOSED | 4 处误命中经实跑全部移出区间 |
| 2 | 空 unit 集 | CLOSED | 守卫先于 `any()/all()`; 两读法收敛 |
| 3 | 部分读失败 | **PARTIAL** | 步骤 1 文本本身正确, 但 R3-A 守卫伪码的 `units` 形式定义与之冲突 → R4-A |
| 4 | 模板选择器全函数 | CLOSED | **78 组可达组合, 0 条 UNDEFINED** (行命中分布 1:16/2:16/3:16/4:8/5:22) |
| 5 | §5 backend cwd | CLOSED | 6 处代码面引用逐个实核全对, 无 mis-citation |

## R4 新 finding

| 簇 | severity | 命中 | 内容 |
|----|----------|------|------|
| **R4-A** `units` 定义把整 workflow 级 fail-CLOSED 判定结构性排除 | **critical (ba) / major (cr)** | **2/2** | `units = [(workflow, event) \| …]` 是 **pair** 定义; `workflow_unreadable`/`flow_mapping_on_block`/`no_events_parsed`/`unrecognized_yaml_construct`/`unrecognized_indent_structure` 五类**没有 event** ⇒ 贡献零元素。ba 构造 2-workflow 反例逐字遵照规格产出 `covered=False, confident=True` ⇒ green; cr 实跑 4/4 场景两读法结论相异, 2 场景 WAIT↔GREEN 翻转 |
| **R4-B** token「命中」未作操作性定义 | major | 1/2 (实跑) | 收窄作用域后**区间内恰好是 `paths:` 通配模式所在处**。朴素子串读法 (`'*' in line`) 在 4 份真实语料**命中 3 份** (`- 'skills/issue-triage/**'` 等) ⇒ 每份带 `paths:` 的 workflow 都 fail-CLOSE ⇒ **恒 wait 复发** |
| **R4-C** `---` 规则误判 YAML 文档起始标记 | major | 1/2 (实跑) | 「列 0 且在 `on:` 块之前」—— 文档起始标记**永远**满足这两条。首行 `---` 的仓任何变更恒 wait, 且 **AC-7b 明确不钉 covered 真值 ⇒ 零 AC 会红** = 静默失效。`yamllint` 的 `document-start` 默认要求首行 `---` |
| **R4-D** `_match_coverage` 纯函数无 `changed_files` 内部防线 | major | 1/2 | 空集守卫只在 `coverage()` 层; 纯函数被设计为可独立单测且 AC-7/8c 已直接调用 ⇒ 任何第二个直接调用点会**原样复现 R1 最初的 bug** |
| **R4-E** 聚合 reason 在「多 `confident=False` 且 `covered_by=None`」时未定义 | minor | 2/2 | 模板 3 的 `<reason>` 因实现而异 |
| **R4-F** AC-12 mock 按字面 KeyError | minor | 1/2 | mock #1 落模板 3, 模板 3 插值 `<reason>`, 而 AC 只列 4 个键 |
| **R4-G** AC-14 的 `==` 恒不等 | minor | 1/2 | `cwd="."` vs `repo_root_resolved` 绝对路径 |
| **R4-H** token 匹配粒度 (`*wordchar` glob 误判 alias) | minor | 1/2 | 与 R4-B 同根, 已并入 |

### severity 分歧的裁定 (memory `feedback_cross_agent_verdict_independent_verify`: 1/N 反对方须独立 verify)

R4-A 两席同题不同判。owner 侧独立核对结论: **两边在各自框架内都成立** —— 缺陷的**后果**是假绿 (ba 的 critical 判读), 但它被 **AC-5a / 5b / 5j / 5k / 11(a) 至少 4 条既有 AC 机械兜住**, 结构上**无法静默 ship** (cr 的 major 判读, 附实跑佐证: 错误读法下这些 AC 会同时变红)。两席**修法完全一致**且只有一句定义。故 severity 之争在修法应用后自动消解, 不需要第三方裁决。

## R4-fix 处置 (全量吸收)

1. **`units` 定义扩宽** (R4-A): `units = pair_units + workflow_level_units`; 后者为 `(workflow, None)` 型伪单元, 同时参与 `covered` 的 OR 与 `confident` 的 AND, 天然不满足白名单条件 2 故不改变安全性论证。**AC-5a 参数化**: X 遍历全部 5 个 reason code。
2. **token 命中判据改位置式** (R4-B): 预处理后**值或键的首字符**为 `&`/`*`/`!`, 或键位以 `<<` 开头; 串中间的 `*` 不算。AC-5b 加第三条负控 `paths: ['a/**']` 不触发。
3. **`---` 改正确 YAML 语义** (R4-C): 首个非空非注释内容行**之后**才是多文档分隔; 之前是文档起始标记 ⇒ 忽略。新增 **AC-5b2** 双向断言。
4. **`_match_coverage` 自带防御性早退** (R4-D)。
5. **聚合 reason 四条确定性规则** (R4-E), 含排序键。
6. **AC-12 补 7 键完整 schema** (R4-F); **AC-14 改 `os.path.realpath` 比较** (R4-G)。

## 四轮收敛趋势

| 轮次 | 团队 | verdict | critical | 性质 |
|------|------|---------|----------|------|
| R1 | 5 | 4×FAIL+1×PWW | 5 | 设计骨架级, 整段重写 |
| R2 | 5 | 4×FAIL+1×PWW | 4 | 设计级 (极性 / 单出口) |
| R3 | 3 | 1×FAIL+2×PWW | 1 | 局部收口 |
| R4 | 2 | 1×FAIL+1×PWW | **1 (争议; 另一席判 major)** | **一句定义 + 一条 AC** |

**病灶谱系 (「空集/退化集真值真空」四次形变)**: R1 空 `changed_files` → R2 零 event → R3 空 unit 集 → R4 **unit 定义域结构性偏窄**。前三次是「集合恰好为空, 语言默认值代为决策」; 第四次是「集合的构造公式对一整类合法贡献者不可达」—— **前置守卫检查不到它** (`units` 在反例里非空)。

**这是 `feedback_fix_recurs_in_its_own_fallback_path` 在 spec 层的四连实证**, 且 R4 的形态最值得记忆: 「新写的文本只解决了自己举的那一个例子, 没有意识到自己举的例子是一整类的代表」(AC-5a 只测 `workflow_unreadable` 一个实例, 而它其实是 5 类的代表)。

## 收敛判定 + 降级

`conclusions_stable = (R4_keys == R3_keys)` → **False**。`unanimous_pass` → False。
**converged: false**, `oscillation: false` (R4 未推翻 R3 任何结论; R3 的 1 critical + 4/5 major 经提出方自己裁定闭合)。

**`max_rounds=4` 耗尽 ⇒ 触发降级策略。owner 2026-07-26 裁定: [1] 接受当前结论** ⇒ `converged: false, overridden_by_user: true` ⇒ 进 A.2。

裁定依据 (记录): R4 两席修法完全一致且已在 R4-fix 全量应用; code-reviewer 实跑结论「没有任何一条会让本 change 在本仓产出错误的 gate 结果」; critical 轨迹 5→4→1→1(争议); 剩余均为补测试/补定义类, 随 tasks.md 落。

两席的收敛建议 (记录备裁): code-reviewer —「本轮 0 critical…**没有任何一条会让本 change 在本仓产出错误的 gate 结果**…建议 finding 1/2/3 三句定义在进入 B.2 前直接补进 proposal (预计 <15 行、不动设计骨架、无需再开一轮 post_spec)」(**已在 R4-fix 中全部补入**); backend-architect 判 FAIL, 未给收敛建议。

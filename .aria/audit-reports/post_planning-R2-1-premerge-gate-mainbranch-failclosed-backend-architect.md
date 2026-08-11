---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-11T02:00:00.000Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R2 — backend-architect 独立审计

被审对象: R1-fix 后的 `proposal.md` + `tasks.md` + `detailed-tasks.yaml` (换人执笔轮, tech-lead 执笔, 主 loop 核验)。

## 投票

**VOTE: REVISE** — 发现 1 条 Critical + 2 条 Major, 均为**本轮 (R2) 独立发现**, 不与 R1 已列条目重复, 也不与 `verified-ground-truth.md` / `adjudication-draft.md` 已记录条目重复 (已逐条 grep 核对未重复)。

## 审视范围与方法

我的席位角度 = **实现可行性**: spike 的输入是否够定稿、复用先例是否真能复用、异常/重试/解码三轴是否闭合、插入点是否正确。已采信 `verified-ground-truth.md` 与 `adjudication-draft.md` 的既有结论 (未发现其错误), 在此基础上对**换人执笔轮新写/新扩的内容**做独立实读+实跑, 聚焦三处此前审计未覆盖的角落: TASK-020 (本轮从 M/4h 扩到 L/6h, 内容几乎全新)、SC-M12 的任务归属、TASK-002 spike 输入的完整性。

---

## Finding 1 (Critical) — TASK-020 的 fail-closed 机制无插入点/信号传播设计, 最自然实现会使 CLI 崩溃而非产出 `verdict=fail`

**定位**: `openspec/changes/premerge-gate-mainbranch-failclosed/tasks.md:83-91` (TASK-020) + `detailed-tasks.yaml:493-543` (TASK-020) + `aria/skills/phase-c-integrator/scripts/pre_merge_gate.py:94-119`(`_normalize_config`)、`:325`(调用点)、`:424-441`(`main()`)。

**实读证据**:

```
$ sed -n '94,95p' pre_merge_gate.py
def _normalize_config(config: dict[str, Any]) -> dict[str, Any]:
    """Translate legacy config keys to v1.31.0 schema with deprecation warnings.
```
—— 纯 `dict -> dict` 函数, 无任何抛出错误/返回错误结构的通道。

```
$ grep -n "_normalize_config" aria/skills/phase-c-integrator/scripts/pre_merge_gate.py \
        aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py
tests/test_pre_merge_gate.py:410,424,438,448,538   (5 处, 全是单测)
scripts/pre_merge_gate.py:94(def) :325(唯一生产调用点)
```
—— 全仓唯一生产调用点是 `gate_check():325`。

```
$ sed -n '320,327p' pre_merge_gate.py
    user_normalized = _normalize_config(config or {})
    cfg = {**DEFAULT_CONFIG, **user_normalized}

    if not cfg["enabled"]:
```
—— **调用处无 try/except**, `_normalize_config` 若抛异常会直接冲出 `gate_check()`。

```
$ sed -n '424,441p' pre_merge_gate.py
def main(argv: list[str] | None = None) -> int:
    ...
    output = gate_check(
        pr_branch=args.pr_branch, main_branch=args.main_branch, config=config
    )
    sys.stdout.write(json.dumps(output, ensure_ascii=False) + "\n")
```
—— **`main()` 对 `gate_check()` 的调用同样无 try/except**。`if __name__ == "__main__": sys.exit(main())` 之外再无兜底。

**推导 (可证伪)**: TASK-020 要求「v2.0 后 legacy key 在场必须发红, 不得静默忽略」且「硬失败走 `verdict='fail'` + `raw_message`」(SKILL.md:255 逐字规定的 surface 通道)。但实现这条要求最自然的写法——在 `_normalize_config()` 检测到 legacy key 时 `raise` ——会导致:

1. 异常从 `:325` 裸传播出 `gate_check()`(无 try/except);
2. 异常从 `main()` 裸传播出去(无 try/except);
3. 进程以未捕获异常方式崩溃, stdout **无 JSON 输出**, 只有 traceback 落 stderr;
4. `verdict="fail"` + 含 (a)(b)(c) 三要素的 `raw_message` **从未被构造出来** —— TASK-020 自己的验收要求因此无法兑现;
5. AI 依 SKILL.md §C.2.4 步骤 6 解析这条 CLI 输出时, 拿到的是一段 traceback 而非可路由的 JSON, 与本 Spec 在 `gate_error`/workflow-runner 臂那一段**自己点名警告过**的同一种病 (memory `fix-recurs-in-fallback`: 「修复类 change 最易在自己新写的兜底路径里重犯要治的病」) 一模一样, 只是这次落在 TASK-020 自己身上而未被察觉。

**为什么会红而不会被 TASK-020 现有验收挡住**: TASK-020 给出的验收用例原文是「传入含任一 legacy key 的 config ⇒ 必须发红」——这条断言**只钉了"要发红"这个方向, 没钉"在哪一层发红、以什么形状发红"**。一个满足字面要求但仍然踩中上述崩溃路径的实现完全可能通过验收: 例如单测写成 `with self.assertRaises(SomeError): gate._normalize_config({"no_aether_fallback": "abort"})` —— 该测试断言的是 `_normalize_config` 单独调用时抛异常, 完全不经过 `main()`/CLI 这条真实生产路径, 于是 CLI 层的裸崩溃永远不会被这条验收捕获。这正是本 Spec 自己反复点名过的**维度不匹配**模式 (memory `invariant-dimension`, R1 的 PC1 就是同一模式的另一实例) —— 只是这次出现在 TASK-020 里, R1 与本会话此前的复核均未覆盖到 (grep 两份既有底稿 `_normalize_config` 均零命中)。

**为何是 R1-fix 新引入而非既有缺陷**: R1 阶段 TASK-020 完全不存在于任务图中 (R1 aggregate Major 原文: 「19 条任务无一承接」MAJOR 弃用到期承诺); TASK-020 是本轮 (2026-08-10 换人执笔) 全新新增的产物, 其内容(删除面枚举/fail-CLOSED 要求/raw_message 三要素)全部是本轮新写, 因此这个控制流缺口是**本轮引入的新缺陷**, 不是延续 R1 的旧账。

**建议**: TASK-020 需补一条明确设计: 要么 (a) 让 `_normalize_config` 改签名为返回 `(cfg, legacy_error | None)` 元组, 由 `gate_check()` 在早退链最前端显式检查并构造 `_build_output(verdict=FAIL, raw_message=...)`; 要么 (b) 在 `gate_check()` 内用 try/except 包裹 `_normalize_config()` 调用并转译为 `_build_output`。且验收用例必须**经由 `main()`/CLI 层**断言 stdout 是合法 JSON 且 `verdict=="fail"`, 不能只在 `_normalize_config` 单元层断言抛异常。同时需与 TASK-008 的早退顺序 (D9: 三早退之后、path coverage 之前) 显式排出这第 4/5 条早退分支的相对位置——目前 TASK-020 的 `dependencies` 只有 `[TASK-006]`, 与 TASK-008 无任何协调, 两条各自新增早退分支的任务在 DAG 上互不知情。

---

## Finding 2 (Major) — SC-M12 (五种 cwd 可达性) 全任务图中无任何 task 交付持久化测试, 只挂在一个纯 prose 产出的 spike 上

**定位**: `tasks.md:23`、`detailed-tasks.yaml:78-109`(TASK-002)。

**实读证据**:

```
$ grep -n "SC-M12" tasks.md detailed-tasks.yaml
tasks.md:23:      **验收 = SC-M12**: ...
detailed-tasks.yaml:91-92:  - 'SC-M12: 五种 cwd 全部可达 ...'
detailed-tasks.yaml:412:    (...D1 的行为证据主要由 SC-M1/SC-M3a-c/SC-M12 承担...)
```
—— SC-M12 在全部 20 个任务中**只出现在 TASK-002 一处的 verification 字段**, 无第二个 owning task。

```
$ grep -n "deliverables:" -A2 detailed-tasks.yaml | sed -n '1,6p'
88:  deliverables:
89:  - spike 结论回写 openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md §1
```
—— TASK-002 的**唯一 deliverable 是写回 proposal.md 的一段 prose**, 不含任何测试文件/脚本。

**对照仓内既有先例** (证明"这类东西该有测试"在本 skill 是有成文惯例的, 不是我的主观标准):

```
$ ls aria/skills/phase-c-integrator/tests/
test_ci_backends.py  test_path_coverage.py  test_pre_merge_gate.py
test_submodule_gate.sh  test_submodule_tripwire_audit.sh
```
—— 本 skill 已有对**同类**"路径解析 + shell 探测"逻辑 (`submodule_gate.sh`) 建立专门 shell 测试的先例 (`test_submodule_gate.sh`)。SC-M12 所测的正是同一类东西 (helper 路径解析在不同 cwd 下的可达性), 却没有沿用这个先例建对应测试。

**推导 (可证伪)**: 若 Phase B 执笔人严格按 TASK-002 的 deliverables 执行 (只做一次性人工/临时验证, 把结论写成 proposal.md 里的一段文字, 不留下可重跑脚本), 则 SC-M12 校验的性质——**本 Spec 自称的"两个已被否决形态的判别器"**——只在 spike 当次被验证过一次, 此后任何一次对 SKILL.md 路径解析段落的修改 (包括 TASK-014 本身、以及未来任何编辑) 都不会被任何自动化机制复检是否又退回到已被证伪的两种形态之一。这正是本项目反复吃过的"机械断言无 owning 执行通道 = 静默失效"的形状 (R1 的 PC3 原话: 「组0『先看到红』只覆盖 4/13 条 SC……无 owning task、无 deliverable、无红窗」)。

**与 R1 PC3 的关系**: R1 PC3 点名 SC-6~SC-13 (旧编号) 整体缺 owning task。本轮 R1-fix 已经把其中大多数 (SC-M6/M7/M8/M9/M10/M11/M13) 通过 TASK-003/004/005/008/010 配上了带 test 文件 deliverable 的 owning task (已核实, 见下方"R1 闭合情况"), **唯独 SC-M12 仍停留在只有 prose 产出的 spike 上**。故 PC3 是**部分闭合**而非全部闭合——这是本次审计新发现的、R1-fix 遗留的缺口, 不是我重复举报 R1 已举报过的同一件事(R1 举报的是"8 条全部无 owning task", 现状是"7 条已配, 1 条仍未配")。

---

## Finding 3 (Major) — TASK-002 的 spike 输入丢失了本轮 adjudication 已决定要补入的复用先例引用

**定位**: `tasks.md:21-25`、`detailed-tasks.yaml:78-109`(TASK-002 全文) 对照 `adjudication-draft.md` D-2 落地动作 2。

**实读证据**:

```
$ grep -n "submodule-gate-telemetry" openspec/changes/premerge-gate-mainbranch-failclosed/*.md \
        openspec/changes/premerge-gate-mainbranch-failclosed/*.yaml
tasks.md:66:      ...submodule_gate.sh 的真实调用者是 aria/hooks/submodule-gate-telemetry.sh:60-62...
detailed-tasks.yaml:387:    ...submodule_gate.sh 的真实调用者是 aria/hooks/submodule-gate-telemetry.sh:60-62...
```
—— 这个文件路径**只出现在 TASK-014 的段落里**(论证 `:262`/`:559` 为何"无消费者、零行为风险"), 而 TASK-002 (真正要用这个先例的 spike) 全文对它**零引用**。

对照 `adjudication-draft.md` (本轮 session 内部产物) 第 59-65 行, D-2 的落地动作原文:

> 「2. TASK-002 的 spike 输入补上『先例 = submodule-gate-telemetry.sh:60-62』与『hook 上下文 ≠ Bash 工具上下文』这条区分 (否则会第三次测错总体)」

`hook 上下文 ≠ Bash 工具上下文` 这半确实写进了 `proposal.md:67` (核实通过), 但**"先例 = submodule-gate-telemetry.sh:60-62" 这半在提交文档里完全没有落地**——它作为一条决定被记在 adjudication 草稿里, 但从未写进 TASK-002 本身。

**推导 (可证伪)**: `submodule-gate-telemetry.sh:60-62` 是一个已实读确认、已 ship 到生产的可复用模式 (「环境变量优先 → 失败则自定位 → 仍不中则不执行」, 已独立核实见下方读取):

```
$ sed -n '60-62p' aria/hooks/submodule-gate-telemetry.sh
gate="${CLAUDE_PLUGIN_ROOT:-}/skills/phase-c-integrator/scripts/submodule_gate.sh"
if [[ ! -f "$gate" ]]; then
    gate="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." 2>/dev/null && pwd)/skills/phase-c-integrator/scripts/submodule_gate.sh"
fi
[[ -f "$gate" ]] || exit 0
```

若 Phase B 执笔人只读 TASK-002 自身的 notes/verification (adjudication 草稿是本会话临时工作文件, 不随 Spec 交付, 执笔人看不到), 他们得不到任何指向这个已验证可行模式的线索, 存在重新发明一套探测逻辑的风险——这与本 Spec 对 TASK-004 复用重试逻辑的严格程度 (「在一份治『同一算法两份实现』的 Spec 里再造第二份重试实现是自相矛盾, 本条的产出若是『新写一份』, 必须显式论证为何不能复用」) 不对称: 同一份 Spec 对"复用" 的要求在 TASK-004 是显性、强制、可核验的, 在 TASK-002 却完全缺席, 而 TASK-002 面对的恰恰是本 Spec 反复强调"必须先定锚点再谈机制"的最核心难题。

**严重度评级理由**: 定为 Major 而非 Critical——因为 TASK-002 本身仍然给出了正确的判定标准 (SC-M12 五种 cwd 全可达 + 两个已否决形态的负控), 缺失先例引用不会使一个认真做 spike 的实现者得出错误结论, 只是提高了"重新发明轮子/绕远路"的概率, 不构成结构性红/绿翻转。

---

## R1 闭合情况 (逐条回源, 不采信"已修"的声称)

| R1 编号 | 内容 | 本轮判定 | 证据 |
|---|---|---|---|
| **PC1** | TASK-011 验收对 `--main-branch` 完全失明 | ✅ **已闭合** | 独立实跑 SC-M3b 正则: 对 `--main-branch main`/`--main-branch master ` 命中 2, 对占位符 `--main-branch "<MAIN_BRANCH>"` 命中 0 —— 正则本身确实具备区分能力, 非自陈 |
| **PC2** | SC 编号与既有测试全面冲突 (SC-1..13 全撞) | ✅ **已闭合** | 独立实跑 `grep -oE 'def test_sc[0-9_]+' test_*.py`: 既有测试全部是裸 `test_sc9_`…`test_sc22_`(无 "M"), 新方案统一 `SC-M*` 前缀不与之冲突 |
| **PC3** | 组0「先看到红」只覆盖 4/13 条 SC, SC-6~13 无 owning task | ⚠️ **部分闭合** | SC-M6/7/8/9/10/11/13 均已配上带 test 文件 deliverable 的 owning task (TASK-003/004/005/008/010); **SC-M12 仍无 owning task 交付测试文件** (本报告 Finding 2), 是 R1-fix 遗留缺口而非新缺陷 |

其余 12 条 Major (`SKILL.md:262/:559/:610` 误引 / TASK-004 复用目标不可直接复用 / ship_target 多处未收敛 / DAG 缺依赖边 / TASK-005/008 接缝无人复检 / 多条恒绿断言等) 已由 `verified-ground-truth.md` 逐条回源确认闭合, 我独立核对其中与我席位相关的部分 (`:242`/`:610` 实读、`aether.py`/`path_coverage.py` 实读、DAG 依赖边实跑) 均属实, 未发现被推翻之处, 不再重复列出。

---

## R1-fix 是否引入新缺陷 (本轮核心判据)

**是, 引入了 3 条新问题** (1 Critical + 2 Major), 全部集中在**本轮新扩/新写的内容**——TASK-020 (从 M/4h 扩到 L/6h, 内容几乎全新) 与 TASK-002 spike 输入的最终定稿——而非旧任务的旧措辞。这与本 Spec 五轮 post_spec 审计的规律 (每轮 fix 引入 73-100% 新 Major) 部分相似 (fix 确实引入了新缺陷), 但**严重度显著更低**: 本轮的三条问题均属"设计细节遗漏"性质 (缺插入点规格 / 缺 owning task / 缺先例引用), 没有出现此前反复出现的"断言维度与病灶维度不匹配导致全套验收恒绿/恒红"这类结构性翻车 (唯一带一点这个形状的是 Finding 1 的"验收用例可能在错误的层级断言"这个子问题, 但 SC-M12/precedent 两条不属此类)。**换人执笔看起来确实部分打断了"每轮引入等量新缺陷"的规律**——数量从 R1 的 3C+12M 降到本轮我独立发现的 1C+2M, 且这 1C+2M 集中在两个此前审计从未深入检查过的角落 (TASK-020 的控制流、SC-M12 的任务归属), 而不是散布在已被反复审计过的核心机制 (D1/D6/D-4 三条承重腿本轮我逐条重读均成立, 未发现被推翻之处)。

## 阻塞项 (我认为的)

1. **TASK-020 需补充信号传播设计** (Finding 1) —— 建议在进入 TG-3 前解决, 不阻塞 TG-0 启动(TASK-001~005 均不依赖它)。
2. **SC-M12 需指定一个带测试文件 deliverable 的 owning task** (Finding 2) —— 可并入 TASK-002 本身(把"spike 结论"升级为附带一个可重跑的检查脚本)或另设一条 TG-1 任务, 建议在 TASK-002 关闭前解决。
3. **TASK-002 补回 submodule-gate-telemetry.sh 先例引用** (Finding 3) —— 低成本修复(一句话), 建议顺手做, 不构成硬阻塞。

无发现推翻本 Spec 的三条承重腿 (D1 两处散文收敛 / D6 精确比对 / D-4 aether.py 入 scope)。

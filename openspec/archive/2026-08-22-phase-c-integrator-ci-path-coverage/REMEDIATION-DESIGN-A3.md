# 修法设计存档 (原 A3 版 proposal 全文)

> **⛔ 这不是一份待实施的 Spec。** 它是 superseded 轨 (`phase-c-integrator-ci-path-coverage`) 在
> 2026-07-28~31 对**竞品 Spec** `phase-c-gate-path-coverage-not-applicable` 所做的 A1/A2/A3 三轮修订全文。
> 该竞品 Spec 已于 2026-07-31 独立 ship 为 aria-plugin **v1.65.0** 并归档
> (`openspec/archive/2026-07-31-phase-c-gate-path-coverage-not-applicable/`) —— 本文件的修订**从未进入**
> 那条实现路径, **也不得回写归档 Spec** (归档是「实际 ship 了什么」的历史记录)。
>
> **保留它的唯一理由**: A2/A3 里的判据设计对修复 ship 后暴露的三个缺陷有直接参考价值 ——
> - [aria-plugin #124](https://forgejo.10cg.pub/10CG/aria-plugin/issues/124) fail-OPEN → 见本文 §0 的 `-z` 三条义务 (D14) 与 SC-29
> - [#125](https://forgejo.10cg.pub/10CG/aria-plugin/issues/125) 同缩进块序列 → 见 D12 的 **(2a) 值域归属计算** 与 SC-30 负控 (x)(xi)(xv)
> - [#126](https://forgejo.10cg.pub/10CG/aria-plugin/issues/126) 内部异常误诊 → 见 **D15 的 `internal-error` 槽** 与 SC-34
>
> 另: A3 的 **(2b) 位置 ∧ 形态判据**是为解 C-2 (`paths: *alias` 被当 pattern) 设计的。
> **实跑证实 ship 的实现不存在 C-2** —— 它独立到达了等价的 `paths: <非列表标量> → uncertain` 兜底。
> 故 (2b) 属**未命中的防御**, 参考时请注意这一点 (它防的问题在 ship 版本里不存在)。
>
> 复现三缺陷: `python3 .aria/repro/repro-aria-plugin-124-125-126.py aria/skills/phase-c-integrator/scripts/path_coverage.py`
>
> 修订轨迹: A1 (并入竞品 4 条发现) → post_spec R5 定向轮 5 席 5/5 REVISE → A2 → R6 新鲜眼睛轮 REVISE → A3。
> 审计报告: `.aria/audit-reports/post_spec-R{5,6}-*-phase-c-gate-path-coverage-*.md`

---

# Proposal: phase-c-gate-path-coverage-not-applicable (aria-plugin #122)

> **Status**: 📝 **Draft (A3, post_spec R6-fix)** — **⛔ 不 ready for Phase B** (R6 新鲜眼睛轮 REVISE, 2 critical + 8 major + 7 minor 已在 A3 全量吸收, 待下一轮判定)。原状态: ✅ Approved (owner sign-off 2026-07-27, 签字面两项均批: 机制本体 + `path_coverage_enabled` 默认 true; post_spec R1→R4 CONVERGED)。**机制本体的 owner 签字未撤销**; A1/A2/A3 只动实现判据与验收面, 未动 §Why / §非目标 / 三态语义。**A3 的判据方向 (C-2 用「位置 ∧ 形态」) 经 owner 2026-07-30 明确裁定。**
> **⚠️ A1 修订 (2026-07-30, owner 裁定「以本 Spec 为准」后并入竞品发现)**: 本 Spec 与并发轨的 `phase-c-integrator-ci-path-coverage` (下称 **L**) 同治 #122, 各自跑满 4 轮 post_spec。owner 2026-07-30 裁定**以本 Spec 为基线**, 并入 L 的实跑发现。本轮并入 **3 条真缺口 + 1 条欠定钉死** (§修订记录 A1), 均带 L 侧实跑证据; L 的另 2 条 (`_match_coverage` 纯函数拆分 / `paths-ignore` 极性) 经逐条核实**本 Spec 已用别的方式解决**, 不并入。碰撞全量对比见 `openspec/changes/phase-c-integrator-ci-path-coverage/MERGE-ANALYSIS.md`。**本修订是实质 Spec 变更, post_spec 闸门处置见文末「闸门待裁」。**
> **Created**: 2026-07-27
> **Spec Level**: 2 (Minimal — 单域 [C.2.4 gate 增路径覆盖感知三态], 全部落点在 phase-c-integrator; blast radius 限 gate 输出 additive 扩展, covered 路径既有字段逐字段不变)
> **关联 Issue**: [10CG/aria-plugin #122](https://forgejo.10cg.pub/10CG/aria-plugin/issues/122) (open; triage verdict=`confirmed`/`major`/`next-cycle`, 3/3 复现, [issuecomment-16979](https://forgejo.10cg.pub/10CG/aria-plugin/issues/122#issuecomment-16979))
> **授权链 (Rule #10)**: 本 spec 修改 enabled gate (Rule #8 C.2.4) 的判定语义 — 授权 = owner 2026-07-25 复议定案「#122 (路径覆盖感知 not_applicable 态) 优先落地, 是唯一真机制」(`.aria/config.json` `phase_c_integrator._lane` 留痕; 该裁决全文将在 Phase D 改写 `_lane` **之前**抽取存独立 DEC, 见 §7) + 本 spec owner sign-off。**sign-off 面显式含两项**: (1) 机制本体; (2) `path_coverage_enabled` **默认 true** (TL-8 — 翻默认影响所有装机仓, 单独点名不随整体默认批准)。落地前, 过渡规则 (2) (verdict=wait 一律上报 owner) 继续有效。
> **复发序数口径 (KM-4)**: 「第 5 次」= 历史总复发人工裁决数 (v1.54.0 / v1.55.0 / v1.55.2 / v1.64.0 / v1.64.1); 「手工特批第 2 次」= 2026-07-25 owner 新规 (过渡规则 (2)) 确立**后**的上报-特批次数 (v1.64.0 一次性 ratify 为第 1 次, v1.64.1 为第 2 次)。两口径并存, 下文标注取前者。
> **ship target**: aria-plugin v1.65.0 (MINOR — 新模块 + SKILL.md §C.2.4 指令面扩展; 当前 SOT plugin.json = v1.64.1)
> **代码落点**: `aria/` 子模块 `skills/phase-c-integrator/`; Spec 落主仓 `openspec/changes/` (meta-repo 惯例, Rule #5)
> **审计轨迹 (post_spec, convergence)**: R1 5-agent [5/5 REVISE; SCOPE_OK ×5] → 4 Critical (TL-1 执行上下文 / BA-1 glob 未建模方向 / BA-2 仓边界 / QA-1 workflow 自身变更反向假绿) + 15 Major 簇 (三处 3-agent 交叉命中: build-aria-runner 语料错 [TL-3=BA-3=CR-1] / covered-unknown 谓词矛盾 [TL-2=BA-4=CR-2] / 文档同步面 [KM-1/2/3]) + 12 Minor → R1-fix 全量吸收 → **R2 5-agent [code-reviewer PASS / tech-lead PASS_WITH_WARNINGS / backend-architect + qa-engineer + knowledge-manager REVISE]**: R1 findings 24 条中 22 条 CLOSED + 2 PARTIAL (BA-2 残留负向 SC / KM-5 指针错字); 新 findings 全部「文字补完级」— 规则 7/8 空真重叠 **四方独立命中** (TL-Major-1 = BA-R2-M1 = QA-9 = CR-N-1) / R2-C1 `pull_request_target` 兜底方向 (BA, 唯一新 Critical) / SC-19 具体化 (QA-10 = CR-N-4 = TL-Minor-2) / KM-9 指针 / 各家 Minor → R2-fix 全量吸收 (判定规则重排为数据依赖序 + reason 封闭集 + D7 精确白名单 + SC-25~27 + KM-9/10) → **R3 2-agent 定向 [backend PASS_WITH_WARNINGS (三残留全 CLOSED + 全分割独立复验通过) / qa REVISE 窄口径 (SC 回填机械缺口)]** → R3-fix (SC-4/5/20/23 reason 回填 + SC-28 empty-diff) → **R4 1-agent 终轮 [qa PASS 0/0/0] → CONVERGED**。报告: `.aria/audit-reports/post_spec-R{1,2,3,4}-1785112156889-phase-c-gate-path-coverage-*.md`

---

## Why

Rule #8 C.2.4 pre-merge gate 对**路径过滤型 CI** 的仓库结构性恒 `wait`:

- `ci_backends/aether.py:223-224` `_normalize_pr_ci_status`: `if not runs: return "pending"` — 「CI 还没跑完」与「CI 永远不会为这些路径跑」折叠为同一值 (函数注释自述保守映射意图, 但未区分两种零 run 成因);
- `pre_merge_gate.py:187-188` `pending → VERDICT_WAIT` — 调用方 (workflow-runner `wait_recoverable`) 指数退避等满 `wait_timeout_seconds` (1800s) 也不会变。

**真实语料 (2026-07-27 probe; R1 三 agent 勘正 build-aria-runner 行)**:

| 仓库 | workflow | 自动触发 | paths 过滤 |
|------|----------|----------|-----------|
| aria (plugin) | `issue-triage-tests.yml` | push + pull_request | `skills/issue-triage/**` |
| Aria (主仓) | `issue-triage-tests.yml` | push (branches+paths) + pull_request (paths) | `aria/skills/issue-triage/**` |
| Aria (主仓) | `build-aria-runner.yaml` | **workflow_dispatch + push (branches: [feature/aria-2.0-m0-prerequisite], paths)** | `aria-orchestrator/docker/aria-runner/**` |
| Aria (主仓) | `submodule-gate-tripwire.yml` | ❌ 仅 workflow_dispatch (deprecated; schedule 被注释) | n/a |

⇒ 两仓中**绝大多数变更** (state-scanner / session-closer / tdd-enforcer / 文档 / 版本文件) 零 CI run, C.2.4 恒 `wait`。语料同时给出评估器必须正确处理的三种触发形态: 纯 paths 过滤 (aria 仓) / branches+paths 组合 (主仓 issue-triage, build-aria-runner) / 纯 dispatch (tripwire)。

**复发史 (历史口径共 5 次)**: v1.54.0 / v1.55.0 / v1.55.2 / v1.64.0(#113, owner 一次性 ratify) / v1.64.1 (2026-07-26, 新规后特批第 2 次) — 每次都消耗人工现场裁决。owner 2026-07-25 复议已认定: 把 verdict=wait 当 skip 是 Rule #10 反模式, 真解法只有把「无覆盖」从「pending」里分出来。

**为什么恒红是伤害**: 假绿的反面是恒红, 同样零信息量 — 永远返回 wait 的闸门会被学会忽略, 对真 pending / 真 failing 也失去拦截力。`ci_backends: []` 糊不过去 (对所有变更跳过闸门, 含真有覆盖的路径; `_not_ci_backends_empty` 已留痕)。

---

## What Changes

**核心原则 (D2, R1 按 CR-2/TL-2/BA-4 重写): fail-toward-covered 是「行为」承诺 — 任何不确定, gate 行为一律退回与现状逐字段一致 (正常查询→wait); `not_applicable` 只在高置信「零 workflow 会为本变更自动触发」时产生。`decision` 字面值按失败层级分两档 (见 §1 判定全分割), 两档 gate 行为均=现状。绝不把「解析不了」当「无覆盖」; 同时「评估失败」不得静默 (D9 可观测性义务)。**

### 0. 执行上下文契约 (R1 TL-1/BA-2 新增, Critical 修复)

- **仓根 = 评估进程 cwd 的 `git rev-parse --show-toplevel`**。调用方契约: **在执行 C.2 合并的目标仓根内调用** — 子模块本地合并 (约束 1 场景) 时 cwd = 子模块根 (dogfood 即 aria/), 主仓 PR 时 cwd = 主仓根。SKILL.md §C.2.4 执行流程写明此契约 (既有 `--config-file .aria/config.json` 相对路径已隐含同一契约, 本 spec 把它成文)。
- **`main_branch` 不依赖默认值**: 评估必须使用调用方显式传入的 `--main-branch` 真值 (本项目为 `master`; `pre_merge_gate.py` CLI default="main" 仅为向后兼容保留)。main ref 不存在 → `git diff` 失败 → `unknown`, reason=`git-diff-failed: <stderr 摘要>` — 与「diff 成功但空」(reason=`empty-diff`, 判 covered, 见 §1) 是**不同 reason, 可辨**。
- **gitlink-only diff 语义 (成文, 非巧合)**: 主仓评估时 submodule bump 在 `git diff --name-only -z` 输出为 gitlink 路径单 token (如 `aria`), 按普通路径参与 glob 匹配 — 与 forgejo/GHA 对 gitlink 变更的 paths 匹配行为一致 (gitlink 不展开为子路径)。SC-19 锁定。
- **rename 策略 (QA-6)**: `git diff` 调用显式加 `--no-renames` — rename 呈现为 delete(旧路径) + add(新路径) 两条, changed_files 同时含两侧, 「从覆盖路径重命名移出」保守地保持 covered。SC-18 锁定。
- **非浅克隆前提 (BA-9)**: 评估假定本地为完整 clone (gate 运行环境 = agent 本地开发仓, 非 CI runner); shallow 导致 merge-base 失败 → 落 `git-diff-failed` → unknown, 不误判。
- **⭐ NUL 分隔输出 (A1 并入 L-4; A2 补前提与解码契约)**: `git diff` 调用**必须**带 `-z`, 三条义务一体:
  1. **`-z` 本身**: 不带时 git 对含非 ASCII 或特殊字符的路径按 `core.quotePath` 做**八进制转义并加双引号** (如 `"skills/\346\265\213/x.py"`) — 该形态与 glob pattern **恒不匹配** ⇒ 这类文件的变更被静默判为「不命中任何 paths」⇒ 假 `not_applicable`。
     > **触发前提须钉死 (A2/M2)**: 该转义只在 `core.quotePath` **为 true 时**发生 —— 它是 git 的**默认值**, 但可被仓级/全局 config 关掉。⇒ 评估**不得**依赖 quotePath 的取值 (`-z` 对两种取值都正确); 而 **SC-29(a) 的红窗必须显式设 `core.quotePath=true`**, 否则「忘记 `-z`」的实现在 `quotePath=false` 下同样绿 (R5 code-reviewer 实测)。
  2. **尾随 NUL**: 非空 diff 的 `-z` 输出**含尾随 NUL** (L 侧 R2 实测) ⇒ 解析用 `stdout.rstrip("\0").split("\0")`。**空 diff 的输出是空串** (零字节), `rstrip` + `split` 后得 `[""]` ⇒ **必须滤空串**才落到既有规则 2 (`empty-diff`)。
     > **⚠️ A3/m-4 如实订正**: A2 此处写「两步不重复, **各治一病**」并据此设计 SC-29(b) 的红窗。**该说法不成立** —— 滤空串**完全覆盖** rstrip 的作用域 (尾随 NUL 产生的末位空元素就是「空元素」的一种)。一个**省略 rstrip、保留滤空串**的实现: 3 文件 diff → `split("\0")` → `[a,b,c,""]` → 滤空 → 3 个 ⇒ `count == 3` ✅、无空串 ✅ ⇒ **SC-29(b) 全绿**。⇒ **`rstrip` 无独立红窗; SC-29(b) 实际只能抓「两步皆缺」的实现。** 保留 rstrip 作为可读性冗余 (显式表达意图), 但**不得声称它有红窗** —— 「声称有红窗而实际没有」比缺步骤本身更有害 (这正是本轮 R6 反复指认的「义务写了、红窗没有」形状)。
  3. **字节→字符串解码契约 (A2/minor)**: `-z` 输出是**原始字节**, 且 git 不保证路径是合法 UTF-8。⇒ 用 `subprocess.run(..., capture_output=True)` 取 `bytes`, 以 `decode("utf-8", errors="surrogateescape")` 解码 (保持往返可逆, 与 Python 的 `os.fsdecode` 语义一致)。**不得**用 `text=True` 默认解码 —— 非 UTF-8 路径会抛 `UnicodeDecodeError`, 而本评估器承诺永不 raise。
  > 来源: L 的步骤 0。L 用 `-z` 规避 quotePath, 本 Spec 原方案 (`--name-only --no-renames`, 无 `-z`) 未处置该转义面。SC-29 三子用例分别锁 1/2/3。

### 1. 新增 `scripts/path_coverage.py` — workflow 触发覆盖评估器 (stdlib-only)

- **发现**: 仓根 `.forgejo/workflows/` + `.gitea/workflows/` + `.github/workflows/` 下 `*.yml` / `*.yaml`。
- **触发子集解析** (手写最小 parser, 不引 PyYAML — stdlib-only 硬约束, 先例 `custom_checks.py` minimal parser + `lib/detailed_tasks.py`): 只解析 `on:` 块的 `push` / `pull_request` 两类自动触发及其 `paths:` 列表 (块映射 + block list / flow list 两形)。
  - `on: push` 标量形 / `on: [push, pull_request]` 列表形 = 该触发**无 paths 过滤** → 该 workflow `covered` (D6);
  - **块映射形 + paths 子块是本仓 4 份语料的全部形态** (BA-9), 单独 SC-20 锁定 (不只靠语料测试隐式兜底);
  - **push 与 pull_request 逐触发独立判定, 任一会触发即该 workflow covered (OR 语义, QA-4)** — 两者 paths 不一致时不得只看其一。SC-17 双向锁定;
  - 「零覆盖贡献」触发键 = **精确白名单 {`workflow_dispatch`, `schedule`} 两键** (D7, 语料: tripwire); **其余任何未建模顶层触发键 (`pull_request_target` / `repository_dispatch` / `workflow_call` 等) 一律按未建模构造 → 该 workflow `covered`** (R2-C1 — 与 glob 未建模语法同一 fail 方向: `pull_request_target` 是真自动触发, 按字面归零贡献会产生假 not_applicable; SC-25 钉死); **混合触发** workflow (如 build-aria-runner: dispatch + push) 仅自动触发臂参与判定;
  - `paths-ignore` 在场 / anchors / 其他无法辨识的**构造级**内容 → 该 workflow 记 `covered` (per-workflow 级不确定, D2; **判据见 D12** —— anchors 的命中判定走 D12 的位置 ∧ 形态四段, 不靠本行的宽泛措辞)。**三类成因均计入 `uncertain_workflows`, 无真实匹配时整体 reason=`workflow-construct-uncertain` (规则 6b)** (A3/m-5+M-3);
  - **⭐ 构造级命中判据 (A1 并入 L-3, D12; A2 全面重写 — R5 三席 CRITICAL)**: 判据由**四段**构成, 缺任一段即欠定。
    **(1) 作用域 — 区间定义 (A2/C3)**: 构造扫描**只在「`on:` 键行 (含) → `on:` 块结束行 (不含)」的行区间内**进行。区间起点 = 识别到的顶层 `on:` 键所在物理行; 区间终点 = 该行之后**首个缩进 ≤ `on:` 键缩进的非空非注释行** (若无则文件末尾)。空行与纯注释行**跳过**: 既不参与判定, 也不终止区间。
      > A1 原文只写「对区间内每一行」而**全文无「区间」定义** —— 搬 L 的命中判据 (L:184) 时丢了紧邻的作用域子句 (L:182「只在 `on:` 键行到 `on:` 块结束的行区间内进行」)。本 Spec 无 L 的「规则 1/5」编号体系, 故就地定义。
    **(0) 键值拆分 — 前置步骤 (A3/m-1: 从原 (3) 提前, 消除定义自指)**: 对区间内每一物理行, 先剥行尾 `#` 注释 (quote-aware) → strip → 剥块序列标记 `- `, 再按**首个未被引号包裹的 `:`** 拆为**键**与**值**; **无 `:` 则整行为值, 键为空**。键与值各自再 strip。**后续 (1)(2)(3) 全部引用本步的产物。**
      > A2 把拆分放在 (3), 而 (2) 需要「该行的键」才能排除 —— (2) 用了只在 (3) 定义的概念, (3) 又只作用于「未被 (2) 排除的行」, 定义顺序不闭合 (R6/m-1)。提为 (0) 后无自指。
      > A1 原文写「值或键的首字符」却**未给拆分规则** ⇒ `push: &push_cfg` (最主流锚点写法) 首字符是 `p`, **不命中**。R5 两席对该输入**独立实现得出相反结果** —— memory `feedback_spec_underdetermination_two_implementer_test` 的直接实证。
    **(2) 值位互斥 — 位置 ∧ 形态双条件 (A2 引入, A3 按 owner 裁定重写 — R6 两条 CRITICAL)**:
      **(2a) 位置 — 值域归属计算 (A3/C-1: A2 未成文, 致原病第三次复发)**: 一行属于某 `paths:` / `paths-ignore:` 键的**值域**, 当且仅当满足其一 ——
      - 该行**就是**该 `paths:`/`paths-ignore:` 键行本身 (含 flow list 同行形态 `paths: ['a/**']`);
      - 该行**以 `- ` 开头**且缩进 **≥** 该键行缩进 (⚠️ **是 `≥` 不是 `>`** —— YAML 允许块序列项与父键**同缩进**, 见下方实跑);
      - 该行缩进 **>** 该键行缩进 (非序列项的续行)。
      **值域终点** = 首个「缩进 ≤ 该键行缩进 **且不以 `- ` 开头**」的非空非注释行 (无则区间终点)。**空行与纯注释行不终止值域**: 既不参与判定, 也不终止块 (与 (1) 同一约定, 此处**一字不差重述**, 不写「参见 (1)」)。
      > **A2 的 CRITICAL 缺陷 (R6 + 主控 PyYAML 6.0 实跑复验)**: A2 只写「缩进 **>** 该键行缩进」。实跑 `on:\n  push:\n    paths:\n    - '**.js'\n` → **解析成功** `{'push': {'paths': ['**.js']}}` ⇒ 同缩进块序列是完全合法的真实输入。缩进 4 的序列项不满足 `> 4` ⇒ 不被排除 ⇒ 落回 (3) 剥引号 → `**.js` → 首字符 `*` ⇒ 判 alias ⇒ **恒 wait, 与 A1 的失败链逐字相同**。同源第二缺口: A2 的 (2)(b) 无「空行/注释不终止块」子句 (而 (1) 有), 致 paths 列表中间的空行 / 列 0 注释按字面终止块。
      > **这是同一条失败链的第三个入口**: L-R4 (子串读法 `'*' in line`) → A1 (剥引号排在首字符判定前) → A2 (缩进比较符 `>`)。每次换入口, 同一个结果。
      **(2b) 形态 — 值域内的二次判定 (A3/C-2: owner 2026-07-30 裁定采用「位置 ∧ 形态」)**: 落在值域内的 token **不是无条件排除**, 而是按形态二分 ——
      - **带成对首尾引号** (`'...'` / `"..."`) ⇒ 判 **glob pattern** ⇒ **排除**出构造扫描;
      - **裸 token 且首字符为 `*` / `&` / `!`** ⇒ 仍判**构造级** ⇒ **不排除**, 走 (3) 命中 ⇒ 该 workflow 记构造级不确定 → covered;
      - 其余裸 token (如 `docs/**`, 不以 `*`/`&`/`!` 开头) ⇒ 判 glob pattern ⇒ 排除。
      > **判据依据 (PyYAML 6.0 实跑, R6 提出 + 主控独立复验)**:
      > ```
      > 裸  - **.js       → ScannerError: while scanning an alias
      > 引号 - '**.js'     → 解析成功 {'paths': ['**.js']}
      > 真 alias paths: *c → 展开为 ['a/**']
      > ```
      > ⇒ **YAML 层面, 值位上裸的 `*` 开头 token 必定是 alias; glob pattern 必定带引号** (裸 leading-`*` 根本不是合法 YAML 标量)。这条铁律使「位置 ∧ 形态」判据既消灭 C1 (`'**.js'` 带引号 ⇒ 排除) 又不放过真 alias (`*common_paths` 裸 ⇒ 命中)。
      > **⚠️ A2 的一条承重断言被本实跑推翻**: A2 原文写「glob 的 `*`/`!` 与 YAML 的 `*`/`&`/`!` 在同一位置的字符上不可靠区分…**唯一稳健的区分是按位置排除, 不靠字符形状**」。**「唯一稳健」是过强断言** —— 形态 (引号有无) 恰是可靠的第二维。该断言已删除。
      > **A2 无条件排除的后果 (R6/C-2, 本 Spec 迄今第一个 fail-OPEN)**: `paths: *common_paths` (键是 paths ⇒ 被排除) 与 `- *p` (在子块 ⇒ 被排除) 这两种**真 YAML 构造**失去唯一检出通道 ⇒ 手写 parser 拿不到真实 pattern ⇒ 零贡献 ⇒ **假 not_applicable ⇒ 闸门在 CI 本该拦它时放行**。之前所有缺陷的坏结果都是「多等 1800 秒」, 这条是误放行。且与 D2「绝不把『解析不了』当『无覆盖』」正面冲突 —— A1 在此点是 fail-CLOSED (难受但安全), A2 翻成了 fail-OPEN。
      > **`*` 为何两头落空 (M6 结论不可外推)**: 同位置的 `!` 有救 —— 归下方 glob matcher 条款 (未建模 glob 语法 → 判匹配 → covered)。但 **`*` 是本 Spec 已建模的 glob 字符**, 落不进 matcher 的「未建模」兜底 ⇒ A2 下 D12 不判它、matcher 不兜它。**A2/M6 关于 `!` 所有权无行为差异的结论, 对 `*` 不成立。**
      **(2c) 值形态兜底 (A3/C-2 第二道, 独立于 2b)**: `paths:` / `paths-ignore:` 的**解析后取值**不是 block list / flow list 两形之一 ⇒ 该 workflow 记**构造级不确定 → covered**, 并入 6b 成因。此条**即使 (2b) 被绕过也独立生效**。
      **⚠️「取值」的判定必须按解析后, 不按同行文本 (A3 自查拦下的第四次同形复发)**: `paths:` 键行同行为空、其后跟缩进块序列 —— **那是 block list**, 不是空值。若把「同行无内容」读成空值, 则**每一个正常的块序列 `paths:`** 都落 (2c) ⇒ 全判构造级不确定 ⇒ 恒 covered ⇒ **恒 wait**, 即同一条失败链的第四个入口。故 (2c) 的取值判定为:
      - 同行有 flow list (`paths: [...]`) ⇒ flow list ⇒ **不**触发;
      - 同行为空 ∧ 其后**存在**属于该键值域 (按 2a 计算) 的 `- ` 序列项 ⇒ block list ⇒ **不**触发;
      - 同行为空 ∧ 其后**无**任何值域内的 `- ` 序列项 ⇒ 真空值 ⇒ **触发**;
      - 同行为非 list 标量 (含 alias `*c` / 普通字符串) ⇒ **触发**。
      **`!` 前缀所有权 (A2/M6, A3 保留)**: 落在值域内**带引号**的 `!` 归 glob matcher (未建模语法 → 判匹配 → covered); 值域内**裸**的 `!` 归 (2b) (YAML tag → 构造级); 值域外的 `!` 归 (3)。三者互斥无重叠。
    **(3) 位置式判定**: 对 (0) 拆出的键与值**分别**做 —— 剥**成对**首尾引号后判: **键的首字符或值的首字符**为 `&` / `*` / `!`, **或键以 `<<` 开头**。`&` / `*` / `!` 出现在串**中间**一律**不算命中**。
    **逐例判定表 (承重算法钉到字符级)**:

    | 输入行 (含缩进) | 上下文 | (2a) 位置 | (2b) 形态 | 判定 |
    |---|---|---|---|---|
    | `      - '**.js'` | `paths:` 子块 (缩进 6 > 4) | 值域内 | 带引号 ⇒ 排除 | **不命中** ← A1 在此误判 |
    | `    - '**.js'` | `paths:` **同缩进** (4 ≥ 4) | **值域内** (A3 修) | 带引号 ⇒ 排除 | **不命中** ← **A2 在此误判 (C-1)** |
    | `      paths: ['*.py', '!docs/**']` | flow list 同行 | 键行本身 | flow list ⇒ 排除 | **不命中** |
    | `      - *p` | `paths:` 子块 | 值域内 | **裸 + 首字符 `*`** ⇒ 不排除 | **命中** ← **A2 在此误放行 (C-2)** |
    | `    paths: *common_paths` | 键行, 值是 alias | 键行本身 | **裸 + 首字符 `*`** ⇒ 不排除; 另 (2c) 独立命中 | **命中** ← **A2 在此误放行 (C-2)** |
    | `      - docs/**` | `paths:` 子块 | 值域内 | 裸但首字符非 `*&!` ⇒ 排除 | 不命中 |
    | `    push: &push_cfg` | `on:` 块内, 非值域 | 值域外 | — | **命中** (值首字符 `&`) ← A1 在此漏判 |
    | `      - *alias` | 非 paths 子块 | 值域外 | — | **命中** |
    | `    <<: *base` | `on:` 块内 | 值域外 | — | **命中** (键以 `<<` 开头) |
    | `    paths:` + 其后有值域内 `- ` 项 | 键行, 值 = block list | 键行本身 | block list ⇒ 排除 | **不命中** (正常形态) |
    | `    paths:` + 其后**无**值域内 `- ` 项 | 键行, 真空值 | 键行本身 | 非两形 ⇒ **(2c) 命中** | **命中** |
    | `    tags: !!str foo` | `on:` 块内 | 值域外 | — | **命中** (值首字符 `!`) |

    > **L 侧 R4 实跑背景 (原发现, 仍成立)**: 朴素子串读法 (`'*' in line`) 在本仓 4 份真实语料中**命中 3 份** —— `- 'skills/issue-triage/**'` / `- 'aria/skills/issue-triage/**'` / `- 'aria-orchestrator/docker/aria-runner/**'` ⇒ 恒 wait 复发。本 Spec 原文 (A1 前) 只写「anchors → covered」未定判据, 属欠定 —— 虽有 SC-2 作间接兜底, 但承重算法必须钉到字符级。SC-30 (A2 重写) 双向锁定。
  - **⭐ `---` 的 YAML 语义 (A1 并入 L-2, D13; A2 补区间与边界 — R5/M1)**: 列 0 的 `---` 出现在**首个「内容行」之后**才是多文档分隔 ⇒ 按构造级不确定判 `covered`; 出现在其**之前**是 **YAML 文档起始标记** ⇒ **忽略, 不触发任何判定**。
    **扫描区间 (A2 — 与 D12 不同, 须分别声明)**: `---` 扫描是**全文件**的 (文档级构造), **不**限于 D12 的 `on:` 块区间。两个区间**并存且互不影响**: D12 扫 `on:` 块内的节点标记, D13 扫全文件的文档分隔。实现上是两趟独立扫描, 顺序无关 (两者都只产出「该 workflow 构造级不确定」这同一个结论, 不存在相互覆盖)。
      > A1 只写「列 0 的 `---`」未声明区间, 而 D12 紧邻处明确说了 `on:` 块区间 ⇒ 实现者会自然沿用上一条的区间, 使 `on:` 块**之外**的多文档分隔漏检 (R5 backend-architect + code-reviewer 双席命中)。
    **「内容行」定义 (A2 — 四个分叉点逐条封闭)**:
    1. **内容行 = 非空行 ∧ 非纯注释行**。`---` 自身**算内容行**(它是文档级 token, 不是空白)—— 故文件里的**第一个** `---` 若前面只有空行/注释, 它是文档起始标记 (忽略); 此后再出现的列 0 `---` 一律是分隔符 (命中)。
    2. **连续两个 `---`**: 第一个按 1 判 (前无内容行 ⇒ 忽略), 第二个此时前面已有内容行 (第一个 `---`) ⇒ **命中**。
    3. **`%YAML` / `%TAG` 指令行**: 算内容行。⇒ `%YAML 1.2` 后紧跟的 `---` 前面已有内容行, 按字面会命中。**显式豁免**: **跳过空行与纯注释行后**的第一个列 0 `---` 仍是文档起始标记 ⇒ 忽略 (YAML 规范要求指令后必须有 `---`)。
      > **A3/m-3**: A2 写「**紧随** `%`-指令块之后」而未定义「紧随」是否容许中间夹空行/注释。YAML 允许。物理下一行的读法下 `%YAML 1.2` + 空行 + `---` 会命中 ⇒ covered ⇒ 恒 wait。改为「跳过空行与纯注释行」, 与 (1)/(2a) 对空行注释的处理**同一约定**。
    4. **精确匹配形态 (A3/m-2 修必要条件)**: 只有**列 0 起始 ∧ 整行去行尾空白后恰为 `---`** 才参与判定。`--- foo` (带内容) / `----` (四连字符) / **缩进 > 0 的 `  ---`** 均不参与。
      > **A3/m-2**: A2 首句写「只有**整行 strip 后**恰等于 `---` 才参与判定」—— 按字面**包含** `  ---` (strip 后正是 `---`), 与紧接着的排除项「缩进 > 0 的 `---` 均不参与」**自相矛盾**。照首句实现的人会把块标量里的缩进 `---` (例: `run: |` 内 heredoc 输出 YAML frontmatter) 判成多文档分隔 ⇒ covered ⇒ 恒 wait —— L 侧 R3 那个 `echo "--- image size ---"` 坑的近亲。A3 把「列 0」提进**必要条件本身**, 排除清单退化为示例。
    5. **`...` (document-end marker) — A3/m-7**: 列 0 且去行尾空白后恰为 `...` 的行, **与列 0 `---` 同等对待** (记构造级不确定)。
      > 多文档 YAML 的另一个文档级 token 是 `...`。`on: push` … `...` … 之后再起内容构成第二个文档而**不出现 `---`** ⇒ 只建模 `---` 时检测不到, 手写 parser 会把两个文档的键混读成一份。现实度低 (workflow 极少用), 但「封闭了吗」的诚实回答是: **A2 对 `---` 封闭度已高, 对文档级 token 整体未封闭**。A3 补齐。
    > L 侧 R4 实跑: 把首行 `---` 当多文档分隔 ⇒ 该仓**任何**变更恒 covered ⇒ 恒 wait。`yamllint` 的 `document-start` 规则**默认要求**首行 `---`, 与本 Spec 自己援引的 `on:  # yamllint disable-line` 是同一批用户 ⇒ 触发面现实。本仓语料 4/4 首行为注释, 今天零代价, 但对采用者非零。**本 Spec 原文 (A1 前) 全文未提 `---`** ⇒ 实现者遇到时只能归入「其他无法辨识的构造级内容」→ covered ⇒ 正是该 bug。SC-31 (A2 重写) 四子用例逐条锁。
  - `branches` 过滤**不建模** — 只会减少触发, 不建模方向落 covered, 行为不劣于现状 (语料正例: build-aria-runner 的 branches+paths, 按 paths 交集判)。
- **glob 匹配**: 自研 matcher, `**` (跨目录) / `*` (单段) / `?` 语义对齐 forgejo/GHA paths 规则 (SC-14 表驱动, **期望值来源标注 forgejo 官方 paths 文档条目**, TL-7); **对任何未建模 glob 语法片段 (字符类 `[abc]` / 否定 `!` / 其他) 一律判定为「匹配」→ 该 workflow covered** (BA-1, matcher 层的 fail 方向显式钉死; SC-14 含字符类/否定用例); 大小写敏感 (QA-8, SC-14 含不匹配用例)。
- **changed files**: `git diff --name-only --no-renames -z <main_branch>...<pr_branch>` (merge-base 三点 + `-z`, §0 契约; 解析 `rstrip("\0").split("\0")` 后滤空串)。
- **判定 (全分割, 互斥+全覆盖 — R2 修正: 规则序 = 数据依赖执行序; reason 字面值全封闭, R2 四方交叉命中 [TL-Major-1 / BA-R2-M1 / QA-9 / CR-N-1])**:
  1. `git diff` 失败 (含 main ref 缺失 / 非 repo / shallow 缺 merge-base) → 整体 `unknown`, reason=`git-diff-failed: <stderr 摘要>`;
  2. diff 成功但输出为空 → 整体 `covered`, reason=`empty-diff` (异常形态, 保守);
  3. changed_files 中**任一条位于三个 workflows 目录下** → 整体 `covered`, reason=`workflow-files-changed` (D10 硬规则: 对 CI 配置本身动刀的 PR 永不 not_applicable);
  4. workflow 文件枚举: **零 workflow 文件 → `not_applicable`, reason=`no-workflow-files`** — **循环前置短路, 不进入规则 5** (消除规则 8 旧版全称谓词在空集上的空真重叠);
  5. 逐 workflow 解析: 解析成功 → 判触发 (covered / 零贡献); 文件读取或 YAML 结构解析失败 → 记 `parse_failed`;
  6. **(A2/C4 拆分 — 原规则 6 折叠了两种成因)** 任一解析成功的 workflow 判 covered → 整体 `covered`, 但 reason **按成因二分**:
     - **6a** 存在 workflow 因**真实路径匹配** (步骤 4 的 paths 命中 / 无 paths 过滤) 判 covered → reason=`workflow-trigger-matched` (+ `matched_workflows` 列全);
     - **6b** 无任何真实匹配 ∧ 存在 workflow 因**构造级不确定** (D12 节点标记 / D13 多文档分隔 / `paths-ignore` 在场 / 其他不建模构造) 判 covered → reason=**`workflow-construct-uncertain`** (+ `uncertain_workflows` 列全该类 workflow 路径);
     - 优先级 **6a > 6b > 规则 7** (真实覆盖 > 构造不确定 > 解析失败; **covered 优先于 parse_failed 的存在** — 已证明真实覆盖是更强信号, BA-4);
     > **为什么必须二分 (R5 qa-engineer CRITICAL + code-reviewer MAJOR)**: 折叠成单一 `workflow-trigger-matched` 有三重后果 —— (i) 上报的 reason 是**事实错误** (没匹配上却说匹配了); (ii) 对 D9 的可观测性义务**隐形** (「评估没能确定」这个信息被伪装成「确定覆盖」); (iii) 使 **SC-31(a) 的自证失效** —— 「若把首行 `---` 误判为多文档分隔则必红」不成立, 因为两种实现在该 fixture 上输出**逐字节相同**。二分后 SC-31(a) 可断言 reason == `workflow-trigger-matched`, 误判实现会产出 `workflow-construct-uncertain` ⇒ **可红**。同理救活 SC-30 正控。
  7. 无 covered (含 6a/6b 均不成立) ∧ 存在 `parse_failed` → 整体 `unknown`, reason=`workflow-parse-failed: <files>`;
  8. 无 covered ∧ 全部解析成功 (此时必有 ≥1 个 workflow, 由规则 4 保证) ∧ 全部判不触发 → `not_applicable`, reason=`no-triggering-paths` (与规则 4 语义区分:「有 workflow 但都不命中」vs「压根没 workflow」)。
  规则 1-8 互斥且穷尽 (6a/6b 内部亦互斥, 由「无任何真实匹配」这一前置条件保证); **此序即数据依赖执行序** (diff 先行 → diff 结果三分 [规则 1/2/3] → 文件枚举短路 [规则 4] → 解析与聚合 [规则 5-8]), 可直译为 if/elif 实现 (QA-11)。

  **reason 封闭集 (A3 后共 9 个)** — 产生终态判定的 reason 字面值:
  `git-diff-failed` / `empty-diff` / `workflow-files-changed` / `no-workflow-files` / `workflow-trigger-matched` / `workflow-construct-uncertain` / `workflow-parse-failed` / `no-triggering-paths` / **`internal-error: <exception 类型 + 摘要>`** (A3/M-1 新增)。

  - **`internal-error` 的产生方 (A3/M-1)**: **只**由「永不 raise」的全捕获兜底产生 (规则序之外的横切分支), `decision` **恒为 `unknown`**。
    > **为什么必须新增这个槽 (R6/M-1)**: 封闭集里能产 `unknown` 的原本只有 `git-diff-failed` (规则 1) 与 `workflow-parse-failed` (规则 7)。而全捕获要接住的是**任意位置的内部异常** —— 最可能的来源恰是 A2/A3 新引入的值域归属计算、键值拆分、`---` 扫描。此时按封闭集上报**只能冒用**那两个 = **事实错误的 reason**, 正是 C4 判为 CRITICAL 的那个病在兜底分支复发。具体后果: 值域计算里一个 `IndexError` 会以「评估失败 (git-diff-failed)」的面貌出现, 运维去查 git 与 main ref, 而真 bug 在 parser 里, 且**每次稳定复现却永远指向错误方向** (memory `feedback_issue_reporter_root_cause_may_miscite` 的机制化版本)。
  - **满射口径 (A3/M-3 勘正)**: 封闭集与测试矩阵的满射按**规则分支**计, **不按 reason 字面值计** —— 「每个 reason 至少被某条 SC 断言过」不保证「每条产生该 reason 的**路径**都断言了 reason」(R6/M-3 实证: `paths-ignore` 与 `pull_request_target` 两个最高频 6b 成因的既有 SC 都没断言 reason)。
  - **短路路径的 `workflows_scanned` (A3/m-6)**: 规则 1/2/3/4 均在「逐 workflow 解析」**之前**返回, 此时 `workflows_scanned` **恒为 0**, `uncertain_workflows` 恒为 `[]` —— 但其含义是「**没扫**」而非「**扫了没有**」。⇒ 下游 (含 D15 的 AI 判断) **不得**单凭 `uncertain_workflows == []` 判定「评估干净」, 必须合取 `workflows_scanned > 0`。该读法写入 D15 的判断条件。
- **返回契约 (A2/C4 增一键)**: `{"decision": "covered"|"not_applicable"|"unknown", "workflows_scanned": int, "matched_workflows": [str] (相对仓根的 workflow 文件路径, QA-7), "uncertain_workflows": [str] (**A2 新增** — 因构造级不确定判 covered 的 workflow 路径; 规则 6b 的证据面, 恒存在, 无则 `[]`), "changed_files_count": int, "reason": str}`。永不 raise (内部全捕获 → unknown + reason)。
  > `matched_workflows` 与 `uncertain_workflows` **语义不重叠**: 前者是真实路径匹配的, 后者是构造读不懂而保守放过的。两者都非空时 reason 取 `workflow-trigger-matched` (6a 优先), 但两个列表**各自照实填** —— 否则「有 workflow 读不懂」这个事实在 6a 路径上再次隐形 (C4 的同一病在另一分支)。

### 2. `gate_check()` 集成 (`pre_merge_gate.py`)

评估点: backend 解析成功 + precheck 通过之后、**(a) PR CI 查询之前; (b) main in-flight 查询保持无条件执行, 顺序仍 (b) 先 (a) 后** (TL-6 — 与代码真实 query 顺序 :317→:330 一致表述)。**集成符号 (QA-12)**: 评估器以模块级函数 `evaluate_path_coverage` 挂在 `pre_merge_gate.py` 命名空间 (镜像 `resolve_ci_backend` 可 mock 先例), SC-9/10/21/22 的测试骨架统一 `mock.patch.object(gate, "evaluate_path_coverage", ...)`。

- `decision == "not_applicable"` → **跳过 (a) PR CI 查询与其 wait** (实现须保证 `backend.query_pr_ci` 不被调用, SC-9/10 以 `assert_not_called` 钉死, QA-2); `pr_ci_status = "not_applicable"`; **(b) 照跑不减** (D3 — SilkNode PR-321 事故是 (b) 轴, 正交不放松);
- `compute_verdict` 扩展: 写**显式** `elif pr_ci_status == "not_applicable":` 分支 (BA-8 — 不依赖现有 fallthrough 隐式兜底, 防未来改兜底逻辑时悄悄改变语义): in-flight 空 → `green` (raw_message 留痕); in-flight 非空 → `wait` (仅 (b) 轴驱动, message 指明);
- **NIE 交叉不变量 (TL-4)**: not_applicable 只免 (a); stub backend 的 NIE 经 (b) 查询照常 propagate (abort), 不被 not_applicable 掩盖。「(b) 无条件先跑」这一正交性前提锁进测试 (SC-21);
- `covered` / `unknown` → gate 输出**既有字段逐字段不变** + additive `path_coverage` 键 (CR-5 口径; SC-11 断言口径=既有字段; 承认行为面增量: covered 路径每次 gate 新增 1 次 git diff subprocess + workflow 文件 IO);
- no-backend (`no_ci_fallback`) / `enabled:false` / `ci_backends:[]` / NIE-propagation 各路径**全部不变** (正交 — 评估只在 backend 可用臂内发生);
- gate_check docstring 「matches current Aether subprocess invocation count」同步更新 (BA-7 — not_applicable 使 (a) 调用数条件化)。

### 3. Output schema (additive-only)

- `pr_ci_status` 增值 `"not_applicable"` (gate 侧产生, **backend `CIStatus` Literal 不动** — 该态从不来自 backend 查询, D1);
- 新增顶层 `path_coverage` object (§1 返回契约原样)。**键出现范围 (BA-6)**: 仅在「评估已执行且流程走到 `compute_verdict` 最终路径」的输出携带; backend-query-failure 早退分支 / precheck 失败 / no-backend / enabled:false 输出保持既有六键不变。`_build_output` 增可选参数 (Impact 表列入);
- SKILL.md Output schema 行改写时一并处置预存漂移: 注明 `not_found` 来自 backend `CIStatus` 层、`not_applicable` 来自 gate 层 (CR-6)。

### 4. Config (additive)

`phase_c_integrator.pre_merge_gate.path_coverage_enabled`: bool, **默认 `true`** (D4; 扁平键名 — namespace 内不嵌套是本仓惯例, KM-8)。默认值锁定测试 (SC-12)。**既有 62 测试隔离方法论 (QA-3)**: Phase B 统一给既有 GateCheckTests/FallbackTests mock path_coverage 评估器入口 (不改测试语义), 并新增卫生断言 SC-22「既有套件运行期间零真实 git 子进程」。

### 5. 可观测性义务 (D8+D9, R1 BA-5 扩展)

- `not_applicable` → AI 必须在 workflow report surface 警告行:「C.2.4: 变更路径无 CI workflow 覆盖, PR CI wait 已跳过 (not_applicable), main in-flight 已核」;
- **`unknown` 同样进 surface 面 (D9; A3/M-1 扩枚举)**: 警告行含 reason (`git-diff-failed` / `workflow-parse-failed` / **`internal-error`**),「评估失败, gate 已按 covered 现状行为处理」 — 防评估器自身静默失效 (与本 spec 批评的「零信息量→被忽略」同病, 不能换个位置复发)。**`internal-error` 的文案须点明「评估器自身异常 (非 git / 非 workflow 解析), 请报 issue」** —— 否则它会被读成外部环境问题, 正是 M-1 要防的误诊;
- **`uncertain_workflows` 非空 ⇒ 进 surface (A2/D15, C4 修复; A3/M-2 文案按路径二分)**:
  - **6b 路径** (reason == `workflow-construct-uncertain`): 「C.2.4: N 个 workflow 的触发定义含不建模构造 (`<uncertain_workflows>`), 已保守按 covered 处理 — 若本应 not_applicable 则表现为多余等待」;
  - **6a 路径** (reason == `workflow-trigger-matched` ∧ `uncertain_workflows` 非空): 「C.2.4: 本次 covered 由**真实路径匹配**得出 (`<matched_workflows>`); 另有 N 个 workflow 的触发定义含不建模构造 (`<uncertain_workflows>`), 其覆盖贡献**未参与判定**」。
  > **为什么文案必须二分 (R6/M-2)**: A2 只写了一套文案, 而它逐字说「已保守按 covered 处理 — 若本应 not_applicable 则表现为多余等待」。在 6a 上 covered 是**真实匹配**得出的, 不是保守兜底; 那个 workflow 读不懂与否不改变结论, 更没有「多余等待」。⇒ A2 **强制 AI 在 6a 上报一句事实错误的解释**, 与 C4 要治的「上报事实错误」同形。
  > **它与 D9 是同一条原则的第三个落点**: `unknown` 是「评估失败」, `construct-uncertain` 是「评估成功但读不懂一部分」—— 后者以 `decision=covered` 输出, **最容易被当成正常结果吞掉**。A1 把它折叠进 `workflow-trigger-matched` 正是这种吞掉的实例。
  > **判断条件须合取 `workflows_scanned > 0` (A3/m-6)**: 规则 1/2/3/4 短路时 `uncertain_workflows` 恒 `[]` 但含义是「没扫」。AI **不得**据 `uncertain_workflows == []` 单独判定「评估干净」。
- 三义务写入 SKILL.md §C.2.4 指令面 (**落点见 §6, A3 已补 D15 的逐处点名**)。

### 6. SKILL.md 同步清单 (KM-1/2/3 修正, 逐处点名不数数)

phase-c-integrator/SKILL.md:
- `:39-53` 顶部总览配置表 (KM-3) — 增 `path_coverage_enabled` 行;
- `:176` 紧凑 YAML 预览块 `pr_ci_status` 枚举 (KM-2 — 历史上从不随详细版同步, 显式点名);
- 执行流程插「2.5 Path coverage 评估 (v1.65.0+)」(KM-7 版本标注) + §0 执行上下文契约;
- `:241-245` verdict 计算 (bullet list, CR-3 措辞) 增 not_applicable 两行;
- `:246-249` 路由决策 + **D8/D9/D15 三条** surface 义务 (A3/M-7 — A2 只点名 D8/D9 而自己新增了 D15)。⚠️ **含新增通道**: 实读 SKILL.md `:236-262`, **covered 路径当前无任何 surface 通道** (现文只在 `fail` 分支输出 raw_message) ⇒ D15 的 `uncertain_workflows` 上报需**新建**该通道, 不是改文案;
- `:258-270` Output schema (含 CR-6 漂移处置);
- `:272-281` §C.2.4 内配置参数表;
- `:283-289` 降级行为 (补 fail-toward-covered 边界与判定全分割摘要)。

`aria/skills/config-loader/SKILL.md:241-281` (KM-1, 第二权威 config schema 登记, CR-N-3 范围勘正至 `user_escape_hatch` 末条): 增 `path_coverage_enabled` 条目 (type: boolean, default: true, v1.65.0+ 注记)。

`aria/skills/workflow-runner/references/workflow-state-schema.md:125` (KM-10): `raw_message` 字段说明补注「v1.65.0+ 起 not_applicable/unknown 态的 path_coverage 提示文案也经此字段传递, 非仅 fail」(gate_state.status 三态不变, 无结构性同步)。

### 7. 主仓 `.aria/config.json` 注释退役 + DEC 存档 (Phase D, 主仓侧; R1 TL-5/KM-5/KM-6 重写)

- **先存档后改写 (KM-5)**: 改 `_lane` 之前, 把 2026-07-25 owner 裁决全文抽取存 `docs/decisions/DEC-2026MMDD-NNN-*.md` (canonical 目录, 近期命名惯例), `_lane` 改写后留指针;
- **co-land 硬时序 (TL-5)**: `_lane` 过渡规则 (2) 的退役编辑必须与「主仓 gitlink bump 到含 not_applicable 机制的 v1.65.0」**同一个主仓 commit** 落地 — 消除「规则已退、pinned 子模块无机制」的裸奔窗口;
- **三注释字段同批处置 (KM-6)**: `_comment` (现状陈述改写) / `_lane` (退役+指针) / `_not_ci_backends_empty` (前瞻引用改「已实现」过去时); `_open_question_no_ci_fallback` 保持挂起 (非目标);
- 改写稿须 owner 过目 (它是 owner 的裁决记录)。

---

## 决策记录

| # | 决策 | 要点 |
|---|------|------|
| D1 | 评估落 gate 侧, 非 backend 侧 | backend-agnostic; `CIStatus` Literal 不动 (代码级已核: not_applicable 从不来自 backend) |
| D2 | fail-toward-covered = 行为承诺; decision 字面分两档 | **构造级**不确定 (可读 YAML 但含不建模特性) → 该 workflow covered; **解析失败** (读不了/YAML 坏) → per-workflow 记 parse_failed → 聚合无 covered 时整体 unknown (TL-Minor-3 二分); 两档 gate 行为均=现状 (CR-2 重写) |
| D3 | (b) 轴不免除 | not_applicable 只跳 (a); NIE 经 (b) 照常 propagate (SC-21) |
| D4 | `path_coverage_enabled` 默认 true | owner sign-off 单独点名此项 (TL-8); SC-12 锁定; 既有测试隔离 SC-22 |
| D5 | stdlib-only 手写触发子集 parser | 语料 = 本仓 4 真实 workflow (含三种触发形态) + GHA 文档形态 |
| D6 | 无 paths 的 push/pull_request → covered | 标量/列表/块映射三形; 块映射+paths 单独 SC-20 |
| D7 | 零覆盖贡献 = 精确白名单 {workflow_dispatch, schedule} | 其余未建模触发键 (pull_request_target 等) → covered (R2-C1); 纯 dispatch 语料 = tripwire (唯一); 混合触发仅自动臂参与 (build-aria-runner 正例, TL-3 勘正) |
| D8 | not_applicable 双留痕 + AI surface 义务 | raw_message + path_coverage field + SKILL.md 指令警告行 |
| D9 | unknown 同样 surface (BA-5) | 评估器自身失效必须可见, reason 可辨 (TL-1c) |
| D10 | workflow 文件自身变更 → 强制 covered (QA-1) | 判定规则 3 (diff 层最先的语义规则); 对 CI 配置动刀的 PR 永不 not_applicable |
| D11 | 执行上下文成文 (TL-1/BA-2) | cwd=目标仓根 + main_branch 显式传值 + gitlink 语义 + --no-renames + **`-z` (A1/D14)** + 非浅克隆前提 |
| **D12** (A1, A2 重写, **A3 按 owner 裁定改判据**) | 构造级命中判据 = **(0) 键值拆分 + (1) 区间 + (2a) 位置 + (2b) 形态 + (2c) 值形态兜底 + (3) 位置式判定** | **A3 的关键: 值位互斥从「纯位置」改为「位置 ∧ 形态」** (owner 2026-07-30 裁定)。依据 PyYAML 实跑: **裸 `- **.js` → ScannerError (必为 alias); 引号 `- '**.js'` → 解析成功** ⇒ 值域内**带引号者判 pattern (排除)、裸且首字符 `*&!` 者判构造级 (不排除)**。**A2 的两条 CRITICAL**: (C-1) 值域归属只写「缩进 `>`」, 排不掉 YAML 合法的**同缩进块序列** ⇒ 恒 wait 第三次复发 ⇒ A3 改 `≥` + 定义块终点 + 空行注释不终止; (C-2) 无条件排除使 `paths: *alias` 真构造被当 pattern ⇒ **假 not_applicable (第一个 fail-OPEN)** ⇒ A3 由形态维度救回 + (2c) 独立兜底。**A2 的「唯一稳健的区分是按位置」断言已被实跑推翻并删除。** 另: 键值拆分提为 (0) 消除自指 (m-1)。SC-30 十五子用例 |
| **D13** (A1, **A2 补边界**) | 首个 `---` = YAML 文档起始标记, **忽略** | 扫描区间 = **全文件** (与 D12 的 `on:` 块区间并存, 两趟独立扫描)。「内容行」四个边界封闭: `---` 自身算内容行 / 连续两个则第二个命中 / `%`-指令后首个 `---` 豁免 / 只有 strip 后恰等于 `---` 才参与。SC-31 五子用例 |
| **D14** (A1, **A2 补前提**) | `git diff` 带 `-z` + rstrip + 滤空串 + surrogateescape 解码 | 三条义务一体。**红窗前提须显式**: quotePath 转义只在 `core.quotePath=true` 时发生 (git 默认值, 可被关) ⇒ 评估不依赖其取值, 但 SC-29(a) 必须显式设 true 且锁唯一匹配项。解码用 `surrogateescape` 而非 `text=True` (后者遇非 UTF-8 路径抛异常, 违背永不 raise)。SC-29 四子用例 |
| **D13** 补充 (A3/m-2+m-3+m-7) | `---` 判据三处收口 | 「列 0」提进**必要条件本身** (A2 首句「整行 strip 后恰等于 `---`」与自身排除项矛盾); `%`-指令豁免的「紧随」= **跳过空行与纯注释行后**; 新建模 `...` document-end marker |
| **D15** (A2/C4, **A3 扩**) | reason 封闭集增槽 + 返回契约增 `uncertain_workflows[]` + surface 三义务 | A2: 规则 6 拆 6a/6b, 增第 8 槽 `workflow-construct-uncertain`。**A3 增第 9 槽 `internal-error`** (M-1: 全捕获兜底原本只能冒用 `git-diff-failed`/`workflow-parse-failed` = 事实错误 reason, C4 的病在兜底分支复发); **surface 文案按 6a/6b 二分** (M-2: A2 单套文案在 6a 上说「已保守按 covered 处理…多余等待」是事实错误); **满射口径改按规则分支计** (M-3); 短路路径须合取 `workflows_scanned > 0` 才可判「评估干净」(m-6) |
| **D16** (A3/M-4+M-5) | SC-32 落**主仓侧**并断言**本次新产出**的 benchmark.json | A1 落点结构上永不执行; A2 落点跨 git repo (test 在 `aria` gitlink 子模块, 文件属主仓) ⇒ 独立 clone 下 error 或 `skipIf` 恒 skip 假绿, 且守的是**冻结归档** ⇒ 断言今天就已成立。A3: 同仓 + 断言新产出 + **文件缺失 = FAIL, 禁 `skipIf`** |

**Rule #6 (rule6_note)**: SKILL.md §C.2.4 为**处方性·运行时指令面** (新增 verdict 分支的 AI 处理指令 + surface 义务) → 判据决策表第二行, **照跑 AB** (phase-c-integrator: ab-suite 3 selected evals [source 5]; `phase-c-integrator-pre-merge-gate.json` 6 fixtures 一并纳入执行面 — 其形态与 SC-2/9/10 天然相关, CR-4), 零裁量。

**⭐ AB 执行面三处勘正 (A1 并入 L-5; A2 订正归因与第 1 条的方向 — R5/C6+M4)**:

> **来源归因 (A2/M4 订正)**: A1 表头写「L 侧 R2 5/5 席实地核实」, 把三项一并归因于 post_spec-R2 的 5/5 强共识。**实测不准**: 第 1/2 项确出自 L 的 **post_spec-R2 (5/5)**; 第 3 项 (`measured` 是 int) 首见于**另一检查点** L 的 **post_planning-R2 的单席 code-reviewer** (severity major, 非 critical)。三项结论经本轮 R5 knowledge-manager 内容级独立复核**均确认为真**, 仅证据强度标注需订正。

| # | 陷阱 | 正确做法 | 来源 |
|---|------|---------|------|
| 1 | **裸名 `phase-c-integrator` 解析会漏掉 fixture 套件** | 按 `AB_TEST_OPERATIONS.md` §场景1 的解析流程, 裸名只命中 parent 套件 `ab-suite/phase-c-integrator.json` (含 commit-generation / merge-conflict-handling / multi-remote-merge-push 三个 **LLM eval**)。⚠️ **A2/C6 方向订正**: 正确做法**不是**「排除 parent 改点全称」, 而是**两个套件都跑** —— parent 套件是**唯一有 LLM `evals` 的**, 它测的正是 SKILL.md §C.2.4 指令面 (本 change 的处方性变更所在), 排除它等于让 Rule #6 失去 AB 双臂对象; `phase-c-integrator-pre-merge-gate.json` (6 structural fixtures) 测确定性判定面。**两个执行面并列, 缺一不可** | L post_spec-R2 (5/5) + **R5 tech-lead 方向订正** |
| 2 | **基线路径不能用 `latest` symlink 或「最近一次归档」** | **structural 臂基线写死** `aria-plugin-benchmarks/ab-results/2026-05-10-phase-c-integrator-pre-merge-gate/benchmark.json`。⚠️ **A2 理据订正**: A1 说「最近一次归档」也解析到 state-scanner, 实测**最近一次归档是 `2026-07-20-v1.62.0-phase4-rule6`** —— 结论 (不能用相对选取) 仍成立, 但理由是「相对选取不稳定」而非「它恰好指向 state-scanner」。<br>⚠️ **A3/M-6 补对照臂**: **LLM eval 臂 (parent 套件 `phase-c-integrator.json`) 的 A 臂基线 Spec 未指定, 且 `ab-results/` 27 个归档中 parent 套件基线实测为 0 个**。⇒ Phase B 前须确认; **若确认不存在历史归档, 则本次为首建基线, 必须在 rule6_note 与 AB 存档里显式声明「parent 套件本次无 A 臂, 回归结论只覆盖 structural 臂」** —— 不得无声地把单臂当双臂跑过了 | L post_spec-R2 (5/5) + **R5 双席理据订正 + R6/M-6 对照臂缺口** |
| 3 | **`structural_metrics.*.measured` 是 `int` 不是 `str`** | 既有 8 个指标断言 `measured` 保持**整数 `100`** (`unit:"percent"` 另存, R5 实地复核 8/8 确为 `int 100`); 只有 `primary_pass_gate.measured` 才是字符串 `"100%"`。写成 `"100%"` 会产出**恒假断言** (同 L 侧 N-γ 的病因: `dict == str` 恒 False ⇒ 无红→绿窗口) | L **post_planning-R2 单席** (A2 订正) |

新增 `not_applicable` 指标无历史对照, 只需 `measured == 100`; **只追加, 不改既有 8 个指标的定义与分母**。存档目录 `ab-results/<date>-v1.65.0-phase-c-gate-path-coverage-not-applicable/`。

**⚠️ 可机械化程度分层 (A2/C5 — 三条不能一律当 SC)**:

| 条 | 被测对象 | 可机械断言? | 落点 |
|---|---------|-----------|------|
| 1 | AB 套件的**解析与选取行为** (人/AI 执行期 judgment) | ❌ 仓内无可调用的套件路径解析代码 | **执行手册约束** — 写进 `AB_TEST_OPERATIONS.md` + TASK 级 checklist |
| 2 | 基线**选取**决定 (含 A3 新增的「LLM 臂无 A 臂时须显式声明」) | ❌ 同上 | **执行手册约束** |
| 3 | **本次新产出**的 `benchmark.json` 里 metric 的**类型** | ✅ 可对该文件实跑断言 | **SC-32 (A3 重定落点, 见下)** |

**⚠️ SC-32 落点的两次纠错 (A3/M-4+M-5)**:

| 版本 | 落点 | 断言对象 | 失效方式 |
|---|---|---|---|
| A1 | `aria-plugin-benchmarks/` | — | 被 `run_all_tests.sh` (硬编码 `SKILLS_DIR="skills"`) **结构上永不执行** |
| A2 | `aria/skills/phase-c-integrator/tests/` | **2026-05-10 冻结归档** | (a) 测试在 `aria` 子模块 (gitlink → `10CG/aria-plugin`), 被断言文件属**主仓** ⇒ aria-plugin 独立 clone 下路径不存在 ⇒ error 或 `skipIf` **恒 skip 假绿**; (b) 守的是本 change 一字节都不会碰的冻结文件 ⇒ **断言今天就已成立**, 对「这次会不会写错」零信息 |
| **A3** | **主仓侧**发版门禁 (与被断言文件同仓) | **本次新产出**的 `ab-results/<date>-v1.65.0-phase-c-gate-path-coverage-not-applicable/benchmark.json` | — |

**A3 定案**: SC-32 落**主仓侧**, 断言**本次新产出**的 benchmark.json —— 全部 `structural_metrics.*.measured` 为 `int`、`primary_pass_gate.measured` 为 `str`、新增 `not_applicable` 指标 `measured == 100` (int)。**文件缺失 = FAIL, 显式禁止 `skipIf(not exists)`** (缺失意味着 AB 没跑, 那正是要拦的)。**路径解析基点**: 主仓根。
> 这样「本次把 `measured` 写成 `\"100%\"`」这个**真正要防的错**在 Phase C 发版前会红; 而 A2 版守着冻结归档, 那个错**不会**让任何断言变色。config-loader/SKILL.md 登记条目为描述性 schema 同步 (substitute: 结构化测试)。确定性代码层 (path_coverage.py / pre_merge_gate.py) 由 SC-1~28 结构化测试覆盖 (计数经 CR-N-2 / QA-14 两轮勘正), 与 AB 并行不互替。

**Rule #8 自指说明**: 本 cycle 自身的 C.2 合并 (aria 子模块内, cwd=aria/, 变更路径 `skills/phase-c-integrator/**`, aria 仓唯一 workflow paths=`skills/issue-triage/**` 零交集) 即 not_applicable 的**首个生产用例** — 实现完成后用新机制走正门, meta-dogfood。若新机制对自身产出非预期判定, 即为发版前最后一道真实性检验。注意 §0 契约: 评估发生在 aria 子模块根, 非主仓根 (BA-2 双树歧义在 dogfood 场景的正确侧)。

---

## Success Criteria (SC, 全部可测)

| SC | 场景 | 期望 |
|----|------|------|
| SC-1 | 零 workflow 文件 | `not_applicable`, reason=`no-workflow-files` (规则 4 前置短路产出) |
| SC-2 | aria 仓真实语料回归 (issue-triage paths workflow + 变更 `skills/run_all_tests.sh`) | `not_applicable`, reason=`no-triggering-paths` (复发形态钉死) |
| SC-3 | 变更含 `skills/issue-triage/x.py` | `covered`, reason=`workflow-trigger-matched`, matched_workflows 含该 workflow 路径 |
| SC-4 | push 无 paths 过滤 (块映射形) | `covered`, reason=`workflow-trigger-matched` |
| SC-5 | `on: [push]` 列表形 / `on: push` 标量形 | `covered`, reason=`workflow-trigger-matched` |
| SC-6 (**A3 回填** — R6/M-3) | `paths-ignore` 在场 (fixture 须**无任何真实 paths 匹配**, 否则落 6a) | `covered` ∧ **reason == `workflow-construct-uncertain`** ∧ **`uncertain_workflows` 含该 workflow** (A2 只写「`covered` (per-workflow 档)」, 无 reason 无列表 ⇒ 折叠进 6a 的实现全绿, 而 `paths-ignore` 是**最高频**的 6b 成因) |
| SC-7 | 全部 workflow 畸形 YAML (构造) | `unknown`, reason=`workflow-parse-failed` → gate 行为=现状 |
| SC-8 | git diff 失败 (ref 不存在 / 非 repo) | `unknown`, reason=`git-diff-failed` → gate 行为=现状 |
| SC-9 | not_applicable ∧ main in-flight 非空 | `verdict=wait` + **`query_pr_ci.assert_not_called()`** |
| SC-10 | not_applicable ∧ in-flight 空 | `verdict=green` + raw_message 非空 + `path_coverage` 在场 + **`query_pr_ci.assert_not_called()`** |
| SC-11 | covered / unknown | 既有字段逐字段回归 (断言口径=既有六键; 既有 62 tests 全绿) |
| SC-12 | config 无 `path_coverage_enabled` | 评估执行 (默认 true 锁定) |
| SC-13 | `path_coverage_enabled: false` | 评估不执行, 输出无 `path_coverage` 键, 现行为 |
| SC-14 | glob 表驱动: `**` / 尾 `/**` / `*` 单段 / `?` / **字符类 `[abc]` → 判匹配** / **`!` 前缀 → 判匹配** / **大小写不匹配用例** | 期望值来源标注 forgejo 官方 paths 文档 |
| SC-15 | Output schema | 老键全保留 (additive-only); 早退分支不带 `path_coverage` 键 |
| SC-16 | PR 仅修改 workflow 文件自身 (真实语料: `.forgejo/workflows/issue-triage-tests.yml`) | `covered`, reason=`workflow-files-changed` |
| SC-17 | push 无 paths + pull_request 有 paths (及反向) | OR 语义: 任一触发即 covered |
| SC-18 | 文件从覆盖路径 rename 移出 / 移入 (`--no-renames` 下) | 新旧路径都进 changed_files → covered |
| SC-19 | 主仓语境 gitlink-only bump (changed_files=[`aria`]) + 主仓 3-workflow 真实语料 | **`not_applicable`, reason=`no-triggering-paths`, matched_workflows=[]** (gitlink 单 token 对主仓 workflow 的 `aria/skills/issue-triage/**` 与 `aria-orchestrator/docker/aria-runner/**` 均不命中, CR-N-4 勘正语料归属; QA-10 钉死终态; 补充正证 fixture: 合成 paths 含 `aria` 精确 token 的 workflow → `covered`, 验证 gitlink 按不透明单段路径参与匹配不展开) |
| SC-20 | 块映射形 + paths 子块 (本仓语料全部形态), 双子用例 (QA-9-residual 具体化) | (a) changed_files 命中 paths → `covered`, reason=`workflow-trigger-matched`; (b) 不命中 (单 workflow 语料) → `not_applicable`, reason=`no-triggering-paths` |
| SC-21 | not_applicable ∧ stub backend (query 抛 NIE) | gate 仍 raise NIE ((b) 无条件先跑, 不被 not_applicable 吞) |
| SC-22 | 既有 GateCheckTests/FallbackTests 套件运行 | 零真实 git 子进程 (评估器入口被 mock, 卫生断言) |
| SC-23 | 主仓 3 workflow 联合语料 (branches+paths / dispatch+push 混合 / 纯 dispatch) + 变更 `docs/x.md` | `not_applicable`, reason=`no-triggering-paths`; 同语料 + 变更 `aria-orchestrator/docker/aria-runner/Dockerfile` → `covered`, reason=`workflow-trigger-matched` (QA-5, D5 语料承诺兑现) |
| SC-24 | 一 workflow covered ∧ 另一 workflow 解析失败 (混合) | 整体 `covered`, reason=`workflow-trigger-matched` (规则 6 优先级, BA-4) |
| SC-25 (**A3 回填** — R6/M-3) | 仅 `pull_request_target` 触发的 workflow (手造 fixture, 须**无真实 paths 匹配**) + 任意变更 | 该 workflow `covered` (未建模自动触发键白名单方向, R2-C1) ∧ **reason == `workflow-construct-uncertain`** ∧ **`uncertain_workflows` 含该 workflow** (与 SC-6 同因: 未建模触发键是另一个高频 6b 成因) |
| SC-26 | 在主仓根对子模块分支名评估 (该 ref 不存在于主仓) | `unknown`, reason=`git-diff-failed` (BA-2 残留负向用例: cwd 错仓的自然安全网) |
| SC-27 | cwd 位于仓内子目录 | 仍以 `git rev-parse --show-toplevel` 定仓根扫描 workflows (D11 机制锁定) |
| SC-28 | diff 成功但输出为空 (changed_files=[]) | `covered`, reason=`empty-diff` (规则 2 覆盖行, QA-14 — 封闭集与测试矩阵满射) |
| **SC-29** (A1/L-4, A2 重写, **A3 修 (d)** — R6/M-8+m-4) | `-z` 各义务独立可红。**(a) `-z` 本身**: fixture 仓显式 `git config core.quotePath true`; 变更集**唯一**元素是非 ASCII 路径 `skills/测试/x.py`, 且它是唯一命中 workflow `paths` 的文件 → **`covered`**。**(b) 尾随 NUL / 滤空串**: 非空 diff (**恰 3 个文件**) → `changed_files_count == 3` 且列表无空串。**(c) 空 diff**: 空输出 → 落规则 2 `covered`/`empty-diff`。**(d) 解码 (A3 钉死终态)**: 路径含非 UTF-8 字节序列且**该路径是唯一命中项** → 断言 `decision == "covered"` ∧ `reason == "workflow-trigger-matched"` ∧ reason **不以** `git-diff-failed`/`internal-error` 开头 | (a) 红窗依赖 **quotePath=true 已显式设** + **唯一匹配项**锁定。**(d) 的 A2 版恒绿 (R6/M-8)**: 原断言「不抛异常, `decision` 有效」—— `text=True` 实现抛 `UnicodeDecodeError` 后被**全捕获**接住返回 `unknown`, 两个条件全部满足 ⇒ 要抓的实现全绿。**(b) 的红窗仅对「两步皆缺」成立 (A3/m-4 如实标注)**, 见下方 D14 说明 |
| **SC-30** (A1/L-3, A2 重写, **A3 增 5 子用例** — R6 两条 CRITICAL) | 位置 ∧ 形态判据各段独立可红。**正控** (均须 `uncertain_workflows` 含该文件 ∧ reason==`workflow-construct-uncertain`, 且该 workflow **无任何真实 paths 匹配**以免被 6a 掩盖): (i) `push: &push_cfg` 同行锚点; (ii) `- *alias` 块序列项; (iii) `<<: *base` 合并键; (iv) `tags: !!str foo`; **(xii) `paths: *common_paths`** ← **A2 在此误放行 (C-2), 必红**; **(xiii) `- *p` 在 `paths:` 子块** ← 同 C-2; **(xiv) `paths:` 后无任何值域内 `- ` 项 (真空值)** ← (2c) 兜底。**负控** (均须**不**触发): (v) token 只在 `run: \|` 块体; (vi) token 只在注释里; (vii) **`- '**.js'` 在 `paths:` 子块 (缩进 6)** ← A1 的 CRITICAL 在此必红; (viii) `paths: ['*.py', '!docs/**']` flow list 同行; (ix) `on:` 块**之外**的 `&anchor`; **(x) `    paths:` + 同缩进 `    - '**.js'`** ← **A2 的 C-1 在此必红**; **(xi) paths 列表中夹一个列 0 注释行后再跟 `- '**.js'`** ← C-1 同源第二缺口; **(xv) `paths:` 后跟正常缩进块序列** ← **A3 自查拦下的第四次复发在此必红** (若把「同行为空」误读成真空值, (2c) 会让每个正常块序列 paths 都判构造级 ⇒ 恒 wait) | (vii)(viii) 抓 A1; **(x)(xi) 抓 A2 的 C-1**; **(xii)(xiii) 抓 A2 的 C-2**; **(xv) 抓 A3 自己**; (i) 抓 C2; (ix) 抓 C3 |
| **SC-33** (A3/M-2, 新增) | **6a 路径的 `uncertain_workflows` 红窗**: 双 workflow 混合语料 —— W1 的 `paths` **真实命中**变更, W2 含 `&anchor` (构造级) ⇒ 断言 `reason == "workflow-trigger-matched"` ∧ `matched_workflows == [W1]` ∧ **`uncertain_workflows == [W2]`** | **缺一即红**。A2 的全部 SC 都活在 6b 或空集 (SC-30 正控显式要求「无真实匹配」、SC-31(a) 断言 `== []`) ⇒ **一个只在 6b 填、6a 恒填 `[]` 的实现能通过 A2 的全部 SC** (R6/M-2) |
| **SC-34** (A3/M-1, 新增) | **「永不 raise」的唯一红窗**: `mock.patch` 令内部某函数 (如值域归属计算) 抛 `RuntimeError` ⇒ 断言 (a) **不向调用方抛出**; (b) `decision == "unknown"`; (c) `reason.startswith("internal-error")` — **不得**是 `git-diff-failed` / `workflow-parse-failed` | A2 之前「永不 raise」承诺**零 SC 验证**; 且无 `internal-error` 槽时实现只能冒用他人 reason ⇒ (c) 必红 (R6/M-1) |
| **SC-31** (A1/L-2, **A2 重写** — R5/C4+M1) | `---` 语义四个边界各自可红。**(a)** **首行** `---` + `paths` 命中变更 → `covered` ∧ reason==**`workflow-trigger-matched`** ∧ `uncertain_workflows == []`; **(b)** `---` 在首个内容行**之后** → `covered` ∧ reason==**`workflow-construct-uncertain`** ∧ `uncertain_workflows` 含该文件; **(c)** **连续两个** `---` (首个前无内容行) → 按 (b) 判 (第二个命中); **(d)** `%YAML 1.2` + 紧随 `---` → 按 (a) 判 (指令后首个 `---` 豁免); **(e)** 形态负控 `--- foo` / `----` / 缩进 `  ---` → **均不参与**判定 | **(a) 的红窗靠 A2 的 reason 二分才成立** — A1 下两种实现输出逐字节相同 (规则 6 折叠), 该 SC 恒真 (R5 qa CRITICAL) |
| **SC-32** (A1/L-5, **A2 收窄** — R5/C5) | **只保留可机械断言的第 3 条**: 读 `aria-plugin-benchmarks/ab-results/2026-05-10-phase-c-integrator-pre-merge-gate/benchmark.json`, 断言既有 **8 个** `structural_metrics.*.measured` 的 `type(...) is int` 且值为 `100`, 并断言 `primary_pass_gate.measured` 是 `str`。落点 `aria/skills/phase-c-integrator/tests/` (**在 `run_all_tests.sh` 的 `SKILLS_DIR="skills"` 扫描域内**) | A1 的前两条断言 (套件解析 / 基线选取) **无可计算主体** — 测的是 AI 执行期 judgment, 仓内无对应代码 ⇒ 恒真; 且原落点 `aria-plugin-benchmarks/` 结构上永不被执行。两条已移入执行手册约束 (见 rule6_note 分层表) |

---

## 非目标

- **不动 `no_ci_fallback` 政策** (`_open_question_no_ci_fallback` 归 owner, 正交);
- 不实现 GitHub Actions backend 真查询 (stub 现状不变);
- 不建模 `branches` 过滤 (conservative 方向已论证, 语料正例锁定);
- 不消除 gate→merge race window (SKILL.md :291 现状声明不变);
- 不动 workflow-runner `wait_recoverable` 机制本身 (not_applicable 在 gate 内消化, 不产生 wait)。

---

## Impact

| 文件 | 变更 |
|------|------|
| `skills/phase-c-integrator/scripts/path_coverage.py` | **新增** (评估器; §0 契约 + §1 全分割判定) |
| `skills/phase-c-integrator/scripts/pre_merge_gate.py` | `gate_check` 插评估点 + docstring 更新 (BA-7) / `compute_verdict` 显式分支 (BA-8) / `_build_output` 增可选参数 (BA-6) / `DEFAULT_CONFIG` 增键 |
| `skills/phase-c-integrator/tests/test_path_coverage.py` | **新增** (SC-1~8, 14, 16~20, 23~28, **29~32**; fixture 用**独立 tempdir**非 repo.parent, QA-13 — **先例在代码不在 memory** (A2/M3 订正): `aria/skills/state-scanner/tests/test_handoff_worktrees.py:9,36` + `test_git_operation_detection.py:92`, 引「#135 `$TMPDIR`-leak lesson」。**前提成文** (A2/minor): 该 tempdir 须 `git init` + 造两个分支, 否则 `git diff` 落 `git-diff-failed` 使 SC-29~31 全部在错误分支上求值) |
| `skills/phase-c-integrator/tests/test_pre_merge_gate.py` | 扩展 (SC-9~13, 15, 21~22) |
| `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` | **执行手册约束** (A2/C5): AB 执行面三处勘正中**不可机械断言**的两条 (套件解析 / 基线选取) 移入手册 + TASK 级 checklist, 不冒充 SC |
| `skills/phase-c-integrator/SKILL.md` | §6 清单逐处 (含 :39-53 总览表 + :176 紧凑块) → Rule #6 照跑 AB |
| `aria/skills/config-loader/SKILL.md` | :241-281 登记 `path_coverage_enabled` (KM-1) |
| `aria/skills/workflow-runner/references/workflow-state-schema.md` | :125 `raw_message` 用途补注 (KM-10) |
| 发版 5 文件 + 主仓 gitlink | v1.65.0 MINOR |
| 主仓 `docs/decisions/DEC-*` | **新增** 2026-07-25 裁决存档 (KM-5, 先于 `_lane` 改写) |
| 主仓 `.aria/config.json` | `_comment`/`_lane`/`_not_ci_backends_empty` 三字段退役改写, **与 gitlink bump 同 commit co-land** (TL-5/KM-6) |

**测试基线 (A2 订正 — R5/minor: 原「~110+」在全部 13 份 R1-R4 报告中零命中, 无核算依据)**: 起点 **phase-c 62 tests (实测)**。本 change 新增测试**按 SC 子用例数下界核算**, 不再给未经核算的总数:

| 来源 | 子用例数 (下界) |
|------|---------------|
| SC-1~28 (R1-R4 既有) | 未逐条核算 — 沿用「每 SC ≥1」⇒ **≥28** |
| SC-29 (a/b/c/d) | 4 |
| SC-30 (i~xv, **A3 增 5**) | 15 |
| SC-31 (a~e) | 5 |
| SC-33 (A3/M-2 新增) | 1 |
| SC-34 (A3/M-1 新增) | 1 |
| SC-6 / SC-25 回填 (A3/M-3) | 0 (加强既有断言, 不增条数) |
| **A1+A2+A3 小计** | **26** |

⇒ 下界 62 + 28 + 26 = **≥116**, 上界不预测 (Phase B 实测后回填)。**口径澄清 (A3 修)**: 该数字**仅含 `aria/skills/phase-c-integrator/tests/`** 域 —— `run_all_tests.sh` 硬编码 `SKILLS_DIR="skills"`, 结构上不扫 `aria-plugin-benchmarks/`。**SC-32 不计入本表** —— A3 已把它移到**主仓侧**发版门禁 (D16), 与 aria 子模块的测试套件分属两仓, 混算是 A1/A2 两版都犯过的口径错误。全量跨 skill 套件须绿 (`run_all_tests.sh`)。

---

## 修订记录

### A1 (2026-07-30) — 双 Spec 碰撞归并, 并入 L 的实跑发现

**背景**: 并发轨 `aria-runner-bot/023236f2` 与本轨 `simonfishgit` 同治 aria-plugin #122, 各自跑满 4 轮 post_spec (合计 10 轮 / 33+ agent), 互不知情。owner 2026-07-30 裁定**以本 Spec 为基线**并入 L 的发现。

**并入 (3 真缺口 + 1 欠定)**:

| 条目 | 性质 | 落点 | L 侧证据 |
|------|------|------|---------|
| L-4 `-z` + 尾随 NUL | **真缺口** — 本 Spec 原用 `--name-only --no-renames` 无 `-z`, 非 ASCII 路径被 `core.quotePath` 八进制转义 ⇒ 恒不匹配 ⇒ 假 not_applicable | §0 新 bullet + §1 命令行 + D14 + SC-29 | R2 实测尾随 NUL |
| L-2 `---` 语义 | **真缺口** — 本 Spec 全文未提 `---`, 实现者只能归入「其他构造级不确定」→ covered ⇒ 首行 `---` 的仓恒 wait | §1 新 bullet + D13 + SC-31 | R4 实跑 |
| L-5 AB 三处勘正 | **真缺口** — 本 Spec 点了套件文件名, 未涉基线路径与 metric 类型 | rule6_note 新表 + SC-32 | R2 **5/5 席实地核实** |
| L-3 位置式 anchor 判据 | **欠定** — 本 Spec 只写「anchors → covered」未定命中判据; SC-2 有间接兜底, 但承重算法须钉到字符级 | §1 新 bullet + D12 + SC-30 (含三条负控) | R4 实跑 3/4 语料命中 |

**未并入 (经逐条核实, 本 Spec 已用别的方式解决同一问题)**:

- **L-6 `_match_coverage` 纯函数拆分** — L 用它规避「fixture 在 Aria 仓内致 `git -C` 成功并返回 Aria 自己的 changed files」。本 Spec 的 Impact 表已声明 **fixture 用独立 tempdir 非 repo.parent** (QA-13), 同一问题的另一解。不引入双层结构。
  > **⚠️ A2/M3 引用订正**: A1 此处 (与 Impact 表) 引 memory `feedback_test_worktree_fixture_isolated_tmpdir` 作为该做法的先例依据。**该 memory 不存在** —— R5 knowledge-manager 与主控独立核实, `/home/dev/.claude/projects/-home-dev-Aria/memory/` 下文件名与内容**双零命中**。该引用系沿用本 Spec `:224` (R1-R4 期即有) 并在 A1 被**用于论证本决策**, 属继承并放大失实引用。**真实先例在代码不在 memory**: `aria/skills/state-scanner/tests/test_handoff_worktrees.py:9,36` + `test_git_operation_detection.py:92`, 引「#135 `$TMPDIR`-leak lesson」issue。**拒并 L-6 的结论不变** (替代解确实存在且方向正确), 但依据已换成可核实的那个; 且替代解的**前提** (tempdir 须 `git init` + 造两分支) A1 未成文, A2 已补进 Impact 表。
- **L-7 `paths-ignore` 极性反转 (P5)** — L 的 R2 发现「从 `paths-ignore` 推导不覆盖」会使 `match` 落否定位致极性反转。本 Spec §1 原文即「`paths-ignore` 在场 → 该 workflow `covered`」(**根本不推导不覆盖**), 与 L 的 R2-fix 同结论。无需变更。

**正交项 (不属本 Spec, 建议独立处置)**:

- **L-1 `compute_verdict` catch-all `else → GREEN` 的 fail-OPEN** — L 侧实跑 3/3: `compute_verdict([], "not_found")` / `([], "wat")` / `([], "")` 在 v1.64.0 上**全返回 `green`**。对本 Spec 而言该 catch-all **仍不可达** (本 Spec 不改 backend, `not_found` 不上岗), 故**非本 change 引入、也不阻塞本 change**。但它是既有 latent 缺陷, 建议开独立 issue + 小 PR 单修 (baseline-failing 测试: 上述三条在 v1.64.1 上应为红)。**已列入 §Follow-up, 不并入本 Spec 范围。**

---

### A2 (2026-07-30) — post_spec R5 定向轮 fix

**输入**: owner 裁定的 **R5 定向轮** (范围锁 A1 新增 4 处; 席位不降, config `teams.post_spec` 全 5 席)。结果 **5/5 REVISE**, `scope_ok` 5/5 true, **6 个 critical 簇全部落在 A1 新增范围内**。聚合报告 `.aria/audit-reports/post_spec-R5-1785377400000-phase-c-gate-path-coverage-aggregated.md`。

**吸收情况 (全量, 无 deferred)**:

| 簇 | 席位 | 处置 |
|---|------|------|
| **C1** D12 剥引号致 leading-`*` glob 误判 ⇒ 恒 wait 原样复发 | 3 席 + 主控自验 | D12 全面重写 — 新增**值位互斥**段 (最高优先); SC-30 负控 (vii)(viii) 改用首字符为 `*`/`!` 的 pattern |
| **C2** D12 缺键值拆分 ⇒ `push: &push_cfg` 漏判 | BA (跨席欠定实锤) | D12 第 (3) 段 + 逐例判定表 8 行; SC-30 正控 (i) |
| **C3** D12「区间」无定义 (搬运丢失 L:182 作用域子句) | CR + 主控自验 | D12 第 (1) 段就地定义区间起止; SC-30 (ix) 作用域边界红窗 |
| **C4** reason 封闭集缺构造级槽位 ⇒ SC-30 正控/SC-31(a) 双双恒真 | QA + CR | 规则 6 拆 **6a/6b** + 封闭集增第 8 槽 `workflow-construct-uncertain` + 返回契约增 `uncertain_workflows[]` + surface 义务扩至三条 (**新 D15**) |
| **C5** SC-32 前两条无可计算主体 + 落点永不执行 | QA + CR + TL | rule6_note 增**可机械化程度分层表**; SC-32 收窄至第 3 条并移回 skills 域; 前两条降为执行手册约束 |
| **C6** 勘正 1 排除 parent 套件 ⇒ AB 失去双臂对象 | TL | 勘正 1 **方向订正**: 两个套件都跑 (parent = 唯一有 LLM evals, 测指令面; -pre-merge-gate = structural fixtures) |
| **M1** D13 区间 +「内容行」四分叉未定义 | BA + CR | D13 补全文件区间声明 + 四个边界逐条封闭; SC-31 五子用例 |
| **M2** SC-29(a) 红窗不成立 | QA + CR | SC-29 重写: 显式 `core.quotePath=true` + 锁唯一匹配项 + 断言计数 |
| **M3** 引用不存在的 memory | KM + 主控自验 | 两处引用删除, 换真实代码先例 (`test_handoff_worktrees.py:9,36` + #135) + 补替代解前提 |
| **M4** AB 勘正表来源归因失实 | KM | 表头拆分归因 (第 1/2 项 post_spec-R2 5/5; 第 3 项 post_planning-R2 单席) |
| **M5** `:3` Status 行未随 A1 更新 | TL | Status 改 `Draft (A2, post_spec R5-fix)` + 显式 **⛔ 不 ready for Phase B** |
| **M6** D12 与 glob 条款 `!` 前缀所有权重叠 | TL | D12 第 (2) 段末显式划分所有权 (值位内归 glob matcher / 值位外归 D12), 声明互斥无重叠 |
| Minor ×7 | 各席 | 全部吸收: 测试基线改**按子用例下界核算**并澄清口径 · `:47` gitlink 条款同步 `-z` · rstrip 与滤空串**各治一病**说明 + SC-29(b) 断言计数 · D14 增解码契约 · 独立 tempdir 前提成文 · 勘正 2 理据订正 (最近归档实为 `2026-07-20-v1.62.0-phase4-rule6`) · `:62` anchors 与 D12 建立引用关系 |

**未吸收**: 无。

**R5 已实测确认无需改动的部分** (下轮免重复): D14 三条技术前提 · AB 三处勘正的事实内核 (含 8/8 metric 为 `int 100`) · L-7 拒并判断 · reason 封闭集与规则互斥穷尽性 (A2 加槽后仍成立) · D13「列 0」限定词已避开 L 侧 R3 的 `echo "--- image size ---"` 坑 · ~~§6 SKILL.md 同步清单不需为 A1/A2 扩项~~。

> **⚠️ A3/M-7 订正上面最后一项**: 该结论是 R5 对 **A1** 的实测结论, A2 把它**原样外推到了 A2 自己** —— 而 A2 恰恰新增了第三条 surface 义务 (D15)。R6 指认: §6 的逐处点名清单 (Phase B 真正照着改的那张表) 仍只写 D8/D9, 且实读 SKILL.md `:236-262` 发现 **covered 路径当前无任何 surface 通道** ⇒ D15 不点名等于不存在。A3 已在 §6 补 D15 并注明需新建通道。**教训: 「上一轮说不用改」的结论只对上一轮审过的版本成立, 不能随修订版本顺延。**

**⚠️ A2 引入的新表面 (供下轮重点看)**: 值位互斥 (D12-2) 是本轮最大的新机制 —— 它把「构造扫描」与「pattern 值域」定义成互斥两域, 判定正确性依赖**缩进块归属计算**的准确性 (`paths:` 键的子块边界)。该计算此前不存在于任何条款, 是 A2 新引入的承重逻辑。

**元教训**: 三条最严重的缺陷 (C1/C3/M3) **全部产生于「搬运」本身**, 而非原发现有问题 —— 已实证的发现换语境后, 其前提子句 / 执行顺序 / 依赖引用都可能不再成立。memory `feedback_fix_recurs_in_its_own_fallback_path` 的新 locus: **移植修复这个动作**。C1 尤其典型: 并入 L-3 的全部目的是防「恒 wait 复发」, 而 A1 在自己新写的剥引号步骤上原样复发了同一个病; 且 SC-30 的负控例子从 L 逐字照搬, **把 L 的盲区一起抄了进来**。

---

### A3 (2026-07-31) — post_spec R6-fix (新鲜眼睛轮)

**输入**: owner 裁定「再跑一轮, 派一席没参与 R5 的新眼睛」。R5 已用满 config `teams.post_spec` 全部 5 类型 ⇒「没参与」结构上必须走出配置团队, 选 `pr-review-toolkit:silent-failure-hunter` (专攻静默失败 / 兜底吞信息, 与本 Spec 满篇 fail-toward-covered 正面对口)。结果 **REVISE, critical=2 major=8 minor=7 (+3 OUT_OF_SCOPE)**。聚合报告 `.aria/audit-reports/post_spec-R6-1785380000000-*-aggregated.md`。

**C-2 的修法方向由 owner 明确裁定**: 采用「**位置 ∧ 形态**」判据。

**吸收情况 (全量, 无 deferred)**:

| 簇 | 处置 |
|---|---|
| **C-1** 值域归属未成文 ⇒ 恒 wait **第三次**复发 | (2a) 重写: 序列项归属改 `≥` (YAML 允许同缩进块序列) + 定义值域终点 + 空行注释不终止 (一字不差重述, 不写「参见 (1)」)。SC-30 增负控 (x)(xi) |
| **C-2** 无条件排除 ⇒ 真 alias 被当 pattern ⇒ **第一个 fail-OPEN** | (2b) 新增形态维度 (带引号判 pattern / 裸且首字符 `*&!` 判构造级) + (2c) 值形态兜底 (非 block/flow list ⇒ 构造级不确定)。SC-30 增正控 (xii)(xiii)(xiv) |
| **M-1** 全捕获无 reason 槽 | 封闭集增第 9 槽 `internal-error`; D9 surface 扩枚举 + 文案点明「评估器自身异常」; **新增 SC-34** —「永不 raise」此前零 SC 验证 |
| **M-2** 6a 路径无红窗 + 文案事实错误 | **新增 SC-33** (混合语料, 缺一即红); surface 文案按 6a/6b **二分** |
| **M-3** 二分未回填 SC-6 / SC-25 | 两条既有 SC 期望列加 reason + `uncertain_workflows`; 满射口径改**按规则分支计** |
| **M-4+M-5** SC-32 跨仓 + 守错对象 | **新 D16**: 落主仓侧 + 断言**本次新产出**的 benchmark.json + **文件缺失 = FAIL, 禁 `skipIf`**; 从测试基线口径中剔除 |
| **M-6** LLM eval 臂无对照 | 勘正 2 分列两臂; 若确认无历史归档则**必须显式声明「本次无 A 臂, 结论只覆盖 structural 臂」** |
| **M-7** §6 未点名 D15 | `:199` 改 D8/D9/D15 三条并注明 **covered 路径当前无 surface 通道, 需新建**; 删去 A2 那句把 R5 对 A1 的结论外推到 A2 的话 |
| **M-8** SC-29(d) 恒绿 | (d) 改为钉死终态 (`covered` + 精确 reason + 排除 `internal-error`) |
| **minor ×7** | m-1 键值拆分提为 (0) 消除自指 · m-2 「列 0」提进必要条件 · m-3「紧随」= 跳过空行注释后 · **m-4 如实订正: rstrip 无独立红窗**, 删「各治一病」的失实声称 · **m-5 主控自犯: `:67` 补 D12 引用 + 6b 归属** (A2 吸收表声称已做而实际未落地, 行号也写错) · m-6 短路路径须合取 `workflows_scanned > 0` · m-7 新建模 `...` |

**未吸收**: 无。

**⚠️ A3 自查拦下的第四次同形复发**: 起草 (2c) 时初版写「值为**空值** ⇒ 构造级不确定」。自查发现 —— `paths:` 键行同行为空、其后跟缩进块序列, **那是 block list 不是空值**; 按初版每一个**正常的块序列 `paths:`** 都会落 (2c) ⇒ 全判构造级 ⇒ 恒 covered ⇒ **恒 wait**, 即同一条失败链的第四个入口。已改为按**解析后取值**判定并给出四分支表, 且**新增 SC-30 负控 (xv) 专抓这个** (`paths:` + 正常缩进块序列 ⇒ 必不触发)。

**R6 已实测确认无需改动的部分** (下轮免重复): C4 的 reason 二分确实救活 SC-30 正控与 SC-31(a) 两个红窗 (**A2 最有价值的一处修复**) · C2 键值拆分 8 行判定表逐行走查无新漏判 · C3 区间定义起止完整 · M3 代码先例引用实读属实 · M5 Status 行实跑验证机读层返 `pending` · 勘正 3 事实内核 (8 metric 全 `int 100`) · §6 行号锚点抽验准确 (缺的是 D15 点名非锚点漂移)。

**⚠️ A3 引入的新表面 (供下轮重点看)**:
1. **(2b) 形态维度**依赖「带成对引号」的判定 —— 这是 A3 新引入的承重逻辑, **未经任何席位审过**。边界: 转义引号 / 单双混用 / 引号内含引号。
2. **(2c) 的「解析后取值」四分支**需要向后看值域内是否存在 `- ` 项 —— 与 (2a) 的值域计算**互相依赖**, 存在循环定义风险。
3. `internal-error` 槽使封闭集 8→9, **满射矩阵需重核**。

**元教训 (本轮新增)**: R6 席位的贯穿判断 ——「八条 major 里五条是同一形状: **义务写了、槽位留了、红窗没有**」。A2 在「把事实记下来」上做得好, 在「让记错时会红」上系统性欠一步。这与 memory `feedback_falsifiable_evidence_for_binary_acceptance` 同源, 但落点更细: **不是「有没有验收标准」, 而是「那条验收标准存在一个会让它变红的实现吗」**。A3 对每条新义务都补了红窗 (SC-33/SC-34 + SC-6/25 回填), 并对**证不了的**如实标注 (m-4 的 rstrip)。

---

## ⚠️ 闸门待裁 (Rule #10 — AI 不自行判定)

A1 是**实质 Spec 变更** (新增 D12/D13/D14 三条决策 + SC-29~32 四条验收 + 改一条 git 命令), 不是文字勘误。`.aria/config.json` 的 `audit.checkpoints.post_spec = "convergence"` 处于 **enabled** 状态, 且该文件 `_comment` 逐字重申「AI 不得自行豁免已 enabled 的 checkpoint」, 封闭豁免白名单四类 (config 显式 off / adaptive_rules / 已成文 lane / 结构性前提不成立) **无一适用**:

- 非 config off (post_spec = convergence);
- 无对应 adaptive_rules 映射;
- 无成文 lane 覆盖「Spec 修订后是否重跑」;
- 结构性前提**成立** (审的对象 = 修订后的 proposal, 确实已产生)。

⇒ **默认应重跑 post_spec**。同时存在一个正交约束: 本 session 的硬约束「未经用户要求不得调用 Agent」与闸门执行相撞 (与 2026-07-27 session 同一形状, 见该 handoff §9)。**两者均须 owner 显式裁, AI 不以任一方为由跳过另一方。**

**执行史**: owner 2026-07-30 裁定 **(2) 定向轮** → R5 (5 席, 5/5 REVISE, 6 critical) → **A2 = R5-fix, 全量吸收** → owner 裁定「再跑一轮 + 派新眼睛」→ R6 (1 席团队外, REVISE, 2 critical + 8 major + 7 minor) → owner 裁定「跑 R6-fix, C-2 用位置 ∧ 形态」→ **A3 = R6-fix, 全量吸收** (见 §修订记录 A3)。

**轮次趋势 (同口径不可比, 如实标注)**:

| 轮 | 席位 | critical | major | 性质 |
|---|---|---|---|---|
| R5 | 5 (config 全员) | 6 | 6 | 审 A1 |
| R6 | 1 (团队外新眼睛) | 2 | 8 | 审 A2 |

**读法**: 席位 5→1 使绝对数不可比。critical 6→2 是降; major 在五分之一席位下升, 是**换视角带来的新覆盖面** (「红窗存在性」这一类前五席系统性漏掉), 非「加轮收不敛」(memory `feedback_stop_adding_rounds_when_major_count_flattens` 的判据是**同口径**下 major 是否还在降)。

**当前待裁**: A3 之后是否再跑一轮?

- **A3 引入三处新表面且全未经审** (形态判定的引号边界 / (2c) 与 (2a) 的互相依赖 / 封闭集 8→9 后的满射矩阵) —— 见 §修订记录 A3。其中 (2b) 是 owner 裁定方向后**由主控起草**的承重判据, 无第三方看过。
- **A3 自查在起草中拦下了第四次同形复发** —— 说明这条失败链在每一版都在找新入口, 自查能拦一次不代表能拦下一次。
- **修法提出方与审查方的分离**: (2b)(2c) 的方向由 R6 席位提出、owner 裁定, 具体条款由主控写。若再跑, 建议**既非 R6 席位、也非 R5 五席**的第三方眼睛。

- **判据参考** memory `feedback_stop_adding_rounds_when_major_count_flattens`: 加轮判据是 **major 数是否还在降**, 非 critical 归零。A1→A2 是这条修订线的**第一次** fix, critical 6→? 尚无第二个数据点 ⇒ **不属于「加轮收不敛」形态**, 再跑一轮是正常收敛过程。
- **另一判据** memory `feedback_premerge_iteration_pattern`: 首个 0-finding 轮不能直接声称收敛, 需稳定性确认轮。
- **A2 引入了新承重逻辑** (值位互斥的缩进块归属计算), 该逻辑此前不存在于任何条款、未经任何席位审过 ⇒ 若免跑, 它将带着零审计记录进 Phase B。
- **换新鲜眼睛 > 加轮** (同 memory): 若跑, 建议至少一席**未参与 R5** 的新眼睛 (R5 五席已看过 A1 的错误版本, 存在锚定风险)。

**AI 不预判裁决**。owner 可选: (1) 再跑一轮 (定范围/席数, 建议含新眼睛); (2) 判定 A2 已足并接受, 留痕请复议; (3) 只定向审 A2 新引入的值位互斥一处。**本 Spec 在裁决前不进 A.2/A.3。**

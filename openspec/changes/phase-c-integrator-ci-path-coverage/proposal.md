# Proposal: phase-c-integrator-ci-path-coverage (aria-plugin #122)

> **Status**: 📝 **Draft (R4-fix)** — post_spec 收敛轨迹 R1 [4×FAIL+1×PWW, 5 critical] → R2 [4×FAIL+1×PWW, 4 critical] → R3 [1×FAIL+2×PWW, 1 critical] → **R4 [1×FAIL+1×PWW, 0 critical 共识 —— 两席对同一 finding 判 critical vs major, 分歧点是「后果是假绿」vs「被 4 条既有 AC 机械兜住、无法静默 ship」]** → R4-fix。`max_rounds=4` 耗尽 ⇒ 降级策略 **owner 2026-07-26 裁定 [1] 接受当前结论** ⇒ `converged: false, overridden_by_user: true`, 进 A.2。审计轨迹全文见 `.aria/audit-reports/post_spec-R{1,2,3,4}-*-aggregated.md`
> **Created**: 2026-07-25
> **Spec Level**: 2 (单域 — C.2.4 gate 的 PR-CI 状态判定链路)
> **关联 Issue**: [10CG/aria-plugin #122](https://forgejo.10cg.pub/10CG/aria-plugin/issues/122) (open, 0 评论, 无 in-flight — 本地 fetch + Forgejo API 双核实)
> **Owner 授权**: owner 定案 2026-07-25 (主仓 `194a73b` + `.aria/config.json` `phase_c_integrator._lane`): 「#122 优先落地是唯一真机制」
> **⚠️ 需 owner 单独裁的条目**: §7 将改写 **CLAUDE.md 规则 #8 判据本体** 与 `_lane` — Rule #10 权限面, **拆独立 commit, 不随实现 PR 合并** (R2 backend-architect 要求)
> **代码落点**: `aria/` 子模块; Spec 落主仓 `openspec/changes/`
> **ship target**: aria-plugin v1.65.0 (MINOR)
> **Rule #6**: ✅ 照跑 AB, 零裁量。**不申请豁免**。判据见 AC-9 (R2 5/5 命中原判据引用了不存在的字段, 已重写)

---

## Why

### 症状

Rule #8 的 C.2.4 pre-merge gate 对**路径过滤型 CI** 结构性恒 `wait`。已重复 **4 次** (v1.54.0 / v1.55.0 / v1.55.2 / v1.64.0#113)。owner 2026-07-25 复议认定这 4 次「不是先例 lane, 是 4 次错过机制化」, 把 `verdict=wait` 当 skip 属 **Rule #10 反模式**。

### 根因链路 (实测)

```
AetherBackend._normalize_pr_ci_status([])   aether.py:223-224  → "pending"
  ↓ query_pr_ci → CIStatus(state="pending")  aether.py:109-115
  ↓ gate_check                               pre_merge_gate.py:330-341
  ↓ compute_verdict: == "pending"            pre_merge_gate.py:187-188  → VERDICT_WAIT
  → workflow-runner 指数退避至 1800s
```

**信息塌缩点 `aether.py:223`**: 「CI 还没跑完」与「CI 永远不会为这些路径跑」折叠成同一个 `"pending"`。

「假绿的反面是恒红, 同样零信息量」—— 永远返回 `wait` 的闸门会被学会忽略。

### Probe: 真实 workflow 语料 (4 份, 实读)

| 文件 | 仓 | PR 相关触发 | paths | branches |
|------|----|-------------|-------|----------|
| `aria/.forgejo/workflows/issue-triage-tests.yml` | aria | `push`+`pull_request` (+`workflow_dispatch: {}`) | `'skills/issue-triage/**'` | 无 |
| `.forgejo/workflows/issue-triage-tests.yml` | 主仓 | `push`+`pull_request` (+`workflow_dispatch: {}`) | `'aria/skills/issue-triage/**'` | push: `[master, 'feature/aria-issue-triage-sop']` |
| `.forgejo/workflows/build-aria-runner.yaml` | 主仓 | **仅 `push`** (+`workflow_dispatch` 带 3 层嵌套 `inputs`) | `'aria-orchestrator/docker/aria-runner/**'` | push: `[feature/aria-2.0-m0-prerequisite]` |
| `.forgejo/workflows/submodule-gate-tripwire.yml` | 主仓 | **仅 `workflow_dispatch`** (文件头自述 DEPRECATED) | — | — |

两仓均无 `.github/workflows/` 与 `.gitea/workflows/`。**全部 pattern 带单引号**; **零 `paths-ignore`**; **4/4 裸 `on:`**。`build-aria-runner.yaml` 的 `on:` 下是 3 层嵌套 `inputs` + **空行**, 之后才是 `push:`。

### 审计增量事实

1. `CIStatus.state` 的 `Literal` 已含 `"not_found"` (`base.py:29`) 但零生产者。
2. `compute_verdict` 的 catch-all 是 `else → VERDICT_GREEN` (`:192-194`)。**R1/R2 两席独立实跑**: `compute_verdict([], "not_found")` / `([], "totally_bogus")` / `([], "")` 全返回 `green`。改前该 catch-all 不可达; 本 change 让 `not_found` 上岗即把它**从不可达变可达**。
3. `compute_verdict` 返回 **dict** (v1.31.0+), 不是 str。

---

## What Changes

**核心原则 P1-P5** (P5 经 R2 修正):

| 原则 | 防的病 |
|------|--------|
| **P1** 先分开「零 run」与「run 在跑」, 再谈覆盖 | 把真在跑的 CI 判成 not_applicable |
| **P2** 任何不确定一律回落**现状** (wait) | 枚举分区 fail-OPEN |
| **P3** 自审**枚举全部产出 `covered=False` 的路径** (不是枚举 except 分支) | 修复在自己兜底路径复发 |
| **P4** 反向对照 + 每条测试能回答「它怎么会红」 | 修成对所有情况都 skip 的假绿 |
| **P5 (R2 重述)** 歧义时取**使 `covered` 更大**的读法 | 正向枚举对新值 fail-OPEN |

> **P5 的 R2 修正 (critical)**: 上一版写「取**匹配更多**的读法」。3 席独立指出并实跑证伪 —— `paths-ignore` 的公式是 `covered = ∃f, ∀p, ¬match(f,p)`, `match` 在**否定位**: 匹配更多 ⇒ `¬match` 更少 ⇒ **covered 更小** ⇒ 更容易 skip。反例 (qa 构造): `paths-ignore: ['docs/**']` + 变更为裸目录名 `docs` (子模块 gitlink 变更的真实输出形态) ⇒ 零段补偿使 `match('docs','docs/**')=True` ⇒ `covered=False ∧ confident=True` ⇒ 四重合取全过 ⇒ green。**「匹配更多」不是不变量, 「covered 更大」才是。**

> **P3 的三轮教训 (「空集真值真空」病灶连续下移三次)**:
> - R1: 空 `changed_files` ⇒ `∃` 对空集恒假 ⇒ `covered=False, confident=True`
> - R2: 零 event (流式映射 / 找不到 `on:` 键) ⇒ 静默流入并集
> - R3: 黑名单过滤后 **unit 集为空** ⇒ `any([])=False` / `all([])=True`
>
> 自审方法论已改过两次 (枚举 except → 枚举 `covered=False` 路径 → **显式白名单**), 每次都仍有下一级漏网。**本版的收口手法是「禁止默认值代为决策」**: §2 步骤 5 加显式早退守卫, 任何空集合都必须先被 `if not X: return covered=True` 拦住, 绝不允许 `any()`/`all()` 的语言默认值参与判定。这是比「再枚举一遍」更强的不变量 —— 它不依赖枚举的完备性。

### 1. `not_found` 上岗

`AetherBackend._normalize_pr_ci_status([])`: `"pending"` → **`"not_found"`** (`aether.py:223-224`)。非空 runs 映射逐字节不变。

**映射表**:

| `CIStatus.state` (backend 观测) | `pr_ci_status` (gate 派生) |
|---|---|
| `passing` / `failing` / `pending` | 同名 |
| `not_found` | `not_applicable` **或** `pending` (§3 四重合取) |
| — | `error` (`compute_verdict:185` 历史值, 无生产者, 保留不动) |

`not_applicable` **不进** `CIStatus.state` —— gate 层派生值, 非 backend 观测值。

**破坏性面 (3 项)**:
1. `tests/test_pre_merge_gate.py:329` 断言 `_normalize_pr_ci_status([]) == "pending"` → 改判 `"not_found"` (有意契约变更)。
2. 本条**不受 `path_coverage_aware` 控制** (`_normalize_pr_ci_status` 是 `@staticmethod`)。关掉开关**不能**完全回滚 —— 直接消费 `ci_backends` 而不经 `gate_check` 的调用方仍见新值。AC-6 的等价承诺**限定在 `gate_check` JSON 输出层**。
3. `_build_output` / `compute_verdict` 新增 **keyword-only** 参数 (§4)。
4. **同文件 docstring 同步** (R2 knowledge-manager): `aether.py:216-221` (`"→ passing | failing | pending"` + "unknown statuses route to pending") + `pre_merge_gate.py:20-21` Usage (加 `[--repo-root PATH]`)。

### 2. 新增 `lib/ci_path_coverage.py` (stdlib-only)

不引入 PyYAML。先例: `aria/skills/state-scanner/scripts/collectors/custom_checks.py` 的窄域 minimal parser —— **被借用的是 `_indent_of` (`:116`) + `_parse_check_list` 内的 reference-indent 技法 (`:177-229`)**, 非复用其代码。(R1/R2 三轮引用勘正: 此前引的 `:62`/`:63-65` 均落在 section-divider 注释上。)

**双层结构 (R2 新增, 解 AC-7 注入缝)**:

```python
def _match_coverage(workflow_files: list[tuple[str, str]], changed_files: list[str]) -> dict:
    """纯函数: (相对路径, 文件文本) 列表 × 变更文件集 → 覆盖判定。无 IO, 无 git。"""

def coverage(repo_root: str, main_branch: str, pr_branch: str) -> dict:
    """薄壳: 算 changed_files (步骤 0) + 读 workflow 文件 (步骤 1) → 委托 _match_coverage。永不 raise。"""
```

> R2 3 席指出: 簇 C 把 git 调用移进模块后, AC-7 要对同一 fixture root 喂不同变更集**按字面不可实现**; 若 fixture 目录在 Aria 仓内, `git -C` 会**成功**并返回 Aria 自己的 changed files ⇒ 断言在错误输入上求值, 且失败模式**不对称**(「→not covered」会意外通过)。拆纯函数后 AC-7 直接测 `_match_coverage`, AC-5f/5g 测 `coverage()` 的 fail-CLOSED 包裹层。

**返回契约 (两层同 schema)**:
```
{"covered": bool, "confident": bool, "reason": str,
 "workflows_seen": int, "changed_files_count": int,
 "covered_by": str|None, "repo_root_resolved": str|None}
```
- `workflows_seen` / `changed_files_count` 由 `_match_coverage` 从入参长度直接算出 (`len(workflow_files)` / `len(changed_files)`)。
- **`repo_root_resolved` 是两层共享契约中唯一由外层 `coverage()` 专属回填的字段** —— `_match_coverage` **恒返回 `None`** (它签名里没有 `repo_root`, 结构上算不出)。(R3 backend-architect Finding F: 不写死这句, 两个实现者可能一个填 `None`、一个干脆不产出该键, 违反「键恒存在」哲学且无测试能发现。)
- **`_match_coverage` 自带防御性早退 (R4-B)**: 函数首行 `if not changed_files: return covered=True, confident=False, reason="changed_files_empty"`。
  > 步骤 0 的空集守卫只在 `coverage()` 层, 而 `_match_coverage` 是**被设计成可独立单测的纯函数** (R2 引入双层结构的初衷), AC-7/AC-8c 已在直接喂参数调用它。任何第二个直接调用点 (含未来测试作者想测「零变更」而直接调 `_match_coverage(real_workflows, [])`) 会**原样复现 R1 最初那个** 「`∃` 对空集恒假 ⇒ `covered=False, confident=True` = 最高置信度 skip」的 bug, 且无任何报错提示。

#### 步骤 0 — 变更文件集 (仅 `coverage()`)

```
git -C <repo_root> diff --name-only -z <main_branch>...<pr_branch>
```
- **`-z` 必须** (绕开 `core.quotePath` 八进制转义)。**三点 `...`** (merge-base 语义)。
- 解析: `stdout.rstrip("\0").split("\0")`, 再滤空串 (R2 实测: 非空 diff 的 `-z` 输出**含尾随 NUL**, 朴素 `split` 会多出一个空元素)。
- 非零退出码 / 任何异常 / **结果为空** ⇒ **立即** `covered=True, confident=False, reason="changed_files_empty"` 或 `"changed_files_unavailable"`, 不进步骤 1+。
  > R1 抓到的最危险 fail-OPEN: 上一版 ∃ 对空集恒假 ⇒ `covered=False, confident=True` = **最高置信 skip**。触发路径全现实: `--main-branch` 默认 `"main"` 而本仓是 `master` (实测 `git diff main...HEAD` → exit **128**) / 跨仓分支不存在 / 空 PR / 只改 gitlink。
- 同时回填 `repo_root_resolved = git -C <root> rev-parse --show-toplevel` (R2 tech-lead: 让错配事后可定位)。
- **子模块 gitlink 变更**: `git diff --name-only` 只输出**裸目录名** (实测本机输出 `aria-orchestrator`)。按普通路径参与匹配。

#### 步骤 1 — 收集 workflow 文件 (仅 `coverage()`)

`.forgejo/workflows/` + `.github/workflows/` + `.gitea/workflows/`, 扩展名 `*.yml` + `*.yaml`。读为文本, 传给 `_match_coverage`。

- 三目录皆不存在, **或**存在但 0 个 `*.yml`/`*.yaml` ⇒ `covered=True, confident=False, workflows_seen=0, reason="no_workflow_files"`。
  > 「目录在但空」与「目录不存在」**认知等价** (都没有可读的 workflow 定义), R1 版让前者落 `covered=False, confident=True`。
- **⭐ 单个文件读失败 (R3 critical-family, code-reviewer Finding 3)**: **任一** workflow 文件读失败 (非 UTF-8 / dangling symlink / 权限) ⇒ 该文件**仍计入 `workflows_seen`** 并单独产出一条 `covered=True, confident=False, reason="workflow_unreadable"` 的 unit。**不得**静默跳过。
  > R2 版只定义了「**全部**读失败」。**部分**读失败的自然实现是 `try/except: pass` 跳过该文件 ⇒ `if not texts` 守卫不触发。R3 实跑构造 (2 个 workflow, 覆盖变更的那个不可读): 两个都可读 → `covered=True` ⇒ wait (正确); 覆盖那个不可读 → `covered=False, confident=True` ⇒ 四重合取全过 ⇒ **green, 而该路径的 CI 正在跑**。且 AC-5a 按字面用**单文件**不可读 fixture 即可通过 (那时「全部读失败」成立), 现有 AC 集合**结构上抓不到它**。

#### 步骤 2 — 解析 `on:` 子树 (`_match_coverage`)

**通用预处理 (R3, 优先于下面一切判断)**: 对**任何**被拿来做同行残留判断或值解析的物理行, 先剥行尾 `#` 注释 (quote-aware), 再 strip, 再剥**成对**首尾引号 (单/双)。
  > R3 backend-architect: 「同行残留判断」与「剥注释」的执行顺序未定义。真实常见形态 `on:  # yamllint disable-line rule:truthy` (正因 `on:` 的 YAML 1.1 布尔陷阱广为人知才会有人加这条 disable 注释) 在两种顺序下分类不同。两个方向最坏都只是多余 wait, 但属实实的实现者分叉点。

**`on:` 键识别**: 接受 `on:` / `"on":` / `'on':`, **且必须是列 0 的文档顶层键** (R3 code-reviewer minor 6: 否则 `run: |` 块体内的 shell/markdown 行出现 `on: ...` 会被误认)。
  > GitHub 官方为规避 YAML 1.1 `on`→bool 推荐引号写法; 本仓语料 4/4 裸 `on:`, 套件测不到该形态 —— 故需 AC-13 正面验证引号写法与裸写法**等价**。

**缩进跟踪 (R2 要求正文化, 不再「借用引用」)** —— 5 条可直接编码的规则:
1. 记 `on:` 键行的缩进为 **N**。
2. `on:` 后**同行有非空白残留** (`on: [push]` / `on: {…}` / `on: push`) → 见「非块状 `on:`」。
3. 从下一行起扫描: **空行与纯注释行跳过, 不终止块也不参与缩进判定**。
4. 首个缩进 > N 的非空非注释行, 其缩进锁定为 **参照缩进 E**。此后: 缩进 **== E** ⇒ 新的 event 键; 缩进 **> E** ⇒ 当前 event 的子结构 (跳过, 不生成新 event); 缩进 **< E 且 > N** ⇒ **不认识的结构** ⇒ 该 workflow `covered=True, confident=False`。
5. 缩进 **≤ N** 的非空非注释行 ⇒ `on:` 块结束。

**非块状 `on:`**:
- `on: push` / `on: [push, pull_request]` (标量或流式序列) ⇒ 视为**无 paths 过滤** ⇒ 该 workflow `covered=True, confident=True, covered_by="<file>#<event>"`。
- `on: {…}` (流式映射) ⇒ **不解析** ⇒ `covered=True, confident=False, reason="flow_mapping_on_block"`。
  > **设计收窄 (R2-fix, 请 R3 挑战)**: R2 backend-architect 用最小原型实测流式映射会让缩进扫描抽到 **0 个 event** 而静默流入并集。与其补一套流式映射解析规则 (再开一个正确性来源), 不如直接 fail-CLOSED。代价: 用流式 `on:` 的仓库永远 wait。本仓 4/4 块状, 今天零代价。

**⭐ 零 event 兜底 (R2 critical N-β)**: 走完上述流程后 **event 数为 0** (含找不到 `on:` 键、`on:` 块为空、文件被截断、混入的非-workflow `*.yml`) ⇒ 该 workflow `covered=True, confident=False, reason="no_events_parsed"`。**不允许**以 0 个 (workflow, event) pair 静默参与步骤 5 的并集。

**标量归一化**: 剥行尾 `#` 注释 (quote-aware) → strip → 剥**成对**首尾引号 (单/双)。
  > 语料实证: 4 份 workflow 的 pattern **全部**单引号。忘剥 ⇒ 恒不匹配 ⇒ **全仓假绿**。

**序列**: 支持块序列 (`- item` 多行) 与流式序列 (`key: [a, b]`)。`workflow_dispatch: {}` 视为无子键。

**fail-CLOSED 第二半 (R3 定作用域 + R4 定命中判据与 `---` 语义)**: 构造扫描 (`&anchor` / `*alias` / `<<` / `!tag`) **只在 `on:` 键行到 `on:` 块结束的行区间内进行** (区间由规则 1/5 已算出), **且跳过纯注释行**。命中 ⇒ 该 workflow `covered=True, confident=False, reason="unrecognized_yaml_construct"`。

**⭐ 命中判据 — 位置式, 不是子串式 (R4 code-reviewer 实跑)**: 对区间内每一行, 先走「通用预处理」(剥注释 → strip → 剥块序列标记 `- ` → 剥成对引号), 然后判 —— **值或键的首字符**为 `&` / `*` / `!`, 或**键位以 `<<` 开头**。`*` / `&` / `!` 出现在串**中间**一律**不算命中**。
> R3 把作用域从全文件收窄到 `on:` 块, 但**区间内恰好就是 `paths:` 通配模式所在处**。R4 实跑: 朴素子串读法 (`'*' in line`) 在 4 份真实语料中**命中 3 份** —— `- 'skills/issue-triage/**'` / `- 'aria/skills/issue-triage/**'` / `- 'aria-orchestrator/docker/aria-runner/**'` ⇒ 每一份带 `paths:` 的 workflow 都 fail-CLOSE ⇒ 整体 `confident=False` ⇒ 四重合取恒不过 ⇒ **恒 wait 复发**。位置式读法则 4/4 零命中。R3-B 报的是同一病经由全文件扫描; 收窄作用域消除了旧路径, 却把扫描搬到了通配符的家门口。

**⭐ `---` 的正确 YAML 语义 (R4 code-reviewer)**: 列 0 的 `---` 出现在**首个非空非注释内容行之后**才是多文档分隔 ⇒ fail-CLOSED; 出现在其**之前**是 **YAML 文档起始标记** ⇒ **忽略**。
> R3 版写「仅当出现在 `on:` 块之前且在列 0」—— 而文档起始标记恰恰**永远**满足这两个条件 (文件首行、列 0)。实跑: 首行 `---` 的 workflow 即便 `paths` 明确命中变更也判 `unrecognized_yaml_construct` ⇒ 该仓**任何**变更恒 wait, 且 **AC-7b 明确不钉 covered 真值 ⇒ 没有任何 AC 会红** = 静默失效。`yamllint` 的 `document-start` 规则**默认要求**首行 `---`, 与本文自己援引的 `on:  # yamllint disable-line` 是同一批用户。本仓语料 4/4 首行为注释, 今天零代价。

> **R3 code-reviewer 实跑, 真实语料 2/4 命中**: R2 版未定作用域, 而 `---` 是文档级构造, 把实现者往「全文件扫」推。全文件扫描下 —— `submodule-gate-tripwire.yml:122-133` 的 markdown 粗体 `**Detected at**:` 等 **5 行 strip 后以 `*` 开头** (朴素 `*alias` 命中); `:93` `echo "misses<<EOF"` 命中 `<<`; `build-aria-runner.yaml:97/:99` `echo "--- image size ---"` 命中 `---`。**这两份文件正是 AC-7 meta fixture 要冻结进仓的语料** ⇒ tripwire 判 `covered=True` 会让 AC-7 的 `['docs/foo.md']`→not covered 断言**直接失败**, 且整体 `confident=all(...)` 塌成 False ⇒ 四重合取过不了 ⇒ **恒 wait 复发**。方向虽是 fail-CLOSED (不误 skip), 但按 §Why 自己的判据「恒红同样零信息量」, 这是把病搬回原点。

#### 步骤 3 — 事件是否贡献覆盖 (`_match_coverage`)

**封闭黑名单 (不贡献覆盖)** —— 结构上不可能被 PR 触发的事件:
```
workflow_dispatch, workflow_call, schedule, issues, issue_comment, release,
create, delete, fork, watch, registry_package, deployment, deployment_status,
gollum, page_build, public, status, repository_dispatch
```
> R2 加 `workflow_call` (3 席): 可复用 workflow 结构上不可能被 PR 事件触发, 落「未识别 ⇒ covered=True」会让任何含它的仓**恒 wait** —— 病从假绿一侧搬到恒红一侧, 而恒红是 §Why 认定的同样零信息量的那一侧。

**paths-aware 白名单** (走步骤 4 真实路径匹配): `push` / `pull_request` / **`pull_request_target`**。
> R2 3 席指出上一版步骤 3 与 AC-5h 对 `pull_request_target` 给出**互斥**处置。技术事实: 它与 `pull_request` 的 `paths`/`paths-ignore` 语法语义完全相同, 不存在「语义未知」的理由。归入白名单。

**其余任何事件名** (含 `merge_group` / 未来新增) ⇒ 该 event `covered=True, confident=False, reason="unrecognized_event"` (不猜其 paths 语义)。
> `merge_group` 留在这里是**对的** —— 合并队列不受 paths 过滤, `covered=True` 即真实语义。

#### 步骤 4 — 单 event 的路径覆盖 (`_match_coverage`)

**判定序 (R3: 顺序本身是规格的一部分, 不再靠表格行序隐含表达)** —— 按下表**自上而下**求值, 首个命中即返回:

| # | 情形 | 结果 |
|---|------|------|
| **1** | 解析到 `paths-ignore` 键 —— **无论 `paths` 是否同时存在** | **立即** `covered=True, confident=False, reason="paths_ignore_present"`, **不再检查 `paths`** |
| 2 | 无 `paths` 且无 `paths-ignore` | `covered=True, confident=True, reason="no_event_filter"` |
| 3 | `paths` 键存在但解析结果为空列表 | `covered=True, confident=False, reason="unparsable_paths"` |
| 4 | 有 `paths` (非空) | `covered = ∃f ∈ changed_files, ∃p ∈ paths, match(f, p)`; **`confident=True`**; reason = `covered_by_paths_match` (真) / `no_paths_match` (假) |

> **R3 backend-architect**: R2 版用**表格行序**隐含表达优先级。实现者很自然会把「有 `paths` → 做真实匹配」当主路径先写 (那是「有趣」的一支), 只在其后 `elif` 兜底检查 `paths-ignore` —— 对「两者共存」的输入会直接落真实匹配分支产出 `covered=False, confident=True`, 正是设计要根治的极性反转以另一种方式复发。故提为**第 1 条显式规则 + 短路**。第 4 行的 `confident` 字段也是 R3 补的 (R2 版只给了 `covered` 公式, 承重算法须钉到字段级)。

> **⭐ 设计收窄 (R2-fix 关键决定, 请 R3 挑战)**: 上一版试图从 `paths-ignore` 推导「不覆盖」(`covered = ∃f ∀p ¬match`)。该公式把 `match` 放在**否定位**, 使 P5 的极性反转 (N-α critical, 3 席命中 + 实跑证伪)。R2 三席分别提出「双重求值取保守」/「strict-only + 补偿形态 fail-CLOSED」/「极性感知」三种修法 —— **本版一律不采纳**, 改为**根本不从 `paths-ignore` 推导不覆盖**: 存在即判 `covered=True`。
> - 消掉的: 整个极性问题类 + 零段补偿在否定位的副作用 + 三种修法各自的新表面。
> - 代价: 用 `paths-ignore` 表达过滤的仓库永远 wait (治不干净, 但**绝不误 skip**)。
> - 今天成本: **零** (本仓 4/4 用 `paths:`, 零 `paths-ignore`, 已 grep 确认)。
> - 留 follow-up: 若将来有真实需求, 需先对 Forgejo 匹配器实测再实现。

#### 步骤 5 — 并集 (`_match_coverage`) — **显式白名单单出口**

> **P3 白名单**: `covered=False` **仅允许**由下面这一条产出。其余**所有**分支上文已各自显式写明 `covered=True`。

**⭐ 前置守卫 (R3 critical, 2 席独立命中 + 实跑双读法结论相反 3/3)**:

**`units` 的定义 (R4 两席独立命中 —— 上一版只写了 pair, 漏掉整 workflow 级判定)**:

```
units = pair_units + workflow_level_units

pair_units           = [(workflow, event) | event 不在步骤 3 黑名单内]
workflow_level_units = [(workflow, None)  | 步骤 1/2 对该 workflow 整体下过 fail-CLOSED 结论]
                       # 即 workflow_unreadable / flow_mapping_on_block / no_events_parsed
                       #   / unrecognized_yaml_construct / unrecognized_indent_structure
                       # —— 这五类在拿到 event 列表**之前**就已判定, 结构上没有 event

if not units:          # 只含黑名单事件的 workflow: 两类都不产 unit —— 这是守卫唯一该触发的形态
    return covered=True, confident=False, covered_by=None, reason="no_paths_aware_event"
```

`workflow_level_units` 一律 `covered=True, confident=False`, **同时参与 `covered` 的 OR 与 `confident` 的 AND**。它们没有「走到步骤 4 第 4 行」, 天然不满足下方白名单条件 2, 故不改变任何安全性论证。

> **R4 反例 (backend-architect 构造, code-reviewer 实跑复现 4/4 场景两读法结论相异, 其中 2 场景 WAIT↔GREEN 翻转)**: `wf1.yml` (`on: pull_request` + `paths:['docs/**']`, 变更 `['src/foo.py']` 不匹配 ⇒ 合法 unit, `covered=False`) + `wf2.yml` (`on: {push: {...}}` 流式映射 ⇒ 按设计收窄判 `covered=True, confident=False`, **但产不出 event**)。按上一版字面公式 `wf2` 对 `units` 贡献**零个元素** ⇒ 三项条件全真 ⇒ `covered=False, confident=True` ⇒ **green, 而 `wf2` 可能正覆盖 `src/foo.py` 且 CI 在跑**。
>
> **这是「空集真值真空」病灶的第四次形变** —— 前三次是「集合恰好为空, 语言默认值代为决策」, 这次是「**集合的构造公式对一整类合法贡献者结构性不可达**」, 前置守卫检查不到它 (`units` 在反例里非空)。
>
> **规格作者自己隐约意识到但只堵了五分之一的佐证**: AC-5a 的 fixture 是「一个可读且不匹配 + 一个不可读」并断言整体 `covered=true` —— 它**正是**针对「整 workflow 级判定必须折入同一聚合池」设计的正面测试, 但只覆盖了 `workflow_unreadable` **一个**实例; 另外四个结构完全相同的姊妹分支 (AC-5b/5j/5k/5n) 全部只在**单 workflow、无伴随真实 unit** 的场景下测, 抓不到混合场景。故 AC-5a 参数化 (见验收标准)。

> **必须显式早退, 绝不允许 `any()`/`all()` 对空集的默认值代为决策。** 步骤 3 的黑名单事件「不贡献覆盖」—— 它既不产 `covered=True` 也不产 `covered=False`, 而是**不产 unit**。当一个仓的全部 workflow 只含黑名单事件 (真实例子: `.forgejo/workflows/submodule-gate-tripwire.yml` 只有 `workflow_dispatch`; 纯 `schedule` 仓同理), unit 集为空:
> - 白名单条件 2 为假 ⇒ 规格**不允许** `covered=False`;
> - 「任一 unit 判 True ⇒ 整体 True」对空集**也不触发**;
> - ⇒ 两条都不覆盖。R3 实跑两种自然读法: 实现者 A (照白名单字面, 非允许即 True) → `covered=True` ⇒ **WAIT**; 实现者 B (`covered=any(units)`, `confident=all(units)`; 注意 `all([]) is True`) → `covered=False, confident=True` ⇒ 四重合取全过 ⇒ **GREEN**。**3/3 组输入结论相反。**
>
> 这是「空集真值真空」病灶的**第三次**下移 (R1: 空 `changed_files` → R2: 零 event → R3: 黑名单过滤后空 unit), 也是 `feedback_spec_underdetermination_two_implementer_test` 的签名形状发生在本版**最承重的结构性主张**上。AC-11(a) 的输入集 (5a~5l) 全不含这形态, 抓不到 —— 故新增 **AC-5m**。

**唯一允许产出 `covered=False` 的条件 (三项全真)**:
1. `workflows_seen >= 1` 且 `changed_files_count >= 1`;
2. `units` 非空, 且**至少存在一个** unit 走完了步骤 4 的**第 4 行** (非空 `paths` 分支);
3. **所有**走到第 4 行的 unit 的 `∃f∃p match(f,p)` 全为假。

⇒ `covered=False, confident=True, covered_by=None, reason="no_paths_match"`。

任一 unit 判 `covered=True` ⇒ 整体 `covered=True`; `covered_by` 取**首个 `confident=True` 的命中**的 `"<相对路径>#<event>"`。
**整体 `confident` 聚合**: `confident = all(unit.confident for unit in units)` —— 任一不确定则整体不确定。
**聚合 `reason` 的确定性取值 (R4 两席)**:
1. `covered=False` ⇒ `no_paths_match` (唯一)。
2. `covered=True ∧ confident=True` ⇒ 取 `covered_by` 那个 unit 的 reason。
3. `covered=True ∧ confident=False` ∧ `covered_by != None` (不确定性被**其它不相关 unit** 拖累) ⇒ **`mixed_confidence_partial_match`**, **不得**复用 `covered_by` 那个 unit 的 `covered_by_paths_match` —— 否则模板 3 渲染出自相矛盾的 `coverage undetermined (covered_by_paths_match, …)`。
4. `covered=True ∧ confident=False` ∧ `covered_by == None` (无任何 unit 同时 `covered=True ∧ confident=True`) ⇒ 取**首个 `confident=False` 的 unit 的 reason**, 排序键 = (workflow 相对路径, event 在文件中的出现序; `workflow_level_units` 的 event 序视为 `-1`)。
   > R4 实跑: 三个不确定 unit (`flow_mapping_on_block` / `no_events_parsed` / `workflow_unreadable`) 并存且 `covered_by=None` 时, 上一版**取哪一个未定义** ⇒ 模板 3 的 `<reason>` 因实现而异。

#### 步骤 6 — `branches:` 不实现 (见 §非目标 N1)

#### 步骤 7 — `match(f, p)` 语义

**只在正向 `paths` 分支使用** (步骤 4 已不再有否定位用法 ⇒ P5 极性在本版**只有一个方向**)。

**支持特性**: 字面字符 + `*` + `**`。**仅此三种**。
- `**` → `.*` (含 `/`); `*` → `[^/]*` (不含 `/`); 其余 `re.escape`; 全串锚定 `\A...\Z`。**不用 `fnmatch`** (其 `*` 跨 `/`)。
- **零段补偿 (P5, 扩大匹配)**: 模式以 `/**` 结尾 ⇒ 额外接受去掉 `/**` 的裸前缀 (`a/**` 也匹配 `a`); 以 `**/` 开头 ⇒ 额外接受去掉 `**/` 的剩余串 (`**/*.md` 也匹配根 `README.md`)。
- **裸目录名 / 尾随斜杠**: `paths: ['docs']` 与 `['docs/']` 一律**同时**接受 `docs` 本身与其下任意深度。大小写**敏感**。

**移出支持集 → 该 event `covered=True, confident=False, reason="unsupported_pattern_feature"`**: `?` / `+` / `!` 前缀 / 字符类 `[]` / 空 pattern / 前导 `/` 或 `./`。
> **`?` 的理由**: GitHub filter-pattern 的 `?` = 「**前一字符出现 0 或 1 次**」(正则式), **不是** glob 单字符。上一版 `?`→`[^/]` 写反, 方向恰是误 skip。且真正执行的是 Forgejo Actions, 其匹配库与 GH 文档是否逐字一致**未经实证** —— 收缩到两引擎必然一致的交集是唯一不需先做 Forgejo 实测就成立的选择。

#### 步骤 8 — 永不 raise

任何异常 ⇒ `covered=True, confident=False, reason="exception:<type>"`。

#### `reason` 取值全表 (R2 补 — 它被拼进持久化 `raw_message`)

| reason | 产出方 | covered / confident |
|--------|--------|---------------------|
| `changed_files_empty` / `changed_files_unavailable` | 步骤 0 | True / False |
| `no_workflow_files` | 步骤 1 | True / False |
| **`workflow_unreadable`** (R3) | 步骤 1 (per-file) | True / False |
| **`no_paths_aware_event`** (R3) | 步骤 5 前置守卫 | True / False |
| **`mixed_confidence_partial_match`** (R3) | 步骤 5 聚合 | True / False |
| `flow_mapping_on_block` / `no_events_parsed` / `unrecognized_yaml_construct` / `unrecognized_indent_structure` | 步骤 2 | True / False |
| `unrecognized_event` | 步骤 3 | True / False |
| `paths_ignore_present` / `unparsable_paths` | 步骤 4 | True / False |
| `unsupported_pattern_feature` | 步骤 7 | True / False |
| `exception:<type>` | 步骤 8 | True / False |
| `covered_by_paths_match` | 步骤 4/5 | True / True |
| `no_event_filter` | 步骤 4 | True / True |
| **`no_paths_match`** | 步骤 5 | **False / True** ← 唯一 |

### 3. `gate_check` 接线 + `compute_verdict`

```python
path_coverage = None
if pr_status.state == "not_found":
    if cfg["path_coverage_aware"]:
        path_coverage = coverage(repo_root, main_branch, pr_branch)
        not_app = (
            (not path_coverage["covered"])
            and path_coverage["confident"]
            and path_coverage["workflows_seen"] >= 1
            and path_coverage["changed_files_count"] >= 1
        )
        pr_ci_status = "not_applicable" if not_app else "pending"
    else:
        pr_ci_status = "pending"      # ← 无条件回折, 不受开关影响
else:
    pr_ci_status = pr_status.state
```

**`compute_verdict` — catch-all 极性反转 (不新增 `not_applicable` 分支)**:

```python
if pr_ci_status in ("failing", "error"):
    verdict = VERDICT_FAIL
elif pr_ci_status == "pending":
    verdict = VERDICT_WAIT
elif pr_ci_status not in ("passing", "not_applicable"):
    verdict = VERDICT_WAIT          # fail-CLOSED: 未知态一律等
elif main_in_flight_runs:
    verdict = VERDICT_WAIT
else:
    verdict = VERDICT_GREEN
```

对 v1.64.0 全部现有输入**逐字节等价**。`not_applicable` 与 `passing` **同列**进入既有 in-flight 判定 ⇒ Rule #8 (a)(b) 独立性由**结构**保证。同步改 `:190`/`:193` 两条注释。

**verdict 真值表**:

| pr_ci_status | main in-flight | verdict |
|---|---|---|
| `failing` / `error` | — | `fail` |
| `pending` | — | `wait` |
| **未知值** (含未翻译的 `not_found`) | — | **`wait`** (新, fail-CLOSED) |
| `not_applicable` | 非空 / 空 | **`wait`** / `green` |
| `passing` | 非空 / 空 | `wait` / `green` |

**`raw_message` — 生产者钉死 (R2 N-ε)**: 由 **`compute_verdict` 内部合成** (从 `path_coverage` 的 `workflows_seen`(N)/`reason` + `len(main_in_flight_runs)`(M)), 覆盖 `_build_output` 的默认空串。**不得**在 `gate_check` 事后打补丁改 dict —— 那正是簇 F 判为反模式的写法。

**模板选择器 —— 互斥全覆盖的判定序 (R3: 必须是全函数)**。按下表**自上而下**求值, 首个命中即用:

| # | 条件 | 模板 |
|---|------|------|
| 1 | `pr_ci_status=="not_applicable"` ∧ `main_in_flight_runs==[]` | `no workflow covers the changed paths (N workflows scanned); PR CI check not applicable — main in-flight clean` |
| 2 | `pr_ci_status=="not_applicable"` ∧ `main_in_flight_runs!=[]` | `no workflow covers the changed paths (N workflows scanned); PR CI check not applicable — BUT main has M in-flight run(s): waiting per Rule #8 (b)` |
| 3 | `pr_ci_status=="pending"` ∧ `path_coverage is not None` ∧ `confident==False` | `coverage undetermined (<reason>, N workflows scanned) — conservatively treated as covered; waiting` |
| 4 | `pr_ci_status=="pending"` ∧ `path_coverage is not None` ∧ `covered==True` ∧ `confident==True` | `changed paths covered by <covered_by> (N workflows scanned); PR CI not yet reported — waiting` |
| **5** | **其余全部情形 —— 含 `path_coverage is None` 的每一次普通 gate 运行 (真实 CI 报 passing/failing/pending) 与 `path_coverage_aware=false` 路径** | **`raw_message = ""`** (保持 `_build_output` 默认, 与 v1.64.0 逐字节一致) |

> **R3 code-reviewer 实跑: R2 版的选择器不是全函数, 14 个可达输入组合中 8 条落 UNDEFINED** —— 其中包括 `path_coverage is None` 的**全部**情形 (即绝对多数路径: 每一次 backend 真报 passing/failing/pending 的普通 gate 运行), 以及 AC-12 自己的 mock #2/#3 (`covered=F, confident=T, seen=0`/`cnt=0` —— 模板 3 要 `confident=False`、模板 4 要 `covered=True`, **两条都不匹配**; 若实现者仍套模板 4 还会取到 `covered_by=None`)。AC-6 隐含要求「`path_coverage is None` ⇒ `raw_message` 保持空串」但全文没写, 只能靠猜, 且只在开关关闭这一支被 AC 兜住 —— 开关**开着**的常态路径既无规定也无 AC。猜错 ⇒ 每次普通 gate 都把伪诊断文本落盘进 `.aria/workflow-state.json`。

> 后两条是 R2 抓的: (i) fail-CLOSED 是本版**最宽**的一类路径 (步骤 0/1/2/3/4/7/8 全汇入), 恰恰是第三种 wait、恰恰没模板、恰恰没 AC (N-μ); (ii) N1 残留的排查指引依赖 `covered_by`, 但该形态走的正是第四条路径, 上一版无模板 ⇒ 诊断结构上不可达 (N-η)。`raw_message` 是**唯一**被持久化进 `.aria/workflow-state.json` 的诊断槽位 (`gate_state_helper.py::write_gate_state()` kwarg 集合固定)。

### 4. 输出 schema

`_build_output` 与 `compute_verdict` 各新增 **keyword-only** 参数 `path_coverage: dict | None = None` (带默认值 ⇒ 对既有 positional caller 兼容; 属对 Hard Constraint #10 的**显式增补**, tasks 写明「只加 keyword-only 参数」)。

**7 个输出构造点** —— `:196` (compute_verdict) / `:237`+`:250` (`_no_ci_output`) / `:290` (enabled=false) / `:307` (precheck fail) / `:322` (main-leg error) / **`:335`** (PR-leg error; R2 三席勘正, R1 版误作 `:337`; R3 code-reviewer `grep -n "_build_output("` 复核 7/7 精确) —— **全部**显式传值, 未计算时传 `None`。**`path_coverage` 键恒存在**, `null` 表示「未做覆盖判定」, 与「判定了但无覆盖」严格区分。

**另: `gate_check:343` 的 `compute_verdict(...)` 调用点** (R3 code-reviewer minor 4) —— 它是唯一需要**同时**改传派生 `pr_ci_status` (不再是 `pr_status.state`) 和 `path_coverage=` 的一行, 也是 §3 伪代码结束后没接上的那一行。tasks 须点名。

### 5. 配置 + CLI + 作用仓

- 新键 `phase_c_integrator.pre_merge_gate.path_coverage_aware`, 默认 `true`, **必须加进 `DEFAULT_CONFIG`** (`pre_merge_gate.py:~45-60`) —— 否则 §3 的 `cfg["path_coverage_aware"]` 缺键即 **KeyError 崩溃** (`gate_check:287` 是 `{**DEFAULT_CONFIG, **user_normalized}`)。
- 新 CLI `--repo-root` (**默认 CWD**) → `gate_check(pr_branch, main_branch, config, repo_root=".")` (**带默认值**, 不破坏既有 3 参调用点与测试)。
- **作用仓一致性 — 机械化 (R2 tech-lead N-05)**: R1 版只是散文不变量 + SKILL.md 提示, 与本 change 要终结的「文档级规则」同型。本版: `gate_check` 把 `repo_root` **同时**作为 backend 子进程的工作目录传下去; 并把 `repo_root_resolved` 回填进 `path_coverage` 使错配事后可定位。
  > 实证必要性: 既有 dogfood 惯例是 `cd /home/dev/Aria && python3 aria/skills/.../pre_merge_gate.py --pr-branch <分支>` (`openspec/archive/2026-05-28-aria-ci-backend-abstraction/tasks.md:101`)。CWD=主仓而 PR 在子模块 ⇒ 前缀互不匹配 ⇒ green 而子模块 CI 在跑。且 R2 实测**两仓分支名确实会撞** (`feature/benchmark-transparency-enhancement` 等 3 个同时存在于两仓) ⇒ 撞名时 diff 成功、文件集是错仓的 ⇒ **静默假绿**, 步骤 0 兜不住。

  **⚠️ R3 补: 这条腿目前是「未实证的承重假设」, B.2 前必须先 spike** (code-reviewer Finding 5 + backend-architect Finding C, 2 席独立命中):
  - **承重假设**「aether 由 CWD 决定查哪个仓」**零实证**。实读代码: `AetherBackend.__init__(self, binary=None, timeout=DEFAULT_TIMEOUT)` **无 cwd 参数**; `_run_with_retry` (`aether.py:173`) 与 probe (`:150`) 的 `subprocess.run(...)` **均未传 `cwd=`**; `_query` 发的是 `aether ci status --branch <b> --json` —— **无仓参数**。若 aether 实际按 git remote / 配置文件解析仓, 整条机制化是**空转**。
  - **B.2 前置 spike**: 在两个不同 CWD 各跑一次 `aether ci status --branch <双仓同名分支> --json` 比对结果, 结论写回本 proposal。(memory `feedback_prod_state_must_ground_playbook` / `feedback_spec_precedent_verify_execution_history` 正是这形状。)
  - **代码面完整清单** (R2 版把 aria/aether.py 的改动写成「返回值 + docstring」, 漏了整条腿): `AetherBackend.__init__(..., repo_root: str | None = None)` (**`None` 时退回 ambient cwd, 保持向后兼容**) + `_run_with_retry`/`_verify_in_flight_flag` 的 `subprocess.run(..., cwd=...)` + `_instantiate` (`pre_merge_gate.py:151-161`) 透传 + `resolve_ci_backend(config, repo_root)` 签名 + `CIBackend` ABC 契约声明 + `GitHubActionsBackend` 是否同步接受 (哪怕忽略)。
  - **既有测试工厂需同步** (R2 backend-architect 实核): `test_ci_backends.py` 的 `TestAetherBackendQuery._backend()` (`:152-157`) 与 `TestAetherBackendPrecheck._backend()` (`:191-195`) 都用 `AetherBackend.__new__(AetherBackend)` 绕过 `__init__` 手工赋值 —— 若 `_run_with_retry` 开始读 `self.repo_root` 而工厂没补, 会直接 `AttributeError`。
  - **AC-14 验证** (见验收标准)。

### 6. 文档 + AB 套件同步面

| # | 落点 | 内容 |
|---|------|------|
| 1 | `SKILL.md:160-179` (尤其 `:176`) | 第二份 schema 副本 (流程块内三值枚举 + 三态结果) |
| 2 | `SKILL.md:240` | 「映射为 passing/failing/pending」补 `not_found` |
| 3 | `SKILL.md:241-245` | 步骤 5 verdict 表 |
| 4 | `SKILL.md:258-270` | Output schema |
| 5 | `SKILL.md:272-281` | 配置参数表 (+`path_coverage_aware`) |
| 6 | `SKILL.md:283-289` | 降级行为 (+「**黑名单可能过宽 / 白名单可能不全**」前提 — R2 勘正: P5 反转后风险方向已变) |
| 7 | `SKILL.md §C.2.4.X` | backend `not_found` 语义 |
| 8 | `config-loader/SKILL.md:241-281` | config key 权威清单 |
| 9 | `.aria/config.template.json:**73-90**` | `pre_merge_gate` 块 (R2 勘正: 上一版误作 `:73-86`; 该块仍用 legacy 键 `primitive_preference`/`no_aether_fallback`) |
| 10 | `aether.py:216-221` docstring + `pre_merge_gate.py:20-21` Usage | **R2 新增** — 本 change 直接改的源码自身文档 |
| 11 | AB 套件 (见下) | |
| 12 | `aria/CHANGELOG.md` | v1.65.0 |

**AB 套件 — 事实勘正 (R2 5/5 命中)**:

R1 版写「fixture 经 `ARIA_AETHER_MOCK_RESPONSE_FILE` 直接喂给真实 `pre_merge_gate.py` 执行」。**该机制不存在** (**实现源码 `*.py` 零命中**; R3 code-reviewer minor 1 勘正 R2 版「全仓 grep 零命中」的说法 —— 全仓其实命中 8 处, 全在 fixture JSON 的 `_consumed_by`/`_description` 与 benchmark.md 的勘误段里, 与本文 Follow-up 7 自洽), 且 `ab-results/2026-05-10-phase-c-integrator-pre-merge-gate/benchmark.md:70` **已明文勘误过同一说法一次**。真实机制: `tests/test_pre_merge_gate.py` 内 `mock.patch.object(gate, "resolve_ci_backend", ...)`; fixture JSON 是**人类参照文档**, 经 `fixtures[].test_case_in_unit_tests` 指向真实单测。

→ 新增 fixture `not_applicable_green.json` + `not_applicable_main_inflight_wait.json`, **各配一条真跑得起来的 `test_pre_merge_gate.py` 用例并填上 `test_case_in_unit_tests` 指针** (否则只是 JSON 里的文档条目); suite `version` `1.0.0` → `1.1.0`。
→ 该 suite 的 `primary_pass_gate_metric` 是 `wait_triggered_when_in_flight_mock_present`, 统计 **in-flight 触发的 wait**, 不含路径覆盖触发的 wait —— 否则本 change 会被误判为该指标回归。

### 7. Rule #8 文档面对齐 (主仓 — ⚠️ owner 权限面, 独立 commit)

**拟写入 CLAUDE.md 规则 #8 的确切文本** (指针级, 一句, 供 owner 逐字核验):

> 变更路径无任何 CI workflow 覆盖时 gate 返回 `not_applicable` 而非无限等待 (机制见 SKILL.md §C.2.4)。

预算: CLAUDE.md 当前 **151 行 / 13139 字节** (R1/R2 两轮独立 `wc` 实测吻合), 预算 ≤200 行 / ≤24000 字节。新增一句不撞预算。未含 P1-P5 / 四重合取 / 零段补偿等 skill 内部设计术语 (防 #116 baseline 污染)。

`.aria/config.json` `_lane` 回改为机械态描述。

---

## 非目标

**N1. `branches:` 过滤感知** — 方向性论证经 R1 4 席 + R2 复核**无反例**: `branches:`/`branches-ignore`/`tags:` 只能**减少**触发面, 忽略只会**高估**覆盖 ⇒ 落 wait 侧。

> **不变量声明**: 该论证成立**当且仅当** `covered=True` 恒等于保守侧。若将来把覆盖判定接到别的分支 (如「有覆盖 ⇒ 可信任 CI ⇒ 少等」), 论证会静默反转。
>
> **为什么不做「便宜版 branches 布尔检测」** —— R2 tech-lead 给出的具体反例 (取代上一版的抽象论证): `pull_request: branches: [master]` 是**对 base 分支**的过滤, PR 合入 master 时该 workflow **正常触发**; 便宜版看到「有 branches 限制」就剔出覆盖 ⇒ `covered=False` ⇒ **green 而 PR CI 正在跑**。这是一等一的假绿, 且该写法极常见。
>
> **⚠️ 已知残留**: `.forgejo/workflows/build-aria-runner.yaml` 仅 `push` + `branches:[feature/aria-2.0-m0-prerequisite]` + `paths:` , **无 `pull_request`**。忽略 branches 后, 任何其它分支改该路径的 PR 都判 `covered=true` ⇒ **恒 wait 复发**, 而 M6 aria-orchestrator 轨活跃。**ship 后该路径仍需上报 owner, 不属本 change 治好的范围。** 排查: 看 `raw_message` 第四条模板里的 `covered_by` 指向的 workflow 的 `branches:` 是否与 PR 分支不符 —— 若是则属 N1 已知限制, **不是「#122 没修好」也不是「第 5 次错过机制化」**。

**N2. `github_actions.py` 的 `not_found` 生产** — stub backend, 无 run 可映射。
**N3. `_open_question_no_ci_fallback`** — owner 待裁, 正交, 不动 (R2 已确认 `git diff` 该文件为空)。
**N4. Race condition mitigation** — SKILL.md 现有 future-Spec 项。
**N5 (R2 新增). 从 `paths-ignore` 推导不覆盖** — 见 §2 步骤 4 的设计收窄。
**N6 (R2 新增). 流式映射 `on: {…}` 解析** — 见 §2 步骤 2。

---

## 影响面

| 面 | 内容 |
|----|------|
| 代码 | 新增 `scripts/lib/ci_path_coverage.py` (双层: `_match_coverage` 纯函数 + `coverage` 薄壳); 改 `ci_backends/aether.py` (**返回值 + docstring + 构造参数 `repo_root` + `subprocess.run(cwd=)` ×2**) + `ci_backends/base.py` (`CIBackend` 契约声明) + `ci_backends/github_actions.py` (是否同步接受) + `pre_merge_gate.py` (接线 / catch-all 极性 / `--repo-root` / `_instantiate` + `resolve_ci_backend` 透传 / `:343` 调用点 / `path_coverage` 穿透 / `raw_message` 合成 / `DEFAULT_CONFIG` / Usage) |
| 测试 | `test_ci_backends.py` (含 `:152-157`/`:191-195` 两处 `_backend()` 工厂同步) + `test_pre_merge_gate.py` (含 `:329` 契约改判 + 2 个新 AB fixture 对应用例) + 新增 `test_ci_path_coverage.py` + 冻结 fixture `tests/fixtures/workflows/{submodule,meta}/` |
| 文档 | §6 表格 12 处 |
| 行为 | 有覆盖: `gate_check` 输出 6 个既有字段中 5 个逐字节不变 (`raw_message` 新增诊断文本)。无覆盖 + main 干净: `wait` → `green` + 留痕。无覆盖 + main 有 in-flight: 仍 `wait` |
| 版本 | aria-plugin MINOR → v1.65.0 |

---

## 验收标准

> **记法 (R3: 计数三轮三错, 索性去掉数字)** —— 子标号 (`5a~5n` / `8a~8c`) 各算**独立一条**; 母条目 `AC-5` / `AC-8` 不单独成条。

**核心判定**
- **AC-1** 无覆盖 + main 干净 → `verdict=green`, `pr_ci_status="not_applicable"`, `raw_message` **逐字等于** §3 模板 1, `path_coverage` 4 子字段全断言 (`covered=false`/`confident=true`/`workflows_seen>=1`/`changed_files_count>=1`)。
- **AC-2** (反向对照) 变更命中某 workflow `paths` + 零 run → `verdict=wait`, `pr_ci_status="pending"`; **除 `raw_message` 外** v1.64.0 的 5 个字段逐一相同; `raw_message` 逐字等于 §3 模板 4 且含 `covered_by`; `path_coverage.covered=true`。
  > R2 N-η: 上一版要求 6 字段全等 ⇒ 结构上**禁止** `raw_message` 携带 `covered_by` ⇒ N1 排查指引不可达。
- **AC-3** (Rule #8 (b) 独立性) 无覆盖 + main **有** in-flight → `verdict=wait` (**不得** green), `raw_message` 逐字等于 §3 模板 2。
- **AC-4** (P1, 对抗性) mock `coverage()` 返回 `covered=False`, 同时 `pr_status.state` 为**非** `not_found` 的真实值 → `pr_ci_status` 仍 `"pending"`, 且**断言 `coverage()` 未被调用**。
- **AC-12** (四重合取三项各自可红 — R2 N-θ) mock `coverage()` 三组参数化: `{covered:F, confident:F, seen:5, cnt:3}` / `{covered:F, confident:T, seen:0, cnt:3}` / `{covered:F, confident:T, seen:5, cnt:0}`, 各断言 `pr_ci_status == "pending"`。**三组 mock 均须按 §2 的 7 键完整 schema 构造** (`reason` 任取合法值, `covered_by=None`, `repo_root_resolved=None`)。
  > R4 实跑: mock #1 落模板 3, 而模板 3 插值 `<reason>` ⇒ 按字面只列 4 个键会在断言之前就 `KeyError: 'reason'`。(#2/#3 落模板 5 不读 reason, 无此问题 —— 二者是**非 conforming 对抗 mock**, 步骤 5 单出口保证生产不可达, AC-12 只断言 `pr_ci_status` 故不冲突。)
  > 单出口成立时后三项由 term 1 蕴含 ⇒ AC-11 恰恰保证它们永不是判定因素 ⇒ 删掉/写反/`.get()` 拿 None 全部测试仍绿。

**fail-CLOSED (逐条独立可红)** —— 均针对 `_match_coverage` 或 `coverage()`, 断言 `covered=true, confident=false` + 对应 `reason` + 无异常:
- **AC-5a** (R3 改双文件 → **R4 参数化**) fixture 模式为「**一个可读且不匹配 + 一个 X**」, **X 遍历全部 5 个整 workflow 级 fail-CLOSED reason** (`workflow_unreadable` / `flow_mapping_on_block` / `no_events_parsed` / `unrecognized_yaml_construct` / `unrecognized_indent_structure`) ⇒ 每组均断言**整体 `covered=true`** 且**聚合 reason 按步骤 5 第 4 条确定性规则**取值。
  > R2 版只用单文件不可读 (那时「全部读失败」成立 ⇒ 按字面通过, 抓不到「部分读失败」)。R3 版改双文件但**只测 `workflow_unreadable` 一个实例** —— R4 指出它其实是「整 workflow 级判定必须折入同一聚合池」这一整类的代表, 另外四个姊妹分支 (AC-5b/5j/5k/5n) 全在**单 workflow 无伴随真实 unit** 的场景下测, 抓不到混合场景。
- **AC-5b** `&anchor`/`*alias`/`<<`/`!tag` — **fixture 必须让触发 token 落在 `on:` 子树内** (R3)。**三条负控 (R4 补第三条)**: (i) token 只出现在 `run: |` 块体 ⇒ **不**触发; (ii) token 只出现在注释里 ⇒ **不**触发; (iii) **`paths: ['a/**']` 落在 `on:` 块内 ⇒ 不触发** (位置式命中判据, 串中间的 `*` 不算)。
- **AC-5b2** (R4) 首行 `---` 的 workflow (YAML 文档起始标记) + `paths` 命中变更 ⇒ `covered=true, confident=**true**, reason="covered_by_paths_match"` (**不得**判 `unrecognized_yaml_construct`); 对照: `---` 出现在首个内容行之后 ⇒ 判 `unrecognized_yaml_construct`。
- **AC-5c** 三目录皆不存在 (`workflows_seen=0`) · **AC-5d** 目录存在但 0 个 yml (`workflows_seen=0`)
- **AC-5e** `paths: []`
- **AC-5f** `changed_files` 为空 (不进步骤 1+) · **AC-5g** git 失败 (`--main-branch main` 撞 `master` 仓; **且 `gate_check` 不抛异常、`main()` 退出码 0**)
- **AC-5h** 未识别事件名 (**例子用杜撰的 `future_event`**, 不用 `pull_request_target` — R2 N-ι)
- **AC-5i** (R3 拆两子场景) **5i-1** 只有 `paths-ignore`; **5i-2** `paths-ignore` 与**非空 `paths` 共存** —— 两者均 `reason="paths_ignore_present"`。
  > 5i-2 专盯优先级写反: `if 'paths' in event: 走匹配 elif 'paths-ignore' ...` 这种顺序在「只有 paths-ignore」上是对的, 在「两者都有」上会错。
- **AC-5j** `on: {…}` 流式映射 (`reason="flow_mapping_on_block"`)
- **AC-5k** (R3 删 `"on":` 子句) 找不到 `on:` 键 / `on:` 块为空 / 零 event ⇒ `reason="no_events_parsed"`。
  > R3 qa: R2 版把 `"on":` 引号写法塞进 fail-CLOSED 断言, 与 §2「`on:` 键识别接受 `on:`/`"on":`/`'on':`」**直接矛盾** —— 照 AC 实现会把 GitHub 推荐写法误判为 fail-closed。移到 AC-13 正面验证。
- **AC-5l** 不支持的 pattern 特性 (`?`/`+`/`[]`/空/前导 `/`)
- **AC-5m** (**R3 critical**) 全部 workflow 只含黑名单事件 (fixture 直接用 `submodule-gate-tripwire.yml` 真实内容, 仅 `workflow_dispatch`) ⇒ `covered=true, confident=false, reason="no_paths_aware_event"`。**不得** `covered=false`。
- **AC-5n** (R3) 内部辅助函数抛任意异常 ⇒ 捕获后 `covered=true, confident=false, reason.startswith("exception:")` 且**不传播**; 另一条: 缩进介于 N 与 E 之间的行 ⇒ `reason="unrecognized_indent_structure"`。
  > R3 qa #1: 这两个 reason 在 R2 版**零 AC 覆盖**。`exception:<type>` 是整个手写 parser「永不 raise」承诺的唯一安全网 —— 漏写即 `gate_check` 崩溃 (§3 伪码未包 try/except), 是本 change 引入的新故障面。

**单出口性质**
- **AC-11** (a) 参数化跑遍 **AC-5a~5n** 全部输入, 断言**无一** `covered=false`; (b) **两个字面值互不相同的「应产出 `covered=False`」正例** —— `(['skills/state-scanner/scan.py'], 'skills/issue-triage/**')` 与 `(['docs/foo.md'], 'aria/skills/issue-triage/**')`, 各断言 `covered=false` 且 `reason=="no_paths_match"`。
  > R2 N-ν: R1 版输入集全是「应产出 True」的正例 ⇒ `match()` 恒真的退化实现也能全绿。
  > R3 qa #5: R2 版的 (b) 只有**一个**正例 ⇒ 「硬编码这一个输入」的退化实现 (`if changed_files==[...] and pattern==...: return covered=False else True`) 仍能同时通过 (a)(b)。该洞事实上被 AC-7 的另一独立反例补上了, 但 AC-11 不该依赖一条它没声明的外部依赖 —— 故直接把第二个字面值不同的正例**写进 AC-11 自身**。

**catch-all 极性 (baseline-failing)**
- **AC-10** `compute_verdict([], "not_found")["verdict"] == VERDICT_WAIT` 且 `compute_verdict([], "wat")["verdict"] == VERDICT_WAIT` 且 `compute_verdict([], "")["verdict"] == VERDICT_WAIT`。
  > **R2 N-γ 修正**: 上一版写 `compute_verdict(...) == wait` —— 该函数返回 **dict** (v1.31.0+), `dict == str` **恒 False** ⇒ 无红→绿窗口 ⇒ 簇 A 的修复**零自动化保护**。改后三条在 v1.64.0 上实测为红 (返回 `green`), 符合 SC 级 baseline-failing。

**开关 + 匹配语义**
- **AC-6** `path_coverage_aware=false` + 零 run → `gate_check` 输出的 v1.64.0 既有 6 字段逐一相同 (含 `pr_ci_status="pending"`); `path_coverage` 键存在且为 `null`。**不承诺** `CIStatus.state` 层回滚。
- **AC-7** (冻结 fixture, 双 root, **直接测 `_match_coverage` 纯函数**) 4 份 workflow 复制进 `tests/fixtures/workflows/{submodule,meta}/` (附来源 SHA + 抓取日期):
  - `submodule` (1 workflow): `['skills/issue-triage/x.py']`→covered; `['skills/state-scanner/scan.py']`→**not** covered; 两者并集→covered。
  - `meta` (3 workflows): `['aria/skills/issue-triage/x.py']`→covered; `['docs/foo.md']`→**not** covered; `['aria-orchestrator/docker/aria-runner/Dockerfile']`→covered (验证 N1 忽略 branches 落保守侧)。
- **AC-7b** (drift guard) 对**真实** `.forgejo/workflows/` 跑 `coverage()`, **只**断言「不抛异常 + 字段齐全 + `workflows_seen>=1`」, **不**钉 covered 真值。
- **AC-8** (表驱动, 三层分开 — R2 要求) **8a** `match()` 布尔层: `skills/issue-triage/**` 匹配 `skills/issue-triage/a/b.py` ✅ 且匹配裸 `skills/issue-triage` ✅; `skills/*/x.py` **不**匹配 `skills/a/b/x.py`; `**/*.md` 匹配根 `README.md` ✅ 且匹配 `docs/a/README.md` ✅; `.github/workflows/**` 的字面 `.` 不被通配污染。**8b** 解析层: 带单引号的原始 YAML 行 `- 'skills/issue-triage/**'` 经剥引号后能匹配。**8c** `_match_coverage` 层: `docs/v?/**` → `covered=true, confident=false, reason="unsupported_pattern_feature"`。

**Rule #6**
- **AC-9** (R2 5/5 命中重写)
  - **前置**: `ab-suite/phase-c-integrator-pre-merge-gate.json` 已升 `1.1.0` 且含 2 个 `not_applicable` fixture, **各自的 `test_case_in_unit_tests` 指向真实存在的单测方法**。
  - **命令**: 点名全称套件 `phase-c-integrator-pre-merge-gate` (**不用裸名 `phase-c-integrator`** —— 按 `AB_TEST_OPERATIONS.md` §场景1 的解析流程, 裸名会命中无关的 parent 套件 `ab-suite/phase-c-integrator.json`, 内容是 commit-generation / merge-conflict-handling / multi-remote-merge-push 三个 LLM eval)。
  - **基线**: 路径**写死** `aria-plugin-benchmarks/ab-results/2026-05-10-phase-c-integrator-pre-merge-gate/benchmark.json` (**不用「最近一次归档」/`latest` symlink** —— 二者均解析到 **state-scanner** 的归档)。
  - **判据 (R3 类型勘正)**: 既有 8 个 `structural_metrics.*` 的 `measured` 全部保持 **整数 `100`** (实测该字段是 int, `unit:"percent"` 另存 —— 写成 `"100%"` 会让实现者产出恒假断言, 同 N-γ 的病因) + `primary_pass_gate.measured == "100%"` (**这个才是字符串**) + `test_counts` 三组 `failed == 0`; 新增 2 个 `not_applicable` 指标无历史对照, 只需 `measured == 100` (**只追加, 不改既有 8 个指标的定义与分母**)。
  - **存档**: `ab-results/<date>-v1.65.0-phase-c-integrator-ci-path-coverage/`。
  > R1 版判据写「五维得分 (触发准确率/输出质量/工具使用/错误处理/Token 效率) 每一维不低于上一次归档, 容差 0」。R2 5/5 实地核实: 该 skill 3 份历史归档 schema 各不相同且**均无该字段**; 「五维」是 `aether:skill-benchmark` 插件的词汇, 全仓另一处出现是 M7 agent 淘汰选优的 LLM-judge 评分法 (proposal 自标「不适用本 MVP」)。

**R3 新增三条**
- **AC-13** (正面验证, 补 R2 引入的零测试设计点) 取 AC-7 的某个 fixture, 把 `on:` 替换成 `"on":` (再取一份换成 `'on':`), 断言产出与裸写法**逐字段一致** (`covered`/`confident`/`reason`/`covered_by` 全同)。
- **AC-14** (§5 backend cwd 那条腿 — R3 2 席指出它是「未实证承重假设 + 零 AC」) mock `subprocess.run`, 断言其**实际收到的 `cwd` == 传入的 `repo_root`**; 且 `os.path.realpath(cwd) == path_coverage["repo_root_resolved"]` (**R4 勘正**: `--repo-root` 默认 `"."` 而 `repo_root_resolved` 来自 `git rev-parse --show-toplevel` = 绝对路径, 直接 `==` **恒不等** ⇒ 会得到一条为错误理由而红的测试)。**可红**: 漏传则 `cwd` 为 `None`。
  > 与 §5 的 B.2 前置 spike 配套 —— spike 回答「aether 是否真按 cwd 解析仓」, AC-14 回答「我们是否真把 cwd 传下去了」。两件事都要。
- **AC-15** (模板 3 端到端 — 补 N-μ 剩下的那一半) mock `coverage()` 返回 `{covered:True, confident:False, reason:"no_workflow_files", workflows_seen:0, ...}`, 断言 `gate_check` 输出的 `raw_message` **逐字等于**模板 3 的渲染结果 (含 `reason` 与 `N` 的插值)。
  > 模板 1/2/4 分别由 AC-1/AC-3/AC-2 逐字钉死, 唯独模板 3 —— 覆盖面最广的一条 (步骤 0/1/2/3/4/7/8 的 fail-CLOSED 结果全部汇入) —— R2 版零端到端验证。AC-5x 系列测的是 `coverage()` 自身返回值, 不触达 `compute_verdict` 的拼装层, 两层之间的接线此前零验证。

---

## 风险

| 风险 | 缓解 |
|------|------|
| **误 skip 真该拦的 CI** (最高) | P1 分离 + P5 (covered 更大) + 四重合取 + catch-all fail-CLOSED + 步骤 5 显式白名单单出口 + AC-10/AC-11(a)(b)/AC-12 |
| 跨仓 repo_root 错配 | §5 机械化 (backend 共用 repo_root 句柄) + `repo_root_resolved` 回填 + AC-7 双 root |
| 手写 YAML parser | 只解析 `on:` 子树; 5 条缩进规则正文化; 零 event / 流式映射 / 白名单外形态一律 fail-CLOSED |
| `match()` 与 Forgejo 偏差 | 支持集收缩到两引擎必然一致的交集; 歧义取 covered 更大; 其余 fail-CLOSED |
| N1 残留致病复发 | §N1 显式披露 + `raw_message` 模板 4 携带 `covered_by` + 排查指引 + follow-up |
| AB 套件测不到新分支 | §6 新增 2 fixture + 真单测指针 + AC-9 前置条件 |

---

## Follow-up (Phase D 开 issue)

1. **N1 完整实现** (解析 `branches:` 值并与 PR 分支匹配; 首个受益场景 = `build-aria-runner.yaml`)。
2. **`paths-ignore` 真实推导** (需先对 Forgejo 匹配器实测)。
3. **流式映射 `on: {…}` 解析**。
4. **`.gitea/` 目录清单实测** (按当前 Forgejo 版本 probe)。
5. **`match()` 对 Forgejo 匹配器实测** (若确认与 GH 文档一致可放回 `?`/`+`)。
6. **非 workflow-文件形态表达 CI 的仓库** (服务端配置型) 的逃生口。
7. **fixture 的 `_consumed_by` 字段**仍留着已被勘误的 `ARIA_AETHER_MOCK_RESPONSE_FILE` 旧文本 (`green.json`/`wait.json`/`fail.json`/`wait_then_green.json`/`NEG-2-timeout.json` 共 5 处; 与同目录 `NEG-1-malformed.json` 的「Documentation only」自相矛盾)。
8. **`ab-results/latest` symlink 已 stale** —— 指向 `2026-05-13-state-scanner-issue-101-fix`, 其后至少 6 个更新归档从未更新过。任何依赖它的判据都会解析到错误的 skill。

## 参考

- Issue [aria-plugin #122](https://forgejo.10cg.pub/10CG/aria-plugin/issues/122); 4 次错过机制化: v1.54.0 / v1.55.0 / v1.55.2 / v1.64.0([#113](https://forgejo.10cg.pub/10CG/aria-plugin/issues/113))
- owner 复议留痕: 主仓 `194a73b` + `.aria/config.json` `phase_c_integrator._lane`
- 规则: CLAUDE.md #8 / #10 / #6 / #3; SOT `aria/skills/phase-c-integrator/SKILL.md §C.2.4`
- 审计报告: `.aria/audit-reports/post_spec-R1-*-aggregated.md` / `post_spec-R2-*-aggregated.md`

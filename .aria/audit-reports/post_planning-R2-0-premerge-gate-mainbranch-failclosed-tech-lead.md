---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-11T00:20:00.000Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R2 — tech-lead 席位报告

**被审对象**: `proposal.md` (372 行) + `tasks.md` (116 行 / 20 checkbox) + `detailed-tasks.yaml` (550 行 / 20 task), R1-fix 后 (commit `6818773`, 换人执笔)
**席位镜头**: 架构与流程 — 任务拆解结构 / DAG 依赖语义 / ship_target 与版本口径 / 跨仓 scope 声明

## 投票

**REVISE** · verdict **FAIL** (1 Critical) · Critical 1 / Major 8 / minor 3

---

## 0. 本席位实跑的核验 (全部只读)

| 命令 | 输出 |
|---|---|
| `git submodule status` | `aria` af87cae · `aria-orchestrator` 92acce5 · `standards` 2111c84 ⇒ **`aria-plugin-benchmarks/` 不是子模块** |
| `git ls-files --error-unmatch aria-plugin-benchmarks/ab-suite/phase-c-integrator.json` | 成功 ⇒ 属主仓 Aria 跟踪 |
| `git rev-parse --short HEAD` | `6818773` (yaml 声明 `head: 98ad1f5`, 已是其祖先) |
| `grep -c '^- \[ \] \*\*TASK-' tasks.md` / `grep -c '^- id: TASK-' detailed-tasks.yaml` | **20 / 20** ⇒ 两文件已同步 |
| PyYAML 拓扑分析 | 20 task · 无环 · 无悬空依赖 · `TASK-008` 传递依赖 `TASK-010` = **False** · `TASK-015` 传递依赖 `TASK-020` = **False** |
| 合法拓扑序 (贪心) | `001→019→002→003→004→006→005→007→**008**→009→**010**→011→012→013→014→**015**→016→017→018→**020**` |
| `ls aria-plugin-benchmarks/ab-suite/ \| grep -i config` | **NONE** ⇒ 无 config-loader 套件 |
| `grep -n '"version"' aria/.claude-plugin/plugin.json` | `1.65.5` |
| `ls aria/.claude-plugin/{plugin,marketplace}.json aria/{VERSION,CHANGELOG.md,README.md}` | 5 文件全在 |
| `ls README*.md` | `README.md` `README.ja.md` `README.ko.md` `README.zh.md` |
| `grep -n badge README.md` | `:8 [![Plugin Version](...Plugin-v1.65.5-blue)]` |
| `sed -n '35p;79p;113p' CLAUDE.md` | :35「向后兼容 (破坏性变更须 MAJOR)」· :79「新增 Skill / Skill 架构重构 = MINOR+」· :113 Rule #8 — proposal 三处引用**逐字属实** |
| `git symbolic-ref --short HEAD` | `master` — proposal:328 承重腿属实 |
| `grep -nE '本项目.*master\|<MAIN_BRANCH>\|main_branch' SKILL.md` | **唯一命中 `:242`** |
| `sed -n '318,350p' pre_merge_gate.py` | `_normalize_config(config)` 在 `if not cfg["enabled"]` **之前**执行 |
| `sed -n '75p;78p' .aria/config.template.json` / `sed -n '48p;49p;285p;286p;349p;350p;351p' SKILL.md` | TASK-020 全部行锚**今日仍准确** |
| `sed -n '249p;257p' aria/skills/config-loader/SKILL.md` | 两行逐字含 "alias still works, emits DeprecationWarning, removed in v2.0" |
| `python3 -c "sum est_hours"` | **63h / 20 task**; `est_hours < 4` 的有 **12** 条 |

**对提供的地面事实的一处更正**: `verified-ground-truth.md §10` 末尾的「⚠️ `tasks.md` 无 TASK-020 checkbox ⇒ 两文件不同步 (19 vs 20)」**已过时** —— 实测 20/20，该条已在 R1-fix 中闭合。其余条目本席位抽验的部分 (`:242` 逐字 · `symbolic-ref` · 111 tests 基线口径 · `:610`/`:262`/`:559` 三行) 全部成立。

---

## Critical

### C-1 — TASK-020 的 fail-CLOSED 与 D9 / §6 / SC-M10 在**同一个输入**上要求相反结果, 且未规定插入点

**锚点**: `detailed-tasks.yaml:520-521` (TASK-020 verification) vs `proposal.md:259` (SC-M10) / `proposal.md:195` (§6) / `proposal.md:234` (D9) / `pre_merge_gate.py:325-336` 实读

三处逐字并列:

- TASK-020 (`yaml:520-521`): 「🔴 **fail-CLOSED**: v2.0 后 legacy key 在场必须发红, 不得静默忽略。**用例 = 传入含任一 legacy key 的 config ⇒ 必须发红**」
- SC-M10 (`proposal:259`): 「负控: `enabled=false` 早退 → 六键不变、**无 `gate_error`**」
- §6 (`proposal:195`): 「**在三早退之后**: 否则 owner 显式关闭的闸门与 `no_ci_fallback` 既有降级**会被变成 `fail`**」

⇒ 输入 `config = {"enabled": false, "no_aether_fallback": "skip_with_warning"}` 上, TASK-020 要求 **fail**, SC-M10 + D9 要求 **green + 六键**。两条验收都无作用域限定, Spec 未裁哪条优先。

**并且插入点结构上偏向错的那侧** —— 本席位实读 `pre_merge_gate.py:325-336`:

```
    # Alias translation BEFORE merge with DEFAULT_CONFIG (Hard Constraint #9).
    user_normalized = _normalize_config(config or {})
    cfg = {**DEFAULT_CONFIG, **user_normalized}

    if not cfg["enabled"]:
        return _build_output(verdict=VERDICT_GREEN, ...)
```

`_normalize_config()` 是 `gate_check()` 的**第一条可执行语句**, 且代码注释逐字声明它**必须**在 merge 之前 (Hard Constraint #9)。TASK-020 的 legacy-key 判定最自然的落点就是这里 ⇒ 它会在 `enabled=false` 早退**之前**发红。

本 Spec 全篇为 `_verify_branch_exists` 的插入点写了 D9 + §6 + SC-M10 三重保护, 却**给 TASK-020 的硬失败零插入点规定**。

**它在什么实现下会红**: 实施者在 `_normalize_config` 里对 legacy key 抛/返 fail ⇒ 一条 `gate_check(pr_branch="x", main_branch="master", config={"enabled": False, "no_aether_fallback": "abort"})` 的用例, 按 SC-M10 应得 `verdict=green` 六键无 `gate_error`, 实得 `fail` ⇒ SC-M10 红。反过来若实施者把判定放到 `enabled` 之后, TASK-020 那条「含任一 legacy key ⇒ 必须发红」的用例 (不指定 `enabled`) 若取 `enabled=false` fixture 则红。**两个独立实施者会得出相反结果** (memory `spec-underdetermination`)。

**为什么这是 Critical 而不是 Major**: 受影响的正是 TASK-020 自己点名的那个人群 —— 「每个新采用方都从 `.aria/config.template.json` 复制 legacy key」。他们中显式 `enabled: false` 关掉闸门的那部分，会因为一个陈旧 config key 而被 **BLOCK 每一次合并**。这直接击穿 `CLAUDE.md` 规则 #10 的 SOT 前提「enabled 闸门是 owner 的配置决定」——只是方向反了 (不是 AI 豁免闸门, 是 Spec 把 owner 关掉的闸门重新打开成阻断)。而 SC-M10 的 fixture 不含 legacy key ⇒ **整套断言对这个冲突失明**。

形状 = memory `fixes-contradict` (逐条吸收多簇 fix 后, 每条单独看都对但 A 违反 B 的隐含前提) + `feedback_fix_recurs_in_its_own_fallback_path`。

---

## Major

### M-1 — TASK-010 把「全量收口」**移交**给一个不依赖它的任务; 合法拓扑序下 TASK-008 的全量断言必红 【R1-fix 新引入】

**锚点**: `yaml:294` (TASK-010 verification #4) / `yaml:251` (TASK-008 verification #6) / `yaml:234-238` (TASK-008 dependencies)

R1 我席 M-6 指「TASK-010 的『全量 111 tests 绿』在其执行点不可达」。R1-fix 改成 (`yaml:294` 逐字):

> 本任务执行点只断言 **TG-1 范围内**测试绿; **全量收口在 TASK-008 之后**

而 TASK-008 的 `dependencies` 实测 = `[TASK-003, TASK-004, TASK-005, TASK-007]` —— **不含 TASK-010**。本席位实跑拓扑分析:

```
TASK-008 传递依赖 TASK-010? -> False
合法拓扑序: ...→006→005→007→[008 位置8]→009→[010 位置10]→...
```

⇒ 在这个**完全合法**的执行序里, TASK-008 执行「落地新 subprocess 后**重跑全量套件**」时, TASK-006 已把 `main_branch` 改必填而 TASK-010 尚未给 24 处调用补参 (地面事实 §6: 显式传 `main_branch` 的 **0** 处) ⇒ 24 条 `TypeError` ⇒ **全量套件必红**。

修复动作把一个「不可达绿」换成了另一个「视执行序而定的恒红」，而**换量时没有去被移交方核过它是否真会做这件事** —— 正是 memory `delegate-verify` 的逐字形状 (「写『由 X 保证/移交 X』前必去 X 源码核三件事」)。

**它在什么实现下会红**: 按上述拓扑序执行, TASK-008 verification #6 直接红。加一条边 `TASK-008.dependencies += TASK-010` 即闭合。

### M-2 — MAJOR 的**落地面**无任何 task 承接, 也不在 `scope_repos.paths`; TASK-020 的「v2.0」前提因此无机械保证

**锚点**: `yaml:6-33` (scope_repos) / `proposal.md:339` / `yaml:441-446` (TASK-017)

`ship_target: MAJOR` ⇒ aria-plugin `1.65.5 → 2.0.0`。CLAUDE.md「发版同步面」逐字 = **aria 子模块 5 文件 + 主仓 gitlink + 主仓 VERSION + root README badge + i18n README**。本席位实测这 5+3 个文件全部存在 (`aria/.claude-plugin/plugin.json` · `marketplace.json` · `aria/VERSION` · `aria/CHANGELOG.md` · `aria/README.md`; 主仓 `VERSION` · `README.md:8` badge · `README.{ja,ko,zh}.md`)。

实跑 `grep -niE 'plugin\.json|VERSION 文件|badge|marketplace|CHANGELOG' detailed-tasks.yaml tasks.md` ⇒ **零命中** (唯一沾边的是 `yaml:445` 那条**否定式**声明「两条 custom check 不构成机械兜底」)。proposal 全文只有 `:339`「号段落地时按 `plugin.json` 当前版本计算, 不预写字面量」。

三层后果:

1. **8 个必改文件不在 `scope_repos.paths`** —— 而该 yaml 的 `scope_notes` 自己把 scope 当权威用 (「`.aria/config.template.json` 于 2026-08-10 依 TASK-020 删除面**新入 scope**」「TASK-004 若落成新模块…**定稿时须回写本 scope**」)。同一轮 fix 为**一个**跨仓文件专门补了 scope 与「跨两个仓」声明，却漏掉**八个**同性质文件 —— memory `fix-the-class` (修实例不修类)。
2. **TASK-015 的 deliverable `aria-plugin-benchmarks/ab-results/` 也在 scope 外** —— 实测该目录属主仓 Aria 跟踪 (非子模块), 而 `scope_repos[Aria].paths` 只有 `CLAUDE.md` / `.aria/config.template.json` / `openspec/changes/.../`。
3. **最硬的一层 — TASK-020 的触发前提无人交付**: TASK-020 删除的是「v2.0 移除」这条承诺, 其正当性完全依赖版本真的走到 2.0.0。20 条任务里没有一条交付 `plugin.json` 的 bump。

**它在什么实现下会红**: Phase B 20 条全做完后跑 `grep '"version"' aria/.claude-plugin/plugin.json` 仍返 `1.65.5`, 而 legacy alias 已删 ⇒ **一个 1.65.x 版本违背了自己写在代码里的「will be removed in v2.0」**; 且 `m6-version-badge-match` (实读 `.aria/state-checks.yaml:87-101`, `enabled: true`) 在此恒绿 —— 它比的是 README badge ↔ plugin.json, 两边都没动 ⇒ **该 custom check 对这个失效方向天然 fail-OPEN**, 与 `yaml:445` 的自陈一致。

### M-3 — Rule #6 覆盖漏掉 `config-loader` 这个 skill; 且 TASK-015 排在 TASK-020 **之前** 【R1-fix 新引入】

**锚点**: `yaml:400-411` (TASK-015 deps + verification) / `yaml:506` (TASK-020 deliverables) / `proposal.md:275-281` (§Rule #6)

TASK-020 的 deliverables 实测含 **`aria/skills/config-loader/SKILL.md`** —— 这是**另一个 skill** 的 SKILL.md, 于本轮新入 scope。本席位实读该文件 `:249` / `:257`, 两行逐字是 "alias still works, emits DeprecationWarning, **removed in v2.0**", TASK-020 要改它们。

而:

- `ls aria-plugin-benchmarks/ab-suite/ | grep -i config` = **NONE** ⇒ **无 config-loader 套件**;
- proposal §Rule #6 (`:275`) 逐字「照跑 AB, **零裁量。不申请任何豁免**」, 但 `:281` 列的 ship 前置只有 `phase-c-integrator.json` + `phase-c-integrator-pre-merge-gate.json` 两个套件 —— **config-loader 既无套件、无 `rule6_note`、无 substitute SC**;
- CLAUDE.md 规则 #6 判据表第三行 (处方性·套件覆盖外) 逐字要求「点名行为 + 建可证伪定向 fixture + **套件缺口开 issue** (缺一照跑)」—— 三样一样没有, 而 TASK-019 的 6 条 follow-up 也不含这一条。

**且顺序也错**: 实跑拓扑 `TASK-015 传递依赖 TASK-020? -> False`, 合法序里 TASK-015 在位置 15、TASK-020 在位置 19 ⇒ AB 跑完之后 TASK-020 才去改 `phase-c-integrator/SKILL.md` 的 `:48/:49/:285/:286/:349/:350/:351` (本席位实读七行, 全部是 config 键的 schema 描述面)。按本 Spec 自己援引的 SOT 条款「`description` 或**指令流程变动** ⇒ 一律第二行」, 这批改动应被 AB 覆盖, 而实际产出的 `ab-results/` 对它零覆盖。

**它在什么实现下会红**: 按 DAG 执行完毕后, `ab-results/` 里的 run 对应的 SKILL.md SHA 早于 TASK-020 的提交 ⇒ 一条「AB 结果的输入 SHA == ship 的 SKILL.md SHA」断言直接红; 且 `config-loader` 侧无论跑不跑都拿不出 Rule #6 留痕。闭合动作 = `TASK-015.dependencies += TASK-020` + 为 config-loader 补 `rule6_note` 或 substitute SC (二选一, 按判据表)。

### M-4 — SC-M12 仍只挂 TASK-002 (spike), 真正 ship 的那条调用从未跨五 cwd 复跑 【R1 M-1 未闭合】

**锚点**: 本席位实跑的 SC↔task 映射 (逐 SC 正则扫 `verification` 字段):

```
SC-M12  在 verification 中的任务: TASK-002
```

写进 `SKILL.md` 的两条 helper 调用由 **TASK-011** 产出 (`yaml:296-317`), 其 5 条 verification 是 SC-M1 / SC-M3a / SC-M3b / SC-M3c / 去掉 `:240` —— **无 SC-M12**。DAG 上 TASK-011 依赖 TASK-002, 之后没有任何任务回头对**落地文本**复跑五 cwd。

R1 我席 M-1 逐字提过这条; R1-fix 把 SC-M12 从四种 cwd 扩到五种、把「模拟 plugin 安装态」的假绿 fixture 作废 —— **都在加强 spike 那一侧的断言, 没有把它移到交付侧**。这与 memory `feedback_completion_signals_vs_runtime_invocation` 同形: spike 结论正确 ≠ 抄进 SKILL.md 的那两行正确。

**它在什么实现下会红**: spike 定稿形态 X, 而 TASK-011 抄进 SKILL.md 时漏一层引号 / 少一个候选 / 把 `${CLAUDE_PLUGIN_ROOT}` 写成 `${CLAUDE_PLUGIN_ROOT:-aria}` 的错位 —— 五 cwd 参数化跑落地文本会红, 现有断言集全绿。闭合动作 = `TASK-011.verification += SC-M12 对落地文本复跑`。

### M-5 — TASK-014 的第三版验收量是**行号集合**, 与同一任务的「不得按行号核」自相矛盾 【R1-fix 新引入】

**锚点**: `yaml:369-378` = `tasks.md:68-71`

同一条任务的两条 verification 逐字并列:

- (1) 「旧形态命中集合封闭: `grep -n '${ARIA_PLUGIN_ROOT:-aria}/skills/' SKILL.md` 的命中集合**恰为 `{:610}`**」
- (⚠️) 「**行号必然位移** —— TASK-011 改动 `:99-:216` 与 `:218` 起两段 ⇒ `:262+` 全部前后移。验收一律按内容锚重定位, **不得按行号核**」

本席位实测今日命中 = `{262, 559, 610}` (SKILL.md 共 1066 行)。TASK-014 依赖 TASK-011 (实测传递依赖 = True), 故求值时 `:610` 必已位移。⇒ **按字面读, 验收 (1) 在正确实现下也永远为假 = 恒红**; 按 ⚠️ 读, 则「恰为 {:610}」得被重解释成「恰为 {降级策略那一行}」—— 而 `tasks.md:67` 逐字自称「**验收 —— 三条都不依赖裁量的量**」, 该自陈被同任务的 ⚠️ 直接推翻。

这是该验收量**第三次更换** (yaml:383-385 逐字留痕了前两次作废理由), 而第三版落在了任务自己禁止使用的单位上 —— memory `redfix-change-quantity` (修恒红别在同一个量上调阈值, 换量) 的镜像失败。

**它在什么实现下会红**: 一个完全正确的实现 (只把 `:262`/`:559` 转定稿形态, `:610` 一字不动) 跑 `grep -n` 得到 `{<某个 ≠610 的行号>}` ⇒ 验收 (1) 字面判假。闭合动作 = 把量改成「命中**条数**恰为 1, 且该条落在『**降级策略**』段」——条数与内容锚都不随位移变。

### M-6 — `SKILL.md:242` 是全文件**唯一**告知「本项目传 `master`」的一行, 落地后被折进「⛔ 不要手工执行」块, 无任务保护 【R1 M-9 未闭合, 且本轮加重】

**锚点**: `proposal.md:104` (§2 折叠范围) / `SKILL.md:242` 实读 / `yaml:318-336` (TASK-012 只保护步骤 6)

本席位实跑 `grep -nE '本项目.*master|<MAIN_BRANCH>|main_branch' SKILL.md` ⇒ **唯一命中 `:242`**, 逐字:

> **执行上下文契约**: 在执行 C.2 合并的目标仓根内调用 (子模块合并 → 子模块根); `main_branch` **显式传真值 (本项目 `master`)**, 不依赖 CLI default

`:242` 是 C.2.4 的「步骤 2.5」(实读 `sed -n '218,260p'` 确认步骤序为 1/2/2.5/3/4/5/6), 落在 §2 要整体移进 `<details><summary>…⛔ 不要手工执行 (供理解与排障)</summary>` 的 1–5 步之内。TASK-012 用整条任务保护步骤 6, **没有任何任务保护 2.5**。

**本轮把它加重了**: R1-fix 在 proposal `:77` / `:88` / yaml `:99-100` / tasks.md `:22` 四处新增了「`:242` 的作用域**限于步骤 2.5**」的更正 —— 这个更正本身是对的 (确实修掉了本项目有前科的 `:242` 误引), 但它同时把这条唯一的取值指令**明确钉进了正在被折叠的那一段**, 而没有任何一条任务把它捞出来。

与 TASK-006 (参数改必填) + SC-M3a (要求写占位符 `--main-branch "<MAIN_BRANCH>"`) + SC-M3b (禁止 `--main-branch main|master` 字面值) 三者叠加后的终态是: **AI 在折叠块外读到一条带占位符的必填参数, 而告诉它占位符取什么值的唯一句子在一个自我声明为「不要手工执行」的块里。**

**它在什么实现下会红**: 落地后跑「在 `<details>` 块**之外**存在至少一处说明 `<MAIN_BRANCH>` 取值来源的指令」这条断言 ⇒ 当前任务集下必红。闭合动作 = 给 2.5 的两条 AI 义务建一条与 TASK-012 同形的保护任务, 或在折叠块外补一行取值指引 (须同时不触发 SC-M3b)。

### M-7 — 「verification 必须能在该任务完成的那一刻求值」这条**类**未修, 在本轮重写的三条任务上复发 【R1-fix 新引入 2 例】

R1 我席 M-6/M-7 报了这个形状两次并逐字建议「A.2 统一补一条规则」。R1-fix 修了那**两个实例** (TASK-010 改口径 / TASK-008 加 test_sc22 复检), **没有补规则**, 于是本轮重写的任务上又出现三例:

| 实例 | 锚点 | 为什么在自身执行点求不出值 |
|---|---|---|
| **TASK-004** 认领 SC-M7 / SC-M8 | `yaml:147-148` vs `yaml:142-145` deliverables | 两条 SC 断言的是 **gate 层**输出 (`fail` + `kind=="main-branch-verify-failed"`)。`_verify_branch_exists` 由 TASK-008 交付, 而 TASK-008 **依赖** TASK-004 ⇒ TASK-004 完成时该代码不存在。其 deliverables 只有 `aether.py` / `test_ci_backends.py` / proposal 回写, 不含 `pre_merge_gate.py` 与 `test_pre_merge_gate.py` |
| **TASK-007** verification #1 | `yaml:223` | 逐字「核验与 in-flight 查询使用**同一个 `main_branch` 值**且**同一个 cwd**」。R1 M-5 指出上一版的「同一个 remote 值」恒绿, fix **换了量却没换求值时点** —— TASK-007 deps=`[TASK-006]`, 而「核验」由 TASK-008 建 ⇒ 该断言在 TASK-007 完成时是**空真**。且没有任何后续任务复检它 (TASK-008 的 6 条 verification 里无此项) |
| **TASK-006** 认领 SC-M9 | `yaml:206` vs `yaml:201-202` deliverables | 实跑 SC↔task 映射: `SC-M9 在 verification 中的任务: TASK-006` —— **唯一 owner**。而 TASK-006 的 deliverables 只有 `pre_merge_gate.py`, **不含 `tests/test_pre_merge_gate.py`**; TASK-001 的红窗只覆盖 SC-M1..M5。⇒ proposal:258 逐字称 SC-M9「**唯一覆盖内部调用路径**」, 而这条 SC 的测试没有任何任务的交付面装得下它。这是 R1 PC3 (Critical) 的残余 —— fix 给 TASK-008 补了测试 deliverable, 没给 TASK-006 补 |

**它在什么实现下会红**: 一条机械检查「∀task: 其 verification 引用的每个 SC, 该 SC 的被测代码/测试文件 ⊆ (本任务 ∪ 其传递依赖) 的 deliverables」在这三条上全红。

### M-8 — TASK-011 里那个被点名「须单独 spike」的未知量, 仍嵌在 L 级实现任务的 notes 里, 无 deliverable / 无 SC / 无红窗 【R1 M-8 未闭合】

**锚点**: `yaml:315-317` (TASK-011 notes) / `tasks.md:13` (组 0 定义)

notes 逐字 (与 R1 时一字未改):

> `### 步骤执行` (:99 段) 的 C.2.4 条目在 :101 开 :216 闭的 yaml 围栏内, 且该处没有「5 步」结构 ⇒ **该处改法须单独 spike**, 不得照搬 :218 段的形态。

`tasks.md:13` 自立的组织原则是「**组 0 = TDD 前置 + spike**」, TG-0 现有 TASK-001..005 五条, 无一覆盖它。这个 spike 承的是 **D1 承重面的一半** (两处散文里的第一处), 却被塞进一条 complexity=L / 6h 的实现任务的 notes。R1-fix 对 TASK-011 只动了 verification (加 SC-M3a/b/c), notes 原样保留。

**它在什么实现下会红**: 实施者在 yaml 围栏内无法表达一条「强制执行的 helper 调用」(围栏里是 `primitive 调用:` 的纯描述结构), 于是照搬 `:218` 段形态或干脆只改一处 ⇒ SC-M1 (`aether ci status` 由 4→0, 覆盖 `:167`/`:168`/`:243`/`:244` 四行) 会红, 但**红在 TG-2 的 L 级任务上, 而不是在组 0 的 spike 里** —— 这正是 owner「用 TDD 接管、让缺陷早发红」裁定要避免的。

---

## Minor

### m-1 — `proposal:113` / `:302` 的**确定式**「补一句」与 TASK-012 的**条件式**未收口, 且大概率是既定不实

`proposal:113` 逐字「**仅在其 `fail` 分支的措辞里补一句**『若 `raw_message` 含 `gate_error` 诊断则一并 surface』」, `:302` §Impact 同为确定式「步骤 6 的 `fail` 分支补一句」; 而 `yaml:333` = `tasks.md:63` 是条件式「若既有措辞已覆盖 `raw_message` 的 surface, **不加句**」。地面事实 §5 实读 `SKILL.md:255` 已含 `raw_message` ⇒ 大概率不加句 ⇒ proposal 两处确定式陈述落地即假。属 memory `feedback_spec_frontmatter_reflects_reality` 同形。

### m-2 — TASK-020 逐行枚举 7 个 SKILL.md 行号, 却没有 TASK-014 那条「行号必然位移」的护栏, 且与 TASK-011/013 同改一文件无依赖边 【R1-fix 新引入】

`yaml:512-519` / `proposal:302` 把删除面钉在 `:48 :49 :285 :286 :349 :350 :351` (本席位实读, 今日全部准确)。但 TASK-020 deps=`[TASK-006]`, 与同改 `phase-c-integrator/SKILL.md` 的 TASK-011/012/013/014 之间**零依赖边** (实测 `TASK-020 传递依赖 TASK-011? -> False`), 而 TASK-011 改动 `:99-216` 必然使 `:285+` 位移。TASK-014 为此写了整段「不得按行号核」的护栏, 同一轮 fix 里的 TASK-020 没有。缓解项: `yaml:516-517` 给了中英并列的 grep 口径, 内容可重定位, 故只判 minor。另: 同文件多任务并行改动应按 memory `workflow-file-domain` 串行化。

### m-3 — 20 条任务中 12 条 `est_hours < 4`, 低于 `CLAUDE.md:35` 逐字的「任务 4-8h 粒度」; 且 M 档内部不一致

实跑: `est_hours<4` 的 12 条 = TASK-001(2) 006(2) 007(2) 009(2) 010(3) 012(1) 013(2) 014(2) 016(2) 017(3) 018(2) 019(2); 合计 **63h / 20 task**。另 `TASK-017` complexity=**M** 而 3h, 其余 M 档均 4-5h (002=4 · 003=4 · 004=5 · 005=4 · 008=5 · 015=4) ⇒ 分档口径不一致。一条 `all(4 <= est_hours <= 8)` 的机械检查在此红。

---

## R1 的 3C + 12M 逐条回源结论

| R1 条目 | 状态 | 依据 (本席位实测) |
|---|---|---|
| **PC1** TASK-011 验收对 `--main-branch` 失明 | ✅ **闭合** | SC-M3a/M3b/M3c 三条进 TASK-001 红窗 + TASK-011 验收; `yaml:74` 另要求两个对抗 fixture, proposal:252 记载编排层已实证「两个坏实现各被 M3b/M3c 拒绝」。断言的量已换到病灶所在的量 |
| **PC2** SC 编号与既有测试全冲突 | ✅ **闭合** | 三文件全面 `SC-M*` 前缀; 逐 SC 扫描 15 个编号无一裸 `SC-数字` |
| **PC3** 组 0「先看到红」只覆盖 4/13 SC | ⚠️ **部分闭合** | 13 条 SC 现在都有 owning task (实跑映射表), 但 SC-M9 的 owner TASK-006 不交付测试文件、SC-M7/M8 的 owner TASK-004 不交付 gate 层文件 ⇒ 残余见 **M-7** |
| M `:262/:559/:610` 误引 | ✅ 闭合 | proposal `:75` 现列三项口径实测值并标注方向反了; yaml:107 同步 |
| M TASK-004 两个「⛔不得再造」不可复用 | ✅ 闭合 | D-4 裁定 + `aether.py`/`test_ci_backends.py` 入 scope 与 deliverables + 四条缺口 + 「25 tests 全绿是恒绿判据」换量 |
| M ship_target 未收敛 + MAJOR 连锁无人承接 | ⚠️ **半闭** | 抬头/D11/§版本/tasks.md/yaml 五处已统一 MAJOR ✅; 弃用到期承诺由 TASK-020 承接 ✅; 但**版本落地面**仍无人承接 ⇒ **M-2** |
| M DAG 缺 3 处语义依赖边 | ✅ 闭合 (旧的) / ❌ 新缺 2 条 | 008←007 · 011←003 · 012←009 实测在位; 但新缺 **008←010** (M-1) 与 **015←020** (M-3) |
| M TASK-005/008 接缝无人复检 | ✅ 闭合 | `yaml:251` TASK-008 verification #6 逐字含「复检 test_sc22 仍能拦真实 git 子进程」; TASK-005 #1 加了故意违规桩 (可在自身执行点求值) |
| M 多条恒绿断言 (SC-12 / TASK-007 / TASK-019) | ⚠️ 2/3 闭合 | SC-M10 补「且 assert ls-remote 未被调用」✅; TASK-019 补「每条须有可 GET 的 issue 号回填」✅; **TASK-007 换了量但没换求值时点** ⇒ M-7 |
| M-1 SC-M12 未覆盖落地文本 | ❌ **未闭** | 见 **M-4** |
| M-3 TASK-014 越出 §Impact | ✅ 闭合 | 覆盖集收到 `:262`+`:559`, `:610` 转负控白名单 + TASK-019(6); §Impact `:302` 已补该行 |
| M-5 TASK-007 转写漂移 | ⚠️ 半闭 | `remote` → `main_branch` 已改正 ✅, 求值时点问题新生 ⇒ M-7 |
| M-6 TASK-010 全量断言不可达 | ⚠️ 半闭 | 口径已改 ✅, 但移交给不依赖它的 TASK-008 ⇒ **M-1** |
| M-8 yaml 围栏 spike 无独立任务 | ❌ **未闭** | 见 **M-8** |
| M-9 `:242` 两条 AI 义务被降级 | ❌ **未闭且加重** | 见 **M-6** |
| m-1..m-5 (SC-2 红窗 / 未决陈旧 / `/skill-creator` / issue 号 / D2·D6) | ✅ **5/5 闭合** | 逐条实读确认 |

**净**: R1 的 3 Critical 中 2 条真闭合、1 条留残余; 12 Major 中 **7 条闭合 · 3 条半闭 · 2 条未闭**。R1-fix 的**方向全部正确**, 失效集中在「只修实例不修类」与「移交给没核过的下游」两个形状。

## 换人执笔是否打断了「fix 引入新 Major」的规律

**本席位口径 (三项写明)** — 总体 = 本席位 R2 的 9 条 C+M / 范围 = tech-lead 镜头 (架构·DAG·版本·跨仓 scope) / 计数法 = 逐条判 `introduced_by_r1fix`:

- 由 R1-fix 新引入: **C-1 · M-1 · M-3 · M-5 · M-7(2/3 实例) · m-2** ⇒ C+M 口径 **5 / 9 ≈ 56%**
- 对比 post_spec 五轮编排层自陈的 **73–100%**

⇒ **规律被显著削弱但未被打断。** 按 memory `feedback_audit_marginal_return_goes_negative` 的判据 (本轮 fix 引入的 major 占比 > 1/2 即到拐点), 56% 仍**在拐点之上**。

两条更具体的观察, 建议进 handoff:

1. **新引入的缺陷高度集中在本轮改动量最大的那一块** —— TASK-020 从 1 文件扩到 5 文件跨 2 仓 (yaml:546 自陈), 而 C-1 与 m-2 两条都长在它身上。「换人执笔」降低了**转写型**错误 (R1 的 `:262/:559/:610` 误引、`remote` 漂移、SC 编号冲突全部一次修净), 但对**新写大块内容**的引入率没有改善。
2. **本轮 5 条新引入缺陷里有 4 条是同一个形状** —— 「A 条款被修好, 但它对 B 的隐含前提 (依赖边 / 插入点 / 求值时点 / 交付面) 没有同步」。这不是执笔人的问题, 是**多簇 fix 逐条吸收后缺一次条款间交叉一致性扫描** (memory `fixes-contradict` 逐字预言过: 「多 agent 并行审计不覆盖它, 接缝落在角度之间」)。⇒ 处方建议不是再换人, 而是在 fix 之后加一道**机械的**交叉检查 (见下)。

## 阻塞项 (进 Phase B 前必须闭合)

| # | 项 | 闭合动作 |
|---|---|---|
| B1 | **C-1** TASK-020 fail-CLOSED × D9/SC-M10 | 裁定优先序并**写死插入点** (建议: legacy-key 硬失败落在 `enabled` 早退**之后**, 与 `_verify_branch_exists` 同档); TASK-020 的用例须显式覆盖 `enabled=false + legacy key` 这个交叉输入 |
| B2 | **M-1** DAG 缺边 | `TASK-008.dependencies += TASK-010` |
| B3 | **M-3** Rule #6 缺口 | `TASK-015.dependencies += TASK-020`; 为 `config-loader/SKILL.md` 补 `rule6_note` 或 substitute SC (按判据表二选一), 套件缺口开 issue |
| B4 | **M-2** MAJOR 落地面 | 建一条「版本 bump + 8 个同步面文件」的任务并补进 `scope_repos.paths`; `aria-plugin-benchmarks/ab-results/` 一并入 scope |
| B5 | **M-4 / M-6** D1 承重面两个网眼 | TASK-011 verification 加「SC-M12 对落地文本复跑」; 为 `:242` 的两条 AI 义务建保护任务 |
| B6 | **M-5** TASK-014 验收量 | 「命中集合恰为 {:610}」→「命中**条数**恰为 1 且落在『降级策略』段」 |

**跨条款的一次性处方 (优于逐条修, memory `fix-the-class`)**: 在 A.2 补两条机械不变量, 一次性覆盖 M-1 / M-3 / M-7 / m-2 四条 —— (i) **∀task: 其 verification 引用的每个 SC, 被测代码与测试文件必须 ⊆ (本任务 ∪ 传递依赖) 的 deliverables**; (ii) **∀两条任务改同一文件 ⇒ 必须存在依赖边** (memory `workflow-file-domain`)。这两条都是可脚本化的, 不依赖裁量。

---

## 轮次记录

| 轮 | 席位 | Critical | Major | minor | verdict | 备注 |
|---|---|---|---|---|---|---|
| R1 | tech-lead | 1 | 9 | 5 | FAIL | 审计对象 = tasks.md + detailed-tasks.yaml (19 条) |
| R2 | tech-lead | 1 | 8 | 3 | FAIL | 同席位复审 R1-fix 后三件套 (20 条)。R1 的 12 Major: 7 闭 / 3 半闭 / 2 未闭; 3 Critical: 2 闭 / 1 残余。本轮 9 条 C+M 中 5 条由 R1-fix 新引入 (56%, 前五轮为 73-100%) |

**本轮未做的事** (供后续接力): 未复核 spike 结论回写 proposal 后是否需重开 post_spec (属编排层, R1 已交 owner, 仍未答); 未核 `aria-orchestrator/` 侧的 `gate_check` 消费者 (TASK-018 口径覆盖它, 本席位未替它跑); 未评估 TASK-020 硬失败对 `no_ci_fallback: "abort"` 采用方的具体失效方向 (需仓外证据)。

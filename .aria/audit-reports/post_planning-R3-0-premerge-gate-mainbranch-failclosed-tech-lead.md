---
checkpoint: post_planning
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-11T02:00:00.000Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R3 — tech-lead 席位报告

被审对象 = R2-fix 后的 A.2 产物 (工作树 = commit `0dd26ce` 时的三件套, `git status --short openspec/` 零输出, 与 HEAD 一致)。

## 投票

**VOTE: REVISE** · **VERDICT: FAIL** (1 Critical + 6 Major + 3 minor = 10) · **blocks_phase_b: 5 条**

`introduced_by_r2fix` = **8 / 10 = 80%** (本席位口径, 见文末「量化」段的三项口径声明 — **不与 R1→R2 的 53% 直接可比**)。

---

## 一、R2 的 1C + ~13M 逐条回源

不采信「已修」的声称。回源方式: 实读现版文本 + 实跑命令 + 与 `6818773` (R1-fix 版) 做 diff。

| R2 条目 (席位) | 现状 | 判定 |
|---|---|---|
| **C1** TASK-020 fail-CLOSED 无插入点 + 信号传播 (tech-lead + backend-architect) | proposal §6.1 新增 (`:205-231`); 插入点钉在 `:328` 之后 / `:337` 之前; 三条唯一确定用例; 走 CLI 真实路径的用例; 错误文案指路; SC-M10 变体 (b) | **方向闭合, 但承重理由有一处事实错误 + 漏钉判定输入 ⇒ 见 M2** |
| **M1** TASK-010 移交不依赖它的 TASK-008 (tech-lead) | `TASK-008.dependencies += TASK-010` 实测在位 | ✅ 闭合 |
| **M2** Rule #6 漏 config-loader + TASK-015 排在 TASK-020 之前 (tech-lead) | proposal §Rule #6 新增 config-loader 归档段 (三件套全给) + `TASK-015.dependencies += TASK-019, TASK-021` (021 传递依赖 020) | ✅ 闭合 |
| **M3** MAJOR 落地面 8 文件无 task / 不在 scope (tech-lead) | TASK-017 deliverables 补 10 个真实文件 + `scope_repos` 两侧补齐 | **半闭合 ⇒ 见 M4 (漏 gitlink + 版本线混淆)** |
| **M4** SC-M12 只挂 TASK-002 (tech-lead + backend-architect + code-reviewer) | TASK-011 verification 新增「SC-M12 对落地文本复跑」+ deliverables 补 `test_pre_merge_gate.py` | ✅ 闭合 |
| **M5** TASK-014 验收量 `{:610}` 自相矛盾 + 预裁 spike 产出 (tech-lead + code-reviewer) | 第三次换量, 改为「与定稿形态 F 的相等关系」 | **换量方向对, 新量结构上不可满足 ⇒ 见 C1** |
| **M6** `SKILL.md:242` 是唯一告知「本项目传 master」的一行, 会被折进块内 (tech-lead) | 新增 SC-M16 | **新量的「今日实测」是假的 ⇒ 见 M1** |
| **M7** 「verification 须在该任务完成那一刻可求值」这一类未修 (tech-lead) | SC-M7/M8/M14 owner 由 TASK-004 移到 TASK-008; TASK-007 的断言移交 TASK-008 | **三个实例闭合, 该类在 R2-fix 自己新写的 TASK-015 条款里复发 ⇒ 见 M3** |
| **M8** TASK-011 的围栏内 spike 无 deliverable / SC / 红窗 (tech-lead) | notes 补「结论须先回写 proposal §2」+ 收口挂 SC-M1 (`:167/:168` 归零) | **半闭合 ⇒ 见 m1 (无 deliverable 承载)** |
| **M9** D9 因果断言只补 enabled=false 一条 (qa-engineer) | TASK-008 两条早退各带 `assert ls-remote 未被调用`; proposal §非目标 同步 | ✅ 闭合 |
| **M10** 「TASK-019 已纳入」承诺不成立 (knowledge-manager) | 真正写进 TASK-019 第 (7) 项, 标题改「8 项」 | ✅ 闭合 |
| **M11** metadata「不再是条件触发」与 TASK-020 矛盾 (code-reviewer) | metadata 改口「仍是条件任务, 只是条件当前为真」 | ✅ 闭合 |
| **M12** §2 把承重要求委派给量不相干的 SC-M2 (code-reviewer) | 新增 SC-M15 (折叠块内可执行命令字面量 = 0), 撤掉「须人工核」裁量腿 | ✅ 闭合 |
| **M13** 无终局收口, 唯一一次全量在 L4 (code-reviewer) | 新增 TASK-021; 实测其依赖闭包覆盖全部改被测文件的任务 (见下) | ✅ 闭合 (但引入 M5 的组序倒置) |
| **M14** SC-M9 / SC-M12 无测试交付物; **SC-M6..M13 无一条要求「先看到红」** (code-reviewer) | 前半闭合 (TASK-006 / TASK-011 deliverables 补测试文件, SC-M9 红窗入 TASK-001) | **后半未闭合 ⇒ 见 M6** |
| minor ×11 | SC-M3b 拒绝域扩 ✅ · `:557` 归类更正 ✅ · TASK-012/013 位移护栏 ✅ · TASK-005 恒真换量 ✅ · `main_branch_resolved` 删除 ✅ · ab-results 入 scope ✅ · est_hours 粒度 ❌ (见 m2) | 10/11 闭合 |

### TASK-021 是否真收口 — 实跑核验 (本席位被点名的问题)

```
$ python3 -c "…Kahn 拓扑 + 依赖闭包…"   (完整脚本见「实跑命令」段)
TASK-021 依赖闭包 ⊇ {004,005,006,007,008,009,010,011,012,013,014,020}
改被测文件的任务全集 = {001,004,005,006,007,008,009,010,011,012,013,020}
```

- `SKILL.md` 改动者 = {011,012,013,014,020} → **全在 TASK-021 闭包内**;
- `pre_merge_gate.py` 改动者 = {006,007,008,009,020} → 全在;
- `test_pre_merge_gate.py` 改动者 = {001,005,006,008,010,011,020} → 全在;
- `aether.py` / `test_ci_backends.py` 改动者 = {004} → 经 TASK-008 在;
- `config-loader/SKILL.md` 改动者 = {020} → 在;
- TASK-021 之后仍会执行的只有 TASK-015 (ab-results) / TASK-016 (CLAUDE.md) / TASK-017 (发版文件), **无一触及被 SC 断言的文件**。

⇒ **TASK-021 的收口是真的**, 这是本轮最扎实的一处修复。它引入的问题在别处 (M5 组序)。

---

## 二、本轮 findings

### C1 [critical · blocks_phase_b · **由 R2-fix 引入**] TASK-014 第三次换的验收量「两处路径表达式**逐字** == 同一个 F」结构上不可满足

**locator**: `detailed-tasks.yaml` TASK-014 verification (1) (= `tasks.md:92`)

**实读证据**:

```bash
$ cd /home/dev/Aria/aria/skills/phase-c-integrator && sed -n '262p;559p' SKILL.md
262: **Helper 实现**: `${ARIA_PLUGIN_ROOT:-aria}/skills/phase-c-integrator/scripts/pre_merge_gate.py` (stdlib + subprocess only)
559: **Helper 实现**: `${ARIA_PLUGIN_ROOT:-aria}/skills/phase-c-integrator/scripts/submodule_gate.sh` (Bash, stdlib + git only)
```

条款逐字: 「其**路径表达式逐字 == TASK-002 回写 proposal §1 的定稿形态 F**」。两处路径表达式**尾段是两个不同脚本名**, 因此它们不可能同时「逐字」等于同一个 F。

且 F 的类型与「路径表达式」不匹配 —— proposal §1 逐字把 spike 的可移植物定为「**显式优先序 + 不中即收口**」这个**结构** (援引 `submodule-gate-telemetry.sh:60-62`), TASK-014 自己的「怎么会红」也写「**少一个候选**」⇒ F 是一个多候选探测形态, 而 `:262`/`:559` 是两条单反引号 markdown 路径句。一个多候选探测**无法**「逐字」写进一条 `**Helper 实现**: \`…\`` 里。

**它在什么实现下会红 / 会分叉**:
- 实施者 A 按「逐字」执行 ⇒ 两处任一 ≠ F ⇒ **恒红**, 无论实现多正确;
- 实施者 B 把 F 重解释成「前缀相等 / 形态一致」⇒ 与条款字面「逐字」矛盾, 且该重解释无成文依据 ⇒ 判绿。
- 两个独立实施者得相反结果 (memory `spec-underdetermination`), 且这一支恰恰是**承重的 D1 落地面** (TASK-014 → TASK-019 → TASK-015 整条合规尾巴被它阻塞)。

**加重情节**: `tasks.md:99` 与 `detailed-tasks.yaml` TASK-014 notes 逐字写「**这是本任务验收量的第三次更换 —— 若第四次再来, 请优先怀疑「拿 grep 计数当验收」这个手段本身在此不适用**」。本条即第四次的触发条件已成立, 而这次连「计数」都不是, 换成了一个类型不匹配的相等关系 (memory `assertion-swap-severs-link` / `redfix-change-quantity`)。

**归因**: `git diff 6818773 878ee44 | grep -c "^+.*逐字 == TASK-002 回写"` = **1**, 删除行 0 ⇒ R2-fix 新写。

---

### M1 [major · blocks_phase_b · **由 R2-fix 引入**] SC-M16 的「今日实测 = 1」是假的; 实测 0 ⇒ 它不是守恒断言而是 baseline-failing 断言, 且无红窗

**locator**: `proposal.md:300` (SC 表 SC-M16 行) + `:110`; `detailed-tasks.yaml` TASK-011 verification SC-M16 条

**实跑**:

```bash
$ cd /home/dev/Aria/aria/skills/phase-c-integrator && grep -n -- '<MAIN_BRANCH>' SKILL.md
(零命中)
$ grep -c -E '<MAIN_BRANCH>' SKILL.md
0
$ sed -n '242p' SKILL.md
…**执行上下文契约**: 在执行 C.2 合并的目标仓根内调用 (子模块合并 → 子模块根); `main_branch` 显式传真值 (本项目 `master`), 不依赖 CLI default
```

三项口径: 总体 = `aria/skills/phase-c-integrator/SKILL.md` · 范围 = 全文件 · 计数法 = 含字面串 `<MAIN_BRANCH>` 的行数 ⇒ **0**。

SC-M16 的判据逐字是「同时含 `<MAIN_BRANCH>` **与**「本项目」或 `master` 的段落」。全文件零行含 `<MAIN_BRANCH>` ⇒ 不可能存在这样的段落 ⇒ **今日值 = 0, 不是 SC 表写的 1**。`:242` 里是 `main_branch` (小写、无尖括号), 不是 `<MAIN_BRANCH>`。

**后果三条**:
1. SC 表抬头逐字「每条 grep 断言的 pattern 与今日计数**均已实跑**」—— 本条未实跑, 是本 Spec 反复点名要根除的**自陈**类;
2. proposal 把它框成「**守恒断言** … 守的是落地后不掉到 0」, 而它今日就是 0 ⇒ 它其实是一条 **baseline-failing** 断言, 却**没有进 TASK-001 的红窗清单** (实跑: TASK-001 覆盖 `SC-M1,M2,M3a,M3b,M3c,M4,M5,M9,M17`, 无 M16);
3. 最自然的实现 ——「把 1-5 步整体折叠, 把 `:242` 那句原样留在块外」—— 按 proposal 的散文 framing 应当通过, 按 SC-M16 的字面判据仍是 0 ⇒ 红。**两个实施者相反。**

**它在什么实现下会红**: 上述第 3 条的实现; 或任何不新写一段「同时含占位符与取值来源」的实现。发现时点会被推到 TASK-021 (逐条贴 SC 实跑输出), 即全部 20 条任务做完之后。

**归因**: `grep -cE 'SC-M16' <R1-fix 版 proposal>` = **0** ⇒ R2-fix 新增。

---

### M2 [major · blocks_phase_b · **由 R2-fix 引入**] §6.1 的承重理由「两个别名键的首个消费者分别在 `:337` 与 `:339`」与代码不符, 且未钉「判定读哪份 dict」

**locator**: `proposal.md:218` (§6.1)、`tasks.md:122`、`detailed-tasks.yaml` TASK-020 「fail-CLOSED 的插入点」条

**实读** `aria/skills/phase-c-integrator/scripts/pre_merge_gate.py`:

```
101:     out = dict(config)  # shallow copy
102:     for old, new in _OLD_TO_NEW.items():
103:         if old in out:
111:                 del out[old]
120:                 out[new] = _translate_value(old, out.pop(old))
121:     return out
…
325:     user_normalized = _normalize_config(config or {})
326:     cfg = {**DEFAULT_CONFIG, **user_normalized}
328:     if not cfg["enabled"]:
337:     backend = resolve_ci_backend(cfg)
339:         return _no_ci_output(cfg["no_ci_fallback"])
```

⇒ **两个 legacy key 的首个消费者是 `:325` 的 `_normalize_config`**, 它在 `:111`/`:120` 把旧键 `del` / `pop` 掉。`:337`/`:339` 消费的是**翻译后的新键** (`ci_backends` / `no_ci_fallback`), 从不接触旧键名。§6.1 的承重理由陈述错了一层。

**真正的规格缺口**: 在被钉死的插入点 (`:328` 之后 / `:337` 之前) 上, 手边的 `cfg` **结构上不含旧键名**。§6.1 与 TASK-020 只规定了「位置」, 通篇**未规定判定的输入是未归一化的原始 `config` 参数**。读 `cfg` 是该位置最自然的写法。

**它在什么实现下会红**: 读 `cfg` 的实现对 §6.1 用例 (ii)(iii) 必红 (旧键永不命中 ⇒ 不触发硬失败 ⇒ 走到 `:339` 用翻译后的 `skip_with_warning` 放行)。⇒ 用例集**能**拒绝它, 故不构成 Critical; 但它是一次可预防的 TDD 返工, 且承重理由的事实错误恰好**掩盖**了这条必须补的规定 (memory `feedback_rationale_formula_contradiction_is_signal` 的镜像 —— 这次是理据错而公式对)。

**归因**: `git diff 6818773 878ee44 | grep -c "^+.*### 6.1"` = 1, R1-fix 版 §6.1 零命中 ⇒ R2-fix 新写。

---

### M3 [major · blocks_phase_b · **由 R2-fix 引入**] TASK-015 的 blob-SHA 验收: 命令在主仓结构上不可执行 + 断言对象在 Phase B 不可求值 (「求值时点」类在自己新写的条款里复发)

**locator**: `detailed-tasks.yaml` TASK-015 verification 第 3 条 (= `tasks.md:106`)

条款逐字: 「ab-results 里记录本次 run 对应的 `git rev-parse HEAD:aria/skills/phase-c-integrator/SKILL.md`, 并断言它**与 Phase C 落地时的同一路径 blob SHA 相等**」。

**实跑**:

```bash
$ cd /home/dev/Aria && git rev-parse HEAD:aria/skills/phase-c-integrator/SKILL.md
fatal: path 'aria/skills/phase-c-integrator/SKILL.md' exists on disk, but not in 'HEAD'
rc=128
$ cd /home/dev/Aria/aria && git rev-parse HEAD:skills/phase-c-integrator/SKILL.md
4c1fd90f60faab1821a876a8ffbcbd806fc23a08
rc=0
```

两条缺陷:
1. `aria/` 在主仓是 **gitlink**, superproject 的 tree 里没有它的子路径 ⇒ 该命令在主仓**恒 fatal(128)**。而它写的是主仓相对路径 (`metadata.path_convention` 逐字「主仓路径相对仓根」), 且 TASK-015 的 deliverable `aria-plugin-benchmarks/ab-results/` 也是主仓路径 ⇒ 读者只会在主仓跑它。正确形态见上面第二条命令。
2. 「与 **Phase C 落地时**的 blob SHA 相等」—— Phase C 是本任务 (Phase B) 完成之后的事件 ⇒ **在 TASK-015 完成那一刻不可求值**。这正是 R2/tech-lead 判为**一类**的「求值时点」缺陷 (M7), 而 R2-fix 在关闭该类的同一轮里、在自己新写的条款上原样重犯 (memory `fix-recurs-in-fallback`)。

**它在什么实现下会红**: 任何实施者照抄该命令 ⇒ fatal, 产不出断言所需的量; 或它被"完成"于 Phase C 之前而断言恒真空转。

**归因**: `git diff 6818773 878ee44 | grep -c "^+.*git rev-parse HEAD:aria/skills"` = **2**, 删除行 0 ⇒ R2-fix 新写。

---

### M4 [major · blocks_phase_b · **由 R2-fix 引入**] 发版落地面: 漏了 canonical 清单里的「主仓 gitlink」, 且把主仓 VERSION (meta-repo 独立版本线) 并入「与版本 SOT 一致」判据

**locator**: `detailed-tasks.yaml` TASK-017 deliverables + verification (= `tasks.md:111-112`); 对照 `CLAUDE.md:81`、`standards/conventions/version-management.md §4.3`

**实读 canonical 清单** `CLAUDE.md:81`:

> 发布同步面: aria 子模块 5 文件 + **主仓 gitlink** + 主仓 VERSION + root README badge + i18n README

**实跑**:

```bash
$ grep -rniE 'gitlink|子模块指针|submodule pointer' openspec/changes/premerge-gate-mainbranch-failclosed/
(零命中)
$ head -3 VERSION                → # Aria 项目版本信息 / > **版本**: 1.7.3
$ grep -m1 '"version"' aria/.claude-plugin/plugin.json  → "version": "1.65.5",
$ sed -n '8p' README.md          → [![Plugin Version](…/badge/Plugin-v1.65.5-blue)]…
$ git show --stat --oneline 7661e96   (TASK-016 自己援引的先例)
 CLAUDE.md | 24 +-
 aria      |  2 +-        ← 该先例的同一提交里**就有 gitlink bump**
 …/aria-ci-backend-abstraction/README.md | 249 +++
```

两条缺陷:

**(a) 漏 gitlink。** TASK-017 逐字自称「**8 个已知落点必须在最终清单内且实际被改**」, 而它是 canonical 五元清单的**真子集** —— 独缺 gitlink。这一项恰是 proposal 自己点名的机械失明面 (「custom check `m6-version-badge-match` 比的是 badge ↔ `plugin.json`」⇒ 对 gitlink 完全失明)。`version-management.md §4.3` 逐字「主项目版本随插件 **gitlink bump** + 文档同步滚动」⇒ gitlink 是主仓版本滚动的触发器, 不是可选项。
**怎么会红**: 落地后主仓 README badge 写 `Plugin-v2.0.0` 而 `git submodule status aria` 仍指 `af87cae` (1.65.5) ⇒ `clone --recursive` 拿到的是旧插件 (Aria #165 同族失效)。

**(b) 两条独立版本线被并成一条判据。** 主仓 `VERSION` = **1.7.3** (meta-repo 自有版本线), 插件 = 1.65.5; `CLAUDE.md` 逐字「版本 SOT = `aria/.claude-plugin/plugin.json`; 派生文件 (marketplace.json / VERSION / CHANGELOG.md / README.md) 必须与其一致」—— 这 **4 个**派生文件全在 aria 子模块内。而 TASK-017 的「怎么会红」逐字写「或 **5 个派生文件**与版本 SOT 不一致」, 落点清单里却含主仓 VERSION。
**怎么会红**: 主仓 VERSION 今天就 ≠ plugin.json 且**永远不该等于** ⇒ 该判据对它**恒红**; 或实施者照判据把主仓 VERSION 写成 `2.0.0` ⇒ 把 meta-repo 版本线从 1.7.x 直接推到 2.0.0, 一次错误落地。且「5 个派生文件」本身与 SOT 的 4 个对不上, 是又一个不可核的数。

**归因**: R1-fix 版 TASK-017 的 deliverables 只有一句「版本引用点清单」, 8 落点与 scope 全部是 R2-fix 新写 (`git diff | grep -c "^+.*8 个已知落点"` = 5) ⇒ 缺口随新枚举一起产生。

---

### M5 [major · **由 R2-fix 引入**] `task_group` 与 DAG 方向 7 处倒置, 全部由 R2-fix 新加的边造成; 而 `tasks.md` 的组标题逐字承诺了组序

**locator**: `detailed-tasks.yaml` TASK-005 / TASK-015 / TASK-021 的 `dependencies` + `task_group`; `tasks.md:16` `:58`

**实跑**:

```
✗ TASK-005(TG-0) 依赖 TASK-010(TG-1)
✗ TASK-015(TG-3) 依赖 TASK-019(TG-4)
✗ TASK-021(TG-1) 依赖 TASK-011/012/013/014(TG-2)
✗ TASK-021(TG-1) 依赖 TASK-020(TG-3)
  倒置条数: 7
```

依赖 diff (`6818773` → 现版) 显示这 7 条**全部**来自 R2-fix 新加的边:
`TASK-005 += TASK-010` · `TASK-015 += TASK-019, TASK-021` · `TASK-021` 整条新增且 `task_group: TG-1` / `parent: '1.6'`。

`tasks.md` 的组标题逐字:
- `:16` 「## 组 0 — TDD 前置 (**必须先做**, 且必须先看到红)」—— 而 TASK-005 属组 0, 拓扑实测落在 **L4**, 排在组 1 的 TASK-006/TASK-010 之后;
- `:58` 「## 组 1 — 实现 (**组 0 全绿后**)」—— 而 TASK-021 属组 1 (parent `1.6`), 却依赖组 2 的四条与组 3 的 TASK-020;
- 组 3 的 TASK-015 依赖组 4 的 TASK-019。

**它在什么实现下会红**: 执行方按 `tasks.md` 的组序推进 (这是该文件唯一给出的执行编排) ⇒ TASK-021 在组 1 执行时组 2/3 尚未发生 ⇒ 其验收「SC-M1…SC-M17 全部为期望值」必红; TASK-015 在 TASK-019 之前执行 ⇒ config-loader 的判据表第三行三件套缺第 (c) 件 ⇒ 按 Spec 自己的话「缺任一即须照跑」而「照跑结构上不可能」⇒ 死锁。执行方按 yaml DAG 推进则组标签成为噪声, 两条编排面互相矛盾。

**注**: 那道机械交叉检查**不覆盖这一族** (CHECK0 只查环与悬空依赖, 不查 group ↔ DAG 一致性)。

---

### M6 [major · blocks_phase_b · 非 R2-fix 引入] R2/code-reviewer「SC-M6..M13 无一条要求先看到红」只闭合了 SC-M9 一条; 19 条 SC 中 **10 条无红窗**

**locator**: `detailed-tasks.yaml` TASK-001 verification; `tasks.md:16`

**实跑**:

```
TASK-001 覆盖: SC-M1, SC-M2, SC-M3a, SC-M3b, SC-M3c, SC-M4, SC-M5, SC-M9, SC-M17
未建红窗:     SC-M6, SC-M7, SC-M8, SC-M10, SC-M11, SC-M12, SC-M13, SC-M14, SC-M15, SC-M16
全 yaml 中出现「红窗 / 必须 RED / 先看到红」的 task: 001, 003, 006, 011, 020
```

组 0 抬头逐字「**必须先看到红**」, TASK-001 验收逐字「**贴出实施前实跑输出证明全部 RED 项确实红** — 不接受「应该会红」的声称」。这条纪律对 10 条 SC 不成立, 其中 SC-M16 还是**今日已红却被写成守恒**的那条 (M1)。SC-M15/M16 结构上无法建红窗 (今日 0/1 即期望值), 但 SC-M6/M7/M8/M10/M11/M13/M14 都是可建的。

**它在什么实现下会红**: 一条 fixture 在断言前就走错分支的测试 (memory `test-claims-vs-verifies`) 会以「绿」交付而无人发现 —— 本 Spec 五轮里已实证过两次恒红、一次恒绿断言, 红窗正是为此设。

---

### m1 [minor · 由 R2-fix 引入] TASK-011 的「围栏内改法结论须先回写 proposal §2」无 deliverable 承载

TASK-002 / TASK-003 / TASK-004 的 deliverables 都含「spike 结论回写 proposal.md §…」, 唯独 TASK-011 的 deliverables 只有 `SKILL.md` + `test_pre_merge_gate.py`。⇒ 与 R2 抓到的「SC-M9 的断言没有任何任务的交付面装得下」是同一形状, 同轮只修了三个实例。**怎么会红**: 实施者直接改文件而不回写 §2, 无任何交付面缺失可被发现。

### m2 [minor · 非 R2-fix 引入] est_hours 粒度: R2 那条 minor 未闭合, 绝对数上升

`est_hours < 4h` 的任务: R1-fix 版 **12 / 20** → 现版 **13 / 21** (`CLAUDE.md` 逐字「任务 4-8h 粒度」)。新增的 TASK-021 也是 S/2h, 而它的验收要求逐条贴出 17 条 SC 的实跑输出 + 全量套件。

### m3 [minor · 由 R2-fix 引入] `metadata.audit_state` 把那道机械交叉检查记为已执行的质量保障, 而实测它对方向性与新实例免疫

`detailed-tasks.yaml:88-91` 逐字「fix 后强制跑机械的条款间交叉检查四项」。证据见下一节 —— 该检查对 R2 两个形状中的**方向维度**与**未预置的新实例**全部失明。把它记入 audit_state 会让下一轮读者高估这批产物已受的机械保护。

---

## 三、对那道机械交叉检查的评估 (本轮被点名要回答的四问)

基线实跑: `python3 …/xcheck.py openspec/changes/premerge-gate-mainbranch-failclosed` → `RESULT: PASS — 四项交叉检查全部通过` (exit 0)。

**验的是拒绝能力, 不是当前取值** —— 在 scratchpad 副本上构造好实现变体与坏实现各若干:

| 试验 | 构造 | 期望 | 实测 | 结论 |
|---|---|---|---|---|
| T4 | 删掉 TASK-006 的位移护栏句 (行号锚仍在) | FAIL | **FAIL** ✅ | CHECK3 有真实拒绝能力 |
| T5 | 把该句换成「本条与**内容锚**无关, 一律按 `:21/:300/:427` 三个行号逐字核」 | FAIL | **PASS** ❌ | CHECK3 只验**词是否出现**, 不验性质 —— 一句明令按行号核的句子因含「内容锚」三字而过关 |
| T2 | 删掉 SC-M6 的真 owner (TASK-008) 的那条 verification | FAIL | **PASS** ❌ | CHECK2 把**作废/否定语境**里的提及算作 owner (TASK-005 里那句「上一版第 2 条是「SC-M6/SC-M13…」…零信息量」使它成为 owner 且交付测试文件) |
| T6 | 把 TASK-017 与 TASK-020 的边**反向** (先 bump 版本号, 再执行 v2.0 删除) | FAIL | **PASS** ❌ 且打印 `TASK-017 -> TASK-020 ✓ (它依赖本任务)` | CHECK1 的判据是 `n in ANC[tid] **or** tid in ANC[n]` —— **无向**。R2 那两条 Major (TASK-010→008 / TASK-015→020) 全是**方向性**错误 |
| T7 | 新造一个插入点冲突: 给 TASK-009 加「诊断信息初始化必须放进 `_normalize_config()` 内, 在 enabled 早退之前 (与 §6.1 相反)」 | FAIL | **PASS** ❌ | CHECK4 的探测半边是**纯 print 无断言**, 断言半边是 9 条从本次 fix 抄来的硬编码字符串存在性检查 |

### 逐条回答

**1) 四项判据覆盖得住 R2 那两个形状吗? 有没有 R2 findings 属于这两形状却逃过?**

- 「只修实例不修类」: CHECK3 覆盖了**行号锚**这一个类, CHECK2 覆盖了**SC 交付面**这一个类。但 R2 的「只修实例」还包括: 因果断言只补一条早退 (M9)、位移护栏只给 014 (R1/M3)、`rule6_note` 只给一个 skill (M2) —— **四项判据没有一项能表达这些**。
- 「移交给没核过的下游」: CHECK1 只在移交对象被写成字面 `TASK-\d{3}` 时才可见, 且**无向**。本轮 M4 (发版落地面移交给一个漏项的枚举)、M3 (移交给「Phase C 落地时」这个未来事件) 两条都**属于该形状且完全逃过**。

**2) 有没有恒绿的判据?** 有, 两处:
- **CHECK4 的前半段完全无断言** —— 它只 `print` 六个插入点在三份文档里的提及次数, 任何取值都不进 `fails`。这是一个字面意义上的恒绿检查 (memory `feedback_false_green_dual_is_permanent_red` 的另一半)。
- **CHECK4 的后半段是 9 条硬编码字符串**, 全部摘自 R2-fix 自己刚写下的句子 ⇒ 它在被写下的那一刻即为真, **相对于产生它的那次 fix 是重言式**; T7 证明它抓不到任何未被预置的新冲突。

**3) 它自己是不是「只修实例不修类」的产物?** **是, 而且很典型。**
- CHECK4 逐字硬编码了 `"### 6.1"` / `"在 \`resolve_ci_backend\` 之前"` / `"含任一 legacy key 的 config"` 等本 Spec 专属串 —— 换一个 Spec 即全部失效, 换一个新插入点即失明;
- CHECK2 的 `TESTISH` 元组含 `"收口实跑输出"` —— 这是为放行 TASK-021 一个任务专门加的字面量;
- **同族里明显缺席的检查至少三项**: (i) `task_group` ↔ DAG 方向一致性 (本轮 M5, 7 处倒置全部漏检); (ii) `deliverables` ⊆ `scope_repos.paths` (R2/code-reviewer 那条 ab-results minor 的**类**; 我补跑了这一项, 现版只剩 TASK-002 一条带前缀散文的字符串未匹配, 属表述而非缺口); (iii) SC 表「今日实测」列是否回源 —— 本轮 M1 那条假值, 四项判据无一能碰到。

**4) 拒绝能力**: 见上表。**5 个构造里 4 个被放行**, 其中 T6 (方向翻转) 与 T7 (新插入点冲突) 恰好命中该检查被创建时声称要治的那两个形状。

### 结论

这道检查**不是无用的** —— CHECK0 的两层同步 (21 task / 21 checkbox / total_tasks 21) 与 CHECK3 对「删掉护栏」的拒绝是真实的机械价值, 且它在 R2-fix 当场抓到 CHECK1(6)/CHECK3(10) 这件事我采信 (那是**缺边/缺护栏**这类"有没有"的问题, 正是无向存在性检查擅长的维度)。

但把它当成「比换人执笔更接近根治」的处方**不成立**: 它的**维度**与它要治的错误的维度不匹配 —— R2 两个形状的失效都是**方向性**与**类推广性**的, 而这四项判据是**无向存在性**检查, 对方向与推广天然免疫 (memory `feedback_invariant_dimension_must_match_error_dimension` 逐字预言了这个结果)。本轮实测数据支持这个判断: 它跑绿之后, 本席位仍从同样的两个形状里找出 1C+6M, 其中 8/10 由 R2-fix 引入。

**最小可用的改法 (给下一轮执笔方, 不是本轮 finding)**: CHECK1 改成有向 (`n in ANC[tid]` 单向, 并把「它依赖本任务」单列成需要显式声明的例外); CHECK2 的 owner 判定排除作废/否定语境; CHECK3 把护栏与具体行号绑定而非按 task 布尔; CHECK4 的前半段补上断言 (同一插入点被 ≥2 条互斥条款管辖即红)。

---

## 四、量化 —— `introduced_by_r2fix`

**本席位: 8 / 10 = 80%。**

⚠️ **三项口径必须并列, 否则不可与 R1→R2 的 53% 比较**:

| | R1→R2 的 53% | 本轮本报告的 80% |
|---|---|---|
| **总体** | 5 个席位的**原始** findings 合集 | **tech-lead 单席** |
| **范围** | C + M + m 全部 30 条 | C + M + m 全部 10 条 |
| **计数法** | 各席位自报 `introduced_by_r1fix` 之和 / 30 | 逐条对 `git diff 6818773 878ee44` 回源判定 |

三项**全部不同** ⇒ 按 memory `critique-repeats-error`, **只能写「不可比」, 不能据此声称"从 53% 涨到 80%"**。可比的数须等 R3 五席聚合后按同一口径重算。

但有一件**同口径**的事可以说: 判据「本轮低于 50% 才说明那道机械检查起作用了」在本席位的样本上**没有达成**, 且第三节的拒绝能力实验给出了独立的、不依赖比例的理由 —— 5 个构造 4 个被放行。

---

## 五、阻塞 Phase B 的条目

`blocks_phase_b: true` × **5**: C1 · M1 · M2 · M3 · M4。

按 CLAUDE.md 规则 #10, AI 不得自行豁免该阻断; 亦不得以「R2-fix 已改 372 行 / 已跑机械检查」为由降级。

---

## 六、实跑命令原文 (可复跑)

```bash
cd /home/dev/Aria
# M1
(cd aria/skills/phase-c-integrator && grep -n -- '<MAIN_BRANCH>' SKILL.md; grep -c '<details' SKILL.md; sed -n '242p' SKILL.md)
# C1
(cd aria/skills/phase-c-integrator && sed -n '262p;559p' SKILL.md)
# M2
awk 'NR>=100&&NR<=121||NR>=320&&NR<=345{printf "%d: %s\n",NR,$0}' aria/skills/phase-c-integrator/scripts/pre_merge_gate.py
# M3
git rev-parse HEAD:aria/skills/phase-c-integrator/SKILL.md ; (cd aria && git rev-parse HEAD:skills/phase-c-integrator/SKILL.md)
# M4
grep -n '发布同步面' CLAUDE.md
grep -rniE 'gitlink|子模块指针|submodule pointer' openspec/changes/premerge-gate-mainbranch-failclosed/
head -3 VERSION; grep -m1 '"version"' aria/.claude-plugin/plugin.json; sed -n '8p' README.md
git show --stat --oneline 7661e96
# M5 / TASK-021 收口 / est_hours / SC 红窗 — Python 脚本, 见报告正文引用的输出
python3 /tmp/claude-1000/-home-dev-Aria/a87f33ea-9a9d-49e2-a762-18d0fd38bfc4/scratchpad/xcheck.py \
  openspec/changes/premerge-gate-mainbranch-failclosed
# 归因
git diff --stat 6818773 878ee44 -- openspec/changes/premerge-gate-mainbranch-failclosed/
```

对抗 fixture 全部落在 `/tmp/claude-1000/-home-dev-Aria/a87f33ea-9a9d-49e2-a762-18d0fd38bfc4/scratchpad/{adv,t1..t7}/`, **未改动仓内任何文件** (`git status --short openspec/` 全程零输出)。

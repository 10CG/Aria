---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-11T00:00:00.000Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R2 — code-reviewer

被审对象: `openspec/changes/premerge-gate-mainbranch-failclosed/{proposal.md, tasks.md, detailed-tasks.yaml}` (R1-fix 后; R1-fix = commit `6818773` 「换人执笔」, 其前置 `0e27f0d` 亦含部分 R1 后的修补)。

镜头 (本席): **逐字核对所有 file:line 引用是否属实 / 所有计数是否可复现且标了计数法 / 条款间是否自相矛盾**。

## Verdict

**PASS_WITH_WARNINGS** — 0 Critical + 5 Major + 6 Minor。
**VOTE: REVISE** (M2/M3 落在两条承重任务 TASK-011 / TASK-014 上, 修法各 ≤4 行; TG-0 可先行开工)。

---

## 一、R1 闭合情况 (逐条回源, 不采信「已修」的声称)

### 三条 Critical

| ID | R1 内容 | R2 判定 | 回源证据 |
|---|---|---|---|
| **PC1** | TASK-011 验收对 `--main-branch` 完全失明 (`--main-branch main` 得 0/0/2 全过) | ✅ **闭合** | 新 SC-M3a 断言 `--main-branch "<MAIN_BRANCH>"` 计数 **2**、SC-M3b 负控断言无裸 `main\|master`。把 R1 的攻击串重放: SC-M3a=0 (红) + SC-M3b=1 (红)。断言的量已换到病灶所在的量上 |
| **PC2** | SC 编号与既有测试全面冲突 | ✅ **闭合** | 实跑 `grep -rn 'SC-M' tests/` = **0**; 既有 `test_sc*` 编号实测为 `1-13,15-28`, `SC-M*` 前缀与之零交集 |
| **PC3** | 组 0「先看到红」只覆盖 4/13 条 SC | ⚠️ **部分闭合 (见 M5)** | TASK-004 deliverables 补入 `test_ci_backends.py`、TASK-008 补入 `test_pre_merge_gate.py` ⇒ SC-M6/M7/M8/M10/M11/M13 六条有了 owning deliverable。**但 SC-M9 / SC-M12 仍无测试交付物, 且「先看到红」仍只有 TASK-001 一条** |

### 十二条 Major (取 aggregate 摘出的六条 + 本席 R1 的 M1–M8)

| R1 条目 | R2 判定 | 回源证据 (实跑/实读) |
|---|---|---|
| `SKILL.md:262/:559/:610` 误引 `CLAUDE_PLUGIN_ROOT` (4 席) | ✅ **闭合且计数法已标** | `grep -n 'ARIA_PLUGIN_ROOT' SKILL.md` → `262 / 559 / 610`; `CLAUDE_` 仅 `737`。proposal:75 现写「按行数: 该文件 ARIA_ 3 / CLAUDE_ 1; 子模块 CLAUDE_ 65 / ARIA_ 5。按 occurrence: 4/1; 66/7」—— 四对数**全部实跑复现** (`git grep -c` 求和 / `git grep -o \| wc -l`, 总体=aria 子模块, 范围=git-tracked)。R1 的混口径 (66,5) 已被显式作废 |
| TASK-004 两个复用目标不可直接复用 + 唯一可行路径不在 scope (3 席, = 本席 R1/M6) | ✅ **闭合** | `scope_repos[aria].paths` 现含 `ci_backends/aether.py` + `tests/test_ci_backends.py` + `config-loader/SKILL.md` (实测 6 条); TASK-004 deliverables 含 `aether.py`; 「25 tests 全绿」已被实测证伪 (`grep -c '_run_with_retry' tests/test_ci_backends.py` = **0**, 本席复跑 = 0) 并降为必要不充分条件 |
| ship_target 多处未收敛 + MAJOR 连锁无人承接 (2 席, = 本席 R1/M8) | ✅ **闭合 (但引入 M1)** | 抬头 `:12` / D11 `:236` / §版本 `:318` / `tasks.md:5` / `yaml:35` 五处均为 MAJOR; TASK-020 已建, 删除面逐文件枚举**全部实跑复现** (见下表) |
| DAG 缺 3 处语义依赖边 | ✅ **闭合** | PyYAML 解析: TASK-008 deps 含 TASK-007 ✅ / TASK-011 deps 含 TASK-003 ✅ / TASK-012 deps 含 TASK-009 ✅; 20 task / id 唯一 / 字段数恒 12 / 无悬空依赖 / 无环 |
| TASK-005/008 接缝无人复检 (3 席) | ✅ **闭合** | TASK-008 verification 新增「落地新 subprocess 后重跑全量套件, 并复检 `test_sc22` 仍能拦真实 git 子进程」 |
| 多条恒绿断言 (SC-12 / TASK-007「同一个 remote 值」/ TASK-019 五条) | ✅ **闭合** | TASK-007 已改「同一个 `main_branch` 值且同一个 cwd」并逐字写明旧量恒绿的理由; TASK-019 新增「每条 follow-up 必须有可 GET 的 issue 编号/URL 回填本文件」; SC-M12 已由「四种 cwd」扩为「五种 cwd」且第 5 种改为真形态 |
| 本席 R1/M1 (TASK-011 不依赖 TASK-006) | ✅ **实质闭合** | 依赖边未加 (deps 仍 `[TASK-002, TASK-003]`), 但 PC1 的修法 (SC-M3a 强制占位符形态) 使执行顺序不再产生该失效 —— 无论 TASK-006 先后, SKILL.md 都必须写出 `--main-branch "<MAIN_BRANCH>"` |
| 本席 R1/M2 (TASK-015 AB 依赖漏两条改 SKILL.md 的任务) | ✅ **闭合** | `yaml:400-404` TASK-015 deps = `[TASK-011, TASK-012, TASK-013, TASK-014]` |
| 本席 R1/M3 (012/013/014 用绝对行号锚点) | ⚠️ **1/3 闭合 (见 m6)** | `scope_repos` 已补 `head: af87cae` (实测 `git -C aria rev-parse --short HEAD` = `af87cae` ✅) 且 TASK-014 已改内容锚 + 明写「行号必然位移, 一律按内容锚重定位」; **TASK-012 (`:252-255`) 与 TASK-013 (`:267/:270/:279`) 未同批改** |
| 本席 R1/M5 (TASK-014 把 `:559`/`:610` 拉回范围, 与 TASK-019(5) 冲突) | ✅ **闭合** | 覆盖集裁定为 `{:262, :559}`, `:610` + `sync-detection.md:587` 明确转 TASK-019(6); §Impact `:302` 已补「`:262`/`:559` 定位约定 (TASK-014)」 |
| 本席 R1/M7 (无全量收口任务) | ❌ **未闭合, 且被改得更弱 (见 M4)** | TASK-010 原「全量 111 tests 绿」被改为「本任务执行点只断言 TG-1 范围内测试绿; 全量收口在 TASK-008 之后」, 而 TASK-008 在拓扑 L4, 其后仍有 TASK-009 (L5, 改 `pre_merge_gate.py`) / TASK-012·TASK-013 (L6, 改 SKILL.md) |
| 本席 R1/m1 (TASK-001 漏 SC-2) | ✅ 闭合 (`yaml:64` 已列 SC-M2) |
| 本席 R1/m2 (TASK-005 第二条恒真) | ❌ 未闭合 (见 m2) |
| 本席 R1/m3 (TASK-007「同一个 remote 值」) | ✅ 闭合 |
| 本席 R1/m4 (两文件不同步 + 陈旧未决) | ✅ 闭合 —— `grep -c '^- \[ \] \*\*TASK-' tasks.md` = **20**, `grep -c '^- id: TASK-' yaml` = **20** (0e27f0d 时为 19/20); 「未决四条」已改「已裁」段 |
| 本席 R1/m5 (TASK-004「非零非 2」凿洞) | ❌ 未闭合 (见 m3) |

### 本席复跑的全部承重数 (总体 / 范围 / 计数法 三项并列)

```
# SC 表「今日实测」列 —— 逐条复跑, 8/8 一致
grep -c 'aether ci status' SKILL.md                          → 4   (Spec: 4)
grep -c '"branch": "main"' SKILL.md                          → 1   (Spec: 1)
grep -c -- '--main-branch "<MAIN_BRANCH>"' SKILL.md          → 0   (Spec: 0)
grep -cE -- '--main-branch +(main|master)([[:space:]]|$)' …  → 0   (Spec: 0)
grep -c '<details' SKILL.md                                  → 0   (⇒ SC-M3c 空真, Spec 已标注)
grep -c 'default="main"' pre_merge_gate.py                   → 1   (Spec: 1)
grep -c 'main_branch: str = "main"' pre_merge_gate.py        → 1   (Spec: 1)
grep -c -- '--main-branch main' pre_merge_gate.py            → 1   (Spec: 1)
grep -c 'default: main' pre_merge_gate.py                    → 1   (Spec: 1)

# 24 的三项口径 —— 成立
总体=tests/test_pre_merge_gate.py 单文件 / 范围=全部行 / 计数法=含 'gate_check(' 的行数
  grep -c 'gate_check(' tests/test_pre_merge_gate.py         → 24
  grep -c 'gate_check(.*main_branch' 同文件                   → 0
放宽总体到 phase-c-integrator/**/*.py, 同计数法                → 31   (Spec: 31, 去 def 为 30)

# 测试基线 —— 成立
pytest -q  → 111 passed ; 分文件 46 / 25 / 40   (Spec: 111 = 46+25+40)

# PLUGIN_ROOT (总体=aria 子模块, 范围=git-tracked)
按行数:      CLAUDE_ 65 / ARIA_ 5      (Spec: 65 / 5)
按 occurrence: CLAUDE_ 66 / ARIA_ 7      (Spec: 66 / 7)
phase-c SKILL.md 内 行数 3/1, occurrence 4/1  (Spec: 3/1, 4/1)

# TASK-020 删除面 (键名面 grep -nE 'no_aether_fallback|primitive_preference'
#                 承诺面 grep -nE 'still (readable|works)|removed in v2\.0|仍读|v2\.0 移除')
pre_merge_gate.py            6 / 2   (Spec 6/2)  行: 70,71,79,82,85,89 | 68,116
phase-c-integrator/SKILL.md  6 / 4   (Spec 6/4)  行: 48,49,285,286,350,351 | 49,285,286,349
config-loader/SKILL.md       2 / 2   (Spec 2/2)  行: 249,257
tests/test_pre_merge_gate.py 17 / 3  (Spec 17/3)
.aria/config.template.json   2 / 0   (Spec 2/0)  行: 75,78
⇒ SKILL.md 两面并集 = {48,49,285,286,349,350,351} = 7 行, 与 §Impact:302 的「7 行」逐字一致 ✅

# TASK-014 v1 的今日命中集合
grep -n -F '${ARIA_PLUGIN_ROOT:-aria}/skills/' SKILL.md → {262, 559, 610}   (Spec: 同)
```

### 逐行实读命中的引用 (全部属实, 无一条落空)

`SKILL.md`: `:99`(### 步骤执行) `:101`/`:216`(yaml 围栏开闭) `:167` `:168` `:189-191`(三条裸 git) `:218`(### C.2.4) `:240`(`aether --help | grep -q`) `:242`(作用域=步骤 2.5) `:243` `:244` `:252-255`(步骤 6, `:255` = fail→raw_message) `:259`(重试 5/15/45×3) `:260`(127→no_ci_fallback) `:267` `:270` `:279`(逐字四类早退) `:285` `:286` `:310` `:349` `:350` `:351` `:392` `:557` `:559` `:610` `:737` `:742`
`pre_merge_gate.py`: `:21` `:56` `:68` `:70-71` `:79` `:82` `:85` `:89` `:116` `:298`(def) `:300` `:328` `:338` `:344` `:345` `:356` `:357` `:358` `:366` `:427` `:435`
其它: `aether.py:38/:164/:168/:176/:180/:187` · `path_coverage.py:78/:93` + `:78-84` bytes+surrogateescape docstring · `ci_backends/__init__.py:17` · `github_actions.py:37-42`(逐字含 "set ci_backends: [] …") · `workflow-runner/SKILL.md:354-357`(逐字四条臂) · `gate_state_helper.py:32-34/:115/:147` · `test_pre_merge_gate.py:663`(逐字 `main_branch="main"`)/`:710` · `state-scanner/references/sync-detection.md:587` · `CLAUDE.md:35/:79/:113` · `.aria/config.template.json:75/:78` · `plugin.json` version = `1.65.5` ⇒ MAJOR = v2.0.0 · `grep -rn 'gate_error' aria/` = **0**

**⇒ 本轮在「引用属实 / 计数可复现 / 计数法标注」这三项上, 本席未找到任何一处失实。** 这与 R1 的画像 (4 席独立命中同一处误引、混口径计数) 是质变。

---

## 二、Major

### M1 — `yaml:41` 逐字「TASK-020 **不再是条件触发**」与同文件 `:496`/`:543` 及 `tasks.md:83`/`:107` 直接矛盾 (R1-fix 新引入)

**四处逐字**:

| 位置 | 逐字 |
|---|---|
| `detailed-tasks.yaml:41` | 「… ⇒ TASK-020 **默认生效 (不再是条件触发)**。」 |
| `detailed-tasks.yaml:496` | `title: v2.0 弃用到期承诺的承接 (条件任务 — 仅当 ship_target 确认为 MAJOR; 条件已于 2026-08-10 满足)` |
| `detailed-tasks.yaml:543` | 「⚠️ 本任务**条件触发** — ship_target 若最终不是 MAJOR 则整条 cancelled, 须在本文件留痕而非静默删除」 |
| `tasks.md:83` | 「⚠️ **条件性不得抹掉**: 若 `ship_target` 在 handoff 复议中被改档, 整条 **cancelled 并在本文件留痕**, 不得静默删除。」 |

**归属实证**: `git diff 0e27f0d 6818773 -- detailed-tasks.yaml` 中该行以 `+` 出现 (diff 第 39 行), 而 `:543` 是 context 行 ⇒ **矛盾由 R1-fix 那一轮新造**。

**它在什么实现下会红**: `ship_target` 目前是 **AI 依 owner 授权作出的裁定**, 三份文件都逐字写着「须写入 handoff 请 owner 复议」(Rule #10 留痕)。复议若改档为 MINOR, 读 `metadata.ship_target` 的执行者会保留 TASK-020 (「不再是条件触发」), 读 `TASK-020.verification` 的执行者会 cancel 它 —— 两个独立执行者对同一输入得相反结果, 正是 memory `spec-underdetermination` 的判据形状。而 TASK-020 是 **L/6h、跨两个仓、5 个文件**的最大单条任务。

**修**: `yaml:41` 删「(不再是条件触发)」, 改为「⇒ TASK-020 触发条件当前满足; 条件性保留, 改档则整条 cancelled 并留痕」。

---

### M2 — TASK-014 验收第 1 条**预先裁定了 TASK-002 spike 的产出**, 与三处「变量归属是 spike 的产出不是输入」直接矛盾; 特定 spike 结论下该验收**恒红** (R1-fix 新引入)

**逐字对照**:

- `yaml:369-370` (= `tasks.md:68`): 「旧形态命中集合封闭: `grep -n '${ARIA_PLUGIN_ROOT:-aria}/skills/' SKILL.md` 的命中集合**恰为 `{:610}`**。今日实测 = `{:262, :559, :610}` ⇒ 实施前必红; 只改一处、**或别处新增一条旧形态, 亦红**。」
- `proposal.md:92`: 「变量归属是 spike 的**产出**, 不是它的输入 —— 本 Spec 与 `tasks.md` 均**不预先定死**」
- `tasks.md:24`: 「**变量归属 (`ARIA_` vs `CLAUDE_`) 是本 spike 的产出, 不是它的输入** —— 本文件与 proposal 均不预先定死」
- `yaml:97-98`: 同上

**归属实证**: `git diff 0e27f0d 6818773` 中该验收以 `+` 出现 ⇒ R1-fix 新写。

**它在什么实现下会红**: TASK-014 v1 把 `${ARIA_PLUGIN_ROOT:-aria}/skills/` 定义为「旧形态」并要求它在实施后**只剩 `:610`**。这等价于**禁止** TASK-002 产出任何含该字面量的定稿形态。而:
1. `proposal.md:69` ⛔ 只禁止「把 `CLAUDE_PLUGIN_ROOT` 降为非承重」, **不禁止** 定稿形态保留 `ARIA_` 作为候选之一;
2. 仓内已 ship 的先例 `aria/hooks/submodule-gate-telemetry.sh:60-62` 正是「环境变量优先 → 失败则自定位 → 仍不中即不执行」的**多候选**形态;
3. `aria/CHANGELOG.md:2796` 记载 `:262`/`:559`/`:610`/`sync-detection.md:587` 是 v1.15.2 **按同一意图一次拉平**的等价类。

⇒ 若 spike 定稿为「多候选探测, 候选之一保留 `${ARIA_PLUGIN_ROOT:-aria}/skills/…` 以兼容既有等价类」——一个完全合规且有先例支撑的结论——则 `:262`/`:559`/两条新增调用都会携带该字面量, **命中集合永远不可能收敛到 `{:610}`**, TASK-014 转为**恒红**。这正是本 Spec 已发生过两次的形状 (memory `false_green_dual_is_permanent_red` / `redfix-change-quantity`), 而 TASK-014 的验收量已被换过**两次**, 这是第三次。

**修**: 把 v1 改成**相对于 spike 产出**的量, 例:「令 `F` = TASK-002 定稿形态字面量。断言 (a) `grep -F "$F" SKILL.md` 命中集合 ⊇ `{:262, :559}` 且各恰 1; (b) 若 `F` 不含 `${ARIA_PLUGIN_ROOT:-aria}/skills/`, 则该旧字面量的命中集合恰为 `{:610}`; 若含, 则断言 `:610` 内容锚 diff 为零改动」。

---

### M3 — `proposal.md:107` 把承重要求「去掉全部可执行命令字面量」委派给 **SC-M2**, 而 SC-M2 的量与命令字面量无关; 同一份 yaml 自陈该要求「须人工核」

**逐字**:
- `proposal.md:107`: 「折叠块**不是**保护机制 …… 真正的保护是**去掉命令字面量** (**SC-M2 钉住**)。」
- `proposal.md:247` (SC 表): 「**SC-M2** \| `grep -c '"branch": "main"' .../SKILL.md` \| **0** \| **1** \| 必红 (`:270`)」
- `yaml:314` (TASK-011 verification): 「去掉全部可执行命令字面量 — 含 `:240` 的 `aether --help | grep -q` (**SC-M1/M2 两条 pattern 都不命中它, 须人工核**)」

**实读 `SKILL.md:270`**: `{"run_id": 3161, "branch": "main", "started_at": …}` —— 这是 in-flight **输出**示例, 不是命令字面量。实跑 `grep -c '"branch": "main"' SKILL.md` = 1, 唯一命中即 `:270`。

**它在什么实现下会红**: 构造实现 —— 两处散文各写一条 `--main-branch "<MAIN_BRANCH>"` 占位符调用, 5 步移入 `<details>` 折叠块, 但**保留** `:240` 的 `aether --help | grep -q "in-flight"` 以及任何非 `aether ci status` 形状的可执行字面量。实测该实现: SC-M1=0 ✅ SC-M2=0 ✅ SC-M3a=2 ✅ SC-M3b=0 ✅ SC-M3c=0 ✅ —— **五条全绿, 而 §2 的承重要求被违反**。全 13 条 SC 里没有任何一条断言「折叠块内零可执行命令字面量」。

这是 memory `delegate-verify` 的形状 (写「由 X 保证」前必去 X 核三件事), 且 SC 号本身也引错 (最接近的是 SC-M1, 但它只覆盖 `aether ci status` 四行)。承重任务 TASK-011 的验收因此有一条落在**裁量**上, 而本 Spec 的 SC 表抬头逐字写着「SC-M1..SC-M5 **零裁量**」。

**修**: `proposal.md:107` 改引 SC-M1 并限定范围 (「SC-M1 钉住 `aether ci status` 四行; 其余命令字面量由 TASK-011 新增 SC-M14 钉住」), 并补一条机械 SC: 「提取 `<details>…</details>` 区间, 断言其中 ` ``` ` 代码块数 = 0 且不含 `aether ` / `python3 ` / `git ` 起首行」。

---

### M4 — 唯一一次「重跑全量套件」在拓扑 **L4**, 其后仍有 4 条任务改被测文件; 全清单**无终局收口** (R1/M7 未闭合, 且 R1-fix 把它改得更弱)

**实读**:
- `yaml:251` TASK-008 verification: 「**落地新 subprocess 后重跑全量套件**, 并复检 `test_sc22` …」
- `yaml:294` TASK-010 verification: 「本任务执行点只断言 **TG-1 范围内**测试绿; **全量收口在 TASK-008 之后** (⚠️ 上一版写「全量 111 tests 绿」…)」

**实跑拓扑排序** (PyYAML + Kahn): `L4 = {TASK-008, TASK-014}` · `L5 = {TASK-009, TASK-016}` · `L6 = {TASK-012, TASK-013}` · `L7 = {TASK-015}`。

**它在什么实现下会红**: TASK-009 (L5) 交付物逐字是 `scripts/pre_merge_gate.py` —— 它在**唯一一次全量套件复跑之后**改生产代码; TASK-012/TASK-013 (L6) 与 TASK-014 (L4) 改 `SKILL.md`, 而 SC-M1/M2/M3a/M3b/M3c 五条断言**就是对 `SKILL.md` 做 grep 且住在 `test_pre_merge_gate.py` 里**。任何在 L4 之后引入的回归 (例: TASK-013 把 `:267` schema 示例写成 `"branch": "main"` —— `proposal.md:216` 自己逐字警告过这个对撞; 例: TASK-012 给步骤 6 `fail` 分支补的那句里带进命令字面量) **无任何任务会重新跑到它**。TASK-015 (L7) 虽在最下游, 但其 verification 只有 AB 三条, 不含测试套件。

R1-fix 把 TASK-010 的全局断言删掉并转指 TASK-008, 而 TASK-008 拓扑上更早 ⇒ 这一改**扩大**了缺口。

**修**: 新增 TASK-021 收口 (deps = `[008,009,010,011,012,013,014]`), verification = 「`pytest tests/ -q` 全绿且计数 == 111 + 本 change 新增数」+「SC-M1..SC-M13 逐条复跑贴输出」。

---

### M5 — R1/PC3 残留: **SC-M9 与 SC-M12 无任何测试交付物**; SC-M6..M13 无一条要求「先看到红」

**实跑** (对 yaml 做 deliverables 反查):
- `TASK-006.deliverables` = `['aria/skills/phase-c-integrator/scripts/pre_merge_gate.py']` —— 而 `TASK-006.verification` 逐字含「**SC-M9**: `gate_check(pr_branch=…)` 不传 `main_branch` ⇒ `TypeError`」。断言 SC-M9 的那条**测试**没有交付物;
- `TASK-002.deliverables` = `['spike 结论回写 … proposal.md §1']` —— 而 `TASK-002.verification` 逐字含「**SC-M12**: 五种 cwd 全部可达」。SC-M12 需要**五种 cwd 的参数化 fixture**, 其中第 5 种逐字是「采用方仓根 (有 `.aria/`、无 `aria/` 无 `skills/`, 插件装在仓外)」—— 这是本清单里**最重的测试基础设施**, 却零交付物、零红窗、零文件路径;
- `TASK-001` 是**唯一**带「贴出实施前实跑输出证明全部 RED」的任务, 其覆盖面逐字只有 SC-M1/M2/M3a/M3b/M3c/M4/M5 (grep 面)。

**它在什么实现下会红**: SC-M12 的红窗缺失恰是本 Spec 已两次踩中的坑 —— `proposal.md:96` 逐字记录上一版的「模拟 plugin 安装态」fixture 被取成 cwd = marketplace 目录本身,「候选 1 直接命中, 是一个**假绿且不对称**的 fixture」。**同一条 SC、同一种失效方式已经发生过一次**, 而现在它仍然没有 owning deliverable 与红窗要求 ⇒ 第二次以同样方式假绿时无机制发红。

**修**: 组 0 补一条任务, deliverable = `tests/test_pre_merge_gate.py` (+ SC-M12 的 fixture 目录), 内容 = SC-M9/SC-M12 空壳 + 贴实施前红输出; 并把 TASK-008/TASK-004 的 SC 验收改为「由红转绿, 且 diff 显示测试先于实现提交」。

---

## 三、Minor

### m1 — `TASK-015.deliverables` = `aria-plugin-benchmarks/ab-results/` 不在任何 `scope_repos.paths` 内
实跑集合差 (deliverables 对 scope 前缀匹配): 唯一一条「是真实仓内路径却未被 scope 声明」的是 TASK-015。`git ls-files aria-plugin-benchmarks/ | wc -l` = **1772** ⇒ 它是**主仓 tracked 目录**, 不是子模块 (`.gitmodules` 只有 standards / aria / aria-orchestrator)。`scope_repos[Aria].paths` 现为 `CLAUDE.md` / `.aria/config.template.json` / `openspec/changes/…/`。§Impact 有「AB \| 两套件照跑, 结果存 `ab-results/`」行, 故是 yaml 漏声明而非整体遗漏。**与 R1/M6 (aether.py 不在 scope) 同形** —— 修实例未修类。

### m2 — `TASK-005` 验收第 2 条仍恒真 (R1/m2 未闭合)
逐字「SC-M6/SC-M13 能用真实 git 受控裸仓运行, **不被该守卫误拦**」。实读 `tests/test_pre_merge_gate.py:718-723`: `test_sc22` 的 `mock.patch.object` 是**单个测试方法内的 `with` 块**, 结构上不可能影响别的测试方法 ⇒ 任何实现都满足该条。承重的是第 1 条 (「用一个故意违规的桩验证它会红」), 那条是好断言。

### m3 — `TASK-004` 验收「**非零非 2** 退出码」仍在 catch-all 上凿洞 (R1/m5 未闭合), 且与新增的 ⛔`--exit-code` 禁令语义重叠未对齐
`yaml:147` 逐字「SC-M7: **非零非 2** 退出码 … ⇒ fail + `verify-failed`, 未重试」, 而 `proposal.md:157-159` 的表逐字以「**其余一切**」收口并明写「不是正向枚举」。`2` 只在用 `--exit-code` 时产生, 而 `proposal.md:149` 现已 ⛔ 明禁 `--exit-code` ⇒「非 2」这半句把一个已被禁的实现假设又带回来了。

### m4 — `SKILL.md:557` 被两处归类为「skill 目录相对」的 **helper 定位形态**, 实读该行与 helper 定位无关
`tasks.md:74` / `yaml:383` (4 套形态枚举) 与 `tasks.md:95` / `yaml:484` (TASK-019(6) issue 正文要求) 均写「`:392` `:557` (skill 目录相对)」。实读 `:557` 逐字: 「v1.28.0 ships workflow as `on: workflow_dispatch` only; tripwire periodic execution migrated to **host-cron** …; standalone `scripts/submodule-tripwire-audit.sh`」—— 那是 **tripwire 独立脚本**的迁移记述, 不是 gate helper 的定位约定。**它在什么实现下会红**: TASK-019(6) 的 issue 正文按此逐字枚举后, 任何读者点开 `:557` 都会发现枚举错项 —— 而该 issue 正文的精度要求被 `yaml:487-488` 逐字提到「不得含糊成『风格不统一』」的高度。(留在 TASK-014 负控白名单里作「零改动」要求本身无害。)

### m5 — SC-M3b 的负控声称「写死字面值的实现在此必红」略强于其正则的拒绝域
`proposal.md:249` 逐字「**负控**: 写死字面值的实现在此必红」。实测该正则 `--main-branch +(main|master)([[:space:]]|$)` 对 `--main-branch "master"` (带引号) **不命中**。主路径仍被 SC-M3a 兜住 (占位符计数会掉到 0 ⇒ 红), 故只在「额外多写一条带引号的写死示例」时逃逸。建议正则补 `["']?` 或把声称改为「裸字面值」。

### m6 — TASK-012/TASK-013 的验收锚点仍是 TASK-011 会位移的绝对行号 (R1/M3 只修了 1/3)
`yaml:332` 「步骤 6 (**:252-255**) 仍在折叠块外」· `yaml:340/:351-353` 「`:267` schema 含 `gate_error`」「`:279` 早退注记逐字仍是四类」。TASK-011 逐字要重整 `:99-:216` 与 `:218` 起两段并插入折叠块 ⇒ `:252+` 必然整体位移。TASK-014 已获得「内容锚 + 一律按内容锚重定位」的处置, 同一 R1 finding 的另两个实例未同批处理 (memory `fix-the-class`)。实际风险偏低 (「步骤 6」「枚举归层注记」本身即内容锚), 故列 Minor。

---

## 四、阻塞项 (本席认为进 Phase B 前应清)

| # | 条目 | 理由 | 修法规模 |
|---|---|---|---|
| B1 | **M2** — TASK-014 v1 恒红风险 | 落在承重任务, 且形状与本 Spec 已发生两次的恒红同款 | 改 1 条 verification |
| B2 | **M3** — §2 委派给不相干的 SC | 落在**最承重**的 TASK-011 (D1), 使承重要求退回裁量 | 改 1 句 + 加 1 条 SC |
| B3 | **M1** — TASK-020 条件性自相矛盾 | Rule #10 复议尚未发生, 改档路径当前是**双读双结果** | 删 6 字 |
| B4 | **M4** — 无终局收口 | L4 之后 4 条任务改被测文件而无人复跑 | 加 1 条任务 |

M5 / m1–m6 不阻塞 TG-0 开工。

---

## 五、对本轮问题的直接回答

**1. R1 的 3C + 12M 真的闭合了吗** —— 3 Critical: **2 闭合 (PC1/PC2)**, 1 部分闭合 (PC3 → 8 条孤儿 SC 降到 2 条, 但红窗纪律未扩展)。12 Major: **9 闭合、1 部分闭合 (R1/M3)、2 未闭合 (R1/M7 + PC3 残留)**。5 Minor: 3 闭合 / 2 未闭合。**所有「已修」的声称本席均回源实跑, 未发现纸面修复。**

**2. R1-fix 是否引入新缺陷 / 换人执笔是否打断了规律** —— 本席 R2 共 5 Major, 其中 **2 条 (M1, M2) 由 R1-fix 新引入 = 40%**。post_spec 五轮的实测区间是 **73–100%**。40% 已跌破 memory `marginal-return-negative` 给出的拐点判据 (「本轮 fix 引入的 major 占比 > 1/2 即到拐点」)。**⇒ 换人执笔在本轮打断了该规律。** 另一个更硬的旁证: 本席的镜头 (引用属实 / 计数可复现 / 计数法标注) 在 R1 抓到 4 席共同命中的方向性误引 + 混口径计数, 本轮**逐条复跑 30+ 处引用与 20+ 个数, 零失实**。

**3. 恒红 / 恒绿 / 空真** —— 找到 **1 条恒红风险 (M2, 条件性)** · **1 条恒真 (m2, R1 遗留)** · 空真已被正确标注 (SC-M3c 的「今日 0 是空真, 不得当正面证据读」同时出现在 `proposal.md:250` 与 `yaml:67-70`, 且其拒绝能力已由 `proposal.md:252` 的三 fixture 对抗验证覆盖)。另确认 R1 点名的两条恒绿 (「25 tests 全绿」/「同一个 remote 值」) 均已换量。

---

## 轮次记录

| 轮 | 席位 | 结论 | Critical | Major | Minor | 其中 fix 新引入 |
|---|---|---|---|---|---|---|
| R1 | code-reviewer | FAIL | 2 | 8 | 5 | — |
| R2 | code-reviewer | PASS_WITH_WARNINGS | **0** | **5** | 6 | **2 / 5 = 40%** |

**R2 说明**: 本席全部 finding 基于实跑命令或逐字实读, 无一条基于推断; 所有引用行在报告中给出命令原文或逐字内容。采信了主 loop 的 `verified-ground-truth.md` 与 `adjudication-draft.md`, 并对其中 §2 / §5 / §6 / §10 / §12 / §14 的关键数据做了独立复跑 —— 全部成立, 未发现该两份文件有误。

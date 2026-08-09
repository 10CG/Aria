---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-09T03:20:58.018Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R4 — tech-lead 席位报告

被审对象: `openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md` (263 行, R3-fix 范围重定版)
镜头: 架构与流程 — D1–D9 自洽性 / 条款间交叉一致性 / §非目标↔§Impact 边界 / Rule #6 定档 / §版本悬置正当性 / 与 #136 #137 Rule #8 SOT 的关系

---

## 审计结论

**承重项 D1 的方向是对的** —— R3 挖出的「两份实现, AI 走没被加固的那份」是真结论, 我独立复核了它的三个事实基础, 全部成立:

| R3 事实 | 我的独立复核 | 结果 |
|---|---|---|
| `§C.2.4` 标题逐字「执行流程」, 步骤 1-5 是裸命令 | `SKILL.md:238-255` 实读 | ✅ 成立 |
| 全文「同行含 `python3` 与 `--main-branch`」= 0 | `grep -cE 'python3.*--main-branch\|--main-branch.*python3'` = 0 (GNU grep 3.8 + ugrep 7.5.0 双跑) | ✅ 成立 |
| `pre_merge_gate.py` 在 SKILL.md 出现 4 次 (`:262`/`:308`/`:310`/`:316`) 均无带参示范 | 逐行实读 | ✅ 成立 |
| helper 侧 `main` 三处 + 24 处 `gate_check(` 零显式传参 | `default="main"` 1 / `main_branch: str = "main"` 1 / `--main-branch main` 1 / `default: main` 1; 24 处调用点, AST 邻域扫描确认 0 处传 `main_branch` | ✅ 成立 |
| 测试基线 111 (46+25+40) | 逐文件 `grep -c '    def test_'` | ✅ 成立 |
| `gate_state_helper.py:32-34` 封闭枚举 / `:147` 原样写入 / `base.py:29` `not_found` | 实读 | ✅ 成立 |

**但 D1 这个新表面本身带进了三个 Critical**, 且都落在「前三轮从未审过」的那块地上。核心问题可以一句话概括:

> **D1 提出了三项结构要求 (① 唯一 helper 入口 ② 5 步去命令字面量 ③ 占位符统一), 只有 ① 有一条机械断言 (SC-3), 而那条断言按 Spec 自己给的逐字命令**恒红**; ② ③ 零断言; 与此同时 `:166-169` 那处同形的裸命令清单被明确降级为「只换字面量」处置 —— 而 Spec 自己在 `:37` 刚论证过「只换字面量没用」。**

即: **承重项的完成度既无法机械验证, 又在 Spec 自己的 Impact 表里被写小了**。这是典型的「条款间交叉一致性」失效 —— D1 单看对, §Success Criteria 单看严, §Impact 单看诚实, 但三者拼起来时 D1 的合格线掉在了缝里。

另有 6 条 Major, 集中在两个类:
- **委派未核验类 (3 条)**: 「由 SC-10 机械钉住」/「`_OLD_KEYS` 守护测试」/「先例 `:737` 本条沿用」—— 三处都去被引用方实测了, 三处都不做它被声称做的事;
- **同步面漏项类 (3 条)**: 折叠块少一步 / 步骤 6 归属未定义 / CLAUDE.md Rule #8 不在任何枚举口径里。

**Verdict: FAIL (3 Critical + 6 Major + 4 Minor)。** 这是 `max_rounds=4` 最后一轮, 我对「什么阻塞 Phase B」的判断写在 §Verdict 末尾的**准入清单**里 —— 只有 4 项必须在进 Phase B 前落到 Spec, 其余可在 A.2 任务分解时吸收。

---

## Critical

### C-tl-1 · 唯一执行入口用了一个**从不会被自动设置**的环境变量, 且 D1 没有为「helper 不可达」定义任何 fail-closed 行为

**锚点**: proposal.md `§What Changes 1` (:69-72 逐字命令块) · `SKILL.md:737` (被引先例) · `SKILL.md:242` (cwd 契约)

Spec 的唯一执行入口逐字是:

```bash
python3 "${ARIA_PLUGIN_ROOT:-aria}/skills/phase-c-integrator/scripts/pre_merge_gate.py" \
  --pr-branch "<PR_BRANCH>" --main-branch "<MAIN_BRANCH>" --remote origin
```

而它自称的先例 (`:74`「**先例**: `SKILL.md:737` 已有同形的强制 helper 调用范式, 本条沿用」) 实读是:

```
SKILL.md:737  python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/aria-token-telemetry/scripts/token_telemetry.py" --project-root .
```

**两者用的不是同一个变量**, 而这恰恰是承重的那一位:

| | `CLAUDE_PLUGIN_ROOT` | `ARIA_PLUGIN_ROOT` |
|---|---|---|
| 谁设置 | Claude Code plugin harness 自动注入 (**本次会话内实证**: PreToolUse hook 以 `bash ${CLAUDE_PLUGIN_ROOT}/hooks/secret-guard.sh` 成功执行) | 无人。全仓 `grep -rn 'ARIA_PLUGIN_ROOT='` = **0 命中**; `.claude/settings.json` 无 `env` 键; 用户级 settings 的 env 只有 4 个代理/超时键 |
| live plugin 内用量 | 39 处 | 4 处 (全在 phase-c-integrator SKILL.md + sync-detection.md) |
| 实际语义 | 安装路径 | **恒等于 fallback `aria`** (相对 cwd) |

⇒ 逐字命令**必然**退化成相对路径 `aria/skills/...`。而 `SKILL.md:242` 的执行上下文契约逐字要求「在执行 C.2 合并的目标仓根内调用 (**子模块合并 → 子模块根**)」。受控实测:

```
cwd=/home/dev/Aria       test -f "${ARIA_PLUGIN_ROOT:-aria}/skills/.../pre_merge_gate.py"  → OK
cwd=/home/dev/Aria/aria  同上                                                              → MISSING
```

**本 change 自己就落在 `aria/` 子模块**, 且按 CLAUDE.md 硬约束 1「子模块合并一律本地做」, 它自己的 Phase C 就会撞上 MISSING 这一格。

真正致命的不是路径, 是**没有失败契约**。D1 同时做了两件事: (a) 宣布 helper 是**唯一**执行方式; (b) 把折叠块里的 5 步**去掉全部可执行命令字面量**并标注「⛔ 不要手工执行」。于是当 `python3` 返回 `can't open file` 时, AI 手上是: 一条跑不通的唯一入口 + 一份被明令禁止且已被抽掉命令的兜底。Spec 全文 (263 行逐行读过) **没有一句**规定此时该怎么办。两种自然结局都不 fail-closed:

1. AI 自行重构命令 → 回到 R3 要治的裸命令路径, 且因为折叠块已去字面量, 它重构出的版本比今天更不可靠;
2. AI 判定「gate 跑不了」→ 静默跳过 → **Rule #8 的静默降级**, 而 CLAUDE.md Rule #8 逐字只授权了两条降级 (`no_ci_fallback` / stub-NIE abort), 「helper 不可达」不在其中。

这就是把一个「恒绿的 gate」换成「一个新的静默降级向量」, 与本 Spec 存在的理由直接冲突。

**修法 (Spec 层, 三句话)**: (i) 逐字命令改用 `${CLAUDE_PLUGIN_ROOT}` 与 `:737` 真正对齐 (或显式写死解析顺序 `CLAUDE_PLUGIN_ROOT → ARIA_PLUGIN_ROOT → 相对`), 并说明 cwd 必须是合并目标仓根而脚本路径必须是插件根; (ii) 增加一条 D 决策: **helper 不可达/非零退出 ⇒ `verdict=fail`, 禁止手工重构命令、禁止跳过**; (iii) 增加一条 SC 钉住 (ii)。

---

### C-tl-2 · SC-3 —— D1 唯一的机械断言 —— 按 Spec 自己给的逐字命令**永远不会变绿**

**锚点**: proposal.md `§Success Criteria` SC-3 行 (:176) · `§What Changes 1` (:69-72)

SC-3 逐字: `grep -cE 'python3.*--main-branch\|--main-branch.*python3' SKILL.md` 期望 **≥ 1**。

受控实验 (`/tmp/.../sc3/`, 把 Spec 的逐字命令块原样写进一份 md 再跑):

| 检查 | GNU grep 3.8 | ugrep 7.5.0 (本机 `grep`) | 结论 |
|---|---|---|---|
| `-E` 下 `\|` 是不是 alternation | `grep -cE 'a\|b'` 对 `a\|b` 命中 1, 对 `ab` 命中 **0** | 同 | **是字面竖线, 不是或** |
| Spec 逐字命令块 (两行, 反斜杠续行) | 0 | 0 | 恒红 |
| 同一命令压成一行 | 1 | 1 | 才会绿 |

两条腿都断:

1. **写法腿**: `-E` 里的 `\|` 被两种 grep 一致地当成**字面 `|`**, 该 pattern 实际在找「同行同时含 `python3`…`--main-branch|--main-branch`…`python3`」的行, 永不存在;
2. **形态腿 (更要命)**: 就算把 `\|` 修成真 alternation, Spec 自己规定的逐字命令是**两行反斜杠续行** —— `python3` 在第 1 行, `--main-branch` 在第 2 行, 「同行」这个前提被 Spec 自己的交付物否定。实测仍是 0。

⇒ 一个**完全正确实现了 D1** 的 Phase B 交付, SC-3 依然红。这正是 memory `feedback_false_green_dual_is_permanent_red` 与 `feedback_perpetual_red_fix_must_change_the_quantity_not_the_threshold` 点名的形状: 恒红与假绿同样零信息量, 而且实施者面对恒红的最短路径是**去动断言而不是动实现** —— 一旦他把命令压成一行只为喂 grep, 或者悄悄放宽 SC-3, 承重项的验收就名存实亡 (且这属于 Rule #10 明令禁止的「AI 自作主张的流程判断」)。

Spec 在 SC 表头逐字写着「本表不留裁量空间」「前一版写『无 `"main"` 字面量』被 R3 三席证明两种自然实现都失效」—— 它在同一张表里对同一个病复发了一次: **这次不是宽/窄的问题, 是断言与被断言物在物理形态上不相容**。

**修法**: 断言换量。不要断言「同行」, 断言「`SKILL.md` 中存在一个以 `python3` 起、含 `pre_merge_gate.py`、且在同一个 fenced code block 内出现 `--main-branch` 的调用块」; 最省事的零裁量形态是 `grep -cE -- '--main-branch "?<MAIN_BRANCH>' SKILL.md` ≥ 1 配合 `grep -cE 'python3.*pre_merge_gate\.py' SKILL.md` ≥ 1 两条**分别**给期望值 (两条都今日为 0, 都必红, 都不含恒绿从句)。

---

### C-tl-3 · D1 只重整了 `§C.2.4` 详述段, `:166-169` 那份同形裸命令清单被降级为「只换字面量」—— 而 Spec 自己在 `:37` 刚论证过这不够; 且 SC-1..SC-11 无一条能检出

**锚点**: proposal.md `§What Changes 1` 段落定位行 (:64) + `§Impact` SKILL.md 行 (:222) · `SKILL.md:161-169`

`SKILL.md` 里今天有**两处**裸命令面, 不是一处:

```
:161  C.2.4 - Pre-Merge Precondition Gate (v1.3.0+):        ← 在 ## 执行流程 / ### 步骤执行 总览 yaml 块内
:166    primitive 调用:
:167      - aether ci status --branch main --in-flight --json (查 main 是否有 in-flight)
:168      - aether ci status --branch <PR_BRANCH> --json (查本 PR CI 状态)
...
:238  **执行流程**:                                          ← §C.2.4 详述段 (D1 要改的那处)
:243  3. **Query main in-flight**: `aether ci status --branch main --in-flight --json` ...
```

我全仓搜过 (`aether ci status` / `--in-flight` / `C.2.4` 三轮), **live plugin 面只有这两处**, `references/` 下零命中, 其他 skill 对 C.2.4 全是编排引用无命令 (workflow-runner `SKILL.md:313/323/329/341/351/385` + `references/workflow-state-schema.md:112/130` 都只说「调 C.2.4 gate」)。所以待审点 1 的答案是: **外部无泄漏, 但同文件内还剩一处, 而 Spec 恰恰对这一处开了口子**。

Spec 的处置证据链:
- `§1` 段落定位逐字只描述「`**执行流程**:` + 步骤 1-5 裸命令」⇒ 结构重整的对象是 `:238-255`;
- `§Impact` SKILL.md 行逐字: 「§C.2.4 结构重整 (…) · **`:167` `:243` `:270` 字面量** · …」⇒ `:167` 归在**字面量**处置, 不在结构重整里。

而 Spec 自己 `:37` 写着: 「⇒ **把 `:243` 的 `main` 换成占位符也没用** —— 占位符被逐字执行返回同样的空集, 同一个假绿。」

**同一份文档, 对同一种病, 在 `:243` 判「换字面量不够」, 在 `:167` 判「换字面量即可」。** 改完之后 SKILL.md 会同时说两件矛盾的话: `:166` 说「primitive 调用: aether ci status …」, `:238` 说「执行方式 (唯一): python3 helper」。AI 读哪份取决于它先读到哪一段 —— 而 `:167` 在**总览步骤块**里, 位置比详述段更靠前、更像流程定义。收敛没有完成。

**更硬的问题是: 没有任何 SC 能发现这件事。** 我逐条核过 SC-1..SC-11:

| D1 的结构要求 | 有断言吗 |
|---|---|
| ① 唯一 helper 入口在场 | SC-3 (**且见 C-tl-2, 恒红**) |
| ② 折叠块内去掉全部可执行命令字面量 | **无** —— 折叠块里留 `aether ci status --branch <MAIN_BRANCH> --in-flight --json` 也过 SC-1 |
| ③ `:167` 结构收敛 (不只是换字面量) | **无** —— SC-1 只查 `--branch main` 计数归零, 占位符替换即满足 |

**修法**: `§1` 把段落定位扩到「`:161-169` 总览块的 `primitive 调用:` 两行同批改为 helper 调用指引」; `§Impact` 把 `:167` 从「字面量」挪进「结构重整」; 补一条零裁量 SC: `grep -c 'aether ci status' SKILL.md` 期望 **0** (今日 4: `:167` `:168` `:243` `:244`) —— 这一条同时把 ② ③ 都钉住, 且必红。

---

## Major

### M-tl-1 · 折叠块将记载 5 步, 而 helper 改完是 6 步 —— 本 Spec 自己制造文档/代码失同步 (Rule #3)

**锚点**: proposal.md `§What Changes 1` 步骤行 (:65) + `§5` 插入点 (:117-126) + `§Impact` SKILL.md 行 (:222)

`§5` 明确把存在性核验插在 precheck 早退之后、`evaluate_path_coverage` 之前 —— 对应散文里的**步骤 2.5 与步骤 3 之间**, 是一个新步骤。但 `§1` 逐字只说「步骤 **1-5** 移入折叠块」, `§Impact` 的 SKILL.md 行也只列了「5 步移入折叠块去命令字面量」, **全文没有一句要求折叠块补上这一步**。

照字面实施的结果: 折叠块声称在描述「helper 内部算法 (供理解与排障)」, 却少描述了本 change 新加的、**唯一会 BLOCK 合并的那一步**。这既违反 Rule #3, 又直接损害待审点 2 关心的排障能力 —— 排障者看折叠块找不到 `main-branch-not-found` 是哪来的。

顺带回答**待审点 2**: 去命令字面量本身**不损害**排障 (5 步的诊断价值在「顺序 + 每步在判什么 + 失败怎么路由」, 不在命令字面量), 真正的损害来自这里 (少一步) 和 M-tl-2 (步骤 6 归属不明)。补上第 6 步的**无命令描述**即可, 成本一行。

---

### M-tl-2 · 步骤 6「路由决策」+ v1.65.0/#126 两条 surface 强制义务的归属未定义, 无断言保护, 而 DEC-20260731-001 依赖它们

**锚点**: `SKILL.md:252-255` (步骤 6 全段) · proposal.md `§1` (:65) · `docs/decisions/DEC-20260731-001-c24-wait-adjudication-retirement.md:29`

`§C.2.4` 的执行流程实际是 **6 步**, 不是 5 步。步骤 6 (`:252-255`) 是「路由决策」, 它规定的是**AI 侧的义务**, helper 完全不做:

- `green` → 调 branch-manager merge; `wait` → 输出 `wait_recoverable`; `fail` → BLOCK;
- **v1.65.0+ surface 义务 (二者缺一不可)**: not_applicable 放行必须加警告行; `path_coverage.decision == unknown` 时必须 surface 评估器失效 (含 #126 的 `internal-error` 单列文案)。

我核过 `pre_merge_gate.py` 全文: 它只往 stdout 写一行 JSON (`:438`), **不产生任何警告文案**。所以这两条是纯 AI 义务, 且是 `DEC-20260731-001` 逐字记载的**替代义务** (「not_applicable 放行必须 surface 警告行」) —— 是 owner 裁决退役人工裁决规则时的交换条件。

Spec 对步骤 6 一个字没提 (`git diff` 确认前后版本均无「路由决策」「步骤 6」字样), `§Impact` 的 SKILL.md 行也没有它。风险是双向的:
- 若实施者把 6 一起折进「⛔ 不要手工执行」的块 → 一条 owner 交换来的强制义务被降级成非规范注释;
- 若留在外面 → 一个只剩「6.」而看不到 1-5 的悬空编号, 下一个人很可能顺手重编号或并入折叠块。

且**无任何 SC 保护这两条 surface 义务在改完后仍在场**。

**修法**: `§1` 明写「步骤 6 保持在折叠块**外**且保持规范性 (它是 AI 义务, 非 helper 内部算法), 折叠块只收 1-5(+新核验步)」; `§Impact` 补该行; 加一条 SC (grep 两条警告文案关键字各 ≥1)。

---

### M-tl-3 · 三处「由 X 保证/机械钉住」, 去 X 实测都不做那件事 (delegate-verify 形状, 一 Spec 三例)

**锚点**: proposal.md `§非目标` (:213) · `§6 在场范围` (:148) · `§What Changes 1` 先例行 (:74)

| # | Spec 的声称 | 实读被引用方 | 差在哪 |
|---|---|---|---|
| a | 「**不动** `no_ci_fallback` / stub backend 既有降级语义 —— 由 **SC-10** 机械钉住, 不只是声明」 | SC-10 逐字只写「负控: `enabled=false` 早退」 | SC-10 只钉了 `enabled=false` **一条腿**。no-backend 降级 (`gate_check:337-339` → `_no_ci_output`) 与 stub-NIE abort (`:367-368`) **零 SC 覆盖**。三件事声称被钉住, 实际钉住 1/3 |
| b | 「三个早退分支保持既有六键不变 (`SKILL.md:279` 契约 + **`_OLD_KEYS` 守护测试**)」 | `test_pre_merge_gate.py:598-605` 定义 `_OLD_KEYS`; 两处消费在 `:658` (covered vs disabled 逐键相等) 与 `:689` (`assertIn`, not_applicable 路径) | 该守卫 (i) 是 `assertIn` **超集容忍**, 不是「恰好六键」; (ii) 覆盖的是 not_applicable / covered / backend-query-failure 三条路径, **不覆盖** Spec 点名的 no-backend 与 precheck-失败两条早退 |
| c | 「**先例**: `SKILL.md:737` 已有同形的强制 helper 调用范式, 本条沿用」 | `:737` 用 `${CLAUDE_PLUGIN_ROOT}` + 单行 | 「沿用」在**承重的那一位上没沿用** (见 C-tl-1), 且形态差异直接造成 C-tl-2 |

这三条是同一个类 (memory `feedback_delegation_must_verify_target_actually_does_it`): 写「由 X 保证」之前没去 X 核「它真做吗 / 方式合约吗 / 失败会发红吗」。按 memory `fix-the-class` 的教训, 修的时候请**一次扫完三处**, 不要只修被点名的那处。

**修法**: (a) 要么补 2 条 SC (no-backend 早退 / stub-NIE abort 各一条负控), 要么把 `§非目标` 的措辞降回「声明, 无机械保护」并诚实标注; (b) 同理; (c) 见 C-tl-1。

---

### M-tl-4 · `test_sc22` 守卫按 Spec 的字面扩法会**恒红** —— 待审点 4 的答案是「冲突, 但不在你问的那个位置」

**锚点**: proposal.md `§Success Criteria 测试卫生` (:188) · `test_pre_merge_gate.py:710-724`

Spec 要求「把该守卫**扩到 patch `pre_merge_gate` 模块自己的 `subprocess`**, 否则它对新代码恒绿」。实读该守卫:

```python
:715  def _forbidden(*_a, **_k):
:716      raise AssertionError("real git subprocess spawned in unit suite")
:718  with mock.patch.object(pc_module.subprocess, "run", _forbidden):
:723          out = gate.gate_check(pr_branch="feat/x")
:724  self.assertEqual(out["verdict"], "green")
```

它的桩是**抛异常的禁止桩**。而按 `§5`, 存在性核验落在三个早退**之后**、`evaluate_path_coverage` 之前 ⇒ **每一次 enabled + backend 可用的 `gate_check` 正常路径都会调一次 gate 层 subprocess**。所以把 `_forbidden` 也挂到 `gate.subprocess.run` 上之后, `:723` 那次调用会直接抛 `AssertionError`, `:724` 永远到不了 ⇒ **守卫恒红**。

Spec 只给了「扩」这个动词, 没给「扩了以后 `:723-724` 怎么还能绿」的解 (要么改成对 `_verify_branch_exists` 打桩, 要么把 gate 层 subprocess 换成**受控成功桩**而不是禁止桩 —— 但后者会把「禁止真 git」的语义换成「允许假 git」, 是另一个断言了)。这是 memory `spec-underdetermination` 的形状: 两个实施者会给出语义不同的两种守卫。

**待审点 4 的正面回答**: SC-6/7/8 的受控裸仓 fixture 与 `test_sc22` **不冲突** —— `test_sc22` 的 patch 是 `with` 块内局部作用域, 不泄漏到别的用例; 裸仓 fixture 是它自己的 `git init --bare` + 真 `ls-remote`, 两者井水不犯河水。**真正的冲突在 `test_sc22` 自己身上**: 它的语义 (「本套件不许起真 git 子进程」) 与 gate 正常路径新增的合法 subprocess 直接对立。

**修法**: `§Success Criteria` 把「扩到 patch `pre_merge_gate.subprocess`」改写成明确的两段式 —— 「(i) `test_sc22` 内对 `gate._verify_branch_exists` 打**成功桩**以保持 green 断言; (ii) **另立**一条守卫: 断言 `gate.subprocess.run` 在该代表性调用中**恰好被调用 1 次且 argv[0:2] == ['git','ls-remote']`」。后者才是真正「看得见 gate 层 subprocess」且不恒红的量。

---

### M-tl-5 · §版本「待 owner 裁定」是**半正当**的悬置 —— 选项集本身不完整, PATCH 分支已被成文约定排除

**锚点**: proposal.md `§版本` (:230-237) · CLAUDE.md `§版本管理` 第 2 行 · `standards/conventions/version-management.md §2.1-2.3`

先说结论: **悬置本身正当** (Rule #10 与 memory `no-self-exempt-gates` 都支持「拿不准就上报而不是自裁」), 但 Spec 呈给 owner 的**二选一是错的**:

Spec 给的两支: 「按对外 API 契约读 ⇒ MINOR/MAJOR」vs「按修复本不该存在的 fail-OPEN 缺省读 ⇒ PATCH」。

我核了两处成文约定:

- CLAUDE.md `§版本管理` 逐字: 「Aria 约定: 新增 Skill / **Skill 架构重构 = MINOR+**; 文档更新 / bug 修复 = PATCH。」
- `version-management.md §2.1` 的 Major 触发条件是**方法论结构级**的 (十步循环增减 / OpenSpec 不兼容 / 移除废弃功能), **不含**「helper CLI 参数由可选变必填」; §2.2 Minor 含「功能增强（向下兼容）」。

D1 逐字是「`§C.2.4` **由散文流程改为强制 helper 调用**」+ Spec 自己在 `§Impact` 称之为「结构重整」—— 这是教科书式的 **Skill 架构重构**, 直接命中 CLAUDE.md 那条。⇒ **PATCH 分支已被成文约定排除**, 地板是 MINOR。

Spec 漏引了这条直接管辖条款 (它引了「破坏性变更须 MAJOR」和「bug 修复 = PATCH」, 唯独漏了夹在两者中间、恰好裁决本例的那条)。按 memory `feedback_written_exception_exact_condition_match`「援引成文条款前逐字核对」, 这是一次**不完整援引**。给 owner 一个含有已被排除选项的二选一, 有让 owner 选出违反 CLAUDE.md 的结果的实际风险。

**修法**: `§版本` 改成「**地板 = MINOR** (依据 CLAUDE.md『Skill 架构重构 = MINOR+』逐字); 待 owner 裁定的是 **MINOR vs MAJOR** —— 即『plugin 的 helper CLI/函数签名算不算对外契约』」。这既保住了 Rule #10 的上报纪律, 又把 AI 该做的那部分做完。

**不阻塞 Phase B** (版本号在 C/ship 才落地), 但必须在 Phase B 开工前改掉措辞, 否则它会以现在的形态被端到 owner 面前。

---

### M-tl-6 · CLAUDE.md Rule #8 的同步面缺失, 且 §风险的 blast-radius 口径**结构上搜不到它**

**锚点**: proposal.md `§Impact` 表 (:220-228) + `§风险` grep 口径 (:244-245) · CLAUDE.md:113 · `docs/handoff/2026-05-28-aria-ci-backend-abstraction-v1.31.0-shipped.md:68`

CLAUDE.md Rule #8 逐字 (`:113`):

> **PR merge 前必跑 pre-merge gate** — phase-c-integrator C.2.4 验证 (a) 本 PR CI passing; (b) main 无 in-flight CI run; 经 CI backend 抽象层调用 (Aether 默认)。无可用 backend 按 `no_ci_fallback` 显式降级; stub backend 抛 NotImplementedError 时 gate 必须 abort, 不得静默降级。**SOT: `aria/skills/phase-c-integrator/SKILL.md §C.2.4`**。

本 Spec 做了两件直接触及这段文字的事: (1) 新增**第三条**会 BLOCK 合并的前置条件 (主分支须在 remote 上存在), 而 Rule #8 逐字只枚举了 (a)(b) 两条; (2) 把它指名的 SOT 段落从「散文流程」改成「helper 调用 + 非规范折叠块」, 规范算法实际迁进 `pre_merge_gate.py`。

`§Impact` 表**无 CLAUDE.md 行**。而 `§风险` 的 blast-radius 口径是 `grep -rn "pre_merge_gate\|gate_check" … aria/ aria-orchestrator/ standards/ docs/` —— 仓根 CLAUDE.md **既不在目录列表里**, 实测 `grep -c 'pre_merge_gate\|gate_check' CLAUDE.md` 也是 **0** (它用的措辞是「pre-merge gate」)。⇒ 就算把 CLAUDE.md 加进目录, 这个口径也搜不到它。这是 memory `feedback_invariant_dimension_must_match_error_dimension` 的形状: 口径的**维度** (符号名) 匹配不上错误的维度 (自然语言规则条文)。

**先例实证**: 同类改动 v1.31.0 (backend 抽象) 的 handoff 逐字记着「D | Doc updates | **CLAUDE.md Rule #8 L432-444 backend-agnostic** + 2 SKILL.md + new §C.2.4.X」—— 那次同步了, 这次漏了。

**修法**: `§Impact` 补 CLAUDE.md 行 (Rule #8 (a)(b) 枚举 + SOT 指针措辞); `§风险` 的口径补一条自然语言维度的 sweep (`grep -rn 'pre-merge gate\|C\.2\.4' CLAUDE.md README*.md standards/`)。**另**: 给一条非负债的判断 —— 「新增第三条 BLOCK 前置条件」是否需要 owner 单独签字, 我倾向**需要** (Rule #10 的对象是「已启用闸门的语义」, 加一条新的阻断腿是在改闸门语义, 不是实现细节)。建议 Spec 显式列为 owner sign-off 项而非默认吸收。

---

## Minor

- **m-tl-1 · 交付面内部自相矛盾**: `§待 R4 重点审` 第 3 条 (:262) 把 SC-3 描述成「`grep -c 'pre_merge_gate.py'` ≥2 + 同行含 `python3` 与 `--main-branch`」, 而 SC-3 表格行 (:176) 逐字**明令禁止**附加 `pre_merge_gate.py` ≥2 从句 (理由: 该文件名今日已 4 次, 恒绿零信息)。同一文件两处对同一条断言给出互斥描述。修 C-tl-2 时一并改。

- **m-tl-2 · Rule #6 定档正确, 但对 SOT §3 的转述比原文紧**: `§Rule #6` (:198) 写「同 SOT §3 界定第三行**专指**『给 spec 作者读的』处方 (authoring)」。SOT 实读 `skill-benchmark-exemption.md:30` 是「处方性, 但它治的行为在**固定测试集覆盖范围之外** (**典型**: authoring 向导 —— 给 spec 作者读的处方)」—— authoring 是**典型例**不是**定义**。结论不受影响 (第二行由 `:33` 逐字「`description` 或指令流程变动 ⇒ 一律第二行」**过度决定**, 我逐字核对过, 定档 D8 完全成立且论证扎实), 但「专指」这个转述会被后来者当规则复用。改成「典型形态是 authoring」即可。

- **m-tl-3 · SC-2 把输出示例也归零, 层级混淆**: SC-2 要求 `"branch": "main"` (`SKILL.md:270`) 计数归零。但 `:270` 是 `in_flight_runs[]` 的**输出示例** —— backend 返回的真实分支名, 且取自 `:221` 记载的 SilkNode PR-321 真实事故 (run 3161)。把它换成 `<MAIN_BRANCH>` 对 fail-close 零贡献 (输出示例不会被照抄成命令), 却损失示例的真实性与可读性。建议 SC-2 降级为可选, 或在 Spec 里说明「输出示例层与输入占位符层不同, 此处归零仅为 grep 面统一」。

- **m-tl-4 · `gate_error` 在场范围表述欠定**: `§6` (:148) 写「`gate_error` 只在核验失败路径与**最终 verdict 路径**可能在场」。但按 `§4`/`§5`, 核验失败即 `return`, 根本走不到 `compute_verdict`。「最终 verdict 路径在场」要么是笔误, 要么隐含要求把 `gate_error` 也 plumb 进 `_build_output`/`compute_verdict` 签名 —— 两个实施者会做出不同 schema。请二选一写死。

---

## 交叉一致性小结 (本席核心镜头)

D1–D9 逐条单看都成立, 我没找到「某条决策本身错」的例子。**全部 Critical/Major 都落在条款之间的缝上**, 这与 memory `feedback_fixes_contradict_each_other_across_clusters` 的预测一致 —— 多席位并行审计按角度切分, 接缝恰好落在角度之间:

| 缝 | 条款 A | 条款 B | 症状 |
|---|---|---|---|
| C-tl-1 | D1 (helper 唯一入口) | `SKILL.md:242` cwd 契约 + `:737` 先例 | 唯一入口在契约要求的 cwd 下不可达, 且无失败契约 |
| C-tl-2 | D1 的逐字命令 (两行) | SC-3 的「同行」断言 | 交付物与验收物物理形态不相容 |
| C-tl-3 | `§Why :37` (换字面量没用) | `§Impact :222` (`:167` 归字面量处置) | 同病两判, 收敛未完成且无断言 |
| M-tl-1 | D1 (折叠 5 步) | D4/§5 (新增第 6 步) | 折叠块少记一步 |
| M-tl-2 | D1 (折叠块 = 非规范) | `SKILL.md:253` + DEC-20260731-001 (AI 强制义务) | 规范义务可能被折进非规范块 |
| M-tl-5 | `§版本` 二选一 | CLAUDE.md「Skill 架构重构 = MINOR+」 | 上报给 owner 的选项集含已被排除项 |

关于 **#136 / #137 的关系**: Spec 的处置我认为**正确且克制** —— D9 (不在 #137 body 打删除线) 纠正了前一版的稻草人主张, 我核了 `gate_check:378-386` 确实存在 `not_applicable` 跳过 (a) 的通路, #137 原文的 (a) 描述成立; `§非目标` 把 branch-manager 合并动作留给 #136 也是对的边界。唯一建议: `docs/handoff/2026-08-08-post-planning-…:45` 已成文「**在 #136 落地前, 本 change 的子模块合并只能 owner 手工本地执行, pre-merge gate 需单独调用**」—— 这条**执行前提**没进 Spec, 而它恰好是 D1「唯一执行方式」在本 change 自己 Phase C 上的适用条件 (也正是 C-tl-1 的触发场景)。建议 `§Impact` 或 `§风险` 收录一句。

---

## Verdict

**FAIL** — 3 Critical + 6 Major + 4 Minor。**VOTE: REVISE。**

因为这是 `max_rounds=4` 最后一轮, 明确给出**进入 Phase B 的准入清单** —— 只有下列 4 项必须先落到 Spec, 其余 9 项建议在 A.2 任务分解时吸收 (可作为 tasks 条目, 不必再开一轮 Spec 审):

| # | 必须先修 | 为什么它阻塞 | 改动量 |
|---|---|---|---|
| 1 | **C-tl-1** 逐字命令的 `PLUGIN_ROOT` 选择 + 「helper 不可达 ⇒ fail, 禁止手工重构/跳过」决策 + 1 条 SC | 不修则承重项在本 change 自己的 Phase C 场景下不可执行, 且新增一个 Rule #8 静默降级向量 | 3 句 + 1 SC 行 |
| 2 | **C-tl-2** SC-3 换量 | 不修则 D1 的唯一验收标准恒红, 实施者只能改断言或改命令形态迁就 grep (Rule #10 禁止的自作主张) | 1 SC 行 |
| 3 | **C-tl-3** `:167` 纳入结构重整 + 补 `grep -c 'aether ci status'` = 0 断言 | 不修则收敛未完成且无任何机制能发现, 改完的 SKILL.md 自相矛盾 | 2 处措辞 + 1 SC 行 |
| 4 | **M-tl-2** 步骤 6 归属明写 | 不修有实际概率把 DEC-20260731-001 交换来的 owner 义务降级成注释 (规范回归, 且无断言) | 1 句 + 1 SC 行 |

四项合计约 **6 句措辞 + 4 条 SC 行**, 不改变任何决策 (D1–D9 全部保留), 不构成新范围。

**关于是否再开一轮**: 建议 **不再加轮**。按 memory `feedback_audit_marginal_return_goes_negative` 的判据 (本轮 fix 引入的 major 占比), 审计轨迹记载 R2=100% / R3=9/10, 已过拐点; 本轮 13 条中 11 条 `introduced_by_r3fix=true` (经 `git diff HEAD` 逐锚点核实), 说明缺陷源已从「原始范围」完全转移到「重定范围的新表面」, 再审同一表面只会继续制造同形循环。**正确处置是: owner 拍板上述 4 项 → 直接进 Phase B**, 把剩余 9 条写进 `tasks.md` 由 TDD 与 pre_merge 检查点承接。

---

## 轮次记录

| 项 | 值 |
|---|---|
| 轮次 | R4 / 4 (max_rounds) |
| 席位 | tech-lead (架构与流程镜头) |
| 本轮性质 | 范围重定后的**新对象**首审 (D1 面前三轮从未审过) |
| 未核对旧清单 | 是 —— 按编排指令, 只审当前 263 行交付面; R1/R2/R3 条目载体多已不存在 |
| 独立实证 | 22 条只读命令 + 2 组受控实验 (`/tmp/.../sc3/` grep 语义 × GNU grep 3.8 与 ugrep 7.5.0 双跑; `test -f` 在 meta-repo 根 vs 子模块根双 cwd) |
| 实读文件 | `proposal.md` (全 263 行) · `SKILL.md` (:140-350, :720-770, 全文 grep) · `pre_merge_gate.py` (全 445 行) · `test_pre_merge_gate.py` (:585-748 + 全文 grep) · `path_coverage.py` (grep) · `ci_backends/base.py` `aether.py` (grep) · `gate_state_helper.py` (:28-40, :139-167) · `CLAUDE.md:113` · `standards/conventions/skill-benchmark-exemption.md` (:5,:30,:33,:35,:39,:67) · `standards/conventions/version-management.md` (:25-70,:159-192) · `DEC-20260731-001` (:29) · 3 份相关 handoff |
| 仓库改动 | **零** (只读审计; 唯一写入是本报告与 `/tmp` 下的实验文件) |
| Spec 自述核验 | 数值断言 8 项全部独立复核通过 (见 §审计结论首表), 无一处夸大 |
| 与 R3 结论的关系 | **支持** —— R3 的根因结论经独立复核成立, 本轮全部 finding 是对其**处方完成度**的挑战, 不是对其诊断的挑战 |

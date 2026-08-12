---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-12T14:08:58.000Z
context: openspec/changes/premerge-gate-branch-existence/proposal.md
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R1 — tech-lead 席位报告

**被审对象**: `openspec/changes/premerge-gate-branch-existence/proposal.md` (Spec A, Level 2)
**审视角度**: 划界是否自足 / Level 2 与 MINOR 定档 / 与 B 侧的边界有无重叠或缺口
**基线**: 主仓 `0548317`, `aria` 子模块 `af87cae` (= Spec 声称的行锚基线)
**投票**: REVISE · **verdict**: FAIL (1 Critical + 4 Major + 2 minor)

---

## 0. 先说结论

**拆分本身是对的。** A 是一个真实、必要、可独立实现的增量, 且它的每一条行锚 / 逐字引用 / 实测数
我逐条回源都命中 (见 §5 溯源表复核, 12 行抽查 11 行 + 两个受控裸仓实验全部复现)。**执笔质量显著
高于 B 侧四轮任何一版。**

但有 **一条 Critical 与四条 Major 落在「组合是新的」这个接缝上** —— 它们无一是 B 侧 finding 的搬运:

- **Rule #6 定档 (Critical)**: A 提供的 substitute (SC-A6/A13/A-zero) 对它声称要替代的那两处
  `SKILL.md` 改动 **恒绿**; 且 A 自引的先例 v1.65.0 对**同形改动照跑了 AB**; 且 A 文内三处关于
  Rule #6 的表述互相矛盾。
- **自足性 (Major)**: A 的「关掉恒绿腿」在 `gate_check()` 层成立, 在**执行路径**层不成立 ——
  `SKILL.md:243` 的裸命令 A 不碰, 而那正是恒绿腿的执行形态 (今日实测本仓 `origin` 无 `main`)。
- **两条 SC 覆盖缺口 (Major ×2)**: §3 自称「唯一合法插入点」零 SC 覆盖 (违反它的实现 12/12 全绿);
  `--remote` 的 CLI 接线零 SC 覆盖 (漏接线则该 flag 静默 no-op, 12/12 仍全绿)。
- **定档依据 (Major)**: `:6` 的「无跨仓同步面」被 `:229` 自己推翻;「无架构变更」悬在一个未决 spike 上。

---

## 1. 我实际跑过的命令 (证据链)

```bash
# 基线与规模
git rev-parse HEAD                                  # 0548317018b9f647dc03af8e26042949bd6a04cb
git -C aria rev-parse HEAD                          # af87caeeed88af6af76f29a8002badbe1228d927  ← Spec 声称的基线
cd aria/skills/phase-c-integrator && python3 -m pytest tests/ -q   # 111 passed in 1.15s  ✅

# 调用面
grep -c "gate\.gate_check(" tests/test_pre_merge_gate.py           # 24
grep -rn "gate_check(" aria/ --include=*.py                        # 另有 pre_merge_gate.py:298 (def) + :435 (main() 内调用)
grep -n "main(argv" tests/test_pre_merge_gate.py                   # 零命中 ⇒ CLI 入口今日零测试
grep -rn "gate_error" aria/ | wc -l                                # 0  ✅
grep -c '_run_with_retry' tests/test_ci_backends.py                # 0  ✅
grep -c 'aether ci status' SKILL.md                                # 4  (:167 :168 :243 :244)
grep -rohn "SC-[A-Za-z0-9]*" tests/ | sort -u                      # SC-1,2,4,9,11,14,18,19,22,23,27 — 无 SC-A*  ✅

# 本仓现实
git ls-remote --heads origin main                                  # 零行输出, RC=0   ← 恒绿腿的活体
```

**受控裸仓实验** (scratchpad, 独立于本仓):

| 实验 | 结果 | 与 Spec 的关系 |
|---|---|---|
| 远端只有 `refs/heads/wip/master`, 查裸名 `master` | 命中 `wip/master`, **RC=0** | ✅ 复现 §2 表第 1 行 |
| 同上, 查锚定 `refs/heads/master` | 零行, RC=0 | (锚定确实排除了 `wip/master` —— 见 §4 minor-2) |
| 远端有 `refs/heads/master`, 查 `refs/heads/mast*` / `m[a]ster` / `maste?` | **三者全部命中 `refs/heads/master`, RC=0** | ✅ 复现 §2 表第 2 行「锚定关不掉 glob」 |
| 查不存在的 `wibble` | **RC=0 + 零行** | ✅ 复现「零命中亦返 rc=0」 |
| `--exit-code` 查 `wibble` | **RC=2** | ✅ 复现「⛔ 不得用 `--exit-code`」 |
| 指向不存在的 remote 路径 | **RC=128** | ✅ 复现 catch-all 那行 |

**行锚逐个实读** (全部命中, 零偏差):

`pre_merge_gate.py` `:328` `if not cfg["enabled"]:` · `:338` `if backend is None:` · `:344` `ok, precheck_err = backend.precheck()` ·
`:345` `if not ok:` · `:356` `pc: dict[str, Any] | None = None` · `:357` `if cfg.get("path_coverage_enabled", True):` ·
`:358` `pc = evaluate_path_coverage(` · `:366` `in_flight = backend.query_branch_in_flight(main_branch)` ·
`:68` `# Old keys still readable until v2.0` · `:116` `f"will be removed in v2.0",`

`SKILL.md` `:255` ``- `fail` → BLOCK + 输出 verdict + raw_message,phase-c-integrator return failure`` ·
`:259` 重试规范 · `:260` exit-code 映射 (含 `127 → no_ci_fallback`) · `:267` schema 首行 · `:279` 「各早退分支 (no-backend /
precheck 失败 / backend query 失败 / enabled:false) 保持六键不变」(**确为四类**)

`path_coverage.py:93` `except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as exc:` ·
`aether.py:38` `RETRY_BACKOFF = (5, 15, 45)` · `aether.py:164-187` `_run_with_retry` (硬绑 `[self.binary]` / 只捕
`TimeoutExpired` / docstring 逐字 "other exceptions bubble up" / 无 `cwd` / `text=True`) ·
`gate_state_helper.py:115` `def write_gate_state(` (形参 `state/name/verdict/in_flight_runs/primitive_used/raw_message/intervals` —
**确无 `gate_error`**) · `workflow-runner/SKILL.md:335-338` exit conditions **确为四条臂, 无异常臂** ·
`test_pre_merge_gate.py:710/:718/:723` (`:723` = `out = gate.gate_check(pr_branch="feat/x")`, **确未传 `main_branch`**) ·
`fetch_gate.py:55` `_DEFAULT_BRANCH_FALLBACKS = ("master", "main")` · `worktree_manager.py:170` `base_branch: str = "master"`

---

## 2. Findings

### C-1 [Critical] Rule #6 定档: A 提供的 substitute 对它声称要替代的 `SKILL.md` 改动**恒绿**; 且 A 自引的先例对同形改动照跑了 AB

**locator**: `proposal.md:191-201` (§Rule #6) × `proposal.md:38-39` (⛔不在范围 逐字含「Rule #6 AB」) ×
`proposal.md:125` (自引 v1.65.0 先例) × `standards/conventions/skill-benchmark-exemption.md:26/:33` ×
`aria/CHANGELOG.md` v1.65.0 段 × `aria/skills/phase-c-integrator/SKILL.md:242`

**evidence** (四条, 逐条实读/实跑):

**(a) substitute 恒绿。** SOT `:26` 逐字给第一行的处置是「**deterministic substitute**: 以结构化测试
(SC 级 **baseline-failing** 单元/集成测试, 必须在场) 替代 AB」。A `:196-197` 逐字提名
「本 Spec 的 SC-A6 / A13 / A-zero 即是」。但这三条 SC 断言的全是 `gate_check()` **返回的 dict**
(`verdict` / `gate_error.kind` / `raw_message`) —— **没有任何一条读 `SKILL.md`**。
⇒ 把 A 的两处 `SKILL.md` hunk (`:267` 加 `gate_error` 键、`:279` 早退注记) **单独回退**、
保留全部 `.py` 改动, 这三条 SC **仍全绿**。substitute 的定义性要求是「把改动回退, 该 fixture 必须转红」
(SOT §3 第 2 条逐字, 且第一行的 "baseline-failing" 是同一要求) ⇒ **它们不是那两处的 substitute, 是对那两处恒绿的旁观者。**

**(b) 逐字先例反向。** A `:125` 逐字「`gate_error` 是 additive 可选结构化副本 (**沿用 v1.65.0 `path_coverage` 先例**)」。
实读 `aria/CHANGELOG.md` v1.65.0 段: 「全量跨 skill 1546 绿。**Rule #6 照跑 AB** (3 eval × with/old/without 三臂…)」。
即 A 自己援引的那个先例走的是**第二行**, 不是第一行。且 v1.65.0 与 A **是同一形状的改动** ——
「往 `gate_check` 中间插一个新步 + 加一个 additive 可选输出键 + 同步 schema 与早退注记」——
它的落地实测结果是 `SKILL.md:242` 多了一条 **`2.5. **Path coverage 评估** (v1.65.0+…)`** 的
**执行流程新步骤**。A 主张同形改动**不需要**动执行流程, 与实执行史直接冲突
(memory `feedback_spec_precedent_verify_execution_history`: 引先例必核实际执行史)。

**(c) SOT `:33` 的收窄不匹配。** 逐字:「**SKILL.md 有变动时的附加约束**: **仅当**变动是**事实性同步**
(溯源注释 / 行号勘正 / 术语修正) 且 frontmatter `description` 零变动, **才可能**落进第一行」。
A 的两处 hunk 是「为本 change **新产生的**行为写文档」, 三个例示全是「文档陈旧、代码不变 ⇒ 修文档」。
即便认为这属边界情形, 判据表第四行逐字「**拿不准 ⇒ 照跑 (宁跑勿豁)**」仍指向照跑
(memory `exact-exception-condition`: 援引成文豁免须**字段级**匹配确切触发条件, 覆盖外分支上报而非自搭桥)。
可比先例 `linked-issue-normalization:270` 就是靠把 `SKILL.md:176` 那个 hunk 明确刻画成
「**纯事实勘正 hunk**」才留在第一行的 —— A 的 hunk 没有这个性质。

**(d) 文内三处自相矛盾, 不可能同时为真。**
`:196` 主张第一行 (substitute = AB 豁免通道) × `:201` 逐字「**本 Spec 不申请任何豁免**」×
`:39` 逐字把「Rule #6 AB」整体划归 B 侧。而 Rule #6 的触发点是**本 change 自己的发版**
(CLAUDE.md 逐字「Skill 变更**发版前**须过 Rule #6 benchmark」) —— A 按 MINOR **独立发版**,
AB 义务结构上无法转移给一个至今「不具备进 Phase B 条件」的姊妹 Spec。

**how_it_goes_red** (机械, 一条命令级实验):
在 Phase B 落地分支上 `git checkout HEAD -- aria/skills/phase-c-integrator/SKILL.md`
(只回退那两处 hunk, 保留 `.py` 与 tests), 跑 `pytest -k "sc_a6 or sc_a13 or sc_a_zero"` ⇒ **三条全绿**。
substitute 若成立必须至少一条转红。反向: 若把 `SKILL.md` 执行流程按 v1.65.0 先例补一条新步骤,
则 `description` 之外的**指令流程**已变 ⇒ SOT `:33` 逐字「指令流程变动 ⇒ **一律第二行**」⇒ 必须照跑 AB,
而 A `:39` 说那不在范围内 ⇒ Spec 必须回炉。两个方向都红。

**blocks_phase_b**: **true** —— `rule6_note` 是 A.2 排任务的直接输入; 现文任一读法都会把 A.2 引到
一个 A 自称不在范围的动作上。

**处方 (供参考)**: 二选一并写死 —— (i) 落**第二行**, 把 Rule #6 AB 收进 A 的范围 (与 `:201`
「不申请任何豁免」自洽), `:39` 的「Rule #6 AB → B 侧」改为「B 侧的 AB 覆盖 B 侧改动」;
(ii) 若坚持第一行, 必须给出**真正 baseline-failing 于 `SKILL.md` 那两处**的结构化测试
(例: 一条断言「`SKILL.md` Output schema 块所列键集 == `_build_output` 实产键集 ∪ {`gate_error`}」的
doc-code 一致性测试 —— 回退 `:267` 即红)。

---

### M-1 [Major] 「存在性核验单独就关掉恒绿腿」在 `gate_check()` 层成立, 在**执行路径**层不成立 —— A 未声明残余暴露

**locator**: `proposal.md:27-35` (§本 Spec 的范围判定) + `:37-39` (⛔ D1 留 B) + `:205-216` (§非目标)
× `aria/skills/phase-c-integrator/SKILL.md:243`

**为什么这落在 A 而不是 B**: 被审的是 **A 自己的范围声称** ——`:29-32` 逐字「存在性核验单独就消除了
那个不可区分性 … ⇒ 本 Spec **只做这一件事**」。这句判断是 A/B 划界的承重理据 (DEC §3 同句),
不是 B 侧的 finding。我不引用、也不继承 R4 那 3 条 Critical。

**evidence**:
1. `SKILL.md:243` 逐字: ``3. **Query main in-flight**: `aether ci status --branch main --in-flight --json` → parse `data.runs[]` ``
   —— **分支名 `main` 是硬编码字面量**, 且这是 §C.2.4「执行流程」编号步骤本体。
2. 实跑 `grep -c 'aether ci status' SKILL.md` = **4** (`:167` `:168` `:243` `:244`), A 的 §Impact 表
   (`:222-229`) 对 `SKILL.md` 的改动逐字只有「**仅描述性**: `:267` schema 增 `gate_error` · `:279` 四类早退注记同步」
   ⇒ **`:243` 不在 A 的改动面内**。
3. 实跑本仓 `git ls-remote --heads origin main` = **零行 + RC=0** ⇒ `:243` 那条命令在本仓今日就是恒绿腿的活体。
4. `workflow-runner/SKILL.md` 全文 grep `pre_merge_gate.py` = **零命中**; 它对 gate 的唯一表述是
   `:329` / `:351` 的「re-invoke: **phase-c-integrator C.2.4**」⇒ 编排层把执行交回 `SKILL.md` 的散文流程,
   进入 `gate_check()` 的唯一文档入口是 `:262` 那句被动的「**Helper 实现**: …/pre_merge_gate.py」, 它不是指令。

**how_it_goes_red**: A ship 后, 按 `SKILL.md §C.2.4 执行流程` 步骤 3 **逐字**执行
`aether ci status --branch main --in-flight --json`, 在本仓仍得 `runs:[]` RC=0 ⇒ verdict 仍 green。
建一条「按 SKILL.md 散文路径执行 C.2.4」的 fixture 即红; 建一条「按 helper 路径执行」的 fixture 即绿。
两者并存就是这条 finding 的可证伪形态。

**风险为何是实的而不是理论的**: B 侧抬头逐字「**本侧当前不具备进 Phase B 的条件**」⇒ D1 的落地时点未定
⇒ 残余暴露是**无限期**的。而 B 侧抬头同时逐字称 A 承接「**即关掉 #137 那条恒绿腿所需的全部内容**」——
若 A ship 后据此 close #137, 就是 memory `feedback_paper_fix_antipattern` /
`feedback_completion_signals_vs_runtime_invocation` (单测绿 ≠ 代码真被生产调用) 的教科书形状。

**blocks_phase_b**: **true** (它改变 A 的「完成」定义与 A.2 的验收/闭环任务)

**处方**: §Why 或 §非目标 补一条逐字残余声明 ——「A 落地后, `SKILL.md:243`/`:167` 的散文裸命令路径
**仍恒绿**, 直到 B 侧 D1 收敛两份实现; **A ship 不构成 #137 的闭环, 不得据此 close #137**」。

---

### M-2 [Major] §3 自称「唯一合法插入点」, 但 12 条 SC 无一钉住它 —— 违反它的实现 12/12 全绿

**locator**: `proposal.md:96-113` (§3) × `proposal.md:171-187` (SC 表)

**evidence**: §3 `:105` 逐字标注「★ 存在性核验 (本 Spec 新增) ← **唯一合法插入点**」, `:113` 逐字给理据
「**在 path coverage 之前**: 它更早消费 `main_branch`, 放它之后等于放行一次未核验的使用」。
SC 表 12 条中, A 对**三个早退**用了因果断言 (`SC-A10/A10b/A10c` 逐字「**且 `assert ls-remote 未被调用`**」,
且 `:179` 自己写明「兄弟早退不同步则该类只修了一个实例」) —— 但对 `evaluate_path_coverage`
这条**同族的顺序约束零断言**。这正是 memory `fix-the-class` 点名的形状: 认出了类, 只推广了一半。

**how_it_goes_red**: 把核验步插在 `pre_merge_gate.py:358` 的 `evaluate_path_coverage(...)` **之后**、
`:366` 之前 —— SC-A6/A13/A-zero 仍得 `verdict=fail` + 正确 `kind` (path coverage 先跑但 `decision=unknown`
不改 verdict, 见 `path_coverage` 的 fail-toward-covered), SC-A7/A8/A14/A10*/A11/A-sc22/A-baseline 亦全绿
⇒ **12/12 通过而 §3 被违反**。补一条「存在性核验判 fail 时 `assert evaluate_path_coverage 未被调用`」即让该实现转红。

**次生实害** (非理论): 违规实现下, `main_branch` 不存在会先让 `git diff --name-only <main>...<pr>` 失败
⇒ `decision=unknown` ⇒ 按 `SKILL.md:253` 的 surface 义务 AI 必须报「path coverage 评估失败
(reason=`git-diff-failed`)」—— 把人指向 git/main ref, 而真因是「分支名根本不存在」。诊断被引偏一层。

**blocks_phase_b**: **true**

---

### M-3 [Major] `--remote` 的 CLI 接线零 SC 覆盖; §版本「既有 24 处调用零改动」漏计第 25 处 (`pre_merge_gate.py:435`)

**locator**: `proposal.md:49-51` (§1 逐字「/ CLI `--remote`」) × `proposal.md:233-234` (§版本) ×
`proposal.md:171-187` (SC 表) × `aria/skills/phase-c-integrator/scripts/pre_merge_gate.py:424-440`

**evidence** (实跑, 三项并列):
- 总体 = `aria/` 全仓 `*.py`; 计数法 = `grep -c`。`grep -c "gate\.gate_check(" tests/test_pre_merge_gate.py` = **24**;
  `grep -rn "gate_check(" aria/ --include=*.py` 另得 `pre_merge_gate.py:298` (**def, 非调用**) 与
  **`:435`** (`main()` 内 `output = gate_check(pr_branch=args.pr_branch, main_branch=args.main_branch, config=config)`, **是调用**)
  ⇒ **真实调用点 = 25, 不是 24**。
- `grep -n "main(argv" tests/test_pre_merge_gate.py` = **零命中** ⇒ CLI 入口 `main()` 今日**完全无测试覆盖**。
- SC 表 12 条**无一条**经 `main(argv)` 进入; 全部走 Python 层 `gate_check(...)`。

**how_it_goes_red**: 实现只加 `parser.add_argument("--remote", default="origin")` 而**漏掉** `:435` 处的
`remote=args.remote` ⇒ `--remote github` 被静默忽略, 永远查 `origin`; **12 条 SC 全绿**, `--remote` 沦为
装饰性 flag (memory `feedback_completion_signals_vs_runtime_invocation` 同形)。
补一条 `main(["--pr-branch","x","--remote","<不存在的 remote>"])` ⇒ 期望
`verdict=fail` + `kind=="main-branch-verify-failed"` 的 SC, 该漏接线实现即红。

**为什么不是纯 nitpick**: 「24 处零改动」是 A 论证 MINOR 的**承重实证之一** (`:234` 逐字加粗)。
数字本身不影响 MINOR 结论 (加带默认值的 kwarg 对 25 处都零破坏), 但它把**唯一必须改的那处调用点**
排除在读者视野外 —— 而那处恰是 `--remote` 唯一的落地点。

**blocks_phase_b**: **true** (SC 集合自足性)

---

### M-4 [Major] Level 2 / MINOR 的两条定档依据: 一条被本文件自己推翻, 一条悬在未决 spike 上

**locator**: `proposal.md:6` (Level 2 依据逐字「无架构变更, 无跨仓同步面, 无破坏性契约变更」) ×
`proposal.md:229` (§Impact 「发版同步面」行) × `proposal.md:227` (`aether.py` 条件性入 scope) ×
`proposal.md:151-153` (§5「复用形态 = Phase B spike」)

**(a) 「无跨仓同步面」与 `:229` 自相矛盾。**
CLAUDE.md 逐字:「发布同步面: **aria 子模块 5 文件 + 主仓 gitlink + 主仓 VERSION + root README badge + i18n README**」。
A 的代码落 `aria/` 子模块 (`:10` 逐字), Spec 落主仓 ⇒ 按 MINOR ship **必然**跨两仓。
而 `:6` 写「无跨仓同步面」, `:229` 又写「发版同步面: **MINOR, 走常规发版流程**」—— 同一文件里
一处说没有、一处说走流程。Level 2 = proposal only ⇒ **无 `tasks.md` 承载那份清单**。
姊妹 Spec R4 三条 Critical 之一就是 `TASK-017` 漏 gitlink; A 的处理方式是把整张清单降为一句
「走常规发版流程」, 机械可验性比 B 更低而不是更高 (memory `scoped-add-splits-claim`: 发布同步面
一天内两次漏项实证)。

**(b) 「无架构变更」悬在未决 spike 上。**
`:227` 逐字:「`ci_backends/aether.py` | **条件性** —— 仅当 spike 判定须抽取共享重试 helper 时入 scope」。
实读 `aether.py`: `_run_with_retry` 定义在 `:164`, **唯一调用者** `:199` (`AetherBackend._query`);
实跑 `grep -c '_run_with_retry' tests/test_ci_backends.py` = **0**, 全 `tests/` 目录亦 **0**
⇒ 抽取它是**跨 backend 抽象层、零既有测试保护**的结构改动。若 spike 判「抽取」, `:6` 的
「无架构变更」事后失效, 而 Level 已定 2、无 `tasks.md` 承载该风险与其回归面。

**how_it_goes_red**:
(a) A ship 后只改子模块而不 bump 主仓 gitlink/VERSION/badge ⇒ `git submodule status` 与 root README
badge 立即不一致, custom check `m6-version-badge-match` 对 gitlink 方向**结构上失明**
(post_planning R3 已实证该失明), 即「不会发红」本身就是缺口的证明。
(b) Phase B spike 若判「抽取」, `git diff --stat` 出现 `ci_backends/aether.py` ⇒ 与 `:6` 定档依据直接冲突,
必须回炉重定 Level —— 而此时 A 已在 Phase B 中途。

**blocks_phase_b**: **true** (对 (b): 需在 A.2 前二选一钉死 —— 要么明写「A **不动** `aether.py`, gate 层自建
私有 runner (可复制 `path_coverage.py:78-96` 的形状)」, 要么把 Level 定 3 并出 `tasks.md`)

---

### m-1 [minor] `verify-failed` 路径的 `raw_message` 无任何 SC 兜底 —— 生产上唯一可见的诊断通道可以为空而全绿

**locator**: `proposal.md:117-124` (§4) × SC 表 `SC-A7 / SC-A8 / SC-A14`

**evidence**: §4 `:123-124` 逐字要求「**`raw_message` 主通道 (必填)**: 失败时须写入人类可读诊断,
**含分支名与 remote 名**, 且**明确区别于「无 in-flight run」**」。SC 表中只有 **SC-A6** 断言了
`raw_message` 内容 (且只覆盖 `not-found` 分支); `SC-A7/A8/A14` (即全部 `verify-failed` 分支) **只断言 `kind`**。
而 `kind` 住在 `gate_error` 里, A `:137` 自陈实测**全仓零消费者** ⇒ 生产上唯一能被 `SKILL.md:255`
(「fail → BLOCK + 输出 verdict + **raw_message**」) 输出的就是 `raw_message`。

**how_it_goes_red**: 实现在 verify-failed 分支写 `raw_message=""` ⇒ SC-A7/A8/A14 全绿, 而无人值守
Layer 2 跑里 workflow-runner 只能打印空串, 零诊断。补
`assert main_branch in raw_message and remote in raw_message` 于三条 SC 即红。

**blocks_phase_b**: false

---

### m-2 [minor] 「其余一切 ⇒ 不重试」把瞬时网络故障与永久性坏 remote 名合并为**不可重试的 fatal**, Spec 未评估其在 168h 无人值守下的可用性面

**locator**: `proposal.md:88` (catch-all 行, 逐字「重试? **否**」) × `workflow-runner/SKILL.md:337`

**evidence**: 我实测 `git ls-remote --heads ../nonexistent.git master` ⇒ **RC=128**; git 对**一切**远端错误
(坏 remote 名 / DNS / TCP reset / 认证) 统一用 128 —— A `:88` 自己也逐字列了「remote 名不存在 / 坏 URL /
**网络不可达**均为 128」并判**不重试**。而 `workflow-runner/SKILL.md:337` 逐字 exit condition 3:
「**verdict=fail → 转为 stop (fatal)**」。⇒ Forgejo 一次短暂不可达 ⇒ gate 直接 fatal, 无重试、无 `wait_recoverable`。
对照: 同一 SKILL 的 `:259` 对 subprocess **timeout** 给了 3 次退避重试。

**为什么仍只判 minor**: fail-CLOSED 与 catch-all 的设计选择本身是对的 (正向枚举天然 fail-OPEN,
memory `feedback_invariant_needs_failclosed_default`), 且今日 aether 路径遇网络错误同样直接 fail。
但 A 是**新增的、更早的**失败点, 且 v2.0 的 168h 无人值守是本项目当前的主线场景 ——
Spec 应显式记一句该权衡 (或把 128 中可辨识的瞬时子集纳入既有 `RETRY_BACKOFF`), 而不是留给实现者推断。

**how_it_goes_red**: 把 remote URL 指向一个连接后立即 reset 的地址, 跑一次 C.2.4 ⇒ A 后
`verdict=fail`(不重试) 且 `session.status=failed` 不可 resume; A 前同一构造走 aether 路径至少经 3 次尝试。

**blocks_phase_b**: false

---

## 3. 明确**不成立**的怀疑 (我查过并排除)

为免下一轮重复劳动, 记录我验过但**判无问题**的项:

| 我怀疑的 | 实测 | 结论 |
|---|---|---|
| `SC-A*` 前缀与既有号段冲突 | `grep -rohn "SC-[A-Za-z0-9]*" tests/` = SC-1/2/4/9/11/14/18/19/22/23/27, **无 SC-A\*** | ✅ A `:168-170` 的预防成立 |
| 六键 schema 会被 `gate_error` 破坏 | `_build_output` (`:232-263`) 实读: 固定六键 + `path_coverage` 条件加键; 加第七个条件键与 `path_coverage` 同构 | ✅ 纯 additive |
| `gate_error` 会撞下游 schema | `grep -rn "gate_error"` 全仓 (排除 spec/审计/handoff) = 0; `write_gate_state(:115)` 形参不含它且它**逐字段重建** `state["gate_state"]` ⇒ 多余键根本传不下去 | ✅ 零破坏面 |
| `workflow-runner` 有异常臂会吞 fail | `:335-338` 四条臂 (Ctrl-C / retry超限 / **fail→stop** / green), 无异常臂 | ✅ A `:138` 陈述准确 |
| 111 基线是陈的 | 实跑 `111 passed in 1.15s` | ✅ 红窗前提成立 |
| SC-A13 不能区分锚定 vs 精确 | 受控实验: `refs/heads/mast*` 命中 `refs/heads/master` RC=0 ⇒ 锚定实现判「存在」⇒ green ⇒ 必红; 精确比对实现 `"refs/heads/master" != "refs/heads/mast*"` ⇒ fail | ✅ 有判别力 |
| §非目标里两个「同形兄弟位置」是编的 | `fetch_gate.py:55` / `worktree_manager.py:170` 实读命中 | ✅ |
| §5 两个先例锚点漂了 | `path_coverage.py:93` / `aether.py:38` / `:164-187` 逐行命中, 含 docstring 逐字 "other exceptions bubble up" | ✅ |

另: **溯源表 (`:245-262`) 12 行我抽查了 11 行, 11/11 命中。** 唯一未独立复核的是
「post_planning R1 对抗复核 / R2 / R3」这三个**来源标注**本身 (我核的是被标注的**事实**, 不是它出自哪一轮)。

---

## 4. 划界结论 (席位本职, 三问三答)

**Q1: A 侧真的只需要这些吗? 有没有把 B 侧的东西漏带过来?**
**漏带一件: 与 `SKILL.md` 执行流程的同步。** A 把「散文收敛为 helper 调用 (D1)」整块留给 B 是对的
(那是重构, 拉 MAJOR); 但 A 自己**往 `gate_check()` 里插了一个新步**, 而 `SKILL.md §C.2.4 执行流程`
是该流程的规范面 (`:240-252` 编号步骤 1/2/**2.5**/3/4/5/6)。**v1.65.0 做同形改动时补了步骤 2.5** ——
这是实执行史, 不是类推。A 主张不补 ⇒ 要么 Rule #3 文档-代码漂移 (M-1 的执行路径缺口),
要么补了就变成指令流程变动 (C-1 的第二行)。**这一件必须在 A 内解决, 不能推给 B。**

**Q2: 有没有把 A 不需要的带过来?**
**没有多带, 但有一件「带了一半」**: §5 的异常/重试复用。异常轴 (`path_coverage.py:93` 元组) 是纯抄一个
三元组, 零耦合, 带得对; 重试轴留了 `aether.py` **条件性入 scope** —— 那是把「A 会不会变成架构改动」
这个定档前提留给未决 spike (M-4b)。建议直接钉死「不动 `aether.py`」, A 的 subprocess 面小到自建即可,
`path_coverage.py:78-96` 就是现成的、已过 #124 教训的形状。

**Q3: 「存在性核验单独就关掉了恒绿腿」成立吗?**
**在 `gate_check()` 层成立, 在执行路径层不成立** (M-1)。DEC §3 的推理只引了 B 的 §症状
(后端不可区分性), **没引 B 的 §根因** (两份实现 / AI 走散文那份)。这两段在 B 的原文里是紧邻的
上下句。A 承接了 §症状 的逐字, 却没承接 §根因 对「helper 层修复的射程」的限定。
**拆分不因此失效** —— A 仍是必要且正确的第一步, 且它是唯一能以 MINOR 交付的那一步;
**但 A 的完成定义必须写明残余暴露**, 否则 ship + close #137 = paper fix。

---

## 5. 我这一轮**没有**做的事 (边界声明)

- 未继承 R4 的 3 条 Critical (全属 B 侧); 上文任一 finding 都不引用它们;
- 未改任何文件 (报告除外), 未 commit/push, 未调外部 API;
- 受控裸仓实验建在 scratchpad, 与本仓无交互;
- 未对 B 侧 proposal 提任何 finding。

---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-09T12:39:35.675Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R1 — qa-engineer 席位报告

**被审对象**: `tasks.md` (69 行) + `detailed-tasks.yaml` (19 条 / 378 行)
**参照物**: `proposal.md` (post_spec R1–R5 已 owner override 放行, 本席位不重审其决策, 仅在其文本被任务当作"已实证输入"直接引用时回源核字面)
**镜头**: 测试策略与可证伪性 —— 本 Spec 的核心押注是"TDD 前置, 让缺陷在实施时自己发红", 本席位的任务就是压这个押注站不站得住。

**方法论声明**: 下列每条 finding 均基于本席位自己实读的源文件行号或自己实跑的命令输出, 不转述 proposal 的"今日实测"列或其他文档的自陈。凡引用行号, 均以 `Read`/`grep -n` 当场核对为准。

---

## 审计结论

**四条核心结论**:

1. **TASK-001 的"先看到全红"设计本身成立**: 我逐条实跑了 proposal SC-1/SC-3/SC-4/SC-5 的字面 grep 命令, 计数与 proposal"今日实测"列**完全一致** (4 / 0 / 1·1·1 / 1), 详见 §1。TASK-001 要求的红窗是真红, 不是自证的空话。
2. **但 TASK-011 (D1 承重任务) 的验收网眼比它要挡的缺陷粗一档**: 我独立构造了两个会让本仓或第三方采用方恒红的 SKILL.md 写法, 两者都 100% 通过 TASK-011 现有的全部 4 条验收 (SC-1/SC-2/SC-3 + 折叠块检查)。承重断言测的维度 (`--pr-branch` 出现次数) 与本 Spec 要治的病灶维度 (`--main-branch` 的值/存在与否) 不重合。这是 **Critical**, 详见 §2 / C-2。
3. **本 Spec 押注的"让测试自己发红"机制, 建立在一套与仓内既有测试命名空间冲突的编号方案上**: `test_pre_merge_gate.py` 里已有一个类 `PathCoverageGateTests`, docstring 逐字声明覆盖"SC-9/10/11/12/13/15/21/22"(源自另一个已 ship 的 Spec `phase-c-gate-path-coverage-not-applicable` #122), `test_path_coverage.py` 头部逐字声明覆盖"SC-1~8, 14, 16~20, 23~28"。本 proposal 全新起了一套从 SC-1 到 SC-13 的编号, 与既有编号在同一个测试文件内 5 个号 (SC-9/10/11/12/13) 直接复用、在跨文件语境下全部 13 个号都复用。这是 **Critical**, 详见 §3 / C-1 —— 本席位认为这是本轮独有的、其他镜头不会看到的发现, 因为它需要"测试策略/命名空间"这个特定视角。
4. **TASK-005 (测试隔离接缝) 对隔离机制本身的判断是对的** (`subprocess` 模块对象跨模块共享, patch 会全局生效) —— 我独立复现了这个机制。但它的 `dependencies` 缺一条边: 新 subprocess 调用最终落在哪个模块 (自己新写 vs 复用 `ci_backends/aether.py`) 由 TASK-004 的 spike 决定, 而这直接决定接缝该设在哪个粒度。TASK-005 只声明依赖 TASK-003, 未依赖 TASK-004。这是 **Major**, 详见 §4。

**本席位实做的核验** (全部只读, 未改任何文件):

| 核验对象 | 方法 | 结果 |
|---|---|---|
| SC-1/SC-3/SC-4/SC-5 今日实测计数 | 实跑 4 条 grep | 4 / 0 / 1·1·1 / 1, 与 proposal 声称逐条一致 |
| 24 处 `gate_check(` 调用 + 0 处显式 `main_branch=` | 实跑 grep, 人工核对全仓 30 处命中的构成 | 24 (test 调用) + 1 (CLI 内部调用) + 5 (注释提及) = 30, "24" 之数属实 |
| `test_sc22_no_real_git_subprocess_in_suite` 的 patch 是否全局生效 | 实读 `path_coverage.py:47/87/93` + `test_pre_merge_gate.py:710-724`, 结合 Python 模块单例语义推演 | 属实 —— `pc_module.subprocess` 与 `sys.modules['subprocess']` 同一对象, patch 跨模块生效 |
| `SKILL.md:262/:559/:610` 是否均用 `${CLAUDE_PLUGIN_ROOT}` (proposal:64 / TASK-002 verification#3 的输入) | 逐行 `sed -n` 核对字面 | **均为 `${ARIA_PLUGIN_ROOT:-aria}`, 零处 `CLAUDE_PLUGIN_ROOT`**; 全文件 `CLAUDE_PLUGIN_ROOT` 仅 `:737` 一处 (无关的 telemetry 脚本) |
| `test_pre_merge_gate.py` / `test_path_coverage.py` 既有 `test_scN_*` 方法全表 | `grep -n 'def test_sc'` | 见 §3, 与本 proposal SC-1..13 五号直接同文件冲突 |
| SC-6/SC-13 判据 (D6 三轮实验) 是否可复现 | 自建受控裸仓, 实跑 `git ls-remote --heads` 5 种场景 | **完全复现** proposal 的三轮结论 (裸分支名尾段 glob / 锚定仍被元字符 glob / 精确比对才对), 见 §5 |
| SC-7 声称的退出码 128/129 | 自建场景, 实跑 `git ls-remote` 对不存在 remote 名 / 坏路径 / 错误 flag | 128 / 128 / 129, 与 proposal 声称一致 |
| proposal §测试基线"111 tests" | 实跑 `pytest tests/ -q` | **111 passed**, 46+25+40 精确对应, 当前绿态 |
| TASK-011 验收 (SC-1/SC-2/SC-3) 是否覆盖 `--main-branch` 的值/存在 | 自建 2 个违规 SKILL.md 片段实测 grep | 两者均**全绿通过**, 验收对该维度失明 (C-2) |
| `:328/:338/:344-345/:356-358/:366` 三早退 + 核验点插入坐标 | 实读 `pre_merge_gate.py:296-370` | 行号精确, 与 proposal §6 逐字一致 |
| `:21` docstring / `:427` CLI 两处 `main` 字面量 | `grep -n` | 行号精确 |

---

## §1 TASK-001 的"先看到全红"设计成不成立

**结论: 成立。**

```
$ grep -c 'aether ci status' aria/skills/phase-c-integrator/SKILL.md
4   (命中 :167 :168 :243 :244)
$ grep -c -- '--pr-branch' aria/skills/phase-c-integrator/SKILL.md
0
$ grep -c 'default="main"' .../pre_merge_gate.py ; grep -c 'main_branch: str = "main"' ... ; grep -c -- '--main-branch main' ...
1 / 1 / 1
$ grep -c 'default: main' .../pre_merge_gate.py
1
```

四条与 proposal SC 表"今日实测"列逐条一致, TASK-001 verification 里"贴出实施前的实跑输出证明四条全红"这条要求是可执行、非空话的。这也间接验证了 proposal 自陈的"编排层两次写出恒红断言与一次恒绿断言"教训在本轮确实被吸收——这四条今天是真红。

**唯一缺口 (m-1, Minor)**: proposal SC-1..SC-5 五条并列声明"零裁量", 但 TASK-001 的红窗只取了四条 (SC-1/SC-3/SC-4/SC-5), **独缺 SC-2** (`grep -c '"branch": "main"' SKILL.md`, 今日实测 1, 期望 0)。SC-2 与其余四条同类同形、同样是纯 grep 断言, tasks.md/detailed-tasks.yaml 都没有给出"为什么它不进红窗"的理由。它最终由 TASK-013 认领转绿, 但破了"组 0 = 全部 TDD 前置先见红"这条 tasks.md 自己立的组织原则的完整性 (`tasks.md:13`)。

---

## §2 每条任务的 `verification` 数组 —— 逐条判断"它怎么会红"

多数任务的 verification 是合格的 (grep pattern + 期望值 + 起止状态三元组俱全, 例如 TASK-006/009/010)。但两类问题反复出现:

### 2.1 Critical: TASK-011 的验收对本 Spec 的病灶维度失明 (C-2)

TASK-011 (D1 承重, `detailed-tasks.yaml:221-239`) 的全部验收是:

1. SC-1 `grep -c 'aether ci status'` 由 4→0
2. SC-3 `grep -c -- '--pr-branch'` 由 0→2
3. 折叠块须补上存在性核验步 (人工判断)
4. 去掉全部可执行命令字面量, 含 `:240` (人工判断)

我用两个刻意违规的 SKILL.md 片段实测这四条断言中唯二可机械执行的两条 (SC-1/SC-3; SC-2 与本任务无关, 因为示例片段本就不含 `"branch": "main"`):

```
变体 A —— 两处调用完全不带 --main-branch:
  `python3 pre_merge_gate.py --pr-branch <PR_BRANCH>` × 2
  SC-1=0 SC-3=2  → 全绿通过

变体 B —— 两处调用把 --main-branch 硬编码成字面量 "main":
  `python3 pre_merge_gate.py --pr-branch <PR_BRANCH> --main-branch main` × 2
  SC-1=0 SC-3=2  → 全绿通过
```

两个变体在真实场景下的后果:
- 变体 A: TASK-006 已把 `main_branch` 改成必填参数 ⇒ argparse 直接 `error: the following arguments are required: --main-branch` ⇒ 本仓与所有采用方的 C.2.4 **永久恒红**。
- 变体 B: 本仓 main 分支实际名叫 `master` ⇒ 新增的存在性核验判定 `main-branch-not-found` ⇒ 本仓每次合并 **永久被 BLOCK**; 若某第三方仓库的主分支恰好叫 `main`, 则对方反而"恰好蒙对", 掩盖了硬编码本身的问题。

SC-3 断言测的是 `--pr-branch` 这个 flag 出现的次数——它和 `--main-branch` 传不传、传什么值之间没有任何逻辑关联。proposal 本身在 §1 早已点出同一形状的教训 ("R4-fix…触发 abort ⇒ 把假绿换成了对所有第三方采用方的恒红"), 但那条教训只被用来否决"两分支解析"这个路径形态、并转化成 TASK-002/SC-12 的双向验收 (可达 + 不可达两个方向都建用例), 却**没有对同一条调用里的 `--main-branch` 参数做同样处理**——而 `--main-branch` 的取值恰恰是本 Spec 要治的病灶本体, 不是旁枝。

**这也放大了 TASK-002/SC-12 的价值缺口**: SC-12 (四种 cwd 全可达) 只挂在 TASK-002 (spike 草稿) 名下, TASK-011 (真正写入 SKILL.md 的那条调用) 的验收列表里**没有 SC-12**。也就是说, 即便 TASK-002 的 spike 本身做对了, 也没有任何任务在"抄进 SKILL.md 之后"回头对**落地文本**重跑四-cwd 验证——验证的是草稿, 不是交付物。

**处方方向** (供 A.2 修订参考, 非本席位越权指定实现): TASK-011 需要至少一条独立断言, 同时防"漏写"和"硬编码"两个方向, 例如 `grep -c -- '--main-branch' SKILL.md == 2` **且** `grep -cE -- '--main-branch (main|master)\b' SKILL.md == 0` ——两条缺一都只堵住半边; 并把 SC-12 的复跑挂到 TASK-011 (针对落地文本), 而不只是 TASK-002 (针对 spike 草稿)。

### 2.2 部分 verification 项缺少机械锚点 (m-2, Minor)

TASK-011 第 3/4 条("折叠块须补上存在性核验步" / "去掉全部可执行命令字面量, 含 `:240`") 没有 grep pattern 或测试引用, 依赖人工审阅。我验证了第 4 条里点名的具体缺口是真实的: `:240` 的 `aether --help | grep -q "in-flight"` 是一条本该被清除的可执行命令字面量, 但 SC-1 (`aether ci status`) 和 SC-2 (`"branch": "main"`) 两条 pattern 都不命中它 (逐字核对, 均为 0 命中) ——这个盲区被 A.2 正确识别并标注"须人工核", 这是好的诚实标注, 但没有回答"谁在什么时点做这次人工核对"。TASK-016 ("规则 #8 那段反映新增的分支存在性核验腿")、TASK-017/018 的部分验收项也是同一模式: 给了方法但没给可执行断言。这类任务本质上是文档核对, 天然难以完全机械化, 我不把它升级为 Major, 但建议至少在每条这类任务上补一句"由谁审阅 / 何时审阅"以避免自我声明式收尾。

---

## §3 SC ↔ TASK 覆盖矩阵 —— 以及一个编号命名空间冲突 (C-1, Critical)

先给出正向覆盖矩阵 (proposal SC-1..13, 逐条核对确有承接任务, 无遗漏、无任务引用不存在的 SC):

| SC | 内容摘要 | 红窗任务 | 转绿任务 |
|----|---|---|---|
| SC-1 | `aether ci status` 裸命令清零 | TASK-001 | TASK-011 |
| SC-2 | `"branch": "main"` 示例清零 | **(缺, 见 m-1)** | TASK-013 |
| SC-3 | `--pr-branch` 计数=2 | TASK-001 | TASK-011 (但见 C-2, 维度失明) |
| SC-4 | 三处字面量清零 | TASK-001 | TASK-006 |
| SC-5 | help 文案清零 | TASK-001 | TASK-006 |
| SC-6 | 受控裸仓精确匹配 | — | TASK-003 / TASK-005 / TASK-008 / TASK-009 |
| SC-7 | 128 退出码不重试 | — | TASK-004 / TASK-008 |
| SC-8 | timeout 重试 | — | TASK-004 / TASK-008 |
| SC-9 | 缺 main_branch → TypeError | — | TASK-006 |
| SC-10 | 负控 enabled=false | — | TASK-008 |
| SC-11 | 负控 wait 不变 | — | TASK-008 |
| SC-12 | 四 cwd 全可达 | — | TASK-002 (草稿, 未回补 TASK-011 落地文本) |
| SC-13 | glob 元字符必红 | — | TASK-003 / TASK-005 / TASK-008 |

无 SC 缺任务承接; 无任务凭空引用不存在的 SC 号 (我对 `detailed-tasks.yaml` 全文 `grep -oE 'SC-[0-9]+'` 逐一核对, 命中集合恰为 {1..13}, 与 proposal 表定义域相同)。

**但覆盖矩阵背后有一个更根本的问题**——这 13 个 SC 号本身在仓库里不是"新鲜"的。`test_pre_merge_gate.py` 现有一个类:

```python
class PathCoverageGateTests(_ProbeCacheResetMixin, unittest.TestCase):
    """v1.65.0+ (#122) path coverage × gate 集成 — SC-9/10/11/12/13/15/21/22。
    ...
    """
    def test_sc9_not_applicable_with_inflight_waits_and_skips_pr_query(self): ...   # :623
    def test_sc10_not_applicable_clean_green_with_message(self): ...                 # :634
    def test_sc11_covered_existing_fields_identical_to_disabled(self): ...           # :647
    def test_sc12_default_true_lock(self): ...                                        # :663
    def test_sc13_disabled_no_eval_no_key(self): ...                                  # :672
    def test_sc15_schema_additive_and_early_exit_six_keys(self): ...                  # :683
    def test_sc21_nie_propagates_through_b_axis(self): ...                            # :699
    def test_sc22_no_real_git_subprocess_in_suite(self): ...                          # :710
```

而 `test_path_coverage.py` 头部 docstring 逐字: "覆盖 Spec SC-1~8, 14, 16~20, 23~28 (openspec/changes/phase-c-gate-path-coverage-not-applicable/proposal.md)"，并有 `test_sc1_no_workflow_files` / `test_sc2_real_aria_corpus_regression` / `test_sc3_matching_change_covered` / `test_sc4_block_mapping_push_no_paths` / `test_sc5_flow_list_form` / `test_sc6_paths_ignore_covered` / `test_sc7_all_malformed_unknown` / `test_sc8_git_diff_failure_unknown` 等方法与之一一对应。

两个既有测试文件合起来, **SC-1 到 SC-28 (至少) 都已经是"有主"的编号**, 且是一个已经 ship 的、不相关的 Spec (`phase-c-gate-path-coverage-not-applicable`, v1.65.0, aria-plugin #122)。本 proposal 起了一套**全新但同样从 1 开始**的 SC-1..SC-13, 内容与旧编号风马牛不相及 (旧 SC-12 = "path_coverage_enabled 默认 true 锁定", 新 SC-12 = "helper 路径解析四种 cwd 全可达"; 旧 SC-13 = "disabled 时不评估不留键", 新 SC-13 = "glob 元字符分支名必须精确匹配失败")。

**具体风险路径**:
- `test_pre_merge_gate.py` 现有的既有方法命名清一色遵循 `test_scN_<语义后缀>` 惯例 (8/46 个方法如此, 且集中在文件末尾同一个 class 里, 视觉上极醒目)。TASK-002/003/004/005/008/010 的 verification 数组通篇用"SC-N"指称新criteria, 若 Phase B 实施者 (无论人类还是 AI) 沿用该文件已建立的强惯例去命名新增测试, 在 `test_pre_merge_gate.py` 这一个文件内, SC-9/10/11/12/13 五个号会与既有方法**完全撞号**。
- Python 类体在同名方法上是静默覆盖 (后定义者胜出, 无报错、无警告)——若新方法与旧方法**全名**恰好重合 (比如都简化命名为类似 `test_sc12_...`), 旧的 `test_sc12_default_true_lock` 会被**静默从可执行套件中删除**, 而它是当前 111 条绿测试里真实守护 `path_coverage_enabled` 默认值契约的那一条。即便新旧全名不完全重合, "test_sc12"这个前缀在同一个类里出现两次、含义互斥, 对任何后续用 `grep test_sc12` 定位"SC-12 测的是什么"的人 (包括 TASK-014/015 的执行者、未来的 AB 评审、以及下一次审计) 都是确定性的误导源。
- 本 proposal 自己在多处指示实施者去参照 `path_coverage.py` 复用异常处理模式 (TASK-004), 而 `path_coverage.py` 对应的测试文件 `test_path_coverage.py` 恰好拥有 SC-6/SC-7/SC-8 (与本 proposal 的 SC-6/SC-7/SC-8 同号不同义)——一个被反复要求"去 path_coverage 那边找先例"的实施者, 极容易在 grep "SC-6" 或 "SC-7" 时命中错误文件、错误含义。

**没有任何一条 verification 提及这个冲突或要求消歧命名**——19 条任务里, 唯一显示"注意到"旧 SC-12 存在的地方是 TASK-010 ("test_sc12_default_true_lock (:663) 断言由 `main_branch=\"main\"` 改为 `\"master\"`"), 但那是把它当"既有 24 处调用之一"来改, 并未意识到这个既有名字与**本 proposal 自己的 SC-12**（含义完全不同）撞了号。

**处方方向**: 在 TASK-001 (组 0 最先触碰该测试文件的任务) 层面显式约定一条消歧规则——例如新测试一律不用裸 `test_scN_...` 命名, 改用能体现"属于本 change"的前缀 (如 `test_mainbranch_sc{N}_...` 或直接用语义化描述、在 docstring/注释里写"proposal SC-N"而不进方法名), 并在 TASK-014 (一致性核对任务) 里加一条"repo 内不存在两个语义不同但方法名前缀相同的 test_scN"的检查。

---

## §4 TASK-005 (测试隔离接缝) 的验收够不够

**机制判断本身是对的**: TASK-005 notes 断言"`test_sc22` 的 patch 本就全局生效, 编排层早先的相反陈述已作废"。我独立核验: `path_coverage.py:47` `import subprocess` (模块级), `:87` `subprocess.run(...)`, `test_sc22` (`:718`) 用 `mock.patch.object(pc_module.subprocess, "run", _forbidden)`。因为 `pc_module.subprocess` 就是 `sys.modules['subprocess']` 本身 (Python 模块是进程内单例, `import subprocess` 在任何模块里拿到的都是同一个对象), 这个 patch 打的是**该单例对象的 `run` 属性**, 在 `with` 块范围内对**任何**后续 `subprocess.run(...)` 调用生效, 无论调用方是哪个模块。`pre_merge_gate.py` 目前完全不 `import subprocess` (仅在注释里提及), 新增的 `_verify_branch_exists()` 一旦真的调用 `subprocess.run`, 会在 `test_sc22` 的默认健康路径场景下 (`gate_check()` 走到 `_verify_branch_exists()` 才到 `evaluate_path_coverage`) **撞上这个 patch 并抛 `AssertionError`**——即"转红"而非"静默恒绿"。这条判断准确, notes 里的推翻是有实据支撑的。

**"用一个故意违规的桩验证它会红"是否可执行**: 可执行。在 `test_sc22` 的 `with` 块作用域内构造一段直接调用 `subprocess.run(["git", ...])` 而不经过任何新设的桩接缝的代码路径, 应能观察到 `_forbidden` 触发——这是一个合理、可复现的元测试写法。

**但依赖声明有缺口 (Major)**: `TASK-005.dependencies == [TASK-003]`, 不含 `TASK-004`。TASK-004 的 spike 目标是"异常与重试的复用形态"——如果 spike 结论是复用/抽取 `ci_backends/aether.py:164` 的 `_run_with_retry` (proposal 明确要求"不得再造", 优先考虑复用), 新的 `git ls-remote` subprocess 调用点很可能不落在 `pre_merge_gate.py` 里新写的一段代码, 而是落在被抽取/复用的既有模块 (`ci_backends/aether.py` 或某个新抽出的共享 util) 内——这直接决定 TASK-005 要设计的"接缝粒度 (函数级 vs subprocess 级)"的可选空间: 如果调用点在 `pre_merge_gate.py` 本地新函数里, 函数级 mock (`mock.patch.object(gate, "_verify_branch_exists", ...)`) 是最小侵入的接缝; 如果调用点被抽到了 `ci_backends` 包内, 接缝可能需要设在那个包的层级。TASK-008 (真正落地实现) 正确地把 `[TASK-003, TASK-004, TASK-005]` 全部列为前置依赖, 说明规划者已经意识到三者耦合, 但这一认识没有对称写入 TASK-005 自身的 `dependencies`——TASK-005 在当前 DAG 下可以先于 TASK-004 完成, 若届时按"函数级"假设把接缝钉死, TASK-004 若得出"复用 aether.py"的结论, 有返工风险。

**补充观察** (与上一条互相印证): TASK-008 的 4 条 verification (`detailed-tasks.yaml:176-180`) 里没有一条提到 `test_sc22`——也就是说, 在"新 subprocess 真正被插入 `gate_check()` 主流程"的那一刻 (TASK-008 落地时), 没有任何任务显式要求重新跑一遍 `test_sc22` 确认接缝真的挡住了它。TASK-005 自己执行时 (排在 TASK-006/008 之前也是允许的, 因为它只依赖 TASK-003) 该断言在其执行时点是**恒真**的 (那时还没有新 subprocess 可撞), 真正的考验在 TASK-008 落地后才发生, 却没有任务回头验证。

---

## §5 受控裸仓 fixture (TASK-003 的 SC-6/SC-13) 与 TASK-005 的隔离要求是否冲突

**结论: 不冲突, 且 D6 算法本身经我独立复现是可靠的。**

`mock.patch.object` 作为 context manager 的作用域仅限其所在的 `with` 块/所在测试方法, 不会跨测试方法泄漏。SC-6/SC-13 的新测试方法本身不进入 `test_sc22` 的 `with _forbidden` 块, 因此可以自由发起真实 `subprocess` 调用, 与 `test_sc22` 互不干扰——两者是同一个模块里不同测试方法的独立 mock 作用域, 不存在 fixture 级冲突。

我用真实临时裸仓复现了 proposal §5 D6 决策表的完整三轮实验 (自建 `/tmp` 下的裸仓, 用后清理, 未污染任何仓库文件):

```
场景 1 — 远端只有 refs/heads/wip/master, 用裸分支名 master 查询:
  git ls-remote --exit-code --heads <remote> master
  → 命中 refs/heads/wip/master, exit 0   (尾段 glob 误匹配, 复现 ❌ fail-OPEN)

场景 2 — 远端只有 refs/heads/master (真实分支), 用锚定 pattern 查询:
  "refs/heads/mast*"   → 命中 refs/heads/master, exit 0  (glob 元字符仍被解释)
  "refs/heads/m[a]ster" → 命中 refs/heads/master, exit 0  (字符类仍被解释)
  "refs/heads/maste?"   → 命中 refs/heads/master, exit 0  (单字符通配仍被解释)
  控制组 "refs/heads/master" (完全一致) → exit 0 (正常匹配)
  控制组 "refs/heads/notexist" → exit 2 (正常不匹配)
```

即: 无论是裸分支名的尾段 glob, 还是"锚定 `refs/heads/<name>`"这种半修复, 只要 `<name>` 本身含 glob 元字符, `git ls-remote` 的 pattern 匹配语义都会给出假阳性。proposal 的结论——"必须对**返回的 ref 名列表**做 Python 层精确字符串比较, 不能依赖 `ls-remote` 自身的 pattern/exit-code 语义"——是唯一站得住的方案, 这个技术判断本身是扎实的, 我认为不需要在 Phase B 重新论证。

**唯一的小缺口**: proposal §测试基线的"打桩边界"一段只明文钉了 SC-6 用真实裸仓、SC-7/SC-8 用 mock, **没有明确点名 SC-13 的打桩边界**。TASK-003 (`SC-13: ... 三个 glob 形态 ⇒ 全部 fail`) 和 TASK-005 (`"SC-6/SC-13 能用真实 git 受控裸仓运行"`) 两处**相互一致**地把 SC-13 也归为"需要真实裸仓"一类 (这在技术上也是唯一合理的选择——glob 误匹配是 git 自身的行为, mock 无法真实验证), 所以这不构成任务层面的矛盾, 只是提醒 proposal 那张"打桩边界"表本身有一个可以顺手补全的空位, 不影响本轮任务拆解的可执行性。

我另外确认了 SC-7 声称的退出码 (128 = remote 不存在/坏路径, 129 = 用法错误) 同样可复现 (自建实验, 见上方核验表), TASK-004 的 spike 目标同样有扎实的实证基础。

---

## §6 工时与复杂度估算

19 条任务 `est_hours` 求和 = **55h**, 我用脚本重新汇总核对无误 (2+4+4+3+4+2+2+5+2+3+6+1+2+2+4+2+3+2+2 = 55)。complexity (S/M/L) 与小时数的映射内部自洽 (S ∈ [1,3]h, M ∈ [3,5]h, L = 6h), 没有出现"S 比 M 估时更高"这类明显反常。

依赖图我用脚本解析校验: **19 个 ID 全部唯一, 无任务引用不存在的依赖 ID, 图是无环的 DAG**——机械层面干净。

风险提示 (非硬缺陷): 三条 spike 任务 TASK-002/003/004 合计仅 11h (4+4+3), 而它们要解决的问题——路径解析跨 4 种 cwd (含此前不存在的"模拟 plugin 安装态" fixture, 需要新搭建)、精确比对算法 (proposal 自陈这是"R2 承重 Critical 的真正闭合腿", 已经两次修法失败)、异常/重试复用形态 (M-4 级别的架构决策)——在 proposal 自己的历史记录里, 是耗费 5 轮 25 个 agent-run 才勉强诊断清楚问题边界的同一批设计难点 (虽然此前 5 轮做的是审计而非实现, 工作性质不同, 不能线性类比工时)。11h 对"设计 + 搭 fixture + 实现 + 对齐 SC + 写 spike 结论回写 proposal"这个完整闭环而言偏乐观, 但我没有足够依据把它定为"明显失真"意义上的缺陷, 归入风险提示。

---

## Critical

### C-1 — 本 proposal 的 SC-1..13 编号与仓内既有测试的 SC-9~13/15/21/22 (+ SC-1~8/14/16~20/23~28) 直接命名空间冲突

**锚点**: `aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py:582-587` (`class PathCoverageGateTests` docstring, 逐字"SC-9/10/11/12/13/15/21/22") + `:623/:634/:647/:663/:672/:683/:699/:710` (对应既有方法) + `aria/skills/phase-c-integrator/tests/test_path_coverage.py:1-9` (docstring 逐字"覆盖 Spec SC-1~8, 14, 16~20, 23~28")。均为我本人逐行实读确认, 非转述。

**scope**: TASK-001(红窗) / TASK-002 / TASK-003 / TASK-004 / TASK-005 / TASK-008 / TASK-010 —— 凡引用"SC-N"作为新测试标识的任务全部受影响, 尤以在 `test_pre_merge_gate.py` 同文件内新增 SC-9/10/11/12/13 (TASK-006 的 SC-9、TASK-008 的 SC-10/11/13) 风险最高。

**详见正文 §3**。核心是: 本 Spec 从零起了一套 SC-1..13 编号, 与仓内一个已 ship (`phase-c-gate-path-coverage-not-applicable` #122, v1.65.0) 的旧 Spec 编号完全重叠, 且旧编号已经绑定在 8 个现存、当前全绿、遵循 `test_scN_<语义>` 强命名惯例的测试方法上。19 条任务里没有一条识别或处置这个冲突。轻则新旧"SC-12"/"SC-13"等术语在同一文件内产生歧义, 重则若方法全名巧合重合会被 Python 静默覆盖删除既有回归测试——这正是本方法论最忌惮的"假绿"形状 (memory `feedback_false_green_dual_is_permanent_red`)。

**blocks_phase_b**: true —— 在 TASK-001 开始写第一个新测试方法之前就需要一条消歧命名规则, 否则后续 6 条任务都会带着这个隐患往前走。

### C-2 — TASK-011 (D1 承重) 的验收对"main-branch 取值/存在与否"这个病灶维度完全失明

**锚点**: `detailed-tasks.yaml:232-236` (TASK-011 verification 全集) / `proposal.md:198` (SC-3 定义) —— 均为我本人实读; 违规变体为我本人现场构造并实跑 grep 验证 (见正文 §2.1 命令输出)。

**scope**: TASK-011。

我独立构造两个会导致本仓或第三方仓库恒红的 SKILL.md 改法 ("--main-branch 完全不传" / "--main-branch 硬编码为字面量 main"), 两者均 100% 通过 TASK-011 现有的 SC-1/SC-2/SC-3 三条机械断言。SC-3 测的是 `--pr-branch` flag 出现次数, 与本 Spec 要治理的 `--main-branch` 病灶不在同一维度, 断言的"不变量维度"与"错误的维度"不匹配 (memory `invariant-dimension`)。同时 SC-12 (四 cwd 全可达) 只挂在 TASK-002 spike 名下, 从未在 TASK-011 落地文本上复跑。

**blocks_phase_b**: true —— 这是本 Spec 最核心的承重任务 (D1), 验收网眼比缺陷粗一档意味着"实施完成"这个信号本身不可信。

---

## Major

### M-1 — proposal §1 关于 `SKILL.md:262/:559/:610` 使用 `${CLAUDE_PLUGIN_ROOT}` 的引用与源文件字面不符, 已被 TASK-002 逐字复述

**锚点**: `proposal.md:64` ("`SKILL.md:262` / `:559` / `:610` 均用它" [指 `${CLAUDE_PLUGIN_ROOT}`]) / `detailed-tasks.yaml:63` (TASK-002 verification#3: "须核 CLAUDE_PLUGIN_ROOT…与 SKILL.md:262/:559/:610 的既有约定是否可直接沿用") vs 我本人 `sed -n '262p;559p;610p'` 实读 `SKILL.md` 的结果。

**scope**: TASK-002 (直接), TASK-014 (下游一致性检查因此输入受污染)。

三行实际字面均为 `${ARIA_PLUGIN_ROOT:-aria}` (`:262` pre_merge_gate.py 定位 / `:559` submodule_gate.sh 定位 / `:610` git-remote-helper 降级探测), `CLAUDE_PLUGIN_ROOT` 在整个 `SKILL.md` 里只出现一次 (`:737`, 与本 change 无关的 aria-token-telemetry 脚本), 与这三行完全不重合。TASK-002 verification#3 逐字复述了这个错误归因。虽然该条措辞用的是"须核" (要求验证而非直接采信), 给 spike 执行者留了自行发现矛盾的空间, 但风险仍然真实: `:559`/`:610` 两行分属 `submodule_gate.sh` / `git-remote-helper` 两个与本 Spec 无关、proposal §Impact 未列入变更范围的 helper, 若 TASK-002 依循这条被污染的引用在 `:262` 引入 `CLAUDE_PLUGIN_ROOT`, 而 `:559/:610` (超出本 Spec 改动范围) 依然是 `ARIA_PLUGIN_ROOT`, 文件内就会产生两套环境变量并存——恰是 TASK-014 ("全文无互斥两套") 存在的目的所要拦截的那种缺陷, 而 TASK-014 自身的判断依据 (`:262/:559/:610` 一致) 又源自同一条被污染的引用。

**blocks_phase_b**: true —— 应在 TASK-002 启动前修正这条输入陈述, 成本极低 (改一句话), 但不修正的话它会带着错误的"既有约定"预设进入一个本该完全靠现场证据决策的 spike。

### M-2 — TASK-005 (测试隔离接缝) 的 `dependencies` 遗漏 TASK-004, 且 TASK-008 落地时无人回头复核该守卫

**锚点**: `detailed-tasks.yaml:118` (TASK-005 `dependencies: [TASK-003]`) vs `:173` (TASK-008 `dependencies: [TASK-003, TASK-004, TASK-005]`) / `:176-180` (TASK-008 verification 全集, 未提 `test_sc22`)。均为我本人实读。

**scope**: TASK-005 / TASK-008。

详见正文 §4。TASK-004 的 spike 结论 (新 `git ls-remote` subprocess 调用是自己新写在 `pre_merge_gate.py` 里, 还是复用/抽取 `ci_backends/aether.py:164` 的 `_run_with_retry`) 直接决定新调用点落在哪个模块, 从而决定 TASK-005 要设计的"接缝粒度 (函数级 vs subprocess 级)"的可选空间——但 TASK-005 的依赖列表只含 TASK-003, 不含 TASK-004。TASK-008 (真正把新 subprocess 接入主流程的任务) 正确地把三条 spike 全部列为前置依赖, 说明规划者已意识到三者耦合, 但这一认识未对称写入 TASK-005 自身; 且 TASK-008 的 4 条 verification 里没有一条要求在新 subprocess 落地后重跑 `test_sc22` 确认接缝依然有效——该守卫目前只在 TASK-005 自己执行的、新 subprocess 尚不存在的更早时点被验证过一次 (那时该断言恒真), 真正的考验时刻 (TASK-008 落地后) 无人回头复核。

**blocks_phase_b**: false —— 不阻塞 TASK-001 起步, 但建议在组 0/组 1 交界处补上这条依赖边和一条"TASK-008 完成后 `test_sc22` 仍须绿"的显式验收, 避免先设计接缝、后被 TASK-004 结论推翻返工。

---

## Minor

### m-1 — SC-2 未进入 TASK-001 的红窗空壳

**锚点**: `detailed-tasks.yaml:39-44` (TASK-001 verification, 仅 SC-1/3/4/5 四条) / `proposal.md:197` (SC-2 定义, 与 SC-1/3/4/5 同样标注"零裁量")。

SC-2 与其余四条同类同形 (纯 grep 断言, 今日实测 1, 期望 0), 却未被纳入 TASK-001 的"先看到全红"红窗, 最终由 TASK-013 单独认领。不构成阻塞 (TASK-013 会转绿它), 但破坏了"组 0 = 全部 TDD 前置断言先见红"这条 tasks.md 自陈的组织完整性, 且没有说明理由。

### m-2 — 部分 verification 项缺少机械锚点, 依赖未指名主体的人工审阅

**锚点**: `detailed-tasks.yaml:235-236` (TASK-011 第 3/4 条) / `:322-323` (TASK-016) / `:337-339` (TASK-017 第 1/2 条)。

这几条验收给出了"要检查什么"但没给出可执行断言或指名"谁在哪个环节做这次检查"。其中 TASK-011 第 4 条点名的 `:240` 缺口经我核实是真实存在的盲区 (SC-1/SC-2 两条 pattern 均不命中该行, 我已实测确认), 说明 A.2 对盲区本身的识别是准确的, 只是没有配套一个可执行或至少可追责的核验步骤。

### m-3 — TASK-015 (AB 基准) 的依赖遗漏同样编辑 SKILL.md 的 TASK-012/TASK-014

**锚点**: `detailed-tasks.yaml:299` (TASK-015 `dependencies: [TASK-011, TASK-013]`) vs `:249` (TASK-012 deliverable = SKILL.md) / `:286` (TASK-014 deliverable = SKILL.md)。

若严格按 `detailed-tasks.yaml` 的细粒度依赖边执行 (而非 `tasks.md` 组级"组 2 全部完成后才进组 3"的隐含顺序), TASK-015 可能在 TASK-012/014 尚未落地前就对 SKILL.md 跑 AB 基准, 需要重跑才能满足 Rule #6"零裁量"的要求。`tasks.md` 的分组结构大概率能在实践中兜底这个问题, 但形式化依赖图本身不完整, 与 M-1 (proposal §1 vs 决策表 D2 的类似"字面没跟上意图"问题) 是同一形状的偏差, 建议一并扫一遍。

### m-4 — 三条 spike 任务的工时估算相对历史难度可能偏乐观

**锚点**: `detailed-tasks.yaml:33-108` (TASK-002/003/004, 合计 4h+4h+3h=11h) / `proposal.md:3` (post_spec R1–R5, 25 agent-run 才诊断清楚这批问题的边界)。

不构成"明显失真"的实证结论 (工作性质不同, 审计轮次与实现工时不能线性类比), 仅作为风险提示: TASK-002 需要新搭一个此前不存在的"模拟 plugin 安装态"fixture, TASK-003 是 proposal 自陈的"R2 承重 Critical 的真正闭合腿"(已两次修法失败), 两者的 4h 预算偏紧。

---

## Verdict

**FAIL** (≥1 Critical)

- Critical 2 / Major 2 / Minor 4
- C-1 与 C-2 是两类不同的失效: C-1 是"验证基础设施本身的命名空间与既有资产冲突", C-2 是"验证的量纲选错, 挡不住它声称要挡的缺陷"。两者都要在 Phase B 动笔写第一个新测试方法之前解决, 否则 TASK-001 建立的"红窗"从一开始就立在不稳的地基上。
- M-1 与 memory `delegate-verify` 同形: 引用一处源码去承载一个"既有约定"判断之前, 没有去那一处核对字面。这是本项目反复复发的失效模式 (proposal 自己在 §1 就纠正过一次"`ARIA_PLUGIN_ROOT` 全仓未赋值"的测错总体, 而修正后的新论据本身又带了一个新的字面错误), 建议 A.2 修订时对全部 19 条做一次"凡出现『沿用既有约定 / 参照 X』, 逐处回源核字面"的横扫, 而不是只改 TASK-002 这一处。
- M-2 是"验收断言可评估时点"与"真正的考验时点"错位的一个例子: TASK-005 在新 subprocess 尚不存在时就能"通过", 真正接缝生效与否要到 TASK-008 落地才见分晓, 但没有任务在那个时点回头复核。建议 A.2 补一条通用规则: 每条 verification 都要能在它所在任务**完成的那一刻**求值, 而不是在依赖链更早的某个时点就已经恒真。
- 本席位的核验方法论: 所有 SC 表数字、行号、退出码、模块单例语义、既有测试方法名, 均为本人实读或实跑确认, 未采信任何文档的自陈值; SC-6/SC-13 的核心算法 (D6) 经我独立复现的受控裸仓实验证实technically sound, 不在本轮的问题清单里。

**建议**: REVISE。C-1 (命名空间冲突) 与 C-2 (TASK-011 验收维度失明) 必须先处理——两者都是"验证机制本身有洞"而非"实现思路有洞", 与本 Spec"让测试自己发红"的核心押注直接相关。M-1/M-2 建议顺带用同一次修订处理 (前者改一句验证语句, 后者补一条依赖边 + 一条 TASK-008 时点的复核断言)。Minor 四条可与上述同批带走, 不构成独立阻塞。

---

## 轮次记录

| 轮 | 席位 | Critical | Major | Minor | verdict | 备注 |
|---|---|---|---|---|---|---|
| R1 | qa-engineer | 2 | 2 | 4 | FAIL | 首轮, 镜头 = 测试策略与可证伪性。全部 finding 均基于本席位自己实读的行号/自己实跑的命令 (含 3 组自建受控裸仓实验、1 组违规 SKILL.md 片段构造实验、1 次全量 pytest 运行、1 次依赖图程序化解析), 无一条转述 proposal 的"今日实测"列或其他文档自陈。 |

**本轮未做的事** (供后续轮次或其他席位接力):
- 未对 `standards/openspec/project.md:21` vs `:118` (detailed-tasks.yaml 是否为 Level 3 强制项) 的表述不一致做裁定——不在 qa-engineer 镜头内。
- 未核 `.aria/config.json` 里 `phase_c_integrator.pre_merge_gate` 是否有 `main_branch` 兜底键——若其他席位已核, 可与本报告 C-2 的"硬编码风险"结论互相印证。
- 未评估 TASK-014 是否越出 proposal §Impact 范围 (`:559/:610` 涉及的两个 Spec 外 helper)——这是架构/范围边界问题, 不在本镜头内, 但与本报告 M-1 共享同一处引用错误的根源, 建议一并处理。

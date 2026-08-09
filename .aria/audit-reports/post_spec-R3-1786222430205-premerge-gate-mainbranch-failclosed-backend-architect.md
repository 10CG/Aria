---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-08T21:21:59.192Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R3 审计报告 — backend-architect

> 审的是**当前 186 行** `proposal.md`(R2-fix 大幅减法后)。不复核 R1/R2 旧清单;镜头 = 实现可行性与接口契约。全部结论基于本次实读/实跑,证据附命令与输出。

## 方法论说明

本轮我独立跑通了以下只读验证(均在 `/home/dev/Aria` 工作树内,零文件改动;一处受控实验建在 `/tmp` 标准 scratchpad,不碰仓库):

1. 全文读 `pre_merge_gate.py` / `ci_backends/{aether,base}.py` / `path_coverage.py` / `SKILL.md` / `test_pre_merge_gate.py`(§Impact 提及的关键区段全读,非抽样)。
2. `python3 -m pytest aria/skills/phase-c-integrator/tests/ -q` → **111 passed**,且 `test_pre_merge_gate.py`/`test_ci_backends.py`/`test_path_coverage.py` 分别 collect **46/25/40**,与 §测试基线 逐字一致。
3. 定向跑通 4 个当前**遗漏 `main_branch` 且穿过某条早退分支**的既有测试(见 Finding A),确认它们**今日全绿**。
4. 在 `/tmp` 建最小 argparse + 函数复现两种"必填"失败的时机/形态,证实 SC-M1/SC-M2 对失败形态(RC=2 vs `TypeError`)的刻画准确。
5. 全仓(不限 `aria/`)grep `pre_merge_gate|gate_check`,并单独检查 `aria-orchestrator/` 子模块,核实 §Impact 的 blast-radius 处方范围。
6. 对 `DEFAULT_CONFIG`(9 键)、`_OLD_TO_NEW` alias 表、`_load_config_from_file`→`gate_check` 的参数流做逐行复核。
7. 对 SKILL.md 全文 15 处独立 `\bmain\b` 命中逐条分类,核 SC-M5 grep 模式有无漏判。

---

## 审计结论

### 复核 R3 待办三问(Spec §审计轨迹 末段点名)

**(a) 必填是否真的关掉了所有静默路径 —— 结论「关得干净」是否成立?**

对**配置注入**这一具体维度成立、且已独立复核:

- `DEFAULT_CONFIG`(`pre_merge_gate.py:53-65`)实读 **9 键**(`enabled/ci_backends/no_ci_fallback/wait_timeout_seconds/wait_check_intervals/primitive_call_timeout_seconds/poll_chunk_seconds/user_escape_hatch/path_coverage_enabled`),无 `main_branch`。
- `_OLD_TO_NEW`(`:69-72`)只两条映射:`primitive_preference→ci_backends`、`no_aether_fallback→no_ci_fallback`,`_translate_value`(`:75-91`)对应两分支穷尽,无第三条把任何旧键翻译成 `main_branch`。
- `_load_config_from_file`(`:410-421`)只读 `.aria/config.json` 的 `phase_c_integrator.pre_merge_gate` 子块并原样传给 `config=` 形参;CLI `main()`(`:435-437`)对 `main_branch` 只用 `args.main_branch`,**从不**读 `cfg["main_branch"]`——纵使用户手滑在 config.json 里写了 `"main_branch": "master"`,也会被静默无视(不报错,但也不生效)。这点 Spec 未言明,但不构成"静默放行"(不影响 verdict 正确性,只是一个惊讶点),故不升级此点本身为独立 finding,并入 Finding A 讨论。

但"结构上不受影响"这个更强断言(§非目标末条)在**调用方体验**维度**不成立**——见 **Finding A**(Major)。

**(b) §移出面 四条是否真解耦,有无残留依赖?**

确认解耦干净。`grep -rn "symbolic-ref\|ls-remote --symref\|ls-remote --exit-code\|main_branch_resolved\|gate_error" aria/skills/phase-c-integrator/` 唯一命中在 `tests/test_submodule_gate.sh:565`(`git symbolic-ref -q HEAD` 用于检测 detached HEAD),属 C.2.4.5 子模块门禁的另一机制,与本 Spec 的 `main_branch` 参数无关。四条移出面的理由本身也经交叉检查站得住:尤其"分支存在性核验"一条,Spec 已明确区分"显式传错值"(存在性核验治的)与"缺省是错值"(本 Spec 治的)是两个不同缺陷(§移出本 Spec 的面 表格第 2 行)——这意味着本 Spec **只堵上"忘记传参→默认到错误分支"这一条路,不堵"显式传了一个仍然错误的分支名"**;但由于 (b) 腿 aether 语义未变(§非目标"不改 aether CLI 返回语义"),显式错值场景不是新引入的风险,是已知且被主动移出的既有风险面,不算本轮"cut 太多"。

**(c) SC-M4/SC-M5 grep 模式是否会漏(大小写/引号形态/跨行)?**

不会漏。独立复跑:

```
SC-M4: grep -n '"main"\|\[--main-branch main\]' pre_merge_gate.py → 命中 :21 / :300 / :427,共 3 处,与表格逐一对应
SC-M5: grep -n -- '--branch main|"branch": "main"' SKILL.md → 命中 :167 / :243 / :270,共 3 处,与表格逐一对应
```

进一步核了 SKILL.md 全文全部 15 处独立 `\bmain\b` 命中(非仅 SC-M5 目标模式),逐条分类:3 处是待改字面量(已覆盖)、2 处已是占位符形态(`<main>...<pr>`,`:242` 本行)或纯散文提示、6 处是"main 分支"概念性叙述(不含可执行字面量)、2 处是"main **仓**"(vs submodule,`:528`/`:550`,与分支名无关)、2 处是 C.2.5 推送矩阵示例标签(`:604`/`:605`,同样是"主仓"非"main 分支")。**唯一一处在 SKILL.md 别处、语义上与本 Spec 同形却未被列入同批**的是 `:765` `skip_if: in [develop, main]`(见 Finding D,Minor,判定为可接受的显式范围外)。SC-M4/SC-M5 两条断言本身的模式设计(大小写敏感全字匹配 `"main"`/`--branch main`/`"branch": "main"`)对其**声明的目标**(C.2.4 相关的 3+3 处)是精确的,没有漏判。

---

## Findings 详述

### Finding A(Major)—— §非目标"结构上不受影响"断言对调用方边界不成立,已有 4 个现绿测试实证

**锚点**:`proposal.md` §非目标 末条("不动 no_ci_fallback / stub backend 既有降级语义...该语义结构上不受影响");`pre_merge_gate.py:298-360`(`gate_check` 三个早退分支 + `main_branch` 首次被读取的位置);`tests/test_pre_merge_gate.py:272`(`test_case_f_outdated_binary_fails_fast`)/`:299`(`test_disabled_skips_to_green`)/`:309`(`test_no_backend_skip_with_warning`)/`:319`(`test_no_backend_abort`)。

**问题**:`gate_check` 函数体内三个早退分支——`enabled=false`(`:328-335`)、`backend is None`→`no_ci_fallback`(`:337-339`)、`precheck() 失败`(`:344-352`)——**结构上从不读取 `main_branch`**(该形参首次被消费是 `:358-359` 的 `evaluate_path_coverage(main_branch=...)`,严格晚于三个早退分支)。这意味着**今天**这三条路径可以在完全不传 `main_branch` 的情况下正常工作(拿到默认值 `"main"` 但从未被使用)。我实跑确认这不是理论推演:

```
$ python3 -m pytest tests/test_pre_merge_gate.py -q \
    -k "test_disabled_skips_to_green or test_no_backend_skip_with_warning or test_no_backend_abort or test_case_f_outdated_binary_fails_fast"
....                                                                     [100%]
4 passed, 42 deselected in 0.04s
```

四个测试各自的调用点(`:301`/`:311`/`:321`/`:282`)全部形如 `gate.gate_check(pr_branch="feat/x", config={...})`,**均不传 `main_branch`**,且分别精确对应上述三个早退分支之一(`test_disabled_skips_to_green` 甚至显式 `m_resolve.assert_not_called()` 断言连 backend 解析都没发生)。

必填改动落地后,这四处调用**在触及 `enabled`/`no_ci_fallback`/`precheck` 判断之前就已 `TypeError`**——因为 Python 的实参绑定发生在函数体执行**之前**。用最小复现验证了这个时机差异(不改仓库文件,`/tmp` 内独立脚本):

```
--- function experiment: call without main_branch, config={'enabled': False} ---
TypeError: gate_check_sim() missing 1 required positional argument: 'main_branch'
```

这个 `TypeError` 在函数体的第一行代码执行前就抛出——**比"结构上不受影响"所指的『gate_check 内部早退分支之前』还要早一层**。所以 §非目标 的字面断言("不在 gate_check 内新增任何早退前的逻辑")在"函数体内没加新代码"这个窄含义上是对的,但它营造的印象——no_ci_fallback / 禁用 backend / 关闭闸门这些降级路径的**可达性**不受影响——是不准确的:这些路径本身的行为(返回值)确实没变,但**到达它们的方式**从"main_branch 传不传都行"变成了"main_branch 必须先给出一个值(哪怕这个值在这条路径上根本不会被用到)"。

**这不是隐蔽回归**——它被 §Impact"既有测试必然要动"段落的"24 处 `gate_check(` 调用点...全部 24 处 `TypeError`"机械兜底覆盖,Phase B 跑测试会红。**但 §非目标 的措辞本身需要更精确**,否则容易让后续读者(包括下一次 audit、或 6 个月后来查这份 Spec 的人)误以为"关闭闸门"这个逃生舱在编程接口层面 100% 免疫于本次改动,而实测证明并非如此。

**建议**:把 §非目标末条改写为类似:"gate_check 函数体内部的分支逻辑不变;但必填参数把『能否进入函数体』的检查点前移到调用表达式本身——即便 `enabled=false` 或无可用 backend 等 main_branch 实际不会被读取的路径,调用方现在也必须先能提供一个 main_branch 值。这是本次改动的预期后果,不是回归,4 个现有测试(`:272`/`:299`/`:309`/`:319`)已通过强制补参覆盖。"或者至少在 §风险 段补一句点名这个子情形,而不是让它完全隐藏在"既有测试必然要动"的机械改动清单里。

`introduced_by_r2fix: true`(必填设计本身引入)`cut_too_much: false`(不是"砍多了"的问题,是**剩下的东西**自身断言不精确)。

---

### Finding B(Major)—— ship target 声称 PATCH,但改动本身是教科书式破坏性 API 变更

**锚点**:`proposal.md:10`("ship target: PATCH")、`proposal.md:53`("不传参的行为: CLI → argparse 报错退出 (RC=2); 函数 → TypeError")、`CLAUDE.md` §协作原则("向后兼容 (破坏性变更须 MAJOR)")、`standards/conventions/version-management.md` §2.1。

**问题**:Spec 自己在 §What Changes(`:53`)白纸黑字承认这个改动让"不传参"从**成功**变成**硬失败**(CLI `RC=2`,函数 `TypeError`)——这是 SemVer "MAJOR version when you make incompatible API changes" 的教科书场景:CLI 参数由可选变必填、Python 函数签名去缺省值,两个公开调用面同时对现有调用方**不兼容**。

`CLAUDE.md` 明文列出的协作原则含"向后兼容 (破坏性变更须 MAJOR)"。`standards/conventions/version-management.md` §2.1 把 MAJOR 触发条件框定在"方法论核心结构变更"层面(十步循环步骤增减、OpenSpec 格式不兼容),没有专门覆盖"某个 Skill 内部脚本的 CLI/函数签名破坏性变更"这个更细粒度的场景——但 `aria/CHANGELOG.md:2958` 一条既有记录写着"CHANGELOG 注明: **无 breaking change**",说明项目确有"显式标注变更是否 breaking"的既往实践。本 Spec 目前对这个问题**完全沉默**:既没有引用"这是 Aria 约定里的 bug fix = PATCH"来自证 PATCH 合理,也没有讨论过为什么一个自认是"硬失败"的调用面变更不需要 MAJOR(或至少 MINOR)。

不认为这个 gap 应该阻塞本 Spec 的核心修复(修复方向是对的,fail-open bug 是真实且该修),但**版本号标注 PATCH 而实际是 breaking 的组合本身会误导下游**:一个只扫 MAJOR/MINOR bump 决定"要不要认真看这次升级"的消费方(例如通过 `git submodule update --remote` 被动拉取 aria 子模块的项目)会完全看不到这次变更。

**建议**:至少在 §Impact 版本行补一句显式裁决("虽是 breaking change,但因为... 归入 PATCH"或者改口径为 MINOR),并在落地时的 CHANGELOG 条目里明确标注 "Breaking: `pre_merge_gate.py --main-branch` / `gate_check(main_branch=...)` 由可选变必填",与 `:2958` 那条先例的透明度对齐。

`introduced_by_r2fix: true` `cut_too_much: false`。

---

### Finding C(Major)—— blast-radius grep 口径限定在 `aria/`,未覆盖跨项目分发面

**锚点**:`proposal.md` §风险("Phase B 须 `grep -rn "pre_merge_gate\|gate_check" aria/ --include=*.py --include=*.md` 核全部调用方")、§Impact 表(无下游通知/协调行)、`CLAUDE.md` `project_kairos_adopter` memory(Kairos 是 Aria 首个跨项目采用者)。

**问题**:我按同样模式跑了一次**不限定 `aria/`** 的全仓 grep,并单独查了 `aria-orchestrator/` 子模块(结果:零命中,说明它目前不直接调用这两个符号,符合它经 Claude Code 动态 shell 出去而非静态 import 的调用方式)。结论是:**在这个 meta-repo 范围内**,`aria/` 限定的 grep 口径今天是够用的——没漏掉任何真实调用方。

但这条 grep 处方**结构上无法覆盖 aria-plugin 的真正分发面**:aria-plugin 经 marketplace / `git submodule update --remote` 分发给外部消费方(memory `project_kairos_adopter.md` 记录 Kairos 是首个跨项目采用者),这些消费方仓库里可能存在的调用点(尤其是**非 AI 驱动**的硬编码脚本/cron,不遵循 SKILL.md 散文里"main_branch 必须显式传真值"的既有约定)对本仓 grep 完全不可见。§Impact 表列了"外部 | aria-plugin #137 body 加删除线..."和"follow-up issue",但**没有任何一行是"通知/协调已知下游采用方"**——这与 Finding B 指出的 breaking-change 定性缺口是同一个根问题的两个侧面:如果确实认定这是可以 PATCH 下去的改动(不广播),那至少应该说明"已知下游都通过 AI 编排调用、必然显式传参,所以此处安全"这个前提本身,而不是把 grep 范围留在能看见的地方就停手。

**建议**:§Impact 加一行"已知外部采用方(Kairos 等)是否受影响待核实/待通知",或者显式论证"因为调用方式是...,所以跨仓 grep 不必要",把这个假设从隐含变成明文。

`introduced_by_r2fix: false`(这个 gap 在 R1/R2 版本里应该同样存在,只是这次 186 行版本依然未补)`cut_too_much: false`。

---

### Finding D(Minor)—— SKILL.md:765 同形字面量未列入本批("develop"/"main" 分支跳过规则)

**锚点**:`aria/skills/phase-c-integrator/SKILL.md:765`(`skip_if: in [develop, main]`,§跳过逻辑 C.2 分支)。

**问题**:这行假设项目主分支字面量是 `"main"`(或 `"develop"`),语义上与本 Spec 治的"硬编码 main 当作项目主分支"是**同一个坏味道的兄弟实例**——如果 AI 严格按字面匹配这条规则,Aria 自己的 `master` 分支不会被识别为"主分支,跳过 PR"。但这行属于**完全不同的机制**(C.2 是否需要创建 PR 的判断,而非 C.2.4 pre-merge gate 的 main-in-flight 检查),且失败方向相反(不是 fail-open 静默放行,顶多是"该跳过 PR 时没跳过,多创建一次 PR",不构成安全问题),也不在 §Impact 列出的任何文件:行号范围内。判定为**合理的范围外**(owner 已经把这轮压缩到"只改三处字面量",不应借审计之机顺带扩大 diff),但作为"下一批 follow-up issue"的候选点值得记一笔,避免以后又要单独发现一次。

`introduced_by_r2fix: false` `cut_too_much: false`(不是被砍掉的,是从未被纳入过)。

---

### Finding E(Minor)—— §移出本 Spec 的面 表格"(a) 腿 not_applicable 通路"行的"见下方风险"指向含糊

**锚点**:`proposal.md` §移出本 Spec 的面 表格最后一行("(a) 腿 `not_applicable` 通路 | 见下方风险 —— 本 Spec **不改变**它")、§风险 小节(`proposal.md:161-163`)。

**问题**:通读 §风险 小节,内容是"忘记传参从静默放行变硬失败"的一般性讨论,并没有专门针对 (a) 腿 `not_applicable` 通路的段落。交叉核实后 (a) 腿本身确实不受影响(`path_coverage.py` 对错误的 `main_branch` 值走 "git diff 失败 → unknown"、fail-toward-covered,这个既有行为本 Spec 没有触碰,§非目标也明确"不改 path_coverage.py 代码"),所以内容本身没错,只是"见下方风险"这个指针找不到明确对应的小节,读者要自己拼。文档精度问题,不影响正确性。

`introduced_by_r2fix: false` `cut_too_much: false`。

---

## Verdict

**PASS_WITH_WARNINGS**(0 Critical + 3 Major + 2 Minor)。

判据复核:verdict 规则 = 0C+0M→PASS;0C+≥1M→PASS_WITH_WARNINGS;≥1C→FAIL。本轮未发现 Critical——核心机制(三处字面量去缺省、CLI/函数双路径同批改、SC-M1..M5 可复跑 grep/TypeError 断言)在我独立实读+实跑下均成立,§移出面 四条的解耦断言与 R3-preview (a)(b)(c) 三条待验结论也都独立复核通过。3 条 Major 全部指向"**已保留在本 Spec 内的那部分内容,其自身文字断言比实际行为更强/更乐观**"(§非目标措辞、版本定性、blast-radius 口径),而不是"核心修复机制本身有缺陷"或"被砍掉的东西不该砍"——这与 R3 的风险预期("砍掉的东西是否真的可以砍")吻合:我没有找到"砍多了"的证据,找到的是"剩下的三句断言需要更精确"。

不建议因这些 Major 发起 R4。理由:(1) 三条都是**文档精度/流程完备性**问题,不是代码逻辑缺陷,修法是在 Spec 里加几句话/加一行表格,不改变已经定型的"三处字面量必填"这个核心设计;(2) 已有 owner 明确裁定(R2 后)"两条成文判据同时点亮 ⇒ 停止审计→重写循环,改减法+spike-first",本轮 Major 不满足那两条判据(不是 major 数上升、不是本轮 fix 引入占比过半——因为压根不是在评估一个"这轮 fix",是在评估一个新提案的自证完整性);(3) Phase B 的 SC-M1..M5 实跑是下一道验证,3 条 Major 里没有一条会被那五个 SC 挡住或推翻。

---

## 轮次记录

| 轮 | 席位 | vote | 备注 |
|---|---|---|---|
| R1 | 5 | 5/5 REVISE | 见 `.aria/audit-reports/post_spec-R1-1786216818583-*-aggregate.md` |
| R2 | 5 | 5/5 REVISE | 见 `.aria/audit-reports/post_spec-R2-1786220900000-*-aggregate.md`;major 10→15 上升,fix 引入占比 100% ⇒ owner 裁定停止审计→重写循环,改减法 |
| R3(本席) | backend-architect | **PASS**(内容判定,附 3 Major 警告) | 全文实读 + 111 测试实跑 + `/tmp` 受控实验 + 全仓 blast-radius 复核;0 Critical,判 PASS_WITH_WARNINGS,不主张进 R4 |

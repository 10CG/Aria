---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-09T10:32:00.000Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R5 · qa-engineer · premerge-gate-mainbranch-failclosed

镜头: SC-1..SC-12 断言设计本身 (量取对了吗) / SC-3 红绿窗口 / SC-6·7·8 打桩边界 / 「测试隔离」段处方可行性 / 三条负控是否恒绿 / SC 集覆盖空洞。只审当前 271 行 `proposal.md` 本身, 未核对 R1-R4 旧清单。全部 finding 均实读 `file:line` 或实跑命令/最小 repro 得出。**未修改本仓任何文件, 未 commit/push。**

方法: 逐条重跑 SC-1..SC-5 的 grep pattern 并核对「今日实测」列 · 通读 `test_pre_merge_gate.py` 全 748 行确认 24 处 `gate_check(` 调用点与 `test_sc22`(:710) 现状 · 通读 `pre_merge_gate.py` 全文确认 §4/§5/§6 行锚点 · 通读 `test_path_coverage.py` 确认 `_RepoFixtureMixin` 精确形态 · 独立实测本机 plugin marketplace 安装态 + `standards`/`aria-orchestrator` 两子模块的路径可达性。

---

## 审计结论

**核验通过的部分** (先列, 避免"全是问题"的失真印象): SC-1..SC-5 的 5 条 grep pattern 与"今日实测"列逐条重跑，计数与行号（`:167`/`:168`/`:243`/`:244`、`:270`、`:427`/`:300`/`:21`）全部吻合；SC-9 (`TypeError`) 设计上零裁量、正确；24 处 `gate_check(` 调用点中显式传 `main_branch=` 的确为 0 处（唯一疑似命中 `:669` 是 `pc_eval.assert_called_once_with` 的断言参数，不是 `gate_check` 调用参数）；SC-11 设计上是干净的透传验证，未发现问题。

**核心判断**: 本轮的失败面集中在两类，与既有的四轮规律（fix 环节新造等量问题）一致：(1) 我独立验证并确认了本轮另两席（tech-lead / code-reviewer）已各自发现的同一个结构性 Critical —— §1「唯一执行入口」的两分支路径解析在 plugin 市场安装态与 `standards`/`aria-orchestrator` 两个子模块根 cwd 下**全部**不可达，而后者是 CLAUDE.md 硬约束 1 钦定的合法执行位置；(2) 我独立发现了一处另两席未覆盖的 QA 专属缺口 —— 「测试隔离」段新写的「为 gate 层核验建独立打桩接缝」处方，粒度未定，与 SC-6（禁打桩）、SC-8（须保留真实重试/退避逻辑）之间存在结构性张力，Spec 全文没有回答「这个新桩加在哪一层、SC-6/7/8 是否需要脱离共享 mixin 的独立测试类」。

---

## Verdict

**FAIL**（≥1 Critical，与本轮 tech-lead / code-reviewer 独立收敛）。

- 1 Critical（跨席独立确认）+ 3 Major + 2 Minor。
- **blocks_phase_b = true 的两条**: CRIT-1（路径解析）· MAJ-2（SC-3 承重断言的落点矛盾, Phase B 第一步就卡住）。
- 本报告的独有贡献是 MAJ-1（测试隔离粒度未定 × SC-6/8 冲突）——通读另两席报告后确认此点未被覆盖；其余发现与另两席收敛，本报告给出的是**独立复现路径**（不同命令、同一结论），提升该组发现的置信度，而非转述。

---

## Findings

### CRIT-1（architecture）· §1 两分支路径解析在 plugin 安装态与 2/3 合法子模块 cwd 下结构性不可达 ⇒ Rule #8 闸门从「恒绿」变「恒红」

**锚点**: `proposal.md:48-53`（§1 调用块）+ D2 `:159` + SC-12 `:189` vs CLAUDE.md「多远程推送 — 约束 1」+ `SKILL.md:242`

**独立实证**（未参考另两席报告前先跑，之后核对结论一致）：

```
$ find /home/dev -iname "pre_merge_gate.py"
/home/dev/.claude/plugins/marketplaces/10CG-aria-plugin/skills/phase-c-integrator/scripts/pre_merge_gate.py   ← 活的插件安装副本
/home/dev/Aria/aria/skills/phase-c-integrator/scripts/pre_merge_gate.py                                        ← 唯一仓内副本
(+ 3 份历史 cache 版本)

$ ls /home/dev/Aria/standards/            # 无 skills/ 目录
autonomous conventions core docs extensions governance legal methodology openspec ...

$ ls /home/dev/Aria/aria-orchestrator/skills/
dispatch-development  heartbeat-scan       # 无 phase-c-integrator

$ cd /home/dev/Aria/standards && git rev-parse --show-toplevel
/home/dev/Aria/standards
$ cd /home/dev/Aria/aria-orchestrator && git rev-parse --show-toplevel
/home/dev/Aria/aria-orchestrator
```

§1 的两分支解析（`<toplevel>/aria/skills/...` 与 `<toplevel>/skills/...`）在 `standards/` 与 `aria-orchestrator/` 两个 cwd 下**都不可达**（`standards/aria/skills/...` 与 `standards/skills/...` 均不存在；`aria-orchestrator` 同理），而 CLAUDE.md 硬约束 1 逐字把 `aria`/`standards`/`aria-orchestrator` 三个子模块并列为「分支合并必须本地 `git merge`」的对象，`SKILL.md:242` 逐字要求 C.2.4 在「子模块合并 → 子模块根」执行 —— 这两个 cwd 不是异常输入，是成文契约钦定的合法执行位置。§1 又逐字规定「helper 不可达 ⇒ abort (exit 2), 不得降级放行」——三个受管子模块里有两个的合并场景会**永久阻死** Rule #8 闸门且无绕行口子（折叠块已去掉全部命令字面量）。第三个场景更硬：plugin marketplace 安装态（`/home/dev/.claude/plugins/marketplaces/10CG-aria-plugin/...`）下 `git rev-parse --show-toplevel` 解析的是**消费方仓**的根，两条分支必然全 miss。

D2「两者都不能作为承重路径来源」的论证只验证了 `ARIA_PLUGIN_ROOT` 在 Aria 仓内未赋值——但该变量按设计就是给仓外场景用的（`aria/CHANGELOG.md:2796`「支持跨项目场景」），「仓内没人设」不能推出「它不可用」，这与 memory `critique-repeats-error`（反驳数字前必须核对总体是否一致）同形。

这与我 QA 镜头第 2 条要查的问题**同源但不同轴**：镜头第 2 条问「调用块放在 SKILL.md 另一节, SC-3 还成立吗」（本报告 MAJ-2），本条问的是「调用块本身在不同 cwd/部署形态下能否启动」——两者独立成立，任一条单独发生即可让本版无法兑现自己的验收标准。

- **收敛**: 本轮 tech-lead（C-1）与 code-reviewer（C1）各自用不同方法独立发现同一问题；本报告是第三条独立复现路径。三席收敛显著提升该发现的置信度。
- introduced_by_r4fix: **true**（R4 版用 `${ARIA_PLUGIN_ROOT:-aria}` + 反斜杠续行；两分支 git-toplevel 解析是本版新写）
- blocks_phase_b: **true**

---

### MAJ-1（testing，本报告独有贡献）· 「测试隔离」段新处方「为 gate 层核验建独立打桩接缝」粒度未定，与 SC-6（禁打桩）/ SC-8（须保留真实重试逻辑）存在未言明的结构冲突

**锚点**: `proposal.md:191-193`（打桩边界 + 测试隔离段）vs SC-6/SC-7/SC-8 `:183-185` vs `test_pre_merge_gate.py:59-80`（`_ProbeCacheResetMixin`）vs `test_path_coverage.py:116-148`（`_RepoFixtureMixin`，既有的"脱离共享 mixin 建真实 fixture"先例）

本版原文：

> **打桩边界**: 只有 SC-6 用真实 `ls-remote` + 受控裸仓; SC-7 / SC-8 必须 mock。
> **测试隔离**: `test_sc22` 的 patch 本就全局生效……`tasks.md` 须含一条前置任务: 为既有调用补 `main_branch="master"` **并**为 gate 层核验建独立打桩接缝, 使 `test_sc22` 保持有效而非被放宽。

问题在于「独立打桩接缝」没有回答两件事，而这两件事互相牵制：

1. **粒度**：如果新桩仿照既有 `evaluate_path_coverage` 的模式加进 `_ProbeCacheResetMixin.setUp()`（即在 `gate._verify_branch_exists`——或其他命名——这一层做**函数级**桩，返回固定"存在"），那么这条桩会对**所有**继承该 mixin 的测试类全局生效。SC-6 明确要求"不打桩，用真实 `ls-remote`"——如果 SC-6 的测试类为了复用既有基础设施（probe cache reset 等）也继承 `_ProbeCacheResetMixin`，它会被这条新的默认桩直接短路，`_verify_branch_exists` 根本走不到真实 `subprocess.run`，SC-6 名不副实。SC-8 需要验证"3 attempts + backoff 5/15/45 + mock `time.sleep`"这条**内部重试逻辑**，如果新桩是函数级（直接桩 `_verify_branch_exists` 的返回值），SC-8 根本没有机会触达这段逻辑；SC-8 要求的桩粒度必须是**更底层**的（桩 `subprocess.run` 的返回值/异常，让 `_verify_branch_exists` 内部的重试计数、退避、exit-code 分派照常跑）——这与"独立打桩接缝"字面上最自然的读法（比照 `evaluate_path_coverage` 的函数级桩）矛盾。
2. **测试类归属**：本仓 `test_path_coverage.py:116` 的 `_RepoFixtureMixin` 是解决这类问题的既有可复用先例——它用 `tempfile.mkdtemp()` + `self.addCleanup(shutil.rmtree, ...)` 建真实临时仓，**不继承**任何"只桩不真跑"的 mixin，与需要真实 git 行为的测试类结构性分离。但它建的是**非裸**仓（`_git(root, "init", "-q", "-b", "master")`，见 `:127`），并非 SC-6 需要的"受控裸仓, 远端只有 `refs/heads/wip/master`"——即便采用同一**模式**（独立、不继承共享 mixin 的测试类），SC-6 仍需要一个新建的、专属的裸仓 fixture，Spec 对此只字未提；`tasks.md` 这个"前置任务"目前唯一的具体产出要求是"补 `main_branch="master"`"，"独立打桩接缝"这半句没有可执行的验收标准。

**后果推演**：如果 Phase B 实现者选择"函数级桩进共享 mixin"（对既有 24 处/新增用例最省事的路径），会在**首次运行 SC-8** 时发现桩把要验的重试逻辑短路了，被迫回头重新设计——这正是本 Spec 自己在四轮历史里反复出现的"处方在自己新写的路径上重犯要治的病"形状（本 change 治的是"两份实现、AI 走了没被加固的那份"，如果 SC-8 的桩把内部重试逻辑短路，效果上是"SC-8 测的不是真实实现，是一份桩出来的影子实现"，同构）。

- introduced_by_r4fix: **false**（这条张力的成因——patch 全局共享——是 R4 轮（QC4/C-4）已发现的既有问题；本版的「独立打桩接缝」是对它的**部分**响应，纠正了"expand patch to pre_merge_gate 模块"这个已被证伪的旧处方，但没有把 R4 报告里已经给出的具体解法（分离测试类 + 底层桩）落进本版文本，残留的是**同一问题的未闭合部分**，非本版新造）
- blocks_phase_b: **false**（有既有模式`_RepoFixtureMixin`可参照，Phase B 可在 tasks.md 阶段自行设计解决，不需要回退 Spec，但若不在 tasks.md 显式钉死粒度与类归属，大概率重蹈"改一次错一次"）

---

### MAJ-2（testing）· SC-3（自称"D1 承重断言"，期望计数=1）与 §1/D1「两处都要改成强制 helper 调用」的具体落点矛盾

**锚点**: `proposal.md:180`（SC-3）vs `:42-44`（§1）· `:68`（§2）· `:158`（D1）· `§Impact:226`

D1 逐字「**两处**散文一起收敛为强制 helper 调用」「只改一处等于没改」；§Impact 逐字「**两处**散文流程重整 (`### 步骤执行` :99 段 + `### C.2.4` :218 段)」。SC-3 逐字要求 `grep -c 'python3 "$GATE" --pr-branch' == 1`。若两处都字面插入同一个调用块 ⇒ 计数 2 ⇒ SC-3 转红（即便实现完全忠实于 D1 的"两处都要改成 helper 调用"这句话）；若只插入一处以保 SC-3 = 1 ⇒ `### 步骤执行`（`:99` 段，AI 按文件线性阅读顺序会先读到的一节，且本 Spec §Why 明确点名它是"AI 走的是没被加固的那份散文"里的一份）就只剩折叠说明、没有可执行入口，D1"两处都要改成 helper 调用"字面不成立。全文没有一句规定`:99`段在不放字面调用块的情况下应该放什么替代内容（指针？纯折叠？删除该 bullet？）。

这是"承重断言的落点没有钉到字符级 ⇒ 两个独立实现者会给出相反但都能自圆其说的结果"的判据命中（同 memory `spec-underdetermination`），且历史上 SC-3 这一条断言本身已经在 R2/R3/R4 三轮里换过三种失败形态（反斜杠续行恒红 → 转义问题恒红 → 现在的落点歧义）——同一断言连续多轮不稳定，本身就是需要更谨慎对待的信号。

- **收敛**: 本轮 tech-lead（M-2）与 code-reviewer（M1）各自独立发现同一矛盾。
- introduced_by_r4fix: **true**（本版把 SC-3 改成单行块 + 期望值钉死为 1，是本版新写的具体形态）
- blocks_phase_b: **true**（这是 Phase B 第一步就会撞上的选择，且现在没有依据能替它做选择）

---

### MAJ-3（testing）· SC-10 只覆盖三条早退中的一条（`enabled=false`），§非目标声称的"由 SC-10 机械钉住"对另两条（no-backend / precheck 失败）不成立

**锚点**: `proposal.md:187`（SC-10）vs §6 `:119-121`（三个早退行锚）vs §非目标 `:217`

§非目标逐字：「不动 `no_ci_fallback` / stub backend 既有降级语义 —— 由 **SC-10** 机械钉住」。SC-10 逐字：「负控: `enabled=false` 早退 | 六键不变、无 `gate_error`, 且 `assert ls-remote 未被调用`」。

§6 自己列出的"三个早退"是 `:328 enabled=false` / `:338 no backend` / `:345 precheck 失败`——三条互相独立的分支。SC-10 只对第一条建立了"核验未被调用"这条因果断言。一个把存在性核验插在 `:328` 与 `:338` 之间（而非 §6 要求的三早退**之后**）的实现：`enabled=false` 路径不受影响（SC-10 依旧全绿，因为它在核验之前就已 return），但`ci_backends: []`（no-backend 显式禁用）与 stub backend precheck 失败这两条路径，会被新核验错误地转成 `fail`——本仓 `.aria/config.json` 的 `no_ci_fallback` 是 live 配置，不是假设场景。SC-1..SC-12 全绿的情况下，这个回归不会被任何一条 SC 捕捉到。

这是"立了判据（§非目标的机械性承诺）又用一条覆盖面更窄的 SC 去兑现它"的形状，本 Spec 历史上已出现多次（§Rule #6 定档三次摆动、SC-2 与 §6 示例的对撞等）。

- **收敛**: 本轮 tech-lead（M-1）与 code-reviewer（M2）各自独立发现同一缺口。
- introduced_by_r4fix: **true**（"由 SC-10 机械钉住"这句机械性声明是本版新加）
- blocks_phase_b: **false**（不阻塞 Phase B 起步，但会让一个真实回归穿过全部 12 条 SC）

---

### MIN-1（testing）· SC-1/SC-2 未覆盖不含 "main" 子串的可执行命令字面量（`SKILL.md:240`），"去掉全部可执行命令字面量" 的「全部」无机械兜底

**锚点**: `proposal.md §2 :68-73`（"折叠块不是保护机制……真正的保护是去掉命令字面量 (SC-2 钉住)"）vs `SKILL.md:240`

```
240  1. Aether binary pre-flight check: `aether --help | grep -q "in-flight"` 验证 binary 含 P0-A flag, ...
```

SC-1 的 pattern 是 `'aether ci status'`（今日计数 4，覆盖 `:167`/`:168`/`:243`/`:244`），SC-2 的 pattern 是 `'"branch": "main"'`（今日计数 1，覆盖 `:270`）。`:240` 这行是一条独立的、可复制执行的命令字面量，两条 pattern 都不命中——若 Phase B 把"5 步"折叠进 `<details>` 时保留了这一行（折叠对 AI 读取无隐藏效果，§2 自己讲得很清楚），它会在全部 SC 绿的情况下原样留在文档里。§2 引用"(SC-2 钉住)"这句表述本身也不准确：SC-2 钉的是 JSON schema 示例里的一处特定字面量，与步骤 1 的这条命令不是同一处。

风险等级放在 Minor 是因为：这条命令本身（`aether --help | grep -q ...`）即便被 AI 复制执行，产出的只是版本探测结果，不直接产生一个可以被误读为"闸门已判定"的假绿输出——不同于本 Spec 要根治的 `aether ci status` 那两条。

- **收敛**: 本轮 tech-lead（m-3）独立发现同一缺口；R4 版 qa-engineer 报告（M-3）已提出过，本版未处理，非本版新造。
- introduced_by_r4fix: **false**
- blocks_phase_b: **false**

---

### MIN-2（testing）· D9「在 path coverage 之前」这半条排序声明无任何 SC 钉住

**锚点**: `proposal.md §6 :128`（"在 path coverage 之前: 它更早消费 main_branch, 放它之后等于放行一次未核验的使用"）vs SC-6..SC-9（均无 `evaluate_path_coverage`/`pc_eval` 相关的 `assert_not_called` 或调用顺序断言）

D9 给了两条排序理由（"三早退之后" + "path coverage 之前"）。前者由 SC-10 部分覆盖（见 MAJ-3，覆盖不全但至少有一条）；后者在整张 SC 表里**没有任何一条**断言。若实现把存在性核验插在 `evaluate_path_coverage()` 调用之后，现有测试基础设施（`_ProbeCacheResetMixin` 把 `evaluate_path_coverage` 桩成一个不看参数、固定返回 "covered" 的 stub）不会让任何一条 SC 变红——SC-6 需要的最终输出（`verdict=fail` + `kind=="main-branch-not-found"`）无论核验插在 path coverage 之前还是之后都一样产出，因为桩后的 `evaluate_path_coverage` 根本不关心 `main_branch` 是否真的存在。行为上的实际风险也偏低（`decision=unknown` 是 fail-toward-covered，不会导致误判为绿），核验查的是**远端** ref（`ls-remote`），而 `evaluate_path_coverage` 消费 `main_branch` 走的是**本地** ref 的 `git diff`（`path_coverage.py:436`）——两者本就不是同一个失效面，"放行一次未核验的使用"这个理由的字面严重性比它实际能造成的后果更强。因此定为 Minor 而非 Major。

- **收敛**: 本轮 code-reviewer（Minor #4）独立发现同一缺口，并给出了与我一致的"行为上无害"判断；tech-lead（m-2）从"核验维度≠消费维度"角度给出了互补的语义论证。
- introduced_by_r4fix: **false**（D9 本身承自更早轮次，覆盖缺口是持续存在、未被本版处理的部分）
- blocks_phase_b: **false**

---

## 轮次记录

- R1-R4: 范围经历两次重定，最终收敛为 D1（SKILL.md 散文 → 强制 helper 调用）。本轮（R5, qa-engineer 席位）按指示不复核 R1-R4 旧清单，只审当前 271 行 `proposal.md`。
- R5 本席：1 Critical（路径解析，三席独立收敛）+ 3 Major（含 1 条本席独有贡献：测试隔离粒度 × SC-6/8 冲突）+ 2 Minor。与本轮同批 tech-lead / code-reviewer 的独立报告在"路径解析恒 abort""SC-3 落点矛盾""SC-10 覆盖不全"三点上收敛（各自独立复现、方法不同、结论一致），提升这三项发现的置信度；MAJ-1 是通读另两席报告确认未被覆盖后单独列出的。
- 建议（供编排层判断是否加第 6 轮）：与 tech-lead 的收敛判断一致——本轮三席合计的 Critical 都落在同一个根因（§1 路径解析）上，Major 里至少 2/3（SC-3 落点、SC-10 覆盖）也是三席收敛的同一批问题，说明诊断已经稳定；如果加第 6 轮，范围应收窄到"§1 路径解析怎么改"+"SC-3 承重块具体落哪"+"测试隔离粒度"三件事，其余 Minor 可直接吸收不必再审。

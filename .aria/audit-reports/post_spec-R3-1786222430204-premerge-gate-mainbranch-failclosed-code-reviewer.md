---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-08T21:23:50.624Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R3 — code-reviewer 席位报告

被审对象: `openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md` (186 行, R2 后「大幅减法」版, 未提交, working tree)。
本轮镜头: **砍掉的能不能砍**。未核对 R1/R2 旧清单 (任务书明令), 全部结论从当前文件 + 生产代码 + 实跑重新起。

---

## 审计结论

### Phase 1 — Spec 对现有代码的陈述是否属实 (逐条回源)

| Spec 陈述 | 锚点 | 核验方式 | 结果 |
|---|---|---|---|
| `:21` docstring `[--main-branch main]` | pre_merge_gate.py:21 | 实读 | ✅ 属实 |
| `:300` 签名缺省 `main_branch: str = "main"` | pre_merge_gate.py:300 | 实读 | ✅ 属实 |
| `:427` CLI `default="main"` | pre_merge_gate.py:427 | 实读 | ✅ 属实 |
| `:436` CLI 透传 | pre_merge_gate.py:435-437 | 实读 | ✅ 属实 |
| DEFAULT_CONFIG 9 键, 不含 `main_branch` | pre_merge_gate.py:53-65 | 实读计数 | ✅ 属实 (9 键) |
| `_normalize_config` alias 层无 `main_branch` 映射 (R3 指定复核项 a) | pre_merge_gate.py:69-72 | 实读 `_OLD_TO_NEW` | ✅ 属实 — 只有 `primitive_preference→ci_backends` / `no_aether_fallback→no_ci_fallback`。**config 面「关得干净」成立** |
| `aether.py:117-135` = `query_branch_in_flight`, 仅 aether 自身失败才抛 | ci_backends/aether.py:117-135 | 实读 | ✅ 属实 |
| `path_coverage.py:24` 规则 1 = git diff 失败 → unknown | path_coverage.py:24 | 实读 | ✅ 属实 |
| 后端「分支不存在」与「无 in-flight」合流 (§Why 实测) | — | **我复跑** | ✅ 属实, 且**比 Spec 说的更强** (见下) |
| 测试内 `gate_check(` 24 处 / 显式传 `main_branch` 0 处 | test_pre_merge_gate.py | grep -c + grep -n | ✅ 属实 (24 / 0) |
| `test_sc12_default_true_lock` 在 `:663` 断言 `main_branch="main"` | test_pre_merge_gate.py:663,669 | 实读 | ✅ 属实 (方法 :663, 断言字面在 :669) |
| 111 tests = 46 + 25 + 40 | 三个测试文件 | 计数 `def test_` | ✅ 属实 (46/25/40) |
| 已有 `test_sc9/10/11/12/13/15/21/22` ⇒ 需 `SC-M*` 前缀 | test_pre_merge_gate.py:623-724 | 实读 | ✅ 属实, 该预防正确 |
| AB: `type: workflow_skill_subextension` / 0 prompt / 0 双臂 | ab-suite/phase-c-integrator-pre-merge-gate.json:4 | 实读 + `grep -c prompt` = 0 | ✅ 属实 |
| `benchmark.json` 自证 `type=structural_verification` | ab-results/2026-05-10-.../benchmark.json:6 | 实读 | ✅ 属实 |
| `benchmark.md:173` 引文 | 同上 | 逐字比对 | ✅ 逐字属实 |
| `phase-c-integrator.json` 3 eval 覆盖 C.1/C.2/C.2.5, C.2.4 零命中 | ab-suite/phase-c-integrator.json | json 解析 | ✅ 属实 (commit-generation / merge-conflict-handling / multi-remote-merge-push) |
| 「387 行 → 本文件」 | .aria/audit-reports/post_spec-R2-*-{tech-lead,qa,code-reviewer,backend-architect}.md | grep 387 | ✅ 属实 (四份 R2 报告均记 387 行) |
| #137 body 首段仍逐字保留「两条腿都失败为绿」 | forgejo GET /repos/10CG/aria-plugin/issues/137 | 实拉 | ✅ 属实 |

**我复跑的 §Why 关键实测** (本机 `/usr/local/bin/aether`, repo 10CG/Aria):

```
aether ci status --branch main   --in-flight --json  → RC=0 {"status":"ok",...,"runs":[]}
aether ci status --branch master --in-flight --json  → RC=0 {"status":"ok",...,"runs":[]}
aether ci status --branch zzz-nonexistent-branch-xyz --in-flight --json → RC=0 {"status":"ok",...,"runs":[]}
aether ci status --branch '<main-branch>' --in-flight --json → RC=0 {"status":"ok",...,"runs":[]}
```

⇒ §Why 成立, 且推论更强: **任意字符串**都返回 `runs:[]` RC=0 ⇒ 判 green。最后一行是本报告 C1 的直接证据。

**Phase 1 判定**: 事实陈述面**罕见地干净** —— 我逐条回源的 19 项数字/行号断言 **19/19 属实**。这是本版相对前两轮的实质进步, 应予确认。
但 Phase 1 **不通过**: 有一条属于「自我声称不成立」—— §What Changes:53 的全称句 `无路径静默继续` 被实测推翻 (C1), 且 §非目标:139 的「降级语义结构上不受影响」推理错误 (M1)。按本轮两阶段适配约定, 自我声称不成立即进入问题列表, 不阻断 Phase 2。

### Phase 2 — 按此 Spec 原样实施会产生什么正确性问题

见下。

---

## 优点 (先说做对的)

1. **回源纪律**: 19/19 数字断言属实, 含「24 处调用 / 0 处显式传参」这种必须实跑才敢写的量。
2. **SC 命名空间避撞** (`:98`): 实读证实 `test_sc9..sc22` 已占用, `SC-M*` 前缀是必要的, 且理由 (同名方法静默覆盖) 正确。
3. **「1 与 2 必须同批改」** (`:49`): 只改 CLI 会留函数签名恒绿, 这个判断对。
4. **Rule #6 的三条 AB 事实**全部实地可验, 不是转述。
5. **D6 版本号不预写字面量**: 与并发姊妹 Spec 共享 SOT 时确实有非单调风险, 判断正确。

---

## 问题

### Critical

#### C1. required=True 守的是 SKILL.md 从未指示 AI 走的那条路 —— AI 主执行路径上现在**一个拦截物都没有**

- **锚点**: `aria/skills/phase-c-integrator/SKILL.md:167` / `:243` / `:262`; proposal.md:53; proposal.md §Rule #6 ①(`:124`)
- **追踪 (任务书点名要求)**: 一个执行 C.2.4 的 AI, 读改动后的 SKILL.md, 会实际发出什么命令?
  - `:243` 步骤 3 是**唯一带「无条件执行」标注的处方性指令行**, 改后为 `aether ci status --branch <main-branch> --in-flight --json`;
  - `:262` 只写 `**Helper 实现**: .../pre_merge_gate.py` —— **一个字都没说要怎么调、传什么参数**;
  - 我 grep 了整个 `aria/` (`grep -rn "pre_merge_gate.py "`): **仓内没有任何 SKILL.md / 文档给出过带参数的 helper 调用形式**。唯一存在的带参调用样例在 `aria-plugin-benchmarks/aria-ci-backend-abstraction/README.md:164-165` (归档物, 且它已经传了 `--main-branch master`)。
  - ⇒ AI 的默认路径是**照抄 `:243` 的裸命令**, 不经 argparse、不经 `gate_check` 签名。
- **实测后果**: `aether ci status --branch '<main-branch>' --in-flight --json` → **RC=0, `runs:[]`** (见上方实跑)。占位符原样执行 = 假绿; 替换成任何错值 = 假绿。
- **为什么这是「砍过头」**: 能堵住这条路的两个面 —— 「自动解析真值」(供给) 与「分支存在性核验」(检测) —— 在 `§移出本 Spec 的面` 里**同时**被移出。移出后, 这条路上取值的唯一来源退回到 `:242` 的散文, 而 §Why:29 正是控诉「唯一现有约束是散文不是兜底」。**减法把处方行的字面量拿走了, 却没有把取值来源接上, 于是那行从「确定的错」变成「不确定」——而后端对两者的回答一样是绿。**
- **为什么 proposal.md:53 的自我声称不成立**: 「CLI → argparse 报错; 函数 → TypeError。二者都是硬失败, **无路径静默继续**」是全称句, 但 §Why:29 自己列举的三条路径里「复制粘贴命令」这条既不过 argparse 也不过函数签名。§Rule #6 ①(`:124`) 更是逐字承认「AI 执行 C.2.4 步骤 3 时, 从 `SKILL.md:243` 读取并执行 in-flight 查询命令」—— Spec 自己知道这条路存在, 却在 :53 宣称它已关闭。
- **如何修复** (二选一, 都在本 Spec 现有减法预算内, 零新增失败面):
  - (a) 把 `:243`/`:167` 从裸 `aether` 命令改写成 **helper 调用形式**: `python3 ${ARIA_PLUGIN_ROOT:-aria}/skills/phase-c-integrator/scripts/pre_merge_gate.py --pr-branch <PR_BRANCH> --main-branch <本仓主分支>` —— 让 AI 的默认路径落到 required=True 守着的那条上; 或
  - (b) 若坚持保留裸命令, 则必须在 `:243` 就地写死取值来源 (例: 「`<main-branch>` 取本仓实际主分支, Aria = `master`; 取不到时 abort, 不得填 `main`」), 并把「取错值仍绿」显式登记为本 Spec **已知未关闭**的残留面, 而不是在 :53 声称已关闭。

---

### Major

#### M1. 「不动降级语义」是错的 —— 必填在**绑定期**失败, 早于 `enabled:false` 早退, 破坏 SKILL.md 承诺的 100% 向后兼容; 而机械补参会让这个回归在测试里恒绿

- **锚点**: proposal.md:139 (非目标末条); pre_merge_gate.py:328-335 (`enabled:false` 早退) 与 :337-339 (`ci_backends:[]` → `_no_ci_output`); SKILL.md:284 / :294; test_pre_merge_gate.py:301
- **Spec 的推理**: 「本 Spec 不在 `gate_check` 内新增任何早退前的逻辑, 该语义结构上不受影响」。
- **推理错在哪**: 参数必填的失败点**不在函数体内**, 而在**调用绑定期** —— 它先于函数体里的每一个早退分支。今天 `gate_check(pr_branch="x", config={"enabled": False})` 返回 `verdict=green / "gate skipped"` (:328-335); 改后同一调用直接 `TypeError`。CLI 侧同理: argparse 在 `_load_config_from_file` (:434) **之前**就退出, 所以 `.aria/config.json` 里写着 `enabled: false` 的项目, 忘传参时得到的是 RC=2 而不是「跳过」。
- **为什么重要**: SKILL.md:284 `enabled | true | gate 总开关 (false → 完全跳过 C.2.4,**向后兼容**)` + :294 `enabled: false → 完全跳过 C.2.4 (**与 v1.2.0 行为 100% 一致**)`。闸门被 owner 显式关掉时不存在「假绿要修」, 此时硬失败是**纯回归**, 不适用 §风险:163 的「这是修复不是回归」辩护 —— 该辩护只对 enabled 的情形成立。
- **且它会假绿**: §Impact:157 要求把 24 处调用**机械补** `main_branch="master"`, 其中就包括 :301 那条 `enabled:False` 用例。补完后测试全绿, 这个回归**在测试里完全不可见**。
- **如何修复**: 在 §非目标 或 §风险 明确写出「`enabled:false` / `ci_backends:[]` 的调用方也必须传 `main_branch`」并评估是否可接受; 或给出保住关闭态兼容的写法 (例: CLI 仅在 `enabled` 为真时才要求该参数 —— 但这会引入 Spec 想避免的条件性, 需显式决策而不是默认沉默)。至少要有一条 SC 钉住关闭态的行为。

#### M2. D2 与 D4 互相拆台: 必填把 **100% 调用方**转成「显式传值」类, 而守这一类的核验恰好被 D4 移出; 且 §Why 的判据与 :51 的判据互斥

- **锚点**: proposal.md:31 (判据本体) vs :51 (D2 论据) vs :73 (D4 移出理由); `docs/handoff/2026-08-08-post-planning-four-rounds-and-three-cross-repo-transfers.md:183`
- **判据自相矛盾**: §Why:31 把判据定义为「**这个信号猜错时会不会被发现**」; :51 则改口为「闸门的正确性…只依赖它**不会猜错**」。这是两个不同的判据。按 :31 的判据, 本 Spec 的方案**不通过** —— 改成必填后, 显式传进来的错值依旧不会被发现 (实测: 任意分支名都返回 `runs:[]` RC=0)。Spec 靠中途换判据让自己通过。
- **交叉不一致**: D2 的效果是把「靠缺省」的调用方**全部**转成「显式传值」的调用方; D4 移出的存在性核验, 治的恰恰是「显式传了错值」。**减法后, 唯一剩下的失效模式正好是唯一没人看守的那个。**
- **与已提交记录冲突且未和解**: `docs/handoff/…:183` 逐字记着上一轮的实测结论 —— 「⇒ **修法不能只改缺省值**, 必须加独立存在性核验, 否则显式传错分支名仍恒绿」。本 Spec 做的正是「只改缺省值 + 把核验移出」, 却全文未引用、未推翻、未标注为 owner 授权的知情降级。
- **如何修复**: (1) 判据只留一个, 若采用 :51 的「不会猜错」版, 必须说明为什么 :31 的判据被替换; (2) 在 §移出面 D4 那格补一句知情声明:「本 Spec 交付后, (b) 腿对**显式错值**仍 fail-OPEN, 该残留由 follow-up issue 承接」, 并把 handoff:183 的结论列为被本次 owner 裁定推迟的项。

#### M3. SC-M4 有一个假绿孔: `:427` 的 help 文本 `(default: main)` 改后仍在且变成谎言, 而 SC-M4 的断言形态够不着它

- **锚点**: proposal.md:105 (SC-M4) 与 :45 (改法表第 1 行); pre_merge_gate.py:427
- **事实**: `:427` 整行是
  `parser.add_argument("--main-branch", default="main", help="Main branch to check (default: main)")`
  —— 这一行有**两处** `main`: `default="main"` 与 help 文本里的 `(default: main)`。改法表第 1 行只写「`required=True` (**无 default**)」, `...` 省略了 help; 若照字面实施, `--help` 输出会是「Main branch to check (default: main)」, 而此时**根本没有 default**。
- **SC-M4 抓不到**: 我实跑 `grep -n '"main"' pre_merge_gate.py` → 只有 :300 / :427 两行命中 (`:21` 无引号)。而 help 里的 `(default: main)` 无引号 ⇒ 任何以 `"main"` 形态写的机械断言, 改后**返 0 命中判绿**, 残留文本安然存活。这正是 SC-M4 自称要钉住的「改没改全」。
- **且「机械 grep, 零裁量」不成立**: (a) 覆盖 `:21`+`:300`+`:427` 三处至少需要两个不同模式 (`"main"` 与 `--main-branch main`), Spec 却把它描述成一次 grep 得 3 命中; (b) 断言正文写的是「`"main"` 字面量**作为分支名缺省**」—— 「作为分支名缺省」是语义判断, grep 做不到, 该修饰语一旦进入执行就是裁量。
- **如何修复**: 把 SC-M4 写成**逐字给出的命令 + 期望命中数**, 并显式含 help 文本 (例: 断言 `grep -c -i 'default.*main' pre_merge_gate.py` == 0 且 `grep -c -- '--main-branch main' pre_merge_gate.py` == 0); 同时在改法表第 1 行把 help 文本一并写进「改为」列。

#### M4. Rule #6 落「第三行」的举证不满足 SOT 的触发条件, 且援引的先例条件不匹配

- **锚点**: proposal.md:112-128; SOT `standards/conventions/skill-benchmark-exemption.md §2 表 / §3 第 1 条 / §4`
- **SOT §3 第 1 条**逐字要求写清「为什么现有固定测试集**结构上**测不到它」。Spec 给的三条证据里:
  - 「`phase-c-integrator.json` 3 个 eval 覆盖 C.1/C.2/C.2.5, C.2.4 零命中」= **选题缺口**, 不是结构性不可测 (加一个 eval 即可);
  - 援引 `benchmark.md:173` 的那句, 其**确切条件**是「AB measurement of LLM workflow behavior **under multi-PR concurrent CI** is not feasible in mock environments」—— 讲的是并发 CI 下的 workflow 行为; 而本次要测的行为是「AI 在命令里写哪个分支名」, 一个 prompt 就能测, 不需要 mock 并发 CI。**条件不匹配, 属类推援引**。
  - 更要命的是**自证矛盾**: §Rule #6 ② 自己承诺「新建可证伪定向 fixture, 向 AI 呈现改动后的 SKILL.md C.2.4 段…断言其产出的命令」。**能建出这个 fixture, 恰恰证明这个行为可被 LLM eval 测量** ⇒ 落 SOT §2 第二行 (处方性·运行时指令面, 能测 ⇒ 照跑 AB), 最不济落第四行「拿不准 ⇒ 照跑 (宁跑勿豁)」。
- **Rule #10 相关**: SOT §4 明写「AI **不可以**在决策表之外自创理由」。「现有 eval 恰好没选这一步」不是决策表里的理由。
- **如何修复**: 要么补上真正的结构性论证 (说明为什么给 parent 套件加一个 C.2.4 eval 结构上做不到), 要么按第四行回落照跑 AB (parent 套件 + 新增 C.2.4 eval), 并按 `REMEDIATION-DESIGN-A3.md:276` 的先例处理「parent 套件无 A 臂基线」的声明义务。

#### M5. Rule #6 ② 的 fixture 断言方向 fail-OPEN —— 满足断言仍可假绿

- **锚点**: proposal.md:125 (`断言其产出的命令**不含**字面 `main``)
- **问题**: 这是**否定式**断言。实测 `--branch trunk` / `--branch '<main-branch>'` 都不含字面 `main`, 却都返回 `runs:[]` RC=0 判绿。一个把占位符原样抄出来、或猜了个错分支名的 AI, **通过 fixture, 同时产生假绿**。
- **与 C1 同源但需独立修**: 正确断言应是肯定式 ——「产出的命令中 `--branch` 的取值 == fixture 仓的实际主分支」。而要让 AI 有可能满足它, `:242` 的「(本项目 `master`)」这个取值来源**必须在改写中保留** —— §同步面 (`:62`) 只说该行散文改成「必填, 不传即报错」, 没有要求保留取值来源。若被一并改掉, 该 fixture 在设计上就不可满足。
- **如何修复**: ② 改为肯定式断言 + 在 §同步面 `:62` 那格显式写「保留『本项目 `master`』的取值来源」。

#### M6. §对 #137 的订正打了稻草人, 且与 §移出面 `:76` 自相矛盾 —— 据此在 issue body 打删除线会划掉一句成立的陈述

- **锚点**: proposal.md:33-35 (订正) vs :76 (移出面第 5 行) vs :151 (Impact 外部动作); pre_merge_gate.py:378-386; #137 body (我实拉)
- **#137 body 原文** (实拉): (a) 那条的原话是「变更路径经 `path_coverage` 判 `not_applicable` 时 PR CI 等待步被跳过 —— 设计如此」。这一陈述**与代码一致** (`gate_check:378-386` 确实在 `not_applicable` 时不调 `query_pr_ci` 直接算 verdict)。
- **Spec 的订正对不上**: :35 用「`path_coverage.py:24` 规则 1 是 git diff 失败 → unknown ⇒ **分支名错时** (a) 腿更保守」来判定「只有 (b) 那条成立」。但 #137 的 (a) 从头到尾没有主张「(a) 因分支名错而失效」。**订正反驳的是一个 issue 没提出的主张**。(a) 腿在分支名错时更保守 —— 这句本身对, 我核过 `path_coverage.py:24` + `_evaluate:436-447`; 但它不能推出 #137 的 (a) 不成立。
- **内部矛盾**: :76 自己承认「(a) 腿 `not_applicable` 通路 …… 本 Spec **不改变**它」, 即承认该通路真实存在。:35 却说那条「不成立」。
- **外部后果**: §Impact:151 要在 #137 body 上「加删除线」。按当前订正执行, 会把一句**成立**的缺陷陈述划掉, 使该缺陷在 issue 上被标记为已被推翻。
- **如何修复**: 订正措辞收窄为「#137 把 (a) 的失效**归因于**分支名缺省, 这一归因不成立 —— (a) 的 `not_applicable` 跳过是设计使然且在分支名错时更保守; (a) 作为缺陷面本身仍在, 由 follow-up 承接」, 删除线只打在归因那半句上。

#### M7. SC-M1 / SC-M3 的执行契约与 §SC 前言的「无 subprocess、无网络」冲突, 且该测试文件零 CLI 级先例

- **锚点**: proposal.md:97 (前言) / :102 (SC-M1) / :104 (SC-M3); test_pre_merge_gate.py:10 (文件 docstring) 与 :710 (`test_sc22` 卫生断言); pre_merge_gate.py:424-440
- **事实 1**: `grep -n "gate.main(\|argv" tests/test_pre_merge_gate.py` → **零命中**。该文件 46 个测试**全部**打在 `gate_check` / `compute_verdict` 层, 通过 `mock.patch.object(gate, "resolve_ci_backend", …)` 打桩。`main(argv)` 从未被测过, 也没有既成的打桩接缝。
- **事实 2**: `main()` 会先 `_load_config_from_file(".aria/config.json")` (:434, 读真实文件), 再 `gate_check` → `resolve_ci_backend` → `AetherBackend.probe()` (`shutil.which("aether")`)。**本机 `which aether` = `/usr/local/bin/aether`** ⇒ probe 为真 ⇒ `precheck()` 起真子进程 `aether ci status --help` ⇒ SC-M3 (`--main-branch master` 全程跑通) 会打**真实网络**。
- **事实 3**: 文件 docstring:10 逐字写着「no real aether/gh calls are made」, `test_sc22`(:710) 是同方向的卫生断言 (禁止真实 git 子进程)。SC-M1 的「今日红窗」尤其危险: 改前 argparse 不报错, `main()` 会一路跑到真实查询, 而断言 `SystemExit` 失败 —— 红是红了, 但代价是单测里打了一次生产 CI 查询。
- **另**: SC-M1 写「退出码非 0」不精确 —— argparse 是 `sys.exit(2)` 抛 `SystemExit`, 不是 `main()` 的返回值; 测试必须 `assertRaises(SystemExit)` 并查 `.code`。
- **如何修复**: 在 SC-M1/M3 显式写明打桩接缝 (`mock.patch.object(gate, "resolve_ci_backend", …)` + `--config-file` 指向 tmp 文件), 并把 §前言 :97 的「无 subprocess、无网络」改为「以既有 `resolve_ci_backend` 打桩接缝保证无网络」。

---

### Minor

#### m1. `:76` 「见下方风险」是悬空引用
- **锚点**: proposal.md:76 → §风险 (:161-163)。§风险 通篇只讲「忘记传参从静默放行变硬失败」, **一个字未提** (a) 腿 / `not_applicable`。移出面第 5 行的移出理由因此没有落点。

#### m2. 缺 `rule6_note` 标记与 SOT 路径引用
- **锚点**: proposal.md §Rule #6 处置 (:112-128); SOT `skill-benchmark-exemption.md:55` 「**无论走哪一行**, 都要在 spec/tasks 留 `rule6_note` 引用本规范」。
- 全文无 `rule6_note` 字串, 也未引 SOT 文件路径。姊妹 Spec 均有: `a1-entry-claim-duplicate-work-guard/proposal.md:273` (`**Rule #6 (rule6_note)**`) / `secret-guard-per-segment-evaluation/proposal.md:156` (`## rule6_note`)。后续复议将 grep 不到本 Spec。

#### m3. fixture 落点与既有布局不符, 目录不存在
- **锚点**: proposal.md:125 `ab-suite/fixtures/c24-main-branch-literal.json`。
- 实测 `aria-plugin-benchmarks/ab-suite/fixtures` **不存在**; 既有布局是 `ab-suite/<skill>-fixtures/` (例: `phase-c-integrator-pre-merge-gate-fixtures/`)。建议改 `ab-suite/phase-c-integrator-fixtures/` 或沿用 `phase-c-integrator-pre-merge-gate-fixtures/`。

#### m4. 占位符拼写三套并存, 削弱「这是要替换的」可辨识度
- **锚点**: proposal.md:47 (`--main-branch <name>`) / :59 (`--branch <main-branch>`) vs SKILL.md:168/:244 既有约定 `<PR_BRANCH>`。
- 同一段落里 `<PR_BRANCH>` 与 `<main-branch>` 并列, 大小写与连字符风格都不同。结合 C1 的实测 (占位符原样执行返绿), 建议统一为 `<MAIN_BRANCH>`。

#### m5. SC-M3「行为与现状逐字一致」不可执行
- **锚点**: proposal.md:104。改后代码里不再存在「现状」那条路径, 单次跑内无可比对象, 也没有 golden 存档。它实际只能退化成「传 master 时输出符合预期」的正向断言。建议改写为具体期望值断言, 或明确要求先归档一份 pre-change 输出作 golden。

#### m6. §非目标 `:134` 的「仍」与现状不符
- **锚点**: proposal.md:134 「`main_branch` **仍**由调用方显式传入」。今天恰恰**不是**由调用方显式传入 (24/24 调用点都不传, 靠缺省) —— 这正是本 Spec 要治的病。措辞把「改后应然」写成了「现状既然」。

---

## 建议

1. **C1 是本轮唯一阻塞项, 且修法在预算内**: 把 `:243`/`:167` 改写成 helper 调用形式, 就同时关掉了 AI 主路径, 并让 required=True 从「守着无人走的路」变成「守着唯一的路」。这不引入 subprocess / 解析 / 新枚举, 完全符合 D2 的「零新增失败面」自我约束。
2. **减法本身没砍错方向, 砍错的是接缝**: 移出解析与核验是合理的; 问题在于移出后没有回头检查「原本靠它们兜底的那条路现在靠什么」。建议在 §移出本 Spec 的面 每格加一列「移出后该面的残留风险由什么承接」, 三格里有两格的诚实答案会是「无, 记入 follow-up」—— 写出来就不会再被 :53 那样的全称句掩盖。
3. **判据只留一个** (M2): 判据在同一文件里换了一次, 而 D4 的移出正当性依赖于换后的那个。这类换判据在后续轮次极难被发现。
4. **两条 grep SC 都需要逐字给出命令与期望命中数** (M3): 「机械」的定义是「不同的人跑得到同一个数」, 不是「听起来像 grep」。

---

## Verdict

**FAIL** (1 Critical + 7 Major + 6 Minor)

- Critical ⇒ 按评分规则 `verdict: FAIL`, `VOTE: REVISE`。
- 说明: 本版**事实面质量显著高于**被审前提所暗示的水平 (19/19 数字断言属实)。阻塞不是因为它写错了事实, 而是因为**减法之后, 承重面落在了 AI 实际不走的那条路上** —— 这恰好是本轮被指定要找的那类缺陷。
- C1 的修复面很小 (SKILL.md 两行改写形式), 修完后本 Spec 的核心主张即成立。

---

## 轮次记录

| 轮 | 席位 | vote | 本席 C/M/m | 说明 |
|---|---|---|---|---|
| R1 | 5 | 5/5 REVISE | — | 本席未参与本轮口径 (任务书明令不核对旧清单) |
| R2 | 5 | 5/5 REVISE | — | 同上 |
| **R3** | 本席 (code-reviewer) | **REVISE** | **1 / 7 / 6** | 被审版本 186 行 (working tree, 未提交)。全部结论从当前文件 + 生产代码 + 实跑重起 |

**本轮 finding 的来源分布** (供编排层判断「fix 引入占比」):

| finding | 由本次减法新引入 | 属「砍过头/砍不干净」类 |
|---|---|---|
| C1 | 是 (占位符形态 + 两个兜底面同批移出) | 是 |
| M1 | 是 (必填是本版新决策) | 否 |
| M2 | 是 (D2/D4 的组合是本版新造) | 是 |
| M3 | 是 (SC-M4 是本版新写) | 否 |
| M4 | 是 (§Rule #6 归类是本版新写) | 否 |
| M5 | 是 (② fixture 是本版新写) | 是 |
| M6 | 是 (§订正是本版新写) | 是 |
| M7 | 是 (SC-M1/M3 是本版新写) | 否 |
| m1 | 是 | 是 |
| m2 | 是 | 否 |
| m3 | 是 | 否 |
| m4 | 是 | 是 |
| m5 | 是 | 否 |
| m6 | 是 | 否 |

⇒ 「本轮 fix 引入的 major 占比」= 7/7 (100%)。但**性质与 R2 不同**: R2 的 100% 出现在「新增设计面自带缺陷」上, 本轮的 100% 是**因为整份文件是新写的**, 分母里没有旧条款可继承 —— 该比值在结构性重写后不具可比性 (与 R2 汇总自己记的「四元组比较在结构性重写后不可比」同理)。**建议编排层不要据此比值直接判「不收敛」**, 而以「C1 是否为单点、修法是否在预算内」为准: 本席认为是, 且是。

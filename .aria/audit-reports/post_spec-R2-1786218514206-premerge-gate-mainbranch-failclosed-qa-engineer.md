---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-08T20:17:38.034Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R2 — qa-engineer 审计报告

## 审计范围与方法

逐条审 §Success Criteria (SC-1..SC-12, proposal.md:249-269) 与 §Impact 测试小节 (:322-357)。实读:

- `openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md` (387 行, 全文)
- `aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py` (748 行, 全文)
- `aria/skills/phase-c-integrator/scripts/pre_merge_gate.py` (445 行, 全文)
- `aria/skills/phase-c-integrator/scripts/path_coverage.py` (509 行, 全文)
- `aria/skills/phase-c-integrator/scripts/ci_backends/{base,aether}.py` (相关片段)
- `aria/skills/phase-c-integrator/SKILL.md` (§C.2.4 全段)
- `aria/skills/workflow-runner/scripts/gate_state_helper.py` (248 行, 全文)
- `aria/.forgejo/workflows/issue-triage-tests.yml` (仅有的 aria 仓 CI workflow)

跑了的命令 (只读, 未改任何文件):

```
python3 -m pytest aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py \
  aria/skills/phase-c-integrator/tests/test_ci_backends.py \
  aria/skills/phase-c-integrator/tests/test_path_coverage.py -q
→ 111 passed in 1.61s   (与 proposal.md:356 "111 tests" 逐字吻合: 46+25+40)

grep -c "gate_check(" test_pre_merge_gate.py → 24   (与 proposal.md:338 "24 处" 吻合)
grep -c "main_branch=" test_pre_merge_gate.py → 1 (仅 test_sc12 的 assert_called_once_with,
  非 gate_check( 调用点) → 与 "显式传 main_branch 的 0 处" 吻合

cd aria && git symbolic-ref refs/remotes/origin/HEAD → refs/remotes/origin/master (RC=0)
git diff --name-only --no-renames main...HEAD → RC=128 (fatal: ambiguous argument)
git diff --name-only --no-renames master...HEAD → RC=0, 7 files

python3 -c "import sys; sys.path.insert(0,'aria/skills/phase-c-integrator/scripts'); import gate_state_helper"
→ ImportError: No module named 'gate_state_helper'

python3 -c "json.load(open('aria-plugin-benchmarks/ab-suite/phase-c-integrator-pre-merge-gate.json'))"
→ version 1.1.0, 7 fixtures   (与 proposal.md:279 逐字吻合)

grep -n "def run_gate" aria/skills/ -r → state-scanner/scripts/phase1_gate.py:1031 (非本 skill,
  与 proposal.md:256 的 m1 订正吻合)
```

**先说结论性事实核验**: proposal §Impact 里给出的全部数字性断言 (24 处 gate_check 调用 / 0 处显式传 main_branch / 111 = 46+25+40 / test_sc12 断言字面量 / AB 套件 v1.1.0 7 fixtures / `run_gate` 真实归属) **逐条核实准确**，无一处数字造假或引用漂移。R1 指出的「既有用例逐字不改」证伪 (C3) 在本版已被诚实吸收且验证准确。

以下是本轮新发现，全部落在 R1-fix **新写内容** (SC 表 + §Rule #6 + §Impact 测试小节) 内，符合 proposal 自己在结尾 (:387) 提出的怀疑方向。

---

## 逐条 SC 审查

| SC | 可测性判定 | 备注 |
|----|-----------|------|
| SC-1 | ⚠️ 见 Finding 3 | 断言依赖 ambient git ref 状态，未钉打桩策略 |
| SC-2 | ✅ 有效 | 函数签名路径，直调 `gate_check`，m1 订正已验证 (`run_gate` 确实不在本 skill) |
| SC-3 | ✅ 有效负控 | 已标注「必须打桩」，判别力真实存在 (新增 `_verify_branch_exists` 调用) |
| SC-4 | ✅ 有效，承重 | 与 §Why 实测 (`InFlightStatus(runs=[])` ⇒ green) 逻辑自洽 |
| SC-5 | ✅ 有效 (但"怎么会红"措辞类型见 Finding 5) | 今日代码没有解析步骤，`main_branch_resolved`/`gate_error` 字段今天必然不存在 ⇒ 断言必红 |
| SC-5b | ✅ 有效 (同上) | 防"只做快路径"退化，见 §Why m6 段落，逻辑自洽 |
| SC-6 | ✅ 有效 (同上) | mock time.sleep 要求明确 |
| SC-7 | ✅ 有效负控 | 同 SC-3 |
| SC-8 | ⚠️ 见 Finding 2 | 三态封闭子句可测；`gate_state_helper` 子句不可达且零信息量 |
| SC-9 | ✅ 有效 (今天连参数都不存在，TypeError 即视为红) | — |
| SC-10 | ⚠️ 见 Finding 3 | "git diff master...pr 成功" 措辞与既有 mock 惯例冲突未消歧 |
| SC-11 | ❌ 见 Finding 4 | 断言对象无 Python 可观测面 |
| SC-12 | ✅ 有效 (但"怎么会红"措辞类型见 Finding 5) | 实为负控 (防解析点错放早退分支前)，未标注为负控 |

---

## Findings

### Finding 1 (Major) — SC 编号与既有 `test_sc*` 方法名命名空间冲突，未被本版识别

`test_pre_merge_gate.py` 内已有四个方法，全部属于 **#122 Spec** (`phase-c-gate-path-coverage-not-applicable`) 自己的 SC 编号体系:

```
test_pre_merge_gate.py:623   def test_sc9_not_applicable_with_inflight_waits_and_skips_pr_query
test_pre_merge_gate.py:634   def test_sc10_not_applicable_clean_green_with_message
test_pre_merge_gate.py:647   def test_sc11_covered_existing_fields_identical_to_disabled
test_pre_merge_gate.py:663   def test_sc12_default_true_lock
```

本 Spec (`premerge-gate-mainbranch-failclosed`) §Success Criteria (proposal.md:264-267) 全新引入 **SC-9 / SC-10 / SC-11 / SC-12**，编号与上述四个既有方法**完全重叠但语义完全不同** (existence-check remote 一致性 / (a) 腿激活 / AI surface 义务 / 早退六键)。

- 不会造成 Python 方法名字面冲突 (完整方法名含不同描述性后缀)，但会造成严重可读性/可维护性风险: 审计过程中我本人在第一遍读到 `test_sc12_default_true_lock` 时，需要专门交叉核对才能确认它属于旧 Spec 而非本 Spec 的 SC-12 (最终靠 :668-670 断言字面量 `main_branch="main"` 才确认)。
- proposal 全文 387 行未提及此命名冲突，§Impact 的「既有测试必然要动」小节 (:336-345) 精确引用了 `test_sc12` 会因本修复而红，却完全没有提示 Phase B「这个 `test_sc12` 和你即将新写的 SC-12 测试是两码事，请勿混淆或误改」。
- 本 Spec 自己在 §同形状兄弟位置 (:309-318) 反复强调「修类不修实例」「不得照抄」的方法论纪律，但没有把同一纪律用到自己的 SC 编号选择上——本可以在起草阶段 `grep test_sc` 一次就能看到既有编号已用到 test_sc28 (`test_path_coverage.py`)，从 SC-13 起接续编号即可避免全部冲突。

**建议**: Phase B 命名新增测试方法时，用能区分 Spec 归属的前缀 (如 `test_mbfc_sc1_...`，mbfc = mainbranch-failclosed)，或至少在类 docstring 里显式注明「本类 SC-9..12 特指 premerge-gate-mainbranch-failclosed proposal，非 #122」。

### Finding 2 (Major) — SC-8 的 `gate_state_helper` 子句既不可达也无判别力，且与本 Spec 自己的非目标矛盾

SC-8 (proposal.md:263) 期望列包含: *"`gate_state_helper.write_gate_state()` 接受该 verdict 不产生未知 status"*。三点实测证明此子句站不住:

**(a) Import 路径今天不通**。`test_pre_merge_gate.py:24` 只把 `phase-c-integrator/scripts` 插入 `sys.path`:
```python
sys.path.insert(0, os.path.join(os.path.dirname(_HERE), "scripts"))
```
`gate_state_helper.py` 实际位于 `aria/skills/workflow-runner/scripts/gate_state_helper.py` — 不同 skill 目录。实测:
```
python3 -c "import sys; sys.path.insert(0,'aria/skills/phase-c-integrator/scripts'); import gate_state_helper"
→ ImportError: No module named 'gate_state_helper'
```
`workflow-runner/tests/test_gate_state_helper.py:17` 有自己独立的 `sys.path.insert`，两个测试目录彼此不连通。proposal §Impact 变更文件表 (:324-334) 未列出任何让 `test_pre_merge_gate.py` 能够导入 `gate_state_helper` 的改动 (新增 sys.path / conftest.py / 挪测试文件)。

**(b) 即便解决了 import，`write_gate_state()` 本体对 `verdict` 零校验**。`gate_state_helper.py:115-155` 的函数体把 `verdict` 原样塞进 `"status": verdict`（:147），全程无 `assert`/`raise`/枚举校验。传入 `"fail"` 或传入历史上被 D-H 明确否决的 `"error"`，函数**同样"接受"**——不抛异常、不记录、无任何可观测差异。"接受该 verdict 不产生未知 status" 这个断言因此**无论 Phase B 实现对错都会通过**，属于审计任务书 §2 点名的「断言的对象在代码里是否存在可观测面」反例：这里没有可观测面。

**(c) 与本 Spec 自己的非目标自相矛盾**。proposal §8 (:226) 自陈: *"`gate_state_helper.write_gate_state()` 的具名参数与 `workflow-state-schema.md:38-54` 的持久化字段集均无该字段位置...**本 Spec 范围内不改 workflow-runner**"*。既然明确声明不碰 workflow-runner，SC-8 又要求对 `workflow-runner` 内的 `gate_state_helper` 做机械验证，这本身就是自相矛盾的范围声明。

C1 (verdict 第四枚举值 → 消费侧 fail-OPEN 复发) 是 R1 五个 Critical 之一；SC-8 前半句「`verdict ∈ {green,wait,fail}`」对 `pre_merge_gate.py` 自身输出仍然可测、有判别力，**核心保护并未落空**，故本 finding 定为 Major 而非 Critical——但 `gate_state_helper` 子句应从 SC-8 删除，或改写成可行的形式 (例如显式在 §Impact 加一条 workflow-runner 侧 follow-up 而非塞进本 skill 的单测)。

### Finding 3 (Major) — SC-1/SC-2/SC-5b/SC-10 缺打桩策略指引，SC-1 若走真实路径存在环境脆弱性风险

proposal 对 SC-3 (:257 "必须打桩 (M10)")、SC-6 (:261 "测试须 mock time.sleep")、SC-7 (:262 "同 SC-3 须打桩") 三条都**明文**要求打桩底层 git 调用。但 SC-1 / SC-2 / SC-5b / SC-10 / SC-11 (同样会触碰 `_resolve_main_branch`/`_verify_branch_exists`/`evaluate_path_coverage` 真实调用链) **只字未提**打桩与否，留给 Phase B 自行判断——这与本 Spec §What Changes 开篇给自己定的判据「两个独立实现者读本节应得同一结果」(proposal.md:92) 不一致。

具体到 SC-1 (proposal.md:255): 期望 `main_branch_resolved == {"name":"master","source":"symbolic-ref"}`，隐含要求执行环境的 `refs/remotes/origin/HEAD` 是设置好的 symbolic ref。若 Phase B 选择"真实端到端不打桩"这一读法 (SC 自身描述"仓内 `refs/remotes/origin/HEAD` → `master`" 明显是在描述真实仓库状态，而非 mock 返回值)，则该断言的对错取决于**执行该测试的容器/CI 的 git checkout 方式**，而非取决于修复代码本身对不对:

- 实测**本仓/aria 子模块今天确实如此** (`git symbolic-ref refs/remotes/origin/HEAD` → `refs/remotes/origin/master`, RC=0)。
- 但 `aria` 仓自己唯一现存的 CI workflow (`aria/.forgejo/workflows/issue-triage-tests.yml:32-35`) 用 `actions/checkout@v4` + `fetch-depth: 1` —— 这是浅克隆单分支检出的典型配置，此类检出**通常不会**建立 `refs/remotes/origin/HEAD` 这个 symbolic ref (GitHub/Forgejo Actions checkout 的已知行为: 只 fetch 目标 SHA/ref，不做完整 `git clone` 或 `git remote set-head`)。
- 本 Spec 自己在 D-C/m6 段落 (proposal.md:125) 精确点名了这个风险场景: *"Layer 2 容器里脚本化 checkout 的仓可能根本没有这个 ref"*，并因此在**生产代码**里设计了"快路径失败则退到 `ls-remote --symref` 权威路径"的双层解析——但没有把同一份怀疑用回 SC-1 **自己的测试断言**: SC-1 硬编码要求 `source=="symbolic-ref"` (快路径值)，一旦这批测试将来接入任何浅克隆环境 (含 `phase-c-integrator` 目前还没有但未来可能补齐的 CI workflow，或 Layer 2 aria-runner 容器自身跑 `pytest` 做验证)，**同一个正确实现**会因为落到 `ls-remote-symref` 分支而让 SC-1 失败——即"实现是对的，断言却环境相关地为假"，这正是本 Spec 花一整段篇幅 (m6) 去防止在**生产逻辑**里出现的同一类脆弱性，原样复发在了**测试断言**里。
- SC-10 (proposal.md:265) "解析出 `master` 后 `git diff master...pr` 成功" 的措辞同样暗示真实 subprocess 执行，但全文件既有先例 (`_ProbeCacheResetMixin.setUp()`, :67-76) 对 `evaluate_path_coverage` 做的是**类级自动全局打桩**——`PathCoverageGateTests` 类下已有的 `test_sc9`/`test_sc10`/`test_sc11` (旧 Spec) 全部通过覆写 `self.pc_eval.return_value` 来模拟不同 decision，从未真实调用 git。SC-10 若不打桩就与这一贯穿全文件的惯例背离，若打桩则 proposal 的"git diff...成功"措辞具有误导性 (真正验证的是"`main_branch` 参数被正确传成 `master`"，类似既有 `test_sc12_default_true_lock:668-670` 的 `assert_called_once_with` 模式，而非真实 git 行为)。

两种读法 (真实 vs 打桩) 目前都能自圆其说，但 proposal 没有替 Phase B 做出选择，且"真实"这一读法在当前项目唯一可查的 CI 先例下有实测支持的脆弱性证据。

**建议**: 在 SC-1/SC-2/SC-5b/SC-10/SC-11 各自的"怎么会红"列补一句打桩策略 (仿照 SC-3/SC-6/SC-7 的写法)；若坚持 SC-1 要用真实 git 状态断言 `source` 字段，至少改为对 `source in {"symbolic-ref","ls-remote-symref"}` 做宽断言，而不是死抠某一条路径。

### Finding 4 (Major) — SC-11 断言对象在代码里无可观测面，唯一可行代理与既有测试冗余

SC-11 (proposal.md:266) 期望列: *"AI surface 义务照常触发 (`SKILL.md:252` (a) 项警告行)"*。这是要求"下游编排 AI 在自己的 workflow report 里手写一行警告文案"——是**给 AI 读的 prose 义务**，不是 `pre_merge_gate.py` 这个 Python 函数的返回值契约。`test_pre_merge_gate.py` 里的单元测试只能断言 `gate_check()` 的返回 dict (`verdict`/`raw_message`/`path_coverage` 等字段)，无法机械验证"AI 是否真的把警告行写进了它自己的报告"。

proposal 自己在 §Rule #6 (:287) 已经正确识别了同一类问题: *"两套件均覆盖不到 C.2.4 的 D9 surface 措辞...本 Spec 新增的 `gate_error` / `main_branch_resolved` surface 同样落在该缺口内"*——但没有把同样的判断用回 SC-11 本身: 既然 AB benchmark 测不到这类"AI 措辞义务"，写在 `test_pre_merge_gate.py` 里的 pytest 单测同样测不到，性质相同。

若 Phase B 把 SC-11 折算成检查 `raw_message`/`path_coverage` 字段内容 (唯一可行的机械代理)，这与已经存在且已经绿的 `test_compute_verdict_explicit_not_applicable_branch` (test_pre_merge_gate.py:726-745) **逻辑重叠**：该测试今天就直接单元测试 `compute_verdict()` 在 `pr_ci_status="not_applicable"` 时的 `raw_message`/`path_coverage` 行为 (来自 #122 Spec，与 `main_branch` 解析是否正确完全无关，且**完全不依赖本 Spec 的任何改动**)。SC-11 若照此实现，等同"新起一个名字重新断言已经验证过的旧逻辑"，对本 Spec 真正要修的 bug (main_branch 解析激活 not_applicable 通路) 没有增量判别力——真正有判别力的部分其实是 SC-10 (验证 `main_branch` 参数被正确解析并传给 `evaluate_path_coverage`)，SC-11"承 SC-10"这句话恰恰说明二者在设计意图上就是同一件事的两个角度，但 SC-11 独立列出的那个角度 (AI surface 义务) 没有可测代理。

按 CLAUDE.md Rule #6 判据表的分类原则 ("处方性·套件覆盖外 (典型: authoring 向导) → 不能 [AB 测得到] → 点名行为 + 建可证伪定向 fixture + 套件缺口开 issue")，这类内容的正确处置是点名 + 开 issue，而不是包装成一条表面上可机械验证的单测 SC 混入表格造成"必红/必绿"的错觉。

**建议**: 将 SC-11 降级为 §Impact 里的一条"已知不可测 AI 义务，人工 checklist 项"，或者把它并入 SC-10 (SC-10 本身已经覆盖 `path_coverage.decision=="not_applicable"` 且 `assert_not_called`，这才是真正有红窗的部分)。

### Finding 5 (Minor) — 多条 SC 的"怎么会红"实为负控式判别力而非真正 baseline-failing，未被标注

严格按"在**当前未改**代码上跑这个测试是否失败"的标准逐条核验，SC-5 / SC-5b / SC-6 / SC-9 / SC-12 的"怎么会红"列描述的实际上都是"某个可信但错误的 Phase B 实现会在此翻车"，而非"当前代码跑这个测试必然失败"。以 SC-12 (proposal.md:267, 三早退分支保六键) 为例: **今天** `pre_merge_gate.py` 的三个早退分支 (`enabled:false`/no-backend/precheck 失败) 产出的就是恰好六键、不含 `main_branch_resolved`/`gate_error` (这两个键在今天的代码里根本不存在) —— 用这套断言去跑**今天**的代码，结果是**绿**，不是红；只有当 Phase B 把解析点错放到三个早退分支**之前**时才会转红。SC-3/SC-7 明确标注了「负控」二字，但同样性质的 SC-5/SC-5b/SC-6/SC-9/SC-12 没有被同样归类。

不影响正确性，但影响 Phase B 执行 TDD RED-GREEN 步骤时的预期管理：如果不清楚哪些 SC 本来就该在功能代码到位前保持绿 (因为它们防的是"错误实现"而非"未实现")，容易在写测试阶段误以为看到绿是"测试写错了"而浪费排查时间。

**建议**: 在这几条的"怎么会红"列前加"(负控)"标注，与 SC-3/SC-7 保持一致的表述纪律。

---

## 审计结论

本轮 R1-fix 是一次高质量的结构性重写: 全部可核验的量化声明 (24 处调用点 / 0 处显式传参 / 111 = 46+25+40 测试基线 / AB 套件 v1.1.0 7 fixtures / `run_gate` 真实归属) **逐条实测通过**，§Why 的核心技术前提 (`AetherBackend.query_branch_in_flight` 把"分支不存在"与"无 in-flight run"合流、`path_coverage.py` 规则 1 的 fail-toward-covered 语义) 也逐字对得上源码。R1 的 5 个 Critical (C1-C5) 在本版 §What Changes/§决策记录/SC 表里都能找到对应的机制化处置且论证站得住。

但本轮任务书特别提醒的"新写内容复发同形状缺陷"确实命中: 新增的 SC-8/SC-9/SC-10/SC-11 与整段 §Success Criteria 表格暴露出四类问题 (Finding 1-4，均为 Major)——SC 编号与既有测试方法名的命名空间冲突、SC-8 的跨 skill 断言不可达且零信息量、SC-1/SC-10 一族的打桩策略空白外加真实的环境脆弱性证据、SC-11 断言对象无 Python 可观测面且与既有测试冗余。这些都不是"整体方案错了"级别的问题 (R1 的 5 个 Critical 均已有效处置，没有发现新的 Critical)，而是"如果不在 Phase B 前补一句消歧文字，实现者可能在此绊倒或产出低价值/环境脆弱的测试"级别的问题——按 verdict 判据 (0C+≥1M → PASS_WITH_WARNINGS) 落在 PASS_WITH_WARNINGS。

## Verdict

**PASS_WITH_WARNINGS** — 0 Critical + 4 Major + 1 Minor。核心机制 (D-A 至 D-L) 论证扎实、量化声明逐条属实，可以进入 Phase B；但建议在 Phase B 启动前对 SC-1/SC-8/SC-10/SC-11 四条补一句实现指引 (打桩策略 / 删除不可达子句 / 消歧编号)，避免 Phase B 因表述空白而在这几条上产生二义实现或环境脆弱的测试。

## 轮次记录

- **R1** (5 席 tech-lead/backend-architect/qa-engineer/code-reviewer/knowledge-manager): 5/5 REVISE，聚合 FAIL，5C+10M+6m=21，触发结构性重写。
- **R2** (本轮, qa-engineer 单席): 聚焦重写后新表面 (SC-1..12 + §Impact 测试小节)。核验全部量化声明准确；R1 的 5 个 Critical 均已被有效吸收，未发现新 Critical。新发现 4 Major (SC 命名空间冲突 / SC-8 gate_state_helper 子句不可达 / SC-1&SC-10 打桩策略空白+环境脆弱性 / SC-11 无可观测面) + 1 Minor ("怎么会红"负控标注不一致)。个人 verdict: **PASS_WITH_WARNINGS**。是否需要 R3 由编排层依据其余席位的本轮结论综合判定 (本报告仅代表 qa-engineer 单席意见)。

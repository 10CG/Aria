---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-11T00:19:25.000Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R2 — qa-engineer 独立审计

被审对象: R1-fix 后的 `proposal.md` + `tasks.md` + `detailed-tasks.yaml`（换人执笔勘正轮）。
本轮判据: (1) R1 的 3C+12M 是否真闭合; (2) R1-fix 是否引入新缺陷; (3) 有无恒红/恒绿/空真。

**方法**: 主 loop 提供的 `verified-ground-truth.md` + `adjudication-draft.md` 覆盖面很广，我
对其中与我席位（验收可证伪性 / 打桩边界 / 测试基线口径）相关的条目做了**独立复跑**（不是只读结论），
再针对 ground-truth 未覆盖的角度做了新的搜索。凡本报告引用 ground-truth 已验证的数，均标注「复跑确认」。

## 投票

**VOTE: REVISE**（0 Critical / 1 Major / 1 minor — 新发现，均非 ground-truth/adjudication 已提及）

---

## 一、R1 三条 Critical 的闭合情况（逐条回源，非采信声称）

### PC1 — SC 对 `--main-branch` 全套失明（写死 `main` 能 0/0/2 全过）

**判定：闭合。**

复跑确认：
```
$ cd aria/skills/phase-c-integrator
$ grep -nE -- '--main-branch +(main|master)([[:space:]]|$)' SKILL.md
(无输出，0 命中)
```
今日 SKILL.md 尚未改，理应命中 `:167`/`:243` 的 `main` 字面量——但这两处是 `aether ci status --branch main`（宾语是 `<main-branch>` 语义的 `main` 但语法上不是 `--main-branch main` 这个 flag+value 对），所以 SC-M3b 现在测的是**未来** SKILL.md 改造后的负控，当前 0 是"还没构造出会被拒的坏形态"而非空真——这点 proposal 自己也用 SC-M3a/b/c 三元组说清楚了（M3a 正控测占位符存在、M3b 负控测写死值缺席、M3c 负控测调用不在折叠块）。且已见 §Rule#6 一节下方 "SC-M3a/b/c 已做对抗性验证" —— 构造了「写死 main」「藏进折叠块」两个坏 fixture，均被拒（ground-truth §2 已复跑确认 pattern 命中值与 Spec 自陈一致）。TASK-001 也把这两条对抗性验证列为交付物（tasks.md/detailed-tasks.yaml TASK-001 最后一条 bullet）。
⇒ PC1 指控的"断言维度与病灶维度不同"已经用**换维度的新断言**（SC-M3a/b/c，而非仍然停留在 `--pr-branch` 存在性）解决，且该修复本身经过对抗性 fixture 验证，不是自证。

### PC2 — SC 编号与既有测试文件全面冲突

**判定：闭合。**

复跑确认（本席位独立跑，未采信 ground-truth 的等价陈述）：
```
$ grep -rn 'SC-M' aria/skills/phase-c-integrator/tests/
(无命中 —— SC-M 前缀今日在测试文件里零使用)
$ grep -noE 'SC[-_][0-9]+[a-zA-Z]?' tests/test_pre_merge_gate.py | sort -u
SC-9 / SC-11 / SC-22（既有编号）
$ grep -noE 'SC[-_][0-9]+[a-zA-Z]?' tests/test_path_coverage.py | sort -u
SC-1/SC-2/SC-4/SC-14/SC-18/SC-19/SC-23/SC-27（既有编号）
```
`SC-M*` 是一个语法上与既有 `SC-N` 编号不相交的新命名空间（`M` 前缀），今日实测零碰撞。PC2 闭合。

### PC3 — 组 0"先看到红"只覆盖 4/13 条 SC，SC-6~13 无 owning task/deliverable/红窗

**判定：闭合，但有一处遗留的验收力度不对称（见下文 Major-1）。**

现状核对：SC-M6/M13 由 TASK-003 领（deliverable=spike 结论回写 §5，verification 含 SC-M6/SC-M13）；
SC-M7/M8 由 TASK-004 领（deliverable=`aether.py`+`test_ci_backends.py`，verification 含 SC-M7/SC-M8）；
SC-M9/M10/M11 及"零命中用例"由 TASK-008 领（deliverable=`pre_merge_gate.py`+`test_pre_merge_gate.py`）。
13 条 SC 现在**每条都有 owning task + deliverable**，PC3 点名的"无人认领"结构性缺口已补齐。

"红窗"维度：SC-M1/M2/M3*/M4/M5 是既有代码上的 grep 断言，红窗需要显式验证（且 proposal 已实跑给出"今日实测"列，TASK-001 也要求"贴出实施前实跑输出"）；SC-M6~M13 是**尚不存在的新行为**，其"红"是结构性的（函数不存在/调用会 TypeError），不需要像 grep 断言那样单独证明"确实红"——这与 grep 断言的红窗要求不是同一范畴，我认为 PC3 原文的诉求（"owning task/deliverable/红窗"三项）已经在能适用的范畴内被满足。

---

## 二、R1 十二条 Major 抽样复核（六条抽样，均闭合）

我从 12 条里挑了与我席位最相关、且最容易"看似改了其实没改"的六条，逐条源码复跑：

| Major | 复核方式 | 结果 |
|---|---|---|
| `SKILL.md:262/:559/:610` 用 `ARIA_` 非 `CLAUDE_` | `grep -nF '${ARIA_PLUGIN_ROOT:-aria}/skills/' SKILL.md` | **命中 {:262,:559,:610} 精确**，proposal/tasks.md 现在的表述方向已纠正为 `ARIA_`，一致 |
| TASK-004 两个"不得再造"目标不可直接复用 | 直读 `aether.py:37-38`(`RETRY_BACKOFF=(5,15,45)`) 与 `:164-187`(`_run_with_retry`, docstring "other exceptions bubble up", `text=True`) | **逐字确认**；D-4 四条缺口（catch-all/解码/cwd/超时哨兵）均已写入 TASK-004 verification |
| `test_ci_backends.py` 25 tests 全绿是恒绿判据 | `grep -c '_run_with_retry' tests/test_ci_backends.py` → **0**；`grep -c 'def test_'` → **25** | 确认；tasks.md 已把该判据降级为"必要不充分"并要求新建针对 `_run_with_retry` 本身的用例 |
| DAG 缺 3 条语义依赖边 | 读 `detailed-tasks.yaml` TASK-008(deps 含 TASK-007) / TASK-011(deps 含 TASK-003) / TASK-012(deps 含 TASK-009) | **三边均在位** |
| `test_sc22` 守卫接缝 | 直读 `tests/test_pre_merge_gate.py:710-724`，`gate.gate_check(pr_branch="feat/x")` 未传 `main_branch` | 确认 D5 落地后该调用会 TypeError（守卫本身逻辑未变，需要 TASK-005 打桩接缝——已建为独立任务） |
| 24 处 `gate_check(` 调用口径 | `grep -c 'gate_check(' tests/test_pre_merge_gate.py` → **24**；`grep -n 'gate_check(' ... \| grep -c 'main_branch'` → **0** | 与 §4 口径逐字一致 |

六条全部**闭合且可复现**，无一条是"文档改了、代码/事实对不上"的纸面修复。

---

## 三、新发现（ground-truth 与 adjudication 均未提及）

### 🟠 Major-1: D9 插入点因果断言只补了三条早退中的一条，另两条被同一套修法遗漏

**位置**: `openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml:246`
（对应 `tasks.md` TASK-008 同一条 bullet；`proposal.md` §非目标 "由 TASK-008 的两条专用用例钉住" 一句）

**背景**（R1 遗留 Major，proposal 已回写修复）: `SC-M10` 原本只断言"六键不变"，被指出这是**缺后半条因果断言则健康与不健康实现都绿**（D9 插入点这个不变量守不住——因为如果实现者把 `_verify_branch_exists()` 放在三个早退**之前**，只要测试 fixture 用的分支恰好存在，六键仍然不变，看不出插入点错了）。修复方式是给 SC-M10 加上 **`assert ls-remote 未被调用`** 这条因果断言。proposal.md:259 / tasks.md TASK-008 的 SC-M10 bullet（`detailed-tasks.yaml:244`）逐字带着这条：

```
- 'SC-M10 负控: enabled=false 早退保持六键、无 gate_error, **且 assert ls-remote 未被调用**'
```

**问题**: `enabled=false` 只是**三个**早退分支之一（`:328`）。另外两个早退——`backend is None`（`:338`）和 `precheck() 失败`（`:345`）——同样受 D9 约束（核验点必须在这两条**之后**）。proposal 自己也在 §非目标 里承认"这两条不在 SC-M10 覆盖内"，并交给 TASK-008 的"两条专用用例"处理。但我逐字核对了这条 bullet（`detailed-tasks.yaml:246`）:

```
- no-backend (:338) 与 precheck 失败 (:345) 两条早退亦须各有一条用例 — SC-M10 只覆盖
  enabled=false, R5 三席指出 §非目标『由 SC-M10 机械钉住』对另两条不成立 (proposal
  §非目标 已于 2026-08-10 回写该缺口)
```

**只要求"各有一条用例"，没有把刚给 SC-M10 补上的那半句"且 assert ls-remote 未被调用"带过来。** 这正是本项目 memory `fix_the_class_not_the_instance`（"修实例必问这形状还有几个兄弟位置"）点名的那个模式——这次它在同一个 Spec、同一次修复动作里，同一个不变量（D9）、三个结构等价的兄弟分支上，只把因果断言焊在了 1/3 上。

**它在什么实现下会红（更准确地说：不会红，这才是问题）**:
构造实现 X：把 `_verify_branch_exists()` 插在 `cfg = {**DEFAULT_CONFIG, **user_normalized}`（`pre_merge_gate.py:326` 附近，我已读该区段确认结构）之后、**enabled 检查之前**——不对，这个位置会被 SC-M10 现有的因果断言直接抓到（enabled=false 时会去调 ls-remote，assert 失败）。

真正漏网的是插入点 X'：正确跳过 `enabled=false`（`:328`），但插在 `backend is None`（`:338`）**之前**，或正确跳过前两个但插在 `precheck() 失败`（`:345`）**之前**。若 TASK-008 新增的两条"专用用例"只按 bullet 字面构造——backend 不可用时六键不变 / precheck 失败时六键不变——而不显式 mock/patch 断言"验证分支存在性的子进程未被调用"，则：只要这两条用例的 fixture 里 `main_branch` 恰好指向一个真实存在的分支（多数负控 fixture 会图省事复用一个能过的默认分支名），实现 X' 会**静默成功地跑一次 ls-remote，再照常触发 backend-None / precheck-fail 早退，返回的六键与健康实现完全相同**——测试绿，但 D9（"核验点必须在三早退之后"）对这两条分支的约束**从未被验证过**。这与 SC-M10 修复前的失效模式字面相同，只是分支换了两个。

**建议修法**（一句话即可，成本极低）: 把 `detailed-tasks.yaml:246`（及 `tasks.md` 对应行）改为：

> "no-backend (:338) 与 precheck 失败 (:345) 两条早退亦须各有一条用例，**且各自都要带上与 SC-M10 同款的因果断言（assert ls-remote 未被调用）**——理由与 SC-M10 完全相同：缺该断言则该分支下健康与不健康实现（核验点插入位置）都绿。"

**严重度定级理由**: 不定 Critical——因为它只是 D9 这一个不变量在 3 个等价分支中的 2 个上失去了机械保护，SC-M6/M7/M8/M11/M13 等其余正向路径断言仍然完整，且第三个分支（enabled=false，历史上最容易被误插的位置，因为它在函数最前面）已被完整保护。定 Major：属于"Level 3 应钉住但没钉住"的完整性缺口，不阻塞 TG-0~TG-2（TASK-001/002/003/004/005 均不涉及此 bullet），但**必须在 TASK-008 执行前**（TG-1，晚于 TASK-003/004/005/007）补上，否则会在实现阶段产出一个自己看不见的洞。

### 🟡 minor-1: `UnicodeDecodeError` catch-all 分支没有 SC 编号，是本 Spec 里唯一"无编号"的行为要求

**位置**: `detailed-tasks.yaml` TASK-004 verification（`aria/skills/phase-c-integrator/scripts/ci_backends/aether.py:176` 的 `text=True` 引出的缺口 2）

**内容**: TASK-004 的 verification 列表里有一条：
```
- 'catch-all 分支存在: 任何未枚举情形 (FileNotFoundError / OSError / UnicodeDecodeError /
  输出不可解析) 一律 fail, 不得放行'
```
这条**没有对应的 `SC-M*` 编号**。对照本 Spec 其余全部 20 条 verification bullet（SC-M1~SC-M13 逐条挂编号），以及本 Spec 自己的方法论教训——SC-M numbering 存在的**理由本身**就是"未编号的散文要求会被跳过"（proposal:249 SC-M3b 那行明确写着这是"PC1 的修复"，PC1 的病灶正是"断言存在但测错了维度"，而这条则是"要求存在但连断言维度都没定"，是同一类问题更早的一步）。`UnicodeDecodeError` 分支需要专门构造一个会抛该异常的 mock（`subprocess.run` 的 mock 返回值或 side_effect 设成 `UnicodeDecodeError` 实例），这在技术上可行（做法与 SC-M8 mock `TimeoutExpired` 完全同构），但没有编号意味着**没有任何机械勾稽点判断这个 mock 用例是否真的被写出来**——只能靠实施者读散文时不漏看。

**它在什么实现下会红**：不会红——这正是问题所在。若实现者把 `aether.py:176` 的 `text=True` 原样搬进共享 helper（"这是最自然的写法"，proposal/tasks.md 自己在别处这样形容过同一种疏漏），`UnicodeDecodeError` 分支永远不会被任何**编号**断言捕获；因为它没编号，Rule#6 AB 套件、TASK-015 的合规检查、乃至下一轮审计的机械核对都不会去找它，只能指望人工读到这行散文。

**建议**: 给这条补一个 `SC-M14`（或类似编号）并写明 mock 配方（`side_effect=UnicodeDecodeError(...)`），与 SC-M8 同构写法。成本一句话。

---

## 四、恒红 / 恒绿 / 空真 扫描（本轮独立核对）

- **SC-M3c 空真**: proposal/tasks.md 均已**主动标注**"今日的 0 是空真, 不得当正面证据读"，且给出了它何时开始有信息量（TASK-011 建出折叠块后）。这是**已充分披露**的空真，不是隐藏缺陷——按本项目 memory `false_green_dual_is_permanent_red` 的判据（"该信号在健康常态下应是什么值"），SC-M3c 今天不提供信号，文档如实说了，不算新问题。
- **未发现新的恒红/恒绿断言**——本轮抽样复核的六条 R1 Major（§二）与 TASK-014 的封闭白名单验收（`{:610}` 精确命中 + `:262`/`:559` 各恰 1 处 + 五点负控零改动）在设计上都要求"实施前红、实施后绿、且有负控/对抗 fixture"，没有发现"任何实现都会通过"或"任何实现都通不过"的结构。
- **打桩边界自洽性**：proposal.md `:264-267`（"打桩边界"一段）自己指出并修正了上一版的两处自相矛盾（"只有 SC-M6 用真实 ls-remote" vs SC-M13 自身定义矛盾；"SC-M7 必须 mock" vs 允许非 mock 手段矛盾）。复核该段当前文本，两处矛盾确已消除，SC-M6/SC-M13 用真实受控裸仓、SC-M8 必须 mock、SC-M7 两种手段皆可，三档边界现在内部一致。

---

## 五、测试基线口径复核

```
$ cd aria/skills/phase-c-integrator && python3 -m pytest -q
111 passed in 1.10s
```
与 proposal.md「测试基线」段声称的 `46+25+40=111`、"当前全绿" 一致，且晚于 ground-truth 实跑一天（今日 2026-08-11 复跑）仍然 111/111，无漂移。`aria` 子模块 HEAD 实measured `af87caeeed88af6af76f29a8002badbe1228d927`，与 `detailed-tasks.yaml metadata.scope_repos[0].head` 声称的 `af87cae` 一致。

---

## R1 闭合情况总结

3 Critical (PC1/PC2/PC3) 与抽样 6 条 Major **全部闭合**，且闭合方式是可独立复现的源码/命令层证据，非文档自陈。换人执笔在本轮**没有重蹈**"每轮 fix 引入 73-100% 新 Major"的模式——我独立发现的新问题只有 1 Major + 1 minor，且都是**同一类"验收力度不对称/漏编号"的完整性缺口**，不是新的逻辑错误、不是新的恒红/恒绿、不是对 R1 已修复内容的破坏。这与 tasks.md 自己的方法论陈述（"换人执笔"是本 session 验证过的处方）在我这个席位的观测上是**吻合**的。

## 阻塞项

无。Major-1 与 minor-1 均为一句话规模的 tasks.md 文字补丁，可在 TASK-008/TASK-004 各自执行前顺手补上，不构成阻塞 Phase B 启动的理由（TG-0 的 TASK-001~005 均不依赖这两条）。

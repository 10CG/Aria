---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-09T10:09:58.776Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R5 · tech-lead · premerge-gate-mainbranch-failclosed

镜头: 架构与流程 (D1-D11 自洽性 / §非目标 与 §Impact follow-up 边界 / Level 3 与版本地板定档 / Rule #6 / 与 #136·#137·Rule #8 SOT 的关系 / §Impact 的 CLAUDE.md 行)。

**方法**: 只审当前 271 行文件本身, 不核对 R1-R4 旧清单。所有 finding 均实读锚点或实跑受控实验。编排层已过的 23 项机械自检未复跑, 但对其中两项的**设计**下了判断 (见 m-5 / 结论 §2)。

---

## 审计结论

**2 Critical + 6 Major + 5 Minor。** 两条 Critical 都落在 R4-fix 本轮新写/重写的内容上, 与「每轮 Major 的 79-100% 是上一步 fix 新造」的规律一致 —— 且 C-2 是**在吸收 R4 的一条 Major 时, 在同一段里新造了一条同形缺陷**的直接实例。

先记下**核验通过**的部分 (占我实读锚点的多数, 避免把「全是问题」的印象带给读者):

| 已实证正确 | 方式 |
|---|---|
| §1 四行块在两种 cwd 下都可达 | 实跑: `cwd=/home/dev/Aria/aria` → 走第二分支解析出 `/home/dev/Aria/aria/skills/.../pre_merge_gate.py`, `python3 "$GATE" --help` RC=0 (`ci_backends` / `path_coverage` 相对 import 也解析成功) |
| abort 分支真会阻断 | 实跑: `cd /tmp` 跑同一块 → 打印 `C.2.4 ABORT` 并 `exit 2`, 第四行未执行 |
| D6 `refs/heads/` 锚定 | **独立第三次复现**: 受控裸仓只有 `refs/heads/wip/master` 时, `--heads <r> master` RC=**0** (假存在); `--heads <r> refs/heads/master` RC=**2** ✓ |
| §5 表的 0 / 2 / 128 三行 | 实测: 存在=0 · 不存在=2 · remote 名不存在=128 · 坏 URL=128 · **非 git 目录=128** (故「非 git 目录」已被 128 行吸收, 不是缺口) |
| §6 六个行锚点 | 逐行实读 `pre_merge_gate.py` :328 / :338 / :344 / :345 / :356 / :357 / :358 / :366 全部逐字命中, 且 :358 确在 :366 之前 ✓ |
| §4 三处落点 | :427 CLI 缺省 · :300 签名缺省 · :21 docstring 逐字命中 ✓ |
| 外部引用 | `SKILL.md:252-255`/`:259`/`:260`/`:267`/`:279` · `ci_backends/base.py:29` (`Literal[... "not_found"]`) · `aether.py:117-135` · `gate_state_helper.py:32-34` + `:147` (`"status": verdict`) · `worktree_manager.py:170` (`base_branch: str = "master"`) · `fetch_gate.py:55` (`("master","main")`) 全部逐字命中 ✓ |
| Rule #6 定档 | SOT `skill-benchmark-exemption.md:33` 逐字确有「**`description` 或指令流程变动 ⇒ 一律第二行**」, 且确在「SKILL.md 有变动时的附加约束」段内 ⇒ **D10 / rule6_note 判对, 无 finding** ✓ |
| Level 3 本身 | `standards/openspec/project.md:118` 逐字 `\| 3 \| Full \| Architecture changes \| proposal.md + tasks.md \|` ✓ (但派生不全, 见 m-1) |
| 24 处 gate_check | `grep -c 'gate_check(' tests/test_pre_merge_gate.py` = **24** ✓ (全仓其余命中均为文档/def/CLI 自身) |
| §测试隔离 | `test_sc22` (:710) 确实 patch `pc_module.subprocess.run`, 因模块对象共享而全局生效 ✓; 它自身也是那 24 处之一 (:722 `gate_check(pr_branch="feat/x")`) ✓ |
| D4 的 DEC 依据 | `DEC-20260731-001:29` 逐字「替代义务 (SKILL.md §C.2.4 v1.65.0+): not_applicable 放行必须 surface 警告行」✓ —— 该交换条件保护的是步骤 6 的 **green 分支**, 而 §3 只动 fail 分支, 二者不冲突 |
| CLAUDE.md 逐字 | `:35`「向后兼容 (破坏性变更须 MAJOR)」· `:79`「新增 Skill / Skill 架构重构 = MINOR+」· `:113` Rule #8 (a)/(b) 两腿 ✓ |

---

## Critical

### C-1 (architecture) — §1/D2 的两分支路径解析把 helper 钉死在 Aria 仓布局上; 插件安装形态两条分支都 miss ⇒ Rule #8 闸门在采用方侧变成**硬 abort**; 且同文件 `SKILL.md:262` 的可移植契约既不在 §Impact 也不在 §非目标

**锚点**: `proposal.md §1 :49-52` + `D2 :159` · `aria/skills/phase-c-integrator/SKILL.md:262`

§1 的逐字块只有两个解析目标, 都相对 `git rev-parse --show-toplevel`:

```
<toplevel>/aria/skills/phase-c-integrator/scripts/pre_merge_gate.py     # 主仓根
<toplevel>/skills/phase-c-integrator/scripts/pre_merge_gate.py          # aria 子模块根
```

**但本机上还存在第三个 —— 而且它才是分发形态的那个** (实测存在, 非推断):

```
/home/dev/.claude/plugins/marketplaces/10CG-aria-plugin/skills/phase-c-integrator/scripts/pre_merge_gate.py
```

`diff -q` 与仓内副本 **IDENTICAL** (SKILL.md 亦 IDENTICAL), 即它是活的安装副本。当 `phase-c-integrator` 在**任何其它项目**里被以 `/aria:` 前缀加载时 (CLAUDE.md「其他项目经 Plugin 安装用 `/aria:` 前缀」; memory `project_kairos_adopter` 记 Kairos 是首个跨项目采用者), AI 读到的 SKILL.md 来自这个安装副本, 而块里的 `git rev-parse --show-toplevel` 解析的是**消费方仓**的根 —— 两条分支必然全 miss ⇒ 第三行 `exit 2`。

⇒ **本 Spec 把 Aria 内部的一条假绿, 换成了所有采用方侧的一条恒红**。这正是 memory `feedback_false_green_dual_is_permanent_red` 的判据形状 (「假绿的反面是恒红, 同样零信息量」), 也是 `DEC-20260731-001:19` 逐字否决过的交易 (「等于用假绿换恒红」)。而且它是**硬 abort 不是降级**: §1 逐字「helper 不可达 ⇒ abort (exit 2), 不得降级放行」+ §2 已把兜底命令字面量全部抽走 ⇒ 采用方侧 C.2 无路可走。

**D2 的证据测的是错误的总体**。D2 逐字理由是「`${ARIA_PLUGIN_ROOT}` **全仓从未被赋值**」。但该变量按设计就是**由仓外设置**的: `aria/CHANGELOG.md:2796` 逐字记载它的引入目的是「支持跨项目场景 (非 Aria 主项目时通过环境变量指定路径)」。「在 Aria 仓内没人设它」是预期行为, 不是「它不可用」的证据 —— 与 memory `critique-repeats-error`「反驳数字前必须并列总体/范围/计数法」同形。(`CLAUDE_PLUGIN_ROOT` 那半我复核了: Bash 通道内实测确为 UNSET, Spec 这半说的对。)

**同文件自相矛盾 (点 5 要找的那条形状)**: `SKILL.md:262` 逐字仍是

```
**Helper 实现**: `${ARIA_PLUGIN_ROOT:-aria}/skills/phase-c-integrator/scripts/pre_merge_gate.py` (stdlib + subprocess only)
```

它是该文件里**唯一**的「helper 在哪」声明, 而 §Impact:226 的 SKILL.md 行 (两处散文重整 · 四行裸命令 · `:270` · `:267` · `:279` · 步骤 6 补句) **不含 `:262`**, §非目标也没说「不动 :262」。改后同一份 SKILL.md 将并存两条互相否定的路径契约: `:262` 说走 `ARIA_PLUGIN_ROOT`, D2 说 `ARIA_PLUGIN_ROOT` 不能承重。同族的 `:559` / `:610` 也用同一惯例 ⇒ 本 Spec 实际是在**单点推翻一条文件级惯例**却未声明。

**这不是「可以留到 Phase B 顺手处理」的**: 它决定 §1 那个承重块的形态本身。

**建议方向** (不替 owner 决策, 只给出可判别的选项): (1) 三分支解析 —— 在两条之前先试 `${ARIA_PLUGIN_ROOT}` / `${CLAUDE_PLUGIN_ROOT}`, 保留 abort 兜底 (仍 fail-CLOSED, 但恢复可移植性); 或 (2) 显式把适用面缩到 Aria meta-repo + aria 子模块, 在 §非目标写死「本 change 不为插件安装形态提供入口, 采用方按 `:262` 走」, 并同批修 `:262` 消除矛盾 + 开 issue。**当前版本两者都没做, 而是既未缩范围也未保可移植。**

- introduced_by_r4fix: **true** (R4 版是 `${ARIA_PLUGIN_ROOT:-aria}` + 反斜杠续行; 两分支 + abort 是本版新写, 见 `post_spec-R4-...-tech-lead.md` C-tl-1)
- blocks_phase_b: **true**

---

### C-2 (documentation) — §「#137 的处置」对「(a) 腿」的判断与 #137 上**唯一一条已发布评论**正面冲突, 并据此裁定了一个会发到公开 issue 上的动作; 同段内 (a)/(b) 还有两套互斥语义

**锚点**: `proposal.md:36` + `§Impact:232` · `forgejo GET /repos/10CG/aria-plugin/issues/137/comments` → comment id `18015` (2026-08-08T16:37:00Z, 该 issue **仅此一条**评论)

Spec 逐字:

> #137 报的 (a) helper 缺省是真缺陷, 但它只是两个病因之一; (b) 散文裸命令未被覆盖。**#137 正文关于「(a) 腿」的陈述成立** (`gate_check:378-386` 确证 `not_applicable` 通路存在) ⇒ **不在 body 打删除线**

comment 18015 逐字 (作者 simonfish, 起 Spec 当天):

> **⚠️ 订正正文一处: 「两条腿都失败为绿」不成立 —— 只有 (b) 那条**
> 起 Spec 时 probe 生产态, 发现**我在正文里对 (a) 那条腿的判断是错的** … `unknown` 是 fail-toward-covered … 正文观测到的 `not_applicable` 来自「两仓 workflow 的 `paths` 真的不覆盖本次变更文件」这个**设计内条件**, **与分支名无关**。我把两件事混成一件了。

三处独立缺陷:

1. **事实冲突**。Spec 断言 body 关于 (a) 腿的陈述「成立」; 该 issue 上唯一一条评论逐字断言它「是错的」并已公开订正。R4/knowledge-manager 的 FINDING-6 (`:154`) 也是这么读的。Spec 站在了与已发布订正相反的一侧, **且没有提出任何推翻那条订正的新证据**。
2. **举证不成立**。`gate_check:378-386` 我实读了 (`if pc is not None and pc.get("decision") == "not_applicable":` 块), 它只证明 `not_applicable` 通路**存在** —— 这一点 18015 从未否认。18015 的订正是「它不由分支名错误触发」。用「通路存在」去证「body 关于该腿的陈述成立」是答非所问 (memory `feedback_spec_precedent_verify_execution_history` 同形: 引先例必须核**实际语义**)。
3. **(a)/(b) 一段两义**。同一句里前半把 helper 缺省叫「(a)」, 后半的「(a) 腿」指 PR CI 腿。而 (a)=PR CI / (b)=main in-flight 是本项目的固定约定, 三处 SOT 一致: `CLAUDE.md:113` 逐字「(a) 本 PR CI passing; (b) main 无 in-flight CI run」· `SKILL.md:243`「(b) 轴保留」· `pre_merge_gate.py:318/364` 注释。按约定, 本 Spec 要治的是 **(b)**, Spec 却把它叫 (a)。

**后果不是纸面的**: §Impact:232 逐字要求「aria-plugin #137 补 comment (**不打删除线**, 且须 **supersede** 早先那条…评论)」。按当前措辞落地, 会在公开 issue 上发一条 (i) 重新肯定作者已亲自撤回的 (a) 腿指控、(ii) 把那条撤回评论 supersede 掉、(iii) 用错的腿编号描述本 Spec 治的是哪条腿的评论。

**附带的 supersede 范围未界定**: comment 18015 装了**三样东西** —— (i) (a) 腿订正; (ii) 已放弃的方案 (`refs/remotes/<remote>/HEAD` 解析 + `main_branch_resolved` + 7 SC, 我逐字核对确在该评论内, 故 §「早先那条评论」指代**存在**, 这点 Spec 没错); (iii) 范围路由「本 issue 附带的『`phase-c-integrator` 缺 gate-only 形态』那段**不在该 Spec 范围** —— 它与 #136 耦合, 归 #136」。Spec 只说「supersede 早先那条评论」而未限定到 (ii), 整条 supersede 会连 (i) 和 (iii) 一起作废。

- introduced_by_r4fix: **true**。可实证: R4/knowledge-manager FINDING-6 只要求「补一句 supersede 那个已过时方案」, 并**正确复述**了 18015 对 (a) 腿的订正。R4-fix 吸收了 supersede 那半, 却在同一段新写了与订正相反的「(a) 腿陈述成立」—— 即 memory `fix-recurs-in-fallback` / `stop-adding-rounds` 描述的「修一条时在自己新写的措辞里造一条同形的」。
- blocks_phase_b: **false** (外部沟通面, 但必须在 §Impact 落地前改掉, 否则 Phase C/D 会照字面执行)

---

## Major

### M-1 (architecture) — §非目标 声称「`no_ci_fallback` / stub backend 既有降级语义由 **SC-10** 机械钉住」, 而 SC-10 只测 `enabled=false`; 三条早退里两条零覆盖

**锚点**: `proposal.md §非目标 :217` · `SC-10 :187` · `§6 :119-121`

§非目标逐字: 「**不动** `no_ci_fallback` / stub backend 既有降级语义 —— 由 **SC-10** 机械钉住」。
SC-10 逐字: 「负控: **`enabled=false`** 早退 | 六键不变、无 `gate_error`, 且 `assert ls-remote 未被调用`」。

`enabled=false` 早退 (`:328`) 与 `no_ci_fallback` (`:338` backend is None)、precheck 失败 (`:345`)、stub NIE (`:367-368` propagate) 是**四条互不相干的路径**。SC-10 只钉第一条。⇒ 一个把核验插到 `resolve_ci_backend` **之前**的实现 (§6 只在散文里禁止, 无断言) 会让 `ci_backends: []` 显式禁用与 `no_ci_fallback` 降级全部变成 `fail`, 而 SC-1..SC-12 **全绿**。

这是「立了判据又违反它」的第 4 次实例: §非目标承诺的机械性由一条覆盖不到它的 SC 承担。修法便宜 —— 把 SC-10 拆成 SC-10a (`enabled=false`) / SC-10b (`ci_backends: []` → 走 `_no_ci_output`, 且 `assert ls-remote 未被调用`) / SC-10c (precheck 失败) 三条负控。

- introduced_by_r4fix: true (「由 SC-10 机械钉住」这句是本版新加的机械性声明)
- blocks_phase_b: false

### M-2 (architecture) — §1/§2 对 `### 步骤执行` 那一处的处方结构上不成立, 且「唯一执行入口落在哪一节」全文未定 —— 两个独立实现者会产出不同工件且都过 SC

**锚点**: `proposal.md §1 :46` + `§2 :68-73` + `D1 :158` + `SC-3 :180` + `§Impact :226` · `SKILL.md:101 / :161-181 / :216`

两个子问题, 同一处接缝:

**(a) 折叠块塞不进去。** `### 步骤执行` 里的 C.2.4 条目在 `SKILL.md:161-181`, 而 `:101` 开、`:216` 闭的是一个 ` ```yaml ` **围栏代码块** (实测 `grep -n '^```'`)。`<details><summary>…</summary>` 落进围栏内只会呈现为字面文本, 并破坏那份 YAML 文档的可解析性。而且那一处**没有「5 步」** —— 它是 `primitive 调用:` / `三态结果:` / `output:` 三个 YAML 字段, 「5 步」只存在于 `### C.2.4` §执行流程 (且实为 1/2/2.5/3/4/5 六项)。§2 逐字「**两处**散文的 5 步移入折叠块」+ §Impact:226 把两处并列为「散文流程重整」, 对第一处两个描述都不成立。

**(b) 唯一入口落哪一节没定。** §1 逐字「新增**唯一**执行入口」, SC-3 期望 **1**。但全文没有一句规定它落在 `### 步骤执行` 还是 `### C.2.4`。而 §Why:19-28 的根因逐字是「**AI 走散文那份**」并点名 `### 步骤执行` 的 `:167`/`:168` —— 若唯一入口落进 `### C.2.4`, 被点名为病灶的那一节就只剩去字面量后的描述, 治愈与否取决于 AI 跨节跳转, 而 SC-1..SC-12 **没有任何一条能区分两种落法**。这是 memory `spec-underdetermination`「两独立实现者同规格得相反结果」的判据命中, 且落在承重条款 D1 上。

- introduced_by_r4fix: true (§2 折叠块 + SC-3=1 的组合是本版形态)
- blocks_phase_b: **true** (Phase B 第一件事就是改这两处, 现在无法确定改成什么)

### M-3 (implementation) — §5 自称「本表自带**完整分区**」但不完整: 缺 `FileNotFoundError` / `OSError` / 129 三类; 同包内 `path_coverage.py:93` 恰有现成先例未采纳

**锚点**: `proposal.md §5 :100-110` (含 `:108` 的「**本表自带完整分区, 不依赖越界援引**」) · `path_coverage.py:93` · `pre_merge_gate.py:12`

我实测的分区结果:

| 情形 | 实测 | §5 表 |
|---|---|---|
| 存在 / 不存在 / remote 不存在 / 坏 URL / 非 git 目录 | 0 / 2 / 128 / 128 / **128** | ✓ 覆盖 (128 一行吸收了后三者) |
| `--exit-code --heads` 传空 pattern | **2** | 落进「不存在」⇒ fail, fail-CLOSED, 可接受 |
| 参数用法错误 | **129** | ✗ 表外 |
| **`git` 二进制缺失** | 无退出码 —— Python 抛 `FileNotFoundError` (实测) | ✗ 表外 |
| 一般 `OSError` (fd 耗尽 / 权限) | 无退出码 | ✗ 表外 |

后两类不是退出码而是**异常**, 会穿透 `gate_check` —— `pre_merge_gate.py:12` 模块契约逐字「Other exceptions propagate (unchanged from prior behavior)」⇒ helper traceback 非零退出。而 §1 的 abort 分支只覆盖「**文件不可达**」, 不覆盖「**跑了但崩了**」。于是在一个自称 fail-CLOSED 的设计里, 留了一个交给 AI 临场裁量的洞 (Rule #10 反模式的入口)。

尤其可惜的是**同一个包里就有正解**: `path_coverage.py:87-97` 的 `_run_git()` docstring 逐字「Never raises」, 并 `except (subprocess.TimeoutExpired, FileNotFoundError, OSError)` 三者一并翻译。§5 却自造了一张只有退出码维度的表并宣布它完整。这也是 memory `invariant-dimension` 的形状: 表的**维度** (退出码) 不覆盖错误的**维度** (异常)。

- introduced_by_r4fix: true (「自带完整分区」这句断言是本版新加, 且它把表从「援引 :260」改成了自证)
- blocks_phase_b: false

### M-4 (architecture) — §1 强制块里的 `--remote "<REMOTE>"` 占位符全文无取值规则, 而本仓是双 remote + 镜像分叉是四次复发的事故形状

**锚点**: `proposal.md §1 :52` · `§5 :93` · `CLAUDE.md §多远程推送 — 两条硬约束`

§5 给了函数默认 `origin`, 但 §1 的**逐字强制块**把它变成必须现填的占位符 `--remote "<REMOTE>"`, 而全文没有一句说这个值怎么取。本仓的实际 remote 集合是 `origin` (Forgejo, 也是 CI backend 所在平面) + `github` (镜像), 且 CLAUDE.md 用一整节记着「半推造成镜像分叉」是 Aria #165 四次复发的形状。

这条是 **fail-CLOSED 的承重腿**, 取错 remote 两个方向都出错: 镜像滞后 ⇒ `refs/heads/master` 查不到 ⇒ 误 `fail` 阻塞合并; 镜像超前/分叉 ⇒ 查到但不是 CI 那个平面的 ⇒ 误放行。

Spec 也从未写下本该写的那条不变量: **核验必须打在 CI backend 查询的同一个 remote 上**。§5「已知残留限制」承认了 git 平面 ≠ API 平面, 但只承诺「同一个 `main_branch` 值且同一个 cwd」, 没承诺同一个 remote。

最便宜的修法: 从强制块里**删掉** `--remote`, 让默认 `origin` 生效 (与 CI 平面一致), 并在 §5 写死「非默认取值须与 CI backend 同源」。

- introduced_by_r4fix: true (`--remote` 进入强制块是本版)
- blocks_phase_b: false

### M-5 (documentation) — §Impact 缺**发版同步面**整行; 本 Spec 自引为 Level 3 先例的姊妹 Spec 恰好用整行列了 18 个引用点并警告两条 custom check 不是兜底

**锚点**: `proposal.md §Impact :224-233` + `§版本 :237-243` · `openspec/changes/linked-issue-normalization/proposal.md:271-272`

本 Spec 要 ship 一个 ≥MINOR 的插件版本, 但 §Impact 八行里没有任何一行覆盖发版同步面, §版本只有一句「号段落地时按 `plugin.json` 当前版本计算, 不预写字面量」。

对照本 Spec 在 `:5` 明确引为升级理由的姊妹 Spec `linked-issue-normalization`, 它的 Impact:271 是一整行, 逐字列出「**普通引用文件 18 个引用点**: 主仓 14 … + aria 侧 4 …; **append-only 账本 2 个** … 外加主仓 **gitlink**」, 并明写「⛔ **两条 enabled custom check 不是机械兜底**: `m6-version-badge-match` 只比 README badge, `i18n-readme-translation-currency` 只比 `translated-from` ⇒ **7 处**残留旧版本时二者仍全绿 = 假绿」, 且已为此开 **Aria #177** (`CLAUDE.md:81` 同款错误清单)。

即: 「照 CLAUDE.md 的发布同步面那行走」这条隐含兜底**本项目已知不成立且已立案**。本 Spec 既没列面, 也没引 #177, 也没声明「发版面由 Phase D 的既有流程承担」。memory `scoped-add-splits-claim` 记的「发布同步面漏 6 处」正是这条漏掉后的实际后果。

- introduced_by_r4fix: false (Impact 表历版都无此行)
- blocks_phase_b: false

### M-6 (architecture) — §版本把 CLAUDE.md:79 与 :35 描述成「两条成文条款**指向不同**」是逻辑错误: `MINOR+` 是下界, MAJOR 满足它 ⇒ 二者交集唯一为 MAJOR; 「地板 = MINOR」给下游留了一个看起来合规的违规口

**锚点**: `proposal.md :8 (ship target)` + `§版本 :237-241` · `CLAUDE.md:35` · `CLAUDE.md:79`

逐字核对结果:

- `CLAUDE.md:79` = 「新增 Skill / Skill 架构重构 = **MINOR+**」 —— 这是**下界** (MINOR 或更高)。
- `CLAUDE.md:35` = 「向后兼容 (**破坏性变更须 MAJOR**)」 —— 这是**定值**。
- MAJOR ∈ MINOR+ ⇒ **两条不冲突**。在 Spec 自己认定「D5 使 CLI 参数由可选变必填 … 是**教科书式破坏性签名变更**」(`:241` 逐字) 的前提下, 二者的交集**唯一**, 就是 MAJOR。

所以 §239 的「两条成文条款**指向不同**」是错的, 由它推出的「地板 = MINOR, MINOR vs MAJOR 待 owner 裁」也就把一个**已被条款确定**的结论降级成了裁量项。风险不是学术的: 「地板 = MINOR」这句会被下游 (Phase C/D、release flow、未来 session) 当作「发 MINOR 合规」的依据, 而按 `:35` 那是违规。

正确的两条出路 (二选一, 都要写进 Spec 而不是留给裁量):
1. 认定这是破坏性变更 ⇒ **地板 = MAJOR**, 请 owner 确认的是「是否接受 MAJOR」而非「MINOR 还是 MAJOR」;
2. 论证 `gate_check()` / `--main-branch` 不构成 `:35` 意义上的对外破坏性变更 (例如: 二者都是 skill 内部接口, 无 documented public contract) ⇒ 那么地板 = MINOR **成立**, 但必须**把这个论证写下来**, 而不是把它伪装成两条条款打架。

当前版本两条都没走, 而是用一个不成立的「条款冲突」把结论悬置。这也踩到 memory `exact-exception-condition`「援引成文条款前逐字核对确切条件」。

- introduced_by_r4fix: true (§版本这段的「指向不同」框架是本版新写, R4 版 ship target 只写 MINOR)
- blocks_phase_b: false

---

## Minor

### m-1 — Level 3 定档正确, 但派生的交付物不全: SOT 同文另有一处逐字要求 `detailed-tasks.yaml`, 且本 Spec 自引的两个先例都带它

**锚点**: `proposal.md :5` + `§Impact :230` · `standards/openspec/project.md:118` 与 **`:21`**

`:118` 逐字 `Level 3 = Architecture changes → proposal.md + tasks.md` ✓ Spec 引对了。但**同一份 SOT 的 `:21`** 逐字是「任务表达 | Level 3: `proposal.md` + `tasks.md` + `detailed-tasks.yaml` (**双层**)」。Spec 只引了 `:118` 一处, 并当作 SOT 的单一口径。

实证倾向 `:21`: 本 Spec `:5` 自引的先例 `linked-issue-normalization` **有** `detailed-tasks.yaml`; 同一个 skill 的前一个 Spec `phase-c-integrator-ci-path-coverage` **也有**; `aria-2.0-m6-dispatch-input-delivery` 也有。(另有若干 Level 3 只有 tasks.md, 故惯例确实不一致 —— 正因如此更该在 Spec 里明说走哪条, 而非默认。)

`§Impact:230` 只新建 `tasks.md`。建议: 要么补 `detailed-tasks.yaml` 行, 要么写一句「本 Spec 不建 detailed-tasks.yaml, 理由 X」并顺带记一条 SOT 自相矛盾的 follow-up。

### m-2 — §6 的排序理由与 §5 的诚实限制互相抵触: 核验的维度 (远端 ref) ≠ 被保护的使用的维度 (本地 ref)

**锚点**: `proposal.md §6 :128` · `§5 :114` · `path_coverage.py:436-447`

§6 逐字「**在 path coverage 之前**: 它更早消费 `main_branch`, 放它之后等于**放行一次未核验的使用**」。但新核验查的是 `ls-remote <remote> refs/heads/<main>` (**远端**), 而 `evaluate_path_coverage` 消费 `main_branch` 的方式是 `git diff --no-renames <main>...<pr>` (`path_coverage.py:436`, **本地** ref)。一个在远端存在、本地不存在的 `main_branch` 照样让 path coverage 走 `git-diff-failed → unknown`。

⇒ 该理由**名义成立、实质不成立**; 而 §5「已知残留限制」自己只承诺「同一个 `main_branch` 值且同一个 cwd」, 没承诺跨平面等价。行为上无害 (unknown 是 fail-toward-covered), 故只记 Minor —— 但 D9 的两条腿之一是空的, 应改写理由或改成「顺序不重要, 选此处因 X」。

### m-3 — §2「去掉**全部**可执行命令字面量」无机械覆盖, 一条可执行字面量可以整条存活而 SC 全绿

**锚点**: `proposal.md §2 :68` · `SC-1 :178` / `SC-2 :179` · `SKILL.md:240`

SC-1 只钉 `aether ci status` (4 命中), SC-2 只钉 `"branch": "main"` (1 命中)。`### C.2.4` 执行流程步骤 1 (`SKILL.md:240`) 的 `aether --help | grep -q "in-flight"` 是可执行命令字面量, 两条 grep 都不命中 ⇒ 可以原样留在折叠块里而 SC 全绿。「全部」这个全称词没有对应断言。(memory `fix-the-class`: 全称句 sweep 最容易在同批新造一个漏网。)

### m-4 — SC 表「今日实测」列的**设计**: 无日期无 SHA 锚, 不可复算也不会自失效

**锚点**: `proposal.md SC 表表头 :174` + 「今日实测」列

表头声明「每条 grep 断言的 pattern 与今日计数均已实跑」范围限定正确 (只声称 grep 断言, 不越界到 SC-6..SC-12 —— 那 7 条该列为「—」, 诚实 ✓), 所以这不是假绿。但作为**设计**有两点弱:

1. 「今日」无绝对时点。文件头 `Created: 2026-08-08`, 本轮已跨到 2026-08-09; 任何人再改 SKILL.md 该列即静默腐烂, 且没有任何机制会发红 (memory `feedback_spec_frontmatter_reflects_reality`)。
2. 该列的功能是给「怎么会红」提供证据, 但承重的 SC-6 (D6) 恰恰是「—」。

建议改成「基线 SHA + 命令」两列 (例: `aria@af87cae` + 逐字命令), 使它可复算。

### m-5 — §1 四行块隐含「必须作为**单次** shell 调用整体执行」, 而 Aria 的执行通道不跨调用保留 shell state; Spec 只钉了「单行无续行」(为过 SC-3)

**锚点**: `proposal.md §1 :46` (「逐字, **全部单行, 无反斜杠续行**」)

`GATE` 是 shell 变量, 第 2/3/4 行都依赖它。Aria 的 Bash 通道逐字声明「Shell state (env vars, functions) does not persist」跨调用。若 AI 把四行拆成四次调用 (对一个被标为「逐字」的多行块并非不可能), 第四行退化成 `python3 "" --pr-branch …`。Spec 为了让 SC-3 的单行 grep 命中而强调「无反斜杠续行」, 却没有把真正的执行前提 (「整块一次跑完」) 写进去。一句话可补。

---

## Verdict

**FAIL** (≥1 Critical)。

- Critical 2 · Major 6 · Minor 5
- **10/13 条 introduced_by_r4fix = true** (false 的 3 条: M-5 · m-2 · m-3) —— 与四轮规律一致, 且 C-2 是「吸收上一轮 Major 时在同一段新造同形缺陷」的直接实证。
- **blocks_phase_b = true 的两条**: C-1 (承重块形态未定且对分发形态恒 abort) · M-2 (Phase B 第一件事就是改那两处, 但改成什么当前无法确定)。
- 本轮我**未**发现的问题面 (供交叉核对): §1 两 cwd 可达性与 abort 阻断 (实跑通过) · D6 pattern 锚定 (第三次独立复现通过) · §5 表内已有的 0/2/128 三行 (实测通过) · 全部 6 个 `pre_merge_gate.py` 行锚点与 8 处外部引用 (逐字通过) · Rule #6 定档与 SOT 引文 (逐字通过) · D4 的 DEC 依据 (通过, 且我复核出它保护的是 green 分支, 与 §3 只动 fail 分支不冲突)。

### 关于第 4 条待审点 (§7 `raw_message` 主通道 vs `SKILL.md:252-255`) 的单独判断

我实读了 `SKILL.md:255` (「`fail` → BLOCK + 输出 verdict + **raw_message**, phase-c-integrator return failure」)。**衔接得上** —— `raw_message` 本就是既有 surface 通道, §7 把它定为主通道是顺着既有措辞走, 不是新造。D4「只补一句」在**机制层面成立**, 故我不开 finding。

但要给 owner 留一句提醒 (不计入 finding, 因为它落在措辞而非机制): §3 要补的那句逐字是「若 `raw_message` 含 `gate_error` 诊断则一并 surface」。`raw_message` 是字符串, `gate_error` 是它的**兄弟键**, 「raw_message 含 gate_error」在 §7 定义的 schema 里不成立; 而且 §7 逐字规定 `gate_error.message` = 「同 raw_message」⇒ 「一并 surface」信息量为零。建议改成「`gate_error` 在场时一并回显 `kind` 与 `remote`」之类**有增量**的措辞, 否则就是 memory `fix-recurs-in-fallback` 记的「有记录 ≠ 有路由」的另一个实例。

---

## 轮次记录

| 轮 | 席位 | 本席位 verdict | 说明 |
|---|---|---|---|
| R1-R4 | 各 5 席 (20 agent-run) | — | 范围两次重定, 本轮按指示**不核对旧清单** |
| **R5** | tech-lead (本报告) | **FAIL** | 2C + 6M + 5m; 11/13 由 R4-fix 新引入 |

**收敛判断 (供编排层)**: 按 memory `stop-adding-rounds` 的判据 —— 加轮与否看 **major 数是否还在降**, 而非 critical 是否归零。本轮 major 未降且新引入占比 = 10/13, 按 memory `marginal-return-negative` 已到「本轮 fix 引入的 major 占比 > 1/2」的拐点。⇒ 我的流程建议是: **不要再加第 7 轮**。R6 应把范围收缩到本报告 C-1 / C-2 / M-2 三条 (它们决定承重块的形态与外部动作), 其余 M/m 直接吸收不再复审; 若 R6 后 major 仍不降, 按该 memory 应换新鲜眼睛或上报 owner 裁, 而非继续同构加轮。

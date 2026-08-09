---
track-id: premerge-gate-mainbranch-failclosed
owner-container: aria-runner-bot/023236f2
phase: session-close
status: done
updated-at: 2026-08-09T14:10:00Z
---

# Session Handoff (2026-08-09) — 一份 Spec 跑掉 6 轮 30 席审计, 而结论是「执笔的那个环节才是瓶颈」

> **本段主线一句话**: 承前一段 §6 第 1 条, 跑 `premerge-gate-mainbranch-failclosed` 的 post_spec。结果是 **R1–R5 五轮 25 个 agent-run 未收敛** + post_planning R1 五席, 合计 **30 席 / 37 份报告**。
>
> **最有价值的产出不是这份 Spec** —— 它至今 `converged: false`。是**五轮量化出来的一条规律**: 席位稳定找到真问题, 而**编排层每一轮 fix 引入 73–100% 的新 Major**, 总量五轮持平 (21→26→22→27→21)。
>
> ⭐ **并发轨同日在另一个 Spec 上独立复现了同一形状, 且 owner 给出了同一处方 (「换人执笔」)** —— 见 §4.1。这条从孤例升级为可复现规律。

## §0 入口 (新 session 优先读)

- **当前态**: 本地 master `98ad1f5`, **落后两远端 3 个 commit** (`2ada533`, 全部来自并发轨 `simonfishgit`)。**本段零推送、零提交** —— 所有产物仍在工作树。
- **未提交产物**: `openspec/changes/premerge-gate-mainbranch-failclosed/` 三件套 (proposal 改, tasks.md + detailed-tasks.yaml 新建) + **37 份 audit 报告 (untracked)** + 1 份 audit-trail。
- **Spec 状态**: `Approved for Phase B (owner override)` —— **不是收敛**, 是 owner 依据五轮数据裁定停止「审计→改文档」循环。
- **下一步**: 见 §6。**开工前必先 rebase/merge 那 3 个 commit** (其中一个新增了 `.aria/probes/plugin-cache-currency.py` 探针 + `state-checks.yaml` 条目, 会影响 `/state-scanner` 输出)。
- ⚠️ **本段有意未更新 `docs/handoff/latest.md` (Rule #10 留痕)**: 该文件**已分叉** —— 本地指向 `2026-08-08-silknode-...`, 远端 (领先 3 commit) 已由并发轨改为指向 `2026-08-09-issue172-closure-and-128-r4-r5-...`。在落后状态下编辑它, 合并时必然冲突且会覆盖一侧指针, 即本项目反复栽的「handoff 链失真」。⇒ **指针更新推迟到下段 rebase 之后**; 且当前 `collision.kind = self_multi_container`, 按 `session-handoff.md §2.3` 多 track 场景, 届时应考虑写 **deprecation banner 指向看板**而非单指针。**这是主动不执行 handoff-write SOT 的一个子步骤, 请复议。**

## §1 已完成 (本段)

1. **post_spec 跑满 R1–R5** (5 席 × 5 轮 = 25 agent-run, `max_rounds` 由 owner 从 4 加到 6, 用 5 余 1)。逐轮: R1 21 条 → R2 26 → R3 22 → R4 27 → R5 21 (均为去重后)。**五轮均 5/5 或 4/1 REVISE, 从未收敛。**
2. **Spec 经历两次范围变更 + 三次重写**: R1-fix 结构性重写 → R2-fix 大幅减法 → R3-fix **范围重定 (承重项从「加固 helper」换成「收敛 SKILL.md 两份实现」)** → R4-fix。
3. **A.2 产物落地**: Level 由 2 升 **3** (判据表输出栏直接管辖), 建 `tasks.md` (20 条) + `detailed-tasks.yaml` (schema 对齐姊妹 Spec, DAG 无环、依赖闭合、12 字段齐全)。
4. **post_planning R1** (5 席): 4 REVISE / 1 PASS, 去重 3C+12M+8m。**本轮缺陷集中在验收断言与依赖图, 不在拆解结构** —— 与前五轮性质不同。
5. **post_planning R1 的机械可修项已全部改完** (owner 裁定「先把本轮可修的改掉」): 见 §1.6。
6. **本段最实的一次修复 —— SC 断言从「失明」改到「对抗性验证过」**:
   - post_planning 抓到 **全套验收对 `--main-branch` 完全失明**: 构造 `--main-branch main` 写死的实现, SC-M1/M2/M3 得 **0/0/2 全过** (3 席独立命中 + 编排层复现);
   - 修法: SC-M3 拆为 **M3a (占位符=2, 红窗) + M3b (无字面值, 负控) + M3c (折叠块内无调用, 负控)**;
   - **验证方式本身升级**: 不再只验「当前值对不对」, 而是**建三个 fixture 做对抗性验证** —— 好实现全过, 「写死 main」被 M3b 拒, 「藏进折叠块」被 M3c 拒。**这是本 session 第一次验证断言的「拒绝能力」而非「当前取值」。**

## §2 未完成 / Carry-forward

**AI 内省 (load-bearing)**:

- 🔴 **Spec 未收敛且未进 Phase B**。`converged: false` + `overridden_by_user: true`。post_planning R1 后仍有 **6 条阻塞项**, 其中机械可修的已修完, 余 **4 条须 owner 裁**:
  1. **ship_target = MAJOR 的确认** —— 若确认, v2.0.0 会激活 `pre_merge_gate.py:68/:116` 自带的「removed in v2.0」弃用到期承诺 (已建 `TASK-020` 条件承接; 若非 MAJOR 则该任务须显式 cancelled 留痕而非静默删)。
  2. **`ARIA_PLUGIN_ROOT` vs `CLAUDE_PLUGIN_ROOT` 的约定归属** —— `phase-c-integrator/SKILL.md` 内部用 `ARIA_` (`:262`/`:559`/`:610` 三处), 全仓主流是 `CLAUDE_` (66 处 vs 5 处)。`TASK-002` spike 需要一个方向。
  3. **`SKILL.md:559` / `:610` 归属** —— 分属 `submodule_gate.sh` 与 `git-remote-helper` 两个无关 helper, `TASK-014` 是否应覆盖。
  4. **`ci_backends/aether.py` 是否入 scope** —— `TASK-004` 若要抽取共享重试逻辑, 该文件不在 `scope_repos.paths` 内。
- 🔴 **零提交零推送** —— 40 份产物全在工作树, 且**本地落后 3 个 commit**。下段须先 rebase/merge 再定提交策略。推共享 master 属外向动作, 须 owner 显式授权 (memory `sync≠push-auth`)。
- 🟡 **post_planning 未收敛** (R1/4)。是否跑 R2 未裁。
- 🟡 **Rule #6 定档已定但未执行** —— 第二行「照跑 AB, 零裁量」, `TASK-015` 已点名须用 `/skill-creator`, 未跑。

**机械补漏 (backstop)**: `handoff_autofill` unfinished **226** 条 (本 Spec 占 19, 其余 8 个活跃 Spec 占 207 —— **非本段引入**); consistency **11 flags 全是 `active_change_not_in_upm`** (Aria 无 UPM, **恒亮**); sync **2 条 warning** (`[main] parity=behind vs github/origin`) —— 这条是真信号, 已在 §0/§7 处置。

## §3 owner 裁定记录 (本段 8 次)

| # | 裁定 | 触发点 |
|---|---|---|
| 1 | R1-fix 用**结构性重写**而非逐条补丁 | R1 后 |
| 2 | Rule #6 改判**照跑 AB** | R1 后 (⚠️ 前提由编排层提供, **后被证伪**) |
| 3 | 停止循环, 改**大幅减法 + spike-first** | R2 后 (major 10→15 上升 + fix 引入占 100%) |
| 4 | Rule #6 改判**第三行** | R2 后 (⚠️ 前提由编排层提供, **再次被证伪**) |
| 5 | 减法版仍须**过 R3** | R3 前 |
| 6 | **重定范围: 改治 SKILL.md 层** | R3 后 (TC1 推翻三版共同前提) |
| 7 | **加 2 轮配额** (`max_rounds` 4→6), 我再改 | R4 后 (编排层已提示预测, owner 仍选此路 — 决定已记录) |
| 8 | **进 Phase B, 用 TDD 接管** + **跑 post_planning** + **写 detailed-tasks.yaml** + **先修本轮可修项** | R5 后 |

> ⚠️ **裁定 2 与 4 的前提均由编排层提供且均被证伪** —— 两次方向相反。详见 §4.3。

## §4 关键风险 / 已知陷阱

### §4.1 ⭐ 本段最重要的发现: 两条独立轨同日收敛到同一结论

**本轨 (`023236f2`) 的五轮数据**:

| 轮 | C | M | m | 合计 | 本轮 fix 引入 (Major) |
|---|---|---|---|---|---|
| R1 | 5 | 10 | 6 | 21 | — |
| R2 | 3 | 15 | 8 | 26 | **100%** |
| R3 | 3 | 10 | 9 | 22 | **9/10** |
| R4 | 4 | 14 | 9 | 27 | **11/14** |
| R5 | 3 | 11 | 7 | 21 | **~8/11** |

**并发轨 (`simonfishgit`) 同日在 `secret-guard-per-segment-evaluation` (#128) 上** (commit `333bc1a`):

> post_spec R4 (5 席全 REVISE, 6C+13M, max_rounds 耗尽) → owner 裁 [2] 先修 Critical → R4-fix (**主 loop 执笔**) → owner 批准超配 R5 全量重审 (5 席全 REVISE, 9C+12M, **判定 R4-fix 引入 22 条新错**) → **owner 裁定换人执笔** → R5-fix (**tech-lead 执笔, 主 loop 只核验**)。

且其 R5 核心发现的形状极干净: **R4-fix 的换行守卫治了 fail-open 却造出 fail-close, 覆盖面 (13/13) 比它修的 (11/13) 还广** —— 「修复比病更广」。其中一条缺陷是 backend-architect **找出自己 R4 提案的问题**。

⇒ **两条轨、两个不同 Spec、同一天, 各自独立收敛到「主 loop 执笔是瓶颈」, 且 owner 两边都给出「换人执笔」的处方。** 本轨尚未试过该处方 —— 这是下段最值得做的实验。

### §4.2 三条有干净实证的方法论 (均不在现有 memory)

1. **机械自检抓错值, 抓不了错问题。** R4-fix 版通过了编排层 **23 项机械自检 (23/23 全绿)**, 而 R5 的 3 条 Critical **全部在自检覆盖之外**。典型: 我问「`ARIA_PLUGIN_ROOT` 在仓里被赋值了吗」→ 答「否」→ 自检通过 ✅; **该问的是「本仓定位 plugin root 的约定是什么」** → 答 `CLAUDE_PLUGIN_ROOT` (66 处)。**自检验的是我写下的断言的值, 验不了我该不该问这个问题。**
2. **断言的维度必须匹配病灶的维度。** 全套 SC 对 `--main-branch` 失明: 我的断言量是 `--pr-branch`, 病灶量是 `--main-branch`。**成因尤其值得记**: R5 抓到「SC-3 期望值与 D1 矛盾」后, 我改断言时挑了一个**不会和 D1 打架**的量 —— **优化了文档的内部自洽, 把它与缺陷的连接优化掉了**。(与既有 `invariant-dimension` 同族, 但成因是新的。)
3. **重写会静默清零已付出的修复。** SC 编号与既有测试冲突 (`test_path_coverage` 占 1-8/16-20/23-28, `test_pre_merge_gate` 占 9-13/15/21/22, 我的 SC-1..13 **十三个号全撞**) —— 该问题在 R2-fix 版**已用 `SC-M*` 前缀修好**, **重定范围时静默丢失** (当前 `SC-M` 计数曾归 0)。⇒ **重写的成本不只是新增风险面, 还包括让已付出的修复归零, 且无任何机制会发红。**

### §4.3 编排层 (AI) 自身错误 —— 六轮累计 22 条, 留痕在 audit-trail

高频形状 (每种均 ≥2 次实证):

- **引先例不核承重位** ×3: 引 `:737` 抄形状没抄环境变量名 · 称 `:262/:559/:610` 用 `CLAUDE_PLUGIN_ROOT` (实为 `ARIA_`, 方向相反) · 引 `:242` 时用 `cut -c1-150` 截断致误判;
- **同一文件内既立判据又违反它** ×5: 论证「换字面量不够」却按字面量处置 `:167` · 写「不得越界援引」却援引 `:260` 的 1-126 (实测失败码 128) · 引用「假绿的反面是恒红」却写出对所有采用方恒红的路径解析 · 「零裁量 grep」写成恒红 · SC-3 期望值未随 D1 扩面更新;
- **测错总体 / 量的定义不清** ×2: `ARIA_PLUGIN_ROOT` 的搜索对象错 · 「helper 3 个副本」把同一 inode 数两次又漏三份 cache (实为 5 条路径);
- **修落一处、声称留另一处** ×1: §版本 改 MAJOR 但抬头与 tasks.md 未同步;
- **对 Python 语义的错误断言并已外传** ×1: 断言 `test_sc22` 的 patch 只对 path_coverage 生效 —— 受控实验推翻 (`import subprocess` 使模块对象全局共享)。**该断言曾向 owner 陈述过**。

### §4.4 其他

- **闸门状态必须被如实读**: post_spec `converged: false` + `overridden_by_user: true`, **不是收敛**。任何下游读到「Approved for Phase B」时必须一并读到这两个字段。
- **post_planning 是独立 checkpoint**: `max_rounds=4` 重新起算, 与 post_spec 那 6 轮无关。
- **一次 cwd 事故**: 受控实验把 shell cwd 带跑, 导致 R3 汇总报告**第一次写盘静默失败** —— 是同命令内跟的 `ls` 计数抓到的。⇒ **回执不等于落盘** 再次实证。

## §5 四维一致性 (机械)

`consistency_check` **11 flags 全是 `active_change_not_in_upm`** (Aria 无 UPM, **恒亮**, 非本段引入)。活跃 change 由 10 增至 11 (本 Spec 三件套齐后仍计 1)。

## §6 Next session 入口 + 优先级

1. 🔴 **先 rebase/merge 落后的 3 个 commit** (`2ada533`)。其中 `71bdd60` 新增 `.aria/probes/plugin-cache-currency.py` + `state-checks.yaml` 条目, 会改变 `/state-scanner` 的 custom_checks 输出 (由 8 项变 9 项)。
2. 🔴 **裁 §2 的 4 条** (MAJOR 确认 / PLUGIN_ROOT 归属 / `:559`+`:610` 归属 / `aether.py` 入不入 scope) —— 它们卡住 `TASK-002`/`TASK-004`/`TASK-014`/`TASK-020` 四条任务。
3. 🔴 **决定提交策略** —— 40 份产物 (含 37 份 audit 报告) 未提交。姊妹轨的做法是把审计报告随 Spec 一起 commit。推共享 master 须显式授权。
4. ⭐ **强烈建议试「换人执笔」** (§4.1) —— 并发轨已在另一个 Spec 上由 owner 裁定并执行 (tech-lead 执笔, 主 loop 只核验)。本轨五轮数据指向同一结论但**尚未试过该处方**。这是当前信噪比最高的一步。
5. 🟡 **post_planning R2 是否跑** 未裁 (R1/4)。
6. 🟡 **Rule #6 照跑 AB** (`TASK-015`) 未执行, 须用 `/skill-creator`。

## §7 同步状态 (autofill 机械汇编)

```
[main]              master = 98ad1f5 | github=behind(3) origin=behind(3)   ⚠️ 落后并发轨
[standards]         (detached) = 2111c84
[aria]              (detached) = af87cae
[aria-orchestrator] feature/m6-cost-model-telemetry = 92acce5 | origin=equal
```

**warnings: 2** (`[main] parity=behind vs github` / `vs origin`) —— **不是漏推, 是并发轨推了新东西**。本段 ahead=0, 无待推内容。**本段零 push、零 commit。**

## §8 Memory entries this session

```
[候选 memory]
- 「机械自检抓错值, 抓不了错问题」—— 通过 23/23 自检的那版, 3 条 Critical 全在覆盖之外; 判据是「我验的是我写下的断言, 还是我该不该问这个问题」。type: feedback
- 「断言的维度必须匹配病灶的维度」的**新成因**: 为消除文档内部矛盾而更换断言量, 会把断言与缺陷的连接一并换掉 (SC-3 从 --main-branch 面滑到 --pr-branch 面)。与既有 invariant-dimension 同族, 成因不同。type: feedback
- 「重写会静默清零已付出的修复」—— SC-M* 前缀修好过又在范围重定时丢失, 无机制发红。重写的成本包含已付出修复的归零。type: feedback (新形状, 现有 memory 无此条)
- 「验断言要验它的拒绝能力, 不只验当前取值」—— 对抗性 fixture (好实现 + 两个像样的坏实现) 是低成本高收益的做法, 本段第一次用就关掉了 2 个失明面。type: feedback
- 「两条独立轨同日收敛到『主 loop 执笔是瓶颈』」—— 跨轨复现, owner 两边处方均为「换人执笔」。type: project

[未写下经验]
- 「多轮审计的边际产出转负后, 继续加轮 vs 换执笔人」的选择判据尚未成文 —— 本段五轮 + 并发轨五轮共十轮数据可支撑一条, 但需要 owner 参与定义「什么时候该换人」。
- 「Spec 的处方边界」—— 本段最后确立了「Spec 钉『什么算对』(SC), 不钉『怎么写』(降 spike)」, 有效但只跑了一轮, 样本不足以成文。
```

**已有覆盖未重复落**: 引先例不核承重位 ([[feedback_delegation_must_verify_target_actually_does_it]]) · 假绿恒红对偶 ([[feedback_false_green_dual_is_permanent_red]], 本段第 4 次实证) · fix 在自己兜底路径复发 ([[feedback_fix_recurs_in_its_own_fallback_path]], 本段 5 次) · 边际产出转负 ([[feedback_audit_marginal_return_goes_negative]], 本段五轮量化) · 回执不等于落盘 ([[feedback_output_hygiene_no_raw_control_bytes]]) · 声称 vs 落盘 ([[feedback_scoped_git_add_splits_claim_from_landing]])。

## §9 流程判断留痕 (Rule #10, 请复议)

- **闸门全部跑满未自行缩减**: post_spec 5 轮 × 5 席全部派出, 零 spawn 失败、零超时、无降级、无改序。`max_parallel_agents=2` 全程遵守。
- **`drift_guard` 未启用**是 config 默认所致 (`convergence_mode` 默认 false), **非 AI 裁量** —— 已在每轮汇总留痕。
- **post_planning 未自行跳过** —— A.2 完成即触发该 checkpoint, 我把它作为决策点上报而非自行处置 (Rule #10)。
- **两次 Rule #6 定档均由我提供前提且均被证伪**, owner 两次据此裁定。**第三次 (第二行「照跑 AB」) 的依据改为 SOT 直接管辖条款而非我的实证** —— 三席逐字核过。**请复议这条定档。**
- **Level 3 与版本地板由我按成文规则直接定** (判据表输出栏 / CLAUDE.md:79), 未上报 —— 依据是「有直接管辖条款时先读条款」。**MINOR vs MAJOR 的剩余分歧仍交 owner。** 请复议这个「定到地板、只上报剩余分支」的做法。
- **本段零提交、零推送、零外部动作** (未在 #137 发任何评论 —— R5 抓出原计划会推翻我自己上一 session 的订正)。
- **R4 后 owner 加轮时我已提示预测** (「R5 大概率再出约等量新 Major, 多数是我这次 fix 新造的」), owner 仍选该路径, 我按全量执行并如实记录。预测**被 R5 数据证实**。

## Cross-references

- 前一段: [2026-08-08 post_planning 四轮 + 三起跨仓转交](./2026-08-08-post-planning-four-rounds-and-three-cross-repo-transfers.md)
- 并发轨同日: `2ada533` (`docs(handoff): 会话收尾 — #172 闭环 + #128 R4/R5 + 换人执笔裁定`)
- Spec 三件套: `openspec/changes/premerge-gate-mainbranch-failclosed/{proposal.md,tasks.md,detailed-tasks.yaml}`
- **审计轨迹 (append-only, 与交付面分居)**: `.aria/audit-reports/premerge-gate-mainbranch-failclosed-audit-trail.md`
- 六轮汇总报告: `.aria/audit-reports/post_spec-R{1..5}-*-aggregate.md` + `post_planning-R1-*-aggregate.md`
- 30 份席位报告: `.aria/audit-reports/post_{spec,planning}-R*-premerge-gate-mainbranch-failclosed-{role}.md`
- 关联: aria-plugin [#137](https://forgejo.10cg.pub/10CG/aria-plugin/issues/137) (**本段未在其上做任何操作**) · Aria [#177](https://forgejo.10cg.pub/10CG/Aria/issues/177) · aria-plugin [#127](https://forgejo.10cg.pub/10CG/aria-plugin/issues/127)

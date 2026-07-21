---
track-id: session-close-20260720-0721-rule6-formalize-165-converge
owner-container: simonfish/bfe8285d
phase: session-close
status: done
updated-at: 2026-07-21
---

# Session Handoff — 会话收尾: Rule #6 判据成文 + #165 从基建收敛成两条规范

> 会话维度增量。承接 [上一份 session-close](./2026-07-20-session-close-rule10-audit-and-rule6-ab.md)（已 done 冻结）之后的一段：
> 上次收尾后 owner 继续给了三条指令 —— Rule #6 判据成文、给 standards 配 push mirror（被 owner 自己的质疑撤回）、方案 D + 纪律层。
> **本段的主线是「一个观察被 owner 的朴素质疑纠正为更省的方案」。**

## §0 入口 (新 session 优先读)

- **当前态**: 三仓双远程一致 —— 主仓 `9dfd4f0` / standards `b98cf73` / aria `da15d0f`（均已用新规范约束 2 的 ls-remote 方式核验）。custom check 全绿。
- **本段时序**: 上次收尾 → owner「把 Rule #6 判据改成内容是否影响 AI 行为并成文」→ 新 convention `skill-benchmark-exemption.md` + CLAUDE.md Rule #6 重写 + 回复 #113 → owner「给 standards 配 push mirror」→ 我调查 → **owner 质疑「本地双推不就够了吗」** → 我承认论证错位 + 落 #165 → **owner 裁「方案 D + 纪律层」** → CLAUDE.md 多远程推送 +两条硬约束 → #165 状态更新（观察期 + 关闭条件）。
- **下一步**: 见 §6。

## §1 已完成 (本段)

1. **Rule #6 判据成文** — 从「文件落在哪个目录」改为「**内容是否影响 AI 行为, 以及那个行为 AB 套件测不测得到**」。SOT 下沉 `standards/conventions/skill-benchmark-exemption.md`（standards `b98cf73`，与规则 #10 的 `configured-gate-authority` 同族互引），CLAUDE.md 只留精简决策表 + 指针（**删了旧的目录判据**，不留两套）。四行决策表，第三行（authoring 向导：处方性但 AB 测不到）刻意设计成比照跑更麻烦（点名行为 + 建可证伪 fixture + 记套件缺口），防「AB 测不到」变捷径。回复 aria-plugin #113（它那条提请裁定的项现在有答案）。
2. **#165 从基建工程收敛成两条规范** — 见 §7，本段最重的一件。
3. **CLAUDE.md 多远程推送 +两条硬约束**（主仓 `9dfd4f0`）: 约束 1（方案 D）子模块一律本地合并 + 双推，禁 Forgejo 服务端合并；约束 2（纪律层）推后逐个 ls-remote 核验，不信 push 回执。

## §2 未完成 / Carry-forward

**AI 内省 (load-bearing)**:

- 🔴 **凭据轮换 — 现在是第四次未回**: `FORGEJO_TOKEN` / `NEXUS_API_TOKEN` / `CF_ACCESS_CLIENT_SECRET` 因本会话早段一处断言失误进 transcript。代码侧已堵死，但**脱敏≠闭环**。上次 handoff 记「三次未回」，本段又过了一整轮 owner 交互仍未触及。这是**跨两次会话收尾都在 §2 顶部、始终没有回音的唯一事项**——它不会因为收尾而消失，只会越积越旧。
- **Aria #165**: 保持 **open 作观察窗**，有可判定关闭条件（≥3 个跨子模块 cycle 遵守约束 1 无 orphan / 约束 2 至少捕获一次真实漏推-半推 / 期间无新事故）。本会话已捕获一次半推分叉，计入条件 2。
- **Rule #6 边界成文已完成**（本段做完），但**成文本身尚未经一个真实 cycle 检验**——下个改 `references/rules/*` 或 authoring 向导的 cycle 是它的第一次实战。
- **Aria #169**（AC-5 落位重构，未开始）/ **Aria #168**（5 项 deferred + AC-5 语义补齐）/ **aria-plugin #116**（AB baseline 污染，4 方案待评估）。

**机械补漏 (backstop)**: `handoff_autofill` 报 159 条 unfinished，逐条核验**全属其它 6 个 active spec**（m6×4/m7×2），本段零残留。`consistency_check` advisory flags 均结构性（Aria 无 UPM）。sync 零 warning（三仓双远程 equal）。

## §3 关键风险 / 已知陷阱 (本段新增)

- 🔴 **我把「观察」直接滑成「行动建议」，被 owner 的朴素质疑纠正**: 撞见 standards 漏推 2 commit → 我说「所以该配 push mirror」→ 而那个漏推是**纪律类**（本地双推就能防），不是 push mirror 要解决的**机制类**（服务端合并）。我拿错了证据的类别去论证方案。owner 一句「本地双推不就够了」戳破，最终收敛成零基建的方案 D + 纪律层。→ memory `feedback_match_evidence_class_to_solution_class`（本段核心教训）。
- **cwd 混淆本会话第三次**: grep CLAUDE.md 时在 aria 子模块里，报 no such file。已有 memory `feedback_git_minus_c_for_submodule_push` 覆盖，且上次 handoff 已记「违反既有 memory」——**仍在犯**。这说明「知道规则」不等于「不犯」，可能需要更强的机制（每个跨仓命令强制绝对路径 / `git -C`，而非靠记）。是本会话反复最多的操作错误。
- **shell 反引号吃内容本会话第二次**: commit message 用双引号含反引号 → 被当命令替换 → commit 没发生而尾部检查照打 ✅。上次收尾已记一次。同样是「知道但仍犯」类。

## §5 多维度同步状态 (机械核验)

- **git**: 主仓 `9dfd4f0`（origin=github=local，本段用约束 2 ls-remote 逐个核验）/ standards `b98cf73`（三方一致，本段顺带补齐其此前落后 github 的 2 commit）/ aria `da15d0f`（三方一致）/ aria-orchestrator detached 只读。
- **custom checks**: 全绿。**sync 零 warning**（不同于上次收尾时主仓落后双远程）。
- **规范新增**: CLAUDE.md +Rule #6 决策表 +多远程推送两条硬约束；standards +`skill-benchmark-exemption.md`。
- **并发**: 本段**与 bot 零撞车**（上次收尾后 bot 未推主仓）——是本整个会话唯一一段没撞车的。

## §6 Next session 入口 + 优先级

1. 🔴 **凭据轮换**（§2，第四次未回）。
2. **#165 观察期**: 下个跨子模块 ship 必须走约束 1（本地合并，不用 Forgejo Web merge）——**这也约束我自己**，本会话给 aria 子模块一直走的是 Forgejo PR `Do: merge`，从此改本地合并。
3. **Rule #6 成文的首次实战**: 下个改 `references/rules/*` / authoring 向导的 cycle 按新决策表走一遍，验证第三行（定向 fixture + 记缺口）实际可操作。
4. **#169 / #168 / #116** 承前。
5. 承前 owner 门: M6 四门 / 168h 跑 / M7 fleet。

## §7 本段对方法论本身的影响

- **Rule #6 的豁免判据从「按目录」进化到「按内容对 AI 行为的影响」**——同日两起真实案例（Phase 4 的 dispatch 表 / #113 的 authoring 向导）证伪了目录判据，逼出内容判据。新增的「AB 测不到的处方性内容」第三行是这次成文的核心增量。
- **#165 从「要不要配 push mirror」收敛成两条零基建规范** —— 这是 owner 一句质疑（「本地双推不就够了」）触发的重构。它揭示的通用道理：**一个兜底机制的价值 = 基础手段覆盖不到的独占增量；若那个增量能被更省的手段消除，机制就是过度工程**。方案 D（消除服务端合并路径）恰好消除了 push mirror 的唯一独占价值。
- **两条规范都当场约束了我自己**: Rule #6 成文后回看 Phase 4 应照跑（已补跑）；多远程约束 1 立后回看本会话的 Forgejo PR merge 正是它禁止的（commit 里已自曝）。规范不是写给未来的，是立刻生效的。

## §8 Memory entries this session (本段)

**已落 (1 条新)**:
- `feedback_match_evidence_class_to_solution_class` — 用「X 坏了」论证「建机制 Y」前先核实 X 属于 Y 的目标类；拿纪律问题证据推机制兜底=论证错位。

**本段未落 (已有覆盖)**: cwd 混淆（`feedback_git_minus_c_for_submodule_push`）/ 反引号吃内容（已在上次 handoff §3 记）—— 两者都是「已有 memory 但仍在犯」，属执行纪律衰减，非缺 memory。**值得 owner 知道: 本会话这两类各犯了 2-3 次，靠"记住"不够。**

## Cross-references

- 上一份 session-close: [2026-07-20-session-close-rule10-audit-and-rule6-ab.md](./2026-07-20-session-close-rule10-audit-and-rule6-ab.md)
- Rule #6 SOT: `standards/conventions/skill-benchmark-exemption.md`
- 多远程规范: CLAUDE.md「多远程推送」段 §两条硬约束
- issues: [Aria #165](https://forgejo.10cg.pub/10CG/Aria/issues/165)（观察期）/ [Aria #168](https://forgejo.10cg.pub/10CG/Aria/issues/168) / [Aria #169](https://forgejo.10cg.pub/10CG/Aria/issues/169) / [aria-plugin #113](https://forgejo.10cg.pub/10CG/aria-plugin/issues/113) / [aria-plugin #116](https://forgejo.10cg.pub/10CG/aria-plugin/issues/116)

---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-07-08T19:48:39.383Z
context: openspec/changes/agent-router-auto-project-agent-injection/proposal.md
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R1 审计报告 — tech-lead lens

被审对象: `agent-router-auto-project-agent-injection/proposal.md` (Level 2, 修 Forgejo Aria #153 发现 B)。本报告全部结论对四个源文件真读核验 (SKILL.md 449 行 / ROUTING_RULES.md / capabilities-taxonomy.yaml / 三份上游 Spec)，非凭 proposal 转述。

## 审计结论 (逐条 finding 带证据)

### C-1 (Critical, architecture) — B5 diff 护栏与 AC-1 auto-win 在黄金场景自相矛盾

这是本轮头号问题，直接落在我的角色侧重 (B5 护栏是否足够 / 主链改动对模式波及)。

proposal 自己引的 #153 黄金数据 (proposal.md:21-22): `database-specialist` CAP=**1.00**, `backend-architect` FP=**0.95**。改造后二者同池 (B2, proposal.md:48『取全局最高』)。B5 (proposal.md:86)『差值<0.1 降级推荐 (沿用既有规则)』——我核实『既有规则』就是 ROUTING_RULES.md:198-201『多个 Agent 差值<0.1→降级到推荐模式』和 SKILL.md:389『多个 Agent 置信度都>threshold→降级到推荐模式』。黄金场景 top-2 差值=0.05<0.1，且 1.00/0.95 双双>0.9 阈值 → **双重触发强制 recommend**。

但 AC-1 (proposal.md:113) 要求『auto 模式该 agent...胜出。复现 #153 场景』。#153 bug 的本质是『auto 从不 *使用* database-specialist』。B5 使黄金场景退化 recommend → database-specialist 只是『进池且排名第一』，仍未被 auto 路由。于是 B2/AC-1(auto route) 与 B5/AC-4(diff<0.1 degrade) 不可同时成立。即便把『胜出』宽读成『排名第一』，spec 对其唯一动机例的 mode 结果仍未消歧，且若 degrade recommend 则 #153 只被部分修复。**spec 的首要成功条件按其自采护栏不可达**，判 Critical。

修法 (三选一，须使 AC-1/AC-4/AC-5 自洽): (a) diff 护栏只在同类候选内比 (CAP-vs-CAP / FP-vs-FP)，跨类另裁；(b) 堵短路场景豁免 diff<0.1；(c) 接受 degrade 并重写 AC-1 措辞。

### M-1 (Major, implementation) — required_caps 的 task→标签推断无成文映射，B3 确定性主张不成立

CAP 分子分母都依赖 required_caps。proposal.md:44/62 把 `task_type→caps ∪ 关键词→caps ∪ file-path→caps` 当已知算子，但我核验：`capabilities-taxonomy.yaml:1-146` 只有 tag→synonyms（无 task-feature→tag 映射）；`ROUTING_RULES.md` 的 FP/TT/keyword 三表 (:27-54/:59-85/:91-143) 全部映射到 **Agent 名**而非能力标签。B3 (proposal.md:84)『复用 gap-analyzer 标签重合率语义』亦不精确——`agent-project-adapter/proposal.md:126-138` + `m7:114` 显示 gap-analyzer 的 required 来自 `.aria/project-profile.yaml` **项目场景**，不是单条 task。agent-router 又是纯 prose fork (SKILL.md:10-12)，故 task→标签这步实为 LLM 判断，与 B3『确定性/可审计』直接冲突，AC-1/AC-2 的 CAP 分数不可机械复现。修：补 task-feature→tag 映射表，或改 B3 措辞为半确定性，并让 fixture 同时 pin 住 task→required_caps。

### M-2 (Major, architecture) — B2 尺度不可比 + 能力劫持误派 (角色侧重: B2 风险面)

B2『同池取全局最高』把 FP/TT (路径/类型匹配强度) 与 CAP (标签覆盖率) 两条异质语义轴当同尺度比。required_caps 小 (单标签 task) 时任一覆盖它的项目 agent 即 1.00；B4 精度 tiebreak (proposal.md:85) 只破 match_rate 完全相等的平局，**不阻止饱和**。B5『<0.1』是刀刃阈值: project 1.00 vs plugin FP 0.90 (ROUTING_RULES.md:29 FP-001=0.90) 差值恰=0.10，『<0.1』不含 0.1 → 仍 auto 路由项目 agent。同名保护 (SKILL.md:417-421 / D9) 只防同名不防按能力抢占。AC-2 (proposal.md:114) 仅测显然 disjoint 的『UI task vs DB caps』，兜不住『误标签/过宽项目 agent 靠小 required_caps 饱和抢占强 FP 插件』——这正是我被要求核验的『项目级 agent 抢走插件级路由』场景。修：给 CAP 设独立胜出门槛/最低 required_caps 基数；补对应误派 AC。

### M-3 (Major, implementation) — 『强制 3d』与既有 scan_project_agents/plugin_only 配置冲突

proposal.md:82/41 把 3d 定为主链『强制』步，全篇未提既有配置。我核实 SKILL.md:429-431 已有 `agent_router.scan_project_agents`(默认 true)/`plugin_only`(默认 false)，且 SKILL.md:421 明文承诺『plugin_only: true 忽略项目级 Agent』的退路。若 3d 无条件执行则破坏该退路 (回归)；AC-3 零回归 (proposal.md:115) 只测空目录、不测 `plugin_only:true`。附带：B6『复用 audit-augmentation AC-3 范式』(proposal.md:87) 不精确——audit-augmentation 是 experimental default-off (其 proposal.md:68)，空路径天然零成本；agent-router **常开**，3d 每次都跑，零回归需另证。修：3d 受 scan_project_agents/plugin_only 门控 + AC-3 增 plugin_only:true 子用例。

### m-1 (Minor, documentation) — §393 改写把正确的 D4 rationale 误判为『误导 framing』

proposal.md:74 要删的 SKILL.md:408『Plugin 不会自动加载 .aria/agents/』其实**事实正确**且是载重设计依据 (agent-project-adapter D4 :190 / m7:34)。真正误导的是『扫描已生效』的暗示，非 Plugin-vs-Skill 说明本身。修：接线机制的同时保留 D4 rationale。

### m-2 (Minor, documentation) — SKILL 既有版本漂移 + proposal 定位不准

机械核验 SKILL.md:17=`1.0.0` vs SKILL.md:449=`1.1.0` 已漂移；frontmatter (L1-13) 无 version。proposal.md:7/74『frontmatter/footer v1.1.0→v1.2.0』两处失准，照字面改会让 L17 继续停 1.0.0。修：header(L17)+footer(L449) 统一 bump 到 1.2.0。

### m-3 (Minor, testing) — recommend (默认模式) 无专门 AC；manual 不波及未刻画

SKILL.md:62 recommend 为默认、SKILL.md:263 subagent-driver 实用 recommend，但 AC 全限 auto。manual 因 step2 (SKILL.md:216-219) 前置返回永不到 3d，proposal 未说明。修：补 recommend Top-3 纳入 AC + 注明 manual 不受影响。

### m-4 (Minor, documentation) — 对 M7 依赖关系的表述反转所引 L129 (角色侧重: scope 边界核验)

proposal.md:26 称 M7『依赖 agent-router 好用...兑现二者依赖的前提』，但 m7:129 明说『本 Spec 不依赖任何未实现的 routing 能力, 也不改 agent-router』(并见 m7:202/219/237/244)。audit-augmentation 半句 (:16) 确凿，M7 半句反转。**结论: scope 真不相交**——本 change 改 agent-router internals 但保留 I/O 契约 (task→recommendation + .aria/agents/ 扫描)，未破坏 m7 abi_compat(a)(:13)；OOS proposal.md:103 (发现 A→M7 B.2) 与 m7:28-29/:125 一致，准确。仅 Why 措辞需拆分 + 提醒 M7 Phase B 的 v1.1.0 black-box pin 须 re-baseline。

### m-5 (Minor, documentation) — AC-6『版本 5 文件』低估发版全清单

proposal.md:118『5 文件』只覆盖版本一致性子表，漏 CLAUDE.md 发布清单里的主项目 submodule pointer / 主项目 VERSION / root README badge (m6-version-badge-match)——badge/pointer 是历史高频漂移。§What-3 (proposal.md:76) 已引全清单，故内部略不一致。修：AC-6 对齐全集，注明 i18n 本次免重译 (#140 B档) 但 badge 必 bump。

## Verdict

**FAIL** (1 Critical + 3 Major)。**vote = REVISE**。

- Critical C-1 使 spec 首要成功条件 (auto 路由项目级 agent、复现 #153) 按其自采 B5 护栏不可达，必须先消解 B2/B5/AC-1/AC-4/AC-5 的自洽性再进 A.2。
- 三个 Major (required_caps 无成文映射 / B2 尺度劫持 / 强制步破配置退路) 均需 rework，且都动摇 CAP 机制的可实施性与零回归保证。
- Level 2 定级本身**合理** (单 Skill + additive + 无 net-new 文件，对齐 audit-augmentation 先例)；版本语义 (SKILL MINOR / plugin v1.53.0→v1.54.0 MINOR) **符合** CLAUDE.md 规范——这两项无需改。scope 与 M7/audit-augmentation **真不相交**，仅表述层面待订正。

## 核验锚点 (code_anchors)

- proposal.md:14-28 / 32-51 / 55-70 / 72-76 / 80-88 / 101-118 (被审全段)
- SKILL.md:10-12,17,216-237,262-265,389,393-421,429-431,449
- ROUTING_RULES.md:27-54,59-85,91-143,172-186,190-201
- capabilities-taxonomy.yaml:1-146 (仅 tag→synonyms),136-139
- agent-project-adapter/proposal.md:126-138,169-181,190/193/196 (D4/D7/D10)
- m7-agent-lifecycle/proposal.md:13,34,119-129,202,219,237,244
- audit-augmentation/proposal.md:16,68,82
- plugin.json:4 (1.53.0) / CLAUDE.md#版本管理规范
- change dir = proposal.md only (Level 2 确认)
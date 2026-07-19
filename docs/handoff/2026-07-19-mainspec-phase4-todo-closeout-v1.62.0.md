---
track-id: state-scanner-stale-refs-false-parity
owner-container: simonfish/bfe8285d
phase: D.3
status: done
updated-at: 2026-07-19
---

# Session Handoff — 主 spec Phase 4: 29 TODO 实质收口 → ship v1.62.0 → 归档

> cycle 维度。承接 [v1.60.0 核心 ship](./2026-07-19-mainspec-false-parity-core-ship-v1.60.0.md) 与 [会话总账](./2026-07-19-session-close-mainspec-marathon.md)。本轮把主 spec 剩余 29 TODO 的**实质项**收口并走完 Phase C/D，spec 已归档。

## §0 入口 (新 session 优先读)

- **本对话时序**: `/state-scanner` 开局 → owner 选 [1]+[3] 并要求先核并发冲突 → 四维核实无冲突 + `phase1_gate` 认领 → 三个 owner 裁决 (#165 只评估 / OQ-C 不造冷却 / 实质项做完再走 C/D) → 8 轮实施 (含 2 个并行 agent) → 双轮对抗 review 修 2C+5I+3M → rebase 让位 bot 的 v1.61.0 → ship v1.62.0 → 跨仓落地 → D.2 归档。
- **当前态**: 主 spec **已归档** `openspec/archive/2026-07-19-state-scanner-stale-refs-false-parity`。aria `9af7b21` (v1.62.0) / 主仓 `e7883b0`，三仓双远程 parity 齐，8 custom check 全绿。
- **下一步**: 见 §6。

## §1 已完成 (本 cycle)

实质 TODO 全部收口，测试 **1219 → 1248**：

1. **task 6.1/6.2/1.6/6.4** — F5′ `enforced_remotes`/`read_only_remotes` 接进核心裁决。此前它们**只**影响 gitlink 循环与 F3′ fetch 范围，不影响 `_overall_parity` ⇒ 配了等于没配；更糟的是 remote_refresh 早已跳过 read-only 腿的 fetch，而裁决仍向它索要新鲜证据 ⇒ **配了 read_only 的采用者 parity 恒 false**。现在 fetch 范围与裁决范围收敛为同一集合。命名空间按 phase-c-integrator §C.2.5 step 3 已发布契约继承顶层，消 cross-skill split-brain。
2. **task 3.4** — git 非交互契约 (`stdin=DEVNULL` + `GIT_TERMINAL_PROMPT=0` + `GIT_SSH_COMMAND` BatchMode/ConnectTimeout)，收在 `_common._run` 单一咽喉点，覆盖 47 个调用点 + F3′ 全部 fetch。
3. **task 2.12 (AC-5)** — snapshot 跨 collector 自洽检测，实现在 `scan.py` 装配层（跨 collector 不变量不属于任一 collector；且 multi_remote 1.12 早于 handoff_multibranch 1.17，放前者需重排 collector 顺序）。
4. **task 1.10/7.2** — 退役 `verify_mode`/`_remote_parity_ls_remote`（第三个独立可达性计算点，正是本 spec 要消除的缺陷形态）+ ≥8 处 SOT 清扫。
5. **task 13.3/9.2 + OQ-C** — drift dispatch 第七路 (gitlink 层，与 remotes[] 层六路正交) + 离线降级裁定。
6. **文档/测试** — 1.8/3.2/10.4/10.6/10.7 drift 收口；2.4/2.9/2.10 AC 直接断言；11.2 AB rubric 按 v4+ unknown 二分语义精确化。
7. **Phase C/D** — v1.62.0 5 处 SOT + PR#115 merge + 双远程 + 主仓 gitlink/VERSION/badge/i18n×3 + CLAUDE.md live 覆写 + D.2 归档。

## §2 未完成 / Carry-forward

**spec 内明示未做** (已写进归档 proposal.md 顶部，不冒充完成)：

- 🔴 **3.16 k_eff `observed_rotation` — DEFERRED** (fail-CLOSED)。k_eff=k_min 冷启动兜底，**AC-15 防饥饿仅对 rotation ≤ 3 的采用者完全成立**；大仓会被砍腿 → expired → 偏红。**不得记 AC-15 已完全满足。**
- **3.5d** 永久失败 leg 退避 / **3.10** collector 依赖逐一核对表 / **13.7** gitlink contains 性能实测附表 / **11.1** `/skill-creator` AB benchmark (本 cycle 改动集中在机械 collector，未动 SKILL.md 指令面)。

**跨 cycle**:
- **Aria #165** (镜像漏推) — 已产出 A/B/C 评估报告发到 issue 评论。**核心结论: F10″ 不可直接复用为 bump 守卫**（五个函数全私有符号 / 签名深绑 scan 缓存与 generation / `orphan_unverified` + D18「连续 k 次 scan」收敛语义在单点 bump 时刻无定义）⇒ B 的成本按「新写」估。推荐 C 但先做 A，且 **A 的健康监控探针必须算 A 的组成部分**（Forgejo push mirror 失败默认不告警，否则退化成「有兜底的错觉」，比现在更危险）。5 个未决问题待 owner 拍板（凭据形态 / 镜像哪些分支 / C.2.5 是否扩展 / B 的 mode flip 条件 / 监控放哪）。
- 🔴 **凭据轮换未做**: `FORGEJO_TOKEN` / `NEXUS_API_TOKEN` / `CF_ACCESS_CLIENT_SECRET` 因本 session 一处断言失误（`assertIn` 对 dict 查键 → 失败时 unittest 把整个 env 渲染进 diff）进入 transcript。代码侧已改成不可能再打印 env 并加了 Rule #7 注释，但**脱敏≠闭环**，owner 尚未回复是否轮换。

## §3 关键风险 / 已知陷阱 (本 cycle 新增)

- 🔴 **「我自己的测试把自己的洞锁成正确行为」**（AC-5 fail-OPEN 实证）: 我把 `rc != 0`（评估失败）和 `rc == 0 且空输出`（真答案）合并成一个静默 `continue`，而 rc!=0 的总体**与被检测条件正相关** —— 守着原始事故的唯一探针在事故邻域失声。更糟的是我配了一条测试断言「此时应当静默」，把洞固化成契约。**只有对抗 review 读代码抓得到**；任何后来者修这个洞都会先撞上我那条测试并误以为是回归。
- 🔴 **fixture 形状恰好绕开缺口，第三次**（task 1.6 继承实证）: `_load_config` 的 `if not block: return {}` 早退杀死继承，而「整块缺席」正是绝大多数采用者的形态。我的继承测试在 skill 块里塞了个无关的 `enabled: True` 保持块非空 ⇒ 恰好走不到早退分支。**两个 review agent 独立命中同一条**。
- **退役字段留下活消费方**: `reachable` 随 ls_remote 退役成常量 true，`session-closer/handoff_autofill.py` 的 `reachable is False` 静默变死码 ⇒ handoff 从此不报 remote 不可达。退役时必须 grep 全仓消费方，不能只清 SOT 文档。
- **agent 的「还原」会吃掉你在制的编辑**: code-reviewer 做变异测试时改写并「逐字节还原到 HEAD」了 `multi_remote.py`/`_common.py`，把我未提交的 I1/I2/M1 修复一并抹掉（它如实自报了）。**并行跑 review agent 时，主 loop 的在制改动应先提交**，或明确禁止 agent 写文件。
- **编号匹配勾选会误伤 SUPERSEDED 区**: tasks.md 有两个 13.x 块（F10″ 现行 + F10′ 已证伪「勿实施」），按编号正则勾选把 superseded 的同号任务也勾上了 —— 归档门要抓的正是这种虚标，自查阶段拦下。
- **勾了却留着「(TODO: …未完成)」批注**: 22 行。归档门 `gate_result` 的 `unverified_claims` 回显的就是这些旧文本 —— 机器读到的是自相矛盾的 spec。

## §5 多维度同步状态 (机械核验)

- **git**: aria `9af7b21` (origin=github=local 三方 ls-remote 核验一致) / 主仓 `e7883b0` (origin=github 一致) / standards·aria-orchestrator detached 只读。
- **custom checks**: 8/8 绿（`issue-cache-freshness` 从 skip 转 pass —— Spec C 的 lag-1 探针拿到了上一份 snapshot）。
- **版本**: 插件 v1.62.0 / 主项目 v1.7.3 / 3 份 i18n README @ 1.62.0（marker + badge + 正文版本行各 3 处）。
- **归档门**: verdict=warn / 0 block / complete=False。

## §6 Next session 入口 + 优先级

1. **owner 决策待回**: (a) 凭据轮换（见 §2）；(b) #165 五个未决问题。
2. **规则 #10 复议请求**（本 cycle 的流程判断，按规则要求显式摆出）: 本 cycle 是既有 Approved spec 的 Phase B/C/D，未产出新 spec/planning 产物，故 `post_spec`/`post_planning`（配置里唯二 enabled）按「checkpoint 结构性前提不成立」未跑；而配置里 `pre_merge: off` 我反而跑了两轮对抗 review。**请复议这个判断是否成立** —— 若认为 Phase 4 这种「大批量收口」应当重跑 post_planning，我这次就是踩了规则 #10。
3. 承前 owner 门: M6 四门 / 168h 跑 / M7 fleet。

## §8 Memory entries this session

- **候选**: 「自己写的测试把自己的 fail-open 锁成正确行为，只有对抗 review 抓得到」—— 与既有 `feedback_agent_authored_tests_encode_own_bug_false_green` 同族但主语是**主 loop 自己**而非 agent，值得单落。
- **候选**: 「并行 review agent 的『还原到 HEAD』会抹掉主 loop 未提交的在制改动」—— 操作纪律，既有 memory 未覆盖。
- **已有覆盖不重落**: fixture 贴合 bug（`feedback_check_predicate_must_validate_against_real_data_range`）/ 并发 bot 撞车（`project_aria_runner_bot_autonomous_same_repo_work`）/ i18n 正文漂移（`feedback_version_checks_blind_to_i18n_readme_body`）。

## Cross-references

- 归档 spec: `openspec/archive/2026-07-19-state-scanner-stale-refs-false-parity/`
- aria PR#115: https://forgejo.10cg.pub/10CG/aria-plugin/pulls/115
- Aria #165 评估报告: https://forgejo.10cg.pub/10CG/Aria/issues/165#issuecomment-16241
- CHANGELOG v1.62.0 (行为变更 4 项 + 明示未做 3 项)

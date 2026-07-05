# Tasks: Interactive Session Dedup — Layer L Advisory Activation + Structured Carry-ID

> **Change ID**: `interactive-session-dedup-coordination`
> **Level**: 3 | **Decision**: DEC-20260704-002 | **Mother engine**: multi-terminal-coordination (Layer L, 完成其 TASK-024 集成)
> 粗粒度功能交付单元(OpenSpec 双层架构 Layer 1);4-8h 颗粒度 + 文件路径 + agent 分配由 A.2/A.3 `detailed-tasks.yaml` 保证。
> post_spec R1 fixes 已落地(见各 task 内 R1-* 标注)。

## 1. 接线 + block→advisory（P1 — 修死代码/完成 TASK-024,本 Spec 首要交付）

- [x] 1.1 `.aria/config.json` schema + config-loader 默认值:**复用既有 `state_scanner.coordination.enabled`**(R1-C2,**不新建** `coordination_gate`;该键承载 rule 1.54/#133 AC-2 互斥不变式)+ **新增子键 `state_scanner.coordination.mode: advisory|block`**(默认 advisory)。文档化:mode 与 enabled 正交(仅 enabled==true 相关),不改 rule 1.54 disjointness
- [x] 1.2 **AI 编排层**接线(R1-C1,**非 scan.py**):state-scanner 阶段 2 推荐检查 `tracks_multibranch.collision.kind` → 用户确认进 Phase B(phase-b-developer B.1 / branch-manager)→ 调 `phase1_gate.run_gate(raw_track_id=<carry-id 原始串>, phase="B", ...)`。对齐 `layer-l-integration.md:15/44`(闸门 Phase B 启动前调,不在 scan.py);完成从未落地的 TASK-024 集成。SKILL.md 记录接线点 + config 触发条件
- [x] 1.3 `phase1_gate.run_gate` advisory 模式(R1-M1):新增 `mode` 参数;advisory 下**放行 = 跳过 `_call_decision` 的 abort/yield 动作,像 7d 分支无条件执行 step 8/9(acquire_claim `:573` + resilient_push `:640`)写并推送自己 claim**,额外返回 surface 标记(占用 7c `:517` / 偏移 7b `:476` / push-fail step9 `:640` 均放行);**但 surface 内容按分支分化,不 blanket 静默丢弃 7b 告警**(R2-Major-B):7b 须保留 `max_clock_skew_seconds` 信号;**reconcile winner 判定(`reconcile.py:163`)不改**;block 模式保留原 abort/yield/block
- [x] 1.4 state-scanner 阶段 2 推荐区 surface 输出契约(**按分支分化**,R2-Major-B):(a) **7c 占用** → 🔴 "<owner/container> <age> 前已认领 <carry-id>",**回显供逐字 copy 的精确 carry-id 串**(R1-m5);(b) **7b 时钟偏移** → 🔴 "⚠️ 时钟偏移 <skew>s(>30s)—— winner 判定可能有误,查容器时钟";放决策前必经推荐区(决策点 9,与 Layer H 看板同位)
- [x] 1.5 P1 golden test(R1-M1/m10 + R2):(a) **run_gate 编排器直测**(现无直测,本 task 是首个)—— advisory outcome 映射:占用/偏移/push-fail 三路径在 advisory 下均**放行且 `own_claim != None` 且真调 acquire_claim/push**,block 下保留 abort/yield;(b) reconcile 确定性不受 mode 影响;(c) `coordination.enabled` 关闭时零调用(向后兼容);(d) **接线缝合测试**:AI 编排层消费路径真把 carry-id 原始串传入 run_gate 并拿到 advisory outcome(非只测 phase1_gate 内部);**A.2 前先定该缝合的可自动化接口契约**(R2-qa-Minor-2:如 SKILL.md 约定固定 CLI 契约 或暴露 `consume_carry_id()` 可导入函数作编排层↔run_gate 唯一耦合点),否则"首个直测"易退化成只测 phase1_gate 内部;(e) **advisory 7b 分支断言仍暴露 `max_clock_skew_seconds` 告警**(非只放行)

## 2. 结构化 carry-id + handoff 稳定身份（P2 — 根治病根 + 根除漂移）

- [x] 2.1 `standards/conventions/session-handoff.md` §2.3 加结构化 carry-id schema:§6 每条 carry-forward = `{id, desc}`;id 约定 kebab `carry-<slug>`(**禁 `:`** —— `derive_track_id` 替换表 `track_id.py:28` 不译冒号);**当 §6 carry-id 与本 handoff frontmatter `track-id` 指同一工作时取相同原始串**(推荐直接复用 track-id,R1-M5,防同一工作算两条 track;**复用时不强制 `carry-` 前缀**,前缀仅新起 carry-id 的可读性约定,R2-Minor);明确 carry-id **留 §6 prose 层,不进 frontmatter**(向后兼容硬约束);**显式划界 §6 carry-id(human-curated)vs §2 `carry_forward_inventory`(机读,tasks.md inline 注解自动汇入)—— 后者 id 化留 #95/follow-up**(R1-M5,防"以为已根治漏大头")
- [x] 2.2 `aria/templates/session-handoff.md`(**aria-plugin 子模块 track**,R1-M4)§6 skeleton(`:181-197`)加 `{id, desc}` carry-id 结构(prose markdown,非 frontmatter)
- [x] 2.3 carry-id → gate 消费路径:开工时 AI/人读 §6 选 carry-id → **原始串作 `raw_track_id` 喂 `run_gate`,由 run_gate 内部(`:354`)调 `derive_track_id` 归一**(R1-m6,归一职责在 run_gate,调用方不预归一);human-in-the-loop,无 collector 自动解析 §6
- [x] 2.4 handoff-write 改用 `identity.py::get_identity().owner_container`(`identity.py:67-70`)填 frontmatter `owner-container`:接入 `phase-d-closer` D.3 / `session-closer` step4 / 共享 SOT `handoff-mechanics.md`(或机械化到 `handoff_autofill.py`);替代 AI 手填
- [x] 2.5 向后兼容回归测试:(a) §6 加 carry-id 后 `handoff.py` frontmatter 解析仍取 5 字段、doc 不退化 legacy;(b) carry-id 归一单测(`carry-m6-blocker3-spec` 幂等 / `carry:x` 有归一但约定禁用);(c) **旧无-carry-id §6 行 = 不触发 gate 消费**(R1-m2 明确二选一:未打标行不喂 run_gate,ship 当天存量 handoff 防护=部分生效直至迁移;不把整行自由文本当隐式 carry-id 以免保留病根);(d) 两容器 `get_identity` 产出不同 container_id(home_dir 注入);(e) 同一 handoff 内 track-id ≡ 对应 carry-id 归一后一致(R1-M5)

## 3. runtime 探针 + AB harness（P3 — 防再死代码 + trigger 定夺）

- [x] 3.1 runtime-invocation 探针(#95 修法示范,R1-m1 + R2-Major-C):custom-check / 遥测断言 `run_gate()` **生产分区真有新近记录**;**防伪 = 结构性来源判别,不可被调用方参数覆盖**(否则 harness 单跑即假绿 = 本 Spec 引用的 `feedback_noop_in_test_env_hardening_needs_mechanism_assertion` 复现)。具体形状 A.2 定二选一:(a) 双入口分区(生产 `run_gate()` vs harness 显式 wrapper,写不同 telemetry 分区,探针只读生产分区);(b) 调用栈 frame 派生 source(源自 `state-scanner`/`phase-b-developer` 已知生产模块路径,非可传参 boolean)。接入 `.aria/state-checks.yaml` 或等效。**补一条防伪机制自测**(R3-qa-advisory):单测断言"无论如何从 harness 入口调用都不会被误记为生产分区",防实施成"看似结构性、实际留自报参数"的退化版(即 R2-Major-C 本要防的模式换形式复现)
- [x] 3.2 埋点:append-only `.aria/coordination-telemetry.jsonl`(`claim_written` / `collision_surfaced`+latency / `collision_missed` / `false_positive` / `claim_friction`;每条打 **arm 标签 + 结构性来源字段**[非自报]+ 时间戳)
- [x] 3.3 合成双-session dedup harness(R1-M2 + R2-qa-Minor-1):**明确时序模型**(session B 在何时点检查/跳过 gate、相对"已完成多少工作")—— 以便人为构造**至少一种 collision_missed 失败案例**(某臂刻意不在 A 完成前调 gate = 复现 #94 未触发场景),而非只测 trivial 100% 检出;**并定义 collision_missed 的检出侧**(gate 没被调则该记录由谁/何时 emit —— 如 harness 事后对比 ground-truth 是否真有 2 并发 claim 后补写);三 trigger arm(auto/semi/manual)各自如何被 harness 驱动(即便 stub)须给出;量每臂检出率 = surfaced/(surfaced+missed)+ 假阳性 + 摩擦 + 时延
- [x] 3.4 预注册决策规则:跑 AB 前先定阈值(检出≥90% / 假阳性≤5% / **摩擦≤500 token/认领**);**manual arm = P1 交付的 live arm**(runtime 探针断言对象),auto/semi 标 **pending**(AB 定夺后 follow-up 落地某臂)

## 4. 文档同步 + errata + Rule #6 substitute + Dogfood + 发布（P4 — 完整闭环）

- [x] 4.1 母 spec errata(R1-M6):在 `openspec/archive/2026-05-20-multi-terminal-coordination/` **新增 `ERRATA.md`**(不修改归档 `tasks.md`/`proposal.md` 本身),标注 tasks 2.5 + P3 勾 `[x]` 但 `layer-l-integration.md` 自陈 TASK-024 集成 P3 deferred、run_gate scan.py 零调用,现由本 Spec 接续;**说清与 #134 `archive_type`/`design_deferred` 机制的关系**(#134 面向"归档前"gate,本案是"归档后回溯纠错",ERRATA.md 是回溯场景的落点惯例,给 #95 系统修复复用);新 Spec References 双向链接回归档目录
- [x] 4.2 doc-sync 双处(R1-m7 + R2-Minor):(a) **CLAUDE.md** Rule #9 Extension 段 **新增**一句 Layer L 从"P3 未接线/TASK-024 deferred"→"advisory 认领已接活"说明(现状文字未提此缺口,是**新增非替换**);(b) **`aria/skills/state-scanner/references/layer-l-integration.md`**(live 设计文档,aria-plugin 子模块)把 "P3 TASK-024 将把...集成"(未来时)+ ":12 要求 reconcile 后再 claim"(advisory 默认下失真)更新为"TASK-024 已完成 / advisory 接活" —— 否则同一文档家族重演 §Why.2 批判的自相矛盾(#95 自我拆台,Rule #3);#137 enforcement 不涉 frontmatter 变更(本 Spec 不加 frontmatter 字段,grep `==5` 不变),文档化此判定
- [x] 4.3 Rule #6 substitute(structural + runtime-invocation,非 LLM with/without):测 gate 接线真被调 + carry-id 撞检确定性 + advisory surface 正确性 + handoff identity 无漂移;human review 确认真接活(per `feedback_deterministic_structural_skill_rule6_substitute` + `feedback_completion_signals_vs_runtime_invocation`)
- [x] 4.4 Aria 主仓 dogfood(R1-M3):(a) `.aria/config.json` 设 `state_scanner.coordination.enabled: true` + `mode: advisory` 作 dogfood 闭环(使 runtime 探针从第一天有真实调用对象,非一次性验证);(b) 本机制实际承载 ≥1 双子星并发场景,断言 carry-id 认领撞车被检出且 surface(可证伪指标)
- [ ] 4.5 版本发布:aria-plugin minor bump + standards 子模块(§2.3 变更)+ 跨 repo C.2 + Rule #8 pre-merge gate(C.2.4)+ Phase D 归档(plugin.json/marketplace.json/VERSION/CHANGELOG/README + 子模块指针 + 多远程推送);#94 关闭 + #95 部分回应记录

---

## Summary

| Phase | 主题 | Tasks |
|-------|------|-------|
| 1 | 接线(AI 编排层,完成 TASK-024)+ block→advisory | 5 |
| 2 | 结构化 carry-id + handoff 稳定身份 | 5 |
| 3 | runtime 探针 + AB harness | 4 |
| 4 | 文档同步 + errata + Rule #6 + dogfood + 发布 | 5 |

## Dependencies

```
Phase 1 (接线+advisory) ──┐
                          ├──> Phase 3 (探针+AB) ──> Phase 4 (闭环)
Phase 2 (carry-id+身份) ──┘
```

- Phase 1 与 Phase 2 可并行(gate 接线 vs handoff 机制,disjoint 文件集);Phase 3 探针依赖 Phase 1 接线落地;AB harness 依赖 Phase 2 carry-id 存在。
- **"每 Phase 独立价值" = 概念/回滚安全语义**(R1-m3),非 merge 层可独立先发:实际 4.5 打成一次 release train(standards §2.3 先 merge → aria-plugin → 主仓 gitlink),P1 aria-plugin 无 import 级依赖 standards §2.3 文档但随同一 train 发布。语义上:P1 = 接线活了(manual arm 撞检);P2 = carry-id 稳定 key + 身份不漂;P3 = 防再死代码 + 科学选 trigger;P4 = 闭环 + #94 关闭。

## Cross-repo split（per Rule #5 / 母 spec Notes 模式;R1-M4 归属修正）

- `standards`:2.1(session-handoff §2.3 carry-id schema)先 merge,bump 子模块指针
- `aria-plugin`:1.x / **2.2(模板 §6,子模块 track)** / 2.3-2.5(含 **2.4 handoff-write identity,落点全在子模块** phase-d-closer/session-closer/handoff_autofill.py)/ 3.x / **4.2(b) layer-l-integration.md** / 4.3 在 standards 指针更新后 merge
- Aria 主仓:**4.1 errata(`openspec/archive/…` 主仓)** / **4.2(a) CLAUDE.md** / 4.4 dogfood(`.aria/config.json` + 承载)
- 4.5 发布 = 跨 repo fan-out(phase-c-integrator C.2.5 编排)

> R1-M4 修正:`aria/templates/session-handoff.md`(2.2)由 **aria-plugin 子模块 track**(git 实测:主仓 `git ls-files` 不认,子模块认),归 aria-plugin bucket(与 2.3-2.5 同 merge),**非主仓**;原 Cross-repo split 误挂主仓 + task 号 typo(模板是 2.2 非 2.4)已修。

## Audit Plan（per Aria audit-engine）

- **post_spec (A.1)**:convergence mode 5-agent code-grounded。**R1 = 4 REVISE+1 PASS**(2C+6M+11m 全落地);**R2 = 3 PASS+2 REVISE**(R1 全 CLOSED 无 regression;3 新 Major [over-claim / 7b 静默 / 探针防伪] + 7 Minor 全落地);**R3 待稳定性确认**(fresh agents,非 resume,per `feedback_audit_workflow_land_edits_between_rounds`;预期 0 新 Major → unanimous PASS 收敛)
- **post_planning (A.3)**:detailed-tasks.yaml 后触发(per DEC-20260704-001 首个 post_planning gate 已启用)
- **mid_implementation**:Phase 1.3 advisory 改造 + 1.5 golden test 通过后
- **post_implementation**:Phase 3 AB harness + runtime 探针 + 4.3 Rule #6 substitute 通过后

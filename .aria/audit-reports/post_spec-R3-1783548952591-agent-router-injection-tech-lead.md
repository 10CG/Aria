---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-07-08T21:30:26.222Z
context: openspec/changes/agent-router-auto-project-agent-injection/proposal.md
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## R2 closure 核验

对源文件逐条核验（不信 Resolved 表字面），我维度 R2 处置分「真关闭」与「纸面关闭」：

**真关闭（不重复报）**
- **R2 唯一 Critical「差值边界静默改 + 波及纯插件」(1a1d3115/1ba6f643)** — 已真关闭。§2.4 R-b 明文「仅当候选池含项目级 CAP 候选才启用」+「纯插件级候选之间沿用既有 §优先级处理 (差值 < 0.1 严格) 一字不改」(proposal L133,139-141)，与 ROUTING_RULES.md L198「差值 < 0.1 → 降级推荐」逐字对齐；B5 重写一致。Rev1 静默改 <=0.1 确已撤回。
- **rationale 自相矛盾 (ab462321)** — §2.4 rationale (L121) 重写为「数学冲突为唯一硬理由 + 跨刻度=有界务实近似」，自洽。
- **R-a 宽标签劫持 (eabedb99)** — R-a 加 precision >= 0.5 门 (L126) + Impact 登记 (L251) + AC-4 后半 (L273)。

**纸面关闭（本轮升级为 major，见 finding #1）**
- **R2「同名得分归属」(596796f6 簇) + tech-lead 建议新增 AC-12** — 只落了「吸收」定义 (B12 L51-56/L239)，但「吸收后混合候选如何经 §2.4 裁决 / 输出哪条 decision_path」未定文；AC-12「断言裁决路径与 B12 一致」(L281) 不可机械判定。且 R2 Critical 的修法（R-b 收窄到「有 CAP 候选才启用」）恰与 B12（可产出无 CAP 候选的项目级候选）复合出无人区 —— 属 Rev2 fix-introduced 新缺陷。

## 审计结论

**主结论（major）**：Rev2 的两处新机制 —— B12「吸收」与 R2-Critical 修法「R-b 收窄」—— 单独看都对，**复合起来对同名项目级候选制造了未定义裁决**。

B12 令同名幸存候选同时持有：吸收的 baseline confidence（FP 0.95）AND 另算的 CAP 分数。§2.4 R-a/R-b 却只以 `match_rate` 作项目级候选 confidence（L135），吸收值无进入决策的路径。两条可复现分叉：

1. **junk caps 同名候选**（match_rate=0 → §2.3 不产 CAP 候选）：R-b『仅当含项目级 CAP 候选才启用』不启用；同时该候选 `agent_source=project`，『纯插件…无项目级候选参与』(L139-141) 亦不适用 → **无任何 §2.4 子句裁决它**，decision_path 只能靠 enum 消去法猜。
2. **部分命中同名候选**（0<match_rate<1）：既是吸收 0.95 的 baseline top，又是 match_rate 0.67 的『项目级 CAP 候选』→ R-b『项目级 CAP 候选与基线 top 比较』变**自比较**；且 0.67 领先弱基线 >0.1 但 <threshold，落入 R-b 三子条件覆盖缺口。

两名实现者按同一 fixture 会分叉：一个用 match_rate 0.67 → recommend（吸收 0.95 被忽略，B12 的『防高分静默蒸发』反被架空）；一个用吸收 0.95 → auto 直派。**相反 status + 相反 decision_path → AC-12 无法双跑一致**。

不推翻设计：修法 = §2.4/B12 补一段消歧（同名吸收候选 auto 分支的 governing confidence = 吸收值，CAP 仅供 trace/排序；decision_path 定死 baseline+project=『同名接管』），并给 AC-12 补 fixture caps 与期望值。因不破 #153 黄金场景（AC-1/AC-5 用异名 database-specialist，不触发 B12）且不破零回归三支（B12 仅在 scan on + 同名时触发），故为 **major 非 critical**。

**其余 advisory（可折入实施注意事项，不阻塞收敛）**：B12 同名静默 auto 接管未登记 Risk（角色 brief 明问）；§4 TTL 缺 last_full_scan 时间戳字段 → 不可执行；§2.1 negation 与 L2 启用求值顺序未定；AC 总注 task_type『或』分支单独不可达 |L1|>=2；decision_path 在 recommend 的基数未定；tasks TASK-013/014 对 AC-3 重复覆盖；§5「SOT」措辞与 max_candidates 仍居 legacy config 的分裂易误读。

**全局自洽核验（通过）**：B1-B12=12 决策、AC-1..AC-12=12、TASK-001..017=17（TG-A..E=5）计数一致；连带段落 §6 九段与 TASK-007（§145 + 8 段）并集完整覆盖；SKILL L17/L449 与 ROUTING_RULES L3 版本漂移锚点、目标版本 v1.1.0→v1.2.0 / plugin v1.53.0→v1.54.0 与 source_sha 一致；tasks 顺序（TG-A→B→C∥D 前半→D 实跑→E）可执行、主仓文件随 Phase C 落地划分正确；M7 L129「不改 agent-router / v1.1.0 pin」与本 change「additive 输出 + re-baseline」无实质冲突（本 change 使 M7 描述的注入在 auto 成真，非其前置）。

## Verdict

**PASS_WITH_WARNINGS**（0 Critical + 1 Major + 7 minor-advisory），vote = **REVISE**。

单条 major 是 Rev2 fix-introduced 的机制复合缺陷（B12 × R-b 收窄），修复代价小（一段消歧 + AC-12 补值）但当前不可机械判定，须 Rev3 落文后再判收敛。其余 7 条为 advisory，随实施酌处即可，不单独阻塞。

## 核验锚点

- proposal.md:51-56 — B12 同名吸收定文（双 confidence 来源）
- proposal.md:116 — §2.3 match_rate==0 不产 CAP 候选（junk caps 分叉根）
- proposal.md:133-144 — §2.4 R-b CAP-gate + 纯插件『无项目级候选参与』边界（无人区根）
- proposal.md:159-162 — §2.6 per-candidate decision_path + max_candidates §286 legacy
- proposal.md:170-171 — §3 decision_path enum（无 recommend 值）
- proposal.md:190-197 — §4 TTL 语义 + per-file schema（缺 last_full_scan）
- proposal.md:89-98 — §2.1 negation × L2 启用顺序
- proposal.md:250-254 — Impact 表（无 B12 Risk 行）
- proposal.md:268 / 271 / 281 — AC 总注 task_type『或』/ AC-2(b) 单值 / AC-12 不可判定
- tasks.md:29-30 — TASK-013/014 AC-3 重复
- ROUTING_RULES.md:198 — 纯插件 <0.1 严格（R2 Critical 真关闭锚）
- SKILL.md:281-289 — legacy config max_candidates/threshold（§5 SOT 分裂）
---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-07-08T21:48:19.655Z
context: openspec/changes/agent-router-auto-project-agent-injection/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R3 审计报告 — agent-router-auto-project-agent-injection Rev2 + tasks.md (code-reviewer)

## R2 closure 核验

我维度 R2 findings (5 Major R2-CR-1..5 + 7 Minor R2-CR-6..12) 逐条对源文件核验, **12/12 实质关闭, 无纸面关闭**:

| R2 finding | Rev2 处置 | 核验结论 |
|---|---|---|
| CR-1 L1/L2 复合未定义 (簇 cf4aa23e/ad935a3a) | §2.1 编排算法: 并集−negated + **仅当 \|L1\|<2 启用 L2** + 上界 3 | **真关闭** — AC-1 的 pin 分母被 \|L1\|≥2→L2 关闭封死; 但该机制结构上不覆盖 AC-2(b) 的 \|req\|=1 (新报 F1) |
| CR-2 AC-2(b) 无区分力 + 路径无载体 (91c8e97b/4a3f5098 + b4aeb123/d4ea6516) | AC-2(b) 基线参数 0.90→**0.85** + §3 新增 **decision_path** | **真关闭** — 数学复算: 差 0.15>0.1 且 1.0≥0.9, 无禁令则 R-b 直派/有禁令则 recommend, 参数可区分; 粗粒度 R-a\|R-b\|baseline 配合参数足以归因 |
| CR-3 差值边界 ≤0.1 翻转波及纯插件 (R2 唯一 Critical 簇 1a1d3115/1ba6f643) | §2.4 R-b「仅候选池含项目级 CAP 候选才启用」+「纯插件级之间沿用既有 <0.1 **一字不动**」+ §1 step5 同步 + B5 重写 | **真关闭** — ROUTING_RULES.md:198 原文「差值 < 0.1」复核吻合; 3e 关闭三支回到既有规则, AC-3 结构性失败面消除, 零回归恢复真实成立 |
| CR-4 插件级 capabilities 裁决缺失 (c0e74580) | B11 显式裁决 (仅项目级) + OOS 条目 + §6 对 §393 L404 措辞修正 | **真关闭** — 源 SKILL.md:402-403「合并…(FP/TT/关键词 + capabilities)」引文核实准确, 实施分歧点消除 |
| CR-5 同名替换得分归属 (沿 R1 450102ae, 簇 596796f6 等四方) | B12 **吸收**定案 + §1 3e 定文 + AC-12 | **真关闭** (高分蒸发回归堵死); 残余: 吸收候选在 R-b 的侧别归属未明 → 降级为本轮 minor F8 |
| CR-6 D9 引用失准 (簇 bac15556 等) | §1 改述「§416 实现语义保留」+ D9 弱化系 v1.13.0 既状记录于 R2 表 | **真关闭** — SKILL.md:419-421 源核实 |
| CR-7 Rule #6 张力 (25220fa6) | 后续段适格性论证补齐 (可复跑+可机械判定) | **真关闭**; 其 blanket「L2…隔离在断言路径之外」claim 有 AC-2(b) 反例 → 并入 F1 |
| CR-8 Resolved 表 id (814e68de/a1fd3131/f3d5f9b9) | 1d35911a-a/-b 后缀 + 尾注 | **实质关闭** — R1 表 39 id、R2 表 49 id 逐一复点均成立, -a/-b 落实; 但尾注对 f2a4ac9a 修复落点描述 stale + §3 标题新 7 位 id e16ad9f 同类新例 → 新报 F5 |
| CR-9 TTL 悬空 + 旧 schema (簇 97cb686e 等) | §4 TTL 重定义 (更严方向, 默认 0 未 flip) + Impact「旧缓存直接重建」 | **真关闭** |
| CR-10 match_rate=0 入池 (b304c182) | §2.3 明文「不产出候选」+ §1 3e 同步 | **真关闭** |
| CR-11 task_type 机械边界 (f3677340/87ff93a7) | §2.1 显式传参前提 + 撤回「L1 为主干」 | **真关闭** |
| CR-12 维护指南五类 (9681f9b2/8cb5b4cd) | §6 五类枚举 | **真关闭** — 源 ROUTING_RULES.md:255 漏「技术栈」核实属实 |

**角色侧重的 Rev2 新引用逐行核验 — 全部通过**:
- DEC-20260621-001 文件存在, 含同源表述: L13「agent-router v1.1.0 **已实现**所需机制——扫描 .aria/agents/*.md」+ L90「triage 已确认那条路正常 (项目 agent 在任务路由已被感知)」。注意: DEC 无 verbatim「会扫」, 该 verbatim 在 archive proposal L16 (「**会**扫」粗体拆分, grep 连串不中但引用忠实) → §6 引语归因措辞报 F6
- US-011 三锚点真实: AC-4 (L51「agent-router 运行时注入…首次缓存」) / D4 (L43「agent-router 需动态感知项目级 Agent」) / Scope (L61「修改: agent-router (运行时注入 + 缓存 + 同名保护)」)
- M7 agent-lifecycle proposal L129 引语「本 Spec **不**依赖任何未实现的 routing 能力, 也**不**改 agent-router」+ v1.1.0 pin — 行号与措辞精确
- SKILL.md §416 同名保护 (L416 标题, L419 警告文「覆盖了插件级路由」) / config 3 key L429-431 (名称+默认值 true/false/0 + 旧注释「0 = 仅 mtime 失效」引文全对) / §35/§47/§93/§145/§205/§221/§232/§250/§286/§305/§323/§383/§393/§438 全部对上; §277 引用的「项目级配置」标题实际在 L279 (§277 为上级「## 配置」, 2 行内偏差不碍定位)
- ROUTING_RULES §优先级处理 L198「差值 < 0.1」严格边界原文核实; L3 版本 1.0.0 核实
- handoff-contract.md:14,33 agent_source 预留字段行号精确; config.template.json 确无 agent_router 块; taxonomy 头注确只列 agent-gap-analyzer
- **双 Resolved 表内部一致性**: R1 表 19 行 id 计数 = 39 (含 -a/-b) ✓; R2 表 26 行 id 计数 = 49 ✓; 74dce1fc → AC-9 已真实改引「What §5+§6」✓; AC-9 枚举与 §5+§6 全清单逐项对得上 (连带 9 段 = §145+8 段, 与 TASK-007 口径算术一致)

## 审计结论

Rev2 8 项新机制经边界组合推演, **无 critical/major 级新缺陷**。R2 Critical (差值边界) 的修复方式 (范围收窄而非全局改边界) 是正确解法且未引入新回归面; B12 吸收、precision 门、L1/L2 编排、输出收窄、缓存完整化在主场景全部自洽。以下 11 条 minor 为 advisory, 可折入实施注意事项:

1. **[F1 testing] AC-2(b) 的 \|req\|=1 无机械 pin 通道** — pin 机制 (L1≥2→L2 关) 结构上产不出 \|req\|=1; \|L1\|=1 时 L2 必启用可加料, 双跑一致有风险。AC 总注与后续段两处 blanket「全机械 pin/隔离」表述被 AC-2(b) 自身反例。连带: task_type 单值参数最多贡献 1 个 L1 命中, 总注「或」读法误导。修法: AC-2(b) 加例外注记 (极简任务文本 + trace 前置校验 l1 恰 1/l2 空), blanket 表述限定例外。
2. **[F2 testing] TASK-015 排序矛盾** — AC-9 清单含发版产物但 TASK-015 在 TG-E 前, 按文序必挂。移后或拆段。
3. **[F3 documentation] TASK-017 缺 submodule pointer bump** — AC-9「主仓 3 项」vs TASK-017 仅 2 项。
4. **[F4 documentation] TASK-013「AC-1..AC-8」与 TASK-014 (AC-3) 双认领** — archive gate 勾选语义歧义。
5. **[F5 documentation] id 卫生**: §3 标题 (L164) 7 位「e16ad9f」(他处 e16ad9fc); R1 表尾注声称「§6 正文引用统一 8 位 id f2a4ac9a」但 §6 正文已无该引用 (stale)。
6. **[F6 documentation] §6 DEC 勘误引语归因** — 「router 会扫」非 DEC 原文 (DEC 为 L13/L90 同源表述; verbatim 在 archive proposal L16); Why 段口径准确, §6 与之不一致。
7. **[F7 architecture] off-taxonomy 标签计入 precision 分母未显式声明** — identity 保留→分母稀释可把全命中 specialist 挡在 R-a 外 (2 命中+3 off-taxonomy → 2/5=0.4<0.5); 行为可确定推导且方向自洽, 但交互未记录, 而 off-taxonomy 项目专属标签有现实先例 (DEC 的 shell-safety/ssh-egress)。
8. **[F8 architecture] B12 吸收候选的 R-b 侧别归属未明** — 吸收 0.95 的项目级候选按得分类别归基线侧还是按 agent_source 归项目侧, 多候选池两种读法裁决可不同; 「纯插件级候选之间」措辞在含吸收候选池中留白。建议一句话: 吸收分按基线得分类别参与, agent_source 仅为元数据。
9. **[F9 documentation] negation 随 L2 门控隐式关闭** — \|L1\|≥2 时 negated 恒空未标注。
10. **[F10 documentation] Impact 宽标签行「precision≥0.5 门拦截」略过强** — 门仅锁 R-a; R-b 对宽标签 1.0 候选领先弱基线 >0.1 且 ≥threshold 时仍直派 (有界残余)。
11. **[F11 architecture] 项目级互相 close-but-unequal (0<差≤0.1) 无护栏** — 理论完备性注记: 量化 k/\|req\| 使该窗口需 \|req\|≥10 才可达 (L2 路径上界 4), 现实几乎不可达, 可实施酌处。

**tasks.md 对齐性**: 17 task 对 What §1-§6 全部工作项覆盖核对完成 — §1→TASK-005; §2→TASK-001..004; §3→TASK-007; §4→TASK-005/006/007 分摊 (3e 主链/缓存子段/§383 退化行); §5→TASK-006/009; §6→TASK-006..011/016/017; AC→TASK-012..015。无 What 内容完全无 task 承接; 缺口仅上列 F2/F3/F4 级别 (另: fixture 清单未显式命名 AC-10 双 R-a 候选场景, 可并入 proj-a, 随 F4 一并酌处)。

## Verdict

**PASS** (0 Critical + 0 Major + 11 Minor advisory) → **vote: PASS**

Rev2 在我维度已收敛: R2 全部 5 Major (含 Critical 簇的护栏范围收窄) 均实质落文且修复方式正确, 双 Resolved 表 88 条 id 计数复点成立, 新引用行号/引语精度显著优于前两轮 (仅 2 处 id/引语级瑕疵)。剩余 11 条全部是措辞精度、tasks.md 排序/清单对齐、以及两处「行为已确定但交互未记录」的边界组合注记 — 均可随实施酌处, 不阻塞进 A.2。

## 核验锚点

- openspec/changes/agent-router-auto-project-agent-injection/proposal.md:1-355 (Rev2 全文; 重点 §1 L36-76 / §2 L82-162 / §3 L164-179 / §4 L181-197 / §5 L199-204 / §6 L206-222 / B1-B12 L226-239 / AC L266-281 / 双 Resolved 表 L283-338 / 后续 L351-355)
- openspec/changes/agent-router-auto-project-agent-injection/tasks.md:1-41 (17 task + 执行顺序)
- aria/skills/agent-router/SKILL.md:17, 35, 47-54, 93, 137, 145, 205, 221-225, 232-235, 250, 277-289 (286 max_candidates), 305, 323, 383, 393-434 (397 机制句 / 399-406 流程 / 402-403 L404 引文 / 408 D4 note / 416-421 同名保护 / 429-431 config 3 key), 438, 449
- aria/skills/agent-router/ROUTING_RULES.md:3, 185 (上限 1.0), 192-201 (198 差值 < 0.1), 251-259 (255 三类枚举)
- aria/references/capabilities-taxonomy.yaml:1-4 (头注), 20/136-139 (#153 三 caps 均在词表)
- .aria/decisions/DEC-20260621-001-agent-team-audit-project-agent-augmentation.md:9, 13, 90
- docs/requirements/user-stories/US-011.md:43 (D4), 51 (AC-4), 59-61 (Scope)
- openspec/archive/2026-06-21-agent-team-audit-project-agent-augmentation/proposal.md:16 (verbatim「**会**扫」)
- openspec/changes/aria-2.0-m7-agent-lifecycle/proposal.md:129
- aria/skills/subagent-driver/references/handoff-contract.md:14, 33
- .aria/config.template.json:1-72 (确无 agent_router 块)
- .aria/audit-reports/post_spec-R2-1783545343184-agent-router-injection-code-reviewer.md (R2-CR-1..12 closure 基线)
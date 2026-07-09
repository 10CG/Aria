---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-07-08T22:28:59.166Z
context: openspec/changes/agent-router-auto-project-agent-injection/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## R3 closure 核验

独立对源文件重新推导(不信 Resolved 表)，逐项复核 Rev3 对 R3 12 Major 的核心处置:

1. **R-b 四分支 MECE 化**(146fa0b3/2bf3e6d6, L141-148)：设 d = 挑战者 match_rate − baseline_top confidence。四分支覆盖 d>0.1(细分两支)/|d|<=0.1/d<−0.1("baseline_top 领先")，在实数轴上无缝隙无重叠——独立验证 MECE 确实成立，R3 修复有效。

2. **negation 脱离 L2 连坐**(b59e5149, L93-98)：确认 L2-negation 段落明确标注"恒时执行，不受下方启用条件门控"，与 L2-addition 的净值门控 (e) 条款物理分离——独立验证脱钩到位。

3. **precision 分母=valid_caps 定案除零复核**(9ab6adf4, L108-118)：独立数学重新推导（非信任声明）：因 matched⊆valid_caps，`match_rate=|matched|/|required_caps|>0` 蕴含 `|matched|>=1` 蕴含 `|valid_caps|>=1`；而候选产出的前置门控恰是 `match_rate>0`（L58/L118）。故 precision 被计算/输出时分母恒不为零——**结构性安全，非仅声明**，R3 定案确认成立，且数学上不可达除零路径。

4. **§4 last_full_scan/TTL/旧 schema 重建**(8660ec54, L200-214)：字段完整、TTL 强制重建语义（"即使 stat 一致也重建"）与主判（stat 差异触发）先后关系清晰、旧 schema 直接失效重建路径简单可执行。agent-router 是 prose Skill + Bash 工具（无 Python），stat 采集/JSON 读写/原子写均可经 Bash 完成——可执行性确认。

5. **B12 混合候选消歧**(79070f61/ff4315de/95d37650/4b94a576, L150-157)：**部分关闭**。"每候选恒有唯一归属"的一般性无人区问题已解决；但独立复核 Stage 2 挑战者选择步骤与 B12 自我挑战排除条款的术语对齐后，发现一个 R3 未覆盖、当前 fixture 计划也未触达的复合子情形残留——见下 Finding 1（本轮新增，非重报，且正是本角色 brief 明确要求核查的"B12 吸收候选同时是 baseline_top 且被 CAP 挑战者挑战时的自洽"）。

## 审计结论

Rev3 在四个复核维度（R-b MECE、negation 脱钩、precision 除零、缓存可执行性）上都做到了**结构性**而非仅声明层面的正确——这是本轮独立重新推导后的结论，不是照抄 Resolved 表。B12 消歧总体方向正确，一般性"无人区"问题已彻底解决，但在"吸收候选自身 CAP 分是否可被选为 Stage 2 挑战者"这一具体复合场景上，操作性文本（L136 挑战者选择行）与排除条款（L150-153 B12 段）之间存在术语衔接缺口：前者用未限定的"CAP 候选"，后者才补充说明该分录"不作为 auto 挑战分数"，两者之间缺一处显式交叉引用或限定词重复。构造性反例显示：当同名吸收候选自身capabilities 恰好也满足 R-a 全部条件时，decision_path 会依实现读法在 'R-a' 与 'baseline' 之间分叉——这正是 AC 总注"双跑不一致处置=判 fail 并回炉"机制设计要拦截的那类分歧，但当前 AC-12 fixture 刻意选择 match_rate=0.5 回避了此组合（"无 R-a"注记见 L298），故该场景现仍未被任何 AC 覆盖。

其余三项（显式 required_caps 的 off-taxonomy 处理未定义 / last_full_scan 格式双选未定案 / AC-15 fixture 依赖未显式声明）均为 Minor/advisory，不阻断，但建议顺手处理，避免遗留到实施阶段被动发现。

## Verdict

**PASS_WITH_WARNINGS**（0 Critical + 1 Major + 3 Minor）

**vote: REVISE** — 存在真实 Major（非措辞级 advisory），按终轮判据如实上报，不因终轮放水，也不为凑数强报。修复成本低（预计一行文本 + 一个交叉引用，可在 TASK-003 执笔时一并落笔），不构成结构性重做，不影响 Rev3 已收敛的其余部分。

## 核验锚点

- proposal.md L61-64（step 4 置信度聚合：B12 候选 CAP 分归"项目侧"/属于"CAP 候选"池的成员资格声明——与"纯"限定词的排除意图存在张力的源头）
- proposal.md L71（§1 伪代码摘要："Stage 2 项目级 CAP 挑战 (仅当存在纯 CAP 项目级候选)"——"纯"限定词的另一处引用，佐证其应贯穿整个 Stage 2）
- proposal.md L135-136（§2.4 Stage 2 触发前提用"纯 CAP 项目级候选"，但下一行"挑战者 = CAP 候选中 match_rate 最高者"未重复"纯"限定词——核心缺口所在）
- proposal.md L150-153（B12 消歧段："其自身 CAP match_rate 仅用于 trace 与 recommend 排序, 不作为 auto 挑战分数 (防同一候选自我挑战)"——排除条款存在，但未内联到 L136 挑战者选择定义处，也无交叉引用）
- proposal.md L298（AC-12 fixture 显式选 match_rate=0.5"无 R-a"，回避了本 finding 所指的复合场景，佐证该场景当前未被测试覆盖）
- proposal.md L82-87（§2.1 显式传参段，未说明 off-taxonomy/拼写错误标签在显式输入路径下如何处理）
- proposal.md L106-109（§2.2 归一语义，off-taxonomy 讨论仅覆盖 agent capabilities 侧，未覆盖 required_caps 输入侧）
- proposal.md L203-204（§4 缓存 schema，`last_full_scan: <epoch/ISO UTC>` 双格式未定案）
- proposal.md L197, L301（§3 输出契约门控 vs AC-15 推断层专项：required_caps_trace 字段需 `.aria/agents/` 非空才输出，但 AC-15 本身不需要任何项目级候选参与匹配语义）
- tasks.md L28, L31（TASK-012 fixture 清单 / TASK-015 AC-15 专项，未显式提及为 AC-15 复用一个非空 `.aria/agents/` fixture）
- 环境核验：主仓 SHA 2067ddf（实测匹配 anchor 声明）、aria 子模块 SHA 93b7406（实测匹配 anchor 声明），source_sha 锚点核对通过；taxonomy 标签 api-design/database-schema/orm-migration 均在 capabilities-taxonomy.yaml 中确认存在，AC-1/AC-12 引用的标签有效。
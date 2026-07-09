---
checkpoint: post_planning
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-07-09T02:47:56.903Z
context: openspec/changes/agent-router-auto-project-agent-injection/detailed-tasks.yaml
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## R2 closure 核验

对 PP-R2 (10 findings: 0C+2M+8m) 到 plan Rev3「修复全部 10 条」的声称，本轮完整核验代表 6 组修复对源文件 (tasks.md + detailed-tasks.yaml，逐字段/逐条目核对，并回查 proposal.md 作技术依据佐证)：

| 编号 | 严重度 | 内容 | 落地状态 |
|------|--------|------|----------|
| 1 | M | tasks.md TASK-012 补「单标签 specialist」+ 9 类同构 + 双 runner/隔离副本 | 确认落地 |
| 2 | M | 重跑全批范围显式 (= TASK-013+014+015 全体) + TASK-014 挂钩句 | 确认落地 |
| 3 | m×3 三方 | TASK-012 deps=[TASK-008, TASK-004] (RULES 终笔编辑闭包) | 确认落地, 三方(deps 字段/execution_order/tasks.md 执行顺序)一致 |
| 4 | m | scratchpad 副本表述 →「git show 为 SOT; session 副本仅当次缓存」 | 确认落地, 原字对照 |
| 5 | m | TASK-005 行款目与 yaml/proposal 六款同构; 执行顺序行 ∥→, 记号 | **未确认落地** |
| 6 | m | TASK-003 verification 补 R-a 覆盖面刻画 + max_candidates 注 (共 10 项) | 确认落地, 程序计数=10 |

详细证据见 `r2_closure_check` 字段。核心方法：对可枚举的条目 (fixture 类别数/verification 条目数) 用脚本切分计数，不靠肉眼数数；对措辞类修复做原字比对；对依赖类修复做三方交叉 (tasks.md 执行顺序 / yaml dependencies / yaml execution_order)。

## 审计结论

5/6 组代表性修复扎实落地，且都能在 proposal.md 找到对应技术原文——不是「文件之间抄来抄去」，是真的对得上业务规则。

fix 5 是本轮唯一的缺口，判定为 **未落地** 而非「已按不同方式落地」，理由：

1. **条目集合真不同，不是措辞差异**。tasks.md L15 的 3e 括注切出来是 5 项 (门控最先/健壮性/同名B12/缓存/评分)；yaml L77 明文「3e 六款」列出 6 项 (门控最先/健壮性/同名B12含吸收+警告/归一/评分/零分不入池)。tasks.md 这份缺「归一」「零分不入池」两条真实验收规则，却多出一条不在六款之列的「缓存」。这两条不是无关紧要的措辞——「归一」对应 proposal §205 3e 第 5 子步骤 (capabilities 经 taxonomy 归一)，「零分不入池」对应第 6 子步骤的产出条件 (match_rate>0 才产出候选)，都是 §CAP 评分链路里会实际跑测试断言的行为点。如果开发/验证时只照 tasks.md 这行走，这两条行为会被漏验。
2. **记号也是反的**。tasks.md L41 执行顺序行「TG-C ∥ TG-D(TASK-012)」两侧全是 main-loop 任务，和 yaml metadata 自己写的记号约定「∥ 仅表 subagent 真并行窗」矛盾；而真正该用 ∥ 的 TASK-013/014/015 (subagent 真并行) 反而在同一行用了没有定义过的「/」。yaml 自己的 execution_order 字段 (L222) 是用对的 (「013∥014∥015 subagent 真并行」)，只有 tasks.md 这行反了。
3. **佐证是"漏改"而非"另一种改法"**：fix 2/3/4/6 在 yaml 里全部留了「PP-R2 <8位hash>」溯源注，唯独 TASK-005 行和执行顺序行两处，全文搜「PP-R2」零命中。四条有痕迹、一条没有，指向 fix 5 在 Rev3 编辑轮次里被跳过，不是刻意选了别的写法。

**快扫 (fix-introduced 新问题)**：结构层面做了任务 ID 唯一性 / 依赖图可解析 / total_tasks 计数三项脚本核验，均干净 (18 个任务、零重复、零悬空依赖)。baseline_sha 93b7406 在 aria 子模块 git 历史中真实存在且含 SKILL.md/ROUTING_RULES.md 当时版本 (header 1.0.0/footer 1.1.0，与 proposal.md Why 段描述的版本漂移 bug 吻合)；L17/L449/L3 三处行号引用逐一核对，与当前 aria/skills/agent-router/ 源文件行内容精确对应，无引用漂移。TASK-013 覆盖 AC 集合 (AC-1,2,4-8,10-14,16) 与 TASK-014 (AC-3) + TASK-015 (AC-15) + TASK-017/018 (AC-9a/9b) 拼起来恰好是 proposal 全部 16 条 AC，无遗漏无重复。

**非阻塞观察 (未列入 findings，无下游机械消费方)**：yaml metadata.plan_rev 字段 (L7) 仍是「Rev2 # post_planning R1 (0C+15M+16m) 全吸收」，本轮的框架前提是把当前文件当「plan Rev3」(已吸收 PP-R2 10 条)，这个自描述字段没跟着 bump。在 aria/ 与 standards/ 全文搜索未发现任何脚本/skill 读取 plan_rev 字段 (与 spec_rev 不同，spec_rev 在 proposal.md/tasks.md/yaml 三处一致显示 Rev4)，纯自描述漂移，建议顺手在修 fix 5 时一并把这行改成「Rev3 # post_planning R2 (0C+2M+8m) 全吸收」，但不构成本轮阻塞项。

## Verdict

**PASS_WITH_WARNINGS**，vote = **REVISE**。

理由：0 Critical，1 Major (fix 5 两处未落地)，其余 5 组修复扎实且有据可查，问题范围窄、修复动作是两行文本编辑 (不涉及依赖图/deliverables/verification 字段变更)，不需要打回重新做 A.2 全量规划。建议路径：owner 或 main-loop 直接按 findings 里的 suggested_fix 把 tasks.md L15/L41 改掉，改完不必再开一轮 5-agent 全量 R4，本 agent 做一次轻量复核 (核对两行文本) 即可收敛，随后可以进 Phase B。

若 owner 判断这两行的信息缺口可以留到 Phase B 实施时再由 yaml (权威细节层) 兜底——tasks.md 只是精简导航层——也是合理的风险接受路径，但那样应该在 proposal.md 或本报告旁明确记一句「已知接受」，而不是让 tasks.md 继续挂着一个「声称已修复但未修复」的状态。

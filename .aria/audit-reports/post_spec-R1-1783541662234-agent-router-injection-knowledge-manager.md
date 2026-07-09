---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-07-08T20:10:03.838Z
context: openspec/changes/agent-router-auto-project-agent-injection/proposal.md
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 审计结论

角色定位: knowledge-manager, 本轮聚焦 Rule #3 (文档与代码同步) 完备性。已逐字核对 proposal.md 全文、agent-router 的 SKILL.md(449 行全文)+ ROUTING_RULES.md(270 行全文)+ capabilities-taxonomy.yaml, 并追溯三份上游/下游关联文档(agent-project-adapter / agent-team-audit-project-agent-augmentation / aria-2.0-m7-agent-lifecycle)及 subagent-driver 的 SKILL.md + handoff-contract.md、US-011.md、.aria/config.json 等 code-grounded 交叉验证。

**核心判断**: proposal 对根因的诊断(§393 孤儿段从未接进 §205 主链、§232 短路、无成文 CAP 评分规则)三处 line-level 引用全部精确核实无误(§205/§232/§393 均命中实际标题/代码行);Decision Records 的技术选择(B1-B7, 尤其 B3/B4 复用 gap-analyzer `match_rate = matched/required` 语义)与既有跨 Skill 惯例完全一致, 是一份 grounding 扎实的方案。**但"文档同步"这一维度(proposal §3 + AC-6)覆盖的范围明显小于实际需要同步的范围** —— 下述 8 条 major 均属于"proposal 目前的文档同步计划遗漏, 但按 Rule #3 应处理"的缺口, 无一动摇方案本体设计, 故未评 critical。

### Major 发现 (按证据强度排序)

1. **`agent_source` 字段无从被正确赋值** (`subagent-driver/references/handoff-contract.md:14/33`): 该字段自 2026-04-11(早于 `.aria/agents/` 机制本身)就预留 `"project"` 枚举值, 但 agent-router 自身输出 schema(§145)从无 provenance 字段, subagent-driver 路由集成示例(L710-764)也从不提及此字段。本提案是第一个真正让 "project" 值有资格被选中的变更, 却未接线赋值来源, 也无 AC 验证。OOS 条款"不改 subagent-driver 契约"字面成立但掩盖了这一层。
2. **US-011.md (已标记 "done") 的 AC-4/D4/Scope 仍宣称运行时注入已兑现**, 现被 #153 证伪, proposal 未安排回溯订正 —— 与刚 ship 的 archive-gate-runtime-reality(#95, "生产零语义引用"模式)高度同构, 项目已有 ERRATA.md 处理先例(CHANGELOG [1.52.0])可循。
3. **版本号实际位置与 proposal §3 描述不符**: SKILL.md 除 frontmatter(无 version 字段)外还有正文头 L17 "1.0.0"(既存漂移, 从未随 v1.1.0 更新)独立于 footer L449 "1.1.0"; ROUTING_RULES.md 版本号只在 header L3, footer L270 只有日期无版本号。proposal 的"frontmatter/footer"及"footer 版本"措辞均不准确, 且遗漏 SKILL.md L17。
4. **step 3d "强制" 与既有 `.aria/config.json agent_router.scan_project_agents/plugin_only` 开关关系未澄清**, 且与另一套 `.claude/agent-router-config.json`(§277)配置面并存, proposal 对 §393 的"保留清单"未列配置开关, 无 AC 覆盖关闭态。
5. **recommend 模式(subagent-driver 默认调用模式)同样应受益于修复**, 但 6 条 AC 全部用"auto"措辞框定, 结构上 step 3d 在 step 5 模式分支之前(对 auto/recommend 都生效), 却无一条 AC 验证 recommend 模式候选池现在包含项目级 Agent。
6. **§438「相关文档」从未链接 ROUTING_RULES.md**, §93「路由规则」也未随新增 §CAP 补呼应小节 —— 新引入的跨文件内联引用("ROUTING_RULES §CAP")使既存割裂更突出。
7. **§323 使用示例 / §35 核心功能表 / §305 Agent 能力矩阵 三处汇总性段落未纳入新机制**, proposal §3 文档同步清单未列; #153 场景本可直接作为第 4 个示例。
8. **§383 错误处理表未纳入 step 3d 的新退化路径**(`required_caps` 为空 → 退化基线), 该规则目前只活在 proposal 正文。

### Minor 发现

9. ROUTING_RULES.md「维护指南 → 添加新规则」枚举未同步为四类(FP/TT/关键词/CAP)。
10. proposal 把 M7 与 audit-augmentation 并列称"两处 Spec 都假设 agent-router 好用, 本 change 修好后才真正兑现二者依赖的前提" —— 核实 M7 全文把 agent-router 列为纯 black-box 且自身交付流程不调用它, "依赖"措辞对 M7 略夸大(对 audit-augmentation 成立)。

### 未采纳为独立 finding 的核实项(供其他 lens 参考)

- `.aria/agents/` 在本仓库确认不存在(`ls` 验证), 与 AC 段"本 Aria 项目无 .aria/agents/ 目录"一致, 与 audit-augmentation AC-5 验证模式的类比准确。
- CAP 评分公式 `match_rate = matched/required_caps` 与 M7 proposal Constraints 段 (`match_rate = matched_tags/required_tags, covered ≥0.5`) 及 agent-project-adapter D7 精确一致, 复用主张成立, 无虚构。
- `agent-project-adapter` D4 grounding 引用准确; `agent-team-audit-project-agent-augmentation` L16 引文逐字核实准确; M7 proposal §28-29 + B.2 的"已认领"表述准确。
- "版本 5 文件同步" 精确对应 CLAUDE.md「派生文件(必须同步)」5 条清单(marketplace.json/hooks.json/VERSION/CHANGELOG.md/README.md), 计数无误, 未列入 finding。
- agent-creator/SKILL.md、agent-gap-analyzer 相关引用未发现需要同步的过时声称。

## Verdict

**PASS_WITH_WARNINGS**(0 critical / 8 major / 2 minor)。方案本体(根因诊断、修复位置、CAP 评分算法设计、零回归策略)code-grounded 扎实, 未发现自相矛盾或不可实施之处, 故非 FAIL。但"文档同步"维度存在 8 项实质缺漏(尤其 finding 1/2 触及跨文件数据契约与历史需求文档的准确性), 按本检查点 severity 规则(>=1 major 必须 REVISE)判 **vote = REVISE** —— 建议在进入 A.2 前, proposal §3 与 AC-6 至少吸收 finding 1-8 的可执行部分(重点: agent_source 接线、US-011 订正安排、recommend 模式 AC、§438/§93/§383/§35/§305/§323 补录), 使"版本 5 文件同步"实际覆盖到位。

## 核验锚点

见 `code_anchors` 字段, 涵盖: proposal.md 全文、agent-router SKILL.md 全文(449 行, 逐段核对 §35/§47/§93/§132/§145/§205/§221-244/§250/§277/§305/§323/§383/§393/§438/§449)、ROUTING_RULES.md 全文(270 行)、capabilities-taxonomy.yaml、aria/CHANGELOG.md 头部 60 行、agent-creator/SKILL.md 全文、subagent-driver/SKILL.md 关键段(L600-770)、subagent-driver/references/handoff-contract.md 全文、US-011.md 全文、US-010.md 抽查、三份上游 OpenSpec(agent-project-adapter/agent-team-audit-project-agent-augmentation/aria-2.0-m7-agent-lifecycle)全文、.aria/config.json 全文、CLAUDE.md 版本发布检查清单段。

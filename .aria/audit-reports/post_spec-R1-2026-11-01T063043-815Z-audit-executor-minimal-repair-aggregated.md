---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: false
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-11-01T06:30:43.815515+00:00
context: audit-executor-minimal-repair
agents: [aria:tech-lead, aria:backend-architect, aria:qa-engineer, aria:code-reviewer, aria:knowledge-manager]
---

# 执行器最小修复 — post_spec R1

质量verdict=PASS_WITH_WARNINGS；converged=false；配置5席，实际派发5席，准入2席。

- Sibling probe: 入口已执行；首轮完整扫描未发现同issue竞品，后续轮结果见对应入口记录。
- Drift checker: convergence opt-in未启用，不派发；原始目的anchor保持固定。
- 新守卫未实现/未激活，当前审查使用既有算法；此报告不解除PR #38暂停。

## Conclusions

### 4e12674e [major] execution_state各行条件存在交叉且缺少优先级，无法唯一确定迟到空结果、截止后完成及恰在整轮截止完成的分类。
- scope: `execution_state/classification_precedence`
- source: `/home/dev/Aria/openspec/changes/audit-executor-minimal-repair/proposal.md:64`
- scenario: queuedAt=0、complete_at=130000且raw=null，同时满足completed_late和completed_no_result；collect取得complete_at=310000的完成记录时，同时满足截止前未完成的running_at_deadline和completed_late，前者要求完成时间null。相同输入由不同实现得到不同状态及时间字段。
- suggestion: 补充确定性的有序判定或决策表：明确迟到判定与空结果判定的优先级、complete_at等于整轮截止的归类，以及execution_state采用截止快照还是收集时证据；截止时状态与后续完成时间、termination_evidence分别表达，并为这些交叉输入指定唯一预期。
- found_by: aria:tech-lead

### 5524c7fd [major] 以原生Workflow startTime定义的派发截止没有接入生成脚本可用的计时通道，相对timer不能保证在该原生截止点停止派发。
- scope: `workflow_start/round_ms/dispatch_deadline_clock`
- source: `/home/dev/Aria/openspec/changes/audit-executor-minimal-repair/proposal.md:51`
- scenario: 原生startTime=0，脚本在20ms安装300000ms相对timer；一席在原生300010ms返回时roundExpired仍为false，worker派发下一席。collector虽拒绝越窗票，但无法撤销越窗派发，违反第53行的停止派发承诺。
- suggestion: 明确脚本计时零点与原生startTime的接线及误差语义。若现有公开接口不能提供原生零点，则区分相对timer调度截止与原生时间准入裁决，明确前者并非原生边界硬截止，不假造可用时钟或取消能力。
- found_by: aria:tech-lead

### 67af0ca5 [major] execution_state表的完成、迟到和无结果谓词相互重叠，尚未形成所要求的互斥分类。
- scope: `execution_state.partition.completed_late_running_no_result`
- source: `/home/dev/Aria/openspec/changes/audit-executor-minimal-repair/proposal.md:64`
- scenario: 角色在t=200000ms排队、t=300001ms完成，collect时原生完成证据已存在：它既满足running_at_deadline的“截止前没有完成事件”，也满足completed_late；前者要求完成时间null，后者已有确定完成时间。另一个超过120000ms才返回null的调用同时满足completed_late和completed_no_result，两个实现可合法给出不同状态。
- suggestion: 定义有顺序的分类决策表，明确截止后完成证据存在时的唯一状态，并规定迟到与null结果的优先级；已知完成时间不得因分类而清空。如需表达截止瞬间状态，将其与最终完成证据分开。为截止后有完成证据及迟到null两个交叉输入加入唯一状态和时间字段断言。
- found_by: aria:qa-engineer

### 86935565 [major] 整轮控制窗口绑定原生startTime，但生成脚本没有取得该零点或剩余预算的契约，无法保证按同一截止点停止派发。
- scope: `workflow_deadline.native_startTime_timer_origin`
- source: `/home/dev/Aria/openspec/changes/audit-executor-minimal-repair/proposal.md:51`
- scenario: 原生Workflow在t=0启动，脚本在t=20ms安装300000ms相对定时器；已有调用在t=300005ms返回，脚本定时器尚未触发，worker继续派发下一角色。collector即使事后拒绝该票，也已经违反原生t=300000ms截止停止派发的要求。
- suggestion: 补齐可由现有公开能力实现的控制时钟契约，明确脚本如何获得原生截止点或剩余预算；若平台无法提供，明确区分原生准入时钟与脚本控制定时器的边界，不声称两者精确等价。增加原生启动与定时器安装存在偏移、槽恰在截止后空出的负控，分别验证派发和准入，不改变120/300数值。
- found_by: aria:qa-engineer

## Role status

- aria:tech-lead: completed
- aria:backend-architect: timeout
- aria:qa-engineer: completed
- aria:code-reviewer: round_timeout_or_not_started
- aria:knowledge-manager: round_timeout_or_not_started

## Drift metrics

```json
{
  "anchor": {
    "checkpoint": "post_spec",
    "change_id": "audit-executor-minimal-repair",
    "primary_goal": "为Workflow后端建立真实执行/收集宿主、明确状态与时钟，并以显式opt-in机械执行相邻轮准入角色集合一致性；不救迟到票、不增7/7门、不改PR38暂停。",
    "why_sha256": "6cb77366966d4c9ea482387af343044e0f046845260953665a0393f690fce2ed",
    "source_sha": "cf0b25d220dd981eaead25ab834e7f96932aa559",
    "in_scope": [
      "build/collect可调用宿主与接线",
      "原生身份/计时/状态/终态证据",
      "显式opt-in可比性guard与兼容",
      "可证伪验收及后续Rule6"
    ],
    "out_of_scope_hints": [
      "恢复PR38或增加其轮数",
      "保证7席在300s完成",
      "新增成本平台/通用调度框架",
      "实现/发布当前Spec"
    ],
    "config_snapshot": {
      "_comment": "Step-by-step rollout (DEC-20260519-001). post_spec enabled 2026-05-19. post_planning enabled 2026-07-04 per DEC-20260704-001 (mid_post_spec dogfood on a concurrent A.3 draft found a per-artifact transcription drift + a shared spec-wording drift → post_planning audits A.2/A.3). Remaining checkpoints kept off until dogfood-verified; mid_post_spec deferred pending a Phase-B SMOKE-triggered dogfood. **AI 不得自行豁免已 enabled 的 checkpoint** (CLAUDE.md 规则 #10, owner 决策 2026-07-19): 「Spec 小 / 任务是已审 SC 的 1:1 派生 / 性价比不高」不构成跳过理由 —— 跳过即销毁标签, 无法事后判定该跳是否正确; 便宜的准确率跟踪 (没出事=判断对) 对「跳错但未浮出」结构性失明。豁免只能来自本文件显式 off / adaptive_rules / hotfix lane / checkpoint 结构性前提不成立。",
      "enabled": true,
      "mode": "convergence",
      "max_rounds": 5,
      "checkpoints": {
        "post_brainstorm": "off",
        "post_spec": "convergence",
        "post_planning": "convergence",
        "mid_implementation": "off",
        "post_implementation": "off",
        "pre_merge": "off",
        "post_closure": "off"
      },
      "teams": {
        "post_spec": [
          "aria:tech-lead",
          "aria:backend-architect",
          "aria:qa-engineer",
          "aria:code-reviewer",
          "aria:knowledge-manager"
        ],
        "post_planning": [
          "aria:tech-lead",
          "aria:backend-architect",
          "aria:qa-engineer",
          "aria:code-reviewer",
          "aria:knowledge-manager"
        ]
      }
    },
    "workflow_orchestration_authorized": true,
    "authorization_source": "用户在本会话AskUserQuestion选择运行新Spec审计，明确授权Workflow多Agent编排。"
  },
  "drift_guard_enabled": false,
  "is_refocus": false
}
```

# 发布前兼容修订：历史报告读取

> **Status**: Implemented — 定向TDD、独立负控和两阶段审查通过；插件v1.78.0已本地合并双推；主仓集成与原周期收口仍进行中
> **Date**: 2026-11-07
> **Scope**: 原执行器修复发布前的读取兼容；不改旧审计结论、原始验收、周期预算或PR #38暂停

## 1. 真实授权与目的

用户新`/goal`要求完成原交付并完成推荐机制change的Phase A。独立源码核对发现，新scope的build在全量历史归属扫描时，会被已入主干的旧报告`post_spec-R2-1783054040265-dispatch-input-delivery-code-reviewer.md`拒绝：该报告有`audit_type: post_spec`、`checkpoint: convergence`、`spec_id: aria-2.0-m6-dispatch-input-delivery`。

这不是本轮审计投票。原实现与contract对字段矛盾的字面拒绝相符，不能未经owner裁定直接收窄。用户已于2026-11-07T11:29:52.270Z真实选择**“兼容可识别旧格式（推荐）”**：允许读取侧适配，原件不改；当前任务历史周期、真实矛盾和无法判明来源仍须阻断。问答来源保存在`.aria/notes/2026-11-07-goal-delivery-and-phase-a/legacy-compat-owner-decision.json`，不是自动通知或旧周期override的重放。

## 2. 兼容规则的拟定边界

本修订为既有历史读取/保全能力补充封闭的legacy解释，不以“其它scope”作无条件忽略：

1. 仅对可确认的legacy Markdown frontmatter识别模式误置形态：文件名有已注册checkpoint前缀，`audit_type`与该前缀一致，`checkpoint`只能是旧执行模式`convergence`或`challenge`，并有可解析且无矛盾的变更归属。
2. 变更归属必须利用真实`spec_id/context`和已知change目录/文件名线索。字段重复、互相矛盾、unknown归属，或文件名明确指向另一已知change，均不借兼容放行。不能仅因任意字符串含convergence就豁免。
3. 规范格式中两个真实checkpoint的矛盾、无法识别的旧模式、缺少匹配`audit_type`，仍保留拒绝。读取失败/软链接/截断扫描等原护栏不变。
4. 可识别legacy一经解释，仍必须参与原scope历史检查。若属于当前scope，必须按既有周期检测拒绝新genesis；不得为了兼容旧字段而重置轮数或忽略历史。
5. 原始文件的路径、字节和hash不改。兼容解释与归属观察留痕；绝不写回旧报告或伪造新PASS。

实现者须从实际现有parser、已知change命名及消费者推导最小实现；以上边界若不可无歧义实现，先报告具体冲突，不自行扩大兼容集合。

## 3. 实施与验证

- 先新增真实build入口的baseline-failing定向测试，看到正确RED后才写生产实现。
- 最小文件域：`aria/skills/audit-engine/scripts/audit_executor.py`、新增legacy兼容测试文件、`references/executor-contract.md`的字段/schema解释。
- 测试覆盖：健康对照；真实旧格式的他scope；同格式的当前scope不得新开周期；真checkpoint冲突；缺失/矛盾归属；不识别模式；软链接与读取错误；原件hash、genesis/events/workflow副作用。
- 非作者另构造至少两类真实坏态，检验不是“拒绝所有旧格式”或“放过所有冲突”。
- 新修订只回归受影响路径，不重写旧B19/19接受记录或将新结果冒充旧297项原验收。必要回归属于本次新增代码变化，不是无依据重做Phase B。
- 独立代码/规格合规审查及原发布门仍执行；规范要求的启用检查点不由本记录豁免。

## 4. Rule #6

拟定分类：新增代码与legacy字段/schema描述为SOT决策表第1行，使用新建baseline-failing结构化测试作deterministic substitute；原有运行时指令及description保持原字节，既有Rule #6接受记录保持原归属，不重写。

最终须对实际diff逐hunk核对。如果改变AI调用/调度/判定指令或无法确认性质，则按SOT照跑skill-creator场景1；description实际变化时另跑4b。不能仅因文件在Python或本次变更小而认定豁免。

```yaml
rule6_note:
  decision_table_row: 1
  description_changed: no
  scenario1: not_required
  scenario4b: not_required
  negctrl: n/a
```

实际逐hunk核对仅新增解析代码、测试及legacy字段/schema描述，SKILL.md与description原字节未变，因此第1行deterministic substitute成立；这里的negctrl不冒充场景4b的10条触发负控。新增15项回归与既有41项历史测试共56/56通过，0fail/error/skip；非作者18项正常断言通过、2类真实坏实现CAUGHT。主控类型检查产品2文件与独立fixture1文件均0error/0warning；隐藏目录已显式纳入，未拿零文件检查作证。

原报告SHA256保持`d6c9e0d25ead1d408ce5ece6adb58473b1b7e7311c90e3270158f38020721861`；真实仓build已记录LEGACY_CHECKPOINT_MODE并成功构建，不以新Spec是否收敛作为原交付前置。详细来源见`.aria/audit-reports/audit-executor-minimal-repair/release-compatibility-evidence.json`及本轮notes；旧验收与失败原件不回写。

## 5. 不变量与原计划关系

原SC-1～SC-10、120s/300s/并发2、同部分角色可收敛、guard默认false/本仓true、固定scope预算、未知终态阻断、原PR38暂停均不改变。原proposal与历史审计按原revision保存，此文件记录本次owner批准的发布前读取兼容，不重命名旧周期或为旧审计开新额度。

当前新`/goal`已要求原交付继续集成与收口；详细任务的授权进度须同步此实际事实。推荐机制change只完成Phase A，不混入本次插件行为发布。

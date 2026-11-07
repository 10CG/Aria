# 审计执行器最小修复

> **Level**: Full (Level 3 Spec)
> **Status**: Approved — revision2 post_spec R3按现行legacy规则收敛；post_planning R5未收敛、5轮耗尽，2026-11-03 owner经真实AskUserQuestion选择“接受当前结论，继续实现”，仅本检查点 overridden_by_user=true，不改票、不加轮
> **Implementation Authorization**: Phase B TASK-001～019的原接受记录保留；2026-11-07用户新`/goal`要求完成原交付，继续TASK-020/021的集成、发布同步与周期收口。发布前legacy读取兼容另有真实owner裁定，见[release-amendment.md](./release-amendment.md)。旧规划审查接受仍只属于其原检查点，不泛化为新票；PR #38恢复、构建部署及168h仍不在本轮范围。
> **Created**: 2026-11-01
> **Linked Issue**: `10CG/aria-plugin#210, 10CG/aria-plugin#209`
> **Module**: aria-plugin / audit-engine；主仓仅配置接入与规范证据
> **Owner decision**: 2026-11-01 用户选择“加入可比性守卫”；不要求七席全到，不自动调整时限或轮数，PR #38 继续暂停。

## Why

PR #38 的 R3–R5 同为候选 `49d7da44`，实际派发为 7/6/5 席、准入为 4/2/1 席。120s 是准入过滤而非原生取消，超时调用继续占槽；300s 截止时，未派发与已启动未完成被同一状态覆盖。聚合随后比较不同准入总体的结论集合。冻结已观察角色结论，只改变准入集合即可精确重放 5/3/2 项及全部比较键，不能把数量下降当作修复进展。

当前实际宿主是逐轮生成的 Workflow 脚本和临时 persist 脚本。仅在 Skill 散文中补提醒，既不能保证字段真实生成，也不能机械执行用户已确认的可比性约束。本变更建立可调用代码宿主、接线及拒绝坏输入的测试；不是把 PR #38 的暂停审计另起名字重跑。

诊断 SOT：[报告](../../../.aria/notes/2026-11-01-pr38-audit-execution-diagnosis/README.md)、[原生时间表](../../../.aria/notes/2026-11-01-pr38-audit-execution-diagnosis/timeline.tsv)、[离线重放](../../../.aria/notes/2026-11-01-pr38-audit-execution-diagnosis/replay-result.json)。R2 是不同候选且有独立确认事实通道，不与 R3–R5混作同一聚合总体。

## What

### 1. 范围与不做事项

本次仅覆盖 **Workflow 后端**的一轮构建、原生结果收集、状态分类及可比性计算；模式为 convergence。`require_same_admitted_roles=false`时生产编排保留原路径与算法；true时才强制接入新宿主。新后端本期要求该checkpoint在项目配置中有显式团队数组；未支持的人工团队覆盖或动态增补报unsupported，不偷偷删人或退回旧路径。跨插件代码、配置注册和主仓配置接入，因此为 Level 3；不意味着扩大产品目标。

不做：
- 不实现或承诺未公开的 `agent()` 单席取消接口；不在超时后无确认地释放仍被调用占用的槽。
- 不保证七席在300s内全部完成，不降低审计域、不自动换模型、不调整120s/300s、并发2或max_rounds。
- 不加入7/7门、不救迟到票、不跨轮继承缺席角色的旧票，不以角色减少假造收敛。
- 不实现全量成本闸、重试平台或通用调度框架；不顺手解决 #209/#210 全部内容或关闭整单。
- 不修改 PR #38 代码、历史报告、原轮数或暂停处置，不合并、部署或启动168h。

### 2. 真实代码宿主与接线

新增 `aria/skills/audit-engine/scripts/audit_executor.py`，使用 Python stdlib，提供 `build` 与 `collect` 子命令。生成物是工具内部审计执行程序，不是消费方业务代码模板。

1. `build --repo-path <root> --manifest <json> --output-dir <dir>`：从固定的`<root>/.aria/config.json`与插件DEFAULTS读取有效守卫和显式团队，生成`workflow.js`与`build-record.json`，并按[revision2 amendment](#revision2-implementation-amendment)维护固定scope证据与reservation，不再将这两个文件误解为全部持久化副作用。原始配置的新守卫键必须先做严格布尔校验；JSON损坏/类型错误报错，不经过通用“回落默认false”而关门。manifest只是期望值，不能覆盖配置；角色名单/守卫不一致或预算不等于本后端120000/300000/2时拒绝。build-record保存配置/defaults/脚本hash和有效值；collect及check-result重读同源配置，漂移时报错，不静默换策略。JS以纯字面量`export const meta`开头；数据用JSON编码，不拼接未转义代码。
2. audit-engine 编排层用真实 `Workflow({scriptPath: <workflow.js>, args: ...})` 执行。脚本只用公开的 `agent/log/phase`、Promise与已在原生记录中运行的timer机制；不导入本地模块、不使用Node/文件系统、`Date.now()`或随机API。
3. 工具返回后不再直接发布collect结果：按[revision2 amendment](#revision2-implementation-amendment)先传真实run_id/原件到 `collect --prepare-policy`，必要时完成独立drift调用，再以相同基础参数执行最终 `collect --repo-path <root> --manifest ... --build-record ... --workflow-run-id ... --native-record ... --previous-round ... --output ...`。最终native指冻结副本；首个有效逻辑轮省略previous-round，void尝试不清历史。
4. 生成脚本在每次调用前记录attempted、角色索引/标签；返回时输出深拷贝的逐角色快照及已返回raw，不让截止后回调继续改写返回对象。仅声明角色不等于attempted，attempted也不冒充原生已启动。
5. **最终** `collect` 计算并一致渲染 `round-result.json` 和配套MD聚合报告；`--prepare-policy`成功不发布它们、不表示审计通过。audit-engine必须消费此文件的准入集合、稳定性及收敛布尔值，不再由AI手填这些值；沿用原命名、frontmatter与质量verdict语义。
6. 消费前调用同一 `collect` 的 `--check-result <round-result.json>` 只读模式，传入相同repo-path/manifest/build-record/native/previous。它重算并比较身份、输入hash、逐角色判定、角色集合、keys、policy与全部收敛布尔域，忽略纯展示生成时间；不一致则非零退出且不覆盖原报告。正常接线必须经此校验，不把未经校验的MD当作helper已验证结果。此保证不声称能阻止AI在工具外手工伪造文件。

不得只新建helper而不修改Skill的实际调用链。`build-record`包含生成脚本hash；collector核对原生记录内**嵌入的script内容**，不用可能被后轮覆盖的scriptPath作为执行内容证明。

公开 `agent()` 接口未提供可确认的取消/原生起始事件回调；本Spec不假造能力。无法取得本次原生记录时，collect报错而不是转为AI散文准入。非Workflow后端保持原路径，不宣称本次覆盖；守卫启用却没有所需参与证据时不得判稳定。

### 3. 输入身份与原生计时

manifest至少包含：`audit_cycle_id`、`client_round_id`、`checkpoint`、`change_id`、`round`、`candidate_sha`、配置角色id/agentType/model别名、冻结prompt、`single_agent_ms`、`round_ms`、`max_parallel`、有效守卫配置；revision2另加 `attempt_index/evidence`（见下文amendment及executor-contract §10）。round是有效逻辑轮号，void不推进；attempt_index含void单调递增。两个id由宿主在VM外产生；audit_cycle_id跨轮/会话延续，不能自动换id重置预算。

- `role_id`与agentType必须逐项等于项目显式团队数组中的完整注册名，顺序不改；不自行补别名、删除或增补角色，同轮唯一。该最小后端不支持manifest的model/agents_config覆载，模型由agentType自身配置/继承决定，别名说明仅作追溯。标签由client_round_id与索引生成，collector必须一一映射原生agent记录，拒绝重复、串轮或无法映射。
- **准入时钟**：原生Workflow `startTime`为零点，`D = startTime + 300000`；单席起点为原生`queuedAt`，已知完成时刻`C = startedAt + durationMs`。只接受整数时间与一致先后关系。准入要求`C - queuedAt <= 120000 AND C < D`；等于D不准入。
- **调度时钟**：VM安装相对timer的事件S0是控制起点，timer延迟仍为300000ms；未公开S0与原生startTime对齐接口，所以不承诺在原生D精确停止派发。仅承诺timer回调置stop后不再调用agent并返回快照；同轮最多2个未返回调用，席超时不释放槽。不得把未知偏移填0或发明同源时钟。
- collector记录两种时钟边界、`control_native_alignment=unknown`及按原生queuedAt判出的`dispatched_at_or_after_native_deadline`。即使软timer偏移导致D后派发，该票也必须按原生窗口拒绝，不能延长D。控制硬截止能力未解决，不宣称此修复保证原生时间精确停派发或所有OS进程退出。
- build/collect宿主耗时单列；相对控制timer与原生准入各使用既有300000数值，但不再将二者假称精确同源。外层耗时、后端限制与越窗派发必须显影，不据此放宽120/300或重置轮数。若产品需要原生D硬截止，应另行取得运行时能力和政策授权。
- 未知完成时间保留null。原生duration是调用wall-clock，不是纯推理时间；实际model标签与配置别名分开记录。

### 4. 状态分区与终态证据

`execution_state`采用**collect时证据视图**，不是截止瞬间快照。先验证身份/文件完整性/时序；声称done却缺完成字段、attempted与节点矛盾等直接collect错误。之后严格按以下顺序首个命中即退出：

| 顺序/值 | 判据 |
|---|---|
| 1 `not_dispatched` | 完整原生记录无节点，且attempted=false |
| 2 `dispatched_no_completion` | 有有效节点但collect时无可验证C；C=null，不声称此刻仍在运行 |
| 3 `completed_late` | 已知C且`C-queuedAt>120000 OR C>=D`，无论raw是否null，保留真实C |
| 4 `completed_no_result` | 已知C且窗口内，raw=null；不猜skip/API失败 |
| 5 `completed_parse_error` | 已知C且窗口内、raw非null但契约失败 |
| 6 `completed_admitted` | 已知C且窗口内、报告有效，唯一可投票状态 |

另记`unfinished_at_native_deadline = queuedAt<D AND (C未知 OR C>=D)`，不因此清空collect时已知C。例：130000ms返回null先判late；310000ms已知完成判late且保留310000；恰在D完成判late；只有真实未知C才保持null。已开始后被中断但没有完成报告的任务仍可为dispatched_no_completion，终态证据在下字段独立表达。

另存 `termination_evidence`：`completed` / `interrupted_observed` / `unknown`，及其原件引用。运行时中断标记不是新的用户授权，不证明OS进程全部退出。下一轮启动前必须呈现仍未确认的调用终态，不得宣称已清理或直接释放其资源槽；无法确认则暂停新增派发并上报。此为资源槽生命周期约束，不额外改写本轮收敛公式，也不作废已有有效票或重置轮计数。

迟到raw独立保留hash/引用，只可进入既有独立事实核实通道，不并入准入票。既有全部失败轮作废、部分失败incomplete、漂移及max_rounds处置规则不变。

### 5. 可比性守卫（用户已选择，尚未激活）

新增布尔配置 `audit.require_same_admitted_roles`：插件DEFAULTS为false；非法类型报配置错误，不作truthy转换。本仓在Phase B显式设true，并同步项目配置模板；本次起草不改运行配置。

- 对本轮和紧邻前轮，分别从真实 `completed_admitted` 记录取得非空、去重后的role_id集合。不能从frontmatter的agents配置名单或结果数组长度推断。
- 启用时两集合必须相等；只比角色身份，不把candidate SHA相等或model标签相等偷偷增加成新门。候选、模型、配置名单仍记录供追溯。
- 首轮无前轮为 `first_round`；旧报告无实际参与证据为 `missing_participant_evidence`；空集合为 `empty_population`；不同集合为 `population_changed`。这些情况的population_comparable=false；重复id、串cycle或损坏记录是错误，不自动重置基线。
- 两轮属于同一audit_cycle_id/checkpoint/change_id且轮号相邻才可配对。不会为旧PR生成新cycle_id或把历史报告回填为合规新证据。

机器计算：

```text
conclusion_keys_equal = 既有四元组集合严格相等
population_comparable = 启用时两轮实际非空准入角色集合相等
conclusions_stable = conclusion_keys_equal AND (NOT require_same_admitted_roles OR population_comparable)
converged = conclusions_stable AND 既有unanimous_pass AND NOT 既有all_failed_void
```

比较函数的关闭向量中population_comparable=null、reason=`disabled`，conclusions_stable与converged遵循原算法；生产关闭路径保持legacy，旧报告不强制补新字段。开启时同一部分角色集合仍可收敛，incomplete不新增为否决项。守卫是AND收紧，不能覆盖既有drift/error等阻断或发放额外轮次。质量verdict与收敛布尔值仍分开。

### 6. 机器输出与消费边界

round-result包含：上述身份/预算、configured/dispatched/admitted角色集合、逐角色状态/时间/终态原件引用、原生run_id/script hash、raw引用、旧四元组、conclusion_keys_equal、population_comparable/reason、conclusions_stable、converged、incomplete/all_failed_void。

输出原子写入项目 `.aria/audit-reports/` 的明确run-key文件；发生错误不覆盖已有已验证结果。报告frontmatter采用既有checkpoint/round/context命名，新增参与信息为additive字段；不能用PASS质量级别代替converged或merge gate。

真实接线验收必须证明[revision2 amendment](#revision2-implementation-amendment)的build→Workflow(scriptPath,args)→prepare→必要的独立drift→最终collect→check→报告消费者实际发生；只有单测、文件存在或宣称“由audit-engine保证”不算。

### Key Deliverables

| 文件 | 职责 |
|---|---|
| `aria/skills/audit-engine/scripts/audit_executor.py` | build/collect、状态分类及可比性计算代码宿主 |
| `aria/skills/audit-engine/tests/test_audit_executor.py`及portable fixtures | 原生记录回放、坏输入/坏实现拒绝与边界测试；不依赖本机绝对路径 |
| `aria/skills/audit-engine/SKILL.md`及`references/executor-contract.md` | 真实调用接线、输入/输出与后端能力边界 |
| `aria/skills/audit-engine/references/convergence-algorithm.md` | opt-in公式、无参与证据与部分角色兼容性 |
| `aria/skills/config-loader/DEFAULTS.json`及`SKILL.md` | 注册false默认值，并明确该键非法类型报错、不适用通用回落false策略 |
| 主仓`.aria/config.json`、`.aria/config.template.json` | 本仓显式true接入；不顺带补齐#222全部配置问题 |

## Impact

| Type | Description |
|---|---|
| Positive | 相同结论但不同参评总体不能被本仓直接判稳定；状态和时钟有真实输入，不再手填或混淆已启动/未派发。 |
| Compatibility | 默认false保持采用方原收敛行为；本仓显式true是本次用户选择。仍允许同一部分角色收敛，无7/7新门。旧报告不倒写。 |
| Risk | 原生记录schema/路径有宿主依赖；参数显式传入并严格验证，不猜路径、不虚构取消API。可能更经常显示“不可比”，不承诺自动收敛或七席完成。 |
| Rule 6 | 本阶段只建Spec，无Skill变更。实现会修改运行时指令，必须用skill-creator跑场景1；若description也改则另跑4b。结构测试不替代这项AB义务，结果写rule6_note。 |
| Release | 发布面按实现后的版本管理规范同步；不以本Spec提前宣称已发版或擅自定破坏性变更兼容级别。 |

## Tasks

见[粗粒度tasks.md](./tasks.md)与[A.2/A.3详细任务](./detailed-tasks.yaml)。粗任务编号保持不变；详细任务包含依赖与Agent预分配，须经post_planning审计，不构成Phase B执行授权。

## Success Criteria

| ID | 可证伪验收 |
|---|---|
| SC-1 | build产物可经真实Workflow的scriptPath调用；不需要VM内文件/Node/Date.now/取消API。保存run_id、嵌入script hash与collect输入对应证据。无真实调用证据不得标完成。 |
| SC-2 | portable R2–R5原生回放分别得到派发6/7/6/5、准入2/4/2/1；12个旧占位拆为8个dispatched_no_completion、4个not_dispatched；右删失不填0，中断不冒充报告完成。 |
| SC-3 | 同一部分角色集合、相同keys、全部准入票PASS、incomplete=true时，开启守卫仍可converge；证明不是7/7门。 |
| SC-4 | 两轮keys相同但实际角色集合不同，关闭守卫保持legacy结果，开启时conclusions_stable=false/converged=false且reason=population_changed；坏实现忽略角色或只比集合大小必须被拒绝。 |
| SC-5 | 首轮、旧参与证据缺席、空集合、重复id、串cycle、时钟矛盾、错误script hash各有指定非通过结果；不得把取不到数据当空集稳定。 |
| SC-6 | q=0/C=120000可准入、C=120001为late；q=200000/C=300000为late。C=130000且raw=null先late；collect时已知C=310000为late且不得清空C；未知C保持null。timer安装偏移20ms且槽在原生D后空出的fixture允许暴露软控制越窗派发，但必须显影并拒票，不能宣称原生硬截止。未取消却释放槽的坏实现必须因物理并发超2被拒绝。 |
| SC-7 | collector输出被真实报告链消费；对converged/参与集合的篡改由重算校验拒绝，正常渲染入口不得跳过重算。保留消费者源码及一次完整接线探针；不把Skill工具外的人工伪造也宣称为机械可防。 |
| SC-8 | 缺省false维持整个legacy生产路径；本仓true且manifest写false/删减配置角色/修改固定预算必须build失败；源配置在build后变化必须collect/check失败；字符串等非法值不得回落false。显式团队/模式不受支持时报错，不静默换后端。原quality verdict、all-failed作废、drift/max_rounds处置不变。 |
| SC-9 | source文件/PR #38历史报告/原max_rounds不被fixture或探针改写。新机制真实探针使用独立目标，不以PR #38重跑验收；新Spec自己的审计不计作该PR的新轮次。 |
| SC-10 | 新宿主单测、坏实现负控、实际调用探针、Rule #6结果齐备后才可宣称实现完成；本Spec审核通过不等于以上实现验收已完成。 |

## 审核与阶段边界

- 根配置post_spec已启用，本Spec起草后必须执行，报告存`.aria/audit-reports/`并以本change_id归属；与PR #38 pre_merge周期分离。
- 用户于2026-11-02批准本规范并授权A.2/A.3详细规划；详细任务落盘后必须按配置执行post_planning，规划产物生成不等于该检查点已通过。
- revision1的Approved/post_spec与post_planning R3结论保留原归属；revision2新增面尚未通过post_spec/post_planning，必须绑定本修订hash另行审查，不能凭v1绿灯开始本修订实现。原Phase B授权范围不扩大；提交推送发布、Phase C/D与PR #38恢复仍须另行授权。
- PR #38保持暂停，其原max_rounds=5及合法后续处置不变；本Spec不是旧审计的新名字或预算重置入口。

## revision2 implementation amendment

本节为主控委派的透明技术修订，状态 `task002_contract_accepted_implementation_pending`；post_spec已审、post_planning由真实owner接受未收敛结论继续实现，不冒充owner逐字批准本段字句。TASK-002完整独立两阶段审查及三项修补复核已PASS，仅表示契约交付完成，不表示产品实现或验收完成。仅补证据传输、周期闭包与唯一规范化；原Why、SC-1..SC-10、120000/300000/2、同部分角色可收敛、false完整legacy和PR #38暂停/max_rounds=5不变。字符级接口SOT为[executor-contract §10](../../../aria/skills/audit-engine/references/executor-contract.md#10-revision2-证据协议与唯一重算)；以下是对What §2/3/6失效接缝的替代定义，不保留另一条直接collect发布路径。

1. **显式prepare**：仅新增collect的 `--prepare-policy`，与 `--check-result` 互斥，不加子命令。build→真实审计Workflow(scriptPath,args)→prepare→必要的独立drift Workflow→最终collect→相同输入只读check→消费。prepare只冻结输入/生成policy-request及需要的checker脚本，exit0不是审计通过，不发round-result/MD或commit；未取得真实必需checker证据的final报E_POLICY_SOURCE。Python唯一生成规范化conclusions/request/policy；编排层不手写另一套算法。
2. **前后证据分离**：manifest.evidence包含cycle_origin、previous_round、dispatch_preflight、policy_inputs等运行前FileRef，以及post_audit_index_path/post_drift_index_path/post_disposition_index_path三个未来locator。真实capture adapter按回执runId/Transcript入口或显式路径生成新index，不冒充native字段。prepare/final保存原字节blob及origin关联；未来hash/runId不塞回已冻结manifest。JSONL映射逐run/agent/uuid/完整正文核验，损坏引用拒绝、仅无引用可unknown。封存后live增长不改旧票；新终态只作资源preflight。
3. **无环scope与持久化**：允许单stdlib脚本维护固定 `.aria/audit-reports/_executor-ledgers/<完整scope hash>/` 的genesis、连续reserve/commit/observe/disposition、不可变输入快照与POSIX短期排他文件锁。scope由checkpoint/change决定，不含cycle/candidate；首次cycle_origin=null仅在锁内来源扫描确证无genesis/旧同scope周期时合法，build生成genesis后由build-record引用，genesis不含本次build-record/manifest自hash。后续null/换cycle/旧head拒绝；本期不自动rollover。pending不能自动作废或重派；恢复只复用同reservation/同完整输入字节，半发布仅重算一致才补缺文件/commit，冲突不覆盖。check完全只读。
4. **历史与有效轮语义**：递归从固定scope读完整事件和冻结manifest/build/native/policy源，不执行旧代码；visited/visiting拒绝循环，身份/seq/有效轮/attempt_index连续，缺叶子拒绝。previous指紧邻有效轮，void保留attempt_index/client_round_id却不耗额度、不推进round、不替换基线、不进normal振荡序列、不完成refocus义务。R1有效→R2 void→R2新attempt有效仍与R1比较。is_refocus由真实REFOCUS决策派生；checker skipped不增加也不清零consecutive_refocus_count，不能伪装已证明normal。first_round仅跳比较/drift，limit=1仍耗尽；固定genesis上限只有绑定耗尽head的真实一次性increase_rounds才加2。
5. **真实政策/处置来源**：固定config/defaults/mode/level、Step0实际fallback观察和原文件byte-span生成冻结anchor；缺wrapper不是缺锚证据。独立checker的完整request/脚本/args/run/raw或真实失败事件决定drift，不把审计timeout当checker失败。其60s独立timer位于原30–60s范围，仍不释放未知调用槽。原生AskUserQuestion须校验tool_use_id/sourceToolAssistantUUID、toolUseResult.questions/answers/annotations及实际cycle/head/三选项映射；旧样本仅证schema，不是新授权。后发生的合法动作由相同collect参数封存sidecar/disposition事件，旧结果/MD不改；check后消费base+sidecar view，accept/degrade保持converged=false，increase固定+2且禁止重放。无动作由空已验证事件序列导出，不添加无人验证的false默认。
6. **canonical_v1**：只收当轮准入findings，精确(category,scope) bucket取最高severity，每个实际type各保留一条conclusion及该type全部完整finding variants/members；完整C(finding)字节相等才合并，不继承prior_id或临时persist归一化。bucket多variant标unresolved_variants，只表示保守保留差异，不冒充语义矛盾识别、不加收敛门。完整四元组比较/排序，短id仅展示；scope不trim/改大小写/路径归一化，summary仅展示。drift分母为真实conclusions长度。有效阈值采用binary64除法与>=，不另改Decimal/Fraction；边界向量见contract §10.4，保持配置数值不变。

### Amendment 验收向量（映射原SC，不替换原要求）

| 向量 | 必须可证伪的结果 | 映射 |
|---|---|---|
| A-1 | 独立三席目标首次null bootstrap无未来hash环；两席PASS零findings、另一席完成无报告，第二个有效轮同两席/keys仍收敛；prepare成功无最终报告 | SC-1/3/7/10 |
| A-2 | R1有效→void R2→有效R2的attempt=1/2/3、charged=1/1/2且最后比较R1；refocus义务经void保留、skipped不清零；limit=1首轮耗尽 | SC-3/5/8 |
| A-3 | 政策原件缺失/伪失败E_POLICY_SOURCE，JSONL串agent/损坏E_NATIVE_EVIDENCE，无终态引用unknown阻断新派发；有源非空结论真实checker路径可完成 | SC-1/5/6/7/8 |
| A-4 | 前史回边按contract §10.6的origin栈优先级报E_HISTORY_CYCLE，不要求hash固定点；跳轮/换cycle/null重置/回退head E_PREVIOUS_IDENTITY，缺叶子E_POLICY_SOURCE，config擅增额度E_SOURCE_DRIFT；篡改派生boolean E_RESULT_MISMATCH。同context而checkpoint不同不误判同scope，已登记/可归属旧scope不迁移，未知归属如实告警不冒称全局无历史 | SC-4/5/7/8/9 |
| A-5 | 同scope不同claim/type、Critical/Minor混合与短id碰撞保留完整成员/变体/type及最高severity；吞成员、合并不同key的坏实现命中指定断言 | SC-4/7/8 |
| A-6 | 同reservation/同字节窄恢复只补缺commit；不同字节冲突不覆盖、不重派。真实问答处置重放/通知/跨cycle拒绝；sidecar不修改base结果、不伪造converged | SC-5/7/8/9 |

正常构造顺序、闭合schema与四组坏态见contract §10.8；由非作者QA独立构造坏态，而非把本文自带fixture当拒绝证据。后续TASK-012须同步真实SKILL/execution-modes调用/汇总指令，TASK-013验证接缝，TASK-017仍履行Rule #6。本次仅修文档，不声称已实现这些接口，不改运行配置或TASK状态。主控须先完成revision2已启用的post_spec/post_planning并登记修订hash/归属；原v1报告不删除、不迁移，本修订不重开耗尽旧周期或PR #38。

## References

- 2026-11-01本会话用户选择：加入可比性守卫（同一部分角色仍可收敛）。
- [诊断验证回执](../../../.aria/notes/2026-11-01-pr38-audit-execution-diagnosis/verification.json)：38份原件未改、离线重放一致，未产生新审计票。
- [配置闸门权限](../../../standards/conventions/configured-gate-authority.md)、[Rule #6](../../../standards/conventions/skill-benchmark-exemption.md)。
- #210/#209为关联父问题，本Spec不采信其所有历史根因表述或承诺关闭整单；实际依据为本次原生诊断。

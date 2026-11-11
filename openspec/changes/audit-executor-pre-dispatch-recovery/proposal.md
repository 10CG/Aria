# 审计执行器派发前拒绝的受控恢复

> **Level**: Full (Level 3 Spec)
> **Status**: In Progress — post_spec R5真实accept_current、post_planning R5合法OSCILLATION末轮PASS（均converged=false）；TASK001–017完成，插件v1.79.0已本地合并、双远端分发并通过fresh完成审查；018主仓采用中，实际恢复未执行，原资格不移算，展示/AB不重开
> **Created**: 2026-11-07
> **Linked Issue**: `none`
> **Module**: aria-plugin / audit-engine；主仓规范、恢复证据与版本采用
> **Authorization**: owner 于 2026-11-07T15:49:25.673Z 真实问答选择“修复受控恢复能力（推荐）”，授权必要修复的设计、实现、验证和所需发布，再恢复原规划审计；不授权关闭守卫、重置旧 cycle/预算，或开发推荐机制 Phase B。另一次真实 root 问答已确认本旧对象只由本对话及其明确委派操作域管理、未另行授权/转交其他会话或机器；接受 v1 必须有真实操作者有界声明的本机交互恢复，不要求全平台自动隔离。该声明不覆盖已知成功或未知运行反证，不替代启用审计。

## Why

原执行器 v1.78.0 已交付并完成原周期收口。另一个 `state-scanner-goal-aligned-recommendations` 的 `post_planning` R1 构建生成了 570716-byte 脚本并写入唯一 reserve；一次原生 Workflow 调用返回 `exceeds 524288 bytes` 输入拒绝，未产生该次调用的 runId 或审计票。现有精确恢复只复用原输入且禁止再次派发，collect 又要求真实 runId；因此该检查点不能合法继续。此次拒绝不单独证明所有历史会话未运行。

这是原工具未覆盖的输入拒绝/恢复情形，不是给原审计换名字增轮，也不是以工具修复为由重做已接受 B19/19。

### 诊断依据与边界

- 真实工具调用：session `ef6094a0-96c0-4895-bee8-412d5d0b24f3`，call UUID `018ed58a-19d7-4a5b-8ebd-9839e469f1d8`、response UUID `2b57abae-25c8-47dd-b723-b8fbc2632946`；两条原生记录的 parent/sourceToolAssistantUUID/tool_use_id 完整关联，response `is_error=true`。普通元数据及原件定位保留在本机，不把摘录当独立原件。
- 隔离 baseline 已实跑：纯 renderer 与历史脚本逐字节一致（SHA256 `dd23a303125c031c51e70f6d74c0852069f47e4977b68921131979c52bc2aad9`）；复制同五席 prompt 到合法临时 fixture 后，旧 build 接受 570090-byte 脚本并产生 reserve，命中指定 `SC-CAPACITY RED`，exit 1。临时路径不同，不声称其脚本 hash 等于历史原件。
- 主仓基线 `0641cf5f`；插件 v1.78.0 `2d8e223f`。关联广域背景仍为 aria-plugin #209/#210，但此次新故障没有专属 issue；已分页查151条 issue 的特定容量/派发前关键词，不把该检索说成语义上不存在任何相关 issue。
- 新轨已认领：`audit-executor-pre-dispatch-recovery-023236f2`，本地 active；fetch_degraded/no-push 如实保留。没有传主 Issue，linked-issue overlap 未检测，不宣称无碰撞。
- 本机事实 locator：`.aria/notes/2026-11-07-executor-pre-dispatch-recovery/operator-assisted-boundary-owner-decision.json` 和 `operator-recovery-target.json`。真实声明 Q UUID 为 `71846169-0a0a-41a7-9a55-ef6cc7201d8b`，tool_use_id 为 `call_ea18554d89c6447f86a831117ab62af1`，真实 user answer UUID 为 `09c1c721-bb5f-412f-996e-9bd0462cf6b3`；这些索引只定位输入，必须由宿主重读真实 root 记录并按 design.md 逐字段派生。相同文字的 `api-request-blob` 副本不是人类授权。

## What

### 1. 范围

新增一个窄恢复入口及最终脚本容量检查，保持普通 build/prepare/collect/check 的既有参数含义、计时、准入、聚合、同参评集合守卫和预算语义；普通精确 resume 的保留范围是六源兼容且脚本符合现行 L 上限的合法准备物，不新增跨源码的超限旧 pending 兼容承诺。仅恢复后的首次新 build 增加必需的已知来源 locator 输入，其他 scope 与上述精确 resume 不新增该前置。选择 canonical executor 内的受限事件扩展，不建设通用取消、重试或任意版本迁移框架。

v1 恢复对象**只限**：同 scope 当前前缀恰为 genesis + 一个首轮 reserve（attempt 1、round 1），无 commit/observe/disposition/既有 rejection；一次真实容量输入拒绝、真实操作者对该 head/reservation/script 的有界历史授权域声明、全部旧绑定及已知反证检查必须同时成立。其他阶段、后续轮、checker 拒绝以及未知运行活性不由此入口解锁。无人值守不能由 AI 生成声明，本期不改变 v2 正常业务的人类参与节点。

### 2. 核心行为

1. **容量按实际最终 bytes 计量**：`L=524288` 固定，不设放宽开关。主审计 build 在任何 writer.lock、scope/run 目录、blob、genesis、observe、reserve 写入之前，渲染一次并判 `len(script_bytes) > L`；通过时发布同一份已检查 bytes，不二次渲染。`L` 本身允许。超限返回结构化 `E_WORKFLOW_CAPACITY`，不输出 prompt。
2. **同形兄弟入口**：checker 新脚本发布前也应用同一容量不变量；不改纯 renderer 的历史重建功能。checker 既有 request/闭包准备物可能已经存在，不能声称其整次 prepare 零写入；不得发布超限 checker.js/成功 prepare-record。本次不新增 checker 恢复协议，仍保留其现有真实 tool_error 路径与 fail-closed 边界。
3. **四项共同闭合旧准备物**：核验一次原生容量拒绝记录及 loader→resolver→Tool call 的本机静态拒绝顺序；严格读取真实 operator 问答，派生独占授权/未转交声明；独立读取第二份真实问答，派生仅对此对象接受历史映像身份未独立验证的政策；锁内复核当前唯一首 reserve、全部旧绑定和已知关联成功/未知运行反证。四项缺一均保持 pending，不将当前静态窗口表述为历史映像同一证明。容量上限保留为构建检查与此次拒绝原因，不再生成声称所有历史/未来均不运行的不可执行性证书；无 runId、空搜索、单份 transcript 均不是全称证明。签字不能 override 反证。
4. **追加而不改写**：新 CLI `recover-dispatch-rejection` 验证原前缀及证据后，在原 writer.lock 内追加 `dispatch_rejected`。保留原 genesis、reserve、manifest、script、build-record、blobs；不生成 PASS、FAIL、void 或伪 native。支持不写入的 `--check-only`。
5. **计数分维度与首次续接门**：rejection 清除其所指的 pending，但不产生 policy row，不改变 charged/effective/remaining，不改变 latest effective round、latest committed attempt、资源终态或历史票。下一普通 build 仍同 checkpoint/change_id/audit_cycle_id/cycle_origin，使用新 client/run-dir，`attempt_index=2, round=1`，仍须经过全部既有资源/政策/来源检查。另按 design.md §6.1，在 build 内消费 `--recovery-sources`，独立读取当前已知 root 并冻结绑定 seq2/新 manifest/script 的 handoff；`_reserve_build` 发布前再核 live bytes，不依赖再次调用 recover。缺输入、发现反证或来源变化均不产生新 reserve；不增加事件种类。
6. **精确来源承接**：不改 `genesis.initial_sources`。仅在首个 rejection 中，允许分发包固定路径的兼容清单明确列出的旧/new executor+contract SHA256 对；其余四项**逻辑来源**的完整 FileRef、guard=true 与原预算必须不变。旧逻辑来源取原build-record.sources并由旧闭包验证，另按字节绑定genesis的冻结blob；不要求blob存储路径等于live路径。清单与新/旧闭包一起冻结。未知配对、stale清单、逻辑路径或其他source变化拒绝，普通路径不能借此跳source gate。
7. **双闭包按历史阶段读取**：旧准备物通过原 input_closure 验证，新 active sources 通过新闭包验证；同一 live 路径跨这两个已证明的 source generation 可以有不同 hash，但不能把两份闭包按 path 扁平合并或用新字节覆盖旧来源。所有后续重放与 check 必须理解这个有界转换，详见 design.md。
8. **幂等/崩溃/并发**：以原 reservation、拒绝工具对及真实声明工具对为身份。输入未变可复用已有签字；首次提交前 head 变化即过期。精确同事件重入只确认既有提交，不重复签字、不追加、不派发；在返回既有 event 之前仍须检查当前输入及新增反证。不同证据冲突拒绝。只追加一个同时闭合准备物并承接来源的事件，不分两次提交。证据已冻结但 event 未发布的半状态可按原内容续写；event 后无回执可恢复；writer.lock/head CAS 保护竞争。已合法预留的 attempt2 只从冻结 handoff 精确 resume；collect/check/历史重放不读取 live 旧 root，不能把正常 attempt2 的同 cycle 调用倒判为旧反证。
9. **完整链与真实恢复**：修复发布后，先 `--check-only` 验原生产故障，再实际追加唯一恢复事件；用包含全部冻结审计材料引用的紧凑新 manifest 开始 attempt 2，实际执行原 `post_planning` 的 build→Workflow→capture→prepare→必要 checker→collect→check。不得为容量删除审计对象/角色/准入要求，不替换旧脚本为 loader。

### 明确不做

- 不关 `require_same_admitted_roles`，不切 legacy，不改角色顺序、模型、120000/300000/2/max_rounds5，不要求全员准入。
- 不将 timeout/network/丢回执/已有 runId 的未知活性认作未派发，不释放未知资源，不提供单席取消。
- 不支持一般旧版本迁移、任意来源漂移、已有审计结果的跨版本混算或后续轮恢复；未覆盖分支保持阻断。
- 不建设全平台自动派发登记/隔离网关，不以本机检查声称覆盖所有会话或机器；不接受 AI 自填声明、模拟答复或 API 请求副本。
- 不改 scan.py、snapshot schema、推荐 Skill 指令或其 Phase B 实现；不恢复 PR #38、不部署、不启动168h。
- 不发布原生 JSONL、ledger blobs、保全 payload、密钥，不承诺跨容器完整来源闭包。

### Key Deliverables

- 执行器代码、容量与恢复测试、真实 operator 来源验证 adapter、非作者坏态 fixture，以及描述新字段/命令事实的 executor-contract。既有耗尽处置 parser 的 action/准入不放宽。
- 分发包内自动按最终源码字节生成的 `pre-dispatch-recovery-compat.json`；旧配对固定，新的 to 指纹必须匹配当前实际 executor/contract，不能 caller 自选清单。
- 必要版本/主仓采用同步、真实恢复与原规划检查点结果；原件与来源局限保留。

## Alternatives / Decision

- **采用：canonical executor 的首轮容量拒绝扩展 + operator-assisted 本机交互恢复**。将单次原生拒绝与真实有界声明明确分工，来源差异有固定、可重放的清单；不豁免来源闸门，也不冒充全平台隔离。
- **不采用：通用恢复/迁移框架或独立新 host**。前者扩大状态面；后者仍要完整承接 build/prepare/collect/check/replay，不能只写 sidecar 冒充现有程序支持。
- **不采用：固定版本容量证书代替历史授权域声明**。当前字节的拒绝性质不能排除此前其他入口、代码或机器的关联运行；已知反证仍须独立否决。
- 旧路径配置降级不是本次选择；修改旧冻结文件、换周期或绕工具容量限制不是备选。

## Tasks

粗任务见 [tasks.md](./tasks.md)。A.2 的前置是启用 post_spec 已真实执行，并取得既有审计路由允许继续的合法终态或规范内真实 owner 处置；本次为 R5 耗尽后 accept_current，sidecar 已 check，overridden_by_user=true、converged=false，不称收敛或全员通过。所有启用检查点仍须真实执行并取得各自允许继续的终态/合法处置；post_planning 尚未满足该前置时不得进入 B.1。全流程授权不代替检查点，也不回写原票或把未收敛结果改成通过。

## 单对象证据接受政策同步

除顶部所述原产品授权和独占操作域声明外，owner 在 `2026-11-09T14:40:55.778Z` 的真实 root 问答另选“接受此边界，继续恢复”，仅对已冻结旧对象接受“历史执行映像身份未独立验证”的残余不确定。权威定位为 `.aria/notes/2026-11-07-executor-pre-dispatch-recovery/historical-evidence-acceptance-owner-decision.json`；locator 不是授权本身，须依 design.md §3.2.1 从真实问答独立派生，旧声明不能代替新政策。当前本机静态窗口、PID 或版本不证明历史 binary 同一，也不再把补出该历史身份列为准入；原生精确容量拒绝、本机静态路径、全部旧绑定/六源/head/双闭包及已知反证依然必核。成功或未知关联运行仍否决。此政策不是 `accept_current`、审计 PASS 或立即恢复许可，不改审计配置、闸门、预算或其他 scope；§6.1 首次真实 build 的 live 续接与最终复核不变。

以下 SC 原有要求全部保留，并作强制补充：SC-3 须验证独立 EvidenceAcceptance adapter、所选 preview 与完整 TargetBinding，以及缺/错政策、拒绝选择、错对象、非 root/API 副本和仅信 locator 布尔均拒绝；SC-7 非作者坏实现须覆盖仅验政策索引布尔和以政策覆盖已知成功/未知运行反证，指定业务断言捕获，两个实际已观察 UI 布局各有合法正控；SC-10 严格复用两份既有真实问答，无须重签，派生政策 FileRef 必须进入恢复 evidence、闭包和历史重放验证，真实承重输入不齐仍阻塞。完成规范修订不等于正式审计通过。

## Success Criteria

| ID | 可证伪验收 |
|---|---|
| SC-1 | 真实 build 的 L−1/L 成功、L+1 指定容量错误；包括历史 prompt 复制复现、中文/转义导致 manifest 小而最终 JS 大的例子。超限时全 scope/run 树无新增/改写（含锁/目录/observe），含已有超限 pending 的容量拒绝，不先补 record 再称零写入；已发布 bytes 恰为被检查的唯一渲染结果。旧基线已对真实超限接受命中 RED；另保留同源旧 host 可精确 resume/补 record、仅源码变化即原有 E_SOURCE_DRIFT 的隔离对照，不把旧 host 正控当新 host 必须接受旧来源。 |
| SC-2 | checker 超限不发布 script/成功 prepare-record，正常 checker 及其真实错误路径保持；不夸称整次 prepare 零写入或已有 checker 恢复。 |
| SC-3 | 单次原生输入拒绝、真实 operator 声明、首 reserve/全部旧绑定及已知反证检查须同时满足。隔离 fixture 中验证静态 loader error 先于 run 创建；错窗口/hash/来源、small/等于L、错工具/绑定、重复、timeout/network、缺声明/错对象/变 head/非 root/模拟答复/API 副本均拒绝。真实问答封闭 adapter 可从原生 toolUseResult.answers 与 preview 派生绑定；合法非空 preview 不被旧耗尽处置 parser 误拒绝。已知第二 root 或不同关联脚本的成功/未知调用即使有签字仍否决，不宣称发现未提供、无已知线索的全平台运行。 |
| SC-4 | 原 reserve1→单一 dispatch_rejected→新 reserve2→真实结果的完整链可重放；同 scope/cycle，attempt 2/round1、预算不变、旧票/字段语义不变；取消记录不是审计结果。首次后继 build-record 必须绑定冻结 recovery_preflight；删字段、错 successor/head、缺 snapshot 须使 native/collect/check/history 的实际消费者拒绝，其他旧 build-record 不被要求补字段。 |
| SC-5 | 仅兼容清单的精确旧/new host 对与四项未变 source 可承接；其他变化拒绝；旧/new 同路径不同 hash 的双闭包正确读取，旧 genesis 不改，新结果的 collect/check 不断链。 |
| SC-6 | 同输入复用真实签字；首次提交前 head 变化过期。重复、证据冲突、并发与 event 前/后崩溃能命中指定分支；重复不加事件。恢复幂等返回前的反证仍拒绝；另从合法 seq2 起点在 root 尾追加关联成功/未知调用或引入已知第二 root 后，**不再调用 recover、直接普通 build**，须以 recovery_handoff_counterevidence 拒绝且零新 reserve，不能仅因参数/事件/容量不合法而红。capture后/reserve前变动被最终复核拒绝；无关尾追加允许首次续接；合法 attempt2 运行后的 pending resume 只返回原冻结准备物、零新增/零重派，旧历史离线 check 不因 live 增长/移除而恒红；普通耗尽/终态/未知资源仍阻断。 |
| SC-7 | 非修复作者构造至少四类坏态：检查太晚、量错 manifest、未知错误误解锁、错绑定/伪原生证据；另构造只验 locator 布尔、漏真人来源、签字覆盖反证、幂等早返回的坏实现。续接另须分别捕获删除 build live capture、reserve 最终复核只读旧 snapshot 的坏实现，从 seq2 直接 build 命中指定业务断言。坏实现编译并进入指定业务断言后才算 CAUGHT；每类先以合法对照证明可过，回归与类型检查有 judged 明细。 |
| SC-8 | Rule6逐hunk判性质；纯代码/描述性部分有 baseline-failing substitute；若产生运行时AI指令改动则照跑AB场景1，description改动另4b；失败/SKIP/not_judged不作通过。 |
| SC-9 | 版本、CI gate、指针门、本地子模块merge及双推逐SHA、主仓post-merge gitlink有实际证据；旧原件/预算保留，安装缓存/覆盖边界如实说明。 |
| SC-10 | 已发布修复对真实原准备物 check-only/实际恢复成功，严格 adapter 复用既有真实声明而非重签，原规划审计产生经check的合法终态；新推荐机制仅PhaseA完成、实现任务仍pending；修复本周期归档/handoff/claim尝试等Phase D后置交付齐全，不以合成fixture代替真实调用；这些后置动作不是归档前功能tasks的完成条件，按tasks.md独立义务实际执行后才补SC-10的周期收尾证据，不能提前勾任务或放宽归档门。若真实承重输入不足则如实阻塞，不伪造成功或要求 AI 代签。 |

## Impact / Risks

主要风险是把“缺证据”误当“确定没执行”、把机器可核事实与人类有界声明混为全称证明、把源码更新伪装成同一来源、只改局部 loader 导致历史重放接缝断裂，以及为过容量删审计内容。恢复协议字段、来源隔离和拒绝表见 [design.md](./design.md)。本期 source 承接只解决第一条未运行 reservation，不能泛化到任意活动审计。声明是已由产品接受的有界可信输入，不是密码学证明；本机不能发现的域外行为不被包装成已经扫描或强制隔离。

规范/实现/验证/发布按既有十步循环执行。UPM若未配置不新建；各 checkpoint 读实际配置，off不伪造PASS。技术细节由AI按可证伪依据收敛，新增产品范围/安全姿态变化仍回owner；当前授权不含这些扩张。

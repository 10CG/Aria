# 派发前容量拒绝恢复 — 技术契约

> 状态：实施中（post_spec R5真实accept_current、规划R5合法OSCILLATION末轮PASS，均converged=false）；与 proposal/tasks 同属本次交付面，不是 append-only 审计流水。原票/处置证据留 reports/notes；按已审计划进入B.2测试先行，不改变原票或宣布收敛。

## 1. 有界选择

选择在 canonical executor 增加 `recover-dispatch-rejection`，而不是另造未冻结 host。仅支持 **genesis + seq1 reserve、round1/attempt1、没有任何其他事件** 的主审计准备物。只有原生 Workflow 文件容量输入拒绝是 v1 原因，canonical token 为 `workflow_input_file_too_large`。后续轮、checker、已有 commit、未知活性、其他错误均不在本入口范围。

真实目标是现有 `state-scanner-goal-aligned-recommendations/post_planning` 的首个 reserve。它不是本修复 Spec 的审计；本修复照常另走 post_spec/post_planning，不借此重置目标的预算。恢复为 **operator-assisted 本机交互动作**：原生容量拒绝记录与本机静态依据、真实操作者有界历史授权域声明、独立单对象证据接受政策、当前唯一首 reserve/全部旧绑定及已知反证检查四项缺一不可。没有全平台自动隔离或全局历史未运行证明；无人值守不得由 AI 生成声明，本期不增加或改变 v2 正常业务的人类节点。

## 2. 最终程序容量

`MAX_WORKFLOW_SCRIPT_BYTES = 524288`，不提供配置/CLI覆盖。衡量对象是 renderer 返回的最终 bytes，不是 manifest 文件大小、prompt 长度或“预计压缩后大小”。

主 build 顺序：

1. 读取/验证 manifest、固定配置及路径形状，计算 scope/run locator（仅计算，不 mkdir）。
2. `program = _workflow(manifest, sha256(manifest_raw))`；如 `len(program)>L` 报 `E_WORKFLOW_CAPACITY`，stdout 为空，stderr 为现有 ExecutorError JSON；reason 给实际 bytes/limit，不能含 prompt。
3. 才进入 `_writer_lock`，执行原来源/历史/pending/资源/政策/写入流程。
4. 若创建新 reservation，直接发布步骤2的 `program`，不再渲染一次。**来源兼容且最终脚本不超限**的普通精确 pending 仍只恢复/返回原准备物，必要时按原规则补齐缺失 record；不新增 reserve、script 或派发。

超限诊断先于 scope 来源漂移/预算等历史诊断；它只做无写入拒绝，不授权任何派发。健康尺寸输入仍须通过原全部检查。本次不承诺任意旧来源的超限 pending 能在新 host 普通路径恢复：现有 build 已在 `_resume_build` 之前按六源逐 SHA 拒绝源码变化（1820–1833行），旧 executor 的超限准备物因此本就不能跨本次源码变更普通 resume；本契约唯一旧→新承接又先用 rejection 清除该旧 pending。新 host 的所有新 reserve 必须先过固定 L 检查，故健康实现不能产生来源兼容而超限的 pending。本期不为该不可达健康状态新增绕容量分支；只在旧执行器/来源仍匹配时成立的历史 resume 正控，不是新 host 的可用性承诺。

已有超限 pending 不会自动解锁：符合第1节首轮条件且两项 authority 齐全者才走独立恢复；已有 runId、未知活性、非首轮或其他来源的旧对象保持既有阻断，不以容量修复扩大来源迁移。SC-1 的超限零写入仍适用于所有被本 host 容量前检拒绝的调用；不会通过先锁写/补 record，再称无写入来满足它。

同一个纯容量检查也位于 checker 新脚本的**发布之前**。不把检查嵌进纯 renderer：历史重建仍可得到旧原字节。checker 已有 request/blobs 可能保留，不能承诺整次 prepare 零写入；但超限时不得发布 checker.js/成功 prepare-record，更不能生成假 checker 结果。checker 恢复保持现有协议，本期不新增其重试入口。

## 3. 原生证据、真人声明与信任边界

### 3.1 输入与可定位性

CLI 接收 repo、原 manifest/build-record、实际原生 root tool transcript locator、目标 `tool_use_id`、`operator_index` 的 FileRef；有 `--check-only`。输入路径/hash仍走稳定读取与安全路径规则，不允许执行日志/历史脚本。禁止将 controller 摘录、截图、业务 Markdown、普通 error JSON 当充分证据。`operator_index` 是 locator，不是带 `approved=true` 的授权令牌。

原生来源必须来自当前运行时配置目录下的 root transcript namespace（`projects/<project>/<session_id>.jsonl`），不是仓内任意伪装文件。配置根为宿主启动环境 `CLAUDE_CONFIG_DIR`（非空时）或 `Path.home()/'.claude'` 的实际绝对路径；输入原件的祖父目录须为该根下 `projects`，filename须为selected sessionId加`.jsonl`，禁止符号链接或repo内伪原件。CLI不提供“可信根”覆盖，AI也不得临时改该宿主环境来使证据通过。selected rows 的 cwd 必须等于本次 repo 实际根，isSidechain严格为false，sessionId必须相同并与原件文件身份一致。平台实际locator由现有工具返回的存储位置发现，不为此猜测远端API或执行未公开模块。隔离测试可在子进程启动时设置测试HOME/配置根，不改生产环境。离线重放按事件已冻结的runtime_config_root/原件身份与snapshot校验，不重新读取live原件或假装跨容器存储已齐。

这里继承已有本地原生记录的信任模型：防错误来源、业务字符串冒充与错绑定；**不声称抵御能改写宿主可信原生存储和执行器代码的同权限恶意主体**。哈希和格式不是平台密码学签名。测试模拟可信存储只能放在隔离 HOME/运行时环境，不写生产原生目录。operator 的授权域声明是产品明确接受的有界可信输入，不由上述哈希推导为全局事实。

### 3.2 唯一肯定输入拒绝

从完整、稳定读取的 UTF-8 JSONL 中选定两条完整记录。原始行 SHA256 对去掉末尾一个 LF 后的原行 bytes 计算，不重新序列化；若有 CR则保留。以下条件**全部**成立：

- request：root assistant 记录，包含唯一匹配 id 的 `tool_use`，工具名严格 `Workflow`；input 恰含 `scriptPath` 与 `args`。
- `scriptPath` 串恰为该 build 记录绑定的绝对脚本路径，原文件/冻结 closure 的 bytes/hash一致；实际最终 bytes 必须 `>524288`。
- args 恰为该 build 的 identity 和 manifest_sha256，identity 的六字段与 manifest 完全相等，无额外覆盖。
- response：root user/tool_result，`is_error is True`，tool_use_id 精确相等；parentUuid/sourceToolAssistantUUID 精确指向该 request UUID；两条 timestamp 有效且先后不倒置。
- content 类型为 string，恰为 `<tool_use_error>Workflow script file {scriptPath} exceeds 524288 bytes</tool_use_error>`，不接受子串匹配、任意换因、timeout或业务报告引用。
- 选定响应/关联结构没有 runId、taskId、native run 或启动成功的矛盾信号。重复、不配对、成功或未知关联调用均拒绝；不得把未配对请求的缺回执解释成未运行。

此次输入拒绝的执行顺序依据为本机分发程序**静态取证**，不是执行私有模块。来源为 notes 下 `runtime-capacity-source-windows.json` 与 `runtime-loader-to-call-static-evidence.json`，二者记录 binary SHA256 `708c77b204db30086ff6f1ed34577bda03e1be74ced80557cbf7b54249ebf0bd`。只使用下列半开 byte windows，不把其他二进制字符串命中当控制流依据：

| 环节 | offset 范围 `[start,end)` | window SHA256 |
|---|---|---|
| `p9n` 文件读取/超限错误返回 | `[304476230,304478630)` | `fd742347a3860917357f75700ac6c536f4beec15ffa72c11b5c1a6dea8528ab0` |
| resolver `_r` 传播 `p9n` 的 error | `[315302860,315303700)` | `f9ec9f4607472d5cb24e512f8fe5487a24e1867d34d853e08bd5514528ec388d` |
| Tool call 在 `_r` error throw 之后才生成新 runId | `[315310362,315315900)` | `f1515c786e76998c5eb220cdbed29a03b2d7fa7a959753397a678ffd29eacf02` |

宿主验证、冻结这些实际 window bytes/指纹及原生 request/response 的版本字段；v1 仅识别本次 `2.1.318` 布局。依据记录的 `kind` 必须分别为 `static_distribution_bytes_not_executed`、`static_only_no_private_module_execution`，不是自填的顺序布尔。字节、窗口映射、原生版本或控制流依据不符/缺失时拒绝。`524288` 的此次错误字面值从原生响应核对，构建 L 独立固定；不从空的 `constant_bindings` 或无关字符串猜常量赋值。固定窗口只证明已取证的本机静态拒绝路径，**不证明历史调用执行映像与该 binary 相同**；当前 PID、版本或这些窗口均不能补证历史身份，也不要求取得不可达的历史 binary 身份记录。该项未独立验证的不确定性只按下述单对象政策接受；不运行私有函数、不假造历史指纹。

#### 3.2.1 单对象证据接受政策及独立 adapter

除 3.3 的 operator 声明外，恢复还必须验证以下独立 authority，二者均必需且不可互相替代。owner 于 `2026-11-09T14:40:55.778Z` 在真实 root `AskUserQuestion` 选择“接受此边界，继续恢复”，仅为这个旧对象接受 `historical_executable_identity_not_independently_verified` 残余不确定；不是 `accept_current`、审计 PASS、立即恢复许可，也不跳过启用的审计、实现测试或发布。旧独占声明不等于此政策。原生精确容量拒绝、本机静态窗口、旧六源/对象/head/双闭包及所有已知反证仍须逐项验证；成功或未知关联运行一律否决，不可由政策覆盖。

CLI 增加 `recover-dispatch-rejection --evidence-acceptance-index PATH`，宿主稳定读取该 locator/index 文件并计算其 FileRef；仅与实际 TargetBinding 相同的旧目标准入，其他 scope 不得借用该政策，caller/config 无全局开关。本次已有 locator 为 `.aria/notes/2026-11-07-executor-pre-dispatch-recovery/historical-evidence-acceptance-owner-decision.json`，不是程序必须信任的业务目录。以下是独立封闭 schema，类型、Hash、FileRef、NativeSource、TargetBinding 与 3.3 相同，未知键拒绝，整数不得为 boolean：

```text
EvidenceAcceptanceIndex = {schema_version:1, adapter:"historical_evidence_acceptance_20261109_v1",
  target:FileRef, question:{path:string,line:integer,uuid:Id,line_sha256:Hash},
  response:{path:string,line:integer,uuid:Id,line_sha256:Hash}, tool_use_id:Id}
EvidenceAcceptance = {schema_version:1, sourceData:{
  adapter:"historical_evidence_acceptance_20261109_v1",
  decision:"accept_boundary"|"retain_threshold",
  policy:"accept_native_capacity_rejection_with_local_static_basis_and_prior_exclusive_operator_statement_for_this_target_only",
  residual_uncertainty:"historical_executable_identity_not_independently_verified",
  counterevidence_policy:"veto", target:TargetBinding, target_locator:FileRef,
  source:NativeSource, question:{uuid:Id,line:integer,line_sha256:Hash},
  response:{uuid:Id,line:integer,line_sha256:Hash}, tool_use_id:Id}}
```

locator 可机械归一化：`target` 原样作为 target FileRef；`native_source` 填两个 path；`question`、`response` 的 line/uuid/line_sha256 分别映射对应字段，`question.tool_use_id` 映射 tool_use_id，adapter 固定上述值。原 locator、归一化索引均冻结；locator 的 selection、policy、residual_uncertainty、摘录和任何布尔都不是 authority。原生 question UUID `8533a12c-0b60-412b-bbe5-510b4c632ccf`、line 6090，response UUID `cd87f711-e516-4657-857b-258048675e7c`、line 6095，tool id `call_7dde52c13035418fa2013a89ec422c38`；原行 hash 和 target FileRef 从 locator 取，不能补造字段。

新增 `_parse_evidence_acceptance` 复用 3.3 的可信 root namespace、稳定读取、原始行 hash、唯一 root assistant/user、同 session/cwd、tool_result 与 parent/sourceToolAssistantUUID 配对、顺序和错误检查；禁止 sidechain、API envelope 副本、普通 user 同文或仅验索引布尔。恰一题且 `multiSelect=false`；真实 `user.toolUseResult.questions` 与 request questions 逐值一致，`answers` 恰以原 question 为唯一键且值恰匹配唯一 option，`annotations` 恰该题的 `preview` 字段且与真实选中 option.preview 逐字相等。完整 question/header、两个 option 的 label/description 和 preview 固定说明，须匹配分发代码按本次已观察 UI 固化的封闭模板；只有 preview 的 change_id/checkpoint/reservation SHA/script SHA 四值由实际 TargetBinding 填入。locator **不提供模板或允许值**，不能以“真实问答等于 caller locator 摘录”替代上述语义核验；程序仍须重读原行。中文选项仅窄读取 alias：“接受此边界，继续恢复”→`accept_boundary`，“保留门槛，保持阻塞”→`retain_threshold`，后者及不匹配直接拒绝、不生成肯定政策。机器输出字段及枚举只用英文 canonical。

从真实选中 preview 精确解析 change_id、checkpoint、reservation sha256、script sha256，逐项匹配旧原件；再按 3.3 对 identity 六字段、attempt、genesis、reservation、head、manifest、script 完整重算 TargetBinding，与 operator 声明和 target FileRef 独立相等，并锁内复核唯一当前 head。宿主自行派生 EvidenceAcceptance 并冻结；caller 提交同形输出不能代替问答。重放从冻结的原生 snapshot、locator、target 和索引重新派生验证；相同原件复用已观察签字，不要求重签。幂等 key 同时包含此 question/response UUID、tool_use_id、两条原行 SHA 与 TargetBinding；先按 3.5 扫描当前已知反证，再可返回既有事件。后续 §6.1 的真实 build live 续接门及最终复核原样保留。

测试须以实际观察到的两份 root UI 布局分别作合法正控：3.3 的三选项声明和本节两选项政策，均从原生 questions/answers/annotations.preview 派生而非拿 locator 摘录作原件；并覆盖缺/错政策、错对象、拒绝选择、API 副本、只验 locator 布尔、以 caller locator 自选错误语义模板及用政策覆盖已知成功/未知运行的坏态，负控须命中对应业务拒绝。

该本机来源识别沿用可信原生存储与分发代码的 TCB 假设，不是密码学运行证明。机器核验的是**这次调用已记录的容量输入拒绝**；旧准备物的受控闭合还必须同时具有独立证据接受政策、独占操作域声明、全部旧绑定与已知反证检查。不得将此闭合表述为已独立证明历史映像或所有运行活性；不能据此排除此前其他版本/机器/脚本的关联运行。不再要求 ASCII/inline 字符不可执行性，不生成全历史或未来不可运行证书。无 runId、无 index、空 call 集合、本地超限 stat 只能作辅助信息，未知错误保持 pending。

### 3.3 真实 operator 来源验证与逐字段派生

实现宿主为 canonical `audit_executor.py` 新增的独立 `_parse_operator_recovery_statement`，复用稳定读取、路径/FileRef、原生记录解析和冻结设施。已有 `executor-contract.md` §10.3/§10.5 与 `_parse_human_disposition`（现有源码3507–3616行）提供真实来源验证先例，但**不能直接调用它并宣称适配完成**：它绑定耗尽结果、固定三类 action、`audit-disposition-context=`，且要求 annotations 为空；此次对象是 reserve，真实问答带 preview/非空 annotations。保留旧 parser/处置政策，不放宽为任意 user 文本；新增 adapter 由代码与测试承担。

封闭输入 schema：

```
OperatorIndex = {
  schema_version: 1,
  adapter: "operator_boundary_20261109_v1",
  target: FileRef,
  question: {path:string, line:integer>=1, uuid:Id, line_sha256:Hash},
  response: {path:string, line:integer>=1, uuid:Id, line_sha256:Hash},
  tool_use_id: Id
}
TargetBinding = {
  identity: <manifest 六字段>, attempt_index: 1,
  genesis: FileRef, reservation: FileRef, head: FileRef,
  manifest: FileRef, script: FileRef
}
OperatorStatement = {schema_version:1, sourceData:{
  adapter:"operator_boundary_20261109_v1",
  decision:"confirm_local_domain"|"decline"|"require_global_fencing",
  authorization_domain:"root_session_and_explicit_delegations",
  transfer_state:"not_authorized_or_transferred",
  recovery_scope:"local_interactive_legacy_recovery",
  counterevidence_policy:"veto",
  target:TargetBinding, target_locator:FileRef,
  source:NativeSource,
  question:{uuid:Id,line:integer>=1,line_sha256:Hash},
  response:{uuid:Id,line:integer>=1,line_sha256:Hash},
  tool_use_id:Id
}}
NativeSource = {original_locator:string, runtime_config_root:string, snapshot:FileRef}
```

已有 `operator-assisted-boundary-owner-decision.json` 不必改写为新授权文件。宿主的 locator adapter 可将其机械归一化为 OperatorIndex：`exact_target`→`target`，`native_source`→question/response.path，`native_binding.question` 的 line/uuid/raw_line_sha256→question 的 line/uuid/line_sha256，`native_binding.answer` 同样映射到 response，`native_binding.question.tool_use_id`→tool_use_id，adapter 使用上述固定枚举。原 locator 与归一化数据都冻结；selection/authorizes/tool_use_result 摘录不提供 authority，仍重新读取真实 root 的 toolUseResult。索引生成不等于新签字，也不要求 owner 再答一次。

全部键封闭、类型严格；Hash 为完整 SHA256，整数不接受 boolean。`OperatorStatement` 只由宿主生成并纳入 closure，caller 不能提交它代替原件。只有 `decision=confirm_local_domain` 生成准入声明；其他选择直接拒绝，不填肯定 transfer_state。各字段的派生/拒绝条件为：

| 输出/条件 | 实际输入及确定规则 |
|---|---|
| `source`、两事件定位 | 从可信 namespace 连续两次完整读取一致的原生文件生成 snapshot；逐 LF 行定位，UUID 在 root 记录中唯一、行 hash 精确相等。先限定顶层 `type=assistant/user`、`isSidechain=false`，再检查 message.role/cwd/sessionId；不递归进入 `api-request-blob` 或其他 envelope 搜索 authority。 |
| question/response/tool 绑定 | question 须有唯一真实 `AskUserQuestion` tool_use；response 须有唯一相应 tool_result，`is_error` 不为 true，`parentUuid=sourceToolAssistantUUID=question.uuid`，`tool_use_id` 精确相等；同 session，先问后答。唯一性只在真实 root record/tool blocks 上计算，不把嵌入 API 请求的拷贝算作第二次真人回答。 |
| `decision` | 恰一题、`multiSelect=false`；真实 `response.toolUseResult.questions` 与 question.input.questions 逐值一致；`answers` 恰以原 question 文本为唯一键，其值精确匹配一个封闭 option label。不从 tool_result 展示字符串、普通 user 文本或索引 selection 推断。 |
| domain/transfer/scope/veto | 仅由该封闭 adapter 的完整 question、三个 options 的 label/description/preview 与真实选择共同派生；不是 NLP 猜测或 caller boolean。确认选项明确断言未另授权/转交，且成功/未知反证否决。缺一、添项、交换映射或模拟答复均拒绝。 |
| `target` | 用真实选中 preview 的 change_id/checkpoint/reservation SHA/script SHA，匹配原 reserve、build/manifest/script/closure 和 genesis；首 reserve 的完整 hash 传递绑定其 identity、manifest、script 及 genesis。锁内另证明它就是当前唯一 head，故 `head=reservation`。不要求尚不存在的签字字段，却不允许用索引替代这些匹配。 |
| `target_locator` | 解引用 `OperatorIndex.target`，核完整 FileRef；其 identity/genesis/reservation/current_head/script/script_bytes/initial_max_rounds/已知工具对必须分别与实际旧绑定一致。`kind` 的历史描述、`no_recovery_executed`、owner 索引的 selection/authorizes 都不是判定事实。 |
| preview/annotations | 此 adapter 仅接受真实已取证布局：确认 option 的 preview 与 `toolUseResult.annotations[原 question].preview` 精确相等，annotations 恰该一个键/preview 字段；不套用旧 parser 的 annotations={}。preview 内中文说明与 `reservation sha256`/`script sha256` 为封闭读取 alias，机械映射到英文 canonical 字段，禁止宽松 substring/任意翻译。 |

本期 adapter 是对**已有真实声明**的窄迁移读取，不建设通用提问模板或新授权 UI。与3.2.1相同，question/header、三个 option 的 label/description 及 preview 固定说明由分发代码固化，仅四个目标值由实际 TargetBinding 填入；caller locator 不是模板或语义白名单。其封闭匹配样本必须来自以下实际 root 原行，不从 API 请求副本重新制造。机器字段/枚举均为上面的 English canonical；当前中文三选项仅此 adapter 可读，不把本仓中文模板规定给其他项目。

- 原生 root 路径：`/home/dev/.claude/projects/-home-dev-Aria/ef6094a0-96c0-4895-bee8-412d5d0b24f3.jsonl`。
- question：line `5026`，UUID `71846169-0a0a-41a7-9a55-ef6cc7201d8b`，原行 SHA256 `bed8a564d51d470fadb6f69cb8c689ca1d737893cfa9cb5cdc60dbb91b993319`。
- tool_use_id：`call_ea18554d89c6447f86a831117ab62af1`。
- response：line `5033`，UUID `09c1c721-bb5f-412f-996e-9bd0462cf6b3`，原行 SHA256 `a1289d0d34fff56cd6c0e0c525a64d7ecbf2476e80870618dd5c45e738a38018`；timestamp `2026-11-09T10:23:41.871Z`。
- 三个 label 的封闭映射：“确认唯一，采用交互恢复”→`confirm_local_domain`；“不能确认，保持挂起”→`decline`；“仍要求全自动全域证明”→`require_global_fencing`。这里只登记已观察映射，不能给其他文本推定授权。
- target FileRef：`/home/dev/Aria/.aria/notes/2026-11-07-executor-pre-dispatch-recovery/operator-recovery-target.json`，SHA256 `184bba8c75fd2eaf6aa34554b5f99292a832cf2f8cd90ee34a228f09f61a2b80`。该文件也只是被核对的输入，不是可信布尔。
- 目标六字段：audit_cycle_id=`post-planning-state-scanner-goal-aligned-recommendations-2c1b8f1cac3e4f63a36a434869bb8d32`，checkpoint=`post_planning`，change_id=`state-scanner-goal-aligned-recommendations`，client_round_id=`post-planning-r1-d9013c9410d54e23a1da62ded463a2cf`，candidate_sha=`012fc3927bc6587da15d0ddc6e92a19086e668fe`，round=`1`；attempt_index 从原 reserve/build 重算为1。
- ledger 目录：`/home/dev/Aria/.aria/audit-reports/_executor-ledgers/b164be9323efe2ca66551beb758dce367a8dc3cdddcddd358d8a8bf6f4f85521/`；genesis.json SHA256 `b5f1150848793ee009d65337b414c8b023c0b5b0b1fa1567653671e6d55defdd`，reservation/current head 均为 `events/0000000001.json`、SHA256 `d216da3207d8210869a01d6fa0068cb4e52b7c24c7ccd169fbc95aac2a24f2c2`。
- 原 script：`/home/dev/Aria/.aria/audit-reports/post_planning-R1-post-planning-r1-d9013c9410d54e23a1da62ded463a2cf-state-scanner-goal-aligned-recommendations/workflow.js`，SHA256 `dd23a303125c031c51e70f6d74c0852069f47e4977b68921131979c52bc2aad9`，570716 bytes；initial_max_rounds=5。目标已知原拒绝工具 id=`call_470145c1f5bc4f458a5d5888227dfcb1`，request UUID=`018ed58a-19d7-4a5b-8ebd-9839e469f1d8`，response UUID=`2b57abae-25c8-47dd-b723-b8fbc2632946`。

真实原行/结构与这些绑定不符即拒绝，不能因文本相同或已有产品授权而 override。隔离测试将该已取证布局放进测试可信存储，测试 adapter 的结构与派生规则；生产来源校验仍须实际 root，不把测试 fixture 当授权。不能仅因旧问题没有新定义的 context marker 而要求重签：以上 reservation/script hash、唯一首 head 和旧绑定已提供可核传递绑定。若实现实读发现缺失/不匹配的承重字段，必须报出具体字段并保持 pending，不补造、不自行再问 owner、不宣称 SC-10 已解决。

### 3.4 全部旧绑定、已知反证与证明量词

首次 mutation 前，锁内重放整个实际事件前缀：只能是原 genesis + seq1 reserve，head 完整 FileRef 与声明绑定完全相同；原 manifest/build-record/script/input_closure、identity、attempt、cycle_origin、原预算及源映射逐项按原机制验证。`known_binding_sources` 是本次实际读取这些原件及已存在原生索引的 FileRef 去重排序清单，由宿主生成，冻结后重放重新推导，不接受 caller 声明“检查过”。不存在的运行后 index 不提供未运行证明。

已知原生来源至少包含：原拒绝、operator 问答及 evidence acceptance 问答所在 root，原准备物/闭包/已存在运行后索引明确引用的原生 locator，以及 caller 显式提供的其他已知 root（`additional_sources`）。§6.1 首次续接的来源集合亦必须包含这两项 authority 的 root，不因二者共用同一 root 而省略任一原行验证。这些输入中若出现明确指向其他相关原生载体的 locator，必须继续读取并冻结；已知相关载体缺失、无法读取、无法归属或未配对时拒绝，不能从清单静默剔除。除此之外不扫描全平台、猜测远端 API 或声称穷尽所有 session。

**通用旧式 locator 与 typed 引用的消歧**：`native_record` 位于通用结构化归档或完整 native carrier 时，缺键/null 维持“没有此链接”语义，不证明未运行；dict 仍须是精确 `{path,sha256}` FileRef（保留原 carrier-relative path 与原 expected hash 校验），非 null 的其他类型拒绝。string 是必须追读的旧式 Workflow export locator，**不是可以略过的散文**：仅允许 Linux 规范绝对路径 `s.startswith('/') and not s.startswith('//')`，不含 U+0000–U+001F/U+007F，且 `s == str(Path(os.path.abspath(s)))`。不 trim/resolve/展开变量或 URI，不猜相对 string 的基准，不按扩展名判定。新增 string 入口在 live 阶段拒绝本体/祖先 symlink；Frozen 阶段只从已验证 origin 映射读取，缺叶子拒绝，不访问 live 检查路径。由实际绑定的 schema/callsite 决定 typed 角色：audit index、workflow drift index、preflight observations、result inputs 等已声明 FileRef 的位置仍严格 FileRef，generic union 不得泄漏到它们；首次恢复和已提交 rescan 均须守同一边界，合法 tool_error null 分支不变。

对合法旧式路径，用当前 inputs 稳定读取并由宿主捕获 path/实际 bytes/hash，随后汇入与 FileRef 相同的 native 解析、关联、termination 与递归路径；不能改旧归档补 hash、用 caller hash 或当前字节替换已有 FileRef 的 expected hash。每份 Workflow export 必须能归属为 object、非空 runId:string、args:object、script:string；外层声明 workflow_run_id 时仍须精确相等。target_context=false 也继续追读反证及兄弟字段；native/typed active-ancestry 真环拒绝，独立分支重复 DAG 不误判环。缺失、坏 JSON、未知归属或关联成功/未知运行继续拒绝。新追读的全部叶子进入既有 known_binding_sources/闭包及实际 read_origins 精确消费校验；不增加持久 schema 或全平台扫描，不声称现有 root 队列去重已证明全图无环。

在以上完整载体内检查全部旧关联：相同脚本逻辑路径或脚本 hash、manifest SHA、旧 client identity，以及同 cycle 的其他 Workflow 调用。关联不以“具有合法 build 资格”为必要条件；另一段代码/平台只要具有这些关联，同样会构成反证。只有选定的精确输入拒绝可被本事件闭合；其他成功、有 runId/taskId、无回执、未知活性或相互矛盾的调用均否决。无关消息不否决。签字不把 unknown 改为终态，不授予取消权，也不允许以另一脚本不合规为由忽略已知运行。

因此，机器核验的是原生容量拒绝记录、具体旧状态和已知输入内不存在反证；人类分别提供该历史对象未另行授权/转交的有界声明，以及接受未独立验证历史映像身份的单对象政策。两项 authority 与机器核验共同支持本机这一个旧准备物的恢复，不声称发现没有已知线索的域外行为、全历史无运行或阻止未来裸 Workflow。writer.lock 只是本 scope 事务锁，不是平台派发锁。

### 3.5 冻结、签字新鲜度与幂等来源

首次验证时将实际读取的完整原生载体 snapshot、静态依据、target/index 和派生证据冻结，保留 original locator、完整 carrier SHA、selected UUID/tool_use_id/行号/原行 SHA。相同载体可复用同一 snapshot；证据摘要从原件派生，不由 caller 自填成功布尔。

签字不因规范文字更新、check-only、无关日志追加或日期变化自动过期；目标输入不变可复用。首次提交前 head/reservation/script 或其他 TargetBinding 变化即过期，check-only 不预留有效性；锁内必须再核 head CAS。唯一例外是已有**完全同一** dispatch_rejected：可依据其 previous_event 重验签字原 head，只确认已经发生的那次提交，不授权任何新动作。若 head 已推进到其他事件（包括合法 attempt2），本恢复 CLI 不再返回 eligible/旧成功，而报告目标已过期；该合法后续历史仍可离线重放，不把它认作非法重复派发。

幂等 key 是 `(reservation FileRef, 原拒绝 request/response UUID、tool_use_id、两条原行 SHA, operator question/response UUID、tool_use_id、两条原行 SHA, evidence acceptance question/response UUID、tool_use_id、两条原行 SHA, TargetBinding)`；不是活跃 journal 整体 hash。重复调用时，两份独立 authority 的原已冻结载体必须是当前同 locator 原件的字节前缀、选定原行不变；仅追加无关消息可复用旧 snapshot/签字。不同 locator/工具对/行内容、截断或前缀改写拒绝。additional_sources 与 known_binding_sources 的精确清单同样属于输入。

**任何幂等短路之前**，重新稳定读取当前已知输入、扫描完整载体及新增已知载体的关联反证，再判断是否是同 key。即使新增载体导致输入不再相同，也先检查其反证；发现成功/未知调用报冲突，不返回旧成功、不追加替代 event、不授新派发许可。新增无关来源也不冒充同一输入，而按输入变化拒绝。event 后发现反证不回写历史或假装撤销已完成事件；当前交互恢复及其续接必须停止，不能拿旧回执继续。本文不声称这个本机动作能自动拦截工具外裸调用。

离线 collect/check/replay 只使用事件冻结的输入与原前驱，不查询 live 日志或要求用户重复签字，故日志后续增长/容器来源缺失不会改变旧证据视图。CLI 重新提交则必须提供可读的 live 来源；缺失不能称同一输入。检查历史证据与此刻申请恢复是两个不同操作，不能混用其新鲜度规则。

## 4. 追加事件与普通字段语义

事件外壳继续为现有封闭结构：`schema_version,seq,genesis,previous_event,kind,payload`，顺序/hash链不变。新增 `kind=dispatch_rejected`，payload 的键固定为：

```
{
  "reservation": FileRef,
  "build_record": FileRef,
  "evidence": FileRef,
  "input_closure": FileRef,
  "source_transition": SourceTransition
}
```

`reservation` 必须是 seq1 当前 pending，build-record/manifest/script/closure 必须与该 reserve 相符。此入口不创建 genesis，不接收任意 prefix；真实 operator 声明及独立证据接受政策是第3节有界证据的一部分，不是人类 override。`evidence` 指向程序生成的封闭记录，键恰为 `schema_version,cause,source,session_id,request,response,script,runtime_rejection_basis,operator_statement,evidence_acceptance,known_binding_sources,additional_sources`，schema_version=1、cause恰为第1节token。source 是 NativeSource；request键恰为 `uuid,tool_use_id,line_sha256,input`，input为原两字段工具输入；response键恰为 `uuid,tool_use_id,line_sha256,error`，error是第3节精确原生错误串。script为原冻结FileRef。

`runtime_rejection_basis` 是程序验证生成的 FileRef，内容封闭为 `{schema_version:1,binary_sha256:Hash,native_version:"2.1.318",capacity_source:FileRef,loader_source:FileRef,windows:[{start:integer,end:integer,sha256:Hash}]}`；三个 windows 按3.2表顺序固定，source 指向含实际窗口字节的冻结静态取证文件。其 binary hash 仅标识所取证的本机静态字节，不证明历史运行映像身份；它不叫 capacity_certificate，也不携带全称不可执行断言。`operator_statement` 指向3.3的宿主派生 OperatorStatement；`evidence_acceptance` 是指向3.2.1宿主派生 EvidenceAcceptance 的必需 FileRef；`known_binding_sources` 为3.4的原件 FileRef 数组；`additional_sources` 为其他已知载体的 NativeSource 数组。closure 必须包含这些引用、两个独立 index/locator/target、完整原生 snapshots、静态来源及其传递叶子；重放验证实际字节、两项 authority 独立派生及目标相等，不能只信 evidence 字段。所有字符串/整数/布尔按原始类型严格验证，未知键拒绝；实现不得用 caller 自填 no_run/approved 或“没有搜索命中”代替第3节判定。

锁内重新验证 head 和输入稳定性，在原 scope 只追加 seq2 一个 event。该 event 同时清除指向 seq1 的 pending、承接经验证的 active sources；不另写“迁移成功”事件或改旧行。blob可以先封存，event 由既有原子/不覆盖发布机制作为唯一提交点。

| 量 | seq1后 | seq2 rejection后 | 下个新reserve后 |
|---|---:|---:|---:|
| reserve_count | 1 | 1 | 2 |
| committed audit attempt 数 | 0 | 0 | 0 |
| charged_rounds | 0 | 0 | 0 |
| effective_limit / remaining | 原值 | 原值 | 原值 |
| pending | seq1 | 无 | 新reserve |
| 新 manifest 的 attempt_index | — | 提示2，不派发 | 2 |
| 新 manifest 的 round | — | 提示1，不派发 | 1 |

`previous_round` 仍指最近有效审计结果（此例 null），`previous_attempt` 仍指最近 commit（含既有 void，此例 null），两者**不改指 rejection**。原 cycle_origin 仍是原 genesis FileRef。新 client_round_id/run-dir 必须全新；candidate_sha 按普通当前候选规则确定，旧候选/脚本不回写。rejection 不进入 `_apply_policy` 的 audit attempts/投票/结论列表，也不伪造 void；attempt序号依据所有reserve单调，不根据实际审计结果列表长度重编号。

事件数、审计调用数、有效轮数必须各自报告，不能笼统报“R1已审”。新 build 仍跑原 `_require_dispatch_policy` 和资源检查，拒绝本身不授予 Workflow 调用权。已有终态或支出预算不会被本入口重新开放；v1前置已排除有commit的scope，普通后续行为仍由既有政策裁定。

## 5. 精确源兼容，不覆盖初始身份

当前旧 host 指纹：executor `5b9a32e23d665e494a21dc002a1a8498db445462762fba52916ce79716333777`；contract `27e145e159e5b828e2c60d9a743ca8a0ea59bfb11560ce4f1e8783e2ed711920`，均来自发布2d8e223f原字节。

新增分发文件固定为 `references/pre-dispatch-recovery-compat.json`，无 caller/配置覆盖入口。封闭 schema：

```
{
  "schema_version": 1,
  "compatibility_id": "pre-dispatch-rejection-v1",
  "from": {"executor": "64hex", "contract": "64hex"},
  "to": {"executor": "64hex", "contract": "64hex"}
}
```

from 恰为上面发布旧对；to 由最终实际 executor/contract bytes **机械生成**。代码只引用清单路径而不内嵌自身 to hash，避免自引用hash。新代码/contract再改一个字节也必须重新生成并跑检查；不得手改hash迎合。未知 compatibility_id、任一配对不等、格式不闭合、清单stale均拒绝。

SourceTransition 的封闭键：`compatibility_id,compatibility_manifest,from_sources,to_sources,new_source_closure`。from/to_sources 均为六个 SOURCE_NAMES 的**逻辑来源**完整 FileRef map，而不是blob存储地址：from_sources恰为通过原input_closure校验的原build-record.sources，to_sources恰为本次命令从固定路径读出的实际六源；两者的config/defaults/convergence_algorithm/report_storage完整FileRef必须前后相等，executor/contract的旧/新SHA恰配清单。另须逐个证明：原build.sources的origin/path在旧闭包中有恰同SHA的bytes，且这些bytes与genesis.initial_sources对应的冻结blob字节完全一致；genesis blob FileRef仍按原存储路径/SHA验证，但**不与live逻辑路径要求相等**。所有逻辑路径都须符合原_fixed_paths规则，禁止仅删路径检查或仅比hash。guard仍true，原预算/anchor/policy_inputs不变。清单本身、当前源码和验证输入均冻结到新闭包，作为恢复事件证据。验收必须用现有生成器产生的“genesis blob + build.sources live”双身份数据，合法映射通过，改逻辑路径、改bytes或错绑blob均拒绝。

v1只支持上面已发布旧host到本修复host的精确配对，source_transition不可为null。此次恢复能力本身必然改变executor/contract；不另建设“同源码也已具备新入口”的不可达通用分支。未知旧版本、相同from/to指纹或不在清单的配对保持拒绝；普通未恢复scope仍按原固定源校验。

**双闭包是承重接缝**：旧 genesis/reserve/build通过原input_closure只读校验，当前源码用新的输入reader；不能把同 live path 的旧、新 bytes塞进同一 path→bytes cache。新scope视图须先验证事件链与恢复证据，再导出active sources；不能先用新live源码dereference旧initial_sources而误报，也不能干脆跳过来源校验。读取旧源码只作数据校验，不执行历史代码。v1无任何旧审计commit，因此不引入已投票结果跨版本聚合。

后续 `_load_scope/_replay_history/_HistoryGraph/build/_native_build/prepare/collect/check` 必须一致理解：初始身份永不变，只有已证明的首个rejection可导出active sources；普通源漂移继续原错误。新 result 自身冻结当前源、完整prefix及恢复证据。旧被拒绝的 build 永远不能被 collect 当成真实审计运行。

## 6. 事务、幂等与拒绝表

- `--check-only` 仅做完整验证并返回 eligible/would_append 等元数据；不锁写、不mkdir、不freeze、不生成实际event FileRef，不得称已恢复或已获派发许可。与 mutation 使用同一证据判定；输入缺失不能降为仅容量预览。
- mutation在既有scope锁内复核；scope缺失/格式不符先拒绝，不为错误请求创建新scope。无事件前缀不“补genesis”。首提交必须重新核对声明 target 与 live head，不能使用 check-only 时的旧判断。
- event前崩溃：保留可能孤立的证据blobs，原pending仍有效；同原输入重入只复用已有相同blob再提交，不创建第二套身份。event后/回执前崩溃：完成3.5的当前来源/反证检查、确认 head 恰为该同key event 后，返回既有event，不重复签字。不同payload撞同seq/FileRef报冲突。
- 同时两份恢复：一份最多发布seq2；另一份在锁内依据同key幂等或冲突，不再追加。完成恢复后由普通build单独创建attempt2，不把两步捆成一个无法重放的操作。
- 原manifest/script/record/closure字节不符、错误scope/cycle、事件缺口/分叉、非首个单reserve前缀、真实/未知运行、证据错配、来源不在清单等，均无恢复event；沿用既有来源/身份/冲突错误，新证据失败使用 `E_RECOVERY_EVIDENCE`。human记录缺失/错对象/过期/非root/模拟答复/API请求副本同样拒绝；错误给具体 reason/引用，不输出原生正文或 secret。异常不能变为PASS或空证据成功。
- 普通精确resume、source drift、预算耗尽、unknown资源、oscillation/terminal、collect半发布和checker错误分支须回归，不因新入口改变。新真人声明只用于本次恢复，不映射为 accept_current/increase_rounds/degrade_single，不减少任何审计域/门。

### 6.1 seq2 后首次普通 build 的强制 live 续接门

恢复 CLI 的冲突返回不写持久阻断状态，不能承担普通 build 的准入。新增检查必须落在同一 `audit_executor.py` 的真实调用链，而不是要求调用方先再次运行 recover。当前源码的宿主实际为 `build`（1793–1929行）、`_record`（1594–1600行）、`_reserve_build`（1778–1790行）、`_freeze_closure`（418–422行）、`_native_build`（2523–2612行）及 `_replay_history/_HistoryGraph/_resume_build`；不存在可直接委托的 `_record_build` 或 `_reserve` 函数。以下为须实现的接口，不声称现有代码已经具备。

**触发与输入**：新增 `build(..., *, recovery_sources:Path|None=None)` 及对应 CLI `build --recovery-sources PATH`。仅当锁内实际前缀恰为 seq1 reserve + seq2 dispatch_rejected、pending=null、reserve_count=1，准备创建 attempt2/round1 时，必须提供此输入；缺失报 `E_RECOVERY_EVIDENCE/recovery_sources_required`，不能沿旧路径继续。不是新增任意状态文件或 caller allowed 布尔。其他未恢复 scope 维持原参数语义。该首续接没有既往真实 audit 调用，其普通 `manifest.evidence.dispatch_preflight` 必须为 null；不拿现有 native-run 终态 preflight schema 冒充恢复源清单，不为这次检查追加 observe 事件。

```
RecoverySourcesIndex = {
  schema_version:1, recovery_event:FileRef,
  additional_sources:[string]  // 规范化绝对 root locator，排序、唯一
}
RecoveryHandoff = {
  schema_version:1, recovery_event:FileRef, prefix_head:FileRef,
  rejected_reservation:FileRef,
  successor:{identity:<六字段>,attempt_index:2,manifest:FileRef,workflow_script:FileRef},
  sources_index:{original_locator:string,snapshot:FileRef},
  sources:[{original_locator:string,runtime_config_root:string,
            baseline_snapshot:FileRef|null,snapshot:FileRef}]
}
```

字段封闭、类型严格，无 approved/no_conflict/timestamp 新鲜度令牌。prefix_head 必须等于该 seq2 FileRef，rejected_reservation 指向 seq1，successor 绑定本次实际 manifest 原字节与容量已检查的唯一最终 script bytes。清单只能增加显式已知 root，不能替换 seq2 已有来源；已有来源的 baseline_snapshot 为 seq2 冻结 snapshot，新发现的来源才为 null。sources 按 original_locator 排序唯一，实际集合由 seq2 的拒绝/operator/additional_sources、旧绑定中的原生 locator、输入清单及这些 live 载体里明确关联的 locator 递归推导；缺源、截断、旧前缀改写、无效 namespace、无法归属、未配对或关联成功/未知调用均拒绝。索引只是 locator 输入，不是其完整性的机器证明；不扩展为全平台扫描。

**非 root export 的基线绑定**：§3.4 通用旧式路径首次读取时由宿主捕获的非 root native export digest，也必须从 seq2 已验证冻结 capture 重建并接入首次续接的独立 live reader/helper；对已有非 root export 保持原 bytes/hash 精确绑定，不能现场新算 hash 把另一份合法无关 JSON 冒充同输入。当前已知 root 仍按原 snapshot 前缀规则容许无关尾追加，不把所有 root 整体 hash 固定。live 递归扫描、冻结 `_verify_recovery_handoff` 及最终 reserve 前复读须实际消费这些 export 叶子；新增可接受来源才由本次稳定 capture 固定。沿用现有闭包/读入映射，不为 export 新增 caller hash 参数或状态文件；已提交重入仍在比较来源/字节前优先检查当前反证。

**真实生产调用与发布顺序**：

1. 保留第2节容量前检；锁内 `build` 先按既有路径 `_load_scope`、重放冻结历史、验证 active sources/identity/预算与资源。不要把“重放 seq2 无反证”当成 live 检查。精确 pending resume 分支先单独处理，不进入新的派发门。
2. 在首次续接分支、任何新 script/metadata/closure/reserve 发布之前，调用新增 `_capture_recovery_handoff`。它以**独立、未灌入 view.frozen_raw 的 `_Inputs()`**读取当前清单和完整 root，按既定来源/关联判据核验旧冻结前缀、选定原行与全部关联调用，继续追读新 locator。无须再次调用 recover 或重新签字。关联反证报 `E_RECOVERY_EVIDENCE/recovery_handoff_counterevidence`；不可读/不稳定等给对应具体 reason。旧 policy 允许、资源空闲或无新 runId 均不能覆盖此拒绝。
3. 验证成功后才以 `_freeze_blob` 封存当前清单和 live 载体，并发布本次 run-dir 的不可变 `recovery-preflight.json`（RecoveryHandoff）。**不把新 root bytes 按旧 original_locator 写进 build 的 inputs.raw 或 view.frozen_raw**：旧 root 原字节继续属于 seq2 闭包；新字节仅以独立 snapshot/blob FileRef 进入 handoff。将该文件及 snapshot/blob 叶子按实际 blob 路径加入新 build reader，再由既有 `_freeze_closure` 纳入 attempt2 的 input-closure。这样不改六源/双闭包的旧逻辑映射，也不将同一路径的两个时间视图扁平覆盖。
4. 按原顺序发布已检查的 script/metadata、冻结 build closure，再调用扩展的 `_reserve_build(..., recovery_preflight:FileRef|None, inputs:_FrozenInputs|None, live:_Inputs|None)`。在上述首次续接条件下，这三个内部参数缺一即拒绝；helper 从冻结 handoff/实际 state/manifest/script 重算绑定与无反证，不接收 caller policy_ok。**紧靠 reserve 的排他发布之前**，用 live reader 再稳定读取清单及全部已检查 root，要求与捕获 bytes 完全相等；有变化则拒绝本次预留，不使用已变旧的 handoff。保持原 reserve payload/事件外壳，成功仅新增一个普通 reserve。该复核是本机有限观察，不声称 writer.lock 锁住原生日志或阻止最终观察后的外部裸调用。
5. `_record(..., recovery_preflight:FileRef|None=None)` 为这个首次续接的 build-record 增加且仅增加 `recovery_preflight:FileRef`，绑定上面固定 run-dir 文件。普通记录保留原封闭键集，不能给所有旧记录补 null。条件 schema 必须在 `_record`、`_native_build`、`_HistoryGraph` 的 build 分支和 `_resume_build` 中一致实现；需要该字段而缺失、非该路径却夹带字段、指向其他 successor/head、缺 snapshot 或无法重算均拒绝。

**冻结重放与幂等分工**：新增纯 `_verify_recovery_handoff` 从该 build 的已验证 closure 取得 handoff、清单 snapshot 和全部载体 snapshot，重推来源集合、前缀/绑定及关联判定；不只检查 handoff 文件 hash 或自报清单。`_native_build` 在 build closure 校验后调用它；`_HistoryGraph` 为 handoff 增加封闭结构边并读取 snapshot 叶子，`_replay_history` 校验首次后继 reserve 与该 handoff 的对应关系。未提交的 pending attempt2 经 `_resume_build` 从固定 run-dir 的冻结 handoff 复算并恢复同一 record，record 丢回执/缺失不要求重做 live 派发许可；仍仅返回 resume_only，零重派。不能把 live 读取塞进 `_native_build` 或普通历史重放，使旧结果随日志增长变化。

首次后继 reserve 已存在后，scope 不再满足 live 门的触发条件：相同 manifest 的 attempt2 pending 走上述冻结精确 resume；不同 manifest 继续原 pending 拒绝；后续合法 commit/下一 attempt 继续既有资源和 policy 门。不得对这些路径再以 seq2 时的“同 cycle 其他调用皆反证”扫描 live 日志，否则合法 attempt2 自己的 Workflow 会造成恒红。历史重放只验证 handoff 捕获时的载体，当前 root 里的合法 attempt2 不会被倒灌进旧证明。

首次续接在 capture 阶段失败不发布 handoff/script/reserve，不改 seq1/seq2。若冻结后最终复核失败或在 reserve 前崩溃，可以留下无 reservation 的不可变准备物/blobs，但不得新增 reserve 或改旧 event；维持原 unreserved_existing_output 拒绝，不偷偷覆盖它们，使用新的 client/run-dir 重新申请同一个 attempt_index=2。reserve 已发布而 record 未发布时，仅按冻结 handoff 补同一 record；不重编号、不重签、不再次运行 live 门或新建 reserve。此处不增加撤销/解锁事件或全局运行登记。

**本接缝验收**：合法 seq2 fixture、有效来源清单与尺寸合规的新 manifest 为共同起点。先证明直接普通 build（没有任何第二次 recover）可创建唯一 attempt2，并可从冻结 handoff 重放；再独立向原 root 尾追加关联成功/未知请求，或在原 root 的关联 locator/输入清单中引入含同类调用的新 root，直接调用同一 build，必须以 recovery_handoff_counterevidence 红且无 successor reserve，不能靠缺参数、未知事件、版本不兼容或容量错误命中其他分支。另用非作者坏实现分别删除 build 的 live capture、令 reserve 复核只读旧 snapshot，证明指定业务断言抓到它们；在 capture 后、reserve 前修改 root 还须被最后复核拒绝。删除/错绑 handoff、snapshot、record 字段必须使 `_native_build`/collect/check/history 红。无关尾追加须允许首次 build；已合法 attempt2 的真实格式运行及 pending resume 必须通过冻结验证且零新增 reserve/零重派，旧历史在 live 原件增长或移除后仍能离线 check。

## 7. 测试与真实调用边界

1. 先在现有临时fixture上写RED，再改生产代码。容量测试使用真实L，不用缩小常量；L−1/L/L+1、manifest小但JS大、晚于锁/observe的坏实现、检查后重渲染都要可红。保留旧同源超限 pending 可 resume/补 record 的 baseline 对照，再证明仅改 executor 源字节即已有 E_SOURCE_DRIFT、无新增 reserve；新实现另验健康同源合规 pending（含record缺失）仍 resume_only、零新增/零派发，旧超限输入在新 host E_WORKFLOW_CAPACITY 且全树字节不变。不得靠改 frozen source hash、伪造恢复事件或先跑错分支来制造“合法同源超限”正控。
2. 原生错误与 operator adapter 使用隔离原生存储fixture。合法对照必须包含实际已观察的 question/options/preview、root user 的真实布局和非空 annotations，证明不是恒拒绝。非作者独立构造错来源/绑定、缺声明、普通 user 同文、sidechain、API blob 同文、伪 toolUseResult、错选项/preview/target、head变化、拒绝版本/静态窗口/hash不符、small/等于L却自称拒绝、超时与无回执等坏态。非ASCII本身不作为拒绝理由，仍按真实字节容量和精确原生拒绝判定。
3. 单次拒绝顺序测试以固定静态窗口和隔离控制流fixture区分“loader返回error后立即throw、未进入run创建”与“先创建run再返回同文错误”；后者必须拒绝，不执行分发程序私有模块。两个root中的已知关联成功/未知调用，以及另一段代码但同旧identity/manifest/cycle关联的运行，均在有真实格式签字时仍否决。没有未提供来源的已知线索时，不把隐匿全平台运行的自动发现写成验收能力。
4. 签字/幂等测试覆盖同输入check-only后复用、无关尾追加复用、首次提交前head过期、event后回执丢失重入；在幂等返回前向原root尾追加关联反证、提供含反证的新root、改写原前缀，均报指定冲突且不返回旧成功。新来源无关也不能冒充原精确输入。分别验证旧事件离线重放不因live日志增长失效、合法后续head不再具有恢复准入。
5. 来源测试用隔离from/to清单与冻结旧数据，覆盖同path不同hash的两个reader、stale to指纹、四项源任一变更、没有显式恢复事件的source变化。不得执行冻结旧脚本来取得通过。
6. 端到端本地fixture覆盖 reserve1/rejection/reserve2/真实格式audit/prepare/checker若required/collect/check/replay，确认attempt不重编号、无旧票混入。源码替身/VM不能充作在线真实恢复。新增拒绝能力至少以好实现和两个非作者坏实现证伪；只信 locator 布尔、签字覆盖反证、幂等早返回分别须被指定业务断言捕获，不以编译失败计 CAUGHT。
7. 发版前对真实目标先执行check-only，按3.3严格 adapter 复用已有真实声明，确认原件hash不变；发布、两端逐SHA及主仓采用完成后，才实际恢复并执行原规划审计。紧凑manifest通过冻结文件引用提供原完整审计材料，派发前/后均核hash，角色明确读全再给coverage；不得删段落或只审摘要以凑容量。真实来源输入不足时记录具体阻塞，不假装已解决或自动要求重签。
8. Rule6逐hunk：本设计预计代码/字段/命令事实采用定向substitute；如实际加入AI恢复流程指令则照跑AB，不凭文件目录豁免。旧baseline/失败/SKIP与新结果分开。测试/fixture成功不等于启用 post_spec/post_planning 已真实执行并取得审计路由允许继续的合法终态/处置；本次 post_spec 是已 check 的真实 accept_current，converged=false，不改称收敛或全员通过。

## 8. 文档与范围同步

当前设计不改SKILL.md/description/execution-modes的AI流程；新CLI与事件在executor-contract记**程序事实**，不声称旧Skill已能自动选择恢复。当前主控因真实owner授权执行新入口，且必须验证独立的真实有界声明。若实现发现必须改AI指令，先把hunk与Rule6执行要求同步进计划，不偷改归类。

分发版本按实际变更SemVer判断，不预写占位版本；发布后记录真实SHA。只交付筛选结果与来源hash，不公开native carrier或ledger。最终目标是原推荐机制PhaseA有合法审计结论、10项实现任务仍pending，修复自身周期完成；不是“做出一个新CLI就算解阻”。功能tasks的完成仅证明实现、验证、发布、真实恢复与收尾输入就绪；归档、最终handoff、claim释放及estimator是主控随后按Phase D实际执行的独立后置义务，不能把“归档已发生”设为归档前任务完成条件。完整goal仍在这些后置义务实际完成后才结束，不以移出tasks数组免除它们或绕过归档门。本期不修改 PR #38 暂停或 v2 正常业务人类节点；不能以产品接受 operator-assisted 边界为由减审计域、跳门或回写旧票。

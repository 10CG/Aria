---
checkpoint: post_spec
mode: convergence
rounds: 6
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-15T11:20:01.000Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [backend-architect]
---

# post_spec Round 6 — backend-architect

被审对象: proposal.md v7 (HEAD `c3a5903`)。任务: 复核 R5 major 6 (「需要改时任务进 S_FAIL」缺机械触发路径) 在 v7 收窄后的对账; 核 D5.6 跟进 issue 完整性与「硬前提」可操作性; 排查收窄是否引入新的运行时机制描述失实。

## R5 对账

**closed 1 / partially 0 / open 0。**

R5 major (「需要改时任务进 S_FAIL」缺机械触发路径) —— **closed**。

R5 时的顾虑是针对 v5 的「部分跳过」策略: 若 Layer 2 只跳过 description 改动、完成其余部分, 是否落到 S_FAIL 取决于 S6_REVIEW 的通用 LLM code-review 能否碰巧识别出「该做的没做」, 而这条判断没有专属机械路径。v7 把禁令改成「放弃整个任务、不提交任何改动」, 这条新策略绕开了 R5 顾虑的整条依赖链 (S6_REVIEW 的 LLM 判断), 走的是另一条更早、更机械的路径。逐句核对如下 (证据见「机制核实记录」):

1. 「整单不提交」在 `initial.sh` 里落成 `CLAUDE_NO_OP`(或若 push/PR 步骤另有意外, 落成 `PR_CREATE_FAILURE`/其他), 两者都不是 `PENDING`, 因此 Step 11 的 `FINAL_OUTCOME="SUCCESS"` 分支 (要求 `PROVISIONAL_OUTCOME=="PENDING"`) 永远不会被进入; 脚本末尾 `if FINAL_OUTCOME==SUCCESS then exit 0 else exit 1` 决定退出码——只有 `SUCCESS` 才 0, 其余包括 `CLAUDE_NO_OP` 都是 1。这一条对「Forgejo 是否接受零 diff PR」不敏感: 接受与否都不改变 `PROVISIONAL_OUTCOME` 落在 `CLAUDE_NO_OP`(未被 PR 创建步骤的失败分支进一步改写为 `PR_CREATE_FAILURE` 的话), 两条路径终点都是非零退出。**结论: 「整单不提交必进 S_FAIL」这半句准确。**
2. `_handle_s5_await` (`extension.py` L2467-2665) 对 alloc `exit_code` 的处理是无条件分支, 不经过任何 LLM 判断: `alloc_state=="terminated" and exit_code==0` → `S6_REVIEW`; `terminated and exit_code!=0` → 直接 `S_FAIL(CONTAINER_CRASH)`; `lost` → `S_FAIL(DISPATCH_LOST)`。且 Nomad 原生 `ClientStatus` 到这里的 `terminated/running/lost` 三态映射是写死的契约 (`alloc_status_provider.py` L107-116, AD-M2-9): `complete`→`terminated`(exit_code 0, 兜底), `failed`→`terminated`(从 Terminated.ExitCode 取, 缺失兜底为 1), `lost`→`lost`; 只有 `pending/queued/未知` 才回落 `running` 继续等待。也就是说容器只要真正终止且退出码非零, 无论 Nomad 侧汇报的是 `complete` 还是 `failed`, 最终都会在 `_handle_s5_await` 里被判为 `terminated + exit_code!=0`, 直接写 `S_FAIL(CONTAINER_CRASH)`——比 R5 假设的「靠 S6 通用 review 判断」更直接, R5 的顾虑对象(依赖 LLM 判断)在这条新路径上不存在。**结论: 「编排器只看退出码、非零即进 S_FAIL」准确, 且比 R5 报告描述的机制更强(全程零 LLM 裁量)。**
3. 「部分跳过则可能按 SUCCESS 推进」对应的 SUCCESS 五条件 (`initial.sh` L524-534): `CLAUDE_EXIT_CODE==0` 且 `COMMIT_SHA` 非空且 `PR_URL` 非空且 `FILE_TOUCHED_HIT==true` 且 `DIFF_CONTAINS_HIT==true`。后两者由 `compute-assertions.sh` 对 `issue.yaml` 的 `expected_file_touched[]`/`expected_diff_contains[]` 做逐项匹配 (`compute-assertions.sh` L84-120), 与 Rule #6/description 语义完全无关——只要 issue 的断言字段本身没有点名 description 相关文件/片段, 部分跳过(其余部分做完、有 commit、有 PR)就能让五条件全过。**结论: 该半句用词「可能」(条件性)与机制吻合, 描述准确, 不是恒真也不是恒假的断言。**

综上, v7 §D1 的依据句逐字核对为真, R5 major 的具体顾虑(部分跳过 + 依赖 LLM review)已被新策略(整单放弃 + 纯 exit-code 路由)结构性绕开, 判 **closed**。

## Findings

- [major] architecture/proposal.md §Impact+§D5(6) (issue): 「放弃后的失败类型记为 `container_crash` 且默认自动重试、反复告警, 直到 owner 手动阻止该 issue 自动派发」与代码矛盾——`reconciler.py` `_RETRYABLE_FAIL_REASONS = {infrastructure, timeout}` 不含 `container_crash`, LLM 判「retry」也会因该 gate 被降级为 `notify_owner`(不重试); Phase 1 扫描对 issue_id 存在 attempt=1 行 (任意 state, 含 `S_FAIL`) 一律跳过重播种。实际默认行为是「不重试, 大概率仅一次 `notify_owner` 告警, 之后静默卡在 `S_FAIL`」, 不是「默认自动重试+反复告警」; 该错误同时写入了将要开的 D5.6 issue 正文, 会带偏跟进 spec 对现状的认知。

## 观察

- `aria-orchestrator/docs/layer-boundary-contract.md` §S_FAIL handling(proposal 引用为 Impact 段依据)整体已陈旧: 状态名用的是改名前的旧版 (`S5_REVIEWING`/`S6_RECONCILING`/`S7_AWAITING_MERGE`/`S8_MERGED`/`S9_CLOSED`, 应为 `S5_AWAIT`/`S6_REVIEW`/`S7_HUMAN_GATE`/`S8_MERGE`/`S9_CLOSE`), 失败模式表 (`dispatch_timeout`/`execution_crash`/`stuck_s5_await`/`cost_alarm`/`state_mismatch`/`schema_violation`) 与实际 `FailReason` 枚举 (`interfaces.py` L82-102: `quota_exhausted`/`provider_5xx`/`timeout`/`schema_invalid`/`container_crash`/`dispatch_lost`/`review_rejected`/`infrastructure`/`other`/`human_reject`/`human_timeout`/`changes_requested`/`rework_exceeded`) 完全对不上; 「Owner optional intervention: Acknowledge and let Layer 1 auto-retry (default)」这一条正是本轮 major 引用的源头。这与我在 R5 对 `architecture-decisions.md` §AD10 发现的旧状态名问题是同一类文档滞后, 但范围更大(整节失败模式分类都不对应现状), 不是 v7 引入(该文件本 Spec 不改), 不阻塞本轮, 但建议 D5.6 或另开一张「更新 layer-boundary-contract.md 状态名与失败模式表以对齐现行代码」的文档同步 issue, 因为本轮 major 说明这份陈旧文档已经实际误导了一次规范起草。
- D5.6「硬前提: 该跟进 spec 须在要改 skill description 的任务派给 runner 之前落地」目前没有对应的机械检查点(未见 Layer 1 triage/派发前对「issue 是否涉及 skill description 变更」的过滤或拦截), 「由谁、在哪一步检查」问题的答案目前是「无人无处」, 纯靠 owner 记忆自律。但这不构成 major: 即便硬前提被违反(D5.6 落地前就派发了此类 issue), 兜底机制(整单放弃 → `CLAUDE_NO_OP` → 非零退出 → `S_FAIL(CONTAINER_CRASH)`, 见 R5 对账)已验证会接住, 后果是「静默卡住+可能不告警」的运维体验问题而不是「误改坏 description 却被判 SUCCESS」的正确性问题; 建议 D5.6 里补一句明确「此前提当前无机械拦截, 落地前的窗口期靠上面这条兜底机制托底, 不是靠拦截」, 避免读者误以为有前置过滤器。
- D5.6 已知缺口列表(runner 镜像无 skill-creator / 只在 Claude 模型验证过 / `unattended` 传递未定义)三项与我在 R5 核对过的事实(Dockerfile 只 `COPY aria/`、`10CG/Aria#196` 原文)相符, 本轮未发现该三项本身有新的失实; 唯一失实的是「默认自动重试」一句(已列 major)。
- issue-dispatch.md §Execution constraints 第 5 条「若任务无法完成, 不要带着部分工作提交 commit; 在最终消息里写清理由, 让 runner 分类为 `CLAUDE_REFUSAL` 或 `CLAUDE_NO_OP`」与 v7 新禁令的落地方式(整单放弃、理由写进最终消息)天然吻合, 不需要为 Rule #6 专门改这份 prompt 模板——「最终消息里写明是哪个 skill、为什么要改」直接复用这条既有 affordance, 不是新增负担。同时确认 `initial.sh` 的 `claude -p` 调用未加 `--setting-sources project` 限制, 默认会加载被派发仓库 (Aria) 根目录的 `CLAUDE.md`(即本 Spec 要改的规则本体), 所以 Rule #6 新句无需额外改 runner 的 prompt 渲染管线就能传导到 Layer 2, 佐证「本 Spec 只写一句禁令」这一收窄选择在现有 runner 架构下是自洽的。

## Verdict

PASS_WITH_WARNINGS — 0 critical / 1 major / 0 (阻塞) minor。

## Vote

REVISE

## 机制核实记录

- 完整读 `aria-orchestrator/docker/aria-runner/modes/initial.sh`(596 行)L300-596: 确认 Step 6-11 全链路。`PROVISIONAL_OUTCOME` 判定顺序(L338-348 claude 退出码/usage json → L374-376 NO_OP → L449-460 push 分类 → L494-495 PR 创建失败)与 Step 11 的 `FINAL_OUTCOME`/SUCCESS 五条件(L524-534)/退出码(L591-595)逐行核对, 确认「只有 `PROVISIONAL_OUTCOME=="PENDING"` 才可能被判 `SUCCESS`」, `CLAUDE_NO_OP` 一旦成立即不可逆转为 `SUCCESS`。
- 读 `aria-orchestrator/docker/aria-runner/lib/compute-assertions.sh` 全文(137 行): 确认 `file_touched_hit`/`diff_contains_hit` 是对 `issue.yaml` 的 `expected_file_touched[]`/`expected_diff_contains[]` 做字面匹配, 与 description/Rule #6 语义无关, 支持「部分跳过可能被判 SUCCESS」的条件性表述。
- 读 `aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/extension.py` `_handle_s5_await` 全函数体(L2467-2665)与 `LEGAL_TRANSITIONS`(L270-285, 确认 `S_FAIL` 出边为空、终态)、`_advance_dispatch`(L1259-1330 附近): 确认 exit_code==0/!=0 与 lost 三分支均为无条件路由, 不经 LLM。
- 读 `aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/alloc_status_provider.py` L25-239: 确认 Nomad `ClientStatus`→ 内部 `running/terminated/lost` 三态映射(`complete`/`failed`→`terminated`, `lost`→`lost`, 其余→`running`)是写死契约(AD-M2-9), 且 `failed` 状态的 exit_code 缺失时兜底为 1(L409 附近), 补齐了「容器非零退出→Nomad 侧汇报→_handle_s5_await 分支」这条链路中间的一环。
- 读 `aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/interfaces.py` `FailReason` 枚举(L67-102, 13 个值)全量核对, 确认没有任何值对应「需要 owner 裁决」这一 D5.6 目标设计要新增的失败类型, 支持 D5.6 把它列为待建能力(不是漏查现有能力)。
- 读 `aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/extension.py` L1120-1200(Phase 1 issue 扫描/去重逻辑)全段: 确认 `existing = repo.get_dispatch(issue_id, derive_dispatch_id(issue_id, attempt_count=1)); if existing is not None: continue` 对「任意 state」生效(注释原文「a hard UNIQUE preventing any re-seed of an issue_id whose prior dispatch reached S_FAIL」), 即 M2 扫描逻辑不会自动重新派发已有 attempt=1 行的 issue, 无论该行现在是 `S_FAIL` 还是别的终态。
- 读 `aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/reconciler.py` L1120-1373(`_OWNER_INITIATED_FAIL_REASONS`/`_RETRYABLE_FAIL_REASONS`/`_RETRY_COUNT_MAX`/`_scan_failed_dispatches_for_analysis`/`_handle_failure_analysis_for_row` 全部读完): 确认 `_RETRYABLE_FAIL_REASONS = frozenset({"infrastructure", "timeout"})`(L1138-1141)不含 `container_crash`; 即便 LLM 失败分析给出 `verdict.action=="retry"`, `retry_gates_ok` 检查(L1273-1276)因 `fail_reason not in _RETRYABLE_FAIL_REASONS` 而为假, 导致 `effective_action` 降级为 `notify_owner`(L1284-1291), 不会调用 `create_rework_dispatch`; 且该扫描本身用 `NOT EXISTS (... event_type='failure_analysis' ...)` 反连接(L1176-1183), 对同一 dispatch 只会分析/告警一次, 不是「反复」。
- 读 `aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/db.py` L639 附近 `mark_failed` 定义与 `extension.py` L3557-3578 `enter_s_fail`: 确认写入 `S_FAIL` 本身不直接触发 Feishu 告警(告警只在 M5 failure-analysis 的 `notify_owner` 分支里发生), 「Immediate Feishu alert」一说(源自 layer-boundary-contract.md)与代码不符, 支持本轮 major 的判断。
- 读 `aria-orchestrator/docs/layer-boundary-contract.md` §3(L142-169)与 §4(L173-215)全段: 确认其状态名(`S5_REVIEWING` 等)与失败模式分类(`dispatch_timeout`/`execution_crash`等)均与当前代码(`DispatchState`/`FailReason` 枚举)不一致, proposal.md §Impact 的「默认自动重试」原文正是转引自该文档 §S_FAIL handling 第 2 条「Acknowledge and let Layer 1 auto-retry (default)」, 确认这是一次「继承上游文档的错」而非 v7 自造。
- 读 `aria-orchestrator/docker/aria-runner/prompts/issue-dispatch.md` 全文(39 行): 确认第 5 条 Execution constraint 已要求「不完成任务时不带部分工作提交, 理由写进最终消息」, 与 v7 新禁令的落地方式一致, 且该 prompt 不含 `--setting-sources` 限制线索; 交叉读 `initial.sh` L308-317 的 `CLAUDE_ARGS` 数组确认调用未传 `--setting-sources`, 故被派发仓库根 `CLAUDE.md` 按 Claude Code 默认行为会被加载。
- `find`/`grep` 核对: `aria-orchestrator` 内搜索 "aria-blocked"/`label_filter` 相关, 未找到独立的「手动阻止 issue 自动派发」标签机制, 该「手动阻止」防线目前无代码对应, 仅在 Phase 1 的 attempt=1 去重(已引证)里以「不问 state 一律跳过」的形式**隐式**成立, 不需要 owner 手动操作。

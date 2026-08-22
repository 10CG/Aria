---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-22T06:26:09.544Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A2-backend-architect
critical_count: 0
major_count: 3
minor_count: 3
---

## 摘要

对 `pre-merge-gate-no-run-for-branch` proposal.md 做机制正确性 / 状态机 / 枚举封闭性 / schema 兼容 / 实现可行性审查。基线冻结于 `aria @ 400f0bc`，本报告所有代码引用与行号均对该 SHA 直读+实跑核实（`pytest` 119 通过；`compute_verdict`/`_normalize_pr_ci_status`/`_parse_workflow`/`_result` 均直调验证）。

核心结论：**spec 的机制设计方向正确、大部分行号与「红/绿」标注经实测核实准确**（SC-1/SC-2/SC-6/SC-8/SC-9 的基线断言均如实描述），(a)/(b) 轴分离、`not_applicable` 结构性不可达等关键论证站得住。但发现 3 处 Major 级欠定/遗漏，集中在 §2 elif 插入顺序的隐性不变量、§3 `retry_count` 归零与既有 `gate_state_helper.py` 状态转移规则的接缝、以及 `no_run_escalation_retries` 两个独立消费方（gate 侧 vs workflow-runner 侧）校验语义可能分叉。均未达到「按 spec 实施必然错误行为」的 Critical 门槛（多数有 SC 或既有安全网兜底），但都是「实施者会在此分叉」的欠定点，建议在进 A.2 前补一句明确文字或补一条断言。

## Findings

### [A2-M1] Major — §2 新分支相对 `elif main_in_flight_runs:` 的插入顺序是隐性不变量，误置会复现原始盲区

**锚点**: spec proposal.md §2 (行 54-61 代码片段) + `pre_merge_gate.py:203-221` (`compute_verdict` 内 `elif main_in_flight_runs:` / `else:` 兜底段)

**问题**: spec 给出的新分支代码片段是孤立的 `elif pr_ci_status == "not_found": ...`，未标注它必须插在 `elif main_in_flight_runs:` **之前**。由于该 elif 链是 first-match-wins，`elif main_in_flight_runs:` 本身不检查 `pr_ci_status`——若实现者把新分支物理写在 `elif main_in_flight_runs:` **之后**（例如顺手追加在文件更靠后的位置，这是常见的“加分支就往后加”直觉），对 `(pr_ci_status="not_found", main_in_flight_runs=非空)` 这一组合，`elif main_in_flight_runs:` 会先命中，把它判成没有 `gate_error` 的普通 `wait`——verdict 依旧是 `wait`（不构成 fail-open），但诊断信息被静默吞掉，**逐字复现了 #152 要修的原始症状**（`verdict=wait` 但不可辨，AI 会继续等满 1800s）。SC-4 恰好测的就是这个组合，会在 TDD 阶段把这个错误位置炸红——但那是靠“测试恰好覆盖到”兜底，不是靠 spec 文本/代码注释本身防呆；未来任何人重排这段 elif 链（例如给 not_applicable 分支再加条件）都可能不知不觉破坏这个顺序不变量，届时没有专门测试会立刻警觉。

**实测证据**: 用与仓内实现同构的逻辑分别模拟「正确顺序」与「误序」两版 `compute_verdict`：
```
误序 not_found + main_inflight=[{'id':1}] → ('wait', None)              # gate_error 被吞
误序 not_found + main_inflight=[]         → ('wait', {'kind': 'no-run-for-branch'})
```
证实两种输入下行为不对称——只有 main_in_flight 非空这一支会被吞，正是最容易被最初实现漏测到的边角（若开发者先写 `path_coverage=covered_pc, main_in_flight_runs=[]` 这个「主线」用例通过就误以为完工）。另核实基线 `compute_verdict([{'run_id':1}], 'not_found')` 当前返回 `{'verdict': 'wait', ...}`（无 `gate_error`），SC-4 的红判定成立。

**建议**: (1) 在 proposal §2 代码片段里显式加一行注释/说明「必须插在 `elif main_in_flight_runs:` 之前」；(2) 落地时仿照既有 `BA-8` 惯例在代码里加防呆注释钉住顺序；(3) 确认 SC-4 的断言显式检查 `gate_error.kind == "no-run-for-branch"`（不能只查 `verdict == "wait"`，否则误序实现也能让 SC-4 通过——`wait` 是两种实现共同的输出）。

---

### [A2-M2] Major — `retry_count` 归零机制未定义与 `gate_state_helper.py` 既有状态转移规则的关系，可能连带重置 `started_at` 使超时保险失效

**锚点**: spec §3 (行 87 "触发后回到 `wait_recoverable` 循环 (`retry_count` 归零)") + `skills/workflow-runner/scripts/gate_state_helper.py:115-155` (`write_gate_state`) + `references/workflow-state-schema.md:120-121` (`started_at`/`retry_count` 字段定义)

**问题**: `gate_state_helper.py`（该文件自身文档定位为 "reference implementation... canonical reference for any re-implementer"，22 个既有单测）里 `retry_count` 只有两种转移路径：
- `is_first`（`gate_state` 不存在或 `name` 不同）→ `retry_count=0` **且 `started_at` 重置为当前时刻**；
- 否则 → `verdict==waiting` 且既有 `status==waiting` 时 `+1`，其余情况保持原值。

**没有第三条路径**能在「同一个 waiting 态 gate（`name` 不变）」内把 `retry_count` 单独归零而不动 `started_at`。而 `started_at` 是 `elapsed > wait_timeout_seconds`（既有 exit condition 2，唯一真正的绝对超时兜底——`retry_count > max` 在现有代码里甚至没有对应的 `max` 配置项，实测搜索未见）的计时基准，且按既有 schema 文档「Created by phase-c-integrator C.2.4 first wait verdict」「Updated each polling cycle (retry_count += 1, next_check_at recomputed)」——`started_at` 明确只在创建时写一次。

spec 只写了「`retry_count` 归零」，没有说清楚**如何**归零：如果实现者（或 AI 在运行时）按现有唯一能把 `retry_count` 清零的路径去做——即 `clear_gate_state()` 后再 `write_gate_state()`——`is_first` 会重新判为真，`started_at` 也会被刷新为当下时刻。这样一来，只要处方（dispatch / push）本身没有真正让新 run 出现（例如 token 权限问题静默失败、`workflow_dispatch` 路由本仓 404 后 fallback 到处方 2 但推送的 commit 因权限/hook 又没有真正触发 CI），每 ~90s 就会再次命中 2.5、再次把 `retry_count` 与 `started_at` 一起清零——`elapsed > wait_timeout_seconds` 这道 AD-2/AD-4 精心设计的“阈值是个真实可测量”的兜底会被绕过，理论上可以无限循环，永远到不了「user prompt (continue/abort)」这个 fail-closed 出口。

这不是凭空假设：`gate_state_helper.py` + 其 22 个测试是这块状态机**当前唯一的机器可验证 ground truth**，而本 spec 的「代码落点」清单、Cross-references、SC-1~13 都**没有提到这个文件**——即便实现者想去查「归零该怎么实现」，也找不到一条现成的、已测试的 API 可以调用来做「只清 retry_count、留 started_at」这件事。

**实测证据**: 直接读 `gate_state_helper.py:115-146`：
```python
if is_first:
    retry_count = 0
    started_at = _utcnow_iso()          # ← 每次 is_first 都刷新
else:
    if verdict == GATE_STATUS_WAITING and existing.get("status") == GATE_STATUS_WAITING:
        retry_count = int(existing.get("retry_count", 0)) + 1
    else:
        retry_count = int(existing.get("retry_count", 0))
    started_at = existing.get("started_at") or _utcnow_iso()   # ← 非 is_first 时保留
```
`grep -rn "gate_state_helper" --include=*.py --include=*.md .` 确认该文件除自身 22 个单测外，无任何生产代码/文档引用它（`workflow-runner/SKILL.md` 正文未提及其名），印证它是「测试过的参考实现」但和 prose 驱动的实际执行路径之间没有强绑定——恰恰意味着新增的 2.5 行为完全没有一个已验证的落点。

**建议**: 在 SKILL.md §wait_recoverable 2.5 明确写清楚「仅重置 `gate_state.retry_count` 字段为 0，`started_at` 保持原值不动，禁止走 `clear_gate_state()+write_gate_state()` 路径」；同时把 `gate_state_helper.py` 正式纳入本 Spec 代码落点，补一个新的辅助函数（如 `reset_retry_count(state)`，只动 `retry_count`/`next_check_at`，不碰 `started_at`）并配一条单测钉死「重置后 `started_at` 不变」。

---

### [A2-M3] Major — `no_run_escalation_retries` 有两个独立消费方，spec 只对其中一个（gate 侧）要求 fail-closed 校验

**锚点**: spec §2/§3 (行 89, 132 SC-10) + `pre_merge_gate.py:174-179`（`compute_verdict` 的 `cfg` 参数当前函数体内完全未被读取，是首次要被消费）+ `skills/workflow-runner/SKILL.md` §wait_recoverable

**问题**: SC-10 要求「非 int / <1 → 回落默认 + `warnings.warn`」的校验点落在 `gate_check` 的 `cfg` 合并后（Python 侧），且 gate 把**这个校验后的生效值**写进 message。但 `no_run_escalation_retries` 有**第二个独立消费方**：workflow-runner 侧的 2.5 判定（`retry_count ≥ no_run_escalation_retries`），按 spec 原文是「读同一 key」——即 workflow-runner（prose 驱动、不经过 `gate_check`/`_normalize_config` 这条 Python 校验管道）会自己再读一次 `.aria/config.json` 里的原始值。spec 没有要求 workflow-runner 侧对这个原始值做同款校验/回落。

若配置被写成非法值（`0`、负数、字符串），两个消费方会各自独立处理：gate 侧显影为回落后的 `2` 并写进 message；workflow-runner 侧若直接用原始值做 `retry_count ≥ 0`（AD-4 原文明确禁止「不提供 0（=等同 fail，回到 AD-2 的假红）」这正是被禁止的语义）或 `retry_count ≥ "banana"`（未定义比较），两边对「同一次 no-run 事件该在第几次重查后升级」给出的答案会不一致——用户看到的 message 说「第 2 次重查」，但实际系统行为可能是第 1 次甚至第 0 次就升级（0/负数场景），或行为完全未定义（非数字场景）。这违反了「配置只应有一个校验事实来源」的原则，且恰好复刻了 AD-4 明确点名要防的「假红」场景，只是绕过校验点触发而非绕过默认值本身。

**实测证据**: 确认 `_normalize_config`（:98-127）只做两个旧键别名映射，从不校验任何键的类型/范围（包括既有的 `wait_timeout_seconds` 等，历史上就是如此），`gate_check` 里 `cfg["enabled"]` / `cfg["no_ci_fallback"]` 是仅有的两处直接使用；`compute_verdict` 的 `cfg` 形参当前函数体内 `grep -n "cfg" ` 命中为 0（只在签名里），确认这是该字段第一次被真正消费——因此校验逻辑必须是全新代码，没有既有先例可依样画葫芦到 workflow-runner 侧。

**建议**: 二选一：(a) workflow-runner 不再独立读原始 config，改为读 gate 输出里已校验过的生效值（如把 `no_run_escalation_retries` 的生效值也放进 `gate_error` 或 `gate_state` 的某个字段，而不仅仅嵌在 message 文案里给人看）；(b) 在 workflow-runner SKILL.md §wait_recoverable 逐字复制同款校验规则（非 int/<1 → 回落 2），并把这条也纳入 rule6_note 的「描述性 substitute 测试」范围。

---

### [A2-m1] Minor — `compute_verdict` 的 `cfg=None` 默认值与 SC-2/SC-3/SC-4 的调用签名不设防会导致早期崩溃而非预期的红

**锚点**: `pre_merge_gate.py:174-179`（`cfg: dict[str, Any] | None = None`）+ proposal §2 SC-2/SC-3/SC-4 的调用示例（均未传 `cfg` 参数）

**问题**: SC-10 要求 not_found 分支的 message 里嵌入生效的 `no_run_escalation_retries` 值，实现上自然是在 `compute_verdict` 内部第一次读 `cfg.get("no_run_escalation_retries", ...)`。但 SC-2/SC-3/SC-4 描述的调用形态是 `compute_verdict([], "not_found", path_coverage=covered_pc)`——不传 `cfg`，此时 `cfg` 为 `None`。若消息构造代码写成 `cfg.get(...)` 而不做 `cfg or {}` 防御，这几条测试会直接 `AttributeError` 崩溃，而不是产生「断言失败」意义上的红——不是错误行为，但是一个会在开发第一轮就被撞见、容易让人误以为是别的地方出 bug 的坑（该异常发生位置和真正缺陷位置隔着一层调用栈）。

**建议**: 在 proposal §2 明确写一句「message 构造必须对 `cfg is None` 防御，回落 `DEFAULT_CONFIG["no_run_escalation_retries"]`」。

---

### [A2-m2] Minor — `.aria/config.template.json` 未列入 §5 文档同步面，且既有机械探针方向性防不住这类遗漏

**锚点**: proposal §5（文档同步面清单）+ `/home/dev/Aria/.aria/config.template.json:73-` + `/home/dev/Aria/.aria/probes/config-template-key-currency.py`

**问题**: 主仓根 `.aria/config.template.json` 里已声明 `phase_c_integrator.pre_merge_gate` 的全部既有键，且有一个已启用的机械探针 `config-template-key-currency.py` 专门盯这个字段与 `DEFAULT_CONFIG` 的一致性。但该探针的判定方向是**单向**的——只检查「模板键 ⊆ `DEFAULT_CONFIG`」（防模板带陈旧/未知键），**不检查**「`DEFAULT_CONFIG` 新增键是否也补进了模板」。proposal §5 的文档同步面清单里没有提到这个文件，若最终实现漏掉它，`config-template-key-currency.py` 依然会 PASS（因为不会因为模板「少了」一个键而变红），于是这个遗漏不会被任何已启用的闸门捕获，只会体现为「SKILL.md 配置表写了 `no_run_escalation_retries`，新采用方复制的模板里却没有」的静默文档漂移（Rule #3）。

**建议**: 在 §5 显式加一行：同步更新 `.aria/config.template.json` 的 `phase_c_integrator.pre_merge_gate` 段。

---

### [A2-m3] Minor — Why/What Changes 叙事中「六键契约逐字不变」一语与 SKILL.md 自身既有措辞冲突

**锚点**: proposal §2 行 74（"既有早退分支 (... main 核验) **六键契约逐字不变**"）vs `SKILL.md` 既有文字（main-核验分支是「唯一一个不保持六键不变的（它多一个 `gate_error`）」）vs proposal SC-7（用词是「输出键集逐字不变」，未写「六键」）

**问题**: proposal §2 的叙事句把 main-核验也归进「六键契约逐字不变」的分支列表里，但 main-核验分支从 #137 起就已经比其余四类多一个 `gate_error`（7 键），这是 SKILL.md 自己白纸黑字写明的既有事实，不是本 spec 要改的东西。真正的测试标准 SC-7 用词更准确（「输出键集逐字不变」，不含「六键」字样），所以不影响实施正确性，纯属叙事段落措辞不严谨，容易让读者以为本 spec 打算把 main-核验也压缩回六键。

**建议**: 把 §2 那句改成「相对基线逐字不变（main-核验分支既有的 `gate_error` 七键不受影响）」，避免用「六键」一概而论。

## 未发现问题但已核验的点

- `_normalize_pr_ci_status([]) == "pending"`（基线）与改后 `"not_found"` 的红窗断言位置（`test_pre_merge_gate.py:363`）经 `sed -n` 核对行号完全吻合。
- `query_branch_in_flight` 走 `_translate_in_flight_run`，与 `_normalize_pr_ci_status` 是两条独立代码路径，**不**共享判定逻辑 —— 确认 §1 改动不会误伤 (b) 轴，spec 对此的论证成立。
- `compute_verdict([], "not_found")` 基线实测确实返回 `green`（fallthrough 到 `else` 分支），与 SC-2「基线红：无该分支，fallthrough 到 green」的描述完全一致；`compute_verdict([{"run_id":1}], "not_found")` 基线实测返回 `wait`（因 `main_in_flight_runs` 已真，不依赖 `gate_error`），核实 SC-4 之所以「红」是因为缺 `gate_error.kind` 而非 `verdict` 错——需要 SC-4 断言显式检查 `gate_error.kind`（见 A2-M1 建议）。
- `not_applicable` 短路（`gate_check:498` `pc.get("decision") == "not_applicable"`）在 `query_pr_ci` 调用**之前**就已 `return`，结构上确认 `query_pr_ci` 永不会在该 decision 下被调用 —— §2 表格「结构上不可达」的论证成立；SC-6 直接跑通（`query_pr_ci.called == False` 且 `"gate_error" not in out`），基线即绿，符合 spec 标注。
- `_parse_workflow` 对块形 `workflow_dispatch: {}`、flow 列表形 `on: [push, workflow_dispatch]`、无该键三种输入分别实跑，确认现状均不产生任何 `dispatchable` 信息（键不存在），且新增该判定不会触碰 `covered_uncertain`/`triggers` 既有逻辑（`NON_AUTO_TRIGGER_KEYS` 的 `pass` 分支是唯一插入点，零副作用）；本仓真实文件 `.forgejo/workflows/issue-triage-tests.yml` 确认同时声明 `push`/`pull_request`/`workflow_dispatch` 三键，是 SC-13 活体验证的合理靶子。
- `_result()` 现有全部调用点均为 ≤5 个位置参数，新增第 6 个带默认值参数（`dispatchable_workflows`）不破坏任何既有调用——已逐一核对 `_evaluate()` 内 6 处 `_result(...)` 调用。
- `gate_error` 全仓（.py/.md/.json，排除 gate 自身/SKILL/tests）零外部消费方，`pr_ci_status` 同样零外部消费方——R-a 的「守卫非风险」判断成立；`aria-orchestrator/` 快速交叉检索同样未见消费方。
- `github_actions.py` 是纯 NIE stub，不存在与 `aether.py:225` 同形态的 `if not runs: return "pending"` 兄弟位置需要同步修——排除 fix-the-class 遗漏。
- `DEFAULT_CONFIG`/`compute_verdict`/`_build_output`/`gate_check`/not_applicable 短路的行号引用（:55-75 / :174-233 / :236-275 / :387-527 / :498-506）逐一 `grep -n` 核对，与 SHA `400f0bc` 完全吻合，未见「行号漂移」。
- `POST .../actions/workflows/{file}/dispatches` 与 `workflow_id` 按文件名寻址、`/actions/workflows` 404 的 R-c 断言超出本 lens 可复核范围（需要真实 HTTP 探针，非静态代码审查），未重复验证，采信 owner 本 session 探针记录。

## Verdict

**PASS_WITH_WARNINGS** (0 Critical / 3 Major / 3 Minor)

vote: REVISE — 三条 Major 均可通过给 proposal.md 补充明确文字/断言而收敛（不需要推翻设计方向），建议在进 A.2 前吸收 A2-M1/M2/M3，尤其 A2-M2（`retry_count` 归零 vs `started_at` 的接缝）涉及 fail-closed 兜底是否真正生效，是本 spec 整个 AD-2/AD-4 设计意图能否落地的关键点，值得在动代码前先钉死语义。

---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-14T15:30:00.000Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [backend-architect]
---

# post_spec Round 5 — backend-architect

被审对象: proposal.md v5 (HEAD `f169a0b`)。任务: 复核 v5 新增的运行时内容 (OQ-7 自主栏四选项可行性 / 「运行模式怎么判」段对 `10CG/Aria#196` 缺口的描述 / SOT 自主模式条款的执行靠什么保障), 并排查新引入的机制描述失实。

## R4 对账

无 (R4 本席零发现)。

## Findings

- [major] architecture/proposal.md §D1+§OQ-7+§Impact (issue): 「需要改时任务进 S_FAIL」无对应机械触发路径 —— `_handle_s5_await` 推进到 S6_REVIEW 只看 Nomad alloc `exit_code`, 明确注释「result_path NOT persisted: no downstream consumer」; `initial.sh` 写入的 `CLAUDE_NO_OP` 结果在 hermes-extensions 全仓零消费。AD5「任意状态可进 S_FAIL」只证状态图上合法, 不证本场景真的会走到那条边; S6 之后能否落到 S_FAIL 取决于通用 LLM code-review 恰好把「跳过的 description 改动」判成 REVIEW_REJECTED (它审的是 diff/commit_message/acceptance_criteria, 不识别 Rule #6/scenario 4b 语义), 若该改动只是大 issue 的一部分, 整单更可能直接报 SUCCESS, 「进 S_FAIL」不会发生。

## 观察

- **「运行模式怎么判」段对 `10CG/Aria#196` 的描述本身准确** (与 issue 原文「缺 import 会静默 fallback 到 false」逐字对得上), 但「后果」只说到「runner 可能误按交互模式走 (A) 并请人审」「这条规则无法保证生效」, 隐含「#196 修好 = 规则就能生效」——上面的major 表明这不成立: 即便 `unattended` 被正确读到 `true`, S5→S6 的推进依然不看 result.json 的 outcome/CLAUDE_NO_OP, 「进 S_FAIL」照样没有机械路径。#196 与本 major 是两个独立缺口, 修好前者不会连带修好后者, 建议在 OQ-7 或 D6 局限里把两者分开写, 避免 owner 误以为解决 #196 就足够。这条本身不再单列 major, 因为已被上面更根本的缺口涵盖。
- OQ-7 (B) 的「aria-runner 镜像没装 skill-creator」核对属实: Dockerfile (`aria-orchestrator/docker/aria-runner/Dockerfile`) 只 `COPY aria/ /opt/aria-plugin/`, 没有安装官方 `skill-creator` 插件, 与 RESULT.md 里插件缓存路径 (`claude-plugins-official/skill-creator/...`) 是完全不同的两个插件来源。
- OQ-7 (E) 引用的 AD10 回滚路径 Level 2 原文「在 S5_REVIEWING 中间插入一个 optional human gate (只对高风险 issue 触发)」逐字核对准确; 但顺手发现 AD10 自己的正文仍用旧状态名 (`S5_REVIEWING` / `S6_REVIEW_PASSED` / `S7_AWAITING_MERGE`), 与 AD5 2026-04-28 revision 后的现行命名 (`S5_AWAIT` / `S6_REVIEW` / `S7_HUMAN_GATE`, 已在 `extension.py` 的 `DispatchState` 枚举里实际使用) 不一致 —— 这是 AD10 文档自身没跟着 AD5 改名同步的旧账, 本 Spec 只是照抄 AD10 原文, 不是 v5 引入的新问题, 且本 Spec 不改 `architecture-decisions.md`, 不阻塞本轮, 但值得另开一条文档同步待办。
- D5.2 的 skill 口径「`aria/skills/` 下 43 个目录、42 个含 SKILL.md、`issue-triage-workspace` 不是 skill」逐项核对准确 (`ls -d` 43 / `find -name SKILL.md` 42 / 唯一缺口目录确为 `issue-triage-workspace`); `ab-suite/trigger/` 现有 0 个套件、`ab-suite/version.yaml` 当前 `version: "1.5.0"` 均与 SC-2/SC-4 的前提一致。
- OQ-7 (D) 「离线批量预审」隐含的假设是「suite 存在于 `ab-suite/trigger/` 就等于已审」(靠 OQ-3 的「未审套件不让搭车进 ab-suite/」流程习惯支撑), 这个假设比 (C) 更弱依赖机械保障 (不需要运行期判断「是否已审」, 只需判断文件是否存在), 相对稳妥; 但同一份「怎么知道已审」的数据从哪来的问题, 在 D4 的 `rule6_note` 设计里目前只落在单次 cycle 的 spec/tasks 文本里, 没有跨 cycle 的机读登记处, 与本 major 描述的「无持久化审阅登记」是同一类缺口的另一面, 供 owner 一并考虑, 不单独计分。
- D4「无机械 enforcement (本 Spec 不加 custom check): 合规靠审阅」这条免责声明覆盖的是「agent 是否愿意遵守 Rule #6」这件事; 本 major 说明的是另一层、更深的缺口——即便 agent 愿意遵守并主动放弃改动, 这个「放弃」目前也没有可靠路径变成 Layer 1 能看到的 S_FAIL, 两者不是同一件事, D4 现有免责声明不能覆盖本 major。

## Verdict

PASS_WITH_WARNINGS — 0 critical / 1 major / 0 (阻塞) minor。

## Vote

REVISE

## 机制核实记录

- 读 `aria-orchestrator/docs/architecture-decisions.md` §AD5 (L395-470) 全文: 确认「10 正常状态 + S_FAIL 全局兜底」「任意状态都可进入 S_FAIL」(选型理由第 2 点) 为 AD5 原文逐字表述; 现行状态名为 `S0_IDLE...S9_CLOSE` (2026-04-28 revision, 旧命名 `S0_SCANNING...S8_DONE` 已作废)。
- 读 §AD10 (L752-817) 全文: 确认「Aria 2.0 流水线只保留 1 个人类审批 gate, 位置在 S7_AWAITING_MERGE」与回滚路径「Level 2: 在 S5_REVIEWING 中间插入一个 optional human gate (只对高风险 issue 触发)」均为 AD10 原文逐字表述, proposal.md §OQ-7 (E) 与 §Impact 的引用与之逐字一致。同时发现 AD10 正文用的状态名 (`S5_REVIEWING`/`S6_REVIEW_PASSED`/`S7_AWAITING_MERGE`) 是 AD5 改名前的旧词, 与当前代码实际使用的 `DispatchState.S7_HUMAN_GATE` 等枚举不一致 (AD10 文档自身未随 AD5 revision 同步, 非本 Spec 引入, 见观察)。
- 读 `aria-orchestrator/docker/aria-runner/Dockerfile` 全文: 确认镜像只 `COPY aria/ /opt/aria-plugin/` (aria-plugin 子模块), 无任何安装官方 `skill-creator` 插件的步骤, 支持 OQ-7 (B) 「当前跑不起来」的代价声明。
- 读 `aria/skills/phase-a-planner/SKILL.md` 协作 (multi-track) 小节 (L100-145): 确认「`state_scanner.coordination.unattended == true` ⇒ 零 `AskUserQuestion`, 改写 awaiting_owner 记录」与「有没有人可问是配置事实, 不得运行期推断」为该 SKILL.md 原文逐字表述, proposal.md §OQ-7「运行模式怎么判」段的引用与之一致; 但该「unattended=true 时用 awaiting_owner 记录替代 AskUserQuestion」的替代逻辑是 A.1 协调模块专属, Rule #6/OQ-7 的自主模式条款没有同款替代逻辑。
- `forgejo GET /repos/10CG/Aria/issues/196` 读取全文 (+ comments, 0 条): 确认 issue 原文「取值路径钉死为 aria-runner 容器镜像内 `.aria/config.json`」「缺 import 会静默 fallback 到 `false`」与 proposal.md 引用逐字一致。
- 追踪「(C) 任务进 S_FAIL」的实际触发链路:
  - `docker/aria-runner/modes/initial.sh` L21+L337-376: 定义 `PROVISIONAL_OUTCOME` 枚举 (`CLAUDE_TIMEOUT`/`INFRA_FAILURE`/`CLAUDE_REFUSAL`/`CLAUDE_NO_OP`/`IDEMPOTENCY_CONFLICT`/`GIT_STAGE_FAILURE`/`PR_CREATE_FAILURE`/`SUCCESS`/`ASSERTION_MISMATCH`), 其中 `CLAUDE_NO_OP` = claude exit 0 且 `git diff HEAD` 空且无新 commit —— 这正是「agent 因 Rule #6 拒绝改 description 且未做其他改动」时会落入的枚举值。
  - `docker/aria-runner/modes/changes.sh` L271: 类似地对「claude produced no diff」调用 `fail_with "no_changes"`, 但 changes 模式 (owner PR 反馈重做) 不是自主模式下「新 issue 顺带改 description」的典型路径, 仅作旁证「no-diff 場景在两个模式脚本里走不同枚举, 没有统一到一个 Rule #6 专属 reason」。
  - `grep -rn "CLAUDE_NO_OP" aria-orchestrator/hermes-extensions/`: 零命中。即 Layer 1 侧 (`hermes-extensions/aria-layer1/`) 没有任何代码专门处理这个枚举值。
  - `hermes-extensions/aria-layer1/aria_layer1/extension.py` `_handle_s5_await` (L2467+) 文档字符串与内联注释明确: 「terminated + exit_code==0 → 转到 S6_REVIEW (result_path NOT persisted: no downstream consumer)」—— 即 S5→S6 的推进只读 Nomad alloc 的 `exit_code`, 不读 `result.json` 里 `initial.sh` 精心计算的 outcome 字段; L2596-2598 的注释重复同一结论 (「not result_path; no downstream consumer exists」)。
  - `_handle_s6_review` (L2830+): 该状态的 PASS/S_FAIL 分支由 `call_review()` 对 `pr_diff`/`commit_message`/`acceptance_criteria` 做通用 LLM (glm-5.1) 代码评审决定, 例外分支 (parse error / timeout / provider 5xx) 才直接判 S_FAIL; 评审 prompt 不含 Rule #6/scenario 4b 语义, 只能靠「diff 没解决 issue 要求」这类通用判据碰巧命中。
  - 结论: 「agent 因 Rule #6 自主放弃 description 改动」到「任务进 S_FAIL」之间, 现状没有专属机械路径; 唯一潜在路径依赖 (a) 该改动确实导致空 diff 或大 issue 里唯一实质内容缺失, (b) 空 diff 仍然被推上去开了 PR (未验证 Forgejo 是否接受零 diff PR), (c) S6 通用 review 把「没做」正确判定为不满足 acceptance criteria。三个环节均非本 Spec Tasks (T1-T8) 覆盖范围, 也未在 proposal 任何位置被点名为待建设的前提。
  - 检索 `hermes-extensions/aria-layer1/*.py` 中 `result.json`/`result_path` 相关引用 (`db.py`/`alloc_status_provider.py`/`extension.py`), 均为「明确不持久化 / 不消费」的注释, 未发现反例 (即没有找到其他函数悄悄读取了 result.json 的 outcome 字段)。
- `find`/`ls` 核对 D5.2 数字: `aria/skills/` 43 个目录、`find -name SKILL.md` 42 个命中、唯一缺口目录为 `issue-triage-workspace`; `ab-suite/trigger/` 现有 0 个套件文件; `ab-suite/version.yaml` 当前 `version: "1.5.0"`。均与 proposal.md D5.2 / SC-2 / SC-4 的前提数字一致。

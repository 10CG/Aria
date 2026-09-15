---
checkpoint: post_spec
mode: convergence
rounds: 6
converged: false
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-15T11:54:07.000Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
---

# post_spec Round 6 聚合 — rule6-description-change-trigger-eval-lane

> 被审 SHA `c3a5903` (v7, owner 2026-09-15 裁定收窄范围之后的版本)。drift_guard 未配置 ⇒ `drift_check_skipped: true` (knowledge-manager 席按 `.aria/config.json` 实读订正; 其余四席 frontmatter 写 `false`, 以本聚合为准)。
> Sibling probe: 已完整扫描, 未发现同 issue 竞品 (R6 入口跑一次; 聚合时重跑一次, 结果相同)。
> 观察条数 (只数顶层条目, 不进比较键): tech-lead 12 · code-reviewer 11 · backend-architect 4 · qa-engineer 6 · knowledge-manager 6。

## 审计结论 (去重: 按 {category, scope} 合并, scope 归一到章节锚; 同一问题跨 category 的交叉注明)

### Critical
无。

### Major (6 个比较键, 对应 5 个问题)
1. [major] architecture/proposal.md §D1 (SOT §2 自主禁令及其依据) (issue) — 「放弃整个任务、不提交任何改动 ⇒ 必进 S_FAIL」不成立: 工作区留有未提交改动时, `initial.sh` Step 10 由 runner 自己 `git add -A`、提交、推送并开 PR, issue 断言命中即 SUCCESS; changes / redo 模式有 diff 且推送成功即写 PASS 退 0。执行者照字面停手而不撤销, 正落进禁令要防的「部分交付按成功推进」(tech-lead; code-reviewer 观察 1 同题)。
2. [major] testing/proposal.md §D2 (同批参照臂) (issue) — v6 为回应 R5 第 2 条新加的参照臂有两处漏洞。(1) 它只接得住同时落在自己 should-trigger 段的故障: 故障只落在被评臂 ⇒ 正确的 description 判 fail; 落在臂的后半程 (should-not) ⇒ 过宽改动判 pass; 负控 ≥ 6/10 只在门通过时作废, 按 v7 规则回放基线 v2 判成 fail (code-reviewer, 用假 `claude` 实跑)。(2) 三种正当情形下必然作废: 按「fail 的后果」第 (2) 条改了套件划分后, 旧 description 过不了新套件的门; 新增 skill 没有改动前的 description, 且新增 skill 是否属于场景 4b 未界定; 修复一个现行已坏的 description (tech-lead)。
3. [major] documentation/proposal.md §Impact+§D5.6 (issue) — 「放弃后记为 `container_crash` 并默认自动重试、反复告警, 直到 owner 手动阻止该 issue 自动派发」与代码不符: `container_crash` 不在可重试集合; 失败分析默认关闭; tick 标 S_FAIL 不发告警; 心跳扫描对已有派发行的 issue 不再派发 ⇒ 默认行为是不重试、不告警的终态, 放弃原因无人看到 (tech-lead, code-reviewer)。
4. [major] architecture/proposal.md §Impact+§D5.6 (issue) — 与第 3 条同一问题 (backend-architect: 即使打开失败分析, `container_crash` 的 retry 判定也会降为 notify_owner, 同一派发只分析一次, 至多一张卡)。
5. [major] documentation/proposal.md §D5 (第 7 项残留) (issue) — D5 第 7 项仍要求另开一张 `10CG/Aria` issue, 与 owner「全部已知缺口并入唯一一张跟进 issue」的裁定、以及抬头 / T6 / SC-6 / Key Deliverables 的「三张」冲突; 照 D5 做会多开一张且无 SC 验收 (knowledge-manager 列 major; tech-lead、code-reviewer 列 minor, 同键取最高)。
6. [major] documentation/proposal.md §D6+头部 (issue) — R5 第 3 条的残留: 头部「RESULT 再修订须同步重核」清单仍不含 §D6 (也不含 §Impact、T8); D6 待转录句里「写入时附当时的版本号与提交 SHA」是给执行者的指令, 没有标「不转录」, 逐字写进 SOT 会自相矛盾 (knowledge-manager; tech-lead 观察 7、code-reviewer 观察 10 同题)。

### Minor
无 (两席提的 minor 与第 5 条同键, 已并入)。

## Verdict

PASS_WITH_WARNINGS — 0 critical / 6 major / 0 minor (去重后; 去重前 major 8 / minor 2: tech-lead 3M + 1m · code-reviewer 2M + 1m · backend-architect 1M · knowledge-manager 2M · qa-engineer 0)。vote: 4 REVISE / 1 PASS (qa-engineer)。

## 主控复核 (聚合前逐条对代码核实, 不照搬席位转述)

- runner 代提交: `aria-orchestrator/docker/aria-runner/modes/initial.sh` Step 10 注释原文「若 claude 没 commit 但 working tree 有 changes, runner 补 stage+commit」, 其下即 `git add -A` 与 `git commit`; Step 8 只在「工作区干净且相对 base 无新提交」时判 `CLAUDE_NO_OP`。第 1 条成立。
- 不重试: `reconciler.py` 可重试集合为 `{"infrastructure", "timeout"}`, 每个派发至多系统重试 1 次; 失败类型不在集合内时, LLM 给出的 retry 降为 `notify_owner`。
- 默认不告警: tick 的 S_FAIL 分支只调 `repo.mark_failed`; `extension.py` 的飞书发送点只有 S7 两处; 失败分析在 `ARIA_FAILURE_ANALYSIS_ENABLED` 未设时整段跳过, 仓内部署配置没有一处设置它 (`docs/m5-handoff.yaml` 记为「owner choice; default off」); 打开后同一派发只分析一次 (`NOT EXISTS` 反连接), 卡里的原因取自 `fail_detail`, 而 `_handle_s5_await` 写入的 `fail_detail` 只有退出码与 alloc id, 不含 Claude 写的说明。第 3、4 条成立。
- 参照臂漏检: `run_eval.py` 把 `claude -p` 的 stderr 接到 DEVNULL; 超时后 kill 进程、返回「未触发」; 遇结果帧即返回当时的判定; 只有工作进程抛异常才打印 `Warning: query failed`。基线套件前 10 条 should-trigger、后 10 条 should-not, `--num-workers 1` 时按提交顺序执行 ⇒ 臂后半程的故障只落在 should-not 上。第 2 条 (1) 成立。
- 对修法的约束: `run_eval.py` 看到第一个 tool_use 开始或第一个 `message_stop` 就判定并 kill 进程, 正常调用本来就没有结果帧; 「按每次调用的结果帧识别故障」不能直接套用, 写进规范前须先做实验。
- Impact 数字 (tech-lead、code-reviewer 观察同题): aria 子模块 master (`1cb3872`) 非合并提交 456 个, 改了已有 skill description 的 7 个 (brainstorm 一次删掉 frontmatter、一次恢复并换措辞, 按两次计; 合并成一次为 6), 约 1.5%; 另有 15 个提交新增 skill (不含首版)。v7 写的「577 次里 6 次」, 分母是含合并提交与非 master 分支的 `--all`, 分子口径没写。

## 轮次记录

| 轮 | 被审 | critical | major | minor | vote |
|---|---|---|---|---|---|
| R1 | `298d0e4` (v1) | 1 | 14 | 17 | 5 REVISE |
| R2 | `55bc9f3` (v2) | 0 | 10 | 26 | 3 REVISE / 2 PASS |
| R3 | `0c41e53` (v3) | 0 | 5 | 6 | 4 REVISE / 1 PASS |
| R4 | `e822829` (v4) | 0 | 3 | 4 | 3 REVISE / 2 PASS |
| R5 | `f169a0b` (v5) | 0 | 6 | 4 | 5 REVISE |
| R6 | `c3a5903` (v7) | 0 | 6 | 0 | 4 REVISE / 1 PASS |

(R3 起非阻塞意见分进「观察」, minor 计数口径与 R1 / R2 不同。v6 `3b2215e` 未单独过审: R5 后 owner 裁定先收窄, 收窄结果即 v7。)

### Round 6
- Agents: 五席全部完成
- Sibling probe: 已完整扫描, 未发现同 issue 竞品
- Conclusions: 6 (另有观察 39 条)
- R5 对账各席合计: closed 8 / partially 3 / open 0 (tech-lead 2 / 1; code-reviewer 2 / 1; knowledge-manager 1 / 1; qa-engineer 2 / 0; backend-architect 1 / 0)。三条 partially 分别落到本轮第 2 条 (1)、第 6 条与 tech-lead 观察 7。
- Converged: false —— R6 仍有 major

## 未收敛原因分析

- 5 个问题的来历: 第 1 条与第 3、4 条出在 v7 为收窄新写的运行时描述上; 第 2 条出在 v6 为修 R5 第 2 条新加的参照臂上; 第 5 条是 v7 编辑漏删 (主控的残留扫描只搜了字面「D5.7」, 没搜第 7 项正文); 第 6 条是 R5 第 3 条没修完。4 个是修复文字带出的新缺口, 1 个是旧条目修得不全, 与 R3–R5 同一形状。
- 第 3、4 条的根源: 主控把 `aria-orchestrator/docs/layer-boundary-contract.md` §S_FAIL handling 的描述 (连同 tech-lead 席 R5 的一条观察) 当作事实写进 v7, 没有对代码核实; 该节与现行代码不一致, 状态名与失败类型也是旧版 (backend-architect 观察 1)。
- 性质: 6 个键都在文字层, 三席明写修改不需要重跑基线。第 1、3、4、5、6 条靠删改文字即可修; 第 2 条是设计问题, 且 D2 的故障识别已连续两轮冒 major (R5 第 2 条 ⇒ v6 参照臂 ⇒ R6 第 2 条)。
- 按收敛算法, R6 仍有 major ⇒ R7 的比较键不可能与 R6 相等 ⇒ R7 结构上不可能收敛; max_rounds = 7 在 R7 后耗尽。

## 下一步 (待 owner 裁定)

按 R5 聚合登记的规则「R6 若仍有 major, 如实报 owner」, 本轮聚合后不启动 R7、不改 proposal。主控已向 owner 汇报并给出选项, 裁定后在本节追记。

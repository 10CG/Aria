---
track-id: aria-a1-entry-claim-guard
owner-container: aria-runner-bot/023236f2
phase: session-close
status: done
updated-at: 2026-08-04T02:30:00Z
---

# Session Handoff (2026-08-04) — #122 碰撞 → 三次 ship → Spec 不收敛 → spike → 重写 → 双 Spec R1-fix

> 会话维度增量。承接 [2026-08-02 勘误 handoff](./2026-08-02-dual-spec-collision-postmortem-and-shipped-defects.md)。
> **本段主线 = 一条「审计 → 发现审计本身出错 → 订正」的完整链**。最有价值的产出不是 Spec, 是**三次自我订正**: 我的 spike 结论错了一条、我的发布交付漏了两次、我的 Spec 修法互相拆台三次。每一条都由**别人**(审计席位 / custom check / 工作流镜头 / 并发轨的 rebase)抓到, **没有一条是自查发现的**。

## §0 入口 (新 session 优先读)

- **当前态**: 主仓 `ca4db78`, 双远端 equal, custom checks **8/8**, 工作区仅 `aria-orchestrator` (一贯排除)。
- **两份 Spec 都在闸门后、均已 R1-fix, 但都不可进 A.2**:
  - `linked-issue-normalization` — R1-fix 已落, 待下一轮裁决;
  - `a1-entry-claim-duplicate-work-guard` — **两个阻塞性未决项** (见 §6)。
- **本段 ship**: aria-plugin **v1.65.2** (#124) + **v1.65.3** (#125/#126)。
- **下一步**: 见 §6。

## §1 已完成 (本段)

1. **#122 双 Spec 碰撞的完整处置** — 归并分析 → owner 裁「以 R 为准」→ A1/A2/A3 三轮修订 + post_spec R5(5 席)/R6(新眼睛) → **发现修订对象已被并发轨 ship 并归档** → 本轨 superseded, 写勘误 handoff。
2. **三个 live 缺陷开 issue 并修完两轮**: [#124](https://forgejo.10cg.pub/10CG/aria-plugin/issues/124) fail-OPEN 误放行 → **v1.65.2**; [#125](https://forgejo.10cg.pub/10CG/aria-plugin/issues/125) + [#126](https://forgejo.10cg.pub/10CG/aria-plugin/issues/126) → **v1.65.3**; [#127](https://forgejo.10cg.pub/10CG/aria-plugin/issues/127) AB 套件缺口 (Rule #6 第三行第 3 条义务) 已开。自包含复现脚本落 `.aria/repro/`。
3. **`a1-entry-claim` 走完 R1(5 席) → R2(新眼睛) → R3(第三双新眼睛)**, 判定**不收敛** (同口径 major 4→6 上升)。
4. **owner 裁 A+B** → 抽出 [`linked-issue-normalization`](../../openspec/changes/linked-issue-normalization/proposal.md) 独立交付 + **S1–S6 六条 spike 全部完成**。
5. **母 Spec 全量重写** (非打补丁), 原 7 处「A.2 待办」清零。
6. **两份 Spec 各跑 5 席 post_spec** → 均 5/5 REVISE。
7. **动态工作流跑两份 R1-fix** (`wf_03a8b72c-489`, 10 agent / 0 error / 1.48M tokens): 起草 2 → **三镜头对抗验证 6** → 综合 2。

## §2 未完成 / Carry-forward

**AI 内省 (load-bearing)**:

- 🔴🔴 **凭据轮换 —— hard cap `2026-08-02` 已过期**。本 session 从头到尾 surface 了 **十余次**, owner 始终未动。`FORGEJO_TOKEN` / `NEXUS_API_TOKEN` / `CF_ACCESS_CLIENT_SECRET`。**这是唯一过期不可补救、且 AI 完全无法代劳的项。**
- 🔴 **`a1-entry-claim` 两个阻塞项** (详见 §6): C1 `allowed-tools` / C2 heartbeat 触发点。**未解决前该 Spec 不具备实施条件。**
- 🔴 **`include_terminal` 的签名变更跨两 Spec 冲突** — 本 Spec 要给 `linked_issue_overlaps` 加形参, 而前置 Spec 的 §非目标写「签名与返回 schema 不变」。**须 owner 协调归属。**
- **两份 Spec 的 R1-fix 后均未再过闸门** — 工作流的三镜头是**验证修法**不是过闸门, 二者不可互替。
- **S6 的 follow-up 未做**: `owner-container` (形如 `simonfish/bfe8285d`) 与 claim 的 container 段口径**已经不同**, 需成文。
- **未 triage**: aria-plugin #117 / #120 / #123 + 并发轨新开的若干; 承前 Aria #168 / #169 / M6 四门 / M7。

**机械补漏 (backstop)**: `handoff_autofill` 的 unfinished 全部来自 M6/M7 六个活跃 spec 的 `tasks.md` —— **本段零碰**。`sync` 段**零告警** (双远端 equal)。consistency 12 flags 全是 `active_change_not_in_upm` —— Aria 无 UPM, **恒亮**, 非本段引入。

## §3 三次自我订正 (本段最值钱的部分)

**没有一条是自查发现的。**

| # | 我错在哪 | 谁抓到的 | 形状 |
|---|---|---|---|
| 1 | **spike S4 的「R2 量错了总体」本身是一次跨总体比较** | 工作流的 fact-check 镜头 | 批评在批评自身里复发 |
| 2 | **两次「声称完成而实际没落盘」** (发布同步面漏 6 处 / AB fixture 从未提交却三处声称已做) | custom check 变红 / 并发轨推送触发 rebase | 动作 scoped 而声称 global |
| 3 | **多簇 fix 互相拆台三次** (issue 派生 track-id 杀死主机制 / 保护窗与 track-id 形态矛盾 / `无` 作实参致误报) | R2 席位 / R3 席位 / 工作流整合者 | 每条单独看都对 |

**第 1 条的细节值得记**: 我指控 R2「把别名统计量在了错误的总体上」, 逐字复跑后 —— R2 量的是 issue **引用位置** (含 `docs/`) 得 25/11 (与其报的 24/10 一致); 我量的是**全文裸 token** (只有 `openspec/`) 得 16/799。**口径与范围都不同, 谁也没推翻谁**; 而且 **R2 的口径其实更贴近 `--linked-issue` 的真实取值**。三处引用已同批订正 (spike 报告 / 母 Spec §Why / LIN §极性段)。

**第 3 条的最后一例三个对抗镜头都没抓到** —— `linked_issue_overlaps` 只在 `own_linked_issue` falsy 时短路, 而 `"无"` 是 truthy ⇒ **两份毫无关系的 Spec 只要都写「无」就互相误报 overlap**。由整合者实测发现。**接缝恰好落在三个镜头的角度之间。**

## §4 关键风险 / 已知陷阱

1. **`allowed-tools` 是 Spec 可实施性的前置条件, 而三轮审计 + 六条 spike 都没查过 frontmatter**。实读: `phase-a-planner:9` = `Read, Write, Glob, Grep, Task, Skill` (**无 Bash 无 AskUserQuestion**); `spec-drafter:10` = `Read, Write, Glob, Grep, AskUserQuestion` (**无 Bash**)。⇒ 主机制在它自己指定的执行位置上**不可调用**。
2. **`release_gate.py --sweep-stale` 的 help 逐字写着「跨 container」** —— 我的 D6「无任何函数支持释放别的容器的 claim」是假的。**与 heartbeat 无人调 (C2) 复合后**: 所有 claim 30min 后即 stale, 而 phase-d-closer 逐周期带该 flag ⇒ 从「已知限」升级为**数据面风险**。
3. **「换新鲜眼睛 > 加轮」这条处方在本条修订线上连用两轮后失效** (R2/R3 都是新眼睛, 仍不收敛)。真正起作用的是 owner 裁的 **A+B (缩范围 + spike-first)** —— 六条 spike 里**两条推翻了上游审计结论**, 那是再跑几轮审计问不出来的。
4. **归档 Spec 不可回写**。rebase 撞上 `openspec/archive/` 时,正确反应不是解冲突而是意识到修订对象已完成生命周期 (本段据此 skip 了 A2/A3 两个 commit)。

## §5 多维度同步状态 (机械核验)

- **git**: 主仓 `ca4db78`, **双远端 equal**; `aria` `af87cae` (v1.65.5, 并发轨); `standards` `2111c84`; `aria-orchestrator` `92acce5` (feature 分支, 只读未动)。`gitlink_integrity` **6/6 ok**。
- **custom checks**: **8/8** (本段一度 6/8, 因我漏了发布同步面 6 处, 已补齐)。
- **openspec**: 活跃 **9** (本段新增 `linked-issue-normalization`; `a1-entry-claim` 重写; `phase-c-integrator-ci-path-coverage` 已 superseded)。
- **issue**: aria-plugin #124/#125/#126 **已关**, #127 新开; open 总数涨到 30 (含并发轨新开)。
- **并发撞车 3 次** (v1.65.4 / v1.65.5 / owner 的 rule6_note 裁定), 全部零重叠, rebase 通过。

## §6 Next session 入口 + 优先级

1. 🔴🔴 **凭据轮换 —— 已过 hard cap**。owner 亲自操作, AI 无法代劳。
2. 🔴 **`a1-entry-claim` 的两个阻塞项须 owner 裁**:
   - **C1 `allowed-tools`**: (a) 扩权 (`phase-a-planner` 加 `Bash, AskUserQuestion`; `spec-drafter` 加 `Bash`) —— **加 `Bash` 是能力面变更, 会改变 Rule #6 判据**; 或 (b) 换宿主代调 —— **会改变「A.1 起草前」的时点语义**;
   - **C2 heartbeat 触发点**: 三个候选 (挂 A.1 机械步骤 / 挂 state-scanner Phase 0.5 / 承认做不到改延长 TTL), **A.2 前必须定死其一**。
3. **`include_terminal` 签名变更的归属** — 两 Spec 冲突, 须 owner 协调。
4. **两份 Spec 的下一轮闸门** — 跑不跑、派谁。若跑, 建议至少一席未参与过本轮的。
5. **`linked-issue-normalization` 可先行** — 它无阻塞项, 是母 Spec 的前置依赖, 且修的是**今天就在生产中静默失效**的机制。
6. 未 triage: #117 / #120 / #123 + 并发轨新开; 承前 #168 / #169 / M6 四门 / M7。

## §7 同步状态 (autofill 机械汇编)

```
[main]              master = ca4db78 | github=equal origin=equal
[standards]         (detached) = 2111c84
[aria]              (detached) = af87cae
[aria-orchestrator] feature/m6-cost-model-telemetry = 92acce5 | origin=equal
```

**warnings: 零。** 本段所有 commit 均已双推 + `ls-remote` 独立核验 (github 两次瞬时 SSH 失败均按硬约束重试后确认, 未据单次失败下结论)。

## §8 Memory entries this session

**新增 3 条** (均经查重, 与既有 memory 形状不同):

- `feedback_critique_repeats_the_error_it_names` — 指控别人「量错总体」时极易在指控里犯同款; 反驳数字前必须**逐字复跑对方命令** + 并列「总体/范围/计数法」三项, 任一不同只能写「不可比」非「推翻」。与 [[feedback_fix_recurs_in_its_own_fallback_path]] 不同形状 (那条讲修复在兜底路径复发, 本条讲**批评在批评自身里复发**)。
- `feedback_scoped_git_add_splits_claim_from_landing` — scoped `git add` / 子模块内提交后, 动作是 scoped 而声称是 global; 收尾必须跑**不带路径**的 `git status`。一天两次实证。与 [[feedback_completion_signals_vs_runtime_invocation]] 同族但根因更浅 (命令作用域, 非语义)。
- `feedback_fixes_contradict_each_other_across_clusters` — 多簇 fix 逐条吸收后必做**条款间交叉一致性检查**; 三次实证均致主机制失效; **多 agent 并行审计不覆盖它** —— 接缝落在角度之间。

**已有覆盖未重复落**: 并发重复劳动 (`feedback_concurrent_duplicate_audit_fetch_before_start`, 本段第五次实证) / 加轮判据 (`feedback_stop_adding_rounds_when_major_count_flattens`, 本段验证其处方「换新鲜眼睛」有失效边界) / 已 ship ≠ 能用 (`feedback_completion_signals_vs_runtime_invocation`, 本段三次命中)。

## §9 流程判断留痕 (Rule #10, 请复议)

- **闸门全程未自行豁免**。post_spec 共跑 **6 轮 / 26 agent 实例** (R5 5 席 / R6 1 席 / a1-R1 5 席 / a1-R2 1 席 / a1-R3 1 席 / 两份新轮各 5 席), 席位数**从未自行下调** —— owner 说「定向」时我按「收范围不收席位」执行并显式说明。
- **动态工作流经 owner 明确要求后才启用** (「启用动态工作流」), 未自行发起。
- **三个 issue 的拆分与定级 (#124 fail-OPEN / #125 恒 wait / #126 误诊) 是 AI 判断**, owner 只说「开 issue 报这三条」—— 请复议定级。
- **A2/A3 两个 commit 的 skip 是 AI 的技术判断** (归档 Spec 不可回写), 不在 owner 的指令文本内。可从 reflog 取回 (`925fd90` / `32a887a`)。
- **v1.65.3 ship 时 Rule #6 第三行的义务 2 事实上不在仓里** (AB fixture 未提交), 已补并在 commit 中披露, **未追溯撤版** —— 该处置是 AI 判断, 请复议。
- **推送均在 owner 明确授权后执行**; 本段未出现未授权的外向动作。

## Cross-references

- 前一段: [2026-08-02 勘误](./2026-08-02-dual-spec-collision-postmortem-and-shipped-defects.md) · 并发轨: [2026-08-02 #121+#170](./2026-08-02-121-ship-and-170-secret-guard-four-round-audit.md)
- 两份 Spec: `openspec/changes/{linked-issue-normalization,a1-entry-claim-duplicate-work-guard}/proposal.md`
- spike (6 条): `.aria/spikes/2026-08-02-*`
- 审计报告: `.aria/audit-reports/post_spec-R{1,2,3,5,6}-*` (含两份 aggregated + 本轮 5+5 席)
- 工作流产物: `.aria/audit-reports/post_spec-R1-fix-editlist-*.md` + `.aria/audit-reports/wf-r1fix/` (2 PLAN + 6 VERDICT)
- 复现脚本: `.aria/repro/repro-aria-plugin-124-125-126.py`

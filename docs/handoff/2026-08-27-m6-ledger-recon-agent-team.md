---
track-id: session-close-20260827-m6-ledger-recon
owner-container: simonfish/bfe8285d
phase: session-close
status: done
updated-at: 2026-08-27T09:10:00Z
---

# Session Handoff (2026-08-27) — 会话收尾: M6 账目核实 (agent team + 动态工作流) + #177 补证据 (session-closer, leaf)

> **一句话**: owner 设 goal「创建 agent team + 动态工作流, 按你的建议执行」→ 起 11-agent 工作流核实 M6 `dispatch-input-delivery` 的 30 个 task 账目 (六组并行 + 对抗轮) → **真实进度 = done 17 / in_progress 10 / pending 3**, 而非 yaml 此前显示的「30/30 未勾、54 天」→ 回填 yaml + 同步 tasks.md → 给 Aria#177 补上版本漂移的实例证据。
>
> ⭐ **这段最该留下的**: 对抗轮的**反事实手法**。让 challenger 不是"再读一遍代码", 而是**去撤销那个 fix, 看测试会不会红** —— 两条 done 判定当场被推翻: 把 `initial.sh:880` 的 fetch 分支条件改成永不成立 (等于撤销 TASK-008 的整个 fix), 集成套件 5 条 check **仍全 PASS**; 把 fetched body 换成常量 (等于抓回的正文整个丢弃), **5 PASS / 0 FAIL 不变**。这两个"绿"正向核实一万遍也抓不到。

## §0 入口 (新 session 优先读)

- **主仓** master `5e7875f`, 双端 equal, 工作树干净。**aria 子模块 master `d50f9c3` 仍领先 gitlink (`58a49e7` = v1.67.1) 2 个 commit** (刻意未发版, 承前)。
- 本 session **无 spec cycle、无 claim** (只读核实 + 账目回填 + issue 评论)。
- **M6 真实状态已浮出**: 报告 `.aria/notes/2026-08-27-m6-task-ledger-recon.md`; 四门无一待决策, 全是待执行的基建动作。

## §1 已完成 (按时间顺序)

1. `/aria:state-scanner` → 指出「距昨天零变化, 三件待决事项全没动」, 换角度给出**不需要 owner 决策就能推进 M6** 的选项 [1] 账目回填 + [2] #177 补证据。
2. **owner 设 goal**: 创建 agent team / 拉入所有相关 agent / 动态工作流 / 按建议执行。
3. **[2] Aria#177 补证据** —— 把本 session 的主项目版本漂移 (9 点漏改 8 点、存活 9 天、连清单都没有) 写成该 issue「发布同步面漏项是类级根因」的实例。⚠️ 过程插曲: 首次 POST 用 `-d '...'` 内联长 body 失败 (shell 吃掉反引号), 误发了一条 `test` 评论 (id 20022) —— 已 DELETE, 改用 `-d @file` 成功 (comment 20023)。
4. **[1] M6 账目核实工作流** (`wf_4ee913aa-65f`, 11 agents / 0 error / 325 tool calls / ~1.06M tokens):
   - **agent team 按 A.3 锁定分工**: backend-architect ×3 (TG-1/2/3 代码面) · qa-engineer ×2 (TG-4/TG-6 执行门) · knowledge-manager ×1 (TG-5 文档) · **code-reviewer 做对抗轮**。
   - **pipeline 而非 barrier**: 每组核实完立刻进自己的对抗轮, 不等其他组。
   - **判定纪律写进 prompt** (本次产出质量的来源): 逐条对照 `verification`; 代码存在 ≠ 完成; **文档存在 ≠ 动作已执行**; 拿不准判 partial 不往 done 靠。
   - 结果 **done 17 / in_progress 10 / pending 3, 对抗轮推翻 5 条**。
5. **回填双账目**: `detailed-tasks.yaml` 27 条 status (done→done / partial→in_progress / not_done 保持 pending); 随后**复核发现 `tasks.md` 30 个 checkbox 仍全未勾** ⇒ 同步 17 条勾选 + 10 条 partial 行内加 `<!-- ⚠️ 部分完成 (TASK-00N): 缺什么 -->` 注记。
6. 归档门复核: `13/30 unchecked` (原 30/30), verdict=warn, complete=false —— 准确反映真实状态。

## §2 未完成 / Carry-forward (AI 内省, load-bearing)

- 🔴 **M6 四门待执行** (无一待决策, 互为前置): TASK-021 build (partial, 需真实触发 `aether-build-container` 构建+push) → TASK-022 freeze (pending); TASK-028 egress 活测 (pending, 仓里有现成 HCL 待在 heavy-node 实跑) → TASK-029 E2E dogfood (pending, AC-1 最重要那道)。**021 与 028 无前置, 可并行起步。**
- 🟡 **六处测试补强** (partial 的那批, 不阻塞门但影响 168h 跑的可信度): TASK-002 file-mode 失败路径 / TASK-003 body 半边零验证 + files_hint 无测试 / TASK-005 YAML-safe escape 措辞与实现路径不符 (**需 owner 判是否历史遗留**) / TASK-007 RED 未在真实 call-site / TASK-008 重言式测试 / TASK-009 / TASK-013 / TASK-020 / TASK-023。逐条缺口见 `.aria/notes/2026-08-27-m6-task-ledger-recon.md`。
- 🟡 **承前未动** (昨天 handoff §2 的原样): Aria#147 误关待 owner 定是否重开 · Luxeno 延迟 45 天未复核 (决定 TASK-029 能否过) · aria 2 个未发版 commit 去向 · `m6-arch-doc-stale` 92d (我仍未改 Last Updated, 理由同前) · #182 / #184。
- 🟡 并发轨 023236f2: 24h 内无提交; `a1-entry-claim` claim 心跳停在 08-23 (已超 STALE_TTL)。

**机械补漏 (autofill 交叉核验)**: `unfinished` **159 → 142**, 减少的 17 条正是本 session 勾掉的 M6 task —— 机械侧确认账目回填生效, 零额外补漏; `consistency_check` 7 flags 全 `active_change_not_in_upm` (Aria 无 UPM, 恒亮); `sync` 零告警。

## §3 关键风险 / 已知陷阱

- **回填一个账目必须同时回填它的孪生账目**: 本 session 先只改了 `detailed-tasks.yaml`, 复核才发现 `tasks.md` 的 30 个 checkbox 原封不动。OpenSpec 的 Level 3 spec 有**两份**任务账目, 归档门读 tasks.md、design_deferred 读 yaml —— 只改一份会造出新的不一致。
- **workflow 结果 JSON 存的是原始 enum, 不是映射后的值**: 我在 `m6-results.json` 里存 `partial`, 却在下游判断写成 `in_progress` ⇒ 10 条注记静默漏加 (勾选 17 条正常, 掩盖了漏加)。**跨脚本传递 enum 时要么两端同名, 要么在边界处显式映射一次并断言。**
- **长 body 走 `-d '...'` 内联会被 shell 吃字符**: 含反引号/表格的 markdown 必须 `-d @file`。本 session 因此误发了一条评论 (已删)。
- **对抗轮 agent 也会写错证据**: TG-6 的 challenger 在一处引用 `host-volume.hcl:26-29` 说"确认本地 ext4", 实际取出整份文件 30 行后那几行没有该内容 —— 对抗方的证据同样要抽验 (本次由核实方反查抓到)。

## §4 实战教训 (memory 沉淀来源)

```
[候选 memory]
- feedback_adversarial_verify_by_reverting_the_fix (新, 高价值): 对抗轮最有效的手法不是
  "再读一遍代码找漏", 而是**撤销被验证的那个 fix, 看测试会不会红**。本 session 两条 done
  判定当场倒掉: 撤销 TASK-008 的 fetch 跳过分支后集成 5/5 仍 PASS; 把 fetched body 换成
  常量后 5 PASS/0 FAIL 不变。重言式测试与"测试存在即覆盖"的假绿只有反事实能抓。
  与 feedback_counterfactual_test_for_every_new_sc 同族, 但施加对象是**已有测试**而非新 SC。
- feedback_level3_spec_has_twin_task_ledgers (新): OpenSpec Level 3 有 tasks.md (checkbox,
  归档门读) 与 detailed-tasks.yaml (status, design_deferred 读) 两份账目。回填/勾选任一份
  都必须同批回填另一份, 否则造出新的不一致。checkbox 是二元的, partial 用行内注释承载。
- feedback_enum_value_must_match_across_script_boundary (新): 跨脚本/跨阶段传 enum 时,
  中间产物存的是原始值还是映射值必须一致。本 session 存 partial 判 in_progress ⇒ 10 条
  注记静默漏加, 而同批的 17 条勾选正常, 掩盖了漏加 (部分成功最难发现)。
- feedback_long_markdown_payload_needs_file_not_inline (追记既有 shell 陷阱族): 含反引号/
  表格的长 body 走 `-d '...'` 会被 shell 吃字符并静默失败, 必须 `-d @file`。
[未写下经验]
- 昨天 handoff §4 列的 4 条候选 (commit message 引述误关 / 百分比闸小基数失真 / VERSION
  裸 semver 块是机械入口 / 「卡 owner 门」要展开核实) 仍未落成 memory 文件。加上本段 4 条,
  累计 8 条候选待固化 —— 建议下个 session 先清这批, 否则继续贬值。
```

## §5 四维一致性 (autofill)

UPM present 但 cycle=null (Aria 无 runtime UPM); OpenSpec 活跃 7 (门控 6 + a1-entry), pending_archive 0; User Story 21 (done 17 / in_progress 2 / approved 1 / pending 1); PRD present。consistency 7 flags 全 `active_change_not_in_upm` (结构性恒亮)。

## §6 Next session 入口 + 优先级建议

`/aria:state-scanner`。本 session leaf 终结。

1. **推 M6 的起点已经明确**: TASK-021 (触发一次镜像构建) 与 TASK-028 (heavy-node 跑现成 egress HCL) **无前置可并行**; 各自完成后解锁 022 / 029。
2. **先复核 Luxeno 延迟** (承前建议) —— 它决定 TASK-029 能否过, 45 天未测。
3. **清 memory 积压**: 累计 8 条候选 (§4 + 昨天 §4), 建议优先固化 `feedback_adversarial_verify_by_reverting_the_fix` 与 `feedback_commit_message_quoting_closes_autocloses_own_repo_issue`。
4. 承前: Aria#147 重开与否 / aria 2 个未发版 commit / 架构文档 92d / #182 / #184。

## §7 同步状态 (autofill, 收尾时)

```
[main]              master = 5e7875f | github=equal origin=equal
[aria]              gitlink 58a49e7 (v1.67.1); master d50f9c3 领先 2 (未发版, 双端已推)
[standards]         334c609 (未动) | [aria-orchestrator] master 237045a | 双端 equal
[coord ref]         本 session 无 claim
本 session 主仓提交: 1d497ce (账目回填+报告) → 5e7875f (tasks.md 同步)
```

## §8 Memory entries (本段对话新增 0, 候选 4 + 承前 4)

未写 memory 文件。§4 列 4 条新候选; 昨天 handoff §4 的 4 条仍未落。累计 8 条待固化。

## Cross-references

- 报告: `.aria/notes/2026-08-27-m6-task-ledger-recon.md` (逐条明细 + 5 条推翻全文)
- 工作流 transcript: `.claude/projects/*/subagents/workflows/wf_4ee913aa-65f/` (11 agents, journal.jsonl 含每 agent 完整返回值)
- Spec: `openspec/changes/aria-2.0-m6-dispatch-input-delivery/` (proposal 头部加了账目核实注记)
- Issue: [Aria#177 comment 20023](https://forgejo.10cg.pub/10CG/Aria/issues/177#issuecomment-20023)
- 前序: [2026-08-26 SC-8 闸门 + 版本 SOT + M6 门踩点](./2026-08-26-sc8-gate-version-sot-and-m6-gate-recon.md)

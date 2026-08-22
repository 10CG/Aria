---
track-id: credential-echo-defense-three-layers
owner-container: simonfish/023236f2
phase: shipped
status: done
updated-at: 2026-08-22T04:50:00Z
---

# Session Closeout (2026-08-18 → 08-22) — 一个 session, 三仓五 ship, 两次方向相反的撞车, 一桩凭据事故闭环

> **一句话**: 这是会话维度收尾 (session-closer, leaf), 覆盖 08-18 起的整段对话。周期产物已在
> [2026-08-20 batch handoff](./2026-08-20-issue-batch-181-147-145-ship-and-gate-blindspot.md) 逐项留痕 (含 §6续);
> 本文只放 **入口指针 + 未闭合线程 + 本段沉淀的经验**, 不复述账目。
>
> ⭐ **这段对话最该留下的一件事**: 同一周内两次撞车**方向相反、成本不对称** — 我重复了对方几分钟的归档 (08-18), 对方重复了我已 ship 的修复却付出一整条 L2 spec + 两轮审计 (08-21)。根因都在 Aria#174/#180/#135 在案, 但本段把「起 ≥小时级工作前查该 issue 有无别的 track」补成了自己的判据 (memory 已追记)。

## §0 入口 (新 session 优先读)

- **运行时状态**: aria-plugin **v1.66.3** 为 cache/SOT 双侧现行 (四分判定 PASS 08-21); aria master 领先 tag 两个**未发版** docs/test commit (`6e2adc8` traps#5 勘正 / `400f0bc` 守卫三轴), 随下次 ship。
- **三仓同步**: main `5ce9651` / aria `400f0bc` / standards `faaede2`, 双端 equal, gitlink 4 组 REACHABLE (machine-checked 本次 scan)。
- **本段 ship 清单**: 主仓 #181 (`fd594bc`) · aria-plugin v1.66.2 (#147+#145) · v1.66.3 (#153 L1) · Aether PR#318 (#317 L2, wrapper) · standards 两次计数同步。
- **本段立案**: aria-plugin#152 (gate 盲区) / #153 ✅closed / #154 (L3, 已范围修正) / Aether#317 ✅closed; #174 补第 5 次实证; #138 spike 数据归档。
- **凭据事故**: registration-token 回显 (08-20) → owner 08-21 重置 + 5/5 runner 主机侧对账零陌生注册 → **闭环**。

## §1 本段工作 (指针, 非复述)

全部细节见 [2026-08-20 batch handoff](./2026-08-20-issue-batch-181-147-145-ship-and-gate-blindspot.md): §1 时序 (triage 4 件 → #181 → v1.66.2 → gate 盲区诊断) / §3 事故与 Rule #10 留痕 / §6续 (三层防御 L1/L2/L3) / §2 carry-forward (已随进展逐条收口)。本段后半程 (08-21/22) 另有: superseded spec `subprocess-decode-hardening` 残值 harvest (守卫三轴收紧 `400f0bc`, 对方已归档 `909d771`) + 一次 detached-HEAD 造成的 ~2 分钟活体 orphaned gitlink (逐端核验抓住并收编, memory 已追记)。

## §2 未闭合线程 (AI 内省, load-bearing)

- 🟡 **aria-plugin#152 gate 盲区修法待裁** — A (path_coverage 感知新分支首推) / B (文档处方) / C (上游)。A 最治本; 未裁前每条新 feature 分支首推都会让 gate 恒 wait 一次 (绕行: 第二次 push 碰 path)。
- 🟡 **aria-plugin#154 L3 待排期** — 范围已收窄为「secret-scan.sh 补通用 JSON 凭据键模式 + FAKE 白名单 + 日志 sha256 留痕」(小改动); 活体复现在案 (`{"token":"…"}` 形状穿过)。
- 🟡 **#138 跨段 fail-open** — owner 裁定「数据存档暂不起 spec」; OR 候选 4 腿实测在 issue comment 19247, 排期时直接可用。
- 🟡 **Rule #10 复议点未回应** — 「先修 runner 再 ship」被我按意图执行为「CI 真绿再 ship」(batch handoff §3.2); owner 至今未评, 默认接受但留痕不撤。
- 🟡 **Aether 侧拓扑文档过时** (aether-status skill: heavy 3 节点, 实际 5) — 本段只改了 memory, **未立案** (提了没做)。
- 🟡 **两个未发版 aria commit** — 下次任何 PATCH ship 顺带带出; 不单独发版。
- ⏸️ `aria-orchestrator` 工作树停 `feature/m6-cost-model-telemetry @ 92acce5` — 全 session 有意排除, gitlink 未动 (承前)。
- ⏸️ M6 三门 / backlog (#150 / #139-146 / #180 / #182) — 承前, 非本段可动。

**机械补漏 (backstop, 交叉核验)**: `handoff_autofill` unfinished **207 条**, 逐一归属 M6/M7/linked-issue-normalization/ci-path-coverage 等**其他轨** (本段全部为无 spec 的 Level 1 批次, 无 spec 任务可遗漏) → 零补漏项; `consistency_check` 9 flags 全 `active_change_not_in_upm` (Aria 无 UPM, 恒亮, 非本段引入); `sync` 零告警。

## §3 待固化经验 (AI 内省)

```
[候选 memory]  — 本段已写入 (全部 type: feedback/reference, 索引已更新或追记到既有条目)
- 报告→行动隔小时级 = 报告已陈旧; 别容器 stale claim 是信号非噪声 (追记 feedback_concurrent_duplicate_audit_fetch_before_start, 08-18)
- 同一 issue 两个 track-id 镜像撞车 + 成本不对称; 起 ≥小时级工作前查该 issue 有无别的 track (同上条, 08-21 追记)
- Forgejo 新分支首推不评 paths 过滤→不建 run→gate 恒 wait; 误诊 runner 停摆的速判法 = 全局 task id 是否在涨 (新条 reference_forgejo_new_branch_paths_filter_no_run)
- submodule update 后 detached HEAD 上 commit → push master 推陈旧 ref → 分钟级活体 orphaned gitlink; 子模块 commit 前先确认在分支上 (追记 feedback_detached_head_may_be_stale_rebase)
- fixture 假值必须与真值零关联 (连前缀都不借); 凭据类端点响应即凭据本体 (追记 feedback_secrets_never_in_conversation)
- 「不存在」也是未测量的摘要: 立案新机制前先 ls hooks/ + grep (追记 feedback_own_past_summary_is_not_a_measurement)
- 拓扑更正 heavy 3→5 节点 (reference_10cg_cluster_internal_routing)

[未写下经验]
- 「L2 wrapper 方法感知 DENY」是 knob-granularity 的又一实证 (GET 枚举是合法轮换步骤, 一刀切逼人开 RAW 反而失去脱敏) — 既有 memory 已覆盖该类, 未另写
- 「两条讨论性命令被 secret-guard 按形状误拦, 回显把整条 heredoc 打进对话」— 这恰是 #145 的活体证据, 已随 #145 修复进 CHANGELOG, 不另成 memory
```

## §4 四维一致性 (机械 + 人工)

| 维 | 状态 |
|---|---|
| UPM | 无 (Aria 不配置), 9 flag 恒亮 |
| OpenSpec | 活跃 9 (全部他轨), pending_archive 0, `subprocess-decode-hardening` 已归档 (design-only, SUPERSEDED) |
| User Story | 21 (done 17 / in_progress 2 / approved 1 / pending 1), 本段无 US 变动 |
| PRD | 无变动 |

本段无 spec, 四维无「已做未反映」项; 版本同步面 (aria 5 文件 + 主仓 14 处 + standards 计数) 两次 ship 均机械核对 (custom checks 10/10 pass 本次 scan)。

## §5 同步状态 (autofill 机械汇编, 本次 scan)

```
[main]              master = 5ce9651 | github=equal origin=equal
[aria]              master = 400f0bc | github=equal origin=equal  (tag v1.66.3 = c7a37e2, +2 未发版 commit)
[standards]         master = faaede2 | github=equal origin=equal
[aria-orchestrator] feature/m6-cost-model-telemetry = 92acce5 | origin=equal (有意排除)
gitlink integrity: all ok (4 组) | custom checks 10/10 | coordination: 本段 claim 已释放 (done)
Aether (无 github 镜像): master 08d9700 (PR#318 merged); 安装副本 ~/.npm-global/bin/forgejo byte-identical
```

## §6 Next session 入口

入口: `/aria:state-scanner`。候选 (均待 owner 定序): ① #152 修法裁定 (A 推荐); ② #154 L3 小改动 (可与下次 PATCH 同发); ③ Aether 拓扑文档漂移立案; ④ backlog。**开工前**: fetch 三面 (issue 板 / master / coord ref) + 查该 issue 有无别的 track (本段两次撞车的判据)。

## Cross-references

- 周期产物 handoff: [2026-08-20 batch](./2026-08-20-issue-batch-181-147-145-ship-and-gate-blindspot.md) (含 §6续 三层防御)
- 并行轨: [2026-08-18 #128 Phase D](./2026-08-18-issue128-phase-d-archive-and-sc9b-close.md) (bfe8285d) · superseded spec 归档 `openspec/archive/2026-08-21-subprocess-decode-hardening/` (对方容器)
- 版本史: `aria/CHANGELOG.md` [1.66.2] [1.66.3]

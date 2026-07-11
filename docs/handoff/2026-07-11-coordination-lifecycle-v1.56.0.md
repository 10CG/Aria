---
track-id: coordination-claim-lifecycle-and-overlap
owner-container: simonfish/bfe8285d
phase: D
status: done
updated-at: 2026-07-11
---

# Session Handoff (周期收尾) — 协调机制 claim 生命周期闭环 v1.56.0 ship + issue #159/#160 关票

> 承接同日 [2026-07-11-partB-v1.55.4-and-coordination-spec.md](./2026-07-11-partB-v1.55.4-and-coordination-spec.md) §6 第一优先级 (item 1 Phase B)。

## §0 入口 (新 session 优先读)

- **本 session 干了什么**: (1) 关 #159/#160 —— 实测证明两票内容已全被 v1.55.2/v1.55.4 覆盖, 零代码, 带证据关票。(2) **item 1 完整 ship**: `coordination-claim-lifecycle-and-overlap` L3 spec Phase B 全三部件 (C 释放闭环 / A1 认领强制 / B1 linked_issue 重叠 advisory) → aria **v1.56.0** (PR#106 `504da89`), pre-merge 对抗 review 1C/5I 全修, 一次性清理真协调 ref, spec 归档。
- **当前态**: 全闭环。aria v1.56.0 双远程 parity; 主仓本 commit 收尾; 协调 ref 干净 (0 stale active); 本 cycle claim 已由 D.2b dogfood 释放 (done)。
- **下一步**: 无 carry (本轨终结)。承前项见 §6。

## §1 已完成

1. **#159/#160 关票** (零代码): #159 readarray/zsh 崩溃 = #154 已修 (v1.55.2), zsh 本机实测 3 用例佐证; #160 三项全被覆盖 —— 命令替换 4 用例 BLOCK (部件 B), NUL-in-field 通用字段数校验 fail-closed (NUL+无害命令交叉验证非 pattern 碰巧), log_ack 换行折叠 L199-200 早已在 (我先 regex 误判未修, 读代码+运行时 3行→1行 验证后纠正)。
2. **Part C (defect c — claim 从不释放)**: `release_gate.py` CLI (按归一 track_id+container 定位, session 无关; 释放全部同 track 匹配 [review I1]; fetch→release→sweep→gc→resilient_push 全 fail-soft; 独立遥测分区防污染 run_gate 探针) + `apply_tree_edits` 批量单 commit 原语 (CAS update-ref, 并发窗口 `ref_moved` 不静默覆写 [I3]) + GC 真写入 (abandoned 同 retention 归档; retention 按 heartbeat_at=释放时刻 [M1]) + `sweep_stale_active` + schema 增 `abandoned` (修写后读回即丢的 latent bug) + phase-d-closer **D.2b** 接线。
3. **Part A1 (defect a)**: `coordination.enabled` 默认 false→true (opt-out, ⚠️ 行为变更: 第三方项目走 Phase B 会向 origin 推 `refs/aria/coordination`) + phase-b-developer **B.0 REQUIRE claim** / branch-manager 前置 + doc lock-in 测试。
4. **Part B1 (defect b)**: claim schema 可选 `linked_issue` (additive, 6 构造点穿线) + `phase1_gate --linked-issue` + 输出 additive 键 `linked_issue_overlap[]` (「同 issue 两个名字」advisory) + 纯函数 `collision.linked_issue_overlaps`。
5. **pre-merge 对抗 review R1**: 1 Critical —— sweep 复用 STALE_TTL=30min 会把并行活 session durable 判死 (heartbeat 零生产调用, heartbeat_at 冻结在 acquire) = 自拆协调目标; 改新常量 **SWEEP_TTL=24h** + 误杀锁定测试。5 Important (I1 多 claim 全释放 / I2 resilient_push + push_success 文档 / I3 CAS / I4 linked_issue CLI e2e 测试 / I5 skip 谓词可判定) + 7 Minor 全修。
6. **一次性清理真 ref**: 4 条本容器 stale release→done + bot runtime-probe sweep→abandoned + 2 条 GC 归档; 清理后唯一 active = 本 cycle claim → D.2b dogfood 释放 ✓。
7. 测试 968→1006 (+38); **顺手修假绿**: test_release_by_track 原 pytest 裸函数在 stdlib unittest runner 下从未被执行。
8. follow-up 双票: aria-orchestrator#31 (bot dispatch 强制 claim, defect a Layer 2 维度) + aria-plugin#107 (heartbeat 生产接线, SWEEP_TTL 收回的前置)。

## §2 未完成 / Carry-forward

- 无 (本轨全闭环; follow-up 已开票不入 carry)。
- (承前) M6 owner 4 门 / M7 D3 门 / aria-plugin#101 / i18n README @1.51.0 (custom check STALE, #140 B 档待正文实质变更时重译)。

## §3 关键风险 / 已知陷阱

- **durable 状态改写的 TTL ≠ advisory 判定的 TTL** (本 session 核心教训): reconcile 的 stale_takeover_eligible (30min) 是可逆 advisory, sweep 的 abandoned 是不可逆改写 —— 后者阈值必须按「无 heartbeat 基建的现实」定 (24h), 不能想当然复用常量。tasks.md 里我自己写的"活 session 必已 heartbeat"与 proposal 里"heartbeat 零生产调用"自相矛盾, review 抓出。
- **pytest 裸函数在 stdlib unittest runner 下静默不执行** = 假绿。repo 用 unittest discovery 的, 测试必须写 TestCase。
- **probe 分区不按 symbol 过滤**: 新 CLI 的遥测别写进 run_gate 的 coordination-telemetry.jsonl, 会虚增探针计数 (raw-count 膨胀坑) — release_gate 用独立分区文件。
- **release/GC 语义键**: 释放按业务键 (track_id+container) 不按 session (fresh session_id 永远匹配不上); retention 按 heartbeat_at (=终结时刻) 不按 claimed_at。
- cwd 相对路径跑 run_tests.py 会 file-not-found 且管道 grep 出"无失败"假绿 —— 断言测试真跑了 (看 "Ran N tests")。

## §4 实战教训 (memory 沉淀)

- 候选: durable-rewrite TTL vs advisory TTL 分离 (上条 §3 第 1 点) —— 收尾后落盘。
- 上一 handoff 两条候选 (抢先ship≠质量更高 / 自主bot独立接活) 已在 memory (MEMORY.md 确认在索引)。

## §5 多维度同步状态

| 维度 | 状态 |
|------|------|
| aria-plugin | **v1.56.0** @ `504da89` (PR#106; origin=github ✓); wip/coordination-part-c 已并入 (可删) |
| 主仓 | 本 commit: spec 归档 + gitlink + VERSION/README badge/CLAUDE.md + 本 handoff |
| standards / aria-orchestrator | 未变更 |
| Forgejo | 关 #159 #160; 开 aria-orchestrator#31 + aria-plugin#107 (follow-up) |
| 协调 ref | 干净: 0 stale active; 本 cycle claim released (D.2b dogfood); terminal 记录待 7d retention GC |
| OpenSpec | 本 spec 归档 `2026-07-11-coordination-claim-lifecycle-and-overlap`; active 剩 M6×4 + M7×2 |

## §6 Next session 入口 + 优先级建议

1. (承前) M6 owner 4 门 (build/deploy/egress/E2E dogfood + Blocker 4 Luxeno) —— input-delivery/遥测两 spec 卡此。
2. aria-plugin#101 / #158 (aria-report 版本抽取恒报 1.47.0 — 本 session 又实证一次: #159 票内版本不可信)。
3. follow-up 自然节奏: orchestrator#31 (bot 强制 claim) 可搭下次 orchestrator cycle; plugin#107 (heartbeat) 低优。
4. 惯例: 大活前 fetch 三仓 + B.0 claim (本版起默认强制, phase-b-developer B.0 成文)。

## §7 提交清单 (multi-remote parity)

- aria-plugin: v1.56.0 `504da89` (PR#106 merge; origin ✓ github ✓)
- 主仓: 本 commit (归档 + 5 文件同步 + handoff; 推 origin + github)

## §8 Memory entries this session

- 候选 1 (§4): durable-rewrite TTL 与 advisory TTL 必须分离 —— 收尾后落盘。

## Cross-references

- spec 归档: `openspec/archive/2026-07-11-coordination-claim-lifecycle-and-overlap/`
- aria PR#106: https://forgejo.10cg.pub/10CG/aria-plugin/pulls/106
- 关票: [#159](https://forgejo.10cg.pub/10CG/Aria/issues/159) / [#160](https://forgejo.10cg.pub/10CG/Aria/issues/160); 开票: orchestrator#31 / plugin#107
- 前序 handoff: partB-v1.55.4-and-coordination-spec (同日)

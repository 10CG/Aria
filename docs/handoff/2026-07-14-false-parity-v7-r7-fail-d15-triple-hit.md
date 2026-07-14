---
track-id: state-scanner-stale-refs-false-parity
linked-issue: 10CG/aria-plugin#110
owner-container: simonfish/bfe8285d
phase: A.1-postspec-R7
status: active
updated-at: 2026-07-14
---

# Session Handoff — 接手 bot 轨: v7 (F10″ 重写 + D15-D17 代裁) → R7 FAIL 3/3

> owner /goal「1+2 都做」: 1=接手 false-parity 轨做 F10″→v7→R7; 2=裁 3 条待裁。两者完成; R7 FAIL 是流程正常产物 (本轨 R1-R7 全 FAIL, 单调收敛)。

## §0 入口 (新 session 优先读)

- **下一步 = 按 R7 聚合报告折 v8 → R8**。修法全部写在 [`post_spec-R7-2026-07-14-*-aggregated.md`](../../.aria/audit-reports/post_spec-R7-2026-07-14-state-scanner-stale-refs-false-parity-aggregated.md) (RC-1..8 / RM-1..12, 每条带锚), proposal Status 行有 v8 待办核心速览。
- 🔴 **v8 的两个非机械决策点**: (a) **D15′ 双角色窗拆分** (∃ 证据资格=短墙钟窗 / ¬blocking 豁免=代际窗) — backend C-3 给的方向, 是 RC-3/RC-4 的合并解, 但它是**新核心谓词 = 第 11 次复发候选位**, v8 起草时按第八次复发的教训自查对偶; (b) **RC-8 升格裁定** (¬可信腿 orphan_unverified 持续 ≥k 代升 blocking vs 显式接受) — 涉及 advisory 被吞史, 建议 owner 过目。
- 本 session 的 D15-D17 是**代裁** (owner /goal 授权), D15 被 R7 打出 3C — 代裁被审计修正是机制在工作, D16/D17 三方无异议存活。

## §1 已完成

1. **接手交割**: claim 带 `--linked-issue aria-plugin#110` (v1.56.1 新参数 dogfood, 无重叠); bot handoff §6 全项消化。
2. **CE 归因复验结案** (agent 干净条件 5 组对照): custom_checks **确是**漂移通道 (条件=缓存缺失/mtime>30min); R5/R6 矛盾根源=缓存新鲜度隐藏变量; 通道 4→**6** 条; 根治=offline 旁路为主 (契约字段被 test_rule_4 pin 死, DROP_KEYS 结构性不可用于通道 #5)。→ 12.10 v7 重写 + **Spec C v3** (撤回的条件性反转)。
3. **3 条待裁 → DEC v8 §3c (D15-D17, 代裁标注)**: D15 可信窗代际制+7d 硬上限 / D16 横扫表搬 aria-plugin + 机械 lock 测试 / D17 ls_remote 退役 (强验归 C.2.5 gate 独立脚本)。
4. **v7** (`ed21aba`): tasks §13 按 F10″ 重写 (9 任务, 定义域五分支) + AC-16/17 重述 (含反惯例 trunk fixture) + R6 全部 7 Major 折入 (M-1→D15/M-2→3.5d 退避/M-3→3.14 shim/M-4→免疫/M-5→D16/M-6→12.10 粒度/M-7→3.15+F6′ 精化) + 横扫表登记 gitlink_orphaned。
5. **R7 三视角审计** (backend/qa/复发狩猎, 全 code-grounded + 真 git 实验): **FAIL 3/3**, 去重 8C/12M/10m, 聚合已落盘。判定质量高 — 两方独立算出同一笔 k/rotation 账; 狩猎场抓到 no-prune 视图这个「原语对了但喂数视图错了」的新宿主。
6. 顺手同 commit 修掉 v7 自引入的 proposal Verification stale 段 (qa M-3) + Status 收敛。

## §2 未完成 / Carry-forward

- **carry-v8-fold**: 按聚合报告折 v8 (RC-1..8 全部 + RM-1..12; 两个非机械点见 §0) → R8 窄范围 (RC 修复文本 + D15′ 重点对抗)。
- **carry-spec-c-v4**: Spec C 求值基底裁定 (RC-7: lag-1 两跑断言 vs 挪位) — 一票否决级, v4 必答。
- (承前) bot handoff 的落地顺序不变: Spec C → Spec B → 主 Spec; M6 owner 4 门 / carry-136-rotation / 168h 跑。

## §3 关键风险 / 已知陷阱 (增量)

- **复发宿主谱系再 +2**: (10 候选) 原语的**喂数视图** (no-prune fetch 看不见 ref 删除 — 原语选对了, 喂它的数据视图有结构性盲区); (11 候选) 新窗口的**参数耦合** (k 与 rotation 脱钩 — 每引入带参数的窗, 必须写死参数间的收敛不等式并用生产实测数字代入验证)。加上 fixture 参数反推 (把 fixture 预算调到公式恰好成立) = 假绿的新形态。
- **代裁的正确姿势**: D15 三中弹但这恰是把裁决置于 R7 复核之下的目的; 教训是代裁核心谓词时应当场做 R7 级别的推演 (split-brain 落位横扫 + 参数代入), 而不是留给审计。
- CE 实验方法论: 带 git-status 前后快照的重跑可以把并发污染通道与目标通道干净分离 — 复用价值高。

## §5 多维度同步状态

| 维度 | 状态 |
|------|------|
| 主仓 | 本 commit (v7 收敛 + R7 聚合 + 本 handoff); 推 origin+github |
| aria-plugin / orchestrator / standards | 未变更 (v1.56.1 / 86bb684 / 79b7cd6) |
| 三 spec | 主 Spec Draft v7 (R7 FAIL 收敛) / Spec B v2 (未动) / Spec C v3 (待 v4 裁基底) |
| DEC | v8 (D15-D17 代裁; D15 待 v8 修订为 D15′) |
| 协调 ref | 本 cycle claim 收尾释放 |

## §6 Next session 入口 + 优先级

1. ⭐ **v8 折入 + R8** (carry-v8-fold; 两个非机械点先裁)。
2. (承前) M6 owner 4 门 / carry-136-rotation。
3. 低优: plugin#107/#109 / orchestrator#31。

## §8 Memory entries this session

- 候选: 「带参数的窗必须写死参数间收敛不等式并用生产实测数字代入」(复发形态 11 的一般化) — 收尾后落盘。

## Cross-references

- R7 聚合: `.aria/audit-reports/post_spec-R7-2026-07-14-state-scanner-stale-refs-false-parity-aggregated.md` (三方原文在同目录 R7-{backend,qa,hunter} 视角段内聚合)
- v7 commit: `ed21aba`; 前序 handoff: 2026-07-12-false-parity-r5-r6-f10-primitive-swap (bot)

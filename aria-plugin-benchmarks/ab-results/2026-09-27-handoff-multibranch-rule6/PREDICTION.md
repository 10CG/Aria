# PREDICTION — Rule #6 AB `state-scanner` (`10CG/Aria#195` handoff-multibranch-subdir-path-fidelity, TASK-026)

> 写于 26 臂 (13 eval × 2 臂) 派出**之前** (2026-09-27T16:5xZ, 精确时刻见本轨台账 §TASK-026)。事后不改本文件, 只在 RESULT.md 对账。

## 臂与口径

- 口径写死为 **「代码 + 文档整体」**: 区分力不归因到文档。
- `with_skill` = aria feature `feature/handoff-multibranch-subdir-path-fidelity` @ `b181678619023910bb4eed7266afc765ce937322` (= TASK-021 回归前记录的 HEAD), 路径 `/home/dev/Aria/aria/skills/state-scanner` (开跑前断言 HEAD 等于该 SHA 且 `status --porcelain` 为空)。
- `old_skill` = B.1 基线 aria `1cb387218935433312fde4067c276754b77686a8` 的一次性 worktree, 建在会话 scratchpad (`.../scratchpad/old-arm-1cb3872`)。
- 套件: `ab-suite/state-scanner.json` version 1.7.0, 13 eval / 78 条断言, 本次未改。
- `ARIA_COORDINATION_NO_PUSH=1` 已核 (子进程 `no_push_requested_by_env()` → `True`); 协调 ref 基线 本地 = origin = `e911132`。

## 两臂到底差在哪 (派臂前实测, 决定预测)

- `SKILL.md` 两臂**逐字节相同** (`git diff 1cb3872 b181678 -- skills/state-scanner/SKILL.md` 为空)。本 cycle 在 state-scanner 下改的是 `collectors/handoff_multibranch.py` / `scan.py` / `writers/latest_md_writer.py` + 三份 references 文档 + 测试。
- 派臂前在本仓根对两臂 `scan.py` 各跑一次 (输出写 scratchpad, 不是臂运行): 两份 snapshot 除时间戳 / 缓存来源外, **唯一的结构差异**是 with 臂 `tracks_multibranch` 多了 `unreadable_count: 0` 与每条 track 多一个 `rel_path` 键; 去掉这两个新增键后 2040 条 track **完全相同**, `legacy_count` 两臂同为 336, `collision.kind` 两臂同为 `self_multi_container`。原因: 本仓与全部 origin 分支的 `docs/handoff/` 都是平铺 (TASK-002 已证), 本 spec 修的子目录路径在真仓里**没有输入**。
- 套件对 `handoff_multibranch` / `legacy` / `basename` 零命中, `tracks_multibranch` 只在 eval 13 题面出现一次且把 `collision.kind` 的取值写死在题里 (proposal rule6_note 已预判: 结构上测不到 collector 输出变化)。

⇒ 两臂 AI 可见的输入差异只有两个新增键, 且没有任何 eval 的断言会读它们。

## 逐 eval 预测

点估计取 2026-09-05 同套件先例 (`ab-results/2026-09-05-v1.70.0-a1-entry-rule6/SCORES.md`) 的 with 臂实测分 —— 那次的 with 臂已含 A.1 心跳小节, 与本次两臂的 SKILL.md 同代; 仓库状态已变, 绝对分可能漂移, 但**两臂同向漂移**。

| eval | 断言数 | with | old | 依据 |
|---|---|---|---|---|
| 1 basic-state-collection | 3 | 3/3 | 3/3 | 两臂同一 SKILL.md, snapshot 实质相同 |
| 2 user-options-display | 2 | 2/2 | 2/2 | 同上 |
| 3 readme-sync-detection | 3 | 3/3 | 3/3 | 同上 |
| 4 config-awareness | 3 | 3/3 | 3/3 | 同上 |
| 5 submodule-sync-detection-new | 6 | 3/6 | 3/6 | 同上 (先例两臂 3/6) |
| 6 upstream-behind-detection-new | 6 | 2/6 | 2/6 | 同上; 先例两臂曾 2 vs 4 —— 这是已知高方差条 |
| 7 issue-awareness-opt-in-new | 8 | 4/8 | 4/8 | 同上 |
| 8 readme-skill-count-badge-check | 8 | 5/8 | 5/8 | 同上 |
| 9 forgejo-config-detection | 7 | 6/7 | 6/7 | 同上 |
| 10 multi-remote-parity-drift | 12 | 9/12 | 9/12 | 同上; 最大的一条, 最可能出随机波动 |
| 11 submodule-push-github-sync-miss | 9 | 5/9 | 5/9 | 同上 |
| 12 (未命名, 跨仓 linked_issue 重叠) | 5 | 5/5 | 5/5 | 纯问答, 不读 snapshot |
| 13 a1-heartbeat-on-entry-TARGETED | 6 | 6/6 | 6/6 | 两臂都有该小节; 题面写死 `collision.kind` |

## 汇总预测

- 断言总数 78; with ≈ 56/78, old ≈ 56/78。
- **delta.pass_rate = mean(with) − mean(old) 预测 ≈ 0** (期望值 0; 单次采样噪声下 |delta| ≤ 0.05 都视为与 0 相符)。
- ⇒ 按预测, AB_TEST_OPERATIONS.md 场景 1 的验收 `delta.pass_rate > 0` **不会达成**, 回归面**未被有效测试** —— TASK-026 的 owner 裁决点**按预期会触发**。这写在跑之前, 免得事后拿聚合数字做任何方向的文章。

## 可证伪的失败预期

1. **任一 eval with < old** ⇒ 按 TASK-026 判据该 eval 复跑两次, 三个样本中 ≥2 个仍 with < old ⇒ 判回归, 阻断 TASK-027 / TASK-029 并上报 owner。先验上这只能是采样噪声 (两臂 SKILL.md 相同、snapshot 实质相同), 但**不得**据此先验跳过复跑。
2. **with 明显高于 old (某 eval 差 ≥2 条)** ⇒ 同样可疑: 两臂输入几乎相同, 大差距更可能是臂的执行路径出错 (跑到同一份 / 错的 scan.py) 或采样噪声, 须先核 transcript 里的 scan.py 路径。
3. **任一臂 transcript 出现 `phase1_gate` / `release_gate` 且 `push_skipped: false`** ⇒ 该 run 作废, 立刻 `ls-remote` 核远端。
4. **任一臂在 eval 13 答成「先跑 phase1_gate 认领」** ⇒ 两臂同一小节, 属 SKILL.md 指令面与本 cycle 无关的既有缺陷, 记入 RESULT, 不改断言。

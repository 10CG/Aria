# 3c 主控复核: 结果 (2026-10-24 14:20-14:40Z)

预期在 PREDICT.md (实测前写下)。对象: worktree 未提交改动 (套件 d085afae6834 / helper 213d01379695 / 垫片 5c5c04525a67, hook af4658b6f935 不变) 与主仓 v31/run-suite.sh。脚本: branches.py (6 组两支对照)、refcheck.sh (参照表对原始日志)、mkprobe.py (参照负控副本)、drive.sh (实跑), 时间线 drive.log。

## 静态

| 项 | 预期 | 结果 |
|---|---|---|
| S1 hook | af4658b6f935 | 相符 |
| S2 6 组基线支 | 与 fee1a65 逐行相同; 10 条触发点命令的 limit 行与 else 段一一对应 | 相符: 6 组 else 段逐行相同; 21ab 三条与 21ag、21aj 三条对 $wpa_L_seg, 21ac、21al、21ao 对 $wpa_L_whole, 与各自 else 段的 wpa_x_toolarge 相同; 放宽断言种类与 HEAD 的原断言一一对应 (longline / pass / growth) |
| S3 只跑一次 hook | wpa_x6_eval 只换 wpa_err / wpa_rc | 相符: wpa_x、wpa_x_longline、wpa_x_toolarge 只经 wpa_rc / wpa_err 取结果, 子 shell 里两者都换成交回同一份输出 |
| S4 参照表 | 与原始日志逐条相符 | 相符: 59e333c 与实现各 5 个 bash, 读出 25 处 (3.2 上 23 处, 两条直调为 SKIP [platform]), 0 处与 sg_w10_ref / fbref 不同 |
| S5 垫片 | 非注释行不变 | 相符 |

## 实跑 (PATH 上的 bash 5.2.15)

| 轮 | 预期 | 结果 | 负载 开 / 尾 |
|---|---|---|---|
| R2 BI-8 (我自己构造, sha ff9f7a43eb7e, 与 mutants.py 相同) | V9-E12 FAIL [reference], 退出 1 | 相符: `gate-closed arm rc=0 none, reference (59e333c) rc=2 vmax [reference]`, 退出 1 | 0.83 / 0.84 |
| R3 参照负控 (我改错三处) | 三处 FAIL [reference], V6-S21 过; PASS 1 / FAIL 3 | 行为相符: V7-E1 `gate-closed arm rc=2 oversize, reference (59e333c) rc=2 vmax [reference]`; V1-E16-p1-small-benign `rc=unrecorded - [reference]`; V6-S20 `status 2 oversize, reference (59e333c, the same copy and mode) 2 vmax [reference]`; V6-S21 过; 退出 1。**计数预期错**: 实为 PASS 3 / FAIL 3, 我漏算了过滤轮恒在的 V0-H1 / V0-H2 两条 (R2 同理, PASS 2 / FAIL 1) | 0.84 / 0.84 |
| R1 过滤轮 SG_W10_ONLY=. | 136/0/0, 无 [reference], 计时批 judged | 相符 | 0.84 / 1.03 |
| R4 worktree 整轮 | FAIL 0, 961, SC-13 绿, 截止回落 0 / 10 | 相符: PASS 961 / FAIL 0 / SKIP 0, W10 计时批 judged (1.14 收尾), 6 组走放宽支, `deadline fallback (截止回落) 0 / 10` | 0.88 / 2.68 |

## 复核中的新发现 (写进计划 notes 的 3c 主控裁定)

3c 报告第 6 节第 1 条 (2.85 s 下界分不开「门关、立刻基线拦截」与「截止回落」) 成立。主控复核 hook 时另发现反方向的洞: 作业里的重跑有自己的时间检查点 (`_sg_vx_collect` 重置 `_SG_T0=$SECONDS`, `_sg_over_budget` 在整秒差 >= 3 时让重跑返回 3, 回落成基线拦截, hook `:612-632`、`:648`、`:722`、`:798`), 它在重跑开始后 2-3 s 触发; 基线那一遍快 (< 1 s) 的命令, 这样的合法回落墙钟落在 2-3 s 之间, 2.85 s 会把其中一部分判红。3b 的裁定只想到准入门与截止两条路, 漏了这一条; 2.85 s 是从截止类用例抄的, 不是推出来的。改定的判法 (2 s 以下判红、3 s 以上认回落、中间用关门重跑的墙钟区分) 交 3c2 实现, 任务书 BRIEF-T002c-3c2.md。

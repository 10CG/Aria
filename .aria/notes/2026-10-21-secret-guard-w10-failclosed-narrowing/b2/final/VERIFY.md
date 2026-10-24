# TASK-002 最终整轮: 结果 (2026-10-24 17:53-18:46Z)

预期在 PREDICT.md (开跑前写下)。对象: aria 分支 acb644b 的 git 检出 (工作区干净); hook af4658b6f935, 套件 d4168aace3e8, helper 213d01379695。驱动 drive.sh (七轮与 commentsync)、rerun50.sh (5.0 补跑), 时间线 drive.log。每轮开跑前一分钟负载 < 1.2 (补跑 < 1.0)。

| 轮 | 结果 | W10 批负载 开 / 尾 | 计时批 | 6 组 |
|---|---|---|---|---|
| SC_BASH 5.2.15 | PASS 961 / FAIL 0 / SKIP 0 | 1.19 / 1.40 | judged | 放宽支, 截止回落 0 / 10 |
| SC_BASH 5.0.18 | PASS 932 / FAIL 0 / SKIP 29 [void] | 1.04 / 2.06 | void (尾读数 >= 2, INV-7 作废) | 放宽支, 0 / 10 |
| SC_BASH 5.0.18 补跑 | PASS 961 / FAIL 0 / SKIP 0 | 0.79 / 0.88 | judged | 放宽支, 0 / 10 |
| SC_BASH 5.1.16 | PASS 961 / FAIL 0 / SKIP 0 | 1.17 / 1.13 | judged | 放宽支, 0 / 10 |
| SC_BASH 5.3.20 | PASS 961 / FAIL 0 / SKIP 0 | 1.18 / 1.06 | judged | 放宽支, 0 / 10 |
| SC_BASH 3.2.57 | PASS 903 / FAIL 0 / SKIP 58 [platform] | 0.95 / 1.24 | judged | 放宽支, 0 / 10 |
| 导出 WSL_DISTRO_NAME=Ubuntu | PASS 961 / FAIL 0 / SKIP 0 | 1.12 / 0.93 | judged | 基线支, 0 / 0 |
| 导出 WSL_INTEROP | PASS 961 / FAIL 0 / SKIP 0 | 0.99 / 0.87 | judged | 基线支, 0 / 0 |
| commentsync target (worktree 的 hook 与套件) | GREEN (194 处 ok) | | | |
| commentsync baseline (59e333c 的 hook 与套件, e83c5e30f2cc) | GREEN (184 处 ok) | | | |

预期全部相符 (5.0 首轮正是预期里「未判时 PASS 932 + SKIP 29」那一档, 按 INV-7 补跑后判过)。每轮 961 个用例里移植用例的编号数相同 (136; V0-H2 核对编号清单逐平台一致), SC-13 每轮都绿 (FAIL 0 已含 SC-13)。

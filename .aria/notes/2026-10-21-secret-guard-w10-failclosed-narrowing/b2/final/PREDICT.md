# TASK-002 最终整轮: 预期 (2026-10-24, 开跑前写下)

对象: aria 分支上 3e 提交后的 worktree (git 检出, 工作区须干净); hook af4658b6f935。全部为整轮, 开跑前一分钟负载 < 1.2。
SC_BASH 只决定移植用例 (W10 批) 用哪个 bash 执行 hook; 6 组既有用例按 PATH 上的 bash (5.2.15) 与环境里的 WSL 标记分支。移植用例的两臂在 sg_w10_run 里先清掉 WSL_DISTRO_NAME 与 WSL_INTEROP (套件 :252), 所以环境里导出的 WSL 标记只影响 6 组。

- F 5.0.18 / 5.1.16 / 5.2.15 / 5.3.20: FAIL 0; W10 计时批判过时 PASS 961, 未判时 PASS 932 + SKIP 29 ([void] 或 [load]), FAIL 仍为 0; SC-13 绿; 6 组走放宽支, 截止回落 0-2 / 10 (多半 0)。
- F 3.2.57: FAIL 0; W10 批 78 PASS + 58 SKIP [platform]; 判过时总计 PASS 903 / SKIP 58; 6 组走放宽支 (PATH 上的 bash)。
- F 导出 WSL_DISTRO_NAME=Ubuntu: FAIL 0; W10 批照常 (relaxation expected: yes, 136 条按判没判计); 6 组走基线支, 截止回落 0 / 0 (基线支不经 wpa_x6)。
- F 导出 WSL_INTEROP: 同上 (3b 已跑过一次, 结果 0 FAIL、6 组走基线支)。
- commentsync: target (worktree 的 hook 与套件) GREEN; baseline (59e333c 的 hook 与套件) GREEN。

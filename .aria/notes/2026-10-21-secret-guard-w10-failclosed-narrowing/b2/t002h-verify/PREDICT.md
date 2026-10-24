# 3e 主控复核: 预期 (2026-10-24, 3e 交回之前写下)

对象: 3e 交回的 worktree 套件改动 (起点 df2d629) 与主仓 v31/run-suite.sh 的改动; hook af4658b6f935 不变。

静态:
- 套件 diff 只在 wpa_x6 的 (b) 支 (关门重跑至多 3 次、间隔 1 s、首个满足即停)、Summary 的 (b) 项 (第 k > 1 次才满足时带 (try k))、wpa_x6 上方注释块 (重试与理由; 删掉 sha256 af4658b6f935) 与可能的 6 组共用注释一句; 其余不变。
- run-suite.sh: SC_BASH、SG_W10_LOG 改 readlink -m; SG_W10_LOG 的目录不存在时退出 3; 头注释同步。

实跑 (主控自己的构造, 都以 C3 为底: 作业在计时器起来后 2.2 s 让重跑回落; 包装脚本按输入记数, 只让设了 WSL_DISTRO_NAME 的调用卡 1.5 s; 被 source 时直接交给 C3, 不读 stdin):
- V-S2 每个输入的前 2 次关门调用各卡 1.5 s: 6 组全部 PASS, 截止回落 10 / 10; 走 (b) 的那些 (约 7 条) 带 (try 3), 走 (a) 的不变。
- V-S3 前 3 次都卡: 走 (b) 的命令 3 次读数都约为 Tb + 1.5 s, 大于 W - 1.0 s (W 约 Tb + 2.2 s), 判不符, 细节列 3 个读数; 21ab (wpa_vx_cmd 159)、21ac、21al、21ao 必红, 21aj 多半红 (除非三条都因截止先到走 (a)); 21ag 走 (a), 照过。截止回落只剩走 (a) 的那几条。
- V-C5 作业 0.5 s 后就失败 (a4b04f1f97cf): 6 组全部 FAIL; 21ab 两条填充命令走 (b), 3 次读数都约为 W - 0.5 s, 判不符。
- V-R1 SC_BASH 指向父目录也不存在的路径, 经 run-suite.sh、SG_W10_ONLY=^V1-E16-p1-small-benign$: 套件 FAIL、退出 1, 首行记下原路径。
- V-R2 SG_W10_LOG 指向不存在的目录: run-suite.sh 退出 3, stderr 有说明。
- V-R3 正常过滤轮 (SG_W10_ONLY=^V1-E16, 带 SG_W10_LOG): 与改前同样全过, 日志逐行相同 (时间与负载之外)。
- V-impl worktree 整轮: FAIL 0, 961, SC-13 绿, 截止回落 0 / 10 (1-2 也不算错)。

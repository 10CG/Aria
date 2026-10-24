# 3e 第 2 步预期 (写于第二阶段开跑前; 新套件 = df2d629 + 本段改动, 新 run-suite.sh)

改动已落: 套件 5 处 (6 组共用注释 1、注释块 3、(b) 支 1), bash -n 通过, commentsync --suite-only GREEN; run-suite.sh 3 处。
构造 hook 与 3c2 / 主控复核同 sha: c1 93c7f2fac02a、c3 2a9e3d898705、c5 a4b04f1f97cf; C6 包装层 7884d94e0c1b。
附带实测: GNU readlink -m 遇到符号链接环不失败 (退出 0, 按字面给出路径)。

依据 (3c2 / 主控复核的读数): C1 旧轮 21ab 三条 W 0.63 / 2.34 (Tb' 2.37) / 3.35 s, 其余组全部 W < 2.0 s (0.17-1.14);
C5 旧轮 21ab 1.20 / 2.89 (Tb' 2.33) / 2.96 (Tb' 2.43) s, 其余 0.68-1.61 s。

## C6-new (新判法, 至多 3 次关门重跑)
- 走 (b) 的命令 (约 7 条: 21ab 快的一条、21ac、21aj 三条、21al、21ao): 第 1 次读数约 Tb + 1.5 s > W - 1.0 s 不满足, 等 1 s 后第 2 次
  约 Tb (0.16-0.7 s) 满足 -> 记截止回落, Summary 写 `W/Tb Xs (try 2)`。第 1 次就满足要 W 自己被拖长 >= 约 0.3 s, 低负载不预期;
  第 2 次也被卡 >= 约 0.6 s 才会出现 `(try 3)`, 不预期。
- 走 (a) 的命令 (约 3 条: 21ab 两条、21ag) 照记 `X.XXs`, 不带 Tb。
- 6 组全部 PASS, 截止回落 10 / 10。贴界的 21ab / 21ag 3.01 s、21aj 2.9x s 落在 (a) 还是 (b) 不影响组结论, 只改 (try 2) 的条数。

## C1-new (准入门恒关)
- 6 组全部 FAIL。W < 2.0 s 的 (约 8 条) 判不符 `want > 2.0 s`; 21ab 中间那条 W 约 2.3-2.4 s 落在 (b) 窗口: 三次读数都约等于 W,
  细节列 `gate-closed Tb' a, b, c` 三个读数, 判不符; 21ab 慢的那条 W 约 3.3 s 记截止回落 (固有限度), Summary 约 1 / 10。

## C5-new (主控的快速失败构造: 作业在计时器起来后 0.5 s 以 1 结束)
- 6 组全部 FAIL。21ab 两条慢的 W 约 2.9 s 落在 (b): 三次读数约 2.3-2.5 s (约 W - 0.5), 都 > W - 1.0, 列三个读数判不符;
  其余 W < 2.0 s 判 `want > 2.0 s`。截止回落 0 / 10; 若 21ab 慢的那条 W 越过 3.0 s, 记回落 (固有限度), 逐条列出。

## 实现整轮 (worktree, PATH 上的 bash, 直接跑套件, 低负载)
- PASS 961 / 961、FAIL 0, SC-13 绿; 6 组走放宽支, 截止回落 0 / 10 (3c2 同条件 0 / 10)。若有回落, 只可能在负载偏高时出现, 逐条记下。

## run-suite.sh 三项
- (ii) `SG_W10_LOG=<t002h>/no-such-dir/w10.log`: 退出 3, stderr 一行 `run-suite.sh: SG_W10_LOG ...: its directory does not exist ...`,
  套件不跑 (没有首行与尾行), no-such-dir 仍不存在。
- (iii) 过滤轮 `SG_W10_ONLY='^V1-E16'` 带 SG_W10_LOG, 新 run-suite.sh 跑两次 (旧套件快照 / 新套件), 与改前那次比: 日志行数相同,
  抹掉 `N.NNs` 读数后逐行相同 (raw diff 只在墙钟读数上); 套件输出去掉首尾行、抹掉读数后相同, 若仍有差异只应是带负载读数的行。
- (i) `SC_BASH=<t002h>/no-such-dir/sub/bash`、`SG_W10_ONLY=.`: 首行 `SC_BASH <t002h>/no-such-dir/sub/bash` (原路径, 不再是 bash on PATH),
  套件报 FAIL (3d 同类读数为不存在的文件 FAIL 135), 退出 1。

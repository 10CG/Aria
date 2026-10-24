# T002c-3b 主控复核: 开跑前写下的预期 (2026-10-24, 先写后测)

对象: worktree 未提交改动 (套件, 3a64827 之上 +145 / -45) 与主仓 v31/commentsync.py。hook af4658b6f935 不变。
每轮开跑前等一分钟负载 < 1.2; 重实验串行, taskset -c 0,1 nice -n 19。

R4 计时探针 (先跑, 轻): 21ab 放宽支里两条应放行的命令 (b) f=x; echo $f<9000 填充> 与 (c) f=x; echo $f< a x4500>, 各 3 次, 直接喂 hook。
   预期: 都 rc 0 (放行), 墙钟 2.2-2.7 s (执笔席在负载约 1.5 时量到 2.49-2.78 s); 同一命令关门 (WSL_DISTRO_NAME=Ubuntu) 时 rc 2、尺寸文案, 墙钟 < 1 s
R3 commentsync: target (worktree hook + 套件) GREEN; baseline (59e333c 的 hook + 套件) GREEN;
   构造 (只在副本上): 删掉第 12 处 (21ag) 改写后的整段注释 -> RED; 第 9 处一条新句改一个字符 -> RED
R1 整轮, PATH 上的 bash (SC_BASH 缺省): 总数 961, SKIP 0, 计时批 judged (W10 批现在最先跑), Summary 显示 6 组走 relaxed branch, SC-13 绿。
   FAIL 点预测 0; 已知风险: 6 组排在套件后部, 那时负载常已过 2, 21ab 的 (b)(c) 若撞上 3 s 截止会回落成尺寸文案, 那就是 SC-21ab 1 条 FAIL (exit 2, 想要 0) —— 这是执笔席报告的待裁定项, 不算复核不符
R2 整轮, 只导出 WSL_INTEROP (执笔席没单独跑过的那个输入): 总数 961, FAIL 0, SKIP 0, Summary 显示 6 组走 baseline branch; 移植用例照常放宽 (端到端清掉两个 WSL 变量), 编号 136, 计时批 judged; SC-13 绿

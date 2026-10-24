# TASK-003 第一段主控复核: 预期 (2026-10-24, 实跑前写下)

静态 (已做): hook af4658b6f935 未动; 三个冻结物的 sha256 与报告相同 (FROZEN.sha 记于 19:04:12Z, 第一轮上机 19:10:54Z 起); 五个 V14 用例在 helper 与 v31/sc-direct.sh 里逐行相同 (41 行); sc-cases.sh 只在期望编号清单里加了五个编号; 套件只改 SGW_EXP_DIRECT 与头注释两个计数 (967 -> 972, 136 -> 141)。

实跑 (PATH 上的 bash 5.2.15 除另注; 开跑前一分钟负载 < 1.2):
- V-W14 用 w14.sh 在主控自己的目录里重新生成 31 个坏实现并跑预计用例 (W14_FULL=0): 末行「caught as predicted 26, caught by the added case 5, caught elsewhere 0, not judged 0, NOT CAUGHT 0」; 逐个结论与交付的 W14-independent-mutants.txt 相同 (按编号比)。若首尾负载过门槛, 计时类的 Q-16、Q-17、Q-24 会是 not judged, 其余不变。
- V-full worktree 整轮 (git 检出): FAIL 0, 966/966 (计时批未判时 937 + 29 SKIP), SC-13 绿。
- V-sc v31/sc-cases.sh 在实现上 (基线取 59e333c): 142 PASS / 0 FAIL / 0 SKIP。
- V-5x 只跑移植用例 SC_BASH 5.0.18、5.1.16、5.3.20: 各 141 PASS, 计时批判过。
- V-32 只跑移植用例 SC_BASH 3.2.57: 78 PASS + 63 SKIP [platform], FAIL 0。

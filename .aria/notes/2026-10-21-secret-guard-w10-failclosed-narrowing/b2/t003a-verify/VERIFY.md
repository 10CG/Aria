# TASK-003 第一段主控复核: 结果 (2026-10-24 19:50-20:13Z)

预期在 PREDICT.md (实跑前写下)。对象: worktree 套件 3351b47da825、helper 4f467588aef1 (起点 acb644b), 主仓 v31/sc-cases.sh 7d29c3cd0f5b、v31/sc-direct.sh fb3418921bca 与新建的 v31/impl/ (w14.sh、w14-mutants.py 4327121c903c、W14-independent-mutants.txt); hook af4658b6f935 未动。驱动 drive.sh, 时间线 drive.log。

## 静态

| 项 | 结果 |
|---|---|
| 冻结物 | w14-mutants.py、list.md、predict.md 的 sha256 与报告逐字相同; FROZEN.sha 记于 19:04:12Z, 第一轮上机 19:10:54Z 起 |
| INV-2 | 五个 V14 用例在 helper 与 v31/sc-direct.sh 里逐行相同 (41 行); 编号进 helper 的 RELAX_IDS / N_IDS、sc-direct.sh 的 N_IDS、套件的 SGW_EXP_DIRECT、sc-cases.sh 的期望清单 |
| 改动范围 | 套件只改 SGW_EXP_DIRECT 与头注释两个计数 (967 -> 972, 136 -> 141); sc-cases.sh 只改期望编号清单 |
| INV-8 | W14 首行的 suite、helper、sc-cases.sh、sc-direct.sh、mutants.py、w14-mutants.py 六个前缀与现在的文件逐个相同 |
| V2-G12 / G13 (Q-7 未被它抓住) | 只断言关门一极 (平台检查失败时 2 oversize、绝不 4); 开门一极 (返回 4、存对的原因串) 由 V14-G1 补上 |

## 实跑 (PATH 上的 bash 5.2.15 除另注)

| 轮 | 预期 | 结果 | 负载 开 / 尾 |
|---|---|---|---|
| V-W14 主控在自己的目录里用 w14.sh 重新生成 31 个坏实现并跑 | 26 按预期 + 5 由补的用例, 别处 / 未判 / 未抓住 0; 逐个结论与交付文件相同 | 相符: 末行 `caught as predicted 26, caught by the added case 5, caught elsewhere 0, not judged 0, NOT CAUGHT 0`; 31 个编号的结论与交付的 W14 逐个相同 (0 处不同) | 1.04 / 1.04 |
| V-sc v31/sc-cases.sh 在实现上 (基线 59e333c, e83c5e30f2cc) | 142 / 0 / 0 | 相符: PASS 142, FAIL 0, MISSING 0, SETUP 0, SKIP 0; V0-H2「all 140 expected case ids of mode relax」 | 1.04 / 1.85 |
| V-w10 SC_BASH 5.0.18 / 5.1.16 / 5.3.20 | 各 141 PASS, 判过 | 相符 | 1.14 / 1.06; 1.06 / 1.35; 1.18 / 1.24 |
| V-w10 SC_BASH 3.2.57 | 78 PASS + 63 SKIP [platform] | 相符 | 0.97 / 1.40 |
| V-full worktree 整轮 (git 检出) | 966/966, SC-13 绿 | 相符: PASS 966 / FAIL 0 / SKIP 0, W10 批判过 (1.13 / 1.05) | 1.13 / 2.79 (尾读数在 W10 批之后, 含套件自己的压测) |

预期全部相符。

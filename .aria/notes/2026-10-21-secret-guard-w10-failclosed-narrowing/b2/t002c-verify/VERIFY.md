# T002c-3a 主控复核记录 (2026-10-24 UTC 10:47 起; 预期见同目录 PREDICT.md, 写于开跑前)

对象: wt217/aria 的未提交改动 (套件 53f1eaefaf72 / helper 265a7b8d9b63 / 垫片 637c52c10bbf), hook af4658b6f935; 主仓 v31/run-suite.sh 711a0201e23b。
驱动 drive.sh: 串行, 每轮开跑前等一分钟负载 < 1.2, 全部 taskset -c 0,1 nice -n 19; 读数在 drive.log。比对脚本 check.py (只输出数字与编号)。

## 代码审读 (要点)
- 端到端每次起 hook 都 env -u 清掉 CLAUDE_PROJECT_DIR、_SG_RELAXED、SECRET_GUARD_TIME_BUDGET_S、WSL_DISTRO_NAME、WSL_INTEROP; 直调 helper 第 22 行同样 unset (沿用 v31)。
  所以外层环境导出 WSL_DISTRO_NAME 时, 移植用例照常测放宽; 只有 6 组旧用例 (经 wpa_err 把环境原样传给 hook) 会走基线, 这是 3b 的分支判据要算进去的输入。
- 关门臂: 端到端 sg_w10_run B 传 WSL_DISTRO_NAME=Ubuntu; helper 的 fbt 在 source hook 的子 shell 里 export 它, 并另设 _SG_P0 锚点, 使关门原因只有 WSL 标记。
- SG_W10_ONLY 过滤轮在移植块之后、第一条旧用例之前调用 sg_w10_cases 并退出; 正常轮在 SC-13 之前调用。计数 pass+fail+skip, SKIP 按原因分, 不影响退出码。
- 旧用例经 wpa_err 直接执行 $WPA_HOOK (shebang /usr/bin/env bash): 跑旧用例的是 PATH 上的 bash, 不是 SC_BASH。

## 结果对照预期
| 项 | 预期 | 实测 | 一致 |
|---|---|---|---|
| R1 W10-only 5.2.15 | 136 PASS, judged | 136 PASS, 负载 0.91 -> 1.12, judged | 是 |
| R1 W10-only 5.0.18 | 同上 | 136 PASS, 1.12 -> 1.35, judged | 是 |
| R1 W10-only 5.1.16 | 同上 | 136 PASS, 0.96 -> 1.68, judged | 是 |
| R1 W10-only 5.3.20 | 同上 | 136 PASS, 1.05 -> 1.29, judged | 是 |
| R1 W10-only 3.2.57 | 78 PASS + 58 SKIP [platform] | 78 PASS + 58 SKIP [platform], relax no, judged | 是 |
| R1 编号 | 每轮 136 个, 无重复 | 每轮日志 136 个编号, 0 重复 | 是 |
| R2 sc-cases.sh 对实现 (5.2) | 137 PASS, judged | 137 PASS, judged (0.96 -> 0.79) | 是 |
| R2/R5 按编号对齐 | 136 共有, 只差 V12-C1 | 136 共有、状态全同; only-v31: V12-C1; only-suite: 无 | 是 |
| R4 BI-24 | V2-G12 红 [status] | 红, 原因相符 | 是 |
| R4 BI-7 | V6-E2 红 | 红, 原因相符 | 是 |
| R4 BI-11 | V10-N3、V11-S4 红 | 都红, 原因相符 | 是 |
| R4 BI-5 | V2-G4 [status]、V2-E9 [bytes] 红 | 都红, 原因相符 | 是 |
| R4 BI-45 | V6-S20 [bytes] 红 | 红, 原因相符 | 是 |
| R4 BI-8 | V9-E12 PASS (指定用例上漏抓) | PASS: hook rc=0 none、gate-closed rc=0 none、IDENTICAL; 套件退出 0 | 是 (预期中的缺陷) |
| R4 实现对照 | 同批 8 个指定用例 + V0-H1/H2 全 PASS | 10/10 PASS | 是 |
| R3 整轮 5.2 (现位置) | 961, FAIL 恰 6 组, SC-13 绿, 计时批 SKIP [load] | 961: PASS 926 / FAIL 6 / SKIP 29 (全为 [load]); FAIL 恰为 SC-21ab、21ac、21ag、21aj、21al、21ao; SC-13 不在 FAIL 里 (通过时不打印); 整轮开跑负载 1.07, W10 批开始 2.74、结束 2.02 -> 计时批 SKIP [load]; 退出码 1 | 是 |

## 发现
1. 口径 (ii) 的漏洞 (主控 2026-10-24 定的口径, 不是执笔席的错): 关门臂跑的是被测 hook 本身。坏实现改的若是两臂共用的代码或常量,
   两臂一起变, 逐字节比对照样相同。BI-8 (_SGV_VMAX 4096 -> 8192) 在 v31 上由 V9-E12 抓住 (对照臂是真基线 59e333c), 在套件上 V9-E12 PASS。
   旧用例 SC-21ad / SC-21am (4097 字符的值被拒) 预计会在整轮里变红, 未实测; 它们不是指定用例, 不改变「指定用例上漏抓」的结论。
   designated.tsv 里指定用例是逐字节比对类端到端用例的坏实现只有 BI-5 (V2-E9) 与 BI-8 (V9-E12); BI-5 改的是只在放宽一侧生效的判定, 抓得住。
   补法交 3c: 关门臂另核基线对该输入的已知结局 (退出码与文案种类, 由 59e333c 实测成表), 不符记 FAIL [reference]。
2. 计时批位置: 见 R3 与 3a 报告第 6 节第 1 条; 主控裁定移到套件最前 (3b 做)。

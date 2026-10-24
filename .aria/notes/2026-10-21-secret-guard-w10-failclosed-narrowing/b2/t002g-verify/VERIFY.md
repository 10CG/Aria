# 3d 主控复核: 结果 (2026-10-24 16:28-16:34Z)

预期在 PREDICT.md (实跑前写下)。对象: 主仓 v31/run-mutants.sh 未提交改动 (460fb113a3ce); 套件 worktree df2d629 (60f7f95525cd); 实现 af4658b6f935; run-suite.sh 7584c219c4ba。驱动 drive.sh, 时间线 drive.log。

## 静态

- 不设 MUT_SUITE 时: 改动都在 SUITE 非空的分支里, 或只把读的文件由 <ID>.txt 换成 <ID>$RES, 非套件模式下 $RES 仍是 .txt, 逐字等价 (执笔席另做了改前改后 BI-8|BI-24 两轮 diff 为空)。
- 套件模式: verdict 读 SG_W10_LOG; 该文件含 `load start ... | timing batch: ...` 行 (抽查 all/BI-10.log), 所以「计时批未判」的旧逻辑照常生效。REFIDS 25 个编号与套件 sg_w10_ref (23) 加 helper fbref (2) 相同。漂移方向: REFIDS 少列一个只会更严; 多列一个也不会放过 —— 不走关门臂的用例根本不会出现 [reference]。

## 实跑 (PATH 上的 bash 5.2.15, 全是过滤轮)

| 轮 | 预期 | 结果 |
|---|---|---|
| V1 正样本 (主控挑: BI-8、BI-13、BI-45、BI-1、BI-24、P-0、P-M29) | 5 个 CAUGHT (BI-8 为 red[reference]); P-0 GREEN; P-M29 CAUGHT; 退出 0 | 相符 (BI-13 的 V3-E3 计时类在低负载下判红) |
| V2 negA (副本里改两处原因: BI-1 [rc] -> [bytes], BI-8 [bytes] -> [status]) | BI-1 WRONG-REASON; BI-8 CAUGHT (V9-E12 在 REFIDS 里, 带 [reference]); 退出 1 | 相符 |
| V2 negB (再从 REFIDS 删 V9-E12) | 两个都 WRONG-REASON; 退出 1 | 相符 —— [reference] 的放宽只对 REFIDS 里的用例生效, 原因表核对在套件模式下是活的 |
| V3 SC_BASH 指向父目录也不存在的路径 | 经 run-suite.sh 退出 0、W10 头行 SC_BASH 回落成 /usr/bin/bash; 直接跑套件 FAIL、退出 1 | 相符: run-suite.sh 首行记成 `SC_BASH bash on PATH` (readlink -f 清空了它), 套件 PASS 1 / 3 退出 0; 直接跑 FAIL 2 / 3 退出 1。3d 报告的 fail-open 属实 |
| V4 基线红集 (59e333c, sha e83c5e30f2cc 先断言) | PASS 24 / FAIL 112 ([missing] 74, [reference] 0); 与 base-5.2.15.txt 136 个编号状态逐个相同; 只在 v31 的是 V12-C1 | 相符 (cmp-base.py 另写, 只输出计数与差异: 0 处不同) |

负载: 开跑 0.57, 收尾 1.12, 每轮开跑前都 < 1.2 (V4 前等了 20 s)。

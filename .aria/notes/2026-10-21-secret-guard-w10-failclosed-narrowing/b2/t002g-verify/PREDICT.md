# 3d 主控复核: 预期 (2026-10-24, 实跑前写下)

对象: 主仓 v31/run-mutants.sh 未提交改动 (66 -> 104 行, 套件模式 MUT_SUITE)。套件 = worktree df2d629; 实现 af4658b6f935。

静态 (已读 diff):
- 不设 MUT_SUITE 时各分支与原来逐字相同 (改动都在 SUITE 非空的分支里, 或只把读的文件名由 .txt 换成 $RES, 而 $RES 在非套件模式下仍是 .txt)。
- 套件模式: verdict 读 SG_W10_LOG (含 timing batch 与 load start 行); 走关门臂的 25 个编号 (REFIDS) 上, 细节带 [reference] 即算对的原因; P-0 有 [platform] 以外的 SKIP 判 NOT-JUDGED。

实跑 (PATH 上的 bash 5.2.15, 开跑前一分钟负载 < 1.2; 全是过滤轮):
- V1 正样本 (我挑的, MUT_ONLY='BI-8|BI-13|BI-45|BI-1|BI-24|P-0|P-M29'): 5 个坏实现全 CAUGHT —— BI-8 的 V9-E12=red[reference]; BI-13 的 V3-E3 [wall>hi] (计时批须判过); BI-45 的 V6-S20 [bytes]; BI-1 的 V4-S6 [rc]; BI-24 的 V2-G12; P-0 GREEN; P-M29 CAUGHT; 退出 0。
- V2 原因表负控 (我构造: v31 目录的副本里改 mutants.py 两处原因 —— BI-1 的 V4-S6 由 [rc] 改成 [bytes], BI-8 的 V9-E12 由 [bytes] 改成 [status]):
  - negA (REFIDS 不动): BI-1 WRONG-REASON (V4-S6 不走关门臂, 实际原因 [rc] 对不上); BI-8 CAUGHT (V9-E12 在 REFIDS 里, 细节带 [reference]); 汇总 1 caught / 1 wrong reason, 退出 1。
  - negB (再从副本的 REFIDS 里删掉 V9-E12): BI-1、BI-8 都 WRONG-REASON; 退出 1。
- V3 环境错误 (3d 报告的 fail-open): SC_BASH 指向父目录也不存在的路径。经 run-suite.sh 跑 SG_W10_ONLY=^V1-E16-p1-small-benign$: 套件退出 0, W10 头行的 SC_BASH 变成 /usr/bin/bash (被 readlink -f 清空后回落)。同一个值直接在 worktree 跑: FAIL, 退出 1。
- V4 基线红集: 59e333c (sha 前缀 e83c5e30f2cc 先断言) 经 run-suite.sh 跑 SG_W10_ONLY=.: PASS 24 / FAIL 112 ([missing] 74, [reference] 0); 与 b2/t002b-verify/base-5.2.15.txt 按编号对齐 136 个, 状态逐个相同 (v31 的 MISSING 对套件的 FAIL [missing]); 只在 v31 里的是 V12-C1。

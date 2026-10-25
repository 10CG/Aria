# T004b 预期 (先写: 改 run-evidence.sh 与开跑之前, 2026-10-24)

## A. run-evidence.sh 四处改动
1. W9 页眉: 开跑前 H9=$(hdr), 块首行打印 H9, 末行 hdr 照旧 -> 新 W9-suite.txt 首行时间早于末行 (差约两轮套件耗时), 首行负载是开跑前读数。
2. TRAFFIC_DIR 前置核对: 选了 W12 而 TRAFFIC_DIR 为空 / 未设 / 没有 cmds 子目录 -> 退出 3, 工作目录不被建出, OUT 不被写; 不选 W12 的阶段不受影响 (W8 正控照常写出)。旧版 (HEAD) 同参数: 建出工作目录并写 base.sh / impl.sh 后在 W12 以 1 退出。
3. W12-replay-138.tsv 首行加页眉 (# 开头), 第 1 节四个 awk 跳过 # 行 (最后一个的总数改用非 # 行数)。核对: 95cf1de7 那份 tsv, 旧 awk 吃无页眉版 vs 新 awk 吃加页眉版, 输出逐字相同; 本轮 W12 跑完后对 .rows 与 .tsv 再核一次。
4. 1b: 基线回放 (replay138.sh 喂 base.sh, 无探针, T_trigger 记 -) -> W12-replay-138-base.tsv (有页眉), 按编号对齐; 字节核对: replay138.sh 不记 stderr 的 sha256 且本段不许改它, 所以 rc + sha256(stderr) 取自 ident.sh 在同 138 条上另跑的一遍 (base vs 未插桩实现) -> W12-ident-138.txt (有页眉)。这是取法上的选择, 报告列为拿不准项。

## B. 各阶段
- W9: base 与 impl 之间变化恰好 21ab、21ac、21ag、21aj、21al、21ao 六组; 各组检查清单与主控低负载的 suite-proto.out、suite-impl2.out 逐条相同; 与 95cf1de7 的 W9-suite.txt 只差 SC-21ab 那 3 处, 其余逐条相同。首尾负载 < 2。
- W13 (MUT_SCOPE=full): 第 1 节 5 个 bash FAIL 0 (3.2.57 有 SKIP [platform]); 第 2 节基线红集在与 95cf1de7 (PASS 19 FAIL 73) 共有的编号上逐个相同, 新编号 (R2 补强、TASK-003 的 V14-*) 单列; 第 3 节全部 BI CAUGHT, P-0 以外的 P-* CAUGHT, P-0 可能 NOT-JUDGED (全量连跑尾部负载)。风险: 末读数可能因全量连跑自身负载 >= 2 -> 按 INV-7 作废重跑, 至多 3 次。
- P-0 单跑: v31 模式与套件模式都 GREEN (套件模式只容 SKIP [platform])。
- 套件坏实现 (W13-suite-mutants.txt): 全部 BI CAUGHT (BI-8 原因为 [reference], 同 3d), P-0 GREEN, 其余 P-* CAUGHT, 退出 0。
- W12: 第 1 节 OVER 0 of 138; W1 class size (SMAX) 放行 >= 135 (95cf1de7 为 136), 若 135, 少的那条是 relax-start + rc 2 + 与基线同类尺寸文案; class value (VMAX) 1 条拦; 第 2、3 节 identical=300 / 40, different=0。1b: 回落 0-3 条; 放行的多等 p50 约 0.4-0.8 s, max < 3.3 s; 未进重跑的 (至少 VMAX 那条) rc + sha256(stderr) 全与基线相同。
- wt217/aria 在套件模式前后 git status 不变, HEAD 2893bcc。

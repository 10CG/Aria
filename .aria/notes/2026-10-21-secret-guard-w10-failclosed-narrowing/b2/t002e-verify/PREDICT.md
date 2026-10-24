# 3c 主控复核: 预期 (开跑前写下, 2026-10-24 14:4xZ)

对象: worktree 未提交改动 (套件 d085afae6834 / helper 213d01379695 / 垫片 5c5c04525a67), hook af4658b6f935 不变; 主仓 v31/run-suite.sh 首行加 helper 前缀。

静态 (已做, 结果见 VERIFY.md):
- S1 hook sha 前缀仍为 af4658b6f935。
- S2 6 组的基线支 (else 段) 与 HEAD (fee1a65) 逐行相同; 放宽支行数不变, 只是 10 条触发点命令改走 wpa_x6, 每条的第 2 个参数 = 该命令在 else 段里 wpa_x_toolarge 的 limit 行, 第 1 个参数 = HEAD 放宽支对它的原断言种类。
- S3 wpa_x6_eval 只替换 wpa_err / wpa_rc, 原断言 helper 不再自己跑 hook (每条触发点命令只跑一次 hook)。
- S4 参照表 (sg_w10_ref + fbref) 与 3c 在 59e333c / 实现上各 5 个 bash 的原始日志逐条相符 (按日志的 gate-closed 字段与 fbt 的 (status rc kind) 字段独立解析)。
- S5 垫片非注释行与 HEAD 逐字节相同。

实跑 (PATH 上的 bash 5.2.15, taskset 0,1 + nice 19, 开跑前一分钟负载 < 1.2):
- R1 run-suite.sh, worktree 套件, 实现 hook, SG_W10_ONLY=. : PASS 136 / FAIL 0 / SKIP 0; 输出里没有 [reference]; 计时批 judged (若收尾负载过门槛则可能出现 SKIP, 但 FAIL 仍为 0)。
- R2 BI-8 由我自己构造 (实现副本里 `_SGV_VMAX=4096` 改 8192, 预期 sha 前缀与 mutants.py 的 ff9f7a43eb7e 相同), SG_W10_ONLY=^(V9-E12-vmax-unchanged)$ : V9-E12 FAIL, 细节含 "gate-closed arm rc=0 none, reference (59e333c) rc=2 vmax [reference]"; 退出码 1。
- R3 我自己构造的参照表负控 (套件与 helper 的副本, 实现 hook):
  (a) 参照表里 V7-E1 改成 '2 vmax' -> V7-E1 FAIL, 细节 "gate-closed arm rc=2 oversize, reference (59e333c) rc=2 vmax [reference]";
  (b) V1-E16-p1-small-benign 改成未登记 -> FAIL, 细节 "reference (59e333c) rc=unrecorded - [reference]";
  (c) helper 的 fbref 里 V6-S20 改成 '2 vmax' -> V6-S20 FAIL, 细节 "status 2 oversize, reference (59e333c, the same copy and mode) 2 vmax [reference]";
  对照 V6-S21 PASS。合计 PASS 1 / FAIL 3, 退出码 1。
- R4 worktree 整轮 (git 检出, PATH bash): FAIL 0, PASS 961 (计时批若未判则 SKIP 计入, FAIL 仍 0), SC-13 绿; 6 组那行 "deadline fallback (截止回落) N / 10", 预期 N = 0 (3c 整轮为 0; 3a/3b 的 9 次整轮里放宽断言每次都成立), N 为 1-2 也不算错。

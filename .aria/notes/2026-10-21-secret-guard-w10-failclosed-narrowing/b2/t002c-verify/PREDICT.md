# T002c-3a 主控复核: 开跑前写下的预期 (2026-10-24, 先写后测)

对象: wt217/aria 的未提交改动 (套件 53f1eaefaf72 / helper 265a7b8d9b63 / 垫片 637c52c10bbf), hook af4658b6f935 (21a37ea); 主仓 v31/run-suite.sh 711a0201e23b。
每轮开跑前等一分钟负载 < 1.2; 全部 taskset -c 0,1 nice -n 19, 串行。

R1 W10-only 轮 (SG_W10_ONLY=., worktree):
  - 5.0.18 / 5.1.16 / 5.2.15 / 5.3.20: PASS 136 / FAIL 0 / SKIP 0, relaxation expected: yes, timing batch: judged, 退出码 0
  - 3.2.57: PASS 78 / FAIL 0 / SKIP 58 (platform 58), relaxation expected: no, 退出码 0
  依据: 3a 报告第 3 节与移植口径 (iii)。批末负载 >= 2 时 29 条记 SKIP [void], 属负载问题不算不符
R2 等价: v31/sc-cases.sh (PATH bash) 对实现 PASS 137、计时批 judged; 与 R1 的 5.2 日志按编号对齐, 136 个共有编号状态相同, 只差 V12-C1 (only-v31)
R3 整轮 (PATH bash, 现位置 = SC-13 之前): 总数 961, FAIL 恰 6 (SC-21ab/ac/ag/aj/al/ao), SC-13 绿, 退出码 1;
   W10 批开始时负载 >= 2, 计时批 SKIP [load]: 29 条 SKIP [load] + 107 PASS (3a 的诊断: 前面约 5 分钟旧用例把负载推过 2)
R4 坏实现抽查 (v31/run-suite.sh, SG_W10_ONLY = 该坏实现的指定用例; mutants.py 由主控重新构造):
  - BI-24 / BI-7 / BI-11: 指定用例全 FAIL, 原因标签与 reasons.tsv 相符 (同 3a)
  - BI-5 (准入门不问扩展清单): V2-G4-extension-file-with-entry FAIL [status], V2-E9-extension-project FAIL [bytes], 抓住。
    依据: 只改了放宽一侧的判定, 关门臂 (WSL_DISTRO_NAME) 不受影响
  - BI-45 (分段触发点用整条命令的原因串): V6-S20-segment-fallback-text FAIL [bytes], 抓住。依据: 只改了放宽分支里的原因串
  - BI-8 (_SGV_VMAX 4096 -> 8192): V9-E12-vmax-unchanged PASS, 即指定用例上漏抓。
    依据: VMAX 是两臂共用的常量, 关门臂跑的也是这份坏实现, 两臂同样放过 4097 字符的值, 逐字节相同;
    v31 的对照臂是真基线 59e333c 才抓得住。旧用例 SC-21ad / SC-21am (4097 被拒) 在整轮里会红, 但它们不是指定用例
  - 实现对照: 同一批指定用例全 PASS
R5 编号: R1 的 5.2 日志里 136 个编号 = R2 输出的 137 个编号去掉 V12-C1

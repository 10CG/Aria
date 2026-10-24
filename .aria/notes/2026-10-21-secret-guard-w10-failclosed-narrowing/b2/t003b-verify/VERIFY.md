# TASK-003 第二段主控复核: 结果 (2026-10-24 21:29-21:34Z)

预期在 PREDICT.md (实跑前写下)。对象: 主仓新建的 v31/impl/w14-matrix.sh、w14-shapes.py (2f5cf9bdad16)、W14-timing-matrix.txt; 实现 af4658b6f935 未动。主控自己的量法 measure.py (不经 w14-matrix.sh; 一次调用一行: JSON 从文件进 stdin, HOME 与 cwd 新目录, LC_ALL=C.UTF-8, 去掉预算变量; W 用 time.time() 从起跑到退出; T_trigger 取第一个 relax-start 探针减同一起跑时刻; 上界 max(T_trigger 或 W, 3) + 0.3)。越界构造 cover.sh (974610ac2dcb): 作业停掉计时器后再等 4 s 以状态 1 结束。驱动 drive.sh, 时间线 drive.log。

## 静态

- 埋点副本 = 实现 + 3 行探针 (diff +3 -0), sha c329a5b830af, 与矩阵首行相同; gen-v3.py a271badaaae5、w14-shapes.py 2f5cf9bdad16 与首行相同; 末行「236 of 236 (over the bound: 0)」。
- w14-matrix.sh 的上界与 v31/run-evidence.sh:47 同一公式 (没进重跑的 t 取 W 本身)。
- 矩阵里 shrink 放行 (rc 0): 已核为规格「放宽了什么」R-b 申报的裁定 A 后果 (R2 TL2-F4 构造, W11 shrink: 读凭据形路径另有无关的 >/dev/null, 基线按尺寸拦、现在放行), 不是新缺陷。

## 实跑 (PATH 上的 bash 5.2.15; 开跑前一分钟负载 < 1.2, 全程 0.89-1.42)

| 轮 | 预期 | 结果 |
|---|---|---|
| V-own segfinding × 3 | rc 2 finding, W 约 1.1-1.25 s, T 约 0.65-0.78 s, 不越界 | rc 2 finding, W 1.168 / 1.267 / 1.167, T 0.710 / 0.706 / 0.687, 不越界 (W 有一次略高于我写的上沿) |
| V-own many-segs × 3 | rc 0 allow, W 约 2.65-2.9, T 约 1.85-2.0, 不越界 | rc 0 allow, W 2.837 / 2.922 / 2.774, T 1.937 / 2.105 / 1.961, 不越界 (第 2 次的 W、T 略高于我写的上沿) |
| V-own apply-heavy-cjk × 3 | rc 2 size, W 约 3.02-3.08, T 约 1.95-2.15, 不越界 | rc 2 size, W 3.074 / 3.075 / 3.072, T 1.889 / 2.073 / 2.330, 不越界 (两次 T 出我写的范围) |
| V-own km-ext-small × 3 (不设扩展目录) | 不进重跑, W < 0.3 s, 不越界 | rc 0, T -, W 0.114-0.115 s, 不越界 |
| V-over 越界构造, 经 w14-matrix.sh calib | segfinding、many-segs over=1, W 约 T + 4 s; km-ext-small over=0 | 相符: segfinding W 4.698 (T 0.688, job 4.004) over=1; many-segs W 5.988 (T 1.977) over=1; km-ext-small W 0.076 over=0 |
| V-over-own 同一构造, 主控量法 segfinding × 2 | over=YES | 相符: W 4.737 / 4.725, over=YES |

结论: 矩阵的判法能红 (越界构造两种量法都报越界); 主控独立量的三个代表形状与矩阵的读数同一量级、都不越界。数值范围的预期有 4 个读数略出 (测量噪声, 不影响结论), 照实记下。

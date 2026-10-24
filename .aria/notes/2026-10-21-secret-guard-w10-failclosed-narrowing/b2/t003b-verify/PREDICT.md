# TASK-003 第二段主控复核: 预期 (2026-10-24, 实跑前写下)

静态 (已做): 埋点副本 = 实现 + 3 行 (diff +3 -0), sha c329a5b830af, 与矩阵首行相同; gen-v3.py a271badaaae5、w14-shapes.py 2f5cf9bdad16 与首行相同; 矩阵末行 236 of 236 (over 0)。shrink 放行 (rc 0) 已核为规格 R-b 申报过的裁定 A 后果 (TL2-F4, W11 shrink), 不是新缺陷。

实跑 (PATH 上的 bash 5.2.15; 开跑前一分钟负载 < 1.2; INV-7: 批首尾读数 < 2):
- V-own 主控自己的量法 (measure.py, 不用 w14-matrix.sh), 真实现的埋点副本, 每形状 3 次:
  - segfinding: rc 2 finding, W 约 1.1-1.25 s, T_trigger 约 0.65-0.78 s, 不越界;
  - many-segs: rc 0 allow, W 约 2.65-2.9 s, T_trigger 约 1.85-2.0 s, 不越界;
  - apply-heavy-cjk: rc 2 size, W 约 3.02-3.08 s, T_trigger 约 1.95-2.15 s, 不越界;
  - km-ext-small (不设扩展目录): 不进重跑 (T_trigger -), W < 0.3 s, 不越界。
- V-over 越界构造 (作业停掉计时器后再拖 4 s 才回落; cover.sh 974610ac2dcb), 经执笔席的 w14-matrix.sh calib: segfinding、many-segs 都 over=1, W 约 T_trigger + 4 s (约 4.7 s、约 5.9 s); km-ext-small over=0 (不进重跑)。
- V-over-own 同一构造用主控的 measure.py 量 segfinding 2 次: over=YES。

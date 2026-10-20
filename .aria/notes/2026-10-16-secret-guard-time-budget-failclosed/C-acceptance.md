# secret-guard-time-budget-failclosed — C 验收记录 (v1.75.1 候选)

> 主控独立复核 (不信执笔回执)。2026-10-16 实现 / 10-20 定稿。基线 aria v1.75.0 (`08db1c0`); C 落 aria feature `feature/secret-guard-time-budget-failclosed` (`9a6ce0e` C + `fb73e88` cap)。owner 2026-10-16「先发 C, B 另做」→ 本 change 只发 C；B + built-in 首遍缺口 → #228。

## 实现 (C = 时间预算 fail-closed)
- `SECRET_GUARD_TIME_BUDGET_S`（默认 3，**上界 4** < CC 5s）：`SECONDS` 检查点（3.2 兼容，非 EPOCHREALTIME）在 W10 第二遍 per-segment / i×j 链式 / W9 扩展腿；逾预算 → fail-closed BLOCK + 拆小文案（复用 M6 oversize 路径的新 timeout 分支）；新 status 3 + TIME 哨兵。时钟 `_SG_T0` 在每命令入口（`_sg_per_segment_eval`）与 `_sg_vx_collect` 重置；预算每命令解析一次。
- 不变量：内建直接判定（#154 核心，~0.47s）先于计时且永不被门控；`# guard:ack` 不变；从不 fail-open；`_SGV_*` 尺寸预算（M6）语义不变。

## 主控复核发现并处置 (执笔席 + 主控)
1. `_SG_MODE==none` 路径跳过 `_sg_vx_collect` 却仍跑 W9 ext 检查点 → 陈旧 `_SG_T0`（sourced 套件假性 fail-closed）→ **修**：`_sg_per_segment_eval` 入口也重置（SC-T4 守卫）。
2. 逐检查点重解析 env（SC-8 tier(e) +155%，仍 <100ms）→ **修**：每命令缓存一次。
3. `SECRET_GUARD_TIME_BUDGET_S` 无上界 → 高值可禁用 fail-closed（退回 CC 5s fail-open）→ **修**：封顶 ≤4（SC-T5）。
4. **built-in 首遍对巨大无变量 raw 命令的 O(copy²) 慢路径无检查点**（先于 WP-A 的旧慢路径，非 #216 W10/W9）→ **不扩 C 范围**，如实披露为已知限制，归 **#228**。
   - 注: 对抗复核由主控执笔席进行（非另立 qa 席）；若需额外保险可加一轮新鲜眼睛。

## 验收 (全绿)
- 套件 `secret-guard.test.sh`（真 git checkout，含 SC-9a + SC-8 五档 = SC-30）：**PASS 825/825, FAIL 0**。SC-8 五档全 <100ms 天花板。
- SC-T 新用例：SC-T1/T1b/T2a **baseline-failing**（基线 v1.75.0 对同输入 exit0 / 本版 exit2）+ SC-T2b/T3a/T3b/T3c 核心不受影响/逃生口 + SC-T4 时钟新鲜度结构守卫 + SC-T5 预算封顶。
- red-proof（直调基线 vs 本版）：SC-T1 基线 exit0 / 本版 exit2；SC-T3a 两侧 exit2（内建块，不受预算影响）；SC-T4 基线 `_sg_per_segment_eval` 无重置；cap 99→4 / 2→2 / 默认→3。
- **W14 时档 `timing.py --judge`（本版 vs 268da8f）：20 有界档 0 failed**。比值≈v1.75.0（g-c 1.02 / fh 1.90·2.01 / i3-f·g·h 3.41·3.25·3.51 / i 1.25·1.18）→ C 检查点开销可忽略。
- bash **3.2.57 + 5.2** `bash -n` 过；C/POSIX locale 未变（新代码仅 SECONDS/算术/case）。

## 结论
C 全部验收腿 PASS，就绪发 v1.75.1（PATCH）。发版 = 取号 + 合并 master + tag + origin/github 双推（owner 门）；#216 于该版收口（关单披露含 Windows 实测 + built-in 已知边界 #228）。

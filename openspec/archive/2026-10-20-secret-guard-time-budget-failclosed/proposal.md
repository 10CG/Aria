# secret-guard 时间预算 fail-closed + W10/W9 成本收敛（收口 #216）

> **Level**: 2（proposal only）
> **Status**: **Approved（方向）** — owner 2026-10-16「先按你推荐的来」：机制 **c1（纯 bash `SECONDS`）+ N=3s + 版本 PATCH + C 作兜底 / B 降误拦**。进 B.1 实现（实现仍走执笔席 + 主控独立复核）。
> **Linked Issue**: `10CG/aria-plugin#216`（hook 5s 超时后 fail-open）；放大场景 `10CG/aria-plugin#219`（Windows/MINGW64）；关联 `10CG/aria-plugin#203`（变量间接 partial）、`10CG/aria-plugin#154`（报告环境即 MINGW64）
> **动机证据**: owner Windows 主力机实测（2026-10-15，记于 #219 comment 28759）：g-c tier 重命令（6.4 KB；16 赋值×400B + 128 引用）直跑 `secret-guard.sh` = **real 5.037s / user 4.668s（纯 CPU，非负载）**，恰越 5s。典型直接读取命令仅 0.47s（#154 核心不受影响）。

## Why

v1.75.0 的 L1 `secret-guard` 对重命令成本高：W10 第二遍判定走 `_sg_compute_credit`，对单条长副本是 **O(copy²)**（头注释 `secret-guard.sh:586-587` 实测：约 0.9s@8KB / 3s@16KB / 13s@32KB），`_sg_vx_collect` 的链式展开是 **O(vars²)**；W9 扩展「整串一眼」在 Linux 3.45s。现有 fail-closed 只按**尺寸**（`_SGV_VMAX/SMAX/TMAX` 字符预算，M6 owner 2026-10-14 裁定）。

但**尺寸 ≠ 时间**：慢平台（Windows MINGW64 实测比 Linux 慢约 2.6×）上，尺寸合规（6.4KB ≪ `_SGV_TMAX` 65536）的命令仍越 5s hook 超时 → Claude Code 在 5s kill hook → **fail-open（命令放行、判定未跑完）**。`secret-guard.sh:582` 头注释已明记「5s 超时与其 fail-open（#216）未触及」——**本 change 触及它**。W9 扩展在 Windows 外推 ~9s，更早越线。

核心问题：**fail-open 恰在最需要守卫的平台让守卫静默失效**（#154 报告环境就是 Windows MINGW64），违反 fail-closed 不变量（memory `failopen-posture-owner`）。

## What Changes

### C — 时间预算 fail-closed（安全网，主）

hook 自设一个**时间上界 N（< CC 的 5s）**；一旦自身昂贵扫描逼近 N，**停下并 BLOCK（fail-closed）**，复用 M6 的「命令过大/过于复杂，无法在时限内扫描，请拆成更小的命令」文案，而**不是**放任 CC 的 5s 超时把它 fail-open。覆盖所有慢腿：W10 第二遍、W9 扩展整串、W1 大文件全扫。

- **机制候选（spec 定稿时择一/组合）**：
  - **(c1) 纯 bash 时间检查点**（推荐）：在各昂贵循环/腿的边界读 `SECONDS`（bash 内建，**3.2 兼容**，1s 粒度），累计耗时 ≥ N 即中止当前腿、走 fail-closed BLOCK。无外部依赖。粒度粗（1s）→ N 取整秒并留足余量。
  - **(c2) `timeout Ns <腿>` 外部包裹**：子秒精度，但需先核 `timeout`(coreutils) 在 MINGW64 / macOS 可用并给兜底（不可用时退回 c1 或 fail-closed）。
- **自上界 N**：建议 **4s**（CC 5s 之下留 ~1s 给 hook 收尾 + 机制自身延迟 + 1s 粒度误差）；需在 spec 用慢平台实测余量论证。
- **可配置**：`SECRET_GUARD_TIME_BUDGET_S`（默认 4；设更低用于**确定性测试**与运维调参）。
- **fail-closed 性质**：同 M6 —— **从不 fail-open**；逃生口 `# guard:ack: <理由>` 仍放行；内建直接判定（#154 核心，~0.47s）在时间预算之内、不受影响。

### B — W10/W9 成本收敛（优化，次）

降两处主导成本，使 C 的时间预算**罕被触发**（合法重命令不至于被误拦）：

- **(b1)** `_sg_vx_collect` 的 i×j 链式展开 O(vars²) → 收敛（如只展开实际被引用的变量 / 上界更紧）。
- **(b2)** `_sg_compute_credit` 的 O(copy²) 判定 → 次平方（或封顶每命令判定的段数/总量 + 短路）。
- 目标：g-c 一类在慢平台（~2.6×）也 < 自上界 N。

## Out of scope

- **不改** CC 的 5s 超时本身（框架侧、不可控）；只在 hook 内**抢在它之前** fail-closed。
- **不改** L3 `secret-scan`（PostToolUse，设计上 fail-open：工具已执行，拦无意义）。
- **不改** 既有尺寸预算 `_SGV_*` 的语义（M6 保留）；时间维是**叠加**，不替换。
- **不改** 既有 BLOCKED 文案归一化（除新增/复用「时限内无法扫描」一句）。
- **built-in 首遍对巨大无变量 raw 命令的 O(copy²) 慢路径**：C 的时间检查点只在 W10 第二遍 + W9 扩展；built-in 首遍（`_sg_compute_credit` 对命令本身）无检查点，故一条巨大 raw 命令仍可能越 CC 5s → fail-open。这是**先于 WP-A 的旧慢路径**（非 #216 的 W10/W9 新能力），C 不覆盖、如实披露为已知限制，归 follow-up **#228**。

## Success Criteria（可证伪；baseline-failing 优先）

- **SC-T1（fail-closed 不 fail-open）**：设 `SECRET_GUARD_TIME_BUDGET_S` 为一个低值（如 1），喂一条会超过它的重命令 → **exit 2 + 时限 fail-closed 文案**；基线 v1.75.0（无时间预算）对同输入**不**因时间而 BLOCK（判定跑完或被 CC 超时截断=fail-open 代理）→ 红。
- **SC-T2（文案 + 逃生口）**：时间预算触发时文案含「拆小」且 rc=2；同命令加 `# guard:ack: <理由>` → 放行（exit 0/继续）。
- **SC-T3（核心不受影响）**：典型直接读取凭据命令仍 exit 2（内建先判，远在预算内），时间预算**不**改变它。
- **SC-B1（成本降）**：g-c tier 的整进程 CPU 时间较 v1.75.0 降 ≥ 阈值（交错 min/5 比值；阈值在 B.1 定）。
- **SC-R（零回归）**：既有 `secret-guard.test.sh` 822/816 + SC-30（含 SC-8 五档）+ W14 时档全绿；`_SGV_*` 尺寸 fail-closed（M6）行为不变。
- **SC-32（兼容）**：新代码 bash-3.2 兼容（无 bash4+ 构造，`SECONDS` 而非 `EPOCHREALTIME`）；C/POSIX 与第二 locale 下一致；若有 MINGW64 环境则附一次实测（典型拦截 + 重命令 fail-closed）。

## Impact

- **版本**：建议 **PATCH**（修复 fail-open → fail-closed + 性能，向下兼容；先例 v1.66.x 的 fail-open 修复类）；号归 owner。收口 #216。
- **同步面**：aria `hooks/secret-guard.sh` + `hooks/tests/secret-guard.test.sh`（计数再同步）+ 头注释（`:582` 改为「#216 已由 <本 change> 收口」）+ `CHANGELOG`；standards `secret-hygiene.md` §5.7 追一句时间预算（additive）。
- **误拦面**：C 会拦**合法的重命令**（走拆小 / `# guard:ack`）——这是 #217 误拦面向**安全侧**的扩张，须在 CHANGELOG「行为变更双向申报」披露；B 的目的正是把这个误拦降到罕见。

## Tasks（A.2 骨架；细粒度待 owner 批准本 proposal 后展开）

1. **B.1 入场**：核 `timeout` 跨平台可用性 + 定机制（c1/c2）；在 Linux（+ 若可 Windows/MINGW64）记基线重命令时间，定 N 与 SC-B1 阈值。
2. **C 实现**：时间预算 fail-closed（检查点或包裹）+ `SECRET_GUARD_TIME_BUDGET_S` + SC-T1/T2/T3。
3. **B 实现**：b1 + b2 成本收敛 + SC-B1。
4. **回归**：SC-R（套件 + SC-30 + 时档）+ SC-32 + 非作者对抗复核。
5. **发版 + #216 收口**（owner 门）。

## owner 裁定（2026-10-16，「先按推荐来」）

1. **机制 = c1**（纯 bash `SECONDS` 检查点；3.2 兼容、零外部依赖、跨平台最稳）。若实现后实测误拦偏多再评估 c2（子秒）放宽 N。
2. **自上界 N = 3s**（1s 粒度下留 ~2s 余量给 hook 收尾 + CC 5s 之差；B.1 用慢平台实测复核余量）。
3. **版本 = PATCH**（fail-open 修复，向下兼容）。
4. **分工 = C 作兜底（永不 fail-open）+ B 把误拦降到罕见**（owner 选的 B+C）。
   —— 以上为「先按推荐」的起点裁定，实现中若实测推翻可带数据复议。
5. **（2026-10-16）发布划分**：本 change **只发 C**（v1.75.1 PATCH，安全兜底、低风险、已验证）。**B（成本收敛）** 与复核发现的 **built-in 首遍 raw 命令超时缺口** → 另立 follow-up **10CG/aria-plugin#228**（同属 compute 成本域）；C 发布时如实披露该 built-in 边界为已知限制。

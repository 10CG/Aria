# secret-guard 扫描成本收敛 (B) + built-in 首遍密钥形超限 cap (收口 #228)

> **Level**: 2（proposal + detailed-tasks.yaml）
> **Status**: **Approved（方向）** — owner 2026-10-20「按你的设计来，并记录判断理由，后续衍生问题可优化迭代」。设计 = Part 2 在 `_sg_compute_credit` 入口（密钥形命中**之后**）加尺寸上界（fail-closed，阈值 B 之后实测定）+ B 成本收敛，二者互补、合为**一个** change。进 B.1（实现走执笔席 + 主控独立复核）。
> **Linked Issue**: `10CG/aria-plugin#228`（resolve）；上游 C = `secret-guard-time-budget-failclosed`（v1.76.1，已归档）；关联 `#216`（超时 fail-open，C 已收口 W10/W9 侧）、`#219`（Windows/MINGW64 放大）、`#203`（变量间接 partial）、`#154`（本 cap 保护的核心）。
> **动机证据**: C 的主控对抗复核（2026-10-20，记于 `.aria/notes/2026-10-16-secret-guard-time-budget-failclosed/C-acceptance.md` 第 4 项）发现 built-in 首遍无时间检查点；读码确认 O(len²) 源在正则引擎内部（`_sg_compute_credit` 对单条长行：约 0.9s@8KB / 3s@16KB / 13s@32KB，头注释 `secret-guard.sh:586`）。基线 aria v1.76.1（master `59e333c`）。

## Why

两部分根因**同一个**：`_sg_compute_credit` 里约 20 条 `_sg_line_match` 正则在单条长行上触发回溯 → 对单段是 **O(len²)**；`_sg_vx_collect` 的链式展开另是 **O(vars²)**。

1. **Part 2（安全洞）**：C 的时间检查点只在 **W10 第二遍 + W9 扩展**；built-in 首遍（`_sg_core_eval` → `_sg_judge_one` → `_sg_compute_credit`）**一个检查点都没有**。一条巨大**单段** raw 命令（无顶层 `; && ||`）若命中密钥读取形，其 O(len²) 扫描在慢平台（Windows ≈2.6× Linux，#219）>5s → Claude Code 在 5s kill hook → **fail-open（命令放行、未扫完）**。分号/`&&` 分段救不了（短的恶意段会先 BLOCK），但**单段**（如一条 32KB 的 `python3 -c '…读 ~/.aws/credentials…'`）绕过——绕过的正是 #154 / WP-A 存在的理由；无人复议的 v2.0 Layer 2 里最危险（Rule #10）。
2. **B（误拦）**：C 把慢扫描变 fail-closed BLOCK，代价是误拦合法重命令（#217）。降成本 → C 的时间预算**罕被触发** + Part 2 的 cap 阈值可设更高（更少误拦）。

## What Changes

### Part 2 — built-in 首遍密钥形超限 cap（安全，主）

在 `_sg_judge_one` 的 **compute_credit 入口**（某条 risky / 密钥读取形**已命中之后**）加尺寸上界：命中 + 段长 > cap → fail-closed BLOCK（复用 M6 oversize「命令太大无法扫描、请拆小」文案）+ return 2，**先于** O(len²) 的 `_sg_compute_credit`。

- **为何放 compute_credit 入口而非段入口**：读码确认 `_sg_compute_credit` 只在某条 risky 正则命中后才跑（`_sg_judge_one` 的 `if [[ $subj =~ $pat ]]` 之内）。放这里 → 巨大**良性**命令（不含密钥形 token）永不进 compute_credit、永不被 cap 拦；只有「既像密钥读取、又大到无法在时限内核验」的命令 BLOCK。**误拦面从「所有大命令」缩到「大的像密钥读取的命令」。**
- **为何是尺寸 cap 而非时间检查点**：单段的 O(len²) 在正则引擎内部、**没有 mid-scan 边界**；时间检查点扫描前测=0（还没开始）、扫描后测=已越 5s（太晚）→ 对单段无效。扫描前的尺寸 cap 是唯一有效机制，且与 M6 `_SGV_SMAX` 同族。
- **阈值**：B 之后按实测定——取「最慢可及平台（Windows 2.6×）仍 <~4s（CC 5s 下留 ~1s）」的最大段长。基线 8KB（=SMAX，Linux 0.9s → Windows ~2.3s 安全）；B 降常数后可上移以减误拦。
- **多段补点（次）**：built-in 首遍 `_sg_core_eval` 的 per-segment 循环补时间检查点（C 只在第二遍 `_sg_vx_pass` 设了点），关多段慢命令的同类洞。
- **防御纵深**：审 `risky_patterns` 本身在长输入上不回溯（否则恶意大命令在 for-pat 检测循环就超时、走不到 cap 检查）；有回溯的 → 在 B 里 bound/改写成线性。

### B — 扫描成本收敛（优化，次）

- **(b1)** `_sg_vx_collect` 的 i×j 链式 O(vars²) → 收敛（只展开实际被引用的变量 / 更紧上界）。
- **(b2)** `_sg_compute_credit` 的 O(len²) → 降常数 / 次平方（单行只切一次行并复用、审回溯正则、必要处短路）。
- 目标：g-c tier（16 赋值×400B + 128 引用）Linux 整进程 CPU 从 ~1.8s 降到 ≲1.1s → Windows g-c <3s（不触发 C 的 fail-closed）。

## Out of scope

- **不改** CC 的 5s 超时本身（框架侧、不可控）。
- **不改** C 的时间预算语义（W10 第二遍 + W9 扩展的检查点保留）；Part 2 是**叠加**首遍维。
- **不改** L3 `secret-scan`（PostToolUse，设计上 fail-open）。
- **不改** 既有尺寸预算 `_SGV_*` 语义；Part 2 cap 是首遍侧的新尺寸门，与 `_SGV_SMAX`（第二遍副本侧）正交。
- **不号称挡住能写文件的对手**：guard 从设计只看命令文本，「写文件再 `bash file`」本就扫不到（既有边界，非本次引入）；Part 2 关的是「超时 fail-open 把命令行扫描架空」这一条，在 guard 真实威胁模型（命令行里的凭据读取）之内。

## Success Criteria（可证伪；baseline-failing 优先）

- **SC-P1（Part 2 短路，baseline-failing）**：巨大单段、命中密钥读取形、> cap 的命令 → 新版在 `_sg_compute_credit` **之前**短路为 oversize BLOCK（oversize 文案 + 耗时远小于 O(len²) 全扫）；基线 v1.76.1 同输入走完 O(len²) 全扫后才 BLOCK（**普通 risky 文案** + 全扫耗时）。**红判据 = 文案变体（oversize vs 普通）与耗时二者**——两版 exit 同为 2，故 **exit code 不作判据**（避免「基线也 exit 2」的恒绿陷阱）。真实 CC 链里「全扫 >5s → fail-open」由耗时代理，harness 无 CC 超时、不直接测。
- **SC-P2（良性大命令不误拦，防位置回归）**：巨大单段、**无密钥形** token、同样 > cap 的命令 → **不**被 cap 拦（继续/exit 0）；证明 cap 在 compute_credit 入口而非段入口。基线对同输入也放行 → 本项**非 baseline-failing**，是防「把 cap 放错位置（段入口）」的回归闸：坏实现（cap 放段入口）会把它拦 → 红。
- **SC-P3（首遍多段补点，baseline-failing）**：一条**无变量、良性但慢**的多段命令（基线 verdict = ALLOW）+ 低预算 → 新版在 built-in 首遍 per-segment 时间检查点 fail-closed（exit 2）；基线首遍无检查点 → 跑完 → ALLOW（exit 0）。**红判据 = exit 0→2 翻转**。（须用**无变量**命令以命中首遍，而非 C 已设点的第二遍 `_sg_vx_pass`。）
- **SC-B1（成本降）**：g-c tier 整进程 CPU 较 v1.76.1 降 ≥ 阈值（交错 min/5 比值；阈值 B.1 定）；慢平台外推 < C 的时间预算 N。
- **SC-R（零检出回归）**：既有 `secret-guard.test.sh` 全绿 + SC-30 + W14 时档；**既有检出集合逐条不变**（B 是 correctness-critical 改写）；C 的 SC-T 系列仍全绿（时间预算不破）；`_SGV_*` 尺寸 fail-closed 不变。
- **SC-32（兼容）**：新代码 bash-3.2 兼容；C/POSIX + 第二 locale 一致；若有 MINGW64 附一次实测（良性大命令放行 + 密钥形大命令拦）。

## Impact

- **版本**：B = 优化 + Part 2 = fail-open→fail-closed 修复，向下兼容 → **PATCH**（号归 owner）。收口 #228。
- **同步面**：aria `hooks/secret-guard.sh` + `hooks/tests/secret-guard.test.sh`（计数再同步）+ 头注释（`:586` 的 O(copy²) 注更新 + `:582` 的 #216 措辞顺手厘清，C TASK-006 遗留）+ `CHANGELOG`；standards `secret-hygiene.md`（首遍 cap additive 一句）。
- **误拦面**：Part 2 cap 新拦「巨大 + 像密钥读取」的命令（走拆小 / `# guard:ack`）——#217 误拦面向安全侧的小扩张，须在 CHANGELOG「行为变更双向申报」披露；compute_credit 入口 gating 把它压到罕见。

## Decision record — 现在判断的理由（owner 2026-10-20「按你的设计来」）

记这三条硬事实 + 推理，供后续衍生问题迭代时回看（owner 明示「可优化迭代」）：

1. **洞是真 bypass，不是理论**：单个不可分段的巨大命令（如 32KB `python3 -c`）把凭据读取藏进去 → 慢平台 O(len²) >5s → CC fail-open → 照跑照读。分段救不了（短恶意段先 BLOCK），单段绕过，绕的正是 #154；v2.0 无人复议最危险。
2. **「高阈值 64KB」是假选项**：最慢平台 <5s 要求 Linux <5/2.6≈1.9s → 对应 ~12KB（曲线 0.9s@8KB / 3s@16KB）。[12KB, 64KB] 这段在 64KB 上界下不拦、却仍超时 fail-open。**只有 ≤~12KB 的 cap 真关洞**；中间档不存在，真正选择是二元（~8KB cap vs 留口）。
3. **compute_credit 入口 gating 是把误拦成本从「所有大命令」缩到「大的像密钥读取的命令」的关键**：读码确认 O(len²) 只在 risky 正则命中后才跑；cap 放那里 → 良性大命令永不被拦。这让 fail-closed 的代价小到可接受。
- **叠加 B**：降 O(len²) 常数 → 超时的尺寸门槛上移 → cap 可设更高 → 更少误拦。故 B + Part 2 互补、合一个 change；阈值 B 之后实测定，非拍脑袋。
- **诚实边界**：guard 只看命令文本；「写文件再 `bash file`」本就扫不到（既有边界）。Part 2 关「超时 fail-open 架空命令行扫描」这一条，不号称挡能写文件的对手。
- **姿态归属**：在 #154 核心路径（C 明写「永不被计时门控、永远快」）上新设 fail-closed = owner 权（memory `failopen-posture-owner` 2026-10-14 + Rule #10）；owner 2026-10-20 拍板关洞、delegating 理由给主控但决定仍其所拍。
- **可迭代**：若后续实测误拦偏多 / 出现相关衍生问题（cap 阈值在某平台不合适、risky_pattern 回溯超预期、多段补点的粒度），带数据复议优化。

## Tasks（A.2 骨架；细粒度见 `detailed-tasks.yaml`）

1. **B.1 入场 + 基线**：建分支、重锚行号、测 g-c 与首遍 O(len²) 基线曲线（Linux [+Windows 若 owner 跑]）、审 `risky_patterns` 回溯、定 cap 阈值公式 + SC-B1 阈值。
2. **B 实现**：b1 + b2 成本收敛 + SC-B1。
3. **Part 2 实现**：compute_credit 入口密钥形 cap + 首遍多段补点 + SC-P1/P2/P3。
4. **回归 + 非作者对抗复核**：SC-R（检出集合逐条不变）+ SC-32 + 坏实现对抗。
5. **验收**：主控独立复跑探针/套件/时档 + 良性大命令放行 + 密钥形大命令拦 实证。
6. **发版（PATCH）+ #228 收口**（owner 门）。

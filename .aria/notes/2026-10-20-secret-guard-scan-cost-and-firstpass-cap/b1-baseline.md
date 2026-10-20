# B.1 记录 — secret-guard-scan-cost-and-firstpass-cap（TASK-001）

> 2026-10-20，主控亲做。基线 aria v1.76.1（`59e333c`）；分支 aria `feature/secret-guard-scan-cost-and-firstpass-cap`；claim `claims/023236f2/s-9fd6@1625`（协调 ref `310361f → a7c698d`，ls-remote 核验，他人 4 条 active claim 完好）。
> **数字以 `evidence/` 与 `pilot-8-32.tsv` 为准**（脚本重生成，本文只引用；改文不改证据）。共享宿主纪律：全部 `taskset -c 0,1 nice -n 19`，一次一个重实验，文件头记负载。

## 工具与重生成

| 文件 | 作用 |
|------|------|
| `b1_shapes.py` | 填充形状唯一来源（A 长 token / B 多词 / C `\| cat` 管道 / D 引号内管道 / E jq 程序 / F 400B 随机串 / S 凭据读取独立首段 + 第二段填充）；凭据路径运行时拼装 |
| `b1_curve.py` | 整进程首遍曲线（CPU = RUSAGE_CHILDREN，交错、取 min，退出码作活性）；`--bash` 可换 3.2 |
| `b1_stage.sh` | 进程内分阶段计时：`_sg_safe_to_split` / `_sg_split_top` / 检测循环（bash ≥ 5） |
| `b1_detect.sh` | 检测循环单独计时（`time` 内建，bash 3.2 可跑） |
| `b1_gate_complete.sh` | 整串 vs 逐段检测在 11 种分隔符写法上的一致性 |
| `b1_fn_audit.sh` / `.py` | 函数级 + 逐正则拆分（R2 备用，本轮未跑） |
| `b1_run_all.sh` | 重生成 `evidence/E2–E7`（~3 min）；pilot 由 `b1_curve.py --lens 8,32 --reps 1` 单独生成（~6.5 min） |

冒烟测试抓到工具自身缺陷一处（相对 hook 路径 + `cwd=home` → 全部 rc 127，活性全 FAIL），已修（绝对路径）后活性全 ok —— 新写的检查先在基线自跑（memory `check-runs-at-baseline-first`）。`b1_curve.py` 重构为 import `b1_shapes` 后，A–E 形状长度与 pilot 20/20 一致。

## 发现

- **F1 根因**：首遍两个扫描器逐字符 `${_cmd:_i:1}`（`:215` `:294` @ `_sg_safe_to_split` `:204`；`:331` @ `_sg_split_top` `:321`）→ O(n²)；C locale 仍平方级、只快 ~2.5×（bash 每次取子串都重算串长，UTF-8 下还要多字节解码）。→ `evidence/E2-stage.tsv`
- **F2 作用面**：扫描器在切分前、任何时间预算前对每条命令运行；良性 ≈ 密钥形，与形状无关。→ `pilot-8-32.tsv`
- **F3 compute_credit 是次要项**：只在 A 形（单个长 token）多出 ~0.9s@8KB；头注释 `:587`「`_sg_compute_credit` on one long line: 0.9 s at 8 KB …」的数字对得上 A 形，但把它当成主成本是**错误归因**，#228 issue 与 v1 proposal 继承了它。→ pilot
- **F4 已发布版本可被绕过（Linux 生产默认）**：凭据读取 + 填充 14KB → C 形 6.21s、S 形（凭据读取单独首段）5.98s，均先超 CC 5s 才出 BLOCK → 在 CC 中 fail-open。→ `evidence/E3-bypass.tsv`
- **F5 bash 3.2.57**：良性 C 形 2 / 4 / 8KB = 2.1 / 8.4 / 34.2s → ~3KB 以上任何命令越 5s。注：本机 3.2 是 Linux 构建，Apple 构建可能有常数差，需 macOS 实测佐证（如有采用方环境）。→ `evidence/E4-bash32.tsv`
- **F6 检测循环线性**：bash 3.2 8 / 16 / 32KB = 0.19 / 0.29 / 0.53s；bash 5.2 = 0.04 / 0.07 / 0.14s；密钥形命中 #28 用 0.02–0.13s → 扫描前闸门可行。→ `evidence/E5-detect.tsv`
- **F7 g-c**：1.87s（低负载）；按 E2 曲线插值，7.2KB 时扫描器 ≈ 全部成本（第二遍被 M6 `_SGV_SMAX` 快速拒绝，rc 2）。#219 的 Windows 5.037s 同源；#228 原定 B（vx_collect / compute_credit）对 g-c 几乎无贡献。→ `evidence/E6-gc.txt`
- **F8 C 的时钟不覆盖首遍**（读码）：`_sg_per_segment_eval` 先 `_sg_core_eval`，后 `:1542` 才重置 `_SG_T0`；`_sg_vx_collect` `:633` 再重置 → 首遍耗时从不计入预算；「慢首遍 + 慢第二遍」可在预算触发前越 5s。R2 的 SC-C1 负责实测复现。
- **F9 整串检测完备（AWS 族）**：11 种写法（无空格 `;`、`&&`、`||`、子 shell、`$( )`、后台 `&`、管道、重定向）整串命中 = 逐段命中；`risky_patterns` 无 `^` 起首条目、无裸 `$` 收尾条目，12 条 `(^|[;&…])`、15 条 `($|…)` 交替。全族完备性留给 R1 的 SC-G9（既有全部 BLOCK 用例补填充）。→ `evidence/E7-gate-complete.txt`

## v1 → v2 更正（审计叙事放这里，不进 proposal）

v1 Decision record 的三条「硬事实」：

1. 「洞是真 bypass，单段绕过、分段救不了」→ **面更宽**：分段也绕过（F4 S 形），因为扫描器先于切分。
2. 「高阈值 64KB 是假选项，只有 ≤~12KB 的 cap 真关洞」→ 只在平方模型下成立；R2 线性化后超时门槛远高于 64KB，结论反转。
3. 「cap 放 compute_credit 入口即可、良性大命令不受影响」→ 控制流描述对（compute_credit 只在命中后跑），但**成本位置错**（F1–F3）：放在那里触发时 5s 已耗尽，作为主修法无效。

根因：设计时只核了控制流，没测成本位置，照搬了头注释的归因（memory `reporter-miscite` / `past-summary≠measurement` 同形）。B.1 抓住了它，但 v1 proposal 与 #228 comment 29792 已对外写了错的事实 → v2 改写 + #228 贴更正（owner 2026-10-20 批）。

## 阈值推导（R1，R2 重设）

- `_SG_RAW_GATE`：每档取「首遍扫描在该档最慢平台 ≤ ~2s」的最大尺寸。bash ≥ 4 → **4096**（E2：@4KB 扫描器 0.64s；Windows 按 #219 的 ×2.6 ≈ 1.7s —— ×2.6 来自 g-c，而 g-c 本身就是扫描器成本，故适用）；bash < 4 → **1536**（E4 @2KB 2.1s，平方外推 @1.5KB ≈ 1.2s）。
- `_SG_RAW_MAX` = **65536**：闸门自身（检测循环）在 bash 3.2 @64KB ≈ 1.1s（E5 线性外推）；与 `_SGV_TMAX` 同值。代价：> 64KB 的良性命令也被拦（今天它们靠 CC 超时放行）。

## 行号重锚（59e333c）

`_sg_line_match :182` · `_sg_safe_to_split :204` · `_sg_split_top :321` · `_sg_compute_credit :453` · `_sg_time_budget :609` · `_sg_over_budget :616` · `_sg_vx_collect :632`（时钟重置 `:633`）· `_sg_vx_pass :704` · `_sg_ext_pass :809` · `_sg_core_eval :906`（注释写 `:903`）· 源码闸门 `:926` · `# guard:ack` 判定 `:1166` · `risky_patterns :1183–1472` · `_sg_judge_one :1497` · `_sg_per_segment_eval :1537`（时钟重置 `:1542`）· 性能注释 `:586–587`（proposal v1 / #228 引的 `:586` 为该句起始行）。

## 流程判断（请 owner 复议，Rule #10）

1. A.1（起草 proposal）时未走 state-scanner / phase1_gate 认领（brainstorming 直接起草），于 B 入口按 `phase-b-developer` B.0 补认领。
2. 分支名沿用 aria 近 6 条先例 `feature/<change-name>`，未用 `branch-manager` 文档的 `feature/{module}/{task-id}-{desc}`（一个 change 跨多 task）。
3. 本记录宣称的「当前 v1.76.1 可被绕过」只在本机 Linux bash 5.2 / 3.2（Linux 构建）实测；Windows 数字为按 #219 的 ×2.6 外推，macOS 为 Linux 构建的 3.2 —— 未在真机复测。

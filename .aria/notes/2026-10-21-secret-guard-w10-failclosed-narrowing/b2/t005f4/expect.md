# t005f4 预期（先写，后跑；2026-10-25）

## 编辑（edit5f4.py，从 pre/ 改前副本出发，可重放）
- E1 hook：只变 5 行——`_sg_relax_ok` 的 `_sg_relax_nowslfs || return 1` 那行（只有行尾注释变），函数里 4 行（函数头注释、读出 0 行、binfmt_misc、`-x` 换成 `-d && -x`）；行数 1756 不变；`local`/awk/`-e`/`return 0`/`}` 与准入门 WSL 环境那行逐字不变；D-3 那句不动。proposal 的函数块与 `spec-probe2/spec5.sh` 逐字相同。hook 里旧函数与 `spec3.sh` 不逐字相同（已知：第 1 行第 300 字节起不同），换掉整个函数不受影响。
- E2 helper 与 sc-direct.sh 同一组改动（INV-2）：W1l 包进 uid 0 判断（+3 行）、新增 W1o（+4 行）、W1n 加一个 elif（+1 行）并补全注释（+1 行）、miss 清单加 W1o；681 -> 690 行；两份除头注释外仍同一代码（diff 只在第 2-10 / 2-4 行）。
- E3 套件：`SGW_EXP_DIRECT` 加 W1o、头注释 990 -> 991、984 -> 985；行数不变。sc-cases.sh：期望清单加 W1o，1 行变。
- E4 `mutants.py` 锚点不受 A 影响（锚点只到 `_sg_relax_nowslfs` 行首，不含行尾注释）：不改；`w14-mutants.py` 只改 `IMPL_SHA12`。

## prove5f4.sh
- P0 `bash -n`：5 个 bash x 5 个文件全过，stderr 0 字节。
- P1 能红（PATH bash 5.2.15，MODE relax，SC_ONLY `^V15-W1[a-mo]-`，共 14 条）：good FAIL [] PASS 14；v34fn（新 hook 换回 spec3.sh 的函数）FAIL [o] PASS 13；nodx（删掉 `-d && -x` 那行）FAIL [ko]；donly（只留 `-d`）FAIL [k]。norelax（3.2.57，`^V15-W1o-`）：good PASS，v34fn FAIL [status]。
- P2 W1n：PATH 前置从第 501 次起失败的 mount 包装 -> 新 helper 记 `SKIP ... [platform] the stacking stopped after 500 ...`（不是 FAIL/TIMED）；从第 1 次起失败 -> 照旧 `SKIP ... [platform] tmpfs cannot be mounted ...`；改前的 helper 在 501 包装下出 `TIMED ... bad ...`（硬判据坏，套件里即 FAIL）——对照用。
- P3 判据对照：四份判据导出与 5f3 逐字相同；13 种情形 x 5 个 bash 全一致（`13 cases, 0 not ok`），hook 的值 = proposal 所列（host 0、autofs 0、late 1、none 0、stacked 0、empty 1、unreadable 1、dir-as-table 1、noglob 1、failglob 0、nosearch 1、listless 1、xfile 1），stderr 0。
- P4 变异生成：mutants.py rc 0（57 + 7，hook 前缀为新值）；w14-mutants.py rc 0（31 行）。
- P5 commentsync：derive rc 0；与 5f3 版只差 FIX5_HOOK 一行（2 行 diff；拿不准：也可能多一个站点）；target / baseline / proto GREEN，四个构造 RED（计数可能与 78/60/58/57 略有不同）。

## runall4.sh（每步开跑前一分钟负载 < 1.2）
- perf-good（5.2.15/5.0.18/5.1.16/5.3.20）：`TIMED ... ok ok`，1000 层，返回 0，< 0.5 s；perf-v33fn：`TIMED ... ok bad`（约 2 s）。
- w10 过滤轮 5 个 bash：0 FAIL / MISSING / SETUP；比 5f3 多 1 条 PASS（W1o，两种模式都跑，3.2.57 上也是 PASS）。
- full-path：0 失败，总数比 5f3 多 1（本机无 zsh：985）；full-wsl（WSL_DISTRO_NAME=Ubuntu）：0 失败，总数同上。
- sc-cases：`PASS 161 FAIL 0 MISSING 0 SETUP 0 SKIP 0`。
- run-mutants v31 / suite：BI 全 CAUGHT，P-0 GREEN，扰动轮 0 not as expected（suite 模式在负载下可能有 NOT-JUDGED，按 runall3 的做法单跑）。
- w14：caught as predicted 26、caught by the added case 5、not judged 0、NOT CAUGHT 0（与 5f3 同）。

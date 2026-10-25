# 5f4 复核：预期（5f4 报告到达之前写下）

## 静态
- 5f4 的 hook 与 `expected-5f4.sh`（3ed6c24 的 hook 换上 proposal v3.5 的准入门第二行与整个函数，`mkexp4.py`）逐字节相同；相对 3ed6c24 的改动只有 5 行（准入门 1 行、函数 4 行：函数头、读出 0 行那行、binfmt_misc 那行、`-d && -x` 那行），`diff` 计 10 行。
- helper 相对 3ed6c24 与 `v31/sc-direct.sh` 相对 HEAD 的改动逐行相同（helper 独有的 MODE relax 清单行除外，若 W1n 的编号没变则该行不动）。
- 四份测试侧判据不动。

## 套件 V15（run-suite.sh，SG_W10_ONLY='^V15-'，PATH bash 5.2.15，uid 1000；新增那条记作 NEW = DIR 是普通文件）
- 负控（5f4 的 hook）：V15 全 PASS（W1l 在 uid 1000 下照常跑并 PASS；W1n 叠满 1000 层 PASS）。
- MD（`-d` 去掉，回到 `[[ -x ]]`）：只有 NEW 红。
- MX（整行去掉）：W1k 与 NEW 红。
- MW：只有 W1n 红。MG：W1i、W1j、W1l 红。MF：只有 W1g 红。ME：只有 W1f 红。MO：只有 W1m 红（[platform] [time]）。MS：只有 W1e 红（[closed]）。MI：W1e 红（[open] [closed]），另 T2 红（[value]，第三段复核已见）。MN：W1b、W1i、W1l 红。
- 以上每个坏实现，除所列编号外 V15 全 PASS。

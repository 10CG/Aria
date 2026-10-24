# 主控独立复核 T002b — 结果（2026-10-24 05:22–05:36 UTC）

预期写在 `PREDICT.md`（实测前）。被测 hook 一律直接取 aria 分支的 worktree（`af4658b6f935`），基线由 `git show 59e333c:hooks/secret-guard.sh` 现取（`e83c5e30f2cc`），不用执笔席的副本。所有轮次 `taskset -c 0,1 nice -n 19`，一次一个。脚本 sha256 前缀与报告第 4 节所列一致（`sc-cases e537079f6738`、`sc-direct e97513c59e58`、`mutants 2060d2e0c17f`、`shim 637c52c10bbf`、`run-mutants 201c646c5a41`、`commentsync cdab1c8debca`、`shapes 12ec06e470da`）。

| 预期 | 实测 | 一致 |
|---|---|---|
| 1. 实现 × 5.2.15：PASS 137，FAIL 0，SKIP 0，judged | PASS 137、FAIL 0、MISSING 0、SETUP 0、SKIP 0；负载 1.44 → 1.28，judged（`impl-5.2.15.txt`） | 是 |
| （补）实现 × 5.0.18 / 5.1.16 / 5.3.20 | 各 PASS 137、SKIP 0，judged（负载 1.44→1.60、1.49→1.69、1.42→1.30） | 是 |
| （补）实现 × 3.2.57（identity） | PASS 79、FAIL 0，judged（1.30 → 1.41） | 是 |
| 2. 基线 × 5.2.15：PASS 24，FAIL 39，MISSING 74 | 同（1.23 → 1.40，judged；`base-5.2.15.txt`） | 是 |
| 3. 57 个坏实现全 CAUGHT；P-0 GREEN；6 个扰动 CAUGHT | `57 caught, 0 missed, 0 wrong reason, 0 not judged, 0 setup`；P-0 GREEN；6／6 CAUGHT（`mut-summary.txt`） | 是 |
| 4. `SC_BASH` 指向不存在的文件：SETUP，退出码 3 | 两种（父目录不存在／存在）都是 `SETUP: SC_BASH does not run`、退出码 3 | 是 |
| 5. `sc-direct.sh` 启动即崩：V0-H1、V0-H2 两条 FAIL，退出码 1 | 同（副本第 2 行插 `exit 1`；`SC_ONLY` 只跑确定性部分，故缺编号数与报告不同，不可比） | 是 |
| 6. commentsync target：实现 GREEN；插字符绕过 RED (64)；整块删除 RED (57)；原型 RED (13) | 同；旧版 commentsync 对两种绕过都是 GREEN（复现 PP2-M）；原型的 13 项恰在站点 1、2、9、10，即 What 7 补充的四处 | 是 |
| 7. 抽查：坏实现文件与实现确有不同；指定用例的 FAIL 行带 `reasons.tsv` 的原因标签 | 57 个坏实现无一与实现逐字节相同；BI-24、BI-44、BI-37、BI-17b 各恰一行改动，FAIL 行分别带 `[status]`、`[value]`、`[status]`、`[value]`，与 `reasons.tsv` 一致 | 是 |

说明与偏差：

- 复跑坏实现那一轮后半段负载升到 2.2–3.5，38 轮的计时批记 `SKIP [load]`。依赖计时的 6 个坏实现（BI-2、6、7、13、14、15）都落在前半段的 judged 批里、全部抓住；其余在 load 批里被抓住的都是不依赖墙钟的硬断言（状态、文本、字节、`[uncut]`）。P-0 本轮只判了确定性部分（108 PASS、29 SKIP [load]）；P-0 的计时批由执笔席 05:06:55 的低负载轮判过（报告 4.6 节）。
- 报告称长行文案的期望文本「已机械核对与 proposal What 5 逐字相同（textcheck/）」，但 `textcheck/` 目录是空的。主控另写 `textcheck.py` 复核：proposal What 5 代码块、实现 hook 的 heredoc、`sc-direct.sh` 的期望文本三者按同一组参数代入后逐字节相同（854 字节、15 行）；两条增长原因串与 proposal What 5 表格同字。
- 主控自己的等待脚本 `other-bash.sh` 第一版犯了报告第 4.6 节写过的同一个错误（`waitlow` 等过之后返回非 0），5.0.18 与 5.3.20 因此被跳过；修好后补跑（`other.log` 的 `--- rerun` 之后）。

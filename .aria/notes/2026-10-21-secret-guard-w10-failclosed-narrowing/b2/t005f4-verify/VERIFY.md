# 修复轮第四段（5f4）主控复核（2026-10-25）

对象：aria worktree 相对 `3ed6c24` 的未提交改动（hook `628652570ce3`，helper、套件）与主仓 v31 的三个文件（`sc-direct.sh`、`sc-cases.sh`、`impl/w14-mutants.py`）。预期写在 `PREDICT.md`，在 5f4 报告到达之前写下。

## 1. 静态

- 主控照 proposal v3.5，从 `3ed6c24` 的 hook 拼出预期的 hook（`mkexp4.py`：换上准入门第二行与整个 `_sg_relax_nowslfs`，其余不动），得到 `expected-5f4.sh`。5f4 的 hook 与它**逐字节相同**，与预期一致。相对 `3ed6c24` 只改了 5 行：准入门 1 行，函数 4 行。
- INV-2：helper 相对 `3ed6c24` 的改动与 `v31/sc-direct.sh` 相对 HEAD 的改动逐行相同（各 19 行）。W1o 两种模式都跑，所以 helper 独有的 MODE relax 清单那一行没有改动。
- W1n 注释：在 `3ed6c24` 里截断在半句「soft (INV-7): the wall」，第三段就是这样提交的。主控复核第三段时按 260 列截读 diff，没看到行尾，第三轮复审也没报。5f4 把它补全成「the wall time, at most 0.5 s」，并写明三种 SKIP 情形，与代码相符；主控认可。
- commentsync 的导出与第三段逐字相同。它只绑定 What 7 各类注释里点名的句子，`_sg_relax_nowslfs` 与准入门那一行的注释不在其中，新旧措辞都不核。这几处属于 What 1 补充 2 的逐字代码块，由上面的逐字节比对核（4r 的 W8 也会按内容差逐字对 proposal），所以不是缺口。

## 2. 套件层的坏实现（`RESULT-suite.txt`，逐条结果在 `runs/*.log`）

跑法：`run-suite.sh`，`SG_W10_ONLY='^V15-'`，PATH 上的 bash 5.2.15，uid 1000。坏实现由 `mkmut4.py` 从 5f4 的 hook 构造：第三段复核的 9 个，锚点换成 v3.5 原文；另加 MD（`-d` 去掉，回到 `[[ -x ]]`），MX 改为整行去掉。每个 hook 开跑前一分钟负载都 < 1.2，首尾负载全部 < 2。

- 负控（5f4 的 hook）：20 / 20 PASS，W1n 读表 0.009 s。
- 10 个坏实现全部按 `PREDICT.md` 变红，编号与原因标签逐一相符：

| 坏实现 | 变红的用例与标签 |
|---|---|
| MD | W1o |
| MX | W1k、W1o |
| MW | W1n（2.254 s，界 0.5 s） |
| MG | W1i、W1j、W1l |
| MF | W1g |
| ME | W1f |
| MO | W1m [platform] [time] |
| MS | W1e [closed] |
| MI | W1e [open] [closed]，T2 [value] |
| MN | W1b、W1i、W1l |

## 3. 执笔席的各轮与它标出的不符（报告第 4 节与「预期与结果不符」，过程材料在 `../t005f4/`）

- 各轮：
  - 5 个 bash 的过滤轮各 159 条，FAIL 0；
  - 两次整轮各 985 条，FAIL 0；
  - sc-cases 161 PASS；
  - run-mutants 两种模式全部 CAUGHT，P-0 GREEN；套件模式首轮因负载有 4 项未判，重跑后已判；
  - w14 的 NOT CAUGHT 为 0。
- 判据对照：13 种情形 × 5 个 bash，hook 与四份测试侧判据逐种一致。
- 能红 / 能 SKIP 的证明（报告第 2 节）与主控上面的结果一致；W1n 的 SKIP 分支用从第 501 次起失败的 mount 包装证明。
- 执笔席自己标出 3 处不符：
  - 行数：它写预期后又改了注释，属预期写错。
  - commentsync 的导出没变：原因见第 1 节，不是缺口。
  - w14 的 Q-17 一次「在别处抓到」：之后单独重跑两次都按预期抓到。Q-17 是计时类坏实现，判为时序波动，4r 会在低负载下重跑 W14。

## 4. 执笔席拿不准的项

主控的裁定写在计划 TASK-005 notes 里。

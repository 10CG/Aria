# 修复轮第三段（5f3）主控复核（2026-10-25）

对象：aria worktree 相对 `710a36d` 的未提交改动（hook `16996eb7db21`，helper、套件）与主仓 v31 的五个文件（`sc-direct.sh`、`sc-cases.sh`、`commentsync.py`、`mutants.py`、`impl/w14-mutants.py`）。预期先写：`PREDICT.md` 第一节（函数层）与第二节在 5f3 报告到达之前写下；「二补」按 5f3 的编号写定，在套件实跑之前写下。

## 1. 静态

- 主控按 proposal v3.4 的两个代码块，从 `710a36d` 的 hook 独立拼出预期的 hook（`mkexp.py`）。它与 5f3 的 hook 逐字节 diff，只差 hook 头注释里的一处（What 7 补充 2 第 8 处，纯注释，见 `static-exp-vs-5f3.diff`），与预期一致。
- hook 相对 `710a36d` 的 hunk 数：在 `-U0` 下 4 个——头注释 1 个，准入门删一行、加一行共 2 个，函数整段替换 1 个；默认上下文下合成 3 个。
- 头注释新补的那句与重跑块头（:805 起）那句同义，并且属实。重跑只为基线按尺寸拦下的命令而跑，所以句中的 size block's text 就是基线文案。
- INV-2：helper 相对 `710a36d` 的改动，与 `v31/sc-direct.sh` 相对 HEAD 的改动逐行相同。唯一的差别是只有 helper 才有的 MODE relax 编号清单那一行（多了 W1n）。
- 测试侧有四份 WSL 判据：helper 与 `sc-direct.sh` 的 `wslmark`、套件的 `sg_w10_wslfs`、`sc-cases.sh` 的 `wslmark`。
  - 去掉注释后，四份函数体逐字相同（md5 前缀 `d53dfae530f5`）。
  - 写法与 hook 不同：用 cat 读表，awk 加 tail 取最后一条，在 cd 子壳里试搜索权限，再用 `[ -e ]` 查项。四份都不 source hook。
- 坏实现生成器两处锚点：`mutants.py` 的 BI-22 与 `impl/w14-mutants.py` 的 Q-30 都改成「`_sg_relax_left || return 1` 加上它的下一行 `_sg_relax_nowslfs`」。删掉的仍是 `_sg_relax_ok` 里那一行，所以坏实现本身不变。`IMPL_SHA12` 已改为 `16996eb7db21`。
- commentsync 只多绑定了头注释新增的那一句 D-3 例外。

## 2. 函数层的坏实现（`RESULT-fn.txt`）

9 个里 7 个与预期逐项相符。另有 2 处是我的预期写错了：ME 在「目录当表」上的结论，MG 在 failglob 下中止的范围。原因见该文件，两处都不影响抓不抓得住。

## 3. 套件层的坏实现（`RESULT-suite.txt`，逐条结果在 `runs/*.log`）

跑法：`run-suite.sh`，`SG_W10_ONLY='^V15-'`，PATH 上的 bash 5.2.15，uid 1000。每个 hook 开跑前一分钟负载都 < 1.2，首尾负载全部 < 2。

- 负控（5f3 的 hook）：19 / 19 PASS，W1n 读表 0.009 s。
- 9 个坏实现全部按「二补」的预期变红，编号与原因标签逐一相符：

| 坏实现 | 变红的用例与标签 |
|---|---|
| ME | W1f |
| MF | W1g |
| MG | W1i、W1j、W1l |
| MI | W1e [open] [closed]，另有 T2 [value] |
| MN | W1b、W1i、W1l |
| MO | W1m [platform] [time] |
| MS | W1e [closed] |
| MW | W1n（3.126 s，界 0.5 s） |
| MX | W1k |

- MI 下 T2 [value] 变红：T 系列事先没有作预测。原因是准入门恒关后判定根本不运行，正是 T2 注释里说的那种假红。

## 4. 执笔席的各轮（报告第五节，过程材料在 `../t005f3/`）

- 5 个 bash 的过滤轮都是 FAIL 0；3.2.57 上 67 条 SKIP [platform]。
- 两次整轮都是 FAIL 0 / 984。full-path 那一轮收尾负载 2.26，按 INV-7 整轮的计时结论不算数；不过移植用例那一批自身的首尾负载是 1.04 / 0.82，已判。4r 会在低负载下重跑。
- sc-cases：160 PASS。
- run-mutants：
  - v31 模式：63 个 CAUGHT，P-0 GREEN；
  - 套件模式：63 个 CAUGHT；P-0 首轮因负载未判，低负载单跑两次都 GREEN。
- w14：与 5f2 相同。
- 执笔席对 full-wsl 那一轮的预期写错了一处，报告里没有标出：
  - 它预期移植用例会 SKIP [platform]，实际照常按放宽跑。套件对移植用例会清掉 WSL 变量，这是 3a 起就定下的设计；
  - 旧的 6 组用例走基线支，与设计相符。

## 5. 执笔席拿不准的 7 项

主控的裁定写在计划 TASK-005 notes 里。

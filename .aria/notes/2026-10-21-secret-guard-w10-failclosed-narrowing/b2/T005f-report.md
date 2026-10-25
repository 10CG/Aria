# TASK-005 修复轮执笔席报告（10CG/aria-plugin#217）

> 本文由主控从执笔席交回的最后一条消息原样存入：执笔席写报告文件时被运行环境拒绝，报告全文在消息里（见第六节第 1 条）。证据文件在 scratchpad 的 `r217impl/t005f/`。

## 一、各项结论（一句话）

1. hook：WSL 一行按 proposal 逐字换成两行，新增 `_sg_relax_nowslfs`（放在闸门之上），What 7 补充 2 第 1-5 处注释已改。`git diff 2893bcc` 只有这些改动，5 个 bash 上 `bash -n` 都通过，新 sha256 前缀是 `50ce186a28c9`，所以 TASK-004 的证据按 INV-8 作废。
2. 套件：W10 块头那句同义句已改，8 个新编号加进 `SGW_EXP_DIRECT`，头注释计数改成 980 (974)、149，整轮实跑总数正好是 974。
3. helper 与 `v31/sc-direct.sh`：m-3、m-4、m-6 都做了，另加 8 条新用例：V15-T1/T2/T3 与 V15-W1a-e。两处改动行逐行比对，只差 helper 独有的 RELAX_IDS 那一行，符合 INV-2。
4. 能红：做了 9 个坏实现（任务书点名 6 个，另加 3 个），新用例在每个坏实现上都按预测变红，在实现上全绿。
5. sc-cases.sh：新编号已进 V0-H2 的期望清单；在实现上跑 PASS 150、FAIL 0，V0-H2 报「148 个编号各报一次」。
6. mutants.py：不用改。两个生成器在新旧 hook 上生成的坏实现，改动行逐个相同（v31 64 个、w14 31 个都是 0 处不同），A 的改动没碰任何锚点。
7. w14-mutants.py：只改了 `IMPL_SHA12`（hook 的 sha 绑定值，不是锚点），不改它在新 hook 上直接拒绝生成。
8. commentsync：按 3b 的做法机械导出了句子清单。target、baseline 都是 GREEN（另跑了 proto，也是 GREEN）；对基线做的「插字符」「整块删除」两种构造，hook 与套件各两个，全部 RED。
9. 各轮实跑：全部达到任务书要求，只有一条预期是执笔席读错了（第五节第 3 条）。

## 二、改动明细

- hook：两段代码由 `edit_hook.py` 从 proposal 里原样取出写入，没有手打。新函数放在 `_sg_relax_platform` 之后、`_sg_relax_noext` 之前。改了的注释段落按该段原有行宽重排：头注释 91 列；LENGTH BUDGET 与 `_sg_vx_pass` 说明 173 列；重跑块头 155 列。完整 diff 见 `t005f/hook.diff`。
- 套件：除了 W10 块头那句、`SGW_EXP_DIRECT` 与头注释计数，没有别的改动。
- helper / sc-direct.sh（同一个脚本 `edit_cases.py` 一起改）：m-3（V2-G12 / G13 的注释和 chk 文案只说关门一极，开门一极写明在 V14-G1，编号不变）；m-4（`nproc_binds` 快路径改用 `id -ru`，CapEff 由 bash 用 read 循环从 `/proc/$BASHPID/status` 读，注释改成 real user ID 0）；新用例 W1a-d 两种模式都跑，T1-T3 与 W1e 放在 relax 块末尾，每条都在子 shell 里重新 source hook；helper 的 RELAX_IDS 加了 4 个 relax 编号。
- sc-cases.sh：`EXP_DIRECT_BOTH` 加 W1a-d，`EXP_DIRECT_RELAX` 加 T1-T3 与 W1e。
- commentsync.py（脚本 `cs/derive-5f.py`）：对每个站点取 2893bcc 与修复轮的注释，在 `.` 与 `;` 之后切句，求出删去的句和新增的句；hook 一侧删去的句移出 new 清单、加进 untrue，按它在 59e333c 或原型里出现与否标 b / p / i，新增的句标 s；套件一侧删去的句放进新加的 `SUITE_RETRACT`（任何模式都须出现 0 次，`check_suite_text` 为此加了 2 行）。导出：hook 站点 1 删 2 增 2；站点 2 删 1 增 1；站点 5 删 1 增 1；站点 10 删 0 增 1；套件站点 9 删 2 增 2。

## 三、What 7 补充 2 每处改前改后（读者所见形式，供回填 proposal；逐行形式见 hook.diff）

1. hook 头注释（新文件 :93-:101）——改前：「A substituted copy over 8192 characters is blocked for its size only where the relaxed rerun of 10CG/aria-plugin#217 is not in effect; where it is (an x86_64 GNU/Linux build of bash 5.0-5.3 outside WSL, no project extension, time left), the pass is re-run under a hard deadline with no count bound, the growth over the input as the limit and the copy judged in full, and growth over 8192 characters, the deadline or any failure of the rerun still blocks.」改后：「A substituted copy over 8192 characters is blocked for its size wherever the relaxed rerun of 10CG/aria-plugin#217 is not in effect, and also where it is (an x86_64 GNU/Linux build of bash 5.0-5.3 outside WSL, no project extension, time left) whenever that rerun falls back. The rerun runs the pass again under a hard deadline with no count bound, the growth over the input as the limit and the copy judged in full: growth over 8192 characters blocks with the growth text, a value over 4096 characters with the value text (the rerun reaches values that the counts cut off in the baseline pass), and the deadline, a time checkpoint, the self-check or any other failure of the rerun falls back to that size block.」套件 W10 块头的同义句：「… blocked that way only where the relaxation is not in effect (…; P2).」改成「… blocked that way wherever the relaxation is not in effect (…; P2), and also where it is whenever the rerun falls back (the deadline, a time checkpoint, the self-check, any other failure: What 4).」（VMAX 那一点由同段首句的 on every platform 覆盖。）
2. LENGTH BUDGET（:602-:605）：「whenever the rerun does not finish in time,」改成「whenever the rerun neither allows nor blocks on its own (the deadline, a time checkpoint, the self-check, any other failure),」。
3. `_sg_relax_noext` 行尾注释——改前：「prints "none" only when no extension can be in effect: no project root, or no .aria/secret-guard.paths under it. A file in any state, or an error, keeps the relaxation off」改后：「prints "none" only when no extension can be in effect: no project root is found (_sg_ext_root prints nothing, which includes a cwd that jq cannot read: without a root no extension can be in effect), or there is no .aria/secret-guard.paths under it. A file there, in any state, keeps the relaxation off」
4. `_sg_vx_pass` 说明（:724-:727）：「the baseline block text is kept in _SG_OV_PAT / _SG_OV_MODE for the fallback)」改成「the baseline reason string and mode are kept in _SG_OV_PAT / _SG_OV_MODE -- not a text: on a fallback _sg_emit_blocked writes the baseline block text from them again)」。
5. 重跑块头（:802-:805）：原句保留，后面补「The one exception (What 4): a fatal error of bash itself inside the job that makes it exit with status 2 and write its error message is passed on as the block text -- the command is still blocked, but with bash's message instead of the baseline text.」
6. WSL 两行的注释：逐字照抄 proposal。

## 四、新用例与「能红」证明

- V15-T1：子 shell 里定义一个 `sleep` 函数，先记下参数再真睡；`_sg_relax_left` 桩成把 `_SG_LEFT` 设为 1.234567；判定桩先等到参数记下了才返回；断言记下的参数恰好是 1.234567。
- V15-T2：静态——hook 里非注释行对 `_SG_P0=` 的赋值恰好 1 处，并且就在 `set -uo pipefail` 的下一行；直调——锚点设为「现在减 2.5 s」、预算 3，真 `_sg_vx_pass` 处理一条副本超过 8192 的命令，由它去问真准入门、再由真 run 起真作业，只把作业里的那次判定桩成记下 `_SG_LEFT`，断言 0 < 值 <= 0.5。与审查报告第 5 项字面的差别：报告写的是「桩作业」，执笔席桩的是作业里的判定，因为桩掉整个作业时「在作业里重取锚点」那段代码不会执行。
- V15-T3：`_sg_relax_job` 桩成 `kill -KILL "$BASHPID"`，断言 `_sg_relax_run` 返回 4 且 stderr 为空。
- V15-W1a-d：`_sg_relax_nowslfs` 直调，用假挂载表和 helper 自己 `$X` 下的目录，每张假表的最后一行都故意不匹配：autofs 加 `WSLInterop` 返回 0；binfmt_misc 加 `WSLInterop-late` 返回 1；binfmt_misc 但没有 `WSLInterop*` 项返回 0；挂载表读不出返回 1；四条都要求 stderr 为空。
- V15-W1e：relax 模式下把 `_sg_relax_nowslfs` 桩成返回 1，期望准入门返回 1。

坏实现在 `t005f/bad/`（`mkbad.py` 生成），实测全部与预期一致：B1 WSL 恢复旧的单行 `-e` -> W1e [status]；B2 循环里用 `&& m=1` -> W1a、W1c [status]（本机挂载表末行不匹配，准入门随之关上，T2 [value] 也红）；B3 `<` 写在 `2>/dev/null` 前面 -> W1d [stderr]；B4 计时器睡 3 -> T1 [value]；B5 作业里重取锚点 -> T2 [static][value]；B6 去掉 `exec 2>/dev/null` -> T3 [stderr]；B7 run 里重取锚点 -> T2；B8 准入门里重取锚点 -> T2；B9 未挂上也看项（D-2 本身）-> W1a [status]。实现上：5.2 relax 下 8 条 PASS；3.2 norelax 下 W1a-d PASS，另外 4 条 SKIP [platform]；套件过滤轮（`^V15-`）与 sc-cases 各一次，都是 PASS 10 / 10。

## 五、各轮预期与结果（预期开跑前写进 `t005f/expect.md`；编排 `runall.sh`）

| 轮次 | 结果 | 首尾负载 |
|---|---|---|
| W10-only，bash 5.0.18 / 5.1.16 / 5.2.15 / 5.3.20 | 每轮 PASS 149/149，FAIL 0，SKIP 0；计时批判过 | 1.15->1.33、1.11->1.08、1.08->1.39、1.12->1.46 |
| W10-only，bash 3.2.57 | PASS 82，SKIP 67 全是 [platform]，FAIL 0；计时批判过 | 1.17->1.79 |
| 整轮，PATH 上的 bash | PASS 974/974，FAIL 0，SKIP 0；计时批判过 | 1.10->2.47 |
| 整轮，导出 `WSL_DISTRO_NAME=Ubuntu` | FAIL 0，PASS 945，SKIP 29 全是 [void]；6 组走 baseline branch | 1.19->2.75 |
| sc-cases.sh | PASS 150，FAIL / MISSING / SETUP / SKIP 都是 0；计时批判过 | 1.19->1.05 |
| run-mutants，v31 模式 | 63 个 CAUGHT，P-0 GREEN，扰动 0 个不如预期 | 1.05->1.75 |
| run-mutants，套件模式 | 63 个 CAUGHT；P-0 首跑 NOT-JUDGED（开跑负载 2.15），低负载单独重跑 GREEN | 重跑 1.14->1.36 |
| w14.sh | as predicted 26，by the added case 5，NOT CAUGHT 0，not judged 0 | 1.16->1.15 |
| commentsync | target / baseline / proto 都是 GREEN；四个构造 RED（77、59、58、57 项） | - |

## 六、未完成或拿不准的项

1. 报告文件没写成（运行环境拒绝子代理写这类文件）；本文由主控存入。
2. w14-mutants.py 改了 `IMPL_SHA12`（af4658b6f935 -> 50ce186a28c9）：不是锚点，不改就不能在新 hook 上生成；hook 以后再改一个字节，这个值也要跟着改。
3. WSL 整轮的预期执笔席写错了：移植用例按设计会清掉环境里的 WSL 变量（R2 PP2-m14），照常走 relax。不是缺陷。
4. 一处同类失实没改：重跑块头 :796 一带的「keeps the baseline block text in _SG_OV_PAT / _SG_OV_MODE」，与 m-2 第 4 处同一个问题，不在清单里。
5. 测试侧的 WSL 判据还是旧的 `-e /proc/sys/fs/binfmt_misc/WSLInterop`：helper :72 的 `WSLM`、套件 :374 与 :2931、`sc-cases.sh` :47。在只有 `WSLInterop-late`、挂载表读不出、或 binfmt_misc 是没挂上的自动挂载点的宿主上，测试侧会和 hook 的判定对不上（只会假红）；测试侧的 `-e` 本身也可能卡在没人服务的自动挂载点上。
6. commentsync 管不到行尾注释（noext 的行尾注释、WSL 两行的注释），只能靠审读。
7. V15-T2 在极重负载下会假红（从设锚点到问准入门之间若超过 0.5 s）；可改成 2.0 s / 1.0 s。
8. INV-4 的静态清单没列 `_sg_relax_nowslfs`（W1a-e 间接覆盖：放到闸门之下时 helper 取不到，报 MISSING）。

工具调用 52 次（含被拒的那次写入）。

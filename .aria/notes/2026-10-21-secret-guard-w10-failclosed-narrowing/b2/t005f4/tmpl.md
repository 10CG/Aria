# T005f4 报告：TASK-005 修复轮第四段（10CG/aria-plugin#217）

执笔席（全新实例），2026-10-25。脚本与证据都在 `r217impl/t005f4/`：`expect.md`（先写的预期）、`edit5f4.py`（全部改动，从 `pre/` 的改前副本出发，可重放）、`prove5f4.sh`（bash -n、坏实现、能红 / 能 SKIP、判据对照、变异生成、commentsync）、`runall4.sh`（各轮）、`q17.sh`（W14 Q-17 单独重跑）、`proofs/`、`runs/`、`diffs/`、`cs/`、`bad/`、`mnt/`（mount 包装）。没有 commit。

## 结论一览

- **A hook**：按 proposal v3.5（What 1 补充 2）两个代码块用脚本取出后替换：`_sg_relax_ok` 里 `_sg_relax_nowslfs || return 1` 那行（只有行尾注释变）、整个 `_sg_relax_nowslfs`（函数头注释、读出 0 行与 binfmt_misc 两行的注释、`[[ -d "$d" && -x "$d" ]] || return 1`）。只动 5 行（-5 +5），行数 1756 不变；准入门 WSL 环境那行与 D-3 那句未动。proposal 的函数块与 `spec-probe2/spec5.sh` 逐字相同。新 hook sha256 前缀 **628652570ce3**（旧 16996eb7db21）。
- **B 用例**：新增 `V15-W1o-regular-file-as-directory`（两种模式、不分 uid）；W1l 在 uid 0 下记 SKIP [platform]（照 W1k）；W1n 叠到 1-999 层停下时记 SKIP [platform]；helper、`v31/sc-direct.sh` 同一组改动（INV-2：两份文件之间的差异行改前改后完全相同，77 行），清单（helper 的 miss 清单、套件 `SGW_EXP_DIRECT`、`sc-cases.sh` 期望清单）与套件头注释计数（990 -> 991、984 -> 985）已改。能红 / 能 SKIP 证明全部如预期。
- **判据对照**：主控 13 种情形 x 5 个 bash，hook 的函数与四份测试侧判据逐种全一致（`13 cases, 0 not ok` x 5），hook 的 stderr 全程 0 字节；四份判据导出与 5f3 逐字相同（未改）。
- **C 工具**：`mutants.py` 与 w14 Q-30 的锚点只到 `_sg_relax_nowslfs` 行首，不受 A 影响，未改；两者在新 hook 上全部能生成（57 + 7；31）。`impl/w14-mutants.py` 只改 `IMPL_SHA12` 为 628652570ce3。commentsync 照第三段做法从 eeb67786 版重新导出，结果与 5f3 版逐字相同（git 无变化）；target / baseline / proto GREEN，四个构造 RED（78、60、58、57，与 5f3 相同）。
- **各轮**：全部 0 FAIL / MISSING / SETUP；过滤轮 5 个 bash 各 159 条（5f3 为 158）；整轮两轮各 985 条（5f3 为 984；本机无 zsh）；sc-cases PASS 161；run-mutants 两种模式 BI 全 CAUGHT、P-0 GREEN（suite 模式第一轮在负载下有 3 个 BI 与 P-0 NOT-JUDGED，按 runall3 的做法低负载重跑后全判）；w14 NOT CAUGHT 0、not judged 0，但 Q-17 一条从「caught as predicted」变成「caught elsewhere」（见下面不符第 3 条）。

## 预期与结果不符（逐条）

1. **helper / sc-direct 行数**（expect.md E2）：预期 helper 681 -> 690；实际 692（sc-direct 638 -> 649）。原因是我写预期之后把 W1o 的 if 行注释折成了两行（W1o 块 5 行而非 4 行）、W1n 补的注释是 2 行而非 1 行。属预期写错，改动内容见第 2 节。
2. **commentsync 导出的 diff**（P5）：预期与 5f3 版差 2 行（FIX5_HOOK 一行）；实际 0 行，导出与 5f3 版逐字相同。derive 的输出把每个站点记成（站点名, 删的单元数, 增的单元数），如 `('1 header: shell variable indirection', 2, 3)`；本轮只改了已有注释单元的文字，没有增删单元，所以导出不变。我推测 commentsync 只比对单元的增删、不比对单元里的文字——这意味着本轮这几处注释措辞的改动它看不到；没有读它的源码证实，留主控判断是否要紧。
3. **w14 的分布**：预期与 5f3 相同（caught as predicted 26、caught by the added case 5、caught elsewhere 0）；实际 25 / 5 / **1**，not judged 0、NOT CAUGHT 0。那一条是 Q-17（job 的命令替换不再静默自己的 stderr）：预期抓手 V6-E2-deadline-fallback-bytes 这次是 PASS，由整轮里 V3-S4、V5-S5、V4-S6、V15-T3 等多条 FAIL 抓到。之后单独重跑 Q-17 两次（`q17.sh`，首尾负载 1.02/1.01、1.01/0.93）都是 caught as predicted（V6-E2 FAIL [bytes]）。本轮没有碰 job 与截止相关的代码，我判断是 V6-E2 在这个变异上的抓取依赖时序、整跑那一次没抓到，不是本轮引入；这一点没有进一步证明。
4. **（过程，非结果）** prove 的后台 PID 记成了 setsid 的包装进程（本会话 Bash 工具的 shell 开着作业控制，setsid 因此另 fork 一层），第一次等待提前返回，当时看到的 prove 输出不全；之后按输出文件末行（`runall4 started`）确认 prove 已跑完。runall4 的 PID 由脚本自己写 `$$`，等待与「ALL DONE」一致。没有杀过任何进程；收尾时命令行含 t005f4 的进程为 0（见第 6 节）。

## 未做或拿不准的项

- **W1l 的 uid 0 分支**本机造不出（uid 1000），只做了代码审读：与 W1k 同形（`[[ "$(id -ru)" == 0 ]]` 时 `out SKIP ... "[platform] ..."`，否则原样构造并判定）；uid 1000 下 W1l 照旧判定（各轮 PASS）。
- **W1n 注释**：3ed6c24 里这条的注释截断在「soft (INV-7): the wall」（edit5f3.py 的模板里就是这样）。本轮改 W1n 时补成「the wall time, at most 0.5 s」并加一句 SKIP 的三种情形——超出任务书逐条列出的范围，请主控确认措辞。
- **helper W1 段头注释**（「A table that cannot be read or reads empty, or a DIR that cannot be searched, keeps the relaxation off」）没有随 v3.5 改成「not a directory that can be searched」：任务书没列，字面仍成立（普通文件同样查不了），保留未动。
- 没有为 W1o / `-d` 判据新增 v31 变异（任务书没要求）；`nodx`、`donly` 两个坏实现只在 scratchpad 里用来证明 W1k 钉住 `-x`、W1o 钉住 `-d`。
- 复审第三轮观察二（假表路径含空白时 W1b / W1i / W1l 假红）按主控裁定只记录；新 W1o 用同一种假表写法，同样受影响。
- INV-7：步级首尾负载 >= 2 的步有 full-path（尾 2.08）、full-wsl（尾 1.98，未到 2）、mut-v31（尾 2.21）、mut-suite（尾 2.37，已按 NOT-JUDGED 重跑）。这些步里的计时判定由套件 / run-mutants 自己的批内读数决定（均 judged，或已重跑判定）；步级读数不作为计时结论的依据。W1n 的计时（perf 各步）首尾负载都 < 2。

## 1. hook 完整 diff（相对 3ed6c24）

```diff
@@HOOKDIFF@@```

## 2. 新用例与改过的用例

helper（`hooks/tests/lib/secret-guard-w10-direct.sh`）的 diff 如下；`v31/sc-direct.sh` 是同一组改动（行号不同）。

```diff
@@HELPERDIFF@@```

### 能红 / 能 SKIP 的证明（`prove5f4.sh`，PATH 上的 bash 5.2.15 除注明外；坏实现在 `bad/`）

- `v34fn` = 新 hook 换回 `spec-probe2/spec3.sh`（v3.4）的函数；`nodx` = 删掉 `-d && -x` 那行；`donly` = 那行只留 `-d`；`v33fn` = v3.3 的函数（`spec-probe2/old.sh`，给开销用例）。
- W1o 能红：v3.4 的函数上 W1o FAIL（status 0, want 1），其余 13 条 PASS；两种模式都验了（3.2.57 MODE norelax 上同样 good PASS、v34fn FAIL）。
- W1n 能 SKIP：PATH 前置 `mnt/mount`（真 mount 的包装，从第 501 次起返回 32）——新 helper 记 SKIP [platform]（不是 FAIL）；从第 1 次起失败——照旧 SKIP [platform]；对照：改前的 helper 在同一包装下出 `TIMED ... bad ok`（硬判据坏，套件里即 FAIL，正是复审观察一说的硬红）。W1n 原有的红：v3.3 的函数上 `TIMED ... ok bad`（2.394 s）。
- W1l：uid 0 分支只做代码审读（见上）。

```
@@PROVE@@```

## 3. 判据对照表（主控 13 种情形，`spec-probe2` 的 `cases5.sh` 同一组假表、目录与参数；`cmp5f4.sh` = 5f3 的 `cmp5f3.sh` 加 xfile 一条）

每格按 3.2.57 / 5.0.18 / 5.1.16 / 5.2.15 / 5.3.20 列。测试侧判据的 0 表示「有标记」（与 hook 相反），所以 hook 为 1 时四份判据应为 0。

@@TABLE@@
## 4. 各轮预期、结果与首尾负载

预期见 `expect.md`（先写）。步级记录（`runs/steps.log`，每步开跑前一分钟负载 < 1.2）：

```
@@STEPS@@```

| 轮 | 预期 | 结果 | 符合 |
|---|---|---|---|
| bash -n（5 个 bash x 5 个文件） | 全过 | 25 项全过，stderr 0 字节 | 是 |
| perf-good（5.2.15 / 5.0.18 / 5.1.16 / 5.3.20） | TIMED ok ok，1000 层，< 0.5 s | 4 次 ok ok，1000 层，0.008-0.009 s | 是 |
| perf-v33fn（5.2.15） | TIMED ok bad，约 2 s | ok bad，2.394 s | 是 |
| 过滤轮 5 个 bash | 0 FAIL，比 5f3 多 1 条 | 各 FAIL 0 / 159（5f3 为 158）；3.2.57 SKIP 67 [platform]（与 5f3 同），其余 SKIP 0 | 是 |
| full-path | 0 失败，985 | FAIL 0 / 985，SKIP 0（5f3：984） | 是 |
| full-wsl（WSL_DISTRO_NAME=Ubuntu） | 0 失败，985 | FAIL 0 / 985，SKIP 0（5f3：984） | 是 |
| sc-cases | PASS 161，其余 0 | PASS 161 FAIL 0 MISSING 0 SETUP 0 SKIP 0 | 是 |
| run-mutants v31 | BI 全 CAUGHT，P-0 GREEN | 57 CAUGHT，P-0 GREEN，扰动轮 0 not as expected | 是 |
| run-mutants suite | 同上（可能需按负载重跑） | 第一轮 54 CAUGHT，BI-13/14/15 与 P-0 NOT-JUDGED；重跑 3 CAUGHT；P-0 单跑 GREEN；扰动轮 0 not as expected | 是 |
| w14 | 26 / 5 / 0 / 0 / 0 | 25 / 5 / **1** / 0 / 0（Q-17，见不符第 3 条；单独重跑两次均 as predicted） | **否** |
| commentsync | 与 5f3 差 2 行；GREEN x 3，RED x 4 | 差 0 行；GREEN x 3，RED x 4（78/60/58/57） | **diff 行数否**，其余是 |
| 变异生成 | 57 + 7；31 | 57 + 7（hook 628652570ce3）；31 | 是 |
| 判据对照 | 13 x 5 全一致 | 13 x 5 全一致 | 是 |

## 5. 其他文件的改动

套件（`hooks/tests/secret-guard.test.sh`）、`v31/sc-cases.sh`、`v31/impl/w14-mutants.py`（`v31/sc-direct.sh` 与 helper 同，略）：

```diff
@@OTHERDIFF@@```

## 6. 收尾状态

```
@@FINAL@@```

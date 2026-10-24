
实测 (11:12:39Z 开跑, 11:18:12Z 结束; 开跑负载 0.89 1.15 1.34, 结束 1.59 1.77 1.59; 输出 `t002d/pre.out`、`t002d/pre.w10log`):
- PASS 926 / FAIL 6 / SKIP 29 (全是 [load]) / 总数 961;
- FAIL 恰为 21ab (11 项检查不符)、21ac (3)、21ag (1)、21aj (3)、21al (3)、21ao (3);
- SC-13 绿 (不在 FAIL 里);
- W10 计时批 SKIP [load] (批开始负载 2.45)。

四条预期全部对上。附记: 21ab 的 11 项 = (a) 8193 字符副本出 longline 文案 3 项 + (b)(c) 两条无读取者的大段被放行 (exit 0)。W9-suite.txt 里 21ab 只列 3 项 (另一轮: 负载 3.59, 原型 9f61db0e7b8b), 与本轮不同, 见第 6 节第 1 条。

## 1. 改了哪些文件

- worktree `hooks/tests/secret-guard.test.sh` (`git diff --stat`: 145 行增, 45 行删; 未 commit)。改前副本 `t002d/suite.3a64827.sh`。
- 主仓 `.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/commentsync.py`: 只加不删 (与改前副本 `t002d/commentsync.orig.py` 比, 删除行 0)。hook 一侧、现有锚点、哈希、标题检查、ADD 词都没动。
- 改动由 `t002d/apply3b.py` 机械落地 (`suite` / `cs` / `verify` 三个子命令; 每个锚点要求恰好一处命中), 没有手改。hook、helper、垫片、`v31/run-suite.sh` 都没动。

套件改动逐项:
1. **W10 批移到最前** (3a 主控裁定 1): `sg_w10_cases` 只剩一处调用, 在移植块之后、第一条旧用例之前 (原过滤轮处); 设了 `SG_W10_ONLY` 时照旧打印过滤轮汇总并退出, 没设时继续跑旧用例。SC-13 前那次调用删掉, 原处留一行注释指向新位置。负载门槛 2、本批首尾各读一次都没动。头注释 (移植说明一句)、移植块块首、调用处三处注释改写; `just before SC-13` 在套件里 0 次。
2. **一套规则**: 新增 `sg_w10_relax_rule MACH MAJ MIN OSRELEASE WSLINTEROP` (What 1 与 What 1 补充的平台规则, 每个参数带缺省); 移植用例的 `SGW_RELAX` 那一行改为调用它 (规则字面不变), 6 组的判据也调用它。
3. **6 组按平台分两支**: 判据只算一次 (`wpa_rx6`, 在 W10 旧块的 helper 之后、21aa 之前), 见第 2 节。新 helper `wpa_x_longline`、`wpa_x_hit` 与增长文案行 `wpa_L_gseg`。每组仍是一个 `wpa_begin_bash_case` … `wpa_end_case`, 两支计数相同。
4. **7 块注释、2 处相邻头注释 (KM2-14 的第 21、22 处)、5 个标题**整块改写, 见第 3 节。
5. **头注释**: Expects 行改成实查的依赖清单 (含主控补充的 bash 5.0 要求); Coverage 行加 "counted in a git checkout of aria", 两个数不变 (实跑仍是 961, 见第 4 节); 移植说明改为 "defined after the helpers and run once, before every older case"。
6. **Summary** 加一行 `W10 older groups 21ab 21ac 21ag 21aj 21al 21ao: <哪一支> | bash on PATH <路径> <版本> (machtype <BASH_VERSINFO[5]>) | osrelease <内核串> | WSLInterop <yes/no> | WSL_DISTRO_NAME '<值>' WSL_INTEROP '<值>'`。

Expects 行逐项实查 (行号为改前 3a64827 的):
- bash 5.0 以上 (主控补充): `:29 set -u`; SC-8 计时基础设施 `:2146-2148` 读 `$EPOCHREALTIME`; `sg_w10_run` `:236`、`:239` 读 `$EPOCHREALTIME`。bash 4.x / 3.2 没有这个变量, `set -u` 下中止。`SC_BASH` 不受此限 (本段 3.2.57 那一轮即为实证)。
- jq: `:325` (`SGW_JQ`)、`:893` 等。
- python3: `:1433` (SC-20 两份改写副本)、`:1945` (SC-19 census, `corpus_census.py`)。改前 Expects 说 "只给 SC-20 用" 不实 (3a 第 6 节第 4 条)。
- timeout: `:359` 起 (移植的端到端用例; 没有时 SKIP [platform])。其余出现处都是传给 hook 的命令文本, 不执行。
- ps: `lib/secret-guard-w10-direct.sh:224-225` (`lv`、`lv5`), `:238` 没有 ps 时 V5-S13b 记 SKIP [platform]; 另一条用到 `lv5` 的是 `:313` 的 V5-S12-no-leftovers (第二条的 SKIP 分支未逐行核对, 照任务书写 "two")。
- git: `:1608` (SC-9a 的改前比对)、`:2055` (SC-8) 用 `git show af87cae:...`; 取不到时打印 [SKIP] 行、不计数 (所以 Coverage 写明是 git 检出里的数)。
- zsh: `:1097` 的条件组, 6 个 `zsh_case` (`:1105-:1110`)。

## 2. 6 组两支的断言对照

判据 (`wpa_rx6`, 只算一次): `sg_w10_relax_rule` 对 **PATH 上的 bash** (经 `env bash -c` 取 `BASH_VERSINFO[5]`、`[0]`、`[1]`, 与 hook 的 shebang `/usr/bin/env bash` 同一查找; 不是 `SC_BASH`)、`/proc/sys/kernel/osrelease`、`/proc/sys/fs/binfmt_misc/WSLInterop` 是否存在成立, **且**套件环境里 `WSL_DISTRO_NAME`、`WSL_INTEROP` 都为空 (旧用例经 `wpa_err` 把环境原样传给 hook)。成立 = 放宽生效支, 否则 = 基线支。

扩展: 6 组都在 `wpa_use_none` 下跑 (W10 旧块 `:2817`、`:2826`、`:2828`、`:2830` 起 `wpa_use_none`; 块内下一处 `wpa_use_proj` 是 21ao 之后、21ap 之前的 `:3012`), **没有**用例经 `wpa_use_proj` 设带扩展清单的项目, 所以扩展条件恒成立、不入判据。准入门的时间条件 (`_sg_relax_left`) 套件无法预判, 不入判据 (见第 6 节第 1 条)。

| 组 | 子断言 (命令) | 其余平台: 原断言, 一字不改 | 放宽生效: 新断言 | proposal 出处 |
|---|---|---|---|---|
| 21ab | (a) `wpa_vx_cmd 159`: 副本 8193, 增长约 8 KB | `wpa_x_toolarge … "$wpa_L_seg"` | `wpa_x_longline` | What 1 (触发点上完整判定)、P7 (最长行 > `_SGV_LMAX` 只匹配规则)、What 5 (longline 文案) |
| 21ab | (b) `f=x; echo $f<9000 填充>`: 增长 ≤ 0 | `wpa_x_toolarge … "$wpa_L_seg"` | `wpa_x Bash 0` (放行) | R-a (增长不超过 8192 → 完整判定, 无规则命中即放行)、P7 |
| 21ab | (c) `f=x; echo $f< a×4500>` | `wpa_x_toolarge … "$wpa_L_seg"` | `wpa_x Bash 0` (放行) | R-a、P7 |
| 21ac | (a) `f=<4096>; cat $f`: 副本约 4.1 KB | `wpa_x_finding` | `wpa_x_hit` | P1 (不在触发点, 与基线相同) |
| 21ac | (b) `for f in <3000>; …`: 副本约 6 KB | `wpa_x_finding` | `wpa_x_hit` | P1 |
| 21ac | (c) `for f in <4096>; …`: 副本约 8.2 KB, 增长约 4 KB | `wpa_x_toolarge … "$wpa_L_whole"` | `wpa_x_longline` | P7、What 5 |
| 21ag | `wpa_vx_dense 300`: 副本约 36 KB, 增长约 35 KB | `wpa_x_toolarge … "$wpa_L_seg"` | `wpa_x_toolarge … "$wpa_L_gseg"` | P8 (增长 > 8192 仍拦)、What 5 (分段增长原因串) |
| 21aj | `wpa_vx_over 1 / 7 / 8`: 每段副本约 12 KB, 增长约 12 KB | `wpa_x_toolarge … "$wpa_L_seg"` ×3 | `wpa_x_toolarge … "$wpa_L_gseg"` ×3 | P8、What 5 |
| 21al | (a) `wpa_vx_braced 31`: 整串副本 8192 | `wpa_x_finding` | `wpa_x_hit` | P1 |
| 21al | (b) `wpa_vx_braced 32`: 8193, 增长约 5.4 KB | `wpa_x_toolarge … "$wpa_L_whole"` | `wpa_x_longline` | P7、What 5 |
| 21ao | (a) `wpa_vx_whole 2123`: 整串副本 8192 | `wpa_x_finding` | `wpa_x_hit` | P1 |
| 21ao | (b) `wpa_vx_whole 2124`: 8193, 增长约 4 KB | `wpa_x_toolarge … "$wpa_L_whole"` | `wpa_x_longline` | P7、What 5 |

新 helper 的检查项: `wpa_x_longline` = 退出码 2、出现 `has a line longer than`、出现 `Matched pattern:`、不出现 `too large to scan`、全文 < 3000 字符 (What 5: 只回显命令前 200 字符, 分段模式不追加 Triggering segment 行)。`wpa_x_hit` = 退出码 2、出现 `value-REDACTING filter`、不出现 `has a line longer than`。`wpa_L_gseg` = `a command segment grows by more than 8192 characters after variable expansion` (What 5 分段增长原因串, `_SGV_GMAX` 8192)。放宽支不再用 `wpa_x_finding` 区分普通命中与 longline (PP1-A12)。

新期望的来源: 先按 proposal 推 (触发点 = 副本 > 8192; 增长与 `_SGV_GMAX` 比, 按该段自身输入量; 最长行与 `_SGV_LMAX` 比), 再与改前现状轮的 FAIL 明细对照, 12 条全部一致; 不是照抄实现输出。逐条的副本长度与增长推算写在各组注释里。

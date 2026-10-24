# TASK-002 第三步 3b 报告 (10CG/aria-plugin#217)

## 结论

- 改前现状轮: 四条预期全部对上 (FAIL 恰为 6 组、总数 961、SC-13 绿、计时批 SKIP [load])。
- W10 批移到套件最前: 完成。五个 bash 的验收轮计时批全部判过 (首尾负载都 < 2); 3.2.57 第一轮结束读数 2.04 作废, 重跑判过。
- 6 组按平台分两支: 完成。五个 bash 轮都走放宽支、FAIL 0; 导出 WSL_DISTRO_NAME 的一轮走基线支、FAIL 0。**需主控裁定**: 放宽支依赖重跑在 3 s 截止前跑完, 21ab 的两条放行断言只差 0.2-0.5 s, 3.2.57 第一轮在负载约 2.3 下翻红过一次 (第 6 节第 1 条)。
- 7 块注释、2 处相邻头注释、5 个标题: 改写完成; 锚点短语与旧标题在套件里 0 次, 注释里 `_SGV_GMAX` 8 次、`longline` 14 次。
- commentsync 套件一侧逐句核对: target GREEN、baseline GREEN, 三种构造都 RED。
- 头注释: Expects 行按实查改 (含 bash 5.0 要求); Coverage 两个数不变 (git 检出实跑 961, 有 zsh 的 967 为推算)。

## 0. 改前现状轮 (先写预期, 后跑)

预期 (写于开跑前): worktree 3a64827, hook sha256 前缀 af4658b6f935, PATH 上的 bash (/usr/bin/bash 5.2.15) 整轮跑:
- FAIL 恰为 SC-21ab、SC-21ac、SC-21ag、SC-21aj、SC-21al、SC-21ao 六组 (旧断言在放宽生效的平台上红);
- 总数 961;
- SC-13 绿;
- W10 计时批多半 SKIP [load] (批在 SC-13 前, 开批时负载已被前面 7 分钟旧用例抬高; 3a 的诊断)。

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

## 3. 注释与标题改写前后对照 (只列句子)

切句与 commentsync 相同 (连续 # 行去前缀连成一行, 在 `.` 与 `;` 之后切)。原句一字不改仍在改后段里的算 "保留", 不另列。由 `t002d/gen-b.py` 从两份套件生成。

### 第 9 处 (test W10 block head (3b); 紧挨 `wpa_rep() {` 的注释段; 保留 5 句)

改写前 (删掉的句子):
- Owner ruling 2026-10-14: beyond a limit the command is BLOCKED -- exit 2 with the "command too large to scan for secrets ...
- split it" text, NOT the finding text -- never passed (the COUNT bounds, 21y, still pass).
- After the flip both sides of a limit exit 2, so the exit code alone no longer tells "judged" from "refused": the text does.
- The inside of every limit asserts the first, the outside the second: a limit that is one too low or too high swaps the text of a side and turns the case red;
- an overrun that passes (the fail-open M6, exit 0) or is blocked with the finding text turns the outside red.
- The numbers are part of the contract (_SGV_SMAX 8192 = one substituted copy, _SGV_VMAX 4096 = one collected value, _SGV_TMAX 65536 = all copies of one command);

改写后 (新句):
- Owner ruling 2026-10-14, narrowed by 10CG/aria-plugin#217 (owner rulings A and E, 2026-10-23): a value over the value limit, or copies over the pass-wide limit, block the command on every platform -- exit 2 with the "command too large to scan for secrets ...
- split it" text, not the finding text -- and are never passed (P9);
- a copy over the copy limit is blocked that way only where the relaxation is not in effect (What 1 and its supplement: another platform or bash version, WSL, a project extension, or no time left;
- P2).
- Where it is in effect the pass is re-run under a hard deadline with the relaxed rules (What 1): a copy that grows by more than _SGV_GMAX over its input is blocked with the growth text (P8, What 5), a copy over _SGV_SMAX whose longest line is longer than _SGV_LMAX is matched against the rows only and a match blocks with the longline text (P7, What 5), and any other copy is judged as usual, so it may pass (R-a).
- The COUNT bounds of the baseline pass, 21y, still pass (P9).
- After the flip both sides of a limit exit 2 wherever a row matches (in the relaxed branch the outside of the copy limit passes when none does, 21ab), so the exit code alone does not tell "judged" from "refused": the text does.
- Every limit is pinned from both sides.
- In the cases that the relaxation does not change, and in the baseline branch of the six groups that it changes (21ab, 21ac, 21ag, 21aj, 21al, 21ao;
- the branch is chosen once, below: wpa_rx6), the inside asserts the first helper and the outside the second, so a limit one too low or too high swaps the text of a side and turns a case red, and an overrun there that passes (exit 0, the fail-open M6) or draws the finding text turns the outside red.
- In the relaxed branch of the six groups wpa_x_hit asserts the ordinary finding text (value-REDACTING filter, and not the longline text), wpa_x_longline the longline text (has a line longer than ...
- Matched pattern:), and wpa_x_toolarge the growth line where a copy grows too much: wpa_x_finding cannot tell the ordinary finding text from the longline text, both say that the command reads a secret-bearing source (PP1-A12).
- The numbers are part of the contract (_SGV_SMAX 8192 = the longest copy the baseline pass builds, _SGV_VMAX 4096 = one collected value, _SGV_TMAX 65536 = all copies of one command;
- in the relaxed rerun _SGV_GMAX 8192 = the most a copy may grow over its input, _SGV_LMAX 8192 = the longest line of a copy over _SGV_SMAX that is still judged with credit);

### 第 10 处 (test 21aa/21ab (3b); 紧挨 `wpa_vx_cmd() {` 的注释段; 保留 1 句)

改写前 (删掉的句子):
- 21aa is judged (the reader is found), 21ab is refused.
- 21ab's second command pins what the limit counts: the WHOLE judged string, not its growth -- a 9000-character segment with a one-character value and one reference is refused as well (so is a big heredoc that happens to hold `x=1` and `$x`): a decision of the owner's ruling, pinned here so that narrowing it is deliberate.
- The third command is made of short words (nothing the echo's redaction would cut away): the size text echoes only the START of the command.
- Red when (21ab): the 8193-character copy or the 9000-character segment passes (exit 0 -- the fail-open M6), is refused with the finding text or by another limit line, or the limit is 8191 / 8193 (21aa and 21ab swap sides);
- the whole command is echoed back.

改写后 (新句):
- 21aa's copy (8192) is not over the copy limit, so it is not a trigger point of the relaxation: it is judged and its reader found on every platform (What 1, P1).
- 21ab's three commands are over it: the 8193-character copy, a 9000-character segment with a one-character value and one reference, and a segment of short words (nothing the echo's redaction would cut away).
- Where the relaxation is not in effect all three are refused as too large, the baseline bytes (P2): the limit counts the whole copy, not its growth, so a tiny value behind one reference is refused too (so is a big heredoc that happens to hold `x=1` and `$x`), and the size text echoes only the START of the command.
- 10CG/aria-plugin#217 narrowed that posture on purpose (owner ruling A): where the relaxation is in effect the copy limit of the rerun is the growth over the input (_SGV_GMAX, P8) and none of the three grows by that much, so each copy is judged in full (What 1, R-a);
- each is one line longer than _SGV_LMAX, so it is matched against the rows only (P7): the first, whose reader matches a row, is blocked with the longline text (What 5), and the other two hold no reader, match no row and pass (R-a).
- Red when (21ab), where the relaxation is not in effect: a command passes (exit 0 -- the fail-open M6), is refused with the finding text or by another limit line, the limit is 8191 / 8193 (21aa and 21ab swap sides), or the size text echoes the whole command;
- where it is in effect: the first command passes, is refused as too large or draws the ordinary finding text, or one of the other two is blocked.

### 第 11 处 (test 21ac/21ad (3b); 紧挨 `wpa_vx_val() {` 的注释段; 保留 4 句)

改写前 (删掉的句子):
- The list of a for statement is the third place a value is collected: 3000 characters are expanded (not 4096: the list stays in the command, so its copy holds the list twice and 2 x 4096 is over the copy limit -- which is how a 4096-character list is refused: by the COPY limit, not by the value limit), 4097 refuses the command by the value limit.
- (21ac): the 4096-character for list is refused by the value limit instead of the copy limit.

改写后 (新句):
- The list of a for statement is the third place a value is collected: 3000 characters are expanded and the read is found on every platform (the list stays in the command, so the copy holds it twice, about 6 KB: inside the copy limit, not a trigger point of the relaxation, P1), and 4097 refuses the command by the value limit on every platform (P9).
- A 4096-character list makes a copy over the copy limit (2 x 4096 and the rest).
- Where the relaxation is not in effect that copy is refused by the COPY limit with the size text, not by the value limit (P2);
- where it is in effect the copy grows by about 4 KB over the input, under _SGV_GMAX, so it is judged in full, and as its one line is longer than _SGV_LMAX the read is blocked with the longline text (P7, What 5).
- The two reads inside the limits draw the ordinary finding text on every platform (P1), which the relaxed branch checks with wpa_x_hit: not the longline text.
- (21ac), where the relaxation is not in effect: the 4096-character for list is refused by the value limit instead of the copy limit;
- where it is in effect: that list passes, is refused as too large or draws the ordinary finding text instead of the longline text, or a read inside the limits draws the longline text.

### 第 12 处 (test 21ag (3b); 紧挨 `wpa_begin_bash_case "W10 SC-21ag` 的注释段; 保留 0 句)

改写前 (删掉的句子):
- Red when (21ag): the 36 KB dense copy passes (exit 0 -- the fail-open M6), or is refused by another limit line.

改写后 (新句):
- 21ag: the dense copy (about 36 KB in one segment) is over the copy limit, and it grows by far more than _SGV_GMAX over its input: it is refused as too large on every platform, only the limit line differs -- the copy limit where the relaxation is not in effect (P2), the growth line of the rerun where it is (P8, What 5: "a command segment grows by more than 8192 characters after variable expansion").
- Red when (21ag): the command passes (exit 0 -- the fail-open M6), or the refusal names a limit line other than its branch's.

### 第 13 处 (test 21aj (3b); 紧挨 `wpa_vx_over() {` 的注释段; 保留 0 句)

改写前 (删掉的句子):
- 21aj: a segment whose copy is over the copy limit ends the pass -- the command is refused at once, and the reader behind it is never judged.
- (The fail-open M6 refused such a segment cheaply but counted it as a whole copy, 8192, against the pass-wide limit: after seven of them the reader was still judged and blocked, after eight it passed.) Red when (21aj): such a segment is skipped or counted instead of refused -- the finding text after seven of them, exit 0 after eight (the fail-open M6).

改写后 (新句):
- 21aj: each heavy segment ` echo $p $p $p` makes a copy of about 12 KB, over the copy limit, that grows by about 12 KB over its own text, over _SGV_GMAX as well: the first of them ends the pass, the command is refused at once and the reader behind it is never judged -- by the copy limit where the relaxation is not in effect (P2), by the growth line of the rerun where it is (P8, What 5).
- (The fail-open M6 refused such a segment cheaply but counted it as a whole copy, 8192, against the pass-wide limit: after seven of them the reader was still judged and blocked, after eight it passed.) Red when (21aj): a heavy segment does not refuse the command -- the finding text after seven of them, exit 0 after eight (the fail-open M6) -- or the refusal names a limit line other than its branch's.

### 第 14 处 (test 21al (3b); 紧挨 `wpa_begin_bash_case "W10 SC-21al` 的注释段; 保留 0 句)

改写前 (删掉的句子):
- Red when (21al): the braced 8193-character whole copy passes (exit 0 -- the fail-open M6), or the edge moves by one (the two commands swap sides).

改写后 (新句):
- Red when (21al): either command passes (exit 0 -- the fail-open M6), the edge moves by one (the two commands swap sides), or the 8193-character copy draws a text other than its branch's: the size text that names the whole-command limit where the relaxation is not in effect, the longline text where it is.

### 第 15 处 (test 21ao (3b); 紧挨 `wpa_begin_bash_case "W10 SC-21ao` 的注释段; 保留 0 句)

改写前 (删掉的句子):
- Red when (21ao): the 8193-character whole copy passes (exit 0 -- the fail-open M6), or the edge moves by one (the two commands swap sides).

改写后 (新句):
- Red when (21ao): either command passes (exit 0 -- the fail-open M6), the edge moves by one (the two commands swap sides), or the 8193-character copy draws a text other than its branch's: the size text that names the whole-command limit where the relaxation is not in effect, the longline text where it is.

### 第 21 处 (test 21al head (3b); 紧挨 `wpa_vx_braced() {` 的注释段; 保留 3 句)

改写前 (删掉的句子):
- 21al: the copy limit holds for the braced form ${NAME} too (it goes through _sg_vx_replace, not through the $NAME loop).

改写后 (新句):
- 21al: the braced form ${NAME} goes through the same copy limit as $NAME (through _sg_vx_replace, not through the $NAME loop).
- echo ${p} ${p}<filler> | cat ${f}` has 53 + 2700 + filler characters and its copy 2 x 2696 + 16 more -- 8161 + filler, so a 31-character filler makes exactly 8192.
- Exactly 8192 is not over the limit: it is judged, with the ordinary finding text, on every platform (P1).
- 8193 is refused as too large where the relaxation is not in effect (P2);
- where it is in effect the whole copy grows by about 5.4 KB over the input, under _SGV_GMAX, so it is judged in full, and as its one line is longer than _SGV_LMAX its read is blocked with the longline text (P7, What 5).

### 第 22 处 (test 21ao head (3b); 紧挨 `wpa_vx_whole() {` 的注释段; 保留 0 句)

改写前 (删掉的句子):
- 21ao: whole-command mode (the command degrades because of a `(`) obeys the same copy limit -- the unit is the whole command: 6069 + filler, so a 2123-character filler makes 8192

改写后 (新句):
- 21ao: whole-command mode (the command degrades because of a `(`) meets the same copy limit -- the unit is the whole command: 6069 + filler, so a 2123-character filler makes 8192.
- Exactly 8192 is not over the limit: it is judged, with the ordinary finding text, on every platform (P1).
- 8193 is refused as too large where the relaxation is not in effect (P2);
- where it is in effect the whole copy grows by about 4 KB over the input, under _SGV_GMAX, so it is judged in full, and as its one line is longer than _SGV_LMAX its read is blocked with the longline text (P7, What 5).

### 第 16-20 处 (用例标题, 整句)

- 第 16 处 21ab 改写前: W10 SC-21ab bf: copy limit exceeded is refused — 8193 characters: the copy is not judged, the command is blocked as too large (no padding passes)
  - 改写后: W10 SC-21ab bf: copy limit exceeded — 8193 characters, or a 9000-character segment with a one-character value: refused as too large where the relaxation is not in effect; where it is, each copy is judged in full: the reader is blocked with the longline text, the two commands with no reader pass
- 第 17 处 21ag 改写前: W10 SC-21ag bf: the dense shape of the review (15 assignments of 300 B, 8 references each: a 36 KB copy; 16 x 300 B x 8 took 5.4 s) is over the copy limit and refused as too large
  - 改写后: W10 SC-21ag bf: the dense shape of the review (15 assignments of 300 B, 8 references each: a 36 KB copy; 16 x 300 B x 8 took 5.4 s) is refused as too large on every platform — by the copy limit where the relaxation is not in effect, by the growth limit where it is
- 第 18 处 21aj 改写前: W10 SC-21aj bf: a segment over the copy limit ends the pass — with one, seven or eight of them in front of the reader the command is refused as too large and the reader is never judged
  - 改写后: W10 SC-21aj bf: a segment over the copy limit that also grows over the growth limit ends the pass — with one, seven or eight of them in front of the reader the command is refused as too large (the copy limit, or the growth limit where the relaxation is in effect) and the reader is never judged
- 第 19 处 21al 改写前: W10 SC-21al bf: the copy limit holds for the braced form too — a substituted whole command of exactly 8192 characters is judged and blocked, 8193 is refused as too large
  - 改写后: W10 SC-21al bf: the braced form meets the same copy limit — a substituted whole command of exactly 8192 characters is judged and blocked; 8193 is refused as too large where the relaxation is not in effect and blocked with the longline text where it is
- 第 20 处 21ao 改写前: W10 SC-21ao bf: whole-command mode obeys the copy limit — a whole copy of exactly 8192 characters is judged and blocked, 8193 is refused as too large
  - 改写后: W10 SC-21ao bf: whole-command mode meets the same copy limit — a whole copy of exactly 8192 characters is judged and blocked; 8193 is refused as too large where the relaxation is not in effect and blocked with the longline text where it is

## 4. 各轮结果与首尾负载

每轮在 worktree 里跑 `taskset -c 0,1 nice -n 19 bash hooks/tests/secret-guard.test.sh` (PATH 上的 bash = /usr/bin/bash 5.2.15), 开跑前等一分钟负载 <= 1.2; 输出 `t002d/<轮>.out`、`<轮>.w10log`、`<轮>.meta`。
"整轮负载" 是驱动在开跑前与结束后读的 /proc/loadavg; "计时批负载" 是套件在 W10 批首尾读的 (INV-7 判据, 门槛 2)。

| 轮 | SC_BASH / 环境 | 整轮开跑 → 结束负载 | PASS / FAIL / SKIP / 总数 | SKIP 原因 | 放宽预期 | 计时批: 开始 → 结束负载, 结论 | 移植编号数 | 6 组 | SC-13 |
|---|---|---|---|---|---|---|---|---|---|
| b-usr | /usr/bin/bash (x86_64-pc-linux-gnu 5.2) | 0.80 0.89 1.12 → 2.56 1.85 1.46 (rc 0) | 961 / 0 / 0 / 961 | platform 0, load 0, void 0, inconclusive 0, root 0, other 0 | yes | 0.80 0.89 1.12 → 1.39 1.00 1.14, judged | 136 | relaxed branch | 绿 |
| b-5.0.18 | /home/dev/.aria/tools/bash-5.0.18/bash (x86_64-pc-linux-gnu 5.0) | 1.08 1.58 1.42 → 2.58 2.16 1.72 (rc 0) | 961 / 0 / 0 / 961 | platform 0, load 0, void 0, inconclusive 0, root 0, other 0 | yes | 1.08 1.58 1.42 → 1.22 1.54 1.41, judged | 136 | relaxed branch | 绿 |
|  | 开跑前等待读数: wait t=0s load=2.56 |
| b-5.1.16 | /home/dev/.aria/tools/bash-5.1.16/bash (x86_64-pc-linux-gnu 5.1) | 1.19 1.80 1.64 → 2.21 2.21 1.89 (rc 0) | 961 / 0 / 0 / 961 | platform 0, load 0, void 0, inconclusive 0, root 0, other 0 | yes | 1.19 1.80 1.64 → 1.26 1.72 1.62, judged | 136 | relaxed branch | 绿 |
|  | 开跑前等待读数: wait t=0s load=2.58 |
| b-5.3.20 | /home/dev/.aria/tools/bash-5.3.20/bash (x86_64-pc-linux-gnu 5.3) | 1.08 1.89 1.80 → 4.13 2.52 2.05 (rc 0) | 961 / 0 / 0 / 961 | platform 0, load 0, void 0, inconclusive 0, root 0, other 0 | yes | 1.08 1.89 1.80 → 1.11 1.78 1.77, judged | 136 | relaxed branch | 绿 |
|  | 开跑前等待读数: wait t=0s load=2.21 |
| b-3.2.57 | /home/dev/.aria/tools/bash-3.2.57/bash (x86_64-unknown-linux-gnu 3.2) | 1.02 1.94 1.90 → 2.29 2.34 2.11 (rc 1) | 902 / 1 / 58 / 961 | platform 58, load 0, void 0, inconclusive 0, root 0, other 0 | no | 1.02 1.93 1.90 → 2.04 2.08 1.95, void (SKIP [void]): run again | 136 | relaxed branch | 绿 |
|  | 开跑前等待读数: wait t=0s load=4.13 |
| b-3.2.57-r2 | /home/dev/.aria/tools/bash-3.2.57/bash (x86_64-unknown-linux-gnu 3.2) | 1.19 1.66 1.84 → 3.68 2.86 2.31 (rc 0) | 903 / 0 / 58 / 961 | platform 58, load 0, void 0, inconclusive 0, root 0, other 0 | no | 1.19 1.66 1.84 → 1.68 1.73 1.86, judged | 136 | relaxed branch | 绿 |
|  | 开跑前等待读数: wait t=0s load=1.47; wait t=300s load=1.82 |
| wsl | /usr/bin/bash (x86_64-pc-linux-gnu 5.2) + WSL_DISTRO_NAME=Ubuntu | 1.08 1.97 2.00 → 2.57 2.15 2.05 (rc 0) | 961 / 0 / 0 / 961 | platform 0, load 0, void 0, inconclusive 0, root 0, other 0 | yes | 1.08 1.97 2.00 → 1.35 1.90 1.97, judged | 136 | baseline branch | 绿 |
|  | 开跑前等待读数: wait t=0s load=2.29 |

FAIL 行: 
- b-3.2.57: FAIL [W10 SC-21ab bf: copy limit exceeded — 8193 characters, or a 9000-character segment with a one-character value: refused as too large where the relaxation is not in effect; where it is, each copy 

Summary 新行 (b-usr 与 wsl 两轮原文):
- `W10 older groups 21ab 21ac 21ag 21aj 21al 21ao: relaxed branch (new outcomes) | bash on PATH /usr/bin/bash 5.2.15(1)-release (machtype x86_64-pc-linux-gnu) | osrelease 6.17.9-1-pve | WSLInterop no | WSL_DISTRO_NAME '' WSL_INTEROP ''`
- `W10 older groups 21ab 21ac 21ag 21aj 21al 21ao: baseline branch (assertions as before) | bash on PATH /usr/bin/bash 5.2.15(1)-release (machtype x86_64-pc-linux-gnu) | osrelease 6.17.9-1-pve | WSLInterop no | WSL_DISTRO_NAME 'Ubuntu' WSL_INTEROP ''`

3.2.57 第一轮 (`b-3.2.57`) 的计时批结束读数 2.04 >= 2, 按 INV-7 作废重跑; 同一轮还有 21ab 的 1 项 FAIL (见第 6 节第 1 条)。重跑 `b-3.2.57-r2` 判过、FAIL 0, 作为 3.2.57 的验收轮。五个 bash 的验收轮 (b-usr、b-5.0.18、b-5.1.16、b-5.3.20、b-3.2.57-r2) 总数都是 961, SC-13 都绿; SKIP 只在 3.2.57 上, 58 个全是 [platform]。WSL 轮 6 组走基线支, 移植编号数与五轮相同。

## 5. commentsync 各模式与构造

`SUITE_TEXT` 的生成: 第 9-15、21、22 处各用 `('next', <紧跟注释段的代码行前缀>)` 定位 (基线与改后两份套件里都是同一行); 把基线段与改后段都按 `.` 与 `;` 之后切句, 只在基线段里的句子列为旧句, 只在改后段里的列为新句, 原样保留的句子两边都不列 (第 9 处保留 5 句、第 10 处 1 句、第 11 处 4 句、第 21 处 3 句)。检查: 旧句 baseline 模式在原段里至少 1 次、target 模式全部注释里 0 次; 新句 target 模式在该处自己的段里至少 1 次、baseline 模式全部注释里 0 次。各处数目: 9 (旧 6 / 新 14)、10 (5 / 7)、11 (2 / 7)、12 (1 / 2)、13 (2 / 2)、14 (1 / 1)、15 (1 / 1)、21 (1 / 5)、22 (1 / 4)。

| 运行 | 结果 |
|---|---|
| target: worktree hook + worktree 套件 | GREEN (194 项 ok), `t002d/cs-target.txt` |
| baseline: 59e333c 的 hook + 59e333c 的套件 | GREEN (184 项 ok), `t002d/cs-baseline.txt` |
| 构造 1: worktree 套件副本, 第 13 处新句 "grows by about 12 KB" 改一个字符为 13 | RED (1): 第 13 处 new 句 n=0, `t002d/cons/c1-onechar.txt` |
| 构造 2: worktree 套件副本, 删掉第 10 处整块改写后的注释 (11 行) | RED (8): 定位不到注释段 1 项 + 第 10 处新句 7 项, `t002d/cons/c2-delblock.txt` |
| 构造 3: 59e333c 的套件跑 target 模式 | RED (89): anchor 10、block 9、title 5、add 2、old 20、new 43, `t002d/cons/c3-base-suite-target.txt` |

构造只在 `t002d/cons/` 的副本上做, worktree 未动。

## 6. 未做、拿不准、与规格字面不同的项

1. **【需主控裁定】放宽支的新结局依赖放宽重跑在截止前跑完, 6 组没有负载门。** 放宽支断言的 longline、增长文案、放行 (21ab 的 b、c), 都要求作业在 `_SG_P0` + min(预算, 3) s 内结束; 主机过慢时 hook 按规格回落基线的尺寸文案, 这时 6 组记 FAIL (21ab 的 b、c 会是 exit 2 而不是 0)。INV-7 把套件里 "重跑须在截止前跑完" 类用例列为计时类 (负载 ≥ 2 整批 SKIP), 移植用例里同类情形按 3a 裁定 (2) 走计时口径; 而任务书与 design (iv) 对 6 组的写法是每组一个普通用例、计 PASS / FAIL。两种读法: (A) 6 组是结局断言, 照任务书不加门; (B) 它们隐含 "重跑须在截止前跑完", 按 INV-7 负载 ≥ 2 时应 SKIP。我照 (A) 落地, 没有自行加门。现有证据: 各轮里旧用例段的负载 (见第 4 节, 结束读数) 下 6 组全部 PASS; W9-suite.txt (负载 3.59、原型) 里 21ab 只列 3 项, 与改前现状轮的 11 项不同, 可能就是 (b)(c) 那一轮回落到了基线文案 (未核实)。
   **本段实测到了这一风险。** 3.2.57 第一轮 (整轮开跑负载 1.02, 结束 2.29) 唯一的 FAIL 是 21ab: (c) `f=x; echo $f a a …` 得 exit 2, 想要 0 (1 项不符)。随后直接计时 (负载约 1.5; taskset 0,1、nice 19; 与 wpa_err 相同地清掉 CLAUDE_PROJECT_DIR 等三个变量、HOME 指向私有目录): (b) 三次 2.49 / 2.54 / 2.55 s, (c) 三次 2.51 / 2.54 / 2.78 s, 都放行, 离 3 s 截止 (min(预算, 3)) 只差 0.2-0.5 s。第二轮 (开跑 1.19, 结束 3.68) 6 组全部 PASS。所以 21ab 的 (b)(c) 放行断言在本机负载 2 上下就会翻转, 读法 (B) 的理由更强。若选 (B), 旧用例需要一个与移植用例 [load] 同口径的 SKIP 出口 (计数不变, 仍是每组一个用例); 其余 4 组的放宽支 (longline、增长文案) 同样依赖重跑跑完, 我没有单独计时。计时材料在 `t002d/m21ab/`。
2. **判据的输入只取平台规则与 WSL 环境变量。** 扩展条件: 6 组都不在项目里, 恒成立 (第 2 节)。时间条件无法预判, 不入判据 (同第 1 条)。
3. **`SGW_RELAX` 那一行改成调用 `sg_w10_relax_rule`。** 规则字面等价 (空的 MAJ / MIN 两边都按 0 处理, 结论都是不放宽); 3c 与 v31/sc-cases.sh 对照时请知悉。这一改动是为了让 6 组与移植用例在结构上用同一条规则。
4. **Coverage 的 967 是推算。** 本机无 zsh; git 检出里五个 `SC_BASH` 各一轮实跑都是 961 (第 4 节); 有 zsh 时多跑 `:1097` 条件组里的 6 个 `zsh_case` (`:1105-:1110`), 所以 961 + 6 = 967, 与 3a 的推法 (旧值 831 + 移植 136) 一致。头注释两个数因此不变。
5. **WSL 一轮只导出了 `WSL_DISTRO_NAME`。** `WSL_INTEROP` 与 `WSLInterop` 文件两个输入没有单独实跑 (同一条判据; WSLInterop 文件无 root 造不出)。
6. **ps 的 "两条"**: 已核 V5-S13b 的 SKIP [platform] 分支 (`lib:238`); 另一条 (V5-S12-no-leftovers, `lib:313`) 只看到它用 `lv5`, 其 SKIP 分支未逐行核对。
7. 不在本段 (3c): 关门臂的基线参照核对、run-suite.sh 与垫片头注释、run-mutants.sh 的套件模式、全部坏实现与扰动、两种环境错误、基线红集在套件上复跑。


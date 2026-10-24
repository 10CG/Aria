
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

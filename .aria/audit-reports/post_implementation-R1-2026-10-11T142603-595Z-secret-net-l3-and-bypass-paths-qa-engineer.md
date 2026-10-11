---
checkpoint: post_implementation
mode: adversarial_single_round
rounds: 1
converged: true
oscillation: false
overridden_by_user: true
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-11T14:26:03.595Z
context: openspec/changes/secret-net-l3-and-bypass-paths/
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---

## 已实读文件

被审对象(`git archive` 取出的参考树;6 个 sha256 前 16 位逐一核对,与派单一致):
- `aria/hooks/secret-guard.sh` 1–1437(全文);`aria/hooks/secret-scan.sh` 1–577(全文);`aria/hooks/hooks.json` 1–88(全文)及其 diff。
- `aria/hooks/tests/secret-guard.test.sh` 1–60、1270–1295、2085–2140、2301–2312、2725–2770,另 grep 定位 563–604、1697–1940;`git diff -U0` 里被删 / 改的基线行(4 行)。
- `aria/hooks/tests/secret-scan.test.sh` 1–33,另 grep 定位 249–300;被删 / 改的基线行(30 行夹具,W7 拼装后仍在:`expect_detect` 28、`expect_pass` 12,与基线相同)。
- `aria/hooks/tests/jq-crlf-guard.sh` 1–60、`crlf-shim.test.sh` 1–61;`aria/README.md`、`README.zh.md`、`VERSION` 的改动 hunk;`standards/conventions/secret-hygiene.md` 全部改动 hunk。
- `proposal.md` 第 383 行、SC-4…12 / 16…25 / 28…35 行(272–312)、W10 184–199、W11 198–204、W14 235–252、Impact 性能 355、待复议 410;`detailed-tasks.yaml` 185–235。
- `baseline_probe.py` 1–152、440–500、636–652、1490–1511、1700–1722、1914–1925、1995–2100、2355–2364、2445–2490、2700–2882(其余 grep 定位)。
- `PROGRESS.md` 222–232;决策单 20–24、37–41;`writer-v6-proto/timing.py` 1–140(仅作测量工具)。
- `mut_summary_v6.txt` 1–40、36–224(节与 `==` 行)、374–400 及名称统计,**矩阵跑完后**才读。

## 坏实现矩阵

### 枚举集合与上界清单(file:line 以 `69af7cd` 为准)

L3 `secret-scan.sh`:

| 集合 | 位置 | 成员数 |
|---|---|---|
| json-credential-field 键名表 | :290 | 58 |
| json-env-secret-key / kv-secret-assign 关键字 | :292 / :294 | 10 / 10 |
| cli-secret-flag 后缀 | :300 | 7 |
| auth scheme 词、两个头名的逐字母大小写类、值字符类符号 | :296、:298、:294-300 | 2、13+20、7+7+6+6 |
| 白名单标记词 / 掩码 / 定界形 / 省略号 | :360 / :356 / :352-355 / :367 | 6 / 3 / 4 / 1 |
| 熵类 / 路径起头 / CLASSIFIED_TAGS / NEW_TAGS | :372-374 / :377 / :313 / :314 | 3 / 4 / 7 / 6 |
| `_value_of` 分支 | :337-350 | 9 |

L1 `secret-guard.sh`:

| 集合 | 位置 | 成员数 |
|---|---|---|
| 打印型读取器 | :435 | 29 |
| launcher / 关键字 / 命令位置字符 | :441、:1259 | 15 / 4 / 8 |
| 外壳包裹、包裹引导类 | :442、:1260 | 9 组、5 |
| `/proc` 基线组 / 加宽组 | :1253 | 13 / 24 |
| pid 记号 | :447 | 8 |
| W10 声明前缀 | :589 | 5 |
| os.environ 子串 | :1371-1374 | 4 |
| jq 元数据词 | :493 | 4 |
| Read/Edit 路径正则备选 | :942 | 34 |
| `_SG_SRVCFG` 备选 / 解释器源组名 | :433 / :1211-1212 | 3 / 2×9 |
| ps 备选与 pgrep / pstree / top / docker 部分 | :441、:1259、:1261 | 逐项 |
| claude-config 名 | :406 | 3 |
| W8 行左右边界类 | :1132 | 4 + 3 |

上界与下界:

| 界 | 位置 |
|---|---|
| 前 200 个 span(`head -n 200`、`count > 200`) | scan.sh:491-492 |
| 指纹项 10(`FP_N >= 10` 两处;PEM 循环 `FP_N < 10`) | :389、:394、:443 |
| 指纹哈希门槛 16 | :396 |
| 六个新 tag 值长 `{16,}` | :290-300 |
| kv 键前后缀 `{0,64}`;cli 旗标前缀 `{0,40}` | :294;:300 |
| 熵 `n>=2` | :375 |
| 路径形至少 2 个 `/` | :384 |
| W10 赋值 16、`for` 8、`${}` 替换 8、引用 8 | guard.sh:590、:605、:579、:630 |
| W9 条目 4..200 字节、条目数 200、文件 32768 字节、出现点 64 | :688、:692、:685、:705 |

### 总表(类别照第 383 行原词)

「预期」是 Spec「怎么会红」点名的行;「实际」是我的坏实现转红的行。「整组」指把该 SC 的全部行都跑一遍。

| 类别 | 坏实现(file:line,怎么改) | 预期转红 | 实际转红 | 抓住? |
|---|---|---|---|---|
| 白名单写成单字符前缀 / 含 / 大小写不敏感 | A01–A06(scan.sh:359-365、:313):尖括号形 → `=="<"*`;`${}` 形 → `=='$'*`;`{{}}` 形 → `=="{"*`;标记词两侧加 `*`;`nocasematch`;白名单套到 env-line | 7h 7j 11z | A01 11z 7h 7j;A02 11z 7h 7i 7j;A03 11x 7j;A04 7h 7j;A05 7h;A06 7h | 6/6 是 |
| 熵下限写成必须含数字 | A07 :375 `(( n >= 2 ))` → 含数字 | 4o 4t | 4o 4t | 是 |
| 路径形写宽 | A08 `/` 开头即路径(:381-384);A09 字符类含 `+=`(:378) | 4n 5l | A08 4n 5l 9w 9y;A09 4n 5l | 是 |
| 路径形写宽 | **A10** 只要 1 个 `/`(:384 `*/*/*` → `*/*`) | 4n 5l | 无(SC-4/5/7/9/10/11 整组 + scan 套件 S3 全绿) | **否 → M4** |
| tight 漏并入 | A11 / A12 / A13(guard.sh:472)分别去掉 app.ini 名字组 / 进程表族 / claude-config | 16r / 22bm / 16p | 同 | 3/3 是 |
| 扩展条目拼成正则 | A14 Bash 面 `grep -oEib`(:702) | 19j 20h | 19j 20h | 是 |
| 扩展条目拼成正则 | **A15** Read/Edit 面 `grep -qEi`(:727);**A16** Read/Edit 面无引号 `case "$lp" in *$e*)` 循环 | 19j 20h | 无(SC-19/20 整组 + guard 套件 S2 / S5 全绿) | **否 → M8** |
| 扩展代码裸调用 | A17 Bash 面(:1410)、A18 Read/Edit 面(:952)改成主 shell 里裸调用 | 20i 20j 20k | 20i 20j | 是 |
| 扩展先于内建 | A19 `_sg_per_segment_eval` 先 ext 后 core(:1400) | 20l | 20l(+ timing h2 FAIL) | 是 |
| 第二遍按段交错 | G20b 每段后调 `_sg_vx_pass`(:781-785) | 21v | 21v(timing h1 141×) | 是 |
| 第二遍按段交错 | A20 每段后内联 collect / apply,不经 `_sg_vx_pass` | 21v | 探针 / 套件全绿;仅 timing h2 FAIL 5.75× | 仅 timing(m2) |
| W12 给 `\.env` 加右边界 | A21 python3 / node 两行(:1211-1212);A22 另含 lua(:1302) | 23c 23d 23h | 23c 23d 23h | 是 |
| `/proc` 连 status 一起放宽 | A23(:1253 加宽组加 status) | 22as | 22as | 是 |
| jq 新词进宽松词表 | A24(+`keys_unsorted`、`map_values(length)`)、A25(+`keys_unsorted`)(:493);A26 锚定形去闭合引号(:499) | 24f | 24f(A26 另 24a–e) | 是 |
| bash 4+ 构造 | H01–H16(guard.sh)、H21–H24(scan.sh),共 20 个:`mapfile -d`(#154 回退)、`${x,,}`、`[[ -v ]]`、`declare -A`、nameref、负下标、`${x@Q}`、`\|&`、`&>>`、`;;&`、coproc、globstar / lastpipe、`wait -n`、`${x^^}`、readarray | 32a(32c) | 20/20 红:19 个 32a;H01–03 H06–12 H16 H22 另被 32c / 32d 抓;H23(`${1,,}`)只被 32c / 32d 抓 | 是 |
| 执行了命令文本、条目或被扫描内容的 eval 式实现 | B01 `_sg_vx_collect` 对值 eval(:596) | 21z | 21z | 是 |
| 同上 | B02 `_sg_ext_entries` 对条目 eval(:695);G03b `_sg_ext_subst` 无条件 eval 命令文本(:700) | 19ab | B02 19ab 19j;G03b 19a 19ab 19b 19j | 是 |
| 同上 | G04b `_sg_judge_one` 对命令文本 `eval printf %s $subj`(:1370) | 23i | 23c 23i | 是 |
| 同上 | B05 / B09 `_value_of` JSON 分支 eval(:338) | 7n | 7n | 是 |
| 同上 | B03 `_sg_ext_pass` 命中后 `eval printf %s "$sub"`(:718) | 19ab | 19aa 19af 19ag 19o 19u 19z(eval 弄坏引号的副作用),不含 19ab | 间接 |
| 同上 | **I03d** 命中后 `eval ": \"$sub\""`(只执行,文本不变) | 19ab | 无(整组 + guard 套件 S5 全绿);直接复现:金丝雀被建出 | **否 → M5** |
| 同上 | **B08** `_value_of` URL 分支 eval(:345) | 7n | 无(SC-7/12 整组 + scan 套件 S3 全绿);直接复现:金丝雀被建出 | **否 → M5** |
| 同上 | B06 / B07 kv、头分支 eval | 7n | 无 | 不适用:值字符类不含元字符,不可利用 |
| 扩展另写阶段切分(含完全不切) | B10 整串不切(:719);B11 sed 粗切 `; && \|\|`;B12 手写引号感知切分 | 19aa 19af | B10 19aa 19af;B11 19aa 19af 19z;B12 19af | 是 |
| 偏移与切片单位不一致 | B15 `grep -b` 字节偏移 + 字符切片(:700-702) | 19ag | 19ag | 是 |
| 字节语义依赖调用方导出 `LC_ALL` | B16 三处 `local -x` → `local`;B18 仅 path_pass | 19ah 19am | B16 19ah 19am;B18 19am | 是 |
| 同上 | B17 仅 `_sg_ext_entries` | — | 无 | 等价:调用方 `_sg_ext_subst` / `_sg_ext_path_pass` 已导出,经 `<( )` 继承 |
| 有效条目为零时把空模式交给 grep | B20 去 `[[ -n "$out" ]] \|\| return 0`(:689) | 20o–q | 20o 20p 20q | 是 |
| 字符类用 glob 范围 | B25 熵三类全改范围;B26 只改小写类(:372-374) | 32d | B25 32d(9p 10a 10k);B26 32d(10k) | 是 |
| 按字符判后缀 | B28 `${v: -1}`;B29 `${v:${#v}-1}`(:367) | 32e | 32e(11v 11x 11y) | 是 |
| 分类器步骤套到不该套的既有 tag | B30–B34:env-line 进 CLASSIFIED+NEW;白名单套全部 tag;熵 / 路径 / 点链也套全部;json-secret-field 进 NEW;熵套全部已分类 tag(:313-314、:481-484) | 7l 7m 7h | B30 7h 7l;B31 7h 7m;B32 7h 7l 7m;B33 7h 7l;B34 7h | 5/5 是 |
| tight 拷贝与规则行漂移 | B4a–o 去 15 个 launcher 之一(:441);B5 去 ps 备选 7、pgrep / pstree / top、绝对路径、包裹 9、docker 3、整段 3,共 22 个 | 22bm | 全 22bm | 37/37 是 |
| tight 拷贝与规则行漂移 | **B5kw / F1 / F2 / F3**:去掉命令位置字符 `; & ( ) {` 反引号 cntrl(7)、关键字 then / do / else / elif(5,含整组)、launcher 时长后缀 m / h / d(3)(:441) | 22bm | 无;直接复现:`{ true; ps aux \| grep -v x; }` 等被放行;guard 套件 S1 全绿 | **否 → M2**(14 个有行为差异) |
| 包裹下的转储并入 tight | B60 `_SG_PS_REMOTE_T` 换成规则行(:442) | 22br 22bs | 22br 22bs | 是 |
| 对输入做的变换使既有检出变静默或使计数翻倍 | B70 NUL 视图替换基线视图;B71 无条件追加;B72 预检后不比较;B73 NUL→空格;B74 无第二视图;B75 基线视图改 NUL→换行(scan.sh:187-197) | 1e 1f / 1g 2a–d / 1g / 1c 1d / 1c 1d / 1e 1f | 同(B71 另 2e 2f) | 6/6 是 |
| 无界前缀与平方级取值 | C7:kv 去引号 `${V#["']}`;JSON `${span#*:}`;kv `${span#*[=:]}`;`${span#*=}`;URL `#*://`、`#*:`、`%%@*`;cli 旗标前缀 `*`;cli 去左边界;kv 键前缀 `*`;kv 去左边界 | 34a 34b(9z 10n 10o) | 9/9 红 | 是 |
| 同上 | `${span##* }`、cf 头 `${span#*:}`、kv 后缀 `*` | — | 无;timing (i3) 实测不慢 | 等价 |
| 对每个出现点各判一遍 | H41 每个出现点一份替换副本逐个 `_sg_core_eval`(:715);H42 每个出现点重算阶段(:707) | 34c | 34c;timing fh-b 29.4× / 28.7× FAIL | 是 |
| 内容形态 | 同上两类 + H31–H34:去掉新增 jq 取值点的 CR 剥离或 `crlf-ok` | 29g | `jq-crlf-guard.sh` 静态检查报未防 CR | 4/4 是 |
| 内容形态((i) 档) | H52 去 `head -n 200` 与溢出算术 | 11w | 11w | 是 |
| 内容形态((i) 档) | H51 只去 `head -n 200` | 11w | 11w 绿;timing i1 5.11× / i2 10.46× FAIL | 仅 timing |
| W11 命令位置字符集缺成员 | C1×9:规则行 :1259 去 `; & \| ( ) {` 反引号 cntrl `^` 之一 | 22bt | 9/9 红 | 是 |
| W11 簇内字母只认首位 | C2:pgrep / pstree / ps `-F` / top;I02:ps `-O` / `-x` / `-u` / `-o` | 22bu | 22bu 22av 22bm(top 经整组 22bl) | 是 |
| W11 列表关键字只认末位 | C3 两个 | 22bv | 22bv | 是 |
| W11 操作数只认首个 | C4:pgrep / pstree / ps `-F` / docker ps / 时长后缀 | 22bu | 22bu(top 经 22bl) | 是 |
| W11 操作数只认首个 | **C4psO**(ps `-O`)、**I04psu**(末位 `-u`) | 22bu | 无(整组 SC-22 全绿);`ps -p 1 -O rss`、`ps -p 1 -u`、`ps -C nginx -u` 被放行 | **否 → M2** |
| 失败事件(35a–d) | C5a–j:不读 `error` / 不注册 / 事件名写死 ×2 / 只凭子串 / 失败路径漏分类器 / matcher 收窄 / 多一个 hook / 超时 5→3 / 注册成 guard | 35a–d(35e) | 全部红 | 10/10 是 |
| 判定函数留在 source 闸门之下(30b) | C6core_eval、C6vx_pass | 30b | 30b | 是 |
| 同上 | **C6emit_blocked、C6vx_collect、C6vx_apply、C6vx_replace、C6ext_pass、C6ext_subst、C6ext_entries、C6ext_root、C6vars** | 30b | 无;组合 S4(8 个函数同时下移,带 git 历史副本):`PASS: 783 / 783` | **否 → M1**(9 个) |

#### 枚举集合「删掉任一成员」

| 集合 | 坏实现数 | 结果 |
|---|---|---|
| json-credential-field 58 名 | 8 个动态 + 静态证明 | 6 红;2 等价(`password` / `secret` 被既有 tag 先消费);探针 4p 的 NAMES 与 hook 表逐字相同 |
| 关键字 10 / 10、cli 后缀 7、scheme 词 2、值字符类 26 | 55 | 55/55 红 |
| 标记词 6、掩码 3、定界形 6、熵类 3、路径起头 4 | 22 | 22/22 红 |
| CLASSIFIED / NEW 成员 | 13 | 9 红,4 全绿(json-env-secret-key、cf-access-client-secret)→ M7 |
| `_value_of` 分支 | 9 | 8 红;PEM 分支是死代码,等价 |
| 读取器 29;launcher 15;关键字 4;包裹 9;pid 记号 8;os.environ 4;路径正则 34 | 99 | 99/99 红 |
| `/proc` 基线组 13 | 13 | 13/13 红(22aj 22bc) |
| `/proc` 加宽组 24 | 24 | 11 个新读取器红,`cat` 经 22be 22bp 红,**12 个基线读取器全绿** → M3 |
| ps 备选 / docker / 包裹 dump 备选 | 15 | 15/15 红 |
| claude-config 名 3 | 3 | 2 红;`settings.local.json` 由 guard 套件 `#179 SC-1 变体` 抓 |
| W8 行左右边界类 | 8 | 4 红;`_` `.` `-` 左边界成员 3 个全绿 → M7 |
| 引导类 5 | 5 | 3 红;2 等价(`(` 与反引号被命令位置字符冗余覆盖) |
| 头名逐字母类 66 | 66 | auth 26/26 红;cf 25 红,15 个全绿 = 等价(全大写 cf 写法被 kv-secret-assign 先消费) |
| W10 声明前缀 5 | 5 | 5/5 绿 = 等价(Spec W10 明写前缀词多余) |
| jq 元数据词 4 | 4 | 2 红;`paths` `leaf_paths` 全绿 → M7 |
| 解释器源组名 14 | 14 | 12 红;`/v1/var/` ×2 等价(Spec 16o 已注) |

#### 上界差一

| 界 | 结果 |
|---|---|
| W9 条目长度 4..200、条目数 200、文件 32768、出现点 64 | 11/11 红 |
| W10 赋值 16、引用 8 | 4/4 红 |
| W10 `for` 帽 8、`${}` 替换帽 8 | **4/4 全绿** |
| L3 值长 `{16,}`×6、指纹门槛 16、`FP_N>=10`、熵 `n>=2` | 全红 |
| PEM 指纹循环 `FP_N<10` | **2/2 全绿** |
| span 帽 200(`head -n 200`)±1 | **2/2 全绿** |
| span 帽与 `count - 200` 常量不一致 | 1 红;E02x1 等价,E02x2 全绿 |
| kv 键 `{0,64}`(前缀、后缀各 ±1) | **4/4 全绿** |
| cli 旗标 `{0,40}` ±1 | **2/2 全绿** |
| 路径形斜杠数:A10(1 个)、E08p(3 个) | **2/2 全绿** |
| 基线遗留界 1 MB、64 KB(E09m、E15p) | 无点名行,未判 |

### 汇总

667 个独立坏实现:
- 511 个在点名行转红,32 个只在点名行之外的行转红,4 个只由命令行静态检查抓(H31–H34)。
- 120 个全绿:70 个是真验收缺口(归并为 M1–M8),50 个是等价、不忠实、仅 timing.py 可抓,或整组 / 套件复跑后被抓。
- 对不忠实的变体按「先再试 1–2 个变体」处理:`M2unq` → `N2unq`(19ao 红)、`M3unset` → `N3unset`(19ap 红)、`B04` → `G04b`(23i 红)、`G03c` / `B03` → `I03d`(仍全绿,有效)。
- 第 383 行点名的每一类都至少有一个坏实现让对应探针行或套件用例转红。

### 未覆盖

- SC-29 的 `crlf-shim.test.sh`、`jq-crlf-guard.test.sh` 本身:它们是 shim / 静态检查脚本的自测,本次 diff 未动,hook 的坏实现够不着,以 29g 的 4 个坏实现代替。
- 时档 (f)(f0)(g)(gmax)(h)(fhit)(i)(i3):只对列出的坏实现用 `timing.py --judge` 跑,不是逐个坏实现都跑。
- 31d(其他注册项被动):未单独构造,判据是 hooks 对象去掉 `PostToolUseFailure` 后的 sha256,任何改动必红;且 `WPA_ONLY` 含 SC-31 会拉起整套件 + census(约 4 分钟),不适合子集。
- 29h / 29i 对坏实现:只在参考树各跑一次,不逐个坏实现跑。
- 32c 差分:只对 bash 4+ 的 20 个坏实现用小子集跑。
- D01 的 58 个键名:动态只跑 8 个。
- 20i–20k 的 `return 1` / 未绑定变量注入对每个 `_sg_ext_*` 逐个:以 A17 / A18 代表,未逐函数。
- macOS / BSD 工具链(`grep -b`、`sed` 字节类、`localedef`):本机 Linux,未验证。
- 探针全量与 `WPA_REQUIRE_ALL`:派单禁止,留给 TASK-010。

## 与起草期汇总对照

只列结论不同的类别。起草期该轮 95 个变异 + 此前各轮 601 个回归。

- **复现一致:**
  - 起草期点名的转红行我都复现了,覆盖第 383 行的二十六类;
  - 它记录的 5 个「不转红」的等价变异(8 个小写重叠键名、5 个声明前缀、`/v1/var/` 重复、`ext_perentry` 属时档类)我也复现为等价或仅 timing 可抓。
- **30b:** 起草期只有 `core_below_gate` 一个变异(转红)。我把其余 9 个辅助函数 / 初始化下移,全绿。
  - 原因:30b 只断言 rc 0 / 2,`_sg_ext_*` 只在 `$( … )` 里被调用,缺失是静默的;`_sg_emit_blocked`、`_sg_vx_collect` 的返回值被忽略。
- **`/proc` 加宽组:** 起草期 `drop_procreader_*` 对应的是单组读取器设计,被 22bc / 22aj 抓住。
  - 正式代码是两组:基线组(self|数字,含 status)+ 加宽组(24 个读取器,pid 记号加宽)。
  - 删加宽组里的基线读取器只影响加宽 pid 形态,22bc / 22aj 不走,22bp 只用 ≤2 个读取器。
  - 结果 12/13 全绿(M3)。
- **tight 漂移:** 起草期的 36 个(`tdrop_launch` ×15、`tdrop_remote` ×9、`tdrop_psalt` ×7 等)全部复现为 22bm 转红。它们之外的命令位置字符、关键字、时长后缀不在 22bm 的 91 个成员里(M2)。
- **eval 类:** 起草期 `ext_eval`、`ext_glob`、`vx_eval`、`w12_eval`、`val_eval` 都复现。新增两个变体全绿:命中后求值命令文本(I03d)、URL 分支(B08)(M5)。
- **上界差一:** 起草期已覆盖 W9 的 6 个界、W10 赋值与引用、值长 15 / 17 等,我复现。新增差一(span 帽、PEM 循环、`{0,64}`、`{0,40}`、斜杠数、`for` 帽、`${}` 替换帽)全绿(M4)。
- **路径形:** 起草期是 `loosepath` / `nopath` / `path_eq` / `path_plus` / `path_firstlower`,没有斜杠数的变异;A10 与 E08p 全绿(M4)。
- **时档 (g):**
  - 起草期 `${s#*"$pat"}` 在 (g) 上 5.1× / 13×。我复现为 `Xg2` 5.37× / 15.28×。
  - 我的 `Xg` 先放在 `_sg_vx_replace`,(g) 输入走 `$VAR` 用不到,属不忠实变体,1.40× / 2.06× 绿。
  - 它的探针行全绿,只有 timing (g) 能抓。
- **其它时档:**
  - `Xf` 对 (f) Read 面 9.09× FAIL,对应起草期 `ext_perentry`。
  - `H51` / `H52` 对 (i) 5.11× / 10.46×,起草期 4.8× / 6.9×,量级一致。
  - `H41` / `H42` 对 fhit 29.4× / 28.7×,起草期 65.5×。
  - 方向一致,实现不同,数值不同。
- **19al:** 起草期手写切分「另在 19al 转红」。我的 B12 复用同一个 `_sg_judge_one`,继承同一内建盲区,19al 不红。实现不同,不是矛盾。

## 重点三处

### 1. SC-28 28f 的写法

结论:内容如实,不是迁就检查器造成的假绿,但判据对写法敏感,过宽。

- **内容如实:** 探针里的真实 Write 信封键序就是 `filePath` 在前、`content` 在后(`baseline_probe.py:380`)。注释 `#       "filePath": "...", "content": "..."    // Write: tool_response.content` 如实。
- **换写法测试:** 把 28f 的 lambda(`baseline_probe.py:2360`)原样复制,套到同一头注释的五种写法上:
  ```
  28f check -> PASS   shipped (filePath, content on ONE line)
  28f check -> FAIL   truthful: filePath line, then content on its own line
  28f check -> FAIL   truthful: content first, filePath after it (same line)
  28f check -> FAIL   truthful: Write shape in its own sub-block
  28f check -> FAIL   stale (the baseline Read line restored)
  ```
  三种同样如实的写法都红,只有执笔选的单行写法过。
- **判据是否过宽:** 它禁的是任何以顶层 `"content":` 起头的注释行。这对旧的错误 Read 形状成立,但对 Write 响应的如实写法同样红。不是对如实文档恒红(有一种写法能过),而是写法敏感。
- **反向没问题:** 旧 Read 行恢复后仍红,不会漏掉要抓的错误。
- 评级:minor(m1)。

### 2. W12 归一化循环的代价

- **增量很小:** 同一输入、基线与被审版本交错取最小值,同一 python3 -c 命令里放 N 个 `os.environ.get('K…')`(dense),基线对它 rc=2(拦),被审 rc=0(放)。以下为 3 对交错取最小值,装载 `/proc/loadavg` 一分钟值 0.84–1.98(<2):

  | 命令长度 | 出现次数 | 基线 CPU / 墙钟 | 被审 CPU / 墙钟 | 比值 |
  |---|---|---|---|---|
  | 6.0 KB | 254 | 1.273 / 1.321 s | 1.311 / 1.313 s | 1.03 |
  | 10.8 KB | 454 | 3.630 / 3.674 s | 3.866 / 3.908 s | 1.06 |
  | 12.0 KB | 504 | 4.546 / 4.715 s | 4.960 / 5.004 s | 1.09 |
  | 16.0 KB | 670 | 7.929 / 8.114 s | 9.416 / 9.524 s | 1.19 |

  同长度的非 dense 对照(`os.getenv`,两边都放行)比值 0.94–1.05。
- **会不会越过 5 s:**
  - 窄带内会。12.0 KB / 504 次时,基线墙钟 4.715 s,被审 5.004 s,正好越线。
  - 基线自己在约 12.3–12.6 KB 越过 5 s,所以这只是基线悬崖下方一条约 3% 宽的带,约 0.3–0.4 KB。
  - 带内被审版的结果(放行)与 W12 的预期一致,除非同一条命令还带真实的读取。
  - 不升级:基线悬崖处普通 padding 即可达到同样的绕过(Spec:410 已记「超时即放行」为既有缺口)。
- **成本形态:** 约 0.65 ms/次出现,与 N×L 成正比。可改成一次线性 `sed`,记 m4。

### 3. `_sg_per_segment_eval` 里的 `(( ${#_SGV_N[@]} ))`

- **是否处于 `set -u`:** 是。`secret-guard.sh:174` `set -uo pipefail`,`:1428` 的 `( _sg_per_segment_eval "$command" )` 子 shell 继承该选项。
- **哪些路径会让 `_SGV_N` 未赋值:**
  - 正式代码里没有。`:573` 在 source 闸门之上顶层赋值(加载时执行),`:587` 每次 `_sg_vx_collect` 再赋值。
  - 只有 `_SG_MODE=none`(所有段为空,如命令 `;`)时不会调用 `_sg_vx_pass`,此时靠 `:573` 的初始化。
  - 实测去掉 `:573`,命令 `;` 在 3.2.57 和 5.2.15 上都得到:
    ```
    g_noinit.sh: line 1411: _SGV_N: unbound variable
    [secret-guard] BLOCKED: internal error in per-segment evaluation (rc=1). Failing closed.   (rc=2)
    ```
    即 fail-closed,不是 fail-open。
- **真 bash 3.2.57 实测**(`bin/t_sgvn.sh`,有 `set -u`):

  | 情形 | 3.2.57 | 5.2.15 |
  |---|---|---|
  | `arr=()` 后 `(( ${#arr[@]} ))` | rc 0,「empty」 | rc 0 |
  | 从未赋值 | `arr: unbound variable`,rc 1 | 同 |
  | `declare -a arr` 后 | rc 0 | 5.2 报 unbound(版本差异) |
  | `local arr` 后 | unbound | unbound |
  | `for x in "${arr[@]}"`(已赋值为空数组) | **`arr[@]: unbound variable`**(3.2 特有) | 无错 |

  无 `set -u` 时,各情形都当作 0 个元素。
- **3.2 特有一行的影响:** `"${arr[@]}"` 展开空数组在 3.2 下会死。hook 里这类展开只有 `"${_SG_SEGS[@]}"`(两处,`:780` 先判空)和 `"${risky_patterns[@]}"`(非空),没有未保护的展开。无 finding。

## Findings

### Critical
无。
- **回退:**
  - 120 条日常命令的差分(基线 vs 被审),基线拦、被审放的只有 3 条:`os.environ.get('HOME')`、`os.environ['HOME']`、`jq 'keys_unsorted'`,正是 W12 的误报修复。
  - 30 条泄露形态命令(进程表 / app.ini / `/proc`)被审版全拦,基线只拦 3 条。
  - 两个套件对基线的改动只有 4 行(guard)和夹具拼装(scan),没有被放宽的基线用例。
  - `risky_patterns` 与基线的 diff 恰为 1 条新增 + 2 条解释器行改写 + 2 条 `/proc` 行改写 + 3 条新增 W11。
  - 基线行的删成员坏实现(读取器、路径正则 34 备选、os.environ 4 子串)全被抓。
- **fail-open:** 内建判定先于第二遍与扩展,内建已拦的命令不付额外代价。扩展代码全在 `$( … )` 里,出错只丢扩展。L3 的提前 `exit 0` 与基线一致。未发现让基线能拦的输入被放行的新路径。

### Major

**M1 — id `71e85498`**
- severity major;type gate-placement-check-incomplete;category acceptance-gap;scope `aria/hooks/tests/secret-guard.test.sh#W14 SC-30b`。
- **摘要:** 30b(探针行与套件用例同形)只能发现 `_sg_core_eval`、`_sg_vx_pass` 在闸门之下,发现不了其余 9 个。
- **证据:**
  - 套件 `:2756-2763` 与探针 30b 只断言五档 rc=0 与两条必拦 rc=2。
  - `secret-guard.sh:1410`、`:1412`、`:952`:`_sg_ext_*` 只在 `$( … )` 里被调用,缺函数时 `_x` 为空即「无扩展拦截」;`:1382` `_sg_emit_blocked …; return 2` 忽略其返回值;`:645` `_sg_vx_collect "$cmd"` 忽略返回值,`_SGV_N` 保持 `()`。
  - 变异 `C6emit_blocked`、`C6vx_collect`、`C6vx_apply`、`C6vx_replace`、`C6ext_pass`、`C6ext_subst`、`C6ext_entries`、`C6ext_root`、`C6vars`,`WPA_ONLY=SC-30 WPA_ROWS=30b` → 9/9 `yes`。
  - 组合 S4 把 8 个函数同时下移,带 git 历史的副本,SC-8 五档与 SC-9a 生效:`PASS: 783 / 783`。
  - `proposal.md:246` 明写 `_sg_core_eval`、`_sg_emit_blocked`、`_sg_vx_pass`、`_sg_ext_pass` 及其下游都在闸门之上。
- **失败场景:** 有人把扩展或第二遍的辅助函数写到闸门之下(或新增辅助函数忘了放上面)。SC-8 延迟闸装配里这些函数缺失,开销被漏计,闸门对一个空操作计时仍绿。
- **怎么会红:** 修补后上述 9 个坏实现在 30b 转红。
- **建议修法:**
  - 在 30b 装配里 `source` 之后对传递闭包的函数名逐个 `declare -F … || fail`。闭包名单由静态扫描 `_sg_judge_one` 与 `_sg_per_segment_eval` 的调用图生成。
  - 或让回放在 `command_not_found_handle` 下运行,出现一次即红。

**M2 — id `d8e3fab4`**
- severity major;type tight-copy-drift-unguarded;category acceptance-gap;scope `aria/hooks/secret-guard.sh#_SG_PROCTAB`。
- **摘要:**
  - tight 拷贝的命令位置字符 `; & ( ) {` 反引号 cntrl(7 个)、关键字 then / do / else / elif(5 个含整组)、launcher 时长后缀 m / h / d(3 个),14 个漂移坏实现全绿。
  - W11 的 `ps -O`、末位 `-u` 的「操作数只认首个」2 个全绿。
- **证据**(`bin/t_tight.py`,`ref` 为参考树,`mutant` 为对应坏实现):
  ```
  F1semi    ref=2 mutant=0   '{ true; ps aux | grep -v x; }'
  F1lpar    ref=2 mutant=0   '(ps aux | grep -v x)'
  F1bq      ref=2 mutant=0   'echo `ps aux | grep -v x`'
  F2then    ref=2 mutant=0   'if true; then ps aux | grep -v x; fi'
  F3sufm    ref=2 mutant=0   'timeout 5m ps aux | grep -v x'
  ```
  `22bm`(`22bm,22bn`)全红不了它们;整组 SC-22 对 `B5kw` 全绿;guard 套件 S1(同时含 F1semi、F2then、F3sufm、A20、C4psO、E10bm、E10cm)只因 B03、C2top 红,这 14 个无贡献。`C4psO` 的 `ps -p 1 -O rss` 与 `I04psu` 的 `ps -p 1 -u`、`ps -C nginx -u`:ref=2、坏实现=0,整组 SC-22 全绿。
- **Spec:** `proposal.md:202`「规则行与 tight 判定是同一份定义的两份拷贝…逐成员行使任一份漂移转红」;22bm 的成员清单是 10 类 ps 参数、14 个短横写法、15 个 launcher 等,没有位置形态。
- **失败场景:** 以后改规则行(加一个命令位置字符或关键字)忘了同步 tight 拷贝,这些位置的整行 `grep -v` 过滤重新获得 credit,进程表被放行。
- **怎么会红:** 给 22bm 补 14 个位置 / 关键字 / 时长形态;给 22bu 补 `ps -p 1 -O rss`、`ps -p 1 -u`。
- **建议修法:** 把规则行的命令位置前缀抽成变量,规则行与 tight 拷贝共用(规则行是变量时 31c 的 census 会读成空串,所以需内联生成或用同一份字面再加一致性断言)。

**M3 — id `f535d33d`**
- severity major;type enum-member-unguarded;category acceptance-gap;scope `aria/hooks/secret-guard.sh#risky_patterns:/proc-widened-row`。
- **摘要:** `/proc` 加宽组(`:1253` 第二分支)里 12 个基线读取器 head tail less more strings hexdump od xxd tr awk perl rev,删掉任一,加宽 pid 形态下的整份环境读取被放行。
- **证据**(`bin/t_enum.py`):
  ```
  tail /proc/$$/environ              ref=2 D24b-tail=0
  tail /proc/*/cmdline               ref=2 D24b-tail=0
  tail /proc/thread-self/environ     ref=2 D24b-tail=0
  head /proc/$pid/cmdline            ref=2 D24b-head=0
  rev  /proc/*/cmdline               ref=2 D24b-rev=0
  ```
  整组 SC-22 对 12 个坏实现全绿;`cat` 经 22be 22bp 红,新增 11 个读取器经 22bd 22bp 红。
- **Spec:** `proposal.md:201`「读取器 = 基线 13 个 + 新增 11 个」。22bc / 22aj 只走基线组的 self / 数字 pid;22bp 的加宽 pid 形态只用 ≤2 个读取器。
- **失败场景:** 重写加宽组时丢了某个基线读取器,`tail /proc/*/environ` 之类被放行,无任何行报警。
- **怎么会红:** 22bp 对 24 个读取器 × 一个加宽 pid 形态(如 `$$`)逐个出行。
- **建议修法:** 加宽组读取器表改成变量并断言与基线 13 个 + 新增 11 个相等。

**M4 — id `1377556c`**
- severity major;type bound-off-by-one-unguarded;category acceptance-gap;scope `aria/hooks/secret-scan.sh#_path_form`。
- **摘要:** Spec 要求「对每个上界做差一的边界坏实现」,约 16 个差一坏实现让所有点名行与两个套件保持绿。
- **证据**(`bin/t_bounds.py`、`bin/t_path.py`;scan 套件 S3 / S3b 为 `122/122`,guard 套件 S1 / S2 的失败用例均可归因到其它成员):
  ```
  201 real kv credentials: ref matches=201  E01m(cap 199)=200  E01p(cap 201)=202  E02x2=200
  kv key with 64 upper-case chars before TOKEN: ref alert=True  E06prem(63)=False  E06prep(65)=True
  kv key with 65 upper-case chars:             ref alert=False E06prem=False       E06prep=True
  cli flag with 40 chars before 'token':       ref alert=True  E06clim(39)=False   E06clip(41)=True
  W10 ${f} cap, reader is the 8th/9th occurrence: ref rc=2/0  E10cm(7) 0/0  E10cp(9) 2/2
  W10 for-statement cap, 8th/9th statement:       ref rc=2/0  E10bm(7) 0/0  E10bp(9) 2/2
  exactly ONE slash  (credential-shaped, must alert): ref True  A10 False  E08p True
  exactly TWO slashes (relative path, must be silent): ref False A10 False  E08p True
  ```
  另 `E03bm` / `E03bp`(PEM 指纹循环 `FP_N < 9` / `< 11`)探针与套件全绿。
- **失败场景:** 以后有人把某个界写偏一格:漏掉第 200 个真凭据、把 65 字符键名也当键、把一斜杠的 base64 值当路径放过(约 0.4% 的 `/` 起头 44 字符随机值受影响)。
- **怎么会红:** 补行:
  - 199 个占位 + 第 200 / 201 个真凭据;
  - 键名恰好 64 / 65 前缀;
  - 旗标名 40 / 41;
  - 恰 1 个与恰 2 个 `/` 的路径形;
  - 8 个与 9 个 `for` 语句;
  - `${f}` 第 8 / 9 次引用;
  - 超过 10 个 PEM 块的指纹项数。
- **建议修法:** 补这些边界行。`E01` 需要真凭据放在边界位置,11w 全是占位值所以观察不到。

**M5 — id `85125bc9`**
- severity major;type no-execution-invariant-coverage-hole;category acceptance-gap;scope `aria/hooks/secret-guard.sh#_sg_ext_pass`(另见 `secret-scan.sh#_value_of`)。
- **摘要:** 「不执行不变量」两处覆盖洞,坏实现不改任何点名行,但钩子执行了被扫描内容或命令文本。
- **证据(19ab):**
  - 19ab 的三条命令 `ls -la`、`cat gl/stxxar.conf`、`echo "$(touch canary-ext-3)"`(`baseline_probe.py:1504`)都不含条目命中,所以命中之后才执行的路径没人跑。
  - `bin/t_i03d.py`:
    ```
    ref   entry hit + payload              rc=2 canary created=False
    I03d  entry hit + payload              rc=2 canary created=True
    I03d  payload only (the 19ab shape)    rc=0 canary created=False
    ```
  - 整组 SC-19 / SC-20 全绿;guard 套件 S5(I03d + A16)`771/772`,仅 SC-13 无 git 假红。
- **证据(7n):** 7n 的 10 个运行只含 5 个 JSON / env 键(`baseline_probe.py:7n`,Spec SC-7)。`bin/t_survivors.py` T4:
  ```
  T4 ref: Read result with a back-quoted payload in the password slot of a postgres URL  rc 0 alert: True canary created: False
  T4 B08: (same input)                                                                   rc 0 alert: True canary created: True
  ```
  SC-7 / SC-12 整组与 scan 套件 S3 全绿。URL 三个 tag 的口令位字符类 `[^@[:space:]"]{4,}` 允许 `$ ( ) \``,所以可利用。
- **失败场景:** 有人为展开 `~` 在命中后对替换副本 `eval`,或在 URL 分支取口令时 `eval echo`。被扫描输出里的命令替换会在钩子里执行,绕过权限提示与 deny 规则。
- **怎么会红:** 19ab 增加 `cat <条目> $(touch c)`;7n 增加 postgres / redis / mongodb / basic-auth 四类 URL 口令位带命令替换(用 `${IFS}` 免空格)的载荷。
- **建议修法:** 补行即可,hook 无缺陷。

**M6 — id `a9882850`**
- severity major;type timeout-regression;category performance;scope `aria/hooks/secret-guard.sh#_sg_vx_apply`。
- **摘要:** W10 第二遍判定的串长 = 命令 + 引用数 × 值长,没有上界,实测一个 5.45 KB 的命令越过 5 s 超时,基线不会;Spec 的 (g) 档只测到 ≤300 B 值。
- **证据:**
  - `bin/w10time.py`(16 个赋值每个 VLEN 字节、其后一个段里每个变量 8 次引用共 128 个引用;`loadavg(1m)` 2.19):
    ```
    vlen  cmdlen  base cpu/wall      new cpu/wall      new/base
     150    3050   0.48s/ 0.48s       1.76s/ 1.78s       3.7
     250    4650   0.96s/ 0.97s       4.04s/ 4.09s       4.2
     300    5450   1.14s/ 1.15s       5.44s/ 5.48s       4.8     ← 墙钟 >5 s
     400    7050   1.76s/ 1.77s       8.81s/ 8.87s       5.0
    ```
  - 较轻的形态(`bin/w10shapes.py`):

    | 形态 | 命令长度 | 基线 | 被审 |
    |---|---|---|---|
    | 4 个变量 × 300 B × 8 次引用 | 1.4 KB | 0.17 s | 0.29 s(1.7×) |
    | 8 × 600 × 8 | 5.1 KB | 0.97 s | 3.05 s,墙钟 3.40 s(3.1×) |
    | 16 × 300 × 8 | 5.45 KB | 1.14 s | 5.18 s,墙钟 5.26 s |
    | 16 × 300 × 4 引用 | | 1.21 s | 1.88 s |

    成本与引用数、值长之积成正比。
  - Spec 自带 `timing.py` 的 (g) 档,参数改成 `--vlen 400 --nrefs 128 --nvars 16 --gsize 8000`,在**参考树**上 FAIL:g-a 2.294 → 8.604 s(3.75×),g-b 2.229 → 9.644 s(4.33×),界 2.5。
  - `proposal.md:355` 写「含 `$VAR` 引用的命令因 W10 第二遍约为基线的 1.45–2.50 倍…引用越密越近 2×」,与上面矛盾。
- **为什么不是 critical:** 第二遍只在内建全部放行之后才运行,内建已拦的命令不付这个代价,所以不会把基线能拦的输入放行。受影响的是良性命令的无谓超时,以及 W10 / W9 这套新增能力本身的有效性。
- **失败场景:** 5 KB 级的部署脚本,有十几个长值变量且每个被引用多次(同一管道段内),钩子 5–10 s,harness 报 hook 超时。
- **怎么会红:** 加 (g-c) 档:16 个赋值 × 300–400 B、每个变量 8 次引用,界 ≤2.5×;当前参考树红。
- **建议修法:**
  - 在 `_sg_vx_apply` 里给替换后串长设预算(如不超过原段的若干倍或 16 KB),超限当作「超出上限放行」,与 21y 的既有口径一致。
  - `$NAME` 循环每次从头做正则扫描,是平方项:把已替换的前缀累加进 `out`,只在剩余后缀里继续找(如 `_sg_vx_replace` 的写法)。
  - 订正 Impact 里 1.45–2.50 倍的表述。

**M7 — id `e0470306`**
- severity major;type enum-member-unguarded;category acceptance-gap;scope `aria/hooks/secret-scan.sh#CLASSIFIED_TAGS`。
- **摘要:** L3 逐 tag 的分类范围缺项全绿(均为误报方向)。
- **证据:**
  - 白名单:CLASSIFIED_TAGS 去掉 `json-env-secret-key`、`cf-access-client-secret`,SC-4…SC-11 整组全绿;`bin/t_enum.py`:
    ```
    whitelist (FAKE_ marker) on json-env-secret-key       ref alert=False mutant alert=True
    whitelist (FAKE_ marker) on cf-access-client-secret   ref alert=False mutant alert=True
    ```
  - 熵 / 路径 / 点链:NEW_TAGS 去掉 `json-env-secret-key`、`cf-access-client-secret`,SC-9 / SC-10 整组全绿:
    ```
    entropy floor (single class) on json-env-secret-key        ref alert=False mutant alert=True
    entropy floor on cf-access-client-secret                   ref alert=False mutant alert=True
    ```
    `auth-header-token`、`cli-secret-flag` 缺项由 10i 抓。
  - jq 元数据词:去掉 `paths` / `leaf_paths`,SC-24 整组全绿;`curl -s http://nomad.invalid/v1/var/x | jq paths` 基线与 ref 为 0,坏实现为 2。
  - W8 行左边界类 `[^[:alnum:]_.-]` 去掉 `_`、`.`、`-`:`my-cat /etc/forgejo/app.ini` 等 ref=0、坏实现=2,SC-16 / SC-17 整组全绿。
- **失败场景:** 误报增多(告警或拦截更吵),不增加漏报。
- **怎么会红:** 对每个新 tag 的白名单、熵、路径、点链各补一例同形的放行行;SC-24 补 `paths` / `leaf_paths`;SC-17 补 `my-cat` / `a_cat` / `x.cat`。
- **建议修法:** 补行。

**M8 — id `d4c465c7`**
- severity major;type literal-match-unguarded;category acceptance-gap;scope `aria/hooks/secret-guard.sh#_sg_ext_path_pass`。
- **摘要:** Read/Edit 面扩展条目的「字面子串」性没有任何行。
- **证据:** `bin/t_survivors.py` T1,项目清单含 `a(b)c.conf`、`x[1]y.txt`、`p+q.cfg`、`m*n.dat`、`v?w.env2`:
  ```
  Read /srv/a(b)c.conf                     want 2  ref/A15/A16 = [2, 0, 2]
  Read /srv/x[1]y.txt                      want 2  ref/A15/A16 = [2, 0, 0]
  Read /srv/p+q.cfg                        want 2  ref/A15/A16 = [2, 0, 2]
  Read /srv/nxdat (must be 0)              want 0  ref/A15/A16 = [0, 2, 0]
  Read /srv/x1y.txt (must be 0)            want 0  ref/A15/A16 = [0, 2, 2]
  ```
  SC-19 / SC-20 整组与 guard 套件(S2、S5)全绿。套件的 19j 用 `cat $wpa_e`(`secret-guard.test.sh:2302`),只测 Bash 面。
- **失败场景:** 有人把 Read 面改成 ERE 或 glob 匹配:含 `( [ +` 的条目在 Read 上失效(放行)或误拦相近路径。
- **怎么会红:** 19j 与 19k 各加一遍 Read / Edit 面。
- **建议修法:** 补行。

### Minor

- **m1 — id `1ad079e6`**(doc-consistency / checker-over-wide,`aria/hooks/secret-scan.sh#hook-contract-header`):28f 写法敏感,见「重点三处」1。建议把负条件收窄到旧 Read 形状(如 `"content"` 行带 `Read` 字样,或不在 `file` 之下),不要禁所有顶层 `"content":`。
- **m2 — id `31136efd`**(test-design / name-coupled-marker,`baseline_probe.py#marker_row`):
  - 求值顺序行 20l / 20m / 21v / 21w 以函数名(`_sg_vx_pass`、`_sg_ext_pass`、`_sg_ext_path_pass`)插桩;换一个不调这些函数的实现(A20)就绕过,只剩 timing.py h2 抓(5.75×,7.2 s CPU,会越过 5 s 超时)。
  - 32a 的检测器要求变量名或行首:`${1,,}`(H23)只被 32c / 32d 抓;`declare -A` / `mapfile` / `coproc` 在行中或循环里的写法 32a 看不到(H04 / H05 / H13 / H14 / H15 / H21 / H24 只被 32a 抓,依赖该行被扫到)。
  - 建议加一条与函数名无关的顺序行:`f=/etc/forgejo/app.ini; cat "$f"; cat .env` 的 BLOCKED 文案必须点名 `.env` 行。
- **m3 — id `dcaaa47b`**(code-quality / redundant-code,`aria/hooks/secret-guard.sh#_sg_vx_collect`):`:589` 的声明前缀可选组整个多余(删任一成员或整组,全部行与命令不变),Spec 已注明。属已知等价,留作后来者免追。
- **m4 — id `c73144ec`**(performance / linear-scan-loops-before-verdict,`aria/hooks/secret-guard.sh#_sg_judge_one`):`:1371-1374` 四个 `while` 循环在内建判定之前、对每个含 `environ` 的段做 O(出现次数 × 长度) 的归一化。增量见「重点三处」2。建议改成一次 `sed` 或只在内建没拦下时再做。
- **m5 — id `94afa057`**(false-positive / right-boundary-collateral,`aria/hooks/secret-guard.sh#_SG_SRVCFG`):右边界「app.ini 后无字母 / 数字 / 下划线」把 `cat /etc/gitea/app.ini.example` 和 `git diff HEAD -- custom/conf/app.ini` 也拦下(`bin/fp_diff.py`)。属 16m 备份覆盖的连带效果,按设计,但示例文件和 git diff 是良性写法。建议在 Spec 里点名接受,或把备份后缀收成 `.bak|.old|.orig|~|.swp`。

## 证据复跑记录

- **参考树与基线树:** `git -C aria archive 69af7cd | tar -x`,`git -C standards archive be842ce | tar -x`;基线树 `268da8f` / `2bc1c4c` 同法。sha256 前 16 位:guard `061d15f16e7c6d39`、scan `77d747e63402fdbb`、hooks.json `20529435a4533428`、guard.test `0cadad2f2a2b06ea`、scan.test `0e009b821504520b`、hygiene `f7a8fb9363ed5d57`,全部一致。
- **探针子集:** `WPA_ONLY=… WPA_ROWS=… python3 baseline_probe.py <树>/aria` 共 699 次(含整组复跑与重复),全为子集,无全量。控制:`A00` 只加一行注释,5 行全绿;`K0`(52 行,其中 49 个 hook-direct 行):32c / 32d / 32e 在 bash 5.2 vs 真 bash 3.2.57、`C.UTF-8` vs `en_US.UTF-8` vs `C` 下逐行一致。
- **套件(11 次完整运行):**
  - 参考树 `b5` 与 `b32`:scan `122/122`;guard `771/772`,唯一 FAIL 是无 git 副本上的 SC-13 头注释计数假红。
  - 带 git 历史的克隆副本(`gitrepo/`)对照 `S0g`:`783/783`,SC-8 五档与 SC-9a 生效。
  - 组合坏实现:S1(9 个)guard `764/772`,失败用例只来自 B03(SC-19 六例)与 C2top(22bl)与 SC-13;S2(4 个)guard `768/772`,失败来自 C4top(22bl / 22bm / 22p)与 SC-13;S3 / S3b 各 7 个 scan `122/122`;S4(带 git,8 个函数下移)guard `783/783`;S5(2 个)guard `771/772`(仅 SC-13)。
- **`timing.py --judge`**(`out/timing_all.txt`,约 18 次):
  - 参考树全部 19 个有界档 PASS(装载约 7.5)。
  - 坏实现:A19 h2 FAIL;A20 h2 FAIL(5.75×);G20b h1 单次 215 s CPU(141×)后手动中止;H41 / H42 fhit FAIL;H51 / H52 (i) FAIL;Xf (f) Read FAIL;Xg2 (g) FAIL;Xg(位置错)PASS。
  - 大值 (g) 档在参考树上 FAIL(见 M6)。
  - i3 档对 5 个 C7 变体:`C7lastword` / `C7cfkey` / `C7kvafter` 全部 PASS,即等价。
- **差分与静态:** `bin/fp_diff.py`(120 条日常命令)、`bin/fn_probe.py`(30 条泄露形态)、`shellcheck 0.9.0 -S warning` 对两个 hook(基线 / 被审)均 0 条、`bash -n` 在 5.2 与 3.2.57 均通过。
- **直接复现脚本**在 `bin/`:`t_survivors.py`、`t_enum.py`、`t_bounds.py`、`t_path.py`、`t_tight.py`、`t_j.py`、`t_jq.py`、`t_i03d.py`、`t_sgvn.sh`、`w10time.py`、`w10shapes.py`、`w12time.py`。结果:`out/res_*.jsonl`、`out/timing_all.txt`、`out/quiet.txt`、`out/mutsuite_*/`。

## 风险 / 疑问

1. `hooks.json` 新增的 `PostToolUseFailure` 键:若某采用方的 Claude Code 版本不认该事件,整份 `hooks.json` 被拒的行为未知,可能让插件所有 hook(含 secret-guard)一起不加载。本机是 2.1.292,没有旧版二进制,未验证。建议 Tasks 1.12 加一腿:最低支持版本加载该文件。
2. macOS / BSD 工具链(`grep -b` 与 `-o -F -f` 组合、`sed` 字节类、`localedef`、`local -x`)未验证。
3. SC-8 tier (e) 在 `S0g` 的装载约 7.5 下 old=43.9 ms、new=80.6 ms、天花板 100 ms 绝对值,余量只有 19%,装载更高的 CI 上有误红风险。
4. 超时即放行(Spec:410)是既有缺口。本次新增的 W10 / W9 路径缩短了到悬崖的距离(M6),是否改成超时 fail-closed 属 owner 决定,不在本次范围。
5. L3 不扫成功 Bash 调用的 stderr(Spec W1 选 A);harness 是否把 stderr 并入 `stdout` 未验证。
6. 仅 timing.py 能抓的坏实现(A20、H51、Xg2、Xf)没有功能行,TASK-010 的 `timing.py --judge` 是唯一防线,须在空闲主机跑(我的控制跑在装载约 7 时仍 19/19 PASS,但绝对值随主机变)。
7. `WPA_ONLY` 里只要含 SC-14 / 27 / 29 / 31,探针就拉起整套件加 census(约 4 分钟),`WPA_ROWS` 不能让它变快;给后来的审查者提个醒。
8. 项目里的 `.aria/secret-guard.paths` 只增不减,但来自不可信仓库的清单可以让命令被误拦(DoS),Spec 已记。
9. 真仓里的 `.aria/notes/2026-10-08-wpa-phase-b/PROGRESS.md` 显示已修改,不是本席动的(本席没有向 `/home/dev/Aria` 及其子模块写过任何字节,没有任何 git 写操作;`git clone --no-local` 只读源仓,落在我自己的工作区)。

## Verdict

**PASS_WITH_WARNINGS:** critical 0 / major 8 / minor 5。

修完 major 后能进入 TASK-010 验收,有两个条件:
- 只有 M6 需要改 hook 代码:W10 第二遍加串长预算、重测 (g) 档,并订正 Impact 的 1.45–2.50 倍。其余 7 条是补探针行和套件用例,hook 行为没有缺陷。
- 补行后重跑 `WPA_REQUIRE_ALL=1` 与 `timing.py --judge`(空闲主机)。

## 用量

- **实际工作墙钟:** 约 4 h 20 min(10:08:54Z 建工作区 → 14:26Z 收尾,含等后台)。
- **探针子集:** 699 次。
- **套件:** 11 次完整运行,另有 `jq-crlf-guard.sh` 静态检查与 `shellcheck` 若干次。
- **timing.py:** 约 18 次。
- **坏实现个数:** 667 个独立构造。
- 无残留后台任务。
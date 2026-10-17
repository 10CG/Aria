# 返修报告: secret-net-l3-and-bypass-paths v4 -> v5 (post_spec 第 4 轮)

## 0. 摘要

- 第 4 轮 25 条 finding (1C / 9M / 15m) **全部 fixed** (0 rejected, 0 deferred; km/m6 的 Spec 侧已修, 清理已推送内容属 owner, 记 7.20), 主控 7 条裁定全部执行。
- 机制层面按主控方针 7 **复用而不新写**: 簇 T 的扩展判定直接调用内建的同一个判定函数 (`_sg_core_eval`), 没有第二份阶段 / 引号状态机; 簇 F 沿用默认 credit; 簇 M 只加成员行; 簇 U 是把基线视图原样保留再追加一个视图。需要新写的只有 W2 两个 pattern 的有界化 (线性)。
- 探针 437 行 (上一版 411), 目标态 436 行 `yes` + SC-30 一行不执行, 基线形态 `holds`。三份文件 sha256 前 16 位: proposal `cedbdfce05575891` (214093 字节), 探针 `cf331b4aa264a863` (222199 字节), 证据 `b41e86d796bb583c` (104900 字节)。
- 变异实测: 本轮新坏实现 117 个, 112 个转红、5 个转 0 行 (逐个有理由); 前几版坏实现回归 499 个, 丢失转红行 0 个。
- **改变实现者动作且需重点核**的改动见第 3 节 (W1 两视图、W9 重做、W2 有界化、W11 credit 反转), 第 6 节列请裁项。

## 1. 处置表 (席位 · 编号 · 键 · 处置 · 改动位置或证据; 全文见结构化输出的 `dispositions`)

| 席位 | 编号 | 键 | 处置 | 改动位置 / 证据 (摘要) |
|---|---|---|---|---|
| tech-lead | M1 | `e2459206` | fixed | W11 转储 credit 默认 (不属 tight) + SC-22 22br (44 运行放行) / 22bs (22 运行限制) + Impact + 待复议 23; 坏实现 env_tight 使 22br / 22bs 全红; 4 个 remote_env_split 等价变异在带过滤的转储上重新验证 0 行红 |
| tech-lead | M2 | `22bdd143` | fixed | 整个机制换掉: 一次固定字符串比对 + 换名 + 内建 _sg_core_eval 一遍 (线性); W14 (f-hit) / (i3), SC-34 34c; 实测 2 KB / 8 KB 64 处: 目标 1.7x / 1.9x, 旧设计 7.6x / 24.7x, 逐出现点重判 55x / 64.8x |
| tech-lead | m1 | `6ff1d962` | fixed | 成文并钉 (不改规则): W11 已知限制 + Impact + 22bj 扩为 14 个运行 (新增 env 词 5 + /proc 文本检索 3, 每个成员都有会转红的坏实现); 待复议 27 |
| tech-lead | m2 | `984b1c3d` | fixed | W2 / W8 已知限制 + SC-10 10m (6 个运行) + 7.8 / 7.9 |
| backend-architect | C1 | `1038b8da` | fixed | W1 两视图并集 (基线视图照扫, 含 NUL 且 N != D 才追加); SC-1 1e / 1f / 1g; 坏实现 nul_replace 使 1e / 1f 红, nul_always_* 使 1g / 2a-2d 红 |
| backend-architect | M1 | `755aab21` | fixed | W2 线性段 + kv / cli 有界前后缀与左边界 + 值抽取线性; SC-34 34a / 34b, SC-9 9z, SC-10 10n / 10o, W14 (i3); fuzz_value_of 17 tag 0 分歧 |
| backend-architect | M2 | `0a8380fd` | fixed | 簇 T: 复用 _sg_core_eval, 不另写切分; SC-19 19af (73 形态零分歧) / 19z / 19aa / 19ak / 19al; 旧设计 54/73, 本设计 73/73 (独立 93 形态电池与随机 2500 条差分都是 0 分歧) |
| backend-architect | m1 | `6f503728` | fixed | 采纳: 含 ASCII 字母数字或任一非 ASCII 字节即有效; 19ae 改 baseline-failing + 19ah; 坏实现 ext_ascii_only 红 |
| qa-engineer | M1 | `0a8380fd` | fixed | 同簇 T: 掩码机制已删, 19af 含转义 / `$'…'` / 管道 / 换行; ext_v4stage:noesc_q / noesc_all / noansi / nopipe / nonl 各红 19af |
| qa-engineer | M2 | `eb350937` | fixed | W8.3 + W14 通则列入 `:641`; SC-18 18j / 18k 各 32 运行; readface16 与 readface_drop:1-32 逐成员红 |
| qa-engineer | m1 | `65fb3fcf` | fixed | W12 全部替换 + SC-23 23j + SC-25 25h; w12_once 使 23j 4/4 红, w12_echo_norm 只使 25h 红 |
| qa-engineer | m2 | `684e9a24` | fixed | W9 剥 BOM + SC-19 19ai; ext_nobom 红 |
| qa-engineer | m3 | `aa08f71d` | fixed | SC-32 32e (POSIX locale, 382 行); ell_lastchar 使 32e 红 (点名 11v / 11x / 11y), 默认 32d 仍 yes |
| code-reviewer | M1 | `0a8380fd` | fixed | W9 偏移与切片同一单位 + `local -x LC_ALL=C`; SC-19 19ag / 19ah / 19am; ext_charslice / ext_localnoexp / ext_noc 红 |
| code-reviewer | M2 | `8fbbee80` | fixed | 同 tl/M1: credit 默认 + 22br / 22bs; env_tight 红; 等价变异论证重做 |
| code-reviewer | m1 | `6ff1d962` | fixed | 同 tl/m1 (两类 + 22bj 14 个运行) |
| code-reviewer | m2 | `684e9a24` | fixed | W9 / Impact / 7.1 不再复述旧数字; 时档数字只在 W14 第 5 项与 Impact 性能条, 由 mk_numbers.py 从原始输出生成 |
| knowledge-manager | M1 | `0a8380fd` | fixed | 同簇 T |
| knowledge-manager | m1 | `a8f5db8c` | fixed | W1 理由按实测重写 (nul_off: kv=1; nul_space: kv=4) |
| knowledge-manager | m2 | `13e1f258` | fixed | 删除全部版本 / 审计叙事 (逐处列在同族扫描); format_lint 机械检查 0 |
| knowledge-manager | m3 | `7b20c975` | fixed | 同 cr/m2 |
| knowledge-manager | m4 | `60eea71e` | fixed | 26g 标记词扩为 13 个 (逐条披露各一) + 逐标记词坏实现 --cl-drop x13 各红; W9 指明第二个 Hooks 小节 |
| knowledge-manager | m5 | `cfd9ca0b` | fixed | 消除对 awk 的依赖 (只用 sed); 去 LC_ALL=C 的坏实现 ext_noc 在 mawk 主机上本机可证伪 |
| knowledge-manager | m6 | `91a89f9b` | fixed | Spec 侧: 7.1 / 7.2 去量化 + 新增 7.20 产品级披露范围; 研究笔记同改与已推送分支清理不在执笔权限内, 列请裁 |
| knowledge-manager | m7 | `8936aa07` | fixed | 四处各改: 28o + W14 清单加 :8; 22av 逐个写全; 22bk 清单 11 个; Impact 改引 COMMIT_FOOTER_GUIDE.md:199-200 |
| 主控 | 裁定1 | `master-1` | fixed | 簇 U: 两视图并集 + UTF-16LE 反向守卫 + 进程环境形检出行 |
| 主控 | 裁定2 | `master-2` | fixed | 簇 T: 复用内建同一判定函数, 差分表零分歧钉进 SC-19 |
| 主控 | 裁定3 | `master-3` | fixed | 簇 V / W: 线性写明原因 + 时档行 + 探针内 SC-34 |
| 主控 | 裁定4 | `master-4` | fixed | 簇 F: credit 制度明文 + 22br / 22bs 两方向 + Impact 申报 |
| 主控 | 裁定5 | `master-5` | fixed | 簇 M: 18j / 18k 逐备选 |
| 主控 | 裁定6 | `master-6` | fixed | 全部 minor 逐条处置 (见上) |
| 主控 | 裁定7 | `master-7` | fixed | 复用已有机制, 每处配会转红的坏实现, 既有检出不降低 (Part B1 / B2 回归) |

键 `0a8380fd` 在 ba/M2、qa/M1、cr/M1、km/M1 四个席位下是同一个问题 (簇 T) 的四个视角; 键 `684e9a24` 在 qa/m2 (BOM) 与 cr/m2 (旧时档数字) 下是**两个不同的问题**, 分开处置; 键 `6ff1d962` 在 tl/m1 与 cr/m1 下同一问题。

## 2. 同族扫描清单 (修类不修例)

**簇 U (对输入做变换必须相对既有检出是超集)** —— 逐个核对 proposal 里「对输入做变换」的全部位置:
1. W1 内容提取 (`jq` 之后): 修 —— 两视图并集。
2. W9 条目文件读取与过滤: 新输入, 没有基线检出可丢; 文件含 NUL 则整体忽略 (SC-20 20d)。
3. W9 命令文本换名: 内建先判原文、放行后才判替换副本, 只追加拦截 (超集)。
4. W10 变量展开: 内建先判、放行后才判展开副本 (超集, SC-21 21v / 21w)。
5. W12 单键读取归一化: **有意放宽** (Impact 新放行已申报; 23c / 23d / 23e / 23j 与 25h 钉边界)。
6. W3 白名单 / W2 分类器: 有意减少计数 (Impact 新静默已申报; SC-7 7h / 7j / 7k / 7l / 7m 钉不外溢)。
7. W2 / W4 取值与去空白代码: 只影响分类与指纹, 不改计数循环; 与上一版逐 span 差分 0 分歧。

**簇 T (扩展与内建同判)** —— 兄弟位置: (a) Read / Edit 面的扩展入口 `_sg_ext_path_pass` 是对小写化路径的字面子串比对, 与内建 Read / Edit 面的名字组 + 右边界**有意不同** (19aj / 19s / 19t / 19p / 19am 钉); (b) W10 变量展开之后的扩展判定: 对替换副本再走同一个 `_sg_ext_pass` (19i); (c) 「偏移与切片单位」类: 全部 bash 层切片位置核对 —— W10 的 `_sg_vx_replace` 与 W12 的前后缀拼接、L3 的 `_value_of` 用的都是同一个 shell 内的长度 (同一单位), 唯一把外部程序给的字节偏移交给 bash 切片的是 W9, 已按字节统一; (d) 「导出 locale」类: 原型里全部 `local ... LC_ALL=C` 只出现在 `_sg_ext_*` 内, 且都是 `local -x`。

**簇 V / W (线性)** —— 新增或改写的全部匹配 / 取值 / 扫描代码逐个列出并各有依据: 6 个新 pattern (kv 与 cli 有界 + 左边界; 两个 JSON 键形以 `"` 起头; 两个头形以字面头名起头, 都没有无界前缀; ere_battery 对 40 种对抗形态 × 6 个 pattern 做缩放比, 最大尺寸下单个 grep 最长约 0.43 s), 17 个 tag 的取值 (`%%` + 长度取余量, fuzz_value_of 0 分歧), `_trimV` / `_RE_LASTWORD` (`[[ =~ ]]` 捕获), W10 / W12 的前后缀拼接, W9 命中路径 (一次 grep + 至多 64 次循环), `_sg_ext_entries` (一条 sed 流水线)。时档 (i3) / (f-hit) 与探针 SC-34 各盯一类。

**簇 F (credit 制度)** —— 新增或改写的全部「credit」判定位置: ps 族 (tight, 22bm / 22bn)、`/proc` 行 (默认, 22bh)、包裹下的转储 (默认, 22br / 22bs)、app.ini (tight, 16r)、claude-config (tight, 16p)、jq 锚定 credit (W12, 24 系列)。各自两个方向都有行。

**簇 M (原位改写的既有规则)** —— `/proc` 两行 (22bc / 22aj)、python3 -c / node -e 两行 (16o)、`_sg_compute_credit` 的 tight (16p)、Read / Edit 面 `:641` (18j / 18k): 全部列在 W14 原位改写通则里。

**minor 类** —— (1) 同一事实的多处数字: 进程时档数字 (W9 无扩展开销句、Impact 扩展开销句、待复议 7.1) 不再各抄一份, 只留 W14 第 5 项、Impact 性能条与 W1 的 Read 耗时三处, 由脚本从同一份原始输出写入 (W2 / W9 里另有一次性实测数字: ERE 秒数与手写阶段切分的倍数, 各自来自 `ere_claims.py` / `occ_cost.py` 的输出); (2) 版本 / 审计叙事: 头部证据位置、W2、W9、W11、W14、SC 导言、Tasks 1.8、待复议 23 / 27、Impact refs_check 句, `format_lint.py` 机械检查为 0; (3) 清单与计数对不上: 22av (14 个逐个写全)、22bk (11 个)、SC-18 / SC-22 / SC-23 / SC-25 / SC-28 / SC-32 的 `×N` 表头与总行数 (check_counts.py 与 xref_check.py 对 stdout 逐 SC 对账: 本轮改过的条目全部一致; 其余 5 条 (SC-11 / 15 / 17 / 20 / 27) 是上一版就有的「分段计数、未写总数」写法, 未改); (4) 引用精度: Impact 的 COMMIT_FOOTER_GUIDE.md:199-200 与 git-commit.md §6.1; W14 陈旧表述清单补 `secret-guard.sh:8`。

## 3. 改变实现者动作的改动 (单列, 请主控重点核)

下面每一条都会改变实现者**要写的代码或要做的验证**, 请主控逐条核:

1. **W1 NUL 处理由「替换基线视图」改为「两视图并集」**: 提取处的 `jq` 程序提成单一变量 `_content_prog`; 基线提取一行不动; 仅当原始信封含 `\u0000` 且换行视图与基线视图不同才追加。实现者不再写 `tr '\000' '\n'` 接在提取之后。
2. **W2 两个 pattern 的写法收紧**: kv 的键名前后缀 `{0,64}` + 左边界 `(^|[^A-Za-z0-9_])`, cli 的参数名前缀 `{0,40}` + 左边界 `(^|[^A-Za-z0-9-])`; 超出上界或紧贴字母数字的写法不覆盖 (新增 3 个 known-limit 行 10m / 10n / 10o)。这是**覆盖面的收窄**, 理由是线性 (SC-34), 列待复议 31。
3. **W2 / W4 取值代码的写法约束**: 禁用前导 `*` 的 `#` / `##` 前缀删除, 取值只用 `${s%%X*}` + `${s:N}` + `[[ =~ ]]` 捕获 (原型的 `_value_of` / `_trimV` 即是)。
4. **W9 扩展的 Bash 面整体重做**: 不再自写阶段 / 引号 / 转义状态机; 要写 `_sg_ext_subst` (一次 `grep -oFib -f` + 前 64 处换成 `/etc/gitea/app.ini ` 的拼接) 与 `_sg_ext_pass` (把替换副本交 `_sg_core_eval`); `_sg_core_eval` 是把基线 `_sg_per_segment_eval` 的函数体原样提出 (加一个 `_SG_MODE` 记录), `_sg_per_segment_eval` 与 `_sg_ext_pass` 各调用它。
5. **W9 条目与 locale 的细则**: `local -x LC_ALL=C` (导出; 不是 `local LC_ALL=C`), 条目有效性 = 4-200 字节且含 ASCII 字母数字或任一非 ASCII 字节 (**纯中文条目现在有效**, 这是行为变化), 剥 UTF-8 BOM 与 CR 与首尾空白, 条目过滤只用 `sed`。
6. **W11 包裹下的转储不进 tight**: 实现者不得把 env / printenv 备选并进 tight 拷贝 (22br / 22bs 钉); 这是对上一版原型行为的**反转** (原型曾使基线 docker / kubectl exec 转储接锚定 grep 由放变拦), 备选 B 见待复议 23。
7. **W8.3 `:641` 的改写约束**: 保持原串逐字节不变, 在其后用 `|` 并入名字组; 32 个基线备选各一条路径重放 (18j / 18k)。
8. **W12**: 同一单键子串多处出现全部替换; BLOCKED 文案的 `Command was:` 回显原命令文本 (25h)。
9. **新增验证项**: SC-32 32e (POSIX locale 腿, 无需环境变量); SC-34 (34a / 34b / 34c); W14 新时档 (f-hit) 与 (i3) (`timing.py --judge` 可自动给 PASS / FAIL); SC-26 26g 的标记词扩为 13 个; SC-28 28o (`secret-guard.sh` 头注释 `~100` 一句); Tasks 1.8 的对抗 review 清单扩为 12 + 14 类; Tasks 1.10 的验收模式含 32e。
10. **文本与流程**: Impact 新增 Layer 2 一句与关单评论的验证范围一句 (MINGW64 / macOS 未验证); 待复议新增 7.20 (产品级) 与 31 / 32。

## 4. 证据复跑记录

全部由脚本生成, 命令与产物在交付目录 `deliver/` (`writer-v5-proto/README.md` 说明用法); 实验目录 `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v5/`。

**探针定稿运行** (`python3 baseline_probe.py <树>/aria`, 实验目录里的 aria / standards 副本, 非 root, 带 `WPA_BASH32` 的运行同时设真 bash 3.2.57):

命令 (`<X>` = 实验目录, 经 `proto/runprobe.sh <标签> <树根> <spec 目录> <b32: 0|1>` 调用, 它先把 spec 目录快照到 `work/snap/<标签>/` 再在快照里跑; 环境 `HOME=<X>/home TMPDIR=<X>/tmp`): final_A / final_B / final_C = `WPA_BASH32=<X>/bash32/bash python3 baseline_probe.py <X>/base/aria`; final_N = 同上不带 `WPA_BASH32`; final_T = `WPA_BASH32=<X>/bash32/bash WPA_REQUIRE_ALL=1 python3 baseline_probe.py <X>/work/t5f/aria`; final_TN = 目标树不带任何环境变量。三个基线运行 (A / B / N) 与三个目标 / 对照运行 (T / TN / C) 各并发一批 (`proto/final_runs.sh stage1|stage2`)。

| 运行 | 对象 | rc | stdout sha256 前 16 位 | 字节 | stderr |
|---|---|---|---|---|---|
| final_A | 基线, `WPA_BASH32` | rc=0 | `526efaa2b5a9d52e` | 97972 | 0 字节 |
| final_B | 基线, `WPA_BASH32` (复现孪生) | rc=0 | `526efaa2b5a9d52e` | 97972 | 0 字节 |
| final_N | 基线, 不带 `WPA_BASH32` | rc=0 | `da4c5c185abea1ec` | 97946 | 0 字节 |
| final_T | 目标原型, `WPA_BASH32` + `WPA_REQUIRE_ALL=1` | rc=0 | `baf7c962e4e78392` | 95688 | 0 字节 |
| final_TN | 目标原型, 不带 `WPA_BASH32` | rc=0 | `cedf4efff40d6e67` | 95695 | 0 字节 |
| final_C | 基线, `WPA_BASH32`, 定稿 proposal + evidence 在场 | rc=0 | `526efaa2b5a9d52e` | 97972 | 0 字节 |

- stage 2 跑了三遍: 前两遍之后各为改准或补全 proposal 里几句措辞与坏实现点名而重新定稿 (最后一次是 SC-10 / SC-19 / SC-22 / SC-26 的「怎么会红」补点名与 Tasks 1.8 一处), 交付的是第三遍 (快照与交付文件逐字节相同); 第一遍与第三遍的 final_T stdout 逐字节相同: **是**, 前两遍的日志不入交付。
- final_A / final_B / final_C 逐字节相同: **是** (C 在定稿 proposal 与 evidence 就位后跑, 证明基线 stdout 与这两份文件的文字无关)。
- 基线类别计数 (final_A): baseline-failing 0/213, doc-sync 0/26, reverse-guard 79/79, allow-guard 70/70, known-limit 39/39, zero-regression 9/9; 基线形态 `holds`。目标 (final_T): baseline-failing 213/213, doc-sync 26/26, reverse-guard 79/79, allow-guard 70/70, known-limit 39/39, zero-regression 9/9; 目标形态 `holds`, 唯一未运行的行是设计上不执行的 30a。
- `baseline-evidence.md` 的代码块 = final_A 的 stdout 原样 (mk_evidence.py 断言逐字节一致); 不带 `WPA_BASH32` 的 final_N 与它只在 29h / 29i / 32c / 32d 四行与末尾三行不同。
- 与 proposal 的对账: `check_counts.py` / `xref_check.py` 输出在 `logs/check_counts.out`、`logs/xref_check.out`; `format_lint.py` 对三份文件的输出在 `logs/format_lint.out`; Rule #7 自扫 (`scan_all.py`, 基线与目标两个 `secret-scan.sh` 各以 Bash 输出与 Read 结果喂一遍, 对整个交付目录 119+ 个文件) 在 `logs/scan_all.out`, 0 个告警。

**变异 / 坏实现** (`run_final_campaign5.sh` + `docvariants5.py` + `build_mut_summary5.py` -> `logs/mut_summary_v5.txt`):

- Part A (本轮): 117 个 (含 25 个文档类), 112 个转红, 5 个转 0 行 (`ext_perentry` 是时档类: 功能行恒等, 由时档 (f) 抓到 13.3x / 9.7x; 4 个 `remote_env_split` 等价变异的理由重做并在 22bo+22br+22bs 上重新验证)。
- Part B1 (上一版的坏实现回归): 108 个重跑, 104 个保持全部转红行, 0 个丢行, 4 个上一版就是等价变异, 7 个因设计已不存在而被取代 (逐个点名并写替代者)。
- Part B2 (更早几版): 391 个重跑, 377 个保持, 0 个丢行, 14 个当时即等价。

**时档与成本** (原始输出 `logs/timing_main.txt` 等; Linux 6.17, 4 核共享主机; 同一次运行内交错取最小整进程 CPU 时间; `timing.py --judge` 对 W14 上界逐档判 PASS / FAIL):

- 目标原型: judge: 16 bounded tiers, 0 failed。关键比值: (f) Bash 1.67 / Read 1.53、(f0) 1.14 / 1.14、(f-hit) 2.01 / 2.01、(g) 1.42 / 2.06、(h) 1.21、(i) 1.24 / 1.30、(i3) 1.44 / 1.46 / 1.25 / 1.74 / 1.15。
- 坏实现: 手写阶段切分 (f-hit 64 处) 30.7x; 逐出现点重判 63.4x; 取值前缀删除 (i3) 28.8x; 无界 cli 前缀 3.4x; 无左边界 cli 10.7x; 无界 kv 4.3x; 每条一个 grep 13.3x; W10 余量二次写法 (g) 4.9x / 13.3x。
- 命令长度 x 出现点 (occ_cost.py, 64 处): 2 KB: 目标 1.7x / 手写阶段切分 7.6x / 逐出现点重判 55.0x; 8 KB: 1.9x / 24.7x / 64.8x。
- 其它自检: `fuzz_value_of.py` (17 个 tag 的 6017 个真实 span, bash 5.2 与 3.2.57 各一遍): 0 差异; `diff_ext_builtin.py`: 本设计 93 形态 0 分歧, 手写阶段切分的参考坏实现 19/93 分歧; `fuzz_ext_builtin.py` (随机命令): 2500 条中内建拦 1873 条、分歧 0, 手写阶段切分的参考坏实现 600 条中分歧 98; `readface_check.py`: 32 条路径各恰好命中一个基线备选; `refs_check.py`: 3-step wrong 0; `ere_battery.py` / `ere_claims.py`: 6 个新 pattern 的缩放比与 W2 引用的数字。

## 5. 执笔自报薄弱点

1. **34c 是探针里唯一带比值的行** (整进程 CPU 总量之比 <= 3.5, 交错取 3 次最小值): 实测约 2.0, 余量 1.75 倍, 且是 CPU 时间而非墙钟; 在极嘈杂主机上仍可能抖动。已缓解: 只判二值、不打印比值; 不放心可改为只留每进程 CPU 上限。
2. **19af 的「零分歧」是对有限形态表成立** (探针 73 个、独立电池 93 个、随机 2500 条): 「由构造一致」的论证成立的前提是替换不改变命令的引号 / 分隔结构; 条目本身含 shell 元字符时前提不成立 (已写进 W9 已知限制, 未钉行)。
3. **键名 / 参数名上界 (64 / 40) 是一个取舍**: 比上一版覆盖面窄 (10n / 10o 钉现状); 选它是为了线性, 上界数值本身没有数据支撑, 只是量级判断 (待复议 31 列备选)。
4. **W1 的 NUL 前提无端到端样本**: 平台是否以 `\u0000` 转义把 NUL 交给 hook 没验证; 若不是, N 视图空转, 这一段是无害的空操作 (Spec 已写明)。
5. **耗时回升与时档余量**: 180 KB 稠密 INI 的 Read 扫描, 上一版 proposal 写约 0.66 s, 本轮空闲主机上实测约 0.95 s (负载高时测到 1.2 s; 有界量词展开使 pattern 自动机变大), 仍在 5 s 超时内; (f) 档比值 1.67 / 1.53 超过 1.5 倍、靠 100 ms 地板 (绝对值 0.085 / 0.072 s 对上界 0.15 s) 才过, 与上一版同型; (i3-d) 档比值在 1.74-1.82 之间, 对原定 2.0 只有约 10% 余量, 所以我把 (i3) 上界定为 2.5 —— 这是我对验收参数的一个自作主张 (见请裁项)。
6. **回归覆盖靠重跑旧坏实现**: 设计已不存在的旧变体不再回归 —— 7 个 (6 个引号掩码类、1 个字符类) 与 29 个 `drop_extreader_*` (扩展的读取器表不再存在; 内建读取器表同样的删除是 `drop_reader:*`, 29 个都使 16q 与 19u 转红) —— 汇总里逐个点名并写了替代者; 若主控认为替代不充分, 请点名。
7. **proposal 增长约 30 KB** (184 -> 214 KB): 主要是 SC 条目的逐成员 / 逐形态说明与新增的两个 W 段落; 没有借返修扩大范围, 但体量使第 5 轮的逐字审阅更费力。
8. **研究笔记与已推送分支** (km/m6): 本轮不能写仓内文件, 笔记里的配方段落没动, 只做了 Spec 一侧的去量化与 7.20 登记。
9. **时档数字是单次主机上的测量** (4 核共享主机, 负载 1-2): 数值随主机而变, 判据是比值上界与活性断言, 不是数字本身。

## 6. 请裁项 (需要主控或 owner 的取舍)

1. **(产品级, 已入 7.20) 未修复旁路的披露范围**: Spec 一侧已去量化并登记; 研究笔记里对应两处的同样编辑、已推送分支的清理 (改写历史 / 删除远端分支) 不在我的权限内 (本轮不写仓内文件, 也不应做破坏性动作), 请 owner 裁 A (默认现状保留) / B (先修后披露) / C (披露规范成文)。主控「暂停推 GitHub」的自作主张请照主控记录列入 handoff 请复议。
2. **(技术级, 已按默认执行) W9 条目规则**: 含 ASCII 字母数字或任一非 ASCII 字节即有效 (采纳 ba/m1) 与剥 BOM (采纳 qa/m2); 备选: 纯非 ASCII 条目跳过 / 不剥 BOM (待复议 24)。
3. **(技术级) 簇 F 的 credit 取舍**: 默认 (转储后的锚定 grep / cut 放行, `grep -v x` 同样放行, 与基线 docker / kubectl 行一致); 备选 B 并入 tight (堵住「整份环境减一行」, 但把基线放行的日常核对改拦: 22br 的 44 个运行转红); 备选 C 收窄包裹 (待复议 23)。我认为默认更贴近「不降低既有检出、不新增未申报拦截」, 请主控确认。
4. **(技术级) W2 的上界 64 / 40** (待复议 31): 线性与覆盖面的折中, 数值是量级判断; 要更大上界只需改两个数字加两行 known-limit。
5. **(技术级, 我自作主张的验收参数) W14 时档**: (i3) 上界定 2.5 (原型 1.2-1.8, 坏实现 3.4x 起), (i3-b) 取 60 KB `-` 串、(i3-c) 取 100 KB 大写连续段 (基线自己对 300 KB 同类输入就要约 5 s CPU, 时档会「环境不合格」); 另给 `timing.py` 加了 `--judge` (回应 qa 的风险 2)。请确认这些参数。
6. **(技术级) SC-34 的判据口径** (待复议 32): 探针内用每进程 CPU 上限与整进程 CPU 总量比 (34c <= 3.5x), 不用墙钟; 代价约 25 秒。
7. **(技术级) 采纳了席位备注两条** (不属 finding 表): Impact 加 Layer 2 一句 (新拦截在无人值守运行里同样生效, `# guard:ack` 由执行方自己写) 与关单评论的验证范围一句 (未在 MINGW64 / macOS 验证, 三席都提了)。
8. **未采纳**: (1) post-ship 复验 Tasks 1.12 里加 NUL 腿 —— NUL 以 `\u0000` 到达 hook 的前提无端到端样本, 加了腿也只能记「未验证」, 不改; (2) 把 `timing.py` 的判据并进探针 —— 探针只做二值的线性判据 (SC-34), 比值判据留在 SC-30; (3) 给 W9 条目加 gawk 腿 —— 已消除对 awk 的依赖。
9. **Rule #10 自作主张清单** (请 owner 复议): 以上 2-7 条技术级取舍; 7 个旧变体与 29 个 `drop_extreader_*` 按「设计已不存在」移出回归并逐个写了替代者; `build_deliver5.py` 把 stage-1 的 proposal 快照相等断言放宽为「只要求探针相等」(proposal 文字不影响基线 stdout, 由 final_C 的逐字节相等证明); 没有以「变更小 / 性价比」为由跳过、降级或改序任何已启用的审计检查点。

## 7. 交付物 (`deliver/`, MANIFEST.sha256 共 123 个文件)

- `proposal.md` cedbdfce05575891 / 214093 字节; `baseline_probe.py` cf331b4aa264a863 / 222199; `baseline-evidence.md` b41e86d796bb583c / 104900; `dispositions.json` 2a66a7b83726efdc / 22533。
- `logs/` 探针定稿运行 stdout / rc / stderr 与各脚本输出; `writer-v5-proto/` 脚本、计划与汇总 (无树副本); `MANIFEST.sha256` 覆盖其余全部文件 (`sha256sum -c MANIFEST.sha256` 在 `deliver/` 内通过)。

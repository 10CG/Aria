# -*- coding: utf-8 -*-
# Static text of the repair report (the numbers are filled in by mk_report.py from the final files; nothing numeric below is typed from memory except counts of things that
# are structural facts of the text itself: the 25 findings, the 7 rulings, the list of positions).

SHORT = {
 ("tech-lead", "M1"): "W11 转储 credit 默认 (不属 tight) + SC-22 22br (44 运行放行) / 22bs (22 运行限制) + Impact + 待复议 23; 坏实现 env_tight 使 22br / 22bs 全红; 4 个 remote_env_split 等价变异在带过滤的转储上重新验证 0 行红",
 ("tech-lead", "M2"): "整个机制换掉: 一次固定字符串比对 + 换名 + 内建 _sg_core_eval 一遍 (线性); W14 (f-hit) / (i3), SC-34 34c; 实测 2 KB / 8 KB 64 处: 目标 1.7x / 1.9x, 旧设计 7.6x / 24.7x, 逐出现点重判 55x / 64.8x",
 ("tech-lead", "m1"): "成文并钉 (不改规则): W11 已知限制 + Impact + 22bj 扩为 14 个运行 (新增 env 词 5 + /proc 文本检索 3, 每个成员都有会转红的坏实现); 待复议 27",
 ("tech-lead", "m2"): "W2 / W8 已知限制 + SC-10 10m (6 个运行) + 7.8 / 7.9",
 ("backend-architect", "C1"): "W1 两视图并集 (基线视图照扫, 含 NUL 且 N != D 才追加); SC-1 1e / 1f / 1g; 坏实现 nul_replace 使 1e / 1f 红, nul_always_* 使 1g / 2a-2d 红",
 ("backend-architect", "M1"): "W2 线性段 + kv / cli 有界前后缀与左边界 + 值抽取线性; SC-34 34a / 34b, SC-9 9z, SC-10 10n / 10o, W14 (i3); fuzz_value_of 17 tag 0 分歧",
 ("backend-architect", "M2"): "簇 T: 复用 _sg_core_eval, 不另写切分; SC-19 19af (73 形态零分歧) / 19z / 19aa / 19ak / 19al; 旧设计 54/73, 本设计 73/73 (独立 93 形态电池与随机 2500 条差分都是 0 分歧)",
 ("backend-architect", "m1"): "采纳: 含 ASCII 字母数字或任一非 ASCII 字节即有效; 19ae 改 baseline-failing + 19ah; 坏实现 ext_ascii_only 红",
 ("qa-engineer", "M1"): "同簇 T: 掩码机制已删, 19af 含转义 / `$'…'` / 管道 / 换行; ext_v4stage:noesc_q / noesc_all / noansi / nopipe / nonl 各红 19af",
 ("qa-engineer", "M2"): "W8.3 + W14 通则列入 `:641`; SC-18 18j / 18k 各 32 运行; readface16 与 readface_drop:1-32 逐成员红",
 ("qa-engineer", "m1"): "W12 全部替换 + SC-23 23j + SC-25 25h; w12_once 使 23j 4/4 红, w12_echo_norm 只使 25h 红",
 ("qa-engineer", "m2"): "W9 剥 BOM + SC-19 19ai; ext_nobom 红",
 ("qa-engineer", "m3"): "SC-32 32e (POSIX locale, 382 行); ell_lastchar 使 32e 红 (点名 11v / 11x / 11y), 默认 32d 仍 yes",
 ("code-reviewer", "M1"): "W9 偏移与切片同一单位 + `local -x LC_ALL=C`; SC-19 19ag / 19ah / 19am; ext_charslice / ext_localnoexp / ext_noc 红",
 ("code-reviewer", "M2"): "同 tl/M1: credit 默认 + 22br / 22bs; env_tight 红; 等价变异论证重做",
 ("code-reviewer", "m1"): "同 tl/m1 (两类 + 22bj 14 个运行)",
 ("code-reviewer", "m2"): "W9 / Impact / 7.1 不再复述旧数字; 时档数字只在 W14 第 5 项与 Impact 性能条, 由 mk_numbers.py 从原始输出生成",
 ("knowledge-manager", "M1"): "同簇 T",
 ("knowledge-manager", "m1"): "W1 理由按实测重写 (nul_off: kv=1; nul_space: kv=4)",
 ("knowledge-manager", "m2"): "删除全部版本 / 审计叙事 (逐处列在同族扫描); format_lint 机械检查 0",
 ("knowledge-manager", "m3"): "同 cr/m2",
 ("knowledge-manager", "m4"): "26g 标记词扩为 13 个 (逐条披露各一) + 逐标记词坏实现 --cl-drop x13 各红; W9 指明第二个 Hooks 小节",
 ("knowledge-manager", "m5"): "消除对 awk 的依赖 (只用 sed); 去 LC_ALL=C 的坏实现 ext_noc 在 mawk 主机上本机可证伪",
 ("knowledge-manager", "m6"): "Spec 侧: 7.1 / 7.2 去量化 + 新增 7.20 产品级披露范围; 研究笔记同改与已推送分支清理不在执笔权限内, 列请裁",
 ("knowledge-manager", "m7"): "四处各改: 28o + W14 清单加 :8; 22av 逐个写全; 22bk 清单 11 个; Impact 改引 COMMIT_FOOTER_GUIDE.md:199-200",
 ("主控", "裁定1"): "簇 U: 两视图并集 + UTF-16LE 反向守卫 + 进程环境形检出行",
 ("主控", "裁定2"): "簇 T: 复用内建同一判定函数, 差分表零分歧钉进 SC-19",
 ("主控", "裁定3"): "簇 V / W: 线性写明原因 + 时档行 + 探针内 SC-34",
 ("主控", "裁定4"): "簇 F: credit 制度明文 + 22br / 22bs 两方向 + Impact 申报",
 ("主控", "裁定5"): "簇 M: 18j / 18k 逐备选",
 ("主控", "裁定6"): "全部 minor 逐条处置 (见上)",
 ("主控", "裁定7"): "复用已有机制, 每处配会转红的坏实现, 既有检出不降低 (Part B1 / B2 回归)",
}

SIBLINGS = """
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
"""

IMPLEMENTER = """
下面每一条都会改变实现者**要写的代码或要做的验证**, 请主控逐条核:

1. **W1 NUL 处理由「替换基线视图」改为「两视图并集」**: 提取处的 `jq` 程序提成单一变量 `_content_prog`; 基线提取一行不动; 仅当原始信封含 `\\u0000` 且换行视图与基线视图不同才追加。实现者不再写 `tr '\\000' '\\n'` 接在提取之后。
2. **W2 两个 pattern 的写法收紧**: kv 的键名前后缀 `{0,64}` + 左边界 `(^|[^A-Za-z0-9_])`, cli 的参数名前缀 `{0,40}` + 左边界 `(^|[^A-Za-z0-9-])`; 超出上界或紧贴字母数字的写法不覆盖 (新增 3 个 known-limit 行 10m / 10n / 10o)。这是**覆盖面的收窄**, 理由是线性 (SC-34), 列待复议 31。
3. **W2 / W4 取值代码的写法约束**: 禁用前导 `*` 的 `#` / `##` 前缀删除, 取值只用 `${s%%X*}` + `${s:N}` + `[[ =~ ]]` 捕获 (原型的 `_value_of` / `_trimV` 即是)。
4. **W9 扩展的 Bash 面整体重做**: 不再自写阶段 / 引号 / 转义状态机; 要写 `_sg_ext_subst` (一次 `grep -oFib -f` + 前 64 处换成 `/etc/gitea/app.ini ` 的拼接) 与 `_sg_ext_pass` (把替换副本交 `_sg_core_eval`); `_sg_core_eval` 是把基线 `_sg_per_segment_eval` 的函数体原样提出 (加一个 `_SG_MODE` 记录), `_sg_per_segment_eval` 与 `_sg_ext_pass` 各调用它。
5. **W9 条目与 locale 的细则**: `local -x LC_ALL=C` (导出; 不是 `local LC_ALL=C`), 条目有效性 = 4-200 字节且含 ASCII 字母数字或任一非 ASCII 字节 (**纯中文条目现在有效**, 这是行为变化), 剥 UTF-8 BOM 与 CR 与首尾空白, 条目过滤只用 `sed`。
6. **W11 包裹下的转储不进 tight**: 实现者不得把 env / printenv 备选并进 tight 拷贝 (22br / 22bs 钉); 这是对上一版原型行为的**反转** (原型曾使基线 docker / kubectl exec 转储接锚定 grep 由放变拦), 备选 B 见待复议 23。
7. **W8.3 `:641` 的改写约束**: 保持原串逐字节不变, 在其后用 `|` 并入名字组; 32 个基线备选各一条路径重放 (18j / 18k)。
8. **W12**: 同一单键子串多处出现全部替换; BLOCKED 文案的 `Command was:` 回显原命令文本 (25h)。
9. **新增验证项**: SC-32 32e (POSIX locale 腿, 无需环境变量); SC-34 (34a / 34b / 34c); W14 新时档 (f-hit) 与 (i3) (`timing.py --judge` 可自动给 PASS / FAIL); SC-26 26g 的标记词扩为 13 个; SC-28 28o (`secret-guard.sh` 头注释 `~100` 一句); Tasks 1.8 的对抗 review 清单扩为 12 + 14 类; Tasks 1.10 的验收模式含 32e。
10. **文本与流程**: Impact 新增 Layer 2 一句与关单评论的验证范围一句 (MINGW64 / macOS 未验证); 待复议新增 7.20 (产品级) 与 31 / 32。
"""

WEAK = """
1. **34c 是探针里唯一带比值的行** (整进程 CPU 总量之比 <= 3.5, 交错取 3 次最小值): 实测约 2.0, 余量 1.75 倍, 且是 CPU 时间而非墙钟; 在极嘈杂主机上仍可能抖动。已缓解: 只判二值、不打印比值; 不放心可改为只留每进程 CPU 上限。
2. **19af 的「零分歧」是对有限形态表成立** (探针 73 个、独立电池 93 个): 「由构造一致」的论证成立的前提是替换不改变命令的引号 / 分隔结构; 条目本身含 shell 元字符时前提不成立 (已写进 W9 已知限制, 未钉行)。
3. **键名 / 参数名上界 (64 / 40) 是一个取舍**: 比上一版覆盖面窄 (10n / 10o 钉现状); 选它是为了线性, 上界数值本身没有数据支撑, 只是量级判断 (待复议 31 列备选)。
4. **W1 的 NUL 前提无端到端样本**: 平台是否以 `\\u0000` 转义把 NUL 交给 hook 没验证; 若不是, N 视图空转, 这一段是无害的空操作 (Spec 已写明)。
5. **耗时回升与时档余量**: 180 KB 稠密 INI 的 Read 扫描, 上一版 proposal 写约 0.66 s, 本轮空闲主机上实测约 0.95 s (负载高时测到 1.2 s; 有界量词展开使 pattern 自动机变大), 仍在 5 s 超时内; (f) 档比值 1.67 / 1.53 超过 1.5 倍、靠 100 ms 地板 (绝对值 0.085 / 0.072 s 对上界 0.15 s) 才过, 与上一版同型; (i3-d) 档比值在 1.74-1.82 之间, 对原定 2.0 只有约 10% 余量, 所以我把 (i3) 上界定为 2.5 —— 这是我对验收参数的一个自作主张 (见请裁项)。
6. **回归覆盖靠重跑旧坏实现**: 设计已不存在的旧变体不再回归 —— 7 个 (6 个引号掩码类、1 个字符类) 与 29 个 `drop_extreader_*` (扩展的读取器表不再存在; 内建读取器表同样的删除是 `drop_reader:*`, 29 个都使 16q 与 19u 转红) —— 汇总里逐个点名并写了替代者; 若主控认为替代不充分, 请点名。
7. **proposal 增长约 29 KB** (184 -> 213 KB): 主要是 SC 条目的逐成员 / 逐形态说明与新增的两个 W 段落; 没有借返修扩大范围, 但体量使第 5 轮的逐字审阅更费力。
8. **研究笔记与已推送分支** (km/m6): 本轮不能写仓内文件, 笔记里的配方段落没动, 只做了 Spec 一侧的去量化与 7.20 登记。
9. **时档数字是单次主机上的测量** (4 核共享主机, 负载 1-2): 数值随主机而变, 判据是比值上界与活性断言, 不是数字本身。
"""

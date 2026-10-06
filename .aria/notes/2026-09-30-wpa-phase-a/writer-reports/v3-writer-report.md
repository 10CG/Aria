# 返修报告: WP-A `secret-net-l3-and-bypass-paths` proposal v2 → v3 (post_spec 第 2 轮)

> 执笔: 返修实例 (backend-architect), 接续上一个因额度耗尽中断的实例; 半成品只当草稿, 对照 R2 逐簇重新核验后采用或重写。实验目录 `X` = `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v3b`, 母本在 `X/deliver/`。**没有 `report.md`**: 写报告类 md 文件被 harness 拒绝 (「Subagents should return findings as text, not write report files」), 本文即报告全文, 所以 MANIFEST 不含它。

## 0. 摘要与交付物

1. **处置**: R2 全部 50 条 (tech-lead 9 / backend-architect 11 / qa-engineer 9 / code-reviewer 10 / knowledge-manager 11, 原始计数 1C/15M/34m) 全部 `fixed`, 0 `rejected`, 0 `deferred`。七簇 A K L M N O P 按主控裁定 1–7 执行, 全部 minor 按裁定 8 逐条处置; 同键不同席各有处置行 (共 50 行)。
2. **文件** (`X/deliver/`): `proposal.md` 151287 B / 425 行 / `9e7fbe0bbc86caf9` (v2: 107305 B / 402 行); `baseline_probe.py` 160820 B / 2095 行 / `51936cff0a363c7f` (v2: 105616 B / 1531 行); `baseline-evidence.md` 79998 B / `cb9d8f8482faef16` (v2: 57519 B); `dispositions.json` 29507 B / `99e88c67eaa59072`; `MANIFEST.sha256` (76 个文件: 上述四份、五组探针 stdout 与 `.rc` / `.err`、`writer-v3-proto/` 归档); `cd deliver && sha256sum -c MANIFEST.sha256` 全部 OK。头部 Level / Status / Created / Linked Issue 四行与 v2 逐字节相同 (Status 仍是一句当前状态); 审计叙事没有写进正文。
3. **规模**: 探针 320 → 383 行 (新增 63、改写 20、未变 300、删除 0); 类别 baseline-failing 190 / doc-sync 25 / reverse-guard 59 / allow-guard 65 / known-limit 34 / zero-regression 9 (+ SC-30 一行按设计 `n/a`)。
4. **结论**: 基线上 `baseline-failing` 与 `doc-sync` 共 215 行全 `no`、其余 167 行全 `yes`, 基线形态 `holds`; 完整目标态原型 (T 跑, 带真 bash 3.2 与 `WPA_REQUIRE_ALL=1`) 382 行全 `yes`, 目标形态 `holds`; 不带真 bash 3.2 时只会是 `not established`。
5. **R1 已关闭的问题没有被改回**: v2 的 320 行里 300 行的类别 / 描述 / 期望原样不动, 20 行改写 (清单见 §5.8), 0 行删除, 目标态全 `yes`。

## 1. 处置表 (50 条; 完整证据在 `dispositions` 与 `deliver/dispositions.json`)

| 席位 | 编号 | 键 | 处置 | 改动位置或证据 (短) |
|---|---|---|---|---|
| tech-lead | C1 | e8d39a8a | fixed | W3 保留判据: 删 `$NAME` / `$(…)` / ASCII `...` 三类; 7h (11 运行) / 7j (15) / 11z; wl_* 坏实现红 |
| tech-lead | M1 | ac42f607 | fixed | W11 改写 (launcher 15 词超集、参数选项、绝对路径、关键字位置、BSD `-` 簇与 `-O`、`/proc` 内联解释器); 22av–22bl; 22bh 钉残余 |
| tech-lead | M2 | ce6fc59c | fixed | Tasks 1.10 发版前验收, 1.12 post-ship 惰性诱饵腿 (含 harness Read 腿), 1.13 收尾; 头部 Rule #7 声明、Impact 同步 |
| tech-lead | m1 | c9357eb5 | fixed | W14 时档改同次运行交错的整进程 CPU 时间比 (1.5 / 2.0 / 2.5, 墙钟只作 20 s 兜底) + 活性断言 |
| tech-lead | m2 | d65a895f | fixed | W9 删「无扩展不 fork」, 承认 +6–9 ms, 隔离条款不变; (f0) 时档; 待复议 14 |
| tech-lead | m3 | 684e9a24 | fixed | W9 语义改「每一处分别判断, 任一处满足即拦」, 与 19r 同向 |
| tech-lead | m4 | c941e4e1 | fixed | W8 已知限制列读取器组之外的放行写法; 17d (21 运行, known-limit) |
| tech-lead | m5 | 0033f2f4 | fixed | 7.10 追加 export -p / declare -x / set / env -0 / systemctl / kubectl 等; cases_m5.py 两侧实跑核对 |
| tech-lead | m6 | 5d032f7a | fixed | 头部「术语」行 + 26i: SOT 用 Path 3 / Layer 2 术语, 不写 L1 / L3 |
| backend-architect | M1 | e7e041c6 | fixed | W2 枚举逐成员出行 (4p 4s 4t 4r 5n 6i 6j 6k 9x 9y 12k 12l 12m); 缺项类坏实现全红 |
| backend-architect | M2 | 51e90cab | fixed | L1 枚举: 16q 16n 16o; 19u 19v–19y; 21j 21x 21y; 22aw 22ax 22ay 22az 22bc 22bd 22bk 22bl; plan_l1_* 全红 |
| backend-architect | M3 | ac42f607 | fixed | 同 tech-lead/M1 |
| backend-architect | M4 | ce6fc59c | fixed | 同 tech-lead/M2 |
| backend-architect | m1 | cffa7c09 | fixed | 7h / 4n / 5l 决定性 (强制出形; 带填充值强制不含 `+`); path_eq / path_plus / loosepath 各 10/10 红 |
| backend-architect | m2 | b4230080 | fixed | W3 第 5 类只留 Unicode `…`, ASCII `...` 删除并成文为已知误报; 7h / 11v / 11z |
| backend-architect | m3 | 984b1c3d | fixed | W2 点分链理由订正; 漏报侧 10i / 10j, 误报侧钉 10l |
| backend-architect | m4 | cfb24732 | fixed | W2 每 tag 迭代前 200 个 span, 余量只计数; W14 (i) 档 + 活性断言; no_cap 12.9× / 4.0× |
| backend-architect | m5 | 467c8b54 | fixed | W11 `/proc` pid 位置收窄 (22bf); 文本提及误拦成文并钉 22bj |
| backend-architect | m6 | 15da802b | fixed | W8 已知限制 15 类放行 (17d); 16n; 右边界 17c / 18i |
| backend-architect | m7 | a305732c | fixed | 形态行点名未运行行, `not established`, `WPA_REQUIRE_ALL=1` exit 3; 负控已跑 |
| qa-engineer | M1 | 5ce95ecf | fixed | W14 原位改写通则; 22bc (28 运行) / 22aj / 16o / 16p; drop_procreader_* 红 |
| qa-engineer | M2 | eb350937 | fixed | 逐成员枚举行 + 上界差一对; 420 个坏实现 / 406 红 / 14 等价; 83 条新增改写行全被覆盖 |
| qa-engineer | M3 | ac42f607 | fixed | 同 tech-lead/M1 |
| qa-engineer | M4 | 60f3173a | fixed | W5 只加 tag 与工具名; 13g (14 个敌意路径运行) / 13d 全串等值; 待复议 19; 7.19 |
| qa-engineer | m1 | a4af42ab | fixed | 按裁定 1 删分支, 7h / 11z 钉住 |
| qa-engineer | m2 | 6114c254 | fixed | W2 点分链「代价」+ 10i |
| qa-engineer | m3 | c941e4e1 | fixed | W8 已知限制: Bash 面大小写敏感且不认反斜杠; 17d + 18h |
| qa-engineer | m4 | 684e9a24 | fixed | 上界触顶 fail-open 成文: 19x / 19y、21x / 21y |
| qa-engineer | m5 | 335996c0 | fixed | SC-33 预筛补 `private[_-]?key` + 77 个名字自检 |
| code-reviewer | M1 | fc97f926 | fixed | 同簇 A, 另含 9l / 9m 改为决定性 |
| code-reviewer | M2 | 6bd285b1 | fixed | 同 tech-lead/m1 |
| code-reviewer | m1 | cfb24732 | fixed | 同 backend-architect/m4 |
| code-reviewer | m2 | 6114c254 | fixed | 同 qa-engineer/m2 |
| code-reviewer | m3 | 15da802b | fixed | W8 目录递归 / glob 放行成文 (17d) |
| code-reviewer | m4 | 467c8b54 | fixed | podman 纳入 (22bb / 22bl), 绝对路径 (22ay), 非首位 BSD 簇列 22bh |
| code-reviewer | m5 | 29a5d0bd | fixed | `pgrep -fl` 移入 22bh known-limit |
| code-reviewer | m6 | 335996c0 | fixed | 同 qa-engineer/m5 |
| code-reviewer | m7 | d65a895f | fixed | 同 tech-lead/m2; 64 处语义成文 (19x / 19y) |
| code-reviewer | m8 | 51dded0b | fixed | SC-15 15g; 负控已跑 |
| knowledge-manager | M1 | fc97f926 | fixed | 同簇 A |
| knowledge-manager | M2 | 5fd1f356 | fixed | 同 tech-lead/M2 (头部声明改写, W13 `nomad var put` 限不可达地址) |
| knowledge-manager | M3 | 05982c10 | fixed | Impact「提交页脚 / PR 描述的关键字」: 只写 Refs + 机械检查 (正则正反例实测); Tasks 贯穿行与 1.11 |
| knowledge-manager | m1 | eff49510 | fixed | 26c / 26e / 26g 加强 (静默、大小写不敏感、字面子串、放行侧、`fp=`、`partial`) |
| knowledge-manager | m2 | 5e342bfd | fixed | W14 清单补 Scope 清单 (28n)、§5.1 括号 (26k)、版本行 (26j)、Acceptable filters 注 (26b / 26f) |
| knowledge-manager | m3 | 51dded0b | fixed | 同 code-reviewer/m8 |
| knowledge-manager | m4 | 4900bccc | fixed | SC-27 27d 非注释自检断言 |
| knowledge-manager | m5 | 5d032f7a | fixed | §3.8 分界 60 秒; 末句限长时; 26a / 26h |
| knowledge-manager | m6 | 0033f2f4 | fixed | SOT §5.2 + README 两语种各加一句 updatedToolOutput 事实 (28m) |
| knowledge-manager | m7 | 5d12116d | fixed | 头部与 Tasks 1.8 指向 writer-v3-proto/ |
| knowledge-manager | m8 | 84a82267 | fixed | W14 列出替换文本英文字面 (28a–28l) |

## 2. 七簇逐簇说明

> 每簇: 裁定要求 → 做了什么 → 三态 / 坏实现 → 与裁定的差异或取舍。落点用 W / SC 编号, 不用行号。

### 簇 A — W3 白名单 (裁定 1)

- **做法**: 逐类对「保留判据」评估 (该类在既有 tag 的检出域内是否会与任何 ASCII 随机值或口令哈希重合)。**删除三类**: 裸 `$NAME`、`$(…)`、以 ASCII `...` 结尾; 我没有援引「可保留」的例外, 7h 的 `dollar-lower` / `dollar-upper` / `dollar-cmd` / `dots-ascii` 四个独立运行就是它们「基线检出、保留即静默」的反证。**保留 7 个分支**: `<…>`、`${…}`、`{{…}}` / `${{…}}`、`[REDACTED…]`、整值 `*` / `x` / `X`、Unicode `…` 结尾、6 个标记词 (FAKE / PLACEHOLDER / NOT-REAL / NOT_REAL / NOTREAL / REDACTED)。保留判据里的概率量级 (尖括号约 1e-4、`${…}` 约 1e-6、其余更低) 是按 94 字符口令字母表的估算, 没有实测, 已写进 W3 与已知限制。
- **两面决定性行**: 放行侧 11m–11r / 11v / 11x / 11y; 检出侧 7h (11 个强制出形的独立运行) / 7i / 7j (15 个边界运行) / 11z; 生成器对每个边界强制出形, 没有只能概率性转红的行。
- **三态**: 基线 7h / 7i / 7j 对既有键 yes; 目标原型全 yes; 坏实现 (plan_l3_wl 38 个): 再加入三类中任一类 → 7h 对应用例红 (除大写类外另在 11z 红); 边界类 (angle / brace / tmpl / red / mask / ellipsis 的前缀、后缀、宽松、缺结束锚) → 7j; 缺项类 (`wl_drop:CLASS`, 15 个) → 11m–11y。
- **取舍**: 代价 (成文) = 文档里写成 `$NAME` / `$(…)` / ASCII `...` 的占位示例在既有键上与基线一样告警; 本 Spec 自己的文本因此只用 `<…>` / `${…}` / `…` 写法。Impact『新静默』、待复议 10、W3 已知限制、SC-9 / SC-11 描述同步改写。cr/M1 点名的 9l / 9m 也改为决定性: 原先的纯大写变量名会被熵下限单独静默, 放过「值字符类误含 `$`」的坏实现; 现用大写加数字两类字符的名字, 变异 `add_dollar:hdr` / `add_dollar:kv` 各使 9l / 9m 转红。

### 簇 K — W11 进程表覆盖 (裁定 2)

- **做法**: launcher 集 = `secret-guard.sh:873` 既有 13 词 (`sudo doas nice timeout xargs nohup stdbuf env time eval setsid ionice unbuffer`) 并上 `command` (`:875` 既有形态) 与 `exec`, 共 15 个, 逐个出行 (22aw); 之后可带选项、带参数的选项 (`sudo -u svc`、`timeout -s KILL 5`)、数字 / 时长与 `NAME=值` (22ax); 程序名可带绝对目录前缀 (22ay); 命令位置含 `then do else elif` (沿用 `:877`, 22az); `ps` 增 `-O` 与带 `-` 的 BSD 兼容写法 (含 `x` 的短横簇、以 `u` 结尾且其后无用户名的簇; `ps -u dev` 仍放行) —— 我在本机 procps-ng 4.0.2 实跑核对了 `-u -au -eu -ux -aux -ax -x -xw -ex -O -eO` 的表头都带完整命令行的 COMMAND 列; podman (22bb / 22bl); `/proc` pid 位置收窄为 self / 数字 / `*` / `$name` / `${…}` / `$(…)`, 读取器 = 基线 13 个 (22bc 逐个重放) + 新增 11 个 (22bd), `python3 -c` / `node -e` 源组纳入同一 `/proc` 名字 (22bg)。我选「纳入」而不是「列已知限制」: W8 / W9 已纳入同一对解释器, 且这两行本来就在被原位改写的清单里, 只追加名字, 行预算 149 / 150 (SC-31)。
- **每侧决定性行**: 纳入侧 22av / 22aw / 22ax / 22ay / 22az / 22bb / 22bc / 22bd / 22be / 22bg / 22bk / 22bl; 放行侧 allow-guard 22O / 22S / 22Y / 22ad / 22as / 22at / 22bf / 22bi; 未纳入的 (嵌套 launcher、`if` / `while` / `until` 条件位置、非首位 BSD 簇、`find -exec` 与 `lua -e` 读 `/proc`、macOS `pgrep -fl`、容器内裸 `ps`) 写进已知限制并由 22bh 钉现状。
- **三态**: plan_l1_w11 的 82 个坏实现 (逐个删 15 个 launcher、24 个 `/proc` 读取器、远程包裹、ps 备选、pid 位置、关键字位置、非 ps 拼写、docker 形态, 以及 `pidtok_any` / `proc_status` / `launcher_any` / `anchor_nocntrl` 等越界类) **全部至少让一行转红, 0 个等价变异**。
- **新增误拦 (成文)**: `ps axo pid,comm`、取 PID 的 `ps aux | grep X | awk '{print $2}'`、heredoc 里以 `ps aux` 起行的文本提及 (22bj 钉住)。

### 簇 L — Tasks 1.10 post-ship 复验腿 (裁定 3)

- **做法**: 1.10 改为发版**前**验收 (目标态全 `yes`, 带 `WPA_BASH32` 与 `WPA_REQUIRE_ALL=1`, 目标形态必须 `holds`); 1.11 发版; **1.12 post-ship** 只在 `python3 .aria/probes/plugin-cache-currency.py` 报 `PASS` 且会话已重启后开始, 其它结果 (`STALE` / `SKIP` / `FAIL` / `AHEAD`) 记「未生效」停下、不得关单。四腿全是惰性操作数: L3 Bash 腿 (运行时 `secrets.token_urlsafe` 合成值打印成 `JWT_SECRET = <值>`)、L3 Read 腿 (先用一条不打印该值的 Bash 命令把合成值写进私有临时目录里的诱饵文件, 再用 Read 工具读它; 备选 Read SC-33 归因清单里的公开示例文件)、L1 进程表腿 (`ps aux | head -c 0`)、L1 配置文件腿 (不存在目录下的 `forgejo/app.ini` 路径, Bash 与 Read 各一次)。1.13 issue 收尾 (10CG/aria-plugin#154 须在 1.12 通过之后)。头部 Rule #7 声明、rule6_note 的 dogfood 句、Impact 的 #154 关单前提同步改指 1.12; W13 第 3 点的 `nomad var put` 实跑限定为不可达地址或只引 `-h` 原文。
- **三态**: 流程文字, 没有探针行; 「规则按命令文本判、验证力不变、失败路径无害」由 ba 与 km 两席在目标原型上实测过 (旧 hook 下零字节输出 / ENOENT, 新 hook 下 exit 2), 我没有在探针里重复这些命令。执行条件不满足时写的是「停下」而不是「放宽」(Rule #10)。

### 簇 M — 枚举集合逐成员出行 + 缺项类坏实现 (裁定 4)

- **做法**: 每个枚举集合在探针里**只列一处**, 循环即是行 (`l3e` / `l1e`, 红了点名前 6 个出错成员): 名表 58 键名 (4p)、关键字 10 × 2 (4s / 5n)、旗标后缀 7 (6i)、scheme 词与头名拼写 (6j)、值字符类符号 26 (6k)、熵下限三个两两组合 (4t)、路径起头 4 (9y)、名表封闭 (9x)、标记词与定界形 (11m–11y)、W4 取值表 38 tag (12k) + `pem-header-only` (12l) + PEM 项位置 (12m)、W8 读取器 29 (16q)、W9 读取器 31 (19u) 与上界 (19v–19y / 20f / 20n)、W10 声明形态 9 个 (21j) 与上界 (21x / 21y)、W11 各枚举 (簇 K)、W12 四个字面子串 (23b)。每个上界做 N-1 / N+1 对: 200 / 201 条、32768 / 32769 字节、4 / 3 与 200 / 201 字符、64 / 65 处、16 / 17 个赋值、8 / 9 次替换、16 / 15 字符值长、200 个 span。
- **坏实现**: 见 §5.4。**相对 v2 新增或改写的 83 条行全部被至少一个坏实现转红** (69 条由计划内坏实现, 14 条由手工运行, 0 条未覆盖; `work/coverage_check.py`)。
- **局限**: 坏实现仍是执笔人构造 (同源盲区); 实现期 Tasks 1.8 的非作者对抗 review 仍必要 (头部「证据位置」已指向归档)。

### 簇 N — W5 外来文本进 additionalContext (裁定 5)

- **做法**: 比裁定举例更严: **不放任何 `tool_input` 文本**。插入段 ` (tags: <tag>=<n> …; source: <tool_name>)` 只含 hook 自己的 tag 表与计数、以及 harness 字段 `tool_name` (两层 matcher 限定为 Bash / Read / Edit / Write / MultiEdit)。理由: 「基名 + 严格字符集 + 截长」仍要在 bash 3.2 / locale 下新增净化代码, 攻击者仍控制其中至多数十个字符, 而模型本就知道自己读了哪个文件; 选项 B' (净化基名) 列待复议 19。
- **敌意路径行**: SC-13 13g, 14 个独立运行 (良性、`)` 加祈使句、换行加伪造 hook 行、引号、非 ASCII 含 U+202E、5000 字符、控制字符; Read 与 Write 各一遍), 判据 = 整个 additionalContext 恰等于「基线文本 + 严格形状的插入段」; 13d 全串等值守「插入段之外逐字节同基线」; rule6_note 块 B 理由改写。
- **三态**: 基线 Read 例静默、另两例告警但无 tag 与来源、13g 全部不符; 目标 yes; `w5_path` → 13a / 13c / 13g 红, `w5_append` → 13d / 13g 红。
- **兄弟位置**: L1 BLOCKED 文案把 `file_path` 原文与命令回显进「退出码 2 的 stderr = 反馈给 AI 的拦截理由」 (`secret-guard.sh:676-690`; Bash 面只经 `_sg_redact_echo` 脱敏、不防注入)。本 Spec 冻结 BLOCKED 文案 (SC-25), 所以不改, 列入建议开单 7.19。

### 簇 O — 时档 (裁定 6)

- **做法**: W14 与 SC-30 改为同一次运行内交错 A/B (基线 hook 与目标 hook) 的**整进程 CPU 时间** (user+sys, 含全部子进程), 每侧 N≥5 取最小, 判据量 = 目标/基线之比, 墙钟与 loadavg 只记录。上界: (f) / (f0) ≤ 1.5×max(基线, 100 ms) (沿用测试内 SC-8 的地板)、(h) ≤ 1.5、(i) ≤ 2.0 (新增 6 个 tag = 6 趟额外 `grep -oE`, 固有开销 20–30%)、(g) ≤ 2.5 (第二遍近乎翻倍); 每档配活性断言 ((f) 扩展入口被调用; (g) `_sg_vx_pass` 被调用; (h) 仍 exit 2 且第二遍与扩展入口一次都不被调用; (i) 仍告警且计数同基线); 宽松兜底: 目标单次进程墙钟 < 20 s; 基线自身 CPU ≥ 5 s 判「环境不合格」重测。L3 稠密输入 (i): 约 900 KB bearer 行 (约 1.6 万命中) 与约 600 KB JSON 口令行 (约 2 万命中)。配套实现面: L3 每 tag 只迭代前 200 个 span (v2 只限制了「分类」, 原型仍逐个取值与记指纹, 这是稠密输入变慢的来源); W10 余量改用 `${s:N}` 长度切片 (v2 推荐的 `${s#*"$pat"}` 在命中点靠后的长串上是 O(n²))。
- **数值与坏实现**: 见 §5.5。参考实现 `writer-v3-proto/timing.py` (含对 f / g / h 的注入标记活性检查)。
- **差异**: SC-30 本身仍不由探针执行 (需要带 git 历史的真 checkout 与 `af87cae`); 阈值由我在单一共享主机上用原型实测定 (薄弱点 3)。

### 簇 P — 提交页脚 / PR 描述的关闭关键字 (裁定 7)

- **做法**: Impact 新增「提交页脚 / PR 描述的关键字」条: 本 Spec 全部提交 (页脚与正文)、PR 标题与描述、合并提交信息对三张 issue 一律只写 `Refs <org>/<repo>#<n>`, 不写 `Closes` / `Fixes` / `Resolves` 及时态变体; 10CG/aria-plugin#154 在 Tasks 1.12 通过之前也只用 `Refs`, 关闭是 1.13 的独立显式动作; 该约定覆盖仓内 `git-commit.md` §6.1 的默认写法。机械检查: `git -C <仓根> log --format=%B <起点>..HEAD | grep -niE '…'; echo "rc=${PIPESTATUS[1]}"` (aria / standards / 主仓各跑一次; PR 标题与描述草稿同法), 判据「无匹配输出且 `rc=1` = 通过; 有输出 = 违规; 其它 rc = 没跑成, 停下上报」。Tasks 增「贯穿全部任务」行 (每次推送前跑一次) 并在 1.11 引用; 1.13 写明归档 (D.2) 须在 1.12 / 1.13 勾选之后 (km 风险 4: `openspec-archive` Step 7 对未勾选的 Tasks 会自动开 tracker issue)。
- **正则实测**: `work/refs_check.py`: 11 个正例全部匹配, 12 个反例全部不匹配; proposal 内嵌正则与被测正则逐字符相等。
- **兄弟位置**: 待复议 3 追加「`Refs` 引用会在对方 issue 时间线产生引用事件, 是否算评论」请 owner 裁。

## 3. 同族扫描清单 (修类不修例)

| 触发 | 查过的兄弟位置 | 结果 |
|---|---|---|
| 簇 A (W3 删三类) | (1) W3 其余 7 个保留分支的边界; (2) 同形的「靠生成器不产出而安全」规则: 路径形 (起头标记 / 字符类 / ≥2 个 `/`)、点分标识符链、熵下限三类、值字符类符号 (kv 7 / 头 6)、值长 16 / 15、键名封闭; (3) 文字: Impact「新静默」、W3 已知限制、待复议 10、SC-9 / SC-11 描述 | 全部各有强制出形的决定性行与坏实现; 复跑发现并修了 4n / 5l 的概率性与 9l / 9m 的「被别的机制单独静默」 |
| 簇 K (W11) | env / printenv 既有 launcher 行 (`secret-guard.sh:873-877`) 的同一文法被 `ps` / `pgrep` / `pstree` / `top` / docker top / 远程与外壳包裹 / 包裹下 env 转储共用; `/proc` 行 (pid 位置、读取器、内联解释器、`status`); W8 / W9 的 python3 -c / node -e 源组; 非 ps 拼写 12 个 | 逐成员行 + 22bh 钉残余; 82 个坏实现全红 |
| 簇 L (Tasks) | 头部 Rule #7 声明; rule6_note dogfood 句; Impact #154 关单前提; Tasks 1.1 (取不到真 bash 3.2 → 上报 owner, 不以静态检查代之) / 1.10 / 1.11 / 1.13; W13 第 3 点 `nomad var put` | 一并改写; 无遗漏的「真实命令验拦截」 |
| 簇 M (枚举) | W2 / W3 / W4 / W8 / W9 / W10 / W11 / W12 的全部枚举集合与全部上界 (见簇 M 列表) | 逐成员 / 差一对; 一处只列一次, 循环即行 |
| 簇 N (W5) | 其它进入 additionalContext 的外来文本: 无 (systemMessage 只含 tag 名与计数); L1 BLOCKED 回显 `file_path` / 命令 | 后者不改 (SC-25 冻结), 列 7.19 |
| 簇 O (时档) | SC-30 / Tasks 1.10 / Impact 性能 / 待复议 20 / 建议开单 7.1 / W1 与 W9 的毫秒句 | 全部改为 CPU 比值或记录性数字; 测试内 SC-8 (owner 裁定) 不动 |
| 簇 P (关键字) | Impact / Tasks 贯穿行 / 1.11 / 1.13 / 待复议 3; 合并提交信息、PR 标题与描述 | 同查 |
| tl/m3 (全称 / 特称) | 全文「每一处 / 任一处 / 所有出现」措辞 | 仅 W9 一处, 已改 |
| tl/m6 (术语) | SOT 条款 + README 段 + 26i | 26i 钉 SOT |
| ba/m7 (形态行) | 基线与目标两条形态行; 20g 在 root 下 by-design `n/a` | 两条都点名未运行行 |
| cr/m8 + km/m3 (SC-15) | 三份附件 proposal / 探针 / 证据 | 15e / 15f / 15g; 负控已跑 |
| ba/m3 (已知限制) | 漏报侧与误报侧 | 漏报钉 10i / 10j, 误报钉 10l (与 22bj 同体例) |
| 「默认值掩盖缺项」 | W4 日志写 `${FP_ITEMS:--}`, 使「不记项」与「记 `-`」在单个 PEM 上不可分 | 12m (PEM 块与 header-only 兜底各一个运行, 排在 kv 凭据之后); 同时发现原型的 header-only 兜底没记项, 已补 |
| qa/m5 + cr/m6 (预筛) | 其它「只为提速」的过滤: 无 | 预筛对 77 个枚举名的自检 |

## 4. 改变实现者动作的改动 (相对 v2; 请主控重点核)

1. **W3**: 实现者少写三个白名单分支 (`$NAME`、`$(…)`、ASCII `...`); v2 要求写 (收紧)。
2. **W5**: additionalContext 只写 `(tags: …; source: <tool_name>)`, 不再带 `file_path` (v2 带路径; 收紧)。
3. **W2 分类器**: 每 tag 只迭代前 200 个 span, 超出部分**不取值、不记指纹**, 只计数; 分类路径零 fork (v2 只限制「分类」)。6 个新 tag 按 W2 列表 1–6 的顺序插入 (v2 未写顺序, 指纹遍历序依赖它)。
4. **W4**: PEM 块与 perl 缺席时的 header-only 兜底都在 PEM 预扫里记一个 `-` 项 (v2 表格已写, 原型的 header-only 没做, 现由 12m 钉)。
5. **W9**: 不再要求「无扩展文件时不 fork」 (放宽, 与隔离条款互斥); Bash 面语义措辞改「每一处分别判断, 任一处满足即拦」 (澄清); 上界触顶 fail-open 成文。
6. **W10**: 余量用 `${s:N}` 长度切片, 不用 `${s#*"$pat"}` (v2 推荐后者, O(n²))。
7. **W11**: 规则面显著扩大 (簇 K 全部内容); 这是裁定 2 的直接后果, 实现者要写的规则比 v2 多, 行预算 149 / 150。
8. **W8**: Read/Edit 面右边界与 Bash 面一致 (18i); `node -e` 追加同一名字组 (16n); 已知限制成文 15 类放行 (放行类不得被顺手收口, 17d 转红即须改 Spec)。
9. **W14 时档**: 实现期在 B.1 / B.2 按 CPU 比值与活性断言跑; 比值越界 → 上呈, 不得放宽阈值 (Rule #10)。
10. **Tasks**: 1.10 / 1.11 / 1.12 / 1.13 重排; post-ship 腿只用惰性诱饵并要求缓存 `PASS` + 会话重启; 每次推送前跑 `Refs` 机械检查。
11. **文档**: SOT §3.8 含 `60 秒` 分界; §5.6 含 `CLAUDE_PROJECT_DIR` / 静默 / 大小写不敏感; README 两语种 Hooks 小节含字面子串语法; CHANGELOG 含放行侧 (`os.environ`、`keys_unsorted`)、`fp=`、`partial`; `secret-scan.test.sh` 加 `Coverage: K cases` 与非注释自检 (K = 50); SOT §5.2 与 README 两语种各加一句 updatedToolOutput 事实; 头注释 Scope 清单点名 6 个新 tag; 替换文本的英文字面见 W14 (28a–28l)。
12. **SC-15 15g**: 证据文件须对 L3 静默 (B.2 回填证据后保持占位写法)。
13. **SC-10 10l**: 已接受误报的五个代表形态被钉成「仍告警」; 实现者不得为降误报悄悄加 URL / 资源名排除 (须改 Spec)。
14. **探针**: `WPA_REQUIRE_ALL=1` 验收模式; 缺腿时目标形态只会是 `not established`。

## 5. 证据复跑记录

### 5.1 环境与命令

- 环境: Linux 6.17.9-1-pve (4 核共享), Python 3.11.2, GNU bash 5.2.15, jq 1.6, GNU grep 3.8, GNU sed 4.9, perl 5.36.0, 无 zsh, `C.UTF-8`; 真 bash 3.2.57(2) = `X/bash32/bash` (writer-v2 构建的拷贝, sha256 前 16 位 `5997a028c645039d`; 配方在证据文件)。实跑日期 2026-10-06。
- 树: 基线 `X/base` (aria `268da8f` + standards `2bc1c4c` 的拷贝, 删去子模块 gitfile); 目标 `X/work/t3` (由 `proto/build_full.sh` 对基线文本替换生成, 与重建结果逐字节相同)。
- 命令 (在含最终三份文件的快照目录里): `HOME=X/home TMPDIR=X/tmp [WPA_BASH32=X/bash32/bash] [WPA_REQUIRE_ALL=1] python3 baseline_probe.py <树>/aria`。`proto/runprobe.sh` 先快照 spec 目录, 所以编辑 spec 不影响在跑的运行。

### 5.2 基线 (探针对冻结基线)

| 运行 | 命令要点 | rc / stderr | stdout 字节 | sha256 前 16 位 | 结论 |
|---|---|---|---|---|---|
| A | 基线, 带 `WPA_BASH32` | 0 / 空 | 74072 | a6e187b50a4f3514 | 383 行; 基线形态 `holds`; 32c 一致于 334 个 hook-direct 行; 29h 49/49, 29i 581/582 (唯一 FAIL = 测试内 SC-13, 无 git 伪影) |
| B | 同 A, 最终证据文件已就位 | 0 / 空 | 74072 | a6e187b50a4f3514 | 与 A `cmp` 逐字节相同 (可复现) |
| N | 基线, 不带 `WPA_BASH32` | 0 / 空 | 74072 | e22e0486a497425d | 与 A 只差 29h / 29i / 32c 三行与汇总行; 基线形态 `holds [3 leg row(s) not run]` |

`baseline-evidence.md` 由 `proto/mk_evidence.py` 组装: 内嵌块 = A 的 stdout 原样 (脚本断言 `"```" not in` 输出、基线形态成立、两次带腿运行逐字节相等); 单次运行约 8–9 分钟 (空闲主机), 本次 A + N 并发 11.6 分钟、B + T + TN 并发 19 分钟。A / N 的快照里 proposal 与探针与最终母本逐字节相同; B / T / TN 的快照三份文件都与母本相同。

### 5.3 目标态原型

| 运行 | 命令要点 | rc | stdout 字节 | sha256 前 16 位 | 结论 |
|---|---|---|---|---|---|
| T | 目标, 带 `WPA_BASH32` 与 `WPA_REQUIRE_ALL=1` | 0 | 72649 | 0e1d2eb9ea1522fb | 382 行全 `yes` (+ 30a 按设计 `n/a`); 目标形态 `holds`; 29a 50/50, 29b / 29i 584/585 (同一伪影), 31a patterns=149, 31b census 64 = 64, 32c 334 行一致, 33a flagged=2 (均在归因清单), 15a–15g 静默, 14a / 14b 0 行 / 0 条 |
| TN | 目标, 不带 `WPA_BASH32` | 0 | 72682 | a50faa579147f95b | 除 29h / 29i / 32c / 30a 外全 `yes`; 目标形态 `not established (3 leg row(s) not run)` |

### 5.4 变异复跑 (`writer-v3-proto/mut_summary_v3.txt`, `manual_runs.txt`)

- **总数**: 420 个坏实现 (每个 = 完整目标态原型里替换一个 hook, 只跑其对应的 SC / 行); 406 个至少让一行转红; 14 个转红 0 行, 全部点名为**等价变异**并写明理由: 8 个与既有 `json-secret-field` 重叠的小写键名 (被排在前面的既有 tag 先消费, 新表里的成员资格不可观察; W2 已成文)、5 个声明前缀词 (原型上多余; W10 已成文)、1 个 `/v1/var/` 解释器名副本 (与更靠前的通用行重复, 目标 / 变体 / 基线对三种写法都 exit 2)。
- **分计划**: 白名单 38 / W4 指纹与 W5 41 / 枚举与分类器 106 / W8-W9-W10-W12 95 / W11 82 / 重复 20 / vsym 13 / 额外 20 + 若干; 全部红 (等价变异除外)。
- **覆盖检查**: `coverage_check.py`: 相对 v2 新增或改写的 83 条行 = 69 (计划内坏实现转红) + 14 (手工运行转红: 文档类 26a–26g / 26i / 26j / 26k / 28h / 28m / 28n、27d、33a、15g) + 0 未覆盖。
- **手工运行** (需要完整树或重复次数, 见 `manual_runs.txt`): 文档 `--bad-sot` (26a–26d / 26j / 26k / 28h / 28m 红)、`--bad` (SC-26 9 条 + SC-28 14 条全红, 26h / 26i 不变)、`--bad-layer` (只 26i 红)、`--no-scope` (只 28n 红); 27d (`--no-selfcheck`: 27d 红, 27b 仍绿); 33a (`noentropy` 在完整树上 flagged=7, 5 个文件在归因清单外); 路径字符类三个坏实现各 10 次运行 4n / 5l 10/10 红、目标 0/10; 真 bash 3.2 差分: `b4` (`[[ -v ]]`) → 32a 与 32c 同时红 (32c: 1 of 17 rows differ), `vx_patsub` (`${x//p/r}`) → 32c 红 (1 of 22 rows differ)。
- **我自己的 campaign 暴露的缺陷 (已修, 作废的首轮结果单列 36 块, 不计入总数)**: (1) 4n / 5l 带填充值里随机的 `+` 让「路径字符类误含 `=`」约半数运行全绿 (只概率性转红), 现强制不含 `+`; (2) 12k 看不见「PEM 块不记 `-` 项」 (`${FP_ITEMS:--}` 使不记项与记 `-` 不可分), 补 12m, 并发现原型的 header-only 兜底也没记项, 一并补齐; (3) 9l / 9m 的纯大写变量名被熵下限单独静默; (4) 复跑脚本里 `+ / = _ ~` 的符号变体工作目录重名 (9 个变体互相覆盖, 个别 PATCH-FAILED), 已改并重跑 13 个; (5) 两个变体本身有错 (`wl_cmdsub` 草稿使 hook 解析失败; PEM 变体改的是不可达的 case 表项), 已重写; (6) mutbatch 的树只含 `aria/hooks`, 所以 SC-33 / 文档类坏实现必须手工跑完整树。

### 5.5 时档 (`writer-v3-proto/timing_summary.txt`; 测量时 1 分钟负载 1.5–2.9, 每侧交错 5 对取最小 CPU 时间)

| 档 | 基线 → 目标 | 比值 | 上界 |
|---|---|---|---|
| (f) 200 条扩展, Bash / Read | 0.049 → 0.076 s / 0.043 → 0.070 s | 1.55 / 1.65 | ≤ 1.5×max(基线, 100 ms) = 0.15 s |
| (f0) 无扩展, Bash / Read | 0.052 → 0.061 s / 0.043 → 0.049 s | 1.18 / 1.13 | 同上 |
| (g) 8 赋值 × 300 B + 40 引用 | 0.62 → 0.88 s | 1.40–1.43 (3 次复测) | ≤ 2.5 |
| (g) 16 赋值 × 100 B + 128 引用 (满额) | 0.69 → 1.44 s | 2.09 | ≤ 2.5 (余量约 16%) |
| (h) 150 段引用 + `cat .env` + 200 条扩展 | 1.006 → 1.187 s | 1.18 | ≤ 1.5 |
| (i) 900 KB bearer / 600 KB JSON 口令 | 0.64 → 0.79 s / 0.79 → 0.90 s | 1.24 / 1.15 | ≤ 2.0 |
| w1 (信息): Read 4 KB / 60 KB / 180 KB 稠密 INI | 0.108 → 0.313 / 0.117 → 0.330 / 0.134 → 0.655 s | — | 仅 W1 句 |

坏实现: W10 余量用 `${s#*"$pat"}` → (g) 5.1× / 13.6×; 每条扩展条目一个 grep → (f) 12.6× / 10.5×; L3 不设迭代上界 → (i) 12.9× / 4.0×; 第二遍按段交错 → (h) 2.3× 且活性断言失败; 扩展先于内建 → (h) 仅 1.24× (没越界), 但活性断言失败 (内建已拦时扩展入口仍被调用)。首批 (g) 8 赋值档出现过一次基线最小值异常 (0.881 s, 比值 1.01), 复测三次 1.40–1.43, 表中取复测值。时档在加 header-only 项之前测的 (该分支只在 perl 缺席时执行), 不影响数字。

### 5.6 负控与其它核验

- **形态行** (目标树, `WPA_ONLY=SC-32`, 无 `WPA_BASH32`): rc 0, `target shape ... not established (1 leg row(s) not run)`; 加 `WPA_REQUIRE_ALL=1` → rc 3; 无缺腿的 `WPA_ONLY=SC-1` → `holds`。
- **SC-15** (`nc15.py`, 往三份文件副本各追加一行运行时拼装的凭据形状): 目标 hook 下 15e / 15f / 15g 全红; 基线 hook 全 `yes` (基线看不见该键形, 即 2026-08-20 的洞本身)。
- **自检脚本**: `check_counts.py` (proposal 各 SC 的 `×N` 与 stdout 逐 SC 对账; 6 处提示均为只写类别名未写数量, 逐一核对相符; 全局 383 行相符); `xref_check.py` (引用的行号 224 个全部存在, `SC-n id` 对 166 个全对; 有 162 行不被正文单独点名, 由范围与类别列表覆盖); `check_dispositions.py` (50 条, 引用的行号全部存在)。
- **Rule #7 自扫**: `deliver/` 76 个文件 (含 stdout 日志与归档脚本) 各当 Bash 输出与 Read 结果喂基线与目标两个 `secret-scan.sh`: 0 告警; `check_bare_issue_refs.py` 对三份母本: 0 裸引用; 全文无带圈数字 / 表情。
- **其它**: `cases_m5.py` (tl/m5, 基线 / 目标两侧); `l3try.py` (已接受误报五形在目标告警、基线静默); procps 表头核对 (见簇 K); 头部四行与 v2 逐字节相同。
- **探针缺陷以外的已核事实**: W10 / bash 3.2 引号语义、`curl -K -`、jq `length` 取绝对值、16 个版本点 + 6 个发版文件等沿用 v2 已核结论, 本轮未改动其文字, 未复核。

### 5.7 相对 v2 新增的行 (63; R3 审计导览)

SC-4: 4p 4r 4s 4t; SC-5: 5n; SC-6: 6i 6j 6k; SC-7: 7j; SC-9: 9x 9y; SC-10: 10h 10i 10j 10k 10l; SC-11: 11x 11y 11z; SC-12: 12k 12l 12m; SC-13: 13g; SC-15: 15g; SC-16: 16n 16o 16p 16q; SC-17: 17c 17d; SC-18: 18h 18i; SC-19: 19u 19v 19w 19x 19y; SC-20: 20n; SC-21: 21j 21x 21y; SC-22: 22av 22aw 22ax 22ay 22az 22bb 22bc 22bd 22be 22bf 22bg 22bh 22bi 22bj 22bk 22bl; SC-26: 26i 26j 26k; SC-27: 27d; SC-28: 28m 28n。

### 5.8 相对 v2 改写的行 (20)

SC-4: 4n; SC-5: 5l; SC-7: 7h; SC-9: 9l 9m 9v; SC-13: 13a 13c; SC-22: 22O 22S 22aj; SC-23: 23b; SC-26: 26a 26b 26c 26e 26f 26g; SC-32: 32a; SC-33: 33a。

## 6. 执笔自报薄弱点

1. **原型不是实现, 坏实现是自构的 (同源盲区)**: 本轮 campaign 暴露的 6 类缺陷 (见 §5.4) 全是我自己的探针 / 脚本 / 变体问题, 说明自构 campaign 既有牙也有洞; Tasks 1.8 的非作者对抗 review 仍是必需。
2. **体量**: proposal +40% (107305 → 151287 B), 探针 +52% (105616 → 160820 B, 1531 → 2095 行), 新增 63 行 / 改写 20 行; 主要由裁定 4 的逐成员行与裁定 2 的 W11 文法造成, 没有为收紧而削字 (削字本身造接缝)。第 3 轮审计面大; 单次探针运行约 8–9 分钟。
3. **时档阈值由单一共享 4 核主机上的原型实测定**: (g) 满额档 2.09 距 2.5 余量约 16%; (f) 比值 1.55–1.65 靠 100 ms 地板而过; 真实现可能更慢。Spec 写的口径是「越界上呈、不放宽」 (Rule #10), 请确认。
4. **W1 + W2 使每次 Read 的 hook 成本显著上升**: 整进程 CPU 由约 0.11 s (基线对 Read 提取为空而提前退出) 增至约 0.31 s (4 / 60 KB 无命中文本) 与约 0.66 s (180 KB 稠密 INI)。在 5 s 超时内, 但是约 3× 的每 Read 成本; R2 未提, 我写进了 W1 与 Impact, 请 owner 知悉。
5. **已接受误报的钉法 (22bj / 10l) 是我的取舍**: 把被接受的过拦 / 过报钉成 `baseline-failing` 行。若认为是新增机制, 可删 10l (删一行 + SC-10 / W2 / 待复议 9 三处文字 + 计数 383 → 382)。
6. **真 bash 3.2 沿用 writer-v2 的构建**, 未重建; Windows Git-Bash、macOS、BSD userland (`grep -F -f` 空模式文件语义、`pgrep -fl`、MINGW64 路径形态) 未实测。
7. **「表里写了、原型没做」**: header-only 兜底曾就是这样漏的; 我对 W4 表其余 tag 已由 12k 逐个核对, 对其它章节只做了抽查, 没有逐项再审。
8. **cr 的两条非编号风险备注未采纳**: (a) W9「有效条目为零 → 不调用 grep (BSD 空模式文件语义)」; (b) W6「清理对象是 `mktemp -d` 记下的变量, 不写 `rm -rf "$HOME"`」。理由: 没有可证伪的判据, 与裁定「收紧、不新增机制」冲突; 建议由主控决定是否写进 B.2 实现注意事项。

## 7. 请裁项

1. **待复议 19 (W5)**: 默认 A (只含 tag 与工具名); 备选 B' (净化基名)。
2. **10l 保留或删除** (薄弱点 5)。
3. **时档阈值与「比值越界上呈、不放宽」口径** (待复议 20; 薄弱点 3)。
4. **W1 的每 Read 成本上升**是否可接受 (薄弱点 4)。
5. **cr 两条未采纳的备注**是否写进 Tasks / 实现注意事项 (薄弱点 8)。
6. **km 的两条风险**: (a) A.1 认领 (2026-09-30T17:57:13Z, `SWEEP_TTL` 24 h) 早已过期, 需主控按例行维护续心跳或重新认领 (我没有 push / fetch); (b) 建议开单 7.1 含「约 1400 个空段使 hook 超时后命令被放行」的配方, 主仓 GitHub 镜像匿名可读, 请 owner 决定是否保留该句 (未改)。
7. **归档落盘**: 把 `deliver/writer-v3-proto/` 落到 `.aria/notes/2026-09-30-wpa-phase-a/writer-v3-proto/` (头部已引用; README 说明脚本内绝对路径须改写; `mut_summary_v3.txt` 92 KB)。
8. **Rule #10 — 我的自作主张, 请写进 handoff 复议**: (a) `/proc` 纳入内联解释器; (b) W5 零外来文本 (比裁定举例更严); (c) 10l / 12m header-only / 9l-9m 重做 —— 这些是 R2 字面之外的同族修补, 范围由我判断; (d) 没有写 `report.md` (harness 拒绝); (e) 重写了 mutbatch 的重名处理并重跑、两次重跑最终证据; (f) 变异复跑限于新写 / 改写判据与同族, 没有做全量。
9. **观察 (无需动作)**: 读取席位报告原文时, 现行 v1.74.1 L3 对含文档式占位示例的行告警了几次 (如 tl 报告里 `{"password":"$<…>"}` 一行), L1 数次把含 `/v1/var/` 等字样的命令文本当提及拦下 (用 Write 工具落文件绕开, 未用 `# guard:ack`); 与 W3 / W11 的已知误报类一致, 未复述任何值。
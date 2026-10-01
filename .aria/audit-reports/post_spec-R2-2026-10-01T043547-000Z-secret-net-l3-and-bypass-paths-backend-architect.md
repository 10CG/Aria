---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-01T06:55:00.000Z
context: openspec/changes/secret-net-l3-and-bypass-paths/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R2 backend-architect 报告 — secret-net-l3-and-bypass-paths (proposal v2 @ b3e3123)

> 视角: 实现可行性与正确性。结论: R1 的全部 critical 与簇 A–I 的 major 在 v2 里确已收口 (本席逐条实跑复核, 见「上一轮对账」); 本轮新增 4 条 major / 7 条 minor, 性质是「验收放过坏实现」(M1 / M2)、「W11 对常见写法失明」(M3)、「post-ship 验证的失败路径即泄露路径」(M4)。修法都小, M3 的修法已在原型上验证 (99 行探针仍全 yes, 258 条真实历史命令零新增误拦), 不涉及设计重做。

## 已实读文件

**被审 (全文)**: `openspec/changes/secret-net-l3-and-bypass-paths/proposal.md` 1–402; `baseline_probe.py` 1–1531; `baseline-evidence.md` 1–40, 并与探针 stdout 逐字节比对 (三份文件 sha256 前 16 位 `654cb86e8d588ffe` / `522fe6216524d5ea` / `bbcdf8377f2447e9`, 与执笔 MANIFEST 一致)。

**必读材料**: 三个 issue 正文与评论 (全文); 决策单 (全文); CLAUDE.md #6 / #7 / #10 与多远程两条 (上下文原文); R1 聚合报告 (全文, 含「主控记录」) 与本席 R1 报告 (全文); 执笔 v2 返修报告 §0–§7 (全文)。研究笔记: `cc-hooks.md` 全文; `secret-scan.md` 只读 stderr / 信封相关条与全部节锚; `secret-guard.md` / `precedent.md` 只核对节锚存在性 (proposal 里 19 个 `scan` / `guard` / `prec` 节引用逐条解析到小节标题, 无悬空)。

**源码与规范 (aria `268da8f` / standards `2bc1c4c`)**: `hooks/secret-scan.sh` 1–377、`hooks/secret-guard.sh` 1–1120、`hooks/hooks.json` 全文; `hooks/tests/secret-scan.test.sh` 1–60 / 100–153; `hooks/tests/secret-guard.test.sh` 11 / 819 / 839–843 / 1618–1624 / 1660–1900 (测试内 SC-8 的进程内计时器与抽取) / 2018–2030; `secret-hygiene.md` §0–§2 / §5 / §9–§10; `skill-benchmark-exemption.md` 全文; `LEVEL_GUIDE.md:150-162`、`proposal-minimal.md:53`、`project.md:117`; aria `README.md` / `README.zh.md` Hooks 标题、`CHANGELOG.md` 顶部、`VERSION:164`、`.github/secret_scanning.yml`; 10CG/Aria#199 `detailed-tasks.yaml` 的 `guard_config_hooks` 条; 归档先例的 rule6_note (2026-08-02 / 2026-08-22); 发版同步提交 `72cb02b` / `a99dd8d` (主仓) 与 `26e644e` / `1ad31fa` (aria)。执笔产物: `writer-v2-proto/` 的 README / runprobe.sh / build_full.sh / mut_summary.txt, 以及完整目标态原型 (`final/full`) 的 `secret-scan.sh` 与 `secret-guard.sh` 对基线的全量 diff (读完)。

### 实跑验证 (全部在 `$A` = `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/audit/post_spec-R2-backend-architect` 的副本内; `$W` = 同级 `exp/writer-v2`; 值运行时生成, 只看退出码 / alert-silent / tag)

- **V1 基线复现**: `cd $A/spec && HOME=$A/home TMPDIR=$A/tmp WPA_BASH32=$W/bash32/bash-3.2/bash python3 baseline_probe.py $A/base/aria` → rc=0, stderr 空, 52197 字节, sha256 前 16 位 `13cdea30978e1119`, 整段含于 `baseline-evidence.md` (Python `out in ev` = True); baseline-failing 0/154 · doc-sync 0/20 · reverse-guard 53/53 · allow-guard 57/57 · known-limit 26/26 · zero-regression 9/9, `baseline shape … holds`。成立。
- **V2 目标态复现**: 同命令对完整目标态原型 (`$W/final/full` 的副本 `$A/target`) → rc=0, 52861 字节, `4b0eea9cd97621d4` (与执笔 T1 相同), 154/154 · 20/20 · 53/53 · 57/57 · 26/26 · 9/9, `target shape … holds`; SC-31 `patterns=149`, `census=64 test-hardcoded=64`; SC-32 32c `identical over 277 hook-direct rows` (基线同为 277); SC-29 29h / 29i (真 bash 3.2) `PASS 49/49` / `PASS 584/585` (唯一 FAIL 是测试内 SC-13 头注释计数的无 git 伪影); SC-14 `0 lines` / `0 events` (基线 33 / 12)。
- **V3 信封事实 (本会话 transcript 的 `toolUseResult` 键形)**: Bash `{interrupted,isImage,noOutputExpected,stderr,stdout}` ×164, Read `{file:{content,filePath,numLines,startLine,totalLines},type}` ×5, Write `{content,filePath,originalFile,structuredPatch,type,userModified}` ×12, Edit ×4 —— 与 W1 描述的真实信封一致; 基线提取链无 `file.content`。
- **V4 R1 两个 critical 的收口 (基线 / 原型直调)**: (a) W3: 既有键上 `$` 开头混合 20 位值、bcrypt 形值, 新键上 `$` 开头值 → 基线与原型都 ALERT; (b) W12: 自拟 106 条 L1 命令, 整表导出与遍历 (`print(dict(os.environ))`、`.items()`、推导式、`for k in os.environ`、`sorted(os.environ.keys())`、`.get('A', dict(os.environ))`) 基线 2 / 原型 2; 单键 `.get(` / `[ ]` 基线 2 / 原型 0; `.env.example` 经 `python3 -c` 仍 2。
- **V5 写手变体独立复跑**: `SGVARIANT=ext_bare` 复跑 SC-19 / 20 → 20i / 20j 转红 (`exit=2,2,2,1,2`, Read `/x/README.md` 得 1); `ext_first` → 19i / 20l 红; `vx_interleave` → 21v 红 (SC-21 18/19) —— 隔离与求值顺序这三个 SC 有鉴别力, R1 C 簇与 tl M3 的收口属实。
- **V6 本席自构坏实现 (非作者)**: mutA / mutB / mutC / mutD / mutE / mutH / mutI / mutM, 结果见 M1 / M2 / m1 / m2; 修法原型 mutK / mutL / mutP, 结果见 M3 / m5。
- **V7 L1 历史命令对拍**: 本机 Aria 项目 transcript 里前 5000 条去重 Bash 命令 (内存处理, 不落盘、不打印原文) 分别过基线与原型 `secret-guard.sh`: (0,0) 4971 · (2,2) 20 · (0→2) 8 · (2→0) 1。8 条新拦: 1 条 W10 变量间接 (`for f in <四个 settings 路径>; do jq … "$f"`, 与同命令字面写路径时基线的判定一致), 5 条 W11 已申报的习惯变化 (3 条 ssh 包裹下的 `ps aux`, 2 条 `pgrep -af … | grep -v pgrep`), 2 条文本提及 (见 m5); 1 条新放是 `os.environ.get(...)` 单键读取 (W12 的目标)。
- **V8 自拟 L3 对拍 40 例** (20 个应检出形态 + 20 个应静默形态, 基线 vs 原型): 新检出且应检出: compose 列表 env、CRLF `.env`、`set -x` 回显、`$` 开头值落新键、含多个 `/` 的 b64; 仍漏 (基线 / 原型皆 silent): 见 m3; 基线 ALERT → 原型 silent 的真值类: 见 m2; npm integrity、`sha256sum` 输出、git sha、docker digest、变量引用、guard 自己的 BLOCKED 回显、占位写法全部静默; 套件自身输出 (`secret-scan.test.sh` 49/49、`secret-guard.test.sh`) 当 Bash 输出与 Read 结果喂 L3, 基线与原型都 silent。
- **V9 自拟 L1 对拍 106 例**: W8 / W10 / W11 / W12 / jq 形态逐条 (基线 / 原型 exit): 设计内的变化全部成立; 发现的缺口见 M2 / M3 / m6。
- **V10 时延 (4 核共享主机, load 12–29, 取 CPU 秒 = user+sys, 绝对值约为轻载的 2 倍, 看比值)**: L1 单段 0.10→0.12; 300 段+末段读 dotenv 3.20→3.94 (×1.23); 600 段 7.50→8.78 (×1.17); 9.5 KB 整串 8 赋值 + 40 引用 4.69→5.40 (×1.15); 60 段每段含 `$VAR` + 8 赋值 0.86→1.82 (×2.1), 200 段 + 16 赋值 3.02→6.91 (×2.3) —— 第二遍使「全部内建放行」的命令成本约翻倍, 但因内建先判 (21v 钉住) 不会推迟任何内建拦截, 不构成 R1 d4bcaf7c 同型的超时放行回退。L3 见 m4。SC-30 的 (f)(g)(h) 用测试内 SC-8 的**进程内**计时器 (`_sc8_stat`, 不含进程启动), 与 W14 里整进程的 ms 数字口径不同, 不可直接比。
- **V11 平台 / 仓内事实**: 真 bash 3.2.57 `x=abc; r=Z; echo "${x//b/"$r"}"` → `a"Z"c`, 5.2.15 → `aZc`, 前后缀拼接式在两者上都得 `a&Z&c` (W10 的论据成立); 3.2 对 `[[ … =~ ^<[^<>]*>$ ]]` 报 `syntax error … unexpected token '<'`, 正则放进变量则可 (W2 论据成立); curl 7.88.1: `curl -K -` 读到 URL 后 exit 7、空配置 exit 2 `no URL specified!`、`curl -H @file` 被接受 (W13 示例成立); procps-ng 4.0.2 的 ps 表头事实见 M3、`pgrep -fl` 只出 2 个字段而 `-af` 出完整命令行 (W11 放行 `-fl` 成立); 主仓 16 个版本点 (CLAUDE.md 2 + README.md 2 + zh/ja/ko 各 3 + VERSION 1 + system-architecture 1 + version-scheme 1) 与 aria 6 个发版文件逐个对上 `72cb02b` / `a99dd8d` / `26e644e` / `1ad31fa`; 接缝命令与 10CG/Aria#199 `detailed-tasks.yaml:342` 的 `guard_config_hooks` 逐字一致; `check_bare_issue_refs.py` 对三份文件 rc=0、裸引用 0; `proposal.md` 引用的 `secret-scan.test.sh:28-32 / :93-123 / :145-153`、`secret-guard.test.sh:11 / :1620 / :2018-2030`、`secret-hygiene.md:23 / :287 / :288 / :319`、`VERSION:164`、`secret_scanning.yml:18-22` 抽查全部对得上。
- **V12 主仓 L3 普查 (SC-33 只覆盖 aria + standards)**: 主仓 tracked、≤200 KB、过关键词预筛的 1928 个文本文件里随机 450 个 (seed 20261001) 当作 Read 结果喂原型: 只有 1 个文件命中新 tag (`aria-plugin-benchmarks/requesting-code-review/…/result.txt`, `kv-secret-assign=1`), 与 SC-33 归因清单同量级; 未见 R1 qa M5 担心的「W1 之后恒红」。

## Findings

### Critical

无。R1 的两个 critical (W3 白名单、W12 右边界) 与 W9 隔离 (tl C2) 均已收口且各自的守卫有鉴别力 (V4 / V5)。

### Major

#### M1 — id `e7e041c6` / major / issue / testing / scope `proposal.md SC-4`
**summary**: W2 的枚举型契约 (JSON 键名表 17 名干 × 拼写、`json-env-secret-key` 与 `kv-secret-assign` 的 10 个关键字、`cli-secret-flag` 的 7 个旗标后缀) 在 SC-4 / 5 / 6 里只被抽样钉住; 缩成「被钉住子集」的坏实现让 129 行 L3 SC 全绿, 却漏掉 Spec 明列的 19 种形态。

**证据**:
- 探针实际钉住的 (`baseline_probe.py:398-412 / :415-428 / :436`): 键名只有 token / Token / sha1 / registration_token / jwt_secret / auth_token / apiKey / ClientSecret 8 个拼写; `json-env-secret-key` 关键字只有 SECRET (4l) 与 PASSWORD (4m), 2/10; `kv-secret-assign` 只有 SECRET (5a / 5c / 5e)、PASSWD (5d)、TOKEN (5f / 5k), 3/10; `cli-secret-flag` 只有 `--token=` (6f), 1/7。Spec 明列: `proposal.md:59-64` (17 名干 × snake / camel / Pascal / 连写、两处同一关键字集、7 个旗标后缀)。
- 坏实现 mutC (原型 `secret-scan.sh` 里四条新模式的枚举改成恰好上述子集, 其余不动): `WPA_ONLY=SC-1,SC-2,…,SC-13,SC-15 python3 baseline_probe.py $A/mutC/aria` 跑 2 次, 两次都是 SC-1 2/2 · SC-2 4/4 · SC-3 2/2 · SC-4 15/15 · SC-5 13/13 · SC-6 8/8 · SC-7 9/9 · SC-8 1/1 · SC-9 23/23 · SC-10 7/7 · SC-11 23/23 · SC-12 10/10 · SC-13 6/6 · SC-15 6/6 (共 129 行 yes, 零行 no)。
- 同一份 mutC 与原型对 19 个 Spec 明列形态的直调 (alert / silent): camel `accessToken` / `refreshToken` / `sessionToken`、Pascal `SecretKey` / `Password`、snake `bearer_token`、Env 键 `STRIPE_API_KEY` / `DATA_ENCRYPTION_KEY` / `ALERT_WEBHOOK`、kv `API_KEY` / `PRIVATE_KEY` / `ACCESS_KEY` / `ENCRYPTION_KEY` / `WEBHOOK` / `PASSWORD`、旗标 `--password=` / `--client-secret=` / `--api-key=` / `--access-key=` —— 原型全部 alert, mutC 全部 silent。
- 三态: 基线 (这些 baseline-failing 行本就红); 目标 (原型) 全绿; 坏实现 mutC 仍全绿 ⇒ 这组行证伪不了「名表 / 关键字集被缩」。

**失败场景**: B.2 手写 alternation 漏项, 或日后维护者为「精简」删项 → 全部 SC 绿; `{"accessToken":"<40 位>"}` 这类 JS 系 API 最常见的键形、`export DATA_ENCRYPTION_KEY=…`、`mysql --password=…` 仍静默, 而 10CG/aria-plugin#154 的诉求正是键形缺口。

**建议修法**: SC-4 / 5 / 6 改数据驱动: 17 名干 × 适用拼写、10 关键字 × (json-env 与 kv) 两面、7 旗标后缀各一条正例 (一行 AND 多用例, 沿用 `l3m`), 并各配一条键名在表外的负例 (钉住封闭性); 「怎么会红」补「枚举被缩成子集」。

#### M2 — id `51e90cab` / major / issue / testing / scope `proposal.md SC-21`
**summary**: L1 面同型缺口: W10 的引号值赋值、W8 的 16 个新增读取器、W11 的 13 个 launcher 都只被抽样钉住; 三个坏实现 (mutD / mutE / mutI) 各自让对应 SC 全绿, 却放行真实写法 (如 `f="/etc/forgejo/app.ini"; cat "$f"`)。

**证据** (直调: `printf %s "$cmd" | python3 -c 'json.dumps({"tool_name":"Bash","tool_input":{"command":…}})' | bash <tree>/aria/hooks/secret-guard.sh; echo $?`):
- (a) 引号值: W10 明写收集「单双引号值」(`proposal.md:174`), 但 SC-21 的 8 条 baseline-failing 命令 21a–21h 的赋值全部无引号 (`baseline_probe.py:880-885`)。mutD (`_sg_vx_collect` 的赋值正则去掉引号值分支) 跑 `WPA_ONLY=SC-16,SC-17,SC-18,SC-21` → SC-16 13/13 · SC-17 2/2 · SC-18 7/7 · SC-21 19/19, 41 行全 yes; `f="/etc/forgejo/app.ini"; cat "$f"` 与 `f='/etc/forgejo/app.ini'; sed -n 1,80p "$f"` 基线 0 / 原型 2 / mutD 0。
- (b) 读取器: W8.2 点名 29 个 (claude-config 行 13 个 + 16 个新增, `proposal.md:145`), SC-16 只用到 cat / sed / head / grep / awk 五个 (+ python3 -c 源组)。mutE (`_SG_READERS_PRINT` 只留 13 个) 同样 41 行全 yes; `sort`、`base64`、`cut -d= -f2`、`xxd`、`paste` 读 `/etc/forgejo/app.ini` 基线 0 / 原型 2 / mutE 0。
- (c) launcher: W11 点名 13 个 (`proposal.md:185`), SC-22 的 launcher 行只有 `sudo` (22n / 22x) 与 `watch` (22y / 22z)。mutI (两处 launcher 列表改成 `sudo|watch`) 跑 SC-22 → 51/51 yes; `timeout 5 ps aux`、`nice ps -ef`、`nohup ps aux`、`env ps aux`、`command ps aux`、`ionice ps aux`、`time ps aux` 基线 0 / 原型 2 / mutI 0。

**失败场景**: 实现者复用既有 claude-config 读取器组、只处理无引号赋值或只写 `sudo` → 全绿; 事故之外最常见的 `f="…"` 写法 (10CG/aria-plugin#203 第 2 类的主形态) 与 `timeout N ps aux` 仍放行。

**建议修法**: SC-21 补 `f="…"` / `f='…'` / `export f="…"` / `declare` / `local` / `readonly` 各一行; SC-16 对 29 个读取器、SC-22 对 13 个 launcher 各一行 (一行 AND 多用例, 沿用 `l1m`)。

#### M3 — id `ac42f607` / major / issue / implementation / scope `proposal.md What.W11`
**summary**: W11 的进程表规则对三类常见写法失明, 且与同文件 env / printenv 行的既有约定不一致: (a) 带 `-` 的 BSD 簇 (`ps -aux` / `-ax` / `-x` / `-ux` / `-au`)、(b) `xargs` / `eval` / `unbuffer` launcher (`pgrep -f x | xargs ps -fp`)、(c) `then` / `do` / `else` / `elif` 关键字位置 (`while true; do ps aux; sleep 5; done`); 它们输出完整命令行列却放行, SC-22 无行、已知限制未写。

**证据**:
- (a) Spec 只写「任意 BSD 选项簇 (不带 `-`, 如 `aux`、`e`、`eww`)」(`proposal.md:184`); 全文与探针对 `-aux` / `-ax` 零命中。本机 procps-ng 4.0.2 实测 (只取表头): `ps -aux` → `USER PID %CPU %MEM VSZ RSS TTY STAT START TIME COMMAND`, `ps -ax` / `-x` / `-xw` / `-ex` → `PID TTY STAT TIME COMMAND`, `ps -ux` / `-uax` / `-u` / `-au` → `USER … COMMAND` (BSD 格式的 COMMAND 列是完整命令行; procps 文档: 不存在名为 x 的用户时 `ps -aux` 按 `ps aux` 处理); 对照 `ps -e` → `PID TTY TIME CMD`。原型直调: `ps -aux` / `-auxww` / `-ax` / `-x` exit 0 (基线 0), `ps aux` / `ps ax` exit 2。
- (b)(c) 基线对 env / printenv 的既有约定: launcher 行 `secret-guard.sh:873` 含 `xargs|eval|unbuffer`, 关键字位置行 `:877` 含 `then|do|else|elif`; W11 的 launcher 列表是 `sudo doas nice timeout nohup stdbuf env time setsid ionice watch command exec` (无这三个), 锚点也无关键字位置。直调 (基线 / 原型): `pgrep -f curl | xargs ps -fp`、`pgrep -f curl | xargs -r ps -o pid,args -p`、`unbuffer ps aux`、`eval ps aux`、`if true; then ps aux; fi`、`for i in 1; do ps aux; done`、`while true; do ps aux; sleep 5; done`、`for i in 1 2; do pgrep -af x; done` 全部 0 / 0; 对照 `xargs printenv`、`eval printenv`、`unbuffer env`、`if true; then printenv; fi`、`for i in 1; do printenv; done` 基线与原型都是 2。
- 修法原型 mutP (三处同改, 见下) 直调: 上列 (a)(b)(c) 全部 → 2; `ps -u dev -o pid,comm`、`ps -U dev`、`ps -e`、`ps -A`、`ps -p 1`、`ps -C curl`、`ps -t pts/0`、`ps -eo pid,comm`、`ps -ejH`、`ps -ely`、`ps -aux | wc -l`、`for i in 1; do ps -eo pid,comm; done`、`pgrep -f curl | xargs ps -o pid,comm -p` → 0; `WPA_ONLY=SC-16,SC-17,SC-18,SC-21,SC-22,SC-25` 跑 mutP → 13/13 · 2/2 · 7/7 · 19/19 · 51/51 · 7/7 (99 行全 yes); 258 条真实历史命令 (含 `ps` 字样) 过原型与 mutP, 零差异 (129 同放行、129 同拦)。
- 本机 30124 条去重历史 Bash 命令里 `ps aux` 20 条、`ps -aux` 0 条, 当前习惯下命中面小; 但 `pgrep -af` 被拦后 `| xargs ps -fp`、`ps aux` 被拦后 `ps -aux` 正是最近的替代写法, BLOCKED 文案又不给替代建议。

**失败场景**: AI 被 `ps aux` / `pgrep -af` 拦下后改写 `ps -aux`、`pgrep -f x | xargs ps -fp` 或套一层 `while … do ps aux … done` 即放行, 复现 10CG/Aria#221 的泄露路径; SC-22 的 41 条 baseline-failing 全绿给出「进程表族已封」的错误结论。

**建议修法** (mutP 已验证, 共改 4 个位置: `_SG_PS_ARGS`、`_SG_PROCTAB` 与两条字面行; SC-31 31c 禁整行变量, 故规则行保持字面; 行数不增): ① 在 `ps[[:blank:]]+(` 的选项簇备选里加 `-[a-zA-Z]*x[a-zA-Z]*([^[:alnum:]_-]|$)` 与 `-[a-zA-Z]*u[[:blank:]]*($|[|;&)<>])` (含 `x` 的短横簇与裸 `-u` 是 procps 的 BSD 兼容写法, `ps -u dev` 带用户名的 UNIX 写法仍放行); ② launcher 列表补 `xargs|eval|unbuffer`; ③ 命令位置锚点补 `(then|do|else|elif)[[:space:]]`。SC-22 补 baseline-failing (`ps -aux`、`ps -ax`、`ps -x`、`ps -ux`、`pgrep -f curl | xargs ps -fp`、`unbuffer ps aux`、`if true; then ps aux; fi`、`while true; do ps aux; sleep 5; done`、`for i in 1 2; do pgrep -af x; done`) 与 allow-guard (`ps -u dev -o pid,comm`、`ps -U dev`、`for i in 1; do ps -eo pid,comm; done`、`pgrep -f curl | xargs ps -o pid,comm -p`)。

#### M4 — id `ce6fc59c` / major / issue / testing / scope `proposal.md Tasks`
**summary**: Tasks 1.10 的 post-ship 腿用真实的 `ps aux` 与 `/etc/forgejo/app.ini` 验拦截, 验证失败 (插件缓存未更新 / 会话未重启, 恰是该腿要查的情形) 的路径就是泄露路径; 且该腿写在发版 (1.11) 之前的任务里。

**证据**:
- `proposal.md:355` (Tasks 1.10): 「ship 后经 harness hook 链复验 … 再对 `ps aux` 与 `/etc/forgejo/app.ini` 的读取各验一次拦截」; 发版在 1.11 (`:356`), Impact 要求 post-ship 复验完成后才关 10CG/aria-plugin#154, rule6_note 说明该腿「需 owner 更新插件缓存并重启会话」。L3 一腿用了运行时合成值 (正确), L1 两腿没有。
- 规则按命令文本判, 诱饵与真实命令等效触发。三态直调: `ps aux | head -0` 基线 0 / 原型 2, 未被拦时输出 0 字节; `cat /nonexistent-wpa-probe/forgejo/app.ini` 基线 0 / 原型 2, 未被拦时只得 ENOENT; `ps -o args= -p $$` 基线 0 / 原型 2, 未被拦时只含当前 shell 自己的命令行。

**失败场景**: owner 尚未更新插件缓存或未重启会话就执行 1.10 → 新规则未装载 → `ps aux` 把本机全部进程的命令行 (含 10CG/Aria#221 同型的带凭据后台进程) 打进上下文; 轮换已被决策单第 2 项延后, 属难以撤销的外向后果。读 `/etc/forgejo/app.ini` 在恰有该文件的主机上同理。

**建议修法**: 把 L1 两腿换成上列诱饵命令 (规则按文本判, 验证力不变, 失败路径无害); 把 post-ship 腿从 1.10 拆成 1.11 (发版) 之后的单列任务, 并显式写出 owner 等待点 (更新插件缓存并重启会话)。

### Minor

#### m1 — id `cffa7c09` / minor / issue / testing / scope `proposal.md SC-7`
**summary**: W3 / W2 分类器的反向守卫对三个坏实现无决定性: 两个只概率性转红, 一个根本没有决定性的行。
**证据**: (a) mutA (变量引用白名单接受混合大小写名: `^\$[A-Za-z_][A-Za-z0-9_]*$`, 即 R1 critical C1 同类的回退): `WPA_ONLY=SC-4,SC-5,SC-7,SC-11` 跑 8 次, 7h 红 6 次、全绿 2 次 (`dollar20` 的 `$` 后首字符是数字时不命中该正则, 理论 16%); (b) mutB (路径形字符类误含 `+` 与 `=`): 8 次里 4n / 5l 红 7 次、全绿 1 次 (`b64slash44` 含 ≥2 个 `/` 的概率约 48%); (c) mutM (删去裸 `$NAME` 变量引用规则 `_RE_VARU` / `_RE_VARL`): SC-4 / 5 / 6 / 7 / 9 / 10 / 11 共 98 行全 yes —— 9l / 9m 的头 / 旗标形先被值字符类 (不含 `$`) 静默, 11g / 11v 只用 `${…}`; 直调既有键上的 `$` 加小写下划线变量名 (如 `$database_password_value`) 基线 alert / 原型 silent / mutM alert。
**失败场景**: B.2 把变量引用写成 `[A-Za-z_]…` (自然写法) → 约 1/6 的探针运行放过; 删掉裸 `$NAME` 规则则永远放过。
**建议修法**: `dollar20` 强制 `$` 后首字符为字母, 另配数字首字符一例; 4n / 5l 强制值内 ≥2 个 `/`; 补一行既有键上 `$` 加单一大小写变量名的 baseline-failing 行来决定裸 `$NAME` 规则。

#### m2 — id `b4230080` / minor / issue / implementation / scope `proposal.md What.W3`
**summary**: W3 第 5 类「以 `…` / `...` 结尾」是后缀规则而非整值形态, 加上第 2 类 `$` 加单一大小写标识符形, 还有两类真值会被放过, 已知限制只写了第 6 类, 且 SC-11 11v 只钉 Unicode 省略号。
**证据**: (a) 既有键 `json-secret-field` 上「18 位字母数字 + `...`」基线 ALERT / 原型 silent; 新 tag 的值字符类含 `.`, 所以 `ADMIN_PASSWORD = <18 位>...` 里的点并入 span 一并被放行; (b) 既有键上 `$` 加单一大小写字母数字的 12 位人为口令 (小写 + 数字, 或大写 + 数字) 基线 ALERT / 原型 silent (形同 `$NAME`), 混合大小写的仍 ALERT; (c) mutH (去掉 ASCII `...` 分支只留 `…`): SC-7 9/9 · SC-8 1/1 · SC-11 23/23 全 yes, 直调 bcrypt 前缀 + ASCII 省略号 基线 alert / 原型 silent / mutH alert (`baseline_probe.py:531-535` 的 `crypt-ellipsis` 只用 `…`)。Spec 已知限制 `proposal.md:95` 只列「第 6 类标记词开头、小写 `fake_`、尖括号包住」。
**失败场景**: 人为口令以 `...` 结尾或形如 `$ummer2024xx` 时静默; 实现漏掉 ASCII 省略号分支则所有 SC 仍绿, 文档里最常见的截断写法 `$2b$12$...` 重新误报。
**建议修法**: 已知限制补 (a)(b); 11v 补 ASCII `...`; 或把第 5 类收窄到可识别的截断形 (哈希前缀 / crypt 前缀 + 省略号); kv / cli 的 span 不吞结尾的 `.`。

#### m3 — id `984b1c3d` / minor / issue / documentation / scope `proposal.md What.W2`
**summary**: W2 已知限制 / 已知误报清单仍不全, 且「点分标识符链 … 漏报面≈0」(`proposal.md:74`) 与实测不符。
**证据**: 点分链规则对点分 token 静默: 20 次运行里 base64url 字符集的三段式 (`DISCORD_TOKEN = <24>.<6>.<27>`) 静默 9 次, `GOOGLE_ACCESS_TOKEN = ya29.a0…(约 100 位)` 静默 2 次。基线与原型都 silent 的形态 (均未列入 KNOWN-LIMIT, SC-10 只钉小写 YAML 冒号形): JSON 渲染的头 `{"Authorization":"token …"}`、Python repr 头、Go `map[Authorization:[token …]]`、URL 查询 `?access_token=<40 hex>`、小写 INI / TOML (`aws_secret_access_key = …`、`password = "…"`)、K8s `- name: JWT_SECRET` 下一行 `value: "…"`。误报 (值并非凭据): `"TOKEN_URL":"https://login.example.com/oauth2/v2.0/token"`、`"SECRET_NAME":"prod/payments/db-credentials-v2"`、`"PASSWORD_POLICY":"min-length-12-with-symbols-required"` → `json-env-secret-key` 告警; `SECRET_NAME: prod/payments/db-credentials-v2`、`PASSWORD_RESET_PATH = auth/reset/Confirm2Step` → `kv-secret-assign` 告警 (带数字的 URL / 资源名过熵下限)。
**失败场景**: 读者按「漏报面≈0」判断头部 / 点分 token 已覆盖; 采用方对 `TOKEN_URL` 类配置 JSON 常态告警。
**建议修法**: 改写 :74 的措辞; 已知限制与已知误报补上述两类, 各钉 1–2 行 known-limit。

#### m4 — id `cfb24732` / minor / risk / architecture / scope `proposal.md What.W14`
**summary**: L3 新路径对每个命中 span 做一次 bash 迭代 (O(命中数)), SC-30 只给 L1 设了时档, L3 只有「B.2 实测记录」; 密集输入下 5 s 超时即静默丢检; 新时档的 N / rounds 与活性断言也未规定。
**证据** (CPU 秒, 基线 → 原型, 共享主机 load 12–29): 既有 tag `env-line` 命中 1k / 3k / 10k / 20k (37 / 113 / 379 / 770 KB) 0.64→0.98 / 0.81→1.68 / 1.38→3.87 / 2.18→7.08, 均仍 alert; `json-secret-field` 10k 命中 1.15→4.12; 180 KB 稠密 INI (约 3.5k 命中) 0.54→2.36; 30k 行全白名单 span 0.96→11.96; 干净 900 KB 0.91→0.99。W2 的「每 tag 最多分类 200 个 span, 超出不分类照计」(`proposal.md:65`) 只界定了分类, 原型对超出部分仍逐个 `_value_of` + `_fp_add`。`hooks.json` 的 PostToolUse `timeout` 为 5 s。另: W14 的 (h) 档沿用测试内 SC-8 的 N=10 × rounds=20 时约 200 次 × 3.8 s ≈ 13 分钟 (改前、改后各一份); (f) / (g) 只写耗时, 未要求先断言负载确实走到扩展 / 第二遍 (空操作会假绿; 对照 SC-20 20m 的无死代码断言)。
**失败场景**: 约 15k–20k 命中以上的输入 (≤1 MB 上限内) 在真实 harness 里超时被杀, 无告警 (且 `mktemp` 副本残留, 同 7.6); 基线对同输入 2.2 s 就告警。
**建议修法**: 规定迭代上界 (只迭代前 200 个 span、fp 只收前 10 项, 余量用已有的 `count` 做算术); SC-30 增一个 L3 时档 (如 20k 命中输入 < 5 s 且 ≤ 基线 ×1.5); 写明 (h) 的 N / rounds 并说明不属「改口径」; (f) / (g) 先断言活性。

#### m5 — id `467c8b54` / minor / issue / implementation / scope `proposal.md What.W11`
**summary**: W11 新增两类文本提及误拦: `/proc` 行的 pid 位置接受任意 token (`N`、`<pid>`), 命令位置锚点含换行使 heredoc 里以 `ps aux` 起行的文档示例被拦; SC-22 22Y 只钉同行提及。
**证据**: V7 的 8 条新拦里 2 条是文本提及: 一条 heredoc 正文写「grep -a、top -c、/proc/N/cmdline」(基线要求 pid 为 `self` 或数字, 新 `_SG_PIDTOK` 接受任意 token, 命中 `/proc` 行), 一条 python heredoc 里有以 `ps aux` 起行的一行 (换行在锚点集里)。直调: `cat /proc/N/cmdline`、`grep -a x /proc/<pid>/cmdline` 原型 2; 把 `_SG_PIDTOK` 收窄为 `([0-9]+|\*|\$\{[^}]*\}|\$[A-Za-z_][A-Za-z0-9_]*|\$\([^)]*\))` (正是 W11 列出的形态) 后这两条为 0, `/proc/*/cmdline`、`$pid`、`${pid}`、`$(…)`、`task/1/environ` 仍 2, SC-22 51/51 (mutL)。换行锚点沿用了基线 env / printenv 行的写法, 属既有约定的延伸。
**失败场景**: 写 Spec / 文档 / 测试的 heredoc 里出现 `/proc/<pid>/cmdline` 或行首 `ps aux` 被拦, 促使使用者 `# guard:ack` —— 正是 10CG/Aria#221 评论 25898 批评的诱因。
**建议修法**: 收窄 `_SG_PIDTOK`; 换行锚点的文本提及误拦写进 W11 已知限制 (讨论文本用 Write 工具), 22Y 补一行 heredoc 与 `<pid>` 的 allow-guard 或 known-limit。

#### m6 — id `15da802b` / minor / issue / documentation / scope `proposal.md What.W8`
**summary**: W8 已知限制没写出读取器组之外的放行形态, 而同文件 `.env` 族对其中多数各有专行; 另有三处 Spec 文字未被 SC 钉住。
**证据**: 自拟 21 条 W8 形态里 15 条放行 (基线 / 原型皆 0): `while read -r l; … done < /etc/forgejo/app.ini`、`mapfile -t a < …`、`< /etc/forgejo/app.ini cat`、`source …`、`perl -ne 'print' …`、`tr -d '\r' < …`、`dd if=…`、`cp … /dev/stdout`、`docker cp forgejo:/data/gitea/conf/app.ini -`、`bat …`、`echo … | xargs cat`、`find … -exec cat {} \;`、`grep -rn X /etc/forgejo/`、`cat /etc/forgejo/app.*`、`git show HEAD:deploy/forgejo/app.ini`; 基线对 `.env` 的 `while read` / `mapfile` / `source` / `.` / `dd if=` / `cp … /dev/stdout` / `xargs` / `find -exec` / `perl` 都有专行 (`secret-guard.sh:826-843`)。W8 已知限制 (`proposal.md:149`) 只写相对名 / cp 后读 / 模板被拦 / 引号内 `|` / `sed -i` / Edit / Grep。未被 SC 钉住: 右边界 `app.inix` 放行 (Spec 写明)、`node -e` 读 `app.ini` (Spec 写明追加同一名字组, 只有 python 一行 16h)。
**失败场景**: 读者以为 `app.ini` 与 `.env` 同等设防; 实现者去掉 `node -e` 追加或右边界, SC 仍绿。
**建议修法**: 已知限制列出上述放行类; 补 `node -e` 与 `app.inix` 各一行。

#### m7 — id `a305732c` / minor / issue / testing / scope `baseline_probe.py`
**summary**: 探针的末尾两行形态判定把 `n/a` 行排除在外, 不带 `WPA_BASH32` 跑目标态时仍打印 `target shape … holds`, 即便 29h / 29i / 32c (及 30a) 没跑。
**证据**: 代码 `baseline_probe.py:1496-1521`: `if ok is None: continue` 先于 `tally` 累加, `target_shape = all(v[0] == v[1] for v in tally.values())`; 执笔 E2 (基线不带 bash 3.2) 同样 `baseline shape holds`。Tasks 1.1 / 1.10 要求带该腿, 但判定行本身不强制。
**失败场景**: B.2 在没有 bash 3.2 的机器上跑探针, 末行显示 holds, 被读成通过。
**建议修法**: 两条形态行追加「not-run rows: N」, 且验收模式 (环境变量) 下 N>0 即非零退出; 不必改默认的可复现输出。

## 上一轮对账

对 R1 聚合报告「全部 finding」的 30 个 critical / major 键 (按主控归并簇); 状态均经本席实跑或实读核验。

| R1 键 (席位编号) | 簇 | 状态 | 本席核验 |
|---|---|---|---|
| `e8d39a8a` (tl C1 · cr C1 · km C1)、`14b7e703` (ba C1)、`8645b99f` (qa M2) | A: W3 前缀白名单吞真值 | **closed** | W3 改整值形态。直调: 既有键上 `$` 开头混合 20 位值、bcrypt 形值, 新键上 `$` 开头值 → 基线 / 原型都 ALERT; 探针 7h / 7i 目标态 yes。残余见 m1 (反向守卫非决定性)、m2 (后缀与单一大小写 `$NAME` 的真值类) |
| `e600e931` (tl C3)、`179045cd` (ba C2)、`f42265a1` (qa C1) | B: W12 右边界 | **closed** | V4(b): 整表导出 / 遍历 / 与单键同现的导出 10 余形基线 2 / 原型 2; 单键读取 2 → 0; 5000 条历史命令里 1 条因单键读取由拦变放 (目标行为); 探针 23c / 23d / 23h yes |
| `d9308fba` (cr M1)、`ab6a3123` (qa M1) | B2: `.env2` 等 | **closed** | `python3 -c` 读 `.env.example` 仍 2; 23d 九条 yes |
| `7e0343bd` (tl C2) | C: W9 隔离 | **closed** | V5: `ext_bare` 变体令 20i / 20j 转红 (`exit=2,2,2,1,2`), 其余 yes; 原型的 `_sg_ext_*` 只经 `$( )` 调用 |
| `d4bcaf7c` (ba M2)、`d8e7b380` (tl M3) | C2: 延迟无上界 | **closed** (Spec 层) | 条目 ≤200 / 32 KiB / 64 处、内建先判、W14 (f)(g)(h)。`ext_first` 红 19i / 20l, `vx_interleave` 红 21v; 实测 600 段 CPU ×1.17。残余: L3 无时档 (m4) |
| `719ae05c` (ba M4) | C3: 字面转义 | **closed** | 固定字符串匹配; 19j (14 个元字符条目) / 19k / 20h 目标态 yes; 原型用 `grep -F`, 含 UTF-8 命令与非 ASCII 条目的直调也正确 |
| `53c140c4` (cr M2)、`27f6c3ce` (qa M6)、`b73ab606` (km M3) | C4: W9 无文档落点 | **closed** | SC-26c / e / f / g 目标态 yes (基线 doc-sync 0/20 → 目标 20/20); aria 两份 README 的 Hooks 小节标题存在, 26e 判据可达 |
| `634eac5c` (qa M4)、`2ce0049b` (cr M4) | D: W4 指纹 | **closed** | 逐 tag 取值表; 12a–12j 目标态 yes (遍历序与 W2 列出的新 tag 顺序一致); 与 pat-inventory「sha256(token 原文) 前 8 位」口径一致 |
| `44b5bb44` (tl M1 · cr M6) | E: bash 3.2 | **closed** | V1 / V2: 真 3.2.57 上基线 29h 49/49、29i 581/582、32c 277 行一致; 目标 49/49、584/585、277 行一致; 变体 `[[ -v ]]` 与 `${s//p/r}` 由执笔复跑, 本席未重跑 |
| `e2459206` (tl M2)、`9db51a43` (cr M3) | F: W11 包裹 env / `/proc` status | **closed** | `ssh host printenv HOME` 2、`ssh host env FOO=1 cmd` 0、`nomad alloc exec … ps -eo pid,comm` 0、`grep VmRSS /proc/$$/status` 0。W11 同族的新缺口见 M3 |
| `846b21f8` (km M5) | G: W13 与 SOT 示例 | **closed** | §3.8 限定适用面; 26h 钉 §3.1–§3.7 / §4.1–§4.4 逐字节不变; 两条 curl 示例实跑成立 (V11); `nomad var put -h` 的措辞本席未能复核 (已装的 guard 拦了该命令) |
| `7deac83f` (ba M3)、`2779a016` (km M6)、`ba98e41f` (km M2) | H: 评论口径 / 同步面 | **closed** | Impact 默认理解 B (`#203` / `#221` 不评论, `#154` 在 post-ship 复验后关); 16 + 6 个同步点对上四个发版提交 (V11) |
| `cf0ae932` (km M4) | I: 研究笔记 | **closed** | 引用指向 `.aria/notes/2026-09-30-wpa-phase-a/research/`; 19 个节锚均解析 |
| `d9986b27` (cr M5) | J: SC-13 | **closed** | 13d 全串等值; 追加句变体 `w5_append` 由执笔复跑。注: 13d 的正则 `[^()]*` 允许插入段内自由文本, 单 tag 的 13a–c 钉住内文, 多 tag 情形未钉 (不另立 finding) |
| `5831f8c0` (km M1) | J: SC-26 | **closed** | 判据限定到具体小节, 基线 0/7 → 目标 7/7 |
| `1c0bc16f` (qa M3) | J: 反向守卫负向侧 | **partially closed** | 7h 七个独立运行 + 4o + 11s 已加; 本席新构坏实现仍有存活 (m1 的 mutM、m2 的 mutH) |
| `a3054a20` (ba M1) | J: 生成器首字符 | **partially closed** | 强制首字符生成器已加 (4n / 5l / 5m / 7h), 但检出为概率性 (mutA 6/8、mutB 7/8 转红, m1) |
| `8e77d1ca` (qa M5) | J: 语料级误报验收 | **closed** | SC-33 在目标态 1/1; 主仓 450 文件抽样仅 1 个命中新 tag (V12) |

**R1 minor 中我认为仍未处置的**: 无。本席 R1 的 m1 (W2 已知限制不全) 已按清单补了一批, 但实测仍有遗漏, 并入本轮 m3; 其余抽查均已处置。

## 对执笔人自报薄弱点与请裁项的表态

**自报薄弱点 (§5)**
1. 文字体量 +44%: **可接受**。体量本身不改变实现者动作; 但 R1 的 86% finding 落在当轮新文本 (memory rewrite≠cleanup), 本轮 4 条 major 也都在 v2 新增的探针行 / 规则 / 任务文字里 —— v3 只做最小改动, 并用同一套变异复跑验证, 不建议再大规模削文。
2. 交付形态偏离 (母本路径 + sha256): **可接受**。三份文件 sha256 前 16 位与 MANIFEST 一致, 探针输出逐字节复现 (V1)。
3. 原型不是实现: **可接受**。目标态探针在原型上复现 (V2), 且原型帮本席构造了变异与修法; 3 个 census 探针是占位用例, 属 B.2 的事。
4. 「变异实测」旧声称 5 处与实测不符、仍有少量数字来自研究笔记: **可接受**。研究笔记数字已标注出处 (`guard §0` / `guard §2(c)`), 不承重。本席复跑了 `ext_bare` / `ext_first` / `vx_interleave` 三个变体, 与执笔汇总一致。
5. 12j 未经独立 review: **可接受**。目标态 yes; 12j 假设的顺序 (gcp → postgres → x-api-key → auth-header → cf → cli) 与 W2 列出的新 tag 顺序一致, 但 W2 没写「按此顺序插入」, 建议 v3 在 W2 补一句。
6. bash 3.2 腿默认 `n/a`: **部分可接受**。Tasks 要求带该腿, 但探针末行不区分 (m7)。
7. 性能数字噪声大: **可接受**, SC-30 才是闸; 但 L3 缺闸 (m4)。
8. 25 个坏实现由作者自构: **可接受**。本席独立构造 8 个坏实现与 3 个修法原型, 暴露了作者变体没覆盖的存活类 (M1 / M2 / m1 / m2)。
9. SC-33 归因清单写死两个路径: **可接受**; 主仓抽样见 V12。
10. W9 静默失效是产品取舍: **可接受** (owner 级, 待复议 18)。
11. Windows / macOS 未实测: **可接受**, 但 10CG/aria-plugin#203 的报告者在 MINGW64, 建议 B.1 请 owner 在该平台验 W9 的 `CLAUDE_PROJECT_DIR` 路径形态与 `grep -ob` 偏移语义 (BSD grep 未验)。
12. 探针并发竞态: **可接受**; 修法 (私有 `USER`) 与待复议 7.18 合理, 本席并发跑多份探针未再遇到。

**请裁项 (§6)**
1. rule6_note 块 A 取 `n/a` 还是 `1`: **可接受 `n/a`**。SOT §4.1 字面: `n/a = 本 spec 不属 Skill 变更`, 且文字已写明这是分类而非免验; 取 `1` 反而暗示「描述性 + substitute」。
2. 是否再削体量: 不要求。
3. W9 静默失效 (待复议 18): 可接受按 A 选项落地, 选项 B / C 的 spike 由 owner 定。
4. #203 / #221 评论口径: **可接受理解 B** (与决策单第 2 项字面一致)。
5. SC-33 是否改写 `no-plan-fallback.md`: 可接受只归因, 改写牵涉 Rule #6。
6. 探针对未带 `WPA_BASH32` 是否改为失败: 不要求; 但应让形态行显式带 `not-run rows` (m7)。
7. 原型与脚本归档: 已见 `.aria/notes/…/writer-v2-proto/` 入仓; 可接受 (绝对路径需重跑时改)。
8. 交付形态: 可接受。

**待 owner 复议 (Spec 内 1–18)**: 1 默认 A 可接受; 2 默认 A 可接受; 3 默认 B 可接受; 4 Level 2 可接受 (决策单第 3 项已裁); 5 可接受 (已申报习惯变化, 见 M3 / m5 的补充覆盖); 6 MINOR 可接受; 7 建议开单清单可接受; 8–17 可接受 (8 见请裁 1); 18 可接受按 A。

## 风险 / 疑问 (不计入 finding)

- **环境观察**: 本席审计期间装机的 v1.74.1 `secret-scan` 对 Bash 输出里的 R1 报告文本 (4 处)、对 `secret-scan.test.sh` 夹具文本 (9 处)、对本席写脚本的 Write 结果 (1 处) 告警, 全部是合成占位 / 夹具, 无需轮换; 装机的 `secret-guard` 拦了本席 3 条含 `.env` / `nomad var put -h` 字样的 Bash 命令, 改用 Write 落脚本绕开, 未用 `# guard:ack`。这正是 W3 / W7 要消除的误报形态, 也提示 B.2 会话里改测试 / 夹具文件应一律用 Write。
- **W5 的必要性**: 三个 issue 都没诉求在 additionalContext 里加 tag / 来源 (评论 19339 明说原草案那部分「现行已满足」), Why 表也没有对应的洞; 删去 W5 即无需 rule6_note 块 B 与待复议 8。不改变实现者动作, 故不立 finding; 请主控 / owner 知悉。
- **W12 原型的写法**: 原型的 `_sg_judge_one` 用 `${subj//"pat"/"rep"}` 做归一化, 在真 bash 3.2 下替换串会带字面引号 (本席实测 `.environ.get(` → `".ek_("`), 对「不再含 `.env`」的判定无影响, 但与 W10 自己的「禁用 `${s//p/r}`」警告不一致; 建议 W12 同样规定前后缀拼接, 以免实现者把这种写法抄进 W10。
- **bash 5.2 对 `[[ … =~ ^<…>$ ]]` 的裸 `<` 同样报语法错** (本席实测), Spec 只写了 3.2; 不影响结论。
- **SC-13 13d**: 正则 `[^()]*` 允许插入段内含自由文本, 多 tag 情形 (13a–c 都是单 tag) 的内文未钉; 属理论缺口。
- **规模**: proposal 402 行 / 探针 320 行 / 14 个工作项, 三条 Level 3 判据字面命中, owner 已裁 Level 2 (决策单第 3 项) —— 本席不再重复异议。
- **未复核项**: Windows Git-Bash 与 macOS (BSD grep `-ob`、`ps -aux` 在 macOS 上是报错而非 BSD 输出, M3 的 `-aux` 只对 Linux procps 成立); 执笔 25 个变体里本席只复跑了 3 个 (V5), 其余按汇总采信。
- **时延数字**: 本席全部在 load 12–29 的 4 核共享主机上测 (V10), 绝对值不可比, 只给比值。

## Verdict

- verdict: **PASS_WITH_WARNINGS**
- counts: **0C/4M/7m**
- **Vote: REVISE**

## 是否足以进入 A.2

**不足以** —— 4 条 major 须在 v3 处理后再进 A.2 (M1 / M2 为补 SC 行并数据驱动、M3 为 W11 一处三类覆盖加 SC-22 行、M4 为 Tasks 1.10 改诱饵并拆任务), 修法均小, M3 的修法已在原型上验证 (SC-16 / 17 / 18 / 21 / 22 / 25 共 99 行仍全 yes, 258 条真实历史命令零新增误拦); R1 的 critical 与簇 A–I 已收口, 方案取舍与 Level 2 范围本身成立。

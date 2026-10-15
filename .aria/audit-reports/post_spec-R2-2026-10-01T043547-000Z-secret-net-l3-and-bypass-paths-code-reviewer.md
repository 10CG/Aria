---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-01T05:31:12.815Z
context: openspec/changes/secret-net-l3-and-bypass-paths/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 已实读文件

- 被审文件: `proposal.md` 全文 (1-402); `baseline-evidence.md` 全文 (1-421); `baseline_probe.py` 1-410、640-700 (SC-13)、730-1000 (SC-18 到 SC-25)、1000-1531。另看了 `git diff --stat 47aa15f b3e3123` (proposal 427 行 +/-, 基本是重写)。
- issue 与决策单: `aria-plugin-154.md` / `aria-plugin-203.md` / `Aria-221.md` 全文 (含评论 19339、25898); 决策单 `.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md` 全文; CLAUDE.md 规则 #6 / #7 / #10 与「多远程推送」两条约束 (已在上下文中)。
- 源码 (aria `268da8f`): `hooks/secret-scan.sh` 全文; `hooks/secret-guard.sh` 全文 (1-1120); `hooks/hooks.json` 全文; `secret-guard.test.sh` :9-13 / :838-843 / :1616-1624 / :2015-2032; `secret-scan.test.sh` :26-34 / :90-125 / :143-155; `VERSION` :160-168; `.github/secret_scanning.yml` :14-22; `README.md` :137-160 与 Hooks 标题; `README.zh.md` 标题; `CHANGELOG.md` 版本标题与 1.47.0 / 1.65.4 / 1.66.3 / 1.66.4 条; `skills/spec-drafter/LEVEL_GUIDE.md` :150-162; `skills/aria-doctor` (grep, 无耦合)。
- standards (`2bc1c4c`): `secret-hygiene.md` 标题、:1-8、:23、:73-236、:285-290、:317-321; `skill-benchmark-exemption.md` :1-100; `openspec/templates/proposal-minimal.md` :45-58; `openspec/project.md` :117。
- 先例与接缝: `openspec/archive/2026-08-02-secret-guard-nomad-var-put-echo/proposal.md` :96-138; `openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml` :341-342 (`guard_config_hooks`); 主仓 `72cb02b` / `a99dd8d` 与 aria `268da8f` 的 `--stat`。
- 研究笔记: `secret-scan.md` §1.2 / §1.9 / §3 矩阵行 / :112-115; `secret-guard.md` §0; `precedent.md` §6.4; `cc-hooks.md` 标题 (节号引用逐条核对存在)。
- 上一轮: R1 聚合报告全文; R1 code-reviewer 报告全文。返修: `v2-writer-report.md` 全文; `writer-v2-proto/README.md` 与 `mut_summary{,2,3}.txt`。
- 原型 (writer-v2 `final/full` 的私有副本): `secret-scan.sh` :232-420; `secret-guard.sh` :500-660、:1250-1360。
- 平台: `claude` 2.1.285 二进制的定向字符串检索; bash 3.2.57 / 5.2.15、jq 1.6、curl 7.88.1、nomad v1.11.2 实跑。

**独立复算 (成立的部分, 不计 finding)**

- 探针复跑 (私有副本 aria `268da8f` + standards `2bc1c4c`, 带 `WPA_BASH32`): stdout sha256[:16] = `13cdea30978e1119`, 52197 字节, stderr 为空, rc=0, 用时约 7 分钟, 与 `baseline-evidence.md` 内嵌块**逐字节相同**。不带 `WPA_BASH32`: `4560f25263f2a6e0`, 52164 字节, 与带腿版本只差 29h / 29i / 32c 三行与计数行。两者都与证据文件的声称一致。
- 探针跑原型副本: `4b0eea9cd97621d4`, 52861 字节, 「target shape … holds」, 六类分别为 154/154、20/20、53/53、57/57、26/26、9/9, 32c 在 277 行上一致, 29i 为 584/585。与执笔 T1 的声称一致。
- 行数自洽: 33 组 SC 合计 320 行, 每组的类别计数与 proposal 各 SC 段写的 ×N 逐条对上。三份文件的 sha256 与执笔 MANIFEST 表一致 (`654cb86e…` / `522fe621…` / `bbcdf837…`)。
- file:line 抽核全部成立 (@ `268da8f` / `2bc1c4c`): secret-scan.sh :15-20 / :33-34 / :52 / :64 / :72-80 / :135-142 / :144 / :152-231 (31 条) / :215 / :218 / :224 / :227 / :355-361 / :367; secret-guard.sh :21-23 / :62 / :405-408 / :427 / :491-493 / :564 / :617-620 / :626 / :631-694 / :641 / :698-700 / :736-1009 (145 行) / :815 (13 个读取器) / :893 / :894 / :930-933 / :974 / :1043-1071 / :1088-1102 / :1111; 测试 :11 / :841 / :1620 / :1622 / :2018-2030; hygiene :23 / :287 / :288 (49) / :319, 版本 1.1.2; VERSION:164; secret_scanning.yml:18-22; LEVEL_GUIDE:160; proposal-minimal:53; project.md:117。runbook 路径在全仓不存在 (确实悬空)。
- 平台与工具事实: 二进制含 `updatedToolOutput`, 描述串「Replaces the tool output before it is sent to the model」出现 3 次; 真 bash 3.2.57 上 `${x//b/"$r"}` 输出 `a"Z"c`, 5.2 输出 `aZc`; jq 1.6 `map_values(length)` 把 -4821 变成 4821; curl 7.88.1 `-K -` 读 stdin 配置后连接被拒 exit 7, 无 URL 时 exit 2, `-H @<文件>` 被接受; `nomad var put -h` 含「consumed as-is」; `grep updatedInput aria/hooks` 零命中。
- 同步面: `72cb02b` / `a99dd8d` 的 `--stat` 都是 CLAUDE.md 2 处、README.md 2 处、zh/ja/ko 各 3 处、VERSION 1 处、两份架构文档各 1 处, 合计 16 处, 与 Impact 一致; 10CG/Aria#199 守卫命令与 `detailed-tasks.yaml:342` 逐字一致。
- 自扫描: `proposal.md` / `baseline_probe.py` / `baseline-evidence.md` 三份文本分别以 Bash 与 Read 信封喂基线和原型 L3, 6 种组合全部静默。

## Findings

### Major

**M1** `fc97f926` · major · issue · implementation · `proposal.md What.W3`

Summary: W3 白名单第 2 类里的裸 `$NAME` 与 `$(…)` 两种整值形态, 没有任何一行钉住 (把它们删掉的坏实现照样全绿)。而 `$NAME` 会让既有 json 键上「`$` + 字母 + 单一大小写字母数字」的真值由检出变成静默。这与 Impact「`$` / `<` 开头的随机值 … 仍检出」以及主控裁定 1 的字面相反, 既没申报, 也没有 known-limit 行。

证据:
- `proposal.md:82`「`$NAME` (NAME 全大写或全小写, 加数字与下划线; **不含混合大小写**)、`$(…)`」; `:88`「**不是**白名单的: 以 `$` 开头的随机值 (`$` 后是混合大小写或夹杂符号)」; `:95` 已知限制没有提单一大小写这一类; `:330` Impact 新静默写着「`$` / `<` 开头的随机值与 crypt 口令哈希**不**在内 (仍检出)」; R1 聚合「主控裁定」第 1 条:「`$` / `<` 开头的随机值必须仍被检出」。
- 实跑。值在 Python 进程内用 `secrets` 运行时生成, 用 Bash 真实信封喂 hook, 只打印元数据; base = aria `268da8f` 副本, proto = writer-v2 `final/full` 副本:
```
D1 json:password      = '$'+字母+18 位 [a-z0-9]  base alert {json-secret-field=1}  proto silent  (2/2 次)
D2 json:client_secret = '$'+字母+30 位 [a-z0-9]  base alert {json-secret-field=1}  proto silent  (2/2)
D3 json:api_key       = '$'+字母+30 位 [A-Z0-9]  base alert {json-secret-field=1}  proto silent  (2/2)
D4 json:secret        = '$'+字母+38 位 hex       base alert {json-secret-field=1}  proto silent  (2/2)
D5 对照: '$'+混合大小写                          base alert                        proto alert   (2/2)
```
- 坏实现: 在原型副本里删掉 `_RE_VARU` / `_RE_VARL` / `_RE_CMDS` 三条匹配, 等于不实现裸 `$NAME` 与 `$(…)`。用 `WPA_ONLY=SC-1,…,SC-13,SC-15,SC-33` 复跑, 结果 0 行 `no`, 打印「target shape (every row 'yes'): holds」。
- 原因: 用到裸 `$NAME` 的只有 9l / 9m, 而它们落在 `auth-header-token` / `cli-secret-flag` 上。这两个 tag 的值字符类 (原型 `[A-Za-z0-9._/+=-]` / `[A-Za-z0-9+/=._~-]`) 都不含 `$`, 正则根本不命中, 白名单一次也没被执行。9b 的 `$(…)` 在行首 env 形, 同理。JSON 键上的 `${…}` 有 11g / 11v 钉住, 裸 `$NAME` 与 `$(…)` 一行都没有。7h 的 dollar20 生成器强制混合大小写 (`baseline_probe.py:198`), 只钉住了「混合大小写不放行」这一侧。

失败场景与三态:
- 基线: D1–D4 告警。
- 照 W3 字面实现 (原型): D1–D4 静默, 320 行仍然全绿, 而 owner 在 Impact 里读到的是「仍检出」。
- 坏实现: 漏掉 `$NAME` / `$(…)`, 文档式占位的误报回来了, 也是全绿。
- 结论: SC 两个方向都测不出。

修法:
1. W3 已知限制与 Impact「新静默」如实写出这个残余: 既有 10 个 json 键上, 整值为「`$` + 字母 + 单一大小写字母数字下划线」的值由检出变静默。
2. 补两行。allow-guard: json:token = `$`+大写变量名、json:password = `$(…)` → 静默, 用来钉住白名单的意图; known-limit: json:client_secret = `$`+字母+31 位单一大小写 → 静默, 用来钉住残余。
3. 是否收窄 (例如裸 `$NAME` 只认全大写环境变量名) 列入待复议第 10 条, 由 owner 裁。

**M2** `6bd285b1` · major · issue · testing · `proposal.md SC-30`

Summary: SC-30 时档 (h) 的「耗时 < 5 s」是共享主机上的墙钟绝对值, 红绿由主机负载决定, 不由实现决定。本机负载约 4 时, 基线自身 600 段就要 6.5 s; 负载约 12 时要 13–19 s, 此时任何实现都是红。安静时一个每段慢 25% 的实现反而能过。而「内建先判、不被推迟」已经由 20l / 21v 确定性地钉住了。

证据:
- `proposal.md:225` W14 (h) 原文:「耗时 ≤ 改前 × 1.5 **且** < 5 s (… 基线 600 段已 3.8 s …)」; `:286` SC-30「(h)」; `:355` Tasks 1.10 要求「SC-30 全绿 (含三个新时档)」。
- 实跑。同一主机, 命令在 Python 内运行时拼装, 每格 3 次取最小; 600 个 `echo x` 段加末段 dotenv 读取, 两侧都 exit 2:
```
load≈4.3  600 段 base 6.54 s / proto 6.49 s; 700 段 5.41 / 6.36; 800 段 6.29 / 7.37
load≈12   600 段 base 墙钟 13.5–19.4 s, CPU 7.3–7.5 s; proto 墙钟 9.6–20.9 s, CPU 7.6–8.7 s (CPU 比约 1.16)
执笔记录 (load 1.5–3.1): base 3.83 s / proto 4.43 s
```
- 执笔 §5 第 7 条自报了噪声与 0.6 s 余量。本条补上的是「基线自身就越界」的实测, 以及判据的改法。

三态:
- 基线: 负载 ≥ 约 3 时已越过 5 s, 判红。
- 正确实现: 随负载忽红忽绿。
- 坏实现: 每段多 25% 开销的实现, 安静时 3.8 × 1.25 ≈ 4.75 s, 可以过。

失败场景: 实现者在 B.2 照字面跑 (h)。共享主机任一时段负载上来就红, 没有合法的下一步, 只能等或者换机器; 反过来也可能挑安静时段, 让一个慢了 25% 的实现过关。

修法: (h) 改为与同一次运行里基线 hook 的 CPU 时间 (user+sys) 比值, 例如 ≤ 1.2×, 保留「仍 exit 2」。「内建先判」交给 20l / 21v, 二者已钉住。墙钟与负载只记录、不判。若测量环境里基线自身 ≥ 5 s, 判为环境不合格、重测, 而不是判红。

### Minor

**m1** `cfb24732` · minor · risk · architecture · `proposal.md What.W14`

Summary: L3 新增的逐 span 处理没有成本上界的验收。原型 (全部 320 行绿) 对每个 tag 的每个 span 都跑一遍 bash 循环, 在稠密的既有 tag 输入上比基线慢 3–11 倍。约 1 MB 的 bearer 行输入从 0.52 s 变成 5.84 s, 越过了 5 s 超时: 基线能检出, 目标会因超时而没有告警。W14 只给了「180 KB 稠密 INI ≤ 2.5 s」这一个点。

证据:
- 原型 `secret-scan.sh` 的 `while IFS= read -r span … done < <(grep -oE …)` 在 seen>200 后仍对每个 span 调 `_value_of` / `_fp_add`。
- 实测 (负载 2–5, 3 次取最小, base → proto):

| 输入 | base | proto |
|---|---|---|
| bearer 稠密 100 KB | 0.25 s | 0.75 s |
| bearer 稠密 200 KB | 0.27 s | 1.26 s |
| bearer 稠密 300 KB | 0.30 s | 1.81 s |
| bearer 稠密 600 KB | 0.37 s | 3.21 s |
| bearer 稠密 800 KB | 0.90 s | 4.34 s |
| bearer 稠密 990 KB | 0.52 s | 5.84 s |
| JSON 口令行 600 KB | 0.56 s | 1.78 s |

- 研究笔记 `secret-scan.md:112` 记录的真实最大值: Bash 103 KB / Read 93 KB / Write 198 KB。所以实际暴露面限于病态的稠密输出, 或者主机高负载。

修法: W2 / W4 写明「分类到 200、指纹到 10 之后不再逐 span 迭代, 余数用计数取得」; W14 补一条相对预算 (约 200 KB 稠密既有 tag 输入, CPU 时间 ≤ 基线 × 2), 并写进 Tasks 1.10。

**m2** `6114c254` · minor · issue · implementation · `proposal.md What.W2`

Summary: 点分标识符链的排除, 把「点分结构的真凭据」也当成读取写法静默掉了。SendGrid 形 `SG.<22>.<43>` 约 1/4 的取值满足 `_RE_DOTID`, 在 kv 空格形、`export`、camel json 键、`--api-key=`、`Authorization: token` 这五种新 tag 形态下全部静默。W2 写的「随机凭据不含以 `.` 分隔的标识符段, 漏报面≈0」(`proposal.md:74`) 不成立, 已知限制也没有列。

证据: 原型上 5 种形态都是 silent; 走既有 tag 的两种 (json:api_key、行首 env) 仍告警。按 base64url 字母表算, 取值落入点分链的概率 ≈ (53/64)² × (63/64)^63 ≈ 0.25。不是回退 (基线这些形态也静默)。

修法: W2 已知限制补「点分结构的凭据 (SendGrid / Mapbox 形)」, SC-10 加一行 known-limit; 可选的收紧 (例如要求首段小写开头) 列入待复议第 9 条。

**m3** `15da802b` · minor · issue · documentation · `proposal.md What.W8`

Summary: W8 的名字组只认命令文本里出现的 `app.ini`, 对目录递归和文件名 glob 读取全部放行。已知限制 (`:149`) 只列了相对名、先复制再读、模板等, 没列这一类, 也没有 known-limit 行。

证据: 下面 6 种 base / proto 都是 exit 0:
- `grep -rn JWT_SECRET /etc/forgejo/`
- `grep -r SECRET /var/lib/forgejo/custom/conf`
- `cat /etc/forgejo/*.ini`
- `sed -n '1,80p' /etc/gitea/*`
- `head -n 200 /etc/forgejo/app.*`
- 花括号展开

对照 `grep -n JWT_SECRET /etc/forgejo/app.ini` 为 0 → 2。输出侧有兜底: `grep -rn` 的输出行形 `<路径>:<行号>:JWT_SECRET = <44 b64>` 在原型上命中 `kv-secret-assign=1` (基线静默)。

修法: W8 已知限制补「目录递归 / 文件名 glob」; SC-17 加 known-limit 行, 例如 `grep -rn JWT_SECRET /etc/forgejo/` → exit 0, 并写明输出侧由 W2 兜底。

**m4** `467c8b54` · minor · issue · implementation · `proposal.md What.W11`

Summary: W11 有一批同族形态既没覆盖也没申报, 在原型上都放行:
- `podman top <c>` / `podman ps --no-trunc`: 与 `docker top` / `docker ps --no-trunc` 同义, 且 hook 已有 `podman exec` 行。
- 绝对路径 `/bin/ps aux`: 既有 printenv 行有 `/bin/`、`/usr/bin/` 变体。
- BSD 选项簇不在首位: `ps -U dev -u dev u`、`ps -e o pid,args`。这与 W11「任意 BSD 选项簇」的字面不符。

证据: 上述 6 条命令在原型上都是 exit 0; 探针 SC-22 的命令表 (`baseline_probe.py:900-912`) 里一条也没有。

修法: 纳入, 或在 W11 已知限制成文并补 known-limit 行; 同时写明 BSD 簇的判定是「首个操作数」还是「任意位置」。

**m5** `29a5d0bd` · minor · issue · testing · `proposal.md SC-22`

Summary: 22S 把 `pgrep -fl curl` 钉成 allow-guard (误报守卫)。但 W11 自己写明 macOS 上 `pgrep -fl` 会输出完整命令行, 只是本 Spec 按 Linux 语义放行 (`proposal.md:193`)。这是已知漏拦, 按类别定义 (`:241`) 应当是 known-limit。现在的分类下, 日后为 macOS 收口会表现成「误报守卫被破坏」。

证据: `baseline_probe.py:916` 的 22S 列表含 `pgrep -fl curl`, 类别为 allow-guard。

修法: 把 `pgrep -fl` 从 22S 拆成一行 known-limit 并注明 macOS 语义; 22S 只留 Linux 下只出名字的形态。

**m6** `335996c0` · minor · issue · testing · `proposal.md SC-33`

Summary: SC-33 说关键词预筛是 6 个新 tag 的必要条件、只为提速 (`proposal.md:289`, 探针 :1402 注释)。但 `json-credential-field` 封闭名表里的 `privateKey` / `PrivateKey` / `privatekey` 不含预筛的任何关键词 (预筛只有带下划线的 `private_key`)。含这类键的文件会被预筛跳过、根本不进普查, 结果是假绿。

证据: 三种拼写的预筛结果都是 False, 而原型都告警 `json-credential-field=1`。当前 aria 与 standards 语料里这类文件为 0 个, 所以眼下没有实际影响。

修法: 预筛补 `private[_-]?key`, 或者干脆取消预筛。

**m7** `d65a895f` · minor · issue · architecture · `proposal.md What.W9`

Summary: W9 同时要求两件事, 而二者不能同时成立:
- 「项目根解析、文件读取与校验 … **只**经 `$( … )` 调用」(`:159`);
- 「无扩展文件时 … 不 fork 任何子进程 (`[[ -f ]]` 是 builtin)」(`:158`)。

命令替换必然 fork。原型在每次 Bash 调用时都 fork, 并以空模式文件调用 `grep -f`。另外, `:158`「命中的出现点最多检查 64 处」超出之后是放行还是拦截没有规定, 也没有行钉住。原型的做法是第 64 处后 `break`, 即放行。

证据: 原型 `_sg_ext_pass` 每次都执行 `grep -oFib -f <(_sg_ext_entries) …`; 执笔实测的「无扩展」列单段从 48 ms 升到 54 ms。

修法: 二选一写明取舍, 要么允许主 shell 里只做一次 `[[ -f ]]` 预检, 要么删去「不 fork」句。另外规定第 65 处起的语义, 并补一行。

**m8** `51dded0b` · minor · issue · testing · `proposal.md SC-15`

Summary: 头部「Rule #7 声明」(`:13`) 说「本 Spec 与两份附件 … (SC-15 15e / 15f 钉住)」。但 15e 钉的是 `proposal.md`, 15f 钉的是 `baseline_probe.py`, 第二份附件 `baseline-evidence.md` 没有任何一行钉住。本席实测它在基线与原型上、两种信封下都静默, 所以当前无实际影响。

修法: SC-15 加一行 15g (`baseline-evidence.md` 文本 → 静默), 或者改写头部声明的覆盖范围。

## 上一轮对账

按 R1 聚合「主控记录」的归并簇逐条对账。证据里的「T1」指本席在原型副本上的探针复跑 (`4b0eea9cd97621d4`), 「base 复跑」指 `13cdea30978e1119`。

| 簇 | R1 键 (C/M) | 状态 | 本席核验证据 |
|---|---|---|---|
| A | `e8d39a8a` · `14b7e703` · `8645b99f` | **partially closed** | 前缀放行已改为整值形态。T1 中 7h (crypt60 / dollar20 / lt16 不闭合 / marker-mid / 小写 fake_ / env-line marker) 与 7i 均为 yes, D5 混合大小写对照仍告警。残余是裸 `$NAME` 单一大小写的静默与 `$NAME` / `$(…)` 无行钉, 见 M1 (新键 `fc97f926`) |
| B | `e600e931` · `179045cd` · `f42265a1` | closed | T1 中 23c 的 10 条为 yes。另测 9 种整表导出在原型上仍是 exit 2: `__dict__`、`vars()`、`*values()`、`get() or os.environ`、推导式遍历、别名、`map(get, environ)` 等; 只有单键 `.get(` / `[ ]` 变成 0 (已申报) |
| B2 | `d9308fba` · `ab6a3123` | closed | T1 中 23d (`.env_prod` / `.env2` / `.envprod` / `.envs/` 经解释器) 仍为 exit 2; 23g 把 `cat .env_prod` 钉成现状 |
| C | `7e0343bd` | closed | T1 中 20i–20k 为 yes; 原型的扩展只经 `$( _sg_ext_* )` 调用 (`secret-guard.sh` 原型 :815-819、:1328-1334) |
| C2 | `d4bcaf7c` | closed | 已改为固定字符串单遍匹配 (`grep -F -f`), 上界为条目 200、32 KiB、64 处; 时档 (f) 有相对判据 |
| C2 | `d8e7b380` | **partially closed** | 求值顺序由 20l / 21v 钉住 (T1 均为 yes); 但时档 (h) 的绝对 5 s 判据受负载决定, 见 M2 (新键 `6bd285b1`) |
| C3 | `719ae05c` | closed | T1 中 19j (14 个元字符条目)、19k、20h 为 yes; `mut_summary` 的 ext_regex 让 19j / 20h 转红 |
| C4 | `53c140c4` · `27f6c3ce` · `b73ab606` | closed | 落点为 §5.6、README 两语种、头注释、CHANGELOG, SC-26c / e / f / g 都限定在小节内 (`section()`, 探针 :1122-1208); docs_bad2 让 26a–26d 与 28h 转红 |
| D | `634eac5c` · `2ce0049b` | closed | W4 取值表覆盖 31 条既有 tag、6 个新 tag 与 2 个 PEM tag (逐 tag 对 `secret-scan.sh:159-230` 核过); T1 中 12a–12j 为 yes; fp_span 让 12g–12j 转红 |
| E | `44b5bb44` | closed | 真 bash 3.2.57 已核; base 复跑与 T1 的 32c 都是「identical over 277 hook-direct rows」, 29h 为 49/49, 29i 为 581/582 与 584/585。残余: 不带腿时汇总行仍打印 holds, 见下节对 §5 第 6 条与 §6 第 6 条的表态 |
| F | `e2459206` · `9db51a43` | closed | T1 中 22ao–22ar、22at、22as 为 yes; 本席另测 launcher 包裹 (nice / env / exec / timeout / watch) 与 docker / kubectl / lxc exec 下的 `ps`, 在原型上都是 exit 2 |
| G | `846b21f8` | closed | §3.8 的适用面限定为长时进程; 26h 用哈希 `e6ebdabbb10d0030` 钉住 §3.1–§3.7 与 §4.1–§4.4, 基线与 T1 都为 yes |
| H | `7deac83f` · `2779a016` · `ba98e41f` | closed | `:341` 默认理解 B (不在 10CG/aria-plugin#203、10CG/Aria#221 下评论); `:340` 10CG/aria-plugin#154 的关单放在 post-ship 复验之后; 16 个版本点与 `72cb02b` / `a99dd8d` 的 `--stat` 一致; Tasks 1.11 有承载行 |
| I | `cf0ae932` | closed | 研究笔记在 `959daed` 入仓 (`git ls-files` 已核), 引用的 `scan` / `guard` / `prec` / `cc` 节号逐条存在 |
| J | `d9986b27` | closed | 13d 为全串等值 (`INSERT_RE` + 基线串, 探针 :660-668); w5_append 让 13d 转红; 13a–13c 的精确针在括号内插入时也会红 |
| J | `5831f8c0` | closed | SC-26 改为限定小节, 见 C4 |
| J | `1c0bc16f` | closed | R1 列出的 5 个存活变体都已转红 (`mut_summary`: 7h / 4o / 11s)。本席另构造的「去掉 `$NAME`」变体存活, 记为 M1 |
| J | `a3054a20` | closed | 加了强制首字符生成器 (`baseline_probe.py:131-137`、:196-200), 4n / 5l / 5m / 7h 已覆盖; loosepath 让 4n / 5l / 9w 转红 |
| J | `8e77d1ca` | closed | SC-33 在 T1 上 flagged=1 且在归因清单内; noentropy 变体使清单外 5 个文件命中。残余见 m2 (点分链漏报) 与 m6 (预筛盲区) |

R1 minor 中我认为仍未完全处置的只有 `5856b370` (cr/m3): 9l / 9m 虽然加长到 24 / 25 字符, 但它们所在 tag 的值字符类不含 `$`, 白名单仍然没被执行。已并入 M1。

## 对执笔人自报薄弱点与请裁项的表态

**§5 执笔自报薄弱点**

1. **文字体量 +44%**: 可接受。不影响正确性; 建议收敛后再削, 本轮不必。
2. **交付形态 (母本路径 + sha256)**: 可接受。三份文件的 sha256 与 MANIFEST 表一致, 证据块已由本席逐字节复现。
3. **原型不是实现**: 可接受。但 m1 恰恰来自原型的成本特性 —— 「设计可达」不等于「成本可接受」, 所以 W14 应补相对预算。
4. **「变异实测」声称**: 可接受。`mut_summary` 与 proposal 里点名的转红行一致。本席另构造的一个变体全绿, 见 M1。
5. **12j 未经独立 review**: 可接受。本席核过: 基线 no、T1 yes, fp_span 让它转红, W4 表逐 tag 完整。
6. **bash 3.2 腿默认不开**: 不可接受现状。本席在原型上不带 `WPA_BASH32` 跑 `WPA_ONLY=SC-32`, 32c 为 `n/a`, 末行却仍打印「target shape (every row 'yes'): holds」(`target_shape` 把 n/a 行排除在外, 探针 :1519)。建议: 行级 match 保留 n/a, 以保证基线可复现; 但只要存在 SC-30 与 root 下 20g 之外的 n/a 行, 汇总行就改印「not established (N rows not-run)」。
7. **性能数字噪声大**: 作为风险自报可接受, 但作为验收口径不可接受, 见 M2。
8. **坏实现都由执笔构造**: 可接受, Tasks 1.8 已要求非作者构造。本席独立构造的一个即暴露了 M1, 说明 1.8 是必要的。
9. **SC-33 归因清单写死**: 可接受。
10. **W9 失效静默**: 作为 owner 产品级默认可接受 (待复议第 18 条)。
11. **Windows / macOS 未实测**: 可接受 (已成文)。另有 BSD userland 风险, 见下节。
12. **探针并发竞态**: 可接受。探针已用私有 `USER` 绕开, 套件缺陷已进建议开单第 18 条。

**§6 请裁项**

1. **rule6_note 块 A 取 `n/a` 还是 `1`**: 可接受 `n/a`。SOT §4.1 的字段语义是「n/a = 本 spec 不属 Skill 变更」, 与事实相符; 块 A 正文已明确不援引 Rule #10 第四类, 并给出 substitute 三件, 与 2026-08-02 先例里被 owner 否决的「不适用 = 结构性前提不成立」写法不同; 且已列入待复议第 8 条。
2. **是否再削文字体量**: 不要求。
3. **W9 失效静默**: 维持默认选项 A, 由 owner 裁。
4. **10CG/aria-plugin#203 / 10CG/Aria#221 的评论口径**: 可接受默认理解 B (决策单第 2 项执行注的字面, 加主控裁定 4)。
5. **是否改写 `no-plan-fallback.md`**: 可接受只归因。改 Skill 示例会牵动 Rule #6, 超出本 Spec。
6. **未带 `WPA_BASH32` 时 n/a 还是失败**: 同 §5 第 6 条: 行级 n/a 可接受, 汇总行不得印 holds。
7. **原型与脚本是否归档**: 可接受。`writer-v2-proto/` 下 14 个文件已在 `b3e3123` 入仓 (`git ls-files` 已核); 树副本不入仓也可接受。
8. **交付形态**: 可接受。

## 风险 / 疑问

1. **L1 超时悬崖在本主机上远低于 1400 段**: 负载约 4 时基线 600 段就要 6.5 s, 负载约 12 时 13–19 s。生产中长命令因超时而放行的阈值会随负载大幅下移。这是既有问题 (建议开单第 1 条); W8 / W11 / W12 使每段 CPU 约增加 16%。
2. **BSD userland 没有运行腿**: W2 / W8 / W11 声称兼容 BSD grep / sed, 但没有任何 BSD 测试腿。原型在没有扩展文件时会以空模式文件调用 `grep -F -f`: GNU 下匹配零行, 其它实现的语义待核。建议 W9 写明「零有效条目 ⇒ 不调用 grep」。
3. **W6「退出时清理」的实现提示**: 清理时要删的是记录下来的临时目录变量, 不得写成 `rm -rf "$HOME"`。否则只要有任一路径恢复了 HOME, 就会删掉真实的家目录。
4. **现场观察**:
   - 本席一次 awk 掩码失效 (mawk 不支持 `{n,}` 区间), `secret-scan.test.sh` 里的仓内公开夹具 (FAKE / EXAMPLE 字样) 进入了本会话输出, 现行 L3 告警 22 处。全部是公开测试夹具, 不是真实凭据, 无需轮换; 这也顺带复证了 W7 的前提。
   - 另有一次 Bash heredoc 因正文含 dotenv 读取的字面被现行 L1 拦下 (文本提及类误拦), 改成运行时拼装后通过。真仓未做任何写操作 (HEAD `b3e3123`、aria `268da8f`、standards `2bc1c4c`, 工作区干净)。
5. **版本先例证据偏弱**: Impact 拿 v1.47.0 作「新增检测覆盖 = MINOR」的先例, 但它是 4 个 cycle 的合并发布, 证据偏弱。号由 owner 裁, 不影响实现。
6. **9m 注释的计数口径**: 9m 注释写「25 字符」, 但 `$RUNNER_REGISTRATION_TOKEN` 含 `$` 是 26 字符 (9l 的 24 是含 `$` 的计数), 两处口径不一。无实际影响。

## Verdict

**PASS_WITH_WARNINGS** —— counts `0C/2M/8m` —— **Vote: REVISE**

## 是否足以进入 A.2

不足以: M1 与 M2 都会改变 SC 行或判据本身 —— W3 要补两行并改 Impact 的申报, SC-30 (h) 要改成同一次运行内的 CPU 比值。若不先落进 proposal, detailed-tasks 会把不实的申报和由负载决定的判据原样编进任务。改动量小, 预计一轮可收。

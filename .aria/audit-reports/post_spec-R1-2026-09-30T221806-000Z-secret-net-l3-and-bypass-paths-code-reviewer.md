---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-09-30T22:52:06.374Z
context: openspec/changes/secret-net-l3-and-bypass-paths/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 已实读文件

- 被审: `openspec/changes/secret-net-l3-and-bypass-paths/proposal.md` 全文 (1-365); `baseline-evidence.md` 全文 (1-408); `baseline_probe.py` 全文 (1-1030)
- issue: `aria-plugin-154.md` / `aria-plugin-203.md` / `Aria-221.md` 全文 (含全部评论); 决策单 `.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md` 全文
- 源码: `aria/hooks/secret-scan.sh` 全文; `aria/hooks/secret-guard.sh` 全文; `aria/hooks/hooks.json` 全文; `secret-guard.test.sh` :1-15 / :743-753 / :836-845 / :1612-1626 / :2015-2032; `secret-scan.test.sh` :1-40 / :88-125 / :140-160 (长串掩码后读); `host-docker-logout-guard.sh` :122-123; `aria/.github/secret_scanning.yml` 全文; `aria/VERSION` :160-168; `aria/README.md` :7 / :31-33 / :136-160; `aria/skills/spec-drafter/LEVEL_GUIDE.md` :150-162
- SOT: `standards/conventions/skill-benchmark-exemption.md` 全文; `secret-hygiene.md` :1-26 / :114-125 / :281-296 / :316-322 / :397-404; `.aria/decisions/DEC-20260703-001-…` :30-77; `.aria/pat-inventory.yaml` 只读注释 :11-21 与键名 (未读任何指纹值); `.aria/state-checks.yaml` :135-141; `openspec/archive/2026-08-02-secret-guard-nomad-var-put-echo/proposal.md` :96-160 与另 5 份 archive 的 Level 行
- 背景: 研究笔记 `cc-hooks.md` 全文、`secret-scan.md` §0/§1.2/§1.7/§1.8/§1.9、`open-issues.json` (过滤)
- 平台: Claude Code 2.1.285 二进制 (定向字符串检索); 本机会话记录 `toolUseResult` 键结构统计 (只统计键名与类型, 不读值); `/usr/share/doc/bash/NEWS.gz`

**独立复算结果 (成立的部分, 不计 finding)**
- 探针复跑 (副本: aria 268da8f + standards 2bc1c4c, spec 目录同层): stdout sha256[:16] = `1ab63a323da13f45`, 41873 字节, 与 `baseline-evidence.md` 内嵌块逐字节相同, stderr 为空。
- 行数自洽: baseline-failing 131 + doc-sync 14 + reverse 60 + allow 88 + known-limit 25 + zero-regression 7 + SC-30 1 = 326, 与 proposal / 证据一致。
- file:line 抽核全部成立 (secret-scan.sh :15-23/:33-34/:52/:64/:72-80/:135-142/:144/:152-231 共 31 条/:224/:227/:355-361/:367; secret-guard.sh :21-23/:62/:405-408/:427/:491-493/:564/:617-620/:641/:698-700/:736-1009/:782/:815/:893/:894/:930-933/:974/:1043-1071/:1088-1102; 测试 :11/:841/:1620/:1622/:2018-2030; hygiene :23/:287/:288/:319, 版本 1.1.2; VERSION:164; secret_scanning.yml:18-22; LEVEL_GUIDE「影响多个子模块 → 自动提升为 Level 3」), 唯一偏差见 m1。runbook 路径确实悬空。
- 真实信封: 本机会话记录 Read = `{file:{content,filePath,numLines,startLine,totalLines},type}` (186 条), Bash = `{interrupted,isImage,noOutputExpected,stderr,stdout}` (5603 条); Edit 结果给模型的文本 938/938 不含片段回显 —— W1 与 Out of scope 的依据成立。
- 平台事实: 2.1.285 二进制确含 `updatedToolOutput:…describe("Replaces the tool output before it is sent to the model")` 与「hooks run in parallel on the ORIGINAL output … last-write-wins … can clobber a real redaction」。proposal 的表述正确; 研究笔记 `cc-hooks.md` 第 1 条「不存在 updatedToolOutput」是错的。
- 待复议第 7 条抽核: 7.2 `grep -E 'A|B' <bash rc>` exit 0 ✓; 7.4 `chmod 600 <ssh key>` exit 2 ✓; 7.11 私有 HOME 跑 secret-guard 套件后 `guard-bypass.log` 12 条事件、0 个换行 ✓; 7.12 源码 :122-123 写外层 HOME ✓; 7.15 census rc=1 且 `criteria.site_count == 6, expected exactly 13` ✓ (`patterns.total=145`, `family_count=61`); SC-29 无 git 副本 581/582, 唯一 FAIL = 测试内 SC-13 (599 vs 582) ✓。

## Findings

### Critical

**C1** `e8d39a8a` · critical · issue · implementation · `proposal.md What.W3`

Summary: W3 把「值以 `$` / `<` 开头即不计数」延伸到既有 `json-secret-field`, 且被放行的 span 仍被哨兵吞掉 → crypt 格式口令哈希与以 `$` 开头的真值在 JSON 凭据键上由检出变静默; proposal「须人为构造」的限制声明不成立, SC 集结构上测不到。

证据:
- `proposal.md:77`「值以下列任一开头即不计数: …`<`、`$`、`{{`…」「被放行的 span 仍被计数哨兵替换, 后序 tag 看不到它。作用范围 = 6 个新 tag + 既有 `json-secret-field`」; `:83`「以白名单词开头的真凭据会被放过 (须人为构造)」; `:290` 新静默只列占位 / 掩码 / wrapper 占位 / 哨兵回灌。
- `secret-scan.sh:227` json-secret-field (值 `"[^"]{8,}"`) 排在 `:230` bcrypt-hash 之前, 新 tag 按 `proposal.md:56` 插在二者之间。
- 实跑 (值在进程内运行时生成, 只打印 tag; 原型 = 按 W3 字面只给 json-secret-field 加前缀白名单并保留哨兵替换):
```
--- baseline (aria copy) ---
json password = bcrypt-shaped hash          -> rc=0 alert m=1 {json-secret-field=1}
json secret = argon2id-shaped hash          -> rc=0 alert m=1 {json-secret-field=1}
json passwd = sha512-crypt-shaped hash      -> rc=0 alert m=1 {json-secret-field=1}
json client_secret = $-leading 16-char      -> rc=0 alert m=1 {json-secret-field=1}
json token = bcrypt-shaped hash             -> rc=0 alert m=1 {bcrypt-hash=1}
--- W3 prototype on json-secret-field ---
json password = bcrypt-shaped hash          -> rc=0 silent
json secret = argon2id-shaped hash          -> rc=0 silent
json passwd = sha512-crypt-shaped hash      -> rc=0 silent
json client_secret = $-leading 16-char      -> rc=0 silent
json password = FAKE_ + 24 alnum (11m 形)   -> rc=0 silent            (W3 预期效果, 原型忠实)
json password = 12 alnum + ! (11t 形)       -> rc=0 alert m=1 {json-secret-field=1}
```
  原型只动了 json-secret-field; 按 W3 全文, 名表含 `token` 的 `json-credential-field` 对 `{"token":"$2b$…"}` 同样放行并吞掉 span, 排在其后的 bcrypt-hash 失去今天的检出。
- `baseline_probe.py:98-105` 生成器 `BAD_FIRST = set("/.~<$*{[\"'+=-_")`, 所有随机值首字符永不落入这些类 —— SC-7 7d/7e、SC-11 11t 等守卫行结构上不可能踩到本回退。

失败场景: 实现者照 W3 做 → 探针目标态全 `yes` → ship 后 Bash / Read 输出里的 `{"password":"$2b$12$…"}`、`{"secret":"$argon2id$…"}`、`{"client_secret":"$…"}` 不再告警 (今天告警)。三态: 基线 = 检出; 照 Spec = 静默; 坏实现同样静默 → SC 无法区分。

修法: (1) `$` 规则收窄为「整值是变量引用」(`^\$\{[A-Za-z_][A-Za-z0-9_]*\}$`、`^\$[A-Za-z_][A-Za-z0-9_]*$`、`^\$\{\{.*\}\}$`), `<` 规则收窄为整值 `^<[^<>]*>$` (仍覆盖尖括号占位与 `<secret-scan-counted:TAG>` 哨兵, SC-8 不受影响), 并显式排除 crypt 前缀 `^\$(2[abxy]|argon2(id|i|d)?|[0-9]|y|gy)\$`; (2) 或放行的 span 不被替换 (只有计数的 span 才吞), 后序 tag 仍可见; (3) 加不经生成器的确定性 reverse-guard 行: json:password=<bcrypt 形> → `json-secret-field=1`、json:token=<bcrypt 形> → 必有告警、json:client_secret=<`$`+15 随机> → `json-secret-field=1`; 同步改 `:83` 已知限制与 `:290` 申报。

### Major

**M1** `d9308fba` · major · issue · implementation · `proposal.md What.W12`

Summary: `\.env(rc)?([^A-Za-z0-9_]|$)` 让所有字母 / 数字后缀名经解释器由拦变放 (含 cookiecutter-django 的 `.envs/.production/*`), 申报与 SC 只覆盖下划线后缀。

证据: `proposal.md:166-167` fail 方向只写 `.env_prod`; `:289` 新放行只列 `os.environ` / `os.environb` / `*.environment` / 下划线后缀; SC-23 (`:237`) 无字母 / 数字后缀行。按 `:166` 原文改 `secret-guard.sh:893/:894/:974` 三行后实跑 (DOTENV = 点 env 名, 命令文本运行时拼装):
```
case                                                 base    W12-literal
python3: open(DOTENV+'s/.production/.postgres')      exit=2  exit=0
node:    readFileSync(DOTENV+'s/.production/.django') exit=2 exit=0
python3: open(DOTENV+'2')                            exit=2  exit=0
python3: open(DOTENV+'prod')                         exit=2  exit=0
python3: open(DOTENV+'_prod')   [已申报 23f]         exit=2  exit=0
python3: open(DOTENV)           [23g]                exit=2  exit=2
python3: os.environ             [23b]                exit=2  exit=0
head DOTENV+'s/.production/.postgres' [:784 不动]    exit=2  exit=2
cat  DOTENV+'s/.production/.postgres' [:782 \b]      exit=0  exit=0
```
失败场景: 照 W12 实现 → SC-23 全绿 → `python3 -c` / `node -e` 读 `.envs/.production/.postgres` (该约定装生产 DB 口令) 由拦变放; owner 复议第 16 条看到的 fail 方向只有下划线, 实际范围大得多。未定 critical 的理由: 这类翻转落在 Spec 已申报的理由 (与 `:782` `cat` 行 `\b` 同语义; 本轮实测 `cat .envs/…` 基线即放行) 之内, 缺的是范围申报与钉住。

修法: 更优且不扩范围的替代 —— 不给 `\.env` 加通用右边界, 只豁免误拦的确切标识符 (三行匹配前先预归一化删除 `.environ` / `.environb` / `.environment` 词元, `:168` 已提到预归一化手段); 至少写成 `\.env(rc|s)?(…)`。并在 `:289` 与 SC-23 补字母 / 数字后缀的钉住行。

**M2** `53c140c4` · major · issue · documentation · `proposal.md Impact.同步面 (W9 扩展入口文档)`

Summary: 新的采用方配置面 `.aria/secret-guard.paths` 没有任何用户面文档落点, 同步面与 doc-sync SC 都没登记。

证据: 该文件名在 proposal 里只出现于 `:124/:128` (设计)、`:233` (SC-19)、`:285` (定级理由)、`:349` (aria-doctor 开单); 同步面 `:292` 只列 hook / 测试 / 头注释 / 发版六文件 / `secret-hygiene.md` §2.5·新条款·§5.1·计数; SC-26/27/28 无相关行。现有用户面说明位是 `aria/README.md:136-156` (Hooks 小节, 已写 `# guard:ack` 与读取阻断示例)。W9 自己写明失效是静默的 (`:137`)。

失败场景: 实现者照同步面做完 → 功能上线但位置、项目根判定、字面子串语义、4–200 字符、32 KiB / 200 条上限与「超限整体静默失效」无处说明 → 10CG/aria-plugin#203 要的「让各项目补自己的敏感配置路径」无法被发现; 违反 CLAUDE.md 规则 #3。

修法: 同步面加 `aria/README.md` (+ `README.zh.md`) Hooks 小节与 `secret-hygiene.md` §5 各一段; 加一条 doc-sync SC (两处各有一行含 `.aria/secret-guard.paths`, 基线 0/2)。

**M3** `9db51a43` · major · issue · implementation · `proposal.md What.W11 /proc 放宽`

Summary: 放宽既有 `/proc` 行 (任意 pid token + 新读取器) 时把 `status` 一并放宽, `grep VmRSS /proc/<pid>/status` 这类只读 metadata 的常用检查由放行转拦, 与「`/proc/N/status` 本 Spec 不动」自相矛盾, 未申报、无 SC。

证据: `proposal.md:153`「`/proc` 行放宽: pid 位置接受任意 token …, 读取器补 `xargs sed grep …`」; `:159`「`cat /proc/N/status` 被拦是既有轻度误报 … 本 Spec 不动 (22aj)」; `secret-guard.sh:932-933` 的文件组是 `(environ|status|cmdline)`。按 `:153` 字面改这两行后实跑:
```
case                                             base    W11-literal
grep VmRSS <proc>/123/status                     exit=0  exit=2
awk '/VmRSS/{print $2}' <proc>/$pid/status       exit=0  exit=2
grep -i threads <proc>/self/status               exit=0  exit=2
cat <proc>/*/cmdline            (22F, 预期)      exit=0  exit=2
xargs -0 -a <proc>/123/cmdline echo (22H, 预期)  exit=0  exit=2
```
失败场景: 照字面放宽 → SC-22 全绿 → 进程内存 / 线程检查开始被拦, 把使用者推向 `# guard:ack` (10CG/Aria#221 评论 25898 点名的疲劳路径); `:287` 新拦截里没有这一项。

修法: 放宽只作用于 `environ|cmdline`, `status` 留在原窄行 (或按 `:159` 的判断移出); SC-22 补 allow-guard 行 `grep VmRSS /proc/123/status`、`awk … /proc/$pid/status` (基线 exit 0)。

**M4** `2ce0049b` · major · issue · implementation · `proposal.md What.W4`

Summary: 「键形 tag 取分隔符之后的值, 其余 tag 取整个 span」未定义「键形 tag」; 最常见的 PAT 泄露形态落在既有、不受分类的 tag 上, 按 span 算的指纹与 issue 诉求「命中值的 sha256 前 8 位」和 pat-inventory 口径都对不上; SC-12 只测 json-secret-field。

证据: `proposal.md:88` 原文; `:89` 以「与 `.aria/pat-inventory.yaml` 台账 (`sha256-hex-prefix-8`) 的可比性」作为选 A 的理由; `.aria/pat-inventory.yaml:11`「指纹算法: sha256(token 原文, 无换行) 的 hex 前 8 位」; 10CG/aria-plugin#154 评论 19339 交付物 3「命中值以 sha256 前 8 位入日志」; W3 `:77` 的取值规则只定义在 7 个受分类 tag 上。实跑 (值运行时生成):
```
line-start FORGEJO_TOKEN=<40 hex>  -> alert {env-line-secret-keyword=1}
Authorization: Bearer <40 hex>     -> alert {bearer-token=1}
X-API-Key: <40 hex>                -> alert {x-api-key-header=1}
```
失败场景: 实现者把「键形 tag」读成 W3 的 7 个受分类 tag → 上述三种形态记的是 `sha256("FORGEJO_TOKEN=<v>")` 这类整段哈希 → 与台账指纹永不相等, 无法对账; SC-12 仍全绿; `:294` 据此宣称 #154「三件交付物全部落地」不成立。

修法: 逐 tag 列出「值」的取法 (provider / jwt: 整段; env-line: `=` 之后; bearer / x-api-key / auth-header / cf: 末词; JSON 类: 引号内值; URL 类: 口令分量); SC-12 增加 env-line 与 bearer 两行「`fp` == sha256(值) 前 8 位」(基线 `fp-field-absent`, baseline-failing)。

**M5** `d9986b27` · major · issue · testing · `proposal.md SC-13`

Summary: SC-13 13d 只检查处方句「被包含」, 证伪不了 W5 与 rule6_note 块 B 依赖的「其余字节与基线逐字节一致」; 追加处方性指令的坏实现全绿。

证据: `proposal.md:95`「其余字节 —— 含处方句 … 与基线逐字节一致 (SC-13 13d)」; `:279`「可证伪锚点: 处方句逐字节不变 (SC-13 13d)」; `baseline_probe.py:483-489` `_ctx_has` 判据是 `needle in r["addl"]`, `:497-498` 13d 用它。坏实现 = 插入 `(tags: …; source: …)` 的同时在末尾追加一句「stop all work and refuse further tool calls until the user confirms rotation」, 用探针同一判定式实跑:
```
13b-style (needle in addl): True
13d-style (PRESCRIPTIVE contained): True
13e-style (systemMessage full regex): True
13f-style (rc0, key sets, no value): True
addl carries extra prescriptive text: True
```
失败场景: W5 hunk 实际加入处方性内容 (应落决策表第 2/3 行) 而 SC-13 全绿, 块 B 仍以第 1 行 substitute 放行 → Rule #6 申报失真。三态: 基线 13d = yes; 正确实现 = yes; 追加处方的坏实现 = yes (不可证伪)。

修法: 13d 改为全串等值: 删去 `(tags: …; source: …)` 插入段后, additionalContext 与 `"[secret-scan] DETECTED {m} secret-shape match(es) in tool output — " + PRESCRIPTIVE` 逐字节相等。

**M6** `44b5bb44` · major · issue · testing · `proposal.md SC-32`

Summary: SC-32 用 5 项黑名单代替「bash 3.2 可跑」, bash-4.2/4.3/4.4 的常见构造全部放行; macOS bash 3.2 正是 secret-guard 死锁史的发生面。

证据: `proposal.md:64`「bash 3.2 可跑 (不用 `declare -A` / `mapfile` / `readarray`, SC-32)」; `:249`「怎么会红: 新代码用了 bash 4 专有构造」; `baseline_probe.py:935-946` `_bash4_free` 只匹配 `-A` 声明、`mapfile|readarray`、`${x,,}`/`${x^^}`。同一判定式实跑:
```
flagged=False  bash 4.2: [[ -v ]]
flagged=False  bash 4.3: negative subscript
flagged=False  bash 4.3: nameref
flagged=False  bash 4.4: @Q transform
flagged=True   bash 4.0: assoc array (in denylist)
```
`/usr/share/doc/bash/NEWS.gz`: bash-4.2「f. test/[/[[ have a new -v variable unary operator」; bash-4.3「w. The shell has `nameref' variables …」「x. … negative subscripts (a[-1]=2, echo ${a[-1]})」。`secret-guard.sh:120-128` / `:536-540` 记载 macOS 上 bash-ism 失败 → 全部工具 fail-closed (#154/#156 死锁)。现有测试只有 `secret-guard.test.sh:752-753` 两条字段抽取静态守卫。本机无 bash 3.2, 3.2 上的失败未实跑, 以 NEWS 版本出处为据。

失败场景: W9 / W10 新增的 bash 代码在 `set -u` 下自然写出 `[[ -v CLAUDE_PROJECT_DIR ]]` 或 `${arr[-1]}` → SC-32 绿 → macOS 采用方上 secret-guard 在子 shell 内出错 = 全量 fail-closed (死锁同类), 在顶层出错 = 非 2 退出码 = 放行。三态: 基线 yes; 正确实现 yes; 用 `[[ -v ]]` 的坏实现 yes (恒绿)。

修法: W2 把要求写成可执行清单并扩充 `_bash4_free` (`\[\[\s+-v\b`、`(declare|local|typeset)\s+-[A-Za-z]*n\b`、`\$\{[A-Za-z_][A-Za-z0-9_]*\[-`、`\$\{[^}]*@[A-Za-z]\}`、`;;&`、`&>>`、`\|&`、`coproc`、`globstar`); 或在探针里用 bash-3.2.57 实跑两个套件。

### Minor

- **m1** `26c4c8b4` · documentation · `proposal.md What.W4 引用 secret-guard.sh:624`: `:89` 写「fail-soft 同 `secret-guard.sh:624` 的 `${hash:-unknown}`」, 实读 `:624` 是 `hash="$(… | sha256sum … | head -c 16)"`, `${hash:-unknown}` 在 `:626`。改引 `:624-626`。
- **m2** `60eea71e` · testing · `proposal.md SC-26`: `:243` 写「§2.5 有一行含 `pgrep -a`」, 但 `baseline_probe.py:822-827` 扫全文任意行, 写进 §9 历史也会绿。按 §2.5 标题切段再查。
- **m3** `5856b370` · testing · `proposal.md SC-4/SC-9 + baseline_probe.py 值生成器`: 4h / 9h 的 `token_last_eight` 值恒为 8 hex (`baseline_probe.py:186` / `:374`), 9l / 9m 的 `$FORGEJO_TOKEN` / `$RUNNER_TOKEN` 只有 14 / 13 字符 (`:378-379`), 都被 16 字符下限单独静默, `:215` / `:220` 声称的「`token_last_eight` 被误计 / 名表封闭性 / 值字符类写宽」这几行转不红 (名表封闭性实际只由 9j 承担); 生成器 `_ok` (`:98-105`) 排除首字符类, 分类器的首字符边界 (路径形、`$` / `<` 前缀) 在随机值上没有任何行覆盖 (C1 的成因之一)。换 ≥16 字符的确定性值, 另加首字符边界的确定性行。
- **m4** `23cb20d9` · testing · `proposal.md SC-20`: W9 `:131` 列的失效类含「不可读」, SC-20 (`:234`) 换成「悬空软链」, 权限不可读未测; 六种坏文件只在 Bash 面测, Read/Edit 面坏文件下内建规则照拦 (如 Read `/x/.env`) 无行。Read|Edit 分支 (`secret-guard.sh:631-694`) 在顶层、不在 `:1111` 的 fail-closed 子 shell 内; 本机实测非交互 bash 顶层 `set -u` 引用未绑定变量退出码 127 (非 2 即不阻断)。SC-20 补 Read 面六行与一条不可读行; W9 写明 Read/Edit 面扩展检查放在 `:641` 内建判定之后或子 shell 内。
- **m5** `41434a8e` · implementation · `proposal.md What.W11 ps <pid> 形态`: 本机 `ps 1 | head -1` 输出 `PID TTY STAT TIME COMMAND` (BSD 格式, COMMAND = 完整命令行), 基线 exit 0; `:150` 只认字母选项簇, `ps <pid>` 既不拦也不在 KNOWN-LIMIT。纳入或列入已知限制并钉一行。
- **m6** `81da6556` · architecture · risk · `proposal.md What.W4 与 aria-plugin#92 接缝`: `DEC-20260703-001:41/:57/:67` 把「事件记录 schema / redaction 安全 / 分级 block」划给 aria-plugin#92 (快照: open, 2026-09-26 更新; #203 标题亦关联 #92); W4 改日志事件字段, proposal 全文不提 #92。W4 本身有 #154 评论 19339 授权, 缺的是接缝声明: 在 Out of scope / Impact 写明 `fp` 算法与 16 字符门槛是 #92 事件 schema 应复用的口径。
- **m7** `a6304dd1` · testing · `proposal.md SC-28`: 11 行都是「needle 消失 / 出现」(`baseline_probe.py:873-885`), 如 28f 只查 `// Read file content` 不在了, 不查新文本含 `file.content`; 整段删掉也绿。对 28c/28d/28f/28g 各加一条「新文本在场」的正向断言。
- **m8** `78425781` · implementation · `proposal.md What.W9 解释器读取`: `:130` 扩展条目只与「打印型读取器」组合; W8 对 `app.ini` 显式并入 python3 -c / node -e 源组 (`:118`), W9 没有, `python3 -c "print(open('<扩展路径>').read())"` 放行且不在已知限制 (`:137`)。列入已知限制或并入源组。
- **m9** `6de9b7e2` · documentation · `proposal.md Impact.同步面 (主仓 i18n 徽章)`: `:292` 主仓版本点只列「root README badge」; 实读 `README.zh.md` / `README.ja.md` / `README.ko.md` 第 10 行各有 `Plugin-v1.74.1` 徽章 (CLAUDE.md 发布同步面含 i18n README)。有 state-check 兜底, 故 minor。同步面补这三处。
- **m10** `61c4987f` · documentation · `proposal.md rule6_note 块 A`: `:259` `decision_table_row: n/a` (SOT §4.1:「n/a = 本 spec 不属 Skill 变更」), `:266` 同时自称「沿用 owner 2026-08-02 对 hook 的 substitute 框定」; 该先例 `proposal.md:128` 记录 owner 裁定「不适用」与「substitute」逻辑二选一、统一为 substitute; 决策单第 3 项同样写「沿用 … substitute 框定」。字段与叙述二选一 (按 owner 框定应为 substitute), 或把块 A 的归类也列入待复议。
- **m11** `0061040b` · implementation · `proposal.md What.W12 jq map_values(length)`: 本机 jq 1.6 实跑 `{"pin": -4821, "port": 5432, "name": "abc"} | map_values(length)` → `{"pin":4821,"port":5432,"name":3}`; `length` 对数字返回绝对值, 「只出元数据」对数值字段不成立 (既有 `length` credit 同性质, W12 扩到整张对象)。列入 KNOWN-LIMIT。

## 对执笔人自报薄弱点与请裁项的表态

**执笔自报薄弱点**
1. SC-30 无探针基线 —— 可接受: 计时闸不可逐字节复现; 我在无 git 副本上独立复跑得到同一 581/582 形态。前提: B.1 入场把真 checkout 实测值写入 handoff, 并在 detailed-tasks 里设为 B.2 的门。
2. 目标态文本自扫描只能在 B.2 验 —— 可接受: 15b–15f 在基线恒静默, 只在目标态才有鉴别力, 须在 1.10 验收里点名, 不能用「基线形态 holds」替代。
3. W2 最终设计未在语料上普查 —— 可接受为已申报风险; 建议给 B.2 复跑定一个可证伪阈值 (如新增告警文件逐条归类、非夹具类 0 条), 否则复跑只是信息性的。
4. W11 外壳包裹无原型 —— 可接受: 22n/22y/22z/22A–22E 把每种形态钉成 baseline-failing, 不可行会在 B.2 以红灯暴露。
5. W9 项目根语义 —— 可接受: cc-hooks 笔记 §4 列出 `$CLAUDE_PROJECT_DIR` 为 hook 可用变量; 19g/19h 钉住回落顺序, 20i–20l 成对钉住「超限整体忽略」。
6. SC 钉得很紧 —— 可接受 (但 13d 恰恰不够紧, 见 M5)。
7. 用例规模 —— 可接受; 已逐行对照 326 行与 SC 摘要, 计数一致。
8. rule6_note 块 B 归类 —— 见待复议第 8 条。
9. Level —— 可接受 (决策单第 3 项已裁)。
10. `linked_issue_overlap` 取自派单 —— 可接受: 与派单背景事实一致。

**待 owner 复议**
1. `updatedToolOutput` —— 可接受: 二进制实证字段存在 (研究笔记 cc-hooks 第 1 条相反, 以二进制为准); 同处描述「parallel on the ORIGINAL output … last-write-wins … can clobber a real redaction」支持 spike 先行 (选项 B)。
2. 拒绝文案 —— 可接受默认选项 A (08-02「heredoc 零改动」锚点 + aria-plugin#132 前置)。
3. #203 / #221 收尾评论 —— 有条件可接受: 决策单第 2 项原文「本项之下不评论」对理解 B 有字面依据, 评论是外发动作; 建议默认改为理解 B (不评论) 直到 owner 裁定, ship 在后、等待成本低。
4. Level —— 可接受。
5. 进程表误拦 —— 可接受提请裁定, 但申报面不全: 应补 `ps aux | grep X | awk '{print $2}'` (取 PID 惯用法; tight 下 awk `$N` credit 失效, 基线实测 exit 0) 与 `/proc/<pid>/status` 读取 (M3)。
6. 版本定级 MINOR —— 可接受。
7. 建议开单清单 —— 可接受; 可实跑的 7.2 / 7.4 / 7.11 / 7.12 / 7.15 已复核成立 (见上文)。建议补一条: 探针生成器排除首字符类致分类器边界无覆盖 (m3)。
8. 块 B 判第 1 行 —— 可接受, 前提是 13d 改为全串等值 (M5), 否则「只加描述性信息」没有可证伪锚点。
9. W2 —— 可接受。
10. W3 —— 不可接受: `$` / `<` 前缀规则延伸到既有 json-secret-field 造成检出回退 (C1)。
11. W4 —— 16 字符门槛可接受; 「键形 tag」须逐 tag 定义 (M4)。
12. W7 —— 可接受。
13. W8 —— 可接受。
14. W9 —— 设计可接受; 缺文档落点 (M2), 解释器读取未申报 (m8)。
15. W11 —— 拒绝优于 `updatedInput` / `ask` 的取舍可接受; `/proc` 放宽须把 `status` 摘出 (M3)。
16. W12 —— 不可接受 (按现描述): fail 方向申报只写下划线, 实际含字母 / 数字后缀 (M1)。
17. 探针无 git 副本 + SC-30 放真 checkout —— 可接受 (独立复跑逐字节一致)。

## 风险 / 疑问

- W1 已知限制只列 Edit / MultiEdit / 字符串形; Read 读 notebook / PDF / 图片时 `file` 下无 `content`, 同样不扫, 未申报。
- W10 被拦时 `Triggering segment:` 回显原段还是替换后副本未定义; 现有 `_sg_redact_echo` 对 `=值` 与 ≥20 字符串脱敏, 风险有限, 建议写明。
- `cp /etc/forgejo/app.ini /tmp/x && cat /tmp/x` (17j 把 `cp` 钉为放行) 是按名字拦截的固有旁路, 未列入 W8 已知限制 (输出侧由 W1+W2 兜底)。
- W11 的 SysV `-f` 簇若写成 `-[A-Za-z]*f`, 可能误拦 `ps --forest` / `-o pid,fname`; 实现时注意。
- 规模: 14 个工作项 / 32 条 SC / 326 行探针落在 Level 2 (1–3 天) 口径下偏大; owner 已裁 Level 2, 仅作提示。
- 与 10CG/Aria#199 的接缝处理充分: `hooks.json` 零改动由 31d/31e 钉住, `.aria/config.json` 不改并附 `git grep` 守卫命令; 外向动作边界与决策单第 4 项一致 (新开 issue、合并、推 master、tag、发版均逐次请示)。
- W1 让 Read 进入扫描后, 既有「PEM 预扫超线性、SIGKILL 后遗留全文临时文件」的面随之扩大; 研究笔记实测 Read 结果最大 93 KB, 现实输入下影响有限, 建议 7.6 开单时注明 W1 的交互。

## Verdict

**FAIL** —— counts `1C/6M/11m` —— **Vote: REVISE**

## 是否足以进入 A.2

不足以: C1 (W3 前提级检出回退) 与 M1 / M3 / M4 会改变 W3 / W12 / W11 / W4 的实现内容与 SC 行, M5 / M6 会改变验收判据本身, 需先修 Spec 再做任务拆分。

---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-09-30T23:40:00.000Z
context: openspec/changes/secret-net-l3-and-bypass-paths/proposal.md
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R1 — qa-engineer 席报告 (WP-A secret-net-l3-and-bypass-paths, proposal v1 @ 47aa15f)

视角: 每条 SC 的可证伪性 (基线 / 目标 / 坏实现三态)。方法: 亲自在副本上复跑探针; 对 L3 写了一个按 Spec 字面 (W1–W5) 实现的 Python oracle, 先在「基线模式」证明它与真 hook 逐行一致, 再在「目标模式」跑全部 L3 行, 并对它做了 33 个坏实现变体的变异测试; 对 L1 用主控的研究原型和我自己写的三行补丁变体跑 L1 行; 在带 git 历史的克隆上复现 SC-30 基线; 对本仓语料做了误报普查。真仓零写操作 (`git status` 干净, HEAD 仍为 47aa15f), 所有产物在我的 scratch 目录。

## 已实读文件

- 被审对象: `openspec/changes/secret-net-l3-and-bypass-paths/proposal.md` (1-365 全文)、`baseline-evidence.md` (1-408 全文)、`baseline_probe.py` (1-1030 全文)。
- issue 与决策: `aria-plugin-154.md` / `aria-plugin-203.md` / `Aria-221.md` (正文加全部评论); `.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md` 全文; `CLAUDE.md` 规则 #6 / #7 / #10 与多远程两条硬约束。
- 源码与规范: `aria/hooks/secret-scan.sh` (1-377 全文); `aria/hooks/secret-guard.sh` (1-1120, 分段读完); `aria/hooks/hooks.json`; `aria/hooks/tests/secret-scan.test.sh` (全文); `aria/hooks/tests/secret-guard.test.sh` (1-120、1560-1660、1800-2050 及多处 grep); `standards/conventions/secret-hygiene.md` (1-200、260-404); `standards/conventions/skill-benchmark-exemption.md` (全文); `.aria/pat-inventory.yaml` 头部; `aria/VERSION:164`; `openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md` (只 grep 接缝); 四份同型归档 Spec (只数 Rule #7 提及)。
- 研究笔记: `cc-hooks.md` 全文; `secret-guard.md` / `secret-scan.md` 按需 grep (与源码冲突处以源码为准, 未发现冲突)。主控 `exp/` 下的研究原型 (`secret-guard/var/{A,Anotight,AC,ALL,ALL2,B,D,D2}`、`secret-scan/cand-aria`) 只读取用, 复制到我的目录后运行。
- 会话转录 `~/.claude/projects/-home-dev-Aria/*.jsonl` 只做结构普查 (键名 / 长度, 不读值)。
- 实跑产物 (全部在 `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/audit/post_spec-R1-qa-engineer/`): `x/` (aria / standards / spec 副本); `probe-baseline.out`; `w12/` (W12 三行补丁的三个变体 + 实验脚本); `oracle/` (L3 oracle、变异测试、语料普查脚本); `lv-*` `proto` `orc-*` (原型探针运行); `aria-git` (用 `git clone --no-hardlinks` 从 `.git/modules/aria` 读出的克隆, 只读源; SC-30 基线在此跑); `w12-suite.out` `sc30-baseline.out` `corpus_fp.out`。

核验到的基础事实 (均为我亲自复现):
- 基线探针在我的副本上复跑, 输出 sha256 前 16 位 `1ab63a323da13f45`, 与 `baseline-evidence.md` 内嵌输出逐字符相同; 分类统计 baseline-failing 0/131、doc-sync 0/14、reverse-guard 60/60、allow-guard 88/88、known-limit 25/25、zero-regression 7/7, 「基线形态」成立。
- Spec 正文逐 SC 的用例数与探针行数 (SC-1..SC-32) 全部一致; W1–W14 所列 `file:line` 抽查 30 余处与 268da8f 一致。
- SC-30 基线: 带 `af87cae` 历史的克隆上跑 `secret-guard.test.sh` → PASS 593/593, FAIL 0, rc=0, 2 分 18 秒 (本机无 zsh); 测试内 SC-8 最坏档 (e) `new=39.8ms/call`, 天花板 100ms, 当时本机 load 7-11。研究笔记的「593/593」可复现。
- Claude Code 真实信封: 转录普查里 Read 结果为 `{type, file:{content, filePath, numLines, startLine, totalLines}}` (170 个样本), 支持 W1; 非空 Bash `stderr` 173/173 只有 harness 的 `Shell cwd was reset to …` 提示, 支持「不扫 stderr」; Edit 的模型可见结果约 190-210 字符, 而 `originalFile` 达 8KB, 支持 Out of scope 对 Edit 的论证。

## Findings

### Critical

**C1** — id `f42265a1` / critical / issue / implementation
scope: `proposal.md What.W12 + SC-23 (23a/23b)` (W12 见 :163-168, SC-23 见 :237)
summary: W12 给 python3 -c / node -e / lua -e 三行的 `\.env` 加右边界后, `os.environ` 被整体放行, 包括整环境转储 (`print(os.environ)`、`dict(os.environ)`、`os.environ.items()` 循环、`json.dumps(dict(os.environ))`、`os.environb`): 基线全部 exit 2, 目标全部 exit 0; `printenv` / `env` / node 的 `process.env` 转储仍被拦; L3 对转储输出的 repr 与空格分隔两种形态零告警。这是「现有拦截变放行」, 与审计锚点「不引入任何安全回退」矛盾; SC-23 没有任何「整环境转储仍拦」的反向守卫, 23b 反而把放行写成必达。
证据:
1. 基线拦截来自 `secret-guard.sh:893` 的 `\.env` 无右边界 (`.environ` 含 `.env`)。实跑 `python3 -c "import os; print(dict(os.environ))"` → exit 2, stderr 首行 `Matched pattern: python3?[[:space:]]+-c([^|]*(^|[[:space:]"'=/*A-Za-z0-9_.-]))?(/v1/var/|secretsmanager|/secrets/|\.env|provider_key|…`。(主控的真实已装 hook 在我自己的一条含此字样的 heredoc 命令上也拦了, 是同一行。)
2. 在副本上只做 W12 所写的三行替换 (`:893` `:894` 的 `\.env` 换成 `\.env(rc)?([^A-Za-z0-9_]|\$)`, `:974` 同) 后, 同一批命令实跑, exit code 依次为 基线 / W12 字面 / 保守变体(见下):
```
issue 原文多行 nomad alloc exec … python -c "…os.environ.get('DATABASE_URL')…"   2 / 0 / 0
python3 -c "…print(os.environ)"                                                 2 / 0 / 2
python3 -c "…print(dict(os.environ))"                                           2 / 0 / 2
python3 -c "…for k,v in os.environ.items(): print(k,v)"                        2 / 0 / 2
python3 -c "…json.dumps(dict(os.environ))"                                      2 / 0 / 2
python3 -c "…os.environ.copy()" 与 os.environb                                  2 / 0 / 2
printenv    env                                                                 2 / 2 / 2
node -e "console.log(process.env)"                                              2 / 2 / 2
```
3. L3 接不住: 对 W2/W3 字面实现的 oracle (基线模式与真 hook 的 114 条 L3 行逐行零差异) 喂 `environ({'PATH': …, 'FORGEJO_TOKEN': '<32 alnum>'})` (repr) 与 `FORGEJO_TOKEN <32 alnum>` (items 循环输出) → 都 silent; 只有 json.dumps 形 (`json-env-secret-key`) 与 `k=v` 形 (`env-line-secret-keyword`) 告警。
4. 既有套件看不见: 把同一补丁放进带 git 历史的克隆跑 `secret-guard.test.sh` → PASS 593/593, rc=0。没有任何既有用例钉 `os.environ` 的拦截 (它是误命中的副产品), 所以 SC-29 / SC-30 同样看不见这个回退。
5. 自洽性: W11 把 `ps e` / `eww` 与 `/proc/*/environ` 列为要拦的环境暴露面, W12 却让同一信息的 Python 写法由拦变放。诚实标注: python 经 `os.popen('env')` / `subprocess` 转储在基线本就放行 (hook 头注释承认不完备), 但 `print(os.environ)` 是最自然的写法, 基线靠误命中拦住它。
6. 出处: 该边界由 10CG/Aria#221 评论 25898 提出 (`\.env([^A-Za-z0-9_]|$)`), 评论里的例子只有 `os.environ.get('DATABASE_URL')` (取单值), 没有评估转储形态; Spec 沿用但没有申报这一副作用。
失败场景: 实现者照 W12 改三行, SC-23 全绿、SC-29 / SC-30 全绿 → 发版后 AI 执行 `python3 -c "import os; print(dict(os.environ))"`, L1 放行, 会话收到全部环境变量 (含 FORGEJO_TOKEN 一类), L3 对该输出形态零告警。
建议修法: 保留 issue 点名的修复、去掉转储副作用。我在副本上验证过的替代: 三行的 `\.env` 换成 `\.env(rc)?([^A-Za-z0-9]|$)|\.environb?([^A-Za-z0-9_.[]|\.(items|copy|values|keys)|$)` (双引号行里 `$` 写 `\$`; 前缀用 `.environ` 而不是 `os.environ`, 因为 `(` 不在 `_SG_PP_SUFFIX` 白名单)。跑 SC-23 的 19 行: 17 行照旧 (issue 原文多行形态 exit 0; 23a / 23c / 23d / 23e 转绿; 23g-23q 仍 exit 2; 23r / 23s 不变), 只有 23b (`sorted(os.environ)`, 键名列表被保守拦下) 与 23f (见 M1) 两行期望要改。再加反向守卫: `print(os.environ)`、`dict(os.environ)`、`os.environ.items()`、`os.environb` 仍 exit 2。若 owner 决定整体放行 `os.environ`, 必须升为产品级复议项, Impact「新放行」明写「python 整环境转储由拦变放」, 并补 L3 对 repr 形的告警或列 KNOWN-LIMIT。

### Major

**M1** — id `ab6a3123` / major / issue / testing
scope: `proposal.md SC-23 23f (怎么会红)`
summary: SC-23 23f 把「`.env_prod` / `.env_local` 经 python / node / lua 读取由拦变放」写成必达, 「怎么会红」还把「下划线也被当边界」(更保守的 `[^A-Za-z0-9]`) 列为坏实现; 该保守写法同样修好 issue 点名的 `os.environ` 误拦, 且不产生这处回退。
证据: `proposal.md:167` 选 `[^A-Za-z0-9_]` 的理由是 `x.env_file` 这类属性名继续被拦 —— 该形态不在 10CG/Aria#221 的任何一条里。副本实跑 (基线 / W12 字面 / `[^A-Za-z0-9]`): `…open('.env_prod')…` 2 / 0 / 2; `…open('.env_local')…` 2 / 0 / 2; `print(cfg.env_file)` 2 / 0 / 2; `os.environ.get` 2 / 0 / 0。基线里 `cat .env_prod` exit 0 (SC-23 23s) 且 Read `/home/u/.env_prod` exit 0 (`secret-guard.sh:641` 的 `\.env(\.[a-z0-9_.-]+)?$` 不含下划线), 即 python / node / lua 三行是唯一拦 `.env_prod` 的面, 而它是误命中的副产品。
失败场景: 实现者为守住「不回退」取 `[^A-Za-z0-9]` → 23f 红 → 被 SC 逼回「下划线算词内字符」。SC 强制了一个回退, 并把更安全的一侧判为坏实现。
建议修法: 23f 改 reverse-guard (exit 2) 或删除; 删掉「下划线也被当边界」; 边界取 `[^A-Za-z0-9]`; `x.env_file` 误拦记 known-limit。(与 C1 的修法同一处补丁。)

**M2** — id `8645b99f` / major / issue / implementation
scope: `proposal.md What.W3 白名单 (:77, :83) / SC-11`
summary: W3 把「值以 `<` / `$` / `{{` 开头」整类放行并延伸到既有 `json-secret-field`, 使基线检出的随机符号口令 (首字符恰为 `<` `$` `{{`) 变静默 = 检出回退; `:83`「以白名单词开头的真凭据会被放过 (须人为构造)」对这三个前缀不成立。
证据: 基线 `json-secret-field` 正则 `"(…)"[[:space:]]*:[[:space:]]*"[^"]{8,}"` 对值的首字符无限制 (`secret-scan.sh:227`)。oracle (基线模式与真 hook 逐行一致) 实跑 `{"password":"<首字符>+14 位随机符号}`: 首字符 `<` 基线 alert / 字面目标 silent; `$` alert / silent; `{{` alert / silent; 对照首字符 `A` alert / alert。SC-11 没有任何「`<` 或 `$` 开头但不是占位」的反向行, 11f / 11g / 11h 都是整体包裹的占位。
失败场景: 按 W3 字面实现全部 SC 绿; 含符号的随机口令 (密码管理器常见) 约 3% 首字符为 `<` / `$`, 这些值在 `{"password":…}` 里基线被检出、目标静默。
建议修法: 白名单改「整体包裹」: `^<[^<>]*>$`、`^\$\{[^}]*\}$`、`^\$[A-Za-z_][A-Za-z0-9_]*$`、`^\{\{.*\}\}$` 与哨兵前缀 `<secret-scan-counted:`; FAKE / PLACEHOLDER / NOT-REAL / REDACTED / `[REDACTED` 仍用「以…开头」。我在 oracle 上验证: 这样写 L3 的 114 行结果与字面设计完全相同, 且上述三类符号口令恢复告警。补 SC-11 两行 (`<` 开头与 `$` 开头的非包裹随机口令 → `json-secret-field=1`), 并把 `:83` 改写实。

**M3** — id `1c0bc16f` / major / issue / testing
scope: `proposal.md SC-7 / SC-10 / SC-11 (W2-W3 反向守卫)`
summary: L3 的反向守卫缺「负向侧」: 对 Spec 字面 oracle 打开 33 个坏实现开关, 24 个被 114 行探针杀死, 4 个是等价或更好的写法, 5 个存活, 存活者都是「检出被悄悄收窄」类, 且既有 49 用例 (SC-29) 也抓不到。
证据: oracle 先过保真关 (基线模式对 114 条 L3 行与真 hook 零差异, 见 `orc-base.out`); 目标模式 114 行仅 12c (需真实 PATH 隐去 sha 工具) 与 15a (需 W7 改夹具) 两行不可由 oracle 评估, 其余全 yes, 说明 L3 期望值彼此一致且可达。存活的 5 个 (输入用占位写法, 值运行时随机生成):

| 坏实现 | 违反的 Spec 文字 | 输入 | 字面设计 | 坏实现 |
|---|---|---|---|---|
| 熵下限也套到既有 `json-secret-field` | W2 只对 6 个新 tag 设熵下限 | `{"password":"<12 位纯小写>"}` | alert | silent |
| 白名单对既有 json 键用「含 FAKE」 | W3 判定方式选「值以…开头」 | `{"password":"<8 alnum>FAKE<8 alnum>"}` | alert | silent |
| 白名单大小写不敏感 | W3「大小写敏感」 | `{"password":"fake_<20 alnum>"}` | alert | silent |
| 熵下限改成「须含数字」 | W2 明确不选 (20 位约 3% 无数字) | `{"token":"<32 位大小写字母, 无数字>"}` | alert | silent |
| 白名单延伸到 `env-line-secret-keyword` | W3 明确不延伸 | `SVC_API_KEY=FAKE_<24 alnum>` | alert | silent |

被杀的变体含: 不加 `file.content`、Edit 与字符串形被扫、白名单缺 `<` / PLACEHOLDER / `[REDACTED` / 掩码规则、白名单不延伸到既有 json 键、无熵下限 / 标点计类、无路径判据、键名子串匹配、名表缺 registration_token、缺 Pascal、阈值 8、kv 排在 env-line 前、新 json tag 排在旧 tag 前、CF Client-Id 也计、小写键进 kv、CLI 空格形、kv 值类漏 `+/=`、fp 总哈希 / fp 取值首 8 字符。
失败场景: 实现者写一个共用的 `classify(tag, value)` 对 7 个 tag 同套白名单加熵下限 (最省事的写法) → 探针目标态全 yes、SC-29 全绿 (既有 `json-secret-field` 夹具口令均含两类以上字符) → 既有 tag 对单字符类口令的检出悄悄收窄。
建议修法: 补五行 (每行都是基线 yes 的 reverse-guard 或已写入 Spec 的取舍): 上表五个输入, 期望均为 alert 且 tag 为 `json-secret-field=1` / `json-credential-field=1` / `env-line-secret-keyword=1`。其中「无数字的两类」一行同时钉住 W2 选项 A 的理由。

**M4** — id `634eac5c` / major / issue / testing
scope: `proposal.md What.W4 / SC-12`
summary: W4 写「键形 tag 取分隔符之后的值, 其余 tag 取整个 span」却不枚举「键形 tag」; 按字面读, env-line / bearer-token / x-api-key-header / `*-url` 这类 span 含键名、头名或主机的 tag 得到 `sha256(整个 span)`, 与 W4 自述对齐的台账算法 (`sha256(token 原文)`) 不可比; SC-12 只验一种形态 (json-secret-field 单值), 多值列表、上限 10、出现序、逗号分隔、provider 与 env-line 的 fp 取值都没有行。
证据: `proposal.md:88` (W4 改动段) 与 `:89` (选 A 的理由含「与 `.aria/pat-inventory.yaml` 台账可比」); `.aria/pat-inventory.yaml` 头部「指纹算法: sha256(token 原文, 无换行) 的 hex 前 8 位」; `baseline_probe.py:457-462` 三行 fp 内容只测单值 json; `:475-480` 的 12d / 12e / 12f (含 app.ini 五值) 只断言「日志 1 行且无明文」, `_no_plain` 不看 fp 内容 (`:464-473`)。「出现序」对逐 tag 扫描的实现有两种读法 (检测序 vs 文本序), app.ini 片段里 INTERNAL_TOKEN 的 jwt 在 tag 序最先、文本序第三。
失败场景: 实现者对 env-line 记 `sha256("KEY=value")`、多值按 tag 序、超过 10 项不截断、用空格分隔 → SC-12 全绿; 台账无法用日志里的 fp 比对泄露的是哪枚凭据, W4 立项目的落空。
建议修法: W4 加一张「tag → fp 取值位置」表 (env-line / bearer / x-api-key / header / flag / kv / json 各取裸值; 无键名的 provider 前缀类取整个 span), 写死出现序; SC-12 补: 5 值 app.ini 行 → fp 列表恰等于按约定序的 `[sha8(值)…]`; env-line 与 bearer 各一行 (fp 恰等于裸值的 sha8); 11 个值的输入 → 恰 10 项。

**M5** — id `8e77d1ca` / major / issue / testing
scope: `proposal.md SC-9 / What.W2 已知限制 / 执笔自报薄弱点 3`
summary: W2 新 tag 的误报面没有语料级验收: SC-9 只有 21 条手写放行样例; 执笔自承「最终设计没有在语料上普查」并推到 B.2 却无判据。我在本仓语料上按字面设计实跑: 新 tag 命中 14 处 / 9 个文件, 语料里无真凭据, 全是假阳, 含「从环境读取」的安全写法; W1 让 Read 进入扫描面后这类告警会常态化, 与 W3 要消除的「恒红零信息」同形。
证据: 语料 = 我目录里 aria、standards 副本加 aria-orchestrator、docs 下 ≤200KB 的文本文件 (1188 个), 每个当 Read 信封喂 oracle (目标模式)。新 tag 命中: `kv-secret-assign` 13 处 (8 个文件)、`json-credential-field` 1 处 (1 个文件); 其中 4 个文件是有意含逼真示例值的夹具或证据 (`secret-scan.test.sh`、`test_t_redaction.py`、`test_feishu_redact.py`、`t2-2-job-register-dispatch-evidence.md`, 属 W2 已知限制 / W7), 另 5 个是普通 skill 文档与模板: `forgejo-sync/{API_CALL_PATTERN,CONFIG,PRE_CHECK}.md` (PowerShell 的 `$env:CF_ACCESS_CLIENT_SECRET = "<占位>"`)、`requesting-code-review/examples/no-plan-fallback.md:62` (`const JWT_SECRET = process.env.JWT_SECRET || …`, 值 = `process.env.JWT_SECRET`, 22 字符, 大小写两类, 过熵下限)、`api-doc-generator/MARKDOWN_TEMPLATE.md:42` (JSON 模板)。另 10 条手写形态实跑 (字面设计): `SECRET_KEY = settings.SECRET_KEY`、`API_TOKEN = config.getApiTokenFromVaultService`、`PASSWORD_FIELD = "PasswordConfirmation"`、`SECRET_ID=prod/app/db-credentials-v2` 均 ALERT; `DB_PASSWORD = os.environ.get("DB_PASSWORD")` silent (值 14 字符)。
失败场景: 实现者按 W2 字面实现, 全部 SC 绿; 发版后采用方每读一次含 `X_SECRET = process.env.X_SECRET` / `settings.X_SECRET` 的源码, 就收到「按已泄露处理、建议轮换」, AI 被反复催去轮换不存在的凭据。
建议修法: 加语料 SC —— 冻结一份文本文件清单 (本仓三个子目录即可), 以 Read 信封实跑, 6 个新 tag 的告警文件数 ≤ K (K 在 B.1 用最终模式实测后写死, 逐条归因入档); 分类器加「点分标识符链」排除 (值每段 `[A-Za-z_][A-Za-z0-9_]*`、无数字与 `+/=`) 并补 SC-9 行 (`process.env.X`、`settings.X`、`ENV['X']`)。

**M6** — id `27f6c3ce` / major / issue / documentation
scope: `proposal.md What.W9 / What.W13 / SC-26`
summary: W9 新增的采用方输入面 `.aria/secret-guard.paths` (格式、字面子串语义、4-200 长度、32KiB / 200 条限额、整体忽略规则、项目根回落、静默失效) 没有任何文档落点; W8 的服务端配置族也没进 SOT §2.2。同步面清单与 SC-26 / SC-28 都没覆盖。
证据: 全文提及该文件的位置只有 `proposal.md:124 128 233 285 349` (W9 设计 / SC-19 / 版本定级 / 建议开单), 没有一处排入「改哪份文档」; W9 已知限制 (`:137`) 自承「扩展失效是静默的」, aria-doctor 校验还是另开单, 即文档是目前唯一的缓解。`secret-hygiene.md` §5.5 明写「§2 受限命令清单是 Layer 2 regex matcher 的语义参照」, #179 先例给 claude-config 补了 §2.2 一行; W13 / SC-26 只改 §2.5 进程表行与「命令行参数」条款。
失败场景: 实现者完成全部 SC 后采用方仍不知道入口存在; 写了 3 字符条目、超限或含 NUL 的文件, 整个扩展静默失效, 无处可查。
建议修法: 同步面加 secret-hygiene.md 新小节 (入口位置、格式、限额、只增不减、失效即忽略) + §2.2 增 app.ini / 服务端配置一行, hook 头注释记同一格式; SC-26 增两行 doc-sync 判据。

### Minor

**m1** — id `47c3900d` / minor / decision / architecture
scope: `proposal.md Impact.issue 收尾口径 / 待 owner 复议 3`
summary: 复议 3 的默认 (理解 A, `:332`) 会在 owner 未裁前就对 10CG/aria-plugin#203 与 10CG/Aria#221 发「代码侧进展」评论; 决策单第 2 项执行注原文是「相关 issue 保持 open、本项之下不评论」, A 是字面冲突的一侧。发评论不可撤回地通知了 owner 与订阅者, 选 B 零成本 (之后随时可补)。建议默认改 B。证据: 决策单第 2 项执行注; `proposal.md:294`、`:332`。

**m2** — id `7d4fec1c` / minor / issue / testing
scope: `proposal.md What.W11 / SC-22 (Read 面)`
summary: W11 的新拦截族只有 Bash 面; Read 工具读 `/proc/<pid>/cmdline` 与 `/proc/<pid>/environ` 基线与目标都放行, 未声明 KNOWN-LIMIT, 与 W8 给 app.ini 补 Read/Edit 面的做法不对称。证据: 副本实跑 Read `/proc/4242/cmdline`、`/proc/4242/environ`、`/proc/self/environ` → 基线 exit 0 (`secret-guard.sh:641` 的路径正则不含 `/proc`); Bash 面 `cat /proc/4242/cmdline` 基线已拦 (22J)。未验证 Read 工具在平台上能否读取大小为 0 的 `/proc` 文件。建议: 加一行 KNOWN-LIMIT (22am) 并并入建议开单第 5 条「Bash 面与 Read/Edit 面名单不对齐」。

**m3** — id `b976c610` / minor / issue / implementation
scope: `proposal.md What.W2 熵下限 (路径形判据)` (`:64`)
summary: 路径形判据要求「首段为小写目录名」, `/Users/…`、`~/Library/…` 这类 macOS 路径与 `prod/app/db-credentials-v2` 这类相对名仍告警。证据: oracle (字面设计) 实跑 `SECRET_FILE = /Users/alice/.config/app/token.json`、`TOKEN_PATH=~/Library/Keychains/login.keychain-db`、`GITHUB_TOKEN_FILE=/Users/alice/.gh_token`、`SECRET_ID=prod/app/db-credentials-v2` 均 ALERT, 对照 `SECRET_FILE = /run/secrets/Db2Password` silent (9o 只覆盖小写路径)。hook 头注释与 README 明写支持 macOS。建议: 路径形改为「以 `/` `~/` `./` `../` 开头且含第二个 `/`」, 去掉小写要求, 补一行 SC-9。

**m4** — id `d70f228c` / minor / issue / testing
scope: `proposal.md SC-23 / SC-24 (issue 点名形态)`
summary: 误报回归集没有 10CG/Aria#221 点名的原形: SC-23 缺那条多行 `nomad alloc exec -task server <alloc> python -c "…os.environ.get('DATABASE_URL')…"` (我实跑: 基线 exit 2, W12 字面 exit 0, 所以 W12 能修好, 只是没钉); SC-24 钉了 `map(.name)` 却没钉 issue 点名的 `map(.key)`。证据: `Aria-221.md` 评论 25898 的命令原文与 jq 形态清单; `baseline_probe.py:649-672`。建议: 各补一行。

**m5** — id `b5bbd88c` / minor / issue / testing
scope: `proposal.md SC-18 / SC-19 (Read/Edit 面 nonce 与大小写)`
summary: W8 (`:122`「Edit 被拦, 走 nonce」) 与 W9 (`:130`「同一 SECRET_GUARD_ACK_PATH nonce 逃生口」) 都承诺新拦截可经 nonce 放行, 没有一行验证; BLOCKED 文案会教 AI 用这条路, 若扩展分支自己 `exit 2` 就是死路。W9 条目还没测混合大小写: Read 面对 `lower_path` 匹配 (`secret-guard.sh:640`), 条目若不同步小写就永远不命中。证据: SC-19 / SC-20 的条目全小写; 探针无 nonce 行。建议: 各补一行 (extension Read + 有效 nonce → exit 0; 含大写条目的 Read 命中)。

**m6** — id `6b5eb047` / minor / risk / testing
scope: `proposal.md SC-32 / What.W10 (bash 3.2)`
summary: 「bash 3.2 可跑」只有 SC-32 的 5 种构造 grep 作证 (`declare -A`、`mapfile`、`readarray`、`${x,,}`、`${x^^}`), 既有套件也只有 readarray / mapfile 的静态断言 (`secret-guard.test.sh:752-753`), 没有任何 bash 3.2 真跑; `[[ -v ]]`、`declare -n`、`|&`、`&>>`、`;&`、`${x@Q}` 一类能通过 SC-32 却在 macOS 系统 bash 上语法失败, 而 hook 在 bash 语法错误时 exit 2 会阻断全部 Bash 调用 (#154 同型死锁)。另 W10 (`:142`) 要求替换串加引号 (为 bash 5.2 的 patsub_replacement), 这个写法在 bash 低于 4.3 时 `"${x//p/"$r"}"` 会把引号原样带进结果, 我本机只有 bash 5.2.15, 未验证。建议: 扩 SC-32 的构造清单; B.2 在 macOS 或 bash 3.2 容器上手工冒烟并记入 handoff。

**m7** — id `a0cb1abc` / minor / issue / documentation
scope: `proposal.md SC-26 / SC-28 (doc-sync 判据强度)`
summary: doc-sync 行判别力弱: 26a 只要求某行同时含 `命令行参数` `env` `--config` `stdin` 四个词元 (`env` 会被 `environment` 命中), 词元堆砌即过; 28f 只验旧 Read 形状行消失, 删掉那行不写真实形状也过; 28a-28i 都是「删句即过」。证据: `baseline_probe.py:815-820`、`:873-885`。建议: 26a 绑定一句完整成句 (或唯一标记); 28f 增「新形状含 `file.content`」。

**m8** — id `9519ae32` / minor / issue / documentation
scope: `proposal.md Impact.覆盖关系 (10CG/aria-plugin#154 全覆盖)`
summary: 覆盖关系写「10CG/aria-plugin#154 全覆盖」, 而 issue 评论 19339 交付物 1 的正则是 `"[^"]{8,}"`, W2 对 `token` / `sha1` 统一 16 并用 SC-10 10c 钉住「token 12 位静默」。偏离在 W2 设计取舍里有说明, 但覆盖关系行没点明。建议在该行加一句「`token` / `sha1` 值长门槛 16, 8-15 位不覆盖 (KNOWN-LIMIT 10c)」。

### SC 三态核验总表 (非 finding)

「基线」= 我的副本实跑; 「目标」= 可达性证据; 「坏实现」= 已实证或设计上会红的行。

| SC | 基线 | 目标 (可达性证据) | 坏实现如何红 | 评 |
|---|---|---|---|---|
| 1 | 0/2 | 字面 oracle 2/2 | 不加 file.content → 1a 1b 13a (实证) | 好 |
| 2 | 4/4 | 4/4 | 破坏旧分支 → 2a-2d (设计) | 好 |
| 3 | 2/2 | 2/2 | 扩面到 Edit / 字符串 → 3a 3b (实证) | 好 |
| 4 | 0/13 | 13/13 | 键子串 → 4i 4j 4k 9j; 缺 registration_token → 4e; 缺 Pascal → 4i 4k (实证) | 好 |
| 5 | 0/11 | 11/11 | kv 值类漏 `+/=` → 5a 5g 5h 5k; kv 在 env-line 前 → 7a 7f (实证) | 好 |
| 6 | 0/7 | 7/7 | Client-Id 也计 → 6d 6g; 小写键进 kv → 6c 6d 6f 6g (实证) | 好 |
| 7 | 7/7 | 7/7 | 新 tag 排序抢 span → 7a 7d 7e 7f (实证) | 好 |
| 8 | 0/1 (m=2) | 1/1 | 无 `<` 规则 → 8a (实证) | 好 |
| 9 | 21/21 | 21/21 | 无熵下限 → 9o 9p 9q; 标点计类 → 9p; 无路径判据 → 9o (实证) | 好, 缺 M5 / m3 的形态 |
| 10 | 6/6 | 6/6 | 阈值 8 → 10c; 小写键 → 10d; CLI 空格 → 10e (实证) | 好 |
| 11 | 14/21 | 21/21 | 「含」→ 11s; 缺各前缀 → 11d 11e 11f 11l 11n 11p 11q 11r (实证) | 存活变体见 M3, 过宽见 M2 |
| 12 | 3/6 | oracle 5/6 (12c 需真实 PATH) | 整 span 哈希 → 12a; 短值哈希 → 12b; 值头 8 字符 → 12a 12b 12d-f (实证) | 只验单值, 见 M4 |
| 13 | 3/6 | 6/6 (oracle) | 不做 W5 → 13a-13c | 好 |
| 14 | 0/2 (33 行 / 12 条) | 需实现 | 晚隔离 HOME → 红 (设计) | 好 |
| 15 | 5/6 (matches=33) | 15b-15f 在字面目标设计下静默 (oracle 实证); 15a 需 W7 | 无熵下限 → 15b 15f 红 (实证) | 好; 薄弱点 2 由此部分消解 |
| 16 | 0/11 | 原型 A 11/11 | 无 tight → 16f (+17a) (实证) | 好 |
| 17 | 10/10 | 原型 A 10/10 | 缺左边界 → 17a (实证) | 好 |
| 18 | 2/6 | 原型 A 6/6 | 设计 | 好, 缺 nonce 行 (m5) |
| 19 | 6/14 | 原型 B 12/14 (缺 19g cwd 回落与 19i 变量, 原型未做) | 设计 | 好 |
| 20 | 12/12 | 原型 B 在 20g 20i 20k 红 —— 原型是「截断半采用」, 正是该 SC 要抓的坏实现 | 判别力已实证 | 好 |
| 21 | 13/21 | 原型 AC 21/21 | 「赋值即拦」→ 21i-21m (设计) | 好 |
| 22 | 29/64 | 原型 ALL2 / D2 转绿 30/35; 22n 22z 22A 22B 22C 原型缺 | 太宽 / 太窄 / 无命令位锚 → 放行行 (设计) | 好; 外壳族未实证 (薄弱点 4) |
| 23 | 13/19 | 字面 W12 全 yes (含 23f) | 保守边界 → 23f 红, 即把更安全的实现判坏 | 见 C1 / M1 |
| 24 | 11/16 | 原型 F2 在 24h 红 (放宽词表, 正是 Spec 描述的坏实现) | 判别力已实证 | 好 |
| 25 | 3/7 | 原型改了文案 → 25a 25b 红 | 判别力已实证 | 好 |
| 26 | 0/2 | 需文档 | 词元堆砌可过 | 弱 (m7) |
| 27 | 2/3 | 需实现 | 忘回填 → 红 | 好 |
| 28 | 0/11 | 需实现 | 删句即过 | 弱 (m7) |
| 29 | 7/7 | 套上 W12 补丁后 593/593 仍全绿 | 只防外溢 | 回退不可见 (C1) |
| 30 | 无探针 | 我在带 af87cae 历史的克隆上复现 593/593 rc=0, SC-8 最坏档 39.8ms / 天花板 100ms | — | 可接受 |
| 31 | 5/5 | 原型 31b (63 对 61) 31c (3 个纯变量行) 红 | 判别力已实证 | 好 |
| 32 | 2/2 | — | 仅 5 种构造 | proxy (m6) |

独立旁证: 研究原型 (设计与 Spec 不同) 上跑全探针, 非 baseline-failing 行共 11 条转红 (3a 3b 10c 10d 23r 24h 25a 25b 29b 31b 31c), 每条都对应原型与 Spec 的一处真实差异 —— 说明 reverse-guard / known-limit 行不是恒绿。

## 对执笔人自报薄弱点与请裁项的表态

执笔自报薄弱点 (逐条):
1. SC-30 没有探针基线 — 可接受。我在带 `af87cae` 历史的克隆上复现 593/593 (rc=0, 2m18s, SC-8 最坏档 39.8ms 对 100ms); B.1 记录时请带上 load 与日期。
2. 目标态文本自扫描要到 B.2 才能验 — 可接受, 风险已降: 字面目标设计的 oracle 下 15b-15f 全静默 (proposal.md、探针、两个 hook 源码、guard 测试文件); 15a 只依赖 W7。
3. W2 最终设计没有在语料上普查 — 不可接受, 见 M5 (我做了普查: 14 处 / 9 个文件全为假阳)。
4. W11 外壳包裹形态没有原型 — 可接受为风险, 不作 finding: 研究原型 D2 / ALL2 对 35 条 W11 红行转绿 30 条, 缺的正是 22n 22z 22A 22B 22C; 预算 149 行的原型含 3 个 SC-31c 禁止的纯变量行, 改成内联后 ≤150 的余量只剩约 1 行。建议 A.2 把外壳族拆成独立任务, 预留预算调整的 Spec 变更口。
5. W9 项目根语义 — 可接受。原型 B 的 25 用例加我跑的 SC-19 / SC-20: 除原型与 Spec 有意不同的 5 行外全绿, 且「截断半采用」被 SC-20 抓住, 判别力已实证。Windows Git Bash (issue #203 的报告环境) 下 `CLAUDE_PROJECT_DIR` 的路径形态无法在本机验证。
6. SC 钉得很紧 — 可接受。字面 oracle 满足全部 L3 行, 说明紧钉没有造成无解; 唯一过紧且方向有害的行是 23f / 23b (C1 / M1)。
7. 用例规模 326 行 — 可接受。我已逐 SC 对账计数 (全部一致), 探针确定性 (两次输出哈希相同), 耗时约 2 分钟。
8. rule6_note 块 B 归类 — 可接受。描述性事实陈述, 落决策表第 1 行有据; 「hook 不是 Skill, 按 n/a 更准」是另一种读法, 但第 1 行更保守; 「AB 对 hook 零覆盖 = 测量剧场」与 SOT §3 一致; 若 owner 判处方性, 三件套已写全。
9. Level — 可接受。owner 已裁; 风险点是一次发版同时动 PreToolUse 热路径的五个面 (W8 W9 W10 W11 W12), 与 07-11 先例同形, post_planning 照跑即可。
10. `linked_issue_overlap == []` 取自派单 — 可接受 (主控已实测)。

待 owner 复议 (逐条):
1. L3 是否升级脱敏 — 可接受默认 A。`updatedToolOutput` 未端到端验证; 注意 `secret-scan.sh:15-23` 「architectural limit」等表述在此期间继续留在本 Spec 要改的头注释块里, 与 Why 段的平台事实互相矛盾, 属已申报的延后订正。
2. 拒绝文案 — 可接受默认 A (零改动, SC-25 有锚点)。
3. #203 / #221 收尾 — 不可接受默认 A, 见 m1。
4. Level — 可接受 (owner 已裁)。
5. `ps aux | grep` 被拦 — 可接受默认按 W11; 我 grep 了 aria、standards 与已装的 aether / superpowers 插件缓存, 没有任何 skill 指示 AI 运行这些命令 (aether 的两处只是「别把凭据放 argv, 会进 ps aux」的警示)。
6. 版本定级 — 可接受 MINOR。
7. 建议开单清单 16 条 — 可接受。我在基线复核了第 2 条 (`grep -E 'A|B' ~/.bashrc` exit 0)、第 3 条 (多行命令里另一行的 `| wc -l` 使整段放行, exit 0)、第 4 条 (`chmod 600 ~/.ssh/id_rsa` exit 2)、第 11 条 (两次 ack 后日志 380 字节 0 个换行)、第 15 条 (census rc=1, 诊断同文) 均属实。建议新增两条: Read 面 `/proc` 不对齐 (m2); 备份副本 `app.ini.bak` 与 `cp` 后再读 (17j 有意放行 `cp`) 不在 W8 覆盖内。
8. rule6_note 分块 — 可接受 (同薄弱点 8)。
9. W2 取舍 — 可接受名表封闭、统一 16、至少两类; 但熵下限的路径形判据有 macOS 缺口 (m3), 且无误报验收 (M5)。
10. W3 取舍 — 不可接受整类前缀放行 (M2) 与缺负向守卫 (M3); 「值前缀判定」「不延伸 env-line」本身可接受。
11. W4 取舍 — 「追加字段、16 字符门槛」可接受; fp 取值规则欠定且无验收 (M4)。
12. W7 — 可接受 (源头拼装, 无路径豁免)。
13. W8 只做 app.ini 族 — 可接受。
14. W9 — 可接受设计 (纯文本、字面子串、整体忽略); 缺文档 (M6) 与 nonce / 大小写行 (m5)。
15. W11 — 可接受拒绝处置与 tight credit; 外壳族与预算见薄弱点 4; Read 面见 m2。
16. W12 — 不可接受 (C1 / M1)。
17. 探针在不带 git 的副本上跑 — 可接受, 但要求 B.1 把 SC-30 的真实数写进 handoff。

## 风险 / 疑问 (不计入 finding)

1. bash 3.2: W10 要求的「替换串加引号」在低版本的语义, 以及 macOS 系统 bash 的真实行为, 本机无法验证 (只有 bash 5.2.15); macOS 上 hook 语法错误的后果是全部 Bash 调用被阻断。
2. Windows Git Bash: `CLAUDE_PROJECT_DIR` 可能是 `C:\…` 形态, 条目是否要写 `/c/…`, 大小写不敏感文件系统对字面子串的影响, 都没有行。
3. SC-31a 的 ≤150 行预算余量很小 (见薄弱点 4); 纯变量行被 SC-31c 禁止, 研究原型的写法不能直接搬。
4. L3 性能: 基线 hook 对 120-280KB 输入只需 0.19-0.30 秒 (含 2500 处命中), ≤2.5s 预算宽裕, 但 W14 的该预算没有 SC (只有「B.2 实测记录」); 分类循环须无 fork, 否则 200 个 span x 7 个 tag 会逼近 hooks.json 的 5s 超时 (超时 = 静默漏检)。
5. W8 只认名字: 备份副本 (`app.ini.bak`)、`cp` 到别处再读都在覆盖外; 这是黑名单的固有上限, 但「覆盖」措辞应克制。
6. 既有的「credit 按整段计」缺陷 (多行命令里另一行的 `| wc -l`) 让新增的 app.ini / 进程表 / 扩展族同样可被绕过 (基线实跑 exit 0), 已在建议开单第 3 条, 但 Spec 对新族的「已拦」表述应带这条限定。
7. 回滚 / 止损: hook 对内部错误 fail-closed, 上线后若出现全量阻断 (#154 先例), Spec 只有 post-ship 复验腿, 没有「何时回退插件版本、谁操作」的口径; 建议一句话写进 Tasks 1.10 / 1.11。
8. Rule #7: Spec 没有独立的 Rule #7 声明 (值运行时生成、夹具拼装、证据只写元数据散见于 Why / W6 / 探针头); 四份同型先例里提及次数为 4 / 1 / 2 / 0, 不构成缺陷, 建议补一句。
9. 主控已装的真实 secret-guard 在我两条仅含 `os.environ` 或 `/run/secrets/` 字样的 heredoc 命令上触发拦截 (已知的「prose 位置」误拦), 说明 Spec 承认的残余误报是日常可遇的。
10. SC-8 时序闸对负载敏感 (load 7-11 时最坏档仍 39.8ms); W9 / W10 / W11 会吃掉这 2.5 倍余量, B.2 应在同等负载下复测。

## Verdict

verdict: FAIL
counts: 1C/6M/8m
Vote: REVISE

## 是否足以进入 A.2

不足以 —— C1 (W12 使 python 整环境转储由拦变放, 且现有 593 用例与 SC-23 都看不见) 必须先改设计与 SC-23 / 23b / 23f, M2 (W3 对既有 tag 的前缀放行造成检出回退) 与 M3 / M4 / M5 (验收对坏实现与误报面不设防) 也应在 R2 前补齐; 其余 L1 / L3 的 SC 我实跑证实可证伪且目标可达。

# WP-A Phase A 研究笔记 — L3 `aria/hooks/secret-scan.sh` (标签 secret-scan)

> 基线: aria-plugin v1.74.1 @ 268da8f; `secret-scan.sh` 377 行, sha256 前缀 `c5f53f7a164fa72e`, 与 `~/.claude/plugins/cache/10CG-aria-plugin/aria/1.74.1/hooks/secret-scan.sh` 逐字节一致 (即本会话 live 跑的就是它)。
> 环境: Linux 6.17 / bash 5.2.15 / jq 1.6 / GNU grep 3.8 (子进程 `bash hook.sh` 用 `/usr/bin/grep`; 交互 shell 里的 `grep` 是 ugrep 包装函数, 未导出, 不影响) / sed 4.9 / perl 5.36 / Python 3.11.2 / Claude Code 2.1.285。
> 纪律: 真仓只读; 全部实验在 `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/secret-scan/` (下称 `$EXP`); 所有「像凭据的值」运行时由 `secrets` 生成并经 stdin 喂 hook, 报告只含元数据; 未读取/打印任何真实凭据。
> 证据标记: 「实测」= 我跑出来的; 「实读」= 我读到的源码/文档; 「推测」= 推断。

## 0. 结论速览

1. **基线矩阵复现了 owner 决策单的全部断言**: `{"token":…}` / `{"sha1":…}` / `JWT_SECRET = <b64>` 零输出, 阳性对照 `client_secret` 与 `JWT_SECRET=` 被检出。92 个「bash_real + 提取路径」行里 **GAP 36 / FP 5 / OK 44 / info 7** (实测, 见 §3)。
2. **比 #154/#203 更深的一个缺口 (本次最重要的新发现)**: hook 的内容提取 (`secret-scan.sh:135-142`) 只认 `.tool_response.output // .content // .stdout`。CC 2.1.285 里 **Read 的真实形状是 `{type:"text", file:{content,…}}`** (实测 transcript 172/175 + 二进制), 顶层没有 `content` ⇒ **生产里 Read 永远不被扫描**。活体 A/B (本会话, 同一份含 AWS 文档公开示例 key 的文件): `Bash cat` 触发告警, `Read` 不触发; `Edit` 同样不触发。真实日志里 35 条 Read 事件全是测试套件指纹。现有测试用合成形状 `{content}` (`secret-scan.test.sh:28-32`) 所以一直绿 —— 典型「测试绿 ≠ 生产被调用」。
3. **前提可能已过期**: DEC-20260703-001 与 `secret-scan.sh:15-24` 写的「PostToolUse 架构性不可能 redact, 非 version-dependent」**与 CC ≥ v2.1.220 不符**: 官方文档 (WebFetch) + 本机 2.1.285 二进制里的 hook schema 都有 `hookSpecificOutput.updatedToolOutput` (「Replaces the tool output before it is sent to the model」, 支持 Read/Grep/Bash/PowerShell, 对 Write/Edit 忽略)。L3 理论上可从「检测+告警 (视为已泄露)」升级为「检测+脱敏」。未做端到端活体验证 (见 open_questions)。
4. 现状无 FP 白名单 (全文无 FAKE/PLACEHOLDER/REDACTED 判断): 基线对既有键 `password/client_secret/api_key` 的 `FAKE_*` / `PLACEHOLDER_*` / `NOT-REAL-*` / `[REDACTED]` / `********` 值 **5/5 误报**; 且哨兵回灌会**重复计数** (`{"api_key":<anthropic key>}` → `matches=2`, 实际 1 个凭据)。
5. **日志不含值也不含哈希** (`secret-scan.sh:358-361`: ts/USER/PWD/SCAN-DETECT/tool/matches/breakdown/size)。#154 评论里「若现行为已如此则只加断言」前半句不成立: `hash8` 是**新功能**, 不是钉住既有行为。原型实测: 全部 170 行结果里日志与 hook 输出均**无明文、无 8 位片段**。
6. **可行的加法式原型** (不改既有 tag 语义, 在 `$EXP/cand-aria/`): 既有 49 用例 49/49 通过; 92 行矩阵 OK 84 / GAP 1 (仅首字母大写键 `Token`) / FP 0; 505 文件语料普查告警文件 5→9 (新增全是测试夹具 / 文档示例; 259 个散文类文件里 1 个)。
7. **新增通用模式必须带 FP 分类器 + 熵下限**, 否则新 `kv-secret-assign` 在本仓立刻误报 6 处 (`SECRET_GUARD_ACK_PATH=/路径`、`*_SECRET_ENV=<环境变量名>`、kebab 短语…); 下限代价是「单字符类值」(全小写/全数字随机串) 漏报。
8. **兼容性硬约束**: 同目录 `secret-guard.sh:118-135 / :538-552` 明文记载 macOS `/bin/bash` 3.2 + zsh 曾造成死锁 ⇒ 新代码不得用 `declare -A` / `mapfile` / `readarray` (我第一版原型两者都用了, 已重写并加静态检查)。
9. 性能 (Linux 实测): 干净输入 0.25-0.4 s, 900KB 无命中 0.34 s, 稠密命中 442KB 1.3-1.9 s, 均远低于 `hooks.json:60` 的 5 s; 但 PEM 预扫 (perl `.*?`+`\1`, `:260-273`) 对「大量 BEGIN 头无 END」**超线性** (125KB→7.4 s, 250KB→21.6 s, 870KB→>120 s), 且被 SIGKILL 时 `mktemp` 缓冲文件 (0600, 含全文) 会遗留 (实测)。真实输出最大 Bash 103KB / Read 93KB, 远低于 1MB 上限, 属病态输入。
10. 本会话 live L3 共触发 6 次 (1 次 Write + 5 次 Bash), **全是 FP**: 我自造的占位符/掩码文本 (Write matrix 脚本→`DETECTED 10`, 打印矩阵表→`7`)、公开 fixture、AWS 文档公开示例 key; 无真实凭据、无需轮换。它本身就是「讨论凭据格式的文本会命中」的活体证据。

---

## 1. 架构地图

### 1.1 注册与触发 (`aria/hooks/hooks.json`)

| 项 | 值 | 行 |
|---|---|---|
| 事件 / matcher | PostToolUse × `Bash\|Read\|Edit\|Write\|MultiEdit` | :53-55 |
| 命令 | `bash ${CLAUDE_PLUGIN_ROOT}/hooks/secret-scan.sh` (显式 `bash`, 不受 `$SHELL`/zsh 影响) | :59 |
| 超时 | `timeout: 5` (秒) | :60 |
| 同事件第二条 | Bash-only `submodule-gate-telemetry.sh`, timeout 30 | :64-71 |
| 未覆盖的出口 | `Grep` / `PowerShell` / `WebFetch` / MCP / `Agent` (文档称 updatedToolOutput 支持 Read/Grep/Bash/PowerShell); 本仓 37 个会话 transcript 里 Grep 调用 0 次 | :55 |

### 1.2 信封解析 (`secret-scan.sh`)

- `:96` `set -uo pipefail`; `:98` `INPUT_SIZE_CAP=1MB`。
- `:107-110` 缺 jq → **fail-open** (exit 0 + stderr 警告); `:112-113` 空输入 exit 0。
- `:118-122` 大小上限按**整个输入 JSON 的字节数** (`wc -c`, 修过 codepoint 计数的坑); 超限 → exit 0, **仅 stderr NOTE, 不写日志** (静默跳过)。
- `:125-127` `tool_type` 门 (`.tool_name|type == "string"`, 已 CR 剥离以抗 Windows jq CRLF, #132 sibling); `:129-130` `tool` (同样剥 CR)。
- `:135-142` 内容提取 (`# crlf-ok` 标注: 这是被扫描的数据体, 不得剥 CR):

```
.tool_response.output // .tool_response.content // .tool_response.stdout //
.tool_result.content // .tool_result.output // ""
```
  `//` 取**第一个非 null**, 不拼接。`:144` 空内容 exit 0。

**各工具真实 `tool_response` 形状 vs hook 读取 (核心表)**:

| 工具 | hook 读取 | CC 2.1.285 真实形状 | 生产是否扫描 | 证据 |
|---|---|---|---|---|
| Bash | `output`→`content`→`stdout` | `{stdout, stderr, interrupted, isImage, noOutputExpected, …}`, **无 `output`**。命令自身 stderr 已并入 stdout; `stderr` 字段只装 harness 提示 (「Shell cwd was reset…」: 163/163 非空样本首 14 字符同形) | 是 (stdout) | transcript 5,231 条; 官方插件 `security-guidance/hooks/security_reminder_hook.py:1028-1036, :1515-1524` 读 `stdout`+`stderr`; 二进制 Bash 投影 `.pick({stdout,stderr,interrupted,isImage,timedOutAfterMs,noOutputExpected})`; **live**: stderr-only 输出 (公开示例 key) 被告警 |
| Read | `content` (顶层) | `{type:"text", file:{filePath, content, numLines, startLine, totalLines[, truncatedByTokenCap]}}`; `file.content` 是原文 (无行号前缀: 172 条样本 0 条有) | **否** | transcript 172/175; **live A/B**: 同内容 Bash cat 告警、Read 静默; 真实日志 35 条 Read 事件全为测试指纹 |
| Write | `content` | `{type:"create"|…, filePath, content, structuredPatch, originalFile, userModified}` | 是 | live 告警 (matrix 脚本); 真实日志 62 条 Write 事件 |
| Edit | (无可读字段) | `{filePath, oldString, newString, originalFile, replaceAll, structuredPatch[], userModified}` | **否** | live Edit 探针静默; 真实日志 Edit 事件 0 条 (2026-05-17→09-30)。注: Edit 结果给模型的只是一句成功提示, 不回显内容 |
| MultiEdit | — | transcript 0 样本, **形状未知** | 未知 | — |
| 字符串形 `tool_response` | `.output` 对 string 报错→被 `2>/dev/null` 吞→内容空→exit 0 | transcript 里 Bash 有 86 条是纯字符串 (错误文案) | 否 | 实测 |

> 同一份 `toolUseResult` 与 hook 入参 `tool_response` 同源是**推测**, 但有三重旁证: 官方插件读的字段 / 二进制里 hook-facing 投影 / 三个 live 探针 (Bash 与 Write 告警, Read 与 Edit 静默) 与该假设一致。

### 1.3 PATTERNS (`:152-231`, 共 31 条 + PEM 预扫 = 32 个 tag)

顺序 = 特异性优先 (jwt 最先; 通用键形最后)。

| # | tag | 行 | 覆盖 | 形状 (ERE 摘要) |
|---|---|---|---|---|
| 1 | jwt | 159 | 任意 JWT (含 Forgejo INTERNAL_TOKEN) | `eyJ…{10,}.eyJ…{10,}.…{10,}` |
| 2-6 | silknode / anthropic / openrouter / openai / openai-legacy | 166-174 | `sk-silk-`32+ / `sk-ant-(api03\|admin03\|sid)-`32+ / `sk-or-v1-`32+ / `sk-(proj\|svcacct\|admin)-`32+ / `\bsk-`48+ | provider 前缀 |
| 7-11 | stripe live/test/publishable/webhook/restricted | 177-181 | `sk_live_` `sk_test_` `pk_(live\|test)_` `whsec_` `rk_(live\|test)_` + 20+ | provider 前缀 |
| 12-16 | github-pat/oauth/user/fine-grained, gitlab-pat | 184-188 | `gh[ps]_`36 / `gho_`36 / `ghu_`36 / `github_pat_`82 / `glpat-`20+ | provider 前缀 |
| 17-19 | aws-access-key-id / aws-session-token / aliyun-access-key-id | 191-195 | `AKIA`16 / `FwoGZXIvYXdzE`40+ / `LTAI`16+ | provider 前缀 |
| 20 | gcp-private-key-id | 198 | `"private_key_id": "<40 hex>"` | 键+值 |
| 21-22 | discord-webhook / slack-webhook | 201 / 204 | webhook URL | URL |
| 23-25 | postgres / redis / mongodb URL | 207-209 | `scheme://user:pass@host` (pass≥4) | URL 内嵌凭据 |
| 26 | basic-auth-url | 212 | `https?://user:pass@host` (pass≥6) | URL 内嵌凭据 |
| 27 | bearer-token | 215 | `Authorization: Bearer` + ≥20 | 头部 |
| 28 | x-api-key-header | 218 | `X-API-Key:` + ≥16 | 头部 |
| 29 | **env-line-secret-keyword** | 224 | `^[A-Z0-9_]*(SECRET\|PASSWORD\|PASSWD\|TOKEN\|API_KEY\|PRIVATE_KEY\|WEBHOOK\|ENCRYPTION_KEY\|ACCESS_KEY)[A-Z0-9_]*=` + ≥8 个 `[A-Za-z0-9+/=._\\-]` | **行首、`=` 两侧零空白、无引号、无 `export`、仅大写** |
| 30 | **json-secret-field** | 227 | `"(password\|passwd\|secret\|api_key\|access_token\|refresh_token\|private_key\|client_secret\|webhook_secret\|encryption_key)"` `:` `"[^"]{8,}"` | **仅这 10 个键 (无 token / sha1), 键名两侧必须是引号, 值任意 ≥8 字符** |
| 31 | bcrypt-hash | 230 | `$2[abxy]$NN$`+53 | hash |
| — | PEM 多行预扫 | 250-281 | perl `-0` `/s`: `-----BEGIN [A-Z ]+(PRIVATE KEY(?: BLOCK)?)-----.*?-----END [A-Z ]+\1-----` (RSA/EC/OPENSSH/PGP/加密 PEM); 无 perl 降级为仅数 BEGIN 头 | 多行 |

头注释陈旧: `:34` 写「~15 secret-shape patterns」(实际 31+PEM), `:52` 写「argon2」(实际无 argon2 模式), `:72-80` Hook contract 只列 `output`/`content` (与真实形状不符)。

### 1.4 匹配引擎

- 计数: 每个 tag `grep -oE -- "$pattern" tmpfile | wc -l` (`:296`, 数**匹配数**而非行数); 消耗: `sed -i -E "s\x01pattern\x01<secret-scan-counted:TAG>\x01g"` (`:300`, 用 `\x01` 做分隔符避开模式里的 `|`); 再 grep 复核残留 (`:312`), 残留则报 `tag=N+M-uncounted` (`:314-325`)。
- PEM: perl (`:262-273`), 缺 perl 降级 grep/sed 仅数 BEGIN 头 (`:274-281`)。
- `tmpfile` 是**全文副本** (`mktemp`, `:239-241`, `trap rm EXIT`), 永不输出。
- **哨兵回灌**: 前序模式把命中段替换成 `<secret-scan-counted:TAG>`, 这个哨兵长度 >8 且不含 `"`, 会被后序的 `"key":"[^"]{8,}"` 当成值再匹配一次 (实测 JX8: `anthropic-api-key=1 json-secret-field=1`, matches=2)。任何新增「值 ≥N 个任意字符」的通用模式都会继承这个问题。

### 1.5 现有 FP 白名单

**无** (实读: 全文无 FAKE/PLACEHOLDER/allowlist 判断, `grep -i` 仅命中 `:338` 的「NOT redacted」文案)。仅有结构性误报抑制: 最小长度/前缀锚定 (如 `:170-174` legacy key ≥48 + `\b`) 与测试里的 pass-through 用例 (`secret-scan.test.sh:127-137`)。`sk-silk-FAKEFIXTURE…` / `ghp_FAKEFIXTURE…` 两个夹具 (`:102`, `:107`) 的 FAKE 在**值中间**, 不是值前缀 —— 所以 #154 的「FAKE 前缀值跳过」若写成「span 含 FAKE 即跳」会把这两个既有测试翻红; 必须是「值以…开头」且只作用于通用键形 tag。

### 1.6 告警通道与格式

- 命中: `exit 0` (`:377`, 永不 block) + stdout JSON (`:369-375`): `hookSpecificOutput{hookEventName:"PostToolUse", additionalContext}` + `systemMessage`。
  - `additionalContext` (`:367`, 进模型上下文): 「DETECTED N secret-shape match(es) … treat as already-leaked; do NOT repeat the value(s); recommend rotating …; (This hook detects+warns only; it cannot redact …)」—— **只有计数, 没有 tag、没有文件路径/命令** (live 收到的正是这段, 我得离线复现才知道是哪些 tag)。「轮换」在第三项而非 #154 原稿想要的最前。
  - `systemMessage` (`:368`, 给 operator): 含 breakdown (`(tag=n …)`)。
  - stderr 摘要 (`:337-353`): 按官方文档 (WebFetch, 摘要模型, 中等置信) **exit 0 时 stderr 只进 debug log, 不给用户也不给模型** ⇒ 「stderr 摘要」不是有效通道; 测试里 CRLF 用例拿 stderr 的 `DETECTED` 当信号仅在测试里有意义。
- 告警数来自 span 计数, 不是凭据数 (哨兵回灌会多计; 老 tag 有 `+M-uncounted` 分支)。

### 1.7 日志

`${HOME}/.claude/logs/secret-scan.log` (`:355-361`), `mkdir -p` + 追加; TSV 8 字段: `ts \t USER \t PWD \t SCAN-DETECT \t tool= \t matches= \t breakdown= \t size=`。**无值、无哈希**; 无轮换/大小上限; 仓内无任何读取方 (grep `secret-scan.log|SCAN-DETECT` 在 aria/standards/docs/openspec 0 命中) ⇒ 加字段无兼容负担。
真实日志 (实测): ≈1.5k 行, 2026-05-17→09-30; Bash 1416 / Write 62 / Read 35 / **Edit 0**; 按「完整套件指纹」保守估计至少 9 次完整套件运行 (≥297 行, ≥20%) 把测试夹具写进了**真实**审计日志 (套件不隔离 HOME), 另有 ≥22 次含首个 PEM 用例指纹。

### 1.8 大输出 / 超时 / 性能

- ≥1MB 输入静默跳过 (`:119-122`)。真实 `tool_response` JSON 尺寸 (transcript): Bash p99 33.6KB / max 103KB; Read max 93KB; Write max 198KB; Edit max 38KB; **0 条超 1MB**。
- 超时: 官方文档 (WebFetch): PostToolUse 命令 hook 超时**不阻断**, 输出被丢弃, 仅 debug log, 用户与模型都看不到 ⇒ 超时 = 静默漏检 (而非报错)。
- 实测 (Linux, 串行交错 7 次取中位): 干净 6B 0.28 s / 200KB 日志 0.41 s / 单命中 0.45 s; 原型 0.25 / 0.36 / 0.39 s; 稠密 INI 180KB 基线 0.54 s (根本看不见) vs 原型 1.29 s。单次约 100 个进程派生 (31 模式 × grep/wc/tr + jq×3 + perl)。**Windows Git-Bash 进程创建慢一个数量级 (推测)**, 5 s 余量需在该环境实测 (#203 报告者是 MINGW64); 本次未测。
- PEM 预扫超线性 (实测, 基线): N 个 `BEGIN RSA PRIVATE KEY` 头且无 END: 4000 个 (125KB) 7.4 s, 8000 个 (250KB) 21.6 s, 27000 个 (870KB) >120 s。被 `timeout -s KILL` 杀掉后 `tmp.XXXX` (0600, 255,999 字节 = 输出全文副本) 遗留在 `$TMPDIR` (实测)。属既有、非现实输入, 但「新增模式一律用线性 ERE、不引入 perl/回溯」应写进约束。

### 1.9 DEC-20260703-001 (`.aria/decisions/DEC-20260703-001-secret-scan-honest-downgrade.md`) 与本次的关系

- 内容 (实读): #91 part② —— 官方 hooks-guide 证实 PostToolUse **无** `updatedToolOutput`、「PostToolUse hooks can't undo actions」(line 891), 故 secret-scan 必须从「redact」诚实降级为 **warn-only 检测器**; 选 Q1=b「保住检测价值」; `.jsonl` 事件记录 / block / 自动开 issue 全拆到 **#92**; 预估 Level 2。
- 与 WP-A 的一致面: WP-A 是「补检测面 + 压误报」, 符合 Q1=b; 仍 warn-only、不 block。
- **冲突面 1 (前提过期)**: 当前官方文档与 CC 2.1.285 二进制都支持 `updatedToolOutput` (文档: 「Requires Claude Code v2.1.220 or later」; 本机 transcript 版本跨度 2.1.220-2.1.285, 即本实验室已全部在支持版本上)。DEC 的「非 version-dependent」现在是 version-dependent。WebFetch 未在当前文档里找到「can't undo」原句 (摘要模型, 低置信)。
  - 二进制证据 (实读 `claude` 2.1.285): PostToolUse schema 含 `updatedToolOutput: "Replaces the tool output before it is sent to the model"` 与 `updatedMCPToolOutput: "…MCP tools only. Prefer updatedToolOutput, which works for all tools"`; 应用逻辑对非 MCP 工具用 `tool.outputSchema.safeParse` 校验, 不合形则 `"PostToolUse hook returned updatedToolOutput that does not match <tool>'s output shape; using original output."` 并回退原输出 (报 hook_error_during_execution)。
  - 文档与二进制对多 hook 语义表述不一致: 文档「后一个 hook 看到前一个的改写 (叠加)」; 二进制 schema 描述「hooks run in parallel on the ORIGINAL output … last-write-wins」。本 hook 与 `submodule-gate-telemetry.sh` 同 matcher(Bash) 并行, 若启用改写需实测。
- **冲突面 2 (#92 边界)**: DEC 把「事件 schema / redaction 安全 / 分级 block」划给 #92。`hash8` 字段落在 #92 的「redaction 安全」设计面, 需与 #92 状态对齐 (我无法核实 #92 进展)。
- 需同步更正的「PostToolUse cannot redact」陈述见 §4。

---

## 2. 测试套件 `aria/hooks/tests/secret-scan.test.sh` (293 行)

- **运行**: `bash aria/hooks/tests/secret-scan.test.sh` (aria-plugin 根目录); 依赖 `jq`/`python3`/`lib/crlf-shim.sh`; 需要 `secret-scan.sh` 有执行位 (直接 `"$HOOK"` 调用)。
- **结果 (实测, 副本, HOME 指向 `$EXP/home`)**: **PASS 49 / FAIL 0**, 墙钟 22.6 s (首跑) / 14.3 s (复跑, 机器上另有其他 agent 并发, 有噪声)。
- **用例构成 49 = 28 `expect_detect` + 12 `expect_pass` + 9 专项**:
  - `expect_detect` (`:42-74`) 三重断言: (1) stdout JSON 同时有 `additionalContext` 与 `systemMessage`; (2) `systemMessage` 含期望 tag; (3) stdout 无 `tool_response` 键 (warn-only 结构性缺席)。覆盖 PEM ×5 (单行/多行/PGP/加密/OPENSSH)、JWT、silknode/openai/anthropic、stripe live/webhook、github/gitlab、aws/aliyun、discord/slack、pg/redis/mongo、basic-auth、bearer、x-api-key、env-line、JSON password/api_key、bcrypt、gcp (`:93-123`)。**没有** stripe-test/publishable/restricted、github-oauth/user/fine-grained、aws-session-token、openrouter、openai-legacy 的用例 (11 个 tag 无直接覆盖)。
  - `expect_pass` (`:78-137`): 干净输出/git log/`NODE_ENV=production`/版本串/短 hex/无凭据 URL/`password=hunter2`/空输出。注释说 `hunter2`「too short for env-line-secret-keyword」, 但真实原因是**小写键** (模式要求大写) —— 注释与实际验证对象不符, 将来加小写族时要警惕该用例恰好翻转。
  - 专项 9 个: Read 工具含凭据 (`:145-153`, **用顶层 `{content}` 合成形状**)、多命中计数 ≥2 (`:156-171`)、exit-0-on-match (`:174`)、缺 jq fail-open (`:185-196`)、>1MB 跳过 (`:200-213`, python 造 JSON)、畸形 JSON (`:216-223`)、CRLF 三件 (shim 自检 + pristine/fixed 两态 + CR 内容检测, `:233-277`)。
- **「像凭据的值」怎么构造**: **字面量写在测试文件里**, 不是运行时拼装 (与「哨兵须运行时拼装」的 memory 反着来); 夹具做了 FAKE 化命名 (`:102`, `:107`) 与 AWS 文档公开示例 key (`:109`, `:174`, `:187`)。GitHub push protection 靠 `aria/.github/secret_scanning.yml:18-22` 的 `paths-ignore` 放行 **仅** `hooks/tests/secret-guard.test.sh` 与 `hooks/tests/secret-scan.test.sh`。⇒ 新夹具只能放这两个文件, 或运行时拼装; 放进其他文件 (含 Spec 文档) 可能被 push protection 拦。
- **不隔离 HOME**: 套件不设 `HOME`, 每次运行向真实 `~/.claude/logs/secret-scan.log` 追加约 33 行夹具事件 (§1.7)。
- **与 hook 文本耦合**: CRLF 两态用例用 `sed '/would fail the type gate below/d'` 删 hook 的 `:126` 那一行制造「无修复」副本 (`test:246`)。改 hook 时这行注释文字必须保留, 否则该用例要么失效要么变空转。`tests/lib/crlf-shim.sh:95` 还引用「secret-scan.sh:116」(当前已是 `:126`, 已过期)。
- **副本上的旁注**: 在无 git 元数据的副本上跑 `secret-guard.test.sh` 得 581/582 (1 项头注释计数断言失败 + 若干 SKIP), 属副本环境差异 (无 git/无 zsh), 非本任务范围。其运行输出仅 665 字节摘要, 被基线与原型扫描均不告警。

---

## 3. 基线检测矩阵

### 3.1 方法

- 运行器 `matrix_paste.py` (下方全文; 原始版在 `$EXP/matrix.py`, 已验证二者对 158/170 个 case×shape 的告警态逐一一致): 每个 case×shape 跑 N 次 trial (基线 3-5 / 原型 5-10), **每次新生成值**; 每次 `HOME=<新临时目录>`、`TMPDIR=<临时目录>`、最小化 `PATH`; 值经 `subprocess.run(input=…, capture_output=True)` 喂 `bash secret-scan.sh`; 判据全在 Python 内: 退出码 / `additionalContext` 非空 / 从 `systemMessage` 解析 tag 与 `matches` / 日志是否生成 / 明文(全值)与片段(首末 8 位)是否出现在日志 / 是否出现 `sha256(value)[:8]` / 明文是否出现在 hook 的 stdout+stderr。
- 两种 Bash 形状: `bash_real` = CC 2.1.285 真实 `{stdout,stderr,interrupted,…}`; `bash_test` = 现有套件用的 `{output}`。**全部非提取类 case 两种形状结果逐一相同** (实测, 无差异 id)。Read/Write/Edit 另按真实形状构造, 并保留 Read 的套件合成形状作对照。
- 「期望」列 = 设计意图 (ALERT 应告警 / QUIET 应静默 / `-` 仅记录), 所以基线与期望不符的行直接就是 TDD 的 RED 清单。
- 92 行 = `bash_real` 行 + 提取路径 (S-*) 行。汇总 (实测): **基线 OK 44 / GAP 36 / FP 5 / info 7; 原型 OK 84 / GAP 1 / FP 0 / info 7**。
- 逐行共性 (全部 170 行, 基线与原型均成立): **退出码恒为 0**; **日志仅在告警时生成 (log_written ≡ alert)**; **日志与 hook 输出里无明文、无 8 位片段**; 基线**任何一行**日志里都没有 `hash8` (因为根本没写哈希)。

### 3.2 结果表 (neutral label: 形状用 `key=<shape>` 书写以免本笔记自身触发 L3)

GAP = 期望告警而基线静默; FP = 期望静默而基线告警。「原型」= `$EXP/cand-aria` 的加法式候选 (§5.1)。

| id | 输入 | 期望 | 基线 | 基线 tag | 原型 | 原型 tag |
|---|---|---|---|---|---|---|
| J1 | json:token=<40 hex> (08-20 事故形) | ALERT | GAP | - | OK | json=1 |
| J1b | json:token=<40 alnum> | ALERT | GAP | - | OK | json=1 |
| J2 | json:token=<40 b64url> (冒号后带空格) | ALERT | GAP | - | OK | json=1 |
| J3 | json:sha1=<40 hex> (Forgejo 建 PAT) | ALERT | GAP | - | OK | json=1 |
| J4 | json:client_secret=<32> (阳性对照) | ALERT | OK | json=1 | OK | json=1 |
| J5 | json:password=<16> | ALERT | OK | json=1 | OK | json=1 |
| J6 | json:api_key=<32> | ALERT | OK | json=1 | OK | json=1 |
| J7 | json:secret=<24> | ALERT | OK | json=1 | OK | json=1 |
| J8 | json:access_token=<36> | ALERT | OK | json=1 | OK | json=1 |
| J9 | json:private_key=<40 b64> | ALERT | OK | json=1 | OK | json=1 |
| JX1 | json:registration_token=<40 alnum> | ALERT | GAP | - | OK | json=1 |
| JX2 | json:jwt_secret=<43 b64url> | ALERT | GAP | - | OK | json=1 |
| JX3 | json:Token=<40 hex> (首字母大写键) | ALERT | GAP | - | **GAP** | - |
| JX4 | json:auth_token=<40 alnum> | ALERT | GAP | - | OK | json=1 |
| JX5 | 多行美化 json:token=<40 hex> | ALERT | GAP | - | OK | json=1 |
| JX6 | 完整 Forgejo 建 PAT 响应 (sha1+token_last_eight) | ALERT | GAP | - | OK | json=1 |
| JX7 | json:token=<gh 前缀 token> (重复计数探针) | ALERT | OK | github-pat=1 | OK | github-pat=1 |
| JX8 | json:api_key=<anthropic 前缀 key> (重复计数探针) | ALERT | OK | anthropic-api-key=1 json=1 (**matches=2**) | OK | anthropic-api-key=1 |
| JX9 | json Env 映射 JWT_SECRET=<44 b64> (Nomad/compose 大写键) | ALERT | GAP | - | OK | json-env-key=1 |
| JX10 | json:DB_PASSWORD=<20 alnum> (大写键, 多行) | ALERT | GAP | - | OK | json-env-key=1 |
| K1 | JWT_SECRET = <44 std-b64> (等号两侧空格, #203 泄露原形) | ALERT | GAP | - | OK | kv-assign=1 |
| K1b | JWT_SECRET = <43 b64url> | ALERT | GAP | - | OK | kv-assign=1 |
| K2 | JWT_SECRET=<44 std-b64> (无空格; 决策单称可检出) | ALERT | OK | env-line=1 | OK | env-line=1 |
| K3 | SECRET_KEY = <64 alnum> | ALERT | GAP | - | OK | kv-assign=1 |
| K4 | INTERNAL_TOKEN = <JWT 形> | ALERT | OK | jwt=1 | OK | jwt=1 |
| K5 | PASSWD = <20 alnum> (Forgejo [database]) | ALERT | GAP | - | OK | kv-assign=1 |
| K6 | LFS_JWT_SECRET = <43 b64url> | ALERT | GAP | - | OK | kv-assign=1 |
| K7 | YAML password: <16 alnum> | ALERT | GAP | - | OK | kv-assign-lc=1 |
| K8 | export API_TOKEN=<32 alnum> | ALERT | GAP | - | OK | kv-assign=1 |
| K9 | Authorization: token <40 hex> (Forgejo/Gitea PAT 头) | ALERT | GAP | - | OK | auth-header-token=1 |
| K10 | Authorization: Bearer <32 alnum> (阳性对照) | ALERT | OK | bearer-token=1 | OK | bearer-token=1 |
| K11 | CF-Access-Client-Secret: <64 hex> | ALERT | GAP | - | OK | cf-access-client=1 |
| KX1 | JWT_SECRET="<44 b64>" (dotenv 双引号) | ALERT | GAP | - | OK | kv-assign=1 |
| KX2 | JWT_SECRET='<44 b64>' (dotenv 单引号) | ALERT | GAP | - | OK | kv-assign=1 |
| KX3 | export API_TOKEN="<32 alnum>" | ALERT | GAP | - | OK | kv-assign=1 |
| KX4 | YAML api_key: "<32 alnum>" | ALERT | GAP | - | OK | kv-assign-lc=1 |
| KX5 | DB_PASSWORD=<20 alnum> (env-line 对照) | ALERT | OK | env-line=1 | OK | env-line=1 |
| KX6 | curl -H "Authorization: token <40 hex>" (命令回显) | ALERT | GAP | - | OK | auth-header-token=1 |
| KX7 | CF-Access-Client-Id + -Secret 头对 (curl -H 回显) | ALERT | GAP | - | OK | cf-access-client=1 |
| KX8 | app.ini 片段含 5 个凭据 (基线只因其中 JWT 形的 INTERNAL_TOKEN 告警: matches **1/5**; 原型 **5/5**: jwt=1 kv-assign=4) | ALERT | OK(部分) | jwt=1 | OK | jwt=1 kv-assign=4 |
| KX9 | password=<16 alnum> (小写; 套件认为低熵小写不在范围) | - | info:静默 | - | info:告警 | kv-assign-lc=1 |
| KX10 | Authorization: Basic <b64 user:pass> | - | info:静默 | - | info:告警 | auth-header-token=1 |
| F1 | json:token=FAKE_<24> | QUIET | OK | - | OK | - |
| F1b | json:password=FAKE_<24> (既有键) | QUIET | **FP** | json=1 | OK | - |
| F1c | json:client_secret=PLACEHOLDER_VALUE | QUIET | **FP** | json=1 | OK | - |
| F1d | json:api_key=NOT-REAL-<24> | QUIET | **FP** | json=1 | OK | - |
| F2 | json:token=PLACEHOLDER | QUIET | OK | - | OK | - |
| F3 | json:token=[REDACTED] | QUIET | OK | - | OK | - |
| F3b | json:password=[REDACTED] (既有键) | QUIET | **FP** | json=1 | OK | - |
| F4 | json:sha=<40 hex> (git 提交 sha) | QUIET | OK | - | OK | - |
| F4b | json:commit.id=<40 hex> | QUIET | OK | - | OK | - |
| F5 | git log --oneline (6 行) | QUIET | OK | - | OK | - |
| F5b | git log 完整格式 (3×commit <40 hex>) | QUIET | OK | - | OK | - |
| F5c | git rev-parse HEAD (裸 40 hex) | QUIET | OK | - | OK | - |
| F5d | git ls-remote (2 行) | QUIET | OK | - | OK | - |
| F5e | git submodule status | QUIET | OK | - | OK | - |
| F6 | sha256sum 输出行 | QUIET | OK | - | OK | - |
| F6b | docker images --digests (sha256:<64 hex>) | QUIET | OK | - | OK | - |
| F7 | UUID v4 裸值 | QUIET | OK | - | OK | - |
| F7b | json:uuid=<uuid> | QUIET | OK | - | OK | - |
| F8 | npm lockfile integrity sha512-<b64> | QUIET | OK | - | OK | - |
| F9 | json:password=<空> | QUIET | OK | - | OK | - |
| F10 | json:password=******** (既有键) | QUIET | **FP** | json=1 | OK | - |
| F10b | json:token=******** | QUIET | OK | - | OK | - |
| F11 | json:token_last_eight=<8 hex> (Forgejo 元数据) | QUIET | OK | - | OK | - |
| F12 | Actions yaml `token: ${{ secrets.X }}` | QUIET | OK | - | OK | - |
| F13 | curl 示例 `Authorization: token $VAR` | QUIET | OK | - | OK | - |
| F14 | JWT_SECRET = <尖括号占位> | QUIET | OK | - | OK | - |
| F15 | JWT_SECRET=$(命令替换) | QUIET | OK | - | OK | - |
| F16 | PASSWD = (空) | QUIET | OK | - | OK | - |
| F17 | grep -n JWT_SECRET app.ini (仅键名) | QUIET | OK | - | OK | - |
| F18 | JWT_SECRET = ${模板引用} | QUIET | OK | - | OK | - |
| F19 | YAML password: ******** | QUIET | OK | - | OK | - |
| F20 | 散文: set the token in your config file | QUIET | OK | - | OK | - |
| E1 | 飞书自定义机器人 webhook URL (open.feishu.cn/…/hook/<uuid>) [Aria#136 形] | - | info:静默 | - | info:静默 | - |
| E2 | json:SecretID=<uuid> (Nomad/Consul ACL) | - | info:静默 | - | info:静默 | - |
| E3 | VAULT_TOKEN=hvs.<90> | - | info:告警 | env-line=1 | info:告警 | env-line=1 |
| E4 | VAULT_TOKEN = hvs.<90> (带空格) | - | info:静默 | - | info:告警 | kv-assign=1 |
| S-read_test-ini | Read(套件合成形 `{content}`): JWT_SECRET = <44 b64> | ALERT | GAP | - | OK | kv-assign=1 |
| S-read_test-json | Read(合成形): json:client_secret=<32> | ALERT | OK | json=1 | OK | json=1 |
| S-read_test-akia | Read(合成形): AKIA<16> | ALERT | OK | aws-access-key-id=1 | OK | aws-access-key-id=1 |
| **S-read_real-ini** | **Read(真实形 `file.content`)**: JWT_SECRET = <44 b64> (brief 要求的 Read+ini 用例) | ALERT | **GAP** | - | OK | kv-assign=1 |
| **S-read_real-json** | Read(真实形): json:client_secret=<32> (阳性对照) | ALERT | **GAP** | - | OK | json=1 |
| **S-read_real-akia** | Read(真实形): AKIA<16> (provider 对照) | ALERT | **GAP** | - | OK | aws-access-key-id=1 |
| S-write_real-ini | Write(真实形): JWT_SECRET = <44 b64> | ALERT | GAP | - | OK | kv-assign=1 |
| S-write_real-json | Write(真实形): json:client_secret=<32> | ALERT | OK | json=1 | OK | json=1 |
| S-write_real-akia | Write(真实形): AKIA<16> | ALERT | OK | aws-access-key-id=1 | OK | aws-access-key-id=1 |
| S-edit_real-ini | Edit(真实形): JWT_SECRET = <44 b64> | ALERT | GAP | - | OK | kv-assign=1 |
| S-edit_real-json | Edit(真实形): json:client_secret=<32> | ALERT | GAP | - | OK | json=1 |
| S-edit_real-akia | Edit(真实形): AKIA<16> | ALERT | GAP | - | OK | aws-access-key-id=1 |
| S-bash-stderr-akia | 仅在 `stderr` 字段 (**人工构造; 真实 CC 把命令 stderr 并入 stdout, 故非实际缺口**) | ALERT | GAP | - | OK | aws-access-key-id=1 |
| S-bash-str-akia | `tool_response` 为裸字符串 | - | info:静默 | - | info:告警 | aws-access-key-id=1 |

### 3.3 读表要点

1. **三个 issue 对应的 GAP 根因都在两行代码**: `:227` 键表缺 `token`/`sha1` 且只认精确小写键 (J1-J3, JX1-JX6); `:224` 要求行首、`=` 零空白、无引号、无 `export`、仅大写 (K1/K3/K5/K6/K8, KX1-KX4)。header 形 (`Authorization: token`, `CF-Access-Client-Secret`) 与大写键的 JSON 映射 (Nomad/compose) 是模式表里完全没有的形状 (K9/K11/KX6/KX7/JX9/JX10)。
2. **M-形 (#203 原事件) 在 `sed -n` 打印行区间时只会露出 `JWT_SECRET = …` 一行**: 基线对该形状 0/5 —— 与决策单一致。
3. **提取路径缺口独立于模式缺口**: 即使把模式全补齐, `S-read_real-*` 与 `S-edit_real-*` 仍 0/5 (基线的 provider 对照 `AKIA` 在真实 Read 形状下也是 GAP 就是证明)。
4. **FP 并非新增模式才有**: 基线对既有键已 5/5 误报占位/掩码值; 我自己的 Write(matrix 脚本)与打印矩阵表在 live 上各触发 `DETECTED 10` / `DETECTED 7` (表里 `<40 b64>` 这类尖括号占位 ≥8 字符被当成值) —— 「讨论凭据格式的文本」会命中。
5. **F5*/F6*/F7/F8 (git sha / digest / UUID / lockfile) 基线与原型都静默**, 这是将来若做 #154 的「高熵裸串」第二判据时必须保住的回归护栏 (本矩阵已含)。

### 3.4 复跑脚本 `matrix_paste.py` (源码不含任何凭据形状字面量; 假值标记运行时拼装; 已验证对基线/原型自身文本静默)

```python
#!/usr/bin/env python3
"""matrix_paste.py -- detection matrix runner for aria/hooks/secret-scan.sh (PostToolUse L3).

Rule #7 safe:
  * every secret-shaped value is generated at runtime (secrets module) and fed to the hook on stdin
    via subprocess (capture_output=True); nothing is printed; the report holds only exit code /
    alert yes-no / tag names / log booleans.
  * source text contains NO credential-shaped literal (fake markers are assembled at runtime), so this
    file itself does not trip secret-scan / secret-guard.
Usage:  python3 matrix_paste.py --hook <path/to/secret-scan.sh> [--trials 5] [--out NAME] [--only J1,K1]
Needs:  bash, jq, python3.  HOME is redirected to a throw-away dir per run (the real ~/.claude/logs is never touched).
"""
import argparse, base64, concurrent.futures as cf, hashlib, json, os, re, secrets, shutil
import statistics, string, subprocess, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
ALNUM, HEX = string.ascii_letters + string.digits, "0123456789abcdef"

# ---------------------------------------------------------------- runtime value generators
def alnum(n): return "".join(secrets.choice(ALNUM) for _ in range(n))
def hexs(n): return "".join(secrets.choice(HEX) for _ in range(n))
def b64std_44(): return base64.b64encode(secrets.token_bytes(32)).decode()            # 44 chars, '=' padded
def b64url(n): return base64.urlsafe_b64encode(secrets.token_bytes(n)).decode().rstrip("=")[:n]
def _e(b): return base64.urlsafe_b64encode(b).decode().rstrip("=")
def jwt_like(): return (_e(b'{"alg":"HS256","typ":"JWT"}') + "." +
                        _e(json.dumps({"nbf": 1700000000 + secrets.randbelow(10 ** 6)}).encode()) + "." + _e(secrets.token_bytes(32)))
def uuid4(): h = hexs(32); return f"{h[:8]}-{h[8:12]}-4{h[13:16]}-a{h[17:20]}-{h[20:32]}"
def akia(): return "AKIA" + "".join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16))
G = {  # name -> generator ; fake/mask markers are ASSEMBLED here so no literal appears in source
    "hex8": lambda: hexs(8), "hex40": lambda: hexs(40), "hex64": lambda: hexs(64),
    "alnum16": lambda: alnum(16), "alnum20": lambda: alnum(20), "alnum24": lambda: alnum(24), "alnum32": lambda: alnum(32),
    "alnum36": lambda: alnum(36), "alnum40": lambda: alnum(40), "alnum64": lambda: alnum(64), "alnum90": lambda: b64url(90),
    "b64url40": lambda: b64url(40), "b64url43": lambda: b64url(43), "b64std44": b64std_44, "jwt": jwt_like, "uuid": uuid4,
    "akia": akia, "ghp": lambda: "gh" + "p_" + alnum(36), "antkey": lambda: "sk-" + "ant-api03-" + alnum(40),
    "fake24": lambda: "FA" + "KE_" + alnum(24), "notreal": lambda: "NOT-" + "REAL-" + alnum(24),
    "ph": lambda: "PLACE" + "HOLDER_VALUE", "ph11": lambda: "PLACE" + "HOLDER", "red": lambda: "[" + "REDA" + "CTED]",
    "mask": lambda: "*" * 8, "empty": lambda: "", "b64user": lambda: base64.b64encode(("admin:" + alnum(16)).encode()).decode(),
}
def T(tpl, *gens):
    """template with @V0@.. placeholders (value position in tpl is always short, e.g. '@V0@')"""
    def build():
        vals = [G[g]() for g in gens]
        out = tpl
        for i, v in enumerate(vals): out = out.replace(f"@V{i}@", v)
        return out, vals
    return build
def S(text): return lambda: (text, [])
def appini():
    v = [G["b64url43"](), G["b64std44"](), G["jwt"](), G["alnum64"](), G["alnum20"]()]
    txt = ("[server]\nAPP_DATA_PATH = /var/lib/forgejo\nLFS_JWT_SECRET = @0@\n\n[oauth2]\nJWT_SECRET = @1@\n\n"
           "[security]\nINSTALL_LOCK = true\nINTERNAL_TOKEN = @2@\nSECRET_KEY = @3@\n\n[database]\nDB_TYPE = postgres\nPASSWD = @4@\n")
    for i, x in enumerate(v): txt = txt.replace(f"@{i}@", x)
    return txt, v
def lines(fmt, n, *gens): return lambda: ("\n".join(fmt.replace("@V0@", G[gens[0]]()) for _ in range(n)), [])
def gitlog_full(): return "\n".join(f"commit {hexs(40)}\nAuthor: A Dev\nDate: Tue Sep 30 10:00:00 2026\n\n    fix: typo\n" for _ in range(3)), []
def npm_integrity(): return '    "node_modules/foo": {\n      "integrity": "sha512-%s"\n    }\n' % base64.b64encode(secrets.token_bytes(64)).decode(), []
def pat_response():
    s = hexs(40); return '{"id":7,"name":"ci","sha1":"%s","token_last_eight":"%s","scopes":["all"]}' % (s, s[-8:]), [s]

# (id, group, label, builder, desired, shapes) ; desired: ALERT | QUIET | None(info)   labels use 'json:KEY=<shape>' so they carry no quoted-value literal
B2 = ("bash_real", "bash_test")          # bash_real = real CC shape {stdout,stderr,...}; bash_test = the suite's {output} shape
CASES = [
 ("J1","json","json:token=<40 hex> (08-20 incident)",T('{"token":"@V0@"}',"hex40"),"ALERT",B2),
 ("J1b","json","json:token=<40 alnum>",T('{"token":"@V0@"}',"alnum40"),"ALERT",B2),
 ("J2","json","json:token=<40 b64url> (space after colon)",T('{"token": "@V0@"}',"b64url40"),"ALERT",B2),
 ("J3","json","json:sha1=<40 hex> (Forgejo PAT creation)",T('{"sha1":"@V0@"}',"hex40"),"ALERT",B2),
 ("J4","json","json:client_secret=<32> (positive control)",T('{"client_secret":"@V0@"}',"alnum32"),"ALERT",B2),
 ("J5","json","json:password=<16>",T('{"password":"@V0@"}',"alnum16"),"ALERT",B2),
 ("J6","json","json:api_key=<32>",T('{"api_key":"@V0@"}',"alnum32"),"ALERT",B2),
 ("J7","json","json:secret=<24>",T('{"secret":"@V0@"}',"alnum24"),"ALERT",B2),
 ("J8","json","json:access_token=<36>",T('{"access_token":"@V0@"}',"alnum36"),"ALERT",B2),
 ("J9","json","json:private_key=<40 b64>",T('{"private_key":"@V0@"}',"b64url40"),"ALERT",B2),
 ("JX1","json-x","json:registration_token=<40 alnum>",T('{"registration_token":"@V0@"}',"alnum40"),"ALERT",B2),
 ("JX2","json-x","json:jwt_secret=<43 b64url>",T('{"jwt_secret":"@V0@"}',"b64url43"),"ALERT",B2),
 ("JX3","json-x","json:Token=<40 hex> (capitalised key)",T('{"Token":"@V0@"}',"hex40"),"ALERT",B2),
 ("JX4","json-x","json:auth_token=<40 alnum>",T('{"auth_token":"@V0@"}',"alnum40"),"ALERT",B2),
 ("JX5","json-x","pretty-printed multi-line json:token=<40 hex>",T('{\n  "token": "@V0@"\n}\n',"hex40"),"ALERT",B2),
 ("JX6","json-x","full Forgejo PAT-create response (sha1 + token_last_eight)",pat_response,"ALERT",B2),
 ("JX7","json-x","json:token=<provider-prefixed gh token> (double-count probe)",T('{"token":"@V0@"}',"ghp"),"ALERT",B2),
 ("JX8","json-x","json:api_key=<provider-prefixed anthropic key> (double-count probe)",T('{"api_key":"@V0@"}',"antkey"),"ALERT",B2),
 ("JX9","json-x","json Env-map JWT_SECRET=<44 b64> (Nomad/compose uppercase key)",T('{"Env":{"JWT_SECRET":"@V0@"}}',"b64std44"),"ALERT",B2),
 ("JX10","json-x","json:DB_PASSWORD=<20 alnum> (uppercase key, pretty)",T('{\n  "DB_PASSWORD": "@V0@"\n}',"alnum20"),"ALERT",B2),
 ("K1","ini","JWT_SECRET = <44 std-b64>  (spaces around =, #203 leak form)",T("JWT_SECRET = @V0@","b64std44"),"ALERT",B2),
 ("K1b","ini","JWT_SECRET = <43 b64url>",T("JWT_SECRET = @V0@","b64url43"),"ALERT",B2),
 ("K2","ini","JWT_SECRET=<44 std-b64>  (no spaces; owner sheet: detected)",T("JWT_SECRET=@V0@","b64std44"),"ALERT",B2),
 ("K3","ini","SECRET_KEY = <64 alnum>",T("SECRET_KEY = @V0@","alnum64"),"ALERT",B2),
 ("K4","ini","INTERNAL_TOKEN = <JWT-shaped>",T("INTERNAL_TOKEN = @V0@","jwt"),"ALERT",B2),
 ("K5","ini","PASSWD = <20 alnum>  (Forgejo [database])",T("PASSWD = @V0@","alnum20"),"ALERT",B2),
 ("K6","ini","LFS_JWT_SECRET = <43 b64url>",T("LFS_JWT_SECRET = @V0@","b64url43"),"ALERT",B2),
 ("K7","ini","YAML password: <16 alnum>",T("password: @V0@","alnum16"),"ALERT",B2),
 ("K8","ini","export API_TOKEN=<32 alnum>",T("export API_TOKEN=@V0@","alnum32"),"ALERT",B2),
 ("K9","ini","Authorization: token <40 hex>  (Forgejo/Gitea PAT header)",T("Authorization: token @V0@","hex40"),"ALERT",B2),
 ("K10","ini","Authorization: Bearer <32 alnum> (positive control)",T("Authorization: Bearer @V0@","alnum32"),"ALERT",B2),
 ("K11","ini","CF-Access-Client-Secret: <64 hex>",T("CF-Access-Client-Secret: @V0@","hex64"),"ALERT",B2),
 ("KX1","ini-x","JWT_SECRET=\"<44 b64>\"  (dotenv, double-quoted)",T('JWT_SECRET="@V0@"',"b64std44"),"ALERT",B2),
 ("KX2","ini-x","JWT_SECRET='<44 b64>'  (dotenv, single-quoted)",T("JWT_SECRET='@V0@'","b64std44"),"ALERT",B2),
 ("KX3","ini-x","export API_TOKEN=\"<32 alnum>\"",T('export API_TOKEN="@V0@"',"alnum32"),"ALERT",B2),
 ("KX4","ini-x","YAML api_key: \"<32 alnum>\"  (quoted)",T('api_key: "@V0@"',"alnum32"),"ALERT",B2),
 ("KX5","ini-x","DB_PASSWORD=<20 alnum>  (env-line control)",T("DB_PASSWORD=@V0@","alnum20"),"ALERT",B2),
 ("KX6","ini-x","curl -H \"Authorization: token <40 hex>\" (command echo)",T('curl -s -H "Authorization: token @V0@" https://forgejo.example/api/v1/user',"hex40"),"ALERT",B2),
 ("KX7","ini-x","CF-Access-Client-Id + -Secret header pair (curl -H echo)",T('-H "CF-Access-Client-Id: @V0@.access" -H "CF-Access-Client-Secret: @V1@"',"alnum32","hex64"),"ALERT",B2),
 ("KX8","ini-x","app.ini fragment with 5 secrets",appini,"ALERT",B2),
 ("KX9","ini-x","password=<16 alnum> (lowercase; suite: out of scope)",T("password=@V0@","alnum16"),None,B2),
 ("KX10","ini-x","Authorization: Basic <b64 user:pass>",T("Authorization: Basic @V0@","b64user"),None,B2),
 ("F1","fp","json:token=FAKE_<24>",T('{"token":"@V0@"}',"fake24"),"QUIET",B2),
 ("F1b","fp","json:password=FAKE_<24> (legacy key)",T('{"password":"@V0@"}',"fake24"),"QUIET",B2),
 ("F1c","fp","json:client_secret=PLACEHOLDER_VALUE",T('{"client_secret":"@V0@"}',"ph"),"QUIET",B2),
 ("F1d","fp","json:api_key=NOT-REAL-<24>",T('{"api_key":"@V0@"}',"notreal"),"QUIET",B2),
 ("F2","fp","json:token=PLACEHOLDER",T('{"token":"@V0@"}',"ph11"),"QUIET",B2),
 ("F3","fp","json:token=[REDACTED]",T('{"token":"@V0@"}',"red"),"QUIET",B2),
 ("F3b","fp","json:password=[REDACTED] (legacy key)",T('{"password":"@V0@"}',"red"),"QUIET",B2),
 ("F4","fp","json:sha=<40 hex> (git commit sha)",T('{"sha":"@V0@"}',"hex40"),"QUIET",B2),
 ("F4b","fp","json:commit.id=<40 hex>",T('{"commit":{"id":"@V0@"}}',"hex40"),"QUIET",B2),
 ("F5","fp","git log --oneline (6 lines)",lines("@V0@ docs(handoff): session closeout note",6,"hex8"),"QUIET",B2),
 ("F5b","fp","git log full format (3 x commit <40 hex>)",gitlog_full,"QUIET",B2),
 ("F5c","fp","git rev-parse HEAD (bare 40 hex)",T("@V0@","hex40"),"QUIET",B2),
 ("F5d","fp","git ls-remote (2 lines)",lines("@V0@\trefs/heads/master",2,"hex40"),"QUIET",B2),
 ("F5e","fp","git submodule status",lines(" @V0@ aria (v1.74.1)",2,"hex40"),"QUIET",B2),
 ("F6","fp","sha256sum output line",T("@V0@  ./aria/hooks/secret-scan.sh","hex64"),"QUIET",B2),
 ("F6b","fp","docker images --digests (sha256:<64 hex>)",T("aria-runner  latest  sha256:@V0@  2 days ago","hex64"),"QUIET",B2),
 ("F7","fp","UUID v4 bare",T("@V0@","uuid"),"QUIET",B2),
 ("F7b","fp","json:uuid=<uuid>",T('{"uuid":"@V0@"}',"uuid"),"QUIET",B2),
 ("F8","fp","npm lockfile integrity sha512-<b64>",npm_integrity,"QUIET",B2),
 ("F9","fp","json:password=<empty>",T('{"password":"@V0@"}',"empty"),"QUIET",B2),
 ("F10","fp","json:password=******** (legacy key)",T('{"password":"@V0@"}',"mask"),"QUIET",B2),
 ("F10b","fp","json:token=********",T('{"token":"@V0@"}',"mask"),"QUIET",B2),
 ("F11","fp","json:token_last_eight=<8 hex> (Forgejo metadata)",T('{"token_last_eight":"@V0@"}',"hex8"),"QUIET",B2),
 ("F12","fp","Actions yaml  token: ${{ secrets.X }}",S("        token: ${{ secrets.FORGEJO_TOKEN }}"),"QUIET",B2),
 ("F13","fp","curl example  Authorization: token $VAR",S('curl -H "Authorization: token $FORGEJO_TOKEN" https://x/api/v1/user'),"QUIET",B2),
 ("F14","fp","JWT_SECRET = <angle-bracket placeholder>",S("JWT_SECRET = <your-secret-here>"),"QUIET",B2),
 ("F15","fp","JWT_SECRET=$(command substitution)",S("JWT_SECRET=$(openssl rand -base64 32)"),"QUIET",B2),
 ("F16","fp","PASSWD =  (empty)",S("PASSWD = "),"QUIET",B2),
 ("F17","fp","grep -n JWT_SECRET app.ini (key name only)",S('grep -n "JWT_SECRET" /etc/forgejo/app.ini'),"QUIET",B2),
 ("F18","fp","JWT_SECRET = ${TEMPLATE_REF}",S("JWT_SECRET = ${JWT_SECRET}"),"QUIET",B2),
 ("F19","fp","YAML password: ********",T("password: @V0@","mask"),"QUIET",B2),
 ("F20","fp","prose: set the token in your config file",S("Set the token in your config file, then restart the service."),"QUIET",B2),
 ("E1","env","Feishu custom-bot webhook URL (open.feishu.cn/.../hook/<uuid>)",T("https://open.feishu.cn/open-apis/bot/v2/hook/@V0@","uuid"),None,B2),
 ("E2","env","json:SecretID=<uuid> (Nomad/Consul ACL)",T('{"AccessorID":"00000000-0000-4000-8000-000000000000","SecretID":"@V0@"}',"uuid"),None,B2),
 ("E3","env","VAULT_TOKEN=hvs.<90>",T("VAULT_TOKEN=hvs.@V0@","alnum90"),None,B2),
 ("E4","env","VAULT_TOKEN = hvs.<90> (spaces)",T("VAULT_TOKEN = hvs.@V0@","alnum90"),None,B2),
]
for shp in ("read_test", "read_real", "write_real", "edit_real"):      # extraction-path cases (same 3 contents per tool)
    CASES += [(f"S-{shp}-ini","shape",f"{shp}: JWT_SECRET = <44 b64>",T("JWT_SECRET = @V0@","b64std44"),"ALERT",(shp,)),
              (f"S-{shp}-json","shape",f"{shp}: json:client_secret=<32> (control)",T('{"client_secret":"@V0@"}',"alnum32"),"ALERT",(shp,)),
              (f"S-{shp}-akia","shape",f"{shp}: AKIA<16> (provider control)",T("AWS_ACCESS_KEY_ID=@V0@","akia"),"ALERT",(shp,))]
CASES += [("S-bash-stderr-akia","shape","bash_stderr: AKIA<16> only in the stderr field (artificial: real CC merges cmd stderr into stdout)",T("AWS_ACCESS_KEY_ID=@V0@","akia"),"ALERT",("bash_stderr",)),
          ("S-bash-str-akia","shape","bash_string: tool_response is a bare string",T("error: AWS_ACCESS_KEY_ID=@V0@","akia"),None,("bash_string",))]

# ---------------------------------------------------------------- tool_response envelopes (real Claude Code 2.1.x shapes)
def envelope(shape, c):
    n = c.count("\n") + 1
    tr = {"bash_test": {"output": c},
          "bash_real": {"stdout": c, "stderr": "", "interrupted": False, "isImage": False, "noOutputExpected": False},
          "bash_stderr": {"stdout": "", "stderr": c, "interrupted": False, "isImage": False, "noOutputExpected": False},
          "bash_string": c,
          "read_test": {"content": c},
          "read_real": {"type": "text", "file": {"filePath": "/x/app.ini", "content": c, "numLines": n, "startLine": 1, "totalLines": n}},
          "write_real": {"type": "create", "filePath": "/x/f.txt", "content": c, "structuredPatch": [], "originalFile": None, "userModified": False},
          "edit_real": {"filePath": "/x/f.txt", "oldString": "a", "newString": c, "originalFile": "a\n", "replaceAll": False, "userModified": False,
                        "structuredPatch": [{"oldStart": 1, "oldLines": 1, "newStart": 1, "newLines": n, "lines": ["-a"] + ["+" + l for l in c.split("\n")]}]}}[shape]
    return {"tool_name": shape.split("_")[0].capitalize(), "tool_input": {}, "tool_response": tr}

TAG_RE = re.compile(r"Detected (\d+) secret-shape match\(es\) \(([^)]*)\)")
def run_one(hook, case, shape, tmproot):
    cid, grp, label, builder, desired, shapes = case
    content, vals = builder()
    home, tmpd = tempfile.mkdtemp(prefix="h-", dir=tmproot), tempfile.mkdtemp(prefix="t-", dir=tmproot)
    env = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": home, "USER": "matrix", "LANG": "en_US.UTF-8", "TMPDIR": tmpd}
    t0 = time.perf_counter()
    p = subprocess.run(["bash", hook], input=json.dumps(envelope(shape, content)).encode(), capture_output=True, cwd=HERE, env=env, timeout=60)
    ms = (time.perf_counter() - t0) * 1000
    out, err = p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")
    logp = os.path.join(home, ".claude", "logs", "secret-scan.log")
    log = open(logp, encoding="utf-8", errors="replace").read() if os.path.exists(logp) else ""
    alert, nm, bd = False, 0, ""
    try:
        j = json.loads(out) if out.strip() else {}
        alert = bool((j.get("hookSpecificOutput") or {}).get("additionalContext"))
        m = TAG_RE.search(j.get("systemMessage", ""))
        nm, bd = (int(m.group(1)), m.group(2)) if m else (0, "")
    except Exception:
        pass
    r = dict(exit=p.returncode, alert=alert, matches=nm, breakdown=bd, n_secrets=len(vals), log_written=bool(log), ms=round(ms),
             plain_full_in_log=any(v in log for v in vals if v), plain_frag_in_log=any((v[:8] in log or v[-8:] in log) for v in vals if len(v) >= 8),
             hash8_in_log=any(hashlib.sha256(v.encode()).hexdigest()[:8] in log for v in vals if v),
             plain_in_hook_output=any(v in out or v in err for v in vals if v))
    shutil.rmtree(home, ignore_errors=True); shutil.rmtree(tmpd, ignore_errors=True)
    return r

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hook", default=os.path.join(HERE, "aria", "hooks", "secret-scan.sh"))
    ap.add_argument("--trials", type=int, default=5); ap.add_argument("--out", default="matrix"); ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--only", default=""); a = ap.parse_args()
    only = set(x for x in a.only.split(",") if x)
    tmproot = os.path.join(HERE, "tmp-matrix"); os.makedirs(tmproot, exist_ok=True)
    jobs = [(c, s) for c in CASES if not only or c[0] in only for s in c[5] for _ in range(a.trials)]
    res = {}
    with cf.ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(run_one, a.hook, c, s, tmproot): (c[0], s) for c, s in jobs}
        for f in cf.as_completed(futs): res.setdefault(futs[f], []).append(f.result())
    rows = []
    for c in CASES:
        if only and c[0] not in only: continue
        for s in c[5]:
            rs = res[(c[0], s)]; k, n = sum(r["alert"] for r in rs), len(rs)
            v = ("info" if c[4] is None else ("OK" if k == n else "GAP" if k == 0 else "FLAKY") if c[4] == "ALERT" else ("OK" if k == 0 else "FP" if k == n else "FLAKY"))
            rows.append(dict(id=c[0], group=c[1], label=c[2], shape=s, desired=c[4], alerts=f"{k}/{n}", verdict=v,
                             exit_codes=sorted({r["exit"] for r in rs}), tags=sorted({r["breakdown"] for r in rs if r["breakdown"]}),
                             matches=sorted({r["matches"] for r in rs}), n_secrets=rs[0]["n_secrets"], log_written=f'{sum(r["log_written"] for r in rs)}/{n}',
                             plain_full_in_log=any(r["plain_full_in_log"] for r in rs), plain_frag_in_log=any(r["plain_frag_in_log"] for r in rs),
                             hash8_in_log=any(r["hash8_in_log"] for r in rs), plain_in_hook_output=any(r["plain_in_hook_output"] for r in rs),
                             median_ms=round(statistics.median(r["ms"] for r in rs))))
    json.dump(rows, open(os.path.join(HERE, a.out + ".json"), "w"), indent=1)
    print("| id | shape | desired | alerts | verdict | exit | tags | matches/secrets | log | plain(full/frag) | hash8 | plain-in-output | ms |\n|" + "---|" * 13)
    for r in rows:
        print(f"| {r['id']} | {r['shape']} | {r['desired'] or '-'} | {r['alerts']} | {r['verdict']} | {','.join(map(str, r['exit_codes']))} | {'; '.join(r['tags']) or '-'} | "
              f"{','.join(map(str, r['matches']))}/{r['n_secrets']} | {r['log_written']} | {str(r['plain_full_in_log'])[0]}/{str(r['plain_frag_in_log'])[0]} | {str(r['hash8_in_log'])[0]} | {str(r['plain_in_hook_output'])[0]} | {r['median_ms']} |")
    from collections import Counter
    print("\nverdict counts:", dict(Counter(r["verdict"] for r in rows)))
    shutil.rmtree(tmproot, ignore_errors=True)

if __name__ == "__main__":
    main()
```

复跑: `cd $EXP && python3 matrix_paste.py --hook $EXP/aria/hooks/secret-scan.sh --trials 5 --out mx-base` (基线) / `--hook $EXP/cand-aria/hooks/secret-scan.sh --out mx-cand` (原型)。逐行原始 JSON (含每行的 exit/log/明文/hash8 布尔值) 在 `$EXP/mp-baseline.json`、`$EXP/mp-cand2.json`。

### 3.5 live 活体 A/B (本会话, 只用 AWS 文档公开示例 key, 非凭据)

| 动作 | 工具 | 同内容 | live PostToolUse 告警 |
|---|---|---|---|
| `Bash cat probe.txt` | Bash | 含 AKIA…EXAMPLE 的 2 行文本 | **有** (`DETECTED 1`) |
| `Read probe.txt` | Read | 同一文件 | **无** |
| `Edit` 把一行改成含该 key | Edit | newString 含该 key | **无** |
| `printf … >&2` (仅 stderr) | Bash | 同 key 仅写 stderr | **有** (stderr 已并入 stdout) |
| `Write` 含 10 个占位/掩码/FAKE 值的脚本 | Write | 无真实凭据 | **有** (`DETECTED 10`, FP) |

---

## 4. 文档同步面 (改模式/行为/通道时需同步)

**hook 自身 (同一 PR, 同一文件内)**
- `aria/hooks/secret-scan.sh:34` 「~15 patterns」(实 31+PEM)、`:40-53` Scope 清单 (含「argon2」不实)、`:58-68` 「What this does NOT catch」(其中「base64/hex without telltale prefix」「low-entropy」措辞在补键形后需改)、`:72-80` Hook contract (只列 `output`/`content`; 需列真实 Bash/Read/Write/Edit 形状)、`:15-24` 「架构性不可 redact, 非 version-dependent」(与 CC ≥2.1.220 不符)、`:341-345` / `:367` 告警文案里的「cannot redact」。
- `aria/hooks/tests/secret-scan.test.sh` (49 用例; 新夹具只能进此文件或运行时拼装)。
- `aria/hooks/tests/lib/crlf-shim.sh:95` 「Mirrors secret-scan.sh:116」已过期 (当前 `:126`), 且测试 `:246` 依赖 hook `:126` 那行注释文字。
- `aria/.github/secret_scanning.yml:18-22` (GitHub push protection 白名单, 仅两个测试文件)。

**aria-plugin 文档 (子模块 aria)**
- `aria/README.md:33` 与 `aria/README.zh.md:33` (PostToolUse 表格行: 「cannot redact…」); `aria/README.md:153-155` 与 `aria/README.zh.md:153-155` (「PostToolUse cannot redact」代码注释块) —— i18n README 仅「正文实质变更」才重译 (CLAUDE.md #140 B 档)。
- **`aria/VERSION:164`: 「PostToolUse … → secret-scan.sh (v1.24.0 新增, output REDACT)」—— 2026-07-03 诚实降级 cycle 漏改的过期宣称 (实读)**; 另 `:46` 是 v1.51.0 条目 (历史, 不改)。
- `aria/CHANGELOG.md` 新版本条目 (现顶部 `:13` = 1.74.1); 历史 `:1161-1167` (v1.51.0 诚实降级) 与 `:433` (v1.66.3 「PostToolUse 不能 redact ⇒ 唯一防线是请求侧拦截」) 为 append-only 历史, 若采纳 updatedToolOutput 应在新条目里显式订正而非改历史。
- 发版同步面 (CLAUDE.md「版本管理」): `plugin.json:4` / `marketplace.json:3,16` / `VERSION` / `CHANGELOG.md` / `README.md` 五文件 + 主仓 gitlink + 主仓 VERSION + root README badge + `docs/architecture/system-architecture.md` §2.8 与 `version-scheme.md` 的 aria-plugin 版本行; 机械兜底检查 `m6-version-badge-match` / `i18n-readme-translation-currency` / `plugin-version-arch-docs-match`。

**standards 子模块 (共享, 须「本地 merge + 双推」, 禁 Forgejo 服务端合并)**
- `standards/conventions/secret-hygiene.md`: `:23` (Path 3 行), `:286` (secret-scan 行「detect-only」), **`:288` 「49 regression cases」(测试数变即须同步)**, `:295` (§5.2 exit semantics: 「exit 0 always… 不改写 tool_response…唯一可靠防线 = PreToolUse」—— 若采纳 redaction 需重写)。
- `standards/conventions/shell-jq-crlf-hygiene.md:14` (secret-scan CRLF 姊妹条, 仅在 `:125-127` 逻辑改动时需看)。

**历史/记录类 (append-only, 通常不改)**: `.aria/decisions/DEC-20260703-001-…` (若前提被推翻, 新开 DEC 并在其中声明取代关系), `docs/handoff/2026-07-03-secret-scan-honest-downgrade.md`, `.aria/audit-reports/post_spec-R4-…secret-scan-honest-downgrade.md`。
**不在仓内 (容器本地)**: memory `reference_postooluse_cannot_redact_tool_output.md` (「CC PostToolUse 无法 redact」) 若前提变化需由席位更新。
**无读取方**: `secret-scan.log` 格式无消费者 (grep 0 命中), 加字段不需兼容处理; `aria-doctor` 只查 secret-guard 安装态, 不查 secret-scan。

---

## 5. 设计要点与风险

### 5.1 建议写法 (推测; 已在 `$EXP/cand-aria/hooks/secret-scan.sh` 原型验证, 用 `$EXP/cand_patch.py` 从基线副本可重现)

设计原则: **加法式** (不改既有 tag 语义 ⇒ 既有 49 用例零改动全绿)、**线性 ERE** (无回溯/无 perl)、**bash 3.2 安全**、**值从不进日志**。

1. **提取修复 (P0, 与模式无关)**: 主体取 `output`→`content`→`stdout`→`file.content` 的第一个非空串; 另附 `stderr`、Edit 的 `structuredPatch[].lines` (去 diff 前缀一字符; 无 patch 时用 `newString`)、以及 `tool_response` 本身是字符串的情形。
2. **键形模式**: `json-secret-field` 键表 = 既有 10 键 ∪ #154 清单 (`token`、`sha1`) ∪ 封闭的 snake/camel 家族 (`auth_token`/`registration_token`/`api_token`/`bearer_token`/`session_token`/`jwt_secret`/`secret_key`/`apikey` + 驼峰); **不采用**「任意 `*token*` 后缀」(分页 cursor `next_page_token` 等会成 FP)。新增 `json-env-key` (大写环境变量名作 JSON 键: Nomad/compose)、`kv-secret-assign` (INI/env/YAML 赋值: `=`/`:` 两侧可空白、可引号、可 `export`、可缩进、值 ≥12)、`kv-secret-assign-lc` (小写键, 值 ≥16, 可选)、`auth-header-token` (`Authorization: token|Basic`)、`cf-access-client-secret`。
3. **FP 分类器 (通用键形 tag 专属, 不作用于 provider 前缀 tag)**: 对 `grep -oE` 抽出的每个 span 取「值」(kv: 去 1 字符左边界 → 首个 `[:=]` 之后 → 去空白与引号; hdr: 末词), 值匹配 `ALLOW_VALUE_RE` 则**不计数**: `FAKE|PLACEHOLDER|NOT-REAL|EXAMPLE|CHANGEME|YOUR_|REDACTED|[REDACTED` 前缀、以 `<` / `$` / `{{` / `%` 起头 (尖括号占位/变量/模板引用)、全由 `* x X . - _` 构成的掩码; 对**新增**键名再加熵下限 (`is_secretish`: 小写/大写/数字 ≥2 类, 且不是「小写目录段」形路径)。每 tag 分类上限 200 span, 超限 **fail-closed** (照计数)。被分类器放过的 span 仍被哨兵替换, 所以也消除了哨兵回灌重复计数 (JX8 `matches` 2→1)。
4. **日志 `hash8`**: 对每个被接受 span 的**值** (非整个 span) 取 `sha256` 前 8 位, 每事件最多 10 个, 追加到 TSV 第 9 字段; 无 `sha256sum`/`shasum` 则写 `-`。实测全部 170 行无明文无片段。**建议**再加「值长 <16 不哈希」(8 位前缀对低熵短口令可被离线字典确认, 推测) 与「对 shape 类 tag 也按值而非整个 span 哈希」(原型里 env-line/bearer 等已用 `VALUE_KIND` 映射)。
5. **告警文案 (提示文案 hunk, Rule #6 须单独判)**: 建议 `additionalContext` 带上 tag 名单与 (Read/Write/Edit) `tool_input.file_path` / (Bash) 命令摘要 —— 二者都不含值 —— 让告警可行动; 并复核「轮换」措辞与 owner 09-30 「不逐条提示轮换」的关系。

原型 `diff -U2` (基线副本 → 候选; 仅为设计证据, 非可直接合入补丁):

```diff
@@ -134,10 +134,15 @@
 # Try multiple field names since Claude Code versions vary.
 content="$(printf '%s' "$input" | jq -r '  # crlf-ok: data body being SCANNED (internal counting scratch only) — must NOT CR-strip (would corrupt user content, Spec C2)
-  .tool_response.output //
-  .tool_response.content //
-  .tool_response.stdout //
-  .tool_result.content //
-  .tool_result.output //
-  ""
+  def strs: map(select(type == "string" and length > 0)) | join("\n");
+  (.tool_response // .tool_result // null) as $r
+  | if ($r | type) == "string" then $r
+    elif ($r | type) == "object" then
+      ( [ $r.output, $r.content, $r.stdout, ($r.file | objects | .content) ]
+        | map(select(type == "string" and length > 0)) | .[0] // "" ) as $primary
+      | ( [ $r.stderr,
+            ($r.structuredPatch | arrays | map(.lines | arrays | map(.[1:]) | join("\n")) | join("\n")),
+            (if ($r.structuredPatch | type) == "array" then null else $r.newString end) ] | strs ) as $extra
+      | [ $primary, $extra ] | strs
+    else "" end
 ' 2>/dev/null)"
 
@@ -225,5 +230,21 @@
 
   # JSON shape `"password": "..."` / `"secret": "..."` / `"token": "..."`
-  'json-secret-field|"(password|passwd|secret|api_key|access_token|refresh_token|private_key|client_secret|webhook_secret|encryption_key)"[[:space:]]*:[[:space:]]*"[^"]{8,}"'
+  # [PROTOTYPE] json-secret-field: existing key list UNION #154 list (token|sha1) + closed snake/camel token family.
+  'json-secret-field|"(password|passwd|secret|secret_key|jwt_secret|api_key|apikey|access_token|refresh_token|auth_token|registration_token|api_token|bearer_token|session_token|token|private_key|client_secret|webhook_secret|encryption_key|sha1|accessToken|refreshToken|authToken|apiToken|apiKey|clientSecret|secretKey)"[[:space:]]*:[[:space:]]*"[^"]{8,}"'
+
+  # [PROTOTYPE] kv-secret-assign: INI / env / YAML assignment — spaces around =/:, `export`, quoted values, indentation.
+  # Additive to env-line-secret-keyword above (which keeps its exact old semantics).
+  'kv-secret-assign|(^|[^A-Za-z0-9_])(export[[:space:]]+)?[A-Z0-9_]*(SECRET|PASSWORD|PASSWD|TOKEN|API_KEY|APIKEY|PRIVATE_KEY|ENCRYPTION_KEY|ACCESS_KEY)[A-Z0-9_]*[[:space:]]*[=:][[:space:]]*["'"'"']?[A-Za-z0-9+/=._~-]{12,}'
+
+  # [PROTOTYPE] kv-secret-assign-lc: lowercase keys (YAML / ini / code literal): password: X, api_key = "X", client_secret=X.
+  # Stricter: value >= 16 chars AND the >=2-class floor below (kept separate so the owner can drop it alone).
+  'kv-secret-assign-lc|(^|[^A-Za-z0-9_])(export[[:space:]]+)?[a-z0-9_]*(secret|password|passwd|token|api_key|apikey|private_key|encryption_key|access_key)[a-z0-9_]*[[:space:]]*[=:][[:space:]]*["'"'"']?[A-Za-z0-9+/=._~-]{16,}'
+
+  # [PROTOTYPE] json-env-key: env-style UPPERCASE keys inside JSON (Nomad/compose job JSON: "Env":{"JWT_SECRET":"..."}).
+  'json-env-key|"[A-Z0-9_]*(SECRET|PASSWORD|PASSWD|TOKEN|API_KEY|APIKEY|PRIVATE_KEY|ENCRYPTION_KEY|ACCESS_KEY)[A-Z0-9_]*"[[:space:]]*:[[:space:]]*"[^"]{8,}"'
+
+  # [PROTOTYPE] HTTP header credential forms not covered by bearer-token / x-api-key-header.
+  'auth-header-token|[Aa]uthorization:[[:space:]]*([Tt]oken|[Bb]asic)[[:space:]]+[A-Za-z0-9+/=._~-]{20,}'
+  'cf-access-client-secret|[Cc][Ff]-[Aa]ccess-[Cc]lient-[Ss]ecret:[[:space:]]*[A-Za-z0-9._~-]{20,}'
 
   # bcrypt hash
@@ -231,4 +252,65 @@
 )
 
+# ── [PROTOTYPE] generic-tag allow-filter stage + value hashing ────────────────
+# Generic key-form tags (value semantics decided by a key name, not a provider prefix) go through
+# a per-span classifier: spans whose VALUE is an obvious non-secret marker are NOT counted
+# (FAKE/PLACEHOLDER/NOT-REAL/EXAMPLE/REDACTED prefixes, <angle>/$var/{{tpl}} references, masks).
+# Provider-prefix tags never pass through it (their fixtures legitimately contain "FAKE" mid-token).
+# bash-3.2-safe (macOS /bin/bash): NO `declare -A`, NO mapfile/readarray (see secret-guard.sh:118-135 / :538-552 precedent).
+tag_kind() {        # sets KIND = how to cut the VALUE out of a span: kv (key SEP value) | hdr (last word) | "" (span is the value)
+  case "$1" in
+    json-secret-field|json-env-key|kv-secret-assign|kv-secret-assign-lc|env-line-secret-keyword|gcp-private-key-id) KIND=kv ;;
+    auth-header-token|cf-access-client-secret|bearer-token|x-api-key-header) KIND=hdr ;;
+    *) KIND="" ;;
+  esac
+}
+tag_classified() {  # 0 when the tag goes through the allow-filter stage (generic, key-name-driven tags only)
+  case "$1" in
+    json-secret-field|json-env-key|kv-secret-assign|kv-secret-assign-lc|auth-header-token|cf-access-client-secret) return 0 ;;
+  esac
+  return 1
+}
+GENERIC_CLASSIFY_CAP=200          # beyond this many spans per tag: fail-CLOSED (count without classifying)
+ALLOW_VALUE_RE='^(FAKE|PLACEHOLDER|NOT[-_]?REAL|EXAMPLE|CHANGE[-_]?ME|YOUR[-_]|REDACTED|\[REDACTED|<|\$|\{\{|%)|^(\*+|[xX]+|\.+|-+|_+)$'
+PATHLIKE_RE='^(/|~/|\./|\.\./)[a-z0-9._-]+(/|$)'
+VOUT=""
+is_secretish() {    # weak entropy floor for NEW key names: >=2 of {lower,upper,digit} classes, and not path-like
+  local v="$1" c=0
+  [[ "$v" =~ [a-z] ]] && c=$((c + 1))
+  [[ "$v" =~ [A-Z] ]] && c=$((c + 1))
+  [[ "$v" =~ [0-9] ]] && c=$((c + 1))
+  (( c >= 2 )) || return 1
+  [[ "$v" =~ $PATHLIKE_RE ]] && return 1   # path-like: lowercase dir segment (base64 starting with '/' practically never matches)
+  return 0
+}
+needs_secretish() { # $1=tag $2=span  -> 0 when the floor applies (only to key names added by WP-A; legacy keys keep legacy semantics)
+  case "$1" in
+    kv-secret-assign|kv-secret-assign-lc|json-env-key) return 0 ;;
+    json-secret-field)
+      local k="${2%%:*}"; k="${k//[\"[:space:]]/}"
+      case "$k" in token|sha1|auth_token|registration_token|api_token|bearer_token|session_token|authToken|apiToken) return 0 ;; esac ;;
+  esac
+  return 1
+}
+value_of_span() {   # $1=kind(kv|hdr|"") $2=span  -> sets VOUT (no subshell)
+  local v="$2"
+  if [[ "$1" == hdr ]]; then
+    v="${v##*[[:space:]]}"
+  elif [[ "$1" == kv ]]; then
+    local lead="${v%%[A-Za-z0-9_]*}"; v="${v#"$lead"}"      # drop the 1-char left boundary ('(^|[^A-Za-z0-9_])'), which may itself be ':' or '='
+    v="${v#*[:=]}"
+    v="${v#"${v%%[![:space:]]*}"}"
+    v="${v#[\"\']}"
+    v="${v%[\"\']}"
+  fi
+  VOUT="$v"
+}
+sha8() {            # first 8 hex of sha256($1); "-" when no sha tool exists
+  if command -v sha256sum >/dev/null 2>&1; then printf '%s' "$1" | sha256sum | cut -c1-8
+  elif command -v shasum >/dev/null 2>&1; then printf '%s' "$1" | shasum -a 256 | cut -c1-8
+  else printf '%s' '-'; fi
+}
+hash8_list=""; hash8_n=0; HASH8_CAP=10
+
 # ── Scan + count matches ───────────────────────────────────────────────────
 # tmpfile is an INTERNAL match-counting scratch buffer: each matched span is
@@ -290,38 +372,54 @@
   tag="${entry%%|*}"
   pattern="${entry#*|}"
-  # Count occurrences using grep -oE to count MATCHES not LINES (R2 audit I-2 fix: ... [旧计数/消耗/复核循环体共 32 行, 此处从略])
+  tag_kind "$tag"; kind="$KIND"
+  spans=()
+  while IFS= read -r span; do spans+=("$span"); done < <(grep -oE -- "$pattern" "$tmpfile" 2>/dev/null)
+  total=${#spans[@]}
+  (( total == 0 )) && continue
+  accepted=()
+  if tag_classified "$tag"; then
+    n=0
+    for span in "${spans[@]}"; do
+      n=$((n + 1))
+      if (( n <= GENERIC_CLASSIFY_CAP )); then
+        value_of_span "$kind" "$span"
+        [[ "$VOUT" =~ $ALLOW_VALUE_RE ]] && continue
+        if needs_secretish "$tag" "$span"; then is_secretish "$VOUT" || continue; fi
       fi
+      accepted+=("$span")
+    done
+  else
+    accepted=("${spans[@]}")
+  fi
+  count=${#accepted[@]}
+  # hash8 of accepted values (first HASH8_CAP overall). Only the 8-hex prefix ever reaches the log.
+  if (( count > 0 )); then
+    for span in "${accepted[@]}"; do
+      (( hash8_n >= HASH8_CAP )) && break
+      value_of_span "$kind" "$span"
+      hash8_list="${hash8_list}$(sha8 "$VOUT"),"
+      hash8_n=$((hash8_n + 1))
+    done
+  fi
+  # In-place counting-substitution using \x01 as sed delimiter (ALL spans incl. allowed ones, so later
+  # patterns never re-see them).
+  sed -i -E "s${SEP}${pattern}${SEP}<secret-scan-counted:${tag}>${SEP}g" "$tmpfile" 2>/dev/null || {
+    echo "[secret-scan] WARN: counting-substitution failed for pattern tag=${tag}; skipping" >&2
+    continue
+  }
+  residual="$(grep -oE -- "$pattern" "$tmpfile" 2>/dev/null | wc -l | tr -d ' ')"
+  [[ -z "$residual" ]] && residual=0
+  if (( residual > 0 )); then
+    partial_warns="${partial_warns}[secret-scan] NOTE: pattern ${tag} still present after counting-substitution (${residual} span(s) could not be isolated for exact counting); match count may be under-reported."$'\n'
+    actual_counted=$(( count - residual ))
+    if (( actual_counted > 0 )); then
+      matches_total=$(( matches_total + actual_counted ))
+      matches_breakdown="${matches_breakdown}${tag}=${actual_counted}+${residual}-uncounted "
+    else
+      matches_breakdown="${matches_breakdown}${tag}=0+${residual}-uncounted "
     fi
+    continue
+  fi
+  if (( count > 0 )); then
     matches_total=$(( matches_total + count ))
     matches_breakdown="${matches_breakdown}${tag}=${count} "
@@ -356,7 +454,7 @@
 # ~/.claude/logs/guard-bypass.log). Log every detection event.
 mkdir -p "${HOME}/.claude/logs" 2>/dev/null || true
-printf '%s\t%s\t%s\tSCAN-DETECT\ttool=%s\tmatches=%s\tbreakdown=%s\tsize=%s\n' \
+printf '%s\t%s\t%s\tSCAN-DETECT\ttool=%s\tmatches=%s\tbreakdown=%s\tsize=%s\thash8=%s\n' \
   "$(date -u +%FT%TZ)" "${USER:-unknown}" "${PWD:-unknown}" \
-  "$tool" "$matches_total" "${matches_breakdown% }" "$input_size" \
+  "$tool" "$matches_total" "${matches_breakdown% }" "$input_size" "${hash8_list%,}" \
   >> "${HOME}/.claude/logs/secret-scan.log" 2>/dev/null || true
```
(注: 上面循环段为便于阅读把被删除的旧循环体 32 行折成一行注释; 真实 diff 见 `$EXP/cand-U2.diff`。)

**原型验证结果 (实测)**: 既有套件 49/49; 矩阵 §3 (原型 OK 84 / GAP 1 / FP 0); 套件自身运行输出与原型 diff 文本对基线/原型均静默; 对 base64/alnum 类 kv 值 30 trials 无 FLAKY (见 §5.2 第 2 点的下限选型)。**遗留**: (a) 首字母大写键 `Token` (JX3) 未覆盖; (b) 模式表里无飞书 webhook / Nomad-Consul `SecretID` (E1/E2, 属三个 issue 之外); (c) `kv-secret-assign-lc` 有语义性 FP (见下)。

### 5.2 误报面评估 (讨论凭据格式的文档/测试/本 Spec 自己会不会被命中)

**语料普查** (`census.py`: 把仓内文件当作一次 Bash stdout 喂 hook, 只记路径+tag): 505 个文件样本 —— 14 hook/测试源、21 conventions、117 handoff(7-9 月)、58 decisions、16 openspec md、42 SKILL.md、5 aria docs、225 aria-orchestrator 配置类样本、3 本任务 issue 文本、1 本 Spec 草稿、3 我的实验脚本。

| | 基线 | 原型 |
|---|---|---|
| 告警文件 / 505 | 5 | 9 |
| 散文类 (conventions/handoff/decisions/openspec/SKILL/aria docs/issue 文本/Spec 草稿, 共 ≈259) 告警 | 0 | 1 (`standards/conventions/nomad-docker-registry-auth.md:172`: 一个「❌ 凭据明文写进 HCL」的反例, 值形如 `1234567890abcdef…`) |
| `secret-scan.test.sh` (夹具文件) | 告警 33 match | 告警 (+1 kv) |
| `secret-guard.test.sh` (131KB, 599 用例源码) | **静默** | **静默** (原型第一版曾因 `SECRET_GUARD_ACK_PATH=/路径` 告警 3 处, 加下限后消失) |
| aria-layer1 测试/脱敏夹具 | 2 文件告警 | 6 文件告警 (新增 4 个测试夹具文件, 语义即「假 token」) |
| 我自己的实验脚本 | `matrix.py` 告警 (`json-secret-field=10`, 与 live Write 的 `DETECTED 10` 一致) | `matrix.py` **静默** (FAKE/占位/掩码被白名单) |

再做一轮更广的 **raw-hit 普查** (1,183 个 aria/aria-orchestrator/standards/docs/openspec 文本文件, 不含 archive/ab-results/audit-reports): 新模式原始命中 31 个文件 (kv 13 / kv-lc 24 / json-env 1 / auth-header 0), 经完整管线后 **告警 13 个 (基线 3 个)**, 即分类器救回 18 个。新增告警的 10 个文件构成: 测试夹具 5、文档示例/占位 4 (含 `aria-orchestrator/docs/t2-2-job-register-dispatch-evidence.md:38,48` 自述「smoke 占位 (非真实 key)」的 51 字符值, 机器无法区分)、脚本 1 (`setup_relay.sh` 里变量名含 `_tokens` 的 jq 路径表达式)。JSON 键表扩张本身几乎免费: 基线 4 文件 / 朴素 #154 清单 5 文件 / 原型扩展表 5 文件 (原始命中)。

结论与含义:
1. **最大 FP 驱动是 INI/env/YAML 赋值族 (`kv-*`), 不是 JSON 键**。语义性 FP 无法靠正则消除 (值是「名字」「路径」「占位」: `NEW_TOKEN_NAME=<某 token 的名字>`、`*_SECRET_ENV=<环境变量名>`、`secret_prompt=<标记串>`、`exceeds_200k_tokens=<jq 路径>`)。熵下限能挡掉纯单字符类值, 但挡不住「大小写混合的标识符」。
2. **熵下限选型有代价 (实测)**: 先试「含数字」版 → 20 位 alnum 约 3% 无数字被漏 (30 trials 出现 FLAKY), base64 以 `/` 开头的值被「路径」规则误杀 (~1/64); 改成「小写/大写/数字 ≥2 类」+「路径 = `^/|~/|./|../` 后跟**小写目录段**」后, 30 trials 零 FLAKY。仍漏的是「单字符类」值 (全小写随机串、全数字、全大写随机串) —— 需在 Spec 里成文为已知漏报类。
3. **尖括号占位必须放行**: 朴素 #154 正则 `"[^"]{8,}"` 会把 `"token": "<40 hex>"` / `<40 b64>` 当成值 (我打印自己的矩阵表时 live 告警 7 次, 其中 `json:private_key=<40 b64>`、`json:api_key=<sk-ant-api03- 40>` 即此类)。Spec 文档与 issue 文本本身会有大量这类写法; 「值以 `<` 起头」规则使 3 份 issue 文本、Spec 草稿在原型下静默 (G/J 组 0 告警)。
4. **本 Spec 自己会不会被命中**: 用占位 (`<…>`)、`FAKE`/`PLACEHOLDER` 前缀或省略号 (`…`) 写示例则不会; 写「真实形状」(40 hex 裸值、`JWT_SECRET = <44 位 base64 真值>`) 会命中且 **会被 push protection 拦** (仅两个测试文件在 `secret_scanning.yml` 白名单)。

### 5.3 恒红 / 恒绿风险

**恒红 (持续告警、零信息)**
- **修好 Read 提取会制造新的红**: 凡读取夹具文件 (`aria/hooks/tests/secret-scan.test.sh` 33 match; aria-layer1 测试) 都会注入「视为已泄露 / 建议轮换」。历史上这些文件在 37 个会话里从未被 Read/Edit/Write (0 次, transcript 路径统计), 但 **WP-A 自己会反复编辑它们**。需要「夹具静默机制」: 路径白名单 (`*/hooks/tests/*`, `*/tests/fixtures/*`, 仅日志不注入 additionalContext) / 行内标记 / 不做。与 secret-guard #203 要求的「项目级扩展入口 (`.aria/` 下路径清单)」同构, 建议两层共用一套机制。
- **既有键的占位值** (F1b/F1c/F1d/F3b/F10 5/5) —— 已由分类器解决。
- **套件污染真实日志** (§1.7): 应在套件顶部 `export HOME="$(mktemp -d)"` 并加一条断言「套件自身不写真实日志」。
- **文档式占位 key** (t2-2 evidence 等): 无法机械区分, 只能接受残余或用行内标记。
- **secret-guard 自己的测试输出会不会天天告警**: 运行输出 (≤665B 摘要)、源码 (基线/原型) 均静默 ⇒ 不会。secret-guard.test.sh 失败回显的命令文本若含夹具命令, 理论上可命中 (本次未构造失败场景验证)。

**恒绿 (永不失败的断言)**
- **现状就是一例**: Read 用例用合成 `{content}` 形状, 生产形状 `file.content` 下 hook 失明但套件 49/49 绿 (memory `completion_signals_vs_runtime_invocation` / `test_asserts_what_its_name_claims`)。新测试必须用**真实形状信封** (Bash `{stdout,stderr,…}`, Read `{type,file:{content…}}`, Write, Edit `structuredPatch`)。
- **允许类用例必须与同形状的拒绝类成对** (F1↔J1 …), 否则「FAKE 被放过」在模式根本没覆盖该键时也恒绿 (F1/F2/F3 对基线正是如此: 基线对 `token` 键本就静默)。
- **正向夹具不得以 `FAKE`/`PLACEHOLDER` 开头** (会被白名单吞掉 ⇒ 检测用例变红; 反之若有人为躲 push protection 改成 FAKE 前缀, 需让测试立刻红)。
- **`expect_detect` 只断言「某 tag 名出现在 systemMessage」**: 新 tag 上线后旧断言可能被别的 tag 满足; 新用例需指名新 tag 并断言 `matches` 数。
- `matches>=2` 的既有多命中用例会被「哨兵重复计数」顺带满足 —— 计数类断言要用 JX8 那种「1 个凭据 ⇒ matches==1」的反例。
- 静态检查: 加一条 grep 断言「secret-scan.sh 不含 `declare -A`/`mapfile`/`readarray`」(bash 3.2 护栏), 与 jq-crlf-guard 同类; 新增 `VAR=$(… jq -r …)` 须带 `# crlf-ok` 或 `${VAR%$'\r'}` (否则 `tests/jq-crlf-guard.sh` 红)。
- 性能护栏: 稠密 200KB 输入 <5 s (本机 1.3 s)。

### 5.4 兼容性 / 平台 / 其他风险

- **bash 3.2 / zsh**: 见 §0.8。另 `set -u` 下 bash <4.4 对空数组 `"${a[@]}"` 会报 unbound —— 原型已保证只在非空时展开。
- **macOS BSD sed**: 既有代码 `sed -i -E` (`:278`, `:300`; `perl -0i` 另议) 在 BSD sed 上语义不同 (`-i` 需后缀参数) ⇒ 计数替换失败 ⇒ 每个模式都 `continue` (推测: macOS 上整个 hook 静默失明); 无 macOS 实测, 原型沿用同样的 `sed -i -E`, 未更糟。
- **Windows Git-Bash**: 5 s 超时 + 进程派生开销 (§1.8) 未实测。
- 超时即静默漏检 (官方文档); `mktemp` 缓冲文件在被 SIGKILL 时遗留 (实测, 0600, 含输出全文)。
- PEM 预扫超线性 (既有; 是否在 WP-A 内顺手修由 Spec 定)。
- **`updatedToolOutput` 若启用**: 必须整体回传合乎各工具 `outputSchema` 的对象 (Bash: `{stdout,stderr,interrupted,isImage,…}`; Read: `{type:"text",file:{…}}`), 否则 CC 回退原输出并记 hook_error_during_execution; Write/Edit 被忽略; 误报代价从「多一条提醒」升级为「模型看不到被误脱敏的正文」, 使 FP 白名单/熵下限成为前置条件 (与 WP-A 的 FP 工作同向); 多 hook 并行/叠加语义与文档不一致; 需要最低 CC v2.1.220 (旧版对未知字段行为未验证)。`hookSpecificOutput.updatedToolOutput` 在 CC 2.1.285 二进制里的 schema 原文: 「Replaces the tool output before it is sent to the model」。

### 5.5 建议的 AC 草案 (推测, 供 Spec 起草参考)

1. **提取**: 真实形状 Bash/Read/Write/Edit 信封各自能检出 provider 对照 (基线下 Read/Edit 红 → baseline-failing 测试, 符合 owner 2026-08-02 对 hook 的 substitute 框定)。
2. **键形**: §3 的 J1-J3、JX1/JX2/JX4-JX6/JX9/JX10、K1/K3/K5/K6/K8/K9/K11、KX1-KX4/KX6/KX7/KX8 全检出 (KX8 断言 `matches==5`)。
3. **FP**: F1-F20 静默, 且每个 allow 用例配同形状 deny 用例。
4. **日志**: 命中事件的日志行含 `hash8`、不含明文/8 位片段 (对 stdout/stderr 同断言); 套件不写真实日志。
5. **计数**: JX8 `matches==1`。
6. **兼容**: 静态断言无 bash-4-only 构造; 稠密输入 <5 s。
7. **文档**: §4 清单 + `secret-hygiene.md:288` 计数。

### 5.6 三个 issue 之外的候选 (scope-creep, 仅记录)

飞书 webhook URL (`open.feishu.cn/open-apis/bot/v2/hook/<uuid>`, Aria#136 形, E1 静默)、Nomad/Consul `SecretID` (UUID 形, E2 静默)、首字母大写键 (`Token`/`Password`/`SecretID`, JX3)、Vault `hvs.` (env-line 已覆盖 E3)、matcher 缺 `Grep`/`PowerShell`。

---

## 6. 实验目录 `$EXP` 清单 (可复跑)

`aria/` (基线副本, 只读用) · `cand-aria/` (原型, 由 `cand_patch.py` 自基线生成) · `matrix_paste.py` / `matrix.py` · `census.py` (语料普查) · `perf.py` / `perf2.py` / `ab_perf.py` / `perf_pem.py` (性能) · `mp-baseline.json` / `mp-cand2.json` (逐行原始结果) · `census-baseline.json` / `census-cand7.json` · `cand-U2.diff` · `shape_probe.py` / `stderr_probe.py` / `stderr_shape_probe.py` / `readshape_probe.py` / `size_probe.py` / `tools_probe.py` / `readpaths_probe.py` (transcript 结构/尺寸探针, 仅输出键名/类型/计数/形状) · `binprobe*.py` (对本机 `claude` 2.1.285 二进制的只读字符串探针) · `baseline-test-run.txt` (49/49 输出)。
复跑示例 (HOME 务必隔离): `cd $EXP && HOME=$EXP/home-cand bash cand-aria/hooks/tests/secret-scan.test.sh`; `python3 census.py --hook $EXP/cand-aria/hooks/secret-scan.sh --out census-x`; `python3 ab_perf.py`。

### 附: Rule #7 / 自我纪律说明
- 全程未读取真实凭据; transcript 探针只输出键名/类型/长度/计数/字符形状 (字母→a、数字→0)。
- 读取 `aria/hooks/tests/secret-scan.test.sh` (公开 FAKE 夹具) 与 live 探针使用的 AWS 文档公开示例 key 各触发过 L3; 本会话 live L3 共 6 次, 全部是 FP (占位/掩码/公开夹具/公开示例), **无需轮换, 也不需要提示轮换** (与 owner 09-30 决定一致)。
- 未做 git 写操作、未改仓内文件、未开 issue/评论、未用 Agent 工具; 未对真实 `~/.claude/logs` 写入 (HOME 全程隔离); 对真实日志与 transcript 只做只读聚合。

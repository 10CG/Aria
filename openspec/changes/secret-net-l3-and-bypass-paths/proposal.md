# Secret 防护网补洞: L3 读取失明与键形缺口 + L1 服务端配置 / 变量间接 / 进程表旁路

> **Level**: Minimal (Level 2 Spec)
> **Status**: Draft
> **Created**: 2026-09-30
> **Linked Issue**: `10CG/aria-plugin#154, 10CG/aria-plugin#203, 10CG/Aria#221`
> **认领**: track `secret-net-l3-and-bypass-paths-023236f2` @ simonfish/023236f2 (session `s-3e77@1757`), phase1_gate A.1 advisory, 2026-09-30T17:57:13Z, `linked_issue_overlap == []`。`--linked-issue` 只接受单值, 认领传的是 `10CG/aria-plugin#154`; 10CG/aria-plugin#203 与 10CG/Aria#221 对其它容器的碰撞检测不可见, 以本头部与决策单声明
> **基线冻结**: aria `268da8f` (= v1.74.1); 主仓 `0748dbc`; standards `2bc1c4c` —— 文中行号与计数均对此; SC 的基线值都来自同目录 `baseline_probe.py` 的实跑输出 (SC-30 除外, 见该条), 原样存于 `baseline-evidence.md`
> **代码落点**: aria 子模块 `hooks/secret-scan.sh`、`hooks/secret-guard.sh`、`hooks/tests/secret-scan.test.sh`、`hooks/tests/secret-guard.test.sh` (+ 发版六文件); standards `conventions/secret-hygiene.md`; Spec 落主仓 (Rule #5)。`hooks/hooks.json` 与 `.aria/config.json` 不动
> **决策来源**: `.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md` —— 第 1 项 (B 类第 5 项 secret 网补洞归 WP-A) / 第 2 项 (凭据轮换全部延后, 不产出轮换清单、不逐条提示) / 第 3 项 (WP-A = Level 2; Rule #6 沿用 owner 2026-08-02 的 hook substitute 框定, 提示文案 hunk 单独判) / 第 4 项 (一次性授权的四类外发动作) / 第 5 项 (023236f2 串行 WP-C → WP-A → WP-B)
> **Level 对账**: LEVEL_GUIDE §跨模块判断「影响多个子模块 → 自动提升为 Level 3」字面命中 (aria + standards); 决策单第 3 项已裁 Level 2; 同型先例四份均为 Level 2 且同改 aria hook 与 standards `secret-hygiene.md` (`2026-07-03-secret-scan-honest-downgrade` / `2026-08-02-secret-guard-nomad-var-put-echo` / `2026-08-18-secret-guard-per-segment-evaluation` / `2026-08-22-secret-guard-manifest-precision`); 反例一份 (`2026-07-11-secret-guard-bash3-multiline-hardening` 以 blast radius 定 Level 3)。本 Spec 按 owner 裁定执行 Level 2, 升级与否列入「待 owner 复议」第 4 条, 不自行改级

---

## Why

三个 issue 指向同一张防护网的三个洞, 两层都有:

- **L3 (`hooks/secret-scan.sh`, PostToolUse, 检测 + 告警)**: 2026-08-20 事故的 `{"token":…}` 与 2026-09-26 事故的 `JWT_SECRET = <值>` (等号两侧带空格) 都从全部模式底下穿过 (10CG/aria-plugin#154、10CG/aria-plugin#203)。研究又发现一个更深的前置缺口: 提取链只认 `output` / `content` / `stdout`, 而 Claude Code 2.1.285 的 Read 结果是 `{type:"text", file:{content,…}}` —— **生产中 Read 从未被扫描**, 现有 Read 用例用的是合成形状所以一直绿 (研究笔记 secret-scan 关键发现 2)。
- **L1 (`hooks/secret-guard.sh`, PreToolUse, 按命令文本拦截)**: 服务端配置文件 (Forgejo / Gitea `app.ini`) 不在名单、路径经一次 shell 变量即绕过全部文件名规则 (10CG/aria-plugin#203); 进程表列举能把别的进程命令行里的凭据打进输出, 读取路径拦得住、旁路拦不住 (10CG/Aria#221); 同时两处误拦 (`os.environ` 被 `\.env` 命中、只出长度的 jq 形态) 在把使用者推向 `# guard:ack` (10CG/Aria#221 评论 25898: 「降低假阳性率本身就是在保护那道真闸的有效性」)。

**基线实测** (`python3 baseline_probe.py <aria>` @ aria `268da8f`; 值全部运行时生成, 只看退出码 / 是否告警 / tag 名; 原始输出见 `baseline-evidence.md`):

| 洞 | 基线实测 | SC |
|---|---|---|
| L3 Read 提取失明 | Read 真实信封 2/2 静默; 同一内容经 Bash / Write / 旧合成信封 4/4 检出 | SC-1 / SC-2 |
| L3 JSON 键形 (`token`、`sha1`、大写环境变量键等) | 0/13 检出 | SC-4 |
| L3 INI / env 赋值形 (等号两侧空格、引号、`export`、YAML 冒号) | 0/11 检出; `app.ini` 片段 5 个凭据只检出 JWT 形的 1 个 | SC-5 |
| L3 HTTP 头 / CLI 参数形 (含 10CG/Aria#221 的进程行原形) | 0/7 检出 | SC-6 |
| L3 既有键的占位值误报 (FAKE / PLACEHOLDER / NOT-REAL / `[REDACTED]` / 掩码 / L2 wrapper 占位) | 6/6 误报 | SC-11 |
| L3 一份凭据计两次 (哨兵回灌) | `matches=2` | SC-8 |
| L3 日志无值指纹 | 3/3 无 `fp` 字段 | SC-12 |
| L3 测试套件污染真实日志 | secret-scan 套件每跑一次写 33 行; secret-guard 套件写 12 条 ack 事件 | SC-14 |
| L1 `app.ini` 读取 (Bash 面 / Read·Edit 面) | 0/11 拦 / 0/4 拦 | SC-16 / SC-18 |
| L1 路径经 shell 变量间接 | 0/8 拦 | SC-21 |
| L1 进程表列举 (`ps` 完整命令行列 / `pgrep -a` / `top -c` / `/proc/*/cmdline` …) | 0/35 拦 | SC-22 |
| L1 `\.env` 无右边界误拦 (`os.environ` 等) | 5/5 误拦 | SC-23 |
| L1 jq 只出元数据的形态 (`keys_unsorted`、`map_values(length)`) | 5/5 误拦 | SC-24 |

平台事实 (影响 Out of scope 的边界): 本机 Claude Code 2.1.285 二进制里 PostToolUse `hookSpecificOutput` 的 schema 含 `updatedToolOutput` (描述原文「Replaces the tool output before it is sent to the model」), 与 `DEC-20260703-001` 及 `secret-scan.sh:15-23`「架构上不能改写、与版本无关」的前提不符; 但**端到端未验证**。本 Spec 维持「检测 + 告警」, 升级为「检测 + 脱敏」列入「待 owner 复议」第 1 条。

## What Changes

> 编号 W1–W14。每项: 现状 (file:line @ `268da8f`) → 改动 → 设计取舍 → 已知限制。tag 名、日志字段名、文件名等机读 token 一律英文 canonical。文中「测试内 SC-n」指 `hooks/tests/secret-guard.test.sh` 里既有的编号 (来自归档 Spec), 与本 Spec 的 SC-n 无关。

### W1 L3 读取提取修复 (10CG/aria-plugin#154 的前置缺口)

- **现状**: `secret-scan.sh:135-142` 提取链 `.tool_response.output // .tool_response.content // .tool_response.stdout // .tool_result.content // .tool_result.output`; Read 真实形状无顶层 `content` ⇒ 内容为空 ⇒ `:144` 直接 exit 0。现有 Read 用例 (`secret-scan.test.sh:28-32`、`:145-153`) 用合成 `{content}` 形状。
- **改动**: 提取链在 `.tool_response.stdout` 之后加 `.tool_response.file.content`, 其余分支与顺序不动 (`# crlf-ok` 保留: 被扫描的数据体不剥 CR)。新测试一律用真实信封 —— Bash `{stdout, stderr, interrupted, isImage, noOutputExpected}`、Read `{type, file:{filePath, content, numLines, startLine, totalLines}}`、Write `{type, filePath, content, structuredPatch, originalFile, userModified}`。
- **设计取舍**: **选 A** 只加 `file.content` 一个分支: 最小、可证伪 (回退即 SC-1 转红)。不选 B 研究原型的「主体 + `stderr` + `structuredPatch` / `newString` + 字符串形」全量拼接: 真实 Bash 形状里 `stderr` 只装 harness 提示 (命令自身 stderr 已并入 stdout, 研究笔记 163/163 样本同形), 拼接只增噪声; 字符串形 `tool_response` 会不会到达 PostToolUse 未证实。不选 C 按 `tool_name` 分派提取: `//` 取首个非 null 已自然区分, 多一层分支无收益。
- **已知限制**: Edit / MultiEdit 结果不扫 (理由见 Out of scope); 字符串形 `tool_response` 不扫。两者以 KNOWN-LIMIT 钉住现状 (SC-3)。

### W2 L3 通用键形模式 (加法式: 6 个新 tag, 既有 31 条模式的正则与顺序不动)

- **现状**: `secret-scan.sh:152-231` 共 31 条模式 + PEM 预扫。通用键形只有两条: `env-line-secret-keyword` (`:224`, 要求行首、`=` 两侧零空白、无引号、无 `export`、仅大写键) 与 `json-secret-field` (`:227`, 10 个小写键, 无 `token` / `sha1`)。HTTP 头只有 `Bearer` (`:215`) 与 `X-API-Key` (`:218`)。
- **改动**: 在 `json-secret-field` 之后、`bcrypt-hash` 之前新增:
  1. `json-credential-field` —— JSON 键属封闭名表, 值 `"[^"]{16,}"`。名表 17 个名字干: `token` `sha1` `auth_token` `api_token` `bearer_token` `session_token` `registration_token` `jwt_secret` `secret_key` `api_key` `access_token` `refresh_token` `client_secret` `private_key` `secret` `password` `passwd`; 每个允许 snake / camel / Pascal 与连写拼写 (如 `auth_token` / `authToken` / `AuthToken` / `authtoken`)。与既有键重叠的小写 snake 拼写由排在前面的 `json-secret-field` 先消费, 不重复计数 (SC-7)。
  2. `json-env-secret-key` —— JSON 键是大写环境变量名且含 `SECRET|PASSWORD|PASSWD|TOKEN|API_KEY|APIKEY|PRIVATE_KEY|WEBHOOK|ENCRYPTION_KEY|ACCESS_KEY` (Nomad / compose 的 `Env` 映射), 值 ≥16。
  3. `kv-secret-assign` —— INI / env / YAML 赋值: 左侧为行首或非词字符, 可选 `export`, 大写键含同一关键字集, `=` 或 `:` 两侧可有空白, 值可带一层单 / 双引号, 值字符类 `[A-Za-z0-9+/=._~-]` 连续 ≥16。
  4. `auth-header-token` —— `Authorization: token <值>` 与 `Authorization: Basic <值>` (首字母大小写两可), 值 ≥16。
  5. `cf-access-client-secret` —— `CF-Access-Client-Secret: <值>`, 值 ≥16。
  6. `cli-secret-flag` —— 以 `token|password|passwd|secret|api-key|apikey|access-key` 结尾的 `-` / `--` 参数名用 `=` 连写值 (如 `--token=<值>`、`--client-secret=<值>`), 值 ≥16。

  6 个新 tag 都过分类器: W3 白名单 + **熵下限** (值须含小写 / 大写 / 数字三类中至少两类, 且不是「以 `/`、`~/`、`./`、`../` 开头、首段为小写目录名」的路径形)。每个 tag 最多分类 200 个 span, 超出部分不分类照计 (fail-closed)。新模式一律线性 ERE (`grep -E` 与 `sed -E` 通用), 不引入 perl 或回溯; bash 3.2 可跑 (不用 `declare -A` / `mapfile` / `readarray`, SC-32)。
- **设计取舍**:
  - 键表: **选 A** 封闭名表 + 拼写变体。不选 B「任意含 `token` 的键」: 分页游标 `next_page_token` 等会成误报 (SC-9 9j 钉住)。不选 C 只加 10CG/aria-plugin#154 原文的 `token` / `sha1`: 漏研究矩阵里的 `registration_token` / `jwt_secret` / `auth_token` 与首字母大写键 (矩阵 JX1 / JX2 / JX4 / JX3 期望告警)。
  - 大小写: **选 A** 纳入 camel / Pascal (Go 系服务的 JSON 常用 PascalCase)。不选 B 全大小写不敏感: ERE 里要逐字母写 `[Tt][Oo]…` 或先归一化, 复杂度换不到证据。
  - 小写 YAML 键 (`password: <值>`): **选 A** 不纳入, KNOWN-LIMIT (SC-10 10d)。依据: 研究普查最大的误报来源正是小写赋值族 (原始命中 24 个文件), 名字形 / 路径形值无法用正则消除。不选 B 纳入并提高熵下限: 普查显示仍挡不住大小写混合的标识符值。
  - 值长下限: **选 A** 统一 16 (研究矩阵全部正例 ≥20; 机器生成凭据的常见下限)。不选 B 沿用既有 `json-secret-field` 的 8: 误报面更大 (短标识符)。
  - CLI 参数: **选 A** 只认 `=` 连写。不选 B 空格分隔 `--token <值>`: 下一个词可能是子命令或文件名, 无语料证据支撑精度 (KNOWN-LIMIT SC-10 10e)。
  - 熵下限形式: **选 A**「至少两类 + 非路径形」(研究实测 30 trials 零 FLAKY)。不选 B「必须含数字」: 研究实测 20 位字母数字约 3% 无数字而漏。不选 C Shannon 熵阈值: bash 3.2 下计算昂贵, 对 16–40 字符的值不稳定。
- **已知限制** (漏报类成文并以 KNOWN-LIMIT 钉住, SC-10): 单字符类随机值 (全小写 / 全数字 / 全大写); 值短于 16; 小写 YAML 键; CLI 空格分隔; 封闭表外的 PascalCase 键 (如 AWS 的 `SecretAccessKey`)。已知误报类 (成文, 不钉测试): 16 字符以上、含两类字符的名字形值 (例如大小写混合的类名) 会告警; 文档里自述「非真实」的逼真示例值同样会告警 (研究普查例: aria-orchestrator 的 t2-2 evidence)。

### W3 L3 误报白名单 (按值前缀判定)

- **现状**: 全文无白名单。既有 `json-secret-field` 对占位 / 掩码值 6/6 告警 (SC-11 11m–11r); L2 wrapper 对 `token` / `sha1` / `client_secret` / `secret` 四键输出 `[REDACTED-BY-WRAPPER len=N]` 占位串 (precedent 笔记 §6.4), 已在既有键上误报; 给 L3 加 `token` / `sha1` 而不放行这类占位, 每次走 wrapper 的凭据类调用都会恒红。
- **改动**: 对每个被分类的 span 抽出「值」(JSON / 赋值: 分隔符之后去空白与一层引号; 头部: 末词; 参数: `=` 之后), 值以下列任一开头即不计数: `FAKE`、`PLACEHOLDER`、`NOT-REAL` / `NOT_REAL` / `NOTREAL`、`REDACTED`、`[REDACTED`、`<`、`$`、`{{`; 或整个值是 `*` / `x` / `X` 的重复 (掩码)。大小写敏感 (英文大写 canonical, 与 10CG/aria-plugin#154 评论 19339 一致)。被放行的 span 仍被计数哨兵替换, 后序 tag 看不到它。**作用范围** = 6 个新 tag + 既有 `json-secret-field`; 不作用于 provider 前缀类 tag 与其余既有 tag。副作用 (有意): 前序 tag 留下的 `<secret-scan-counted:…>` 哨兵以 `<` 开头, 同一条规则让一份凭据只计一次 (SC-8)。
- **设计取舍**:
  - 判定方式: **选 A**「值以…开头」。不选 B「span 含 FAKE 即跳」: 既有 provider 夹具的 FAKE 在值中间 (`secret-scan.test.sh:102`、`:107`), 会被翻红; 也会放过中段恰含该词的真值 (SC-11 11s 钉住)。
  - 是否延伸到既有 `json-secret-field`: **选 A** 延伸, 两面测试: 6 条既有误报消除 (SC-11 11m–11r, `baseline-failing`) + 真阳性仍检出 (SC-7 7d / 7e、SC-11 11t, 既有 49 用例零回归 SC-29)。不选 B 不延伸: wrapper 占位在 `client_secret` / `secret` 上的既有误报继续恒红。
  - 是否延伸到 `env-line-secret-keyword`: 不选。它的值字符类已排除 `<` `$` `{` `*` `[`, 残余只有字母前缀一类, 没有实测误报证据; 少改一个既有 tag 的语义。
  - 占位写法与本 Spec 自身: 本 Spec、测试与证据文件里的尖括号占位与 `${…}` 由 `<` / `$` 规则覆盖; SC-15 15e / 15f 钉住「本 Spec 与探针的文本被扫描时静默」。
- **已知限制**: 以白名单词开头的真凭据会被放过 (须人为构造); 小写 `fake_` 不在白名单。

### W4 L3 日志留痕: 值指纹 (新功能, 不是「补断言」)

- **现状**: `secret-scan.sh:355-361` 日志 8 个 TSV 字段 (时间 / USER / PWD / `SCAN-DETECT` / tool / matches / breakdown / size), 既无值也无哈希。10CG/aria-plugin#154 评论 19339「若现行为已如此则只加断言」的前提不成立。
- **改动**: 追加第 9 字段 `fp=`: 对每个被计数的值 (键形 tag 取分隔符之后的值, 其余 tag 取整个 span) 按出现序最多记 10 项, 逗号分隔。每项: 值长 ≥16 → `sha256(值)` 的 hex 前 8 位; 值长 <16 → `L<长度>` (不记哈希); `sha256sum` 与 `shasum -a 256` 都取不到 → `-` (fail-soft, 日志照写)。值与片段不进日志、stdout、stderr (SC-12 12d–12f)。
- **设计取舍**: **选 A** 16 字符门槛 + 短值只记长度: 8 位无盐前缀可被离线字典确认低熵口令, 16 字符以上的机器生成值没有这个风险。不选 B 全部记 8 位 (研究原型): 对短口令构成确认预言机。不选 C 加盐 / HMAC: 失去与 `.aria/pat-inventory.yaml` 台账 (`fingerprint_algo: sha256-hex-prefix-8`) 的可比性, 且盐本身要安全存放。不选 D 另起 `credential-tripwire.log` (10CG/aria-plugin#154 原草案): 该日志仓内零读取方 (研究笔记 secret-scan §1.7), 追加字段零兼容负担, 新文件徒增维护面。口径对齐: 算法同 pat-inventory; fail-soft 同 `secret-guard.sh:624` 的 `${hash:-unknown}` 先例。
- **已知限制**: 日志文件权限沿用默认 umask (既有); 人为选取的 16 字符以上低熵口令仍可被字典确认。

### W5 L3 告警文案: 只加描述性信息

- **现状**: `secret-scan.sh:367` 的 additionalContext 只有计数; 收到告警的一方要离线复现才知道是哪类命中 (研究笔记 secret-scan §1.6)。
- **改动**: 在 `in tool output` 与 ` — treat as already-leaked` 之间插入 ` (tags: <tag>=<n> …; source: <tool_name>[ <file_path>])`。tag 串复用 systemMessage 已有的 breakdown; `file_path` 取 `tool_input.file_path`, 只对 Read 与 Write 输出 (取值剥 CR)。其余字节 —— 含处方句「treat as already-leaked; do NOT repeat …; recommend rotating …」与括号说明 —— 与基线逐字节一致 (SC-13 13d); systemMessage 格式、stdout 键集、exit 0 不变 (SC-13 13e / 13f)。
- **设计取舍**: **选 A** 只加描述性事实, Rule #6 可按描述性判 (见 rule6_note)。不选 B 10CG/aria-plugin#154 原稿的「疑似, 若为 fixture 请说明」「轮换放最前」: 属处方性改写; 且该 issue 评论 19339 已确认「措辞把轮换放最前 / 不 block」现行已满足。不选 C Bash 也附命令摘要: 命令文本可能含值, 需要再做一轮脱敏。
- **与决策单第 2 项的关系**: 第 2 项「不逐条提示轮换」针对已知的四枚待轮换凭据 (10CG/aria-plugin#203 / 10CG/Aria#221 / 10CG/Aria#170 / 10CG/Aria#136) 的处理节奏; L3 对**新检出事件**的标准处置 (按已泄露处理、建议轮换) 不变, 本 Spec 不改那句话, 也不产出任何轮换清单。

### W6 测试卫生

- **现状**: 两个套件都不设 `HOME`。基线每跑一次 `secret-scan.test.sh` 向外层 `~/.claude/logs/secret-scan.log` 追加 33 行夹具事件, `secret-guard.test.sh` 向 `guard-bypass.log` 追加 12 条 ack 事件 (SC-14)。`secret-scan.test.sh:93-123` 的检测夹具是字面量。
- **改动**: 两个套件开头把 `HOME` 指向自建临时目录并在退出时清理; 新夹具一律运行时拼装 (随机生成或字符串拼接), 源码不出现凭据形状字面量 (GitHub 镜像的 push protection 只放行这两个测试文件, `aria/.github/secret_scanning.yml:18-22`)。
- **设计取舍**: **选 A** 在套件里隔离。不选 B 让 hook 识别测试环境后不写日志: 生产代码为测试开后门。
- **已知限制**: `host-docker-logout-guard.test.sh` 同样写外层 `guard-bypass.log` (本 Spec 实跑观察到), 不在本 Spec 文件域 → 列入建议开单。

### W7 夹具静默 (W1 的连带问题)

- **现状**: W1 生效后, 读 `hooks/tests/secret-scan.test.sh` 会持续注入「按已泄露处理」(研究笔记 secret-scan §5.3「修好 Read 提取会制造新的红」); 把该文件文本当 Bash 输出扫, 基线即命中 33 处 (SC-15 15a)。WP-A 实施期会反复读写这个文件。
- **改动**: 把该文件现有字面夹具改为运行时拼装 (如把前缀拆成两段字符串拼接), 每条断言的输入值与期望 tag 不变; hook 侧**不加**任何按路径的豁免。
- **设计取舍**: **选 A** 源头拼装: hook 零新增逻辑, 没有任何路径被豁免, 也就不存在「真实泄露只进日志」的盲区; 可证伪: 文件文本扫描转为静默 (SC-15 15a), 同时既有断言照过 (SC-29)。不选 B 按路径的「只记日志、不注入 additionalContext」清单: 要新逻辑与清单维护; 清单内若真有泄露, 模型不知情 (盲区); 清单路径在采用方项目里没有意义。不选 C 不处理: 实施期每次读测试文件都收到恒红告警, 零信息。
- **已知限制**: 其它含逼真示例值的文件 (如 aria-orchestrator 的测试夹具) 在 W1 后被 Read 时会告警, 与今天 `cat` 它们时一致, 不是新增面。

### W8 L1 服务端配置文件 (Forgejo / Gitea `app.ini`)

- **现状**: Bash 面 `risky_patterns` (`secret-guard.sh:736-1009`, 145 行) 与 Read/Edit 面正则 (`:641`) 都没有服务端配置文件 (SC-16 0/11、SC-18 0/4)。credit 收紧 (tight) 只认 claude 配置 (`:405-408`)。既有读取器组没有左边界 (`chmod` 里含 `od`)。
- **改动**:
  1. 名字组单一定义为变量、两处消费: `(forgejo|gitea)` 之后同一路径内的任意非空白非引号字符再接 `app.ini` (覆盖 `/etc/forgejo/app.ini`、`/etc/gitea/app.ini`、`/var/lib/forgejo/custom/conf/app.ini`、容器内 `/data/gitea/conf/app.ini`), 以及 `custom/conf/app.ini`。
  2. Bash 面新增一行: 打印型读取器组 (claude-config 行 `:815` 的 13 个 + `nl tac rev sort uniq cut paste diff cmp comm xxd od hexdump base64 column fold`), 自带左边界 `(^|[^[:alnum:]_.-])`; 名字前用 `_SG_PP_NAME` 前置白名单 (10CG/Aria#179 体例)。python3 -c / node -e 源组 (`:893` / `:894`) 追加同一名字组。
  3. Read/Edit 面 `:641` 追加同一名字组 (对小写化后的路径)。
  4. tight 检测 (`:405-408`) 并入该名字组: 锚定 grep / `grep -v` / sed / cut / awk 不再算 credit (否则 `cat …/app.ini | grep '^JWT_SECRET'` 被当过滤放行并泄露, SC-16 16f); `wc` / `sha*sum` / `>/dev/null` / jq 名字面 credit 保留 (SC-17 17h)。
- **设计取舍**: **选 A** 只做 `app.ini` 族 (有事故证据)。不选 B 同批纳入 `grafana.ini`、`/etc/{nomad,consul,vault}.d/`、`/etc/pve/priv/`、`/etc/shadow` 与经典凭据点文件: 研究用的 2700 条 docs 命令语料里只有 1 条触及这些名字 (`find /etc/nomad.d …`, 未误拦), 不足以作「语料零误报」实证 → 列入建议开单 (附研究笔记 secret-guard §2 服务端配置一节的候选清单)。不选 C 裸名 `app.ini`: 任何应用都有 (SC-17 17e / 17f 钉住 `/opt/myapp/app.ini`、`php.ini` 放行)。
- **已知限制**: `cd /etc/forgejo && cat app.ini` 这类相对名 (SC-21 21r); 引号内 `|` 让 `[^|]*` 行失明 (既有缺陷, 建议开单); `sed -i` 编辑 `app.ini` 同样被拦 (与 `sed -i ~/.bashrc` 一致, 走 ack); Edit 工具被拦 (走 `SECRET_GUARD_ACK_PATH` nonce)。

### W9 L1 项目级扩展入口 `.aria/secret-guard.paths`

- **现状**: 两个 hook 都不读任何项目文件, 也不解析 stdin `cwd` 与 `CLAUDE_PROJECT_DIR` (`secret-guard.sh:564` 只抽 4 个字段)。
- **改动**:
  - **位置**: `<项目根>/.aria/secret-guard.paths`。项目根 = 非空的 `CLAUDE_PROJECT_DIR`; 否则 stdin 的 `cwd` (单独一次 jq 取值并剥 CR; 不改 `:564` 的 4 字段 NUL 抽取与 `== 4` 守卫)。
  - **格式**: 一行一个**字面子串** (不是正则); `#` 起首为注释, 空行忽略, 剥行尾 CR 与首尾空白; 长度 4–200 且含字母或数字的行才生效, 其余行跳过。
  - **语义**: 只增不减 —— 不能移除或放宽任何内建规则 (写一行 `!.env` 也只是一条字面子串, SC-19 19n)。两面生效: Bash 面 = 打印型读取器 (与 W8 同组、自带左边界) 出现在该子串之前 → 按 tight credit 判; Read/Edit 面 = `file_path` 含该子串 → 拦 (同一 `SECRET_GUARD_ACK_PATH` nonce 逃生口)。变量间接 (W10) 同样作用于扩展条目 (SC-19 19i)。拒绝时复用同一份 BLOCKED 文案 (SC-25 25f), 不为扩展另写文案。
  - **失败处理 = 扩展失败只丢扩展**: 文件缺失 / 不是普通文件 / 不可读 / 超过 32 KiB / 含 NUL 字节 / 有效条目超过 200 → 整个扩展不生效, 内建名单照常 (SC-20 两面各 6 行); 从不因扩展问题 exit 2 (10CG/Aria#154 会话死锁教训; `handoff-location-guard.sh` 的 fail-open 先例)。这**不是**整体 fail-open: 内建规则的判定与其 fail-closed 路径不受扩展影响。
- **设计取舍**:
  - 宿主: **选 A** `.aria/` 下纯文本清单 (仓内先例 `bare-issue-ref-allowlist.txt`、`linked-issue-field-grandfathered.txt`)。不选 B `.aria/config.json` 新键: 撞 10CG/Aria#199 的 `completeness_gate` 守卫面与 `config-template-key-currency` 检查, 还要登记 `config.template.json`、`DEFAULTS.json` 与 config-loader (Skill ⇒ Rule #6 面扩大)。不选 C `.claude/settings.json` 的 env 注入: 未验证 env 块是否传给 hook, 且只有人能维护。
  - 条目语义: **选 A** 字面子串 (杜绝正则写错导致的静默不匹配; SC-19 19j / 19k 钉住「`.` 是字面」)。不选 B ERE。
  - 项目根回落: **选 A** stdin `cwd` (hook 契约字段)。不选 B hook 进程的 `$PWD` (研究原型): Bash 工具 `cd` 之后与项目根无关。
  - 超限处理: **选 A** 整体忽略 (一条规则, 可预测)。不选 B 截断到前 200 条 / 前 32 KiB (研究原型): 部分生效的清单更难排查。
- **已知限制**: 扩展失效是静默的 (PreToolUse exit 0 时 stderr 既不给模型也不给用户) → 建议开单: aria-doctor 增加一项校验; 采用方的 AI 也能编辑这个文件 (威胁模型是防意外, 同 hook 头注释); `cwd` 回落在 `cd` 之后可能找不到文件 (只在 `CLAUDE_PROJECT_DIR` 缺失时才会用到)。

### W10 L1 路径经 shell 变量间接 (部分修复)

- **现状**: 路径与读取器分落两段 (`f=…; cat "$f"`), 逐段评估 (`:1088-1102`) 看不到; 即便降级成整串, 所有行都要求「读取器在前、名字在后」(SC-21 0/8)。10CG/aria-plugin#203 自己写明它的第 2 类「在命令侧基本堵不住」, 设计意图就是交给 L3。
- **改动**: 在整条命令上收集字面赋值 (`NAME=值`, 含 `export/declare/local/readonly/typeset` 前缀、单双引号值、`for NAME in 列表`、单层链式 `d=…; f=$d/…`; 上限 16 个赋值、每变量 8 次替换), 对每个含 `$NAME` / `${NAME}` / `\$NAME` 的段 (或降级时的整条命令) **额外**判一次替换后的副本。原判定不变, 只可能新增拦截。新函数放在测试 source 闸门 (`:491-493`) 之上; 替换串一律加引号 (bash 5.2 的 `patsub_replacement` 下, 未加引号的 `&` 会被替换成匹配文本)。
- **设计取舍**: **选 A** 字面赋值展开 (研究原型: 24 条泄露形态 24/24 拦, 22 条正常用法 0 误报, 2700 条 docs 语料 0 新增拦截)。不选 B「给敏感路径赋值就拦」: `export KUBECONFIG=~/.kube/config` 这类惯用法误报面大 (SC-21 21j 钉住放行)。不选 C 整串共现: 精度最差。
- **已知限制** (KNOWN-LIMIT, SC-21 21n–21u, 各钉现状放行; 对外表述为「部分覆盖」, 不宣称根治): 数组赋值、`read … <<<`、引号拼接路径、`"$d"/app.ini` 引号夹在路径中间、`cd … && cat 相对名`、glob、`set --` 位置参数、`$(printf …)` 拼路径、跨两次工具调用的变量 (Bash 工具不保留 shell 状态)。这些交给 L3 (W1 + W2 在输出侧兜底: 2026-09-26 事故泄露的那一行正是 SC-5 5a 的形态)。同一架构面的在案 issue: 10CG/aria-plugin#138 (跨段 fail-open)、10CG/aria-plugin#140 (`ssh '…'` / `sh -c '…'` 外壳)、10CG/aria-plugin#142 (`$(…)` / heredoc 内部)。

### W11 L1 进程表列举

- **现状**: 只拦 `/proc/(self|数字)/(environ|status|cmdline)` (`secret-guard.sh:930-933`); `ps` 完整命令行列、`pgrep -a`、`top -c`、`pstree -a`、`docker top` 全放行 (SC-22 0/35)。L3 对 `Authorization: token …` 与 `CF-Access-Client-Secret` 零告警 (SC-6 基线 0/7) ⇒ 今天 L1 是唯一预防层。
- **改动**: 新增进程表行 (命令位置锚定, 沿用 `:867-877` 的前缀写法), 拦暴露 argv 或 environ 的形态:
  - `ps`: 任意 BSD 选项簇 (不带 `-`, 如 `aux`、`e`、`eww`)、SysV `-f` / `-F` 簇、`-o` / `--format` 列表含 `args|cmd|command`;
  - `pgrep -a` / `--list-full`; `pstree -a` / `--arguments`; `top -c`; `docker top`; `docker ps --no-trunc`;
  - launcher 包裹 (`sudo doas nice timeout nohup stdbuf env time setsid ionice watch command exec`) 对以上全部生效 (SC-22 22n `sudo pgrep -af …`); 远程与外壳包裹中出现的以上形态 —— `ssh`、`docker|podman|kubectl|lxc exec`、`nomad alloc exec`、`pct exec`、`sh|bash -c '…'`、`watch '…'`;
  - `/proc` 行放宽: pid 位置接受任意 token (`*`、`$pid`、`${pid}`、`$(…)`), 读取器补 `xargs sed grep egrep fgrep rg cut paste nl sort base64 cp dd` (SC-22 22F–22I);
  - credit 用 tight: `ps -ef | grep -v grep` 打印的仍是整行命令, 行级过滤不算 (SC-22 22q–22s); `wc` 与 `>/dev/null` 保留 (22aa / 22ab);
  - 放行只出 pid 或进程名的形态: `ps -e`、`ps -eo pid,comm`、`ps -p N`、`pgrep PAT` / `-f` / `-l` / `-fl` (Linux)、`pstree -p`、不带 `-c` 的 `top -b`、`docker ps` (SC-22 放行守卫 19 行)。
- **处置**: 拒绝 (exit 2), 与现有 hook 一致, 复用同一份 BLOCKED 文案 (SC-25 25d)。
- **设计取舍**: **选 A** 拒绝。不选 B PreToolUse `updatedInput` 改写 (如把 `ps aux` 改成 `ps -eo pid,comm`): 多个 PreToolUse hook 同时改写时「最后完成者生效」(cc-hooks 笔记; 本仓 Bash matcher 下已有两个 hook 并行), 静默改写用户命令违背意图, 且现 hook 没有 JSON 输出路径 (只有 exit 2 + stderr)。不选 C `permissionDecision: ask`: 现 hook 没有 JSON 通道, 且把判断转嫁给用户逐次确认, 与 ack 疲劳同形。
- **同族的进程环境读取**: 纳入 BSD `ps e` / `eww` (输出 environ) 与 `/proc/*/environ` (同一组行); 不纳入 `docker inspect <容器>` 全量 JSON (含 `.Config.Env`; 基线只拦带 `--format …Config.Env` 的)、`journalctl`、`nomad job inspect` —— 研究未评估其误报面, 列 KNOWN-LIMIT (22ak / 22al) 并建议开单。
- **已知限制**: `systemctl status` 放行 —— 暴露已验证 (研究活体), 但它是最常用的健康检查, 误报代价高; W2 之后其输出里的 `Authorization: token …` / `CF-Access-Client-Secret` 由 L3 检出 (SC-6 6g 同形), KNOWN-LIMIT 22ah / 22ai。`cat /proc/N/status` 被拦是既有轻度误报 (不含 argv / environ), 本 Spec 不动 (22aj)。macOS 的 `pgrep -fl` 会输出完整命令行 (平台差异, 未实测), 本 Spec 按 Linux 语义放行。`ps axo pid,comm` 因 BSD 选项簇被拦 (tight 侧误报, 接受)。

### W12 L1 两处误拦

**`\.env` 右边界**

- **现状**: `secret-guard.sh:893` (python3 -c)、`:894` (node -e)、`:974` (lua -e) 源组里的 `\.env` 无右边界, `os.environ` / `os.environb` / `cfg.environment` 被拦 (SC-23 23a–23e)。
- **改动**: 只改这三行, 写成 `\.env(rc)?([^A-Za-z0-9_]|$)`。
- **设计取舍**: **选 A** 只改三行并带 `(rc)?`。不选 B 10CG/Aria#221 评论 25898 建议的全局加边界: 研究实测套到全部 39 行时 465 条探针里 108 条由拦变放, 含 20 条 `.envrc` 漏拦与 `cp .env /dev/stdout`、`scp .env user@h:` 这类「边界吞掉后面必需的空白」造成的真漏 (SC-23 23l–23q 钉住仍拦)。边界字符类: **选 A** `[^A-Za-z0-9_]` (下划线算词内字符), fail 方向 = `.env_prod` 这类下划线后缀名经这三种解释器读取时由拦变放 (SC-23 23f, 计入 Impact 新放行); 与既有 `cat` 行 `:782` 的 `\b` 同语义 —— 基线 `cat .env_prod` 本就放行 (SC-23 23s)。不选 B「下划线也算边界」`[^A-Za-z0-9]`: `x.env_file` 这类属性名会继续被拦。
- **已知限制**: `process.env.X` 仍被拦 (`.env` 后面是 `.`, 加边界救不了, 要靠预归一化; 不纳入, KNOWN-LIMIT 23r)。

**jq 只出元数据的形态**

- **现状**: credit 词表 (`:427`) 已放行 `length` 与 `.X | length` —— 10CG/Aria#221 评论 25898 这一部分已过时 (SC-24 24l / 24m 基线即放行); 真正缺的是 `keys_unsorted` 与 `map_values(length)` (SC-24 24a–24e 基线 5/5 拦)。
- **改动**: 新增一条**锚定语法** credit: jq 程序必须带引号, 前缀只允许一个简单点路径加 `|`, 词后紧跟闭合引号, 词 ∈ {`keys_unsorted`, `map_values(length)`}; 不进 `:427` 的宽松词表。tight 模式下同样有效 (24e)。`keys[]` 保持拦截 (负向锚 `secret-guard.test.sh:841` 与 SOT 明文, 24f)。
- **设计取舍**: **选 A** 锚定写法。不选 B 把 `keys_unsorted` 加进 `:427` 词表 (研究原型 F1): 该词表「词后只要是 `|` 就算、之后不受约束」, 本 Spec 实测研究原型对 `jq 'keys_unsorted | $ENV'` 放行 (会打印 jq 进程环境), 锚定写法仍拦 (SC-24 24h 钉住)。不选 C 纳入 `map(.name)` / `map(.key)`: 依赖「name / key 字段不是密」的数据假设 (KNOWN-LIMIT 24o)。
- **已知限制**: 既有洞 `jq '. as $d | keys | map($d[.])'` 基线放行 —— 本 Spec 不扩大也不修 (KNOWN-LIMIT 24p, 建议开单)。

### W13 拒绝文案零改动, 条款落 SOT

- **现状**: 10CG/Aria#221 建议在拒绝文案加一句「凭据不要放命令行参数, 改用 env / `--config` / stdin」。BLOCKED heredoc (`secret-guard.sh:1043-1071`) 被全部 145 行共用; 其处方性行自 2026-05-23 初版起未改过 (precedent 笔记 §1.2); `2026-08-02-secret-guard-nomad-var-put-echo` 的 Rule #6 可证伪锚点正是「heredoc 零改动」, 并明确拒绝过往共享文案里加专属内容 (会污染无关拦截), 按 pattern 给定向建议则转为 10CG/aria-plugin#132 (未初始化的 `$pattern_hint` 在 `set -u` 下会让全部 BLOCKED 文案崩溃)。
- **改动**: hook 文案零改动 —— SC-25: 三种既有 BLOCKED 文本归一化后与基线逐字节一致, 新增的进程表 / `app.ini` / 扩展 / Read 拦截复用同一文本。条款写进 `standards/conventions/secret-hygiene.md`: §2.5 加一行进程表列举 (`ps` 完整命令行列 / `pgrep -a` / `top -c` / `/proc/<pid>/cmdline` 与 `environ`); 新增一条「凭据不要放命令行参数, 改用 env / `--config` / stdin」正例 (SC-26)。示例须逐工具实跑: `curl -K -` 从 stdin 读配置 (已实跑, curl 7.88.1: 从 stdin 配置读到 URL 后连接被拒 exit 7; 对照组无配置时 exit 2 `no URL specified`) 与 `curl -H @<文件>` (已实跑, 参数被接受); 其它工具的 env 写法 (如 `NOMAD_TOKEN`、`VAULT_TOKEN`) 在 B.2 实跑或以 `--help` 原文为据, 做不到就不写。
- **设计取舍**: 三个选项见「待 owner 复议」第 2 条: 选项 A 不改文案、只落 SOT (本 Spec 推荐) / 选项 B 全局共享文案加一句 / 选项 C 先解 10CG/aria-plugin#132 再做按 pattern 的定向提示。
- **已知限制**: 被拦的当下 AI 看不到这条建议 (它只在 SOT 里)。

### W14 测试元耦合与同步

- **测试内 SC-13 头注释计数**: `secret-guard.test.sh:11` (`Coverage: 599 cases (593 without zsh)`, 断言 `:2018-2030`) 与 `secret-hygiene.md:23` / `:287` / `:319` 三处同步为实跑数 (权威值 = 带 git 历史的真 checkout 实跑, SC-30)。
- **测试内 SC-19 census**: `family_count` 硬编码 61 (`secret-guard.test.sh:1620` / `:1622`) 改为 census 实测值; 每个新增或改名的跨段族补 `# family='<精确 key>'` 探针 (10CG/aria-plugin#153 57→60、10CG/Aria#179 60→61 先例); 改 `/proc` 读取器行开头的分组会让该族 key 改名; 新行不得整行只由 `"${VAR}"` 组成 (census 在不带前置变量的 bash 里求值, 这类行是空串、在测试内 SC-19 里隐形; SC-31 31c)。
- **性能预算**: 测试内 SC-8 五档每次调用 ≤ max(100ms, 改前 × 1.5) —— 既有闸门, owner 2026-08-24 裁定, 不改阈值、口径、档位 (SC-30)。研究原型比基线慢约 10–25%, 负载下最坏档 46.6–75.8ms, 仍在天花板内但余量变小。另设结构预算: `risky_patterns` 静态行 145 → 不超过 150 (SC-31 31a); 变量展开只在「段含 `$` 且收集到赋值」时触发。L3 预算: 180 KB 级稠密 INI 输入单次 ≤ 2.5s (hooks.json `timeout: 5` 的一半; 研究原型实测 1.29s), B.2 实测记录。
- **其它耦合**: 测试内 SC-20 注入自测依赖的两段文本 (`_sg_compute_credit` 里 `wc` 那段、`local nl=$'\n'`) 逐字节不变; hook 源码不出现 `(?:` (测试内 SC-16); 用例名不重复 (测试内 SC-17); 新增 jq 取值点带 CR 剥离或 `# crlf-ok` (jq-crlf-guard, SC-29 29g); 新辅助函数放在 source 闸门之上, 并跑一次测试内 SC-20 风格的未绑定变量注入自测 (新代码里任何未绑定变量都会让**所有** Bash 命令 fail-closed)。
- **secret-scan 计数**: `secret-scan.test.sh` 新增头注释 `Coverage: K cases` 与测试内 SC-13 同款的自检 (本 Spec 补; 现在 `secret-hygiene.md:288` 的 49 没有任何机械断言; SC-27 27b / 27c)。
- **陈旧 / 悬空表述** (SC-28): `secret-guard.sh:21-23`「Phase 2 would add PostToolUse hook … + redacts」与 `:62` 悬空的 `docs/operations/secret-rotation-runbook.md` 引用 (改指 `secret-hygiene.md`); `secret-scan.sh:33-34` 的 `49 known bypass classes` / `~15 secret-shape patterns`、`:52` 不存在的 argon2、`:72-80` hook contract 里的旧 Read 形状、`:64`「base64 / hex 无前缀」非目标声明 (改为「无前缀且无凭据键名」); `secret-hygiene.md` §5.1 把 secret-guard 称作 Write/MultiEdit blocker (`secret-guard.sh:698-700` 对二者直接 exit 0); `aria/VERSION:164` 的「output REDACT」; 两个 hook 的头注释记本 change-id。

## Out of scope

- **凭据轮换** (决策单第 2 项): 本 Spec 不产出轮换清单、不涉及任何具体凭据、不逐条提示轮换。
- **WP-B** (10CG/Aria#223 + 10CG/aria-plugin#207) 与 **10CG/Aria#199** 本身。
- **L3 升级为「检测 + 脱敏」(`updatedToolOutput`)**: 产品级 (模型将看不到被脱敏的正文)、端到端未验证、要推翻 `DEC-20260703-001`。本 Spec 保持检测 + 告警, 只保证检测核心 (提取 + tag + 分类器) 日后可被脱敏模式复用; 选项见「待 owner 复议」第 1 条。在 PostToolUse 无法改写内置工具输出这一平台前提下的「撤回」能力 (值已进上下文) 不在范围。与之相关的既有陈述 (`secret-scan.sh:15-23`、README 两语种、`secret-hygiene.md` §5.2 等「cannot redact」) 本 Spec 不改, 随第 1 条的复议结论统一订正。
- **Edit / MultiEdit 结果扫描**: Edit 的结果给模型的只是一句成功提示, 不回显内容 (研究笔记 secret-scan §1.2), 值本来就在模型自己写的 `tool_input` 里, 不构成「经工具输出进入模型上下文」的泄露; MultiEdit 真实形状 0 样本。
- **既有缺陷** (研究新发现, 非三个 issue 所诉) 与 matcher 缺 Grep / PowerShell、飞书 webhook URL / Nomad-Consul `SecretID` 等未覆盖形状: 见「待 owner 复议」第 7 条建议开单清单。
- **aria-doctor 对扩展文件的校验** (W9 已知限制): 属 Skill 改动, 另开单。

## Success Criteria

> **类别** (机读枚举, 英文 canonical): `baseline-failing` = 基线不符、目标相符 (RED → GREEN); `reverse-guard` = 基线与目标都保持拦截 / 检出 / 一致 (防回退); `allow-guard` = 基线与目标都保持放行 / 静默 (误报守卫); `known-limit` = 钉住已知不覆盖的现状, **该行转红 = 已收口, 须同步更新本 SC 与对应「已知限制」**; `zero-regression` = 全量既有测试, 只承担「无外溢」, 不作功能正确的证据; `doc-sync` = 文档同步。
>
> **判定命令**: 全部由同目录 `baseline_probe.py` 执行 (`python3 baseline_probe.py <aria 仓路径>`; SC-30 除外)。L3 行: 把「输入形态」按注明的信封 (默认 Bash 真实信封) 构造成 JSON, 经 stdin 喂 `bash hooks/secret-scan.sh`, 判据 = exit 0 + stdout JSON 的 `additionalContext` 是否非空 + `systemMessage` breakdown 的 tag 与计数**恰好**等于期望。L1 行: `{"tool_name":"Bash","tool_input":{"command":<命令>}}` (Read / Edit 行用 `file_path`) 经 stdin 喂 `bash hooks/secret-guard.sh`, 判据 = 退出码。像凭据的值全部运行时生成; 每个用例的输入形态、期望、基线实得逐行见 `baseline-evidence.md` (共 326 行, 其中 SC-30 一行不执行)。
>
> **基线形态自检**: 探针在基线上的输出必须是「`baseline-failing` 与 `doc-sync` 行全部 `no`、其余类别全部 `yes`」, 实跑成立 (证据末尾两行); 目标态必须是「全部行 `yes`」。

**L3 (`secret-scan.sh`)**

- **SC-1** (`baseline-failing` ×2, W1): Read 真实信封, 内容为 `AWS_ACCESS_KEY_ID=<AKIA+16>` / json:client_secret=<32 alnum> → 期望检出 `aws-access-key-id=1` / `json-secret-field=1`。**基线 2/2 静默**。怎么会红: 提取链没加 `file.content` 或加错层级。
- **SC-2** (`reverse-guard` ×4, W1): 同内容经 Read 旧合成信封 / Bash 真实信封 / Bash 旧 `{output}` 信封 / Write 真实信封 → 仍检出 `aws-access-key-id=1`。**基线 4/4 相符**。怎么会红: 改提取链时破坏既有分支。
- **SC-3** (`known-limit` ×2, W1): Edit 真实信封、字符串形 `tool_response` → 静默。**基线 2/2 相符**。怎么会红: 有人扩了扫描面 (须同步本 SC 与 Out of scope)。
- **SC-4** (`baseline-failing` ×13, W2): json:token=<40 hex> (08-20 事故形) / 同形冒号后带空格 / json:sha1=<40 hex> / 多行美化 / `registration_token` / `jwt_secret` / `auth_token` / 完整 Forgejo 建 PAT 响应 (含 `token_last_eight`, 期望只计 1) / 首字母大写 `Token` / camel `apiKey` / Pascal `ClientSecret` → 期望 `json-credential-field=1`; JSON 里的大写环境变量键 (`Env` 映射的 `JWT_SECRET`、多行 `DB_PASSWORD`) → 期望 `json-env-secret-key=1`。**基线 0/13 (全静默)**。怎么会红: 名表缺项、拼写变体没覆盖、值长门槛写错、`token_last_eight` 被误计。
- **SC-5** (`baseline-failing` ×11, W2): `JWT_SECRET = <44 std-b64>` (10CG/aria-plugin#203 原形) / `<43 b64url>` / `SECRET_KEY = <64>` / `PASSWD = <20>` / `LFS_JWT_SECRET = <43>` / `export API_TOKEN=<32>` / dotenv 双引号 / 单引号 / `export` 加双引号 / 缩进 YAML 冒号形 → 期望 `kv-secret-assign=1`; `app.ini` 片段 (5 个凭据, 其一为 JWT 形) → 期望 `jwt=1 kv-secret-assign=4`, `matches=5`。**基线 0/11** (`app.ini` 片段只检出 `jwt=1`)。怎么会红: 等号两侧空白、引号、`export`、冒号任一形态没覆盖, 或 JWT 值被两个 tag 重复计数。
- **SC-6** (`baseline-failing` ×7, W2): `Authorization: token <40 hex>` / curl 命令回显里的同一头 / `CF-Access-Client-Secret: <64 hex>` / curl 回显的 CF-Access-Client-Id + Secret 头对 (期望只计 Secret) / `Authorization: Basic <b64>` → `auth-header-token=1` 或 `cf-access-client-secret=1`; `--token=<40 hex>` → `cli-secret-flag=1`; 进程表行 (10CG/Aria#221 原形: curl 带 CF 头对与 `Authorization: token`) → `auth-header-token=1 cf-access-client-secret=1`。**基线 0/7**。怎么会红: 头名大小写、值字符类或 Client-Id 被误计。
- **SC-7** (`reverse-guard` ×7, W2): 行首 `JWT_SECRET=<44>` 仍为 `env-line-secret-keyword=1`; `INTERNAL_TOKEN = <JWT>` 仍为 `jwt=1`; `Authorization: Bearer <32>` 仍为 `bearer-token=1`; json:client_secret / json:password 仍为 `json-secret-field=1`; 行首 `DB_PASSWORD=<20>` 仍为 `env-line-secret-keyword=1`; json:token=<gh 前缀 PAT> 仍只计 `github-pat=1`。**基线 7/7 相符**。怎么会红: 新 tag 排序在前抢走既有 span, 或同一值被两个 tag 计数。
- **SC-8** (`baseline-failing` ×1, W3): json:api_key=<anthropic 前缀 key> → 期望 `anthropic-api-key=1`, `matches=1`。**基线 `matches=2`** (哨兵回灌)。怎么会红: 白名单没延伸到 `json-secret-field`, 或 `<` 前缀规则缺失。
- **SC-9** (`allow-guard` ×21, W2): 通用键形在非凭据上静默 —— 尖括号 / `$(…)` / `${…}` 占位、空值、只含键名的 grep 命令、git 提交 sha、`commit.id`、`token_last_eight`、UUID、`next_page_token`、完整 git log、`Authorization: token $VAR`、`--token=$VAR`、`--token-file=<路径>`、路径形值 (三类字符齐全)、单字符类名字形值、`export SECRET_GUARD_ACK_PATH="<路径>"`、散文、镜像 digest、Actions `${{ secrets.X }}`、`--password-stdin`。**基线 21/21 相符**。怎么会红: 熵下限、路径判定、名表封闭性或值字符类任一写宽。
- **SC-10** (`known-limit` ×6, W2): json:token=<40 纯小写>、`JWT_SECRET = <24 纯数字>`、json:token=<12 alnum> (短于 16)、YAML 小写键 `password: <16>`、`--token <40 hex>` (空格分隔)、json:SecretAccessKey=<40> → 静默。**基线 6/6 相符**。怎么会红: 有人覆盖了该类 (须同步更新已知限制)。
- **SC-11** (W3, 两面): 新 tag 放行侧 (`allow-guard` ×12): json:token 的值为 FAKE_ 前缀 / PLACEHOLDER / NOT-REAL- / L2 wrapper 占位 / 尖括号占位 / `${…}` / `{{ … }}` / 16 个 `*`、json:sha1 的 wrapper 占位、赋值形的 FAKE_ 值、`Authorization: token` 的 FAKE 值、`--token=` 的 PLACEHOLDER 值 → 静默 (**基线 12/12 静默**; 但基线静默是因为这些键根本没被覆盖 —— 放行侧只有与 SC-4 / 5 / 6 的同形正例成对才有鉴别力); 既有键误报修复 (`baseline-failing` ×6): json:password / client_secret / api_key 上的 FAKE_、PLACEHOLDER_VALUE、NOT-REAL-、`[REDACTED]`、8 个 `*`、wrapper 占位 → 静默 (**基线 6/6 告警**); 标记不在值首 (`baseline-failing` ×1): json:token=<16 alnum + FAKE + 16 alnum> → 期望 `json-credential-field=1` (**基线静默**); 真阳性仍检出 (`reverse-guard` ×2): json:password=<12 alnum + !> 仍为 `json-secret-field=1`, 正文以 FAKE 开头的 gh 前缀 PAT 仍为 `github-pat=1` (provider tag 不套白名单), **基线 2/2 相符**。怎么会红: 白名单写成「含」而非「以…开头」、延伸到 provider tag、漏掉 wrapper 占位。
- **SC-12** (W4): (`baseline-failing` ×3) json:client_secret=<32> → 日志第 9 字段恰为 `fp=<sha256(值) 前 8 位>`; json:password=<12> → 恰为 `fp=L12` 且日志不含该值的哈希; 在 PATH 里去掉 `sha256sum` 与 `shasum` → 恰为 `fp=-` 且日志照写。**基线 3/3 无 `fp` 字段**。(`reverse-guard` ×3) 同两例加 `app.ini` 片段: 日志恰 1 行, 日志 / stdout / stderr 里没有任何值或值的首末 8 字符片段。**基线 3/3 相符**。怎么会红: 指纹取了整个 span 或加了盐、短值也记了哈希、缺工具时不写日志、值或片段落进任一输出。
- **SC-13** (W5): (`baseline-failing` ×3) additionalContext 含 `(tags: aws-access-key-id=1; source: Read /x/app.ini)` / `(tags: json-secret-field=1; source: Bash)` / `(tags: aws-access-key-id=1; source: Write /x/f.txt)`。**基线: Read 例静默 (读取失明), 另两例告警但无 tag 与来源**。(`reverse-guard` ×3) 处方句逐字节等于基线; systemMessage 格式不变; exit 0 且 stdout 键集恰为 `{hookSpecificOutput{hookEventName, additionalContext}, systemMessage}`、不回显值。**基线 3/3 相符**。怎么会红: 改了处方句、把值或命令写进告警、输出了改写类键。
- **SC-14** (`baseline-failing` ×2, W6): 以外层 HOME 跑 `secret-scan.test.sh` → 外层 `secret-scan.log` 新增 0 行; 跑 `secret-guard.test.sh` → 外层 `guard-bypass.log` 新增 0 条事件。**基线 33 行 / 12 条**。怎么会红: 任一套件没隔离 HOME, 或隔离发生在第一次调用 hook 之后。
- **SC-15** (W7 / W3): 文件文本当 Bash 输出扫 —— `hooks/tests/secret-scan.test.sh` (`baseline-failing`) 期望静默, **基线告警 `matches=33`**; `hooks/tests/secret-guard.test.sh`、`hooks/secret-scan.sh`、`hooks/secret-guard.sh`、本 Spec 的 `proposal.md`、`baseline_probe.py` (`allow-guard` ×5) 期望静默, **基线 5/5 静默**。怎么会红: 夹具没拼装干净; 新模式在 hook 源码、测试源码或本 Spec 的占位写法上误报。

**L1 (`secret-guard.sh`)**

- **SC-16** (`baseline-failing` ×11, W8): `sed -n '1,80p' /etc/forgejo/app.ini`、`cat /etc/gitea/app.ini`、`cat custom/conf/app.ini`、`grep -n JWT_SECRET /etc/forgejo/app.ini`、`cat /data/gitea/conf/app.ini`、`cat /etc/forgejo/app.ini | grep '^JWT_SECRET'` (tight)、`ssh root@pve 'pct exec 101 -- cat /etc/forgejo/app.ini'`、python3 -c 读取、`head -n 40 /var/lib/forgejo/custom/conf/app.ini`、awk 段落区间、`docker exec forgejo cat /data/gitea/conf/app.ini` → exit 2。**基线 0/11 (全 exit 0)**。怎么会红: 名字组漏某一路径形态、读取器组漏某个读取器、tight 没并入。
- **SC-17** (`allow-guard` ×10, W8): `chmod 600 …/app.ini` (左边界)、`ls -l`、`systemctl restart forgejo`、`grep -rn 'app.ini' docs/`、`/opt/myapp/app.ini`、`php.ini`、`git log -- custom/conf/app.ini`、`… | wc -l`、`sha256sum …`、`cp … /tmp/…` → exit 0。**基线 10/10 相符**。怎么会红: 新行缺左边界、名字组退化成裸 `app.ini`、tight 把 `wc` 也收掉。
- **SC-18** (W8): Read `/etc/forgejo/app.ini`、Read `/var/lib/gitea/custom/conf/app.ini`、Edit `/etc/gitea/app.ini`、Read `/data/gitea/conf/app.ini` (`baseline-failing` ×4) → exit 2, **基线 0/4**; Read `/opt/myapp/app.ini`、Read `…/php.ini` (`allow-guard` ×2) → exit 0, **基线 2/2**。怎么会红: `:641` 只改了 Bash 面, 或名字组两面漂移。
- **SC-19** (W9, `CLAUDE_PROJECT_DIR` 指向含 `.aria/secret-guard.paths` 的临时项目): (`baseline-failing` ×8) 列入的路径被 `cat` / `grep … | grep -v` (tight) / Read / Edit 读取、只给 stdin `cwd` 时的回落、经变量间接、含正则元字符的条目、CRLF 文件 → exit 2, **基线 0/8**; (`allow-guard` ×5) `… | wc -l`、`ls -l`、`CLAUDE_PROJECT_DIR` 与 `cwd` 冲突时以前者为准、`.` 按字面、3 字符条目被忽略 → exit 0, **基线 5/5**; (`reverse-guard` ×1) 文件里写 `!.env` 时 `cat .env` 仍 exit 2, **基线相符**。怎么会红: 条目当正则用、没剥 CR、回落顺序颠倒、扩展能放宽内建规则。
- **SC-20** (W9, 扩展失败只丢扩展): 六种坏文件 (缺失 / 是目录 / 悬空软链 / 含 NUL / 超过 32 KiB / 201 条) 各两行 —— 列入的路径 `cat` 放行 (`allow-guard`) + `cat .env` 仍拦 (`reverse-guard`)。**基线 12/12 相符**; 鉴别力来自与 SC-19 成对: 坏文件若导致 fail-closed, 或被部分采用, 放行行即转红。
- **SC-21** (W10): (`baseline-failing` ×8) `f=/etc/forgejo/app.ini; sed -n '1,80p' "$f"`、`f=~/.bashrc; cat $f`、`F=… && cat "$F"`、`export CONF=…; cat $CONF`、事故原形 `ssh root@pve 'pct exec 101 -- sh -c "f=…/app.ini; sed -n 1,80p \$f"'`、链式 `d=…; f=$d/app.ini`、`${f}`、`for f in …` → exit 2, **基线 0/8**; (`allow-guard` ×5) `ls -l "$f"`、`export KUBECONFIG=…; kubectl get pods`、`cp $f /tmp/x`、`for f in *.txt`、普通变量 → exit 0, **基线 5/5**; (`known-limit` ×8) W10 已知限制各一 → exit 0, **基线 8/8**。怎么会红: 展开没覆盖 `export` / 引号值 / `\$` / `for` 形式, 或展开后改用「赋值即拦」。
- **SC-22** (W11): (`baseline-failing` ×35) `ps aux` / `-ef` / `auxww` / `-eo pid,args` / `-o pid,command` / `-ww -fp` / `eww` / `e` / `-C … -o args=` / `--format pid,cmd`、`pgrep -af` / `-a` / `--list-full` / `sudo pgrep -af`、`pstree -ap`、`top -b -n1 -c`、`ps aux | grep curl` / `ps -ef | grep -v grep` / `ps aux | grep '^dev'` (tight)、`docker ps --no-trunc`、`docker top`、`ssh host 'ps aux'`、`x=$(ps aux)`、`sudo ps -ef`、`watch -n 5 ps aux`、`watch -n1 'ps aux'`、`sh -c 'ps aux'`、`bash -c "ps -ef"`、`pct exec 101 -- ps aux`、`kubectl exec … -- ps aux`、`nomad alloc exec … ps aux`、`cat /proc/*/cmdline`、`cat /proc/$pid/cmdline`、`xargs -0 -a /proc/123/cmdline echo`、`cat /proc/*/environ` → exit 2, **基线 0/35**; (`reverse-guard` ×5) 既有 `/proc/N/cmdline`、`tr … < /proc/N/cmdline`、`/proc/N/environ`、`/proc/self/environ`、`strings /proc/1/environ` → exit 2, **基线 5/5**; (`allow-guard` ×19) 只出 pid / 进程名的形态、文本里提到 `ps aux`、`| wc -l`、`>/dev/null`、`man ps`、`docker ps`、`/proc/N/comm`、`/proc/cpuinfo` → exit 0, **基线 19/19**; (`known-limit` ×5) `systemctl status` / `show -p ExecStart`、`docker inspect`、`journalctl` → exit 0, 既有 `cat /proc/N/status` → exit 2, **基线 5/5**。怎么会红: `ps` 选项簇判定过宽 (误拦 comm 形态) 或过窄、命令位置锚丢失 (误拦文本提及)、外壳 / launcher 包裹未覆盖、没用 tight。
- **SC-23** (W12 `\.env`): (`baseline-failing` ×6) `os.environ` ×2、`os.environb`、node / lua 的 `cfg.environment` → exit 0, 以及有意放行的 python3 读 `.env_prod` → exit 0, **基线 6/6 exit 2**; (`reverse-guard` ×11) python3 读 `.env` / `.env.production` / `.envrc`、node 与 lua 读 `.env`, 以及全局加边界会漏的 `head .envrc`、`tail -n 5 .envrc`、`cp .env /dev/stdout`、`scp .env user@host:/tmp/`、`rsync -a .env user@host:/tmp/`、`strings .envrc` → exit 2, **基线 11/11**; (`known-limit` ×2) `node -e "…process.env.HOME…"` → exit 2, `cat .env_prod` → exit 0, **基线 2/2**。怎么会红: 边界套到了三行以外 (`.envrc` 与空白吞并类漏拦)、漏了 `(rc)?`、下划线也被当边界。
- **SC-24** (W12 jq): (`baseline-failing` ×5) `… | jq '.Items | map_values(length)'`、`jq 'keys_unsorted'`、`jq -r '.Items | keys_unsorted'`、`nomad var get … | jq '.Items | map_values(length)'`、claude 配置 (tight) 上的 `map_values(length)` → exit 0, **基线 5/5 exit 2**; (`reverse-guard` ×6) `keys[]`、`. as $d | map_values(length) | $d`、`keys_unsorted | $ENV`、`.Items`、`map_values(tostring)`、`map_values(length), .` → exit 2, **基线 6/6**; (`allow-guard` ×3) `length`、`.Items | length`、`keys` → exit 0, **基线 3/3**; (`known-limit` ×2) `map(.name)` → exit 2, 既有洞 `. as $d | keys | map($d[.])` → exit 0, **基线 2/2**。怎么会红: 新词进了宽松词表 (24h 转红)、锚定写法没要求闭合引号、tight 模式下没生效。
- **SC-25** (W13): (`reverse-guard` ×3) `cat .env` (分段模式)、`x=$(cat .env)` (整串模式)、Read `/x/.env` 的 BLOCKED stderr, 归一化 (`Matched pattern:` / `Command was:` / `Triggering segment:` / `Path:` / `Blocked:` / ack 路径的动态部分替换为占位) 后 sha256 前 16 位等于基线常量。**基线 3/3 一致**。(`baseline-failing` ×4) `ps aux`、`cat /etc/forgejo/app.ini`、扩展条目、Read `/etc/forgejo/app.ini` 被拦时的文本同样等于基线常量。**基线 4/4 未拦 (无文本)**。怎么会红: 改了 heredoc, 或为新拦截另写文案。

**文档、回归与结构**

- **SC-26** (`doc-sync` ×2, W13): `secret-hygiene.md` 有一行同时含「命令行参数」「env」「`--config`」「stdin」; §2.5 有一行含 `pgrep -a`。**基线 0/2**。怎么会红: 条款或进程表行没落 SOT。
- **SC-27** (W14): (`reverse-guard`) `secret-hygiene.md` 三处计数等于 `secret-guard.test.sh` 头注释的 `N` / `M`, **基线 3/3 一致 (599 / 593)**; (`doc-sync`) `secret-scan.test.sh` 头注释 `Coverage: K cases` 存在且等于实跑总数, **基线缺席**; (`reverse-guard`) `secret-hygiene.md` 的 secret-scan 计数等于该套件实跑总数, **基线一致 (49)**。怎么会红: 增删用例后没回填头注释或 SOT。
- **SC-28** (`doc-sync` ×11, W14): W14 所列陈旧 / 悬空表述 9 处消失, 两个 hook 的头注释含 change-id。**基线 0/11**。怎么会红: 同步面漏改。
- **SC-29** (`zero-regression` ×7): 在不带 `.git` 的私有副本上 (zsh 从 PATH 隐去) 跑 `secret-scan.test.sh` 全过且总数 ≥49; `secret-guard.test.sh` PASS ≥581 且 FAIL 至多是测试内 SC-13 头注释计数这一条 (git 历史用例与 zsh 用例被跳过造成的环境性假红); `crlf-shim.test.sh`、`jq-crlf-guard.test.sh`、`host-docker-logout-guard.test.sh`、`submodule-gate-telemetry.test.sh` 与 `jq-crlf-guard.sh` 对两个 hook 的静态检查 rc=0。**基线: 49/49; 581/582 且唯一 FAIL 为测试内 SC-13; 其余 5 项 rc=0**。怎么会红: 新改动破坏既有断言, 或新增 jq 取值点未防 CRLF。
- **SC-30** (`zero-regression`, 探针外): 在带 git 历史 (可取到 `af87cae`) 的真 checkout 上跑 `secret-guard.test.sh` 全绿 —— 含测试内 SC-9a 对拍与测试内 SC-8 五档延迟闸 (天花板不改), 且测试内 SC-13 头注释等于实跑数。**本探针不测**: 测试内 SC-8 是计时闸, 输出不能逐字节复现; 测试内 SC-9a / SC-8 需要 `af87cae` 历史。基线值不填推测数; 研究笔记在带 git 的副本上实测 593/593 (非本探针产出), B.1 入场在真 checkout 实测并记入 handoff 为准。怎么会红: 新行让某档延迟超过天花板, 或改变了测试内 SC-9a 钉住的判定。
- **SC-31** (`reverse-guard` ×5, W14 / Impact): census `patterns.total` ≤ 150; census `family_count` 等于测试里硬编码的值; `risky_patterns` 无整行只由变量组成的行; `hooks/hooks.json` 与基线字节一致; `hooks/hooks.json` 不含字面 `completeness_gate`。**基线 5/5 (145; 61 = 61; 0 行; 一致; 不含)**。怎么会红: 规则膨胀超预算、新族没同步硬编码、用变量整行躲过 census、动了注册面。
- **SC-32** (`reverse-guard` ×2): 两个 hook 的代码行不含 `declare -A` / `mapfile` / `readarray` / `${x,,}` / `${x^^}`; 两个 hook 与两个测试文件保持 LF。**基线 2/2**。怎么会红: 新代码用了 bash 4 专有构造, 或脚本化编辑带进 CRLF。

## rule6_note

SOT = `standards/conventions/skill-benchmark-exemption.md` §2 决策表与 §4.1 五字段。逐 hunk 判定; 代码 hunk 与文案 hunk 判定不同, 分两块写。

**块 A —— hook 判定逻辑、测试、头注释 / 计数 / SOT 文档** (W1–W4、W6–W14 的全部 hunk):

```yaml
rule6_note:
  decision_table_row: n/a
  description_changed: no
  scenario1: n/a
  scenario4b: n/a
  negctrl: n/a
```

理由: 改动对象是两个 PreToolUse / PostToolUse hook 脚本、它们的测试与一份 standards 规范, 零 SKILL.md、零 `description`、零 `references/` 变更, 不属 Skill 变更。W13 写进 `secret-hygiene.md` 的条款是处方性文字, 但它是 standards 规范而不是 Skill 的运行时指令面, 也不被任何 AB 套件加载; 与 `2026-08-02-secret-guard-nomad-var-put-echo` 在同一份 SOT 里改四个推荐位、加两段警示的同类改动同框处理。沿用 owner 2026-08-02 对 hook 的 substitute 框定 (`openspec/archive/2026-08-02-secret-guard-nomad-var-put-echo/proposal.md` 的 rule6_note: deterministic detector hook → structural fixture + unit-test corpus + dogfood; hook 无 SKILL.md / 无 description / 不参与 skill 触发, AB 套件的被测对象与之无交集), 与 `2026-08-18-secret-guard-per-segment-evaluation`、`2026-08-22-secret-guard-manifest-precision` 同框。substitute 三件: structural fixture = 各 SC 的 `baseline-failing` 行 (基线实跑全红, 见证据); unit-test corpus = SC-29 + SC-30; dogfood = 对 canonical hook 的直调 (本探针即是, 目标态须全部 `yes`) + ship 后经 harness hook 链复验 (post-ship 腿, 需 owner 更新插件缓存并重启会话)。可证伪锚点: SC-25 (BLOCKED 文案零改动) 与 SC-31 31d (`hooks.json` 零改动)。

**块 B —— `secret-scan.sh:367` additionalContext 插入「tags + source」** (W5, 唯一改动 AI 可见文本的 hunk):

```yaml
rule6_note:
  decision_table_row: 1
  description_changed: no
  scenario1: not_required
  scenario4b: not_required
  negctrl: n/a
```

理由: 插入的是事实陈述 (命中了哪些 tag、来自哪个工具 / 文件), 不含任何指示行为的措辞 —— 对应 SOT §1「描述性内容: … 陈述事实, 不指示行为」, 落 §2 决策表第 1 行 ⇒ deterministic substitute = SC 级 baseline-failing 结构化测试 (SC-13 13a–13c, 基线实跑全红)。可证伪锚点: 处方句逐字节不变 (SC-13 13d)。L1 的 BLOCKED 文案零改动 (SC-25), 不构成 hunk。

AI 自作主张、待 owner 复议: 块 B 判第 1 行而非第 3 行 —— 若判处方性, 须按 SOT §3 三件套 (点名行为 + 可证伪定向 fixture + 开「AB 套件缺 hook 文案维度」issue); AB 套件对 hook 零覆盖, 照跑 AB 是测量剧场。见「待 owner 复议」第 8 条。

## Impact

- **版本定级**: 建议 **MINOR**。依据 CLAUDE.md §版本管理 (新增能力 = MINOR+、文档更新 / bug 修复 = PATCH): WP-A 新增检测能力 (Read 首次被扫描、6 个 L3 tag)、新输入面 (`.aria/secret-guard.paths`)、新拦截族 (进程表、服务端配置)。先例: 同为新增检测覆盖的 v1.47.0 (`2026-06-19-secret-guard-exfil-coverage-iteration`) 为 MINOR; 单纯 pattern / 名单扩展的 v1.65.4 / v1.66.3 / v1.66.4 为 PATCH。**不写死版本号** (`<vNEXT>`): 取号在发版时刻两端 `ls-remote --tags` 并与 10CG/Aria#199 协商, 号的裁定归 owner。
- **行为变更双向申报**:
  - **新拦截 (L1)**: `app.ini` 族 (Bash / Read / Edit); 项目扩展条目; 变量间接展开后命中的读取; 进程表列举族 —— 含以往放行的日常检查习惯 `ps aux | grep …`, 替代写法 `pgrep -f …` / `ps -eo pid,comm`; `/proc/*` 与 `$pid` 形态。
  - **新告警 (L3)**: Read 工具结果首次被扫描 (读含逼真示例值的文件会告警); 6 个新 tag; 已知误报类 (W2)。
  - **新放行 (L1)**: python3 -c / node -e / lua -e 里的 `os.environ`、`os.environb`、`*.environment`; 经这三种解释器读 `.env_prod` 类下划线后缀名 (有意, 与 `cat .env_prod` 基线一致); jq `keys_unsorted` 与 `map_values(length)` (锚定写法)。
  - **新静默 (L3)**: 既有 `json-secret-field` 上的占位 / 掩码 / wrapper 占位值; 哨兵回灌造成的重复计数。
  - **日志**: `secret-scan.log` 每行多一个 `fp=` 字段 (仓内无读取方)。
- **同步面**: aria 子模块 (两个 hook、两个测试、头注释, 发版六文件 `plugin.json` / `marketplace.json` / `VERSION` / `CHANGELOG.md` / `README.md` / `README.zh.md`; README 只在描述变化时改, i18n 只在正文实质变更时重译); standards (`secret-hygiene.md` §2.5、新条款、§5.1、三处 secret-guard 计数与一处 secret-scan 计数, 版本行 1.1.2 → 1.2.0 —— 新增条款属 additive, 先例 1.0.0 → 1.1.0, 版本历史表追加一行); 主仓 gitlink (aria + standards) 与版本点 (`VERSION`、root README badge、`docs/architecture/system-architecture.md` §2.8 与 `docs/architecture/version-scheme.md` 的 aria-plugin 版本行); CHANGELOG 新节带 rule6_note 行。子模块合并一律本地 merge + 双推 + 逐个 `ls-remote` (CLAUDE.md 多远程两条硬约束); 不在一次性授权内的动作 (合并 master、推 master、tag、发版) 逐次请示。
- **与 10CG/Aria#199 的接缝**: `aria/hooks/hooks.json` 与 `.aria/config.json` 不得出现字面 `completeness_gate` —— 本 Spec 两者都不改 (SC-31 31d / 31e 钉住 `hooks.json`; `.aria/config.json` 在每次动相关文件后用 10CG/Aria#199 的守卫命令复核: 主仓根 `git grep --recurse-submodules -l -F completeness_gate | grep -E '(^|/)(hooks\.json|\.aria/config\.json)$'` 无输出); 文件域不相交 (10CG/Aria#199 不改 hooks); 发版串行 (aria-plugin 版本源唯一), 合并前重新核 `plugin.json`。
- **issue 收尾口径**: ship 后 10CG/aria-plugin#154 可按一次性授权评论并关闭 (三件交付物全部落地, 另含 Read 提取修复); 10CG/aria-plugin#203 与 10CG/Aria#221 属决策单第 2 项的轮换延后集, **保持 open**, 只评论代码侧进展 (哪些形态已拦、哪些是 KNOWN-LIMIT), 不涉轮换 —— 该口径与决策单原文「本项之下不评论」的字面关系列入「待 owner 复议」第 3 条。
- **覆盖关系**: 10CG/aria-plugin#154 全覆盖 (另含 Read 提取修复与头部 / 参数形); 10CG/aria-plugin#203 部分覆盖 (第 1 类服务端配置: `app.ini` 族 + 扩展入口; 第 2 类变量间接: 部分修复 + KNOWN-LIMIT, 输出侧由 L3 兜底); 10CG/Aria#221 部分覆盖 (进程表列举已做; 两处误拦的 `\.env` 与 `keys_unsorted` / `map_values(length)` 已做, `map(.name)` 与 `process.env` 不做; 「拒绝文案加一句」改落 SOT)。

## Tasks (A.2 骨架; 细粒度由 task-planner 产 `detailed-tasks.yaml`, 经 post_planning 审计)

- [ ] 1.1 B.1 入场: 重取行号 (对 `268da8f` 核差异); 在带 git 历史的真 checkout 实跑 `secret-guard.test.sh` 记录 SC-30 基线 (含测试内 SC-8 五档); 复跑 `baseline_probe.py`, 输出与 `baseline-evidence.md` 逐字节一致
- [ ] 1.2 测试先行: 按 SC 把探针用例落为两个套件的用例 (运行时拼装), 先在基线上跑出「baseline-failing 全红、守卫全绿」
- [ ] 1.3 W1 提取 + W6 套件隔离 HOME + W7 既有夹具拼装 (`secret-scan.test.sh`)
- [ ] 1.4 W2 + W3 + W4 + W5 (`secret-scan.sh`)
- [ ] 1.5 W8 + W11 (新行、tight 并入、`/proc` 放宽)
- [ ] 1.6 W12 (`\.env` 三行 + jq 锚定 credit)
- [ ] 1.7 W10 变量展开 + W9 扩展入口
- [ ] 1.8 W14 元耦合同步 (测试内 SC-13 / SC-19 / SC-20 注入自测 / census) + 对抗 review: 坏实现由非作者构造, 至少覆盖「白名单写成含」「tight 漏并入」「扩展坏文件 fail-closed 或部分生效」「jq 新词进宽松词表」四种
- [ ] 1.9 文档同步 (W13 SOT 条款与示例逐工具实跑 + SC-26 / 27 / 28; 勘正执笔人 ≠ 实现执笔人)
- [ ] 1.10 验收: 探针目标态全部 `yes` + SC-30 全绿 + L3 稠密输入预算实测; ship 后经 harness hook 链复验 (post-ship 腿)
- [ ] 1.11 发版 (取号与 10CG/Aria#199 协商, 两端 `ls-remote`) + issue 收尾 (按 Impact 口径) + release claim

## 执笔自报薄弱点

1. **SC-30 没有探针基线**: git 腿 (测试内 SC-9a 对拍、测试内 SC-8 延迟闸) 需要 `af87cae` 历史且是计时闸, 探针为逐字节复现刻意不跑; 基线只能在 B.1 入场实测, 研究笔记的 593/593 不是本探针产出。
2. **目标态的文本自扫描只能在 B.2 验**: SC-15 15e / 15f 的基线只证明现行 hook 不在本 Spec 与探针文本上误报; 新 tag 上线后是否静默, 要等实现。执笔期用研究原型 (设计与本 Spec 不同) 扫过本 Spec 作近似, 不是证据。
3. **W2 的最终设计没有在语料上普查过**: 研究普查用的原型与本 Spec 不同 (JSON 值门槛 8、赋值门槛 12、含小写赋值族、无 Pascal 拼写、无 `cli-secret-flag`); 本 Spec 的误报率要到 B.2 在同一语料上复跑才知道。
4. **W11 的外壳包裹形态没有原型**: `sh -c '…'`、`watch '…'`、`pct exec`、`sudo pgrep -af` 研究原型全部漏 (本 Spec 在原型上实跑确认), 可行性是按既有 remote 行的写法推断的, 未实证。
5. **W9 的项目根语义**: hook 进程里 `CLAUDE_PROJECT_DIR` 的存在性在本环境不可观测 (研究笔记); stdin `cwd` 会随 `cd` 漂移; 「超限整体忽略」与研究原型的截断语义不同, 未原型验证。
6. **SC 钉得很紧**: L3 行要求 tag breakdown 与计数**恰好**等于期望, additionalContext 的插入串逐字写死 —— 实现几乎没有自由度; 若 owner 想换措辞或 tag 名, 是 Spec 变更。
7. **用例规模**: 探针共 326 行 (SC-30 一行不执行); proposal 只写 SC 级摘要, 逐行细节在证据里, 审计需两边对照。
8. **rule6_note 块 B 的归类**是判断 (描述性 vs 处方性), 见待复议第 8 条。
9. **Level**: 与 07-11 先例的 blast radius 论证同形 (改的是每次工具调用必经的判定路径), 本 Spec 未自行升级。
10. **头部 `linked_issue_overlap == []`** 取自派单给出的 phase1_gate 结果; 执笔只在本地协调 ref 上核到了 claim 记录 (`claims/023236f2/s-3e77@1757.yaml`: `status: active`、`phase: A.1`、`linked_issue: 10CG/aria-plugin#154`), 没有见到 gate 输出原文。

## 待 owner 复议

> 产品级 = 请裁 (未裁前按「默认」执行); 技术级 = AI 已裁, 列出供复议 (Rule #10: AI 的流程判断须请复议)。

**产品级 (请裁)**

1. **L3 是否升级为「检测 + 脱敏」(`updatedToolOutput`)**。选项 A: 维持检测 + 告警 (本 Spec 现状; `DEC-20260703-001` 继续有效) —— 代价: 值照样进模型上下文, 只多一条告警。选项 B (**推荐**): 先做一次端到端 spike (验证 `updatedToolOutput` 对 Read / Bash 是否真生效、不合形时的回退、与同 matcher 其它 hook 并行时「最后写入者生效」的实际语义), 通过后新 DEC + 独立 Spec —— 代价: 一次 spike 的成本, 期间同选项 A。选项 C: 本 Spec 内直接加脱敏 —— 代价: 未验证、要推翻 DEC, 误报代价从「多一条提醒」升级为「模型看不到被误脱敏的正文」, 本 Spec 的 W3 / 熵下限会从「降噪」变成「正确性前提」。**默认 (未裁时)**: 选项 A。
2. **拒绝文案是否加「凭据不要放命令行参数」**。选项 A (**推荐**): 文案零改动, 条款只落 SOT (W13) —— 代价: 被拦的当下 AI 看不到这条建议。选项 B: 在全体共用的 heredoc 里加一句 —— 代价: 全部 145 条拦截 (含 `cat .env` 这类无关拦截) 都带这句; 首次改动处方性文案, 按 SOT §3 须三件套 (点名行为 + 定向 fixture + 开套件缺口 issue), 失去 2026-08-02 的「heredoc 零改动」锚点。选项 C: 先解 10CG/aria-plugin#132 (`set -u` 下 `$pattern_hint` 的缺省初始化), 再只对进程表族给定向提示 —— 代价: 多一个前置 issue, 本 Spec 的进程表拦截先无提示上线。**默认**: 选项 A。
3. **10CG/aria-plugin#203 与 10CG/Aria#221 在 ship 后怎么收尾**。决策单第 2 项原文「相关 issue 保持 open、本项之下不评论」: 理解 A (本 Spec 默认) 把「本项之下」读作「不就轮换话题评论」, 保持 open 但评论代码侧进展; 理解 B 读作「整张 issue 都不评论」, 等轮换统一处理时一并。两种都不关闭。**默认**: 理解 A。
4. **Level**: 维持 Level 2 (决策单第 3 项已裁) —— 代价: 不产 `tasks.md`, 细粒度计划只在 `detailed-tasks.yaml`; 或按 07-11 先例的 blast radius 理由改 Level 3 —— 代价: 补 `tasks.md`。post_spec / post_planning 两种 Level 下都照跑。**默认**: 维持 Level 2。
5. **进程表拦截改变日常习惯**: `ps aux | grep X` 这类检查被拦, 改用 `pgrep -f X` 或 `ps -eo pid,comm`; `systemctl status` 刻意放行 (交给 L3)。若 owner 认为误拦代价过高, 可改为只拦不带过滤的形态 —— 代价: `ps aux | grep curl` 恰是 10CG/Aria#221 的泄露形态之一。**默认**: 按 W11。
6. **版本定级** MINOR (建议) 还是 PATCH; 号的裁定归 owner。
7. **建议开单清单** (开新 issue 不在一次性授权内, 逐条请示; 每条附证据位置):
   1. secret-guard 超时即放行: `hooks.json` timeout 5s, 约 1400 个空段使 hook 超时后命令被放行并执行 (研究笔记 secret-guard §0 第 7 条、§6.2 风险 1, 活体证实); 同源的延迟悬崖 (逐字符取子串 O(n²))。
   2. 参数里引号内的 `|` 让所有「读取器 + `[^|]*` + 文件名」行失明 (`grep -E 'A|B' ~/.bashrc` 放行; 研究笔记 secret-guard §0 第 6 条所列既有缺陷之二)。
   3. credit 按整段计: 多行命令里随手一行 `| wc -l` 让整段放行 (研究笔记 secret-guard §0 第 6 条所列既有缺陷之三)。
   4. 既有读取器行无左边界: `chmod 600 ~/.ssh/id_rsa` 因 `chmod` 含 `od` 被拦 (研究笔记 secret-guard §0 第 6 条所列既有缺陷之一; 本 Spec 探索实跑复现 exit 2)。
   5. Bash 面与 Read / Edit 面名单不对齐: 52 个样例 15 个两面判定不同, Read `~/.bashrc` 放行 (研究笔记 secret-guard §0 第 9 条)。
   6. secret-scan PEM 预扫超线性 (870 KB 超过 120s), 被 SIGKILL 后遗留含输出全文的临时文件 (研究笔记 secret-scan §1.8、§5.4)。
   7. secret-scan matcher 缺 Grep / PowerShell (研究笔记 secret-scan §1.1)。
   8. 未覆盖形状: 飞书 webhook URL、Nomad / Consul `SecretID`、封闭表外的 PascalCase 键如 AWS `SecretAccessKey` / `SessionToken` (研究笔记 secret-scan §5.6; 本 Spec SC-10 10f)。
   9. 服务端配置候选名单: `grafana.ini`、`/etc/{nomad,consul,vault}.d/`、`/etc/pve/priv/`、`/etc/shadow`、`.netrc` / `.npmrc` / `.pgpass` / `.git-credentials` / `.vault-token` / `.pypirc` / `.my.cnf` 等 (研究笔记 secret-guard §2 服务端配置一节的候选清单; 需先建语料证明零误报)。
   10. 进程 / 容器环境族: `docker inspect <容器>` 全量 JSON 含 `.Config.Env`、`journalctl`、`nomad job inspect` (研究笔记 secret-guard §2 进程表一节的相邻发现)。
   11. `log_ack` 写 `guard-bypass.log` 不带换行: `entry="$(printf '…\n')"` 的命令替换吃掉换行, 「一事件一行」的 TSV 不变量被破坏 (`secret-guard.sh:617-620`; 本 Spec 实跑: secret-guard 套件 12 条事件写成 0 个换行)。
   12. `host-docker-logout-guard.test.sh` 也向外层 HOME 的 `guard-bypass.log` 写事件 (本 Spec 实跑观察)。
   13. aria-doctor 校验 `.aria/secret-guard.paths` (W9 已知限制)。
   14. jq 词表既有洞: `jq '. as $d | keys | map($d[.])'` 放行 (研究笔记 secret-guard §2 jq 白名单一节; 本 Spec SC-24 24p)。
   15. `corpus_census.py` 的 `criteria.site_count == 6, expected exactly 13` 漂移 (census 以 rc=1 退出, 测试只取 stdout 所以不受影响; 研究笔记 secret-guard §3.4, 本 Spec 实跑复现)。
   16. `cat /proc/N/status` 轻度误报 (研究笔记 secret-guard §2 进程表一节; 本 Spec SC-22 22aj)。

**技术级 (AI 已裁, 待复议)**

8. rule6_note 分两块, 块 B (additionalContext 插入 tag 与来源) 判 SOT 决策表第 1 行 (描述性); W13 写进 `secret-hygiene.md` 的处方性条款按「非 Skill 变更」归入块 A (同 2026-08-02 先例)。
9. W2: JSON 键封闭名表 + 拼写变体; 不纳入小写 YAML 键、CLI 空格分隔形、封闭表外 PascalCase; 新 tag 值长门槛统一 16; 熵下限「至少两类 + 非路径形」。
10. W3: 白名单按值前缀、大小写敏感; 作用于 6 个新 tag + 既有 `json-secret-field`, 不含 `env-line-secret-keyword` 与 provider 前缀类。
11. W4: 值长 16 以上记 sha256 前 8 位、以下只记长度; 追加字段而不另起日志文件。
12. W7: 夹具源头拼装, hook 不加按路径的豁免。
13. W8: 本次只做 `app.ini` 族, 其它候选推迟 (语料证据不足)。
14. W9: 纯文本 + 字面子串 + 失败整体忽略 + `CLAUDE_PROJECT_DIR` 优先、回落 stdin `cwd`。
15. W11: 处置选拒绝而非 `updatedInput` 改写或 `ask`; tight credit; `systemctl status` 放行; 纳入 `sh -c` / `watch '…'` / `pct exec` 外壳与 launcher 包裹的 `pgrep` / `pstree` / `top`。
16. W12: `\.env` 边界用 `[^A-Za-z0-9_]` (fail 方向: `.env_prod` 经解释器由拦变放); jq 两个新形态都走锚定语法, 不进宽松词表。
17. 探针在不带 git 的副本上跑套件 (逐字节可复现), git 腿 (SC-30) 放到 B.1 / B.2 的真 checkout 上。

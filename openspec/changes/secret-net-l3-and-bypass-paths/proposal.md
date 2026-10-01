# Secret 防护网补洞: L3 读取失明与键形缺口 + L1 服务端配置 / 变量间接 / 进程表旁路

> **Level**: Minimal (Level 2 Spec)
> **Status**: Draft — post_spec 审计中
> **Created**: 2026-09-30
> **Linked Issue**: `10CG/aria-plugin#154, 10CG/aria-plugin#203, 10CG/Aria#221`
> **认领**: track `secret-net-l3-and-bypass-paths-023236f2` @ simonfish/023236f2 (session `s-3e77@1757`), phase1_gate A.1 advisory, 2026-09-30T17:57:13Z, `linked_issue_overlap == []`。`--linked-issue` 只接受单值, 认领传的是 `10CG/aria-plugin#154`; 另两张对其它容器的碰撞检测不可见, 以本头部与决策单声明
> **基线冻结**: aria `268da8f` (= v1.74.1); standards `2bc1c4c`; 主仓 `0748dbc` (起草时) —— 文中行号与计数均对 aria / standards 这两个 SHA。SC 的基线值都来自同目录 `baseline_probe.py` 的实跑输出 (SC-30 除外), 原样存于 `baseline-evidence.md`
> **证据位置**: 研究笔记已入仓 `.aria/notes/2026-09-30-wpa-phase-a/research/`, 下文 `scan` = `secret-scan.md`、`guard` = `secret-guard.md`、`prec` = `precedent.md`、`cc` = `cc-hooks.md`, 加节号引用 (如 `scan §1.2`)。笔记里的原型 / 脚本 / 语料在会话临时目录、不在仓内, 所以本 Spec **承重的判据只靠 `baseline_probe.py` 的 SC 行复现**, 笔记只作背景与动机
> **代码落点**: aria 子模块 `hooks/secret-scan.sh`、`hooks/secret-guard.sh`、`hooks/tests/secret-scan.test.sh`、`hooks/tests/secret-guard.test.sh`、`README.md` / `README.zh.md` (Hooks 小节)、`CHANGELOG.md` (+ 发版文件); standards `conventions/secret-hygiene.md`; Spec 落主仓 (Rule #5)。`hooks/hooks.json` 与 `.aria/config.json` 不动
> **决策来源**: `.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md` —— 第 1 项 (secret 网补洞归 WP-A) / 第 2 项 (凭据轮换全部延后: 不产出轮换清单、不逐条提示, 相关 issue 保持 open、本项之下不评论) / 第 3 项 (WP-A = Level 2; Rule #6 沿用 owner 2026-08-02 的 hook substitute 框定, 提示文案 hunk 单独判) / 第 4 项 (一次性授权四类外发动作: feature 分支推送、开 PR、issue 评论、issue 关闭; 边界之外逐次请示: 合并到任一 master (含子模块本地 merge 后的推送)、推 master、打 tag 与发版、主仓 PR 的合并、删除远端分支) / 第 5 项 (023236f2 串行 WP-C → WP-A → WP-B)
> **Level 对账**: 三条升级判据字面命中: `LEVEL_GUIDE` 跨模块条件 (「影响多个子模块」→ 自动提升为 Level 3; 本 Spec 改 aria 与 standards 两个子模块)、`proposal-minimal.md` 的「Changes affecting > 10 files」(aria 10 个 + standards 1 个 + 主仓同步面 8 个文件加 2 个 gitlink + Spec 目录 3 个)、`project.md` Level 表的「Medium features (1-3 days)」(14 个工作项 / 33 组 SC / 320 行探针)。决策单第 3 项已裁 Level 2; 同型先例四份均为 Level 2 且同改 aria hook 与 `secret-hygiene.md` (`2026-07-03-secret-scan-honest-downgrade` / `2026-08-02-secret-guard-nomad-var-put-echo` / `2026-08-18-secret-guard-per-segment-evaluation` / `2026-08-22-secret-guard-manifest-precision`), 反例一份 (`2026-07-11-secret-guard-bash3-multiline-hardening` 以 blast radius 定 Level 3)。按 owner 裁定执行 Level 2, 升级与否列入「待 owner 复议」第 4 条, 不自行改级
> **Rule #7 声明**: 本 Spec 与两份附件不含任何可被现行或拟议 L1 / L3 规则命中的凭据形状字面量 (SC-15 15e / 15f 钉住); 像凭据的值只在探针里运行时生成、只经 stdin 喂 hook, 证据只含退出码 / 是否告警 / tag 名 / 计数。post-ship 复验腿同样只用运行时生成的合成值, 不触碰任何真实 secret 存储, 因此不使用 `# secret-leak-ok-explicit` (步骤见 Tasks 1.10)

---

## Why

三个 issue 指向同一张防护网的三个洞, 两层都有:

- **L3 (`hooks/secret-scan.sh`, PostToolUse, 检测 + 告警)**: 2026-08-20 事故的 JSON `token` 键与 2026-09-26 事故的 `JWT_SECRET = <值>` (等号两侧带空格) 都从全部模式底下穿过 (10CG/aria-plugin#154、10CG/aria-plugin#203)。研究又发现更深的前置缺口: 提取链只认 `output` / `content` / `stdout`, 而 Claude Code 2.1.285 的 Read 结果是 `{type:"text", file:{content,…}}` —— **生产中 Read 从未被扫描**, 现有 Read 用例用合成形状所以一直绿 (`scan §0` 第 2 条)。
- **L1 (`hooks/secret-guard.sh`, PreToolUse, 按命令文本拦截)**: 服务端配置文件 (Forgejo / Gitea `app.ini`) 不在名单、路径经一次 shell 变量即绕过全部文件名规则 (10CG/aria-plugin#203); 进程表列举能把别的进程命令行里的凭据打进输出, 读取路径拦得住、旁路拦不住 (10CG/Aria#221); 同时两处误拦 (`os.environ` 被 `\.env` 命中、只出长度的 jq 形态) 在把使用者推向 `# guard:ack` (10CG/Aria#221 评论 25898: 「降低假阳性率本身就是在保护那道真闸的有效性」)。

**基线实测** (`python3 baseline_probe.py <aria>` @ aria `268da8f`; 值全部运行时生成, 只看退出码 / 是否告警 / tag 名; 原始输出见 `baseline-evidence.md`):

| 洞 | 基线实测 | SC |
|---|---|---|
| L3 Read 提取失明 | Read 真实信封 2/2 静默; 同一内容经 Bash / Write / 旧合成信封 4/4 检出 | SC-1 / SC-2 |
| L3 JSON 键形 (`token`、`sha1`、大写环境变量键等) | 0/15 检出 | SC-4 |
| L3 INI / env 赋值形 (等号两侧空格、引号、`export`、YAML 冒号) | 0/13 检出; `app.ini` 片段 5 个凭据只检出 JWT 形的 1 个 | SC-5 |
| L3 HTTP 头 / CLI 参数形 (含 10CG/Aria#221 的进程行原形) | 0/8 检出 | SC-6 |
| L3 既有键的占位值误报 (FAKE / PLACEHOLDER / NOT-REAL / `[REDACTED]` / 掩码 / L2 wrapper 占位; 文档式占位) | 6/6; 4/4 误报 | SC-11 |
| L3 一份凭据计两次 (哨兵回灌) | `matches=2` | SC-8 |
| L3 日志无值指纹 | 7/7 无 `fp` 字段 | SC-12 |
| L3 测试套件污染真实日志 | secret-scan 套件每跑一次写 33 行; secret-guard 套件写 12 条 ack 事件 | SC-14 |
| L1 `app.ini` 读取 (Bash 面 / Read·Edit 面) | 0/13 拦 / 0/4 拦 | SC-16 / SC-18 |
| L1 路径经 shell 变量间接 | 0/8 拦 | SC-21 |
| L1 进程表列举 (`ps` 完整命令行列 / `pgrep -a` / `top -c` / `/proc/*/cmdline` / exec 包裹下的 env …) | 0/41 拦 | SC-22 |
| L1 `\.env` 无右边界误拦 (`os.environ` 单键读取) | 5/5 误拦 | SC-23 |
| L1 jq 只出元数据的形态 (`keys_unsorted`、`map_values(length)`) | 5/5 误拦 | SC-24 |

平台事实 (影响 Out of scope 的边界): 本机 Claude Code 2.1.285 二进制里 PostToolUse `hookSpecificOutput` 的 schema 含 `updatedToolOutput` (描述原文「Replaces the tool output before it is sent to the model」, `scan §1.9`), 与 `DEC-20260703-001` 及 `secret-scan.sh:15-23`「架构上不能改写、与版本无关」的前提不符 (`cc` 第 1 条写的「不存在 updatedToolOutput」与二进制不符, 以二进制为准); 但**端到端未验证**。本 Spec 维持「检测 + 告警」, 升级为「检测 + 脱敏」列入「待 owner 复议」第 1 条。

## What Changes

> 编号 W1–W14。每项: 现状 (file:line @ `268da8f`) → 改动 → 设计取舍 → 已知限制。机读 token (tag 名、日志字段名、文件名、函数名前缀) 一律英文 canonical。「测试内 SC-n」指 `hooks/tests/secret-guard.test.sh` 里既有的编号 (来自归档 Spec), 与本 Spec 的 SC-n 无关。

### W1 L3 读取提取修复 (10CG/aria-plugin#154 的前置缺口)

- **现状**: `secret-scan.sh:135-142` 提取链 `.tool_response.output // .tool_response.content // .tool_response.stdout // .tool_result.content // .tool_result.output`; Read 真实形状无顶层 `content` ⇒ 内容为空 ⇒ `:144` 直接 exit 0。现有 Read 用例 (`secret-scan.test.sh:28-32`、`:145-153`) 用合成 `{content}` 形状。
- **改动**: 提取链在 `.tool_response.stdout` 之后加 `.tool_response.file.content`, 其余分支与顺序不动 (`# crlf-ok` 保留: 被扫描的数据体不剥 CR)。新测试一律用真实信封 —— Bash `{stdout, stderr, interrupted, isImage, noOutputExpected}`、Read `{type, file:{filePath, content, numLines, startLine, totalLines}}`、Write `{type, filePath, content, structuredPatch, originalFile, userModified}`。
- **设计取舍**: **选 A** 只加 `file.content` 一个分支: 最小、可证伪 (回退即 SC-1 转红)。不选 B「主体 + `stderr` + `structuredPatch` / `newString` + 字符串形」全量拼接: 真实 Bash 形状里 `stderr` 只装 harness 提示 (`scan §1.2` 样本同形), 拼接只增噪声; 字符串形 `tool_response` 会不会到达 PostToolUse 未证实。不选 C 按 `tool_name` 分派: `//` 取首个非 null 已自然区分。
- **已知限制**: Edit / MultiEdit 结果不扫 (见 Out of scope); 字符串形 `tool_response` 不扫 (两者以 KNOWN-LIMIT 钉住, SC-3); Read 读 notebook / PDF / 图片时 `file` 下是否有 `content` 无样本, 不扫。W1 让每次 Read 都走完整扫描 (Linux 实测 4–60 KB 输入每次约 +0.01–0.05 s, 稠密 180 KB 命中输入约 0.8–1.2 s, 均在 `hooks.json` 的 5 s 超时内; Windows Git-Bash 进程派生慢一个量级, 未实测)。

### W2 L3 通用键形模式 (加法式: 6 个新 tag, 既有 31 条模式的正则与顺序不动)

- **现状**: `secret-scan.sh:152-231` 共 31 条模式 + PEM 预扫。通用键形只有两条: `env-line-secret-keyword` (`:224`, 行首、`=` 两侧零空白、无引号、无 `export`、仅大写键) 与 `json-secret-field` (`:227`, 10 个小写键, 无 `token` / `sha1`)。HTTP 头只有 `Bearer` (`:215`) 与 `X-API-Key` (`:218`)。
- **改动 (模式)**: 在 `json-secret-field` 之后、`bcrypt-hash` 之前新增 6 个 tag; 线性 ERE (`grep -E` 与 `sed -E` 通用), 不引入 perl 或回溯; 头名用逐字母大小写类写法而不用 `-i` / `I` 修饰符 (BSD sed 不支持); bash 3.2 可跑 (SC-32):
  1. `json-credential-field` —— JSON 键属封闭名表, 值 `"[^"]{16,}"`。名表 17 个名字干: `token` `sha1` `auth_token` `api_token` `bearer_token` `session_token` `registration_token` `jwt_secret` `secret_key` `api_key` `access_token` `refresh_token` `client_secret` `private_key` `secret` `password` `passwd`; 多词名干允许 snake / camel / Pascal / 连写四种拼写 (`auth_token` / `authToken` / `AuthToken` / `authtoken`), 单词名干允许小写与首字母大写。与既有键重叠的小写 snake 拼写由排在前面的 `json-secret-field` 先消费, 不重复计数 (SC-7)。
  2. `json-env-secret-key` —— JSON 键是大写环境变量名且含 `SECRET|PASSWORD|PASSWD|TOKEN|API_KEY|APIKEY|PRIVATE_KEY|WEBHOOK|ENCRYPTION_KEY|ACCESS_KEY` (Nomad / compose 的 `Env` 映射), 值 ≥16。
  3. `kv-secret-assign` —— INI / env / YAML 赋值: 左侧为行首或非词字符, 可选 `export`, 大写键含同一关键字集 (关键字可在键首), `=` 或 `:` 两侧可有空白, 值可带一层单 / 双引号, 值字符类 `[A-Za-z0-9+/=._~-]` 连续 ≥16。
  4. `auth-header-token` —— `Authorization: token <值>` 与 `Authorization: Basic <值>` (`token` / `Basic` 首字母大小写两可; 头名大小写不敏感, 因为 HTTP/2 下 `curl -v` 回显的是小写头名), 值 ≥16。
  5. `cf-access-client-secret` —— `CF-Access-Client-Secret: <值>` (头名大小写不敏感), 值 ≥16。
  6. `cli-secret-flag` —— 以 `token|password|passwd|secret|api-key|apikey|access-key` 结尾的 `-` / `--` 参数名用 `=` 连写值 (如 `--token=<值>`), 值字符类同第 3 项, ≥16。
- **改动 (分类器)**: 6 个新 tag 与既有 `json-secret-field` (后者只过第 2 步) 的每个命中 span 依次过 —— 1. 取值 (取值表见 W4); 2. W3 白名单 → 不计数; 3. **熵下限** (仅新 tag): 值含小写 / 大写 / 数字三类中至少两类 (符号不算类); 4. **路径形** → 不计数: 值以 `/`、`~/`、`./`、`../` 之一开头, 全部字符属 `[A-Za-z0-9._~/-]`, 且至少含两个 `/` (`+` 与 `=` 不在字符类里, 所以 `openssl rand -base64 32` 的 44 位值 (末尾带 `=`) 即使以 `/` 开头也不会被当成路径; 无填充且不含 `+` 的 b64 值偶有同形, 属残余); 5. **点分标识符链** → 不计数: 整值匹配 `^[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)+$` (`process.env.X`、`settings.X` 这类「从环境 / 配置读取」的写法)。其余计数。每个 tag 最多分类 200 个 span, 超出部分不分类照计 (fail-closed, SC-11 11w); 分类路径**零 fork** (只用 builtin 与 `[[ =~ ]]`; 正则放进变量: bash 3.2 解析不了 `[[ ]]` 里的裸 `<`)。
- **设计取舍**:
  - 键表: **选 A** 封闭名表 + 拼写变体。不选 B「任意含 `token` 的键」: 分页游标 `next_page_token` 等会成误报 (SC-9 9j; 9h 用 24 位值钉住 `token_last_eight` 这类「以 token 起头」的键)。不选 C 只加 10CG/aria-plugin#154 原文的 `token` / `sha1`: 漏 `registration_token` / `jwt_secret` / `auth_token` 与首字母大写键 (`scan §3` 矩阵 JX1–JX4)。
  - 大小写: **选 A** 纳入 camel / Pascal (Go 系服务的 JSON 常用 PascalCase)。不选 B 全大小写不敏感: ERE 里要逐字母写类, 复杂度换不到证据。
  - 小写 YAML 键 (`password: <值>`): **选 A** 不纳入, KNOWN-LIMIT (SC-10 10d); 研究普查最大的误报来源正是小写赋值族 (`scan §5.2` 结论 1)。不选 B 纳入并提高熵下限: 仍挡不住大小写混合的标识符值。
  - 值长下限: **选 A** 统一 16 (`scan §3` 矩阵正例全部 ≥20)。不选 B 沿用既有 `json-secret-field` 的 8: 误报面更大。
  - CLI 参数: **选 A** 只认 `=` 连写。不选 B 空格分隔 `--token <值>`: 下一个词可能是子命令或文件名 (KNOWN-LIMIT SC-10 10e)。
  - 熵下限: **选 A**「至少两类」。不选 B「必须含数字」: 20 位字母数字约 3% 无数字而漏 (SC-4 4o 钉住)。不选 C Shannon 熵阈值: bash 3.2 下计算昂贵, 对短值不稳。
  - 路径形: **选 A** 开头标记 + 字符类 + ≥2 个 `/`。不选 B「首段为小写目录名」: macOS 的 `/Users/…`、`~/Library/…` 仍告警 (SC-9 9w)。不选 C「任何 `/` 开头即路径」: `openssl rand -base64 32` (10CG/aria-plugin#203 事故形态) 的值有 1/64 以 `/` 开头, 会被静默 —— 严格与宽松读法只在 SC-4 4n / SC-5 5l 上分叉, 这两行就是为此而设 (探针默认生成器从不以 `/ $ < - _` 等字符开头, 这些行用强制首字符生成器)。
  - 点分标识符链: **选 A** 排除: 「从环境读取」的写法是新 tag 的主要误报形态, 随机凭据不含以 `.` 分隔的标识符段, 漏报面≈0 (SC-9 9v)。不选 B 排除全部「只含字母」的值: 重新引入那 3% 的漏报。
- **已知限制** (漏报类以 KNOWN-LIMIT 钉住, SC-10): 单字符类随机值; 值短于 16; 小写 YAML 键; CLI 空格分隔; 封闭表外 PascalCase 键 (如 AWS 的 `SecretAccessKey`); Python dict repr (单引号); 值里第一个符号出现在 16 个字符类字符之前的赋值; JSON 文本嵌在 JSON 字符串里 (转义引号, 键名两侧带反斜杠)。已知误报类 (成文, 不钉测试): 16 字符以上、含两类字符的名字形值 (`PasswordConfirmation` 一类类名)、人类可读的示例口令 (小写 + 数字 + 连字符)、不以 `/` `~/` `./` `../` 起头的相对路径值 (如 `Config/Prod/Db2Password`) 会告警, 本仓语料里只有两个文件命中新 tag (SC-33 的归因清单); 校验和 JSON 里的 `sha1` 键、文档里的 `Authorization: Basic` 示例值、`TOKEN_ID: <uuid>` 同样会告警。

### W3 L3 误报白名单 (只认整值占位形态, 不认单字符前缀)

- **现状**: 全文无白名单。既有 `json-secret-field` 对占位 / 掩码值 6/6 告警 (SC-11 11m–11r); L2 wrapper 对 `token` / `sha1` / `client_secret` / `secret` 四键输出 `[REDACTED-BY-WRAPPER len=N]` 占位串 (`prec §6.4`), 已在既有键上误报; 给 L3 加 `token` / `sha1` 而不放行这类占位, 每次走 wrapper 的凭据类调用都会恒红。文档里的占位写法 (`<…>`、`${VAR}`、被截短的哈希前缀) 同样在既有键上告警。
- **改动**: 对每个被分类的 span 取值后, **整值**属于下列形态之一即不计数 (大小写敏感, 英文大写 canonical, 与 10CG/aria-plugin#154 评论 19339 一致):
  1. 尖括号占位: 以 `<` 开头、以 `>` 结尾、中间不含 `<` `>` (含计数哨兵 `<secret-scan-counted:…>`);
  2. 变量引用: `${…}` (花括号闭合)、`$NAME` (NAME 全大写或全小写, 加数字与下划线; **不含混合大小写**)、`$(…)` (圆括号闭合);
  3. 模板: `{{…}}` 或 `${{…}}`;
  4. 脱敏串: `[REDACTED…]` (括号闭合) 或整值是 `*` / `x` / `X` 的重复;
  5. 截断标记: 值以 `…` 或 `...` 结尾 (被截短展示的哈希前缀等);
  6. 刻意标记词开头: `FAKE`、`PLACEHOLDER`、`NOT-REAL` / `NOT_REAL` / `NOTREAL`、`REDACTED`。

  **不是**白名单的: 以 `$` 开头的随机值 (`$` 后是混合大小写或夹杂符号)、以 `<` 开头但不闭合的值、完整长度的 crypt 口令哈希 (如 `$2b$` 开头的 60 字符串) —— 它们在既有键上基线即检出, 必须仍被检出 (SC-7 7h / 7i)。作用范围 = 6 个新 tag + 既有 `json-secret-field`; 不作用于 provider 前缀类、`env-line-secret-keyword` 与其余既有 tag。
- **被放行的 span 是否仍被哨兵消费**: **是**。理由: 放行的只有上面 6 类整值占位, 没有任何后序 tag 应当计数它们 (整值占位不是哈希也不是凭据), 消费让每个 span 只做一次决定; 若放行靠 `<` / `$` 这类单字符前缀, 被放行的 span 会连真值一起吞掉 (SC-7 7h / 7i 的负向行钉住), 整值形态下不存在这个问题。唯一的损失面是第 6 类: 带 `FAKE_` 前缀的真哈希会被放行且不被 `bcrypt-hash` 再看 (有意: 作者刻意标了假)。哨兵整值属第 1 类, 所以前序 tag 已计数的 span 在 `json-secret-field` 里不再重复计数 (SC-8)。
- **设计取舍**:
  - 判定方式: **选 A**「整值形态 + 标记词开头」。不选 B「值以 `<` / `$` / `{{` 开头即放行」: 把 bcrypt 哈希与 `$` / `<` 开头的随机口令也放行 (SC-7 7h / 7i 钉住; 变异实测该写法在 7h / 7i 转红)。不选 C「span 含标记词即跳」: 既有 provider 夹具的 FAKE 在值中间 (`secret-scan.test.sh:102`、`:107`), 会被翻红, 也会放过中段恰含该词的真值 (SC-11 11s、SC-7 7h; 变异实测「含」与「大小写不敏感」都转红)。
  - 是否延伸到既有 `json-secret-field`: **选 A** 延伸, 两面测试: 占位误报消除 (SC-11 11m–11r、11v) + 真阳性仍检出 (SC-7 7d / 7e / 7h / 7i、SC-11 11t, 既有 49 用例零回归 SC-29)。不选 B 不延伸: wrapper 占位在 `client_secret` / `secret` 上的既有误报继续恒红。
  - 是否延伸到 `env-line-secret-keyword`: 不选。它的值字符类已排除 `<` `$` `{` `*` `[`, 没有实测误报证据 (SC-7 7h 钉住「不延伸」)。
  - 占位写法与本 Spec 自身: 本 Spec、测试与证据文件里的占位用尖括号、`${…}` 或 `json:key=<…>` 标签形; SC-15 15e / 15f 钉住「本 Spec 与探针的文本被扫描时静默」。
- **已知限制**: 以第 6 类标记词开头的真凭据会被放过 (须人为构造); 小写 `fake_` 不在白名单 (SC-7 7h); 整值被尖括号包住的真凭据会被放过 (实际不出现); 值中夹带哨兵但不是整值时仍会重复计数 (基线同)。

### W4 L3 日志留痕: 值指纹 (新功能, 不是「补断言」)

- **现状**: `secret-scan.sh:355-361` 日志 8 个 TSV 字段 (时间 / USER / PWD / `SCAN-DETECT` / tool / matches / breakdown / size), 既无值也无哈希。10CG/aria-plugin#154 评论 19339「若现行为已如此则只加断言」的前提不成立。
- **改动**: 追加第 9 字段 `fp=`: 对每个被计数的 span 取**凭据本体** (下表) 按计数遍历序最多记 10 项, 逗号分隔; 遍历序 = PEM 预扫最先, 然后按 `PATTERNS` 顺序, 同一 tag 内按文本先后。每项: 值长 ≥16 → `sha256(值)` 的 hex 前 8 位; 值长 <16 → `L<长度>` (不记哈希); `sha256sum` 与 `shasum -a 256` 都取不到 → `-` (fail-soft, 日志照写)。值与片段不进日志、stdout、stderr (SC-12 12d–12f)。

  | tag | 凭据本体 (指纹与 W2 / W3 分类的取值) |
  |---|---|
  | provider 前缀类 (`jwt`、`silknode-` / `anthropic-` / `openrouter-` / `openai-*`、`stripe-*`、`github-*`、`gitlab-pat`、`aws-*`、`aliyun-*`)、`discord-webhook`、`slack-webhook`、`bcrypt-hash` | 整个 span |
  | `env-line-secret-keyword`、`cli-secret-flag` | 第一个 `=` 之后 |
  | `json-secret-field`、`json-credential-field`、`json-env-secret-key` | JSON 字符串值 (不含引号) |
  | `kv-secret-assign` | 键名 (大写字母 / 数字 / 下划线连续段) 之后的第一个 `=` 或 `:` 之后, 去空白与一层引号 |
  | `bearer-token`、`auth-header-token` | 末词 |
  | `x-api-key-header`、`cf-access-client-secret` | 头冒号之后, 去空白 |
  | `postgres-url`、`redis-url`、`mongodb-url`、`basic-auth-url` | 口令分量 (用户名之后的第一个 `:` 到 `@` 之间) |
  | `gcp-private-key-id` | 引号内的 40 位 hex |
  | `pem-private-key-block`、`pem-header-only` | `-` (不是 token) |

  SC-12: 12a–12c 单值 JSON; 12g 非 JSON tag 取裸值且按遍历序; 12h `app.ini` 五值「jwt 先、其余按文本序」; 12i 11 个值恰 10 项; 12j 其余取值形态 (gcp key id / URL 口令分量 / `X-API-Key` / `Authorization: token` / `CF-Access-Client-Secret` / `--token=`) 一个文本六种形态。
- **设计取舍**: **选 A** 16 字符门槛 + 短值只记长度: 8 位无盐前缀可被离线字典确认低熵口令, 16 字符以上的机器生成值没有这个风险。不选 B 全部记 8 位: 对短口令构成确认预言机。不选 C 加盐 / HMAC: 失去与 `.aria/pat-inventory.yaml` 台账 (`sha256(token 原文)` 的 hex 前 8 位) 的可比性 —— 这也是上表逐 tag 取裸值的原因: 整 span 的哈希与台账永不相等。不选 D 另起 `credential-tripwire.log` (10CG/aria-plugin#154 原草案): 该日志仓内零读取方 (`scan §1.7`), 追加字段零兼容负担。fail-soft 同 `secret-guard.sh:626` 的 `${hash:-unknown}` 先例。
- **与 10CG/aria-plugin#92 的接缝**: `DEC-20260703-001` 把「泄露事件记录 schema / redaction 安全 / 分级 block」划给仍 open 的 10CG/aria-plugin#92; 本 Spec 只追加 `fp=` 字段、不起事件记录。`fp` 的算法、16 字符门槛与「值与片段不进任何输出」是 10CG/aria-plugin#92 的事件 schema 应复用的口径。
- **已知限制**: 日志文件权限沿用默认 umask (既有); 人为选取的 16 字符以上低熵口令仍可被字典确认。

### W5 L3 告警文案: 只加描述性信息

- **现状**: `secret-scan.sh:367` 的 additionalContext 只有计数; 收到告警的一方要离线复现才知道是哪类命中 (`scan §1.6`)。
- **改动**: 在 `in tool output` 与 ` — treat as already-leaked` 之间插入 ` (tags: <tag>=<n> …; source: <tool_name>[ <file_path>])`。tag 串复用 systemMessage 已有的 breakdown; `file_path` 取 `tool_input.file_path`, 只对 Read 与 Write 输出 (取值剥 CR)。其余字节 —— 含处方句 —— 与基线逐字节一致: SC-13 13d 用**全串等值**钉住 (删去插入段后与基线文本逐字节相等, 追加任何别的句子都转红); systemMessage 格式、stdout 键集、exit 0 不变 (SC-13 13e / 13f)。
- **设计取舍**: **选 A** 只加描述性事实, Rule #6 可按描述性判 (见 rule6_note)。不选 B 10CG/aria-plugin#154 原稿的「疑似, 若为 fixture 请说明」「轮换放最前」: 属处方性改写, 且评论 19339 已确认现行已满足。不选 C Bash 也附命令摘要: 命令文本可能含值, 需要再做一轮脱敏。
- **与决策单第 2 项的关系**: 第 2 项「不逐条提示轮换」针对已知的四张待轮换 issue (10CG/aria-plugin#203 / 10CG/Aria#221 / 10CG/Aria#170 / 10CG/Aria#136) 的处理节奏; L3 对**新检出事件**的标准处置 (按已泄露处理、建议轮换) 不变, 本 Spec 不改那句话, 也不产出任何轮换清单。

### W6 测试卫生

- **现状**: 两个套件都不设 `HOME`。基线每跑一次 `secret-scan.test.sh` 向外层 `~/.claude/logs/secret-scan.log` 追加 33 行夹具事件, `secret-guard.test.sh` 向 `guard-bypass.log` 追加 12 条 ack 事件 (SC-14)。`secret-scan.test.sh:93-123` 的检测夹具是字面量。
- **改动**: 两个套件开头把 `HOME` 指向自建临时目录并在退出时清理; 新夹具一律运行时拼装, 源码不出现凭据形状字面量 (GitHub 镜像的 push protection 只放行这两个测试文件, `aria/.github/secret_scanning.yml:18-22`)。
- **设计取舍**: **选 A** 在套件里隔离。不选 B 让 hook 识别测试环境后不写日志: 生产代码为测试开后门。
- **已知限制**: `host-docker-logout-guard.test.sh` 同样写外层 `guard-bypass.log` (本 Spec 实跑观察到), 不在本 Spec 文件域 → 列入建议开单。

### W7 夹具静默 (W1 的连带问题)

- **现状**: W1 生效后, 读 `hooks/tests/secret-scan.test.sh` 会持续注入「按已泄露处理」(`scan §5.3`); 把该文件文本当 Bash 输出扫, 基线即命中 33 处 (SC-15 15a)。WP-A 实施期会反复读写这个文件。
- **改动**: 把该文件现有字面夹具改为运行时拼装 (如把前缀拆成两段字符串拼接), 每条断言的输入值与期望 tag 不变; hook 侧**不加**任何按路径的豁免。可机械做到 (起草期原型验证): 在每个被扫描模式命中的 span 内部插入一对空引号 (`""` 或 `''`, 取决于所处引号上下文), shell 构造出的字符串逐字节不变, 49 条断言照过, 文件文本再扫描零命中。
- **设计取舍**: **选 A** 源头拼装: hook 零新增逻辑, 没有任何路径被豁免, 也就不存在「真实泄露只进日志」的盲区; 可证伪: 文件文本扫描转为静默 (SC-15 15a), 既有断言照过 (SC-29)。不选 B 按路径的「只记日志、不注入 additionalContext」清单: 要新逻辑与清单维护, 清单内若真有泄露模型不知情。不选 C 不处理: 实施期每次读测试文件都收到恒红告警。
- **已知限制**: 其它含逼真示例值的文件 (如 `aria/skills/requesting-code-review/examples/no-plan-fallback.md` 里一行人类可读的硬编码口令) 在 W1 后被 Read 时会告警, 与今天 `cat` 它们时一致, 不是新增面; SC-33 把这类文件列入归因清单。

### W8 L1 服务端配置文件 (Forgejo / Gitea `app.ini`)

- **现状**: Bash 面 `risky_patterns` (`secret-guard.sh:736-1009`, 145 行) 与 Read/Edit 面正则 (`:641`) 都没有服务端配置文件 (SC-16 0/13、SC-18 0/4)。credit 收紧 (tight) 只认 claude 配置 (`:405-408`)。既有读取器组没有左边界 (`chmod` 里含 `od`)。
- **改动**:
  1. 名字组单一定义为变量、两处消费: 一个路径分量含 `forgejo` 或 `gitea` (词内前缀允许, 如 `git-forgejo`) 之后同一路径内的任意非空白非引号字符再接 `app.ini` (覆盖 `/etc/forgejo/app.ini`、`/var/lib/forgejo/custom/conf/app.ini`、容器内 `/data/gitea/conf/app.ini`、`/srv/git-forgejo/app.ini`), 以及 `custom/conf/app.ini`; `app.ini` 之后不得紧跟字母 / 数字 / 下划线 (所以 `app.ini.bak` 这类备份也在名单里, `app.inix` 不在)。
  2. Bash 面新增一行: 打印型读取器组 (claude-config 行 `:815` 的 13 个 + `nl tac rev sort uniq cut paste diff cmp comm xxd od hexdump base64 column fold`), 自带左边界 `(^|[^[:alnum:]_.-])`; 名字前用 `_SG_PP_NAME` 前置白名单 (10CG/Aria#179 体例)。python3 -c / node -e 源组 (`:893` / `:894`) 追加同一名字组。新行不用 `\b` (BSD 正则不支持, 与 10CG/aria-plugin#144 同族)。
  3. Read/Edit 面 `:641` 追加同一名字组 (对小写化后的路径)。
  4. tight 检测 (`:405-408`) 并入该名字组: 锚定 grep / `grep -v` / sed / cut / awk 不再算 credit (否则 `cat …/app.ini | grep '^JWT_SECRET'` 被当过滤放行并泄露, SC-16 16f); `wc` / `sha*sum` / `>/dev/null` / jq 名字面 credit 保留 (SC-17 17a)。
- **设计取舍**: **选 A** 只做 `app.ini` 族 (有事故证据, 10CG/aria-plugin#203)。不选 B 同批纳入 `grafana.ini`、`/etc/{nomad,consul,vault}.d/`、`/etc/pve/priv/`、`/etc/shadow` 与经典凭据点文件: 本轮没有它们的事故证据, 也没有零误报的语料实测 (候选清单见 `guard §2(a)`) → 列入建议开单。不选 C 裸名 `app.ini`: 任何应用都有 (SC-17 17a 钉住 `/opt/myapp/app.ini`、`php.ini` 放行)。右边界: **选 A** 不为模板放行 —— `app.ini.example` / `.tpl` 在基础设施仓里会被拦 (走 ack), 因为 `app.ini.bak` 这类真备份与模板在命令文本上无法区分, 拦住备份的价值更大。
- **已知限制**: `cd /etc/forgejo && cat app.ini` 这类相对名 (SC-21 21r); `cp …/app.ini /tmp/x && cat /tmp/x` 先复制再读 (SC-17 17b; 按名字拦截的固有上限, 输出侧由 W1 + W2 兜底); 模板 / 示例文件被拦; 引号内 `|` 让 `[^|]*` 行失明 (既有缺陷, 建议开单); `sed -i` 编辑 `app.ini` 同样被拦 (与 `sed -i ~/.bashrc` 一致, 走 ack); Edit 工具被拦 (走 `SECRET_GUARD_ACK_PATH` nonce, SC-18 18f / 18g 钉住该逃生口对新拦截有效); **Grep 工具读这些路径两层都不经过** (两层 matcher 都不含 Grep, 本 Spec 冻结 `hooks.json`, 结构上无法修, 建议开单)。

### W9 L1 项目级扩展入口 `.aria/secret-guard.paths`

- **现状**: 两个 hook 都不读任何项目文件, 也不解析 stdin `cwd` 与 `CLAUDE_PROJECT_DIR` (`secret-guard.sh:564` 只抽 4 个字段)。
- **改动**:
  - **位置**: `<项目根>/.aria/secret-guard.paths`。项目根 = 非空的 `CLAUDE_PROJECT_DIR`; 否则 stdin 的 `cwd` (单独一次 jq 取值并剥 CR, 且仅当输入含 `"cwd"` 才取 —— 常态下零额外 fork; 不改 `:564` 的 4 字段 NUL 抽取与 `== 4` 守卫)。
  - **格式**: 一行一个**字面子串** (不是正则, 不是 glob); `#` 起首为注释, 空行忽略, 剥行尾 CR 与首尾空白; 长度 4–200 且含字母或数字的行才生效, 其余行跳过 (跳过的行不影响其它行)。匹配**大小写不敏感** (两面一致: Read/Edit 面本就对小写化路径匹配; 默认大小写不敏感的文件系统上也不会因大小写漏拦)。
  - **语义 (只增不减)**: 不能移除或放宽任何内建规则 (写一行 `!.env` 也只是一条字面子串, SC-19 19n)。Bash 面: 条目 (小写化后) 作为字面子串出现在命令文本里, 且其**每一处出现**之前、同一管道阶段内 (最近的 `|` `;` `&` 换行之后) 有一个读取器 —— W8 打印型读取器组, 或 `python3 -c` / `node -e` 源组 (与 W8 对 `app.ini` 的作用面一致, SC-19 19o) —— 则按 **tight credit** 判 (`grep … | grep -v` 不算过滤, `| wc -l` 算, SC-19 19b / 19e); Read/Edit 面: `file_path` (小写化后) 含该子串 → 拦 (同一 `SECRET_GUARD_ACK_PATH` nonce 逃生口, SC-19 19s / 19t)。变量间接 (W10) 同样作用于扩展条目: 判原命令一次, 判替换后的整串一次 (SC-19 19i)。拒绝时复用同一份 BLOCKED 文案 (SC-25 25f), 不为扩展另写文案。
  - **匹配实现 = 固定字符串、单遍、有上界**: 全部条目对命令文本 (或 `file_path`) 只做**一次**固定字符串多模式比对 (建议 `grep -F -i -f <(条目) <(命令文本)`: 不编译正则、不解释 glob, 条目里的 `\ ^ $ . | ? * + ( ) [ ] { }` 全是字面字符, 一条坏条目不会让其它条目失效, SC-19 19j / 19k、SC-20 20h); 命中的出现点最多检查 64 处; 条目数上限 200、文件上限 32 KiB 即是成本上界。无扩展文件时 (项目根下没有该文件) 不 fork 任何子进程 (`[[ -f ]]` 是 builtin)。
  - **隔离 (扩展代码不得能中断内建判定)**: 扩展的全部代码 —— 项目根解析、文件读取与校验、条目匹配、tight credit 调用 —— 写在名为 `_sg_ext_*` 的函数里, 且**只**经命令替换 `$( … )` 调用 (各在独立子 shell 里); 调用方只比较其输出与字面哨兵 `BLOCK`, 其它任何结果 (空输出、非零退出、未绑定变量、`exit`) 一律视为「扩展不生效」。Read/Edit 面与 Bash 面都走这条路 (Read/Edit 分派 `:631-694` 在主 shell 里, 不在 `:1111` 的 fail-closed 子 shell 之内, 裸调用的故障会以 exit 1 结束 = PreToolUse 放行, 连内建拦截一起失效)。Bash 面入口函数 `_sg_ext_pass`、Read/Edit 面入口函数 `_sg_ext_path_pass` 的名字是约定 (故障注入与顺序探针按名定位, SC-20 20i–20m); 函数定义行 `name() {` 之后可带注释, 探针的注入器容忍之。
  - **求值顺序 (内建先、扩展后)**: 全部内建判定 (含 W10 的第二遍) 都放行之后才调用扩展; 内建已拦则扩展代码**一次都不被调用** (SC-20 20l), 内建放行且扩展文件存在则扩展**被调用** (无死代码, SC-20 20m)。因此扩展只能追加拦截, 也不会把内建判定推迟。
  - **失败处理 = 扩展失败只丢扩展**: 文件缺失 / 不是普通文件 / 不可读 / 超过 32 KiB / 含 NUL 字节 / 有效条目超过 200 → 整个扩展不生效, 内建名单照常 (SC-20 20a–20g 两面各查); 扩展代码自身故障同样只丢扩展 (SC-20 20i–20k 故障注入); 从不因扩展问题 exit 2 (10CG/Aria#154 会话死锁教训; `handoff-location-guard.sh` 的 fail-open 先例)。这**不是**整体 fail-open: 内建规则的判定与其 fail-closed 路径不受扩展影响。
  - **失效是否对用户可见**: 本 Spec **不**加。扩展失效保持静默, 缓解靠文档 (下) 与后续 aria-doctor 校验 (属 Skill 改动, 建议开单)。不选「exit 0 + stdout `systemMessage`」: 该通道在 PreToolUse 上的端到端行为未验证、会在热路径新增一条输出通道、且无状态时每次调用都重复提示; 选项列入「待 owner 复议」第 18 条。
  - **文档落点** (同步面, SC-26): `secret-hygiene.md` 新增 §5.6 (位置 / 格式 / 只增不减 / 限额 / 失效即整体忽略且静默 / 大小写不敏感); aria `README.md` 与 `README.zh.md` 的 Hooks 小节各一段; `secret-guard.sh` 头注释一段。
- **设计取舍**:
  - 宿主: **选 A** `.aria/` 下纯文本清单 (仓内先例 `bare-issue-ref-allowlist.txt`、`linked-issue-field-grandfathered.txt`)。不选 B `.aria/config.json` 新键: 撞 10CG/Aria#199 的 `completeness_gate` 守卫面与 `config-template-key-currency` 检查, 还要登记 `config.template.json`、`DEFAULTS.json` 与 config-loader (Skill ⇒ Rule #6 面扩大)。不选 C `.claude/settings.json` 的 env 注入: 未验证 env 块是否传给 hook, 且只有人能维护。
  - 条目语义: **选 A** 字面子串 + 固定字符串匹配 (杜绝正则写错或元字符导致的静默失配; 变异实测「条目当 `grep -E` 正则」的实现在 SC-19 19j、SC-20 20h 转红)。不选 B ERE / glob。
  - 项目根回落: **选 A** stdin `cwd` (hook 契约字段)。不选 B hook 进程的 `$PWD`: Bash 工具 `cd` 之后与项目根无关。
  - 超限处理: **选 A** 整体忽略 (一条规则, 可预测; SC-20 20f, 变异实测「截断到 200 条」转红)。不选 B 截断到前 200 条: 部分生效的清单更难排查。代价是悬崖 —— 第 201 条让前 200 条一起失效且静默, 与「失效是否可见」一并列入「待 owner 复议」第 18 条。
- **已知限制**: 扩展失效是静默的; 采用方的 AI 也能编辑这个文件 (威胁模型是防意外, 同 hook 头注释); `cwd` 回落在 `cd` 之后可能找不到文件 (只在 `CLAUDE_PROJECT_DIR` 缺失时才用到); Windows Git-Bash 下 `CLAUDE_PROJECT_DIR` 的路径形态 (`C:\…` 还是 `/c/…`) 与条目写法的关系未验证; Grep 工具读列入的路径两层都不经过 (见 W8)。

### W10 L1 路径经 shell 变量间接 (部分修复)

- **现状**: 路径与读取器分落两段 (`f=…; cat "$f"`), 逐段评估 (`:1088-1102`) 看不到; 即便降级成整串, 所有行都要求「读取器在前、名字在后」(SC-21 0/8)。10CG/aria-plugin#203 自己写明它的第 2 类「在命令侧基本堵不住」, 设计意图就是交给 L3。
- **改动**: 在整条命令上收集字面赋值 (`NAME=值`, 含 `export/declare/local/readonly/typeset` 前缀、单双引号值、`for NAME in 列表`、单层链式 `d=…; f=$d/…`; 上限 16 个赋值、每变量 8 次替换), 对每个含 `$NAME` / `${NAME}` / `\$NAME` 的段 (或降级时的整条命令) **额外**判一次替换后的副本。原判定不变, 只可能新增拦截。
  - **求值顺序**: 全部段先按内建规则判完, 全部放行后才进入第二遍 (入口函数名 `_sg_vx_pass`): 内建已拦则第二遍一次都不运行 (SC-21 21v), 全部放行则运行 (SC-21 21w); 按段交错 (段 1 原判、段 1 替换判、段 2 原判 …) 会把「原判定不变」在时间维度上破坏 —— 5 s 超时即放行。新函数放在测试 source 闸门 (`:491-493`) 之上。
  - **替换一律用前后缀拼接** (`${s%%"$pat"*}` / `${s#*"$pat"}`), 不用 `${s//pat/rep}`: bash 5.2 的 `patsub_replacement` 要求给替换串加引号 (否则 `&` 被换成匹配文本), 而 bash < 4.3 把替换串里的引号**原样带进结果** (3.2.57 实测 `x=abc; r=Z; echo "${x//b/"$r"}"` 输出 `a"Z"c`, 5.2 输出 `aZc`) —— 两条规则互相冲突; 用 `${s//p/r}` 的实现在真 bash 3.2 下链式赋值判错 (SC-32 32c 的差分可抓到)。
- **设计取舍**: **选 A** 字面赋值展开 (研究原型: 24 条泄露形态 24/24 拦, 22 条正常用法 0 误报, `guard §2(c)`; 可复现的钉子是 SC-21)。不选 B「给敏感路径赋值就拦」: `export KUBECONFIG=~/.kube/config` 这类惯用法误报面大 (SC-21 21i)。不选 C 整串共现: 精度最差。
- **已知限制** (KNOWN-LIMIT, SC-21 21n–21u, 各钉现状放行; 对外表述为「部分覆盖」, 不宣称根治): 数组赋值、`read … <<<`、引号拼接路径、`"$d"/app.ini` 引号夹在路径中间、`cd … && cat 相对名`、glob、`set --` 位置参数、`$(printf …)` 拼路径、跨两次工具调用的变量 (Bash 工具不保留 shell 状态)。这些交给 L3 (W1 + W2 在输出侧兜底: 2026-09-26 事故泄露的那一行正是 SC-5 5a 的形态)。同一架构面的在案 issue: 10CG/aria-plugin#138 (跨段 fail-open)、10CG/aria-plugin#140 (`ssh '…'` / `sh -c '…'` 外壳)、10CG/aria-plugin#142 (`$(…)` / heredoc 内部)。被 W10 拦下时 `Triggering segment:` 回显替换后的副本还是原段不作规定 (回显经 `_sg_redact_echo` 脱敏, 风险有限)。

### W11 L1 进程表列举

- **现状**: 只拦 `/proc/(self|数字)/(environ|status|cmdline)` (`secret-guard.sh:930-933`); `ps` 完整命令行列、`pgrep -a`、`top -c`、`pstree -a`、`docker top` 全放行 (SC-22 0/41)。L3 对 `Authorization: token …` 与 `CF-Access-Client-Secret` 零告警 (SC-6 基线 0/8) ⇒ 今天 L1 是唯一预防层。
- **改动**: 新增进程表行 (命令位置锚定, 不用 `\b`), 拦暴露 argv 或 environ 的形态:
  - `ps`: 任意 BSD 选项簇 (不带 `-`, 如 `aux`、`e`、`eww`) 与 BSD pid 操作数 (`ps 123`: 输出 COMMAND 列 = 完整命令行, 22am)、SysV `-f` / `-F` 簇、`-o` / `--format` 列表含 `args|cmd|command`; `pgrep -a` / `--list-full`; `pstree -a` / `--arguments`; `top -c`; `docker top`; `docker ps --no-trunc`;
  - launcher 包裹 (`sudo doas nice timeout nohup stdbuf env time setsid ionice watch command exec`) 对以上全部生效 (22n); 远程与外壳包裹中出现的以上形态 —— `ssh`、`docker|podman|kubectl|lxc exec`、`nomad alloc exec`、`pct exec`、`sh|bash -c '…'`、`watch '…'`;
  - **同一批包裹下的整环境转储一并拦** (`nomad alloc exec … env|printenv`、`pct exec … -- env`、`ssh … env`): 这些包裹本 Spec 已为 `ps` 家族加进规则, 基线对 `docker|kubectl|podman|lxc exec … env` 已拦而这几个漏 (22ao–22ar); 只拦裸 `env` / `printenv`, `env FOO=1 cmd` 这种 `env` 作 launcher 的形态放行 (22at);
  - `/proc` 行放宽**只针对 `environ|cmdline`**: pid 位置接受任意 token (`*`、`$pid`、`${pid}`、`$(…)`) 与 `task/<tid>/` 子路径, 读取器补 `xargs sed grep egrep fgrep rg cut paste nl sort base64 cp dd` (22F–22I、22an); `status` 留在原窄行 (基线 `cat /proc/N/status` 被拦是既有轻度误报, 本 Spec 不动, 22aj; `grep VmRSS /proc/N/status` 这类只读元数据检查保持放行, 22as; 变异实测把 `status` 一并放宽的实现在 22as 转红);
  - credit 用 tight: `ps -ef | grep -v grep` 打印的仍是整行命令, 行级过滤不算 (22q–22s); `wc` 与 `>/dev/null` 保留 (22Y);
  - 放行只出 pid 或进程名的形态: `ps -e`、`ps -eo pid,comm`、`ps -p N`、`pgrep PAT` / `-f` / `-l` / `-fl` (Linux)、`pstree -p`、不带 `-c` 的 `top -b`、`docker ps` (22O / 22S / 22ad)。
- **处置**: 拒绝 (exit 2), 与现有 hook 一致, 复用同一份 BLOCKED 文案 (SC-25 25d)。
- **设计取舍**: **选 A** 拒绝。不选 B PreToolUse `updatedInput` 改写 (如把 `ps aux` 改成 `ps -eo pid,comm`): 静默改写使用者的命令违背其意图, 且现 hook 没有 JSON 输出路径 (只有 exit 2 + stderr); 另外采用方可能并存会改写命令的其它 hook, 那时「最后完成者生效」(`cc` 第 2 条) 有竞态 (本仓 Bash matcher 下现有两个 hook 都不产出 `updatedInput`, 所以这条不是本仓的现状理由)。不选 C `permissionDecision: ask`: 现 hook 没有 JSON 通道, 把判断转嫁给用户逐次确认与 ack 疲劳同形, 且无人值守的 Layer 2 容器里没有应答者 (`ask` 的 headless 行为未核验, 不依赖它)。
- **同族的进程环境读取**: 纳入 BSD `ps e` / `eww`、`/proc/*/environ` 与上面的包裹下 env 转储; 不纳入 `docker inspect <容器>` 全量 JSON (含 `.Config.Env`; 基线只拦带 `--format …Config.Env` 的)、`journalctl`、`nomad job inspect` —— 误报面未评估, 列 KNOWN-LIMIT (22ah) 并建议开单。
- **已知限制 (成文)**: `systemctl status` 放行 —— 暴露已验证 (`guard §2(d)`), 但它是最常用的健康检查, 误报代价高; W2 之后其输出里的 `Authorization: token …` / `CF-Access-Client-Secret` 由 L3 检出 (SC-6 6g 同形)。macOS 的 `pgrep -fl` 会输出完整命令行 (平台差异, 未实测), 本 Spec 按 Linux 语义放行。**新增误拦 (成文, 不钉测试)**: `ps axo pid,comm` 因 BSD 选项簇被拦; 取 PID 的惯用法 `ps aux | grep X | awk '{print $2}'` 被拦 (tight 下 awk `$N` 不算过滤), 改用 `pgrep -f X`。**Read 工具读 `/proc/<pid>/cmdline|environ` 两层都不拦** (22au; Read 面名单与 Bash 面名单不对齐是既有问题, 建议开单)。`sh -c 'printenv'` 这类外壳内的裸 `printenv` 仍放行 (基线同)。tight 族 (claude-config / `app.ini` / 进程表 / 扩展条目) 只认 discard / count / hash / 名字面 credit, 而共用 BLOCKED 文案的 Acceptable filters 列了 `| grep '^SAFE_PREFIX='` —— 对 tight 族该提示无效 (文案零改动, 见 W13)。

### W12 L1 两处误拦

**`os.environ` 单键读取被 `\.env` 命中**

- **现状**: `secret-guard.sh:893` (python3 -c)、`:894` (node -e)、`:974` (lua -e) 源组里的 `\.env` 无右边界, `os.environ.get(…)` 这类单键读取被拦 (SC-23 23a / 23b)。
- **改动**: 在 `_sg_judge_one` 匹配前, 若段含 `environ`, 把四个**单键读取**字面子串 `.environ.get(`、`.environb.get(`、`.environ[`、`.environb[` 各替换为不含 `.env` 的中性记号 (固定字符串替换, 两侧都是字面量), 再对替换后的副本跑全部 `risky_patterns`; BLOCKED 文案里的 `Command was:` 与 `Matched pattern:` 仍是原文 (SC-25 不变)。`\.env` 三行与其余几十行**不加任何右边界**。语义: `os.environ.get('X')` / `os.environ['X']` 与基线本就放行的 `os.getenv('X')` 是同一信息量 (取一个名字的值), 所以放行; **整表导出与遍历保持拦截** —— `print(os.environ)`、`dict(os.environ)`、`.items()` / `.copy()` / `.keys()`、`json.dumps(dict(os.environ))`、`os.environb`、`sorted(os.environ)`、`len(os.environ)`、与单键读取同现的整表导出 (SC-23 23c); `.env` / `.env.production` / `.envrc` / `.env_prod` / `.env2` / `.envprod` / `.envs/…` 经解释器读取**不得由拦变放** (SC-23 23d, 与基线一致)。
- **设计取舍**: **选 A** 单键读取归一化。不选 B 10CG/Aria#221 评论 25898 建议的 `\.env([^A-Za-z0-9_]|$)` (无论全局还是只改三行): 全局套到 39 行时 465 条探针里 108 条由拦变放, 含 20 条 `.envrc` 漏拦与 `cp .env /dev/stdout`、`scp .env user@h:` 这类「边界吞掉后面必需的空白」造成的真漏 (`guard §0` 第 4 条; SC-23 23e 钉住这些仍拦); 只改三行则把 `print(os.environ)` 这类整表导出一并放行 (等价放行 `printenv`, 而 `printenv` 与 W11 的 `ps e` / `/proc/*/environ` 都在拦) 并让 `.env_prod` / `.env2` / `.envs/` 经解释器读取由拦变放 (变异实测该写法在 SC-23 23c / 23d / 23h 转红)。不选 C 只豁免 `.environ` / `.environb` / `.environment` 三个标识符词元: 同样放行整表导出。
- **已知限制**: `os.environ['X']` 的单键读取现在放行 (含 `print(os.environ['FORGEJO_TOKEN'])`, 与基线放行的 `os.getenv` 同); `process.env.X` 仍被拦 (`.env` 后面是 `.`, 要靠预归一化; KNOWN-LIMIT SC-23 23f); `cfg.environment` / `x.env_file` 这类只是以 `.env` 起头的标识符仍被拦 (KNOWN-LIMIT 23h); `os.environ.setdefault(` / `'X' in os.environ` / `**os.environ` 等其它用法仍被拦。关联在案 issue: 10CG/aria-plugin#131 (既有 pattern 尾边界缺失 + FP 面) —— 本 Spec 对 `\.env` 的取向是「不加通用右边界、只归一化已证实无害的单键读取」, 可作为它的输入。

**jq 只出元数据的形态**

- **现状**: credit 词表 (`:427`) 已放行 `length` 与 `.X | length` —— 10CG/Aria#221 评论 25898 这一部分已过时 (SC-24 24l 基线即放行); 真正缺的是 `keys_unsorted` 与 `map_values(length)` (SC-24 24a–24e 基线 5/5 拦)。
- **改动**: 新增一条**锚定语法** credit: jq 程序必须带引号, 前缀只允许一个简单点路径加 `|`, 词后紧跟闭合引号, 词 ∈ {`keys_unsorted`, `map_values(length)`}; 不进 `:427` 的宽松词表。tight 模式下同样有效 (24e)。`keys[]` 保持拦截 (负向锚 `secret-guard.test.sh:841` 与 SOT 明文, 24f)。
- **设计取舍**: **选 A** 锚定写法。不选 B 把 `keys_unsorted` 加进 `:427` 词表: 该词表「词后只要是 `|` 就算、之后不受约束」, 实测研究原型对 `jq 'keys_unsorted | $ENV'` 放行 (会打印 jq 进程环境), 锚定写法仍拦 (SC-24 24f)。不选 C 纳入 `map(.name)` / `map(.key)`: 依赖「name / key 字段不是密」的数据假设 (KNOWN-LIMIT 24o)。
- **已知限制**: `map_values(length)` 对数值型字段**回显数值本身** (jq 的 `length` 对数字返回绝对值, 实测 `-4821` → `4821`), 「只出元数据」对数值字段不成立; Nomad Variable 的 Items 值恒为字符串, 不影响 10CG/Aria#221 的核对场景, 既有 `length` credit 同性质。既有洞 `jq '. as $d | keys | map($d[.])'` 基线放行 —— 本 Spec 不扩大也不修 (KNOWN-LIMIT 24p, 建议开单)。

### W13 拒绝文案零改动, 条款落 SOT

- **现状**: 10CG/Aria#221 建议在拒绝文案加一句「凭据不要放命令行参数, 改用 env / `--config` / stdin」。BLOCKED heredoc (`secret-guard.sh:1043-1071`) 被全部 145 行共用; 其处方性行自 2026-05-23 初版起未改过 (`prec §1.2`); `2026-08-02-secret-guard-nomad-var-put-echo` 的 Rule #6 可证伪锚点正是「heredoc 零改动」, 并明确拒绝过往共享文案里加专属内容, 按 pattern 给定向建议则转为 10CG/aria-plugin#132 (未初始化的 `$pattern_hint` 在 `set -u` 下会让全部 BLOCKED 文案崩溃)。
- **改动**: hook 文案零改动 —— SC-25: 三种既有 BLOCKED 文本归一化后与基线逐字节一致, 新增的进程表 / `app.ini` / 扩展 / Read 拦截复用同一文本。条款落 `secret-hygiene.md`, 并与同一 SOT 里**现有的** argv 示例对账:
  1. §2.5 加进程表行 (`ps` 完整命令行列 / `pgrep -a` / `top -c` / `/proc/<pid>/cmdline` 与 `environ`; SC-26 26b); §2.2 加 `app.ini` 一行 (26d); §5.1 勘正 (SC-28 28h); 新增 §5.6 (W9, 26c)。
  2. 新增 **§3.8「长时进程的凭据传递」**: 长时进程 (后台轮询 / 守护 / watch 循环, 存活期超过数秒) 的**命令行参数**不得含凭据, 改用 env / `--config` 文件 / stdin (SC-26 26a)。条款**精确限定适用面**: 短命令 (秒级) 的 argv 暴露窗口只在其执行期, §3.1 / §3.2 / §3.4 / §3.5 / §4.4 里把值放在 `KEY=…` 的示例属此类, **保持不变** —— SC-26 26h 钉住 §3.1–§3.7 与 §4.1–§4.4 逐字节等于基线, 新条款不会与既有正面示例自相矛盾 (10CG/Aria#221 的事故是后台轮询进程, 不是秒级写入命令)。能用 `@<文件>` 或 stdin 时同一凭据优先用它。
  3. 示例须逐工具实跑: `curl -K -` 从 stdin 读配置 (已实跑, curl 7.88.1: 从 stdin 配置读到 URL 后连接被拒 exit 7; 对照组无配置时 exit 2 `no URL specified`) 与 `curl -H @<文件>` (已实跑, 参数被接受); `nomad var put … KEY=@<文件>` 的 `@文件` 形 (nomad v1.11.2 `nomad var put -h` 写明「Item values provided from file references or stdin are consumed as-is」) 与其它工具的 env 写法 (如 `NOMAD_TOKEN`、`VAULT_TOKEN`) 在 B.2 实跑或以 `--help` 原文为据, 做不到就不写。
- **设计取舍**: 三个选项见「待 owner 复议」第 2 条: 选项 A 不改文案、只落 SOT (本 Spec 推荐) / 选项 B 全局共享文案加一句 / 选项 C 先解 10CG/aria-plugin#132 再做按 pattern 的定向提示。
- **已知限制**: 被拦的当下 AI 看不到这条建议 (它只在 SOT 里)。共用 BLOCKED 文案的 Acceptable filters 把 `| grep '^SAFE_PREFIX='` 列为可接受, 而 tight 族对它仍拦, AI 照文案重试仍被拦、会转向 `# guard:ack` (正是 10CG/Aria#221 评论 25898 批评的诱因); 这条不一致记入 SOT §2.5 末尾注与 hook 头注释 residual gaps, 并是第 2 条选项 C 的收益。

### W14 测试元耦合与同步

- **测试内 SC-13 头注释计数**: `secret-guard.test.sh:11` (`Coverage: 599 cases (593 without zsh)`, 断言 `:2018-2030`) 与 `secret-hygiene.md:23` / `:287` / `:319` 三处同步为实跑数 (权威值 = 带 git 历史的真 checkout 实跑, SC-30)。
- **测试内 SC-19 census**: `family_count` 硬编码 61 (`secret-guard.test.sh:1620` / `:1622`) 改为 census 实测值; 每个新增或改名的跨段族补 `# family='<精确 key>'` 探针 (10CG/aria-plugin#153 57→60、10CG/Aria#179 60→61 先例); 改 `/proc` 读取器行开头的分组会让该族 key 改名 (原型实测 61 → 64, 须补探针的三个族: `/proc` 放宽行、其 `<` 重定向行、外壳包裹行); 新行不得整行只由 `"${VAR}"` 组成 (census 在不带前置变量的 bash 里求值, 这类行是空串; SC-31 31c) —— 所以 W11 若用变量拼规则行, 须内联成字面行。
- **性能预算**: 测试内 SC-8 五档每次调用 ≤ max(100ms, 改前 × 1.5) —— 既有闸门, owner 2026-08-24 裁定, 不改阈值、口径、档位 (SC-30)。结构预算: `risky_patterns` 静态行 145 → 不超过 150 (SC-31 31a; W8 一行 + W11 三行 = 149, `/proc` 两行原位改写); 变量展开只在「段含 `$` 且收集到赋值」时触发。**新路径另设三个时档** (SC-30 的一部分, 沿用测试内 SC-8 的计时器与 `max(100 ms, 改前 × 1.5)` 口径, 「改前」= 基线 `268da8f` 的 hook; 不改测试内 SC-8 的五档与阈值): (f) 200 条扩展条目 × 单段 benign 命令; (g) 9.5 KB 整串、8 个赋值 + 40 个 `$VAR` 引用; (h) 600 段 `echo` + 末段 `cat .env`: 必须仍 exit 2, 耗时 ≤ 改前 × 1.5 **且** < 5 s (`hooks.json` 超时即放行, 而基线 600 段已 3.8 s, ×1.5 会越过超时; 内建先判, 不被扩展 / 替换推迟)。本 Spec 原型实测 (Linux, 单次进程调用, 每格 5 次取最小、三轮再取最小; 共享主机负载 1.5–3.1, 单轮数字有 ±20% 噪声), 基线 / 无扩展 / 200 条扩展: 单段 48 / 54 / 62 ms, 4 段最坏档 76 / 91 / 99 ms, 整串赋值 59 / 101 / 119 ms, 600 段 3.83 / 4.43 / 4.34 s (基线本身已逼近 5 s 超时, 见建议开单第 1 条)。L3 预算: 180 KB 级稠密 INI 输入单次 ≤ 2.5 s (`hooks.json` `timeout: 5` 的一半; 原型两次实测 0.8 s 与 1.2 s), B.2 实测记录。
- **其它耦合**: 测试内 SC-20 注入自测依赖的两段文本 (`_sg_compute_credit` 里 `wc` 那段、`local nl=$'\n'`) 逐字节不变; hook 源码不出现 `(?:` (测试内 SC-16); 用例名不重复 (测试内 SC-17); 新增 jq 取值点带 CR 剥离 (`VAR="${VAR%$'\r'}"` 须另起一行, 同行分号拼接过不了 jq-crlf-guard) 或 `# crlf-ok` (SC-29 29g); 新辅助函数放在 source 闸门之上, 并跑一次测试内 SC-20 风格的未绑定变量注入自测 (W10 的新代码在 fail-closed 子 shell 内, 任何未绑定变量都会让**所有** Bash 命令 fail-closed; W9 的扩展代码则故意隔离在命令替换里, 同样的故障只丢扩展, SC-20 20i–20k)。
- **secret-scan 计数**: `secret-scan.test.sh` 新增头注释 `Coverage: K cases` 与测试内 SC-13 同款的自检 (现在 `secret-hygiene.md:288` 的 49 没有任何机械断言; SC-27 27b / 27c)。
- **陈旧 / 悬空表述** (SC-28; 每条验「旧文本消失且替换文本在场」, 删句不算): `secret-guard.sh:21-23`「Phase 2 would add PostToolUse hook … + redacts」与 `:62` 悬空的 `docs/operations/secret-rotation-runbook.md` (改指 `secret-hygiene.md`); `secret-scan.sh:15-20` 的「exposes no field to replace tool_response … not a version-dependent behaviour」(与本 Spec 的二进制实测直接矛盾, 改为「schema 里有 `updatedToolOutput`, 端到端未验证, 本 hook 不使用」; 其余「cannot redact」表述随「待 owner 复议」第 1 条统一订正)、`:33-34` 的 `49 known bypass classes` / `~15 secret-shape patterns` (删除, 且**不得**在头注释里写新的 pattern / 类别总数字面)、`:52` 不存在的 argon2、`:72-80` hook contract 里的旧 Read 形状、`:64`「base64 / hex 无前缀」非目标声明 (改为「无前缀且无凭据键名」); `secret-hygiene.md` §5.1 把 secret-guard 称作 Write/MultiEdit blocker (`secret-guard.sh:698-700` 对二者直接 exit 0); `aria/VERSION:164` 的「output REDACT」; 两个 hook 的头注释记本 change-id。

## Out of scope

- **凭据轮换** (决策单第 2 项): 本 Spec 不产出轮换清单、不涉及任何具体凭据、不逐条提示轮换。
- **WP-B** (10CG/Aria#223 + 10CG/aria-plugin#207) 与 **10CG/Aria#199** 本身。
- **L3 升级为「检测 + 脱敏」(`updatedToolOutput`)**: 产品级 (模型将看不到被脱敏的正文)、端到端未验证、要推翻 `DEC-20260703-001`。本 Spec 保持检测 + 告警, 只保证检测核心 (提取 + tag + 分类器) 日后可被脱敏模式复用; 选项见「待 owner 复议」第 1 条。在 PostToolUse 无法改写内置工具输出这一平台前提下的「撤回」能力 (值已进上下文) 不在范围。与之相关的既有陈述 (README 两语种、`secret-hygiene.md` §5.2 等「cannot redact」) 本 Spec 不改, 随第 1 条的复议结论统一订正; 唯一例外是 `secret-scan.sh` 头注释里与二进制实测直接矛盾的那一句 (W14, SC-28 28l)。
- **Edit / MultiEdit 结果扫描**: Edit 的结果给模型的只是一句成功提示, 不回显内容 (`scan §1.2`), 值本来就在模型自己写的 `tool_input` 里, 不构成「经工具输出进入模型上下文」的泄露; MultiEdit 真实形状 0 样本。
- **既有缺陷** (研究新发现, 非三个 issue 所诉) 与 matcher 缺 Grep / PowerShell、飞书 webhook URL / Nomad-Consul `SecretID` 等未覆盖形状: 见「待 owner 复议」第 7 条建议开单清单。
- **aria-doctor 对扩展文件的校验** (W9 已知限制): 属 Skill 改动, 另开单。

## Success Criteria

> **类别** (机读枚举, 英文 canonical): `baseline-failing` = 基线不符、目标相符 (RED → GREEN); `reverse-guard` = 基线与目标都保持拦截 / 检出 / 一致 (防回退); `allow-guard` = 基线与目标都保持放行 / 静默 (误报守卫); `known-limit` = 钉住已知不覆盖的现状, **该行转红 = 已收口, 须同步更新本 SC 与对应「已知限制」**; `zero-regression` = 全量既有测试, 只承担「无外溢」, 不作功能正确的证据; `doc-sync` = 文档同步。
>
> **测的是哪份副本** (10CG/Aria#178): 全部 SC 测的是**仓内 canonical hook 的直调** (`bash <aria>/hooks/secret-*.sh`), 不是插件缓存里的副本、也不是 harness hook 链; harness 链复验是 ship 后的一次性动作 (Tasks 1.10)。
>
> **判定命令**: 全部由同目录 `baseline_probe.py` 执行 (`python3 baseline_probe.py <aria 仓路径>`; SC-30 除外; 可选环境变量 `WPA_BASH32=<真 bash 3.2 路径>` 打开 SC-29 29h / 29i 与 SC-32 32c, 缺省时这三行打印 `not-run`、match 为 `n/a`)。L3 行: 把「输入形态」按注明的信封 (默认 Bash 真实信封) 构造成 JSON, 经 stdin 喂 `bash hooks/secret-scan.sh`, 判据 = exit 0 + stdout JSON 的 `additionalContext` 是否非空 + `systemMessage` breakdown 的 tag 与计数**恰好**等于期望 (`any` = 有告警即可)。L1 行: `{"tool_name":"Bash","tool_input":{"command":<命令>}}` (Read / Edit 行用 `file_path`) 经 stdin 喂 `bash hooks/secret-guard.sh`, 判据 = 退出码。**多用例行** 是同一类别下若干独立 hook 运行的 AND, `actual` 列逐个列出, 红了仍能指出是哪一个。像凭据的值全部运行时生成; 默认生成器从不以 `/ . ~ < $ * { [ " ' + = - _` 开头, 首字符敏感的行 (SC-4 4n、SC-5 5l / 5m、SC-7 7h) 用强制首字符生成器。每个用例的输入形态、期望、基线实得逐行见 `baseline-evidence.md` (共 320 行, 其中 SC-30 一行不执行)。
>
> **基线形态自检**: 探针在基线上的输出必须是「`baseline-failing` 与 `doc-sync` 行全部 `no`、其余类别全部 `yes`」, 实跑成立 (证据末尾两行); 目标态必须是「全部行 `yes`」。**三态**: 每个新增或改写的行都在基线、在按本 Spec 实现的原型、在至少一个像真实坏情形的变异实现上跑过 (变异结果在各 SC 的「怎么会红」里点名; 实现期由 Tasks 1.8 的非作者对抗 review 复核)。

**L3 (`secret-scan.sh`)**

- **SC-1** (`baseline-failing` ×2, W1): Read 真实信封, 内容为 `AWS_ACCESS_KEY_ID=<AKIA+16>` / json:client_secret=<32 alnum> → 期望 `aws-access-key-id=1` / `json-secret-field=1`。**基线 2/2 静默**。怎么会红: 提取链没加 `file.content` 或加错层级。
- **SC-2** (`reverse-guard` ×4, W1): 同内容经 Read 旧合成信封 / Bash 真实信封 / Bash 旧 `{output}` 信封 / Write 真实信封 → 仍检出。**基线 4/4 相符**。怎么会红: 改提取链时破坏既有分支。
- **SC-3** (`known-limit` ×2, W1): Edit 真实信封、字符串形 `tool_response` → 静默。**基线 2/2**。怎么会红: 有人扩了扫描面 (须同步本 SC 与 Out of scope)。
- **SC-4** (`baseline-failing` ×15, W2): 08-20 事故形 (json:token=<40 hex>) 及冒号后带空格 / 多行美化 / `sha1` / `registration_token` / `jwt_secret` / `auth_token` / 首字母大写 / camel / Pascal 键 / 完整 Forgejo 建 PAT 响应 (含 `token_last_eight`, 只计 1) → `json-credential-field=1`; 大写环境变量键 (`Env` 映射) → `json-env-secret-key=1`; 4n 以 `/` 开头的 44 位 std-b64、4o 40 位无数字的大小写字母 → `json-credential-field=1`。**基线 0/15**。怎么会红: 名表缺项、拼写变体没覆盖、值长门槛写错、`token_last_eight` 被误计、路径形写成「任何 `/` 开头」(4n)、熵下限写成「必须含数字」(4o)。
- **SC-5** (`baseline-failing` ×13, W2): `JWT_SECRET = <44 std-b64>` (10CG/aria-plugin#203 原形) / `<43 b64url>` / `SECRET_KEY` / `PASSWD` / `LFS_JWT_SECRET` / `export API_TOKEN=` / dotenv 双单引号 / 缩进 YAML 冒号形 → `kv-secret-assign=1`; `app.ini` 片段 (5 个凭据, 其一为 JWT 形) → `jwt=1 kv-secret-assign=4`, `matches=5`; 5l 以 `/` 开头的 44 位 std-b64; 5m 43 位 b64url 以 `-` / `_` 开头。**基线 0/13**。怎么会红: 等号两侧空白、引号、`export`、冒号任一形态没覆盖, JWT 值被两个 tag 重复计数, 路径形写宽 (5l), 首字符处理漏掉 `-` `_` (5m)。
- **SC-6** (`baseline-failing` ×8, W2): `Authorization: token <40 hex>` / curl 命令回显里的同一头 / `CF-Access-Client-Secret: <64 hex>` / curl 回显的 Client-Id + Secret 头对 (期望只计 Secret) / `Authorization: Basic <b64>` → `auth-header-token=1` 或 `cf-access-client-secret=1`; `--token=<40 hex>` → `cli-secret-flag=1`; 进程表行 (10CG/Aria#221 原形) → 两个 tag 各 1; 6h HTTP/2 小写头名两例。**基线 0/8**。怎么会红: 头名大小写、值字符类或 Client-Id 被误计。
- **SC-7** (`reverse-guard` ×9, W2 / W3): 行首 `JWT_SECRET=<44>` 仍为 `env-line-secret-keyword=1`; `INTERNAL_TOKEN = <JWT>` 仍为 `jwt=1`; `Authorization: Bearer <32>` 仍为 `bearer-token=1`; json:client_secret / json:password 仍为 `json-secret-field=1`; 行首 `DB_PASSWORD=<20>` 仍为 `env-line-secret-keyword=1`; json:token=<gh 前缀 PAT> 仍只计 `github-pat=1`。**7h (检出不得被悄悄收窄的负向侧)**: 既有键上的 crypt 口令哈希 / `$` 开头的 20 位 / `<` 开头不闭合的值 / 12 位纯小写 / 标记词在值中间 / 小写 `fake_` 开头, 以及 `SVC_API_KEY=FAKE_…` 行首赋值 → 各自仍是 `json-secret-field=1` / `env-line-secret-keyword=1` (七个独立运行); **7i** json:token=<crypt 哈希形> 仍须有告警 (基线 `bcrypt-hash=1`, 新 json tag 不得静默吞掉它)。**基线 9/9**。怎么会红: 新 tag 排序在前抢走既有 span; 白名单写成 `<` / `$` / `{{` 单字符前缀 (7h / 7i)、「含」(7h)、大小写不敏感 (7h)、套到 `env-line` (7h); 熵下限套到既有 json 键 (7h) —— 上述各写法均做过变异实测, 转红的行如括号所示。
- **SC-8** (`baseline-failing` ×1, W3): json:api_key=<anthropic 前缀 key> → 期望 `anthropic-api-key=1`, `matches=1`。**基线 `matches=2`** (哨兵回灌)。怎么会红: 白名单没延伸到 `json-secret-field`, 或哨兵整值占位规则缺失。
- **SC-9** (`allow-guard` ×23, W2): 通用键形在非凭据上静默 —— 尖括号 / `$(…)` / `${…}` 占位、空值、只含键名的 grep 命令、git 提交 sha、`commit.id`、`token_last_eight` (**24 位值**, 钉键名封闭性)、UUID、`next_page_token`、完整 git log、`Authorization: token $FORGEJO_ADMIN_API_TOKEN` 与 `--token=$RUNNER_REGISTRATION_TOKEN` (**24 / 25 字符的变量引用**, 只有值规则能让它们静默)、`/run/secrets/…` 路径值、单字符类名字形值、`export SECRET_GUARD_ACK_PATH="<路径>"`、散文、镜像 digest、Actions `${{ secrets.X }}`、`--password-stdin`; **9v** 从环境 / 配置读取凭据的代码 (`const JWT_SECRET = process.env.X`、`SECRET_KEY = settings.X`、`API_TOKEN = config.getApiToken…`); **9w** 值是文件路径的赋值 (`/Users/…`、`~/Library/…`)。**基线 23/23**。怎么会红: 熵下限、路径形、点分标识符链排除、名表封闭性或值字符类任一写宽 (变异实测: 去掉标识符链排除 → 9v; 去掉路径形 → 9o / 9w; 路径形写成「首段小写」→ 9w)。
- **SC-10** (`known-limit` ×7, W2): json:token=<40 纯小写>、`JWT_SECRET = <24 纯数字>`、json:token=<12 alnum> (短于 16)、YAML 小写键 `password: <16>`、`--token <40 hex>`、json:SecretAccessKey=<40>、10g (三个独立运行: python repr 单引号 dict; 值里 3 个字符后即出现符号的赋值; 转义引号的 JSON-in-JSON) → 静默。**基线 7/7**。怎么会红: 有人覆盖了该类 (须同步更新已知限制)。
- **SC-11** (W3, 两面): 新 tag 放行侧 (`allow-guard` ×12): FAKE_ 前缀 / PLACEHOLDER / NOT-REAL- / L2 wrapper 占位 / 尖括号占位 / `${…}` / `{{ … }}` / 16 个 `*` 作 json:token 的值, wrapper 占位作 json:sha1 的值, 赋值形 FAKE_、`Authorization: token` 的 FAKE 值、`--token=` 的 PLACEHOLDER 值 → 静默 (**基线 12/12**; 基线静默是因为这些键根本没被覆盖, 所以放行侧只有与 SC-4 / 5 / 6 的同形正例成对才有鉴别力); 既有键误报修复 (`baseline-failing` ×6): json:password / client_secret / api_key 上的 FAKE_、PLACEHOLDER_VALUE、NOT-REAL-、`[REDACTED]`、8 个 `*`、wrapper 占位 → 静默 (**基线 6/6 告警**); **11v** (`baseline-failing` ×1, 四个独立运行): 既有键上的**文档式占位**静默 —— 含 `$` 的尖括号说明文字、`$2b$12$` 加省略号的截断哈希、`${VAR}`、`{{ template }}` (**基线 4/4 告警**; 这些值在探针里运行时拼装, 因为探针文本本身必须对基线 hook 静默); 标记不在值首 (`baseline-failing` ×1): json:token=<16 alnum + FAKE + 16 alnum> → `json-credential-field=1`; **11w** (`baseline-failing` ×1): 250 个值为 16 个 `x` 的赋值 → 前 200 个 span 被分类并放行、超出部分不分类照计, 期望 `kv-secret-assign=50`; 真阳性仍检出 (`reverse-guard` ×2): json:password=<12 alnum + !> 仍为 `json-secret-field=1`, 正文以 FAKE 开头的 gh 前缀 PAT 仍为 `github-pat=1` (provider tag 不套白名单), **基线 2/2**。怎么会红: 白名单写成「含」而非「整值形态 / 开头」、延伸到 provider tag、漏掉 wrapper 占位、漏掉截断标记 (11v)、没有 200 个 span 的上限 (11w)。
- **SC-12** (W4): (`baseline-failing` ×7) 12a json:client_secret=<32> → 日志第 9 字段恰为 `fp=<sha256(值) 前 8 位>`; 12b json:password=<12> → 恰为 `fp=L12` 且日志不含该值的哈希; 12c 在 PATH 里去掉 `sha256sum` 与 `shasum` → 恰为 `fp=-` 且日志照写; 12g / 12h / 12i / 12j 见 W4。**基线 7/7 无 `fp` 字段**。(`reverse-guard` ×3) 12d–12f: 同两例加 `app.ini` 片段, 日志恰 1 行, 日志 / stdout / stderr 里没有任何值或值的首末 8 字符片段。**基线 3/3**。怎么会红: 指纹取了整个 span 或加了盐、短值也记了哈希、缺工具时不写日志、值或片段落进任一输出、非 JSON tag 取了含键名的 span 或整 span (12g / 12j; 变异实测整 span 写法在 12g / 12h / 12i / 12j 转红)、遍历序写成文本序 (12h)、没有 10 项上限 (12i)。
- **SC-13** (W5): (`baseline-failing` ×3) additionalContext 含 `(tags: aws-access-key-id=1; source: Read /x/app.ini)` / `(tags: json-secret-field=1; source: Bash)` / `(tags: aws-access-key-id=1; source: Write /x/f.txt)`。**基线: Read 例静默 (读取失明), 另两例告警但无 tag 与来源**。(`reverse-guard` ×3) 13d 删去 ` (tags: …; source: …)` 段后的 additionalContext **与基线文本全串逐字节相等**; systemMessage 格式不变; exit 0 且 stdout 键集恰为 `{hookSpecificOutput{hookEventName, additionalContext}, systemMessage}`、不回显值。**基线 3/3**。怎么会红: 改了处方句、**在插入段之外追加任何句子** (只判「处方句仍在」的写法对此恒绿, 13d 为全串等值)、把值或命令写进告警、输出了改写类键。
- **SC-14** (`baseline-failing` ×2, W6): 以外层 HOME 跑 `secret-scan.test.sh` → 外层 `secret-scan.log` 新增 0 行; 跑 `secret-guard.test.sh` → 外层 `guard-bypass.log` 新增 0 条事件。**基线 33 行 / 12 条**。怎么会红: 任一套件没隔离 HOME, 或隔离发生在第一次调用 hook 之后。
- **SC-15** (W7 / W3): 文件文本当 Bash 输出扫 —— `hooks/tests/secret-scan.test.sh` (`baseline-failing`) 期望静默, **基线告警 `matches=33`**; `hooks/tests/secret-guard.test.sh`、`hooks/secret-scan.sh`、`hooks/secret-guard.sh`、本 Spec 的 `proposal.md`、`baseline_probe.py` (`allow-guard` ×5) 期望静默, **基线 5/5**。基线只证明现行 hook 不误报; 新 tag 上线后 15e / 15f 是否静默要到 B.2 才有鉴别力, Tasks 1.10 验收须点名它们。怎么会红: 夹具没拼装干净; 新模式在 hook 源码、测试源码或本 Spec 的占位写法上误报。

**L1 (`secret-guard.sh`)**

- **SC-16** (`baseline-failing` ×13, W8): 十一个形态 —— `sed -n '1,80p'` / `cat` / `head` / `grep -n JWT_SECRET` / awk 区间 / python3 -c 读取 `app.ini` (`/etc/forgejo`、`/etc/gitea`、`custom/conf`、`/data/gitea/conf`、`/var/lib/forgejo/custom/conf`)、`cat … | grep '^JWT_SECRET'` (tight)、`ssh root@pve 'pct exec 101 -- cat …'`、`docker exec forgejo cat …` —— 加 16l `cat /srv/git-forgejo/app.ini` (词内前缀)、16m `cat /etc/forgejo/app.ini.bak` (备份) → exit 2。**基线 0/13**。怎么会红: 名字组漏某一路径形态、读取器组漏某个读取器、tight 没并入、左前缀只认词首 (16l)、右边界把 `.` 当词内 (16m)。
- **SC-17** (W8): 17a (`allow-guard`, 10 条命令一行): `chmod 600 …/app.ini` (左边界)、`ls -l`、`systemctl restart forgejo`、`grep -rn 'app.ini' docs/`、`/opt/myapp/app.ini`、`php.ini`、`git log -- custom/conf/app.ini`、`… | wc -l`、`sha256sum`、`cp` → exit 0, **基线 10/10**; 17b (`known-limit`) `cp …/app.ini /tmp/x && cat /tmp/x` → exit 0。怎么会红: 新行缺左边界、名字组退化成裸 `app.ini`、tight 把 `wc` 也收掉。
- **SC-18** (W8): Read `/etc/forgejo/app.ini`、Read `/var/lib/gitea/custom/conf/app.ini`、Edit `/etc/gitea/app.ini`、Read `/data/gitea/conf/app.ini` (`baseline-failing` ×4) → exit 2, **基线 0/4**; 18f (`baseline-failing`) 设了 `SECRET_GUARD_ACK_PATH` 但无 nonce 标记 → 仍 exit 2; 18e / 18g (`allow-guard`) Read 其它应用的 `app.ini` / `php.ini` → exit 0, 带有效一次性 ACK 的 Read → exit 0。怎么会红: `:641` 只改了 Bash 面, 名字组两面漂移, 或新拦截绕开了 nonce 逃生口。
- **SC-19** (W9, `CLAUDE_PROJECT_DIR` 指向含 `.aria/secret-guard.paths` 的临时项目): (`baseline-failing` ×12) 列入的路径被 `cat` / `grep … | grep -v` (tight) / Read / Edit 读取、只给 stdin `cwd` 时的回落、经变量间接 (19i)、**14 个各含一个 `\ ^ $ . | ? * + ( ) [ ] { }` 的条目逐个被字面拦下** (19j)、CRLF 文件、`python3 -c` 读列入路径 (19o)、**大小写不敏感** (Read 大写路径 / 含大写的条目 / 混合大小写命令, 19p)、同一命令里第一处出现在非读取器之后而第二处在读取器之后 (19r)、Read 带 ACK 但无 nonce 仍拦 (19s) → exit 2, **基线 0/12**; (`allow-guard` ×5) `… | wc -l` 与 `ls -l`、`CLAUDE_PROJECT_DIR` 与 `cwd` 冲突时以前者为准、**把条目里的 `. * ? + | (` 当模式字符才会命中的 6 个相似路径放行** (19k)、3 字符条目被忽略、Read 带有效一次性 ACK (19t) → exit 0, **基线 5/5**; (`reverse-guard` ×1) 文件里写 `!.env` 时 `cat .env` 仍 exit 2。怎么会红: 条目当正则 / glob 用 (变异实测 `grep -E` 实现在 19j 转红)、没剥 CR、回落顺序颠倒、扩展能放宽内建规则、条目没小写化 (19p)、只在第一处出现判读取器 (19r)。
- **SC-20** (W9, 扩展失败只丢扩展 + 隔离 + 求值顺序): (`reverse-guard` ×6) 六种坏文件 (缺失 / 是目录 / 悬空软链 / 含 NUL / 超过 32 KiB / 201 条) 各一行、一行四条命令: 列入的路径 `cat` 与 Read 放行、`cat .env` 与 Read `/x/.env` 仍拦, **基线 6/6**; 20g 不可读 (`chmod 000`; root 运行时不可构造, 打印 `not-constructible`, match 为 `n/a`)。鉴别力来自与 SC-19 成对: 坏文件若导致 fail-closed、被部分采用 (截断到 200 条, 变异实测 20f 转红) 或误判, 放行或拦截行即转红。**20h** (`baseline-failing`): 满是未配对 `( [ \ * ?` 的条目文件里有效条目仍被拦、无关路径仍放行 (组合正则实现转红)。**20i–20k** (`reverse-guard` ×3): 在**每个** `_sg_ext_*` 函数首句注入 `exit 1` / 未绑定变量 / `return 1`, 五条金丝雀 (`cat .env`=2、`ls -la`=0、Read `/x/.env`=2、Read `/x/README.md`=0、Edit `/x/.env`=2) 不得变 (裸调用扩展代码的实现: 主 shell 里 exit 1 = Read 放行, fail-closed 子 shell 里 = 全部 Bash 被拦, 变异实测 20i / 20j 转红); **20l** (`reverse-guard`) 内建拦的命令里扩展入口一次都不被调用; **20m** (`baseline-failing`) 内建放行且扩展文件存在时两个入口都被调用 (无死代码)。基线上没有 `_sg_ext_*` 函数, 20i–20l 的注入是空操作、守卫恒绿 (鉴别力由变异实现给出), 20m 在基线红。
- **SC-21** (W10): (`baseline-failing` ×9 = 八条命令 + 21w) `f=/etc/forgejo/app.ini; sed -n '1,80p' "$f"`、`f=~/.bashrc; cat $f`、`F=… && cat "$F"`、`export CONF=…; cat $CONF`、事故原形 `ssh root@pve 'pct exec 101 -- sh -c "f=…/app.ini; sed -n 1,80p \$f"'`、链式 `d=…; f=$d/app.ini`、`${f}`、`for f in …` → exit 2, **基线 0/8**; 第 9 行 21w: 全部内建放行时第二遍被调用 (`_sg_vx_pass`), **基线未调用**; (`allow-guard` ×1, 五条命令) `ls -l "$f"`、`export KUBECONFIG=…; kubectl get pods`、`cp $f /tmp/x`、`for f in *.txt`、普通变量 → exit 0, **基线 5/5**; (`known-limit` ×8) W10 已知限制各一 → exit 0, **基线 8/8**; (`reverse-guard` ×1) 21v `f=/etc/hosts; cat "$f"; cat .env` → exit 2 且第二遍一次都不运行。怎么会红: 展开没覆盖 `export` / 引号值 / `\$` / `for` 形式, 展开后改用「赋值即拦」, 第二遍按段交错 (21v 转红, 变异实测), 或展开用了 `${x//p/r}` (SC-32 32c 在真 bash 3.2 上转红)。
- **SC-22** (W11): (`baseline-failing` ×41) `ps` 的 `aux` / `-ef` / `auxww` / `-eo pid,args` / `-o pid,command` / `-ww -fp` / `eww` / `e` / `-C … -o args=` / `--format pid,cmd`; `pgrep -af` / `-a` / `--list-full` / `sudo pgrep -af`; `pstree -ap`; `top -b -n1 -c`; `ps aux | grep curl` / `ps -ef | grep -v grep` / `ps aux | grep '^dev'` (tight); `docker ps --no-trunc`、`docker top`; 包裹与外壳 (`ssh host 'ps aux'`、`x=$(ps aux)`、`sudo ps -ef`、`watch -n 5 ps aux`、`watch -n1 'ps aux'`、`sh -c 'ps aux'`、`bash -c "ps -ef"`、`pct exec`、`kubectl exec`、`nomad alloc exec`); `/proc` 放宽形态 (`*`、`$pid`、`xargs -0 -a`、`environ`); 22am `ps 123`; 22an `cat /proc/1/task/1/environ`; 22ao–22ar 四条包裹下的 env / printenv → exit 2, **基线 0/41**; (`reverse-guard` ×1, 五条命令) 既有 `/proc/N/{cmdline,environ}` 的 `cat` / `tr <` / `cat self` / `strings` → exit 2, **基线 5/5**; (`allow-guard` ×6) 只出 pid / 状态 / 进程名的 `ps` 形态 (22O)、`pgrep` / `pstree` / `top` 的 pid-名字形态 (22S)、文本里提到 `ps aux` 与 `| wc -l` / `>/dev/null` / `man ps` (22Y)、`docker ps` 与 `/proc/N/comm` / `cpuinfo` (22ad)、**`grep VmRSS /proc/N/status` 等只读元数据 (22as)**、**exec 包裹下不转储的命令与 `env FOO=1 cmd` (22at)** → exit 0, **基线 6/6**; (`known-limit` ×3) 22ah (四条: `systemctl status` / `show -p ExecStart`、`docker inspect`、`journalctl` → exit 0)、22aj (`cat /proc/N/status` → exit 2)、22au (Read `/proc/…` 三个路径 → exit 0), **基线 3/3**。怎么会红: `ps` 选项簇判定过宽 (误拦 comm 形态) 或过窄、命令位置锚丢失 (误拦文本提及)、外壳 / launcher 包裹未覆盖、没用 tight、`/proc` 放宽连 `status` 一起放宽 (22as 转红, 变异实测)。
- **SC-23** (W12 `os.environ` 单键读取): (`baseline-failing` ×2) 23a 10CG/Aria#221 评论里的原始多行 `nomad alloc exec … python -c` 读 `os.environ.get('DATABASE_URL')` → exit 0; 23b 四条单键读取 (`.get(`、`['X']`、`.environb.get(`、一条命令里多处) → exit 0, **基线 2/2 exit 2**; (`reverse-guard` ×3) 23c 十条整表导出 / 遍历 / 与单键读取同现的导出 (含 `printenv` 对照) → exit 2; 23d 九条经解释器读 `.env` 家族 (含 `.env_prod` / `.env2` / `.envprod` / `.envs/…`、node / lua) → exit 2; 23e 六条非解释器读取器 (`head .envrc`、`tail -n 5 .envrc`、`cp .env /dev/stdout`、`scp`、`rsync`、`strings .envrc`) → exit 2, **基线 3/3**; (`known-limit` ×3) 23f `node … process.env.HOME` → exit 2; 23g `cat .env_prod` → exit 0; 23h `cfg.environment` / `cfg.env_file` 一类 → exit 2, **基线 3/3**。怎么会红: 给 `\.env` 加了右边界 (23c / 23d / 23h 转红, 变异实测)、归一化吃掉了整表导出、漏了 `.environb`。
- **SC-24** (W12 jq): (`baseline-failing` ×5) `… | jq '.Items | map_values(length)'`、`jq 'keys_unsorted'`、`jq -r '.Items | keys_unsorted'`、`nomad var get … | jq '.Items | map_values(length)'`、claude 配置 (tight) 上的 `map_values(length)` → exit 0, **基线 5/5 exit 2**; (`reverse-guard` ×1, 六条) `keys[]`、`. as $d | map_values(length) | $d`、`keys_unsorted | $ENV`、`.Items`、`map_values(tostring)`、`map_values(length), .` → exit 2, **基线 6/6**; (`allow-guard` ×1, 三条) `length`、`.Items | length`、`keys` → exit 0, **基线 3/3**; (`known-limit` ×2) `map(.name)` 与 `map(.key)` → exit 2、既有洞 `. as $d | keys | map($d[.])` → exit 0, **基线 2/2**。怎么会红: 新词进了宽松词表 (24f 转红)、锚定写法没要求闭合引号、tight 模式下没生效。
- **SC-25** (W13): (`reverse-guard` ×3) `cat .env` (分段模式)、`x=$(cat .env)` (整串模式)、Read `/x/.env` 的 BLOCKED stderr, 归一化 (`Matched pattern:` / `Command was:` / `Triggering segment:` / `Path:` / `Blocked:` / ack 路径的动态部分替换为占位) 后 sha256 前 16 位等于基线常量, **基线 3/3**; (`baseline-failing` ×4) `ps aux`、`cat /etc/forgejo/app.ini`、扩展条目、Read `/etc/forgejo/app.ini` 被拦时的文本同样等于基线常量, **基线 4/4 未拦 (无文本)**。怎么会红: 改了 heredoc, 或为新拦截另写文案。

**文档、回归与结构**

- **SC-26** (`doc-sync` ×7 + `reverse-guard` ×1, W13 / W9 / W14): 每条判据**限定在具体小节内** (「全文件任一行」的写法会被版本历史行单独满足): 26a `secret-hygiene.md` §3.8 内有一行同时含「命令行参数」「env」「`--config`」「stdin」且含「长时」或「存活期」; 26b §2.5 内有一行含 `pgrep -a`; 26c §5.6 内含 `.aria/secret-guard.paths`、字面子串、只增不减、32 KiB、200、整体忽略; 26d §2.2 内有一行含 `app.ini`; 26e aria `README.md` 与 `README.zh.md` 的 Hooks 用法小节各含 `.aria/secret-guard.paths`; 26f `secret-guard.sh` 头注释前 140 行含扩展文件名与两个代表性残余缺口 (`systemctl status`、`docker inspect`); 26g `aria/CHANGELOG.md` 最上一节含 `rule6_note`、`.aria/secret-guard.paths`、`ps aux`; **26h** (`reverse-guard`) §3.1–§3.7 与 §4.1–§4.4 逐字节等于基线。**基线 doc-sync 0/7**。怎么会红: 条款或进程表行没落 SOT; 把内容塞进版本历史表 (变异实测: 其余文档照常落地, 但 SOT 里只往版本历史表追加一行含全部关键词的行 → 26a–26d 与 28h 转红); 改了 §3 的既有示例。
- **SC-27** (W14): (`reverse-guard`) `secret-hygiene.md` 三处计数等于 `secret-guard.test.sh` 头注释的 `N` / `M`, **基线 3/3 一致 (599 / 593)**; (`doc-sync`) `secret-scan.test.sh` 头注释 `Coverage: K cases` 存在且等于实跑总数, **基线缺席**; (`reverse-guard`) `secret-hygiene.md` 的 secret-scan 计数等于该套件实跑总数, **基线一致 (49)**。怎么会红: 增删用例后没回填头注释或 SOT。
- **SC-28** (`doc-sync` ×12, W14): W14 所列陈旧 / 悬空表述各一行 (28a–28i、28l), 判据 = 旧文本消失**且**替换文本在场 (28c / 28d 另要求头注释不再出现任何 pattern / 类别总数字面), 加两个 hook 头注释含 change-id (28j / 28k)。**基线 0/12**。怎么会红: 同步面漏改、整段删掉不写替换、把计数句换成新的字面数字。
- **SC-29** (`zero-regression` ×9): 在不带 `.git` 的私有副本上 (zsh 从 PATH 隐去) 跑 `secret-scan.test.sh` 全过且总数 ≥49; `secret-guard.test.sh` PASS ≥581 且 FAIL 至多是测试内 SC-13 头注释计数这一条 (git 历史与 zsh 用例被跳过造成的环境性假红); `crlf-shim.test.sh`、`jq-crlf-guard.test.sh`、`host-docker-logout-guard.test.sh`、`submodule-gate-telemetry.test.sh` 与 `jq-crlf-guard.sh` 对两个 hook 的静态检查 rc=0; **29h / 29i** 同样两个套件由**真 bash 3.2** 运行 (PATH 里 `bash` 与 `#!/usr/bin/env bash` 都解析到 3.2)。**基线: 49/49; 581/582 且唯一 FAIL 为测试内 SC-13; 其余 5 项 rc=0; 3.2 下 49/49 与 581/582**。怎么会红: 新改动破坏既有断言, 或新增 jq 取值点未防 CRLF, 或新代码在 bash 3.2 下行为不同。
- **SC-30** (`zero-regression`, 探针外): 在带 git 历史 (可取到 `af87cae`) 的真 checkout 上跑 `secret-guard.test.sh` 全绿 —— 含测试内 SC-9a 对拍与测试内 SC-8 五档延迟闸 (天花板不改), 且测试内 SC-13 头注释等于实跑数; **另含 W14 的三个新时档 (f) / (g) / (h)**。**本探针不测**: 测试内 SC-8 是计时闸, 输出不能逐字节复现; 测试内 SC-9a / SC-8 需要 `af87cae` 历史。基线值不填推测数 (研究笔记在带 git 的副本上实测 593/593, `guard §0` 第 1 条, 非本探针产出), B.1 入场在真 checkout 实测并记入 handoff 为准。怎么会红: 新行让某档延迟超过天花板, 或改变了测试内 SC-9a 钉住的判定, 或扩展 / 替换判定把内建判定推迟、使 600 段命令越过 5 s 超时 (h)。
- **SC-31** (`reverse-guard` ×5, W14 / Impact): census `patterns.total` ≤ 150; census `family_count` 等于测试里硬编码的值; `risky_patterns` 无整行只由变量组成的行; `hooks/hooks.json` 与基线字节一致; `hooks/hooks.json` 不含字面 `completeness_gate`。**基线 5/5 (145; 61 = 61; 0 行; 一致; 不含)**。怎么会红: 规则膨胀超预算、新族没同步硬编码、用变量整行躲过 census、动了注册面。
- **SC-32** (`reverse-guard` ×3, bash 3.2): **32a** (启发式, **不是可跑性证明**) 两个 hook 的代码行 (去掉整行注释、单引号内文本与行尾注释) 不含 13 类 bash 4+ 构造 —— `declare -A`、`mapfile` / `readarray`、`${x,,}` / `${x^^}`、`[[ -v ]]`、nameref、负下标、`${x@Q}` 一族、`|&`、`&>>`、`;;&`、`coproc`、`shopt -s globstar|lastpipe`、`wait -n`; **32b** 两个 hook 与两个测试文件保持 LF; **32c** (**真运行腿**) 全部 hook-direct 行 (L1 与 L3) 各由默认 bash 与**真 bash 3.2** 跑一遍, 两个结果字符串逐行相同 (需要 `WPA_BASH32`)。**基线 3/3** (32c 在基线上 277 行一致)。怎么会红: 新代码用了 bash 4+ 专有构造或 3.2 下行为不同的构造 —— 解析类不兼容在 3.2 上使脚本整体 exit 2 (全部 Bash 被拦, 与 10CG/Aria#154 同型), 运行期不兼容使个别判定偏离 (用 `${s//p/r}` 的 W10 实现即是后者, 32c 可抓到); 变异实测: 往 hook 里加一个 `[[ -v … ]]` 函数, 32a 与 32c 同时转红。
- **SC-33** (`allow-guard` ×1, W2 / W3): L3 误报**语料普查**。语料 = `<aria>` 与 `<standards>` 两棵树 (固定 SHA: aria `268da8f`、standards `2bc1c4c`; 目标态为实现后的树) 下全部 ≤200 KB 的 UTF-8 文本文件 (不含 `.git`; 关键词预筛是 6 个新 tag 的必要条件, 只为提速), 每个当作一次 Read 结果喂 hook; 判据 = 6 个新 tag 命中的文件都在探针里写死的**归因清单**内 (现 2 个: `hooks/tests/secret-scan.test.sh` —— 带逼真示例值的夹具, W7 拼装后消失; `skills/requesting-code-review/examples/no-plan-fallback.md` —— 一行人类可读的硬编码口令示例)。**基线 0 个 (新 tag 尚不存在, 恒绿)**; 在按本 Spec 写的原型上命中的文件恰在清单内 (W7 拼装前 2 个, 拼装后只剩第二个); 变异实测去掉熵下限的分类器会让清单之外的 5 个文件命中 (四份 `forgejo-sync` 文档与 `aria-dashboard` 的 `issue-storage.md`) 而转红。**局限**: 这是对「分类器整体写宽」的回归守卫; 点分标识符链、路径形这类边缘规则在本语料里没有样本, 由 SC-9 9v / 9w 的形态行钉住。B.2 若新增含逼真示例值的文档, 须改占位写法或把该文件**带理由**加进归因清单 (走 Amendment)。

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

理由: 改动对象是两个 PreToolUse / PostToolUse hook 脚本、它们的测试、一份 standards 规范与插件 README, 零 SKILL.md、零 `description`、零 `references/` 变更 —— 即 SOT §4.1 所称「不属 Skill 变更」, 所以 `decision_table_row` 取 `n/a`。这是**分类, 不是免验主张**: 本 Spec 不援引 Rule #10 白名单第四类 (结构性前提不成立) 或任何别的豁免理由; 验证口径沿用 owner 2026-08-02 对同一 hook 的裁定 (该先例记录 owner 否决过「Rule #6 不适用」式写法, 因其与提供 substitute 逻辑上二选一, 统一为 substitute 框定), 验证口径即下列 substitute 三件。W13 写进 `secret-hygiene.md` 的条款与 W9 的 README 段是处方性文字, 但它们是 standards 规范 / 插件 README 而不是 Skill 的运行时指令面, 也不被任何 AB 套件加载; 与 `2026-08-02-secret-guard-nomad-var-put-echo` 同框处理。substitute 三件: structural fixture = 各 SC 的 `baseline-failing` 行 (基线实跑全红, 见证据); unit-test corpus = SC-29 + SC-30; dogfood = 对 canonical hook 的直调 (本探针即是, 目标态须全部 `yes`) + ship 后经 harness hook 链复验 (post-ship 腿, 需 owner 更新插件缓存并重启会话)。可证伪锚点: SC-25 (BLOCKED 文案零改动)、SC-31 31d (`hooks.json` 零改动)、SC-13 13d (处方句全串不变)。

**块 B —— `secret-scan.sh:367` additionalContext 插入「tags + source」** (W5, 唯一改动 AI 可见文本的 hunk):

```yaml
rule6_note:
  decision_table_row: 1
  description_changed: no
  scenario1: not_required
  scenario4b: not_required
  negctrl: n/a
```

理由: 插入的是事实陈述 (命中了哪些 tag、来自哪个工具 / 文件), 不含任何指示行为的措辞 —— 对应 SOT §1「描述性内容: … 陈述事实, 不指示行为」, 落 §2 决策表第 1 行 ⇒ deterministic substitute = SC 级 baseline-failing 结构化测试 (SC-13 13a–13c, 基线实跑全红)。可证伪锚点: 插入段之外的全串与基线逐字节相等 (SC-13 13d, 追加处方性句子即转红)。L1 的 BLOCKED 文案零改动 (SC-25), 不构成 hunk。

AI 自作主张、待 owner 复议: 块 B 判第 1 行而非第 3 行 —— 若判处方性, 须按 SOT §3 三件套 (点名行为 + 可证伪定向 fixture + 开「AB 套件缺 hook 文案维度」issue); AB 套件对 hook 零覆盖, 照跑 AB 是测量剧场。见「待 owner 复议」第 8 条。

## Impact

- **版本定级**: 建议 **MINOR**。依据 `standards/conventions/version-management.md` §2.2 (Minor = 新功能 / 功能增强, 向下兼容): WP-A 新增检测能力 (Read 首次被扫描、6 个 L3 tag)、新输入面 (`.aria/secret-guard.paths`)、新拦截族 (进程表、服务端配置)。CLAUDE.md §版本管理只对「新增 Skill / Skill 架构重构 = MINOR+、文档更新 / bug 修复 = PATCH」有明文, 对 hook 能力没有条款; 本族先例两个方向都有: v1.47.0 (`2026-06-19-secret-guard-exfil-coverage-iteration`, 新增检测覆盖) 为 MINOR, v1.65.4 / v1.66.3 / v1.66.4 (新增拦截族与名单扩展) 为 PATCH。**不写死版本号** (`<vNEXT>`): 取号在发版时刻两端 `ls-remote --tags` 并与 10CG/Aria#199 协商, 号的裁定归 owner。
- **行为变更双向申报**:
  - **新拦截 (L1)**: `app.ini` 族 (Bash / Read / Edit, 含备份与模板文件名); 项目扩展条目; 变量间接展开后命中的读取; 进程表列举族 —— 含以往放行的日常检查习惯 `ps aux | grep …` 与取 PID 的 `ps aux | grep X | awk '{print $2}'` (替代写法 `pgrep -f …`)、`ps axo pid,comm`、`ps <pid>`; `/proc/*` 与 `$pid` 形态; `nomad alloc exec` / `pct exec` / `ssh` 包裹下的裸 `env` / `printenv`。
  - **新告警 (L3)**: Read 工具结果首次被扫描 (读含逼真示例值的文件会告警); 6 个新 tag; 已知误报类 (W2)。
  - **新放行 (L1)**: python3 -c / node -e / lua -e 里 `os.environ` / `os.environb` 的**单键读取** (`.get(` / `[ ]`, 与基线放行的 `os.getenv(` 同一信息量); jq `keys_unsorted` 与 `map_values(length)` (锚定写法)。**整表导出与遍历、`.env` 家族经解释器读取均保持拦截 (与基线一致)**。
  - **新静默 (L3)**: 既有 `json-secret-field` 上的整值占位 / 掩码 / wrapper 占位 / 截断标记值; 哨兵回灌造成的重复计数。`$` / `<` 开头的随机值与 crypt 口令哈希**不**在内 (仍检出)。
  - **日志**: `secret-scan.log` 每行多一个 `fp=` 字段 (仓内无读取方)。
  - **性能**: Read 面每次多一次扫描 (W1); 进程调用延迟见 W14 (新行使 40–600 段的命令约 +15–20%, 200 条扩展再 +8–18 ms)。
- **同步面** (按最近两次发版同步提交 `72cb02b` / `a99dd8d` 实测列全, Tasks 1.11 承载):
  - aria 子模块 6 个发版文件: `.claude-plugin/plugin.json`、`.claude-plugin/marketplace.json` (两处版本)、`VERSION` (版本行 + 发布日期行 + 旧日期行)、`CHANGELOG.md` (新节带 rule6_note 行与五向行为变更)、`README.md` 与 `README.zh.md` (**每次发版都改** `Version | Released` 一行; Hooks 小节另按 W9 / SC-26 加段); 加上本 Spec 的代码 / 测试 / 头注释文件 (W1–W14)。
  - 主仓 **16 个版本点** (一个 `chore(release)` 提交): `CLAUDE.md` 2 处 (`v1.52.0–v1.74.x 已 ship` 行与 `版本: aria-plugin v…` 行, **无机械 check 兜底, 须人工**)、`README.md` 2 处 (badge 与 `Plugin Version:` 行)、`README.zh.md` / `README.ja.md` / `README.ko.md` 各 3 处 (`translated-from` 标记、badge、`Plugin Version:` 行; 标记受 `i18n-readme-translation-currency` 约束, 正文只在实质变更时重译)、`VERSION` 1 处、`docs/architecture/system-architecture.md` §2.8 与 `docs/architecture/version-scheme.md` 各 1 处; 外加两个 gitlink (aria + standards)。发版前后复跑 `m6-version-badge-match` / `i18n-readme-translation-currency` / `plugin-version-arch-docs-match` / `main-project-version-consistency`。
  - standards: `secret-hygiene.md` (§2.2 一行、§2.5 进程表行、§3.8 新条款、§5.1 勘正、§5.6 新节、三处 secret-guard 计数与一处 secret-scan 计数; 版本行 1.1.2 → 1.2.0 —— 新增条款属 additive, 先例 1.0.0 → 1.1.0, 版本历史表追加一行)。
  - 子模块合并一律本地 merge + 双推 + 逐个 `ls-remote` (CLAUDE.md 多远程两条硬约束); 不在一次性授权内的动作逐次请示。
- **与 10CG/Aria#199 的接缝**: `aria/hooks/hooks.json` 与 `.aria/config.json` 不得出现字面 `completeness_gate` —— 本 Spec 两者都不改 (SC-31 31d / 31e 钉住 `hooks.json`); `.aria/config.json` 在每次动相关文件后用 10CG/Aria#199 的守卫命令复核 —— 命令与判据以该 Spec `detailed-tasks.yaml` 的 `guard_config_hooks` 条为准, 不复述弱写法: `git -C <主仓根> grep --recurse-submodules -l -F completeness_gate | grep -E '(^|/)(hooks\.json|\.aria/config\.json)$'; echo "rc=${PIPESTATUS[0]}"`, `<主仓根>` 写绝对路径 (不带 `-C` 时 `git grep` 只搜当前目录以下, 会真空通过); 判据: 末行 `rc=` 为 0 或 1 且其前**无任何输出** = 通过, 其它 `rc` 值 = 没跑成, 停下上报。文件域不相交 (10CG/Aria#199 不改 hooks); 发版串行 (aria-plugin 版本源唯一), 合并前重新核 `plugin.json`。
- **issue 收尾口径** (默认取更保守的一侧):
  - **10CG/aria-plugin#154**: 三件交付物 + Read 提取修复落地并**经 post-ship 端到端复验 (Tasks 1.10) 之后**, 才按一次性授权评论并关闭; 关单评论须逐条披露与评论 19339 字面参数的两处**有意偏离**: (a) `token` / `sha1` 等键的值长门槛是 16 而不是 8 (8–15 位值不覆盖, KNOWN-LIMIT SC-10 10c); (b) 命中值的 sha256 前 8 位只对 ≥16 字符的值记 (更短只记长度), 且逐 tag 取裸值。
  - **10CG/aria-plugin#203 与 10CG/Aria#221**: 属决策单第 2 项的轮换延后集, **保持 open, 且在 owner 就「本项之下不评论」的范围作出裁定之前, 本 Spec 不在这两张 issue 下发任何评论** (默认取字面读法, 即「待 owner 复议」第 3 条的理解 B; 评论是不可撤回的外发动作, 含糊授权不构成放行)。代码侧进展写在 10CG/aria-plugin#154 的关单评论、PR 描述与 handoff 里。
- **覆盖关系**: 10CG/aria-plugin#154 全覆盖 (两处有意偏离见上; 另含 Read 提取修复与头部 / 参数形); 10CG/aria-plugin#203 部分覆盖 (第 1 类服务端配置: `app.ini` 族 + 扩展入口; 第 2 类变量间接: 部分修复 + KNOWN-LIMIT, 输出侧由 L3 兜底); 10CG/Aria#221 部分覆盖 (进程表列举已做; 两处误拦的 `os.environ` 单键读取与 `keys_unsorted` / `map_values(length)` 已做, `map(.name)` 与 `process.env` 不做; 「拒绝文案加一句」改落 SOT)。

## Tasks (A.2 骨架; 细粒度由 task-planner 产 `detailed-tasks.yaml`, 经 post_planning 审计)

- [ ] 1.1 B.1 入场: 重取行号 (对 `268da8f` 核差异); 在带 git 历史的真 checkout 实跑 `secret-guard.test.sh` 记录 SC-30 基线 (含测试内 SC-8 五档); **取得真 bash 3.2** (从 `ftp.gnu.org` 源码构建 bash 3.2 + 官方补丁 001–057, 需要 bison; 配方见 `baseline-evidence.md`) 并记下路径作 `WPA_BASH32`; 复跑 `baseline_probe.py` (带 `WPA_BASH32`), 输出与 `baseline-evidence.md` 逐字节一致
- [ ] 1.2 测试先行: 按 SC 把探针用例落为两个套件的用例 (运行时拼装), 先在基线上跑出「baseline-failing 全红、守卫全绿」
- [ ] 1.3 W1 提取 + W6 套件隔离 HOME + W7 既有夹具拼装 (`secret-scan.test.sh`)
- [ ] 1.4 W2 + W3 + W4 + W5 (`secret-scan.sh`; 分类路径零 fork, 正则放进变量)
- [ ] 1.5 W8 + W11 (新行、tight 并入、`/proc` 放宽; 内联成字面行以过 SC-31 31c)
- [ ] 1.6 W12 (单键读取归一化 + jq 锚定 credit)
- [ ] 1.7 W10 变量展开 (`_sg_vx_pass`, 前后缀拼接替换) + W9 扩展入口 (`_sg_ext_pass` / `_sg_ext_path_pass`, 全部扩展代码只经 `$( )` 调用)
- [ ] 1.8 W14 元耦合同步 (测试内 SC-13 / SC-19 / SC-20 注入自测 / census) + 对抗 review: 坏实现由非作者构造, 至少覆盖「白名单写成单字符前缀 / 含 / 大小写不敏感」「熵下限写成必须含数字」「路径形写宽」「tight 漏并入」「扩展条目拼成正则」「扩展代码裸调用」「扩展先于内建」「第二遍按段交错」「W12 给 `\.env` 加右边界」「`/proc` 连 status 一起放宽」「jq 新词进宽松词表」「bash 4+ 构造」十二种 (起草期对这十二种逐一做过变异实测, 转红的行已在各 SC 的「怎么会红」里点名, 复核其复现)
- [ ] 1.9 文档同步 (W13 SOT 条款与示例逐工具实跑、§5.6、README 两语种、hook 头注释、CHANGELOG 草稿 + SC-26 / 27 / 28; 勘正执笔人 ≠ 实现执笔人)
- [ ] 1.10 验收: 探针目标态全部 `yes` (带 `WPA_BASH32`, 32c / 29h / 29i 不得是 `not-run`) + SC-30 全绿 (含三个新时档) + SC-33 归因清单复核 + L3 稠密输入预算实测; **ship 后经 harness hook 链复验 (post-ship 腿)**: 用一条 Bash 命令打印运行时生成的合成值 (如 `python3 -c` 里用 `secrets` 生成并直接打印, 不写任何文件、不取自任何真实凭据), 期望 L3 告警并在 handoff 记「合成事件, 无需轮换」; 再对 `ps aux` 与 `/etc/forgejo/app.ini` 的读取各验一次拦截。**回退口径**: 出现全量阻断 (10CG/Aria#154 同型) 或超时放行 → owner 把插件缓存换回上一版并重启会话, 在 handoff 记事件; 不在 hook 内加逃生开关
- [ ] 1.11 发版 (取号与 10CG/Aria#199 协商, 两端 `ls-remote`) + **主仓 16 个版本点与 aria 6 个发版文件的同步提交** (Impact 同步面; CLAUDE.md 两处人工核) + issue 收尾 (按 Impact 口径; 10CG/aria-plugin#154 须在 post-ship 复验之后) + release claim

## 待 owner 复议

> 产品级 = 请裁 (未裁前按「默认」执行); 技术级 = AI 已裁, 列出供复议 (Rule #10: AI 的流程判断须请复议)。

**产品级 (请裁)**

1. **L3 是否升级为「检测 + 脱敏」(`updatedToolOutput`)**。选项 A: 维持检测 + 告警 (本 Spec 现状; `DEC-20260703-001` 继续有效) —— 代价: 值照样进模型上下文, 只多一条告警。选项 B (**推荐**): 先做一次端到端 spike (验证 `updatedToolOutput` 对 Read / Bash 是否真生效、不合形时的回退、与同 matcher 其它 hook 并行时「最后写入者生效」的实际语义), 通过后新 DEC + 独立 Spec —— 代价: 一次 spike 的成本, 期间同选项 A。选项 C: 本 Spec 内直接加脱敏 —— 代价: 未验证、要推翻 DEC, 误报代价从「多一条提醒」升级为「模型看不到被误脱敏的正文」, 本 Spec 的 W3 / 熵下限会从「降噪」变成「正确性前提」。**默认**: 选项 A。
2. **拒绝文案是否加「凭据不要放命令行参数」**。选项 A (**推荐**): 文案零改动, 条款只落 SOT (W13) —— 代价: 被拦的当下 AI 看不到这条建议, 且 tight 族与 Acceptable filters 的不一致继续存在。选项 B: 在全体共用的 heredoc 里加一句 —— 代价: 全部 145 条拦截 (含 `cat .env` 这类无关拦截) 都带这句; 首次改动处方性文案, 按 SOT §3 须三件套, 失去 2026-08-02 的「heredoc 零改动」锚点。选项 C: 先解 10CG/aria-plugin#132, 再只对进程表族给定向提示 (顺带能让 tight 族的提示与 credit 一致) —— 代价: 多一个前置 issue, 本 Spec 的进程表拦截先无提示上线。**默认**: 选项 A。
3. **10CG/aria-plugin#203 与 10CG/Aria#221 在 ship 后怎么收尾**。决策单第 2 项原文「相关 issue 保持 open、本项之下不评论」: 理解 B (本 Spec **默认**) 读作整张 issue 都不评论, 等轮换统一处理时一并; 理解 A 读作「不就轮换话题评论」, 保持 open 但评论代码侧进展。两种都不关闭。**默认**: 理解 B (含糊的否定性指令不构成放行, 评论不可撤回; 理解 A 需 owner 明示)。
4. **Level**: 维持 Level 2 (决策单第 3 项已裁) —— 代价: 不产 `tasks.md`, 细粒度计划只在 `detailed-tasks.yaml`, 且 Level 对账里三条升级判据字面命中; 或按 07-11 先例的 blast radius 理由改 Level 3 —— 代价: 补 `tasks.md`。post_spec / post_planning 两种 Level 下都照跑。**默认**: 维持 Level 2。
5. **进程表拦截改变日常习惯**: `ps aux | grep X` (含取 PID 的 `| awk '{print $2}'`) 被拦, 改用 `pgrep -f X` 或 `ps -eo pid,comm`; `systemctl status` 刻意放行 (交给 L3)。若 owner 认为误拦代价过高, 可改为只拦不带过滤的形态 —— 代价: `ps aux | grep curl` 恰是 10CG/Aria#221 的泄露形态之一。**默认**: 按 W11。
6. **版本定级** MINOR (建议) 还是 PATCH; 号的裁定归 owner。
7. **建议开单清单** (开新 issue 不在一次性授权内, 逐条请示; 每条附证据位置或最小复现命令; **开单前须对 open issue 去重**, 至少含 10CG/aria-plugin#131、10CG/aria-plugin#138、10CG/aria-plugin#139、10CG/aria-plugin#141、10CG/aria-plugin#142、10CG/aria-plugin#143、10CG/aria-plugin#144、10CG/aria-plugin#146):
   1. secret-guard 超时即放行: `hooks.json` timeout 5s, 约 1400 个空段使 hook 超时后命令被放行并执行 (`guard §0` 第 7 条、`§6.2` 第 1 条, 活体证实); 同源的延迟悬崖。**本 Spec 在加延迟 (新行使 40–600 段的命令约 +15–20%, 600 段命令基线 3.8 s → 4.4 s), 建议提高优先级**。
   2. 参数里引号内的 `|` 让所有「读取器 + `[^|]*` + 文件名」行失明: `grep -E 'A|B' ~/.bashrc` → exit 0 (`guard §0` 第 6 条 (ii))。
   3. credit 按整段计: 多行命令里随手一行 `| wc -l` 让整段放行 (`guard §0` 第 6 条 (iii))。
   4. 既有读取器行无左边界: `chmod 600 ~/.ssh/id_rsa` 因 `chmod` 含 `od` 被拦 (`guard §0` 第 6 条 (i); 本 Spec 探索实跑复现 exit 2)。
   5. Bash 面与 Read / Edit 面名单不对齐: 52 个样例 15 个两面判定不同, Read `~/.bashrc` 放行, Read `/proc/<pid>/cmdline|environ` 放行 (`guard §0` 第 9 条; SC-22 22au)。
   6. secret-scan PEM 预扫超线性 (870 KB 超过 120s), 被 SIGKILL 后遗留含输出全文的临时文件 (`scan §1.8`、`§5.4`); W1 让 Read 进入扫描面后该面随之扩大。
   7. **两层 matcher 都缺 Grep** (PreToolUse `Read|Edit|Write|MultiEdit`、PostToolUse `Bash|Read|Edit|Write|MultiEdit`), 另缺 PowerShell: Grep 的 `output_mode content` 绕过 W8 / W9 的 Read 面保护 (`scan §1.1`; `hooks.json` 在本 Spec 冻结, 结构上无法修)。
   8. 未覆盖形状: 飞书 webhook URL、Nomad / Consul `SecretID`、封闭表外的 PascalCase 键如 AWS `SecretAccessKey` / `SessionToken` (`scan §5.6`; SC-10 10f)。
   9. 服务端配置候选名单: `grafana.ini`、`/etc/{nomad,consul,vault}.d/`、`/etc/pve/priv/`、`/etc/shadow`、`.netrc` / `.npmrc` / `.pgpass` / `.git-credentials` / `.vault-token` / `.pypirc` / `.my.cnf` 等 (`guard §2(a)`; 需先建语料证明零误报)。
   10. 进程 / 容器环境族: `docker inspect <容器>` 全量 JSON 含 `.Config.Env`、`journalctl`、`nomad job inspect`、`sh -c '…printenv…'` 外壳内的裸 env (`guard §2(d)`); 以及「包裹 × 转储」整张矩阵 (nomad alloc exec / pct exec / ssh / sh -c × env / printenv / `cat /proc/*/environ`) 的统一处理。
   11. `log_ack` 写 `guard-bypass.log` 不带换行: `entry="$(printf '…\n')"` 的命令替换吃掉换行, 「一事件一行」的 TSV 不变量被破坏 (`secret-guard.sh:617-620`; 本 Spec 实跑: secret-guard 套件 12 条事件写成 0 个换行)。
   12. `host-docker-logout-guard.test.sh` 也向外层 HOME 的 `guard-bypass.log` 写事件 (本 Spec 实跑观察)。
   13. aria-doctor 校验 `.aria/secret-guard.paths` (W9 已知限制; 扩展失效目前静默)。
   14. jq 词表既有洞: `jq '. as $d | keys | map($d[.])'` 放行 (`guard §2(f)`; SC-24 24p)。
   15. `corpus_census.py` 的 `criteria.site_count == 6, expected exactly 13` 漂移 (census 以 rc=1 退出, 测试只取 stdout 所以不受影响; `guard §3.4`, 本 Spec 实跑复现)。
   16. `cat /proc/N/status` 轻度误报 (`guard §2(d)`; SC-22 22aj)。
   17. 语料普查扩面: 把 SC-33 的语料从 aria + standards 扩到 aria-orchestrator 与 `docs/` (探针只有 aria / standards 两个入口路径, 扩面须另定语料口径)。
   18. `secret-guard.test.sh` 的 R3-C-9 一组用 `testnonce_$(date +%s)` (秒级时间戳) 作一次性 ACK 的 nonce, 标记文件落在 `/tmp/secret-guard-ack-${USER}-<nonce>.nonce`: 同一秒内并发的两份套件 (同 `USER`) 会互相消费标记而偶发 FAIL (本 Spec 实跑复现一次: 两个并发的探针运行里 29b 得 580/582, 失败项为 R3-C-9; 探针改为每个套件任务使用私有 `USER` 绕开, 套件本身未修)。

**技术级 (AI 已裁, 待复议)**

8. rule6_note 分两块, 块 B (additionalContext 插入 tag 与来源) 判 SOT 决策表第 1 行 (描述性); W13 写进 `secret-hygiene.md` 的处方性条款与 W9 的 README 段按「非 Skill 变更」归入块 A (同 2026-08-02 先例); 块 A 的 `decision_table_row: n/a` 只是「不属 Skill 变更」的分类, 不是免验主张, 验证口径沿用 substitute 框定 (n/a 与 substitute 的关系见 rule6_note 块 A)。
9. W2: JSON 键封闭名表 + 拼写变体; 不纳入小写 YAML 键、CLI 空格分隔形、封闭表外 PascalCase; 新 tag 值长门槛统一 16; 熵下限「至少两类」; 路径形 = 开头标记 + 字符类 + ≥2 个 `/`; 点分标识符链排除; 头名大小写不敏感。
10. W3: 白名单只认整值占位形态 (尖括号 / 变量引用 / 模板 / 脱敏串 / 截断标记) 与刻意标记词开头, 大小写敏感; 作用于 6 个新 tag + 既有 `json-secret-field`, 不含 `env-line-secret-keyword` 与 provider 前缀类; 放行的 span 仍被哨兵消费 (理由见 W3)。
11. W4: 值长 16 以上记 sha256 前 8 位、以下只记长度; 逐 tag 取裸值 (表见 W4), 遍历序 = 计数遍历序, 上限 10 项; 追加字段而不另起日志文件。
12. W7: 夹具源头拼装, hook 不加按路径的豁免。
13. W8: 本次只做 `app.ini` 族, 其它候选推迟; 右边界不为模板放行 (备份与模板在命令文本上不可区分, 拦备份的价值更大); 词内前缀允许 (`git-forgejo`)。
14. W9: 纯文本 + 字面子串 + 固定字符串单遍匹配 + 大小写不敏感; 扩展代码全部隔离在命令替换里、内建先于扩展; 失败整体忽略且静默; `CLAUDE_PROJECT_DIR` 优先、回落 stdin `cwd`。
15. W11: 处置选拒绝而非 `updatedInput` 改写或 `ask`; tight credit; `systemctl status` 放行; 纳入 `sh -c` / `watch '…'` / `pct exec` 外壳与 launcher 包裹的 `pgrep` / `pstree` / `top`; **纳入**包裹下的裸 env / printenv 转储; `/proc` 放宽不含 `status`。
16. W12: 单键读取归一化 (`.environ.get(` / `.environ[` 及 `environb` 变体), 不给任何 `\.env` 行加右边界; 整表导出与遍历保持拦截; jq 两个新形态都走锚定语法, 不进宽松词表。
17. 探针在不带 git 的副本上跑套件 (逐字节可复现), git 腿 (SC-30) 放到 B.1 / B.2 的真 checkout 上; bash 3.2 腿由可选环境变量打开 (缺省时三行 `n/a`, Tasks 1.10 验收要求打开)。
18. **扩展失效是否对用户可见**: 选项 A (**已裁**) 保持静默 (现状), 缓解靠文档与后续 aria-doctor 校验。选项 B: 失效时 exit 0 + stdout `{"systemMessage": "…ignored: <原因>"}` (不含条目内容) —— 代价: PreToolUse 上该通道的端到端行为未验证、热路径新增输出通道、无状态时每次调用重复提示; 建议先做一次小 spike 再定。选项 C: 超限改「截断 + 告警」而不是整体忽略 —— 代价: 部分生效的清单更难排查, 且依赖 B 的告警通道。

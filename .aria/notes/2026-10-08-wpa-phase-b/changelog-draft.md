<!--
CHANGELOG 草稿 — Spec secret-net-l3-and-bypass-paths (WP-A) — TASK-009 产出, 由 TASK-011 发版时并入 aria/CHANGELOG.md 最上一节。

使用说明 (发版者读完删掉本注释):
1. 本文件不是 aria/CHANGELOG.md 的一部分; aria/CHANGELOG.md 由 TASK-011 修改。
2. 尖括号占位待填: <vNEXT> (版本号, 取号归 owner: 发版时刻两端 ls-remote --tags 并与 10CG/Aria#199 协商) / <发布日期> / <TASK-010 实测> (性能数值与规则行数, 下面写的是 Spec 原型量级)。
3. SC-26 26g 机械检查 aria/CHANGELOG.md 最上一节须含这 14 个标记词, 缺一转红: rule6_note / .aria/secret-guard.paths / ps aux / /proc / app.ini / file.content / kv-secret-assign / placeholder / os.environ / keys_unsorted / fp= / CPU / partial / PostToolUseFailure。改写时保留它们 (已用探针自带的判据对本草稿跑过: 14/14)。
4. 提交页脚与 PR 描述对三张 issue 只写 Refs, 不写 Closes / Fixes / Resolves。
5. 不含任何凭据形状字面量 (aria 有公开 GitHub 镜像)。
-->

## [<vNEXT>] - <发布日期> — secret-net-l3-and-bypass-paths: 检测网补洞 + 旁路收口 (`10CG/aria-plugin#154` / `10CG/aria-plugin#203` / `10CG/Aria#221`; MINOR: 新检测能力 + 新输入面 + 新拦截族, 向下兼容)

### Security — PostToolUse secret-scan (检测 + 告警, 不改写输出)

**背景**: 2026-08-20 事故的 JSON `token` 键与 2026-09-26 事故的 `JWT_SECRET = <值>` (等号两侧带空格) 都从全部既有模式底下穿过; 更深的前置缺口是提取链只认 `output` / `content` / `stdout`, 而 Claude Code 2.1.285 的 Read 结果是 `{type:"text", file:{content,…}}` —— **生产中 Read 从未被扫描** (旧 Read 用例用合成形状, 所以一直绿)。

**修复**:
- 提取链补 `.tool_response.file.content` (Read) 与 `.error` (失败调用); NUL 分隔的内容 (`/proc/<pid>/environ`、`env -0`) 另加第二个视图 (含 NUL 的输入在两个视图上各扫一遍, 同一凭据的计数可能多一份, 只会多不会少)。
- `hooks/hooks.json` 为 secret-scan 增一条 `PostToolUseFailure` 注册 (matcher、命令、超时同其 `PostToolUse` 条目; 其余注册零改动): 失败的工具调用 (Bash 非零退出等) 不触发 `PostToolUse`, 它们的错误文本此前整体失明。输出里的 `hookEventName` 取输入的 `hook_event_name`, 因为 harness 按实际触发的事件校验它。
- 6 个通用键形 tag: `json-credential-field` / `json-env-secret-key` / `kv-secret-assign` (INI / env / YAML 赋值, 含等号两侧空格、引号、`export`) / `auth-header-token` / `cf-access-client-secret` / `cli-secret-flag`。值先过分类器: placeholder 白名单 (FAKE / PLACEHOLDER / NOT-REAL / `[REDACTED…]` 整值、`<…>`、`${…}`、`{{…}}`、掩码、以 `…` 结尾的截断值)、熵下限 (小写 / 大写 / 数字至少两类)、路径形、点分标识符链 (如 `process.env.X`)。
- 告警文案 (`additionalContext`) 多一段事实陈述: 命中的 tag 与来源工具 (`tags: …; source: …`); 不含 `tool_input` 的任何文本。
- 日志 `secret-scan.log` 每行多一个 `fp=` 字段: 每个计入的 span 一个指纹 (值 ≥16 字符取 sha256 前 8 位, 更短只记长度; 至多 10 个), 不含值。
- 两个测试套件把 `HOME` 指向自建临时目录 (不再往真实 `~/.claude/logs` 追加夹具事件), 既有夹具改为运行时拼装。

### Security — PreToolUse secret-guard (按命令文本拦截)

- **`app.ini`**: Forgejo / Gitea 服务端配置 (`JWT_SECRET` / `SECRET_KEY` / `INTERNAL_TOKEN` 与数据库口令都在其中) 进 Bash 面 (29 个打印型读取器 + `python3 -c` / `node -e`) 与 Read/Edit 面, tight credit。
- **进程表**: 带完整命令行列的 `ps` (`ps aux` / `ps -ef` / `ps -eo pid,args` 等)、`pgrep -a`、`pstree -a`、`top -c`、`docker top`、`docker ps --no-trunc`、`/proc/<pid>/cmdline|environ` (pid 位置放宽到 `self` / `$$` / glob / 变量)、11 个远程与外壳包裹下的 `env` / `printenv` 转储。
- **项目扩展入口 `.aria/secret-guard.paths`** (新输入): 一行一个字面子串, 大小写不敏感, **只增不减** (内建先判; 复用内建的同一判定函数, 不另写状态机); 限额 32 KiB / 200 条 / 每条命令前 64 处出现; 失效即**整体忽略且静默**; 保护边界与「条目选最短特征子串」的建议见 `README.md` / `README.zh.md` 与 standards `secret-hygiene.md` §5.6。
- **变量间接 (`partial` 修复)**: 字面赋值 (`f=…; cat "$f"`、`for f in …`、单层链式) 在内建判定全部放行之后再判一遍替换后的副本; 数组、`read <<<`、引号夹在路径中间、`cd` 后相对名、glob、`set --`、`$(printf …)`、跨两次工具调用的变量不覆盖, 由 secret-scan 在输出侧兜底。
- **两处误拦修复 (新放行)**: `python3 -c` / `node -e` / `lua -e` 里 `os.environ` / `os.environb` 的**单键读取** (`.get(` / `[ ]`, 与基线放行的 `os.getenv(` 同一信息量); jq 的 `keys_unsorted` 与 `map_values(length)` (锚定写法)。整表导出与遍历、`.env` 家族经解释器读取**仍拦**。
- **拒绝文案零改动** (BLOCKED 文本归一化后与基线逐字节一致): 「凭据不要放命令行参数」的建议落 standards `secret-hygiene.md` §3.8, 不进共用文案。已知不一致: 共用文案的 `Acceptable filters` 对 tight 族无效 (已记入 SOT §2.5 注与 hook 头注释)。

### 行为变更双向申报

- **新拦截**: `app.ini` 族 (含 `app.ini.bak` 一类备份与模板文件名); 项目扩展条目; 变量间接展开后命中的读取; 进程表族 —— 含以往放行的日常检查习惯 `ps aux | grep …` (及 `ps -aux`)、取 PID 的 `ps aux | grep X | awk '{print $2}'` (替代: `pgrep -f …`)、`ps axo pid,comm`、`ps aux | grep -c X`; 包裹下带变量名的 `printenv <NAME>` (以往放行的容器内单变量核对由放变拦, 改走 `# guard:ack`)。文本提及的误拦 (含 `ssh` / `watch` 这类包裹词再出现进程表形态的提交信息、`echo`) 见 SOT §2.5。**新拦截在 Layer 2 (aria-runner 容器, 无人值守) 里同样生效**: BLOCKED 文案里的 `# guard:ack: <理由>` 在那里由执行方 AI 自己写、没有人复议, 本次不改这一既有机制。
- **新告警**: Read 结果首次被扫描 (读含逼真示例值的文件会告警); 失败调用的错误文本 (`PostToolUseFailure`) 首次被扫描 (该事件上 `additionalContext` 的端到端送达待 post-ship 验证); NUL 分隔内容首次可被检出; 6 个新 tag (含已知误报类, 如文档里以 ASCII `...` 截短的示例值)。
- **新放行**: `os.environ` 单键读取; jq `keys_unsorted` / `map_values(length)`。
- **新静默**: 既有 `json-secret-field` 上的整值占位 / 掩码 / wrapper 占位 / 以 `…` 结尾的截断值; 哨兵回灌造成的重复计数。
- **日志**: `fp=` 字段 (仓内无读取方)。
- **性能 (CPU)**: Read 面每次多一次扫描 (整进程 CPU 时间约 0.104 s → 约 0.299 s; 60 KB 无命中文本约 0.345 s); Bash 面无扩展文件时约 +24% CPU、Read 面约 +7%; 含 `$VAR` 引用的命令因变量间接的第二遍约为基线的 1.45–2.5 倍 (内建先判, 已被拦下的命令不付第二遍); 200 条扩展条目约 +30 ms / 次调用; 命令里出现列入的路径时多付一遍内建判定 (约 2 倍, 与出现点数无关); 长单行 L3 输入的匹配与取值对长度线性。以上为 Spec 原型量级, 发版前以 <TASK-010 实测> 复测值替换。

### Documentation

- standards `conventions/secret-hygiene.md` 1.1.2 → 1.2.0 (additive): §2.2 `app.ini` 行 / §2.5 进程表行与 tight 族注 / 新增 §3.8「长时进程的凭据传递」(命令行参数不得含凭据, 与短命令以 60 秒分界; §3.1–§3.7 与 §4 的短命令示例逐字节不变) / §5.1 勘正 (secret-guard 是 Bash + Read/Edit blocker) / §5.2 追加 `updatedToolOutput` 事实 / 新增 §5.6 项目扩展入口; 三处 secret-guard 自测计数与一处 secret-scan 计数同步。
- `README.md` / `README.zh.md` 的 Hooks 用法小节: `.aria/secret-guard.paths` 用法 (字面子串、最短特征子串、保护边界)、`PostToolUseFailure`、`updatedToolOutput` 事实各一句。
- 两个 hook 的头注释勘正 (只改注释, 去掉整行注释后与改前逐字节相同): 去掉陈旧的 `~100` / `49` / `~15` 数量字面与不存在的 argon2 声明; 改写与 `updatedToolOutput` 实测矛盾的「无字段可替换」一句; 补 Read 的 `file.content` 形状与失败事件的 `error` 契约; 记本 change-id。`VERSION` 里 v1.24.0 条目的「output REDACT」改为 detect + warn。

### Tests

- `secret-guard.test.sh` 599 (593 无 zsh) → **822 (816 无 zsh)**, 含 census `family_count` 61 → 64 与新族探针、未绑定变量注入自测、测试内 SC-8 五档延迟闸 (阈值与口径不改); `risky_patterns` 静态行数 149 (预算 ≤ 150)。`secret-scan.test.sh` 49 → **129**, 头注释 `Coverage: K cases` 与一条读取它的自检断言 (K 与实跑总数一致)。standards `secret-hygiene.md` 的计数与二者同步。
- 验收探针 `baseline_probe.py` 目标态全部 `yes` <TASK-010 填: 命令与结果行>。

### Notes

- **未做 (范围外)**: L3 升级为「检测 + 脱敏」(`updatedToolOutput`, 产品级, 端到端未验证); Grep 工具读敏感路径 (两层 matcher 都不含 Grep, 结构上无法在本次修); 凭据轮换 (决策单另行处理); WP-B (`10CG/Aria#223` + `10CG/aria-plugin#207`)。
- **覆盖关系**: `10CG/aria-plugin#154` 全覆盖; `10CG/aria-plugin#203` 部分覆盖 (服务端配置 + 扩展入口; 变量间接为 `partial` 修复, 输出侧由 secret-scan 兜底); `10CG/Aria#221` 部分覆盖 (进程表列举与两处误拦已做; 「拒绝文案加一句」改落 SOT)。
- **post-ship 复验** (发版后, owner 更新插件缓存并重启会话后执行): 惰性诱饵验证 Read 提取、进程表与 `app.ini` 拦截、NUL 前提、失败事件送达。

rule6_note: hook bash 代码 + 测试 + 头注释 / 计数 / SOT 文档与 README, 零 SKILL.md、零 `description`、零 `references/` 变更 → 不属 Skill 变更 (`decision_table_row: n/a`, `description_changed: no`), 验证口径为 substitute: 各 SC 的 baseline-failing 行 (基线实跑全红) + 两个套件回归 + 对 canonical hook 的直调探针 + 发版后经 harness hook 链的 post-ship 复验。唯一改动 AI 可见文本的 hunk 是 secret-scan 告警 `additionalContext` 里插入的「tags + source」事实陈述 (判据表第 1 行, 描述性: 不含指示行为的措辞, 不含 `tool_input` 文本; 可证伪锚点 = 插入段之外的全串与基线逐字节相等); L1 的 BLOCKED 文案零改动。该分类为 AI 依 `skill-benchmark-exemption.md` 自行判定, 已列入 Spec「待 owner 复议」。

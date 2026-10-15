你是 WP-A Spec 的**执笔实例** (tech-lead), 按 Aria 规范 (spec-drafter, 十步循环 A.1) 起草 `openspec/changes/secret-net-l3-and-bypass-paths/proposal.md` **v1** 全文 (Level 2), 以及它引用的基线证据。主控会独立核验你的每一处事实声称并复跑你的证据脚本; 之后是五席 post_spec convergence 审计。全程中文叙述, 代码 / 命令 / 路径 / SHA 保留英文。

## 输入 (全部先读)

1. 四份研究笔记 (主控派 agent team 做的, 源码与基线实测): `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/research/secret-guard.md`、`/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/research/secret-scan.md`、`/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/research/precedent.md`、`/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/research/cc-hooks.md`。笔记与源码冲突时以你实读的源码为准, 并在交付里指出冲突。
2. 三个 issue 的正文与评论: `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/issues/aria-plugin-154.md`、`/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/issues/aria-plugin-203.md`、`/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/issues/Aria-221.md`。
3. owner 决策单 `.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md` (全文; WP-A = Level 2; 凭据轮换全部延后、先头脑风暴、期间不产出轮换清单也不逐条提示; 一次性授权的四类外向动作与其边界; 双子星分工)。
4. spec-drafter 规范: `/home/dev/.claude/plugins/cache/10CG-aria-plugin/aria/1.74.1/skills/spec-drafter/SKILL.md` (特别是「proposal.md 头部字段要求」)。
5. 体例先例 (同为 secret-guard 的 Level 2 Spec, 已 ship): `openspec/archive/2026-08-22-secret-guard-manifest-precision/proposal.md`。
6. 当前 proposal 头部 (已存在, 共 6 行): `openspec/changes/secret-net-l3-and-bypass-paths/proposal.md`。标题行可以改得更准确, 但 **Level / Status / Created / Linked Issue 四行逐字保留** (Linked Issue 已被 A.1 认领使用)。
7. 源码: `aria/hooks/secret-guard.sh`、`aria/hooks/secret-scan.sh`、`aria/hooks/hooks.json`、`aria/hooks/tests/` (基线 = aria `268da8f`, 即当前 checkout)。

## 交付物

1. **proposal.md 全文** (结构化输出的 `proposal_markdown`)。
2. **基线探针脚本** (`probe_script`, 将落为同目录 `baseline_probe.py`): stdlib-only Python 3; 用法 `python3 baseline_probe.py <aria 仓路径>`; 对 proposal 里**每一条** SC 的判定命令逐条在给定 aria 上执行并打印一张表 (SC 编号 / 用例 id / 输入形态的占位描述 / 期望 / 实得 / 是否符合)。约束: 像凭据的值在进程内用 `secrets` 运行时生成, 经 stdin 喂给 hook, `capture_output=True`, 绝不打印; 运行 hook 时 HOME 指向脚本自建的临时目录; 输出必须确定性 (不含时间戳、随机值、绝对临时路径), 这样任何人重跑都应逐字节相同。
3. **基线证据** (`evidence_markdown`, 将落为同目录 `baseline-evidence.md`): 一段说明 (在哪个 SHA、怎么跑) + 你在自己的副本上实跑 `python3 baseline_probe.py <副本>/aria` 的 **stdout 原样** (放进代码块, 不手改一个字符)。主控会在 aria `268da8f` 上重跑并逐字节比对。
4. `self_reported_weak_points`: 你自己认为最薄弱、最可能被审计打回的地方 (如实写)。
5. `owner_review_items`: AI 自作主张、需要 owner 复议的判断 (CLAUDE.md 规则 #10: AI 的流程判断必须请复议; 同时按「owner 只裁产品级、技术级 AI 直接裁」区分, 产品级的列为请裁, 技术级的列为已裁待复议)。
6. `design_decisions`: 每个关键取舍一条 (候选 / 选择 / 理由 / 可证伪的判据)。

## proposal.md 的要求

- **头部 blockquote**: 保留四行后追加: `认领` (track `secret-net-l3-and-bypass-paths-023236f2` @ simonfish/023236f2, phase1_gate A.1 advisory, 2026-09-30T17:57:13Z, `linked_issue_overlap == []`) / `基线冻结` (aria `268da8f` = v1.74.1; 主仓 `0748dbc`; 行号与计数均对此) / `代码落点` / `决策来源` (决策单文件与条目)。
- **节**: `## Why` / `## What Changes` (按 W1、W2… 分项, 每项写: 现状 (file:line) → 改动 → 设计取舍 (至少两个候选与不选的理由) → 已知限制) / `## Out of scope` / `## Success Criteria` / `## rule6_note` / `## Impact` / `## Tasks` (A.2 骨架) / `## 执笔自报薄弱点` / `## 待 owner 复议`。
- **What 至少覆盖**: (1) L3 secret-scan 通用键形模式 (10CG/aria-plugin#154 评论 19339 收窄后的三项交付: 键形条目 + FP 白名单 + 日志只留哈希前缀的断言) 以及 INI / env 赋值形 (等号两侧带空格, 10CG/aria-plugin#203 的泄露原形) —— 研究笔记里的基线检测矩阵决定要补哪些形状; (2) L1 服务端配置文件入敏感名单 (10CG/aria-plugin#203 第 1 类) 与项目级扩展入口; (3) 路径经 shell 变量间接 (10CG/aria-plugin#203 第 2 类): 明确决定在 L1 做到什么程度、哪些承认堵不住并交给 L3, 并论证; (4) 进程表列举 (10CG/Aria#221): 拦哪些形态、放哪些形态 (只出 pid / comm 的不拦), 选拒绝还是其它处置 (以 cc-hooks 笔记的平台事实为据); 同族的进程环境读取要不要一并处理; (5) 两处误拦 (10CG/Aria#221 评论 25898: `\.env` 右边界; 只出元数据的 jq 形态入白名单); (6) 拒绝文案补一句「凭据不要放命令行参数, 改用 env / --config / stdin」。每一项都必须能追溯到 issue 原文或研究笔记的实测。
- **Success Criteria**: 每条写死判定命令 (hook 输入如何构造、期望退出码 / 判定 / 是否告警) 与**基线实测值**, 并标注类别: `baseline-failing` (基线红, 目标绿) / `反向守卫` (基线与目标都应保持拦截或检出, 防回退) / `零回归` (全量既有测试通过, 计数不低于基线实测值) / `文档同步`。误报修复的 SC 必须同时有「修复后放行」与「真阳性仍拦」两面。每条 SC 都要回答「它怎么会红」。基线值只能来自你实跑 `baseline_probe.py` 的结果, 不得凭推测填写。
- **rule6_note**: 字段按 `standards/conventions/skill-benchmark-exemption.md` §4.1 (研究笔记 precedent.md 已抄出字段名与 2026-08-02 的 hook substitute 先例原文); 逐 hunk 性质判定 —— hook 判定逻辑与测试 vs 会注入 AI 上下文的拒绝 / 告警文案, 后者要单独判并给出依据。
- **Impact**: 版本定级 (PATCH 或 MINOR, 按 CLAUDE.md §版本管理判并说理由; **不写死版本号**, 取号在发版时刻 `ls-remote --tags` 两端并与 10CG/Aria#199 协商, 号的裁定归 owner); 行为变更双向申报 (新拦截 / 新告警 vs 新放行); 同步面 (aria 子模块、standards、主仓 gitlink 与版本点、CHANGELOG); 与 10CG/Aria#199 的接缝 (`aria/hooks/hooks.json` 与 `.aria/config.json` 不得出现字面 `completeness_gate`; 发版串行); 本 Spec 关闭哪些 issue、哪些只部分覆盖。
- **Out of scope** 至少写明: 凭据轮换 (决策单第 2 项, 本 Spec 不产出轮换清单、不涉及具体凭据); WP-B; PostToolUse 无法脱敏内置工具输出这一平台限制下的「撤回」能力。

## 写作纪律

- **Rule #7**: 文档与脚本里不出现任何能被现行或拟议的 L1 / L3 规则命中的真实凭据形状字面, 一律用占位写法 (如 `<40 位 hex>`)。注意: 拟议的 JSON 键形模式若写成「值 8 个以上非引号字符」, 连 `"token":"<40 位 hex>"` 这种占位写法都会命中 —— 设计 FP 白名单时要把 Spec、测试、文档里的占位写法考虑进去, 并用 SC 钉住 (本 Spec 自己被扫描时不应告警)。
- issue 引用一律全限定 `<org>/<repo>#<n>`; 编号只用 `1.` `2.` 或「第 1 类」这类写法, **不要用带圈数字** (owner 的终端看不清); 不写 AI 署名行。
- 被机器解析的字段名、哨兵、枚举一律英文 canonical。
- 审计叙事 (各轮结论、裁定过程) 不写进 proposal 正文 —— Status 行只写一句当前状态。
- 新文件用 LF 行尾。

## 硬性纪律

- **你不写仓内文件、不 commit、不 push、不 fetch**, 不开 issue、不发评论, 不使用 Agent 工具。三份交付物放在结构化输出里返回, 由主控落盘。
- 实跑只在 `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v1/` 下: `cp -a /home/dev/Aria/aria` 到那里再跑; HOME 指向该目录下的 `home/`。
- 不读取、不打印任何真实凭据。

## 主控范围裁定 (技术级, 基于四份研究笔记; 你可以反驳, 但必须给出实测或源码证据, 并写进 design_decisions)

主控已亲自核实一条平台事实: 本机 Claude Code 2.1.285 二进制的 PostToolUse hookSpecificOutput schema 含 `updatedToolOutput` (描述原文「Replaces the tool output before it is sent to the model」, 旁注「Prefer updatedToolOutput, which works for all tools」; 多个 hook 并行跑在原始输出上、最后写入者生效)。cc-hooks 笔记里「PostToolUse 不能改写」的说法来自过时文档, 以二进制为准。**但端到端未验证**。

### 纳入 WP-A (in scope)

L3 (`secret-scan.sh`):
1. **Read 提取失明** (secret-scan 笔记关键发现 2): 读真实 Read 形状 `.tool_response.file.content`, 保留旧的合成形状以兼容; 新测试必须用真实信封 (从笔记里的实测形状构造), 旧测试一直绿正是因为用了合成形状。Edit / MultiEdit 不纳入 (Edit 结果不向模型回显内容, 不构成「进入模型上下文」的泄露), 在 Out of scope 写明理由。
2. **通用键形模式** (加法式, 不改既有 tag 语义): JSON 键形 (封闭键表, 以笔记矩阵为据决定是否含首字母大写键)、INI / env 赋值形 (等号两侧空格, 10CG/aria-plugin#203 原形)、HTTP 头部与参数形 (`Authorization: token <hex>`、`CF-Access-Client-Secret`、`--token=<hex>`; 10CG/Aria#221 的 L3 互补面, 基线零告警); 必须配分类器与熵下限, 已知漏报类 (单字符类随机串等) 成文并配测试。
3. **FP 白名单**: 按「值以…开头」判定 (FAKE / PLACEHOLDER / NOT-REAL / [REDACTED, 以及占位写法 `<…>`、`${…}`、`{{…}}`、掩码等), 作用范围你来定并证明: 至少覆盖新增的通用键形 tag; 是否延伸到既有 json 键形 tag 要给出两面测试 (消除既有误报 vs 不翻红既有 provider 夹具)。provider 前缀类 tag 不套白名单。
4. **日志留痕**: 新增命中值的哈希前缀 (笔记证实现行日志既无值也无哈希, 这是新功能, 不是「补断言」); 主控倾向: 值长度 ≥ 16 才记 `sha256` 前 8 位, 更短只记长度 (8 位无盐前缀可被离线字典确认低熵口令)。你可以另选, 但要论证。
5. **告警文案最小改动**: additionalContext 里加命中的 tag 名单与来源 (工具名、Read 的 file_path), 不含任何值; 其余措辞尽量不动 (提示文案是运行时指令面, 改动越小 Rule #6 越好判)。写明它与 owner 决策单第 2 项「不逐条提示轮换」的关系 (那一项针对已知的四枚待轮换凭据, 不改变新检出事件的标准处置)。
6. **测试卫生**: secret-scan 测试套件隔离 HOME (现每次运行向真实审计日志追加约 33 行夹具噪声), 新夹具一律运行时拼装。
7. **夹具静默**: 修好 Read 提取后, 读本仓含字面夹具的测试文件会持续告警 (笔记关键发现 11)。给出最小可证伪的处置 (例如按路径的「只记日志、不注入 additionalContext」清单, 或把相关夹具改为运行时拼装), 并论证不会成为真实泄露的盲区。

L1 (`secret-guard.sh`):
8. **服务端配置文件**: 以 Forgejo / Gitea `app.ini` 族为本次必做 (事故证据), Bash 面与 Read / Edit 面两面都补, 并入 tight 检测 (否则 `| grep '^JWT_SECRET'` 这类锚定 grep 会被当成过滤而放行), 新行自带读取器左边界。其它候选 (grafana.ini、/etc/{nomad,consul,vault}.d/、/etc/pve/priv/、经典凭据点文件) —— 若现行名单缺、且你能给出语料零误报的实测, 可纳入; 否则列入后续。
9. **项目级扩展入口**: `.aria/secret-guard.paths` (字面子串、只增不减、两面生效; 文件缺失 / 不可读 / 格式坏 / 超大 ⇒ 忽略扩展、内建名单照常生效, 并在 Spec 里说明这是「扩展失败只丢扩展」而非整体 fail-open); 项目根取 `CLAUDE_PROJECT_DIR`, 回落 stdin `cwd`。不改 `.aria/config.json` (避开 10CG/Aria#199 的 `completeness_gate` 守卫与 config-template-key-currency 检查)。
10. **变量间接**: 采用笔记原型「整条命令收集字面赋值 + 对含 `$VAR` 的段多判一次替换副本」, 残余清单 (数组 / read / 引号拼接 / cd 加相对名 / glob / 跨工具调用的变量) 写进已知限制, 并明确「这些交给 L3」。
11. **进程表列举**: 按笔记实测矩阵拦暴露 argv 或 environ 的形态 (ps 的 aux / -ef / -o args|cmd|command / -f 等、pgrep -a、top -c、/proc/N/cmdline、/proc/N/environ、ps e / eww), 用 tight credit; 不拦只出 pid 或进程名的形态; `systemctl status` 不拦 (误报代价高), 写成已知残余。处置用拒绝 (exit 2, 与现有 hook 一致); `updatedInput` 改写方案考虑后不选 (多 hook 并行最后写入者生效、静默改用户命令、现 hook 无 JSON 输出路径), 理由写进取舍。
12. **两处误拦**: `\.env` 右边界只改三条内联解释器规则 (python3 -c / node -e / lua -e), 写成 `\.env(rc)?([^A-Za-z0-9_]|$)`, 并用 SC 证明全局加边界会漏拦的形态仍被拦; jq 只新增 `keys_unsorted` 与 `map_values(length)` (锚定写法), `keys[]` 保持拦截 (负向锚与 SOT 明文), 并如实写出 `length` 与 `.X | length` 基线本就放行 (issue 这部分已过时); `map(.name)` / `map(.key)` 不纳入。node 的 `process.env` 误报不纳入 (需归一化, 非加边界可解)。
13. **拒绝文案补一句**: 「凭据不要放命令行参数, 改用 env / --config / stdin」—— 由你决定只放进进程表族的拒绝文案还是全体共用, 并给理由。
14. **测试元耦合与同步**: 笔记列出的 SC-13 头注释计数、SC-19 census `family_count`、SC-8 性能预算 (新行使每段成本多 10-25%, Spec 要给明确预算) 等必须在计划里点名同步; `standards/conventions/secret-hygiene.md` 的计数同步。

### 不纳入 WP-A (out of scope, 列入「待 owner 复议」或后续)

- **L3 从「检测 + 告警」升级为「检测 + 脱敏」(`updatedToolOutput`)**: 产品级 (模型将看不到被脱敏的正文) + 未做端到端验证 + 要推翻 DEC-20260703-001。本 Spec 保持检测 + 告警, 并让检测核心可被日后的脱敏模式复用; 在「待 owner 复议」里如实给出选项 (建议先做端到端 spike, 通过后新 DEC + 独立 Spec), 不要只写对自己有利的那一面。
- **既有缺陷** (研究里新发现, 非三个 issue 所诉): secret-guard 的超时即放行 (约 1400 个空段使 hook 超 5 秒, 已活体证实) 与延迟悬崖、引号内 `|` 使 `[^|]*` 行失明、credit 按整段计、既有行无读取器左边界 (chmod 600 误拦)、Bash 面与 Read / Edit 面名单不对齐; secret-scan 的 PEM 预扫超线性与被杀后遗留含输出全文的临时文件、matcher 缺 Grep / PowerShell、飞书 webhook URL 等未覆盖形状。开新 issue 不在 owner 一次性授权内 ⇒ 在「待 owner 复议」里列成「建议开单清单」, 每条附研究笔记里的证据位置。
- 凭据轮换 (决策单第 2 项)、WP-B、10CG/Aria#199 本身。

### precedent 笔记带来的补充裁定 (覆盖上文对应条目)

- **第 13 条改为「不改 BLOCKED 拒绝文案」**: precedent 笔记证实 10CG/Aria#221 的「文案加一句」与 08-02 Spec 明确拒绝并转出的 10CG/aria-plugin#132 同根 (全局共享 heredoc 会污染全部 145 条 pattern 的拦截文案; `$pattern_hint` 未初始化在 `set -u` 下使全部 BLOCKED 文案崩溃), 且 BLOCKED 处方性行自 2026-05-23 起未改过、08-02 的可证伪锚点正是「heredoc 零改动」。本 Spec 把「凭据不要放命令行参数, 改用 env / --config / stdin」写进 SOT `standards/conventions/secret-hygiene.md` (precedent 笔记指出的自然落点, 示例须逐工具实跑), hook 文案零改动; 在「待 owner 复议」里如实列出三个选项 (A 不改文案只落 SOT / B 全局加一句 / C 先解 10CG/aria-plugin#132 再做定向提示) 与主控推荐 A 的理由。
- **L3 additionalContext 的改动**只加「命中 tag 名单 + 来源 (工具名、Read 的 file_path)」这类描述性信息, 不改处方性措辞; rule6_note 里逐 hunk 判定它属于描述性还是处方性, 并给 SOT 依据。precedent 笔记指出 WP-A 是第一份必须按 SOT §4.1 五字段写 rule6_note 的 hook Spec: 写全五字段; 代码 hunk 与文案 hunk 若判定不同, 分两块写并说明理由。
- **FP 白名单必须含 `[REDACTED` 前缀**: L2 wrapper 对 token / sha1 / client_secret / secret 四键输出 `[REDACTED-BY-WRAPPER len=N]` 占位串; 给 L3 加 token / sha1 而不放行这类占位, 每次 wrapper 调用都会恒红。用 SC 钉住。
- **变量间接**: 部分修复 (同一命令串内的字面赋值) + 残余写成 KNOWN-LIMIT (08-02 SC-8 体例), 并引用同一架构面的在案 issue (precedent 笔记所列 10CG/aria-plugin#138 / #140 / #142, 引用时全限定), 不宣称根治。
- **哈希指纹口径**与仓内已有口径对齐 (`.aria/pat-inventory.yaml` 的 sha256-hex-prefix-8、`secret-guard.sh` 已有的 sha256sum fail-soft 先例), 并处理无 `sha256sum` 平台的 fail-soft。
- **`\.env` 边界写法**在 `[^A-Za-z0-9_]` (issue 建议, 会放过 `.env_prod` 这类下划线后缀名) 与不把下划线当边界的写法之间, 用两面测试选定并写明 fail 方向。
- **Level 2 对账**: 在 Spec 里记一条对账 (LEVEL_GUIDE「影响多个子模块自动 L3」vs 决策单第 3 项已裁 L2 与四份同型 Spec 先例)。
- **issue 收尾口径 (写进 Impact)**: ship 后 10CG/aria-plugin#154 可按授权评论并关闭; 10CG/aria-plugin#203 与 10CG/Aria#221 属决策单第 2 项的轮换延后集, **保持 open**, 只评论代码侧进展、不涉轮换; 该口径列入「待 owner 复议」。
- **陈旧头注释**: 本 Spec 触及的文件里的陈旧 / 悬空表述 (precedent 笔记所列 secret-guard.sh 的「Phase 2 ... redacts」与悬空 runbook 引用、secret-scan.sh 的计数与非目标声明、secret-hygiene.md 把 secret-guard 称作 Write/MultiEdit blocker、三处 599/593 与 49 计数) 并入文档同步; 其中 secret-scan 的 49 计数目前没有等价于 SC-13 的机械断言, 说明本 Spec 是否补。
- **推送保护**: 新夹具一律运行时拼装 (GitHub 镜像的 push protection 只放行两个既有测试文件); Spec 与证据文件只用占位写法。
- **命名**: change-id = `secret-net-l3-and-bypass-paths` (审计报告与 Spec 目录用它); claim track-id = `secret-net-l3-and-bypass-paths-023236f2` (按 phase-a-planner 的 `<slug>-<uuid>` 规则)。

---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: false
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
drift_warning: false
is_refocus: false
verdict: FAIL
timestamp: 2026-09-30T22:18:06.000Z
context: openspec/changes/secret-net-l3-and-bypass-paths/proposal.md
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
counts_raw: 8C/25M/42m
counts_dedup: 6C/24M/39m
sibling_probe: no_sibling_found
---

# post_spec R1 聚合 — secret-net-l3-and-bypass-paths — 未收敛

> 本节为机械聚合 (脚本从运行记录生成; 各席报告原文见同目录同轮次文件)。主控独立核验与处置意见见文末「主控记录」节。

## 判定

| 席 | verdict | counts (自报) | counts (按 findings 计) | vote | 报告文件 |
|---|---|---|---|---|---|
| tech-lead | FAIL | 3C/3M/8m | 3C/3M/8m | REVISE | `post_spec-R1-2026-09-30T221806-000Z-secret-net-l3-and-bypass-paths-tech-lead.md` |
| backend-architect | FAIL | 2C/4M/5m | 2C/4M/5m | REVISE | `post_spec-R1-2026-09-30T221806-000Z-secret-net-l3-and-bypass-paths-backend-architect.md` |
| qa-engineer | FAIL | 1C/6M/8m | 1C/6M/8m | REVISE | `post_spec-R1-2026-09-30T221806-000Z-secret-net-l3-and-bypass-paths-qa-engineer.md` |
| code-reviewer | FAIL | 1C/6M/11m | 1C/6M/11m | REVISE | `post_spec-R1-2026-09-30T221806-000Z-secret-net-l3-and-bypass-paths-code-reviewer.md` |
| knowledge-manager | FAIL | 1C/6M/10m | 1C/6M/10m | REVISE | `post_spec-R1-2026-09-30T221806-000Z-secret-net-l3-and-bypass-paths-knowledge-manager.md` |

## 全部 finding (按席位原编号, 不转述)

| 席 | 编号 | 键 (重算) | 席位所写 id | severity | type | category | scope | summary (席位原文) |
|---|---|---|---|---|---|---|---|---|
| tech-lead | C1 | `e8d39a8a` | `e8d39a8a` | critical | issue | implementation | proposal.md What.W3 | W3 把 $ / < / {{ 值前缀放行延伸到既有 json-secret-field, 且放行 span 仍被哨兵消费 ⇒ 基线检出的 {"password":"$2b$…"} / crypt 哈希 / 以 $ 或 < 起头的生成口令变为静默 (检出回退, SC-29 与全部 SC 看不见) |
| tech-lead | C2 | `7e0343bd` | `7e0343bd` | critical | issue | architecture | proposal.md What.W9 | W9 扩展代码在 Read/Edit 面与主体 (per-segment 子 shell 之外) 的运行期故障 exit 1 = PreToolUse 放行, 连内建拦截一起失效; W14「任何未绑定变量都 fail-closed」只对子 shell 成立, W9 两条隔离保证无机制兜底, 验收测不到 (故障注入实测) |
| tech-lead | C3 | `e600e931` | `e600e931` | critical | issue | implementation | proposal.md What.W12 | W12 按字面改三行后 python3 -c 的整环境转储 (print(os.environ) / dict(os.environ) / .items() / os.environ['X'] / os.environb) 由 exit 2 变 exit 0, 与 printenv 同类却被当误报放行, SC-23 无守卫行 (字面实现实测) |
| tech-lead | M1 | `44b5bb44` | `44b5bb44` | major | issue | testing | proposal.md SC-32 | SC-32 把「bash 3.2 可跑」缩为 5 个构造的静态 grep; 解析类不兼容使脚本以上一条状态 (0/1) 退出 = 整层静默放行而非死锁, 无 bash 3.2 运行腿, [[ -v ]] 等坏实现测不出 |
| tech-lead | M2 | `e2459206` | `e2459206` | major | issue | architecture | proposal.md What.W11 | W11 为 ps 族新增 nomad alloc exec / pct exec / ssh 包裹, 但同包裹下的 env / printenv 整环境转储基线放行 (docker/kubectl/podman/lxc exec 已拦), Spec 既不补也不申报, SC 两不钉 |
| tech-lead | M3 | `d8e7b380` | `d8e7b380` | major | risk | architecture | proposal.md What.W14 | L1 5s 超时 = 放行, 而 W8/W11 重行、W9 每次读文件、W10 第二遍判定都加延迟; 无 SC 约束新路径延迟, 未钉「内建判定先于替换副本/扩展」的求值顺序, SC-30 五档不走这些路径 (基线 600 段已 3.69s) |
| tech-lead | m1 | `5ac56a9f` | `5ac56a9f` | minor | decision | documentation | proposal.md What.W11 | W11 否决 updatedInput 的「两 hook 并行改写竞态」前提不成立 (host-docker-logout-guard 从不产出 updatedInput), 结论应由意图保持单独支撑 |
| tech-lead | m2 | `efd4c1c5` | `efd4c1c5` | minor | issue | documentation | proposal.md 待 owner 复议.7 | Grep 工具是 W8.3/W9 Read 面保护的同族旁路 (两层 matcher 均不含 Grep), Spec 只记了 L3 一侧, L1 侧未申报为已知限制 |
| tech-lead | m3 | `f410df76` | `f410df76` | minor | issue | documentation | proposal.md Impact | MINOR 依据误引 CLAUDE.md (原文是「新增 Skill」, 实际支撑为 version-management.md §2.2); 发版同步面漏 README.md:242、三份 i18n README badge/Plugin Version 行、CLAUDE.md:138/142 |
| tech-lead | m4 | `68e80369` | `68e80369` | minor | issue | documentation | proposal.md What.W4 | W4「键形 tag 取值、其余取整个 span」中「键形 tag」未定义; 整 span 哈希与其用来拒绝加盐的 pat-inventory 可比性理由矛盾 |
| tech-lead | m5 | `684e9a24` | `684e9a24` | minor | issue | documentation | proposal.md What.W9 | 扩展条目在 Bash 面只对打印型读取器生效, 不含 W8 为 app.ini 扩充的 python3 -c / node -e 源组, 不对称未申报 |
| tech-lead | m6 | `ab625935` | `ab625935` | minor | decision | architecture | proposal.md What.W9 | 扩展「超限整体忽略 + 静默」是悬崖 (第 201 条让全部失效); 平台 systemMessage (所有 hook, exit 0 亦可) 可让失效可见, Spec 未考虑 |
| tech-lead | m7 | `bdf4778c` | `bdf4778c` | minor | issue | documentation | proposal.md Out of scope | SC-28 订正 secret-scan.sh 头注释多处, 却保留 :15-20「exposes no field / not version-dependent」, 与本 Spec :40 的二进制实测直接矛盾 |
| tech-lead | m8 | `60eea71e` | `60eea71e` | minor | issue | testing | proposal.md SC-26 | SC-26b 声称 §2.5 有 pgrep -a 行, 探针实际对全文件任意行判定, pgrep -a 写在别处的坏实现测不出 |
| backend-architect | C1 | `14b7e703` | `14b7e703` | critical | issue | architecture | proposal.md What.W3 | W3 把 `<`、`$`、`{{` 前缀白名单延伸到既有 `json-secret-field`, 使基线已检出的真实形态 (`$`/`<` 开头口令、JSON 里的 bcrypt 哈希) 变静默并被哨兵吞掉; 实测基线 5/5 告警、字面原型 5/5 静默, 收窄原型保持告警且通过同一探针, 验收因生成器排除这些首字符而看不见。 |
| backend-architect | C2 | `179045cd` | `179045cd` | critical | issue | architecture | proposal.md What.W12 | W12 的 `\.env` 右边界改动使 python3 -c 的 `os.environ` 整表导出 (print / dict / items / copy / json.dumps / environb) 从 exit 2 变 exit 0, 等价放行 `printenv`; Impact 与 SC-23 均未识别, 无整表导出的 reverse-guard。 |
| backend-architect | M1 | `a3054a20` | `a3054a20` | major | issue | testing | baseline_probe.py value generators; proposal.md SC-5 SC-9 SC-11 | 探针生成器 BAD_FIRST 排除 `/ + - _ $ <` 开头的值, 且 W2 路径形只有散文定义; 严格与宽松两种读法通过同样的全部探针行, 但 `/` 开头的 std-b64 凭据 (约 1.6%) 在宽松版静默。 |
| backend-architect | M2 | `d4bcaf7c` | `d4bcaf7c` | major | issue | architecture | proposal.md What.W9 What.W10 Impact.性能预算 | W9 扩展条目与 W10 变量展开延迟无上界且无 SC: 200 条逐条正则实测 200 段 11 s (基线 1.7 s), 约 130 段起越过 hooks.json 的 5 s 超时而被放行; SC-8 五档与 SC-31 都不覆盖该负载, glob 预筛可把成本压到约 1.4 s。 |
| backend-architect | M3 | `7deac83f` | `7deac83f` | major | decision | architecture | proposal.md Impact.issue 收尾口径 待 owner 复议.3 | 待复议 3 默认理解 A (在 #203/#221 评论代码侧进展) 对决策单第 2 项「本项之下不评论」的含糊原话选了动手, 且是不可收回的外向动作; 另 #154 关闭可能早于 post-ship 端到端复验。 |
| backend-architect | M4 | `719ae05c` | `719ae05c` | major | issue | testing | proposal.md SC-19 SC-20 | SC-19/20 只用 `.` 与 `+` 验证字面子串, 仅转义这两个字符的实现也全绿; 实测含 `(`、`[` 的条目不匹配, 组合正则里一条未配对 `(` 使全部扩展条目静默失效 (rc=2)。 |
| backend-architect | m1 | `1b61303c` | `1b61303c` | minor | issue | implementation | proposal.md What.W2 已知限制 SC-9 SC-10 | W2 漏报/误报类清单不全: Python dict repr 单引号、含符号口令、JSON 套 JSON、HTTP/2 小写头名漏报; 校验和 JSON 的 sha1 键、Basic 文档示例、TOKEN_ID 的 uuid 值误报, 均未成文也未钉住。 |
| backend-architect | m2 | `369a8b32` | `369a8b32` | minor | issue | implementation | proposal.md What.W4 SC-12 | W4 指纹取值对象在头部/参数/URL/PEM 类 tag 上未定, 整 span 哈希与 pat-inventory 的 token 原文指纹不可比, 排序规则含糊, SC-12 只覆盖 json-secret-field。 |
| backend-architect | m3 | `b9d73d73` | `b9d73d73` | minor | issue | documentation | proposal.md What.W12 jq | `map_values(length)` 对数值型字段会原样回显 (jq 1.6 实测 `{"pin":483920}`), 「只出元数据」的前提不成立, 应补 KNOWN-LIMIT。 |
| backend-architect | m4 | `60eea71e` | `60eea71e` | minor | issue | testing | proposal.md SC-26 | SC-26 文字说 §2.5 有 `pgrep -a`, 探针对整份文件任一行匹配即过, 且是短语匹配, 可被为过检查器而写的内容满足。 |
| backend-architect | m5 | `c941e4e1` | `c941e4e1` | minor | issue | implementation | proposal.md What.W8 | W8 名字组右边界与左前缀未定: `app.ini.tpl` / `.example` / `.go` 被拦, `/srv/git-forgejo/app.ini` 因前置白名单漏拦, `cp` 后读副本放行未在已知限制中写明。 |
| qa-engineer | C1 | `f42265a1` | `f42265a1` | critical | issue | implementation | proposal.md What.W12 + SC-23 (23a/23b) | W12 的 `\.env` 右边界使 python3 -c 内 os.environ 整体放行, 含整环境转储 (print(os.environ)/dict(os.environ)/items 循环, 基线 exit 2 变目标 exit 0), printenv/env/node process.env 仍拦, L3 对 repr 形零告警; SC-23 无转储反向守卫且 23b 把放行写成必达 (安全回退) |
| qa-engineer | M1 | `ab6a3123` | `ab6a3123` | major | issue | testing | proposal.md SC-23 23f (怎么会红) | SC-23 23f 强制 .env_prod/.env_local 经解释器读取由拦变放, 并把更保守的 [^A-Za-z0-9] 边界列为坏实现; 保守写法同样修好 issue 点名的 os.environ 误拦且不回退 |
| qa-engineer | M2 | `8645b99f` | `8645b99f` | major | issue | implementation | proposal.md What.W3 白名单 (:77, :83) / SC-11 | W3 对既有 json-secret-field 整类放行以 <、$、{{ 开头的值, 基线检出的随机符号口令变静默 (检出回退), :83 称『须人为构造』不实; 应改为整体包裹形态白名单并补 SC-11 反向行 |
| qa-engineer | M3 | `1c0bc16f` | `1c0bc16f` | major | issue | testing | proposal.md SC-7 / SC-10 / SC-11 (W2-W3 反向守卫) | L3 反向守卫缺负向侧: 33 个坏实现变体中 5 个存活 (熵下限套到既有 json 键、含式白名单、大小写不敏感白名单、须含数字、env-line 套白名单), 114 行探针与 SC-29 均抓不到 |
| qa-engineer | M4 | `634eac5c` | `634eac5c` | major | issue | testing | proposal.md What.W4 / SC-12 | W4 未枚举『键形 tag』, 按字面 env-line/bearer/x-api-key/URL 类 fp=sha256(整 span) 与 pat-inventory 台账不可比; SC-12 只验单值 json-secret-field, 多值/上限 10/出现序/provider/env-line 无行 |
| qa-engineer | M5 | `8e77d1ca` | `8e77d1ca` | major | issue | testing | proposal.md SC-9 / What.W2 已知限制 / 执笔自报薄弱点 3 | W2 最终设计无语料级误报验收: 本仓 1188 文件上字面设计的新 tag 命中 14 处/9 文件全为假阳 (含 const JWT_SECRET = process.env.JWT_SECRET), W1 使 Read 进入扫描面后会常态化为恒红零信息 |
| qa-engineer | M6 | `27f6c3ce` | `27f6c3ce` | major | issue | documentation | proposal.md What.W9 / What.W13 / SC-26 | W9 新增的 .aria/secret-guard.paths 采用方输入面 (格式/限额/静默失效/项目根规则) 与 W8 服务端配置族无任何文档落点, 同步面清单与 SC-26/28 均未覆盖 |
| qa-engineer | m1 | `47c3900d` | `47c3900d` | minor | decision | architecture | proposal.md Impact.issue 收尾口径 / 待 owner 复议 3 | 复议 3 默认 A 会在 owner 未裁前对 #203/#221 发评论, 与决策单第 2 项『本项之下不评论』字面冲突的一侧; 默认改 B 零成本 |
| qa-engineer | m2 | `7d4fec1c` | `7d4fec1c` | minor | issue | testing | proposal.md What.W11 / SC-22 (Read 面) | W11 新拦截族无 Read 工具面: Read /proc/<pid>/cmdline\|environ 基线与目标均 exit 0, 未声明 KNOWN-LIMIT |
| qa-engineer | m3 | `b976c610` | `b976c610` | minor | issue | implementation | proposal.md What.W2 熵下限 (路径形判据) | 路径形判据要求首段小写, /Users/…、~/Library/…、prod/app/… 等 macOS 路径与相对名仍告警 |
| qa-engineer | m4 | `d70f228c` | `d70f228c` | minor | issue | testing | proposal.md SC-23 / SC-24 (issue 点名形态) | SC-23 缺 issue 原文多行 nomad alloc exec + python -c 形态行, SC-24 未钉 issue 点名的 map(.key) |
| qa-engineer | m5 | `b5bbd88c` | `b5bbd88c` | minor | issue | testing | proposal.md SC-18 / SC-19 (Read/Edit 面 nonce 与大小写) | W8/W9 的 Read/Edit 拦截承诺走 SECRET_GUARD_ACK_PATH nonce 逃生口却无行验证; W9 条目未测混合大小写 (Read 面对 lower_path 匹配) |
| qa-engineer | m6 | `6b5eb047` | `6b5eb047` | minor | risk | testing | proposal.md SC-32 / What.W10 (bash 3.2) | bash 3.2 可跑仅由 SC-32 的 5 种构造 grep 作证, W10 要求替换串加引号的 bash 3.2 语义未验 (本机只有 bash 5.2.15) |
| qa-engineer | m7 | `a0cb1abc` | `a0cb1abc` | minor | issue | documentation | proposal.md SC-26 / SC-28 (doc-sync 判据强度) | SC-26a 词元堆砌即过、SC-28f 删句即过, doc-sync 判据判别力弱 |
| qa-engineer | m8 | `9519ae32` | `9519ae32` | minor | issue | documentation | proposal.md Impact.覆盖关系 (10CG/aria-plugin#154 全覆盖) | 覆盖关系写 #154 全覆盖, 但 issue 评论 19339 的阈值是 {8,} 而 W2 统一 16 (SC-10 10c 钉住 12 位静默), 偏离未在覆盖关系行点明 |
| code-reviewer | C1 | `e8d39a8a` | `e8d39a8a` | critical | issue | implementation | proposal.md What.W3 | W3 把「值以 $ / < 开头即不计数」延伸到既有 json-secret-field 且放行 span 仍被哨兵吞掉: crypt 格式口令哈希与以 $ 开头的真值在 JSON 凭据键上由检出变静默 (基线 5/5 检出, 按 W3 字面原型 4/4 静默, token 键经新 tag 同理); 「须人为构造」不成立, 探针生成器排除首字符类致 SC 结构上测不到 |
| code-reviewer | M1 | `d9308fba` | `d9308fba` | major | issue | implementation | proposal.md What.W12 | \.env(rc)?([^A-Za-z0-9_]\|$) 让字母/数字后缀名 (含 cookiecutter-django 的 .envs/.production/*、.env2、.envprod) 经 python3 -c / node -e 由 exit 2 变 exit 0, 申报与 SC-23 只覆盖下划线后缀; 更优替代是只豁免 .environ/.environb/.environment 词元 |
| code-reviewer | M2 | `53c140c4` | `53c140c4` | major | issue | documentation | proposal.md Impact.同步面 (W9 扩展入口文档) | 新采用方配置面 .aria/secret-guard.paths (字面子串、4-200 字符、32 KiB/200 条上限、失效静默) 在同步面与 doc-sync SC 中没有任何用户面文档落点 (README Hooks 小节 / secret-hygiene.md §5), 违反规则 #3, #203 诉求的扩展入口不可发现 |
| code-reviewer | M3 | `9db51a43` | `9db51a43` | major | issue | implementation | proposal.md What.W11 /proc 放宽 | 放宽既有 /proc 行 (任意 pid token + grep/sed 等新读取器) 时把 status 一并放宽, grep VmRSS /proc/123/status 等三种只读 metadata 检查由 exit 0 转 exit 2, 与「/proc/N/status 本 Spec 不动」自相矛盾, 未申报、无 SC |
| code-reviewer | M4 | `2ce0049b` | `2ce0049b` | major | issue | implementation | proposal.md What.W4 | 「键形 tag 取值、其余 tag 取整个 span」未定义键形 tag; FORGEJO_TOKEN=/Bearer/X-API-Key 等最常见 PAT 形态落在既有 tag 上, 按 span 算的 fp 与 #154「命中值的 sha256 前 8 位」及 pat-inventory「sha256(token 原文)」都对不上, SC-12 只测 json-secret-field |
| code-reviewer | M5 | `d9986b27` | `d9986b27` | major | issue | testing | proposal.md SC-13 | 13d 只做处方句包含判断, 证伪不了 W5 / rule6_note 块 B 依赖的「其余字节与基线逐字节一致」; 实跑一个追加处方性指令的坏实现, 13b/13d/13e/13f 全为真 |
| code-reviewer | M6 | `44b5bb44` | `44b5bb44` | major | issue | testing | proposal.md SC-32 | SC-32 以 5 项黑名单代替「bash 3.2 可跑」, [[ -v ]] (4.2)、nameref / 负下标 (4.3)、@Q (4.4) 全部放行 (探针同一判定式实跑); macOS bash 3.2 正是 secret-guard 全量 fail-closed 死锁的历史发生面 |
| code-reviewer | m1 | `26c4c8b4` | `26c4c8b4` | minor | issue | documentation | proposal.md What.W4 引用 secret-guard.sh:624 | W4 引用 secret-guard.sh:624 的 ${hash:-unknown}, 实读该表达式在 :626 (:624 是 hash 赋值) |
| code-reviewer | m2 | `60eea71e` | `60eea71e` | minor | issue | testing | proposal.md SC-26 | SC-26 26b 声称检查「§2.5 有一行含 pgrep -a」, 探针 _sot_ps_row 实际扫全文任意行 |
| code-reviewer | m3 | `5856b370` | `5856b370` | minor | issue | testing | proposal.md SC-4/SC-9 + baseline_probe.py 值生成器 | 4h/9h (token_last_eight 8 hex) 与 9l/9m ($VAR 13-14 字符) 被 16 字符下限单独静默, 转不红其声称的名表封闭性/$ 白名单/值字符类; 生成器 _ok 排除首字符类, 分类器首字符边界无任何行覆盖 |
| code-reviewer | m4 | `23cb20d9` | `23cb20d9` | minor | issue | testing | proposal.md SC-20 | SC-20 未测 W9 列出的「不可读」失效类, 且六种坏文件只测 Bash 面; Read/Edit 分支在顶层不在 fail-closed 子 shell 内 (未绑定变量实测退出码 127 即不阻断), W9 未规定扩展检查的位置 |
| code-reviewer | m5 | `41434a8e` | `41434a8e` | minor | issue | implementation | proposal.md What.W11 ps <pid> 形态 | BSD 形态 ps <pid> 输出 COMMAND (完整命令行, 本机表头实测), 基线放行; W11 只认字母选项簇, 既不拦也未列 KNOWN-LIMIT |
| code-reviewer | m6 | `81da6556` | `81da6556` | minor | risk | architecture | proposal.md What.W4 与 aria-plugin#92 接缝 | DEC-20260703-001 把事件记录 schema / redaction 安全划给仍 open 的 aria-plugin#92, W4 改日志事件字段但全文不提 #92, 接缝未声明 |
| code-reviewer | m7 | `a6304dd1` | `a6304dd1` | minor | issue | testing | proposal.md SC-28 | SC-28 各行只查旧文本消失 / change-id 出现, 删掉整段也绿, 不验证替换后的文本 (如 28f 不查 file.content 形状在场) |
| code-reviewer | m8 | `78425781` | `78425781` | minor | issue | implementation | proposal.md What.W9 解释器读取 | W9 扩展条目只与打印型读取器组合, python3 -c / node -e 读扩展路径放行且未列已知限制 (W8 对 app.ini 显式覆盖了解释器) |
| code-reviewer | m9 | `6de9b7e2` | `6de9b7e2` | minor | issue | documentation | proposal.md Impact.同步面 (主仓 i18n 徽章) | 同步面只列 root README badge, 漏主仓 README.zh/ja/ko.md 第 10 行各一枚 Plugin 版本徽章 (有 state-check 兜底) |
| code-reviewer | m10 | `61c4987f` | `61c4987f` | minor | issue | documentation | proposal.md rule6_note 块 A | 块 A 写 decision_table_row: n/a (SOT §4.1 = 不属 Skill 变更) 又自称沿用 owner 2026-08-02 substitute 框定; 该先例记录 owner 裁定二者逻辑二选一并统一为 substitute |
| code-reviewer | m11 | `0061040b` | `0061040b` | minor | issue | implementation | proposal.md What.W12 jq map_values(length) | jq length 对数字返回绝对值 (实跑 -4821 -> 4821), map_values(length) 对数值字段并非只出元数据, 应列 KNOWN-LIMIT |
| knowledge-manager | C1 | `e8d39a8a` | `e8d39a8a` | critical | issue | implementation | proposal.md What.W3 | W3 把 $、<、{{ 当整体前缀放行并延伸到既有 json-secret-field, 使基线可检出的真实形值 (JSON password 里的 $2b$12$… 口令哈希、$ 起头的人工口令) 由告警变静默, 而 Spec 的验收与已知限制都放过它。 |
| knowledge-manager | M1 | `5831f8c0` | `5831f8c0` | major | issue | testing | proposal.md SC-26 | SC-26 两条判据是全文件任一行同时含若干子串, Spec 自己要求追加的版本历史行即可单独满足, §2.5 行与正例条款不写也绿 (坏实现实测为绿)。 |
| knowledge-manager | M2 | `ba98e41f` | `ba98e41f` | major | issue | documentation | proposal.md Impact.同步面 | Impact 列的主仓版本点与发版同步面少列实际必改项: 近两次发版同步提交各改 8 个内容文件、16 个版本点 (含 CLAUDE.md 两处与三份 i18n README), Spec 只点名约 4 个, Tasks 无承载任务行。 |
| knowledge-manager | M3 | `b73ab606` | `b73ab606` | major | issue | documentation | proposal.md What.W9/W13/W14 | 新增的采用方入口 .aria/secret-guard.paths、已知限制与五向行为变更申报都没有指定文档落点 (SOT / hook 头注释 / CHANGELOG), SC-26/27/28 也不验。 |
| knowledge-manager | M4 | `cf0ae932` | `cf0ae932` | major | issue | documentation | proposal.md 全文 (研究笔记引用) | Spec 把只存在于会话 scratchpad 的四份研究笔记及其原型/普查/矩阵当证据引用约 47 处, 归档后全部悬空, 且 B.2 的同一语料复跑与待复议 7 的证据位置不可执行。 |
| knowledge-manager | M5 | `846b21f8` | `846b21f8` | major | issue | documentation | proposal.md What.W13 | W13 新增的凭据不要放命令行参数正例与同一 SOT 现有推荐示例 (§3.1/§3.2/§3.4/§3.5/§4.4 的 argv KEY=…) 直接冲突, Spec 没有安排对账, SC-26 也测不出。 |
| knowledge-manager | M6 | `2779a016` | `2779a016` | major | issue | documentation | proposal.md Impact.issue 收尾口径 | 对 10CG/aria-plugin#203 与 10CG/Aria#221 的 ship 后评论, Spec 默认取理解 A 并声明未裁前按默认执行, 与决策单第 2 项执行注字面本项之下不评论相反, 默认方向不够保守。 |
| knowledge-manager | m1 | `b7387216` | `b7387216` | minor | issue | documentation | proposal.md Impact.覆盖关系 | 10CG/aria-plugin#154 全覆盖/三件交付物全部落地 与 W2/W4 对评论 19339 字面参数 (值长 8 与指纹前 8 位) 的有意偏离不符, 关单评论须披露。 |
| knowledge-manager | m2 | `d8e2f426` | `d8e2f426` | minor | issue | documentation | proposal.md Impact.同步面 / What.W5 (决策单复述) | 决策单复述不精确: 授权边界少列主仓 PR 的合并与删除远端分支, 四枚待轮换凭据把四张 issue 当成四枚凭据。 |
| knowledge-manager | m3 | `8e1df30a` | `8e1df30a` | minor | issue | documentation | proposal.md Impact.版本定级 | 版本定级依据误引 CLAUDE.md (原文为新增 Skill/Skill 架构重构=MINOR+), 且本族先例 v1.66.3/v1.66.4 为 PATCH; 应改引 version-management.md §2.2。 |
| knowledge-manager | m4 | `852deadc` | `852deadc` | minor | issue | testing | proposal.md Impact.与 10CG/Aria#199 的接缝 | 接缝守卫命令用了 10CG/Aria#199 已淘汰的弱写法 (无 -C、无 rc 判据, 无输出即通过), 子目录或 git 失败时空过。 |
| knowledge-manager | m5 | `381efd94` | `381efd94` | minor | risk | documentation | proposal.md 执笔自报薄弱点 | 执笔自报薄弱点是 v1 时点的审计叙事, 不属 Spec 交付面且随修订必然过时, 存在重演审计叙事与交付面同居一文的风险。 |
| knowledge-manager | m6 | `0f70cf57` | `0f70cf57` | minor | issue | documentation | proposal.md header Level 对账 | Level 对账只引 LEVEL_GUIDE 一条且为合并转述, 未列模板的 >10 files 与 1-3 days 判据, 待复议 4 的判据列举不全。 |
| knowledge-manager | m7 | `67e73dab` | `67e73dab` | minor | risk | documentation | proposal.md What.W13 (BLOCKED 文案) | 共享 BLOCKED 文案的 Acceptable filters 把锚定 grep 列为可接受而 tight 族仍拦, Spec 把 tight 族增至 4 个并冻结文案, 未记录该不一致, 待复议 2 选项集也未含此点。 |
| knowledge-manager | m8 | `a1d19fe7` | `a1d19fe7` | minor | issue | documentation | proposal.md What.W4 / What.W12 | W4 与 W12 漏链两个在案 issue (10CG/aria-plugin#92 事件记录闭环、10CG/aria-plugin#131 尾边界), 待复议 7 开单前也未去重。 |
| knowledge-manager | m9 | `b63b7640` | `b63b7640` | minor | risk | documentation | proposal.md rule6_note / Rule #7 | Rule #7 申报散落 (全文无该字样), 且 post-ship 腿须让像凭据的值出现在真实会话输出里, 取值规程未写。 |
| knowledge-manager | m10 | `a6304dd1` | `a6304dd1` | minor | issue | testing | proposal.md SC-28 | SC-28 的 9 条陈旧表述判据只验旧串消失 (删除即绿) 不验改为, 计数句被替换成新字面数字会重演陈旧计数。 |

## 收敛计算 (本仓先例口径: 相邻两轮 Critical+Major 键集相等 且 全票 PASS)

- 本轮 Critical+Major 键集 (30): `14b7e703`, `179045cd`, `1c0bc16f`, `2779a016`, `27f6c3ce`, `2ce0049b`, `44b5bb44`, `53c140c4`, `5831f8c0`, `634eac5c`, `719ae05c`, `7deac83f`, `7e0343bd`, `846b21f8`, `8645b99f`, `8e77d1ca`, `9db51a43`, `a3054a20`, `ab6a3123`, `b73ab606`, `ba98e41f`, `cf0ae932`, `d4bcaf7c`, `d8e7b380`, `d9308fba`, `d9986b27`, `e2459206`, `e600e931`, `e8d39a8a`, `f42265a1`
- 第 1 轮无上一轮可比, 按算法不可收敛, 必须进入下一轮
- unanimous_pass = False (0 PASS / 5 REVISE)
- converged = False

## 机械核对

- 席位数 5 / 5; incomplete = False
- frontmatter 开头: tech-lead=ok, backend-architect=ok, qa-engineer=ok, code-reviewer=ok, knowledge-manager=ok
- 自报 counts 与 findings 计数不一致的席: 无
- finding id 与四元组重算不一致: 0 条
- 竞品 Spec 探针 (本轮入口): status=ok / verdict=no_sibling_found

## 主控记录

> 2026-10-01 主控追加。只在这里写主控的核验与裁定; 上面各节是脚本生成的机械聚合, 未改动。

### 席位间同题归并 (定稿键)

| 簇 | 问题 | 席位编号 (键) | 定稿键 / 级别 |
|---|---|---|---|
| A | W3 把 `$` / `<` / `{{` 前缀白名单延伸到既有 `json-secret-field`, 基线检出的 `$2b$…` 口令哈希、`$` / `<` 开头的口令变静默 (检出回退) | tl/C1 `e8d39a8a` · ba/C1 `14b7e703` · cr/C1 `e8d39a8a` · km/C1 `e8d39a8a` · qa/M2 `8645b99f` | `e8d39a8a` critical |
| B | W12 的 `\.env` 右边界使 `python3 -c` 的 `os.environ` 整表导出由拦变放 (等价放行 printenv) | tl/C3 `e600e931` · ba/C2 `179045cd` · qa/C1 `f42265a1` | `e600e931` critical |
| B2 | 同一边界让 `.env2` / `.envprod` / `.envs/` 由拦变放; SC-23 23f 把更保守写法列为坏实现 | cr/M1 `d9308fba` · qa/M1 `ab6a3123` | 两键 major |
| C | W9 扩展入口: 运行期故障在子 shell 外 exit 1 = 放行 (连内建规则一起失效) | tl/C2 `7e0343bd` | critical |
| C2 | W9 / W10 新路径延迟无上界 (约 130 段即越过 5 s 超时而放行) | ba/M2 `d4bcaf7c` · tl/M3 `d8e7b380` | 两键 major |
| C3 | W9 字面子串的转义测试不足 (含 `(` `[` 的条目失配 / 一条未配对 `(` 使全部扩展失效) | ba/M4 `719ae05c` | major |
| C4 | W9 扩展入口与 W8 配置族、已知限制、行为变更申报都没有文档落点 | cr/M2 `53c140c4` · qa/M6 `27f6c3ce` · km/M3 `b73ab606` | 三键 major |
| D | W4 指纹口径: 「键形 tag」未定义, 既有 tag 按整 span 哈希与 pat-inventory「sha256(token 原文)」不可比, SC-12 覆盖窄 | qa/M4 `634eac5c` · cr/M4 `2ce0049b` (+ tl/m4) | 两键 major |
| E | SC-32 用 5 项静态黑名单代替「bash 3.2 可跑」, 测不出 `[[ -v ]]` / nameref / `@Q` 等 | tl/M1 · cr/M6 `44b5bb44` | major |
| F | W11: ssh / pct exec / nomad alloc exec 包裹下的 env / printenv 整环境转储未处理也未申报; 放宽 `/proc` 行误拦 `/proc/N/status` | tl/M2 `e2459206` · cr/M3 `9db51a43` | 两键 major |
| G | W13 新条款与 SOT 现有 argv `KEY=…` 示例冲突, 未安排对账 | km/M5 `846b21f8` | major |
| H | Impact: 10CG/aria-plugin#203 / 10CG/Aria#221 ship 后评论的默认理解取了「动手」一侧 (与决策单第 2 项「本项之下不评论」相反); 发版同步面少列 (16 个主仓版本点) | ba/M3 `7deac83f` · km/M6 `2779a016` (+ qa/m1) · km/M2 `ba98e41f` | 三键 major |
| I | Spec 约 47 处引用只在会话 scratchpad 里的研究笔记, 归档后悬空 | km/M4 `cf0ae932` | major |
| J | SC 可证伪性: SC-13 证伪不了「其余字节不变」; SC-26 全文件任意行即过; 反向守卫缺负向侧 (33 个坏变体存活 5 个); 探针生成器排除 `/ + - _ $ <` 首字符; 新 tag 无语料级误报验收 (本仓 14 处命中全为假阳) | cr/M5 `d9986b27` · km/M1 `5831f8c0` · qa/M3 `1c0bc16f` · ba/M1 `a3054a20` · qa/M5 `8e77d1ca` | 五键 major |

### 主控独立核实

- 簇 A: 实读 proposal v1 W3 改动条原文 —— 「值以下列任一开头即不计数: … `<`、`$`、`{{` …; **作用范围** = 6 个新 tag + 既有 `json-secret-field`」, 前提属实。
- 簇 B: 实读 W12 —— 三行改为 `\.env(rc)?([^A-Za-z0-9_]|$)`, `.environ` 中 `.env` 后接 `i` 不再命中, 前提属实; 三席各自实测整表导出由 exit 2 变 exit 0。
- 簇 C: 实读 W9 —— 只写了失败语义 (扩展失败只丢扩展), 没有规定扩展判定在脚本中的位置与出错处理; Claude Code PreToolUse 只有 exit 2 阻断, 其它非零退出放行, tl/C2 的故障注入结论成立。
- 旁证: 主控写本记录时, 一条 `python3 -` heredoc 命令因正文提到 `\.env` 被现行 secret-guard 拦下 (内联解释器 + `.env` 子串), 正是 W12 要处理的误拦形态; 改用 Write 工具落文件后再拼接。

### 主控裁定 (v2 返修据此执行; 均为技术级, 列入 handoff 请 owner 复议)

1. **W3**: 白名单只认**整值占位形态**, 不认单字符前缀 —— 例如整值是尖括号占位、`${VAR}` / `$VAR` 形的变量引用、`{{…}}` 模板、`[REDACTED…]`、全掩码, 或以 FAKE / PLACEHOLDER / NOT-REAL / REDACTED 这类刻意标记词开头; `$2b$…` 口令哈希与 `$` / `<` 开头的随机值必须仍被检出 (补反向守卫行)。具体正则与「被放行的 span 是否仍被哨兵消费」由执笔给出并论证。
2. **W12**: 放弃「给 `\.env` 加右边界」的思路, 改为只对**单键读取形态** (`.environ.get(` / `.environ[`, 与基线已放行的 `os.getenv(` 同一信息量) 豁免, 整表导出 (`print(os.environ)` / `dict(os.environ)` / `.items()` / `.copy()` / `json.dumps(…os.environ…)` / `os.environb` / 遍历) 保持拦截; `.env2` / `.envprod` / `.envs/` / `.env_prod` 经解释器读取不得由拦变放 (与基线一致)。实现可用「匹配前把单键读取形态归一化」; 必须给出反向守卫与 issue 原形放行两面的 SC。
3. **W9**: (a) 扩展判定不得能中断内建判定 —— 内建判定先完成、扩展只能追加拦截, 扩展处理中的任何内部错误 ⇒ 忽略扩展、内建结果照常, 并用 SC 做故障注入验证; (b) 条目按固定字符串匹配, 不编译成正则 (消除转义类问题); (c) 成本有上界 (条目数上限 + 单遍匹配), 写明延迟预算并用 SC 钉住; (d) 文档落点: `standards/conventions/secret-hygiene.md`、aria README 的 Hooks 小节、`secret-guard.sh` 头注释, 均进同步面与 doc-sync SC; (e) 扩展失效是否经 systemMessage 让用户可见, 由执笔论证取舍。
4. **Impact 收尾口径**: 默认改为理解 B —— owner 裁定前, 不在 10CG/aria-plugin#203 与 10CG/Aria#221 下发任何评论 (决策单第 2 项字面); 10CG/aria-plugin#154 的关闭放在 post-ship 端到端复验之后。
5. **研究笔记**: 主控已把四份研究笔记纳入仓内 `.aria/notes/2026-09-30-wpa-phase-a/research/`, v2 的全部引用改指仓内路径。
6. **SC-32 (bash 3.2)**: 执笔先尝试取得真实 bash 3.2 运行环境 (例如在实验目录从源码构建); 取不到时, 扩充静态检查覆盖面并把「真 bash 3.2 运行腿」写成 Phase B 的执行条件, 不得把静态黑名单写成「可跑」。
7. **W11**: 包裹形态下的 env / printenv 整环境转储, 纳入或写成已知限制都可以, 但必须论证并用 SC 钉住所选一侧; `/proc/<pid>/status` 等只读元数据保持放行 (与基线一致)。
8. **W13**: 与 SOT 现有 argv `KEY=…` 示例对账 (改示例或精确限定新条款的适用面), 并让 SC-26 锚定到具体条款位置。
9. **同步面**: 按最近两次发版的同步提交实测列全 (主仓 16 个版本点 + aria 六文件), 并在 Tasks 里有承载行。
10. **SC 可证伪性**: 逐条处理簇 J; 坏实现须像真实坏情形; 新 tag 的语料级误报验收要可复跑 (固定 SHA 的文件清单、可复现的结果)。
11. **收敛口径提醒**: 第 2 轮起各席 finding 的 scope 只写一个节锚 (`proposal.md What.W<n>` / `proposal.md SC-<n>` / `proposal.md <节名>`), 以免同一问题因 scope 写法不同而产生不同的键。

### 流程记录

- 派单指纹: tl `b1de224318b76a41` / ba `9cd797465e9eb0ff` / qa `be2e29fd15412e8e` / cr `ae0f41695fcfa62e` / km `018314d80fdef4b5` (派单原文存于 `.aria/notes/2026-09-30-wpa-phase-a/dispatch/R1/`)。
- 五份席位报告为各席结构化输出 `report_markdown` 原样, 主控用脚本从运行记录取出落盘, 未作改动。
- 并发: 本机工作流并发上限 2, 与 audit-engine `max_parallel: 2` 一致。
- 工作区: 席位只在各自的 scratchpad 实验目录操作; 结束时主仓 HEAD `47aa15f`、aria `268da8f` 未变, 协调 ref 只有主控的心跳刷新。

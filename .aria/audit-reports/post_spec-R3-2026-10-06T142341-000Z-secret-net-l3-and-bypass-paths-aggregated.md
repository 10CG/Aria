---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: false
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-06T14:23:41.000Z
context: openspec/changes/secret-net-l3-and-bypass-paths/proposal.md
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
counts_raw: 0C/12M/23m
counts_dedup: 0C/10M/16m
sibling_probe: no_sibling_found
---

# post_spec R3 聚合 — secret-net-l3-and-bypass-paths — 未收敛

> 本节为机械聚合 (脚本从运行记录生成; 各席报告原文见同目录同轮次文件)。主控独立核验与处置意见见文末「主控记录」节。

## 判定

| 席 | verdict | counts (自报) | counts (按 findings 计) | vote | 报告文件 |
|---|---|---|---|---|---|
| tech-lead | PASS_WITH_WARNINGS | 0C/1M/2m | 0C/1M/2m | REVISE | `post_spec-R3-2026-10-06T142341-000Z-secret-net-l3-and-bypass-paths-tech-lead.md` |
| backend-architect | PASS_WITH_WARNINGS | 0C/5M/5m | 0C/5M/5m | REVISE | `post_spec-R3-2026-10-06T142341-000Z-secret-net-l3-and-bypass-paths-backend-architect.md` |
| qa-engineer | PASS_WITH_WARNINGS | 0C/4M/5m | 0C/4M/5m | REVISE | `post_spec-R3-2026-10-06T142341-000Z-secret-net-l3-and-bypass-paths-qa-engineer.md` |
| code-reviewer | PASS_WITH_WARNINGS | 0C/2M/8m | 0C/2M/8m | REVISE | `post_spec-R3-2026-10-06T142341-000Z-secret-net-l3-and-bypass-paths-code-reviewer.md` |
| knowledge-manager | PASS | 0C/0M/3m | 0C/0M/3m | PASS | `post_spec-R3-2026-10-06T142341-000Z-secret-net-l3-and-bypass-paths-knowledge-manager.md` |

## 全部 finding (按席位原编号, 不转述)

| 席 | 编号 | 键 (重算) | 席位所写 id | severity | type | category | scope | summary (席位原文) |
|---|---|---|---|---|---|---|---|---|
| tech-lead | M1 | `4f713847` | `4f713847` | major | issue | architecture | proposal.md What.W1 | L3 对 NUL 分隔内容结构性失明: 提取链经命令替换丢弃 NUL, KEY=value 记录粘连, 键形 tag 的左边界与行首锚都锚不上。进程环境的标准形态 (/proc/<pid>/environ 经 Read、env -0 经 Bash) 在基线与目标都两层皆盲 (L1 分别由 22au / 7.10 放行)。Spec 把 22au 只归因于两面名单不对齐, W1 的取舍与已知限制未提 NUL, 也未考虑在同一提取管道加一段 NUL→换行 (已验证: environ 形从静默变为 alert m=3, 套件 50/50, 探针 L3 全部行 154/154)。 |
| tech-lead | m1 | `cfb2fb14` | `cfb2fb14` | minor | issue | testing | proposal.md Tasks | Tasks 1.12 的执行条件要求 plugin-cache-currency.py「报 PASS」, 但探针在相等时只输出 `OK installed=… sot=…` (PASS 只是 docstring 状态名), 且 ##SKIP## 同样退出码 0; 照字面会永远停在 1.12, 按退出码读则会把 SKIP 当通过。 |
| tech-lead | m2 | `6ff1d962` | `6ff1d962` | minor | issue | documentation | proposal.md What.W11 | W11 同族扫描漏列几种打印完整 argv 的进程列举: 本地 systemd-cgls (基线 secret-guard.sh:850 已视 ssh 包裹形为暴露)、pidstat -l、w、宿主 busybox ps、AIX 格式 ps -o '%p %a'。基线与目标均放行, 但未进已知限制 / 22bh / 7.10。 |
| backend-architect | M1 | `8d258b19` | `8d258b19` | major | issue | testing | proposal.md What.W10 | W10 的变量展开是本 hook 第一处解析并改写命令文本的新代码, Spec 没有「不得执行命令文本」的不变量, 全部 L1 SC 行也无副作用 canary: 本席自构的 eval 式实现在 SC-16..25 / 29 / 31 / 32 全绿的同时在 hook 里真的执行了命令文本 (5 种 canary 载荷 4 种创建文件), 基线与原型都不执行。 |
| backend-architect | M2 | `8fbbee80` | `8fbbee80` | major | issue | testing | proposal.md What.W11 | W11 要求进程表族 credit 用 tight, 但 SC-22 只用 plain ps 三行 (22q-22s) 钉它: tight 判据收窄成行首 plain ps 的坏实现让 SC-16..25 / 31 全绿却放行 13 种 pgrep / pstree / top / docker / launcher / 远程包裹加行过滤的形态; 规则行与 tight 判据是两份必须同源的正则拷贝, 去掉一个 launcher 词只改一份相关 7 行零红; W8 的 app.ini tight 同形只有一行单路径。 |
| backend-architect | M3 | `0a8380fd` | `0a8380fd` | major | issue | implementation | proposal.md What.W9 | W9 扩展条目的读取器判定按「最近的 \| ; & 换行之后」切阶段, 不识别引号: python3 -c / node -e / awk 程序文本里含 ; & 或换行时读取器与条目被切开而放行 (内建 app.ini 行对同形命令是拦的), 而 Spec 声称解释器源组与 W8 作用面一致; 探针 19o / 19u 只用无分号的单语句形。 |
| backend-architect | M4 | `ac42f607` | `ac42f607` | major | issue | implementation | proposal.md What.W11 | (R2 K 簇残余) W11 重写的 /proc pid 位置枚举漏掉 $$ / $!、[0-9]* 一类 glob、brace 与 thread-self: cat /proc/$$/environ、cat /proc/[0-9]*/cmdline 基线与目标都放行 (对照 $PPID 与 * 被拦), 既无用例也未列已知限制。 |
| backend-architect | M5 | `1c49d896` | `1c49d896` | major | issue | testing | proposal.md SC-7 | 新分类器各步骤与白名单作用于哪些 tag 只钉了一部分: 路径形 / 点分链套到既有 json-secret-field、白名单套到既有 bearer / x-api-key / URL tag 的两个坏实现让全部 L3 行 (SC-1..13, 15) 与对照一致全绿, 却让基线检出的 SendGrid 形 key、点分口令、路径形口令与标记词开头的头 / URL 值变静默。 |
| backend-architect | m1 | `dcba7939` | `dcba7939` | minor | issue | implementation | proposal.md SC-22 | docker container top (docker top 的长写法) 基线与目标都放行, 既未纳入也未列入 22bh 已知限制; ps aux \| grep -c X 是新增误拦, 未在 W11 的新增误拦清单里。 |
| backend-architect | m2 | `6f503728` | `6f503728` | minor | issue | implementation | proposal.md What.W9 | 扩展条目的长度 4-200 与含字母或数字未说明按字节还是字符、字母类取哪个 locale: mawk 按字节计使 3 字符的 a配置 被接受, 纯中文 4 字符条目被静默跳过, 中文环境的敏感目录无法列入且无提示。 |
| backend-architect | m3 | `2f76563e` | `2f76563e` | minor | issue | testing | proposal.md Impact | 关闭关键字机械检查只监视 PIPESTATUS[1] (grep), 看不见 git log 失败 (实测 rc=1 而 git 为 128), 与其自称照 Aria#199 的 rc 判据不符, 应同时校验 PIPESTATUS[0]。 |
| backend-architect | m4 | `cfb2fb14` | `cfb2fb14` | minor | issue | testing | proposal.md Tasks | Tasks 1.10 要求 WPA_REQUIRE_ALL=1 下 20g 不得为 n/a, 但 20g 在 root 下按设计不可构造 (aria-runner 容器默认 root), 1.10 / 1.1 未写须以非 root 运行探针, 在 root 容器里验收会卡在 exit 3。 |
| backend-architect | m5 | `f410df76` | `f410df76` | minor | issue | documentation | proposal.md Impact | 10CG/aria-plugin#154 关单评论须披露的与评论 19339 字面参数的两处有意偏离不全: 评论写的是 [REDACTED 前缀值跳过, Spec 只放行括号闭合的 [REDACTED…] 且要求未闭合者仍检出, 是第三处偏离, 关单评论是不可撤回的外发动作。 |
| qa-engineer | M1 | `eb350937` | `eb350937` | major | issue | testing | baseline_probe.py | 枚举/边界逐成员出行在 v3 补到了新增集合,但既有被改写触及的成员与 W4/W9 的阈值、回退腿、格式规则仍无行:我造的 8 个自然坏实现 (删既有 json-secret-field 的 webhook_secret\|encryption_key 两键、删提取链 .tool_result.content/.output 两分支、W4 指纹阈值 <=16/<20/<13、去掉 shasum 或 sha256sum 回退腿、W9 条目不剥首尾空白) 在对应全部行上 0 行红。 |
| qa-engineer | M2 | `05982c10` | `05982c10` | major | issue | documentation | proposal.md Impact | 簇 P 的修复(关闭关键字机械检查,proposal.md:352)在 git log 失败或范围为空时真空通过:判据取 PIPESTATUS[1](grep 的 rc),起点写错/为空(..HEAD)/-C 路径错都得无输出且 rc=1=通过,与其自称照抄的 10CG/Aria#199 判据(PIPESTATUS[0],其 R5-M4 正为此而改)相反。 |
| qa-engineer | M3 | `28af0372` | `28af0372` | major | issue | testing | proposal.md SC-20 | SC-20 的扩展失败只丢扩展矩阵缺有效条目为零的文件(只含注释/空行/全被跳过):把空模式喂给 grep -F -f 的自然坏实现使每个 Read 与 Edit 都被拦(exit 2),与从不因扩展问题 exit 2 的不变量相反,而 SC-19/SC-20 的 37 行全绿。 |
| qa-engineer | M4 | `44b5bb44` | `44b5bb44` | major | issue | testing | proposal.md SC-32 | SC-32 32c 的 bash 3.2 差分只在 LC_ALL=C.UTF-8 一个 locale 里跑:同一个真 bash 3.2.57 在 en_US.UTF-8 下,原型熵下限的 glob 类 [[ $v == *[a-z]* ]] 把大写也算小写,目标原型 L3 行 9p/10a/10k 转红(bash 5.2 同 locale 与 3.2+C.UTF-8 全绿),差分看不见,W2 也未规定字符类须与 locale 无关。 |
| qa-engineer | m1 | `b298cc56` | `b298cc56` | minor | risk | testing | proposal.md SC-28 | 28c/28d 的判据只认两个旧措辞(~?\d+ (known bypass classes\|secret-shape patterns)),窄于 SC-28/W14 声称的不得写任何 pattern/类别总数字面:头注释写入 37 patterns, ~12 key-shape forms 后 SC-28 的 14 行全绿。 |
| qa-engineer | m2 | `6ff1d962` | `6ff1d962` | minor | issue | documentation | proposal.md What.W11 | W11 已知限制与 22bh 未列同族进程命令行列举 w、systemd-cgls、pidstat -l:基线与目标原型对它们均 exit 0(按手册语义列出带参数命令行,未实跑输出)。 |
| qa-engineer | m3 | `44510e65` | `44510e65` | minor | issue | documentation | proposal.md SC-12 | 12k 清单文字写 2 个头 tag,逐类相加为 37 而非共 38 个 tag(漏了 x-api-key-header;探针 W4 表实为 38 项)。 |
| qa-engineer | m4 | `cfb2fb14` | `cfb2fb14` | minor | issue | testing | proposal.md Tasks | Tasks 1.12 执行条件写 plugin-cache-currency.py 报 PASS,探针成功时实际输出 OK installed=… sot=… 且退出码 0,SKIP 的退出码也是 0:按字面找 PASS 永远找不到,按退出码判则把 SKIP 当通过。 |
| qa-engineer | m5 | `9ce750ed` | `9ce750ed` | minor | risk | testing | baseline_probe.py | WPA_REQUIRE_ALL=1 验收要求 20g 不得是 n/a,而 20g 在 root 下不可构造;aria-runner 容器无 USER 指令且 modes/initial.sh:309-311 写明按 root 运行,root 执行席位没有合法路径满足 Tasks 1.10。 |
| code-reviewer | M1 | `05982c10` | `05982c10` | major | issue | documentation | proposal.md Impact | Impact「提交页脚 / PR 描述的关键字」的机械检查只取 grep 的 rc (PIPESTATUS[1]), 不验上游 git log 是否跑成、范围是否非空: 起点无法解析 (git 退出 128) 或代换为空 (..HEAD) 时末行都是 rc=1, 按判据真空通过; 同节 #199 守卫防了同类真空, 本条声称照其 rc 判据却没继承 (R2 簇 P 残余) |
| code-reviewer | M2 | `eb350937` | `eb350937` | major | issue | testing | baseline_probe.py | W11「包裹下整环境转储」集合 (nomad alloc exec / pct exec / ssh × env / printenv) 未逐成员出行: ssh … env 只在 22aq 与 pct exec 复合出现; 本席构造的拆行坏实现去掉 ssh 后 SC-22 / SC-25 全绿 (target shape holds) 而 ssh host env 由拦变放; 另 W11 已知限制称 sh -c 'printenv' 仍放行, 既无行钉住, 原型又拦了它 (连同 bash -c env、watch env), Spec 与原型相反 (R2 簇 M 残余) |
| code-reviewer | m1 | `467c8b54` | `467c8b54` | minor | issue | implementation | proposal.md What.W11 | W11 的 /proc pid 位置闭集漏了 $$ (等同 self)、反引号替换、glob 字符类 [0-9]*、前缀 glob 1*、花括号 {1,2,3}: cat /proc/$$/environ 与 for f in /proc/[0-9]*/cmdline 在基线与原型都放行, 而 /proc/self/environ 被拦; 既未纳入也未进 22bh |
| code-reviewer | m2 | `6ff1d962` | `6ff1d962` | minor | issue | documentation | proposal.md What.W11 | W11 未约束远程 / 外壳包裹词锚在命令位置; 原型照基线体例不锚定, 含 ssh / watch (含 sshd、stopwatch 子串) 再接进程表形态的文本提及 (git commit -m、gh issue comment、grep 文档) 都被拦; 该误拦类未在 W11 新增误拦与 Impact 申报, 22Y 也无含包裹词的样例 |
| code-reviewer | m3 | `5d12116d` | `5d12116d` | minor | issue | documentation | proposal.md Tasks | Tasks 1.12 的执行条件要求 plugin-cache-currency.py「报 PASS」, 但该探针成功时打印 OK …(exit 0), 从不打印 PASS, 跳过打印 ##SKIP##, 版本串坏打印 MALFORMED; 字面执行时成功态落进「其它任何结果」而停下, 1.12 / 1.13 无合法下一步 |
| code-reviewer | m4 | `5e342bfd` | `5e342bfd` | minor | issue | documentation | proposal.md What.W14 | W14 新写「目标态 K = 50, SOT 同步为 50」, 与未改的 Tasks 1.2「按 SC 把探针用例落为两个套件的用例」矛盾 (L3 用例落入后 K 必然 > 50); 50 来自只加了自检的原型 (29a PASS 50/50), 可能诱使实现者不把 L3 用例落进套件 |
| code-reviewer | m5 | `f410df76` | `f410df76` | minor | issue | documentation | proposal.md Impact | #154 关单评论只计划披露与评论 19339 的两处偏离 (16 vs 8、fp 门槛), 漏了第三处: 19339 要求 [REDACTED 前缀值跳过, W3 只放行闭合的 [REDACTED…], 不闭合的值仍检出 (7j) |
| code-reviewer | m6 | `26e1a7a9` | `26e1a7a9` | minor | issue | documentation | proposal.md What.W7 | W7 已知限制称 no-plan-fallback.md 这类文件 W1 后被 Read 时告警「与今天 cat 时一致, 不是新增面」, 实测今天 cat (基线 Bash) 静默, 原型 Bash 与 Read 都报 kv-secret-assign=1, 告警来自 W2 新 tag |
| code-reviewer | m7 | `4447c607` | `4447c607` | minor | issue | testing | proposal.md What.W14 | W14 (f0) 把 Bash 面无扩展档委托给测试内 SC-8, 但 SC-8 只抽取并计时 _sg_per_segment_eval (secret-guard.test.sh:1773-1775, :1852), 而 W9 未规定扩展调用必须在其内, 放在 :1111 子 shell 之后的实现不被任何时档覆盖; 另 timing.py 的 (g) 默认参数是满额档, 与 W14 定义的 (g) 不同 |
| code-reviewer | m8 | `15da802b` | `15da802b` | minor | issue | documentation | proposal.md What.W8 | What 里的旧计数未随 v3 同步: W8 现状仍写 SC-16 0/13、SC-18 0/4 (v3 为 0/15、0/6, Why 表已改); W11 现状写 SC-6 基线 0/8 (v3 为 ×11); 12k 枚举合计 37 与「共 38 个 tag」不符 (头 tag 实为 3 个) |
| knowledge-manager | m1 | `a6304dd1` | `a6304dd1` | minor | issue | testing | proposal.md SC-28 | SC-28 对「替换文本在场」按单个子串判定, 放过半截改写与新造悬空锚点 (R1 a6304dd1 的残余): 28l 只以 version-dependent behaviour 为旧文本, 保留 Claude Code exposes no field to replace tool_response 也绿; 28b 只验头注释含 secret-hygiene.md, 保留不存在的 §1.3 也绿; 执笔原型两处都这样落地而 doc-sync 23/23 yes。 |
| knowledge-manager | m2 | `cfb2fb14` | `cfb2fb14` | minor | issue | testing | proposal.md Tasks | Tasks 1.12 执行条件写「plugin-cache-currency.py 报 PASS」并把 STALE / SKIP / FAIL / AHEAD 并列, 但脚本通过时首行是 OK installed=… sot=… (exit 0), PASS 是 state-scanner 运行器的状态词, 且 ##SKIP## 也是 exit 0: 照字面判 PASS 永远对不上, 只看 exit code 则会把 SKIP 当通过。 |
| knowledge-manager | m3 | `4447c607` | `4447c607` | minor | issue | testing | proposal.md What.W14 | W14 写死「secret-scan 目标态 K = 50 (49 + 自检本身), SOT 同步为 50」, 与 W1「新测试一律用真实信封」、Tasks 1.2「按 SC 把探针用例落为两个套件的用例」、SC-29「总数 >=49」及 27b / 27c 以实跑总数为准相矛盾; 50 只是原型 (未落 L3 用例) 的产物, 应改为「同步为实跑总数」。 |

## 收敛计算 (本仓先例口径: 相邻两轮 Critical+Major 键集相等 且 全票 PASS)

- 主控定稿键映射 (同一问题不同四元组, 比较前先映射): `51e90cab` → `eb350937`; `5ce95ecf` → `eb350937`; `5fd1f356` → `ce6fc59c`; `e7e041c6` → `eb350937`; `fc97f926` → `e8d39a8a`
- 本轮 Critical+Major 键集 (10): `05982c10`, `0a8380fd`, `1c49d896`, `28af0372`, `44b5bb44`, `4f713847`, `8d258b19`, `8fbbee80`, `ac42f607`, `eb350937`
- 上一轮 Critical+Major 键集 (7): `05982c10`, `60f3173a`, `6bd285b1`, `ac42f607`, `ce6fc59c`, `e8d39a8a`, `eb350937`
- conclusions_stable = False
- unanimous_pass = False (1 PASS / 4 REVISE)
- converged = False

## 机械核对

- 席位数 5 / 5; incomplete = False
- frontmatter 开头: tech-lead=ok, backend-architect=ok, qa-engineer=ok, code-reviewer=ok, knowledge-manager=ok
- 自报 counts 与 findings 计数不一致的席: 无
- finding id 与四元组重算不一致: 0 条
- 竞品 Spec 探针 (本轮入口): status=ok / verdict=no_sibling_found

## 主控记录

> 2026-10-06 主控追加。只在这里写主控的核验与裁定; 上面各节是脚本生成的机械聚合, 未改动。

### 簇归并 (本轮键已与 R2 定稿键对齐的直接沿用)

| 簇 | 问题 | 席位编号 (键) | 性质 |
|---|---|---|---|
| Q | L3 对 NUL 分隔内容结构性失明: 提取链经命令替换丢 NUL, `KEY=value` 记录粘连, 键形 tag 锚不上; `/proc/<pid>/environ` 经 Read、`env -0` 经 Bash 两层皆盲 | tl/M1 `4f713847` | 既有盲区, 本轮新发现 |
| M | 覆盖面: 既有被改写触及的成员与 W4 / W9 的阈值、回退腿、格式规则无行 (qa/M1); 包裹下整环境转储未逐成员出行 (cr/M2); 分类器各步骤与白名单作用于哪些 tag 只钉了一部分 (ba/M5); 进程表族 tight credit 只用 plain ps 三行钉住 (ba/M2) | qa/M1 · cr/M2 `eb350937` · ba/M5 `1c49d896` · ba/M2 `8fbbee80` | R2 簇 M 残余 + 新增覆盖缺口 |
| P | 关闭关键字的机械检查只看 grep 的退出码, git log 失败或范围为空时真空通过 | qa/M2 · cr/M1 `05982c10` (+ ba/m3) | R2 簇 P 残余 (v3 引入) |
| R | SC-20 缺「有效条目为零」的扩展文件: 空模式喂给 `grep -F -f` 会让每个 Read / Edit 都被拦 | qa/M3 `28af0372` | v3 引入 |
| E | bash 3.2 差分只在一个 locale 里跑; glob 字符类在别的 locale 下把大写算小写 | qa/M4 `44b5bb44` | R1 簇 E 延伸 |
| S | W10 是本 hook 第一处解析并改写命令文本的代码, Spec 没有「不得执行命令文本」的不变量, L1 SC 无副作用诱饵: eval 式实现在全部 L1 行全绿的同时真的执行了命令文本 | ba/M1 `8d258b19` | 既有设计缺口, 本轮新发现 |
| T | W9 扩展条目的读取器判定按 `| ; & 换行` 切阶段且不识别引号, 内联解释器程序文本里的 `;` `&` 换行把读取器与条目切开而放行 (内建 app.ini 行对同形命令是拦的) | ba/M3 `0a8380fd` | v2/v3 设计 |
| K | W11 `/proc` pid 位置枚举漏 `$$` / `$!`、`[0-9]*` 一类 glob、花括号与 `thread-self` | ba/M4 `ac42f607` | R2 簇 K 残余 |

### 趋势与判断

- Critical: R1 6 → R2 1 → R3 0。Major (去重): R1 24 → R2 11 → R3 10, 计数持平。
- 本轮十键里约一半由 v3 返修引入或是其残余 (P、R、E、M 的一部分、T), 另一半是既有设计中更深的缺口 (Q、S) 与覆盖面。缺陷集中在 L1 的三个新机制 (W9 扩展入口、W10 变量展开、W11 进程表) 与测试覆盖面; L3 侧只剩 Q 与覆盖面。
- 按本仓收敛口径 (相邻两轮 C+M 键集相等且全票 PASS ⇒ 实际是连续两轮零 C/M) 与 `max_rounds` 5: 只有 R4、R5 两轮都零 C/M 才能在第 5 轮收敛。v4 是还能达成这一点的最后一次完整返修; R4 与 R5 之间若还要返修, 只能是 minor。
- 若第 5 轮仍未收敛, 按 audit-engine 降级策略由 owner 三选一 (接受当前结论 / 加轮 / 降级为单轮); owner 2026-08-16 决策单 (`docs/decisions/DEC-20260816-002-fix-first-outcome-oriented.md` §3.1) 列过的另两种处置 (换执笔人 / 缩小被审对象) 届时一并呈上, 主控不自行降级、不自行缩小范围。

### 主控裁定 (v4 返修据此执行; 均为技术级, 列入 handoff 请 owner 复议)

1. **簇 S (W10)**: Spec 写明不变量「hook 绝不执行、求值或 source 命令文本的任何部分 (变量展开只做纯文本替换)」, 并补副作用诱饵类 SC 行, 使任何 eval 式实现必然转红。
2. **簇 T (W9)**: 扩展条目与读取器的共现判定不得因引号内的 `;` `&` `|` 换行而切断; 与内建 app.ini 行对同形命令的判定一致 (行为对齐用 SC 钉住)。
3. **簇 R**: 「扩展失败只丢扩展、从不因扩展 exit 2」的不变量覆盖有效条目为零的文件, 补行。
4. **簇 E**: 新写代码里的字符类必须与 locale 无关 (写明做法), bash 3.2 差分至少在两种 locale 下跑 (本机缺的 locale 如何构造写清; 构造不了就写成执行条件, 不得省略)。
5. **簇 P**: 机械检查同时校验上游 `git log` 成功且范围非空, 判据与 10CG/Aria#199 那条逐项对齐 (引原文 file:line)。
6. **簇 Q (W1)**: 提取链对 NUL 分隔内容的处理 —— 纳入 (例如提取后把 NUL 换成换行, 复核不会破坏既有行) 或列为已知限制, 二选一并论证; 选哪一侧都要有决定性的 SC 行 (Read 读进程环境形 / Bash `env -0`)。
7. **簇 K (W11)**: `/proc` pid 位置把 `$$` / `$!` / glob / 花括号 / `thread-self` 纳入或逐一列为已知限制, 每一项有决定性的行。
8. **簇 M**: 每条规则、白名单分支、分类器步骤**作用于哪些 tag** 都要被行钉住 (套到不该套的 tag 会转红); tight credit 在进程表族的全部形态上各有行; 被改写触及的既有成员与阈值、回退腿、格式规则各有边界行。
9. **全部 minor** 照返修模板逐条处置。
10. **方针**: v4 的最高优先级是**不引入新的 major**。改动越小越好, 不新增机制; 每改一处都跑对应的缺项类或越界类坏实现。若某条修复只能靠新增机制, 优先改为收窄语义或列为已知限制并论证 (技术级, 写入「待 owner 复议」), 不得为了少改而降低既有检出。

### 流程记录

- 派单指纹: tl `550e98e5c44cfff3` / ba `2f12131f0c16677c` / qa `10540aa5520e6409` / cr `6ac5b977433d163d` / km `7e3cd138f501186c` (原文存于 `.aria/notes/2026-09-30-wpa-phase-a/dispatch/R3/`)。
- 并发: 两组, 同时在跑最多 3 席。报告为各席结构化输出原样, 由脚本从两份运行记录取出落盘。
- 工作区: 主仓 HEAD `c0a6654`、aria `268da8f` 全程未变。

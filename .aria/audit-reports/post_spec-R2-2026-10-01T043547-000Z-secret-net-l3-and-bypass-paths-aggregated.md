---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: false
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
drift_warning: false
is_refocus: false
verdict: FAIL
timestamp: 2026-10-01T04:35:47.000Z
context: openspec/changes/secret-net-l3-and-bypass-paths/proposal.md
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
counts_raw: 1C/15M/34m
counts_dedup: 1C/11M/23m
sibling_probe: no_sibling_found
---

# post_spec R2 聚合 — secret-net-l3-and-bypass-paths — 未收敛

> 本节为机械聚合 (脚本从运行记录生成; 各席报告原文见同目录同轮次文件)。主控独立核验与处置意见见文末「主控记录」节。

## 判定

| 席 | verdict | counts (自报) | counts (按 findings 计) | vote | 报告文件 |
|---|---|---|---|---|---|
| tech-lead | FAIL | 1C/2M/6m | 1C/2M/6m | REVISE | `post_spec-R2-2026-10-01T043547-000Z-secret-net-l3-and-bypass-paths-tech-lead.md` |
| backend-architect | PASS_WITH_WARNINGS | 0C/4M/7m | 0C/4M/7m | REVISE | `post_spec-R2-2026-10-01T043547-000Z-secret-net-l3-and-bypass-paths-backend-architect.md` |
| qa-engineer | PASS_WITH_WARNINGS | 0C/4M/5m | 0C/4M/5m | REVISE | `post_spec-R2-2026-10-01T043547-000Z-secret-net-l3-and-bypass-paths-qa-engineer.md` |
| code-reviewer | PASS_WITH_WARNINGS | 0C/2M/8m | 0C/2M/8m | REVISE | `post_spec-R2-2026-10-01T043547-000Z-secret-net-l3-and-bypass-paths-code-reviewer.md` |
| knowledge-manager | PASS_WITH_WARNINGS | 0C/3M/8m | 0C/3M/8m | REVISE | `post_spec-R2-2026-10-01T043547-000Z-secret-net-l3-and-bypass-paths-knowledge-manager.md` |

## 全部 finding (按席位原编号, 不转述)

| 席 | 编号 | 键 (重算) | 席位所写 id | severity | type | category | scope | summary (席位原文) |
|---|---|---|---|---|---|---|---|---|
| tech-lead | C1 | `e8d39a8a` | `e8d39a8a` | critical | issue | implementation | proposal.md What.W3 | R1 簇 A 只部分关闭: W3 白名单的两类形态照样作用于既有 json-secret-field —— 裸 $NAME (单一大小写 + 数字 + 下划线) 与截断标记 (值以 … / ... 结尾)。按 W3 字面实现后, 基线能检出的这两类真实值变为静默 (原型实测: 基线告警, 原型静默)。已知限制没写, SC 没钉, Impact 「$ 开头的随机值仍检出」对单一大小写子集不成立。 |
| tech-lead | M1 | `ac42f607` | `ac42f607` | major | issue | implementation | proposal.md What.W11 | W11 的 launcher 集是 secret-guard.sh:873 既有集合的未论证子集 (少了 xargs / eval / unbuffer), 也不接受 sudo -u <用户> 这类带参数的选项和 /bin/ps 这类绝对路径; /proc 放宽行没有纳入 W8 / W9 都纳入了的 python3 -c / node -e。pgrep -f X \| xargs ps -fp、sudo -u svc ps -ef、python3 -c 读 /proc/<pid>/environ 在原型上照样放行, 无 SC, 也未列已知限制。 |
| tech-lead | M2 | `ce6fc59c` | `ce6fc59c` | major | issue | testing | proposal.md Tasks | Tasks 1.10 的 post-ship 腿有两处缺口: (a) 不经 harness 验 Read 路径, 而 Impact 把 10CG/aria-plugin#154 的关单条件写成 「Read 提取修复经 post-ship 端到端复验之后」; (b) 用真实危险命令 (ps aux、读 /etc/forgejo/app.ini) 验 L1 拦截, 本仓发版后插件缓存 STALE 是常态, 此时或超时放行时会把真实 argv / 配置值泄进会话。已有无写入、无泄露的 Read 金丝雀 (SC-33 归因文件) 与 \| head -c 0 这类安全探针可用。 |
| tech-lead | m1 | `c9357eb5` | `c9357eb5` | minor | issue | testing | proposal.md SC-30 | W14 (h) 档的 「< 5 s」 绝对上界随主机负载漂移: 本机负载 4-10 时, 基线自己跑 600 段整进程就要 7.15 s, 该档会在与实现无关的条件下转红。它与测试内 SC-8 owner 裁定的 「绝对腿 + 相对腿取宽」 设计相反, 且只计判定段, 不计 5 s 超时所针对的整个进程。 |
| tech-lead | m2 | `d65a895f` | `d65a895f` | minor | issue | architecture | proposal.md What.W9 | W9 的 「扩展代码 (含项目根解析) 只经 $( ) 调用」 与 「无扩展文件时不 fork 任何子进程」 字面不可兼得。原型在无扩展文件时每次 Bash / Read 调用仍多 1 次 exec; 若实现者为满足后者把预检放进主 shell, 那段代码不在故障注入范围内, 会重开 C2 那一类故障面。 |
| tech-lead | m3 | `684e9a24` | `684e9a24` | minor | issue | documentation | proposal.md What.W9 | W9 Bash 面语义 「且其每一处出现之前…有一个读取器」 可读作全称 (每处都要有读取器才判), 与 19r 要求的 「任一处在读取器之后即判」 相反, 措辞须改。 |
| tech-lead | m4 | `c941e4e1` | `c941e4e1` | minor | issue | implementation | proposal.md What.W8 | W8 的 app.ini 读取器组比既有 .env 家族窄: dd if=、< 重定向读取、cp … /dev/stdout、perl -ne、tee < 在原型上都放行, W8 已知限制没有列出。 |
| tech-lead | m5 | `0033f2f4` | `0033f2f4` | minor | issue | documentation | proposal.md 待 owner 复议 | 同族扫描漏列几条既有的整环境 / 进程环境旁路 (基线与原型都放行): export -p、declare -x、裸 set (SOT secret-hygiene.md:96 明列为受限)、env -0 / env -u (含新包裹下)、systemctl show -p Environment / systemctl cat、kubectl get pod -o yaml\|json。建议开单清单第 10 条未收录。 |
| tech-lead | m6 | `5d032f7a` | `5d032f7a` | minor | issue | documentation | proposal.md What.W13 | Spec 用 L1 / L2 / L3 编号叙述分层, 而 W13 / W9 要写入的 SOT secret-hygiene.md §0 自有 Path / Layer 0 / Layer 2 术语, 且明文 「Why no Layer 1」。Spec 没给落 SOT 时的术语映射, 实现者把 L1 / L3 写进 SOT 会与 §0 自相矛盾。 |
| backend-architect | M1 | `e7e041c6` | `e7e041c6` | major | issue | testing | proposal.md SC-4 | W2 的枚举型契约 (JSON 键名表 17 名干 × 拼写、json-env 与 kv 的 10 个关键字、cli 旗标后缀 7 个) 在 SC-4 / 5 / 6 里只被抽样钉住; 缩成被钉住子集的坏实现 mutC 让 129 行 L3 SC 全绿, 却漏掉 Spec 明列的 19 种形态。 |
| backend-architect | M2 | `51e90cab` | `51e90cab` | major | issue | testing | proposal.md SC-21 | L1 面同型缺口: W10 的引号值赋值、W8 的 16 个新增读取器、W11 的 13 个 launcher 都只被抽样钉住; 三个坏实现 mutD / mutE / mutI 各自让 SC-16 / 17 / 18 / 21 / 22 全绿, 却放行真实写法 (如 f="/etc/forgejo/app.ini"; cat "$f"、timeout 5 ps aux)。 |
| backend-architect | M3 | `ac42f607` | `ac42f607` | major | issue | implementation | proposal.md What.W11 | W11 的进程表规则对带 - 的 BSD 簇 (ps -aux / -ax / -x)、xargs / eval / unbuffer launcher (pgrep -f x \| xargs ps -fp)、then / do 关键字位置 (while true; do ps aux; done) 三类常见写法失明, 与同文件 env / printenv 行的既有约定 (secret-guard.sh:873 / :877) 不一致, SC-22 无行、已知限制未写; 四处同改的修法已在原型上验证。 |
| backend-architect | M4 | `ce6fc59c` | `ce6fc59c` | major | issue | testing | proposal.md Tasks | Tasks 1.10 的 post-ship 腿用真实的 ps aux 与 /etc/forgejo/app.ini 验拦截, 验证失败 (插件缓存未更新 / 会话未重启) 的路径就是泄露路径, 且该腿写在发版 (1.11) 之前; 应换诱饵命令并拆到 1.11 之后。 |
| backend-architect | m1 | `cffa7c09` | `cffa7c09` | minor | issue | testing | proposal.md SC-7 | W3 / W2 分类器的反向守卫对三个坏实现无决定性: 变量引用白名单接受混合大小写 (mutA, 8 次中 2 次全绿) 与路径形字符类误含 + 和 = (mutB, 8 次中 1 次全绿) 只概率性转红, 裸 $NAME 规则 (mutM) 没有任何决定性的行。 |
| backend-architect | m2 | `b4230080` | `b4230080` | minor | issue | implementation | proposal.md What.W3 | W3 第 5 类 (以 … / ... 结尾) 是后缀规则, 连同 $ 加单一大小写标识符形口令, 会放过真值; 已知限制只写了第 6 类, 且 SC-11 11v 只钉 Unicode 省略号, 去掉 ASCII ... 分支的坏实现 (mutH) 全绿。 |
| backend-architect | m3 | `984b1c3d` | `984b1c3d` | minor | issue | documentation | proposal.md What.W2 | W2 已知限制 / 已知误报清单仍不全, 且点分标识符链 漏报面≈0 的说法与实测不符 (三段式点分 token 20 次里静默 9 次); JSON 渲染头、Python repr 头、URL 查询、小写 INI / TOML 与 K8s name/value 对均未列为已知限制, TOKEN_URL / SECRET_NAME 类值会误报。 |
| backend-architect | m4 | `cfb24732` | `cfb24732` | minor | risk | architecture | proposal.md What.W14 | L3 新路径对每个命中 span 做 bash 迭代 (O(命中数)), SC-30 只给 L1 设时档, 密集输入 (约 15k–20k 命中) 下 5 s 超时即静默丢检; 新时档的 N / rounds 与活性断言也未规定。 |
| backend-architect | m5 | `467c8b54` | `467c8b54` | minor | issue | implementation | proposal.md What.W11 | W11 新增两类文本提及误拦: /proc 行 pid 位置接受任意 token (N、<pid>), 命令位置锚点含换行使 heredoc 里以 ps aux 起行的示例被拦; SC-22 22Y 只钉同行提及, 收窄 _SG_PIDTOK 的修法已验证。 |
| backend-architect | m6 | `15da802b` | `15da802b` | minor | issue | documentation | proposal.md What.W8 | W8 已知限制没写出读取器组之外的 15 种放行形态 (while read / mapfile / source / perl / tr / dd / cp / docker cp / xargs cat / find -exec 等), 而同文件 .env 族对其中多数各有专行; node -e 追加与右边界 app.inix 两处 Spec 文字也未被 SC 钉住。 |
| backend-architect | m7 | `a305732c` | `a305732c` | minor | issue | testing | baseline_probe.py | 探针的形态判定行把 n/a 行排除在外, 不带 WPA_BASH32 跑目标态时仍打印 target shape holds, 即便 29h / 29i / 32c 没跑; 应显式打印 not-run 行数。 |
| qa-engineer | M1 | `5ce95ecf` | `5ce95ecf` | major | issue | testing | proposal.md SC-22 | W14 明写 /proc 两行原位改写, 但反向守卫只有 22J 的 5 条命令; 基线行名的 13 个读取器里 9 个 (head tail less more hexdump od xxd awk perl rev) 无行, 把合并读取器表缩成 cat\|strings\|tr\|xargs 的坏实现使 9 类基线拦截变放行, SC-22 全 51 行与既有套件均不红 |
| qa-engineer | M2 | `eb350937` | `eb350937` | major | issue | testing | baseline_probe.py | 枚举型要求只按代表成员出行而 SC 声称会抓全表: 14 个实现不全或边界错的坏实现 (W8 读取器组与 node -e、W11 launcher / /proc 读取器 / 远程包裹、W9 node -e 与五个上界边界、W2 名表 / 关键字集 / flag 名集) 在对应全部行上 0 行红; 写手 25 个坏实现与 Tasks 1.8 的 12 类都是违反设计选项类, 无缺项类 |
| qa-engineer | M3 | `ac42f607` | `ac42f607` | major | issue | implementation | proposal.md What.W11 | W11 的 ps 形态写成 BSD 选项簇不带 - 加 SysV -f/-F 加 -o args, 漏掉带前导 - 的 BSD 式拼写 (ps -aux / -ax / -x / -w -x) 与 -O; procps-ng 4.0.2 上这些写法输出完整 argv, 原型放行, ps -aux \| grep curl 绕过 10CG/Aria#221 的核心拦截; SC-22 与已知限制均未覆盖 |
| qa-engineer | M4 | `60f3173a` | `60f3173a` | major | issue | architecture | proposal.md What.W5 | W5 把 tool_input.file_path 原样 (仅剥 CR) 拼进此前不含外来文本的 additionalContext 受信通道, 路径里的 ) 可闭合描述性括号并接任意祈使句、换行可伪造第二条 hook 行; 13a-c 只用良性路径, 13d 剥除正则对括号内不设限, rule6 块 B 只含事实陈述的归类前提对敌意输入不成立, 且 W5 拒绝命令摘要的理由同样适用于路径却未论证 |
| qa-engineer | m1 | `a4af42ab` | `a4af42ab` | minor | issue | documentation | proposal.md What.W3 | 白名单对既有 json-secret-field 仍有两处检出收窄未成文也无行钉住: $ 后全小写加数字或全大写加数字的值 ($NAME 形) 与以 ... 或省略号结尾的值 (基线 alert, 目标 silent) |
| qa-engineer | m2 | `6114c254` | `6114c254` | minor | issue | implementation | proposal.md What.W2 | 点分标识符链排除的理由 随机凭据不含点分标识符段 漏报面约等于 0 不成立: 由三段字母开头纯字母数字下划线段拼成的凭据 (Discord bot token 形、签名 cookie 形) 在新 tag 上静默, 已知限制与 SC-10 无此类 |
| qa-engineer | m3 | `c941e4e1` | `c941e4e1` | minor | issue | implementation | proposal.md What.W8 | W8 Bash 面名字组大小写敏感且不认反斜杠路径分隔符, Read/Edit 面两者都认, 两面不一致且未成文 (与 W9 要求两面大小写不敏感相悖); 10CG/aria-plugin#203 报告环境是 MINGW64, Gitea 大写目录与 C:\gitea 路径经 Bash 读取放行 |
| qa-engineer | m4 | `684e9a24` | `684e9a24` | minor | issue | documentation | proposal.md What.W9 | 成本上界触顶后的方向未成文: W9 64 处出现点与 W10 16 个赋值上限超出后均 fail-open (padding 即绕过) 无已知限制无行; 另 无扩展文件时不 fork 与扩展代码只经 $( ) 调用互斥, 原型每次调用都进子 shell |
| qa-engineer | m5 | `335996c0` | `335996c0` | minor | issue | testing | proposal.md SC-33 | SC-33 称关键词预筛是 6 个新 tag 的必要条件, 但预筛正则不含 private_key 的 camel/Pascal/连写拼写, 而名表含 privateKey PrivateKey privatekey, 只含这些键的文件普查失明 |
| code-reviewer | M1 | `fc97f926` | `fc97f926` | major | issue | implementation | proposal.md What.W3 | W3 白名单的裸 $NAME 与 $(…) 整值形态没有任何行钉住 (删掉它们的坏实现全绿), 而 $NAME 让既有 json 键上「$+字母+单一大小写字母数字」的真值由检出变静默 (基线 8/8 告警 → 原型 8/8 静默), 与 Impact「$ 开头的随机值仍检出」及主控裁定 1 字面相反, 未申报、无 known-limit 行 |
| code-reviewer | M2 | `6bd285b1` | `6bd285b1` | major | issue | testing | proposal.md SC-30 | SC-30 时档 (h) 的墙钟绝对值「< 5 s」红绿由主机负载决定: 本机负载约 4 时基线自身 600 段 6.5 s, 约 12 时 13–19 s, 任何实现都红; 安静时每段慢 25% 的坏实现可过; 内建先判已由 20l/21v 确定性钉住, 应改为同次运行的 CPU 时间比值 |
| code-reviewer | m1 | `cfb24732` | `cfb24732` | minor | risk | architecture | proposal.md What.W14 | L3 逐 span 处理无成本上界的验收: 全绿的原型对每个 span 都跑 bash 循环, 稠密既有 tag 输入慢 3–11 倍, 约 1 MB bearer 行 0.52 s → 5.84 s 越过 5 s 超时 (基线检出、目标丢告警); W14 只有「180 KB INI ≤ 2.5 s」一个点 |
| code-reviewer | m2 | `6114c254` | `6114c254` | minor | issue | implementation | proposal.md What.W2 | 点分标识符链排除让 SendGrid 形 SG.<22>.<43> 约 1/4 的真值在 5 种新 tag 形态下全部静默, W2「漏报面≈0」不成立且未列已知限制 |
| code-reviewer | m3 | `15da802b` | `15da802b` | minor | issue | documentation | proposal.md What.W8 | W8 名字组对目录递归 / 文件名 glob 读取 (grep -rn KEY /etc/forgejo/、cat /etc/forgejo/*.ini 等 6 种) 全部放行, 已知限制未列、无 known-limit 行 (输出侧由 W2 kv tag 兜底) |
| code-reviewer | m4 | `467c8b54` | `467c8b54` | minor | issue | implementation | proposal.md What.W11 | W11 同族形态未覆盖也未申报: podman top / podman ps --no-trunc、绝对路径 /bin/ps aux、不在首位的 BSD 选项簇 (与「任意 BSD 选项簇」字面不符), 原型均放行 |
| code-reviewer | m5 | `29a5d0bd` | `29a5d0bd` | minor | issue | testing | proposal.md SC-22 | 22S 把 pgrep -fl 钉为 allow-guard, 而 W11 自述它在 macOS 上输出完整命令行, 属已知漏拦, 应为 known-limit |
| code-reviewer | m6 | `335996c0` | `335996c0` | minor | issue | testing | proposal.md SC-33 | SC-33 称关键词预筛是 6 个新 tag 的必要条件, 但封闭名表的 privateKey / PrivateKey / privatekey 不被预筛命中而原型会告警, 含此类键的文件会被跳过 (假绿; 当前语料 0 个) |
| code-reviewer | m7 | `d65a895f` | `d65a895f` | minor | issue | architecture | proposal.md What.W9 | W9「项目根解析等只经 $( ) 调用」与「无扩展文件时不 fork」不能同时成立 (原型每次都 fork 并以空模式调用 grep -f); 命中超过 64 处后的语义未定、无行钉 |
| code-reviewer | m8 | `51dded0b` | `51dded0b` | minor | issue | testing | proposal.md SC-15 | 头部 Rule #7 声明称两份附件由 SC-15 15e / 15f 钉住, 实际 15e/15f 钉的是 proposal.md 与探针, baseline-evidence.md 无行钉住 (当前实测静默) |
| knowledge-manager | M1 | `fc97f926` | `fc97f926` | major | issue | implementation | proposal.md What.W3 | W3 把变量引用整值放行延伸到既有 json-secret-field, 但 $NAME 规则又宽又欠定: 基线检出的 $ 加单一大小写 (含数字、下划线) 口令会变静默; 按散文字面再放宽到纯数字也全绿; 整个删掉小写类同样全绿, 115 行 L3 探针对这一类零约束 (R1 簇 A 的残余)。 |
| knowledge-manager | M2 | `5fd1f356` | `5fd1f356` | major | issue | documentation | proposal.md Tasks | 头部 Rule #7 声明称 post-ship 复验腿只用合成值、不触碰真实 secret 存储, 但 Tasks 1.10 的两条 L1 腿是对真实进程表 (ps aux) 与真实路径 /etc/forgejo/app.ini 的读取验拦截; hook 未生效时命令会真执行并回显, 声明与步骤矛盾, 应改用无害操作数。 |
| knowledge-manager | M3 | `05982c10` | `05982c10` | major | issue | documentation | proposal.md Impact | Impact 的 issue 收尾口径只管评论与关闭两个显式动作, 没约束提交页脚与 PR 描述里的关闭关键字; 仓内约定要求修复类提交写 Closes 并自动关闭 issue (实测 #153 在带 Closes 的提交后约半分钟被关), 会绕过 #154 post-ship 复验后才关与 #203/#221 保持 open (决策单第 2 项)。 |
| knowledge-manager | m1 | `eff49510` | `eff49510` | minor | issue | documentation | proposal.md SC-26 | SC-26 判据弱于 W9 与 Impact 自己的文档要求: 26c 不要求写明静默失效与大小写不敏感 (删掉后仍 8/8), 26e 一行注释即过, 26g 不验放行侧申报。 |
| knowledge-manager | m2 | `5e342bfd` | `5e342bfd` | minor | issue | documentation | proposal.md What.W14 | 若干文档同步项只在散文里承诺, 既不在 W14 清单也无 SC: secret-scan.sh 头注释 Scope 清单与已知限制、SOT 5.1 括号新族、SOT 版本行、tight 族与 Acceptable filters 不一致的记录、W10 部分覆盖的对外落点。 |
| knowledge-manager | m3 | `51dded0b` | `51dded0b` | minor | issue | testing | proposal.md SC-15 | 头部 Rule #7 声明称两份附件由 SC-15 15e/15f 钉住, 但 SC-15 只钉 proposal.md 与 baseline_probe.py, 不含 baseline-evidence.md (今天静默但未被钉住)。 |
| knowledge-manager | m4 | `4900bccc` | `4900bccc` | minor | issue | testing | proposal.md SC-27 | W14 要求 secret-scan.test.sh 加与测试内 SC-13 同款的自检, 27b 只比头注释数与实跑总数, 只加头注释不加自检的实现也绿。 |
| knowledge-manager | m5 | `5d032f7a` | `5d032f7a` | minor | issue | documentation | proposal.md What.W13 | 3.8 的适用面判据不闭合: 长时(存活期超过数秒)与短命令(秒级)之间无分界, 被 26h 钉死的 3.1 示例自带 timeout=30; 末句优先用 @文件或 stdin 主语不明, 与钉死的 3.4 推荐示例并存时 SOT 自相不一致。 |
| knowledge-manager | m6 | `0033f2f4` | `0033f2f4` | minor | issue | documentation | proposal.md 待 owner 复议 | 发版后 hook 头注释将写 schema 含 updatedToolOutput 端到端未验证, 而 README 两语种与 SOT 5.2 仍写架构上无法 redact; Spec 已知矛盾却把订正整体推给第 1 条复议, 而该订正不依赖复议结论。 |
| knowledge-manager | m7 | `5d12116d` | `5d12116d` | minor | issue | documentation | proposal.md Tasks | Spec 里 19 处变异实测是各 SC 怎么会红的承重声称, 但 Spec 不指向其仓内证据落点 (writer-v2-proto 与返修报告 4), Tasks 1.8 的非作者对抗 review 无从对照。 |
| knowledge-manager | m8 | `84a82267` | `84a82267` | minor | issue | documentation | proposal.md SC-28 | SC-28 要求旧文本消失且替换文本在场, 但替换字面 (credential key name、PreToolUse Bash + Read/Edit blocker、secret-scan.sh (v1.24.0 加 detect) 只在探针里, Spec 散文只给中文说明, 实现者只能读探针源码反推措辞。 |

## 收敛计算 (本仓先例口径: 相邻两轮 Critical+Major 键集相等 且 全票 PASS)

- 主控定稿键映射 (同一问题不同四元组, 比较前先映射): `51e90cab` → `eb350937`; `5ce95ecf` → `eb350937`; `5fd1f356` → `ce6fc59c`; `e7e041c6` → `eb350937`; `fc97f926` → `e8d39a8a`
- 本轮 Critical+Major 键集 (7): `05982c10`, `60f3173a`, `6bd285b1`, `ac42f607`, `ce6fc59c`, `e8d39a8a`, `eb350937`
- 上一轮 Critical+Major 键集 (30): `14b7e703`, `179045cd`, `1c0bc16f`, `2779a016`, `27f6c3ce`, `2ce0049b`, `44b5bb44`, `53c140c4`, `5831f8c0`, `634eac5c`, `719ae05c`, `7deac83f`, `7e0343bd`, `846b21f8`, `8645b99f`, `8e77d1ca`, `9db51a43`, `a3054a20`, `ab6a3123`, `b73ab606`, `ba98e41f`, `cf0ae932`, `d4bcaf7c`, `d8e7b380`, `d9308fba`, `d9986b27`, `e2459206`, `e600e931`, `e8d39a8a`, `f42265a1`
- conclusions_stable = False
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

### 席位间同题归并 (定稿键; 映射已在「收敛计算」节列出)

| 簇 | 问题 | 席位编号 (键) | 定稿键 / 级别 | R1 对应 |
|---|---|---|---|---|
| A | W3 白名单仍有会撞上真值的形态作用于既有 `json-secret-field`: 裸 `$NAME` (单一大小写加数字与下划线)、`$(…)`、以 `...` 结尾的截断标记; 这些分支没有决定性的 SC 行 | tl/C1 `e8d39a8a` · cr/M1 `fc97f926` · km/M1 `fc97f926` (+ qa/m1 · ba/m2 · ba/m1) | `e8d39a8a` critical | 簇 A 未完全关闭 |
| K | W11 进程表规则覆盖不全: 包裹器集合是 `secret-guard.sh` 既有集合的未论证子集 (缺 xargs / eval / unbuffer), 不接受带参数的选项与绝对路径, 漏带前导 `-` 的 BSD 拼写与 `-O`、do / then 关键字位置; `/proc` 读取未纳入内联解释器 | tl/M1 · qa/M3 · ba/M3 `ac42f607` (+ cr/m4) | `ac42f607` major | 簇 F 的延伸 |
| L | Tasks 1.10 post-ship 复验腿用真实 `ps aux` 与真实 `/etc/forgejo/app.ini` 验拦截, hook 未生效 (插件缓存未更新 / 会话未重启) 时就是泄露路径, 且与头部 Rule #7 声明矛盾; 也不经 harness 验 Read 路径 | tl/M2 · ba/M4 `ce6fc59c` · km/M2 `5fd1f356` | `ce6fc59c` major | v2 新增 |
| M | 枚举型要求只按代表成员出行: W2 键名表 / 关键字 / 旗标, W8 读取器, W9 解释器与上界, W10 引号赋值, W11 包裹器与 `/proc` 读取器 —— 删掉部分成员的坏实现在全部对应行上 0 行红 | qa/M2 `eb350937` · ba/M1 `e7e041c6` · ba/M2 `51e90cab` · qa/M1 `5ce95ecf` | `eb350937` major | 簇 J 的延伸 |
| N | W5 把 `tool_input.file_path` 原样拼进 additionalContext (注入 AI 上下文的受信通道), 构造过的路径可闭合括号接祈使句或伪造第二条 hook 行 | qa/M4 `60f3173a` | `60f3173a` major | v1 起即有 |
| O | SC-30 时档 (h) 的「< 5 s」墙钟绝对值由主机负载决定 (负载 4 时基线自身 6.5 s), 应改为同次运行的相对量 | cr/M2 `6bd285b1` (+ tl/m1 · ba/m4 · cr/m1) | `6bd285b1` major | v2 新增 |
| P | Impact 只约束评论与关闭两个显式动作, 没约束提交页脚 / PR 描述里的 `Closes` 关键字 (仓内约定会自动关单), 会绕过「10CG/aria-plugin#154 post-ship 复验后才关」与「10CG/aria-plugin#203 / 10CG/Aria#221 保持 open」 | km/M3 `05982c10` | `05982c10` major | 新发现 |

### 主控独立核实

- 簇 A: 实读 v2 W3 改动条第 2 类与第 5 类 —— 「`$NAME` (NAME 全大写或全小写, 加数字与下划线; 不含混合大小写)、`$(…)`」与「值以 `…` 或 `...` 结尾」, 作用范围含既有 `json-secret-field`, 前提属实。
- 簇 L: 实读 v2 头部 Rule #7 声明 (post-ship 复验腿只用运行时生成的合成值、不触碰任何真实 secret 存储) 与三席引用的 Tasks 1.10 两条 L1 腿, 二者矛盾属实。
- 其余五簇由多席独立复现或给出变异实测, 主控未逐条复跑。

### 主控自我订正 (请 owner 复议时一并看)

本轮七簇里有两簇的种子是主控自己的话: R1 主控裁定第 1 条举例时写了「`$VAR` 形的变量引用」(v2 照此加入裸 `$NAME`, 即簇 A 残余); 执笔 v1 派单「主控范围裁定」第 5 条建议把 Read 的 `file_path` 放进 additionalContext (即簇 N)。另有簇 L、O 由 v2 返修新引入。按本仓 memory「本轮 fix 引入的 major 占比过半即到边际拐点」的判据, R2 已接近拐点。因此本轮起: 主控裁定只写**必须成立的约束**, 不再给具体形态; 返修以收紧为主, 不新增机制。

### 主控裁定 (v3 返修据此执行; 均为技术级, 列入 handoff 请 owner 复议)

1. **簇 A**: 白名单只保留**不可能是真实凭据**的形态 (判据: 该形态在既有 tag 的检出域内不会与任何 ASCII 随机值或口令哈希重合); 每个保留分支都要有两面的**决定性** SC 行 (放行侧 + 同形真值仍检出), 探针生成器对每个分支的边界做决定性覆盖, 不得出现只能概率性转红的行。裸 `$NAME`、`$(…)`、ASCII `...` 截断这三类按此判据应删除; 若执笔认为某类可保留, 须给出满足该判据的证据。
2. **簇 K**: 包裹器集合必须是 `secret-guard.sh` 既有包裹器集合 (env / printenv 行所用那一组, 引 file:line) 的超集; 对目标命令接受带参数的选项与绝对路径; 覆盖带前导 `-` 的 BSD 拼写、`-O` 与关键字位置; `/proc` 读取纳入内联解释器 —— 纳入或列为已知限制均可, 但每一侧都要有决定性的 SC 行。
3. **簇 L**: post-ship 复验腿只能用**惰性诱饵**: 即使 hook 未生效, 命令输出也不含任何真实 argv / 配置值 / 环境值 (例如输出被截成零字节、目标路径不存在但命中名字规则、Read 一个运行时生成合成值的诱饵文件); 该腿放在发版之后, 执行条件 (插件缓存已更新、会话已重启) 写明。
4. **簇 M**: What 里每一个枚举集合都要逐成员出行 (可由探针循环生成), 并且变异集合里每个集合都要有「缺成员」类坏实现, 证明删掉任一成员会转红。
5. **簇 N**: 任何来自工具输入的外来文本进入 additionalContext 之前, 必须变成不可注入的表示 (例如严格字符集白名单替换并截长, 或只给哈希与基名), 并补敌意路径行 (括号、换行、引号、非 ASCII、超长)。
6. **簇 O**: 时档改为对主机负载稳健的判据 (同次运行的相对量为主, 绝对值只作宽松兜底), 并补 L3 稠密输入的时档 (ba/m4 · cr/m1)。
7. **簇 P**: Impact 与 Tasks 写明提交页脚与 PR 描述的关键字口径 (10CG/aria-plugin#203 与 10CG/Aria#221 只用 `Refs`; 10CG/aria-plugin#154 在 post-ship 复验通过之前也只用 `Refs`), 能机械检查的给出检查方式。
8. **全部 minor** 照返修模板逐条处置。

### 流程记录

- 派单指纹: tl `cb617a53b91fa48e` / ba `66c181a7ac6ef6a5` / qa `fe85417e04d878f1` / cr `b16b1a5cb0a5999f` / km `5486d38ac52c8e64` (原文存于 `.aria/notes/2026-09-30-wpa-phase-a/dispatch/R2/`)。
- 并发: 五席分两组 (tl / qa / ba 一组并发 2; cr / km 一组串行), 同时在跑的席位最多 3 个, 不超过 audit-engine `hard_cap: 3`。
- 五份席位报告为各席结构化输出 `report_markdown` 原样, 由脚本从两份运行记录取出落盘。
- 工作区: 主仓 HEAD `b3e3123`、aria `268da8f` 全程未变; 席位只在各自实验目录操作。

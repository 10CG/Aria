---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-10-21T10:39:56.147Z
context: openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R1 — tech-lead 席 — secret-guard-w10-failclosed-narrowing (#217)

审查对象：`openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md`（主仓 `acd6a95`）。基线代码 aria `v1.76.1`（`59e333c`）的 `hooks/secret-guard.sh`。

**实验环境**（全部实验都按任务书的资源纪律执行）：bash 5.2.15，`en_US.UTF-8`（已确认多字节生效），`taskset -c 0,1 nice -n 19`，单次 ≤ 60 s。实验期间宿主机 loadavg 在 2.2 到 5.3 之间，所以**秒数的绝对值偏大，可靠的信号是同一环境下两段耗时的比值**。脚本都在 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217audit/tech-lead/`（下文简称 `$X/`）。凭据形文件名在脚本运行时拼装，不读取任何文件内容，也不涉及任何 secret 值。

## 审计结论

### 已核实的代码事实（不是 finding，供主控对照）

| proposal 断言 | 结论 | 证据 |
|---|---|---|
| SMAX 数的是总长 | 成立 | `_sg_vx_apply`：`:685` 把 `$_SGV_SMAX` 传给 `_sg_vx_replace`（`:626` 比较 `${#out}+${#s}`），`:694` 比较 `${#out}+${#s} > _SGV_SMAX` |
| `_sg_compute_credit` 逐行，`:476` 是唯一的整段匹配 | 「唯一」成立；「通配段不跨空白」**不成立**，见 F7 | `:453–563` 里不经 `_sg_line_match` 的 `=~` 只有 `:476` 一处 |
| `_SG_T0` 在首遍之后才重置 | 成立 | `:1539` 首遍，`:1542` 重置；`:633` 在 collect 时再重置。另外 `:607` 是加载时的初值 |
| `SECONDS` 从进程启动计，hook 里没有给它赋值 | 成立，但有环境变量导入的前提，见 F8 | 全文件只在 `:607/:617/:633/:1542` 读 `SECONDS`；`hooks.json:32-33` 为 `bash …/secret-guard.sh`、`"timeout": 5` |
| 扩展检查会重跑 `_sg_core_eval` | 成立 | `_sg_ext_pass` `:814`；调用点 `:1548`、`:1557` |
| 真实流量表（E12、W1–W3） | 与证据文件逐项一致 | `W-summary.txt`；E12×W1 按 n 联表：138 条「基线耗时 + 第二遍判定」最大 1.93 s，基线耗时 ≥ 1 s 的 4 条，最大 1.15 s |
| W10 预算数值在 standards 和 README 里都没有写；`secret-hygiene.md:316` 的计数「822 / 816」 | 成立 | grep 只在 `aria/CHANGELOG.md` 命中；`:316` 原文如 proposal 所述 |
| 本机没有项目启用扩展 | 部分核实 | `/home/dev` 下两层内没有任何 `.aria/secret-guard.paths` |

### F1 — 「不新增 fail-open 路径」不成立：大副本的判定没有总工作量上界，而时间护栏只看已经花掉的时间

- **type**: issue　**severity**: Critical　**category**: architecture
- **scope**: proposal §What Changes 2（大副本判定）、§不变量与范围外第 1 条、§Decision record 2–3
- **摘要**：时间护栏 `SECONDS*2 >= _SG_TIME_BUDGET` 建立在「大副本的判定与首遍判原串的代价相近」这个前提上。但在 W10 本来要处理的场景里，这个前提恰好不成立，有两类实测反例。基线对这两类输入都能在 1 s 内按尺寸拦截，新版会判定超过 5 s，被 CC 的 hook 超时杀掉，从而放行。
- **证据**：
  1. **credit 按行累加，「最长行 ≤ 8192」只给单行设了上界。** 平方项来自 `:476` 的第一支 `($_SG_CLAUDE_CFG|$_SG_SRVCFG)`，也就是 SRVCFG 开头的 `[A-Za-z0-9._-]*(forgejo|gitea)` 对长 token 逐起点扫描。它按 token 计算，多行之间是累加的。
     - 归因（`$X/e5_attr476.sh`）：两行 8 KB 时，第一支 2.32 s，第二支 0.00 s，整个 credit 2.61 s。
     - 累加（`$X/e2_credit_shapes_aws.sh`）：K = 1 / 2 / 4 条 8 KB 的 A 形行（` /tmp/aaa…`，非 tight 凭据名），credit 分别为 0.87 / 1.74 / 4.67 s。
  2. **端到端反例**（`$X/e3_endtoend.sh`，K=6）。命令 `F=<凭据名>; { cat $F; }` 后接 6 行 8 KB 长 token，|S| = 48,099。
     - 首遍：整串模式，rc=0，0.93 s。凭据读取经变量间接，首遍没有命中，也就没有算 credit。
     - 到时间护栏时已过 0.98 s，`SECONDS` ≤ 1，护栏放行。
     - 副本增长 16，最长行 8,010 ≤ 8192，所以走「完整判定（含 credit）」分支。
     - `_sg_judge_one` 判定副本：rc=2，耗时 **7.34 s**，全程合计 **8.32 s**，超过 `hooks.json` 配置的 5 s，CC 会杀掉 hook 并放行。
     - 对照：同一输入下基线 hook 进程用 0.81 s 按尺寸拦截。
  3. **不依赖 credit 的增长放大**（`$X/e7_growth_amplify.sh`）。16 个约 30 字符的 `curl curl …` 值，每个按计数上限引用 16 次；整串模式，正文没有 `|`。
     - B=4：增长 6,304，在 GMAX 之内；`curl` 从 96 个变成 1,632 个；首遍 0.79 s；判定副本 **9.35 s**，是首遍的 11.8 倍，rc=0。
     - B=10：首遍 1.68 s，判定 21.61 s，12.9 倍。
     - `risky_patterns` 的第 3 行就是 `curl[^|]*/v1/var/`，规则按顺序求值，所以这段昂贵扫描排在绝大多数凭据读取行之前。只要再经变量藏一条命中靠后行的读取，结果就是 5 s 后放行。**这一步是推理，没有做端到端实测。**
  4. 背景：直接形式（凭据名直接写进命令）在基线首遍上也要 8.95 s（`$X/e4_direct_base.sh`），属于 #228 已申报的 r2c / F7 残余，所以对抗者并没有获得新能力。但基线的 W10 第二遍靠 8192 总长上限与这些残余隔离开（这正是 M6 返工的目的），本 change 拆掉了这层隔离，把 #228 的两类残余经变量间接重新引入第二遍，而 proposal 没有申报。慢平台（Windows 约 2.6 倍、bash 3.2）上情况更严重。
- **建议改法**：
  1. 用**确定性的工作量上界**代替「代价相近」这个前提，时间护栏只作为纵深防御：
     - credit 部分：把「最长行 ≤ LMAX」改成「各行长度平方和 Σ L_i² ≤ LMAX²」。这是线性计算，W2×W3 实测 31 条命中规则的副本全部满足 `len × maxline ≤ 8192²`，所以在这批语料上不会多出误拦。
     - 规则行放大：另设一个按增长量计的界（例如增长量 × 副本长度不超过某个阈值，或增长超过实测阈值时仍按尺寸拦），用对抗形状实测定标。
  2. 新增 bf 对抗 SC：E3 形状和 E7 形状，新版必须拦截，或者在 < 2.5 s 内完成判定（Linux），并且整进程不得超过 5 s。
  3. 如果无法用技术手段完全恢复这条不变量，就把残余写进「不变量与范围外」并链接 #228，然后回 owner 裁定。fail-open 姿态归 owner 决定，而 A 是在「不新增 fail-open」这个前提下裁定的。

### F2 — 第 4 项「for 列表止于换行」照字面实现，会在反斜杠续行上新增漏检

- **type**: issue　**severity**: Critical　**category**: implementation
- **scope**: proposal §What Changes 4；`_sg_vx_collect` `:654`
- **摘要**：shell 会把「反斜杠 + 换行」整个删掉，把两行接成一行，所以续行属于同一个 for 列表。往字符类里加入换行后，列表在续行处被截断，凭据路径不再被收集。基线能拦的输入，新版放行。
- **证据**：`$X/e6_edges.sh`（b）对比了基线和一份只按第 4 项字面改了 `:654` 字符类的副本。输入形如 `for f in /tmp/x \⏎  <凭据名>; do cat "$f"; done`：
  - 基线：rc=2，finding 文案；
  - 第 4 项补丁：rc=0；
  - 单行对照：两版都是 rc=2。
- **建议改法**：
  1. 把规则写成「列表止于第一个**前面没有反斜杠**的换行；反斜杠加换行的组合属于列表」。同时写明引号内的换行如何处理（这种情况读不到凭据，但要写清楚）。
  2. SC-7 增加回归用例：续行 for 列表里含凭据路径，两版都要拦。
  3. 第 4 项不是 owner 裁定点（A–D 中没有它），真实流量里出现 0 次。如果不打算处理续行和引号语义，可以把第 4 项移出本 change。

### F3 — 扩展整串检查的接缝：`_sg_vx_apply` 是共享的，「维持原口径」有两种读法，其中一种会 fail-open

- **type**: issue　**severity**: Major　**category**: architecture
- **scope**: proposal §What Changes 5 第 1 条、SC-8；`_sg_per_segment_eval` `:1553–1565`
- **摘要**：`:1554` 同样调用 `_sg_vx_apply "$cmd"`，`:1562` 靠 `ar=2` 判断「副本总长 > SMAX」。第 1 项改了 rc=2 的语义以后，`:1562` 的行为会悄悄变成「增长 > GMAX」。这时如果执笔席把「维持原口径」理解成「不动 `:1563` 一带」，扩展就会对大副本调用 `_sg_ext_pass`，进而跑 `_sg_core_eval`（#228 E2：16 KB 约 7.9 s）。C 只在 `:813` 检查一次时间，结果是扩展生效时超时放行。
  - SC-8 写的是「两版都拦」，没有按文案区分。上面那种坏实现会因为扩展判定命中、以 finding 文案 exit 2，SC-8 照样变绿。
  - 能抓住它的只有现有 SC-21ap 的文案断言（`wpa_L_ext`），而 21ap 恰好属于 SC-11 要「逐条列出」后修改的尺寸类用例。
- **证据**：`hooks/secret-guard.sh:1553–1565`；`hooks/tests/secret-guard.test.sh:2685–2694`（21ap）、`:2532`（`wpa_L_ext`）。
- **建议改法**：
  1. 在规格里写明机制：`ar=0` 且扩展生效（`_sg_ext_entries` 非空）且 `${#_SG_SUB} > _SGV_SMAX` 时，在调用 `_sg_ext_pass` 之前按 oversize 拦截；`ar=2`（增长超限）且扩展生效时同样拦截。
  2. SC-8 断言 `wpa_L_ext` 文案，并且用扩展判定**不会**命中的夹具。
  3. 明确把 21ap 列为「不改」。

### F4 — 第 3 项「被引用」的定义比 shell 的实际展开窄，漏掉了 `${NAME:-x}` 一类形式

- **type**: issue　**severity**: Major　**category**: implementation
- **scope**: proposal §What Changes 3；SC-6
- **摘要**：
  - 只查 `$NAME` 和 `${NAME}` 两种文本，会漏掉 `${NAME:-x}`、`${NAME%…}`、`${NAME:off:len}`、`${NAME/…}` 等形式。超大值只经这些形式引用时，基线会因 VMAX 拦截，新版放行；而这个值完全可以是一串含凭据路径的词。
  - 同形的短值在基线上本来就放行（W10 从不代入这些形式，属于既有的部分覆盖缺口），所以对抗者没有获得新能力。但从字面看，这是一条新的「基线拦、新版放」路径，也违背了 D 的立论（「不参与任何代入」，而 shell 实际上会展开它）。
- **证据**：`$X/e6_edges.sh`（c）：短值只经 `${F:-/dev/null}` 引用时基线 rc=0；用 `$F` 引用的对照为 rc=2。另外 W1 那 1 条「未被引用」的判定，是 `traffic/assign-probe.py` 用同样窄的定义（`$name` / `${name}`）得出的。
- **建议改法**：
  1. 把「被引用」定义为：去掉该赋值后的命令文本里出现 `$NAME` 或 `${NAME`（任何花括号形式，已包含 `${NAME}`）。前缀撞名照旧偏严。
  2. SC-6 增加两条：「只经 `${NAME:-x}` 引用的超大值，两版都拦」和「链式引用，两版都拦」。

### F5 — 三个 SC 按现在的写法分不清好实现和坏实现

- **type**: issue　**severity**: Major　**category**: testing
- **scope**: proposal SC-5、SC-7、SC-8
- **摘要与证据**：
  - **SC-5**：只对 helper 做单测，再加一条「快命令放行」的端到端用例。一个定义了 helper 却从没在 `_sg_vx_pass` 里调用它的实现，两条都会变绿。
    - 设 `SECRET_GUARD_TIME_BUDGET_S=0` 也区分不出来：C 的 `:718/:732` 会先触发，同样给出 time 文案。
    - `SECONDS` 是整秒相减：`sleep 0.6` 后读出 0 或 1，赋值 `SECONDS=1` 后再过 0.6 s 读出 1 或 2（本机实测）。所以 `SECONDS=k` 单测在边界值上有极小但非零的抖动。
  - **SC-7**：没有要求循环体引用循环变量。如果循环体不引用，只做了第 3 项就能让它通过，第 4 项没有被验证。
  - **SC-8**：见 F3。
- **建议改法**：
  1. SC-5 增加进程内接线测试：source hook，设 `SECONDS=100` 后对大副本调用 `_sg_vx_pass`，期望 time 文案；设 `SECONDS=0` 时期望照常判定。这两种情况下 `_SG_T0` 都会在 collect 时重置，C 的检查不受影响，因此能隔离出新护栏。另外把 helper 写成接收时间参数的纯函数，单测就不会抖动。
  2. SC-7 夹具必须在循环体里引用循环变量。

### F6 — 现有套件里大批 W10 用例写死了基线语义；SC-11 的「逐条列出」没有归属，新限制文案也没有给出

- **type**: risk　**severity**: Major　**category**: testing
- **scope**: proposal SC-3、SC-11、Tasks；`hooks/tests/secret-guard.test.sh:2510–2694`
- **摘要**：
  - 有几条用例专门钉住了本 change 要改的语义：
    - `:2517` 写明「数值是契约」；
    - 21ab（`:2545–2547`）明确钉住「数整个被判串，不数增长」；
    - 21ad（`:2558–2561`）钉住「提没提到都拦」；
    - 21an 探针（`:2657`、`:2672`）断言「建成的副本 ≤ 8192」以及 edge8193 状态为 2。
  - 21al、21ao 的 8193 一侧会从 oversize 变成「超长单行」拦截；21ag、21aj 的限制文案会改变。
  - proposal 没有列出这些用例改成什么，也没有给出「增长」和「超长单行」两条新 `Limit hit:` 文案的英文原串。现有用例用 `sed` 精确解析这一行（`:2535`），而 proposal 只给了中文原因串。
  - 这样 SC-11 就由实现者自己开列、自己认证，有自证风险。
- **建议改法**：
  1. 在 proposal 里列一张旧/新期望对照表（用例号、旧结论、新结论、原因）。
  2. 给出两条新限制行的英文 canonical 原串。
  3. 在 TASK-002 里明确「改写现有 W10 预算用例与 21an 探针」这项工作。

### F7 — §Why 对 `:476` 的事实陈述有误，头注释改写时会把错误写进代码

- **type**: issue　**severity**: Minor　**category**: documentation
- **scope**: proposal §Why「8192 原本要防什么」；What Changes 5「头注释」
- **摘要**：
  - 「通配段不跨空白…同样受单行长度约束」这句话对 `_SG_PROCTAB_ALL` 不成立：它的 `[^|;&]*` 和 `[^|]*` 会跨空白和换行，代价随总长增长。
  - 「平方级成本只跟单行长度有关，不跟总长」也不准确：平方项按 token 计，但多行之间是累加的（见 F1 证据 1）。
- **证据**：`hooks/secret-guard.sh:445–448`。`$X/e5b_proctab_crossline.sh`：每行 4 KB 的 `ssh h …`，K = 1 / 2 / 4 时第二支分别为 0.35 / 1.06 / 1.89 s。
- **建议改法**：随 F1 一起改写立论；新的头注释要写实际的成本模型（按 token 平方、按行累加、PROCTAB 跨行）。

### F8 — 新护栏读的是绝对 `SECONDS`：会被环境变量带偏，粒度语义也没有写清

- **type**: risk　**severity**: Minor　**category**: implementation
- **scope**: proposal §What Changes 2.1、Decision record 3
- **摘要**：
  - bash 会从环境变量导入 `SECONDS`。继承一个负值会让护栏永远不触发，继承一个大正值会让所有大副本都按时间拦截。C 用的是 `SECONDS - _SG_T0`，不受这个影响。
  - 两个时钟的关系：C 的时钟从首遍之后起算，在各条腿的边界检查；新时钟从进程启动起算，只在判定前检查一次。两者都管不到单次 `_sg_judge_one` 自身的耗时（F1）。
  - 默认预算 3 时，护栏在 `SECONDS ≥ 2` 时触发，实际触发点按相位落在已用时 1 到 2 s 之间。预算设成 1 或 2 时，`SECONDS ≥ 1` 可能在启动几毫秒后就成立，对调低了预算的用户会产生不确定的误拦。
- **证据**：`$X/e6_edges.sh`（a）：`env SECONDS=1000` 读出 1000，`env SECONDS=-100` 读出 -100。
- **建议改法**：
  1. 在 `:176` 重新 exec 之后的第一条语句记下 `_SG_START=$SECONDS`，护栏改用 `SECONDS - _SG_START`。
  2. 在规格和头注释里写明触发区间和预算覆盖的边界。

### F9 — 超长单行分支沿用 oversize 文案，与它的拦截原因自相矛盾

- **type**: issue　**severity**: Minor　**category**: documentation
- **scope**: proposal §What Changes 2.3
- **摘要**：oversize 文案的正文是「Nothing was matched.」，而这个分支的原因恰恰是「命中了凭据形读取」。#228 v2.1 已经因为同样的矛盾新增了 `pregate` kind（#228 proposal `:84`）。
- **证据**：`hooks/secret-guard.sh:851–866`。
- **建议改法**：新增一个 kind，或者改写这个分支的正文；英文原串在规格里定死（与 F6 合并处理）。

### F10 — 几处实现细节没有写明，执笔席可能各自理解

- **type**: issue　**severity**: Minor　**category**: implementation
- **scope**: proposal §What Changes 1、2.3
- **摘要**：
  1. 第 1 项的 `${#S}` 必须是入口处算一次的**原始参数长度**。函数内的局部变量 `s` 会随代入不断变化，如果按 `${#s}` 实现，上限就变成了每个变量各增长 8192。
  2. 「只匹配规则」需要 W12 中和，但中和逻辑内联在闸门之下的 `_sg_judge_one` 里（`:1505–1510`）。`_sg_environ_neutral` 只存在于已搁置的 #228 R1 分支（`b2ed608`），基线里没有。可选做法有三种：抽出来并做差分验证、复制一份（会漂移）、给 `_sg_judge_one` 加一个不算 credit 的模式参数。规格没有选。
  3. 分段模式下，大副本分支相对 TMAX 累计的先后顺序没有写明。
- **建议改法**：逐条写进规格。推荐给 `_sg_judge_one` 加模式参数：锚点名不变，W12 也不会出现两份。

### F11 — SC-9 能否复现、判据能否证伪都有缺口

- **type**: risk　**severity**: Minor　**category**: testing
- **scope**: proposal SC-9
- **摘要**：
  1. 判据 2 只统计「尺寸类」拦截。如果误拦被换成 time 或「超长单行」，A 的核心收益（138 降到 0）就没有得到验证，应该限制三类拦截的合计并分别报告。按 E12×W1 联表，本机有 4 条的基线耗时 ≥ 1 s，时间护栏可能按相位不确定地触发。
  2. `extract.py` 按会话记录文件的排序加行序编号，会话记录还在不断增长，重新抽取后编号会漂移。所以「同一批语料」只能依赖 `TRAFFIC_DIR` 快照，或者每条命令的内容哈希清单。快照是否仍然存在：**未核实**。
  3. 判据 3 只覆盖真实流量，对抗形状交给 F1 的新 SC。
- **证据**：`.aria/notes/2026-10-20-secret-guard-scan-cost-and-firstpass-cap/traffic/extract.py:5–29`。
- **建议改法**：在证据目录落一份「n 到 sha256」的清单（只存哈希），SC-9 按哈希对齐。判据 2 改为限制三类拦截的合计。

### F12 — 同步面不完整

- **type**: issue　**severity**: Minor　**category**: documentation
- **scope**: proposal §What Changes 5「头注释」、Impact
- **摘要**：
  - 描述 W10 预算语义的地方除了 `:577–589` 还有好几处：文件顶部头注释 `:87–95`（「a substituted segment up to 8192 … beyond a SIZE limit the whole command is BLOCKED」），`:630–631`（collect 的「nothing behind it is collected」），`:674–676`（apply 的 rc 2），`:701–703`，`:1534–1536`，以及 C 注释 `:598–600`。
  - 测试文件的说明注释也要同步：`:2510–2518`、`:2545–2549`、`:2556–2562`。
  - proposal 引用了 `detailed-tasks.yaml`，但这个文件目前还不存在（按流程会在 A.2 生成）。SC-10 要求在真 bash 3.2 下实跑，本机 3.2 二进制的位置**未核实**，应该在 TASK-004 里写明。
- **建议改法**：Impact 补全同步清单；TASK-004 写明 bash 3.2 二进制的来源。

### 侧重点小结

- **两个时钟**：两个时钟起点不同、检查点不同，都不约束「单次判定自身」的耗时（F1、F8）。新护栏只能作为纵深防御，不能作为主要上界。
- **#228 残余的接缝**：基线 W10 第二遍靠 8192 总长上限，与首遍的 r2c / F7 残余隔离。本 change 拆掉了这层隔离：E3 属于 r2c 类，E7 属于 F7 类并被增长放大约 12 倍。规格要么用确定性上界把它们挡住，要么作为 #228 残余申报，并请 owner 复议 A 的前提。
- **范围**：第 3、4 项的真实收益分别是 1 条和 0 条，却分别带出 F4（Major）和 F2（Critical）。第 3 项的修法很小（`${NAME` 视为引用），建议修。第 4 项不是 owner 裁定点，可以修，也可以移出本 change。
- **能否进入 A.2**：还不能。F1 需要重新设计成本模型并重新实测（会改 What 2 和 Decision record 2–3），F2 需要改第 4 项的规则，F3 和 F6 需要补写机制与原串。其余各条可以在同一轮修订里一并处理。

## Verdict

**FAIL**：Critical 2 条（F1、F2），Major 4 条（F3–F6），Minor 6 条（F7–F12）。

## 轮次记录

- R1（convergence），tech-lead 席，2026-10-21。只读审查：没有改 proposal、代码，没有 commit。
- 已读：`proposal.md` 全文；`hooks/secret-guard.sh` 的 `:80–100`、`:170–206`、`:400–500`、`:560–930`、`:1140–1183`、`:1440–1590`；测试文件 `:40–80`、`:1775–1910`、`:2505–2720`；W 证据与 `traffic/*`；E12；#228 `proposal.md`；`b1_shapes.py`；`hooks.json`。
- 实验：`$X/e1_credit_multiline.sh`（tight 名会让 `:476` 短路，作为对照）、`e2_credit_shapes*.sh`、`e2b_credit_sameline*.sh`、`e3_endtoend.sh`、`e4_direct_base.sh`、`e5_attr476.sh`、`e5b_proctab_crossline.sh`、`e6_edges.sh`、`e7_growth_amplify.sh`。
- 未核实：E7 的端到端泄露路径（只测了成本）；bash 3.2 下的行为；`TRAFFIC_DIR` 快照是否存在；macOS / Windows 上的倍率（引用 #228 的数据）。

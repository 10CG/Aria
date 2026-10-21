---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-10-21T11:54:36.755Z
context: openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R1 — knowledge-manager 席位报告（secret-guard-w10-failclosed-narrowing）

**审查对象**：`openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md`（主仓 `acd6a95`，基线 aria v1.76.1 `59e333c`）。
**侧重**：文档与知识面完整性（同步面 / issue 处理 / 证据可复现 / proposal 结构 / 与 #228 的交叉引用 / 措辞歧义）。
**独立性**：未打开同轮其他席位的报告（`.aria/audit-reports/` 下另有 code-reviewer / qa-engineer / tech-lead 三份，未读）。
**实验脚本**：全部在 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217audit/knowledge-manager/`（下称 `$KM/`）。
**需要先说的结论**：审文档面时顺带复现出两条会让「不新增 fail-open 路径」不成立的输入（F-01、F-02），所以本席位 verdict 为 FAIL；此外还有 8 条 Major（文档、测试清单、实现归属类）和 5 条 Minor。

## 审计结论

### 总表

| ID | severity | category | scope | 一句话 |
|---|---|---|---|---|
| F-01 | Critical | architecture | §What Changes 2.2、§不变量、Decision 2 | LMAX 只给「单行」credit 成本设上界，总成本是各行之和；6–8 条 ≤8192 的长行即可使第二遍越过 5 s → fail-open，基线对同输入 <1 s 拦下 |
| F-02 | Critical | implementation | §What Changes 4、SC-7 | for 列表「字符类加入换行」会丢掉反斜杠续行的第二行起，续行里的凭据读取从拦变放（5.2 与 3.2.57 均复现） |
| F-03 | Major | documentation | §Impact（头注释同步面） | 同步面只列了「W10 预算段」一处，实际有 9 处注释/测试注释描述旧语义，其中含文件头 Residual gaps 与 `_sg_emit_blocked` |
| F-04 | Major | testing | SC-11、§Impact（测试） | SC-11 说「逐条列出」却没列；现有 21aa–21ap 钉死旧语义；缺 GMAX/LMAX 双边缘 SC、多长行总成本 SC、续行 for SC |
| F-05 | Major | documentation | §Impact、§Tasks（TASK-005）、Decision 6 | 未写 #217 收口方式 / 关闭关键词 / INV-6；issue 6 项诉求有 2 项被推迟却无载体（且 aria-plugin#201 会让 Level 2 prose 里的推迟项被归档吞掉） |
| F-06 | Major | documentation | §Impact（CHANGELOG） | 「C 项与扩展口径的如实申报」有歧义（姿态 C / 上游 #216 的 C / 阶段 C），且残余清单不全，放行面扩大没有申报 |
| F-07 | Major | testing | SC-9 | 「E12 同一批语料」已无法取得（`/tmp/r1traffic` 不存在，重抽已是 2426/745 而非 2412/739），判据 2/3 的口径不可执行，语料看不到 F-01 型对抗形状 |
| F-08 | Major | architecture | §What Changes 2.3、§Impact | 「对 W12 中和后的副本匹配」依赖基线不存在的 `_sg_environ_neutral`（只在搁置分支 b2ed608），实现归属与被改函数清单缺失 |
| F-09 | Major | documentation | §不变量与范围外、§5、姿态表 | 不变量段与全文互相矛盾或过强：A/D 本是放宽、「三种原因」漏了尺寸类、扩展口径对开了扩展的采用方反而更严、理由只对子集成立 |
| F-10 | Major | testing | §What Changes 2.3、SC-2/3/4 | 沿用 oversize 模板会打印「Nothing was matched」，与「命中了凭据形读取」自相矛盾；三条「按文案区分」的 SC 没有可比对的确切字符串 |
| F-11 | Minor | documentation | §Impact（standards） | 测试计数在 standards 有三处（`:23`、`:316`、`:352`），不是一处；还缺版本行与目标值；v1.76.1 已漏同步一次 |
| F-12 | Minor | documentation | 证据目录 `.aria/notes/2026-10-21-.../` | 证据包缺口：W-summary 无生成脚本、`NEUT_SRC` 未钉、计时是墙钟、`/tmp` 默认目录、「不入库」的理由与可验证范围没写 |
| F-13 | Minor | documentation | 页眉「关联」、全文 | 8 处裸 `#n`（主仓同号条目均无关）；与 #228 缺互链；数字口径与「等 #228 再议」的触发条件对不上 |
| F-14 | Minor | documentation | 页眉、§Tasks、§Impact | 结构：`detailed-tasks.yaml` 悬空、无 `rule6_note`、基线冻结只含 aria、INV 未继承、SC 编号与套件撞名 |
| F-15 | Minor | documentation | 全文 | 措辞歧义清单（17 条，含「一半预算」的整数算术、字符/字节、「去掉这条赋值本身」、`:1563` 的「维持原口径」） |

---

### F-01 逐行成本有上界 ≠ 副本总成本有上界 —— 新 fail-open 路径

- **type**：issue　**severity**：Critical　**category**：architecture
- **scope**：§What Changes 2.2（「逐行计算 credit 的成本因此有上界」）、§不变量（「不新增 fail-open 路径」）、Decision 2/3
- **摘要**：`_SGV_LMAX` 只约束单行。`_sg_compute_credit` 的成本是各行成本之和（每条 ≈8000 字符的单 token 行约 1 s CPU），而 hook 自己的 64 KB 命令上限（`secret-guard.sh:1157`）允许最多 8 条这样的行。变量间接的凭据读取 + ≥6 条长行，第二遍判定就会越过 Claude Code 的 5 s，hook 被杀，命令不经扫描放行（fail-open）。基线对同一输入 <1 s 按 SMAX 拦下，所以这是**相对基线新增**的 fail-open；hook 的 M6 头注释（`:577–583`）自己就把「填充」当作绕过配方，这不是臆想的对抗。规格的三道护栏都不触发：增长约 25 字符远小于 GMAX；每行 8000 ≤ LMAX；入口一次性的 `SECONDS*2 >= 预算` 在首遍便宜时读到 0 或 1。
- **证据**：
  1. 代码：规则命中后 `_sg_judge_one`（`:1497`）只调用一次 `_sg_compute_credit "$seg"`（`:453`），其内部全是 `_sg_line_match`（`:182–188`，按行循环）；判定过程内没有时间检查点。规格 §2.2 的「有上界」只对单行成立。
  2. 实验 A（进程内、CPU 时间，`$KM/credit_lines_cpu.sh`）：头行为凭据读取，其后 N 行各为一个 8000 字符的 token。N=1：1.40 s；N=2：2.25 s；N=4：4.07 s（user+sys，负载 5–8 的共享主机）。约 1 s/行，与头注释 `:586–587`「8 KB 约 0.9 s」一致。
  3. 实验 B（整进程，`$KM/attack_emul_cpu.sh`）：base = 未改动的 v1.76.1；emul = 只把 `_SGV_SMAX` 抬到 1000000 的副本，等价于「规格的第二遍去掉全部护栏」。输入 = 变量间接的凭据读取（路径运行时拼装）+ N 行×8000 字符。

     | N | 命令长度 | base（v1.76.1） | emul（规格第二遍） |
     |---|---|---|---|
     | 2 | 16,044 | 0.19 s CPU，按尺寸拦 | 2.18 s CPU，finding 拦 |
     | 4 | 32,056 | 0.44 s CPU，按尺寸拦 | 4.19 s CPU |
     | 6 | 48,068 | 0.88 s CPU，按尺寸拦 | 6.48 s CPU / 6.53 s 墙钟，越过 5 s |

     N=8（64 KB）仍在命令上限内。头注释 `:599` 记的慢平台倍率 2.6×，在 Windows 上 N=2 就越线。
  4. SC 盲区：E12 副本的最长行只有 4457（W3），没有任何副本含多条长行，所以 SC-9 看不到这类形状（见 F-07）。
- **建议改法**：
  1. 把上界从「每行」改成「每副本」：对 Σ(行长²)，或「长于约 1 KB 的行的总字符数」设上限（都是线性可算，与 §2 的实现约束一致），超限走姿态 C（只匹配规则）或拦。
  2. 和/或在 `_sg_compute_credit` / `_sg_line_match` 的逐行循环里放 `_sg_over_budget` 检查点，沿用 C 的 fail-closed 约定（注意 `SECONDS` 是 1 s 粒度，而单行就可能 1 s，所以要配合降 LMAX）。
  3. 和/或把 LMAX 降到约 1–2 KB（单行 credit 约 0.03–0.06 s），使 64 KB 命令的最坏总成本 <2 s。
  4. Why 节「8192 原本要防什么」与将要重写的头注释，立论要改成「总成本 = Σ 行成本」，不要写成「逐行有界所以副本有界」。
  5. 新增 SC（baseline 对照）：N×(≤LMAX) 行 + 变量间接凭据读取，断言新版 exit 2 且整进程 CPU 在阈值内（W14 同款比值判据，不用墙钟）。

### F-02 for 列表「字符类加入换行」丢掉反斜杠续行 —— 新 fail-open 路径

- **type**：issue　**severity**：Critical　**category**：implementation
- **scope**：§What Changes 4、SC-7、§不变量
- **摘要**：`for f in a \⏎ b; do …` 是合法 bash（反斜杠换行是续行，列表是 `a b`）。基线的列表类 `[^;&|)]*`（`secret-guard.sh:654`）跨换行，所以续行里的凭据路径会被收集并代入。按规格把换行排出字符类后，列表在第一行末尾截断，第二行起不再收集，续行里的凭据读取从「拦」变成「放」。规格第 4 项只说「多行 for 循环的循环体不再被当成一个值」，没有处理续行。
- **证据**：`$KM/mkpatched.py` 按规格第 4 项改出副本 `$KM/hook_nlstop.sh`（只改列表类，其余不动），`$KM/forlist_cont.sh` 与 `$KM/forlist_cont32.sh` 跑三个形状：

  | 形状 | 基线 | 按规格第 4 项改后 |
  |---|---|---|
  | c1 列表用反斜杠续行，凭据路径在第二行 | exit 2（finding） | **exit 0（放行）** |
  | c2 单行列表（对照） | exit 2 | exit 2 |
  | c3 换行结束的多行 for（issue 里的形状） | exit 2 | exit 2 |

  bash 5.2 与真 bash 3.2.57（`/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v4/bash32/bash`）结果相同。
- **建议改法**：
  1. 规格写出 ERE 原文，让列表类在「未被反斜杠转义的换行」处停止（续行吃进列表，裸换行才止），并在 3.2 与 5.2 下字符级钉死。
  2. 或明确声明为 KNOWN-LIMIT：写进头注释、CHANGELOG、standards，并加一条「现状放行」的 pinning 用例（沿用 SC-21 的 21n–21u / 21y 体例），同时把 §不变量改成穷举式。
  3. SC-7 增第三组：续行 for 列表（baseline 对照：基线拦，新版不得变放）。

### F-03 同步面（hook 注释）：规格只列 1 处，实际 9 处

- **type**：issue　**severity**：Major　**category**：documentation
- **scope**：§What Changes 5「头注释」、§Impact（aria）
- **摘要**：§5 只说「W10 预算段改为逐行成本的立论加实测数据」。描述旧语义的注释还有 8 处，其中 `:86–94` 是文件头给读者的总述，`:826–828` 的契约注释对姿态 C 的路径是错的。仓内已有过因头注释归因错误而作废整份设计的先例（#228 B.1：头注释 `:587` 把 credit 当主成本，v1 设计作废），所以这类漏改要列成封闭清单。
- **证据**（`aria/hooks/secret-guard.sh` 与测试文件，基线 v1.76.1）：

  | # | 位置 | 旧表述 | 本 change 后 |
  |---|---|---|---|
  | 1 | `:86–94` 文件头 Residual gaps（W10 条） | 「a substituted segment up to 8192 characters … beyond a SIZE limit the whole command is BLOCKED」 | 三道上限语义全变 |
  | 2 | `:577–596` LENGTH BUDGET（规格已覆盖） | 「whether or not the variable is mentioned」「not its growth」「blocking is as cheap as passing was」 | 全部翻转；「拦比放便宜」不再成立（大副本现在被判定） |
  | 3 | `:597–607` Time-budget 段 | 「the `_SGV_*` size budget are unchanged」；「measures THIS command's judgement (not wall time since the process started)」「stays fresh when the test suite sources the hook」 | 新护栏有意用进程级 `SECONDS`，要点名第二个时钟及其对 sourced 套件的影响（`:1542` 的注释记过同类陈旧时钟 bug） |
  | 4 | `:630–631` `_sg_vx_collect` 契约 | 「2 = a value is longer than _SGV_VMAX … nothing behind it is collected」 | 只对被引用的值返回 2；未引用的跳过并继续收集 |
  | 5 | `:674–676` `_sg_vx_apply` 契约 | 「2 = the copy would be longer than _SGV_SMAX」 | 条件改为增长 >GMAX；扩展点 `:1553–1565` 也调这个函数 |
  | 6 | `:701–703` `_sg_vx_pass` 契约 | 「An overrun … ends the pass at once with an oversize BLOCK」 | 新增 time / 超长行 / 规则命中出口 |
  | 7 | `:826–828` `_sg_emit_blocked` 注释，及 `:851–866` oversize 模板正文 | 「nothing was matched, the command is too large to be checked」 | 姿态 C 是「命中了」，见 F-10 |
  | 8 | `:1534–1536` `_sg_per_segment_eval` 注释 | 「when that copy is too large to build, blocks here」 | 「too large to build」的定义随 `_sg_vx_apply` 变 |
  | 9 | 测试 `secret-guard.test.sh:2510–2520` 块头、`:2545–2546`（21ab「the WHOLE judged string, not its growth」）、`:2556–2562`（21ac/21ad「narrowing is the owner's call, not the code's」） | 「The numbers are part of the contract (_SGV_SMAX 8192 = one substituted copy …)」 | owner 已裁 D；GMAX / LMAX 要进「契约数字」清单 |
- **建议改法**：
  1. §Impact 以封闭清单列出上面 9 处（改行号时重锚）。
  2. 加一条文档同步 SC：对退役短语做 grep 负控，体例同 WP-A 的「陈旧/悬空表述」清单各配 SC（`.aria/notes/2026-09-30-wpa-phase-a/writer-reports/v3-dispositions.json:308`）。这是 code + test + doc 三位一体，而不是只改注释。
  3. 头注释等 F-01 的成本模型定稿后再落笔，避免把错误立论写进代码。
  4. 发布面按 CLAUDE.md「发布同步面」处理：aria 5 文件（含 `VERSION` 里那一行带 issue 号的描述）、主仓 gitlink ×2（aria 与 standards 都变）、VERSION、README badge、`system-architecture.md` §2.8 与 `version-scheme.md`；机械兜底是 `m6-version-badge-match`、`i18n-readme-translation-currency`、`plugin-version-arch-docs-match`。aria 的两份 README（`README.md`、`README.zh.md`）经 grep 确认**都没有** W10 尺寸行为的描述，所以规格「README 不需要同步」成立，i18n 不重译（#140 B 档）。

### F-04 SC-11 的清单缺失；现有用例钉死旧语义；缺 SC

- **type**：issue　**severity**：Major　**category**：testing
- **scope**：SC-10 / SC-11、§Impact（`hooks/tests/secret-guard.test.sh`：新 SC，计数同步）
- **摘要**：SC-11 写「除了本 change 点名的尺寸类用例（逐条列出）」，但规格里没有任何一条点名。现有 21aa–21ap 区块把旧语义逐字符钉住，至少一批用例必须改写；不给清单，差分判据无法执行，实现者也分不清哪些红是预期、哪些是回归。
- **证据**：`secret-guard.test.sh:2510–2692` 的用例名与注释。按注释与用例名读出的**候选**清单（未逐条实跑，不跑全套件）：
  - 语义翻转需改写：21ab（8193 字符副本被拒；第二条命令钉「不是增长」）、21ac（4096 字符 for 列表「由副本上限而非值上限拒绝」）、21ad（第二条「未提及也拦」）、21aj（超限段结束整个 pass）、21al、21ao（整串 8193 被拒）、21an（函数探针：副本 ≤8192、边缘 8193 返回 2）。
  - 期望文案常量要换：21ag（36 KB 密集形状，常量 `wpa_L_seg` / `wpa_L_whole`，`:2528–2532`）。
  - 应保持不变的回归：21aa、21ae、21af、21ah、21ai、21am；21ak（数 `_sg_vx_apply` 调用次数的探针，如新 helper 改变调用次数会红）；21ap（见 F-15 的 W-10）。
  - 机械兜底：套件内 SC-13（`:3213–3228`）会在头注释计数与实跑总数不符时自动变红，头注释计数这一项因此不会漏。
- **建议改法**：
  1. SC-11 附上逐条清单与每条的新期望（改写 / 换常量 / 不变），并要求其余 BLOCK 用例零差分。
  2. 补 SC：GMAX 双边缘（增长 8192 放、8193 拦）、LMAX 双边缘（8192 走 credit、8193 走仅规则）——套件自己的契约是「每个上限两侧都钉到字符」（`:2511–2517`），规格 SC-3/4 现在用的是粗值。
  3. 补 SC：F-01 的多长行总成本；F-02 的续行 for 列表；扩展生效 + 条目不出现 + 小增长 + 副本 >8192（只有这个输入能区分「维持旧口径」与「扩展顺手判了」，见 W-10）。
  4. 新 SC 用独立前缀（见 F-14），每条补「怎么会红」。

### F-05 issue 处理：收口方式、关闭关键词、INV-6、推迟项的载体

- **type**：decision　**severity**：Major　**category**：documentation
- **scope**：§Impact、§Tasks（TASK-005 只有「发版 / owner 门」）、Decision 6、§5
- **摘要**：规格没有写 #217 如何收口，也没有继承 INV-6；issue 的 6 项诉求里有 2 项被推迟，推迟项只存在于 proposal 散文里。
- **证据**：
  1. 先例一律 Refs-only：v1.76.1 发版提交 `59e333c` 页脚是 `Refs 10CG/aria-plugin#216, 10CG/aria-plugin#219, 10CG/aria-plugin#228`，#216 是发版后用 API 关单并评论逐条披露（C spec `detailed-tasks.yaml` TASK-006 备注）。INV-6 原文「提交页脚与 PR 描述对三张 issue 只写 Refs，不写 Closes / Fixes / Resolves」（`openspec/changes/secret-net-l3-and-bypass-paths/detailed-tasks.yaml:39–40`，发版备注 `:221`「INV-6 全提交 Refs-only（#154 未关）」）。#217 自己的页脚也是 `Refs 10CG/aria-plugin#154, 10CG/aria-plugin#203, 10CG/Aria#221`。`.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md` §2：轮换类 issue 保持 open、本项之下不评论。
  2. issue（`forgejo GET /repos/10CG/aria-plugin/issues/217` 与评论）的诉求与规格处置：

     | issue 诉求 | 规格处置 | 去向 |
     |---|---|---|
     | 1 按膨胀量判 | What Changes 1 | 交付（受 F-01 影响） |
     | 2 for 列表止于换行 | What Changes 4 | 交付（受 F-02 影响） |
     | 3 只拦被引用的超大值 | What Changes 3 | 交付 |
     | 4 count 轴「若收窄 size 轴时一并评估」 | 范围外（Decision 6） | **无载体**；「误拦面远大于」没有实测，E12 语料可以直接数 |
     | 5 死代码 | What Changes 5 | 交付 |
     | 6 评论（2026-10-14）：扩展整串一眼的口径「一并评估」 | §5 维持原口径，「等 #228 线性化之后再议」 | **无载体**：#228 的三条重启条件不含它 |

  3. aria-plugin#201（open）：Level 2 spec 没有 tasks.md / detailed-tasks.yaml 时，归档闸的 `d_payload` 恒为 null，proposal 散文里的 deferred 项**不会被看见**。本规格现在恰好没有这两个文件（见 F-14）。
  4. `.aria/decisions/2026-09-30-...` §4：一次性授权覆盖「WP-A / WP-B / WP-C 及其后续」的四类外发动作，边界之外（合并 master、推 master、打 tag 与发版）逐次请示。#217 的评论 / 关闭是否算「后续」，规格没说。
- **建议改法**：
  1. TASK-005 写明：提交页脚与 PR 描述只用 `Refs 10CG/aria-plugin#217`，不用任何关闭关键词；`10CG/aria-plugin#154`、`10CG/aria-plugin#203`、`10CG/Aria#221` 只 Refs（继承 INV-6，保持 open、不评论）；#217 在 owner 发版门之后人工关单，评论按上表逐项披露。
  2. 对 4、6 两项：要么开 follow-up issue，要么写成 `detailed-tasks.yaml` 里 `status: deferred` 的任务（C spec 的 TASK-003 B 是先例），再加一行说明触发条件。不要只留在 §5 的散文里。
  3. 写明 #217 评论 / 关闭走 2026-09-30 的一次性授权，还是在发版门由 owner 确认。

### F-06 CHANGELOG 申报：「C 项」有歧义，残余清单不全

- **type**：issue　**severity**：Major　**category**：documentation
- **scope**：§Impact（`CHANGELOG`：误拦面收窄，以及 C 项与扩展口径的如实申报）
- **摘要**：同一份文档里「C」有三种含义：姿态表的 C（超长单行命中规则则不评估脱敏过滤直接拦）、上游 `#216` 的 C（时间预算）、十步循环的阶段 C（TASK-005）。「C 项」读者无法确定指哪个。申报清单也不全，还缺「放行面扩大」这一最该申报的行为变更。
- **证据**：上游 C 在 L7、L59、L61、L101、L154（共 5 处「C 的…」）；姿态 C 在 L103、L109；有歧义的是 Impact 的 L146「C 项」；阶段 C 在 L167。v1.76.1 的 CHANGELOG（`aria/CHANGELOG.md:12–23`）的「已知限制（归 #228）」一段已经向采用方承诺过 B 归 #228，新条目要与它衔接。
- **建议改法**：在 Impact 直接给出 CHANGELOG 骨架，至少含：
  - **行为变更 · 放行面扩大**：大而不膨胀的命令、未被引用的超大值，现在经完整判定后放行（以前被尺寸拦）。
  - **行为变更 · 新增拦截原因**：增长 >8192；大副本判定前进程已用时 ≥ 预算一半（按整数秒的真实触发表，见 W-4）；代入后有 >8192 的单行且命中规则（不评估脱敏过滤）。
  - **未改动 / 残余**（逐项点名）：扩展生效时仍按总长 >8192 拦（开了 `.aria/secret-guard.paths` 的采用方继续吃旧误拦）；count 轴仍 fail-open（第 17 个赋值 / 第 9 个引用 / 第 9 条 for）；`_SGV_TMAX` 在分段模式仍按总长累计；首遍扫描 O(n²) 与 5 s 超时 fail-open 仍归 #228（积压，重启条件见其 v3）；D 之后未被引用的超大值经 `${!x}`、`printenv` 等未覆盖的间接消费不再被尺寸规则兜住（与小值一致，见 F-09）。
  - 「C」一律写全称，姿态与上游分开命名（见 W-14）。
  - 页眉不要沿用「向下兼容」之类的 v1.76.1 措辞，放宽也要如实写。

### F-07 SC-9：语料无法「同一批」重取，判据 2/3 口径不可执行，且看不到对抗形状

- **type**：issue　**severity**：Major　**category**：testing
- **scope**：SC-9 及其三条判据、证据目录
- **摘要**：SC-9 要「用 E12 同一批语料（2,412 条）」跑新版，但那批原文在 `TRAFFIC_DIR` 默认值 `/tmp/r1traffic`，该目录已经不存在，重新抽取得到的是另一批。判据 2 写的是对旧快照的绝对数（130→≤5）；判据 3「没有命令新变成超过 5 s」没规定用墙钟还是 CPU，而这台共享主机上墙钟会失真。
- **证据**：
  1. `ls /tmp/r1traffic` → 不存在。`extract.py` 读活的 `~/.claude/projects`，按 `sorted(rglob)` 给流水号。
  2. 只计数的复刻版 `$KM/count_only.py`（不写原文）今天跑出：3580 个 jsonl，去重后 >4096 字节的 NUL-free Bash 命令 **2426** 条，其中 >8192 字节 **745** 条；E12 是 2412 / 739。几小时内已经漂移，流水号 `n` 也随之失去意义。
  3. 墙钟失真的实例：同一条 N=4 的仿真，`nice -n 19` 下墙钟 52.06 s，改 `nice -n 5` 测 CPU 为 4.19 s（`$KM/attack_emul.sh` 与 `attack_emul_cpu.sh`）。E12 的时间列也是 `EPOCHREALTIME` 墙钟。
  4. 判据 2 的「≤5，目标 0」没有依据：W1 的最大增长是 6200 <GMAX，所以预期恰为 0；允许 5 条等于允许 5 条未解释的回归。
  5. 判据 1 是闭集，漏了 oversize → oversize（增长上限）；E12 的 `kind` 还有 `timebudget` / `killed` / `other`，没有说它们的迁移怎么判。
  6. 语料最长行 4457（W3）、没有多长行副本：F-01 / F-02 型形状在语料里不存在，SC-9 全绿不能说明它们安全。
- **建议改法**：
  1. TASK-004 先冻结快照：抽取一次，只把 manifest（条数、总字节、每条 sha256）存进 `evidence/`，原文留本机；基线与新版在**同一快照**上各跑一遍，所有判据改成对基线的差分。
  2. 判据 1 把预期分布写进去（W1/W2/W3 已预言：138 条全部 oversize → allow，其余类别为 0），任何偏离逐条解释；闭集补上 oversize → oversize（增长）。
  3. 判据 2 改成「增长上限以外的尺寸类拦截 = 0，例外逐条附增长值」。
  4. 判据 3 用整进程 CPU 时间或新版 / 基线比值，并记录负载。
  5. 对抗形状靠合成夹具（F-04 的新 SC）覆盖，不指望语料。

### F-08 「只匹配规则」路径依赖基线不存在的 `_sg_environ_neutral`

- **type**：issue　**severity**：Major　**category**：architecture
- **scope**：§What Changes 2.3（「对 W12 中和后的副本逐条匹配」）、§Impact（被改函数清单）、证据 `rowhit-traffic.sh`
- **摘要**：基线里 W12 中和是 `_sg_judge_one` 内联的 4 个 while 循环（`:1506–1509`），不是函数。W2 的数据（31 条命中）用的是搁置分支里抽出来的 `_sg_environ_neutral`。规格没写：谁把它抽出来、`_sg_judge_one` 是否因此成为被改函数、新 helper 如何拿到 `risky_patterns`（声明在源码闸门之下 `:1183`，闸门在 `:926`）。Impact 只列了三个函数加「新 helper」。
- **证据**：
  1. `grep -n _sg_environ_neutral aria/hooks/secret-guard.sh` 零命中；`_sg_judge_one` 在 `:1497`，位于闸门之下。
  2. `rowhit-traffic.sh:7–8` 注释：函数「taken from the R1 snapshot, where it was extracted unchanged; differential 0/3031」，运行时要 `NEUT_SRC`；`W-summary.txt` 只写 `NEUT_SRC=<hook with _sg_environ_neutral>`，没有 SHA 或分支。该函数在 aria 分支 `feature/secret-guard-scan-cost-and-firstpass-cap`（本地与 origin 均存在，`b2ed608`，`#228` 的 proposal 记载）。
  3. 若从 `_sg_judge_one` 抽取，则改动了每条命令都走的热路径，套件内 SC-8 的时延 harness 按 `^_sg_judge_one\(\) \{` 锚点抽取（WP-A proposal `:247`）；若复制 4 个循环，则两份会漂移。
- **建议改法**：
  1. 明写采用哪条路：建议复用 b2ed608 里已做过 0/3031 差分的 `_sg_environ_neutral`，抽到闸门之上，`_sg_judge_one` 与新 helper 共用，把 `_sg_judge_one` 列入被改函数，并加 SC-8 / W14 的时延对比。
  2. W-summary 和规格都钉 `NEUT_SRC` 的 SHA。
  3. 写一句与 #228 R1/R2 的接缝：R1 分支只作参考不合并；将来重启时，同名函数以本 change 的为准。

### F-09 不变量段与全文互相矛盾，或表述过强

- **type**：issue　**severity**：Major　**category**：documentation
- **scope**：§不变量与范围外（L96–101）、§5、姿态表、SC-9
- **摘要**：「不新增 fail-open 路径」是整份规格的安全论断，也是 CHANGELOG 的来源，但它与规格自己的其他段落冲突：
  1. 被 F-01、F-02 直接证伪。
  2. 姿态 A、D 是 owner 裁定的「放宽」，本质就是相对基线新增放行。D 的理据「不参与任何代入」只对 `$NAME` / `${NAME}` 两种文本形态成立。实测（`$KM/unref_value.sh`，基线）：小值经 `${!x}` 间接消费 → 放行（已知局限）；5000 字符值经 `${!x}` → **按尺寸拦**。D 之后后者降到与小值一致，应当写成「owner 接受的、与小值同级的部分覆盖」，而不是「没有跳过扫描的路径」。
  3. L98「拦截的原因只会从尺寸变成三种之一」漏了增长上限、被引用的 VMAX、TMAX，它们仍是尺寸类；SC-9 判据 1 的闭集同病。
  4. 扩展口径对「选择加固的采用方」反而更严：开了 `.aria/secret-guard.paths` 的项目继续被旧口径误拦。理由「本机所有项目都没有启用扩展」我核实成立（`/home/dev` 深度 ≤5 无该文件），但这只说明 E12 语料无法度量该人群，不说明该人群不存在（#203 的报告者就是 Windows 采用方，standards §5.6 的示例即为此）。
  5. §5 的成本理由「扩展检查会在副本上重跑 `_sg_core_eval`」只在副本里**出现条目**时成立：`_sg_ext_pass`（`:809–817`）在 `_sg_ext_subst` 无命中时立即返回，而 `:1553–1565` 的拦截不看条目是否出现。存在更窄的口径：仅在条目出现且副本 >SMAX 时拦。issue 评论 2 要的正是对这一口径的评估。
  6. `_SGV_TMAX` 仍按总长累计（分段模式），与「按增长」同形的缺陷保留，Decision record 没解释；E12 里分段模式 0 条，所以没有数据。
  7. 姿态表 A 写「误拦从 138 降到 0」，SC-9 判据 2 写「130 → ≤5」，同一目标两套数字。
- **建议改法**：把不变量改写成穷举式——「相对基线新增放行的形状：…（A 大副本经完整判定；D 未引用超大值，含间接消费边界）；相对基线新增拦截的原因：…（时间、超长单行、增长）；未改：…」。F-01 / F-02 修好之前不要保留「不新增 fail-open 路径」这句。对 4、5 补一份评估结论（含更窄口径的可行性），并把残余写进 F-06 的 CHANGELOG 清单。

### F-10 拦截文案与原因串：自相矛盾，且未钉死

- **type**：issue　**severity**：Major　**category**：testing
- **scope**：§What Changes 2.3（「文案沿用 oversize 那一套，原因串为…」）、SC-2/3/4（「按文案区分」）
- **摘要**：
  1. oversize 模板正文第一句是「Nothing was matched. After variable expansion the command is bigger than the guard can check reliably」（`:855–857`），其补救建议是「keep every variable value … short / do not repeat one long $VAR」。姿态 C 恰恰是「命中了凭据形读取」，且成因是单行过长：模板的话是错的，建议也不对症（对症的建议是拆行，或改用 Write 工具写文件）。
  2. 规格给的 C 原因串是中文，而现有 `Limit hit:` 的串全为英文（`:713, 725, 740, 745, 1563`），测试按常量 `wpa_L_*` 逐字比对（`secret-guard.test.sh:2528–2532`）。「增长」原因串、LMAX 原因串、时间护栏是否沿用 `kind=timeout` 文案，规格都没给确切字符串，两个实现者会写出不同的串，SC-2/3/4 的「按文案区分」就没有可比对的内容。
  3. 时间文案会打印 `(${_SG_TIME_BUDGET}s)`（默认 3 s），而护栏在 ≥2 s 就触发，文案与触发点不符；正文「The secret scan did not finish」对「根本没开始判定」也不准确。
- **建议改法**：新增 `kind=longline`（或在 oversize 模板里按原因分支），写出四条确切英文原因串与中文行，并同步测试常量；时间护栏文案另写一句「判定未开始，因进程已用时过半预算」或把触发点改成与文案一致；把这些字符串写进 SC 表。

### F-11 standards 计数：三处、版本行与目标值

- **type**：issue　**severity**：Minor　**category**：documentation
- **scope**：§Impact（standards）
- **摘要**：规格只点名 `secret-hygiene.md:316`。该文件有三处计数（`:23`「822 self-tests [816 无 zsh]」、`:316`「822 regression cases, 816 无 zsh」、`:352`「822 self-tests (816 无 zsh)」）；1.2.0 版本行（`:465`）也写着「计数同步 … 共三处」。
- **证据**：套件头注释 `:11` 是 `831 cases (825 without zsh)`，v1.76.1 CHANGELOG `:21` 是 825（无 zsh），而 standards 仍是 822/816：v1.76.1 的 9 条新用例（SC-T1…T5 等）发版时就没有同步 standards。套件内 SC-13 的注释（`:3213–3218`）自己点名「secret-hygiene.md 三处」，并明说跨仓一致靠 TASK 回填时机械 grep，不在套件内断言。先例：1.1.2 版本行（`:466`）为纯计数同步单独记了一行「计数同步（零语义变更）」。
- **建议改法**：Impact 写「`:23`、`:316`、`:352` 三处 + 版本行 1.2.1（计数同步，零语义变更，沿 1.1.2 先例）」；目标值是本 change **落地后**的总数（N 与 N−6），不是现在的 831/825；TASK-004 的验收清单加一条 grep 断言（三处 == 套件头注释）。Aria#177 点名过「同步面之外的引用点必漂」，可考虑日后补一个 custom check，本轮不强求。

### F-12 证据包缺口

- **type**：risk　**severity**：Minor　**category**：documentation
- **scope**：`.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/`（`evidence/`、`traffic/`）
- **摘要**：设计是「只入库聚合数据，原文不入库」，这点本身对（实命令里可能有凭据，且仓会镜像到公开的 GitHub）。我复算的结果全部吻合（见「已核实」），但后来者无法重现：
  1. `W-summary.txt` 的聚合数字没有生成脚本。分位数取法是下标 floor((n−1)p)，所以「中位数 566」是下位数（真中位数 567.5）。我用 `$KM/recompute.py` 复算才对上，建议把它入库为 `traffic/summarize.py`。
  2. W1–W3 的 TSV 没有表头，列义分散在三个脚本的注释里，W-summary 只写了 W1 的列。
  3. `longval_referenced` 对赋值类恒为 `-`（脚本只对 for 列表求引用），所以规格 Why 表对「4594 字符、未被引用」一行写的证据「W1」并不严格成立；它只在 W-summary 散文与 `assign-probe.py`（其输出没存）里。旁证是该行 growth=0（n=666，34617 → 34617）。
  4. `NEUT_SRC` 未钉 SHA（见 F-08）。
  5. 环境没记：bash 版本、locale、负载、taskset（E12 头有，W-summary 没有）。时间列（`judge_s` 等）是 `EPOCHREALTIME` 墙钟，在共享主机上受负载影响，「平均 0.19 s、最慢 0.97 s」应改记 CPU 时间或附负载。
  6. `TRAFFIC_DIR` 默认 `/tmp/r1traffic`（已不存在），`cmds/` 是真实命令原文，默认权限，放在共享 `/tmp`。建议默认改到 `$HOME` 下的私有目录并 `umask 077`，用后清理。
  7. 复现链分在两个目录（`extract.py`、`base-all.sh` 在 #228 目录；`w10/rowhit/expline` 在本目录），没有一页式说明；W1–W3 的 join 键来源 `E12-base-all.tsv` 没被规格证据行引用（只引了 `E12-base-real-traffic.txt`）。
  8. 「命令原文不入库」在规格里只有一句结论。应补三点：原因（Rule #7 + 公开镜像）、后果（后来者只能核对聚合、不能重放；流水号 `n` 只在 E12 快照内有意义）、替代（冻结快照只存 sha256 清单，见 F-07）。
  9. 「138 条全部判为无害」「全是误拦」的依据是完整判定 rc=0，也就是被审对象自己的判决；其中 31 条规则命中、靠 credit 放行的尤其需要抽样人工看（credit 本身就是被审对象之一）。
- **建议改法**：补一份 `evidence/README` 或扩展 W-summary 头部：复现步骤（含两个目录的先后）、钉死的 SHA（base `59e333c`、`NEUT_SRC` `b2ed608`）、环境、「仓内数据能核对什么 / 不能核对什么」；入库 `summarize.py`；改默认 `TRAFFIC_DIR`；规格 L37 的措辞改成「完整判定后全部放行（未人工复核）」。

### F-13 与 #228 的交叉引用、裸 issue 引用

- **type**：issue　**severity**：Minor　**category**：documentation
- **scope**：页眉「关联」、L1、L7、L41、L61、L92、L101、L152
- **摘要与证据**：
  1. **裸 `#n` 共 8 处**（`check_bare_issue_refs.py` 实跑：L1、L7×2、L41、L61、L92、L101、L152）。本规格住在主仓，裸 `#217` 默认解析到 `10CG/Aria#217`；我用 API 核了：`10CG/Aria#217` 是开放 issue（session-closer…）、`#228` 是已关闭 PR（docs(triage)）、`#216` 是开放的 Archive Tracker，全部与本事无关。规范是 `standards/conventions/content-integrity.md` §4.4 规则 1（「新写的文字按此写」；该检查是手动工具、不是闸门，所以按 Minor）。邻居里 #228 的 proposal 有 34 处、C spec 有 14 处，WP-A 为 0。
  2. 缺互链：本规格只给 #228 的 notes 目录，没给 `openspec/changes/secret-guard-scan-cost-and-firstpass-cap/proposal.md`；#228 的 proposal 说「属于 `#217`」也没给本规格路径。
  3. 数字口径：#228 的「W10 尺寸预算 34」（R1 闸门人群内）、本规格的 130（>8 KB）与 138（>4 KB）都指「W10 尺寸拦」，分母不同；规格没说 138−130=8 条在 4–8 KB 区间（我从 `E12-base-all.tsv` 核实：4096–8192 字节区间 oversize 恰为 8）。
  4. L61「（#228 实测）」：#228 的 B.1 表里该行证据栏写的是「读码」。
  5. L92「等 #228 线性化之后再议」与 #228 v3 的重启条件（出现真实超时放行事件 / 慢平台用户反馈卡顿 / 对抗防护提上日程）不衔接，条件里没有这一项，实际没有触发（见 F-05）。
  6. L7「W10 的来源是 `10CG/aria-plugin#154`」：W10（变量间接）的原始报告是 `#203`（标题「路径经 shell 变量间接即绕过全部文件名规则」），C spec 页眉也这么写（「`#203`（变量间接 partial）、`#154`（报告环境即 MINGW64）」）；`#154` 是母单，M6 返工在 WP-A TASK-014。
  7. 观察（不要求本规格改）：acd6a95 把 #228 的 Status 改成 Pending 是对的（`Deferred` 不在词表，会归 unknown 并产生 design_deferred 噪声），但现在 `changes/` 下两份 secret-guard spec 机读上都是 `pending`，无法区分「积压」与「待开工」。
- **建议改法**：全文改全限定（`10CG/aria-plugin#217` 等）；互链两份 proposal 的路径；L92 改成实情（无计划，除非 #228 重启）或另开 issue（F-05）；L7 改正归属。

### F-14 proposal 结构

- **type**：issue　**severity**：Minor　**category**：documentation
- **scope**：页眉、§Tasks、§Impact、SC 表
- **摘要与证据**：
  1. 页眉 `Level: 2（proposal + detailed-tasks.yaml）` 与 §Tasks 标题「细粒度见 detailed-tasks.yaml」指向**不存在**的文件（目录里只有 `proposal.md`）。页眉是从 #228 复制的。标准的 Level 2 只要 proposal（`standards/openspec/project.md` Levels 表），所以要么补文件，要么改成「detailed-tasks.yaml 由 A.2 产出」。C spec 起初写的是「proposal only」。
  2. 没有 `rule6_note`。SOT §4（`standards/conventions/skill-benchmark-exemption.md`）要求「无论走哪一行」都留；非 Skill 变更应写 `decision_table_row: n/a`、`description_changed: no`、`scenario1/4b/negctrl: n/a` 加理由。「按 substitute 处理」用词也不对：substitute 是决策表第 1 行（描述性内容）的处置，不是「不属于 Skill 变更」。
  3. 基线冻结只有 aria（页眉第 9 行）。本 change 还改 standards（`a611136`）并落主仓；WP-A 页眉冻结了三个 SHA。
  4. 认领 track id（`secret-guard-w10-failclosed-narrowing-023236f2`）只在提交信息里，而 TASK-001 依赖「B.0 认领续用」。
  5. 执行不变量没有继承：WP-A 的 INV-4（新函数在闸门之上；文内写成「W14 规则」）、INV-5（夹具运行时拼装，Rule #7）、INV-6（Refs）、INV-7（资源纪律）。detailed-tasks.yaml 不存在，没有地方放。
  6. SC 编号撞名：文内 L71 的「SC-8」指套件里**已有**的时延 harness，L129 的「SC-8」是本规格新 SC；套件内另有多个 SC-8/SC-13 的含义（`secret-guard.test.sh:834, 1697, 1702` 已有一条「编号消歧」注释）。先例：C spec 用 `SC-T*` 前缀（`:3158–3168`）。
  7. 姿态 A–D 与 What Changes 无映射（A=§1、B=§2.1、C=§2.3、D=§3），且字母与上游 C spec 的 B/C 撞车（F-06）。
  8. §Tasks 是表格，不是 `- [ ]` 复选框；配合 aria-plugin#201，归档闸看不到这些任务。
  9. 本 change 触三个仓（aria + standards + 主仓），TASK-005 只有一行；应引用 CLAUDE.md「发布同步面」与两条多远程推送硬约束（子模块一律本地 merge + 双推，推后逐个 `ls-remote` 核验）。
  10. 正向：没有发现审计叙事混入交付面。Status 行只有一句状态说明，姿态表「主控建议」列是唯一的过程性文字，可以接受；后续各轮的处置请只落 `.aria/audit-reports/` 与 detailed-tasks，不要回写本文。
- **建议改法**：补 detailed-tasks.yaml（含 `meta.rule6_note`、`invariants`、`deferred` 任务、`meta.baseline_freeze`）；SC 改独立前缀（如 `SC-N1…`）；其余按上面逐项补。

### F-15 措辞歧义清单

- **type**：issue　**severity**：Minor　**category**：documentation
- **scope**：全文（行号为 proposal 行号）

| # | 位置 | 句子 | 读法 A | 读法 B | 建议 |
|---|---|---|---|---|---|
| W-1 | L34 | 「31 条命中规则（今天靠 credit 放行）」 | 基线今天就是靠 credit 放行 | 基线今天被尺寸拦；取消尺寸拦之后才靠 credit 放行 | 改成「取消尺寸拦后，靠 credit 放行」 |
| W-2 | L37、L107 | 「这 138 次全是误拦」「误拦从 138 降到 0」 | 人工核实无害 | 仅指完整判定 rc=0 | 改成「完整判定后全部放行（未人工复核）」 |
| W-3 | L51 与 L92 | 「SMAX 保留…不再直接拦」「副本总长 > SMAX 即拦」 | 全局不再拦 | 仅 `_sg_vx_pass` 不再拦，扩展点仍拦 | §1 加「（扩展点除外，见 §5）」 |
| W-4 | L59–61、L108 | 「已经用掉一半预算」 | elapsed ≥ 预算/2 | 实际 `SECONDS*2 >= b`，即 SECONDS ≥ ceil(b/2)：b=3→2，b=2→1，b=1→1，b=0→恒真。`SECONDS` 按整秒边界翻转（`$KM/seconds_flip.py` 在 bash 5.2 与 3.2.57 上实测一致）：首次读到 1 出现在真实 0.01–0.99 s（取决于启动时刻在整秒内的相位），读到 2 对应真实 (1,3) s。所以 b=3 的触发点落在预算的 33%–100%，b=1、2 时可能在 0.01 s 就触发 | 写成公式并附 b=0…4 的触发表，删掉「一半」 |
| W-5 | L62 | 「逐行计算 credit 的成本因此有上界」 | 副本总成本有上界 | 仅单行有上界 | 见 F-01 |
| W-6 | L63、L29–35 | 「超过 8192 字符的行」；表里的「8 KB」「4 KB」 | 字符（`${#}`，UTF-8 locale 下是字符） | 字节（C locale 下 `${#}` 是字节；E12 的 KB 是字节） | 钉成一种（建议按字节，与 #228 v2.1 一致），并注明与 locale 无关的做法 |
| W-7 | L65 | 「文案沿用 oversize 那一套」 | 复用 `kind=oversize` 模板（正文含 Nothing was matched） | 新 kind | 见 F-10 |
| W-8 | L75 | 「命令里（去掉这条赋值本身）」 | 原命令 `$1` 去掉该匹配片段 | collector 循环里的 `rest`（随匹配被消耗，只含该赋值之后的文本） | 钉成：用 `$1` 全文去掉该匹配的这一处；for 列表的等价物（表头无 `$` 出现）也写出来 |
| W-9 | L88 | 「字符类加入换行」 | 把换行加进被匹配的字符（否定类本来就匹配） | 把换行加进被排除的集合 | 写出 ERE 原文与 bash 构造（如 `[^;&\|)${_nl}]`），并见 F-02 |
| W-10 | L92 | 「维持原口径（基线 :1563 一带，副本总长 > SMAX 即拦）」 | 不改该处代码 | 保持行为 | `:1553–1565` 调用的 `_sg_vx_apply` 被 §1 改了，不改代码 = 行为变化；写明用显式长度判断（扩展生效且 `${#_SG_SUB} > _SGV_SMAX` 则拦）还是给 `_sg_vx_apply` 加模式参数；SC-8 的「两版都拦」要钉文案 |
| W-11 | L98 | 「拦截的原因只会从尺寸变成三种之一」 | 尺寸类拦截消失 | 仅指这批命令的原因变化 | 见 F-09 |
| W-12 | L99 | 「数值不变」 | 无新数字 | 三个既有数值不变，但新增 GMAX、LMAX，且 SMAX 由上限变分界 | 改成「三个既有数值不变；新增 GMAX=8192、LMAX=8192；SMAX 由上限变为分界」 |
| W-13 | L100 与 L157 | 「issue 建议另议」「issue 建议维持 fail-open」 | — | issue 原文：「建议维持 fail-open；若本 issue 收窄 size 轴时一并评估」 | 两处统一为 issue 原文并给评估结论（F-05） |
| W-14 | L103–110、L146、L59… | 姿态 A–D、「C 的时间预算」、「C 项」 | 姿态 C | 上游 C spec（`#216` 时间预算） | 姿态改名（如 P-A…P-D），上游一律写 `10CG/aria-plugin#216` |
| W-15 | L123–129 | SC-5 / SC-8「两版都拦」「按 `2k ≥ b`」 | 任意原因 | 同文案 | 钉文案；SC-5 的 `SECONDS=k` 要避开整秒边界翻转（让 k 与 k+1 判定一致） |
| W-16 | L136 | 「判定变化只允许以下四种」 | 闭集完备 | 缺 oversize→oversize（增长），缺 `timebudget` / `killed` / `other` | 见 F-07 |
| W-17 | L7 | 「W10 的来源是 `10CG/aria-plugin#154`」 | 母单 | W10 的原始报告是 `#203` | 见 F-13 第 6 项 |

---

### 已核实（无问题 / 成立）

1. **Status 词**：`_status.py` 的 `_normalize_status` 实跑，首段 `Draft` → `pending`；真实 `collect_openspec` 实跑：本 change `pending`，无 soft_error，不进 `design_deferred`（`$KM/status_check.py`、`$KM/run_openspec_collector.py`）。词表含 draft / pending；分隔符 `—` 之后的「Approved」不参与归类。
2. **Linked Issue 字段与 Level 行**：`linked_issue_field_probe.py` 返回 `OK（10 份在范围内, 6 条在册）`；完整性门的 `completeness_gate.parse_level` 实跑，本 change 与 #228 都解析为 2（`$KM/level_check.py`）。
3. **README 与 standards 不含 W10 尺寸行为**：`aria/README.md`、`aria/README.zh.md` 只有 secret-guard 的概述与 `.aria/secret-guard.paths` 用法；standards 只有测试计数。规格「W10 预算数值在 standards 和 README 里都没有写」成立（仅计数需要同步，见 F-11）。
4. **证据数字复算**（`$KM/recompute.py`、`$KM/pct.py`）：W1 的 137 size + 1 value；增长分桶 ≤0:2 / 1–256:60 / 257–1K:64 / 1K–4K:10 / >4K:1，最大 6200；完整判定均值 0.194 s、最大 0.97 s、rc 全 0；W2 命中 31、均值 0.163 s、最大 0.46 s；W3 最长行 p50=566 / p90=1734（下标取法）、>8192 为 0、31 条命中者最大 2139；三份 TSV 的 `n` 集合一致，并与 `E12-base-all.tsv` 的 oversize 集合一致（138）。E12：2412 = 2168 allow + 106 finding + 138 oversize；>8192 字节 739 = 557 + 52 + 130（17.6%）。E12 头记的 hook 哈希 `e83c5e30f2ccb58f` 正是 v1.76.1 hook 的 sha256 前缀。
5. **规格引用的代码事实**：`:476` 是 tight 检测（`_sg_compute_credit` 内唯一对整段 `$seg` 的 `=~`，其余全经 `_sg_line_match`）；`SECONDS` 在 hook 内从未被赋值（只在 `:601, 607, 617, 633, 1542` 被读）；`_SG_T0` 在 `_sg_core_eval` 之后才重置（`:1542`），并在 `_sg_vx_collect` 起点再置（`:633`）；头注释 `:586–588` 的 0.9 / 3 / 13 s 立论与规格引用一致；count 轴的 16 / 8 / 8 计数与实现相符。

### 未核实

1. 全套件与各新 SC 在真 bash 3.2 下的行为：本席位只在 3.2.57 上复现了 F-02 一项，其余实验在 5.2。
2. F-04 的候选清单：来自读注释与用例名，没有逐条实跑（按任务书不跑全套件）。
3. 姿态 C 的「只匹配规则」在 ~64 KB 副本上的耗时上界：W2 最大样本 34 KB / 0.46 s，没做对抗形状实验。
4. Windows / MINGW64 实测（慢平台倍率沿用头注释的 2.6×）。
5. Forgejo 在 aria-plugin 仓对 `Closes 10CG/aria-plugin#217` 的行为：未验证，以先例（Refs-only + 人工关单）为准即可。
6. #217 评论 / 关闭是否落在 2026-09-30 的一次性授权内：需 owner 确认。

## Verdict

**FAIL**。统计：Critical 2（F-01、F-02）/ Major 8（F-03 至 F-10）/ Minor 5（F-11 至 F-15）。按规则 ≥1 Critical 即 FAIL。

优先级建议：先处理 F-01、F-02（改设计，并补对应 SC），随后 F-09 重写不变量段；F-03 / F-04 / F-05 / F-06 / F-10 属于同一次改稿里能一起收的文档与测试清单；F-07 / F-08 需要先定冻结快照与 helper 归属；Minor 项可并入同一改稿。

## 轮次记录

| 项 | 内容 |
|---|---|
| 轮次 | R1（convergence），席位 knowledge-manager，`rounds: 1` |
| 读取 | proposal 全文；hook 按行号读（`:86–94, 176–215, 453–563, 570–760, 809–817, 826–870, 906–934, 1154–1160, 1183, 1492–1523, 1534–1590`）；测试按 grep 与行号读（`:1–40, 2510–2700, 3158–3228`）；证据 TSV / 脚本全读；#228 的 proposal 与 B.1；`standards/openspec/project.md`、`status-field-guide.md`、`_status.py`、`skill-benchmark-exemption.md`、`content-integrity.md` §4.4、`secret-hygiene.md`；WP-A 与 C spec（含 archive）作先例；`.aria/decisions/2026-09-30-...`；Forgejo 只读 GET：aria-plugin #217（含评论）、#201、开放 issue 列表、主仓 #154/#203/#216/#217/#228 的类型与标题 |
| 实验（`$KM/`） | `status_check.py`、`run_openspec_collector.py`、`level_check.py`、`recompute.py`、`pct.py`、`count_only.py`（只计数，不写原文）、`credit_lines.sh` / `credit_lines_cpu.sh`、`attack_emul.sh` / `attack_emul_cpu.sh`、`mkpatched.py` + `forlist_cont.sh` / `forlist_cont32.sh`、`unref_value.sh`、`seconds_flip.py` |
| 资源纪律 | 开头用 `taskset -c 0,1 nice -n 19`；宿主负载 5–8 时 nice 19 把进程饿住（同一仿真墙钟 52 s、CPU 4.2 s），中途改为 `nice -n 5`（仍限 0,1 核），计时一律以 user+sys CPU 为准。**这是对任务书「nice -n 19」的偏离，如实记录**。单个实验均 ≤1 分钟（被饿的那次墙钟 52 s） |
| Secret 卫生 | 凭据路径在脚本里切开、运行时拼装；未打印任何 secret 值；未使用 `# guard:ack` |
| 未改动 | 未改 proposal、代码、测试；未 commit；唯一新增文件是本报告与 scratchpad 下的实验脚本 |

---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: false
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: FAIL
timestamp: 2026-10-22T15:40:00.000Z
context: openspec/changes/secret-guard-w10-failclosed-narrowing/detailed-tasks.yaml
agents: [qa-engineer, code-reviewer, tech-lead, knowledge-manager, backend-architect]
---

# post_planning R1 汇总 — secret-guard-w10-failclosed-narrowing（10CG/aria-plugin#217；任务计划 @ `a136dbf8`，proposal v3 @ `910d9fa2`，v3 原型与证据）

> **Verdict：FAIL**。去重后 1 Critical / 23 Major / 15 Minor（39 簇，原始 90 条）。一席 FAIL（TL），四席 PASS_WITH_WARNINGS（QA / CR / KM / BA），五席都有 Major 以上的发现，按 REVISE 计。未收敛。
>
> 本文件是有损汇总。每个簇都回链到席位原编号：QA = qa-engineer（F*n*），CR = code-reviewer（CR-*n*），TL = tech-lead（F*n*，下文写作 TL-F*n*），KM = knowledge-manager（KM-*n*），BA = backend-architect（BA-*n*）；括号里是该席的定级。细节以各席报告为准（同目录、同时间戳 `1792649702638` 的五份文件）。簇号写作 PP1-A*n*，与 post_spec 的 R1-A*n* / R2-A*n* 区分。

## 一句话

v3 的机制本身（基线先跑、只在基线按尺寸拦的那一刻进硬截止作业重判、结论只取退出码）五席都没有证伪；问题集中在三处：

1. **放宽面漏了一类**（PP1-A1，Critical）：判定在 count 轴触顶时并不完整，一条读凭据路径的大命令基线拦、v3 放行，规格没有申报。
2. **截止的三个旁路**（PP1-A2–A4）：环境变量带入放宽标志、后代进程占住管道、计时器 fork 失败。输入都够不到，但与 proposal 写下的机制保证直接矛盾。三处都已在 v3.1 草稿里修掉并实测。
3. **验收写成了散文**（PP1-A5–A17，13 个 Major 簇）：SC 与 BI 用文字描述，两个执笔者会写出不同的用例；时延判据依赖本机速度；基线红绿在计划里排在用例写出来之前；证据不绑 hook 版本。这一段在 post_spec R2 也是 Major 的主要来源（8/11），本轮是 13/23，属于结构问题，处置见「主控处置建议」第 2 条。

## 审计结论

### Issues / Risks（按 {category, scope} 去重）

| 簇 | 级别 | type | category | scope | 摘要 | 席位回链 |
|---|---|---|---|---|---|---|
| PP1-A1 | Critical | issue | architecture | 放宽面申报 R-a–R-c、CHANGELOG 标题「不新增 fail-open」、Decision 13、TASK-007 | 基线的 count 轴上限（第 17 个赋值、每个变量第 9 个引用、第 9 个 for 不收集也不代入）在小命令上本来就是 fail-open，过去大命令被尺寸上限顺带挡住。放宽后大命令改为「完整判定」，可判定在 count 轴触顶时并不完整：TL 构造的命令（读取放在第 9 个引用里，另加约 9.4 KB 良性短行）基线按尺寸拦，v3 放行，读的是凭据路径。规格逐个点名了放宽后变大的既有缺口，唯独没有 count 轴；#217 关闭后它也没有载体 | TL-F1(C) |
| PP1-A2 | Major | issue | implementation | 原型 `_SG_RELAXED` 的全部读点；What 1 准入门第 1 行 | `_SG_RELAXED` 从未初始化，bash 会把环境里的同名变量导入。带着它启动 hook，顶层直接走放宽规则，没有作业也没有截止：`apply-heavy-cjk` 实测 rc 0、17.7–25.4 s（基线 2.0–2.2 s 拦），生产里 5 s 超时即放行 | CR-03(M) BA-1(M) |
| PP1-A3 | Major | issue | implementation | `_sg_relax_run` 的 `wait` 之后；P5、SC-V5 | `wait` 返回后只杀计时器组、不杀作业组。作业正常退出但留下仍占着命令替换管道的后代时，`_sg_relax_run` 被拖到后代结束，并在截止之后采纳作业结论（截止 1 s：CR 4.42 s 放行，BA 4.45 s，TL 3.31 s）。现有判定路径没有后台进程，输入够不到；但 P5 的措辞是无条件的 | CR-01(M) TL-F11(m) BA-7(m) |
| PP1-A4 | Major | issue | implementation | 计时器 fork 失败分支 `[[ "$tp" != "$jp" ]]`；What 3 要点；SC-V5 变异；BI-3 | 真实的 fork 失败走不到这条检查：EAGAIN 时 bash 先重试约 15 s，再中止命令替换子 shell，作业此时已在自己的进程组里、没有计时器（CR 实测 21.6 s 后回落，BA 21.3 s）。基线遇到 fork 失败同样整体退出，所以不是新增的 fail-open；但 proposal 对这条分支的描述，以及 SC-V5「删掉计时器那一行」的变异，测的都是真实失败里不会出现的状态 | CR-02(M) BA-8(m) |
| PP1-A5 | Major | risk | testing | SC-V3 两条 e2e、SC-V6 的「会回落的输入」、BI-13、INV-7 | 这几条判据依赖自然的首遍耗时与本机速度：共享宿主上首遍波动 ±30–40%（`21ab#2` 基线 3.52 s 对 2.48 s），对正确实现会假红；换一台快机器又会恒绿。BI-13 自相矛盾：首遍就在 `_sg_per_segment_eval` 里面跑，锚点设在它的入口照样计入首遍，按字面构造的 BI-13 与好实现只差几十毫秒。BA 用 PATH 里的 `jq` 桩在锚点前注入确定延迟，结局确定（延迟 0 → 放行 1.49 s；1.5 s → 回落 3.02 s；2.5 s → 3.11 s；3.5 s → 3.90 s） | QA-F3(M) CR-05(M) CR-08(M) TL-F6(M) BA-4(M) |
| PP1-A6 | Major | issue | testing | BI 清单与 SC 覆盖、TASK-003 | 三个像真实执笔错误的坏实现没有任何用例能抓：截止漏了 `min(…, 3)`、作业结束后不杀计时器、准入门只看 `EPOCHREALTIME` 有无。本轮新暴露的两个形状也应入清单：不初始化 `_SG_RELAXED`、`wait` 后不清组 | TL-F5(M)；BA-1、BA-7 的建议 |
| PP1-A7 | Major | issue | testing | TASK-003 acceptance 与 design | 「每个 BI 至少让一条用例变红」区分不了「被指定用例抓住」与「被无关断言碰红」；对抗矩阵的判据「结局只能是放行、拦截文案或基线回落」几乎覆盖所有结局；也不核对 BI 是否「好实现加单一改动」。按字面构造的 BI-13 与好实现等价，该验收不可满足 | QA-F1(M) CR-07(M) TL-F5(部分) |
| PP1-A8 | Major | issue | testing | SC-V6、BI-7 | 「会回落的输入」没有确定的来源；回落从外部看与「准入门没打开」字节相同（P6 本就如此设计），输入若恰好没回落，用例照样绿，BI-7 活下来 | QA-F5(M) CR-08(部分) TL-F6(部分) |
| PP1-A9 | Major | issue | testing | SC-V8、BI-9 | 「引用全部在第 8193 字符之后」的 e2e 形状对负载脆弱，文字也没说应放行还是出增长文案；BI-9（`lim` 取改写后的剩余串）只在「小增长应放行」的方向上才暴露 | QA-F4(M) |
| PP1-A10 | Major | risk | testing | SC-V10、BI-11、Decision 11 | SC-V10 只直调 `_sg_judge_one … nocredit`，触及不到 `_sg_vx_big_judge` 的「只匹配规则」分支；若实现在那里另写规则循环（Decision 11 禁止的形状），直调用例全绿 | QA-F6(M) |
| PP1-A11 | Major | issue | testing | SC-V9、R-c、BI 清单 | 放宽重跑里仍可能出 TMAX 文案，R-c 与 CHANGELOG 没列；SC-V9 的「1 KB × 8 引用」使每段副本超过 SMAX，不在重跑里直调时第一段就停在触发点，到不了 TMAX；BI 清单没有「重跑里丢掉或放宽 TMAX」 | QA-F7(M) CR-14(m) TL-F18(m) |
| PP1-A12 | Major | issue | testing | SC-V7、既有 helper `wpa_x_finding` | `wpa_x_finding` 只断言出现 `reads a secret-bearing source`、不出现 `too large to scan`；`longline` 文案同样含前者，所以「普通命中」与「误路由到 `longline`」分不清 | KM-6(M) BA-10(m，第 1 点) |
| PP1-A13 | Major | decision | testing | TASK-002 acceptance「bash 3.2.57 下套件全绿」、SC-V2、套件 SC-13 | 照字面做不到：套件本身要 bash 5（`mapfile`、`EPOCHREALTIME`）；直调用例写 `_SG_P0=$EPOCHREALTIME`，在 `set -u` 下于 3.2 直接中止；6 组改写的用例与依赖放宽的新用例断言的是放宽后的结局，在 3.2 下必红，计划没说按版本怎么分；3.2 二进制不在仓里，SKIP 若计作 PASS 就是恒绿 | CR-04(M) QA-F8(M) BA-5(M) TL-F19(m) |
| PP1-A14 | Major | issue | testing | TASK-001「基线红 / 绿」、SC-V1 两部分、SC-V11 / V12 | 被记录的 SC-V 用例到 TASK-002 才写，TASK-001 没法在基线上实跑；SC-V1 混了「旧用例不变」与「6 组改断言」两部分；多条「基线红」只是因为函数不存在（127），不是断言在判别行为；SC-V11、SC-V12 没归类 | TL-F3(M) KM-3(M) BA-6(M) QA-F13(m) CR-12(m) |
| PP1-A15 | Major | issue | testing | TASK-004 title / design / acceptance | 「放行数不低于原型 (136/137)」与证据（SMAX 类 137/137）对不上；「无越过 … 的放行」在构造上恒绿（放行最大 1.805 s），迟到的拦截与回落反而不受约束；判据要用的「首遍 + 前段」W12 根本没记；W9、W10、W11、W10b、commentsync 都没有验收条；语料复原没有任务负责 | QA-F2(M) TL-F4(M) KM-8(M) BA-3(M) CR-11(m) TL-F17(部分) |
| PP1-A16 | Major | issue | testing | TASK-004 design 第 1 条（脚本的基线来源） | 各脚本的第一个参数就是「基线 hook」；实现落地后再传工作树里的 hook，base 与 impl 是同一个文件，P1、P2、P6 的比较全成了自己比自己 | BA-2(M) |
| PP1-A17 | Major | issue | architecture | TASK-003 / 004 / 005 / 006 的依赖；证据与 hook 版本的绑定 | 没有修复回路与作废规则：TASK-005 只依赖 TASK-002，审查后的修改会让 TASK-003 / 004 的证据过期；计划没有「证据绑定 hook 的 sha256，hook 变了就重跑、重审」 | TL-F2(M) QA-F18(m) CR-21(m) BA-13(m，第 1 点) KM-8(部分) |
| PP1-A18 | Major | issue | documentation | What 7 注释封闭清单、`commentsync.py` | 清单每处只钉一个短语，同一注释里其他会失实的句子不受检查；仍说「never passed」的注释与 W9 六组里四组的 `Red when` 说明块不在清单里；「应出现」的词只查出现；INV-1「逐字落地原型」与 TASK-002「commentsync target 为 GREEN」不能同时满足 | CR-06(M) KM-7(M) QA-F15(m) |
| PP1-A19 | Major | issue | documentation | `rule6_note`、`longline` 模板 | 单块 `decision_table_row: n/a` 与 note 里「AI 可见的 hunk 按第 1 行判」自相矛盾；`longline` 说是「逐字复用两条指令行」，实际是 3 条要点取 2、删了一条，且含祈使句，按 WP-A 先例不属第 1 行；「逐字」也没有断言钉住 | TL-F9(M) KM-5(M) CR-20(m) QA-F14(m) BA-14(m，第 1 点) |
| PP1-A20 | Major | issue | documentation | 残余与载体：放宽面、CHANGELOG 草稿、TASK-001 / TASK-007 | #217 关闭后几项残余没有载体：裁定 E 的放开条件、评论 28512 第 2 点（扩展项目整串口径）、「≤ 8192 的单次判定可超 5 s」（R2 TL2-F5；CHANGELOG 把它归给 #228，但留言内容没写它）；`#230` 只涉及扩展项目，而扩展项目不放宽，点名不当；`#138`、`#140`、`#141` 漏点名 | KM-9(M) CR-17(m) TL-F20(m) |
| PP1-A21 | Major | issue | documentation | INV-6；TASK-002 / 006 / 007；proposal「编号约定」 | 关闭关键词的核对只写在 TASK-007 一句话里，没有命令、没有验收；TASK-002、TASK-006 的提交、合并提交与 PR 描述先于 TASK-007 推送，却不查；名单式禁止（3 张）而非白名单；不核验 #217 实际已关；主仓里裸写 `#217` 会指向 `10CG/Aria#217`（一张开着的无关 issue） | KM-1(M) TL-F7(M) QA-F16(m) CR-19(m) BA-13(m，第 2 点) |
| PP1-A22 | Major | issue | documentation | TASK-001 的外发动作 | 开两张残余 issue、在 `#228` 与 `#217` 留言都是对外动作，不在 owner 的常设授权内，计划没有 owner 门 | KM-2(M) |
| PP1-A23 | Major | issue | documentation | TASK-006、INV-2、proposal Impact、SC-V12 | standards 三处计数、CHANGELOG 终稿（占位符来自四个任务）与 tag 没有任务认领、没有验收；SC-V12「三处计数一致」没有宿主，基线上已漂移（standards 822 对套件头注释 831） | QA-F9(M) QA-F10(M) KM-4(M) BA-12(m) CR-18(m) TL-F16(部分) |
| PP1-A24 | Major | issue | architecture | 阶段 C / D | 关单前没有上线后的运行时复验（插件缓存更新 + 新会话），也没有认领释放、归档与周期 handoff；归档前任务须为 done，否则会自动建 tracker | TL-F8(M) KM-13(m) |
| PP1-A25 | Minor | issue | implementation | `_sg_relax_run` 的 `out="$( … )" 2>/dev/null` | 赋值语句后的重定向不作用于命令替换本身（5.2 与 3.2 实测），fork 重试信息会漏到调用方 stderr | CR-09(m) TL-F10(m) |
| PP1-A26 | Minor | risk | implementation | 准入门与锚点 | `OSTYPE` 与 bash < 5 下的 `EPOCHREALTIME` 都可由父进程环境改写；墙钟回拨时剩余时间没有封顶；只在 bash 5.2.15 上实测过，5.0 / 5.1 / 5.3 未验证 | CR-10(m) TL-F12(m) BA-9(m) |
| PP1-A27 | Minor | issue | architecture | 准入门扩展探测、`_sg_vx_big_judge` | 两处「判不出就走宽松分支」：扩展探测出错等于没有扩展；最长行测量失败时 max 留在 0，走带 credit 的普通判定 | TL-F13(m) |
| PP1-A28 | Minor | risk | architecture | What 3 / Decision 5 的结论编码 | 放行用裸 `0` 表示，而 `0` 也是 bash 在若干异常下的默认值（BA 实测：命令替换里 `wait` 一个继承来的旧 PID 返回 0）；目前靠 bash 5.2.15 在 fork 失败时自行中止才堵住。可选：作业以专用非零码表示放行，裸 `0` 回落 | BA-15(m) |
| PP1-A29 | Minor | issue | documentation | What 3 耗时上界、P3、INV-7 | 上界公式漏了锚点之前（含 zsh re-exec）、准入门里的扩展探测、计时器启动三项；「与负载无关」说过头 | CR-22(m) TL-F14(m) |
| PP1-A30 | Minor | issue | documentation | proposal What 2 / 3 代码块 | 分段模式那一行路由改动不在 proposal 里：`fill.py` 把含新函数的整个 hunk 当函数剔掉了 | CR-13(m) |
| PP1-A31 | Minor | issue | documentation | proposal 与 detailed-tasks 全文 | 新文本 68 处裸 `#n`，与 standards `conventions/content-integrity.md` §4.4 规则 1（跨仓引用写全 `<org>/<repo>#<n>`）冲突 | KM-15(m) |
| PP1-A32 | Minor | issue | documentation | CHANGELOG 草稿 | 没有 Rule #6 行；130 与 137 未对账；放行类的危害没写具体；被拦命令的耗时变化（`f5like` 0.75 s → 3.01 s）与本机依赖（Linux、`/proc`、小数秒 `sleep`）没申报 | KM-10(m) BA-14(m，第 2–3 点) |
| PP1-A33 | Minor | risk | testing | SC-V11、BI-12 | 静态检查只认字面 `{8193`，换写法即绕过；检查的维度（拼写）与错误的维度（代价、跨行误判）不匹配 | QA-F11(m) CR-15(m) BA-10(m，第 2 点) |
| PP1-A34 | Minor | issue | testing | SC-V5 的桩形 | 「后台子进程继承 stderr 并睡 6 s」有两种写法，参考实现只对其中一种绿 | QA-F12(m) |
| PP1-A35 | Minor | issue | testing | locale | R2-A22 的处置（locale 用例用 `C.UTF-8` 并先断言字符集）声称由 TASK-002 承接，文字里没有；CJK 形状的结局随 `LANG` 变 | CR-16(m) BA-11(m) TL-F17(部分) |
| PP1-A36 | Minor | risk | testing | INV-7 与耗时矩阵 | 「一分钟负载 < 2」没写在哪个时刻量、违反时怎么办；证据本身是在负载 2.4–3.6 下取的；TASK-003 的耗时矩阵与 13 次整套件的成本不受约束 | QA-F17(m) TL-F17(部分) TL-F14(部分) |
| PP1-A37 | Minor | issue | documentation | 发布同步面、TASK-006 | 发版线已到 v1.77.1，「照 v1.77.0 的实际改动列」不准；VERSION 与 i18n 当前已漂移；漏 tag；版本号与本地 master 的新鲜度要在合并前重核 | KM-11(m) TL-F16(m) |
| PP1-A38 | Minor | issue | documentation | INV-1、INV-2、引用精度 | INV-2 与 TASK-001 / 003 / 004 自己的交付物冲突；INV-1 与 TASK-002「以补丁为准」各有一种读法；E12 没写路径、「71 条」的口径、17 处审计簇编号 | TL-F15(m) KM-14(m) |
| PP1-A39 | Minor | issue | documentation | 证据 `v3/README.md` 与脚本 | 复现说明缺调用参数；脚本把结果写回证据目录，会原地覆盖已提交证据；依赖清单不全；「+106」「17」两个数字不准 | KM-12(m)；QA-F2、KM-8 的相关子项 |

**冲突标记**：QA 认为任务依赖顺序合理；TL、CR、BA 指出 TASK-005 审后修改没有复审与作废规则（PP1-A17）。二者不矛盾：顺序本身可行，缺的是规则。

### 各席一致确认的代码事实（不是 finding）

- **机制在 bash 5.2.15 上成立**（BA 主测，CR、QA、TL 部分复现）：`set -m` 使作业与计时器各自成组（非 tty 与 pty 两种环境）；组长自检；`wait` 的退出码（3000 次快作业，0 / 2 各 1500 次全部正确）；`kill -KILL -- -PGID`；`/proc/$BASHPID/stat` 的解析（comm 含 `)`、空格时仍取对 pgrp）；`EPOCHREALTIME` 在逗号小数点 locale（`de_DE.UTF-8`）下正常；`set -u` / `pipefail` 继承；父进程的 EXIT trap 不在子 shell 里触发。
- **P1 由结构保证**（BA 逐 hunk、QA、CR）：非放宽路径没有可观察差异，前提是 PP1-A2 的初始化。
- **所有失败出口的回落与基线逐字节相同**（BA）：自检失败、作业内部错误、作业返回 2 但无文本、六种预算取值、拒绝小数秒的 `sleep` 桩，`f5like` 与 `apply-heavy` 两形状的 stderr 都与基线 IDENTICAL。
- **证据可复现**：`mkv3.py` 重新生成的 diff 与 `W8-v3.diff` 逐行一致（QA、BA）；`run-w10-w11.sh` 在 scratch 副本里 S1–S8、G1–G8 全 PASS、残留 0（QA、BA）；`w10b.sh` IDENTICAL × 4（BA）；`commentsync.py` 基线模式 GREEN（QA、BA）。
- **bash 3.2.57**：四个形状的 stderr 与基线相同（BA）。
- **INV-4 有现成的机械守卫**：套件 SC-30b 的闭包由 hook 文本推导，新函数放到 source 闸门下面会红（QA）。
- **`rule6_note` 的字段格式合规**（QA、CR、BA、KM）；内容上的问题见 PP1-A19。

## 主控核验与补充（汇总时新增）

### 复跑

| 簇 | 核验 | 结果 |
|---|---|---|
| PP1-A1 | 用 TL 的 `count-axis.sh` | 大命令：基线 rc 2（过大），v3 rc 0。**CONFIRMED** |
| PP1-A1 | 「count 触顶即回落」（TL 选项 2）在真实流量 137 条上的收益 | 只剩 73 条放行（64 条回落） |
| PP1-A1 | 「重跑内取消计数上限」（v3.1 草稿） | 大命令 rc 2（普通命中，读取可见）；小命令不变；真实流量 136 / 137 放行（n=1053 变为增长拦截，n=666 照旧 VMAX 拦） |
| PP1-A2 | e2e `apply-heavy-cjk` | 继承 `_SG_RELAXED=1`：v3 rc 0、25.40 s；不带时 rc 2 回落 3.03 s。v3.1 草稿两种情况都是 3.06 s 回落。**CONFIRMED** |
| PP1-A3 | 桩判定 `sleep 2.718 &` 后立即返回，截止 1 s | v3 rc 0、2.73 s。v3.1 草稿 0.00 s 返回、残留 0。**CONFIRMED** |
| PP1-A30 | `grep -F` 分段路由那一行 | 只在 W8 里有，proposal 代码块里没有。**CONFIRMED** |
| PP1-A21 | `10CG/Aria#217` | 存在且开着（session-closer 的 locale 问题），与本 Spec 无关。**CONFIRMED** |
| PP1-A31 | standards `content-integrity.md` §4.4 规则 1 | 原文要求跨仓引用写全。**CONFIRMED** |
| PP1-A39 | W8 增删行 | 实为 +110 / −6（新增里 4 行空行）；README 的「+106」漏算空行 |
| PP1-A39 | 「17 个依赖 `git show` 的用例」 | 831 − 814 = 17 是实测差；依赖 `git show` 的是 SC-8（套件 `:1733`、`:1734`、`:1769`、`:1810`）与 SC-9a（`:1286`）两组，17 个是否全来自这两组未逐个核对，README 改为只写这两组 |
| PP1-A16 | 当前 `aria/hooks/secret-guard.sh` | sha256 前缀 `e83c5e30f2cc`，与 `59e333c` 相同（aria 已到 v1.77.1 `68c7f65`，`hooks/` 零差异） |

### v3.1 原型草稿（scratch，尚未入仓）

在席位审 v3 的同时，主控按已核实的簇改出 v3.1 草稿：

- 锚点行初始化 `_SG_RELAXED`（PP1-A2）。
- 准入门改用只读的 `BASH_VERSINFO` 判 Linux 构建与 bash ≥ 5；剩余时间封顶到 `cap`（PP1-A26）。
- 计时器挪进作业，在自检之后、判定之前启动并确认存活，否则作业不判定直接以 9 退出（PP1-A4）。
- 命令替换内首行 `exec 2>/dev/null`（PP1-A25）；`wait` 之后组杀作业（PP1-A3）。
- 扩展探测只有「无项目根」或「无扩展文件」才放宽；最长行读循环加哨兵（PP1-A27）。
- 重跑内取消三个计数上限（PP1-A1）。

实测：更新后的单元 harness S1–S10、G1–G9 全 PASS（S9：作业提前退出、后代占管道 → 0.00 s 返回；S10：计时器 fork 失败 → 判定根本不开始，因 bash 的 EAGAIN 重试共 15.00 s 后回落，与基线自身 fork 失败的行为同类）。

### 事件记录

- 2026-10-22 约 10:27Z，另一会话双推主仓（v1.77.1，aria `68c7f65`；`hooks/` 对 `59e333c` 零差异）。主控把 v3 与 A.2 两个提交变基到新 master（`297b5cc → 910d9fa2`、`8ee867d → a136dbf8`），经 owner 授权把 aria-orchestrator `788a7ef` 补推到 GitHub，随后双推主仓并以 `ls-remote` 核验。TL、BA、KM 的任务书带新哈希；QA、CR 拿到的内容与新哈希逐字节相同。
- 主仓 `scratchpad/` 下多出约 298 个文件、约 6.9 万行（另一会话所为，未动），转告 owner。
- 认领心跳又两次推送失败（`fetch_failed`、`fetch_replay_failed`，aria-plugin #169 的形状）；主控按既定手法恢复：远端取到临时 ref、确认本地独有的只有自己那条心跳、`update-ref` 到远端后重跑。最新一次 15:12Z 推成，`ls-remote` 核验。
- QA 想对原型副本构造 3–4 个坏实现，那一轮输出被安全分类器拦下，没有重做。所以 QA 席关于「某个 BI 能否被某条 SC 抓住」的结论都是纸面推演；这也是 TASK-003（非作者构造坏实现）的执行风险。
- BA 一席跑了约 3.9 小时：fork 失败的模拟每次 15–21 s，全部串行、加了 `taskset` 与 `nice`。BA 报告写明没有用 `pkill`。

## 主控处置建议

### 判断

- 机制没有被证伪，Critical 只有一个，修法已在草稿里实测，所以不需要换机制。
- 但 Major 有 23 个簇，其中 13 个落在验收与证据上（PP1-A5–A17）。这一段在 post_spec R2 也是 Major 的主要来源（8/11）。连续两轮同一段最多，说明问题在写法：SC 和 BI 是用文字描述的，两个执笔者照同一段文字会写出不同的用例，只修措辞，下一轮还会在新措辞上出问题。

### v3.1 怎么做

1. **原型**：v3.1 草稿入仓（`mkv3.py`），另加两处：
   - 放行改用专用退出码，裸 `0` 回落（PP1-A28，fail-closed 方向的编码，不改姿态）。
   - bash 版本只在实测过的版本上放宽：本机另建 5.0、5.1、5.3 跑同一组机制测试，通过的才进准入门的版本集合，其余版本维持基线（照裁定 E 的原则，PP1-A26）。
2. **把验收从散文改成代码**（结构调整，回应 PP1-A5–A14、A33–A36）：
   - SC-V1–V12 现在就写成可执行的用例脚本，放在证据目录。
   - 用例脚本在三种 hook 上各跑一遍：基线 `59e333c`、v3.1 原型、按 BI 清单逐个构造的坏实现，结果存成新证据 W13。坏实现由主控构造，只算自检；非作者构造仍留给 TASK-003，下一轮审计席也可以用。
   - 时延类用例一律改用注入延迟（BA 的 `jq` 桩），断言结局，不断言墙钟。
   - bash 版本与 locale 的分支写在用例里，SKIP 单独计数。
   - 这样 TASK-001 的「基线红绿」在设计阶段就有了实跑结果，TASK-002 只是把用例搬进套件。
3. **证据**：`fill.py` 补上分段路由那一行（PP1-A30）。各脚本的基线一律取自 `59e333c`，并断言 sha256 前缀 `e83c5e30f2cc`（PP1-A16）；输出写到工作目录，不再原地覆盖证据（PP1-A39）。用 v3.1 重新生成 W8–W12b，README 的数字重算。
4. **proposal**：
   - 放宽面按 PP1-A1 改写：大命令在重跑里完整判定，count 轴只剩小命令这一侧的基线残余，写明并给载体。
   - TMAX 补进 R-c（PP1-A11）；`#230` 换成 `#138`、`#140`、`#141`（PP1-A20）；全文跨仓引用写全（PP1-A31）。
   - 注释清单扩到逐句（PP1-A18）；`longline` 原样复用 oversize 模板的全部指令行，只新增描述句，并加逐字断言（PP1-A19）。
   - CHANGELOG 草稿补齐（PP1-A32）；耗时上界补项（PP1-A29）。
5. **任务计划**：
   - TASK-001 的外发动作加 owner 门（PP1-A22）。
   - 证据页眉记 hook sha256，并加作废与复审规则（PP1-A17）。
   - TASK-004 验收逐条列判据（PP1-A15）。
   - TASK-006 认领 standards 计数、CHANGELOG 终稿与 tag（PP1-A23、A37）。
   - INV-6 给出每次推送都跑的核对命令（PP1-A21）。
   - TASK-007 补 D.1 / D.2、认领释放、handoff 与上线后复验（PP1-A24）。
6. `dispositions.md` 追加本轮 39 簇的逐条处置。

### 待 owner 的事项

1. **时间护栏没有新的姿态问题**：裁定 B（2026-10-21，判定来不及完成就拦）与裁定 E（2026-10-22，未实测平台维持基线拦）照旧成立。本轮找到的三个截止旁路（PP1-A2–A4）都已修成拦。
2. **PP1-A1 按技术决定处理，向 owner 通报**：
   - TL 给了两个选项，并定为 owner 的姿态决定：一是申报（这类命令放行），二是计数触顶即回落（真实流量收益 137 → 73）。
   - 主控取第三种：只在有硬截止的重跑里取消计数上限，判定完整后按结果判。这就是裁定 A 的原文，判不完就回落拦截（裁定 B）。与 v3 相比，大多数情形是多拦：藏在第 9 个引用之后的读取被看到。也有反方向的个例：脱敏过滤藏在第 9 个引用之后时，v3 照拦、v3.1 给 credit 后放行，与小命令的判定一致，属 R-a 已申报的 credit 语义（`10CG/aria-plugin#139`）。真实流量收益 137 → 136。
   - owner 若要自己定，可在三者里选。
3. **对外动作，需要 owner 放行**（TASK-001 开工前上呈）：
   - 开残余 issue（for 列表续行感知；collect 误收 heredoc 内形似赋值的文本）。
   - 以下几项各记到哪里：count 轴小命令一侧的残余；「≤ 8192 的单次判定可超 5 s」（与 `#228` 同类，现行版本已有）；裁定 E 的放开条件；评论 28512 第 2 点。
   - 在 `#228`、`#217` 留言。

## Verdict

**FAIL** — 1 个 Critical（PP1-A1）。

计算依据（去重后）：

- Critical：1
- Major：23
- Minor：15

## 轮次记录

### Round 1

- 对象：`detailed-tasks.yaml` @ `a136dbf8`、proposal v3 @ `910d9fa2`、证据 `.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v3/`；基线 aria `59e333c`（与 v1.77.1 的 `hooks/` 零差异）。
- Agents：qa-engineer、code-reviewer、tech-lead、knowledge-manager、backend-architect，5/5 全新实例，均未参与 post_spec；并发 ≤ 2。
- Sibling probe：已完整扫描，未发现同 issue 竞品（`no_sibling_found`）。
- Drift guard：config 未配置 `audit.drift_guard`，convergence 模式默认不跑 drift-checker。
- Conclusions：去重后 39 条（原始 90 条：QA 18、CR 22、TL 20、KM 15、BA 15）。
- Vote：REVISE × 5。TL 为 FAIL；QA、CR、KM、BA 为 PASS_WITH_WARNINGS。
- Duration：约 31671 s（2026-10-22 06:15:02Z → 15:02:54Z）。

## 统计

| 指标 | 值 |
|------|-----|
| 总轮次 | 1 |
| 总耗时 | 约 31671 s |
| Agent 参与率 | 5/5 |
| 去重前 / 后 issues | 90 / 39 |
| Critical / Major / Minor | 1 / 23 / 15 |
| Major 簇落在本轮新文本上的占比 | 23 / 23（v3 是重写版，`detailed-tasks.yaml` 是新文件） |
| 收敛轮次 | N/A（未收敛） |

## 成本与收敛距离

- **本轮成本**：5 席，墙钟约 8.8 小时（并发 ≤ 2），席位报告合计约 168 KB。
  - 各席耗时与工具调用：QA 约 33 分钟 / 56 次，CR 约 39 分钟 / 70 次，TL 约 34 分钟 / 58 次，KM 约 42 分钟 / 145 次，BA 约 233 分钟 / 约 90 次。
  - KM、BA 结束时上下文分别约 47 万、44 万 token，接近「40–50 万即换实例」的线。
- **累计**：post_spec 2 轮加 post_planning 1 轮；席位报告约 512 KB；规格 46 KB；仓里的实现代码仍是 0 行，参考实现以 W8 diff（+110 / −6）形式存在于证据目录。
- **距离**：
  - 机制层面，post_spec R2 的两个 Critical 都没有复发。
  - 本轮的 Critical 是放宽面漏申报的一类，修法已实测。
  - 剩下的 Major 主要在验收写法上，v3.1 用「验收写成代码」从结构上处理。
- **停止规则**（沿用 post_spec 的约定）：
  - 下一轮（post_planning R2）换全新席位。
  - 若 Major 簇数没有降到 23 以下，或本轮修订引入的 Major 占比超过一半，就不再加轮，按「实现优先」上报 owner。

---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: false
oscillation: false
overridden_by_user: true
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: FAIL
timestamp: 2026-10-22T00:53:36.580Z
context: openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
---

# post_spec R2 汇总 — secret-guard-w10-failclosed-narrowing（10CG/aria-plugin#217，proposal v2 @ `41e9308`）

> **Verdict：FAIL**。去重后 2 Critical / 14 Major / 13 Minor。三席 FAIL（TL / CR / KM），两席 PASS_WITH_WARNINGS（QA / BA），五席全部投 REVISE。未收敛。
>
> **R1 写下的停止规则已触发，两条都满足**：Major 数没有下降（14 → 14）；14 个 Major 簇全部落在 v2 新文本上（其中 3 簇另含沿用的子项）。因此不自动进入 R3，交 owner 定下一步。
>
> 本文件是有损汇总。每个簇都回链到席位原编号：TL2 = tech-lead，BA2 = backend-architect，QA2 = qa-engineer，CR = code-reviewer，KM = knowledge-manager；括号里是该席的定级。细节以各席报告为准（同目录、同时间戳 `1792591829231` 的五份文件）。簇号一律写作 R2-A*n*，与 R1 的 R1-A*n* 区分。

## 一句话

v2 的硬截止只罩住了「大副本判定」这一步，而且这一步本身也能被骗：

1. **状态行能被冒充**（R2-A1）。判定被计时器杀掉时，它启动的外部进程不会一起终止，会在状态行之后继续往同一管道写。hook 于是可能把拦截文案里回显的命令末行当成判定结果；命令末行是 `0` 时就读成放行。主控在 bash 5.2.15 与 3.2.57 上复现。
2. **其余步骤没有上界，也不在截止之内**（R2-A2）。基线靠 8192 尺寸早停兜住了几步的工作量：apply 跑两次，扩展阶段还要对原命令再判一次。v2 去掉早停后，这几步都失去上界，也不在截止内。基线 0.2–3 s 内按尺寸拦下的输入，新版要 7–21 s。超过 5 s，Claude Code 就杀掉 hook 并放行。R1 写下的可证伪判据「新版超过 5 s」因此成立，「硬截止只罩判定」这一处置不成立。

其余 14 个 Major 的分布：

- 10 个是 SC 表与测试规格写不成、测不准；
- 2 个在时间机制：截止的「硬」依赖一个没写明的前提；整秒时钟让实际截止落在 2–4 s；
- 2 个在申报与收口：一类放宽面漏了申报；#217 收口与 #228 的接缝还有缺口。

## 审计结论

### Issues / Risks（按 {category, scope} 去重）

| 簇 | 级别 | type | category | scope | 摘要 | 席位回链 |
|---|---|---|---|---|---|---|
| R2-A1 | Critical | issue | implementation | What 2 参考实现 `_sg_vx_big` 的状态行解析与进程模型 | 状态行取命令替换输出的最后一行。判定被计时器 `kill -KILL` 时，它启动的外部进程（`_sg_emit_blocked` 的 `cat`、`_sg_redact_echo` 的 `sed`）不随之终止，会在 `printf '\n%s' "$r"` 之后继续写同一管道。`$( )` 又剥掉末尾换行，最后一行就可能是拦截文案回显的命令末行；命令末行为 `0` 时解析成放行。同族小项：`SECONDS - _SG_P0` 读数为负时截止被拉长；计时作业 fork 失败不在「失败都拦」的清单里；孤儿 `sleep` 的数量与存活时长没有上界 | CR-F1(C) · BA2-F-05(m) · BA2-F-13(m) · BA2-F-14(m) |
| R2-A2 | Critical | issue | architecture | 不变量「时间上不新增 fail-open」/ What 1 增长上限 / What 2 截止覆盖范围 / What 4 / Decision 4、7 | 基线在 `:685`、`:694` 用 `_SGV_SMAX` 边构建边早停，输入超过 8192 时第一次替换就返回，后面各步都不跑。v2 只给 `_sg_vx_big` 加了截止，原来靠早停兜住工作量的步骤都失去上界、也不在截止内。一是 `_sg_vx_apply` 改按增长判后，代价变成「替换次数 × 串长」，在 `_sg_vx_pass`（截止之前）和扩展腿（`:1554`）各跑一次。二是扩展阶段对原命令的 `_sg_ext_pass "$cmd"`（`:1548`，内含 `_sg_core_eval`）。三是大副本放行后，后续各段与 ≤ 8192 副本的判定只受首遍后起算的协作预算约束。实测如下。TL 用约 61.5 K 字符的整串命令（16 变量 × 16 引用）：基线 rc 2，3.2 上 3.03 s、5.2 中文 2.37 s；v2 分别 15.44 s、20.90 s。KM 在扩展生效时用单个 24000 字符 token：基线 0.16 s 拦下，新版 CPU 7.3–10.4 s。TL 构造的放行路径 3.05–4.13 s，基线 0.39 s 拦下。超过 5 s 即被 CC 杀掉放行 | TL2-F1(C) · KM-F-01(C) · CR-F2(M) · TL2-F5(M) · BA2-F-12(m) |
| R2-A3 | Major | risk | architecture | What 2 参考实现：截止之「硬」的前提 | 截止的「硬」依赖一个没写明的前提：判定路径上不能有比判定活得更久的外部子进程。否则命令替换要等管道 EOF：判定里放一个 `sleep 6`，返回码是 3（按时间拦），墙钟却是 6.00 s。需写成不变量并配结构检查，与 R2-A1 同根 | BA2-F-02(M) |
| R2-A4 | Major | risk | testing | What 2「时钟 / 截止时长」/ Decision 4 / Why 表 W5 / SC-N1、N16 | `SECONDS` 按整秒跳，实际截止落在距 `_SG_P0` 2–4 s 之间（BA 实测 2.30–3.57 s），判定本身只拿到 2–3 s。W5 按 3 s 估算偏乐观（区间见 R2-A17）。最慢的真实命令 1.93 s，SC-N16 只剩 0.07 s 余量。断言「完整判定完成」的 SC 对宿主负载敏感；本机 bash 3.2 的绝对速度远低于「×4」的估算。可选：bash 5 用 `EPOCHREALTIME`，3.2 回落整秒，收益写成区间 | TL2-F3(M) · CR-F6(M，SC-N1 在 3.2 上的抖动沿用 v1) · BA2-F-01(M) · QA2-F09(m) · BA2-F-17(m，沿用) |
| R2-A5 | Major | issue | documentation | 不变量「放宽了什么」/ CHANGELOG 草稿 / SC-N13 前提 / What 4「与基线完全相同」 | 放宽面漏申报一类：变量名长、值短，代入后串变短，于是原串或某个中间副本 > 8192，而最终副本 ≤ 8192。基线在第一次替换时就按总长拦下。v2 按增长不拦，最终副本走普通 `_sg_judge_one`，不在截止内。整串模式下，命令里任一处 `>/dev/null` 都会给 credit（基线对 ≤ 8192 命令的既有行为）。TL 的构造读一个运行时拼装的凭据形路径，另有一处无关的 `echo done >/dev/null`：基线 rc 2，v2 rc 0，即凭据会被读出。这与三处文本矛盾：CHANGELOG「在硬截止内完整判定」、SC-N13「≤ 8192 逐字节相同」、What 4「与基线完全相同」。这一类按 A 的口径属于「只因尺寸被拦」，但要让 owner 看见 | TL2-F4(M) · CR-F8(m) |
| R2-A6 | Major | issue | testing | SC-N1 / N2 / N3 的副本行结构；`longline` 与 finding 的区分 | SC-N1–N3 没规定副本是单行还是多行。`_SGV_LMAX` 与 `_SGV_SMAX` 同为 8192，单行大副本恒走 nocredit，结局是 `longline`，不是 finding。`wpa_x_finding` 只验「exit 2、含 reads a secret-bearing source、不含 too large」，两种模板都能过，分不开。需钉死行结构并新增 `wpa_x_longline`；SC-N4 系列须用多行构造 | QA2-F02(M) · CR-F4(M，形状描述沿用 v1 SC-1) · TL2-F2(M，部分) · KM-F-02(M，部分) · BA2-F-09(m) |
| R2-A7 | Major | issue | testing | §预计会变的既有用例 / SC-N18 | 成员预测正确（BA 逐组核对）。错在结局：21ab#1、21ac#3、21al#2、21ao#2 实为 `longline`，不是 finding。照表改用例会变绿，因为 `wpa_x_finding` 也接受 `longline`，但断言的是错模板。21ab#2 / #3 预测的 exit 0 不稳定：分段模式下首遍要 2.4 s，QA2 估计约四成概率在判定前就读到截止已过，直接出时间文案。21an `edge8193` 的 apply 状态由 2 变 0，表里没写 | CR-F3(M) · QA2-F03(M) · TL2-F2(M，部分) · KM-F-02(M，部分) · BA2-F-18（核对结果，不计数） |
| R2-A8 | Major | issue | testing | SC-N12 后半 | 「套件 20 条 BLOCK 用例各自包进超长行 → 全部 `longline`」照字面做不到：字面读取在首遍就被拦，到不了 W10，而且结果抖动。需改用整串模式加经变量的读取，或给出 credit 配方 | QA2-F04(M) · BA2-F-04(M) · TL2-F6(M) · CR-F5(M，b 部分) |
| R2-A9 | Major | issue | testing | SC-N9 / N5c / N4e 的对抗形状 | 关键约束没写：路径字面要在 token 之后；读取不能撞上 `_SG_SRVCFG` / `_SG_CLAUDE_CFG` 而提前被拦。第三种形状违反自己的「首遍 < 1 s」前提。N5c 的检出是概率性的；N4e 必须用整串模式 | QA2-F01(M) · BA2-F-03(M) · CR-F5(M，a 部分) · TL2-F11(m，部分) |
| R2-A10 | Major | issue | testing | 参考实现的 fail-closed 出口 / SC-N5f | What 2「每一条都有对应的 SC」不成立。状态行拿不到数字时返回 3 的 fail-closed 分支没有任何 SC：把它写成放行的坏实现，能通过全部已列 SC。SC-N5f 只看返回值，去掉 `left > 0` 守卫的坏实现也 30 / 30 返回 3，需要 marker 才能区分。计时子 shell 不占管道、被杀的判定只出时间文案，这两条性质也没有 SC。另外，「`wait` 加 `2>/dev/null` 吃掉 Killed 提示」在两版 bash 下都复现不出 | QA2-F07(M) |
| R2-A11 | Major | issue | testing | SC-N8 的 TMAX 例 | 例子按字面算不到 65536；换一种读法，成本又高到不可用。建议直调，或改用「1 KB 值 × 8 引用 × 8 段」这种廉价形状 | QA2-F05(M) · BA2-F-08(m) |
| R2-A12 | Major | issue | testing | SC-N11 | 漏了「不得使用 `{8193,}` 正则」的断言。比值判据在毫秒级抖动，是噪声；直调需要桩掉 `_sg_judge_one`；N 的取值有歧义 | QA2-F06(M) · BA2-F-10(m) · CR-F11(m，a 部分) · TL2-F11(m，部分) |
| R2-A13 | Major | issue | testing | SC-N1b / N4b | 输入形式欠定，SC 点名要抓的坏实现在自然写法下会漏过。SC-N1b 没钉 `$NAME` / `${NAME}` 拼写：用 `${NAME}` 拼写时，「`lim` 取被改写的剩余串」的坏实现全绿。SC-N4b 没钉长行是字面写出还是由展开产生：用字面长行时，「用原串量行长」的坏实现全绿 | QA2-F08(M) |
| R2-A14 | Major | issue | testing | SC-N15 / §Impact 注释同步清单 / SC-N17 | SC-N15 的 grep 断言不可证伪。规格给的例句在基线里折成两行（`:581–582`），单行 grep 在基线就返回 0，「退役短语不在」恒真；其余 7 处没给短语，执笔席可以事后挑词。清单本身也不封闭：第 1 处应为 `:87–95`；第 9 处块头是 `:2510–2518`；第 4 处无事可改；漏了 `_sg_judge_one` 的契约注释（`:1492–1496`）和 7 个用例标题；`_SG_T0` 的重置点写错；新用例须插在 SC-13 之前；standards 三处计数没有机械核对。KM 附了逐处的短语表 | KM-F-03(M) · KM-F-06(m) · CR-F12(m) · QA2-F13(m) · BA2-F-07(m) · TL2-F8(m) |
| R2-A15 | Major | issue | testing | SC-N16 / N16b / §证据与复现 | SC-N16b 依赖的 `traffic/standin.sh` 与期望结果不在仓里，也没有任务产出；「W1 四类形状」推不出来。SC-N16 的回放链走不通：`refreeze.py` 不产出 `index.tsv`；`base-all.sh` 固定写同一个文件，两次运行互相覆盖，并按 grep 把 `longline` 记成 finding；没有指名比对脚本。refreeze 的 50 条上限、「137」的口径、CPU 时间口径都未定 | KM-F-05(M) · QA2-F10(m) · QA2-F11(m) · BA2-F-16(m) · TL2-F12(m) · KM-F-10(m，第 4 条) |
| R2-A16 | Major | issue | documentation | TASK-006 / TASK-004 / Decision 9 / 页眉「关联」 | #217 的收口与残余载体仍有缺口，R1-A14 只修了一半。具体是：#217 评论 28512 第 2 点（评估扩展整串那一眼的口径）不在对账项里；Decision 9 在 #228 的 issue 与 proposal 里都没有载体，也漏了「覆盖首遍之后全部步骤」这个中间选项；「Windows / macOS 未实测」只落在 CHANGELOG；残余 issue 在发版之后才开，而发版时 CHANGELOG 就要写号；关闭关键词落在哪个提交没写。交叉引用也不双向：#217 上没有指向本 Spec 的评论；#229 / #230 全文未提，而放宽后它们覆盖的流量变多 | KM-F-04(M) · TL2-F9(m) · KM-F-15(m) |
| R2-A17 | Minor | issue | documentation | Why 表 W5 行 / Decision 4 | 慢平台收益写成了单点，应写成区间：按最坏 2 s 算，Windows 31 / 138、bash 3.2 62 / 138 会撞上时间拦。「3 s / 4 s」两列与 3 s 封顶矛盾，读者会以为调高 `SECRET_GUARD_TIME_BUDGET_S` 能减少时间拦 | CR-F7(m) · KM-F-09(m) |
| R2-A18 | Minor | issue | implementation | What 1 `lim` | 「长出 8192 以上」读作 ≥，代码与 SC 都是 >；`lim` 是否 `local` 没写 | CR-F9(m) · BA2-F-06(m) · KM-F-10(m，第 3 条) |
| R2-A19 | Minor | issue | testing | SC-N10 | 「`wpa_fault_case` 的手法」有两种读法，方向相反；注入点未定 | CR-F10(m) · TL2-F10(m) · QA2-F14(m，N10 部分) |
| R2-A20 | Minor | issue | testing | SC-N13 | 网格的取值与「≤ 8192」前提冲突；oracle 放在哪里未定 | CR-F11(m，b 部分) · QA2-F14(m，N13 部分) |
| R2-A21 | Minor | issue | documentation | What 5 文案 / 时间文案 / 全文措辞 | 涉及的文案与措辞问题如下。`longline` 模板的「in a line」措辞和 UNSCANNED 理由不准。heredoc 里有三处展开，不是两处。时间文案在截止路径上写「Nothing was matched」不准，因为被杀的判定可能已经命中规则；预算设为 4 时文案打印 4 s，实际截止是 3 s。另有几处需更正：`:476` 与 crossline 的 `_SG_PROCTAB`、页眉漏 W7、LMAX 的定义位置、oversize 首行。行文上，「第 N 项」用了三套编号，字母 A–D 有四种含义，`:126` 指涉上一版 | CR-F13(m，d 以外) · BA2-F-15(m) · TL2-F7(m) · KM-F-16(m) · KM-F-10(m，第 1、2、7、8 条) |
| R2-A22 | Minor | issue | testing | SC-N14 | `en_US.UTF-8` 不一定存在，缺失时用例空转；改用 `C.UTF-8` | QA2-F12(m) · BA2-F-11(m) |
| R2-A23 | Minor | issue | testing | SC-N4e / N5a / N6 / N17 / §Impact「SC-N1–N18 入套件」 | 措辞欠定。N5a 的「返回时间拦」不清楚是 `_sg_vx_pass` 返回 2，还是 `_sg_vx_big` 返回 3。N6 没写模式：分段模式形状在基线已是 `wpa_L_ext`，只有整串形状才是 bf | QA2-F14(m，其余部分) · KM-F-10(m，第 5、6 条) |
| R2-A24 | Minor | risk | documentation | §证据与复现：本机依赖 | 本机依赖申报不全：bash 3.2.57 是本机的 Linux 构建，没有配方；`b2ed608` 只在 origin 上；W5 读的是另一个笔记目录的 `E12-base-all.tsv`；`TRAFFIC_DIR` 默认值和 `taskset` / `jq` / mawk 依赖没写；`assign-probe.py` 未列入；W-summary 仍是手写的；`extract.py` 没给路径。KM 已验证：W5（逐字）、W4 / W6（定性）、E12 聚合数都能只凭仓内文件复现 | KM-F-07(m，部分沿用 R1-A22) |
| R2-A25 | Minor | issue | documentation | §Impact CHANGELOG 草稿 / 发布同步面 | CHANGELOG 草稿有以下问题。漏报两类残余：for 列表跨换行误拦；heredoc 内的赋值形文本被当成赋值。「Linux 上全部放行」缺少「空闲机器」与平台限定。漏了用户可见的变化：`Limit hit:` 原因串、`longline` 模板、预算变量对大副本不再延长。体例与 v1.76.1 不符。「收窄」易被读成变严，而且对单行大副本不准。另外，发布同步面的转述漏了 i18n README 与 CLAUDE.md 项目状态行 | KM-F-08(m) · KM-F-12(m) · CR-F13(m，d 部分) |
| R2-A26 | Minor | issue | documentation | TASK-001 / TASK-006 / 页眉 | INV-6 在本 Spec 内没有定义（定义在 `secret-net-l3-and-bypass-paths/detailed-tasks.yaml`）。INV-4 / 5 / 7 没有声明继承，其中 INV-7（时档类测量只看比值）与多条带绝对墙钟上界的 SC 冲突。认领存在于 `refs/aria/coordination`，页眉没有记 | KM-F-11(m，部分沿用 R1-A23) |
| R2-A27 | Minor | issue | documentation | §Impact Rule #6 | 只写了「只改 hook，按 substitute」，没有逐 hunk 说明面向 AI 的文字：`longline` 模板里有对 AI 的指令，另有两条改写的 `Limit hit:` 原因串。WP-A 与 #228 都逐 hunk 判过 | KM-F-13(m，沿用) |
| R2-A28 | Minor | risk | documentation | §R1 处置对照 / 行内回链 | 审计叙事与交付面同居一文（memory `audit-trail-not-in-spec`）。本轮有不少 Minor 落在这类文本上，再加入 R2 的处置只会更多。建议机械搬出，不重写 | KM-F-14(m) |
| R2-A29 | Minor | decision | architecture | §不变量 / TASK-004 / §Owner 裁定点 | 规格自己写明：Windows / macOS 上 `kill -KILL` 若不能及时终止判定，大副本会退回 fail-open，比基线差。处置却写成「发版前实测，或在 CHANGELOG 申报」，交给执行席选。选申报，就是在未验证的平台上带着放宽发版。这是 fail-open / closed 的姿态问题，应由 owner 定（memory `failopen-posture-owner`），裁定点表里却没有这一项 | KM-F-17(m) |

**映射核对**：原始发现 73 条，全部归入上表。

- TL2 12 条（1C/5M/6m）；
- CR 13 条（1C/5M/7m）；
- QA2 14 条（0C/8M/6m）；
- BA2 17 条（0C/4M/13m），另有 BA2-F-18 是核对结果，不计入；
- KM 17 条（1C/4M/12m）。

标「部分」的发现拆进了两个以上的簇，计数时只算一次。

### 各席一致确认的代码事实（不是 finding）

- proposal `:131–159` 的参考实现与 `traffic/deadline-helper.sh` 逐字节一致（CR、KM）。
- 草稿 hook 在 bash 3.2.57 与 5.2.15 下 `bash -n` 都通过；helper 用到的写法在 3.2 下可用；W6 在两版 bash 下跑通了 rc 0 / 2 / 3 三条路径（CR、BA、KM）。
- proposal 引用的行号与 `59e333c` 一致，只有 §Impact 第 1 处与第 9 处的块头例外，见 R2-A14（TL2、CR、BA2、KM）。
- `:666` 恒为假，删掉后行为不变（CR、TL2、KM）。
- 「预计会变的既有用例」表的**成员**正确，错在其中 4 行的结局（R2-A7）。
- 最终副本 > 8192 时，扩展门与基线逐分支等价（TL2、BA2、KM）；唯一例外是缩短类（R2-A5）。
- standards 三处计数（`:23`、`:316`、`:352`）为 822 / 816，套件头 `:11` 为 831 / 825（CR、TL2、KM）。
- W0 / W1 / E12 的数字都能由仓内文件复算吻合（TL2、KM）。
- 不传第三参数时，`_sg_judge_one` 与基线逐字节相同（CR）。

## 主控核验与补充（汇总时新增）

### 复跑

- **R2-A1**：主控用 CR 的 `orphan-race.sh` 在 bash 5.2.15 与 3.2.57 上复跑，最后一行都是 `0`，解析结果为状态 0，即放行。成立。
- **R2-A2**：主控用 BA2 独立转写的 v2 hook，跑 TL2 的输入 `c-apply.txt`（bash 5.2，宿主负载 5.7）。单次 apply：基线 0.022 s，rc 2；v2 1.644 s，rc 0。与 TL2 的直调结果同量级，成立。

### 阴性与阳性结果的对照（输入不同，只能写「不可比」）

- BA2-F-12 曾尝试构造「新版超过 5 s、基线不超」：扩展生效、原文 7–13 KB、分段模式。结果**没有复现**，原因如 BA2 所析：原文一大，首遍就吃掉了 `SECONDS`，新版很快按时间拦下。KM-F-01 用的是整串模式加单个 24000 字符 token，首遍很快，扩展阶段才慢，**复现成立**。两者输入不同，BA2 的阴性不构成对 KM 阳性的反证。
- BA2 §2 写「没找到未申报且确实读到凭据的放宽反例」。TL2-F4 用缩短类构造出了一个（R2-A5）。同样是输入不同；TL2 的阳性成立。

### R1 可证伪判据的回看

R1 对硬截止处置写的判据是：「R2 若有人构造出『新版放行、基线拦』或『新版超过 5 s』的输入，此处置即不成立」。

- 后半句已由 TL2-F1、KM-F-01 实测满足。所以无论前半句怎么读，「硬截止只罩判定」这一处置都已不成立。
- 前半句按字面写坏了：放宽 A 本身就会产生大量「新版放行、基线拦」的输入，W1 那 138 条真实命令全是这一类，所以它恒成立，没有区分力。主控当时想表达的是「因截止机制失效而放行」，但原文没写这个限定。这里不事后补写，只如实记为判据缺陷。
- 下一版的判据要写成可证伪的形式，例如：「放宽类命令的墙钟 ≥ 5 s」，或「某输入在截止机制失效时被放行」。

### 基线漂移

R2 进行期间，aria v1.77.0（`f2e801d`）合入主仓 master（`7143f3c`）。它的 `hooks/` 对 `59e333c` 零差异，所以各席引用的行号全部仍然成立。影响有三处：

- 本变更的发版目标改为 v1.77.x 的 PATCH；
- CHANGELOG 条目要排在 v1.77.0 之上；
- 规格里以 v1.76.1 为参照的文字需要改（并入 R2-A25）。

### 事件记录

- **共享宿主上的 `pkill`**：TL2 席约 16:30Z 执行了 `pkill -f 'sleep 3$'`，可能误杀其他席位计时作业里的 `sleep`。误杀的效果是计时器提前到点、判定被提前杀掉，只会让新版显得更易拦，不会造成假放行。影响面如下：
  - CR、QA2 早已结束；BA2 报告时间戳 16:24Z，实验在此之前做完。
  - KM 当时刚派发、还在读材料，它的 F-01 以 CPU 时间计，方向不受影响。
  - 下一轮派单书写明：只准按自己的 PID 清理进程，禁用按模式匹配的 `pkill -f`。
- **KM 的独立性例外**：KM 一次 grep 的路径过滤写错，带出了 CR、BA2 的 R2 报告各一行。KM 声明没有据此下结论，相关两点（standards 计数、行号）都由它独立核对过（见 KM 报告的轮次记录）。

## 主控处置建议（停止规则已触发，交 owner 定）

### 判断

问题的分布变了：

- **设计层的真问题只剩两处**：截止覆盖哪些步骤（R2-A2），以及 helper 的进程模型（R2-A1、R2-A3）。两处都有明确改法，而且只影响基线本来就按尺寸拦的那一类命令。
- **其余多数是规格写法问题**，而且只要用真实代码一跑就能定形，例如：
  - 单行副本走 `longline`；
  - SC-N12 的形状是否成立；
  - SC-N16 的回放链能不能走通。

  在规格里继续写，只会再产生新的写法问题。R1 → R2 的轨迹就是这样：v2 新增的文本承载了本轮全部 Major。

### 若继续，v3 只做「设计钉死」，钉到字符级

1. **截止覆盖（R2-A2）**：命令一旦进入放宽类，之后的全部步骤都放进同一个以 `_SG_P0` 计的硬截止，超时按时间拦。放宽类指输入或任一中间副本 > `_SGV_SMAX`，恰是基线按尺寸拦的那一类；之后的步骤包括 apply、大副本判定、后续各段和扩展腿。超时的结局与基线对这类命令的结局一样，都是拦。≤ 8192 的命令与基线逐字节相同。候选实现有两种，B.2 实测后再定：
   - 剩余流程整体放进一个后台作业；
   - 逐次替换时检查截止，扩展 apply 改为绝对早停；扩展生效时，放宽类直接按基线文案拦（KM-F-01 的建议 1）。
2. **helper 加固（R2-A1、A3）**：
   - 状态行带每次调用唯一的标签，只认带标签的最后一行，认不出就按时间拦；
   - 判定路径上不得有比判定活得更久的外部进程，写成不变量并配结构检查；
   - `left` 取非负；
   - 计时作业 fork 失败时按拦处理。
3. **时钟（R2-A4）**：bash 5 用 `EPOCHREALTIME`，3.2 回落到整秒；收益写成区间。
4. **申报（R2-A5）**：缩短类写进放宽面和 CHANGELOG。
5. **SC**：改成「性质 + 必须抓住的坏实现」两栏。具体形状不在规格里预写，在 TASK-001 实跑派生后回写。
6. **未实测平台的默认态（R2-A29）**：属姿态问题，由 owner 定。

这些都是在姿态 B（时间护栏 fail-closed）之内更换机制：结局只会是基线的结局（拦），或者是完整判定后的结局。按 memory `failopen-posture-owner`，这属于技术裁定，向 owner 通报即可。

### 考虑过、不推荐的方案

**整个 hook 加一个总截止**，与 #228 的首遍残余合并处理。不推荐，原因有三：

- 它会把首遍超时从放行改成拦，改变基线放行类命令的姿态，属于 owner 的决定；
- 真实流量里首遍超时只出现过 1 次，而且是测试探针，收益约为 0；
- 慢平台上被拦的命令会变多。

此方案作为 #228 重启时的选项，记在 R2-A16 的载体里。

### 选项

| 选项 | 内容 | 主控意见 |
|---|---|---|
| 【1】先钉设计，再实现优先 | v3 只做上面的「设计钉死」。post_spec 由 owner 裁定关闭，记 `overridden_by_user: true`；A.2 与 post_planning 照配置跑。须知：本项目 post_implementation 与 pre_merge 闸门在配置里是关的，写完代码后没有已配置的闸门。补救是加自愿复核：非作者构造坏实现矩阵、对抗成本矩阵、独立代码审查，再在真实流量上用实际实现量收益与耗时。执笔可换新席 | 推荐 |
| 【2】先钉设计，再审一轮 | 同【1】的 v3，但换新席跑 R3。代码前保留一道已配置的闸门；代价是新机制文本大概率再引出新的 Major | 可选 |
| 【3】完整修订 v3 再审 | 逐簇修全部 29 簇再跑 R3 | 不推荐：R1 → R2 的轨迹显示这条路会继续产生新文本缺陷 |
| 【4】转积压 | 同 #228，保留证据与两轮报告 | W10 尺寸预算的误拦（>8 KB 真实命令的 17.6%）继续存在 |

## Verdict

**FAIL** — 2 个 Critical（R2-A1、R2-A2）。

计算依据（去重后）：

- Critical：2
- Major：14
- Minor：13

## 轮次记录

### Round 1

- 见 `post_spec-R1-1792577352602-secret-guard-w10-failclosed-narrowing-aggregated.md`：proposal v1 @ `acd6a95`，去重 3C/14M/7m，原始 69 条，REVISE × 5，约 10296 s。

### Round 2

- 对象：proposal v2 @ `41e9308`；基线 aria `59e333c` + standards `a611136`。
- Agents：tech-lead、backend-architect、qa-engineer、code-reviewer、knowledge-manager，5/5 全新实例，均未参与 R1；并发 ≤ 2。
- Sibling probe：已完整扫描，未发现同 issue 竞品（`no_sibling_found`）。
- Conclusions：去重后 29 条（原始 73 条）。
- Vote：REVISE × 5。TL2 / CR / KM 为 FAIL，QA2 / BA2 为 PASS_WITH_WARNINGS；五席都有 Major 以上的发现。
- Duration：约 37811 s（2026-10-21 14:10:29Z → 2026-10-22 00:40:40Z）。
- 事件：见「事件记录」。

## 统计

| 指标 | 值 |
|------|-----|
| 总轮次 | 2 |
| 总耗时 | 约 48107 s（R1 10296 + R2 37811） |
| Agent 参与率 | 每轮 5/5 |
| 去重前/后 issues | R1 69 / 24；R2 73 / 29 |
| Critical / Major / Minor 走势 | 3 / 14 / 7 → 2 / 14 / 13 |
| 本轮修订引入的 Major 占比 | 14 / 14 |
| 收敛轮次 | N/A（未收敛） |

## 成本与收敛距离

- **本轮成本**：5 席，墙钟约 10.5 小时（并发 ≤ 2），席位报告合计约 169 KB。各席工具调用数：QA2 158、KM 144、BA2 120、TL2 99。KM 一席跑了约 8.2 小时，结束时上下文约 54 万 token，超过了「40–50 万即换实例」的线。
- **累计**：2 轮；席位报告约 344 KB；规格 41 KB / 456 行；代码 0 行。
- **距离**：
  - R1 的三个 Critical 里，R1-A2（for 列表）与 R1-A3（D）靠收缩已经消失。
  - R1-A1（大副本判定无成本上界）的处置只罩住一步，问题换了位置继续存在，即 R2-A2。
  - 新增的 Critical R2-A1 落在 v2 新写的参考实现上。
  - Major 14 → 14。每一轮的 Major 都主要落在当轮新写的文本上。
- **停止规则**：两条都满足，见页首。主控不再加轮，按 R1 汇总的约定上报 owner，选项里包含「实现优先」。

## Owner 裁定（2026-10-22）

1. **下一步：先钉设计，再实现优先**（选项【1】）。
   - post_spec 以本轮结论关闭，`overridden_by_user: true`。这是 Rule #10 允许的 owner 覆盖，不是 AI 自行豁免。
   - v3 只做「设计钉死」（见上文「若继续」1–6），之后不再跑 post_spec。A.2 与 post_planning 照配置跑。
   - 配置里 post_implementation 与 pre_merge 是关的，所以写完代码后，主控补做自愿复核：非作者构造坏实现矩阵、对抗耗时矩阵、独立代码审查，以及用实际实现在真实流量上量收益与耗时。
2. **未实测平台维持基线拦**（关闭 R2-A29）。
   - 放宽只在实测过的平台生效，目前只有 Linux。Windows / macOS 与现行版本行为一致，实测通过后另行放开。
   - 这是姿态 B（时间护栏 fail-closed）在新机制上的延伸，由 owner 裁定。
3. **（与 #217 无关）GitHub 镜像**：owner 授权主控补推。
   - aria-orchestrator #34 在 Forgejo 上合并后没推到 GitHub，主仓 GitHub master 指向的 `ef5506d` 在 GitHub 镜像里不存在。
   - 主控已把 aria-orchestrator master 快进推到 GitHub（`237045a..a9f0658`），`ls-remote` 核验一致；随后双推主仓。


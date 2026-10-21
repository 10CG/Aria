---
checkpoint: post_spec
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
timestamp: 2026-10-21T13:22:01.564Z
context: openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
---

# post_spec R1 汇总 — secret-guard-w10-failclosed-narrowing（10CG/aria-plugin#217，proposal v1 @ `acd6a95`）

> **Verdict：FAIL**。去重后 3 Critical / 14 Major / 7 Minor；五席全部 FAIL，全部投 REVISE。未收敛，进入 R2。
>
> 本文件是有损汇总。每个簇都回链到席位原编号：TL = tech-lead，BA = backend-architect，QA = qa-engineer，CR = code-reviewer，KM = knowledge-manager；括号里是该席的定级。细节以各席报告为准（同目录、同时间戳 `1792577352602` 的五份文件）。

## 一句话

v1 的四处改动里有三处照写会让基线拦下的输入变成放行：

1. A 的大副本完整判定没有总成本上界，会超时放行。
2. D 的「只拦被引用值」认不全引用形式。
3. 第 4 项「for 列表止于换行」会截断续行列表。

这三处都至少有两席在 bash 3.2.57 与 5.2.15 上实测复现。其余问题集中在 SC 可测性、拦截文案、同步面和 issue 收口。

## 审计结论

### Issues / Risks（按 {category, scope} 去重）

| 簇 | 级别 | type | category | scope | 摘要 | 席位回链 |
|---|---|---|---|---|---|---|
| R1-A1 | Critical | issue | architecture | §What 2 大副本判定 / §不变量 / SC-9 判据 3 | 大副本完整判定没有总成本上界。credit 成本由三项组成：行数 × 0.5–0.9 ms（14 个过滤器逐行求值）、逐 token 的平方项、`_SG_PS_REMOTE_T` 的跨行项；LMAX 只封住单个 token。5 行 × 8000 字符的 40 KB 副本，新版 5.4–6.3 s，超过 5 s 被放行；基线 0.6–1.6 s 内按尺寸拦。B 护栏只看判定**前**的耗时，在 5.2 上 6 次 0 次拦住。「不新增 fail-open 路径」不成立 | TL-F1(C) · QA-F1(C) · KM-F-01(C) · BA-F-01(C) · CR-M1(M) |
| R1-A2 | Critical | issue | implementation | §What 4 for 列表止于换行 / SC-7 | 字符类加入换行会截断反斜杠续行的列表，续行里的读取从「拦」变成「放」，3.2.57 与 5.2.15 均复现。另有编码陷阱：ERE 方括号里写 `\n` 不是换行 | TL-F2(C) · QA-F2(C) · KM-F-02(C) · BA-F-03(C) · CR-m3(m) |
| R1-A3 | Critical | issue | implementation | §What 3 只拦被引用值（D）/ §不变量 / 姿态 D 立论 | 「被引用」只认 `$NAME` / `${NAME}` 子串，比 shell 的实际展开窄，也比 `_sg_vx_apply` 的实际代入窄。漏掉的形式：`${NAME:-x}` 一类（apply 不代入，运行时会展开）；`eval $P $B$C` 拼接（apply 链式代入后得到 `$A`）；`${!NAME}` 等。值超过 4096 时，基线按 VMAX 拦，新版放行，而且真的会读到凭据。链式溢出（`:668-669`）的处理未定；「去掉这条赋值本身」有两种读法 | CR-C1(C) · BA-F-02(C) · TL-F4(M) · QA-F3(M) · CR-m1(m) |
| R1-A4 | Major | issue | architecture | §What 5 扩展整串检查 / SC-8 / `:1553-1566` | 扩展检查与 W10 共用 `_sg_vx_apply`。apply 改成按增长判之后，原串大、增长小的副本在扩展里不再按尺寸拦，而是重跑 `_sg_core_eval`：10–16 KB 要 6.7–17 s（仅 5.2 实测）。「维持原口径」因此无法达成，需要独立的绝对尺寸门；SC-8 区分不了好坏实现 | TL-F3(M) · QA-F9(M) · CR-M2(M) · BA-F-04(M) |
| R1-A5 | Major | issue | implementation | §What 2 步骤 2 最长行测量 | 没有指定算法。参数展开剥离法在 3.2 上处理 64 KB、1000 行要 22.5 s；正则 `{8193,}` 要 12–14 s，且 `RE_DUP_MAX` 不可移植。只有单遍 `read` 循环合格 | BA-F-05(M) |
| R1-A6 | Major | issue | architecture | §What 2 步骤 3 只匹配规则路径 / §Impact | 只匹配规则这条路径必须复用 W12 中和，否则裸规则循环会误拦 `os.environ` 下标读取（5.2 实测）。而 `_sg_environ_neutral` 只存在于已搁置的分支 `b2ed608`。实现归属与被改函数清单缺失；中和失败得到空串时会放行 | BA-F-06(M) · KM-F-08(M) · QA-F14(m) |
| R1-A7 | Major | issue | testing | §What 2.3 拦截文案 / SC-2..SC-4 | 沿用 oversize 模板会打印「Nothing was matched」，与「命中了凭据形读取」自相矛盾。增长、超长单行、时间三类原因串都没有钉死字面值，按文案区分的 SC 无从比对 | QA-F10(M) · KM-F-10(M) · TL-F9(m) · BA-F-06(部分) · QA-F12(部分) |
| R1-A8 | Major | risk | testing | §What 2.1 时间护栏 / SC-5 / Decision 3 | `SECONDS*2>=budget` 在整秒粒度下是 1–2 s 的爬坡，不是「一半」。`SECONDS` 可从环境导入；套件 source hook 时，绝对 `SECONDS` 会误触发。SC-5 直接赋值会在秒边界漂移，helper 也没有名字。建议：`_SG_P0` 锚 + 具名 helper + 走子进程 | BA-F-07(M) · QA-F4(M) · TL-F8(m) · CR-m2(m) · QA-F12(m) |
| R1-A9 | Major | risk | testing | SC-9 真实流量回放 | 语料已无法同批重取：重抽得到 2426/745，不是 2412/739；`/tmp` 易失。判据 2 把 time 和超长单行当成功，恒绿；判据 3 在良性语料上恒绿；还允许 `oversize→finding`。语料里看不到对抗形状；3.2 上 time 占比估计 7–14%；第三方无从复核 | QA-F5(M) · KM-F-07(M) · BA-F-08(M) · TL-F11(m) · CR-m5(m) |
| R1-A10 | Major | issue | testing | SC-1..SC-8 可测性 | 形状没有钉死。SC-1 在 3.2 上抖动，按总长判或按可变剩余串判的坏实现都能通过。SC-6/SC-7 的自然写法在基线上就是绿的（没写明 bf 前提）。SC-8 区分不了好坏实现。缺 credit 正证与正向对照、边界对、`Limit hit:` 字面值 | TL-F5(M) · QA-F6(M) · QA-F7(M) · BA-F-09(M) |
| R1-A11 | Major | issue | testing | SC 清单（缺失项） | 缺 14 类 SC：分段模式孪生、TMAX、扩展、GMAX/LMAX 双边缘、分流常量、护栏范围、故障注入、最长行线性、多长行/多短行/包装词密集的对抗成本、续行 for、构造引用、差分 | QA-F8(M) · KM-F-04(部分) · BA-F-09(部分) · CR-M1(部分) |
| R1-A12 | Major | risk | testing | SC-10 / SC-11 / 既有 W10 用例 | SC-11 写了「逐条列出」却没有列。读码推演会变的既有用例：21ab、21ac 第 3 条、21ad 第 2 条、21ag、21aj、21al、21an、21ao，可能还有 21ap，以及 `wpa_L_*` 字面值（未实跑）。差分没有定义「判定」的口径；SC-10 的 3.2 实跑与 9.7 KB 形状冲突 | TL-F6(M) · QA-F11(M) · KM-F-04(M) · BA-F-10(M) |
| R1-A13 | Major | issue | documentation | §Impact 同步面 | 描述旧语义的 hook 注释有 9 处，规格只列了 1 处（其中包括文件头 Residual gaps 与 `_sg_emit_blocked`），另有测试注释。standards 计数在 `secret-hygiene.md` 有三处（`:23`、`:316`、`:352`），现值已陈旧（822/816，套件头是 831/825），还缺版本行 | KM-F-03(M) · KM-F-11(m) · TL-F12(m) · QA-F13(m) · BA-F-14(m) · CR-m6(m) |
| R1-A14 | Major | issue | documentation | §Impact / §Tasks / Decision 6（#217 收口） | 没写 #217 怎么收口、用什么关闭关键词、INV-6 怎么核对。issue 的 6 项诉求有 2 项被推迟却没有载体，而 aria-plugin#201 的归档机制会吞掉 Level 2 正文里的推迟项 | KM-F-05(M) |
| R1-A15 | Major | issue | documentation | §Impact CHANGELOG 申报 | 「C 项与扩展口径的如实申报」有三种读法（姿态 C / #216 的 C / 阶段 C）；残余清单不全，放行面扩大没有申报 | KM-F-06(M) |
| R1-A16 | Major | issue | documentation | §不变量与范围外 / 姿态表 | 不变量段与全文矛盾或说得过强：A/D 本身就是放宽；「三种原因」漏了尺寸类；扩展口径对启用了扩展的采用方反而更严；理由只对子集成立。大副本里任一处无关的 `>/dev/null` 就会给整份副本 credit，这是 A 的固有含义，但没写出来 | KM-F-09(M) · BA-F-15(m) |
| R1-A17 | Major | decision | architecture | R1-A1 的处置 | BA 认为 A1 不能单靠技术收口，需要 owner 三选一：(a) 加成本门（封不住包装词密集的文本）；(b) 先做 #228 的 credit 根治；(c) 明确申报残余 | BA-F-11(M) |
| R1-A18 | Minor | issue | documentation | §Why「8192 原本要防什么」（`:476` 的理由） | 「它的通配段不跨空白」不准确：`_SG_PROCTAB` 的 `[^|;&]*` 包含空白和换行，阻止跨行匹配的是后面的 `[[:blank:]]`。**conflicted**：CR 实测 40 KB 匹配 <0.03 s，认为「便宜、有界」；BA 用包装词密集的文本（1000 行 × `watch …`，24 KB）测得 `_SG_PS_REMOTE_T` 单独就要 2.07–2.97 s。两边输入不同，BA 的反例成立，结论应改为「一般文本便宜，包装词密集的文本昂贵」 | TL-F7(m) · CR-m4(m) · BA-F-01 证据 1 |
| R1-A19 | Minor | issue | implementation | §What 1 增长上限的实现细节 | `lim` 必须在入口用 `${#1}` 一次算出，因为循环里 `s` 会被改写；「增长」指任一中间副本；TMAX 仍按完整长度累计，「同一口径」说过头了 | BA-F-12(m) · TL-F10(m) |
| R1-A20 | Minor | issue | documentation | 全文措辞 | 歧义清单（KM 17 条、BA 7 条），例如「字符类加入换行」「一半预算」「去掉这条赋值本身」「300 个引用」「维持原口径」 | KM-F-15(m) · BA-F-13(m) |
| R1-A21 | Minor | risk | documentation | §What 1 / 2「字符」口径 | `${#s}` 按字符还是按字节随 locale 变，规格没有申报；多字节命令在 C locale 下会被分到超长单行分支 | QA-F16(m) |
| R1-A22 | Minor | issue | documentation | 证据包 `.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/` | W-summary 没有生成脚本；`NEUT_SRC` 未钉；计时用的是墙钟；默认目录在 `/tmp`；「不入库」的理由与可验证范围未写。W3 用 awk `length`，与 `${#l}` 单位不同；`judge_s` 不含 collect、首遍与 B 护栏；慢平台外推是借来的，没有为 #217 重测 | KM-F-12(m) · BA-F-16(m) |
| R1-A23 | Minor | issue | documentation | 页眉 / §Tasks / 全文引用 | `detailed-tasks.yaml` 悬空；没有 `rule6_note`；基线冻结只含 aria；INV 没有继承；SC 编号与套件里既有的 SC 撞号；8 处裸 `#n`；与 #228 缺互链，也缺互相更正 | QA-F15(m) · KM-F-13(m) · KM-F-14(m) · BA-F-14(部分) |
| R1-A24 | Minor | risk | documentation | §Why / SC-9 / CHANGELOG（A 的收益） | A 的收益依赖平台：bash 3.2 上 6 次有 4 次被护栏拦下；「138 降到 0」只在本机 bash 5.2 上成立，需要限定措辞 | QA-F17(m) |

**映射核对**：原始发现 69 条，全部归入上表。TL 12 条（2C/4M/6m）、QA 17 条（2C/9M/6m）、CR 9 条（1C/2M/6m）、KM 15 条（2C/8M/5m）、BA 16 条（3C/8M/5m）；CR-D1 是核实留痕，不计入。

### 各席一致确认的代码事实（不是 finding）

- SMAX 数的是总长（`:694`）。
- VMAX 超限立即返回 2，不看是否被引用（`:645`）。
- `_SG_T0` 在首遍之后才重置。
- `SECONDS` 从进程启动开始计，hook 里没有给它赋值。
- 扩展检查会重跑 `_sg_core_eval`（`:814`）。
- oversize 和 timeout 的文案都是「Nothing was matched」（`:836`、`:855`）。
- `:666` 的死代码判断正确：条件恒假。
- W1–W3 的数字与 proposal 一致。

## 主控补充证据（汇总时新增，回应 R1-A1 / R1-A17）

BA 的三个选项都以「无法从技术上收口」为前提。汇总时，主控实测了第四条路：给大副本判定加一个硬截止。

做法：判定放到后台子 shell 里跑；另起一个计时子 shell，到点 `kill -KILL`；父进程 `wait` 等结果，返回码 ≥128 就按时间拦。

- **W4**（`evidence/W4-watchdog.txt`，由 `traffic/watchdog-probe.sh` 生成）：
  - bash 5.2.15 与真 bash 3.2.57 都通过。
  - 一长串小步骤，以及单次 3 s 的长正则（hook 自己的 `_SG_SRVCFG`，16000 字符 token），都在 2.00 s 被掐断。
  - 不超时时，返回码和拦截文案照常透传。
  - 每次开销约 1 ms。
  - 计时进程不占管道：管道 2–4 ms 内就到 EOF。
  - `wait` 加 `2>/dev/null` 后，shell 的 `Killed` 提示不会混进拦截文案。
  - **未核实**：Windows MINGW64、真 macOS。
- **W5**（`evidence/W5-deadline.txt`，由 `traffic/deadline-estimate.sh` 生成）：
  - 基线按尺寸拦下的 138 条真实命令，新版改成完整判定后，首遍加判定在 Linux 上最长 1.93 s。
  - 截止点设 3 s / 4 s 时，会撞点的条数：Linux 0 / 0；Windows（×2.6）8 / 3；bash 3.2（×4）35 / 17。倍率是粗估。
  - 这些命令基线本来就拦，所以硬截止不会比基线多拦任何一条。

## 主控处置（v2 方向，交 R2 审）

| 簇 | v2 处置 |
|---|---|
| A1 / A17 | 大副本判定（最长行测量 + 两条分支）整体放进硬截止，超时就拦。截止以 hook 启动时的锚 `_SG_P0` 计，用 `SECONDS - _SG_P0`，不受环境导入影响。这是 owner 已裁定的 B（时间护栏 fail-closed）的实现方式变化：从「判定前看表」改成「判定中掐表」，姿态不变，结局与基线一样是拦，不新增放行。Why 的成本模型按 BA-F-01 建议 1 重写。新增对抗 SC（k × 8000 字符 token、2000 短行、包装词密集三种形状），断言按时间拦且墙钟 < 5 s。**可证伪判据**：R2 若有人构造出「新版放行、基线拦」或「新版超过 5 s」的输入，此处置即不成立 |
| A2 | 撤下第 4 项。W1 显示真实流量 0 例，收益为零、风险 Critical。转为推迟项，按 A14 给载体 |
| A3 | D 改为保守版本：(1) 超大值不丢弃，留「墓碑」，`_sg_vx_apply` 代入时碰到墓碑就拦，覆盖链式和 `$B$C` 拼接；(2) 文本里出现 `${NAME` 加任意后续字符也算引用；(3) 出现任一间接构造（`eval`、`${!`、`declare/local/typeset -n` 等），所有超大值一律按被引用处理，与基线一样拦。补构造引用 SC |
| A4 | 扩展整串检查前加独立的绝对门：`${#_SG_SUB}` 超过 `_SGV_SMAX` 就拦，文案不变，不再借用 apply 的 rc=2 判尺寸。SC-8 改为「原串大、增长小，且启用扩展」 |
| A5 | 最长行测量钉死为单遍 `while IFS= read -r` 循环，放在硬截止内 |
| A6 | 把 `_sg_environ_neutral` 从 `b2ed608` 移植进 #217，连同它的单测，列入被改函数清单。中和失败得到空串时拦 |
| A7 | 新增三类原因串并钉死字面值：增长超限、超长单行命中规则、大副本判定超时。不再借用「Nothing was matched」 |
| A8 | `_SG_P0` 锚 + 具名 helper。SC-5 在子进程里用 `SECRET_GUARD_TIME_BUDGET_S` 加一个假的慢判定来测，不直接给 `SECONDS` 赋值 |
| A9 | SC-9 改为单机验收，写明复现边界：冻结语料清单（命令哈希 + 抽取参数）入库；判据按 W1 期望逐类钉死，`oversize→finding` 必须为 0，time 单列；另配合成替身语料，供第三方复跑 |
| A10–A12 | 采用 QA 附录 C 的 SC 清单；SC 换一个不与套件撞号的命名空间；列出要改的既有用例，B.2 实跑核对 |
| A13 | 同步面逐处列出：9 处 hook 注释、测试注释、standards 三处计数、版本行 |
| A14 | 推迟项（含撤下的第 4 项）开独立 issue 承载；#217 的关闭关键词与 INV-6 核对写进 Tasks |
| A15 / A16 | 重写不变量段和 CHANGELOG 申报：A/D 明写为放宽，逐条列出新的放行面（未被引用的超大值；大副本按整份 credit 判）和残余 |
| A18–A24 | 逐条改措辞、单位、证据包和引用 |

**对 BA-F-11 的处置**：硬截止让 A1 有了技术收口，而且不改姿态，所以主控按技术裁定采用，并向 owner 通报，不请求新的裁定（memory `failopen-posture-owner`：变的是机制，不是 fail-open/closed 姿态）。如果硬截止在 Windows 或 macOS 上实测不可靠，就退回 BA 的 (a)(b)(c)，届时再上呈 owner。

## Verdict

**FAIL** — 3 个 Critical（R1-A1、R1-A2、R1-A3）。

计算依据（去重后）：

- Critical：3
- Major：14
- Minor：7

## 轮次记录

### Round 1
- Agents：tech-lead、backend-architect、qa-engineer、code-reviewer、knowledge-manager（5/5，并发 ≤ 2）
- Sibling probe：已完整扫描，未发现同 issue 竞品（`no_sibling_found`）
- Conclusions：24（去重后；原始 69）
- Vote：REVISE × 5
- Duration：约 10296 s（2026-10-21 10:09:12Z → 13:00:48Z）

## 统计

| 指标 | 值 |
|------|-----|
| 总轮次 | 1 |
| 总耗时 | 约 10296 s |
| Agent 参与率 | 5/5 |
| 去重前/后 issues | 69 / 24 |
| 收敛轮次 | N/A（未收敛） |

## 成本与收敛距离

- **本轮成本**：5 席，墙钟约 2.9 小时，席位报告合计约 180 KB。
- **距离**：3 个 Critical 都已有具体处置。两个靠收缩：撤下第 4 项、D 改保守；一个靠已经实测过的机制：硬截止。但 v2 会带进新文本（硬截止、墓碑、扩展门、三类文案、新 SC 清单），按以往经验，R2 的 Major 多数会落在这些新文本上。
- **停止规则**：R2 若出现以下任一情况，就不再加轮，而是上报 owner，选项里包含「实现优先」（先写代码，用对抗形状实测，再回头收规格）：
  - 本轮修订引入的 Major 占比超过一半（memory `marginal-return-negative`）；
  - Major 数不降（memory `no-ruling-shortens`）。

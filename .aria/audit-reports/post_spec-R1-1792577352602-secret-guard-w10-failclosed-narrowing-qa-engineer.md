---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-10-21T10:58:30.000Z
context: openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R1 -- qa-engineer 席位报告 (#217 secret-guard-w10-failclosed-narrowing)

被审对象: `openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md` (主仓 `acd6a95`, 工作树与提交一致)。基线: aria v1.76.1 (`59e333c`)。
侧重: 可测性。姿态 A/B/C/D 为 owner 已裁, 本报告不重议; 凡报告的 fail-open 均指「在该姿态内未申报的新路径」。

## 审计结论

**一句话**: 方向可测, 但按现稿实现会出 2 处 Critical (大副本「全量判定」的成本上界不成立; for 列表止于换行会放过续行列表), 且 SC-5 / SC-9 写不出或写出来恒绿, SC-1..SC-4 区分不了几类像真的坏实现。以下每条都带可复跑的实验证据。

**方法与口径**:

- 读码 + 在 scratch 副本上**仿真提案的行为**, 不改仓库。`mkpatched.py` 生成 `hook-prop.sh` (增长上限 + `SECONDS*2` 护栏 + for 列表加换行 + 朴素 D), 另生成 7 个「坏实现」变体; 用真 bash 5.2.15 与真 bash 3.2.57 (`/home/dev/.aria/tools/bash-3.2.57/bash`) 实跑。
- 仿真**没有实现分支 3 (只匹配规则)**; 凡涉及分支 3 的结局, 报告写明「推断」。
- 全部实验前缀 `taskset -c 0,1 nice -n 19`; 宿主共享、负载 1.3–4.7, 绝对秒数只作量级参考。
- 实验脚本与产物在 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217audit/qa-engineer/` (会话级临时目录; 关键数字已抄进下文)。

### 发现总表

| 序号 | severity | category | scope | 一句话 |
|---|---|---|---|---|
| F1 | Critical | implementation | Why「8192 原本要防什么」/ What 2 / Decision #3 | credit 成本被判为「只跟单行长度有关」, 实测对多条长行求和; 全量判定的副本总量无上界, 时间护栏在判定前看不见, 会让基线能拦的输入超过 CC 的 5 s 而 fail-open |
| F2 | Critical | implementation | What 4 / SC-7 | for 列表字符类加换行会截断 `\`+换行续行的列表, 基线拦的续行读取被放过 (新 fail-open) |
| F3 | Major | implementation | What 3 / 不变量 / SC-6 | 「被引用」判据只认 `$NAME` `${NAME}`, `${NAME:-}` 一类引用被当作未引用; 链式溢出 (`:668-669`) 未定; 「不新增 fail-open」一句不成立 |
| F4 | Major | testing | SC-5 | 时间护栏单测按现稿写不出 (helper 无名, `_SG_T0` 状态未定, 边界抖动); 给出已验证的确定性方案 |
| F5 | Major | testing | SC-9 | 判据 2 把 time/超长单行当成功吸收 (恒绿), 判据 3 在良性语料上恒绿, 语料已不可复现 |
| F6 | Major | testing | SC-1..SC-4 | 形状未钉死: 总长型 / 可变剩余串型坏实现通过 SC-1, SC-1 在 bash 3.2 上抖动, 缺「短行大副本含 credit → 放行」正向对照 |
| F7 | Major | testing | SC-6 / SC-7 | 「bf」前提未写明 (入口门要有 `$`; 循环体前 4096 字符不得含 `;&\|)`), 否则在基线是绿的; 缺正向对照 |
| F8 | Major | testing | SC 清单 | 缺 14 类 SC (分段模式、TMAX、扩展、边界、分流常量、护栏范围、故障注入、最长行线性、成本上界、差分等) |
| F9 | Major | implementation | What 5 / SC-8 | 扩展整串检查与 `_sg_vx_apply` 共用, 朴素改法静默放宽扩展口径 (已实证 rc=0); 机制未定、文案未钉 |
| F10 | Major | testing | SC-3 / SC-4 | 增长与超长单行的原因串未给出 (语言未定), 且「Nothing was matched」模板与分支 3 的事实矛盾 |
| F11 | Major | testing | SC-10 / SC-11 / Impact | 差分未定义「判定」口径, 被点名要变的现有用例未列; SC-10 的 bash 3.2 实跑与 9.7 KB 形状冲突; 同步面少列 |
| F12 | Minor | documentation | What 2.1 | 「用掉一半预算」不准: `SECONDS` 整秒粒度下默认预算 3 s 在约 1.0–2.0 s 触发; 文案是「未在预算内完成」而事实是预先拦截 |
| F13 | Minor | documentation | 不变量 / Impact | 头注释同步点列少 (至少 6 处), standards 计数在 3 处不是 1 处; 死代码同形兄弟未扫 |
| F14 | Minor | implementation | What 2.3 | 「W12 中和」没说是抽取还是复制; 中和失败得空串即放行的 fail-open 陷阱 |
| F15 | Minor | documentation | 全文 | `detailed-tasks.yaml` 被引用但不存在; SC 编号与套件内既有 SC 撞号 |
| F16 | Minor | documentation | What 1 / 2 | 「字符」口径随 locale 变 (`${#s}`), 未申报; 多字节命令在 C locale 下被分到超长单行分支 |
| F17 | Minor | risk | Why / SC-9 / CHANGELOG | A 的收益依赖平台: bash 3.2 实测 6 次里 4 次被护栏拦, 「138 降到 0」只在本机 bash 5.2 成立, 需限定措辞 |

---

### F1 [Critical] 大副本全量判定无总量上界: credit 成本跨行求和, 时间护栏判定前看不见

- type: issue
- severity: Critical
- category: implementation
- scope: proposal Why「8192 原本要防什么」第一条与「因此真正要防的, 是构造出来的超长单行」; What 2 (分流 2); 实现约束「逐行计算 credit 的成本因此有上界」; Decision record #3; `secret-guard.sh:476` `:728` `:748`
- 摘要: 提案把 credit 成本归结为「只跟单行长度有关, 不跟总长」, 并据此用 LMAX=8192 分流。实测不成立: `:476` 的整段 tight 检测对副本里**每个**长路径形 token 各付一份二次成本, 总成本对行数求和。由于副本总量只受 `${#S}+8192` 与 64 KB 命令上限 (`:1157`) 约束, 构造「K 行、每行 <=8192」的副本能让第二遍跑 7 s 以上; 时间护栏在判定**前**只看到首遍的 0.7–0.9 s (SECONDS<=1), 不触发, CC 在 5 s 杀掉 hook 后 fail-open。基线对同一输入 0.7–0.9 s 返回 oversize 拦截。
- 证据:
  1. 代码: tight 检测是整段多行串上的两次 `[[ =~ ]]` (`:476`: `$_SG_CLAUDE_CFG|$_SG_SRVCFG` 与 `$_SG_PROCTAB_ALL`)。`_SG_PROCTAB` 里有 `(/[^[:space:]|;&"'`$()<>]*/)?` 与 `([^|;&]*[[:blank:]])?`, 后者的负向字符类**跨空白也跨换行**, 所以提案括号里「通配段不跨空白, 成本受单个 token 长度约束」对 `_SG_PROCTAB_ALL` 不成立; 即便对 `_SG_SRVCFG` 成立, 「每个 token 有界」也推不出「总成本有界」。
  2. xtrace 定位 (`credit-prof.sh`): 6 行×8000 字符的副本上, `_sg_compute_credit` 的 8.26 s 间隔整段落在 `:476` 这一行, 其余每步 <=0.04 s。
  3. 叠加性 (`credit-sum.sh`, R 形 = 读取 + 长 `/tmp/aaa…` token): K=1/2/3 行 (每行 8000) 的 `_sg_judge_one` 耗时 1.22/1.96/2.77 s; 固定总量约 48 KB, 行长 1000/2000/4000/8000 耗时 1.85/2.25/3.82/6.85 s。粗拟合 cost ≈ 24 us/字符 x N + 15 ns x Σ(行长^2) (4 个点, 共享宿主, 跨平台系数**未核实**)。单行 16 KB / 24 KB 分别 4.70 / 10.12 s (印证原头注释的二次增长)。
  4. 端到端 PoC (`gen.py viavar_env 6 8000` + `e2e.sh`): `f=/opt/.env; (true); cat $f` 后接 6 行 `echo /tmp/aaaa…(8000 字符)`, 共 48,121 字节, 每行 8006 字符 (<= LMAX, 走分流 2)。
     - 基线 v1.76.1: rc=2 oversize, 0.67 / 0.91 s。
     - 仿真提案 (`hook-prop.sh`): 7.12 / 7.47 s。`timeout 5` 模拟 CC: 基线 rc=2 (0.73 s); 仿真 rc=124 (5.00 s 被杀, 无判定 => CC fail-open)。
     - bash 3.2.57, K=2 (16 KB): 基线 0.50 s, 仿真 2.51 s。
  5. 取决于凭据族: `tight=0` 的族 (aws 凭据文件、`.env`) 所有 credit 检查都跑; app.ini 族 (`tight=1`, 跳过多数检查) 同形状仅 1.16 s (`viavar_ai 6 8000`)。所以不是所有族都能打。
  6. 时间护栏的立论失效: Decision #3「第二遍判大副本的成本约等于首遍」在此形状上差 7 倍以上, 因为 credit 只在**第二遍**命中规则后才计算 (首遍的原串里读取被变量藏住)。
  7. 既有同形缺口 (校准用): 字面读取 + 同样填充, 基线 `gen.py literal 6 8000` = 7.67 s (即 #228 的首遍问题)。所以在 #228 未修时, 攻击者的边际能力 = 「变量间接」这条新增路线与字面路线等价; #228 线性化之后, 这条路线会独立存在。主控可据此调级, 但规格的两条明文断言 (「不新增 fail-open 路径」「逐行计算 credit 的成本因此有上界」) 在现稿下都不成立。
- 建议改法:
  1. 把分流 2 (全量判定, 含 credit) 的准入条件从「最长行 <= LMAX」改为对**总量**设界, 且线性可算。例如同时要求 `${#copy} <= FMAX` 与 `Σ(行长^2) <= QMAX`, 否则走分流 3 (只匹配规则, 命中即拦)。真实数据余量: 31 条靠 credit 放行的副本 N <= 28,240、N x 最长行 <= 4.07e7 (W2 与 W3 联表, 最大一条 19,018 x 2,139), 小于 8192^2 = 6.7e7, 所以取 `QMAX = LMAX^2` 不会重新误拦。FMAX 的取值取决于 owner 对慢平台的姿态 (拟合下 N=32 KB 的线性项约 0.8 s, Windows x2.6 约 2 s), 需在规格里写成数字并说明依据。
  2. 删改 Why 节的结论句, 改述为「单个 token 二次、跨 token 求和; 副本里长 token 的总质量才是成本」; 删去「逐行计算 credit 的成本因此有上界」。
  3. 时间护栏保留 (姿态 B), 但不要再声称它能挡住第二遍的成本: 它只能挡「首遍已慢」的输入。
  4. 加 SC (见 F8 的 COST 两条): 确定性的入口量标记 + 对抗形状的时延上界。

### F2 [Critical] for 列表字符类加换行会截断续行列表, 基线拦的读取被放过

- type: issue
- severity: Critical
- category: implementation
- scope: proposal What 4; SC-7; `secret-guard.sh:654` (`rf`)
- 摘要: 提案只说「列表部分 `([^;&|)]*)` 的字符类加入换行」。bash 里一个 for 列表跨行的**唯一合法写法**是 `\`+换行续行; 单纯在字符类里加换行会把续行列表截成第一行, 后面几行的条目不再代入。基线对此类命令恰好是拦的 (整段列表被当作一个值), 新版放行, 而命令真实读取了该文件。SC-7 的两行 (多行循环体 / 单行长列表) 都不覆盖, 现有套件里 for 用例全是单行 (`:2475` `:2565` `:3085`), 所以套件保持绿色, 回归不会被发现。
- 证据: 实跑 (`cases.py` + `runcases.sh`, 仅应用提案第 4 项的 `hook-fornl.sh`; 命令中的路径为 `/etc/forgejo/app.ini`, 与套件 SC-21h 同):

  | 用例 | 基线 v1.76.1 (5.2 / 3.2) | 仅加换行 (5.2 / 3.2) |
  |---|---|---|
  | `for f in /etc/forgejo/app.ini; do cat "$f"; done` (对照) | rc=2 finding | rc=2 finding |
  | `for f in a.txt \`+换行+`/etc/forgejo/app.ini; do cat "$f"; done` | rc=2 finding | **rc=0 allow** |
  | 三行续行 (`a.txt \` / `b.txt \` / 路径) | rc=2 finding | **rc=0 allow** |
  | 续行列表 + `do` 独占一行 | rc=2 finding | **rc=0 allow** |
  | 单行列表 + `do`/`done` 各占一行 (无续行) | rc=2 finding | rc=2 finding |

  首遍对这些命令放行 (仿真与基线首遍同源), 基线的拦截来自 W10。
- 建议改法:
  1. 列表止于**未转义**的换行, `\`+换行仍属列表。已在 bash 5.2.15 与 3.2.57 上验证的写法 (`forre.sh`, 仅验证列表抽取行为, 未接入钩子全量回归): `local nl=$'\n' bs='\'` 后令列表段为 `(([^;&|)${bs}${nl}]|${bs}${bs}(.|${nl}))*)`。60,000 字符列表耗时 0.063 s (5.2) / 0.079 s (3.2)。
  2. 必须用 `$'\n'` 变量注入换行, 不要在方括号里写 `\n`: ERE 里 `\n` 是反斜杠和字母 n, 钩子自己在 `:275-278` 已写过同一条警告。写错的变体 (`hook-bad-for_bsn.sh`) 会把 `for f in /etc/forgejo/app.ini` 截在 `/etc/forgejo/app.i`, 使 `for_single` 与多行用例都变成 allow (现有 SC-21h 会红, 但 SC-7 的「放行」断言会绿)。
  3. SC-7 增加三行 (均期望 finding, 基线同为 finding, 即「钉死不得放行」的回归): 两行续行、三行续行、续行 + `do` 独占一行。

### F3 [Major] D 的「被引用」判据过窄, 链式溢出未定, 不变量断言不成立

- type: issue
- severity: Major
- category: implementation
- scope: proposal What 3 与「补充说明」; 不变量「不新增 fail-open 路径」; SC-6; `secret-guard.sh:645` `:659` `:668-669`
- 摘要:
  1. 判据只列 `$NAME` 与 `${NAME}`。`${NAME:-}`、`${NAME#..}`、`${#NAME}`、`${!NAME}` 等都是 shell 里的引用, 但 W10 不代入它们, 也不会被这两个子串命中, 于是被当作「未引用」放行。
  2. `_sg_vx_collect` 里有**四处** `return 2` (`:645` 赋值, `:659` for 列表, `:668` `:669` 链式展开后超 VMAX)。What 3 只覆盖前两处; 一个自身从不被引用、只因链式展开 (`b=$a$c`) 才超 4096 的值, 字面实现下仍被拦, 与 D 的口径 (未被引用的超大值放行) 不一致, 且规格没说这是有意的。
  3. 「不新增 fail-open 路径」一句在 D 面前字面不成立 (D 本身就是 owner 已裁的放宽); 需改写成「除 D 外」, 并列出 D 的残余 (与小值相同的既有缺口)。
- 证据 (`cases.py`, 基线 vs `hook-dskip.sh` = 提案第 3 项的字面实现):

  | 用例 | 基线 | 字面 D |
  |---|---|---|
  | `F=<app.ini>; cat ${F:-}` (小值, 对照) | rc=0 allow (既有缺口) | rc=0 allow |
  | `B="<2300 个 x 加路径>"; cat $B` | rc=2 oversize | rc=2 oversize |
  | 同上但 `cat ${B}` | rc=2 oversize | rc=2 oversize (含 `${NAME}` 判据时) |
  | 同上但 `cat ${B:-}` (shell 会按空白拆词, 实际读取该文件) | rc=2 oversize | **rc=0 allow** |
  | 同上但 `echo $HOME` (真正未引用, D 本意) | rc=2 oversize | rc=0 allow |
  | `a=<2100>; c=<2100>; b=$a$c; echo hi $HOME` (b 仅链式超限且未被引用) | rc=2 oversize | rc=2 oversize |
  | `for f in <超 4096 的列表>; do echo hi $HOME; done` | rc=2 oversize | rc=0 allow |

  边际能力校准: `${F:-}` 这一类对小值在基线就是放行的 (第一行), D 把同一缺口延伸到超大值; 但这不改变「新版放行、基线会拦、且确实读取凭据文件」这一事实。
- 建议改法:
  1. 判据改为命令全文出现 `$NAME` 或 `${NAME` (不要求紧跟 `}`)。一字之差, 覆盖全部 `${NAME…}` 形态, 方向偏严; `$NAMEX` 前缀撞名继续按偏严处理。
  2. 在 What 3 里写明链式展开溢出 (`:668-669`) 的处置: 要么同口径 (被链式展开吞并的值必然出现在别的赋值值里, 可按「被引用」处理; 真正孤立的溢出值才放行), 要么明说保留拦截并给理由; 加一条 SC 钉死。
  3. 不变量句改写, 并把 D 的残余缺口列表写进规格 (`${F:-}`、间接展开、nameref、子进程读 env 等), 让 owner 看到的是「D 把大值提到与小值相同的覆盖」而不是「没有新路径」。
  4. SC-6 做成引用形态矩阵 (见附录 C 的 REF)。

### F4 [Major] SC-5 按现稿写不出; 给出已验证的确定性方案

- type: issue
- severity: Major
- category: testing
- scope: SC-5; Decision #3
- 摘要: 「单元测试: 时间护栏 helper, 设 `SECONDS=k`、预算 b」有 5 个问题。
  1. helper 没有名字和签名, 非作者无法据规格写测试 (`_sg_vx_pass` 等才是已声明的契约名)。
  2. 没有规定 `_SG_T0` 的状态。独立调 helper 时 `_SG_T0` 是 source 时的值 (新开 shell 里为 0), 此时坏实现「用 `SECONDS - _SG_T0`」与正确实现对任何 k 给出相同结果, 单测**区分不了** Decision #3 要防的那种错误。
  3. 在套件主进程里 source 的话, `SECONDS` 是套件已运行的时间 (数十秒到分钟), 任何走到大副本分支的进程内用例都会被护栏误拦; `SC-T4` 自己的注释就写着「sourced suite: suite-start, spuriously fires」。应当像 `SC-T5` 那样用 `bash -c` 新进程。
  4. 整秒粒度的边界抖动 (见 F12): 「刚好不触发」一侧 (如 k=1, b=3) 在调用跨过整秒边界时翻成触发, 约等于调用耗时占 1 s 的比例 (几个百分点); 唯一抗跳变的「不触发」取值是 k=0 且 b>=3。
  5. 预算为 0 时 C 的 `_sg_over_budget` (`SECONDS - _SG_T0 >= 0` 恒真) 在 `_sg_vx_pass` 的整串与逐段检查点先触发 (`:718` 与 `:732`), 文案相同, 所以**不能用 `SECRET_GUARD_TIME_BUDGET_S=0` 把新护栏隔离出来**。
- 证据 (实测): bash 5.2.15 与 3.2.57 都把环境变量 `SECONDS=<n>` 导入为进程起点 (`SECONDS=5 bash -c 'echo $SECONDS'` 打印 5), 子 shell 继承。用它做端到端, 套件现成的 `env "${WPA_ENV[@]}" "$WPA_HOOK"` 通道 (`:2104`) 直接可用。对 `hook-prop.sh` 与 3 个坏变体, 命令为 9.7 KB 早 `(` 形 `gen.py sc1 300 9700`:

  | 环境 | 正确实现 | `_SG_T0` 型 | 护栏作用于所有副本型 | 预算取原始 env 型 (不封顶) |
  |---|---|---|---|---|
  | `SECONDS=3`, 默认预算 | time 拦 | **allow (漏)** | time 拦 | time 拦 |
  | `SECONDS=0`, 默认预算 | allow | allow | allow | allow |
  | `SECONDS=3`, 小副本变量命令 (`viavar_small`) | finding (同基线) | finding | **time 拦 (红)** | finding |
  | `SECONDS=3` + `SECRET_GUARD_TIME_BUDGET_S=99` | time 拦 (封顶 4) | allow (漏) | time 拦 | **allow (漏)** |

  基线加 `SECONDS=2`: 仍是 oversize, 说明导入的 `SECONDS` 不会误触发 C 的检查点 (C 的 `_SG_T0` 在 collect 开头从 `SECONDS` 重置)。
- 建议改法:
  1. SC-5 改写为三条: (a) 端到端 `env SECONDS=3`: 大副本 => time 拦; (b) 端到端 `env SECONDS=0`: 同命令 => 判定结果 (allow 或 finding); (c) `SECONDS=3` + 小副本 => 与基线判定逐字节相同 (护栏范围) 以及 `SECRET_GUARD_TIME_BUDGET_S=99` + `SECONDS=3` => time 拦 (封顶)。所有 e2e 用例在 `wpa_use_none` 里补 `SECONDS=0`, 防被继承的导出值污染。
  2. 若坚持单元级: 规格里写出 helper 名和返回约定; 单测在 `bash -c` 新进程内, **经 `_sg_vx_pass`** 调用 (其 collect 先重置 `_SG_T0`), 或手工 `SECONDS=k; _SG_T0=$SECONDS`。只断言「k=0 不触发」与「k>=ceil(b/2) 触发」两侧。
  3. 另加一条「不能用 budget=0 隔离」的注释, 避免后人写出一条看似测了新护栏、实际测的是 C 的用例。

### F5 [Major] SC-9: 判据 2 恒绿 (time/超长单行吸收失败), 判据 3 良性语料恒绿, 语料不可复现, 第三方无从复核

- type: issue
- severity: Major
- category: testing
- scope: SC-9 与 SC-9 三条判据; Impact「真实流量回放」
- 摘要:
  1. **判据 2 数的是「尺寸类拦截」**。判据 1 又把 oversize -> time、oversize -> 超长单行列为允许。一个把 130 条全拦成 time 的实现 (例如护栏读到偏大的 `SECONDS`) 同时满足判据 1 与 2, 回放照样「通过」。应改数「原 130 条里被放行的条数」。
  2. **判据 3「没有命令新变成超过 5 s」在良性语料上恒绿**: W1 全量判定最慢 0.97 s, E12 首遍最慢的 oversize 行 1.15 s, 良性语料不可能越 5 s; 而真正的风险 (F1) 不在这批语料里。E12 自己给出的更有意义的线是 >1.25 s (bash 3.2 x4 到 5 s) 与 >1.9 s (Windows x2.6 到 5 s)。
  3. **没有写下预测**。W1 到 W3 已经推出了确定的预期: 138 条基线 oversize 全部 allow (31 条靠 credit), finding/time/超长单行各 0 (W1 judge_rc 全 0; W3 最长行最大 4457 < 8192; E12 里首遍 >1 s 的只有 4 条, 期望触发 time 约 0.4 条)。没有预测的回放会退化成对任何输出的事后解释。
  4. **语料不可复现**: 提取目录 `/tmp/r1traffic` 已不存在 (实查); 源转录是 `/home/dev/.claude/projects` 下 3574 个 jsonl 且每天增长 (含本会话); `extract.py` 按文件名排序 + 字节去重编号, 重提取会让序号整体漂移, W1/W2/W3 与 E12 的逐条索引失去对应。「用 E12 同一批语料」做不到, 只能重提取一批新语料并**同会话重跑基线**再比。
  5. **第三方**: 语料与转录只在这台主机; `.aria/notes/` 在主仓而不在 aria-plugin 仓, 插件使用者既没有语料也没有脚本。SC-9 因此是 owner 本机的一次性验收, 不能作回归守护, 也无法被后来的审计复核 (仓里只有聚合数)。
- 建议改法 (改写 SC-9):
  1. 冻结: 提取后复制到非 `/tmp` 的固定目录, 在证据里记一个「所有命令 sha256 排序后再取摘要」的单值 (只留摘要, 不留逐条哈希, 避免对低熵秘密做离线猜测); 基线与新版在**同一会话、同一冻结集**上各跑一遍, 按序号逐条比。
  2. 预测先行 (写进规格): 基线 kind=oversize 的 138 条 => allow >= 135, finding = 0, 超长单行 = 0, time <= 3 (逐条按序号解释偏差); 其余 2274 条 => 逐条 `new.kind == base.kind` (finding 106 / allow 2168 零容忍)。
  3. 时延判据换成相对线: 新放行的 138 条里 (首遍 + 第二遍) 超过 1.25 s 与 1.9 s 的条数要**披露**, 并给 owner 一个接受阈值; 另在 bash 3.2 上随机抽 20 条报 time 占比 (非门槛)。
  4. 回放脚本的 `kind` 分类要能区分新的超长单行与旧 oversize (见 F10: 现在两者共用「too large to scan」模板, `base-all.sh` 的 `grep` 分不开)。
  5. 在 aria 仓里放一个**可移植的合成替身** (SC-9s): 按 W1 到 W3 的边缘分布 (字节数、膨胀量、最长行、是否命中规则) 生成 138 条合成命令, 提交生成器与种子。它进 CI, SC-9 本体标注为 owner 本机验收。

### F6 [Major] SC-1..SC-4 形状未钉死, 区分不了几类像真的坏实现

- type: issue
- severity: Major
- category: testing
- scope: SC-1 / SC-2 / SC-3 / SC-4
- 摘要: 对每条 SC, 在仿真钩子上构造了坏实现并实跑 (表见附录 B)。结论: 现稿的 SC-1 (约 9.7 KB, 300 个短引用) 能拦住「总长 8192 型」, 但**拦不住**「增长上限 = SMAX+GMAX 的总长型」(9.7 KB 通过, 24 KB 才暴露) 和「用被改写过的剩余串长度算上限」型 (引用都在前 8192 字符内时通过, 引用在 8192 之后时误拦); SC-3 的「4000 x 3」对总长型与增长型给出同一结果; SC-4 能拦「大副本走了 credit」, 拦不住「大副本一律只匹配规则」。此外 SC-1 在 bash 3.2 上抖动 (实测 6 次 4 次 time 拦), 因为 9.7 KB 的首遍已逼近 1 s。
- 证据: `mkpatched.py` 的变体 + `e2e.sh`:
  - `growth_total16k`: `gen.py sc1 300 9700` => allow (与正确实现同); `sc1 300 24000` => oversize (正确: allow)。
  - `growth_mut`: `sc1` (引用在前) => allow; `sc1tail` (9 KB 填充在前, 300 个引用在 8192 之后) => **oversize**。
  - bash 3.2.57 上 `hook-prop.sh` 对 `sc1 300 9700` 6 次: time x4, allow x2 (首遍+collect 约 1.0–1.3 s, 越过两个整秒边界的概率不低)。换成「小原文、大副本」的 `sc1grow` (原文 1,595 字符, 同一个 1000 字符值在 8 个独立行里各引用一次, 副本约 9.6 KB, 增长约 7,968): 3.2 上 6/6 allow (0.43–0.59 s), 5.2 上 3/3 allow; 基线 3.2 上 oversize (0.26 s) => 是稳定的 bf。
- 建议改法 (写进 SC 的输入规格):
  1. SC-1 拆为 1a/1b/1c: 1a 为 `sc1grow` 形 (原文约 1.6 KB, 副本 > 8192, 增长 <= 8192, **多行且每行 <= 8192** 以走分流 2, 块字符放在最前使首遍线性退出); 1b 引用分布在 8192 偏移前后 (抓可变剩余串型); 1c 总长 >= 24 KB (真实语料到 51 KB; 64 KB 命令上限 `:1157`) 且增长小 (抓 SMAX+GMAX 总长型)。1a 同时是 bash 3.2 上可跑的形状。
  2. SC-2 以 1a 形状为底, 凭据路径变量 + `cat $f`, 断言 finding 文案 (`reads a secret-bearing source`) 且非 oversize 文案; 若形状含 > 8192 的单行, 命中会落到超长单行文案, 要在规格里写明这是另一条用例 (SC-4)。
  3. SC-3 加边界钉子: 增长恰为 8192 (判定) 与 8193 (拒), `$NAME` 与 `${NAME}` 各一, 整串与逐段各一 (套件一贯做法: 「a limit that is one too low or too high swaps the text of a side」)。增长 = Σ 引用次数 x (值长 - 引用文本长), 引用文本长为 `|NAME|+1` (`$NAME`) 或 `|NAME|+3` (`${NAME}`)。再加「总长 > 8192 但增长 <= 8192 => 判定」一条 (抓总长型)。
  4. SC-4 的超长行必须**由代入产生** (原文各行都短), 否则「用原串量行长」的坏实现也能通过; 加时延断言: 24 KB 单行 + 含 credit 慢内容的副本, 整进程 < 3 s (只匹配规则的正确实现远低于此, 「算了 credit 但丢弃结果」的坏实现约 10 s, 单行 24 KB 实测 10.12 s)。
  5. 新增 SC-4b: 副本 > 8192、每行都短、含「读取 + `| wc -l`」, 期望 **allow** (credit 生效); 基线 oversize。这是抓「大副本一律只匹配规则」或「按总长分流」两类坏实现的唯一用例。

### F7 [Major] SC-6 / SC-7 的 bf 前提未写明, 现稿的自然写法在基线是绿的; 缺正向对照

- type: issue
- severity: Major
- category: testing
- scope: SC-6; SC-7
- 摘要:
  1. **入口门**: `_sg_vx_collect` 开头 (`:637`) 要求命令里同时有 `$` 与 `=` (或 ` in `), 否则直接返回 0。所以「未被引用的 5000 字符赋值」若命令里没有别的 `$`, 基线**放行**, SC-6 就不是 bf (套件 21ad 注释已写过这一条)。
  2. **for 列表截止符**: 基线列表在第一个 `;` `&` `|` `)` 处就停。「多行 for 循环, 循环体 > 4096, 良性」若循环体里有正常的分号或管道, 列表很短, 基线也不会超限。
  3. 缺**正向对照**: SC-7 的「放行」断言对写错的实现 (`[^;&|)\n]` 把反斜杠和字母 n 排除了) 也是绿的。
- 证据 (基线实跑):

  | 用例 | 基线 |
  |---|---|
  | 多行 for, 循环体 4300 个 `w`, 无 `$` | rc=0 allow (入口门) |
  | 同上但循环体含 `"$f"` | rc=2 oversize (这才是 bf) |
  | 多行 for, 循环体 120 行, 每行含 `"$f"` 且带 `;` (入口门已开) | rc=0 allow (列表被第一个分号截断, 未超 4096) |

  坏实现 `for_bsn`: `for_single` => allow (SC-21h 会红, SC-7 放行侧不红)。
- 建议改法: SC-6 / SC-7 的输入写明「命令含 `$`」「循环体前 4096 字符不含 `;&|)`」, 并要求提交者在基线上先跑出红 (check-runs-at-baseline-first)。SC-7 加正向行 (多行 for 的列表里放敏感路径 => finding) 与 F2 的续行行。

### F8 [Major] 缺失的 SC (14 类)

- type: risk
- severity: Major
- category: testing
- scope: SC 清单整体
- 摘要: 现稿 11 条 SC 没有覆盖: 分段模式、TMAX、扩展口径、各常量边界、三个同值常量的接线、护栏作用范围与封顶、故障注入、最长行线性、credit 成本上界、规则匹配与「判定去掉 credit」等价、闸门以下逐字节差分。清单见附录 C。其中 COST 两条是 F1 的闸, CONT 是 F2 的闸, REF 是 F3 的闸, 必须与修复同批提交。
- 证据: 关键性来自实验而非推测 --
  - 分段模式: `_sg_split_top` **不**按换行切 (`:317-318`), 多行段落可达分流 2; 但分段模式的首遍 `_sg_safe_to_split` 是 O(n^2) (无块字符时): 9 KB 的单段良性命令在基线就要约 3.0 s (实测 21ab2/21ab3 的等价命令, en_US.UTF-8, 负载 4.5), 仿真得 time 拦。所以分段模式的 SC 不能用「大原文」, 要用 `_sg_vx_pass` 直调 + 预置 `_SG_SEGS` (21an 探针风格) 绕过首遍。
  - 最长行线性: 用本代码库惯用的「前缀/剩余串」循环写最长行 (`longest.sh` 的 B 变体) 是二次的: 32 KB / 2500 行 => bash 5.2 2.35 s, bash 3.2 16.27 s; 160 KB / 10000 行 => 5.2 39.8 s。线性的 `while IFS= read -r l ... <<< "$s"` (A 变体) 同输入 0.09–0.61 s。命令上限 64 KB 内就能把 3.2 拖过 5 s => 又一条 fail-open 路径。因为护栏先于最长行计算, e2e 打不到它 (大输入的首遍已 >1 s), 只能单元级。
  - 三个同值常量: `_SGV_SMAX`、`_SGV_GMAX`、`_SGV_LMAX` 都是 8192, 接线错 (在 LMAX 的位置用了 SMAX) 在数值上不可见。
- 建议改法: 见附录 C。

### F9 [Major] 扩展整串检查与 `_sg_vx_apply` 共用: 朴素改法静默放宽, 机制与文案未定

- type: issue
- severity: Major
- category: implementation
- scope: What 5 第一条; SC-8; `secret-guard.sh:1554` `:1562-1563`
- 摘要: 提案要求扩展检查「维持原口径 (副本总长 > SMAX 即拦)」, 但 What 1 又把 `_sg_vx_apply` 的返回 2 条件改成增长口径, 而 `:1554` 的扩展分支调用的就是同一个函数, 靠它的返回 2 来拦。字面照做会让扩展生效时的大副本放行。规格没有说用什么机制 (加参数? 加全局? 另写检查?), 也没有说 `_sg_vx_apply` 的单参数默认口径 (21an 探针以单参数调用) 属于哪一种。
- 证据: 在 `CLAUDE_PROJECT_DIR` 下放 `.aria/secret-guard.paths` (一条无关条目), 命令为 `gen.py sc1 300 9700` (良性 9.7 KB 整串): 基线 rc=2 oversize (在 `_sg_vx_pass` 即被 `the command is longer than 8192 characters after variable expansion` 拦下, 根本走不到扩展分支); 朴素仿真 `hook-prop.sh` => **rc=0 allow**。另: 两版「都拦」时走的是**不同的路径、不同的文案** (基线 L_whole, 正确的新版应是 L_ext), 只断言退出码的 SC-8 分不出「按设计拦」与「因别的原因拦」。
- 建议改法: 规格里写明机制 (例如给 `_sg_vx_apply` 加第二个参数, 缺省 = 增长口径, 扩展分支传入「总长口径」), 并把 SC-8 改成: 扩展生效 + SC-1a 形状 => exit 2 且 `Limit hit:` 行逐字等于 `wpa_L_ext`; 扩展文件存在但不生效 (无有效条目/超 200 条等) => 与无扩展一致 (放行); 21ap 的 8192/8193 边界不变。说明扩展生效的项目得不到 A 的收益 (本机无项目启用扩展, 所以 SC-9 看不到)。

### F10 [Major] 增长 / 超长单行的原因串未给出, 且模板与分支 3 的事实矛盾

- type: issue
- severity: Major
- category: testing
- scope: SC-3; SC-4; What 2 分流 3
- 摘要: 现有尺寸用例靠 `Limit hit:` 行的**逐字内容**区分各拦截点 (`wpa_L_val/seg/whole/total/ext`, `wpa_x_toolarge` 逐字比对)。SC-3 说「新版用『增长』原因串拦」, SC-4 给了一句中文原因串, 但没有任何一处给出**要逐字实现的字符串**。后果: 测试由执笔席自编, 与规格脱钩, 非作者 (TASK-003) 无从复核, 「bf 按文案区分」又会因文案是新字符串而在基线上平凡地红。另外:
  1. 已有 `Limit hit:` 行全是英文 (带 `$_SGV_*` 插值), 提案给的是中文且把 8192 写死。
  2. 「文案沿用 oversize 那一套」, 该模板第一段是 `Nothing was matched.`, 而分支 3 的前提恰恰是**命中了规则**; 用户会看到「没有匹配到任何东西」加一句「命中了凭据形读取」。
  3. 分支 3 与旧 oversize 共用 `command too large to scan` 模板, 回放脚本 (`base-all.sh` 用 `grep 'too large to scan'`) 无法把「oversize」和「超长单行」分开 (F5)。
- 建议改法: 规格里逐字给出 (英文, 带插值) 增长原因串与超长单行原因串各一条; 分支 3 单独一句首段 (去掉「Nothing was matched」); 保持中文说明行。测试用 `wpa_L_gmax` / `wpa_L_line` 逐字比。

### F11 [Major] SC-10 / SC-11 的口径与同步面

- type: issue
- severity: Major
- category: testing
- scope: SC-10; SC-11; Impact
- 摘要:
  1. **SC-11「判定不变」未定义判定**。现有套件一贯指出「after the flip both sides of a limit exit 2, so the exit code alone no longer tells 'judged' from 'refused': the text does」。差分必须以 (退出码, 拦截类别 {finding, oversize + Limit 行, time}) 为判定, 只比退出码会放过 finding <-> oversize 互换。
  2. **被点名要变的用例未列** (SC-11 写「逐条列出」)。按读码 + 在仿真钩子上重放等价命令得到下表 (「推断」= 分支 3 未仿真; 原套件**未整套跑**, 任务书禁止):

     | 现有用例 | 现行断言 | 本 change 后 | 备注 |
     |---|---|---|---|
     | 21ab 第 1 条 (8193 字符段) | 拒, L_seg | 增长约 4 KB 不拒; 单行 8193 > LMAX => 分支 3, 文案变 | 仿真得 finding (无分支 3), 结局推断 |
     | 21ab 第 2、3 条 (9000 字符段, 增长 0) | 拒, L_seg | 放行 (首遍慢时 time) | 仿真 rc=2 timeout: 本机基线首遍约 3 s, 不宜再作「放行」断言 |
     | 21ac 第 3 条 (`for f in <4096>`) | 拒, L_whole | 单行副本 > 8192 => 分支 3 | 推断 |
     | 21ad 第 2 条 (`f=<4097>; echo $HOME`) | 拒, L_val | 放行 (D) | 仿真 rc=0 |
     | 21ag (dense 300) | 拒, L_seg | 增长约 31 KB 拒, 文案变 | 仿真仍出旧 L_seg 串 |
     | 21aj (三个 4000 引用) | 拒, L_seg | 增长约 12 KB 拒, 文案变 | 同上 |
     | 21al 第 2 条 | 拒, L_whole | 分支 3 | 推断 |
     | 21an (函数探针) | `edge8193` 期望状态 2; 不变量「建成副本 <= 8192」 | 状态 0; 不变量改为 `<= ${#S}+GMAX` | 读码 |
     | 21ao 第 2 条 | 拒, L_whole | 分支 3 | 推断 |
     | 21ap (扩展) | 8193 拒 L_ext | 不变 (须维持旧口径) | 见 F9 |
     | 21aa / 21ae / 21ai (TMAX) | - | 不变 | 仿真同基线; 21ah / 21ak / 21am 推断不变 |

     21ad 注释里的「narrowing is the owner's call, not the code's」也要改为已裁。
  3. **SC-10「新增 SC 在真 bash 3.2 下实跑」与 SC-1 的 9.7 KB 形状冲突** (F6): 用该形状在 3.2 上要么抖动要么红。须规定新增 SC 用「小原文、大副本」形状 (1a), 并说明 e2e 的「放行」断言在 3.2 上的前提。
  4. **同步面少列**: standards `secret-hygiene.md` 的测试计数「822 / 816」出现在 `:23` `:316` `:352` 三处 (提案只写 `:316`); 当前套件头为 `Coverage: 831 cases (825 without zsh)` (`:11`), 加新 SC 后要再改, SC-13 会机械校验头注释; 另见 F13 的头注释同步点。
- 建议改法: 如上; 把差分口径与用例清单写进 SC-11, 并加「SC-12 逐字节差分」(附录 C)。

### F12 [Minor] 「用掉一半预算」不准; 文案与事实不符

- type: issue
- severity: Minor
- category: documentation
- scope: What 2 分流 1; 复用 C 的时间预算文案
- 摘要: `SECONDS` 是整秒、起点取整, `(( SECONDS*2 >= 3 ))` 等价 `SECONDS>=2`, 实际在真实耗时 1.0–2.0 s 之间触发 (均值 1.5 s), 不是「3 s 的一半」。实测: 对齐到整秒的 0.85–0.95 处启动 bash 后 `sleep 1.2`, `SECONDS=2`, 护栏判真 (3 次都是) (`secs-granularity.sh`)。该护栏还是「预先拦截」, 而复用的 C 文案写的是「The secret scan did not finish within the guard's own time budget (3s)」, 用户看到 3 s 而实际只过去约 1.2 s。
- 建议改法: 规格改写为「`SECONDS >= ceil(b/2)`」并说明触发区间; 为护栏单独写一句文案, 或在复用文案里去掉「did not finish」。

### F13 [Minor] 同步面: 头注释至少 6 处; 死代码同形兄弟

- type: issue
- severity: Minor
- category: documentation
- scope: What 5 第 3 条;「头注释」
- 摘要: 提案只写「W10 预算段」。实际与新口径冲突的注释至少还有: 文件头 `:88-93` (「a substituted segment up to 8192 characters」), `_sg_vx_collect` 注释 `:630`, `_sg_vx_apply` 注释 `:674`, `_sg_vx_pass` 注释 `:701-703`, `_sg_emit_blocked` 注释 `:826-827` (「nothing was matched」), `_sg_per_segment_eval` 注释 `:1535`。死代码: `:666` 的 `[[ -z "${_SGV_V[j]}" ]] && continue` 确为死 (收集时已跳空值, 链式替换不会使非空变空); 同形兄弟 `_sg_vx_apply` 的 `[[ -n "$v" ]] || continue` (`:684`) 同样是死的, 提案没扫。不变量句「不新增 fail-open」与 D 的关系见 F3。
- 建议改法: 列出同步点清单进 TASK; 死代码一并清。

### F14 [Minor] 「W12 中和」的实现路径未定; 空串放行陷阱

- type: risk
- severity: Minor
- category: implementation
- scope: What 2 分流 3
- 摘要: 基线的 W12 中和是 `_sg_judge_one` 里的四个内联循环 (`:1502` 一带), 没有独立 helper (证据脚本 `rowhit-traffic.sh` 用的是另一快照里的 `_sg_environ_neutral`)。分流 3 要「对 W12 中和后的副本逐条匹配 `risky_patterns`」, 规格没说是抽取成共享 helper 还是复制一份。复制会漂移; 抽取要改热函数。且规则数组 `risky_patterns` 声明在源码闸门之下 (`:1183` > `:926`), 新 helper 在闸门之上引用它, 要注意 SC-30b 的闭包检查与 `set -u`。若中和 helper 失败返回空串, 空串不命中任何规则 => 放行 (fail-open)。
- 建议改法: 规格指定抽取成 helper 并让 `_sg_judge_one` 也调它; 分流 3 里「中和结果为空或比输入短到不合理 => 拦」; 加故障注入 SC (附录 C FAULT) 与「分流 3 的命中 == `_sg_judge_one` 去掉 credit 的命中」差分 (含 `os.environ.get(` 不得误拦的一条)。

### F15 [Minor] 文件引用与编号

- type: issue
- severity: Minor
- category: documentation
- scope: 文首、Tasks 节
- 摘要: 提案两处引用 `detailed-tasks.yaml` (文首 Level 行, Tasks 节), 变更目录里只有 `proposal.md`。SC-1..SC-11 与套件内既有 SC-5..SC-11 撞号 (套件 `:1702` 起已有过一次「SC-8」撞号消歧注释)。
- 建议改法: 补文件或删引用; 新测试用 W10 家族前缀 (`SC-21aq` 起) 命名。

### F16 [Minor] 「字符」口径随 locale 变

- type: issue
- severity: Minor
- category: documentation
- scope: What 1 / 2 的所有阈值
- 摘要: `${#s}` 在 UTF-8 locale 下数字符, 在 C locale 下数字节, 核心路径不强制 locale (只有 W9 扩展局部设 `LC_ALL=C`)。本项目命令里中文很常见: 6000 个汉字的行, UTF-8 下 6000 (走分流 2), C locale 下 18000 字节 (走分流 3, 命中规则即拦)。同一条命令在不同环境走不同分支。
- 建议改法: 规格申报口径 (字符, 随 locale); 边界 SC 只用 ASCII; 另加一条多字节用例在显式 `LC_ALL` 下钉死预期。

### F17 [Minor] A 的收益依赖平台, 措辞需限定

- type: risk
- severity: Minor
- category: documentation
- scope: Why 结论; SC-9 判据 2; CHANGELOG 申报
- 摘要: 「误拦从 138 降到 0」是本机 bash 5.2 的结论。macOS 系统 bash 3.2 (hook 经 `exec bash` 重进时默认取 PATH 里的 bash) 的首遍慢约 6 倍 (同一 9.7 KB 早 `(` 形: 5.2 0.15 s, 3.2 0.93 s), 护栏在 `SECONDS>=2` 即触发, 实测 6 次 4 次 time 拦; 分段模式的 9 KB 命令在本机 5.2 就要约 3 s 首遍。姿态 B 已把「慢平台仍拦」裁为接受, 但对外措辞 (CHANGELOG、issue 回复) 需写明收益范围。
- 建议改法: CHANGELOG 与 issue 回复写「在首遍能在约 1 s 内完成的平台上, 大而不膨胀的整串命令不再被尺寸拦截」。

---

## 附录 A: SC-1..SC-11 逐条可测性判定

「bf」= 在 v1.76.1 上必红。

| SC | 能写成会红的测试? | 恒绿 / 恒红风险 | 区分坏实现 | 判定 |
|---|---|---|---|---|
| SC-1 | 能 (基线 oversize, 已实跑 9.7 KB 早 `(` 形) | bash 3.2 上 4/6 次被护栏拦 => 红; 若命令没有对已赋值变量的引用, 基线也放行 => 假 bf | 抓总长 8192 型; 漏 SMAX+GMAX 总长型、剩余串型 (F6) | 需改 (形状) |
| SC-2 | 能 (finding 文案 vs oversize 文案) | 形状含 > 8192 单行则落到超长单行文案 | 抓「大副本未判」; 对「只匹配规则却借 finding 文案」不敏感 | 需改 (钉形状与逐字文案) |
| SC-3 | 能, 但只靠新字符串 (平凡红) | 文案未给 (F10); 「4000 x 3」对总长型与增长型同结果 | 漏总长型 | 需改 (边界钉子 + 文案) |
| SC-4 | 能 | 文案未给; 超长行若由原文字面产生, 「用原串量行长」型也过 | 抓「大副本走 credit」「跳过最长行检查 (一律 credit)」; 漏「一律只匹配规则」 | 需改 (+SC-4b、时延断言) |
| SC-5 | 单测按现稿写不出 | `_SG_T0` 状态未定; 边界抖动; 隔离不了 budget=0 | 漏 `_SG_T0` 型 | 不可写 => 改 e2e `env SECONDS` (F4) |
| SC-6 | 能 (需命令含 `$`) | 无 `$` 时基线放行 => 假 bf | 漏 `${NAME}` 型 (除非回归行用花括号); 漏 `${NAME:-}`、链式 | 需改 (矩阵) |
| SC-7 | 能 (需循环体含 `$` 且前 4096 字符不含 `;&\|)`) | 自然写法基线是绿的 => 假 bf | 抓「没加换行」; 漏 `\n` 写进方括号型、**续行列表 (F2)** | 需改 (+正向行 +续行行) |
| SC-8 | 能 (回归) | 只断言退出码时两版「都拦」但路径不同 | 抓朴素共用型 (实测 rc=0) | 需改 (钉 L_ext 逐字 + 机制) |
| SC-9 | 部分: 本机验收可做, 非回归 | 判据 2 吸收失败 (恒绿), 判据 3 良性语料恒绿; 语料已不可复现 | - | 需重写 (F5) |
| SC-10 | 套件回归可做 | 3.2 上 9.7 KB 形状红/抖; 计数同步 3 处 | - | 需改 (形状 + 同步面) |
| SC-11 | 差分可做 | 「判定」口径未定; 用例清单未给 | - | 需改 (F11) |

## 附录 B: 坏实现矩阵 (均在仿真钩子上实跑)

| 坏实现 | 实现方式 (`mkpatched.py` 标志) | 现稿哪条 SC 能抓 | 实测 / 缺口 | 需补 |
|---|---|---|---|---|
| 增长用总长算 (基线口径) | 不改 SMAX | SC-1 | 抓 | - |
| 增长用总长算 (SMAX+GMAX) | `growth_total16k` | 无 | SC-1 的 9.7 KB 通过; 24 KB 才 oversize | 1c: >= 24 KB 小增长 |
| 增长用「被改写的剩余串长度」 | `growth_mut` | SC-1 仅当引用在 8192 之后 | 引用在前 allow; 引用在后 oversize | 1b |
| 跳过最长行检查 (一律 credit) | 删分流 3 | SC-4 第 1 行 | 抓 (`\| wc -l` 获救 => 期望拦) | - |
| 跳过最长行检查 (一律只匹配规则 / 按总长分流) | 未仿真 (推断) | 无 | SC-1 良性通过, SC-2 若断言 finding 文案可抓 | SC-4b |
| 时间护栏用 `_SG_T0` | `tguard_t0` | SC-5 现稿 (无 `_SG_T0` 状态) 不稳 | `SECONDS=3` => allow (漏) | F4 的 e2e |
| 护栏作用于所有副本 | `tguard_all` | 无 | `SECONDS=3` + 小副本 => time (红) | 护栏范围 SC |
| 护栏读原始预算 (不封顶) | `tguard_rawbudget` | 无 | `SECONDS=3` + 预算 99 => allow (漏) | 封顶 SC |
| 引用检测漏 `${NAME}` | `dskip_nobrace` | SC-6 回归行仅当用花括号 | `cat $B` 仍拦; `cat ${B}` => allow | REF 矩阵 |
| 引用检测用 `$rest` (赋值之后的剩余串) | `dskip_rest` | 无 | 本批用例无差异 (引用在赋值前时在整串模式首遍多半已拦, 逐段模式下无实际危害), 仅作口径钉子 | REF 矩阵 (低优先) |
| for 正则没加换行 | = 基线 | SC-7 | 抓 (前提见 F7) | - |
| for 正则把 `\n` 写进方括号 | `for_bsn` | SC-7 放行侧不红; 现有 SC-21h 红 | `for_single` => allow | SC-7 正向行 |
| for 正则加了换行但丢续行 | `forlist_nl` | 无 | 续行列表 => allow (F2) | CONT |
| 扩展分支吃了新口径 | `growth` (朴素) | SC-8 仅当断言放行/拦 | rc=0 | F9 |
| 大副本走了 credit | = 跳过最长行 | SC-4 第 1 行 | 抓 | 时延断言 |

## 附录 C: 建议新增 / 改写的 SC

| 标识 | 内容 | 判据 | 备注 |
|---|---|---|---|
| COST-a | 打补丁副本在 `_sg_compute_credit` 入口记 `${#1}` 与 Σ(行长^2) (套件 `wpa_hook_copy` 现成手法) | 对 `viavar 6 8000`、`8 x 7000`、`48 x 1000`、单行 24 KB 四个对抗形状, 记录值 <= 规格的上界 | 确定性, 不依赖时钟; F1 的闸 |
| COST-b | 同四个形状整进程时延 | 结果类别 in {finding, time, 超长单行} 且 wall < 3 s (bash 5.2) | 基线对 `viavar` 形状本就快, 属回归守护 |
| CONT | for 续行三行 + 续行加 `do` 独占行 | finding (基线同) | F2 的闸 |
| REF | 引用形态矩阵: `$B` `${B}` `${B:-}` `${B#x}` `${#B}` `${!B}` `$BX`(前缀撞名) `B` 在更早 / 更晚的段、链式 `C=$B`、for 列表同矩阵 | 被引用 => 拦 (oversize), 未引用 => 放行; 钉死链式溢出结局 (`chain_unref`) | F3 的闸 |
| EDGE-G | GMAX 边界: 增长恰 8192 判定 / 8193 拒; `$NAME` 与 `${NAME}`; 整串与逐段 | 逐字 `Limit hit:` | 套件惯例 |
| EDGE-L | LMAX 边界: 最长行 8192 走全量 (credit 生效 => allow) / 8193 走分流 3 (拦) | 逐字文案 | 同值常量需 DISTINCT |
| EDGE-S | SMAX 分界: 副本 8192 不进护栏 / 8193 进护栏 (`SECONDS=3` 下前者照常判定, 后者 time) | - | 抓「护栏作用于所有副本」 |
| DISTINCT | 探针里把 `_SGV_GMAX` `_SGV_LMAX` `_SGV_SMAX` 设成互不相同的值 (如 300/200/100), 逐一验证各检查点只认自己的常量 | 21an 探针风格 | 同值 8192 掩盖接线错 |
| GUARD | `env SECONDS=3` / `SECONDS=0` / 小副本 / 预算 99 封顶 | 见 F4 | `wpa_use_none` 补 `SECONDS=0` |
| CREDIT+ (SC-4b) | 副本 > 8192、短行、含 `\| wc -l` | allow; 基线 oversize | 抓「一律只匹配规则」 |
| LONGLINE-LAT | 24 KB 单行含 credit 慢内容 | 超长单行拦, wall < 3 s | 抓「算了 credit 又丢弃」 |
| SEG-PROBE | `_sg_vx_pass` 直调 + 预置 `_SG_SEGS`: 逐段的增长拒、全量判定、分流 3、护栏、TMAX (只计有代入的段; 总和是副本长度而非增长)、拒绝时 `_SG_SUB` 不变、建成副本 <= `${#S}+GMAX` (21an 重写) | 状态码 + 文案 | 绕开分段模式 O(n^2) 首遍 |
| TMAX | 5 段、每段约 8 KB 且各自增长约 6 KB, 良性 (经 SEG-PROBE 直调, 不走 e2e: 分段模式大原文的首遍 O(n^2)) | 拒, `wpa_L_total` (新版) / `wpa_L_seg` (基线) | TMAX 仍按副本总和, 大命令多段仍会被拦, 规格应申报 |
| EXT | 见 F9 | 逐字 L_ext | 扩展生效者得不到 A 的收益 |
| FAULT | 对每个新 helper 打故障 (`wpa_fault_case` 手法): 失败 => exit 2, 不得 exit 0; 中和结果为空 => 拦 | 与 SC-20i-k 同族 | F14 |
| LINEAR | 最长行 helper 直调 60 KB / 4000 短行 | < 1 s (bash 5.2) 且 4N / N 的耗时比 < 8 | 二次实现: 2500 行 2.35 s (5.2) / 16 s (3.2) |
| EQUIV | 分流 3 的命中 == `_sg_judge_one` 去掉 credit 的命中 (遍历套件里所有 BLOCK 行, 包进 > 8192 行); `os.environ.get(` 在超长行里不误拦 | 差分 | F14 |
| SC-12 | 逐字节差分: 副本 <= 8192、值 <= 4096、无未引用超大值的命令网格 (模式 x 值长 {0,1,100,4096} x 引用数 {0,1,8,9} x 花括号 x 敏感 / 良性读取) | 基线与新版 (退出码, stderr 全文) 逐字节相同 | 抓「闸门以下行为漂移」 |
| MB | 多字节: 显式 `LC_ALL=en_US.UTF-8` 与 `C` 各一条 | 钉死口径 | F16 |

## 附录 D: SC-5 与 SC-9 专项评估

**SC-5 (SECONDS 赋值的进程内单测) 是否可行**: 可行但需修正。可行性依据: bash 允许给 `SECONDS` 赋值, 之后读数 = 赋值 + 自赋值起的整秒数; 子 shell 继承; 5.2.15 与 3.2.57 都支持用环境变量 `SECONDS=<n>` 导入为起点 (已实测), 因此端到端也能确定性复现。修正点: (1) 新 shell 内跑; (2) 经 `_sg_vx_pass` 或手工重置 `_SG_T0`; (3) 「不触发」侧只用 k=0; (4) 不要指望 budget=0 隔离新护栏; (5) helper 命名或改为契约名驱动。详见 F4。

**SC-9 (真实流量回放) 能否复现 / 判据能否证伪**: 本机、当次可做, 不可复现、不可移植。判据 1 可证伪 (逐条比 kind); 判据 2、3 如 F5 所述会恒绿; 应补预测与冻结。语料只在本机对第三方意味着: 无法复核、无法进 CI、仓里只有聚合数; 需要合成替身承担回归守护。

## Verdict

按「0C+0M = PASS、0C+>=1M = PASS_WITH_WARNINGS、>=1C = FAIL」计算: Critical 2 (F1, F2), Major 9 (F3..F11), Minor 6 (F12..F17) => **FAIL**。

两条 Critical 都是**规格层**问题 (改设计 / 改正则), 不是实现疏漏; 且 F1 的修复会改变分流 2 的准入条件, 需要 owner 对「全量判定的总量上界取多大」(慢平台姿态) 给出数字, 这是姿态 A/B 之间的接缝, 不是重议姿态。

## 轮次记录

- 轮次: R1 (convergence), 席位 qa-engineer, 侧重可测性。
- 已做:
  1. 读 BRIEF、proposal、`secret-guard.sh` 的 W10/credit/ext 相关段、测试套件 `:1700-1830` `:2440-2700` `:2975-3245`、证据 W-summary / W1-W3 / E12 / `traffic/*`。
  2. 核对 proposal 的代码断言: SMAX 数总长 (`:685` `:694`), `_SG_T0` 首遍后才重置 (`:1542`, 另 `:633` `:607`), 钩子内无 `SECONDS=` 赋值 (grep), 扩展分支重跑 `_sg_core_eval` (`:807` 一带 `_sg_ext_pass`)、共用 `_sg_vx_apply` (`:1554`), 死代码 (`:666`), 头注释 (`:580-596`), 命令 64 KB 上限 (`:1157`)。结论: 这些断言除下列者外成立; 不成立者: credit 成本「只跟单行长度」(F1)、「通配段不跨空白」(对 `_SG_PROCTAB_ALL` 不成立, F1)、「不新增 fail-open」(F1 F2 F3)、standards 计数位置 (F11)。
  3. 在 scratch 副本上仿真提案与 8 个坏变体, bash 5.2.15 / 3.2.57 实跑; PoC 与数字见各 finding。
- 未核实 / 偏离:
  1. 未实现分支 3, 涉及分支 3 的结局 (21ab 第 1 条、21ac 第 3 条、21al、21ao 的新文案) 为推断。
  2. 未整套跑原测试套件 (任务书禁止); SC-11 的变更清单来自读码 + 等价命令重放。
  3. 未在 Windows / Apple 构建的 bash 3.2 上验证; 慢平台系数取自 E12 的 x2.6 / x4 约定。
  4. credit 成本拟合只有 4 个点、共享宿主 (负载 1.3–4.7), 系数仅作量级。
  5. F2 的续行正则只验证了列表抽取行为 (两个 bash 版本), 未接入钩子跑全量回归。
  6. 资源纪律偏离一次: `longest.sh` 的二次对照在 160 KB 输入上, bash 3.2 的 B 变体触发了我设的 100 s `timeout` 被截断 (已在 F8 写明为下限), bash 5.2 的同一项 39.8 s; 其余实验单次 <= 60 s。
- 未改动仓库任何文件; 本报告为唯一新增文件 (仓外产物均在上述 scratch 目录)。

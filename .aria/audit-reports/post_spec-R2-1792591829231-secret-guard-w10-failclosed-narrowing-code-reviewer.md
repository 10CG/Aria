---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-10-21T14:45:47.807Z
context: openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R2 — code-reviewer 席（侧重：钉进规格的代码与代码事实）

- 审查对象：proposal v2（主仓 `41e9308`）。
- 基线：aria `59e333c`（v1.76.1）+ standards `a611136`。
- 实验脚本都在 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217audit-r2/code-reviewer/`，下文记作 `$W`。
- 实验纪律：一律 `taskset -c 0,1 nice -n 19`，单次 < 1 min；未跑全套件；未改 proposal 和代码。

## 审计结论

### 核实无误的部分（不是 finding）

- **参考实现与 helper 一致**：proposal `:131–159` 与 `traffic/deadline-helper.sh` 逐字相同（`diff` 无输出）。
- **语法与 3.2 兼容**：
  - `bash -n` 在 3.2.57 与 5.2.15 下都通过。
  - 以下写法在 3.2 下都可用：`$'\n'`、`${out##*"$nl"}`、`${out%"$nl"*}`、`[[ =~ ^[0-9]+$ ]]`、算术三元。
  - W6 在两版 bash 下都跑通了 rc=0、2、3 三条路径。
- **变量作用域**：
  - `jp`、`tp`、`r` 只在命令替换子 shell 里赋值，不会泄漏；都是先赋值后使用，`set -u` 下不报错。
  - `_sg_vx_big` 的 `left out rc nl`、`_sg_vx_big_judge` 的 `line max` 都是 local。
  - `_sg_vx_pass` 的 `rc`、`ar` 已在 `:705` 声明；`_sg_per_segment_eval` 的 `ar` 已在 `:1538` 声明。
- **What 2 的两处拼接**：
  - 整串块替换 `:728`，其后 `:729 return 0` 保留。
  - 分段块替换 `:748–750`，不影响 `:738` 的 `continue` 和 `:739–746` 的增长、TMAX 出口。
  - 没有漏 `fi` 或 `return`，也没有改变无关分支。
- **What 3**：
  - 改的是 `:1498` 的 local 声明；插入点在 `:1512` 命中之后、`:1513` 计算 credit 之前。
  - W12 中和（`:1505–1510`）仍在最前面。
  - 不传第三参时，与基线逐字节相同。
- **不会挂起**：`_sg_judge_one` 及其调用链（`_sg_compute_credit`、`_sg_line_match`、W12 循环）都在进程内运行。会 fork 的只有 `_sg_emit_blocked` 的 `cat` 和 `_sg_redact_echo` 的 `sed`，都很短命，所以判定被掐断后不会有长时间占着管道的后代。孤儿写者引出的问题见 F1。
- **行号全部核对一致**：
  - Why 表与 What 1：`:594–596`、`:645`、`:659`、`:668–669`、`:685`、`:694`、`:744`、`:725`/`:740`、`:728`、`:748–750`、`:607`、`:633`。
  - What 2、3、4：`:178`、`:926`、`:1581`、`:1506–1509`、`:1500`、`:1554–1555`、`:1563`。
  - Why 成本模型：`:182`（`_sg_compute_credit` 里恰好 14 处 `_sg_line_match`）、`:476`、`:437`、`:446`。
  - 唯一例外是 Impact 第 1 处，见 F12。
- **What 6 的死代码**：
  - `_SGV_V` 只在 `:651`、`:661` 追加，追加前 `:646`、`:660` 已经排除空值。
  - 链式代入（`:668–669`）用非空值替换，失败就 `return 2`，不会写入空串。
  - 所以 `:666` 恒为假，删掉后行为不变。
- **standards 计数**：`secret-hygiene.md` 的 `:23`、`:316`、`:352` 三处都是 822/816；套件头 `:11` 是 831/825。与 proposal 的说法一致。
- **新字面量与断言手法**：
  - GMAX=8192 时，`wpa_L_grow_whole`、`wpa_L_grow_seg` 与 What 5 的原因串逐字相同。
  - `wpa_x_toolarge`（`:2533–2543`）用 sed 抽出 `Limit hit:` 行，可以直接匹配新原因串。
  - 它对 oversize 模板的其余检查（「命令过大」、「Split it」、长度 < 3000）继续成立。
- **既有直调探针不受 `_SG_P0` 陈旧的影响**：
  - SC-8 的五档负载（`:1891–1897`）都是没有 `$` 引用的小命令。
  - 21an 探针每次新开 shell，只调用 collect 和 apply。
  - SC-T5 只调用 `_sg_time_budget`。
- **既有用例预测的其余部分**：除 F3 外逐条核过，成立。包括 21ab 后两条 exit 0、21ag 与 21aj 按 `wpa_L_grow_seg` 拦、21an 的契约变化，以及「预计不变」清单（21aa、21ad、21ae、21af、21ah、21ai、21ak、21am、21ap）。

### Findings

#### F1 — Critical · issue · implementation · v2 新文本

- **scope**：What 2 参考实现 `_sg_vx_big`，以及「要点」里的两句断言：「被掐断的判定即使写了半截文案也会被丢弃，只出时间文案」「失败的方向都是拦」。
- **摘要**：被掐断的判定可能被解析成放行。
  - 状态码与判定输出走同一条管道，靠「最后一行」来解析。
  - 判定被 `kill -KILL` 时，它的外部子进程（`_sg_emit_blocked` 里 heredoc 的 `cat`）会成为孤儿。这个孤儿仍持有命令替换的写端，可能在 `printf '\n%s' "$r"` **之后**才写完拦截文案。
  - 此时解析出的 `rc` 是文案的最后一行。finding 模板的末行是命令全文的末行（`Command was: ...`）；longline 模板的末行是命令前 200 字符的末行。
  - 如果那一行是 `0`，`_sg_vx_big` 就返回 0，命令被**放行**。而判定原本的结论是 BLOCK，基线也是按尺寸拦。
  - 如果那一行是 `2`，结果是拦，但输出的是夹着 `137` 的残缺文案。
- **证据**：
  - `$W/orphan-race.sh`：用一个慢写入的孤儿把调度顺序固定下来，两版 bash 都输出 `command's last line '0' -> _sg_vx_big status 0 (ALLOW)`。
  - `secret-guard.sh:869–897`：finding 模板由外部 `cat` 写出，末行是 `$command` 的末行。`:852–866` 同理。
  - 触发条件：
    - 真实环境里的窗口是 `cat` 的存活期（毫秒级），必须与截止时刻重合；
    - 命令末行由命令作者决定，可以反复重试。
  - 这种情况概率低但不为零，与上面两句断言直接矛盾。SC-N5 和 SC-N10 都测不到。
- **建议**：
  - 给状态行加一个本次调用生成、命令作者无法预知的标记，只认带这个标记的最后一行，否则返回 3。写法（3.2 兼容）：
    - 声明：`local tag="sg$RANDOM$RANDOM"`；
    - 计时块末尾：`printf '\n%s %s' "$tag" "$r"`；
    - 解析：`last="${out##*"$nl"}"; [[ "$last" == "$tag "* ]] || return 3; rc="${last#"$tag "}"; out="${out%"$nl"*}"`。
  - 至少也要加一行 `[[ $rc -eq 0 && -n "$out" ]] && return 3`。理由：放行的判定不会写出任何东西。
  - 补一条故障注入 SC：替身判定通过外部子进程慢慢写，末行为 `0`；期望返回 3，只出时间文案。

#### F2 — Major · risk · architecture · v2 新文本

- **scope**：不变量「时间上不新增 fail-open」；What 2；What 4 的「扩展本身的代价……不变」；Decision 7。
- **摘要**：硬截止只包住 `_sg_vx_big` 那一次判定。大副本按时判完并放行后，同一条命令还有两段工作不在截止之内：
  - (a) 分段模式下后面各段的小副本 `_sg_judge_one`。段前只有 `_SG_T0` 的协作式检查点（`:732`），单次判定本身没有上界。
  - (b) W9 扩展对**原命令**的 `_sg_ext_pass`。命令里出现扩展条目时，它在 `:813` 的检查点之后重跑 `_sg_core_eval`（`:814`），代价与首遍同级。
  - 对这类命令，基线在 W10 就按尺寸拦掉了，根本走不到 (a)、(b)。
  - 因此存在「基线几毫秒就拦、新版超过 5 s 进而 fail-open」的输入。两个例子：
    - 大副本段在截止前判完，后面再跟一段小副本，里面有 8000 字符的 token 和一处读取（R1 测得 credit 约 1.0–1.2 s，慢平台更久）；
    - 启用了扩展、命令里含条目的大命令：首遍 + 大副本判定 + 扩展的 `_sg_core_eval`，约为首遍的 3 倍。
  - 全局最坏值没有超出基线已有的残余（小副本串联本来就能做到），但 proposal 的断言是无条件的，而且 (b) 与 What 4 的说法矛盾。
- **证据**：
  - 代码：`secret-guard.sh:731–751`、`:809–816`、`:1548`。
  - 分量实测（`$W/fp-parts.sh`）：24 KB 的文本类命令，首遍 `_sg_judge_one` 在 5.2 上约 1.37 s，在 3.2 上约 1.7–1.8 s。
  - **未做 e2e 实测**，那需要完整的试实现。
- **建议**：二选一。
  - 技术收口：本次 `_sg_vx_pass` 一旦调用过 `_sg_vx_big`，其后的段判定一律也走 `_sg_vx_big`，或者在它们之前加 `(( SECONDS - _SG_P0 >= cap ))`，成立即拦；`_sg_ext_pass` 的检查点同样处理。这样做只会把「基线本来就按尺寸拦的命令」变成按时间拦，不会新增误拦。
  - 照实申报：把 (a)、(b) 写进「不变量与范围外」和 CHANGELOG 的残余。

#### F3 — Major · issue · testing · v2 新文本

- **scope**：「预计会变的既有用例」表。
- **摘要**：
  - 表里有 4 行预测「大副本判定 → finding」，实际会走 C 路径，出 `longline` 文案：21ab 第 1 条、21ac 第 3 条、21al 第 2 条、21ao 第 2 条。原因是这些副本都是**单行**，最长行就是副本全长（8193 / 8218 / 8193 / 8193），超过了 `_SGV_LMAX`。
  - `wpa_x_finding`（`:2522–2527`）只检查子串 `reads a secret-bearing source`，而 What 5 的 longline 首行同样含这个子串。所以把这 4 条改写成 `wpa_x_finding` 会意外变绿，掩盖实际走的分流。
  - 次要：21ag 的增长约 35.6 KB（80×297 + 40×296 + 18），不是「约 31 KB」。
- **证据**：`$W/table-copies.sh` 用基线的 collect 和 apply（放开 SMAX）把副本建出来，四条的输出都是 `big, nocredit => longline`。
- **建议**：
  - 这 4 行改成「→ longline」，理由写「单行副本超过 LMAX」。
  - 给 `wpa_x_finding` 加一条反向断言「不是 longline 首行」，并另设 `wpa_x_longline`。

#### F4 — Major · issue · testing · v2 新文本（SC-N1 的形状描述沿用 v1 的 SC-1）

- **scope**：SC 表的 SC-N1、SC-N2、SC-N3 的行布局。
- **摘要**：C 分流看的是**副本**的最长行，但这三条 SC 都没有钉行布局。
  - SC-N2 写「SC-N1 的形状 + 经变量读取 → finding 模板，逐字」。#217 正文只写了「9.7KB 命令 (300 个短变量)」，没有说行布局；套件现有的 W10 生成器 `wpa_vx_*` 生成的全是单行。如果复现形是单行，副本就是一行超过 8192，会出 longline，逐字比对恒红。
  - SC-N3 写「增长恰为 8192 → 进入判定，含读取则 finding」。增长要达到 8192，至少得代入两个约 4 KB 的值；两者在同一行时，最长行超过 8192，同样出 longline。
  - 照字面执行，执笔席会以为是代码错了，可能把行长改成按原串量——这正是 SC-N4b 要抓的坏实现。
- **证据**：
  - `secret-guard.sh:317–318`：`_sg_split_top` 不按换行切段。
  - F3 的实测。
  - #217 正文（Forgejo 只读 GET）。
- **建议**：
  - 期望 finding 或 credit 的大副本 SC（SC-N2、SC-N3 的 8192 例、SC-N4、SC-N4d）写明「副本每行 ≤ 8192，多行布局」。
  - 期望 longline 的 SC 写明「单行」。
  - SC-N1 写明行布局。

#### F5 — Major · issue · testing · v2 新文本

- **scope**：SC-N4e、SC-N12。
- **摘要**：两条 SC 都没写明「读取只在副本里可见，也就是经变量」。照字面读，首遍 `_sg_core_eval` 会先判原命令，两条都恒红：
  - (a) SC-N4e 写「一行 24 KB、含读取」。如果读取写在原文里，首遍就会在这一长行上算 credit。按这条 SC 自己的形状约束，算 credit 要超过 3 s，「墙钟 < 2 s」不可能满足；在生产环境里还会退回「首遍不计时」的 fail-open（#228）。
  - (b) SC-N12 后半写「把套件中 20 条 BLOCK 用例的命令各自包进超长行 → 全部按 longline 拦」。这些命令的原文本身就会命中规则，首遍直接出 finding 模板，走不到 W10，也就出不了 longline。另外，按命令名命中的规则行（进程表、环境转储一类）要先改写成经变量调用才能藏起来，规格没有说怎么改。
- **证据**：
  - `secret-guard.sh:906–922`：首遍逐段判定，含 credit。
  - `:1539–1541`：首遍一旦拦下就直接返回。
  - SC-N9 那一行明确写了「经变量的读取」，SC-N4e 和 SC-N12 没写。
- **建议**：
  - SC-N4e、SC-N12（连同 SC-N4 系列）写明「凭据源只经变量出现，原文在首遍不命中」。
  - 给 20 条 BLOCK 用例写出逐条改写规则（路径类放进赋值；命令类写成 `c=<cmd>; $c`），或者改成「从中选 N 条可以改写的」。

#### F6 — Major · risk · testing · v2 新文本（SC-N1 的 3.2 抖动是 v1 沿用，R1 QA-F6 已指出）

- **scope**：What 2 的时钟段；SC-N1c、SC-N1、SC-N8 的 TMAX 例、SC-N16；SC-N17 的「全部 SC-N 在 3.2 下全绿」。
- **摘要**：
  - **掐断时刻是一个区间**：硬截止从 hook 启动算起，首遍包含在内。`SECONDS - _SG_P0` 是两个整秒读数之差，可能比真实流逝少读、**也可能多读**近 1 s。所以从 `_SG_P0` 起算，实际掐断时刻落在 `[cap−1, cap+1)`，cap=3 时是 [2, 4) s。proposal 只写了「读数最多比真实流逝时间少约 1 s」这一侧。
  - **对 SC 的隐含要求**：期望非时间结局的大副本 e2e SC，都隐含要求「3.2 下首遍 + 判定 < 约 2 s」。规格只给 SC-N4e 和 SC-N9 写了形状约束。
  - **实测**（24 KB 文本类良性整串命令）：
    - 基线 e2e：5.2 上 1.45–1.48 s，宿主负载高时 3.21–3.35 s；3.2 上 2.13 s，负载高时 3.91–3.94 s。
    - 只判定副本：5.2 上约 1.37 s，3.2 上约 1.7–1.8 s。
  - **受影响的 SC**：
    - SC-N1c（≥ 24 KB，期望 exit 0）：按整秒对齐估算，5.2 上约 45% 会被时间拦，3.2 上约一半。
    - SC-N8 的 TMAX 例：5 段，每段原文约 8 KB、副本约 14 KB；要先在截止内判完 4 个大副本才轮到 TMAX，所以可能出时间文案，而不是 `wpa_L_total`。
    - SC-N1（9.7 KB）：3.2 上的抖动仍在。
    - SC-N16：要求「oversize → time 为 0」，但 W5 最慢的一条总计 1.93 s，紧贴 2 s 的最坏截止，宿主一有负载就会出现 time。
- **证据**：
  - `$W/n1c-time.sh`、`$W/fp-parts.sh`、`$W/trace-e2e.sh`。xtrace 显示时间几乎全花在 `:1512` 的规则循环上。
  - `secret-guard.sh:617`：协作式预算同样是整秒读数。
- **建议**：
  - 时钟段补上「多读」那一侧，写明实际掐断时刻是 [2, 4) s。
  - 所有期望非时间结局的大副本 SC，统一加形状约束：3.2 下首遍与判定各 < 0.5 s，实测值写进用例注释。或者允许 3.2 下以 time 结局，并单列判据。
  - 不测时间的直调 SC，写明用 `_SG_P0=$((SECONDS+60))` 中和截止。
  - SC-N16 写明在空闲宿主上跑；出现 oversize → time 时重跑确认，而不是直接判红。

#### F7 — Minor · issue · documentation · v2 新文本

- **scope**：Why 表的 W5 行；`evidence/W5-deadline.txt`。
- **摘要**：W5 的「硬截止设为 3 s / 4 s」有两处不准：
  - v2 的截止封顶 3，「4 s」不是能配出来的值。
  - 同一个 cap=3，实际掐断时刻落在 [2, 4) s（见 F6），所以「3 s」那一列既不是最坏情况，也不是最好情况。
  - 用同一份证据按最坏的 2 s 重算：Windows ×2.6 是 31/138，bash 3.2 ×4 是 62/138。proposal 写的是 8/3 和 35/17。
  - Linux 三档都是 0，因为最慢一条 1.93 s < 2 s，这个结论不变。
- **证据**：`traffic/deadline-estimate.sh` 的阈值是 `split("3 4",D," ")`；换成 `2 3 4` 后的重算输出见「轮次记录」。
- **建议**：
  - Why 表和 CHANGELOG 的慢平台收益写成区间（最坏按 2 s，最好按 4 s），删掉「4 s」这一配置。
  - `deadline-estimate.sh` 增加 2 s 一档。

#### F8 — Minor · issue · documentation · v2 新文本

- **scope**：What 4「与基线完全相同」；「放宽了什么」。
- **摘要**：扩展门那一行并不逐分支等价。
  - 变量值比引用短时，代入会让副本变短，于是可能出现「中间副本超过 8192、最终副本不超过 8192」。
  - 这时基线 apply 返回 2：启用扩展时按 `wpa_L_ext` 拦，W10 自身也按尺寸拦。
  - v2 的 apply 返回 0，最终副本不超过 SMAX，不触发新门；扩展改为检查副本，W10 改走小副本判定。
  - 安全上没有损失（副本被完整检查了），但「完全相同」不成立。「放宽了什么」只列了「副本 > 8192、增长 ≤ 8192」，漏了这一类。
- **证据**：`$W/shrink.sh`。命令 8330 字符，基线 apply 返回 rc=2；最终副本 8082 字符（增长 −248）。
- **建议**：
  - What 4 改为「最终副本超过 8192 时与基线相同；中间超限而最终不超限的副本改为完整检查」。
  - 「放宽了什么」补上这一条。

#### F9 — Minor · issue · implementation · v2 新文本

- **scope**：What 1 的 `lim`。
- **摘要**：「在函数入口计算一次 `lim=$(( ${#1} + _SGV_GMAX ))`」没写 `local`。照字面实现会生成一个全局 `lim`，违反文件里变量一律 local 的惯例；套件 source hook 之后，它也会进入套件的命名空间。
- **证据**：`secret-guard.sh:678`，即现有的 local 列表。
- **建议**：写明「把 `lim` 加进 `:678` 的 local 列表」。

#### F10 — Minor · issue · testing · v2 新文本

- **scope**：SC-N10。
- **摘要**：照字面「套件 `wpa_fault_case` 的手法」做不出这条 SC：
  - `wpa_fault_case`（`:2442–2446`）写死了 `_sg_ext_*` 正则和五个金丝雀。这五个都是没有变量引用的小命令，走不到 `_sg_vx_big`。
  - `wpa_hook_copy`（`:2437–2441`）只在函数入口插语句。插在 `_sg_judge_one` 入口会连首遍一起弄坏，exit 2 恒成立（恒绿），测不到 nocredit 分支。
- **建议**：
  - 写明用 `wpa_hook_copy` 插一条带条件的语句，例如往 `_sg_judge_one` 插 `[[ "${3:-}" == nocredit ]] && exit 1`。payload 用一条能走到「大副本 + 单行」路径的命令。
  - 往 `_sg_vx_big_judge` 入口注入时，同样配上大副本 payload。
  - 期望里写上 internal error 文案，以便与时间拦区分开。

#### F11 — Minor · issue · testing · v2 新文本

- **scope**：SC-N11、SC-N13。
- **摘要**：
  - (a) SC-N11 测「最长行测量」，但这段代码内联在 `_sg_vx_big_judge` 里，紧接着就调用 `_sg_judge_one`。不先 stub 掉判定的话，计时里占大头的是规则匹配。另外，60 KB 的线性 read 只要几毫秒，在毫秒级计时上「4N 与 N 的耗时比 < 8」噪声很大。
  - (b) SC-N13 网格里「值长 4096 × 引用 8 或 9」的格子，副本约 32 KB，违反网格自己的前提「副本 ≤ 8192」。新旧两版在这些格子上的文案必然不同（一个是总长原因串，一个是增长原因串），差分恒红。
- **建议**：
  - SC-N11 写明先定义 `_sg_judge_one() { return 0; }` 再计时，并重复多次，使单次计时 ≥ 100 ms。
  - SC-N13 写明剔除副本超过 8192 的格子。

#### F12 — Minor · issue · documentation · v2 新文本

- **scope**：Impact 的 9 处注释同步；SC-N15。
- **摘要**：
  - (a) 第 1 处行号差一：W10 条目在 `:87–95`，不是 `:86–94`。
  - (b) 这份封闭清单漏了测试里逐用例的注释和用例名，它们同样写着「数总长」的语义：
    - 注释：21ag `:2585`、21aj `:2597–2599`、21al `:2628–2632`、21an `:2643–2644`、21ao `:2679–2681`；
    - 用例名：`:2552`、`:2586`、`:2605`、`:2633`、`:2676`、`:2682`。
  - (c) 第 4 处 `:630–631` 本来就没有与死代码相关的措辞，SC-N15 的 grep 断言无内容可断，恒绿。
  - (d) SC-N15 对测试文件做「退役短语不在」的 grep 时，断言自己那一行就含退役短语，照字面写恒红。
- **建议**：
  - (a) 改正行号。
  - (b) 把这些行并入第 9 处。
  - (c) 删掉第 4 处，或改为补上状态 3（`:667` 会返回 3，现有契约注释漏写了）。
  - (d) 写明退役短语在运行时拼装，或 grep 时排除断言自身所在的行。

#### F13 — Minor · issue · documentation · v2 新文本

- **scope**：What 5 的 longline 模板；时间文案；CHANGELOG 草稿；Why 对 `:476` 的更正；页眉。
- **摘要**：几处措辞与代码事实不符。
  - (a) 文中说模板「含两处展开」，实际有三处：`${_SGV_LMAX}`、`$pat`、`$(_sg_redact_echo …)`。
  - (b) longline 正文说算 credit「can outlast Claude Code's 5s hook timeout and let the command through UNSCANNED」。v2 有了硬截止，超时的结果是按时间拦，不是放行，这个理由已经过时。
  - (c) `SECRET_GUARD_TIME_BUDGET_S=4` 时，硬截止在 3 s 掐断，时间文案却打印「(4s)」，因为 `:832–834` 会重新解析预算。
  - (d) CHANGELOG「收窄」一条写「改为在硬截止内完整判定」，对超长单行的情况（只匹配规则、不算 credit）不准确。
  - (e) Why 说「阻止它跨行匹配的是其后的 `[[:blank:]]`」，不成立。两版 bash 下用整串 `=~` 时，`_SG_PROCTAB` 的 `[^|;&]*[[:blank:]]` 都会跨换行匹配：`$W/crossline.sh` 的 s1 整串匹配为 MATCH，逐行的 `_sg_line_match` 为 no。所以 `_SG_PROCTAB` 本身也是跨行成本项，Why 的第 3 项不止 `_SG_PS_REMOTE_T` 一个。
  - (f) 页眉写「`evidence/` W0–W6」，但 W7 已经存在，并且被引用了。
- **建议**：逐条改正。
  - (b) 改成「can use up the guard's time budget」一类的说法。
  - (c) 硬截止触发时，文案打印 `min(_SG_TIME_BUDGET,3)`；或者把这个出入写进申报。

## Verdict

- **FAIL**：Critical 1（F1），Major 5（F2–F6），Minor 7（F7–F13）。
- 13 条全部针对 v2 新写的文本。其中 F4、F6 牵涉 v1 沿用的 SC-1 形状和 3.2 抖动，各条已注明。
- F1 改一行（或加状态行标记）就能关闭。若主控直接修进 v3，本席余下的是 5 Major + 7 Minor，相当于 PASS_WITH_WARNINGS。

## 轮次记录

- **本席情况**：本轮首次参与（R2），没有参与 R1。
- **R1 处置抽查**：
  - 到位：A5（线性 read 循环）、A6（复用 W12 中和）。
  - 行号正确，但清单不全：A13，见 F12。
  - 到位但缺 local：A19，见 F9。
  - 预测表有误判：A12，见 F3。
  - SC-1 在 3.2 上的抖动以新形式延续：A10，见 F6。
- **实验输出摘录**（脚本都在 `$W`）：
  - `orphan-race.sh`，5.2 与 3.2 结果相同：末行 `0` → status 0 (ALLOW)；末行 `2` → status 2；末行 `7` → status 7。
  - `table-copies.sh`：
    - `21ab-1 copy=8193 growth=8014 longest_line=8193`
    - `21ac-3 copy=8218 growth=4094 longest_line=8218`
    - `21al-2 copy=8193 growth=5408 longest_line=8193`
    - `21ao-2 copy=8193 growth=4014 longest_line=8193`
    - 四条都是 `big, nocredit => longline`。
  - `shrink.sh`：`len(cmd)=8330`，`baseline apply rc=2`；放开 SMAX 后最终副本 `len=8082`，`growth=-248`。
  - `crossline.sh`：5.2 与 3.2 结果相同，`s1 MATCH (per-line _sg_line_match: no)`。
  - `n1c-time.sh`（24 KB 文本类整串良性命令，基线 e2e）：
    - 5.2：3.35 / 3.21 s（负载 1.79）；1.45 / 1.48 s（负载约 1.1）。
    - 3.2：3.91 / 3.94 s（负载高）；2.13 s（负载约 1.4）。
    - 10 KB 在 5.2 上为 0.36 / 0.37 s。
  - `fp-parts.sh`（只判定 24 KB 命令）：
    - 5.2：C.UTF-8 下 1748 ms（负载高）/ 1372 ms；C locale 下 446 ms。
    - 3.2：en_US.UTF-8 下 1775 / 1700 ms。
  - W5 用同一 awk、阈值改为 2/3/4 s 的重算：
    - linux：0/0/0
    - windows-x2.6：31/8/3
    - bash3.2-x4：62/35/17
- **未核实**：
  - F2 的端到端 > 5 s 实例（需要完整试实现）；
  - 真实环境中 F1 竞态的发生概率；
  - Windows MINGW64 与 macOS 上的任何行为。

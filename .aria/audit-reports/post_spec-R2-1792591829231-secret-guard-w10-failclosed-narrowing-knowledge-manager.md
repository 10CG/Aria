---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-10-22T00:40:40.061Z
context: openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R2 — knowledge-manager 席（proposal v2 @ `41e9308`，基线 aria `59e333c` + standards `a611136`）

> 结论：FAIL（1 Critical / 4 Major / 12 Minor）。除 F-01 外都是同步面、收口、复现性、措辞类问题，修订成本低。F-01 是一条我用规格逐字实现的草稿实测出来的「基线按尺寸拦、新版超过 5 s」输入，落在 W9 扩展阶段，不在硬截止之内。

## 审计结论

### 做了什么（范围与方法）

- 通读 proposal v2 全文，逐条对照基线源码 `aria/hooks/secret-guard.sh`、套件 `aria/hooks/tests/secret-guard.test.sh`、`aria/hooks/hooks.json`、standards `conventions/secret-hygiene.md`、`aria/CHANGELOG.md` 现有体例。
- 读 R1 汇总，核对 24 簇处置是否到位。
- 只读 GET 了 Forgejo 上 `10CG/aria-plugin` 的 #154、#201、#216、#217（含评论）、#219（含评论）、#228（含评论）、#229、#230；另用 `git ls-remote` 只读查远程分支。没有任何写操作。
- 复跑证据：W5（逐字吻合）、W4 / W6（两版 bash 下定性吻合）、E12 聚合数、W0 清单对 E12 的逐条核对；`manifest.py` / `refreeze.py` 用合成语料验证。没有生成或读取真实命令原文。
- 在 scratchpad 里按规格逐字构造了一份草稿 hook（`patch_hook.py` 由基线 + `traffic/deadline-helper.sh` 生成，`bash -n` 在 3.2.57 与 5.2.15 下通过），端到端跑了套件 21aa–21ap 的命令形状与几组对抗形状。所有重实验都带 `taskset -c 0,1 nice -n 19`，单次不超过 1 分钟，同一时间只开一个。

草稿与脚本都在 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217audit-r2/knowledge-manager/`：`patch_hook.py`、`hook-draft.sh`、`run21.sh`、`run_ext.sh`、`run_stage.sh`、`run_adv.sh`、`run_apply.sh`、`run_n6.sh`。

下面每条 finding 末尾的「针对」写明它落在 v2 新文本还是 v1 沿用文本。

---

### F-01  扩展阶段不在硬截止内：基线按尺寸拦的命令，新版会跑到 5 s 以上

- **type**：issue　**severity**：Critical　**category**：implementation
- **scope**：§不变量「时间上不新增 fail-open」（`:257`、`:345`）；§What Changes 4（`:196–202`）；Decision 7（`:413`）
- **针对**：声明与 What 4 末句「扩展本身的代价……不变」是 **v2 新文本**；「扩展阶段不进硬截止」的设计沿用 R1-A4 的处置。
- **一句话**：硬截止只罩住 W10 判定，随后的 W9 扩展阶段不受限：基线按尺寸拦的含变量大命令，新版在启用扩展的项目里要跑 7–10 s（超过 5 s 即 fail-open）。
- **摘要**：硬截止只罩住 W10 的 `_sg_vx_big`。随后 `_sg_per_segment_eval` 里的 W9 扩展阶段——对原命令的首次 `_sg_ext_pass "$cmd"`（`secret-guard.sh:1548`，其内 `_sg_core_eval "$sub"` 在 `:814`）——既不在硬截止内，也不受 What 4 新加的那一行约束（那一行只管第二次看「代入后整串副本」）。基线对「引用了变量、总副本 > 8192」的整串模式命令在 W10 阶段就按尺寸拦下（`:724–726`；分段模式下含大分段的命令按代码读法同理，我未实测），根本到不了扩展阶段；新版让这类命令的 W10 判定在 0.2 s 内放行后，把它们交给扩展阶段，而扩展对大原文的判定可超 5 s，Claude Code 杀 hook 后 fail-open。
- **证据**：
  - 输入：项目 `.aria/secret-guard.paths` 列一个路径（`billing/conf/prod.toml`）；命令 `(x=1; : $x` + 一行 24000 个 `A` + `cat /srv/billing/conf/prod.toml)`，整串模式，变量引用良性。
  - 结果（bash 5.2.15，CPU 秒为 user+sys）：基线 exit 2「too large」，0.16 s；草稿 exit 2「finding」，7.3–10.4 s（墙钟 7.5–10.8 s，另有一次 35 s 的宿主负载尖峰）。同一命令不开扩展，草稿 0.23 s 放行，说明时间全花在扩展阶段。
  - 其它尺寸：16000 字符单 token，基线 0.11 s / 草稿 3.5 s；5 行 × 8000 字符 token，基线 0.21 s / 草稿 9.3 s（墙钟 10.5 s）。
  - `_sg_ext_pass` 里的 `_sg_over_budget` 检查（`:813`）拦不住：W10 阶段只用了约 0.2 s，远未到 3 s 预算，此后 `_sg_core_eval` 无界。
  - 孪生输入（去掉变量引用）在基线上本来就要 10.3 s（24000）/ 4.5 s（5 × 8000），均为 CPU 时间，属 #228 的已知残余；本条的增量是把「含变量」这一类也放了进去，并让不变量的措辞失真。
  - 复现：`bash run_stage.sh <hook> 24000`（基线与草稿各一次）、`ADV=1 NS=5 bash run_ext.sh <hook>`。
- **建议改法**：
  1. 沿用基线结局：`_sg_vx_pass` 一旦走过大副本分支（任一副本 > `_SGV_SMAX`），置一个标志；`_sg_per_segment_eval` 在首次 `_sg_ext_pass "$cmd"` 之前，若标志在且 `_sg_ext_entries` 非空，直接按 `:1563` 的扩展尺寸文案拦。这恰好复原基线对这类命令的结局，也与 Decision 7「扩展保持绝对尺寸门」同口径。
  2. 或把硬截止挂到整个扩展阶段（Decision 9 的机制），代价是改动面更大。
  3. 无论哪种，改写 `:202` 与 `:257` 的措辞，补一条回归 SC：扩展生效 + 整串 + 单个 24000 字符 token + 引用变量 + 读取列出路径 → exit 2 且墙钟 < 5 s（基线本就绿，属 rg）。
- **严重度说明**：按任务书字面「新的 fail-open」定 Critical，也是主控在 R1 汇总里写下的可证伪判据（「新版超过 5 s、基线不会」）。限定条件是项目启用了扩展，且输入含一个超大 token。若主控按 R1-A4 的先例（Major）校准，可以降级，但 `:257` 的措辞必须同时改掉。

---

### F-02  「预计会变的既有用例」表有 4 行结局写错：实际走 `longline`，不是 finding

- **type**：issue　**severity**：Major　**category**：testing
- **scope**：§预计会变的既有用例（`:321–335`）；SC-N2 / SC-N3（`:292–293`）；SC-N18（`:319`）
- **针对**：**v2 新文本**。
- **一句话**：「预计会变的既有用例」表里 4 行结局写成 finding，实际是 longline（LMAX = SMAX 使单行大副本只走 C 路径）；SC-N2 / N3 有同源歧义。
- **摘要**：表里 21ab 第 1 条（`:2553`）、21ac 第 3 条（`:2566`）、21al 第 2 条（`:2634`）、21ao 第 2 条（`:2683`）都写「判定 → finding」。这四条的副本都是**单行且长度 ≥ 8193**，而 `_SGV_LMAX` 与 `_SGV_SMAX` 同为 8192，使「副本 > SMAX」与「最长行 > LMAX」对单行副本恒等：单行大副本永远走 nocredit，到不了 credit 路径，结局是 `longline` 模板。
- **证据**（草稿 hook 逐条实跑，`run21.sh`）：
  - 21ab#1 `longline`；21ac#3（副本 8218）`longline`；21al#2 `longline`；21ao#2 `longline`。
  - 预测对的：21ab#2 / #3 exit 0；21ag、21aj 为 `wpa_L_grow_seg`。
  - 与基线相同、预测对的：21aa、21ac#1 / #2、21ad 四条、21af、21ah、21ai、21am、21ap 三条。
  - `wpa_x_finding`（`:2522–2527`）只验「exit 2 + 含 `reads a secret-bearing source` + 不含 `too large to scan`」，`longline` 首行含该子串，所以照预测改用例会变绿，但断言的是错的模板；表也就无法兼作 SC-N18「允许变化」的权威清单。
  - 同源的歧义：SC-N2（「SC-N1 形状 + 凭据变量」）若是单行，结局是 `longline`，不是「finding 模板」；SC-N3 增长恰为 8192 的「含读取则 finding」同理。规格没说副本是单行还是多行，两种读法结局不同。
  - 21an 的 `edge8193`（`:2672`）期望 apply 状态 2，新版为 0（增长约 8014 ≤ 8192），表里只写了「断言改式」，没写这一行的状态翻转。
- **建议改法**：表中四行改为 `longline`；新增 `wpa_x_longline` 断言（钉首行「command reads a secret-bearing source in a line longer than」）；SC-N1–N3 写明副本是单行（longline）还是多行（credit 路径），SC-N4 系列必须用多行构造；补 21an `edge8193` 的状态翻转；把「LMAX = SMAX 使单行大副本只走 C 路径」明写进 What 2。

---

### F-03  SC-N15 的 grep 断言按字面不可证伪

- **type**：issue　**severity**：Major　**category**：testing
- **scope**：SC-N15（`:315`）；§Impact 注释同步清单（`:349–358`）
- **针对**：**v2 新文本**。
- **一句话**：SC-N15 的 grep 断言不可证伪：给的例句在基线折行（空真），其余 7 处没给短语。
- **摘要**：SC-N15 要求「每处一条 grep 断言：退役短语不在，新语义关键词在」，但规格只给了两处的退役短语，且给的例句在基线就查不到。
  1. 例句 `blocking is as cheap as passing was` 在基线折成两行（`secret-guard.sh:581–582`），单行 `grep -F` 在基线返回 0，所以「短语不在」在基线就是空真，无法发现旧句残留。`:587–588` 的 `The limit counts the whole judged string, not its growth` 同样折行。
  2. 其余 7 处没有给任何短语，执笔席可以事后挑词（memory author-to-match-checker）。
- **证据**：`grep -c -F "blocking is as cheap as passing was" aria/hooks/secret-guard.sh` 得 0；去掉 `# ` 续行前缀并连接后得 1。测试侧 `:2545` 的短语在单行内，没有这个问题。
- **建议改法**：SC-N15 改为「先把连续注释行去掉 `# ` 前缀并连接，再 grep」，并把下表写进规格（行号为基线）：

| 位置 | 应退役 | 应出现 |
|---|---|---|
| `:87–95` | `a substituted segment up to 8192`（`:90`） | 写死一个词，如 `grows` |
| `:577–590` | `blocking is as cheap as passing was`（`:581–582`）；`The limit counts the whole judged string, not its growth`（`:587–588`）；`8192 because a BLOCK verdict costs the square`（`:586`） | `_SGV_GMAX`、`_SGV_LMAX`、`hard deadline` |
| `:597–606` | `the _SGV_* size budget are unchanged`（`:606`） | `_SG_P0` |
| `:674–676` | `the copy would be longer than _SGV_SMAX`（`:674`） | `_SGV_GMAX` |
| `:701–703` | `An overrun of the length budget (a value, a copy, the total)`（`:702`） | `_sg_vx_big` |
| `:826–828` | — | `longline` |
| `:1534–1536` | `when that copy is too large to build`（`:1535`） | `absolute` |
| `:1492–1496`（漏列，见 F-06） | — | `nocredit` |
| 测试 `:2510–2518`、`:2544–2549`、`:2556–2562` | `the WHOLE judged string, not its growth`（`:2545`）；`_SGV_SMAX 8192 = one substituted copy`（`:2517`）；`which is how a 4096-character list is refused`（`:2558`） | `_SGV_GMAX`、`_SGV_LMAX` |

---

### F-04  #217 的收口与残余仍有缺口：评论请求、Decision 9、平台未实测、顺序

- **type**：issue　**severity**：Major　**category**：documentation
- **scope**：§Tasks TASK-006（`:427`）、TASK-004（`:425`）；Decision 9（`:415`）；§范围外（`:262–265`）
- **针对**：**v2 新文本**；同类缺口 R1-A14 只修了一半。
- **一句话**：#217 收口缺评论 28512 的处置，Decision 9 在 #228 无载体，平台未实测无载体，开单与关键词的顺序倒置。
- **摘要**：
  1. **#217 评论 28512（2026-10-14）第 2 点**要求「收窄 item 1 时一并评估扩展整串那一眼的口径」。Decision 7 评估后保持绝对门，但 TASK-006 的对账项（第 1 项 / 小项 / 第 2 项 / 第 3 项 / count 轴）没有这一条。关闭 #217 时，这个显式请求既没有「已评估、结论、残余」的记录，也没有载体（启用扩展的项目，整串副本 > 8192 仍被拦）。#217 正文「都不改预算数值、不碰 5s 超时 #216」与本变更新增硬截止之间的差异，也应在对账评论里点明（由 owner 的 B 裁定放行）。
  2. **Decision 9 在 #228 一侧没有载体**。`openspec/changes/secret-guard-scan-cost-and-firstpass-cap/proposal.md`（§v3）对「硬截止 / watchdog / kill -KILL / W4」零命中，#228 的三条评论（29792 / 29840 / 29957）也没有。归档后（#201：归档闸只看任务文件）这个重启选项与 W4–W6 证据的位置会失联。#228 评论 29957 记的「已知残余……变量间接的读取同样可以」在本变更后对大副本已被硬截止收口，需要更正一句。
  3. **「Windows / macOS 硬截止未实测」只落 CHANGELOG**（TASK-004「实测或申报」），没有 issue、owner、recipe。#219 评论 28755 / 28759 有 owner 在 Windows 主力机跑 recipe 的先例。
  4. **顺序倒置**：残余 issue 在 TASK-006（阶段 D）才开，而 CHANGELOG 在 TASK-005（发版）要写「已知限制（归 `#NNN`）」（v1.76.1 体例）需要号。「只对 #217 使用关闭关键词」也没说明在哪个提交：若在发版提交，#217 会在 TASK-005 就被自动关闭，早于 TASK-006 的逐项对账。
- **证据**：`issue217.json` / 评论 28512；#228 三条评论全文；`grep -n "硬截止\|watchdog\|kill -KILL\|W4" openspec/changes/secret-guard-scan-cost-and-firstpass-cap/proposal.md` 无输出；`aria/CHANGELOG.md:20` 的「已知限制（归 `#228`）」体例。
- **建议改法**：
  - TASK-006 的对账项加一条评论 28512 第 2 点的处置，并写明关闭条件：对账评论逐项列出「完成 / 转 #NNN / owner 撤回 / 不变」，且所有残余 issue 号已落在 CHANGELOG 与该评论里。
  - 在 #228 贴一条评论：Decision 9 的选项、`.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/` 的 W4–W6 位置，以及对「变量间接读取」残余的更正。
  - 残余 issue（for 列表续行感知、collect 把 heredoc 内的赋值形文本当赋值、Windows / macOS 实测）提前到 TASK-001 开，号写进 CHANGELOG；写明关闭关键词出现在阶段 D 的主仓提交，不在发版提交。

---

### F-05  SC-N16b 的输入不存在且无人产出；SC-N16 的回放链走不通

- **type**：issue　**severity**：Major　**category**：testing
- **scope**：SC-N16 / SC-N16b（`:316–317`）；§证据与复现（`:372–395`）；§Tasks（`:420–427`）
- **针对**：**v2 新文本**。
- **一句话**：SC-N16b 依赖的 standin.sh 与期望结果不存在且无任务；SC-N16 回放链缺 index.tsv、两次运行互相覆盖、longline 被记成 finding。
- **摘要**：
  1. SC-N16b 是第三方唯一能复跑的验收项，它依赖的 `traffic/standin.sh` 和「入库的期望结果」都不在仓里（`ls` 实测），Tasks 里没有任务明确产出它们。规格说的「W1 四类形状」在 W1 里推不出来：W1 只有 size-whole 137 / value-whole 1 两类，增长分桶有五档，两种读法。
  2. SC-N16 的回放链：文档步骤止于 `refreeze.py`，它只写 `<out>/cmds/<n>.txt`，不产出 `index.tsv`（我在合成语料上验证：`frozen=5 found=3 missing=2`，输出目录只有 `cmds`）。而回放要用的 `base-all.sh`（`.aria/notes/2026-10-20-secret-guard-scan-cost-and-firstpass-cap/traffic/`）逐行读 `$TRAFFIC_DIR/index.tsv`。
  3. `base-all.sh` 固定写 `$TRAFFIC_DIR/base-all.tsv`，基线与新版各跑一遍会互相覆盖；W1–W3 脚本又读同一个文件里的 `oversize` 行，最后跑新版会把 W1–W3 的输入清空。
  4. `base-all.sh` 的分类靠 grep：`reads a secret-bearing source` → finding，所以 `longline` 会记成 finding，SC-N16 的类别表没有 `longline` 一格；规格也没有指名比对脚本。
- **建议改法**：把 `standin.sh`、期望结果文件、回放脚本（接受 hook 路径与输出文件名）、按 n 对比两份结果的脚本列为 TASK-001 的交付，写进「证据与复现」；SC-N16 的类别表加 `longline`；定义「四类」。

---

### F-06  注释同步「封闭清单」不封闭，行号有两处偏差

- **type**：issue　**severity**：Minor　**category**：documentation
- **scope**：§Impact 注释同步（`:349–358`）；SC-N17（`:318`）
- **针对**：**v2 新文本**。
- **一句话**：注释同步清单不封闭：行号偏差两处、第 4 处无事可改、漏 `_sg_judge_one` 契约与用例标题，插入位置与 standards 计数无机械核对。
- **摘要与证据**：
  - 第 1 处应为 `:87–95`：`:86` 是上一条的末行，`:95`（`calls pass; the output side is left to secret-scan.sh.`）才是 W10 条末行。
  - 第 9 处第一个块头注释是 `:2510–2518`，`:2519–2521` 是代码（`wpa_rep`、`wpa_vx_pad`、`wpa_vx_fill`）。
  - 第 4 处（`:630–631`）没有任何与死代码相关的措辞，无事可改，对应的 SC-N15 子句空转。
  - 漏列 `_sg_judge_one` 的契约注释（`:1492–1496`）：新增第三参数 `nocredit` 与 `longline` 出口。
  - 7 个会变用例的标题（如 21ab 的「the copy is not judged, … blocked as too large」`:2552`）描述的也是旧语义，不在 9 处里。
  - 新用例必须插在 SC-13 断言（`:3213–3229`）之前，否则头注释计数断言变红；规格没写。
  - 计数能否机械核对：套件头 `:11`（831 / 825）由 SC-13 在套件内核对；standards 三处（`secret-hygiene.md:23`、`:316`、`:352`，现为 822 / 816）没有机械核对，SC-13 的注释（`:3216–3217`）明说「跨仓……机械 grep 确认，不在本 test 内断言」，SC-N17 只写「计数同步」。
  - 证据页眉（`:13`）写「W0–W6」，表里有 W7。
- **建议改法**：改正两处行号；删第 4 处，补 `_sg_judge_one` 注释与 7 个用例标题；写明插入位置；SC-N17 加一条 grep 断言：`grep -oE '[0-9]+ (self-tests|regression cases)' conventions/secret-hygiene.md` 三处与套件头一致。standards 的版本行：先例不统一（1.1.2 单独记了一行，#128 / #145 / #153 / `191560e` 的计数同步都只改三处计数），建议规格写明沿用「只改三处」。

---

### F-07  证据复现的本机依赖申报不全

- **type**：risk　**severity**：Minor　**category**：documentation
- **scope**：§证据与复现（`:372–395`）
- **针对**：沿用 R1-A22，v2 已补一部分，余下为新发现。
- **一句话**：证据复现的本机依赖申报不全（bash 3.2 的 Linux 构建、`b2ed608` 仅在 origin、`E12-base-all.tsv` 等）。
- **摘要**：已申报的：命令原文不入库、`TRAFFIC_DIR`、`NEUT_SRC`、字节 / 字符口径、慢平台倍率是借来的。未申报的：
  1. 「真 bash 3.2.57」是本机的 Linux 构建，位于 `/home/dev/.aria/tools/bash-3.2.57/bash`，不在仓里，也没有构建配方；`file` 显示 ELF x86-64，b1-baseline F5 也写过它与 Apple 构建可能有常数差。
  2. `NEUT_SRC`（分支 `b2ed608`）只在 `origin` 上（`git ls-remote github` 无此分支），分支一删 W2 就无法复现。
  3. W5 要读另一个笔记目录的 `E12-base-all.tsv`，页眉只列了 `E12-base-real-traffic.txt`。
  4. 脚本默认 `TRAFFIC_DIR=/tmp/r1traffic`；用到 `taskset` / `nice` / `jq` / `python3` / mawk；`assign-probe.py` 在 `traffic/` 里但证据表没列；W-summary 仍是手写摘要（`:378`「B 阶段改为脚本生成」），Tasks 里没有这个任务。
  5. 「用 #228 的 `traffic/extract.py`」（`:386`）没给路径，第三方会去 aria-plugin 仓里找。
- **已验证可只凭仓内文件复现**：W5（逐字吻合）；W4 / W6（bash 5.2.15 与 3.2.57 下定性吻合，数值随宿主负载浮动，负载下 W4 的单次开销是 5 ms 而非 1–2 ms）；E12 聚合 739 / 130 / 138 由 `E12-base-all.tsv` 复算吻合；W0 清单的字节数与 E12 逐条吻合（2412 / 2412），W1 的 n 全在 W0 内，sha256 无重复；`manifest.py` / `refreeze.py` 的逻辑在合成语料上正确。
- **建议改法**：「证据与复现」加一行「本机依赖」，列出以上各项；`b2ed608` 打 tag 或推 GitHub；W-summary 脚本化列为任务。

---

### F-08  CHANGELOG 草稿：漏报残余、收益限定不足、体例不符

- **type**：issue　**severity**：Minor　**category**：documentation
- **scope**：§Impact CHANGELOG 草稿（`:365–370`）
- **针对**：**v2 新文本**。
- **一句话**：CHANGELOG 草稿漏报 for 列表等残余，放行结论缺平台与负载限定，体例不符。
- **摘要与证据**：与正文对照，放宽面、仍然拦、count 轴、首遍、Windows / macOS 未实测都一致。问题在于：
  1. 残余漏了两类：for 列表跨换行误拦（#217 第 2 项转残余，多行 for 循环仍会被误拦）；`_sg_vx_collect` 把 heredoc 内赋值形文本当赋值。读者看到「#217 收口」会以为第 2 项也做了。
  2. 收益依赖负载与平台，草稿只写「Linux 上全部放行」。W5 估算 3 s 截止下 Windows 约 8 / 138、bash 3.2 约 35 / 138 仍被时间文案拦（粗估）；#219 评论 28755 显示 MINGW64 上进程启动开销是 5–9×，不是 2.6×，所以首遍部分的 Windows 估计偏乐观。我在 loadavg 2–5 / 4 核上跑同一条 40 KB 良性整串命令（16 赋值、128 引用）：基线 exit 2 尺寸拦 0.74 s；草稿一次放行（墙钟 3.1 s，CPU 2.7 s），一次被时间文案拦（墙钟 4.2 s，CPU 1.6 s）。「放行」结论应限定「机器空闲」。
  3. 「真实流量」是维护者单机会话记录里超过 4 KB 的 2412 条样本，应写明样本口径。
  4. 漏了用户可见的变化：`Limit hit:` 原因串改为 `grows by more than`；新增 `longline` 模板；`SECRET_GUARD_TIME_BUDGET_S=4` 对大副本不再延长（硬截止另封顶 3 s）。
  5. 体例：现有条目（`aria/CHANGELOG.md:13–23`）是「版本头（含 issue 与 semver 说明）/ `### Security — …` / **问题** / **修复** / **行为变更** / **已知限制（归 `#NNN`）** / 测试行（含用例数）/ `Refs`」。草稿的「收窄 / 申报」标签不在体例内，缺测试行与 Refs；「收窄」一词易被读成变严。
- **建议改法**：按 v1.76.1 体例重排，补上以上各点；放行结论加「空闲机器」限定。

---

### F-09  Why 表的「3 s / 4 s」与 3 s 封顶矛盾

- **type**：issue　**severity**：Minor　**category**：documentation
- **scope**：§Why 表 W5 行（`:43`）；Decision 4（`:406`）；What 2「截止时长」（`:122–125`）
- **针对**：**v2 新文本**。
- **一句话**：Why 表的「3 s / 4 s」两列与 3 s 封顶矛盾。
- **摘要**：W5 生成于 13:17Z，封顶 3 s 随 W6 的参考实现（13:55Z）才出现，晚于 W5；`deadline-estimate.sh` 里 `split("3 4",D," ")` 硬编码两列。封顶后「截止设为 4 s」这一列不存在，读者会以为调高 `SECRET_GUARD_TIME_BUDGET_S` 能把 Windows 的时间拦从 8 条降到 3 条。
- **建议改法**：删 4 s 列，或注明它只对应封顶前的设计；脚本同步。

---

### F-10  有两种读法的句子

- **type**：issue　**severity**：Minor　**category**：documentation
- **scope**：全文措辞
- **针对**：均为 **v2 新文本**。
- **一句话**：八处有两种读法的句子（「第 N 项」三套编号、字母重载、「8192 以上」、SC-N5a / N6 等）。
- **逐条**：
  1. 「第 N 项」用了三套编号：#217 自己的条目（TASK-006 `:427` 的「第 2 项转残余 issue」「第 3 项由 owner 撤回」；`:262`）、v1 的 What 编号（R1 处置对照 A2 `:434` 的「撤下第 4 项」）、v2 的 What 编号。v2 的「第 2 项」是硬截止（要做的），「第 3 项」是 nocredit（要做的），「第 4 项」是扩展门（保留的），与前两套的含义全都相反。应一律写「#217 第 N 项」或「v1 What 4」。
  2. 字母 A / B / C / D 重载：owner 姿态（`:269–274`）、十步循环阶段（Tasks 表阶段列 `:422–427`，如 `TASK-006 | D`）、R1 簇号 A1–A24、#216 的 C、#228 的 B / C。
  3. `:74`「比原串长出 8192 以上」读作 ≥，而代码（`> lim`）、What 5（`more than`）、SC-N3（8192 放行、8193 拦）都是 >。
  4. SC-N16b「W1 四类形状」（见 F-05）。
  5. SC-N5a「返回时间拦」：是 `_sg_vx_pass` 返回 2 并写时间文案，还是 `_sg_vx_big` 返回 3？N5d / e / f 都明写 `_sg_vx_big`。
  6. SC-N6（`:305`）没写模式。实测（`run_n6.sh`）：套件 21ap 的分段模式形状，基线已是 `wpa_L_ext`，不是 bf；只有整串模式形状（加 `(true)`）基线是 `wpa_L_whole`、新版是 `wpa_L_ext`。
  7. `:215`「含两处展开」：`longline` 的 heredoc 里有三处（`${_SGV_LMAX}`、`$pat`、`$(_sg_redact_echo …)`）。
  8. `:126`「这就是 v1『判定前已没有时间就拦』的那一半」：规范性文本在指涉上一版。

---

### F-11  INV-6 悬空；INV-4 / 5 / 7 与认领没有继承

- **type**：issue　**severity**：Minor　**category**：documentation
- **scope**：TASK-006（`:427`）、TASK-001（`:422`）、页眉
- **针对**：沿用 R1-A23 未解部分。
- **一句话**：INV-6 悬空，INV-4 / 5 / 7 与认领没有继承。
- **摘要与证据**：
  - TASK-006 写「（INV-6）」，但 INV 列表在另一个 Spec：`openspec/changes/secret-net-l3-and-bypass-paths/detailed-tasks.yaml:28–42`，INV-6 是「提交页脚与 PR 描述对三张 issue 只写 Refs」，在本 Spec 内无定义。
  - 同一份清单里 INV-4（新 helper 在闸门之上）本规格实际遵守了，INV-5（夹具运行时拼装）在正文有一句，INV-7（时档类测量只在低负载下串行跑、判据只看比值）没有继承，而 SC-N4e / N5c / N5e / N9 / N11 带绝对墙钟上界（N11 有比值）。我在 loadavg 约 3.7 / 4 核的宿主上，基线的 21ap 8192 字符形状墙钟 5.3 s、草稿 8.4 s，说明绝对上界在共享宿主上要谨慎。
  - TASK-001「续用认领」没有指涉对象：认领存在（`refs/aria/coordination` 的 `claims/023236f2/s-28df@0755.yaml`，track `secret-guard-w10-failclosed-narrowing-023236f2`，`linked_issue: 10CG/aria-plugin#217`，phase A.1），但页眉没记录（WP-A 的页眉有「认领」行）。
- **建议改法**：加「不变量继承」一行，列出沿用 WP-A 的 INV-4 / 5 / 6 / 7 并写出 INV-6 与 INV-7 的内容；页眉补认领行。

---

### F-12  发布同步面的转述与实践不符

- **type**：issue　**severity**：Minor　**category**：documentation
- **scope**：§Impact 发布同步面（`:362`）
- **针对**：**v2 新文本**（引用 CLAUDE.md 的清单，转述时漏项）。
- **一句话**：发布同步面的转述漏了 i18n README 与 CLAUDE.md 项目状态行。
- **证据**：主仓 `878f8d9`（v1.76.1，「16 版本点」）实际改了 9 个文件：`CLAUDE.md`（项目状态段 2 行）、`README.md` / `README.zh.md` / `README.ja.md` / `README.ko.md`（徽章 + Plugin Version 行 + translated-from 标记）、`VERSION`、`docs/architecture/system-architecture.md`、`docs/architecture/version-scheme.md`、gitlink。aria 侧 `59e333c` 改了 6 个文件（含 `README.zh.md`），CLAUDE.md 写的是「5 文件」。规格转述的清单没有 i18n README 和 CLAUDE.md 项目状态行，而同一句里引用的 `i18n-readme-translation-currency` 正是兜底这一项。
- **建议改法**：写「按 `878f8d9` 的 16 版本点」，或补全清单。

---

### F-13  Rule #6 处置未逐 hunk 说明面向 AI 的文字

- **type**：issue　**severity**：Minor　**category**：documentation
- **scope**：§Impact Rule #6（`:363`）
- **针对**：沿用，v2 未改。
- **一句话**：Rule #6 处置未逐 hunk 说明面向 AI 的文字。
- **摘要**：WP-A 的 owner 裁定是「hook substitute 框定，提示文案 hunk 单独判」（`openspec/changes/secret-net-l3-and-bypass-paths/proposal.md:12`），#228 的 `rule6_note` 点名新增的 BLOCKED kind（其 `detailed-tasks.yaml:7`）。本规格只写「只改 hook，按 substitute 处理」，没有说明 `longline` 模板（`:217–232`，含「Split it … Write / Edit tool instead of a heredoc」这类对 AI 的指令）与两条改写的 `Limit hit:` 原因串（`:208–209`）怎么判。
- **建议改法**：`rule6_note` 里点名这三处，给出逐 hunk 结论（可判描述性或「套件覆盖外」并开套件缺口 issue）。

---

### F-14  审计叙事与交付面同居一文

- **type**：risk　**severity**：Minor　**category**：documentation
- **scope**：§R1 处置对照（`:429–456`）；Why 的 v1 前提叙述（`:49–61`）；行内的 R1-A / BA-F / CR / KM 回链
- **针对**：**v2 新文本**。
- **一句话**：R1 处置对照与行内回链使审计叙事与交付面同居一文。
- **摘要**：24 行处置对照加十余处行内回链，是 append-only 的审计叙事，与收敛型的交付面（What / SC / Decision）放在同一份文件里。memory `feedback_audit_trail_must_not_live_in_spec.md` 的症状是：每轮修订的 Major 主要落在计数、交叉引用、订正留痕上。本轮 F-06 / F-09 / F-10 就有一半落在这类文本上，R2 处置对照再加进来只会更多。R1 汇总里已有「主控处置」表，处置对照与它重复。
- **建议改法**：处置对照移出为独立 append-only 文件（或只留在审计汇总里），Spec 正文只留 Decision record；机械搬运，不重写。

---

### F-15  交叉引用不是双向的；#229 / #230 未被提及

- **type**：issue　**severity**：Minor　**category**：documentation
- **scope**：页眉「关联」（`:7–11`）；Decision 9；Why
- **针对**：**v2 新文本**。
- **一句话**：交叉引用不是双向的，#229 / #230 未被提及。
- **摘要**：本规格指向 #154 / #216 / #219 / #228；反向：#217 没有任何评论指向本 Spec（对照 #228 在 Spec 起草时贴了说明），#228 的 issue 与 proposal 没有 Decision 9（见 F-04）。#229（风险行右边界只认空白 / 行尾）与 #230（扩展只替换前 64 处命中）完全没被提及。这两条是既有检测缺口，放宽尺寸闸门后，它们覆盖的流量变多（此前被尺寸拦住的、含变量的大命令现在进入完整判定），两条 issue 都写了「不在 #228 范围内」，也没提 #217。
- **建议改法**：页眉「关联」加 #229 / #230，并在「放宽面」里注明大命令现在同样受这两个已知缺口影响；#217 贴一条指向 Spec 与 owner 裁定 A / B / C / D 的评论。

---

### F-16  时间文案在硬截止路径上不准确

- **type**：issue　**severity**：Minor　**category**：implementation
- **scope**：§What 5 文案表（`:210`，「时间模板，不变」）；`secret-guard.sh:834–836`、`:614`
- **针对**：**v2 新文本**（硬截止是 v2 新增的触发路径，文案沿用）。
- **一句话**：硬截止路径上的时间文案不准确（「Nothing was matched」；预算值 4 s 对实际 3 s）。
- **摘要**：
  1. 时间模板写「Nothing was matched. The secret scan did not finish」。硬截止杀死的判定可能已经命中规则、卡在 credit 里；「开始前已无时间」的路径则根本没开始。这与 R1-A7 指出的 oversize 文案自相矛盾同形。
  2. 模板打印 `(${_SG_TIME_BUDGET}s)`；预算环境变量为 4 时，文案写 4 s，而 `_sg_vx_big` 用 `min(预算, 3)`，实际 3 s 截止。
- **建议改法**：硬截止路径用独立的 `kind`（或在模板里按原因分支），文案去掉「Nothing was matched」，时间值用实际截止值。

---

### F-17  未实测平台的默认态是 owner 的取舍，规格交给了执行席

- **type**：decision　**severity**：Minor　**category**：architecture
- **scope**：§不变量（`:257`）；TASK-004（`:425`）；§Owner 裁定点（`:267–274`）
- **针对**：**v2 新文本**。
- **一句话**：未实测平台的默认态是 owner 的取舍，规格交给了执行席。
- **摘要**：规格自己写「Windows / macOS 上 `kill -KILL` 若不能及时终止判定，大副本会退回 fail-open，比基线差」，却把处置写成「发版前要么实测，要么在 CHANGELOG 申报」。选后者就是在未验证的平台上带着放宽发版。memory `failopen-posture-owner`：安全 fail-open / closed 姿态归 owner；「无法验证就放行」违反 fail-closed 不变量。TASK-005 虽是 owner 门，但裁定点表里没有这一项，owner 看不到这是一个待决选项。
- **建议改法**：裁定点表加一行 E，列选项：(i) 实测前不发；(ii) 未验证平台保持尺寸拦（需要一个运行时自检：起一个后台 `sleep` 并 `kill -KILL`，约 2 ms）；(iii) 申报后发。

---

### 已核实无误（不构成 finding）

- 行号：`:178`、`:594–596`、`:607`、`:614`、`:645`、`:659`、`:666`、`:668–669`、`:685`、`:694`、`:701–703`、`:725`、`:728`、`:740`、`:744`、`:748–750`、`:826–828`、`:926`、`:1506–1509`、`:1534–1536`、`:1554–1555`、`:1563`、`:1581` 与基线一致；测试侧 `:2552–2554`、`:2566`、`:2586`、`:2606`、`:2634`、`:2676`、`:2683` 一致。偏差见 F-06。
- `traffic/deadline-helper.sh` 与 proposal `:131–159` 的参考实现逐字节一致（`diff`，仅差文件首行说明）。
- Why 表数字与 `W-summary.txt` 吻合：137 / 1、增长分桶 2 + 60 + 64 + 10 + 1 = 137、0.194 s / 0.97 s、31 条命中、566 / 4457、「没有超过 8192 的行」。E12：739 / 130（17.6%）/ 138。`_sg_compute_credit` 里恰有 14 处 `_sg_line_match`。
- `:666` 的死代码判断成立（空值在 `:646`、`:660` 已跳过，链式代入只会把非空串换成非空值）。
- 草稿在 bash 3.2.57 与 5.2.15 下 `bash -n` 通过；新函数与常量放在源码闸门之上，普通 `source` 后都存在（按 W14 闭包检查的口径自检；我没有运行套件里的 SC-30 本身）。
- 扩展门那一行与基线逐分支等价（按代码推演，非实跑），唯一例外是人造角落：中间副本超过 8192、后续替换又缩回 ≤ 8192（需要数百字符的变量名），此时基线拦、新版去判最终副本。
- `SC-N` 命名空间无撞号；markdown 表列数一致；全文无带圈数字与裸控制字节。
- standards 三处计数在 `:23`、`:316`、`:352`，现为 822 / 816；套件头 `:11` 为 831 / 825；SC-13 机制如上。
- issue 事实：#217 正文是三项加 count 轴加小项，TASK-006 的对账映射正确；#228 评论 29957 写明「下一步做 #217」；#229 / #230 存在；#216 收口评论写明 remaining → #228；#219 评论含 2.6× 数据。

### 未核实

- Windows MINGW64、真 macOS（Apple 构建的 bash 3.2.57 / BSD 正则）。
- 真实命令语料上的 SC-N16 结果（不读语料）。
- 其余席位负责的算法正确性项，我只在复现 F-01 / F-02 时顺带跑了：硬截止 helper 在 3.2.57 下端到端可用（`run_adv.sh` 第三参数），没有做更多对抗构造。

## Verdict

**FAIL**：1 Critical（F-01）、4 Major（F-02–F-05）、12 Minor（F-06–F-17）。

若主控把 F-01 按 R1-A4 先例降为 Major，则为 PASS_WITH_WARNINGS（5 Major），但「时间上不新增 fail-open」的措辞仍须修改。

## 轮次记录

- **席位**：knowledge-manager，全新实例，未参与第 1 轮。
- **读过的材料**：BRIEF-R2、proposal v2、R1 汇总、R1 KM-F-11 一小段（核对「版本行」含义），源码与证据文件，上述 Forgejo issue。
- **独立性声明**：我没有读其他席位的 R2 报告。唯一的例外是一次 grep 的路径过滤写错，输出里带出了另外两席 R2 报告各一行：code-reviewer 一行关于 standards 三处计数与套件头的核对，backend-architect 一行关于行号核对的总评。我没有据此下结论：standards 计数与行号都由我独立核对，结果见 F-06 与「已核实无误」；是否与那两行指向同一处，我不知道。另外，读 R1 KM-F-11 那一小段时，上下文带出了 R1 KM-F-10 / F-12 的片段，属第 1 轮材料，不涉及本轮其他席位。
- **只读纪律**：没有改 proposal、代码、仓内文件；没有 commit；Forgejo 只做了 GET；临时文件都在 scratchpad。
- **资源纪律**：所有实验带 `taskset -c 0,1 nice -n 19`；宿主 loadavg 2–5（4 核），故墙钟数据有浮动，CPU 时间更可靠，正文已分开标注。
- **本轮产出**：1 Critical / 4 Major / 12 Minor。其中 F-01、F-02、F-03、F-05 带实测证据，F-04 带 Forgejo 只读证据。

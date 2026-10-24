# TASK-002 第三步 3c 任务书：关门臂的基线参照核对；6 组放宽支的截止回落判法；两处小改（10CG/aria-plugin#217）

你是 TASK-002 第三步 3c 段的执笔席（全新实例）。主控不亲写测试代码；你按本任务书改套件、helper 与 v31 的 run-suite.sh，在实现上实跑，主控之后独立复核。全部坏实现与扰动、两种环境错误、基线红集在套件上的复跑，以及 run-mutants.sh 的套件模式，由下一段 3d 做，**不在本段**。
3a（移植 136 个编号）提交在 aria 分支 `feature/secret-guard-w10-failclosed-narrowing` 的 `3a64827`，3b（W10 批移到套件最前、6 组既有用例分两支、注释与标题、commentsync 套件一侧）提交在 `fee1a65`；worktree 当前就在 3b 提交上，工作区干净。

## 规格与材料（只按行号读需要的段）

- 计划 `/home/dev/Aria/openspec/changes/secret-guard-w10-failclosed-narrowing/detailed-tasks.yaml`：`grep -n` 找 INV-7、INV-9；TASK-002 notes 里的「口径 (ii) 的漏洞」「3a 主控裁定」「第三步分段调整」三条与 3b 的两条；design「套件 (1) 补充」；acceptance 的前三条与坏实现那条。
- v31 `/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/`：`run-suite.sh`、`mutants.py`（只读头注释，以及 `designated.tsv` / `reasons.tsv` 怎么写出）、`README.md`。
- 主控复核：`/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/b2/t002c-verify/VERIFY.md`（BI-8 的实测与「代码审读」）、`.../b2/t002d-verify/`（3b 的复核，含 21ab 的计时探针 `probe.txt`）；3b 报告 `.../b2/T002c-3b-report.md` 第 2、6 节。
- 套件：worktree `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/wt217/aria/hooks/tests/secret-guard.test.sh`（**不要整份读**）。W10 旧用例块里 6 组的放宽支与新 helper（`wpa_x_longline`、`wpa_x_hit`、`wpa_rx6`）在约 `:2887-3110`。移植块里要改的是 `sg_w10_run`、`sg_w10_identity`、`sg_w10_deadline`、`sg_w10_outcome` 与 `sg_w10_cases` 里端到端那一段的调用行，`grep -n` 定位。helper `hooks/tests/lib/secret-guard-w10-direct.sh` 里要改的是 `fbt`（V6-S20 / S21）。

## 要做的

0. **先跑现状（先写预期再测）**：在 worktree 里 `SG_W10_ONLY=.` 跑一次（PATH 上的 bash），再经 `v31/run-suite.sh` 用 `SG_W10_ONLY=^(V9-E12-vmax-unchanged)$` 跑 BI-8。预期写进报告后再跑：前者 136 PASS；后者 V9-E12 PASS（主控复核已实测的漏抓）。
1. **关门臂的基线参照核对**（计划 notes「口径 (ii) 的漏洞」的补法）：
   - 对象：每一处跑关门臂的调用——端到端的逐字节比对、截止、结局三类（含它们在非放宽平台上回落成逐字节比对的那一支），以及 helper 的 `fbt`。`V2-E17` 是单臂、已判绝对结局，不在内。
   - 量表：对每一处，用**完全相同**的输入、变量与关门方式，在 59e333c 的 hook 上实测关门臂的结局（退出码与 `sg_w10_kind` 的文案种类；`fbt` 是 `_sg_vx_pass` 的返回值与 `kindf`）。基线取 `git show 59e333c:hooks/secret-guard.sh`，先断言 sha256 前缀 `e83c5e30f2cc`（INV-9）。5 个 bash 各量一遍；若某处因 bash 而不同，按 bash 分开记，并在报告里解释。端到端这几类的细节里本来就写着 `gate-closed rc=<rc> <kind>`：经 `run-suite.sh` 对 59e333c 跑一次 `SG_W10_ONLY=.` 并开 `SG_W10_LOG`，就能取到基线一侧，不必另写测量代码；`fbt` 的细节里没有文案种类，需要补进细节或另量。再在实现上量同一张表：两者必须逐处相同，不同就停下写进报告（那说明关门臂没能复现基线，口径 (ii) 本身不成立）。
   - 写进套件：每处调用带上它的参照结局（参数或按编号查表，择一，写清楚）。跑完关门臂后先核参照：对上了再做原来的判定；对不上时，若关门臂撞上 12 s 超时或出现时间文案，按计时类处理（与 `sg_w10_slow` 同一口径），否则记 `FAIL [reference]`，细节写出实测与参照。helper 的 `fbt` 同样加 `[reference]`。
   - 只加检查，不改 v31 的任何期望值与原因标签。套件块首注释与 helper 头注释写明 `[reference]` 是什么、为什么有。
2. **6 组放宽支的截止回落判法**（主控裁定，技术口径，不动姿态；3b 报告第 6 节第 1 条）：
   - 背景：放宽支里副本超过 8192 的命令（触发点上的那些：21ab 三条、21ac 的 4096 字符 for 表、21ag、21aj 三条、21al 与 21ao 的 8193），要求放宽重跑在 `_SG_P0` + min(预算, 3) s 内跑完。主控实测 21ab 两条放行命令在负载 1.2-1.6 时整个 hook 耗时 2.37-2.58 s，同一命令关门时也要 2.39-3.08 s：时间主要花在先跑的基线那一遍（`b2/t002d-verify/probe.txt`）。主机慢时 hook 按 What 4 回落成基线的拦截（P3、P6）；`_sg_relax_left` 只在截止已过时才关门，所以因时间回落时墙钟约在 3 s 或之后。
   - 不加负载门：6 组排在套件后部，3b 的 7 次整轮结束时负载都在 2.21-4.13，加了负载门它们几乎每轮都 SKIP，等于没有这组断言。
   - 判法：触发点上的每条命令在放宽支里只跑一次 hook，用 `EPOCHREALTIME` 量墙钟。放宽支断言成立，就通过。否则，若同一份输出满足基线支对这条命令的断言（else 分支里那条 `wpa_x_toolarge` 及其 limit 行）、且墙钟 >= 2.85 s，也通过，记一次「截止回落」。两者都不成立就 FAIL，细节写出两套断言各自不符的项与墙钟。两套断言在同一份输出上求值，只记一次结果。触发点之下的命令（`wpa_x_hit` 那几条）不变。
   - 这些 hook 调用清掉 `SECRET_GUARD_TIME_BUDGET_S`（与移植用例一致），使截止固定为 3 s、下界 2.85 s 成立。
   - 计数不变（每组仍计一次）；6 组那一行 Summary 加上「截止回落 N / M」。改动处的注释写明这条判法与理由。
   - 构造验证（只在 `run-suite.sh` 的副本里做，不改 worktree）：
     - hook 副本里让 `_sg_relax_ok` 恒返回 1（准入门恒关）：放宽支的触发点命令立刻得到基线拦截、墙钟 < 2.85 s，6 组中有触发点命令的各组都须 FAIL；
     - 另一份副本只把放宽重跑拖过截止（例如在作业入口加 `sleep 4`）：6 组须全部 PASS，且截止回落数等于触发点命令数。
3. **两处小改**：`v31/run-suite.sh` 首行另记 helper 的 sha256 前缀；`hooks/tests/lib/sg-shim/delay-first` 的头注释改成套件里的用法（逻辑一字不改）。
4. **实跑**（输出全落 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/t002e/`）：
   - 实现：`SG_W10_ONLY=.` 下 5 个 bash 各一轮，全 PASS（3.2 上 58 个 SKIP [platform]），计时批判过。
   - 坏实现抽查：`v31/mutants.py` 从实现构造坏实现（写到你的输出目录），经 `run-suite.sh` 加 `SG_W10_ONLY=<指定用例>` 跑 BI-8、BI-5、BI-45（指定用例都走关门臂）。要求：BI-8 由 `V9-E12` 以 `[reference]` 抓住；BI-5、BI-45 照旧按 `reasons.tsv` 的原因抓住；同一批用例在实现上全 PASS。
   - 整轮：worktree 里 PATH 上的 bash 整轮一次（低负载）：FAIL 0，计时批判过，SC-13 绿，6 组那行显示截止回落数。
   - 第 2 条的两个构造。

5. **报告**：写到 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/T002c-3c-report.md`（中文），内容：
   - 改了哪些文件；
   - 参照表（每处：编号、输入、变量、59e333c 上的结局、实现关门臂的结局，按 bash）；
   - 各轮结果与首尾负载；
   - 坏实现抽查与两个构造的结果；
   - 未做或拿不准的项。

## 纪律

- **工具调用上限 70 次；到第 55 次时停止新工作，把已完成的写进报告再收尾。** 上限是硬的。
- **输出纪律**：跑套件与坏实现的输出一律落文件，对话里只看 `tail`、`grep -c` 与不超过 20 行的 FAIL 或判定行；读文件先 `grep -n` 再按行号读，每次不超过 80 行；不要 cat 整份套件或 hook。
- **只改这些文件**：worktree 的 `hooks/tests/secret-guard.test.sh`（移植块，以及 W10 旧用例块里 6 组放宽支的断言与它们的 helper；基线支一字不改）、`hooks/tests/lib/secret-guard-w10-direct.sh`、`hooks/tests/lib/sg-shim/delay-first`（只动头注释）；主仓的 `v31/run-suite.sh`。不改 hook，不改 `v31/run-mutants.sh`（3d 的事）；不 commit。若发现 hook 的缺陷或规格矛盾，停下写进报告。
- 命令加 `taskset -c 0,1 nice -n 19`，同一时刻只跑一个重实验。开跑前看 `/proc/loadavg`，一分钟负载高于 1.2 先等（等的循环要显式 `return 0`），连续等 30 分钟仍高就先做不依赖墙钟的部分，并在报告里附读数。
- Rule #7：不打印任何像凭据的值；凭据形字符串只在运行时拼装。会话自带的旧版 secret-guard 会拦截含凭据形文本或 `| jq …` 一类写法的 Bash 命令行（含 heredoc 正文）。把文本写进文件（Write / Edit 工具不受它影响），或运行时拼装；不要用 `# guard:ack` 绕过。
- 进程只按你自己记下的 PID 清理，禁止 `pkill -f` 一类按模式批量杀。
- 规格有两种读法、或照做会违反某条 INV 时，停下写进报告，不要自行选择。

最后一条消息用中文：各项结论一句话、报告路径、未完成或拿不准的项、用了多少次工具调用。

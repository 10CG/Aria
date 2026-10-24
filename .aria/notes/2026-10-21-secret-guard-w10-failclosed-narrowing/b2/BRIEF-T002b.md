# TASK-002 第二步任务书：按 post_planning R2 补强可执行验收（10CG/aria-plugin#217）

你是 TASK-002 的执笔席（全新实例）。主控不亲写验收代码；你按规格补强 `v31/` 下的验收脚本，在实现与基线上实跑，主控之后独立复核。

## 规格与材料（先读）

- `/home/dev/Aria/openspec/changes/secret-guard-w10-failclosed-narrowing/detailed-tasks.yaml`：INV-1、INV-2、INV-7、INV-8，以及 TASK-002 的「R2 补强」(a)–(f) 与验收。这是你的工作清单，逐条做。
- `/home/dev/Aria/openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md`：What 1 补充（准入门五个参数）、What 7 补充、Success Criteria、SC 表与 BI 表。
- R2 汇总：`/home/dev/Aria/.aria/audit-reports/post_planning-R2-1792689337848-secret-guard-w10-failclosed-narrowing-aggregated.md`，重点读「非作者变异测试汇总」与 PP2-A 到 PP2-T、PP2-m 各行；需要细节时按簇号回链到同目录五份席位报告。
- 现有验收：`/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/`（`README.md`、`sc-cases.sh`、`sc-direct.sh`、`shapes.py`、`shim/`、`mutants.py`、`run-mutants.sh`、`commentsync.py`）。
- 五席的探针与坏实现（只读，取材料用），根目录 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217pp-r2/`：
  - `qa-engineer/`：`xp-newcases.sh`（17 个确定性直调探针）、`mkmut.py`、`mkmut2.py`、`mut/`、`predictions*.tsv`、`xp-*.sh`。
  - `backend-architect/`：`mut.py`、`mut/`、`demo78.sh`、`stub-*.sh`、`demo-all.sh`、`demo2.sh`。
  - `tech-lead/`：`mkmut.py`、`mut/`、`prereg-mutants.txt`、`probes*.py`、`probe-run.sh`。
  - `code-reviewer/`：`mut/MA–ME.sh`（相对原型各一处改动，用 diff 取改动）、`probes/mk.py`、`probes/run.sh`。
  - `knowledge-manager/mk_km_mutants.py`。

## 被测对象

- 实现：worktree `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/wt217/aria/hooks/secret-guard.sh`（已提交到 feature 分支：`96f9083` What 6，`21a37ea` 原型 + What 1 补充 + What 7 补充；sha256 前缀 `af4658b6f935`；已推 origin）。只读，不改，也不要在这个 worktree 里 commit。
- 基线：`git -C /home/dev/Aria/aria show 59e333c:hooks/secret-guard.sh`（INV-9）。

## 要做的

1. 按 TASK-002 的 R2 补强 (a)–(f) 改 `v31/` 下的脚本（INV-2 允许）：`sc-cases.sh`、`sc-direct.sh`、`shim/delay-first`、`shapes.py`、`mutants.py`、`run-mutants.sh`、`commentsync.py`。`RELAX` 的推导要与收紧后的准入门同一判据（x86_64 的 GNU/Linux 构建、bash 5.0–5.3、不在 WSL 里）。新用例沿用 `V<k>-…` 编号，接在现有编号之后，不改既有编号。
2. `mutants.py`：坏实现改为从实现构造（不再从原型），BI-1–23 照旧；五席漏网的坏实现从 BI-24 起编号，每个写明「改动 / 指定用例 / 原席位编号」；BI-17 另拆三个各漏一处；QA-M29 不入 BI，另写一轮常量扰动（`_SGV_GMAX` 改 8190、`_SGV_LMAX` 改 8200）。每处替换断言恰好命中一次。
3. 实跑并记录（输出写到 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/t002b/`）：
   - 实现在 5 个 bash 上（`/usr/bin/bash` 与 `/home/dev/.aria/tools/bash-{5.0.18,5.1.16,5.3.20,3.2.57}/bash`）整轮全绿；3.2 走 identity。
   - 基线的红集，分「缺失（127）」与「判错」两栏。
   - 每个坏实现在其指定用例上变红，红的原因与指定的一致；无关断言碰红不算。
   - 两种环境错误（`SC_BASH` 指向不存在的文件；`sc-direct.sh` 一启动就崩）下报 SETUP 或 FAIL、退出码非 0。
   - commentsync：实现上 target 为 GREEN；对未改动的基线 hook 做「插字符绕过」与「整块删除」两种构造都报 RED。
   - 每一轮开始与结束各记一次 `/proc/loadavg`；计时类判定按 INV-7，负载 >= 2 时作废重跑，并在报告里说明。
4. 报告写到 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/T002b-report.md`（中文）：逐条对应 R2 补强 (a)–(f) 与 PP2 簇号，说明改了什么、用哪条用例钉住、在哪个坏实现上验证变红；列出新用例编号清单、BI-24 起的清单、各轮结果与负载、未做或拿不准的项。

## 纪律

- 只改 `v31/` 下的验收脚本，不改 hook，不改仓内其他文件，不 commit。
- 命令加 `taskset -c 0,1 nice -n 19`；同一时刻只跑一个重实验；单个实验不超过约 2 分钟（整轮 `sc-cases.sh` 约 45–60 s）。
- Rule #7：不打印任何像凭据的值；凭据形字符串只在运行时拼装。会话自带的旧版 secret-guard 会拦含凭据形文本或 `| jq …` 一类写法的 Bash 命令行（含 heredoc 正文）：把文本写进脚本文件，或运行时拼装；不要用 `# guard:ack` 绕过。
- 进程只按你自己记下的 PID 清理，禁止 `pkill -f` 一类按模式批量杀；残余进程用例的桩参数改成每轮唯一之后，自己的运行也不会误伤别人。
- 规格有两种读法，或照做会违反某条 INV 时，停下写进报告，不要自行选择。
- 上下文接近 40 万 token 时，先把已完成的部分写进报告再收尾。

最后一条消息用中文：各项结论一句话、报告路径、未完成或拿不准的项。

## 第一步交回时暴露的问题（必须处理）

第一步的报告：`/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/T002a-report.md`（先读，含「第二轮」一节）。

1. **直调段被静默吞掉**：`sc-direct.sh` 开着 `set -u`，`V2-G2` 按旧签名只给 `_sg_relax_platform` 传三个参数。旧版函数体里的 `"$4"` 没有缺省，第一行就让脚本整体中止，除 `V2-G1` 外 62 行直调用例都没有输出，`sc-cases.sh` 也不报错。规格已改成每个参数带缺省，但用例这边要：`V2-G2` 按五个参数改写；R2 补强 (d) 的 `sc-direct.sh` 末行哨兵与「应出现的用例编号清单」必须让这类整段消失变成 FAIL。改完后，把旧版函数体（无缺省）临时放回一个副本上跑一次，证明整段消失会被报成 FAIL。
2. **期望判定**：`sc-cases.sh` 的 `RELAX` 仍按 `*-linux-gnu*` 推导，要改成与收紧后的准入门同一判据（x86_64 的 GNU/Linux 构建、bash 5.0–5.3、内核串不含 microsoft 或 WSL、没有 WSL 标记）。
3. **WSL 环境变量**：`run()` 起 hook 时要清掉 `WSL_DISTRO_NAME`、`WSL_INTEROP`（只有专门测 WSL 的用例才设）；否则在 WSL 里跑套件，期望与实际会对不上。
4. **commentsync**：目前不检查 What 7 补充的四处，补上。
5. **负载**：第一步全程负载 5.7–8.8，计时结论都要在低负载时重跑（INV-7）。开跑前先看 `/proc/loadavg`；高于 2 时先做不依赖墙钟的部分（直调、静态、坏实现的逻辑红），计时类留到负载回落后整批跑，并在报告里记下等待与重跑。

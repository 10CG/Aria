# TASK-003 第二段任务书：对抗耗时矩阵（10CG/aria-plugin#217）

## 防御语境（先读）

这是对一个**防泄密安全 hook**（Claude Code 的 PreToolUse secret-guard）做**性能对抗测试**：用刻意构造的大命令测它的硬截止是否守得住，目的是证明 hook 不会因为命令形状而拖过时间上限（拖过 Claude Code 的 5 s 会变成放行）。输入只在 scratchpad 生成、只喂给 hook 副本；不涉及真实凭据，凭据形的路径一律运行时拼装（参考 `v3/gen-v3.py` 的写法）。

你是 TASK-003 的 QA 席（非作者），第二段，全新实例。第一段（独立坏实现）已完成：31 个坏实现全被抓住，补了 5 个直调用例 V14-*，交付在主仓 `v31/impl/`（`w14.sh`、`w14-mutants.py`、`W14-independent-mutants.txt`）；本段不碰那些文件，也不改套件。

## 对象与判据

- 实现：aria worktree `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/wt217/aria` 的 `hooks/secret-guard.sh`（sha256 前缀 `af4658b6f935`）。
- 判据（计划 TASK-003 design4 / acceptance2，与 W12 第 1 节同一公式）：每个结局的墙钟 W <= max(T_trigger, 3 s) + 0.3 s。T_trigger 取 `v31/mkdbg31.py` 埋点副本的 `relax-start`（放宽重跑开始的时刻，相对同一次运行的起点）；没有进入重跑的结局不受这个上界约束（与 `v31/run-evidence.sh` 第 47 行的 awk 相同：t 取 W 本身）—— 它们的耗时属于基线那一遍，不在本变更范围内（基线首遍的超时缺口见 `10CG/aria-plugin#228`），但照样逐条记下 W，超过 3 s 的在报告里单列。
- 材料：`/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/` 下 `v3/gen-v3.py`（8 个已有形状）、`v3/matrix.sh`（端到端一次调用的量法）、`v31/mkdbg31.py`、`v31/replay138.sh`（埋点副本的读法）、`v31/run-evidence.sh` 第 40-52 行（W12 的判法）。

## 要做的

1. 用 `mkdbg31.py` 从实现生成埋点副本，`diff` 核对只多三行探针。
2. 形状：`gen-v3.py` 的 8 个，加你自己想的至少 8 个（写成 `w14-shapes.py`，同样运行时拼装凭据形路径）。自己的形状要冲着放宽重跑的开销去：例如多个各自超过 8192 的分段（每段都可能进重跑）、增长量贴着 `_SGV_GMAX`、长行贴着 `_SGV_LMAX` 上下各一、for 列表与替换次数在旧上限附近、多字节字符（字符数与字节数不同）、整串与分段混用、基线那一遍本身就慢的命令（触发点出现得晚）。每个形状在清单里写明想测什么。
3. 量：每个形状在 PATH 上的 bash（5.2.15）跑 5 次，记 rc、文案种类、W、T_trigger、上界、是否越界；再挑最重的 4 个形状在 `/home/dev/.aria/tools/bash-5.0.18/bash` 与 `bash-5.3.20/bash` 上各跑 3 次。INV-7：同一时刻只跑一个重实验，每批开始与结束各记一次 `/proc/loadavg`，任一读数 >= 2 即作废重跑；开跑前一分钟负载 < 1.2。
4. 若出现越界：先在低负载下复跑确认；仍越界就停下写进报告（那是实现的问题，不是测试的问题），不要改 hook。

## 交付

- `/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/impl/w14-matrix.sh` 与 `v31/impl/w14-shapes.py`（新建），生成 `v31/impl/W14-timing-matrix.txt`：首行记日期、负载与实现、埋点副本、`gen-v3.py`、`w14-shapes.py` 的 sha256 前缀（INV-8）；之后每个形状一节：想测什么、每次的 rc / 文案种类 / W / T_trigger / 上界 / 越界否，各批首尾负载；末尾一行「every outcome within max(trigger, 3 s) + 0.3 s: N of M」。
- 报告 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/T003b-report.md`（中文）。

## 纪律

- 工具调用上限 50 次；到第 40 次时停止新工作，把已完成的写进报告再收尾。
- 输出纪律同前（输出落文件；对话里只看 tail、grep -c 与不超过 20 行的判定行；大文件先 grep -n 再按行号读）。
- 只改：scratchpad 的 `r217impl/t003b/` 下随意；主仓新建的 `v31/impl/w14-matrix.sh`、`v31/impl/w14-shapes.py`、`v31/impl/W14-timing-matrix.txt`。不改 hook 与套件；不 commit。
- 命令加 `taskset -c 0,1 nice -n 19`；Rule #7 与 PID 清理同前；规格有两种读法时停下写进报告。

最后一条消息用中文：各项结论一句话、报告路径、未完成或拿不准的项、用了多少次工具调用。

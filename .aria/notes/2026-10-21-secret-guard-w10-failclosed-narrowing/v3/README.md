# #217 v3 原型证据（W8–W12）

本目录是 proposal v3「设计钉死」所依据的可运行原型与实测结果。原型由 `mkv3.py` 从基线 hook 机械生成，规格里的参考实现就是 `W8-v3.diff`；所有 `W*.txt` 都由同目录脚本生成，不手写、不手改。命令原文不入库：真实流量只出汇总与编号。

| 文件 | 内容 | 生成方式 |
|---|---|---|
| `W8-v3.diff` | 原型相对基线的全部改动（+106 / −6 行） | `python3 mkv3.py <基线 hook> v3.sh && diff -u` |
| `W9-suite.txt` | 套件在基线与原型上各跑一遍：基线 813/814，原型 807/814，多出的 6 个失败即 21ab、21ac、21ag、21aj、21al、21ao | `run-w9.sh <基线 hooks 目录> <工作目录>` |
| `W10-mechanism.txt` | 放宽重跑的机制单测：用桩判定替换 `_sg_vx_pass`，截止设为 1 s，8 个截止场景 + 8 个准入门场景 | `run-w10-w11.sh`（调用 `v3unit.sh`） |
| `W11-adversarial.txt` | 对抗输入矩阵（e2e）：apply 重负载三种、缩短类、segfinding、f5like、扩展项目；另附套件 21ab/21ac/21al 形状 | `run-w10-w11.sh`（调用 `gen-v3.py`、`matrix.sh`、`probe21.sh`） |
| `W12-real-traffic.txt`、`W12-replay-138.tsv` | 真实流量：W1 的 138 条逐条回放；放宽类之外 300 条逐字节对比；bash 3.2 下 40 条逐字节对比 | `run-w12.sh`（调用 `replay138.sh`、`ident.sh`、`ident32.sh`），`TRAFFIC_DIR` 指向冻结语料 |
| `W12b-rerun.txt`、`W12b-replay-138.tsv` | 同一原型对 138 条的第二次独立回放，列出两次结局不同的命令 | `run-w12b.sh` |
| `W10b.txt` | 回落文案与基线逐字节相同（P6）；`nocredit` 路径保留 W12 中和（P10） | `w10b.sh` |

辅助：`mkdbg.py` 生成只用于计时的埋点版原型（每个埋点都保留它前一条语句的返回码）；`ident-300.lst`、`w1-sample40.lst` 是抽样清单（只有编号）。`commentsync.py` 核对 proposal What 7 的注释封闭清单；`fill.py` 由 `proposal-template.md`（带占位符的 proposal 正文）加本目录证据生成 proposal：`python3 fill.py proposal-template.md <v3 hook> W8-v3.diff W12-real-traffic.txt <out>`，代码块、注释清单表与真实流量两行都从证据机械填入。

## 本机依赖（R2-A24）

- Linux、bash 5.2.15（`EPOCHREALTIME`）；`/proc`；coreutils `sleep`（支持小数秒）；`taskset`、`nice`、`jq`、`python3`、`shuf`、`sha256sum`、mawk 或 gawk。
- bash 3.2.57 是本机自建的 Linux 版（`/home/dev/.aria/tools/bash-3.2.57/bash`），不在仓里，也没有构建配方；它只用于「3.2 下与基线逐字节相同」这一项（W12 第 3 节）。
- `TRAFFIC_DIR`：真实命令语料，按 `../traffic/manifest.py`、`../traffic/refreeze.py` 由本机会话记录抽取并按 W0 的 sha256 复原，放在仓外。
- W9 的两份套件运行都在非 git 副本里进行，所以依赖 `git show` 读旧版 hook 的 17 个用例在两边都不运行（实跑 814，头注释写 831；两边相同，不影响对比）。
- 时延数字受宿主负载影响（共享 4 核宿主，load 2–5），每份输出的页眉都记了当时的负载；结论只看结局与相对关系，不看绝对秒数。

# 10CG/aria-plugin#217 v3.1 原型与证据（W8、W9、W11–W13）

本目录是 proposal v3.1 的设计钉死所依据的可运行原型、可执行验收与实测结果。v3 的原型与证据在 `../v3/`，那是 post_planning R1 审的对象，保持原样。所有 `W*` 文件都由本目录的 `run-evidence.sh` 生成，不手写、不手改；命令原文不入库，真实流量只出汇总与编号。

## 文件

| 文件 | 内容 |
|---|---|
| `mkv31.py` | 从基线 hook 机械生成 v3.1 原型（先断言基线 sha256 前缀 `e83c5e30f2cc`，每处替换必须恰好命中一次）；第 10 步整块重写 What 7 的 8 处 hook 注释 |
| `sc-cases.sh`、`sc-direct.sh` | 验收用例（proposal 的 Success Criteria）：直调（准入门、截止、桩判定下的作业机制、增长、计数、只匹配规则）、端到端（用被测的 bash 执行 hook）、静态检查。输出每条一行 `PASS/FAIL/SKIP <编号> <细节>` |
| `shapes.py` | 端到端用例的命令文本；凭据形路径运行时拼装，hook 只判文本、从不执行命令 |
| `shim/delay-first`（`shim/jq`、`shim/sed`） | 在已知位置注入固定延迟：`jq` 的首次调用是 stdin 解析（锚点之后、触发点之前），`sed` 的首次调用是作业里第一份拦截文案的命令回显。计时判据由它决定，不依赖本机速度 |
| `mutants.py`、`run-mutants.sh` | 23 个坏实现（v3.1 + 一处改动）及每个的指定用例；逐个跑 `sc-cases.sh` 并判定是否被抓住。作者自建，是对用例的自检，不替代 TASK-003 |
| `commentsync.py` | What 7 的块级核对（`--hook-only`、`--suite-only`；baseline / target 模式） |
| `mkdbg31.py`、`replay138.sh`、`ident.sh`、`ident32.sh` | W12：埋点副本（按代码行锚定）、138 条回放、逐字节对比 |
| `fill31.py`、`proposal-template.md` | 从模板与证据生成 proposal：代码块、注释清单表与实测数字都机械填入，并断言 W8 的每个逻辑 hunk 都被引用 |
| `run-evidence.sh` | 生成全部 W 文件；见下 |
| `build-bash.sh` | 本机另建 bash 5.0 / 5.1 / 5.3 的配方（GNU 源码与全部官方补丁，`gpgv` 校验签名） |
| `W8-v31.diff` | 原型相对基线的全部改动 |
| `W13-sc-cases.txt` | 验收用例：原型在 bash 5.0.18 / 5.1.16 / 5.2.15 / 5.3.20 / 3.2.57 上各一轮；基线作为被测 hook 的一轮（基线红集）；23 个坏实现逐个的结果 |
| `W11-adversarial.txt` | v3 的对抗形状（`../v3/gen-v3.py`）在 v3.1 上的 e2e 矩阵，`LC_ALL=C.UTF-8` |
| `W12-real-traffic.txt`、`W12-replay-138.tsv` | 真实流量：138 条回放（TSV 列：编号、rc、结局、墙钟、首遍完成、触发时刻、作业耗时；单位秒，从调用起算）、300 条逐字节、bash 3.2 下 40 条逐字节 |
| `W9-suite.txt` | aria `59e333c` 的旧套件在基线与原型上各跑一遍（非 git 副本） |
| `ident-300.lst`、`w1-sample40.lst` | 抽样清单（只有编号，与 `../v3/` 相同） |

## 复现

```
bash run-evidence.sh <工作目录> [W8 W13 W11 W12 W9]     # 默认全部阶段
IMPL=<实现的 hook> bash run-evidence.sh <工作目录> …     # TASK-004：在真实实现上重跑
SC_BASH=<bash> bash sc-cases.sh <hook> [基线 hook]       # 单独跑验收用例；基线默认取自 aria 59e333c
```

- 基线一律取自 aria `59e333c`（`git show` / `git archive`）并断言 sha256 前缀，不读工作树里的 hook。实现落地后工作树里就是实现，拿它当基线会让所有对比变成自己比自己。
- 每个阶段先写工作目录，完成后才复制到本目录，失败或中断不会覆盖已提交的证据。每份输出首行记日期、平台、两个 sha256 前缀与负载。
- `sc-cases.sh` 的环境变量：`SC_BASH` 是执行 hook 的 bash，期望值随它而定（GNU/Linux 上的 5.0–5.3 期望放宽生效，其余期望与基线逐字节相同）；`SC_ONLY` 按编号过滤；`SC_DIRECT=0` 跳过直调用例；`SC_NICE=0` 不加 `taskset` 与 `nice`。
- W12 需要 `TRAFFIC_DIR`（冻结语料，仓外；抽取与复原见 `../../2026-10-20-secret-guard-scan-cost-and-firstpass-cap/traffic/`，只认 W0 的 sha256）与 `BASH32`（bash 3.2 二进制）。

## 本机依赖

- GNU/Linux；系统 bash 5.2.15；`/proc`；coreutils `sleep`（小数秒）；`taskset`、`nice`、`jq`、`python3`、`sha256sum`、`gpgv`（只用于构建）、awk、`git`。
- 另建的 bash：`~/.aria/tools/bash-5.0.18`、`bash-5.1.16`、`bash-5.3.20`（`build-bash.sh`，2026-10-22 构建，签名均已校验）；`bash-3.2.57` 由本机更早的会话构建，配方没有留下记录。
- 计时判据由 shim 的固定延迟给出，与负载无关；真实流量的收益与耗时数字随负载变化，每份输出的首行都记了负载（INV-7）。
- `sc-cases.sh` 的 `V5-S10` 用 `ulimit -u 1` 制造 fork 失败，bash 会先重试约 15 s；整轮用时约 45 s。
- `check_bare_issue_refs.py` 会把代码里的 bash 取长度写法（如 `${#1}`）当成裸 issue 引用；对 proposal 运行时报出的只有这一类。

# post_planning R2 五席的坏实现与探针（10CG/aria-plugin#217）

post_planning 第 2 轮（时间戳 `1792689337848`）五个审计席在会话临时目录里写的材料，2026-10-24 收进仓库，供 TASK-002 与 TASK-003 取用（`detailed-tasks.yaml` TASK-002 的「R2 补强」）。席位报告与汇总在主仓 `.aria/audit-reports/post_planning-R2-1792689337848-*`。

## 收了什么、没收什么

- **收**：生成坏实现的脚本；运行前写下的预测记录；探针与演示脚本；每个坏实现跑 `v31/sc-cases.sh` 的逐个结果。code-reviewer 席没有留生成脚本，它的 5 个坏实现存成相对其原型副本的 diff（`code-reviewer/mut-diffs/`）；commentsync 绕过实验存成 `code-reviewer/base-anchor-tweak.diff`。
- **不收**：整份 hook 副本（原型、基线、各坏实现，每份约 100 KB，可由生成脚本复现）；脚本运行时生成的输入文件（各席的 `in/`、`in2/`、`probes/*.json`），其中写着凭据形路径。脚本里的凭据形路径都是运行时拼装的片段，与 `v31/shapes.py` 同一做法。

## 怎么复现

- 原型：`python3 v31/mkv31.py <基线 hook> <输出>`。基线取自 aria `59e333c`（sha256 前缀 `e83c5e30f2cc`），原型的 sha256 前缀是 `9f61db0e7b8b`。
- 坏实现：各席的生成脚本以原型为输入，每处替换断言恰好命中一次：qa-engineer `mkmut.py`、`mkmut2.py`；backend-architect `mut.py`；tech-lead `mkmut.py`；knowledge-manager `mk_km_mutants.py`；code-reviewer 用 `patch` 套 `mut-diffs/*.diff`。
- 脚本里写死的路径指向当时的会话临时目录，复现时按需改。

## 编号

各席的坏实现编号（CR-MA–ME、QA-M01–M30、TL-M1–M10、BA-M1–M14、KM-M1–M6）与 R2 汇总「非作者变异测试汇总」一节一致。TASK-002 把漏网的并入 `v31/mutants.py`，从 BI-24 起编号。

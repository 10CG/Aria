# B.2 各步的报告、补丁与过程材料（10CG/aria-plugin#217 TASK-002）

- `T002a-report.md`：第一步「代码落地」的执笔席报告（两轮）。结果提交在 aria 分支 `feature/secret-guard-w10-failclosed-narrowing`：`96f9083`（What 6，落在基线上）、`21a37ea`（原型 + What 1 补充 + What 7 补充），hook 的 sha256 前缀 `af4658b6f935`。
- `T002a-vs-proto.diff`：第一步结果（不含 What 6）相对原型的差异：What 1 补充 1 个 hunk、What 7 补充 4 个 hunk。
- `T002b-report.md`：第二步「按 post_planning R2 补强可执行验收」的执笔席报告（2026-10-24）。改动是 `../v31/` 下 6 个脚本，与本报告同一个提交。报告里的相对路径相对 `t002b/`。
- `t002b/`：第二步的过程材料，挑选后收入：
  - 运行脚本 `runsc.sh`、`lowload.sh`（第一版：`waitlow` 等过之后返回非 0，见报告 4.6 节）、`lowload2.sh`；
  - 句子导出 `cs/derive.py`、`cs/gen_literal.py`、`cs/derived.*`，整块删除的构造 `cs/mk_delete.py`，commentsync 的输出 `cs/o.txt`、`cs/out.txt`；
  - 坏实现与席位写法的逐个比对 `dev/seatcheck.*`，`mutants.py` 生成的 `dev/mut/designated.tsv`、`reasons.tsv`、`perturb.tsv`；
  - 垫片拟态 `shimtest/mimic.sh`，计时校准 `calib/calib.sh` 与结果；
  - 环境错误各轮的输出 `env/*.txt`；旧版函数体放回实现副本的那个构造，存成相对实现的 `env/impl-old-platform-body.diff`；
  - 低负载轮 `runs/low/`、`runs/low2/`（`log` 记每轮首尾负载，含作废的 5.3.20 第 1 次），全部坏实现与扰动的汇总轮 `runs/mut-all-low/`；高负载各轮只收 `summary.txt`。
  - 没收：坏实现、扰动变体与基线绕过构造的整份 hook 副本（每份约 110 KB，可用 `../v31/mutants.py`、`cs/mk_delete.py` 或 `../pp-r2-seats/code-reviewer/base-anchor-tweak.diff` 复现），计时校准与探针的输入文件（`calib/in/`、`dev/probe/`），以及高负载下已被低负载轮替代的开发轮输出。
  - 报告第 1 节 (e) 所称的 `textcheck/` 在执笔席的目录里是空的；主控的另行核对见 `t002b-verify/textcheck.py`。
- `t002b-verify/`：主控对第二步的独立复核（2026-10-24 05:22–05:36 UTC）。`PREDICT.md` 是实测前写下的预期，`VERIFY.md` 是逐项结果；被测 hook 直接取 aria 分支，基线现取 `59e333c`。另有各轮原始输出、等待脚本 `other-bash.sh` 及其日志 `other.log`。

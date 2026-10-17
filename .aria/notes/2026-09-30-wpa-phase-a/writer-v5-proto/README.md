# writer-v5-proto: 原型、坏实现、时档与自检脚本 (归档)

`openspec/changes/secret-net-l3-and-bypass-paths/proposal.md` 返修成 v5 的过程中, 在会话实验目录里做的「完整目标态原型 + 坏实现变体 + 时档度量 + 文本 / 计数自检」的**重建脚本、复跑计划与汇总**。只归档脚本、计划表与汇总文本; 各树副本、bash 3.2 构建目录与会话日志不入仓。

## 先读这三条

1. **原型不是实现**: 用脚本对基线 (aria `268da8f`、standards `2bc1c4c`) 做文本替换生成, 只证明 proposal 的设计可达, 并给出「哪个坏实现会让哪几行转红」。真实现者拿到的只有 Spec 散文, 不应照抄原型。
2. **脚本里的绝对路径**指向当次会话的实验目录 (`EXP` 变量, 形如 `/tmp/claude-…/scratchpad/exp/writer-v5`)。重跑前把它们改成你自己的实验目录: 先把 aria 与 standards 复制到 `<EXP>/base/` 下并删去其中的 `.git` 文件 (子模块 gitfile); 取得真 bash 3.2 (方法见 `baseline-evidence.md`「取得真 bash 3.2」) 并以 `WPA_BASH32=<路径>` 传给探针; 把 v4 的三份文件 (git `b07f69a` 的 `openspec/changes/secret-net-l3-and-bypass-paths/` 下的 `proposal.md` 与 `baseline_probe.py`) 复制成 `<EXP>/spec/proposal.v4.md` 与 `<EXP>/spec/baseline_probe.v4.py`, 它们是 `apply_edits.py` 与 `patch_probe_v5.py` 的输入。
3. **Rule #7**: 本目录的文件不含凭据形状字面量 (补丁脚本只处理 hook 里的正则; 凭据形状的值与键名在脚本里运行时拼装, 不打印)。`scan_all.py` 把全部文件当 Bash 输出与 Read 结果各扫一遍, 对基线与目标原型两个 `secret-scan.sh` 都应静默。

## 脚本

- **补丁 (生成目标态原型与坏实现)**: `patch_l3.py` (secret-scan) / `patch_l1.py` (secret-guard), 默认变体 `v5` = 目标态, `--variant NAME[:ARG]` = 坏实现 (文件头的列表给出每个变体对应的 SC 行); `patch_docs.py` (SOT、README、CHANGELOG、两个 hook 的头注释; `--bad` / `--bad-sot` / `--bad-layer` / `--no-scope` / `--hdr-*` / `--cl-drop=<标记词>` 是文档类坏实现); `patch_tests.py` (两个测试套件的同步改动); `build_full.sh <绝对路径> 64` 组装完整目标态树 (目标路径必须是绝对路径)。
- **文本与探针**: `patch_probe_v5.py` 由 v4 探针逐处带断言地改出 v5 探针; `apply_edits.py` 把 `proposal_edits/part*.py` 的全部编辑按文件名顺序施加到 v4 proposal 上 (锚点缺失或不唯一即停; 数字占位符 `@NAME@` 取自 `out/numbers.json`, 由 `mk_numbers.py` 从原始时档输出解析, 不手填)。
- **复跑**: `runprobe.sh <label> <树根> <spec 目录> <b32: 0|1> [WPA_ONLY]` 跑探针 (先快照 spec 目录); `final_runs.sh stage1|stage2` 是定稿证据的两段复跑 (stage1: A / B / N 基线; stage2: T / TN / C); `mk_evidence.py` 由 stage1 的 stdout 组装 `baseline-evidence.md` 并断言内嵌块与 stdout 逐字节一致、基线形态成立。
- **变异**: `plans_v5/*.tsv` = 本版计划, `plans_v4/*.tsv` 与 `plans_v3/*.tsv` = 前几版计划 (每行: 标签 / 种类 `l3|l1` / 变体 / SC 列表 / 行列表; 本版移除了 7 个设计已不存在的变体, 汇总里逐个点名并写明替代者); `mutbatch.py <计划> --tree <树> --spec <spec>` 逐个生成坏实现并只跑指定的行; `run_final_campaign5.sh` 依次跑 v5 / v4 / v3 三批与文档类坏实现 (`docvariants5.py`); `build_mut_summary5.py` 汇总为 `mut_summary_v5.txt` (转红 0 行的坏实现逐个点名为等价变异或时档类并写明理由, `equiv_reasons.py`; 前几版转红过的行必须仍然转红, 否则脚本以 1 退出)。
- **时档**: `timing.py <基线 hook 目录> <目标 hook 目录> [档位] [--pairs N …]` 同一次运行内交错 A/B, 记整进程 CPU 时间 (user+sys, 含全部子进程) 的最小值之比与墙钟, 并对 (f) / (f-hit) / (g) / (h) 用注入标记的副本做一次不计时的活性检查; 档位 `f f0 fhit g gmax h i i3 w1`; 它只打印比值与活性, 判据由 W14 给出。`run_timing_variants5.sh` 对每个坏实现跑它该被抓到的那一档; `occ_cost.py` 量命令长度 × 出现点对扩展命中路径 CPU 的影响 (目标 vs 手写阶段切分 vs 逐出现点重判)。
- **自检**: `ere_battery.py` (6 个新 pattern 在对抗单行上的缩放: 2n/n 之比约 2 = 线性, 约 4 = 平方级; 含无界写法与有界写法的对照)、`fuzz_value_of.py` (两版取值 / 去空白代码对 17 个 tag 的真实 span 做差分)、`diff_ext_builtin.py` (扩展条目与内建 `app.ini` 行逐命令形态的差分, 93 形态, 与探针 19af 的 73 形态重叠)、`fuzz_ext_builtin.py` (同一差分的随机版: 由片段拼出的随机命令, 两侧退出码须逐条相等; 手写阶段切分的参考坏实现用来证明它有区分力)、`readface_check.py` (SC-18 的 32 条路径各只命中一个基线备选)、`refs_check.py` (Impact 的关闭关键字检查三态实跑)、`scan_all.py` (Rule #7 自扫)、`check_counts.py` (proposal 各 SC 条目声称的 `×N` 与 stdout 逐 SC 对账)、`xref_check.py` (proposal 引用的行号与探针输出对账)、`validate_plans.py` (计划里的变体都被补丁脚本认得)、`ere_claims.py` (W2 线性段引用的 `grep -oE` 秒数: 目标 pattern 与无界 / 无左边界的坏 pattern)、`format_lint.py` (LF / 无制表 / 无带圈数字 / 无 emoji / 无 AI 署名 / 无裸 issue 号 / 正文无版本与审计叙事)。`mk_report.py` + `report_text.py` 由最终文件组装返修报告 (数字全部取自文件)。

## 汇总

- `mut_summary_v5.txt`: 每个坏实现转红的行数与行名, 前几版坏实现的回归结果, 等价变异与被取代者的理由。
- `../logs/` (交付目录里的 `logs/`): 定稿证据运行的 stdout / rc / stderr (`final_A` `final_B` `final_N` `final_T` `final_TN` `final_C`)、各脚本输出、时档与成本原始输出、`numbers.json`、`campaign.log`。

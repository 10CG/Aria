# writer-v3-proto: 原型、坏实现、时档与自检脚本 (归档)

`openspec/changes/secret-net-l3-and-bypass-paths/proposal.md` v3 的返修过程中, 在会话实验目录里做的「完整目标态原型 + 坏实现变体 + 时档度量 + 文本 / 计数自检」的**重建脚本、复跑计划与汇总**。只归档脚本、计划表与汇总文本 (几百 KB); 各树副本、bash 3.2 构建目录与会话日志不入仓。上一轮的同类材料在 `../writer-v2-proto/`。proposal 头部「证据位置」与 Tasks 1.8 指向本目录: 实现期的非作者对抗 review 以此为对照。

## 先读这三条

1. **原型不是实现**: 用脚本对基线 (aria `268da8f`、standards `2bc1c4c`) 做文本替换生成, 只证明 proposal v3 的设计可达, 并给出「哪个坏实现会让哪几行转红」。真实现者拿到的只有 Spec 散文, 不应照抄原型。
2. **脚本里的绝对路径**指向当次会话的实验目录 (`EXP` 变量, 形如 `/tmp/claude-…/scratchpad/exp/writer-v3b`)。重跑前把它们改成你自己的实验目录; 先把 aria 与 standards 复制到 `<EXP>/base/` 下并删去其中的 `.git` 文件 (子模块 gitfile); 取得真 bash 3.2 (方法见 `baseline-evidence.md`「取得真 bash 3.2」) 并以 `WPA_BASH32=<路径>` 传给探针。HOME 与 TMPDIR 用实验目录下的私有目录。
3. **Rule #7**: 本目录的文件不含凭据形状字面量 (补丁脚本只处理 hook 里的正则; 凭据形状的值与键名在脚本里运行时拼装, 不打印)。`scan_all.py` 把全部文件当 Bash 输出与 Read 结果各扫一遍, 对基线与目标原型两个 `secret-scan.sh` 都应静默。

## 脚本

- **补丁 (生成目标态原型与坏实现)**: `proto/patch_l3.py` (secret-scan) / `patch_l1.py` (secret-guard) / `patch_docs.py` (SOT、README、CHANGELOG、两个 hook 的头注释; `--bad` = 所有事实只塞进 SOT 版本历史表、其余文档不落地, `--bad-sot` = 只有 SOT 塞历史表、其余文档照常落地) / `patch_tests.py` (两个测试套件: 隔离 HOME、头注释计数与自检 (`--no-selfcheck` = 只加头注释不加自检)、夹具拼装、census 计数)。`--variant NAME[:ARG]` 生成坏实现, 变体清单在两个补丁文件的 docstring 里。`build_full.sh <绝对路径 out> [family_count]` 组装完整目标态树。
- **复跑**: `runprobe.sh <label> <树根> <spec 目录> <b32: 0|1> [WPA_ONLY]` 跑探针 (先快照 spec 目录); `mkplan.py <dir>` 生成变异计划表; `plans/*.tsv` = 本次实际用的计划 (每行: 标签 / 种类 `l3|l1` / 变体 / SC 列表 / 行列表); `mutbatch.py <plan.tsv> --jobs N [--b32] --out <dir>` 逐个构造坏实现并只跑其对应的 SC 与行, 记下转红的行 (`SUMMARY.txt`); `run_campaign.sh` 依次跑五份计划, `run_after.sh` / `run_after2.sh` 跑 `plan_extra` 与两个需要真 bash 3.2 的变体; `final_runs.sh stage1|stage2` 是定稿证据的两段复跑。
- **汇总**: `mut_summary_v3.txt` —— 每个坏实现转红的行数与行名 (`build_mut_summary.py` 由各计划的 `SUMMARY.txt` 生成; 因变体 / 探针 / 脚本事后修正而作废的首轮结果不计入总数, 单列并写明由哪次复跑取代); 转红 0 行的坏实现逐个点名为「等价变异」并写明理由 (`equiv_reasons.py`: 行为不变, 不是缺项)。`manual_runs.txt` —— 无法写成 mutbatch 计划行的坏实现与负控 (需要完整树的文档类 / 普查类、需要重复次数的路径字符类、SC-15 / 形态行 / 关键字正则的负控) 及其结果。`timing_summary.txt` —— 时档实测记录 (主机负载、每档基线 / 目标 CPU 时间与比值、坏实现的比值、活性断言)。
- **时档**: `timing.py <基线 hook 目录> <目标 hook 目录> [档位] [--pairs N …]` 同一次运行内交错 A/B, 记整进程 CPU 时间 (user+sys, 含全部子进程) 的最小值之比与墙钟, 并对 (f) / (g) / (h) 用注入标记的副本做一次不计时的活性检查; 档位 `f f0 g h i w1` 见脚本头注释。
- **自检**: `mk_evidence.py` 由探针 stdout 组装 `baseline-evidence.md` 并断言内嵌块与 stdout 逐字节一致、基线形态成立; `sc_counts.py` (每 SC 每类别的行数与 `yes` 数)、`check_counts.py` (proposal 各 SC 条目声称的 `×N` 与 stdout 逐 SC 对账)、`xref_check.py` (proposal 引用的行号都存在、每个行号都被引用过) —— 三个都只读文本; `coverage_check.py <探针 stdout>` (相对 v2 新增或改写的每一行都必须被至少一个坏实现转红: 计划内的 `mut/plan_*/SUMMARY.txt` 或 `manual_runs.txt` 列出的手工运行; 打印未覆盖的行); `refs_check.py` 对 Impact「提交页脚 / PR 描述的关键字」的正则跑正例与反例; `hooktry.py` 把一批命令喂给一个或几个 L1 hook 看退出码 (命令只当 stdin 文本, 不执行), `cases_*.py` 是它的输入; `l3try.py` / `scan_file.py` / `scan_all.py` 对 L3 hook 喂文本只打印 tag 名; `nc15.py` 是 SC-15 的负控 (往三份文件副本里各追加一行运行时拼装的凭据形状, 目标 hook 下 15e / 15f / 15g 应全红); `build_deliver.py` 组装交付目录与 `MANIFEST.sha256`。

# writer-v2 原型与坏实现复跑脚本 (归档)

proposal v2 返修实例在会话实验目录里做的「完整目标态原型 + 坏实现变体」复跑的**重建脚本与汇总**。只归档脚本与汇总 (约 100 KB); 各树副本 (约 430 MB) 与 bash 3.2 构建目录不入仓。

- 原型不是实现: 用脚本对基线 (aria `268da8f`、standards `2bc1c4c`) 做文本替换生成, 只证明 proposal v2 的设计可达, 并给出「哪个坏实现会让哪几行转红」。
- `patch_l3.py` / `patch_l1.py` / `patch_docs.py` / `patch_tests.py`: 原型补丁; `build_full.sh <out> <census_count>`: 组装完整目标态树。
- `run_mutants*.sh` / `rerun_mutants.sh`: 坏实现变体复跑; `mut_summary*.txt`: 汇总 (返修报告 §4 的「三态」表由此而来)。
- `mk_evidence.py`: 断言证据文件内嵌的探针 stdout 与实跑逐字节一致; `runprobe.sh`: 跑探针的环境包装。
- 脚本里的绝对路径指向当次会话的临时目录, 重跑前需要改成你自己的实验目录。bash 3.2 运行腿需要自行构建 `bash-3.2.57` (源码 sha256 与补丁范围见 `../writer-reports/v2-writer-report.md` §4), 并以 `WPA_BASH32=<路径>` 传给 `baseline_probe.py`。

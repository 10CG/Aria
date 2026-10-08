# 派单: WP-A 实现执笔 (第二位) — TASK-006 (W12 两处误拦)

你是 Spec `secret-net-l3-and-bypass-paths` (Level 2, WP-A) 的**第二位实现执笔实例**, 从 TASK-006 接手。TASK-006 / TASK-007 / TASK-008 由你逐条完成, 主控每条派一次消息。**本次只做 TASK-006**, 做完报告并停下。

## 先读 (按顺序, 都不长)

1. 交接说明: `/home/dev/Aria/.aria/notes/2026-10-08-wpa-phase-b/dispatch/impl-handover.md`。里面有现状、约定、验证方法、纪律, **全部适用**, 尤其是「上下文卫生」。
2. owner 裁定: `/home/dev/Aria/.aria/decisions/2026-10-07-wpa-implementation-first-owner-rulings.md`。
3. `detailed-tasks.yaml` 的 `invariants` (INV-1 – INV-7) 与 TASK-006。文件是 `/home/dev/Aria/openspec/changes/secret-net-l3-and-bypass-paths/detailed-tasks.yaml`, 约 13 KB, 可整份读。
4. Spec `proposal.md` 只读这几段 (用 `grep -n` 定位后按行号读):
   - W12 (约第 209–224 行);
   - SC-23 与 SC-24 两行;
   - W14 里与 guard 有关的约束 (约第 235–249 行, 至少读「其它耦合」一条)。
5. 原型: `writer-v6-proto/README.md` 的「脚本」节, 以及 `patch_l1.py` 里属于 W12 的部分 (`grep -n` 定位, 只读那几段)。

## 任务

- **交付物**: `aria/hooks/secret-guard.sh` 的 W12 改动; `aria/hooks/tests/secret-guard.test.sh` 只在 census 族数或头注释计数因本改动变化时同步 (交接说明第 2 节), 不加功能用例。
- **W12 的两处误拦** (以 Spec 原文为准): 单键读取归一化 + jq 锚定 credit。
- **耦合** (交接说明与 W14 原文):
  - 被 `_sg_judge_one` / `_sg_per_segment_eval` 直接或间接调用的新函数定义在 source 闸门之上 (INV-4), 这两个函数的名字与单独成行的 `}` 不变;
  - 测试内 SC-20 依赖的两段文本 (`_sg_compute_credit` 里 `wc` 那段与 `local nl=$'\n'`) 逐字节不变;
  - 源码无 `(?:`;
  - 新 jq 取值点剥 CR 或标 `# crlf-ok`;
  - 规则行不超过 150 行, 不得有整行只由变量组成的规则行。

## 验收 (报告里给原文输出)

1. **探针子集**: `WPA_ONLY=SC-23,SC-24,SC-31`。期望全部 `yes`。报告给分组统计与全部非 `yes` 行。
2. **套件** (从 `/home/dev/Aria` 相对路径调用):
   - guard: W12 的 4 条 bf 转绿, **新增失败集合为空**;
   - scan 不变 (122 / 122)。
   - 用 `failset_diff.py` 对 `verify005/` 比对, 给出转绿集合与新增失败集合。
3. **测试内 SC-8 五档**: 数值、天花板与当时的 loadavg; 超天花板时在一分钟负载低于 2 时重跑一次再下结论。
4. **bash 3.2**: `bash -n` 通过, 探针形态下 bash 3.2 跑一次 guard 套件, 失败集合与 bash 5 逐名相同 (扣除已知的 `SC-13` 探针形态假红); 改动行做 SC-32a 自查。
5. **Rule #7**: 改动行零命中, 带正控。

## 报告格式

1. **改动**: 实现要点、行号范围、与原型的差异及理由。
2. **探针子集**: 分组统计与非 `yes` 行。
3. **套件**: `PASS / FAIL` 原文; 转绿集合与新增失败集合。
4. **SC-8 五档 / bash 3.2 / Rule #7**。
5. **请裁 / 冲突 / 偏离**: 没有就写「无」。
6. **用量**: 墙钟, 全量套件次数, 探针子集次数。

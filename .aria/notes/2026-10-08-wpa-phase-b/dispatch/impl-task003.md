# 派单: WP-A 实现执笔 — TASK-003 (W1 提取 + W6 两个套件隔离 HOME + W7 既有夹具拼装)

TASK-002 已提交: aria `feature/secret-net-l3-and-bypass-paths` 上 `ec99e6c` (已推 origin)。主控复核结论: 相对路径调用下 scan 78 / 122、guard 665 / 780, 失败集合恰等于 bf 集合, `got 127` 为 0。本次在它之上做 TASK-003。**只做 TASK-003**, 做完报告并停下。

## 任务定义

- `detailed-tasks.yaml` 的 TASK-003 (已按你上一份报告第 5 节修订: 交付物加了 `secret-guard.test.sh`, SC-35 的验收范围改了, 见该任务 `notes`)。
- Spec: `proposal.md` 的 W1 (约第 52–59 行)、W6 (约第 138–144 行)、W7 (约第 145–151 行), 以及 SC-1 / SC-2 / SC-3 / SC-14 / SC-15 / SC-35 各行; `hooks.json` 的约束见 SC-31 31d / 31e 与 SC-35 35d。
- 起点 (INV-1): 原型 `patch_l3.py` 中属于 W1 的部分、`patch_hooks_json.py`、`patch_tests.py` 中属于 W6 / W7 的部分。写成正式代码, 行为以 Spec 为准; 原型与 Spec 冲突时以 Spec 为准并上报。

## 交付物 (INV-3: 代码改造面只限这些)

1. `aria/hooks/secret-scan.sh`: **只做 W1** (提取修复、失败事件的 `error` 字段、输出事件名)。W2 – W5 是 TASK-004, 本次不碰。
2. `aria/hooks/hooks.json`: 只增一条 `PostToolUseFailure` 注册 (与 `PostToolUse` 那条同 matcher、同 command、同 timeout), 其余不动, 全文不含 `completeness_gate` 字面。
3. `aria/hooks/tests/secret-scan.test.sh`: W6 的 HOME 隔离块 + W7 的既有夹具拼装。
4. `aria/hooks/tests/secret-guard.test.sh`: **只加** W6 的 HOME 隔离块。

## 你上一份报告带来的约束

- HOME 隔离块必须插在 `_wpa_orig_home` 那一行**之后** (两个套件都是)。
- W7 的夹具拼装要按**目标态**的 pattern 拆 (含 W2 的 6 个新 tag, 例如旧夹具第 119 行一带会被 kv tag 命中), 使 SC-15 15a 在 TASK-004 之后仍静默。每条既有断言的输入值与期望 tag 不变, 49 条既有断言照过。拆法: 在 scratchpad 里用原型生成的目标态 hook 判定要拆哪些 span; hook 侧**不加**任何按路径的豁免 (W7「设计取舍」)。
- 新增的 hook 代码与测试代码都遵守 SC-32a 的 13 类 bash 4+ 构造禁令 (本任务至少对改动行自查一遍)。

## 验收 (都要在报告里给原文输出)

1. **探针子集** (对真 checkout 跑): `WPA_ONLY=SC-1,SC-2,SC-3,SC-14,SC-15,SC-35 python3 /home/dev/Aria/openspec/changes/secret-net-l3-and-bypass-paths/baseline_probe.py /home/dev/Aria/aria`。期望: SC-1 / SC-2 / SC-3 / SC-14 / SC-15 全部 `yes`; SC-35 的 35c / 35d / 35e `yes`; 35a / 35b 仍 `no` (依赖 W2, 归 TASK-004), 报告里写出它们的实得。
2. **两个套件** (从 `/home/dev/Aria` 用相对路径调用, HOME 仍指向私有目录): 与 TASK-002 提交时的失败集合比, **转绿的恰好是 W1 / W6 / W7 该转绿的用例** (W1 的 SC-1a / 1b / 1c / 1d / 1f、SC-35 中 W1 单独成立的用例与 35d、SC-14a / 14b、SC-15a), **其余失败用例不变, 不新增任何失败**。用 TASK-002 时那种逐名比对给出「转绿集合」与「新增失败集合 (应为空)」。
3. **外溢**: W6 之后两个套件即使不设 HOME 也不写真实 HOME —— 用一次「不设 HOME」的运行验证 (跑前跑后记录真实 `~/.claude/logs/secret-scan.log` 与 `guard-bypass.log` 的大小与 mtime, 必须不变)。这一次运行算在下面「全量次数」里。
4. **bash 3.2**: 改后的 `secret-scan.sh` 在真 bash 3.2 下 `bash -n` 通过, 并在 bash 3.2 下跑一次 scan 套件 (探针形态或 PATH 前置 bin32 目录均可), 结果与 bash 5 相同。
5. **Rule #7**: hook 新代码不回显任何值; 新增或改动的测试行用基线与目标态两个 `secret-scan.sh` 各扫一遍, 零命中 (带正控)。

## 资源纪律与硬性纪律

与 TASK-002 派单相同:
- 同一时刻只跑一个重实验。
- 探针只跑上面的子集; 本任务**不跑探针全量**。
- 只改上面四个文件。
- 不做 git 写操作, 不派子代理, 不开 issue / 不发评论。
- Rule #7。
- 含敏感形状的文字用 Write / Edit 落文件。
- 看 `secret-scan.test.sh` 用 Read 工具 (会话里生效的是插件缓存里的旧 hook, 不受你的改动影响)。

## 报告格式

1. **改动**: 按文件列, 给行号范围与一句话说明; W1 的实现要点 (提取了哪些字段、失败事件怎么识别、输出事件名怎么定), 与原型的差异及理由。
2. **探针子集**: 每一行的 SC │ 行 │ 期望 │ 实得 │ match。
3. **套件**: 两个套件的 `PASS / FAIL` 原文; 「转绿集合」与「新增失败集合」的逐名比对结论。
4. **外溢 / bash 3.2 / Rule #7** 三项的结果。
5. **请裁 / 冲突 / 偏离**: 没有就写「无」。
6. **用量**: 墙钟, 全量套件次数, 探针子集次数。

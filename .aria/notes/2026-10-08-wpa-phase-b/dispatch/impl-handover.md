# 执笔交接说明 (WP-A Phase B, 第二位实现执笔用)

> 写给从 TASK-006 起接手的新执笔实例。写于 2026-10-08, 作者是主控, 内容取自第一位执笔 (TASK-002 – TASK-005) 的四份报告与主控复核记录。
> 换人的原因是**成本**: 第一位执笔的上下文累积到约 48 万 token, 之后每次工具调用都要重读一遍。你从干净的上下文开始, 请保持精简。

## 1. 现状

- **分支**:
  - aria 子模块 `/home/dev/Aria/aria` 的 `feature/secret-net-l3-and-bypass-paths`, 已推 origin;
  - standards 子模块的同名分支, 尚无提交。
- **已提交**:

  | 任务 | 提交 | 内容 |
  |---|---|---|
  | TASK-002 | `ec99e6c` | 测试先行, 两个套件 +260 条 |
  | TASK-003 | `7567fe5` | W1 + W6 + W7 |
  | TASK-004 | `2e2a2a8` | W2 – W5, `secret-scan.sh` 全部完成 |
  | TASK-005 | 见主控消息 | W8 + W11, 并同步 census 族数 61 → 64 |

- **当前套件** (TASK-005 之后):
  - `secret-scan.test.sh`: 122 / 122 全绿。
  - `secret-guard.test.sh`: 783 条 (含 zsh 789), 失败 48 条, 全是留给后续任务的 baseline-failing:
    - W9 30 条、W10 12 条 → TASK-007;
    - W12 4 条 → TASK-006;
    - W13 的 SC-25f / 25i 两条 (扩展块文案) → TASK-007。
- **探针**: L3 部分 (SC-1 – SC-15、SC-33、SC-35) 与 W8 / W11 部分 (SC-16 – 18、SC-22、SC-31) 都已 `yes`; SC-34 34c 留给 TASK-007。

## 2. 约定 (前任执笔建立, 照用)

- **用例命名**: `W<n> SC-<行> <类别>: <说明>`, 类别码:
  - `bf` = baseline-failing
  - `rg` = reverse-guard
  - `ag` = allow-guard
  - `kl` = known-limit
- **新增块里的 helper 一律 `wpa_` 前缀**:
  - guard 套件用 `wpa_rc` / `wpa_err` / `wpa_x` / `wpa_all_bash_case` / `wpa_one_bash_case` / `wpa_marker_case` / `wpa_fault_case` 等。
  - hook 路径与套件自身路径已在块头解析成绝对路径 (`wpa_hook` / `wpa_self`); helper 会先 `cd` 到 scratch 目录再执行 hook, **新代码不要再引用相对的 `$HOOK` / `$0`** (TASK-002 的缺陷就是这个)。
- **W6**: 两个套件开头都已把 HOME 指向自建临时目录 (位于 `_wpa_orig_home` 一行之后)。直接跑套件不会写真实 `~/.claude/logs`, 但保险起见仍可再指向私有 HOME。
- **头注释计数**: guard `Coverage: 789 cases (783 without zsh)`, scan `Coverage: 122 cases`, 两个套件都有自检断言。增删用例时同步头注释; `standards/conventions/secret-hygiene.md` 里的计数留给 TASK-008 / 009。
- **census**: `family_count` 硬编码现为 64。任何改变跨段族的规则行改动, 都要在**同一任务**里同步硬编码并补 `# family='<精确 key>'` 的 `bash_case` 探针 (主控裁定, 理由是保持每条任务「新增失败为空」)。
  - key 照 census 输出原样写, 不手敲。
  - 注意 W8 行的 key 是 `GRP:()`: census 在不带共享变量的 bash 里求值, 变量展开为空。

## 3. 验证方法 (主控每次都会独立复跑同一套)

1. **套件**: 从 `/home/dev/Aria` 用相对路径调用 `bash aria/hooks/tests/<套件>`, 输出写文件。
2. **失败集合比对**:
   - 主控用 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/failset_diff.py <旧目录> <新目录>`, 每个目录里放 `secret-scan.out` 与 `secret-guard.out`。
   - 用例名以第一个 `]: ` 结尾, 名字里可能含 `]`。
   - TASK-005 之后的基准输出在同目录的 `verify005/`。
3. **探针子集**: `WPA_ONLY=<SC 列表> python3 /home/dev/Aria/openspec/changes/secret-net-l3-and-bypass-paths/baseline_probe.py /home/dev/Aria/aria`, 输出写文件, 只读分组统计与非 `yes` 行。
4. **bash 3.2**:
   - `WPA_BASH32=/home/dev/.aria/tools/bash-3.2.57/bash`;
   - 前任把整套 PATH 做成了 `.../scratchpad/impl/bin32/` (`bash` 指向 3.2), 套件的「探针形态」运行 (无 `.git` 副本 + PATH 前置 bin32) 见 `.../scratchpad/impl/work/run32.sh` 与 `runprobeform.sh`;
   - 探针形态下 guard 会多一条已知的 `SC-13 头注释计数` 假红 (无 git 历史时 SC-8 / SC-9a 被跳过), 不是回归。
5. **Rule #7**: 新增行用基线与当前 `secret-scan.sh` 各扫一遍, 零命中, 带正控。前任脚本在 `.../scratchpad/impl/work/rule7_t5.sh` / `scan_file.sh`。
6. **SC-32a**: 改动行做 13 类 bash 4+ 构造自查, 脚本 `.../scratchpad/impl/work/sc32a.py`。

## 4. 已知待办 (不是你这次的任务, 别顺手改)

- `hooks.json` 顶层 `description` 是否提及 `PostToolUseFailure` → TASK-009。
- W14 原文点名的第三个新族 (「`<` 重定向行」) 与 census 实测 (W8 读取器行 `GRP:()`) 不符, 数量 61 → 64 一致 → 文档同步时订正 (TASK-009)。
- 时档余量: L3 的 i3-f / g / h 比值约 3.3–3.4 (上界 5.0); 测试内 SC-8 的 (e) 档 new 在 TASK-003 时约 38 ms, TASK-005 后 46.5 ms (天花板 100 ms) → TASK-010 留意。
- TASK-009 (文档同步) 按 Spec Tasks 1.9「勘正执笔人 ≠ 实现执笔人」由另一位执笔做, 不是你。

## 5. 纪律 (每次派单都适用)

- **上下文卫生 (硬要求)**:
  - 只按行号范围读: 先 `grep -n` 定位, 再用 Read 的 `offset` / `limit`;
  - 不整份读 `proposal.md` (240 KB)、`baseline_probe.py` (245 KB)、原型脚本;
  - 大输出落文件只读摘要;
  - 不要 `ls` 大目录 (`bin32` 里有上千个软链);
  - 工具调用宁少勿碎。
- **资源纪律**:
  - 会话进程树 nice 19、只用 0–1 号核 (自动继承, 别改回);
  - 同一时刻只跑一个重实验, 不跑探针全量;
  - 不跑 `find /` 一类全盘扫描;
  - 时档类测量只在一分钟负载低于 2 时串行跑。
- **硬性纪律**:
  - 只改派单列出的文件;
  - 真仓内不做 git 写操作, 提交由主控做;
  - 不派子代理, 不开 issue / 不发评论。
- **Rule #7**:
  - 不读不打印任何真实凭据;
  - 像凭据的值运行时生成, 经 stdin 喂给 hook, 绝不打印;
  - 报告只写元数据。
- **现行会话 hook 的副作用** (会话里生效的是插件缓存里的旧版 hook, 不受你的改动影响):
  - L1 会拦 heredoc / `python3 -c` 命令行里仅为文字提及的敏感读取形状 (如含 `.env` 的文字), 写这类文本用 Write / Edit 落文件再执行;
  - 用 Bash 输出含凭据形状夹具的文件文本可能触发 L3 告警, 看测试文件用 Read 工具。
- **Spec 权威**: 以 `proposal.md` 为准, 原型 (`/home/dev/Aria/.aria/notes/2026-09-30-wpa-phase-a/writer-v6-proto/`, 先读其 `README.md`) 是实现起点 (INV-1); 二者冲突、Spec 有歧义或做不到时不自行发明, 写进报告的「请裁」。

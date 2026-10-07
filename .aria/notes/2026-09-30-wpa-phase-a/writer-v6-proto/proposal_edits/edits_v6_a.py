# edits_v6_a.py -- header, Why, W1 (failure event), W2 (linear rule, known limits), W4.   Executed by apply_edits_v6.py (shares sub1 / after / NUM / t).

# ---------------------------------------------------------------- header
sub1("> **Status**: Draft — post_spec 审计中", "> **Status**: Draft — post_spec 定点修补中")
sub1("> **代码落点**: aria 子模块 `hooks/secret-scan.sh`、`hooks/secret-guard.sh`、`hooks/tests/secret-scan.test.sh`",
     "> **代码落点**: aria 子模块 `hooks/secret-scan.sh`、`hooks/secret-guard.sh`、`hooks/hooks.json` (只增一条 secret-scan 的 `PostToolUseFailure` 注册: W1)、`hooks/tests/secret-scan.test.sh`")
sub1("Spec 落主仓 (Rule #5)。`hooks/hooks.json` 与 `.aria/config.json` 不动", "Spec 落主仓 (Rule #5)。`.aria/config.json` 不动")
sub1("(aria 10 个 + standards 1 个 + 主仓同步面 8 个文件加 2 个 gitlink + Spec 目录 3 个)", "(aria 11 个 + standards 1 个 + 主仓同步面 8 个文件加 2 个 gitlink + Spec 目录 3 个)")
sub1("(14 个工作项 / 34 组 SC / 437 行探针)", "(14 个工作项 / @SC_GROUPS@ 组 SC / @ROWS@ 行探针)")
sub1("writer-v5-proto", "writer-v6-proto", 5)

# ---------------------------------------------------------------- Why
sub1("| 6/6 误拦 | SC-23 |", "| @SC23_BASE@ 误拦 (23a 1 + 23b 5 + 23j 4 个独立运行) | SC-23 |")
sub1("/proc/*/cmdline` / exec 包裹下的 env …) | 0/57 拦 | SC-22 |", "/proc/*/cmdline` / exec 包裹下的 env …) | 0/@SC22_N@ 拦 | SC-22 |")
sub1("| L1 jq 只出元数据的形态 (`keys_unsorted`、`map_values(length)`) | 5/5 误拦 | SC-24 |\n",
     "| L1 jq 只出元数据的形态 (`keys_unsorted`、`map_values(length)`) | 5/5 误拦 | SC-24 |\n"
     "| L3 失败调用 (Bash 非零退出等) 的错误文本 | 失败信封里的凭据行 0/3 检出 (基线没有注册该事件, 提取链也不读 `error`) | SC-35 |\n")
sub1("升级为「检测 + 脱敏」列入「待 owner 复议」第 1 条。\n",
     "升级为「检测 + 脱敏」列入「待 owner 复议」第 1 条。\n\n"
     "平台事实 (失败的工具调用): 本机 Claude Code 2.1.285 二进制的事件表写 `PostToolUse` 为「Run after successful tool」、`PostToolUseFailure` 为「Run after tool fails」; 失败事件的输入 schema 是 "
     "`hook_event_name, tool_name, tool_input, tool_use_id, error, is_interrupt?, duration_ms?` (**没有** `tool_response`), Bash 默认语义下非零退出即失败 "
     "(例外: `grep` / `rg` / `egrep` / `fgrep` / `findstr`、`diff` / `fc` / `where` 的退出码 1, `robocopy` 的 1–7), 失败文本 (`Exit code N` 加 stderr 与 stdout) 在 `error` 里送给模型; "
     "失败事件的 `hookSpecificOutput` 只有 `hookEventName` 与 `additionalContext`, 且 `hookEventName` 必须等于实际触发的事件, 否则 harness 抛 `Hook returned incorrect event name`。"
     "所以 L3 原先对失败的调用整体失明, W8 / W10 / W11 里「交给 L3」的路径对非零退出的命令不成立; W1 补齐。送达路径 (`hook_additional_context`, `hookEvent: PostToolUseFailure`) 在二进制里与 `PostToolUse` 同形, 但**端到端未验证** (Tasks 1.12 第 6 腿)。\n")

# ---------------------------------------------------------------- W1
sub1("提取链在 `.tool_response.stdout` 之后加 `.tool_response.file.content`, 其余分支与顺序不动",
     "提取链在 `.tool_response.stdout` 之后加 `.tool_response.file.content`、在末尾加 `.error` (失败事件, 见下一条), 其余分支与顺序不动")
sub1("\n- **设计取舍**: **选 A** 只加 `file.content` 一个分支",
     "\n- **失败事件 (`PostToolUseFailure`)**: 失败的工具调用 (Bash 非零退出等) 不触发 `PostToolUse`, 触发 `PostToolUseFailure`: 输入没有 `tool_response`, 调用的文本在顶层 `error` (平台事实见 Why)。"
     "**改动**: (1) `hooks/hooks.json` 为 secret-scan 增一条 `PostToolUseFailure` 注册, matcher、命令与超时同其 `PostToolUse` 条目, 不碰任何别的注册 (顶层 `description` 字符串可随之更新, 不是注册), 全文不出现 `completeness_gate` 字面 "
     "(10CG/Aria#199 的守卫; SC-35 35d, SC-31 31d / 31e); (2) 提取链末尾加 `.error`, 失败信封与成功信封走同一条「提取 → 分类 → 告警」路径, 成功路径的既有检出一个不减 (SC-1 / SC-2 照过); "
     "(3) 输出里的 `hookSpecificOutput.hookEventName` 取输入的 `hook_event_name` (缺省 `PostToolUse`), 因为 harness 按实际触发的事件校验它 (SC-35 35b / 35c); 事件名先用一次 bash 子串预检, "
     "命中才用 jq 确认 (常态不多一个进程; 输出文本里仅仅提到这个词不会翻转事件名, 35c)。`is_interrupt` 为真的失败 (用户中断) 同样被扫描。"
     "**设计取舍**: **选 A** 注册并读 `error`。不选 B 把失败调用列为已知限制: 失败的调用同样把输出送进模型上下文 (`systemctl status` 对未运行的单元退出 3, `curl -f -v` 遇 4xx 退出 22, 先打印后失败的读取), "
     "且正是 W8 / W10 / W11 所依赖的兜底场景 (备选 B 列入「待 owner 复议」第 33 条)。不选 C 在 `PostToolUse` 里读 `error`: 该事件上没有 `error` 字段。"
     "\n- **设计取舍**: **选 A** 只加 `file.content` 一个分支")
sub1("字符串形 `tool_response` 会不会到达 PostToolUse 未证实。",
     "PostToolUse 上没有字符串形 `tool_response` 的平台样本 (失败的调用走 `PostToolUseFailure`, 见上一条)。")
sub1("既有 L3 行与两个套件在原型上全部照过。", "既有 L3 行在原型上全部照过; 两个套件的运行条件: `secret-scan.test.sh` 在不带 git 历史的私有副本上全过, `secret-guard.test.sh` 在同样的副本上除测试内 SC-13 头注释计数这一条环境性 FAIL 外全过 (git 历史与 zsh 用例被跳过所致, 基线同样, SC-29), 在带 git 历史的真 checkout 上含测试内 SC-9a 与 SC-8 五档全绿 (SC-30)。")
sub1("字符串形 `tool_response` 不扫 (两者以 KNOWN-LIMIT 钉住, SC-3);",
     "字符串形 `tool_response` 不扫 (PostToolUse 上无此形状的平台样本; 两者以 KNOWN-LIMIT 钉住, SC-3); "
     "失败事件上 `additionalContext` 能否端到端送达无本机样本 (二进制里送达路径与 `PostToolUse` 同形): 属 post-ship 验证 (Tasks 1.12 第 6 腿), 结果如实写进关单评论; 失败事件的契约取自 2.1.285 二进制, 其它版本未验证;")

# ---------------------------------------------------------------- W2
sub1("**值抽取与去空白同样线性**: 取值只用 `${s%%X*}` 找分隔符再按长度取余量 (`${s:N}`) 与 `[[ =~ ]]` 捕获, **不用前导 `*` 的 `#` / `##` 最短 / 最长前缀删除** (bash 逐个试前缀, 每次 O(长度): 16 KB 的值 36 s, 远过 hook 的 5 s 超时)",
     "**值抽取与去空白同样线性**: 取值代码里的任何 `#` / `##` / `%` / `%%` 删除都必须在常数次尝试内命中 —— 被找的分隔符必然存在且位置靠前 (固定头名之后的 `:`、至多 40 个字符的旗标名之后的 `=`、JSON 值两端的引号、scheme 之后的 `://`); "
     "可能很远的分隔符 (空白串之后的 `=` / `:`、无上界的键或口令之后的 `=` / `@`) 用**一次** `[[ =~ ]]` 找到、再按长度 `${s:N}` 切; 可能不命中的单字符剥离 (引号、空白) 用 `${V:0:1}` 判断后切片, 或 `[[ =~ ]]` 捕获 "
     "(bash 逐个试位置, 每次 O(长度): 平方级的取值写法在 8 KB 的头值上要 @bad_val_quadratic_i3-a_t@ s, 在 300 KB 的不带引号的值上要 @bad_val_quote_strip_i3-f_t@ s, 在 500 KB 的上要 @BAD500_QS@ s (原型实测整进程 CPU 时间, 线性写法对同样的输入 1–2 s), 都越过每进程 4 s 的 CPU 上限; hook 自己的超时是 5 s)")
sub1("旗标紧贴在字母数字之后 (`abc--token=<值>`; 紧贴在 NUL 分隔记录里的情形由 N 视图覆盖);",
     "旗标紧贴在字母数字之后 (`abc--token=<值>`; 紧贴在 NUL 分隔记录里的情形由 N 视图覆盖); **大写键紧贴在小写前缀与下划线之后** (`prod_API_TOKEN=<值>`、`export my_DB_PASSWORD = '<值>'`: kv 的左边界 `(^|[^A-Za-z0-9_])` 不把 `_` 算作边界, 静默, SC-9 9z; 备选见「待 owner 复议」第 31 条);")

# ---------------------------------------------------------------- W2 linear paragraph: the grep -oE seconds are measured again each round (out/ere_claims.txt -> numbers.json), not carried over
sub1("(单行 320 KB 的大写连续段: 无界写法 11 s, 有界写法 0.08 s; 单行 300 KB 的 `-` 串: 带边界但无界的写法 9.7 s, 有界加边界的写法 0.06 s; 只有界、无左边界的写法也要 6.1 s)",
     "(单行 320 KB 的大写连续段: 无界写法 @ERE_KV_UNB@ s, 有界写法 @ERE_KV_B@ s; 单行 300 KB 的 `-` 串: 带边界但无界的写法 @ERE_CLI_UNB@ s, 有界加边界的写法 @ERE_CLI_B@ s; 只有界、无左边界的写法也要 @ERE_CLI_NOLEFT@ s)")
# ---------------------------------------------------------------- W9 matching cost: the hand-written per-occurrence stage cut, measured again (out/occ.txt -> numbers.json)
sub1("同一条命令内出现 64 处, 2 KB 前缀约 7.6 倍、8 KB 前缀约 24.7 倍的基线 CPU,", "同一条命令内出现 64 处, 2 KB 前缀约 @V4_2K@ 倍、8 KB 前缀约 @V4_8K@ 倍的基线 CPU,")
# ---------------------------------------------------------------- W2 known limit: the suggested-issue item that holds the FORGEJO__ / GITEA__ override lives in 7.8 only
sub1("是新的取舍, 并入建议开单 7.8 / 7.9)", "是新的取舍, 并入建议开单 7.8)")

# ---------------------------------------------------------------- W4
sub1("| `kv-secret-assign` | 键名 (大写字母 / 数字 / 下划线连续段) 之后的第一个 `=` 或 `:` 之后, 去空白与一层引号 |",
     "| `kv-secret-assign` | 键名 (大写字母 / 数字 / 下划线连续段) 之后的第一个 `=` 或 `:` 之后, 去空白与一层引号 (实现注意: 找 `=` / `:` 用一次 `[[ =~ ]]`, 剥引号用 `${V:0:1}` 判断后切片, 不用 `${V#[\"']}`: 见 W2「线性」) |")

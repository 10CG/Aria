---
verdict: REVISE
agent: backend-architect
round: R1
critical_count: 1
major_count: 2
minor_count: 2
---

# post_spec R1 — secret-guard-per-segment-evaluation — backend-architect

视角: 分段器实现的技术可行性与陷阱 (纯 bash 分段器 / 判定循环重构正确性 / 性能 / BLOCKED 消息定位)。

方法论: 未改仓库任何文件；在 scratchpad 手写 ~50 行 quote-aware 分段器原型逐条对拍 proposal 引用的语料 (SC-4 两条 / SC-1 复合泄漏 / #157 heredoc case)，并对 `aria/hooks/secret-guard.sh` 的 `has_filter` 计算块做了独立子进程开销实测 (非猜测)。

## CRITICAL-1: has_filter 的 13 处 `echo|grep -qE` 未 O3 化, 逐段化后按段数线性放大子进程 fork 开销, 大概率击穿 SC-8

`secret-guard.sh:342-399` 的 `has_filter` 计算块含 13 处 `echo "$command" | grep -qE ...` (每处 2 个进程 = 26 fork), 这是 v1.26.0 O3 **没有**覆盖的部分 —— O3 只把 `risky_patterns` 的 141 条匹配循环 (:658) 换成了 bash 内建 `[[ =~ ]]`, `has_filter` 块原样保留 grep 子进程管道。proposal §3 伪代码 `for seg in segments: has_filter_seg = compute_credit(seg)` 如果照字面把现有 `has_filter` 代码原样搬进逐段循环 (Task 1.1/1.2 都没有明确要求先做 O3 同款的 builtin 化), 子进程 fork 次数会随段数线性放大。

实测 (本机, 50 次迭代, 对照单次调用 vs 4 段循环调用同一段 has_filter 代码):

```
N=1 (现状, has_filter 每次调用只算一次): real 5.334s → 106.7ms/次
N=4 (逐段循环, 未 O3 化):                 real 20.013s → 400.3ms/次
```

即单是 has_filter 这一块, 4 段命令相对单段 **多花 ~294ms**。这个量级远超 proposal §4 引用的 69ms/76ms 基线本身, 也远超 SC-8 的 30% 阈值 (哪怕基线取本机实测的 106.7ms, 294ms 增量 = +275%)。

**这不是边缘情形, 是 Task 1.1/1.2 字面实现路径最自然的落地方式就会踩中的坑** —— 除非 compute_credit() 在"变成逐段函数"的同时**也**把 13 处 `echo|grep` 换成 `[[ $seg =~ pat ]]` (与 O3 对 risky_patterns 做的完全同款优化), 否则 SC-8 大概率不过。当前 Tasks 列表没有一条明确写这件事, rule6_note 也未提及, 存在被实现者漏掉的真实风险。

**建议**: Task 1.1 或 1.2 显式加一条 "has_filter/compute_credit 的全部子判据同步转 bash 内建 `=~`, 不得保留 `echo|grep` 管道" —— 引用同一条 memory (`feedback_bash_hook_perf_subprocess_fork_dominates`) 作为强制而非仅背景引用。

## MAJOR-1: 换行作为顶层分隔符会打散 heredoc body, 与决策表"heredoc 内部不切=偏保守"的自我描述不符

决策表第 1 行把「换行 (顶层)」列为「切」, 第 3 行又声称「子 shell / heredoc 内部…不切」= 「该内容留在所在段内一起匹配」「偏保守 (可能多拦,不会少拦)」。这两条隐含矛盾: 除非分段器专门识别 `<<[-~]?WORD` 并挂起换行切分直到匹配终止行 (这是比"quote-aware"更重的第三种解析模式, Task 1.1 只写了"quote-aware + 转义感知", 未提 heredoc 边界追踪), 否则 heredoc body 里的换行**必然**被当作顶层命令边界切开 —— 不是"留在所在段", 而是**碎成多段**。

原型实测复核 (数组基数, 非行数):
```
输入: cat <<EOF2\nsecret\nEOF2\nnomad var get nomad/jobs/x
ARRAY_LEN=4  →  ["cat <<EOF2", "secret", "EOF2", "nomad var get nomad/jobs/x"]
```
现有 `#157 heredoc-style nomad get` 用例 (`secret-guard.test.sh:603`) 因为风险 pattern 恰好落在被切碎后的**最后一段**、且该段自身仍完整含 `nomad var get`, 侥幸保持 exit=2 —— 这是**分段边界偶然没有切穿该 pattern**, 不是设计保证。真正有风险的场景是: 一条经 heredoc 换行合法携带的、且被同一行首命令的重定向/管道过滤符 (`| jq 'keys'` / `>/dev/null`) 覆盖的内容, 分段后 heredoc body 被切到独立段, 该段拿不到起始行那个过滤符的 credit —— 触发误报 (fail-safe 方向, 尚可接受, 但当前语料**零覆盖**, 无法验证)。更值得注意的是: bash ERE 的 `[[:space:]]` 本身能跨行匹配 (已实测确认: `nomad[[:space:]]+var[[:space:]]+put` 对含真实换行的字符串能整体匹配), 如果某条 risky pattern 的关键 token 恰好被引入的换行切分点撕开, 存在从"现状能拦"退化为"分段后拦不住"的路径, 只是当前 141 条 pattern + 366 条语料里没有恰好踩中这个组合的用例, 无法证实/证伪。

SC-7 目前的写法 ("锁定实现后的实际 exit code…用例转红即提示该边界被触碰") 是诚实的兜底而非正确性断言, 但它没有专门测"起始行过滤符是否因 heredoc 换行切分而与 body 内的风险内容脱钩"这一类。**建议**: Phase B 在 SC-7 之外, 补 1-2 条 heredoc+行首过滤符组合的定向用例 (即便只是记录"目前会变成误报, 属已知限制"), 让这个此前完全未被讨论过的子情形显式进入语料而不是隐藏在"未建模边界"的笼统表述里。

## MAJOR-2: SC-8 的 69ms/76ms 绝对基线在真实负载下不可复现, 阈值判定应改用相对/CPU-time 度量

本机复测 (load average 12.95 / 4 核, 与 proposal 相同方法论 20 次均值) 得到的数字与 proposal 差异很大且方向不稳定:

```
逐次单命令: 183ms ~ 500ms (10 次)
逐次4段命令: 210ms ~ 570ms (10 次)
聚合 (time 包 50 次循环): 单命令 144.8ms/次, 4段命令 130.0ms/次 —— 4段反而更快
```

wall-clock (`real`) 在多租户/高负载宿主上噪声完全淹没了 proposal 声称的 7ms 级差异 (69→76ms)。但用 `user+sys` (CPU time, 对调度噪声不敏感) 复测**当前**(未改动) 实现, 单命令与 4 段命令的 CPU 耗时几乎完全一致 (~110-112ms/次) —— 这符合预期 (现状本就不逐段, 工作量不随分隔符数量变化), 也说明 CPU-time 是比 wall-clock 更稳的度量口径。

**建议**: SC-8 改为 (a) 同一次测试运行内前后交替测改前/改后 (而非引用一次性历史基线数字), (b) 用 `user+sys` 而非 `real` 作比较口径, (c) 阈值判定基于当次实测基线而非 spec 里写死的 69ms/76ms —— 否则 Phase B 验收这条 SC 时很可能因为宿主负载波动而得出误导性的通过/不通过结论 (双向都可能: 假绿掩盖了 has_filter 未 O3 化的真实劣化, 或假红把无关的系统噪声当成本次改动的回归)。

## 判定循环重构正确性 (Positive finding, 非阻塞)

逐条核对 `has_filter` 的 9 类 credit 判据: jq keys/length、jq `{}` 白名单投影、grep 锚定、grep -v、sed s///、cut -d/-f、awk `$N`、awk `/regex/`、wc -c/l/w、sha*sum —— 这 9 类**全部**要求判据里出现字面 `\|[[:space:]]*TOOL` (即必须紧跟在管道后)。由于 proposal §1 的设计"管道不是边界" (整条 pipeline 留在同一段内), 这些判据逐段求值后语义**保持正确** —— 这正是"管道不切"这条决策的用武之地, 设计自洽。

另外两类不要求管道锚定的判据 (`>/dev/null`/`&>/dev/null` 裸重定向、curl `-o /dev/null`) 目前是"整条命令里任意位置出现即整条得分"—— 恰是 #128 本体缺陷的一部分。逐段化后这两类判据的作用域收窄到"所在段", 属于**该判据类别本身被本次修复精确化**, 不是新引入的回归。SC-4 已经用 "put: -o /dev/null (credit not command-anchored)" 显式锁定了"非命令锚定"这个既有特性 (非本次新增), 处置得当。

## quote-aware 可行性 (纯 bash, 无需外部依赖)

原型 (~50 行, 无 python/无新依赖) 逐字符扫描, 正确处理: 单引号 (无转义)、双引号 (`\ $ \` "` 转义)、`$'...'` ANSI-C (全转义直到闭合 `'`)、非引号内反斜杠转义下一字符。对拍结果:

- SC-4 两条对抗语料 (`ssh find env` 的 `\;`、`python -c` 内嵌 `;`) — 均正确保持**单段** (ARRAY_LEN=1, 用数组基数而非行数验证)。
- SC-1 复合泄漏核心用例 (`nomad var put p1 @f1 >/dev/null; nomad var put p2 @f2`) — 正确切成 2 段。
- 管道保留测试 (`curl ... | jq 'keys'`) — 正确不切, 1 段。
- 反斜杠转义分号 (`echo foo\; echo bar`) — 正确不切。
- 反斜杠续行 (`nomad var \<newline>put p @f`) — 正确不切 (合并为 1 段)。
- 经典 `'it'\''s...'` 单引号转义惯用法 — 正确不切 (`;` 落在重开的单引号内)。

`bash -n` 语法检查不适用 (只验证语法合法性, 不产出分段/求值单元, 无法替代)。子 shell `$(…)` / 反引号 / heredoc 见 MAJOR-1, 是决策表已知未覆盖项外**额外**发现的一个具体矛盾点, 而非新的未知范畴。

**方法论提醒 (非分段器本身的缺陷, 但值得写进 Phase B 测试规范)**: 我本人在验证过程中两次踩坑并自纠—— (1) 用 `segment_command | wc -l` 数段数, 当某段自身含字面换行 (反斜杠续行/ANSI-C `\n`) 时行数会虚高, 必须改用数组基数 (`${#segs[@]}`) 断言; (2) 用 `$(printf "...")` 命令替换构造带转义单引号的测试输入时, printf 的二次转义悄悄吃掉了一个反斜杠, 导致测试输入本身就不是想测的那条语料。这两个坑都会在**不改分段器逻辑**的情况下让测试结果看起来"通过"或"失败", 建议 SC-4 的"机制断言"实现说明里明确要求: 用 NUL 分隔或数组基数校验段数, 不用 `wc -l`; 构造带转义的对抗语料优先用字面单引号/heredoc, 避免多层 printf/命令替换的往返转义。

## BLOCKED 消息补段落定位 / set -uo pipefail

风险较低。现有 heredoc 式消息 (`cat >&2 <<EOF ... $command ... EOF`, :664-693) 对 `$command` 的变量替换是单遍展开, 不会因 `$command` 内容含 `$(...)`/反引号而二次执行 (已是现状行为, 换成 `$seg` 同理不新增风险)。`set -u` 层面: 只要分段函数保证 `segs` 数组非空 (`segs+=("$buf")` 收尾无条件 append, 本原型如此), for 循环内 `$seg` 恒有定义, 不存在未绑定变量路径。連续分隔符 (`;;`、`; ;`、末尾 `;`) 产生的空字符串段是无害的 —— 141 条 pattern 无一以 `^$` 锚定, 空段不会误判, 只是可以顺手 skip 掉做小优化, 非必须。

## 总结

- CRITICAL 1 项: has_filter 子判据未 O3 化, 逐段化后子进程 fork 按段数线性放大, 实测 4 段命令仅 has_filter 一块就多耗 ~294ms, 大概率击穿 SC-8, 当前 Tasks 未显式要求同步 builtin 化。
- MAJOR 2 项: (1) 换行顶层切分与决策表"heredoc 内部保守不切"的自我描述矛盾, 已实测确认换行会把 heredoc body 切成多段而非"留在所在段", 存在过滤符与风险内容跨段脱钩的未覆盖场景; (2) SC-8 的绝对 ms 基线在真实负载宿主上不可复现且方向不稳定, 建议改相对/CPU-time 度量。
- MINOR 2 项: 段数断言方法论 (NUL/数组基数, 不用 wc -l) 应写入 SC-4 实现说明; 空段处理建议显式 skip (非必须, 无害)。
- Positive: has_filter 现有 9 类管道锚定判据逐段求值语义保持正确, 是"管道不是边界"这条设计的直接受益; 2 类非锚定判据逐段化后被精确化, 不是新回归; quote-aware 分段器在纯 bash 下可行, 原型对拍 proposal 引用的全部关键语料 (SC-4 两条 / SC-1 核心 / 管道保留 / 转义) 均正确。

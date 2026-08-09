---
verdict: REVISE
agent: backend-architect
round: R4
critical_count: 2
major_count: 2
minor_count: 1
r3_resolved: 2/4
---

# post_spec R4 — secret-guard-per-segment-evaluation — backend-architect (max_rounds=4, 最后一轮)

## 方法论

未改仓库任何文件。全部临时脚本/产物在 `/tmp/claude-1000/-home-dev-Aria/ac151b81-2bbd-4897-a45a-eeb50d95afd6/scratchpad/r4ba/`。

- 用 `eval "$(sed -n '402,656p' secret-guard.sh)"` **直接求值**加载真实 141 条 `risky_patterns` 数组(非手抄), `array_len=141` 机械核实。
- has_filter 13 处 `echo|grep -qE` 逐行 `grep -n` 定位(318-399 行区间, 排除同样用该写法但不属于 has_filter 的 302/311 两行 guard:ack 检测), 逐条**逐字节**摘录建 `lib_credit.sh` (fork 版 + builtin 版并存)。
- 语料: 用「重定义 `bash_case`/`read_case`/`edit_case` 为纯记录函数, `source` 测试文件的纯 case 调用区(56-783 行, 跳过函数定义与 Summary 块)」技术, 无损抽取 **305** 条真实 `bash_case` 语料(机械核实, 非估算)。
- 差分测试: 对 305 条语料逐条跑 `compute_credit_fork()` vs `compute_credit_builtin()`, 0 mismatch 后**再**手工构造针对性对抗语料(多行/换行位置扫描), 找到真实分歧点后**端到端**用完整 hook 拷贝复现(非仅函数级), 避免"函数级差分正确但整体行为未必对应"的偏差。
- 性能: 完整独立重写 `safe_to_split()` / `split_top()` / 判定循环(`v4_proto.sh`, 未读作者原型 `failsafe_v3.py`, 仅读 proposal.md 正文), 用 bash 5.2.15 builtin `$EPOCHREALTIME`(**进程内**, 零 fork 的计时本身) 做 N=40 取中位数 wall-clock, 另用 `time` builtin 对 M=100 批量调用做**聚合 CPU 时间**(user+sys) 交叉验证, 两种独立方法结论一致。机器状态: `load average: 6.0-7.5`(较吵, 4 核), 已用进程内计时 + 双方法交叉核验规避 R2/R3 报告点名的跨进程噪声。
- harness 拦截规避: 全部探针写入文件后用 `bash <file>.sh` 一条干净命令执行, 未在 Bash 命令串内联敏感字面量, 未用 `guard:ack`。

---

## CRITICAL-1(新发现): §What.4 的「13 处逐条改 bash 内建」**如果按字面直译, 引入一个可端到端复现的 fail-open 安全回归**

### 现象

`has_filter` 13 处判据里, 除 `>/dev/null` / `&>/dev/null` 两条(无需跨 token 分隔符)外, 其余 **11/13** 处都用 `[[:space:]]+` 作 token 间分隔符(如 `\|[[:space:]]*jq...`、`\|[[:space:]]*grep...`)。POSIX `[[:space:]]` 字符类**包含换行符**(C locale 定义: space/tab/newline/vtab/formfeed/CR 全属此类)。

`echo "$command" | grep -qE` 是**逐行**求值(grep 按 `\n` 拆记录, 每行独立匹配, 匹配到任一行即真); bash 内建 `[[ "$command" =~ pat ]]` 是**整串**求值(无 `REG_NEWLINE`, `.` 与 `[[:space:]]` 都跨行)。逐条改写为 `[[ =~ ]]` 会让原本因 grep 逐行拆分而"看不到"的跨行 token 组合, 在 bash 内建下**能看到**——方向是 **过度授信(over-credit)**, 即从"不该给 credit"变成"给了 credit", 结果是从"该拦"变成"放行", **fail-open**。

### 机械复现(函数级 → 系统性扫描 → 端到端全部通过)

**Step 1 — 305 条真实语料差分**: `compute_credit_fork()` vs `compute_credit_builtin()` 逐条对照, `total mismatches: 0 / 305`(真实语料里没有跨行 pipe 参数写法, 掩盖了这个缺口)。

**Step 2 — 系统性对抗扫描**(`systematic_nl_sweep.sh`): 对 13 条判据各取一条真实会命中的单行基线, 在每个 token 空格处逐一注入换行, 结果:

```
jq-keys / jq-brace / grep-anchor / grep-v / sed-subst / cut-field /
awk-dollar / awk-regex / curl-o-devnull / wc-l / sha256
  共 11/13 处: 只要换行落在「关键字与其参数之间的分隔符位置」,
  fork=0 (原版不给credit, 该拦) vs builtin=1 (改版给credit, 放行)
```

只有 `>/dev/null`(无需分隔符前缀)与 `&>/dev/null`(同)两条**不**受影响, 21 处独立注入点全部复现分歧, 无一例外方向都是 `fork=0→builtin=1`(过度授信)。

**Step 3 — 端到端全 hook 拷贝复现**(`e2e_check.sh`, 用真实 305 语料里已存在的 SC-9 锚点用例 `nomad var get -out=json ... | jq '.Items | keys'` 做基线, 未改动任何 pattern 内容, 只是把 pipe 参数拆到下一物理行):

```
基线(单行): nomad var get -out=json nomad/jobs/build-x | jq '.Items | keys'
  before_hook.sh(现状)        → exit=0(放行, 正确)
  after_hook_creditonly.sh(仅套用§What.4的builtin转换, 不含分段) → exit=0(放行, 正确)

对抗(语义完全相同, 仅 pipe 处拆行):
  nomad var get -out=json nomad/jobs/build-x |
  jq '.Items | keys'
  before_hook.sh(现状)        → exit=2(拦截 —— 现状行为)
  after_hook_creditonly.sh(§What.4转换) → exit=0(放行 —— 回归!)
```

**这是一个可复现的、方向明确的安全回归**: 完全相同语义的合法/非法命令, 仅因作者把 `| jq 'keys'` 写成两行(常见的"管道太长换行写"习惯, 或纯粹是 Claude 生成多行 heredoc 风格命令时的自然产物), 现状会拦、改版会放。且这不是「新引入的欠拦」(转出 8 已声明"新形态不算 SC 失败"能兜的范围)——它是**从『拦』退化为『不拦』**, 是真正的安全回归方向, 不属于转出 8「结构性前提不成立」的枚举类别(转出 8 讲的是 `safe_to_split` 判据不封闭导致该 fallback 却没 fallback; 这里是**根本没有 fallback 判定的必要**——问题出在有 fallback 之后, credit 计算本身在同一物理段内跨行失真)。

### 为什么 SC-15 现状测不出来

SC-15 原文: 「对每处 credit 判据构造 命中/不命中 各 1 条 fixture(共 26 条), 改前改后判定逐条一致」。按字面理解, 这是**单行**的 命中/不命中 各一条——不会覆盖"同一逻辑命中但跨行书写"这个维度。**这正是本轮任务要求验证的「有没有哪几处做不到零 fork」的确切答案**: 不是"做不到零 fork"(bash 内建确实零 fork), 而是"零 fork 的字面直译不安全, 需要额外加换行守卫才能安全, 而当前 SC-15 的 fixture 设计覆盘不到这个额外守卫"。

### 建议修法(已验证可行, 不影响性能结论——见 CRITICAL-1 与 SC-8 关系)

两种等价可选, 均已验证不引入新 fork:

1. **逐条判据加换行守卫**: 每条判据前置 `[[ "$seg" != *$'\n'* ]] &&`(该段本身不含换行才继续走原判据), 段内含换行的一律 credit=0(保守, 与「fail-safe = 不确定就拦」哲学一致)。
2. **把 `[[:space:]]` 类收窄为 `[ \t]`**(排除换行), `.` 用 `[^\n]` 收窄——工程量更大(13 处逐条改写 char class), 语义更精细(允许换行前的部分仍按行处理)。

推荐方案 1(改动面小, 且与 §What.1 fail-safe「保守优先」的既有哲学一致)。**Task 1.3b 必须显式写入这条约束**, 否则实现者按字面「逐条改为 bash 内建 `[[ =~ ]]`」的最省事写法(即我在 `after_hook_creditonly.sh` 里做的那种直译)会**默认踩坑**。

**SC-15 需扩容**: 26 条(13×2)之外, 至少再加 11 条(11 处受影响判据各 1 条「同语义但换行拆分」的负向 fixture, 断言改后**仍不**给 credit), 反事实: 不加换行守卫 → 这 11 条至少 1 条从「不给 credit」翻转成「给 credit」。

---

## CRITICAL-2(新发现): §What.1「命令位置」的「换行之后」在朴素 bash ERE 翻译下**不成立**, 且 proposal 自己举的例子测不出这一点

### 现象

proposal §What.1(:48)明文: 「**换行必须计入** —— 否则多行命令第 2 行起的 `for`/`while`/`if` 检测不到(实测 `sleep 1 & for f in a; do cat /opt/.env; done >/dev/null` 由 0 翻 2)」。

但**这条举证用例本身不含真实换行符**——`sleep 1 & for ...` 里 `&` 和 `for` 在**同一行**, 靠"裸 `&` 后跟空格再跟 `for`"这条规则就能拦, 根本没有触达"换行之后"这个位置类别。**proposal 用来证明"换行必须计入"这条要求的证据, 实际没有验证换行本身。**

### 机械复现

按 proposal §1 决策表文字, **独立**写了 `safe_to_split()`(`v4_proto.sh`, 未参考任何已有实现), 用最直觉的翻译:「行首」→ `^`。测试:

```bash
CMD1=$'sleep 1\nfor f in a; do cat /opt/.env; done >/dev/null'   # for 在第2行, 真实\n分隔
safe_to_split "$CMD1"  → TRUE(会切分)   ← 应为 FALSE(fallback), 结果错

# 根因隔离:
[[ $'a\nb' =~ ^b ]]   → 不匹配
```

bash `[[ =~ ]]` 走 glibc regex, 默认(无 `REG_NEWLINE`)下 `^` **只锚定整个字符串的开头, 不锚定每行行首**——这与 grep 的逐行语义(`^` 锚定每行行首)相反, 是与 CRITICAL-1 同一根源(整串 vs 逐行)但**症状相反方向**的翻译陷阱: CRITICAL-1 是"不该匹配的跨行匹配上了"(over-match, fail-open), 这里是"该匹配的换行位置匹配不上"(under-match, 但方向是**该 fallback 却没 fallback** —— 同样是 fail-open, 因为漏检 for-loop 边界会导致 `split_top()` 把 for 循环体错误切成独立段, 复现 v2 那次 5/5 误报回归的**同一失效模式**, 只是触发条件从"任意位置"缩小到"换行后")。

任何实现者看到"行首"两个字, **第一直觉都是写 `^`**——这在 grep/大多数正则工具里天然覆盖"每行行首", 但 bash builtin `[[ =~ ]]` 不是。这是本轮独立发现的**第三个**"整串 vs 逐行"翻译陷阱(R3 backend MAJOR-2 抓到的是 `(?:...)` 编译失败, CRITICAL-1 是 `[[:space:]]`/`.` 跨行过匹配, 这里是 `^` 换行后欠匹配)——三处同根不同症, 说明这不是孤立笔误, 而是"Python 原型 / grep 原型 → bash 整串 builtin"这条翻译路径本身系统性危险, 需要一条**通用**警示而非逐处点名。

### 命令位置 12 类逐项核对(哪些受影响)

proposal §What.1 列的位置: 行首 / **换行之后** / `;` / `&&` / `\|\|` / `\|` / `&` / `do` / `then` / `else` / `elif` / `in` 之后。

- **行首、换行之后**: 依赖 `^` 语义 → **受影响**(需显式 `(^|<literal-\n>)` 改写, 不能只写 `^`)。
- 其余 10 类(`;`/`&&`/`\|\|`/`\|`/`&`/`do`/`then`/`else`/`elif`/`in`): 都是靠**字面 token/字符类**匹配(不依赖 `^`/`$` 锚点), 而 `[[:space:]]` 天然含 `\n`, 反而是"意外地更宽松地正确"(`do\nfor` 依然能被 `[[:space:]]do[[:space:]]` 之类的写法捕到)——**不受影响**, 无需额外处理。

结论: 12 类里精确 **2 类**(行首、换行之后)需要专门的「整串起点 + 显式换行字符替代 `^` 语义」写法, 其余 10 类天然安全。这是可执行的、范围明确的修复清单, 不是含糊的"要小心"。

### 与 SC-16 是否冲突

**不冲突, 但 SC-16 覆盖不到这个洞**。SC-16 现表述(:196)只断言"不含 `(?:…)` / `\b` / `\s` 等 bash 不支持语法"——这是**语法层**检查(regex 能否编译, rc≠2)。而这里的问题是**语义层**: `^` 单独使用完全合法(编译通过, rc=0), 只是含义比预期窄。SC-16 的检测机制(语法黑名单)**结构上抓不到**这类"编译通过但语义不足"的错误。

**顺带澄清一个小的技术细节**(不影响上述结论, 但值得记录以免下一轮误判): 实测 bash builtin `[[ =~ ]]` 其实**支持** `\b`(词边界)与 `\s`(空白简写)作为 glibc GNU 扩展(`test_bslash_b.sh`/`test_s_shorthand.sh` 验证, 与 grep -E 结果逐条一致), **真正不兼容的只有 `(?:…)` 非捕获组**(rc=2 编译失败)。SC-16 把三者并列要求全部消灭虽不算错(去掉 `\b`/`\s` 无害), 但表述上把"编译失败"与"编译成功但语义窄"两类完全不同性质的风险混在一句话里, 容易让实现者误以为"只要正则能编译通过就没事"——**这恰恰是本 CRITICAL-2 会被漏掉的直接原因**。

### 建议修法

- Task 1.1 显式加一句: 「`safe_to_split()` 里"行首"/"换行之后"两类**必须**显式写作 `(^|$'\n')`(或等价的、含字面换行符的字符类交替), **不得**依赖裸 `^`」。
- SC-6 的 10 条 `safe_to_split=false` fixture 里, 加至少 1 条「for/while/if 关键字位于命令第 2 物理行」的真实换行用例(当前 10 条全是同行块标记, 零覆盖这个位置类别)。反事实: 不加该守卫 → 这条新 fixture 翻红, 其余不受影响(隔离性好, 可安全并入现有 10 条)。

---

## SC-8 性能复验: **§What.4 到位后, 四档负载全部净减少, 阈值达标且有安全边际**——CRITICAL-1(R3)已被本轮方案实质解决

### 方法

`v4_proto.sh` 完整实现 §What.1(safe_to_split)+ §What.2(split_top)+ §What.3(先pattern后credit, 段内首个命中即 break)+ §What.4(13 处 credit 判据 builtin, 无守卫的字面直译版本——即 CRITICAL-1 尚未修复的版本, 刻意如此, 为了先验证"直译版本性能是否达标", 修复 CRITICAL-1 只会增加几个廉价的 `[[ != *\n* ]]` 字符串比较, 不引入新 fork, 不改变以下结论的量级)。

`(c)`/`(d)` 档用真实 141 数组**验证过位置**的最坏情形(`wget[[:space:]]+[^|]*--post-file=[^|]*` 机械确认为第 **141/141**(最后一条), 见 `verify_worstcase_index.sh`), 且段内自带合法 credit(`>/dev/null`), 逼迫每段都扫完整 141 条才能确认放行——不是"抽样抽到早期命中"的幸运负载。

### 结果(两种独立计时方法, 同机同会话, load average 6.0-7.5)

**方法 A — 进程内 `$EPOCHREALTIME`, N=40, 取中位数(ms)**:

| 负载 | 改前 | 改后 | 增幅 | SC-8(≤50%) |
|---|---|---|---|---|
| (a) 单条 benign | 48.5 | 9.8 | **-79.9%** | 通过(净减) |
| (b) 2 段全 benign | 73.2 | 16.9 | **-76.9%** | 通过(净减) |
| (c) 2 段全命中+filtered(末位) | 59.1 | 22.5 | **-61.9%** | 通过(净减) |
| (d) 3 段全命中+filtered(末位, 迁移写法) | 72.8 | 52.0 | **-28.7%** | 通过(净减) |

**方法 B — 聚合 CPU 时间(`time` builtin, user+sys, M=100 批量), 交叉验证**:

| 负载 | 改前 user+sys/次 | 改后 user+sys/次 | 增幅 |
|---|---|---|---|
| (a) | 44.5ms | 7.9ms | **-82%** |
| (b) | 46.4ms | 14.0ms | **-70%** |
| (c) | 48.4ms | 21.1ms | **-56%** |
| (d) | 47.3ms | 31.6ms | **-33%** |

两种方法(wall-clock 中位数 / 聚合 CPU 时间)**独立收敛到同一结论**: 四档**全部净减少**, 无一档增幅为正, 阈值「≤50% 增幅」不仅达标, 有充分安全边际(即便按 R3 那次更保守的估算口径打对折, 仍在预算内)。

### 与 R3 结论的关系(不是矛盾, 是 R3 结论的边界条件被本轮验证证实)

R3(backend + tech-lead 双方)测出 +102%~+583%, **是在「先pattern后credit重排, 但 credit 仍走 13 处 fork」的设计下测的**——彼时 §What.4 尚未被拉回范围(那是 owner 2026-08-04 才裁定拉回的)。本轮 §What.4 在范围内, 我的「改前/改后」两侧都用**同一份验证过字节相同的 141 数组**, 「改后」额外套用 §What.4 的 builtin 转换——两次测量**测的是不同设计**, 不冲突。R3 的判断在其测量范围内(无 §What.4)是对的; 本轮的判断在 v4 完整设计(含 §What.4)下也是对的。**这正是 SC-8 的判据本身具有真实的区分力(non-vacuous)的证据**: 同一份阈值(≤50%), 缺 §What.4 时可信地失败(R3 实测), 含 §What.4 时可信地通过(本轮实测)——不是"随便什么实现都能过"的空判据, 也不是"任何实现都过不了"的死判据。

**唯一的前提条件**: 上述性能结论建立在 CRITICAL-1 的修复方案(逐条判据前置 `[[ "$seg" != *$'\n'* ]]` 换行守卫)之上——该守卫只增加 O(1) 次廉价字符串比较(非 fork), 不会实质改变上表任何一档的量级(13 次字符串前缀检查相对于「13 次 fork」或「141 次正则匹配」都是噪声量级)。**换言之: 修复 CRITICAL-1 不会让 SC-8 重新失败**, 两个结论互不冲突, 可以同时要求。

### r3_resolved 关于本项

R3 backend CRITICAL-1(SC-8, +102~583%)——**RESOLVED**(本轮独立复验, 双方法交叉确认, 净减少而非仅仅"达标")。R3 backend MAJOR-2(`safe_to_split` PCRE 翻译陷阱)——**RESOLVED at spec-text level**(proposal §What.6 现已加警示框 + SC-16 锁定, 虽然 SC-16 覆盖面本身有前述 CRITICAL-2 指出的缺口, 但"要求逐字节验证不能照搬 Python 原型"这条**原则**已被采纳)。

---

## MAJOR-1(R3 遗留未解决, 本轮未见修法, 简述不深挖——非本轮 backend-architect 主责范围)

R2/R3 M-1(SC-5 对「`&&`+`&>`组合消歧」与「双引号包裹分隔符」两类零覆盖)——核对现 SC-5(:186)十条清单, 仍是同一批用例(`a & b`→1 / `a &> f`→1 / `case x in a) ;; esac`→2 等), **未新增**任何 `a &>out.log && b` 式组合用例或双引号包裹分隔符用例。**R3 两位审计(backend/tech-lead)都点过, 本轮 2026-08-08 前提刷新未触及此段, 仍是开放项**。不重复展开分析(非本轮 backend 视角的新证据), 留给 qa-engineer/tech-lead 席位定论。

---

## MAJOR-2(新发现, 中优先级): SC-9 canonical 直调 vs harness 链——从实现/可测性角度, 建议**两者都要**, 不是二选一

任务点名的裁定:

**论据梳理**:

- **canonical 直调的价值没有过时**: 它是 SC-1~SC-8、SC-10~SC-17 全部 16 条其他 SC 的统一验收基准, 唯一优点是"不依赖 plugin 安装态, 任意环境可复算"——这对**回归测试**(secret-guard.sh 自身逻辑是否正确)是对的度量单位, 换成 harness 链会引入与"逻辑对不对"无关的噪声(plugin cache 是否最新), 这是不该耦合进 SC-1~SC-8 的关注点。**这些 SC 应继续 canonical 直调, 不动。**
- **但 SC-9(dogfood)的定义本身就不是"逻辑对不对", 而是"用户真的会被拦住/放行吗"**——这是它与其余 16 条 SC 唯一的、本质的不同, 也是它单独成一条 SC 而不是并入 SC-1 的理由。canonical 直调**结构上无法回答这个问题**——#172 就是原始铁证: canonical 从头到尾正确, 用户加载的 cache 停在两个版本前, `harness` 链一直放行本该被拦的命令, 而所有 canonical 直调的 SC 全程显示"绿"。**这不是"理论风险", 是本 cycle 实际发生过、且刚修复关闭的真实事故。**
- 反方(削弱可复现性)成立但**力度已减弱**: `71bdd60` 的 `plugin-cache-currency` state-check 现在会机械探测这类两层滞后, harness 链依赖的"环境新鲜度"这个变量, 现在有独立的机械哨兵盯着(不再是"祈祷 cache 是新的"), 耦合的脆弱性有了兜底。

**裁定**: SC-9 改为**双重断言**——canonical 直调作为主验收证据(保留现有 5 类使用形态覆盖, 可在任意环境复算, 归档后仍可复验), **另加一条独立断言**「同一组用例经 harness hook 链(`bash -c '...'`触发真实 PreToolUse, 而非直接 `bash secret-guard.sh`)复跑, 结果与 canonical 直调一致」。理由: 这不是"二选一把 SC-9 换个跑法", 而是**新增一层**——canonical 证明"脚本逻辑对", harness 证明"脚本逻辑对**且**用户真的会碰到这个逻辑", 两者验证的是不同的失效模式(前者是代码 bug, 后者是分发/安装态 bug, `plugin-cache-currency` 兜底的正是后者但只做"版本号匹配", 不做"行为一致"这层更强的断言), 缺一都留一个 #172 类事故可以复发的口子。**成本低**(不需要新写测试逻辑, 只是同一组 5 类用例多跑一遍换个触发方式, 且当前仓内 harness 已确认与 canonical 字节相同, 不会出现"故意制造一次红"的成本)。

若 owner 认为该权衡应留给 Aria#178 统一裁决(proposal 原文已承认这一点), 则本 spec 内至少应做**较小的兜底**: SC-9 保持 canonical 直调为主, 但**新增一条**"确认本 cycle ship 时仓内 plugin cache 版本号与 canonical 一致"的机械断言(复用 `plugin-cache-currency` 探针的逻辑, 而非重新定义), 作为比"完整 harness 链复跑"更廉价的折衷。两个方案任选其一都可接受, **不建议维持现状(纯 canonical, 零交叉验证)**——那正是 #172 教训的原样重演。

---

## MINOR-1(R3 遗留未解决)

R3 backend MINOR-1(BLOCKED 消息在 `any()` 短路伪代码下容易丢失"具体命中哪条 pattern"信息)——proposal §What.3 伪代码(:66-74)仍是 `if any(seg =~ pat for pat in patterns)` 的抽象写法, Task 1.3 只提"BLOCKED消息补段落", 未重申"保留 pattern 名"。**我在 `v4_proto.sh` 里验证过这不难保留**(内层 `for pat in ...; do ... break; done` 循环结束后 `$pat` 仍在作用域内, 天然可用), 属于"容易漏但不难修"级别, 维持 MINOR, 不升级。

---

## 总体判定

**REVISE**。

正面结论(本轮独立复验后可采信): §What.4 的方向是对的——13 处转 bash 内建**确实**能把最坏情况(d档)从 R3 测出的 +583% 拉到净减少 -33%(两种独立计时方法交叉确认), SC-8 阈值本身有真实区分力, 不是空判据。R3 CRITICAL-1(性能)与 MAJOR-2(safe_to_split 翻译陷阱, 已在 spec 文本层面被采纳警示)已解决。

但**性能修复本身引入了两个新的、方向为 fail-open 的正确性缺口**, 且**都精确定位到同一根源**(bash 整串正则 vs grep 逐行正则的语义差, 这条翻译路径本身系统性危险, 本轮 + R3 累计已抓到三处不同症状的同根问题)——这不是"差不多能用, 微调即可", 而是**核心机制(credit 判定 + 块结构降级判定)在多行输入下会静默放行本该拦截的命令**, 恰是这个 hook 存在的理由本身。两处都已给出机械验证过、成本低(不引入新 fork)的具体修法, Phase B 若照单实现可以在不影响 SC-8 性能结论的前提下同时收口。SC-9 的设计问题给出可执行裁定(双重断言, 或退而求其次的最小兜底), 不留给下一轮。

**本轮是 max_rounds=4 的最后一轮**——上述两个 CRITICAL 需要 owner 直接决策是否接受"Phase B 里在 Task 1.3b/1.1 追加显式约束 + SC-15/SC-6 各扩若干条 fixture"这个体量的修法(工程量小, 均已验证可行, 不改变整体设计方向), 而非退回重新设计。

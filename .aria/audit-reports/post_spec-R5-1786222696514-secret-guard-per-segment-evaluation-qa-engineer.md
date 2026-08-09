---
verdict: REVISE
agent: qa-engineer
round: R5
critical_count: 2
major_count: 2
minor_count: 2
r4_resolved: 2/7
newly_introduced: 4
---

# post_spec R5 (超配额加跑, 全量重审) — QA 审计: secret-guard-per-segment-evaluation

审计对象: `openspec/changes/secret-guard-per-segment-evaluation/proposal.md` (274 行, v5 = R4-fix)。方法: 全部反事实用 Write 落盘脚本 + canonical `aria/hooks/secret-guard.sh` 直调实测 (`bash aria/hooks/secret-guard.sh < payload.json`, payload 用 `jq -n` 构造), 未使用 `guard:ack`。产物见 `/tmp/claude-1000/-home-dev-Aria/ac151b81-2bbd-4897-a45a-eeb50d95afd6/scratchpad/r5qa/`。**Phase B 尚未落地** (`grep safe_to_split aria/hooks/secret-guard.sh` 零命中), 故本轮对每条新改 SC 均手写"最可能的 Phase B 错误实现"变体做反事实对照, 而非跑真实现。

## 0. 先处理任务简报点名的事

R4 我审 SC-16 判其"有效, 仅表述夸大", 漏了前提核实, 被 code-reviewer 与主 loop 独立证伪。本轮我重新独立复验 SC-16/§6 的**全部**正则事实断言 (`t5_sc16_regex_facts.sh`), 结果:

```
(?:a)b  vs 'ab'     -> COMPILE-FAIL rc=2       (确认: 不支持)
\bbar\b vs 'foo bar' -> MATCH                  (确认: 支持, 真生效)
\bbar\b vs 'foobar'  -> NO-MATCH                (确认: 词边界真在过滤, 非字面 b)
a\sb    vs 'a b'     -> MATCH                   (确认: 支持)
\w+     vs 'abc'     -> MATCH                   (确认: 支持)
```

且额外验证了一条 R4 报告都没测的点: **rc=2 编译失败是静默的** (`[[ =~ ]]` 不打印 stderr) **且非致命** (`set -uo pipefail` 下 if/else 正常走 else 分支, 脚本不中止) —— 这精确支撑了 SC-16 反事实"关键字分支静默失效"的因果机制, 而不只是结果对。**结论: v5 的 SC-16 重写事实成立, 我 R4 的漏判已订正。** 本轮把"事实前提是否为真"作为每条 SC 的必查项 (见下), 这是本轮方法论的直接产物。

## 1. Critical — 新引入 (R4-fix 本身制造, v4 没有这两个错)

### C-1. SC-14 新增的 2 条 fixture 与其自身适用的验收公式**自相矛盾** —— 字面文本会让"覆盖损失"版实现合法通过

**位置**: `proposal.md:260-263` (SC-14 全段)

**问题**: SC-14 的验收公式对全部 5 条 fixture 统一适用: 「须 `safe_to_split=true` **且** exit 与改前一致」。但紧接着的解释句自己说: 对 R4 新增的 2 条, "词边界读法 (exit=2, **正确**) 与子串读法 (exit=0, **覆盖损失**)"。

**实测「改前」**(`t1_sc14_baseline.sh`, canonical 直调):

```
echo runtime; cat /opt/.env; true >/dev/null            -> exit=0
timeout 5 curl x; cat /opt/.env; true >/dev/null        -> exit=0
控制组: cat /opt/.env (无 credit, 单独出现)               -> exit=2
```

「改前」确认为 0。而 SC-14 自己说"正确"实现应产出 exit=**2**（因为 `cat /opt/.env` 在正确的逐段判定下是独立段、无本段 credit，属于本 spec 存在的理由本身 —— Aria#170 同构泄漏）。**2 ≠ 0**，即"正确"实现不满足「exit 与改前一致」这条字面要求。

这不是文字瑕疵，是**验收公式本身指向错误方向**：一个刻意 (或疏忽) 保留子串匹配、让这 2 条命令继续走 fallback (从而 exit 仍为 0) 的"覆盖损失"实现，字面上**完全满足** SC-14 —— `safe_to_split` 是否等于 true 这半句可能仍需检查，但若该实现是"exec/time 子串命中即 fallback"，`echo runtime` 会被误判含 `time` 子串而**同样触发 fallback**，safe_to_split 也会是... 需具体看实现，但至少「exit 与改前一致」这半句会误导实现者朝错误方向优化，且不存在任何其他 SC 补位 (spec 自己写"SC-1/3/6/11 与全语料全部零鉴别力")。

**反事实构造** (verified, `t1_sc14_baseline.sh` 输出见上): 若 Phase B 实现者把 SC-14 的验收公式读作对 5 条 fixture 统一生效 (文本没有给出任何分组差异化说明), 并因此把 R4-C-2 警示的"子串读法"实现出来 (即含 `runtime`/`timeout` 子串就整条 fallback) —— 该实现对这 2 条新 fixture 产出 exit=0，**与"改前"完全一致**，SC-14 按字面判定 **PASS**；但这正是 R4-C-2 定为 Critical、要求杜绝的那个"覆盖损失"实现，静默保留了 Aria#170 同构的泄漏路径。SC-14 本应是唯一能拦住这个具体缺陷的锁，现在这把锁的钥匙孔和它要防的贼手型一致。

**建议改法**: 拆分验收公式 —— 「原 3 条须 `safe_to_split=true` 且 exit 与改前一致 (无风险段, 用于验证过度触发方向不误伤); R4 新增 2 条须 `safe_to_split=true` **且 exit=2** (由改前 0 变为改后 2, 印证词边界读法生效而非覆盖损失)」。当前文本把两种不同性质的断言塞进同一个公式, 是 R3-M-3 "两层职责混淆" 同款错误的第三次变体 (第一次是 SC-5 的 `case`→1/2, 第二次是 R4-C-2/R4-C-3 举证例子里的 `&`/换行搭配错), 这次出现在**验收公式**层面, 比举证例子层面更危险 —— 举证例子错了顶多误导读者理解, 验收公式错了会让 Phase B 的错误实现拿到绿灯。

---

### C-2. SC-6 新增的 `case` fixture **结构上不可能提供鉴别力** —— spec 自己写的反事实「漏检 case → 对应条红」可被证伪

**位置**: `proposal.md:243-247` (SC-6 全段, 尤其 `:245` "R4 新增 3 条" 与 `:247` "反事实" 两行)

**背景**: 我在 R4 指出 "`case` 仅靠 `BLOCK_CHARS` 的括号巧合覆盖", 建议追加"独立于 BLOCK_CHARS 巧合的直接断言 (哪怕只是对关键字识别函数做一次隔离单元断言)"。v5 采纳的方式是把 `case` 与 `until`/`select` 并列写进"R4 新增 3 条", 并在反事实里断言"漏检 `until`/`select`/`case` → 对应 3 条红"。**这条改法没有保留我建议里"隔离单元断言"这个关键限定词, 而这个限定词恰恰是必需的**。

**结构性事实** (`t2_sc6_case_vacuous.sh` 实测):

```
$ bash -n 一个把 case 分支体写成 "a cat /opt/.env ;;" (省略右括号) 的脚本
=> syntax error near unexpected token `cat'  (右括号在 bash case 语法里不可省, 强制语法要求)
```

任何**带真实分支体**的 `case` 语句, 其模式臂 `pattern)` 语法**强制**含裸 `)` —— 这不是某种常见写法, 是 bash 语法本身不允许省略。而 `)` 正是 §What.1 判据表里 `BLOCK_CHARS` 的一员, 与 `case` 关键字检测是**两条完全独立的判据路径**。

用参照 §What.1 文字写的最小 `safe_to_split()` 实现验证 (buggy 版故意从关键字集里删掉 `case`, 只保留 `for|while|until|if|select`, 但 `BLOCK_CHARS` 检测原样保留):

```
fixture: case $x in a) cat /opt/.env ;; esac
safe_to_split (CORRECT impl, 含 'case' 于关键字集):     false
safe_to_split (BUGGY impl,  'case' 从关键字集里删掉):    false   <- 相同!
```

两个实现在这条 fixture 上**产出完全相同的结果** —— 因为 `)` 已经独立触发了 `BLOCK_CHARS` 判否, `case` 关键字检测这条代码路径根本没被这条 fixture 执行到就已经"蒙对了答案"。作为对照, 我同时验证了 `until` (无 `BLOCK_CHARS` 字符, 真实依赖关键字检测):

```
fixture: until nomad var put secret/x @f >/dev/null; do sleep 1; done
CORRECT: false ; BUGGY (漏检 until): true   <- 正确地区分开, 会让对应 SC-6 fixture 转红
```

**这直接证伪了 spec 自己写的反事实「漏检 `until`/`select`/`case` → 对应 3 条红」**——对 `case` 而言, "漏检 case" 这个 bug **不会**让任何 SC-6 fixture 转红 (只要 fixture 写的是任何带真实泄漏体的 case 语句, 而不写这种带真实体的 fixture 本身就不构成有效测试)。三条里只有 2 条 (`until` / `select`) 真的具有反事实提到的隔离鉴别力。

**为什么这是"自我确认风险"的教科书案例** (任务简报点名的镜头): 我在 R4 提的建议是对的方向, 但建议里"哪怕只是隔离单元断言"这个限定词是**建议能成立的必要条件**, 而不是可选修饰。v5 的作者把"加 case fixture"这个动作字面执行了, 却没有意识到——也没有人在 R4-fix 阶段验证过——常规 end-to-end fixture 对 `case` 这一项**结构上做不到**我建议的效果。这不是"照我说的改了但改法不够用"的一般情况, 是"我给的建议本身在一种条件下不成立, 而这个条件恰好总是成立"。

**建议改法**: 三选一, 且必须明确择一 (不能再用一句"R4 新增 3 条"笼统带过):
1. 把 `case` 从"端到端 SC-6 fixture"移除, 改为**对关键字识别的内部函数/正则做隔离单元断言** (若 `safe_to_split()` 内部关键字检测被拆成可单独调用的辅助函数, 直接断言该函数对含 "case" 的字符串返回真, 不经过完整 `safe_to_split()`/`BLOCK_CHARS` 路径);
2. 明确承认 `case` 在 SC-6 层面就是巧合覆盖、不作为独立鉴别信号, 转而在 Task 1.1 写一条**代码审查级**约束 (如 "BLOCK_KW 正则字面量必须显式含 case, 由 code review 而非 SC 保证"), 不再声称 SC-6 的 case 分支有验证力;
3. 若坚持端到端 fixture, 必须换成能规避 `BLOCK_CHARS` 巧合的构造 —— 但经语言层核验, **这在 bash `case` 语法下不存在** (选 1/2 之一是唯一出路)。
无论选哪条, SC-6 的反事实行**必须删除或改写**"漏检 case → 对应条红"这句 —— 现状是 spec 文本自证的假论断, 与本 cycle 反复出现的"恒绿断言"是同一类缺陷, 只是这次连"制造这条 SC 的人"自己给出的反事实都是错的。

---

## 2. Major

### M-1. SC-8 仍未覆盖「pattern 数组靠后位置 + 每段均 filtered」的最坏档 —— R4-M-2 只被部分修复

**位置**: `proposal.md:249-251` (SC-8 全段)

R4-fix 为 SC-8 补了"测量口径也须写死"一句 (解决 R4-M-2 前半: U1/U2 两种口径横跨 50% 闸的问题), 但 tech-lead 在同一条 R4-M-2 里提出的**后半个问题**——"四档全是便宜类, R3 backend 点名的最坏类 (命中数组靠后 pattern + 每段 filtered) 不在表内"——**完全没有被处理**。当前四档 (a)(b)(c)(d) 的文字里, (c)(d) 只写"全命中 pattern", 未写死命中的是数组哪个位置、每段是否都要过滤判定。

**独立实测** (`t3_sc8_worstcase_sanity.sh`, 用真实 141 条 pattern 数组, 不依赖 Phase B 代码):

```
先确认 wget --post-file 确实是 141 条里的最后一条 (python 定位, 精确核实): index 141/141

真实 141-pattern 数组, N=200 取均值, 单段扫描耗时 (bash [[ =~ ]] 内建, 零 fork):
  EARLY match (~第 3 条, nomad var get)   : 2210.3 us
  LATE  match (第 141 条, wget --post-file): 21683.6 us
  NO match (扫完全部 141 条)              : 10835.6 us

8 段模拟 (纯按位置差异折算, 未含分段/credit 逻辑本身):
  8 段 x early-match: 17132 us
  8 段 x late-match:  159727 us
  比值: 9.32x
```

**这直接支撑 tech-lead R4 report 里独立实现测出的 "8 段靠后命中 -> +60%, 破 50% 闸" 具备现实基础** —— 我用真实 patterns 数组 (非 tech-lead 重写的版本) 独立复现了"位置显著影响单段扫描成本"这一根因, 且比值 (9.3x) 与 tech-lead 报告里 (a)-(d) 各档"便宜"和"靠后命中最坏档"之间的成本级差同方向。

**反事实**: 若 Phase B 实现只用 SC-8 现有 (a)-(d) 四档验收 (均可选用数组前几条便宜 pattern 满足 "全命中"), 一个在**早期 pattern 匹配路径**性能达标、但对**靠后 pattern (idx 90-141, 覆盖 K8s/DB-dump/exfil 那批) 逐段扫描无优化**的实现, 会完整通过 SC-8 四档, 而在真实迁移写法遇到靠后 pattern 时于生产环境劣化 (tech-lead 测得 8 段靠后命中 +60%, 直接破 50% 阈值)。SC-8 判据字面上"负载写死"看似解决了 R3-C-3 的问题, 实际只写死了负载**段数**, 没写死负载**命中哪条 pattern**, 后者恰恰是决定成本的主变量之一 (9.3x 差异)。

**建议改法**: 补第五档「N 段命中数组靠后 pattern (idx>90) 且每段自带 filtered token (逼迫扫完整 141 条才能判定放行)」, 并写死具体 N 与命令串 (可直接采用 tech-lead R4 报告里已验证过的 `wget --post-file=` 载荷)。同时建议标注: SC-8 现有四档 "全部净减少" 的 R4 复验结论**只对四档本身成立**, 不应被解读为"性能问题已全面解决" —— 当前文本的 "R4 复验状态" 一句容易让读者产生这种过度泛化的印象。

---

### M-2. SC-9b 是全新验收项, 但既无 Task 承载其"ship 后"执行, 也未定义 Phase B/C 期间guaranteed 会出现的 `cmp` 不一致场景的判定语义

**位置**: `proposal.md:236, 253-255` (SC-9b 全段) 对照 `:232` (Task 1.9)

SC-9b 原文自称"ship 后经 harness hook 链复验", 前置断言 "`cmp` 判定 plugin cache 副本与 canonical 字节相同"。但两个必须同时成立的操作性问题都未处理:

1. **guaranteed 的 `cmp` 不一致场景没有判定语义**。R4 code-reviewer M-5 已实测证实: 本 spec Phase B 第一步就会把 SOT 版本号从 1.65.5 bump 到 1.65.6, 而 plugin cache 只有在"merge → push → marketplace clone 刷新 → 版本 bump 后新建对应目录"这条链走完才会追上 —— 也就是说**在 Phase B/C 的整个窗口期, `cmp` 结构上必然不一致**。SC-9b 文本对"cmp 不一致时怎么判"只字未提: PASS？FAIL？跳过？R4 两位审计 (tech-lead / code-reviewer) 都独立给出了具体方案 (tech-lead: "挂 Task 1.9 或 release-closeout"; code-reviewer: "记为 BLOCKED-BY-ENV, 不判 spec 失败, 也不允许改判为 PASS"), **两条建议均未被采纳**。
2. **Task 列表里没有任何一条承接 SC-9b 的"ship 后"执行**。核实 (`grep -n "1\.9\|SC-9b" proposal.md`): Task 1.9 全文只讲"开转出 issue / 回填覆盖率声明 / close #128", 不提 SC-9b 或 harness 复验。若 SC-9b 真的要在 ship 后跑, 它需要一个 ship 后仍会被执行到的锚点 (Task 或 release-closeout 挂钩), 现在没有任何锚点。

**为什么这构成一个真实缺口而非纸面吹毛求疵**: SC-9b 被放在与 SC-1~SC-17 同一份 "Success Criteria" 列表里, 而这份列表在本方法论里是 Phase B → Phase C 的验收依据 (十步循环 B.2 执行验证)。一条"结构上只能 ship 后满足"的条目, 如果没有显式声明"不算 Phase C 合并门槛", 会被按缺省语义读作"和其余 16 条一样需要在合并前满足" —— 这正好是与 CLAUDE.md Rule #8 ("PR merge 前必跑 pre-merge gate") 及 memory `feedback_goal_hook_precondition_must_be_in_session_achievable` (session/阶段内不可达的外部前置不可写进门槛) 撞车的形态。走到这一步, Phase B/C 执行方 (若是自主 Layer 2 agent, 无人类实时在场消歧) 只有两条路: 卡死等一个结构上到不了的条件, 或者自行决定"这条其实不算数"——而后者正是 Rule #10 明令禁止 AI 自行豁免已启用闸门的场景。

**反事实**: 若 SC-9b 保持现状进入 Phase B, 一个"忠实按字面执行"的 Phase B/C 流程在 C.2 合并前检查全部 17 条 SC 时, 会在 SC-9b 上遇到 `cmp` 不一致 (guaranteed) 而没有查表可依的判定规则 —— 这不是"某个边角案例可能触发", 是**每一次**跑这个 spec 都会触发的确定性分支缺失。

**建议改法**: 落实 R4 两位建议中的至少一个 —— 优先采纳 code-reviewer 的 BLOCKED-BY-ENV 方案 (更精确, 显式区分"环境未就绪"与"真失败"), 并把"ship 后重跑 SC-9b"写成一条新 Task (如 1.9b 或挂进 release-closeout), 同时在 SC-9b 条目本身补一句"本 SC 不计入 Phase C 合并门槛, 仅 SC-9a 是 pre-merge 主闸" (若这是本意) 或反过来明确它就是主闸但允许 BLOCKED-BY-ENV 状态过闸。当前"既是 SC 又不像其余 SC 一样能在 Phase B 内满足"的悬空状态必须二选一收口。

---

## 3. Minor

### m-1. "R4 五席一致裁定" / "唯一 5/5 收敛项" 的表述, 对照我自己 R4 报告原文, 并非完全准确

**位置**: `proposal.md:16, 197, 219` (三处使用"R4 五席一致裁定"/"5/5 收敛项"描述 SC-9a/9b 拆分)

R4 汇总报告 (`post_spec-R4-*-aggregated.md`) 把"留给 R4 的 SC-9 设计问题"记为"本轮唯一 5/5 收敛的议题", 并把我 (qa-engineer) 的"时序矛盾"论据列为支持"拆两腿"方向的一条互补论据。但重新核对我自己 R4 报告原文第 6 节, 我的**裁定原句是**"保留 canonical 直调, 不改走 harness 链", **建议原句是**"SC-9 保留 canonical 直调不变, 但补一句边界声明", 并明确"部署态的持续正确性由 state-check `plugin-cache-currency` 把关...二者结构上互补, 不是替代关系" —— 即我的方案是**单条 SC + 依赖既有探针**, 明确不同于最终采纳的"拆成 SC-9a + SC-9b 两条独立 Success Criteria"这个具体机制。

我在"不应把 SC-9 整体换成纯 harness 链"这个更弱的命题上确实是 5/5 之一; 但在"是否需要为此新增一条独立 SC (即拆两腿这个具体解法)"这个更强的命题上, 我实际是持不同方案的一方, 不构成对这个具体解法的一致同意。

**为什么值得记**: "5/5 一致"这个表述在文中被用来**关闭进一步讨论** ("唯一 5/5 收敛项" 常规用法即是标记"无需再议")。若这个表述本身对某一具体机制的支持力度被高估, 后续读者/审计会把 SC-9a/9b 这个具体拆分方式当作已获得比实际更强的共识背书, 从而降低对 M-2 里指出的操作性缺口的警惕性 —— 这是一个真实但影响较小的问题 (机制方向本身是合理的, 我在 R4 也认可"不能整体换成 harness 链"), 故列 Minor 而非 Major。

**建议改法**: 把"R4 五席一致裁定"改为更精确的表述, 如"R4 五席一致同意不应把 SC-9 整体替换为纯 harness 链验证; 具体是否需要新增独立 SC-9b 各席方案略有差异 (tech-lead/code-reviewer/backend-architect/knowledge-manager 倾向新增独立验证腿, qa-engineer 倾向单条 SC + 复用既有 state-check), 本版采纳前者"。

### m-2. SC-6 "R4 新增 3 条" 未给出 `until`/`select` 的具体 fixture 文本, 与文档其余部分的具体化惯例不一致

**位置**: `proposal.md:245`

对照 SC-6 原 10 条、SC-14 的 5 条、SC-15 的端到端 3 条, 全部给出可直接执行的具体命令串; 唯独 "R4 新增 3 条" 只给关键字名称 (`until`/`select`/`case`), 未给具体命令。C-2 已指出 `case` 部分连"给具体命令"这条路都走不通 (结构性问题), 但 `until`/`select` 是可以给出具体、有鉴别力的 fixture 的 (我在 R4 报告里给过示例, 本轮 `t2_sc6_case_vacuous.sh` 也验证了这类 fixture 确实具备鉴别力)。留白会造成 Phase B 实现者各自构造出彼此不一致的 fixture, 增加"事后才发现某个人写的 fixture 意外撞上另一条隐藏 BLOCK_CHARS"这类问题的复现概率 (即使不是 `case` 那种必然情形, 也可能是偶然情形, 如 `select e in "a b" c; do ...`这种带引号的写法)。

**建议改法**: 把 `until`/`select` 的具体命令写进 SC-6 (`case` 按 C-2 的三选一处理), 例如: `until nomad var put secret/x @f >/dev/null; do sleep 1; done` (safe_to_split=false) / `select e in prod dev; do nomad var put secret/$e @f >/dev/null; done` (safe_to_split=false)。

---

## 4. 本轮验证到但确认无恙的项 (供 owner 参考, 避免误读为"未查")

- **SC-16 / §6 全部正则事实断言**: 独立重验 5 项核心断言 + 1 项额外机制验证 (rc=2 静默不致命), 全部与 v5 文本一致, 我 R4 的漏判已订正 (§0)。
- **SC-6 R4-C-3 换行 fixture**: `t6_sc6_newline_bare_caret.sh` 独立复验, 裸 `^` 实现确实漏检 (报告 NO), 正确 `(^|\n)` 实现正确检出 (报告 YES), 且对同行 `for` fixture 无副作用 (隔离性good, 与 spec 声称一致)。
- **SC-15 三条端到端 fixture 的"改前"值**: `t4_sc15_fixtures_baseline.sh` 实测, `jq keys⏎echo done`=0 / `cd /tmp⏎jq keys⏎echo finished`=0 / `awk 内嵌换行`=2, 三项与文本一致。
- **SC-15"扩容2"分支覆盖缺口**: 用全新 grep 重新核对 (非复用 R4 产物), `sha256sum` 单分支覆盖 / `jq keys` 单分支覆盖 / `wc -l` 单分支覆盖, 现状与 R4 一致, "扩容 2" 的处置要求 (逐分支各 1 条) 是可执行、非空转的修法。
- **SC-7 KNOWN-LIMIT 两形态**: 实测"改前" (`;` 与 `&&` 两形态) 均 exit=2, 与 spec 隐含的"2→0"迁移方向一致 (非本轮改动, 抽验确认无漂移)。
- **SC-12 guard:ack 命令级**: 实测复合命令 + ack 注释仍 exit=0, 与文本一致 (未改动项抽验)。
- **SC-17 重复用例**: `grep -n "FP-fix timeout run-env"` 仍命中 `:641`/`:673` 两处, 问题依然存在 (未改动项, 与 spec 描述一致, 待 Phase B 处理)。
- **转出清单 1-9 与 Task 1.9 的一致性** (knowledge-manager R4 Critical-1): 核对现文 `1、2、3、4、5、8、9` 与转出清单当前状态 (6/7 已注销) 完全吻合, 该项已正确修复。
- **数字口径**: 305 条 `bash_case` 计数复核 (`grep -c '^bash_case '`) = 305, 与文本一致。

---

## 5. 结论

R4-fix 在**它明确针对的问题**上修复质量高: SC-16 事实前提勘正彻底且我已独立重验通过, SC-6 的换行/until/select 三个新方向里两个 (until/select) 真实生效, SC-15 的换行扩容与分支扩容都是可执行的实质修法, 转出清单与 Task 1.9 的自相矛盾已修复。

但本轮全量重审在**R4-fix 自己新写的文本**里发现 2 条 Critical: (1) SC-14 新增 2 条 fixture 与其验收公式方向相反, 字面判定会放行 R4-C-2 点名要堵的"覆盖损失"实现; (2) SC-6 新增的 `case` fixture 因 bash 语法强制含 `)` 而结构性地不可能提供鉴别力, spec 自己写的反事实断言可被证伪。两条都精确复现了本轮任务简报开头点名的模式 —— **反事实完备的表述, 建立在一个可被当场证伪的事实/结构假设上**, 且都是"勘正引入新错"(本 cycle 第五、六次同类)。另有 2 条 Major (SC-8 未覆盖靠后 pattern 最坏档; SC-9b 无 Task 承载且未定义 guaranteed 出现的环境未就绪判定) 和 2 条 Minor。

**仍恒绿的 SC 数**: 2 条 (SC-14 对其新增的 2 条 fixture 是恒绿的, 在"覆盖损失"实现下不会转红; SC-6 的 `case` 分支对"漏检 case"这个具体 bug 是恒绿的, 在正确/错误两种关键字集实现下产出相同结果)。

判定 **REVISE**。全部 4 条 Critical/Major 修法都是文字/公式级 (拆分验收公式、三选一处理 case、补第五档负载、二选一收口 SC-9b 语义), 不涉及设计变更, 预计一次性可收口, 但**不建议不修就进 A.2** —— 尤其 C-1 (SC-14) 直接关系到 R4-C-2 (本轮唯一"两席独立发现、高置信"的 Critical 之一) 是否真的被验收流程兜住, 这条防线目前实际上是敞开的。

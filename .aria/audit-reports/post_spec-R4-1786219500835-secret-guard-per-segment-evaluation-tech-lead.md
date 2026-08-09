---
verdict: REVISE
agent: tech-lead
round: R4
critical_count: 2
major_count: 3
minor_count: 3
r3_resolved: 6/14
---

# post_spec R4 — secret-guard-per-segment-evaluation (tech-lead 视角, 四审 / 末轮)

审计对象: `/home/dev/Aria/openspec/changes/secret-guard-per-segment-evaluation/proposal.md` (v4 + 2026-08-08 前提刷新, 198 行, 全文读)
被审代码: `/home/dev/Aria/aria/hooks/secret-guard.sh` (`af87cae`, 698 行) + `/home/dev/Aria/aria/hooks/tests/secret-guard.test.sh` (798 行)
参照: 我的 R3 报告 + 其余四席 R3 报告 (backend / qa / code-reviewer / knowledge-manager) 全文
产物: `/tmp/claude-1000/-home-dev-Aria/ac151b81-2bbd-4897-a45a-eeb50d95afd6/scratchpad/r4tl/` — **仓库文件零改动** (本报告除外)

## 方法

本轮把「13 处转内建」当**独立可执行对象**来审, 而不是当作 spec 里的一行承诺:

1. 用 python 从 canonical `:318-401` **机械抽取** 13 条 credit 正则 (保留原始引号字节), 生成两份可运行 hook:
   - `secret-guard.builtin.sh` = 只做 §What.4 的转内建 (`echo|grep -qE` → `_sgre=RE; [[ "$command" =~ $_sgre ]]`), 其余一字未改;
   - `secret-guard.after.sh` = 完整 v4 (转内建 + `safe_to_split()` + `split_top()` + 先 pattern 后 credit + 逐段早停)。
2. 保真度自检先过: `after` 对 SC-1 五形态 **5/5 由 0 翻 2**, 对 SC-6 的 fallback 族 7/7 不变, 对 SC-14 的关键字过度触发方向 2/2 正确 —— 确认我的实现忠于 spec 后才拿它下结论。
3. 语料用「改写 `bash_case` 函数体旁路 dump」技术从测试文件精确抽 **305 条**载荷 (复制件打补丁), 四个变体逐条实跑。
4. 性能给**两个测量单位**分别报数 (这本身是一条 finding)。

harness 的 secret-guard 现为 1.65.5, 全部探针脚本用 Write 落盘后执行, **未使用 `guard:ack`**。

---

## 一、R3 逐条核销 (3C + 5M + 6m = 14 条)

| R3 编号 | v4 处置 | 判定 |
|---|---|---|
| **C-1** 命令位置清单漏 换行/`&`/`time`,「行首」二义 | 清单补 换行 / `&` / `else` / `elif` / `in`;「行首」并列「换行之后」消歧; `time`/`exec` 另起「作用域型内建」行。实测我 R3 的两组反例现已全部降级 (`cd /tmp⏎for…` 0→0, `sleep 1 & for…` 0→0) | **解决** ✓ (但支撑论据写错 → R4-M-1; 新行本身开洞 → R4-C-2) |
| **C-2** 把启发式当保证 | §What.1 加承诺强度下调 blockquote + 决策表改写 + 新开转出 8。**超出建议**: 把「新形态应扩判据表而非算 SC 失败」也写了 | **解决** ✓ |
| **C-3** SC-8 无定义负载 | 写死四档 (a)-(d) + `≤50%` + 点明转内建是达标前提。**但**四档全落在「便宜」类, R3 backend 点名的「靠后命中 + filtered」不在表内; **测量单位仍未定义** | **半解决 → R4-M-2** |
| **M-1** SC-6 12 条里 5 条零鉴别力 | 改为**直接断言 `safe_to_split()` 返回值**而非 exit code, 并写死恒 fallback / 恒 split 两向反事实 | **解决** ✓ |
| **M-2** SC-4 三条被 fail-safe 吞掉 | 换成我 R3 给的 `perl -ne 'print if /a;b/' /opt/.env`, 原三条降为辅助并标注零鉴别力。**独立复验**: canonical 整条 = 2; 引号盲切两段 = [0,0] ⇒ 切错必 0 ⇒ **可证伪成立** | **解决** ✓ |
| **M-3** SC-5 `case`→1 写反 | 改成 →2 + 注明「两层职责不可混淆」 | **解决** ✓ |
| **M-4** SC-7 只锁 `;` | 两形态 (`;` 与 `&&`) 都写进 SC-7 | **解决** ✓ |
| **M-5** fail-safe 覆盖收缩面未声明 | Impact「覆盖率」仍只列块结构 + 省略号; 无转出。**且被新增的 exec/time 行放大** (实测语料 16+5 条被迫 fallback) | **未解决 (第二轮) → R4-M-3** |
| **m-1** bump 前 re-check 落成 task | Tasks 1.1–1.9 仍无 | **未解决 (第四轮)** |
| **m-2** BLOCKED 回显段落自身可能含 secret | 全文仍未提 | **未解决 (第四轮)** |
| **m-3** 决策表加「手写 bash 扫描 vs 外部解析器」 | 决策表 7 行, 仍无 | **未解决 (第四轮)** |
| **m-4** 转出 1 的 `[^\|]*` 记号 | 仍写「81 条 `[^\|]*` pattern」。机械复算: 严格 `[^\|]*` = **79**, `[^\|]+` = **7**, 任意形态 = **81** | **未解决** |
| **m-5** §3 伪代码 `pat` 未绑定 / BLOCKED 取哪条 pattern 未定义 | 伪代码原样, 仍 `any(...)` + `BLOCK(pat, seg)` | **未解决** |
| **m-6** 305 分母定义 | §6 写死了口径 (quote-aware / 顶层记号 / 换行单列), Impact 写「305 条 `bash_case`」= 事实上的分母; 但 `corpus_census.py` 契约里没写死 | **半解决** |

**核销结果: 6/14 干净解决** (C-1 / C-2 / M-1 / M-2 / M-3 / M-4), 2 条半解决, 6 条未解决。

值得记一笔: **v4 是四版里第一次把「锁」而不只是「诊断」改对的一版** —— M-1/M-2/M-3/M-4 四条全部落成可证伪的 SC, SC-6 改成断言分支返回值、SC-4 换成实测可证伪的 fixture, 都是照 R3 给的具体方案落地; 新增的 SC-14/SC-15/SC-16/SC-17 也分别回应了 code-reviewer 的 `done` 论据问题、owner 拉回范围的验收、backend 的 POSIX ERE 陷阱、qa 连喊三轮的语料重复。我 R3 结论里那句「诊断被采纳进散文, 可执行的锁被丢掉」在本版**首次不成立**。

但 m-1 / m-2 / m-3 / m-4 / m-5 五条仍是**零处置**: 既没落 task/SC, 也没写「驳回 + 理由」。其中三条已连续四轮。

---

## Critical

### R4-C-1 「13 处转内建」不是语义保持变换 —— `grep` 逐行 vs bash `[[ =~ ]]` 整串, 在多行 command 上**双向翻转**, 其中一条是漏拦 (安全回归); 而 SC-15 的 26 条 fixture 与 SC-11 的全语料**结构上都抓不到**

§What.4 把 13 处 credit 判据从 `echo "$command" | grep -qE RE` 改为 bash 内建, SC-15 的验收是「每处构造 命中/不命中 各 1 条 fixture (共 26 条), 改前改后判定逐条一致」。这个验收隐含一个前提: **同一条正则在 grep 与 bash `[[ =~ ]]` 下等价**。该前提对单行输入成立, 对**多行输入不成立**, 而多行 command 恰恰是 `#157` 专门修复才得以完整送达 hook 的形态 (canonical `:121-130` 注释即此事)。

两处引擎级差异:

- `grep` 逐**行**匹配, `^` / `$` 锚定每一行; bash `[[ =~ ]]` 对整串匹配, `^` / `$` 只锚定串首串尾。
- POSIX ERE 的 `.` 与负字符类在 bash `[[ =~ ]]` 下**跨换行**; 在 grep 下不可能跨行。

机械对照 (13 条判据 × 8 条载荷 = 104 格, `eq_test.sh`): **2 格分歧**, 分别落在判据 idx 0 (`| jq keys|length|paths|leaf_paths` 尾锚) 与 idx 6 (`| awk '…$N…'`)。

端到端 (`e2e.py`, canonical vs 只做转内建的 `secret-guard.builtin.sh`, 6 例 3 翻):

```
case                                            canonical  转内建后
A  nomad var get nomad/jobs/x | jq keys              0         0     (单行控制组)
B  nomad var get nomad/jobs/x | jq keys⏎echo done    0    ->   2     误报 (fail-close)
C  cd /tmp⏎nomad var get … | jq keys⏎echo finished   0    ->   2     误报
D  cat /opt/.env | awk '{print $1}'                  0         0     (单行控制组)
E  cat /opt/.env | awk 'BEGIN{}⏎{print $1}'          2    ->   0     ★ 漏拦 (安全回归)
F  cat /opt/.env⏎>/dev/null                          0         0     (无分歧)
```

E 是本轮最重的一条: **今天会被拦的读 `.env` 命令, 转内建后放行**。方向与 hook 的存在理由相反。B/C 是反方向的 fail-close 误报 —— 正是 R2-C-2 被定 Critical 的那一类 (合法写法上线当天转红)。

**为什么现有验收抓不到**:

- 全语料实跑 (`corpus_run.py`, 305 条, canonical vs 只转内建): **0 条翻转**。语料几乎全是单行, 所以 SC-11「全量回归全绿」在这条缺陷上是**恒绿**。
- SC-15 的 26 条是「每处 命中/不命中 各 1」, 文字里没有一个字要求多行形态。按字面写出来的 fixture 会全绿。
- 这正是本 cycle 反复出现的形态 (memory `feedback_noop_in_test_env_hardening_needs_mechanism_assertion` + `feedback_counterfactual_test_for_every_new_sc`): 新机制配了新锁, 锁在它该抓的那一类上没有鉴别力。

**处置 (二选一, 都要配 SC)**:
1. §What.4 加实现约束: 转内建前先把 command 归一 (`${command//$'\n'/ }` 或等价), 使整串语义与逐行语义对齐 —— 注意这本身也是行为变更, 须单独验;
2. 或对含 `^` / `$` / `.` / 负字符类的判据**保留 grep** (它们不是热点: 逐段化后仍可只对命中段调用), 只转真正无锚点的那几条。
- 无论选哪条, SC-15 的 26 条必须扩为**每处 3 条 (命中 / 不命中 / 多行)**, 并把上表 B/C/E 三条写死为 fixture。**反事实**: 逐字机械替换 13 处 → B/C/E 必红。

### R4-C-2 判据表的 `exec` / `time` 那一行**没有「仅命令位置」限定** —— 按字面实现会让含 `runtime` / `timeout` / `execute` / `timestamp` 的日常命令整条降级, 修复静默失效; **无一条 SC 能分辨两种读法**

§What.1 的判据表里, 「块起始关键字」那行明确写了 **(仅命令位置)**, 而紧邻的「作用域型内建 (R3-C-1) | `exec` `time`」这行**什么限定都没写** —— 既没有命令位置, 也没有词边界。同一张规范表内两种精度, 直接产出两种实现。

实测两种读法 (`variants.py`; `wb` = 加词边界的宽容读法, `substr` = 表格字面的子串读法; 正确结果应为 2, 因为第二段 `cat /opt/.env` 无本段 credit):

```
payload                                          canonical   wb   substr
echo runtime; cat /opt/.env; true >/dev/null         0        2      0
timeout 5 curl x; cat /opt/.env; true >/dev/null     0        2      0
echo 'execute plan'; cat /opt/.env; true >/dev/null  0        2      0
ls /tmp/timestamps; cat /opt/.env; true >/dev/null   0        2      0
echo mtime-check; cat /opt/.env; true >/dev/null     0        2      0
```

5/5。子串读法下这些命令连**降级检测都到不了**关键字那一步, 直接整条 fallback = 现状泄漏。这是 memory `feedback_word_boundary_root_causes_substring_shadows` 的教科书形态, 而 `timeout` 里含 `time` 尤其致命 —— 语料里就有 4 条 `timeout …` 载荷。

**没有任何 SC 能分辨这两种实现**, 我逐条核过:

- SC-14 只锁 `for` / `if` / `case` 三个关键字的过度触发, **不含 `exec` / `time`**;
- SC-6 的 12 条不含 exec/time 形态;
- SC-1 的五条泄漏形态不含这些子串, 全绿;
- SC-3 (49 条不回归) 与 SC-11 (全量绿) 也全绿 —— 因为这类是 `0→0` 的**覆盖损失**而非回归。
- 全语料实跑坐实了这点: `wb` 与 `substr` 两个变体对 305 条语料**产出完全相同** (各 1 条翻转, 都是设计内的 `KNOWN-LIMIT` 转正)。语料对这条缺陷**零鉴别力** —— 与 spec 自己在三版表里给 v2 下的判语 (「语料零覆盖 ⇒ 回归 SC 恒绿是假绿」) 一字不差地复发在 v4 新加的这一行上。

**处置**: (1) `exec` / `time` 行补上与关键字行同款的 **(仅命令位置)** 限定 —— 语义上也只有命令位置的 `exec` / `time` 才建立 shell 级作用域, `docker exec` / `-exec` / `timeout` 里的那些根本不是; (2) SC-14 扩为覆盖**全部**判据 token 的过度触发方向, 至少加 `echo runtime; …` 与 `timeout 5 …; …` 两条 (上表实测两读法可分辨); (3) Tasks 1.1 写死该限定。

---

## Major

### R4-M-1 §What.1 第 48 行「换行必须计入」的支撑实测是**陈旧继承**, 在 v4 自己的规则下不成立 —— 举的例子里根本没有换行, 且实测不翻转

原文: 「**换行必须计入** —— 否则多行命令第 2 行起的 `for`/`while`/`if` 检测不到 (实测 `sleep 1 & for f in a; do cat /opt/.env; done >/dev/null` 由 0 翻 2)」。

两个问题:
1. 这个例子里**一个换行都没有**, 它论证不了「换行必须计入」;
2. 「由 0 翻 2」这个数是我 R3 在 **v3 规则**下测的 —— 当时 `&` 还不是降级标记。v4 采纳 R3-C-1 后把 `&` 加进了判据表, 于是该命令在 v4 下**必然走 fallback**, 无论换行计不计入。

机械验证 (`variants.py`, `wb` = 命令位置含换行, `nonl` = 不含换行):

```
payload                                       canonical   含换行   不含换行   能分辨?
spec 第 48 行那个例子                              0        0        0        NO
cd /tmp⏎for f in a b; do cat /opt/.env; done…     0        0        2        YES
echo start⏎while read l; do cat /opt/.env; …      0        0        2        YES
```

**规则是对的, 证据是错的。** 真正能支撑该规则的例子是后两条 (它们确实在两种读法下产出不同)。这是本 cycle 第四次「勘正动作里新引入错误」(R2 的 68/52 → R3 的 `case`→1 → R3 code-reviewer 抓的 `done` 论据 → 本条), 也是 memory `feedback_dec_ship_target_staleness_verify` 的形态: 上游结论在前提变更后被原样搬运。

**处置**: 换成上表后两条之一, 并在 §6 的可复算纪律里补一句「跨版本搬运的实测数字必须在**新规则下重跑**」。

### R4-M-2 SC-8 修了负载没修**测量单位** —— 同一实现同一负载, 整进程口径 +43.1%、分析段口径 +60%, 正好横跨 50% 闸; 且四档负载全是「便宜」类, R3 backend 点名的最坏类不在表内

先说好消息, 这条是**实测证实 owner 裁定有效**: §What.4 的 13 处转内建把 R3-C-3 的 +583% 彻底干掉了。SC-8 现有四档在我的 v4 实现上全部**变快**:

```
U2 = 分析段, 进程内, 25 轮均值            改前     改后    增幅
(a) SC-8 1 段 benign                      57ms     8ms    -85%
(b) SC-8 2 段 benign                      56ms    18ms    -67%
(c) SC-8 2 段全命中 (数组靠前 pattern)     59ms    14ms    -76%
(d) SC-8 3 段全命中 (= 迁移写法)           39ms     6ms    -84%
```

四档全过, 且余量极大。R3-C-3 的实质问题**已解决**, owner「根治后性能不再依赖负载分布」的判断在这四档上成立。

问题在闸门本身**结构上不可能失败**, 两层原因:

**其一, 四档全是便宜类。** (a)(b) 是 benign; (c)(d) 的 `nomad var put` 是 `risky_patterns` 数组的**第 4 条**, 先 pattern 后 credit 一扫就早停。R3 backend 点名的最坏类是「命中数组**靠后** pattern + 每段 filtered」(K8s / DB-dump / exfil 那批天然分布在 idx 90-141), 该类**不在 SC-8 表内**。实测 (末位 pattern `wget --post-file=`, 每段带 `>/dev/null`):

```
(X) 3 段靠后命中     41ms  ->  25ms   -39%
(Y) 5 段靠后命中     41ms  ->  41ms    +0%
(Z) 8 段靠后命中     50ms  ->  80ms   +60%   ← 破闸
```

**其二, 测量单位未定义, 而单位选择就能决定过闸。** SC-8 只写「四档负载各跑 20 轮取中位数, 改前改后同机同会话对比」, 没说测的是**整个 hook 进程** (含 spec 自己记录过的 jq 58ms 固定成本) 还是**分析段**。同一负载 (Z) 两种单位:

```
                              改前      改后     增幅     50% 闸
U1 整 hook 进程 CPU (30 轮批)  121.6ms  174.1ms  +43.1%   过
U2 分析段 进程内 (25 轮)        50ms     80ms    +60%     不过
```

同一实现、同一命令, 因为口径不同一个过一个不过。R3-C-1 的两项要求里「写死负载」采纳了, 但同一个病灶下移了一层。

**处置 (三项)**: (1) SC-8 写死测量单位 —— 建议整 hook 进程 CPU time (那才是用户体感, 也与 R1 已核实的「jq 58ms 是固定大头」认知一致), 并注明该单位下固定成本会稀释比值; (2) 补第五档「N 段命中数组靠后 pattern 且每段 filtered」并写死 N 与具体命令串; (3) 上面四档的实测数字请连同单位一起回填 spec (SC-8 自己要求「实测数字须写进 spec」, 而 §What.3 现存那张表是转内建**之前**的旧数, 保留会被下轮当基线继承)。

### R4-M-3 R3-M-5 覆盖收缩面第二轮未处理, 且被新增的 exec/time 行放大; 另有五条 minor 第 3~4 轮零处置

Impact 的「覆盖率 (诚实声明)」仍然只列块结构 + 一个省略号。实测语料 305 条中:

- 含 `exec` 标准 token: **16 条** (`docker exec` / `docker compose exec` / `kubectl exec` / `find … -exec`) —— 即便按最宽容的词边界读法, 这 16 条也全部被新增的 exec 行推进 fallback;
- 含 `time` 子串: **5 条** (其中 4 条是 `timeout …`), 子串读法下全部 fallback;
- 加上 R3-M-5 已列的 `$( )` / brace expansion / `{}` 占位符 / `(( ))` / `<<<`。

这些都不产生回归 (0→0 / 2→2), 所以不是安全问题; 但读者看 Impact 的「49 拦」会显著高估本版作用面, 而 v4 新增的 exec/time 行让这个偏差比 R3 时更大。

同时, 以下五条 minor 在 v4 中既未落 task/SC 也未写驳回理由:

- **m-1 (第四轮)** bump 前 re-check 版本号仍只在 Impact 散文;
- **m-2 (第四轮)** BLOCKED 消息「指出触发段落」但该段落自身可能含 secret, 边界仍未裁定 (Rule #7 相关, 一句话的事);
- **m-3 (第四轮)** 决策表仍无「为何手写 bash 字符扫描而非外部解析器」—— 本轮性能数据进一步支持该决策 (转内建后分析段已压到 6-25ms, 一次外部解析器 fork 就吃掉全部余量), 不写下来将来必有人「优化」成 `shlex`/`bashlex`;
- **m-4** 转出 1 的记号: 机械复算严格 `[^\|]*` = **79**、`[^\|]+` = **7**、任意形态 = **81**。数值 81 对, 记号写 `[^\|]*` 会让收口者 grep 出 79 再开一轮;
- **m-5** §3 伪代码 `any(seg =~ pat …)` 未绑定 `pat`, 下一行却 `BLOCK(pat, seg)`。现状 BLOCKED 消息含 `Matched pattern: $pat` (canonical `:666`), 重排后取哪条未定义 —— 而 SC-9 dogfood 正要看这条消息。应写死「取首个命中」以与 `:658` 顺序遍历一致。

**处置**: Impact 覆盖率声明补一句列全收缩面 (或并入转出 2); 五条 minor 逐条二选一 —— 落成 task/SC, 或明确写「驳回 + 理由」。**静默是唯一不可接受的处置**, 这句我第三次写。

---

## Minor

- **R4-m-1** §What.3 的性能表 (146/158ms 与 +102%/+583%) 是**转内建之前**的数据, v4 加了 §What.4 之后已经失效 (实测四档全部变快)。留着会被下一轮当基线继承 (memory `feedback_spec_inherits_upstream_dec_errors`)。建议整表用转内建后的数字重写并标注测量单位。
- **R4-m-2** §What.3 用「R3 tech-lead 独立验证 (306 条 0 不一致)」给布尔等价背书 —— 但那 306 条是对 **grep 版 credit** 做的, v4 的 credit 已换成内建版 (且 R4-C-1 证明两者不等)。**结论不变但证据链要重述**: 重排等价性成立是因为「对任一固定的**纯函数** credit, `∃pat.match ∧ ¬credit` 与 `¬credit ∧ ∃pat.match` 恒等」, 与 credit 的实现方式无关。改成实现无关的论证反而更强, 也不必再挂那次实测。详见下方专题三。
- **R4-m-3** 转出 8 写「新形态出现时应扩充 §What.1 判据表而非视为 SC 失败」—— 方向对, 但没写**由谁、按什么信号触发**去扩充。建议指定归属 (挂 issue 或接 `state-checks.yaml`, 与 knowledge-manager R3 Minor-1 对 `corpus_census.py` 的建议同一处理)。

---

## 专题二 — 范围是否可在一个 cycle 内安全交付 (owner 关注点)

**结论: 可行, 但必须拆成两个顺序 PR 落地, 不能一个 PR 吃三件事。**

先回答「三轮 Critical 只降 2 条是不是反证」: **不是**, 因为 Critical 的**性质**变了。

| 轮次 | Critical 的性质 |
|---|---|
| R1 (6C) | 机制方向错 —— `&` 不能当切分记号、「保守不切」方向反 |
| R2 (5C) | 机制方向错 —— 切 `;`/`&&` 本身不安全, 5/5 合法写法翻红 |
| R3 (4C) | 判据不完备 + 把启发式当保证 + 性能矛盾无解 |
| **R4 (2C)** | **都落在本轮新拉回的那一件事上** —— 转内建的实现契约不完整 (C-1) + 新加一行判据缺限定 (C-2) |

R1-R3 的 Critical 每次都推翻上一版的**设计本体** (v1→v2→v3 三次完整重写)。R4 这两条不推翻任何设计: fail-safe 降级方向五席一致认可, 全语料实跑零非预期回归, SC 体系本轮首次把锁改成有鉴别力的。两条 Critical 都是**局部、有明确一次改完的改法**。所以收敛趋势是真的, 不是数字凑的。

但范围**必须拆**, 依据是实测而非偏好:

```
只做 13 处转内建 (Task 1.3b)      : 全语料 305 条  0 条翻转
只做分段 (Task 1.1/1.2/1.3)      : 全语料 305 条  1 条翻转 (设计内的 KNOWN-LIMIT 转正)
```

两者的行为变更面在语料上**互不重叠**。放一个 PR 里, 整体验收是「全语料恰 1 条翻转」—— R4-C-1 那类翻转 (多行、语料零覆盖) 会被这个整体绿完整吞掉; 我这轮正是靠把两者**分开跑**才把 A 与 B 分辨出来的。混在一起还有一个后果: 出问题时无法归因是分段错了还是 credit 重构错了, 而 credit 重构碰的是**安全判定的分母**, 归因成本极高。

**建议切法** (对齐 memory `feedback_sub_pr_scope_splitting_pattern` 的 prereq / parallel 模式):

- **PR-1 (prereq, 纯性能重构, 零行为变更)** = Task 1.3b + SC-15 (扩为每处 3 条含多行) + SC-16 + 新增「多行等价」SC。
  黄金验收极便宜且极强: **全语料 305 条 exit code 逐条相同** + 多行 fixture 族逐条相同。它不改行为, 所以任何一条翻转都是 bug, 没有「设计内翻转」来稀释信号。它同时把 SC-8 的达标前提先落地。
- **PR-2 (主体)** = Task 1.1 / 1.2 / 1.3 + 其余 SC + CHANGELOG + 计数回填。
  基线换成 PR-1 之后的 hook, 「恰 1 条翻转」这个判据才真正有意义。

两个 PR 在同一 cycle 内顺序完成完全可行 (PR-1 是机械改写 + 语料复跑), 不需要拆 spec、不需要拆 issue。**不建议**把 Task 1.3b 退回转出 —— 实测证明它确实是 SC-8 达标的前提, owner 2026-08-04 的裁定站得住。

---

## 专题三 — 转内建是否改变 `has_filter` 的纯函数性质 / 布尔等价是否仍成立

**纯函数性质: 不变。** 逐条核过 13 处转写后的形态: `[[ "$command" =~ $_sgre ]]` 无副作用、不写文件、不 export、不修改 `$command`、不依赖循环外可变状态, 与原 `echo | grep -qE` 一样是对同一只读字符串的判定。141 条 pattern 侧本来就是内建。

**「先 pattern 后 credit」的布尔等价: 仍然成立。** 论证不依赖 credit 的实现方式 —— 只要 credit 是对该段的纯函数, `(∃pat: seg =~ pat) ∧ ¬credit(seg)` 与 `¬credit(seg) ∧ (∃pat: seg =~ pat)` 就恒等; 未命中时 credit 值不参与结果。转内建换的是这个纯函数的**实现**, 不是它的**代数性质**, 所以等价性不受影响。

**但有一处必须更正 (R4-m-2)**: §What.3 现在拿「R3 tech-lead 独立验证, 306 条 0 不一致」当 v4 的支撑证据。那 306 条实证是对 **grep 版 credit** 做的, 而 v4 的 credit 已换成内建版 —— 且 R4-C-1 实测证明 **grep 版 credit ≠ 内建版 credit**。所以那次实测**不能直接继承**为 v4 的证据。

这不影响结论, 只影响论证卫生: 请把支撑改成上面那段实现无关的代数论证 (更强, 且不会因 credit 实现再变而失效), 而不是继续引用一次已换前提的实测。

顺带澄清一个容易混淆的点: **R4-C-1 说的不是「重排不等价」, 而是「credit 函数本身被换了」。** 重排的等价性与转内建的等价性是两个独立命题, v4 把前者的证据用来支撑了后者。

---

## 专题四 — SC-9 是否改走 harness hook 链 (留给 R4 的设计问题, 我的裁定)

**裁定: SC-9 维持 canonical 直调, 但拆成两条 —— SC-9 守「逻辑面」(Phase B 验收), 新增 SC-9b 守「投递面」(ship 后验)。不要把 SC-9 本身改成 harness 链。**

理由一 (决定性, 实测): **Phase B 期间 harness 链结构上跑不到本 spec 的改动。**

```
harness 实际执行:  ${CLAUDE_PLUGIN_ROOT}/hooks/secret-guard.sh
                 → /home/dev/.claude/plugins/cache/10CG-aria-plugin/aria/1.65.5/hooks/secret-guard.sh
该路径:           普通文件 (-rwxr-xr-x, 非符号链接), 目录按版本号分桶
                 同级还有 aria/1.63.0/ (#172 留下的旧桶)
来源:             marketplace clone /home/dev/.claude/plugins/marketplaces/10CG-aria-plugin @ af87cae
工作区:           /home/dev/Aria/aria @ af87cae (clean)
cmp 结果:         字节相同 —— 但这是因为两边**恰好在同一 commit**, 是巧合而非结构
```

Phase B 第一次编辑 `/home/dev/Aria/aria/hooks/secret-guard.sh` 之后, 两者立刻分叉; cache 只有在 merge → push → marketplace clone 刷新 → 版本 bump 到 1.65.6 → 新建 `aria/1.65.6/` 桶之后才会拿到新代码。所以**把 SC-9 改成 harness 链, 等于造一条在 Phase B 验收时刻不可满足的门** —— 而 Rule #10 下 Phase B 不得自行豁免已启用的验收项, 结果只会是卡死或被迫走 handoff 请复议。这与 memory `feedback_goal_hook_precondition_must_be_in_session_achievable` 是同一类错误 (把 session/阶段内不可达的外部前置写进门槛)。

理由二: **#172 的教训指向的不是 SC-9, 是另一个正交命题。** 「hook 逻辑对不对」与「用户加载到的是不是这份 hook」是两件事。作者的论据 (「canonical 直调结构上证明不了用户会被拦」) 完全成立, 但结论应该是**再加一条 SC**, 不是**替换现有那条**。用一条 SC 同时承载两个命题, 恰恰是 #172 能潜伏两层滞后而无人发现的机制 —— 单一 SC 只会取其中一个证据面。而且投递面已经有了正确归属: 主仓 `71bdd60` 的 `plugin-cache-currency` state-check 就是干这个的机械兜底, 它比一次性 dogfood 覆盖得更久。

理由三: canonical 直调可在任意环境复算, harness 链依赖本机 plugin 安装态。R4 之后如果有人要复核这个 spec 的验收, 前者跑得起来、后者跑不起来。这是可复现性, 不是次要考虑。

**具体落法**:

- **SC-9 (逻辑面)** 维持 canonical 直调, 但标题与正文各加一句显式声明: 「本 SC 以 canonical 直调为准, **不声称**用户加载的 hook 会拦; 投递面见 SC-9b」。这一句正是 [Aria#178](https://forgejo.10cg.pub/10CG/Aria/issues/178) 要的「hook 类 SC 须显式声明测的是哪条路径」—— 本 spec 顺手就做了 #178 的第一个样例。
- **新增 SC-9b (投递面, ship 后验)**: v1.65.6 发布后, 在一个 plugin cache 已刷新到 1.65.6 的会话里, 取 SC-1 的第 1 条泄漏形态经 **harness hook 链**实跑并确认被拦, 同时 `plugin-cache-currency` state-check 为绿。挂 Task 1.9 (ship 后动作) 或 release-closeout。
- 若 owner 不接受把验收项拉到 ship 后, 次优是把 SC-9b 降为 Task 而非 SC (不作为 A.2 门槛)。**任何情况下都不要把 SC-9 本身改成 harness 链。**

顺带一条给 #178 的输入: 本次「工作区与 cache 字节相同, 但那是同 commit 的巧合」这个事实本身值得写进 #178 —— 探针 (`plugin-cache-currency`) 能测出**版本滞后**, 测不出**工作区 in-flight 改动未进 cache**, 而后者在每一个 Phase B 里都必然成立。

---

## 结论

v4 是四版里**第一版把锁改对的**: 我 R3 的 5 条 Major 解决了 4 条 (SC-6 改成断言分支返回值、SC-4 换成实测可证伪的 fixture、SC-5 改回 2 段并分清两层、SC-7 补齐 `&&` 形态), 两条 Critical 里 C-2 彻底解决、C-1 机制解决, 新增的 SC-14/15/16/17 分别回应了另外三席 R3 的点名问题。owner 拉回 13 处转内建的裁定经我实测**证实有效** —— R3-C-3 的 +583% 已被消除, SC-8 现有四档实测 -67% 到 -85% 全部通过。方向层可以认为已收敛。

不能 PASS 的原因是两条 Critical, 都长在**本轮新拉回的那件事**上, 且都有一个共同形态: **规范文本给出的东西, 现有验收结构上分辨不了**。

1. **13 处转内建不是语义保持变换** (R4-C-1)。`grep` 逐行与 bash `[[ =~ ]]` 整串在多行 command 上双向翻转, 其中 `cat /opt/.env | awk 'BEGIN{}⏎{print $1}'` 由 **2 变 0** 是安全回归。而全语料 305 条对这条缺陷**零翻转**、SC-15 的 26 条也不要求多行 —— 一个照字面机械替换 13 处的实现会全绿交付一个漏拦。
2. **`exec`/`time` 那行缺「仅命令位置」限定** (R4-C-2)。同一张表里紧邻的关键字行写了这个限定, 这行没写, 两种读法产出两种实现; 子串读法让含 `runtime`/`timeout`/`execute` 的命令整条降级、修复静默失效。实测 `wb` 与 `substr` 两个变体对 305 条语料**产出完全相同** —— 现有 SC 集合无一能分辨。这与 spec 自己在三版表里给 v2 下的判语 (「语料零覆盖 ⇒ 回归 SC 恒绿是假绿」) 是同一句话, 复发在 v4 新加的一行上。

三条 Major 分别是: 「换行必须计入」的支撑实测是跨版本陈旧继承且实测不成立 (第四次「勘正里引入新错误」); SC-8 修了负载没修测量单位, 实测同一负载 U1 +43.1% / U2 +60% 横跨 50% 闸, 且四档全是便宜类; R3-M-5 覆盖收缩面第二轮未处理 + 五条 minor 第 3~4 轮零处置。

**范围判断**: 可在一个 cycle 内交付, 但必须拆两个顺序 PR (PR-1 纯 credit 重构 / PR-2 分段), 依据是实测的「两者语料变更面互不重叠, 合并后前者的缺陷会被后者的设计内翻转吞掉」。**SC-9 裁定**: 维持 canonical 直调 + 新增 ship 后的 SC-9b 投递面验收; 实测证明 harness 链在 Phase B 结构上跑不到本 spec 的改动, 改过去会造一条不可满足的门。

改法全部是文字级 + 扩几条 fixture, 不改设计、不改范围。但 R4-C-1 是**安全方向**的, 它必须在进 A.2 之前落进 SC —— 这不是「Phase B 再说」能兜的类别。

verdict: **REVISE**

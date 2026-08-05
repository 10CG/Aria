---
verdict: REVISE
agent: tech-lead
round: R3
critical_count: 3
major_count: 5
minor_count: 6
r2_resolved: 6/13
---

# post_spec R3 — secret-guard-per-segment-evaluation (tech-lead 视角, 三审)

审计对象: `/home/dev/Aria/openspec/changes/secret-guard-per-segment-evaluation/proposal.md`
被审代码: `/home/dev/Aria/aria/hooks/secret-guard.sh` (141 pattern / `has_filter` 13 fork / 判定循环 `:663`) + `aria/hooks/tests/secret-guard.test.sh`
R2 报告: `.aria/audit-reports/post_spec-R2-1785852823204-secret-guard-per-segment-evaluation-tech-lead.md`

## 方法 (独立重写, 未读作者原型)

按 R3 任务要求, `failsafe_v3.py` / `perf_shortcircuit.sh` **一行未读**。我从 proposal §1/§2 的**文字**独立重写了 `safe_to_split()` + `split_top()` (`.../scratchpad/r3tl/mine.py`), 用 canonical `aria/hooks/secret-guard.sh` **直调**作为逐段判定 oracle (`sim.py`), 语料用改写 `run_case` 的 dump 保持逐字节原始引号 (`dump.test.sh` → 309 条 Bash 载荷)。性能用**进程内**计时 (`bench2.sh`, N=40) 消除 bash 启动噪声 —— 第一版跨进程计时基线在 32–126ms 间乱摆, 不可用, 已弃。

**仓库文件零改动。** 中途 harness hook 因 `/v1/var/` 字面量拦了我一次探针 (转出 7 / Aria#172 又一次实证), 改用 Write 落盘绕开。

### 先说好的一半 — 三个作者断言的独立复验结果

| 作者断言 | 我的独立复验 | 判定 |
|---|---|---|
| §What.1 fail-safe 12/12 (10 fallback + 2 split) | **12/12 精确复现** (10 FALLBACK 且改前改后一致 / `ls; echo done >/dev/null` 与 `ls -la; pwd` 走 split) | **成立** ✓ |
| §What.1 隐含: 消除 R2-C-2 的 5/5 误报 | 全语料 309 条对照: **fallback 11 / split 298 / 翻转仅 1 条** —— 正是 `put: KNOWN-LIMIT compound credit leak` (设计内)。**零安全回归** | **成立** ✓ |
| §What.3 布尔等价 | 分析: `has_filter` 纯函数 (13 处 `echo\|grep -qE`, 无写、无 exit、仅 `:663` 读一次) ⇒ `∃pat.match ∧ ¬credit` 与 `¬credit ∧ ∃pat.match` 恒等。实证: 306 条逐段 `creditfirst` vs `patternfirst` **0 不一致** | **成立** ✓ |
| §What.3 实测省 80~86% | 进程内复算: 2 段 benign 9.8ms vs 59.0ms = **−83%**; 3 段 13.9ms vs 100.3ms = **−86%**。数字精确 | **成立** ✓ |
| §What.2 `\|\|` 一字符绕过 | 3/3 复现: `;`/`&&` 形态 v2 已修 (0→2), `\|\|` 形态 v2 仍 0, 纳入后 0→2 | **成立** ✓ |
| §5 定案 65/49/16/15/1 + 5 | 独立计数器复算: **49 / 16 / 15 / 1 / 5 全中** (真边界那 1 条确为 `KNOWN-LIMIT`); 总数 65 vs 我的 66 差 1 条, 纯分母口径 (见 R3-m-6) | **成立** ✓ |
| 转出 1 「1 条 `.*` + 81 条」 | `.*` = 1 ✓; 81 需按 `[^\|]` 任意形态数 (`[^\|]*`=79 + `[^\|]+`=7) | **数对记号错** → R3-m-4 |
| 141 pattern / 13 fork | 141 ✓ / 13 ✓ | **成立** ✓ |

**fail-safe 降级是这三版里最正确的一次转向**, R2-C-2/C-3/M-1 的机制本体都被它一次性化解, 且全语料代价只有设计内的 1 条。下面的问题不在方向, 在**判据的完备性**和**锁的有效性**。

---

## 一、R2 逐条核销 (3C + 5M + 5m = 13 条)

| R2 | v3 处置 | 判定 |
|----|---------|------|
| **C-1** SC-8/§4/转出6 三方互斥 + **SC-8 未定义负载** | 采纳「先 pattern 后 credit」(方案 a) → §What.3 + 决策表 + 转出 6 降 severity。**但 R2 明写的第二项要求「SC-8 必须写死测量负载 (段数 + 具体命令)」原样丢弃**, SC-8 文字仍是「同会话各 20 轮取中位数」 | **半解决 → R3-C-3** |
| **C-2** 转出 2 是本版发出的 fail-close 回归 (5/5 安全写法翻红) | **根治**: fail-safe 降级。5/5 全部回落现状; 转出 2 改写为「本版降级为现状, 未修复」+ 内联复现 | **解决** ✓ (惟判据不完备 → R3-C-1) |
| **C-3** §1 表与 Tasks 1.1 两份互斥契约 (`$()`/反引号/heredoc) | **结构性消解**: 三者全成降级标记, 不再存在「解析 vs 不切」二义; 转出 5 措辞随之变准 | **解决** ✓ |
| **M-1** `[[ ]]`/`(( ))`/C-style `for` 被切碎;「唯一无歧义子集」被证伪 | 机制: 全成降级标记 ✓; 措辞已改成诚实版 ✓。**但 SC-6 里锁它俩的两条断言零鉴别力** (下) | **半解决 → R3-M-1** |
| **M-2** 68/52 是混合口径, 一致口径 49/16 | 定案 49/16 + **交付 `corpus_census.py` 权威计数器** —— 超出建议, 是本版第二好的动作 | **解决** ✓ |
| **M-3** `\|\|` 单开 [缺陷,高] + 删「需前瞻」 | **超出建议**: 直接纳入切分记号; 转出 4 只剩 `&`/换行;「需前瞻」已删 | **解决** ✓ |
| **M-4** 转出 1 补工作面 + `&&` 实例; **SC-7 同锁两条** | 转出 1 两项补齐 ✓。**SC-7 仍只锁 `;` 一条** —— R2 明确要求的 SC 半再次被丢 | **半解决 → R3-M-4 (第三轮)** |
| **M-5** ack 命令级需 SC 锁 | **SC-12 新增** ✓, 实测有鉴别力 (下沉段级两形态均 0→2) | **解决** ✓ |
| **m-1** bump 前 re-check 落成 task | 仍只在 Impact 散文; Tasks 1.1–1.9 无 | **未解决 (第三轮)** → R3-m-1 |
| **m-2** BLOCKED 回显段落自身可能含 secret | 全文未提 | **静默丢弃 (第三轮)** → R3-m-2 |
| **m-3** 决策表加「手写 bash vs 外部解析器」 | 决策表 8 行, 无此行 | **静默丢弃 (第三轮)** → R3-m-3 |
| **m-4** 转出 6 的 294ms 高估 3.4× | 数字整段删除 | **解决** ✓ (删除即修正) |
| **m-5** SC-5 补 `case` 家族 / 空段 | 加了 `case x in a) ;; esac`→**1**。**机械核验为 2 段**; R2 原文给的正是「→2 段」 | **采纳但写反 → R3-M-3** |

**核销结果: 6/13 干净解决。** 7 条为半解决 / 未解决 / 转录出错。

其中三条 (m-1 / m-2 / m-3) 已经**连续三轮**被丢, 且丢法完全一致: 诊断没争议、也没被驳回, 就是不进 Tasks / SC / 决策表。R2 结论那句「诊断被采纳进散文, 可执行的锁被丢掉」在 R3 依然是本 spec 最稳定的形态 —— M-4 的 SC-7 半也是第三轮同一处。**建议作者对这四条要么明确写「驳回 + 理由」, 要么落成 task/SC; 静默是唯一不可接受的处置。**

---

## Critical

### R3-C-1 fail-safe 判据的「命令位置」清单不完备 — 换行 / `&` / `time` 之后的块关键字漏检, R2-C-2 那一类 fail-close 回归原样重开 (实测 4–7 条), 语料零覆盖

§1 把块起始关键字的命令位置限定为 **行首 / `;` / `&&` / `||` / `|` / `do` / `then` 之后**。这张清单漏了真实 bash 里同样合法的命令位置。实测 (canonical 直调, 全部是**合法且真正安全**的写法 —— 我逐条 `bash -c` 验证过 stdout 确实被完全丢弃):

```
sleep 1 & for f in a b; do nomad var put $f @x; done >/dev/null
   cur=0 → post=2   段: ['sleep 1 & for f in a b', 'do nomad var put $f @x', 'done >/dev/null']
time for f in a b; do nomad var put $f @x; done >/dev/null
   cur=0 → post=2   段: ['time for f in a b', 'do nomad var put $f @x', 'done >/dev/null']
```

`&` 与 `time` 都是 bash 里合法的复合命令前缀 (我 `bash -c` 实跑确认), 但都不在 §1 清单里 ⇒ `for` 不被识别 ⇒ 不降级 ⇒ 被切成残片 ⇒ 中段 `do nomad var put $f @x` 丢失组尾的 `>/dev/null` ⇒ **0→2**。

**更重的是「行首」二义**。§2 明写「换行 —— **不切**」, 于是多行命令整条进 split 路径。若「行首」按**字符串首**读 (这是与 §2「换行非记号」一致的读法):

```
cd /tmp⏎for f in a b; do nomad var put $f @x; done >/dev/null      cur=0 → post=2
echo start⏎while read l; do nomad var get $l; done < f >/dev/null   cur=0 → post=2
cd /tmp⏎if true; then nomad var get k; fi >/dev/null                cur=0 → post=2
```

若按**任意行首**读, 这 3 条降级 (安全), 但 `&`/`time` 那 2 条照漏。**两种读法下都有漏, 且 spec 没有一个字裁定该读哪种** —— 这是 R2-C-3 点名的「两份契约, 语料零鉴别力」形态在新机制里换了个位置复发。

严重性: **多行 Bash 命令是 Claude Code 的常态写法**, 不是对抗性构造 (语料自己就有 `#152 FP: multiline benign`)。这正是 R2-C-2 被定 Critical 的那一类 —— 上线当天用户合法脚本转红、无告知、且**语料结构上抓不到**: 我核过全部 11 条走 fallback 的语料用例, 关键字全部出现在字符串首, 没有一条测 换行 / `&` / `time` 位置。

**处置**: (1) §1 命令位置清单补 换行 / `&` / `time` / `!`, 并把「行首」改写成无歧义措辞 (建议「换行或字符串起始」); (2) Tasks 1.1 写死该清单; (3) SC-6 加上述 5 条为降级断言 —— 注意必须选**有鉴别力**的形态 (见 R3-M-1)。

### R3-C-2 「降级 = 只在能保证正确时才改变行为」是被证伪的全称断言 — 存在**不含任何块结构标记、却仍不可安全分段**的命令

关键决策表把 fail-safe 写成categorical保证:「降级 = 只在能保证正确时才改变行为」。反例 (无 `{ } ( ) [[ ]] << ` 反引号, 无任何块关键字):

```
exec >/dev/null; nomad var get nomad/jobs/x     cur=0 → post=2   段: ['exec >/dev/null', 'nomad var get ...']
exec &>/dev/null; cat /opt/.env                 cur=0 → post=2
exec >/dev/null && nomad var get k              cur=0 → post=2
exec >/dev/null; cd /tmp; nomad var get k       cur=0 → post=2
```

`exec >/dev/null` 重定向的是**整个 shell 剩余生命周期**的 stdout (我 `bash -c 'exec >/dev/null; echo LEAKED'` 实跑确认无输出), 所以现状的整命令 credit 判定是**正确**的, 分段判定是**错**的。对照组 `true >/dev/null; nomad var get k` 同样 0→2 —— 但那条是**正确的新增拦截** (`>/dev/null` 只作用于 `true`)。两者字面几乎同构, 判据无法区分。

这跟 R3-C-1 不是一个根因: C-1 是清单漏项 (补清单可修), C-2 是**判据的类别本身不封闭** —— redirect 作用域可以由一个不带任何块标记的前置命令建立。因此:

- 不能只补一条 `exec` 就宣称修好; 得承认判据是**启发式**而非保证。
- 关键决策表与 §1 的措辞必须从「只在能保证正确时才改变行为」降为「覆盖已知的块结构类别; 非块结构的作用域建立 (如 `exec` 重定向) 是已知残余面」, 并新开一条转出。

严重性: `exec >/dev/null` 出现频率远低于块结构, 单看实例够不上 Critical。定 Critical 是因为**被证伪的是 spec 用来支撑整个 v3 转向的那句保证** —— 前两版就是栽在「作者以为已经保证、实际只是碰巧」上 (v1 的「切错=安全回归」、v2 的「只切 `;` `&&` 无歧义」)。同一形态第三次出现, 必须在文本层改掉, 否则 Phase B 会把它当作可依赖的不变量。

### R3-C-3 SC-8 仍无定义负载 (R2-C-1 第二项要求被丢), 且 **spec 自己在 Tasks 1.6 / SC-10 推荐的迁移写法正是最坏负载 —— 实测 2 段 +102%、3 段 +583%, 直接破 50% 闸**

R2-C-1 的处置是明确的两项: (a) 倒转求值顺序 —— **已采纳**; (b)「SC-8 必须写死测量负载 (段数 + 具体命令), 否则它测出什么全看实施者心情」—— **原样丢弃**, SC-8 文字未变。

这次的后果比 R2 更具体, 因为「先 pattern 后 credit」把成本变成了**强数据依赖**: benign 段几乎零成本, 但**每一个命中 pattern 的段都要付 141 次正则 + 13 次 fork**。进程内实测 (N=40, 与整命令现状基线对比):

```
2 段 benign            whole= 33.2ms   pattern1st=  9.8ms   −70%      ← spec 表里的那一半
3 段 benign            whole= 30.7ms   pattern1st= 13.9ms   −54%
1 段 benign            whole= 33.0ms   pattern1st=  5.8ms   −82%      ← 真实收益, 值得写进 spec

WORST 3 段全命中        whole= 50.4ms   pattern1st=106.2ms  +110%      ← 破闸
WORST 4 段全命中        whole= 35.0ms   pattern1st=122.5ms  +250%      ← 破闸
```

「全命中」不是构造出来的极端 —— **它就是 spec 自己让用户迁移过去的写法**。Tasks 1.6 / SC-10 要求 CHANGELOG 给的迁移指引是「逐段补 redirect」, 迁完长这样:

```
nomad var put p1 @f1 >/dev/null; nomad var put p2 @f2 >/dev/null           2 段: whole 30.1ms → pattern1st 61.2ms  (+102%)
… 3 段同形                                                                  3 段: whole 39.2ms → pattern1st 267.7ms (+583%)
… 5 段同形                                                                  5 段: whole 51.3ms → pattern1st 193.5ms (+277%)
```

而且在这个负载上 **pattern1st 比 credit1st 还慢** (3 段 267.7ms vs 177.8ms) —— 重排在此方向是净损失, 因为它在 13 次 fork 之上又叠了 141 次正则。

于是 §What.3 那句「这使 SC-8 从『必然失败』变为可达」只对 benign 负载成立。SC-8 不写死负载, 实施者跑 `ls -la; pwd` 得 −70% 判过, 跑迁移写法得 +583% 判不过 —— 同一实现, 结论由选例决定。Rule #10 下 Phase B 不得自行豁免 SC-8, 所以这不是「差不多就行」, 是会真卡住的门。

**处置 (三项都要)**: (1) SC-8 写死负载矩阵, 至少含 `1 段 benign` / `3 段 benign` / **`3 段全命中 (迁移写法原文)`** 三档, 每档给具体命令串; (2) 三档各自的闸值分开定 —— benign 档可以要求「不劣于现状」, 全命中档必须承认会变慢并给一个诚实上限 (或显式说明该档不设闸及理由); (3) §What.3 的收益表补全命中档, 现表三行全是 benign 或单段命中, 读者会误以为重排是无条件收益。

---

## Major

### R3-M-1 SC-6 (spec 自称「本版新机制的核心锚点」) 12 条里 **5 条零鉴别力** —— 含 R2-M-1 点名要锁的那两条

SC-6 的断言是「前 10 条走 fallback 且改前改后 exit 一致, 后 2 条走 split」。我做了反事实对照: **假设 fail-safe 检测完全没触发** (裸 split), exit 会不会变? 不变 = 该条断言无论实现对错都绿。

```
{ }            cur=0  裸切=2   YES 有鉴别力
( )            cur=0  裸切=2   YES
for            cur=0  裸切=2   YES
while          cur=0  裸切=2   YES
if             cur=0  裸切=2   YES
反引号          cur=0  裸切=2   YES
$()            cur=0  裸切=2   YES
[[ && ]]       cur=0  裸切=0   ✗ 无鉴别力   裸切段: ['[[ -f /opt/.env', '-s /opt/.env ]]', 'cat /opt/.env >/dev/null']
for ((;;))     cur=0  裸切=0   ✗ 无鉴别力   裸切段: ['for ((i=0', 'i<3', 'i++))', 'do nomad var get k$i >/dev/null', 'done']
heredoc        cur=0  裸切=0   ✗ 无鉴别力   (该串无顶层 ;/&&/||, 裸切也是 1 段)
ls; echo done  cur=0  裸切=0   ✗ 无鉴别力
ls -la; pwd    cur=0  裸切=0   ✗ 无鉴别力
```

三处后果:

1. **`[[ && ]]` 与 `for ((;;))` 正是 R2-M-1 要求锁住的两条。** 一个完全不实现 `[[` / `]]` 检测的实现在 SC-6 上 12/12 全绿。R2-M-1 的诊断被采纳了 (它们进了 §1 表), 锁却是空的 —— 与 R3-M-4 同型。
2. **heredoc 条的 fixture 选错了**: 该串没有顶层 `;`/`&&`/`||`, 所以 `<<` 检测触不触发结果都一样。要有鉴别力, heredoc body 或尾部必须含顶层 `;`。
3. **过度触发方向 (后 2 条) 用 exit code 结构上不可观测**: 两条 cur/post 恒为 0, 一个把 `ls; echo done >/dev/null` 误判降级的实现照样绿。SC-6 声称它们「证明关键字检测不过度触发」—— 这个目的没达成。

**处置**: 逐条换成有鉴别力的 fixture, 并把「反事实下 exit 必须改变」写成 SC-6 自己的构造要求。已验可用的替换方向:
- `[[ ]]`: 让 `[[ ]]` 内含可命中 pattern 的片段 + 组级 credit, 例如 `[[ -f /v1/var/x && -s /opt/y ]] >/dev/null` (裸切后段 1 命中且无 credit ⇒ 2, 降级则 0);
- 过度触发方向: 把 `ls` 换成会命中的命令 —— `nomad var put p @f; echo done >/dev/null` (正确=分段⇒2; 若 `done` 误触发降级⇒0), 这样两个方向都可观测。

### R3-M-2 SC-4 三条 fixture 在 v3 下**全部丧失可证伪性** —— fail-safe 降级把 SC-4 要抓的 bug 吞了; 而 rule6_note 正把 SC-4 列为 Rule #6 substitute 证据

SC-4 的存在理由 (R1-M-5 → R2 确认) 是: quote-aware 若没做对, 这几条会由 2 掉到 0。v2 时这成立。v3 加了 fail-safe 层之后不成立了 —— 因为**引号追踪一坏, 引号内的 `{` `(` 就暴露出来, 恰好触发块字符降级**, 于是整命令判定, exit 仍是 2。

我写了一个彻底引号盲的实现跑 SC-4 三条:

```
fixture                正确实现   引号盲实现
ssh find env              2       2 (FALLBACK)   ← 抓不到
python -c HTTP            2       2 (FALLBACK)   ← 抓不到
python3 -c open(.env)     2       2 (FALLBACK)   ← 抓不到
```

3/3 全被吞。SC-4 现在是恒绿断言。这条尤其值得记: **它是 R2-C-2 的修复 (fail-safe) 反手打掉了 R1-M-5 的修复 (SC-4)** —— 加固一处防假绿闸时重开了同类 bug, 对齐 memory `feedback_multiround_audit_catches_fix_introduced_regression`。而 rule6_note 的 substitute 清单里 SC-4 是四项之一, 空了一项就是 Rule #6 证据面缺口。

**处置**: 换成「引号内含 `;` 但整条无块字符」的 fixture。我实测可用的一条:

```
perl -ne 'print if /a;b/' /opt/.env      正确实现=2   引号盲=0   ✓ 可证伪
```

(同批候选里 `grep -h 'a;b' /opt/.env` / `sed -n 's/a;b/x/p' /opt/.env` 整条就不命中, `cat '/opt/.env' 'x;y'` 切碎后仍命中, 都不可用 —— 替换 fixture 必须实测, 不能凭直觉挑。)

### R3-M-3 SC-5 的 `case x in a) ;; esac`→**1** 断言机械核验为 **2 段** —— R2-m-5 原文给的就是「→2 段」, 转录时写反

逐条跑我的独立分段器, SC-5 十条里九条成立, 第十条不成立:

```
a; b →2 ✓   a && b →2 ✓   a || b →2 ✓   a | b →1 ✓   'a;b' 引号内 →1 ✓
a \; b →1 ✓  换行 →1 ✓    a & b →1 ✓    a &> f →1 ✓
case x in a) ;; esac  →  spec 写 1, 实为 2: ['case x in a)', 'esac']
```

`;;` 产生的空段被「空段跳过」吃掉, 剩下前后两段 —— R2-m-5 原文写的正是「`a;; b`→2 段 / `;;` 空段跳过」, 这里在采纳时把结论写反了。

叠加一层混淆: v3 下 `case` 这个串会被 `)` (块字符) **和** `case` (块关键字) 双重触发降级, **根本到不了 `split_top()`**。所以这条断言同时混淆了单元契约 (SC-5 声称测 `split_top` 的数组基数) 与集成行为。

**处置**: 改成 `→2`, 并注明「本断言测 `split_top()` 单元; 集成路径下 `case` 先被 `safe_to_split()` 降级, 二者不冲突」。这类「勘正动作里新引入错误」是本 cycle 第三次 (R2-M-2 的 68/52、作者断言清单第 6 条的 141→139), 建议 §5 的可复算纪律扩用到 SC 断言本身: **每条数值断言落笔前用计数器/分段器跑一遍**。

### R3-M-4 SC-7 仍只锁 `;` 形态 —— R2-M-4 明确要求「同时锁两条」, 第三轮同一处被丢

转出 1 的正文这轮补齐了 (两个实例 + 工作面数字, 我复核实例行为一致):

```
set -o posix; set | grep foo         cur=2 → post=0
set -o posix && set | grep buildid   cur=2 → post=0
```

但 SC-7 仍只写 `set -o posix; set | grep foo`。R2-M-4 给的理由这轮依然成立且未被回应: SC-7 的作用是「转出 1 收口时该用例转红」, 只锁 `;` 形态时, **一个只处理 `;` 的兜底实现就能让 SC-7 转红并被判为收口, 而 `&&` 形态照样 fail-open**。转出 1 正文里有第二实例、SC 里没有, 恰恰是「诊断进散文、锁被丢」的标准形态。

**处置**: SC-7 同时锁两条 (照 SC-2 逐条列名的写法)。

### R3-M-5 fail-safe 的**覆盖收缩面**未声明 —— `$( )` / brace expansion / `find -exec {}` / `xargs -I{}` / `(( ))` / `<<<` 都不是块结构却触发降级, 而 `$( )` 在真实命令里极常见

Impact 的「覆盖率 (诚实声明)」只列了块结构 (`{ }` / `for…done` / `$()` / 反引号 / heredoc)。实测降级还会被一批**形似块结构**的写法触发:

```
cp /opt/{a,b} /tmp; nomad var get k               → FALLBACK  ({a,b} 是 brace expansion)
find . -name x -exec ls {} \; ; nomad var get k >/dev/null   → FALLBACK  ({} 是占位符)
xargs -I{} ./do env                               → FALLBACK  (语料内既有用例)
cd $(pwd); nomad var put p @f >/dev/null          → FALLBACK
(( i++ )); nomad var put p @f >/dev/null          → FALLBACK
grep x <<< "$y"; nomad var put p @f >/dev/null    → FALLBACK  (<<< 是 here-string 不是 heredoc)
```

方向上没问题 (降级 = 现状, 不制造回归), 问题是**声明与实际不符, 而且差距不小**: `cd $(...)`、`X=$(...)` 这类前缀在真实 Bash 调用里非常普遍, 一旦出现整条命令就退回现状泄漏。语料 309 条里 11 条 fallback, 其中 5 条 (`$(env)` / `echo $(printenv KEY)` / `` `env` `` / `find -exec {}` / `xargs -I{}`) 属这一类。读者看 Impact 的「65 条边界用例 / 49 拦」会高估本版的实际作用面。

**处置**: Impact 的覆盖率声明补一句「以及**含 `$( )` / brace expansion / `{}` 占位符 / `(( ))` / `<<<` 的命令**因保守降级而不受益 —— 这些并非块结构, 属判据换取安全性的已知过度收缩」, 并进转出 (可并入转出 2 或单开一条 [缺陷, 低])。这会让「本版到底修了多大面」这个问题在 ship 后可被诚实回答。

---

## Minor

- **R3-m-1** (= R2-m-1 = R1-m-4, **第三轮**) 「bump 前 re-check 版本号」仍只在 Impact 散文, Tasks 1.1–1.9 无对应项。#170 撞过一次并发版号, 本仓 in-flight track 活跃。散文提醒不是闸 —— 落成 Task 或明确写「驳回, 理由 X」。
- **R3-m-2** (= R2-m-2 = R1-m-5, **第三轮**) §What.4 要求 BLOCKED 消息「指出触发段落」, 但全文仍未裁定「该段落自身可能含 secret」这个边界。建议补一句: 回显触发段原文 (与现状回显整条命令同级风险, **不升级**), 但不得额外回显 credit reason 或文件内容。一句话的事, 三轮没写。
- **R3-m-3** (= R2-m-3 = R1-M-6 子项, **第三轮**) 关键决策表 8 行仍无「为何手写 bash 字符扫描而非外部解析器」。本轮实测支持该决策: 外置解析器一次 fork 就吃掉整个性能预算 (对齐 memory `feedback_bash_hook_perf_subprocess_fork_dominates`), 且 R3-C-3 显示预算比 R2 时更紧。不写下来, 将来必有人「优化」成 `shlex`/`bashlex`。
- **R3-m-4** 转出 1 的「81 条 `[^|]*`」记号不精确: 严格含 `[^|]*` 的 = **79** 条, 另有 7 条 `[^|]+`; 按「含 `[^|]` 任意形态」数才是 **81**。数字对, 记号错 —— 未来接手的人按 `grep '\[^|\]\*'` 会数出 79 又开一轮口径争议。改成「81 条含 `[^|]` 有界字符类 (`[^|]*` 79 + `[^|]+` 7, 有重叠)」并交给 `corpus_census.py` 一并算。
- **R3-m-5** §3 伪代码 `if any(seg =~ pat for pat in patterns)` **未绑定 `pat`**, 下一行 `BLOCK(pat, seg)` 却用它。现状 BLOCKED 消息含 `Matched pattern: $pat`, 重排后取哪条未定义。应写死「取**首个**命中的 pattern」以与现状 (`:663` 顺序遍历、首个命中即 exit) 一致 —— 否则 BLOCKED 消息内容会随实现漂移, 而 SC-9 dogfood 又要看这条消息。
- **R3-m-6** §5 / Impact 的「305 条 `bash_case`」分母未定义是否含直调 `run_case` 的 Bash 载荷。我的 dump 得 Bash 载荷 **309** 条, 边界数随之变 66/50 而非 65/49 —— 差值全部来自分母而非算法。§5 的目标是「数法固化」, 那么 `corpus_census.py` 必须把**分母定义**也写死 (只数 `bash_case`? 还是所有 `tool_name=="Bash"` 的载荷?), 否则「可复算」只解决了一半, 下一轮照样能出第六个数字。

---

## 二、攻击 fail-safe 降级本身 (R3 任务 3) — 小结

| 攻击方向 | 结果 |
|---|---|
| 别名 / 函数调用内含结构 | **无效** —— 调用点本身不含结构, 分段正确 (`myfunc; risky >/dev/null` 判定与现状一致) |
| `eval "a; b >/dev/null"` | **无效** —— `;` 在双引号内被 quote-mask, 1 段 = 现状 |
| `bash -c '…'` / `ssh h '…'` | **无效** (已是转出 3), 引号内不切 |
| `$( )` 的其他写法 / `<<<` / `(( ))` / brace expansion / `{}` 占位符 | **过度降级** (覆盖收缩, 非回归) → R3-M-5 |
| **换行 / `&` / `time` 后的块关键字** | **命中** —— 合法安全写法 0→2, 4~7 条 → **R3-C-1** |
| **`exec >/dev/null` 建立的 shell 级重定向作用域** | **命中** —— 无任何块标记却不可安全分段 → **R3-C-2** |
| `exec >&-` / `exec 2>&1 1>/dev/null` | 未命中 (现状本就 exit=2, 无回归) |

即: 「块结构标记 ⇒ 可安全分段」这个判据, **漏检面 (C-1 清单不全 + C-2 类别不封闭) 与过度触发面 (M-5) 同时存在**。方向仍然正确 —— 它把 R2 的 5/5 误报清零, 全语料只翻 1 条 —— 但它是启发式, spec 现在把它当保证在写。

---

## 结论

v3 是三版里**方向最对的一版**, 而且是真的有效: R2 的三条 Critical 里 C-2 与 C-3 被 fail-safe 一次性化解, M-2 不但改对还交付了权威计数器, M-3 超出建议直接把 `||` 纳入。作者自测的三个结论 (12/12 / 布尔等价 + 80~86% / `||` 一字符绕过) 我全部独立复现, **无一被推翻** —— 这是本 cycle 第一次出现作者断言全数经得起独立检验, 值得记一笔。

不能 PASS 的原因是三处**结构性**问题, 都不是文字瑕疵:

1. **fail-safe 判据不完备, 且 spec 把它当保证在写** —— 命令位置清单漏 换行/`&`/`time` (R3-C-1), 且存在无块标记却不可安全分段的类别 `exec >/dev/null` (R3-C-2)。前者让 R2-C-2 那一类 fail-close 回归原样重开, 后者证伪「只在能保证正确时才改变行为」。两处语料都零覆盖。
2. **SC-8 仍无定义负载, 而 spec 自己推荐的迁移写法就是最坏负载** —— 实测 2 段 +102% / 3 段 +583%, 破 50% 闸。R2-C-1 的两项要求只采纳了一项, 被丢的正是「写死负载」那项 (R3-C-3)。
3. **新加的锁大面积无鉴别力** —— SC-6 (自称核心锚点) 12 条里 5 条恒绿, 含 R2-M-1 点名要锁的 `[[ && ]]` 与 `for ((;;))` (R3-M-1); SC-4 三条 fixture 被 fail-safe 层整体吞掉, 而 rule6_note 正把它列为 Rule #6 substitute 证据 (R3-M-2)。

第 3 条最值得作者注意: 它是**修复反手打掉修复** —— fail-safe (修 R2-C-2) 让 SC-4 (修 R1-M-5) 恒绿, 而 SC-6 (为 R2-M-1 而建) 在它该锁的两条上恰好没有鉴别力。这不是新错误类型, 是 memory `feedback_multiround_audit_catches_fix_introduced_regression` 与 `feedback_noop_in_test_env_hardening_needs_mechanism_assertion` 的教科书重演。**建议给每条新增 SC 加一道构造纪律: 写完先跑反事实 —— 「假设这个机制没实现, 这条断言会不会变红?」不会变红的, 换 fixture。** 我这轮就是靠这一道对照抓到 5+3 条恒绿断言的, 成本很低。

另有第三轮重复的四处静默丢弃 (m-1 / m-2 / m-3 / SC-7 的 `&&` 半)。它们单独都不重要, 但连续三轮同样的丢法说明这不是疏忽而是流程缺口: **建议下一版对每条上轮 finding 显式写「解决 / 转出 / 驳回+理由」三选一, 不允许留白。**

verdict: **REVISE**

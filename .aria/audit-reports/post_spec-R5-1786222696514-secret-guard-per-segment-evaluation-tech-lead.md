---
verdict: REVISE
agent: tech-lead
round: R5
critical_count: 3
major_count: 4
minor_count: 5
r4_resolved: 1/8
newly_introduced: 7
---

# post_spec R5 — secret-guard-per-segment-evaluation (tech-lead 视角, 全量重审 / owner 超配轮次)

审计对象: `/home/dev/Aria/openspec/changes/secret-guard-per-segment-evaluation/proposal.md` (v5 = R4-fix, 274 行, 全文读)
被审代码: `/home/dev/Aria/aria/hooks/secret-guard.sh` (698 行) + `/home/dev/Aria/aria/hooks/tests/secret-guard.test.sh` (798 行)
参照: R4-fix diff (104+/27−) / 我的 R4 报告 / R4 汇总 / 其余四席 R4 报告全文
产物: `/tmp/claude-1000/-home-dev-Aria/ac151b81-2bbd-4897-a45a-eeb50d95afd6/scratchpad/r5tl/` — **仓库文件零改动** (本报告除外)

## 方法

本轮的首要产出是「勘正动作本身有没有引入新错」, 所以我不复用 R4 的任何数字, 全部在 v5 规则下重跑:

1. 从 canonical `:318-400` 机械抽出 13 条 credit 判据 (`mk_variants.py`), 生成四份可运行 hook: `guarded_fork.sh` (仅加换行守卫, 隔离守卫本身的效应) / `builtin_plain.sh` (v4 字面直译) / `builtin_guarded.sh` (**= Task 1.3b 强制要求的那一版**) / `builtin_perline.sh` (我构造的对照解法)。
2. 语料用「`bash_case` 重定义为记录器 + 逐行 eval」无损抽 **305** 条 (`dump_corpus.sh`, 与 305 条 `^bash_case ` 调用行 1:1)。
3. `safe_to_split()` 按 §What.1 + Task 1.1 的**字面文本**独立实现两个读法 (`sts.sh`), 不参考任何已有原型。
4. 性能用整 hook 进程 wall time N=25 实测 (`perf.sh`), 不引用任何上轮数字。

全部探针 Write 落盘后执行, **未使用 `guard:ack`**。

---

## 一、我 R4 的 2C + 3M + 3m 逐条核销

| R4 编号 | R4-fix 处置 | 判定 |
|---|---|---|
| **C-1** 13 处转内建不是语义保持变换 (双向翻转, 一向漏拦) | §What.4 加 blockquote + Task 1.3b 写死换行守卫 + SC-15 扩容 | **半解决 + 修法引入更大新错** → **R5-C-1 / R5-C-2** |
| **C-2** `exec`/`time` 缺「仅命令位置」 | 判据表补「仅命令位置」+ Task 1.1(a) + SC-14 加 2 条 | **半解决, 且写进规范的那一半不是有鉴别力的那一半** → **R5-C-3** |
| **M-1** 「换行必须计入」举例里没换行 | 换成 `$'cd /tmp\nfor …'` + 新增「跨版本搬运纪律」 | **解决** ✓ (实测复验: 新例 discriminates=YES, 旧例=NO) |
| **M-2** SC-8 未定义测量口径 + 四档全是便宜类 | 口径写死为「进程内计时、只计 hook 判定段」(比我建议的整进程口径**更严**) | **半解决** —— 第五档 (靠后 pattern + 每段 filtered, 我 R4 实测该档 +60% 破闸) 仍不在四档内 → **R5-M-2** |
| **M-3** 覆盖收缩面未声明 + 五条 minor 零处置 | Impact 覆盖率行逐字未变; m-1~m-5 全部零处置零驳回 | **未解决 (第三轮)** → **R5-M-3** |
| **m-1** §3 性能表是转内建前的旧数 | 补了「基线」列 (code-reviewer M-2), 数字仍是旧数 | **半解决** |
| **m-2** 布尔等价挂的 306 条实证已换前提 | §What.3 `:85` 逐字未变 | **未解决** → R5-m-5 |
| **m-3** 转出 8 未写由谁按什么信号扩充 | `:210` 逐字未变 | **未解决** |

**核销 1/8 干净解决**, 3 条半解决, 4 条未解决。

先把该给的分给足: **M-1 这条是干净的, 而且改法比我建议的更完整** —— 不但换了能分辨的反例, 还把「跨版本搬运的实测数字必须在新规则下重跑」提炼成一条通用纪律写进 §6。R4-fix 整体也确实把 R4 五席的诊断都读进去了, 没有一条被无视。问题出在**执行精度**, 不在意愿。

---

## 二、Critical

### R5-C-1 Task 1.3b 强制的换行守卫**只治一个方向**, 而它自己引入的 fail-close 回归面**比它修掉的 fail-open 面更大**; §What.1「fallback = 现状行为, 零改善零恶化」被实测证伪 **5/5**; 全语料 **0/305** 对此零鉴别力

§What.4 采 backend 方案 1, Task 1.3b 写死: 「每条判据前置 `[[ "$seg" != *$'\n'* ]] &&`, 段内含换行则 credit=0」。我把这条约束**照字面**做进真 hook (`builtin_guarded.sh`), 与 canonical 逐条对照:

```
case                                        canonical  builtin_plain  builtin_guarded
SC15-x1-B  '| jq keys' ⏎ echo done              0            2              2      ← 守卫没修
SC15-x1-C  cd ⏎ jq keys ⏎ echo finished         0            2              2      ← 守卫没修
SC15-x1-E  awk 'BEGIN{}' ⏎ '{print $1}'         2            0              2      ← 守卫修好了
```

**三条里守卫只修好一条。** B / C 是 fail-close 方向 (0→2 误报), 守卫把 credit 强制清零, 结果与不加守卫**完全相同** —— 这一向它结构上不可能修。而 §What.4 自己的 blockquote 明写这一向「即 R2-C-2 被定 Critical 的那一类」。

更重的是**守卫自己制造了新的翻转**, 这些形态在不加守卫的字面直译下**本来是对的**:

```
case                                        canonical  builtin_plain  builtin_guarded
real-1  nomad var put … @f \⏎  >/dev/null       0            0              2   ← 守卫新造
real-2  cat /opt/.env ⏎ | wc -l                 0            0              2   ← 守卫新造
real-3  cat /opt/.env | wc -l ⏎ echo done       0            0              2   ← 守卫新造
real-4  cat /opt/.env | sha256sum ⏎ echo ok     0            0              2   ← 守卫新造
real-5  nomad var get x >/dev/null ⏎ echo ok    0            0              2   ← 守卫新造
```

`real-1` 是反斜杠续行把 redirect 写到下一行 —— **正是本 spec 迁移建议自己推荐的「逐段补 redirect」写法**。

**并且它打穿了本版设计的地基。** §What.1:38 写「判否则退回整命令判定 (= 现状行为, **零改善零恶化**)」。构造 5 条**必走 fallback** 的多行命令 (`fallback.py`, 都带块标记, `safe_to_split()` 恒 false, 根本不分段):

```
fallback-path case                                    canonical  guarded
heredoc + risky + 下一行 redirect                          0    ->   2
for 循环 + redirect 在下一行                               0    ->   2
brace group 多行                                          0    ->   2
subshell 多行                                             0    ->   2
后台 & + 多行                                             0    ->   2
                                                    flips: 5/5
```

「零改善零恶化」在多行命令上**全数不成立**。§Impact 的「含块结构者**维持现状泄漏** —— 非本版引入」同时被证伪: 它们不再维持现状, 而是翻成误报拦截。fail-safe 降级是 v3→v5 三版设计的**承重结构**, R4 五席一致认可的也是它 —— 强制修法把这根柱子改成了「多行一律不给 credit」。

**为什么现有验收全绿**: 全语料 305 条实跑, `guarded_fork` / `builtin_plain` / `builtin_guarded` **各 0 条翻转**。语料里只有 6 条含换行, 且全是 benign 或本来就该拦的形态, 无一条依赖 credit。⇒ SC-11 (全量回归) / SC-2 (5 条换行边界不变) / SC-3 (49 条不回归) 在本缺陷上**结构上恒绿**。这与 spec 自己给 v2 下的判语一字不差, 已是本 cycle 第三次复发。

**存在一个已验证的正解, 而 §What.4 只评估了两个方案就下了结论。** grep 的语义是**逐行**, 那就在内建里**照做逐行** —— 不是加毯子守卫, 也不是逐条改写 13 个字符类 (被以「工程量大 13 倍」否掉的方案 2):

```bash
_sg_line_match() {                       # 6 行, 13 处共用, 零 fork
  local _re="$1" _l
  while IFS= read -r _l || [[ -n "$_l" ]]; do
    [[ "$_l" =~ $_re ]] && return 0
  done <<< "$command"
  return 1
}
```

实测 (`perline.py`, `builtin_perline.sh`):

```
probe                                canonical  强制守卫  逐行内建
SC15-x1-B / C                            0         2        0     ← 守卫错, 逐行对
SC15-x1-E                                2         2        2
real-1 / real-3 / real-5                 0         2        0     ← 守卫错, 逐行对
fallback heredoc / brace group           0         2        0     ← 守卫错, 逐行对
backend e2e: pipe 拆两行                  2         2        2
全语料 305 条 vs canonical                        —      0 flips
```

**9/9 探针 + 305/305 语料与 canonical 完全一致**, 两个方向都对, 且它是真正的「语义保持变换」—— SC-15 的标题终于名副其实。

性能实测 (`perf.sh`, 整 hook 进程 wall time, N=25, load 5.2):

```
canonical         139.3 ms/call
builtin_plain      85.0 ms/call   (-39%)
builtin_guarded    91.4 ms/call   (-34%)   ← 强制修法
builtin_perline    94.8 ms/call   (-32%)   ← 逐行内建, 比强制修法只贵 3.7%
```

**SC-8 的性能收益完全保住。**「不引入新 fork」这个论据对逐行内建同样成立 (`read` / `[[ ]]` / here-string 全是内建)。

**处置**: (1) Task 1.3b 的强制守卫**撤回**, 改为「credit 判据必须复刻 grep 的逐行记录语义 (逐行求值, 任一行命中即真)」, 附上上面 6 行 helper; (2) §What.4 的方案表补第三行并说明为何优于方案 1/2; (3) SC-15 的判据回到真正的「改前改后逐条一致」, 并把上面 9 条探针 + 5 条 fallback 形态写死为 fixture; (4) **反事实**: 任何在多行输入上与 canonical 不一致的实现 → 这 14 条中至少 1 条翻转 (毯子守卫会红 10 条, 字面直译会红 3 条)。

### R5-C-2 SC-15「扩容 1」把三条端到端形态写死为 fixture, 但其中**两条在同一份 spec 强制的修法下不可满足** —— 两条闸门在必然发生的输入上互斥, Rule #10 下 Phase B 无合法出路

SC-15 的判据本体是「基础 26 条 = 每处 命中/不命中 各 1 条, 改前改后判定**逐条一致**」。扩容 1 在这条判据下追加:

> 并把两席实测的三条端到端形态写死为 fixture: `… | jq keys⏎echo done` (0→2 误报) / `cd /tmp⏎… | jq keys⏎echo finished` (0→2) / `cat /opt/.env | awk 'BEGIN{}⏎{print $1}'` (**2→0 漏拦**)

按 SC-15 自己的判据「改前改后逐条一致」, 这三条要求改后分别是 0 / 0 / 2。而 Task 1.3b **强制**的换行守卫实测产出 2 / 2 / 2 (见 R5-C-1 表)。⇒ **SC-15 与 Task 1.3b 互斥, 两条都是 enabled 判据, Phase B 哪条都不能自行豁免。**

若改用另一种读法 (三条只断言「改后仍不给 credit」), 则 SC-15 在放行 B/C 那 0→2 的误报 —— 而 §What.4 的正文刚把这一向标注为「R2-C-2 被定 Critical 的那一类」。**同一份文档, 一段把它定 Critical, 另一段把它写成验收通过条件。**

这与 code-reviewer R4-C-1 (SC-15 vs SC-16 互斥) 是**完全同构**的一次复发: 上一轮的互斥是继承上游的事实错误, 这一轮的互斥是自己新写的修法与自己新写的 fixture 打架。

**处置**: 随 R5-C-1 一并解决 —— 采逐行内建后三条都能同时满足 (实测 0 / 0 / 2)。若 owner 坚持保留毯子守卫, 则必须显式裁定「B/C 那两条的 0→2 是本版接受的行为变更」, 写进 §Impact 行为变更 + SC-10 迁移写法, 并撤下 SC-15 里那两条 fixture —— 但那等于在 spec 里正式接受一类 R2 定过 Critical 的误报。

### R5-C-3 `exec`/`time` 的「仅命令位置」**不足以排除 `timeout`**; Task 1.1(a) 的规范文本与 SC-14 新增 fixture #2 互斥 —— 我 R4 给的措辞就是欠精确的那一半, 作者照做了

按 §What.1 判据表 + Task 1.1(a) 的字面文本独立实现两个读法 (`sts.sh`; READ_A = 只限命令位置, READ_B = 命令位置**且**词边界):

```
case                                   READ_A(仅命令位置)  READ_B(位置+词边界)
SC-14 原 3 条                                 split             split          (两读法相同, 零鉴别力)
SC-14 R4 新增 #1  echo runtime; …             split             split
SC-14 R4 新增 #2  timeout 5 curl x; …       FALLBACK            split          <<< 分歧
额外: format x; …                          FALLBACK            split          <<< 分歧
额外: iferror-check; …                     FALLBACK            split          <<< 分歧
额外: execute-plan; …                      FALLBACK            split          <<< 分歧
```

`timeout` 的 `time` 子串**就落在行首 = 命令位置**。位置限定约束的是**位置**, 不是**词边界**; 它挡住了 `mtime` / `timestamp` / `runtime` 这类**非**命令位置的, 挡不住 `timeout` / `format` / `iferror` / `execute-plan` 这类**在**命令位置的。

SC-14 新增 fixture #2 要求 `safe_to_split=true`, 而 Task 1.1(a) 的字面实现给 FALLBACK ⇒ **该 fixture 在规范文本下不可满足**。SC-14 条目自己的说明文字点名的是「**词边界读法** (exit=2, 正确) 与子串读法 (exit=0)」—— 也就是说 **fixture 是对的, 规范文本是错的**, 两者写在同一份 R4-fix 里。

语料实证这条仍在漏 (`corpus.jsonl` 机械扫): 6 条载荷的 `exec`/`time` 子串落在命令位置, 其中**只有 2 条真是 `exec`/`time` 命令** (`exec 3< …` / `time env`), 另 **4 条是 `timeout 5 …`** —— 按 Task 1.1(a) 全部整条降级。我 R4-C-2 的核心危害 (「含 timeout 的日常命令整条降级, 修复静默失效」) 在这一版上**原封不动**。

**这条我必须先认自己的错**: 我 R4 的处置写的是「补上与关键字行同款的 (仅命令位置) 限定」, 而我同一份报告里给出的鉴别证据是 `wb` (词边界) vs `substr` 两个变体。作者忠实照抄了我的措辞, 而措辞漏掉了真正起作用的那一半。**「作者照我说的改了」不构成「这个改法是对的」** —— 这正是 memory `feedback_spec_inherits_upstream_dec_errors`「忠实 ≠ 正确」, 这一次上游是我。

**处置**: (1) 判据表两行 + Task 1.1(a) 统一改为「**命令位置且词边界**」(`(^|⏎|;|&&|\|\||\||&|do|then|else|elif|in)[[:space:]]*(exec|time)\b`); (2) 块起始关键字行同改 —— 它有同一个洞, SC-14 原 3 条对此**零鉴别力** (上表已证两读法相同), 应补 1 条 `format x; cat /opt/.env; true >/dev/null` 须 `safe_to_split=true`; (3) 语料里那 4 条 `timeout` 载荷写进 SC-14 作为回归锚点。

---

## 三、Major

### R5-M-1 SC-16 的「反事实修正」把红的条数写窄了 —— 实测 **6 条**, spec 写 **3 条**; 根因是同一次编辑把 SC-6 从 10 扩到 14 却沿用了针对旧 SC-6 的计数

SC-16 现写: 「逐字搬运含 `(?:…)` 的 Python 原型 → `safe_to_split()` 的关键字分支静默失效 → SC-6 里 `for` / `while` / `if` **三条**转红」, 并特意加了一句「反事实写宽会让 Phase B 误以为没红满是别处出了问题」。

机械复验 (`sc16_cf.sh`, 关键字正则含 `(?:` ⇒ rc=2 ⇒ 恒 false, 逐条跑 SC-6 的 14 条 false fixture):

```
3 for              FALLBACK -> split   RED
4 while            FALLBACK -> split   RED
5 if               FALLBACK -> split   RED
11 until  (R4 新增) FALLBACK -> split   RED
12 select (R4 新增) FALLBACK -> split   RED
14 newline-for (R4 新增) FALLBACK -> split   RED
其余 8 条 (块字符判定) 不受影响
--> 转红 6 条, spec 断言 3 条
```

`until` / `select` / 换行那条都是**纯关键字型** (无块字符), 关键字分支挂掉必红。`case` 因 `)` 是块字符不红 —— 这一点 spec 的推理对, 但它是在 SC-6 只有 3 个关键字 fixture 的旧版上算的, 而**同一次 R4-fix 刚把 SC-6 扩到 6 个关键字 + 1 个换行位置**。

写窄的危害与写宽**对称**: Phase B 跑出 6 条红, spec 说该红 3 条, 于是去找「多红的 3 条是不是别处坏了」, 正好是 SC-16 自己警告的那句话反过来。这是 memory `feedback_spec_rework_leaves_downstream_ac_drift` 的形态 —— 改了上游 SC, 下游反事实没跟着改。

**处置**: 改为「SC-6 里 `for`/`while`/`until`/`if`/`select` 五条 + 换行那条 = **6 条**转红; `case` 因 `)` 属块字符判定不红; 其余 7 条块字符型不受影响」。

### R5-M-2 SC-8 口径已写死 (且比我建议的更严), 但 R4-M-2 的另一半没做 —— 唯一能破闸的负载类仍不在四档内, 且 SC-8 无「不达标时的处置路径」

正面: 口径落成「进程内计时、只计 hook 判定段」, 这比我 R4 建议的整进程口径**更严** (我 R4 实测同一负载整进程 +43.1% 过闸 / 分析段 +60% 不过闸, 选严的那个是对的选择)。「换行守卫不引入新 fork ⇒ 性能结论仍成立」这句我本轮实测支持 (91.4 vs 85.0 ms, 仍 −34%)。

未做的那一半: 我 R4 明确点名 SC-8 四档 (a)-(d) **全是便宜类**, 需补第五档「N 段命中数组**靠后** pattern 且每段 filtered」—— 我 R4 实测该类 (8 段靠后命中) 在**现在写死的这个分析段口径**下是 **50ms → 80ms = +60%, 破闸**。`grep -n "靠后\|末位\|第五档\|filtered"` 对 proposal 零命中。⇒ 闸门口径变严了, 但唯一能让它失败的负载类**依然不在表内**, 闸门在结构上仍不可能红。

另: code-reviewer R4-M-3 要的两项 —— (a) 给 `+583%` 加「另一独立实现同构复算为 +146~218%」的注记, (b) 补一句「若 (d) 档实测仍 >50%, 不得自行降门, 须以 handoff 请 owner 复议」—— (a) 只在 SC-8 子条目里以「已实质解决」间接缓解, 正文 `:14` / `:96` / `:182` 三处仍原样呈现 `+583%`; (b) **完全没有**。SC-8 是一条带硬阈值的 enabled 闸门, Rule #10 下没有失败路径, Phase B 只能卡死或私自降门。

**处置**: 补第五档 (写死段数与具体命令串) + 补失败处置路径一句 + 三处 `+583%` 加口径注记。

### R5-M-3 R4-M-3 第三轮未解决: Impact 覆盖收缩面未列全 (且被 R5-C-1 进一步扩大), 五条 minor **第五轮**零处置零驳回

`:189` 覆盖率行逐字未变, 仍只列块结构 + 省略号。而本轮 R5-C-1 证明收缩面还要再加一条**更大的**: 强制守卫下**所有多行命令**的现状 credit 面整体消失 (fallback 5/5 翻转)。读者按现文估算本版作用面会同时高估「修好的」和低估「弄坏的」。

五条 minor 逐条机械核 (grep 全文):

| 编号 | 状态 | 证据 |
|---|---|---|
| m-1 bump 前 re-check 落 Task | 未解决 (第五轮) | 仅 `:191` Impact 散文, Tasks 1.1-1.9 零命中 |
| m-2 BLOCKED 回显段落自身可能含 secret (Rule #7) | 未解决 (第五轮) | 全文零命中 |
| m-3 决策表补「手写 bash 扫描 vs 外部解析器」 | 未解决 (第五轮) | 决策表仍 7 行 |
| m-4 转出 1 记号 `[^\|]*` | 未解决 | `:203` 仍「81 条 `[^\|]*`」; 严格 `[^\|]*` = 79, 任意形态 = 81 |
| m-5 §3 伪代码 `pat` 未绑定 / BLOCKED 取哪条 | 未解决 | `:79-81` 逐字未变 |

**静默是唯一不可接受的处置** —— 这句我第四次写。末轮建议 owner 一次性裁决: 每条要么进 Tasks/SC, 要么在 spec 里留一句「驳回 + 理由」。

### R5-M-4 「两个顺序 PR」的交付建议既未采纳也未驳回; 本轮证据把它的依据从「变更面不重叠」升级为「credit 面的回归在全语料上完全不可见」

`grep -n "PR-1\|PR-2\|两个顺序\|顺序 PR\|sub-PR"` 对 proposal **零命中**。R4 汇总专门记了这条 (「tech-lead 给出的答案是不缩范围, 但须拆成两个顺序 PR」), spec 里没有对应文字, Phase B 拿不到任何指示。

本轮把依据加强了一档。R4 我给的理由是「两者语料变更面互不重叠, 合并后前者的缺陷会被后者的设计内翻转吞掉」。本轮实测:

```
只做 credit 重构 (Task 1.3b)     : 全语料 305 条  0 条翻转  (三个变体全部 0)
credit 重构引入的 fail-close 回归 : 全语料 305 条  0 条可见  (5/5 只在语料外形态)
只做分段 (Task 1.1/1.2/1.3)      : 全语料 305 条  1 条翻转  (设计内 KNOWN-LIMIT 转正)
```

也就是说合并成一个 PR 后, 整体验收是「全语料恰 1 条翻转」—— 而 R5-C-1 那 10 条 fail-close 回归**一条都不在语料里**, 会被这个整体绿**完整吞掉**。我这轮能把它们分辨出来, 唯一原因就是把 credit 面单独拉出来跑。

**处置**: PR-1 (prereq, 纯 credit 重构, **零行为变更**) = Task 1.3b + SC-15 + SC-16; 黄金验收 = 全语料 305 条逐条相同 **且** R5-C-1 那 14 条多行 fixture 逐条与 canonical 相同 —— 它不改行为, 任何一条翻转都是 bug, 没有「设计内翻转」稀释信号。PR-2 (主体) = Task 1.1/1.2/1.3 + 其余 SC, 基线换成 PR-1 之后的 hook。若 owner 不采纳, 请写一句驳回理由。

---

## 四、Minor

- **R5-m-1 (新引入)** 两个数字未在新规则下重算, 而这次编辑刚写了「跨版本搬运纪律: 从上一轮报告搬运的实测数字必须在新规则下重跑」。机械复验 (`nl_sweep.py`, 13 条判据逐条注入换行):
  - 「13 处判据里 **11 处**用 `[[:space:]]+` 作 token 分隔符」→ 实际 **10 处** (`:397` 用 `[[:space:]]*`, `:383` / `:386` 同)。
  - 「**11/13 处**受影响」→ 实际 **12/13**。唯一真正免疫的只有 `:383` (`([^0-9&]|^)>[[:space:]]*/dev/null`); `:386` (`&>[[:space:]]*/dev/null`) 在 `cmd &> /dev/null` 带空格写法下同样 `fork=0 → builtin=1`。
  - 后果: SC-15 扩容 1 按「受影响的 11 处各加 1 条」配 fixture, 会**漏掉 1 处**。(采 R5-C-1 的逐行内建后此项自动消解, 但数字仍应改对。)
- **R5-m-2 (新引入)** `:219` 新写的「substitute 清单中的 SC-9 相应改指 SC-9a」指向**不存在的条目** —— `:217` 的 substitute 清单是「SC-1 + SC-5 + SC-6 + SC-2/SC-3」, 从来没有 SC-9。且 `:215` 的 Rule #6 框定明写三根柱子含 **dogfood**, 而 substitute 枚举里**没有任何 dogfood 腿**。建议 substitute 清单显式加入 SC-9a。
- **R5-m-3 (新引入)** issue 前缀归一未做完: `:219` 与 `:236` 仍是裸 `#172` (其余 `#128` / `#152` / Rule `#6` `#10` 均有上下文限定, 不算)。
- **R5-m-4** §What.3 伪代码注释「仅命中段才跑 13 处 **subprocess**」与 §What.4「使逐段 credit 计算**零 fork**」直接矛盾 (第二轮)。同段 `pat` 未绑定 (我 R4-m-5) 亦未改。
- **R5-m-5** §What.3 `:85` 的布尔等价仍挂「R3 tech-lead 独立验证 (306 条 0 不一致)」—— 那 306 条是对 **grep 版 credit** 做的, credit 实现本版已换两次。**结论仍成立** (见下方系统级回答), 但证据链前提已变, 应改成实现无关的代数论证。我 R4-m-2 提过, 未处置。

---

## 五、系统级问题的回答

### 范围与两个顺序 PR

范围判断**不变**: 可在一个 cycle 内交付, 但必须拆两个顺序 PR。本轮证据比 R4 强 (见 R5-M-4)。建议未落地也未被驳回。

### 布尔等价在加了换行守卫后是否仍成立

**成立, 但成立的理由与 spec 现在写的理由不是一回事。**

「先 pattern 后 credit」的重排等价性只依赖一个条件: credit 是对该段的**纯函数**。换行守卫 `[[ "$seg" != *$'\n'* ]] &&` 是对同一只读字符串的无副作用判定, 逐行内建方案同样如此 —— 纯函数性质**不变**, 故 `(∃pat: seg =~ pat) ∧ ¬credit(seg)` 与 `¬credit(seg) ∧ (∃pat: seg =~ pat)` 恒等, **重排等价成立**。

但要分清两个独立命题, spec 现在把它们混在一处:

1. **重排等价** (`credit` 位置换了) —— 成立, 且与 credit 的实现方式无关。
2. **credit 函数本身等价** (`credit_grep` vs `credit_builtin` vs `credit_builtin+守卫`) —— **不成立**, R5-C-1 实测 15 条形态翻转。

`:85` 拿命题 2 时代的 306 条实证去支撑命题 1, 结论侥幸对, 论证已经断了。改成上面那段实现无关的代数论证更强, 也不会因 credit 再改一次而失效。

### 自我确认风险的自查

本轮两条源自我 R4 建议的改法, 复验结论**都是「作者照做了, 但改法不够」**:

- R4-C-1: 作者采的是 backend 方案 1 (不是我给的两个选项)。我 R4 给的选项 2 (对含锚点的判据保留 grep) 本轮复算也**不够** —— E 那条的分歧源自负字符类 `[^'\"]*` 跨行而非锚点, 选项 2 修不了。**我 R4 的两个处置选项都不完备**, 正解是第三条 (逐行内建), 三方都没提。
- R4-C-2: 作者一字不差照抄了我的措辞「仅命令位置」, 而我同一份报告的鉴别证据要求的是词边界。**措辞是我写窄的。**

结论: 本轮 3 条 Critical 里有 2 条可以追到我 R4 的建议欠精确。这不改变它们仍是 Critical 的事实 (spec 现在确实自相矛盾且可端到端复现), 但记录在此, 免得下一轮把「tech-lead 两轮都在说同一件事」误读成作者不改。

---

## 六、收敛判断 —— 本 spec 是否可进 A.2

**我的意见: 不可以直接进 A.2; 但也不需要第六轮完整审计。**

先说清楚这不是「又一轮没收敛」。**设计层已经稳了**: fail-safe 降级方向五席一致认可; 先 pattern 后 credit 的布尔等价本轮独立重证仍成立; owner 拉回 §What.4 的裁决方向本轮第四次实测确认正确 (整进程口径 139.3 → 85~95 ms, −32%~−39%); 判据表、分段规则表、305/141/13/16/65-49-16-15-1 这些数字面全部复算属实。**R4-fix 没有推翻任何设计, 也没有引入新的设计争议。**

不能进 A.2 的原因只有一条, 但它是硬的: **R4-fix 把一条 Critical 的修法写成了 Task 1.3b 的强制实现约束, 而那条约束经端到端实测会产生 10 条 fail-close 回归、打穿 fail-safe 的「零改善零恶化」承诺 (5/5), 并且让 SC-15 自己写死的三条 fixture 里两条不可满足。** Rule #10 下 Phase B 对 Task 1.3b 与 SC-15 都不能自行取舍 —— 照 Task 做则 SC-15 红, 照 SC-15 做则违反 Task。**这是一条会让 Phase B 结构性卡死的自相矛盾, 不是「Phase B 再说」能兜的类别。** R5-C-3 是同一形态的第二例 (Task 1.1(a) vs SC-14 fixture #2)。

**但修法的体量很小, 而且已经验证过了**:

- R5-C-1 + R5-C-2: 撤掉毯子守卫, 换成 6 行的逐行 helper。我已实测 9/9 探针 + 305/305 语料与 canonical 完全一致, 性能只比毯子守卫贵 3.7%、仍比现状快 32%。改 spec 约 8 行 (Task 1.3b 一句 + §What.4 方案表一行 + SC-15 判据回到「逐条一致」)。
- R5-C-3: 判据表两行 + Task 1.1(a) 各加「且词边界」四个字, SC-14 补 1 条 `format …`。
- 四条 Major 是补一档负载 / 改一个数字 / 列全收缩面 / 一次性裁决五条 minor, 全是文字级。

**建议 owner 走的路径**: 授权作者按上述改一版 (R5-fix), 由**一席** (建议 backend-architect —— R5-C-1 的另一半证据是他给的, 且逐行内建方案需要独立复跑一次全语料) 做**定向复验**而非全量五席重审, 复验判据就三条: (1) 逐行内建对全语料 0 翻转且对 14 条多行 fixture 与 canonical 逐条相同; (2) `timeout 5 curl x; …` 在新 Task 1.1 文本下 `safe_to_split=true`; (3) SC-16 反事实红 6 条。三条全绿即进 A.2。

**不建议**的两条路: (a) 直接进 A.2 让 Phase B 自己在 Task 1.3b 与 SC-15 之间选 —— 那正是 Rule #10 禁止的 AI 自行豁免闸门; (b) 开第六轮全量五席 —— 设计层已收敛, 五席重审的边际产出会集中在同一批文字级条目上, 与本轮的 4 条 Major 高度重合。

verdict: **REVISE**

---
verdict: REVISE
agent: backend-architect
round: R3
critical_count: 1
major_count: 2
minor_count: 1
r2_resolved: 0/2
---

# post_spec R3 — secret-guard-per-segment-evaluation — backend-architect

视角: 独立复验「先 pattern 后 credit」重排的性能声称 + 布尔等价性证明 + R2 两项 MAJOR 核销 + `safe_to_split()` 纯 bash 实现面复核。

方法论: 未改仓库任何文件；canonical `aria/hooks/secret-guard.sh` 用 `sed` 逐字抽取 credit 判据块 (323-399 行) 与 141 条 `risky_patterns` 数组 (402-656 行)，包成独立 bash 函数，**独立重写**三份脚本 (`r3_perf.sh` / `r3_ablation.sh` / `r3_before_after.sh`，均在 scratchpad `r3/` 下，未参考作者 `perf_shortcircuit.sh`/`failsafe_v3.py` 的代码本身，仅参考其"用 CPU-time 而非 real"方法论提示)；CPU time (user+sys) via bash `time` + `TIMEFORMAT`，每组 3 轮独立试验，同机 load average 1.2-2.1 (较 R2 记录的 6.5+ 更平静，但仍用 CPU-time 口径排除残余噪声)。

## 1. 性能结论独立复验 — **worst case 下 SC-8 不成立，且比 R2 更糟**

**基线交叉核对** (benign, 对齐作者/R2 口径): 2 段全 benign 改前 39ms→改后 12ms (省 69%)，3 段全 benign 改前 40ms→改后 18ms (省 55%) — 与作者「146→28ms / 158→22ms」量级一致，**证实作者的 benign 场景数字本身可信、非捏造**。

**但**任务点名的「最坏情况 (每段都命中 pattern)」— 我独立构造并测了三层递进语料，**结果与作者表格暗示的方向相反**:

第一层 (幼稚"最坏情况"，pattern 命中位置偏前，如 `cat /opt/.env` 在 141 条里第 26 位): 仍省 31-40%。**但消融实验证明这是假象** —— 用 `r3_ablation.sh` 拆解「credit 重排」与「pattern 扫描提前退出 (proposal §3 `any(...)` 隐含的语义)」两个耦合在一起的优化点，发现节省几乎全部来自后者 (扫到第一条命中就停，不用扫完 141 条)，而非「先 pattern 后 credit」这个改动本身。用命中位置固定在数组**最后一条** (`wget --post-file=...`, 第 141/141 位) 的语料做纯净消融，四种排列组合 (credit→全扫 / 只调 order 全扫仍不早停 / 只加早停 credit 仍无条件跑 / 原版 B) CPU 时间全部收敛到 60-68ms 区间 (差异 <10%，噪声量级) —— **说明"credit 重排"这一项改动本身，在命中位置偏后时，净收益趋近于 0**。

第二层 (真最坏情况，`r3_before_after.sh`，「改前」用现状 hook 真实逻辑: 整条命令算一次 credit + 扫一次全 141 不早停；「改后」用 proposal §3 全貌逐段跑): 每段都在 141 条末位命中且都有 filter credit (代表性场景: 批处理脚本里多条 `nomad var get x >/dev/null; vault read y >/dev/null; ...` 这类合法但触发多个不同 pattern 家族的运维命令):

| 场景 | 改前(现状) | 改后(§3 设计) | 增幅 | SC-8 (≤50%) |
|---|---|---|---|---|
| 2 段末位命中+filtered | 42ms | 85ms | **+102%** | 不过 |
| 3 段末位命中+filtered | 42ms | 122ms | **+190%** | 不过 |
| 4 段末位命中+filtered | 33ms | 140ms | **+324%** | 不过 |
| 3 段位置分散 (早/中/末各一)+filtered | 35ms | 103ms | **+194%** | 不过 |

**根因**: 「先 pattern 后 credit」只解决了 R2 M-2 指出的 credit (13 处 subprocess) 部分的 O(N) 放大，**完全没有解决 pattern 扫描 (141 条 builtin `=~`) 本身的 O(N) 放大** —— 现状 hook 对整条命令只扫一次 141 条 (bash builtin 虽零 fork，但仍有真实 CPU 成本，非"零成本"，本次实测约 0.1-0.2ms/条)；逐段化后每段最坏都要扫到 141 条才能确定"是否命中"，段数从 1 变 N，扫描总量线性放大到 N×141，这部分从未被"credit 重排"触碰。141 条 pattern 里 K8s/DB-dump/其他 secret store/exfil/#69 追加 (约 idx 90-141，占近 1/3) 天然分布在数组靠后位置，SC-1/SC-3 覆盖的 49 条 `expected=2` 语料横跨这些 pattern 家族，**并非人为构造的边角案例**——凡是命中靠后 pattern 家族、且该段本身合法带 filter (真实存在的运维批处理写法) 的语料，都会落入这个未解决区间。

**结论**: SC-8 的 ≤50% 阈值**在最坏情况下不成立**，而且比 R2 报告的 +85~92% (仅 credit 部分) 更严重 (+102~324%，credit+pattern 两部分叠加)。proposal §3 声称「这使 SC-8 从「必然失败」变为可达，且无需拉回转出6」——**这个结论只对 benign-为主的语料成立，对 pattern-命中语料 (恰是 SC-1/SC-3 实际验收、也是这个 hook 存在的理由) 不成立**。R2 MAJOR-2 指出的「SC-8 阈值与转出6 裁定自相矛盾」**未被解决，且证据更强**。

→ **CRITICAL-1**

## 2. 布尔等价性验证 — **成立，无反例**

逐条对照 credit 判据块实际代码 (323-399 行，13 处 `if echo "$command" | grep -qE ...; then has_filter=1; fi`): 全部是对同一个只读字符串 (`$command`/`$seg`) 的纯函数判定，**无任何副作用** — 不写文件、不 export 环境变量、不修改 `$command` 本身、不依赖循环外部可变状态。141 条 pattern 的 `[[ seg =~ pat ]]` 同样是纯函数判定。两者之间不存在"pattern 依赖 credit 的中间状态"这类耦合 — credit 只产出一个布尔值 `has_filter`，用于事后决定是否 BLOCK，不影响 pattern 匹配本身的结果。

`block = (∃pat: seg =~ pat) ∧ ¬credit(seg)` 是可交换表达式，"先算credit再查pattern"与"先查pattern再算credit(仅命中才算)"在**该值本身**上严格等价，**未找到反例**。§3 的重排在正确性维度合格。

**但**: §3 伪代码 `if any(seg =~ pat for pat in patterns)` 用 `any()` 短路，丢失了"具体是哪条 pattern 命中"这个信息，而现状 BLOCKED 消息含 `Matched pattern: $pat` (664-666 行)、Task 1.3 也要求"消息补段落"。Phase B 实现如果真按 `any()` 语义写，需要额外记录首个命中 pattern 的名字 (不难，但伪代码没体现，容易被简化掉)。→ **MINOR-1**

## 3. R2 两项 MAJOR 核销核查

### M-1 (SC-5 消歧+双引号覆盖缺口) — **仍未解决**

现 SC-5 10 条含 `a & b`→1 / `a &> f`→1 / `case x in a) ;; esac`→1。核对 R2 原始要求:

- **`&&` 与 `&`/`&>`/`>&`/`\|&`/`2>&1` 组合消歧**: R2 要求的是 `a &>out.log && b` 这种**同一字符串内 `&>` 与真 `&&` 相邻/共存**的场景 (真正的消歧测试)。现有 `a &> f`→1 是**孤立**的 `&>` 测试，不含任何 `&&`，测不出"分段器扫到 `&` 时会不会误吞后面真正的 `&&`"这个 R2 点名的风险分支。**未覆盖**。
- **双引号保护**: R2 要求 `a; "b;c"; d` 或对称的双引号包 `&&` 用例。SC-5 现有 10 条里"`;` 在引号内"未注明单/双，SC-4 的 `python3 -c 'import os; print(open("/opt/.env").read())'` 外层是单引号 (双引号只包一段路径字符串，不包分隔符本身)。**双引号包裹分隔符的场景仍是零覆盖**。

结论: 3 条新增里只有 `a &> f`→1、`case x in a) ;; esac`→1 是新增的、但都不是 R2 点名的那两个具体缺口 (`&&`+`&>`组合 / 双引号保护)。**M-1 未核销**。

### M-2 (SC-8 阈值与转出6 矛盾) — **未解决，见 §1，且证据更强**

作者声称的"先pattern后credit"重排解决了 M-2，但独立复验显示该重排只在 benign 语料下有效；对 SC-1/SC-3 实际覆盖的 pattern-命中语料 (真正代表本 spec 修复目标的语料)，最坏情况增幅达 +102%~+324%，**远超** R2 原始测出的 +85~92%。**M-2 不仅未核销，问题比 R2 报告时更严重**。

**r2_resolved: 0/2**

## 4. `safe_to_split()` 纯 bash 实现面 — 发现一个可致核心机制静默失效的翻译陷阱

任务点名的两条正则 (取自作者 Python 原型 `failsafe_v3.py` 的 `BLOCK_CHARS`/`BLOCK_KW`，非 proposal.md 正文字面量，但 proposal.md §1 决策表的散文描述与其一一对应，SC-6 的"作者原型已验 12/12"这条证据就来自这份 Python 原型):

- `BLOCK_CHARS = [{}()\`]|\[\[|\]\]|<<` — **纯字符类+字面量，无 PCRE 专属语法，逐字搬进 bash `[[ =~ ]]` 可用** (已实测验证)。
- `BLOCK_KW = (?:^|[;&|]|\bdo\b|\bthen\b)\s*(?:for|while|until|if|case|select)\s` — **含三处 PCRE-only 语法**: 非捕获组 `(?:...)`、单词边界 `\b`、空白简写 `\s`。

**实测结果 (bash 5.2.15, GNU regex/glibc 引擎)**:

```
[[ "for x" =~ '(?:for|while)\s' ]]   → rc=2 (正则编译失败), stderr 无任何输出
```

`rc=2` 在 `[[ =~ ]]` 语境下代表"正则畸形"(区别于 rc=1 的"未命中")，**但 hook 脚本是 `set -uo pipefail` 而非 `set -e`**，`if [[ ... ]]` 对 rc=2 和 rc=1 一视同仁走 else 分支，脚本继续跑、**不报错、不留痕迹**。用真实 `BLOCK_KW` 字符串逐字测试三条 SC-6 语料:

```
for f in a b; do cat /opt/.env; done >/dev/null    → 未命中 (rc=2)  应为 UNSAFE
while read l; do cat /opt/.env; done >/dev/null    → 未命中 (rc=2)  应为 UNSAFE
if true; then cat /opt/.env; fi >/dev/null          → 未命中 (rc=2)  应为 UNSAFE
```

这三条命令**恰好不含任何 `BLOCK_CHARS` 字符** (无 `{}()` `` ` `` `[[ ]] <<`)，只能靠 `BLOCK_KW` 判定为 unsafe。若 Phase B 把 Python 正则字符串逐字搬进 bash (完全可能发生 —— proposal 的证据链是"作者 Python 原型已验 12/12"，实现者很自然会去抄那份"已验证过"的正则)，`safe_to_split()` 的关键字降级分支就是**静默 no-op**，`for`/`while`/`until`/`if`/`case`/`select` 全部会被当作"可安全分段"处理，**原样复现 v2 那次 5/5 误报回归** —— 而这正是 v2→v3 整次重设计要修的问题。SC-6 (proposal 明文"本版新机制的核心锚点") 会立刻抓到 (前 10 条 fallback 断言全部失败)，**前提是 SC-6 被跑在真实 bash 上而非概念性验证** —— 不算生产事故，但算一个容易踩、容易被"抄已验证原型"这个直觉带偏的坑，值得显式点名。

**修复不难** (已验证): 把 `(?:X)` 换成普通捕获组 `(X)` (匹配语义不需要非捕获)；把 `\bdo\b`/`\bthen\b` 换成显式边界字符类 `(^|[;&|[:space:]])(do|then)[[:space:]]+` (前边界 + 后必须接空白，避免"裸写 do/then 不加边界"退化出 `sudo for x` 误判为含 `do` 关键字的新回归 —— 已实测确认裸写会踩这个坑，加边界后不会)；`\s` 换成 `[[:space:]]`。合并后的完整 POSIX ERE 版本对 12 条 SC-6 语料 (10 条 fallback + 2 条 split) **12/12 全部正确**，含 `sudo`-like 场景无误报 (虽 SC-6 本身未含 `sudo for` 这条，但既然是新引入的等价替换写法就该顺手验证不引入新回归)。

**建议**: Task 1.1 或 rule6_note 显式加一句"`safe_to_split()` 须用纯 POSIX ERE 实现 (bash `[[ =~ ]]` 走 glibc regex, 不支持 `(?:...)`/`\b`/`\s` 等 PCRE 语法), 不得直接照搬 Python 原型的正则字符串"，防止这个翻译陷阱被隐性带入 Phase B。

→ **MAJOR-2**

## 判定

R2 遗留 2 项 MAJOR 经独立复验，**0/2 核销**: M-1 (SC-5 消歧/双引号覆盖) 停留在"补了但补错分支"的状态；M-2 (SC-8 阈值矛盾) 表面上被"先pattern后credit"化解，但独立复验证明该重排只解决了 credit 部分的 O(N) 放大，pattern 扫描本身的 O(N) 放大 (141 条 × N 段) 完全未被触碰，最坏情况 (SC-1/SC-3 实际语料形态: 命中靠后 pattern 家族 + 合法 filter) 增幅 +102%~+324%，比 R2 原始测出的数字更差 —— **判定升级为 CRITICAL**。另发现一项新 MAJOR: `safe_to_split()` 的验证证据 (作者 Python 原型 12/12) 建立在 PCRE 语法上，直接搬进 bash 会让核心降级机制静默失效，需在 Task 1.1 显式加纯 POSIX ERE 约束防翻译陷阱；1 项 MINOR (BLOCKED 消息的匹配 pattern 名在 `any()` 短路伪代码下容易被实现者漏掉)。

三项修复均有明确、已验证可行的具体方案 (SC-5 补 2 类断言 / SC-8 阈值需重新面对转出6 的范围问题，本轮证据表明"重排"不足以支撑"无需拉回转出6"这个裁定，需要 owner 重新在 R2 三选一 (a)(b)(c) 里选或提出新方案 / Task 1.1 加 POSIX ERE 约束一句话)，但 SC-8/转出6 这项是设计裁决层面的分歧，不是纯编辑，**REVISE**。

**总结一行**: 独立复验推翻了"先pattern后credit"已解决 SC-8 矛盾的核心声称 —— 该重排只在 benign 语料下生效，pattern-命中语料 (即 SC-1/SC-3 实际覆盖场景) 最坏情况仍 +102%~+324%，转出6 裁定的前提未成立；另发现 `safe_to_split()` 的 Python 原型正则含 bash 不支持的 PCRE 语法，逐字搬运会让核心降级机制静默失效。

---
verdict: REVISE
agent: qa-engineer
round: R4
critical_count: 0
major_count: 2
minor_count: 5
r3_resolved: 2/5
---

# post_spec R4 (最后一轮) — QA 审计: secret-guard-per-segment-evaluation

审计对象: `openspec/changes/secret-guard-per-segment-evaluation/proposal.md` (v4 + 2026-08-08 前提刷新)。方法: canonical `aria/hooks/secret-guard.sh` 直调 (`bash aria/hooks/secret-guard.sh < payload.json`)，全部探针写入 scratchpad `.py`/`.sh` 文件后执行，未在 Bash 命令串内联 secret 字面量。脚本与产物见 `/tmp/claude-1000/-home-dev-Aria/ac151b81-2bbd-4897-a45a-eeb50d95afd6/scratchpad/r4qa/`。核心方法：因 Phase B 未落地（`safe_to_split()`/`split_top()` 尚不存在于代码中），对每条待复验的 SC 手写"最可能的 Phase B 错误实现"变体，喂同一组 fixture，检验是否真的与"正确实现"产生可观测差异。

## 0. R3 遗留核销 (我自己的 R3: 2M + 3m)

| # | R3 结论 | R4 处置 | 证据 |
|---|---------|---------|------|
| Major-1 | SC-5 `case…esac`→1 与 `split_top()` 真实契约矛盾 | **已解决** — v4 改为 `split_top()` 层面断言 →2 (纯语法切分)，`safe_to_split()` 的降级由 SC-6 单独锁定，两层职责已分离 | proposal.md:186 |
| Major-2 | SC-6 后 2 条 (`echo done`/普通两段) exit-code 恒等、无鉴别力 | **已解决** — v4 改为直接断言 `safe_to_split()` 返回值 (10 条须 false + 2 条须 true)，不再依赖端到端 exit | proposal.md:187；实测见 §1 |
| Minor-1 | Impact "16 放行" vs SC-2 "15 条纯管道" 表述易误读 | 部分缓解 — Impact 段现已写「16 放行, 其中 15 纯管道 + 1 真边界即 KNOWN-LIMIT 用例」, 歧义基本消除, 但未采纳我建议的 SC-2 侧显式排除说明 | proposal.md:137 |
| Minor-2 | `corpus_census.py` 交付无回填校验 SC / 机械 diff 步骤 | **未处理** — Task 1.8 仍只写「全量回归 + 性能相对基线实测」, 无 diff 步骤 | proposal.md:175 |
| Minor-3 | §3 伪代码未画出 `guard:ack` 检查位置 | **未处理** — §3 伪代码逐字未变 | proposal.md:66-74 |

`r3_resolved = 2/5`（两项 Major 均为真实修复且引入了鉴别力，非文字掩饰；三项 Minor 中仅 1 项部分缓解，不计入分子）。

## 1. 逐条反事实复验（本轮任务 1）：SC-4 / SC-5 / SC-6 / SC-14 / SC-15 / SC-16

### SC-4（quote-aware，已改用 `perl -ne 'print if /a;b/' /opt/.env`）—— **有效，非恒绿**

实测（`sc4_seg_test.py`）：

```
whole command (quote-aware 正确判定): exit=2
naive quote-blind split (按字面 ; 切两段):
  seg[0] = "perl -ne 'print if /a" -> exit=0
  seg[1] = "b/' /opt/.env"          -> exit=0
```

且该命令不含任何 `safe_to_split()` 判否标记 (`{}()`` `[[ ]] << <<<` / for/while/until/if/case/select 关键字均无)，不会被 fail-safe 兜底掩盖。**结论**：引号盲实现必 exit=0，正确实现必 exit=2，鉴别力成立，R3-M-2 已闭环。

### SC-6（fail-safe 降级族，改为断言 `safe_to_split()` 返回值）—— **机制有效，但存在一个未被本轮任务点名的新缺口，见 §2**

R3 已用故障注入验证「恒 fallback」「恒 split」两个方向对 10+2 条整体有效，本轮不重复。**新发现的缺口是"这 10 条对 §1 declared 的 6 个关键字覆盖不全"，单独成节见 §2，因为它不是"文字表述"问题而是"覆盖面"问题，符合本轮任务重点 3/4。**

### SC-14（关键字过度触发方向）—— **`safe_to_split=true` 断言有效；`exit 与改前一致` 是装饰性重复，无独立鉴别力**

baseline 实测（`sc14_baseline.py`）：

```
'ls; echo for >/dev/null'            -> exit=0
'ls; echo if >/dev/null'             -> exit=0
'git commit -m "add case handling"'  -> exit=0
```

三条命令本身不含任何 risky pattern。推理验证：无论 `safe_to_split()` 因关键字过度触发误判为 `false`（退回 legacy 整命令判定）还是正确判为 `true`（走 split），两条路径对这 3 条命令的最终 exit 都是 0——因为压根没有 pattern 会命中。也就是说 SC-14 里"**且** exit 与改前一致"这半句，对**这三条具体 fixture**不会因为关键字检测是否过度触发而翻转，真正的鉴别力 100% 来自"须 `safe_to_split=true`"这一分支断言。不阻断（因为分支断言本身是真实、独立可证伪的），但这半句是可以删掉而不损失验证力的装饰。

**建议**：删除"exit 与改前一致"半句，或换一条会随过度触发产生 exit 差异的 fixture（例如 `nomad var put p @f >/dev/null; echo for` —— 若关键字过度触发导致误判 fallback，legacy 整命令判定会因 `>/dev/null` 全局免疫给出 exit=0；若正确 split，`echo for` 段单独判定同样 exit=0——需要更巧妙的构造，此处不强求，只指出现状装饰性）。

### SC-15（`has_filter` 13 处转内建，26 条命中/不命中）—— **数量足够但覆盖形状不够，见 §3（本轮任务 3 直接对应）**

### SC-16（POSIX ERE 可移植性）—— **有效，但自身反事实表述存在夸大，Minor 见 §4**

## 2. SC-6 覆盖缺口：`until` / `select` 关键字零 fixture，`case` 仅有巧合冗余覆盖

proposal §1 决策表（:44）声明 6 个"仅命令位置"块起始关键字：`for` `while` `until` `if` `case` `select`。但 SC-6 的 12 条 fixture 清单（10 条须 `false` + 2 条须 `true`）里，10 条 fallback fixture 是 `{ }` / `( )` / `for` / `while` / `if` / `[[ && ]]` / `for ((;;))` / 反引号 / `$()` / heredoc —— **`until` 与 `select` 两个关键字，在全篇 proposal.md（SC-1 至 SC-17、Tasks、转出）里除了 §1 决策表本身之外，零第二次出现**（已 `grep -n "until\|select"` 核实，唯一命中行就是声明它们的那一行）。`case` 虽然出现在 SC-5，但 v4 的修法明确把该 fixture 钉在 `split_top()` 层（纯语法切分契约），**不经过、也不断言 `safe_to_split()`**——所以 `case` 关键字分支本身同样没有被任何 SC 直接断言过。

**反事实构造**（`sc6_case_until_select_gap.py`）：假设 Phase B 实现者把 `BLOCK_KW` 关键字集写成 `(for|while|if)`（例如"照着 SC-6 fixture 清单抄"这种很自然的错误——SC-6 恰好只列了这 3 个），遗漏 `until`/`case`/`select`：

```
fixture: until nomad var put secret/x @f >/dev/null; do sleep 1; done
```

这类 `until` 循环语法上通常不含任何 `{}()`` `[[ ]] << <<<` 字符（与 `for`/`while` 同构，纯靠关键字识别），所以 `BLOCK_CHARS` 检测救不了它。若关键字集漏了 `until`，`safe_to_split()` 会误判 `true`，命令被当成"可安全分段"送进 `split_top()`——这正是 v2 那次"切了再说"5/5 误报的同一失败模式，只是换了一个关键字触发。**当前 SC 集合里没有一条 fixture 会在这个 bug 下变红**（SC-6 没有 `until`/`select` 条目；SC-5 的 `case` 条目不经过这条代码路径）。

进一步核实 `case` 语句的"巧合覆盖"：`case` 语法固定含 `pattern)` 形式的右括号，天然会撞上 `BLOCK_CHARS` 的 `()` 检测，所以典型 `case` 语句即使关键字集漏了 `case` 也大概率仍被挡住——但这是**未设计、未断言的偶然重叠**，不是 SC 集合有意验证的结果；一旦 Phase B 出于别的理由收紧 `BLOCK_CHARS`（例如要求配对括号以减少无关误伤），这个偶然覆盖随时可能消失而无人发觉。

**结论**：`until` / `select` 两个关键字在 §1 声明为必须判否、但整个 SC 体系（SC-1~SC-17）零覆盖；`case` 仅存在结构性巧合覆盖，无设计断言。这是与本轮任务 3/4 直接对应的一类"多分支声明只测子集"缺口，且这个特定实例直接重新打开本 cycle 三次重写都在防的同一类回归（v2 的 5/5 误伤）。

**建议（Major）**：SC-6 追加至少 2 条纯关键字型 fixture：
```
until nomad var put secret/x @f >/dev/null; do sleep 1; done     # 须 safe_to_split=false
select e in prod dev; do nomad var put secret/$e @f >/dev/null; done  # 须 safe_to_split=false
```
并为 `case` 补一条独立于 `BLOCK_CHARS` 巧合的直接断言（哪怕只是对关键字识别函数做一次隔离单元断言，确认 "case" 本身在字符串里能被关键字正则命中，不依赖伴随的括号）。

## 3. SC-15 覆盖缺口：26 条命中/不命中不足以覆盖多分支 alternation 正则（本轮任务 3）

`has_filter` 13 处转内建里，多条正则内部含 2~4 分支 alternation：

| 行号 | 规则 | 内部分支数 |
|------|------|-----------|
| 342 | jq 安全模式 | `keys\|length\|paths\|leaf_paths` — 4 |
| 358 | grep 锚点字符类 | `[\^\$]` — 2（^ 或 $） |
| 361 | grep 反选 | `-v\|--invert-match` — 2 |
| 364 | sed 替换/删除 | `[Ss]/…/\|[0-9]+d\|[Dd]` — 3 |
| 368 | cut 字段 | `-[df]` — 2 |
| 383 | stdout 重定向前置字符类 | `[^0-9&]\|^` — 2 |
| 390 | curl 丢弃输出 | `-o …\|--output …` — 2 |
| 394 | wc 计数 | `-[clw]` — 3（c/l/w） |
| 397 | 哈希工具 | `sha256sum\|md5sum\|sha1sum\|sha512sum` — 4 |

SC-15 要求"每处命中/不命中各 1 条"，但**一处 1 条命中 fixture 只能证明"该规则至少还有一个分支活着"，证明不了"全部分支都活着"**。若 Phase B 转写时静默丢了其中一个分支（如把 `sha256sum|md5sum|sha1sum|sha512sum` 误写成三选一、漏掉 `sha512sum`），只要 SC-15 的命中 fixture 选的是幸存分支（如 `sha256sum`——这也是最"自然"、最容易被 fixture 作者选中的例子），命中/不命中两条**都会通过**，缺陷完全隐形。

**已实测核实这不是纸上谈兵**：现有 366 条回归语料库（`secret-guard.test.sh`）本身就恰好只覆盖了这类规则里的"最常见"那个分支：

```
$ grep -n "sha512sum|sha256sum|md5sum|sha1sum" secret-guard.test.sh
131: bash_case "cat .env | sha256sum" 0 'cat .env | sha256sum'
   ← 只有 sha256sum，sha1sum/md5sum/sha512sum 零覆盖

$ grep -n "jq 'keys'|jq keys|...length|...paths|leaf_paths" secret-guard.test.sh
127: bash_case "curl /v1/var | jq keys" 0 "..."
   ← 只有 keys，length/paths/leaf_paths 零覆盖

$ grep -n "wc -c|wc -l|wc -w" secret-guard.test.sh
130: bash_case "cat .env | wc -l" 0 'cat .env | wc -l'
   ← 只有 wc -l，wc -c/wc -w 零覆盖
```

也就是说：**若 Phase B 实现者依照"抄现有语料库里已验证过的写法"这种非常自然的直觉去构造 SC-15 的命中 fixture（sha256sum / jq keys / wc -l），一个丢弃 `sha512sum` / `paths` / `wc -w` 分支的转写错误会同时骗过 SC-15（26 条）和 SC-11（366 条全量回归）**——两条本该互补的 SC 在这个具体缺陷类别上互相掩护（对应本轮任务 4："SC 之间的相互作用"）。

**建议（Major）**：SC-15 明确要求"对含内部 alternation 的规则，命中 fixture 须优先覆盖现有 366 语料库尚未出现过的分支"，或直接把 26 条改写为"逐分支覆盖"（数一下 13 处规则总计有多少条 alternation 分支，每条至少 1 命中，而不是固定 13×2=26）。按上表粗算，仅这 9 条含内部分支的规则就有 24 个分支，加上无分支的 4 条各 1 条，总命中数至少要到 28 条才能做到"每分支至少 1 条"，比现在的 13 条命中多一倍。

## 4. SC-16 自身反事实表述夸大（Minor，不影响该 SC 有效性）

SC-16 写"反事实：逐字搬运 Python 原型 → 静默失配 → SC-6 前 10 条全红"。核对 SC-6 的 10 条 fallback fixture：`{ }` / `( )` / `for` / `while` / `if` / `[[ && ]]` / `for ((;;))` / 反引号 / `$()` / heredoc。其中仅 `for` / `while` / `if` 这 3 条是**纯关键字型**（不含任何 `BLOCK_CHARS` 字符），只有它们会因 `BLOCK_KW` 正则的 PCRE 语法（`(?:…)` / `\b` / `\s`）在 bash `[[ =~ ]]` 下编译失败（rc=2，R3 backend-architect 已实测）而真正转红；其余 7 条同时命中 `BLOCK_CHARS`（`{}()`` `[[ ]] <<`），这条独立的检测路径不受 `BLOCK_KW` 该 bug 影响，依然会正确判定 `false`。**SC-16 仍然有效**（3 条足够拦住这个 bug），但"前 10 条全红"的表述不准确，应改为"其中 3 条 (`for`/`while`/`if`) 全红，其余 7 条因 `BLOCK_CHARS` 冗余不受影响仍为绿"，避免未来读者高估这条 SC 的覆盖面。

## 5. SC-9 未枚举"5 类实际使用形态"（Minor）

proposal.md:190 "SC-9 (dogfood): canonical 直调端到端脚本，覆盖 5 类实际使用形态" —— 全文未定义这 5 类具体是什么，留给 Phase B 自行挑选。对照本 spec 其余 SC 的一贯风格（SC-2/SC-3 逐条列名、SC-6/SC-15 逐条枚举 fixture），这是全篇唯一一条数量词具体但内容未具体化的 SC，可证伪性弱于同伴。建议列出 5 类的具体名字（例如：单段安全读取 / 管道过滤 credit / `;` 复合写 / `nomad var put` 复合 / `vault read` 复合），否则实现者可能挑 5 条彼此高度相似、覆盖面很窄的用例仍算"过"。

## 6. 留给 R4 的设计问题：SC-9 是否应改走 harness hook 链

**裁定：保留 canonical 直调，不改走 harness 链**，理由三条：

1. **时序上矛盾**（proposal 本身未提到的新论据）：SC-9 是 post_spec / pre-merge 阶段的验收条件，要验的是"这次 PR 改动的代码"；而 harness hook 链验的是"当前已装进 plugin cache 里的代码"。在 PR 尚未合并、cache 尚未刷新之前，harness 链结构上验不到本 PR 的改动——它验的是**旧版本**。这与 Rule #8（pre-merge gate 先验后合）的时序要求直接冲突：若 SC-9 要求过 harness 链，就必须先部署才能验收，形成"先有鸡还是先有蛋"的死循环。canonical 直调不依赖部署态，可以在合并前对这次 PR 的代码本身下判定，这是它能被放进 pre-merge 门槛的结构性前提，不是权宜之计。
2. **可复现性**：proposal 已列的反论据成立，我认同——harness 链引入 plugin 安装态依赖，同一份代码在不同人 / 不同时刻的仓库状态下可能得到不同的 SC-9 结果，这不是本 SC 该测的变量。
3. **#172 的真正教训不在"canonical 测试方式错了"，而在"canonical 跑对了但没人持续验证部署态是否跟上"**——这是一个**部署后 · 持续监控**类问题，根治手段已经存在并已生效：主仓 `71bdd60` 的 `plugin-cache-currency` state-check，在每次相关变更时机械核对 cache 与 SOT 是否一致。把"用户真的会被拦住"这个更强的保证下沉给这个持续运行的机制去把关，SC-9 只需要证明"脚本逻辑本身正确"，这是恰当的分层，不是逃避 #172 的教训。

**建议**：SC-9 保留 canonical 直调不变，但补一句边界声明（例如附在 SC-9 条目末尾）：「本 SC 证明脚本逻辑正确，不证明当前用户已被保护——部署态的持续正确性由 state-check `plugin-cache-currency` 把关（Aria#172 根因闭环），二者结构上互补，不是替代关系」，避免未来审计或使用者把"SC-9 通过"误读成"用户已经被拦住"（正是 #172 复发过的误读）。Aria#178 的规范层权衡可保留，但本 spec 内的 SC-9 文字不必再悬而未决。

## 7. 三轮连续未处理的 Minor（第二次点名，非本轮新发现）

- R3 code-reviewer m-4：SC-3 的 49 条里实际只有 17 条真正走 split/fallback，另 32 条仅含 `\|` 边界恒为单段——建议标注有效面，v4 未采纳。
- R3 tech-lead R3-m-5：§3 伪代码 `if any(seg =~ pat for pat in patterns)` 里 `pat` 未绑定，下一行 `BLOCK(pat, seg)` 取哪条未定义——v4 伪代码逐字未变。
- 我自己 R3 Minor-2/Minor-3（`corpus_census.py` 无回填校验 SC；§3 伪代码未画出 `guard:ack` 检查位置）——均未处理，见 §0。

这几条单独看都不阻断，但连续两轮同样的丢法（本 cycle 已有 m-1/m-2/m-3/SC-7-半 四处三轮丢弃的先例）值得在收敛判定时一并考虑：如果 owner 决定本轮结束 spec 冻结，建议至少把这些 Minor 转成显式"驳回 + 理由"或转出 issue，不再留白。

## 结论

R3 我自己提出的 2 项 Major（SC-5 层级混淆、SC-6 exit-code 无鉴别力）本轮独立复验，**均真实修复**，v4 引入的机制级断言经得起故障注入检验，不是文字掩饰。其余四位审计方 R3 指出的核心问题（tech-lead R3-C-1/C-2 判据补漏、backend-architect M-1/M-2 性能与 POSIX ERE 陷阱）也都能在 v4 正文找到对应修法且逻辑自洽。

但本轮聚焦"SC 可证伪性/覆盖缺口"这个专门任务，找到 **2 项新 Major**，均有实测/实读证据支撑而非猜测：(1) SC-6 对 §1 声明的 6 个块关键字只测了 3 个，`until`/`select` 零覆盖、`case` 仅巧合冗余覆盖，缺口方向正是本 cycle 三次重写都在防的同一类回归；(2) SC-15 的 26 条命中/不命中对多分支 alternation 正则不够，且已用现有 366 语料库的真实覆盖情况证实"fixture 作者会自然选中已验证分支"这一风险确实成立，SC-15 与 SC-11 在这个缺陷类别上会互相掩护。两项都是局部、机械可修（各追加若干条 fixture），不涉及设计变更。

叠加：SC-16 自身反事实表述有夸大（Minor）、SC-14 的 exit 一致性条款对给定 fixture 无独立鉴别力（Minor）、SC-9 的"5 类形态"未枚举（Minor）、SC-9 设计问题给出明确裁定（保留 canonical + 补边界声明）、以及三轮未处理的历史 Minor 残留（§7）。

判定 **REVISE**。这是 `max_rounds=4` 的最后一轮——本轮遗留的 2 项 Major 均为"追加 fixture"级别的机械修复、不改变 v4 已收敛的核心设计（fail-safe 降级 + 先 pattern 后 credit + `has_filter` 转内建），若 owner 判断收敛成本已过高，可选择：(a) 把这两项缺口显式转成新的转出条目（如"转出 9：`until`/`select` 关键字与 alternation 正则的分支级覆盖，Phase B 落地时一并补齐，缺一即视为 SC-6/SC-15 未完成"），或 (b) 在 Phase B 任务里补两组 fixture 后一次性验收，二者都不需要再开一轮完整审计。

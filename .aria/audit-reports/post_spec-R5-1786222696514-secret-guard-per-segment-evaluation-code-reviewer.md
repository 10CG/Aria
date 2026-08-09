---
verdict: REVISE
agent: code-reviewer
round: R5
critical_count: 1
major_count: 3
minor_count: 7
r4_resolved: 3/13
newly_introduced: 6
---

# post_spec R5 — secret-guard-per-segment-evaluation (code-reviewer 视角, 全量重审)

审计对象: `/home/dev/Aria/openspec/changes/secret-guard-per-segment-evaluation/proposal.md` v5 = R4-fix (274 行, 全文读)
参照物: R4-fix diff (104 增 / 12 删) / 我的 R4 报告 / R4 汇总 / 其余四席 R4 报告原文 / canonical `aria/hooks/secret-guard.sh` (698 行, gitlink `af87cae`) / `aria/hooks/tests/secret-guard.test.sh` (798 行)
方法: 全部数字**第五套独立实现**机械重算; 13 处 credit 判据用 `grep` 函数遮蔽法**逐字节导出**后建 fork / builtin / builtin+守卫 三实现对拍; 5 条端到端形态经 canonical 直调取真实 exit; 305 条语料 payload 用 shell `eval` 还原**引号后**真值再做 census。产物在 `scratchpad/r5cr/`。**未修改仓库任何文件** (本报告除外)。

---

## Phase 1: 规范合规性

**判定**: PASS

- Level 2 结构完整 (Why / What 1-6 / 关键决策 / Impact / 转出 9 条 / rule6_note / Tasks 1.1-1.9 / SC-1~SC-17), Rule #1 / #5 满足。
- owner 2026-08-08 裁定 [2]「先修 Critical 再判」的执行面完整: R4 去重后 5 条 Critical **逐条有对应文本**且双向挂接 (判据表 / Tasks / SC 三处同步)。
- 无 scope creep: R4-fix 未新增任何实现范围, 全部是判据限定、fixture 扩容与事实勘正。
- 转出清单与 Task 1.9 的开票范围本轮**一致** (1/2/3/4/5/8/9 开, 6/7 不开), km R4-C-1 已闭环。

进入 Phase 2。

---

## Phase 2

## 一、我 R4 的 1C + 5M + 7m 逐条核销 (3/13 干净核销, 2 条部分)

| R4 编号 | R4-fix 处置 | 判定 |
|---|---|---|
| **C-1** SC-16 事实前提为假 (`\b` / `\s` 实测支持) | 禁用清单收窄为 `(?:` 一项; `\b`/`\s`/`\w` 记「已知 GNU 依赖」允许保留; 平台差异开转出 9; 反事实由「前 10 条全红」改「三条」 | **核销 (方向正确)** —— 但**改法自身引入新错**, 见 M-1 |
| **M-1** 「换行必须计入」的例子里没换行 | 换成真换行反例 `$'cd /tmp\nfor …'`, 并加「跨版本搬运纪律」段 | **干净核销** |
| **M-2** 性能表混三基线无标注 | 加「基线」列 + 补第三基线那一行 (177.8 / 267.7) | **干净核销** |
| **M-3** SC-8 的 +583% 不可复现 + **未达标无处置路径** | 加了「R4 复验状态」(三席实测四档净减少) | **部分** —— (a) +583% 仍未标「单次点测口径」; (b) **「若 (d) 档仍 >50% 怎么办」仍无一字**, Rule #10 下 Phase B 无合法出路 -> 本轮 M-2 |
| **M-4** `corpus_census.py` 有 Task 无 SC | `grep -n -i census` = `:141` `:147` `:227` 三处, SC-1~SC-17 **零命中** | **未核销 (第三轮)** -> 本轮 M-3 |
| **M-5** 探针只比版本号不比字节 | SC-9b 加了 `cmp` 字节前置断言 (操作面已闭环); 但 `:209`「机械兜底 = plugin-cache-currency」措辞原样 | **部分** |
| m-1 转出 1 记号 `81 条 [^|]*` | `:203` 原样 | **未核销 (第四轮)** |
| m-2 命令位置表 `&` 死条目 / `in` 错项 / `!` 漏列 | `:53` 原样, 且 `:55` 新增「逐项核过 12 类位置 … 其余 10 类 … 不受影响」**反而给错项背了书** | **未核销且被加固** |
| m-3 `time` 不是「内建」 | `:48` 原样 | 未核销 |
| m-4 后台记号行漏 `<&` | `:49` 原样 | 未核销 |
| m-5 伪代码 `pat` 未绑定 + 无 `guard:ack` 位置 | `:75-83` 原样 | 未核销 (第三轮) |
| m-6 「五个结果」里 `R1 qa 53/17/2` schema 不同 | `:145` 原样 | 未核销 (第三轮) |
| m-7 三条 R3 minor 顺延 (sed 重读无 Task·SC / SC-3 未标有效面 / Key Deliverables 位置) | `:169` 仍散文, `:240` 未变, Key Deliverables 仍夹在 What.4 与 What.5 之间 | 未核销 (第四轮) |

**核销 3/13, 部分 2 条, 未核销 8 条。** 我 R4 末尾请求的「逐条写采纳 / 驳回」一条都没落实 —— 这批 minor 现在是第三到第四轮零处置零驳回。

---

## 二、数字与事实逐个复算 (第五套独立实现)

### 2.1 沿用数字 (R4 已核, 本轮重做)

| 断言 | 复算命令 | 结果 |
|---|---|---|
| **141** 条 pattern | `count.py` (定位 `declare -a risky_patterns=(` 402 至配对 `)` 656, 计引号起始行) | **141** OK |
| **13** 处 `echo | grep -qE` | `awk 'NR>=323 && NR<=401 && /grep -qE/'` = 13; 全文 17 处 (多出 226 / 302 / 311 / 659, 不在 has_filter 区) | **13** OK |
| **12** 条把管道编码进正则 | `count.py` 数含转义竖线的 pattern | **12** OK |
| `:663` 全局开关 | `:662` = `if [[ "$command" =~ $pat ]]`, `:663` = `if [[ $has_filter -eq 0 ]]` | OK |
| **305** 条 `bash_case` | `grep -c '^bash_case '` | **305** OK |
| **65 / 49 / 16 / 15 / 1 + 5** | `dumpcases.sh` (用 shell `eval` + `bash_case` 遮蔽还原引号后真值) + `census5.py` (第五套 quote/转义感知状态机) | **65 / 49 / 16 / 15 / 1**, 换行-only **5 (4 拦 + 1 放)**, 那 1 条真边界 = `put: KNOWN-LIMIT compound credit leak` — **逐位吻合** OK |
| **366 / 360** | 实跑 `bash aria/hooks/tests/secret-guard.test.sh` -> `PASS: 366 / 366` `FAIL: 0 / 366`; `zsh_case` 6 条且 `/usr/bin/zsh` 在场 -> 无 zsh 时 360 | OK |
| SC-11「其余 5 脚本」 | `ls aria/hooks/tests/*.test.sh` = 6, 减本体 = 5 | OK |
| SOT **1.65.5** | `plugin.json` = `1.65.5` | OK |
| SC-17 的重复用例仍在 | `grep -c 'FP-fix timeout run-env'` = **2** | OK (SC-17 仍有效) |

### 2.2 R4-fix **新写进去**的每一个数字 (本轮重点)

| 新数字 | 位置 | 复算方式 | 结果 |
|---|---|---|---|
| 「**16 条** pattern 含 `\b`」 | `:159` `:211` | `count.py` | **16** OK |
| 「13 处 credit 里 **2 处**含 `\b`」 | `:163` `:211` | `count.py` -> 判据 `:361` `:397`, 与 proposal 逐字引用的两条**完全一致** | **2** OK |
| 「**11/13 处**受影响」 | `:118` `:226` | 我用**自己构造的 13 条基线**做换行注入对拍 (`cmp3.sh`) | **11/13** OK (未受影响的正是 `>/dev/null` 与 `&>/dev/null` 两条) |
| 「**21 个**注入点」 | `:118` | 同上, 独立基线下逐位置计数 | **21** OK (与 backend 独立吻合, 强证据) |
| 「**104 格**机械对照 (13 × 8)」 | `:121` | 算术 13x8=104; 与 tech-lead R4 `:71` 原文核对 | OK |
| 「性能表 **177.8 / 267.7**」 | `:97` | 溯源 R3 tech-lead `:132` `:136` (credit-first 177.8 / pattern-first 267.7); 列映射正确; 267.7/39.2 = +583% 自洽 | OK |
| 「**12 类**位置, 只有 **2 类**需处理, 其余 **10 类**」 | `:55` | 逐项数 `:53` 清单 = 12; 12-2=10 | 算术 OK (但 12 类里含一个错项, 见 m-5) |
| 「SC-6 扩为 **16 条** = **14** + 2」 | `:243-246` | 10 (原) + 3 (until/select/case) + 1 (换行) = **14**; +2 true = 16 | **算术 OK** |
| 「至少 **6 个**引用点游离在外」 | `:194` | 该条**只枚举了 5 个** (CLAUDE.md 版本行 1 + 4 个 README `Plugin Version:` 行) | **不符 -> m-2** |
| 「13 处判据里 **11 处**用 `[[:space:]]+`」 | `:111` | `grep -c '\[\[:space:\]\]+'` 于导出的 13 行 = **10** | **错 (实为 10) -> m-1** |
| 「SC-16 反事实: SC-6 里 **三条**转红 / 其余 **7 条**」 | `:272` | 按同一版 SC-6 的 **14** 条 false fixture 重算 = **6 红 / 8 绿** | **错 -> M-1** |

### 2.3 事实核对 (R4-fix 新增/改写的外部声称)

| 声称 | 核实 | 结果 |
|---|---|---|
| Aria#172 已修复关闭 2026-08-08 | `forgejo GET /repos/10CG/Aria/issues/172` -> `closed` `2026-08-08T19:02:53Z` | OK |
| Aria#177 / Aria#178 存在且 open | 两条 API 均 `state=open`, 标题与 proposal 引用相符 | OK |
| plugin cache = 1.65.5 且与 canonical 字节相同 | `cmp` -> `1.65.5/` 目录 **IDENTICAL**; `1.63.0/` 目录仍在且 DIFFERS | OK (陈旧目录并存这一点 proposal 未提, 但 SC-9b 的 `cmp` 前置已覆盖) |
| `README.md :8 badge` 与 `:242` 独立行不是同一字符串 | 实读两行, 一个是 shields badge 一个是 `Plugin Version:   1.65.5 (aria-plugin, 42 Skills + 11 Agents)`; 三个 i18n README 在 `:10` / `:244` 同构 | OK |
| bash ERE: `(?:` 编译失败 / `\b` `\s` `\w` 支持 | `ere.sh` 七条独立探针 (bash 5.2.15) | 全部 OK |
| `^` 不锚定每行行首 | `[[ $'a\nb' =~ ^b ]]` -> rc=1 | OK |
| 换行守卫 `[[ "$seg" != *$'\n'* ]]` 写法本身 | `ere.sh` D1/D2: 单行段 -> TRUE, 多行段 -> FALSE | **写法正确** (glob 非正则; `$'\n'` 在 `[[ ]]` 内不加引号才展开成裸换行且不被当通配符) |

**结论: 沿用的 8 组数字全对; R4-fix 新写入的 11 个数字里 8 个对、3 个错** (11 应为 10 / 6 应为 5 / 三条应为六条)。**搬运环节确实又出错了, 且错在「作者自己重算的那三个」而不是照抄的那八个。**

---

## 三、问题

### Critical (必须修复)

#### C-1. 强制换行守卫**只闭合了 fail-open 那一半** —— R4-C-1 记录的**双向**翻转里, 0->2 那一向加了守卫仍然翻; 而且守卫**自己新造**一类 fork 与实现不一致 (全部 13 处判据都中招), 语料 0/6 检出

- 位置: `:125` (强制修法) + `:226` (Task 1.3b) + `:265` (SC-15 扩容 1) + `:192` (Impact 行为变更)
- proposal 采的是 backend 方案 1 (「段内含换行则 credit=0」), 而 SC-15 扩容 1 要写死的三条端到端 fixture 来自 tech-lead R4 的 6 例 3 翻表 —— **两席开的药方与两席测的病灶不是同一批**。tech-lead 给的两个处置 (换行归一化 / 对含锚点判据保留 grep) 都没被采纳, 但他要求写死的 B/C/E 三条 fixture 被采纳了。
- **验证 1 —— 五条形态在 canonical 直调下的真实现状** (`mkjson.py` 造 JSON, `bash aria/hooks/secret-guard.sh < x.json`):

```
A_jqkeys_multiline   (jq keys<NL>echo done)          current exit=0
B_jqkeys_singleline  (单行控制组)                     current exit=0
C_cd_multiline       (cd /tmp<NL>… jq keys<NL>echo …) current exit=0
D_wc_multiline       (… | wc -l<NL>echo hi)           current exit=0
E_awk_multiline      (… | awk 'BEGIN{}<NL>{print $1}')current exit=2
```

- **验证 2 —— 三实现同判定管线模拟** (`sim.sh`: 141 条 pattern + 13 条 credit 判据均从 canonical 直接 `source`, 三种 credit 实现分别为 fork / 裸 builtin / builtin+本 spec 守卫; 五条形态均无块字符 => `safe_to_split=true` 且无顶层 `;` `&&` `||` => 单段 = 整串):

```
A  hit=1 credit fork=1 builtin=0 GUARDED=0 | exit now=0 unguarded=2 GUARDED=2   <- 守卫没救回来
B  hit=1 credit fork=1 builtin=1 GUARDED=1 | exit now=0 unguarded=0 GUARDED=0
C  hit=1 credit fork=1 builtin=0 GUARDED=0 | exit now=0 unguarded=2 GUARDED=2   <- 守卫没救回来
D  hit=1 credit fork=1 builtin=1 GUARDED=0 | exit now=0 unguarded=0 GUARDED=2   <- 守卫自己造出来的翻转
E  hit=1 credit fork=0 builtin=1 GUARDED=0 | exit now=2 unguarded=0 GUARDED=2   <- 守卫确实修好了这条
```

  三件事同时成立: (1) SC-15 扩容 1 点名要写死的 `jq keys<NL>echo done` (=A) 与 `cd /tmp<NL>… jq keys<NL>echo finished` (=C) **加了守卫仍是 0->2**, 即 proposal 自己引用的「R2-C-2 被定 Critical 的那一类」原封不动地留着; (2) D 这一类 (fork 给 credit、裸 builtin 也给 credit、**只有加了守卫才不给**) 是**守卫自己新造**的; (3) 只有 E 被真正修好。
- **验证 3 —— 两个方向的量级对称** (`cmp3.sh`, 13 条基线 x 每个空格位注入换行):

```
fail-open 方向 (fork=0 -> builtin=1): 21 个点, 覆盖 11/13 处判据   <- proposal 记录的那一半
fail-close 方向 (fork=1 -> 守卫=0)  : 17 个点, 覆盖 13/13 处判据   <- 守卫引入, proposal 未记录
```

- **验证 4 —— 现有验收再一次全盲**: 305 条语料里含换行的只有 6 条, 逐条跑 `hits + credit_fork vs credit_guard` (`corpusguard.sh`) -> **guard-induced flips = 0**。也就是说 SC-11 在**守卫这条新缺陷**上同样恒绿 —— 与 proposal `:128` 自己写的诊断 (「新机制配了新锁, 锁在它该抓的那一类上零鉴别力」) 一字不差地第二次复发, 这次复发在**修复动作本身**上。
- 为什么是 Critical (按部署可达性判):
  1. **Phase B 无合法出路**: SC-15 扩容 1 要求把 A / C 写死为 fixture, 但没写期望值。写「改前改后一致」-> 实现按 Task 1.3b 做完必红; 写「2」-> 等于在 SC 里锁死一条 proposal 自己定性为 Critical 的误报。Rule #10 下 Phase B 两条都不能自行裁。
  2. **未申报的行为变更**: `:192`「行为变更」只声明了「可安全分段的 `a; b` / `a && b` / `a || b` 形态将开始被拦」。A / C / D **一个顶层分隔符都没有**, 却会由 0 变 2。多行 Bash 命令在 Claude Code 下极常见 (语料 `#157` 那一族正是为多行专门修过的), 这是真用户面的过度拦截, 而 Tasks 1.6 / SC-10 的迁移写法完全没覆盖这一类。
  3. proposal `:121` 自己把这一向定性为「R2-C-2 被定 Critical 的那一类」, 却在 `:125` 用一个只处理另一向的修法收口, 并在 `:265` 用「不加换行守卫 -> 这 11+3 条至少 1 条翻转」的反事实把它盖过去 —— 该反事实**为真但无鉴别力** (加了守卫也仍有翻转), 属于 memory `feedback_counterfactual_test_for_every_new_sc` 点名的那类恒绿断言。
- **修法 (已实测, 比守卫更简单且真的语义保持)**: `grep -qE` 的语义是「**任一行**匹配即真」。用零 fork 的逐行循环直接复刻它, 而不是用守卫近似它:

```bash
# 快路径: 段内无换行时与单次 [[ =~ ]] 完全相同, SC-8 的四档负载全是单行, 性能不受影响
credit_match() {  # $1 = seg, $2 = regex
  local seg="$1" re="$2" line rest
  [[ "$seg" != *$'\n'* ]] && { [[ "$seg" =~ $re ]]; return; }
  rest="$seg"
  while :; do
    line="${rest%%$'\n'*}"
    [[ "$line" =~ $re ]] && return 0
    [[ "$rest" == *$'\n'* ]] || return 1
    rest="${rest#*$'\n'}"
  done
}
```

  实测 (`perline.sh`, 77 个主题 = 13 条基线 x 全部换行注入位 + 前置行 + 后置行):

```
per-line-builtin vs fork divergences  = 0     <- 真语义保持
guard-builtin    vs fork divergences  = 43    <- 本 spec 现在写死的修法
```

  改动面: Task 1.3b 一句话 + SC-15 扩容 1 的反事实改为「任一处不走逐行语义 -> A/C/E 至少 1 条翻转」+ SC-15 基础 26 条各补 1 条多行形态 (断言与改前**逐条一致**, 这时才是可满足的)。若 owner 坚持保留保守守卫, 则必须在 `:192` 行为变更里**显式申报**「含换行且靠行内 filter 拿 credit 的命令将开始被拦」+ CHANGELOG 迁移写法 + 把 A/C 的 fixture 期望值写死为 2, 三者缺一不可。

### Important (应该修复)

#### M-1. SC-16 的反事实数字没随同一次编辑里的 SC-6 扩容重算 —— 「三条转红 / 其余 7 条」是按**旧的 10 条清单**算的, 按新的 14 条应为 **6 红 / 8 绿**

- 位置: `:272` (SC-16 反事实) vs `:243-246` (SC-6 扩为 14 条 false)
- 这条本来是我 R4 C-1 修法的第 3 点, 作者照采了; 但**同一次编辑**把 SC-6 的 false fixture 从 10 条扩到 14 条 (新增 `until` / `select` / `case` / 真换行), 反事实没跟着重算。`:272` 甚至把「其余 7 条」逐条列了出来 —— 正好是**旧 10 条里的那 7 条**, 里面没有 `case`, 证明这句仍在描述旧清单。
- **验证** (`ere2.sh`, 逐条查 SC-6 新 fixture 里有没有块字符 —— 有块字符者不依赖关键字分支, `(?:` 编译失败也不会红):

```
block-char=none   until nomad var put …; do sleep 1; done          <- 会红
block-char=none   select e in prod dev; do …; done                 <- 会红
block-char=)      case x in a) ;; esac                             <- 不红 (靠 BLOCK_CHARS)
block-char=none   cd /tmp<NL>for f in a b; do …; done >/dev/null   <- 会红
```

  (`until` / `select` 的 fixture 文本取自 qa R4 报告 `:82-83`, 即 SC-6 新增三条的出处; 换行那条的文本 proposal `:246` 已写死。)
  => `(?:` 逐字搬运导致关键字分支静默失效时, 转红的是 `for` / `while` / `if` / `until` / `select` / 换行那条 = **6 条**; 靠块字符判定不受影响的是 7 条原块字符 fixture + `case` = **8 条**。
- 为什么重要: proposal 自己在同一句里写「反事实**写宽**会让 Phase B 误以为没红满是别处出了问题」。现在是**写窄** —— Phase B 会看到 6 条红而预期 3 条, 于是去追那 3 条「多出来的红」是不是别的 bug。这正是 memory `feedback_spec_rework_leaves_downstream_ac_drift` 的形态: 改完一段, 下游 AC 没跟着漂。
- 修法: `:272` 三条改六条, 并把「其余 7 条」改为「其余 8 条 (7 条块字符 fixture + `case` 靠 `)` 覆盖)」。

#### M-2. SC-8 仍然没有「(d) 档实测 >50% 时怎么办」的处置路径 (我 R4 M-3 的第 b 点, 未核销)

- 位置: `:249-251`
- `:249` 把 50% 写成硬闸并注明「What.4 的 13 处转内建是达标前提」, `:251` 补了三席复验「四档全部净减少」并要求「Phase B 须复算确认」。**但复算不达标时没有任何出路**: Rule #10 下 Phase B 既不能降门也不能豁免, spec 又没给「以 handoff 请 owner 复议」的口子。
- 与 C-1 叠加后风险更实: `:251` 的乐观结论建立在「换行守卫不引入新 fork」上 —— 这句我复核**成立** (守卫只是字符串比较)。但若按我 C-1 的修法改成逐行循环, 多行段会多一层纯参数展开循环 (仍零 fork, 且 SC-8 四档负载全是单行走快路径), Phase B 需要一句话确认口径。
- 修法: `:249` 末补一句「若任一档实测 >50%, **不得自行降门或改口径**, 须以 handoff 记录实测数据请 owner 复议 (Rule #10)」。另建议把 `+583%` 标注为「R3 单次点测口径; 另一独立实现同构复算为 +146~218%, 结论方向一致」。

#### M-3. `corpus_census.py` 第三轮仍然只有 Task 没有 SC —— 而 SC-2 的 15/5 与 SC-3 的 49 全是它的输出

- 位置: `:141` (Key Deliverables) + `:147` (What.6) + `:227` (Task 1.4); `grep -n -i census proposal.md` 三处命中, SC-1~SC-17 **零命中**
- 本轮我用第五套独立实现复算 `65/49/16/15/1 + 5` **逐位吻合**, 数字本身没问题; 问题只在**计数器自己不被任何断言验证**。它算错一次就会变成「权威的错答案」, 而 SC-2/SC-3 的基数直接引用它。
- 不对称仍在: 同一份 spec 为 `secret-hygiene.md` 的计数专门加了 SC-13, 同类缺陷在 census 上三轮零处置也零驳回。
- 修法 (一行): 加 SC-18 或并进 SC-3 —— 「`python3 aria/hooks/tests/corpus_census.py` 输出 `65 / 49 / 16 / 15 / 1` + 换行 `5 (4 拦 1 放)`, 与 Impact 迁移面逐数字机械比对, 不一致即失败」。qa R3 与 knowledge R3 也各自要过同一件事。

### Minor (建议修复)

#### m-1. 「13 处判据里 **11 处**用 `[[:space:]]+` 作 token 分隔符」实为 **10 处** (R4-fix 新引入)

- 位置: `:111`
- 验证: 把 13 行判据导出后 `grep -c '\[\[:space:\]\]+'` = **10** (缺的是 `:397` 的 `\|[[:space:]]*(sha256sum|…)\b`, 它用的是 `*` 不是 `+`)。
- 溯源: backend R4 `:30` 原文即写「除 `>/dev/null` / `&>/dev/null` 两条外, 其余 **11/13** 处都用 `[[:space:]]+`」, 其举例还恰好是两条 `[[:space:]]*`。作者照搬了这句。**「11 处受影响」是对的** (我独立复现 11/13), 错的是把它归给 `[[:space:]]+`。
- 修法: 改成「13 处里 **11 处**的 token 分隔符落在 `[[:space:]]`(含 `+` 与 `*`) 上, 只有 `>/dev/null` / `&>/dev/null` 两条不跨 token」。

#### m-2. 「至少 **6 个**引用点游离在外」下面只枚举了 **5 个** (R4-fix 新引入)

- 位置: `:194`
- 枚举 = (a) CLAUDE.md 版本行 x1 + (b) 4 个 README 各 1 处 = **5**。km R4 `:56` 的 6 是「CLAUDE.md 的 **2 处** + 4」。
- 验证: `grep -n "1\.65\.5" CLAUDE.md` -> `:139`「aria-plugin 方法论轨: v1.52.0–**v1.65.5** 已 ship」与 `:141`「版本: 插件 aria-plugin **v1.65.5** …」**两处**都含版本号, proposal 只点了 `:141`。
- 讽刺点: 这一条自己的结论是「该缺口不靠『注意点』能防, 只能靠**逐点枚举**」, 而它的枚举就漏了一点。
- 修法: (a) 改为「`CLAUDE.md` 项目状态段的 **2 处** (`:139` 方法论轨版本区间末端 + `:141` 版本行)」。

#### m-3. 「substitute 清单中的 SC-9 相应改指 SC-9a」—— substitute 清单里根本没有 SC-9 (R4-fix 新引入的悬空引用)

- 位置: `:219` (新句) vs `:217` (substitute 清单)
- `:217` 原文 = 「SC-1 + SC-5 + SC-6 + SC-2/SC-3」, **不含 SC-9**。这句同步声明指向一个不存在的引用点。
- 修法: 要么删掉这半句, 要么把 SC-9a 真的加进 substitute 清单 (dogfood 本来就是 Rule #6 substitute 的合理组成)。

#### m-4. `(^|<字面换行>)` 的措辞不足以防住 `(^|\n)` 这个静默误写 (R4-fix 新增文本的残余风险)

- 位置: `:55` + `:223` (Task 1.1 (b))
- 验证 (`ere2.sh`, 主体 = `$'cd /tmp\nfor f in a b; do echo x; done'`):

```
^for                 -> nomatch   (R4-C-3 要防的 bug)
(^|\n)for            -> nomatch   <- 最自然的直译写法, 同样漏
(^|<真换行>)for      -> MATCH     <- spec 想要的
(^|[[:space:]])for   -> MATCH
另: 正则 \n 在 bash ERE 里匹配的是**字母 n**, 不匹配真换行
```

  也就是说 `(^|\n)` 不但漏掉换行位置, 还多出一个「以 n 结尾的词紧跟 for」的误触发面。SC-6 的换行 fixture **能**抓到它 (所以不升级为 Major), 但这是 spec 全程被「实现散文两种读法」咬过三次的同一形态。
- 修法: 把 `<字面换行>` 换成可直接抄的 bash 写法, 例如: `nl=$'\n'; re="(^|${nl})[[:space:]]*(for|while|until|if|case|select)\b"` —— 并加一句「**不得**写 `(^|\n)`, ERE 里 `\n` = 字母 n」。

#### m-5. 「命令位置」12 类里 `in` 是错项 / `&` 是死条目 / 漏 `!`, 且 `:55` 新句反而给它背了书

- 位置: `:53` + `:55`
- `in` 之后是**词表 / case 模式**, 从来不是命令位置 (`for f in …` / `case x in …`); 顶层单独 `&` 已被判据表的「后台记号」行整行接管, 该位置项不可能改变任何判定; `!` (`! if x; then …`) 未列。
- R4-fix 新增的「逐项核过 12 类位置 … 其余 10 类靠字面 token / 字符类匹配, 不受影响」把这 12 项当成已核实清单背了书, 而 Tasks 1.1 (c) 又照它写死「其余 10 类天然安全」。三项偏差都朝 fail-safe 方向、无安全后果, 但会让实现者以为存在 `in <命令>` 这种语法。
- 修法: 删 `&` (注明已被后台记号行吸收) / 删 `in` / 补 `!`; `:55` 与 Task 1.1 (c) 的「10 类」随之改为 9 类。

#### m-6. 性能表的引言与表身对不上 + 新增行缺单位

- 位置: `:89-97`
- 引言写「下表**四行**」, 表身现在是 **5 行**; 新增的第 5 行 `177.8 / 267.7` 没有 `ms` 单位而同列上两行是 `146ms` / `28ms`; 第 4 行两列写 `—` 而第 5 行恰恰把同一档的这两个数补上了, 读者会以为是两档。
- 修法: 引言改「下表」; 第 5 行补 `ms`; 或直接把第 4/5 行合成一行。

#### m-7. 第三、四轮零处置零驳回的一批 (原样顺延)

- `:203` 转出 1 记号「**81** 条 `[^|]*`」: 数值 81 对应「含 `[^|]` 任意量词」, 严格 `[^|]*` 是 **79**, `[^|]+` 是 7 (有重叠) —— 第四轮未改。
- `:48` `time` 是 **keyword** 不是 builtin (`type -t time` = keyword, `type -t exec` = builtin), 「作用域型内建」这个行名不准。
- `:49` 后台记号行的排除表漏 `<&` (`cmd <&3; other`) —— 过度降级, 安全方向。
- `:75-83` 伪代码 `BLOCK(pat, seg)` 用了未绑定的 `pat`; 且 `guard:ack` 的命令级语义 (SC-12) 在伪代码里不可见。
- `:145` 「五个结果」里 `R1 qa 53/17/2` 与其余四组 schema 不同 (其余是 总/拦/放, 这组是 拦/放/真边界, 相加 70) —— 这个列表存在的目的恰恰是终结口径之争。
- `:169` 「验证脚本经 `sed` 编辑须重读」仍是散文, 无 Task 无 SC。
- `:240` SC-3 未标有效面 (49 条里以管道为唯一顶层记号者恒单段)。
- Key Deliverables (`:137-141`) 仍夹在 What.4 与 What.5 之间, 打断 1->6 编号。
- **末轮建议**: 这批已经是第三到第四轮。请 owner 逐条写「采纳 / 驳回 + 理由」, 不要再留白 —— 否则随归档永久变成「诊断过但没人说不做」的悬空项。

---

## 四、优点

1. **四条 R4 Critical 的方向全部改对了, 而且改得比建议更细。** `exec` / `time` 的「仅命令位置」限定不但补进判据表, 还配了 SC-14 的 2 条可分辨 fixture + Tasks 1.1 (a) 写死, 三处挂接; R4-C-3 的裸 `^` 同样是 判据表 + Tasks 1.1 (b) + SC-6 新 fixture 三处挂接。这是四版里第一次「诊断 -> 约束 -> 可证伪断言」三段都落到位。
2. **SC-6 的扩容是本轮最扎实的一处。** 10 -> 14 条, 覆盖了 What.1 声明的全部 6 个块关键字 + 换行位置类别, 且反事实按「哪种坏实现让哪几条红」逐类写死。我按块字符逐条复核过隔离性, 除 M-1 那个计数外, 结论都对。
3. **数字纪律显著改善。** 「跨版本搬运纪律」这一段 (`:171`) 是本 cycle 第一次把「上一轮的实测数字必须在新规则下重跑」写成规范而不是当次勘正; R4-M-1 换掉的那个假证据也换得干净 (新反例含真换行且在 v5 规则下确实可分辨)。本轮我重算的 8 组沿用数字**全对**。
4. **SC-9 拆两腿的收口质量高。** 五席论据被压缩成三句互补的理由 (canonical 证不了投递面 / harness 有时序矛盾 / harness 在 Phase B 结构上跑不到) 且给了 `cmp` 字节前置 —— 比我 R4 建议的版本更简洁, 也把我 M-5 的操作面缺口顺手补了。
5. **owner 拉回 What.4 的裁决方向经四席实测确认正确这件事被诚实记进了设计演进表** (`:18`), 包括「风险从性能面转移到语义保持面 —— 有明确收益的转移, 不是失误」这句定性。这是把审计结论回灌进 spec 而不是只留在报告里的正面样本。

---

## 五、评估

**是否可以继续?** **需要修复** —— 但只卡在一条, 且修法已实测。

**理由**: 全量重审下, v5 的**设计侧**没有新问题; 我 R4 唯一的 Critical (SC-16 事实前提为假) 方向改对了; R4-C-2 / C-3 的判据限定与 SC-14 / SC-6 扩容都经得起独立检验; 141 / 13 / 12 / 305 / 65-49-16-15-1+5 / 366-360 / `:663` / 16 条 `\b` / 2 处 credit `\b` / 11-13 / 21 注入点 / 104 格 / 177.8-267.7 全部第五套独立实现复算属实, 其中 census 与 11/21 两组是**独立构造下逐位吻合**, 置信度很高。

不能 PASS 只因 **C-1**: R4 置信度最高的那条 Critical (两席独立实证) 的**修法本身只闭合了一半**。我用 canonical 直调 + 三实现同管线模拟 + 77 主题对拍三种口径证明: 守卫下 `jq keys<NL>echo done` 与 `cd /tmp<NL>… jq keys<NL>echo finished` 仍是 0->2 (这正是 SC-15 扩容 1 点名要写死的两条 fixture, 而它们的期望值 spec 没写), 另有一整类 (fork 给 credit、裸 builtin 也给、只有守卫不给) 是守卫自己新造的, 覆盖 13/13 处判据、17 个点, 语料 0/6 检出。改用逐行循环复刻 `grep` 的「任一行匹配即真」语义, 77 主题下与 fork **0 分歧** (守卫是 43 分歧), 且单行段走快路径, SC-8 结论不受影响。

另有 **3 条 Major** (SC-16 反事实未随 SC-6 扩容重算 3->6 / SC-8 无未达标处置路径 / census 第三轮无 SC) 与 **7 条 Minor**, 其中 **6 条是 R4-fix 这次 104 行勘正自己新引入的** —— 「勘正动作里新引入错误」在本 cycle 至此是第五、六次。所有修法加起来约 20 行文字 + 1 处实现约束改写, 不触及设计与范围。

**给 owner 的建议**: C-1 与 M-1 是必须落的 (前者决定 Phase B 有没有合法出路, 后者决定 Phase B 读不读得懂反事实); M-2 / M-3 各一行; 七条 Minor 建议一次性逐条裁「采纳 / 驳回」。修完**不需要**再开 R6 完整审计, 但 C-1 的修法 (逐行循环 vs 保守守卫) 属于实现语义选择, 建议由 owner 明确点头再进 A.2。

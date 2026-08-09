---
verdict: REVISE
agent: code-reviewer
round: R4
critical_count: 1
major_count: 5
minor_count: 7
r3_resolved: 3/9
---

# post_spec R4 — secret-guard-per-segment-evaluation (code-reviewer 视角, 第四审 / 末轮)

审计对象: `/home/dev/Aria/openspec/changes/secret-guard-per-segment-evaluation/proposal.md` (v4 + 2026-08-08 前提刷新, 199 行, 全文读)
参照物: canonical `aria/hooks/secret-guard.sh` (698 行, gitlink `af87cae`) / `aria/hooks/tests/secret-guard.test.sh` (798 行) / R3 五份报告原文 / 主仓 `71bdd60` `5fab5b8` / forgejo #172 #178 / 本机 plugin cache
方法: 全部数字**第四套独立实现**机械重算 (`scratchpad/r4cr/`); 13 处 credit 判据**逐字搬进 bash `[[ =~ ]]`** 与 fork 版做 635 主题等价性对拍; 141 pattern + 13 credit 组装成可跑的 before/after 三形态 benchmark, 实测 SC-8 四档 (3 轮 × N=20); canonical 直调复验 13 条行为断言。**未修改仓库任何文件** (本报告除外)。
验收环境: 本轮已核实 harness hook = canonical **字节相同** (见 M-5), 但行为证据仍全部取自 `bash aria/hooks/secret-guard.sh` 直调。

---

## Phase 1: 规范合规性

**判定**: PASS

- Level 2 结构完整 (Why / What §1-§6 / 关键决策 / Impact / 转出 8 / rule6_note / Tasks 1.1-1.9 / SC-1~SC-17), Rule #1 / #5 满足, 落点 `openspec/changes/`。
- owner 2026-08-04 裁定的「拉回 `has_filter` 13 处」已成文并双向挂接: §What.4 + 决策表末二行 + Task 1.3b + SC-15 + SC-8 的达标前提。无越界实现。
- 2026-08-08 前提刷新三处 (§Impact 验收环境 / 转出 7 撤销 / rule6_note dogfood) 与新增的 SC-9 设计问题, **事实全部属实** (逐条核实见 §三)。
- 无 scope creep; 转出 8 项与「本版不做」范围声明一一对应。

进入 Phase 2。

---

## Phase 2

## 一、我 R3 四 Major + 五 minor 的核销 (3/9)

| R3 编号 | v4 处置 | 判定 |
|---------|---------|------|
| **M-1** SC-6 恒绿 (12 条里 ≥3 条两路 exit 相同) | SC-6 改为**直接断言 `safe_to_split()` 返回值** (10 false / 2 true) + 写死双向反事实 | **解决 (采纳修法 2, 比我建议的更彻底)** — 断言下沉到机制层后, payload 是否 benign 不再影响鉴别力 |
| **M-2** 拿 `echo done` 论证「必须限定命令位置」而 `done` 不在关键字集 | `:50` 已删该例, 换成 `ls; echo for >/dev/null`, 并显式记「前一版举 `echo done` 是错的」; 新增 **SC-14** 锁过度触发方向 (3 条 + `safe_to_split=true` 机制断言) | **解决** — 但**同一段的相邻句子重开了同类错误** → 见 **M-1 (本轮)** |
| **M-3** SC-5 `case x in a) ;; esac`→1 不可满足 | 改为 **→2**, 并写明「`split_top()` 直接按 `;` 切, `;;` 产生 2 段; 该命令由 `safe_to_split()` 在上层拦下, 两层职责不可混淆」 | **解决** — 层级归属已显式 |
| **M-4** `corpus_census.py` 有 Task 无 SC | `grep -n -i census proposal.md` = `:108` `:114` `:171` 三处, **SC-1~SC-17 无一提及** | **未解决 (第二轮)** → 本轮 **M-4** |
| m-1 性能表单次点测 + 算术不自洽 | 表整体重写, 191ms 那行已删 | **部分** — 146/158/28/22 仍是单次点测, 且新表引入了更严重的**混基线**问题 → 本轮 **M-2** |
| m-2 「五个结果」里 `R1 qa 53/17/2` schema 不同 | `:112` 原样 | **未解决** |
| m-3 「验证脚本经 `sed` 编辑须重读」无 Task 无 SC | `:118` 仍是散文 blockquote | **未解决** |
| m-4 SC-3 的 49 条中 32 条恒单段, 建议标有效面 | SC-3 (`:184`) 文字未变 | **未解决** |
| m-5 转出 1 记号 `81 条 [^BAR]*` 不精确 + Key Deliverables 打断编号 | `:148` 原样 `81 条`; Key Deliverables 仍夹在 §4/§5 之间 | **未解决 (第二轮)** → 本轮 m-1 |

**核销 3/9。** 三条 Major 全部干净解决且修法优于我的建议; 五条 minor 加一条 Major **零处置、零驳回理由**。这与 R3 tech-lead 记录的「诊断进散文、可执行的锁被丢」是同一形态, 现在已经是**第四轮**。末轮不再重复论证, 只把清单列出供 owner 一次性裁决 (采纳 / 明确驳回, 二选一)。

---

## 二、逐字勘误 — 判据表 / 分段规则表 / 正则可移植性 / 数字

### 2.1 §What.1 判据表逐字核 (镜头 1)

**块字符行** `{` `}` `(` `)` 反引号 `[[` `]]` `<<` `<<<`: 无错项。覆盖 `$()`  (借 `(` `)`) / `(( ))` (借 `(`) / here-string (`<<<`) / heredoc (`<<`)。`<<<` 单列其实被 `<<` 前缀吞掉 (含 `<<<` 必含 `<<`), 冗余但无害。

**块起始关键字行** `for` `while` `until` `if` `case` `select`: 与 bash 复合命令起始保留字比对, 漏 `function` 与 `coproc`, 但两者都不会把 `;`/`&&` 带进不可分段的上下文 (`function f { ...; }` 的 `{` 已被块字符行接住), 不构成缺口。**无错项。**

**作用域型内建行** `exec` `time`: 判据本身正确 (`exec` 建立整 shell 重定向作用域, `time` 是复合命令前缀)。用词不对 —— `type -t time` = **keyword**, `type -t exec` = **builtin**, 把 `time` 叫「内建」是错的 → m-3。

**后台记号行** `&` (单独出现, 非 `&&` / `&>` / `>&` / `|&`): 排除表漏 `<&` (如 `cmd <&3`)。漏了是**朝安全方向**过度降级, 不构成回归 → m-4。

**「命令位置」12 项穷尽性与重叠性** (本轮点名要查的):

| 项 | 承重性 | 核 |
|---|---|---|
| 行首 / 换行之后 | **承重** | R3-C-1 点名的「行首」二义 **已被消解**: 无论把「行首」读成「字符串起始」还是「每行行首」, 与「换行之后」的**并集完全相同**。措辞仍旧但已无后果 —— 记一笔已解决 |
| `;` `&&` `\|\|` `\|` | **承重** | 无异议 |
| `&` | **死条目** | 任何顶层单独 `&` 已被**后台记号行**直接判为不可分段。该位置项无论在不在, 结果都一样, 不可能改变任何判定 |
| `do` `then` `else` `elif` | 近乎冗余 | 有 `do`/`then` 必先有 `for`/`while`/`if`, 而后者绝大多数落在已列位置。唯一残余用途是救 `! if x; then for ...` 这类前缀在表外的形态 |
| `in` | **错项** | `in` 之后是**词表 / case 模式**, 从来不是命令位置 (`for f in …` / `case x in …`)。纯过度触发, 朝安全方向, 但它在表里会让实现者以为存在 `in <命令>` 这种语法 |

结论: 12 项**不构成穷尽枚举** (`!` 未列), 也**有冗余与一个错项**; 真正承重的只有 6 项。全部偏差都朝 fail-safe 方向, 无安全后果, 故计 Minor (m-2)。

### 2.2 §What.2 分段规则表 — 理由与真代码核对 (镜头 2)

| 表内理由 | 我的机械核验 | 判定 |
|---|---|---|
| 「**12 条** pattern 把 `\|` 编码进正则本身」 | `count2.py`: 141 条里含**转义竖线** (即匹配字面管道) 者 = **12** | ✅ 精确 |
| 「按 `\|` 切会让 4 条真泄漏用例由 2 翻 0」 | R1 tech-lead M-4 原始实测, 本轮未复核 (不在 v4 变更面) | 沿用 |
| 「`&` 与重定向记号冲突 (R1 C-1: 打红 2 条合法 credit 写法)」 | 与 R1 原文一致 | ✅ |
| 「换行 — 不切, 会切碎 heredoc body」 | 语料 `:603` `#157 heredoc-style` 即该形态 | ✅ |
| 「`\|\|` 排除会留一字符绕过」 | R2/R3 三方复现 | ✅ |

**分段规则表本身零勘误。**

### 2.3 POSIX ERE 可移植性 (镜头 3) — **本轮唯一 Critical, 详见 C-1**

### 2.4 数字逐个复算 (镜头 4)

| 断言 | 复算命令 / 脚本 | 结果 |
|---|---|---|
| **141** pattern | `count1.py` (定位 `declare -a risky_patterns=(` 至配对 `)`, 计非注释的引号起始行, 行号 402–656) | **141** ✅ |
| **13** 处 `echo \| grep -qE` | `awk 'NR>=318 && NR<=401 && /grep -qE/'` = 13。**口径提醒**: 全文 `grep -qE` 共 **17** 处, 同形状 (`echo "$command" \| grep -qE`) 共 **15** 处 —— 多出的 2 处是 `:302` `:311` 的 `guard:ack` 检测, 不在 `has_filter` 区。spec 的 13 指的是 `has_filter` 区, 表述准确 | **13** ✅ |
| **12** 条把 `\|` 编码进正则 | `count2.py` | **12** ✅ |
| `:663` 全局开关 | `:662` = `if [[ "$command" =~ $pat ]]`, `:663` = `if [[ $has_filter -eq 0 ]]` | ✅ |
| **305** 条 `bash_case` | `grep -c '^bash_case '` = 305 (含函数定义的 `grep -c bash_case` = 306) | ✅ |
| **65 / 49 / 16 / 15 / 1 + 5** | `census2.py` (**第四套独立实现**: `shlex` 精确取载荷 + 6 条 ANSI-C `$'…'` 特判 + 单引号/双引号/反斜杠状态机扫顶层 `;` `&&` `\|\|` `\|`, 换行单列) | **65 / 49 / 16 / 15 / 1**, 换行-only **5** (4 拦 + `#152 FP: multiline benign` 放行), 那 1 条真边界 = `:770 put: KNOWN-LIMIT compound credit leak` — **逐位吻合** ✅ |
| **366 / 360** | 实跑 `bash aria/hooks/tests/secret-guard.test.sh` = `PASS: 366 / 366`; `zsh_case` 6 条 (`:714-:719`, 缩进 2 空格所以 `grep -c '^zsh_case '` = 0, 要用非锚定 grep) 由 `command -v zsh` 门控, 本机 `/usr/bin/zsh` 在场 | ✅ |
| SC-11「其余 5 脚本」 | `ls aria/hooks/tests/*.test.sh` = 6 个, 减本体 = 5 | ✅ |
| SOT **1.65.5** → PATCH **1.65.6** | `aria/.claude-plugin/plugin.json` = `1.65.5` | ✅ |
| 主仓 **5fab5b8** / `.claude/scripts` 已移除 | `git log --oneline -1 5fab5b8` 命中; `ls .claude/scripts` = No such file | ✅ |
| 转出 1「**1** 条 `.*`」 | `count1.py`: 唯一 = `set…posix.*set…grep` | ✅ |
| 转出 1「**81** 条 `[^BAR]*`」 | `count1.py`: 含 `[^BAR]` 任意形态 = **81**; 严格 `[^BAR]*` = **79**; `[^BAR]+` = **7** (kubectl / psql\COPY / redis-cli / rsync / scp / nc / psql -f) | **数对, 记号错, 第三轮未改** → m-1。注: 我 R3 写「另 2 条是 `[^BAR]+`」是**错的**, R3 tech-lead 的 7 才对 —— 我当时数的是「只含 `+` 不含 `*`」, 本轮自我勘正 |

**数字侧结论: 全部属实, 唯一遗留是转出 1 的记号 (数值正确)。**

### 三、2026-08-08 新增文字的事实核对 (镜头 5) — 全部属实

| 新声称 | 核实方式 | 结果 |
|---|---|---|
| Aria#172 已修复并关闭 (2026-08-08) | `forgejo GET /repos/10CG/Aria/issues/172` → `state=closed`, `closed_at=2026-08-08T19:02:53Z`, 标题即 plugin cache 停在 1.63.0 | ✅ |
| 本仓 plugin cache 现为 **1.65.5** | `python3 .aria/probes/plugin-cache-currency.py` → `OK installed=1.65.5 (scope=user) sot=1.65.5` | ✅ |
| `cmp` 判定与 canonical **字节相同** | `cmp ~/.claude/plugins/cache/10CG-aria-plugin/aria/1.65.5/hooks/secret-guard.sh aria/hooks/secret-guard.sh` → 无输出 (相同); marketplace clone 同样字节相同 | ✅ |
| 根因「marketplace clone 停在 `da15d0f` 自称 1.63.0」 | `git -C aria show da15d0f:.claude-plugin/plugin.json` → `"version": "1.63.0"`; 该 clone 现已在 `af87cae` / 1.65.5 | ✅ |
| 机械兜底 = 主仓 `71bdd60` 的 `plugin-cache-currency` | `git show --stat 71bdd60` → 新增 `.aria/probes/plugin-cache-currency.py` + `.aria/state-checks.yaml` | ✅ 存在, **但它比不了字节** → M-5 |
| 衍生转出 Aria#178 | `forgejo GET …/issues/178` → `state=open`, 标题「hook 类 Spec 的 SC 须显式声明测的是哪份副本」 | ✅ |
| rule6_note「仓内 harness 现跑 1.65.5,『我在本仓被拦』重新是有效证据」 | 本轮实证: harness hook 三次拦下我的探针 (`op…inject\b` / `\bpg_dump\b`), 拦截行为与 canonical 一致 | ✅ |

**七条新声称零失真。** 这是本 cycle 第一次「前提刷新」段落经独立核实全数属实, 值得记一笔。

---

## 优点

1. **三条 R3 Major 的修法都比建议更强。** SC-6 没有停在「换 leak-bearing fixture」, 而是整族下沉成 `safe_to_split()` 返回值断言 —— 这一步同时解掉了 R3 里 tech-lead (5 条恒绿) 与 qa (故障注入下后 2 条仍全绿) 的同一诊断, 一处改动核销三份报告的同类 finding。
2. **SC-4 换的 fixture 经我独立复验确实可证伪。** canonical 直调: `perl -ne 'print if /a;b/' /opt/.env` 整条 = **2**; 引号盲切出的两段 `perl -ne 'print if /a` = **0** 与 `b/' /opt/.env` = **0**。即「切错必 0 / 正确必 2」成立, 且整条无块字符不会被 fail-safe 吞掉 —— R3-M-2 (fail-safe 反手打掉 SC-4) 真正闭环。
3. **13 处 credit 逐字搬进 bash 内建是安全的, 我用 635 个主题证了。** `equiv.sh`: 把 `has_filter` 区 13 条 ERE 一字不改地从 `echo \| grep -qE 'RE'` 换成 `re='RE'; [[ "$SUBJ" =~ $re ]]`, 对 305 条整载荷 + 其全部 `;` 分段共 **635** 个主题逐一对拍, **mismatches=0**。这直接给 SC-15 (26 条 fixture) 提供了一个强得多的替代/补充口径 —— 建议 Phase B 把这条全语料对拍写进 SC-15。
4. **owner 拉回的 §What.4 确实是 SC-8 的达标前提, 而且达标幅度很大** —— 见 M-3 表, 四档负载在做了 13 处转内建之后**全部变快**, 最坏档仍有 −38%。这条此前四轮无人实测, 本轮补上。
5. **2026-08-08 的前提刷新没有借「#172 修好了」放松验收**, 反而把 canonical 直调的理由从「被迫」改写成「可复现性选择」, 并主动把 SC-9 的权衡摊开交给 R4 —— 是 Rule #10「AI 不自行裁决闸门」的正面样本。

---

## 问题

### Critical (必须修复)

**C-1. SC-16 与 §6 blockquote 的事实前提为假 —— bash `[[ =~ ]]` 实测**支持** `\b` 与 `\s`; 照 SC-16 字面执行会强制改写 13 处里的 2 处, 与 SC-15 (语义不变) 正面冲突, 而 Rule #10 下 Phase B 不能自行豁免任一条**

- 位置: `proposal.md:116` (§6 blockquote「含 `(?:…)` / `\b` / `\s` —— **bash 的 POSIX ERE 全不支持**」) + `:197` (SC-16「断言不含 `(?:…)` / `\b` / `\s` 等 bash 不支持语法」)
- **验证 1 — 直接实跑** (`scratchpad/r4cr/ere2.sh`, bash 5.2.15):

```
rc=0  A  主体 "pg_dump mydb > f"      正则 "\bpg_dump\b"                → 命中
rc=1  B  主体 "xpg_dumpx"   正则 "\bpg_dump\b"                → 不命中 (证明 \b 真在生效, 不是被当字面 b)
rc=0  C  主体 "vault agent -c" 正则 "vault[[:space:]]+agent\b"                → 命中
rc=1  D  主体 "vault agentx"   正则 "vault[[:space:]]+agent\b"                → 不命中
rc=0  E  主体 "for x"          正则 "for\sx"              → \s 支持
rc=0  F  主体 "abc"            正则 "\w\w\w"               → \w 也支持
rc=2  G  主体 "for x"          正则 "(?:for)"              → **只有非捕获组真的编译失败**
```

- **验证 2 — 被审代码自己就是反例**: `:662` 的匹配循环用的正是 `[[ "$command" =~ $pat ]]`, 而 141 条 pattern 里 **16 条含 `\b`** (`\bpg_dump\b` / `\bmysqldump\b` / `vault[[:space:]]+agent\b` / `\bcp…` / `(\bod\b)…` / `op…(item|read|inject)\b` 等), 测试套件 **366/366 全绿**。若 bash 不支持 `\b`, 这 16 条早该静默失配、相应用例早该红。
- **验证 3 — 冲突是必然触发的**: 13 处 credit 判据里 **2 处含 `\b`** —— `:361` `…grep[[:space:]]+(-v|--invert-match)\b` 与 `:397` `…(sha256sum|md5sum|sha1sum|sha512sum)\b`。而 `equiv.sh` 已证**逐字搬运这 13 条在 635 主题上与 fork 版 0 分歧**。于是 Phase B 面对二选一:
  1. 逐字保留 → SC-15 (语义不变) **过**, SC-16 (不含 `\b`) **不过**;
  2. 把 `\b` 改写成 `([^a-zA-Z]|$)` 之类 → SC-16 过, 但语义**真的变了** (`\b` 把 `_` 和数字算词内字符, 字符类不算; 例如 `grep -v9`), SC-15 只有在恰好有覆盖该差异的 fixture 时才抓得到 —— 也就是说这个改写要么破 SC-15, 要么在 SC-15 的 26 条 fixture 视野外**静默改变拦截面**。
- 为什么是 Critical: 它不是「一句话说错」。SC-16 是 Rule #10 意义上的 enabled 闸门, 它与另一条闸门 SC-15 在**必然发生的输入**上互斥; 且它的判据源自一条**可被本仓代码当场证伪**的事实断言。Phase B 无论选哪条都会被卡, 而 spec 没有给裁定。这正是 memory `feedback_spec_inherits_upstream_dec_errors` 与 `feedback_never_write_unverified_impossibility_claims` 的合流形态 —— R3 backend M-2 把三个语法捆在**同一条正则**里测 (`'(?:for|while)\s'` 一次 rc=2), 把 `(?:` 的编译失败归因给了全部三个; v4 忠实继承了这个归因错误。
- 修法 (三行):
  1. `:116` 与 `:197` 的禁用清单**收窄为 `(?:…)` 一项**, 并注明「实测 rc=2 编译失败」;
  2. 另起一句: 「`\b` / `\s` / `\w` 是 GNU regex 扩展, **glibc + bash 实测可用** (本 hook 现有 16 条 pattern 与 2 处 credit 判据已在生产使用), 非 POSIX —— 允许保留, 但须在 SC-16 记为『已知 GNU 依赖』; 非 glibc 平台 (macOS/BSD/musl) 的行为差异归转出」;
  3. SC-16 的反事实改写为「逐字搬运含 `(?:…)` 的 Python 原型 → `safe_to_split()` 的**关键字分支**静默失效 → SC-6 里 `for` / `while` / `if` **三条**转红」。**注意原文写「SC-6 前 10 条全红」也是错的**: 前 10 条里 `{ }` / `( )` / `[[ && ]]` / `for ((;;))` / 反引号 / `$()` / heredoc 共 7 条靠**块字符**判定 (纯字符类, 不受正则语法影响), 只有 `for` / `while` / `if` 三条纯靠关键字分支。反事实写宽了会让 Phase B 以为没红满就是别处出了问题。

### Important (应该修复)

**M-1. §What.1 给「换行必须计入」配的实测例子里**没有换行**, 而且该例在 v4 自己的判据下走 fallback, 论证不成立 —— 与 `:50` 刚刚勘正掉的 `echo done` 是同一类错误, 隔一句话复发**

- 位置: `proposal.md:48`
- 原文 (python `repr` 取字节, 确认无 `\n`):

```
…**换行必须计入** —— 否则多行命令第 2 行起的 `for`/`while`/`if` 检测不到
(实测 `sleep 1 & for f in a; do cat /opt/.env; done >/dev/null` 由 0 翻 2)。
```

- 两处不成立:
  1. 该命令**一个换行都没有**, 它是 R3-C-1 用来论证「`&` 之后也是命令位置」的例子, 被搬来支撑「换行」的结论;
  2. 在 v4 判据下它**根本走不到分段** —— 它含顶层单独 `&`, 直接命中**后台记号行** ⇒ fallback ⇒ 恒为现状。canonical 直调复验: 整条 = **exit 0** (与现状一致)。所以它既证明不了换行, 也证明不了位置表里的 `&` 项 (那一项已被后台记号行完全吸收, 见 m-2)。
- 为什么重要: `:50` 的注解刚刚花了一整句记「前一版举 `echo done` 为例是**错的**, 论证不成立, R3 code-reviewer 勘正」; 紧邻的 `:48` 又摆了一个同类错误的例子。Tasks 1.1 要求「写死该清单」, 实现者读到「换行必须计入 (实测 X 由 0 翻 2)」而 X 里没有换行, 只能靠猜。
- 修法: 换成 R3 tech-lead 实测过的真换行反例 (`cd /tmp` + 换行 + `for f in a b; do <leaky>; done >/dev/null`, cur=0 → 裸切 post=2); `sleep 1 & for …` 那条若要保留, 移到**后台记号行**下面, 并说明「该形态在 v4 下由后台记号行接管, 位置表里的 `&` 是冗余项」。

**M-2. §3 性能表四行混用了三个不同基线, 一处都没标注; 而这张表是 owner 拉回 §What.4 的直接依据**

- 位置: `proposal.md:80-85`
- 表头是「每段先算 credit | 先 pattern 后 credit | 结论」:
  - 第 1/2 行 (2 段 / 3 段全 benign) 的「省 80% / 省 86%」= **pattern-first vs credit-first** (表内两列相除, 自洽);
  - 第 3/4 行 (全命中) 两列都是 `—`, 而结论写 **+102% / +583%** —— 追到 R3 tech-lead 与 backend 原始数据, 这两个百分比是 **pattern-first vs 现状整命令判定**, 完全不是同一个基线;
  - 第 4 行末尾「此档重排还更慢」又是**第三个**比较 (pattern-first vs credit-first, tech-lead 的 267.7 vs 177.8)。
- 为什么重要: 同一列里「省 80%」与「+102%」不可比。读者 (含 Phase B 与将来的收口者) 会把「省 80%」当成相对现状的收益, 从而低估逐段化的真实成本曲线; 而 SC-8 的判据恰恰是**相对现状**的增幅 ≤50%。表与闸门口径不一致。
- 修法: 加一列「基线」, 或把四行统一改成**相对现状整命令**的口径 (可直接用我 M-3 表的数)。

**M-3. SC-8 的「§What.4 是达标前提」四轮无人实测; 我实测支持它 (甚至四档全部变快), 但 spec 里写死的 +583% 不可复现, 且没有未达标时的处置路径**

- 位置: `proposal.md:189` (SC-8) + `:85` (§3 表 3 段全命中行)
- 我把 canonical 的 141 条 pattern 与 13 处 credit 判据机械抽出, 组装成三种实现在同一进程内对比 (`bench_lib.sh`; `whole_current` = 现状整命令 (13 fork + 扫 141); `after_v4` = 逐段 + pattern-first + credit 走 bash 内建; `after_nofix` = 逐段 + pattern-first + credit 仍 fork)。3 轮 × N=20, 单位 μs/次:

| 负载 | 现状 whole | v4 (含 §4) | v4 缺 §4 | v4 增幅 | 缺 §4 增幅 |
|---|---|---|---|---|---|
| 1 段 benign | 48.4 / 51.4 / 66.8 ms | 7.6 / 7.6 / 7.7 | 13.3 / 9.4 / 8.9 | **−84% / −85% / −88%** | −72% / −81% / −86% |
| 2 段 benign | 49.6 / 48.6 / 55.7 | 15.4 / 15.8 / 14.8 | 14.4 / 15.8 / 16.2 | **−68% / −67% / −73%** | −70% / −67% / −70% |
| **2 段全命中 (迁移写法)** | 45.6 / 49.9 / 47.7 | 3.5 / 3.2 / 3.3 | 107.7 / 96.1 / 78.3 | **−92% / −93% / −93%** | **+136% / +92% / +64%** |
| **3 段全命中 (迁移写法)** | 50.6 / 45.3 / 47.6 | 5.4 / 3.4 / 5.1 | 124.7 / 134.5 / 151.4 | **−89% / −92% / −89%** | **+146% / +196% / +218%** |
| 3 段全命中 (末位 pattern, 最坏) | 54.2 / 57.2 / 60.1 | 33.3 / 21.7 / 28.7 | 152.9 / 137.1 / 146.6 | **−38% / −62% / −52%** | +181% / +139% / +143% |
| 5 段全命中 | 49.5 / 53.9 / 54.8 | 7.6 / 8.8 / 11.7 | 213.8 / 204.7 / 237.6 | −84% / −83% / −78% | +331% / +280% / +333% |

  三条结论: (1) **owner 的裁定是对的** —— 13 处转内建之后, 四档 SC-8 负载没有一档变慢, 最坏档 (末位 pattern 命中) 仍 −38%, ≤50% 闸门远远达标; (2) **不做 §4 则确实破闸**, 方向与 R3 一致; (3) **但 spec 写死的 +583% 我复现不出来** —— 同构配置 (3 段全命中、缺 §4) 我三轮测得 **+146% / +196% / +218%**。差 3 倍。
- 为什么重要: SC-8 明写「实测数字须写进 spec」, 于是 +583% 会成为 Phase B 的对照基线 (memory `feedback_spec_inherits_upstream_dec_errors`); 而更要紧的是 spec 把「§4 是达标前提」当断言写、却没给「万一 (d) 档仍 >50% 怎么办」的路径 —— Rule #10 下 Phase B 不能自行降门。
- 修法: (a) 把 +583% 改标为「R3 tech-lead 单次点测口径, 另一独立实现同构复算为 +146~218%; 二者均远超 50%, 结论不变」; (b) 补一句处置: 「若 (d) 档实测仍 >50%, 不得自行降门, 须以 handoff 请 owner 复议」; (c) 可直接把上表 (含现状基线) 收进 §3, 顺带解掉 M-2。

**M-4. `corpus_census.py` 仍然只有 Task 没有 SC (第二轮) —— 而它是「五次计数争议」的唯一根治交付物**

- 位置: `:108` (Key Deliverables) + `:114` (§6) + `:171` (Task 1.4); `grep -n -i census proposal.md` 三处命中, SC-1~SC-17 **零命中**
- 本轮我用**第四套独立实现**复算, 65/49/16/15/1 + 5 逐位吻合 —— 数字本身没有任何问题, 问题**只在计数器自己不被验证**: 没有任何断言要求它跑出这组数。它一旦算错, 会成为「权威的错答案」, 而 SC-2 的 15/5 与 SC-3 的 49 全是它的输出。
- 对照不对称仍在: 本 spec 为 `secret-hygiene.md` 的计数专门加了 SC-13, 同一缺陷形态在 census 上原样保留, 两轮未处置也未驳回。
- 修法 (一行): 加 SC-18 或并入 SC-3 —— 「`python3 aria/hooks/tests/corpus_census.py` 输出 `65 / 49 / 16 / 15 / 1` + 换行 `5 (4 拦 1 放)`, 与 §Impact 迁移面逐数字机械比对, 不一致即失败」。qa R3 §2 与 knowledge R3 Minor-1 也各自要过同一件事。

**M-5. §Impact 把「字节相同」与「机械兜底 = `plugin-cache-currency`」并排写, 但该探针**只比声明的版本号, 从不比字节**; 而本 spec 一 bump 到 1.65.6, harness 与 canonical 就会立刻再次分叉 —— 这直接决定 SC-9 怎么裁**

- 位置: `proposal.md:141` + `:154` (转出 7 撤销段)
- 核实: `.aria/probes/plugin-cache-currency.py` 里只有 `_parse_version` / `_marketplace_declared_version` / 与 SOT `version` 比对, **无 `cmp` / 无 hash / 无字节比较** (`grep -n "cmp\|sha\|hash\|byte\|version"` 只命中 version 相关行)。它的输出也印证: `OK installed=1.65.5 (scope=user) sot=1.65.5`。
- 两个后果:
  1. 「字节相同」这件事是我这轮**手动 `cmp` 出来的**, 不是任何机械闸保的。声明与兜底之间有缺口, 而 §Impact 的行文会让读者以为探针保了它;
  2. 更关键: 探针的判据是 `installed == sot`。**本 spec Phase B 第一步就是把 SOT bump 到 1.65.6**, 此后直到 plugin 重新发布并被 Claude Code 拉取之前, `installed=1.65.5 < sot=1.65.6`, 探针转红, harness 跑的**必然不是** canonical。也就是说, 在本 spec 的整个开发窗口里, 「harness 链可信」这个刚刚成立的前提**会由本 spec 自己打破**。
- 旁证: 本机 `~/.claude/plugins/cache/10CG-aria-plugin/aria/` 下**同时存在 `1.63.0` 与 `1.65.5` 两个版本目录** (均 `Aug 8 18:4x`)。哪一份是活的由运行时解析决定, 不是 SC 能钉住的。
- 修法: `:141` 把「机械兜底」一句改成「版本号层面的机械兜底 (探针不比字节; 字节一致本轮由人工 `cmp` 核实)」, 并把上面第 2 点写进 SC-9 的裁定依据。

### Minor (建议修复)

**m-1. 转出 1 的记号 `81 条 [^BAR]*` 第三轮未改 (数值对, 记号错)**
- 位置: `:148`。`count1.py` 口径: 含 `[^BAR]` **任意量词** = **81**; 严格 `[^BAR]*` = **79**; 含 `[^BAR]+` = **7** (kubectl get secret / psql \COPY / redis-cli GET / rsync / scp / nc / psql -f, 与 `*` 有重叠)。
- 建议写「81 条含 `[^BAR]` 有界字符类 (`[^BAR]*` 79 + `[^BAR]+` 7, 有重叠)」。**另**: 我 R3 m-5 写「另 2 条是 `[^BAR]+`」是错的 (只数了「含 `+` 且不含 `*`」的), R3 tech-lead 的 7 才对 —— 本轮自我勘正。

**m-2. 「命令位置」表: `&` 是死条目, `in` 是错项, `!` 漏列**
- 位置: `:48`。理由见 §2.1。三项都朝安全方向, 无回归风险, 但 Tasks 1.1 要照这张表写代码, 建议: 删 `&` (注明已被后台记号行吸收) / 删 `in` (它之后是词表不是命令) / 补 `!`。

**m-3. `time` 不是「内建」**
- 位置: `:45`。`type -t time` = **keyword**, `type -t exec` = **builtin**。建议该行改为「作用域型前缀 (保留字 / 内建)」。

**m-4. 后台记号行的排除表漏 `<&`**
- 位置: `:46`。`cmd <&3; other` 里的 `&` 既非 `&&`/`&>`/`>&`/`|&`, 会被当后台记号 ⇒ 过度降级 (安全方向)。补进排除表或明说「过度降级已接受」。

**m-5. §3 伪代码 `pat` 未绑定 + 无 `guard:ack` 位置 (R3 tech-lead m-5 / qa Minor-3, 第二轮未改)**
- 位置: `:70-73`。`if any(seg =~ pat …)` 之后 `BLOCK(pat, seg)` 用了未绑定的 `pat`, 而现状 BLOCKED 消息含 `Matched pattern: $pat` (`:664` 起), SC-9 dogfood 又要看这条消息。建议写死「取首个命中的 pattern, 与 `:662` 顺序遍历一致」, 并在 `safe_to_split` 之前补一行 `if has_command_level_ack(command): return ALLOW` (SC-12 的语义在伪代码里目前不可见)。

**m-6. §5 「五个结果」里 `R1 qa 53/17/2` 与其余四组 schema 不同 (第二轮未改)**
- 位置: `:112`。其余四组是 (总/拦/放), 这组是 (拦/放/真边界), 相加 70。这个列表的存在目的恰恰是终结口径之争。建议写成「R1 qa 70/53/17 (另报真边界 2 条)」。

**m-7. R3 三条 minor 原样顺延, 无处置也无驳回**
- `:118` 「验证脚本经 `sed` 编辑须重读」仍是散文, 无 Task 无 SC (我 R3 m-3);
- SC-3 (`:184`) 未标有效面 —— 49 条里仅 `\|` 为唯一顶层记号者恒为单段, 真正走 split/fallback 的是少数 (我 R3 m-4);
- Key Deliverables (`:104-108`) 仍夹在 §4 与 §5 之间, 打断 §1→§6 编号 (我 R3 m-5)。
- 末轮建议: 上述连同 M-4 与 m-1/m-6, 请**逐条写「采纳 / 驳回 + 理由」**, 不要再留白 —— 这是第四轮同一批条目。

---

## 四、留给 R4 的 SC-9 设计问题 — 裁定

**问题**: 既然 harness 链已可信, SC-9 (dogfood) 是否应改为经 harness hook 链验证?

**我的裁定: 两条都要, 但闸门只挂 canonical; harness 链做「条件必跑、失败即环境阻塞」的第二腿。具体是把 SC-9 拆成 SC-9a / SC-9b。**

**理由 (全部基于本轮实测, 不是偏好)**:

1. **「harness == canonical」是**今天**的偶然属性, 不是结构属性。** 我 `cmp` 过: 今天确实字节相同。但 `~/.claude/plugins/cache/10CG-aria-plugin/aria/` 下**同时躺着 `1.63.0` 与 `1.65.5` 两个版本目录**, 活的是哪个由运行时解析, SC 钉不住。
2. **决定性的一条: 本 spec 自己会打破这个前提。** Phase B 第一步 bump SOT 到 **1.65.6**; 在 plugin 重新发布并被拉取之前, cache 仍是 1.65.5。也就是说, **在本 spec 的整个开发与验收窗口内, harness 链跑的一定是旧代码** —— 若 SC-9 改成「只经 harness 链」, 它在 ship 前**结构上不可能通过**, 变成 goal-hook 式的不可达前置 (memory `feedback_goal_hook_precondition_must_be_in_session_achievable`)。
3. **但反过来, 纯 canonical 也确实证明不了 #172 那一类。** #172 的教训正是「canonical 一直对、用户加载的是错的」, 而本轮已实测: 旧 cache (1.63.0, 688 行, **140** 条 pattern) 缺 `nomad var put` 那条。canonical 直调对这种偏差零检出力。
4. 因此「二选一」是伪选择: 两条腿测的是**不同命题** (「判据对不对」vs「用户真的被拦没」), Aria#178 要求的也正是**显式声明测的是哪一份**, 而不是二选一。

**建议落地 (改动 3 行)**:

- **SC-9a (闸, 必过)**: canonical 直调端到端脚本, 覆盖 5 类实际使用形态 —— 即现文, 不动。理由改为「可复现性: 不依赖 plugin 安装态, 任意环境可复算」。
- **SC-9b (条件必跑, 不可自行跳过)**: 同 5 条经 harness hook 链实跑; **前置断言 `cmp "$CLAUDE_PLUGIN_ROOT/hooks/secret-guard.sh" aria/hooks/secret-guard.sh`**。
  - `cmp` 相同 ⇒ 5 条必须与 SC-9a 结果逐条一致, 否则 SC-9b 失败;
  - `cmp` 不同 ⇒ SC-9b 记为 **BLOCKED-BY-ENV**, 写进 handoff 并注明当时的 installed/sot 版本; **不判 spec 失败, 也不允许改判为 PASS**。
  - 关键点是**字节比对而不是版本比对** —— 见 M-5, 现有探针只比版本号, 挡不住「版本号对、内容不对」。
- **ship 后一次性收口 (进 Task 1.9 或转出)**: v1.65.6 发布并被拉取后, 重跑 SC-9b 的 5 条并把结果回填 CHANGELOG。这是唯一能真正回答「用户被拦住了吗」的时刻, 也正好把 Aria#178 的规范要求在本 spec 上先跑通一遍。

---

## 建议

1. **C-1 暴露的元问题值得单独记一笔**: R3 backend 把三个语法特性捆进**同一条正则**做了一次测试, 得到一个 rc=2, 就归因给全部三个; v4 忠实继承。**特性支持性断言必须逐特性单测** —— 我这轮把它拆成 7 条独立探针, 成本不到一分钟, 结论完全翻转。建议连同 memory `feedback_never_write_unverified_impossibility_claims` 一并更新。
2. **Phase B 可直接复用本轮两个产物**: (a) `equiv.sh` 的 635 主题 fork-vs-builtin 对拍 —— 比 SC-15 的 26 条 fixture 强一个量级, 建议直接写进 SC-15; (b) `bench_lib.sh` 的三实现同进程对比 —— SC-8 要求「同机同会话对比」, 这个骨架现成可用, 且已经把「现状基线」这一列补齐了 (M-2 缺的正是它)。
3. **末轮的处置纪律**: 本 spec 走到第四轮, 设计侧早已收敛 (三版表 + 8 条自陈 + fail-safe 启发式定性都经得起独立检验), 剩下的全是**文字级精度**与**上轮 minor 的留白**。建议 owner 一次性裁决 §一 表里那 6 条未处置项, 让它们要么进 Tasks/SC, 要么在 spec 里留一句驳回理由 —— 否则它们会随归档永久变成「诊断过但没人说不做」的悬空项。

---

## 评估

**是否可以继续?** 需要修复 (但只需**文字级**修订, 不需要第五轮完整审计)

**理由**: v4 的设计侧本轮无新问题 —— fail-safe 从「保证」降为「启发式」+ 转出 8 的定性经得起检验; 我 R3 的三条 Major (SC-6 恒绿 / `done` 举例错 / SC-5 层级混淆) 全部解决且修法优于建议; SC-4 的新 fixture 我独立复验确实「切错必 0、正确必 2」; 141 / 13 / 12 / 305 / 65-49-16-15-1+5 / 366-360 / `:663` / 1.65.5 / `5fab5b8` **全部机械复算属实** (第四套独立实现), 2026-08-08 新增的**七条**前提刷新声称经 forgejo API + `cmp` + `git show` 逐条核实**零失真**; 我还补上了四轮无人做的 SC-8 实测 —— 结果**支持** owner 拉回 §What.4 的裁定 (四档全部变快, 最坏档仍 −38%)。

不能 PASS 只因一条 **Critical**: SC-16 的判据建立在一个**可被本仓代码当场证伪**的事实断言上 (「bash 不支持 `\b` / `\s`」—— 而 141 条 pattern 里 16 条正用着 `\b` 跑在 `[[ =~ ]]` 上、366 测试全绿), 且它与 SC-15 在**必然发生的输入**上互斥 (13 处 credit 里 2 处含 `\b`, 逐字搬运 635 主题 0 分歧却违反 SC-16, 改写则动语义违反 SC-15), Rule #10 下 Phase B 两条闸都不能自行豁免。五条 Major 里 M-1 (「换行」例子里没换行) 与 M-2 (性能表混三个基线) 是同一类精度问题, M-3/M-4/M-5 各带一个可执行修法。**全部修法加起来不超过 15 行文字, 无一处触及设计或范围**; 建议 owner 直接采纳后放行 Phase B, 不再开第五轮。

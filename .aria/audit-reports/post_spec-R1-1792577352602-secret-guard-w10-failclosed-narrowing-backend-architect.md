---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-10-21T13:00:48.878Z
context: openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R1 审计报告 — backend-architect 席位

- 对象: `openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md`（主仓 `acd6a95`），基线 aria v1.76.1（`59e333c`）。
- 侧重: 增长上限 / 大副本分流 / 只拦被引用值 / for 列表止于换行 这四处在 bash 3.2.57 与 5.2.15 下的算法正确性与性能上界。
- 环境: Linux 6.17，`taskset -c 0,1 nice -n 19`，宿主 4 核共享、实验时 load average 约 1.8，LANG=en_US.UTF-8。时间类数字带这个噪声。F-01 的反例 k=5 多次运行是 5.2–7.8 s（刚过 5 s），k=8 是 9.5 s；攻击者只需要加行数，所以结论不依赖这点噪声。
- 方法: 在 scratchpad 里对基线 hook 打补丁做**模拟副本**（`hook-G/D/D2/F/DF/AB/nosmax.sh`，均由 `hook-base.sh` = v1.76.1 复制而来），用真 bash 3.2.57（`/home/dev/.aria/tools/bash-3.2.57/bash`）和 5.2.15（`/bin/bash`）端到端喂 `{"tool_name":"Bash",...}`。**没有改仓内任何文件**。凭据形路径全部在运行时用 `~/.aw` + `s/cre` + `dentials` 拼装，脚本和本报告里都没有连续字面量；app.ini 金丝雀用套件自己的 `/etc/forgejo/app.ini`。
- 没有读其他席位的报告。

## 摘要

结论 **FAIL**：3 条 Critical、8 条 Major、5 条 Minor。

1. **F-01**：设计的成本依据（「credit 的平方级成本只跟单行长度有关」）经实测不成立。按规格实现后，一条 40 KB、每行都 ≤ 8192 字符的整串命令（变量间接读取凭据）会让 hook 跑 5.4–6.3 s，基线 0.6–1.6 s 内就按尺寸拦下。B 时间护栏帮不上忙。
2. **F-02**：D 的「文本里有没有 `$NAME`」比 `_sg_vx_apply` 实际会代入的范围窄。构造出来的引用（`B='$'; C=A; eval $P $B$C`）会在超大值上放行，基线 VMAX 会拦。
3. **F-03**：§4 把换行排除出 for 列表后，反斜杠续行的列表项被丢掉，基线会拦的读取变成放行。

## 验证状态总表

「实验」= 我在这台机器上用真 bash 做过小实验；「读码」= 只读了源码。脚本都在 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217audit/backend-architect/`。

| 设计点 | 子项 | 状态 | 实验 |
|---|---|---|---|
| 1 增长上限 | `lim` 入口一次算出、作为绝对 MAX 传给 `_sg_vx_replace` 与 `$NAME` 循环 | 实验（3.2 + 5.2） | `exp15.sh` + `mkG.py` |
| | 边界：增长恰为 8192 放行、8196 拒；花括号形同口径；缩水为负增长 | 实验（3.2 + 5.2） | `exp15.sh` |
| | 扩展整串检查 `:1553-1566` 在 apply 改成增长口径后的行为 | 实验（仅 5.2；3.2 被 C 的时间预算抢先，见 F-04）+ 读码 | `exp23.sh` `exp24.sh` |
| 2 大副本分流 | `SECONDS*2 >= budget` 的整数语义、粒度、环境导入 | 实验（3.2 + 5.2） | `secs1.sh` `secs2.sh` `secs3.sh`；env 导入见 F-07 |
| | 最长行：read 循环 / 参数展开剥离 / 正则 `{N,}` / token 循环 的代价 | 实验（3.2 + 5.2） | `exp6.sh` `exp6d.sh` `exp16.sh` |
| | credit 成本模型（逐行、逐 token、跨行） | 实验（3.2 + 5.2，除注明） | `exp4` `exp2` `exp17`(两版) `exp11` `exp12`(两版) `exp13`(两版) `exp21`(仅 5.2) `exp5`(仅 5.2) |
| | 只匹配规则路径与 W12 的一致性 | 实验（仅 5.2）+ 读码 | `exp19.sh` |
| 3 只拦被引用值 | 文本引用测试 vs 构造引用；assignment 与 for-list 两处 | 实验（3.2 + 5.2） | `exp7.sh` `exp22.sh` + `hook-D.sh` `hook-D2.sh` |
| | 链式 / `${}` / 前缀撞名 / 引号内 / heredoc 内 | 读码（文本子串测试是超集，语义推演；构造引用是唯一缺口） | — |
| | 真 shell 对构造引用的语义（eval 展开） | 实验（3.2 + 5.2） | `exp8.sh` + 手跑 |
| 4 for 列表止于换行 | 正则里放真换行：3.2 与 5.2 都行 | 实验（3.2 + 5.2） | `exp9.sh` |
| | 字面量 `\n` 放进方括号的陷阱 | 实验（3.2 + 5.2） | `exp10.sh` |
| | 反斜杠续行丢失 | 实验（3.2 + 5.2） | `exp7.sh` `exp9.sh` |
| 其他 | SC-6 / SC-7 的 bf 条件 | 实验（5.2） | `exp22.sh` |
| | 套件里受影响的既有用例 | 读码推演，**未实跑套件** | — |
| | macOS BSD regex 的 `RE_DUP_MAX`、Windows MINGW64 | **未核实**（无环境） | — |

## 审计结论

### Critical

#### F-01
- type: issue（含一项需 owner 决策的处置姿态，见 F-11）
- severity: **Critical**
- category: architecture
- scope: proposal「8192 原本要防什么」第 1 条；What Changes §2 步骤 2「最长行 ≤ `_SGV_LMAX`」；「不变量与范围外」第 1 条；SC-9 判据 3；Impact「头注释改写」
- 验证方式: 实验（3.2 + 5.2；`exp5`、`exp21` 仅 5.2）+ 读码
- 摘要: 「credit 的平方级成本只跟单行长度有关，不跟总长」不成立，所以「最长行 ≤ 8192 ⇒ 逐行 credit 成本有上界」也不成立。按规格实现，变量间接读取凭据 + 多行填充的整串大副本会让 hook 超过 hooks.json 配的 5 s 超时（repo 自己的前提是此时 fail-open），而基线对同一输入 0.2–1.6 s 内按尺寸拦下。「不新增 fail-open 路径」被反例推翻。
- 证据:
  1. 代码事实（成本构成）。`_sg_compute_credit` 的成本有三项，LMAX 只碰到其中一项的一个点：
     - 逐行固定成本：`_sg_line_match`（`secret-guard.sh:182-188`）被调 14 次（`:497-:559`），每次对每一行重新求值一遍正则。实测 0.48–0.71 ms/行（5.2）、0.72–0.92 ms/行（3.2）。2000 行 × 16 字符（34 KB，最长行 16）credit 1.4 s（5.2）/ 1.6 s（3.2）。`exp13.sh`。
     - 逐 token 平方项：`:476` 的 `$_SG_SRVCFG` 以 `[A-Za-z0-9._-]*` 开头，一个 8000 字符 token 单独就 1.17 s。`exp5.sh`（xtrace 时间戳，仅 5.2）。这一项是**逐 token 累加**，不是取最大：k 行各一个 token，成本 ×k。
     - 跨行项：`:476` 第二个 `=~` 的 `$_SG_PROCTAB_ALL` 含 `_SG_PS_REMOTE_T`（`:446`），其中 `(ssh|…|watch)[^|]*[[:space:]…]` 的 `[^|]*` **跨空白也跨换行**。proposal `:43` 说的「它的通配段不跨空白」对这一支是错的。实测 1000 行 × `watch watch watch watch`（24 KB，最长行 23）这个正则单独就 2.07 s（5.2）/ 2.97 s（3.2）；`exp12.sh`。
  2. 实验 A（长 token 行，最直接）。`exp4.sh`：副本 = k 行 × 8000 字符单 token + 末尾变量拼出的读取，`_sg_judge_one` 耗时（其中模式循环仅 27–205 ms，其余全是 credit）：

     | k | 副本长度 | bash 5.2 | bash 3.2.57 |
     |---|---|---|---|
     | 1 | 8 KB | 0.91 s | 0.93 s |
     | 2 | 16 KB | 2.0 s | 1.85 s |
     | 3 | 24 KB | 3.2 s | 2.97 s |
     | 5 | 40 KB | 5.3 s | 5.13 s |
     | 8 | 64 KB | 9.5 s | 未跑 |

  3. 实验 B（整个 hook 端到端）。`exp2.sh`：用 `: $(:)` 强制整串模式，路径由变量 `R=~/.aw`、`S=s/cre…dentials` 拼出，`$P ${R}${S}` 读取。`hook-base.sh` 对 k=5（40 KB）按尺寸拦，0.59 s（5.2）/ 1.63 s（3.2）；模拟新版（`hook-nosmax.sh`：把 SMAX 抬高，副本照建，随后走**同一个** `_sg_judge_one`，这正是新版在「增长小、各行 ≤ 8192、已耗时 < 1 s」时会走的路径）5.4 s（5.2）/ 6.3 s（3.2）。k=3 为 3.5 s / 3.9 s。
  4. 实验 C（B 是不是安全网）。`exp17.sh`，在 `hook-AB.sh` 上同时模拟 A 与 B（副本 > 8192 时先看 `SECONDS*2 >= budget`），k=5，随机起始相位各 6 次：bash 3.2.57 有 4 次被护栏拦下（1.6–2.2 s），2 次跑到 6.1–6.7 s；bash 5.2 **0 次**被拦，全部 5.2–7.8 s。原因：护栏只看判定**前**已耗时，而这类输入首遍很便宜（0.6 s），贵的是二遍里的 credit。proposal 的依据「大副本判定与首遍判原串的代价相近」在这里不成立。
  5. 成本不是「长行」专属。`exp11.sh`：2000 行 × `ssh`（总长 8 KB，最长行 3 字符）credit 3.4 s；`exp21.sh`：1500 行 × `watch watch watch watch`（36 KB）5.9 s，×8 词（72 KB）22 s。所以「行数上限 + Σlen² 上限 + 总长上限」这类只看行形状的门也封不住包装词密集的文本（跨行项）。
  6. 背景（要如实写进规格，也是 owner 决策的依据）。基线首遍对**字面读取**有同样的暴露：`exp18.sh`，同样的 5 × 8000 填充 + 字面凭据读取，基线整串模式 5.4 s；#228 B.1 的 E3 也记录了 14 KB 填充首遍约 6 s。所以对**刻意**的攻击者，新增的这条路没有多出能力。但是：（a）proposal 的不变量和 SC-9 判据 3 写的是相反的结论；（b）项目自己在 #228 决定 7 里的标准是「不比基线差——同样输入基线更早 fail-open」（`openspec/changes/secret-guard-scan-cost-and-firstpass-cap/proposal.md:147`），本条反例里基线是**拦下**而不是 fail-open，所以按这条标准是变差；（c）M6 当时关掉的正是「W10 第二遍被填充拖超时」这一类（`secret-guard.sh:577-583`），#228 又已搁置。
  7. 超时配置: `aria/hooks/hooks.json:32-33`，`bash ${CLAUDE_PLUGIN_ROOT}/hooks/secret-guard.sh` 配 `"timeout": 5`。
  8. #228 B.1 的出处: 同一批文字写「`_sg_compute_credit` 只是次要项（仅单个长 token：+0.9s@8KB）」（`scan-cost-and-firstpass-cap/proposal.md:50`）。它的 pilot 只测了单行单段形状（`pilot-8-32.tsv`），没测多行，所以「逐行」的模型缺了行数项和跨行项。#217 沿用了这个不完整的模型。
- 建议改法:
  1. 先改事实。Why 第二条和头注释都按实测写：credit 成本 ≈ 行数 × 0.5–0.9 ms + Σ token² × 约 1.7e-8 s + 跨行包装词项；LMAX 只封住「单个 token 不超过 8192」。
  2. 在下面三条里选一条，并把选择写进规格（选择权在 owner，见 F-11）:
     - (a) 对 credit 路径加真正管用的门。一遍 `read` 同时算行数、Σlen²、总长；任一超限就走「只匹配规则」。但要写明：这个门对包装词密集的文本封不住（见证据 5），要封住须把总长压到约 16 KB 以下（估计，没有逐点实测），或修 `:476`/`_SG_PS_REMOTE_T`。
     - (b) 把 #217 排在 #228 的 r2c/r2f（credit 与跨行项的根治）之后，或把那一部分并进来。
     - (c) 明确声明残余：大副本二遍成本不设上界，与首遍（#228）同源；同时改写「不变量」、SC-9 判据 3、CHANGELOG 的如实申报，并保留 Σlen² 门作为部分缓解。
  3. 无论选哪条，加对抗 SC（见 F-09）：`k × 8000 字符 token 行` 与 `2000 行短行` 两种形状，断言走了「只匹配规则」或时间文案，或者给出墙钟上限。
  4. 「B 时间护栏」在规格里不要再被描述成成本护栏，它只管「首遍已经很慢」。

#### F-02
- type: issue
- severity: **Critical**
- category: implementation
- scope: What Changes §3；Decision record 第 5 条；owner 姿态 D 的理由「它不参与任何代入」；`secret-guard.sh:645`、`:659`
- 验证方式: 实验（3.2 + 5.2）+ 读码（超集推演）
- 摘要: 「命令文本里有没有 `$NAME`/`${NAME}`」比 `_sg_vx_apply` 实际会代入的范围窄。`_sg_vx_apply` 按数组顺序在**演变中的副本**上逐个变量代入，前面变量的代入结果可以**拼出**后面变量的引用。超大值走 D 时，这种构造引用被放行，基线 VMAX 会拦。D 的前提「未被引用的值不参与任何代入」因此是错的。
- 证据:
  1. 机理读码: `:682-697` 对每个变量在当前 `s` 上跑 `\$NAME([^A-Za-z0-9_]|$)`，`s` 已含前面变量的代入结果。
  2. 反例（`exp7.sh`，bash 3.2.57 与 5.2.15 结果一致，端到端过 `hook-*.sh`）。命令形状 `P=cat; B='$'; C=A; A=<值>; eval $P $B$C`，文本里没有 `$A`：

     | A 的值 | 基线 | D 模拟（文本测试，`hook-D.sh`） |
     |---|---|---|
     | 短值（app.ini 路径） | rc=2，finding | rc=2，finding |
     | 超 4096（4222 字符） | rc=2，VMAX 尺寸文案 | **rc=0，放行** |
     | 超 4096，直接 `cat $A` | rc=2 | rc=2 |
     | 超 4096，完全不提 A（`echo $HOME`） | rc=2 | rc=0（D 本意） |
     | 超 4096，`cat ${A:-}` | rc=2 | rc=0（基线对**短值**的 `${A:-}` 也放行，所以这一形态不是新能力） |

  3. 真 shell 语义（`exp8.sh` + 手跑，两版 bash）: `P=echo; B='$'; C=A; A=hello; eval $P $B$C` 与惯用法 `eval "echo \$$C"` 都输出 `hello`，即这是真能展开 `$A` 的写法，不是 hook 的误读。
  4. for 列表同口径（`hook-D2.sh`）: `for f in <5000>; do echo $HOME; done` 基线拦、D2 放；`...; do echo $f; done` 两版都拦。
  5. 其余任务书列的情形（链式 / 花括号 / 前缀撞名 / 引号内 / heredoc 内）我读码推演，文本子串测试是 `apply` 直接触发条件的超集，所以**不会**漏: 链式（别的赋值的值里写了 `${NAME}`，文本里有）、`${NAME}` 与 `$NAME`、前缀撞名（`$NAMEX` 偏严）、单引号内（偏严）、heredoc 内（偏严）。`${NAME:-x}` / `${NAME%…}` 这些 apply 本来就不代入，不新增缺口。唯一的缺口就是「apply 自己造出来的引用」。
- 建议改法:
  1. 把「是否被引用」的判定放进 `_sg_vx_apply`，用 apply 自己的两个触发条件（`*"\${$n}"*` 与 `\$n([^A-Za-z0-9_]|$)`），这样范围与代入**逐字相同**。做法: 超大值不丢，登记成「墓碑」（名字进 `_SGV_N`，值留空，另用一个并行数组或哨兵标记）。apply 遍历到墓碑时只检查、不代入，命中就返回新状态（例如 3），`_sg_vx_pass` 照旧发 VMAX 文案。chaining 的 i×j 循环同样要对墓碑 j 检查 `V[i]` 里有没有 `${NAME_j}`/`$NAME_j`。
  2. 如果选墓碑法，`:666` 的 `[[ -z "${_SGV_V[j]}" ]] && continue` 就**不再是死代码**，§5「清理死代码」要同步改，别删。
  3. 如果坚持文本测试，则要把扫描范围写死: 整条命令（含赋值之前和之后，循环/函数里会先用后赋），用位置而不是文本搜索去掉「这条赋值本身」，并明确自引用（`PATH="$PATH:…"`）算不算被引用。同时必须接受并申报上面的构造引用缺口，不能再说「不新增 fail-open」。
  4. 加回归 SC（见 F-09）: 构造引用 + 超大值，新旧都拦；该 SC 在「文本测试」实现上必红。

#### F-03
- type: issue
- severity: **Critical**
- category: implementation
- scope: What Changes §4；`secret-guard.sh:654`（`rf`）
- 验证方式: 实验（3.2 + 5.2）
- 摘要: 单纯把换行排除出列表字符类，会把反斜杠续行的列表项丢掉。shell 里 `for f in a \⏎ b; do` 的列表是 `a b`；新正则只取到 `a \`。基线靠列表收集能拦的读取（路径放在续行上、读取在循环体里），新版放行。
- 证据:
  1. 端到端（`exp7.sh`，两版 bash 一致）: `for f in /etc/hostname \⏎ /etc/forgejo/app.ini; do cat "$f"; done`，基线 rc=2 finding，D+F 模拟 rc=0。单行写法两版都 rc=2。首遍放行（路径在读取之前，读取与路径不相邻），所以拦的是 W10 列表这一路，不是别处。
  2. 真 shell（`exp8.sh`，两版）: 续行列表三项全迭代。
  3. 正则层（`exp9.sh`，两版结果相同）: 三个版本对同一输入的列表捕获——基线 `[^;&|)]*` 是 `one \⏎ two \⏎ three`（对）；proposal 版 `[^;&|)<NL>]*` 是 `one \`（丢项）；续行感知版 `(([^;&|)\<NL>]|\\.)*)` 是完整三项，且线性（7.5 KB 的转义密集列表 10–12 ms）。
  4. 陷阱（`exp10.sh`，两版）: 在双引号正则串里写字面量 `\n`（两个字符）放进方括号，POSIX 括号表达式里它就是「反斜杠」和「n」两个成员，列表会在第一个字母 n 处截断（`for f in one two nine` 得到 `o`）。规格只写「字符类加入换行」，没说怎么放。
  5. 在正则里放真换行、3.2 与 5.2 都行: `local _nl=$'\n'`，再 `…([^;&|)${_nl}]*)`；或 `"…([^;&|)"$'\n'"]*)"`。`exp9.sh` / `hook-F.sh` 已在两版上跑通。F 想修的场景本身也确认能修好: `for f in a b⏎do⏎echo <5000> $f⏎done` 基线 VMAX 拦、F 放行（`exp8.sh`）。
- 建议改法:
  1. 采用续行感知的列表正则（见证据 3），并在规格里写明用 `$'\n'` 变量放换行，禁止写字面量 `\n`。
  2. 决定并写明：引号内跨行的列表项（`for f in "a⏎b"`）是否接受为新的已知缺口（它与基线已有的「引号内 `;` 截断」同族；用 `"[^"]*"` 分支可以一并改善，但要先量）。
  3. SC 见 F-09: 续行列表必须仍被拦（在 proposal 原样的 F 上必红）；含字母 `n` 与反斜杠的列表必须被判定。

### Major

#### F-04
- type: issue
- severity: Major
- category: implementation
- scope: What Changes §5「W9 扩展的整串检查维持原口径」；`secret-guard.sh:1553-1566`；SC-8；既有用例 21ap（`secret-guard.test.sh:2685-2693`）
- 验证方式: 实验（仅 5.2）+ 读码
- 摘要: §5 要保持「副本总长 > SMAX 即拦（扩展生效时）」，但 `:1554` 调的就是被改成增长口径的 `_sg_vx_apply`，`ar==2` 的含义随之改变。规格没写保持口径的机制；按字面「不改调用点」实现时，扩展对大副本重跑 `_sg_core_eval`，实测 10–16 KB 副本要 6.7–17 s，超 5 s 即 fail-open，而 SC-8 的「两版都拦」措辞照样能绿。
- 证据:
  1. 读码: `:1562-1565` 的 `elif [[ $ar -eq 2 && -n "$( _sg_ext_entries …)" ]]` 依赖「apply 返回 2 = 总长超 SMAX」。
  2. 口径变化（`exp23.sh`，5.2；`hook-G.sh` = 只把 apply 改成增长口径、调用点不动）。21ap 的夹具（扩展列出的路径经 `$f` 到达，副本 8193 字符，扩展生效）: 基线 rc=2、文案「too large for the project extension」；增长口径 rc=2，但文案变成扩展命中文案（look 被做了）。路径**不在**副本里、副本 > 8192: 基线 rc=2（size(ext)），增长口径 rc=0（look 做了、没有条目，这一支本身无害）。所以既有 21ap 会红，而 SC-8「两版都拦」按字面却可能全过。
  3. 真正的风险（`exp24.sh`，5.2）: 列出的路径只在代入之后才出现（`R=/srv/billing/; S=conf/prod.toml; … | cat $R$S`），分段模式形状，扩展生效。副本约 10 KB: 基线 1.9 s 按 W10 尺寸文案拦；增长口径 + 调用点不动，W10 放行大副本后，ext look 对它重跑 `_sg_core_eval`（含首遍 O(n²) 扫描器），**6.7 s** 才拦。副本约 16 KB: 基线 5.3 s、增长口径 **17.2 s**。都过了 5 s。这就是 proposal 自己说「长副本确实贵」的那一支；`_sg_over_budget` 只在 `_sg_core_eval` 开始**前**查一次（`:813`），挡不住它。
  4. bash 3.2 上 `exp23` 的夹具在本机被 C 的时间预算抢先（文案是 time），没有得到干净对比，**未核实**；`exp24` 只跑了 5.2。
- 建议改法:
  1. 给 `_sg_vx_apply` 加第二个可选参数（绝对总长上限）。默认走增长口径；`:1554` 显式传 `$_SGV_SMAX`，其余不变。这样 `ar==2` 在该调用点的含义、文案、`_SG_SUB` 不被改的约定都原样保留。
  2. SC-8 钉死两个形状，期望都是 rc=2 且文案是 `wpa_L_ext` 那一句，并在 5 s 内返回: （i）扩展生效、增长小（≤ GMAX）、副本总长 > 8192、**列出的路径不在副本里**（`exp23` 的 filler 2160 形状，调用点没改时是 rc=0）；（ii）列出的路径只在代入后出现（`exp24` 形状，调用点没改时 6.7–17 s）。并保留「无扩展时不拦」的对照（21ap 第三条）。
  3. 既有 21ap 要在清单里（见 F-10）。

#### F-05
- type: issue
- severity: Major
- category: implementation
- scope: What Changes §2「实现约束: 最长行的计算必须是线性的」
- 验证方式: 实验（3.2 + 5.2）；macOS `RE_DUP_MAX` 未核实
- 摘要: 规格要线性，没给算法。我量了四种自然写法，两种在 3.2 上直接超时，一种不可移植且慢到离谱，只有 `read` 循环合格。
- 证据（`exp6.sh` `exp6d.sh` `exp16.sh`，3.2.57 / 5.2.15）:

  | 算法 | 64 KB（10 行×6400） | 64 KB（1000 行×64） | 1 MB | 结论 |
  |---|---|---|---|---|
  | A. `while IFS= read -r l …; done <<< "$s"` | 57 ms / 92 ms | 79 ms / 106 ms | 5.2: 62–394 ms；3.2: 1.5–2.6 s | 线性，选它 |
  | B. 参数展开剥离 `${rest#*$'\n'}` | 395 ms / 701 ms | 1.8 s / **22.5 s** | 20000 行未跑完（> 80 s） | 平方级；头注释 `:575-576` 自己就警告过 `${s#*"$pat"}` |
  | C. `set -f; for t in $s`（token 循环） | 123 ms / 432 ms | 252 ms / 339 ms | 5.2: 1.8–2.7 s；3.2: 6.6–8.8 s | 线性但比 A 慢 2–5 倍，还要处理 glob 状态 |
  | D. 正则 `[^$'\n']{8193,}` | **14.0 s / 12.8 s** | 231 ms / 171 ms | — | 含长行时慢到不可用 |

  D 另有可移植问题: glibc `RE_DUP_MAX` = 32767（`getconf`），`{32768}` 时 `=~` 返回 2，在 `if` 里被当成「不匹配」，门会**静默**失效；BSD/macOS 的上限据我所知是 255，`{8193}` 会直接编译失败（**未在 macOS 实测**，POSIX 只保证 255）。
- 建议改法:
  1. 规格直接指定 read 循环，并写明: 按 `\n` 分行（与 `_sg_line_match` 同一套切法）、长度用 `${#l}`（字符，与其余长度口径一致）、末行无换行也要处理（`|| [[ -n "$l" ]]`）、遇到第一行 > LMAX 就可以退出。
  2. 同一遍里顺便把 F-01 需要的行数、Σlen² 一起算出来，不要再扫第二遍。
  3. 证据 W3 的最长行用的是 `awk length($0)`（`traffic/expline-traffic.sh`），与 `${#l}` 单位不一致（mawk 数字节、gawk 数字符）。实现好 helper 后用它重跑一遍 W3，别沿用旧数。
  4. 禁止 B 和 D 写进规格的任何示意。

#### F-06
- type: issue
- severity: Major
- category: architecture
- scope: What Changes §2 步骤 3「只匹配规则」；`secret-guard.sh:1497-1524`（`_sg_judge_one`）；`_sg_emit_blocked` 的 oversize 模板（`:851-867`）
- 验证方式: 实验（仅 5.2）+ 读码
- 摘要: 规格写「对 W12 中和后的副本逐条匹配」，但 W12 的中和代码在 `_sg_judge_one` 里（它在源码闸门之下，被 SC-8 按锚点抽取）。新 helper 如果复制一份，就多一对会漂移的拷贝；漏掉中和则没有任何 SC 会红。另外 oversize 模板的正文固定是「Nothing was matched」，对「命中了规则」这一支是错话。
- 证据:
  1. `exp19.sh`（5.2）: 不做 W12 的朴素规则循环对 `python3 -c "import os; print(os.environ[\"HOME\"])"` 和 `os.environ.get("HOME")` 各命中 1 条规则，而 `_sg_judge_one` 对这两条返回 0。大 Python 片段读单个环境键是常见写法，漏掉中和会批量误拦。
  2. SC-4 的两个用例都不涉及 `os.environ`，漏掉中和时全绿。
  3. 读码 `_sg_emit_blocked` 的 oversize 分支: 固定写「Nothing was matched. After variable expansion the command is bigger than the guard can check reliably」。命中规则那一支套用它，对用户是误导。
- 建议改法:
  1. 不复制。要么给 `_sg_judge_one` 加第三个参数（如 `rules`，跳过 credit、命中即发 oversize 类文案），要么把 W12 的四个 `while` 抽成闸门之上的 helper，两处共用。后者要同步 W14 的闭包检查（`secret-guard.test.sh:2928` 起）。
  2. 新增一个 `kind`（例如 `rulehit`）或改模板，使这一支不再说「Nothing was matched」。
  3. 加 SC: 单行 > 8192 且只含 `os.environ["X"]` 读取的副本放行；同形状含真规则命中的拦。

#### F-07
- type: issue
- severity: Major
- category: testing
- scope: What Changes §2 步骤 1；Decision record 第 3 条；SC-5；`secret-guard.sh:603-607`、`:617`
- 验证方式: 实验（3.2 + 5.2）+ 读码
- 摘要: 时间护栏直接读 `SECONDS` 的绝对值，有三个问题: 粒度比「一半预算」的说法粗、`SECONDS` 会从环境继承、SC-5 的进程内单测按规格写会漂。
- 证据:
  1. 粒度（`secs1.sh`，两版各 4 次，起始相位随机）: `SECONDS` 是「墙钟整数秒之差」，读到 ≥ 2 时真实已耗时落在 (1 s, 2 s]（3.2: 1233/1659/1634/1495 ms；5.2: 1655/1155/1845/1895 ms）。默认预算 3 与封顶 4 都是 `2*SECONDS >= b ⇔ SECONDS >= 2`（`secs3.sh` 的真值表），即触发概率从 1 s 的 0 线性爬到 2 s 的 1，「一半」只是均值。预算 1、2 时是 `SECONDS >= 1`，真实 0–1 s。
  2. 环境导入（两版）: `SECONDS=-100000 bash -c 'echo $SECONDS'` 输出 `-100000`，`SECONDS=7` 输出 7。所以「`SECONDS` 从 hook 进程启动开始计」只在环境里没有它时成立。绝对值读法可被继承值悄悄关掉（负值）或打成全拦（大正值）。C 用的是差值（`SECONDS - _SG_T0`），不受影响。
  3. SC-5 漂移: 直接 `SECONDS=k` 是按墙钟计的，赋值后 sleep 1.2 s 再读，3.2 读到 3、5.2 读到 2（`secs3.sh`），所以 `k=1,b=3`（应放行）这个关键边界会在秒边界翻成拦。`unset SECONDS; SECONDS=k` 则是确定的（两版都验证过，sleep 1.2 s 后仍读 1）。
  4. 进程内测试: 若有用例把 hook source 进长跑的套件 shell，`SECONDS` 就是套件已运行秒数，任何走到大副本的用例都会被误拦。既有 SC-21an 探针和 SC-8 重放都在新进程里跑（`bash "$wpa_vx_probe"`、`sc8_replay.sh`），所以现在没事；新增进程内用例必须沿用，或设 `_SG_P0`。
  5. 时钟语义: 头注释 `:603-606` 写 C 的时钟「measures THIS command's judgement (not wall time since the process started)」，B 恰好相反，两个时钟并存需要写清。
  6. helper 没起名。既有套件靠合约名（`_sg_vx_collect` 等）探测，SC-5 需要一个固定名字。
- 建议改法:
  1. 在 `:607` 旁新增 `_SG_P0=$SECONDS`（进程启动锚），护栏读 `SECONDS - _SG_P0`。对继承的 `SECONDS` 免疫，也让测试直接设 `_SG_P0`，不用动特殊变量。
  2. 起名并写进合约（如 `_sg_half_budget_spent`，返回 0 表示已过半）。SC-5 单测在**新进程**里设 `_SG_P0` 与 `_SG_TIME_BUDGET`，覆盖 `b = 0..4` × `k = 0..3` 的真值表，包含边界对 `(b=3,k=1)` 放行与 `(b=3,k=2)` 拦。
  3. 端到端确定性用例: `SECRET_GUARD_TIME_BUDGET_S=0` + 大而良性的副本 → 必为 time 文案（预算 0 时 `2*SECONDS>=0` 恒真）。这是 bf（基线是尺寸文案）。
  4. 规格里把「已经用掉一半预算」改成「`SECONDS` 整数比较，默认预算下对应已耗时 1–2 s」。

#### F-08
- type: issue
- severity: Major
- category: testing
- scope: SC-9 的三条判据；Impact「真实流量回放」；证据可复现性
- 验证方式: 读码 + 证据文件数据；3.2 占比是估算，未实跑
- 摘要: 判据既放过明显错的实现，也没覆盖 3.2，语料还易失。
- 证据:
  1. 判据 1 允许 `oversize → finding`。W1 说这 138 条完整判定全部 rc=0（`W-summary.txt`），所以 `oversize → finding` 的期望是 **0**。一个「大副本一律只匹配规则」的坏实现会把那 31 条今天靠 credit 放行的（W2）都变成 finding，恰好落在被允许的转移里，判据 1 和 2 都过。
  2. 判据 2「≤ 5，目标 0」: 对 138 条，期望的非放行只可能来自 time 护栏，并且每一条应有已耗时 ≥ 1 s 的记录。`≤ 5` 太松。
  3. 平台: E12 是 bash 5.2。那 138 条在基线下的 hook 总耗时 mean 0.39 s、max 1.15 s、≥ 1.0 s 有 4 条、≥ 0.7 s 有 12 条（`E12-base-all.tsv` 的 seconds 列）。3.2 上首遍到判定前的耗时约为 5.2 的 2.7 倍（我的 k=5 样例 1.63 s / 0.59 s），则约 10–12 条会稳定过 2 s（护栏必拦），加上爬坡区，估计有 10–20 条（7–14%）变成 time，判据 2 会红。这是**估算**，语料拿不到、未实跑。
  4. 判据 3「没有任何命令新变成超过 5 s」只能约束语料里的良性命令，看不见 F-01 那类对抗形状（需要独立的对抗 SC）。
  5. 可复现性: 回放脚本的语料目录默认 `TRAFFIC_DIR=/tmp/r1traffic`（`traffic/w10-traffic.sh:6`），易失；「同一批语料」只能靠 W1 的 crc 列对，规格没要求核。语料来自会话记录，随记录清理而变（本机保留期**未核实**）。
- 建议改法:
  1. 判据 1 改成封闭且带计数: 对 W1 那 138 条，`oversize → allow` 为 138 减去有记录的 time 转移；`oversize → finding` 必须为 0，非 0 即回归；`oversize → 超长单行` 为 0（W3 没有超过 8192 的行）。
  2. 判据 2 按平台分别给期望: 5.2 上 time 转移每条附已耗时；3.2 上另跑一遍并如实记录占比（别拿 ≤ 5 去卡 3.2）。
  3. SC-9 结果文件记录: 新 hook 的 SHA、语料 crc 清单的哈希、bash 版本、逐行转移矩阵。语料放到 `/tmp` 之外并留清单。
  4. 判据 3 保留，另写 F-09 的对抗 SC。

#### F-09
- type: issue
- severity: Major
- category: testing
- scope: SC-1 … SC-8 的夹具说明；缺失的 SC
- 验证方式: 实验（`exp22` 仅 5.2；`exp15` 两版）+ 读码
- 摘要: 几条 SC 在基线上并不红，或者区分不了好坏实现；若干该有的回归没有。
- 证据与建议（逐条）:
  1. **SC-6 不是 bf**（`exp22.sh`，5.2）: `A=<5000>; echo hi` 基线 rc=0，因为 collect 入口有「命令里没有 `$` 就直接返回」的闸（`:637`，21ad 末条也在钉它）。要 bf，夹具须带另一个 `$`（如 `echo $HOME`），此时基线 rc=2、D 模拟 rc=0。
  2. **SC-7 的回归侧**: 单行 for 列表 > 4096 的两版都拦只在循环体**引用 `$f`** 时成立。体里不引用，D 之后新版放行；体里没有 `$` 则基线也放行。必须写明夹具含 `$f`。bf 侧夹具必须是「`do` 在下一行」的形态（`exp8.sh`: 基线 VMAX 拦、F 放行）；`for f in a b; do …` 这种分号形态基线本来就放行，不是 bf。
  3. **缺「完整判定含 credit」的正证**: 没有任何 SC 要求「副本 > 8192、所有行 ≤ 8192、命中规则但带 `| wc -l`」被放行。「大副本一律只匹配规则」的坏实现过得了 SC-1..SC-8，也过得了 SC-9（见 F-08）。要加。
  4. **缺边界对**: 本套件的惯例是两侧钉到字符（21aa/ab、21ac/ad）。增长恰为 8192 放行 / 8193 拒（`exp15.sh` 验证了 `>` 语义：8192 放行，8196 拒）；LMAX 恰 8192 走完整判定 / 8193 走只匹配规则。
  5. **缺 `Limit hit:` 文案**: 既有测试逐字比较限制文案（`wpa_L_*`，`:2528-2532`）。规格只说「增长原因串」「超长单行原因串」，没给字面值，执笔席各自造，测试没法钉。要定稿增长（整串/分段各一）、超长单行、时间的字面值。
  6. **缺 F-02 / F-03 / F-04 的回归**: 构造引用 + 超大值；续行列表；扩展生效时增长小的大副本（见各条）。
  7. **缺对抗成本 SC**: F-01 两种形状。
  8. **缺分段模式的孪生**: 证据 W1 的 137 条全是整串模式，SC-1..SC-4 若只写整串，分段模式的大副本路径（逐段护栏、`spent` 累计）没有任何覆盖。每条加一个分段孪生（21aa 与 21ao 的做法）。
  9. **SC-2** 要求各行 ≤ 8192，否则走的是只匹配规则那支，证明不了「第二遍真的完整判了大副本」。
  10. SC-3 的「4000 字符的值引用 3 次」增长 11994 > 8192，bf 成立（基线按总长拦），但区分靠文案，所以依赖第 5 点。

#### F-10
- type: issue
- severity: Major
- category: testing
- scope: SC-11「现有套件的全部 BLOCK 用例判定不变，除了本 change 点名的尺寸类用例（逐条列出）」
- 验证方式: 读码推演，未实跑套件
- 摘要: SC-11 要求逐条列出，规格没列。我按读码推演列一份，必须由执笔席在 B.1 基线红之后核实（**我没有实跑套件**）。
- 证据（`aria/hooks/tests/secret-guard.test.sh`）:

  | 用例 | 行 | 预期变化 | 原因 |
  |---|---|---|---|
  | 21ab | 2552-2555 | 3 条断言中 1 条文案变（8193 副本仍被拦但走「超长单行」文案），2 条由拦变放（9000 字符段 + 1 字符值；4500×` a`） | 增长 ≈ 0；单行 > LMAX 走只匹配规则，无命中 |
  | 21ac 第 3 条 | 2566 | 文案变 | 4096 字符 for 列表，增长约 4090，副本约 8200，单行走只匹配规则，仍拦但文案不再是 `wpa_L_whole` |
  | 21ad 第 2 条 | 2569 | 由拦变放 | `f=<4097>; echo $HOME`，D 放宽；这正是 `:2559-2562` 写明「narrowing is the owner's call」的那一条 |
  | 21ag | 2586 | 文案变 | 增长 35640 > GMAX，仍拦，但不再是「segment is longer than 8192」 |
  | 21aj | 2605 | 文案变 | 三次 4000 字符引用，增长 11994，同上 |
  | 21al | 2633-2635 | 文案变 | 8193 的花括号整串副本，增长约 5400，单行 > LMAX，只匹配规则 |
  | 21an | 2644-2677 | 断言需重写 | `edge8193` 期望 apply 返回 2，且 `[[ $rc -eq 0 && ${#_SG_SUB} -gt 8192 ]]` 视为失败，都不再成立 |
  | 21ao | 2682 | 文案变 | 同 21al |
  | 21ap | 2691 | 取决于 F-04 的实现 | 扩展口径若不保持，文案变 |
  | `wpa_L_seg/whole/total/ext` | 2528-2532 | 字面值更新 | 增长口径的文案 |

  不变: 21aa、21ae、21af、21ah、21ai、21ak、21am（边界或口径未动）。
- 建议改法: 把上表（核实后）放进 proposal 或 detailed-tasks，作为 SC-11 的「点名用例」；`:2512-2517`、`:2559-2562` 的头注释同步（引用 2026-10-21 裁定）。

#### F-11
- type: decision
- severity: Major
- category: architecture
- scope: F-01 的处置姿态
- 验证方式: 无（决策项）
- 摘要: F-01 不是单靠技术就能收口的，需要 owner 在三条里定一条: 加门（部分封住）、先做 #228 的 credit 根治、或明确申报残余。这是安全 fail-open/closed 的姿态，不是纯技术裁定（memory `failopen-posture-owner`）。
- 证据: 见 F-01 证据 5、6；F-01 建议 2 的 (a)(b)(c)。
- 建议改法: 主控向 owner 提这一个问题，附上选项和成本: (a) 工作量最小，但对包装词密集的文本封不住；(b) 最彻底，要等 #228 的 r2c/r2f，#217 被推迟；(c) 零实现成本，要如实申报，并改写不变量。

### Minor

#### F-12
- type: issue
- severity: Minor
- category: implementation
- scope: What Changes §1；`secret-guard.sh:677-700`；TMAX 的「同一口径」
- 验证方式: 实验（3.2 + 5.2，`exp15`）+ 读码
- 摘要: 增长上限的几个实现细节需要写死。
- 证据与建议:
  1. `lim` 必须在函数入口用 `${#1}` 一次算出。`_sg_vx_apply` 里的 `s` 在循环中被改写（`:691` 把 `s` 换成余串），写成 `${#s}+GMAX` 会错。规格里的 `S` 是入参，不是循环里的 `s`。我的模拟实现是 `local lim=$(( ${#1} + _SGV_GMAX ))`，把它作为 MAX 传给 `:685` 的 `_sg_vx_replace`，并替换 `:694` 的比较；`exp15.sh` 两版 bash 的边界、花括号形、缩水为负增长（−1）都验证过。
  2. 「增长」应写成「任一中间副本长度 > `lim`」，因为边构建边比较，值比引用短时中间长度不单调。
  3. 「整串模式与分段模式同一口径」只对 GMAX 成立。分段模式的 TMAX 仍按**完整副本长度**累计（`:743-747`），> 64 KB 的分段模式命令即使增长很小也仍被拦。证据 W1 的 137 条全是整串模式，这块没量过。要么声明残余，要么说明 TMAX 也改成按增长累计（那就要改数值含义）。
  4. 新的增长拒绝文案不能再写「longer than 8192 characters」（见 F-09 第 5 点）。

#### F-13
- type: issue
- severity: Minor
- category: documentation
- scope: proposal 措辞
- 验证方式: 读码 / 读 proposal
- 摘要: 以下措辞有两种读法，执笔席会选错。
- 清单:
  1. §4「字符类加入换行」: 是加入「排除集」。配合 F-03 的字面量 `\n` 陷阱，必须写成「在排除集里加入真换行字符」。
  2. §2 步骤 1「已经用掉一半预算」: 见 F-07，整数比较，对应 1–2 s。
  3. §2 步骤 2「最长行 ≤ LMAX」: 含等号；单位是 `${#l}` 字符；按 `\n` 分行。
  4. §3「命令里（去掉这条赋值本身）」: 扫描范围（整条命令，不是余串）和去除方式（按位置）没说，见 F-02。
  5. §2 步骤 3 的原因串「…不评估脱敏过滤」与 oversize 模板的「Nothing was matched」矛盾，见 F-06。
  6. SC-1「300 个短变量引用」: `_sg_vx_apply` 对每个变量最多代 8 次 `$NAME` 加 8 次 `${NAME}`（`:624`、`:687`），赋值最多 16 个，300 次引用不可能都被代入。这条夹具考的是尺寸，不是引用数，写清楚。
  7. 「不变量」第 1 条: 在 F-01、F-02、F-03、F-15 都有反例或补充，至少要改成「相对基线，仅在以下已申报的情形放宽: …」。
- 建议改法: 逐条按清单改写；其中 1、3、4 要给出字面写法（真换行用 `$'\n'` 变量、`${#l}` 字符、按位置去掉赋值本身），因为这三处就是执笔席最容易走偏的地方。

#### F-14
- type: issue
- severity: Minor
- category: documentation
- scope: 同步面
- 验证方式: 读码 / 读文件（`ls`、`grep` 核对过）
- 摘要: 同步面清单需要补全。
- 清单:
  1. `secret-guard.sh:577-590` 头注释: 不要把「逐行成本」立论写进去（F-01）；写清三个新常量、分流顺序、两个时钟。
  2. `:603-606`: C 的头注释说时钟度量「this command's judgement」，要补上 B 的进程锚（F-07）。
  3. `secret-guard.test.sh:2512-2517`（「The numbers are part of the contract」）、`:2559-2562`（D 的姿态注释）要引用 2026-10-21 裁定。
  4. proposal 第 3 行和 Tasks 段都引用 `detailed-tasks.yaml`，但变更目录里只有 `proposal.md`（`ls` 核对过），引用悬空。
  5. 若采用 F-02 的墓碑法: `:666` 不再是死代码，§5 的「清理死代码」要同步撤掉。
  6. 兄弟规格 `secret-guard-scan-cost-and-firstpass-cap/proposal.md:103` 写「不改 `_SGV_*` 语义」，而 #217 要改。该规格 `:50` 对 credit 成本的刻画（「仅单个长 token」）与 F-01 的实测不符。两边加互相引用的更正注记，避免 #228 重启时按旧模型设计。
  7. standards 的 `secret-hygiene.md:316` 计数陈旧一条，我只核对到该行确实写「822 / 816」；是否陈旧**未核实**。
- 建议改法: 把上面七项并入 Impact 的同步面清单，并在 B.1 入场时逐项勾；第 6 项两份规格同日互相加注。

#### F-15
- type: risk
- severity: Minor
- category: architecture
- scope: owner 姿态 A；「不变量」的「被放行的大副本都经过完整判定」
- 验证方式: 实验（仅 5.2，`exp20`）
- 摘要: 对整串模式的大副本，「完整判定」里的 credit 是对整份副本一次性给的，任何一处无关的 `>/dev/null` 都给全部命中记功。这是 A 的固有含义（不重新争论），但「不变量」读起来像是大副本有更强的保护。
- 证据: `exp20.sh`（5.2）: 11 KB 整串脚本，变量间接读取在末尾。脚本里没有任何过滤器: 基线尺寸拦，A 模拟 finding 拦。加一行无关的 `make >/dev/null`: 基线仍尺寸拦，A 模拟 **rc=0 放行**；同样内容压到 < 8192，基线本来就放行。W2 的 31 条「今天靠 credit 放行」也是同一机理。
- 建议改法: 在「不变量」里如实写一句: 大副本放行的判据与首遍整串模式的 credit 语义相同，不是更强。

#### F-16
- type: risk
- severity: Minor
- category: testing
- scope: 证据方法
- 验证方式: 读证据脚本与数据文件
- 摘要: 证据本身的几个方法差异，不影响结论但会影响复现。
- 清单:
  1. W3 最长行用 awk `length`（单位与 `${#l}` 不同，见 F-05）。
  2. `w10-traffic.sh` 的「是否被引用」只对 for 列表现算，赋值那 1 条靠 `assign-probe.py`，两者都是文本测试，与 D 的定义一致，但与 apply 的可达范围不是一回事（F-02）。
  3. W1 的 `judge_s` 是在抬高预算后单独计时 `_sg_judge_one`，不含 collect/apply/首遍，也不含 B 护栏，所以「平均 0.19 s」不能直接当作新版整体耗时。
  4. 所有数字都是 Linux + bash 5.2，Windows 与 macOS 的外推（×2.6、3.2 ×4）是借用 E12 和 #219 的，没有为 #217 重测。
- 建议改法: 重跑 W3（用实现后的 helper）；SC-9 结果留痕（F-08 建议 3）；把外推数标成「借用，未重测」。

## SC 逐条可测性判定

| SC | 能写成会红的测试吗 | 能区分好坏实现吗 | 备注 |
|---|---|---|---|
| SC-1 | 能（基线尺寸拦，`exp2`/`exp14` 类夹具） | 不能区分「大副本一律只匹配规则」 | 要补 F-09-3；要写明各行是否 ≤ 8192 |
| SC-2 | 能，靠文案区分 | 夹具各行必须 ≤ 8192，否则证明不了完整判定 | 依赖 F-09-5 的字面值 |
| SC-3 | 能，靠文案区分 | 要有 8192/8193 边界对 | 同上 |
| SC-4 | 能 | 缺「≤ LMAX 且带 credit 命中 → 放行」的对照；缺 W12 用例 | F-06、F-09-3 |
| SC-5 | 按现写法**不能稳定** | — | F-07 |
| SC-6 | **不能**，缺 `$` 时基线也放行 | — | F-09-1（`exp22.sh`） |
| SC-7 | bf 侧要 `do` 换行形态才红；回归侧要引用 `$f` | 区分不了续行丢项 | F-03、F-09-2 |
| SC-8 | 按现写法放不住口径 | 区分不了「调用点没改」 | F-04 |
| SC-9 | 能跑，判据偏松 | 区分不了「一律只匹配规则」 | F-08 |
| SC-10 | 能 | — | 新增 SC 都要在新进程里跑 3.2 |
| SC-11 | 能，但清单未列 | — | F-10 |

## 代码事实核对（proposal 断言 vs 源码）

| 断言 | 结论 | 证据 |
|---|---|---|
| SMAX 数的是总长，整串模式≈整条命令 | 成立 | `:685`、`:694`；头注释 `:587-588` |
| `_sg_compute_credit` 逐行，`:476` 是唯一整段匹配 | **部分成立**: `:476` 确是唯一的 `=~`（两个，`||` 连接）；但「通配段不跨空白、成本受 token 约束」对 `_SG_PS_REMOTE_T` 不成立，且还有逐行固定成本 | `:446`、`:476`、`exp12/13` |
| `_SG_T0` 在首遍之后才重置 | 成立 | `:1539-1542`、`:633` |
| `SECONDS` 从进程启动计、hook 里没有给它赋值 | **部分成立**: 确无赋值（`:607 :617 :633 :1542` 全是读），但环境里的 `SECONDS` 会被导入 | `grep`、`exp: SECONDS=-100000 bash -c …` |
| 扩展检查会重跑 `_sg_core_eval` | 成立，且只在条目出现时 | `:809-817`、`:811-813` |
| `:666` 死代码 | 成立（基线下） | 值入表前已跳过空值，chain 替换不会把非空变空 |
| 头注释对 SMAX 的立论引文 | 准确 | `:586-587` |
| Why 表里 W1–W3 的数字 | 与 W-summary 一致（2+60+64+10+1=137；0.194/0.97；31 条；566/4457/2139） | `W-summary.txt` |
| hook 的 5 s 超时 | 有配置 | `aria/hooks/hooks.json:32-33` |
| 「W10 预算数值在 standards 和 README 里没有写」 | 成立（`grep 8192` 只命中 hook 与测试） | — |
| 「本机所有项目都没有启用扩展」 | **未核实** | — |

## Verdict

**FAIL**

计算: Critical 3（F-01、F-02、F-03）、Major 8（F-04 … F-11）、Minor 5（F-12 … F-16）。≥1 条 Critical 即 FAIL。

说明两点，供主控判断:

1. F-01 的 Critical 评级按任务书的严重度表（新的 fail-open）给出。降级的条件是 owner 在 F-11 里选 (c)，把残余如实申报进规格，此时 F-01 可降为 Major 的文档修正。F-02 同理: 对刻意的攻击者，`${A:-}` 这类写法在基线对短值就放行，构造引用只多出「超大值 + 构造引用」这一窄类，但这是 owner 姿态 D 的理由写错了，规格没有申报。F-03 没有这个缓冲，续行列表是 W10 声称覆盖的范围。
2. 三条 Critical 的修法都不大，且都已在模拟副本上验证过可行（F-03 的续行正则、F-02 的墓碑法思路、F-01 的 read 循环）；F-01 的真正难点是 F-11 那个姿态选择。

## 轮次记录

- R1，convergence 模式，席位 backend-architect。
- 本席工作: 读任务书与 proposal；对照源码核对每条代码断言；写二十多个小实验（含 3 个补丁副本的构造脚本），覆盖 bash 3.2.57 与 5.2.15；读了 `secret-guard.test.sh` 的 SC-21 族、SC-T 族、W14 闭包检查的相关段、`hooks.json`、证据目录、兄弟规格 #228 的成本段。
- 资源纪律: 所有实验 `taskset -c 0,1 nice -n 19`，单个 ≤ 约 1 分钟（`exp6` 的三个形状合计超时被 `timeout 100` 截断，已在 F-05 里按「未跑完」处理）。
- 没做的事: 没跑全套件；没有 macOS / Windows 环境；没有真实语料（有意）；没读其他席位报告；没改任何仓内文件。
- 上一轮遗留: 无（第 1 轮）。

## 附: 实验索引

脚本目录: `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217audit/backend-architect/`

| 文件 | 内容 |
|---|---|
| `h.sh` | 采用与 SC-8 / 30b 相同的锚点抽取（`risky_patterns`、`_sg_judge_one`、`_sg_per_segment_eval`）的进程内 harness |
| `mkpatched.py` `mkG.py` `mkB.py` | 生成模拟副本: `hook-D.sh`（D 文本测试）、`hook-D2.sh`（+for 列表）、`hook-F.sh`、`hook-DF.sh`、`hook-G.sh`（增长口径 apply）、`hook-AB.sh`（A+B）、`hook-nosmax.sh`（只抬高 SMAX） |
| `secs1.sh` `secs2.sh` `secs3.sh` | `SECONDS` 粒度、子 shell、`unset SECONDS` 桩、真值表 |
| `exp2.sh` `exp4.sh` `exp14.sh` `exp17.sh` `exp18.sh` | F-01 的端到端、分解、短行形状、A+B 模拟、基线字面读取对照 |
| `exp5.sh` `exp11.sh` `exp12.sh` `exp13.sh` `exp21.sh` | credit 的 xtrace 分解、包装词/行数/总长 的成本曲线 |
| `exp6.sh` `exp6d.sh` `exp16.sh` | 最长行算法与 `RE_DUP_MAX` |
| `exp7.sh` `exp8.sh` `exp22.sh` | D 与 F 的端到端、真 shell 语义、SC-6/7 的 bf 条件 |
| `exp9.sh` `exp10.sh` | for 列表正则变体与字面量 `\n` 陷阱 |
| `exp15.sh` | 增长上限边界 |
| `exp19.sh` `exp20.sh` `exp23.sh` `exp24.sh` | W12、credit 语义、扩展口径（口径变化 / 大副本上 ext look 的耗时） |

---
agent: code-reviewer
round: R3
verdict: REVISE
critical_count: 0
major_count: 4
minor_count: 5
r2_resolved: 8/9
---

# post_spec R3 — secret-guard-per-segment-evaluation (code-reviewer 视角)

审计对象: `/home/dev/Aria/openspec/changes/secret-guard-per-segment-evaluation/proposal.md` (**v3 fail-safe 降级**版)
参照物: canonical `aria/hooks/secret-guard.sh` @ `af87cae` (698 行) / `aria/hooks/tests/secret-guard.test.sh` (798 行) / R1 五份 + R2 五份审计报告原文 / 主仓 `5fab5b8`
方法: **全语料 v3 设计模拟** (自写 quote-aware `safe_to_split()` + `split_top()`, 对 305 条语料逐条 canonical 直调求 before/after, 共 ~360 次 hook 调用) + 所有数字机械重算 + R1/R2 报告逐条对照。**未修改仓库任何文件** (脚本在 scratchpad)。
验收环境遵守: 全部行为证据来自 `bash aria/hooks/secret-guard.sh` 直调; **未**使用仓内 harness hook 链 (cache 仍 = 1.63.0)。

---

## Phase 1: 规范合规性

**判定**: PASS (可进入 Phase 2)

- Level 2 结构完整: Why / What(§1-§5 + Key Deliverables) / 关键决策(8 行) / Impact / 转出(7) / rule6_note / Tasks(1.1-1.9) / SC(1-13)。
- Rule #6 框定不变 (deterministic detector hook → structural substitute), substitute 从 R2 的 4 项扩为 SC-1/SC-5/**SC-6**/SC-2/SC-3, 与新机制对齐。
- Rule #1/#5 满足。转出七项与「本版不做」的范围声明一一对应, 无越界实现。
- 缩范围→再设计的迭代记录 (三版表) 与实际内容一致, 无 scope creep。

---

## Phase 2: 事实准确性 / 验收有效性

### 一、R2 我方 1C+3M+5m 的核销 (8/9)

| R2 编号 | 本版处置 | 核销结论 |
|---------|---------|---------|
| **C-1** 块结构假阳性 + 语料零覆盖 + 无 KNOWN-LIMIT 锁 | 改为 fail-safe 降级 (§1) + SC-6 十二条族 | **解决 (超预期)** — 见下方「优点 1」。假阳性类**从设计上消失**而非补锁; 且我 R2 的「语料零覆盖」本轮被我自己推翻 (见「自我勘正」) |
| **M-1** 迁移表/SC-3 仍写 68/52 | 全文改 65/49, 并列 16/15/1 + 5 | **解决** — 本轮以 quote/转义-aware 分段器独立重算: 65/49/16/15/1 + 5 (4 拦 1 放), 逐个吻合 |
| **M-2** SC-2 对误切换行零检出力 | SC-2 改为纯「零影响回归锁」, 不再声称「这 20 条即红」; 换行机制锚由 SC-5 (`换行→1`) 承担 | **解决 (改述式)** — 虚假保护的措辞已删, 举证责任已移交, 与我 R2 修法同向 |
| **M-3** 决策表 `$()` 行零 SC + 「不解析 vs 整体留段内」互斥 | `$()` / 反引号 / heredoc 归入块字符 → fail-safe 降级; 「不解析」措辞消失; SC-6 含反引号 / `$()` / heredoc 三条 | **解决** — 二义措辞随设计换代一并消除 |
| **m-1** 「相邻差 92%」口径不准 | 决策表性能行整体重写, 全文已无「相邻差 92%」 | **解决 (删除式)** |
| **m-2** ~294ms 未复现 | 全文已无 294 | **解决 (删除式)** |
| **m-3** `guard:ack` 无锁 | 新增 **SC-12** + 决策表末行点名 | **解决** — 且实测有真检出力 (见「优点 4」) |
| **m-4** Tasks↔SC 追溯断开, SC-9 无承载 | Task 1.5 增「端到端族」可承载 SC-9; Task 1.7 ↔ 新增 SC-13 | **部分** — SC-9 有归属了, 但 Task 1.4 (`corpus_census.py`) 仍无任何 SC → 见 **M-4** |
| **m-5** 与 comment 17545 的 13 vs 15 差异未标注 | 13/15 之争整段不再出现 (改用「4 条真泄漏由 2 翻 0」作理由) | **解决 (删除式, 争议源已移除)** |

**无静默丢弃项** — 9 条全部可追溯。

### 二、自我勘正 (推翻我 R2 的一处断言)

R2 C-1 我写「实测语料中 `{ …; } >/dev/null` / `for…done >/dev/null` 类用例 = **0 条** (机械 grep 确认)」。本轮以插桩 dump + 结构化扫描复核: 语料实有 **11 条**块结构用例走 fallback 路径 —

`find … -exec cat {} \;` / `cat <<EOF…` (heredoc) / `x=$(env)` / `echo $(printenv KEY)` / `` x=`env` `` / `{ env; }` / `{ printenv; }` / `xargs -I{} ./do env` / `if :; then env; fi` / `while :; do printenv; done` / `if x; then y; else env; fi`

我 R2 的 grep 形状 (`{ …; } >/dev/null` 带尾重定向) 过窄, 属 memory `feedback_grep_window_truncation_breeds_false_corpus_evidence` 的同类。**但 spec 三版表 v2 行的「语料零覆盖」措辞仍然准确** —— 它指的是**误报方向**: 语料中 `want=0` 的块结构用例只有 1 条 (`xargs -I{} ./do env`), 且不带尾部 credit, 在 v2 规则下切开后仍 exit=0 ⇒ 全部回归 SC 在误报类上确实恒绿。作者的表述比我 R2 的更精确。

### 三、全文数字与引用终检 (逐项机械重算)

| 断言 | 核实方式 | 结论 |
|------|---------|------|
| **141** pattern | 数组 `:402`(`declare`) — `:656`(`)`), 计 `^\s*['"]` 起始行 = **141** (139 单引号 + `:506/:507` 两条双引号 ssh) | ✅ |
| **305** 条 `bash_case` | `grep -c '^bash_case '` = **305** (含函数定义的 `grep -c bash_case` = 306) | ✅ |
| **65 / 49 / 16 / 15 / 1 + 5** | quote+转义-aware 扫描 305 条 dump: 含顶层 `;&&\|\|\|` = **65**; want=2 = **49**; want=0 = **16**; 仅 `\|` 的 want=0 = **15**; 含真边界的 want=0 = **1** (`put: KNOWN-LIMIT compound credit leak`); NL-only = **5** (4 拦 + `#152 FP: multiline benign` 放行) | ✅ 逐个吻合 |
| **12** 条把 `\|` 编码进正则 | 141 条中含字面 `\|` 者 = **12** | ✅ |
| **13** 处 subprocess | `:318-:401` 区 `grep -qE` = **13** | ✅ |
| **81** 条 `[^\|]*` (转出 1) | 含 `[^\|]` 任意形态 = **81**; 但**严格含 `[^\|]*` 者 = 79** (另 2 条是 `[^\|]+`: `kubectl get secret[^\|]+-o` / `redis-cli GET [^\|]+(secret\|…)`) | ⚠️ 见 **m-2** 之外的口径提示 (数值 81 对「工作面」而言正确, 记号写 `[^\|]*` 略窄) |
| **1** 条 `.*` (转出 1) | `'set[[:space:]]+-o[[:space:]]+posix.*set[[:space:]]*\|[[:space:]]*grep'` 唯一 | ✅ |
| **`:663`** 全局开关 | `sed -n 663p` = `if [[ $has_filter -eq 0 ]]` | ✅ |
| **366 / 360** | 实跑 canonical 套件 = `PASS: 366 / 366`; `zsh_case` 6 条 (`:714-:719`) 由 `command -v zsh` 门控, 本机 `/usr/bin/zsh` 在场 ⇒ 无 zsh = 360 | ✅ |
| SC-11「其余 5 脚本」 | `hooks/tests/` 内 6 个 `*.test.sh` 减本体 = 5 (`jq-crlf-guard.sh` 是库) | ✅ |
| v1.65.5 → **v1.65.6** PATCH | `aria/.claude-plugin/plugin.json` = `1.65.5` | ✅ |
| 主仓 **5fab5b8** | `git show` = "chore(hooks): 移除 .claude/scripts 本地 hook 副本, 统一由 plugin 接管 (owner 裁定)"; 主仓 HEAD 即此 commit | ✅ |
| **Aria#172** / **17512** / **17545** | R2 已经 forgejo API 逐条取回核对; 本轮仓内状态无变化 (cache 仍 1.63.0) | ✅ (沿用 R2 结论) |
| 「R2 backend 实测 2 段 CPU +85~92%」 | R2 backend 报告 `:54` 「3 轮一致 +85% / +90% / +92%」 | ✅ 逐字属实 |
| 性能表 **146→28 / 158→22 / 191→71** | 作者单次点测, 无法复核原值; **内部算术不自洽** → 见 **m-1** |
| SC-1 五形态改前 exit=0 | canonical 直调 5/5 = **0**; 按 v3 规则切分后各含一段 = **2** | ✅ baseline-failing 前提成立 |
| 转出 2/3/4/5 复现命令 | 逐条直调: `for f in a b; do cat /opt/.env; done >/dev/null` = 0 / `( cat /opt/.env; echo x ) >/dev/null` = 0 / `ssh h 'cat /opt/.env; true >/dev/null'` = 0 / `cat /opt/.env &>/dev/null` = 0 / `` x=`cat /opt/.env; true >/dev/null` `` = 0 | ✅ **5/5 属实且自包含** |
| SC-7 现状 | `set -o posix; set \| grep foo` 整条 = **2**, 两段分别 = 0 / 0 | ✅ fail-open 锁的前提成立 |
| SC-4 锚点 | `python3 -c 'import os; print(open("/opt/.env").read())'` = **2** | ✅ |
| `\|\|` 一字符绕过论证 | `nomad var put p1 @f1 >/dev/null \|\| nomad var put p2 @f2` 整条 = **0**, 切后段 2 = **2** | ✅ 论证成立 |

### 四、「三版表」与「7 条被推翻断言」逐条对照 R1/R2 原文

| 断言 | 出处核实 | 结论 |
|------|---------|------|
| (1) `&` 可作切分记号 | R1 code-reviewer C-1 (`&` 与 `&>` `>&` `\|&` `2>&1` 冲突, 打红 2 条合法 credit) | ✅ |
| (2)「保守不切 = 不会少拦」方向反 | R1 code-reviewer C-1 第 2 层 | ✅ |
| (3)「切错 = 安全回归」 | R1 code-reviewer M-2 (R2 已记「R1 实测证伪」) | ✅ |
| (4)「pattern 匹配已全是 bash 内建」 | R1 backend CRITICAL-1: `:342-399` 13 处 `echo\|grep -qE`, O3 只覆盖 `risky_patterns` | ✅ |
| (5)「60ms 固定成本是 bash 启动」实为 `jq` 58ms | R1 code-reviewer `:121`: `bash -c true` = 2ms, `jq -n .` = 58ms | ✅ 逐字属实 |
| (6) R1→R2 重写把已核实的 141 改成 139 | R2 qa `:44` 列为三次数字错误之一 (「141→139 回退」) | ✅ |
| (7)「只切 `;` `&&` = 最小可靠子集」不可靠 | R2 tech-lead **R2-C-2**「5/5 安全写法翻红, 无告知、无迁移指引、语料结构上抓不到」 | ✅ |
| 三版表 v1 行 (`&` 冲突 / 换行切碎 heredoc / 三子问题未预见) | R1 CR C-1 + R1 backend `:42` + R1 tech-lead M-2/M-3 | ✅ |
| 三版表 v2 行 (5/5 误报 + 语料零覆盖 ⇒ 回归 SC 恒绿是假绿) | R1 tech-lead M-2「5/5 实测翻红, 语料零覆盖」+ R2 tech-lead R2-C-2 + 我 R2 C-1 (3/3 复现) | ✅ (口径见上「自我勘正」) |
| 「无一由作者自查发现」 | 与 R2 qa `:44` 表述一致 | ✅ |

**结论: 三版表与 7 条自陈全部经原文核实属实, 无夸大、无张冠李戴。**

---

## 优点

1. **fail-safe 降级是本 cycle 最正确的一次方向转弯, 而且经得起全语料检验。** 我按 §1+§2 规则实现了 `safe_to_split()` + `split_top()`, 对全部 **305 条语料**逐条模拟 (fallback 走整命令直调; 可切者逐段直调取 max):

   | 指标 | 结果 |
   |------|------|
   | 305 条中 mode 分布 | 单段 281 / **SPLIT 13** / **FALLBACK 11** |
   | before ≠ want | **0** (语料现全绿) |
   | after ≠ before | **1** —— 且正是刻意要转正的 `put: KNOWN-LIMIT compound credit leak` (0→2) |
   | want=2 出现回归 (转 0) | **0 条** |
   | 非预期新假阳性 | **0 条** |

   即: v2 的 5/5 误伤类在 v3 下**归零**, 而 SC-3 (49 条不回归) / SC-11 (全量绿) 在正确实现下确实可达。fail-safe 方向的正确性还有一个漂亮旁证: `find … -exec cat {} \;` 与 `xargs -I{} ./do env` 因字面 `{}` 被块字符检测**过度触发**→ 降级 → exit 不变。过度触发只花掉覆盖率, 不产生错误结论 —— 这正是 fail-safe 该有的失效模式。

2. **转出七项全部自包含且实测属实** (R2 knowledge M-2 的要求)。5 条复现命令逐条直调 5/5 = exit 0, 未来开 issue 者不依赖任何未提交的审计报告。

3. **「设计演进三版表」+「7 条被推翻断言」经原文逐条核实零失真**, 且明确写出第 (6)(7) 条是在修前几条的重写里新引入的。这是同类 spec 里少见的元认知诚实度, 直接服务于 Phase B 与转出收口者。

4. **SC-12 有真检出力** (不是补个形式锁): 实测 `cat /opt/.env; echo hi >/dev/null # guard:ack: audit probe` 整条 = **0**; 而首段 `cat /opt/.env` = **2** ⇒ 若实现把 ack 下沉段级, 该断言必红。R2 m-3 得到的是一条会真红的锁。

5. **判定顺序重排 (先 pattern 后 credit) 是本版化解 R2 backend 「+85~92% 击穿 SC-8」的正解**, 且是布尔等价的 —— 我按「命中 pattern ∧ 无 credit ⇒ 拦」逐段模拟, 与逐段先算 credit 的结果完全一致, 等价性成立。用重排换掉「把转出 6 拉回范围」是范围纪律与性能的双赢。

---

## 问题

### Critical (必须修复)

**无。** v3 的核心机制在全语料上零回归、零非预期假阳性, 无安全性或范围性阻塞项。

### Important (应该修复)

**M-1. SC-6 是本版新机制的唯一核心锚点, 但它没要求「两条路径下 exit 必须可分辨」—— 实测其中至少 3 条在 fallback 与误切两种实现下 exit 完全相同, 可以整族写成恒绿**

- 位置: `proposal.md:164` (SC-6)
- SC-6 的形状是「前 10 条走 fallback 且**改前改后 exit 一致**, 后 2 条走 split」。问题在于: **exit 一致**这个谓词, 对 payload 为 benign 的用例在**两种实现下都成立**。canonical 直调实测:

  | SC-6 候选用例 | 整条 (= fallback 路径) | 按 `;`/`&&` 切后各段 max (= 误切路径) | 可分辨? |
  |---|---|---|---|
  | `ls; echo done >/dev/null` (SC-6 第 11 条) | **0** | **0** | ❌ 恒绿 |
  | `ls -la; pwd` (SC-6 第 12 条) | **0** | **0** | ❌ 恒绿 |
  | `[[ -f /opt/.env && -r /opt/.env ]]` (SC-6 `[[ && ]]` 条) | **0** | **0** | ❌ 恒绿 |
  | `{ ls; echo x; } >/dev/null` (benign 写法的 `{ }` 条) | **0** | **0** | ❌ 恒绿 |
  | `{ cat /opt/.env; echo x; } >/dev/null` (**leak-bearing** 版) | **0** | **2** | ✅ 有分辨力 |
  | `for ((i=0; i<3; i++)); do cat /opt/.env; done >/dev/null` | **0** | **2** | ✅ 有分辨力 |

- 为什么重要: SC-6 被 rule6_note 点名为 substitute, spec 自己称它是「本版新机制的核心锚点」。若 Phase B 按字面挑 benign payload 写这 12 条 (最自然的写法就是 `{ ls; echo x; }` 这种), 整族对「降级检测是否真的生效」**零检出力**, 一个根本没实现 `safe_to_split()` 的版本也能全绿。这正是 memory `feedback_noop_in_test_env_hardening_needs_mechanism_assertion` 与我 R2 建议 2 (「凡涉及切/不切一律用分段函数求值表述, 不用 exit code」) 指向的同一个坑, 只是这次落在新加的 SC 上。
- 修法 (二选一或并用):
  1. SC-6 每条 fallback 用例的 payload **必须 leak-bearing + 尾部 credit** (形如 `{ cat /opt/.env; echo x; } >/dev/null`), 并把断言写死为「改后仍 exit=0; **若变 2 即降级检测失效**」—— 上表已实证这种写法两路可分辨;
  2. 或与 SC-5 同形, 断言 `safe_to_split()` 的**返回值**而非 exit code (`{…}`→false / `for ((…))`→false / `ls -la; pwd`→true), 这样 payload 是否 benign 就无所谓了。

**M-2. §1 的注解用 `done` 论证「必须限定命令位置」, 但 `done` 根本不在它自己声明的关键字集里 —— 规则与理由自相矛盾 (v2 残留), 且真正的过度触发面无例、无 SC**

- 位置: `proposal.md:41` (关键字集 = `for` `while` `until` `if` `case` `select`) + `:43` (注解) + `:164` (SC-6 后 2 条沿用该例)
- 矛盾: 注解上半句说「**只检测起始关键字**: 有 `do`/`done` 必有 `for`/`while`」, 下半句却说「否则 `ls; echo done >/dev/null` 里的 `done` 会被误判为关键字而降级」。按上半句, `done` 从不被检测, 这个例子无法论证任何事; 它显然是 v2 原型 (当时检测 `do`/`done`) 的残留。
- 后果不是纸面的: 若实现者照注解把 `do`/`done` 也纳入检测, 那么 `cat /opt/.env; echo done >/dev/null` 这种日常命令会**静默降级** —— 实测该条整条 = **0**, 正确实现 (split) 应给 **2**。#128 的修复在这类命令上悄悄失效, 而 SC-6 的两条锚点 (见 M-1) 抓不到。
- 真正需要锁的过度触发面是**起始关键字出现在参数位**, spec 无一例。实测两条可用锚点:

  | 用例 | fallback 路径 | 正确 (split) 路径 |
  |---|---|---|
  | `cat /opt/.env; echo if >/dev/null` | 0 | **2** |
  | `cat /opt/.env; grep -r for /tmp >/dev/null` | 0 | **2** |

- 修法: (a) 删掉 `:43` 的 `done` 例子, 换成 `echo if` / `grep -r for` 这类**集合内关键字落在参数位**的例子; (b) SC-6 后 2 条同步换成上表两条 (它们两路可分辨, 且同时锁住「关键字集」与「命令位置」两件事)。

**M-3. SC-5 的 `case x in a) ;; esac`→1 段在 spec 自己的口径下不可满足, 两种读法产出不同代码**

- 位置: `proposal.md:163` (SC-5, 自述「分段器单元测试, **数组基数断言**」) + `:145-:146` (Task 1.1 `safe_to_split()` / Task 1.2 `split_top()`「切顶层 `;` `&&` `\|\|`; 空段跳过」)
- 按 Task 1.2 的字面定义对 `case x in a) ;; esac` 求值: `;;` = 两个顶层 `;` ⇒ 段 = `case x in a)` / `` (空, 跳过) / ` esac` ⇒ **2 段**, 与 SC-5 断言的 **1** 直接冲突。
- 两种读法:
  1. SC-5 测的是 `split_top()` 单体 ⇒ 断言不可满足, 实现者会去给 `;;` 加特判 (纯属多余复杂度, 因为 `)` 已经让 `safe_to_split()` 返回 false);
  2. SC-5 测的是 `safe_to_split()+split_top()` 合成管道 ⇒ 值为 1 (降级 = 1 个判定单元) 成立, 但这条属于 **SC-6 的管辖内容被错放进 SC-5**, 且 SC-5 其余 9 项 (`a; b`→2 等) 在两种读法下同值, 唯独这一项分叉 —— 实现者从体例推不出该用哪种。
- 为什么重要: SC-5 是 rule6_note 点名的 substitute, 且是全篇唯一的机制层断言。一条读法分叉的机制断言会直接改变 `split_top()` 的代码形态 (要不要处理 `;;`)。
- 修法: 把 `case x in a) ;; esac` 从 SC-5 移到 SC-6 (它本来就是块结构降级族的成员, `)` 是块字符), 并在 SC-5 开头写死「本 SC 断言 `split_top()` **单体**返回的数组基数, 输入均已假定 `safe_to_split()==true`」。

**M-4. `corpus_census.py` 是「五次计数争议」的根治交付物, 却只有 Task (1.4) 没有任何 SC —— 与本版刚为 `secret-hygiene.md` 补 SC-13 的处置直接不对称**

- 位置: `proposal.md:90` (Key Deliverables 第 3 项) + `:110` (决策表「数字口径 → 交付权威计数器」) + `:148` (Task 1.4) + SC-1~SC-13 (无一条提及)
- 本版为了 R2 knowledge M-1 (「上版只落 Task 无 SC」) 专门加了 SC-13 锁住 `secret-hygiene.md` 的计数回填。同一个缺陷形态在 `corpus_census.py` 上原样存在: 没有任何断言要求它跑出 **65/49/16/15/1 + 5**。
- 为什么重要: (a) 这个计数器的**唯一存在理由**就是让数字可复算, 它自己不被验证等于没有根治 —— 下一次争议时它会成为「权威的错答案」; (b) SC-2 的 15/5、SC-3 的 49 全部是它的输出, 计数器错则两条 SC 一起对不上账; (c) R2 qa `:48` 明确要求「用**提交进仓库的**脚本重新机械枚举……使其可被任何人重跑复现」, 无 SC 就无人验证它真的可重跑。
- 修法: 加一条 SC (或并入 SC-3): 「`python3 aria/hooks/tests/corpus_census.py` 在 CI/本地跑出 `65 / 49 / 16 / 15 / 1` + 换行 `5 (4 拦 1 放)`, 与 Impact 迁移面逐数字一致 (机械比对)」。成本一行。

### Minor (建议修复)

**m-1. §3 性能表三行是单次点测且内部算术不自洽, 而 SC-8 自己要求 20 轮中位数**
- 位置: `proposal.md:71-:75`
- 表内: 2 段全 benign 146ms / 3 段全 benign 158ms / 3 段末段命中 191ms (均为 credit-first 列)。按 spec 自述 `has_filter` = 13 处 subprocess、本 cycle 实测 ~3.5ms/pipeline: 2 段→3 段应多 13 次 fork ≈ **+46ms**, 实测只差 **12ms**; 而「3 段末段命中」在 credit-first 下每段都算 credit, 与「3 段全 benign」**应当等价**, 实测却差 **33ms (21%)**。两处偏差都指向单次点测噪声 (spec 自己在 R2 记录过本机轮间极差可达 92%)。
- 结论方向 (重排省 80~86%) 不受影响, 但建议按 SC-8 同法 (20 轮中位数) 重测后回填, 或至少标注「单次点测, 量级参考」—— 否则这三组数会像 294ms 那样被下一轮当基线继承 (memory `feedback_spec_inherits_upstream_dec_errors`)。

**m-2. §5 的「五个结果」列表混用两种 schema, 而这个列表的存在目的恰恰是终结计数口径之争**
- 位置: `proposal.md:94`
- 「作者 68/52/16」「R1 tech-lead 72/53/19」「R2 qa 65/49/16」「作者权威计数器 65/49/16」都是 (总数 / 拦 / 放); 但「R1 qa 53/17/2」不是 —— 核对 R1 qa 报告 `:30-:31`, 53 = `expected=2`、17 = `expected=0`、2 = want=0 真边界条数, 该报告**没有给总数** (相加为 70)。
- 建议统一为 (总/拦/放) 或给每组标注列名; R1 qa 那组写成「R1 qa 70/53/17 (另报真边界 2 条)」。

**m-3. §What.5 的「验证脚本经 `sed` 编辑后须重读确认」是全文唯一带「必须」却无 Task 无 SC 的规范性要求**
- 位置: `proposal.md:98` (blockquote)
- 与它同源的自查事件已写进头部 (v2 验证脚本被 `sed` 写坏仍「全绿」), 但落到执行面只有一句叙述。按本 spec 自己反复应用的原则 (「有规范性断言就该有可证伪锁」, R2 m-3 就是照此补出 SC-12 的), 这条应有归属。
- 建议: 挂到 Task 1.8 (全量回归 + 性能实测) 作为执行前置, 或写进 SC-9 的脚本要求 (「dogfood 脚本不得经就地编辑后直接采信, 须重读校验」)。这类风险有 memory 背书 (`feedback_harness_nul_in_backtick_edits_verify_with_python`), 不是空谈。

**m-4. SC-3 的「49 条」中 32 条 (65%) 在本版规则下结构上不可能变红, 建议标注有效面**
- 位置: `proposal.md:161` (SC-3)
- 按 v3 规则对这 49 条逐条求值: **32 条**的唯一顶层边界是 `\|` (不切) ⇒ 恒为 1 段; 真正走 SPLIT 的 **12 条** (`#152 mid ; env` / `mid && printenv` / `mid \|\| env` / `env then ; more` / `R3-C-2: exec 3< redirect` 等), 走 FALLBACK 的 **5 条** (`{ env; }` / `{ printenv; }` / `if :; then env; fi` / `while :; do printenv; done` / `if x; then y; else env; fi`)。
- SC-3 作为「拦截面不回归」的回归锁没有问题 (我实测 49/49 改后仍为 2), 但「49 条」的表面覆盖强度会被误读。建议在 SC-3 后加半句「(其中 12 条实际走 split、5 条走 fallback、32 条因仅含 `\|` 而恒为单段 —— 有效面 = 17 条)」, 让 Phase B 知道该重点盯哪 17 条。

**m-5. 转出 1 的「81 条 `[^\|]*`」记号略窄 + Key Deliverables 小节打断 §1-§5 编号**
- 位置: `proposal.md:127` / `:86-:90`
- 前者: 含 `[^\|]` 任意形态的 pattern = **81** (数值正确), 但严格写作 `[^\|]*` 的只有 **79**, 另 2 条是 `[^\|]+` (`kubectl get secret[^\|]+-o …` / `redis-cli GET [^\|]+(secret\|…)`)。建议写「81 条含 `[^\|]` 量词的 pattern (79 条 `[^\|]*` + 2 条 `[^\|]+`)」, 免得收口者按 `[^\|]*` 精确 grep 时数出 79 又开一轮争议。
- 后者: `### Key Deliverables` 夹在 §4 与 §5 之间, 打断 §1→§5 的编号序列, 且 §5 标题「数字口径必须可复算」实际承载的是交付物说明。纯格式, 建议 Key Deliverables 移到 §5 之后。

---

## 建议

1. **把「可分辨性」升为本 spec 的 SC 通则。** 本轮 M-1/M-3 与我 R2 的 M-2 是同一个类: **一条 SC 若在「正确实现」与「典型错误实现」下产出同样的观测值, 它就不是验收条件, 是装饰**。本 spec 已经有两个正面样板 (SC-4 「切错必 exit=0」、SC-12 「下沉段级必由 0 变 2」), 建议在 Success Criteria 抬头补一句通则: 「每条 exit-code 类 SC 须同时写出它在**误实现**下的预期值, 二者必须不同; 做不到的改写成机制断言 (仿 SC-5)」。这一句能一次性覆盖 M-1、M-3 和未来同类。
2. **Phase B 可以直接复用本轮的模拟结论作为实现自检**: 305 条语料下 `mode` 分布应为 单段 281 / SPLIT 13 / FALLBACK 11, `after != before` 恰 1 条 (KNOWN-LIMIT 转正)。这三个数比「全绿」强得多 —— 全绿在 281 条单段用例上是自动成立的, 而这三个数会在 `safe_to_split()` 过度/不足触发时立刻偏移。建议把它们写进 `corpus_census.py` 的输出 (顺带解决 M-4)。
3. **转出 2 的 issue 里请附上本轮的 11 条语料清单**。它们是现成的、已在套件里的块结构用例, 未来做块结构解析时可直接当回归基线, 不必重新构造。

---

## 评估

**是否可以继续?** 需要修复 (设计层已收敛, 验收层未收敛)

**理由**: v3 的 fail-safe 降级是这个 cycle 三版里第一个经得起全语料检验的设计 —— 我按 spec 规则独立实现分段器, 对 305 条语料 ~360 次 canonical 直调模拟, 结果是**零 want=2 回归、零非预期假阳性、恰 1 条刻意的 KNOWN-LIMIT 转正**, v2 的 5/5 误伤类被结构性消除; 我 R2 的 1C+3M+5m 有 8 条完全核销、1 条部分, 零静默丢弃; 141/305/12/13/1/`:663`/366-360/65-49-16-15-1+5、v1.65.5、`5fab5b8`、五条转出复现命令、以及「三版表 + 7 条被推翻断言」逐条对照 R1/R2 原文, **全部属实**, 本轮还推翻了我自己 R2 的一处语料断言。**没有 Critical**。

但四条 Major 都落在**验收有效性**而非设计上, 且集中在本版新加的 SC: SC-6 (新机制的核心锚点) 实测至少 3 条候选在两种实现下 exit 相同、可以整族恒绿; §1 注解拿一个不在自己关键字集里的 `done` 当论据, 使真正的过度触发面既无例也无锁; SC-5 的 `case … esac`→1 在 Task 1.2 的字面口径下不可满足, 读法分叉会改变代码形态; `corpus_census.py` 有 Task 无 SC, 与本版刚为 `secret-hygiene.md` 补 SC-13 的处置自相不对称。这四条会让 Phase B 在「全绿」下交付一个**没有被验证过的降级检测**。修法全是文字级、不改范围、不改设计, 且我已给出实测可分辨的替换锚点 —— 一轮可收敛, R4 应只需核对这四处落地。

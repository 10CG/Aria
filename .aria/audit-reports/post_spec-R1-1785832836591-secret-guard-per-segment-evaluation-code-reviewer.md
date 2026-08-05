---
agent: code-reviewer
round: R1
verdict: REVISE
critical_count: 1
major_count: 6
minor_count: 5
---

# post_spec R1 — secret-guard-per-segment-evaluation (code-reviewer 视角)

审计对象: `/home/dev/Aria/openspec/changes/secret-guard-per-segment-evaluation/proposal.md`
参照物: `aria/hooks/secret-guard.sh` @ `af87cae` (698 行) / `aria/hooks/tests/secret-guard.test.sh` (798 行) / forgejo aria-plugin #128
方法: 逐条实跑核实 (hook 实调 + 测试套件插桩枚举 + 性能实测 + forgejo API 取原文)。**未修改仓库任何文件** (插桩副本在 scratchpad)。

---

## Phase 1: 规范合规性

**判定**: PASS (可进入 Phase 2)

- Level 2 结构完整: Why / What / 关键决策 / Impact / rule6_note / Tasks / Success Criteria 齐备。
- Rule #6 框定与同一 hook 的先例 (`openspec/archive/2026-06-19-secret-guard-exfil-coverage-iteration/`) 及 owner 2026-08-02 对 `secret-guard-nomad-var-put-echo` 的裁定一致, substitute 已点名。
- Rule #1/#5 满足: 变更放本项目 `openspec/changes/`, 非 standards。
- 前序衔接属实: `openspec/archive/2026-08-02-secret-guard-nomad-var-put-echo/proposal.md:113` 转出 1 确为本 spec 的来源, 措辞对应。

---

## Phase 2: 代码质量 / 事实准确性

### 已核实为正确的断言 (逐条实跑)

| 断言 | 核实方式 | 结论 |
|------|---------|------|
| 141 条 pattern | 机械解析 `risky_patterns` 数组 (canonical 402-656 行, 去注释/空行) | 正确 |
| 305 条 `bash_case` | 插桩 `bash_case()` 计数 | 正确 |
| 366 总用例 | 实跑 `bash hooks/tests/secret-guard.test.sh` → `PASS: 366 / 366` | 正确, 且当前全绿 |
| 68 含分隔符 / 52 拦 / 16 放行 / 15 纯管道 / 1 真边界 | 插桩枚举后按「顶层 `;` `&&` `\|\|` `\|`」口径重算 | 五个数**全部正确** (口径见 M-5) |
| triage 五形态全 `exit=0`, 对照 `cat /opt/.env` `exit=2` | 对 canonical hook 实跑 5+1 条 | 5/5 复现, 对照 exit=2 |
| 「#170 修复在复合形态下失效」 | 实跑 `nomad var put p2 @f2` 单条 = exit 2, `... >/dev/null; nomad var put p2 @f2` = exit 0 | 论断成立 |
| `:405` 裸 `/v1/var/` pattern | canonical 与旧副本第 405 行均为 `'/v1/var/'` | 正确 |
| `:318-:400` has_filter 区 | `:318` = Filter detection 分隔注释, `:323` = `has_filter=0`, 区间止于 `:401` 分隔注释 | 正确 |
| v1.26.0 O3 的 `=~` 改造 | 源码 `:659-661` 注释原文 | 正确 |
| `e8e847c` cherry-pick 起源 | `git show e8e847c` = "TASK-001 cherry-pick secret-guard + secret-scan from SilkNode" | 正确 |
| python 组合 pattern 存在 | `:548` `'python3?[[:space:]]+-c[^\|]*(/v1/var/\|secretsmanager\|/secrets/\|\.env\|provider_key)'` | 正确 |
| comment 17512 / 17545 | forgejo API 取回, 内容与 spec 引述逐句对应 | 正确 |
| v1.65.5 → v1.65.6 PATCH | `aria/.claude-plugin/plugin.json` = `1.65.5`; #170 同类「拦截面扩大」以 v1.65.4 PATCH 落地 | 正确, 有先例 |
| 「hooks/tests/ 其余 5 个脚本」 | 该目录 6 个 test 脚本 (`jq-crlf-guard.sh` 是库非测试), 减本体 = 5 | 正确 |
| SC-5 目标用例存在 | `hooks/tests/secret-guard.test.sh:765-770`, 注释确含「归转出 1」指向 | 正确 |

这一层的密度高于一般 spec, 数字大多经得起独立重算 —— 下述问题集中在**行号出处**、**因果论证**与**边界决策的自洽性**上。

### 优点

1. §What.1「管道不是边界」是本 spec 最有价值的判断, 且给了可证伪锚点 (SC-2 的 15 条逐条列名)。实测确认: 若按 `\|` 切, `cat /opt/.env`/`curl …/v1/var/x` 会成为无 credit 的独立段, 15 条正确写法全部翻红。
2. SC-4 的**机制断言**(要求对分段函数直接求值断言返回单段, 而非只看 exit code) 设计正确 —— 它恰好绕开了下面 M-2 揭示的假绿陷阱。这是全篇最硬的一条。
3. SC-1 明确要求「改前实测 exit=0, 改后 exit=2」的 baseline-failing 双向记录, 符合 substitute 框定的举证要求。
4. Impact 里「行为变更告知 + CHANGELOG 显著标注 + 给出迁移写法」把用户可感知的破坏面单列, 不藏在技术描述里。

---

## 问题

### Critical (必须修复)

**C-1. 「子 shell / 反引号 / heredoc: 本 spec 不解析, 保守不切」自相矛盾, 且 fail-safe 方向标反**

- 位置: `proposal.md:64` (§What.2 未建模边界) + `proposal.md:99` (关键决策表第 3 行) + `proposal.md:147` (SC-7)
- 问题有三层:
  1. **不解析 ⇒ 就是会切。** `$( … ; … )` 与 heredoc 体内的 `;`/换行, 在「命令字符串」这一层是普通字符。要实现「不切」必须跟踪括号嵌套与 heredoc 定界符 —— 那正是「解析」。「不解析」与「保守不切」不能同时成立, 实施者必须二选一, 而 spec 没有给出选择。
  2. **理由方向标反。** 决策表写「不切 = 偏保守 (可能多拦, 不会少拦)」, 但 spec 自己在 §What.2 论证的是**切错会让组合 pattern 跨段失配**。实测佐证: `python3 -c 'import urllib.request` 这一段单独喂给 hook = **exit 0**, 而整条 = exit 2。即「切」在组合 pattern 上确实会**少拦**。所以真正保守的是「不切」, 而「不解析」的默认行为恰恰是「切」。
  3. **规范性与描述性打架。** 决策表是规范性的 (「保守不切」= 要求), SC-7 却写「锁定**实现后的实际** exit code」= 描述性 (实现成什么就锁什么)。两者不构成验收关系: 若实现按「不解析」写成了「切」, SC-7 照样绿。
- 为什么重要: 这是安全 hook 的边界语义。两种读法产出不同代码、不同拦截面, 且 SC-7 无法把它们区分开 —— 属于「谓词档未做全分割」的同类 (memory `feedback_predicate_tiers_need_total_partition_proof`)。
- 修法建议: 明确二选一并让 SC-7 与之对齐。若选「不切」, 须在 §What.1 规则表增行 (「`$(`…`)` / 反引号 / heredoc 体内 = 不切」) 并承认它需要最小限度的嵌套/定界跟踪, SC-7 改为断言「分段函数对 `$(cat /opt/.env; true)` 返回单段」这类**机制断言**; 若选「不解析即切」, 须删掉「保守不切」措辞、改写理由 (承认这是**放宽**方向), 并新增一条组合-pattern 跨段失配的已知限制。

### Important (应该修复)

**M-1. `:653` / `:646` / `:648-:690` 三处行号指向的是过期副本, 不是交付目标文件**

- spec 引用: `proposal.md:13` (`:653` has_filter 全局开关) / `:108-:116` 隐含的 risky_patterns 区 `:402-:646` / 匹配循环 `:648-:690`
- 实测 canonical `aria/hooks/secret-guard.sh` (698 行, `af87cae`):

  | spec 写 | 实际 |
  |---------|------|
  | `:653` `if [[ $has_filter -eq 0 ]]` | **`:663`** |
  | risky_patterns 区 `:402-:646` | **`:402-:656`** |
  | 匹配循环 `:648-:690` | **`:658-:696`** |

- 出处已定位: 这三个数字精确匹配 `/home/dev/Aria/.claude/scripts/secret-guard.sh` (688 行, 140 pattern) 与 marketplace 缓存副本 —— 即 **pre-#170** 版本, 二者 `diff` 唯一差异就是 canonical 多出 `:407-:416` 的 `nomad var put` pattern 及其 9 行注释, 正好差 10 行。
- 直接继承自 triage comment 17512 (原文同样写 `:653`), 属 memory `feedback_spec_inherits_upstream_dec_errors` 的复现。
- 为什么重要: spec 一边引用 **141** (canonical 的数) 一边引用 **旧副本的行号**, 出处混合。Phase B 实施者按 `:653` 定位会落在注释区。`:318-:400` / `:402` / `:405` 恰好一致 (差异在其后), 更容易让人误判整组行号可信。
- 修法: 三处行号改为 663 / 402-656 / 658-696, 并注明基准 SHA。

**M-2. 「切错 = 安全回归」被实测证伪 —— quote-aware 的举证链断了**

- 位置: `proposal.md:55` (「切错会让本该拦的命令逃逸」) + `:98` (决策表「实测 2 条 expected=2 用例的分隔符在引号内, 切错 = 安全回归」)
- 实测 (对 canonical hook 逐段喂入):

  | 切开后的段 | exit |
  |-----------|------|
  | `ssh root@host 'find / -name .env.production -exec cat {}` | **2** |
  | `\;'` | 0 |
  | `python3 -c 'import urllib.request` | 0 |
  | ` print(urllib.request.urlopen("http://nomad/v1/var/x").read())'` | **2** |

  两条命令切错后**任一段仍触发 exit 2** ⇒ 整体 fail-safe 后仍 exit 2 ⇒ **不逃逸, 不构成安全回归**。
- spec 只在 `:62` 的「未验证项」里对 python 一例作了推测性对冲 (且推测方向正确), 但正文 `:55` 与决策表 `:98` 仍把「切错 = 安全回归」当作**实测结论**陈述, 且完全没提 ssh 一例同样被兜住。
- 为什么重要: quote-aware 本身仍应做 (spec `:62` 的「兜底是巧合不是设计」是正确论证), 但**当前给出的证据不支持当前给出的结论**。若 R2/R3 有人复算发现证据不成立, 可能连带动摇「必须感知」这个正确决策。
- 修法: 把 `:55` 与 `:98` 的理由改为「已实测: 切错后两条仍被其他 pattern 巧合兜住 (段级 exit=2), **不逃逸**; 但兜底路径 (裸 `/v1/var/` 与 `.env` 读) 与引号语义无关, 属巧合 —— 组合 pattern (`:548`) 本身确已失配, 实测段 1 = exit 0。故 quote-aware 仍是硬要求」。SC-4 无需改 (它已经是机制断言, 恰好不依赖这条错论证)。

**M-3. SC-8 冻结绝对毫秒数不可复现, 阈值远小于本机噪声**

- 位置: `proposal.md:84` (基线 69ms / 76ms + 「约 60ms 是 bash 进程启动固定成本」) + `:148` (SC-8 「相对基线 69ms/76ms 增幅 ≤ 30%」)
- 实测 (同一未改动 canonical hook, benign `ls -la`, 20 次均值, 同机连续 5 轮):

  ```
  111ms / 148ms / 213ms / 153ms / 181ms
  ```

  相邻两轮最大相差 **92%**, 最低值也已是 spec 基线的 1.6 倍。SC-8 的 `69 × 1.3 = 90ms` 门槛在**零代码变更**下就恒红。
- 归因也错: 实测 `bash -c true` = **2ms**, `jq -n .` = **58ms**。60ms 的固定成本是 **`jq`** (hook `:149` 调 jq 解析 stdin JSON), 不是「bash 进程启动」。属 memory `feedback_attribute_latency_by_measurement_not_hypothesis` 的同类。
- 为什么重要: 这是一条会**恒红**的验收门 (memory `feedback_check_predicate_must_validate_against_real_data_range`)。恒红门的实际后果是被绕过或被随手改数字, 两种都比没有更糟。
- 修法: SC-8 改为「Phase B **同 session 同机**先重测 before 基线 (≥20 次, 记录中位数与极差), 再测 after, 断言 `after_median ≤ before_median × 1.3` 且报告极差」; §What.4 的固定成本归因改为 `jq` 启动 (~58ms 实测), 并顺带指出该成本与段数无关 —— 这反而**加强**了「分段增量很小」的结论。

**M-4. 「子 shell / 反引号 / heredoc 内部的分隔符, 现有语料零覆盖」部分证伪**

- 位置: `proposal.md:64` + `:99` (决策表理由「语料零覆盖, 无法验证正确性」)
- 实测枚举 305 条 `bash_case`:
  - `$( )`: 4 条 (`echo "$(< /opt/.env)"` / `printf -v VAR "%s" "$(< /opt/.env)"` / `x=$(env)` / `echo $(printenv KEY)`) —— 内部**确无**分隔符, 这部分断言成立。
  - 反引号: 1 条 (`x=\`env\``) —— 内部无分隔符, 成立。
  - **heredoc: 1 条**, `#157 heredoc-style nomad get` = `cat <<EOF\nsecret\nEOF\nnomad var get nomad/jobs/x` (want=2)。heredoc 体内**含换行分隔符**, 且换行是 spec 规则表里的切分记号 ⇒ **heredoc 内部分隔符并非零覆盖**。
- 为什么重要: (a) 决策表的理由「语料零覆盖 ⇒ 无法验证正确性」对 heredoc 不成立, 而 heredoc 恰是 C-1 里最难「不切」的一类; (b) SC-7 写「子 shell / 反引号 / heredoc 各 **1 条**」新增, 实施者可能新增一条而不知道**已有一条**正在被换行切分器实际穿过。该用例目前碰巧仍 exit=2 (末段含 `nomad var get`), 属侥幸而非设计。
- 修法: 改为「`$()`/反引号内部分隔符零覆盖; heredoc 已有 1 条 (`#157 heredoc-style nomad get`)」, 并把该既有用例纳入 SC-7 一并锁定。

**M-5. 迁移面统计口径把「换行」排除在外, 与 §What.1 规则表冲突; 5 条换行用例落在 SC-2/SC-3 枚举之外**

- 位置: `proposal.md:110-:116` 迁移表 + `:142`(SC-2) + `:143`(SC-3), 对照 `:44-:49` 规则表 (换行 = **切**)
- 实测各口径:

  | 口径 | 总数 | want=2 | want=0 |
  |------|------|--------|--------|
  | 顶层 `;` `&&` `\|\|` `\|` (spec 实际口径) | **68** | **52** | **16** |
  | 上者 + 换行 | 73 | 56 | 17 |

  spec 的 68/52/16/15/1 在**第一行口径**下全部正确 (52 与 54 的差 = 那两条引号内 `;` 的用例, spec 按「顶层」把它们排除, 合理)。但换行被一并排除了, 而规则表明写换行要切。
- 落在枚举外的 5 条: want=2 四条 —— `#157 multiline echo\nenv` / `#157 multiline set\necho\nprintenv` / `#157 multiline first-line hit kept` / `#157 heredoc-style nomad get`; want=0 一条 —— `#152 FP: multiline benign` (`echo begin\necho done`)。
- 为什么重要: `#152 FP: multiline benign` 是唯一一条「真命令边界 + 期望放行」的**非 KNOWN-LIMIT** 用例, 迁移表却声称这类只有 1 条 (KNOWN-LIMIT)。它既不在 SC-2 的 15 条纯管道里, 也不在 SC-3 的 52 条 want=2 里 —— 只有 SC-9 全量兜底。同理 4 条 want=2 换行用例不在 SC-3 的显式回归锁内, 而其中含 heredoc 那条正是跨段失配风险最高的形态 (`[[:space:]]` 会匹配换行, 分段后跨行 pattern 必然失配)。
- 修法: 迁移表补一行「含换行 (顶层外) | 5 | 4 拦 / 1 放行」并写明统计口径; SC-3 的 52 扩为 56 或另立 SC 覆盖换行族; `#152 FP: multiline benign` 显式并入 SC-2 的回归锁语义 (即使不属纯管道)。

**M-6. ship 同步面漏 `.claude/scripts/secret-guard.sh` 本地副本 —— 且该副本当前已停在 pre-#170**

- 位置: `proposal.md:90-:91` (Key Deliverables) + `:120` (ship 同步面)
- `standards/conventions/secret-hygiene.md §6` 明确: Aria self 属 `dual_install` 预期态 (plugin SOT + `.claude/scripts/` 本地副本并存, 双重防线 by design), 并把 `divergent_content` 列为**必须 investigate** 的 sub-flag。
- 实测该副本当前状态: 688 行 / **140 条 pattern**, 缺 `nomad var put` pattern, 最后同步于 v1.55.4 期 (`git log -- .claude/scripts/secret-guard.sh` → `f480e6e` 等「副本同步」提交)。`.claude/settings.json` 的 PreToolUse hook **指向的就是这个副本**。
- 后果实测:

  | 命令 | canonical | 本仓实跑副本 |
  |------|-----------|-------------|
  | `nomad var put p2 @f2` | exit **2** | exit **0** |

  即 **Aria 自身运行时至今没有 #170 的修复**。
- 为什么重要: 本 spec 的立论是「#170 的修复在复合形态下失效」, 而在本仓运行时它在**单命令形态**下也没生效。若本 spec 沿用 #170 的同步面 (2 交付文件 + 5 版本文件 + gitlink), 修完之后 Aria 自己仍然跑旧逻辑, dogfood 会给出误导性结论。副本漂移本身是 #170 遗留 (非本 spec 引入), 但**枚举 ship 同步面是本 spec 的内容**, 漏项属本 spec 的缺陷。
- 修法: ship 同步面增列 `.claude/scripts/secret-guard.sh` 副本同步 (并顺带补齐它缺失的 #170 pattern), 或显式写明「本 cycle 不同步该副本, 理由 X」并开 issue。Task 1.4 的 dogfood 须注明跑的是哪一份。

### Minor (建议修复)

**m-1. 误引 issue 原文用例数**: `proposal.md:108` 写「原文估「141 pattern + **347** 用例语义都要重审」」。issue #128 原文为「影响面大: 141 条 pattern 与 **366** 条用例的语义都要重新审视」; 347 出自原文另一句 (「347 条全量回归对两次退化都全绿」)。141 引对了, 366 被换成了 347。

**m-2. Task 与 SC 的映射有错位**: `:135` Task 1.3 写「测试族: SC-1~SC-**8**」, 但 SC-8 是性能, 实际归 Task 1.4 (`:136` 「+ 性能实测」); SC-9 未被任一 Task 显式点名 (由 1.4「全量回归 (366 + 新增)」隐含)。建议 1.3 改 SC-1~SC-7, 1.4 显式点名 SC-8 + SC-9。

**m-3. 决策表「guard:ack 维持命令级」无对应 SC**: 七行决策中六行有 SC 对应 (管道→SC-2 / 引号→SC-4 / 子shell→SC-7 / 任一段 blocked→SC-1 / BLOCKED 消息→SC-6 / credit 逐段→SC-1), 唯 `guard:ack` 粒度无可证伪断言。ack 判定位于 `:300` 区、在被重构的 has_filter/匹配循环**上游**, 风险确实低, 但既然它进了决策表就该有锁 —— 建议加一条「复合命令 + `# guard:ack: <reason>` 改后仍 exit=0」。

**m-4. 「2 条分隔符落在引号内」未写明口径**: `:55`。实测语料中**引号内含分隔符字符**的共 8 条; 收敛到「切分集 (`;` `&&` `\|\|` `&` 换行)」才是 2 条 (spec 所指)。另 6 条是引号内 `\|` (如 `jq '.Items | keys'` 三条、`kubectl exec pod -- sh -c 'env|cat'`)。按「管道不切」它们不影响结论, 但分段器若对引号内做任何 `\|` 处理需注意。建议把口径一句话写死。

**m-5. `:62` 的「未验证项」现已可验证, 建议直接落定**: 实测 python 例段 2 (` print(urllib.request.urlopen("http://nomad/v1/var/x").read())'`) = **exit 2**, 确由 `:405` 裸 `/v1/var/` 兜住; ssh 例段 1 = **exit 2**。推测方向正确。把结论写进 spec 可消除一个 Phase B 待办, 并同时修掉 M-2。

---

## 建议

1. C-1 与 M-2/M-4 是同一根系: 都源于「边界语义」的论证只做到了直觉层, 没做到「对分段函数求值」的机制层。建议把 SC-4 那种**机制断言**模式推广到 SC-7 与 §What.2 —— 即凡涉及「切/不切」的主张, 一律用「分段函数对 X 返回 N 段」表述, 不用 exit code 表述 (exit code 会被其他 pattern 巧合兜住, 已实证)。
2. M-1 提示一个可机械化的护栏: spec 引用 hook 行号时同时记基准 SHA, 或干脆引用 `符号名 + 上下文片段` 而非行号。本仓存在 3 份以上 secret-guard 副本, 行号引用天然脆弱。
3. M-6 值得独立开 issue: `dual_install` 副本漂移目前无任何机械检测 (`aria-doctor` 的 `divergent_content` 是按需跑, 非 gate)。本 spec 不必承担, 但应点名。

---

## 评估

**是否可以继续?** 需要修复

**理由**: 数字面质量高 (141 / 305 / 366 / 68-52-16-15-1 逐个重算全部正确, 五形态 5/5 复现), 核心设计判断 (管道不切) 与 SC-4 的机制断言都站得住; 但 C-1 使「子 shell / heredoc 边界」在实施层二义且 fail-safe 方向标反, M-1 的行号出处混入了 pre-#170 旧副本, M-2 的 quote-aware 举证被实测推翻, M-3 的 SC-8 在零变更下就恒红, M-6 会让 dogfood 跑在没有 #170 修复的副本上。这五条都会直接影响 Phase B 的代码形态或验收有效性, 须在进入 Phase B 前收敛。

# secret-guard: fail-safe 逐段判定 (aria-plugin #128)

> **Level**: Minimal (Level 2 Spec)
> **Status**: Draft (R1 `6C+19M` → 缩范围 → R2 `5C+12M` → v3 fail-safe → R3 `4C+13M` → **owner 裁定拉回性能根治** → 本版, 待 R4)
> **Created**: 2026-08-04
> **Issue**: [aria-plugin #128](https://forgejo.10cg.pub/10CG/aria-plugin/issues/128) — triage **confirmed / critical / 5-5 复现** ([17512](https://forgejo.10cg.pub/10CG/aria-plugin/issues/128#issuecomment-17512)) + [分隔符更正 17545](https://forgejo.10cg.pub/10CG/aria-plugin/issues/128#issuecomment-17545)

> ### 设计演进 (三版, 前两版均被审计实测推翻)
>
> | 版本 | 设计 | 被什么推翻 |
> |------|------|-----------|
> | v1 | 逐段判定, 切 `;` `&&` `\|\|` `&` 换行 | R1: `&` 与 `&>` 冲突; 换行切碎 heredoc; 三个子问题未预见 |
> | v2 | 缩到只切顶层 `;` `&&` | R2: **切 `;`/`&&` 本身不安全** —— 它们大量嵌在 `{ }` / `for…do…done` / `[[ … && … ]]` / `for ((i=0; i<3; i++))` 里, 实测 **5/5 安全写法被误报**, 且语料零覆盖 ⇒ 回归 SC 恒绿是假绿 |
> | v3 | **fail-safe 降级**: 先检测块结构, 不可安全分段则退回整命令判定 | R3: 判据**不封闭** (`exec >/dev/null; …` 无块标记仍误报); 命令位置清单漏 换行/`&`/`time`; **重排只在 benign 负载有效**, 最坏负载 +583% |
> | **v4 (本版)** | v3 + **`has_filter` 13 处转 bash 内建** (owner 裁定拉回) + 启发式表述 + 判据补漏 | 待 R4 |
>
> **本 cycle 被审计方实测推翻的作者断言 (7 条)**: (1) `&` 可作切分记号; (2)「保守不切 = 不会少拦」方向反; (3)「切错 = 安全回归」; (4)「pattern 匹配已全是 bash 内建」(`has_filter` 尚有 13 处 subprocess); (5)「60ms 固定成本是 bash 启动」(实为 `jq` 58ms); (6) R1→R2 重写时把已核实的 141 改成 139; (7)「只切 `;` `&&` = 最小可靠子集」—— 最小但**不可靠**。**无一由作者自查发现**。另有一次自查拦截: v2 验证脚本的正则被 `sed` 破坏后仍"全绿", 作者发现并干净重写后才采信 (见 §What.5 的验证脚本要求)。

## Why

`hooks/secret-guard.sh` 的 pattern 匹配与 `has_filter` credit 均对**整条 `$command`** 求值, 由单一全局开关 (`:663`) 控制全部 **141** 条 pattern。命令任一处出现 credit 串 ⇒ 全部段落免疫全部 pattern (triage 5/5 实测):

```
cat /opt/.env; echo hi >/dev/null                      → exit=0
nomad var put p1 @f1 >/dev/null; nomad var put p2 @f2  → exit=0   ← #170 泄漏形态本身
vault read secret/x; nomad var put p @f >/dev/null     → exit=0   ← 跨 pattern 家族
```

单条 `cat /opt/.env` → `exit=2`。`critical` 判据见 triage comment。

## What

### 1. fail-safe 降级 — 本版的核心机制 (**启发式, 非完备判据**)

**分段前先判断该命令是否"看起来可以安全分段"**; 判否则退回整命令判定 (= 现状行为, 零改善零恶化)。

> ⚠️ **承诺强度已下调 (R3-C-2 证伪)**: 前一版写「降级 = 只在能保证正确时才改变行为」。**该判据类别不封闭** —— 实测 `exec >/dev/null; nomad var get x` **无任何块标记**却同样不可安全分段 (`exec` 的重定向作用于整个 shell 后续, 0→2 误报)。故本机制只能表述为**启发式**: 覆盖已知的块结构类, 但**不保证穷尽**。未知形态的误报归转出 8。

不可安全分段的判据 (引号外命中任一即降级):

| 类别 | 标记 |
|------|------|
| 块字符 | `{` `}` `(` `)` 反引号 `[[` `]]` `<<` `<<<` |
| 块起始关键字 (**仅命令位置**) | `for` `while` `until` `if` `case` `select` |
| **作用域型内建 (R3-C-1)** | `exec` `time` |
| **后台记号 (R3-C-1)** | `&` (单独出现, 非 `&&` / `&>` / `>&` / `\|&`) |

**命令位置**定义 (R3-C-1 指出前一版清单有漏且「行首」二义): 行首 / **换行之后** / `;` / `&&` / `\|\|` / `\|` / `&` / `do` / `then` / `else` / `elif` / `in` 之后。**换行必须计入** —— 否则多行命令第 2 行起的 `for`/`while`/`if` 检测不到 (实测 `sleep 1 & for f in a; do cat /opt/.env; done >/dev/null` 由 0 翻 2)。

> **只检测起始关键字**: 有 `do`/`done` 必有 `for`/`while`, 有 `then`/`fi` 必有 `if`。**必须限定命令位置** —— 否则 `ls; echo for >/dev/null` 里作为普通参数的 `for` 会被误判 (SC-14 锁该方向; 前一版这里举 `echo done` 为例是**错的** —— `done` 根本不在关键字集内, 论证不成立, R3 code-reviewer 勘正)。

### 2. 分段规则 (仅在可安全分段时生效)

| 记号 | 处置 |
|------|------|
| 顶层 `;` `&&` `\|\|` | **切** |
| `\|` (管道) | **不切** — filter 语义载体; **12 条 pattern 把 `\|` 编码进正则本身**, 按 `\|` 切会让 4 条真泄漏用例由 2 翻 0 (R1 tech-lead M-4 实测) |
| 换行 | **不切** — 会切碎 heredoc body |
| `&` `&>` `>&` `\|&` `2>&1` | **不切** — `&` 与重定向记号冲突 (R1 C-1: 打红 2 条合法 credit 写法) |
| 引号内 / `\;` 转义 | **不切** — quote/转义感知 |

**`||` 纳入切分** (v2 曾排除, R2 M-3 勘正): 排除它会留下**一字符绕过** —— `put p1 >/dev/null || put p2` 修后仍 exit=0 而 `;` 形态 exit=2; 且「`||` 需前瞻」的理由不成立 (与 `&&` 同一次单字符前瞻)。

### 3. 判定语义 — **先 pattern 后 credit** (R2 C-1 唯一范围内解法)

```
if not safe_to_split(command):            # §1
    return legacy_whole_command_verdict(command)
for seg in split_top(command):            # §2
    if any(seg =~ pat for pat in patterns):   # bash 内建 =~, 零 fork
        if not compute_credit(seg):           # 仅命中段才跑 13 处 subprocess
            BLOCK(pat, seg)
ALLOW
```

**顺序重排是布尔等价的** —— R3 tech-lead 独立验证 (`has_filter` 纯函数分析 + 306 条实证 0 不一致): 两者都是「命中 pattern ∧ 无 credit ⇒ 拦」, 未命中时 credit 值不影响结果。

**但重排本身不足以解决性能** (R3 backend C-1 + tech-lead C-3 双方实测推翻作者原判):

| 负载 | 每段先算 credit | 先 pattern 后 credit | 结论 |
|------|----------------|---------------------|------|
| 2 段全 benign | 146ms | **28ms** | 省 80% |
| 3 段全 benign | 158ms | **22ms** | 省 86% |
| **2 段全命中** | — | — | **+102%** |
| **3 段全命中 (即本 spec 推荐的迁移写法)** | — | — | **+583%, 此档重排还更慢** |

作者原判「重排已化解性能矛盾」**只在 benign 负载成立**, 取样漏掉最坏情况; 而最坏负载恰是 spec 自己在迁移建议里推荐的「逐段补 redirect」。

### 4. `has_filter` 13 处转 bash 内建 (**owner 2026-08-04 裁定拉回范围, 原转出 6**)

`has_filter` 区尚有 **13 处 `echo "$command" | grep -qE …`** 未被 v1.26.0 O3 覆盖 —— 逐段化后 fork 次数 = 13 × 段数, 这才是性能矛盾的**根因**。逐条改为 bash 内建 `[[ =~ ]]` (与 `:658` 匹配循环同款, O3 已验证该改造在本 hook 可行), 使逐段 credit 计算**零 fork**。

owner 裁决理由: 绕开 (重排) 只在部分负载有效, 且与 spec 自己的迁移建议冲突; 根治后性能问题不再依赖负载分布。

**代价 (诚实记录)**: 本 spec 范围由「分段」扩为「分段 + credit 判据重构」, 13 处正则须逐条验证语义不变 (SC-15)。

### 5. 其余语义

- 任一段 blocked ⇒ 整体 `exit 2` (fail-safe, 与现状一致)。
- BLOCKED 消息须指出**触发段落**, 否则复合命令下无法定位。
- `# guard:ack` 维持**命令级**语义 (SC-12 锁定 —— R2 M-5 指出该裁定此前无 SC 无 task)。
- **跨段 pattern fail-open**: 逐段化后依赖跨 `;` 上下文的 pattern 会失配 (实证 `set -o posix; set | grep foo` 2→0)。本版不兜底, SC-7 锁现状。

### Key Deliverables

- `aria/hooks/secret-guard.sh` — `safe_to_split()` + `split_top()` + 判定循环重排 + BLOCKED 消息补段落
- `aria/hooks/tests/secret-guard.test.sh` — 分段器单元测试 + fail-safe 降级族 + 端到端族 + `KNOWN-LIMIT` 转正
- **`aria/hooks/tests/corpus_census.py`** (新增, 随 spec 归档) — 语料统计的**权威计数器**, 见 §6

### 6. 数字口径必须可复算 (根治反复出现的计数争议)

本 cycle 同一统计出过**五个**结果 (作者 68/52/16 · R1 tech-lead 72/53/19 · R1 qa 53/17/2 · R2 qa 65/49/16 · 作者权威计数器 65/49/16), 根因是**数法未固化**而非谁算错。

**定案 65/49/16/15/1 + 5** (作者权威计数器与 R2 qa 双独立扫描器交叉确认, R2 tech-lead / code-reviewer 亦复现一致)。计数器随 spec 交付 (`corpus_census.py`), 口径与 §2 规则表同源: quote-aware, 顶层 `;` `&&` `||` `|`, 换行单列。

> **⚠️ 原型正则不可逐字搬运 (R3 backend M-2)**: 作者原型用 Python 正则, 含 `(?:…)` / `\b` / `\s` —— **bash 的 POSIX ERE 全不支持**。逐字搬运会让 `safe_to_split()` 静默失配 ⇒ 全部走 split ⇒ 退回 v2 的 5/5 误报。实现须用 ERE 等价写法 (`[[:space:]]` 代 `\s`, 去掉非捕获组, 词边界改显式字符类), 并由 SC-16 锁定。
>
> **另**: 验证脚本若经 `sed` 等就地编辑, **必须重读确认正则未被破坏后才可采信结果** —— 本 cycle v2 原型被 `sed` 写坏正则后仍输出"全绿", 作者干净重写才发现。

## 关键决策

| 决策 | 选择 | 理由 |
|------|------|------|
| **块结构** | **fail-safe 降级到整命令判定** (**启发式, 不保证穷尽**) | v2 的「切了再说」实测 5/5 误报; 但判据类别**不封闭** (R3-C-2: `exec` 类无标记仍需降级) ⇒ 承诺强度下调, 残余误报归转出 8 |
| 切分记号 | 顶层 `;` `&&` `\|\|` | `&`/换行各有实测反例; `\|\|` 排除会留一字符绕过 |
| 管道 | 不切 | 12 条 pattern 把 `\|` 编码进正则 |
| 判定顺序 | **先 pattern 后 credit** | 布尔等价 (R3 tech-lead 独立验证 306 条 0 不一致); 省 benign 负载 80~86% —— 但**不足以**解决最坏负载, 故须配 §4 |
| quote-aware | 必须 | 理由是**语义正确性** (切出不完整片段), 非「防安全回归」(R1 已证伪) |
| `has_filter` 13 处 subprocess | **本版重构为 bash 内建** (owner 2026-08-04 裁定) | 重排只在 benign 负载有效, 最坏负载 (= spec 自己推荐的迁移写法) +583%; 根治后性能不再依赖负载分布 |
| 数字口径 | 交付权威计数器 | 五次不一致的根治手段 |
| `guard:ack` | 命令级 | 段级会把已 ack 的复合命令由 0 变 2 (R2 实测); SC-12 锁定 |

## Impact

- 影响面: `secret-guard.sh` (降级检测 + 分段 + 判定重排 + 消息) + 测试 + 新增计数器。零 skill / 零 schema / 零跨仓。
- **覆盖率 (诚实声明)**: 仅修复**可安全分段**的复合命令。含块结构者 (`{ }` / `for…done` / `$()` / 反引号 / heredoc …) **维持现状泄漏** —— 非本版引入, 归转出 1/2/5。
- **迁移面 (口径见 §6)**: 305 条 `bash_case` 中 65 条含顶层边界记号 (49 拦 / 16 放行, 其中 15 纯管道 + **1** 真边界即 `KNOWN-LIMIT` 用例), 另 5 条纯换行边界 (4 拦 + `#152 FP: multiline benign` 放行) 因不切换行而零影响。
- 版本: PATCH → **v1.65.6** (SOT 现 1.65.5; **bump 前 re-check**, #170 已撞过一次并发)。
- **行为变更**: 可安全分段的 `a; b` / `a && b` / `a || b` 形态将开始被拦。CHANGELOG 须标注 + 给迁移写法 (逐段补 redirect) — Tasks 1.6 + SC-10。
- ship 同步面: aria 子模块 3 交付文件 + 5 版本文件 + 主仓 gitlink + VERSION + README badge (i18n B 档)。**不含** `.claude/scripts/` (已于主仓 `5fab5b8` 移除)。
- **验收环境**: 全部 SC 以 **canonical `aria/hooks/secret-guard.sh` 直调**为准 —— 本仓 plugin cache 停在 1.63.0 不含 v1.64/v1.65 修复 ([Aria#172](https://forgejo.10cg.pub/10CG/Aria/issues/172)), harness hook 链的行为**不可作验收证据**。
- 文档回填: `secret-hygiene.md` 自测计数 (现 366) — Tasks 1.7 + **SC-13** (R2 knowledge M-1: 上版只落 Task 无 SC)。
- 归档 spec **不回写** (本仓先例: 归档是「实际 ship 了什么」的历史记录); `2026-08-02-secret-guard-nomad-var-put-echo/` 的 `KNOWN-LIMIT` 表述失效仅在本 spec 与 CHANGELOG 记录。

## 转出 (ship 时逐条开 issue; **复现命令内联**, R2 knowledge M-2: 不得只引用未提交的审计报告)

1. **[架构, 高]** 跨段 pattern fail-open — `set -o posix; set | grep foo` (2→0); `set -o posix && set | grep buildid` 同。工作面 = 1 条 `.*` + **81** 条 `[^|]*` pattern 待逐条裁定。
2. **[缺陷, 高]** 块结构内的泄漏 — 本版降级为现状, 未修复。复现: `{ cat /opt/.env; echo x; } >/dev/null` / `for f in a b; do cat /opt/.env; done >/dev/null` / `( cat /opt/.env; echo x ) >/dev/null` 均 exit=0。需块结构解析。
3. **[缺陷, 中]** `ssh host '…'` / `sh -c '…'` 外壳逃逸 — 复现: `ssh h 'cat /opt/.env; true >/dev/null'` exit=0, 含 #170 形态的 ssh 版。需嵌套 shell 解析。
4. **[缺陷, 中]** `&` / 换行 两个切分记号 — `&` 与 `&>` `>&` `|&` `2>&1` 冲突 (复现: `cat /opt/.env &>/dev/null` 若切 `&` 则由 0 翻 2); 换行切碎 heredoc (复现: `cat <<EOF\nsecret\nEOF\nnomad var get x`)。
5. **[缺陷, 中]** `$(…)` / 反引号 / heredoc 内部的欠拦 — 本版降级为现状。复现: `` x=`cat /opt/.env; true >/dev/null` `` exit=0。
6. ~~**[性能]** `has_filter` 13 处转 bash 内建~~ — **已于 2026-08-04 由 owner 裁定拉回本 spec 范围** (见 §What.4), 不再转出。
7. **[运维, 中]** [Aria#172](https://forgejo.10cg.pub/10CG/Aria/issues/172) plugin cache 陈旧致仓内 dogfood 失真 (已立案)。
8. **[缺陷, 中]** fail-safe 判据**不封闭**的残余误报面 (R3-C-2) — 无块结构标记但仍不可安全分段的形态。已知实例: `exec >/dev/null; nomad var get x` (0→2)。根治需真正的 shell 语法解析; 本版只能枚举已知类。**新形态出现时应扩充 §What.1 判据表而非视为 SC 失败**。

## rule6_note

**Rule #6**: deterministic detector hook → structural fixture + unit-test corpus + dogfood (memory `feedback_deterministic_structural_skill_rule6_substitute`); 不走 `/skill-creator` AB (hook 非 capability skill)。框定与 owner 2026-08-02 对 `secret-guard-nomad-var-put-echo` 的裁定一致。

**substitute**: SC-1 (5 形态 baseline-failing) + SC-5 (分段器单元测试) + SC-6 (fail-safe 降级族) + SC-2/SC-3 (迁移回归锁)。

**dogfood 限制 (诚实声明)**: 因 Aria#172, 仓内 harness 跑 1.63.0, **不可用「我在本仓被拦/放行」作 dogfood 证据**; 由 canonical 直调的端到端脚本承担 (SC-9)。

## Tasks

- [ ] 1.1 `safe_to_split()` — 块字符 + 命令位置的块起始关键字 (引号外)
- [ ] 1.2 `split_top()` — quote/转义感知, 切顶层 `;` `&&` `||`; 空段跳过
- [ ] 1.3 判定循环: 降级分支 + 逐段 + **先 pattern 后 credit** + BLOCKED 消息补段落
- [ ] 1.3b **`has_filter` 13 处 `echo\|grep -qE` 逐条改 bash 内建 `[[ =~ ]]`** (owner 裁定拉回; 每处改后须验语义不变 — SC-15)
- [ ] 1.4 `corpus_census.py` 权威计数器 (随 spec 交付)
- [ ] 1.5 测试: 分段器单元 + fail-safe 降级族 + 端到端族 + `KNOWN-LIMIT` 转正
- [ ] 1.6 CHANGELOG 行为变更标注 + 迁移写法
- [ ] 1.7 `secret-hygiene.md` 计数回填
- [ ] 1.8 全量回归 (canonical 直调) + 性能相对基线实测
- [ ] 1.9 开转出 1-6 issue; 回填 #170 覆盖率声明; close #128

## Success Criteria

> 全部以 **canonical 直调**为准 (Aria#172)。

- [ ] SC-1 (baseline-failing, 核心): 5 条泄漏形态 (`;` ×3 / `&&` / `||`) **改前 exit=0, 改后 exit=2**。作者原型已验 5/5
- [ ] SC-2 (零影响回归锁, **逐条列名**): 15 条纯管道 + 5 条换行边界用例改前改后**均不变**
- [ ] SC-3 (拦截面不回归): **49** 条含边界的 `expected=2` 用例改后仍 exit=2; 任一转 0 = 安全回归
- [ ] SC-4 (quote-aware, **反事实可证伪** — R3-M-2 证原 3 条 fixture 在「引号盲实现」下 3/3 仍 exit=2, 被 fail-safe 吞掉): 改用 R3 tech-lead 验证过的 `perl -ne 'print if /a;b/' /opt/.env` —— 引号内含 `;` 且**无块结构标记**故不会走 fallback, 引号盲实现会把它切成两段而两段均不匹配 ⇒ **切错必 exit=0, 正确必 exit=2**。原三条降为辅助用例 (标注其零鉴别力)
- [ ] SC-5 (分段器单元测试, 数组基数断言): `a; b`→2 / `a && b`→2 / `a \|\| b`→2 / `a \| b`→**1** / `;` 在引号内→**1** / `\;` 转义→**1** / 换行→**1** / `a & b`→**1** / `a &> f`→**1** / `case x in a) ;; esac`→**2** (R3-M-3 机械核验: `split_top()` 直接按 `;` 切, `;;` 产生 2 段; 该命令由 `safe_to_split()` 在上层拦下, **两层职责不可混淆** —— 前一版写 →1 是把两层搞混了)
- [ ] SC-6 (fail-safe 降级族, **必须断言分支本身而非 exit code** — R3-M-1 + qa M-2 证 12 条里 5 条在「恒 fallback 的坏实现」下同样全绿, 因两路 exit 相同): 对每条**直接断言 `safe_to_split()` 的返回值** (fallback / split), 而非仅端到端 exit。12 条 = 10 条须 `safe_to_split=false` (`{ }` / `( )` / `for` / `while` / `if` / `[[ && ]]` / `for ((;;))` / 反引号 / `$()` / heredoc) + 2 条须 `safe_to_split=true` (`ls -la; pwd` / `cat /opt/.env; echo hi >/dev/null`)。**反事实**: 恒 fallback 实现 → 后 2 条红; 恒 split 实现 → 前 10 条红
- [ ] SC-7 (跨段 fail-open 锁现状, `KNOWN-LIMIT`): `set -o posix; set \| grep foo` **与 `set -o posix && set \| grep buildid`** 两形态改后均 exit=0 (R3-M-4: 前三版只锁 `;`, 只处理 `;` 的兜底实现即可让本 SC 假性转红), 标注「归转出 1; 转红 = 已收口」
- [ ] SC-8 (性能, **负载写死** — R3-C-3 指出前两版未定义负载致同一实现可在 +0% 与 +583% 间任选): 四档负载各跑 20 轮取中位数, 改前改后同机同会话对比 —— (a) 单条 benign; (b) 2 段全 benign; (c) 2 段全命中 pattern; (d) **3 段全命中 (= 迁移建议的写法)**。判据: **四档增幅均 ≤ 50%**。§What.4 的 13 处转内建是达标前提 (未做时 (d) 档实测 +583%); 实测数字须写进 spec
- [ ] SC-9 (dogfood): canonical 直调端到端脚本, 覆盖 5 类实际使用形态
- [ ] SC-10 (CHANGELOG): 含行为变更段 + ≥2 条迁移写法示例 (机械 grep)
- [ ] SC-11 (全量回归): `secret-guard.test.sh` 全绿 + 其余 5 脚本全绿; **总数注明 zsh 在场与否** (366 / 360)
- [ ] SC-12 (`guard:ack` 命令级锁定): 已 ack 的复合命令改后仍 exit=0 (防实现把 ack 下沉段级 — R2 实测下沉会由 0 变 2)
- [ ] SC-13 (SOT 计数回填断言): `secret-hygiene.md` 中 secret-guard 自测计数与实际测试数一致 (机械 grep 比对, R2 knowledge M-1)
- [ ] SC-14 (关键字**过度触发**方向, R3 code-reviewer M-2): `ls; echo for >/dev/null` / `ls; echo if >/dev/null` / `git commit -m "add case handling"` —— 三条须 `safe_to_split=true` **且** exit 与改前一致。前一版用 `echo done` 举例是错的 (`done` 不在关键字集内, 论证不成立), 真正的过度触发面此前无锁
- [ ] SC-15 (`has_filter` 13 处转内建**语义不变**, §What.4 的验收): 对每处 credit 判据构造 命中/不命中 各 1 条 fixture (共 26 条), 改前改后判定**逐条一致**。**反事实**: 任一处正则转写出错 → 该处 2 条中至少 1 条翻转
- [ ] SC-16 (正则 **POSIX ERE 可移植性**, R3 backend M-2): `safe_to_split()` 与 13 处转写后的正则**全部**在 bash `[[ =~ ]]` 下实跑验证, 断言不含 `(?:…)` / `\b` / `\s` 等 bash 不支持语法。**反事实**: 逐字搬运 Python 原型 → 静默失配 → SC-6 前 10 条全红
- [ ] SC-17 (语料重复用例清理, **连续三轮未处理**): 删除 `secret-guard.test.sh` 中字节级重复的 `bash_case "FP-fix timeout run-env"`, 并断言全文件无重复用例名

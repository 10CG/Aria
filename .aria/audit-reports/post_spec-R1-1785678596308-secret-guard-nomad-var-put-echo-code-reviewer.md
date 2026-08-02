---
verdict: CHANGES_REQUESTED
agent: code-reviewer
round: R1
critical_count: 0
major_count: 5
minor_count: 9
---

# post_spec R1 — secret-guard-nomad-var-put-echo (code-reviewer 视角)

**审计对象**: `/home/dev/Aria/openspec/changes/secret-guard-nomad-var-put-echo/proposal.md` (Level 2, 无实现代码 — 审 spec 自身代码级准确性)
**核实手段**: 全文读 `aria/hooks/secret-guard.sh` (689 行) + `aria/hooks/tests/secret-guard.test.sh` (737 行) + `aria/.claude-plugin/plugin.json`; 对 10 条命令形态**实跑现行 hook** 取真实 exit code; 实跑全量测试套件; 实查 `nomad --version` / `-out` help 原文。

---

## Phase 1 — 规范合规性 (spec 自洽 + 事实准确)

**判定**: PASS (无阻塞缺失; 结构完整: Why / What / 关键决策 / Impact / rule6_note / Tasks / SC 齐备)

---

## Phase 2 — 代码级准确性

### 已实测核实为**正确**的断言 (记录以免后轮重开)

| 断言 | 核实方式 | 结果 |
|------|---------|------|
| `secret-guard.sh:406` = nomad var get/nomad var list pattern | 读第 404-408 行 | ✅ 行号精确 |
| 「`put` 完全不在 risky_patterns 内」 | 全文 grep `put` — 140 条 pattern 中仅 output/input 等词内出现, 无命令 token | ✅ 真 |
| `put` 零拦截 | 实跑 5 形态 (`-in=json @file` / `KEY=v` / `-out=none` / `>/dev/null` / `2>/dev/null`) | ✅ 全 exit=0 |
| §Why 6 条 curl 写向形态的「现行 hook」列 | 逐条实跑 | ✅ 实测 `0,0,2,2,2,2` 与表格逐条一致 |
| nomad `-out` 默认值 help 原文 | `nomad var put --help` (本机 v1.11.2) | ✅ 逐字一致 |
| 「现有 /v1/var/ 用例全为读向」 | 全文 37 处 /v1/var/ 用例逐条看 + grep `PUT`/`-X ` | ✅ 真 (零写向) |
| 「6 条 curl 写向形态当前零测试锁定」 | 同上 | ✅ 真 |
| 版本 v1.65.2 | plugin.json SOT = `1.65.1` (已 ship, CHANGELOG `[1.65.1] - 2026-08-01`) → PATCH | ✅ 推导正确 |
| SC 编号连续性 | SC-1…SC-11 | ✅ 无缺漏/无重号 |
| 「`-out=none` 语境守卫」两处表述 | §What 第 2 点 vs 决策表第 3 行 | ✅ 一致 (均为「须同时命中 nomad var put」+ 同一「通用绕过词」理由) |
| `-out[=[:space:]]+none` 覆盖面 | ERE 推演 | ✅ 同时覆盖 `-out=none` / `-out none` / `--out=none`, 满足 SC-4 两写法 |
| SC-9 三条锚点可证伪性 | 实跑 | ✅ 现行即 exit=2 (vault/aws/gh pattern 命中), 写成全局 credit 会翻绿 → 锚点成立 |
| 决策表「复合命令是既有 has_filter 通病」 | 实跑 `cat /opt/.env; echo hi >/dev/null` | ✅ exit=0 — 通病论断为真, 非推测 |
| SC-11 前提 | `secret-scan.sh` 存在; hooks/tests/ 6 个测试脚本实跑 | ✅ 全 GREEN (baseline 干净) |

---

### Major (应修复 — 5)

**M-1. SC-1 内部算术自相矛盾 (6 vs 7), 且「3 条放行」只列出 2 个形态**
- 位置: `proposal.md:94` (SC-1) vs `:31-38` (§Why 表)
- §Why 表 = **2 放行** (`>/dev/null`, `-o /dev/null`) + **4 拦** (无 redirect / `-v` / `--trace-ascii` / `-d '{"Items"…}'`)。SC-1 却写「6 条 … 3 条放行 (`>/dev/null` / `-o /dev/null`) + 3 条拦 (无 redirect / `-v` / `--trace-ascii`) + `-d` 拦」= 声称 6 但分解求和 = 7, 且「3 条放行」后面只给了 2 个形态。
- 为何重要: SC-1 是**改前即须 PASS 的回归锁**, 计数错会让实施者写出数量不符的用例族并在 §What 第 3 点「共 10 条」处继续放大 (见 M-2)。
- 修法: 改为「2 条放行 + 4 条拦」。

**M-2. 交付物计数「10 条」与 SC 集合实需 (≈17-18 条) 矛盾**
- 位置: `:46` (§What 第 3 点「共 10 条」) / `:60` (Key Deliverables「10 条写向用例族」) / `:101` (SC-8「新增 10」)
- 按 SC 逐条数新增用例: SC-1(6) + SC-2(1) + SC-3(1) + SC-4(**2**: `-out=none` 与 `-out none`) + SC-5(**2**: `>/dev/null`→0, `2>/dev/null`→2) + SC-6(**2**, 其中 nomad var list 全文无既有用例 = 新增) + SC-7(1) + SC-9(**3**) + SC-10(1) ≈ **18** (若 SC-6 的 get 复用 test L55 则 17)。§What 表只列 4 条 put 形态, 与 SC-4/5/6/9/10 需要的 9+ 条 nomad 侧用例对不上。
- 为何重要: 实施者按「10 条」收工会漏掉 SC-9 (语境守卫锚点) / SC-10 (已知限制锁) 的用例, 而这两条正是本 spec 唯一的安全性证伪手段。
- 修法: 把 §What 第 3 点 / Key Deliverables / SC-8 的数字统一改为按 SC 推导的实际值, 或明确写「≥N 条, 以 SC-1…SC-10 为准」。

**M-3. SC-4 缺机制断言 → 可假绿; `-out=json|table|hcl` 无任何 SC 钉住必须拦**
- 位置: `:97` (SC-4)
- SC-4 只断言 `nomad var put -out=none …` exit=0。若实施者把 pattern 写成在 flag-first argv 形态下根本不匹配的形式 (例如 `nomad[[:space:]]+var[[:space:]]+put[[:space:]]+[^-]`), SC-4 依然 exit=0 **通过** —— 通过原因是「pattern 压根没命中」而非「语境守卫生效」。这与 memory `feedback_noop_in_test_env_hardening_needs_mechanism_assertion` 描述的循环论证同型。
- 实测佐证: 现行代码下 `nomad var put -out=json …` / `-out=table …` 均 exit=0 (零覆盖), 改后**必须**变 exit=2 (这两档都会渲染含解密 Items 的变量), 但 SC 集合无一条覆盖。
- 修法: 加一条对照 SC —— `nomad var put -out=json <path> KEY=v` 与 `-out=table …` **必 exit=2**。它同时充当 SC-4 的机制断言 (证明 pattern 在同一 argv 形态下确实会 fire, 只有 `none` 换来 credit)。

**M-4. 新 pattern 的误拦 (FP) 面无任何 SC 覆盖, 且背离 #69 先例**
- 位置: `:44` (§What 第 1 点) / `:78` (§Impact 风险段)
- §Impact 只提到一种 FP: 「运维脚本里合法但无 redirect 的 nomad var put」。但**实测**现行同类 pattern 的真实 FP 面要宽得多 —— 以下三条当前全 exit=2:
  - `grep -rn 'nomad var get' aria/hooks/`
  - `echo "run nomad var get <path> to inspect"`
  - `git commit -m "docs: describe nomad var get usage"`
  加了 put pattern 后, 「文档里提到 / grep 搜索 nomad var put」的命令一并被拦 —— **包括本 spec 实施者自己**执行 `grep -n 'nomad var put' aria/hooks/secret-guard.sh` 时 (本次审计已被实际拦到一次, 属同一形态)。
- 先例背离: `#69` 那轮为同一文件显式建了 FP 守卫用例族 (test `:568-579`, 如 `#69 FP: grep X-Vault-Token in docs` / `#69 FP: hvs. benign short id`), 正是为了防这类「文档提及即误拦」。本 spec 无对应 SC。
- 修法 (二选一): (a) 加 FP-guard SC + 用例, 并按 #69 的做法收紧 pattern (例如要求 put 后跟真实路径 argv 形态); 或 (b) 在决策表**显式接受**该 FP 并说明它继承自既有 get/list 同类行为 (实测已成立) —— 但不能像现在这样在风险段只写一半。

**M-5. SC-10 只钉住该已知限制**最轻**的形态, 低估其严重度**
- 位置: `:103` (SC-10) / `:68` (决策表「残余已知限制」)
- SC-10 选的例子是同类复合 (`nomad var get a && nomad var put -out=none b`) —— 泄漏面仅限 nomad 变量。但 credit 是**命令级全局**的 (实测 `cat /opt/.env; echo hi >/dev/null` → exit=0), 所以加了 put 语境 credit 后, **跨类**形态 `cat /opt/.env; nomad var put -out=none x KEY=1` 同样整体放行 —— 这才是该限制的最高严重度表现 (一个无关的 put 子句可为任意 secret 读取解锁)。
- 为何重要: 决策表用「所有 credit 皆然」为它辩护 (该论断已实测为真, 无异议), 但用最轻例子做「显式记录」会让后来者低估被接受的风险面; 若将来收口, 红灯也只覆盖轻形态。
- 修法: SC-10 补一条跨类 `KNOWN-LIMIT` 用例 (读 .env + put `-out=none` 同命令), `expected=0` 锁现状。

---

### Minor (建议修复 — 9)

**m-1. SC-8「既有 ~50 用例」实为 347** (`:101`)。实跑 `bash aria/hooks/tests/secret-guard.test.sh` → `PASS: 347 / 347`。数字继承自测试文件 L8 的过期注释 (`Coverage: ~50 cases`), 差约 7 倍。建议写实测值或「全量套件」。

**m-2.「既有 ~100 条 pattern 架构」实为 140 条** (`:67` 决策表)。同样继承自 `secret-guard.sh:8` 的过期自述。不影响决策 (「与既有架构一致」的理由成立)。

**m-3. 文件头引用 `L14-24` 略偏** (`:69` 决策表 credit 串伪造行)。核实: 「speed-bump」自述在 **L7** (`L6-13` = What this hook IS); `L14-25` 才是完整的 "What this hook is NOT" (L14-24 把最后一个 bullet 截在半句); threat model 整块 = `L4-44`。**实质无误** —— 引用想指的「shell quoting tricks 绕过属可接受边界」确在 L16-18。建议改引 `L4-44` 或 `L6-25`。

**m-4. `tests/secret-guard.test.sh:56-59` 引用范围偏窄** (`:40`)。该 4 行行号精确且确为读向 (curl GET ×3 + wget ×1), 但全文 /v1/var/ 用例共 **37 处** (L56–L418)。用 `:56-59` 支撑「全为读向」会让读者以为只有 4 条。实质断言 (全部读向、零写向) 经全文核实**为真**。建议改写为「全文 37 处 /v1/var/ 用例 (L56–L418) 全为读向」。

**m-5. SC-5 措辞「既有 credit 仍生效」不成立 (真空)** (`:98`)。现状下 nomad var put 不命中任何 pattern, 改前 exit=0 是**真空成立**, 不存在「既有 credit」可回归。其后半 (`2>/dev/null` → exit=2) 实测改前为 exit=0, 属**新增 block 行为 = baseline-failing**, 却既未计入 §What 第 3 点的「新增中的 block 类」, 也未进 rule6_note 的 substitute 名单 (只点了 SC-2/SC-3)。建议改名为「credit 语义与 R2-C-10 对齐」并把 `2>/dev/null` 归入 baseline-failing 集。

**m-6. SC-6「读向不回归」对 nomad var list 不成立** (`:99`)。nomad var get 已有用例 (test `:55`), 但 nomad var list 全文**无**用例 → 它是新增覆盖而非回归锁。措辞小改即可。

**m-7. rule6_note 措辞与同文件先例不一致** (`:84`)。先例 `openspec/archive/2026-06-19-secret-guard-exfil-coverage-iteration/proposal.md:9` 对**同一个 hook** 的处置是「deterministic detector skill → structural fixture + unit test corpus + dogfood; **不**走 /skill-creator AB (hook 非 capability skill)」, 引 memory `feedback_deterministic_structural_skill_rule6_substitute`。本 spec 改用「Rule #6 **不适用** (结构性前提不成立)」—— 后者是 Rule #10 闸门豁免白名单的用语, 语气比先例的 substitute 强一档。**实质产出一致** (确实给了 SC-2/SC-3 baseline-failing substitute, 符合判据表首行), 但建议对齐先例措辞 + 引 canonical memory, 避免被读成 AI 自行豁免 enabled 闸门。

**m-8. §Impact issue 收尾段自相张力** (`:80`)。「ship 后 #170 发 close comment + PATCH state」与紧随其后的「关 issue 前须与 owner 确认是否分拆」互相冲突。建议改条件式 (「若 owner 确认要求 1 分拆 → 再 close; 否则只发进展 comment 保持 open」)。

**m-9. 已核销的非问题 (记录以防后轮重开)**: `nomad -address=… var put …` **不**构成 pattern 绕过 —— 实测 Nomad CLI 直接拒绝 subcommand 前置 flag (`Invalid flags before the subcommand`), 故 `nomad[[:space:]]+var[[:space:]]+put` 的 token 邻接假设是安全的。

---

### 建议 (Recommendations)

1. **补一条「-out 全档位分区」SC** — `none` 唯一放行, `json|hcl|table|go-template` 全拦。这同时解决 M-3 的假绿口子, 且把 credit 判据变成可穷举证明的分区 (对齐 memory `feedback_predicate_tiers_need_total_partition_proof`)。
2. **SC-7 需防自匹配假绿** — BLOCKED heredoc 末尾会回显 `Command was: $command`, 若触发用例本身含 `-out=none` 字样, grep 会命中命令回显而非文案。SC-7 应显式要求触发命令**不含** `-out=none` (例如用 SC-3 的 `KEY=<value>` 形态触发)。另: 既有 `run_case` 丢弃 stderr, SC-7 需新 helper (可仿 test `:292-299` 的 `stderr_r4c1` 写法)。
3. **Tasks 粒度** — 1.1 把 pattern / credit / 文案三处合成一条, 与 SC-2/SC-3/SC-7 的三条独立验收对不齐; 建议拆成 1.1a/1.1b/1.1c 便于 baseline-failing 逐条留证。

---

### 评估

**是否可以继续?**: 需要修复 (M-1…M-5) 后进 Phase B
**理由**: spec 的**事实底座是扎实的** —— 全部代码引用、行号、6 形态实测表、nomad help 原文、版本推导逐项核实无误, 且核心机制 (put pattern + 语境守卫 credit) 在实跑验证下成立。阻碍在于**计数与验收面**: 用例数三处自相矛盾 (M-1/M-2), 安全形态的验收缺机制断言可假绿 (M-3), 新增拦截面的 FP 未按本文件既有 #69 先例建守卫 (M-4), 已知限制记录选了最轻形态 (M-5)。这四类都是改文档即可闭合、但若带进 Phase B 会直接生成弱测试集的问题。

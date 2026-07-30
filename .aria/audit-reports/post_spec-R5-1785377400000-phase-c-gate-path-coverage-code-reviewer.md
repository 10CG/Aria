# post_spec R5 (定向) — code-reviewer

**verdict**: REVISE
**scope_ok**: true
**counts**: critical=2 major=4 minor=4

**审计对象**: `openspec/changes/phase-c-gate-path-coverage-not-applicable/proposal.md` A1 修订
(主审 `:51`/`:151`/`:201` [D14 `-z`] · `:63`/`:149`/`:202` [D12 位置式] · `:65`/`:150`/`:203` [D13 `---`] · `:155`/`:204` [AB 三处勘正]; 必审 A1 与 §0 契约 / §1 8 条规则 / reason 封闭集一致性)

**视角**: 欠定检测 —— 「两个独立实现者拿这份规格会写出同一份代码吗」。

**实测基座** (本轮所有证据均在本机复现, 非推断):
- `git diff --name-only master...feat` (default quotePath) → `"skills/\346\265\213\350\257\225/x.py"` (八进制+双引号) ✓ D14 前提成立
- `git diff --name-only -z` → `c d.txt\0skills/测试/x.py\0` (**含尾随 NUL**) ✓ ; 空 diff `-z` 输出 = **0 字节**
- `git -c core.quotePath=false diff --name-only` (无 `-z`) → `skills/测试/x.py` **未转义** ← MAJOR-3 的红窗证据
- `ab-suite/phase-c-integrator.json` = 3 evals (commit-generation / merge-conflict-handling / multi-remote-merge-push) ✓ 勘正 #1 属实
- `ab-results/latest` → `2026-05-13-state-scanner-issue-101-fix`; 最近归档 `2026-07-20-v1.62.0-phase4-rule6` 的 `skill_name` = `state-scanner` ✓ 勘正 #2 **两半均属实**
- 基线 `benchmark.json`: `structural_metrics` 恰 8 项, `measured` 全为 `int 100`, `unit:"percent"`; `primary_pass_gate.measured == "100%"` (str) ✓ 勘正 #3 属实

---

## Findings

### [CRITICAL] D12 的「区间」在本 Spec 里是无定义悬空词 — L 的作用域子句没被并进来, 承重算法缺一个自由变量

- **位置**: `proposal.md:63` (D12 正文) / `:149` (D14 表行) / `:202` (SC-30); 对照 `openspec/changes/phase-c-integrator-ci-path-coverage/proposal.md:182`
- **问题**: `:63` 原文第一句是「对**区间内**每一行, 先剥行尾 `#` 注释 ...」。全文 `grep 区间|子树|作用域|缩进` 只有两处命中: `:63` 本句, 和 `:202` SC-30 里的「落在 `on:` 子树内」(一条 fixture 摆放要求, 不是规范条款)。**本 Spec 没有任何一条正文定义这个区间**。这是并入时的截断: L 侧 `:182` 写的是「构造扫描 (`&anchor`/`*alias`/`<<`/`!tag`) **只在 `on:` 键行到 `on:` 块结束的行区间内进行** (区间由规则 1/5 已算出), **且跳过纯注释行**」, 而 A1 只搬了紧接其后的 `:184` 命中判据句 —— 连「区间」这个指代词一起搬了过来, 但它的先行词留在了 L。L 侧 `:185` 甚至专门解释过区间为什么承重 (「R3 把作用域从全文件收窄到 `on:` 块, 但区间内恰好就是 `paths:` 通配模式所在处」)。
- **证据**:
  - **全文件扫描在本仓真实语料上立刻炸**: `.forgejo/workflows/submodule-gate-tripwire.yml:122/123/124/129/133` 是 `run: |` 块体里的 markdown 正文 (不是注释), 形如 `          **Detected at**: $(date -u +"%Y-%m-%dT%H:%M:%SZ")`。走 `:63` 的预处理: 无 `#` → strip → 无 `- ` → 首尾非成对引号 → 键位 = `**Detected at**` → **首字符 `*` ⇒ 命中** (5 行)。这份文件正是 SC-23 要冻结的「主仓 3 workflow 联合语料」之一。
  - **两实现者构造 (都过全部 SC-1~SC-31, 结论相反)**: 输入 X =
    ```yaml
    name: x
    on:
      push:
        paths: ['docs/**']
    jobs:
      build:
        <<: *defaults
    ```
    changed_files = `['src/a.py']`。
    实现者 A (读 SC-30 的暗示, 区间 = `on:` 子树): `<<` 在区间外 → 该 workflow 零覆盖贡献 → 整体 **`not_applicable`** → gate **跳过 (a) PR CI 等待**。
    实现者 B (先按字面全文件扫, 被 SC-23 打红后只收窄到「跳过注释行 + 跳过 `run:` 块体」): `jobs.build` 的 `<<` 命中 → 该 workflow 构造级 `covered` → 整体 **`covered`** → gate **照常 wait**。
    同一输入, 一个 skip 一个 wait —— 正是 memory `feedback_spec_underdetermination_two_implementer_test` 的 16/16 vs 11/17 形状。
  - 注意 SC-23 只惩罚**最宽**的那一版, 不裁决收窄到哪一档; 收窄区间的**下界与上界都没有规范约束**。
- **建议修法**: 在 `:63` 之前 (或 `:57` 触发子集解析 bullet 内) 逐字补 L `:182` 的作用域条款, 且必须连带补 L `:160` 的 `on:` 键识别条款 (「接受 `on:` / `"on":` / `'on':`, **且必须是列 0 的文档顶层键**」—— 否则 `run: |` 块体里的 shell 行出现 `on: ...` 会把区间开在错的地方, 区间条款自己就悬空):
  > 构造级扫描区间 = 从列 0 顶层 `on:` 键行起, 到下一个列 0 非空非注释行 (或 EOF) 前一行止; 区间外的任何行 (含 `jobs:` / `env:` / `run:` 块体 / 文件头注释) 一律不参与构造级命中判定。
  并在 SC-30 增一条负控 (iv):「`<<: *defaults` 只出现在 `jobs:` 子树 → **不**触发」——这条才是能把 A/B 分开的判别式。

---

### [CRITICAL] 「剥引号」排在首字符判定之前 ⇒ 以 `*` 开头的 glob (`- '**.md'` / `- '**'`) 被判成 alias ⇒ 该 workflow 恒 covered ⇒ D12 要治的恒 wait 原样复发; SC-30 三条负控结构上抓不到

- **位置**: `proposal.md:63` (预处理顺序 + 判据) / `:149` (D12 表行) / `:202` (SC-30 三条负控) / `:64` (「位置式读法 4/4 零命中」的实跑引用)
- **问题**: `:63` 规定的顺序是「剥注释 → strip → 剥块序列标记 `- ` → **剥成对首尾引号** → 然后判首字符 ∈ {`&`,`*`,`!`}」。把引号先剥掉再看首字符, 等于把**带引号的字符串**和**裸 alias/anchor/tag** 混为一谈。而 YAML 语义上二者永不可能混淆: **加了引号的标量永远是字符串, 不可能是 anchor/alias/tag/merge key**。顺序反了。
  后果: 一条极常见的 paths 写法 `- '**.md'` 走完预处理变成 `**.md`, 首字符 `*` ⇒ **命中构造级不确定** ⇒ 该 workflow 判 `covered` ⇒ 只要仓里有一份用 `**`/`*` 打头 pattern 的 workflow, **任何变更都 covered** ⇒ 恒 wait。这正是 `:64` 自己引用 L 侧实跑时描述的病 (「把病从假绿搬到恒红, 按本 Spec §Why 自己的判据同样零信息量」), 只是触发条件从「所有带 paths 的 workflow」缩到了「pattern 以 `*` 开头的 workflow」。
- **证据**:
  - **逐字符走一遍**: 行 `      - '**.md'` → 剥注释(无) → strip → `- '**.md'` → 剥 `- ` → `'**.md'` → 剥成对引号 → `**.md` → 值首字符 `*` → **命中**。同理 `- '**'` (匹配全部)、`- '*.md'`、`- '**/*.py'` 全部命中。GHA/forgejo 官方 paths 示例里 `'**.js'` / `'**'` / `'**.md'` 是标准写法。
  - **SC-30 为什么抓不到**: `:202` 三条负控是 (i) `run: |` 块体 (ii) 注释里 (iii) **`paths: ['a/**']`** —— 全部用**非 `*` 开头**的 pattern。本仓 4/4 真实语料同样是非 `*` 开头 (`- 'skills/issue-triage/**'` / `- 'aria/skills/issue-triage/**'` / `- 'aria-orchestrator/docker/aria-runner/**'`), 所以 `:64` 的「位置式读法 4/4 零命中」是真的、但**不能外推**: 它证明的是「本仓这四条 pattern 首字符恰好是字母」, 不是「位置式判据对 glob 免疫」。规范承诺的是给采用者用的算法, 语料只有四条且同形。
  - **两实现者构造**: 输入 = `paths:\n  - '**.md'`, changed_files = `['README.md']`。
    实现者 A (照字面: 先剥引号再判): 构造级命中 → workflow `covered` → 整体 `covered` → wait (且 `matched_workflows` 会把它当成「trigger matched」列出去, 见 MAJOR-2)。
    实现者 B (按 YAML 语义: 引号标量不可能是 alias, 故剥引号即否决): 不命中 → 走正常 glob 匹配 → `README.md` 命中 `**.md` → `covered`, reason 诚实。
    换 changed_files = `['src/a.py']`: A 仍 `covered` (恒 wait), B 得 `not_applicable` (机制生效)。**同一 workflow、同一输入, 结论相反, 且 A 的那一档就是本 Spec 立项要消灭的形态。**
- **建议修法**: 把「剥成对首尾引号」从**预处理步**改成**判据的否决位**, 并在 `:63` 写死:
  > 若该 token 存在成对首尾引号 (单/双), 则它是引号标量 ⇒ **直接判不命中**, 不再做首字符判定; 首字符判定只施加于**未加引号**的 token。
  (裸 `- *alias` 仍命中 ✓; 裸 `- **.md` 在 YAML 里本就是 alias 形态, 命中也正确 ✓。)
  SC-30 增负控 (iv):「`paths:` 下 `- '**.md'` 与 `- '**'` → **不**触发」, 并把 `:64` 的「4/4 零命中」措辞补上适用范围 (「对本仓四条非 `*` 开头 pattern」)。

---

### [MAJOR] D13 的扫描区间 + 「内容行」边界全未定义: `---` 自身算不算内容行 / 连续两个 `---` / `%YAML` 指令 / 精确匹配形态 —— 四个分叉点, SC-31 只钉了其中最简单的一种

- **位置**: `proposal.md:65` (D13 正文) / `:150` (D13 表行) / `:203` (SC-31)
- **问题**: `:65` 原文「列 0 的 `---` 出现在**首个非空非注释内容行之后**才是多文档分隔 ⇒ 按构造级不确定判 `covered`; 出现在其**之前**是 YAML 文档起始标记 ⇒ **忽略**」。四个承重细节缺失:
  1. **扫描区间**: D12 (若按 CRITICAL-1 补上) 是 `on:` 子树, 但 `---` 是**文档级**构造, 必须全文件列 0 扫 —— L 侧 `:190` 明写「`---` 是文档级构造, 把实现者往「全文件扫」推」。本 Spec 两处都没写区间, 实现者极可能复用 D12 的区间。
  2. **`---` 自身算不算「内容行」**: `:65` 用「首个非空非注释内容行」做锚, 但没说 `---` 本身是否计入。
  3. **`%YAML 1.2` 指令行算不算内容行**。
  4. **匹配形态**: `line == "---"` 还是 `line.startswith("---")`? `--- # foo` / `----` / `--- !!map` 各归哪档?
- **证据**:
  - **区间分叉 (方向是 fail-OPEN, 更危险)**: 文件 = `on:` 块正常 + 其后 `jobs:` 之前有一个列 0 `---` + 第二文档另有一套 `on:`。实现者 A (复用 `on:` 区间) 永远看不到那个 `---` → 只按第一文档判 → 若第一文档 paths 不命中就出 **`not_applicable`** (跳过 (a)), 而第二文档的 `on:` 可能是无 paths 的 push (真覆盖) ⇒ **假 not_applicable**, 违反 D2「绝不把解析不了当无覆盖」。实现者 B (全文件列 0 扫) → `covered`。相反结论, 且 A 落在 §What 核心原则明令禁止的方向。
  - **「内容行」分叉**: 输入 = `# c` / `---` / `---` / `on: push`。
    实现者 A (`---` 计入内容行): 第 1 个 `---` 就是首个内容行 → 它不在「之后」→ 忽略; 第 2 个在其后 → **`covered`** ✓ (真值: 两个 `---` = 空首文档 + 第二文档, 确实是多文档)。
    实现者 B (`---` 不计入内容行): 首个内容行是 `on: push`, 两个 `---` 都在它**之前** → **两个都忽略** → 不判构造级 → 直接按第一 (空) 文档解析 ⇒ 漏判多文档。
    **SC-31 只有 (a) 单个首行 `---` 和 (b) 单个内容行之后的 `---`, 连续 `---` 不在其中 ⇒ A/B 全绿而结论相反。**
  - **`%YAML` 分叉**: `%YAML 1.2` / `---` / `on: push`。字面读法把 `%YAML 1.2` 当作「非空非注释内容行」⇒ 其后的 `---` 判多文档 ⇒ 该 workflow 恒 covered ⇒ 恒 wait。这与 `:66` 自己援引的 yamllint `document-start` 用户群高度重叠 (写指令行的和写 `---` 的是同一批人)。
  - (作为对照, A1 的「**列 0**」限定词是有效的: 已实测 `build-aria-runner.yaml:97/:99` 的 `echo "--- image size ---"` 有 10 空格缩进, 不触发 —— L 侧 R3 踩的那个坑本 Spec 已避开。)
- **建议修法**: `:65` 改成四条可直译规则:
  > (1) 扫描区间 = **全文件**, 只看列 0; (2) `---` 行**自身不计入**「内容行」, `%YAML`/`%TAG` 指令行同样不计入; (3) 判据等价写法: 列 0 的 `---` 出现 **≥2 次** ⇒ 多文档 ⇒ 构造级 `covered`; **恰 1 次且其前无内容行** ⇒ 文档起始标记 ⇒ 忽略; **恰 1 次且其前有内容行** ⇒ 多文档 ⇒ `covered`; (4) 匹配形态 = 行去尾空白后等于 `---`, 或以 `--- ` / `---\t` 开头 (YAML 要求 `---` 后为空白或 EOL); `----` 及更多连字符**不算**。
  SC-31 增 (c)「连续两个列 0 `---` → `covered`」与 (d)「`%YAML 1.2` + `---` + paths 命中 → `covered`, reason=`workflow-trigger-matched` (**不得**判构造级)」。

---

### [MAJOR] A1 大幅扩张了「构造级 covered」的产出面, 但 reason 封闭集里没有它的槽位 —— 这类 covered 会被上报成 `workflow-trigger-matched` (事实错误) 且对 D9 surface 完全隐形, 恰好把 CRITICAL-2 变成静默失败

- **位置**: `proposal.md:63`/`:65` (D12/D13 产出构造级 covered) × `:76` (规则 6) × `:79` (7 条 reason 封闭集) × `:106` (D9 surface 义务) × `:178` SC-6 / `:203` SC-31(b)
- **问题**: `:76` 规则 6 是「任一解析成功的 workflow 判 covered → 整体 `covered`, reason=`workflow-trigger-matched` (+ `matched_workflows` 列全)」。`:79` 把 reason 钉成 7 条封闭集, 里面**没有**表达「因构造不可辨识而退回 covered」的字面值。于是 D12/D13/`paths-ignore` 产生的构造级 covered 只能挤进 `workflow-trigger-matched` —— 而它**没有任何 trigger 被 matched**, `matched_workflows` 还会把这份 workflow 列出去, 等于对调用方说谎。同时 `:106` 的 D9 surface 义务只覆盖 `unknown` 一档 ⇒ 构造级降级在报文上**完全不可见**。
  这不是纯洁癖: CRITICAL-2 的 `- '**.md'` 恒命中之所以会长期潜伏, 正是因为它对外表现为「trigger matched, 这份 workflow 覆盖了你的变更」—— 与真覆盖逐字段同形, 运维面无从分辨。本 Spec `:106` 自己写过「防评估器自身静默失效 (与本 spec 批评的『零信息量→被忽略』同病, 不能换个位置复发)」, 这里就是换了个位置复发。
- **证据**:
  - **原文互斥**: `:79` 声明 7 条 reason「全部可断言」构成封闭集 ⇔ `:178` SC-6 (`paths-ignore` 在场 → 「`covered` (per-workflow 档)」) 和 `:203` SC-31(b) (「按构造级不确定判 `covered` (per-workflow 档)」) **都不写 reason**。封闭集若真闭合, 这两条 SC 必然能写出 reason; 写不出正说明该态在封闭集里无家。
  - **三实现者**: A 复用 `workflow-trigger-matched` + 把 workflow 列进 `matched_workflows`; B 复用 reason 但 `matched_workflows=[]`; C 新增第 8 条 `workflow-construct-uncertain` (违反 `:79` 的封闭集断言, 会打红任何按 `:79` 写的封闭集测试)。三者全过 SC-6/SC-31(b) (二者不约束 reason), 但 `path_coverage` 输出三种形状 —— 而 `path_coverage` 是要进 gate 输出给 AI 读的契约字段 (`:96`)。
- **建议修法**: 二选一, 写死在 `:76`/`:79`, 并同步 D9:
  - (a) **保封闭集**: 明确构造级 covered 复用 `workflow-trigger-matched`, 但**不得**进 `matched_workflows`; `path_coverage` 增 additive 键 `degraded_workflows: [str]`; `:106` D9 的 surface 义务扩到「`degraded_workflows` 非空时也出警告行, 注明『N 份 workflow 因不可辨识构造退回 covered』」。
  - (b) **扩封闭集到 8 条**: 增 `workflow-construct-uncertain`, 同步改 `:79` 的「产生终态判定的 7 条」计数措辞、给 SC-6/SC-31(b) 补 reason 断言、并把 D9 覆盖到该 reason。
  无论选哪条, SC-6 与 SC-31(b) 必须钉 reason —— 否则本条的分叉在测试面永远不可见。

---

### [MAJOR] SC-29(a) 的「可红」依赖一个未钉死的外部 git 配置 (`core.quotePath`); 在中文开发者的常见配置下, **不带 `-z` 的实现同样绿** ⇒ 该 SC 无法证明 `-z` 生效

- **位置**: `proposal.md:201` (SC-29(a), 「两子用例各自可红」) / `:51` (D14 前提陈述) / `:151`
- **问题**: SC-29(a) 的红窗前提是「无 `-z` 时该路径被八进制转义恒不匹配」。但八进制转义**不是 `-z` 的对偶**, 它由 `core.quotePath` 控制, 而 `core.quotePath` 是**用户/全局可配的**, 且「处理中文文件名就把它关掉」是中文开发者的标准做法 (本项目 owner 即中文环境)。fixture 若不显式钉死该配置, 它会继承 `~/.gitconfig` / `/etc/gitconfig`。
- **证据** (本机实测, 同一仓同一 diff):
  ```
  $ git diff --name-only master...feat            # quotePath 默认 (true)
  "skills/\346\265\213\350\257\225/x.py"
  $ git -c core.quotePath=false diff --name-only master...feat   # 无 -z
  skills/测试/x.py
  ```
  ⇒ 在 `core.quotePath=false` 的机器上, 一个**完全没有 `-z`** 的实现照样输出未转义路径 → 照样命中 paths → SC-29(a) 返回 `covered` → **绿**。「证 `-z` 生效」不成立, 红窗消失 (memory `feedback_test_asserts_what_its_name_claims`: 该测试怎么会红?)。
  两实现者: A 在默认配置机器上写 `-z`, SC-29(a) 红→绿, 以为锁住了; B 在 `quotePath=false` 机器上**忘了 `-z`**, SC-29(a) 一次都没红过, 同样交付 —— B 上生产后遇到任何 quotePath 默认为 true 的环境 (CI/新机器) 即产生假 `not_applicable`。
- **建议修法**: SC-29(a) 补两条前置并写进 SC 正文:
  > fixture 仓建仓后显式 `git config core.quotePath true`; 对照臂 (无 `-z`) 与被测臂 (有 `-z`) 在**同一 fixture 仓、同一 quotePath=true** 下比对, 断言对照臂返回 `not_applicable` 而被测臂返回 `covered`。
  另建议在 `:51`/`:69` 的生产命令上追加 `-c core.quotePath=false` 作二重保险 (与 `-z` 正交, 成本为零; 若他日有人误删 `-z`, 这一层仍挡住转义面)。

---

### [MAJOR] SC-32 三条断言里两条没有可计算的主体 (仓内不存在「解析套件路径」的代码), 且它被放在一个 `run_all_tests.sh` 扫不到的目录 ⇒ 大概率写成恒真断言 + 永不执行

- **位置**: `proposal.md:204` (SC-32) / `:226` (Impact: 落 `aria-plugin-benchmarks/`) / `:234` (测试基线把 SC-32 计进 phase-c 的 ~120+)
- **问题**:
  1. **无主体**: SC-32 第一条是「**解析出的**套件路径 == `ab-suite/phase-c-integrator-pre-merge-gate.json`」。仓内没有任何代码做这个解析: `aria-plugin-benchmarks/runner/run_benchmarks.py` 只从 config dict 取 `skill_name` (`:300` 起), 不做 ab-suite 路径解析; `aria/skills/` 下**不存在 skill-creator** (`find` 零命中, 它是 CC 侧的 plugin); 真正的解析流程是 `AB_TEST_OPERATIONS.md:206`「读取 `{skill}/evals/evals.json` (或 `ab-suite/{skill}.json`)」——**一句散文, 由人/AI 执行**。左值不存在, 断言就无从写起。
  2. **无 runner**: `:226` 把 SC-32 放 `aria-plugin-benchmarks/`, 但 `:234` 声明的绿门是 `run_all_tests.sh`, 该脚本 `:48` 是 `for tests_dir in $(find "$SKILLS_DIR" -type d -name tests | sort)` —— 只扫 `aria/skills/*/tests`。放在 `aria-plugin-benchmarks/` 的断言**永远不会被这道门执行**。且 `:234` 把 SC-32 计进 phase-c 测试基线增量, 与 `:226` 的落点自相矛盾。
- **证据**:
  - **三实现者**: A 写 `assert SUITE_PATH == "ab-suite/phase-c-integrator-pre-merge-gate.json"` (自定义常量对字面量, **恒真, 零信息** —— 与同一张表第 3 行自己警告的 `dict == str` 恒假是同一枚硬币的两面); B 写 `assert Path("ab-suite/phase-c-integrator-pre-merge-gate.json").exists()` (只验存在, 抓不到「误用 parent 套件」这个真陷阱); C 去 parse `AB_TEST_OPERATIONS.md`。三者都自称实现了 SC-32。
  - 基线路径那条同理: 「基线路径 == 写死的 `2026-05-10-.../benchmark.json`」也是常量对常量。
  - 只有第三条 (`structural_metrics.*.measured` 是 int) 有真主体 —— 它可以断在**已提交的基线文件**上。已实测该文件恰 8 项、`measured` 全为 `int 100`、`primary_pass_gate.measured == "100%"` (str), 所以这条能真红真绿。
- **建议修法**: 把 SC-32 重写成**对仓内既有文件的可执行断言**, 并落到 `aria/skills/phase-c-integrator/tests/` 下 (才进 `run_all_tests.sh`):
  > (1) `ab-suite/phase-c-integrator.json` 与 `ab-suite/phase-c-integrator-pre-merge-gate.json` 是两份**不同**套件, 且前者 `evals` 的 3 个 id 为 commit-generation/merge-conflict-handling/multi-remote-merge-push (即「裸名会命中无关 parent」这一事实本身被冻结成测试, 未来 parent 内容变了会红);
  > (2) `ab-results/2026-05-10-phase-c-integrator-pre-merge-gate/benchmark.json` 存在, 且 `latest` symlink **不**指向它 (把「不能用 latest」冻结成断言);
  > (3) 该 baseline 的 8 个 `structural_metrics.*.measured` 全部 `isinstance(int)` 且 `primary_pass_gate.measured` 为 `str`。
  同时把 `:226` 与 `:234` 的落点表述改一致。

---

### [MINOR] §0 `:48` 的 gitlink 条款仍写 `git diff --name-only` (无 `-z`/`--no-renames`) — 全文四处 `git diff` 命令字面只有这一处没跟 A1 同步

- **位置**: `proposal.md:48`; 对照 `:49` (只提 `--no-renames`) / `:51` (要求必须带 `-z`) / `:69` (权威全命令 `git diff --name-only --no-renames -z <main>...<pr>`)
- **问题**: 逐处 grep 全文 `git diff` 共 10 处 (`:47`×2 / `:48` / `:49` / `:51` / `:69` / `:71` / `:89` / `:180` / `:248`), 其中只有 `:48` 与 `:69` 带完整 flag 字面, 而 `:48` 停留在 A1 前的 `--name-only`。**结论本身不受影响** (已实测: `-z` 下 gitlink 仍是单 token `aria`, 且 `-z` 顺带关掉转义, 这句话反而更成立), 但 `:51` 刚刚立下「`git diff` 调用**必须**带 `-z`」的硬规, `:48` 的字面与之直接对不上, 实现者按 `:48` 抄命令就会掉出 D14。
- **建议修法**: `:48` 改为「…在 `git diff --name-only -z` 输出为 gitlink 路径单 token (如 `aria`)…」, 或去掉 flag 只写「在 diff 输出中为…」, 让 `:69` 唯一持有命令字面。

---

### [MINOR] 规则 2 的「输出为空」与 SC-28 的「changed_files=[]」不是同一个量; D14 插进解析步骤后两者之间多了一道工序

- **位置**: `proposal.md:72` (规则 2) / `:200` (SC-28) / `:51`+`:69` (解析步骤)
- **问题**: `:72` 写「diff 成功但**输出为空** → `covered`, reason=`empty-diff`」, `:200` SC-28 写「diff 成功但输出为空 (**changed_files=[]**)」。A1 之前 `stdout` 与 `changed_files` 之间只隔一次 split, 现在隔了 `rstrip("\0")` + split + 滤空串三步, 两个量在规范上分家了。实现者 A 判 `if not stdout` (原始 stdout), 实现者 B 判 `if not changed_files` (解析后)。
- **证据**: 已实测空 diff 的 `-z` 输出是 **0 字节**, 所以本仓两种读法等价、今天零代价; 但任何让 stdout 非空而 changed_files 为空的形态 (例如将来有人误加 `--name-status -z` 或 diff filter) 会让 A 掉进规则 3~8 而 B 停在规则 2, 两条不同终态 (`no-triggering-paths`/`not_applicable` vs `empty-diff`/`covered`) —— 一个 skip 一个 wait。
- **建议修法**: `:72` 改为「解析后 `changed_files == []` → 整体 `covered`, reason=`empty-diff`」, 与 SC-28 字面对齐, 让规则 1-8 的输入全部是**解析后**的量。

---

### [MINOR] `rstrip("\0")` 与「滤空串」互相覆盖, SC-29(b) 无法单独验证 rstrip 是否存在; 「证尾随 NUL 已 rstrip」这句措辞比它能证的强

- **位置**: `proposal.md:51` (「解析须 `stdout.rstrip("\0").split("\0")` 再滤空串」) / `:69` / `:151` (D14) / `:201` (SC-29(b) 「(证尾随 NUL 已 rstrip)」)
- **问题**: 滤空串是 rstrip 的**超集** (前者顺带清掉尾随 NUL 产生的空元素, 还能清掉中间的)。三种实现 —— 只 rstrip / 只滤空串 / 两个都做 —— 在 SC-29(b) 下**全绿**, 该 SC 只能打红「两个都不做」的朴素 `split("\0")`。所以 `:201` 括注「证尾随 NUL 已 rstrip」是过度声称: 它证的是「解析结果无空串」, 不是「rstrip 存在」。次要副作用: 两道清洗叠加会**静默吞掉**将来真正异常产生的空 token, 与 `:106` D9「评估器自身失效必须可见」的取向相反。
- **建议修法**: 把义务改成**结果义务**而非步骤义务:「解析后 `changed_files` 不得含空串, 且 `changed_files_count == len(changed_files)`」, 步骤上二选一即可 (推荐只留 `rstrip("\0")` + split, 若 split 后仍出现空元素则视为异常 → `unknown`, 这样反而保住可观测性); 同步删掉 `:201` 的「已 rstrip」括注。

---

### [MINOR] D14 只规定了 `-z`, 没规定字节→字符串的解码契约; 而 `-z` 的输出正是**原始字节**, 非 ASCII 路径又是 SC-29(a) 的一等场景

- **位置**: `proposal.md:51` / `:69` / `:151` (D14) / `:201` (SC-29(a)) / `:80` (「永不 raise」) / `:79` (reason 封闭集)
- **问题**: 加 `-z` 之后 git 不再转义, 直接吐原始文件名字节。规范没说实现该用 `subprocess.run(..., text=True)` 还是 `capture_output` + 显式 `decode`。实现者 A 用 `text=True` (编码 = `locale.getpreferredencoding(False)`, `errors='strict'`); 实现者 B 用 bytes + `decode("utf-8", errors="surrogateescape")`。对**非 UTF-8 字节**的文件名 (Linux 上合法), A 抛 `UnicodeDecodeError` → 被 `:80` 的「永不 raise」兜到 `unknown`, 而 `:79` 封闭集里此时唯一可用的是 `git-diff-failed: <stderr 摘要>` —— 但 stderr 是空的, 报文会说「git diff 失败」而实际上 git 成功了, 诊断指向错误的层; B 则正常继续。
- **证据**: 本机实测 `LC_ALL=C python3` 下 `locale.getpreferredencoding(False)` = `utf-8` (PEP 540 UTF-8 mode 自动启用, `sys.flags.utf8_mode=1`), 所以**合法 UTF-8 路径两种写法都过** —— 这也正是它容易被漏掉的原因: SC-29(a) 用的 `skills/测试/x.py` 是合法 UTF-8, 测不出这个分叉。
- **建议修法**: D14 补一句解码契约:「`-z` 输出按 bytes 捕获, 以 `decode("utf-8", errors="surrogateescape")` 解码 (与 git 的字节语义一致, 不因 locale 变化)」。若不愿扩 reason 封闭集, 至少写明解码失败归入 `git-diff-failed` 时 `<stderr 摘要>` 位置须填「decode-error: …」以免误导。

---

## 范围外 (OUT_OF_SCOPE)

无。本轮所有 finding 均落在主审四处 (D12/D13/D14/AB 勘正) 或必审面 (A1 × §0 契约 / §1 8 条规则 / reason 封闭集) 之内。既有内容自身质量未审。

## 附: A1 中已核实为准确、无需改动的部分 (避免下轮重复劳动)

- **AB 勘正三条全部实地核实通过**: 裸名 `phase-c-integrator` 按 `AB_TEST_OPERATIONS.md:206` 确实解析到 parent `ab-suite/phase-c-integrator.json` (3 evals: commit-generation / merge-conflict-handling / multi-remote-merge-push, 与本 change 零关系) ✓; `latest` → `2026-05-13-state-scanner-issue-101-fix`, 且「最近一次归档」`2026-07-20-v1.62.0-phase4-rule6` 的 `skill_name` 也是 `state-scanner` —— **「二者均解析到 state-scanner 归档」两半都成立** ✓; 基线 `benchmark.json` 恰 8 个 `structural_metrics`, `measured` 全为 `int 100`, 仅 `primary_pass_gate.measured` 为 `"100%"` ✓。
- **D14 的技术前提实测成立**: 无 `-z` 时非 ASCII 路径确被八进制转义并加双引号 ✓; `-z` 输出确含尾随 NUL ✓; 空 diff 的 `-z` 输出为 0 字节 ✓。
- **D13 的「列 0」限定词有效**: 已实测 `build-aria-runner.yaml:97/:99` 的 `echo "--- image size ---"` 为缩进行, 不会被误判 —— L 侧 R3 报过的这个坑, A1 的措辞已避开。

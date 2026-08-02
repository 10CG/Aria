---
verdict: REVISE
agent: code-reviewer
round: R3
critical_count: 1
major_count: 4
minor_count: 7
r2_resolved: 14/17
---

# post_spec R3 — secret-guard-nomad-var-put-echo (code-reviewer, convergence 终验)

**审计对象**: `openspec/changes/secret-guard-nomad-var-put-echo/proposal.md` (R2 后 owner 裁定缩到最小范围版)

**核实手段** (全部实跑, 无一处凭读): 复制 hook 到 scratchpad 并**按 §What 字面注入新 pattern**, 对 SC-1~SC-6 全部形态跑真 exit code (改前 / 改后两套); 另做「无尾边界」变体对照跑; 用注入版跑全量 347 条回归; 实跑 `nomad var put --help` / `nomad var get --help` / `nomad var list --help` 与 `-o` flag 解析; 对 `secret-hygiene.md` 的 **HEAD 版本**逐行定位 `-out=keys` 并归属小节; python 精确重数 pattern 数组与 `/v1/var/`; 读 standards 子模块 `git diff` 与 `git status`; 聚合 R1/R2 五方 frontmatter 计数; curl 实拉 Nomad 文档 (HTTP 200)。

**未修改仓库任何文件** (sim hook 与测试副本均在 scratchpad; `standards/` 的 working-tree 修改在我进场前即存在, 见 m-3)。

---

## Phase 1 — 规范合规性

**判定**: PASS。缩范围后结构完整 (Why / What / Key Deliverables / 决策表 / Impact / 转出 / rule6_note / Tasks / SC 齐备), §转出 五项与 Tasks 1.5 一一对应, 无越界章节。进 Phase 2。

---

## Phase 2 — 引用与数字终检 (逐项实测)

### 核实为**正确**的 (记录以免后轮重开)

| 断言 | 核实手段 | 结果 |
|------|---------|------|
| `secret-guard.sh:406` = `nomad[[:space:]]+var[[:space:]]+(get\|list)` | 读第 406 行 | 逐字一致 |
| 「140 条 pattern」 | 数组 L402-L646, 非空非注释条目 = **140** | 精确 |
| 「347 条用例」 | 实跑现行套件 → `PASS: 347 / 347` | 精确 |
| 「L56-L418 共 37 处 `/v1/var/`」 | python 计数 = **37**, 首 = 56, 末 = 418 | 三数全精确 (口径见 m-2) |
| plugin.json 1.65.1 → v1.65.2 (PATCH) | `plugin.json` version = `1.65.1`; CHANGELOG 顶 = `## [1.65.1] - 2026-08-01` | 精确 |
| Nomad 文档 URL + 「PUT 响应含解密 Items」 | curl → HTTP 200 | 前提证伪成立, 要求 2 关闭正确 |
| `-out` 三子命令枚举表 (get / put / list) | 实跑三条 `--help` | **三行逐字一致**: get/put = `go-template\|hcl\|json\|none\|table`; list = `go-template\|json\|table\|terse`; 均无 `keys` |
| 实跑报错原文 `Invalid value for "-out"; valid values are [go-template, hcl, json, none, table]` | 实跑 | 逐字一致 |
| SC-1 五形态「改前 exit=0」 | 实跑现行 hook | 全 **0** |
| SC-1 五形态「改后 exit=2」 | 注入版 | 全 **2** |
| SC-2 第 1/3/4 条 (`>/dev/null` / `&>/dev/null` / `-out=none … >/dev/null`) 改前改后均 0 | 两版实跑 | 全 **0** (第 2 条见 M-3) |
| SC-3 `nomad var putty foo` 改后 exit=0 | 注入版 | **0** |
| SC-4 第 3 条 (`git commit -m …`) + 阳性对照 (真执行形态) 改后 = 2 | 注入版 | 均 **2** (前两条见 C-1) |
| SC-5 全量回归 347 全绿 | 注入版跑完整套件 → `PASS: 346 / 347` | **等效全绿** — 唯一 FAIL 是 `plugin-root: hooks.json missing PreToolUse matcher`, 系我把 hook 复制出仓造成的路径产物, 非语义回归 |
| SC-5「其余 5 个 `.test.sh`」 | `hooks/tests/*.test.sh` = 6 个 | 减去 secret-guard 本身 = **5**, R2 m-6 已闭 |
| SC-6a/6b「`nomad var get <path>` / `nomad var list` 仍 exit=2」 | 两版实跑 | 均 **2** |
| SC-6c「`nomad var get -out=json <p> \| jq 'keys'` 仍 exit=0」 | 两版实跑 | 均 **0**; 且 SOT 订正后实际写法 `jq '.Items \| keys'` 亦 **0** |
| 「本 spec 零豁免」 | 注入版对 `nomad var put … 2>/dev/null` = **2** | 保守选择落地正确 (R2-C-10 语义未被绕开) |
| R1 计数 `1C+13M+21m` | 五方 frontmatter 聚合 | **精确** |

### R2 (code-reviewer) findings 核销 — 14/17

| R2 项 | 状态 | 依据 |
|-------|------|------|
| C-1 `_pat_scoped_safe` 命令级豁免 | 已闭 | 整个豁免机制删除 (决策表「豁免机制 一律不做」), 移入 §转出 1 且保留 `cat /opt/.env; echo hi >/dev/null` 实测证据 (我复跑 = **0**, 证据仍真) |
| M-1 `-out=keys` 非法 | 已闭 (substance) | 升级为 §附带修复 + Tasks 1.3 + SC-7; 三子命令枚举表实测无误。**但范围数字错 → 新 M-1** |
| M-2 §Why 假阴表 6 行无 SC | 已闭 | §Why 假阴表整体删除, rows 7-8 (真假阴) 完整迁入 §转出 2 并保留实测 `curl -v -X PUT … >/dev/null` = 0; rows 1-6 是「现行正确行为」, 随 curl 面出范围一同移除。**信息损失核查**: 「写向零测试锁定」这一立项论据由 §测试面盲区 段独立承载 (未丢); 丢的只是 curl 写向 6 行的 exit code 快照, 而 §What 已不碰 `has_filter`, 该回归面不复存在 ⇒ **无实质损失** |
| M-3 §What 3 stderr 撤销规则 | 已闭 | §What 3 删除 → §转出 2, 且把我 R2 的 FP 证据固化成明文警告 (「修法须锚定 curl 语境, 裸扫 `-v` 会撞既有 `grep -v` credit」) — 转出质量高于单纯删除 |
| M-4 尾边界无 SC | 已闭 | SC-3 新增。**但与 SC-4 互斥 → 新 C-1** |
| M-5 计数「约 24」矛盾 | **未闭** | 由「约 24」改成精确「14」, 对 SC-1~SC-5 正确, 但 SC-6 需新增 2 条无人认领 → 新 M-4 |
| m-1 Key Deliverables 漏 secret-hygiene.md | 已闭 | 现列为第 3 项 |
| m-2 Task 1.5 无 SC | 已闭 | SC-7 新增 (机械性不足 → 新 M-2) |
| m-3 SC-11「仍」措辞 / m-4 SC-6 标注 / m-5 SC-2 标注 | 已闭 | 旧 SC 整体重写; 新 SC-1 标 baseline-failing, SC-2 标「改前改后均 exit=0」, 与实测一致 |
| m-6 脚本计数重复 | 已闭 | 改为「其余 5 个」, 实测 6-1=5 |
| m-7「其余 ~140」 | 已闭 | 「其余」已去掉 |
| m-8 rule6_note 与 archive 先例 | **未闭** | 见 m-4 |
| m-9 issue 收尾张力 | 已闭 | 改为「发进展 comment; **不关闭 issue**」+ 归因 owner/infra, 消歧彻底 |
| m-10 `test.sh:8` `~50 cases` 陈旧注释 | **未闭** | 实读第 8 行仍是 `Coverage: ~50 cases`, 未进 Tasks |
| m-11 dogfood 第 4 例 | 已闭 | §Impact「本 session dogfood 三次实证」 |

---

## Critical (必须修复 — 1)

### C-1. SC-3 与 SC-4 在本 spec 的约束下**不可同时满足** — SC 集合自相矛盾, 且 §Impact 的 FP 叙述被实测证伪

- 位置: `proposal.md` SC-3 (`nomad var putty foo` **exit=0**) vs SC-4 (`grep -rn 'nomad var put' aria/` / `echo "改用 nomad var put"` / `git commit -m "…"` 三条**改后 exit=2**); 连带 §Impact 风险段「文本操作 (`grep 'nomad var put'` / `echo "…"` / `git commit -m "…"`) 会被拦。**本 spec 接受该 FP**」。
- **实测** (两个 sim hook, 唯一差异 = 尾边界):

| 命令 | 带尾边界 `([[:space:]]\|$)` | 去掉尾边界 | SC 期望 |
|------|--------------------------|-----------|---------|
| `nomad var putty foo` | **0** | **2** | SC-3 要 0 |
| `grep -rn 'nomad var put' aria/` | **0** | **2** | SC-4 要 2 |
| `echo "改用 nomad var put"` | **0** | **2** | SC-4 要 2 |
| `git commit -m "fix: nomad var put 回显"` | 2 | 2 | SC-4 要 2 (**唯一自洽的一条**) |

- **机制**: 尾边界 `([[:space:]]|$)` 要求 `put` 后紧跟空白或串尾。`grep -rn 'nomad var put' aria/` 与 `echo "改用 nomad var put"` 里 `put` 后紧跟的是**引号**, 既非空白也非串尾 ⇒ 不匹配 ⇒ 放行。`git commit -m "fix: nomad var put 回显"` 因 `put` 后有空格才命中。所以 SC-4 三条里**只有第 3 条**成立, 前两条**恒为 0**。
- **为何 Critical** (三重):
  1. **SC 集合无解**: 本 spec 明令「零新增豁免逻辑」「唯一改动 = 1 条 pattern」, 在此约束下 SC-3 与 SC-4 前两条构成互斥对 —— 带边界则 SC-4 红, 去边界则 SC-3 红。**不存在**满足全部 SC 的实现。这不是数字错, 是验收契约无解, 会在 Phase B 直接卡死。
  2. **诱导错误修法**: 实施者最省力的「让 SC-4 变绿」动作就是删尾边界 —— 那正是 §What 明令必带、且 §转出 4 把「既有 pattern 缺尾边界」列为待修缺陷的东西。SC 会把实施者推向 spec 自己判定为缺陷的方向。
  3. **§Impact 的风险接受声明失真**: spec 声称「本 spec 接受该 FP」并把 `grep` / `echo` 当作已知代价登记在案。实测这两类**根本不会被拦**。风险登记项与真实行为不符, 会让后续读者 (以及 §转出 4 的收口者) 基于错误的现状认知做决策 —— 与 memory `feedback_doc_claims_need_diff_verification_and_variant_sweep` 同型。
- **修法** (三选一, 都要重跑取真值):
  (a) 保尾边界 (推荐, 与 §What 一致): 把 SC-4 前两条期望值改成 **exit=0**, 并把它们从「接受的 FP」重新归类为「尾边界的**副作用性豁免**: 引号紧邻 `put` 的文本引用天然不匹配」; §Impact 同步改写为「FP 面小于预期 —— 仅 `put` 后带空格的文本形态 (如 commit message) 会被拦」。
  (b) 若确实希望拦住 `grep 'nomad var put'` 这类文本引用, 则需引入命令级 FP 判定 —— 与「零新增豁免逻辑」冲突, 应整体转出。
  (c) 无论选哪条, SC-4 建议追加已实测的边界变体做锚点: `grep -rn 'nomad var put ' aria/` (引号内带尾空格) 实测 **2**, 可精确锁住「边界语义生效」这一事实, 并让 §转出 4 收口时以红灯提示。

---

## Major (应修复 — 4)

### M-1. `-out=keys` 订正范围「§3.3/§3.4 三处」与 SOT 实况不符 — 已应用的编辑因此漏掉 §4.4, 订正后的 SOT **自相矛盾**

- 位置: `proposal.md` §Key Deliverables 第 3 项 / §附带修复 首段 / §Impact「`secret-hygiene.md` 3 处示例」/ Tasks 1.3 — 四处口径一致地写「§3.3/§3.4 三处」。
- **实测** (对 `standards` 的 **HEAD** 版本逐行定位, 按小节归属):

| 行 | 所属小节 | 性质 |
|----|---------|------|
| 39 | **§1 核心条款** | 推荐 (`Verification: … nomad var get -out=keys 仅取 key 名`) |
| 161 | §3.3 | 推荐 (注释) |
| 163 | §3.3 | 推荐 (代码 argv) |
| 175 | §3.4 | 推荐 (注释) |
| 176 | §3.4 | 推荐 (代码) |
| **248** | **§4.4 Round-trip 验证 (反例区)** | 推荐 (`正确替代: 用 nomad var get -out=keys 检查 key 存在, 不读 value (见 §3.3)。`) |

  即字面出现 **6 处**、跨 **4 个小节**、**4 个独立示例位点**。「§3.3/§3.4 三处」在小节归属与数量上**双错**: 漏了 §1 与 §4.4, 且 §3.3 本身就是 2 处不是 1 处。
- **已经造成实害**: `standards/` working-tree 已有一版未提交的订正 (`git diff` = +21/-8), 它按 spec 的范围认知只改了 §1 / §3.3 / §3.4, **§4.4 :248 原样保留**。订正后文件里于是同时存在:
  - `:188` (新增警告) 「**不要用 `-out=keys`** — 该取值在 nomad **不存在** … 实跑报 `Invalid value for "-out"`」
  - `:261` (§4.4 未改) 「正确替代: 用 `nomad var get -out=keys` 检查 key 存在, 不读 value (**见 §3.3**)」

  同一份 Rule #7 SOT 里一节说「不存在, 别用」, 另一节说「正确替代就是它」, 并把读者指向恰好警告了它的那一节。**这比订正前更糟** —— 订正前至少是一致的错, 现在是自相矛盾, 读者按 §4.4 照做仍会撞 `Invalid value`, 失败后转向不安全替代, 正是 §Why 描述的 #170 事故链第 2→3 环。
- **为何 Major 而非 Minor**: 本 spec 的**唯一非 hook 交付物**就是这条订正, 而订正因范围数字错而不完整并制造了新的矛盾。这是 memory `feedback_doc_claims_need_diff_verification_and_variant_sweep`「符号清扫必须枚举全变体」的教科书复现, 也与 `feedback_calibrate_source_of_truth_before_translating` 同型 (派生前未用机械源校准 SOT 自身)。
- **修法**: 四处口径统一改为「`secret-hygiene.md` §1 / §3.3 / §3.4 / §4.4 共 4 个位点 (字面 6 处) `-out=keys` 全量订正」; §4.4 :248 改为指向订正后的真写法 (`-out=json … | jq '.Items | keys'`)。范围确定后再重跑 M-2 的机械清扫。

### M-2. SC-7 是「订正后的示例能跑」检查, 结构上**测不到残留** —— 正是 M-1 漏网的原因

- 位置: SC-7「`secret-hygiene.md` 订正后的示例命令**逐条实跑不报 flag 错误** (至少验证 `-out` 取值在合法枚举内)」。
- 问题: 这是一个**存在性正向检查** —— 它只对「我改过的那几条」求值, 对「我没改到的那条」永远沉默。§4.4 :248 就是这样通过 SC-7 的: 它不在「订正后的示例」集合里, 所以 SC-7 无论怎么跑都是绿。R2 m-2 建议的是**机械残留断言** (grep SOT 中不再出现 `-out=keys` 推荐), 本版换成了正向实跑, 覆盖方向恰好反了。
- 对齐 memory `feedback_check_predicate_must_validate_against_real_data_range` / `feedback_universal_predicate_vacuous_truth_on_empty_set`: 谓词只在自己选定的子集上求值时, 真空/局部成立会吞掉真实缺口。
- **修法**: SC-7 拆两条 ——
  - SC-7a (机械残留清扫, 可脚本化): `secret-hygiene.md` 全文**零处**出现 `-out=keys` 作为推荐; 允许出现的仅限显式反例/警告上下文 (可用「同段落必须含 `不要用` 或 `不存在`」做判据), 否则红。
  - SC-7b (保留现有正向实跑): 订正后示例逐条 `--help` / flag 解析层实跑无 `Invalid value`。

### M-3. SC-2 第 2 条 `nomad var put … -o /dev/null`(N/A, curl 专用则跳过) — 前提错、命令非法、且把断言数变成不确定量

针对本轮点名的问题: **是, 应判 finding**, 且三层都有问题。

- **(1) 「curl 专用」这个前提实测为假**。`secret-guard.sh:390` 的 credit 是对整条命令的裸正则 `(-o[[:space:]]+/dev/null|--output[[:space:]]+/dev/null)`, **没有任何 curl 语境限定**。实测注入版: `nomad var put nomad/jobs/app @f -o /dev/null` → exit=**0**。所以它既不 N/A 也不该跳过 —— 它会真触发, 且结果与 SC-2 期望的 0 一致。
- **(2) 但该命令形态 nomad 根本不接受**。实跑 `nomad var put -o /dev/null nomad/jobs/x K=v` → `flag provided but not defined: -o` (`nomad var get` 同)。也就是说这条 SC 会把一条**跑不通的命令**写进回归套件永久留存 —— 与本 spec 正在修的 `-out=keys` 缺陷**完全同类**。一个以「SOT 教了跑不通的命令」为立项理由的 spec, 不应在自己的 SC 里复制该缺陷 (memory `feedback_spec_inherits_upstream_dec_errors`)。
- **(3) 条件式措辞让验收面不确定**。「则跳过」把取舍留给实施者, 于是 SC-1~SC-5 的断言数在 **13 与 14 之间摇摆**, 而 §Key Deliverables 与 SC-5 都写死了 14 / 「347 + 新增 14」。SC 是验收契约, 不能含实施者自由裁量的分支 —— 否则「全绿」不再是唯一定义的状态。
- **修法** (二选一, 都要去掉括号里的条件式):
  - (a) **保留但改语义标签**: 期望 exit=0 不变, 注释改成事实描述 ——「`-o /dev/null` credit 非 curl 专属 (`:390` 裸正则), 故对 nomad 命令同样生效; 本条锁定该**跨工具溢出**现状, `nomad var put` 不接受 `-o` (实跑 `flag provided but not defined`), 故属 `KNOWN-LIMIT` 类, 与 SC-4 同组」。这样 14 条成立且语义诚实。
  - (b) **删掉本条**, 断言数明确改 13, §Key Deliverables 与 SC-5 同步。
  - 附: 无论选哪条, 建议把「`-o /dev/null` credit 无 curl 语境限定」补进 §转出 (可并入转出 2 或 4) —— 它和转出 2 的「裸扫 `-v` 会撞 `grep -v`」是同一类「credit 正则缺工具语境」缺陷。

### M-4. 「共 14 条断言」只覆盖 SC-1~SC-5, SC-6 需新增的 2 条**无 Task 也未计数** (R2 M-5 未闭)

- 位置: §Key Deliverables「`secret-guard.test.sh` — 写向用例族 (SC-1~SC-5, 共 14 条断言)」/ SC-5「基线 **347** 条 + 新增 14」/ Tasks 1.2「测试族 SC-1~SC-5」。
- **实测**: 现行 `secret-guard.test.sh` 全文只有 3 条 `nomad var` 用例 —— `:55` (`nomad var get <path>` = 2)、`:601` (heredoc 变体)、`:681` (NUL 变体)。SC-6 的三条里:
  - SC-6a (`nomad var get <path>` 仍 2) → `:55` 已覆盖, 无需新增;
  - SC-6b (`nomad var list` 仍 2) → **套件中不存在**, 须新增;
  - SC-6c (`nomad var get -out=json <p> \| jq 'keys'` 仍 0) → **套件中不存在**, 须新增。且它是 SOT 订正后推荐写法的可行性锚点 (M-1/M-2 一旦扩范围, 还应加 `jq '.Items \| keys'` 形态 —— 我实测亦为 0), 属**不可省**。
- 故实际新增 ≥ **16** 条, SC-5 的「347 + 14 = 361」应为 **363**; 且 Tasks 1.2 的范围「SC-1~SC-5」把 SC-6 排除在唯一的写测试任务之外 —— **SC-6/SC-7 没有任何 Task 认领**。
- 为何重要: 与 R2 M-5 同因 —— 实施者按 Task 1.2 收工就会自然漏掉 SC-6b/6c, 而 SC-6c 恰是「SOT 订正后的推荐写法在 hook 下真放行」这一跨交付物一致性的**唯一**锚点。
- **修法**: 断言数改 16 (或按 M-3 的裁定重算), SC-5 改「347 + 新增 16」; Tasks 1.2 范围改「SC-1~SC-6」, 并新增 Task 覆盖 SC-7 (可并入 1.3)。

---

## Minor (建议修复 — 7)

**m-1. §审计轨迹 R2 计数「2C」实为 4C** (`proposal.md:7`)。五方 R2 报告 frontmatter 聚合实测 = **4C + 13M + 24m** (backend 0/2/2, code-reviewer 1/5/11, knowledge 0/0/2, qa 1/1/4, tech-lead 2/5/5)。M/m 两个数字精确, 唯 Critical 少记 2。R1 的 `1C+13M+21m` 实测**完全精确** (1/13/21), 说明只是 R2 这一处漏算。因该行紧接着下结论「严重度未下降」, 用低估的 C 数反而弱化了自己的论据。

**m-2. §测试面盲区 的范围与计数口径不匹配** (「`nomad var` / `/v1/var/` 相关全为读向 (L56-L418 共 37 处)」)。37 与 L56-L418 都只针对 `/v1/var/` (实测精确); 而 `nomad var` **CLI** 用例在 `:55` / `:601` / `:681`, **三条全在该区间外** (`:55` 恰好差一行)。建议拆成两句: 「`/v1/var/` 37 处 (L56-L418) + `nomad var` CLI 3 处 (`:55` / `:601` / `:681`), 全为读向」。

**m-3. Tasks 1.3 已在工作区部分落地, 但 spec 仍 Draft 且复选框未勾**。`git -C standards status` = `M conventions/secret-hygiene.md` (未提交, +21/-8), 内容正是 §1/§3.3/§3.4 的 `-out=keys` 订正。我进场前即存在。两点后果: (a) spec Status「Draft … 待 R3」与实况不符, R3 的审计对象与工作区状态已分叉; (b) 该编辑正是 M-1 漏 §4.4 的载体 —— 先落地再定范围, 范围错就直接固化进文件。建议在 spec 里注明「Task 1.3 已预落地 (未提交), R3 后按修订范围补齐 §4.4 再一并 commit」, 避免下一个读者以为它是干净的未开工状态。

**m-4. rule6_note 同时声称「Rule #6 不适用」与提供「substitute」, 且与同 hook 的 archive 先例措辞仍相左** (R2 m-8 未闭)。若判定「结构性前提不成立、审的对象整个未产生」, 则逻辑上不需要 substitute; 现在两个框定并存。而 `openspec/archive/2026-06-19-secret-guard-exfil-coverage-iteration/proposal.md` 对**同一个 hook** 用的是 substitute 框定。论证本身自洽、实质证据面 (SC-1 baseline-failing, 我已实测五条 0→2 成立) 两种框定下都成立, 不阻塞 Phase B; 但按 Rule #10「AI 任何自作主张的流程判断必须写进 handoff 请复议」, 建议二选一并在 handoff 挂 owner 复议。

**m-5. `secret-guard.test.sh:8` 陈旧注释 `Coverage: ~50 cases` 仍未纳入范围** (R2 m-10 未闭)。实读确认未改。它已经污染过本 spec 一次 (R1 把 347 写成 ~50)。本 cycle 已经要动这个文件, 顺手改一行即可止血。

**m-6. 决策表「提示文案 **不改**」无验收锚点**。全部 SC 都是 exit code 断言, 测不到 heredoc 文本是否被改。考虑到 R1 曾试图改它、且 rule6_note 的免测论证**依赖**「本版未改任何提示文案」这一前提, 建议 SC-5 追加一句机械判据: 「`git diff` 中 `secret-guard.sh` 的改动**仅限** risky_patterns 数组内 1 行新增, heredoc (L654-L682) 零改动」。这条同时给 rule6_note 提供可证伪支撑。

**m-7. §Impact「aria 子模块 5 文件」口径易误读**。该 5 指版本同步 5 文件 (plugin.json / marketplace.json / VERSION / CHANGELOG.md / README.md), 而本 cycle aria 实际改动是 **7** 文件 (再加 `secret-guard.sh` + `secret-guard.test.sh`)。「ship 同步面」措辞技术上没错, 但与 §Key Deliverables 的 2 个 aria 文件并读容易被当成总数。建议写「aria 子模块: 2 交付文件 + 5 版本同步文件」。

---

## 内部自洽核查结论 (§What / Tasks / Key Deliverables / SC 四方矩阵)

| §What 条目 | Task | Key Deliverable | SC | 状态 |
|-----------|------|----------------|-----|------|
| 增补 1 条 pattern | 1.1 | secret-guard.sh | SC-1 | 齐 |
| 尾边界必带 | 1.1 | 同上 | SC-3 | **与 SC-4 冲突 (C-1)** |
| 走既有 has_filter, 零新增豁免 | 1.1 | 同上 | SC-2 | 齐 (SC-2 第 2 条 → M-3) |
| BLOCKED 提示不改 | — | — | — | **无锚点 (m-6)** |
| SOT `-out=keys` 订正 | 1.3 | secret-hygiene.md | SC-7 | **范围错 (M-1) + 谓词方向错 (M-2)** |
| 不回归 (读向 + 全量) | 1.4 | test.sh | SC-5 / SC-6 | **SC-6 无 Task 且未计数 (M-4)** |
| 转出五项开 issue | 1.5 | — | — | 齐, §转出 五项一一对应 |

- SC 编号 1-7 连续、无缺号无重号。
- §转出 五项 ↔ Tasks 1.5「五项」数量一致, 且每项都带独立裁量理由与实测证据, 无遗漏。
- 决策表 7 行与 §What / §Impact 无矛盾 (「豁免机制一律不做」在注入版实测确实成立: `nomad var put … 2>/dev/null` = 2)。

---

## 建议 (Recommendations)

1. **先定 M-1 的订正范围, 再动 SC-7 与工作区那份 diff**。范围从「3 处」扩到「4 位点 6 处」后, M-2 的机械清扫断言 (SC-7a) 才有正确的目标集; 否则会再固化一次「按错范围清扫 → 自认为清完」。
2. **C-1 建议走修法 (a) (保尾边界 + 改 SC-4 期望值)**。实测显示尾边界带来的「引号紧邻豁免」是**免费的 FP 缩减**, 比 §Impact 预估的风险面更小 —— 这是本 spec 的一个未被记录的**优点**, 值得写进 §Impact 而不是被当成需要消灭的偏差。
3. **给 SC 加一条「本 spec 的现实 FP 面」小表** (已全部实测): `put` 后带空格的文本形态 (commit message) 会被拦 = 2; `put` 后紧跟引号的形态 (grep / echo 引用) 不被拦 = 0。两行就能把 §转出 4 收口时需要重估的面精确交接。
4. **`-o /dev/null` credit 缺工具语境** (M-3 发现) 建议单独并进 §转出 2 —— 它与「裸扫 `-v` 撞 `grep -v`」是同一根因 (credit 正则不看调用的是哪个工具), 一起修比分两次修便宜。

---

## 评估

**是否可以继续?**: **REVISE** — C-1 与 M-1 必须在进 Phase B 前定稿 (前者使 SC 集合无解, 后者已在工作区制造了自相矛盾的 SOT); M-2/M-3/M-4 属同批定稿项, 改动量都在一两行文字。

**理由**: 缩范围的裁定**方向完全正确且执行到位** —— R2 的 1 个 Critical 与 4 个 Major 是靠**删除机制**而非打补丁关闭的, 转出五项每项都保留了原始实测证据 (我复跑 `cat /opt/.env; echo hi >/dev/null` = 0、`curl -v … >/dev/null` 的结论均仍成立), §Why 假阴表的移除经核查**无实质信息损失**; 事实底座质量继续保持高位 —— 本轮实测的 `:406` / 140 / 347 / 37 / L56 / L418 / 1.65.1 / 三子命令 `-out` 枚举表 / Nomad 文档 200 / R1 三元计数, **无一处失真**, 且 SC-1 五条、SC-2 三条、SC-3、SC-5 全量回归在注入版下全部按 spec 预期落地。剩余阻碍集中在**验收面的可满足性与完整性**, 不在设计: 其一, SC-3 (尾边界要放行 `nomad var putty`) 与 SC-4 (要拦 `grep 'nomad var put'`) 在「唯一改动 = 1 条 pattern、零新增豁免」的自我约束下被实测证明**互斥无解**, 且最省力的修法恰好会破坏 §What 明令的约束; 其二, 唯一的非 hook 交付物 —— SOT `-out=keys` 订正 —— 的范围数字错了 (实为 4 小节 6 处, 非「§3.3/§3.4 三处」), 而按该范围已预落地的编辑漏掉 §4.4, 使订正后的 Rule #7 SOT 出现「一节说不存在别用 / 另一节说正确替代就是它」的自相矛盾, 比订正前更易误导; 其三, SC-7 用正向实跑代替机械清扫, 结构上**测不到**这种残留, 因此这个洞在当前 SC 集合下永远是绿的。三者都是可在数十行文字内闭合的定稿项, 无需重新设计。

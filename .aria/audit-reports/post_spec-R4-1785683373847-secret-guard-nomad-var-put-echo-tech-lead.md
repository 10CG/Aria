---
verdict: REVISE
agent: tech-lead
round: R4
critical_count: 0
major_count: 3
minor_count: 7
r3_resolved: 5/12
---

# post_spec R4 — secret-guard-nomad-var-put-echo (tech-lead, 收敛验证)

审计对象: `openspec/changes/secret-guard-nomad-var-put-echo/proposal.md` + `standards/conventions/secret-hygiene.md` (工作树未提交改动)
前序: R1 → R2 → owner 缩范围裁定 → R3 (`post_spec-R3-1785681450725-…-tech-lead.md`) → 本轮

## 核对方法 (全部实跑, 零文件修改)

1. scratchpad 三副本: `base.sh` (原样) / `var.sh` (打入 spec 唯一 pattern) / `alt.sh` (替代尾边界, 仅用于证伪一条 spec 声称)。31 条命令逐条对 base/variant 跑真 hook, 取 exit code。
2. `git -C standards diff conventions/secret-hygiene.md` 读实际落地内容; 全文 grep 核 `-out=keys` 残留语境、章节号、`guard:ack` 文案落点 (含中文 i18n)。
3. 全量回归实跑: `bash aria/hooks/tests/secret-guard.test.sh` → **PASS 347 / 347** (基线数字核实)。
4. 基线稳定性: 本轮期间 `proposal.md` mtime 15:07:44 / `secret-hygiene.md` 15:01:56 均早于开审, 全程未变 —— **R3 的中途改写问题本轮未复发**。

### 实测矩阵 (节选, base = 未打 pattern, var = 已打)

| 用例 | base | var | 对应 |
|---|---|---|---|
| `nomad var put -in=json p @file` / `p KEY=v` / `-out=json` / `-out=table` / `-out=none` | 0 | **2** | SC-1 五条 ✓ |
| `nomad var put … >/dev/null` / `&>/dev/null` / `-out=none … >/dev/null` | 0 | 0 | SC-2 三条 ✓ |
| `nomad var put -verbose … >/dev/null` | 0 | 0 | SC-2 警示注记 ✓ |
| `nomad var putty foo` | 0 | 0 | SC-3 ✓ |
| `grep -rn 'nomad var put' aria/` | 0 | **0** | SC-4 第一条 ✓ |
| `echo "改用 nomad var put"` | 0 | **0** | SC-4 第二条 ✓ |
| `git commit -m "fix: nomad var put 回显"` | 0 | **2** | SC-4 第三条 ✓ |
| `nomad var put <path> @f` (阳性对照) | 0 | **2** | SC-4 第四条 ✓ |
| `nomad var get p` / `nomad var list` | 2 | 2 | SC-6 ✓ |
| `nomad var get -out=json … \| jq '.Items \| keys'` | 0 | 0 | SC-6 正向 ✓ |
| `… \| jq -r '.Items \| keys[]'` | 2 | 2 | SC-6 负向锚点 ✓ |
| `nomad var put p1 @f1 >/dev/null; nomad var put p2 @f2` | 0 | **0** | 无 SC 锁 → R4-M-3 |
| `nomad var put p @f 2>&1 >/dev/null` | 0 | **0** | 无处记载 → R4-M-2 |
| `nomad var put p @f -o /dev/null` | 0 | **0** | SC-2 称「与 nomad 无关」→ r4-m-3 |
| `… # guard:ack: writing a non-secret config value` | 0 | **2** | 出路失效 → r4-m-… |
| `… # guard:ack: rotating-credential-per-runbook` | 0 | 0 | 可用形态 |

**方向性核验 (最重要的一条)**: 31 条中变体相对基线的差集**只有 0→2 (拦得更多), 无一条 2→0**。R1/R2 反复出问题的 block→allow 回归方向, 本版结构上不存在。这条我第二次独立确认。

---

## R3 逐条核销 (5/12)

| R3 finding | 现状 | 核销 |
|---|---|---|
| **C-1** SC-4 三条 FP 断言 2 条与实测相反 | SC-4 已按实测重写 (2 条 exit=0 + 1 条 exit=2 + 阳性对照), Impact §风险 同步改正, 且「既有 (get\|list) 条已有同类」改为「同类且**更宽**」—— 措辞现在准确 | **已解决** (四条逐字实跑全对) |
| **C-2** SOT 订正三重脱节 | (a) Tasks 1.3 已勾 + 注「已预落地于工作树」✓; (c) 形态改 `jq '.Items \| keys'` 且搬入 `keys[]` 告诫 ✓ (实测 0 / 2 均对); (d) SC-7 补机械负向断言 ✓ (实测残留 2 处 `-out=keys` 全在警示语境); 章节号 §4.3→**§4.4** 修正且与实际文件一致 ✓ | **已解决**, 但 (b) 数字统一漏了 Impact 一处 → r4-m-1 |
| **M-1** nomad `-verbose` 走 stderr 被静默丢弃 | 转出 2 已拆 curl 侧 / nomad 侧两族, SC-2 加警示注记, SOT 补警示段。三处落点 | **已解决** (R3 建议的两条路都走了) |
| **M-2** 转出 2 丢 `2>&1 >/dev/null` 顺序陷阱 + `-o /dev/null` 第二条 credit 路径 | 全文零字 | **未解决 → R4-M-2** |
| **M-3** Impact 指定 `# guard:ack` 出路 ↔ 转出 3 声明其失效 | Impact 已加「(注意其文案/实现不符, 转出 3)」交叉引用 | **部分解决** — 悬空已显式化, 但可用形态 (首词连写 ≥8) 仍不在任何用户可见处; 降级为 minor |
| **M-4** 知识层通用条目第二次丢弃 | 新增 §转出 **6** `[知识层, 中]`, Tasks 1.5 同步改「六项」 | **已解决** |
| **M-5** 复合命令覆盖率上限无 SC 锁定 | 全文无 SC-8、无 `KNOWN-LIMIT` 字样 | **未解决 → R4-M-3** |
| m-1 转出 3 行号张冠李戴 + 漏 i18n | 原文未动 | **未解决 → r4-m-2** (且实测比 R3 说的更严重) |
| m-2 SC-2 把 `-o /dev/null` 标 N/A | 措辞由「(N/A, curl 专用则跳过)」改为「curl 专用 flag, 与 nomad 无关, 不列」—— 同一断言换皮 | **未解决 → r4-m-3** |
| m-3 SC-5 零鉴别力却被当兼容性证据 | 原文未动 | **未解决 → r4-m-4** |
| m-4 转出 4 severity 低 | 仍「低」; 而 Impact 把 dogfood 由「三次」改成「**四次**」—— 反向加强了它不该是低的论据 | **未解决 → r4-m-5** |
| m-5 §审计轨迹 计数未标多方合计 | 原文未动, 且新增的 R3 条目引入新的不实描述 | **未解决 → r4-m-6** |

**净判**: 两条 Critical 都是真解决 (非措辞规避), 严重度连续第二轮下降。但 12 条里 7 条**原文一字未动且无任何处置说明** —— 既不是解决、不是转出、也不是显式驳回。R3 已经点名过两次「静默丢弃」这个模式, 本轮它换到了 minor 层继续。

---

## 委托的三个专项

### (1) 新「实现约束」块能否防住「修红打掉 SC-3」路径 —— 能防住, 但它的论证是**假的**, 见 R4-M-1

防御效果本身成立: SC-4 现在断言那两条 FP 为 **exit=0**, 所以 Phase B 根本不会看到红灯, 也就没有「凑绿」的动机; 加上「实施者不得为凑某条 FP 断言而放宽边界」的明令, 双保险。我担心的路径已闭合。

但块内的因果论证经实测**证伪** —— 见下。

### (2) 本轮修订引入的新问题

- **R4-M-1** (新引入的不实声称, 就在为闭 C-1 而新增的块里)。
- **r4-m-6** §审计轨迹 对 R3 的概括不实。
- **r4-m-7** Tasks / Key Deliverables 与 SC 集合不对齐 (SC-6/SC-7 无归属)。

### (3) 收敛判定 — 见文末

---

## Major

### R4-M-1 「实现约束」块声称 SC-3 与 SC-4 「二者不可兼得」，实测可兼得 —— 为闭 C-1 而新增的块自身带一条未实测的不可能性断言 (本 cycle 第三次同类)

**位置**: SC-4 下的 ⚠️ 实现约束块

原文: 「要让 `grep 'nomad var put'` 也被拦就必须**去掉尾边界**, 而那会立刻误配 `nomad var putty` (SC-3 转红)。在「零新增豁免」下二者**不可兼得**」。

实测证伪 —— 只需**放宽尾边界的字符类**而非去掉它 (`([^[:alnum:]]|$)` 取代 `([[:space:]]|$)`):

| 用例 | spec 声称 | `alt.sh` 实测 |
|---|---|---|
| `nomad var putty foo` (SC-3) | 必然转红 | **exit=0 (仍绿)** |
| `nomad var putx foo` | — | exit=0 |
| `grep -rn 'nomad var put' aria/` | 无法同时拦 | **exit=2 (拦住)** |
| `echo "改用 nomad var put"` | 无法同时拦 | **exit=2** |
| `nomad var put p @f >/dev/null` | — | exit=0 (credit 未破) |

即 SC-3 与「拦住引号收尾的文本提及」**同时成立**是可实现的。真实的取舍不是「可不可能」, 而是「**要不要更多 FP**」—— 而本 spec 的选择 (少拦 = 少 FP) 恰恰是对的。所以**裁定不变, 论证必须改**。

**为什么算 Major 而非 minor**: (a) 这是**本轮新写入**的文字, 且写在专门用来修正 C-1 事实错误的块里 —— 修复动作自身重开同类缺陷 (memory `feedback_multiround_audit_catches_fix_introduced_regression`); (b) 它是 spec 归档后关于「为什么边界只能这样」的唯一记载, 会直接误导**转出 4** 的收口者 (转出 4 正是「既有 pattern 尾边界缺失 + FP 面」), 让他以为字符类不可调; (c) 「未实测就把一条命令/断言写进 spec」在本 cycle 已是第三次 (R2-C-1 `-out=keys` 非法 → R3-C-2(c) `jq 'keys'` 语义错 → 本条), 这个模式本身该被叫停。

**建议** (逐字可替换): 「尾边界是 SC-3 的硬约束; SC-4 前两条的 exit=0 是**当前字符类 `[[:space:]]` 的副产物**, 非不可改变 —— 放宽字符类 (如 `[^[:alnum:]]`) 可在保住 SC-3 的前提下把引号收尾的提及也拦住 (实测), 但那会**扩大 FP 面**, 与本 spec「接受残余 FP、不扩打击面」的裁定相反。故本 spec 选择 `[[:space:]]`。实施者不得为凑某条 FP 断言而改动该字符类; 若未来要改, 须连同转出 4 一并重评 FP 面。」

### R4-M-2 R3-M-2 原文一字未动 —— 一个专治 redirect 误解的 cycle, 至今没有任何一处记载 `2>&1 >/dev/null` 顺序陷阱, 而它正是本 spec 主推安全出路的镜像反例

**位置**: 转出 2 / SC-2 / SOT 警示段

实测 `nomad var put p @f 2>&1 >/dev/null` → **exit=0** (base 与 var 均是)。语义: `2>&1` 先把 stderr 复制到**当时的** stdout (= 流向 Claude 的管道), 之后才把 stdout 挪走 —— stderr 根本没挡住, 但任何朴素的「命令里出现 `2>&1`」判据都会给 credit。

本轮 SOT 新增的警示段写的是「务必 `>/dev/null 2>&1`」—— 方向正确, 但**恰好把顺序敏感的那对 token 摆在读者面前却不说它顺序敏感**。读者把两个 token 记成一组、写反了, 得到的是零警告 + hook 放行。这是 SOT 加固后新暴露的相邻风险面, 不是可以留到转出 2 才提的东西。

同样仍缺: `-o /dev/null` 是 `has_filter` 的**第二条 stdout-only credit 路径** (`secret-guard.sh:390`), 转出 2 若只修 curl flag 枚举, 这条依旧漏 (与 r4-m-3 同源)。

**建议**: 转出 2 补两句 —— 「判据须显式要求 `2>&1` 出现在 stdout 重定向**之后**才算挡住 stderr; `2>&1 >/dev/null` 是反例 (实测 exit=0 放行)」+ 「`-o /dev/null` 与 `>/dev/null` 同属 stdout-only credit 路径, 同一修法须覆盖」。并在 SOT 警示段 (a) 项后加半句「注意顺序: 写成 `2>&1 >/dev/null` 无效」。

### R4-M-3 R3-M-5 原文一字未动 —— 最常见的批量写 var 形态下本 spec 唯一交付物等于没加, 而无任何 SC / 无任何一句量化说明

**位置**: §转出 1 / SC 集合 / Impact §兼容

实测 (变体):

```
nomad var put p1 @f1 >/dev/null; nomad var put p2 @f2   → exit=0   ← 第二条零保护
nomad var put p @f; echo hi >/dev/null                  → exit=0
```

第一行是「一次写多个 var」的日常形态, 第二条命令正是 #170 的泄漏形态本身。§Why 讲了整命令扫描机制, 转出 1 讲了通用后果, 但举的两个例子是 `cat /opt/.env` 与 `nomad var get` —— 读者要自己推导「我刚加的 put 条也一样被掏空」。Impact §兼容 只写「纯新增拦截面」, 没写覆盖率上限。

**为什么仍是 Major**: 没有红灯 ⇒ **转出 1 收口时没有任何信号提示「这条该转绿了」**。本 spec 在 SC-4 上刚刚示范了「按实测锁现状」的正确手法, 却对这条更要紧的不用。全文现在连 `KNOWN-LIMIT` 这个词都不出现了。

**建议**: 加 SC-8: `nomad var put p1 @f1 >/dev/null; nomad var put p2 @f2` 改前改后均 **exit=0**, 标注「本 spec 已知不覆盖, 归转出 1; 该用例转红 = 转出 1 已收口」。Impact §兼容 加一句「覆盖率上限: 单命令有效; 复合命令 (`a; b`) 任一段携带 redirect 时全段放行 (转出 1)」。

---

## Minor

### r4-m-1 C-2(b) 数字统一漏一处 — Impact 仍写「`secret-hygiene.md` 3 处示例」
其余三处 (Key Deliverables L63 / §附带修复 L67 / Tasks 1.3 L127) 均已统一为「4 个推荐位」, 唯 **L95 影响面**留着旧数字。R3-C-2(b) 逐字点过这一行。不改施工结果 (Tasks 已勾且已落地), 但它是 ship 时被引用的那句。

### r4-m-2 转出 3 的行号/文件数未动, 且实测比 R3 报的更严重
原文「涉 6 处 3 文件 (hook L63/L157 + 姊妹 hook + README L147)」。实测全仓落点 = **8 处 / 5 文件**:
`aria/hooks/secret-guard.sh` L61 / L314 / L679 · `aria/hooks/host-docker-logout-guard.sh` L29 / L63 / L157 · `aria/README.md` L147 · `aria/README.zh.md` L147 · `standards/conventions/secret-hygiene.md` L293。
两处后果: (a) L63/L157 是**姊妹 hook** 的行号, 按描述去 `secret-guard.sh` 找会扑空; (b) 漏了 `README.zh.md` (i18n 发布同步面, 收口时会触发 i18n 一致性 check) **和 `secret-hygiene.md` L293** —— 后者是本 cycle 正在编辑的同一份 SOT, 它也带着这条错文案。

### r4-m-3 SC-2 仍称 `-o /dev/null`「与 nomad 无关, 不列」— 实测它是一条真实放行面
`nomad var put secret/p @f -o /dev/null` → **exit=0**。credit 谓词 (`secret-guard.sh:390`) **不锚定 curl**, 所以一个 nomad 根本不存在的 flag 也能换来放行。SC 断言的是 hook 行为不是 nomad 语义, 「与 nomad 无关」在这个语境下是错的。措辞从 R3 的「N/A 则跳过」改成「与 nomad 无关, 不列」= 同一断言换皮。建议改为一条锁定用例并并入转出 2。

### r4-m-4 SC-5 零鉴别力未加分工说明, Impact 仍把它当兼容性证据
本轮实跑再次确认: 打 patch 前后全量套件均 **347/347**。Impact「既有放行/拦截行为不变 — 由 SC-5 全量回归 (347 条) 锁定」字面正确, 但与 §Why 自陈「347 条对这一维度结构上无鉴别力」并置会误导。建议 SC-5 加一句: 正确性由 SC-1 (baseline-failing) 承担, SC-5 只承担无外溢。

### r4-m-5 转出 4 severity 仍「低」, 而 Impact 本轮把 dogfood 由「三次」改成「四次」
同一轮里把命中频次的论据加强了 (三→四), 却没动 severity。一个 session 内命中四次的 FP 标「低」会让它长期排不上。建议「中」。

### r4-m-6 §审计轨迹 对 R3 的概括不实 + 计数仍未标多方合计
新写的「R3 (去重 2C+15M: 一条真实 SC 互斥 + 两条 R2 静默丢弃 + **其余为作者中途改文件引发的文档不一致**)」—— 可直接证伪: 我 R3 单方 5 条 Major 里, M-2 (转出 2 丢顺序陷阱)、M-5 (无覆盖率 SC) 与中途改文件毫无关系, 且它们恰好是本轮**未被处理**的两条。这行会被 #170 的进展 comment 引出去, 把「未处理」框成「不算数」。另: 「R2 (2C+13M+24m)」仍未标注是**五方合计** (我 R2 单方为 2C+5M+5m), 读者会误认单方结论 (r3-m-5 原诉求)。

### r4-m-7 Tasks / Key Deliverables 与 SC 集合不对齐 (本轮新增 SC 后未回改)
Key Deliverables 写「写向用例族 (**SC-1~SC-5**, 共 14 条断言)」、Tasks 1.2 写「测试族 **SC-1~SC-5**」, 但 SC 集合已到 SC-7。SC-6 的四条 (`nomad var get` / `nomad var list` / jq 投影正向 / `keys[]` 负向锚点) 全是 `secret-guard.test.sh` 级断言却无归属任务; SC-7(b) 的机械 grep 也无任务承接 (Tasks 1.3 已勾, 但那是**订正**动作不是**验证**动作)。属 memory `feedback_spec_rework_leaves_downstream_ac_drift` 的典型残留。

---

## 我复核后认可成立的部分 (不构成 finding)

- **两条 Critical 是真解决, 不是措辞规避**。SC-4 四条用例我逐字实跑, 期望值全对; SOT 形态 `jq '.Items | keys'` 放行 (0) 与 `keys[]` 被拦 (2) 均复现; SC-7(b) 的机械断言对当前 SOT 成立 (残留 2 处 `-out=keys` 全在「误写…会报 Invalid value」「不要用」语境); §4.4 章节号与实际文件 (§4.4 Round-trip 验证, L257-267) 一致。
- **零新增风险面第二次独立确认**。31 条差集只有 0→2 方向, 无 2→0。
- **SC-7 的 (d) 缺口被正确堵上**。R3 指出「正向 SC 测不到散文位漏订正」, 新增的负向 grep 断言恰好覆盖 —— 若 §1 Verification 定义行或 §4.4 那句漏改, 它们会以推荐语境出现在 grep 命中里而失败。这条设计是对的。
- **SOT 落地质量高于 spec 描述, 且本轮 spec 已追上**。`.Items | keys`、`keys[]` 告诫、两段反坑警示、Version 1.1.0→1.1.1 —— 逐条与工作树 diff 核对一致。
- **rule6_note 无需再动**。本 cycle 零 SKILL.md 改动 (跨仓核实), 提示文案不改, 「结构性前提不成立」干净。substitute = SC-1 baseline-failing, 实测确为 baseline-failing (五条 base 全 0 / var 全 2)。
- **版本口径正确**。`plugin.json` 实测 1.65.1, spec 写「现 1.65.1 → v1.65.2 PATCH」一致; standards Version 行实测 1.1.1 一致。(旁注, 不属本 spec: 主仓 `CLAUDE.md` 项目状态段仍写 v1.65.0, 已落后 SOT —— 归 ship 时的 5 文件同步面处理。)
- **审计基线本轮稳定**。两份文件 mtime 均早于开审且全程未变, R3 的中途改写问题未复发, Status 段的自陈留痕做法正确。

---

## 收敛判断 — REVISE (但收敛已在设计轴上完成, 剩余全在事实轴)

**设计轴: 已收敛。** 缩范围裁定、零豁免、保尾边界、SOT co-land、五+一项转出 —— 四轮下来无一条设计分歧残留, 我不再对任何裁定提出异议。R1/R2 的 block→allow 回归类问题两轮独立复核确认消失。

**事实轴: 未收敛。** 判 REVISE 的两个理由, 都不是「还想再讨论」:

1. **修复动作自身引入了新的不实断言** (R4-M-1)。为闭 C-1 而写的「实现约束」块里那句「二者不可兼得」, 我用替代边界实跑直接证伪。这已经是本 cycle 第三次「未实测就把断言写进 spec」(R2-C-1 → R3-C-2(c) → 本条)。让一条被证伪的不可能性声称随 spec 归档, 会精准误导转出 4 的收口者。
2. **12 条里 7 条原文一字未动且零处置说明** (M-2 / M-5 / m-1~m-5)。R3 已经两次点名「静默丢弃」这个模式; 本轮它没消失, 只是从 Major 层挪到了 minor 层。其中 R4-M-2 (顺序陷阱) 尤其刺眼 —— 一个专治 redirect 误解的 cycle, 刚刚在 SOT 里写下 `>/dev/null 2>&1`, 却不告诉读者这两个 token 顺序敏感。

**收敛还差什么 (封闭清单, 全部逐字可改, 无需再实测 —— 数字我都代好了)**:

| # | 位置 | 动作 |
|---|------|------|
| 1 | SC-4 实现约束块 | 用 R4-M-1 给出的替换段落整体替换 (裁定不变, 只改论证) |
| 2 | 转出 2 | 补两句: `2>&1 >/dev/null` 顺序陷阱 (实测 exit=0) + `-o /dev/null` 第二条 credit 路径; SOT 警示段 (a) 项后加半句「注意顺序」 |
| 3 | SC 集合 + Impact §兼容 | 加 SC-8 (复合命令 KNOWN-LIMIT, 改前改后均 exit=0) + 一句覆盖率上限 |
| 4 | Impact L95 | 「3 处示例」→「4 个推荐位」 |
| 5 | 转出 3 | 「6 处 3 文件 (hook L63/L157…)」→「8 处 5 文件」并按 r4-m-2 的实测清单逐条列出 |
| 6 | SC-2 | `-o /dev/null` 由「与 nomad 无关, 不列」改为锁定用例 (实测 exit=0) 并并入转出 2 |
| 7 | SC-5 / 转出 4 / §审计轨迹 / Tasks 1.2+Key Deliverables | 四处一行级订正 (分工说明 / severity 低→中 / 删「其余为…」并标「五方合计」/ SC-1~SC-5 → SC-1~SC-7 及 14 条断言重算) |

**下一步建议**: 改完上表**不必开 R5**。7 项全部是文本替换, 且每项的实测依据已在本报告内给全; 由作者自检 + 一次机械 grep (`grep -n "3 处示例\|不可兼得\|SC-1~SC-5\|6 处 3 文件" proposal.md` 应零命中) 即可确认落地, 直接进 Phase B。若作者对 R4-M-1 的证伪有异议, 可用我的 `alt.sh` 方案 (`nomad[[:space:]]+var[[:space:]]+put([^[:alnum:]]|$)`) 自行复跑 `nomad var putty foo` 与 `grep -rn 'nomad var put' aria/` 两条即可自验, 30 秒。

**并发纪律**: 本轮零中途改写, 保持。若进 Phase B 前还要动文件, 请在改后于 Status 段追一行 mtime + 改动摘要, 让下一个读者能判断自己读的是哪一版。

---
verdict: REVISE
agent: tech-lead
round: R3
critical_count: 2
major_count: 5
minor_count: 5
r2_resolved: 9/12
---

# post_spec R3 — secret-guard-nomad-var-put-echo (tech-lead, 收敛终验)

审计对象: `openspec/changes/secret-guard-nomad-var-put-echo/proposal.md`
前序: R1 → R2 (`.aria/audit-reports/post_spec-R2-1785679872011-…-tech-lead.md`) → owner 缩范围裁定 (2026-08-02) → 本轮

## 核对方法 (全部实跑)

1. 把唯一 pattern 打进 `secret-guard.sh` 的 scratchpad 副本 (`$SCRATCH/ariacopy/hooks/`), 对 baseline 与变体逐条跑 SC-1~SC-7 全部命令 + 30 余条探测形态。
2. 全量回归双跑: baseline **347/347**, 变体 **347/347** (副本目录跑, 无 R2 那条 plugin-root 假 FAIL)。
3. `git -C standards diff` 读实际 SOT 改动; `stat` 核 mtime; 跨仓 grep 核 `-out=keys` / ack 文案 / i18n README。

> **审计基线不稳定 (须先知晓)**: 本轮进行中 `proposal.md` (mtime 14:45:44) 与 `standards/conventions/secret-hygiene.md` (14:45:19) 被并发改写 —— 我在 14:37 版上开审, 中途重读发现 §Key Deliverables/§附带修复 已从「三处」改为「4 个推荐位」。下述 findings 已全部按 **14:45 版**复核。违反 memory `feedback_audit_workflow_land_edits_between_rounds` (审计 workflow 只审不改), 且这正是 R3-C-2(a)(b) 的成因。

---

## R2 逐条核销 (9/12)

| R2 | spec 现处置 | 核销结论 |
|----|------------|---------|
| **C-1** `-out=keys` 非法 | 转为 SOT 订正; spec 内零 keys 豁免 | **已解决** — 全文 grep 确认无 keys 豁免、无 keys hint、决策表不再引它。方向正确。但订正的**事实底座与形态**出错 → R3-C-2 |
| **C-2** 命令级判定 | 转出 1 | **已转出**, 描述含机制 + 两个反例, severity「高」恰当。但新 pattern 自身即刻受制这点未点名 → R3-M-5 |
| **M-1** 撤销规则命令级 / `-v` 撞 `grep -v` | 转出 2 (含「须锚定 curl 语境」告警) | **已转出**, 且保留了最易踩的实现约束 |
| **M-2** stderr 家族 + `2>&1 >/dev/null` 顺序陷阱 | 转出 2 | **部分** — flag 变体列全了, 但**顺序陷阱与 `-o /dev/null` 两条被丢** → R3-M-2 |
| **M-3** `-out=none -verbose` | 无 (推定被零豁免消解) | **未核销** — 消解不成立, 经 spec 主推的 `>/dev/null` 出路复活 → R3-M-1 |
| **M-4** FP 守卫理由/谓词洞 | 转出 4 + SC-4 接受现状 | **已解决** — 不建守卫 ⇒ (b) 谓词洞消失; (a) 理由矛盾随 keys 豁免撤销消失; dogfood 痛点在 get 侧这点由 Impact 明说。裁定站得住 |
| **M-5** 知识层通用条目 | 无 | **未核销, 第二次静默丢弃** → R3-M-4 |
| m-1 `-out=none -out=json` | 无豁免 ⇒ moot | 已消解 |
| m-2 事故第 2 环因果断言 | §Why 改为「API 文档证伪要求 2」 | 已解决 — 不再有 keys 因果断言 |
| m-3 ack 文案 6 处 | 转出 3 | 已转出 (行号张冠李戴 → r3-m-1) |
| m-4 SC-12 不可证伪 | 文案不改 ⇒ SC-12 删 | moot |
| m-5 (a) Key Deliverables 漏 SOT / (b) SC 锁纯 FP | (a) 已增列; (b) 改为 SC-6「读向不回归」 | 已解决 — (b) 改成锁现状而非锁裁定, 措辞诚实 |

**结论**: 转出机制整体诚实 —— 五项都写了 severity、机制、实测证据, 未见「悄悄消失」式丢弃。**但有两条 (M-3 / M-5) 既不在解决面也不在转出面**, 属真正的静默丢弃; 一条 (M-2) 转出时丢了最关键的实现陷阱。

---

## Critical

### R3-C-1 SC-4 的 3 条 FP 断言里 **2 条实测与 spec 声称相反**; Impact §风险 同错 —— 照写即红灯, 而「顺手修好」的做法会直接打掉 SC-3

**位置**: SC-4 / Impact §风险

实测 (变体 = 已打 pattern):

| SC-4 用例 (逐字) | spec 断言 | 实测 |
|---|---|---|
| `grep -rn 'nomad var put' aria/` | 改后 exit=2 | **exit=0** ✗ |
| `echo "改用 nomad var put"` | 改后 exit=2 | **exit=0** ✗ |
| `git commit -m "fix: nomad var put 回显"` | 改后 exit=2 | exit=2 ✓ |
| 阳性对照 `nomad var put <path> @f` | exit=2 | exit=2 ✓ |

**根因**: spec 自己要求的尾边界 `([[:space:]]|$)` 使**引号收尾**的文本提及不匹配 —— `put'` / `put"` 后面既不是空白也不是行尾。只有恰好以空格续接的提及 (`git commit -m "fix: nomad var put 回显"`) 才命中。实测非对称: `grep -rn 'nomad var put ' aria/` (多一个空格) → exit=2, `echo "nomad var put x 会被拦"` → exit=2。

**三处派生后果**:

1. **SC-4 照写进测试即 2 条红**。实施者面对红灯最省事的"修法"是去掉尾边界 —— 那会直接打掉 SC-3 (`nomad var putty foo` 必须 exit=0)。两条 SC 在当前措辞下互相冲突, 这是设计时就该消掉的矛盾, 不该留给 Phase B 临场裁量。
2. **Impact §风险 是事实错误**: 「文本操作 (`grep 'nomad var put'` / `echo "…"` / `git commit -m "…"`) 会被拦」—— 三个例子里两个不会。
3. **「既有 `(get|list)` 条已有同一 FP, 故非新增行为类别」不成立**。既有条**没有尾边界**, 实测 `grep -rn 'nomad var get' aria/` → exit=2; 新 put 条 → exit=0。两者 FP 面**不同类**: 既有条是稳定的全量文本 FP, 新条是**取决于引号收尾字符**的碎片化 FP。这个差异让 SC-4 声称的「锁定现状, 转出 4 收口时以红灯提示」失效 —— 转出 4 若给既有条补尾边界, 反而会让 get 侧的 FP 用例转绿, 而 put 侧的 KNOWN-LIMIT 用例本来就没红。

**建议**: SC-4 三条用例逐条按实测重写期望值 (2 条 exit=0 + 1 条 exit=2), 并把「空格收尾 vs 引号收尾」的非对称显式写成两组对照断言 (`…put' `/`…put "` 各一)。Impact §风险 改为「文本提及**在以空白或行尾收尾时**被拦, 引号收尾时不被拦 —— FP 面比既有 `(get|list)` 条**更窄且更不规则**」。SC-3 与 SC-4 的关系写明: 尾边界是 SC-3 的硬约束, SC-4 的 exit=0 是它的副产物, 不得为消红灯而移除。

### R3-C-2 SOT 订正的事实底座三重脱节: 工作树里**已经改完**而 Tasks 未勾; 同一 spec 内「3 处 / 4 处」并存; spec 写的订正形态 `jq 'keys'` 语义错, 与实际落地的 `jq '.Items | keys'` 不同 —— R2-C-1「拿一条没核实的命令当正解」原样重演

**位置**: Key Deliverables / §附带修复 L73 / Impact L89 / Tasks 1.3 / SC-6 / SC-7

**(a) 状态脱节**。`git -C standards diff` 显示 `conventions/secret-hygiene.md` 已在工作树被改 (22+/9-, mtime 14:45:19), 四处 `-out=keys` 推荐位**全部订正完毕**且新增了 ⚠️ 反坑段。而 Tasks 1.3 仍是未勾的 `[ ]`。spec 把已完成的工作描述成待办, ship 时无人知道它是何时、由谁、在哪个 gate 之前落的 (Rule #2「先 spec 后代码」的记录面缺口)。

**(b) 数字自相矛盾**。14:45 的编辑把 Key Deliverables 与 §附带修复 改成「**4 个推荐位**」, 但 **Impact L89 仍写「`secret-hygiene.md` 3 处示例」**, **Tasks 1.3 仍写「§3.3/§3.4 三处」**。同一份 spec 三处说三处、两处说四处。且 Tasks 1.3 的范围 (§3.3/§3.4) **不含** Key Deliverables 新列的 §1 Verification 定义行与 §4.3「正确替代」句, 也不含新增的反坑警示段 —— 按 Tasks 施工会漏掉一半。

**(c) 订正形态本身错**。§附带修复 L73 与 SC-6 都把正解写成 **`-out=json | jq 'keys'`**。`nomad var get -out=json` 返回的是 Variable 对象 (`{Namespace, Path, CreateIndex, ModifyIndex, CreateTime, Items:{…}}`), `jq 'keys'` 取的是**这层元数据字段名**, 不是 secret 的 item key 名 —— 它跑得通、hook 也放行 (实测 exit=0), 但**答非所问**。实际落地的 SOT 用的是 `jq '.Items | keys'` (正确, 实测 exit=0), SOT 还额外写了「`keys[]` 带方括号会破坏 hook 识别」的告诫 (我实测 `jq -r '.Items | keys[]'` → **exit=2**, 该告诫准确)。

即: **落地的文件比 spec 更准确**, spec 反而记了一条会误导的形态, 而 SC-6 正把这条错形态当成「SOT 订正后推荐写法的可行性验证」锁进回归。这是 R2-C-1 判定的同一类错误 (未核实语义就写进 SC) 在同一 cycle 内换个位置复发。

**(d) SC-7 结构性测不到主要缺陷位**。SC-7 = 「订正后的示例命令逐条实跑不报 flag 错误」。但四个推荐位里 §1 Verification 定义行与 §4.3「正确替代」句是**散文, 不在代码围栏内**, 无「命令可跑」这一说; 而漏订正它们恰是最容易发生的。SC-7 对此永远绿。

**建议**: (a) Tasks 1.3 与 Impact L89 与 Key Deliverables 统一为「4 个推荐位 + 1 段反坑警示」, 并在 Status/Tasks 注明该项**已在工作树落地**(附 diff stat), 由 Phase B 只做核验; (b) §附带修复 L73 与 SC-6 的形态改为 `-out=json … | jq '.Items | keys'`, 并把 SOT 已写的「`keys[]` 会被拦」一并搬进 spec (它是 hook 与 SOT 的耦合事实); (c) SC-7 补一条**机械断言**: `grep -c "out=keys" secret-hygiene.md` 的命中全部位于警示语境 (「不存在」/「不要用」), 零推荐位 —— 这是 R2 code-reviewer m-2 提过的同一条。

---

## Major

### R3-M-1 R2-M-3 (`-verbose` 走 stderr) 既未解决也未转出 —— 零豁免只消解了 `-out=none` 那条路径, 该风险经 spec **主推**的 `>/dev/null` 出路原样复活

**位置**: 决策表「安全形态出路」/ SC-2 / 转出 2

spec 推定「不做豁免 ⇒ R2-M-3 消失」。不成立: 既有 `>/dev/null` credit 是 **stdout-only** (`secret-guard.sh` 注释自陈: `2>/dev/null` 不算 filter), 而 `nomad var put --help` 原文明写 `-verbose` 「Provides additional information **via standard error**」。实测变体:

```
nomad var put -out=none -verbose <path> @f >/dev/null   → exit=0
nomad var put -verbose <path> @f >/dev/null             → exit=0
nomad var put <path> @f 2>&1 >/dev/null                 → exit=0   (顺序陷阱, stderr 未被挡)
```

即 **SC-2 认证为安全的写法族里存在未验证的 stderr 泄漏面**。R2-M-3 的原诉求 (先实机核实 `-out=none -verbose` 往 stderr 写什么, 未定论前 fail-closed) 一字未落。转出 2 的家族描述**只列 curl 变体** (`curl -v` / `--verbose` / `-vv` / `--trace*`), nomad 自己的 `-verbose` 不在其中 —— 未来读者按转出 2 修完 curl, 这条仍在。

**建议**: 二选一 —— (1) 实机核实后在 §遗留/转出 2 显式加一行「nomad `var put -verbose` 同属 stderr 假阴家族, 与 `>/dev/null` 组合时放行, 未实机核实其 stderr 内容」; (2) 更强: SC-2 加限定「本 spec 认证的安全形态**不含** `-verbose`」, 并加一条 KNOWN-LIMIT 用例锁定。至少要有一条, 现状是零。

### R3-M-2 转出 2 丢了 R2-M-2 里最硬的两条 —— `2>&1 >/dev/null` 顺序陷阱 与 `-o /dev/null` 第二条 credit 路径; 未来读者据现描述**复现不出**问题

**位置**: 转出 2

R2-M-2 的核心不是"flag 变体没列全"(那部分转出了), 而是**判据本身会被骗**: `2>&1 >/dev/null` 的语义是「stderr 先复制到当时的 stdout (= 流向 Claude 的管道), 之后才把 stdout 挪走」——stderr 根本没挡住, 但任何朴素的「命令含 `2>&1`」检查会判定"已挡住"并给 credit。实测 `nomad var put p @f 2>&1 >/dev/null` → exit=0 印证。转出 2 全文无一字。同样丢失的是「`-o /dev/null` 与 `>/dev/null` 同属 stdout-only credit 路径」(`secret-guard.sh:390`)。

一个专治 redirect 误解的 cycle, 把「redirect 顺序陷阱」这条知识丢在转出边界上, 下一个实施者极可能修完 flag 枚举就收工, 留下同一个洞。

**建议**: 转出 2 补两句 —— 「判据须显式要求 `2>&1` 出现在 stdout 重定向**之后**才算挡住 stderr; `2>&1 >/dev/null` 是反例 (实测 exit=0)」+ 「`-o /dev/null` 是第二条 stdout-only credit 路径, 同一修法须覆盖」。

### R3-M-3 缩范围造出**新耦合**: Impact 把 `# guard:ack` 指定为 accepted-FP 的唯一出路, 而转出 3 同时声明该逃生门在自然语言理由下失效 —— 两条转出各自成立, 合起来把出路悬空

**位置**: Impact §风险 ↔ 转出 3

Impact: 「本 spec **接受**该 FP …出路是既有 `# guard:ack` 逃生门」。
转出 3: 「实现要求首 token ≥8 连续非空白, 文案写 reason ≥ 8 NON-WHITESPACE chars ⇒ **合法使用下逃生门失效**」。

实测确认两边都真:

```
nomad var put p @f # guard:ack: writing a non-secret config value   → exit=2  (被拒)
nomad var put p @f # guard:ack: rotating-credential-per-runbook     → exit=0  (通过)
```

也就是说: spec 新增了一类拦截 + 声明接受其 FP + 指定出路 + 同时声明该出路对任何按文档写法的人都不工作。R2-M-4 (FP 守卫) 与 r2-m-3 (ack 文案) 各自转出都合理, 但**没人检查两个转出的交集**。可用形态 (首词连写 ≥8 字符) 存在, 却没写在任何用户可见的地方。

**建议**: 不必把转出 3 拉回范围内。Impact §风险 那句改成可执行的: 「出路是 `# guard:ack: <首个 token ≥8 连续非空白>` (注意: 现有文案描述有误, 见转出 3; 在转出 3 收口前, 理由必须**首词连写**, 例: `rotating-credential-per-runbook`)」。一行文字, 零行为风险, 把悬空补上。

### R3-M-4 R2-M-5 (知识层通用条目) 第二次被静默丢弃 —— 既不在交付面也不在转出面; 而本 cycle 恰好正在编辑同一份 SOT

**位置**: §附带修复 / Tasks 1.3 / 转出 (五项)

轨迹: R1 M-4(b) 被 spec 标为**采纳** → R2 复核发现无落点 (R2-M-5) → 本版仍无落点, 且**未进 §转出**。这是唯一不带"nomad"字样的可复用知识: 「Claude Code 的 Bash 工具 stdout 恒为 pipe ⇒ 凡默认输出档随 isatty 变化的 CLI, 在此环境下会输出**更多**而非更少」。

它目前只活在两个地方: 本 proposal 的 §Why (将随 Phase D 归档进 `openspec/archive/`, 不是知识家), 和一条 nomad 专用 regex 里。下一个碰到同类 CLI (docker / gh / kubectl / terraform 的 tty 感知输出) 的人查不到它。

边际成本近零 —— SOT 文件本 cycle 已在改, 且已新增了一段 ⚠️ 反坑警示, 顺手多一句即可。

**建议**: 二选一 —— (1) 并进 §附带修复 的反坑警示段 (推荐, 一句话); (2) 若坚持缩范围, 至少开为 §转出 第 6 项 `[知识, 低]`, 别让它第三次消失。**当前"既不做也不转"是三个选项里唯一不可接受的**。

### R3-M-5 新 pattern 自身即刻受制于转出 1, 但无任何 SC 锁定 —— 最常见的批量写 var 形态下, 本 spec 的唯一交付物等于没加

**位置**: 转出 1 / SC 集合 / Impact §兼容

实测变体:

```
nomad var put p1 @f1 >/dev/null; nomad var put p2 @f2    → exit=0   (第二条完全无保护)
echo hi >/dev/null; nomad var put p @f                   → exit=0
nomad var put p @f; echo hi >/dev/null                    → exit=0
```

第一行是**极常见形态** (一次写多个 var), 且第二条命令正是 #170 的泄漏形态。转出 1 描述了通用机制, 但举的两个例子是 `cat /opt/.env` 与 `nomad var get` —— 读者需要自己推导"我刚加的这条 put pattern 也一样被掏空"。§Why 与 Impact §兼容 (「纯新增拦截面」) 都没把这个覆盖率上限说出来。

R2 认可 SC-14 用 `KNOWN-LIMIT` 命名锁架构限制是好做法; 本版对 FP 用了 (SC-4) 却对这条更重要的没用。**没有红灯 ⇒ 转出 1 收口时没有信号提示"这条 SC 该转绿了"**, 与 SC-4 自陈的收口机制自相矛盾。

**建议**: 加 SC-8 (`KNOWN-LIMIT`): `nomad var put p1 @f1 >/dev/null; nomad var put p2 @f2` 改前改后均 **exit=0**, 注明「本 spec 已知不覆盖, 归转出 1; 该用例转红 = 转出 1 已收口」。同时 §Why 或 Impact 加一句量化本 pattern 的覆盖率上限 (单命令有效, 复合命令携带任意 redirect 时失效)。

---

## Minor

### r3-m-1 转出 3 的行号张冠李戴 + 文件数漏计 i18n
「涉 6 处 3 文件 (hook L63/L157 + 姊妹 hook + README L147)」—— L63/L157 实际是**姊妹 hook** `host-docker-logout-guard.sh` 的行号; `secret-guard.sh` 自身的落点是 **L55 / L61 / L314 / L679** (实测 grep)。按现描述去 `secret-guard.sh` 的 L63/L157 找会扑空。另: `aria/README.zh.md` 同样携带该文案 (实测 grep 命中), 故是 **4 文件**不是 3 —— 且它属发布 5 文件同步面, 漏掉会触发 i18n 一致性 check。

### r3-m-2 SC-2 第二条把一条真实放行面标成「N/A 则跳过」
`nomad var put … -o /dev/null` 标注「(N/A, curl 专用则跳过)」。实测 **exit=0** —— credit 谓词 (`secret-guard.sh:390`) **不锚定 curl**, 所以一个 nomad 根本不存在的 flag 也能拿到 credit。这不是 N/A, 是一条"写错的命令换来放行"的真实面, 应作 KNOWN-LIMIT 锁定 (并入转出 2 的 `-o /dev/null` 条), 而不是跳过。

### r3-m-3 SC-5 对本变更零鉴别力, 但 Impact 把它当作兼容性证据
实测: 打 patch 前后全量套件均 **347/347**。SC-5 锁的是"没碰别的", 不构成本 pattern 正确性的任何证据。Impact §兼容 写「既有放行/拦截行为不变 — 由 SC-5 全量回归 (347 条) 锁定」在字面上正确, 但与 §Why 自陈「347 条对这一维度结构上无鉴别力」并置时会误导读者。建议 SC-5 加一句分工说明: 正确性由 SC-1 (baseline-failing) 承担, SC-5 只承担无外溢。

### r3-m-4 转出 4 severity「低」与本 session 的实际命中频次不符
转出 4 含「读 `--help`、grep 文本、commit message 被拦」, 而 spec 自己在 Impact 里写「本 session dogfood **三次**实证」。一个 session 内命中三次的 FP 标「低」偏轻, 建议「中」; 且这是 R2-M-4 指出的 dogfood 痛点全在 get 侧、本 spec 修的是 put 侧 —— severity 标低会让它长期排不上。

### r3-m-5 §审计轨迹 行的计数未标"多方合计", 读者会误认单方结论
「R2 (2C+13M+24m, 严重度未下降)」—— 我的 R2 单方是 2C+5M+5m; 13M/24m 是五方 agent 合计。行内未注明, 而该行会被 #170 的进展 comment 引用出去。建议写成 `R2 (五方合计 2C+13M+24m)`。

---

## 我复核后认可成立的部分 (不构成 finding)

- **「零豁免 = 零新增风险面」成立**。逐条核: 变体相对 baseline 的行为差集 **只有** `nomad var put …` 一族从 exit=0 转 exit=2 (拦得更多), 无一条从 2 转 0。R1/R2 两轮反复出问题的 block→allow 方向**本版结构上不可能发生** —— 这是缩范围最大的收益, 裁定正确。(注意这只是"新增风险面"为零; 覆盖率上限见 R3-M-5, 两者不冲突。)
- **`nomad var put -out=none` 被拦 (SC-1 第五条) 可接受**。它确是纯 FP (该命令零输出), 但 (a) 出路 `>/dev/null` 只差一个 token 且已在 BLOCKED 提示清单内; (b) 方向 fail-closed; (c) 实测 SOT §3.4 自己推荐的写形态 `nomad var put -force … >/dev/null 2>&1` 在变体下仍 exit=0, **无跨文档回归**; (d) SC-1 已显式标注"这是刻意的保守选择"。不必改。
- **SC-4「接受 FP」的裁定方向站得住** —— 缩范围下不建守卫是对的, 且 KNOWN-LIMIT 锁现状的手法正确。**但其事实基础错了**(R3-C-1) 且论证依据「既有条已有同一 FP」不成立; 裁定保留, 论证与用例须重写。
- **转出机制整体诚实**。五项都带 severity + 机制 + 实测证据 + 实现陷阱提示, 没有"降级成一句话"式的稀释。除 M-3 / M-5 两条真丢失外, 其余转出的描述足以让未来读者独立复现 (转出 2 需补 R3-M-2 的两句)。
- **rule6_note 更强了**。本版不改任何提示文案 ⇒ R2 唯一保留的灰区 (hook 文案是否算 AI 指令面) 消失, 「结构性前提不成立」比 R2 时更干净。实测确认 `hooks/` 与 `hooks/tests/` 零 SKILL.md 耦合。R2 建议补的 README 边界说明现已 moot (README 改动转出)。
- **§Why 的诚实度显著提升**。R2-r2-m-2 点名的那句未验证因果断言已删; 「两版豁免设计都被我自己实测推翻」写进正文是罕见且正确的自陈。
- **SOT 实际落地的订正质量高于 spec 描述** —— `jq '.Items | keys'` 语义正确, `keys[]` 会被拦的告诫经我实测准确 (exit=2)。这部分文件本身无需返工, 需返工的是 spec 对它的描述 (R3-C-2)。

---

## 收敛判断

R2 → R3 的严重度**首次实质下降** (R2 的 block→allow 回归类问题全部消失, 方案方向正确)。但仍 REVISE, 理由是两条 Critical 都落在**可机械核验的事实面**而非设计裁量面: SC-4 的期望值与实测相反 (照写即红), SOT 订正的处数/形态/状态三重不一致 (照做会漏改一半并锁错形态)。这两条都是 30 分钟内可改完的文本修正, 不涉及任何设计重开 —— 修完即可 PASS。五条 Major 中 M-1/M-2/M-4 是转出补字 (三处共约 5 行), M-3 是 Impact 补半句, M-5 是加一条 SC。

**建议下一步**: 直接修上述条目后进 Phase B, 不必开 R4 (findings 已全部落在文本层, 无待收敛的设计分歧)。若并发写入不停止, 先冻结 `proposal.md` 再改 —— 本轮已因中途改写产生一次审计基线失效。

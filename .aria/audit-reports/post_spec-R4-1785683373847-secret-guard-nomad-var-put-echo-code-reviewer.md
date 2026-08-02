---
verdict: REVISE
agent: code-reviewer
round: R4
critical_count: 0
major_count: 3
minor_count: 8
r3_resolved: 4/12
---

# post_spec R4 — secret-guard-nomad-var-put-echo (code-reviewer, convergence 终验)

**审计对象**: `openspec/changes/secret-guard-nomad-var-put-echo/proposal.md` + `standards/conventions/secret-hygiene.md` (工作树未提交订正)。

**核实手段** (全部实跑, 无一条凭读): 复制 hook 到 scratchpad 造两个变体 (带尾边界 / 去尾边界), 对 SC-1~SC-6 全部形态 + 转出证据 + FP 变体跑真 exit code (原版 / tail / notail 三列对照); 用 tail 变体跑**完整** 347 条回归 (整目录复制, 消除 R3 那次的路径产物); 实跑 `nomad var {get,put,list} --help` 与 `-out=keys` / `-o` 报错原文; python 精确重数 pattern 数组 / `/v1/var/` / `nomad var` CLI 用例行号 / SOT `-out=keys` 残留并归属语境; 五方 R1/R2/R3 frontmatter 机械聚合; curl 实拉 Nomad 文档; 读 standards `git diff` 全文。

**未修改仓库任何文件** (sim hook 与回归副本均在 scratchpad; `standards/` 工作树修改在我进场前即存在)。

---

## Phase 1 — 规范合规性

**判定**: PASS。结构完整 (Why / What / Key Deliverables / 附带修复 / 决策表 / Impact / 转出 / rule6_note / Tasks / SC), 无越界章节, 无 scope creep。SOT 订正范围与 §What 声明一致 (已实测, 见下)。进 Phase 2。

---

## Phase 2

### 一、点名复核: R3「SOT 订正漏 §4.4」一条 — **确认为我读旧版所致, 撤回**

对**当前工作树**逐行重扫 `-out=keys` 字面, 全文仅 **2 处**命中, 且**两处都在警示语境**:

| 行 | 内容 | 语境 |
|----|------|------|
| 163 | `旧版本文档误写 -out=keys 会报 Invalid value` | §3.3 注释, 含否定词 + `Invalid value` |
| 188 | `⚠️ **不要用 -out=keys** — 该取值在 nomad **不存在**` | §3.4 后新增警示块 |

四个推荐位 (§1 L39 / §3.3 / §3.4 / §4.4) **全部已订正**, `git diff` 逐条确认: L39 → `-out=json … | jq '.Items | keys'`; §3.3 → `-out=json` + `json.loads(...).get('Items', {})`; §3.4 → `jq '.Items | keys'` + exit-code 两式; **§4.4 L267 → `正确替代: 用 nomad var get -out=json … | jq '.Items | keys' 检查 key 存在, 不读 value (见 §3.3/§3.4)`**。

我 R3 报告里「§4.4 :248 原样保留 / 订正后 SOT 自相矛盾 / 比订正前更糟」的整条论述**不成立, 予以撤回** —— 该处在我读取时点之外已订正。**R3 M-1 的实害部分 (SOT 自相矛盾) 不存在**; 剩下的只是 proposal 内部口径 (见 R4 M-1)。

### 二、C-1 核销: **真正解决, 不是把矛盾写进文档** (关键结论)

R3 C-1 的实质是「SC 集合无解」—— 不存在满足全部 SC 的实现。判断处置是否有效, 唯一判据是: **拿本 spec 允许的实现 (唯一改动 = 1 条带尾边界 pattern, 零新增豁免), 能否让 SC-1~SC-6 同时为真**。实跑三列对照:

| 用例 | 原版 | **tail (本 spec 实现)** | notail | 当前 SC 期望 | 符合 |
|------|-----|------|--------|------------|------|
| SC-1 五条 (`-in=json` / `KEY=` / `-out=json` / `-out=table` / `-out=none`) | 0 0 0 0 0 | **2 2 2 2 2** | 2 2 2 2 2 | 改前 0 / 改后 2 | 全符 |
| SC-2 三条 (`>/dev/null` / `&>/dev/null` / `-out=none …>/dev/null`) | 0 0 0 | **0 0 0** | 0 0 0 | 改前改后均 0 | 全符 |
| SC-2 警示注记 `put -verbose … >/dev/null` | 0 | **0** | 0 | 放行 (有洞) | 符 |
| SC-3 `nomad var putty foo` | 0 | **0** | **2** | 0 | 符 |
| SC-4 `grep -rn 'nomad var put' aria/` | 0 | **0** | 2 | **0 (放行)** | 符 |
| SC-4 `echo "改用 nomad var put"` | 0 | **0** | 2 | **0 (放行)** | 符 |
| SC-4 `git commit -m "fix: nomad var put 回显"` | 0 | **2** | 2 | 2 | 符 |
| SC-4 阳性对照 `nomad var put <path> @f` | 0 | **2** | 2 | 2 | 符 |
| SC-6a `nomad var get <path>` / SC-6b `nomad var list` | 2 / 2 | **2 / 2** | 2 / 2 | 2 | 符 |
| SC-6c `get -out=json … \| jq '.Items \| keys'` (与 SOT 逐字一致) | 0 | **0** | 0 | 0 | 符 |
| SC-6 负向锚点 `… \| jq '.Items \| keys[]'` | 2 | **2** | 2 | 2 | 符 |
| 零豁免 `put … 2>/dev/null` | 0 | **2** | 2 | 拦 | 符 |
| SC-5 全量回归 (tail 变体, 整目录复制) | — | **PASS: 347 / 347, FAIL: 0** | — | 全绿 | 符 |

**结论: tail 列与当前 SC 期望逐格一致, 零冲突。SC 集合已可满足。** 处置不是「把矛盾写进文档」, 而是**改正了错误的期望值** —— R3 认定的「矛盾」其实是 SC-4 前两条把未实测的预估写成了断言; 现按实测改成放行, 互斥自然消失。三点加分:

1. **实现约束块方向正确且必要**。它锁住的正是我 R3 预警的「最省力错误修法」: 实测 notail 列确实让 `grep` / `echo` 转 2 (看似「修好」了), 同时把 SC-3 的 `putty` 打成 2 —— 与该块的因果陈述**逐字吻合**。
2. **§Impact 风险段已同步改写**为实测口径 (「FP 面远小于起草时预估 … 仅 `put` 后真有空格才拦」), R3 指出的「风险登记项与真实行为不符」已消除。
3. **附带发现 (记录为优点)**: 实测既有 `(get|list)` 条对 `grep -rn 'nomad var get' aria/` = **2**、`echo "改用 nomad var get"` = **2**, 而新 pattern 对同形态 = **0**。§Impact 声称的「既有条已有同类且**更宽**的 FP」是**实测成立的**, 不是修辞。

### 三、R3 findings 逐条核销 (4/12 完全闭合)

| R3 项 | 状态 | 依据 (全部实测) |
|-------|------|----------------|
| **C-1** SC-3/SC-4 互斥无解 | **已闭** | 见上表, SC 集合在 tail 实现下逐格满足 + 347/347 全绿 |
| **M-1** SOT 订正范围 3/4 并存 + §4.4 残留 | **半闭** | 实害半边 (§4.4 残留 / SOT 自相矛盾) **不成立, 已撤回**; 口径半边 4 处中改了 3 处 (L63 / L67 / L127 = 「4 个推荐位」), **§Impact L95 仍「3 处示例」** → R4 M-1 |
| **M-2** SC-7 正向谓词测不到残留 | **已闭** | SC-7 拆 (a) 正向 + (b) 负向机械 grep。我对真实数据验证该谓词**非真空且当前为绿**: 全文 2 处命中, 均含「不要用 / 不存在 / Invalid value」⇒ 谓词有可求值对象、可证伪、且与实况一致 (对齐 `feedback_universal_predicate_vacuous_truth_on_empty_set`) |
| **M-3** SC-2 第 2 条 `-o /dev/null` | **已闭** (走修法 b) | 该条已删, SC-2 明写「三条」。残留两点精度问题 → R4 m-7 |
| **M-4** 14 条断言只覆盖 SC-1~SC-5, SC-6 无 Task 未计数 | **未闭 (原样)** | L62 / L128 / L138 / SC-5 全未改; 实测缺口仍在 → R4 M-2 |
| m-1 R2 计数 2C 实为 4C | **未闭** | 重新机械聚合五方 frontmatter: R2 = **4C+13M+24m** (backend 0/2/2, code-reviewer 1/5/11, knowledge 0/0/2, qa 1/1/4, tech-lead 2/5/5); L9 仍写 2C |
| m-2 测试面盲区口径 | **未闭** | L44 原样。复测: `/v1/var/` = 37 处 / 首 56 / 末 418 (三数精确), 但 `nomad var` **CLI** 用例在 `:55` `:601` `:681`, **三条全在 L56-L418 之外** |
| m-3 Tasks 1.3 预落地未标注 | **已闭** | Status 新增流程留痕自陈 + Tasks 1.3 标 `[x]` + 「已预落地于工作树」备注 |
| m-4 rule6_note「不适用」与 substitute 并存 | **未闭** | L117-121 原样, 两个框定仍并存 |
| m-5 `test.sh:8` `~50 cases` | **未闭** | 实读第 8 行仍 `# Coverage: ~50 cases`; 未进 Tasks |
| m-6 「提示文案不改」无验收锚点 | **未闭** | 全部 SC 仍是 exit code 断言, 无 `git diff` 范围约束 |
| m-7 「aria 子模块 5 文件」口径 | **未闭** | L99 原样 |

### 四、全文引用终检 (逐条实跑, 供后轮免复核)

| 断言 | 手段 | 结果 |
|------|------|------|
| `secret-guard.sh:406` = `nomad[[:space:]]+var[[:space:]]+(get\|list)` | 读第 406 行 | 逐字一致 |
| 「140 条 pattern」 | 数组 L402-L646 非空非注释项 | **140**, 精确 |
| 「347 条」(基线 / 回归 / 测试面盲区 三处) | 实跑现行套件 | `PASS: 347 / 347`, 精确 |
| 「L56-L418 共 37 处 `/v1/var/`」 | python 计数 | 37 / 56 / 418 三数全精确 (口径见 m-2) |
| 「其余 5 个 `.test.sh`」 | `hooks/tests/*.test.sh` = 6 | 6-1 = **5**, 精确 |
| plugin.json 1.65.1 → **v1.65.2** (PATCH) | 读 plugin.json + CHANGELOG 顶 | 1.65.1 / `## [1.65.1]`, PATCH 判定正确 |
| §Why 引用的 `var put --help` `-out` 三行 | 实跑 | **逐字一致** (含 "Defaults to \"none\" when stdout is a terminal and \"json\" when the output is redirected") |
| `-out` 三子命令枚举表 | 实跑三条 `--help` | get/put = `go-template\|hcl\|json\|none\|table`; list = `go-template\|json\|table\|terse`; **均无 keys**, 表格逐字正确 |
| 报错原文 `Invalid value for "-out"; valid values are [...]` | 实跑 | 逐字一致 |
| `-verbose` 走 stderr (转出 2 / SC-2 注记) | 实跑 `--help` | `Provides additional information via standard error to preserve standard output (stdout)`, 引用准确 |
| **`.Items \| keys` vs `keys[]` 的区别** | 两形态实跑 hook | `jq '.Items \| keys'` = **0**; `jq '.Items \| keys[]'` = **2**。SOT L181-182 注释与 SC-6 负向锚点**双向成立** |
| Nomad Variables API 文档 URL | curl | **HTTP 200**, 要求 2 关闭前提有效 |
| §转出 1 证据 `cat /opt/.env; echo hi >/dev/null` | 实跑 | **0**, 成立 |
| §转出 2 证据 `curl -v -X PUT … >/dev/null` | 实跑 | **0**, 成立 |
| §转出 4 证据 `nomad var getty` 误配 | 实跑 | **2**, 成立 |
| §转出 六项 ↔ Tasks 1.5「六项」 | 数列表 | 1-6 共 6 条, 一致 |
| R1 计数 `1C+13M+21m` | 五方聚合 | **精确** (1/13/21) |
| §1/§3.3/§3.4/§4.4 节号 | 逐节定位 | **四个节号全部正确**, 全文无 `§4.3` 残留 |
| Version 1.1.0→1.1.1 | `git diff` | header 已改; **§10 表未补行** → R4 M-3 |

### 五、四方覆盖矩阵 (§What / Tasks / Key Deliverables / SC)

| §What 条目 | Task | Key Deliverable | SC | 状态 |
|-----------|------|----------------|-----|------|
| 增补 1 条 pattern | 1.1 | secret-guard.sh | SC-1 | 齐 |
| 尾边界必带 | 1.1 | 同上 | SC-3 + SC-4 实现约束 | **齐 (C-1 已闭)** |
| 走既有 has_filter, 零新增豁免 | 1.1 | 同上 | SC-2 | 齐 |
| BLOCKED 提示不改 | — | — | — | **无锚点 (m-5)** |
| SOT `-out=keys` 订正 (4 位点) | 1.3 | secret-hygiene.md | SC-7a/7b | 齐 (口径 L95 未同步, M-1) |
| 不回归 (读向 + 全量) | 1.4 | test.sh | SC-5 / SC-6 | **SC-6 无 Task 且未计数 (M-2)** |
| 转出六项开 issue | 1.5 | — | — | 齐 |

SC 编号 1-7 连续、无缺号无重号; 决策表 7 行与 §What / §Impact 无矛盾。

---

## Critical (0)

无。R3 唯一 Critical 已实测闭合。

## Major (应修复 — 3)

### M-1. §Impact L95 仍写「`secret-hygiene.md` **3 处**示例」— 四处口径中最后一处未同步 (R3 M-1 残留半边)

- 位置: `proposal.md:95`。同一事实的另三处 (L63 Key Deliverables / L67 附带修复 / L127 Tasks 1.3) 均已改为「**4 个推荐位**」。
- 实测: SOT 实际订正 = **4 个推荐位** (§1 L39 / §3.3 / §3.4 / §4.4), `git diff` 四处全覆盖, 无残留。故 L95 的「3」是**唯一与事实不符**的数字。
- 为何 Major: §Impact 是发布范围记录, ship 后复核 / 回滚定位以它为准; 同一文档里 3 与 4 并存, 读者无法判断哪个是权威。这正是 memory `feedback_doc_claims_need_diff_verification_and_variant_sweep`「符号清扫必须枚举全变体」在**同一 spec 内**的复发 —— 上一轮清扫改了 3 处漏 1 处。
- 修法: L95 改「`secret-hygiene.md` 4 个推荐位 (§1/§3.3/§3.4/§4.4) + 2 段新增警示」。

### M-2. 「共 14 条断言」不可导出且已算错; SC-6 仍无 Task 认领, 三条用例实测缺失 (R3 M-4 原样未闭)

- 位置: L62 Key Deliverables「(SC-1~SC-5, 共 **14** 条断言)」/ L128 Tasks 1.4 / L126 Tasks 1.2「测试族 **SC-1~SC-5**」/ L138 SC-5「基线 347 条 + 新增 **14**」。
- **(1) 14 已算错**。按当前 SC 文本逐条枚举命令: SC-1 = 5, SC-2 = **3** (明写「三条」, `-o /dev/null` 已按 R3 M-3 删除), SC-3 = 1, SC-4 = 4 (grep / echo / commit / 阳性对照) ⇒ **13**。「14」只有把 SC-2 的**警示注记** (`put -verbose … >/dev/null`) 也算成断言才凑得出, 而该注记未声明为断言; 若 SC-1 按「改前 + 改后」双向计则是 18。**同一个数在三种读法下是 13 / 14 / 18** —— 验收契约不能含不可导出的数 (对齐 R3 M-3(3) 的同一根因: 上一轮删了 SC-2 一条却没回改总数)。
- **(2) SC-6 的用例实测确实缺失**。扫 `secret-guard.test.sh` 全文:
  - SC-6a `nomad var get <path>` → **已有** (`:55`), 无需新增;
  - SC-6b `nomad var list` → **全文不存在** (现有 `nomad var` CLI 用例仅 `:55` / `:601` / `:681`, 均为 get), 须新增;
  - SC-6c `nomad var get -out=json … | jq '.Items | keys'` → **全文不存在** (`:125` / `:187` 是 **curl** 形态, 不是 nomad CLI), 须新增;
  - SC-6 负向锚点 `… | jq '.Items | keys[]'` (nomad CLI 形态) → **全文不存在**, 须新增。
  ⇒ SC-6 至少新增 **3** 条, 全量应为 **13 + 3 = 16**, SC-5 的「347 + 14 = 361」应为 **363**。
- **(3) Tasks 1.2 范围仍是 SC-1~SC-5**, 把 SC-6 排除在唯一的写测试任务之外。
- 为何 Major (且已跨两轮未动): 实施者按 Task 1.2 字面收工必然漏掉 SC-6b/6c, 而 **SC-6c 是「SOT 订正后的推荐写法在 hook 下真放行」这一跨交付物一致性的唯一锚点** —— 它一旦不入套件, 下次有人动 jq filter 识别就会再次把 SOT 与 hook 打分裂, 正是本 spec 立项要治的病。对齐 `feedback_freeze_task_must_coland_with_volatile_state_phase`。
- 修法: Tasks 1.2 范围改「SC-1~SC-6」; 断言数三处统一改 **16**; SC-5 改「347 + 新增 16 = 363」; 或改成不写死总数、只写「SC-1~SC-6 每条至少一个用例」以免再次算术漂移。

### M-3. `secret-hygiene.md` §10 版本历史表未补 1.1.1 行 — header 已 bump, 历史表停在 1.1.0 (新)

- 位置: `secret-hygiene.md:3` (`Version: 1.1.1`, 已在工作树落地) vs `:393-396` (§10 表仅 `1.0.0` / `1.1.0` 两行)。
- 该文件自身惯例是**每次版本变更对应一行历史**, 且 1.1.0 那行详载「改了什么 / 零 breaking / 来源 spec / 来源 memory」。现在 header 单方面前进, 历史表出现空洞 —— 这份文档是 Rule #7 的 SOT, 版本审计线索断档会让后续「这段警示是哪版加的、依据哪个 spec」无从追溯。
- **且 Task 1.3 措辞不含该动作** (只写「Version 1.1.0→1.1.1」), 按当前 Tasks 字面执行**不会**补上 —— 缺口会原样 ship。
- 修法: §10 追加 1.1.1 行 (Patch/勘误性质, 记 4 处 `-out=keys` 订正 + 2 段警示 + 来源 spec `secret-guard-nomad-var-put-echo` + 来源 issue Aria #170); Task 1.3 措辞显式纳入「§10 补一行」。
- 顺带核实并**确认为正确的不作为**: 文件头 `Source incidents` 未追加本次 —— 该栏目记录真实泄漏事件, 本次是文档勘误 (无实际泄漏), 不应入栏; 正确落点就是 §10。

## Minor (建议修复 — 8)

**m-1. §审计轨迹 R2 计数「2C」实为 4C, 且 R3 一项混用两种口径** (`proposal.md:9`)。重新机械聚合: R2 = **4C+13M+24m** (M/m 两数精确, 唯 C 少记 2); R3 = 原始 **3C+15M+15m**, 而行内写「去重 2C+15M」—— C 去重、M 取原始、m 整个略去, 三个数三种口径。建议统一标注 (如「R2 4C+13M+24m → R3 3C+15M+15m (去重后 2C)」)。R1 的 1C+13M+21m 复测**完全精确**。

**m-2. §测试面盲区 范围与计数口径不匹配** (L44, R3 m-2 未闭)。「37 处 / L56-L418」只针对 `/v1/var/` (三数精确), 而 `nomad var` **CLI** 用例在 `:55` / `:601` / `:681`, **三条全在该区间外**。建议拆两句写清。

**m-3. rule6_note 同时声称「Rule #6 不适用」与提供「substitute」** (L117-121, R3 m-4 未闭)。「结构性前提不成立」框定下逻辑上不需要 substitute; 同 hook 的 archive 先例 (`openspec/archive/2026-06-19-secret-guard-exfil-coverage-iteration/`) 用的是 substitute 框定。两种框定下实质证据面都成立 (SC-1 baseline-failing 我已实测五条 0→2), 不阻塞 Phase B; 但按 Rule #10「AI 任何自作主张的流程判断必须写进 handoff 请复议」, 建议二选一并挂 owner 复议。

**m-4. `secret-guard.test.sh:8` 陈旧注释 `# Coverage: ~50 cases`** (R3 m-5 未闭)。实读确认未改, 实况 347 (改后 363)。它已污染过本 spec 一次 (R1 把 347 写成 ~50), 本 cycle 正要动这个文件, 顺手改一行止血。

**m-5. 决策表「提示文案 **不改**」无验收锚点** (R3 m-6 未闭)。全部 SC 都是 exit code 断言, 测不到 heredoc 文本是否被改; 而 rule6_note 的免测论证**依赖**「本版未改任何提示文案」这一前提。建议 SC-5 追加机械判据: 「`git diff` 中 `secret-guard.sh` 改动**仅限** risky_patterns 数组内 1 行新增, heredoc (L654-L682) 零改动」—— 同时给 rule6_note 提供可证伪支撑。

**m-6. §Impact「aria 子模块 5 文件」口径易误读** (L99, R3 m-7 未闭)。5 指版本同步 5 文件, 而本 cycle aria 实际改动 **7** 文件 (再加 `secret-guard.sh` + `secret-guard.test.sh`)。建议「aria 子模块: 2 交付文件 + 5 版本同步文件」。

**m-7. SC-2 排除 `-o /dev/null` 的理由不精确, 且 R3 建议的转出未落 (新)**。SC-2 写「`-o /dev/null` 是 curl 专用 flag, **与 nomad 无关**, 不列」。**删除本条是对的** (实跑 `nomad var put -o /dev/null …` → `flag provided but not defined: -o`, 命令根本非法); 但「与 nomad 无关」对 **hook** 不成立 —— `:390` 的 credit 是**无工具语境**的裸正则, 实测注入版 `nomad var put … -o /dev/null` = **0** (被 credit 放行)。建议措辞改成「nomad CLI 不接受 `-o` (实跑 `flag provided but not defined`), 故该形态不可能出现」, 并把「`-o /dev/null` credit 无工具语境」并进 §转出 2 —— 它与已记录的「裸扫 `-v` 会撞 `grep -v` credit」是**同一根因** (credit 正则不看调用的是哪个工具), 一起修比分两次便宜。

**m-8. §Impact 的 FP 枚举漏掉最高频的一类: `nomad var put --help` (新)**。实测 tail 变体: `nomad var put --help` = **2**、`nomad var put -h` = **2** (原版均为 0)。它落在「`put` 后真有空格」这条通则内, 但 §Impact 只举了 commit message 一例; 而**本 spec 自己的 dogfood 四次里就有两次是读 `--help`**, 说明这是开发者最常撞的形态。建议 §Impact 的 FP 句显式列出 `nomad var put --help`, 让 §转出 4 收口时不必重新发现。

**m-9 (附, 预先存在, 非本变更引入)**: `secret-hygiene.md` §5.1 写 `secret-guard.test.sh | 208 regression cases`、§0 与 §5.4 写「251 self-tests」, 实况 **347** (改后 363); 同表 `secret-scan.test.sh | 49` 实跑 **49/49** 正确。本 cycle 正在编辑该文件且正在改变这个计数, 顺手同步的边际成本近零 —— 若不同步, ship 后该 SOT 的陈旧度再加一档。

---

## 建议

1. **M-2 优先于其余全部**。它是唯一会造成**实际交付缺失**的项 (SC-6b/6c/负向锚点三条用例不入套件), 其余六项都是文字口径。建议直接取消写死总数, 改成「SC-1~SC-6 每条 ≥1 用例」, 从根上消掉这个已连错两轮的算术。
2. **M-1 / M-3 / m-9 是同一次编辑可全清的机械项** (一个数字 + 一行表格 + 三处计数), 建议一并落。
3. **把本轮的三列 exit code 对照表 (C-1 段) 直接搬进 proposal 或 Tasks 1.2 的用例清单** —— 它已经是可执行的 fixture 规格 (含期望值), 实施者照抄即可, 且天然覆盖 M-2 要求的 SC-6 三条。
4. **m-3 (rule6_note 框定) 建议在 handoff 挂 owner 复议**而非本轮自行裁定 —— 按 Rule #10, 这属「AI 自作主张的流程判断」类。

---

## 评估

**是否可以继续?**: **REVISE** (未 CONVERGED, 但已逼近)。

**理由**: R3 的**唯一 Critical 已实测真闭合** —— 我用本 spec 允许的实现造了带尾边界的注入版, SC-1~SC-6 的每一格期望值与实测 exit code **逐格一致**, 且完整 347 条回归 **347/347 全绿**, 说明「SC 集合无解」不再成立; 处置方式也不是把矛盾写进文档, 而是把 SC-4 前两条错误的预估值改成了实测值, 并用「实现约束」块封死了我 R3 预警的错误修法 (实测 notail 变体确实同时让 grep/echo 转 2、putty 转 2, 与该块因果陈述逐字吻合)。我 R3 的 M-1「SOT 订正漏 §4.4、比订正前更糟」经对当前工作树重扫**证伪并撤回** —— 四个推荐位全部订正, 全文 `-out=keys` 仅剩 2 处且均在警示语境, SC-7(b) 的负向谓词对真实数据求值非真空且为绿。事实底座依旧无一处失真: `:406` / 140 / 347 / 37 / L56 / L418 / 5 个脚本 / 1.65.1→v1.65.2 / 三子命令 `-out` 枚举 / `Invalid value` 原文 / `-verbose` stderr 原文 / `.Items | keys` 与 `keys[]` 的 0-vs-2 分野 / Nomad 文档 200 / 四个节号 / R1 三元计数, **全部实跑复核通过**。

仍判 REVISE 而非 PASS 的原因只有一条实质项: **M-2 (SC-6 无 Task、断言数不可导出且算错) 是 R3 M-4 的原样复现, 跨一整轮零改动**, 而实测确认 `nomad var list`、nomad CLI 版 `jq '.Items | keys'`、以及 `keys[]` 负向锚点三条用例在现套件中**确实不存在** —— 按当前 Tasks 字面执行会漏掉它们, 其中 SC-6c 恰是「SOT 与 hook 不再分裂」的唯一机械锚点, 而防止这种分裂正是本 spec 的立项理由。另两个 Major (§Impact「3 处」最后一处未同步、SOT §10 缺 1.1.1 行) 均为单点文本, 但后者会让已落地的交付物带着版本审计空洞 ship, 且 Task 措辞不含该动作故不会被自然修掉。三项 Major 加八项 Minor **全部是机械可核对的收尾编辑, 零设计/范围再讨论**, 预期 R5 一次编辑即可收敛为 PASS。

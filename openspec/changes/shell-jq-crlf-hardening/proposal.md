# shell-jq-crlf-hardening — 系统性加固 shell 脚本 jq 输出消费点对 Windows CRLF 的鲁棒性

> **Level**: 3 (Full — proposal.md + tasks.md;含 1 security 项 + 跨 4 脚本 + 新建可复用测试框架 + 新 convention,跨 hooks/skills/standards 三域)
> **Status**: ✅ **Approved** (Phase A.2 post_spec CONVERGED 2026-05-30 via challenge R1 (2 REVISE / 2 Critical) → Rev1 → R2 (code-reviewer PASS + qa REVISE / 1 NEW Major) → Rev2 → R3 (PASS, 0 new);verdict PASS, 无振荡)。实施前拦截 2 load-bearing Critical (C1 非空洞断言 + C2 content 正文篡改) + 4 Major。审计报告: `.aria/audit-reports/post_spec-R3-2026-05-30-shell-jq-crlf-hardening-consolidated.md`。ready for A.2 task-planner。

> **Rev2 changelog (post_spec R2 闭合, 2026-05-30, R2 = 1 PASS / 1 REVISE / 1 NEW Major + 2 Minor)**:
>   - **NEW-M (qa) content 保真测试接入点歧义**: SC-3 "逐字节一致" 未指明 hook 写回输出的捕获方式 → 实施者可能 mock 绕过真实路径产空洞测试 (与 C1 同根: 可观测性不足)。修: 锚定**测试接入点 = hook stdout (重注入的 tool_response envelope)**。code-reviewer R2 已核实写回链路: `secret-scan.sh` content 经 行 225 写 tmpfile → sed in-place redact → 行 320 `cat` 回读 → 行 368 `jq --arg c` 重注入 envelope 到 stdout。测试: 截获 hook stdout → `jq -r '.tool_response.output'` 取回写 content → 与输入 content 逐字节比对 (除 redact 替换 span)。SC-3 + tasks 2.3 补此接入点。
>   - **NEW-m1 (qa) 框架 self-check 自身防空洞**: 两形态 CR 自检若 shim 实现有 bug 可能 trivial-pass。修: tasks 1.2 要求 self-check **双向** (不激活 shim 时断言 CR 不存在 + 激活后断言存在),与站点测试同构防空洞。
>   - **NEW-m2 (qa) 双向断言两态执行机制**: "两态翻转" 未指定执行方式 (跑未打补丁版 vs 条件切换)。修: tasks 2.2 指定机制 = 同一 test run 内对 fixed hook 与 pristine-copy(去掉 fix 的副本) 各跑一次 (复用 #132 hotfix 验证 nofix 时用的 `sed` 去 fix 造副本手法),断言两态结论相反。
>   - **(非阻塞) code-reviewer 文档 nit**: Status 行 "2C+4M+4Min" 计数与 changelog "2 PASS/2 REVISE" 口径不同 — 前者数 finding,后者数 vote,语义不冲突,保留。

> **Rev1 changelog (post_spec R1 audit 闭合, 2026-05-30, challenge 模式 R1 = 2 PASS / 2 REVISE / 2 Critical)**:
>   - **C1 (qa) 非空洞断言缺失**: secret-scan 的 `exit 0` 静默 bypass 无可观测失败信号,Spec 未规定如何构造非空洞 nofix 断言 → 实施者可能复用现有正向 `expect_redact` 框架产出空洞测试。修: §What 加 **双向断言结构** (silent-bypass 站点必须 nofix 期望"无 REDACT" → fix 期望"有 REDACT",两态翻转才算非空洞);tasks 1.2 / 2.2 显式要求。
>   - **C2 (code-reviewer) content 正文篡改**: `secret-scan.sh` 的 `content` (行 123) 是写回 `tool_response.output` 供 LLM 消费的**数据正文**,非门控/比较值。笼统 `tr -d '\r'` 会删掉正文里合法 CR (被扫描文件本身 CRLF) → 篡改用户内容,与本 Spec "语义无损" 前提**直接冲突**。修: 引入 **「门控/比较值」vs「数据正文」分类原则** — 只对 type-check 门控 (行 116) + tool (行 118, 喂 `case`) 剥 CR;**content (行 123) 不剥**。§What 加决策表。
>   - **M1 (tech-lead+qa+cr) 框架须覆盖异构消费形态**: secret-guard 用 `readarray < <(jq)`,secret-scan 等用 `$(printf\|jq)` 命令替换 — 两形态 CR 注入/剥除路径不同。修: tasks 1.x 明确框架须覆盖 readarray-pipe + command-subst 两形态 + 各形态 CR-保留自检 + content 保真负向用例。
>   - **M2 (4/4 corroborate) check_parity 布尔降级 T2→T3**: 实测 `jq --argjson x "$(printf 'true\r')"` 正确解析 (RFC 8259 `\r` = 合法 JSON whitespace),`OVERALL_PARITY` 等唯一下游是 `--argjson` (行 400-402),无 bash 字符串比较 → CR 无害。修: 站点表布尔行 T2→T3。
>   - **M3 (code-reviewer) 缺 strip 策略决策表**: `${VAR%$'\r'}` 只删尾部一个 CR (单值/门控适用),`tr -d '\r'` 删全部 (多行 field-split 适用),content 正文不剥 — Spec 并列两者无判定规则。修: §What 加决策表。
>   - **M4 (qa) SC 不可机验**: "benign 输出仍 redact" / "幂等检测正确" 措辞模糊。修: SC 操作化为可机验断言 (见下)。
>   - **m1 (4/4) grep guard 需豁免**: 模式 `$(jq` 会对 15 处 `ENTRY=$(jq -n …)` 构造器 + T3 已知安全站点误报。修: tasks 5.1 加 allowlist/豁免注释机制 (类比 `# secret-leak-ok-explicit`),区分 `jq -n` 构造 (豁免) vs `jq -r '.field'` 读取 (需防护)。
>   - **m2 (code-reviewer) setup_relay 站点纠正**: 行 48 `jq -c > file` 被行 44 `__aria_cwd` (`[ -d ]` 门控) 保护 — 真正修复点是行 44 捕获剥尾 CR,行 48 不需独立 fix。修: 站点表纠正。
>   - **m3 (tech-lead) multi-terminal ship 卫生**: 本仓近期高频并发 ship。修: tasks 7.x 引用 `feedback_concurrent_sot_conflict_mechanical_resolve` + `feedback_claude_md_project_status_high_contention` + push 前 `git fetch`。
>   - **m4 (qa) convention exception**: `tr -d '\r'` 删合法 `\r` (罕见, 如 base64 含 CR) 属已知局限。修: convention exception 模板收录。
>   - **REFUTE (code-reviewer)**: "累加器累积污染" 不成立 — jq 转义字符串内 CR + argjson 每轮 re-parse,不累积。T3 文档说明即可,无需代码改动。
> **Change ID**: `shell-jq-crlf-hardening`
> **Source**: Forgejo Aria [#132](https://forgejo.10cg.pub/10CG/Aria/issues/132) hotfix (v1.34.1) 的 carry-forward — 单点修复时勘察出同类站点散落多处
> **Target version**: aria-plugin v1.36.0 (tentative — v1.35.0 已被 #58 占用 2026-05-30;新增测试框架 + convention = MINOR;ship 前须 `cat aria/VERSION + plugin.json` 复核当前版本,见 memory `feedback_dec_ship_target_staleness_verify`)
> **Risk class**: 防御性,**但非全盘"剥除即安全"** (R1 C2 修正) — 对**门控/比较值** (type-check / cwd / marker / 单值) 剥 CR 语义无损;对**数据正文** (secret-scan 的 `content` = 写回 LLM 的工具输出) **不得**整体剥 CR (会篡改用户内容)。无 API break;按下方决策表区分处理。
> **同源家族**: #61 (v1.21 GBK locale) / #131 (v1.30.3 None guard) / #132 (本源, secret-guard CRLF) — aria-plugin Windows CRLF/编码边界 bug 家族

---

## Why

#132 暴露的不是单点 bug,而是一个**系统性脆弱模式**:Windows native jq builds 输出 CRLF,而 shell 的多种 jq 输出消费方式(`readarray -t`、`VAR=$(jq …)`、`$()` 命令替换)都**只 strip `\n` 不 strip `\r`**,使每个被捕获的字段/值携带尾部 `\r`。后果按消费点用途而异:

- **type/相等比较**:`[[ "$x" != "string" ]]` 在 `"string\r"` 上判真 → 逻辑反转
- **redaction 门控**:`!= "string" && exit 0` → 静默跳过(secret 泄漏)
- **幂等 marker 比对**:`"已安装的命令\r" != "期望命令"` → 重复注入
- **布尔捕获**:`OVERALL_PARITY="true\r"` 喂 `--argjson` / `== "true"` → 解析/判定失败

#132 hotfix 已修最危险的一处(`secret-guard.sh`,P0 阻断全部工具)。本 Spec 把同一根因在**全 plugin shell 脚本**层面根治,并建立**回归防线**(可复用 CRLF 测试框架 + grep guard + convention),防止未来新增脚本重蹈覆辙。

**关键升级 (Phase A 调研实证)**:carry-forward 时以为同类站点都是「低severity」,但勘察发现 `secret-scan.sh:116`(PostToolUse 姊妹 hook)同样的 type 校验 `[[ "$tool_type" != "string" ]] && exit 0` 在 CRLF 下会**静默跳过整个 redaction** → secret-shaped 输出未脱敏流入 LLM context。这是**静默 secret 泄漏**(比 #132 的 fail-closed 更隐蔽,因为无报错),属 **security 级**,非 hygiene。

---

## What

对 aria-plugin 全部 shell 脚本的 jq 输出消费点,按**「门控/比较值」vs「数据正文」分类**应用 CR 处理(R1 C2/M3 修正 — 不是无差别剥除):

#### CR 处理决策表 (load-bearing — 实施必须遵循)

| 消费形态 | 值的用途 | 处理 | 理由 |
|---------|---------|------|------|
| `readarray -t < <(jq …)` 多行 field-split | 门控/字段值 | jq 管道末 `\| tr -d '\r'` | 多行各带 CR,`${VAR%}` 只删最后一个不够 |
| `VAR=$(jq -r '.x')` / `VAR=$(…\|jq)` 单值 | 门控/比较值 (type / cwd / marker / 布尔) | 捕获后 `VAR="${VAR%$'\r'}"` (只剥尾) | 单值只有 1 个尾 CR;不碰内部,最小副作用 |
| `content=$(…\|jq -r '.tool_response.output')` | **数据正文** (写回 LLM / 文件正文) | **不剥 CR** | content 是任意用户输出,CR 是合法字节;剥除 = 篡改 (违反语义无损) |
| `ENTRY=$(jq -n --arg …)` 构造器 | 生产 JSON 喂 `--argjson` | **不处理** (豁免) | jq -n 构造非消费上游;`--argjson` 容忍 CR (RFC 8259 whitespace) |
| `jq -c '{…}' > file` 写文件 | jq 为生产者 | **不处理** (若有 shell 门控如 `__aria_cwd`,改门控捕获处) | 无 shell 消费其 stdout;下游 JSON parser 容忍 CR |

**关键原则**: 只对**进入 shell 条件判断/字符串比较**的值剥 CR;**数据正文**与 **jq 构造器输出**不动。secret-scan 的修复点是 type-check 门控 (行 116) + tool (行 118 喂 `case`),**绝不**含 content (行 123)。

#### 工作项

1. 按决策表处理 T1/T2 站点 (门控值剥 CR;content 正文不动)
2. **新建** 可复用 cross-platform CRLF 回归测试框架(泛化 #132 jq-shim:awk 每行补 `\r\n` 模拟 Windows native jq + PATH prepend)— 须覆盖 **readarray-pipe + command-subst 两种消费形态**,各形态自检 CR 确被注入/保留 (防空洞)
3. **silent-bypass 站点 (secret-scan) 须双向断言**:nofix 期望"无 REDACT"(bug 复现) → fix 期望"有 REDACT" + content 正文 CR 保真,两态翻转才算非空洞
4. **新建** grep-based 回归 guard:扫描新增未防护 jq **读取**消费点(`< <(jq` / `VAR=$(…jq -r '.field')`);配 allowlist/豁免注释(`jq -n` 构造器 + T3 已知安全站点)
5. **新增** convention:`standards/conventions/shell-jq-crlf-hygiene.md`(secret-hygiene 同结构:决策表 + 正向 pattern + exception 模板,exception 收录"数据正文不剥"+"tr 误删合法 CR")

### 站点清单 (Phase A 调研 grounded,按风险分层)

| Tier | 站点 | 模式 | 处理 (按决策表) | 后果 |
|------|------|------|----------------|------|
| **T1 security** | `hooks/secret-scan.sh:116` | `tool_type=$(…\|jq -r '.tool_name\|type')` + `!= "string" && exit 0` | 门控值 → 剥尾 CR | CRLF → 静默跳过 redaction → **secret 泄漏到 LLM context** |
| **T1 security** | `hooks/secret-scan.sh:118` | `tool` 捕获 (喂 `case "$tool"`) | 比较值 → 剥尾 CR | CR → `case "$tool"` 错配 |
| **T1 (不剥)** | `hooks/secret-scan.sh:123` | `content` 捕获 (写回 LLM 正文) | **数据正文 → 不剥** (R1 C2) | 剥除会篡改用户内容;CR 不影响 redaction 门控 |
| **T2 correctness** | `setup_relay.sh:44` | `__aria_cwd=$(…\|jq)` (门控 `[ -d ]`) | 门控值 → 剥尾 CR | CR → `[ -d "$cwd/.aria" ]` 失败 → relay 静默不写缓存 (亦保护下游 :48 写文件) |
| **T2 correctness** | `setup_relay.sh:60,71` | `cmd=$(jq -r '.statusLine.command')` 安装检测 marker | 比较值 → 剥尾 CR | CR 破坏 marker 比对 → 重复注入 |
| **T2 correctness** | `setup_relay.sh:133,134` | 注入的 runtime statusLine `used`/`model=$(…\|jq)` | 门控/显示值 → 剥尾 CR (注入片段内) | 用户 Windows 机每次渲染 → CR 进 relay cache |
| **T2 correctness** | `aria-doctor/check_context_relay.sh:53` | `cmd=$(jq -r '.statusLine.command')` | 比较值 → 剥尾 CR | relay-install 检测误判 |
| **T3 hygiene (验证)** | `check_parity.sh:383,386,389` | `OVERALL_PARITY=$(jq 'all(…)')` 等布尔 | **R1 M2: 实测 `--argjson` 容忍 `true\r` → 无害,文档说明即可** | 唯一下游 `--argjson` (行 400-402),无 bash 比较 |
| **T3 hygiene** | `check_parity.sh` / `push_all_remotes.sh` `RESULTS_JSON=$(…\|jq '. + [$entry]')` | JSON 累加器 (jq 生产者) | **不处理** (R1 REFUTE: jq 转义串内 CR + argjson re-parse 不累积) | — |
| **T3 hygiene** | `aria-doctor/check_secret_guard_install.sh:74-76` | `state`/`sub`/`adv` 显示串 | 显示串 → 剥尾 CR (按需) | CR 显示瑕疵 |
| **豁免** | `*:ENTRY=$(jq -n --arg …)` (15 处) | jq 构造器 | **不处理 + grep guard 豁免** | 构造非消费;`--argjson` 容忍 CR |
| **已修 (#132)** | `hooks/secret-guard.sh:118` | `readarray < <(jq)` | (v1.34.1 已加 `\| tr -d '\r'`) | — |

### Key Deliverables

- `hooks/secret-scan.sh` — T1 加固(3 站点)
- `aria/skills/aria-context-monitor/scripts/setup_relay.sh` — T2(注入片段 + 安装检测)
- `aria/skills/aria-doctor/scripts/check_context_relay.sh` + `check_secret_guard_install.sh` — T2/T3
- `aria/skills/git-remote-helper/scripts/check_parity.sh` + `push_all_remotes.sh` — T2/T3
- `aria/hooks/tests/lib/crlf-shim.sh`(或等价)— 可复用 CRLF 测试框架(jq-shim 泛化)
- 各受影响脚本的 CRLF 回归测试(复用框架)
- grep-based 回归 guard(test 阶段 / `aria-doctor` 检查项)
- `standards/conventions/shell-jq-crlf-hygiene.md`(新 convention)+ CLAUDE.md 索引

---

## Impact

| 维度 | 影响 |
|------|------|
| **secret-scan.sh** (hook) | 行为修正:Windows 上恢复 redaction(此前静默 bypass);Linux/macOS 无变化(无 CR) |
| **setup_relay.sh 注入片段** | 已注入用户 settings 的旧 statusLine 行需 re-setup 才更新;`setup_relay.sh` 幂等注入逻辑须兼容旧片段检测 |
| **git-remote-helper** | 防御性归一,Linux 行为不变 |
| **回归测试** | 新增 cross-platform CRLF 框架,future-proof;不依赖真实 Windows runner |
| **convention** | standards 新增 1 文档;CLAUDE.md 信息地图 +1 行 |
| **向后兼容** | 全部语义无损(CR 在这些上下文无合法意义);无 API/config break |

### Risk / 注意

- `setup_relay.sh` 的注入片段修改需保证**幂等检测兼容**:旧片段(无防护)与新片段(有防护)的 marker 比对,避免 Windows 用户卡在"检测到旧片段但内容不符 → 反复注入"。
- T3 JSON 累加器:确认 jq 确实容忍 CR(作 JSON whitespace);若确认无害可降级为「文档说明」而非代码改动,避免过度改动(Phase B 验证)。

---

## Success Criteria (R1 M4: 操作化为可机验断言)

- [ ] 决策表中标「剥 CR」的全部门控/比较站点应用对应策略 (多行 `tr -d '\r'` / 单值 `${VAR%$'\r'}`);content (secret-scan:123) 验证**未被改动**
- [ ] **secret-scan 双向非空洞断言** (机验): CRLF shim 激活下 —— (a) **nofix**: 含 secret-shaped 的工具输出 → hook stdout **不含** `REDACTED` (bug 复现, silent bypass);(b) **fix 后**: 同输入 → hook 输出**含** `REDACTED`。两态必须翻转 (仅 (b) 通过 = 空洞,测试失败)
- [ ] **content 正文保真** (机验,R2: 含测试接入点): **接入点 = hook stdout 重注入的 tool_response envelope** (`secret-scan.sh:368 jq --arg c` 回写)。CRLF shim 下,被扫描 content 含合法 `\r` (如 CRLF 文件正文) → fix 后截获 hook stdout → `jq -r '.tool_response.output'` 取回写 content → (a) secret-pattern 仍被 redact;(b) 非 secret 的正文 `\r` **不被**删除 (与输入 content 逐字节一致,除 redact 替换 span 外)。禁止 mock hook 内部路径
- [ ] **setup_relay 幂等** (机验): CRLF shim 下连续运行 `setup_relay.sh` 两次 → settings.json 中 statusLine 注入条目数**第二次 == 第一次** (不重复注入);注入片段内 `used`/`model` 捕获 CR-safe
- [ ] cross-platform CRLF 测试框架覆盖 **readarray-pipe + command-subst 两形态**,各形态 sanity self-check **双向**断言 (R2: 不激活 shim → CR 不存在;激活 → CR 存在;防 shim 实现 bug 致 trivial-pass) (单一 SoT,被 hook + skill 测试复用)
- [ ] grep guard 拦截新增未防护 jq **读取**消费点;**自测非空洞**: 故意引入一处未防护 `jq -r '.field'` 捕获 → guard 失败;且对 15 处 `jq -n` 构造器 + T3 已知安全站点**不误报** (allowlist/豁免生效)
- [ ] `standards/conventions/shell-jq-crlf-hygiene.md` 落地 + CLAUDE.md 索引;含 CR 处理决策表 + 正向 pattern + exception (数据正文不剥 / `tr -d '\r'` 误删合法 CR 局限 / #61·#131·#132 同源家族清单)
- [ ] 全量 hook + skill shell 测试 PASS(secret-guard 225 + secret-scan 既有 + 新增 CRLF case);Linux LF 既有行为零退化
- [ ] Rule #6 substitute:deterministic structural(shell 脚本非 LLM Skill)= 双形态 shim fixture + 双向非空洞验证 + content 保真负向用例 + dogfood,per `feedback_deterministic_structural_skill_rule6_substitute`

---

## 关联

- 本 Spec 是 #132 hotfix (v1.34.1) 的系统性 follow-up
- 同源 bug 家族 #61 / #131 / #132 — 可在 convention 中统一收录为「Windows CRLF/编码边界」检查清单
- triage audit trail:`.aria/triage-report.json` + `.aria/triage-comment.md` (#132)

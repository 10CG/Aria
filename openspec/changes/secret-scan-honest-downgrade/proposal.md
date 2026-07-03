# secret-scan-honest-downgrade

> **Status**: ✅ **Approved (owner sign-off 2026-07-03)** — post_spec CONVERGED (R4 3/3 PASS unanimous, verdict PASS 0 Critical/0 Major; 轨迹 R1→R2→R3→R4 = 3→2→1→0 REVISE)。Phase B 执行中。审计报告 `.aria/audit-reports/post_spec-R4-*-secret-scan-honest-downgrade.md`。
> **Level**: 2 (Minimal — proposal only; hook 行为降级 + cross-repo 文档诚实化, 无新增能力)
> **Target**: `aria/hooks/secret-scan.sh` + `aria/hooks/tests/secret-scan.test.sh` + `aria/README.md` + `aria/README.zh.md` (aria-plugin) · `standards/conventions/secret-hygiene.md` + `standards/conventions/shell-jq-crlf-hygiene.md` (standards) · 主仓 root `VERSION` — **cross-repo (3 repos)**
> **Target version**: aria-plugin v1.50.2 → **v1.51.0** (MINOR — 改 hook 观察行为 [warn-only detection 取代无效 redact, 且新增 additionalContext/systemMessage 告警 = additive] + 撤回文档宣称能力; backward-compat: hook 仍 `exit 0` always、仍扫描、无消费者依赖"有效 redaction")
> **Forgejo issue**: [aria-plugin #91](https://forgejo.10cg.pub/10CG/aria-plugin/issues/91) (part②; part① 已 v1.50.2 修) · triage comment [#14312](https://forgejo.10cg.pub/10CG/aria-plugin/issues/91#issuecomment-14312)
> **决策记录**: [DEC-20260703-001](../../../.aria/decisions/DEC-20260703-001-secret-scan-honest-downgrade.md)
> **拆出后续**: [aria-plugin #92](https://forgejo.10cg.pub/10CG/aria-plugin/issues/92) (B 防御反馈闭环, 依赖本 change 先 ship)

## Why

`aria/hooks/secret-scan.sh` 是 Aria 两层防泄密的**第二层** (PostToolUse)。本意: 命令跑完后扫描 tool output 里的 secret-shaped 内容, **redact (涂黑) 后再给 Claude / 转录看**。

**问题**: 这个 redaction **架构性做不到** —— claude-code-guide 查官方 hooks-guide 坐实 (2026-07):
- PostToolUse **无** `updatedToolOutput` 字段; hooks-guide line 891: *"PostToolUse hooks can't undo actions since the tool has already executed"*。
- hook stdout **不替换**已捕获的 tool result; `suppressOutput` 仅隐藏 hook 自身 stdout (transcript UI), **tool result 照喂 model**。
- **这不是 version-dependent, 是架构性不可用**。

**同一核实确认 warn-only 渠道可行** (支撑本 change 的 reframe, 非又一个未验声明): claude-code-guide 列举 PostToolUse **支持**的输出字段含 `hookSpecificOutput.additionalContext` (注入 Claude context) 与 `systemMessage` (operator 可见告警) —— 二者是**被官方文档确认 honored** 的渠道 (与 redaction 不同)。注意: 当前 hook 代码从未真正 emit `additionalContext` (只 emit 了 CC 忽略的 mutated stdout), 故本 change 的告警是**新增可观察行为**。

**后果 (真实危害 = 误导性安全宣称)**: 多处**文档 + 运行时输出**宣称"REDACT / tool_response 已改写", 致 operator **过度信任第二层**。全仓 grep 核实 (R1 knowledge-manager + tech-lead 补全), 虚假声明散落 **3 repo**:

| 位置 | 声明 | 性质 |
|------|------|------|
| `aria/hooks/secret-scan.sh` header (L2/70/73/76) | "scan ... and redact" / "emit redacted output" | 描述空操作 |
| `aria/hooks/secret-scan.sh` **运行时** L342 stderr | **"[secret-scan] REDACTED N secret-shape matches"** | **运行时**假声明 (最刺眼, operator 每次命中都看到) |
| `aria/hooks/secret-scan.sh` L355 stderr / L363 log tag | "PARTIAL REDACTION WARNING" / `SCAN-REDACT` (写 `~/.claude/logs/secret-scan.log`) | 运行时 + 持久 log 假声明 |
| `aria/hooks/secret-scan.sh` redact-design 注释 **散布全文** (L35-42 header / L77 / L325-339 Option A/B/C 设计块 / L345-346 stderr / L368 + 任意其他) | **"version-dependent" / "best-effort" / "Test in actual Claude Code session" / "Option A/B/C" 设计残迹** + 徒劳验证指引 | **与 Why 自身"架构性不可用非版本相关"结论矛盾** (R2 km + R3 qa); **枚举行号连续两轮漏残留 → 改 scope-based (内涵) 清除**。**排除 L124** (input 字段名版本差异, 与 redaction 无关) |
| `aria/README.md` L33 / L153 / **L154** | "REDACT ... before reaching LLM" / **"replaces secret values in tool_response"** | 事实上做不到 (L154 独立字面假声明) |
| `aria/README.zh.md` L33 / L153 / **L154** | 中文镜像同上 ("进 LLM 前 REDACT" / "替换 tool_response 中的 secret 值") | 中文用户同受误导 |
| `standards/conventions/secret-hygiene.md` **L264** | **"tool_response 已被改写 (secret value 替换为占位)"** | **字面虚假声明** (SOT, Rule #7 指向) |
| `standards/conventions/secret-hygiene.md` L255 | "PostToolUse output 扫描 **+ REDACT**" | 同上 |
| `standards/conventions/shell-jq-crlf-hygiene.md` L14 | "跳过 redaction = secret 泄漏" | 措辞连带 |

**核实清白 (不改, 负向)**: `CLAUDE.md` Rule #7 只讲 operator redirect (`>/dev/null`), **未**宣称 PostToolUse 兜底 → 不动 (R1 km 复核确认)。`README.zh.md` L146 是 PreToolUse secret-guard BLOCK 语义 (不是 PostToolUse redaction) → 不动。`CHANGELOG` 历史条目属如实记录 → 不回填。主仓 root i18n README (README.{zh,ja,ko}.md) grep 无 secret-scan 内容 → 不动。

**本 change (#91 A) = 诚实降级**: secret-scan 停止宣称 redact (代码 + 文档 + 运行时输出 + 持久 log tag), 转为它**做得到**的 warn-only 检测器; 撤回 3 repo 全部虚假声明。防御反馈闭环 (检测→记录→反哺 PreToolUse) 是独立能力, 已拆 [#92](https://forgejo.10cg.pub/10CG/aria-plugin/issues/92)。

## What Changes

### 1. `aria/hooks/secret-scan.sh` — 行为降级为 warn-only 检测器
- **保留**: secret-shape 扫描逻辑 (检测能力**完整不变**) + `exit 0` always + matcher (`Bash|Read|Edit|Write|MultiEdit`) + jq fail-soft。
- **删除**: redact-then-reemit-on-stdout 死代码路径 (sed/jq mutation → mutated envelope on stdout, CC 不认, 空操作)。
- **改为**: 命中时**同时**发两渠道告警 (CC 官方支持):
  - `hookSpecificOutput.additionalContext` = 告知 Claude "本段含 N 处疑似 secret, 按已泄露处理, 勿在回复中复述, 建议轮换" (真实缓解: 阻止 Claude 二次复述);
  - `systemMessage` = 提醒 operator "检测到 X 类 secret-shape, 建议轮换"。
- **运行时字符串诚实化** (R1 tech-lead Major): L342 "REDACTED N matches" → "**DETECTED** N secret-shape matches (not redacted — see warning)"; L355 "PARTIAL REDACTION WARNING" → "PARTIAL **DETECTION**"; L363 log tag `SCAN-REDACT` → **`SCAN-DETECT`**。
- **scope-based 清除全文 redact-design 残迹** (R2 km + R3 qa Major, **内涵定义非枚举** —— 枚举已连续两轮漏残留): 删除/重写 secret-scan.sh 中**所有**与 redact-reemit / output-mutation 设计绑定的注释 / stderr / log tag / 死代码, 使**无任何文本**暗示 (a) hook 执行或尝试 redaction / tool_response 改写, (b) 该行为 version-dependent 或 best-effort, (c) 指引 operator 手动验证 redaction。**包括但不限于** L35-42 (header) / L77 / L325-339 (Option A/B/C 设计块) / L345-346 (stderr caveat) / L368。替换为架构性不可用框架 (hooks-guide 891)。**排除仅 L124 本行** (input 字段名版本差异, 与 redaction 无关; **相邻 L119-120/L125 "written back to LLM"/reinject 注释描述死掉的 mutate-reinject 设计, 属清除范围** — R4 qa)。
- **jq-missing 分支**: WARN 措辞 "passes through UNREDACTED" → "secret **检测** skipped (jq missing)"。
- **`~/.claude/logs/secret-scan.log` 写入保留但仅 relabel tag** (SCAN-REDACT→SCAN-DETECT); **结构化 `.aria/secret-leak-events.jsonl` 事件记录归 #92** (A/B 分界见 OOS)。

### 2. `aria/hooks/tests/secret-scan.test.sh` — 断言重定向 (保覆盖 + 反转 fidelity)
- **保留**所有 per-pattern / per-tag / PEM 多行 / multi-match-count **检测覆盖** (这些验的是真检测逻辑, 非死代码; 只有末端 stdout-reemit 是死的)。
- 命中用例断言从"stdout=redacted output"改为"**发出 additionalContext + systemMessage (含检测计数)**"。
- **重构 content-fidelity 测试非空转** (L223-236, R1+R2 qa Major; 与 AC-3 对齐, R3 tech-lead 2-pass 传播): warn-only hook **不 emit** `tool_response` → 旧 `jq '.tool_response.output' //""` 落空串 = vacuous-pass → 改为断言 ①hook stdout JSON **无 tool_response-mutation key** (结构性缺席) + ②检测仍在含 CR 内容上**触发告警** (检测测试, 非 mutation-fidelity)。
- **新增**: exit-0-on-match 用例 + jq-missing 路径用例。
- 删死代码后全套回归绿 (数量以实际为准, 非硬编号)。

### 3. `aria/README.md` + `aria/README.zh.md` — REDACT → detect+warn (含 L154)
- 两文件 L33 (表格行) / L153 (注释) / **L154** ("replaces secret values in tool_response" / "替换 tool_response 中的 secret 值"): → "**detect** secret-shaped output + **warn** (additionalContext/systemMessage); **不改写 tool_response** — PostToolUse 架构限制 (hooks-guide 891), 真实防线 = PreToolUse `secret-guard`"。README.zh.md 为中文镜像等义翻译。

### 4. `standards/conventions/secret-hygiene.md` — 撤字面虚假声明 (cross-repo)
- **L264** "tool_response 已被改写 (secret value 替换为占位)" → "**exit 0 always**; 命中发 `additionalContext`/`systemMessage` 告警; **不改写 tool_response** — PostToolUse 架构不支持 (hooks-guide 891), 真实防线是 PreToolUse"。
- **L255** "PostToolUse output 扫描 + REDACT" → "PostToolUse output 扫描 + **告警** (detect-only)"。
- **L257 表格** secret-scan.test.sh "44 regression cases" → 同步为 TASK-002 完成后实测数 (当前已轻微漂移)。
- §5 Layer 2 段: 明确 Layer 2 = PreToolUse `secret-guard` (block, 有效) + PostToolUse `secret-scan` (**detect+warn only**, 非 redaction)。

### 5. `standards/conventions/shell-jq-crlf-hygiene.md` L14 — 措辞连带
- "静默跳过 redaction = secret 泄漏" → "静默跳过 **secret 检测** = 泄漏未被告警"。

### 6. 版本 + CHANGELOG (含 R1 km 补全的 root VERSION)
- aria-plugin v1.50.2 → v1.51.0 六面 SOT (plugin.json/marketplace.json/VERSION/CHANGELOG/README/hooks.json) + root README badge + **主仓 root `VERSION` L29 插件版本行** (R1 km Major, 防 badge-drift 同类事故) + i18n marker (无正文重译, #140 B 档)。standards 无版本号, commit + 双远程。

## Impact
- **Cross-repo (3 repo)**: aria (hook + test + README×2 + 版本文件) + standards (2 conventions) + 主仓 (root VERSION + gitlink)。Phase C = **两协调 PR** (aria + standards) + 主仓 gitlink bump ×2 + **post-merge-master-SHA capture** (`[[feedback_submodule_pointer_post_merge_bump]]`, C.2.4.5 block gate + C.2.5 兜底) + 双远程 parity。
- **无运行时能力损失**: redaction 本是空操作, 删它不减真实保护; **新增** warn-only 告警是 additive。
- **防御姿态更诚实**: operator 不再被"有 output 兜底"误导 (含运行时 stderr); 文档明确 PreToolUse 是唯一可靠层 (part① 已加固)。
- Rule #6: hook (非 Skill), **不触发** `/skill-creator` benchmark; 用 `secret-scan.test.sh` deterministic 回归 substitute。

## Out of scope (归 #92 或不做)
- ❌ 结构化 `.aria/secret-leak-events.jsonl` 事件记录 → #92 (本 change 保留既有 `~/.claude/logs/secret-scan.log` 仅 relabel tag, **不新建**结构化事件流)。
- ❌ 置信度分级 `decision:block` → #92。
- ❌ aria-report 反馈 issue 闭环 (含 staged auto-flip) → #92。
- ❌ 扩大 secret-shape 检测 regex 覆盖 (检测质量话题, 非 honesty change)。
- ❌ 改 PreToolUse `secret-guard.sh` (part① 已 v1.50.2 完成)。
- ❌ 改 CLAUDE.md Rule #7 / README.zh.md L146 (核实非 PostToolUse redaction 声明)。

## 验收标准 (AC)
- **AC-1**: `secret-scan.sh` 命中疑似 secret 时, 输出 JSON **同时**含 `hookSpecificOutput.additionalContext` (提示已泄露/勿复述) **和** `systemMessage` (提示轮换) [两者皆必需, 非任一]; **不含**任何改写 `tool_response`/stdout 的尝试; hook `exit 0`。渠道可行性依据: claude-code-guide 官方文档核实 additionalContext/systemMessage 为 PostToolUse 支持渠道 (见 Why)。**B.2 建议补一次 live-CC-session smoke** (真跑一次确认告警在会话中确实渲染, belt-and-suspenders; 非阻塞, R2 qa Minor)。
- **AC-2**: 以下**具名虚假短语**在对应文件**零残留** (逐短语核, 非 bare `redact` substring — 诚实措辞里合法的 "无法事后 redact"/"not redacted" **不算残留**):
  - `secret-scan.sh` (**intensional 门 — R3 qa; 以下短语为非穷举示例, 枚举已两轮漏残留**): **无任何残留文本**暗示 (a) hook 执行/尝试 redaction 或 tool_response 改写, (b) 该行为 version-dependent/best-effort, (c) 指引手动验证 redaction。示例短语: "REDACTED N ... matches" / "PARTIAL REDACTION WARNING" / `SCAN-REDACT` / "emit redacted output" / "version-dependent" / "best-effort" / "Test in actual Claude Code session" / "Option A/B/C" 设计残迹 / "粘贴假密码验证" 徒劳指引 / L119-120/L125 "written back to LLM"/reinject 死设计注释。**排除仅 L124 本行** (input 字段名版本差异, 非 redaction; 相邻行不豁免 — R4 qa)
  - `README.md` + `README.zh.md`: "REDACT ... before reaching LLM" / "replaces secret values in tool_response" / "进 LLM 前 REDACT" / "替换 tool_response 中的 secret 值"
  - `secret-hygiene.md`: "tool_response 已被改写" / "扫描 + REDACT"
  - **`shell-jq-crlf-hygiene.md` (R2 qa+tech-lead Major, 第 4 文件)**: L14 "跳过 redaction = 泄漏" 已改为 "跳过 secret 检测 = 泄漏未被告警"
  - 且各文件**正向**含 detect+warn 诚实措辞。
- **AC-3**: `secret-scan.test.sh` 全绿; **检测覆盖不减** (per-pattern/per-tag/PEM/multi-count 用例保留); **content-fidelity 测试按 warn-only 重构非空转** (R2 qa Major: 旧 `jq '.tool_response.output'` 在 warn-only 下落 `//""` 空串 = vacuous-pass; 新断言 = ①hook stdout JSON **无任何 tool_response-mutation key** [结构性缺席] + ②检测仍在含 CR 内容上触发告警 [检测测试, 非 mutation-fidelity]); 新增 exit-0-on-match + jq-missing 用例; 死代码删除后无回归。**`secret-hygiene.md` L257 "44 cases" 数字 == 测试文件实测用例数** (R2 qa Minor, 收 TASK-004(c) orphan)。
- **AC-4** (负向): `CLAUDE.md` Rule #7 措辞 + `README.zh.md` L146 **未改动**。
- **AC-5**: 版本一致性 —— aria-plugin 6 面 SOT = v1.51.0 一致 + 主仓 root `VERSION` L29 = v1.51.0 + root README badge 同步 + README.zh 同步 + standards 双远程 parity; 主仓 gitlink bump ×2 (aria + standards, post-merge-master-SHA)。
- **AC-6** (负向): `secret-guard.sh` (PreToolUse, part①) 行为**零改动** + 其回归**非降** (vs 当前 baseline 计数不减, 不硬编 260)。
- **AC-7**: jq-missing 路径 + exit-0-on-match 各有对应测试用例锁定 (R1 qa Minor)。

## Resolved (Rev1 — post_spec R1)
R1 3/3 REVISE, 去重后落地: **[Major]** ①AC-2 grep 自绊 + scope 仅 header (qa+tech-lead) → AC-2 改具名短语逐文件全域含运行时串; ②missed sites (km+tech-lead) → 补 secret-scan.sh 运行时 L342/L355/L363 + README.md/zh L154 + README.zh 整份 + 主仓 root VERSION; ③AC-1 渠道未验 (qa) → 补 claude-code-guide 官方核实引用; ④测试反转/覆盖 (qa) → AC-3/TASK-002 明确保覆盖 + 反转 fidelity。**[Minor]** secret-scan.log 处置 (tech-lead) → OOS relabel-only; "44 cases" 漂移 (km+tech-lead) → TASK-004 同步; AC-6 magic 260 → 非降表述; Phase C SHA discipline → Impact 补; AC-1 且/或→皆必需; jq-missing/exit-0 用例 → AC-7。

## Resolved (Rev2 — post_spec R2)
R2 = tech-lead PASS + km/qa REVISE (收敛中: 均 AC-2 完整性 + 测试机制精度, 非 substance). 去重落地: **[Major]** ①caveat/header 仍 "version-dependent" 自相矛盾 (km, L35-42+L345-349) → What-Changes item1 加"整段重写非逐行" + AC-2 加 "version-dependent"/徒劳验证指引禁短语 + Why 表补行; ②AC-2 漏 "PARTIAL REDACTION WARNING" (qa) → 补入; ③AC-2 漏第 4 文件 shell-jq-crlf-hygiene.md (qa+tech-lead) → 补入; ④content-fidelity 测试 vacuous-pass (qa, warn-only 无 tool_response → `//""` 空转) → AC-3 重构为结构性缺席 + CR 检测测试。**[Minor]** "44 cases" orphan 无 gate (qa) → AC-3 绑测试实测数; AC-1 doc-cite 非 live (qa) → AC-1 加 B.2 live-smoke 建议 (非阻塞)。

## Resolved (Rev3 — post_spec R3)
R3 = km PASS + tech-lead PASS + qa REVISE (收敛尾部). **[Major]** qa 抓出**第三个** redact-design 残迹块 (L325-339 Option A/B/C 设计 + "Test in actual Claude Code session"), 躲过枚举行号 + 字面短语门 —— **meta 洞察: 枚举连续两轮漏残留 → 换 scope-based (内涵) 定义**。落地: What-Changes item1(e) 改内涵指令 (删所有 redact-design 绑定注释/死代码, 排除 L124 input-parsing) + AC-2 secret-scan.sh 改 intensional 门 (无残留文本暗示 redaction/version-dependent/手动验证, 示例短语非穷举) + Why 表更新为"散布全文"。**[Minor]** tech-lead: What-Changes item2(c) 未同步 AC-3 vacuous-pass 重构 (2-pass 传播漏, `[[feedback_spec_v2_body_propagation_2pass]]`) → item2(c) 对齐结构性缺席设计。

## Resolved (Rev3.1 — post_spec R4, CONVERGED)
R4 = **3/3 PASS unanimous** (tech-lead + km + qa). intensional 重构确认根治枚举漏检 (qa: "correctly subsumes every violation found across R1-R3 without needing to name each one"); 既往已解决项零回归 (km); item2(c)↔AC-3 lockstep (tech-lead)。**[Minor 非阻塞, 已 fold]** qa: L119-120/L125 "written back to LLM"/reinject 死设计注释紧邻豁免的 L124 有误读风险 → 澄清"排除**仅 L124 本行**, 相邻死设计注释属清除范围"。**收敛**: post_spec verdict PASS。

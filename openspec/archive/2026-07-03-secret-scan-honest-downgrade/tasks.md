# Tasks — secret-scan-honest-downgrade

> Level 2 · cross-repo (aria + standards + 主仓) · 决策 [DEC-20260703-001](../../../.aria/decisions/DEC-20260703-001-secret-scan-honest-downgrade.md)
> Rev1 (post_spec R1) 补全已并入。依赖顺序: TASK-001 先于 TASK-002 ; 文档 (003-005) 可并行 ; 006 最后。

## aria-plugin 子模块

- [x] **TASK-001** `aria/hooks/secret-scan.sh` 行为降级 — (a) 删 redact-reemit 死代码 (sed/jq mutation + mutated stdout); (b) 命中改**同时**发 `additionalContext` + `systemMessage` 告警; (c) **运行时串诚实化**: L342 "REDACTED N matches"→"DETECTED N ...(not redacted)", L355 "PARTIAL REDACTION WARNING"→"PARTIAL DETECTION", L363 log tag `SCAN-REDACT`→`SCAN-DETECT` (保留 `~/.claude/logs/secret-scan.log` 写入, 仅 relabel); (d) jq-missing 措辞 "UNREDACTED"→"检测 skipped"; (e) **scope-based 清除全文 redact-design 残迹** (R2 km + R3 qa Major, **内涵定义非枚举行号** —— 枚举已两轮漏残留): 删除/重写 secret-scan.sh 中**所有**与 redact-reemit/output-mutation 设计绑定的注释/stderr/log tag/死代码, 使无任何文本暗示 hook redact / tool_response 改写 / version-dependent / best-effort / 手动验证 redaction。**含但不限于** L35-42 (header) / L77 / L325-339 (Option A/B/C 设计块) / L345-346 (stderr) / L368; 替换为架构不可用框架 (hooks-guide 891)。**排除仅 L124 本行** (input 字段名版本差异; 相邻 L119-120/L125 "written back to LLM"/reinject 死设计注释属清除范围 — R4 qa)。**Agent**: `backend-architect`。AC-1/AC-2。
- [x] **TASK-002** `aria/hooks/tests/secret-scan.test.sh` 断言重定向 (**保覆盖 + 反转 fidelity**) — (a) **保留**所有 per-pattern/per-tag/PEM/multi-count 检测用例 (验真检测逻辑, 勿塌缩); (b) 命中断言改"发出 additionalContext+systemMessage(含检测计数)"取代"stdout=redacted"; (c) **重构 content-fidelity 测试非空转** (L223-236, R2 qa Major): warn-only hook 不 emit `tool_response` → 旧 `jq '.tool_response.output' //""` 落空串 = vacuous-pass; 新断言 = ①hook stdout JSON **无 tool_response-mutation key** (结构性缺席) + ②检测仍在含 CR 内容上**触发告警** (检测测试, 非 mutation-fidelity); (d) **新增** exit-0-on-match + jq-missing 路径用例; (e) 死代码删后全绿; (f) 测试实测用例数 == secret-hygiene.md L257 记录数 (供 TASK-004(c) 同步)。**Agent**: `qa-engineer`。依赖 TASK-001。AC-3/AC-7。
- [x] **TASK-003** `aria/README.md` + `aria/README.zh.md` **各 L33/L153/L154** — "REDACT...before LLM" / "replaces secret values in tool_response" / 中文镜像 → "detect+warn; 不改写 tool_response (架构限制), 真实防线 = PreToolUse secret-guard"。**注意 L154 独立假声明 + zh 整份镜像** (R1 km)。**不动** README.zh.md L146 (PreToolUse 语义)。**Agent**: `knowledge-manager`。AC-2/AC-4(负向)。

## standards 子模块 (cross-repo)

- [x] **TASK-004** `standards/conventions/secret-hygiene.md` — (a) 撤 L264 字面虚假声明 ("tool_response 已被改写"); (b) L255 "REDACT"→"告警 (detect-only)"; (c) **L257 表格 "44 regression cases" 同步**为 TASK-002 完成后实测数 (已漂移, R1 km/tech-lead); (d) §5 Layer 2 段明确 secret-scan=detect+warn 非 redaction, PreToolUse 是有效层。**Agent**: `knowledge-manager`。AC-2 (核心 SOT)。
- [x] **TASK-005** `standards/conventions/shell-jq-crlf-hygiene.md` L14 — "跳过 redaction=泄漏" → "跳过 secret 检测=泄漏未被告警"。**Agent**: `knowledge-manager`。AC-2。

## 收尾

- [x] **TASK-006** 版本 + CHANGELOG — aria-plugin v1.50.2→v1.51.0 六面 SOT + root README badge + **主仓 root `VERSION` L29 插件版本行** (R1 km Major, 防 badge-drift) + i18n marker (无正文重译)。**Agent**: `general-purpose`。依赖 TASK-001~005。AC-5。

## 负向 / 守卫 (审计+B.2 验)

- [x] **G-1** `CLAUDE.md` Rule #7 + `README.zh.md` L146 措辞**零改动** (AC-4, 负向防误伤)。
- [x] **G-2** `aria/hooks/secret-guard.sh` (PreToolUse, part①) **零改动** + 回归**非降** (vs 当前 baseline, 不硬编 260)(AC-6)。

## Phase C 提醒
- **两协调 PR**: aria (TASK-001/002/003/006) + standards (TASK-004/005) ; 主仓 gitlink bump ×2 + **post-merge-master-SHA capture** (`[[feedback_submodule_pointer_post_merge_bump]]`; C.2.4.5 block gate + C.2.5 兜底) ; 双远程 parity。
- 顺带 hygiene (非本 change scope, Phase C 一并): close stale aria-plugin PR #70 + reconcile 遗留 untracked handoff doc。

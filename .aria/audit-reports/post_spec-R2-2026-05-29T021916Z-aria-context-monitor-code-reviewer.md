---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-05-29T02:19:16.000Z
context: openspec/changes/aria-context-monitor/proposal.md
agents: [code-reviewer]
---

# post_spec R2 — code-reviewer — aria-context-monitor (stability/verification)

审计视角: code-reviewer。R2 任务 = 验证 R1 三个 MAJOR (S1/S2/S3) 在 Rev1 是否 CLOSED, 并扫描 Rev1 引入的 NEW internal-consistency issue (新增 `used_percentage` + `used_percentage_proxy` 双字段 nullable-by-source 的 schema/Success Criteria 互恰性 + relay marker 块 / atomic-write snippet shell 技术正确性)。已对照真实 `~/.claude/statusline-command.sh` + 实跑 atomic-write snippet 验证。

## 审计结论

### R1 finding 闭合表

| ID | R1 严重度 | Rev1 状态 | 证据 |
|----|-----------|-----------|------|
| **S1** schema 证据不可复现 | major | **CLOSED** | (1) Task 1.1 (L155) 现标 **`[BLOCKING pre-Phase-B gate]`**, 显式列 5 个未佐证字段 (`context_window_size`/`model.id[1m]`/`transcript_path`/`remaining_percentage`/`exceeds_200k_tokens`) 必须重新 capture 验证; (2) **失败回退条款** literal 写入 Task 1.1 ("若 `context_window_size` 缺失 → 触发回退条款 (fallback 链升主路径), 回 A.2 修 Spec"); (3) §核心机制 L66 新增 **⚠️ 证据状态 caveat** block, 明确区分"生产脚本已佐证"6 字段 vs "仅单次已删 spike capture, 无独立可复现证据"5 字段, 并复述 BLOCKING gate + fallback。R1 修复要求三项 (BLOCKING gate / fallback clause / evidence caveat) **全部落实, 措辞与 R1 建议一致**。 |
| **S2** used_percentage 双路径语义混用 | major | **CLOSED** | schema (L122-123) 现拆为两独立字段: `used_percentage` (注释 "仅 relay_cache: runtime 口径 (total_input/window). transcript 路径为 null") + `used_percentage_proxy` (注释 "仅 transcript_fallback: (input+cache_read+cache_creation)/window. relay 路径为 null")。L135 caveat block 显式声明 "两者是不同的量, 不共用字段, 消费方按 `source` 读对应字段"。与 R1 S2 修复建议 (区分语义 + 不混用) 一致, 且采用比 R1 建议 (`usage_basis` 注释字段) 更彻底的"双字段分离"方案。 |
| **S3** window_source enum mismatch | major | **CLOSED** | (1) enum 现 5 值 (L126): `runtime / cached_size_reuse / config / empirical_peak / default`, 含 R1 要求的新档 `cached_size_reuse`; (2) §window_source 解析链 (L95-105) 显式映射 DEC 4-tier: relay_cache→恒 `runtime` (**约束: 不得标其他值**), transcript fallback 4 档 (cached_size_reuse>config>empirical_peak>default); (3) relay_cache→always-runtime 约束 literal 化 (L98)。R1 S3 三项修复 (补 cached_size_reuse / 映射 4-tier / relay_cache→runtime 约束) 全部落实。 |
| S4 cache 缺 schema_version | minor | **CLOSED (incidental)** | atomic-write snippet (L83) + output schema (L121) + Task 1.2 (L156) 均含 `schema_version:"1.0"` + 校验。 |
| S5 cache schema 未独立定义 | minor | PARTIAL | Rev1 未补独立 "Cache 文件 schema" 小节, 但 atomic-write snippet (L83) 现给出 cache 生产字段的 inline 形式 + schema_version, 降低歧义。残留为 minor, 不阻塞。 |
| S6 relay 注入锚点欠精确 | minor | **CLOSED** | §Relay 注入语义 (L76-83): 复用 `$input` 不可再 cat + 注入位置必须在 `input=$(cat)` 之后 + marker 锚点 (`# >>> aria-context-monitor relay >>>` / `<<<`) 供幂等检测。R1 S6 三项 (锚点位置 / sentinel marker / 复用 $input) 全部落实。 |

### NEW finding 扫描 (Rev1 引入)

#### [verified-OK] N1: 双字段 nullable-by-source 的 schema ↔ Success Criteria 互恰性 — 一致 ✅

逐路径验证 schema (L118-132) 与 Success Criteria (L169-171) 的 null 契约:
- **relay_cache 路径**: schema 注释 `used_percentage`=runtime 值 / `used_percentage_proxy`=null。SC L169 ("source=relay_cache + used_percentage 与状态栏 0 偏差") 一致, 未要求 proxy 非 null。✅
- **transcript_fallback 路径**: schema 注释 `used_percentage`=null / `used_percentage_proxy`=非 null。SC L170 literal: "`used_percentage_proxy` 非 null (used_percentage = null)" — **与 schema 注释逐字互恰**。✅
- **unavailable 路径**: source 枚举含 `unavailable` (L119), SC L172 (corrupt→unavailable 不抛异常) 覆盖。两 percentage 字段在此路径均 null (隐含, 无显式声明但语义自洽)。✅

结论: 双字段 nullable-by-source 在 schema 与 Success Criteria 间**互斥-填充契约一致**, 无矛盾。R1 S2 的修复未引入新的 schema/SC 不一致。

#### [verified-OK] N2: relay marker 块 + atomic-write snippet shell 技术正确性 — 正确 ✅

实证验证 (对照真实 `~/.claude/statusline-command.sh` + 实跑 snippet):
- **marker 锚点设计可行**: 真实脚本 L2 = `input=$(cat)`, 末尾 = `printf '%b' "$parts"` (实测确认)。Rev1 约束"注入在 `input=$(cat)` 之后"技术成立 — stdin 已被 L2 cat 耗尽, marker 块复用 `$input` 不再 cat, 符合 R1 S6 锚点要求。marker 包裹注释 (`# >>> ... >>>` / `# <<< ... <<<`) 是标准幂等-检测 pattern (grep marker 判已注入), 可行。
- **atomic-write snippet shell 正确**: 实跑 `echo "$input" | jq -c '{schema_version:"1.0", ...}' > "$tmp" && mv "$tmp" "$cache"` — EXIT=0, cache 产出合法 compact JSON (含 `model_id:"claude-opus-4-8[1m]"` 含 `[1m]` 后缀正确保留), tmp 被 mv 消除。`&&` 短路保证 jq 失败时不 mv (不产生半写 cache), `jq -c` compact 输出正确, tmp→rename 在同目录 (`.aria/cache/`) 下是 POSIX 原子 rename, 满足"避免 truncate→write 间并发读 corrupt"目标。✅

  > **观察 (非 finding, advisory)**: atomic rename 仅在 `$tmp` 与 `$cache` **同 filesystem** 时原子。Spec 未显式约束 tmp 路径必须与 cache 同目录 (`.aria/cache/`)。若实施者把 tmp 放 `/tmp` (跨 mount) 则 `mv` 退化为 copy+unlink 非原子。建议 Task 1.3 实施时 tmp 用 `"${cache}.tmp.$$"` 同目录形式。此为实施细节, 不构成 spec-level finding (snippet 示例本身用相对裸名 `$tmp`, 默认 cwd, 通常同 dir)。

结论: relay marker 块设计与 atomic-write snippet **shell 技术正确, 与真实 statusline 脚本结构兼容**, Rev1 的 M-atomic-write + M-relay-stdin 修复未引入技术错误。

#### [verified-OK] N3: Task / Success Criteria / schema 三向交叉一致性 — 一致 ✅

- window_source 5 值: schema L126 = enum 定义, Task 1.6 L160 = "window_source enum 5 值", §解析链 L95-105 = 映射, SC L175 = "relay_cache 命中恒=runtime; transcript 按 4 档" — 三处一致。✅
- staleness 300s: §Staleness L72 / Task 1.6 L160 / Task 1.4 L158 / SC L171 / Backward-compat 全一致。✅
- corrupt cache: atomic-write 动机 (L83) / token_telemetry JSONDecodeError 防御 (L109, Task 1.2 L156) / Task 1.7 corrupt-cache 场景 (L161) / SC L172 — 闭环一致。✅

## Verdict

**PASS**

| 严重度 | NEW (Rev1 引入) | carried (R1 未闭) |
|--------|-----------------|-------------------|
| critical | 0 | 0 |
| major | 0 | 0 (S1/S2/S3 全 CLOSED) |
| minor | 0 | 1 (S5 PARTIAL — cache schema 未独立小节, 但 inline snippet 已降歧义, 不阻塞) |

**判定依据**: PASS = 0 new critical + 0 new major + R1 majors 全 CLOSED。R1 三个 MAJOR (S1 schema 证据 / S2 used% 双口径 / S3 window_source enum) 经 Rev1 changelog 映射 + 逐字交叉验证, **全部 CLOSED 且修复措辞与 R1 建议一致或更彻底**。NEW 扫描 (双字段 nullable schema↔SC 互恰 N1 / relay marker + atomic-write shell N2 / 三向交叉 N3) **全部 verified-OK, 零 new finding**。仅 1 残留 minor (S5 PARTIAL, 已被 inline snippet 部分缓解), 不构成 PASS_WITH_WARNINGS 触发条件 (该 minor 非 Rev1 新引入, 且不阻塞实施)。

**Implementation-readiness**: schema 精确度从 R1 的"欠成熟"提升到"ship-ready"。架构基石 (model→window 不可靠 + statusLine 富 stdin) 在 R1 已实证属实; Rev1 把最大 verifiability gap (S1) 用 BLOCKING gate + fallback 条款制度化 (即使 1.1 capture 失败也有确定性降级路径), schema 内部一致性 (S2/S3) 闭合, atomic-write 实证可跑。code-reviewer 立场: **可进 Phase B**。

## 轮次记录

- **R1 (code-reviewer)**: 6 findings (3 major S1/S2/S3 + 3 minor S4/S5/S6) + 1 正面 (S7)。Verdict PASS_WITH_WARNINGS。核心实证属实, 风险集中 schema 一致性 + 单点 capture 证据不可复现。
- **R2 (code-reviewer, stability/verification)**: R1 三 major **全 CLOSED** (逐字交叉验证 + 措辞对齐); S4/S6 incidental CLOSED, S5 PARTIAL (非阻塞)。NEW 扫描 3 项 (N1 schema↔SC 互恰 / N2 marker+atomic-write shell 实证 / N3 三向交叉) **全 OK, 0 new finding**。对照真实 statusline 脚本确认 marker 锚点可行 + 实跑 atomic-write snippet 确认 shell 正确 (含 `[1m]` 保留)。Verdict **PASS**。无 oscillation (R2 未推翻 R1 任何结论, 仅验证闭合)。建议 converged 由 orchestrator 综合多 agent 判定 (本 agent R2 = PASS, 已收敛到 0 new major; converged=null 待汇总)。

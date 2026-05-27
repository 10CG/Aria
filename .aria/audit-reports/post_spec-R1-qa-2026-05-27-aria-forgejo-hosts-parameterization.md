---
audit_id: post_spec-R1-qa-2026-05-27-aria-forgejo-hosts-parameterization
checkpoint: post_spec
round: R1
agent: qa-engineer
spec_id: aria-forgejo-hosts-parameterization
spec_level: L2
verdict: REVISE
verdict_reason: "AC §6 测试覆盖定义不完整(缺 reverse/edge case);forgejo_config.py 与 issue_scan.py 的 env 路径协调机制在 Spec 中存在歧义;dogfood smoke 未包含 env override path 验证。"
issues:
  critical: 0
  major: 3
  minor: 3
timestamp: 2026-05-27T12:00:00Z
---

# QA-Engineer Audit Report — R1

**Spec**: `aria-forgejo-hosts-parameterization`
**文件**: `/home/dev/Aria/openspec/changes/aria-forgejo-hosts-parameterization/proposal.md`
**审计人**: qa-engineer
**Round**: R1 (L2 baseline = 2-round)

---

## 实际代码现状核查

审计前先对三处 hardcode 的当前状态做了实地核查:

- **C1** (`forgejo_config.py` L35): `_KNOWN_FORGEJO_HOSTS: tuple[str, ...] = ("forgejo.10cg.pub",)` — 确认存在,无 env 逻辑,无 config-loader 集成。`import` 列表中无 `os`,无 `json`。
- **C2** (`issue_scan.py` L71): `DEFAULT_CONFIG["platform_hostnames"]["forgejo"] = ["forgejo.10cg.pub"]` — 确认存在。`_load_config()` 已有 `platform_hostnames` merge 逻辑(L118-122),但 **只处理 config.json 覆盖,没有 env override**。
- **C3** (`DEFAULTS.json` L45): `"forgejo": ["forgejo.10cg.pub"]` — 确认存在,无 env 说明。
- **`.aria/config.json`**: Aria 项目自身已显式 set `platform_hostnames.forgejo: ["forgejo.10cg.pub"]`(L27-29) — R3 风险 Spec 已认知,但 dogfood 覆盖度分析见 Major-2。
- **现有测试**: `test_forgejo_config.py` 已有 `TestHostDetection` / `TestCollectorStates` / `TestRegexHardening`,**但全部 hardcode `forgejo.10cg.pub`,没有任何 env override 或 config override 路径测试**。

---

## Critical Findings

无 Critical 问题。

---

## Major Findings

### Major-1: AC §6 "3 个 unit test" 覆盖规格不完整 — 缺少关键 edge case

**位置**: `proposal.md §Acceptance Criteria #6` + `§Testing Strategy - Unit tests`

**问题**:

AC §6 说"3 个 unit test 覆盖 env / config / default 三条 precedence path",Testing Strategy 补充了 `test_env_override` / `test_config_override` / `test_default_fallback` / `test_env_beats_config` 四个用例。但以下场景在 Spec 中完全未提及,Phase B 实施时极易遗漏:

1. **`ARIA_FORGEJO_HOSTS=""` (空字符串 env)**: Spec §A 的实现代码写了 `env.strip()` 然后 `if env:` 判空,但 AC 和 Testing 都没有对应的 test case 说明空 env 应 fall through 到 config。这是 env precedence 最常见的 off-by-one bug — 用户写 `export ARIA_FORGEJO_HOSTS=""` 期望清空 override 但实际行为不明确。
2. **config 含 `[]` 空 list**: Spec §A 写了 `if config_hosts: return tuple(config_hosts)`,但没有说明 `config_hosts = []` 时是否 fall through 到 DEFAULTS.json。空 list 是有效 JSON,语义上"用户显式清空 forgejo hosts"还是"等价于未配置"?Spec 没有定义,AC 没有测试。
3. **config 含 duplicate hosts**: `["forge.example.com", "forge.example.com"]` — 重复项是否 deduplicate?`_detect_forgejo_host()` 用 `for host in _KNOWN_FORGEJO_HOSTS` 遍历,重复项不会 crash 但会做冗余检测,AC 无说明。
4. **AC §1 的 `forgejo_config` 验证范围模糊**: AC §1 写"snapshot 的 `forgejo_config` collector 识别 `h1` 和 `h2`"。但当前 `forgejo_config.py` 的 `_detect_forgejo_host()` 是用 `host in remote_url` 做 substring 匹配,`_KNOWN_FORGEJO_HOSTS` 是 **module-level 常量**,在 `import` 时已确定。若 env var 在 import 后再 set,`_KNOWN_FORGEJO_HOSTS` 不会重新计算。这个 **import-time binding 的并发/测试隔离风险** Spec 未提及,monkeypatching in test 是必要的但没有规定。

**影响**: Phase B 实施时遗漏空 string / 空 list 边界处理极易引入 regression,而 AC 通过也无法发现。

**建议**: 在 AC §6 和 Testing Strategy 中补充至少 2 个 edge case test:
- `test_env_empty_string_falls_through` — `ARIA_FORGEJO_HOSTS=""` → 走 config/default 路径
- `test_config_empty_list_behavior` — 明确定义空 list 语义并写 test

---

### Major-2: Dogfood 覆盖度不足 — 仅 default fallback path,缺 env override smoke

**位置**: `proposal.md §Testing Strategy - Dogfood evidence`

**问题**:

Spec 中 dogfood evidence 定义为"本 PR 自身 — Aria 项目跑 scan.py 验 forgejo_config collector 仍输出 `forgejo.10cg.pub`(default fallback 路径)"。

这只覆盖了 **default path**,且 Aria 自身 `.aria/config.json` 已显式设置 `platform_hostnames.forgejo: ["forgejo.10cg.pub"]`,所以实际上走的是 **config path 而非 default path**。换言之,当前 dogfood 定义验证的是:

- config path: `forgejo.10cg.pub` (因为 Aria `.aria/config.json` 已有显式 forgejo 配置)

但 **完全没有验证 env override path**。Manual smoke test 里有 Case 1 写了 env override 验证,但它被归类为 "manual smoke",不是 dogfood 证据。`feedback_deterministic_structural_skill_rule6_substitute` 明确要求 dogfood 作为三件套之一。

**实际情况**: Aria 自身 `.aria/config.json` L27-29 已经有 `"forgejo": ["forgejo.10cg.pub"]`,所以 C3 Deliverable 中说"Aria 自身 .aria/config.json 加显式 `platform_hostnames.forgejo` 段 作为 dogfood example"其实已存在,Phase B 不需要新增,但 Spec 描述行为好像需要新增。这是一个 **Spec 与实际现状不匹配** 的描述错误。

**建议**:
1. Phase B 补充将 **env override smoke** (`ARIA_FORGEJO_HOSTS=alt.example.com python3 scan.py` + `jq .forgejo_config`) 作为 **dogfood 正式验证步骤**,记录结果到 PR description。
2. 修正 C/R3 Deliverable 描述:Aria `.aria/config.json` 的 `platform_hostnames.forgejo` 段已存在,Phase B 任务应是"verify 已有配置充当 dogfood example",而非新增。

---

### Major-3: C1/C2 env override 协调机制在 Spec 中有歧义 — 两处实现可能不同步

**位置**: `proposal.md §B - issue_scan.py (C2)` vs `§A - forgejo_config.py (C1)`

**问题**:

Spec §A 明确给出了完整的 `_load_known_forgejo_hosts()` 函数实现,包含 4 层 precedence(env → config → DEFAULTS.json → module fallback)。

Spec §B 对 `issue_scan.py` 的改法却是:

> "删除 `DEFAULT_CONFIG.platform_hostnames` 中的 hardcode list / 在 config-loader merge 后(运行时):若 user 未提供 → 用 C3 DEFAULTS.json + env override 链"

**关键问题**:

1. `issue_scan.py` 的 `_load_config()` 已有 config.json 的 `platform_hostnames` merge 逻辑(L118-122),这个逻辑走的是 **config.json 覆盖 DEFAULT_CONFIG 键值**,不是 env-first 的 3 层 precedence。Spec §B 的"用 C3 DEFAULTS.json + env override 链"与 §A 的 `_load_known_forgejo_hosts()` 是两种不同的实现模式,但 Spec 没有说清楚 C2 是否也要实现 `_load_known_forgejo_hosts()` 风格还是直接依赖 C1 的函数。
2. `issue_scan.py` 的 `DEFAULT_CONFIG` 在 module load 时已 materialized,后续 `_load_config()` 做 shallow merge。若 `ARIA_FORGEJO_HOSTS` env 只在 C1 `forgejo_config.py` 处理,`issue_scan.py` 的 platform detection 可能仍走旧 config 路径,导致 **AC §4"三处一致行为"无法满足**。
3. Spec §B 写"或直接消费 config-loader DEFAULTS.json + env override 链",但 config-loader 是纯 AI Skill(SKILL.md: `disable-model-invocation: true, allowed-tools: Read, Glob`),没有 Python runtime API 可调用。`_config_loader_forgejo_hosts()` 在 §A 注释里说"通过 config-loader skill API",但 config-loader 没有 Python callable API,实际上应该是直接 `json.load` `.aria/config.json`。这个实现细节含糊,可能误导 Phase B 实施者。

**建议**: Spec 需明确 C2 的 env override 机制:
- 选项 A: C2 引用 C1 的 `_load_known_forgejo_hosts()` 作为共享 helper
- 选项 B: C2 在 `_load_config()` 之后,对 `forgejo` key 单独做 env check
- 明确说明 `_config_loader_forgejo_hosts()` 的实现方式是直接 `json.load`,而非调用任何 Skill runtime

---

## Minor Findings

### Minor-1: AC §1 smoke 命令路径有误

**位置**: `proposal.md §Testing Strategy - Manual smoke test`

**问题**: 

```bash
ARIA_FORGEJO_HOSTS="alt.example.com" python3 aria/skills/state-scanner/scripts/scan.py --output /tmp/snap1.json
```

实际 scan.py 入口路径为 `aria/skills/state-scanner/scripts/scan.py`,但 `--output` 参数需确认是否为 scan.py 的合法 CLI flag。当前 scan.py 实际使用方式(基于 state-scanner SKILL.md)通常是直接运行不带 `--output`,snapshot 写入固定路径 `.aria/state-snapshot.json`。若 `--output` 是计划中新增的 flag 而非现有 flag,Spec 应说明。

**建议**: 验证 `--output` flag 的存在性或改为实际 CLI 用法:
```bash
ARIA_FORGEJO_HOSTS="alt.example.com" python3 aria/skills/state-scanner/scripts/scan.py
jq .forgejo_config .aria/state-snapshot.json
```

---

### Minor-2: R4 defer 触发条件为 owner manual,未定义判断流程

**位置**: `proposal.md §Risks R4` + `§Rollout Plan - Cross-coordination 风险`

**问题**:

"2026-06-06 未 ship → 主动 defer 到 v1.30.x patch" 描述了触发条件,但没有定义:

1. 谁负责在 D+13 评估 ship 状态?是 owner 手动检查,还是 state-scanner 能检测?
2. defer 后 v1.30.0 slot 被 block-flip 之后的版本占用,v1.30.x patch 的实际 version 是什么?v1.29.1 还是 v1.30.0 (v1.29.0 之后的下一个 minor)?

这是一个 L2 Spec 可接受的轻量化描述,但对于版本协调来说需要多一点确定性。

**建议**: 在 R4 中补充一行说明 defer 时的版本号策略: "defer 时 version target 改为 v1.29.1 (patch after block-flip v1.29.0)"。

---

### Minor-3: Structural fixture README 缺少失败行为规格

**位置**: `proposal.md §Testing Strategy - Structural fixture README`

**问题**:

fixture README 计划包含"3 precedence path 说明 + expected behavior 表",但 `feedback_deterministic_structural_skill_rule6_substitute` 规范要求 structural fixture 覆盖 **fail-soft 行为**。具体地:

- config-loader (json.load) 失败时 → 应 fallback 到 module constant
- env 含非法字符(空格、斜杠等)时 → `h.strip()` 能处理空格,但含 `:8080` 端口号的 `forge.example.com:8080` 是否合法?

这些 fail-soft 路径在 Spec §A 实现代码中有一定覆盖(`if h.strip()`),但 fixture README 规格没有说明需要文档化 fail-soft behavior。

**建议**: 在 Testing Strategy 中补充"Structural fixture README 需包含 fail-soft 行为表(config read error → fallback / env 含端口号处理)"。

---

## Verdict Summary

**verdict: REVISE**

三个 Major 问题需要在 Spec 中修订:

1. **Major-1**: AC §6 缺少 empty string env / empty list config / duplicate host 边界 case — 直接影响 Phase B 实施质量和 AC 可验证性。
2. **Major-2**: Dogfood 只覆盖 config/default path,缺 env override 实际验证;Spec 描述与 `.aria/config.json` 现状不一致。
3. **Major-3**: C1/C2 env override 协调机制描述不清 — C2 的 env handling 是 delegating to C1 helper 还是独立实现?`_config_loader_forgejo_hosts()` 的 "config-loader skill API" 表述具有误导性。

三个 Minor 问题不阻塞 Approved,但建议同步修正:

- Minor-1: smoke 命令 `--output` flag 需确认存在
- Minor-2: R4 defer 版本号策略不明确
- Minor-3: fixture README 规格缺 fail-soft 行为说明

**Good practices 认可**:
- §Backward compatibility guarantee 有明确保证,三条规则覆盖全面
- §Rollout Plan 明确列出 C.2.4 / C.2.4.5 / C.2.5 gate 序列,符合 Rule #8 要求
- Out of Scope 边界划定清晰,C5/C6 defer 合理
- D.1 5+1 SOT 清单完整,跳 v1.29.0 占位的理由合理

**建议 Spec 作者**处理 Major-1~3 后进入 R2 审计。

# aria-forgejo-hosts-parameterization — 通用层 Forgejo host hardcode 参数化(4 处)

> **Level**: 2 (Minimal — proposal.md only, mechanism 简单 + scope 小)
> **Status**: ✅ **Approved** — Phase A.2 CONVERGED 2026-05-27 via R1 REVISE × 3 → Rev1 → R2 PASS_WITH_WARNINGS × 3 unanimous, 0 new Critical/Major + Rev1.1 polish for substance-converged W-1 env-ordering fix per [[feedback_audit_convergence_patterns]] L2 baseline
> **Rev1 changelog**:
>   - C-API fix: 删除"config-loader skill API"误述(实际是 documentation-only LLM Skill 无 Python 接口),改为直接 inline JSON 读 + 抽到 `collectors/_common.py` 作 legit shared helper
>   - C-paper-promise fix: §A `_load_known_forgejo_hosts()` 拆 2 tier (module-level env-only + collector-time config) + 加 cross-collector parity test
>   - M-4th-hardcode: scope 扩到第 4 处 hardcode (`issue_scan.py:L198` `_detect_platform` URL substring heuristic), 决议 = 删 L198 forgejo-specific fallback (DEFAULTS.json platform_hostnames 已承担)
>   - M-changelog: CHANGELOG ship 时先放 v1.29.0 placeholder line, 避免 block-flip ship 时手动定位插入点
>   - M-D2-arg: 加 §DEC D2 compliance discussion (legacy fallback 不违 D2)
>   - M-AC-edges: AC + Tests 加 empty env / empty list / duplicate hosts / monkeypatch isolation edges
>   - M-dogfood: env override path 加 formal dogfood smoke (不只 default fallback)
>   - M-AB-consistency: §B 措辞改为 "在 `_load_config()` 前加 env override layer" (非 "删 DEFAULT_CONFIG hardcode")
>   - Phase B.0 Agent assignment 段添加
>
> **Change ID**: `aria-forgejo-hosts-parameterization`
> **Source**: Boundary audit `2026-05-27` P0 items C1+C2+C3 (`.aria/notes/2026-05-27-boundary-audit-10cg-hardcode.md`)
> **Parent strategic memo**: `.aria/notes/2026-05-27-aria-fleet-three-layer-architecture.md` §4 边界切割规则
> **Target version**: aria-plugin **v1.30.0** (v1.29.0 = block-flip reserved 2026-06-07)
> **Ship target**: 单 cycle (~2-3h end-to-end per 2026-05-27 handoff §6 estimate)
> **Risk class**: Backward-compatible (默认值未变;`forgejo.10cg.pub` 仍是 fallback;无 API break)

---

## Why

### Direct trigger

2026-05-27 boundary audit(aria-fleet 战略 sign-off 同 session)发现通用层 `aria/` 三处 hardcode 了 `forgejo.10cg.pub`,使 aria-plugin 无法被其他 org 使用 forge 实例(GitHub Enterprise / Gitea / 自建 Forgejo)直接安装。这违反 aria-fleet DEC D2 硬约束"通用层禁止新增 10CG-specific hardcode"(per `feedback_three_layer_universal_workspace_instance`)。

### Why now(Sprint 1 P0 第一项)

Per 2026-05-27 handoff §6 carry-forward 优先级 #2:
- **不阻塞 M6**(aria-fleet 整体 deferred 到 M7+,但 P0 hygiene 可单独 cycle 处理)
- **通用化收益高**(3 处 hardcode 是 aria-plugin 公开发布的最大障碍)
- **~2-3h hygiene cycle** 估时,Level 2 单 cycle 跑得完
- **D+14 v1.29.0 ship(2026-06-07)前**完成,避免与 block-flip ship 撞 slot

### 四处 hardcode 当前现状(audit + R1 ba M-1 复核 2026-05-27)

| ID | 文件 | 行号 | 当前值 |
|----|------|------|--------|
| C1 | `aria/skills/state-scanner/scripts/collectors/forgejo_config.py` | L35 | `_KNOWN_FORGEJO_HOSTS: tuple[str, ...] = ("forgejo.10cg.pub",)` |
| C2 | `aria/skills/state-scanner/scripts/collectors/issue_scan.py` | L71 | `DEFAULT_CONFIG["platform_hostnames"]["forgejo"] = ["forgejo.10cg.pub"]` |
| C3 | `aria/skills/config-loader/DEFAULTS.json` | L45 | `"forgejo": ["forgejo.10cg.pub"]` |
| **C4** (Rev1 new) | `aria/skills/state-scanner/scripts/collectors/issue_scan.py` | L198 | `if "forgejo.10cg.pub" in low: return "forgejo"` (`_detect_platform()` Level 3 URL substring heuristic) |

四处之间无单一 source-of-truth:C1 是 collector-internal 常量, C2 是 internal fallback, C3 是 config-loader default, C4 是 `_detect_platform()` Level 3 fallback heuristic → 任一外部 fork 都要改 4 处, 且 C4 是 audit R1 ba 在 Phase A.2 验证现状时**独立 surface** 的 audit memo 漏抓项(audit memo 仅扫到 L71)。

### Why NOT bigger scope

Sprint 1 范围**仅** C1+C2+C3(Forgejo hosts)。明确 **defer 到 Sprint 2+**:
- **C5+C6** CI backend 抽象(`pre_merge_gate.py` Aether-only 假设)— 8-12h, 需另起 Level 3 Spec
- **C7** standards `integrate-standards.sh` SSH URL — P2, 跨 standards submodule
- **C8** aria-orchestrator `inject-demo-issues.py` PATH + TARGET_REPO — 跨独立 submodule
- 通知后端(Feishu)抽象 — P3 Sprint 3

---

## What

本 Spec ships **5 项 deliverables**(A-E,Rev1 加 E covering C4)。**关键架构决策**(R1 fix):
- **NO** "config-loader Python API" 假设 — config-loader 是 documentation-only LLM Skill(`disable-model-invocation: true`,仅 SKILL.md + DEFAULTS.json + config-example.md,无任何 .py 文件)
- **YES** Inline JSON read,模仿 `issue_scan.py::_load_config()` (L90-123) 现有 pattern
- **YES** `collectors/_common.py` 作 cross-collector legit shared helper 位置(`forgejo_config.py` 已 import `_common`,边界合法)
- **YES** 2-tier precedence: module-level 仅做 env 解析, config.json 读取推迟到 collector function (拿到 project_root 后)

### A. Two-tier env-aware Forgejo hosts in `forgejo_config.py`(C1)+ `_common.py` shared helper

**File 1**: `aria/skills/state-scanner/scripts/collectors/_common.py` (新增 shared helper)

```python
# Add at module level (preserve existing imports + add json + os)
import json
import os
# ... existing imports ...

ARIA_FORGEJO_HOSTS_ENV = "ARIA_FORGEJO_HOSTS"
_LEGACY_FORGEJO_FALLBACK: tuple[str, ...] = ("forgejo.10cg.pub",)


def _parse_env_forgejo_hosts() -> tuple[str, ...] | None:
    """Parse ARIA_FORGEJO_HOSTS env var (comma-separated).

    Returns None when env var is unset, empty, or all-whitespace
    (callers fall through to config / defaults).
    """
    raw = os.environ.get(ARIA_FORGEJO_HOSTS_ENV, "")
    if not raw.strip():
        return None
    hosts = tuple(h.strip() for h in raw.split(",") if h.strip())
    return hosts or None


def _read_config_forgejo_hosts(project_root: Path) -> tuple[str, ...] | None:
    """Read `.aria/config.json` → `state_scanner.issue_scan.platform_hostnames.forgejo`.

    Fail-soft: missing file / parse error / key absent / non-list value → None.
    Empty list `[]` → None (fall through to defaults; explicit empty = same as unset
    per Rev1 qa M1 decision — avoid silently disabling all forgejo detection).
    Duplicates preserved (callers decide whether to dedup).
    """
    cfg_path = project_root / ".aria" / "config.json"
    if not cfg_path.is_file():
        return None
    try:
        with cfg_path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
    except (OSError, json.JSONDecodeError):
        return None
    hosts = (
        ((raw.get("state_scanner") or {}).get("issue_scan") or {})
        .get("platform_hostnames", {}).get("forgejo")
    )
    if not isinstance(hosts, list) or not hosts:
        return None
    cleaned = tuple(h for h in hosts if isinstance(h, str) and h.strip())
    return cleaned or None


def resolve_forgejo_hosts(project_root: Path) -> tuple[str, ...]:
    """Canonical 3-layer precedence resolver — used by ALL forgejo-aware collectors.

    Precedence (highest first):
      1. ARIA_FORGEJO_HOSTS env (comma-separated)
      2. .aria/config.json → state_scanner.issue_scan.platform_hostnames.forgejo
      3. Legacy fallback: ("forgejo.10cg.pub",)

    Returns tuple (immutable; never empty — fallback guaranteed).
    """
    env_hosts = _parse_env_forgejo_hosts()
    if env_hosts:
        return env_hosts
    config_hosts = _read_config_forgejo_hosts(project_root)
    if config_hosts:
        return config_hosts
    return _LEGACY_FORGEJO_FALLBACK
```

**File 2**: `aria/skills/state-scanner/scripts/collectors/forgejo_config.py`

```python
# Replace L34-35:
from ._common import resolve_forgejo_hosts   # add to existing imports

# Remove module-level _KNOWN_FORGEJO_HOSTS constant.
# _detect_forgejo_host signature changes: pass hosts as param instead of reading global.

def _detect_forgejo_host(remote_url: str, known_hosts: tuple[str, ...]) -> str | None:
    """Return matched Forgejo hostname; otherwise None. Hosts now param-injected."""
    # ... existing match logic, use known_hosts instead of _KNOWN_FORGEJO_HOSTS ...

def collect_forgejo_config(project_root: Path) -> CollectorResult:
    # ... existing logic ...
    known_hosts = resolve_forgejo_hosts(project_root)  # NEW: resolve per-call
    matched = _detect_forgejo_host(remote_url, known_hosts)
    # ... rest unchanged ...
```

**Why 2-tier(module-level env + collector-time config)** [Rev1 fix R1 ba M-2]:
- Module常量在 `import` 时求值, 此时 `project_root` 未确定 → 读 config.json 不可行
- Env var 在 import 时已可用, 但测试 isolation 风险高 (monkeypatch difficulty)
- **Rev1 决策**: 完全删除 module-level 常量 → 所有 hosts 解析推迟到 `collect_forgejo_config(project_root)` 内, 由 `resolve_forgejo_hosts(project_root)` 统一处理
- 这同时解决 qa M1 #4 提到的 import-time binding 风险 (test 用 monkeypatch env var 不再受 import-order 影响)

### B. `issue_scan.py` env override layer in `_load_config()`(C2)

**File**: `aria/skills/state-scanner/scripts/collectors/issue_scan.py`
**Lines**: L66-78 (`DEFAULT_CONFIG`) + L90-123 (`_load_config()`)

**Rev1 fix R1 qa M3 + ba N2**: 改写措辞 — **不**删 `DEFAULT_CONFIG["platform_hostnames"]["forgejo"]` 的 list, 改为**在 `_load_config()` 现有 config.json merge 之后追加 env override final layer**(Rev1.1 fix R2 ba W-1 + qa R2 new minor:env 必须 post-merge override,否则现有 L118-122 unconditional merge 会用 config.json 值覆盖 env):

```python
def _load_config(project_root: Path) -> dict[str, Any]:
    # ... existing setup of merged dict + DEFAULT_CONFIG copy ...
    # ... existing config.json read + L118-122 platform_hostnames merge unchanged ...

    # ---- Rev1.1 new: env override AS FINAL LAYER (after config.json merge) ----
    # Position matters: must be POST-merge so env wins over both config.json
    # AND DEFAULT_CONFIG. Pre-merge placement would let the existing merge loop
    # (L118-122) silently overwrite env value with config.json value.
    from ._common import _parse_env_forgejo_hosts
    env_hosts = _parse_env_forgejo_hosts()
    if env_hosts:
        merged["platform_hostnames"]["forgejo"] = list(env_hosts)
        # Other platform_hostnames keys (github, etc.) untouched.
    # ---- end Rev1.1 new ----

    return merged

    # ... existing config.json read + merge logic unchanged ...
    return merged
```

**保留** `DEFAULT_CONFIG["platform_hostnames"]["forgejo"] = ["forgejo.10cg.pub"]` 不动 — 作 Python-layer fallback(与 `_common._LEGACY_FORGEJO_FALLBACK` + DEFAULTS.json L45 三处对称),backward compat 不破。

`"github": ["github.com"]` 不变(github.com 是 GitHub 唯一公开 host;GitHub Enterprise URL 是另一个 capability,defer to future Spec)。

### **(NEW) E. Remove `_detect_platform()` Level 3 forgejo hardcode(C4)** [Rev1 add]

**File**: `aria/skills/state-scanner/scripts/collectors/issue_scan.py`
**Line**: L193-199 (`_detect_platform` Level 3 URL substring heuristic)

**当前**:
```python
# Level 3: URL substring heuristic (lower priority than explicit map)
low = remote_url.lower()
if "github.com" in low:
    return "github"
# Well-known forgejo domain fallback (matches SKILL.md example).
if "forgejo.10cg.pub" in low:
    return "forgejo"
```

**目标**: 删除 forgejo-specific Level 3 fallback — 让 Level 2 `platform_hostnames` map(经 `_load_config()` env+config+default 三层 resolve 后)承担 forgejo host 识别:

```python
# Level 3: URL substring heuristic (lower priority than explicit map)
# Only handles GitHub which has a single universal host (github.com).
# Forgejo hosts are intentionally NOT included here — they MUST come from
# Level 2 platform_hostnames map (env / .aria/config.json / DEFAULTS.json)
# so that custom Forgejo instances (forge.example.com etc.) work uniformly.
low = remote_url.lower()
if "github.com" in low:
    return "github"
```

**Why 安全**: DEFAULTS.json L45 仍 ship `"forgejo": ["forgejo.10cg.pub"]` 作 baseline → Aria self + 任何 install 无显式配置时,Level 2 map 仍命中 `forgejo.10cg.pub`。删 L198 Level 3 只是消除 **dual-codepath drift risk**(两条独立逻辑识同一 host),不丢 backward compat。

**Rev1 ba M-1 解决**: 若仅修 C2 不修 C4 → 用户自定义 host(如 `forge.example.com`)在某些 corner path 下仍走 L198 → return `None` (`ERR_PLATFORM_UNKNOWN`)→ issue scan 失效 → AC-2 在该 path 失效。删 L198 后,Level 2 platform_hostnames map 唯一权威,自定义 host 顺利识别。

### C. Documented precedence chain in `DEFAULTS.json` + DEC D2 compliance(C3)

**File**: `aria/skills/config-loader/DEFAULTS.json`
**Line**: L45 (`"forgejo": ["forgejo.10cg.pub"]`)

**当前**:hardcode list 无说明。

**目标**:保留 `["forgejo.10cg.pub"]` 作 DEFAULTS layer fallback,但通过**伴生 schema/docs**说明 precedence:
- DEFAULTS.json 仍是 baseline default(不删 `forgejo.10cg.pub` — backward compat)
- 在 `aria/skills/config-loader/SKILL.md` 加 §"Forgejo Hosts Configuration" 段, 文档化 3 层 precedence:
  ```
  1. ARIA_FORGEJO_HOSTS (env)
  2. .aria/config.json → state_scanner.issue_scan.platform_hostnames.forgejo
  3. DEFAULTS.json fallback (forgejo.10cg.pub legacy default)
  ```
- Aria 项目自身 `.aria/config.json` 显式 set `forgejo: ["forgejo.10cg.pub"]` → 显式 not relying on default(dogfood)

**Rev1 add — aria-fleet DEC D2 compliance discussion** [R1 tl M2]:

> **DEC D2 原文**: 通用层禁止新增 10CG-specific hardcode;abstraction 接口 + workspace config inject 具体值。
>
> **本 Spec 解读**: D2 禁止 **新增** hardcode。`forgejo.10cg.pub` 在 DEFAULTS.json L45 是 v1.28.0 ship 时**已存在**的 legacy hardcode,本 Spec **不在新代码引入** org-specific 字面量(env + config + workspace `.aria/config.json` 均无 hardcode)。
>
> Legacy fallback 保留的 backward compat 价值:任何现有 Aria install 不破(零行为变化), parametrization gated behind opt-in env/config override。
>
> **Deprecation roadmap**(M7+ aria-fleet 主线):未来 Spec 可在 DEFAULTS.json L45 上加 comment `// DEPRECATED in <future-version>: 改为 [] (require explicit config)` 并最终移除。本 Spec **不**强行做这个 deprecation(scope explicit defer), 因为:
> 1. 需 14d 观察期判 ecosystem 是否准备好(类比 v1.29.0 block-flip 模式)
> 2. M7+ aria-fleet 整体 ship 时通用化更彻底, legacy fallback removal 一起做更系统
> 3. 本 L2 Spec 是 hygiene patch, 不应携 architectural deprecation
>
> **Compliance verdict**: ✅ 不违 DEC D2。

### D. SKILL.md cross-ref + CHANGELOG entry

- `aria/skills/state-scanner/SKILL.md`:在 §"配置 (config-loader)" 表加注:`forgejo hosts` 可通过 `ARIA_FORGEJO_HOSTS` env 覆盖
- `aria/skills/state-scanner/references/issue-scanning.md`(若提及 forgejo hosts):同步加 env override 说明
- `aria/CHANGELOG.md`:**Rev1 fix R1 tl M1** — ship 时**先**在文件顶端插入 v1.29.0 placeholder line(`## [1.29.0] - 2026-06-07 (reserved for aria-submodule-gate-block-flip ship)`),**再**写 `## [1.30.0] - 2026-MM-DD` 真实条目在其下方。block-flip Spec ship 时只需替换 v1.29.0 placeholder 为真实 entry,**避免**手动定位插入点错误。条目内容注明 "Forgejo hosts now configurable via ARIA_FORGEJO_HOSTS env / .aria/config.json (closes boundary audit P0 C1+C2+C3+C4)"。

---

## Implementation Details

### Env var naming convention

Per aria-fleet DEC D2 + `feedback_three_layer_universal_workspace_instance`:
- 通用层 env vars 用 `ARIA_*` 前缀(不是 `ARIA_10CG_*`)
- 本 Spec 用 `ARIA_FORGEJO_HOSTS`(单数 host list, comma-separated)

### Precedence chain(canonical, 3 处实现必须一致)

```
环境变量 ARIA_FORGEJO_HOSTS=h1,h2,h3
       ↓ (if empty/unset)
.aria/config.json → state_scanner.issue_scan.platform_hostnames.forgejo: [...]
       ↓ (if absent/empty)
DEFAULTS.json → state_scanner.issue_scan.platform_hostnames.forgejo: ["forgejo.10cg.pub"]
       ↓ (if config-loader 不可用)
Module hardcode fallback: ("forgejo.10cg.pub",)
```

### Backward compatibility guarantee

- 任何 Aria 项目无显式配置 → 行为不变(仍只识别 `forgejo.10cg.pub`)
- 现有 `.aria/config.json` 含 `platform_hostnames.forgejo` 字段 → 行为不变(已 override default)
- 新增能力:任何项目可 `export ARIA_FORGEJO_HOSTS="forge.example.com"` 立即生效, 无需改 config 文件

---

## Acceptance Criteria

**Happy path**:
1. **Env precedence**:`ARIA_FORGEJO_HOSTS=h1,h2 python3 scripts/scan.py` → snapshot 的 `forgejo_config` collector 识别 `h1` 和 `h2`(而非 forgejo.10cg.pub);**且** `issue_scan` collector `_load_config()` 的 `platform_hostnames.forgejo` = `["h1", "h2"]`
2. **Config.json precedence**:无 env, 但 `.aria/config.json` 含 `state_scanner.issue_scan.platform_hostnames.forgejo: ["custom.example.com"]` → 识别 `custom.example.com`(forgejo_config + issue_scan 双 collector 一致)
3. **Default fallback**:无 env + 无 config → 仍识别 `forgejo.10cg.pub`(Aria 自身 + 现有 install 不破)
4. **Four places consistent**(Rev1: 加 C4):同一 env + config 输入 → C1/C2/C3/C4 四处一致行为 — `forgejo_config.py` host detection / `issue_scan.py` `_load_config()` platform_hostnames merge / `issue_scan.py` `_detect_platform()` Level 2 命中(L198 Level 3 删除后) / `DEFAULTS.json` doc 同步
5. **scan.py exit 0/10**:无 regression — 现有 Aria scan.py 跑通(`.aria/state-snapshot.json` 仍含正确 forgejo_config + issue_scan)

**Edge cases**(Rev1 add per R1 qa M1):
6. **Empty env fall-through**:`ARIA_FORGEJO_HOSTS=""` 或 `ARIA_FORGEJO_HOSTS="   "`(all-whitespace)→ 视为 unset,fall through 到 config / default(NOT 视为"用户清空 hosts")
7. **Empty config list fall-through**:`.aria/config.json` 含 `platform_hostnames.forgejo: []` → fall through 到 DEFAULTS.json fallback(NOT silently 禁用 forgejo detection — 避免 footgun)
8. **Duplicate hosts tolerated**:env 或 config 含 `["h1", "h1", "h2"]` → 保留 duplicate(callers 决定 dedup;`_detect_forgejo_host()` substring match 对 duplicate 是 idempotent)
9. **C4 deletion sanity**:删 `issue_scan.py:L198` 后, vanilla Aria install(无 env override + 默认 DEFAULTS.json)`_detect_platform("ssh://forgejo@forgejo.10cg.pub/...")` 仍 return `"forgejo"`(由 Level 2 platform_hostnames map 命中)
10. **Custom host AC**(Rev1 ba M-1 fix):`ARIA_FORGEJO_HOSTS=forge.example.com` + git remote `https://forge.example.com/owner/repo.git` → `_detect_platform()` return `"forgejo"`(此前因 L198 Level 3 hardcode 此 case 会 return None)
11. **Test coverage**:至少 **8 个** unit test 覆盖 — env / config / default / env-beats-config / empty-env / empty-config-list / duplicate-hosts / C4-custom-host-detection(per Rev1 expanded testing strategy)
12. **Test isolation**(Rev1 qa M1 #4):所有 env-related tests 使用 `monkeypatch.setenv` / `monkeypatch.delenv`,不依赖 import-time binding(本 Spec 删 module-level 常量后, 此风险 architecturally eliminated, 但 test 仍需断言 isolation)

---

## Testing Strategy

### Rule #6 substitute(per `feedback_deterministic_structural_skill_rule6_substitute`)

本 Spec 属 **deterministic structural** Skill 改动(collector 行为参数化,无 LLM behavior 变化)→ 不跑 `/skill-creator` LLM AB benchmark。代替 substitute:

| Substitute artifact | 位置 | 内容 |
|---------------------|------|------|
| Structural fixture README | `aria-plugin-benchmarks/forgejo-hosts-parameterization/README.md` | 3 precedence layer 说明 + 4 处 hardcode 删/改 map + 12 AC behavior 表 + edge case cheatsheet |
| Unit tests(forgejo_config) | `aria/skills/state-scanner/tests/test_forgejo_config.py` 扩展 | `test_env_override` + `test_config_override` + `test_default_fallback` + `test_env_beats_config` + `test_empty_env_falls_through` + `test_whitespace_env_falls_through` + `test_empty_config_list_falls_through` + `test_duplicate_hosts_tolerated` + `test_custom_host_detection_via_env`(C4 fix) |
| Unit tests(issue_scan) | `aria/skills/state-scanner/tests/test_issue_scan.py` 扩展 | `test_load_config_env_override` + `test_detect_platform_level2_via_env`(C4 fix) + `test_detect_platform_no_level3_forgejo_fallback`(L198 删除后行为) |
| Parity test(cross-collector) | `aria/skills/state-scanner/tests/test_forgejo_hosts_parity.py`(新建) | 同一 env+config 三组 fixture 喂给 `forgejo_config` collector 和 `issue_scan._load_config()` → 断言两者 hosts list 完全相等(per R1 tl C2 fix: parity test 作 "三处一致" 的可执行保障, 替代不可行的代码 100% 共享) |
| Dogfood evidence(Rev1 fix R1 qa M2)| 本 PR formal smoke,**两个 path 都覆盖** | (a) **Default path**: Aria 自身有 explicit `.aria/config.json` `platform_hostnames.forgejo: ["forgejo.10cg.pub"]`,验"verify 已有配置充当 dogfood example"(注:**不**新增,仅 verify);(b) **Env override path**: `unset ARIA_FORGEJO_HOSTS && python3 scan.py` baseline,再 `ARIA_FORGEJO_HOSTS=alt.example.com python3 scan.py` + `jq .forgejo_config.instance` 验 `alt.example.com` 替换 → 写入 PR description 作为正式 dogfood evidence |

### Manual smoke test

```bash
# Case 1: env override
ARIA_FORGEJO_HOSTS="alt.example.com" python3 aria/skills/state-scanner/scripts/scan.py --output /tmp/snap1.json
jq .forgejo_config /tmp/snap1.json  # 应识别 alt.example.com

# Case 2: default
unset ARIA_FORGEJO_HOSTS
python3 aria/skills/state-scanner/scripts/scan.py --output /tmp/snap2.json
jq .forgejo_config /tmp/snap2.json  # 应识别 forgejo.10cg.pub (Aria 自身 origin)
```

---

## Rollout Plan

### Phase B(Implementation)
0. **B.0 Agent assignment** [Rev1 add per R1 tl M3]:本 cycle 为 single-owner dev-claude session,不 dispatch subagent;driver = Claude 自身 + owner 审核。若中途 owner 决定切分,推荐:`backend-architect` 实施 `_common.py` + `forgejo_config.py` + `issue_scan.py` 改动;`qa-engineer` 写 parity test + edge case tests;`code-reviewer` Phase B.3 post-implementation review。当前不预 dispatch,保留 caller 灵活性。
1. B.1:aria/ submodule 切 `feature/forgejo-hosts-parameterization` 分支
2. B.2:实现 A+B+C+D+E(Rev1: 含 C4 L198 删除)(~2h, 比 R1 估时 +30min 因 4 处 + parity test)
3. B.3:Rule #6 substitute artifacts(README + 8 unit tests + parity test + 双 path dogfood)+ all tests pass

### Phase C(Integration)
1. C.1:commit + dual push (origin + github)
2. C.2.4:pre-merge gate(Rule #8 aether ci passing + main 无 in-flight)
3. C.2.4.5:submodule pointer regression gate(v1.28.0 warn-only,本 PR 无 regression)
4. C.2.5:multi-remote post-push SHA parity
5. PR merge aria-plugin
6. 主 Aria gitlink re-bump 到 post-merge SHA(per `feedback_sequenced_multirepo_gitlink_bump`)

### Phase D(Closure)
1. D.1:5+1 SOT atomic bump(plugin.json / marketplace.json × 2 / VERSION / CHANGELOG / README.md + Aria main VERSION)
2. D.2:archive `openspec/changes/aria-forgejo-hosts-parameterization/` → `openspec/archive/2026-MM-DD-aria-forgejo-hosts-parameterization/`
3. D.3:Rule #9 session handoff(本 cycle 跨 4 phases → 触发)

### 5+1 SOT bump 清单(D.1)

| 文件 | 当前 v1.28.0 | 目标 v1.30.0 |
|------|--------------|--------------|
| `aria/.claude-plugin/plugin.json` | `"version": "1.28.0"` | `"1.30.0"` |
| `aria/.claude-plugin/marketplace.json` | 顶层 + plugins[].version 两处 `"1.28.0"` | 两处 `"1.30.0"` |
| `aria/VERSION` | 1.28.0 | 1.30.0 |
| `aria/CHANGELOG.md` | — | new `## [1.30.0]` entry |
| `aria/README.md` | `Version: 1.28.0`(若有) | `Version: 1.30.0` |
| 主项目 `git add aria` | parent v1.28.0 SHA | v1.30.0 ship SHA |

注:跳过 v1.29.0(reserved 给 block-flip 2026-06-07 ship),CHANGELOG entry **不**写 v1.29.0 占位 — 等 block-flip ship 时再补 v1.29.0 entry 后顺序仍为 1.28 → 1.29 → 1.30(SemVer 不要求严格连续 minor)。

> **Cross-coordination 风险**:本 Spec 与 `aria-submodule-gate-block-flip` v1.29.0 ship(2026-06-07)有 SOT 文件碰撞风险(plugin.json / VERSION / CHANGELOG)。Mitigation:本 Spec 必须在 2026-06-06 前 ship 完毕, 给 block-flip ship 留 24h buffer。若本 Spec 拖到 D+13(2026-06-06)未 ship → 主动 defer 到 v1.30.x patch(在 block-flip v1.29.0 ship 后)。

---

## Risks

| # | Risk | Severity | Mitigation |
|---|------|----------|------------|
| R1 | C1/C2/C4 三处 collector 行为漂移(env/config 路径不同) | Med | **Rev1 fix**:`collectors/_common.py::resolve_forgejo_hosts(project_root)` 单一 canonical 入口, `forgejo_config.py` 直接调用;`issue_scan.py::_load_config()` 调用 `_common._parse_env_forgejo_hosts()` 后用同样 fallback 链。**Parity test** `test_forgejo_hosts_parity.py` 在 R2 audit + Phase B.3 + CI 强制等价 |
| R2 | ~~config-loader API 在 collector init time 不可用(circular dep)~~ → **Rev1 N/A** | — | Rev1 fix: 已澄清 config-loader 是 documentation-only LLM Skill 无 Python API;实施改为 inline JSON read + `_common.py` shared helper, 不依赖 config-loader Python module。该 risk 整条 dissolved |
| R3 | Aria 自身 `.aria/config.json` 未显式 set → 仍依赖 default fallback(dogfood 残留) | Low | Phase B.3 步骤:Aria 自身 .aria/config.json 加显式 `platform_hostnames.forgejo` 段,作为 dogfood example |
| R4 | 与 v1.29.0 block-flip ship 撞 slot | Med | Hard cap:2026-06-06 未 ship → 主动 defer 到 v1.30.x patch |
| R5 | 现有用户 env 已用 `ARIA_FORGEJO_HOSTS` 做其他用途(冲突) | Low | env var 命名独特,grep github.com/10CG 全网无相同 var 命名前例 |

---

## Out of Scope(明确 defer)

| Item | 位置 | 何时处理 |
|------|------|---------|
| C5+C6 CI backend abstraction | `aria/skills/phase-c-integrator/scripts/pre_merge_gate.py` | Sprint 2 Level 3 Spec(8-12h) |
| C7 standards SSH URL env | `standards/tools/setup/integrate-standards.sh` | Sprint 2 P2 hygiene(跨 standards submodule) |
| C8 aria-orchestrator PATH | `aria-orchestrator/scripts/inject-demo-issues.py` | 跨独立 submodule, 单独 cycle |
| Feishu 通知抽象 | `aria-orchestrator/notify-feishu.sh` | Sprint 3 P3 |
| Git provider abstract base class(GitProvider ABC) | `aria/scripts/git-providers/` | M7+ aria-fleet 主线 |
| `~/.aether/config.yaml` 路径参数化 | `pre_merge_gate.py` | 与 C5+C6 一起 Sprint 2 |

---

## Cross-references

- Boundary audit memo: `.aria/notes/2026-05-27-boundary-audit-10cg-hardcode.md`(原始 audit, 详细修复建议)
- Strategic memo: `.aria/notes/2026-05-27-aria-fleet-three-layer-architecture.md` §4 边界切割规则
- Brainstorm DEC: `.aria/decisions/2026-05-27-aria-fleet-brainstorm.md` D2(通用层硬约束)
- Handoff: `docs/handoff/2026-05-27-aria-fleet-strategic-pivot-session.md` §6 #2(P0 boundary audit Sprint 1)
- Memory:
  - `feedback_three_layer_universal_workspace_instance`(L1 禁 hardcode org-specific)
  - `feedback_deterministic_structural_skill_rule6_substitute`(Rule #6 substitute pattern)
  - `feedback_audit_convergence_patterns`(L2 = 2-round baseline)
  - `feedback_release_phase_d_5_files_synchronization`(5+1 SOT)
  - `feedback_sequenced_multirepo_gitlink_bump`(submodule PR 先 merge → gitlink re-bump)
  - `feedback_dec_ship_target_staleness_verify`(version stake-out 已完成,见 §A.0 task)

---

**Drafted**: 2026-05-27 (R1)
**Rev1**: 2026-05-27 (post R1 audit fix-verify, 3 agents unanimous REVISE → addressing 3 Critical + 6 high-priority Major + selected Minor)
**Author**: dev-claude (single owner simonfishgit session)
**Phase A.2 Rev1**: Complete, ready for R2 verify audit(同 3 agents:tech-lead + backend-architect + qa-engineer)
**Expected R2 verdict**: PASS_WITH_WARNINGS unanimous → 实质 CONVERGED(per `feedback_audit_convergence_patterns` L2 = 2-round baseline)

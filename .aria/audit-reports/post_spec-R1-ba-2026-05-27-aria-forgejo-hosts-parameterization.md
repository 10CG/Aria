---
audit_id: post_spec-R1-ba-2026-05-27-aria-forgejo-hosts-parameterization
checkpoint: post_spec
round: R1
agent: backend-architect
spec_id: aria-forgejo-hosts-parameterization
spec_level: L2
verdict: REVISE
verdict_reason: "config-loader API 描述与架构现实不符(Critical),且 C2 修复范围遗漏 issue_scan.py L198 第二处 hardcode"
issues:
  critical: 1
  major: 2
  minor: 2
timestamp: 2026-05-27T08:00:00Z
---

# Backend-Architect Audit Report — R1
## Spec: aria-forgejo-hosts-parameterization

---

## Critical Findings

### C-1: config-loader 无 Python API — `_config_loader_forgejo_hosts()` 调用对象不存在

**位置**: `proposal.md §What/A` 第 76 行 — `config_hosts = _config_loader_forgejo_hosts()`

**验证方式**: 实际检查 `/home/dev/Aria/aria/skills/config-loader/` 目录结构:

```
/home/dev/Aria/aria/skills/config-loader/
├── config-example.md
├── DEFAULTS.json
└── SKILL.md   ← disable-model-invocation: true, allowed-tools: Read, Glob
```

config-loader 是**纯 LLM Skill**，没有任何 Python 模块实现。`SKILL.md` 明确标注 `disable-model-invocation: true`，它仅是一个 AI Skill prompt，不暴露任何可被 Python `import` 的 API。

**当前实际架构**:

- `issue_scan.py` 有自己的 `_load_config()` 直接读 `.aria/config.json`（L90-123），**不通过 config-loader**
- `forgejo_config.py` 目前根本不读 config，仅用模块常量（L35）
- `scan.py` 中两个 collector 完全独立，无共享 config 层

**影响**: spec §A 的伪代码 `_config_loader_forgejo_hosts()` 在 Phase B 无法实现为描述的形式。实现者要么：(a) 误解为需要创建一个新 Python 模块（超出 spec 范围），(b) 直接内联实现 JSON 读取（实质上重复 `issue_scan.py` 已有的 `_load_config()` 逻辑）。

**修复建议**: 将 §A 的 helper 改为明确的内联 JSON 读取模式，与 `issue_scan.py` 现有 `_load_config()` 对称，或者明确说明"复用 `issue_scan._load_config()` 中的 config 读取逻辑"。建议表述为:

```python
def _config_loader_forgejo_hosts(project_root: Path) -> list[str] | None:
    """Read .aria/config.json directly (no external dependency).
    Returns list of forgejo hosts if configured, else None.
    Fail-soft: any read/parse error returns None.
    """
    cfg_path = project_root / ".aria" / "config.json"
    try:
        with cfg_path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
        hosts = (raw.get("state_scanner") or {}).get("issue_scan", {}) \
                    .get("platform_hostnames", {}).get("forgejo")
        if isinstance(hosts, list) and hosts:
            return hosts
    except (OSError, json.JSONDecodeError):
        pass
    return None
```

同时 `forgejo_config.py` 需要添加 `import json, os` 导入（当前 imports 仅有 `re`, `Path`, `_common`）。

---

## Major Findings

### M-1: C2 范围遗漏 — `issue_scan.py` L198 第二处 `forgejo.10cg.pub` hardcode

**位置**: `issue_scan.py` L193-199 `_detect_platform()` Level 3 URL 子串 heuristic:

```python
# Level 3: URL substring heuristic (lower priority than explicit map)
low = remote_url.lower()
if "github.com" in low:
    return "github"
# Well-known forgejo domain fallback (matches SKILL.md example).
if "forgejo.10cg.pub" in low:
    return "forgejo"
```

**问题**: 边界审计 C2 仅定位到 L71（`DEFAULT_CONFIG` 中的 `platform_hostnames.forgejo`），但 L198 的 Level 3 heuristic 同样 hardcode 了 `forgejo.10cg.pub`。这条路径在以下场景触发：**用户设置了自定义 Forgejo host（如 `forge.example.com`），但 `platform_hostnames` map 未命中时 Level 3 fallback 仍返回 None**——导致自定义 Forgejo 实例的 `_detect_platform()` 返回 `None`（`ERR_PLATFORM_UNKNOWN`），issue scan 功能完全失效。

Spec §What/B 删除了 `DEFAULT_CONFIG` 中的 hardcode，但 Level 3 heuristic 未处理。这与验收标准 AC-2（自定义 host 能被识别）相矛盾：如果用户只设 `ARIA_FORGEJO_HOSTS=custom.example.com`，`DEFAULT_CONFIG["platform_hostnames"]["forgejo"]` 被替换后，Level 2 map 命中；但如果用户绕过 `platform_hostnames`（直接设 `platform: forgejo`），Level 3 仍是死路。更关键的是：**完成本 spec 修复后，`forgejo.10cg.pub` 的硬编码从 `DEFAULT_CONFIG` 删去，Level 3 也删去，新 install 的默认态会丢失 fallback**——除非 env/config 路径完全覆盖，否则 vanilla install 无 `platform_hostnames` 配置时 `_detect_platform` 可能走错路径。

**修复建议**: Spec §B 的范围应包含 L198：要么删去 Level 3 forgejo-specific fallback（让 Level 2 `platform_hostnames` map 承担全部匹配），要么改为动态读取 `_KNOWN_FORGEJO_HOSTS`（与 C1 共享常量）。推荐前者，因为修复后 DEFAULTS.json 已保证 `forgejo.10cg.pub` 在 `platform_hostnames` map 中作为 fallback。

### M-2: C1/C2 共用 helper 的 `project_root` 参数传递路径未设计

**位置**: `proposal.md §A` helper 签名 + §B 对称实现

**问题**: spec 提出 `_config_loader_forgejo_hosts()` 是"共享 helper，三处复用"，但 `forgejo_config.py` 在模块加载时（module scope）执行:

```python
_KNOWN_FORGEJO_HOSTS: tuple[str, ...] = _load_known_forgejo_hosts()
```

此时 `project_root` 尚未确定（`collect_forgejo_config(project_root)` 的调用发生在 `scan.py` 运行时，而非 import 时）。若 `_load_known_forgejo_hosts()` 尝试读取 `.aria/config.json`，它需要知道 project_root，但模块常量在 import 时求值，此时不存在可用的 `project_root`。

两种解法路径：
1. **懒加载**: 将 `_KNOWN_FORGEJO_HOSTS` 改为在 `collect_forgejo_config(project_root)` 调用时动态解析，而非模块常量（需改当前代码结构）
2. **仅 env override at module level**: 模块级常量只做 env var 解析（不读 config），config 读取推迟到 `collect_forgejo_config()` 内部（与 `issue_scan.py` 的 `_load_config()` 在 `collect_issue_scan()` 内部调用对称）

Spec 的伪代码暗示两层（env + config）都在模块级 `_load_known_forgejo_hosts()` 执行，但这要求模块加载时就能访问 `project_root`，**实际上不可行**。这个架构问题在 Phase B 必然需要重新设计。

**修复建议**: spec 应明确 C1 的两级拆分：
- 模块级常量只做 env var 解析（`ARIA_FORGEJO_HOSTS`）
- config.json 读取在 `collect_forgejo_config(project_root)` 内部，通过局部变量覆盖 `_KNOWN_FORGEJO_HOSTS`（或传入 `_detect_forgejo_host()`）

---

## Minor Findings

### N-1: 测试用例 4 个未覆盖 "empty env / whitespace" 边界场景

**位置**: `proposal.md §Testing Strategy` — 4 个 unit test 清单

**问题**: Spec 的 `_load_known_forgejo_hosts()` 实现已考虑了空字符串处理（`.strip()` + `if h.strip()`），但测试列表中无:
- `test_empty_env_var_falls_through`: `ARIA_FORGEJO_HOSTS=""` → 应 fallback 到 config/default
- `test_whitespace_only_env_var`: `ARIA_FORGEJO_HOSTS="  "` → strip 后空，应 fallback
- `test_empty_list_from_config`: config 设 `forgejo: []` → empty list，应 fallback 到 DEFAULTS

这些是 `if env:` / `if config_hosts:` 两个判断的关键边界，不覆盖存在 future regression 风险。

**影响**: Minor — 实现代码已有防护，测试覆盖缺口，Rule #6 structural substitute 精神上要求 boundary case 覆盖。

**建议**: 在测试策略中补充上述 3 个边界 test case。

### N-2: `issue_scan.py` 的 C2 修复描述与现有实现存在表述偏差

**位置**: `proposal.md §What/B` — "删除 `DEFAULT_CONFIG.platform_hostnames` 中的 hardcode list"

**问题**: 当前 `issue_scan.py` 的 `_load_config()` 已经支持从 `.aria/config.json` 合并 `platform_hostnames`（L118-123），这正是 spec 希望的行为。Aria 项目自身的 `.aria/config.json` 已经显式配置了 `platform_hostnames.forgejo`，所以 C2 中的 hardcode 目前**对 Aria 自身已被覆盖**，不是 Aria 的实际问题，而是其他 install 的问题。

`DEFAULT_CONFIG` 中的 `"forgejo": ["forgejo.10cg.pub"]`（L71）已经通过 `_load_config()` 的 merge 逻辑成为 DEFAULTS.json C3 的"Python 镜像"。Spec §B 说"删除 hardcode"后改为"延迟解析"，但实际上只需要给 `_load_config()` 增加 env var override 层即可，`DEFAULT_CONFIG` 的 `forgejo` 值可以保留（作为 Python 层 fallback，与 DEFAULTS.json C3 平行），或者统一由 DEFAULTS.json 读取。

这不影响正确性，但"删除 DEFAULT_CONFIG 中的 hardcode list"的表述可能造成实现歧义（直接删掉 forgejo key vs 改为从 env 读取）。

**建议**: 澄清 §B 的目标是"在 `_load_config()` 最前面添加 env var override 层"，而非删除 `DEFAULT_CONFIG` 中的 `forgejo` 条目（否则需要特别处理 key 缺失的 fallback 路径）。

---

## Verdict Summary

**REVISE** — 1 Critical + 2 Major 需要在 proposal.md 中澄清后方可进入 Phase B。

**Critical (C-1)**: `_config_loader_forgejo_hosts()` 调用的对象（config-loader Python API）不存在。这是架构描述错误，不是实现细节，必须在 spec 中明确"直接内联读 JSON，无外部依赖"。

**Major (M-1)**: C2 范围遗漏 `issue_scan.py` L198 Level 3 URL heuristic 中的第二处 `forgejo.10cg.pub` hardcode。不修复则 AC-2（自定义 host 识别）在特定路径下失效。

**Major (M-2)**: C1 的 `_load_known_forgejo_hosts()` 在模块级执行读 config 的设计有 `project_root` 不可用的根本问题，spec 必须明确拆分：模块级只做 env 解析，config 读取在 collector 函数内部。

**所需修订幅度**: 小（L2 spec 修订，不影响整体架构决策，不需要重新 brainstorm）。预计修订 §A 和 §B 约 10-15 行伪代码 + §Testing 增加 3 条测试。

**Backward compat**: 确认零破坏——Aria 自身 `.aria/config.json` 已有显式 `platform_hostnames.forgejo` 配置，即使模块级 fallback 路径变化，Aria 自身行为不变。

**无 blocker 的部分**: C3 (DEFAULTS.json)、§D (SKILL.md docs)、Rollout Plan、version coordination、env var 命名 (`ARIA_FORGEJO_HOSTS` 无冲突，现有 `ARIA_FORGEJO_REPO/TOKEN/INTERNAL_URL` 均为不同语义)——全部设计正确，可直接进入 Phase B。

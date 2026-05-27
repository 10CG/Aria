---
audit_id: post_spec-R2-ba-2026-05-27-aria-forgejo-hosts-parameterization
checkpoint: post_spec
round: R2
agent: backend-architect
spec_id: aria-forgejo-hosts-parameterization
spec_level: L2
verdict: PASS_WITH_WARNINGS
verdict_reason: "R1 三条 finding 已技术上 addressed,但 §B 伪代码存在 env-override-then-config-overwrite 隐患需 Phase B 实施前确认修正方向"
issues:
  critical: 0
  major: 0
  minor: 1
r1_findings_status:
  C-1: CLOSED
  M-1: CLOSED
  M-2: CLOSED
  N-1: ADDRESSED
  N-2: ADDRESSED
timestamp: 2026-05-27T09:30:00Z
---

# Backend-Architect Audit Report — R2
## Spec: aria-forgejo-hosts-parameterization (Rev1)

---

## R1 Findings Verify

### C-1 CLOSED — `_common.py::resolve_forgejo_hosts(project_root)` + inline JSON

**验证方式**: 实测 `aria/skills/state-scanner/scripts/collectors/_common.py` 现状。

**现状确认**:
- `_common.py` 当前 imports: `logging`, `subprocess`, `dataclasses`, `pathlib.Path`, `typing.Any`
- **无** `json`, `os` — Rev1 §A 需要新增这两个 stdlib import, 无冲突风险
- `forgejo_config.py` 已有 `from ._common import CollectorResult, _run`(L31)— 边界合法,可继续扩展为 `from ._common import CollectorResult, _run, resolve_forgejo_hosts`
- `issue_scan.py` 已有 `from ._common import CollectorResult, _run, log`(L42)— 同样可无缝扩展

**Rev1 fix 技术可行性**: `resolve_forgejo_hosts(project_root)` 设计自洽:
- `_parse_env_forgejo_hosts()`: 纯 env 读取,import-time 安全,无 `project_root` 依赖
- `_read_config_forgejo_hosts(project_root)`: 明确 collector-time 调用,拿到 `project_root` 后再读 `.aria/config.json`
- `resolve_forgejo_hosts(project_root)`: 统一 3-tier 入口,`forgejo_config.py::collect_forgejo_config(project_root)` 在 collector function body 内调用即可

**C-1 结论**: ✅ CLOSED。架构描述已从"config-loader Python API"修正为合法的 `_common.py` shared helper + inline JSON 读取。Phase B 起手可直接落代码,无结构歧义。

---

### M-1 CLOSED — §E deliverable 覆盖 C4 (issue_scan.py L198)

**验证方式**: 实测确认 `issue_scan.py` L198 现状:

```python
# Level 3: URL substring heuristic (lower priority than explicit map)
low = remote_url.lower()
if "github.com" in low:
    return "github"
# Well-known forgejo domain fallback (matches SKILL.md example).
if "forgejo.10cg.pub" in low:
    return "forgejo"            # ← L198, 实测存在
```

**Rev1 §E 的安全性验证**:
- Aria 自身 `.aria/config.json` 已有 `state_scanner.issue_scan.platform_hostnames.forgejo: ["forgejo.10cg.pub"]`(实测确认)
- `_load_config()` 的 `merged` 初始化从 `DEFAULT_CONFIG` deep-copy,`platform_hostnames.forgejo = ["forgejo.10cg.pub"]` 始终存在
- 删 L198 后,`_detect_platform()` Level 2 `platform_hostnames` map 会命中 `forgejo.10cg.pub` — 行为等价
- 现有测试 `TestPlatformDetection::test_forgejo_via_hostmap`(test_issue_scan_helpers.py L89-93) 使用 `BASE_CFG` 含 `platform_hostnames.forgejo: ["forgejo.10cg.pub"]`,走的是 Level 2 路径,**不**依赖 L198 Level 3 heuristic — 删 L198 后该测试仍通过
- 自定义 host AC-10 修复正确:`ARIA_FORGEJO_HOSTS=forge.example.com` → `_load_config()` env override 后 `platform_hostnames.forgejo = ["forge.example.com"]` → Level 2 命中 → `_detect_platform` return `"forgejo"` ✅

**M-1 结论**: ✅ CLOSED。§E 完整覆盖 C4,删 L198 后 backward compat 已验证安全。

---

### M-2 CLOSED — 2-tier 拆分 module-level env-only + collector-time config

**验证方式**: 追踪 Rev1 §A 的架构决策完整性。

**R1 指出的根本问题**: 模块级 `_KNOWN_FORGEJO_HOSTS = _load_known_forgejo_hosts()` 在 import 时执行,此时 `project_root` 不可用。

**Rev1 fix 设计**:
> "Rev1 决策: 完全删除 module-level 常量 → 所有 hosts 解析推迟到 `collect_forgejo_config(project_root)` 内, 由 `resolve_forgejo_hosts(project_root)` 统一处理"

**验证 Phase B 起手可行性**:
1. `forgejo_config.py` L35 `_KNOWN_FORGEJO_HOSTS` 常量 → 删除 ✅(无其他 module 依赖此常量)
2. `_detect_forgejo_host(remote_url)` 单参数签名 → 改为 `_detect_forgejo_host(remote_url, known_hosts)` — **注意**: 现有 `test_forgejo_config.py` L12-35 以单参数形式调用此函数,Phase B 需同步更新测试。Spec 未显式提醒此处测试更新,但可接受(Phase B 常规 test 更新,不是 spec 歧义)
3. import-time binding 风险:Rev1 架构完全消除了 module-level 常量,`monkeypatch.setenv` 测试 isolation 天然成立

**§A 设计自洽确认**: `resolve_forgejo_hosts(project_root)` 在 `collect_forgejo_config(project_root)` 函数体内调用,`project_root` 已可用。qa M1 #4 import-time binding 问题被架构上消除。

**M-2 结论**: ✅ CLOSED。2-tier 拆分设计技术自洽,Phase B 可直接落。

---

### N-1 ADDRESSED — 边界 test case 覆盖

**验证**: Rev1 AC edge cases 已扩展为 12 条(AC-6 empty env / AC-7 empty config list / AC-8 duplicate hosts / AC-9 C4 sanity / AC-10 custom host),Testing Strategy 列出 9+ unit tests + parity test。

**N-1 结论**: ✅ ADDRESSED。边界覆盖充足。

---

### N-2 ADDRESSED — §B 措辞偏差修正

**验证**: Rev1 changelog 明确标注"§B 措辞改为 '在 `_load_config()` 前加 env override layer' (非 '删 DEFAULT_CONFIG hardcode')"。`DEFAULT_CONFIG["platform_hostnames"]["forgejo"]` 保留作 Python-layer fallback。

**N-2 结论**: ✅ ADDRESSED。

---

## R2 New Findings

### W-1 (Warning/Minor): §B 伪代码 env-override-then-config-overwrite 实施歧义

**位置**: `proposal.md §What/B` 伪代码 + 注释 "Skip config.json merge for forgejo key; env wins"

**问题描述**: Rev1 §B 伪代码结构如下:

```python
def _load_config(project_root: Path) -> dict[str, Any]:
    # ... existing setup of merged dict + DEFAULT_CONFIG copy ...

    # ---- Rev1 new: env override layer (highest precedence) ----
    from ._common import _parse_env_forgejo_hosts
    env_hosts = _parse_env_forgejo_hosts()
    if env_hosts:
        merged["platform_hostnames"]["forgejo"] = list(env_hosts)
        # Skip config.json merge for forgejo key; env wins
    # ---- end Rev1 new ----

    # ... existing config.json read + merge logic unchanged ...
    return merged
```

注释说"env wins"并"skip config.json merge for forgejo key",但**伪代码中没有实现这个 skip 的任何逻辑**。现有 `_load_config()` 的 config.json merge 段(L118-122)无条件遍历 `platform_hostnames` 字典并覆写 `merged["platform_hostnames"][k]`:

```python
hostnames = block.get("platform_hostnames")
if isinstance(hostnames, dict):
    for k, v in hostnames.items():
        if isinstance(v, list):
            merged["platform_hostnames"][k] = list(v)  # ← 会覆盖 env 设置的 forgejo hosts
```

如果 Phase B 实施者按伪代码字面落代码,**不**添加 skip guard,则:
- 用户同时设了 `ARIA_FORGEJO_HOSTS=forge.example.com` 且 `.aria/config.json` 有 `platform_hostnames.forgejo: ["other.com"]`
- 结果: env 设置被 config.json 静默覆盖,env precedence 失效
- 这与 precedence chain 定义(env > config > default)矛盾,且是 silent failure

**两种正确实现**:

选项 A(推荐 — 简洁,语义最清晰): 将 env override block 移到 config.json merge **之后**,让 env 作为最终 post-merge override:

```python
# ... existing config.json read + merge logic (unchanged) ...

# Post-merge env override (always wins over config.json)
from ._common import _parse_env_forgejo_hosts
env_hosts = _parse_env_forgejo_hosts()
if env_hosts:
    merged["platform_hostnames"]["forgejo"] = list(env_hosts)

return merged
```

选项 B(等效,如需 early-exit): 在 env 设置后,跳过 config.json 中 forgejo key 的 merge:

```python
if isinstance(hostnames, dict):
    for k, v in hostnames.items():
        if k == "forgejo" and env_hosts:  # env already set this
            continue
        if isinstance(v, list):
            merged["platform_hostnames"][k] = list(v)
```

**严重性评估**: Minor/Warning 级。
- 对 `forgejo_config.py` collector 无影响(走 `resolve_forgejo_hosts()` 路径,独立 self-contained)
- 对 `issue_scan.py` 的 `_load_config()` 实施有实质影响,但仅在"用户同时设 env + config.json"时触发
- vanilla install(无 env,无 config.json forgejo block)或"仅 env 无 config"场景不受影响
- Phase B 实施者经验充足可独立判断,但 spec 应明确消除歧义

**建议**: §B 伪代码更新为选项 A(把 env override block 放到 config.json merge 之后),或在注释中明确 "env override block 必须在 config.json merge 之后,或 merge loop 内需加 `if k == 'forgejo' and env_hosts: continue` guard"。

**不阻塞 Phase B**: 实施者有足够上下文自行选择 A 或 B,且 AC-1 + 单元测试覆盖会 catch 此 bug。**但建议 spec owner 在 Phase B kick-off 前用一行注释消除歧义。**

---

### W-2 (Informational/Minor): §B 的 inline 函数级 import 模式可简化

**位置**: `proposal.md §What/B` 伪代码 `from ._common import _parse_env_forgejo_hosts`

**观察**: `issue_scan.py` L42 已有 `from ._common import CollectorResult, _run, log` 模块级 import。Rev1 §B 伪代码在 `_load_config()` 函数体内再做一次 `from ._common import _parse_env_forgejo_hosts`,技术上有效(Python 允许函数级 relative import),但:
- 不符合 `issue_scan.py` 现有代码风格(所有 intra-package import 在模块顶部)
- 函数级 import 会在每次 `_load_config()` 调用时执行 import machinery(虽然已缓存,但有 micro-overhead)

**推荐**: Phase B 实施时,将 `_parse_env_forgejo_hosts` 加入 L42 模块级 import:
```python
from ._common import CollectorResult, _run, log, _parse_env_forgejo_hosts
```

**严重性**: Informational,不阻塞 Phase B。代码审查时自然会 catch。

---

## Verdict Summary

**PASS_WITH_WARNINGS** — R1 全部 5 条 finding(C-1 / M-1 / M-2 / N-1 / N-2)技术上已 addressed,Rev1 fix 架构方向正确。新增 1 Minor warning(W-1):§B 伪代码的 env-override skip 实施歧义。

**架构健康度确认**:
- `_common.py::resolve_forgejo_hosts(project_root)` 设计自洽,可作为所有 forgejo-aware collector 的规范入口
- C4 (L198) 删除安全:现有测试走 Level 2 路径,backward compat 已实测验证
- 2-tier 拆分(env-only module-level → collector-time config)彻底消除 import-time `project_root` 不可用问题
- `test_forgejo_config.py` 的 `_detect_forgejo_host` 单参数调用需在 Phase B 同步更新(常规 test 维护,非 spec 歧义)

**Phase B 起手条件**: 满足。W-1 建议 spec owner 在 §B 注释补充一行实施指引(选项 A 或 B),不需要重新 revision spec。

**L2 2-round baseline**: R1 REVISE → Rev1 → R2 PASS_WITH_WARNINGS — 符合 `feedback_post_spec_audit_two_round_pragmatic_for_l2` 收敛模式。

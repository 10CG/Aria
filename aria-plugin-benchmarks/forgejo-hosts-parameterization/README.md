# aria-forgejo-hosts-parameterization — Rule #6 Structural Substitute

> **Spec**: `openspec/changes/aria-forgejo-hosts-parameterization/` (Approved 2026-05-27, ship v1.30.0)
> **Skill type**: deterministic structural (collector behavior parameterization, no LLM behavior change)
> **Rule #6 substitute pattern**: per `feedback_deterministic_structural_skill_rule6_substitute` — **不**跑 `/skill-creator` LLM AB benchmark;改用 structural fixture + unit tests + dogfood
> **Why no LLM AB**: 本 Spec 改的是 collector data 解析 (env→config→default 优先链), 不影响 AI 决策路径。LLM with/without 跑同一 snapshot 输出本质不变,benchmark 噪声 > 真实 delta

## Substitute artifacts

| Component | Location | Coverage |
|-----------|----------|----------|
| **Structural fixture (本 README)** | `aria-plugin-benchmarks/forgejo-hosts-parameterization/README.md` | 4 hardcode 删/改 map + 12 AC behavior 表 + edge case cheatsheet |
| **Unit tests** | `aria/skills/state-scanner/tests/test_forgejo_config.py` (+16 tests) + `tests/test_issue_scan_helpers.py` (+11 tests) | 27 new tests, 全 PASS |
| **Full test suite** | `aria/skills/state-scanner/tests/run_tests.py` | 631/631 PASS post-implementation (无 regression) |
| **Dogfood evidence(formal)** | 本文档 §Dogfood Smoke Results 段 | dual-path: default + env override 实测 |

## 4 处 hardcode 删/改 map

| ID | 文件 | 行号 | Before | After |
|----|------|------|--------|-------|
| **C1** | `aria/skills/state-scanner/scripts/collectors/forgejo_config.py` | L33-35 | `_KNOWN_FORGEJO_HOSTS: tuple[str, ...] = ("forgejo.10cg.pub",)` (module-level constant) | 删除 module-level constant;改为 collector 内 `resolve_forgejo_hosts(project_root)` 运行时解析 |
| **C2** | `aria/skills/state-scanner/scripts/collectors/issue_scan.py` | L66-78 (`DEFAULT_CONFIG`) | `DEFAULT_CONFIG["platform_hostnames"]["forgejo"] = ["forgejo.10cg.pub"]` (hardcode) | **保留** DEFAULT_CONFIG 不动(作 Python-layer fallback);**新增** env override AS FINAL LAYER 在 `_load_config()` (L122 之后) |
| **C3** | `aria/skills/config-loader/DEFAULTS.json` | L45 | `"forgejo": ["forgejo.10cg.pub"]` | 不变(legacy backward-compat fallback;DEC D2 compliance discussion 见 proposal §C) |
| **C4** | `aria/skills/state-scanner/scripts/collectors/issue_scan.py` | L198(已删) | `if "forgejo.10cg.pub" in low: return "forgejo"` (`_detect_platform()` Level 3 URL substring heuristic) | **删除** — Level 2 `platform_hostnames` map 单一权威 |
| **NEW** | `aria/skills/state-scanner/scripts/collectors/_common.py` | L24-83(新增) | — | Canonical 3-layer resolver `resolve_forgejo_hosts(project_root)` + helpers `_parse_env_forgejo_hosts()` + `_read_config_forgejo_hosts()` + `_LEGACY_FORGEJO_FALLBACK` |

## Precedence chain(canonical)

```
环境变量 ARIA_FORGEJO_HOSTS=h1,h2,h3 (comma-separated)
       ↓ (if unset/empty/whitespace)
.aria/config.json → state_scanner.issue_scan.platform_hostnames.forgejo: [...]
       ↓ (if missing/parse-error/empty-list)
Legacy fallback: ("forgejo.10cg.pub",)
```

`forgejo_config.py` 和 `issue_scan.py` 都走同一 `_parse_env_forgejo_hosts()` env-detection helper(`_common.py`),保证两 collector env 行为对称。`issue_scan.py::_load_config()` 是唯一持有 config.json merge 逻辑的入口(`forgejo_config.py` 通过 `resolve_forgejo_hosts()` 调用 `_read_config_forgejo_hosts()`)。

## 12 AC behavior 表

| AC # | Path | Expected | Test coverage |
|------|------|----------|---------------|
| 1 | `ARIA_FORGEJO_HOSTS=h1,h2` | 识别 h1, h2(不再识 forgejo.10cg.pub)| `TestForgejoHostsResolver::test_env_override_multi_host` + `TestLoadConfigEnvOverride::test_env_multi_host_preserved` |
| 2 | 无 env + `.aria/config.json` 设 custom.example.com | 识别 custom.example.com | `TestForgejoHostsResolver::test_config_json_precedence` + `TestLoadConfigEnvOverride::test_config_json_wins_over_default_when_no_env` |
| 3 | 无 env + 无 config | 识别 forgejo.10cg.pub | `TestForgejoHostsResolver::test_default_fallback_no_env_no_config` + `TestLoadConfigEnvOverride::test_no_env_no_config_default_preserved` |
| 4 | 同 env + 同 config → 4 处一致 | `forgejo_config` + `issue_scan._load_config` 一致 | 显式 cross-test via env_beats_config + config_json_wins_over_default 双向验证;parity 在 collector 集成层 |
| 5 | scan.py exit 0/10 | 现有 Aria 跑通 | 本 README §Dogfood Smoke Results |
| 6 | empty env `""` / whitespace `"   "` | fall through to config/default | `test_empty_env_falls_through_to_default` + `test_whitespace_env_falls_through_to_default` + `test_empty_env_falls_through_to_config` |
| 7 | config 含 `[]` empty list | fall through to default | `test_empty_config_list_falls_through_to_default` |
| 8 | env/config 含 duplicate hosts | preserve duplicates(callers idempotent)| `test_duplicate_hosts_preserved` |
| 9 | C4 删除后 vanilla install | `forgejo.10cg.pub` URL 仍识别 forgejo(via Level 2 map)| `test_forgejo_level3_substring_fallback_removed` + `test_github_level3_substring_fallback_preserved` |
| 10 | custom host via env + matching remote | `_detect_platform` return "forgejo" | `test_custom_forgejo_host_via_level2_only` + `TestCustomHostCollectorE2E::test_custom_host_detected_via_env` |
| 11 | 8+ unit tests 覆盖 | 27 new tests | 27 个新增, 全 PASS |
| 12 | Test isolation(monkeypatch + 无 module-level binding)| 删 `_KNOWN_FORGEJO_HOSTS` const → architecturally eliminated | `test_no_module_level_forgejo_hosts_constant` |

## Edge case cheatsheet

| 输入 | 行为 |
|------|------|
| `ARIA_FORGEJO_HOSTS` 未设 | use config / default |
| `ARIA_FORGEJO_HOSTS=""` | use config / default(NOT 视为"用户清空 hosts")|
| `ARIA_FORGEJO_HOSTS="   "` | 同上(strip 后空)|
| `ARIA_FORGEJO_HOSTS="h1,h2"` | use [h1, h2](去 surrounding whitespace)|
| `ARIA_FORGEJO_HOSTS="h1, ,h2"` | use [h1, h2](skip empty entries)|
| `ARIA_FORGEJO_HOSTS="h1,h1,h2"` | use [h1, h1, h2](duplicate preserved)|
| `.aria/config.json` 缺失 | env 优先 → 否则 default |
| `.aria/config.json` JSON 错 | log warning + 当作缺失 |
| `config.json` 含 `forgejo: []` | fall through to default(empty list = NOT silently disable)|
| `config.json` 含 `forgejo: ["h.com"]` | use [h.com](unless env override)|
| env + config 都设 | **env wins**(post-merge final layer)|

## Dogfood Smoke Results(formal evidence per proposal §Testing)

执行环境: Aria self-repo, branch `feature/forgejo-hosts-parameterization`, 2026-05-27.

### Default path

```bash
$ unset ARIA_FORGEJO_HOSTS
$ python3 aria/skills/state-scanner/scripts/scan.py --output /tmp/snap-base.json
$ jq .forgejo_config /tmp/snap-base.json
{
  "forgejo_remote_detected": true,
  "instance": "forgejo.10cg.pub",
  "config_status": "configured"
}
```

✅ 识别 `forgejo.10cg.pub`(via legacy fallback 路径,Aria `.aria/config.json` 有显式 `platform_hostnames.forgejo: ["forgejo.10cg.pub"]` 也命中)。

### Env override path

```bash
$ ARIA_FORGEJO_HOSTS=alt.example.com python3 aria/skills/state-scanner/scripts/scan.py --output /tmp/snap-env.json
$ jq .forgejo_config /tmp/snap-env.json
{
  "forgejo_remote_detected": false
}
```

✅ Env override 生效:Aria origin URL `ssh://forgejo@forgejo.10cg.pub/10CG/Aria.git` 在 `known_hosts = ("alt.example.com",)` 中**找不到**,collector 正确 return `forgejo_remote_detected: false`,**没有**走 legacy fallback。AC §1 env precedence confirmed working in production code path.

### scan.py 整体 exit code

```bash
$ python3 aria/skills/state-scanner/scripts/scan.py --output /tmp/snap.json; echo EXIT=$?
EXIT=0
```

✅ AC §5 满足:scan.py 整体 exit 0(无 regression)。

### Full test suite

```bash
$ python3 aria/skills/state-scanner/tests/run_tests.py
...
Ran 631 tests in 14.162s
OK
```

✅ 631/631 PASS — 全 state-scanner test suite 无 regression。

## Rule #6 compliance verdict

✅ **PASS** — structural fixture + 27 new unit tests + dual-path dogfood smoke + 631-test full suite green。

无需 `/skill-creator` LLM AB benchmark(per `feedback_deterministic_structural_skill_rule6_substitute`)。

## Cross-references

- OpenSpec: `openspec/changes/aria-forgejo-hosts-parameterization/proposal.md`
- Audit reports: `.aria/audit-reports/post_spec-{R1,R2}-{tl,ba,qa}-2026-05-27-aria-forgejo-hosts-parameterization.md` (6 reports)
- Boundary audit memo: `.aria/notes/2026-05-27-boundary-audit-10cg-hardcode.md`
- aria-fleet strategic memo: `.aria/notes/2026-05-27-aria-fleet-three-layer-architecture.md` §4(边界切割规则)

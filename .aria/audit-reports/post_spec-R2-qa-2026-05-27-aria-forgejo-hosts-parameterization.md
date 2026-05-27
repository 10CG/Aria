---
audit_id: post_spec-R2-qa-2026-05-27-aria-forgejo-hosts-parameterization
checkpoint: post_spec
round: R2
agent: qa-engineer
spec_id: aria-forgejo-hosts-parameterization
spec_level: L2
verdict: PASS_WITH_WARNINGS
verdict_reason: "R1 三个 Major 均已实质性修复;发现 1 个新 Minor(§B env override 代码草图注释与逻辑不一致)和 2 个 carry-forward Minor,不阻塞 Phase B 启动。"
issues:
  critical: 0
  major: 0
  minor: 1
r1_findings_status:
  Major-1: CLOSED
  Major-2: CLOSED
  Minor-1: CLOSED
  Minor-2: CARRY-FORWARD
  Minor-3: CARRY-FORWARD
timestamp: 2026-05-27T14:30:00Z
---

# QA-Engineer Audit Report — R2

**Spec**: `aria-forgejo-hosts-parameterization`  
**文件**: `/home/dev/Aria/openspec/changes/aria-forgejo-hosts-parameterization/proposal.md`  
**审计人**: qa-engineer  
**Round**: R2 (L2 baseline = 2-round; 本轮为 final verify)

---

## R1 Findings 逐条 Verify

### Major-1: AC 边界覆盖不足 — CLOSED

**Verify 结果**: 充分修复。

Rev1 将 AC 从 §1-5 扩展至 §1-12,新增 7 个 edge case:

- AC §6: `ARIA_FORGEJO_HOSTS=""` / all-whitespace → fall through(对应 R1 缺失 `test_empty_env_falls_through`)
- AC §7: `platform_hostnames.forgejo: []` 空 list → fall through 到 DEFAULTS.json(明确语义决策:空 list ≠ 禁用 forgejo detection)
- AC §8: 重复 hosts 保留(不 dedup;调用方决定;idempotent 行为)
- AC §11: 至少 8 个 unit test,枚举名称到 `test_duplicate_hosts_tolerated` / `test_whitespace_env_falls_through` 等
- AC §12: monkeypatch isolation 要求明确化(architecturally eliminated + test 仍断言)

`_common.py` 代码草图中 `_parse_env_forgejo_hosts()` 实现直接覆盖了空 string / whitespace 的语义(`if not raw.strip(): return None`),`_read_config_forgejo_hosts()` 覆盖了空 list 语义(`if not isinstance(hosts, list) or not hosts: return None`)。AC 与代码草图一致。

Minor-1 中 monkeypatch import-time binding 风险已通过架构决策消除(删除 module-level 常量后 env 解析延迟到 function call 时,无需 import-order 担忧),AC §12 明确说明这一点。

**结论**: 4 个 R1 缺失 edge case 均已在 AC + Testing Strategy 中覆盖,达标。

---

### Major-2: Dogfood 缺 env override path — CLOSED

**Verify 结果**: 充分修复。

Rev1 将 dogfood 改为 dual-path formal smoke:

- **(a) Default/Config path**: 利用 Aria 已有 `.aria/config.json` L27-29 显式 `platform_hostnames.forgejo: ["forgejo.10cg.pub"]`,验"verify 已有配置充当 dogfood example"(注明**不**新增,仅 verify)。修正了 R1 指出的 Spec 描述与现状不符问题。
- **(b) Env override path**: `unset ARIA_FORGEJO_HOSTS && python3 scan.py` baseline + `ARIA_FORGEJO_HOSTS=alt.example.com python3 scan.py` + `jq .forgejo_config.instance` 验 `alt.example.com` 替换 → 写入 PR description 作正式 dogfood evidence。

B.3 验收条件明确包含"双 path dogfood"。符合 `feedback_deterministic_structural_skill_rule6_substitute` 要求。

**结论**: env override path 已纳入 formal dogfood smoke,且与 R3 风险行描述一致。

---

### Major-3: C1/C2 env 协调机制歧义 + "config-loader skill API" 误述 — CLOSED

**Verify 结果**: 充分修复。

Rev1 fix 有三处改动:

1. **架构澄清**: 明确 config-loader 是 documentation-only LLM Skill(无 Python 接口),实施改为 inline JSON read + `_common.py` shared helper。

2. **`§B` 措辞**: "在 `_load_config()` 既有 merge 逻辑前面追加 env override layer"(非"删 DEFAULT_CONFIG hardcode")。代码草图保留 `DEFAULT_CONFIG["platform_hostnames"]["forgejo"] = ["forgejo.10cg.pub"]` 不动。

3. **协调机制明确化**: `forgejo_config.py` 调用 `resolve_forgejo_hosts(project_root)`(env→config→fallback 完整三层), `issue_scan._load_config()` 调用 `_parse_env_forgejo_hosts()`(env 层)+ 自身现有 config.json merge(config 层)。两者通过 parity test `test_forgejo_hosts_parity.py` 保证等价。

**结论**: "config-loader skill API" 误导性表述已清除;C1/C2 协调路径已明确;文字不再歧义。

---

### Minor-1: smoke 命令 `--output` flag — CLOSED

**Verify 结果**: 实地核查 `aria/skills/state-scanner/scripts/scan.py` L190,`--output` flag **确实存在**(`argparse.add_argument("--output", ...)`),L226 注释说明与 stdout 互斥。Spec Manual smoke test 命令正确。R1 的担忧不成立,自然关闭。

---

### Minor-2: R4 defer 版本号策略不明确 — CARRY-FORWARD

**Verify 结果**: Rev1 未修改 R4 表述,仍为"defer 到 v1.30.x patch",未补充 "defer 时 version target 改为 v1.29.1"。

L2 Spec 可接受此轻量化表述,不阻塞 Phase B。但版本号歧义保留:若在 block-flip v1.29.0 ship 后 defer,下一个可用 slot 实际是 v1.29.1(patch)还是 v1.30.0(next minor)在 Spec 中未定义。

Phase B 开始前可口头确认,不需要修改 Spec。

---

### Minor-3: structural fixture README 缺 fail-soft 行为规格 — CARRY-FORWARD

**Verify 结果**: Rev1 fixture README 规格写为"3 precedence layer 说明 + 4 处 hardcode 删/改 map + 12 AC behavior 表 + edge case cheatsheet"。"edge case cheatsheet" 措辞暗示应包含 fail-soft 场景,但 Spec 未明确列举 fail-soft 行为(config read error → fallback / 端口号处理)。

注意:代码草图 `_read_config_forgejo_hosts()` 已有 `Fail-soft: missing file / parse error / key absent / non-list value → None` docstring,且 `except (OSError, json.JSONDecodeError): return None` 实现。fail-soft 行为在代码层已 spec'd,仅 fixture README 规格未明确要求文档化。Phase B 实施者若按草图实现则行为正确,但 README 内容规格需 Phase B 时自行补充。不阻塞。

---

## R2 New Findings

### R2-Minor-1: §B `_load_config()` env override 代码草图存在注释与逻辑不一致

**位置**: `proposal.md §B - issue_scan.py env override layer in _load_config()`

**问题**:

§B 实现草图结构如下:

```python
def _load_config(project_root: Path) -> dict[str, Any]:
    # ... existing setup of merged dict + DEFAULT_CONFIG copy ...

    # ---- Rev1 new: env override layer (highest precedence) ----
    env_hosts = _parse_env_forgejo_hosts()
    if env_hosts:
        merged["platform_hostnames"]["forgejo"] = list(env_hosts)
        # Skip config.json merge for forgejo key; env wins
    # ---- end Rev1 new ----

    # ... existing config.json read + merge logic unchanged ...
    return merged
```

注释写 `"Skip config.json merge for forgejo key; env wins"`,但代码草图中:
- env override block 设置了 `merged["platform_hostnames"]["forgejo"]`
- 之后 `# ... existing config.json read + merge logic unchanged ...` 意味着 L112-122 仍运行
- L118-122 现有 merge 逻辑:若 `config.json` 含 `platform_hostnames.forgejo`,会以 `merged["platform_hostnames"][k] = list(v)` 覆盖 env 刚写入的值

即:注释说"env wins",但代码草图没有实现 skip guard,config.json 仍会覆盖 env 值。Phase B 实施者若照搬草图会引入 bug — env override 失效,AC §1 会失败。

**正确实现**应为以下两选一:
- 选项 A(推荐):将 env override block 放置在 config.json read 完成并 merge 后(作 post-merge override):
  ```python
  # ... existing config.json read + merge logic unchanged ...
  # ---- Rev1 new: env override layer (highest precedence, post-merge) ----
  env_hosts = _parse_env_forgejo_hosts()
  if env_hosts:
      merged["platform_hostnames"]["forgejo"] = list(env_hosts)
  # ---- end Rev1 new ----
  return merged
  ```
- 选项 B:在现有 merge loop 中添加 forgejo key 跳过 guard:
  ```python
  for k, v in hostnames.items():
      if k == "forgejo" and env_hosts:  # env already set, skip config override
          continue
      if isinstance(v, list):
          merged["platform_hostnames"][k] = list(v)
  ```

**影响**: 若 Phase B 实施者照搬草图代码,AC §1 `env precedence` test 会失败(env 被 config.json 值覆盖)。选项 A 更简洁且与 `resolve_forgejo_hosts()` 的 3-tier 语义对称(env 永远最高优先级)。

**建议**: Phase B 实施时采用选项 A(post-merge env override),而非 Spec §B 草图的 pre-merge 位置。此问题不阻塞 Spec 审批(实施层 fix 即可),但 implementer 需注意。

---

## 可执行性分析

### 测试设计可执行性

Rev1 新增 8+ unit test 规格分析:

**`test_forgejo_config.py` 扩展(9 个 test)**:
- `test_env_override` / `test_config_override` / `test_default_fallback` / `test_env_beats_config` — 4 条 happy path,覆盖完整
- `test_empty_env_falls_through` / `test_whitespace_env_falls_through` — 2 条 empty env edge case,语义清晰(`_parse_env_forgejo_hosts()` 返回 None 触发 fallthrough)
- `test_empty_config_list_falls_through` — 1 条 config empty list,语义由 AC §7 明确
- `test_duplicate_hosts_tolerated` — 1 条 idempotent 行为,可直接断言 `resolve_forgejo_hosts()` 返回含重复项的 tuple
- `test_custom_host_detection_via_env` — 1 条 C4 fix,与 AC §10 对应

可执行性评估: 所有 9 个 test name 有对应 AC 条目和代码草图,Phase B 可直接实施。

**`test_issue_scan.py` 扩展(3 个 test)**:
- `test_load_config_env_override` — 对应 AC §1,验证 env 覆盖 `_load_config()` 结果(注意 R2-Minor-1,实施需用 post-merge 方式)
- `test_detect_platform_level2_via_env` — 对应 AC §10
- `test_detect_platform_no_level3_forgejo_fallback` — 对应 AC §9,明确验 L198 删除后不 return "forgejo" via Level 3

**`test_forgejo_hosts_parity.py` 新建**:
- 3 fixture × 2 collector → 断言输出 hosts list 完全相等,是可执行的跨 collector 一致性保障

**总体评估**: 共 13 个 test,语义明确,fixture 设计清晰,与 AC 11 的"至少 8 个"要求有余量。Phase B 起手无歧义。

### C4 deliverable E 覆盖评估

- **AC §9**: vanilla install(`_detect_platform("ssh://forgejo@forgejo.10cg.pub/...")`)删 L198 后仍 return `"forgejo"` — 通过 Level 2 platform_hostnames map,由 DEFAULTS.json L45 保障。逻辑链完整。
- **AC §10**: 自定义 host via env,`_detect_platform()` return `"forgejo"` — 此前 L198 不触发 → return None,修后 Level 2 map 触发。逻辑链完整。
- **`test_detect_platform_no_level3_forgejo_fallback`**: 直接测试 L198 deleted 后的行为,确保 custom host 不被 Level 3 fallback 误处理。覆盖充分。

---

## Verdict Summary

**verdict: PASS_WITH_WARNINGS**

### 通过判定

R1 三个 Major 均已实质性修复:

1. **Major-1 CLOSED**: AC 从 5 项扩到 12 项,明确覆盖 empty env / empty list / duplicate / monkeypatch isolation 全部 4 个 R1 缺失 edge case。
2. **Major-2 CLOSED**: Dogfood 改为 dual-path formal smoke,env override path 纳入正式验证步骤并写入 PR description。
3. **Major-3 CLOSED**: "config-loader skill API" 误述完全清除;§B 措辞改为 "在 `_load_config()` 前加 env override layer";`_common.py` 作 shared helper 架构决策清晰。

### Warning 说明(不阻塞)

**R2-Minor-1(新发现)**: §B 代码草图 env override 放在 config.json merge 前,但注释说"Skip config.json merge for forgejo key"没有对应的 skip guard,Phase B 实施若照搬草图会导致 env precedence 失效。建议 Phase B 实施采用 post-merge override 方式(见上文选项 A),AC §1 unit test 会自动捕捉此 bug 如果草图被照搬。

**Minor-2 CARRY-FORWARD**: R4 defer 版本号策略模糊(v1.30.x patch 实际指哪个号),Phase B 前口头确认即可。

**Minor-3 CARRY-FORWARD**: fixture README fail-soft 行为文档化未明确规格,Phase B 实施者可参考代码草图 docstring 补充。

### Phase B 可启动判定

所有 Critical = 0,Major = 0。R2-Minor-1 已标注 warning 并给出正确实现路径,AC §1 unit test 是天然的回归门。Phase B 可安全启动。

---

## 优质设计认可

- **`_common.py` shared helper 架构**: 单一 canonical `resolve_forgejo_hosts(project_root)` 入口 + `_parse_env_forgejo_hosts()` 子函数,清晰分层。
- **空 list 语义决策**: AC §7 明确"空 list = 等价未配置"(不是"禁用 forgejo detection"),避免 footgun,决策有据可查。
- **Parity test 设计**: `test_forgejo_hosts_parity.py` 以可执行测试替代"三处一致"的口头承诺,是高质量的 spec-to-test 映射。
- **C4 删除安全论证**: §E 的 backward compat 论证完整(DEFAULTS.json L45 仍为 vanilla install 保底),why-safe 说明充分。
- **CHANGELOG 防错设计**: v1.29.0 placeholder 预插入策略,防止 block-flip ship 时手动定位失误,思路严谨。

---

**Drafted**: 2026-05-27  
**Round**: R2 (L2 final round)  
**Agent**: qa-engineer

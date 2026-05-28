# DEC: CI backend abstraction brainstorm (2026-05-28)

> **Type**: Brainstorm DEC (technical mode, formal `/aria:brainstorm` triggered)
> **Status**: ✅ **Owner-Approved 2026-05-28** (Q1-Q5 sequential sign-off)
> **Track-ID**: `aria-ci-backend-abstraction`
> **Source**: Sprint 2 boundary audit P0 (C5+C6) per [`.aria/notes/2026-05-27-boundary-audit-10cg-hardcode.md`](../notes/2026-05-27-boundary-audit-10cg-hardcode.md) §修复 2
> **Ship target**: aria-plugin v1.31.0 (v1.29.0 reserved for block-flip, v1.30.0 shipped forgejo-hosts)
> **Implementation estimate**: ~8h Phase B (L3 Spec)

---

## Why (motivation)

Aria 不可协商规则 Rule #8 (`CLAUDE.md`) 强制 PR merge 前跑 `pre-merge gate` 验证 (a) 本 PR CI 已 passing + (b) main 分支无 in-flight CI run。

当前实现 (`aria/skills/phase-c-integrator/scripts/pre_merge_gate.py:47-62`) 硬编码假设唯一 CI primitive 是 **aether-ci-cli** (10CG 自研 CI 平台):

- `DEFAULT_CONFIG["primitive_preference"] = ["aether-ci-cli"]`
- `detect_aether()` 仅探测 `which aether` + `~/.aether/config.yaml`
- 无 fallback 到 GitHub Actions / GitLab CI / Forgejo Actions

Sprint 1 (v1.30.0, 2026-05-27 SHIPPED) 已解 forgejo-hosts hardcode (C1+C2+C3+C4)。Sprint 2 解 CI backend hardcode (C5+C6)。

---

## 5 Decisions snapshot

| # | Question | Selected | Alternative dropped | Why selected |
|---|----------|----------|---------------------|--------------|
| **Q1** | Ship shape | **(b) Contract + Aether full + GHA stub** | (a) 纯重命名 / (c) 全实现 Aether+GHA | 把"抽象层设计"和"GHA 实际实现"拆开,blast radius 小,contract 单独 ship 单独审计 |
| **Q2** | Backward compat | **(b) Soft alias + deprecation warning** | (a) 硬切换 / (c) 完全保留旧名 | 现网调查零项目用旧 key,alias 是纯防御层;v2.0 是天然清理窗口 |
| **Q3** | Auto-detect strategy | **(b) Config-first + probe fallback** | (a) 显式 config 唯一 / (c) Remote URL 推断 | 保护现网"零配置走 Aether"UX;auto-detect 实质就是把现 `detect_aether()` 抽到 backend registry |
| **Q4** | Contract surface | **(b) 双方法 + 数据契约类** | (a) 单方法 `is_branch_busy()` / (c) `dispatch(cmd, **kwargs)` | 1:1 mirror Rule #8 两个独立检查;dataclass 是 substance,catch typo |
| **Q5** | Rule #8 wording span | **(b) 通用化 + Aether 作默认示例** | (a) 最小改动+附录 / (c) 完全去 Aether 化 | 文档与代码 1:1,GHA 真实现时不需再改 Rule #8 文字;现状是 Aether 唯一 production backend, (c) 撒谎 |

---

## 收敛 design 整体逻辑 (5 决策自洽性)

### Q1 stub × Q4 双方法 = 现在只 ship 半套

- Contract `CIBackend` ABC 含 `query_pr_ci()` + `query_branch_in_flight()` 两个 abstract method
- `AetherBackend` 完整实现两者 (从现 `pre_merge_gate.py` 内部逻辑搬迁)
- `GitHubActionsBackend` stub:`probe()` 真实现 (`shutil.which("gh")` + auth check),两个 query 方法 `raise NotImplementedError("GHA backend not implemented; PR welcome")`
- 生产 100% 不受影响 — Aether 仍是唯一可用 backend

### Q2 alias × Q3 auto-detect = 现网零感知升级

- 调查结果 (2026-05-28):Aria 自仓 `.aria/config.json` `phase_c_integrator: {}` 空节;6 sibling aria-using 项目 (Aether/SilkNode/truffle-hound/Kairos/Kino/nexus) **全部**未配 `phase_c_integrator` 节;`grep -rn "no_aether_fallback\|primitive_preference"` 在 sibling 项目 `.json/.yaml/.md` **0 hit**
- 现网 100% 走默认值 — auto-detect probe 序列正确激活 Aether
- Alias path 是死代码,但保留为 forward-compat 护栏 (旧文档 copy-paste 仍 work);unit test 显式 cover

### Q4 契约 × Q5 文字 = 文档代码 1:1

- ABC 两个 abstract method 名字 (`query_pr_ci` / `query_branch_in_flight`) ↔ Rule #8 文字"两个检查 (a)+(b)"语义对位
- 读 Rule #8 = 读 ABC,新人无认知 gap
- `CIStatus` / `InFlightStatus` dataclass 字段在 SKILL.md 表格列出,backend implementer 照表填字段映射即可

---

## Alternatives considered + drop 理由 (per question)

### Q1 ship shape

| 候选 | Drop 理由 |
|------|---------|
| (a) 纯结构化重命名,Aether 仍唯一实现 | 缺示例 contract,外部 contributor 不知道怎么填 GHA — "抽象层"形同虚设 |
| (c) Contract + Aether + GHA 双 full 实现 | 把 contract 设计 + GHA mechanical fill 混在一个 cycle,blast radius 大,审计 surface 也大;ship 之后 GHA 用法分歧无独立讨论窗口 |

### Q2 backward compat

| 候选 | Drop 理由 |
|------|---------|
| (a) 硬切换无 alias | 任何已有项目 config 自动失效→silent 降级 (虽然现网调查零项目实际配,但 v0.x 用户引用旧文档 risk) |
| (c) 完全保留旧名 | 把命名债从今天延到永远;Rule #8 文字反正要重写 (Q5),既然要动就一次到位 |

### Q3 auto-detect strategy

| 候选 | Drop 理由 |
|------|---------|
| (a) 显式 config 唯一 | 破坏现网"零配置走默认 Aether"UX,所有 sibling 项目都得加 config — 违反 Q2 调查"零现网影响"承诺 |
| (c) Remote URL 推断 | Forgejo ≠ Aether 因果关系 (别人可能跑 Forgejo 但用 GHA-style CI);multi-remote 项目歧义;需 Q1 选 (c) 才有价值 |

### Q4 contract surface

| 候选 | Drop 理由 |
|------|---------|
| (a) 单方法 `is_branch_busy()` | 把"PR CI 状态"和"main in-flight"绑死成一个语义;扩展未来场景必须 breaking change |
| (c) `dispatch(cmd, **kwargs)` 命令调度 | Stringly-typed (no type check, no IDE 补全);mock 困难 (dict 字段易 typo);反 ABC 设计精神 |

### Q5 Rule #8 wording

| 候选 | Drop 理由 |
|------|---------|
| (a) 最小改动 + 附录段 | CLAUDE.md Rule #8 文字与新代码语义脱节;读者看 doc 仍以为只支持 Aether;附录段是 documentation 反 pattern |
| (c) 完全去 Aether 化 | 删掉"为什么这套机制本叫 `no_aether_fallback`"历史 context;Aether 是设计源起 + 现行唯一 production backend,完全不提是 misleading |

---

## Deliverables (Phase B 实施)

| # | 文件 / 变更 | 估时 |
|---|------------|------|
| **A** | 新目录 `aria/skills/phase-c-integrator/scripts/ci_backends/`:`__init__.py` (registry) + `base.py` (`CIBackend` ABC + `CIStatus` / `InFlightStatus` dataclass) + `aether.py` (现 `detect_aether()` + ci-status query 逻辑搬迁) + `github_actions.py` (stub) | ~3h |
| **B** | `pre_merge_gate.py` 改用 `resolve_ci_backend(config)` + `backend.query_pr_ci()` / `backend.query_branch_in_flight()`;`_no_aether_output()` → `_no_ci_output()` (alias 旧名) | ~1h |
| **C** | `test_pre_merge_gate.py` rewrite:~10 处 `mock.patch.object(gate, "detect_aether", ...)` → `mock.patch.object(AetherBackend, "probe", ...)` + 新增 GHA stub 行为 test + alias key path test | ~2h |
| **D** | CLAUDE.md Rule #8 L432-444 重写 backend-agnostic;`aria/skills/phase-c-integrator/SKILL.md` ~10 处 + 新增 §C.2.4.X CI Backends 段 + alias deprecation 注释 | ~1h |
| **E** | Rule #6 substitute (deterministic Skill, per memory `feedback_deterministic_structural_skill_rule6_substitute`):structural fixture (mock CIBackend 实现示例) + 27+ unit tests + dual-path dogfood smoke (`AetherBackend.probe()` + `GitHubActionsBackend.probe()` real-machine result) | ~1h |
| **F** | 5+1 SOT v1.31.0 bump (plugin.json + marketplace.json + VERSION + CHANGELOG + README + main repo CLAUDE.md plugin 版本字段) | ~0.5h |

**Total Phase B**: **~8.5h** (与 boundary audit memo 估 "~8-12h L3" 一致,下限)

---

## Hard constraints (Sign-off 后约束)

1. **Aether 行为零变化**:所有现 `test_pre_merge_gate.py` cases 必须 PASS (内部 mock target 改但 assertion 行为不变)
2. **Rule #8 mechanism 不可降级**:文字通用化但"两个检查 (a)+(b)"和 fallback 行为完全保留 — 只通用化 "哪个工具检查",不通用化 "检查什么"
3. **Alias 旧 key 完整工作**:`no_aether_fallback` + `primitive_preference` 仍读取并 emit deprecation warning;unit test 显式 cover
4. **GHA stub `raise NotImplementedError` 必须含可操作 message**:e.g. "GHA backend probe succeeded but query not implemented; PR welcome (see SKILL.md §C.2.4.X)";不允许裸 `pass` 或空 stub
5. **Standards 子模块零触碰**:Rule #8 引用文件 (`issue-triage.md` / `submodule-pointer-hygiene.md` / `session-handoff.md`) 经 grep 验证无 aether-specific 字面,不需改 — 减少跨 repo 协调
6. **不允许把 GHA 真实现塞进本 Spec**:GHA 实现独立为 next cycle (~4-6h L2 Spec, 估 ship target v1.32.0)
7. **Ship slot 严守 v1.31.0**:v1.29.0 reserved for block-flip ship (2026-06-07 hard date),v1.30.0 已 ship forgejo-hosts;不允许提前/延后

---

## Convergence path

**形式**:formal `/aria:brainstorm` skill triggered (technical mode), 单 session sequential 决策 Q1→Q2→Q3→Q4→Q5,每 Q owner 直接 sign-off `"选 b 继续"`(全部选推荐项)。

**Convergence 实质**:
- Q1-Q5 均 unanimous 选 (b) 推荐项,无振荡 (no back-track)
- Q2 中段 owner 注入"确认当前使用 aria 项目的本地 forgejo 项目不会受影响"风险检查 → AI 跑 `grep` 现网调查 → 验证零受影响 → 信心升高
- 类似 [[feedback_post_spec_audit_pragmatic_convergence]] 中 "unanimous + verdict 改善 + 无振荡" pattern (但是 brainstorm 阶段非 audit 阶段)

**Per Q rationale 强度**:每 Q 都有具体 reject 理由 (见 §Alternatives) + 推荐选项 substance defense (现网调查 / 代码量估算 / 跨 file 影响范围),不是"AI 推荐 owner 服从"。

---

## Cross-references

### Source
- Boundary audit: `.aria/notes/2026-05-27-boundary-audit-10cg-hardcode.md` §修复 2 (sketch + code example)
- Predecessor handoff: `docs/handoff/2026-05-27-forgejo-hosts-parameterization-v1.30.0-shipped.md` §6 carry-forward S1 "C5+C6 CI backend abstraction (~8-12h L3 Spec)"
- aria-fleet strategic memo: `.aria/notes/2026-05-27-aria-fleet-three-layer-architecture.md` §4 边界切割规则

### Forward
- Phase A.1 spec-drafter input: 本 DEC + boundary audit memo §修复 2 sketch
- Phase B target files: `pre_merge_gate.py` + 新 `ci_backends/` 目录 + `test_pre_merge_gate.py` + CLAUDE.md + SKILL.md
- Phase C ship target slot: aria-plugin v1.31.0 (between v1.30.0 forgejo-hosts shipped + v1.29.0 block-flip reserved)
- Phase D archive: `openspec/archive/{date}-aria-ci-backend-abstraction/`
- Future related Specs:
  - GHA backend 真实现 (~4-6h L2, ship v1.32.0+) — 实施本 Spec stub
  - GitLab/Forgejo Actions backend (M7+ aria-fleet 主线)
  - GitProvider ABC (aria-fleet long-term, 类似 contract 抽象)

### Memory
- [[feedback_deterministic_structural_skill_rule6_substitute]] — Rule #6 substitute pattern for deterministic Skill
- [[feedback_sub_pr_scope_splitting_pattern]] — 8h scope 不需拆 sub-PR,单 PR full cycle 可
- [[feedback_audit_convergence_patterns]] — 后续 post_spec audit 期待 L3=4-round baseline

---

## Memory candidates (本 brainstorm 产出)

| # | Candidate | Cross-cycle valuable? | Action |
|---|-----------|----------------------|--------|
| 1 | "**Brainstorm 中段 owner 注入风险检查 (Q2 调查现网) 是健康 forcing function**" | ✅ HIGH — pattern 可复用 | 评估扩 existing [[feedback_brainstorm_owner_escalation_discipline]] vs 新增 |
| 2 | "**Stub-vs-full split 是 abstraction layer ship 的标准 pattern**" | ✅ MEDIUM — 适用任何 contract layer ship | 评估新增 `feedback_stub_vs_full_abstraction_layer_ship` |

**触发 memorialize**:Phase D 收尾时评估 (本 brainstorm 不阻塞)

---

**Created**: 2026-05-28
**Status**: ✅ Owner-Approved (Q1-Q5) + ⚠️ R1 audit PASS_WITH_WARNINGS × 3 unanimous (1 Critical + 5 Major + 9 Minor, all "fix in A.1" — see §Audit findings)
**Next step**: Phase A.1 spec-drafter — input = 本 DEC + §Audit findings amendment + boundary audit memo §修复 2

---

## §Audit findings (R1 amendment, 2026-05-28)

### Audit metadata

- **Checkpoint**: post_brainstorm (config `off`, user override to `convergence`)
- **Mode**: convergence
- **Round**: 1 (R2 not run — 3 agent 一致建议 "address in A.1, don't reopen brainstorm")
- **Agents**: aria:tech-lead, aria:backend-architect, aria:qa-engineer (L3 default per audit-engine adaptive rules)
- **Reports**:
  - `.aria/audit-reports/post_brainstorm-R1-2026-05-28T080358-929Z-aria-ci-backend-abstraction-backend-architect.md`
  - `.aria/audit-reports/post_brainstorm-R1-2026-05-28T080401-452Z-aria-ci-backend-abstraction-tech-lead.md`
  - `.aria/audit-reports/post_brainstorm-R1-2026-05-28T080514-474Z-aria-ci-backend-abstraction-qa-engineer.md`
- **Aggregate**: PASS_WITH_WARNINGS × 3 unanimous — no agent voted FAIL despite 1 Critical (因 finding 是 "must fix in A.1" 而非 "must reopen brainstorm")
- **Convergence verdict**: R1 acceptable, R2 skipped per agent unanimous "downstream addressable" 建议 (per [[feedback_audit_convergence_patterns]] "Critical-but-addressable-downstream" pattern)

### Substance convergence (3-agent independent surface of same root)

**Finding M-TEST-REWRITE-UNDERESTIMATE** — 3 agent 独立 surface "Deliverable C 估时 2h 严重不足":
- tech-lead M1: 实测 `tests/test_pre_merge_gate.py` 有 23 `mock.patch.object(gate, "detect_aether", ...)` 行 (DEC 写 "~10",2.3× under)
- backend-architect F-02: `GateCheckTests` 每个 test stack **3 mock targets** — `detect_aether` + `verify_aether_in_flight_flag` + `_query_aether`,全部 collapse 到 `AetherBackend.probe()` / `query_*()` 方法;DEC 仅提 `detect_aether` 一处,漏 2 处
- qa F3: 23 mock + `probe()` 返回类型 (现 `(bool, str|None)` tuple vs 新 ABC `bool`) mock 写法不同 + 新需 ~5 test class (alias × 2 + GHA stub × 2 + backend registry × 3)

→ 三个独立角度命中同一根因 paper-fix-free finding (per [[feedback_brainstorm_substance_convergence_pattern]]),**信号强度 = HIGH**

### Findings 完整列表 (按 severity × fix-target)

#### 🔴 Critical (1) — must address in A.1 AC

| ID | Finding | Source | Fix target in A.1 |
|----|---------|--------|------------------|
| **C-1** | **GHA stub `NotImplementedError` 调用路径未规约** — DEC Hard Constraint #4 只约束 NIE message,未约束 `gate_check()` 遇 NIE 时的路由 (crash vs catch-and-route-to-skip_with_warning)。**安全风险**: 项目装了 `gh` CLI 但实际用 Aether → GHA stub probe() returns True → 注册为 backend → query_*() raises NIE → 若被 skip_with_warning 静默吞掉 → Rule #8 (a)+(b) 检查均不执行,机制 DOWNGRADED | qa F1 | proposal.md §AC 必须含: (1) 伪代码约束 `gate_check()` 遇 NIE 必须 **abort** (raise to caller, 不 catch);(2) Deliverable C 必加 `test_gha_probe_true_query_nie_raises_aborts_not_skips`;(3) 新 Hard Constraint #7: "GHA stub NIE routing = abort, not skip" |

#### 🟡 Major (5) — fix in A.1 design / AC

| ID | Finding | Source | Fix target in A.1 |
|----|---------|--------|------------------|
| **M-1** | **Test rewrite 估时低估 2.3×** (substance convergence × 3 agents) — 23 mocks (非 ~10) + 3 mock targets/test stacked + `probe()` 返回类型 (`bool` vs `(bool, str)` tuple) 决定 mock 写法 + ~5 new test class needed | tech M1 + ba F-02 + qa F3 | tasks.md Deliverable C 估时 **2h → 3-3.5h**;proposal.md §Implementation 列出 collapse 表 (detect_aether + verify_aether_in_flight_flag + _query_aether → which method);AC: `probe() -> bool` 单一返回类型 (不 tuple) |
| **M-2** | **config-loader/SKILL.md L183/L189 文档老 key 但不在 Deliverable D** — DEC §Deliverable D 列了 CLAUDE.md + SKILL.md 但漏 `aria/skills/config-loader/SKILL.md`;post-ship 旧 key 文档继续存在 = doc inconsistency | tech M2 | Deliverable D scope 扩展加 `aria/skills/config-loader/SKILL.md` L183/L189 alias deprecation 注释;估时 +0.25h |
| **M-3** | **Q2 alias × Q3 config-first 交叉处行为未定义** — config 同时含 `no_aether_fallback`(旧)和 `no_ci_fallback`(新)时,DEC 未指定 precedence。Hard constraint #3 仅约束 "alias 旧 key 完整工作",未约束冲突时谁赢 | tech M3 | proposal.md §AC: "old + new key 同时存在 → 新 key wins + emit `both_keys_present` warning";Deliverable C: `test_both_keys_present_new_wins` |
| **M-4** | **Registry discovery 机制未指定** — DEC 提 `ci_backends/__init__.py (registry)` 但 registry pattern (static import list / @register decorator / setuptools entry-point) 未 commit。Phase B implementer 必须 mid-sprint 决定 | ba F-01 | proposal.md §Implementation: "static import list in `ci_backends/__init__.py` (no decorator, no entry-point) — explicit + zero plugin discovery complexity"。新 Hard Constraint #8 锁定 |
| **M-5** | **默认 probe 优先级在 DEC 中丢失** — boundary audit memo §修复 2 草图含 `priority=100` (Aether) / `priority=50` (GHA), 进 DEC 后细节消失。"现网 100% 走 Aether" 的保证依赖 Aether probe 先执行,但 registry import 顺序未被任何约束锁定 | qa F2 | proposal.md §AC: "ci_backends/__init__.py 导入顺序: AetherBackend → GitHubActionsBackend (Aether-first precedence);Deliverable C: `test_aether_takes_precedence_when_both_probe_true`" |

#### 🟢 Minor (9) — annotate in tasks.md, fix in Phase B

| ID | Finding | Source | Fix in |
|----|---------|--------|--------|
| m-1 | CHANGELOG v1.29.0 placeholder vs v1.31.0 entry 顺序 (9-day overlap window) | tech m4 | tasks.md §Phase C: "CHANGELOG v1.31.0 entry 写在 v1.30.0 上方,v1.29.0 placeholder block 不动 (block-flip ship day 时再 replace)" |
| m-2 | ABC `probe()` classmethod vs instance method 语义未定 | tech m5 | proposal.md §Implementation: "`@classmethod def probe(cls) -> bool`" — classmethod, no instance needed |
| m-3 | Rule #8 wording 草稿在 DEC 描述但未 inline — 应在 A.1 出 draft 接受审计 | tech m6 | proposal.md 含 Rule #8 新版完整 markdown draft (~20 行) |
| m-4 | multi-terminal-coordination Layer H frontmatter 在 DEC 未引用 | tech m7 | session 结束时 handoff doc 加 `track-id: aria-ci-backend-abstraction` frontmatter (per Layer H §2.3) |
| m-5 | `CIStatus` / `InFlightStatus` field sets 未列出 — 缺 field 列表 dataclass 等同 dict | ba F-03 | proposal.md §Implementation: dataclass field tables (`CIStatus`: state[Literal]+run_id+url+checked_at;`InFlightStatus`: runs[list]+checked_at) |
| m-6 | Alias translation point 未指定 (before/after `{**DEFAULT_CONFIG, **config}` merge) | ba F-04 | proposal.md §Implementation: dedicated `_normalize_config(config)` step **before** merge — pseudo-code in AC |
| m-7 | `lru_cache(maxsize=1)` on `probe()` = test isolation hazard | ba F-05 | tasks.md Deliverable C: tearDown 加 `AetherBackend.probe.cache_clear()` + `GitHubActionsBackend.probe.cache_clear()`;OR drop lru_cache 改用 module-level `_probe_cache: dict` (test 显式 reset) |
| m-8 | Deliverable E (Rule #6 substitute) 1h 对标 Sprint 1 (forgejo-hosts) 实测显著不足 (Sprint 1 含 27 tests + 12 AC 表 + dual-path smoke 远超 1h) | qa F4 | tasks.md Deliverable E 估时 **1h → 1.5-2h** |
| m-9 | Alias deprecation warning 不在 test 中 assert string content → silent rot risk | qa F5 | Deliverable C: `test_old_key_emits_deprecation_warning_with_expected_message` assertion |

### 估时调整 (汇总 M-1 + m-8)

| Deliverable | DEC 原估 | R1 audit 后修正 |
|-------------|----------|-----------------|
| A — ci_backends/ 抽象 | 3h | 3h (不变) |
| B — pre_merge_gate.py 改造 | 1h | 1h (不变) |
| **C — Test rewrite** | **2h** | **3-3.5h** (+1-1.5h, M-1) |
| **D — Doc 更新** | **1h** | **1.25h** (+0.25h, M-2 加 config-loader SKILL.md) |
| **E — Rule #6 substitute** | **1h** | **1.5-2h** (+0.5-1h, m-8) |
| F — 5+1 SOT bump | 0.5h | 0.5h (不变) |
| **Total Phase B** | **~8.5h** | **~10-10.5h** (仍在 boundary audit memo "8-12h L3" 区间内) |

### 新增 Hard Constraints (R1 audit 触发,A.1 必须 import)

- **#7**: GHA stub `NotImplementedError` routing — `gate_check()` 遇 NIE 必须 **abort** (raise to caller),**不允许** catch-and-route-to-skip_with_warning。Rule #8 mechanism 安全性硬约束 (来源: qa F1)
- **#8**: Backend registry pattern = **static import list** in `ci_backends/__init__.py`,顺序锁定为 `AetherBackend → GitHubActionsBackend` (Aether-first precedence);无 decorator,无 setuptools entry-point (来源: ba F-01 + qa F2)
- **#9**: Old + new config key 同时存在时 → **new key wins** + emit `both_keys_present` warning;alias translation 在 `{**DEFAULT_CONFIG, **config}` merge **之前** 执行 (来源: tech M3 + ba F-04)

### Verified claims (R1 audit 期间验证)

- ✅ **DEC §Hard constraint #5 (standards/ zero-touch)** verified: grep `no_aether_fallback|primitive_preference` in `standards/` returns 0 hits across 3 Rule #8 referenced conventions (per tech-lead R1)
- ✅ **Q1 stub-vs-full split** = correct architectural boundary per [[feedback_sub_pr_scope_splitting_pattern]] (per tech-lead R1)
- ✅ **Q4 ABC contract** enables clean Forgejo Actions / GitLab CI addition (with m-2 classmethod clarification) (per tech-lead R1)

### Memory candidates (R1 audit 反思)

| # | Candidate | Action |
|---|-----------|--------|
| 1 | "**3-agent independent surface of test-rewrite-underestimate = 强 substance convergence signal at brainstorm phase**" | 评估扩 [[feedback_brainstorm_substance_convergence_pattern]] (add brainstorm-phase audit case;现 entry 是 spec-phase audit) |
| 2 | "**Critical-but-addressable-downstream convergence pattern** — agents 一致建议 'don't reopen brainstorm, fix in A.1' 是合理 R2-skip 信号"  | 评估扩 [[feedback_audit_convergence_patterns]] 加此 pattern |

**触发 memorialize**: Phase D 收尾时统一评估 (不阻塞当前 cycle)

---

**R1 audit closed**: 2026-05-28T08:15Z
**Phase A.1 input**: 本 DEC (含 §Audit findings) + boundary audit memo §修复 2 + 3 audit reports raw

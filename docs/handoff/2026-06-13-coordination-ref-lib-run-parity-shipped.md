---
track-id: coordination-ref-lib-run-parity
owner-container: simonfishgit/dev-claude
phase: D-closed
status: done
updated-at: 2026-06-13T12:00:00Z
---

# Aria — Session Handoff (2026-06-13 #3) — coordination-ref-lib-run-parity (F1) ship v1.46.3

> **Status**: ✅ **DONE**。F1 (lib/coordination_ref.py 平行 _run 加固 + benign-absent) Level 2 收口: owner "修 F1" → 验证诊断 (两分叉 _run) → owner 选 "修 a+b" → Spec (post_spec R1 2/3 REVISE → R2 3/3 PASS) → 实施 → code-review PASS → **v1.46.3** (aria PR [#85](https://forgejo.10cg.pub/10CG/aria-plugin/pulls/85) merge `0ccf42e` + release `82e0e75`; 主仓 gitlink 本 commit)。Spec 归档; F1 无 issue。
> **🏁 #141 review 派生 F1-F5 全收口**: F1 fixed (v1.46.3) / F2 仍 open (低优) / F3=#142 wont-fix / F4=#143 fixed (v1.46.1) / F5=#144 fixed (v1.46.2)。
> **Rule #9 trigger**: 同日第 3 ship + 跨 A/B/C/D。

---

## §0 入口 (新 session 优先读)

1. **本 doc** + 同日前序 (`2026-06-13-track-board-coordination-stale-bar-shipped.md` v1.46.2 / `-git-stderr-locale-hardening` v1.46.1 / `2026-06-12-...coordination-fetch-resilience` v1.46.0)。
2. ✅ **F1 fix**: `lib/coordination_ref.py` 有**自己的 `_run`** (独立于 collectors/_common._run); #61 (UTF-8 crash-safe) + #143 (LC_ALL=C) 只改了 collector 那个。本地 _run 加 `encoding=utf-8/errors=replace` + env `{**environ, **(extra_env or {}), "LC_ALL":"C"}` (LC_ALL 末位非覆盖); `fetch_coordination_ref` 加 benign-absent 三重 AND 闸 (镜像 collector, 复制非 import 防 layering)。**只加 #61/#143**; timeout/None-guard 留 **F2**。
3. **可达性低** (调用链 phase1_gate **opt-in 默认关**) 但真实潜在崩溃 (C-locale + 非 ASCII claim → UnicodeDecodeError) /locale 隐患。
4. **owner-gated 残留** (本 session 未碰): block-flip 重启 / M6 Spec #2 e2e-resilience 168h / #136 Feishu secret 轮换 / i18n README #140。**AI follow-up 剩 F2** (lib _run 与 collector 完全 parity: timeout/None-guard/UnicodeDecodeError→125/FileNotFoundError rc 统一 + 考虑提取共享差异表防再次单边漂移; 低优, 未开 issue)。

→ **next session 入口**: `/aria:state-scanner`。

## §1 已完成 (本 ship)

| # | 项 | 产物 |
|---|----|------|
| 1 | 诊断验证 | lib 平行 _run 缺 #61/#143 (真实崩溃/locale 隐患); fetch_coordination_ref 无 benign-absent; 可达性低 (opt-in gate) |
| 2 | Spec + post_spec | Level 2; R1 2/3 REVISE 3 major (全为"测试落点太松允许 mock 绕过真 code path") → Rev1 强制 TG-C lib-直测 → **R2 3/3 PASS** |
| 3 | 实施 | TG-A 本地 _run #61+#143 + TG-B benign-absent + TG-C 7 lib-直测 (主 loop 亲自) |
| 4 | code-review | aria:code-reviewer **PASS** (env merge / benign 闸 / health_check trace / layering 经源码+实地 git 复现验证) |
| 5 | 测试 | 7 lib-直测 (env host-locale-agnostic + extra_env 共存 + benign/converse/wrong-ref/auth + crash-safe); 97 coordination 测试 + 818 全绿 (1 已知 flake 无关) |
| 6 | ship | aria PR #85 merge `0ccf42e` + release `82e0e75` 双远程; 5 SOT v1.46.3; 主仓 gitlink 82e0e75; Spec 归档 |

## §2 未完成 / Carry-forward

owner 四项不变 (§0.4)。**AI follow-up 剩 F2** (lib/collector _run 完全 parity, 低优未开 issue)。**F1/F3/F4/F5 已全收口** —— #141 silent-failure-hunter 派生的 follow-up 仅剩 F2。

## §3 关键陷阱 (本 cycle 实证)

1. **分叉实现致单边加固漂移** (本 cycle 根因): 同一职责两个 `_run` (collectors/_common + lib/coordination_ref), #61/#143 只打了一个 → 另一个潜伏旧崩溃。code-review 建议 F2 时提取共享差异表防再漂。**新副本 = 加固债**。
2. **测试落点必须打真实被改 code path** (R1 3 major, 复用 #143 memory): 现有 test_failure_injection mock 掉 fetch_coordination_ref wholesale → 改它的 code 测试照绿。强制 TG-C lib-直测 (env 断言 patch lib 的 subprocess + benign 真打 fetch_coordination_ref 仅 mock 内部 _run) 才可证伪 (per [[feedback_noop_in_test_env_hardening_needs_mechanism_assertion]])。
3. **layering: lib 不可 import collectors** (backend-arch): lib 低于 collectors (collectors import lib), 反向 import = 循环。benign 三重 AND 复制 3 行 + 注释互引, 非复用。

## §4-§5 memory / 同步状态

**无新建 memory** (本 cycle 复用 [[feedback_noop_in_test_env_hardening_needs_mechanism_assertion]] [测试机制断言] + [[feedback_rebenchmark_test_diagnosis_not_metric]] [验诊断] + [[feedback_adversarial_finding_severity_by_deployment_reachability]] [可达性裁断])。§3.1 分叉加固漂移是新观察但偏具体, 暂不单列 memory。Spec 归档 `2026-06-13-coordination-ref-lib-run-parity`; F1 无 issue/US 关联; CLAUDE.md/主仓 VERSION 本 commit 同步 v1.46.3。

## §6 Next session 入口

`/aria:state-scanner`。优先级: owner 四项 > AI 可做 (F2 低优)。

## §7 提交清单

| 仓 | HEAD | parity |
|----|------|--------|
| aria-plugin | `82e0e75` (PR #85 merge `0ccf42e` + release; 分支已删) | ✓ origin+github |
| 主仓 | 本 commit (gitlink 82e0e75 + 归档 + handoff + CLAUDE.md/VERSION) | push 后 ✓ |

> C.2.4 gate: aria-plugin 无 CI → skip_with_warning (Rule #8)。

## Cross-references
- 归档 Spec: `openspec/archive/2026-06-13-coordination-ref-lib-run-parity/`
- 审计报告: `.aria/audit-reports/post_spec-R2-2026-06-13-coordination-ref-lib-run-parity.md`
- 代码: `lib/coordination_ref.py` (`_run` + `fetch_coordination_ref`) + `tests/test_coordination_ref_lib.py` (7 tests)
- F1 来源: #141 code-review silent-failure-hunter M2 (无独立 issue)

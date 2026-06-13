---
checkpoint: post_spec
mode: convergence
change_id: coordination-ref-lib-run-parity
rounds: 2
converged: true
verdict: PASS
oscillation: false
agent: audit-engine-consolidated
team_size: 3
timestamp: 2026-06-13
---

# post_spec convergence audit — coordination-ref-lib-run-parity

> **Verdict**: ✅ **PASS** (converged R2, unanimous 3/3, 0 critical / 0 major)
> **Trajectory**: R1 REVISE (2/3, 3 major) → Rev1 → R2 PASS (3/3)
> **Team** (3 lens): backend-architect / code-reviewer / qa-engineer
> **Scope**: F1 收口 — lib/coordination_ref.py 平行 _run 加 #61+#143 + fetch_coordination_ref benign-absent。v1.46.3 PATCH。

## Convergence summary

| Round | backend-arch | code-reviewer | qa-engineer | 聚合 |
|-------|-------------|---------------|-------------|------|
| R1 | PASS (0/0/2) | REVISE (0/1/4) | REVISE (0/2/2) | **REVISE** (3 major) |
| R2 | PASS (0/0/0) | PASS (0/0/1) | PASS (0/0/0) | **PASS** (0 major) |

unanimous_pass=True (3/3) + verdict 改善 + 无振荡。实质收敛 (R2 对真代码核验: collector _run 有 timeout/None-guard 而 lib 缺 → scope 收窄准确; lib L233 inline import os; benign stderr 本地复现; patch target lib.coordination_ref.subprocess.run 有效; health_check trace 经 test_ref_newly_appeared 实证)。

## R1 major findings (3, 全收敛于"测试落点太松") → Rev1 处置

| # | Lens | Finding | Rev1 处置 |
|---|------|---------|----------|
| M1 | code-reviewer | 测试落点 "或新增" 允许加 mock 路径绕过真 code path (现有 test_failure_injection mock fetch_coordination_ref wholesale) | → **TG-C 强制 lib-直测** (非 mock wholesale) |
| M2 | qa | lib._run env 断言缺失 (collector 的 env 测试不覆盖 lib 独立 _run; C-locale CI no-op 循环论证, 同 #143 教训) | → TG-C **C1** env 断言 patch lib.coordination_ref.subprocess.run, host-locale-agnostic + extra_env 路径 |
| M3 | qa | benign-absent 路径零直测 (mock fetch_coordination_ref wholesale → 新分类分支零覆盖) | → TG-C **C2** 真打 fetch_coordination_ref (仅 mock 内部 _run 返回 rc/stderr): benign + converse + 别 ref 名防绕闸 |

## minor (全收, Rev1)
- (backend-arch) GIT_INDEX_FILE merge 安全 + benign 用 lib REF_NAME → env merge 改 **LC_ALL=C 末位非覆盖** `{**environ, **(extra_env or {}), "LC_ALL":"C"}`。
- (code-reviewer m3) "对齐" over-claim: collector _run 有 timeout/None-guard 而 lib 缺 → 收窄"只加 #61/#143, timeout/None-guard 属 F2-class"。
- (code-reviewer m5) 保留 inline `import os as _os_run` (L233) 防 NameError。
- (m2/qa) benign ref_updated=False 双义 ("无 ref 可更新" vs "ref 未变") → docstring 注明; health_check trace 锁定 (success→不标 partial_fetch; sha_before="" 短路 regression)。
- C3 crash-safe 加入 (#61 落到 lib _run); 全 coordination 回归 C4。

## R2 residual minor (1, 已折入 tasks)
- (code-reviewer) C3 坏字节注入机制 → tasks 补 `sys.executable -c "...buffer.write(b'\xff...')"` (同 test_common.py:65-83, 打真实解码路径非 mock)。

## 关键决策
- **layering**: lib **不** import collectors/_common._run (lib 低于 collectors) → 平行加固 + 注释互引; benign 三重 AND 复制 3 行 (非复用)。
- **scope 诚实**: 只加 #61/#143; timeout/None-guard = F2-class (collector _run 有, lib 缺, 不在本 Spec 声称 parity)。

## 结论
Spec **Approved**, ready for Phase B.1。3 个 lib-直测 (C1 env / C2 benign 真路径 / C3 crash-safe) 打真实被改 code path, 闭合 R1 测试-绕过 gap。

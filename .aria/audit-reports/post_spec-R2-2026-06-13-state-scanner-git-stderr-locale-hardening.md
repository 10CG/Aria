---
checkpoint: post_spec
mode: convergence
change_id: state-scanner-git-stderr-locale-hardening
rounds: 2
converged: true
verdict: PASS
oscillation: false
agent: audit-engine-consolidated
team_size: 4
timestamp: 2026-06-13
---

# post_spec convergence audit — state-scanner-git-stderr-locale-hardening

> **Verdict**: ✅ **PASS** (converged R2, unanimous 4/4, 0 critical / 0 major)
> **Trajectory**: R1 REVISE (2/4, 3 major) → Rev1 全落地 → R2 PASS (4/4)
> **Team** (4 lens): backend-architect / code-reviewer / qa-engineer / tech-lead
> **Scope**: 合并 #142(F3 wont-fix)+#143(F4 fixed); `_run` 注入 LC_ALL=C; v1.46.1 PATCH。

## Convergence summary

| Round | backend-arch | code-reviewer | qa-engineer | tech-lead | 聚合 |
|-------|-------------|---------------|-------------|-----------|------|
| R1 | PASS (0/0/2) | PASS (0/0/4) | REVISE (0/2/1) | REVISE (0/1/3) | **REVISE** (3 major) |
| R2 | PASS (0/0/0) | PASS (0/0/1) | PASS (0/0/1) | PASS (0/0/0) | **PASS** (0 major) |

unanimous_pass=True (4/4) + verdict 改善 + 无振荡。实质收敛 (R2 agents 对真代码核验: ls-remote rc=2 absent=hidden / git.py:181 --oneline / custom_checks:320 独立 subprocess / coordination_fetch L124-134 已有 auth-masked 限制注记 / os L17 已 import)。

## R1 major findings (3, verified-real) → Rev1 处置

| # | Lens | Finding | Rev1 处置 |
|---|------|---------|----------|
| M1 | tech-lead | #142 收口 conflate: LC_ALL=C 不解决 #142 auth-masked silent (git 不可解), 不能 imply "本 Spec 修复 #142" | → #142 改 **wont-fix** (非 fixed); §Why + §#142 收口 + Out-of-scope + tasks W1 四处一致区分 #142(wont-fix)/#143(fixed); 诚实四点 comment |
| M2 | qa | "803 绿"在 C-locale CI 对 LC_ALL=C 注入有效性循环论证 | → TG-B 加 env 断言测试 (mock subprocess.run 捕获 env kwarg, superset 比较, host-locale-agnostic 可证伪) |
| M3 | qa | CJK 测试声称 `--format=%s` 但实际 git.py:181 用 `--oneline` + "实测固化"措辞超前 | → 改 `--oneline` (实际路径, 实测字节直通确认) + 措辞修正 |

## 锁定的 OQ (Rev1)
- OQ1 版本 → **PATCH v1.46.1** (锁定既有英文假设, 无新字段/能力/exit-code; 对比 #141 加 field=MINOR)。
- OQ2 LANG=C → **drop, 只 LC_ALL=C** (折叠所有 LC_* 含 LC_MESSAGES, LANG 冗余; backend-arch 实证)。
- OQ3 ls-remote → **decline + #142 wont-fix** (git 不可解 absent-vs-hidden + 成本)。

## R2 residual minor (2, 同一点, 已折入)
- (code-reviewer + qa) 验证命令 `python3 -m unittest discover` 缺 sys.path 得 717+4 import-err 假基线; canonical runner `python3 tests/run_tests.py` 才得 803 → TG-B/B4 已改用 runner。

## R2 实质收敛证据 (真代码核验)
- ls-remote 实测 absent ref = rc=2 (与 hidden 同) → #142 "git 协议不可解" 坐实非 hand-waving (tech-lead)。
- coordination_fetch.py L124-134 docstring **已存在** auth-masked 限制记录 → "#142 已 documented-limitation" 坐实 (tech-lead)。
- LC_ALL=C 折叠 LC_MESSAGES (POSIX) → drop LANG=C 充分 (backend-arch)。
- env 注入 `{**os.environ, "LC_ALL":"C"}` 不 mutate os.environ, 保留 PATH/HOME; custom_checks:320 独立 shell subprocess 排除正确 (code-reviewer)。

## 结论
Spec **Approved**, ready for Phase B.1。仅修复 #143 (LC_ALL=C); #142 wont-fix 收口 (无代码)。实施按 canonical runner 验证 + 真实 `--oneline` CJK 测试。

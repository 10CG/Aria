---
checkpoint: post_release
spec: state-scanner-mechanical-enforcement
task_group: T10 (release closeout)
timestamp: 2026-04-25T00:30Z
verdict: RELEASED
plugin_version: v1.17.0
spec_status: Approved (T8 + T6.5-followup deferred post-release)
---

# Post-Release: aria-plugin v1.17.0 — state-scanner v3.0.0

## Release artifacts
| Repo | Commit |
|------|--------|
| aria-plugin | 4f91461 (merge of PR #27) |
| Aria | (this commit, submodule bump 1a875d5 → 4f91461 + tasks.md T9.3+T10 done + benchmark) |

## Quality Gates Final Tally
| Gate | Result |
|------|--------|
| T6 stdlib unittest | 215/215 (1.6s) |
| T7 stability dogfood | DIFF_EXIT=0 |
| Smoke benchmark v1.17.0 | 35/35 (100%) |
| Audit reports | 8 (T1-T9, all converged) |
| 4-remote parity | ✅ all 9 partial-merge cycles |

## Spec Tasks Final Status
- Done (39): T0+G+T1.1-T2.5+T3.1-T3.6+T4.1+T4.3+T5.1-T5.6+T6.1-T6.6+T7.0-T7.2+T9.1-T9.3+T10.1-T10.3
- Deferred (5): T6.5-followup (subprocess mocking) + T8.1-T8.2 (Kairos cross-project) + Full /skill-creator AB

## Spec archive decision
**NOT archived** — T8 + T6.5-followup 仍在 backlog, archive 后置 (per OpenSpec convention: Spec archive 要求所有 tasks done, 包括 deferred 项目, 即便不阻塞 release).

## v1.18.0 准备
- 需观察 v1.17.x cycle `mechanical_mode=false` 使用量, 零告警 = 安全移除
- AD-SSME-5 计划: v1.18.0 移除 opt-out flag (CHANGELOG/SKILL.md/migration doc 已显式 schedule)

## Verdict
**RELEASED** — aria-plugin v1.17.0 packaging 完成, Spec 主体 done, deferred 项目独立 backlog 跟踪.

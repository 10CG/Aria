---
checkpoint: pre_merge
mode: convergence
rounds: 1
converged: false
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-02T14:41:58Z
context: PR #190 linked-issue-field-availability (main 0e9619c / aria fe32441 / standards fad8b4b @ R1)
agents: [code-reviewer, qa-engineer, tech-lead, knowledge-manager]
---

# Pre-merge 收敛审计 — PR #190 `linked-issue-field-availability` — Round 1 聚合

> **engine**: audit-engine convergence (owner 2026-09-02 显式调用; config `pre_merge: off` 故非自动触发, Rule #10 无豁免), max_rounds=5
> **team**: aria:code-reviewer + aria:qa-engineer + aria:tech-lead + aria:knowledge-manager (fresh subagent ×4, 独立写报告后主控机械汇总)
> **completeness gate (Issue #26)**: post_spec 469 / post_planning 155 份报告在案 (同族 47 / 24) ⇒ PASS
> **R1 verdict**: **PASS_WITH_WARNINGS** — Critical 0 / Major 4 / Minor 8 (去重前 16 → 去重后 12); 投票 4/4 PASS (无「必须合并前修」项); **R1 不可收敛** (需 R2 稳定性比较)

## Anchor (Step 0, 审计周期内不可变; source_sha main 0e9619c / aria fe32441 / standards fad8b4b)

- **primary_goal**: 「proposal.md 头部『Linked Issue』字段可得且可抽取」— E0–E6 纯函数 + 机械 check (plugin 分发面探针 + 仓本地白名单) + 写入侧模板义务 (SOT 模板 + spec-drafter), 使母 Spec `--linked-issue` 主机制有合规输入; ship aria-plugin v1.68.0 (MINOR)。
- **in_scope**: 三仓 diff 全部文件。**out_of_scope**: 母/探针 Spec 内容 (只审接缝) / M6-M7 回填 (O-1 已裁) / proposal 理据勘正 (B3) / AB iteration-2 / aria-orchestrator / 推送操作本身。
- drift-checker 未独立 spawn (`drift_check_skipped`, convergence 模式默认不开 #17 drift guard); 四席 prompt 内嵌 anchor + 已裁项清单。

## 结论 (去重后 12 条, 四元组 = type/severity/category/scope)

| id | severity | category | scope | type | found_by | R1 清账处置 |
|---|---|---|---|---|---|---|
| `e4cde200` | major | testing | `aria/skills/state-scanner/tests/test_linked_issue_field.py` | issue | qa-engineer | **已修** aria v1.68.1 `d1caa66`: SC-5(d) 夹具复制完整 lib/ 只删 collision.py + 断言 ImportError 点名 lib.collision |
| `a3bfd693` | major | documentation | `docs/handoff/2026-09-02-linked-issue-field-b2-implemented-awaiting-push-auth.md` | issue | knowledge-manager, tech-lead | **已修** 本 commit: handoff frontmatter phase/updated-at 刷新; 「落后 1」→ 实为 2, 已 merge origin/master (29c1e4f) 入 feature |
| `9ac5533a` | major | documentation | `aria/skills/spec-drafter/SKILL.md` | risk | tech-lead | **裁定 B8** (决策单): 顺序条款 = 写入侧模板对齐建议, 机械 check 位置无关 (D2) 是设计; 主仓侧白名单头注 + fix 文案补位置说明; SKILL.md 措辞软化延后 (处方性改动须 Rule #6 照跑, 不在 pre_merge 循环内做, carry-forward) |
| `ac44ace3` | major | documentation | `docs/architecture/system-architecture.md` | risk | tech-lead | **已修 + 类级兜底** 本 commit: system-architecture.md §2.8 / version-scheme.md 两行 → 1.68.1; CLAUDE.md 发布同步面加这两点; 新 state-check `plugin-version-arch-docs-match` (三态实测: 错配 DRIFT rc=1 / 一致 OK) |
| `ae4f1c9f` | minor | implementation | `aria/skills/state-scanner/scripts/linked_issue_field_probe.py` | issue | code-reviewer | **已修** aria v1.68.1: 白名单归一 (尾斜杠 / ./ / 去重) 统一两处; archive 判定不用 glob; root 与 --emit-arg 互斥 exit 2 |
| `2ed89c8a` | minor | architecture | `aria/skills/state-scanner/scripts/linked_issue_field_probe.py` | risk | code-reviewer | **已修** aria v1.68.1: `sys.stdout.reconfigure(errors="replace")`, PYTHONIOENCODING=ascii 实测 exit 0 |
| `a0ff4897` | minor | documentation | `aria/skills/state-scanner/scripts/linked_issue_field_probe.py` | issue | code-reviewer | **已修** aria v1.68.1: 注释去 CONTRACT 引用 (probe + test), `is_sentinel` 导入注释改为真实用途 |
| `4605dc4d` | minor | documentation | `standards/openspec/templates/proposal-minimal.md` | issue | code-reviewer | **已修** standards `ffed204`: 模板 Usage Note 英文化, 删 alias 提及 (TASK-013 字面对齐); 测试 SC-6 (iii) 接受中英任一 |
| `6cdc6077` | minor | testing | `aria/skills/state-scanner/tests/test_collision.py` | risk | qa-engineer | **记入口径注** (CHANGELOG 1.68.1 / SUBSTITUTE.md / RESULT.md §4): Ran 1457 vs 静态 1473 差 16 = test_collision.py 16 个 pytest 风格裸函数不被 unittest 收集 (既有); 修法 carry (决策单 C3) |
| `46b1df1a` | minor | testing | `aria-plugin-benchmarks/ab-results/2026-09-02-v1.68.0-linked-issue-field-rule6/PREDICTION.md` | risk | qa-engineer | **接受为方法论留痕** (无更强时序证据可造): PREDICTION 内容与 RESULT 可证伪分支逐字吻合是唯一可核验面; 未来可在跑前把 PREDICTION 单独 commit |
| `5333fe78` | minor | architecture | `.forgejo/workflows/issue-triage-tests.yml` | risk | tech-lead | **carry-forward** (决策单 C1): issue-triage workflow paths 对 gitlink bump 结构上不触发, 非本 PR 引入; Level 1 CI 配置 change |
| `6ab01600` | minor | architecture | `refs/aria/coordination` | risk | tech-lead | **carry-forward** (决策单 C2): 3 条 a1-entry 轨 active claim, D.2b 归档时按两种 track_id 串各 release + --sweep-stale; 探针 Spec B.1 认领前先做 |

## Verdict

PASS_WITH_WARNINGS — 0 Critical / 4 Major / 8 Minor。四席一致投 PASS (Major 皆非阻塞合并; 但主控按「能修的修、修不了的裁」全部处置, 见上表)。

## 轮次记录

### Round 1
- Agents: 4/4 (code-reviewer PASS 0C/0M/6m · qa-engineer PASS_WITH_WARNINGS 0C/1M/2m · tech-lead PASS_WITH_WARNINGS 0C/2M/3m · knowledge-manager PASS_WITH_WARNINGS 0C/1M/1m)
- Conclusions: 12 (raw 16)
- Vote: 4/4 PASS
- 清账落点: aria **v1.68.1** `d1caa66` (+tag, 双推核验) · standards `ffed204` (双推核验) · 主仓 feature 本 commit (arch 两行 / CLAUDE.md 同步面 / 新 check / 白名单与 fix 文案 / handoff / 决策单 B8-B9 + C1-C3 / RESULT·SUBSTITUTE 注 / gitlink ×2 / 14 点 → 1.68.1)
- R2 = 四席 fresh 重审清账后状态; 收敛判据 = 四元组集合 R2 == R1' (清账后预期集合) 且四票 PASS; 若 R2 仍有变动则 R3 稳定性确认

## 统计

| 指标 | 值 |
|------|-----|
| 总轮次 (至此) | 1 |
| Agent 参与率 | 4/4 |
| 去重前/后 issues | 16/12 |
| 收敛轮次 | N/A (进行中) |

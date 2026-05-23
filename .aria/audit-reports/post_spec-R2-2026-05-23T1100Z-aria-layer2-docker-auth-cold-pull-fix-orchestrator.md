# post_spec R2 audit report — aria-layer2-docker-auth-cold-pull-fix

> **Date**: 2026-05-23 ~10:30-11:00 UTC
> **Spec**: `openspec/changes/aria-layer2-docker-auth-cold-pull-fix/proposal.md` (Draft v2 / Rev1)
> **DEC**: `.aria/decisions/2026-05-23-layer2-docker-auth-cold-pull-fix.md`
> **R1 report**: `.aria/audit-reports/post_spec-R1-2026-05-23T0900Z-aria-layer2-docker-auth-cold-pull-fix-orchestrator.md`
> **Mode**: 4-agent parallel verify (tech-lead / backend-architect / qa-engineer / knowledge-manager)
> **Orchestrator**: Claude Opus 4.7 (1M context), solo-lab session

---

## §1 Verdict matrix

| Agent | Verdict | R1 ADDR | PARTIAL | OPEN | NEW C | NEW I | NEW M |
|-------|---------|---------|---------|------|-------|-------|-------|
| tech-lead | PASS_WITH_WARNINGS | 7/7 | 2 | 0 | 0 | 1 | 2 |
| backend-architect | PASS_WITH_WARNINGS | 8/8 | 0 | 0 | 0 | 1 | 2 |
| qa-engineer | PASS_WITH_WARNINGS | 6/8 | 2 | 0 | 0 | 2 | 2 |
| knowledge-manager | PASS_WITH_WARNINGS | 8/9 | 1 | 0 | 0 | 0 | 3 |
| **聚合** | **4/4 PASS_WITH_WARNINGS** | **27/32** | **5** | **0** | **0** | **4 (2 cross-cut)** | **9** |

---

## §2 Convergence judgment

Per `[[feedback_audit_r2_collapse_default_vs_owner_invoked]]` (default-collapse criteria):

| Criterion | Required | Actual | Status |
|-----------|----------|--------|--------|
| R1 Critical 100% addressed | yes | 4/4 | ✅ |
| R1 Important ≥70% addressed | yes | 75-100% per agent | ✅ |
| 0 NEW Critical | yes | 0 | ✅ |
| Unanimity (PASS_WITH_WARNINGS) | yes | 4/4 | ✅ |

→ **R2 收敛**, 默认 collapse R3+R4 进 A.3 合规。**但 2 个 cross-cutting NEW Important 必须 Rev2-micro 修后才进 A.2** (per `[[feedback_paper_fix_antipattern]]` — NEW findings 不能当 advisory)。

---

## §3 NEW findings — cross-cutting (必须 Rev2-micro 修)

### M-cross-N-I-1 (B2 PAT leak in remote process table) — 3/4 agent 共识

- **R1 IDs**: M-tl-N-I-1 + M-ba-N-1 + M-qa-N-2
- **Issue**: 验收 B2 命令 `ssh heavy-N "curl -sI -u aria-runner-bot:\$(python3 -c \"...decode...\") ..."` 把 PAT 字面值 inline 到 curl `-u` 参数。在 ssh remote shell 内执行时:
  - 60s 窗口内 `ps aux` on remote 可见 `curl -u aria-runner-bot:<actual-PAT>` 完整字面值
  - remote `/root/.bash_history` 留痕
  - 若 owner 本地 ssh session log 截图,PAT 漂出
- **违反**: Spec 自己 §Risks R3 (声称 "PAT 不漂入 chat" + "ssh remote shell 内 expand 不通过 stdout") + Rule #7 + `[[feedback_secrets_never_in_conversation]]`
- **Rev2 fix**: 改用 `--password-stdin` pipe 模式 — PAT 走 stdin 不进 command arg

### M-cross-N-I-2 (C2 alloc 节点归属不验证) — 2/4 agent 共识

- **R1 IDs**: M-ba-N-2 + M-qa-N-1
- **Issue**: `nomad job dispatch -meta TARGET_NODE=heavy-N aria-layer2-runner` 依赖 HCL constraint 读 `${NOMAD_META_TARGET_NODE}`。若 HCL 无该 constraint, dispatch 落任意节点 — silent-pass 风险 (3 次 dispatch 可能全落同一节点,但 C 验收声称"3 节点各 1 次")
- **Rev2 fix**: C2 后加 C2.5 `nomad alloc status <id> | grep 'Node Name'` 强制验证 alloc 真落到目标节点

---

## §4 NEW findings — non-cross-cutting (Rev2-micro 顺带 + A.2 tasks.md 自然解决)

### Rev2-micro 顺带 (3-5 行 edits)

- **M-km-N-1**: DEC frontmatter Status 仍 "Draft v1", 未跟进 Rev1 → 2 行 fix (frontmatter + Status changes 段)
- **M-qa-N-3**: A1/A2 regex 不一致 → 统一为 `'^\s*auth\s*\{'`
- **M-qa-N-4**: D 缺责任归属 label → 加 "AI segment self-verify (after commit, before PR)" 标
- **M-tl-N-M-2**: M6 dependency 应在 DEC §6 References → 加 1 行 "M6 entry blocked-by: 本 Spec done"
- **M-km-N-3**: 验收 D1 `[ -f ] && grep` 复合歧义 → 拆 2 步
- **M-ba-N-3**: B2 `| head -1` 对 HTTP/2 100 不健壮 → 改 `-w "%{http_code}"`

### A.2 tasks.md 自然解决 (不在 proposal-level)

- **M-tl-N-M-1**: T1.0 probe 输出归档 `.aria/probes/2026-05-23-aria-runner-template-status.md`
- **M-km-N-2**: memory plan MEMORY.md 索引格式模板 (Phase D.3 任务说明里写明)

---

## §5 R1 PARTIAL items 评估 (5 项)

| Item | Agent | Status | 行动 |
|------|-------|--------|------|
| M-tl-I-4 | tech-lead | PARTIAL (C2 具体化) | A.2 tasks.md 拆 C2 子任务 (constraint propagation + force_pull patch);**不阻 R2 collapse** |
| M-tl-M-2 | tech-lead | PARTIAL (commit msg template 已加但 DEC §6 缺 M6 blocker 行) | M-tl-N-M-2 sweep 时一并解决 |
| M-qa-M-1 | qa-engineer | PARTIAL (D 责任归属) | Rev2-micro fix (M-qa-N-4) |
| M-qa-M-2 | qa-engineer | PARTIAL (dispatch-issue.sh follow-up issue 无 enforcement) | A.2 tasks.md T1.0 任务里 explicit "open Forgejo follow-up issue" |
| M-km-M-1 | knowledge-manager | PARTIAL (顺带 hygiene 索引补全 — owner-decide) | owner-pending, 非阻塞 |

---

## §6 Rev2-micro sweep 计划

5 个 surgical edits, 预计 ~10min:

1. **proposal.md §Acceptance B2**: PAT 进 stdin 不进 process args (3-agent 共识)
2. **proposal.md §Acceptance C**: 加 C2.5 alloc node verify (2-agent 共识)
3. **proposal.md §Acceptance A2 regex**: 统一为 `'^\s*auth\s*\{'`
4. **proposal.md §Acceptance D**: 加责任归属 label + D1 拆 2 步 + B2 `head -1` → `-w "%{http_code}"`
5. **DEC frontmatter + §6 References + §8 Status changes**: Status → "Draft v2 / Rev1" + 加 M6 blocker 行 + Status changes 行

完成后 Spec 进入 "Approved (Rev1.1, R2 closed)" 状态, 准入 A.2 task-planner。

---

## §7 R2 raw transcripts

R2 4 agent outputs full content preserved in session conversation history (2026-05-23 ~10:30-11:00 UTC). 本报告 §1/§2/§3/§4/§5 是 orchestrator 聚合。

---

## §8 Cross-references

- Predecessor R1 report: `.aria/audit-reports/post_spec-R1-2026-05-23T0900Z-...orchestrator.md`
- Spec proposal Rev1: `openspec/changes/aria-layer2-docker-auth-cold-pull-fix/proposal.md`
- DEC memo: `.aria/decisions/2026-05-23-layer2-docker-auth-cold-pull-fix.md`
- Convergence policy: `[[feedback_audit_r2_collapse_default_vs_owner_invoked]]`
- NEW finding policy: `[[feedback_paper_fix_antipattern]]`

**Created**: 2026-05-23 ~11:00 UTC
**Author**: solo-lab (uni.concept.wzfq@gmail.com), aggregated by Claude Opus 4.7
**Verdict**: PASS_WITH_WARNINGS — Rev2-micro sweep 后准入 A.2

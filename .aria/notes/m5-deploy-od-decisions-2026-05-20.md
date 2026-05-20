# M5 T-deploy v2 playbook — Owner OD decisions

> **Created**: 2026-05-20 ~05:54 UTC
> **Authority**: Owner via AskUserQuestion 4-batch
> **Playbook**: `docs/handoff/2026-05-20-m5-deploy-playbook-v2-accurate.md`
> **Prerequisites read**: session-final + prod-state-investigation + v2 playbook ✅

---

## Decisions

| OD | 决策 | 含义 |
|----|------|------|
| **OD-1** Uncommitted M aria-orchestrator | **(a) Reset** | `git submodule update --init aria-orchestrator` 丢弃本地 bump; Phase B Step 3 一次跳到 962cb56 (M5 + HCL fix) |
| **OD-2** Cron architecture | **(b) Pure Nomad periodic** | 部署 `aria-layer1-reconcile.nomad.hcl` + `aria-layer1-cron.nomad.hcl`; Hermes-internal cron 关闭或不注册 (需 verify Hermes plugin entry-point 可 disable) |
| **OD-3** `/opt/aria-orchestrator/hermes-data/` 缺失 | **DEFERRED** — 待 Phase A.4 live Nomad job inspect 后再决 |
| **OD-4** `/opt/aria-orchestrator/app/` 遗留物 | **DEFERRED** — 默认 leave alone, 待 Phase A.4 同批确认 |
| **OD-5** 211-commit jump strategy | **(a) Single big leap + 强 backup** | checkout master + pull + submodule update --init --recursive --remote 一次性;Phase A backup + post-leap smoke 兜底 |

---

## Phase A 启动授权

✅ Owner 已授权进 Phase A (~30min, 零 prod 写, SSH light-1 只读)。

Phase A 步骤序列:
- A.1 ✅ (本 doc)
- A.2 SSH light-1 → `cp -a /opt/aether-volumes/aria-layer1/data/dispatches.db /tmp/aria-layer1-snapshot-<TS>/` + Python sqlite3 integrity check
- A.3 SSH light-1 → `cd /root/Aria` → `git stash push` (保留 M aria-orchestrator 为后备) + `git branch backup/pre-m5-upgrade-<TS>`
- A.4 SSH light-1 → `nomad job inspect -t '{{json .Job.TaskGroups}}' aria-orchestrator` 安全字段限定 (Rule #7) → 记录到 `.aria/notes/prod-job-spec-live-2026-05-20.md`
- 然后 surface OD-3 + OD-4 ask owner 决策
- A.5 sign-off 后才进 Phase B

---

**Status**: Phase A in progress

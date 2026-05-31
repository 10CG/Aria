# Proposal: M6 cost-snapshot 写入 durable host volume (Blocker #2 永久解)

> **Status**: ✅ **Shipped** (2026-05-31 — Option B 实施 + prod 部署验证 via /state-scanner Phase B/C/D; aria-orchestrator master `3cd32fd`; smoke 证实写 volume not checkout; AC-7 链路待 06-01 02:00 第 3 snapshot 自动 PASS)
> **Level**: 2 (Minimal — infra config-path 改动 + 重部署, 向后兼容)
> **Source**: `.aria/notes/2026-05-30-m6-phase-b-blocker-chain-cost-snapshot.md` §C item Blocker #2 (P2, 标注「需拍板」)
> **关联归档 Spec**: `openspec/archive/2026-05-28-aria-2.0-m6-cost-acceptance` (本变更修其 snapshot 落盘机制)

---

## Why

M6 cost snapshot (`aria-layer1-cost-sentinel` 每日 cron) 当前写到 light-1 **git checkout** 内
`/root/Aria/aria-orchestrator/.aria/cost-snapshots/`,带来两个问题:

1. **无 durability**: snapshot 困在单节点 checkout 目录 (非 managed host volume)。light-1 重建/checkout 重置
   = 3-day rolling history (AC-7 闸门证据) + M6 cost-acceptance 历史**全丢**,需重新累积 3 天。
2. **dev/CI 读不到**: validator 默认读 `REPO_ROOT/.aria/cost-snapshots/`,dev 上该目录为空 → AC-7 在 dev 跑恒 FAIL
   (Blocker #2 本体)。

**约束**: light-1 的 Forgejo git 凭据已过期 (Blocker #-1, 关联 deferred secret rotation),节点无法 git push
回仓 → 排除「cron 从节点 commit-back」方案。

**Owner 拍板 (2026-05-31)**: 采 **Option B** — snapshot 改写到与 `dispatches.db` **同一 durable host volume**
(`/opt/aether-volumes/aria-layer1/data/`),AC-7 闸门仍 on-node 跑 (wrapper `m6-phase-b-gate-check.sh` 已就绪)。
解 durability,零新增凭据依赖 (绕过 #-1),改动最小。

---

## What Changes

| # | 文件 | 改动 | 兼容性 |
|---|------|------|--------|
| 1 | `acceptance/m6-cost-snapshot.py` | `_DEFAULT_ARCHIVE_DIR` 改由 `_resolve_default_archive_dir()` 读新 env `ARIA_COST_SNAPSHOT_DIR` (镜像既有 `_resolve_default_db_path()` / `ARIA_DB_PATH` pattern);default 不变 = `REPO_ROOT/.aria/cost-snapshots` | env 未设 = 现行为, 向后兼容 |
| 2 | `docs/validate-m6-handoff.py` | `--check-3-day-history` 支持 `--snapshots-dir <path>` flag + `ARIA_COST_SNAPSHOT_DIR` env (优先级 flag > env > default);default 不变 | env/flag 未给 = 现行为 |
| 3 | `deploy/aria-layer1-cost-sentinel.nomad.hcl` | `env {}` 增 `ARIA_COST_SNAPSHOT_DIR = "/opt/aether-volumes/aria-layer1/data/cost-snapshots"` (与 `ARIA_DB_PATH` 同 volume) | 新增 env, 不影响其他 job |
| 4 | `.aria/scripts/m6-phase-b-gate-check.sh` | VALIDATOR 调用加 `--snapshots-dir /opt/aether-volumes/aria-layer1/data/cost-snapshots` | wrapper 内部 |
| 5 | (一次性) 节点迁移 | 拷贝现有 `cost-2026-05-30.json` + `cost-2026-05-31.json` checkout → volume, 保 rolling-history 进度 | 不删原文件 (additive) |

---

## Impact

- **Durability**: snapshot 与 `dispatches.db` 同 host volume 同级别持久 (节点重建不丢)。
- **零新增凭据依赖**: 绕过 #-1 (节点 git push 不可用)。
- **AC-7 语义不变**: 只移读路径 (on-node 指向 volume),连续性/staleness 判定逻辑零改动。
- **向后兼容**: env 未设 → 与当前完全一致 (单测 / dev / 现有 fixture 不受影响)。
- **遗留未解 (本变更范围外)**: dev/CI 仍需 SSH 跑 on-node 闸 (已由 wrapper + 06-01 crontab 自动化);Blocker #-1 节点凭据
  仍需 owner 独立修 (影响节点全部 submodule 更新, 非本变更)。

---

## Acceptance Criteria

- **AC-1**: writer 设 `ARIA_COST_SNAPSHOT_DIR` → `cost-YYYY-MM-DD.json` 写到该目录;未设 → `REPO_ROOT/.aria/cost-snapshots`
  (与现状逐字节一致)。
- **AC-2**: validator `--snapshots-dir` / `ARIA_COST_SNAPSHOT_DIR` 读指定目录;均未给 → default 不变。
- **AC-3**: 重部署后 cost-sentinel 写到 volume;06-01 02:00 run 后 volume 上有 3 个连续 snapshot。
- **AC-4**: on-node wrapper 闸读 volume,≥3 连续后 AC-7 PASS (EXIT=0)。
- **AC-5**: 现有 2 个 snapshot 已迁移到 volume,rolling-history 无回退 (迁移后 volume = 2/3, 非 0/3)。

---

## Tasks

| TASK | 内容 | 阶段 | 风险 |
|------|------|------|------|
| TASK-001 | writer `_resolve_default_archive_dir()` env-path + 单测 (set/unset 两路) | 本地 | 低 (向后兼容) |
| TASK-002 | validator `--snapshots-dir` + env + 单测 | 本地 | 低 |
| TASK-003 | HCL `ARIA_COST_SNAPSHOT_DIR` env 行 + `nomad job validate` lint | 本地 | 低 |
| TASK-004 | wrapper `--snapshots-dir` 更新 | 本地 | 低 |
| TASK-005 | 节点迁移现有 2 snapshot checkout → volume | **prod (gated)** | 低 (additive) |
| TASK-006 | git bundle+scp 新 aria-orchestrator code → light-1 + `aether dev run` 重部署 | **prod (gated)** | 中 (绕 #-1, 触运行中 cron) |
| TASK-007 | `nomad job periodic force` smoke → 验 volume 写入 + on-node validator 读 volume | **prod (gated)** | 低 |

> **执行顺序**: TASK-001~004 (本地可逆, 含单测) → owner checkpoint → TASK-005~007 (prod, 用 bundle+scp 绕 #-1)。
> prod 段触及运行中 cron + 节点凭据 workaround, 故本地段完成后向 owner 确认再执行。

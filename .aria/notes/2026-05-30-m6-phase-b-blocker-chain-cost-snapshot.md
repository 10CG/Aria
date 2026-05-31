# M6 Phase B Blocker Chain — cost-snapshot 全链路诊断 (2026-05-30)

> **触发**: state-scanner 推荐 [1] M6 e2e-resilience Phase B → tasks.md 硬闸门 `validate-m6-handoff.py --check-3-day-history` FAIL (0 snapshot,需 ≥3)。
> **诊断者**: Claude (owner 授权逐层深挖 + 授权刷新 light-1)。
> **净结论 (诊断时)**: M6 余下 2 Spec (e2e-resilience + release-closeout) 的 Phase B **无法启动**,被一条 4 层 blocker 链阻塞,其中**最深一层是 Spec #1 的代码缺陷**,需独立 fix cycle。
>
> **更新 (2026-05-30 同 session 后续)**: 代码缺陷 (#-2) 已走 emergency_hotfix cycle 修复并发版 (aria-orchestrator `72fa62b` PR #21 / 主仓 `3183401`),已部署 light-1 (#0 刷新到 72fa62b) + cron 重部署 + 首个 snapshot 产出 (机制 prod 功能正常)。**剩余: 3-day 累积 (1/3, cron 每日自动) + Blocker #2 (snapshot-locality, 闸门在 light-1 跑) + Blocker #-1 (节点 git 凭据)。** 详见末尾 §RESOLUTION。
>
> **更新 (2026-05-31, /state-scanner Blocker #2 处理)**: **Blocker #2 (snapshot-locality) RESOLVED** — owner 拍板 Option B「Host volume + on-node 闸」。snapshot 改写 durable host volume (`ARIA_COST_SNAPSHOT_DIR` env, = dispatches.db 同 volume),AC-7 闸 on-node 读 volume (wrapper `--snapshots-dir`)。Spec archived `openspec/archive/2026-05-31-m6-cost-snapshot-durable-volume`;aria-orchestrator master `3cd32fd` / 主仓 `47ed7a8`;prod 部署验证 (smoke mtime proof: 写 volume not checkout) + 迁移现有 2 snapshot。**3-day 累积现 2/3** (06-01 02:00 cron 第 3 个 → 02:30 crontab gate 自动 PASS)。**剩 Blocker #-1 (节点 git 凭据) 仍 owner-gated。** 副发现: cost-sentinel INFO 日志泄 Feishu webhook URL → Forgejo #136 (轮换+脱敏)。

---

## Blocker 链 (由浅入深,实测顺序)

| 层 | Blocker | 证据 | 状态 |
|---|---|---|---|
| #1 | `aria-layer1-cost-sentinel` cron 从未注册 | Nomad job 列表:aria-layer1 系列 7 个 job 独缺它;HCL 头 "Owner action items" step 4 `aether dev run` 从未执行 | ✅ **RESOLVED** — 重部署 + 首 snapshot 产出 (smoke `7ce85072` exit 0);下次 02:00 自动 |
| #2 | snapshot 写 light-1 本地 `/root/Aria/aria-orchestrator/.aria/cost-snapshots/`,无 commit/sync 回仓 | `m6-cost-snapshot.py` `REPO_ROOT = HERE.parent`;HCL 无 git push 步骤 | ⚠️ **未解 (方法论 gap)**:闸门 validator 在 dev 跑读不到 node-local 文件 → 3 天后在 light-1 上跑 validator (节点 checkout 内已有),或同步回仓 |
| #0 | light-1 节点 `aria_layer1` editable-install 指向的 `/root/Aria/aria-orchestrator` 子模块陈旧 (962cb56,无 cost_snapshot_runner) | smoke alloc `e4bb585d` exit 1: `No module named aria_layer1.cost_snapshot_runner` | ✅ **RESOLVED** — bundle 交付,节点刷新到 `72fa62b` (含 hotfix) |
| #-1 | 节点 Forgejo git 凭据**过期** → 无法从内网 Forgejo fetch 任何新代码 | `git fetch origin` → `Credentials are incorrect or have expired` (192.168.69.200:3000) | ⚠️ **未解 (更广影响)**:节点全部 submodule 无法更新;关联 deferred secret rotation;本次用 git bundle+scp 绕过 |
| **#-2 (真根因)** | **Spec #1 (M6 cost-acceptance) cost-snapshot SQL 引用不存在的列 `created_at`** | smoke alloc `c7674182` (e5a7d06 代码) exit 1: `[ERROR] Snapshot failed: no such column: created_at`。`m6-cost-snapshot.py:141,148` `WHERE created_at > datetime('now','-30 days')`;但 `dispatches` 表时间列是 `state_entered_at`/`last_heartbeat_at`,schema (含 e5a7d06) **无 `created_at` 列** | ✅ **RESOLVED** — emergency_hotfix `72fa62b`:`created_at` → `COALESCE(cycle_start_ts, state_entered_at)` (owner-ratified) + real-schema regression gate;prod 部署验证 cost.json 生成 |

---

## 真根因详解 (#-2)

- **缺陷**: `aria-orchestrator/acceptance/m6-cost-snapshot.py` 第 141 + 148 行 cost 聚合 SQL 用 `created_at` 列,`dispatches` 表无此列 (`created_at` 仅作为 `schema_meta` 表的一个 **key** 存在,非列)。
- **后果**: M6 Spec #1 的 cost-snapshot **对真实 prod `dispatches.db` 从未成功跑过** —— 任何真 DB 都会 `no such column: created_at`。整个 cost-acceptance + 3-day-history 闸门从未端到端验证过 prod。
- **为何 AB/单测/audit 没抓到**: 单测必然用了带 `created_at` 的 mock/fixture DB (或 mock 查询),fixture schema ≠ prod schema → 经典 `feedback_test_mock_pattern_hides_prod_bug` 重演;`feedback_validator_repo_drift_guard_test` (validator 必跑 committed canonical instance) 本可拦截但 cost-snapshot 无此类 live-DB gate。
- **语义未定**: `created_at` 该 (a) 改名为 `state_entered_at`(但 state_entered_at 随状态迁移变动,非稳定创建时刻,30/7-day cost 窗口语义会漂移),还是 (b) 新增一个真正的 `created_at` 列 (migration 007 范围?,需建表时写入)。**需 owner 拍板意图**,故未擅自修。

---

## 本 session 已执行的变更 (prod 状态变动留痕)

1. **light-1 `/root/Aria/aria-orchestrator` 子模块: 962cb56 → e5a7d06** (干净 FF,via git bundle+scp 绕过过期凭据)。
   - e5a7d06 = dev 主仓当前 blessed 指针;962cb56..e5a7d06 共 16 commit,**仅 2 个动 aria_layer1 包** (5b75d5e+51b28cb,M6 cost),tick/reconcile/comment_poll runner **0 改动**。
   - 验证: sibling 三 runner checkout 后仍 `import OK` —— 对正在运行的 aria-layer1-cron/reconcile/comment-poll **无回归**。
   - **可逆**: `git checkout 962cb56` 即还原。owner 若想保持最小漂移可 revert;否则 e5a7d06 更接近 master,建议保留。
2. **`aria-layer1-cost-sentinel` cron**: 部署 → 2 次 smoke 失败 (module / created_at) → **完全 purge 清除** (父+2 子 job)。集群恢复到诊断前状态 (无此 job)。

---

## 待 owner 决策 / 后续 fix cycle

1. **[P1 真 unblock] 修 Spec #1 cost-snapshot `created_at` schema-contract bug** —— 适配 emergency_hotfix lane (v1.35.0 新增) 或 Level 2 Spec;需先定 `created_at` 语义 (改列名 vs 加列+回填)。修完才能让 cost-snapshot 对 prod DB 跑通。
2. **[P1] 节点 Forgejo git 凭据过期 (#-1)** —— 关联 deferred secret rotation;影响 light-1 全部 submodule 更新能力,不止本 cron。需 owner 修复节点凭据 (Rule #7:不在 chat 处理 value)。
3. **[P2] snapshot-locality gap (#2)** —— cron 写 node-local,闸门 validator 在 dev 跑。需拍板:on-node 验证 (SSH/aether) vs cron 加 commit-back/sync。
4. **顺序**: 修 #-2 代码 → 修 #-1 凭据 (或继续 bundle 绕过) → 重部署 cron → force smoke 验证 cost.json 真生成 → 解 #2 → 等 3 天 rolling → M6 Phase B 闸门才可能过。

> **方法论教训**: 一个 AB/单测/audit 全过、已 archived 的 Spec,可以在 prod 上**完全非功能** (代码 bug + 从未部署 + DB 未迁移 + 节点凭据过期叠加)。里程碑"可发版"判定必须对 prod **live-probe Phase B 前置**,不能凭 archived 状态推断。见 memory `feedback_shipped_archived_spec_can_be_nonfunctional_on_prod`。

---

## RESOLUTION (2026-05-30 同 session 后续执行)

**A. emergency_hotfix cycle (#-2 代码缺陷)** — owner 拍板 `COALESCE(cycle_start_ts, state_entered_at)`:
- code: `m6-cost-snapshot.py` 2 query `created_at` → COALESCE;test: 3 fixture 修真列 + **新增 `test_m6_cost_snapshot_real_schema.py`** (对真 schema.sql 跑 query 的 anti-recurrence gate);doc: 2 归档 Spec POST-ARCHIVE CORRECTION 横幅。
- 审查: aria:code-reviewer 1 轮 PASS (0 Critical/Important, 2 Minor 已处理)。
- 发版: aria-orchestrator PR #21 → `72fa62b` (origin+github);主仓 `3183401` (rebase over `eb7052e` 另一终端 Spec, 零冲突)。Prod-Validated trailer。

**B. 部署 light-1** (#0 + #1):
- 节点 `/root/Aria/aria-orchestrator` 子模块 e5a7d06 → `72fa62b` (git bundle 增量,绕过 #-1 过期凭据)。COALESCE 落地, `IMPORT OK`。
- cost-sentinel cron 重部署 (`aether dev run`) + `nomad job periodic force`。
- **验证: smoke alloc `7ce85072` exit 0 + `[OK] cost.json written successfully.`**;`/root/Aria/aria-orchestrator/.aria/cost.json` (dual-row) + `cost-snapshots/cost-2026-05-30.json` 生成。cron 下次 02:00 自动。

**C. 仍未解 (M6 Phase B 真解锁还需)**:
1. **3-day rolling 累积**: 现 1/3。cron 每日 02:00 自动加, ~2026-06-01 满 3 个。
2. **Blocker #2 (snapshot-locality)**: snapshot 在 light-1 本地。3 天后跑 `validate-m6-handoff.py --check-3-day-history` 须**在 light-1 上跑** (节点 `/root/Aria/aria-orchestrator/docs/` 内已有 validator),或加 sync/commit-back。dev 上跑仍读 0。
3. **Blocker #-1 (节点 git 凭据过期)**: 本 session 用 bundle 绕过;长期需修 (关联 deferred secret rotation),否则每次节点更新都要手动 bundle。

**M6 Phase B 状态**: 核心障碍 (代码 + 部署) 已清;只差时间累积 (3 天) + Blocker #2 闸门验证路径小决策。

# Track A — M4 Owner Deploy Playbook (2026-05-09)

> **目标**: 将 US-024 M4 Layer 1 Forgejo PR comment polling 部署到 Aether 集群,
> 完成 production unblock。
>
> **角色**: AI 已准备静态 artifacts; **owner 执行 5 步部署 + E2E smoke**。
>
> **预计耗时**: 3-4h owner 时间 (含 first /aria approve E2E)。
>
> **不可协商规则** (per Aria CLAUDE.md 规则 #7 secret-hygiene + memory `feedback_secrets_never_in_conversation`):
> - 所有 secret-set 命令必须 `>/dev/null 2>&1` redirect output
> - 验证只用 `nomad var get -out=keys`,不读 secret 字面值
> - secret 字面值不出现在 conversation / chat / commit message / log

---

## 0. 前置检查 (3 分钟)

```bash
# Aether 集群可达
aether status --nodes 2>&1 | head -5

# Forgejo 内网可达 (绕 CF Access)
curl -s -o /dev/null -w "%{http_code}\n" http://192.168.69.200:3000/api/v1/version

# aria-orchestrator submodule HEAD = 589b6ac (M4 merge commit)
git -C /home/dev/Aria/aria-orchestrator rev-parse HEAD
# Expected: 589b6ac4...

# host volume 存在 (sister jobs 共用)
aether dev exec light-1 "ls -la /opt/aether-volumes/aria-layer1/data/ 2>&1" 2>&1 | head -5
# Expected: dispatches.db + m1-handoff.yaml 已在
```

**Stop 条件**: 任一步骤失败 → 不要继续,先 ping Aether ops。

---

## 1. Nomad Variables 配置 (10 分钟)

> **6 个 nomadVar key 需要存在** (3 个继承自 sister jobs + 3 个 M4 新增):
>
> | Key | 来源 | M4 必需 |
> |-----|------|---------|
> | `ARIA_FEISHU_WEBHOOK_URL` | 已存在 (cron + reconcile job 共用) | ✅ |
> | `FORGEJO_BOT_PAT` | 已存在 | ✅ |
> | `FORGEJO_BOT_USER` | 已存在 | ✅ |
> | `ARIA_FEISHU_SIGNING_SECRET` | **M4 新增** | ✅ M4 reject 卡片 sign |
> | `ARIA_AUTHORIZED_APPROVERS` | **M4 新增** | ✅ owner = `simonfish` (per A.1 lock) |
> | `ARIA_BOT_USERNAME` | **M4 新增 (optional)** | 🟡 set 后启用 self-comment filter (defense-in-depth, R2 QA-8) |

### 1.1 检查现有 keys (零字面值读取)

```bash
# 仅列 key 名,不读 value (per secret-hygiene)
nomad var get -out=keys nomad/jobs/aria-orchestrator
```

**Expected output** (deploy 前): 应至少含 `ARIA_FEISHU_WEBHOOK_URL`, `FORGEJO_BOT_PAT`, `FORGEJO_BOT_USER`。

### 1.2 设置 M4 新增 secrets

> ⚠️ **打开新 terminal,准备好 secret 字面值,然后执行**。每条命令 stdout/stderr 必须 redirect。

```bash
# (a) Feishu signing secret — Layer 1 outbound webhook 卡片签名
#     来源: Feishu 开放平台 → 自定义机器人 → 安全设置 → 签名校验
nomad var put -force nomad/jobs/aria-orchestrator \
  ARIA_FEISHU_SIGNING_SECRET="<paste-secret-here>" >/dev/null 2>&1

# (b) Authorized approvers (owner Forgejo username)
#     M4 lock = "simonfish" per Phase A.1 (2026-05-07)
#     格式: comma-separated 列表 (M4 单值, M5+ 可扩展)
nomad var put -force nomad/jobs/aria-orchestrator \
  ARIA_AUTHORIZED_APPROVERS="simonfish" >/dev/null 2>&1

# (c) Bot username (optional, defense-in-depth)
#     如果有专用 aria-bot Forgejo 账号 → 填账号名;无则 skip
#     用途: 让 comment_poll 跳过自身 reply 评论 (避免 loop)
nomad var put -force nomad/jobs/aria-orchestrator \
  ARIA_BOT_USERNAME="aria-bot" >/dev/null 2>&1   # 或 skip 此条
```

**重要**: 上面命令使用 `nomad var put -force` 覆写;如不希望覆盖现有 key,改用 `nomad var put` (不带 `-force`,key 已存在则报错,需 owner 明确决策)。

### 1.3 验证全部 keys 已就位

```bash
nomad var get -out=keys nomad/jobs/aria-orchestrator
# Expected (M4 new): ARIA_FEISHU_SIGNING_SECRET, ARIA_AUTHORIZED_APPROVERS
# (ARIA_BOT_USERNAME 可选)
# (sister 已有: ARIA_FEISHU_WEBHOOK_URL, FORGEJO_BOT_PAT, FORGEJO_BOT_USER)

# 验证 metadata (length only, 不读 value)
for k in ARIA_FEISHU_SIGNING_SECRET ARIA_AUTHORIZED_APPROVERS; do
  echo -n "$k length: "
  nomad var get -out=json nomad/jobs/aria-orchestrator 2>/dev/null \
    | python3 -c "import sys,json; v=json.load(sys.stdin)['Items'].get('$k',''); print(len(v))" 2>/dev/null
done
# Expected: 两个值 length > 0
```

---

## 2. 验证 HCL job spec (2 分钟)

```bash
cd /home/dev/Aria/aria-orchestrator

# Static lint (per memory feedback_nomad_hcl_validate_early)
nomad job validate deploy/aria-layer1-comment-poll.nomad.hcl 2>&1 | tee /tmp/nomad-validate.log
echo "Exit: $?"
```

**3 路径决策树**:

| validate 输出 | 路径 |
|---------------|------|
| `Job validation successful` (exit 0) | ✅ 跳到第 3 步 deploy |
| `invalid cron expression` (Nomad < 1.4) | 🔄 走 **Fallback 5-field cron** (见下方) |
| 其他 error | ⛔ Stop, ping Aether ops with /tmp/nomad-validate.log |

### Fallback 5-field cron (仅当 Nomad < 1.4)

```bash
# 1. 改 HCL: 6-field → 5-field
cd /home/dev/Aria/aria-orchestrator
cp deploy/aria-layer1-comment-poll.nomad.hcl deploy/aria-layer1-comment-poll.nomad.hcl.bak
sed -i 's|crons            = \["\*/30 \* \* \* \* \*"\]|crons            = ["* * * * *"]|' \
  deploy/aria-layer1-comment-poll.nomad.hcl

# 2. 改 job command args 加 --continuous (1 cron call → 内部 30s sleep loop)
#    runner main() 已支持 --continuous --interval --max-iterations 三参数
#    (per memory feedback_paper_fix_antipattern R3 修复)
# 编辑 deploy/aria-layer1-comment-poll.nomad.hcl:82-93,把 args 改为:
#    args = [
#      "-m",
#      "aria_layer1.comment_poll_runner",
#      "--job-id", "aria_layer1_comment_poll",
#      "--continuous",
#      "--interval", "30",
#      "--max-iterations", "2",     # 1 cron call = 2 polls (0s + 30s)
#    ]

# 3. 再次 validate
nomad job validate deploy/aria-layer1-comment-poll.nomad.hcl
```

---

## 3. Deploy + 验证 alloc launch (5 分钟)

```bash
# Deploy
aether dev run /home/dev/Aria/aria-orchestrator/deploy/aria-layer1-comment-poll.nomad.hcl \
  --name aria-layer1-comment-poll 2>&1 | tee /tmp/aether-deploy.log

# 验证 Nomad UI / CLI 看到 job
nomad job status aria-layer1-comment-poll 2>&1 | head -20
# Expected: Type=batch, Periodic=true, Next periodic launch ~30s

# 等 60 秒后查看 alloc 是否启动了至少 1 次
sleep 60
nomad job status aria-layer1-comment-poll 2>&1 | grep -A 5 "Allocations\|Latest Run"

# Tail recent alloc logs
LATEST_ALLOC=$(nomad job status aria-layer1-comment-poll 2>&1 | grep -oP '^[a-f0-9-]{8}\b' | head -1)
[ -n "$LATEST_ALLOC" ] && nomad alloc logs "$LATEST_ALLOC" 2>&1 | tail -30
```

**Expected log content** (per HCL header):
- `comment_poll: tick summary processed=0 decided=0 errors=0`
- 无 `ARIA_AUTHORIZED_APPROVERS not configured` warning
- 无 `Failed to fetch comments` HTTP 错误

**3 路径决策树**:

| log 内容 | 路径 |
|---------|------|
| `tick summary processed=0` (clean) | ✅ 跳到第 4 步 smoke |
| `ARIA_AUTHORIZED_APPROVERS not configured` | 🔧 回到第 1 步,补 nomad var put |
| HTTP 401 / 403 | 🔧 检查 `FORGEJO_BOT_PAT` value 是否过期 (rotate via Forgejo settings) |
| Python ImportError / DB connection refused | ⛔ Stop, 检查 host volume 是否存在 + venv 是否 ready (`/opt/aria-orchestrator/venv/bin/python -m aria_layer1 --help`) |

---

## 4. E2E smoke test (15-30 分钟)

> **目标**: 触发一个 dispatch 走完 S0 → S7_HUMAN_GATE → /aria approve → S8_MERGE → S9_CLOSE。

### 4.1 Trigger dispatch

owner 选 1 种方式触发 dispatch (任选其一):

**方式 A — Forgejo issue label trigger** (推荐):
```bash
# 在 Forgejo 上,选一个 test issue (e.g. 创建 fresh test issue),
# label 为 "aria-runner" 或 "aria-auto"。
# Phase 1 scan trigger 会扫到 → 进 S0_IDLE → S1_SCAN → ... → S6_REVIEW PASS → S7_HUMAN_GATE
# (依赖 aria-layer1-cron 30min 节奏,首次可能等待 ~15min)
```

**方式 B — Manual force**:
```bash
nomad job periodic force aria-layer1-cron        # phase 1 scan now
# 然后等 1-2 min 看 dispatches.db 是否有新 row
aether dev exec light-1 "sqlite3 /opt/aether-volumes/aria-layer1/data/dispatches.db \
  'SELECT id, state, forgejo_issue_id FROM dispatches ORDER BY id DESC LIMIT 3' 2>&1" 2>&1
```

### 4.2 跟踪 state machine

```bash
# 每 30s 检查一次 dispatch state
DISPATCH_ID=<paste-id-here>
for i in {1..40}; do
  STATE=$(aether dev exec light-1 "sqlite3 /opt/aether-volumes/aria-layer1/data/dispatches.db \
    'SELECT state, fail_reason FROM dispatches WHERE id=$DISPATCH_ID' 2>&1" 2>&1)
  echo "[$i/40] $STATE"
  case "$STATE" in
    *S7_HUMAN_GATE*) echo "✅ 进入 S7,等 Feishu 卡片"; break ;;
    *S_FAIL*)        echo "⛔ FAIL — 检查 fail_reason"; break ;;
  esac
  sleep 30
done
```

### 4.3 Feishu 卡片验证

- ✅ Feishu 群收到 `M4 Human gate request` 卡片 (含 PR URL + dispatch_id + risk_tier_stub=always)
- ✅ 卡片 `查看 PR` 按钮可点击
- ❌ 没收到 → 检查 `ARIA_FEISHU_WEBHOOK_URL` value (curl 测试) + Feishu 群机器人是否 active

### 4.4 PR 评论 /aria approve

owner 在 Forgejo PR 评论框输入:
```
/aria approve
```

或拒绝路径:
```
/aria reject: 测试 reject 路径
```

或测试 7d auto-reject 路径: 不评论,等待 (M4 reconciler 7d 兜底 — smoke 时可以加速验证,临时改 `ARIA_RECONCILER_S7_MAX_AGE_DAYS=0`)。

### 4.5 验证 transition

```bash
# 等待 60s (comment_poll 30s × 2 ticks)
sleep 60

aether dev exec light-1 "sqlite3 /opt/aether-volumes/aria-layer1/data/dispatches.db \
  'SELECT id, state, human_decision, human_decided_at FROM dispatches WHERE id=$DISPATCH_ID' 2>&1" 2>&1
# Expected (approve path): state=S8_MERGE → S9_CLOSE, human_decision=approve

# 看 comment_poll alloc log 是否有命中
nomad alloc logs <alloc-id> 2>&1 | grep -i "decided=1\|human_decision\|/aria approve" | tail -5
```

### 4.6 6 mandatory Feishu+Hermes configs 复检 (per `feedback_feishu_hermes_gotchas`)

> M4 用 webhook outbound only,绕过了 6 项中的多数,但仍需复检关键 3 项:

| # | Config | 验证方法 |
|---|--------|----------|
| 1 | Webhook URL accessible | `curl -X POST -d '{"msg_type":"text","content":{"text":"smoke"}}' "$URL"` 返回 `{"code":0,...}` |
| 2 | Signing secret correct | 4.3 收卡 = 正确 |
| 3 | Card size cap < 3000 chars (lark_md) | `_sanitize_markdown` 已 truncate, 但人工目测 reject 卡片 if reject_reason 长 |

---

## 5. 部署成功 → 写回 m4-handoff.yaml (15 分钟)

> AI 已准备 writeback 模板见 §5.1。Owner 用 sed/Edit 工具批量替换 `<pending>` 为实测值。

### 5.1 立即可填字段 (Phase B.3 audit re-check, AI 可代填)

下面这些来自 R5 audit report,**owner 授权后 AI 可代填**:

```yaml
# Lines 33-53 — Tier-1 acceptance results (per pre_merge R5 CONVERGED)
m4_acceptance:
  a1_slo_formula_synthetic_passed: true
  b_seven_day_auto_reject_passed: true
  c_idempotency_three_layer_passed: true
  d1_three_path_cycle_synthetic_passed: true
  e_schema_v3_migration_passed: true

# Lines 56-59 — PRD reframe (Phase B.2 已完成 4 处)
  f_prd_line_405_406_reframed: true
  f_prd_section_170_reframed: true
  f_prd_us025_table_synced: true
  f_prd_section_409_reconciliation_passed: true

# Lines 211-216 — pre_merge audit trail (Phase B.3 R1-R5)
audit_trail:
  pre_merge:
    rounds: 5    # owner-invoked R1→R5 (NOT R3+R4 collapsed)
    converged: true
    convergence_pattern: "R1 NEEDS_FIX (36) → R2 SCOPE_OK_R2 4/4 → R3 owner-invoked NEW_FINDINGS (15) → R4 STABILITY_CONFIRMED → R5 CONVERGED 4/4"
    final_verdict: "PASS (R5 4/4 CONVERGED)"
    reports:
      r1: ".aria/audit-reports/pre_merge-R1-2026-05-09T0642Z-us024-m4.md"
      r2: ".aria/audit-reports/pre_merge-R2-2026-05-09T0735Z-us024-m4.md"
      r3: ".aria/audit-reports/pre_merge-R3-2026-05-09T0750Z-us024-m4.md"
      r4: ".aria/audit-reports/pre_merge-R4-2026-05-09T0820Z-us024-m4.md"
      r5: ".aria/audit-reports/pre_merge-R5-2026-05-09T0840Z-us024-m4.md"
```

### 5.2 部署后填字段 (Tier-2 real-dispatch metrics)

```yaml
# Lines 35-37, 48-50 — 取决于 owner 实测 dispatch 数
m4_acceptance:
  a2_slo_real_dispatches_count: <实测 dispatch 总数>      # 期望 ≥3
  a2_slo_real_median_seconds: <median 人决策延迟>          # 期望 < 600
  a2_slo_real_passed: <bool>                                # median < 600
  d2_real_dispatches_count: <≥2>
  d2_real_approve_count: <count>
  d2_real_reject_count: <count>

# Lines 66-79 — operational metrics (从 dispatches.db + Nomad alloc logs aggregate)
m4_human_gate_metrics:
  total_dispatches_through_s7: <count>
  approve_count: <count>
  reject_count: <count>
  human_timeout_count: <count>
  comment_poll_actual_p50_latency_seconds: <median tick→decided 延迟>
  comment_poll_actual_p99_latency_seconds: <p99>
  reconciler_s7_scans_total: <reconciler alloc logs 累计 scan 次数>
  reconciler_s7_timeouts_triggered: <实际 timeout 触发次数>
  reconciler_s7_cas_lost_total: <comment_poll race vs timeout 失败次数>
```

### 5.3 Phase D.2 retrospective fields

```yaml
# Lines 5, 25-26 — header + go decision
date: 2026-05-09
go_decision: "Go-with-revision"   # 或 "Go" / "No-Go"
rationale: |
  M4 Tier-1 全 PASS (R5 4/4 CONVERGED). Tier-2 ≥3 dispatches 实测 (≥1 approve + ≥1 reject + ≥1 timeout)
  median < 10min SLO 满足. 已部署到 Aether light-1, alloc 30s 节奏稳定.
  Revision: OD-M4-2 underbaseline 60h→<actual>h ×<ratio> retrospective filed.

# Lines 153-154 — effort
effort:
  actual_phase_b_2_hours: <实际 Phase B.2 时数>      # 期望 ~22-26
  od_m4_1_triggered: false                          # 未触发 (under baseline)

# Line 160 — owner signoff
signoffs:
  owner_phase_d_2: "Signed off — owner reviewed Phase B.3 R5 + Tier-2 ≥3 dispatches passed (2026-05-09)"
```

---

## 6. OD-M4-2 underbaseline retrospective (AI 草稿,owner 审阅)

> Per `feedback_spec_frontmatter_reflects_reality` + R3 TL-R3-5: M4 实测 22-26h vs 60h baseline (×0.42),
> 与 M3 OD-13 反向 (M3 over baseline)。需 OD 锁定 retrospective rationale,避免未来项目轻信 baseline。

**草稿** (建议存入 `.aria/decisions/2026-05-09-od-m4-2-underbaseline-retrospective.md`):

```markdown
# OD-M4-2: M4 underbaseline retrospective (60h → ~22-26h actual ×0.42)

> **Date**: 2026-05-09
> **Spec**: openspec/archive/2026-05-09-aria-2.0-m4-human-gate-feishu-approval
> **Trigger**: R3 TL-R3-5 (Phase B.3 audit important finding)
> **Decided by**: owner (Phase D.2 retrospective)

## 现象

M4 spec 锁 60h Phase B.2 baseline (per Q8' β'); 实测 ~22-26h (×0.42, ~63% saved)。
trajectory 与 M3 反向 (M3 OD-13 over baseline +20%, M4 -58%).

## Why baseline 高估了

1. **Trust-but-verify discovery 红利**: M2/M3 已实现 S7_HUMAN_GATE / FeishuWebhookClient / transitions stub,M4 实施时发现大量"骨架 ready",节省 ~25-30h。Phase A.1 brainstorm 时未充分 audit 已有代码路径。
2. **Phase A 决策深度高 (per `feedback_phase_a_depth_drives_b_velocity`)**: Q1-Q14 + R2 4/4 SCOPE_OK + 6 段 OD lock 让 Phase B 几乎 mechanical translation,无 mid-implementation 重构。
3. **Schema migration v3 选择 additive-only** (vs M3 OD-12 等数据迁移): SQLite atomic migration 比预期 ~3h × 2 testing 节省 ~4h。
4. **Audit 5-round 真跑反而省了 rework**: R1 36 findings → R2 SCOPE_OK_R2 70-76% reduction; R3 owner真跑发现 9 deferred items 不阻塞 merge; 没有 mid-implementation paper-fix 反复 (per `feedback_paper_fix_antipattern`)。

## How to apply (M5 spec drafter)

1. **M5 baseline 不可直接套用 M4 ×0.42 ratio** —— M5 范围 (Replay + Reconciler 深度增强 + 防漂移 + Review loop + 审计日志 immutable) 与 M4 不同,大概率 over baseline。
2. **M5 brainstorm Q0** 必须先 audit 现有代码 (per Trust-but-verify) 再 lock baseline。
3. **abi_compat_promises 4 forward-binding** 已锁,M5 不得违反 (validate-m5-handoff.py 强制)。

## Ratio 历史 trajectory (3 milestones)

| Milestone | Spec baseline (h) | Actual (h) | Δ Ratio | 方向 |
|-----------|-------------------|-----------|---------|------|
| M2 | 156 | ~150 | 0.96 | ≈ baseline |
| M3 | 60 | 72 | 1.20 | over (OD-13) |
| M4 | 60 | 22-26 | 0.42 | under (本 OD-M4-2) |
| M5 | 120 (PRD §409) | TBD | TBD | TBD |

## Owner sign-off

- [ ] Owner 已审阅本 retrospective (date: ____________)
- [ ] OD-M4-2 锁定 (M4 spec archived, this decision is post-hoc retrospective)

---

**Co-references**:
- `feedback_phase_a_depth_drives_b_velocity` (Phase A 深度→B velocity)
- `feedback_paper_fix_antipattern` (R 轮 fix 三位一体)
- `feedback_spec_frontmatter_reflects_reality` (frontmatter reality drift)
- `project_us024_m4_closeout_2026-05-09` (M4 closeout context)
```

---

## 7. PR description amend (5 分钟,可与 §6 并行)

> Per R5 TL deferred: PR #10 + #94 描述含 "R3+R4 collapsed" 与 reality (R5 真跑 CONVERGED) 矛盾。
> PR 已 merged,改 description 仅是 metadata,不影响合并。

```bash
# PR #10 (aria-orchestrator)
forgejo PATCH /repos/10CG/aria-orchestrator/pulls/10 \
  -d '{"body": "Phase B.3 pre_merge audit (2026-05-09): R1 NEEDS_FIX (36) → R2 SCOPE_OK_R2 4/4 → owner-invoked R3 NEW_FINDINGS (15) → R4 STABILITY_CONFIRMED → **R5 CONVERGED 4/4**. NOT R3+R4 collapsed; per `feedback_owner_invoked_convergence_loop`."}' \
  >/dev/null 2>&1

# PR #94 (Aria 主仓)
forgejo PATCH /repos/10CG/Aria/pulls/94 \
  -d '{"body": "<同上 reframe>"}' \
  >/dev/null 2>&1
```

---

## 8. Forgejo Issue #86 close (M4 kickoff, 1 分钟)

```bash
forgejo PATCH /repos/10CG/Aria/issues/86 -d '{"state": "closed"}' >/dev/null 2>&1

# 或加 close comment 指向 closeout
forgejo POST /repos/10CG/Aria/issues/86/comments -d '{
  "body": "M4 done 2026-05-09. PR #94 merged. See `docs/handoff/2026-05-09-us024-m4-done.md`."
}' >/dev/null 2>&1

forgejo PATCH /repos/10CG/Aria/issues/86 -d '{"state": "closed"}' >/dev/null 2>&1
```

---

## 9. 完成 → 状态汇报

部署成功后,owner reply session 主对话:

```
Track A 完成. dispatch <id> 走完 S7→approve→S8→S9 ✅
m4-handoff.yaml writeback 已完成 (Tier-2 + Phase D.2 字段)
OD-M4-2 草稿已审阅 + 签字
PR #10 + #94 description amended
Issue #86 closed
```

AI 收到后会:
1. commit + dual-push m4-handoff.yaml + OD-M4-2 retrospective + 任何 .aria/decisions/ 新条目
2. 更新 docs/handoff/latest.md 标记 Track A 完成
3. 推 Track B (M5 brainstorm) 作为下一步

---

## 故障路径 (rollback)

| 故障 | 操作 |
|------|------|
| Job validate 失败,fallback 5-field cron 也失败 | Stop deploy,回到 .aria/decisions/ 立 OD-M4-Aether (新 spec) |
| Alloc 启动但 ARIA_AUTHORIZED_APPROVERS warning | 回到 §1.2 (b) 补 var |
| /aria approve 评论后 60s 内没 transition | tail comment_poll alloc log,看 comment cursor / pagination 是否卡住 |
| Feishu 卡片签名校验失败 | rotate ARIA_FEISHU_SIGNING_SECRET (per Feishu 群机器人 → 重新生成) + nomad alloc restart |
| reconciler S7 timeout 误触发 (本来想 approve) | 临时恢复 `ARIA_RECONCILER_S7_MAX_AGE_DAYS=7`,重做 dispatch |
| 整体 deploy 不可恢复 | `aether dev destroy aria-layer1-comment-poll --yes`,回到 closeout state d5610f0 |

---

## 相关文档

- `docs/handoff/2026-05-09-us024-m4-done.md` (Track A 主任务清单)
- `aria-orchestrator/docs/architecture-decisions.md` AD-M4-1~AD-M4-11
- `aria-orchestrator/docs/m4-handoff.yaml` (writeback target)
- `.aria/decisions/2026-05-07-us024-m4-brainstorm.md` (Q1-Q14 锁定)
- `.aria/audit-reports/pre_merge-R5-*` (R5 CONVERGED report)

**memory cross-references**:
- `feedback_secrets_never_in_conversation` (rule #7 secret-hygiene)
- `feedback_aether_tool_discovery_flow` (Aether status / nomad API 调查流程)
- `feedback_nomad_hcl_validate_early` (validate before run)
- `feedback_t15_owner_blocking_pattern` (owner cluster deploy blocking pattern)
- `feedback_owner_invoked_convergence_loop` (R5 真跑 vs OD-15 collapse)
- `feedback_paper_fix_antipattern` (3 位一体 fix)

---

**Created**: 2026-05-09
**Maintainer**: AI (静态 artifacts) + Owner (执行)
**Status**: Ready for owner execution

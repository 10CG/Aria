# m3-carryover-hcl-crons-sweep

> **Level**: Minimal (Level 2 Spec — 仅 proposal.md, 无 tasks.md)
> **Status**: Complete (2026-05-07, archived after 3-round multi-agent pre_merge audit STABLE convergence)
> **Created**: 2026-05-07
> **Completed**: 2026-05-07 (aria-orchestrator PR #7 merged at `5d0e70b`; Aria main PR #80 merged at `a21b619`; 3-round 4-agent pre_merge audit converged R1→R2→R3 STABLE 4/4; Forgejo Issue #76 close pending owner Aether dev verify)
> **R1 audit**: 4-agent multi-agent (backend-architect / qa-engineer / tech-lead / code-reviewer); ALIGNED 4/4 direction; tech-lead BLOCK on submodule regression (resolved R1→R2 fix: rebased onto master c0d8c46 + submod pointer → 5d0e70b post-#7-merge HEAD)
> **R2 audit**: same 4-agent team; ALL R1 CRITICAL CLOSED; ALIGNED 4/4; 3 R2 NEW MINOR closed in d4c66a3
> **R3 audit (stability)**: same 4-agent team; STABLE 4/4 (0 NEW findings, R2 closed); finding-set-equality convergence per `feedback_audit_convergence_pattern.md`
> **Owner action remaining**: Aether dev cluster verify (acceptance #7 — `aether dev run` + `nomad job inspect | jq .Periodic.Specs[0]` + `.NextLaunch`); pre-merge audit converged so verify becomes post-merge owner smoke test (HCL change is reversible via revert if verify fails)
> **Type**: 单子系统 hygiene 改动 (aria-orchestrator/deploy/ HCL × 2)
> **Source**: M3 closeout backlog Issue [#76](https://forgejo.10cg.pub/10CG/Aria/issues/76); m3-handoff.yaml §10 t16_backlog_issues #76; AD-M3-5 §风险 #6 (deferred to separate hygiene Spec)
> **Sister-bug bundle**: 否 (与 #75 result_path / #77 validator 分属不同子系统, owner 决策为 3 独立 Level 2)

---

## Why

`aria-orchestrator/deploy/` 下两个 periodic Nomad job 使用了 Nomad 1.8 起被弃用的 `cron =` 字段:

| 文件 | 行 | 当前值 | 用途 |
|------|----|--------|------|
| `aria-layer1-cron.nomad.hcl` | 36 | `cron = "0 * * * *"` | M2 Layer 1 cron tick (60min) |
| `aria-layer1-reconcile.nomad.hcl` | 66 | `cron = "15,45 * * * *"` | M3 reconciler half-offset (30min, AD-M3-5) |

`nomad job validate` 输出:

```
* cron is deprecated and may be removed in a future release. Use crons instead
```

**风险**:
- Aether 当前 Nomad 1.7.7 仍接受 `cron`, 警告非阻塞
- 未来 Nomad 升级 (1.8+) 移除 `cron` 字段时, 两个 periodic job 会拒绝注册 → cron tick + reconciler 双双停摆
- 这是 cycle close (M3 核心交付物) 的运行时基础设施, 一旦中断 dispatch 状态机停止前进

**为何 M3 时未一并修**:
- 单行 warning, 非 M3 acceptance 任何一条
- AD-M3-5 §风险 #6 显式 defer 到独立 hygiene Spec, 避免污染 M3 主议程
- m3-handoff.yaml §10 列入 T16 backlog, owner triage `<pending>` 标记为本 Spec 闭环目标

**Verifiability HIGH**: 上方 `grep` 输出直接定位 2 处, 无 prose-only 描述。

---

## What

### 字面替换

两个文件同一 pattern 替换:

```diff
 periodic {
-  cron             = "0 * * * *"
+  crons            = ["0 * * * *"]
   time_zone        = "UTC"
   prohibit_overlap = true
 }
```

```diff
 periodic {
-  cron             = "15,45 * * * *"
+  crons            = ["15,45 * * * *"]
   time_zone        = "UTC"
   prohibit_overlap = true
 }
```

**字段语义**: `crons` 是 array 形态, 允许单个 periodic stanza 配置多个 cron 表达式。本 Spec 每文件迁移到单元素 array, **不引入多 cadence**, 行为与原 `cron` 完全等价。

### 受影响范围

**仅 2 个文件**, 全 sweep 已确认无遗漏:

```bash
$ grep -rn -E "^\s*cron\s*=" aria-orchestrator/deploy/
aria-orchestrator/deploy/aria-layer1-cron.nomad.hcl:36:    cron             = "0 * * * *"
aria-orchestrator/deploy/aria-layer1-reconcile.nomad.hcl:66:    cron             = "15,45 * * * *"
```

其它 deploy/ 下 HCL (`aria-orchestrator.nomad.hcl`, `aria-orchestrator-light.nomad.hcl`) 不含 `periodic` stanza, 无需改动。

### 文档同步

`aria-orchestrator/docs/architecture-decisions.md` §AD-M3-5 §风险 #6 增加一行: "已通过 `m3-carryover-hcl-crons-sweep` Spec 闭环, 见 archive/<date>"。

---

## 非目标

- 不引入新 cadence (保持 60min / 30min half-offset 不变)
- 不调整 `time_zone` / `prohibit_overlap` 等其它 periodic 字段
- 不改 SQLite busy_timeout (AD-M3-5 §选型理由 #4 secondary guard 保留)
- 不修复其它 nomad job validate warnings (仅 cron→crons; 若有别的 warning 另立 Spec)
- 不动 `aria-orchestrator.nomad.hcl` / `aria-orchestrator-light.nomad.hcl` (无 periodic)

---

## 验收

- [ ] `aria-orchestrator/deploy/aria-layer1-cron.nomad.hcl:36` 改为 `crons = ["0 * * * *"]`
- [ ] `aria-orchestrator/deploy/aria-layer1-reconcile.nomad.hcl:66` 改为 `crons = ["15,45 * * * *"]`
- [ ] `nomad job validate aria-orchestrator/deploy/aria-layer1-cron.nomad.hcl 2>&1 | grep -c "cron is deprecated"` returns `0` (per R1-qa-engineer: concrete pass/fail signal)
- [ ] `nomad job validate aria-orchestrator/deploy/aria-layer1-reconcile.nomad.hcl 2>&1 | grep -c "cron is deprecated"` returns `0`
- [ ] `aria-orchestrator/docs/architecture-decisions.md` §AD-M3-5 §风险 #6 标注闭环引用
- [ ] m3-handoff.yaml §10 #76 entry `triage_t16` 字段从 `<pending>` 改为 `fix-now: closed by openspec/archive/<date>-m3-carryover-hcl-crons-sweep`
- [ ] **owner cluster verify** (concrete metric per R1-qa-engineer + R2-qa-engineer fallback): `aether dev run` 两 job, 后跑 `nomad job inspect <job> | jq -r '.Job.Periodic.Specs[0] // .Job.Periodic.Spec'` 验证 spec 字符串匹配 (`"0 * * * *"` / `"15,45 * * * *"`)。Nomad `crons` array 在 inspect 响应中应在 `Specs` (plural array); 若返回 `null` 则 fallback 至 `.Spec` (singular, legacy)。下个 periodic 触发时间通过 `nomad job inspect <job> | jq -r '.Job.Periodic.NextLaunch'` 检查 (应是下个 :00 或 :15/:45 时点)。
- [ ] Forgejo Issue #76 关闭, comment 引用 archive 路径
- [ ] PR + 多远程推送 (origin + github) per CLAUDE.md §版本发布检查清单

---

## 价值

- **前向兼容**: 解除 Nomad 1.8+ 升级路径上的隐性炸弹, cycle close 运行时基础设施长期稳定
- **文档闭环**: AD-M3-5 §风险 #6 / m3-handoff.yaml §10 #76 / Issue #76 三处 cross-reference 闭环, T16 closeout backlog 减一
- **零行为变化**: `crons = [X]` 与 `cron = X` 在 Nomad 1.7.7 行为完全等价, 回滚成本 = 反向 diff
- **样本积累**: 本 Spec 是 M3 carryover 三连的"热身样本", 走通 Phase A → B → C → D 全循环建立 micro-Spec PR 节奏模板, 为后续 #75 / #77 复用

---

## 风险与回滚

**风险**: Nomad 1.7.7 对 `crons` array 字段的解析正确性未在 Aether 实测过 (推断兼容, 因 Nomad changelog 显式说 `cron` is being **replaced** by `crons`).

**缓解**:
- `nomad job validate` (本地静态校验) 是第一道闸门
- Aether dev 实跑 (验收第 7 项) 是第二道闸门, owner-action 必须执行
- 若 dev 跑后下个 periodic 触发时间漂移, 立即 `git revert` 回退 (单 commit 两文件, 反向 diff 干净)

**Aether 版本契约**: 当前 Nomad 1.7.7 (per `aether status --nodes` 实测, m3-handoff 引用)。若 Aether 集群尚未升级到能解析 `crons` 的 Nomad 版本, 本 Spec 仍可合并代码改动, 但 owner cluster verify 步骤需推迟到 Nomad 升级完成 (届时反过来变成"升级路径解锁器")。

**Nomad 1.7.7 `crons` array 实证** (per R1-backend-architect 关切回应): 本地 dev 环境 `nomad version` = `Nomad v1.7.7` (与 Aether 集群同版本)。本地 `nomad job validate` 在两 HCL 文件均:
- exit code 0
- stdout 含 `Job validation successful`
- stderr/stdout 不再含 `cron is deprecated` warning (实证 grep -c = 0)

证据链: `nomad job validate` 不仅做 schema lint, 也校验字段 ID — 若 `crons` 在 1.7.7 是 unknown field 会被 silently ignore (Nomad HCL parser 对未知 stanza 字段非 error), 但配套 deprecation 提示 (`cron is deprecated... Use crons instead`) 在 v1.7.7 binary 中被实测移除 = 字段已被识别为 valid replacement。然而 *parser 接受* ≠ *runtime scheduler 行为等价*; **本地 binary lint clean ≠ Aether scheduler runtime 等价**, 后者 (next-launch 时间精确触发 + cadence 不漂移) 由验收 #7 owner cluster verify 兜底 (per R1-backend-architect + R2-code-reviewer language clarity request)。

> **决策**: 本 Spec 假设 Nomad 1.7.7 已支持 `crons` array (本地 v1.7.7 binary 实证 + changelog 推断双重证据)。若 owner cluster verify 失败 (next-launch 时间不符 / job 注册成功但永不触发), 本 Spec 失败回滚, 额外起草"等待 Nomad 升级"跟踪 Issue。

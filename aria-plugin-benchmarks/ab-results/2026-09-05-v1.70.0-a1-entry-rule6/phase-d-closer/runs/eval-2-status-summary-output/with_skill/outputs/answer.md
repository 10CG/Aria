# Phase D 收尾 — `add-payment-gateway`

先说一句实测前提, 再给完整收尾报告。

**gate 实跑 (未编造)** —— 收尾第一件事是跑 D.2 的 tri-state 闸门, 不是直接归档:

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/lib/spec_complete.py" \
  --gate "openspec/changes/add-payment-gateway"
```

```json
{"complete": false,
 "complete_reason": "proposal.md not found in openspec/changes/add-payment-gateway — malformed spec dir, gate stays closed",
 "verdict": "pass", "blocking_reasons": [], "warnings": [],
 "unverified_claims": [], "d_payload": null, "soft_errors": []}
```

即: **当前工作目录里没有 `add-payment-gateway` 这个活跃 change**(`openspec/changes/` 下是 a1-entry-claim-duplicate-work-guard / aria-2.0-m6-\* / aria-2.0-m7-\* 共 7 个), 两个 UPM 候选路径 (`mobile/docs/project-planning/…` / `backend/project-planning/…`) 也都不存在。

所以下面这份报告分两层给你: **本仓实跑得到的真实判定**, 加上**目标仓里 spec 存在时的完整收尾形态**。凡是只能从实跑取得的值 (module / cycle 号 / SHA / PR / 时间戳), 我用 `<...>` 标出并附取值命令, **不填假数据**——收尾报告里的假 SHA 比空位危险。

---

## 一、执行输出

```
╔══════════════════════════════════════════════════════════════╗
║              PHASE D - CLOSURE                               ║
╚══════════════════════════════════════════════════════════════╝

📋 执行计划
───────────────────────────────────────────────────────────────
  D.1   progress-updater     → 更新 UPM 进度
  D.post audit checkpoint    → post_closure 经验提取 (config 决定)
  D.2   openspec-archive     → 归档 Spec (tri-state verdict gate)
  D.2b  release_gate CLI     → 释放本 cycle claim (advisory)
  D.3   session-handoff      → 写 docs/handoff/ + latest.md
  D.4   ai-native-estimator  → 采集 token 工作量 (advisory)

🚀 执行中...
───────────────────────────────────────────────────────────────
  ⏭  D.1 跳过 → 未找到 UPM 文档
     探测: mobile/docs/project-planning/unified-progress-management.md  ✗
           backend/project-planning/unified-progress-management.md      ✗
     依据: 跳过规则「无 UPM → 跳过 D.1」

  ⏭  D.post 跳过 → audit.checkpoints.post_closure = "off"
     依据: .aria/config.json (owner 的配置决定; 属白名单第 1 类
           「config 显式 off」, 不是 AI 临场豁免)

  ⏭  D.2 跳过 (不归档) → gate: complete=false ∧ verdict=pass
     Spec: add-payment-gateway
     complete_reason: proposal.md not found in
       openspec/changes/add-payment-gateway — malformed spec dir
     路由: legacy skip 分支 (非 BLOCK — 见下方三态说明, 两者语义不同)
     → 没有目录可移动, 归档未发生, openspec-archive 未被调用

  ⏭  D.2b 未执行释放 → 本 session 未经 phase1_gate 认领 add-payment-gateway
     的 carry-id; 建议仍跑一次不带 --raw-track-id 的 sweep/gc 保持 ref 卫生

  ✅ D.3 可执行 → 写 docs/handoff/<YYYY-MM-DD>-<slug>.md
  ✅ D.4 可执行 → estimator capture (advisory)

🎉 工作流结论
───────────────────────────────────────────────────────────────
  状态: Phase D 未因此失败, 但**核心交付 (D.1 UPM + D.2 归档) 均未发生**
  根因: spec_id 在本仓不可解析 —— 先确认 change_id / 仓库, 再重跑
```

---

## 二、D.1 结果 (进度更新)

| 字段 | 本仓实测 | 目标仓应有的形态 |
|------|---------|-----------------|
| `upm_updated` | `false` (skipped) | `true` |
| module | — | `<module>` |
| 模式 | — | single-pass (`upm.milestone_driven` 未配置 ⇒ false) |
| cycleNumber | — | `<N>` → `<N+1>` |
| lastUpdateAt | — | `date -u +%Y-%m-%dT%H:%M:%SZ` 的输出 |
| stateToken | — | 重算 (读改写 UPMv2-STATE 后) |
| completedTasks | — | 追加本 cycle `TASK-xxx` 列表 |
| kpiSnapshot | — | 覆盖率等指标刷新 |

要点两条:

1. **模式决定工作量**。single-pass = D.1 全量更新所有 Story; 若目标仓开了 `upm.milestone_driven: true`, 则 C.2.6 已在每次 PR 合并时实时追加 sub-bullet 并把 Story 标成 `[~]`, D.1 只做 finalize: `[~]` → `[x] COMPLETED` + 在最后一条 sub-bullet 后追加 `archive: openspec/archive/add-payment-gateway/` + 刷 UPMv2-STATE 头 —— **不重建历史**。
2. **并发冲突**按 retry 处理 (max 3): 重读 UPMv2-STATE → 合并变更 → 重算 stateToken → 重写; 不是覆盖写。

---

## 三、D.2 结果 (Spec 归档) —— 这一步的判定必须看 verdict, 不能看 exit code

本次 gate 的 **exit code = 0**, 但归档**没有**发生。原因就是 `--gate` 的 exit code 是 `pass|warn` 二合一, 单看它会把「未完成 / 目录残缺」误读成「可以归档」。判定只能解析 stdout JSON 的 `verdict` + `complete` 两个字段。

四路路由 (本次命中第 2 路):

| 条件 | 结果 | 本次 |
|------|------|------|
| `openspec/changes/` 为空 | skip (无活跃 Spec) | 否 |
| `complete == false` ∧ `verdict != block` | **skip 不归档** (legacy), 回显 `complete_reason` | ✅ 命中 |
| `verdict == block` | **BLOCK** —— 高置信死代码判定 (点名符号零生产语义引用), 与「未完成」**不是**一回事, 报告里必须分开写 | 否 |
| `complete == true` ∧ `verdict ∈ {pass, warn}` | 调 openspec-archive 归档 | 否 |

归档放行时 D.2 应产出:

```yaml
D.2:
  spec_archived: true
  archive_path: "openspec/archive/add-payment-gateway/"
  gate_verdict: "pass"        # 或 "warn"
```

四步归档动作: 验证 `tasks.md` 全 `[x]` → `proposal.md` status 改 Complete → `changes/add-payment-gateway/` 移到 `archive/add-payment-gateway/` → 记录归档时间与 commit info。

**两条边界, 收尾报告里容易写错**:

- `verdict=warn` 或归档产出 `d_payload` (deferred 未完成项 / `unverified_claims`) 时, frontmatter 写入与 tracker issue 创建**全部由 openspec-archive 自己的 Step 2 / Step 7 完成**。Phase D **不**另建一份 issue —— 双入口会开出重复 issue。本报告的 "next steps" 里因此只写「去看 openspec-archive 开的那条 issue」, 不写「我再开一条」。
- `verdict=block` 时, 本步在报告里写 **BLOCKED** 而非「完成」, 回显 `blocking_reasons`, 且**不**自动带 `--archive-design-only` 绕过 —— 豁免是 owner/AI 的显式决定, phase-d-closer 不代做。D.1/D.3 照常跑, Phase D 整体 `success: true`, 但 `steps_blocked: [D.2]`。

---

## 四、D.2b claim 释放 (advisory, 非阻塞)

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/release_gate.py" \
  --raw-track-id "<A.1 认领时派生的那一串原始 carry-id>" \
  --sweep-stale --gc --repo-path "<repo root>"
```

- carry-id 必须是 **A.1 认领时那一串原始值** (与 Phase B-entry 传给 phase1_gate 的同源, 归一在 CLI 内部完成); 收尾时按 spec 名重新拼一串会 release 不到自己那条, claim 就永久 active 堆积。
- `--sweep-stale` 顺带把全 ref 内 heartbeat 超 STALE_TTL 的 active claim 标 abandoned; `--gc` 归档超 retention 的 done claim。收尾是 GC 的自然挂载点。
- **判读要看两个信号**: exit code 之外还要看 `push_success`。`released.success=true` 但 `push_success=false` ⇒ 只在本地释放, 远端/其他终端仍看到 active claim, 报告里要写「本地已释放, 待下次 fetch/reconcile 收敛」, **不能报成「已释放」完事**。
- `released.error == "claim_not_found"` 是 benign (早已释放 / 从未认领), exit 0, 不算失败。
- exit 1 只记 warning 到本报告, **不阻断** D.3/D.4。

本次: 未认领对应 track ⇒ 只建议跑 `--sweep-stale --gc` (不带 `--raw-track-id`) 做 ref 卫生。

---

## 五、D.3 Session handoff

- **触发** (4 级 fallback, 任一命中即写): session 跨度 > 4h → 自上次 handoff 起 ship ≥ 2 cycles → commit subject 里跨 ≥ 2 个 Phase → 询问 user (D.2 归档成功且 user 在场时默认 yes)。
- **路径硬编码**: `docs/handoff/<YYYY-MM-DD>-<slug>.md`, slug 取 user 提供值 > change_id 后缀 (此处 `add-payment-gateway` → `payment-gateway`) > `session-handoff`; 同日重名退化为 `<YYYY-MM-DD>-<HHMM>-<slug>.md`。**绝对禁止** `.aria/handoff/`。
- **模板**: `aria/templates/session-handoff.md` 9 段骨架 (§0 入口 / §1 已完成 / §2 carry-forward / §3 风险陷阱 / §4 实战教训 / §5 多维度同步状态 / §6 next session 入口 / §7 提交清单+multi-remote parity / §8 memory entries)。
- **写后自校验** (进 latest.md 之前): `head -8 <handoff> | grep -cE '^(track-id|owner-container|phase|status|updated-at):'` 须 == 5; 不足按模板派生规则补齐后重验 (warn-then-fix, 非硬 abort)。`owner-container` **机械填**, 别手拼:
  `python3 aria/skills/session-closer/scripts/handoff_autofill.py --owner-container`
- **latest.md 两个子步骤** —— 这是最常漏的一步:
  - 子步骤 1 History prepend: **always, 任何 cycle 都不可跳过**, 否则本 cycle 在 latest.md 隐形。
  - 子步骤 2 Pointer (`**Latest**:`) 更新: **conditional**。当前这个仓的 `docs/handoff/latest.md` 明确处于 **multi-track** 状态 (在飞 2 条 track, 分属两个 container), 若本 cycle 是 follower scope 就**只做子步骤 1, 不动 pointer**, 把主线 pointer 留给 leader doc。single-track 或本 cycle 即主线时才更新 pointer, 并把前一条改成 "Active (parallel predecessor)"。

---

## 六、D.4 Estimator capture (收尾末位, advisory)

```bash
EST="${CLAUDE_PLUGIN_ROOT:-aria}/skills/ai-native-estimator/scripts/estimator.py"
python3 "$EST" --project-root . capture \
  --spec-slug add-payment-gateway \
  --spec-level <读 openspec/changes/add-payment-gateway/proposal.md frontmatter Level 行> \
  --n-tasks <detailed-tasks.yaml 的 task 数>
```

幂等 (无新 turn ⇒ `{"skipped": true}`, 可安全重跑); 任何失败 (无 transcript / config disabled) 只 skip + warn, 不影响收尾闭环。cycle_id 由 estimator 从 transcript range 末 uuid 生成, 不用传时刻。

---

## 七、时间线

**(a) cycle 时间线** —— 收尾报告要的是这条; 每行都有取值命令, 别凭记忆写:

| 事件 | 值 | 取值 |
|------|----|------|
| A.1 Spec 创建 | `<date> <sha>` | `git log --diff-filter=A --format='%ad %h' -- openspec/changes/add-payment-gateway/proposal.md` |
| B.1 分支创建 | `<date>` | `git log --reverse --format='%ad %h' <branch> ^master \| head -1` |
| C.1 提交 | `<commit_sha>` | Phase C 传入的 context |
| C.2 合并 | `<pr_url>` / `<merge_sha>` | Phase C 传入的 context |
| D 执行 | `<YYYY-MM-DDTHH:MM:SSZ>` | `date -u +%Y-%m-%dT%H:%M:%SZ` (**必须 UTC `date -u`, 不用 `datetime.now()`**) |

**(b) 本次 Phase D 步骤时间线** (实测, 顺序即依赖):

```
D.1   skipped   (UPM 探测 2 路径, 均不存在)
D.post skipped  (config post_closure=off)
D.2   skipped   (gate: complete=false, verdict=pass)  ← 归档未发生
D.2b  advisory  (未认领, 建议仅 sweep/gc)
D.3   pending   (待写 handoff)
D.4   pending   (advisory)
```

---

## 八、机读输出

```yaml
success: true                # D.2 未归档不等于 Phase D 失败
steps_executed: []
steps_skipped: [D.1, D.post, D.2, D.2b]
steps_blocked: []            # 注意: 本次是 skip, 不是 BLOCK
results:
  D.1:
    upm_updated: false
    skip_reason: "no UPM document at either candidate path"
  D.2:
    spec_archived: false
    gate_verdict: "pass"
    complete: false
    complete_reason: "proposal.md not found in openspec/changes/add-payment-gateway — malformed spec dir, gate stays closed"
    blocked: false
    blocking_reasons: []
  D.2b:
    claim_released: null
    note: "本 session 未经 phase1_gate 认领该 track; 建议 --sweep-stale --gc 保持 ref 卫生"
  D.3:
    handoff_written: false   # 待执行
  D.4:
    estimator_captured: false
context_for_next: null       # Phase D 是最后阶段
```

---

## 九、Next steps

1. **先解决 spec 不可解析** (阻塞 D.1+D.2 两步):
   - 核对 change_id 拼写 —— `ls openspec/changes/` 当前是 7 个 change, 无 payment 相关;
   - 或确认应在**另一个仓/另一个 module** 收尾, 换到该 repo root 后重跑同一条 gate 命令;
   - 若目录在但缺 `proposal.md`, 那是 malformed spec dir, 补齐 proposal 后 gate 才会开。
2. **重跑 gate 后按 verdict 分流**: `pass|warn` + `complete=true` → 调 openspec-archive 归档; `complete=false` → 回显 `complete_reason` 并去补未完成任务; `block` → 报 BLOCKED + 回显 `blocking_reasons`, 补齐生产集成后重试, 或由 owner/AI 显式直接调用 openspec-archive 并带 `--archive-design-only` + reason。
3. **若归档时 verdict=warn 或产出 d_payload**: 去 openspec-archive Step 7 自动开的那条 tracker issue 上跟踪 deferred / unverified_claims —— 不要另开一条重复 issue。
4. **D.2b 释放后核 `push_success`**: false 就在 handoff 里写「本地已释放, 待 reconcile 收敛」, 别报成已释放。
5. **写 handoff 并提交**: `docs/handoff/<date>-payment-gateway.md` + latest.md 子步骤 1 (必做) / 子步骤 2 (multi-track follower 则跳过), 然后连同 UPM 变更一起 commit。
6. **下次 session 入口**: `/aria:state-scanner` —— Phase 1.15 会自动 surface 这份 handoff。

---

**说明**: 本报告里 `<...>` 全部是需要从你那轮 cycle 的实际上下文 / 上表命令取值的位置; 我没有替它们编数字。D.1 与 D.2 的「未发生」是实跑判定, 不是省略。

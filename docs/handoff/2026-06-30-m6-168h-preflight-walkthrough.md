---
track-id: m6-168h-preflight
owner-container: simonfish/dev-claude
phase: pre-flight
status: complete
updated-at: 2026-06-30T15:12:17Z
---

# Aria — Session Handoff (2026-06-30) — M6 168h 跑 Phase 0 Pre-flight 走查

> **Next session 入口**: 优先读本 doc → `/aria:state-scanner` → §6 next-step。
> **承接**: `2026-06-30-m6-runtime-remediation-makeready.md` (#147 闭环, M6 make-ready)。
> **会话维度收尾** (session-closer leaf, 非周期收尾): 本 session 未走完整十步循环, 是 pre-flight 验证 + 小 probe artifact ship。

## §0 入口 (新 session 优先读)

1. **本 session 主线**: 起于 `/state-scanner` 等待期扫描 (确认主线全 owner/外部门控) → owner 要求**过一遍 M6 168h 跑的 pre-flight 检查项** → 对 light-1 节点实地核实 Phase 0 → 产出旧 dispatch 只读摘要脚本 → #147 记录。
2. **核心产出**: M6 168h 跑 **Phase 0 pre-flight items 1-5 全绿** (AI 侧前置 100% make-ready, 节点实证), 旧 dispatch corpus 污染**评估为低风险无需清库**, 只读脚本 ship。
3. **剩余 = owner kickoff** (items 6→7→8, 不可 AI 代劳): 选 provenance → 跑 3 次真 dispatch → 验 AC-6 → Day-1 anchor 启动 168h 时钟。
4. trail: 本 doc + #147 `#issuecomment-14055` + runbook `.aria/probes/m6-7d-run-startup-checklist.md`。

## §1 已完成 (按时间顺序)

1. **`/state-scanner` 等待期扫描** (snapshot exit 0, 6/6 custom checks pass): 确认工作区干净, 主线 M6 (owner 168h 运营) + M7 (D3 时机门) 全 owner/外部门控, 无 AI 侧待办阻塞。
2. **M6 168h 跑 Phase 0 pre-flight 走查** (light-1 节点 `root@light-1`, live DB `/opt/aether-volumes/aria-layer1/data/dispatches.db`):
   - **item 1 AC-7**: ✅ 节点 14 连续日 cost 快照 `cost-2026-06-17…06-30.json` (远超 3 日门; 本地 `validate-m6-handoff.py` 报 FAIL 是查本地 `.aria/cost-snapshots/` 的假象, 数据在节点)。
   - **item 2 migration 007**: ✅ 已在 live DB —— `schema_version=5.0` + `is_synthetic` 列在 (非待办, 已应用)。
   - **item 3 schema drift guard**: ✅ `dispatches` 41 列核对含 `is_synthetic`。
   - **item 4 issue_type json key**: ✅ 对齐 —— 生产侧 #28 已部署 (节点 submodule HEAD=`a7afaaa`, `db.py audit_extra` + `extension.py` 从 bug/feature/stale 标签派生 `issue_type_hint`); 消费侧 `acceptance/check-m6-e2e-acceptance.py` `_ISSUE_TYPE_HINT_KEY="$.issue_type_hint"` 同 key。
   - **item 5 abi_compat**: ✅ `validate-m6-handoff.py --check-abi-compat` exit 0 (code-level)。
   - **item 8 旁证**: #146 AC-6 假绿修复 (`_is_unfilled_dispatch_id` + provenance enum) 已部署到节点 acceptance 脚本。
3. **旧 dispatch corpus 污染评估**: live DB 有 **25 旧行** (全 `is_synthetic=0` + 全无 `issue_type_hint`, 都早于 #28): `S_FAIL` ×24 + `S9_CLOSE` ×1 (`dbc9f9118eb00f40`, 2026-05-09); 时间范围 2026-05-03→06-13。判定**风险极低无需清库** —— AC-2 分层无害 (S_FAIL 不算完成 + 无 hint → `json_extract` NULL 不计入), corpus 采样用 `--since <Day-1 anchor>` 时间窗即全排除 (唯一 S9_CLOSE 旧行比 anchor 早 7+ 周)。走 **option (b) 时间窗过滤**。
4. **只读摘要脚本 ship**: `.aria/probes/m6-list-stale-dispatches.py` (stdlib-only, `mode=ro`, 仅取非敏感字段, 支持 `--since` 模拟 anchor 过滤; commit `c271f6e` 双远程 push parity)。
5. **#147 评论** `#issuecomment-14055`: 记录 Phase 0 走查全部结果 (POST comment, 未动 body)。

## §2 未完成 / Carry-forward 清单

### 高优先级 (owner kickoff, 不可 AI 代劳)
- **M6 168h 运营仪式**: 选 provenance (A/B/C, 填 `m6-preflight-provenance.md`) → 跑 3 次 pre-flight dispatch (真 LLM ≤$6, 填 `m6-preflight-log.md`) → 验 AC-6 + 人眼确认 dispatch_id 真值 → 落 Day-1 alloc anchor (启动时钟) → 每日 probe + Day-3 闸 → corpus 采集 + owner 7 维评分 (AC-5 median≥7) → acceptance gate → 归档 #2 → 起 #4 release-closeout。

### 中优先级
- **item 4 live e2e**: `issue_type_hint` 真实写入待**首个 #28 后新 dispatch** 验证 (旧 25 行无此 key 符合预期; pre-flight dispatch 即会产出第一条可验)。
- **corpus 采样过滤**: Phase 4 采样务必 `--since <Day-1 anchor>` (option b 已定), 排除 25 旧行。
- **B2 Feishu WS 稳定性观察** (carry from makeready): gateway 重启后 WS 连 `msg-frontier.feishu.cn` 稳定仅观察 3+ min; owner 留意是否保持, 再现 keepalive 掉线 → 查 conntrack。

### 机械补漏 (autofill backstop, 非本 session 工作)
- `aria-2.0-m6-e2e-resilience` `tasks.md` 多个未勾选项 —— 已知: 代码侧完成, tasks.md 待 168h 跑 + corpus 后才勾。非本 session 遗漏。

## §5 四维一致性 (consistency_check)

- 4 个 advisory `active_change_not_in_upm` (m6-e2e-resilience / m6-release-closeout / m7-agent-lifecycle / m7-fleet-aggregation 未列入 UPM in-progress) —— **已知 false-positive**: Aria 是方法论项目**无 runtime UPM** (`upm.configured=false`, memory `project_aria_no_runtime_upm`)。无真实漂移。
- `aria-2.0-m6-release-closeout` design_deferred (41/41 unchecked, 35d): **合法在飞** sequential Spec, 按设计等 #2 运营证据, 非黑洞。

## §6 Next-step (优先级排序)

1. ⭐ **owner kickoff M6 168h 跑** — runbook Phase 0 收尾 (items 6→7→8) → Phase 1 落 Day-1 anchor。AI 侧前置全清。
2. (跑期) 协助每日 probe / Day-3 闸评估 / corpus 采样 (用 `m6-list-stale-dispatches.py --since` 验过滤)。
3. (等待期可选) 无新纯-AI issue 候选; 主线推进全 owner-gated。

## §7 同步状态 (handoff_autofill)

```
[main]              master = c271f6e | github=equal origin=equal
[standards]         master = 350a7cf | github=equal origin=equal
[aria]              master = daa3945 | github=equal origin=equal
[aria-orchestrator] master = a7afaaa | origin=equal
```
全 parity equal, 无 pending push。本 session 1 commit (`c271f6e`) 已双远程推送验证。

## §8 Memory entries

本 session **无新 memory** —— 学到的均已被既有覆盖, 不重复固化:

```
[候选 memory]
- (无) 本 session 经验均已被既有 memory 覆盖:
  · pre-flight 须对 live 节点状态核实 (非信本地/信"已部署") → [[feedback_verify_agent_diagnosis_against_live_state]]
  · 节点 git pull + pip editable 部署路径 + forgejo SSH deploy key → [[reference_forgejo_ssh_node_deploy_key]]
  · 区分 AI 可做的 make-ready prep vs owner kickoff (不代触发烧预算动作) → [[feedback_experiment_start_action_not_generic_prep]]
[未写下经验]
- (一次性技巧, 不值固化) 节点上解析 pip editable 源: 读 `__editable__*.pth` → finder.py 的 MAPPING dict 取真实 source 路径, 再 grep / git HEAD 核验部署代码。
- (方法论, 已隐含在 advisory-over-hardlock) 存量脏数据处置优先非破坏性时间窗过滤 (option b), 仅当 provably out-of-window 才免 DELETE。
```

---

> **会话收尾说明**: 本 handoff 由 `session-closer` (leaf skill) 写出 —— owner "执行对话收尾" 命中会话维度收尾 (非 phase-d-closer 周期收尾)。AI 内省 (§1/§2/§8) 优先 + 机械 autofill/consistency 交叉补漏 (§5/§7)。未发起任何 phase-a/b/c/d 调用 (leaf 终结)。

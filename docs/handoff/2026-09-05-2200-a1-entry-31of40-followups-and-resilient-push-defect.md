---
track-id: a1-entry-claim-duplicate-work-guard
owner-container: simonfish/023236f2
phase: B.2
status: active
updated-at: 2026-09-05T22:02:46Z
---

# Aria — Session Handoff (2026-09-05, 会话收尾 #2) — 母 Spec 31/40: 8.3 开单 8 条 + 撞出 `resilient_push` 结构缺陷

> **一句话**: 本对话从 `/aria:state-scanner` 起 → owner 选「选项 1」→ B.0 heartbeat dogfood (**当场撞出并复现一个结构缺陷**) + M3 行号复核 (9/9 全中, 无需改) + M4 五处验收项只增不改订正 → 三仓 feature 分支双推 6/6 MATCH → owner「1 和 2 都做」→ **TASK-039 (8.3) follow-up 开单 8 条 + 新缺陷 1 条 = 9 条** → 会话收尾 (本 doc)。**30/40 → 31/40**。
> **本 session 最该记住的一件事**: dogfood 自己刚实现的 `--heartbeat-only` 时 push 报 non-FF, 我顺手跑了一条强制 fetch 想看远端 —— **那一下把刚写好的 heartbeat commit 冲掉了**。追进去发现 `resilient_push` 的 non-FF 恢复路径犯的是同一个错的镜像版本, 而且**结构上每次触发都只能失败**。跑了离线三态负控确认, 开成 aria-plugin#169。**一个手滑和一个 ship 了很久的缺陷, 是同一个形状。**

---

## §0 入口 (新 session 优先读)

1. 三仓仍在 **feature 分支**且**都已推**: 主仓 `feature/a1-entry-claim-duplicate-work-guard` @ `5ee2d26` (origin/github 两端 MATCH) · aria 同名分支 @ `ab3dbd0` (两端 MATCH) · standards 同名分支 @ `bb5d375` (两端 MATCH)。`git status` 应见 ` M aria`, ` M standards`, ` M aria-orchestrator` 三个 dirty 子模块 —— **全部有意**, 不要 `git add` (gitlink bump 归 TASK-038/8.2, 要等各自合 master 之后)。
2. **claim heartbeat 已刷到 `2026-09-05T21:40:06Z`**, sweep 死线 **2026-09-06T21:40Z**。下次进 `/state-scanner` 按新文档再跑一次 `--heartbeat-only` 即可 (命令见 §3 第 4 条)。
3. **Rule #6 AB 仍未跑, 且仍不是豁免** —— 本 session 实测 `ARIA_COORDINATION_NO_PUSH` **UNSET**, 会话内补不上。见 §3 第 1 条。
4. **7.6 (TASK-036) 本 session 明确没做**, 依据见 §3 第 2 条 —— 不是漏了, 是 Spec 依赖不允许。若你判断可以放行, 请显式说, 我不自行改序。
5. 硬约束不变: 子模块推送须 owner 逐条授权; 禁带圈数字 (memory `no-tiny-glyphs`)。
6. 多 track: 本仓另有 `aria-2-0-m6-dispatch-input-delivery` (aria-runner-bot/bfe8285d) 在飞; 另发现 `owner-container-identity-key-and-collision-parser` (同容器, 关联 Aria#193) **09-05 13:55Z 新认领**, 与本轨无交集但与新开的 aria-standards#19 主题相邻 —— 见 §3 第 5 条。

---

## §1 已完成 (本对话, 按时间顺序 UTC)

| 时间 | 事项 | 落点 |
|------|------|------|
| 15:01 | `/aria:state-scanner` 全量扫描 (exit 10, 1 条 AC-5 软错误) → 10 区块报告 + 4 选项 | — |
| 15:2x | owner 选**选项 1**。B.0 `--heartbeat-only` dogfood: 首跑 push 报 `non_ff` → 我手工 `+` 强制 fetch **把本地 heartbeat `6472f81` 冲掉** → 先 fetch 再重放, 二跑 `push_success: true`, `ls-remote` MATCH | `refs/aria/coordination` |
| 15:3x | **M3 行号复核**: 先写预期再实测, **9/9 全中** (`phase1_gate.py` 1566 行 / `collision.py` 四门锚点 / `claim_lifecycle.py` 四锚点 + `heartbeat_by_track:475` 在其后)。按 `tasks.md:7` 成文约定 **proposal.md 正文不改**, 只补一行复核留痕 | 主仓 |
| 15:4x | **M4 五处验收项订正** (只增不改): TASK-006/008/013/021 四处结构上不成立 + TASK-014 deliverable 与 proposal 三处口径矛盾。YAML 解析完好 (40 tasks), diffstat 恰 `+5/−1`, 零 CRLF 污染 | `4b02552` |
| 21:4x | owner 定推送范围 = 三仓双推。standards / aria / 主仓依次 push origin+github, **逐 remote `ls-remote` 6/6 MATCH** | 三仓 |
| 21:4x | 二次 heartbeat (先 fetch 后写, 顺序修正) → `21:40:06Z`, MATCH | `refs/aria/coordination` |
| 21:5x | owner「1 和 2 都做」→ **开单前先 fetch 四仓看板核重复** (aria-plugin 34 / Aria 25 / aria-orchestrator 2 / aria-standards 4) → **9 条 issue**, 全部经独立 GET 核验 open 且正文非空 | 见 §2 表 |
| 21:5x | 8.3 回写 Spec (tasks.md 表 + yaml TASK-039 done + b2_evidence), **31/40** | `5ee2d26` |
| 22:0x | 会话收尾 (本 doc) + memory 2 新 1 追记 | — |

**规模**: 主仓 2 个提交 · 9 条 issue · 30/40 → **31/40** · 三仓六条 push 全 MATCH · memory +2。

---

## §2 未完成 / Carry-forward

> cycle **未完成** (31/40)。机械 autofill 对本 Spec 汇编出 9 条未完成, 与我的内省**逐条吻合, 零补漏项**。

### 高优先级 — 本 cycle 剩余 9 条

| # | 项目 | 状态 |
|---|------|------|
| **H1** | ⛔ **Group 7 跑评测半 (7.1/7.2/7.4 + 7.3·7.5 后半)** —— 阻塞于会话级前置, 见 §3 第 1 条。处置 = owner 以 `ARIA_COORDINATION_NO_PUSH=1 claude ...` 重启会话后经 `/skill-creator` 跑六个套件 (`phase-a-planner` / `spec-drafter` / `state-scanner` / `phase-b-developer` / `branch-manager` / `phase-d-closer`), 结果落 `ab-results/2026-XX-XX-v1.70.0-a1-entry-rule6/<skill>/` (每目录跑前先写 `PREDICTION.md`)。跑完**必做**手册第 3 条 `git fetch origin +refs/aria/coordination:refs/aria/coordination` | 阻塞 |
| **H2** | **7.6 套件缺口 issue (TASK-036)** —— **本 session 没做, 且不是遗漏**: yaml `dependencies: [TASK-035]`, tasks.md 行尾也写着「按 Spec 它依赖 7.5 跑完」。现在开 = 改序 (Rule #10)。**若 owner 判断可放行请显式说** | 依赖阻塞 |
| **H3** | Group 8 发版三条 (8.3 已 done): 8.1 CHANGELOG + 版本 SOT 5 文件 (`<vNEXT>` = **1.70.0**) → 8.4 aria 本地 merge + 双推 + 逐 remote 核验 + tag → 8.2 主仓 16 版本点 + gitlink bump。**执行序 8.1 → 8.4 → 8.2** | 待 AB 过关 |

### 中优先级 — 溢出项

| # | 项目 | 备注 |
|---|------|------|
| M1 | ✅ **已闭环** — 8.3 follow-up 开单 8 条 (见下表) | 本 session 完成 |
| M2 | **`issue_scan.open_count` 静默截断** —— 本轮再次实测复现: snapshot 报 **46**, 四仓 API 实拉合计 **65** (aria-plugin 34 / Aria 25 / aria-orchestrator 2 / aria-standards 4)。config `limit=20`, 而 Aria 与 aria-plugin 恰好各报 20 = 顶到上限且**零截断标记** | **仍未开单**; 与 #182/#173「证据越少越宽松」同族 |
| M3 | ✅ **已闭环** — 行号复核表实测 9/9 全中, proposal.md 按 `tasks.md:7` 成文约定不改 | 本 session 完成 |
| M4 | ✅ **已闭环** — 五处验收项只增不改订正 (原条款保留, 追加「⚠️ 订正」条) | 本 session 完成 |
| M5 | **`resilient_push` 缺陷已开单未修** (aria-plugin#169) —— 影响 `acquire_claim` 与 `heartbeat` 两条写路径 | 见 §3 第 3 条 |
| M6 | **长等待期间的 heartbeat 盲窗** —— 本 session 因 `AskUserQuestion` 等了 6 小时 (15:28Z→21:38Z), 期间 claim 无人刷新。这是 aria-plugin#168 (audit-engine 轮内不触发) 的**兄弟场景**, 但宿主不同 (AI 编排层的长等待点)。建议并入 #168 或另开 | 未开单 |
| M7 | 上轮原样: Aria#192 真修 / AB 套件断言补强 / Aria#182 类级修 / `.aria/repro/` 测试不在任何 gate 路径 | 09-05 前一份 handoff §2 |
| M8 | **Aria#195 新出现** (state-scanner: `handoff_multibranch` 递归枚举但只留 basename, 子目录下的 handoff 必然 `git show` 失败) —— 本 session 未处理 | 他方开单 |

### 本 session 开出的 9 条 issue

| follow-up | issue | 去处 |
|---|---|---|
| #1 `owner-container` 口径统一 | [aria-standards#19](https://forgejo.10cg.pub/10CG/aria-standards/issues/19) | standards (handoff frontmatter 规范) |
| #2 `SWEEP_TTL`→`STALE_TTL` 三处措辞 | [aria-plugin#163](https://forgejo.10cg.pub/10CG/aria-plugin/issues/163) | aria-plugin |
| #3 `unknown_schema_claims` 路径/身份 | [aria-plugin#164](https://forgejo.10cg.pub/10CG/aria-plugin/issues/164) | aria-plugin |
| #4 B.0 YAML-键形态 | [aria-plugin#165](https://forgejo.10cg.pub/10CG/aria-plugin/issues/165) | aria-plugin |
| #5 `unattended` Layer 1→2 env 三腿契约 | [Aria#196](https://forgejo.10cg.pub/10CG/Aria/issues/196) | Aria 主仓 |
| #6 跨容器定向 release | [aria-plugin#166](https://forgejo.10cg.pub/10CG/aria-plugin/issues/166) | aria-plugin (D6 权限面) |
| #7 `ClaimRecord` swept 标记 | [aria-plugin#167](https://forgejo.10cg.pub/10CG/aria-plugin/issues/167) | aria-plugin |
| #8 audit-engine 轮间 heartbeat (§2.2) | [aria-plugin#168](https://forgejo.10cg.pub/10CG/aria-plugin/issues/168) | aria-plugin |
| **(不属 TASK-039) `resilient_push` non-FF 恢复路径结构必失败** | [aria-plugin#169](https://forgejo.10cg.pub/10CG/aria-plugin/issues/169) | aria-plugin |

### 机械补漏 (autofill backstop, AI 内省未提及)

- `handoff_autofill.py` 对本 Spec 汇编出 9 条未完成 (7.1-7.6 + 8.1/8.2/8.4), **与内省逐条吻合, 无补漏项**。另 134 条属 M6/M7 各 Spec, 本 session 未触及。
- `sync` 段**零告警**: 三仓两端全 `equal` (aria-orchestrator github `unknown` = 另一轨的分支, 非本轨)。
- `consistency_check.py`: 7 条 `active_change_not_in_upm` advisory —— UPM 未配置导致的恒亮 flag (Aria#188 在册), 与本 session 无关。

---

## §3 关键风险 / 已知陷阱

1. **⛔ AB 运行前置是会话级的, 在会话内补不上 (本 session 再次实测确认)。** `ARIA_COORDINATION_NO_PUSH` 实测 **UNSET**; 会话内 `export` 只影响那一个 Bash 子进程, 改不了 subagent 的继承环境。硬跑的后果成文且有实证 (被测 Skill 会把合成 claim 推到生产 `refs/aria/coordination`)。**这不是 Rule #6 豁免** —— 本批改了 `allowed-tools` (能力面扩权), 照跑档不变, 只是执行条件不具备。

2. **7.6 的不做是有依据的, 不要当成遗漏补掉。** owner 已授权「开单」, 但授权解的是「能不能做」, Spec 的 `dependencies` 解的是「**现在**能不能做」—— 两者正交。TASK-036 的 `dependencies: [TASK-035]` 明写依赖 7.5 跑评测半, 后者阻塞。已落 memory (`no-self-exempt-gates` 追记)。

3. **`resilient_push` 的 non-FF 恢复路径结构上必失败** (aria-plugin#169, 本 session 实撞 + 离线三态负控)。
   - push 报 `non_ff` ⟺ 本地与远端**分叉**; 恢复路径调的 `fetch_coordination_ref` (`lib/coordination_ref.py:1339`) refspec **无 `+`** ⇒ 分叉必被 reject ⇒ 只能返回 `fetch_replay_failed`。
   - **改成强制也不对**: 循环体只是「再 push 一次」, 不重放本地 claim 写入; 强制 fetch 后 local == remote, 重 push 是 no-op ⇒ claim 静默丢失。函数名承诺的 `fetch-replay-repush` 里**没有 replay**。
   - **fail-soft 文案方向反了**: 「local refresh stands, remote converges on next fetch」—— 下一次 fetch 恰恰是销毁它的那一步 (本 session 亲手复现)。
   - 影响面: `acquire_claim` + `heartbeat` 共用。多容器并发写协调 ref 时 claim 静默丢失, 而多容器并发正是 Layer L 存在的理由。

4. **heartbeat 的正确调用顺序是「先 fetch 再刷」**, 不是「刷了再 fetch」:
   ```bash
   git fetch origin '+refs/aria/coordination:refs/aria/coordination'
   python3 -B aria/skills/state-scanner/scripts/phase1_gate.py \
     --raw-track-id "a1-entry-claim-duplicate-work-guard" \
     --phase B --heartbeat-only --repo-path /home/dev/Aria
   ```
   顺序反了会被强制 fetch 冲掉 (已实证)。落 memory `fetch-then-write`。

5. **aria-standards#19 与 Aria#193 主题相邻, 且 #193 上有容器在制。** `owner-container-identity-key-and-collision-parser` (owner `aria-runner-bot`, 容器 `bfe8285d`, 09-05T13:55Z 认领, linked_issue `10CG/Aria#193`)。#19 是同一问题的 **standards 规范侧** (落点不同), 已在 issue 正文点名请交叉核对。**动 #19 前先看对方进度**, 别重复实现。

6. **本轮 scan.py `exit=0 / errors=[]`, 而同日 15:01 那轮是 `exit=10` + AC-5 inconclusive** —— 唯一变化是 feature 分支这次已推到 github。这是 **Aria#176 (AC-5 未排除本仓不存在的 remote) 形状的旁证**: 分支在某 remote 上不存在时 git 命令失败, 而 `overall_parity` 仍报 `true` 且无 reason。#176 已在册, 此处仅补一条实证。

---

## §4 实战教训 (memory 沉淀来源)

```
[候选 memory — 本 session 已落盘]
- 本地 ref 有未推 commit 时再 fetch 会覆盖它: 强制 refspec 直接重置到远端 SHA, 非强制则因分叉被
  reject —— 两条路都保不住本地写入。顺序必须 fetch-then-write。同日双向实证 (我手工冲掉 heartbeat ·
  resilient_push 同款结构缺陷 #169)。 ✅ 已写 feedback_fetch_after_local_write_destroys_unpushed_ref
- 交接 carry-forward 的散文可能与 Spec 成文约定相反 —— M3 说「proposal.md 行号未同步, 应扫一遍」,
  而 tasks.md:7 逐字写着「不改 proposal.md」。照交接做就违反 Spec 自己的约定, 且改动看起来完全合理。
  ✅ 已写 feedback_handoff_carryforward_can_contradict_spec_convention
- owner 授权做一批外向动作 ≠ 那批里每条现在都能做; 授权解「能不能做」, dependencies 解「现在能不能做」。
  ✅ 已追记进 feedback_ai_must_not_self_exempt_enabled_gates

[未写下经验]
- 「读代码看不出问题, 跑三态负控才现形」这次的对象是**别人早已 ship 的兜底路径** —— 与
  check-runs-at-baseline-first (自己新写的检查) 和 spec-acceptance-needs-baseline-run (审过多轮的
  规格) 同族, 缺的是第三个对象格: **在场很久、从没在它自己的触发场景下被跑过的兜底分支**。
  判据: 「这条 except / retry / fallback 分支, 有没有人在它真正会被触发的那个条件下跑过一次?」
  值得追记进 check-runs-at-baseline-first, 但本 session 没做。
- 长等待 (AskUserQuestion 6 小时) 是一个 heartbeat 盲窗, 与 audit-engine 轮内盲窗同形不同宿主。
  已记为 §2 M6, 但没开单也没落 memory。
```

---

## §5 多维度同步状态

| 维度 | 状态 |
|---|---|
| OpenSpec | `a1-entry-claim-duplicate-work-guard` **31/40** (TASK-039 done), 仍 active (未归档, cycle 未完成)。活跃变更 7 / 已归档 142 / 待归档 0 |
| UPM | 未配置 ⇒ `consistency_check` 7 条 `active_change_not_in_upm` 恒亮 advisory (Aria#188), 与本 session 无关 |
| User Story | 本 cycle 无 US 变更 (21 条: done 17 / in_progress 2 / approved 1 / pending 1) |
| PRD / 架构 | 无变更 (发版时 8.2 会动主仓 16 版本点与架构文档版本行) |
| 自定义检查 | 14/14 OK (0 FAIL / 0 STALE) |
| 审计 | 上次 `pre_merge` R5 PASS (2026-09-02), `converged=false`; 本 session 未触发新审计 |

---

## §6 Next session 入口 + 优先级建议

```bash
/aria:state-scanner
```

1. ⭐ **`{id: a1-entry-claim-duplicate-work-guard}`** —— 本 cycle 续做, **31/40**。**先决**: owner 以 `ARIA_COORDINATION_NO_PUSH=1 claude ...` 重启会话跑 Rule #6 AB (H1)。AB 过关 → 7.6 依赖解除 (H2) → Group 8 发版 (`<vNEXT>` = **1.70.0**, 执行序 8.1 → 8.4 → 8.2)。进入前先按 §3 第 4 条刷一次 heartbeat。
2. **`{id: carry-issue-scan-open-count-truncation}`** —— M2: `open_count` 静默截断 (本轮实测 46 报 vs 65 实), 开单或直接修。
3. **`{id: carry-resilient-push-non-ff-recovery}`** —— aria-plugin#169 已开单, 修复面在 `lib/failure_handlers.py` + `lib/coordination_ref.py:1339`, 影响 claim 两条写路径, 优先级不低。

---

## §7 提交清单 (commit hash + multi-remote parity)

| 仓 | 分支 | SHA | origin | github |
|---|---|---|---|---|
| Aria (主仓) | `feature/a1-entry-claim-duplicate-work-guard` | `5ee2d26` | ✅ MATCH | ✅ MATCH |
| aria-plugin | 同名 | `ab3dbd0` | ✅ MATCH | ✅ MATCH |
| aria-standards | 同名 | `bb5d375` | ✅ MATCH | ✅ MATCH |
| aria-orchestrator | `feature/m6-cost-model-telemetry` | `92acce5` | ✅ equal | unknown (另一轨, 本 session 未动) |

本 session 主仓两个提交:
- `4b02552` — `docs(a1-entry): 归档前复核 — M3 行号表实测全中 + M4 五处验收项只增不改订正`
- `5ee2d26` — `docs(a1-entry): TASK-039 (8.3) 完成 — follow-up 开单 8 条 + 新发现 1 条, 31/40`

协调 ref: `refs/aria/coordination` heartbeat `21:40:06Z`, `ls-remote` MATCH。三个子模块指针**有意保持 dirty** (gitlink bump 归 8.2)。

---

## §8 Memory entries this session (2 new + 1 追记)

- **新增** [`feedback_fetch_after_local_write_destroys_unpushed_ref`](file) — 本地 ref 有未推 commit 时再 fetch 会覆盖它; 顺序必须 fetch-then-write
- **新增** [`feedback_handoff_carryforward_can_contradict_spec_convention`](file) — 交接散文可能与 Spec 成文约定相反; 动手前先去 Spec 找成文约定
- **追记** `feedback_ai_must_not_self_exempt_enabled_gates` — 授权 ≠ 依赖已满足 (同族反方向)
- **索引维护**: MEMORY.md 24402 → 24324 bytes (移 `postplan-blindspot` 四条组行 + `dev-env-npm-path` 入 archive 腾位)

---

## Cross-references

- 前一份 handoff: [2026-09-05-1426-a1-entry-b2-30of40-rule6-blocked.md](./2026-09-05-1426-a1-entry-b2-30of40-rule6-blocked.md)
- Spec: `openspec/changes/a1-entry-claim-duplicate-work-guard/` (proposal.md / tasks.md / detailed-tasks.yaml)
- 本轨 linked issue: [Aria#174](https://forgejo.10cg.pub/10CG/Aria/issues/174) · 相关 [aria-plugin#135](https://forgejo.10cg.pub/10CG/aria-plugin/issues/135)
- 本 session 新开 9 条 issue: 见 §2 表
- AB 手册: `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` §场景 1

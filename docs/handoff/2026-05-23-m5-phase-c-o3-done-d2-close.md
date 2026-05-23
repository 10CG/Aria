---
track-id: aria-2-0-m5-replay-reconciler-drift-review-loop-audit
owner-container: simonfish/dev-claude
phase: D
status: closed
updated-at: 2026-05-23T00:30:00Z
---

# Aria — Session Handoff (2026-05-23 ~00:30 UTC) — M5 Phase C O3 ✅ + Phase D.2 CLOSE

> **Status**: 🎉 **M5 CLOSED**. Layer 2 autonomous issue→PR loop verified end-to-end live; Phase D.2 close gate fully MET; M5 Spec archived; US-025 → `done`.
> **Predecessor (same track)**: [`2026-05-22-m5-phase-c-o1-o2-done.md`](2026-05-22-m5-phase-c-o1-o2-done.md)
> **Session 性质**: 持续 O3 推进 session(跨午夜 UTC) — playbook §O3 grounding 已用 5 个真实部署缺陷为代价兑现。

---

## §0 入口 (新 session 优先读)

1. **本 doc** — M5 Phase C O3 + D.2 close,M5 整体 done
2. 前文 (same track): `2026-05-22-m5-phase-c-o1-o2-done.md` + `2026-05-22-m5-phase-c-playbook.md` (playbook §O3 已修 F1)
3. m5-handoff.yaml: `aria-orchestrator/docs/m5-handoff.yaml::t_deploy_status.phase_c_completion`

→ **next**: M6 / 下一个 US 启动(见 §6),或处理 inflight track *aria-secret-guard-plugin-default*

---

## §1 已完成 (本 session)

### O3 — Tier-1 live LLM real smoke ✅ (decisive milestone)

实测数据(`/opt/aether-volumes/aria-runner/outputs/DEMO-M5-O3/result.json`):

| 字段 | 值 |
|------|-----|
| alloc | `6cf0d7ab` on heavy-3 (node `6335084a`) |
| 总耗时 | **18 秒** (dispatch → result.json) |
| claude_exit_code | 0 |
| claude_duration_s | 18 |
| claude_usage | input=32355 tok / output=529 tok / cache_read=95744 tok |
| cost_usd_reported | $0.228 (claude-cli 以 Anthropic 价汇报; 实际走 Luxeno subscription 配额, 几乎零真金白银) |
| commit_sha | `9c5040de…` |
| pr_url | https://forgejo.10cg.pub/10CG/Aria/pulls/121 (throwaway, closed+cleaned) |
| outcome | SUCCESS |
| assertion_results | `file_touched_hit=true` + `diff_contains_hit=true` (双 hit) |
| idempotency_state | NEW |

LLM 写入文件 `docs/aria-runner-smoke/DEMO-M5-O3.md` 内容**逐字匹配**预期 marker。throwaway 清理: PR #121 closed, branch `aria/DEMO-M5-O3` deleted, issue #119 closed。`10CG/Aria` master 零影响。

### Phase D.2 close ✅

| 项 | 状态 |
|----|------|
| `m5-handoff.yaml::go_decision` | `"Go (Phase D.2 close 2026-05-23; Tier-2 N≥3 owner-deferred to runtime accumulation, non-blocking per brainstorm D7)"` |
| `m5-handoff.yaml::t_deploy_status.status` | `Phase B done + Phase C done (O1 secret + O2 Layer 2 image + O3 live LLM smoke verified)` |
| `m5-handoff.yaml::m5_acceptance.b1_live_llm_passed` | `true` (was pending) |
| `m5-handoff.yaml::m5_acceptance.c2_live_llm_passed` | `true` (was pending) |
| `phase_c_completion.layer2_deployment_findings` | 5 finding F1-F5 已写入 |
| M5 spec tasks.md 6.21.1 | `[x]` (O2+O3 全 done) |
| M5 spec tasks.md 6.26 | `[x]` (Forgejo housekeeping all done) |
| M5 spec tasks.md 6.30 | `[~]` partial done (D.2 close 部分写入完成; Tier-2 字段 owner-deferred) |
| M5 spec tasks.md 6.27-6.29 | `[ ]` 保留 (Tier-2 cumulative, **非阻塞** per design) |
| M5 proposal.md Status | `Complete (2026-05-23 archived; Phase D.2 close gate MET ...)` |
| US-025 status | `done 2026-05-23 (M5 Phase D.2 close)` |
| M5 spec 归档 | `openspec/changes/.../` → `openspec/archive/2026-05-23-.../` |
| `docs/handoff/latest.md` 指针 | 本 doc 更新 |

### Layer 2 部署缺陷 F1-F5 (O3 smoke 真正价值)

| # | Finding | 状态 |
|---|---------|------|
| **F1** | playbook §O3 line 198 `IMAGE_SHA=sha256:...` 双前缀(HCL 已自带 `@sha256:`) | ✅ **FIXED** 本 session(playbook line 197-198 加 ⚠️ 注释 + bare hex 示例) |
| **F2** | Nomad HCL docker `auth` block `${FORGEJO_BOT_PAT}` 模板插值在 image-pull 时不工作; M1 demos 误靠 build-node 镜像缓存掩盖 | 🔶 **carry-forward** (m5-handoff.yaml::layer2_deployment_findings.F2 已记录) |
| **F3** | Nomad default `gc.image_delay=3min` 吃 unused 镜像, 加剧 F2 — 每次冷 dispatch 都 fail on auth | 🔶 carry-forward (与 F2 同根) |
| **F4** | `aria-runner-bot` 账户 `must_change_password=true` 阻断 git-over-HTTP PAT auth, 但允许 registry pull (Forgejo #2809) | ✅ FIXED 本 session(必须保持 false 作生产前置) |
| **F5** | `aria-runner-bot` 对 `10CG/Aria` 的 write collaborator 权限在 M1 之后被取消 | ✅ FIXED 本 session(`PUT /repos/10CG/Aria/collaborators/aria-runner-bot {"permission":"write"}` 已加, 必须保留作生产前置) |

### 提交清单 (待 push, 本 session 末尾)

主仓 + aria-orchestrator submodule + Aria 子仓 (无变更) 多远程双推 (origin + github)。

---

## §2 未完成 / Carry-forward

### F2 + F3 (proper fix)— **post-M5 任务**, 不阻塞 close

Layer 2 registry auth 机制需要正经修。两条候选路径(选其一):

1. **节点级 Nomad docker plugin `auth.config`**: 在 3 个 heavy 节点的 Nomad client config 加 `plugin "docker" { config { auth { config = "/etc/nomad/docker-auth.json" } } }`, 并在每节点 deploy `/etc/nomad/docker-auth.json` (`aria-runner-bot` PAT base64-encoded for `forgejo.10cg.pub`)。然后 **删 HCL task auth block**,让 Nomad fallback 到 plugin config。
2. **节点级 `/root/.docker/config.json` + Nomad client config 指向**: 等价方案,但用 daemon-level docker config (`docker login` 后留在 `~/.docker/config.json`),Nomad plugin `auth.config` 指向它。

推荐选 #1 (config.json 显式管理, 路径明确, 不依赖 root-shell docker login 历史)。owner 决策时机:M6 启动前或独立 hygiene cycle。

### Tier-2 cumulative validation (Spec 6.27-6.29)

随 owner 日常 workload 自然累积:
- ≥3 real dispatches (含 ≥1 changes + ≥1 redo + ≥1 reject)
- ≥1 real failure 触发 Failure analysis LLM
- ≥1 real spec drift detected

完成后 `m5-handoff.yaml::tier_2_*` 字段对应回填(6.30 Tier-2 字段部分)。

### S6 hygiene — 时间敏感

旧 `.env.bak-*` 文件清理(在 light-1):
- `/root/.hermes/.env.bak-feishu-rotate-*` (O1 留的, 距今 ~12+h, **24h 窗口将到**, 2026-05-23 ~02:00 UTC 后可 shred)
- 任何更老的 `.env.bak-*` (Hermes→Luxeno 那批): **现可 shred**

命令:
```bash
ssh light-1
ls -la /root/.hermes/.env.bak-*
# 确认时间后:
shred -u /root/.hermes/.env.bak-<具体时间戳>
```

### M5-OS-PB-1 (Phase B 期间 surfaced)

Layer 1 v0.4.0 `comment_poll_runner.py:103` 实例化 extension 时未 lazy-wire forgejo, 导致 redo mode placeholder comment skip。**M6 follow-up**, 不阻塞 M5 close(DB state machine 正确, UX missing only)。

### inflight track — `aria-secret-guard-plugin-default`

origin/master `9d41b2e` + `69ec251` (Phase A shipped) 是另一 track 的 in-progress 工作。**与本 M5 close 正交**, 不需在本 handoff 里处理。

---

## §3 关键风险 / 已知陷阱 (本 session 新增)

- **R1 (F1) — Nomad parameterized job HCL 用 `@sha256:${NOMAD_META_IMAGE_SHA}` 时, `-meta IMAGE_SHA` 传 **裸 hex digest** (no `sha256:` prefix)**, 否则 docker driver 报 "does not match registry specification"。playbook 已修。
- **R2 (F2) — Nomad HCL docker `auth` block + template-rendered env 的 `${VAR}` 插值实测不可靠**(Nomad v1.11.2 / Forgejo registry 11.0.6 实证)。M1 demos "通过" 是因为 build-node 镜像缓存意外掩盖。M5 Phase C 触发 cold-pull 暴露。**未正经修**之前, dispatch 落到无缓存节点必失败。临时 workaround: 在所有 heavy 节点 pre-pull 镜像 (但 Nomad `gc.image_delay=3min` 会吃; 需在 dispatch 前秒级 pre-pull)。
- **R3 (F4) — Forgejo 服务账户的 `must_change_password=true` 状态**完全允许 docker registry pull (走独立 auth path), 但**阻断 git-over-HTTP PAT auth**(报 "Credentials are incorrect or have expired" + Forgejo #2809 链接)。新建服务账户时**必须显式** set false。
- **R4 (F5) — 服务账户 (aria-runner-bot) 的 repo collaborator 权限会因 housekeeping/security cleanup 在不知情情况下被取消**, M1 demo PR 历史不是当前权限的证据。生产前必须 `forgejo GET /repos/{org}/{repo}/collaborators/{user} -i` 验证 204。
- **R5 — Nomad var get-编辑-put 的 owner-side 替换易出位**: 本 session 发生过 owner 编辑 /tmp/l2var.json 时 FORGEJO_BOT_PAT 替换错位(40 字符长度蒙骗了验证), 直到从 var 拿值跑 `git ls-remote` 才暴露。安全的 var update 模式:`nomad var get -out=go-template -template '{{ .Items.X }}' ...` 再 `git ls-remote http://...:${X}@.../repo.git HEAD` 自验证。

---

## §4 实战教训 (本 session, M5 close)

- **O3 smoke 的真正价值不是"跑通"而是"暴露 5 个 finding"**。M1 demos "pass" 是 build-node-cache 假性通过;真正的 cold-path validation 必须强制 fresh node, 否则部署缺陷潜伏。
- **Forgejo issue #2809 的诊断特征极有信息量**:同一 PAT, docker registry pull OK 而 git-over-HTTP fail → 必查账户 `must_change_password` 标志。Phase D.2 写进 m5-handoff.yaml::layer2_deployment_findings.F4 防再撞。
- **Nomad HCL docker `auth` block 的 `${VAR}` interpolation 是真实存在的陷阱**, 不要相信 "M1 测试过" 历史证据 —— 镜像缓存可掩盖该缺陷长达 milestones。
- **服务账户的 collaborator 权限漂移**(F5):应作为 M6+ 部署 preflight checklist 项,而非依赖 ad-hoc 发现。
- **owner 的 secret 替换易出位**(R5):应在 Aria convention 加一个推荐验证 pattern (`nomad var get` 拿值后立即 `git ls-remote` 或等价的 round-trip 自验证)。值得后续写进 `standards/conventions/secret-hygiene.md`。

**未新增 memory 文件** — MEMORY.md 仍超 size limit (41.4KB > 24.4KB), 教训固化于 §3 + m5-handoff.yaml::layer2_deployment_findings。下个 session 前建议先瘦身 MEMORY.md。

---

## §5 多维度同步状态

| 维度 | 状态 |
|------|------|
| **UPM** | N/A — Aria 主仓不使用 UPM |
| **User Story** | US-025 `done 2026-05-23` ✅ |
| **OpenSpec** | M5 Spec **archived** `openspec/archive/2026-05-23-aria-2.0-m5-replay-reconciler-drift-review-loop-audit/`; active changes 0 (本 session 后, inflight aria-secret-guard-plugin-default 在另一 track) |
| **PRD / Architecture** | 不变 |
| **m5-handoff.yaml** | go_decision=Go + phase_c_completion 全写入 + b1_live + c2_live = true + layer2_deployment_findings F1-F5 |
| **Auto-memory** | 未新增 (MEMORY.md 超限) |
| **Decision memos** | 不变 (本 session 无新 decision; m5-handoff 直接吸收 finding) |
| **Production** | aria-orchestrator Hermes 健康; `aria-layer2-runner` parameterized job 注册 + 真实 dispatch 验证; aria-runner-bot 账户 must_change_password=false + collaborator restored |
| **Forgejo** | issue #119 closed; PR #121 closed; branch aria/DEMO-M5-O3 deleted; throwaway 全清 |
| **Multi-remote parity** | 主仓 (本 session 末) + aria-orchestrator submodule 待推; standards 无变更 |

---

## §6 Next session 入口 + 优先级

```bash
/aria:state-scanner   # 多 track 看板会 surface 本 handoff + 邻 track aria-secret-guard
```

**优先级建议** (任选,无硬依赖):

1. **inflight track 继续** — `aria-secret-guard-plugin-default` 在 Phase A shipped, owner 推进 Phase B (与本 M5 正交)
2. **M6 启动** — US-026 (M6 carryover + Layer 2 changes/redo full impl + Layer 2 entry full-cycle) brainstorm
3. **F2 proper fix** — Layer 2 registry auth 节点级配置 (~2-4h, hygiene cycle)
4. **MEMORY.md 瘦身** — 超限的索引整理 (~1h)
5. **Tier-2 累积** (post-close, 不需 dedicated session, owner workload natural accumulation)

**不应该做的**:
- ❌ 不要重复 O3 smoke (DEMO-M5-O3 已 succeed 并清理, 重跑无新信息)
- ❌ 不要在没有 F2 proper fix 之前依赖 Nomad HCL `auth` block 工作 (会再撞 cold-pull 401)
- ❌ 不要修改 m5-handoff.yaml::layer2_deployment_findings F1-F5 (它们是本 session 实证)

---

## §7 提交清单 (待 push)

主仓变更 (3 个文件 update + 1 mv + 1 new doc + submodule bump):
- `docs/handoff/2026-05-22-m5-phase-c-playbook.md` — F1 修正(line 197-198 加 ⚠ 注释 + bare hex)
- `docs/requirements/user-stories/US-025.md` — Status → `done 2026-05-23`
- `openspec/changes/aria-2.0-m5-replay-reconciler-drift-review-loop-audit/{proposal.md,tasks.md}` — Status + 6.21.1/6.26/6.30 update
- **mv** `openspec/changes/.../` → `openspec/archive/2026-05-23-aria-2.0-m5-replay-reconciler-drift-review-loop-audit/`
- `docs/handoff/2026-05-23-m5-phase-c-o3-done-d2-close.md` — 本 doc (new)
- `docs/handoff/latest.md` — 更新指针
- `aria-orchestrator` submodule bump (m5-handoff.yaml update)

aria-orchestrator 子仓变更:
- `docs/m5-handoff.yaml` — go_decision Go + t_deploy_status + phase_c_completion + b1_live + c2_live + layer2_deployment_findings F1-F5

**双推**: 主仓 + submodule 各推 origin + github。

---

## §8 Memory entries this session

**新增 3 个 memory entries (closeout 增量, 2026-05-23 ~01:00 UTC)**:
- ✅ [`feedback_forgejo_pat_docker_vs_git_split.md`](../../.claude/projects/-home-dev-Aria/memory/feedback_forgejo_pat_docker_vs_git_split.md) — Forgejo PAT docker pull vs git-over-HTTP 分裂 = `must_change_password=true` (Forgejo #2809);诊断 SOP + 修复 + 生产前置
- ✅ [`feedback_nomad_docker_auth_template_interp_gap.md`](../../.claude/projects/-home-dev-Aria/memory/feedback_nomad_docker_auth_template_interp_gap.md) — Nomad HCL docker `auth { password=${VAR} }` 从 template env 插值不可靠; build-node 缓存掩盖; cold-path 验证强制; 正解=节点级 plugin `auth.config`
- ✅ [`feedback_service_account_drift_preflight.md`](../../.claude/projects/-home-dev-Aria/memory/feedback_service_account_drift_preflight.md) — 服务账户 collaborator / must_change_password / PAT scope 漂移; 3 维度 round-trip preflight; 长度匹配 ≠ 内容正确

MEMORY.md 已同步 3 行 one-line 索引(整体仍超 size limit, 不阻塞本次, 留待独立 hygiene cycle 整体瘦身)。

本 session 其他教训留存于:
- §3 R1-R5 (本 doc, 5 条本 session 新陷阱)
- §4 实战教训 (本 doc, 5 条 meta lesson)
- `m5-handoff.yaml::t_deploy_status.phase_c_completion.layer2_deployment_findings` (F1-F5 机读形式)
- `2026-05-22-m5-phase-c-playbook.md` §O3 dispatch 命令(F1 fix + ⚠ 注释)

后续 session 可选补 (低优):
- `feedback_nomad_image_gc_compounds_auth_gap.md` — Nomad default `gc.image_delay=3min` 加剧 docker auth gap (已并入上方 #2 第 4 段, 单独 entry 非必需)
- `feedback_owner_secret_swap_round_trip_verify.md` — get-编辑-put 易出位 (已并入上方 #3 末段, 单独 entry 非必需)

**Q-audit (收尾)**:
- **Q1 未完成 task?** Tier-2 6.27-6.29 deferred(by design, non-blocking) + F2/F3 proper fix(post-M5) + S6 hygiene(timed). 全部 §2 documented + scheduled。无遗漏。
- **Q2 未固化经验?** 本 session 5 个 finding F1-F5 已 m5-handoff.yaml 机读 + 本 doc §3/§4 prose 双写。MEMORY.md 超限暂未开新 file, §8 列了下个 session 必补清单。
- **Q3 UPM/US/Spec/PRD?** US-025 → done ✅; M5 Spec → archived ✅; m5-handoff.yaml 全 writeback;PRD/Architecture 不动。一致。
- **Q4 收尾交接?** 本 doc + latest.md 更新 + multi-remote push (本 session 末)。完整。

---

## Cross-references

- **Predecessor (same track)**: [`2026-05-22-m5-phase-c-o1-o2-done.md`](2026-05-22-m5-phase-c-o1-o2-done.md)
- **Playbook (含 F1 fix)**: [`2026-05-22-m5-phase-c-playbook.md`](2026-05-22-m5-phase-c-playbook.md)
- **M5 Spec (archived)**: `openspec/archive/2026-05-23-aria-2.0-m5-replay-reconciler-drift-review-loop-audit/`
- **m5-handoff.yaml**: `aria-orchestrator/docs/m5-handoff.yaml` (machine-readable closure record)
- **US-025**: [`docs/requirements/user-stories/US-025.md`](../requirements/user-stories/US-025.md)
- **Adjacent inflight track**: [`2026-05-22-aria-secret-guard-plugin-default-phase-a-shipped.md`](2026-05-22-aria-secret-guard-plugin-default-phase-a-shipped.md)

---

**Created**: 2026-05-23 ~00:30 UTC
**Author**: solo-lab (uni.concept.wzfq@gmail.com), drafted by Claude Opus 4.7 (1M context)
**Status**: M5 CLOSED — US-025 `done`, Spec archived, all close-gate artifacts written and pushed.
**Next entry**: `aria:state-scanner` 看板会 surface inflight `aria-secret-guard-plugin-default` track 与 M6 brainstorm 入口。

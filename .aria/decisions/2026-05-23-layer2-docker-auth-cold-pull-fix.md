# Decision: aria-layer2-docker-auth-cold-pull-fix (DEC-20260523-001)

> **Type**: Spec scoping + probe finding
> **Date**: 2026-05-23 ~06:30-11:30 UTC (full Phase A.1 + R1 + R2 + Rev2-micro)
> **Author**: solo-lab (uni.concept.wzfq@gmail.com), drafted by Claude Opus 4.7
> **Status**: Spec Approved (Rev1.1, R2 converged 4/4 PASS_WITH_WARNINGS)
> **Parent decision**: M5 Phase D.2 close handoff `docs/handoff/2026-05-23-m5-phase-c-o3-done-d2-close.md` §2 (F2/F3 carry-forward) + §3 R2

---

## §1 触发场景

M5 Phase D.2 close handoff §2 把 F2/F3 (Layer 2 cold-pull docker auth gap) 标 "post-M5 任务, 不阻塞 close"。推荐路径:

> 1. 节点级 Nomad docker plugin `auth.config`: 在 3 个 heavy 节点的 Nomad client config 加 `plugin "docker" { config { auth { config = "/etc/nomad/docker-auth.json" } } }`, 并在每节点 deploy `/etc/nomad/docker-auth.json` ...
> 推荐选 #1 (config.json 显式管理, 路径明确, 不依赖 root-shell docker login 历史)

2026-05-23 ~06:30 UTC owner 启动 "F2 proper fix 起草" — 应进 Phase A.1。

---

## §2 Probe-first discipline (per feedback_prod_state_must_ground_playbook)

drafting 前 SSH 实地侦察 heavy-1/2/3 状态:

### Nomad config path

实际 path 不是 M5 handoff §2 推荐的 `/etc/nomad/`,而是 `/opt/nomad/config/` (per systemd unit `ExecStart=/usr/local/bin/nomad agent -config=/opt/nomad/config`)。3 节点一致。

### Plugin auth.config 状态

3/3 heavy 节点 `client.hcl` 已含:

```hcl
plugin "docker" {
  config {
    allow_privileged = false
    volumes { enabled = true }
    auth {
      config = "/root/.docker/config.json"
    }
  }
}
```

即 M5 handoff §2 option #1 推荐方案的 **client.hcl 部分已经 wired**。这一行在 M3/M4 era 已经部署 (来源未追溯,可能 Aether init 默认或更早某次 hygiene)。

### Config.json 内容

3/3 heavy 节点 `/root/.docker/config.json` 已存在:

| Host | Size | mtime | top-level | registries |
|------|------|-------|-----------|------------|
| heavy-1 | 128 B | 2026-05-06 13:59:08 | `['auths']` | `['forgejo.10cg.pub']` |
| heavy-2 | 129 B | 2026-05-06 13:59:39 | `['auths']` | `['forgejo.10cg.pub']` |
| heavy-3 | 136 B | 2026-05-22 23:47:22 | `['auths']` | `['forgejo.10cg.pub']` |

每个 file 都有 `forgejo.10cg.pub` 在 `auths` 字段。**但 mtime 差异显著** — heavy-1/2 在 M3 era (2026-05-06 ~14:00),heavy-3 在 M5 O3 debug 期间 (2026-05-22 23:47 = handoff §2 提及的 owner 当时编辑 var)。这暗示 3 节点 cred 内容**可能不一致** (drift 风险 R1 in Spec)。

### Real blocker identified

`aria-layer2-runner.hcl` 行 172-175:

```hcl
auth {
  username = "aria-runner-bot"
  password = "${FORGEJO_BOT_PAT}"
}
```

`${FORGEJO_BOT_PAT}` 在 **Nomad HCL config-time** 解析(而非 template runtime), 但 `FORGEJO_BOT_PAT` 只在 `template { ... env = true }` stanza 渲染后注入 task **process env**, 不在 HCL config-time scope 内。

Nomad docker driver task-level `config.auth` 块 **优先级高于** plugin-level `auth.config`,因此即使节点级 config.json 已正确,HCL auth block 也会以 `password=""` (interp 失败) 或空密码尝试 auth → registry 401 → cold-pull fail。M1 demo "成功" 是 build-node 镜像缓存(F3 image_delay GC 之前缓存命中)掩盖。

sister HCL `aria-runner-template.hcl` 行 78-81 有相同 pattern(M1 baseline,M3 forked 时复制了 auth block,layer2 沿用)。

`aria-build.hcl` / `aria-layer1.hcl` **无** docker auth block — 它们或不拉自定义 image,或依赖 plugin 配置, 不在本 Spec scope。

---

## §3 Scope reframe

**原 M5 handoff §2 估算** (drafting 前):
- Deploy node-level plugin config (3 nodes × Nomad client.hcl edit) → ~30min owner-action × 3
- Deploy `/etc/nomad/docker-auth.json` (3 nodes × base64 cred + write file) → ~30min owner-action × 3
- Delete HCL auth block (2 HCLs × ~5 行) → ~15min AI
- 总计 ~2-4h (大头是 owner SSH 编辑 + restart Nomad client × 3)

**Probe 后实测 scope** (drafting 中):
- Plugin config 部分 ✅ 已部署 — **0 work**
- config.json 文件存在 + has forgejo entry ✅ — **不需重新部署, 只需 verify cred 内容一致 + 有效**
- Delete HCL auth block (2 HCLs) — ~15min AI
- 写 convention 文档 — ~30-45min AI
- Verify cred (3 节点 round-trip,可能发现 drift) — ~10-20min owner
- Live cold-pull verify (3 节点 dispatch + force image GC) — ~15-25min owner
- 总计 **~1.5-2.5h** (压缩 ~40%)

如 R1 触发(cred drift 发现 stale/不一致),需先做独立 PAT rotation cycle,本 Spec 加 ~30-60min owner action(但属于另一个 carry-forward 的 deferred 池,本 Spec 不吸纳)。

---

## §4 决策点

### D1: Level 2 vs Level 3 → **L2 (Minimal)**

**理由**:
- Scope 完全确定 (HCL diff + 文件 verify + convention doc)
- 无设计不确定性 (Nomad precedence + plugin config 行为是 Hashicorp doc 规定)
- 无多模块状态机
- 触及 3 prod 节点但不改 cluster topology,blast radius 限于 docker auth path

升 L3 的可考虑情景: owner 想 enforce 多轮 audit (multi-agent post_spec + pre_merge) — 仍可以执行,但 ROI 边际(无 design space 让多 agent 分歧)。

### D2: F3 image_delay 调整 → **Out of Scope**

F2 修复后 cold-pull 不再 fail,F3 (image_delay=3min default) 不再是放大器。
独立 hygiene cycle 可调 `gc.image_delay=24h` 或 pre-pull 策略,但**不本 Spec**。

### D3: aria-runner-template.hcl 处置 → **T1.0 决** (probe-pending)

T1.0 任务:
```bash
# 3 节点查注册状态
for h in heavy-1 heavy-2 heavy-3; do
  ssh $h "nomad job status aria-runner-template 2>/dev/null | head -3"
done
# repo 引用扫描
grep -r 'aria-runner-template' aria-orchestrator/ docs/ --include='*.hcl' --include='*.md' --include='*.sh'
```

分支 + commit message template (per R1 M-tl-M-2):
- (a) 仍 registered + 有 dispatch 历史 → 同 layer2 删 auth block (parity fix)
  - Commit: `feat(layer2): delete docker auth block from 2 HCLs (aria-layer2-runner + aria-runner-template)`
- (b) registered 但无 recent dispatch → deprecate 注释 + 仍删 auth block + 保留文件 (M1 historical reference)
  - Commit: `feat(layer2): delete auth block from aria-layer2-runner; deprecate aria-runner-template (M1 baseline, no recent dispatch)`
- (c) 未 registered → 整文件 deprecate 注释 (header 加 SUPERSEDED tag)
  - Commit: `feat(layer2): delete auth block from aria-layer2-runner; supersede aria-runner-template (file deprecate, M1 archive)`

dispatch-issue.sh + t5-run-demo.sh 仍引用 `aria-runner-template` 是 pre-existing M1-era drift,T1.0 报告标 **follow-up Forgejo issue**,不在本 Spec scope。

### D4: Convention 文档 SOT → **standards/conventions/nomad-docker-registry-auth.md**

新文件,因当前 standards/conventions/ 无 Nomad-related convention。

**8 段大纲** (Rev1 扩 6→8 段, 加 §0/§7/§8):

- **§0 Rationale + Observed contradiction** (R1 M-km-C-1 closure — 必须 surface)
  - Aether 2026-04-23 spike GO (Nomad < v1.11.2, 11.5MB image, alloc d360435e) vs Aria 2026-05-23 M5 O3 live FAIL (Nomad v1.11.2 + Forgejo 11.0.6)
  - 同集群 30 天前 GO / 现在 FAIL = 当前 ground truth SOT = 严格禁 task-level `auth { ${VAR} }` 组合
  - cross-ref `Aether openspec/archive/2026-04-22-fix-hardcoded-docker-auth` (历史 context)
- **§1 Problem statement** (M5 §3 R2 实证 + 不可复现的根因候选清单: Nomad version / image size / force_pull flag / Forgejo upgrade)
- **§2 Mechanism** (R1 M-ba-I-1 closure)
  - `${NOMAD_META_*}` = Nomad native interp, 解析在 docker driver invocation 之前
  - `${TEMPLATE_VAR}` (来自 template stanza) = 渲染 task process env, 在 driver invocation 之后
  - 因此 task-level `config.auth { password = "${TEMPLATE_VAR}" }` 在 driver pull image 时仍 unresolved → 401
- **§3 Forbidden pattern** (HCL task-level `auth { password = "${VAR}" }` + template env 组合;**scope 限**: envsubst/deploy-time substitution 模式如 Kino/Kairos/SilkNode `__REGISTRY_TOKEN__` **不在本 convention 范围**, §0/§3 显式声明)
- **§4 SOT pattern** (节点级 `/root/.docker/config.json` schema spec)
  - JSON 结构: `{"auths":{"<registry>":{"auth":"<base64(user:pass)>"}}}` — `email` 字段不需要
  - base64 encoding: `printf '%s' 'user:pass' | base64 -w0` (`-w0` 防 76-char wrap, 某些平台 decode 失败)
  - Lab 占位符: `<bot-username>` / `<node-N>` / `<docker-config-path>` (per R1 M-km-I-2)
  - 验证语义: Nomad driver per-alloc 读, 不需 restart;仅 client.hcl 路径变更才需 restart
- **§5 PAT rotation playbook** (**单向 reference** secret-hygiene.md §2.4 + §3.6, per R1 M-km-I-1)
  - **不重复** `docker login --password-stdin` 安全 pattern (在 secret-hygiene.md SOT)
  - 本段只写 Nomad-specific: atomic 3-node sync 顺序 + round-trip verify 命令 + no chat-leak invariant
- **§6 References** (M5 handoff §3 R2 + Aether archived spec + 本 Spec archive path + Forgejo issue 链)
- **§7 Verification checklist** (R1 M-km-M-2 closure — 供已有 Nomad HCL 项目 self-audit)
  - grep auth block count == 0
  - check `${VAR}` template interpolation pattern in HCL config blocks
  - verify client.hcl plugin docker `auth.config` 路径正确
- **§8 Migration path** (R1 M-km-M-2 closure)
  - 已有 HCL 项目过渡步骤: remove auth block → verify node-level config wired → cold-pull live test
  - envsubst 模式 (`__REGISTRY_TOKEN__`) 显式 out-of-scope; 不需 migrate, 但建议 audit cred rotation 流程

### D5: 验收 C 节点覆盖 → **3/3 (推荐)** 或 1/3 representative

3/3 优势: 检出 cred drift R1 + per-node constraint 测试。
1/3 劣势: 漏 drift 风险 (probe 已发现 heavy-3 mtime 不同)。
**推荐 3/3**。

---

## §5 Open Questions for owner (复用 proposal.md §Open Questions)

Q1: L2 vs L3 → 推荐 L2
Q2: aria-runner-template 处置 → T1.0 后决
Q3: 本 Spec vs `aria-secret-guard-plugin-default` 优先级 → 推荐先做本 Spec
Q4: 验收 C 节点覆盖 → 推荐 3/3

---

## §6 References

- **Probe transcript**: 本 session 2026-05-23 ~06:30 UTC, SSH heavy-1/2/3 readonly probe (无 cred 值漂入 chat)
- **Parent handoff**: `docs/handoff/2026-05-23-m5-phase-c-o3-done-d2-close.md` §2 F2/F3 + §3 R2 + §4 实战教训
- **Implicated HCLs**: `aria-orchestrator/nomad/jobs/aria-layer2-runner.hcl` (L172-175), `aria-orchestrator/nomad/jobs/aria-runner-template.hcl` (L78-81)
- **Implicated cluster config**: `/opt/nomad/config/client.hcl` (3 heavy nodes), `/root/.docker/config.json` (3 heavy nodes)
- **Related memories**: `[[feedback_nomad_docker_auth_template_interp_gap]]` (root cause, 待 Phase D.3 更新), `[[feedback_prod_state_must_ground_playbook]]` (probe discipline 本 case 实证), `[[feedback_t15_owner_blocking_pattern]]` (AI-runnable + owner-action 拆分), `[[feedback_test_mock_pattern_hides_prod_bug]]` (shape ≠ content, length-equal ≠ cred-equal 同 pattern), `[[feedback_secrets_never_in_conversation]]` (R3 mitigation)
- **Aether 端**: 已存在规划的 Spec 槽 `fix-hardcoded-docker-auth-node-login` (在 `Aether openspec/archive/2026-04-22-fix-hardcoded-docker-auth/proposal.md` 末段 + Aether Issue #45 follow-up) — owner 决策时, **正确路径是补全这个已规划 Spec 而非新开 issue** (per R1 M-km-M-3)
- **M6 dependency** (R2 M-tl-N-M-2): M6 brainstorm + kickoff **soft-blocked** 在本 Spec done。M6 任何 Layer 2 cold-dispatch 测试都会撞 F2 失败,本 Spec 既是 hygiene 又是 M6 准入。state-scanner Phase 2 推荐应在 M6 推 hint 时显式 surface 这个 dependency。

## §7 Audit history

### R1 (2026-05-23 ~07:00-09:00 UTC) — 4-agent parallel

| Agent | Verdict | C / I / M |
|-------|---------|-----------|
| tech-lead | PASS_WITH_WARNINGS | 0 / 4 / 3 |
| backend-architect | NEEDS_FIX | 1 / 4 / 3 |
| qa-engineer | NEEDS_FIX | 1 / 4 / 3 |
| knowledge-manager | NEEDS_FIX | 2 / 4 / 3 |
| **聚合** | **3/4 NEEDS_FIX** | **4 / 16 / 12** |

**4 Critical**:
- M-ba-C-1 + M-qa-I-4: 验收 C `nomad system gc` 不清 docker image cache → 改 `docker rmi -f` + 推荐 `force_pull = true`
- M-qa-C-1: 验收 A grep 漏 sister HCL → 扩到两 HCL + nomad/jobs/ regression
- M-km-C-1: convention §1 不能与 Aether spike GO 矛盾 → 加 §0 Observed contradiction
- M-km-C-2: nomad/README.md 行 170 主动误导 → 必须进 deliverable

**8 cross-cutting Important** (多 agent 共识):
- M-ba-I-3 + M-qa-I-1: length-equal 不能证 cred 一致 → round-trip mandatory
- M-tl-I-2 + M-qa-I-2: R1 escalation dead reference → piggyback or open issue
- M-ba-I-1 + M-km-C-1: 精确机制说明 (NOMAD_META vs template env timing)
- M-ba-I-2 + M-qa-C-1: 同 M-qa-C-1
- M-tl-I-1: merge-order vs secret-guard track
- M-tl-I-3 + M-km-I-2: standards/ Lab-shareable (占位符)
- M-ba-I-4: config.json schema (no email + base64 -w0)
- M-km-I-1: §5 cross-ref secret-hygiene.md (不重复)
- M-km-I-3: AD-M1-8 Revised note
- M-km-I-4: memory plan

**~6 absorbed Minor** (R2 sweep 顺便): M-tl-M-1 fingerprint cmd, M-tl-M-2 commit msg template, M-tl-M-3 M6 dependency, M-ba-M-1 双索引, M-ba-M-2 reload definitive, M-km-M-2 §7/§8 sections, M-km-M-3 Aether Spec 槽。

**Deferred to Phase B / non-blocking**: M-km-M-1 standards/README hygiene补 (secret-hygiene + session-handoff 索引), M-qa-M-2 dispatch-issue.sh 已知 drift (follow-up issue), M-qa-M-3 non-forgejo registry impact (已 verified)。

**R1 audit reports 原始 transcript**: 保留在本 session conversation history;Phase A.3 sign-off 后合并写入 `.aria/audit-reports/post_spec-R1-2026-05-23T<HHMMSS>-aria-layer2-docker-auth-cold-pull-fix-orchestrator.md`。

### R2 (pending — Task #3)

待 R2 dispatch verify Rev1 fixes,目标 4/4 PASS_WITH_WARNINGS + 0 NEW critical + ≥70% Important 减少 (per `[[feedback_audit_r2_collapse_default_vs_owner_invoked]]`)。

---

## §8 Phase B implementation outcome (appended 2026-05-23 ~15:20 UTC, per qa-engineer M-qa-PI-X-2)

### §8.1 R1 escalation Branch 2 (piggyback) actual execution

Proposal §Risks R1 decision tree Branch 2 ("FORGEJO_BOT_PAT 在 in-flight rotation 子集 → piggyback") **triggered + executed**:

1. T6 initial verify: B1 fingerprint drift detected (heavy-1/2 = `3654ff26d443`, heavy-3 = `21015768f512`) + B2 all 3 LOGIN_OK ⇒ 2 distinct valid PATs in active use
2. Owner revoke 2 旧 PATs (`aria layer2 runner 2026 05 22` + `aria build clone 2026 05 22`)
3. Detected 3rd existing PAT `aria-runner-bot` (2026-05-03), fingerprint `c957308a0e35`, used by Nomad var `FORGEJO_BOT_PAT` for Layer 1 + aria-build + Layer 2 entrypoint git ops → **kept (Option X, scope discipline)**
4. Owner create v1 PAT `aria-runner-bot-prod-20260523-rotated` with scopes per **DEC-20260520 §3.1 R1.B** (incomplete spec: missing `:package`)
5. Atomic 3-node sync (Path B tmp file) → fingerprint `0d6e152a82f1` 3-way, B2 LOGIN_OK 3-way
6. T8 cold-pull FAIL — all 3 nodes 401 unauthorized (JWT payload reveals `Scope=write:issue,write:repository,read:user`, missing `read:package`)
7. Owner create v2 PAT `aria-runner-bot-prod-20260523-v2-full-scope` with **canonical 7-scope set** (per codebase enumeration, see §8.2)
8. Atomic 3-node sync (Path B retry) → fingerprint `46e20fea2f5e` 3-way, B2 LOGIN_OK 3-way
9. T8 cold-pull PASS — 3/3 PULL_EXIT=0, "Pulling from 10cg/aria-runner" + "Pull complete"
10. Owner revoke v1 PAT, retain v2 + 2026-05-03 (independent path)

**Final active PATs for aria-runner-bot**:
- `aria-runner-bot-prod-20260523-v2-full-scope` (fingerprint `46e20fea2f5e`, 7 scopes) — node config.json image pull
- `aria-runner-bot` 2026-05-03 (fingerprint `c957308a0e35`) — Nomad var FORGEJO_BOT_PAT (Layer 1 + aria-build + container git ops)

### §8.2 PAT scope canonical (per codebase enumeration)

**DEC-20260520 §3.1 R1.B was incomplete** — lists only `write:repository / read:repository / write:issue / read:issue / read:user`, missing `:package` series。
**AD-M1-8 §决定 Option A canonical** lists `read:package + write:package + write:repository + read:user`, missing `:issue` series。

True canonical (via 2026-05-23 codebase grep of aria-runner-bot operations) = **7 scopes**:

| Scope | Operation evidence |
|-------|---------------------|
| `read:package` | Nomad docker driver image pull (this Spec C verify) |
| `write:package` | aria-build `docker push` (Dockerfile + registry-push-guide.md) |
| `read:repository` | Layer 1 `GET /repos/.../pulls/{id}` + Layer 2 entrypoint `git clone` |
| `write:repository` | Layer 1 `POST .../pulls/{id}/merge` + Layer 2 `git push` |
| `read:issue` | Layer 1 `GET /repos/.../issues?state=open&label=...` |
| `write:issue` | Layer 1 + Layer 2 `POST .../issues/{id}/comments` |
| `read:user` | Self-identify `GET /user` |

### §8.3 Phase B audit outcome summary

| Stage | Verdict | Audit report |
|-------|---------|--------------|
| post_spec R1 (4-agent) | NEEDS_FIX → 4C/16I/12M | `.aria/audit-reports/post_spec-R1-2026-05-23T0900Z-...md` |
| post_spec R2 (4-agent verify) | PASS_WITH_WARNINGS (4/4) | `.aria/audit-reports/post_spec-R2-2026-05-23T1100Z-...md` |
| Rev2-micro sweep | (5 surgical edits applied) | proposal Rev1.1 |
| Phase B AI segment | (T1.0 + T2.x + T3.x + T4.x + T5.x done, 3 PR merged) | commits 53c0f8a → edc1bdf (rebased) → 6fea5d7 (merge) → a8e0096 (aria pointer regression fix) |
| post_implementation R1 (2-agent L2 proportionality) | PASS_WITH_WARNINGS (0C/5I/7M aggregate); Phase D CONDITIONAL on 3 items | (this DEC §8 + tasks.md sync + probe evidence file address the 3 conditions) |

### §8.4 Latent issues surfaced (for Phase D Forgejo issue batch)

1. **PAT scope canonical missing from AD-M1-8** (per §8.2) — file Forgejo issue to update AD-M1-8 §决定 with 7-scope
2. **`a8e0096` aria pointer regression** caught + fixed but root cause prevention not codified — file Forgejo issue for branch-finisher / Phase C.2.5 mechanical regression gate (multi-terminal-coordination Layer L 6-rule patch)
3. **dispatch-issue.sh + t5-run-demo.sh + test-dispatch-idempotency.sh** still reference `aria-runner-template` (per T1.0 probe report §4 draft) — file Forgejo issue for script drift cleanup
4. **DEC-20260520 §3.1 R1.B incomplete scope spec** — update target via Forgejo issue (covered by #1 above, can bundle)

---

**Status changes**:
- 2026-05-23 ~06:30 UTC: Draft v1 (probe + reframe + Spec draft 同 session)
- 2026-05-23 ~10:00 UTC: Draft v2 / Rev1 (post R1 4-agent audit — 4C/16I/12M; Rev1 addressed 4 Critical + 8 cross-cutting Important + ~6 absorbed Minor)
- 2026-05-23 ~11:30 UTC: **Approved (Rev1.1)** — R2 4-agent 4/4 PASS_WITH_WARNINGS converged + Rev2-micro sweep (B2 stdin / C2.5 alloc node verify / A2 regex unify / D responsibility label / DEC Status sync / M6 blocker note);post_spec audit closed,准入 Phase A.2 task-planner
- 2026-05-23 ~15:20 UTC: **Phase B + Phase C closed (post_implementation 2-agent PASS_WITH_WARNINGS, 0 Critical)** — §8 outcome appended (R1 escalation actual + PAT scope canonical correction + latent issues for Phase D batch);准入 Phase D archive

# Tasks: aria-layer2-docker-auth-cold-pull-fix

> **Spec**: `openspec/changes/aria-layer2-docker-auth-cold-pull-fix/proposal.md`
> **Level**: Minimal (Level 2)
> **Status**: Approved (Rev1.1, post R2 4/4 PASS_WITH_WARNINGS)
> **Created**: 2026-05-23
> **Estimated**: ~5.1h (AI ~3.5h + owner ~0.8h + post_impl audit ~0.5h + closeout ~0.3h)
> **Branch**: `feature/layer2-docker-auth-fix` (主仓 + standards + aria-orchestrator 同名)

---

## Ordering invariants (per R1 M-ba-M-3 + Rev2-micro)

- **T6 cred verify 必须先于 T7 nomad job run activation** — 否则 HCL change 上线后撞到 stale config.json cred = cluster-wide cold-pull 全 fail
- **T1.0 probe 必须先于 T2.2** — `aria-runner-template.hcl` 处置分支 (a)/(b)/(c) 决定 commit message + 文件操作
- **T2.3 constraint 添加必须先于 T8 cold-pull verify** — `${NOMAD_META_TARGET_NODE}` constraint 缺失 = C 验收 silent-pass (per R2 M-cross-N-I-2)

---

## Tag legend

- **[AI]** = AI-runnable, 无 owner block
- **[OWNER]** = 必须 owner SSH/手动操作 (per `[[feedback_t15_owner_blocking_pattern]]`)
- **[AI→OWNER]** = AI 起草 / owner 执行
- **[AI+OWNER]** = AI 编排 + owner 确认 (audit / sign-off)

---

## 1. Phase B start — Probe & sister HCL decision

- [ ] **T1.0 [AI]** probe `aria-runner-template` job 状态 + repo 引用扫描 + 决定处置分支
  - 3 节点 SSH: `for h in heavy-1 heavy-2 heavy-3; do ssh $h "nomad job status aria-runner-template 2>/dev/null | head -3"; done`
  - repo grep: `grep -r 'aria-runner-template' aria-orchestrator/ docs/ --include='*.hcl' --include='*.md' --include='*.sh'`
  - 决分支:
    - (a) registered + recent dispatch (≤30 天) → 同 layer2 删 auth block, parity fix
    - (b) registered 无 recent dispatch → deprecate 注释 + 删 auth block + 保留文件
    - (c) 未 registered → 整文件 deprecate header + 删 auth block
  - 产物: `.aria/probes/2026-05-23-aria-runner-template-status.md` (per R2 M-tl-N-M-1) 含: 3 节点 nomad job status / repo references list / 分支决定 + commit message template (per DEC §4 D3) / dispatch-issue.sh + t5-run-demo.sh follow-up Forgejo issue 草稿
  - **必产**: Forgejo issue draft (label `tech-debt` + `m1-baseline-cleanup`) 关于 dispatch-issue.sh + t5-run-demo.sh script drift (per R1 M-qa-M-2 enforcement)
  - 估时: 0.5h

## 2. Phase B — HCL diff (aria-orchestrator submodule)

- [ ] **T2.1 [AI]** `aria-layer2-runner.hcl` 删 docker task auth block (L172-175) + 周围注释 reframe
  - 删 5 行 `auth { username = "aria-runner-bot" password = "${FORGEJO_BOT_PAT}" }`
  - 改注释 L168 + L169 (原引用 AD-M1-8 + FORGEJO_BOT_PAT 来源) 为: `# Auth: 节点级 plugin auth.config (per standards/conventions/nomad-docker-registry-auth.md + DEC-20260523-001 supersedes AD-M1-8)`
  - 估时: 0.15h
  - 依赖: 无

- [ ] **T2.2 [AI]** `aria-runner-template.hcl` 按 T1.0 分支处理
  - (a)/(b) 分支: 删 L78-81 auth block + 加 deprecation/parity 注释
  - (c) 分支: 文件 header 加 `# SUPERSEDED by aria-layer2-runner @ DEC-20260523-001 — do not run; kept as M1 archive reference` + 仍删 auth block 防 grep 回归
  - 估时: 0.2h
  - 依赖: T1.0

- [ ] **T2.3 [AI]** verify or add `${NOMAD_META_TARGET_NODE}` constraint in HCL (R2 M-cross-N-I-2)
  - grep 检查 `aria-layer2-runner.hcl` 是否有 `constraint { ... ${NOMAD_META_TARGET_NODE} ... }` 块
  - 若无,加:
    ```hcl
    constraint {
      attribute = "${node.unique.name}"
      operator  = "regexp"
      value     = "^${NOMAD_META_TARGET_NODE}$"
    }
    ```
    并标 `meta_optional` 加 `TARGET_NODE`(空时退 regex 匹配 `.+` 任意节点 — 不破现有 dispatch)
  - 注意 alt: 若 HCL 设计上不该有 hard constraint (auto-placement),则改用 `affinity { ... weight = 100 }` 软性,owner T8 时用 `-detach` + `nomad alloc status` 验证落点
  - 估时: 0.25h
  - 依赖: T2.1

## 3. Phase B — Doc updates (aria-orchestrator submodule)

- [ ] **T3.1 [AI]** `aria-orchestrator/nomad/README.md` 行 170 排查表 update (R1 M-km-C-2)
  - 原: `image auth 失败 (401/403) | 检查 HCL config.auth.password template 指向 Nomad Variable 正确`
  - 改: `image auth 失败 (401/403) | 检查节点级 /root/.docker/config.json cred (per standards/conventions/nomad-docker-registry-auth.md); task-level HCL auth block 已废弃 (DEC-20260523-001)`
  - 估时: 0.1h
  - 依赖: 无

- [ ] **T3.2 [AI]** `aria-orchestrator/docs/architecture-decisions.md` §AD-M1-8 Revised note (R1 M-km-I-3)
  - Status 行后追加 1 行:
    ```
    > **Revised by DEC-20260523-001 (2026-05-23)** — task-level docker auth block removed from aria-layer2-runner + aria-runner-template; node-level plugin auth.config (`/root/.docker/config.json` per heavy node) is now SOT. See `standards/conventions/nomad-docker-registry-auth.md`.
    ```
  - 估时: 0.1h
  - 依赖: 无

## 4. Phase B — Convention doc (standards submodule)

- [ ] **T4.1 [AI]** 起草 `standards/conventions/nomad-docker-registry-auth.md` (新文件, 9 段 §0-§8, per DEC §4 D4)
  - §0 Rationale + Observed contradiction (Aether 2026-04-23 GO vs Aria 2026-05-23 FAIL, with table)
  - §1 Problem statement (M5 §3 R2 实证 + 不可复现根因候选)
  - §2 Mechanism (NOMAD_META_* vs template stanza env 解析时序 + docker driver invocation timing)
  - §3 Forbidden pattern (HCL task `auth { password = "${VAR}" }` + template env 组合;**scope 限**: envsubst `__REGISTRY_TOKEN__` 模式 out-of-scope)
  - §4 SOT pattern (节点级 `/root/.docker/config.json` schema spec + `base64 -w0` + Lab 占位符 `<bot-username>` / `<node-N>` / `<docker-config-path>` + reload 语义 "per-alloc read no restart")
  - §5 PAT rotation playbook (**单向 reference** secret-hygiene.md §2.4 + §3.6, 不重复 docker login pattern;本段只写 atomic 3-node sync + round-trip verify + no chat-leak)
  - §6 References (M5 handoff §3 R2 + Aether archived spec + 本 Spec archive + Forgejo issue)
  - §7 Verification checklist (供已有 Nomad HCL 项目 self-audit:grep auth block / check `${VAR}` template interp / verify client.hcl plugin config)
  - §8 Migration path (已有 HCL 项目过渡步骤;envsubst 模式 out-of-scope 声明)
  - **必含约束** (per R2 验收 D1b): 所有 Lab 特定 detail 用占位符,**不含** `heavy-[1-3]` / `aria-runner-bot` 字面
  - 估时: 1h
  - 依赖: 无 (与 T1-T3 并行可)

- [ ] **T4.2 [AI]** verify convention doc 满足 R2 验收 D
  - `[ -f standards/conventions/nomad-docker-registry-auth.md ]`
  - `grep -cE 'heavy-[1-3]|aria-runner-bot' standards/conventions/nomad-docker-registry-auth.md == 0`
  - `grep -cE '^## §[0-8] ' standards/conventions/nomad-docker-registry-auth.md == 9`
  - 估时: 0.05h
  - 依赖: T4.1

## 5. Phase B — Standards index updates

- [ ] **T5.1 [AI]** `standards/summaries/conventions-summary.md` 新增 nomad-docker-registry-auth 摘要条目
  - 估时: 0.1h
  - 依赖: T4.1

- [ ] **T5.2 [AI]** `standards/README.md` Development Conventions 表新增条目
  - **Deferred minor** (per R1 M-km-M-1): 顺带补 `secret-hygiene.md` + `session-handoff.md` 索引缺失? — owner 决,若 yes 一并加;若 no 仅加本 Spec
  - 估时: 0.1h
  - 依赖: T4.1

## 6. Phase B — Owner verify (cred validity, BEFORE HCL activation)

- [ ] **T6 [OWNER]** 3 节点 cred verify per §Acceptance B (fingerprint + round-trip via stdin)
  - B1 fingerprint per node (Python sha256[:12]) — 3 行输出必须全等
  - B2 round-trip per node via `--password-stdin` (PAT 走 stdin 不入 process args) — 期望返 `200`
  - **若 fingerprint drift OR HTTP non-200 → STOP, 进 R1 escalation path**:
    - 查 `.aria/decisions/2026-05-20-secret-rotation-during-m5-deploy.md` §1 active rotation 状态
    - FORGEJO_BOT_PAT 在 in-flight subset → piggyback (合并 sync 与 active rotation), 完成后继续 T7
    - cred stale 且不在 active rotation → 新建 Forgejo issue (label `P0 blocker` + `secret-rotation`), Spec Status 改 Blocked, rotation done 后继续
  - 估时: 0.3h (顺利) / +0.5h (drift fix)
  - 依赖: T2.x 已 commit (HCL diff 在本机, **但不 nomad job run**)

## 7. Phase B — Owner deploy (HCL activation)

- [ ] **T7 [OWNER]** Push HCL change + run on cluster
  - 主仓 dev branch push + Forgejo PR 创建 (但不 merge — 等 post_implementation audit + cold-pull verify)
  - `nomad job run aria-orchestrator/nomad/jobs/aria-layer2-runner.hcl` (3 heavy 任一节点 nomad cli)
  - 若 T1.0 = (a) 分支, 同 run aria-runner-template.hcl
  - 估时: 0.15h
  - 依赖: T6 PASS

## 8. Phase B — Owner verify (cold-pull live, AFTER activation)

- [ ] **T8 [OWNER]** 3 节点 cold-pull live verify per §Acceptance C
  - 每节点 4 步 (C1 docker rmi -f / C2 dispatch / C2.5 alloc node verify / C3 grep log "Pulling from")
  - 3/3 节点 PASS ⇒ live verify done
  - 若任一节点 C3 缺 "Pulling from" 行 但 alloc 仍 SUCCESS → 检查是否走 cache (C1 清得不彻底) 或 alloc 落错节点 (C2.5 漏)
  - 任一 FAIL → rollback HCL change (revert PR, nomad stop) + 进 emergency cred refresh issue
  - 估时: 0.5h
  - 依赖: T7

## 9. Phase C — post_implementation audit (Level 2 proportionality)

- [ ] **T9 [AI+OWNER]** Single-round post_implementation audit (2-agent: tech-lead + qa-engineer)
  - 输入: HCL diff + convention doc + nomad/README update + AD note + standards index + T6/T7/T8 evidence
  - 输出: PASS / NEEDS_FIX verdict + 0-N findings
  - per `[[feedback_agent_team_for_level1]]` proportionality — Level 2 doc-dominant change 1 轮足够
  - 若 NEEDS_FIX → 加 micro sweep round, 不重 4-agent
  - 估时: 0.5h
  - 依赖: T8

## 10. Phase C — Commit + multi-remote push + PR merge

- [ ] **T10.1 [AI]** Commit standards submodule (convention + index)
  - 分支 `feature/layer2-docker-auth-fix` in standards/
  - commit message per DEC §4 D3 + sign reference to DEC-20260523-001
  - push origin + github (multi-remote per `[[feedback_state_scanner_run_all_phases]]`)
  - Forgejo PR open
  - 估时: 0.15h
  - 依赖: T9 PASS

- [ ] **T10.2 [AI]** Commit aria-orchestrator submodule (HCL + nomad/README + AD note)
  - 分支同名
  - commit message 按 T1.0 分支选 (a)/(b)/(c) template
  - push 双 remote
  - Forgejo PR open (但等 T10.1 standards 先 merge — 因 aria-orchestrator HCL 引用 standards/conventions/ 路径不存在的话 doc cross-ref dangling)
  - 估时: 0.15h
  - 依赖: T9 PASS

- [ ] **T10.3 [AI+OWNER]** PR merge order — standards 先, aria-orchestrator 后, 主仓 last
  - per `[[feedback_coupled_pr_merge_discipline]]`:
    1. merge standards PR (`Do=merge`)
    2. aria-orchestrator submodule bump 到 standards master post-merge SHA, 验 `git -C standards merge-base --is-ancestor <PR_SHA> master` (per `[[feedback_submodule_pointer_post_merge_bump]]`)
    3. merge aria-orchestrator PR
    4. 主仓 bump standards + aria-orchestrator 双 pointer 到 post-merge master
    5. Pre-merge gate (Rule #8): `aether ci status --branch master --in-flight --json` 验证 main 无 in-flight CI
    6. merge 主仓 PR
  - 估时: 0.2h
  - 依赖: T10.1 + T10.2

## 11. Phase D — Closeout

- [ ] **T11.1 [AI]** Spec archive
  - `mv openspec/changes/aria-layer2-docker-auth-cold-pull-fix/ openspec/archive/2026-05-23-aria-layer2-docker-auth-cold-pull-fix/`
  - proposal.md frontmatter Status → `Complete (2026-05-23 archived; post_implementation PASS + cold-pull live 3/3)`
  - 估时: 0.05h
  - 依赖: T10.3

- [ ] **T11.2 [AI]** Memory writes (per R1 M-km-I-4)
  - 更新 `feedback_nomad_docker_auth_template_interp_gap.md`: 加 "10CG heavy-1/2/3 plugin auth.config 已 wired + HCL auth block 已删 + 正式 fix complete 2026-05-23"
  - 新增 `reference_10cg_nomad_docker_plugin_auth_wired.md`: 3 节点 client.hcl plugin 配置 + config.json 路径快照 (供未来 onboarding 项目避免重复 SSH 验证)
  - 新增 `feedback_probe_first_scope_reframe.md`: 本 Spec ~40% scope 收缩实证 (跨 session 第二次 `[[feedback_prod_state_must_ground_playbook]]` 应用; M5 §2 推荐 vs 实测的 inversion pattern)
  - MEMORY.md 索引 3 行(格式参照现有最短索引行;**注意 MEMORY.md 当前 22.4KB / 24.4KB limit, 留 buffer ~2KB**, 索引 hook ≤ 120 字节)
  - 估时: 0.3h
  - 依赖: T11.1

- [ ] **T11.3 [AI]** Session handoff doc (Rule #9)
  - `docs/handoff/2026-05-23-aria-layer2-docker-auth-cold-pull-fix-done.md`
  - frontmatter: `track-id: aria-layer2-docker-auth-cold-pull-fix`, `status: closed`
  - 9 段 skeleton per session-handoff template
  - 更新 `docs/handoff/latest.md` pointer
  - 估时: 0.15h
  - 依赖: T11.1 + T11.2

- [ ] **T11.4 [AI]** Forgejo issue closure / new issues
  - 关闭: M5 handoff §2 F2/F3 carry-forward (in M5 m5-handoff.yaml::layer2_deployment_findings — backreference 本 Spec archive)
  - 新建 (per T1.0): dispatch-issue.sh + t5-run-demo.sh script drift follow-up
  - 新建 (per R1 M-km-M-3): Aether 端补全 `fix-hardcoded-docker-auth-node-login` Spec 槽 通报 issue (链 Aether Issue #45 + 本 Spec archive)
  - 估时: 0.15h
  - 依赖: T11.1

---

## Agent assignment (A.3)

| Task | Primary agent | Rationale |
|------|---------------|-----------|
| T1.0 probe + 分支决定 | **backend-architect** | Nomad job / cluster probe + repo grep, infra-domain |
| T2.1 layer2 HCL diff | **backend-architect** | HCL grammar + Nomad driver semantics |
| T2.2 runner-template HCL | **backend-architect** | 同 T2.1 |
| T2.3 constraint add | **backend-architect** | HCL constraint + node placement |
| T3.1 nomad/README 排查表 | **knowledge-manager** | 文档 + cross-ref |
| T3.2 AD-M1-8 Revised note | **knowledge-manager** | 文档 + decision graph maintenance |
| T4.1 convention doc 起草 | **knowledge-manager** | Lab-shareable convention authoring |
| T4.2 convention verify | **knowledge-manager** | 同上 (自验 D gate) |
| T5.1 conventions-summary 摘要 | **knowledge-manager** | 索引文档 |
| T5.2 README 表 | **knowledge-manager** | 索引文档 |
| T6 cred verify | **owner** (Rule #7) | SSH + secret round-trip, 不能委派 AI |
| T7 HCL activation | **owner** | `nomad job run` 需 cluster operator 权限 |
| T8 cold-pull live verify | **owner** | SSH + dispatch + alloc log inspection |
| T9 post_impl audit | **tech-lead** (orchestrator) + **qa-engineer** (verify) | 2-agent L2 proportionality |
| T10.1 standards commit/push/PR | **tech-lead** | 跨 submodule PR coordination |
| T10.2 aria-orch commit/push/PR | **tech-lead** | 同上 |
| T10.3 PR merge 顺序 + Rule #8 gate | **tech-lead** + **owner** (merge button) | merge 时机 + pre-merge gate |
| T11.1 Spec archive | **knowledge-manager** | 文档操作 |
| T11.2 memory writes | **knowledge-manager** | memory plan + MEMORY.md 索引 |
| T11.3 session handoff | **knowledge-manager** | Rule #9 doc |
| T11.4 Forgejo issue 闭/开 | **knowledge-manager** | issue tracker maintenance |

**Agent 总分布**: backend-architect (4) / knowledge-manager (10) / tech-lead (3 + 4 co-owned) / qa-engineer (1 co-owned) / owner (3 sole + 1 co-owned)

**Agent 加载顺序** (优化 fresh subagent 启动):
1. Phase B start: backend-architect (T1.0-T2.3) + knowledge-manager (T3-T5) **并行起 2 subagent**
2. Phase B verify (owner segments T6/T7/T8) — 等 owner
3. Phase C: tech-lead (T9 audit orchestrator) → tech-lead (T10 commit)
4. Phase D: knowledge-manager (T11)

---

## AD slot check (per `[[feedback_ad_slot_backfill_checkpoint]]`)

本 Spec **无 AD slot** (Level 2 Minimal, 无新 architecture decision; DEC-20260523-001 是本 Spec 的 scoping memo, 不是 AD 类决策)。AD-M1-8 是 reference 而非 new AD slot, T3.2 仅是 Revised note 不开新槽。

→ **无 `_待回填_` 风险**, AD slot check pass。

---

## Acceptance summary (机读 gate; 详 proposal §Acceptance)

| Gate | Trigger | Falsifiable command | Owner / AI |
|------|---------|---------------------|------------|
| A | Pre-merge | `grep -cE '^\s*auth\s*\{' aria-orchestrator/nomad/jobs/aria-{layer2-runner,runner-template}.hcl == 0` (双 HCL + nomad/jobs/ regression sweep) | AI |
| B | After T2.x commit, before T7 nomad job run | 3 节点 fingerprint sha256[:12] 全等 + 3 节点 curl --password-stdin 返 `200` | OWNER (Rule #7) |
| C | After T7 activation | 3 节点 docker rmi -f + dispatch + C2.5 alloc node verify + C3 alloc log "Pulling from" | OWNER |
| D | After T4 + T5 commit, before T10 PR merge | conv doc 存在 + 无 hardcoded 占位 + 双索引 + 9 段结构 + nomad/README 排查表 update | AI self-verify |

---

## Cross-references

- Spec proposal: `openspec/changes/aria-layer2-docker-auth-cold-pull-fix/proposal.md`
- DEC: `.aria/decisions/2026-05-23-layer2-docker-auth-cold-pull-fix.md`
- R1 audit: `.aria/audit-reports/post_spec-R1-2026-05-23T0900Z-aria-layer2-docker-auth-cold-pull-fix-orchestrator.md`
- R2 audit: `.aria/audit-reports/post_spec-R2-2026-05-23T1100Z-aria-layer2-docker-auth-cold-pull-fix-orchestrator.md`
- Parent M5 handoff: `docs/handoff/2026-05-23-m5-phase-c-o3-done-d2-close.md` §2 F2/F3 + §3 R2

---

**Created**: 2026-05-23
**Updated**: 2026-05-23 (initial draft post Phase A.1 + R1 + R2 + Rev2-micro)
**Author**: solo-lab (uni.concept.wzfq@gmail.com), drafted by Claude Opus 4.7

# aria-layer2-docker-auth-cold-pull-fix

> **Level**: Minimal (Level 2 Spec)
> **Status**: **Complete (2026-05-23 archived)** — Phase D.2 close gate MET: 3-way SHA parity verified (3 repos × 3 endpoints) post-merge + a8e0096 aria pointer regression patched + T6/T7/T8 owner-segment evidence PASS (per .aria/probes/2026-05-23-t6-t8-execution-evidence.md) + post_implementation 2-agent PASS_WITH_WARNINGS 0 Critical. Original Approved (Rev1.1, post R2 — 4-agent 4/4 PASS_WITH_WARNINGS converged + Rev2-micro). Spec archived to `openspec/archive/2026-05-23-aria-layer2-docker-auth-cold-pull-fix/`.
> **Created**: 2026-05-23
> **决策来源**: M5 Phase D.2 handoff `docs/handoff/2026-05-23-m5-phase-c-o3-done-d2-close.md` §2 F2/F3 + §3 R2
> **Probe grounded**: 2026-05-23 SSH 实地侦察 heavy-1/2/3 (per `[[feedback_prod_state_must_ground_playbook]]`)
> **Audit reports**: R1 `.aria/audit-reports/post_spec-R1-2026-05-23T0900Z-aria-layer2-docker-auth-cold-pull-fix-orchestrator.md` + R2 `.aria/audit-reports/post_spec-R2-2026-05-23T1100Z-aria-layer2-docker-auth-cold-pull-fix-orchestrator.md`
> **Ship target**: aria-orchestrator (no version bump — HCL change is deploy config not plugin SDK) + standards (new convention doc)

---

## Why

M5 Phase C O2 + O3 cold-dispatch 5 实证缺陷中,F2/F3 是 cluster-wide infra gap:

- **F2** (M5 §3 R2): Nomad HCL docker `auth { password = "${FORGEJO_BOT_PAT}" }` 块的 `${VAR}` interpolation 在 cold-pull 时**实测不可靠** (Nomad v1.11.2 + Forgejo registry 11.0.6 实证)。
- **F3** (M5 §3): Nomad default `gc.image_delay=3min` 加速 unused image GC,放大 F2。**F2 修了 F3 自然消失** (本 Spec scope 不动 image_delay)。

### 精确机制 (R1 M-ba-I-1 / M-km-C-1 closure)

为何同 `config {}` 块里 `image = "...sha256:${NOMAD_META_IMAGE_SHA}"` work 而 `auth { password = "${FORGEJO_BOT_PAT}" }` 不 work?

| Variable kind | 解析时机 | 来源 | 在 docker driver 调用前已 ready? |
|---|---|---|---|
| `${NOMAD_META_*}` | Nomad **native** interpolation, driver invocation 之前 | parameterized dispatch meta payload | ✅ |
| `${FORGEJO_BOT_PAT}` (来自 template stanza) | `template { env = true }` 渲染 task **process env**, driver invocation **之后** | Nomad Variables → template → /secrets/file.env → process env | ❌ docker driver 拿到 config 时 `${FORGEJO_BOT_PAT}` 仍 unresolved (literal 或空) |

→ docker driver 用空/literal password 试 registry auth → 401 → cold-pull fail。M1 demos "成功" 是 build-node 镜像缓存掩盖,F3 image_delay GC 后第一次冷拉就 fail。

### Aether vs Aria 时序矛盾 (R1 M-km-C-1 closure — 必须 surface)

| Date | Project | Nomad ver | Result | Source |
|------|---------|-----------|--------|--------|
| 2026-04-23 | Aether spike | (< v1.11.2) | **GO** — template `${VAR}` + auth block 工作 (11.5MB private image cold-pull, alloc d360435e) | `Aether openspec/archive/2026-04-22-fix-hardcoded-docker-auth` |
| 2026-05-23 | Aria M5 O3 live | **v1.11.2** | **FAIL** — cold-pull 401, ${FORGEJO_BOT_PAT} unresolved | M5 handoff §3 R2 实证 |

两次实测**同集群 30 天前 GO / 现在 FAIL**。本 Spec 不假装能解释根因(可能 Nomad upgrade / image size / `force_pull` flag / Forgejo upgrade), 但 convention §0 必须明确这个矛盾, 防其他 Lab 项目 (Kino/Kairos/psych-ai-supervision/SilkNode) 读 convention 时困惑。**Aria 当前实测立场 = 更新的 ground truth SOT**,严格禁 task-level `auth { ${VAR} }`组合。

### Probe 反转 scope (vs M5 handoff §2 原推荐)

| Item | 原假设 | Probe 实测 (2026-05-23 SSH heavy-1/2/3) |
|------|--------|-----------|
| Nomad config path | `/etc/nomad/` (M5 §2 推荐字面) | 实际 `/opt/nomad/config/` (systemd unit 验证) |
| 节点级 plugin `auth.config` 行 | 需新增 | ✅ 3/3 节点 `client.hcl` 已含 `plugin "docker" { config { auth { config = "/root/.docker/config.json" } } }` |
| `/root/.docker/config.json` 文件 | 需创建 | ✅ 3/3 已存在, top-level `auths.["forgejo.10cg.pub"]` |
| **真正阻断** cold-pull | (未确认) | HCL task-level `auth { ... }` block **override** 节点级 plugin (Nomad precedence: task > plugin) |

→ proper fix = **删 HCL auth block** + **verify config.json cred 有效性** + **convention 锁定 SOT** + **故障排查文档同步**。

**M6 soft-dependency** (R1 M-tl-M-3): M6 启动 soft-blocked 在本 Spec done (任何 M6 Layer 2 cold-dispatch 测试都会撞 F2)。本 Spec 既是 hygiene 又是 M6 准入。

## What

3 类 deliverable (HCL + cluster verify + docs):

### 1. HCL diff (AI segment, ~15min)

删 2 个 sister HCL 的 task-level docker `auth { ... }` block (各 ~5 行):
- `aria-orchestrator/nomad/jobs/aria-layer2-runner.hcl` 行 172-175
- `aria-orchestrator/nomad/jobs/aria-runner-template.hcl` 行 78-81 (M1 baseline)

`aria-runner-template.hcl` 整体处置走 **T1.0 probe** 决:
- (a) 仍 active (`nomad job status` returns + `dispatch-issue.sh` / `t5-run-demo.sh` 仍引用) → 同 aria-layer2 删 auth block, parity fix
- (b) registered 但无 recent dispatch → deprecate 注释 + 删 auth block + 保留文件 M1 reference
- (c) 未 registered → 整文件 deprecate 注释 (header 加 `# SUPERSEDED by aria-layer2-runner @ DEC-20260523-001`)

**注**: `dispatch-issue.sh` 行 26 `JOB_NAME="aria-runner-template"` 是 pre-existing script drift, 不在本 Spec scope, 但 T1.0 报告必标作 follow-up issue (M-qa-M-2)。

### 2. 集群 cred 验证 + 同步 (owner segment, ~20-30min)

config.json mtime 漂移 (heavy-1/2 = 2026-05-06 / heavy-3 = 2026-05-22 23:47 = M5 O3 debug 临时改) + file size 差异 (128B/129B/136B) 强烈暗示**3 节点 cred 内容不一致**。R1 M-ba-I-3 / M-qa-I-1 共识:length-equal 不能证 cred 等价 (per `[[feedback_test_mock_pattern_hides_prod_bug]]`)。

owner-action 步骤:
1. **Fingerprint 3 节点 cred (no value leak)**: SSH 各 heavy 跑
   ```
   python3 -c "import json,hashlib;d=json.load(open('/root/.docker/config.json'));print(hashlib.sha256(d['auths']['forgejo.10cg.pub']['auth'].encode()).hexdigest()[:12])"
   ```
   3 行输出全等 ⇒ 一致;任一不等 ⇒ drift。
2. **Round-trip auth verify per node**:
   ```
   docker login forgejo.10cg.pub -u aria-runner-bot --password-stdin < <(active-PAT-source)
   ```
   或等价 `curl -u aria-runner-bot:<PAT> https://forgejo.10cg.pub/v2/ -o /dev/null -w "%{http_code}"` 返 `200`。3/3 OK ⇒ cred valid。
3. **若 drift / FAIL**:进 R1 escalation path (见 §Risks R1)。

base64 encoding 规范 (R1 M-ba-I-4): 必须 `printf '%s' 'user:pass' | base64 -w0` (`-w0` 防 76-char line-wrap 在某些平台 decode 失败)。convention §4 锁死。

**Atomic 3-node sync** 规范 (若 drift fix):
- staging file 在 owner 本机 (不通过 chat) → `scp` to 3 节点 `/tmp/docker-config.json.new` → 各节点 `mv -f /tmp/docker-config.json.new /root/.docker/config.json` (atomic rename) → 立即跑 fingerprint verify
- **不需要** `systemctl restart nomad` (R1 M-ba-M-2 / M-qa-I-3 确证: docker driver per-alloc 读 `auth.config`,不需 restart)

### 3. 文档 + memory + AD update (AI segment, ~45-60min)

3a. **新 convention**: `standards/conventions/nomad-docker-registry-auth.md` (8 段, ~150-220 行):
- §0 Rationale + Observed contradiction (Aether GO 2026-04-23 vs Aria FAIL 2026-05-23)
- §1 Problem statement (M5 §3 R2 实证)
- §2 Mechanism (NOMAD_META_* vs template env 解析时序)
- §3 Forbidden pattern (HCL task `auth { password = "${VAR}" }` + template env 组合 — **scope 限**: envsubst/deploy-time substitution 模式如 Kino/Kairos `__REGISTRY_TOKEN__` 不在范围)
- §4 SOT pattern (节点级 `/root/.docker/config.json` schema spec + `base64 -w0` 规范 + Lab 占位符 `<bot-username>` / `<node-N>`)
- §5 PAT rotation playbook (**单向 reference** `secret-hygiene.md §2.4 + §3.6`, 不重复 docker login 安全 pattern;本段只写 Nomad-specific: atomic 3-node sync + round-trip verify + no chat-leak)
- §6 References (M5 handoff §3 R2 + Aether archived spec + 本 Spec archive 路径 + Forgejo issue 链)
- §7 Verification checklist (供已有 Nomad HCL 项目 self-audit:grep auth block count / check `${VAR}` template interpolation / verify client.hcl plugin config)
- §8 Migration path (已有 HCL 项目过渡步骤;envsubst 模式声明 out-of-scope)

3b. **故障排查表更新** (R1 M-km-C-2 — 主动误导必修): `aria-orchestrator/nomad/README.md` 行 170 改:
- 原: `image auth 失败 (401/403) | 检查 HCL config.auth.password template 指向 Nomad Variable 正确`
- 改: `image auth 失败 (401/403) | 检查节点级 /root/.docker/config.json cred (per standards/conventions/nomad-docker-registry-auth.md); task-level HCL auth block 已废弃`

3c. **AD-M1-8 Revised note** (R1 M-km-I-3): `aria-orchestrator/docs/architecture-decisions.md` §AD-M1-8 Status 追加:
- `Revised by DEC-20260523-001 — task-level docker auth block removed; node-level plugin auth.config is now SOT`

3d. **Memory plan** (R1 M-km-I-4): Phase D.3 写入
- **更新** `[[feedback_nomad_docker_auth_template_interp_gap]]`: 加 "10CG heavy-1/2/3 plugin auth.config 已 wired (2026-05-23 probe), HCL auth block 已删, 正式 fix 完成"
- **新增** `reference_10cg_nomad_docker_plugin_auth_wired`: 3 节点 client.hcl plugin 配置 + config.json 路径快照
- **新增** `feedback_probe_first_scope_reframe`: 本 Spec ~40% scope 收缩实证 (跨 session 第二次 `feedback_prod_state_must_ground_playbook` 应用)

### Key Deliverables (机读清单)

- `aria-orchestrator/nomad/jobs/aria-layer2-runner.hcl` (- ~5 行 auth block + 周围注释 reframe)
- `aria-orchestrator/nomad/jobs/aria-runner-template.hcl` (T1.0 决,但 auth block 至少 deleted/wrapped)
- `aria-orchestrator/nomad/README.md` 行 170 排查表 update
- `aria-orchestrator/docs/architecture-decisions.md` §AD-M1-8 Revised note (~1 行)
- `standards/conventions/nomad-docker-registry-auth.md` (新文件, 8 段, ~150-220 行)
- `standards/summaries/conventions-summary.md` (新增摘要条目)
- `standards/README.md` Development Conventions 表新增条目 (顺带 hygiene 补 secret-hygiene + session-handoff 索引缺失 — defer 由 owner 决, 非阻塞)
- `.aria/decisions/2026-05-23-layer2-docker-auth-cold-pull-fix.md` (probe finding + scope reframe + Aether contradiction 记录, **本文档**)
- Phase D.3: 3 memory entries (1 update + 2 new) + MEMORY.md 索引
- 主仓 commit + multi-remote dual push (origin + github):
  - aria-orchestrator submodule bump (HCL + nomad/README + AD update)
  - standards submodule bump (new convention + summary + README)
  - 主仓: 双 submodule pointer + openspec/changes/ → openspec/archive/

### Out of Scope (明确排除)

- ❌ **F3 image_delay 调整** — F2 修了自然消失;若 owner 仍要 pre-pull / `gc.image_delay=24h` 是独立 hygiene cycle
- ❌ **PAT 轮换主体** — `[[project_secret_rotation_deferred_2026-05-02]]` 4-key + 5-key 不在本 Spec(hard cap 2026-08-02); **但** 若 R1 触发, 本 Spec **可以 piggyback** active rotation 的 `FORGEJO_BOT_PAT` 单 key 同步动作 (见 §Risks R1)
- ❌ **aria-build.hcl / aria-layer1.hcl 修改** — Probe verified 无 docker auth block; 这两 HCL 既然 work 就证明 plugin auth.config 是已有 SOT, 删 aria-layer2 auth block 不影响其它 job (R1 M-qa-M-3)
- ❌ **节点级 plugin config 重新部署** — 已 wired
- ❌ **Vault / Workload Identity** — Aether #32 范畴
- ❌ **`dispatch-issue.sh` / `t5-run-demo.sh` script 更新** — pre-existing M1-era drift,T1.0 报告标 follow-up issue,不在本 Spec
- ❌ **跨项目 audit (SilkNode/Aether/Kairos/Kino/psych-ai-supervision)** — 由 consumer 项目下次 standards update 时自主 audit (R1 M-tl-I-3 + M-km-I-2);本 Spec convention 用 Lab 占位符 + envsubst 模式声明 out-of-scope

## Acceptance

**Ordering invariant (R1 M-ba-M-3)**: B 必须先验证通过, 才能将 deliverable A 的 HCL change 通过 `nomad job run` 激活到 cluster (HCL diff commit + PR 可与 B 并行, 但激活 = B 后)。

### A. HCL auth block 已删 — 两 HCL + 全 nomad/jobs/ 防回归

```bash
# A1: 主要 target
grep -cE '^\s*auth\s*\{' aria-orchestrator/nomad/jobs/aria-layer2-runner.hcl == 0
grep -cE '^\s*auth\s*\{' aria-orchestrator/nomad/jobs/aria-runner-template.hcl == 0
# (若 T1.0 分支 (c) 整文件 deprecate, deprecate 注释包整文件, grep 仍 == 0)

# A2: regression fence — 全 nomad/jobs/ sweep (R2 M-qa-N-3 fix: 与 A1 regex 一致)
grep -rcE '^\s*auth\s*\{' aria-orchestrator/nomad/jobs/ | grep -v ':0$' || echo "PASS"
```

3 行 PASS = A ok。

### B. 3 节点 cred 有效性已验证 (owner segment, per Rule #7 — 不漏 cred 字面值)

每节点跑 2 步。**R2 fix (M-cross-N-I-1)**: PAT 走 stdin 不进 curl `-u` arg, 避免 remote `ps aux` / bash_history leak。

```bash
# B1: fingerprint (no value leak — 12-char SHA prefix only)
ssh heavy-N "python3 -c \"import json,hashlib;d=json.load(open('/root/.docker/config.json'));print(hashlib.sha256(d['auths']['forgejo.10cg.pub']['auth'].encode()).hexdigest()[:12])\""
# 3 行输出全等 ⇒ 一致

# B2: round-trip auth via --password-stdin (PAT 走 stdin, 不进 process args)
ssh heavy-N "HISTFILE=/dev/null python3 -c \"import json,base64;d=json.load(open('/root/.docker/config.json'));print(base64.b64decode(d['auths']['forgejo.10cg.pub']['auth']).decode().split(':',1)[1])\" | curl -s -u aria-runner-bot --password-stdin -o /dev/null -w '%{http_code}\n' https://forgejo.10cg.pub/v2/"
# 期望输出 "200" — PAT 走 stdin 不在 process list 可见; HISTFILE=/dev/null 防 bash_history 留痕
```

3 节点全部 fingerprint 一致 + 全部 `200` ⇒ B PASS。任一 FAIL ⇒ 进 R1 escalation。

### C. Cold-pull live verify — 3 节点各 1 次, 真冷拉 (R1 M-ba-C-1 / M-qa-I-4 closure; R2 M-cross-N-I-2 加 C2.5 验证 alloc 真落到目标节点)

`nomad system gc` **不**清 docker image cache;改用 `docker rmi -f` 直接清。每节点 4 步:

```bash
# C1: SSH 到节点强清目标 image
ssh heavy-N "docker rmi -f forgejo.10cg.pub/10cg/aria-runner@sha256:<IMAGE_SHA> 2>/dev/null; docker images forgejo.10cg.pub/10cg/aria-runner | grep -c '<IMAGE_SHA_first12>' || echo 0"
# 期望 "0" — 镜像已清

# C2: 用 per-node constraint 强 dispatch 到该节点
# (T1.0 必须先 verify HCL 含 constraint { attribute = "${node.unique.name}" value = "${NOMAD_META_TARGET_NODE}" };
#  若 HCL 未含, A.2 tasks.md 加临时 patch 或改用 alloc-level placement preference)
DISPATCH_OUT=$(nomad job dispatch -meta IMAGE_SHA=<sha> -meta TARGET_NODE=heavy-N aria-layer2-runner 2>&1)
ALLOC_ID=$(echo "$DISPATCH_OUT" | grep -oE 'Allocation .{8}' | awk '{print $2}')

# C2.5: ⚠ 验证 alloc 真落到目标节点 (R2 M-cross-N-I-2 — 否则 silent-pass 3 次同节点)
nomad alloc status $ALLOC_ID | grep -E 'Node Name|^Node ' | head -1
# 期望含 "heavy-N" 字符串 (与 dispatch 目标一致); 否则 abort + escalate (HCL constraint 缺失)

# C3: 拉证据 — alloc log 必须含 "Pulling from forgejo.10cg.pub" 行 (而非 "Status: Image is up to date")
nomad alloc logs $ALLOC_ID 2>&1 | grep -E 'Pulling from|Downloading' | head -3
```

3/3 节点 PASS (C1+C2.5+C3 全过) ⇒ C ok。任一 FAIL ⇒ HCL change 不应激活 (rollback 到 HCL with auth block 暂时 — 但本 case 已知 HCL auth block 也不工作, 真正 fallback = open emergency cred refresh issue per §Risks R1 escalation path)。

### D. Convention 文档已 ship + 索引 + 内部 section 完整 (AI segment self-verify, after commit before PR)

R2 M-qa-N-4: 标 AI segment 归属;R2 M-km-N-3: D1 拆 2 步避免 `[ -f ] && grep` 复合歧义。

```bash
# D1a: 文件存在
[ -f standards/conventions/nomad-docker-registry-auth.md ] || { echo "FILE_MISSING"; exit 1; }

# D1b: Lab-shareable (无 hardcoded heavy-N / aria-runner-bot — 全占位符)
grep -cE 'heavy-[1-3]|aria-runner-bot' standards/conventions/nomad-docker-registry-auth.md  # 期望 0

# D2: 索引出现 (双索引位)
grep -c 'nomad-docker-registry-auth' standards/README.md  # >= 1
grep -c 'nomad-docker-registry-auth' standards/summaries/conventions-summary.md  # >= 1

# D3: 9 段结构完整 (§0..§8)
grep -cE '^## §[0-8] ' standards/conventions/nomad-docker-registry-auth.md  # == 9

# D4: nomad/README 排查表已 update (不再误导)
grep -c 'task-level HCL auth block 已废弃' aria-orchestrator/nomad/README.md  # >= 1
```

全 PASS ⇒ D ok。

## Risks

### R1: Cred drift 发现 (B FAIL) → 必须 piggyback 或独立 escalate

R1 audit 共识 (M-tl-I-2 + M-qa-I-2): 原 "独立 PAT rotation cycle" 是 dead reference。Mitigation 决策树:

1. 第一步:**查 active rotation 状态** — `cat .aria/decisions/2026-05-20-secret-rotation-during-m5-deploy.md` §1 Layer 1 + `[[project_secret_rotation_deferred_2026-05-02]]`
2. **若 `FORGEJO_BOT_PAT` 在 in-flight rotation 子集**:把 B sync + Layer 1 rotation 合并为同一 owner-action segment (节省一次 atomic 3-node sync),本 Spec B 走 piggyback。完成后继续 A/C/D。
3. **若 cred 真 stale 且不在 active rotation**:
   - `forgejo POST /repos/10CG/Aria/issues` 新建 issue, 标 label `P0 blocker` + `secret-rotation`, 关联 `.aria/decisions/2026-05-20-secret-rotation-during-m5-deploy.md`
   - 本 Spec proposal 顶部 Status 改为 `Blocked on Forgejo #<NEW>`
   - rotation done 后回填本 Spec, 继续 A/C/D

### R2: aria-runner-template.hcl 处置 + dispatch-issue.sh script drift

T1.0 probe 后选 (a)/(b)/(c) 分支,每分支 commit message 不同 (per R1 M-tl-M-2):
- (a) → `feat(layer2): delete docker auth block from 2 HCLs (aria-layer2-runner + aria-runner-template)`
- (b) → `feat(layer2): delete auth block from aria-layer2-runner; deprecate aria-runner-template (M1 baseline, no recent dispatch)`
- (c) → `feat(layer2): delete auth block from aria-layer2-runner; supersede aria-runner-template (file deprecate, M1 archive)`

dispatch-issue.sh + t5-run-demo.sh 仍指 `aria-runner-template` 是 pre-existing drift,T1.0 报告标 follow-up issue,**不**在本 Spec scope。

### R3: Owner round-trip verify 时 PAT/base64 字面值漂入 chat

Mitigation:
- B1 fingerprint 命令只 print 12-char SHA prefix,不漂 cred
- B2 round-trip 用 `<()` process substitution 让 PAT 仅在 ssh remote shell 内 expand,不通过 stdout (注意 `2>&1` 不要用)
- 本 Spec 不要求 owner 把任何 base64 cred / PAT 字面值粘到 chat;若需修复 drift, atomic sync 走 scp 本机 → 节点不经 chat (per Rule #7 + `[[feedback_secrets_never_in_conversation]]` + `[[feedback_nomad_inspect_secret_leak]]`)

### R4: config.json 改动是否需 Nomad restart? **不需要 (确证)**

R1 M-ba-M-2 / M-qa-I-3 closure: Nomad docker driver 在**每次 alloc 调度时**重新读 `/root/.docker/config.json` (filesystem read per dispatch),不需 `systemctl restart nomad`。仅当 `client.hcl` 中的 `auth.config` **路径**变更才需 restart (本 case 不变,仅改文件内容)。

### R5: Merge-order vs `aria-secret-guard-plugin-default` track — RESOLVED 2026-05-23

R1 M-tl-I-1: 两 Spec 都在 standards/ 写文件:
- secret-guard → 改 `standards/conventions/secret-hygiene.md` (Layer 2 enforcement 段) — **DONE 2026-05-23 via standards PR #8, ship 在 v1.1.0**
- 本 Spec → 新建 `standards/conventions/nomad-docker-registry-auth.md` (Phase B 实施)

**无写冲突** (不同文件)实证: 本 Spec Phase A.1 起草期间, dev-claude2 终端**并行 ship** secret-guard Phase B+C+D (主仓 `246a4a2`, aria-plugin v1.24.0, standards `b3cc647`), 我的 5 文件零冲突 fast-forward。**Self-multi-container coordination 测试通过** (Q2 owner 选 "先本 Spec" 但 secret-guard 在另一 terminal 并行推进, 实际成 (a) 并行执行)。

剩余 invariant: 本 Spec Phase B 在 standards/ 创新 file `nomad-docker-registry-auth.md` + 可在 §6 References 单向 cross-link 到 secret-hygiene.md v1.1.0 (现已是 ship 版本, 无 dangling ref 风险)。

## 取舍 (TLDR)

| 维度 | 选择 | 理由 |
|------|------|------|
| Level | 2 (Minimal) | owner 已决 — Scope clear, 无设计不确定性 |
| Audit mode | full 4-agent × R1+R2 | owner 已决 (proposal R1 audit 已跑, 4 Critical 全在本 Rev1 修) |
| Branch | `feature/layer2-docker-auth-fix` (主仓 + 2 submodule 同名) | 跨 submodule 协调 |
| 验收 gate | A + B (ordering invariant: B 先) → C (live cold-pull 3/3) → D | C 是唯一 ground truth |
| Merge-order vs secret-guard | 独立 (不同 standards 文件,无写冲突) | R1 M-tl-I-1 closure |
| Lab 跨项目 scope | convention 用占位符;不主动 audit SilkNode/Aether/Kairos | R1 M-tl-I-3 + M-km-I-2 closure |

## Owner Decisions Recorded (Q1-Q4 from 2026-05-23 dialog)

| Q | Decision | 体现位置 |
|---|----------|----------|
| Q1 Level 2 vs 3 | **L2 (Minimal)** | proposal frontmatter + §取舍 |
| Q2 vs `aria-secret-guard-plugin-default` priority | **先本 Spec** (实际成并行 — dev-claude2 终端 2026-05-23 同 session 并行 ship secret-guard v1.24.0, 无冲突) | §Risks R5 + §Why M6 dependency |
| Q3 `aria-runner-template.hcl` 处置 | **T1.0 probe 后决** (a/b/c) | §What §1 + §Risks R2 |
| Q4 post_spec audit mode | **4-agent × R1+R2 全量** | proposal frontmatter Status + audit report 路径 |

---

**Status changes**:
- 2026-05-23 ~06:30 UTC: Draft v1 (initial probe + scope reframe + Spec draft 同 session)
- 2026-05-23 ~10:00 UTC: Draft v2 / Rev1 (post R1 audit sweep — 4 Critical + 8 cross-cutting Important + ~6 absorbed Minor; ready for R2 verify)

**Next step**: R2 4-agent verify (Task #3) → A.2 tasks.md (Task #4) → A.3 agent assignment (Task #5) → commit + dual-push (Task #6) → Phase B (HCL edit + convention doc + owner verify B+C) → Phase C/D。

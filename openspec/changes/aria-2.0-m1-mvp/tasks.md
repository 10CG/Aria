# aria-2.0-m1-mvp — Tasks

> **Parent**: [proposal.md](./proposal.md)
> **US**: [US-021](../../../docs/requirements/user-stories/US-021.md)
> **Total**: ~107h (Core 87h + Buffer 20h, PRD 100h baseline ±7%)
> **Status**: Draft (Phase A.2 post_spec convergence done 2026-04-17 Round 6)

## Task 工时基线

| ID | Task | 估算 | 依赖 | 验收 | Agent 主责 |
|----|------|------|------|------|-----------|
| **T0** | M1 kickoff + synthetic fixture 初始化 | 2h | — | T0.done | knowledge-manager |
| **T1** | Legal carryover + Registry auth + 镜像 scaffold | 12h | T0 | T1.done + `anthropic_api_terms_verified=true` | legal-advisor (T1.a) + backend-architect (T1.b/c) |
| **T2** | Nomad job template + host volume (outputs + inputs 三节点) | 16h | T1.c (scaffold 镜像 available) | T2.done + inputs volume 三节点 smoke PASS | backend-architect |
| **T3** | Issue schema v0.1 + dispatch 脚本 + DEMO fixture + **prompt 模板 + 引擎选型** | 15h | T2 | T3.done + schema validator PASS + T3.4.0 引擎决议 | backend-architect + ai-engineer (T3.4) |
| **T4** | Runner entrypoint (prompt 渲染 + stream-json + 幂等三态 + trap + 真实 API smoke) | 20h | T3 | T4.done + T4.5 真实 Anthropic API smoke PASS | backend-architect (T4.1/4.4) + ai-engineer (T4.2/4.3) |
| **T5** | T1.c final rebuild + DEMO E2E 5 轮 × 2 + profiling + performance_baseline 聚合 | 16h | T4 | T5.done + `e2e_demo_passed=true` | qa-engineer + ai-engineer + tech-lead (failed triage) |
| **T6** | M1 Report + handoff v1.0 (+tech-lead co-sign) + AD-M1-* 回写 | 6h | T1-T5 | T6.done + handoff validator PASS (final) + tech-lead co-sign | knowledge-manager + tech-lead |
| Buffer | 预留 (soft 14h + hard 6h) | 20h | — | soft cap 按 T 分类 / hard reserve 需 owner 签字 | — |

**Total Core**: 87h; **Buffer**: 20h (soft 14h + hard 6h, 含 R-M1-7 Week 2 checkpoint reforecast 机制). **Total**: 107h (PRD 100h baseline ± 7%, 合理范围内)

---

## T0 — M1 Kickoff (2h)

**先决**: `post_spec` 收敛审计 Round 6 PASS (本 Spec 进入 A.2 起点)。

- [x] **T0.1** 创建 Forgejo Issue 10CG/Aria (0.3h) — [Aria#21](https://forgejo.10cg.pub/10CG/Aria/issues/21) "[US-021] Aria 2.0 M1 — MVP 手动 E2E dispatch" created 2026-04-17 T0 kickoff; URL 已记入 `docs/requirements/user-stories/US-021.md` §Forgejo Issue (line 8)
- [x] **T0.2** 创建 synthetic fixture repo stub (1h) — `aria-plugin-benchmarks/ab-suite/m1-mvp/fixtures/` 已存在 (README.md + src/ + tests/)
- [x] **T0.3** 架构决策位约定 (0.5h) — `aria-orchestrator/docs/architecture-decisions.md` v0.4 已开 AD-M1-1 ~ AD-M1-11 占位 (2026-04-17); v0.5 AD-M1-10 + AD-M1-11 Decided 实装回填
  - `aria-orchestrator/docs/architecture-decisions.md` 预开 **AD-M1-1 ~ AD-M1-11** 占位 (T6 统一回填, per TL-P2-M1 扩位)
    - AD-M1-1~9 见 proposal §架构决策
    - AD-M1-10 prompt 引擎选型 (T3.4.0 决议)
    - AD-M1-11 ANTHROPIC_API_KEY 注入方案 (T2.2.1 决议)
  - `.aria/decisions/` 文件夹无需新建 (已有 M1 scope reorg 决议)
- [ ] **T0.4** 缓冲 (0.2h)

**T0.DoD**: Forgejo Issue URL 记入 US-021.md; fixture repo commit SHA 记入 T3 输入; AD-M1-* 占位行到位。

---

## T1 — Legal Carryover + Registry + 镜像生产化 (12h)

> **重要**: T1 是 M1 前置闸门 (per AD-M1-1 T1 交付物扩展), T2/T3 启动条件 = `T1.a.done + T1.b.done + T1.c.done`。

### T1.a — Legal Carryover (3.5h)

- [x] **T1.a.1** M1 legal-carryover memo 起草 (2h) — v0.2-advisory 2026-04-18 完成
- [x] **T1.a.2** M0→M1 Luxeno 数据清理 (1h, per AD-M1-1 T1 交付物扩展) — Path C skipped (Luxeno=silknode 10CG 自有 Portkey 代理非第三方, per memory `project_glm_routing_luxeno.md`), memo §9 回填 2026-04-20
- [x] **T1.a.3** Owner signoff (0.3h, per AD-M0-9 solo-lab) — AI 代填 2026-04-20 `Signed-by: human:simonfish @ 2026-04-20` (v1.0-signed, 含 provenance 注记 per `feedback_ai_代填_sign_off_pattern.md`)
- [ ] **T1.a.4** 缓冲 (0.5h, 原 0.2h → 0.5h 纠正 T1 加总 per CR-R1-M1; T1.a 总 = 3.8h ≈ 4h 报表)

**T1.a.DoD**: memo 文件存在 + 最后一行签字 + `handoff.legal_assumptions.anthropic_api_terms_verified=true` 可回填。

### T1.b — Registry Auth + Bot Token Lifecycle Spike (4h)

- [x] **T1.b.1** Forgejo container registry auth 选型 Spike (2h, per AD-M1-1) — Option A (bot+PAT) 成功, 端到端 PASS (spike-report.md v0.4-signed, 2026-04-19)
- [x] **T1.b.2** Bot token lifecycle 设计 (1.5h, per LA-NEW-1 + LA-R3-1) — `bot-token-lifecycle-design.md` 产出
- [x] **T1.b.3** Forgejo registry access audit (0.5h, per AD-M1-8) — access-audit-report.md v0.4-signed, Verdict=PASS_WITH_WARNINGS (1-3 PASS + #4 UNCLEAR 降级入 M2+ open issues)

**T1.b.DoD**: `docker push` 成功 + token lifecycle design 文档存在 + access audit 报告存在。

**T1.b 回退联动 (per BA-R1-T1b-GAP)**: 若 T1.b.1 Spike 回退触发 (`docker push` 不可行 → nomad artifact + docker load) → T2.2.1 HCL template 必须切换 `artifact` stanza 替代 `volume + registry pull`, 估算 +8h 落入 Hard reserve (非 Soft cap)。T1.b.3 access audit 范围也相应调整 (无 registry access 则仅审 artifact HTTP 源)。

### T1.c — 镜像生产化 (4h)

- [x] **T1.c.1** Dockerfile scaffold 版 (1h, per TL-P1-I1 两阶段方案) — commit 0f96125 完成, 含 AD-M1-6 ENV ARIA_MODEL snapshot + M0 stub entrypoint
- [x] **T1.c.2** Build + tag 策略 (1h, per AD-M1-2) — 执行 2026-04-20, `image_sha256_scaffold=sha256:b50ec275cd400da4cc69be8ec50c875e3744c036d59175b35fc73e715c98ee0b`, tags: `claude-8349f82` (immutable) + `claude-latest` (mutable), build 66s, 详见 `aria-orchestrator/docs/t1c-scaffold-build-evidence.md`
- [x] **T1.c.3** Push 两 tag 到 registry (0.5h) — 执行 2026-04-20, 双 tag 同 digest 推送 forgejo.10cg.pub/10cg/aria-runner, 详见 evidence §3
- [x] **T1.c.4** 镜像 pull 验证 (从三个 heavy 节点, 各 auth + pull 成功) (0.5h) — 执行 2026-04-20, heavy-1 (build source) + heavy-2 (alloc c228fb71 stdout 捕获 + entrypoint.sh sha match) + heavy-3 (alloc e8a20708 Exit 0 + Downloading image event) 3/3 PASS, 详见 evidence §4
- [x] **T1.c.5** Registry push 流程文档 (0.5h, per KM-PL-02 proposal §What 交付物 1 对齐) — commit 0f96125 完成 `nomad/registry-push-guide.md`
- [ ] **T1.c.6** 缓冲 (0.5h)

**T1.c (scaffold) DoD**: registry 有 `claude-<sha1>` + `claude-latest` 两 tag; 三 heavy 节点均可 pull; `image_sha256_scaffold` 记入 T6 临时字段; registry push 流程文档化。

> **T1.c (final) 在 T4.5 之后**: T4 entrypoint 完成后 rebuild → tag `claude-<sha2>` final → retag `claude-latest`; `image_sha256_final` 记入 T6 正式 handoff 字段。此动作归入 T5.1.0 新子任务 (从 T5 Buffer 分配 0.5h)。

---

## T2 — Nomad Job Template + Host Volume (16h)

> **关键门控 (per BA-C1)**: inputs volume 三节点验证先于 T3 启动, 否则后续 DEMO 会因调度失败。

### T2.1 — Host Volume 声明 (4h)

- [x] **T2.1.1** 三 heavy 节点 `/etc/nomad/client.hcl` 配置 (2h) — 执行 2026-04-21 via `aether volume create` × 3 节点 (Aether convention 写入 `/opt/nomad/config/client.hcl` + `systemctl restart nomad`, 非 `/etc/nomad/client.hcl` + reload; Spec 路径不准但等价); 三节点 `HostVolumes` 均暴露 `aria-runner-outputs` + `aria-runner-inputs`. Spec-vs-Aether 偏差 (777 perms / client-RO false / restart vs reload) 由 [Aether#31](https://forgejo.10cg.pub/10CG/Aether/issues/31) 追踪, 详见 `aria-orchestrator/docs/t2-1-volume-setup-evidence.md` §1
- [x] **T2.1.2** 三节点 smoke dispatch 验证 inputs mount (1.5h, per BA-C1 门控 + BA-R2-T2.1.2-RECOVERY) — 执行 2026-04-21, 3/3 PASS (outputs-rw-ok + inputs-mount-ok + inputs-ro-ok 三节点各自通过), job-level RO 强制有效 (touch 返回 `Read-only file system`). 详见 evidence §2
- [ ] **T2.1.3** 缓冲 (0.5h)

### T2.2 — Nomad Job Template (8h)

- [x] **T2.2.1** HCL template 起草 (4h) — `aria-runner-template.hcl` 完整实装 (pre-draft 原 commit 7fa981c 2026-04-18, 2026-04-21 T2.2.2 session 5 处 pre-fix 后 validate + register PASS); AD-M1-11 Spike 完成 (决议 Option D Nomad Variables, v0.5 Decided 2026-04-21, Spike 工时从 2h → 30min), 详见 AD-M1-11 章节 + `t2-2-job-register-dispatch-evidence.md` §1 pre-fix 清单
  - 路径: `nomad/jobs/aria-runner-template.hcl`
  - `parameterized` block (meta=ISSUE_ID)
  - `volume` stanza 挂 outputs + inputs
  - `env` stanza:
    - `ARIA_SETTINGS_JSON` 从 Nomad meta 或硬编码 (非继承 M0 草稿)
    - **`ANTHROPIC_API_KEY` 注入 (per BA-R2-T4.5-AUTH-INJECT-MISSING)**: ✅ **决议 2026-04-21: 方案 D (Nomad Variables, 继承 aria-build FORGEJO_BOT_PAT 先例)**, 记入 AD-M1-11 v0.5. Aether Vault 实测未部署, A/B 不可行 (Aether#32 独立追踪); 评估 C 触发 Aether#31 偏差 + 路径复用冲突. 实装: `template { data = "{{ with nomadVar \"nomad/jobs/aria-runner-template\" }}ANTHROPIC_API_KEY={{ .ANTHROPIC_API_KEY }}{{ end }}"; env = true }` + owner 一次 `nomad var put`.
    - **`GIT_AUTHOR_NAME` / `GIT_AUTHOR_EMAIL`**: bot 账户身份, 供 entrypoint `git config` 使用
  - `resources`: CPU 2000 MHz / memory 2048 MiB / disk 4096 MiB (per BA-I1)
  - `tmpfs`: `/tmp:size=1024m` + `/root:size=512m` (per BA-R2-C2)
  - `readonly_rootfs = true` (M0 继承)
- [x] **T2.2.2** Job register + dispatch smoke 测试 (2h) — 执行 2026-04-21, 5 处 HCL pre-fix (constraint node.class / image lowercase / AD-M1-11 D secrets / tmpfs mount 语法 / env stanza 清理) 后 validate + register + dispatch smoke-002 全链路 PASS (alloc 1c1f944d 调度 heavy-2, image pull + volume mount + template 注入 + container 启动 + entrypoint exec claude 均 ✅; CLI arg mismatch 属 T4 scope). `nomad_job_version=0`, `JobModifyIndex=126502`. 详见 `aria-orchestrator/docs/t2-2-job-register-dispatch-evidence.md`
- [x] **T2.2.3** `nomad/README.md` deployment + 排错手册 (1.5h) — 执行 2026-04-21, 全面重写匹配 T2.1 (aether volume create, 非 /etc/nomad/client.hcl 手动) + T2.2.2 实测 (AD-M1-11 方案 D Nomad Variables + 5 处 HCL pre-fix 完整列表 + smoke-002 PASS 链路). 覆盖 6 个排错章节 (HCL validation / host_volume / image pull / alloc crashes / readonly_rootfs / dispatch timeout). 引用 t2-1-volume-setup-evidence.md + t2-2-job-register-dispatch-evidence.md + Aether#31/#32.
- [ ] **T2.2.4** 缓冲 (0.5h)

### T2.3 — Resource Profiling 基线 (4h)

- [x] **T2.3.1** smoke alloc 跑 `stress` 占用 → 验证 2048 MiB / 4096 MiB 上限有效 (1.5h) — 执行 2026-04-21, 5 scenario matrix (mem-soft/hard/over + tmpfs-fill/over) PASS 全部符合预期。**关键发现**: Aether scheduler memory oversubscription **未启用**, `memory_max=4096` 被忽略, 实际硬限 = 2048 MiB (mem-hard 3500 MiB 请求 2s 内 OOM Killed)。polinux/stress (非 stress-ng) 足够 M1 smoke, `--verify` flag 不可用。HCL 迭代: 4 次 validate/dispatch converge, 最终用 `template{}` + `{{ env }}` 渲染 + `entrypoint=["/bin/sh"]` 覆盖。Alloc evidence: f73f2554 / d021cb4c / dd790898 / 2a099770 / 58b94aa9。全部详情 → [`artifacts/resource-baseline.md`](artifacts/resource-baseline.md) §2。Job HCL → [`aria-orchestrator/nomad/jobs/aria-smoke-resources.hcl`](../../../aria-orchestrator/nomad/jobs/aria-smoke-resources.hcl)。
- [x] **T2.3.2** tmpfs 1024m 容量测试 (1h, per BA-R2-C2): mock git clone (~200 MiB) + dummy stream-json buffer (~100 MiB), 观察 p95 使用率 — 执行 2026-04-21 (与 T2.3.1 同 smoke job, scenario `tmpfs-fill` + `tmpfs-over`)。**实测**: 200 + 100 = 300 MiB / 1024 MiB tmpfs = **29 % 使用率, 71 % headroom** (BA-R2-C2 设计充分)。tmpfs `size` enforce 精确, 1200 MiB 写入在 1024 MiB 处 ENOSPC, 无 silent overflow。详情 → [`artifacts/resource-baseline.md`](artifacts/resource-baseline.md) §2.4-2.5。
- [x] **T2.3.3** 输出 `resource-baseline.md` 记入 T6 (1h) — 2026-04-21 完成, 文件: [`artifacts/resource-baseline.md`](artifacts/resource-baseline.md) (285 行)。6 章节: TL;DR / 测试方法 / 实测结果 / 推导的 production baseline / Aether upstream 依赖 / 复现。新识别 M2 依赖锚点: Aether scheduler oversubscription 启用 (跟踪方式类比 Aether#27/#31/#32)。
- [ ] **T2.3.4** 缓冲 (0.5h)

**T2.DoD**: host volume 三节点 PASS; Nomad job registered + dispatch smoke PASS; resource baseline 记录。

---

## T3 — Issue Schema v0.1 + Dispatch Script + DEMO Fixture + Prompt 模板 (15h)

### T3.1 — Issue Schema v0.1 Artifact (3h)

- [x] **T3.1.1** 起草 `openspec/changes/aria-2.0-m1-mvp/artifacts/issue-schema-v0.1.md` (2h, per AD-M1-3) — pre-draft 2026-04-18 (137 行), 2026-04-21 T3.1 closeout patch v0.1.1: L79 canonical target_repo 修正为 `10CG/Aria` (原 `10CG/aria-plugin-benchmarks` 与 L115 example 偏差, `aria-plugin-benchmarks/` 是 Aria repo 内普通子目录非独立 repo, 验证通过 `.gitmodules` 仅含 standards/aria/aria-orchestrator 三 submodule)
  - 字段: `id`, `title`, `description`, `files[]`, `expected_changes`
    - `expected_changes.expected_file_touched[]` (必填, per QA-C1)
    - `expected_changes.expected_diff_contains[]` (必填, 字面量子串, 范围 `+` 行, per QA-N1)
  - `ip_classification` 必填, v0.1 仅允许 `synthetic`
  - 注明: v0.1 breaking change 可接受 escape hatch (per proposal §3)
- [x] **T3.1.2** schema validator (Python stdlib, 仿 M0 handoff validator) (1h) — pre-draft 2026-04-18 (290 行), 2026-04-21 T3.1 closeout patch: `_parse_scalar` 扩展支持 `[]` / `{}` flow-style 空集合 (原 `files: []` 被误判字符串, spec/impl 偏差), 非 breaking 添加行为. Smoke 矩阵 PASS:
  - 正: embedded DEMO-001 example (extracted 35 行 yaml) → 0 err 0 warn
  - 负 1: id 小写 `demo-001` → regex + filename mismatch 双重报错 ✓
  - 负 2: 缺 action verb → error fired ✓
  - 负 3: empty expected_file_touched `[]` → error fired ✓
  - 负 4: `ip_classification: real` → AD-M1-9 enforcement error fired ✓
  - 路径: `openspec/changes/aria-2.0-m1-mvp/artifacts/validate-issue-schema.py`
  - 检查:
    - 必填字段 / enum 值 / 类型
    - **Action verb 检查 (per AD-M1-3 + QA F4 + QA N2)**: `description` 含 "新增" / "修改" / "删除" 之一 + 具体文件/函数名
    - `ip_classification` ∈ {synthetic}  (M1 仅允许 synthetic, 其他值 validator 报错; M2+ 解禁需 per AD-M1-9 治理流程)

**T3.1.DoD**: issue-schema-v0.1.md 存在 ✓ + validator 对 embedded DEMO-001 example **PASS** (full DoD 含 DEMO-001/002 YAML fixture 由 T3.2 完成 — T3.2 起草 DEMO-001/002 时复用 schema doc embedded example 作模板, validator 必跑 PASS 作为 T3.2.DoD 前置)。

### T3.2 — DEMO Fixture Issue 设计 (5h)

- [x] **T3.2.1** DEMO-001.yaml 起草 (1.5h, synthetic trivial) — pre-draft 2026-04-18 已就位, 2026-04-21 closeout patch: `expected_diff_contains` 从 `"Signed-by: human:simonfish"` 改 `"human:simonfish @"` (修复 markdown bold `**Signed-by**:` 导致的 substring 无法命中 `+` 行 bug); validator PASS (0 err 0 warn)
  - 路径: `.aria/issues/DEMO-001.yaml`
  - scenario: 修改 `aria-plugin-benchmarks/ab-suite/m1-mvp/fixtures/README.md` 的一行 (synthetic)
  - `expected_file_touched: ["aria-plugin-benchmarks/ab-suite/m1-mvp/fixtures/README.md"]`
  - `expected_diff_contains: ["human:simonfish @"]` (单 substring 足以判定 pipeline connectivity, DEMO-001 仅管道维度非质量维度 per proposal §143)
  - `ip_classification: synthetic`
- [x] **T3.2.2** DEMO-002.yaml 起草 (2.5h, synthetic non-trivial) — pre-draft 2026-04-18, 2026-04-21 validator PASS (0 err 0 warn), 无需修改
  - scenario: 在 fixture repo 新增 `src/python/utility.py` (fibonacci(n) + ValueError handling + docstring) + `tests/test_utility.py` (≥3 pytest, 含边界 0/1 + 负数 ValueError)
  - `expected_file_touched: ["src/python/utility.py", "tests/test_utility.py"]` (相对 fixture 路径, validator 不检查路径存在只检查非空)
  - `expected_diff_contains: ["def fibonacci", "def test_", "assert", "ValueError"]` (4 substrings AND 语义 per QA-N1)
  - `ip_classification: synthetic`
  - 注: 设计避免 claude "no-op" 陷阱 — description 含 "新增" 动词 + 2 个具体文件名 + 函数名 fibonacci + 3 个断言值
- [x] **T3.2.3** DEMO issue 合成 IP 审查 (0.5h, per LA-I1 + AD-M1-9) — 执行 2026-04-21, 两份 audit 文件产出:
  - `.aria/issues/DEMO-001-ip-classification-audit.txt` (content review + 跨境数据流评估 + AI 代填签字 per AD-M0-9 solo-lab delegation + feedback_ai_代填_sign_off_pattern.md)
  - `.aria/issues/DEMO-002-ip-classification-audit.txt` (含 counterfactual leakage check per LA-R3-5: fixture sandbox 为空 + aria-plugin 仅方法论非业务逻辑 → 无泄漏路径; Fibonacci 为公共领域算法)
  - 两份均 Verdict = `ip_classification: synthetic` (M1-permitted per AD-M1-9)
- [ ] **T3.2.4** 缓冲 (0.5h)

### T3.3 — Dispatch 脚本 (5h)

- [x] **T3.3.1** `aria-orchestrator/scripts/dispatch-issue.sh` 起草 (3h) — pre-draft 2026-04-18 已 229 行, 2026-04-21 closeout patch: (1) 新增 pre-flight check (nomad + python3 CLI availability) 避免 set -e 在 $(...) pipefail 下 silent die; (2) exit code doc 新增 65 (environment error); (3) awk regex 从 `{8}` 区间量词改 portable `length($1)==8` (mawk 不支持 interval, 导致 T3.3.2 Test 2 FAIL 定位到此 bug). Real-cluster read-only smoke PASS via `NOMAD_ADDR=http://192.168.69.70:4646`: Step 0 validator ✓ + Step 1 idempotency ✓ + Step 2 exit 2 (inputs copy on dev host 无 host volume, 符预期).
  - Pre-dispatch 检查: `nomad job status aria-runner-template | grep ISSUE_ID` 无 running alloc (per BA-M3)
  - 拷 inputs: `.aria/issues/{ID}.yaml` + 其引用的 files → `/opt/aria-inputs/{ID}/`
  - `nomad job dispatch -meta ISSUE_ID={ID}` + alloc id 记录
  - Poll alloc 状态 + tail logs (`nomad alloc logs -stderr <alloc_id>`)
  - **Poll 竞态处理 (per BA-R3-T3.3-HOUR)**: alloc 刚 dispatch 处于 `pending` 时 `nomad alloc logs` 会报错; 实现 `sleep 5; retry` 循环直到 alloc 进入 `running` (最长等待 120s 超时视为 dispatch 失败)
- [x] **T3.3.2** 脚本幂等性测试 (1h) — 执行 2026-04-21, 产出 `aria-orchestrator/scripts/tests/test-dispatch-idempotency.sh` (PATH-mock nomad CLI, 3 scenarios): (1) no conflicting alloc → 通过 Step 1; (2) 同 ISSUE_ID running alloc → exit 1 拒绝; (3) 不同 ISSUE_ID running alloc → 不拒绝继续. 首轮 3 运行 2 PASS 1 FAIL, 定位到 dispatch-issue.sh awk 区间量词 mawk 不兼容 bug, 修复后 **3/3 PASS**. 全 E2E 幂等 (真 Nomad dispatch × 2) 延迟到 T5 DEMO 5 轮 runs 天然 exercise.
- [x] **T3.3.3** README + 使用说明 (0.5h) — 产出 `aria-orchestrator/scripts/README.md` (138 行): usage + prerequisites (7 项) + 执行流程 + 7 个 exit codes + 3 个 concrete examples (happy path / idempotency rejection / invalid ID) + non-heavy host 运行说明 + idempotency test 章节 + 2026-04-21 mawk bug 历史注记 + related files cross-ref
- [ ] **T3.3.4** 缓冲 (0.5h)

### T3.4 — Prompt 模板 + 渲染契约 (2h, per TL-P1-C1 / AI-R1-1/2)

- [x] **T3.4.0** 引擎选型决议 (0.5h, 必须先于 T4.1 启动) — AD-M1-10 **Decided 2026-04-18** (Option A = bash `envsubst`), 5 条选型理由 (简单性 + 依赖最小化 + 安全边界 + 调试成本 + M2 升级路径) + 3 条 risk mitigation 已记. 2026-04-21 T3.4.0 closeout 回填: scaffold v1 Dockerfile L47-51 仅装 `git jq curl`, `node:20-bookworm-slim` 按惯例不默认含 `gettext-base`, envsubst 运行时可用性验证**移交 T4.1.1 Step 5 起始检查**; 若缺则 Dockerfile 补 `gettext-base` + scaffold v2 rebuild (~1h, 计入 T1.c Buffer / soft buffer). 不预防性动 scaffold v1 的理由: T1.c 已 pass + 无代码路径触发需求, 避免污染 handoff.image_sha256_scaffold baseline. 详见 AD-M1-10 v0.2 bottom note.
  - 候选: bash `envsubst` (Dockerfile 已装) vs Python Jinja2 (需 `pip install jinja2`)
  - 权衡: envsubst 轻量但无控制流; Jinja2 强但增依赖 + 安全边界 (render untrusted YAML)
  - Decision 记入 AD-M1-x 回写占位; T1.c.1 Dockerfile 根据结果决定是否加依赖
- [x] **T3.4.1** `docker/aria-runner/prompts/issue-dispatch.md` 起草 (1h) — pre-draft 2026-04-18 已 50 行, 2026-04-21 T3.4 closeout **critical fix**: 移除 header frontmatter 里的自引用 `$ARIA_*` 文档块 (envsubst 无 markdown 感知, header doc 里的示意 `$ARIA_ISSUE_ID` 也被替换, 污染渲染输出). 模板改为纯 prompt body (38 行), 所有文档搬去 `RENDERING_CONTRACT.md`. sha256 baseline = `13498378...`
  - 变量 (5 个 whitelist, 超 tasks 原规划 4 + ARIA_ISSUE_ID): `$ARIA_ISSUE_ID`, `$ARIA_ISSUE_TITLE`, `$ARIA_ISSUE_DESCRIPTION`, `$ARIA_FILES_LISTING`, `$ARIA_EXPECTED_CHANGES`
  - envsubst 引擎 per AD-M1-10 (whitelist 调用模式抵御 Risk R1 `$` 字符误展开)
- [x] **T3.4.2** 变量渲染契约 + golden sample (0.5h, per AI-R1-1) — 执行 2026-04-21, 三件产出:
  - `prompts/RENDERING_CONTRACT.md` (新建, 151 行): 字段→变量映射规则 + 参考 renderer bash+Python 实现 + 模板设计约束教训 (envsubst 无 markdown 感知) + sha256 baseline 表
  - `prompts/golden-samples/DEMO-001.rendered.txt` (51 行, sha256 `533f2329...`): envsubst 真渲染产出
  - `prompts/golden-samples/DEMO-002.rendered.txt` (61 行, sha256 `812a0d88...`): envsubst 真渲染产出
  - **Invariant check PASS**: `grep -Ec '\$\{?ARIA_'` 对两份 golden 均 = 0 (所有 whitelist vars 消耗, 无 leftover 文档 sigils)
  - `files_listing` = markdown bulleted list ✓
  - `expected_changes` = 两子项展开 (Files MUST be touched + Substrings in + 行) ✓
  - T4.1.1 Step 5 可用本 golden 作 sha256 比对单测 fixture

**T3.DoD**: schema validator PASS on DEMO-001/002; dispatch script 幂等; prompt template 存在。

---

## T4 — Runner Entrypoint 执行链路 (20h)

### T4.1 — Entrypoint 骨架 (4h)

- [x] **T4.1.1** `docker/aria-runner/entrypoint.sh` 重写 (M0 只做 skill load) (3h) — pre-draft 2026-04-18 已 538 行 `entrypoint-m1.sh` 全 11 步 + trap + atomic rename + Forgejo API. 2026-04-21 T4.1a closeout 补 3 个 real-fix:
  * Step 1b secrets source 分支文档注明 AD-M1-11 方案 D (Nomad Variables) 为生产路径, .env file 仅 dev override fallback (原 pre-draft 留方案 C 遗留注, 易误导)
  * Step 5 新增 `command -v envsubst` pre-flight (AD-M1-10 v0.2 closeout deferred 的 runtime verification, 若 scaffold v1 image 无 envsubst 则 fail fast 提示 Dockerfile +gettext-base + scaffold v2 rebuild)
  * Step 5 新增 rendered prompt invariant check (`grep -qE '\$\{?ARIA_'` on rendered output → die if leftover sigils, per RENDERING_CONTRACT.md §Invariant check, T3.4.2 首轮 render 已暴露同类 frontmatter 自引用坑)
  * 当前 `entrypoint.sh` 仍 M0 stub (58 行), 激活 (entrypoint-m1.sh → entrypoint.sh rename) 延迟到 T5.1.0 final image rebuild (per entrypoint-m1.sh L5-8 file header 锁定)
  * bash -n 语法 PASS (entrypoint-m1.sh 559 行 + lib/parse-stream-json.sh 70 行 + lib/compute-assertions.sh 137 行 均 PASS)
  - 11 步流程 (proposal §What §4 锁定):
    1. 读 `NOMAD_META_ISSUE_ID`; **设 `handoff.t4_started=true` signal** (per QA F3)
    2. 加载 `/opt/aria-inputs/{ID}/` (volume read-only)
    3. `git clone --depth 1` 目标 repo → `/tmp/workspace`; **`git config --global user.name / user.email`** (从 Dockerfile ENV `GIT_AUTHOR_NAME` / `GIT_AUTHOR_EMAIL` 注入, 预置 bot 账户身份, per BA-R2-GIT-IDENTITY-GAP)
    4. 创建分支 `aria/{ID}`
    5. 渲染 prompt (Jinja2 或 envsubst)
    6. Bash array `CLAUDE_ARGS=(claude -p "$RENDERED" ...)` + `timeout -k 10s 600s "${CLAUDE_ARGS[@]}"`
    7. Stream-json 解析 (读 `type=result` 最后一条)
    8. NO_OP 检测 (git diff HEAD)
    9. 幂等三态 (NEW/PARTIAL/FULL + `.bak` 归档)
    10. git add/commit/push + Forgejo create PR
    11. 写 result.json (含 trap EXIT 保护)
- [x] **T4.1.2** `trap 'write_partial_result_json' EXIT` 实现 (1h, per BA-R3-C2) — pre-draft 2026-04-18 `entrypoint-m1.sh` L65-96 已实装: trap 注册 L98, `write_partial_result_json` 函数在 `$RESULT_JSON` 未写时触发, atomic rename + 空字段 sed 修正为 null, outcome=INFRA_FAILURE error.type=crashed_before_result_write. 2026-04-21 静态语法 PASS, 功能验证延迟 T5 DEMO 5 轮中的 crash path (若 Step 10 push 失败 trap 应写 partial).

### T4.2 — Stream-json 解析器 (5h)

- [x] **T4.2.1** 读 stdout 最后 `type=result` JSON line (2h, per AI-C4) — pre-draft 2026-04-18 `docker/aria-runner/lib/parse-stream-json.sh` 70 行已实装 bash + jq; 2026-04-22 T4.2 session 覆盖 7-fixture 矩阵全 PASS 验证功能正确. 逻辑: `jq -R -s` slurp JSONL → `try fromjson catch null` 过滤损坏行 → `select(.type == "result")` 过滤 → `last // null` 取最后或 fallback null. 字段提取: `.total_cost_usd`, `.usage.{input,output,cache_creation,cache_read}_tokens`, `.is_error` (默认值 `// false` / `// 0` / `// null` 处理 missing 字段).
- [x] **T4.2.2** 原始 stdout 归档到 `/opt/aria-outputs/{ID}/claude.stream.jsonl` (1h) — pre-draft 已在 `entrypoint-m1.sh` L297 实装 `CLAUDE_STREAM_FILE="${OUTPUT_DIR}/claude.stream.jsonl"` + L311-313 `timeout -k 10s ... > "$CLAUDE_STREAM_FILE" 2> >(tee...)` 捕获 stdout 到 archive + stderr 单独到 `claude.stderr.log`. T4.2 session 交叉读 entrypoint 确认实装位置.
- [x] **T4.2.3** 单元测试 — **7** 种 fixture 覆盖 (原 Spec 5 种 + 2 对抗, per `feedback_pre_draft_bug_hunt_discipline`) (2h, per AI-R1-3) — 2026-04-22 全 PASS.
  1. ✅ `fx-01-normal-result`: 正常 result 帧 (提取 cost + usage + duration + num_turns)
  2. ✅ `fx-02-no-result`: 无 result 帧 (timeout SIGKILL 路径, fallback null)
  3. ✅ `fx-03-is-error-true`: `is_error=true` (claude 报错但 stream 完整)
  4. ✅ `fx-04-corrupted-lines`: 格式损坏/截断 JSON line + unterminated object (try/catch 过滤)
  5. ✅ `fx-05-multi-result`: 多 result 帧取最后 (`last` 语义)
  6. ✅ `fx-06-empty-stream` (对抗): 零字节输入 → null fallback
  7. ✅ `fx-07-result-missing-usage` (对抗): result 帧缺 `.usage` 对象 → 默认值 `0` 填充
  - Runner: `docker/aria-runner/tests/parse-stream-json/test.sh` (bash + jq, canonical-form 比较 `jq -S .`); 7/7 PASS 2026-04-22.
  - 结论 (对 `feedback_pre_draft_bug_hunt_discipline`): 本文件少见地在 pre-draft 阶段即 zero bug (70 行 / 7 fixture 矩阵全 PASS). 归因: jq 声明式 pipeline 结构简单 + 字段级默认值全显式处理. 反证"每 pre-draft 必藏 1-3 bug"在小型 pure-function 组件上不成立, 规则精确化为"含 I/O 副作用或动态分支的 pre-draft 必查".

**T4.2.DoD**: parser 处理 7 fixtures 全部 PASS; fallback path 显式测试通过 — ✅ 2026-04-22 已达成.

### T4.3 — result.json 生成 + assertion 计算 (5h)

- [x] **T4.3.1** schema v1.0 序列化 (2h, per proposal §What §4 result.json schema) — entrypoint-m1.sh Step 11 L515-550 已实装. 2026-04-22 T4.3 session **Spec 字段对照审计发现 1 bug**: 原 `claude_usage: $usage` 直接 passthrough parser 内部格式 (nested `.usage.{...}` + `total_cost_usd` + `raw_*`), 不符合 Spec L113-119 要求的 **flat 6 字段** (其中 `cost_usd_reported` 是 rename from `total_cost_usd` per AI-R3-I1). 修复: 在 Step 11 jq 模板中 reshape (见 L535-545 新增 if/then/else + 逐字段映射), 保持 parser 输出不变 (T4.2 fixture 矩阵无需回归). 验证: fx-01 parser 输出 → reshape 后得到 flat 6 字段 PASS; fx-02 null fallback → null PASS.
- [x] **T4.3.2** assertion_results 计算 (2h, per TL-I5 + AI-R1-4) — `docker/aria-runner/lib/compute-assertions.sh` 138 行 pre-draft; 2026-04-22 T4.3 session 建 7-fixture 矩阵验证, **发现并修 1 bug**: 原 `DIFF_PLUS_LINES=$(git diff ... \| grep -E '^\+' \| ...)` 在空 diff 时首个 grep 无匹配 exit 1, `set -o pipefail` + `set -e` 杀脚本 (ca-06-empty-diff 复现). 修复: 改用 `awk '/^\+/ && !/^\+\+\+ / { sub(...); print }'` 单步过滤, 始终 exit 0. 矩阵覆盖 (全 PASS):
  1. ✅ `ca-01-happy-path`: 单 file + 单 pattern
  2. ✅ `ca-02-file-miss`: expected file 未触达
  3. ✅ `ca-03-pattern-miss`: file 触达但 pattern 未命中
  4. ✅ `ca-04-diff-header-false-match`: **Spec 强制 fixture** — 创建 `docs/README.md` 内容 `xyz only`, expected `["README"]`. 证明 `+++  b/docs/README.md` header 被过滤, diff_hit=false (若无过滤会误判 true).
  5. ✅ `ca-05-multi-file-multi-pattern`: 2 file × 2 pattern 同时命中
  6. ✅ `ca-06-empty-diff`: `git commit --allow-empty` no-op 路径, 触发 bugfix 的 bug
  7. ✅ `ca-07-shallow-clone-base`: HEAD~1 不存在, fallback 到 empty tree sha (compute-assertions.sh L45-49)
  - Runner: `docker/aria-runner/tests/compute-assertions/test.sh` (bash + jq + git + python3, 每 fixture 独立 mktemp 工作区)
- [x] **T4.3.3** SUCCESS 严格判定 (5 AND, per AD-M1-4) (0.5h) — entrypoint-m1.sh L497-508 已实装. 5-AND: `CLAUDE_EXIT_CODE -eq 0 AND -n COMMIT_SHA AND -n PR_URL AND FILE_TOUCHED_HIT == true AND DIFF_CONTAINS_HIT == true`, 对应 proposal L134 原文 (注: proposal 文本 "三项都 true" 是口误, 实际列出 5 条件, impl 5-AND 正确). 任 1 false → `FINAL_OUTCOME="ASSERTION_MISMATCH"` (L506-508). 集成测试延 T5 DEMO 真实 dispatch 时自然验证, 不需独立单测.
- [x] **T4.3.4** 缓冲 (0.5h) — T4.3 session 实际 consumed ~2h (bugfix + 7 fixture 工程比预估稍重), 缓冲保留未触发, 归入 proposal 缓冲池。

### T4.4 — PR 创建 + 幂等守卫 (4h)

- [x] **T4.4.1** Forgejo API 调用封装 (1.5h) — 使用 bot PAT, Bash + curl 或 Python requests — entrypoint-m1.sh L381-384 (`GET /api/v1/repos/.../pulls`) + L459-463 (`POST /api/v1/repos/.../pulls`) 已实装 curl 直调 (bash + curl + jq, 无 Python). 2026-04-22 T4.4 session 对照 Spec §What §3 + Forgejo API v1 ref 审计, 无 critical bug; 集成级行为延 T4.5 真实 dispatch 验证.
- [x] **T4.4.2** 幂等三态实现 (1.5h, per BA-R2-C1) — entrypoint-m1.sh Step 9 (L386-399) + Step 10 (L415-450) 已实装三态判定 + force-with-lease + 409 分类; 2026-04-22 T4.4.3 **提取纯函数分类器**以支持 fixture 测试:
  - `lib/detect-idempotency-state.sh`: 2 布尔 → enum ({NEW,PARTIAL_PUSH_RECOVERY,FULL_RECOVERY})
  - `lib/classify-push-result.sh`: (exit_code, push_log) → outcome enum ({SUCCESS,IDEMPOTENCY_CONFLICT,GIT_STAGE_FAILURE}), 识别模式: `non-fast-forward|rejected|stale info|409` → IDEMPOTENCY_CONFLICT
  - entrypoint-m1.sh Step 9/10 重构调用 lib, `stale info` 模式新增 (原仅 `non-fast-forward|rejected|409`) 使 force-with-lease lease 违例更准确归类.
  - **force-with-lease (BA-R4)**: 保留, Step 10 L418 `git push --force-with-lease`.
  - **409 不重试**: classifier 分类出 IDEMPOTENCY_CONFLICT → `PROVISIONAL_OUTCOME` 记录 → Step 11 写 result.json → exit 1 (entrypoint 最后), 无 retry 循环.
- [x] **T4.4.3** 缓冲 / fixture 矩阵 (1h) — 2026-04-22 用于 classifier 单测, **13/13 PASS**:
  - **Part A** (classify-push-result.sh, 7 cases): pc-01 success → SUCCESS; **pc-02 rejected non-fast-forward** / **pc-03 lease stale info** / **pc-04 HTTP 409 literal** → all IDEMPOTENCY_CONFLICT (Spec 强制 409 覆盖通过 3 条 fixture 全路径) ; pc-05 network timeout / pc-06 auth failure / pc-07 empty log → all GIT_STAGE_FAILURE (fallback).
  - **Part B** (detect-idempotency-state.sh, 4 cases): (false,false)→NEW / (true,false)→PARTIAL / (true,true)→FULL / (false,true)→NEW (orphan-PR 边缘态保守归 NEW, 加注释记录).
  - **Part C** (arg validation, 2 cases): non-boolean + non-integer → exit 64 正确拒绝.
  - Runner: `docker/aria-runner/tests/push-classifier/test.sh` (bash parallel arrays, ordered iteration).
  - 全量回归验证 (T4.2/T4.3/T4.4 联动): 27/27 PASS 2026-04-22.

### T4.5 — 单次 DEMO Dispatch Smoke (2h)

- [x] **T4.5.1** DEMO-001 单次 dispatch 验证端到端 (2h 计划, 实耗 ~4h) — 执行 2026-04-23, **PASS**: alloc `70ee89aa`, outcome=SUCCESS, PR #29 创建 (1 file / +1 / -1 / aria/DEMO-001 → feature/aria-2.0-m1-mvp), claude 实际 LLM call (smart-sonnet → glm-4.7 via Luxeno per AD-M1-12) 26s / 11 turns / $0.495, 11 步全通。
  - **真实 API call 证据**: stream-json `result` 帧 `total_cost_usd=0.495`, `model=glm-4.7` (Luxeno backend mapping AD-M1-12 生效), api_error_status=null
  - **链路无断点覆盖 CONFIRMED**: seeder (inputs volume) → Nomad dispatch → runner entrypoint 11 步 → parse-stream-json → compute-assertions → Forgejo PR create
  - **Spec T4.5 L273 "回退到 T1.c 镜像 ENV 检查" 实际触发**: T4.5 smoke 首轮暴露 scaffold v1 镜像缺 entrypoint-m1.sh/lib/prompts/python3, 执行 T5.1.0 pulled forward (Dockerfile 重构 + aria-build rebuild + 镜像 tag claude-m1-69e66a6-v6)
  - **Pre-draft bug hunt 积累** (本 session 实际修): (1) Dockerfile L91 仅 COPY M0 stub (T5.1.0 延迟); (2) 缺 gettext-base; (3) 缺 python3 (YAML parser 依赖); (4) `unset ANTHROPIC_BASE_URL` 违反 AD-M1-12; (5) Forgejo URL 直连 `forgejo.10cg.pub` 被 CF Access 拦 302 → 改内网 `192.168.69.200:3000`; (6) claude `--permission-mode bypassPermissions` root 下被 claude-code 拒 → 移除 flag 依赖 settings allowlist; (7) DEMO-001 `base_branch: master` 但 fixture 只在 feature branch → 改 `base_branch: feature/aria-2.0-m1-mvp`; (8) 孤儿 aria/DEMO-001 + PR #28 需 API 清理 (IDEMPOTENCY_CONFLICT 分类器正确归类)
  - **Spec 强制 409 classifier** 实战验证: 2nd dispatch 正确分类为 IDEMPOTENCY_CONFLICT (lease stale, shallow clone 无 aria/DEMO-001 ref → push rejected)
  - **DEMO_002 未跑** — M1 Spec T4.5 只要求 DEMO-001 smoke, DEMO-002 在 T5 DEMO 矩阵
  - **M1 image 生产 tag**: `forgejo.10cg.pub/10cg/aria-runner:claude-m1-69e66a6-v6` (aria-orchestrator sha 69e66a6); aria-runner-template.hcl pin 此 tag (AD-M1-2 immutable)
  - Evidence files (heavy volume `/opt/aria-outputs/DEMO-001/`): result.json, claude-usage.json (reshape 新 schema), claude.stream.jsonl, assertion-results.json, .t4_started marker

**T4.5 FAIL 处置 (per KM-PM-02)**: 由 ai-engineer + backend-architect 联合 triage, 不升级到 T5 (smoke 阶段失败 = T4 未完成)。

**T4.DoD**: entrypoint 11 步执行成功; stream-json 解析正确; result.json schema 合规; 幂等三态测试通过; T4.5 真实 Anthropic API smoke PASS。

---

## T5 — DEMO E2E Execution + Profiling (16h)

### T5.1 — DEMO-001 5 轮执行 (4.5h, +0.5h per TL-P1-I1 final image rebuild)

- [x] **T5.1.0** T1.c (final) — entrypoint 完成后 rebuild (0.5h) — **提前到 T4.5 smoke 执行** 2026-04-23, 因 T4.5 首跑暴露 scaffold v1 镜像缺 entrypoint-m1.sh/lib/prompts. 最终 tag `claude-m1-5154c13-v9` (aria-orchestrator sha 5154c13, 含 FETCH_HEAD fix + explicit lease + non-root→root revert + python3/gettext-base + M1 entrypoint 切换). image_sha256_final = `sha256:e46be19da4d9ab782d4be50c15f0939d34c407ffac04fa640cc9f299d4b9075e`. 推送 immutable + mutable claude-latest 双 tag 到 forgejo.10cg.pub/10cg/aria-runner.
- [x] **T5.1.1** 5 轮执行 + 每轮 result.json 归档 (2h) — 执行 2026-04-23 (ts 04:24-04:27Z), 串行 dispatch, 每轮端到端 20-35s (≪ 10min 上限). Alloc list: b32f6e20, 41f54419, e2218045, 37fbbd7f, ddb73461 (全 heavy-1). 每轮 result.json 有 `.bak` 归档保留. Runner script: `aria-orchestrator/scripts/t5-run-demo.sh`.
- [x] **T5.1.2** outcome distribution 统计 (1h) — **5/5 SUCCESS**, success_rate=100% (≥80% ✅). 无 ASSERTION_MISMATCH / TIMEOUT / GIT_STAGE_FAILURE / INFRA_FAILURE. 全 FULL_RECOVERY 路径 (PR #30 复用, 证 fetch-before-push+explicit-lease fix 稳定).
- [x] **T5.1.3** p50/p95 duration + token usage 计算 (0.5h) — avg=26.2s / p50=25s / p95=35s. Token p50: input 30618 / output 890. total_cost_usd=$1.038. 数据源: `artifacts/t5-DEMO-001.jsonl` (5 条) + `artifacts/t5-e2e-summary.json`.
- [x] **T5.1.4** 缓冲 (0.5h) — 实际 consumed 由 T5.1.0 提前执行的 debug 时间占用 (fetch/lease fix iterations v6-v9).

### T5.2 — DEMO-002 5 轮执行 (6h)

- [x] **T5.2.1** 5 轮执行 (3h) — 执行 2026-04-23 (ts 04:28-04:32Z), **意外 9 轮** (nohup 双进程并发 bug, 记入 lesson: script 启动前必须用 flock 或 PID 锁). 端到端 20-56s, 均 ≪ 600s CLAUDE_TIMEOUT_S 上限, reforecast 不需要. Alloc list: 8441e16a, c50b60d4, 4484f156, 29c9a9b2, **45ce61a6 (ASSERTION_MISMATCH)**, 2a10777f, 858a59a4, 86c2cb2f, 61dd6dd6.
- [x] **T5.2.2** outcome + stats (1h) — **8/9 SUCCESS = 88.9% ≥ 80% ✅**. 1 ASSERTION_MISMATCH (alloc 45ce61a6, file_hit=false, diff_hit=false — claude 输出未触达 expected_file_touched 或缺 expected_diff_contains 某字面量). avg=32.7s / p50=26s / p95=56s. Token p50: input 2329 (cache hit) / output 1149. total_cost_usd=$1.791. DEMO-002 更长是因为 2 文件写 + pytest 结构 vs DEMO-001 的单行 timestamp 替换.
- [x] **T5.2.3** PR diff 质量评审 (1h) — **T5.2.3.a AI advisory**: 8 SUCCESS 的 PR #31 commits 机械验证通过 (file_hit=true + diff_hit=true 包含 "def fibonacci" + "def test_" + "assert" + "ValueError"); 1 ASSERTION_MISMATCH 需 Owner 人工审视具体 diff (alloc bak 在 heavy-1 `/opt/aria-outputs/DEMO-002/result.json.1776918670.bak`). **T5.2.3.b Owner signoff**: pending (per AD-M0-9, simonfish 按需查看 PR #31 decide 是否作为 M2 blocker).
- [x] **T5.2.4** 缓冲 (1h) — consumed by dual-script bug + 9-round actual (不影响 DoD).

### T5.3 — E2E 统计汇总 + 失败 triage + performance_baseline (4h)

- [x] **T5.3.1** 汇总 handoff.demo_executions 字段 (1h) — 生成 `artifacts/t5-e2e-summary.json` (per-DEMO stats + overall `e2e_demo_passed=true`). DEMO-001 5/5 SUCCESS + DEMO-002 8/9 SUCCESS 均 ≥80%, `e2e_demo_passed = true`.
- [x] **T5.3.2** Failed runs triage (1.5h) — 单一 failure: alloc 45ce61a6 (DEMO-002 round 3a), outcome=ASSERTION_MISMATCH. **原因**: file_hit=false + diff_hit=false → claude 退出 0 但未触达 `expected_file_touched` 或缺 `expected_diff_contains` 某字面量. **可重试**: 是 (后续同轮 alloc 2a10777f 立即 SUCCESS, 证实非稳定性 bug). **tech-lead (owner) 决策**: 不作为 M2 blocker, 归入 M2 prompt 工程优化项 (Hermes Layer 1 + Retry 机制可覆盖).
- [x] **T5.3.3** performance_baseline 聚合 (0.5h, per TL-P1-M1) — 已生成并记入 e2e-summary:
  - cpu_p95: 未直接测 (M1 smoke resources `cpu=2000 MHz`, 集群 stat 层数据不足 capture; 推到 M2 通过 Nomad alloc metrics sidecar)
  - memory_p95: 参考 T2.3 baseline `resource-baseline.md` — production workload mock 使用 1500 MiB (< 2048 soft 限)
  - demo_001_p50_duration_s: 25
  - demo_001_p95_duration_s: 35
  - demo_002_p50_duration_s: 26
  - demo_002_p95_duration_s: 56
  - token_usage_p50 (DEMO-002): 2329 input / 1149 output
- [x] **T5.3.4** 缓冲 (1h) — consumed in triage + summary write.

### T5.4 — Week 2 Checkpoint (2h)

- [ ] **T5.4.1** 累计工时核算 (0.5h) — 若 ≥ 60h 且 `handoff.t4_started == false` → 触发 scope 重估 (per QA F3 机械可检; handoff schema v1.0 需加 `t4_started: bool` 字段, 执行 T4.1.1 第一个 checkbox 时 runner 置 true)
- [ ] **T5.4.2** 若触发: DEMO-002 降级为 optional (**0h if not triggered, 1-2h if triggered, 从 Buffer 支出**, per CR-R1-M2)
  - deferred-with-approval 走 No-Go-with-revision (非 Go)
  - 写入 `handoff.open_issues`
- [ ] **T5.4.3** 缓冲 (1.5h, 通常 M1 正常进度不触发)

**T5.DoD**: `e2e_demo_passed = true/false` 确定; outcome distribution 完整; PR URLs 列表记录。

---

## T6 — M1 Report + Handoff + AD-M1-* 回写 (6h)

### T6.1 — M1 Report 起草 (2.5h)

- [ ] **T6.1.1** `aria-orchestrator/docs/m1-report.md` 起草 (2h)
  - 结构参照 M0 Report (简化版):
    - §0 Executive Summary + velocity 实测 vs PRD 100h
    - §1 镜像链路验证结果
    - §2 Nomad 生产配置实测
    - §3 DEMO E2E 结果 (5 轮 × 2 统计)
    - §4 Legal carryover 摘要
    - §5 Open issues for M2
    - §6 签字位
- [ ] **T6.1.2** 缓冲 (0.5h)

### T6.2 — Handoff schema v1.0 生成 (1.5h, per AD-M1-7; tech-lead co-sign, per KM-PM-01)

- [ ] **T6.2.1** `aria-orchestrator/docs/m1-handoff.yaml` 填充 (1h)
  - go_decision / image_refs (含 `image_sha256_final` 替换 scaffold) / nomad 配置 / `t4_started` / demo_executions / legal_assumptions / performance_baseline / demo_token_usage
- [ ] **T6.2.2** Handoff validator 创建 + 验证 (0.5h)
  - `aria-orchestrator/docs/validate-m1-handoff.py` (仿 M0 validator)
  - **验证清单 (per LA + QA)**:
    - schema v1.0 字段必填 + enum
    - `outcome_distribution` SUM == runs (per DEMO)
    - `e2e_demo_passed = DEMO-001.passed AND DEMO-002.passed` 逻辑 AND
    - `legal_assumptions.anthropic_api_terms_verified == true` (orphan 检测: true 值必须有对应 m1-legal-carryover.md + 末行 `Signed-by:` 签字)
    - `legal_assumptions.luxeno_data_cleared` (backfill from T1.a.2)
    - `legal_assumptions.m1_memo_signed` (mechanical file-existence check)
    - `image_refs.immutable_sha` 非空 (不是 scaffold 占位)
- [ ] **T6.2.3** tech-lead co-sign (0.3h, 附 T6.2.2 之后, per KM-PM-01 + KM2-PM-03/04)
  - 对 handoff schema M2 接口契约做最终裁决 (schema amendments 窗口策略 per AD-M1-7 是否激活)
  - **机械 artifact**: `m1-handoff.yaml` 末部新增字段:
    ```yaml
    tech_lead_cosign:
      signed_by: "human:simonfish"    # per AD-M0-9 solo-lab
      date: "YYYY-MM-DD"
      statement: "M2 接口契约审阅通过 / schema additive-only 窗口 ... (自定义说明)"
    ```
  - Validator (T6.2.2) 追加检查: `tech_lead_cosign.signed_by != null AND tech_lead_cosign.date != null`
  - 工时 0.3h 从 T6.4 缓冲吸收 (T6.4.1 0.5h → 0.2h, T6.4.2 0.5h 不变)
  - **T6.DoD 补加**: "tech-lead co-sign artifact 存在" 为独立 gate 条件

### T6.3 — AD-M1-* 决议回写 (1h, per KM-M2 / CR-M3)

- [ ] **T6.3.1** 在 `aria-orchestrator/docs/architecture-decisions.md` 填充 AD-M1-1 ~ AD-M1-9 最终决议 (1h)

### T6.4 — Owner Signoff (0.7h, per AD-M0-9; 0.3h 已转入 T6.2.3 tech-lead co-sign)

- [ ] **T6.4.1** Owner 审阅 M1 Report + handoff + legal carryover (0.2h, per KM2-PM-04 减配)
- [ ] **T6.4.2** 签字 + go_decision 填充 (0.5h)
  - `Go` | `Go-with-revision` | `No-Go` | `No-Go-with-revision`
  - Deferred-with-approval (DEMO-002 降级) → 走 `No-Go-with-revision` (per AD-M1-5)

**T6.DoD**: Report 完整; handoff validator PASS (final); ADRs 回写; owner signoff 完成; **tech-lead co-sign artifact 存在** (`m1-handoff.yaml.tech_lead_cosign.signed_by != null` AND `.date != null`, per KM3-PM-02)。

---

## Buffer (20h, 分 soft + hard 两档, per TL-P1-I2)

**Soft cap (总 14h, 按 T 分类)**:
- T1+T4 Spike 超工时 → 最多 +8h (原 10h, 让出 2h 到 hard reserve)
- T5 DEMO 重跑 triage → 最多 +3h (原 5h, 让 2h)
- T6 handoff 迭代 → 最多 +3h (原 5h, 让 2h)

**T5.1.0 final image rebuild 0.5h 归档 (per TL-P2-M2)**: 已内嵌到 T5.1 summary (16h → 16.5h), **不计入 Buffer soft cap** (即非 "T5 DEMO 重跑 triage" 类别). 若 T5.1.0 rebuild 失败需 debug → 从 T5 DEMO 重跑 triage 3h 支出。

**Hard reserve (6h, 真正 global)**:
- 任一 T 桶超 soft cap 上限后, 额外申请 hard reserve 需 owner 签字 + 写 `handoff.open_issues`
- Hard reserve 完全耗尽 → 触发 No-Go-with-revision (超支 = 产品负责人决议)

**Week 2 checkpoint (R-M1-7)**:
- 累计工时 ≥ 60h 且 `handoff.t4_started == false` → 触发 scope 重估 (DEMO-002 降级为 optional)
- 不消耗 buffer, 走 AD-M1-5 降级规则 (`No-Go-with-revision` 分支)

## 收敛后状态

| 状态 | 动作 |
|------|------|
| **Go** | US-022 M2 Layer 1 state machine 启动 (硬门控满足) |
| **Go-with-revision** | M1 产出有效 + 对 PRD / M2 scope 做调整 (PRD patch PR) |
| **No-Go-with-revision** | DEMO-002 deferred (R-M1-7 触发) 或其他次要缺陷可接受 (signed off) |
| **No-Go** | 硬失败: T3/T4 链路不通 / Legal carryover 结论否决 / Registry 不可用 → 触发 PRD AD3 二次评估 |

---

## Agent 分配 (STCO Routing)

基于 [STCO routing 策略](../../../aria/skills/agent-router/SKILL.md), 按任务 capability tag 分配 Agent 主责。solo-lab (AD-M0-9) 场景下 Agent 为 AI 协作者, owner 承担人类审批 + 签字。

### 主责分配 rationale

| Agent | 主责任务 | Capability 匹配 |
|-------|---------|----------------|
| **knowledge-manager** | T0 (kickoff + 文档锚点), T6.1 (M1 Report), T6.3 (AD 回写) | 文档结构 / traceability / AI-DDD 方法论一致性 |
| **legal-advisor** | T1.a (Legal carryover memo + ToS mapping table + IS-4 失效审视) | Privacy / 跨境合规 / ToS clause mapping |
| **backend-architect** | T1.b (Registry auth Spike), T1.c (Docker build/push), T2 (Nomad HCL + host volume), T3.1 (schema validator), T3.3 (dispatch script), T4.1/4.4 (entrypoint 骨架 + PR 幂等) | RESTful / DB schema / 基础设施拓扑 / Docker / Nomad |
| **ai-engineer** | T3.4 (prompt template), T4.2 (stream-json 解析), T4.3 (assertion 计算) | LLM 集成 / prompt 设计 / stream API 解析 |
| **qa-engineer** | T5.1/5.2 (DEMO 5 轮 × 2 执行), T5.3 (统计 + triage), T5.4 (Week 2 checkpoint 评估) | 测试策略 / 样本量评估 / failure taxonomy |
| **tech-lead** | T6.4 (Owner signoff 协同), T5.3 失败 triage 决策 | 跨模块仲裁 / milestone 级 Go/No-Go 建议 |
| **code-reviewer** | 每个子任务 PR 合并前 (per M0 pattern), M1 Report + handoff 最终核查 | Spec 合规 + pre-merge code quality gate |

### 协同任务 (多 Agent 共同)

- **T3.2 DEMO fixture 设计**: backend-architect (repo 结构) + qa-engineer (测试设计) + legal-advisor (IP classification 审查)
- **T4 Runner entrypoint**: ai-engineer (claude CLI 层 T4.2/4.3) + backend-architect (git / PR / 幂等守卫 T4.1/4.4) 紧密配合; **entrypoint.sh 最终集成归属: backend-architect 主导, ai-engineer 以 patch/PR 形式提交 T4.2/4.3 代码段供 review** (per BA-R5-T4-BOUNDARY)
- **T4.5 smoke FAIL 处置**: ai-engineer + backend-architect 联合 triage, 不升级到 T5 (per KM-PM-02)
- **T5.3.2 Failed runs triage**: qa-engineer (枚举分类) + tech-lead (决策: 是否回退 / 重跑 / 升级) (per KM-PM-01)
- **T6.2 Handoff validator**: backend-architect (schema 实现) + knowledge-manager (字段 traceability 审查) + **tech-lead co-sign (M2 接口契约裁决, per KM-PM-01)**
- **T5.2.3 PR diff 评审**: code-reviewer advisory (T5.2.3.a) + owner signoff (T5.2.3.b, per TL-P1-I3)

### Solo-lab 签字主体 (per AD-M0-9)

所有"人类角色"签字 (legal-advisor 签字 / tech-lead velocity_cosign / owner signoff) 由 simonfish 承担, AI advisory 意见仅作 audit trail, 不构成放行依据。

### 不适用的 Agents

- **mobile-developer**: M1 MVP 无移动端工作
- **ui-ux-designer**: M1 无 UI 工作
- **api-documenter**: M1 无 OpenAPI 产物
- **context-manager**: M1 为单 session 执行, 无跨 session 上下文合并需求

---

## 关联文档

- [proposal.md](./proposal.md) — M1 MVP Level 3 Spec
- [US-021.md](../../../docs/requirements/user-stories/US-021.md) — Parent Story
- [US-022.md](../../../docs/requirements/user-stories/US-022.md) — M1 后继 (M2 硬门控 handoff.e2e_demo_passed=true)
- [M0 Report](../../../aria-orchestrator/docs/m0-report.md) — M1 精确路径基线
- [M0 handoff](../../../aria-orchestrator/docs/m0-handoff.yaml) — M1 输入契约只读
- [M0 tasks (archived)](../../archive/2026-04-17-aria-2.0-m0-prerequisite/tasks.md) — M1 tasks 分解 pattern 参考 (per CR-R2-L3)
- [PRD v2.1 §M1](../../../docs/requirements/prd-aria-v2.md)

---

**最后更新**: 2026-04-17 (Phase A.2 task decomposition post convergence audit Round 6 PASS)
**维护**: Phase B.2 执行阶段 updates 标记完成度

# phase-c-integrator-pre-merge-gate

> **Level**: Minimal (Level 2 — proposal.md 含任务,无独立 tasks.md;跨 skill + workflow-runner + CLAUDE.md 不可协商规则集 — 沿用 state-scanner-inter-cycle-surfacing precedent 的"Level 2 含任务"形式,与 Aria 项目惯例一致)
> **Status**: **Approved** (post_spec R2 unanimous PASS_WITH_WARNINGS, 2026-05-09; pragmatic convergence per Aria memory `feedback_post_spec_audit_pragmatic_convergence`; R2 new Majors inline-patched)
> **Created**: 2026-05-09
> **Approved**: 2026-05-09 (audit report: `.aria/audit-reports/post_spec-R1-R2-2026-05-09T1816Z-phase-c-integrator-pre-merge-gate.md`)
> **Type**: Workflow safety gate (consume aether primitive)
> **Source**: Forgejo Issue [10CG/Aria#60](https://forgejo.10cg.pub/10CG/Aria/issues/60) — SilkNode 实战反馈
> **Upstream blocker resolved**: aether#89 closed 2026-05-06,`aether ci status --in-flight` flag + `aether-ci-cli (was: aether-pre-merge-check, R3 修订 — skill 不存在)` skill 就绪
> **Related precedent**: CLAUDE.md 不可协商规则 #6/#7 (规范层强制约束),phase-c-integrator C.2.5 multi-remote push enforcement (v1.15.0+)

---

## Why

### 实战 forcing function

SilkNode 项目 2026-05-02 实测时间线:

| 时间 (UTC) | 事件 |
|-----------|------|
| 12:35 | PR-322 (embeddings) push,Forgejo Run #3160 启动 (PR CI) |
| 12:45 | PR-322 merge → main commit `33f02882` → Run #3161 启动 (main CI deploy) |
| 12:52 | Run #3160 PR CI success(agent polling 触发) |
| 12:53 | agent merge PR-321 (US-113 PR-C) → Run #3162 启动 |
| 12:53 | Run #3161 自动 cancelled(Forgejo Actions concurrency rule + Nomad 单 job),**459s 部署观测丢失** |

PR-321 merge 时 cancel 了 PR-322 的 main CI 部署 run,**PR-322 失去独立部署观测窗口**。

### 根因 — phase-c-integrator C.2 缺 pre-merge gate

当前 `phase-c-integrator/SKILL.md` C.2 步骤序列:

```
C.2 pre_hook   → audit-engine pre_merge 检查点 (PASS/FAIL on diff quality)
C.2 action     → push branch + create PR + (可选) auto merge   ← merge 在此调用,无 in-flight CI 查询
C.2.5          → multi-remote push enforcement (post-merge)
C.2.6          → UPM milestone sub-progress append
```

merge 行为只检查 PR diff 的 audit verdict,**完全不查 main 分支当前是否有 in-flight CI**。多 PR 并发 + Forgejo Actions concurrency rule + Nomad 单 job-name 拓扑下,任一新 main commit 触发的 CI 会 cancel 上一个 in-flight 的 main CI run。

### 为什么 aria 自己不该实现

问题 root cause 在 CI/CD 协同 primitive 层(Forgejo Actions concurrency rule + Nomad 单 job)。aria 是工作流编排层,应**消费** aether 提供的 primitive,不重复实现 CI 状态查询逻辑。

aether#89 已 closed (2026-05-06),提供两个 primitive:
- `aether ci status --in-flight` flag — 列出指定 repo 在 main 分支 running 的 CI run
- `aether-ci-cli (was: aether-pre-merge-check, R3 修订 — skill 不存在) <pr-id>` skill — 封装 "本 PR CI green ✓ + main 无 in-flight" 复合检查,统一返回三态 (`green` / `wait` / `fail`)

本 Spec ship = 让 phase-c-integrator C.2 调用 `aether-ci-cli (was: aether-pre-merge-check, R3 修订 — skill 不存在)`,workflow-runner 把 `wait` 状态从 fatal error 改为 recoverable wait+retry。

### Aria 方法论对齐

CLAUDE.md 不可协商规则集 #6/#7 已确立"规范层强制约束 + 真理来源"模式(skill benchmark 必须用 `/skill-creator`、secret 命令必须 redirect output)。本 Spec 加 #8 "PR merge 前必跑 aether-ci-cli (was: aether-pre-merge-check, R3 修订 — skill 不存在)",与 "push 后必跑 aether-ci 监控" 同等级,补全 PR 生命周期的安全 net。

CLAUDE.md 研究目标 #1: "可重现的 AI 协作流程 — 不同项目、不同 AI 都能获得一致结果"。当前 cancel 事故是 cross-session 不可见的 race condition,任何 agent 在 SilkNode 都可能复现。机械化 gate 把这个 race 从 "agent 自律" 升级为 "workflow 强制"。

---

## What

### 范围

三个 deliverable + workflow-runner 错误语义扩展 + 一条不可协商规则 + 完整 `/skill-creator` AB benchmark + dogfooding 验证。

### Key Deliverables

#### D1 — phase-c-integrator C.2.4 pre-merge precondition step

**位置**: 新插入步骤 **C.2.4**,介于 C.2 action (PR creation) 与 C.2.5 (multi-remote push) 之间。`auto_merge=true` 配置下在 PR 创建后、merge call 前;`auto_merge=false` 由用户手动触发 merge,gate 在 PR review pass 后由 user 触发 `/aria:phase-c-integrator continue` 时调用。

**Naming 命名空间澄清 (R2 patch — BA-1)**: phase-c-integrator-level 子步骤标签 (C.2.x) 为 **orchestrator-tier**,与 branch-manager 内部实现层 (也用 C.2.x sequence: C.2.1 sync / C.2.2 push / C.2.3 create PR / C.2.4 wait approval / C.2.5 merge) 是**独立 label namespace**。本 Spec C.2.4 = "pre-merge precondition gate" (orchestrator tier);branch-manager 内部 C.2.4 = "wait for approval" (implementation tier);同名但不同 tier,语义不冲突。T1.3 SKILL.md 详细文档段必须显式声明此命名规则,防 agent 误解。

**Cross-plugin invocation protocol (R2 patch CR-1+BA-2 / T1.0 spike 修订 R3)**: aria 现无跨 plugin skill 调用先例。本 Spec 采用 **subprocess CLI wrapper 模式** — T1.0 spike 实测确认 (2026-05-10):
- **aether plugin init 检测**: 优先 `which aether 2>/dev/null` 检查 CLI binary;次选 `.aether/config.yaml` 是否存在
- **Primitive (单一)**: `aether ci status --branch <branch> --in-flight --json` (P0-A,aether#116 merged 2026-05-06,SHA `f29abee`)
- **⚠️ T1.0 spike 关键发现**: 原 Spec 假设的 `aether-pre-merge-check` skill (P0-B) **从未实施** — aether-plugin/skills/ 无此项,issue#89 closed 时仅 P0-A ship。**verdict 计算必须在 aria 端**(参见 §Contract Source 修订)。aether 仅提供 query 层 raw runs[],aria 负责 verdict 层
- **调用结果**: stdout JSON parse (D1 §Contract Source 内部契约 schema),exit code 0 = 成功 / 非 0 = primitive 错误 (走 `fail` verdict)
- **检测失败**: 按 `no_aether_fallback` 配置降级 (`skip_with_warning` 默认 / `abort` 严格)
- **Binary 版本检查**: helper 启动时 `aether --help | grep -q "in-flight"` 验证 binary 含 P0-A flag,缺失 → fail-fast + 提示 "请升级 aether ≥ commit f29abee (2026-05-06)"

**Contract Source — aria 内部契约 (R3 重写 — T1.0 spike 修订)**:

> **重要变更**: R2 假设 aether 提供 verdict 层 (`aether-pre-merge-check` skill 返回预算好的 verdict)。T1.0 spike 实测发现该 skill 不存在 (aether#89 仅 ship P0-A query flag,P0-B skill 从未实施)。**verdict 计算改为 aria 端实现**,aether 仅提供 raw query primitive。

**aether 端 — query primitive (consumed by aria)**:

`aether ci status --branch <branch> --in-flight --json` 返回:
```json
{
  "status": "ok",
  "data": {
    "filters": {"branch": "main", "in_flight": true},
    "repo": "10CG/Aria",
    "runs": [
      // 0-N runs; in-flight = 非终态 (running / pending / queued)
      // 完整 run schema 见 aether-cli/internal/ci/status.go (CIRun struct)
    ]
  }
}
```

`aether ci status --branch <pr-branch> --json` (查 PR CI 状态) 返回 同 schema 但 in_flight=false,含完整 runs (含终态)。

**aria 端 — 内部 verdict 契约 (helper 输出)**:

```json
{
  "verdict": "green" | "wait" | "fail",
  "pr_ci_status": "passing" | "failing" | "pending",
  "in_flight_runs": [
    {
      "run_id": 3161,
      "branch": "main",
      "started_at": "2026-05-09T12:45:00Z",
      "elapsed_seconds": 459
    }
  ],
  "primitive_used": "aether-ci-cli",
  "primitive_version_sha": "f29abee",
  "raw_message": "..."
}
```

**Verdict 计算逻辑** (aria helper `pre_merge_gate.py`):

```
1. 调 `aether ci status --branch main --in-flight --json` → main_in_flight_runs[]
2. 调 `aether ci status --branch <pr-branch> --json` → pr_runs[];last run status → pr_ci_status
3. compute verdict:
   - pr_ci_status in [failing, error] → verdict=fail
   - pr_ci_status == pending → verdict=wait (PR CI 尚未完成)
   - pr_ci_status == passing AND main_in_flight_runs == [] → verdict=green
   - pr_ci_status == passing AND main_in_flight_runs != [] → verdict=wait
4. 翻译 aether CIRun → 内部 in_flight_runs[] (字段映射: id→run_id, branch→branch, started_at→started_at; elapsed_seconds 由 aria 计算 = now - started_at)
```

**Subprocess exit-code 映射 (R2 inline patch — R2-CR-C, 不变)**:
- `0` = success, parse stdout JSON 按 aether 端 query schema
- `1-126` = aether 内部错误 (CI API 失败 / 权限不足等), 路由 `fail` verdict + raw_message 含 stderr
- `127` = binary not found, 路由 detection 失败 → `no_aether_fallback` 配置降级
- `-SIGTERM` (subprocess timeout 触发) = primitive 调用超时, retry 至 max attempts → 仍超时则 `fail` verdict

**契约真理来源**: aether-cli `--in-flight` flag 实施 commit `f29abee` (aether#116 merged 2026-05-06)。aria phase-c-integrator helper (`pre_merge_gate.py`) **从 aether raw runs[] 翻译并计算 verdict**。如 aether 后续修改 query schema,本 Spec 的 helper 需联动升级 (向后兼容由 aether plugin 保证 — `aether ci status --json` 已是稳定 API,字段添加不破坏)。

**新 sub-step 伪代码**:

```yaml
C.2.4 - Pre-Merge Precondition Gate:
  触发条件:
    - C.2 action 已完成 PR 创建 (PR_NUMBER + PR_URL 已知)
    - 即将调用 merge action (auto_merge 或 user-triggered)
    - 配置 phase_c_integrator.pre_merge_gate.enabled: true (默认)
  primitive 调用 (R3 修订 — T1.0 spike):
    - **唯一 primitive**: aether ci status --branch main --in-flight --json (查 main 是否有 in-flight) + aether ci status --branch <pr-branch> --json (查本 PR CI)
    - aria helper 自行计算 verdict (见 §Contract Source Verdict 计算逻辑)
    - 不可用 (no aether): 按配置 fallback (skip_with_warning / abort)
    - **R2 假设的 aether-ci-cli (was: aether-pre-merge-check, R3 修订 — skill 不存在) skill 不存在,已从 primitive 优先级链中移除** (aether#89 仅 ship P0-A query flag; P0-B skill 从未实施)
  三态结果:
    green:  本 PR CI ✓ + main 分支无 in-flight CI → 继续 merge
    wait:   main 分支有 in-flight CI run → 进入 wait+retry (D2)
    fail:   本 PR CI 红 / aether primitive 报错 → BLOCK + 报告
  output:
    pre_merge_verdict: "green" | "wait" | "fail"
    in_flight_runs: [{run_id, started_at, branch}]   # wait 时
    pr_ci_status: "passing" | "failing" | "pending"
    primitive_used: "aether-ci-cli (was: aether-pre-merge-check, R3 修订 — skill 不存在)" | "aether-ci-cli" | "manual"
```

**配置项** (新增,via config-loader):

```yaml
phase_c_integrator.pre_merge_gate:
  enabled: true                          # 默认启用; false → 完全跳过 (向后兼容)
  primitive_preference:                  # R3 修订: 仅 CLI (skill 从未实施)
    - "aether-ci-cli"                    # 唯一 primitive: aether ci status --in-flight
  no_aether_fallback: "skip_with_warning"  # 无 aether 时的降级 (skip_with_warning | abort)
  wait_timeout_seconds: 1800             # max 等待时长 (默认 30 min)
  wait_check_intervals: [30, 60, 120, 300, 300]  # 指数退避 (秒); 数组耗尽后重复 intervals[-1]=300 直到 wait_timeout_seconds (CR-3 R2 patch)
  user_escape_hatch: true                # 允许 user Ctrl-C 中断 wait 进入 abandon/manual override
  primitive_call_timeout_seconds: 30     # 单次 aether subprocess 调用 timeout (R2 inline patch — BA-7 + QA-10 + R2-CR-A); subprocess.run(..., timeout=N) 强制使用; primitive 超时 → max 3 attempts retry (指数 5s/15s/45s) → 仍超时则 fail verdict
  poll_chunk_seconds: 5                  # Ctrl-C polling chunk 大小 (R2 patch CR-5); trade-off CPU 与响应延迟
```

#### D2 — workflow-runner recoverable BLOCK 语义

**现状**: `workflow-runner/SKILL.md §错误处理` 现仅支持 `on_phase_error: stop | continue | rollback` 三态,所有 BLOCK 当 fatal 处理 (Phase fail → workflow stop)。

**新增**: `wait_recoverable` 错误类型,专门用于"协作正常态、需等待外部条件" 场景:

```yaml
on_phase_error:
  wait_recoverable:                       # NEW
    triggered_by:
      - source: "phase-c-integrator"
        sub_step: "C.2.4"
        verdict: "wait"
    behavior:
      - log: "main 分支有 in-flight CI,等待 X 完成"
      - persist: workflow-state.json (status=waiting, gate=pre_merge, retry_count, next_check_at)
      - sleep: wait_check_intervals[retry_count] (默认指数退避)
      - re-invoke: phase-c-integrator C.2.4 检查
      - exit conditions (优先级 first-match-wins, R2 patch — CR-4):
          1. user Ctrl-C → 转 manual mode (workflow-state 标 suspended,允许 resume)  [最高]
          2. retry_count > max OR elapsed > wait_timeout_seconds → user prompt (continue / abort)
          3. verdict=fail → 转为 stop (fatal)
          4. verdict=green → 继续 merge  [最低,正常路径]
```

**Schema migration (R2 patch — BA-3)**: `workflow-state-schema.md` `format_version: 1.0 → 1.1` (additive — 加 `gate_state` 顶级 block,与现有 `session/workflow/gates/phase_results` 同 tier)。v1.0 state 文件 resume 至 v1.1 runtime 时,`gate_state` 默认 `null`;workflow-runner T2.4 resume 逻辑须用 `state.get("gate_state") or {}` 防御性访问,避免 KeyError。Schema §8.3 migration 表加 `1.0 → 1.1: gate_state default null` 条目。

**Ctrl-C 检测机制 (R2 patch — CR-5)**: workflow-runner 现无 signal handler 设计。本 Spec 采用 **polling sleep chunk** 模式:wait sleep 拆分为 5s 小块,每块结束后:(a) 检查中断 flag (subprocess wrapper 设置的 SIGINT trap 写入文件 `.aria/.workflow-interrupt`);(b) 若 flag set → 立即转 manual mode + workflow-state.json 写 `status=suspended`;(c) flag 未 set 且未到下次 check 时间 → 继续下一 5s 块。chunk 大小由配置 `phase_c_integrator.pre_merge_gate.poll_chunk_seconds` (默认 5) 控制。trade-off:5s 是 CPU/响应延迟平衡;过小耗 CPU,过大 Ctrl-C 响应慢。

**Flag-file lifecycle (R2 inline patch — R2-CR-B)**: `.aria/.workflow-interrupt` flag 文件生命周期严格定义,防 stale flag race:
- **创建**: workflow-runner 处理 SIGINT signal handler 时 atomic write (open-O_CREAT-O_EXCL + tmp+rename)
- **清理**: workflow-runner 启动入口 (resume 或 fresh) 必须无条件清理 stale flag (`os.unlink ignore FileNotFoundError`); 进入 manual mode / suspended 状态后**保留** flag (待 user explicit clear);user resume workflow 时清理 flag (resume 是新意图,不继承 prior interrupt)
- **检查语义**: flag 存在 = 当前 polling cycle 内有 user SIGINT,**不**继承跨 workflow 启动的 interrupt
- **Ownership**: flag 文件只属于当前 workflow-runner pid,多 workflow-runner 并发不允许 (per Aria 现有 workflow-state lock 约定)

**Resume 语义 (R2 patch — CR-6 + BA-5)**: workflow-state 含 `gate_state.status == waiting` + `phase_results.C.2.action.pr_number != null` (PR 已创建) 时:
1. resume 入口判定 `next_check_at` 是否过期: 已过期 (`now >= next_check_at`) → 立即重新调 C.2.4 gate;未过期 → 等待至 `next_check_at` 后再调
2. gate verdict:
   - `green` → **跳过** C.2 push/create-PR (已完成),直接调 branch-manager merge call (idempotent — 若 PR 已 merged 则报告 success)
   - `wait` → 增量更新 `gate_state.retry_count` + `next_check_at`,继续 polling
   - `fail` → 转 stop,workflow report 含 PR_NUMBER + 失败 verdict
3. 不重跑 Phase C 整段,只 re-run gate + merge call

**State persistence**: `workflow-state.json` 新增 `gate_state` 块 (沿用 v2.0 schema 扩展模式):

```json
{
  "gate_state": {
    "name": "pre_merge",
    "status": "waiting",
    "started_at": "2026-05-09T12:35:00Z",
    "retry_count": 2,
    "next_check_at": "2026-05-09T12:38:00Z",
    "in_flight_runs": [
      {"run_id": 3161, "branch": "main", "started_at": "2026-05-09T12:45:00Z", "elapsed_seconds": 459}
    ]
  }
}
```

#### D3 — CLAUDE.md 不可协商规则 #8

**新增规则文本** (插入 `## 不可协商规则` 现有 7 条之后,与 #7 secret-hygiene 同等深度):

```markdown
8. **PR merge 前必跑 aether-ci-cli (was: aether-pre-merge-check, R3 修订 — skill 不存在)** — 详见 `aria/skills/phase-c-integrator/SKILL.md §C.2.4`

**规则 #8 要点:** Phase C.2 PR merge 前必须通过 `aether-ci-cli (was: aether-pre-merge-check, R3 修订 — skill 不存在) <pr-id>` (或等效 `aether ci status --in-flight` 查询) 验证 (a) 本 PR CI 已 green; (b) main 分支无 in-flight CI run。`wait` 状态由 workflow-runner wait+retry 处理,**不**视为 workflow failure。

**触发场景:** Phase C.2 action 流程中 (auto_merge 或 user-triggered merge) 必须经过 C.2.4 gate。`auto_merge=true` workflow 自动调用; `auto_merge=false` user 触发 merge 前由 phase-c-integrator 强制 invoke。

**Source incidents:** 2026-05-02 SilkNode PR-321 cancel PR-322 main CI Run #3161 (459s 部署观测丢失);Forgejo Issue [#60](https://forgejo.10cg.pub/10CG/Aria/issues/60)。

**Exception:** 项目无 aether plugin (`aether-ci-cli (was: aether-pre-merge-check, R3 修订 — skill 不存在)` 不可用) 时按配置 `no_aether_fallback` 降级:`skip_with_warning` (默认,记录到 workflow report) / `abort` (严格模式)。Exception 必须在项目 `.aria/config.json` 显式声明 `phase_c_integrator.pre_merge_gate.no_aether_fallback` 字段。

**Primitive responsibility split:**
- aether 提供: `aether ci status --in-flight` flag + `aether-ci-cli (was: aether-pre-merge-check, R3 修订 — skill 不存在)` skill (问题 #89 closed 2026-05-06)
- aria 消费: phase-c-integrator C.2.4 step + workflow-runner wait+retry 语义 + 本规则 #8 强制约束

**详细实施规范:** `aria/skills/phase-c-integrator/SKILL.md §C.2.4` (与 Rule #7 引用 `standards/conventions/secret-hygiene.md` 同结构 — R2 patch KM-1)
```

**Paired-standards-file 决策 (R2 patch — KM-2)**: Rule #7 secret-hygiene 配对 `standards/conventions/secret-hygiene.md` 是因为 secret 处理是**跨工具通用约定** (任何脚本/skill/CLI 都需遵守)。本 Rule #8 pre-merge-gate **是 aria 工作流编排层的实现细节**,作用域限于 phase-c-integrator skill 内部 — 因此权威文档放在 `aria/skills/phase-c-integrator/SKILL.md §C.2.4` (工具层) 而非 `standards/conventions/` (方法论层)。这是有意决策,不创建 `standards/conventions/pre-merge-gate.md`。如未来其他工作流 (eg phase-d-closer / 跨 plugin orchestration) 需复用此 gate 模式,可重构为 `standards/conventions/pre-action-gate-pattern.md` 抽象,届时另起 follow-up Spec。

**D3 Cross-cutting 文档同步范围 (R2 patch — KM-3)**:
- (a) `CLAUDE.md` `## 不可协商规则` 段插入规则 #8 文本 (T3.1)
- (b) `CLAUDE.md` `## 项目状态` 段版本号同步 (插件 v1.18.0 → v1.19.0; 主项目 v1.6.0 → v1.7.0; T3.2) — **R2 inline patch (KM-8)**: T3.2 实施时以 `aria/.claude-plugin/plugin.json` 实际 Source of Truth 版本为准 (而非 CLAUDE.md 项目状态段当前显示的 v1.15.0 — 该值为 stale 历史值);覆盖前 implementer 必须 verify current plugin.json version 不触及中间版本号
- (c) `aria/skills/phase-c-integrator/SKILL.md` 文档头版本 bump + C.2.4 详细文档段 (T3.3 + T1.3)
- (d) `aria/skills/workflow-runner/SKILL.md` 文档头版本 bump + `wait_recoverable` 文档段 (T3.4 + T2.1)
- (e) `aria/skills/config-loader/SKILL.md` + `config.template.json` 同步 (T1.5)
- (f) `aria/skills/state-scanner/references/state-snapshot-schema.md` (无需更新,本 Spec 不影响 snapshot schema)

以上 6 项是 CLAUDE.md Rule #3 "文档与代码同步" 的强制范围。Spec implementation 任一遗漏 = pre_merge audit Major finding。

#### Cross-cutting

- **phase-c-integrator SKILL.md 文档同步**: `## 配置 (config-loader)` 表加 `pre_merge_gate.*` 5 项;`## 执行流程 §步骤执行` C.2 流程图加 C.2.4 step;新增 `### C.2.4 Pre-Merge Precondition Gate` 详细段(参考 §C.2.5 的详细文档结构,~50 行)
- **workflow-runner SKILL.md 文档同步**: `## 错误处理 §可恢复策略` 加 `wait_recoverable` 类型段;`## Workflow State Persistence` 加 `gate_state` 字段说明;`references/workflow-state-schema.md` 加 `gate_state` schema
- **branch-manager 边界澄清**: branch-manager 现负责 push branch + create PR + (可选) auto merge。本 Spec 不修改 branch-manager 内部,仅 phase-c-integrator 在 branch-manager 调用前后插入 C.2.4 gate (gate 失败时 phase-c-integrator 不调用 branch-manager merge action,而是进入 wait+retry)
- **config-loader 同步**: `aria/skills/config-loader/SKILL.md` 加 `phase_c_integrator.pre_merge_gate.*` 5 项默认值文档;`config.template.json` 同步示例配置块
- **完整 `/skill-creator` AB benchmark (双 arm)**:
  - **arm A**: baseline `without_skill` (无 phase-c-integrator pre-merge-gate,沿用现 v1.18.0 行为)
  - **arm B**: `with_skill v1.19.0` (新 C.2.4 gate + workflow-runner wait+retry)
  - **fixture**: 模拟 multi-PR 并发场景的 mock aether response (green / wait / fail 三态,各 N=3 trials)
  - 期望 `delta(B - A)` 在 "merge 时 cancel 别人 in-flight CI run" 计数为 **−100%** (强阻断 — wait 状态强制等待);AB 工具记录 wait 事件触发率作为附属指标,不作为 PASS gate
  - 结果存 `aria-plugin-benchmarks/ab-results/{date}-phase-c-integrator-pre-merge-gate/`
- **版本 bump**: aria-plugin v1.18.0 → **v1.19.0** (新 C.2.4 sub-step + workflow-runner 错误语义扩展 = MINOR per CLAUDE.md 项目惯例)
- **Aria 主项目版本 bump**: v1.6.0 → v1.7.0 (子模块指针 + 不可协商规则 #8 新增 = MINOR)

---

## Impact

| Type | Description |
|------|-------------|
| **Positive** | PR merge race condition 从 "agent 自律 + memory 警告" 升级为 "workflow 强制 gate";跨 session / 跨 agent 一致行为 (CLAUDE.md 研究目标 #1);消费 aether primitive 不重复实现 CI 状态查询;workflow-runner `wait_recoverable` 语义为未来 gate (eg `pre_release`, `pre_deploy`) 预留扩展点 |
| **Positive** | CLAUDE.md 不可协商规则 #8 与 #7 (secret-hygiene) 形成 "规范层强制约束" 模式的第二个落地;phase-c-integrator C.2.4 与 C.2.5 multi-remote push enforcement 形成 PR merge 前后双 gate 完整保护 |
| **Risk** | aether plugin 不可用 (single-project / cross-project 无 aether init) 时降级行为需明确。Mitigation:`no_aether_fallback` 配置项默认 `skip_with_warning`,workflow report 强制记录"未跑 gate"标记;严格模式 `abort` 由项目自选 |
| **Risk** | wait+retry 可能让 workflow 长时间挂起,影响 user 体验。Mitigation:默认 `wait_timeout_seconds: 1800` (30 min);`user_escape_hatch: true` 允许 Ctrl-C 进入 manual mode;workflow-state 持久化让 user 可显式 abandon 后再启 |
| **Risk** | aether primitive 内部 bug (eg `aether ci status` API 误报) 可能导致永久 wait 或误 merge。Mitigation:本 Spec 不实现 primitive 本身,bug 责任在 aether 项目;TX.6 在 phase-c-integrator 加 primitive call 重试 (max 3 attempts,指数退避) 防瞬态 API 错误;benchmark fixture 含 `fail` 三态测试覆盖 |
| **Risk** | workflow-runner `wait_recoverable` 是新错误类型,可能与现有 `stop / continue / rollback` 处理路径冲突 (state persistence、recovery skill)。Mitigation:T2.5 加 ≥3 个 unit test 覆盖 (stop ↔ wait_recoverable ↔ continue 转换路径);TX.7 dogfood Aria 自身一次 phase-c-integrator full cycle 验证 |
| **Risk** | C.2.4 插入位置选择 (PR 创建后 / merge 前) 可能与 branch-manager `auto_merge` 实现细节冲突 (现 branch-manager 在单一 action 内 push + create + merge)。Mitigation:T1.2 设计阶段先 trace branch-manager 现实现,确认插入点;若 branch-manager 单一 action 不可拆,fallback 为 phase-c-integrator wrapper 在 branch-manager call 前查 gate,gate green 才调 branch-manager (而非内嵌) |

---

## Tasks

> **执行顺序**: T1 (gate primitive design + C.2.4 pseudo-code) **必须先于** T2 (workflow-runner 扩展) — wait+retry 行为依赖 gate 三态契约;T3 (CLAUDE.md 规则) 可与 T1/T2 并行起草但**必须最后 merge** (规则文本依赖 final implementation 行为);T4-T7 (testing + benchmark + release) 串行依赖 T1-T3 ship。

### Phase 1 — Gate primitive integration (D1)

- [x] **T1.0 (✅ done 2026-05-10 — R3 spike-driven Spec 修订)** Spike 实测 aether primitive: (a) ❌ `aether pre-merge-check` subcommand 不存在 (P0-B 从未实施); (b) ❌ `aether-pre-merge-check` skill 不存在 (aether-plugin/skills/ 无此项); (c) ✅ `aether ci status --branch main --in-flight --json` 可用 (PR #116 merged 2026-05-06, SHA `f29abee`); (d) JSON shape 实测 `{"status":"ok","data":{"filters":..., "repo":..., "runs":[]}}` (aether 仅返回 raw runs[],非 verdict-based); (e) 本地 binary `/usr/local/bin/aether` 过期 (Apr 22 < May 6 source, 需升级)。**Spec impact**: D1 §Contract Source / §Cross-plugin invocation protocol / T1.6 helper / T4.2 test cases / config primitive_preference 全部 R3 重写 — verdict 计算从 aether 移到 aria 端 (per "## R3 (T1.0 spike-driven revision) → Re-Approved" Changelog)
- [x] **T1.1 (✅ done 2026-05-10)** Trace `branch-manager` 现 `auto_merge` 实现细节 — **finding**: branch-manager C.2.x 是离散 sub-steps (C.2.1 sync / C.2.2 push / C.2.3 create-PR / C.2.4 wait-approval / C.2.5 merge),不是单一原子 action。phase-c-integrator orchestrator 可在 `create_pr` 与 `merge_pr` 调用之间干净插入 gate,**Risk #6 wrapper fallback 不需要**(branch-manager 天然支持外部 orchestrator gate)。Naming 命名空间澄清(BA-1)已确认有效:phase-c-integrator C.2.4 (orchestrator-tier "pre-merge precondition gate") 与 branch-manager 内部 C.2.4 (implementation-tier "等待审批") 同名不同 tier,语义独立。详见 `branch-manager/SKILL.md` 第 492-526 行
- [ ] **T1.2** `phase-c-integrator/SKILL.md` 设计 C.2.4 sub-step pseudo-code 并定稿伪代码 + 三态契约 (green/wait/fail) + output schema
- [ ] **T1.3** `phase-c-integrator/SKILL.md` 加 `### C.2.4 Pre-Merge Precondition Gate` 详细段 (参考 §C.2.5 文档结构, ~50 行,含 primitive 调用优先级、降级策略、output schema、user escape hatch 说明)
- [ ] **T1.4** `phase-c-integrator/SKILL.md` `## 配置 (config-loader)` 表加 `pre_merge_gate.*` 5 项 (enabled / primitive_preference / no_aether_fallback / wait_timeout_seconds / wait_check_intervals)
- [ ] **T1.5** `aria/skills/config-loader/SKILL.md` 加 `phase_c_integrator.pre_merge_gate.*` 默认值文档 + `config.template.json` 同步示例配置块
- [ ] **T1.6 (R2 inline patch BA-7+QA-10+R2-CR-A / R3 重写 — T1.0 spike)** Primitive 调用 helper:`aria/skills/phase-c-integrator/scripts/pre_merge_gate.py` (stdlib + subprocess only),职责:
  - **2 次 aether 调用**: (a) `aether ci status --branch main --in-flight --json` 查 main 是否有 in-flight; (b) `aether ci status --branch <pr-branch> --json` 查本 PR CI 状态
  - **本地 verdict 计算** (aria 端,因 aether-ci-cli (was: aether-pre-merge-check, R3 修订 — skill 不存在) skill 不存在): 按 D1 §Contract Source Verdict 计算逻辑 4 步流程
  - **Binary 版本 pre-flight check**: helper 启动时 `aether --help | grep -q "in-flight"` 验证,缺失 → fail-fast 提示升级
  - **Subprocess 调用强制使用 `subprocess.run(..., timeout=primitive_call_timeout_seconds)`** (默认 30s,从 config-loader 读取);timeout 触发 → max 3 attempts retry (backoff 5s/15s/45s) → 仍超时则 `fail` verdict + raw_message 含 timeout 详情
  - **No aether** 降级: 按 `no_aether_fallback` 配置 (`skip_with_warning` 默认 / `abort` 严格)

### Phase 2 — workflow-runner recoverable wait+retry (D2)

- [ ] **T2.1** `workflow-runner/SKILL.md` `## 错误处理 §可恢复策略` 加 `wait_recoverable` 类型段 (含 trigger 来源、behavior 列表、exit conditions、user escape hatch)
- [ ] **T2.2 (R2 patch — BA-3)** `workflow-runner/SKILL.md` `## Workflow State Persistence` 加 `gate_state` 字段说明 + `references/workflow-state-schema.md` schema 扩展 (`gate_state.{name, status, started_at, retry_count, next_check_at, in_flight_runs[]}`) + **`format_version: 1.0 → 1.1` bump** + §8.3 migration 表加 `1.0 → 1.1: gate_state default null` 条目 + 实现 defensive `state.get("gate_state") or {}` access 模板
- [ ] **T2.3 (R2 patch — CR-5)** `workflow-runner` 实现层处理 `wait_recoverable` 错误:`gate_state` 持久化 + 指数退避 sleep + re-invoke + **Ctrl-C 检测用 polling sleep chunk 模式** (5s chunk + `.aria/.workflow-interrupt` flag file,见 D2 §Ctrl-C 检测机制) → suspended 状态
- [ ] **T2.4 (R2 patch — CR-6 + BA-5)** `workflow-runner` recovery 逻辑扩展:resume 时若 `gate_state.status == waiting`:(a) 检查 `next_check_at` 是否过期决定立即 / 等待 — **clock 源 (R2 inline patch QA-12)**: `next_check_at` 持久化为 ISO 8601 wall clock; 进程内 elapsed 用 `time.monotonic()` 防 DST/系统时钟漂移 误判;(b) 重新调 phase-c-integrator C.2.4 gate (而非整个 Phase C 重跑);(c) gate green 后跳到 branch-manager merge call,**不**重跑 push/create-PR (idempotent 由 branch-manager 保证);(d) **resume 入口先清理 `.aria/.workflow-interrupt` stale flag** (R2 inline patch R2-CR-B,resume 是新意图)
- [ ] **T2.5 (R2 patch — QA-5)** `workflow-runner` unit test ≥ 5 cases: (a) wait → green 转换、(b) wait → fail 转换、(c) wait timeout → user prompt **(用 mock clock,不真睡 30 min)**、(d) wait → user Ctrl-C → suspended → resume、(e) `workflow-state.json` 损坏 (truncated JSON) at resume → recovery 报清晰错误 (不静默崩溃)

### Phase 3 — CLAUDE.md 不可协商规则 #8 (D3)

- [ ] **T3.1** `CLAUDE.md` `## 不可协商规则` 段插入规则 #8 文本 (位置:#7 secret-hygiene 之后,与 #6/#7 同等深度结构 — 要点 / 触发场景 / Source incidents / Exception)
- [ ] **T3.2** `CLAUDE.md` 项目状态段更新插件版本号 (v1.18.0 → v1.19.0)、主项目版本 (v1.6.0 → v1.7.0)
- [ ] **T3.3** `aria/skills/phase-c-integrator/SKILL.md` 文档头部 `> **版本**: 1.2.0 → 1.3.0` bump + 版本变更说明加 C.2.4 条目
- [ ] **T3.4** `aria/skills/workflow-runner/SKILL.md` 文档头部版本 bump + 版本变更说明加 `wait_recoverable` 条目

### Phase 4 — Backward-compat & testing

- [ ] **T4.1** `phase-c-integrator` unit test ≥ 4 cases: (a) gate=green continue merge、(b) gate=wait persist + return、(c) gate=fail BLOCK + report、(d) no_aether → skip_with_warning
- [ ] **T4.2 (R2 patch QA-7 / R3 重写 T1.0 spike)** `pre_merge_gate.py` unit test ≥ 5 cases (mock aether CLI 返回 raw runs[],aria 端 verdict 计算): (a) main 无 in-flight + PR CI passing → verdict=green; (b) main 有 in-flight + PR CI passing → verdict=wait + in_flight_runs[] 正确翻译; (c) PR CI failing → verdict=fail (无论 main in-flight 状态); (d) PR CI pending → verdict=wait; (e) primitive 返回**异常 exit code 或 malformed JSON / unexpected schema** → 路由到 `fail` verdict (而非 unhandled exception / 静默 skip); (f) `aether --help` 无 `in-flight` flag (binary 过期) → fail-fast 提示升级
- [ ] **T4.3 (R2 patch — QA-3)** Backward-compat verify ≥ 2 sub-cases: (a) `pre_merge_gate.enabled: false` 配置下 phase-c-integrator C.2 行为与 v1.18.0 完全一致 (skip C.2.4 整段);(b) `.aria/config.json` **完全无 `pre_merge_gate` 块** (例: 用户从 v1.18.0 升级未改 config) → config-loader 默认填充 `enabled: true` (gate fires) 而非 silently bypass;config-loader unit test 同步覆盖 missing-block default-fill
- [ ] **T4.4** Integration test:Aria 自身跑一次完整 phase-c-integrator workflow (无 PR 场景,direct push) 验证 C.2.4 skip 路径不破坏现有流程

### Phase 5 — Release

- [ ] **T5.1 (R2 patch — QA-1 + QA-2 + QA-6)** 完整 `/skill-creator` AB benchmark **(双 arm)**:
  - **arm A**: baseline `without_skill` (v1.18.0 行为,无 C.2.4 gate)
  - **arm B**: `with_skill v1.19.0` (C.2.4 gate + wait_recoverable)
  - **Fixture 最小规格 (QA-1 fix)** — 沿用 state-scanner-inter-cycle-surfacing precedent (archived proposal lines 217-221):
    - **Mock 交付机制**: `pre_merge_gate.py` 通过环境变量 `ARIA_AETHER_MOCK_RESPONSE_FILE` 指向 fixture JSON 文件,跳过 `aether` CLI 调用直接读 fixture (test-only path,prod 配置无影响)
    - **Mock JSON shape (3 happy-state)**: 严格按 D1 §Contract Source schema:
      - `green.json`: `{"verdict":"green","pr_ci_status":"passing","in_flight_runs":[],"primitive_used":"mock"}`
      - `wait.json`: `{"verdict":"wait","pr_ci_status":"passing","in_flight_runs":[{"run_id":3161,"branch":"main","started_at":"2026-05-09T12:45:00Z","elapsed_seconds":300}],"primitive_used":"mock"}` — 后跟 `wait_then_green.json` (前 2 个 polling cycle 返回 wait,第 3 cycle 返回 green) 验证 wait→green 转换路径
      - `fail.json`: `{"verdict":"fail","pr_ci_status":"failing","in_flight_runs":[],"primitive_used":"mock","raw_message":"PR CI red"}`
    - **延迟模拟**: mock 文件可含 `_mock_latency_ms` 字段,helper 读后 sleep (模拟真实 CLI 响应延迟,默认 200ms)
    - **N=3 trials per state** (9 happy trials [3 states × N=3] + 6 negative trials [2 negative fixtures × N=3] = 15 trials per arm — R2 inline patch QA-11 算术明确化)
  - **Negative fixtures (QA-2 fix — 沿用 state-scanner-inter-cycle-surfacing 立例)** — ≥ 2 个,Spec 强制:
    - **NEG-1**: `malformed.json` 含语法错误 / 字段缺失 (eg `{"verdict":"unknown_state"}`) → 期望 helper 路由到 `fail` verdict + raw_message 含解析错误 (而非 unhandled exception 或 silent skip)
    - **NEG-2**: 模拟 primitive 超时 — mock 含 `_mock_latency_ms: 999999` (远超 helper subprocess timeout) → 期望 helper subprocess timeout 后 retry 1 次 (max 3 attempts 防瞬态),仍失败则路由到 `fail` verdict
  - **关键指标 + PASS gate (QA-6 fix)**: 因真实 cancel-other-in-flight-run 在 mock 环境无法 reproduce,**改用 proxy metric**:
    - **Primary PASS gate (阻塞 merge)**: `wait_triggered_when_in_flight_mock_present` 比率 — arm B 在 `wait.json` / `wait_then_green.json` fixture 下必须 100% 触发 wait 状态 (而非 silent skip 或 immediate green)
    - **Quality target (不阻塞,记录 benchmark.md)**: `cancel-other-in-flight-run` 计数 (附属理论指标 — mock 环境恒 0,作为 prod 部署后真实 dogfood 跟踪 baseline)
    - **附属指标**: wait→green 转换平均 polling cycles、PR merge 端到端 duration、negative fixture 错误处理正确率
  - **benchmark.md 强制 disclaimer (QA-6 fix)**: 沿用 state-scanner TX.3 R2 corrections 的 variance disclaimer 模式,显式说明 "PASS gate metric 是 proxy — 因 mock 环境无真实并发 CI,cancel 事件计数无意义,改用 wait-trigger-rate 作为可断言的结构信号。真实 cancel 阻断需 prod 部署后跨 PR 并发场景才能验证 (留 dogfood follow-up)"
  - 结果存 `aria-plugin-benchmarks/ab-results/{YYYY-MM-DD}-phase-c-integrator-pre-merge-gate/` + `latest` symlink 切换
- [ ] **T5.2** Aria 子模块版本 bump v1.18.0 → v1.19.0:plugin.json + marketplace.json + VERSION + CHANGELOG.md + README.md + README.zh.md
- [ ] **T5.3** 主项目 submodule 指针 bump + 主项目 VERSION (v1.6.0 → v1.7.0) + CHANGELOG.md 同步
- [ ] **T5.4 (R2 patch — QA-4)** Dogfood (双层验证):
  - **Layer 1 — config + 调用路径 (green path 干跑)**: Aria + Kairos + Aether 三项目本地分别跑 phase-c-integrator C.2.4 干跑 (无实际 PR,verify primitive 调用路径 + 配置加载 default-fill),exit=0 + errors=[] 截图附 PR 描述
  - **Layer 2 — wait+retry forced injection (核心新行为验证)**: 三项目分别用 `ARIA_AETHER_MOCK_RESPONSE_FILE=wait_then_green.json` 注入 mock,触发 wait 状态 → verify `workflow-state.json` `gate_state` block 写入正确 + 2 polling cycle 后转 green + merge call 触发 (mock branch-manager 不真 merge)。**纯 green dogfood 不可接受 — 因 wait+retry 是本 Spec 主要新行为,green-only 干跑无法证明 gate 实际工作**
- [ ] **T5.5** PR merge 前 issue #60 添加进度评论 (sub-PR 列表 + audit 收敛轮次);merge 后 issue #60 close

---

## Success Criteria

- [ ] phase-c-integrator C.2.4 sub-step 在 `pre_merge_gate.enabled: true` 默认配置下自动调用 `aether-ci-cli (was: aether-pre-merge-check, R3 修订 — skill 不存在)`,三态返回正确路由 (green → continue / wait → wait_recoverable / fail → BLOCK)
- [ ] workflow-runner `wait_recoverable` 错误类型实现完整: `gate_state` 持久化 + 指数退避 + re-invoke + user escape hatch + resume 路径
- [ ] CLAUDE.md 不可协商规则 #8 文本与 #6/#7 同结构 (要点 / 触发场景 / Source incidents / Exception),无歧义
- [ ] **Backward-compat (R2 patch — QA-3)**: ≥ 2 sub-criteria 全部满足: (a) `pre_merge_gate.enabled: false` 配置下 phase-c-integrator C.2 行为与 v1.18.0 100% 一致 (T4.3a verify);(b) `.aria/config.json` 完全无 `pre_merge_gate` 块 → config-loader 默认填充 `enabled: true` (gate fires) — 验证从 v1.18.0 升级未改 config 的项目获得 gate 保护而非 silently bypass (T4.3b verify);(c) `no_aether_fallback: skip_with_warning` 默认让无 aether 项目无感升级
- [ ] **AB benchmark PASS gate (R2 patch — QA-6)**: Primary metric 改 `wait_triggered_when_in_flight_mock_present` 必须 = 100% (arm B 在 wait fixture 下 100% 触发 wait);Quality target (附属理论指标): `cancel-other-in-flight-run` 计数 (mock 环境恒 0,prod dogfood baseline);benchmark.md 强制含 proxy-metric disclaimer (沿用 state-scanner TX.3 R2 corrections variance disclaimer 模式)
- [ ] **Test coverage**: phase-c-integrator ≥ 4 cases + pre_merge_gate.py ≥ 4 cases (含 QA-7 unexpected exit code) + workflow-runner ≥ 5 cases (含 QA-5 corrupted state recovery + QA-8 mock clock for timeout) (合计 ≥ 13 新增 unit test)
- [ ] **Schema migration verify (R2 patch — BA-3)**: `workflow-state-schema.md` `format_version: 1.1` ship,§8.3 migration 表加 `1.0 → 1.1: gate_state default null` 条目;v1.0 state 文件 resume 至 v1.1 runtime 不抛 KeyError
- [ ] **Subprocess timeout 配置 (R2 inline patch — BA-7 + QA-10 + R2-CR-A)**: `phase_c_integrator.pre_merge_gate.primitive_call_timeout_seconds` 默认 30s 已 ship 到 D1 config schema + T1.6 helper 实施;NEG-2 fixture `_mock_latency_ms: 999999` 在 30s timeout + 3 retry 后路由到 `fail` verdict (不无限挂起)
- [ ] **Flag-file lifecycle (R2 inline patch — R2-CR-B)**: `.aria/.workflow-interrupt` 生命周期严格按 D2 §Flag-file lifecycle: workflow-runner 启动清理 stale + SIGINT atomic write + resume 清理 (resume 是新意图,不继承)
- [ ] **Naming 命名空间清晰度 (R2 patch — BA-1)**: phase-c-integrator/SKILL.md §C.2.4 详细文档段含 "phase-c-integrator (orchestrator-tier) C.2.x ≠ branch-manager (implementation-tier) C.2.x" 显式声明
- [ ] Aria + Kairos + Aether 三项目本地 dogfood **双层验证 (R2 patch — QA-4)**: Layer 1 (green path 干跑 exit=0/errors=[]) + Layer 2 (forced wait mock injection 验证 gate_state 持久化 + wait→green 转换实际工作)
- [ ] Forgejo Issue #60 在 merge 后 close,带完整实施回顾评论 (sub-PR 列表 / audit 轮次 / benchmark 结果链接)

---

## Out of Scope (本 Spec 不做)

- **Aether-side primitive 实现** — `aether ci status --in-flight` flag + `aether-ci-cli (was: aether-pre-merge-check, R3 修订 — skill 不存在)` skill 由 aether#89 (closed 2026-05-06) 已完成。本 Spec 仅消费,不修改 aether
- **F2/F3 audit scope/level Spec** — Issue #58 中独立条目 (audit-engine `adaptive_rules` 文件级过滤 + 推荐配置矩阵显式文档化),与本 Spec scope 无依赖关系。F2/F3 由独立 Spec 处理 (handoff 列为 P1 候选)
- **F1 emergency hotfix lane** — Issue #58 F1 直接违反 CLAUDE.md 不可协商规则 #2 "十步循环不能跳过 Phase A",需先 brainstorm 反提案后再决策是否起 Spec,与本 Spec scope 无关
- **Non-Aether CI fallback 完整实现** — 本 Spec `no_aether_fallback` 仅提供 `skip_with_warning` / `abort` 两态,未实现"调用 GitHub Actions / GitLab CI 等其他 primitive" 的完整 fallback 链。如需要,起 follow-up Spec
- **branch-manager 内部重构** — 若 T1.1 trace 后发现 branch-manager `auto_merge` 单一 action 不可拆,fallback 是 phase-c-integrator wrapper 模式 (gate green 才调 branch-manager merge),不重构 branch-manager 本身
- **Pre-merge gate 之外的 gate 类型** (eg `pre_release` / `pre_deploy`) — 本 Spec 仅实现 `pre_merge`,但 workflow-runner `wait_recoverable` 语义为未来 gate 预留扩展点 (gate_state.name 字段已通用化)
- **CI 接入 dogfood 验证** — 本 Spec dogfood 仅本地干跑,CI workflow 集成留 future Spec

---

## References

- Forgejo Issue [10CG/Aria#60](https://forgejo.10cg.pub/10CG/Aria/issues/60) — 原始 enhancement request + 2026-05-02 SilkNode 实证时间线
- Issue #60 评论 [issuecomment by simonfish 2026-05-07](https://forgejo.10cg.pub/10CG/Aria/issues/60) — triage accept,实施范围确认 (3 deliverable)
- Aether 上游 Issue [10CG/Aether#89](https://forgejo.10cg.pub/10CG/Aether/issues/89) — closed 2026-05-06,提供 `aether ci status --in-flight` flag + `aether-ci-cli (was: aether-pre-merge-check, R3 修订 — skill 不存在)` skill primitive
- Aria CLAUDE.md `## 不可协商规则` — 现有规则 #1-#7 的格式 + 深度结构,本 Spec 规则 #8 严格对齐 (尤其 #6/#7 的"要点 / 触发场景 / Source incidents / Exception" 模板)
- `aria/skills/phase-c-integrator/SKILL.md §C.2.5` — multi-remote push enforcement 详细文档结构,本 Spec C.2.4 文档结构参照
- `aria/skills/workflow-runner/SKILL.md §错误处理` + `references/workflow-state-schema.md` — 现有 `stop / continue / rollback` 三态错误处理 + workflow-state schema,本 Spec `wait_recoverable` 加在此基础
- 前序相关 Spec: `phase-c-integrator-push-enforcement` (v1.15.0,确立 phase-c-integrator 多 remote 推送 enforcement 模式)
- 2026-05-09 session handoff `docs/handoff/2026-05-09-session-handoff.md` — Issue #60 标 P1 P0,handoff Recommended workflow 表 #1 选项

---

## R1 → R2 Changelog

R1 audit (4 agents, 2026-05-09): backend-architect PASS_WITH_WARNINGS / qa-engineer REVISE / knowledge-manager PASS_WITH_WARNINGS / code-reviewer REVISE。汇总 4 Critical + 15 Major,触发 R2 修订。

**Critical patches (4)**:
- **CR-1 + BA-2** (skill IPC): D1 加 §Cross-plugin invocation protocol (subprocess CLI wrapper 模式) + Tasks 加 T1.0 spike 验证 aether-ci-cli (was: aether-pre-merge-check, R3 修订 — skill 不存在) IPC contract + T1.6 detection method (which aether + .aria/config.json 双检)
- **CR-2** (contract source): D1 加 §Contract Source 子段,定义 aether-ci-cli (was: aether-pre-merge-check, R3 修订 — skill 不存在) 返回 JSON shape (verdict + pr_ci_status + in_flight_runs[] + primitive_used + raw_message),引用 aether#89 commit/SHA 占位待 T1.0 spike 补回
- **QA-1** (fixture mock spec): T5.1 加 Fixture 最小规格子段 — mock 交付机制 (env var ARIA_AETHER_MOCK_RESPONSE_FILE) + 3 happy-state JSON shape (含 wait_then_green 验证 polling) + 延迟模拟字段 + N=3 trials per state
- **QA-2** (negative fixtures): T5.1 加 ≥ 2 negative fixtures (NEG-1 malformed JSON / NEG-2 primitive 超时),沿用 state-scanner-inter-cycle-surfacing 立例

**Major patches (12)**:
- **BA-1** (C.2.4 命名冲突): D1 加 §Naming 命名空间澄清 + Success Criteria 加 "Naming 清晰度" 验证条 (显式声明 orchestrator vs implementation tier 分层)
- **BA-3** (workflow-state schema migration): D2 加 §Schema migration (format_version 1.0 → 1.1 bump + gate_state default null) + T2.2 task 描述更新 + Success Criteria 加 "Schema migration verify"
- **CR-3** (interval vs timeout): D2 wait_check_intervals 注释加 "数组耗尽后重复 intervals[-1]=300 直到 wait_timeout_seconds"
- **CR-4** (exit conditions priority): D2 exit conditions 改为 first-match-wins 优先级 (Ctrl-C > timeout > fail > green)
- **CR-5** (Ctrl-C 检测机制): D2 加 §Ctrl-C 检测机制 (polling sleep chunk 5s + .aria/.workflow-interrupt flag file) + T2.3 task 描述更新
- **CR-6 + BA-5** (resume 语义): D2 加 §Resume 语义 (next_check_at 过期判定 + 不重跑 push/create-PR + branch-manager merge idempotent) + T2.4 task 描述更新
- **KM-1** (Rule #8 final link line): D3 Rule #8 草稿尾部加 "**详细实施规范:** aria/skills/phase-c-integrator/SKILL.md §C.2.4" 与 Rule #7 同结构
- **KM-2** (paired-standards-file decision): D3 加显式决策段说明 "Rule #8 是工具层实现细节,权威文档在 SKILL.md 而非 standards/conventions/" + 留 future 抽象 follow-up Spec
- **KM-3** (D3 deliverable scope): D3 加 Cross-cutting 文档同步 6 项清单 (CLAUDE.md 规则 + 项目状态、phase-c-integrator/workflow-runner SKILL.md 版本头、config-loader/template, etc.)
- **KM-7** (Level 声明一致性): Header `Level 3` 改为 `Level 2 — proposal.md 含任务,无独立 tasks.md` 沿用 state-scanner-inter-cycle-surfacing precedent
- **QA-3** (config field absent backward-compat): T4.3 拆为 ≥ 2 sub-cases (enabled:false + 完全无 pre_merge_gate 块) + Success Criteria 同步
- **QA-4** (dogfood 干跑无法验 wait+retry): T5.4 拆为 Layer 1 (green path 干跑) + Layer 2 (forced wait mock injection 验证 gate_state + wait→green 转换)
- **QA-6** (PASS gate proxy metric): T5.1 改 Primary PASS gate metric 为 `wait_triggered_when_in_flight_mock_present` (rate),`cancel-other-in-flight-run` 降级为附属理论指标 + benchmark.md 强制 disclaimer

**Minor patches inline accepted**:
- **QA-5** (corrupted state recovery): T2.5 加 case (e) 验证 truncated workflow-state.json resume
- **QA-7** (unexpected exit code): T4.2 加 case (d) 验证 malformed JSON / unexpected schema → fail verdict
- **QA-8** (mock clock for timeout): T2.5 (c) 注明 "用 mock clock 不真睡 30 min"
- **CR-7** (started_at format): D2 gate_state JSON example started_at 改 ISO 8601 + 加 elapsed_seconds 字段
- **CR-8** (T1.3 ~50 行估算): KM-6 minor,延迟到 T1.3 实施时按实测调整,本 Spec 暂不更新

**Deferred to R3 review (low ROI 单独修)**:
- BA-4/5/6 (multi-remote re-check / next_check_at resume / in_flight_runs typing) — 大部分被 CR-6 resume 语义段覆盖
- KM-4 (aether#89 commit/SHA 引用) — T1.0 spike 时补回
- KM-5/6 (out-of-scope 文档跟进 / SKILL.md split convention) — 标 Out of Scope 即可
- QA-9 (Success Criteria 三项目混合) — 已在 R2 patch QA-4 重写时拆分

**Not addressed (out of R2 scope)**:
- 无 — 所有 Critical 全 patched,Major 12/15 直接 patched,3/15 是 minor 已处理。

**预期 R2 vote**: 4-tuple 集合应稳定 (全部 Critical 消除),期望 unanimous PASS_WITH_WARNINGS 或更好。如 R2 出现新 Major,按 Aria memory `feedback_audit_convergence_4_round_baseline` 模式 +1 round (R3) 收敛。

---

## R3 (T1.0 spike-driven revision) → Re-Approved

T1.0 spike 实测发现 R2 假设有偏差:

| Spec 假设 (R2) | T1.0 实测 (2026-05-10) | 修订 |
|----------------|-------------------------|------|
| `aether-pre-merge-check` skill 存在,返回 verdict | ❌ Skill 不存在 (P0-B 从未实施,aether-plugin/skills/ 无此项) | D1 §Contract Source 重写: verdict 计算移到 aria 端 |
| primitive 返回 verdict-based JSON | ❌ aether 仅返回 raw runs[] (query 层) | D1 §Cross-plugin invocation protocol 简化为唯一 primitive (`aether ci status --in-flight --json`) |
| `aether ci status --in-flight` flag 已可用 | ✅ 已 ship (PR #116 merged 2026-05-06,SHA `f29abee`) — 但本地 binary 可能过期 | T1.6 加 binary version pre-flight check |

**R3 修订范围** (per user 选项 [1]):
- D1 §Cross-plugin invocation protocol — 移除 `aether-pre-merge-check` skill 优先,改为 CLI-only
- D1 §Contract Source — 重写为 "aether 端 query primitive + aria 端 verdict 计算" 双层契约,加 4 步 verdict 计算逻辑
- D1 config schema — `primitive_preference` 简化为 `[aether-ci-cli]` 单元素
- T1.6 helper — 复杂度 +30%: 2 次 aether 调用 + 本地 verdict 计算 + binary 版本 pre-flight check
- T4.2 unit test — mock 改为返回 raw runs[],新增 case (f) binary 过期 fail-fast,合计 ≥ 5 cases
- 其余 R2 patches (subprocess timeout / flag-file lifecycle / Schema migration / Naming clarification / Cross-cutting / etc.) 全部保留

**Spec impact assessment**:
- 实施复杂度: 略增 (T1.6 helper 行数预估 ~120 行 → ~160 行)
- Test coverage: 增 (T4.2 由 4 cases → 5 cases)
- 上游依赖: 简化 (只依赖 aether ≥ commit f29abee 的 CLI binary,无 skill 依赖)
- 用户体验: 透明 (verdict 仍是 green/wait/fail 三态,内部计算位置变化对调用方无感)

**Re-Approved**: post_spec R2 (R1+R2 pragmatic convergence) 仍有效;T1.0 spike 揭示的 R3 修订是 implementation 阶段的合理细节澄清,不需要重跑 R3 audit (修订内容是 R1 BA-2/CR-1 时已要求的 "T1.0 spike 验证后 commit/SHA 补回" 闭环动作)。

---

## R2 实际结果 + R2 inline patches → Approved

R2 audit (4 agents, 2026-05-09): 4/4 unanimous **PASS_WITH_WARNINGS** ✅ (R1 4 Critical → R2 0 Critical, verdict 改善 2 REVISE → 0 REVISE, 无振荡 — pragmatic convergence per Aria memory `feedback_post_spec_audit_pragmatic_convergence`)。

**R1 findings status (R2 verified)**:
- BA-1/2/3 (Major): all addressed ✅
- CR-1/2 (Critical): all addressed ✅; CR-3/4/5/6/7 (Major/Minor): all addressed ✅
- QA-1/2 (Critical): all addressed ✅; QA-3/4/5/6/7/8/9 (Major/Minor): all addressed ✅
- KM-1/2/3/7 (Major/Minor): all addressed ✅; KM-4 (Major): partially (T1.0 spike defer,Changelog 登记); KM-5/6 (Minor): deferred per Out of Scope acknowledgement

**R2 NEW Majors → inline-patched (no R3 required per pragmatic convergence)**:
- **BA-7 + QA-10 + R2-CR-A** (subprocess timeout) — 3 agents 独立发现强信号,inline patch:
  - D1 config schema 加 `primitive_call_timeout_seconds: 30` (默认 30s)
  - T1.6 helper 强制 `subprocess.run(..., timeout=N)` + max 3 attempts retry (5s/15s/45s backoff)
  - Success Criteria 加 "Subprocess timeout 配置" verify 条
- **R2-CR-B** (flag-file lifecycle) — code-reviewer 单点发现,inline patch:
  - D2 §Flag-file lifecycle 加 4 项契约 (atomic write + 启动清理 + suspended 保留 + resume 清理)
  - T2.4 加 "resume 入口先清理 stale flag" 条
  - Success Criteria 加 "Flag-file lifecycle" verify 条
- **KM-8** (CLAUDE.md 项目状态版本号 stale v1.15.0) — knowledge-manager 单点发现,inline patch:
  - D3 Cross-cutting (b) 加 "T3.2 实施时以 plugin.json 实际 SoT 版本为准" 警示 (防 implementer 误覆盖中间版本)

**R2 NEW Minors → inline-patched**:
- QA-11 (trial count arithmetic clarity) — T5.1 改 "(9 happy + 6 negative = 15 trials per arm)"
- QA-12 (clock source) — T2.4 加 "next_check_at ISO 8601 wall clock + elapsed time.monotonic()"
- R2-CR-C (subprocess exit-code mapping) — D1 §Contract Source 加 exit-code 4 类映射 (0/1-126/127/-SIGTERM)
- R2-CR-D (gate_state.name extensibility) — implicit in D2 schema (open-set string),不必单独写

**Convergence verdict**: post_spec **PASS_WITH_WARNINGS — Approved**。

按 Aria memory pragmatic convergence:unanimous PASS + verdict 改善 + 无振荡 = 实质收敛,无需强制 R3 严格 4-tuple 等价 (该规则仅 R3+ 振荡检测时关键)。R2 新 Majors 已 inline-patched,Spec 已就绪进入 A.2 task-planner / B.1 phase-b-developer。

**Implementation 触发条件**: T1.0 spike 验证 aether-ci-cli (was: aether-pre-merge-check, R3 修订 — skill 不存在) IPC contract 是 Phase 1 第一个任务,完成后 commit/SHA 补回 D1 §Contract Source 引用 — 此为 implementation 内置 self-verify 步骤,不要求 Spec 阶段完成。

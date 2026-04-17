# aria-2.0-m1-mvp — Tasks

> **Parent**: [proposal.md](./proposal.md)
> **US**: [US-021](../../../docs/requirements/user-stories/US-021.md)
> **Total**: ~100h (Core ~80h + Buffer ~20h, per PRD v2.1 §M1 baseline)
> **Status**: Draft (Phase A.2 post_spec convergence done 2026-04-17 Round 6)

## Task 工时基线

| ID | Task | 估算 | 依赖 | 验收 | Agent 主责 |
|----|------|------|------|------|-----------|
| **T0** | M1 kickoff + synthetic fixture 初始化 | 2h | — | T0.done | knowledge-manager |
| **T1** | Legal carryover + Registry auth + 镜像生产化 | 12h | T0 | T1.done + `anthropic_api_terms_verified=true` | legal-advisor (T1.a) + backend-architect (T1.b/c) |
| **T2** | Nomad job template + host volume (outputs + inputs 三节点) | 16h | T1.c (镜像 available) | T2.done + inputs volume 三节点 smoke PASS | backend-architect |
| **T3** | Issue schema v0.1 + dispatch 脚本 + DEMO fixture | 14h | T2 | T3.done + schema validator PASS | backend-architect + ai-engineer (prompt 模板) |
| **T4** | Runner entrypoint (prompt 模板 + stream-json + 幂等三态 + trap) | 20h | T3 | T4.done + 单次 DEMO dispatch smoke PASS | ai-engineer + backend-architect |
| **T5** | DEMO E2E 5 轮 × 2 + profiling | 16h | T4 | T5.done + `e2e_demo_passed=true` | qa-engineer + ai-engineer |
| **T6** | M1 Report + handoff v1.0 + AD-M1-* 回写 | 6h | T1-T5 | T6.done + handoff validator PASS (final) | knowledge-manager + tech-lead |
| Buffer | 预留 | 20h | — | Week 2 checkpoint 触发分配 | — |

**Total Core**: 86h; **Buffer**: 20h (含 R-M1-7 Week 2 checkpoint reforecast 机制)

---

## T0 — M1 Kickoff (2h)

**先决**: `post_spec` 收敛审计 Round 6 PASS (本 Spec 进入 A.2 起点)。

- [ ] **T0.1** 创建 Forgejo Issue 10CG/Aria (0.3h) — 标题 "[US-021] M1 MVP 手动 E2E dispatch", body 引用 US-021.md + proposal.md
- [ ] **T0.2** 创建 synthetic fixture repo stub (1h)
  - 路径: `aria-plugin-benchmarks/ab-suite/m1-mvp/fixtures/`
  - 内容: README.md + `src/` 空 Python/Node/Go 模块 × 3 (供 DEMO-002 非语言绑定)
  - commit 基线 (供 DEMO-002 验证 diff 命中)
- [ ] **T0.3** 架构决策位约定 (0.5h)
  - `aria-orchestrator/docs/architecture-decisions.md` 预开 AD-M1-1 ~ AD-M1-9 占位 (T6 统一回填)
  - `.aria/decisions/` 文件夹无需新建 (已有 M1 scope reorg 决议)
- [ ] **T0.4** 缓冲 (0.2h)

**T0.DoD**: Forgejo Issue URL 记入 US-021.md; fixture repo commit SHA 记入 T3 输入; AD-M1-* 占位行到位。

---

## T1 — Legal Carryover + Registry + 镜像生产化 (12h)

> **重要**: T1 是 M1 前置闸门 (per AD-M1-1 T1 交付物扩展), T2/T3 启动条件 = `T1.a.done + T1.b.done + T1.c.done`。

### T1.a — Legal Carryover (3.5h)

- [ ] **T1.a.1** M1 legal-carryover memo 起草 (2h)
  - 产物: `aria-orchestrator/docs/m1-legal-carryover.md`
  - 模板: 参照 M0 `standards/legal/scoped-memo-template.md`
  - 必填 clause-by-clause mapping table 列: `clause#` / `clause_text` / `M1_applicability (yes/no)` / `review_date` / `reviewer_role`
  - 审视项: IS-4 失效 / Anthropic ToS §7-8 / 数据分类 / R10 / R9 GLM legacy / Forgejo registry / end-user consent debt
- [ ] **T1.a.2** M0→M1 Luxeno 数据清理 (1h, per AD-M1-1 T1 交付物扩展)
  - 检查 Luxeno 日志是否含 M0 测试数据 (headers / inputs / outputs)
  - 若有 → 发送 Luxeno 清理请求 (记录 request id + 回应时间)
  - 输出 `m0-m1-transition-audit.md` 附在 memo 尾部
- [ ] **T1.a.3** Owner signoff (0.3h, per AD-M0-9 solo-lab)
  - Memo 最后一行 `Signed-by: human:simonfish @ 2026-MM-DD` (机械 gate 检测)
- [ ] **T1.a.4** 缓冲 (0.2h)

**T1.a.DoD**: memo 文件存在 + 最后一行签字 + `handoff.legal_assumptions.anthropic_api_terms_verified=true` 可回填。

### T1.b — Registry Auth + Bot Token Lifecycle Spike (4h)

- [ ] **T1.b.1** Forgejo container registry auth 选型 Spike (2h, per AD-M1-1)
  - 候选: (a) bot account + PAT (推荐) vs (b) maintainer PAT (不推荐)
  - 验证 `docker login forgejo.10cg.pub` + `docker push` 流程可跑通
  - 失败回退 = nomad artifact + docker load (per BA-M1, 额外 ~8h)
  - 输出: `spike-report-registry-auth.md`
- [ ] **T1.b.2** Bot token lifecycle 设计 (1.5h, per LA-NEW-1 + LA-R3-1)
  - Nomad secret 注入机制设计 (不做实装)
  - 60 天 rotation 自动化草案 (cron + Forgejo API POST new token)
  - Leak 响应流程 (revoke + new PAT issuance)
  - 输出: `bot-token-lifecycle-design.md`
- [ ] **T1.b.3** Forgejo registry access audit (0.5h, per AD-M1-8)
  - 验证 registry 为 private-only (无 auth 无法 pull)
  - 验证 pull 需有效 token
  - 输出 access audit 报告

**T1.b.DoD**: `docker push` 成功 + token lifecycle design 文档存在 + access audit 报告存在。

### T1.c — 镜像生产化 (4h)

- [ ] **T1.c.1** Dockerfile 微调 (1h) — 继承 M0 `aria-runner/Dockerfile`, 调整:
  - `ENV ARIA_MODEL=claude-opus-4-5-20250929` (per AD-M1-6 snapshot id)
  - 无 `ANTHROPIC_BASE_URL` (officially unset, per AD-M1-6)
  - `ENTRYPOINT` 升级为 T4 新版本 (接 T4 交付)
- [ ] **T1.c.2** Build + tag 策略 (1h, per AD-M1-2)
  - `docker build -t forgejo.10cg.pub/10CG/aria-runner:claude-<sha>` (immutable)
  - `docker tag ... forgejo.10cg.pub/10CG/aria-runner:claude-latest` (mutable)
  - 记录 `image_sha256`
- [ ] **T1.c.3** Push 两 tag 到 registry (0.5h)
- [ ] **T1.c.4** 镜像 pull 验证 (从三个 heavy 节点, 各 auth + pull 成功) (1h)
- [ ] **T1.c.5** 缓冲 (0.5h)

**T1.c.DoD**: registry 有 `claude-<sha>` + `claude-latest` 两 tag; 三 heavy 节点均可 pull; `image_sha256` 记入 T6.

---

## T2 — Nomad Job Template + Host Volume (16h)

> **关键门控 (per BA-C1)**: inputs volume 三节点验证先于 T3 启动, 否则后续 DEMO 会因调度失败。

### T2.1 — Host Volume 声明 (4h)

- [ ] **T2.1.1** 三 heavy 节点 `/etc/nomad/client.hcl` 配置 (2h)
  - `aria-runner-outputs` → `/opt/aether-volumes/aria-runner/outputs` (M0 已验证)
  - **`aria-runner-inputs` → `/opt/aether-volumes/aria-runner/inputs`** (新增, per BA-C1)
  - 三节点分别 reload nomad agent
- [ ] **T2.1.2** 三节点 smoke dispatch 验证 inputs mount (1.5h, per BA-C1 门控)
  - 最简测试 alloc: 挂载 inputs volume, `ls /opt/aria-inputs` 非空 → PASS
  - 任一节点失败 → 回退重配置, 修复后再测
- [ ] **T2.1.3** 缓冲 (0.5h)

### T2.2 — Nomad Job Template (8h)

- [ ] **T2.2.1** HCL template 起草 (4h)
  - 路径: `nomad/jobs/aria-runner-template.hcl`
  - `parameterized` block (meta=ISSUE_ID)
  - `volume` stanza 挂 outputs + inputs
  - `env` stanza: `ARIA_SETTINGS_JSON` 从 Nomad meta 或硬编码 (非继承 M0 草稿)
  - `resources`: CPU 2000 MHz / memory 2048 MiB / disk 4096 MiB (per BA-I1)
  - `tmpfs`: `/tmp:size=1024m` + `/root:size=512m` (per BA-R2-C2)
  - `readonly_rootfs = true` (M0 继承)
- [ ] **T2.2.2** Job register + dispatch smoke 测试 (2h)
  - `nomad job run aria-runner-template.hcl` 注册
  - `nomad job dispatch -meta ISSUE_ID=smoke-001 aria-runner-template` 验证可触发
  - 记录 `nomad_job_version` 到 T6 handoff
- [ ] **T2.2.3** `nomad/README.md` deployment + 排错手册 (1.5h)
- [ ] **T2.2.4** 缓冲 (0.5h)

### T2.3 — Resource Profiling 基线 (4h)

- [ ] **T2.3.1** smoke alloc 跑 `stress-ng` 占用 → 验证 2048 MiB / 4096 MiB 上限有效 (1.5h)
- [ ] **T2.3.2** tmpfs 1024m 容量测试 (1h, per BA-R2-C2): mock git clone (~200 MiB) + dummy stream-json buffer (~100 MiB), 观察 p95 使用率
- [ ] **T2.3.3** 输出 `resource-baseline.md` 记入 T6 (1h)
- [ ] **T2.3.4** 缓冲 (0.5h)

**T2.DoD**: host volume 三节点 PASS; Nomad job registered + dispatch smoke PASS; resource baseline 记录。

---

## T3 — Issue Schema v0.1 + Dispatch Script + DEMO Fixture (14h)

### T3.1 — Issue Schema v0.1 Artifact (3h)

- [ ] **T3.1.1** 起草 `openspec/changes/aria-2.0-m1-mvp/artifacts/issue-schema-v0.1.md` (2h, per AD-M1-3)
  - 字段: `id`, `title`, `description`, `files[]`, `expected_changes`
    - `expected_changes.expected_file_touched[]` (必填, per QA-C1)
    - `expected_changes.expected_diff_contains[]` (必填, 字面量子串, 范围 `+` 行, per QA-N1)
  - `ip_classification` 必填, v0.1 仅允许 `synthetic`
  - 注明: v0.1 breaking change 可接受 escape hatch (per proposal §3)
- [ ] **T3.1.2** schema validator (Python stdlib, 仿 M0 handoff validator) (1h)
  - 路径: `openspec/changes/aria-2.0-m1-mvp/artifacts/validate-issue-schema.py`
  - 检查: 必填字段 / enum 值 / 类型

**T3.1.DoD**: issue-schema-v0.1.md 存在 + validator 对 DEMO-001/002 验证 PASS。

### T3.2 — DEMO Fixture Issue 设计 (5h)

- [ ] **T3.2.1** DEMO-001.yaml 起草 (1.5h, synthetic trivial)
  - 路径: `.aria/issues/DEMO-001.yaml`
  - scenario: 修改 `aria-plugin-benchmarks/ab-suite/m1-mvp/fixtures/README.md` 的一行 (synthetic)
  - `expected_file_touched: ["README.md"]`
  - `expected_diff_contains: ["<specific content>"]`
  - `ip_classification: synthetic`
- [ ] **T3.2.2** DEMO-002.yaml 起草 (2.5h, synthetic non-trivial)
  - scenario: 在 fixture repo 新增 `src/<lang>/utility.py` + `tests/test_utility.py`
  - 期望 claude 产出完整 function + test
  - `expected_file_touched: ["src/python/utility.py", "tests/test_utility.py"]`
  - `expected_diff_contains: ["def utility_func", "def test_utility_func", "assert"]`
  - `ip_classification: synthetic`
  - 注: 设计需避免 claude "no-op" 陷阱 (per QA-R2) — issue 描述必须含明确"新增"动词 + 具体文件/函数名
- [ ] **T3.2.3** DEMO issue 合成 IP 审查 (0.5h, per LA-I1 + AD-M1-9)
  - 确认 DEMO-001/002 inputs 无 10CG 真实业务 IP
  - 记入 `DEMO-{001,002}-ip-classification-audit.txt` (per LA-R3-5)
- [ ] **T3.2.4** 缓冲 (0.5h)

### T3.3 — Dispatch 脚本 (5h)

- [ ] **T3.3.1** `aria-orchestrator/scripts/dispatch-issue.sh` 起草 (3h)
  - Pre-dispatch 检查: `nomad job status aria-runner-template | grep ISSUE_ID` 无 running alloc (per BA-M3)
  - 拷 inputs: `.aria/issues/{ID}.yaml` + 其引用的 files → `/opt/aria-inputs/{ID}/`
  - `nomad job dispatch -meta ISSUE_ID={ID}` + alloc id 记录
  - Poll alloc 状态 + tail logs (`nomad alloc logs -stderr <alloc_id>`)
- [ ] **T3.3.2** 脚本幂等性测试 (1h) — 连续两次同 ISSUE_ID dispatch, 第二次应报错拒绝
- [ ] **T3.3.3** README + 使用说明 (0.5h)
- [ ] **T3.3.4** 缓冲 (0.5h)

### T3.4 — Prompt 模板 (1h)

- [ ] **T3.4.1** `docker/aria-runner/prompts/issue-dispatch.md` 起草 (1h, per AI-I1)
  - 变量: `{{ issue_title }}`, `{{ issue_description }}`, `{{ files_listing }}`, `{{ expected_changes }}`
  - 引擎: bash `envsubst` 或 Python Jinja2 (T4 定)

**T3.DoD**: schema validator PASS on DEMO-001/002; dispatch script 幂等; prompt template 存在。

---

## T4 — Runner Entrypoint 执行链路 (20h)

### T4.1 — Entrypoint 骨架 (4h)

- [ ] **T4.1.1** `docker/aria-runner/entrypoint.sh` 重写 (M0 只做 skill load) (3h)
  - 11 步流程 (proposal §What §4 锁定):
    1. 读 `NOMAD_META_ISSUE_ID`
    2. 加载 `/opt/aria-inputs/{ID}/` (volume read-only)
    3. `git clone --depth 1` 目标 repo → `/tmp/workspace`
    4. 创建分支 `aria/{ID}`
    5. 渲染 prompt (Jinja2 或 envsubst)
    6. Bash array `CLAUDE_ARGS=(claude -p "$RENDERED" ...)` + `timeout -k 10s 600s "${CLAUDE_ARGS[@]}"`
    7. Stream-json 解析 (读 `type=result` 最后一条)
    8. NO_OP 检测 (git diff HEAD)
    9. 幂等三态 (NEW/PARTIAL/FULL + `.bak` 归档)
    10. git add/commit/push + Forgejo create PR
    11. 写 result.json (含 trap EXIT 保护)
- [ ] **T4.1.2** `trap 'write_partial_result_json' EXIT` 实现 (1h, per BA-R3-C2)

### T4.2 — Stream-json 解析器 (5h)

- [ ] **T4.2.1** 读 stdout 最后 `type=result` JSON line (2h, per AI-C4)
  - Python 或 bash + jq
  - 提取 `.total_cost_usd`, `.usage.{input_tokens, output_tokens, cache_creation_input_tokens, cache_read_input_tokens}`, `.is_error`
  - **Fallback** (per AI-R3-C1): 若无 result 帧 (timeout SIGKILL) → `claude_usage` null, `outcome=CLAUDE_TIMEOUT`
- [ ] **T4.2.2** 原始 stdout 归档到 `/opt/aria-outputs/{ID}/claude.stream.jsonl` (1h)
- [ ] **T4.2.3** 单元测试 (模拟 stream-json 输出) (1.5h)
- [ ] **T4.2.4** 缓冲 (0.5h)

### T4.3 — result.json 生成 + assertion 计算 (5h)

- [ ] **T4.3.1** schema v1.0 序列化 (2h, per proposal §What §4 result.json schema)
- [ ] **T4.3.2** assertion_results 计算 (2h, per TL-I5)
  - `file_touched_hit`: `git diff HEAD --name-only` 与 `expected_file_touched[]` 对比
  - `diff_contains_hit`: `git diff HEAD` 的 `+` 行与 `expected_diff_contains[]` 字面量子串匹配
  - `unmatched_files[]` / `unmatched_patterns[]` 记录
- [ ] **T4.3.3** SUCCESS 严格判定 (5 AND, per AD-M1-4) (0.5h)
- [ ] **T4.3.4** 缓冲 (0.5h)

### T4.4 — PR 创建 + 幂等守卫 (4h)

- [ ] **T4.4.1** Forgejo API 调用封装 (1.5h) — 使用 bot PAT, Bash + curl 或 Python requests
- [ ] **T4.4.2** 幂等三态实现 (1.5h, per BA-R2-C1)
  - `NEW`: branch 不存在 → 正常路径
  - `PARTIAL_PUSH_RECOVERY`: branch 存在 + PR 不存在 → force-push + 创建 PR
  - `FULL_RECOVERY`: branch + PR 都存在 → force-push + `.bak` 归档旧 result.json + 覆写 + 不创建 PR
- [ ] **T4.4.3** 缓冲 (1h)

### T4.5 — 单次 DEMO Dispatch Smoke (2h)

- [ ] **T4.5.1** DEMO-001 单次 dispatch 验证端到端 (1.5h) — 验证链路无断点
- [ ] **T4.5.2** 缓冲 (0.5h)

**T4.DoD**: entrypoint 11 步执行成功; stream-json 解析正确; result.json schema 合规; 幂等三态测试通过; 单次 DEMO-001 dispatch PASS。

---

## T5 — DEMO E2E Execution + Profiling (16h)

### T5.1 — DEMO-001 5 轮执行 (4h)

- [ ] **T5.1.1** 5 轮执行 + 每轮 result.json 归档 (2h)
  - 串行执行 (非并发, 避免 race condition; per QA-R1 并发可能性 = 否, 简化 M1 MVP)
  - 每轮 triage 上限 10 min (含 dispatch + alloc + claude + PR), 超时 → `outcome=CLAUDE_TIMEOUT`
- [ ] **T5.1.2** outcome distribution 统计 (1h)
  - 分母 = 5, 分子 = `outcome=SUCCESS` 计数
  - ≥ 4 (即 ≥80%) 才 passed
- [ ] **T5.1.3** p50/p95 duration + token usage 计算 (0.5h)
- [ ] **T5.1.4** 缓冲 (0.5h)

### T5.2 — DEMO-002 5 轮执行 (6h)

- [ ] **T5.2.1** 5 轮执行 (3h, DEMO-002 更复杂, 每轮预估 10-15 min)
- [ ] **T5.2.2** outcome + stats 同 T5.1.2/1.3 (1h)
- [ ] **T5.2.3** PR diff 质量人工 review + owner 签字 (1h, per AD-M0-9 solo-lab, 非独立角色)
- [ ] **T5.2.4** 缓冲 (1h)

### T5.3 — E2E 统计汇总 + 失败 triage (4h)

- [ ] **T5.3.1** 汇总 handoff.demo_executions 字段 (1.5h)
  - `e2e_demo_passed = DEMO-001.passed AND DEMO-002.passed`
- [ ] **T5.3.2** Failed runs triage (1.5h) — 按 outcome enum 分类, 记录原因 + 是否可重试
- [ ] **T5.3.3** 缓冲 (1h)

### T5.4 — Week 2 Checkpoint (2h)

- [ ] **T5.4.1** 累计工时核算 (0.5h) — 若 ≥ 60h 且 T4 未开始 → 触发 scope 重估
- [ ] **T5.4.2** 若触发: DEMO-002 降级为 optional (per AD-M1-5 + R-M1-7)
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

### T6.2 — Handoff schema v1.0 生成 (1.5h, per AD-M1-7)

- [ ] **T6.2.1** `aria-orchestrator/docs/m1-handoff.yaml` 填充 (1h)
  - go_decision / image_refs / nomad 配置 / demo_executions / legal_assumptions / performance_baseline / demo_token_usage
- [ ] **T6.2.2** Handoff validator 创建 + 验证 (0.5h)
  - `aria-orchestrator/docs/validate-m1-handoff.py` (仿 M0 validator)
  - 验证: schema v1.0 字段必填 + enum + outcome_distribution SUM == runs + e2e_demo_passed 逻辑 AND

### T6.3 — AD-M1-* 决议回写 (1h, per KM-M2 / CR-M3)

- [ ] **T6.3.1** 在 `aria-orchestrator/docs/architecture-decisions.md` 填充 AD-M1-1 ~ AD-M1-9 最终决议 (1h)

### T6.4 — Owner Signoff (1h, per AD-M0-9)

- [ ] **T6.4.1** Owner 审阅 M1 Report + handoff + legal carryover (0.5h)
- [ ] **T6.4.2** 签字 + go_decision 填充 (0.5h)
  - `Go` | `Go-with-revision` | `No-Go` | `No-Go-with-revision`
  - Deferred-with-approval (DEMO-002 降级) → 走 `No-Go-with-revision` (per AD-M1-5)

**T6.DoD**: Report 完整; handoff validator PASS (final); ADRs 回写; owner signoff 完成。

---

## Buffer (20h)

全局备用, 分配规则:
- T1+T4 Spike 超工时 → 最多 +10h
- T5 DEMO 重跑 triage → 最多 +5h
- T6 handoff 迭代 → 最多 +5h
- R-M1-7 Week 2 checkpoint 触发: 不消耗 buffer, 走 AD-M1-5 降级规则

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
- **T4 Runner entrypoint**: ai-engineer (claude CLI 层) + backend-architect (git / PR / 幂等守卫) 紧密配合
- **T6.2 Handoff validator**: backend-architect (schema 实现) + knowledge-manager (字段 traceability 审查)

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
- [PRD v2.1 §M1](../../../docs/requirements/prd-aria-v2.md)

---

**最后更新**: 2026-04-17 (Phase A.2 task decomposition post convergence audit Round 6 PASS)
**维护**: Phase B.2 执行阶段 updates 标记完成度

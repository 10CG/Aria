# aria-2.0-m1-mvp — Aria 2.0 M1 MVP 手动 E2E dispatch

> **Level**: Full (Level 3 Spec)
> **Status**: Complete
> **Created**: 2026-04-17
> **Completed**: 2026-04-23 (go_decision=Go-with-revision, e2e_demo_passed=true, 85/85 tasks)
> **Parent Story**: [US-021](../../../docs/requirements/user-stories/US-021.md)
> **Target Version**: v2.0.0-m1
> **Source**: [PRD v2.1 §M1 (lines 444-465)](../../../docs/requirements/prd-aria-v2.md), [M0 Report §6 M1 精确路径](../../../aria-orchestrator/docs/m0-report.md), [M0 handoff.yaml schema final](../../../aria-orchestrator/docs/m0-handoff.yaml)

> **Legal carryover notice (Round 1 audit LA-C1)**: AD-M1-6 决定从 Luxeno (silknode 自有代理) 改走 Anthropic 官方 API, 使 M0 Legal Memo IS-4 "内部 API 透传无出境存储" 结论**不再适用**。M1 引入真实跨境 API 调用, 需在 T1 前完成独立 legal carryover 审视 (见 §交付物 §7)。

## Why

M0 (US-020, done 2026-04-17) 已把 5 项核心假设验证并固化 blueprint: A1 headless plugin ✅, A3 virtiofs storage ✅, R7 Nomad meta 128 KiB ✅, AD3 Option C Extension-only ✅, R8 virtiofs override ✅. 但 blueprint 仍是 "单机 docker run + 手动验证" 级别, 未证明:

1. **registry push 链路**: M0 Dockerfile 仅本地 build (local `aria-runner:claude-m0`), 未推送到 Forgejo container registry; cross-node dispatch 要求镜像对所有 heavy 节点可拉取。
2. **Nomad parameterized dispatch 在生产节点 E2E**: M0 T2.2 只验证 dispatch 机制本身 (meta 边界、volume mount), 未验证 "真跑 aria-runner 镜像 + 真写 PR"。
3. **Forgejo PR 回写闭环**: M0 Dockerfile 测试只到 "skill 加载成功", 未验证 claude-code 在 Nomad alloc 内实际产出 commit + push + PR。

若这三项在 M2 Hermes 集成时才暴露失败, Layer 1 工时估算 (140h) 会被连带污染, 决策点后移 2 个月, velocity cost 不可接受 (per [M0 Report §0.3 velocity cosign rationale](../../../aria-orchestrator/docs/m0-report.md) — ×3.76 加速为 M0 特例不可迁移)。

M1 的定位 = **把 blueprint 从 "spike 可跑" 升级到 "production-ish, 手动触发"**, 与 M2 Layer 1 状态机集成 (US-022) 解耦:
- M1 证明 Layer 2 容器 + registry + Nomad 路径可工作
- M2 可以在稳定的 Layer 2 上集成 Hermes, 失败原因归因明确

## What

### 交付物

1. **生产镜像链路**
   - `aria-runner:claude-<sha>` + `aria-runner:claude-latest` 双 tag 推送到 `forgejo.10cg.pub/10CG/aria-runner`
   - 镜像 SHA256 + registry URL 记录到 `m1-handoff.yaml`
   - Registry push 流程文档 (`.env.local` 模式, 不入 git)
   - Dockerfile 构建时门控 (`DEPLOY_ENV=internal`) 保留并验证

2. **Nomad 生产配置**
   - `nomad/jobs/aria-runner-template.hcl` (parameterized, meta=ISSUE_ID)
     - **env 明确声明** (per AD-M1-6): `unset ANTHROPIC_BASE_URL` + 不继承 M0 `smart-opus` alias
     - `--model` 使用官方 model id (e.g., `claude-opus-4-5`), 禁用 Luxeno alias (smart-opus/smart-sonnet/smart-haiku)
     - `tmpfs` 显式大小上限 (`/tmp:size=1024m`, `/root:size=512m`, per BA-R2-C2 升级 — 考虑 DEMO-002 fixture clone + claude stream-json verbose buffer; T4 spike 实测 p95 × 1.3 作调整基线)
   - `nomad/client-config/host-volume.hcl` (三个 heavy 节点)
     - `aria-runner-outputs` → `/opt/aether-volumes/aria-runner/outputs` (M0 已验证)
     - `aria-runner-inputs` → `/opt/aether-volumes/aria-runner/inputs` (**新增, M0 未覆盖**)
     - **T2 门控**: 三节点 inputs volume 声明 + mount 验证 (`nomad node status -verbose` + smoke dispatch) 必须先于 T3 完成
   - `nomad/README.md` (deployment 步骤 + 排错手册)
   - `resources` stanza (初始保守上限: CPU 2000 MHz / memory 2048 MiB / disk 4096 MiB; DEMO profiling 后以实测 p95 为基线做减法)
     - **运维注释 (per BA-R3-I1)**: `disk=4096m` 计 alloc dir 宿主机磁盘预留 (非 tmpfs); tmpfs 配额独立由 tmpfs size= 参数控制 (见 `/tmp:size=1024m` `/root:size=512m`); 两者不可混算

3. **Issue 输入协议 v0.1** (显式标记 breaking change 可接受)
   - **Escape hatch 说明** (per KM-M1 / KM-R2-1):
     - Breaking change 触发条件: M2 T3 (`aria-2.0-m2-*` Spec) 起草时 Hermes 接入需要调整 schema
     - 变更主体: M2 OpenSpec (非 M1)
     - v0.1 与 handoff schema 的治理边界:
       - `issue-schema-v0.1.md` 字段独立豁免 (v0.1 → v1.0 可 breaking)
       - `m1-handoff.yaml` 字段遵 AD-M1-7 additive-only (不 breaking)
       - 两个 schema 不重叠, 互不干扰
   - `openspec/changes/aria-2.0-m1-mvp/artifacts/issue-schema-v0.1.md` — YAML schema 定义
     - 字段: `id`, `title`, `description`, `files[]`, `expected_changes`
     - **早锁字段 (per BA-R2-I1 + AD-M1-3 提前锁定)**: `expected_file_touched[]` + `expected_diff_contains[]` (字面量子串匹配, 不是正则, per QA-C1-PARTIAL); **匹配范围 (per QA-N1)**: v0.1 **仅验证增量 `+` 行** (不覆盖删除语义); 若 DEMO 需验证删除操作, 延后到 schema v1.0 (M2 扩展); 本 v0.1 的 DEMO-001 (README 修改一行 = 改) / DEMO-002 (新增 function+test = 纯增量) 均纯增量, 不受此限制影响
     - **Action verb validator (per QA F4 post_planning R1)**: issue schema v0.1 validator 必须检查 `description` 含 "新增" / "修改" / "删除" 动词 + 具体文件/函数名 (降低 claude `CLAUDE_NO_OP` 概率, 与 §What §4 step 8 git diff 检测形成 defense in depth)
     - **`ip_classification`** (必填, enum: `synthetic` | `trivial-real` | `real`): DEMO-001/002 必须为 `synthetic`, 继承 M0 T3.5 合成 fixture 模式 (per LA-I1); M1 仅允许 `synthetic`, 其他值在 M2+ 解禁前需显式治理流程 (见 AD-M1-9)
   - `.aria/issues/DEMO-001.yaml` — reference DEMO (synthetic)
   - `aria-orchestrator/scripts/dispatch-issue.sh` — 手动 dispatch 脚本 (幂等, bash)
     - Pre-dispatch 检查: `nomad job status` 确认无同 ISSUE_ID running alloc (单 issue 单 alloc 约束, per BA-M3)
     - 拷 inputs: `.aria/issues/{ID}.yaml` + 其引用的 files → `/opt/aria-inputs/{ID}/`
     - 调 `nomad job dispatch -meta ISSUE_ID={ID}`
     - Poll alloc 状态 + tail logs

4. **Runner entrypoint 执行链路**
   - `docker/aria-runner/entrypoint.sh` 升级 (M0 版本只做 skill load 测试, M1 做完整 dispatch → PR)
   - `docker/aria-runner/prompts/issue-dispatch.md` — prompt 模板 (Jinja2 或 bash envsubst, 仿 M0 `ab-suite/glm-smoke/templates/` 模式, per AI-I1)
     - 变量: `{{ issue_title }}`, `{{ issue_description }}`, `{{ files_listing }}`, `{{ expected_changes }}`
     - handoff 记 `prompt_template_sha256` 供回放
   - 流程:
     1. 读 `NOMAD_META_ISSUE_ID`
     2. 从 `/opt/aria-inputs/{ID}/` 加载 issue.yaml + files (volume 挂载 read-only, per AI-M1)
     3. `git clone --depth 1` 目标 repo 到 `/tmp/workspace`
     4. 创建分支 `aria/{ID}`
     5. 渲染 claude prompt (由上述模板, **非 inline 拼接**; 渲染后得到 final string)
     6. **Prompt 传入方式 (per AI-C3 + AI-R3-C1 + AI-R3-C2)**:
        ```bash
        # Bash array 形式, 禁 eval / 字符串拼接 (防 shell injection, per AI-R3-C2)
        CLAUDE_ARGS=(claude -p "$RENDERED_PROMPT"
                     --permission-mode bypassPermissions
                     --model "$ARIA_MODEL"
                     --output-format stream-json --verbose
                     --settings "$ARIA_SETTINGS_JSON")
        # timeout 加 -k grace (10s SIGTERM → SIGKILL), 让 claude 有机会 flush stream-json 末帧
        timeout -k 10s "$CLAUDE_TIMEOUT_S" "${CLAUDE_ARGS[@]}"
        ```
        - **一次性 user turn**, 位置参数, **不使用 stdin / --append-system-prompt**
        - `${ARIA_MODEL}` 默认来源 = Dockerfile ENV 声明, 默认值 `claude-opus-4-5-20250929` (snapshot id, 非 alias, per AI-R3-M2 保证 5 轮 reproducibility); Nomad env 可覆盖但 M1 DEMO 不覆盖
        - `${CLAUDE_TIMEOUT_S}` 默认 600s (T4 spike 后可按实测 p95 × 1.5 调整, per QA-N2); 超时写 `outcome=CLAUDE_TIMEOUT`, per QA-R3
     7. **Stream-json 解析 (per AI-C4 + AI-R3-C1)**:
        - 正常路径: runner 读 stdout 最后一条 `type=="result"` 的 JSON line, 取 `.total_cost_usd`、`.usage`、`.is_error` 填 result.json
        - **Fallback (per AI-R3-C1)**: 若无 `type=result` 帧 (超时 SIGKILL 或进程崩溃导致 stream 被截断) → `claude_usage` 字段填 null (对应 cost_usd_reported, input_tokens 等均 null), `outcome=CLAUDE_TIMEOUT`; 不 block result.json 写入, 仅记原始 stream 供 debug
        - 原始 stdout 存档到 `/opt/aria-outputs/{ID}/claude.stream.jsonl` 供 debug
     8. **NO_OP 检测 (per QA-R2)**: claude 退出后 entrypoint 显式 `git diff HEAD` + check new commits; 若 diff 空 + 无新 commit → `outcome=CLAUDE_NO_OP` (不依赖 claude self-report)
     9. **幂等性守卫 (per BA-I3 + BA-R2-C1 三态判定 + BA-R3-C1)**:
        - `NEW`: branch `aria/{ID}` 不存在
        - `PARTIAL_PUSH_RECOVERY`: branch 已存在但 PR 不存在 → force-push + 跳过创建 branch, 创建 PR
        - `FULL_RECOVERY`: branch 已存在且 PR 已存在 → force-push + 跳过创建 PR + **归档旧 result.json** (覆写前 `mv result.json result.json.$(date +%s).bak`, 保留同目录, per BA-R3-C1 防 debug 历史丢失), 然后覆写 result.json
     10. git add/commit → push origin → Forgejo create PR (若 AD-M1-4 分类为可重试错误, 记 retry_count)
     11. 写 `/opt/aria-outputs/{ID}/result.json` (schema 见下); **crash 保护 (per BA-R3-C2)**: entrypoint 启动时即 `trap 'write_partial_result_json' EXIT` — 若 entrypoint 在步骤 10-11 间崩溃 (OOM/SIGKILL), trap handler 保证至少写出 `outcome=INFRA_FAILURE` + `error.type="crashed_before_result_write"` + 已知字段 (pr_url 如有, commit_sha 如有); 步骤 11 完成后原子 rename 替换临时快照
   - **result.json schema v1.0** (per AI-C1 + QA-I1 + TL-I5 + AI-I5 + AI-I6 + QA-R3):
     ```yaml
     schema_version: "1.0"
     issue_id: string
     pr_url: string | null
     commit_sha: string | null
     claude_exit_code: int
     claude_duration_s: float
     claude_usage:                     # 源自 stream-json result 帧, 不自算 (per AI-I5); 字段名 1:1 映射 Anthropic API result frame (per AI-R3-I1)
       input_tokens: int
       output_tokens: int
       cache_creation_input_tokens: int   # per AI-R3-I1 对齐 Anthropic API
       cache_read_input_tokens: int       # per AI-R3-I1 对齐 Anthropic API (原 cache_read_tokens 错名)
       cost_usd_reported: float           # = result 帧 .total_cost_usd (Anthropic 官方计量)
       source: "claude-cli-result-frame"
     prompt_template_sha256: string    # pre-render 源文件 bytes (per AI-I6)
     rendered_prompt_sha256: string    # post-render final string bytes (per AI-I6, 审计回溯用)
     idempotency_state: NEW | PARTIAL_PUSH_RECOVERY | FULL_RECOVERY
     assertion_results:                # per TL-I5 + QA-C1-PARTIAL + TL-R3-2 对称性
       file_touched_hit: bool
       diff_contains_hit: bool
       unmatched_files: [...]          # 未命中的 expected_file_touched 列表 (对称 unmatched_patterns, per TL-R3-2)
       unmatched_patterns: [...]       # 未命中的 expected_diff_contains 列表
     outcome: SUCCESS | INFRA_FAILURE | CLAUDE_TIMEOUT | CLAUDE_REFUSAL | CLAUDE_NO_OP | GIT_STAGE_FAILURE | PR_CREATE_FAILURE | ASSERTION_MISMATCH | IDEMPOTENCY_CONFLICT
     error:
       type: string | null             # 对应 outcome 的细分类
       detail: string | null
     ```
   - **AD-M1-4 失败分类 (provisional, Spec 层锁定, per QA-I1 / AI-I2 / QA-R3 / TL-I5)**:
     - `SUCCESS` 的严格定义: `claude_exit_code == 0` AND `commit_sha != null` AND `pr_url != null` AND `assertion_results.file_touched_hit == true` AND `assertion_results.diff_contains_hit == true` (三项都 true 才计 SUCCESS, 否则按其他 outcome 分类)
     - `success_rate` 分母仅对 `outcome=SUCCESS` 计数
     - `CLAUDE_NO_OP` (claude 判定 "无需改动" — 以 `git diff HEAD` 空 + 无新 commit 为机械判定, 不依赖 claude self-report) 视为失败, MVP 不接受
     - `CLAUDE_TIMEOUT` (进程 timeout 或 API 超时) 独立 enum, 不归入 INFRA_FAILURE (per QA-R3)
     - `ASSERTION_MISMATCH` 新增: claude exit=0 + PR 创建成功但 assertion 不命中 → 视为失败 (per TL-I5)
     - `GIT_STAGE_FAILURE` 语义 (per BA-R2-M1): `claude_exit_code == 0` AND working tree 有变更 AND git add/commit/push 失败 (区别于 CLAUDE_NO_OP)
     - T4 可**追加**分类, 不允许重归类 `CLAUDE_REFUSAL / NO_OP / TIMEOUT / ASSERTION_MISMATCH` 为 success

5. **DEMO E2E 执行 + M1 Report**
   - **DEMO-001** (synthetic trivial): "管道连通" 验证 — 改 synthetic repo 的一行 README; 成功仅证明基础设施可运行, 不计入"质量"维度 (per QA-M1)
   - **DEMO-002** (synthetic non-trivial): "质量门控" — 在 synthetic fixture repo (专用 fixture, 继承 M0 T3.5 模式) 中新增 1 个 function + 对应 test
     - AD-M1-5 决: fixture repo = `aria-plugin-benchmarks/ab-suite/m1-mvp/fixtures/` 下新建 (per QA-I2, Spec 层锁定 repo 类型 = 自建 synthetic)
   - **执行样本**: 每个 DEMO 独立 **5 轮** (per QA-C2, 不是 3 轮, 样本量提升以区分偶发 vs 系统性失败)
   - 统计量: per-DEMO 独立 `success_rate` (分母 = 5, 分子 = `outcome=SUCCESS` 计数), duration p50/p95, token usage p50/p95
   - `aria-orchestrator/docs/m1-report.md` — 简化版 M0 Report 结构
   - `aria-orchestrator/docs/m1-handoff.yaml` — schema v1.0 (字段见下)

6. **M1 handoff schema v1.0** (per BA-I4 / AI-I3 / LA-I3 / TL-I1)

   > **Schema evolution rule (per TL-I1)**: v1.0 仅允许 **additive** 字段变更 (M1 运行期可新增 optional 字段, 不可删除/重命名); 任何破坏性变更触发 M2 scope 重估。

   ```yaml
   schema_version: "1.0"

   # —— Go/No-Go 与 PR 契约 (per TL-R3-3 enum 扩展) ——
   go_decision: Go | Go-with-revision | No-Go | No-Go-with-revision
   # Go-with-revision = M1 产出有效 + 对 PRD / M2 scope 做调整 (触发 PRD patch PR)
   # No-Go-with-revision = DEMO-002 deferred-with-approval 等降级场景走此分支 (per AD-M1-5)

   # —— 镜像与 Registry (per TL-R3-4 结构化 mutable/immutable) ——
   registry_url: "forgejo.10cg.pub/10CG/aria-runner"
   image_refs:
     immutable_sha: "sha256:..."             # content-addressed, M2 生产引用必须用此
     mutable_tag: "claude-latest"            # M2 开发期可被覆盖, 禁引用为 Nomad job image
     production_pin: "image_sha256"          # M2 pin 规则: 用 immutable_sha 而非 mutable_tag
   image_tags: ["claude-<sha>", "claude-latest"]  # 保留数组供 registry 查询, 但消费方以 image_refs 为准

   # —— Nomad 配置 ——
   nomad_job_id: "aria-runner"
   nomad_job_version: int             # 实际部署的 job version (per BA-I4, M2 diff 对比用)
   host_volumes:
     outputs: "/opt/aether-volumes/aria-runner/outputs"
     inputs:  "/opt/aether-volumes/aria-runner/inputs"

   # —— T4 启动信号 (per QA F3 + post_planning R1) ——
   t4_started: bool                    # runner 执行 T4.1.1 第一个 checkbox 时置 true, 供 Week 2 checkpoint 机械检测

   # —— E2E 验收 ——
   e2e_demo_passed: true | false      # = DEMO-001.passed AND DEMO-002.passed (严格 AND, per QA-C2)
                                      # US-022 启动硬门控
   demo_executions:
     DEMO-001:
       classification: synthetic       # 强制 synthetic per LA-I1
       runs: 5
       success_rate: 0.80              # (outcome=SUCCESS 计数) / runs, per QA-N4 (per-DEMO 独立 ≥ 0.80 才 passed)
       passed: true | false
       p50_duration_s: float
       p95_duration_s: float
       outcome_distribution:           # 每个 outcome 分类的计数 (镜像 result.json.outcome enum, per QA-N3)
         SUCCESS: int
         INFRA_FAILURE: int
         CLAUDE_TIMEOUT: int           # per QA-R3 / QA-N3
         CLAUDE_REFUSAL: int
         CLAUDE_NO_OP: int
         GIT_STAGE_FAILURE: int
         PR_CREATE_FAILURE: int
         ASSERTION_MISMATCH: int       # per TL-I5 / QA-N3
         IDEMPOTENCY_CONFLICT: int     # per BA-R2-T4.4.2-409 (force-with-lease 409)
       # 约束: SUM(outcome_distribution 所有 enum 计数) == runs
       pr_urls: [...]
     DEMO-002: { ... 同结构 ... }

   # —— 成本基线 (per AI-I3) ——
   demo_token_usage:
     DEMO-001:
       p50_input_tokens: int
       p50_output_tokens: int
       p50_cache_read_tokens: int
       p50_cost_usd_estimate: float
     DEMO-002: { ... }
   total_cost_usd_estimate: float      # M1 全部 DEMO + dev 调试累计估算

   # —— Performance baseline (per QA-M2) ——
   performance_baseline:                # 供 US-022 non-regression 引用
     demo_002_p50_duration_s: float     # M2 集成后 ≤ baseline × 1.5 否则告警

   # —— Legal assumptions (per LA-I3) ——
   legal_assumptions:
     anthropic_api_terms_verified: true | false   # T1 legal carryover 产出 (见 §7)
     anthropic_api_data_retention: "..."          # ToS §7-8 摘要
     ip_classification_enforced: true             # 所有 DEMO inputs 均 synthetic
     r9_glm_legacy_status: pending | resolved     # 继承 M0 handoff, 不重置
     forgejo_registry_access_audited: true | false
     aether_node_ownership_verified: true | false # R10 检查
     legal_carryover_memo: "aria-orchestrator/docs/m1-legal-carryover.md"

   # —— 问题跟踪 ——
   open_issues: []                    # blocker list
   report_version: "v1.0"
   ```

### 架构决策 (AD-M1-*)

> **决议回写**: AD-M1-* 最终决定落地到 `aria-orchestrator/docs/architecture-decisions.md` (与 AD-M0-* 同文件, 延续编号体系), 由 T6 Report 阶段统一回填 (per KM-M2 / CR-M3)。

| ID | 决策议题 | 状态 |
|----|---------|------|
| **AD-M1-1** | Registry auth 策略 (bot account token vs maintainer PAT) | 待 T1 Spike 决; Spike 失败回退 = nomad artifact + docker load (额外 ~8h, per BA-M1); **Bot token lifecycle (per LA-NEW-1 + LA-R3-1)**: 本 Spec 锁 "Nomad secret 注入 (非 env 硬编码), **60 天 rotation** (NIST SP 800-63B / RFC 8252 基线, 非 90 天), leak 触发 revoke + new PAT"; 具体 account 边界 (per-DEMO 隔离 vs infra-wide) 由 T1 Spike 定; **T1 交付物扩展 (per LA-R3-3 additional_concerns)**: (a) Secret store 选型报告 (AWS SM / Vault / Nomad native); (b) Rotation 自动化草案 (design only, M1 不实装); (c) M0→M1 transition audit (Luxeno 日志含 M0 测试数据检查 + 清理请求记录) |
| **AD-M1-2** | 镜像 tag 策略 | 待 T1 定; **mutable 指针约定 (per TL-M4)**: `claude-latest` = mutable (M2 开发期可被覆盖); `claude-<sha>` = immutable; M2 生产部署**必须 pin `image_sha256`**, 不直接引用 `claude-latest` |
| **AD-M1-3** | Issue schema v0.1 字段边界 | **本 Spec 早锁**: (a) `ip_classification` 必填, DEMO 必 synthetic; (b) `expected_file_touched[]` + `expected_diff_contains[]` 必填 (per BA-R2-I1, Acceptance Gate 硬依赖); 其他字段 T3 可调整, v0.1 breaking change 见 §What §3 escape hatch |
| **AD-M1-4** | Runner 错误分类 (outcome enum) | **本 Spec 锁定 provisional 基线** (见 §What §4 result.json schema, 含 SUCCESS 严格定义 / TIMEOUT / ASSERTION_MISMATCH 独立 enum); T4 可**追加**分类不可重归类 |
| **AD-M1-5** | DEMO 选型 | **本 Spec 锁**: DEMO-001 synthetic trivial (管道验证, 不计质量维度) + DEMO-002 synthetic non-trivial (fixture repo `aria-plugin-benchmarks/ab-suite/m1-mvp/fixtures/`, 计质量维度); 各 5 轮独立 ≥80% 才 passed; **Week 2 降级规则 (per TL-M3)**: R-M1-7 触发 DEMO-002 降级时, `e2e_demo_passed = DEMO-001.passed AND (DEMO-002.status ∈ {passed, deferred-with-approval})`, deferred 需 owner 书面签字 + 写 `handoff.open_issues` + 自动走 No-Go-with-revision 分支 (非 Go) |
| **AD-M1-6** | LLM 调用栈配置 | **本 Spec 决**: 官方 Anthropic API `https://api.anthropic.com` (M0 T3.4 Luxeno 40% timeout 不迁移, Luxeno 延后 M2+); entrypoint 必须 `unset ANTHROPIC_BASE_URL` + 用官方 model id (禁 `smart-opus` 等 Luxeno alias); `ARIA_MODEL` 默认值在 Dockerfile ENV 声明 (per AI-I4), **默认字面量 (per AI-R3-M2) = `claude-opus-4-5-20250929`** (snapshot id 非 `-latest` alias, 保证 5 轮 reproducibility); Nomad env 可覆盖但 M1 DEMO 不覆盖; **`settings.json` v1.0 最小字段清单 (per AI-M2 + AI-R3-M1)**: `{ "permissions": {"allow": ["Bash", "Edit", "Read", "Write", "Grep", "Glob"]}, "env": {}, "model": "${ARIA_MODEL}", "maxOutputTokens": int }` — bypassPermissions 仍生效, allow 列表作为审计基线; 禁用项 (alwaysThinkingEnabled 等 Luxeno-specific) 必须显式列出, sha256 记入 handoff |
| **AD-M1-7** | M1 M2 接口契约 | **本 Spec 锁 handoff schema v1.0 字段**; T6 可追加 optional 字段, 不允许删除/重命名; 破坏性变更触发 M2 scope 重估; **Post-final additive 窗口 (per TL-I4 + TL-R3-1)**: handoff Go 签字后, 仅允许 additive 字段在 "`min(M2 T1 完成日期, M2 kickoff + 4 周)`" 之前追加 (非固定 2 周); 允许 owner 一次性延长 +2 周 (记 `schema_amendments[].extension_reason`); 超窗追加字段走 M2 Spec 的 AD-M2-1 重决议, 不再是 M1 amendment; 每次追加需 owner 二次签字 |
| **AD-M1-8** | Forgejo registry 访问控制 | **本 Spec 锁**: registry 必须 private-only, pulling 需 auth token, 无 anonymous 访问; T1 交付 access audit 报告 (per LA-I4) |
| **AD-M1-9** | `ip_classification` 跨 milestone 治理 (per LA-NEW-5 + LA-R3-2) | **本 Spec 锁**: M1 locks `ip_classification=synthetic`; M2+ 启用 `trivial-real` / `real` 需**"外部 legal counsel" review + 显式 PRD scope 修订 (new AD-M2-X 决议) 在 T* 实现前完成**; 未经此治理流程不得放开。**Solo-lab 语义澄清 (per AD-M0-9 + LA-R3-2)**: "external counsel" 三种解读 — (a) 第三方律所 (有明确成本/时间影响); (b) owner-in-external-role (角色切换非身份切换); (c) 延后到 M3+ 风险接受; owner 在 M2 kickoff 前必须在 `handoff.open_issues` 书面记录选择路径 + rationale, 未记录 = 自动 escalate No-Go-with-revision |

7. **Legal carryover (per LA-C1 / LA-I2 / LA-I3 / LA-I4 / LA-NEW-3, T1 交付)**
   - `aria-orchestrator/docs/m1-legal-carryover.md` — M0 Legal Memo v1.1 针对 M1 AD-M1-6 pivot 的增量审视
   - **产出格式 (per LA-NEW-3)**: signed memo + clause-by-clause mapping table, 必填列: `clause#` / `clause_text` / `M1_applicability` (yes/no) / `review_date` / `reviewer_role`; 模板参照 M0 `standards/legal/scoped-memo-template.md` 延续 (T1 可加行)
   - **审视范围 (checklist)**:
     - **IS-4 失效检查**: M0 结论 "silknode 内部透传无出境存储" 不再适用 M1 官方 Anthropic API 路径
     - **Anthropic ToS §7-8 逐条审视**: prompt retention duration / training data usage optionality / processing jurisdiction; 输出 mapping table
     - **数据分类审查**: M1 DEMO 全部 synthetic 已满足 "无 10CG IP 出境" 原则 (继承 M0 T3.5 合成 fixture 模式)
     - **R10 Aether 节点归属复查**: M0 IS-6 结论 "10CG 自有" 在 M1 执行期间的持续性
     - **R9 GLM ToS legacy status** (per LA-NEW-4): `pending` = M0 未解决且延续到 M1 (MVP Layer 2 单路径不触发 GLM 决策, 状态保留); `resolved` = M1 期间 GLM 官方回应到位 (与 M1 MVP 无关, 仅影响 M2+ Luxeno 决策); M1 Layer 2 单路径本身不消费该字段, 仅作 audit trail
     - **Forgejo registry access audit**: private-only + auth required + 无 anonymous pull (per LA-I4 / AD-M1-8)
     - **End-user consent debt (per LA-NEW-2)**: M1 DEMO 全 synthetic 无外部 IP → 不触发 customer disclosure; 但记入 `handoff.open_issues` 作为 M2+ reminder: "若 M2+ 消费 real IP → trigger external counsel review + ToS/Privacy Policy 更新 + customer disclosure"
   - Sign-off: per AD-M0-9 (solo-lab role merging), owner 承担签字主体
   - **机械 Gate (per BA-R2-I2)**: Acceptance Gate §3 验证方式 = "`m1-legal-carryover.md` 文件存在 + 最后一行含 owner 签字标记 (e.g., `Signed-by: human:simonfish @ YYYY-MM-DD`)" + `handoff.yaml.legal_assumptions.anthropic_api_terms_verified = true`, 两条件 AND

### 非目标 (Out of Scope)

> **单向引用 (per CR-I4)**: 详细清单见 [US-021.md §不在范围](../../../docs/requirements/user-stories/US-021.md), Spec 层不重复枚举 (避免双份维护漂移)。

本 Spec 层特别强调:
- **Layer 1 状态机 / Hermes Extension / SQLite / cron 自动触发** → US-022 (M2, ~140h)
- **双 provider 切换 / Luxeno 接入** → US-022+ (归属 M2 vs M3 待 AD-M2-* 定, per TL-I3)
- **real / trivial-real IP DEMO** → AD-M1-9 治理流程解禁前禁用

## Impact

### 直接影响

- **US-022 (M2 Layer 1 状态机)** 启动硬门控 = `m1-handoff.yaml.e2e_demo_passed == true`
- **velocity 基线建立**: M1 是第一次 "production-ish" 实施, 实际工时 vs PRD 100h 估算的差值作为 M2+ 估算校准依据 (M0 ×3.76 为 Spike 特例不作基线)
- **Layer 2 v1.0 镜像契约固化**: registry URL + tag 策略 + entrypoint 协议 成为后续所有 Layer 2 变更的向后兼容基线

### 间接影响

- **Forgejo container registry** 首次生产使用 → registry 运维 (镜像清理 / quota / 备份) 需 M3+ 增强
- **Nomad host volume** 从 M0 Spike 路径升级到生产配置, 运维 runbook 更新 (运维/M1 责任, 不在本 Spec, 但要记录到 m1-report.md 附录)
- **Anthropic API 消耗**: 首次长期 API 调用 (DEMO 执行 6 次 + 开发测试 ~20 次), 监控 budget

### Release Coupling

- 本 Spec 与 `aria-2.0-silknode-integration-contract` (Draft 预留 Spec) **不直接 coupling**: silknode 是 Luxeno 接入契约, M1 不走 Luxeno
  - **隐式时间窗 coupling (per TL-I3)**: AD-M1-6 把 Luxeno 接入延后到 M2+; 具体归属 (M2 vs M3) 待 M1 handoff 后由 AD-M2-* 决定, 不默认绑 M2 scope (避免 M2 Layer 1 140h + Luxeno 接入 scope 膨胀)
- 本 Spec 与 `state-scanner-mechanical-enforcement` (Draft) **不 coupling**: 该 Spec 等 L1 探针数据激活, 与 M1 MVP 并行

## Acceptance Gate (M1 Exit Criteria)

四项可检查物 (对齐 M0 Exit 结构):

1. **E2E demo per-DEMO 独立 pass** (per TL-C1 / QA-C1 / QA-C2):
   - DEMO-001 (synthetic trivial, 管道维度): 5 轮独立执行, `outcome=SUCCESS` 计数 ≥ 4 (即 ≥ 80%)
   - DEMO-002 (synthetic non-trivial, 质量维度): 5 轮独立执行, `outcome=SUCCESS` 计数 ≥ 4 (即 ≥ 80%)
   - **两者均独立达标才 `e2e_demo_passed=true`** (AND 语义, 非合并计算)
   - `outcome` 计数排除 `CLAUDE_NO_OP` (视为失败, MVP 不接受 claude 自判 "无需改动")
   - **机械 assertion**: 每个 DEMO 的 `expected_file_touched[]` + `expected_diff_contains[]` 必须在 PR diff 中命中 (不允许主观人工判断 pass)
   - diff 合理性由 owner 按 AD-M0-9 签字 (不引入新评审角色, per TL-M2)

2. **M1 handoff validator PASS (final)**: `e2e_demo_passed: true` + 所有必填字段回填, schema v1.0 全部 additive-only 通过

3. **Legal carryover signoff** (per LA-C1): `legal_assumptions.anthropic_api_terms_verified: true` + `m1-legal-carryover.md` owner 签字

4. **产品负责人签字确认 Go/No-Go** (per AD-M0-9 solo-lab role merging, owner 承担签字主体)

## 风险

> **详细风险登记**: 见 [US-021.md §风险与缓解](../../../docs/requirements/user-stories/US-021.md) (R-M1-1 ~ R-M1-8, 单向引用避免漂移, per CR-M6 / CR-M4)

本 Spec 层特别关注的 3 项:

| 风险 | 缓解 |
|------|------|
| T1+T4 spike 失败触发工时预警 | Week 2 checkpoint: 若累计工时 ≥ 60h 且 T4 未开始 → 触发 scope 重估 (DEMO-002 降级为 optional), 写入 handoff.open_issues (per QA-I3) |
| 工时估算 Low 估 (首次 production-ish) | R-M1-7 Low → Medium; T1+T4 spike 完成后做 reforecast, 剩余估算 > 残余 buffer × 1.5 触发裁剪 (per TL-I2) |
| 跨境 API 合规假设未验证 | T1 legal carryover 先于 T3/T4 交付, `anthropic_api_terms_verified=false` 则 block Go decision (per LA-C1) |

## 收敛后状态

| 状态 | 动作 |
|------|------|
| **Go** | US-022 task-planner 启动 (Layer 1 状态机 + Hermes Option C Extension, M2 ~140h) |
| **Go-with-revision** | 本 Spec 产出有效, 但需要对 PRD / M2 scope 做调整 (例如 issue schema 需大改) → 起草 PRD patch PR |
| **No-Go** | blocker 分类: (a) 技术不可行 → 触发 PRD AD3 二次评估是否保留 Option C; (b) 工时显著超估 → 触发 v2.0 整体 timeline 重估 |

## 关联文档

- [PRD v2.1](../../../docs/requirements/prd-aria-v2.md) §M1 + §关联文档
- [M0 Report §6 M1 精确路径](../../../aria-orchestrator/docs/m0-report.md)
- [M0 handoff.yaml schema final](../../../aria-orchestrator/docs/m0-handoff.yaml)
- [US-020 (M0 done)](../../../docs/requirements/user-stories/US-020.md)
- [US-022 预期 scope (M0 Report §6.4)](../../../aria-orchestrator/docs/m0-report.md)
- [aria-2.0-silknode-integration-contract (Draft, 预留)](../aria-2.0-silknode-integration-contract/proposal.md)

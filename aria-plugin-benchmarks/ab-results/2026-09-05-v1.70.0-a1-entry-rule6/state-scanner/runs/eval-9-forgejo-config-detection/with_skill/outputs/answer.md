已跑完 Step 0 机械扫描 (`scan.py`, **exit 0 / `errors: []`**, snapshot schema 1.0)，下面是完整状态报告 + 你问的两件事的答案。

**直接结论**: 只有 **1 个真正的配置缺口** —— 就是你说的 `CLAUDE.local.md`；另有 1 个次级缺口 (UPM 未配置) 和 1 个配置取值问题 (issue 扫描 `limit` 截断)。其余配置面全部就位。

```
╔══════════════════════════════════════════════════════════════╗
║                    PROJECT STATE ANALYSIS                     ║
╚══════════════════════════════════════════════════════════════╝
```

## 📍 当前状态

- 分支: `feature/a1-entry-claim-duplicate-work-guard` (upstream `origin/同名`, ahead 0 / behind 0)
- 模块: — (UPM 未配置, 无 active module)
- Phase/Cycle: — (UPM 未配置; 活跃轨道进度见下方 handoff 段: 31/40)
- 变更: 4 项 — 3 个 dirty 子模块 (`aria` / `aria-orchestrator` / `standards`) + 1 个未跟踪目录 (`aria-plugin-benchmarks/ab-results/2026-09-05-v1.70.0-a1-entry-rule6/`)；暂存区空
- 关联 OpenSpec: `a1-entry-claim-duplicate-work-guard` (approved)
- 上次 handoff: `2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md` (0.8h ago, via **pointer**)
- git 中间态: 无 (`operation: none`, 无冲突)；中断状态: 上一条 workflow-state 为 `completed` (2026-09-02 收尾), 无需 Resume

## 📊 变更分析

- 类型: 子模块指针 + 未跟踪评测产物 (code 0 / test 0 / docs 0 / config 0 / other 4)
- 复杂度: **Level 2**
- 架构影响: 无
- 测试覆盖: 无对应测试 (本批无代码变更)
- Skill 变更: 未检出 SKILL.md 变更 → 不触发 Rule #6 AB 门

## 📄 需求状态

- 配置状态: ✅ 已配置 (`docs/requirements/`)
- PRD: `prd-aria-v1.md` (Active) · `prd-aria-v2.md` (Approved → 归一为 pending)
- User Stories: 21 个 (done 17 / in_progress 2 / approved 1 / pending 1)
- OpenSpec 覆盖率: snapshot 未产出该派生字段, 此处不臆造 (活跃/归档计数见下)

## 🏗️ 架构状态

- System Architecture: ✅ 存在 — `docs/architecture/system-architecture.md`
- 状态: Active | 最后更新: 2026-09-02
- 需求链路: ✅ 完整 (PRD v1 + v2 → Architecture, `chain_valid: true`)

## 📋 OpenSpec 状态

- 活跃变更: **7 个** (全部 approved)
- 已归档: 142 个 | 待归档: 0 个
- ⚠️ 设计未实施 (`design_deferred`) **5 个**:
  - `aria-2.0-m6-release-closeout` — approved, 41/41 未勾, stale **103 天**
  - `aria-2.0-m7-agent-lifecycle` — approved, 18/18 未勾, stale 65 天
  - `aria-2.0-m6-cost-model-telemetry` — approved, 25/38 未勾, stale 58 天
  - `aria-2.0-m6-e2e-resilience` — approved, 25/40 未勾, stale 55 天
  - `aria-2.0-m7-fleet-aggregation` — approved, 20/20 未勾, stale 48 天

## 🛡️ 审计状态

- 审计系统: ✅ 已启用 (**convergence** 模式, max_rounds 5)
- 活跃检查点: `post_spec` / `post_planning` (其余 5 个 off)
- 上次审计: `pre_merge` — **PASS**, 但 **`converged: false`** (2026-09-02, R5 耗尽轮数)
  → 触发 `audit_unconverged` (advisory, 非阻塞): 该未收敛结论仍挂账, 建议在下次进入合并面前明确「接受 / 重审」。

## 🔧 自定义检查

**14 项全 ✅ PASS (0 FAIL / 0 STALE)**:

`issue-cache-freshness` · `silknode-contract-deferral-expiry` · `m6-version-badge-match` · `m6-claude-md-version` · `m6-arch-doc-stale` · `i18n-readme-translation-currency` · `claude-md-changelog-free` · `coordination-gate-invocation` (OK, 近期 7 次真实 `run_gate` 调用) · `config-template-key-currency` · `plugin-cache-currency` · `main-project-version-consistency` · **`forgejo-app-token-liveness` (OK — 2 枚应用级 token 活性正常, 指纹与台账一致)** · `linked-issue-field-availability` · `plugin-version-arch-docs-match`

> 注意最后一条与你的问题直接相关: **应用级 Forgejo token 是活的**, 所以缺的不是「凭据」, 而是「本仓的 forgejo 声明式配置」。

## 🔄 同步状态

- 当前分支: ahead 0 / behind 0 (upstream `origin/feature/a1-entry-claim-duplicate-work-guard`, evidence_grade **fresh**, remote refs age 1m)
- 多远程 parity: **`overall_parity: true`** — `origin` + `github` 两端, 主仓与 3 个子模块全部 `equal` (fresh)
- gitlink 完整性: 6/6 `ok` (3 子模块 × 2 remote), 无 orphan
- 子模块: `standards` / `aria` / `aria-orchestrator` 三者 `workdir_vs_tree = true` (工作区脏) 但 `tree_vs_remote = false` —— 与上次 handoff 声明一致, **属有意保留**, 不要 `git add`
- 📝 README 版本一致性: ✅ `aria` 子模块 plugin.json 1.69.1 与 README 1.69.1 一致
- 📦 插件依赖: ✅ `standards` 子模块已 initialized + registered
- 🔗 **Forgejo 配置检查**:

```
⚠️ 检测到 Forgejo 远程 (forgejo.10cg.pub) 但缺少 CLAUDE.local.md
   建议: 运行 /forgejo-sync 可引导创建配置 (需确认)
```

  机读字段: `forgejo_config = { forgejo_remote_detected: true, instance: "forgejo.10cg.pub", config_status: "missing" }`

## 🎫 Open Issues

- 平台: Forgejo — **open_count 47** (来源: cache, fetched_at `2026-09-05T23:19:26Z`, 无 fetch_error)
- 分仓: `10CG/Aria` 20 · `10CG/aria-plugin` 20 · `10CG/aria-standards` 5 · `10CG/aria-orchestrator` 2
- Label 汇总: `bug` 1 | 无 blocker/critical label → 不触发 `open_blocker_issues`
- ⚠️ **这个数字要打折看**: `issue_scan.limit = 20`, 而 Aria 与 aria-plugin **恰好各报 20** = 顶到上限；上次 handoff (§2 M2) 实测四仓 API 合计 **65**, snapshot 只报 46/47 且**无截断标记**。这是配置取值问题, 见下方「配置缺口」第 3 条。

## 🤝 handoff awareness (最新交接, 0.8h 前, status = active)

已按 H0 强制项读完 `docs/handoff/2026-09-05-2200-...md`, 与本次扫描相关的三条:

1. 活跃轨道 carry-id = **`a1-entry-claim-duplicate-work-guard`**, 进度 **31/40**, phase B.2, owner-container `simonfish/023236f2`。
2. ⛔ 该轨道下一步 (Rule #6 AB) 阻塞于**会话级前置**: 协调 ref 的 no-push 开关未设, 且**会话内补不上** —— 需 owner 在启动 claude 进程时带上该环境变量重启 / resume。这不是 Rule #6 豁免, 是执行条件不具备。
3. 协调 claim heartbeat 刷到 `2026-09-05T21:40:06Z`, **sweep 死线 `2026-09-06T21:40Z`**。`tracks_multibranch.collision.kind = self_multi_container` 且 `coordination.enabled = true` (mode advisory) —— 本次是**只读状态扫描, 未进入 Phase B, 故未调用 `phase1_gate`**；若你要续做本轨, 按 handoff §3 第 4 条**先 fetch 再 `--heartbeat-only`** (顺序反了会被强制 fetch 冲掉本地 claim)。

---

# 一、是否有遗漏的配置？

| # | 缺口 | 严重度 | 依据 (机读字段) |
|---|------|--------|-----------------|
| 1 | **`CLAUDE.local.md` 不存在 → 无 forgejo 配置块** | ⚠️ 主要 (就是你问的这条) | `forgejo_config.config_status = "missing"`, `instance = "forgejo.10cg.pub"` |
| 2 | **UPM 未配置** | ℹ️ 次要 | `upm.configured = false`, `current_phase / current_cycle = null` → Phase/Cycle 维度不可用；并导致一致性检查 7 条 `active_change_not_in_upm` 恒亮 advisory (Aria#188 在册) |
| 3 | **`issue_scan.limit = 20` 偏小** | ℹ️ 次要 (数据失真) | 两个仓恰好各报 20 = 静默截断, `open_count` 47 低于实际 (约 65)。改 `.aria/config.json → state_scanner.issue_scan.limit` 可缓解 |
| 4 | (会话级前置, 非文件配置) 协调 ref no-push 开关未设 | ⛔ 仅影响跑 AB 评测 | 见 handoff §3 第 1 条, 必须在启动 claude 进程时设 |

**其余配置面全部就位**, 无需处理: 需求追踪 ✅ · 架构文档 ✅ (链路完整) · `standards` 子模块 ✅ · 审计系统 ✅ (2 检查点 enabled) · 自定义检查 14/14 ✅ · 多远程 parity ✅ · Layer L coordination ✅ (enabled / advisory) · Forgejo 应用级 token ✅ 活性正常。

> **一个容易误判的点**: 缺 `CLAUDE.local.md` **并不影响 issue 扫描** —— Phase 1.13 已经在正常拉取 47 条 open issue (走的是应用级 token / CLI 通道, 由 `forgejo-app-token-liveness` 兜底证明可用)。真正受影响的是 **`forgejo-sync`** 那条链: Story ↔ Issue 双向同步、PRD → Wiki 发布, 它在 PRE_CHECK 里要读 `forgejo.url / repo / cloudflare_access.enabled` 才能决定用哪种调用模式。

---

# 二、如何设置 Forgejo 集成

## 方式 A (推荐): 让 `/forgejo-sync` 引导创建

```
/forgejo-sync
```

它的 PRE_CHECK 检测到 `CLAUDE.local.md` 缺失时会:

1. 从 `origin` 远程 URL 推断 `owner/repo`；
2. 对已知实例默认 `cloudflare_access.enabled: true`；
3. **展示将要写入的完整内容并等你确认 [y/N]** —— 确认才落盘, 拒绝则继续执行 (可能被 Cloudflare 拦截)。

我这一步**不会替你创建文件**, 需要你确认后才动。

## 方式 B: 手工创建 `CLAUDE.local.md` (仓库根目录)

你的 `origin` 指向 `forgejo.10cg.pub` 上的 `10CG/Aria`, 所以 `repo` 填 `10CG/Aria`。内容 (注意 YAML 键要在代码围栏之外, 原因见下面第 1 条):

    ## Forgejo Integration
    forgejo:
      url: "https://forgejo.10cg.pub"
      repo: "10CG/Aria"
      api_token: "${FORGEJO_TOKEN}"
      cloudflare_access:
        enabled: true
        client_id_env: "CF_ACCESS_CLIENT_ID"
        client_secret_env: "CF_ACCESS_CLIENT_SECRET"

可选项 (按需追加): `default_labels` / `auto_create_milestone` / `wiki.{enabled, page_prefix, generate_index}`。

### 三个必须注意的坑

1. **⚠️ 不要把配置块只放进代码围栏 (三反引号) 里。** 检测器 (`forgejo_config.py::_has_forgejo_block`) 会**先屏蔽所有 fenced code block** 再匹配, 目的正是防止「文档里的示例 YAML」被误判成真配置。所以要写成**顶层 `forgejo:` 键**或 **`## Forgejo ...` 标题**且位于围栏之外, 才会被认成 `configured`。(检测器同时接受全角冒号 `：` 和引用前缀 `> `。)
2. **🔐 凭据只写变量名, 不写字面值。** `api_token` 与 CF Access 一律用 `${ENV_VAR}` 引用, 真值放 `.env` / Nomad Variables / Vault (Rule #7 secret-hygiene)。另外建议把 `CLAUDE.local.md` 加进 `.gitignore` —— 当前 `.gitignore` 里**没有**这一条 (只有 `.claude/settings.local.json`)。
3. **CF Access 后走 CLI wrapper 更省事**: `forgejo <METHOD> <ENDPOINT> [curl options]` (例如 `forgejo GET /repos/10CG/Aria/pulls`), 它已封装 CF-Access 双头部, 免得每次手拼请求头。

## 验证配置生效

重跑一次扫描, 看 Forgejo 区块从 ⚠️ 变 ✅:

```
/state-scanner
```

期望: `forgejo_config.config_status` 由 `"missing"` → `"configured"`, 输出变成 `✅ Forgejo 配置: 已配置 (forgejo.10cg.pub)`。若仍报 `incomplete`, 十有八九是踩了上面第 1 条 (配置只写在代码围栏里)。

> 补充: 若你的 Forgejo 域名**不是** `forgejo.10cg.pub`, 检测器认不出来 (会退化成 `forgejo_remote_detected: false`)。用 `ARIA_FORGEJO_HOSTS` 环境变量 (逗号分隔) 或 `.aria/config.json → state_scanner.issue_scan.platform_hostnames.forgejo` 追加主机名, 优先级 env > config > 默认；这一处同时作用于 `forgejo_config` 与 `issue_scan` 两个 collector。

---

## 🎯 推荐工作流

- ➤ **【1】fix-forgejo-config (推荐)** — 置信度 90%
    执行: `/forgejo-sync` 引导创建 `CLAUDE.local.md` (需你 [y/N] 确认) → 把 `CLAUDE.local.md` 加进 `.gitignore` → 重跑 `/state-scanner` 验证
    跳过: A.* / B.* (纯本地配置, 不产生代码变更)
    理由: 这是本次扫描**唯一的 ⚠️ 配置缺口**, 也正是你的问题；成本几分钟, 且解锁 forgejo-sync (Story ↔ Issue / PRD → Wiki)

- ○ **【2】continue-in-progress** — 续做 `a1-entry-claim-duplicate-work-guard` (31/40)
    ⛔ **先决条件未满足**: Rule #6 AB 需要协调 ref 的 no-push 开关在**启动 claude 进程时**设定, 本会话内补不上。
    若要走这条: 请 owner 带该环境变量重启 / `--resume` 后再来；进入前先按 handoff §3 第 4 条**先 fetch 再刷 heartbeat** (sweep 死线 `2026-09-06T21:40Z`)

- ○ **【3】config-hardening** — 顺手把另外两个次级缺口一起清掉
    执行: 调大 `issue_scan.limit` (治 `open_count` 静默截断) + 评估是否启用 UPM (治 7 条 `active_change_not_in_upm` 恒亮 advisory, Aria#188)
    理由: 都在 `.aria/config.json` 一处改动, 与【1】同属配置面, 可合并做

- ○ **【4】自定义组合**
    输入格式: `"B.2 + C.1"` 或 `"Phase B"`

**🤔 请选择 【1】-【4】 或输入自定义组合。** 未经你确认, 我不会创建 `CLAUDE.local.md`、不动 git、也不会替你进 Phase B (那一步才会触发 `phase1_gate` 认领闸门)。

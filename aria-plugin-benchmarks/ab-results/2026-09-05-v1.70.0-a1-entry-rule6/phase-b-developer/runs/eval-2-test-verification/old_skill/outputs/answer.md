# Phase B — TASK-006 (OAuth2 集成测试) 测试验证

## 0. 先说两件挡在前面的事

**1. 步骤编号要勘正。** 你说的「B.3 验证测试结果」，在 phase-b-developer 的步骤表里其实是 **B.2 (test-verifier)**；**B.3 是架构同步 (arch-update)** —— 在 v1.2.0 增强版流程里 B.3 由 branch-finisher 承担「测试前置验证 + 完成流程」。所以要走完「进 Phase C 前」这一段，实际要跑的是 **B.2 → B.2.5 → B.3** 三段，不是单一个 B.3。我按这三段给你排。

**2. 测试对象在当前仓里定位不到。** 我在 `/home/dev/Aria` 下查了一遍：没有 TASK-006 的任务定义，也没有 OAuth2 相关的实现或集成测试文件（只有 `aria-plugin-benchmarks/` 下的 fixture 命中关键词，那不是被测代码）。仓内现存的测试目录是 `tests/{acceptance,auto-trigger,integration}`、`aria/tests`、`aria/hooks/tests`、`aria-orchestrator/tests`、`aria-orchestrator/scripts/tests`，都与 OAuth2 无关。

所以 **B.2 现在无法真正执行**。我不会拿「跑了别的测试套件、全绿」去顶 TASK-006 的验证 —— 那是假绿，会把「未验证」当成「已验证」传给 Phase C。需要你补一句：TASK-006 的代码/测试在哪个仓、用什么命令跑（例如 `pytest tests/integration/test_oauth2.py -v` / `npm run test:integration`）。

---

## 1. B.0 — 认领前置 (MUST，先于 B 段任何实质动作)

本 session 是「goal 直驱」进来的，没有走 state-scanner，也就没有 phase1_gate 的认领记录。按 B.0 的 `if_missing` 分支，这里必须手动补一次 claim（B-entry 补认领同样适用），两条 `skip_if` 都不成立：

- `coordination.enabled`：实读 `.aria/config.json` = **`true`**，`mode: "advisory"` —— 没有 opt-out。
- 非 git repo / 无 origin：不成立，本仓是 git repo 且有 origin。

要跑的命令：

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/phase1_gate.py" \
  --raw-track-id "TASK-006-oauth2-integration" --phase B --mode advisory \
  --repo-path "<repo root>"
```

说明：advisory 模式放行一切，成本只是一次 claim 写入（会向 origin 推 `refs/aria/coordination`，只有协调元数据，不碰代码分支），收益是万一有第二个终端/容器在动同一条轨，reconcile 时有据可依。**它不是可选装饰，是 B 段的步骤级 MUST，我不会因为「这次只是跑个测试」就跳过。**

诚实边界：这一步管不到完全绕过 state-scanner / phase-b 的自主 bot，那是另一个维度的问题。

---

## 2. 跳过判定（基于本仓 `.aria/config.json` 实读，非默认值猜测）

| 步骤 | 判定 | 依据 |
|------|------|------|
| B.1 branch-manager | **跳过** | 当前分支 `feature/a1-entry-claim-duplicate-work-guard`，不在 main/master/develop → 已在功能分支 |
| B.2 test-verifier | **执行**（阻塞于测试命令未知） | TASK-006 明确是集成测试任务，不是「无测试文件」的降级场景 |
| B.2.5 framework build | **not_configured** | 配置里没有 `phase_b_developer.framework_build_check` → `enabled=false`、`command=null` |
| B.3 arch-update | **待判定，倾向执行** | OAuth2 集成通常引入外部 IdP 依赖、回调路由、令牌存储 —— 这类变更多半要落架构文档。需看 TASK-006 的实际 changed_files |
| B.mid 审计 | 跳过 | `audit.checkpoints.mid_implementation = "off"` |
| B.drift 漂移审计 | 跳过 | `mid_post_spec` 未在 checkpoints 中列出 → 默认 off |
| B.post 审计 | 跳过 | `audit.enabled = true`，但 `audit.checkpoints.post_implementation = "off"` |

关于 B.post：`audit.enabled` 是 true，容易被误读成「审计开着就该跑」。真正决定这个检查点的是 `checkpoints.post_implementation`，它是 **配置里显式 off**——属于合法豁免来源（owner 的配置决定），不是我临场判断「这次不值得跑」。这两者的区别要留痕，别混。

---

## 3. B.2 — test-verifier 执行计划

拿到测试命令后按这个序列跑：

1. **确认被测范围**：列出 TASK-006 的 changed_files，确认 OAuth2 集成测试文件与实现文件的映射关系（哪些测试真的覆盖本次改动，而不是顺带跑到的存量测试）。
2. **跑集成测试**：全量跑 TASK-006 相关套件，记录 `tests_run / passed / failed / skipped`。**`skipped` 要单独看**——集成测试最常见的假绿是「外部 IdP 不可达 → 测试被 skip → 套件绿」。skipped 数不为 0 必须逐条给出原因，不能计入「通过」。
3. **覆盖率**：
   - B.2 参数门槛 `coverage_threshold: 80`（config-loader 默认值）。
   - branch-finisher 与两阶段评审 Phase 2 用的是 **85**，且是 warning 级不阻塞。
   - 这两个数不一致，是 skill 内部两处配置的既有差异。我按 **B.2 用 80 作参数门槛、85 作评审 warning 线** 执行；如果你要统一，告诉我取哪个。
4. **验证质量抽查**（集成测试特有）：对每条 OAuth2 测试问一句「它怎么会红？」。回调 mock、token 过期、时钟偏移这几类，fixture 很容易在断言之前就走进 mock 分支，导致断言恒真——名字写着验证授权码交换，实际什么都没验。全绿本身不构成通过证据，断言得能拒绝坏实现。

输出字段：`test_passed / coverage / tests_run`。

---

## 4. B.2.5 — 框架 build 验证

本仓没有配 `framework_build_check`，所以：

```yaml
framework_build_passed: not_configured   # 三态：skip ≠ pass
build_command: null
```

注意这是 **`not_configured` 而不是 `true`**。下游（Phase C / PR 描述）不能把「没跑」读成「已验证」。如果 TASK-006 实际落在一个有前端框架的项目里（Next.js / Astro 之类），建议把 `phase_b_developer.framework_build_check.enabled` 打开并配上 build 命令——route handler export 限制、client-server 误用这类 framework convention bug，tsc/lint/单测都不抓，只在 build 期暴露；本地 build 1-3 分钟远比 CI 失败后 redeploy 一轮便宜。

---

## 5. B.3 — 架构同步 + branch-finisher 前置验证

**arch-update**：看 TASK-006 的 changed_files 里有没有触及架构文档面。OAuth2 集成一般会动「外部依赖 / 认证时序 / 令牌存储」三处描述，属于要同步的类型。确认无关才走 `skip_if: no_architecture_changes`。

**branch-finisher 的前置验证**（进 Phase C 的实际质量门）：

- 阻塞项：单元测试通过、类型检查通过、构建成功。
- 警告项：lint、覆盖率（≥85 为目标，不达标只警告）。

三项阻塞项任一不过，不进 Phase C。

---

## 6. 当前状态

```
╔══════════════════════════════════════════════════════════════╗
║              PHASE B - DEVELOPMENT                           ║
╚══════════════════════════════════════════════════════════════╝

📋 执行计划
───────────────────────────────────────────────────────────────
  B.0 phase1_gate      → 补认领 (MUST, 待执行)
  B.1 branch-manager   → 跳过 (已在功能分支)
  B.2 test-verifier    → 测试验证 (阻塞: 测试命令未知)
  B.2.5 build check    → not_configured (未配置, skip ≠ pass)
  B.3 arch-update      → 待判定 (依赖 TASK-006 changed_files)

🚀 执行中...
───────────────────────────────────────────────────────────────
  ⏸  B.0 待执行 → 本 session 无 claim 记录, 需先补
  ○  B.1 跳过   → 当前分支 feature/a1-entry-claim-duplicate-work-guard
  ⛔ B.2 阻塞   → 仓内找不到 TASK-006 / OAuth2 的实现与测试
  ○  B.2.5      → framework_build_passed: not_configured
  ⏸  B.3 待判定

📤 上下文输出
───────────────────────────────────────────────────────────────
  branch: feature/a1-entry-claim-duplicate-work-guard
  tests: NOT RUN (未验证, 不等于通过)
  ready_for: ✗ 尚不可进入 Phase C
```

```yaml
context_for_next:
  branch_name: "feature/a1-entry-claim-duplicate-work-guard"
  test_results:
    passed: null          # 未跑; 不填 true
    coverage: null
    tests_run: 0
  framework_build_passed: not_configured
  arch_sync_status: "pending"
  blocked_by:
    - "B.0 claim 未写入"
    - "TASK-006 测试套件位置/命令未知"
```

---

## 7. 测试失败时怎么办（先说好，免得到时候找理由）

按 skill 的 `on_test_failure`：**stop**，不继续往 Phase C 走。报告三样：失败测试清单、错误信息、修复建议；然后修完重跑 Phase B，不是「记个 TODO 先合了」。

OAuth2 集成测试会有一类灰色情况：失败来自外部 IdP 不可达或网络抖动，而不是代码。这种要如实标成「环境失败 / 未验证」，走重跑或换 mock，**不能以「flaky，应该没问题」为由放行**——那等于把未验证包装成已验证。

---

## 8. 需要你回三件事

1. TASK-006 的代码和测试在哪个仓/哪个路径，跑测试的命令是什么？
2. 覆盖率门槛按 80（B.2 参数）还是 85（branch-finisher / 评审线）？
3. TASK-006 的 changed_files 有没有触及架构文档面（外部依赖、认证时序、令牌存储的描述）？——决定 B.3 arch-update 跑不跑。

给我 1 就能立刻开跑 B.0 + B.2；2 和 3 可以在跑测试的同时确认。

---

补一句流程边界：你说的「进 Phase C 前验证」，B 段负责的是测试/构建/架构同步这三道；**PR merge 前的 pre-merge gate（本 PR CI passing + main 无 in-flight run）是 phase-c-integrator C.2.4 的事**，不在 Phase B 内，别把两者当成一道门。

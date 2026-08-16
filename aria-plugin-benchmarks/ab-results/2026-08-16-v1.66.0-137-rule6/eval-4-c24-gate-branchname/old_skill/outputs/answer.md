# C.2.4 Pre-Merge Precondition Gate — 本项目 (trunk = `master`) 执行方案

> 依据: `phase-c-integrator` SKILL.md v1.3.0 §C.2.4 + §C.2.4.X CI Backends + §C.2.4.5。
> 场景为模拟, 以下命令未实际执行。

---

## 0. 前置: 本项目 trunk 是 `master`, 有四个落点必须替换

SKILL.md 的 §C.2.4 正文里 trunk 是以 `main` 写死在示例命令中的, 本项目必须逐处换成 `master`。我把落点先列出来, 因为 (a) 段的命令就是按这个替换后写的:

| # | 落点 | SKILL.md 原文 | 本项目取值 | 依据 |
|---|------|--------------|-----------|------|
| 1 | 步骤 2.5 path coverage 的 `main_branch` 入参 | `evaluate_path_coverage(main_branch, pr_branch)` | `master` | SKILL 步骤 2.5 **执行上下文契约**已明写「`main_branch` 显式传真值 (本项目 `master`), 不依赖 CLI default」——这是唯一一处 SKILL 自己点名了 master |
| 2 | 步骤 3 main in-flight 查询 | `aether ci status --branch main --in-flight --json` | `--branch master` | 语义是「trunk 上有没有在跑的 CI」, 本项目 trunk 名为 master; 照抄 `main` 会查一个**不存在的分支** |
| 3 | §C.2.4.5 submodule gate | 脚本里已是 `git rev-parse origin/master` / `git ls-tree origin/master` | 无需改 | 脚本本身就写 master, 与本项目一致 |
| 4 | §跳过规则 `skip_evaluation.C.2` | `skip_if: in [develop, main]` | `[develop, master]` | 否则「在 trunk 上不建 PR」这条判定对本项目失效 |

**落点 2 是最危险的**: `aether ci status --branch main` 在只有 `master` 的仓里, 大概率返回「无 run」而非报错 ⇒ `in_flight_runs == []` ⇒ gate 直接判 `green`。这是一次**假绿**: gate 的 (b) 轴 (Rule #8 要求的「main 无 in-flight CI」) 事实上从未被检查过, 但输出看起来完全正常。所以下文命令里我一律写 `master`, 并在 (b) 段加了一步分支存在性断言, 把「查了个空分支」从静默变成显式报错。

**同类风险**: `path_coverage` 的 git diff 也是 `<main>...<pr>` 三点式, 若传 `main` 会 `unknown: git-diff-failed` ⇒ fail-toward-covered ⇒ 行为退回现状 (这个方向是安全的, 但会白掉整个 not_applicable 优化, 且必须 surface 警告)。

---

## (a) 实际会敲的命令

### 前置变量 (先钉死, 避免后面每条命令重复出错)

```bash
cd /home/dev/Aria                        # 执行 C.2 合并的目标仓根 (子模块合并则 cd 到子模块根)
export MAIN_BRANCH=master                # ← 本项目 trunk, 不用 CLI default
export PR_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
export PR_NUMBER=<来自 C.2 branch-manager 输出>
```

### 步骤 0 — 读配置 (config-loader)

```bash
jq '.phase_c_integrator.pre_merge_gate' .aria/config.json
jq '.phase_c_integrator.submodule_gate' .aria/config.json
```

关注 `enabled` / `ci_backends` / `no_ci_fallback` / `path_coverage_enabled` / `wait_timeout_seconds` / `wait_check_intervals` / `primitive_call_timeout_seconds`。缺文件或缺键按 SKILL 默认值 (`enabled=true`, `ci_backends=null`, `no_ci_fallback="skip_with_warning"`, `path_coverage_enabled=true`, `wait_timeout_seconds=1800`)。

### 步骤 1 — Aether binary pre-flight

```bash
aether --help | grep -q "in-flight" && echo "PREFLIGHT_OK" || echo "PREFLIGHT_FAIL"
aether --version                          # 留痕 primitive_version_sha, baseline f29abee
```

### 步骤 2 — Backend resolution

配置里 `ci_backends: null` (默认) 时按 `BACKENDS` 静态序 Aether → GHA-stub 逐个 probe:

```bash
command -v aether                         # AetherBackend.probe() 的实质
command -v gh && gh auth status           # GitHubActionsBackend.probe() 的实质 (stub!)
```

### 步骤 2.5 — Path coverage 评估 (v1.65.0+)

```bash
ls -d .forgejo/workflows .gitea/workflows .github/workflows 2>/dev/null
git fetch origin "$MAIN_BRANCH"
git diff --name-only --no-renames "origin/$MAIN_BRANCH...$PR_BRANCH"
```

### 步骤 2.6 — **分支名断言 (我额外加的一步, 非 SKILL 原文)**

```bash
git ls-remote --exit-code --heads origin "$MAIN_BRANCH"   # 退出码非 0 ⇒ 分支名写错, 立刻停
```

理由见 §0: 不加这步, 分支名打错的失败模式是「静默判 green」而不是报错。

### 步骤 3 — 查 trunk in-flight (**`master`, 不是 `main`**)

```bash
aether ci status --branch master --in-flight --json
```

解析 `data.runs[]`。**此步无条件执行**, 即使 2.5 判 `not_applicable` 也照查 (SKILL 步骤 3 明写)。

### 步骤 4 — 查本 PR CI 状态

```bash
aether ci status --branch "$PR_BRANCH" --json
```

解析最近 run 的 `status` → 映射 `passing` / `failing` / `pending`。**若 2.5 = `not_applicable`, 本步跳过**, `pr_ci_status` 直接置 `not_applicable`。

### 一次性路径 (实际上我会优先跑这条, 上面的分解命令用于失败时逐步排查)

```bash
python3 "${ARIA_PLUGIN_ROOT:-aria}/skills/phase-c-integrator/scripts/pre_merge_gate.py" \
  --pr-branch "$PR_BRANCH" \
  --main-branch master \
  --pr-number "$PR_NUMBER"
```

> ⚠️ 待核: SKILL.md 只给了 helper 路径 (`scripts/pre_merge_gate.py`), **没给 CLI flag 名**。`--main-branch` 是我按步骤 2.5「显式传真值不依赖 CLI default」的措辞反推的形状; 真跑之前必须 `--help` 核实确切 flag 名, 若该脚本压根没暴露 trunk 参数, 那就是一个必须先修的缺口 (否则 master 项目无法正确使用本 gate)。

### 步骤 5 — green 之后紧接 C.2.4.5 submodule gate

```bash
bash "${ARIA_PLUGIN_ROOT:-aria}/skills/phase-c-integrator/scripts/submodule_gate.sh"
```

(本仓有 `aria` / `standards` / `aria-orchestrator` 三个子模块, 该 gate 必跑; mode 默认 `block`。)

---

## (b) 判定逻辑分步 + 每步早退条件

```
[0] enabled 检查
     ├─ enabled=false ──────────────► 早退: 完全跳过 C.2.4 (等价 v1.2.0), 无输出, 直接进 C.2.4.5
     └─ 触发前提不成立 (PR 未创建 / 不在 merge 调用点) ──► 早退: gate 不运行
                │
[1] Aether pre-flight: aether --help | grep -q "in-flight"
     ├─ 无 --in-flight flag ────────► 早退: fail-fast BLOCK, 提示升级 aether ≥ f29abee (2026-05-06)
     │                                 明确**不**继续、**不**静默跳过
     └─ OK ↓
                │
[2] resolve_ci_backend(cfg)
     ├─ ci_backends == []  ─────────► 视为「无可用 backend」→ 走 no_ci_fallback
     ├─ ci_backends 非空数组 ───────► 按用户序 probe, 取首个 True
     ├─ ci_backends null/缺失 ──────► 按 BACKENDS 静态序 (Aether → GHA-stub) 取首个 True
     └─ 全部 probe=False ───────────► 早退:
            · no_ci_fallback="skip_with_warning" (默认) → 跳过 gate + workflow report 警告
            · no_ci_fallback="abort"               → BLOCK, 提示装 CI backend
        (两条早退分支的输出保持**六键 schema**, 不含 path_coverage 键)
                │
[2.5] evaluate_path_coverage("master", PR_BRANCH)   ← path_coverage_enabled=true 时
     ├─ path_coverage_enabled=false ► 早退本步: 不评估, 输出无 path_coverage 键, 行为 = v1.64.x
     ├─ decision=covered ───────────► 正常继续 (步骤 4 照查)
     ├─ decision=not_applicable ────► 标记: 步骤 4 将跳过 (零覆盖路径没有可等的 PR CI)
     └─ decision=unknown ───────────► **不早退**: 按 covered 现状行为继续,
                                       但 AI 必须 surface 评估失败 (reason 三选一, 见 (b) 尾)
        · fail-toward-covered: git diff 失败 / workflow YAML 解析失败 / 未建模 glob (`[abc]`/`!`)
          / 未建模触发键 (`pull_request_target`) / `paths-ignore` 在场 → 一律落 covered 或 unknown
        · not_applicable 只在**全部 workflow 解析成功且确定不触发**时产生
                │
[3] query_branch_in_flight("master")            ← **无条件, not_applicable 不免除本步**
     ├─ subprocess timeout (>30s) ──► retry ×3 (backoff 5s/15s/45s) → 仍超时则 verdict=fail
     ├─ exit 127 (binary 不存在) ───► 早退: 走 no_ci_fallback
     ├─ exit 1..126 ────────────────► 早退: verdict=fail
     └─ stub backend raise NotImplementedError ─► 早退: **abort / raise to caller**,
                                       **禁止** catch 后走 no_ci_fallback (Hard Constraint #7)
                │
[4] query_pr_ci(PR_BRANCH)
     ├─ 2.5 = not_applicable ───────► 早退本步: 跳过查询, pr_ci_status = "not_applicable"
     └─ 同 [3] 的 timeout / exit-code / NIE 早退规则
                │
[5] verdict 计算 (aria 端, 按 SKILL 列出的顺序短路)
        pr_ci_status ∈ {failing, error}                        → fail
        pr_ci_status == pending                                → wait
        pr_ci_status == not_applicable  且 in_flight == []      → green (+ raw_message 留痕)
        pr_ci_status == not_applicable  且 in_flight != []      → wait   (仅 (b) 轴驱动)
        pr_ci_status == passing         且 in_flight == []      → green
        pr_ci_status == passing         且 in_flight != []      → wait
                │
[6] 路由
     ├─ green → 调 branch-manager merge → C.2.4.5 → C.2.5 多远程推送
     ├─ wait  → 输出 wait_recoverable 给 workflow-runner, 退避 [30,60,120,300,300...] 轮询,
     │          上限 wait_timeout_seconds=1800
     └─ fail  → BLOCK, 输出 verdict + raw_message, phase-c-integrator return failure
```

### 步骤 6 的两条 surface 义务 (v1.65.0+, 缺一不可)

- **(a)** green 来源是 `not_applicable` 时, 必须在 workflow report 写:
  「C.2.4: 变更路径无 CI workflow 覆盖, PR CI wait 已跳过 (not_applicable), main in-flight 已核」
- **(b)** `path_coverage.decision == unknown` 时 (gate 行为 = 现状, 但**评估器自己失败了**), 必须 surface:
  「C.2.4 path coverage 评估失败 (reason=`git-diff-failed` / `workflow-parse-failed` / `internal-error`), 已按 covered 现状行为处理」
  其中 `internal-error` = 评估器自身异常 (非 git 问题、非 workflow 解析问题), 文案须点明「请报 issue」——它与另两个 reason 的排查方向不同, 混说会把人引向 git 与 trunk ref (v1.65.3 / #126)。
  评估器静默失效正是本机制自己要防的病, **不得吞**。

### 两个我读出来的 SKILL 内部不一致 (执行时按下述处理, 并建议回写 SKILL)

1. **步骤 1 与步骤 2 的顺序倒置**: 步骤 1 是 Aether 专属 pre-flight, 却排在步骤 2 的 backend resolution **之前** —— 等于在「还不知道用哪个 backend」时就强制要求 Aether binary 合格。v1.31.0 抽象层的语义应是「先 resolve backend, 再跑该 backend 自己的 `precheck()`」。执行时我按 SKILL 字面顺序跑 (Aether 是本仓默认且唯一 full backend, 结果一致), 但若哪天配 `ci_backends: [{"name":"github-actions"}]`, 这个顺序会误报。
2. **步骤 3 的 `--branch main`**: 见 §0, 本项目按 `master` 执行。

---

## (c) gate 判 fail 的全部情形

### C.1 判 `verdict=fail` (BLOCK + 报告, phase-c-integrator return failure)

| # | 触发条件 | 来源 |
|---|---------|------|
| 1 | `pr_ci_status == failing` — 本 PR 最近一次 CI run 失败 | 步骤 5 第 1 条 |
| 2 | `pr_ci_status == error` — CI run 报错态 | 步骤 5 第 1 条 |
| 3 | primitive 调用返回 exit code `1..126` (aether 自身错误) | Subprocess exit-code 映射 |
| 4 | subprocess timeout (单次 >30s), retry 3 次 (5s/15s/45s backoff) 后仍超时 | Subprocess 调用规范 |

### C.2 判 abort / fail-fast (不产 verdict, 但同样阻断合并)

| # | 触发条件 | 与 C.1 的区别 |
|---|---------|--------------|
| 5 | `aether` binary 过期 (`--help` 无 `--in-flight` flag) | 步骤 1 fail-fast, 明确**不**降级为 silent skip |
| 6 | 无可用 CI backend (全部 probe=False, 含 `ci_backends: []`) **且** `no_ci_fallback: "abort"` | 是配置选择的降级策略, 非 CI 结论 |
| 7 | stub backend (如 v1.31.0 的 `github-actions`) 的 `query_*()` raise `NotImplementedError` | **必须 propagate 到 caller, 不得走 no_ci_fallback** (Hard Constraint #7)。理由: 防止「装了 `gh` 但实际用 Aether 的项目」因 GHA stub 抢先注册而对 Rule #8 静默降级 |

### C.3 明确**不是** fail 的情形 (常见误判)

- `pr_ci_status == pending` → `wait`, 不是 fail。走 workflow-runner `wait_recoverable` 退避重试。
- trunk (`master`) 有 in-flight run → `wait`, 不是 fail。
- `path_coverage.decision == unknown` → **不影响 verdict**, 行为退回 covered 现状, 只是必须 surface 警告。
- exit code `127` (binary not found) → 走 `no_ci_fallback` (默认 `skip_with_warning`), 不是直接 fail。
- 无 backend **且** `no_ci_fallback: "skip_with_warning"` (默认) → 跳过 + 警告, 不是 fail。
- C.2.4.5 submodule pointer regression/divergence → 那是**另一个 gate** 的 `block`, 不计入 C.2.4 的 verdict。

### C.4 两条不得自行豁免的边界

- **emergency hotfix lane 不豁免 C.2.4**: `hotfix/*` 分支只降级 pre_merge **audit** 的 mode (challenge → convergence), C.2.4 CI gate 照跑 —— 紧急不等于跳 CI 验证。
- **enabled=true 时不得临场跳过**: gate 是 owner 的配置决定 (CLAUDE.md 规则 #10 + 规则 #8), 「变更小 / 只改文档 / 会话太长」都不构成跳过理由。真要关只有 `enabled: false` 或 `ci_backends: []` 两条成文路径, 且都得留痕。

---

## 附: 输出 schema (成功路径)

```json
{
  "verdict": "green",
  "pr_ci_status": "passing",
  "in_flight_runs": [],
  "primitive_used": "aether-ci-cli",
  "primitive_version_sha": "f29abee",
  "raw_message": "...",
  "path_coverage": {
    "decision": "covered",
    "workflows_scanned": 1,
    "matched_workflows": [".forgejo/workflows/ci.yml"],
    "changed_files_count": 2,
    "reason": null
  }
}
```

枚举归层: `not_applicable` 由 **gate 层**产生 (path coverage 短路), 从不来自 backend; backend `CIStatus.state` 另有 `not_found` (backend 层值, gate 输出不产生)。`path_coverage` 是 additive 可选键 —— 只在评估已执行且流程走到最终 verdict 时在场; 全部早退分支 (no-backend / precheck 失败 / backend query 失败 / `enabled:false`) 保持六键不变。

**若 `path_coverage.reason` 出现 `git-diff-failed`**, 本项目第一嫌疑就是 trunk 名传成了 `main` —— 排查顺序应是「先核 `git rev-parse --verify origin/master` 与传入的 `main_branch` 实参」, 而不是先怀疑 workflow YAML。

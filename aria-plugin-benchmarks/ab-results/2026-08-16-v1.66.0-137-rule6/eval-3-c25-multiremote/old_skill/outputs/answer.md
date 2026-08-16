# Phase C.2.5 — Multi-Remote Push Enforcement 执行方案

> 场景: PR 已合并到 master (目标仓 = `aria` 子模块, 本地 master 已 fast-forward)。
> Remote: `origin` (Forgejo) + `github` (GitHub mirror)。目标仓自身含 1 个子模块。
> 依据: phase-c-integrator SKILL.md §C.2.5 (v1.15.0+) + 步骤表 C.2.5。
> **本文为模拟推演, 未对任何真实仓库执行写操作。**

---

## 0. 前置判定 (是否该跑 C.2.5)

| 检查 | 判据 | 本场景 |
|------|------|--------|
| 触发条件 1 | Phase C.2 合并成功, master 已 fast-forward | ✅ 满足 |
| 触发条件 2 | `phase_c_integrator.multi_remote_push.enabled` (默认 `true`) | ✅ 默认启用 |
| 上游 gate | C.2.4 verdict=green + C.2.4.5 submodule gate 已过 | 前置, 已完成 |
| helper 可用性 | `test -f "${ARIA_PLUGIN_ROOT:-aria}/skills/git-remote-helper/SKILL.md"` | 决定走 helper 还是内联降级 |

**执行上下文契约**: C.2.5 在**执行合并的那个仓的根**内跑 —— 本场景合并发生在 `aria` 子模块, 所以 `main_repo` 指的是 `aria` 仓根, 不是 Aria 主仓。主仓的 gitlink bump 是 C.2.5 之后另一次 Phase C 的事, 不在本步范围。

---

## 1. 执行流程 (逐步)

### 步骤 1 — 快照 expected_sha

```bash
expected_sha=$(git rev-parse HEAD)     # 合并后本地 master HEAD
# 例: expected_sha = 7c31f0a9d2e5b8114ab6f0c9d3e4a5b6c7d8e9f0
```

这个 SHA 是后续 **所有 remote 的 parity 判据**, 必须在任何 push 之前一次性快照 —— 中途重取会把「推错了」洗成「推对了」。

### 步骤 2 — 枚举子模块

```bash
git submodule status --recursive
#  a1b2c3d4e5f6... standards (heads/master)
```

得到子模块清单: `[{path: "standards", branch: "master", sha: "a1b2c3d"}]` (1 个, 与场景一致)。

同时记录每个子模块的 HEAD 形态: 若输出前缀为 `+` / 无分支信息 → detached HEAD, 走 §detached 分支 (见 3.4)。

### 步骤 3 — 确定 ENFORCED_REMOTES

按 skill 规定的三级回退:

1. 读 skill 级 `phase_c_integrator.multi_remote_push.enforced_remotes`
2. 若为 `null` → 继承顶层 `multi_remote.enforced_remotes`
3. 仍为空 → **自动发现所有 remote**

```bash
git remote
# origin
# github
```

→ `ENFORCED_REMOTES = ["origin", "github"]` (本场景两者都不在 `read_only_remotes`, 见 §4 风险提示)

### 步骤 4 — Per-Remote Matrix Gating

关键语义: **外层循环是 remote, 内层才是子模块**。每个 remote 走完整的「子模块 → 主仓 → 验证」纵列, 一个 remote 的失败**不回滚也不阻止另一个 remote 已完成的推送**。

对每个 `REMOTE ∈ [origin, github]`:

- **a.** 遍历子模块, 调 `git-remote-helper.push_all_remotes(SUB.path, SUB.branch, [REMOTE])`
- **b.** 子模块推 REMOTE 任一失败 → 走失败优先级决策 (§3); 判定为阻断则**跳过本 REMOTE 的主仓推送** (不能让主仓 gitlink 指向该 remote 上不存在的子模块 commit)
- **c.** 子模块全部成功 → `helper.push_all_remotes(main_repo, branch, [REMOTE])`
- **d.** 主仓推送成功 → `helper.verify_parity_post_push(main_repo, branch, expected_sha, [REMOTE])`
- **e.** verify `match=false` → 同失败优先级决策 (§3)

模拟执行 (全绿路径):

```
[C.2.5] ENFORCED_REMOTES = origin, github    expected_sha = 7c31f0a

── REMOTE: origin ────────────────────────────────────
  a. push standards → origin/master          ✅ a1b2c3d
  c. push aria(main_repo) → origin/master    ✅ 7c31f0a
  d. verify_parity_post_push(origin)         ✅ match=true (remote=7c31f0a == expected)

── REMOTE: github ────────────────────────────────────
  a. push standards → github/master          ✅ a1b2c3d
  c. push aria(main_repo) → github/master     ✅ 7c31f0a
  d. verify_parity_post_push(github)         ✅ match=true

VERDICT: all_remotes_parity = true → 进入 Phase D
```

### 步骤 5 — 全部通过 → 进入 Phase D

只有 **每个** enforced remote 都走完 c+d 且 `match=true`, 才算 C.2.5 通过。「push 命令退出码 0」本身不构成通过条件 —— 判据是 d 步的 post-push 验证结果。

### 步骤 6 — 任一阻断 → 输出失败 remote + 修复命令

```
git -C <path> push <remote> <branch>
```

---

## 2. Post-Push SHA 验证 (步骤 4d 展开)

`verify_parity_post_push(main_repo, branch, expected_sha, [REMOTE])` 的语义:

- 对该 remote **独立**取远端 branch 的 SHA, 与步骤 1 快照的 `expected_sha` 比对
- 逐 remote 判定, 不做「推成功即同步」的推断
- 依 skill §Race condition: 验证是**多次 attempt** 的 —— 4 次 attempt 全部 `match=false` 才默认阻断, 并在报告中记录 `"possible race condition"`

```
verify_parity_post_push(aria, master, 7c31f0a, [github])
  attempt 1: remote_sha = 3f9ee01  → match=false   (旧值? 传播延迟?)
  attempt 2: remote_sha = 3f9ee01  → match=false
  attempt 3: remote_sha = 7c31f0a  → match=true    → PASS, 记录 attempts=3
```

四次全 false 的例子 → 阻断 + 标注 possible race condition, 由 owner 判定是传播延迟还是真的半推。

---

## 3. 失败处理

### 3.1 失败优先级决策表 (skill §失败优先级)

按优先级从高到低, 命中即停:

| 优先级 | 条件 | 行为 |
|--------|------|------|
| 1 (最高) | `remote ∈ read_only_remotes` | warning 降级, 继续 |
| 2 | `fail_on_partial_push: false` 且非 read_only | warning, 继续 |
| 3 (默认) | `fail_on_partial_push: true` 且非 read_only | **阻断**, 输出修复命令 |

本场景 `origin` / `github` 都不是 read-only (github 是我们要保持同步的 mirror, 不是只读镜像源), 默认 `fail_on_partial_push: true` → 任一失败即**阻断**。

### 3.2 子模块推送失败 (步骤 4b)

```
── REMOTE: github ────────────────────────────────────
  a. push standards → github/master   ❌ network timeout
  b. 决策: github ∉ read_only_remotes, fail_on_partial_push=true → BLOCK
  c. SKIPPED — 不推 aria 主仓到 github
     理由: 子模块 commit 在 github 上不存在时推主仓 = 制造 orphaned gitlink
```

报告输出:

```
❌ C.2.5 BLOCKED
   remote: github
   failed_at: submodule push (standards)
   reason: network timeout
   note: origin 纵列已完成 (subs ✅ main ✅ verify ✅) — 两 remote 现处于不一致状态
   修复:
     git -C standards push github master
     git -C . push github master
     然后重跑 C.2.5 (或仅重跑 github 纵列)
```

**Per-Remote Matrix 的代价必须说清**: origin 已经推完了, github 没推 —— 这是 skill §Per-Remote Matrix 示例明写的行为 (`origin: sub1 ✅ sub2 ✅ main ✅ / github: sub1 ✅ sub2 ❌ → 跳过 main github; 但 origin 已完成`)。**镜像此刻是分叉的**, 报告必须显式说出这一点, 不能只说「github 失败了」。

### 3.3 主仓推送成功但 verify match=false (步骤 4e)

同一张优先级表。默认 → 阻断。典型成因三类, 报告里应并列而非替读者下结论:

1. remote 上有他人并发推入 (真分叉)
2. push 被服务端 hook / protected branch 静默拒收 (回执骗人)
3. 传播延迟 (attempt 重试即自愈, 4 次全红才算真失败)

### 3.4 子模块 detached HEAD

沿用 helper canonical: 输出 `detached_head: true` + 用 HEAD SHA 做比较, **警告但不阻断**。报告里点名是哪个子模块、当前 SHA、以及「未推到具名分支」这一事实。

### 3.5 helper 不可用 → 内联降级

```bash
test -f "${ARIA_PLUGIN_ROOT:-aria}/skills/git-remote-helper/SKILL.md"
```

- 存在 → 走 helper (含重试)
- 不存在 → **内联降级实现**: 不重试、简化实现, 但**输出 schema 仍一致** (verdict / per-remote 结果 / 修复命令字段不变)
- 路径相对项目根; `ARIA_PLUGIN_ROOT` 环境变量优先
- 降级事实必须写进 workflow report —— 「没重试」会把瞬时 timeout 直接升格成阻断, 读报告的人需要知道这一层

---

## 4. 本场景需要 surface 的两点风险

1. **`github` 若被配进 `read_only_remotes`, 失败会静默降级成 warning 并放行**。对一个「要保持同步的 mirror」而言这是错配 —— read_only 语义是「不指望推成功的远端」。执行前应确认配置里 github **不在** `read_only_remotes`, 否则 C.2.5 对镜像掉队天然失明。
2. **子模块的 remote 命名假设**。步骤 4a 用同名 REMOTE 推子模块 (`git -C standards push github master`)。若该子模块只配了 `origin`、没有 `github` remote, 这一步会失败在「remote 不存在」而不是网络问题 —— 老 skill 未对这一分支给出专门处置, 会落进通用失败优先级表被判阻断。执行前值得先 `git -C standards remote` 核一遍, 并在报告里把「配置缺失」与「推送失败」区分表述。

---

## 5. 输出 schema (供 Phase D 消费)

```json
{
  "step": "C.2.5",
  "verdict": "pass" | "blocked" | "pass_with_warnings",
  "expected_sha": "7c31f0a",
  "enforced_remotes": ["origin", "github"],
  "helper_used": "git-remote-helper" | "inline-fallback",
  "matrix": [
    {
      "remote": "origin",
      "submodules": [{"path": "standards", "branch": "master", "pushed": true}],
      "main_repo_pushed": true,
      "verify": {"match": true, "remote_sha": "7c31f0a", "attempts": 1}
    },
    {
      "remote": "github",
      "submodules": [{"path": "standards", "branch": "master", "pushed": false, "error": "network timeout"}],
      "main_repo_pushed": false,
      "skipped_reason": "submodule push failed for this remote",
      "verify": null
    }
  ],
  "remediation": [
    "git -C standards push github master",
    "git -C . push github master"
  ],
  "notes": ["origin 纵列已完成; 两 remote 当前不一致"]
}
```

---

## 6. 报告格式 (workflow report 片段)

```
╔══════════════════════════════════════════════════════════════╗
║        C.2.5 — MULTI-REMOTE PUSH ENFORCEMENT                 ║
╚══════════════════════════════════════════════════════════════╝

  expected_sha: 7c31f0a   submodules: 1 (standards)
  enforced_remotes: origin, github   (auto-discovered; enforced_remotes 未配置)
  helper: git-remote-helper ✅

  origin: standards ✅  main ✅  verify ✅ (match, attempt 1)
  github: standards ✅  main ✅  verify ✅ (match, attempt 2)

  ✅ C.2.5 PASS — 全部 enforced remote parity 一致 → ready_for: Phase D
```

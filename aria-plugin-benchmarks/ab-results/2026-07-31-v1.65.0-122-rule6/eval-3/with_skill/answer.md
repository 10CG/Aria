# C.2.5 Multi-Remote Push Enforcement — 执行推演 (descriptive)

> 场景前提: Phase C.2 PR 刚合并到 master (aria 子模块的变更已合入)。项目配置双 remote: `origin` (Forgejo) + `github` (GitHub mirror), 仓内还有 1 个子模块。以下按 phase-c-integrator SKILL.md §C.2.5 逐步推演, 不实跑命令。

## 1. 触发条件确认

进入 C.2.5 前先核对两个触发条件:

- Phase C.2 合并成功, 本地 master 已 fast-forward 到 merge 结果 — 场景给定成立。
- 配置 `phase_c_integrator.multi_remote_push.enabled: true` (默认) — 未见显式关闭, 按默认启用。

同时确认职责边界: C.2.5 只负责 **PR 合并后的 master 推送 + 多 remote SHA 验证**; feature 分支推送和 PR 创建是 branch-manager 在 C.2 PR 发起前做的 (仅 origin), 两者不重叠。

## 2. 执行流程 (按 skill 六步)

### 步骤 1: 快照 expected_sha

```bash
expected_sha=$(git rev-parse HEAD)   # 合并后本地 master HEAD
```

这个 SHA 是后续所有 remote 验证的唯一基准 — 后面每个 remote 的 post-push 验证都要与它比对, 不采信 push 命令自身的回执 (push 退出码/回执两个方向都会骗人: 假阴性诱发误 force, 半推造成镜像分叉)。

### 步骤 2: 枚举子模块

```bash
git submodule status --recursive
```

场景中会枚举出 1 个子模块 (记为 SUB, 含其 path 与当前 checkout 的 branch/SHA)。注意本次 PR 的实质变更在 aria 子模块 — 意味着子模块自身的 master 也刚有新 commit, 主仓则是 gitlink bump, 两者都必须同步到全部 enforced remote, 且 **子模块先推、主仓后推** (顺序不能反: 若主仓 gitlink 先到而子模块 commit 未到, GitHub 侧 `clone --recursive` 立即断裂, 即 orphaned gitlink)。

### 步骤 3: 确定 ENFORCED_REMOTES

- 读 skill 级 `enforced_remotes`; 若为 `null` → 继承顶层 `multi_remote.enforced_remotes`; 仍为空 → 自动发现所有 remote。
- 场景配置了 `origin` + `github` 双 remote 且无排除配置, 故 `ENFORCED_REMOTES = [origin, github]`。
- 同时读 `read_only_remotes` 与 `fail_on_partial_push` (默认 `true`) 备用于失败决策。

### 步骤 4: Per-Remote Matrix Gating

对每个 REMOTE 依次执行 (先 origin 后 github), 每个 REMOTE 内部按 "子模块 → 主仓 → 验证" 三段:

**REMOTE = origin (Forgejo):**

- 4a. 遍历子模块: 调用 `git-remote-helper.push_all_remotes(SUB.path, SUB.branch, [origin])`, 把子模块 master 推到 origin。
- 4b. 若子模块推 origin 失败 → 按失败优先级决策 (见第 3 节); 阻断则**跳过 origin 的主仓推送** (保证不产生 "gitlink 先行" 的断裂窗口)。
- 4c. 子模块成功 → `push_all_remotes(main_repo, master, [origin])` 推主仓。
- 4d. 主仓推送成功 → `verify_parity_post_push(main_repo, master, expected_sha, [origin])`: 独立 `git ls-remote origin master` 取远端 SHA 与 `expected_sha` 逐字比对, match 才算数。
- 4e. `match=false` → 同失败优先级决策。

**REMOTE = github (GitHub mirror):** 重复 4a-4e, 目标换成 github。github 是完整 enforced remote (非 read_only), 子模块与主仓同样两段都要推 + 验证。

对子模块处于 **detached HEAD** 的情况 (submodule checkout 常态): 沿用 helper canonical 处理 — 标记 `detached_head: true`, 改用 HEAD SHA 比较做 parity 验证, 警告但不阻断。

### 步骤 5: 全部通过 → 放行

4 个推送单元 (2 remote x 2 repo) 全部 push 成功 **且** 每个 remote 的 ls-remote 验证 SHA 全部与本地一致, C.2.5 才算通过, 进入 Phase D。任何一个 remote 只推成功不验证, 不算完成。

### 步骤 6: 任一阻断 → 输出修复指引

阻断时输出具体失败的 remote + 精确修复命令, 例如:

```bash
git -C <SUB.path> push github master
```

并停在 C.2.5, 不进入 Phase D。

## 3. 失败处理 (决策表 + 典型场景)

失败优先级 (skill 决策表, 从高到低):

| 条件 | 行为 |
|------|------|
| remote 在 `read_only_remotes` | 降级为 warning, 继续 (最高优先级) |
| `fail_on_partial_push: false` 且非 read_only | warning, 继续 |
| `fail_on_partial_push: true` (默认) 且非 read_only | **阻断**, 输出修复命令 |

本场景 github 是可写 mirror、默认 `fail_on_partial_push: true`, 所以对两个 remote 的任何失败都是阻断级。典型情形推演:

**A. 子模块推 github 网络超时 (半推成功, matrix 示例):**

```
origin: SUB 已推 + main 已推 + verify 一致 (完成)
github: SUB 推送失败 (network timeout) → 跳过 main 的 github 推送
```

- origin 侧已完成的推送不回滚 (它是正确状态); github 侧连主仓都不推, 避免 orphaned gitlink。
- 判定为 partial push → 阻断, 报告失败 remote=github + 修复命令 `git -C <SUB.path> push github master`, 随后重推主仓并重新 verify。
- 这正是镜像分叉的高危形态: 处置遵循 memory `feedback_partial_push_creates_mirror_divergence` — 修复时不盲目 force, force-with-lease 前必做前置核验。

**B. push 回执成功但 verify 不一致 (可能 race):**

- 可能是并发写入 (dev-claude2 / aria-runner-bot 同仓接活) 或回执假象。verify 做 **4 次 attempt**, 全部 `match=false` → 默认阻断, 记录 "possible race condition", 交人工/上层判断是重推还是先 fetch 对齐 — 不自动 force。

**C. ls-remote 自身失败 (网络/CF Access 抖动):**

- ls-remote 失败不等于 SHA 不一致, 先重试几次再下结论 (CLAUDE.md 约束 2); 重试穷尽仍失败 → 按验证失败阻断, 不得把 "验证不了" 当 "验证通过"。

**D. git-remote-helper 不可用:**

- 降级检测: `test -f "${ARIA_PLUGIN_ROOT:-aria}/skills/git-remote-helper/SKILL.md"`。不存在 → 走内联降级实现 (不重试, 简化), 但输出 schema 与验证义务不变 — 每 remote 仍要 push + ls-remote SHA 比对。

## 4. 与项目硬约束的对齐点

本场景是 aria 子模块合并, 两条 CLAUDE.md 硬约束都命中:

- **约束 1**: 子模块的这次合并本身必须是本地 `git merge` + 本地双推达成的, 不能是 Forgejo 服务端 merge — 否则本地 master 从未 fast-forward, C.2.5 结构上不会把 merge commit 带到 github, 主仓随后 bump gitlink 即 orphaned gitlink。C.2.5 的 per-remote matrix 正是这条约束的自动化载体。
- **约束 2**: "推后逐个 ls-remote 核验、不信 push 回执" 即步骤 4d 的 `verify_parity_post_push` — 全部 remote SHA 与本地一致才算推成功。

## 5. 输出 (推演的成功态)

```yaml
c25_multi_remote_push:
  expected_sha: "<merge 后 master HEAD>"
  enforced_remotes: [origin, github]
  matrix:
    origin: {submodule: pushed, main: pushed, verify: match}
    github: {submodule: pushed, main: pushed, verify: match}
  verdict: pass
  next: Phase D (或按配置继续 C.2.6 UPM milestone append)
```

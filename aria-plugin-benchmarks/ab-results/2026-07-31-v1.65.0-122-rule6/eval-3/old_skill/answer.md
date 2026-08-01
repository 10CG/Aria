# C.2.5 Multi-Remote Push Enforcement — 执行推演 (descriptive)

> 场景前提: PR 刚合并到 master; 双 remote (origin=Forgejo + github=GitHub mirror); 1 个子模块 (aria)。
> 依据: phase-c-integrator SKILL.md §C.2.5 (v1.15.0+ Multi-Remote Push Enforcement)。

## 0. 触发条件确认

进入 C.2.5 前先确认两个前置:

1. Phase C.2 合并成功 — master 已 fast-forward 到 merge 结果 (场景给定成立)。
2. 配置 `phase_c_integrator.multi_remote_push.enabled: true` (默认值, 未显式关闭即触发)。

同时确认执行边界: C.2.5 只负责「PR 合并后推 master + 多 remote SHA 验证」; feature 分支推送 + PR 创建是 branch-manager 在 C.2 PR 发起前的职责 (仅 origin), 两者不重叠。

## 1. 快照 expected_sha

```bash
expected_sha=$(git rev-parse HEAD)   # 合并后本地 master HEAD
```

这个 SHA 是后续所有 remote 的 post-push 验证基准: 每个 enforced remote 推完后, 其 master 必须与它一致。

## 2. 枚举子模块

```bash
git submodule status --recursive
```

场景给定 1 个子模块 (aria)。记录其 path、当前 checkout 的 SHA、以及所在分支 (若 detached HEAD 则记 `detached_head: true`, 后续用 HEAD SHA 比较)。

## 3. 确定 ENFORCED_REMOTES

解析顺序:

1. skill 级配置 `phase_c_integrator.multi_remote_push.enforced_remotes` — 若非 null 直接采用。
2. 为 null 时继承顶层 `multi_remote.enforced_remotes`。
3. 仍为空时自动发现所有 remote (`git remote`)。

场景下无论走哪条路径, 结果都是 `ENFORCED_REMOTES = [origin, github]`。

同时读取失败决策相关配置: `read_only_remotes` (默认空) 与 `fail_on_partial_push` (默认 true)。

## 4. 降级检测 (git-remote-helper 可用性)

```bash
test -f "${ARIA_PLUGIN_ROOT:-aria}/skills/git-remote-helper/SKILL.md"
```

- 存在 → 用 git-remote-helper 的 `push_all_remotes` / `verify_parity_post_push` (含重试)。
- 不存在 → 内联降级实现 (不重试, 简化版), 但输出 schema 保持一致。

以下按 helper 可用描述。

## 5. Per-Remote Matrix Gating (核心循环)

对每个 REMOTE 依次处理, **子模块先行, 主仓库在后** — 这样即使中途失败, 也不会出现「主仓 gitlink 已到 remote 但子模块 commit 缺失」的 orphaned gitlink (GitHub `clone --recursive` 断裂) 局面。

### REMOTE = origin (Forgejo)

- a. 子模块推送: `git-remote-helper.push_all_remotes(aria_path, aria_branch, [origin])`
  - 内部等效 `git -C aria push origin <branch>` (多仓操作必须 `git -C <path>`, 不 cd)。
- b. 若失败 → 按第 6 节失败优先级决策; 阻断则**跳过 origin 的主仓库推送** (子模块失败挡主仓, 防 orphaned gitlink)。
- c. 子模块成功 → 主仓库推送: `helper.push_all_remotes(main_repo, master, [origin])`。
- d. 主仓推送成功 → post-push 验证: `helper.verify_parity_post_push(main_repo, master, expected_sha, [origin])`
  - 等效 `git ls-remote origin master` 取远端 SHA 与 `expected_sha` 独立比对 — **不信 push 回执/退出码**, 以远端实际 SHA 为准。
- e. `match=false` → 同第 6 节优先级决策。

### REMOTE = github (GitHub mirror)

对 github 重复 a–e: 先 `push_all_remotes(aria_path, aria_branch, [github])`, 成功后 `push_all_remotes(main_repo, master, [github])`, 再 `verify_parity_post_push(..., expected_sha, [github])`。

关键点: **每个 remote 独立 gating**。origin 的成败不影响 github 是否尝试; 一个 remote 上子模块失败只跳过**该 remote** 的主仓推送, 已完成的 remote 不回滚。矩阵示例 (SKILL 原文):

```
origin: aria ✅ main ✅ (已推 + verify 通过)
github: aria ❌ (network timeout) → 跳过 main github; 但 origin 已完成
```

## 6. 失败优先级 (决策表)

任一步 (子模块推送 / 主仓推送 / verify 不匹配) 失败时, 按优先级从高到低:

| 条件 | 行为 |
|------|------|
| 该 remote ∈ `read_only_remotes` | warning 降级, 继续 (最高优先级) |
| `fail_on_partial_push: false` 且非 read_only | warning, 继续 |
| `fail_on_partial_push: true` 且非 read_only (默认) | **阻断**, 输出修复命令 |

场景下 origin 与 github 均非 read_only, 且取默认 `fail_on_partial_push: true` ⇒ 任一失败即阻断 C.2.5 整体 verdict (但不撤销已成功的 remote)。

## 7. 具体失败处理

### 7.1 子模块推送失败 (如 github 网络超时)

- helper 路径含重试; 重试耗尽仍失败 → 记录该 remote 失败。
- 跳过该 remote 的主仓推送 (防 orphaned gitlink)。
- 默认配置下阻断, 输出修复命令:

```bash
git -C aria push github <branch>
git push github master          # 子模块补推成功后再补主仓
git ls-remote github master     # 补推后独立核验 SHA == expected_sha
```

- 此时状态 = 部分推送 (origin 完成, github 落后) = 镜像分叉的前兆; 报告须明示哪个 remote 落后, 不能让 push 半成功被当成全成功静默吞掉。

### 7.2 主仓推送失败 (如 non-fast-forward 拒绝)

- 阻断 + 报告。远程冲突场景提示先 fetch 对比再决定; **不自动 force push** (误判假阴性后 force 是镜像分叉事故的经典成因)。

### 7.3 verify 不匹配 (match=false)

- 重试 verify: **4 次 attempt 全部 match=false → 默认阻断**, 记录 "possible race condition" (可能有并发写入者在 verify 窗口内推了新 commit 到该 remote)。
- 阻断报告包含: remote 名、期望 SHA (`expected_sha`)、远端实际 SHA, 供 operator 判断是 race (远端更新, 通常无害需重新对齐) 还是推送未真正落地。
- ls-remote 自身网络失败不等于不匹配 → 先重试查询, 查询稳定失败才下结论。

### 7.4 子模块 detached HEAD

- 沿用 helper canonical 行为: 标 `detached_head: true`, 用 HEAD SHA 比较进行验证, **警告但不阻断**。

## 8. 收尾与输出

- 两个 remote 的 (子模块 + 主仓 + verify) 全部通过 → C.2.5 成功, 进入 C.2.6 (若 `upm.milestone_driven=true`, 默认 false 则跳过) / Phase D。
- 任一阻断 → C.2.5 返回失败, 输出:
  - 失败 remote 与失败环节 (submodule push / main push / verify)
  - 逐条修复命令 (`git -C <path> push <remote> <branch>` 形式)
  - 各 remote 的 per-remote matrix 状态 (成功/失败/跳过)
  - verify 结果: 每 remote 的 remote SHA vs expected_sha

概念输出形态:

```yaml
c25_result:
  expected_sha: "<merge 后 master HEAD>"
  enforced_remotes: [origin, github]
  matrix:
    origin: {aria: pushed, main: pushed, verify: match}
    github: {aria: pushed, main: pushed, verify: match}
  verdict: pass          # 或 blocked + failed_remote + fix_commands
```

## 9. 不变量小结

1. 推送顺序恒为 子模块 → 主仓 (per remote), 子模块失败挡住该 remote 的主仓推送。
2. 成功判据 = 每个 enforced remote 独立 `ls-remote`/verify SHA 与 expected_sha 一致, 全部一致才算推成功; push 退出码与回执不作为成功依据。
3. 部分成功不回滚、不静默: 明确报告哪个 remote 落后 + 修复命令。
4. verify 4 连败默认阻断并标注 possible race, 不自动 force。
5. helper 缺失时内联降级 (无重试) 但 schema 不变; detached HEAD 子模块警告不阻断。

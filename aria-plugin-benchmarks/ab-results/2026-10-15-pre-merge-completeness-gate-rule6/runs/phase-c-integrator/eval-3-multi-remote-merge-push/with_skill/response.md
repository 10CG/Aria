# Phase C C.2.5 Multi-Remote Push Enforcement — 执行流程与失败处理 (描述性推演)

> **性质声明**: 本次为 benchmark eval 的描述性推演 (descriptive), 按 Skill 规定推演, **未实际执行**任何 `git push` / fetch / forgejo 调用, 未改任何 remote 配置。文中所有命令均为「按 Skill 规定将要执行」的规格化描述。
>
> **推演依据** (全部只读核对过):
> - `aria/skills/phase-c-integrator/SKILL.md` §C.2.5 (v1.15.0+, Multi-Remote Push Enforcement)
> - `aria/skills/git-remote-helper/SKILL.md` + `references/api.md` + `scripts/push_all_remotes.sh` / `scripts/verify_post_push.py` 源码
> - `/home/dev/Aria/.aria/config.json` (无 `multi_remote_push` / `multi_remote` 覆写)
> - `git -C /home/dev/Aria/aria remote -v` 只读核对
> - CLAUDE.md「多远程推送 — 两条硬约束」(owner 裁决 2026-07-20, 根治 Aria #165)

---

## 0. 场景与前提核对

| 项 | 核对结果 |
|---|---|
| 合并对象 | aria 子模块 (`/home/dev/Aria/aria`), PR 刚合并到 master, 本地 master 已含合并结果 (fast-forward) |
| Remotes | `origin` → `ssh://forgejo@forgejo.10cg.pub/10CG/aria-plugin.git` (Forgejo); `github` → `git@github.com:10CG/aria-plugin.git` (GitHub mirror) — 与任务给定一致 |
| 子模块 | 场景给定 1 个 (下文记 `SUB`, 路径 `<SUB_PATH>`); 实际集合以执行时 `git submodule status --recursive` 枚举结果为准 |
| 配置 | `.aria/config.json` 无 `phase_c_integrator.multi_remote_push` 键 → `enabled: true` (默认); 无顶层 `multi_remote.enforced_remotes` → 自动发现所有 remote |
| 触发条件 | C.2 合并成功 (master 已 fast-forward) + `enabled: true` ⇒ **C.2.5 触发** ✅ |
| 前提合规 (CLAUDE.md 约束 1) | aria 是子模块, 其分支合并必须本地 `git merge` + 双推, **禁** Forgejo 服务端 merge。刚完成的合并按此应为本地合并; C.2.5 正是「双推 + post-push SHA 验证」的自动化环节 (CLAUDE.md: 多远程推送由 phase-c-integrator §C.2.5 自动化) |

**职责边界** (不与 branch-manager 重叠): branch-manager 在 PR 发起前只推 feature 分支到 origin; C.2.5 在 PR 合并后推 master 到**所有 enforced remote** 并做多 remote SHA 验证。

---

## 1. Step 0 — helper 可用性检测 (降级判定)

```bash
test -f "${ARIA_PLUGIN_ROOT:-aria}/skills/git-remote-helper/SKILL.md"
```

- **存在** (本仓内该 skill 在场) → 走 git-remote-helper 标准脚本段, 本推演按此描述。
- 不存在 → **内联降级实现** (不重试, 简化实现), 输出 JSON schema 仍与 helper 一致。
- helper 依赖前置: `jq` (JSON 构造, 禁止 Bash 手工拼接) + `python3` (verify 脚本) 必须在场。

## 2. Step 1 — 快照 expected_sha

```bash
expected_sha=$(git -C /home/dev/Aria/aria rev-parse HEAD)
```

- 取**合并后本地 master HEAD** (40-char full SHA), 作为后续所有 post-push 验证的唯一期望值。
- verify 侧接受 full SHA 或 ≥7-char prefix (startswith 匹配, v1.17.6+); 短于 7 字符被拒绝 (collision 防护)。

## 3. Step 2 — 枚举子模块

```bash
git -C /home/dev/Aria/aria submodule status --recursive
```

- 场景结果: 1 个子模块 `SUB`。每个子模块的推送分支取 `SUBMODULE.branch` (枚举所得; 本场景 master; detached 检出语义见 §8.1)。

## 4. Step 3 — 确定 ENFORCED_REMOTES

解析顺序 (SKILL.md §C.2.5 步骤 3):

1. skill 级 `enforced_remotes` == null (未设置)
2. → 继承顶层 `multi_remote.enforced_remotes` — 本项目 config 未设/为空
3. → **自动发现所有 remote**: `git -C /home/dev/Aria/aria remote`

⇒ **ENFORCED_REMOTES = {origin, github}** (枚举序为字母序 github→origin; 两个 remote 在矩阵中彼此独立, 顺序不影响语义)。

## 5. Step 4 — Per-Remote Matrix Gating (核心流程)

对每个 `REMOTE ∈ {origin, github}` **独立**执行 a→e; 一个 remote 的失败不回滚另一个 remote 已完成的推送。

### 5a. 子模块推送 (逐个子模块)

```bash
bash aria/skills/git-remote-helper/scripts/push_all_remotes.sh \
  --repo=<SUB_PATH> --branch=master --remotes=<REMOTE>
```

脚本实际行为 (源码核对):

- 校验 `--repo` 是 git 仓库、本地分支 `master` 存在, 否则 exit 1;
- 快照 `pre_local_head = git -C <SUB_PATH> rev-parse HEAD`;
- 快照 `pre_remote_head = git rev-parse refs/remotes/<REMOTE>/master` (可能为空);
- 执行 `git -C <SUB_PATH> push <REMOTE> master`;
- 读 `post_remote_head = git rev-parse refs/remotes/<REMOTE>/master` (push 成功后 git 本地更新的 tracking ref, **零额外网络**)。

**严格 success 判定 (不信文本回执)**:

```
success = (exit_code == 0) AND (post_remote_head == pre_local_head)
```

- **不解析** "Everything up-to-date" 文本 — 已同步 no-op 场景 (`pre_remote_head == pre_local_head`) 经 SHA 比较自然通过;
- `post_remote_head` 读取失败 → `success=false`, message 置 `post-push verification failed: ...`。

### 5b. 子模块失败 → 失败优先级决策

任一子模块对 REMOTE 推送 `success=false` → 查 §6 决策表。`fail_on_partial_push: true` (默认) 判**阻断**时, **跳过本 REMOTE 的主仓 (aria) 推送**。

理由 (顺序不变量): 每 remote 内**先子模块后主仓** — 主仓 master 中指向子模块的 gitlink 目标 commit 必须先到达该 remote, 否则产生「主仓已推而子模块目标 commit 缺失」的断链状态 (GitHub `clone --recursive` 断裂 / orphaned gitlink 形态, 即 Aria #165 类事故的结构性根源)。

### 5c. 子模块全部成功 → 主仓 (aria) 推送

```bash
bash aria/skills/git-remote-helper/scripts/push_all_remotes.sh \
  --repo=/home/dev/Aria/aria --branch=master --remotes=<REMOTE>
```

同一套严格 success 判定 (`exit_code==0` 且 `post_remote_head == pre_local_head`)。

### 5d. 主仓推送成功 → post-push SHA 权威验证

```bash
python3 aria/skills/git-remote-helper/scripts/verify_post_push.py \
  --repo=/home/dev/Aria/aria --branch=master \
  --expected-sha=<expected_sha> --remotes=<REMOTE>
```

- 重试 schedule `[0, 2, 4, 8]` 秒 (`--max-retries=3 --initial-backoff=2` 默认, 共 4 次 attempt);
- 每次 attempt 执行 `git -C /home/dev/Aria/aria ls-remote <REMOTE> refs/heads/master` (`--timeout=15`, v1.15.1 默认, 适配 Forgejo SSH over Cloudflare Access ~8s 延迟);
- SHA 匹配 (startswith) → **提前返回** `match: true`; attempt 耗尽 → `match: false` + reason;
- **per-remote 时间上界: 4×15s + 14s sleep = 74s**;
- 退出码: `all_match=true` → 0; 否则 1。

这一步是 CLAUDE.md **约束 2** 的机制化实现:「双推后对每个 remote 独立 `git ls-remote` 取 SHA 与本地比对, 全部一致才算推成功; push 退出码/回执两个方向都会骗人; ls-remote 自身失败 → 重试几次再下结论」— 4 次 attempt + 指数退避正是「重试几次再下结论」, 74s 窗口吸收 Forgejo/GitHub 10-30s 复制延迟。

### 5e. verify match=false → 同失败优先级决策

进入 §6 决策表处理 (含 race condition 判定, 见 §6.3)。

## 6. Step 5/6 — 汇总与失败处理

全部 remote 处理完毕且全部通过 → C.2.5 完成, 进入 Phase D (C.2.6 `upm.milestone_driven=false` 默认跳过)。
任一阻断 → 输出具体失败 remote + 修复命令, Phase C 不进 Phase D。

### 6.1 失败优先级决策表 (SKILL.md §C.2.5 原表)

| 条件 | 行为 |
|------|------|
| remote ∈ `read_only_remotes` | warning 降级, 继续 (最高优先级) |
| `fail_on_partial_push: false` + 非 read_only | warning, 继续 |
| `fail_on_partial_push: true` (**默认**) + 非 read_only | **阻断**, 输出修复命令 |

### 6.2 push 层错误枚举 (push_all_remotes 输出)

| 场景 | exit_code | success | message |
|------|-----------|---------|---------|
| 推送成功 (new commits) | 0 | true | `<old>..<new>  master -> master` |
| 已同步 (no-op) | 0 | true | `Everything up-to-date` (仍由 SHA 判定) |
| 网络错误 | 非0 | false | git 错误信息 |
| 认证失败 | 128 | false | git 认证错误 |
| post_remote_head 读取失败 | 0 | **false** | `post-push verification failed: ...` |
| remote 不存在 | 1 | false | `Unknown remote "<name>"` |

### 6.3 verify 层 reason 枚举 (match=false 时) 与 race condition

| reason | 触发条件 |
|--------|---------|
| `sha_mismatch` | 全部 attempt 正常完成但 SHA 不匹配 |
| `network_timeout` | 最后一次 attempt 超时 |
| `auth_failed` | 最后一次 attempt 返回 exit 128 |
| `error` | 其他非零 exit code |

**race condition 处理**: verify 4 次 attempt 全部 `match=false` → 默认**阻断**, 记录 `"possible race condition"` (远端复制延迟超出 backoff 窗口, 或推送实际未生效)。处置纪律:

- **不立即 force-push**。push 回执两个方向都会骗人 — 假阴性 (回执报失败但实际已推上) 诱发误 force; 半推造成镜像分叉 (#165)。分叉后的处置 (含 force-with-lease 前的三项前置核验) 按 memory `feedback_partial_push_creates_mirror_divergence` 流程执行;
- 先独立复核 `git ls-remote <REMOTE> master` (约束 2: ls-remote 自身失败也要重试几次再下结论), 与本地 `expected_sha` 比对;
- 确认远端落后 → 用修复命令重推 (非必要不 force); 确认分叉 → 按 memory 流程核验后处置并上报。

### 6.4 阻断时的输出

输出具体失败 remote + 修复命令 (SKILL.md §C.2.5 步骤 6):

```
失败: REMOTE=<remote>, 对象=<SUB_PATH> 或 /home/dev/Aria/aria
修复: git -C <SUB_PATH> push <REMOTE> master
      git -C /home/dev/Aria/aria push <REMOTE> master
```

修复后重跑 C.2.5 (或对剩余未完成部分补推 + 重新 verify)。

---

## 7. 成功路径全景 (矩阵示例)

全绿形态:

```
REMOTE=origin:  SUB ✅ (push_all_remotes: success) → aria ✅ → verify ✅ (attempts=1)
REMOTE=github:  SUB ✅ → aria ✅ → verify ✅ (attempts=2, 吸收 mirror 复制延迟)
→ 两 remote 全过 → C.2.5 完成 → (C.2.6 默认跳过) → Phase D
```

部分失败形态 (SKILL.md 原例同构推广到 1 子模块):

```
origin:  SUB ✅  aria ✅ (已完成, 不受影响)
github:  SUB ❌ (network timeout) → 跳过 aria 的 github 推送
→ fail_on_partial_push=true (默认) ⇒ 阻断 + 输出修复命令 git -C <SUB_PATH> push github master
```

---

## 8. 边界与特殊场景

1. **子模块 detached HEAD**: 沿用 helper canonical 处理 (`detached_head: true` + 用 HEAD SHA 做各 remote 比较), **警告但不阻断**。实操守则 (memory `feedback_submodule_detached_head_push_head_colon_master`): 子模块 detached HEAD 时本地 master 可能陈旧 — push 用 `HEAD:master`, gate/diff 前先 `branch -f master origin/master` 对齐。(推演提示, 本 eval 不执行。)
2. **post_remote_head 为空 / tracking ref 缺失**: 按 §6.2 表 `success=false` 处理, 不当作「已同步」。
3. **验证深度**: C.2.5 契约中权威 ls-remote 验证 (5d) 规定于**被合并仓** (此处 = aria); 子模块推送由 push_all_remotes 的严格 SHA 判定 (本地 tracking ref) 覆盖。如需对子模块追加权威 ls-remote 复核, `verify_post_push.py` 本身 repo-generic (`--repo` 可传子模块路径 + 子模块自身 expected SHA), 属契约外可加做的强化, 非本步骤义务。
4. **主仓 gitlink bump 不在本次 C.2.5 范围**: aria 子模块双推完成后, Aria 主仓的 gitlink bump + 主仓自身双推是**后续独立步骤** (多仓 ship 顺序: submodule 先 merge→gitlink), 不由 aria 仓内这次 C.2.5 承担。
5. **推完即核, 不信回执**: 每 remote 的「完成」定义 = push 严格 success **且** (主仓) verify match, 二者缺一该 remote 未闭环。

## 9. 产出契约 (JSON)

**push_all_remotes.sh** (每个 repo × remote 一条):

```json
{
  "repo_path": "<SUB_PATH> 或 /home/dev/Aria/aria",
  "branch": "master",
  "pre_local_head": "<full-sha>",
  "results": [
    {
      "remote": "origin",
      "exit_code": 0,
      "success": true,
      "pre_remote_head": "<old-or-same>",
      "post_remote_head": "<full-sha>",
      "message": "<old>..<new>  master -> master"
    }
  ],
  "all_success": true
}
```

**verify_post_push.py** (主仓 × remote):

```json
{
  "repo_path": "/home/dev/Aria/aria",
  "branch": "master",
  "expected_sha": "<full-sha>",
  "max_retries": 3,
  "retry_schedule_seconds": [0.0, 2.0, 4.0, 8.0],
  "results": [
    { "remote": "origin",  "actual_sha": "<full-sha>", "match": true, "attempts": 1, "total_seconds": 0.31 },
    { "remote": "github",  "actual_sha": "<full-sha>", "match": true, "attempts": 2, "total_seconds": 2.43 }
  ],
  "all_match": true
}
```

C.2.5 最终判定: `ENFORCED_REMOTES` 中每个 remote 均满足「子模块 push success + 主仓 push success + 主仓 verify match」→ 通过, 进入 Phase D; 否则按 §6 阻断并输出修复命令。

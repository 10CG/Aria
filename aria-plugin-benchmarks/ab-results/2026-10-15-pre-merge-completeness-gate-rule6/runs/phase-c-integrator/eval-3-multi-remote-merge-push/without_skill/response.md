# Phase C C.2.5 — Multi-Remote Push Enforcement (描述性推演)

> **产出形态**: descriptive walkthrough。以下全部命令均为「按 skill 规定将执行什么」的描述, 本次 eval 未实际执行任何 git 读网络/写操作、未调用任何脚本。

## 0. 场景与前提

| 项 | 值 |
|---|---|
| 触发点 | Phase C.2 合并成功, 本地 `master` 已 fast-forward (PR 刚合并到 master) |
| 执行对象 | aria 子模块仓 (工作副本如 `/home/dev/Aria/aria`) |
| remotes | `origin` (Forgejo, `ssh://forgejo@forgejo.10cg.pub/10CG/aria-plugin.git`) + `github` (GitHub mirror, `git@github.com:10CG/aria-plugin.git`) |
| 子模块 | 1 个, 下文记 `SUB` (path 取 `git submodule status --recursive` 输出; 推送分支取 `.gitmodules` 的 `submodule.<name>.branch`, 未配置时缺省 `master`) |
| 主干名 | `master` — 不是 `main` (#137 教训: 分支字面量抄错会静默恒放行/恒空结果, 本流程所有 `--branch` 均写真值 `master`) |

**命名空间澄清**: 本步骤是 phase-c-integrator (orchestrator tier) 的 §C.2.5 "Multi-Remote Push Enforcement", 与 branch-manager 内部实现层同样编号的 C.2.5 "merge" 是同名不同 tier、语义独立 (与 SKILL.md §C.2.4 的澄清同款)。

**与项目两条硬约束 (CLAUDE.md「多远程推送」) 的对应**:
- **约束 1** (子模块合并一律本地做, 禁 Forgejo 服务端合并): 本场景发生在 aria 子模块内, merge 必须是本地 `git merge` —— C.2.5 正是该约束「本地双推」半边的机制化。前置事实: 本地 master 已指向 merge 结果。
- **约束 2** (推后逐个 `ls-remote` 核验, 不信 push 回执): 由步骤 4d 的 `verify_parity_post_push` 落地 —— 对每个 remote 独立 `git ls-remote` 取 SHA 与本地 HEAD 比对; `push_all_remotes` 内建的严格 success 判定同样不 parse 文本回执。

## 1. 配置解析 (config-loader)

执行前读 `.aria/config.json`, 缺失用 DEFAULTS.json 默认值 (实测 aria 子模块仓无自身 `.aria/config.json` → 全走默认):

```
phase_c_integrator.multi_remote_push.enabled              = true    (默认) → 触发条件满足
phase_c_integrator.multi_remote_push.enforced_remotes     = null    → 继承顶层 multi_remote.enforced_remotes = [] (默认空)
                                                          → 空 → 自动发现所有 remote
phase_c_integrator.multi_remote_push.fail_on_partial_push = true    (默认)
phase_c_integrator.multi_remote_push.post_push_verify     = { enabled: true, max_retries: 3,
                                                              initial_backoff_seconds: 2,
                                                              timeout_seconds: 15,
                                                              max_per_remote_seconds: 74 }
```

→ **ENFORCED_REMOTES = 自动发现 = `{origin, github}`**; `read_only_remotes` 为空。

## 2. Helper 可用性检测 (降级策略)

```bash
test -f "${ARIA_PLUGIN_ROOT:-aria}/skills/git-remote-helper/SKILL.md"
```

Aria 仓内插件完整安装 → helper 可用, 走脚本路径 (`push_all_remotes.sh` + `verify_post_push.py`)。不可用时按 SKILL 规定用**内联降级实现** (不重试, 简化), 但输出 JSON schema 必须与 helper canonical 完全一致 (schema.md §Schema 一致性要求)。

## 3. 执行流程

```
快照 expected_sha
  └─ 枚举子模块 (1 个: SUB)
       └─ ENFORCED_REMOTES = {origin, github}
            ├─ REMOTE=origin 腿:  SUB push → (成功) → aria main push → (成功) → verify(ls-remote)
            └─ REMOTE=github 腿: SUB push → (成功) → aria main push → (成功) → verify(ls-remote)
                 (任一环失败 → §5 决策表; 阻断则跳过本腿后续环节)
全通过 → C.2.6 (默认 off) → Phase D
```

**步骤 1 — 快照期望 SHA** (必须在任何 push 之前取, 之后所有比较都用这个冻结值):

```bash
expected_sha=$(git -C /home/dev/Aria/aria rev-parse HEAD)
```

**步骤 2 — 枚举子模块**:

```bash
git -C /home/dev/Aria/aria submodule status --recursive   # → 1 个: SUB
```

**步骤 3 — 确定 ENFORCED_REMOTES**: 见 §1 → `{origin, github}`。

**步骤 4 — Per-Remote Matrix Gating** (对每个 `REMOTE ∈ {origin, github}` 各跑一腿; 腿间相互独立、互不回滚; **同一腿内必须子模块先于主仓** —— 主仓 gitlink 若先推, 其指向的子模块 commit 在该 remote 上尚不存在, `git clone --recursive` 即断链 (2026-07-14 orphaned gitlink 事故根因)):

a. **先推子模块** (单 remote 白名单调用, 便于按腿门控):

```bash
bash aria/skills/git-remote-helper/scripts/push_all_remotes.sh \
  --repo=<SUB.path> --branch=master --remotes=<REMOTE>
```

脚本内部行为 (读源码确认):
- 预检: `--repo` 是 git 仓、`master` 本地存在, 否则直接 exit 1 (腿失败);
- 快照 `pre_local_head = rev-parse HEAD`; `pre_remote_head = refs/remotes/<REMOTE>/master` (无 tracking ref 时 null);
- 执行 `git -C <repo> push <REMOTE> master`;
- push 后读 `post_remote_head = refs/remotes/<REMOTE>/master` (本地 ref, 成功 push 后 git 自动更新, 无额外网络往返);
- **严格 success 判定** (不 parse 输出文本): `success = (exit_code == 0) AND (post_remote_head == pre_local_head)`。"Everything up-to-date" 的 no-op 场景天然兼容 (此时 post == pre_local 仍成立); 读取不到 post ref → success=false + message `post-push verification failed: ...`;
- 输出 canonical JSON (schema 2, 见 §4)。

b. **子模块腿任一失败** → 查 §5.1 失败优先级决策表; 阻断 → **跳过本 REMOTE 的主仓推送**。

c. **子模块全成功 → 推主仓** (aria 仓自身):

```bash
bash aria/skills/git-remote-helper/scripts/push_all_remotes.sh \
  --repo=/home/dev/Aria/aria --branch=master --remotes=<REMOTE>
```

d. **主仓推送成功 → post-push SHA 权威核验** (按 SKILL 文义, `verify_parity_post_push` 仅对 main_repo 执行; 子模块腿的保障来自 push_all_remotes 的严格判定):

```bash
python3 aria/skills/git-remote-helper/scripts/verify_post_push.py \
  --repo=/home/dev/Aria/aria --branch=master \
  --expected-sha=<expected_sha> --remotes=<REMOTE> \
  --max-retries=3 --initial-backoff=2 --timeout=15
```

`verify_post_push.py` 行为 (读源码确认):
- 重试 schedule = `[0, 2, 4, 8]` (立即 + 2s + 4s + 8s, 共 4 attempts); 每次 attempt 执行 `git ls-remote <REMOTE> refs/heads/master`, timeout 15s/次 (v1.15.1 默认, 适配 Forgejo SSH over Cloudflare Access ~8s 延迟);
- SHA 匹配 → early exit `match=true` (单 remote 的重试循环内); 全部耗尽 → `match=false` + `reason` (枚举见 §5.3);
- `--expected-sha` 接受 full 40-char 或 ≥7-char prefix (startswith 匹配, <7 拒绝为歧义);
- per-remote 时间上界 **74s** (4×15s + 14s sleep); exit code: `0` = all_match, `1` = 否;
- 存在意义: Forgejo/GitHub 镜像复制延迟 10-30s, push 退出码与本地 tracking ref 都可能是假象 —— 唯独立 ls-remote 读数作数 (约束 2)。

e. **verify match=false** → 同 §5.1 决策表。

**步骤 5 — 所有 REMOTE 处理完毕且全部通过** → C.2.5 完成 → C.2.6 (`upm.milestone_driven` 默认 false → 跳过) → 进入 Phase D。

**步骤 6 — 任一阻断** → 输出具体失败 remote + 修复命令 (SKILL 原文格式):

```bash
git -C <path> push <remote> <branch>
```

## 4. 成功路径输出示例 (helper canonical JSON)

`push_all_remotes` (主仓 github 腿, schema 2):

```json
{
  "repo_path": "/home/dev/Aria/aria",
  "branch": "master",
  "pre_local_head": "19f2861a3b4c...",
  "results": [
    { "remote": "github", "exit_code": 0, "success": true,
      "pre_remote_head": "f55e130a1b2c...", "post_remote_head": "19f2861a3b4c...",
      "message": "f55e130..19f2861  master -> master" }
  ],
  "all_success": true
}
```

`verify_parity_post_push` (schema 3; 实际按腿各调一次, 此处合并示意):

```json
{
  "repo_path": "/home/dev/Aria/aria",
  "branch": "master",
  "expected_sha": "19f2861a3b4c...",
  "max_retries": 3,
  "retry_schedule_seconds": [0, 2, 4, 8],
  "results": [
    { "remote": "origin",  "actual_sha": "19f2861a3b4c...", "match": true, "attempts": 1, "total_seconds": 0.31 },
    { "remote": "github",  "actual_sha": "19f2861a3b4c...", "match": true, "attempts": 2, "total_seconds": 2.43 }
  ],
  "all_match": true
}
```

## 5. 失败处理

### 5.1 失败优先级决策表 (SKILL.md §C.2.5 原表)

| 条件 | 行为 |
|------|------|
| remote ∈ `read_only_remotes` | warning 降级, 继续 (最高优先级) |
| `fail_on_partial_push: false` + 非 read_only | warning, 继续 |
| `fail_on_partial_push: true` + 非 read_only (**默认**) | **阻断**, 输出修复命令 |

本场景默认配置: 两 remote 均非 read_only、`fail_on_partial_push=true` → 任何腿失败即阻断。

### 5.2 Per-Remote Matrix 半失败形态 (SKILL 示例适配为 1 子模块)

```
origin:  SUB ✅ → aria main ✅ → verify ✅            (本腿完成)
github:  SUB ❌ (network timeout) → 跳过 aria main@github; verify@github 不执行
```

- 一个 remote 阻断**不回滚**已完成的另一个 remote (origin 已推保持已推; SKILL 矩阵示例明示 "origin 已完成");
- 最终 C.2.5 return failure, 输出失败 leg (github/SUB) + 修复命令 `git -C <SUB.path> push github master`;
- 修复后重跑 C.2.5 幂等: 已同步腿的 push 是 no-op, api.md 错误表明示 no-op → `exit_code=0, success=true`。

### 5.3 verify (post-push SHA) 失败的 reason 枚举与处置

| reason | 触发条件 | 处置 |
|--------|---------|------|
| `sha_mismatch` | 4 attempts 全部正常完成但 SHA 不匹配 (含远端分支不存在 → `actual_sha=null` 也归此) | 默认**阻断**, 记录 "possible race condition" (SKILL 明文); 属真分叉/半推信号 → 后续按镜像分叉处置 (协调合并, **不得直觉性 force push**) |
| `network_timeout` | 最后一次 attempt 超时 (exit 124 语义) | ls-remote 自身失败先重试再下结论 —— verify 已内建 4 attempts 退避重试, 仍失败按阻断上报, 不凭单次超时下「远端坏了」结论 |
| `auth_failed` | 最后一次 attempt exit 128 | 检查凭据面 (Forgejo SSH over CF Access / github SSH key) |
| `error` | 其他非零 exit | 按 message 定位 |

Race condition 处理 (SKILL 原文): verify 4 次 attempt 全部 match=false 默认阻断并记录 "possible race condition" —— 不静默放过。

### 5.4 子模块 detached HEAD

子模块默认即 detached HEAD (正常态)。按 helper canonical: 标注 `detached_head: true`, 比较退化为 **HEAD SHA vs remote HEAD SHA**, **警告但不阻断**; 推送目标分支从父仓 `.gitmodules` `branch=` 字段取。若因本地 `master` ref 陈旧导致严格判定失败 (push 出去的是旧 master 而非 HEAD), 修复命令应用 `git -C <SUB.path> push <remote> HEAD:master` (或先 `git -C <SUB.path> branch -f master <HEAD-SHA>` 再常规推)。

### 5.5 其他降级/边界

- helper 不可用 → 内联降级实现 (无重试, 简化), JSON schema 保持一致;
- `post_push_verify.enabled=false` → 跳过权威核验, 只剩 push_all_remotes 的内建严格判定 (等于放弃约束 2 的独立读数, 不建议);
- `push_all_remotes` 遇 `Unknown remote "<name>"` (remote 不存在) → 该腿 `exit_code=1, success=false`, 走决策表; `--branch` 本地不存在 → 脚本直接 exit 1;
- 推送 exit 128 (认证失败) / 非 0 (网络) → 该腿 success=false + git 错误信息 (截断 512 字符), 走决策表。

## 6. 范围边界 (本步骤不做的事)

- 只覆盖本仓 (aria 子模块) 及其 1 个子模块的多 remote 推送与核验; **父仓 (Aria 主仓) 的 gitlink bump** 属父仓自己的下一个 cycle, 不在 C.2.5 范围内 (对应「ship 后子模块 behind … gitlink 归下一发版者」的分工惯例);
- C.2.4 (pre-merge CI gate) 与 C.2.4.5 (submodule pointer regression gate) 已在 merge 前完成, 本步不重复;
- 分支清理 (删 feature 分支) 是 branch-manager 职责, 非 C.2.5;
- C.2.5 自身**永不 force push、永不回滚远端** —— 失败时只阻断 + 输出修复命令, 修复动作由人/下轮执行。

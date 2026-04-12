# Phase C.2.5 Multi-Remote Push Enforcement — 执行流程描述

**评估**: eval-int-3-multi-remote-merge-push (with_skill)
**触发场景**: PR 已合并到 master, 主仓库 + 1 个子模块 (aria), 双 remote (origin=Forgejo, github=GitHub mirror)
**依据**:
- `aria/skills/phase-c-integrator/SKILL.md` §C.2.5 Multi-Remote Push Enforcement (v1.15.0+)
- `aria/skills/git-remote-helper/SKILL.md` (依赖的 helper 契约)

> **声明**: 本文档仅描述 C.2.5 完整执行流程, **不执行实际 push**。

---

## 0. 前置状态

```
主仓库: /home/dev/Aria
  remotes: origin (Forgejo, 可写), github (GitHub mirror, 可写)
  分支: master (PR 合并后已本地 fast-forward)
  子模块: aria → /home/dev/Aria/aria (指针已更新, 即将随主仓库一起推)

子模块: /home/dev/Aria/aria
  remotes: origin (Forgejo), github (GitHub mirror)
  分支: master
```

假设 Phase C.2 branch-manager 已完成:
- PR 创建、审计 (pre_merge 如启用)、合并动作均成功
- **本地 master 已 fast-forward 到 PR 合并 commit**
- **尚未推送 master 到任何 remote**

---

## 1. 触发条件与边界 (Why This Step Exists)

C.2.5 填补了 branch-manager 留下的空白:

| Skill | 范围 | 推送对象 | Remote |
|-------|------|---------|--------|
| branch-manager (C.2 PR 发起前) | feature 分支 | feature/xxx | **仅 origin** |
| phase-c-integrator C.2.5 (PR 合并后) | master + 所有子模块 | master | **所有 enforced remote** |

没有 C.2.5 时的历史事故 (CLAUDE.md 记录):
> 2026-04-10: aria v1.11.1 发版后未推送 GitHub, 市场拉取停留在 v1.11.0。

C.2.5 的核心价值: **保证 Forgejo 主仓 + GitHub mirror 的 master 指针在 PR 合并后同步**, 防止插件市场版本滞后。

---

## 2. 完整执行流程 (描述, 不执行)

### Step 1 — Snapshot `expected_sha`

```bash
# 主仓库
expected_sha_main=$(git -C /home/dev/Aria rev-parse HEAD)
# 子模块 (合并时 aria 指针随主仓更新, 但子模块本身需单独推)
expected_sha_aria=$(git -C /home/dev/Aria/aria rev-parse HEAD)
```

**为什么先 snapshot**: `expected_sha` 是 post-push verification 的"真理来源"。如果后续 push 过程中有其他 hook 或并发写入, 我们仍以 merge 完成那一刻的 HEAD 作为期望值。

### Step 2 — 枚举子模块

```bash
git -C /home/dev/Aria submodule status --recursive
# 预期输出: <sha> aria (<tag>)  — 1 个子模块
```

子模块列表: `[{path: /home/dev/Aria/aria, branch: master}]`

### Step 3 — 确定 `ENFORCED_REMOTES`

依据 SKILL.md:
> skill 级 `enforced_remotes == null` 时继承顶层 `multi_remote.enforced_remotes`, 空则自动发现所有 remote

读取 `.aria/config.json`:
- 若 `phase_c_integrator.multi_remote_push.enforced_remotes` 显式配置 → 使用该列表
- 若继承自顶层 `multi_remote.enforced_remotes` → 使用顶层
- 若均为空 → `git remote` 自动发现 → `[origin, github]`

本评估假设最终 `ENFORCED_REMOTES = [origin, github]`。

同时读取:
- `read_only_remotes`: `[]` (github 虽是 mirror, 但仍需写入, 不在该列表)
- `fail_on_partial_push`: `true` (默认)

### Step 4 — Per-Remote Matrix Gating

**核心设计**: 外层循环 per-remote, 内层子模块优先, 主仓最后。失败早停只作用于**当前 remote**, 不影响其它 remote。

```
for REMOTE in ENFORCED_REMOTES:  # [origin, github]
  4a. 推送所有子模块到 REMOTE
  4b. 有失败 → 失败优先级决策 → 决定是否跳过 4c/4d
  4c. 推送主仓到 REMOTE
  4d. verify_parity_post_push (主仓 + REMOTE, expected_sha)
  4e. verify 失败 → 失败优先级决策 (同 4b)
```

#### Iteration 1: `REMOTE = origin` (Forgejo)

**4a. 子模块推 origin**:
```bash
bash aria/skills/git-remote-helper/scripts/push_all_remotes.sh \
  --repo=/home/dev/Aria/aria \
  --branch=master \
  --remotes=origin
```
期望输出 JSON:
```json
{
  "repo": "/home/dev/Aria/aria",
  "branch": "master",
  "remotes": [
    {
      "name": "origin",
      "exit_code": 0,
      "pre_remote_head": "<old-sha>",
      "post_remote_head": "<expected_sha_aria>",
      "pre_local_head": "<expected_sha_aria>",
      "success": true
    }
  ]
}
```
`success` 严格判定: `exit_code==0 AND post_remote_head == pre_local_head` (不信任 "Everything up-to-date" 文本)。

**4b**: 子模块成功 → 继续。

**4c. 主仓推 origin**:
```bash
bash aria/skills/git-remote-helper/scripts/push_all_remotes.sh \
  --repo=/home/dev/Aria \
  --branch=master \
  --remotes=origin
```

**4d. Post-push verify (origin)**:
```bash
python3 aria/skills/git-remote-helper/scripts/verify_post_push.py \
  --repo=/home/dev/Aria \
  --branch=master \
  --expected-sha=$expected_sha_main \
  --max-retries=3 \
  --initial-backoff=2 \
  --timeout=5 \
  --remotes=origin
```
重试策略: 立即 + 2s + 4s + 8s = 4 次 attempt (应对 Forgejo 复制延迟, per-remote 时间上界 34s)。
- `match=true` → origin 完成
- `match=false` 4 次全部 → 标记 "possible race condition", 进入失败决策

#### Iteration 2: `REMOTE = github` (GitHub mirror)

重复 4a–4d, 独立处理。**即使 origin 全绿, github 也必须单独尝试并 verify。**

### Step 5 — 全部通过 → 进入 Phase D

所有 REMOTE × (子模块 + 主仓) × (push + verify) 全部 match=true, 输出 context 给 phase-d-closer:
```yaml
c_2_5:
  enforced_remotes: [origin, github]
  submodules_pushed: [aria]
  verify_results:
    origin: { main: match, aria: match }
    github: { main: match, aria: match }
```

### Step 6 — 任一阻断 → 输出修复命令

失败时输出具体 `remote + repo + branch` 及对应修复命令。

---

## 3. 失败优先级决策表 (关键)

当 push 或 verify 失败时, 决策顺序严格按优先级:

| 优先级 | 条件 | 行为 | 说明 |
|-------|------|------|------|
| **P1 (最高)** | `remote ∈ read_only_remotes` | **warning 降级, 继续** | 即使 `fail_on_partial_push=true` 也降级 |
| **P2** | `fail_on_partial_push: false` AND remote ∉ read_only | warning, 继续 | 宽容模式 |
| **P3 (默认)** | `fail_on_partial_push: true` AND remote ∉ read_only | **阻断**, 输出修复命令 | 严格模式 |

**本评估配置**: `read_only_remotes=[]`, `fail_on_partial_push=true` → 任意失败直接走 P3 阻断。

---

## 4. 失败处理场景 (SKILL.md §Per-Remote Matrix 示例对应)

### 场景 A: 子模块 aria 推 github 失败 (network timeout)

执行序:
```
origin:  aria ✅  main ✅  verify ✅   (Iteration 1 全绿)
github:  aria ❌ (exit!=0 或 post_remote_head != pre_local_head)
         └─ 失败决策 P3: 阻断 → **跳过 Iteration 2 的 4c/4d (主仓不推 github)**
```

输出:
```
FAIL: submodule aria failed to push github
  exit_code: <code>
  reason: network_timeout (或 specific error)
修复命令:
  git -C /home/dev/Aria/aria push github master
  # 随后手动重试主仓:
  git -C /home/dev/Aria push github master
  python3 aria/skills/git-remote-helper/scripts/verify_post_push.py \
    --repo=/home/dev/Aria --branch=master \
    --expected-sha=$expected_sha_main --remotes=github
```

**注意**: origin 已完成, 不回滚。Phase D 不进入, 直到人工修复后重跑 C.2.5 (或仅补推 github)。

### 场景 B: 主仓推 origin 成功但 verify 4 次全失败 (可能的 race condition)

```
origin:  aria ✅  main push ✅  verify ❌×4  → "possible race condition"
```

决策: P3 阻断 (非 read_only, fail_on_partial_push=true), 输出诊断日志 + 手动验证命令:
```bash
git -C /home/dev/Aria ls-remote origin master
# 若实际 SHA == expected_sha → verify.py 的 ls-remote 出现了短暂延迟, 可重跑
# 若实际 SHA != expected_sha → 有其他 push 介入, 需人工调查
```

### 场景 C: 子模块 detached HEAD

SKILL.md 明确: "沿用 helper canonical (`detached_head: true` + HEAD SHA 比较), **警告但不阻断**"。

本评估 aria 子模块假设在 master 分支, 不触发此路径。若触发, helper 会在 JSON 输出 `detached_head: true`, C.2.5 以 warning 继续。

### 场景 D: github 配置为 read_only (假设场景)

若 `.aria/config.json` 设 `read_only_remotes: ["github"]`:
- github push 失败 → P1 (read_only) → warning, 继续
- 最终 Phase D 照常进入, 输出警告日志提示 github 滞后

**本评估实际配置不触发 P1**。

---

## 5. 降级策略 (helper 不可用)

SKILL.md §降级策略:
```bash
test -f aria/skills/git-remote-helper/SKILL.md
```
- 存在 → 调用 helper 的 3 个脚本 (`check_parity.sh` / `push_all_remotes.sh` / `verify_post_push.py`)
- 不存在 → C.2.5 内联实现同样逻辑 (简化: 不重试, 单次 verify), **JSON schema 仍一致**

本评估 helper 存在, 使用正常路径。

---

## 6. 与 branch-manager 的边界 (不重叠保证)

SKILL.md 明确划线:

| 阶段 | 谁推 | 推什么 | 推到哪 |
|------|------|-------|--------|
| C.2 PR 创建前 | branch-manager | feature 分支 | **仅 origin** (PR 目标仓) |
| C.2 合并后 (C.2.5) | phase-c-integrator | **master + 所有子模块 master** | **所有 enforced remote** |

C.2.5 **不重复** branch-manager 的 feature 分支 push。

---

## 7. 本评估预期结果 (假设全绿路径)

**输入状态**:
- 主仓 master HEAD = `$expected_sha_main`
- aria 子模块 master HEAD = `$expected_sha_aria`
- origin + github 均可写, 网络正常

**预期执行矩阵**:
```
              origin           github
aria   sub    push ✅          push ✅
main   repo   push ✅          push ✅
              verify ✅         verify ✅
```

**预期输出**:
```yaml
success: true
phase: C.2.5
enforced_remotes: [origin, github]
submodules: [aria]
results:
  origin:
    aria: { pushed: true, verified: true }
    main: { pushed: true, verified: true, expected_sha: "<sha>" }
  github:
    aria: { pushed: true, verified: true }
    main: { pushed: true, verified: true, expected_sha: "<sha>" }
ready_for: Phase D
```

---

## 8. 关键正确性属性 (Invariants)

1. **Pre-push snapshot 不变性**: `expected_sha` 在 Step 1 快照后整个 C.2.5 周期不重算。
2. **Per-remote 独立性**: origin 失败不影响 github 尝试, 反之亦然 (matrix gating 内层才依赖)。
3. **子模块先于主仓**: 主仓推送前子模块必须先推到同一 remote, 避免主仓指针指向远程不存在的 commit (dangling pointer)。
4. **Verify 权威性**: 不信任 `git push` 的文本输出, 必须 `git ls-remote` 查询 post-push SHA。
5. **失败可恢复性**: 所有失败输出精确修复命令 (`git -C <path> push <remote> <branch>`), 人工可断点续推。
6. **空配置安全默认**: `enforced_remotes` 缺省 → 自动发现所有 remote → 不漏掉任何已配置的镜像。

---

## 9. 执行前检查清单 (执行时参考, 本次不执行)

- [ ] `expected_sha` 已 snapshot (主仓 + 子模块)
- [ ] `git submodule status --recursive` 列表正确
- [ ] `.aria/config.json` 已读取 (或使用默认值)
- [ ] `ENFORCED_REMOTES` 确定为 `[origin, github]`
- [ ] `jq` / `python3` 可用 (helper 依赖)
- [ ] helper 脚本存在 (`test -f .../git-remote-helper/SKILL.md` → 使用; 否则降级)
- [ ] Cloudflare Access 配置就绪 (Forgejo 访问, SKILL.md 提及由 branch-manager 处理, C.2.5 沿用环境)

---

## 结论

C.2.5 通过 **Per-Remote Matrix Gating** + **失败优先级决策表** + **权威 post-push verify** 三层机制, 保证多 remote + 子模块场景下 master 指针的强一致推送。本评估 (with_skill) 下 LLM 可完整复述该流程、识别 3 个 helper 脚本的职责边界、区分 P1/P2/P3 失败决策, 并在子模块+主仓+双 remote 的具体案例中正确给出 2×2 执行矩阵与修复命令。

**实际 push 未执行** — 本文档仅为流程描述与决策演练, 符合评估任务要求。

# phase-c-integrator 多远程推送强制 — Task Plan

> **Scope**: Layer 2 (phase-c-integrator) + Layer 3 (git-remote-helper)
> **Parent Spec**: [proposal.md](./proposal.md)
> **Parent Story**: [US-012](../../../docs/requirements/user-stories/US-012.md)
> **Target Version**: aria-plugin v1.15.0
> **Estimate**: ~24h

## AC 对照总览

| Task Group | 对应 proposal.md AC 区块 |
|-----------|------------------------|
| T1.x | § Acceptance Criteria / helper (Layer 3) |
| T2.x | § Acceptance Criteria / phase-c-integrator (Layer 2) + branch-manager 边界 + 边界条件 |
| T3.x | § Acceptance Criteria / AB Benchmark + 文档同步 |

---

## Task Group T1: Layer 3 — git-remote-helper (P0, 前置, canonical)

### T1.1 创建 helper skill 目录结构

**目录结构**:
```
aria/skills/git-remote-helper/
├── SKILL.md                           # frontmatter + 引用 scripts + references
├── scripts/
│   ├── check_parity.sh                # T1.2
│   ├── push_all_remotes.sh            # T1.3
│   └── verify_post_push.py            # T1.4 (Python, 指数退避)
└── references/
    ├── api.md                         # 3 指令块完整契约
    ├── schema.md                      # canonical JSON schema
    └── platform-notes.md              # macOS/Linux/shallow/detached
```

**SKILL.md frontmatter**:
```yaml
name: git-remote-helper
description: |
  Git 多远程 parity 检测与 push 验证的共享基础设施。
  内部工具, 仅供其他 skills 引用。
user-invocable: false
disable-model-invocation: true
allowed-tools: Bash, Read
```

**Prerequisites 说明** (在 SKILL.md):
- 需要 `jq` (JSON 构造)
- 需要 `python3` (verify_post_push.py)
- 可选 `timeout` / `gtimeout` (Bash 脚本中, 缺失时脚本降级 Python timeout)

**AC 对应**: helper 存在性 AC

---

### T1.2 实现 `check_parity.sh` (Bash, 纯读)

**参数**: `--repo=<path> --branch=<name> --verify-mode=local_refs|ls_remote --timeout=<seconds>`

**实现要点**:

1. **shallow clone 守卫** (继承 Phase 1.12):
   ```bash
   if [ "$(git -C "$repo" rev-parse --is-shallow-repository)" = "true" ] \
      || [ -f "$repo/.git/shallow" ]; then
     # 为每个 remote 输出 parity: unknown, reason: shallow_clone
     exit 0
   fi
   ```

2. **detached HEAD 处理**:
   ```bash
   if ! git -C "$repo" symbolic-ref -q HEAD >/dev/null; then
     # detached_head: true, 用 HEAD SHA vs 各 remote HEAD SHA
   fi
   ```

3. **枚举 remote** (区分 fetch/push URL — 假设相同):
   ```bash
   git -C "$repo" remote | sort -u
   ```

4. **local_refs 模式**:
   ```bash
   remote_head=$(git -C "$repo" rev-parse "refs/remotes/$remote/$branch" 2>/dev/null || echo "")
   if [ -z "$remote_head" ]; then
     # parity: unknown, reason: no_local_tracking_ref, reachable: unknown
   fi
   ```

5. **ls_remote 模式** (跨平台超时):
   ```bash
   if command -v timeout >/dev/null 2>&1; then
     TIMEOUT_CMD="timeout $timeout"
   elif command -v gtimeout >/dev/null 2>&1; then
     TIMEOUT_CMD="gtimeout $timeout"
   else
     # 降级: 调用 Python wrapper (见 platform-notes.md)
     TIMEOUT_CMD="python3 $(dirname $0)/_timeout_wrapper.py $timeout"
   fi
   remote_head=$($TIMEOUT_CMD git -C "$repo" ls-remote "$remote" "refs/heads/$branch" 2>/dev/null | cut -f1)
   # 区分: exit 124 (timeout) / exit 128 (auth_failed) / empty (not_found)
   ```

6. **behind/ahead 计算**:
   ```bash
   behind_count=$(git -C "$repo" rev-list --count "HEAD..refs/remotes/$remote/$branch" 2>/dev/null || echo 0)
   ahead_count=$(git -C "$repo" rev-list --count "refs/remotes/$remote/$branch..HEAD" 2>/dev/null || echo 0)
   ```

7. **parity 判定**:
   ```bash
   if [ "$local_head" = "$remote_head" ]; then parity="equal"
   elif [ "$behind_count" -gt 0 ] && [ "$ahead_count" -eq 0 ]; then parity="behind"
   elif [ "$ahead_count" -gt 0 ] && [ "$behind_count" -eq 0 ]; then parity="ahead"
   elif [ "$ahead_count" -gt 0 ] && [ "$behind_count" -gt 0 ]; then parity="diverged"
   else parity="unknown"
   fi
   ```

8. **JSON 输出**: 用 `jq -n --arg ... --argjson ...` 构造, 不用 `printf` 手工拼接

**验收 (对应 AC)**:
- shallow clone → `parity: unknown, reason: shallow_clone`
- detached HEAD → `detached_head: true`
- 未 fetch 的 remote → `parity: unknown, reason: no_local_tracking_ref`
- auth 失败 → `reachable: false, reason: auth_failed`
- timeout → `reachable: false, reason: network_timeout`
- 所有 parity 枚举 (equal/ahead/behind/diverged/unknown) 正确分类

---

### T1.3 实现 `push_all_remotes.sh` (Bash, 写)

**参数**: `--repo=<path> --branch=<name> [--remotes=origin,github]`

**实现要点**:

1. **pre_local_head 快照**:
   ```bash
   pre_local_head=$(git -C "$repo" rev-parse HEAD)
   ```

2. **对每个 remote**:
   ```bash
   pre_remote_head=$(git -C "$repo" rev-parse "refs/remotes/$remote/$branch" 2>/dev/null || echo "")
   push_output=$(git -C "$repo" push "$remote" "$branch" 2>&1)
   exit_code=$?
   post_remote_head=$(git -C "$repo" rev-parse "refs/remotes/$remote/$branch" 2>/dev/null || echo "")
   
   # success 判定: **不看 exit_code 或 message 单独判断**
   if [ "$exit_code" -eq 0 ] && [ "$post_remote_head" = "$pre_local_head" ]; then
     success=true
   else
     success=false
   fi
   ```

3. **"Everything up-to-date" 语义**: 当 `pre_remote_head == pre_local_head` (本地已同步), push 是 no-op, 但 post 验证仍必须 `post_remote_head == pre_local_head` 才算 success=true

4. **JSON 输出**: 用 `jq` 构造, 包含 `pre_remote_head` 和 `post_remote_head` 供 verify 比对

**不做**:
- 不 retry (retry 由 verify_post_push 处理)
- 不修改本地 ref (失败时保持原状)

**验收 (对应 AC)**:
- success 依据 SHA 对比, 不依赖 message
- 本地已同步场景 success=true (经 post 验证)
- 网络失败 success=false

---

### T1.4 实现 `verify_post_push.py` (Python, 指数退避)

**选择 Python 原因**: Bash 实现指数退避 + subprocess timeout + JSON 构造脆弱; Python 原生 `subprocess.run(timeout=5)` + `time.sleep()` + `json.dumps()` 清晰可靠。

**接口**:
```bash
python3 verify_post_push.py \
  --repo=<path> --branch=<name> --expected-sha=<sha> \
  [--max-retries=3] [--initial-backoff=2] [--timeout=5] \
  [--remotes=origin,github]
```

**实现伪码**:
```python
import subprocess, time, json, sys

def ls_remote(remote, branch, timeout):
    try:
        r = subprocess.run(
            ["git", "-C", repo, "ls-remote", remote, f"refs/heads/{branch}"],
            capture_output=True, text=True, timeout=timeout
        )
        if r.returncode != 0:
            return None, "auth_failed" if r.returncode == 128 else "error"
        line = r.stdout.strip().split("\n")[0] if r.stdout else ""
        sha = line.split("\t")[0] if line else None
        return sha, None
    except subprocess.TimeoutExpired:
        return None, "network_timeout"

def verify_remote(remote, expected_sha, max_retries, initial_backoff, timeout):
    schedule = [0] + [initial_backoff * (2 ** i) for i in range(max_retries)]
    # [0, 2, 4, 8] by default
    attempts = 0
    start = time.time()
    for sleep_s in schedule:
        if sleep_s > 0:
            time.sleep(sleep_s)
        attempts += 1
        sha, err = ls_remote(remote, branch, timeout)
        if sha == expected_sha:
            return {"remote": remote, "actual_sha": sha, "match": True, 
                    "attempts": attempts, "total_seconds": round(time.time()-start, 2)}
    return {"remote": remote, "actual_sha": sha, "match": False,
            "attempts": attempts, "total_seconds": round(time.time()-start, 2),
            "reason": err or "sha_mismatch"}
```

**上界验证**:
- 4 attempts × 5s timeout = 20s network
- sleep schedule [0, 2, 4, 8] = 14s sleep
- **总 per-remote 上界 = 34s** ≤ `max_per_remote_seconds`

**验收 (对应 AC)**:
- 重试策略完全遵循 [0, 2, 4, 8] schedule
- `max_per_remote_seconds = 34` 是数学上界
- 典型 case (远程已同步) attempts=1, total_seconds<5s
- match=false 情况返回详细 reason, 不抛异常

---

### T1.5 撰写 references 文档

**`api.md`**: 3 个指令块 (check_parity / push_all_remotes / verify_parity_post_push) 的完整调用契约, 含参数 / 输出 / 错误处理

**`schema.md`**: JSON schema canonical 定义 (给 Spec A 和降级 fallback 实现引用)

**`platform-notes.md`**:
- macOS: 无 `timeout`, 用 `gtimeout` 或 Python wrapper
- Linux: 原生支持
- Git 2.15+ `--is-shallow-repository`, 旧版用 `.git/shallow` 文件
- shallow clone 下 `rev-list --count` 返回结果不可靠
- Detached HEAD 下 symbolic-ref 失败 → 用 HEAD SHA 直接比较
- `jq` 依赖声明, macOS/Linux 都需单独安装

---

### T1.6 helper AB benchmark

**新建**: `aria-plugin-benchmarks/ab-suite/git-remote-helper.json`

**evals**:
- `eval-hlp-1` `parity-check-equal` — 单 remote 已同步, 验证 `parity: equal`
- `eval-hlp-2` `parity-check-behind` — 双 remote 一个 behind, 验证 per-remote 状态分离
- `eval-hlp-3` `push-with-post-push-verify` — 描述完整 push + verify 流程
- `eval-hlp-4` `post-push-retry-on-delay` — 描述重试策略应对复制延迟

**运行**: `/skill-creator benchmark git-remote-helper`, 所有 delta > 0 才算通过

---

## Task Group T2: Layer 2 — phase-c-integrator 强化

### T2.1 Phase C.2.5 子步骤实现

**修改**: `aria/skills/phase-c-integrator/SKILL.md`

在 Phase C.2 (合并 PR) 步骤之后, 插入 C.2.5:

```markdown
### C.2.5 Multi-Remote Push Enforcement (v1.15.0+)

触发条件:
- C.2 合并成功 (master 已 fast-forward)
- `.aria/config.json` 中 `phase_c_integrator.multi_remote_push.enabled: true` (默认)

执行流程:
1. 快照 expected_sha = git rev-parse HEAD (合并后的 master HEAD)
2. 枚举子模块 SUBMODULE_LIST
3. 确定 ENFORCED_REMOTES (配置继承逻辑见 proposal § 3)
4. 对每个 REMOTE ∈ ENFORCED_REMOTES (Per-Remote Matrix):
   4a. for each SUBMODULE: helper.push_all_remotes(SUBMODULE.path, SUBMODULE.branch, [REMOTE])
       → 失败 → 按失败优先级表决策 (read_only_remotes > fail_on_partial_push)
   4b. 主仓库 push: helper.push_all_remotes(main_repo, branch, [REMOTE])
       → 失败 → 同上
   4c. 验证: helper.verify_parity_post_push(main_repo, branch, expected_sha, [REMOTE])
       → match=false → 同上
5. 汇总所有 remote 状态, 输出结构化报告
6. 任一阻断 → 退出 C.2.5, 输出修复命令, 不进入 Phase D
```

**验收 (对应 AC)**:
- C.2.5 在 C.2 合并后执行
- Per-Remote Matrix Gating 正确
- 失败优先级符合决策表

---

### T2.2 Per-Remote Matrix Gating 实现

**核心算法**:
```
for remote in ENFORCED_REMOTES:
    remote_ok = True
    for submodule in SUBMODULE_LIST:
        result = helper.push_all_remotes(submodule.path, submodule.branch, [remote])
        if not result.all_success:
            if remote in read_only_remotes:
                warn(submodule, remote, "read-only, skipped")
                continue  # 跳过本 submodule 的本 remote, 不阻断
            elif not fail_on_partial_push:
                warn(submodule, remote, "partial push allowed")
                continue
            else:
                error(submodule, remote)
                remote_ok = False
                break  # 跳过本 remote 的主仓库 push
    if remote_ok:
        # 继续主仓库 push + verify
        ...
    else:
        # 本 remote 主仓库不推送 (matrix gating)
        continue  # 处理下一个 remote
```

**子模块分支推断**:
- 从 `.gitmodules` 的 `branch=` 字段读取
- 未配置 → 用 `HEAD` (detached HEAD 下有歧义, 警告用户)

**验收**:
- 子模块推 X 失败 → 跳过主仓库推 X, 其他 remote 不受影响
- 部分完成状态 (子模块 1 ✅, 子模块 2 ❌) 输出 "部分完成, 手动修复"

---

### T2.3 配置集成

**修改**: `aria/skills/config-loader/DEFAULTS.json`

新增:
```json
{
  "multi_remote": {
    "enforced_remotes": [],
    "read_only_remotes": []
  },
  "phase_c_integrator": {
    "multi_remote_push": {
      "enabled": true,
      "enforced_remotes": null,
      "fail_on_partial_push": true,
      "post_push_verify": {
        "enabled": true,
        "max_retries": 3,
        "initial_backoff_seconds": 2,
        "max_per_remote_seconds": 34
      }
    }
  }
}
```

**config-loader 逻辑**: 新增继承规则 (`enforced_remotes: null` → 继承顶层)

**验收**:
- 无配置时用默认值, 不报错
- skill 级 null 继承顶层
- `enabled: false` 跳过 C.2.5
- `post_push_verify.enabled: false` 跳过 verify

---

### T2.4 降级策略 (helper 不可用)

**检测**: 启动 C.2.5 前 `test -f aria/skills/git-remote-helper/SKILL.md`

**降级行为**:
1. 输出警告 "git-remote-helper 不可用, 使用内联降级模式"
2. 内联 Bash:
   - 简化版 check_parity (仅本地 refs, 不重试)
   - 简化版 push_all_remotes (直接 `git push`, SHA 对比)
   - **不做** 指数退避 (降级不重试)
3. **Schema 一致性必须验证**: 降级版输出 JSON 必须与 helper canonical 格式完全相同

**验收**:
- 删除 helper 目录后, C.2.5 仍能跑完基本流程
- 降级版输出 JSON schema 与 helper 版一致 (同一 validator)

---

### T2.5 phase-c-integrator AB benchmark

**新增**: `aria-plugin-benchmarks/ab-suite/phase-c-integrator.json` 新增

- `eval-int-1` `multi-remote-merge-push` — 双 remote 项目合并 PR, 验证 with_skill 主动推送两 remote + SHA 验证

**验收**: `/skill-creator benchmark phase-c-integrator` delta > 0

---

## Task Group T3: 联调与文档

### T3.1 Spec A (Layer 1) + helper 集成测试

**场景**: state-scanner Phase 1.12 调用 helper `check_parity`

**验证**:
- helper 可用: state-scanner 输出 `multi_remote.*` 字段, schema 来自 helper
- helper 不可用: state-scanner 内联实现, schema 仍一致
- 字段值断言: parity 枚举正确, behind_count 准确, reason 枚举正确

---

### T3.2 Layer 2 + Layer 3 端到端

**场景**: C.2.5 完整 push + verify 链路

**验证**:
- 双 remote 场景主动推送 + SHA 验证
- 子模块递归推送 (matrix gating)
- 各种失败路径的阻断行为
- race condition 路径 (verify match=false)

---

### T3.3 文档同步

**`docs/architecture/system-architecture.md`**: 更新 Phase C.2 职责
> C.2 Multi-Remote Push Enforcement: 合并完成后强制推送所有配置远程, 通过 post-push SHA 验证作为集成质量门控。

**`CLAUDE.md`**: 更新 "多远程推送" 小节 (**不引用行号**):
```yaml
多远程推送 (v1.15.0+ 自动化):
  - [x] Phase C.2.5 自动推送所有 remote + post-push SHA 验证
  - [ ] 如 C.2.5 失败: 按错误提示手动修复后继续
  - [ ] 灾备 (C.2.5 完全不可用时, 保留作为人工 fallback):
    - aria 子模块: git -C aria push origin master && git -C aria push github master
    - 主项目: git push origin master && git push github master
```

**`aria/README.md`**: Skills 数量更新 (internal 5→6 if 包含 helper)
**`aria/CHANGELOG.md`**: v1.15.0 条目

---

### T3.4 全链路端到端测试 (模拟本次事件)

**测试场景**: 复现 2026-04-12 v1.14.0 发版事件

**步骤**:
1. 准备: 测试仓库含 aria 子模块 + origin + github 双 remote
2. 模拟事故: 子模块本地有 commit, 仅推 origin, 不推 github
3. 运行 C.2.5 (模拟 phase-c-integrator 完整流程)
4. **期望**: 
   - T1 (push_all_remotes): 检测 github pre_remote_head != pre_local_head, 自动推送到 github
   - T2 (verify_parity_post_push): SHA 验证通过
   - 事件 100% 不再发生

**验收**: 事故场景被 Layer 2 100% 覆盖, 回归测试入 eval-11 (Spec A)

---

## 实施顺序

```
T1.1 (目录) 
  ↓
T1.2 (check_parity) ─┐
T1.3 (push_all)   ─┼→ T1.5 (docs) → T1.6 (AB)
T1.4 (verify.py)  ─┘
  ↓
[Spec A 合并基于 T1 canonical schema]
  ↓
T2.1 (C.2.5) → T2.2 (matrix) → T2.3 (config) → T2.4 (fallback) → T2.5 (AB)
  ↓
T3.1 (L1+L3 integration) + T3.2 (L2+L3 E2E) → T3.3 (docs) → T3.4 (事故回归)
```

T1.2/T1.3/T1.4 可并行, 之间无依赖 (均依赖 T1.1 目录结构)。

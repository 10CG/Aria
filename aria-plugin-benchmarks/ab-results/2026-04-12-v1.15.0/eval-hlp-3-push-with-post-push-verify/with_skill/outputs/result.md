# Push + Post-Push Verify 完整流程

基于 `git-remote-helper` skill (`push_all_remotes` + `verify_parity_post_push`) 的两阶段推送与权威验证流程。该流程**不依赖 git push 输出中的 "Everything up-to-date" 文本**，而是通过 SHA 对比做严格判定。

仓库: `/home/dev/Aria` — 目标 remote: `origin`, `github` — 分支: `master`

---

## 设计原则

1. **"Everything up-to-date" 文本不可信** — git push 在本地 tracking ref 等于本地 HEAD 时会直接输出该文本，但远程实际是否接收到本次 push（或远程已有的 ref 是否等于本地期望的 SHA）需要独立验证。
2. **两阶段分离** — Stage 1 (`push_all_remotes`) 做写操作并基于**本地 tracking ref** 做初步判定；Stage 2 (`verify_parity_post_push`) 做纯读 `git ls-remote`，是权威答案。
3. **成功 = 所有 remote 的实际 SHA == 本地期望的 SHA** — 任何一个 remote 的 `match=false` 即视为整体失败。
4. **复制延迟容忍** — Forgejo/GitHub 存在 10-30s 复制延迟，`verify_parity_post_push` 使用 `[0, 2, 4, 8]` 秒指数退避重试，每个 remote 上界 34s。

---

## Stage 0 — Pre-push 快照 (必做)

在 push 之前捕获本地 HEAD SHA，作为 Stage 2 验证时的 `--expected-sha` 参数。

```bash
EXPECTED_SHA=$(git -C /home/dev/Aria rev-parse HEAD)
echo "Expected SHA: $EXPECTED_SHA"
```

**为什么必须在 push 之前捕获**：Stage 1 push 完成后，如果有并发提交 / reset 等操作修改了本地 HEAD，用当时的 HEAD 验证会导致假阳性/假阴性。期望值必须是"本次 push 的意图 SHA"。

---

## Stage 1 — `push_all_remotes` (写操作)

### 脚本

```
aria/skills/git-remote-helper/scripts/push_all_remotes.sh
```

### 调用

```bash
bash /home/dev/Aria/aria/skills/git-remote-helper/scripts/push_all_remotes.sh \
  --repo=/home/dev/Aria \
  --branch=master \
  --remotes=origin,github
```

### 参数

| 参数 | 类型 | 必须 | 默认 | 本次取值 |
|------|------|------|------|---------|
| `--repo` | string | 是 | — | `/home/dev/Aria` |
| `--branch` | string | 否 | `master` | `master` |
| `--remotes` | string | 否 | 全部 remote | `origin,github` (白名单) |

### 输出 JSON 形态 (预期)

```json
{
  "repo_path": "/home/dev/Aria",
  "branch": "master",
  "pre_local_head": "<SHA>",
  "results": [
    {
      "remote": "origin",
      "exit_code": 0,
      "success": true,
      "pre_remote_head": "<SHA_before>",
      "post_remote_head": "<SHA_after>",
      "message": "..master -> master"
    },
    {
      "remote": "github",
      "exit_code": 0,
      "success": true,
      "pre_remote_head": "<SHA_before>",
      "post_remote_head": "<SHA_after>",
      "message": "..master -> master"
    }
  ],
  "all_success": true
}
```

### `success` 严格判定

```
success = (exit_code == 0) AND (post_remote_head == pre_local_head)
```

关键点:
- **不依赖** git push stderr 的 "Everything up-to-date" 文本
- `post_remote_head` 通过本地 `git rev-parse refs/remotes/<remote>/<branch>` 读取 (push 会同步更新本地 tracking ref)，无额外网络成本
- 即便 push 是 no-op (本地已同步)，只要 tracking ref 等于 pre_local_head 仍判定为 success

### Stage 1 错误处理

| 场景 | exit_code | success | 下一步 |
|------|-----------|---------|-------|
| 推送成功 (new commits) | 0 | true | 进入 Stage 2 |
| 已同步 (no-op) | 0 | true | 进入 Stage 2 (仍须权威验证) |
| 网络错误 | ≠0 | false | 排查网络后重试本 stage |
| 认证失败 | 128 | false | 修复凭证后重试 |
| post_remote_head 读取失败 | 0 | false | 检查 tracking ref 状态 |
| remote 不存在 | 1 | false | `git remote -v` 确认配置 |

**中止条件**: 若 `all_success == false`，不要盲目进入 Stage 2 — 先解决失败项的根因，因为 Stage 2 只能发现问题、不能修复 push 失败。

---

## Stage 2 — `verify_parity_post_push` (纯读, 权威验证)

### 脚本

```
aria/skills/git-remote-helper/scripts/verify_post_push.py
```

### 调用

```bash
python3 /home/dev/Aria/aria/skills/git-remote-helper/scripts/verify_post_push.py \
  --repo=/home/dev/Aria \
  --branch=master \
  --expected-sha="$EXPECTED_SHA" \
  --max-retries=3 \
  --initial-backoff=2 \
  --timeout=5 \
  --remotes=origin,github
```

### 参数

| 参数 | 类型 | 必须 | 默认 | 本次取值 |
|------|------|------|------|---------|
| `--repo` | string | 是 | — | `/home/dev/Aria` |
| `--branch` | string | 是 | — | `master` |
| `--expected-sha` | string | 是 | — | `$EXPECTED_SHA` (Stage 0 捕获) |
| `--max-retries` | integer | 否 | 3 | 3 (默认) |
| `--initial-backoff` | float | 否 | 2.0 | 2 |
| `--timeout` | float | 否 | 5.0 | 5 |
| `--remotes` | string | 否 | 全部 remote | `origin,github` |

### 重试调度

```
retry_schedule = [0, 2, 4, 8]  秒 (max_retries=3, initial_backoff=2)
```

每次 attempt:
1. Sleep `schedule[i]` 秒
2. `git ls-remote <remote> refs/heads/<branch>` (timeout 5s)
3. SHA == expected-sha → 立即返回 `match: true`
4. 全部 attempt 耗尽 → `match: false, reason: <...>`

**per-remote 时间上界**: 4 × 5s (ls-remote) + 0+2+4+8s (sleep) = **34s**
**总时间上界** (2 个 remote, 最坏情况): 68s

### 输出 JSON 形态 (预期)

```json
{
  "repo_path": "/home/dev/Aria",
  "branch": "master",
  "expected_sha": "<EXPECTED_SHA>",
  "max_retries": 3,
  "retry_schedule_seconds": [0, 2, 4, 8],
  "results": [
    {"remote": "origin", "actual_sha": "<EXPECTED_SHA>", "match": true, "attempts": 1, "total_seconds": 0.3},
    {"remote": "github", "actual_sha": "<EXPECTED_SHA>", "match": true, "attempts": 2, "total_seconds": 2.4}
  ],
  "all_match": true
}
```

### 退出码

| exit | 含义 |
|------|------|
| 0 | `all_match: true` — 所有 remote 的 HEAD 实际等于本地期望 SHA |
| 1 | `all_match: false` 或运行时错误 |

### Stage 2 错误处理 — `reason` 枚举

| reason | 触发条件 | 处置建议 |
|--------|---------|---------|
| `sha_mismatch` | 全部 attempt 正常完成但 SHA 不匹配 | 检查是否有并发 push；Stage 1 是否真的成功；remote 是否被强制覆盖 |
| `network_timeout` | 最后一次 attempt ls-remote 超时 | 网络问题，稍后人工 `git ls-remote <remote>` 复核 |
| `auth_failed` | exit 128 | 修复 remote 凭证 (token / SSH key) |
| `error` | 其他非零 exit | 读取 stderr 人工诊断 |

---

## 总体成功判定 (两阶段组合)

```
整体成功 = Stage1.all_success == true
         AND Stage2.all_match == true
         AND ∀ r ∈ Stage2.results : r.actual_sha == EXPECTED_SHA
```

**任何一项 false 都必须视为失败**，不可用 "Everything up-to-date" 文本安慰自己。

---

## 完整脚本 (端到端示例)

```bash
#!/usr/bin/env bash
set -euo pipefail

REPO=/home/dev/Aria
BRANCH=master
REMOTES=origin,github
HELPER=/home/dev/Aria/aria/skills/git-remote-helper/scripts

# Stage 0: 捕获期望 SHA (push 之前)
EXPECTED_SHA=$(git -C "$REPO" rev-parse HEAD)
echo "[stage-0] expected_sha=$EXPECTED_SHA"

# Stage 1: 推送所有 remote
echo "[stage-1] push_all_remotes"
STAGE1_JSON=$(bash "$HELPER/push_all_remotes.sh" \
  --repo="$REPO" \
  --branch="$BRANCH" \
  --remotes="$REMOTES")
echo "$STAGE1_JSON" | jq .

ALL_SUCCESS=$(echo "$STAGE1_JSON" | jq -r '.all_success')
if [[ "$ALL_SUCCESS" != "true" ]]; then
  echo "[abort] Stage 1 push failed — 不进入 Stage 2"
  exit 1
fi

# Stage 2: 权威验证远程实际 SHA
echo "[stage-2] verify_parity_post_push"
STAGE2_JSON=$(python3 "$HELPER/verify_post_push.py" \
  --repo="$REPO" \
  --branch="$BRANCH" \
  --expected-sha="$EXPECTED_SHA" \
  --max-retries=3 \
  --initial-backoff=2 \
  --timeout=5 \
  --remotes="$REMOTES")
echo "$STAGE2_JSON" | jq .

ALL_MATCH=$(echo "$STAGE2_JSON" | jq -r '.all_match')
if [[ "$ALL_MATCH" != "true" ]]; then
  echo "[fail] 远程实际 SHA 与本地期望不一致"
  echo "$STAGE2_JSON" | jq '.results[] | select(.match==false)'
  exit 1
fi

echo "[ok] Push + Verify 全部通过 — origin & github 的 master 已等于 $EXPECTED_SHA"
```

---

## 关键契约摘要

| 契约点 | 规则 |
|--------|------|
| 成功判定不依赖文本 | `success = (exit_code==0) AND (post_remote_head == pre_local_head)` |
| 权威验证必走网络 | Stage 2 使用 `git ls-remote` (不是本地 tracking ref) |
| 期望 SHA 必须在 push 前捕获 | Stage 0 快照, 作为 Stage 2 的 `--expected-sha` |
| 复制延迟容忍 | [0, 2, 4, 8] 秒指数退避, per-remote 上界 34s |
| 写/读权限分离 | `push_all_remotes` 仅授权 skill 可调用；`verify_parity_post_push` 任意 skill 可调用 |
| 失败不放行 | Stage1 失败 → 不进 Stage2；Stage2 `all_match=false` → 整体失败, 必须处置 |

## 依赖

- `jq` (必须) — JSON 构造/解析
- `python3` (必须) — verify_post_push.py 实现
- `timeout` / `gtimeout` (可选) — ls_remote 超时 fallback (Python wrapper 兜底)

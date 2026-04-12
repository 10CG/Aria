# Post-Push 验证重试策略（GitHub 复制延迟 10-30s）

## 问题模型

Git push 成功到 GitHub 后，由于下列原因存在**最终一致性窗口**：

- GitHub 边缘节点 / CDN 的 fan-out 复制
- API 索引 (REST `/repos/.../commits`, `/branches`, `/actions/runs`) 比 Git 协议层慢
- Webhook / Actions 的调度延迟
- 跨远程镜像 (Forgejo → GitHub) 的 sync job 本身还可能叠加延迟

典型窗口：**10-30s**。极端情况下 60-120s（GitHub 状态页事件、大仓库、Actions 队列堆积）。

因此 push 后**立即**调用 API 验证，很可能返回旧状态（404 / 旧 SHA / 缺失 workflow run），但并非真正失败。需要区分「尚未可见」与「真正失败」。

---

## 重试策略：截断指数退避 + 抖动 (Truncated Exponential Backoff with Jitter)

这是分布式系统处理最终一致性/瞬时错误的标准做法（AWS Architecture Blog、Google SRE Book Ch.22 "Addressing Cascading Failures"）。

### Schedule（建议表）

| Attempt | 等待 (s) | 累计 (s) | 说明 |
|---------|---------|---------|------|
| 1 | 0 | 0 | 立即尝试一次（可能命中，节省时间） |
| 2 | 3 | 3 | 基础延迟，应对快速同步场景 |
| 3 | 5 | 8 | 进入 10s 观察窗 |
| 4 | 8 | 16 | 覆盖 p50 延迟 |
| 5 | 13 | 29 | 接近 30s 上界 |
| 6 | 21 | 50 | 覆盖 p95 |
| 7 | 30 | 80 | 覆盖 p99 / 异常情况 |
| 8 | 40 | 120 | **硬上界**，超过即判失败 |

公式：`wait_n = min(cap, base * 2^(n-1)) + random(0, jitter)`

- `base = 2s`
- `cap = 40s`（单次最大等待，避免无意义长等）
- `jitter ∈ [0, 2s]`（避免多实例/CI 矩阵同步惊群）
- **总预算 (deadline) = 120s**

### 为什么是 120s 上界

| 边界 | 值 | 依据 |
|------|-----|------|
| 乐观下界 | ~10s | GitHub 复制延迟观察下限 |
| 典型上界 | ~30s | 任务描述给定的 p95 窗口 |
| 安全系数 | ×2 | 覆盖 p99 异常抖动 |
| 硬截断 | **120s** | 超过此时间应视为真实故障而非延迟 |

超过 120s 仍 404 / 不收敛 → **升级为错误**：检查 `git push` 输出、`git ls-remote origin`、GitHub 状态页。

---

## 关键实现要点

### 1. 立即重试 + 退避混合

第 1 次 attempt **不等待**，直接打一发。GitHub 经常在 push 返回后 1-2s 内就可见，能节省 ~3s 的用户感知延迟。

### 2. 必须加随机抖动 (Jitter)

纯指数退避在 CI matrix / 多 job 并行时会同步惊群。AWS 推荐 **Full Jitter**：

```
wait = random(0, min(cap, base * 2^n))
```

或 **Equal Jitter**（本方案采用，延迟方差更小）：

```
wait = min(cap, base * 2^n)/2 + random(0, min(cap, base * 2^n)/2)
```

### 3. 幂等性前提

验证调用（GET commit SHA / GET branch / GET workflow run）天然幂等，重试安全。**禁止**对非幂等操作（如 create PR）套用这套重试。

### 4. 错误分类：哪些错误值得重试？

| 错误 | 重试？ | 原因 |
|------|--------|------|
| HTTP 404 (commit/branch not found) | ✅ | 典型复制延迟 |
| HTTP 422 (ref not found) | ✅ | 同上 |
| HTTP 5xx | ✅ | 服务端瞬时 |
| HTTP 429 (rate limit) | ✅ + 尊重 `Retry-After` | 限流 |
| 网络超时 / ECONNRESET | ✅ | 瞬时网络 |
| HTTP 401 / 403 (非限流) | ❌ | 鉴权问题，重试无意义 |
| HTTP 422 (validation error) | ❌ | 参数错，重试无意义 |
| DNS 解析失败 | ❌ (或只重试 1 次) | 通常是配置问题 |

### 5. 验证目标要精确

**推荐**：验证「目标 SHA 是否出现在远程分支」而不是「分支是否存在」：

```bash
git ls-remote origin refs/heads/master | awk '{print $1}'
# 或
gh api repos/OWNER/REPO/commits/<SHA> --jq '.sha'
```

这样避免把「旧 SHA 可见但新 SHA 未同步」误判为成功。

### 6. 日志与可观测性

每次 attempt 记录：`attempt_n / elapsed_ms / http_status / observed_sha`。便于事后分析延迟分布，调优 schedule。

---

## 参考伪代码

```bash
EXPECTED_SHA=$(git rev-parse HEAD)
DEADLINE=$(( $(date +%s) + 120 ))
BASE=2
CAP=40
ATTEMPT=0

while : ; do
  ATTEMPT=$((ATTEMPT+1))
  OBSERVED=$(gh api "repos/$OWNER/$REPO/commits/$EXPECTED_SHA" --jq '.sha' 2>/dev/null || true)
  if [ "$OBSERVED" = "$EXPECTED_SHA" ]; then
    echo "converged after ${ATTEMPT} attempts"
    exit 0
  fi
  NOW=$(date +%s)
  if [ "$NOW" -ge "$DEADLINE" ]; then
    echo "ERROR: not visible on GitHub after 120s (真实故障，非延迟)"
    exit 1
  fi
  # Equal Jitter
  EXP=$(( BASE * (2 ** (ATTEMPT-1)) ))
  [ "$EXP" -gt "$CAP" ] && EXP=$CAP
  HALF=$(( EXP / 2 ))
  JIT=$(( RANDOM % (HALF + 1) ))
  SLEEP=$(( HALF + JIT ))
  # 别越过 deadline
  REMAIN=$(( DEADLINE - NOW ))
  [ "$SLEEP" -gt "$REMAIN" ] && SLEEP=$REMAIN
  sleep "$SLEEP"
done
```

---

## 总结

| 维度 | 取值 |
|------|------|
| 算法 | 截断指数退避 + Equal Jitter |
| base | 2s |
| cap (单次) | 40s |
| **deadline (总上界)** | **120s** |
| 最大 attempt 数 | 8 |
| 首次立即重试 | 是 |
| 幂等操作 | 仅对幂等验证调用使用 |
| 错误分类 | 区分 retriable / terminal |
| 验证目标 | 精确匹配目标 SHA，而非分支存在性 |

**核心原则**：用退避吸收 10-30s 复制延迟（典型）与 30-120s 极端延迟（长尾），以 **120s 硬上界** 防止无限等待掩盖真实故障。

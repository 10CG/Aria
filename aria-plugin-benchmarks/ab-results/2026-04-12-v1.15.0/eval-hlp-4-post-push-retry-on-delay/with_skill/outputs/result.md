# `verify_parity_post_push` 指数退避重试策略

**问题背景**: 推送到 GitHub 后立即验证时, GitHub (以及 Forgejo) 存在 10-30s 的复制延迟窗口 —— 在这段时间内 `git ls-remote` 返回的 SHA 仍可能是旧值。直接读取会误判为推送失败。`verify_post_push.py` 通过**指数退避重试**吸收这段延迟。

**参考文件**:
- Skill 说明: `/home/dev/Aria/aria/skills/git-remote-helper/SKILL.md` (L90-110)
- API 契约: `/home/dev/Aria/aria/skills/git-remote-helper/references/api.md` (L186-305)
- 实现: `/home/dev/Aria/aria/skills/git-remote-helper/scripts/verify_post_push.py`

---

## 1. 重试 Schedule (默认参数)

### 公式

```python
# verify_post_push.py:125
schedule = [0.0] + [initial_backoff * (2 ** i) for i in range(max_retries)]
```

### 默认参数

| 参数 | 默认值 | 语义 |
|------|--------|------|
| `--max-retries` | `3` | 初次 attempt **之后**的最大重试次数 |
| `--initial-backoff` | `2.0` | 首次重试前等待秒数, 之后每次翻倍 |
| `--timeout` | `5.0` | 每次 `ls-remote` 子进程超时秒数 |

### 展开的 sleep 序列

```
i=0: initial_backoff * 2^0 = 2 * 1 = 2
i=1: initial_backoff * 2^1 = 2 * 2 = 4
i=2: initial_backoff * 2^2 = 2 * 4 = 8

schedule = [0, 2, 4, 8]  秒
```

### Attempts 计数

**总共 4 次 attempt** (= 1 次初次 + 3 次重试):

| Attempt # | 前置 Sleep | 累计耗时 (理想网络) | 触发时机 |
|-----------|-----------|-------------------|---------|
| 1 | 0s (立即) | ~0s | push 完成后立即查询 |
| 2 | 2s | ~2s | 吸收轻微延迟 |
| 3 | 4s | ~6s | 吸收中等延迟 |
| 4 | 8s | ~14s | 吸收较长复制延迟 (接近 30s 窗口下半段) |

**关键细节**: `schedule` 的第一个元素是 `0.0`, `verify_remote()` 在 L133 只在 `sleep_seconds > 0` 时才调用 `time.sleep`, 所以初次 attempt 是真正的"立即查询", 不会引入 0 秒 sleep 的开销。

---

## 2. Per-Remote 上界时间 (数学推导)

### 公式 (来自代码注释 L16, L122)

```
upper_bound = (max_retries + 1) * timeout + sum(sleep_schedule)
            = 4 attempts × 5s timeout + (0 + 2 + 4 + 8) 秒 sleep
            = 20s + 14s
            = 34s per remote
```

### 拆分

| 项 | 计算 | 值 |
|------|-----|------|
| 网络最坏情况 (全部超时) | 4 × 5s | 20s |
| Sleep 总和 | 0 + 2 + 4 + 8 | 14s |
| **Per-remote 上界** | 20 + 14 | **34s** |

### 双 remote (origin + github) 上界

```
total_upper_bound = 2 × 34s = 68s
```

因为 `main()` 中对 `target_remotes` 的循环是**串行**的 (L180-190), 没有并发执行。

### Early Exit 的实际耗时

典型场景下远低于 34s 上界:

| 场景 | 实际耗时 | 说明 |
|------|---------|------|
| 无延迟 (Forgejo 本地) | ~0.3s | attempt 1 即匹配, 见 api.md L259 示例 |
| 轻微延迟 (GitHub 热路径) | ~2.4s | attempt 2 匹配, 见 api.md L266 示例 |
| 中等延迟 | ~6s | attempt 3 匹配 |
| 较长延迟 | ~14s | attempt 4 匹配 |
| 全部失败 (worst case) | ~34s | 超时上界 |

**Early exit 机制** (L141-150): 一旦某次 attempt 的 SHA 匹配, 立即 return, 不再消耗后续 sleep/timeout 预算。

---

## 3. Python 实现原因 (为何不用 Bash)

`check_parity` 和 `push_all_remotes` 是 Bash 脚本, 但 `verify_parity_post_push` 选择了 Python。理由:

### (1) 精确 sleep 与浮点 backoff

Bash 的 `sleep` 在 POSIX 严格模式下只保证整数秒; GNU/Linux 虽然支持 `sleep 2.5`, 但跨平台兼容性差。Python 的 `time.sleep()` 天然支持浮点, 允许未来引入 `initial_backoff=0.5` 这样的子秒级配置。

### (2) 超时控制的一致性

`subprocess.run(..., timeout=5.0)` 自动处理子进程超时并 raise `TimeoutExpired`, 无需依赖 `timeout` / `gtimeout` 的二元分支 (macOS 缺失原生 `timeout`, 见 `references/platform-notes.md`)。这消除了 Bash 版本中"检测 timeout 可用性 → fallback 到 gtimeout → 再 fallback 到 Python wrapper"的三层降级。

### (3) JSON 输出的结构化构造

输出 schema (api.md L246-271) 包含:
- `retry_schedule_seconds: [0, 2, 4, 8]` (float 数组)
- `results[].total_seconds: 0.31` (float)
- 嵌套 `results[]` 列表

Python 的 `json.dumps()` 天然处理嵌套结构 + 浮点序列化。Bash + jq 需要逐层 `jq --argjson`, 可读性和错误处理都较差 —— 正好是 SKILL.md L26 "禁止 Bash 手工拼接 JSON" 的反例场景。

### (4) 可测试性

`verify_remote()` 是纯函数 (L108-162), 可以直接被 pytest 引入做单元测试 (mock `subprocess.run` 注入 "前 2 次返回旧 SHA, 第 3 次返回新 SHA" 的延迟模拟)。Bash 脚本的同类测试需要 fixture 仓库 + 网络 mock, 复杂度高一个数量级。

### (5) Early-exit 的清晰控制流

重试循环 (L132-150) 在 Python 中是 `for sleep_seconds in schedule: ... if sha == expected_sha: return` —— 意图清晰。Bash 版本需要 `while`/`break` + 计数器手工管理, 更容易出现 off-by-one (例如把"3 次重试"写成"3 次 attempt")。

### (6) `time.monotonic()` 防时钟跳变

L128, L143, L153 使用 `time.monotonic()` 而非 `time.time()`, 确保 `total_seconds` 不受 NTP 校时/夏令时影响 —— 在 34s 上界内发生时钟跳变概率虽低, 但这是 production-quality 代码应有的细节。

---

## 4. 错误分类 (`reason` 枚举)

当 4 次 attempt 全部耗尽仍未匹配时, 返回 `match: false` 并附带 `reason`。分类逻辑见 L70-105 的 `ls_remote()` + L152-162 的最终归并。

| `reason` 值 | 触发条件 | 实现位置 |
|-------------|---------|---------|
| `sha_mismatch` | 所有 attempt 的 `ls-remote` 均成功返回 SHA, 但 SHA 始终 ≠ `expected_sha`; 最后一次 `last_reason=None`, 归并时 fallback 到 `"sha_mismatch"` | L154 `reason = last_reason or "sha_mismatch"` |
| `network_timeout` | 最后一次 attempt 抛出 `subprocess.TimeoutExpired` (ls-remote 超过 5s) | L100-101 |
| `auth_failed` | 最后一次 attempt 的 git 进程返回 exit code 128 (credential helper 拒绝 / token 过期) | L89-90 |
| `error` | 其他非零 exit code, 或 `OSError` (git 二进制缺失 / 权限拒绝) | L91-92, L102-105 |

### 重要语义: `reason` 只反映"**最后一次**" attempt 的错误

L139 每次 attempt 都覆盖 `last_reason = err`。这意味着:

- 如果 attempt 1-3 全部 `network_timeout`, 但 attempt 4 返回了一个不匹配的旧 SHA, `reason` 会是 `"sha_mismatch"` (而不是 `"network_timeout"`)
- 消费方需要将 `reason` 理解为 "**为什么最后一次 attempt 也没能确认**", 而不是 "过程中出现过什么问题"

这是合理设计, 因为 `verify_parity_post_push` 的职责是给出**最终结论**, 中间态的 transient 错误不应污染最终诊断。

### 正常分支不算错误

`ls_remote()` 在 L95-96 处理 "branch 不存在" 的情况: 返回 `(None, None)`。这不触发 `reason`, 但会导致 `actual_sha is None ≠ expected_sha`, 最终落入 `sha_mismatch` 分支。合理 —— 分支不存在 = 推送未生效 = 验证失败。

### 退出码

| exit code | 含义 |
|-----------|------|
| 0 | `all_match == True`, 所有 remote 验证通过 |
| 1 | `all_match == False`, 至少一个 remote 未匹配 |

L205: `sys.exit(0 if all_match else 1)` —— 允许消费方 (`phase-c-integrator` C.2.5) 直接通过 shell exit code 做决策, 无需解析 JSON。

---

## 5. 对 10-30s 延迟的覆盖能力

### 延迟分布 vs 上界

```
GitHub 复制延迟    : 10s ~~~~~~~~~~~~~~~~~~~~~~ 30s
verify schedule    : 0s | 2s | 6s | 14s
超时累积上界       :                        34s (覆盖 30s)
```

- **下界 10s**: attempt 4 (累计 14s) 之前的 attempt 3 (累计 6s) 可能不匹配, attempt 4 预计能匹配
- **上界 30s**: 仍在 34s 之内; 若 30s 到达时 attempt 4 的 ls-remote 正在进行 (5s timeout), 完整覆盖 20+14=34s
- **超过 30s**: 超出 GitHub 典型 SLA, 视为 GitHub 故障; verify 正确报告 `sha_mismatch` 或 `network_timeout`, 交由 phase-c-integrator 决策重推或告警

### 调优建议

对于延迟更长的场景 (例如跨地域 mirror), 消费方可以:
- 调大 `--max-retries=4` → schedule 变为 `[0, 2, 4, 8, 16]`, 上界增加到 5×5 + 30 = **55s**
- 调大 `--initial-backoff=3` → schedule 变为 `[0, 3, 6, 12]`, 上界 4×5 + 21 = **41s**

两者都不需要改代码, 纯 CLI 参数调整。

---

## 总结

| 维度 | 答案 |
|------|------|
| Schedule 公式 | `[0] + [initial_backoff * 2^i for i in range(max_retries)]` |
| 默认 schedule | `[0, 2, 4, 8]` 秒 |
| Attempts 总数 | 4 (1 初次 + 3 重试) |
| Per-remote 上界 | **34s** = 4×5s timeout + 14s sleep |
| 双 remote 上界 | 68s (串行) |
| Early exit | SHA 匹配时立即 return, 跳过剩余 attempts |
| Python 实现理由 | 浮点 sleep / 跨平台超时 / JSON 结构化 / 单元可测 / monotonic 时钟 |
| 错误分类 | `sha_mismatch` / `network_timeout` / `auth_failed` / `error` |
| `reason` 语义 | 反映**最后一次** attempt 的状态, 非过程累积 |
| Exit code | `0` = all_match, `1` = 任一 remote 未匹配 |
| 对 10-30s 延迟覆盖 | 34s 上界完整覆盖 GitHub 典型复制延迟窗口 |

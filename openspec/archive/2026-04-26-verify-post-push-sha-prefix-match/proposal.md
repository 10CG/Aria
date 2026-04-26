# verify-post-push-sha-prefix-match

> **Level**: Minimal (Level 2 Spec — 仅 proposal.md, 无 tasks.md)
> **Status**: Complete (2026-04-26, archived per Level 2 micro-Spec convention)
> **Created**: 2026-04-26
> **Completed**: 2026-04-26 (aria-plugin PR #35 merged, commit d839b74; v1.17.6 single-Spec patch; P2.1 closed false-positive in same release)
> **Type**: Python script + doc 改动 (verify_post_push.py SHA 比较语义)
> **Source**: Round-2 latent-bug audit catalog P2.2 (`openspec/archive/2026-04-25-round-2-latent-bug-audit-findings/proposal.md` 第 99-103 行) — 2026-04-26 spike verified ✓
> **Spike Result (P2.2)**: 真 bug ✓ — script 严格 `==` + doc 示例用 7/24-char 短 SHA, 用户照抄静默 mismatch
> **Spike Result (P2.1, sister)**: FALSE POSITIVE ✗ — 早退在 per-remote retry loop 内 (line 138), 不跨 outer `target_remotes` loop (line 186); `all_match` (line 198) 正确聚合. P2.1 declared closed in this Spec.
> **Related Memory**: `feedback_smoke_benchmark_truthiness.md` (truthiness 验证)

---

## Why

`aria/skills/git-remote-helper/scripts/verify_post_push.py` 第 147 行:

```python
if sha == expected_sha:
```

- `sha` 来自 `git ls-remote` (line 104), 始终是 **40-char full SHA**
- `expected_sha` 来自 CLI 参数 `--expected-sha`, 由调用方决定长度

**doc 自爆问题**:
- `aria/skills/git-remote-helper/SKILL.md:101`: 示例 `--expected-sha=19f2861` (**7-char short SHA**)
- `aria/skills/git-remote-helper/references/api.md:213/219/235/250`: 示例 `19f2861a3b4c5d6e7f8a9b0c` (**24-char short**)

用户照抄 doc 示例 → `40-char != 7-char` 永远不匹配 → 静默 `match=False` → 困惑"为什么 post-push verify 一直失败".

**production safety 不变**: Aria phase-c-integrator C.2.5 实际调用流程用 `git rev-parse HEAD` 返回 full 40-char SHA, 流程上 happy path 不触发. 但 doc 示例对新用户/新项目 onboarding 是 trap.

**Verifiability**: HIGH ✓ (2026-04-26 spike: doc 示例与 script 行为不一致, 可复现)

**为何 prefix-match 而非 full-SHA-only**:
- Git 生态默认接受 short SHA prefix (e.g. `git show 19f2861` 工作), 用户预期一致
- `git ls-remote` 总返回 full SHA, 但 caller 传 short prefix 是合法用法
- 强制 full SHA 会破坏跨工具习惯, 不符合 Aria 向后兼容原则
- prefix-match 是双向兼容的最小变更

---

## What

### 改动 1: script SHA 比较语义升级

**File**: `aria/skills/git-remote-helper/scripts/verify_post_push.py:147`

**当前**:
```python
if sha == expected_sha:
```

**新版**:
```python
if _sha_match(sha, expected_sha):
```

**新增辅助函数** (插入到 `verify_remote()` 之前):

```python
# Minimum SHA prefix length for safe matching.
# Git default short SHA is 7 chars; 4 is technically allowed but ambiguous.
# 7 chars over a typical repo (~10^4 commits) gives ~16^7 = 268M unique prefixes,
# collision probability negligible. Below 7 we reject as unsafe.
_MIN_SHA_PREFIX = 7


def _sha_match(actual: str | None, expected: str) -> bool:
    """
    Compare actual full SHA (from git ls-remote) against expected SHA,
    which may be a prefix (>= 7 chars) or full 40-char SHA.

    Returns True iff actual.startswith(expected) AND len(expected) >= _MIN_SHA_PREFIX.

    Empty/None actual → False (no match against absent remote SHA).
    Empty/short expected (< 7 chars) → False (rejected as ambiguous, even if prefix matches).
    """
    if not actual or not expected:
        return False
    if len(expected) < _MIN_SHA_PREFIX:
        return False
    return actual.startswith(expected.lower()) if actual else False
```

**注意 case sensitivity**: SHA 是 hex, git ls-remote 输出 lowercase, `expected_sha` 用户可能大小写混用 → 用 `expected.lower()` 兜底, 但 `actual` 来源单一就不动。

**实际生产路径不变**:
- Aria phase-c-integrator 传 full 40-char → `actual.startswith(full_40_char)` 等价于 `==` (因 actual 也 40-char)
- 现有 happy path 行为字节级一致

**新场景兼容**:
- 用户传 7-char short → `actual.startswith("19f2861")` 工作
- 用户传 4-char → `len(expected) < 7` → reject as False (防止 collision 假阳性)

### 改动 2: doc 示例统一为 full SHA + 显式说明 prefix 兼容

**Files**:
1. `aria/skills/git-remote-helper/SKILL.md:101` — 示例改为 full 40-char
2. `aria/skills/git-remote-helper/references/api.md` 第 213/219/235/250 行 — 示例改为 full 40-char
3. api.md `--expected-sha` 字段说明追加: "支持 full 40-char SHA 或 ≥7-char prefix (基于 startswith 匹配)"

### 改动 3: schema.md 不变

`verify_parity_post_push` schema 中 `expected_sha` 字段语义未变, 仅匹配语义放宽。

---

## 非目标

- 不改 retry 逻辑 (P2.1 false-positive, schedule [0, 2, 4, 8] 不变)
- 不改 ls_remote 实现 (timeout/error enum 不变)
- 不改 outer `target_remotes` loop (per-remote 独立执行不变)
- 不引入新 CLI 参数 (prefix-match 自动生效, 用户无需 opt-in)
- 不破坏 v1.15.0 multi-remote enforcement 行为 (Layer 2/3 矩阵报告不变)

## 验收

- [ ] `verify_post_push.py:147` 改为 `_sha_match(sha, expected_sha)` 调用
- [ ] 新增 `_sha_match()` + `_MIN_SHA_PREFIX = 7` 常量
- [ ] SKILL.md:101 示例改 full 40-char SHA
- [ ] api.md 4 处示例改 full 40-char + 字段说明追加 prefix 兼容性
- [ ] smoke benchmark: 3 类输入 (full 40-char, 7-char short, 4-char too-short) 验证 prefix-match + reject-too-short 行为
- [ ] catalog P2.1 false-positive declaration 在 commit message + Spec frontmatter 留痕
- [ ] merge 后立即归档

## 价值

- **doc 自爆 bug 修复**: 新用户照抄 doc 示例不再静默失败
- **Git 生态一致**: short SHA prefix 用法与 `git show`/`git checkout` 习惯对齐
- **catalog spike 闭环**: P2.1 (false-positive) + P2.2 (real bug) 一次性 disposition, Round-2 catalog 进度推进 5/8 (62.5%)
- **production safety**: full-SHA happy path 字节级不变 (`startswith` 在长度相等时退化为 `==`)

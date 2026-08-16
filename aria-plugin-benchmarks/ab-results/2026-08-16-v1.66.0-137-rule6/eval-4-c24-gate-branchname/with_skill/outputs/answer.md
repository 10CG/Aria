# C.2.4 Pre-Merge Precondition Gate — 在本项目 (主干 = `master`) 的执行方案

> 依据: `phase-c-integrator` SKILL.md §C.2.4 (v1.3.0 + v1.31.0 backend 抽象 + v1.65.x path coverage + #137 分支存在性核验)
> 及 `references/pre-merge-gate-empirical-traps.md` (7 条实测坑)。
> **模拟推演, 未执行任何命令, 未触碰任何真实仓库。**

## 0. 开场就要钉死的一件事: 主干名

本项目主干叫 **`master`**。gate 里所有「主干」位置一律写 `master`, **绝不允许出现字面量 `main`**, 也不允许依赖 CLI 的 default 值。

理由不是「风格」, 是这道 gate 的**根本形状**: backend 在结构上**无法区分「分支不存在」与「分支上没有正在跑的构建」** —— 两种情况都返回 `InFlightStatus(runs=[])`。所以 `--branch main` 打在一个远端不存在的分支上, 得到的是「没有 in-flight」⇒ 判 `green` ⇒ **Rule #8 的 (b) 腿恒真, 等于这道 gate 不存在**。这就是 aria-plugin #137。

因此下面的流程里有一步 **2.2 主干存在性核验**, 它的唯一职责就是让「主干名写错」当场炸出来, 而不是安静地放行。

⚠️ 另一个必须自觉的点: SKILL.md §C.2.4 这条「AI 照着敲命令」的散文流程, 是 `gate_check()` 之外**同一算法的第二份实现**。#137 的代码修复只加固了 `gate_check()`。我现在走的正是这第二份, 所以**存在性核验必须由我自己显式执行**, 不能假定「上游已经查过了」。

---

## (a) 我会实际敲进终端的命令

约定的环境变量 (第一段先设好, 后面全部引用它, 避免任何一处手抄成 `main`):

```bash
# ── 上下文 ──────────────────────────────────────────────
# 执行上下文契约: 必须在「C.2 这次合并的目标仓」根目录下跑。
# 若合并的是子模块 → cd 进子模块根再跑, 不要在主仓根跑。
REPO_ROOT=/home/dev/Aria/aria-plugin-benchmarks
cd "$REPO_ROOT"

MAIN_BRANCH=master            # ← 本项目主干真名。不是 main。不用 CLI default。
REMOTE=origin
PR_BRANCH=$(git rev-parse --abbrev-ref HEAD)     # 来自 Phase B / C.2
PR_NUMBER=123                                    # 来自 C.2 branch-manager 输出
```

### 步骤 0 — 读配置 (config-loader)

```bash
jq '.phase_c_integrator.pre_merge_gate' .aria/config.json
jq -r '.phase_c_integrator.pre_merge_gate.enabled            // true'                .aria/config.json
jq -c '.phase_c_integrator.pre_merge_gate.ci_backends        // null'                .aria/config.json
jq -r '.phase_c_integrator.pre_merge_gate.no_ci_fallback     // "skip_with_warning"' .aria/config.json
jq -r '.phase_c_integrator.pre_merge_gate.path_coverage_enabled // true'             .aria/config.json
jq -r '.phase_c_integrator.pre_merge_gate.primitive_call_timeout_seconds // 30'      .aria/config.json
```

同时读旧 alias (仍读, 但要发 deprecation warning):

```bash
jq -c '.phase_c_integrator.pre_merge_gate | {primitive_preference, no_aether_fallback}' .aria/config.json
```

### 步骤 1 — Aether binary pre-flight

```bash
aether --help | grep -q -- "in-flight" && echo "PREFLIGHT_OK" || echo "PREFLIGHT_MISSING_INFLIGHT_FLAG"
```

(`grep -q -- "in-flight"`: 加 `--` 防止 `in-flight` 被当成 grep 自己的选项。)

### 步骤 2 — Backend resolution (v1.31.0+)

```bash
# Aether backend probe (BACKENDS list 第 1 位, Aether-first 锁死)
command -v aether >/dev/null 2>&1 && echo "probe:aether-ci-cli=True" || echo "probe:aether-ci-cli=False"

# GitHub Actions backend probe (第 2 位, v1.31.0 仍是 stub)
command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1 \
  && echo "probe:github-actions=True" || echo "probe:github-actions=False"
```

### 步骤 2.2 — **主干存在性核验** (aria-plugin #137, 本项目最关键的一步)

```bash
# ⛔ 不要写成 `git ls-remote --heads origin master` —— 参数会被当 glob:
#    mast* / m[a]ster / maste? 都能命中 master, 拿它当存在性判据等于放行一切近似名。
# ⛔ 也不要加 --exit-code —— 无命中返 rc=2, 会被 catch-all 的 except 误分类成「核验失败」。
# ✅ 列出全部 heads, 落到「解析出的 ref 名列表」上做精确字符串比对。
git ls-remote --heads "$REMOTE" > /tmp/lsremote.out 2>/tmp/lsremote.err
LSREMOTE_RC=$?
echo "ls-remote rc=${LSREMOTE_RC}"

# 判据 A: 这次核验做成了没有 (只有这一问才看退出码)
#   rc != 0 → main-branch-verify-failed

# 判据 B: 分支到底存不存在 (只看 ref 名列表, 永不看退出码 —— 零命中也返 rc=0)
awk '{print $2}' /tmp/lsremote.out | grep -Fxq "refs/heads/${MAIN_BRANCH}"
EXISTS_RC=$?
echo "exact-match refs/heads/${MAIN_BRANCH} rc=${EXISTS_RC}"

# 人眼复核用 (只是打印, 不作判据)
awk '{print $2}' /tmp/lsremote.out
```

`grep -Fxq` 三个 flag 都是承重的: `-F` 关掉正则, `-x` 要求整行匹配, 合起来才是「精确字符串比对」。

超时重试**只对 timeout**, 不对 `rc != 0`:

```bash
# rc!=0 / 命令不存在 是确定性失败, 重试只是白等 (最坏 60 秒)。
# 只有 subprocess timeout 才退避重试, 且复用 ci_backends/aether.py 的 RETRY_BACKOFF (5s/15s/45s),
# 不在本步另造一套退避表。
timeout 30 git ls-remote --heads "$REMOTE" > /tmp/lsremote.out 2>/tmp/lsremote.err
```

### 步骤 2.5 — Path coverage 评估 (v1.65.0+, `path_coverage_enabled=true` 默认)

```bash
# a. 扫三个 workflow 目录 (.forgejo / .gitea / .github 都要看, 不是只看 .github)
ls -1 .forgejo/workflows/*.y*ml .gitea/workflows/*.y*ml .github/workflows/*.y*ml 2>/dev/null

# b. 取每个 workflow 的 on: push / pull_request 触发 paths
grep -n -A20 '^on:' .forgejo/workflows/*.y*ml .gitea/workflows/*.y*ml .github/workflows/*.y*ml 2>/dev/null

# c. 本 PR 变更集 —— 主干名再次显式给真值, 不依赖任何 default
git diff --name-only --no-renames "${MAIN_BRANCH}...${PR_BRANCH}"
git diff --name-only --no-renames "${MAIN_BRANCH}...${PR_BRANCH}" | wc -l
```

### 步骤 3 — 查主干 in-flight (无条件执行)

```bash
timeout 30 aether ci status --branch "$MAIN_BRANCH" --in-flight --json
#                                    ↑↑↑↑↑↑↑↑↑↑↑↑ 展开就是 master。
# 这里写字面 main 就是 #137 复发: 查一个不存在的分支 → 返回「没有在跑的」→ 恒放行。
```

展开后我真正敲下去的那一行长这样, 我会在敲之前肉眼确认一次分支名:

```bash
aether ci status --branch master --in-flight --json
```

### 步骤 4 — 查本 PR CI 状态 (`decision == not_applicable` 时跳过本步)

```bash
timeout 30 aether ci status --branch "$PR_BRANCH" --json
```

### 步骤 5/6 — verdict 与路由 (无外部命令, 见下节)

green 之后紧接着才是 §C.2.4.5 submodule pointer gate, 然后才轮到 branch-manager merge:

```bash
ARIA_SUBMODULE_GATE_MODE=block bash "${ARIA_PLUGIN_ROOT:-aria}/skills/phase-c-integrator/scripts/submodule_gate.sh"
```

---

## (b) 判定逻辑走哪几步, 每步的早退条件

顺序是**承重的**, 不能重排 —— 特别是 2.2 必须在三道早退之后、path coverage 评估之前 (理由见表内)。

| # | 步骤 | 早退 / 中断条件 | 早退后的结果 |
|---|------|----------------|-------------|
| 0 | 读配置 | `enabled: false` | **完全跳过 C.2.4**, 行为退回 v1.2.0, 六键输出不变 |
| 1 | Aether binary pre-flight | `aether --help` 无 `--in-flight` flag | **fail-fast 中断**, 提示「请升级 aether ≥ commit f29abee (2026-05-06)」。⛔ 不继续、不静默 skip |
| 2 | Backend resolution | `ci_backends: []` (显式禁用) **或** 所有 backend `probe()=False` | 按 `no_ci_fallback` 降级: `skip_with_warning` → 跳过 + workflow report 警告; `abort` → BLOCK |
| 2 | 同上 | stub backend (如 v1.31.0 的 GHA) 的 `query_*()` raise `NotImplementedError` | **abort, 向调用方 raise** —— ⛔ 绝不 catch 后路由到 `no_ci_fallback` (Hard Constraint #7)。否则「装了 gh 但实际用 Aether」的项目会让 Rule #8 静默降级 |
| **2.2** | **主干存在性核验** | `refs/heads/master` 不在解析出的 ref 名列表里 | `verdict=fail` + `gate_error.kind=main-branch-not-found` |
| **2.2** | 同上 | 核验**本身**没做成 (远端不可达 / `rc != 0` / 命令不存在 / 解码炸) | `verdict=fail` + `gate_error.kind=main-branch-verify-failed` |
| 2.5 | Path coverage 评估 | 任何不确定面 (git diff 失败 / YAML 解析失败 / 未建模 glob 或触发键 / `paths-ignore` 在场) | **fail-toward-covered**: 落 `covered` 或 `unknown`, 行为逐字段退回 v1.64.x。⛔ 绝不因为「拿不准」而判 `not_applicable` |
| 3 | 查主干 in-flight | **无早退** —— 这一步无条件执行 | 即使 2.5 判了 `not_applicable`, (b) 轴照查; stub backend 的 NIE 也经此步照常 propagate |
| 4 | 查 PR CI | `decision == not_applicable` | 跳过本步, `pr_ci_status = not_applicable` (零覆盖路径不存在可等的 PR CI) |
| 5 | Verdict 计算 | — | 见下方真值表 |
| 6 | 路由 | — | green → merge; wait → `wait_recoverable`; fail → BLOCK |

### 2.2 的两条硬纪律 (来自实测, 想不出来只能踩出来)

1. **退出码只回答「这次核验做成了没有」, 永不回答「分支存不存在」。** `git ls-remote` 零命中也返 `rc=0`。拿退出码判存在性 ⇒ 永远判「存在」⇒ 整道核验变摆设。
2. **`main-branch-not-found` 与 `main-branch-verify-failed` 不可混为一谈。** 前者是「主干名写错了 / 分支真没了」, 后者是「我没能问出来」。混掉之后, 一个配置错误会被读成一次网络抖动, 下次还犯。

### 2.2 位置为什么必须在 2.5 之前

- 放到 path coverage **之后**: 一个根本不存在的分支会先跑完整个覆盖评估, 白烧时间且报错点错位。
- 更危险的误植: 把它塞进 `if cfg.get("path_coverage_enabled", True):` 块**里面** —— 那是紧邻插入点最自然的落位, 后果是**关掉覆盖评估的调用方连这道核验一起失去**。

### 步骤 5 verdict 真值表

| `pr_ci_status` | main in-flight runs | verdict |
|---|---|---|
| `failing` / `error` | 任意 | **fail** |
| `pending` | 任意 | **wait** |
| `passing` | `[]` | **green** |
| `passing` | 非空 | **wait** |
| `not_applicable` | `[]` | **green** (+ `raw_message` 留痕, v1.65.0+) |
| `not_applicable` | 非空 | **wait** (仅 (b) 轴驱动) |

`gate_error` 在场时 (2.2 判 fail) 直接短路到 **fail**, 不进这张表。

### 步骤 6 路由 + 两条 surface 义务 (v1.65.0+, 缺一不可)

- `green` → 调 branch-manager merge, 进 C.2.4.5 → C.2.5。
  - (a) green 来源是 `not_applicable` 时, **必须**在 workflow report 加一行:「C.2.4: 变更路径无 CI workflow 覆盖, PR CI wait 已跳过 (not_applicable), main in-flight 已核」。
  - (b) `path_coverage.decision == unknown` 时 (gate 行为=现状, 但评估器自己失败了), **必须** surface:「C.2.4 path coverage 评估失败 (reason=`git-diff-failed` / `workflow-parse-failed` / `internal-error`), 已按 covered 现状行为处理」。其中 `internal-error` = 评估器自身异常 (既非 git 问题也非 workflow 解析问题), 文案须点明「请报 issue」—— 它和另两个 reason 的排查方向完全不同, 混着写会把人引向 git 和 main ref。
- `wait` → 输出 `wait_recoverable` 给 workflow-runner, 进 wait+retry (退避 `[30,60,120,300,300]`, 数组耗尽后重复末位; 上限 `wait_timeout_seconds=1800`)。
- `fail` → BLOCK + 输出 verdict / `raw_message` / `gate_error`, phase-c-integrator return failure。

### 输出 schema (本项目实例)

```json
{
  "verdict": "green",
  "pr_ci_status": "passing",
  "in_flight_runs": [],
  "primitive_used": "aether-ci-cli",
  "primitive_version_sha": "f29abee",
  "raw_message": "...",
  "path_coverage": {"decision": "covered", "workflows_scanned": 1,
                    "matched_workflows": ["ci.yml"], "changed_files_count": 3, "reason": "..."}
}
```

`gate_error` 是 additive 可选键, **只在 2.2 判 fail 时在场**, 且那一支**没有** `path_coverage`。它是**副本通道** —— 同一段文字必定同时写进 `raw_message` (主通道), 只读 `raw_message` 的消费方不会丢信息。

注意归层: `not_applicable` 由 **gate 层**产生 (path coverage 短路), 从不来自 backend; backend 的 `CIStatus.state` 另有 `not_found` 值, gate 输出目前不产生它。

---

## (c) 什么情况下 gate 会判 fail

### 直接 `verdict=fail`

| 触发 | 判据 | 说明 |
|---|---|---|
| PR CI 失败 | `pr_ci_status in [failing, error]` | 最主线的一条 |
| **主干分支不存在** | `refs/heads/master` 不在 `ls-remote` 解析出的 ref 名列表里 | `gate_error.kind=main-branch-not-found`。**本项目最可能的触发形态: 有人把 `--branch` 写成了 `main`** |
| **主干存在性核验没做成** | `ls-remote` `rc != 0` / 远端不可达 / binary 缺失 / 解码异常 | `gate_error.kind=main-branch-verify-failed`。与上一条**必须分开**记 |
| Primitive 报错 | aether exit code `1`–`126` | 映射为 fail |
| Subprocess 超时耗尽 | 单次超过 `primitive_call_timeout_seconds` (30s), 重试 3 次 (5s/15s/45s) 仍超时 | 退化为 fail |

### 会 BLOCK / abort, 但严格说不是 `verdict=fail` (行为上同样拦住 merge, 报告里要分清)

| 触发 | 行为 |
|---|---|
| aether binary 过期 (无 `--in-flight` flag) | **fail-fast 中断**, 提示升级到 ≥ `f29abee`。设计意图是宁可炸也不 silent skip |
| 无可用 backend **且** `no_ci_fallback: abort` | BLOCK + 提示安装受支持的 CI backend |
| stub backend `query_*()` raise `NotImplementedError` | **abort 并向上 raise**, ⛔ 不走 `no_ci_fallback` (Hard Constraint #7) |
| C.2.4.5 submodule pointer 出现 regression / divergence 且无 override | `mode=block` (v1.49.0+ 默认) → 拒绝 merge。这是 green 之后的**下一道** gate, 不是 C.2.4 判的 |

### 明确**不** fail 的几种情形 (常被误判)

- `pending` → **wait**, 不是 fail。
- `passing` 但主干有 in-flight → **wait**, 不是 fail。
- `path_coverage.decision == not_applicable` 且主干无 in-flight → **green (带警告放行)**, 不是 fail。
- `path_coverage.decision == unknown` → 行为等同 `covered` (现状), 不影响 verdict, 但**必须 surface**。
- aether exit `127` (binary not found) → 走 `no_ci_fallback` 降级, 不直接判 fail。
- 走 `emergency_hotfix` lane → **C.2.4 不豁免**。降级的只是 pre_merge audit 的 mode (challenge → convergence), CI gate 照过 (Rule #8: 紧急不等于跳 CI 验证)。

---

## 附: 落到本项目时我会额外自查的三点

1. **每一处主干名都展开确认一遍**。`--branch master`, `git diff master...`, `refs/heads/master` —— 三处任一漏成 `main`, 后果都不是报错而是**静默放行**, 这是本形状最阴的地方。
2. **执行目录**。本项目 `aria-plugin-benchmarks` 本身是 Aria meta-repo 的子模块。合并子模块就 `cd` 进子模块根跑 gate, 合并主仓就在主仓根跑; 跑错地方会让 path coverage 的 `git diff` 算错变更集。
3. **`raw_message` 出口净化**。ls-remote / aether 的 stderr 可能非 UTF-8: 用 `capture_output` 取 bytes + `surrogateescape` 解码 (⛔ 不传 `text=True` —— `UnicodeDecodeError` **不是** `OSError` 子类, 会裸抛穿过 `gate_check()` 的 `(TimeoutExpired, FileNotFoundError, OSError)` 元组), 并在出口做 `s.encode("utf-8","replace").decode("utf-8")`, 否则孤立代理码位会在下游 `json.dumps` 时才炸, 离现场极远。

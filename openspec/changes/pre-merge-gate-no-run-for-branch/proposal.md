---
runtime_probe:
  partition: .aria/gate-state-telemetry.jsonl   # gate_state_helper CLI 生产 telemetry 分区 (source=production 记录)
  symbol: record                                # CLI 子命令名 (消息标签)
  max_age_days: 14
---

# pre-merge gate: 「零 run」显影为 `not_found` + `no-run-for-branch` 提前交人, 不放行 (aria-plugin #152)

> **frontmatter 注**: 本 spec 是 `runtime_probe:` 声明式归档门探针 (DEC-20260705-001, `state-scanner/references/runtime-probe-declaration.md`) 的**首个采用者**; 评估前置 = A.2 产出 `detailed-tasks.yaml` (L2 yaml-only 子态自 v1.63.0 起评估)。探针只在 D.2 归档时一次性核验「近 14d 有 source=production 记录」, 非常驻 (R3 #1: 常驻 liveness 在本项目健康常态下恒红)。

> **Level**: Minimal (Level 2 Spec)
> **Status**: ✅ **Approved** (owner sign-off 2026-08-22; post_spec CONVERGED R7 5/5 PASS; **post_planning CONVERGED R5 5/5 PASS** 2026-08-23, 1 次 owner 加轮 — `detailed-tasks.yaml` v5, 20 任务 51h) — ready for B.1
> **审计轨迹 (post_spec, convergence, 5 席)**: R1 5/5 REVISE (2C/23M, 17 簇) → v2 → R2 5/5 REVISE (1C/21M, 14 簇; Major 持平 ⇒ **v3 设计收缩**: 删 AI 自动执行处方, 改 ~90s 提前交人) → R3 5/5 REVISE (0C/18M, 10 簇) → v4 → R4 2 PASS / 3 REVISE (0C/5M) → max_rounds=4 耗尽, **owner 裁 +2 轮** → v5 → R5 3 PASS / 2 REVISE (0C/2M) → v6 → R6 4 PASS / 1 REVISE (0C/1M: SC-5 自相矛盾一行修) → max_rounds=6 耗尽, **owner 裁 +1 轮** → v7 → **R7 5/5 PASS (0C/0M/4m) → CONVERGED**。Major 曲线 23→21→18→5→2→1→0。聚合报告 `.aria/audit-reports/post_spec-R{1..7}-1787379154696-pre-merge-gate-no-run-for-branch-aggregated.md`; R7 后按 A1-R7-m1/m2 + A4-R7-m1 落两处 minor (SC-13 证据抄录前移 / 处方 (b) branches 限定), 不改任何 verdict/kind/SC 语义
>
> ```yaml
> converged: true
> rounds: 7
> pending_owner:
>   - []   # 批准进 A.2 — 已批 (2026-08-22)
> owner_rulings_2026-08-22:
>   - "audit-engine 降级裁定: 选 [2] 加 2 轮 (max_rounds 4→6), R5 对 v5 做稳定性确认"
>   - "v3 设计收缩 (AI 不自动执行处方, 改为 ~90s 提前交人 + gate 渲染处方命令): **接受** (v5 现状); 自动动作若要, 另起 follow-up spec"
>   - "audit-engine 二次降级裁定 (max_rounds=6 耗尽, R6 4/5 PASS + A1 条件 PASS): 选 [2] 再加轮 R7 形式全票 (max_rounds 6→7)"
>   - "A.1 批准进 A.2 (post_spec CONVERGED R7 5/5)"
>   - "2026-08-23 post_planning max_rounds=4 耗尽 (R4 1/5 PASS): 选 [2] 加 1 轮 → R5 5/5 PASS CONVERGED"
> ```
> **Issue**: [aria-plugin#152](https://forgejo.10cg.pub/10CG/aria-plugin/issues/152) (2026-08-20 立案, 三步判别式实证; 候选 A/B/C 未定)
> **Owner 裁定 (2026-08-22, 本 session AskUserQuestion)**: **A′ = 显影 + 处方, 不放行** — 取 A 的「靠远端 run 史感知」与 B 的「处方文字」, 去掉 A 的「归 not_applicable 放行」。
> **认领**: Phase B-entry 经 `phase1_gate.py` advisory 认领 (collision.kind=self_multi_container 在场; 开工前三面 fetch: 无别容器 #152 track, `bfe8285d` 容器在做 Aria#179 secret-guard, 落点零交集)
> **基线冻结**: aria @ `400f0bc` (v1.66.3+2) — 本文所有行号对此 SHA。**复核 2026-08-22 (A.1 批准时)**: aria master 已前进到 `9e6a17c` (**v1.66.4**, #179 secret-guard ship, 对方容器); `git diff --stat 400f0bc..9e6a17c -- skills/phase-c-integrator skills/workflow-runner skills/config-loader .forgejo/workflows` **为空** ⇒ 本 spec 全部代码/文档触点字节不变, 行号继续有效; Phase B 在 `9e6a17c` 起分支
> **代码落点**: `aria/skills/phase-c-integrator/scripts/ci_backends/aether.py` · `scripts/pre_merge_gate.py` (含 `DEFAULT_CONFIG` + `DISPATCH_VIABLE` 常量) · `scripts/path_coverage.py` · `tests/test_pre_merge_gate.py` · `tests/test_path_coverage.py` · `SKILL.md §C.2.4` · `references/pre-merge-gate-empirical-traps.md` · `aria/skills/workflow-runner/scripts/gate_state_helper.py` (+ CLI) · `tests/test_gate_state_helper.py` · `workflow-runner/SKILL.md §wait_recoverable` · `references/workflow-state-schema.md` · `config-loader/SKILL.md` · `.aria/config.template.json` · `.gitignore` (telemetry 分区) · `docs/decisions/DEC-20260731-001-*.md` (前向指针) · `aria-plugin-benchmarks/ab-suite/phase-c-integrator-pre-merge-gate.json` + `-fixtures/NEG-4-no-run-for-branch.json`; Spec 落主仓 (Rule #5)
> **A.1.0 头脑风暴**: 未跑 — `audit.checkpoints.post_brainstorm = off` (Rule #10 白名单第一类, R1 A5 核定)。

---

## Why

### 症状 (issue 实证, 起草时复核)

`fix/147-*` 新分支首推 (变更 path-matched `skills/issue-triage/**`) → Forgejo 未建任何 run → gate 输出 `path_coverage.decision=covered` + `pr_ci_status=pending` → `verdict=wait`, 经 workflow-runner `wait_recoverable` 循环**等满 1800s 也不会有结果** —— 不是排队, 是 run 对象不存在。该次 ship 先被误诊成「runner 停摆」, 探针三步才定位真因 = Gitea/Forgejo 对新分支 push (`before=0000…`) 无 diff 可评, **paths 过滤 workflow 静默跳过不建 run**。

### 起草期复核补充的事实 (issue 没写, 改变修法落点)

| # | 事实 | 出处 | 含义 |
|---|---|---|---|
| F1 | backend 把「零 run」与「run 未完」**同映射**为 `pending`: `if not runs: return "pending"` | `ci_backends/aether.py:225-226` | 盲区的机器侧根因在这一行 |
| F2 | `CIStatus.state` Literal **早有** `not_found` 槽位, gate 输出「目前不产生」 | `ci_backends/base.py:29`; `SKILL.md:288` | 不需要新枚举值 |
| F3 | aria-plugin 自 2026-07-20 起按 CLAUDE.md 硬约束 1 **本地合并不开 PR** (最近 PR = #115, 07-19) | `forgejo GET /repos/10CG/aria-plugin/pulls?state=closed` (R1 A5 复核) | `pull_request` 触发面结构性死亡, 只剩 `push` ⇒ 每条新分支恒中 |
| F4 | backend 所查 `/actions/tasks` **只列已被 runner 领走的任务**; 返回**全量历史无截断** (returned==total_count 三仓) | 2026-08-20 handoff §教训 4; Aether CLI `internal/ci/status.go:45-47` + R1 A1 实测 | 「零 run」有第二来源 = run 已建未被领 (瞬态) ⇒ 不能判 `fail`; 且 **episode 内 `not_found` 单调** (有过 task 就不会回零) |
| F5 | 「PR 分支不存在」与「存在但零 run」在 backend 出口**逐字节同形** (`aether ci status --branch zzz-no-such-branch-152 --json` → `runs=[]`) | R1 A1 实测 | `not_found` 解码前须排除「分支不存在」 |
| F6 | 本 Forgejo (11.0.6+gitea-1.22.0): `/actions/runs`、`/actions/workflows` **404**; `POST …/actions/workflows/{file}/dispatches` **路由存在** (`{"ref":""}` → 400 `ref is empty`), 按文件名寻址; 带合法 ref 是否真建 run **未验** | 本 session + R1 A4/A5 复跑 | TASK-0a 纯 API 探针裁决 (§3.5); memory `reference_forgejo_new_branch_paths_filter_no_run` 的「dispatch 在 gitea-1.22 系不可用」与 F6 互斥, 探针后以 traps §6 为 SOT 修正 |
| F7 | `gate_state_helper.py` 是 **reference 实现, 运行时零消费方** (全部 SKILL.md 零引用, 无 `main()`; docstring 自陈 markdown-driven) | R2 A1 实测 | 任何「由 helper 保证」的不变量都必须先把 helper 接进运行时 (memory `completion_signals_vs_runtime_invocation`) |

### 为什么不能按 issue 原案 A 放行

原案 A 的信号来源 (远端 run 史) 与本 spec **相同**; 分歧只在处置: A 归进 `not_applicable` 放行 + 警告。但 `not_applicable` 的既有语义 (v1.65.0, #122) 是「变更路径结构性无 CI 覆盖, 没有可等的 CI」; 本场景恰相反 —— 变更 path-matched, CI **该跑而没跑**。归进 `not_applicable` = 合并未经 CI 的 path-matched 变更 = Rule #8 fail-open, 且污染 #122 钉死的语义封闭集。

### 为什么 v3 不再自动执行处方 (设计收缩; owner 2026-08-22 复议**接受**)

v1/v2 让 AI 在阈值后自动 dispatch 或推 commit。两轮审计证明这个子设计是最大的缺陷发生器 (R1+R2 44 条 Major 中 15-19 条直接归它): 需要一次性守卫 + 落盘持久 + 求值时点 + dispatch 活体可用性 + 「实质 commit」不可伪造 + prompt 去重 —— 每补一条就长出两条。而 #152 的真实痛点是「**等满 1800s 且误诊**」: 把它变成「~90s 后带着准确诊断和可复制的处方命令交人」已经解决 95% 的痛 (显影 + 处方), 自动动作只省一次人工粘贴。无人值守 (Layer 2) 下 prompt ≡ abort, 与既有 timeout prompt 行为一致, 不新增风险面。

## What Changes

### 1. backend 层: 零 run → `not_found`

`AetherBackend._normalize_pr_ci_status(runs)`: `if not runs: return "not_found"` (`aether.py:225-226`, 原 `pending`); `:218` docstring 同步。其余映射不变。

- 这是 **(a) 轴** 的唯一改动。**(b) 轴 `query_branch_in_flight` 本 spec 不改 —— scope 声明, 不是正确性声明**: (b) 轴共用 `/actions/tasks`, 同样把「main 无 in-flight」与「main 刚 push、run 已建未被领」折叠成空 runs, 存在同形分钟级 fail-open (PR passing + main 未领 ⇒ green)。它没有等价的 `not_found` 出口 (空 = clear = 放行), 需另一种消歧, **另案** (traps §6 记录 + Phase D 立案, 见 §6)。
- `github_actions.py` 仍 NIE stub, 不动。
- ⚠️ **落地顺序硬约束**: 基线 `compute_verdict([], "not_found")` 实测返 **`green`** (`:174-233` 无该分支, fallthrough)。**§1 与 §2 必须同一 commit**; TDD: 先写 SC-2 (红在 green), 再同时改 §1+§2。
- 基线 `test_pre_merge_gate.py:363` (`[] → "pending"`) 翻转为 `"not_found"`。

### 2. gate 层

#### 2.1 `gate_check` 控制流 (`:387-527`) — PR 分支存在性消歧作为**第七个早退 return 点** (现六点八变体之外新增一点; F5; R2 #4/#5)

```
... (b) 轴 in_flight 查询 (:485-497, 不变) → not_applicable 短路 (:498-506, 不变)
pr_status = backend.query_pr_ci(pr_branch)                      # (:508-518, 不变)
verify_note = ""                                                 # 哨兵: 非 not_found 路径也可读 (R3 #3)
if pr_status.state == "not_found":                               # 仅此时多付一次 ls-remote
    st, detail = _verify_branch_exists(pr_branch, remote=remote, timeout=...)
    if st == "not-found":
        msg = _sanitize_for_json(f"PR branch '{pr_branch}' not found on remote '{remote}'")
        return _build_output(verdict=VERDICT_FAIL, pr_ci_status="not_found",
                             in_flight_runs=in_flight.runs, primitive_used=backend.name,
                             raw_message=msg, path_coverage=pc,          # pc 在场 ⇔ 评估已执行
                             gate_error={"kind": "pr-branch-not-found", "message": msg})
    if st != "ok":                                               # verify-failed: detail 是 git stderr, 必须消毒
        verify_note = _sanitize_for_json(f" (PR 分支存在性核验失败: {detail})")
out = compute_verdict(main_in_flight_runs=in_flight.runs, pr_ci_status=pr_status.state,
                      backend_name=backend.name, cfg=cfg, path_coverage=pc)
if out.get("gate_error"):                                        # gate_check 知道分支名: 回填占位 + 核验失败附注
    m = out["gate_error"]["message"].replace("<pr_branch>", _sanitize_for_json(pr_branch)) + verify_note
    out["gate_error"]["message"] = m; out["raw_message"] = m   # 副本通道保持
return out
```

- `_verify_branch_exists(branch, remote, timeout=_LS_REMOTE_TIMEOUT) -> (status, detail)` = 现 `_verify_main_branch_exists` (`:302-352`) 函数体**原样搬迁**改名; **旧名保留为保关键字签名与默认值的包装** `def _verify_main_branch_exists(main_branch, remote, timeout=_LS_REMOTE_TIMEOUT): return _verify_branch_exists(main_branch, remote, timeout)` —— `:449` 调用字面**不改**, 测试 mixin `:85-89` 对旧名的打桩继续有效; PR 核验调**新名**, **mixin 对新名也打一桩** (默认 `("ok","")`, 逐测试按需覆盖; 不放 mixin 则日后 not_found 用例走真 ls-remote, traps #7 形状)。`:278-288` / `:305-319` 注释与 `:548-552` `--remote` help 随之更新。
- `compute_verdict` **不感知**分支核验 (无新形参)。

#### 2.2 `compute_verdict` 新分支 (`:174-233`; 插入位置承重)

```python
# 必须位于 `elif pr_ci_status == "not_applicable":` 之后、`elif main_in_flight_runs:` 之前 ——
# 后者不检查 pr_ci_status; 若在其后, (not_found, main 非空) 被它先命中, verdict 仍 wait 但
# gate_error 被吞 (R1 A2-M1 模拟实证)。代码内保留同义防呆注释。
elif pr_ci_status == "not_found":
    verdict = VERDICT_WAIT                      # 不论 main in-flight 与否
    gate_error = _no_run_gate_error(path_coverage, _effective_prompt_threshold(cfg))   # gate_error 在函数开头初始化为 None (哨兵, R3 #3)
    raw_message = gate_error["message"]         # 副本通道 (#137): 同文同写
...
return _build_output(..., path_coverage=path_coverage, gate_error=gate_error)
```

- `_effective_prompt_threshold(cfg: dict | None) -> int`: **唯一校验点** (R2 #9) — `cfg` 为 None 取 `DEFAULT_CONFIG`; 取 `cfg.get("no_run_prompt_after_observations")`; 非 int / bool / <2 → `warnings.warn` + 回落默认 **3**。`gate_check` 的 cfg 合并后与 `compute_verdict` 直调都经它, 两条路径恒一致。`DEFAULT_CONFIG` (`:57-69`) 加该键 (否则主仓 state-check `config-template-key-currency` 断言「模板键 ⊆ DEFAULT_CONFIG」FAIL, R2 A2 复现)。
- `pr_ci_status` 输出枚举 additive 加 `not_found`。

#### 2.3 `gate_error` 结构与 message 封闭表

```json
{"kind": "no-run-for-branch", "message": "<下表>", "prompt_after_observations": 3}
```

message 按 `(decision, reason 前缀)` 钉 (R1 #6; `git-diff-failed` / `workflow-parse-failed` / `internal-error` 运行时带 `: <detail>` 载荷, **前缀匹配**, R2 #14); 所有档必含子串 `no-run-for-branch`:

| `path_coverage` | message 要点 |
|---|---|
| `covered` / `workflow-trigger-matched` | 「变更 path-matched `<", ".join(matched_workflows)>` 但远端零 run — 符合 aria-plugin#152 (新分支首推 × paths 过滤, Forgejo 不建 run), 或 run 尚未被 runner 领走, 或 workflow `branches` 过滤不含本分支 (path_coverage 不建模 branches, R5 A1-m6)」; **当 `DISPATCH_VIABLE and dispatchable_workflows`** 追加处方行: 每文件一行 `forgejo POST /repos/<owner>/<repo>/actions/workflows/<basename(file)>/dispatches -d '{"ref":"<pr_branch>"}'` (路径取 **basename**: `dispatchable_workflows` 元素形如 `.forgejo/workflows/x.yml`, 逐字拼 URL 会 404, R3 #5; `<pr_branch>` 由 `gate_check` 事后回填 (2.1 末段), `<owner>/<repo>` 由 AI 在 prompt 渲染时填 — gate 不知道远端名; 占位统一尖括号; 渲染**禁用** `str.format` — JSON 体的花括号本就在串内) |
| `covered` / `workflow-files-changed` | 「变更含 workflow 文件本身 (按 covered); 远端零 run — 同 #152 形态、未被领, 或 `branches` 过滤不含本分支」 |
| `covered` / `empty-diff` | 「main…PR 三点 diff 为空, 无变更可跑; 远端零 run」(不带分支名 — compute_verdict 不知道分支名, R3 #6) — **不**归因 #152 |
| `unknown` / `git-diff-failed…` · `workflow-parse-failed…` · `internal-error…` | 「远端零 run; 覆盖未判定 (reason=`<完整 reason>`)」; `internal-error` 附「评估器自身异常, 请报 issue」(#126 同款) |
| pc 为 None (`path_coverage_enabled=false`) | 「远端零 run; 路径覆盖评估已关闭」 |
| `not_applicable` | **结构上不可达** (短路在 (a) 轴查询前, `:498-506`; SC-6 钉死) |

- `gate_error` 在场条件 (SKILL.md:290 改写) 三类: (i) main 核验 fail (既有 2 kind, `verdict=fail`, 无 `path_coverage`); (ii) `pr-branch-not-found` (`verdict=fail`, `path_coverage` 在场 ⇔ `path_coverage_enabled`); (iii) `no-run-for-branch` (`verdict=wait`, `path_coverage` 在场 ⇔ enabled)。**kind 封闭集 4**; 四个 kind 都遵守副本通道 (`raw_message == gate_error.message`)。
- 既有六个早退 return 点 (八变体) 键集逐字不变 (SC-7); main 核验那支本就是七键。
- kind 二维消歧表 (写进 SKILL 枚举处): 分支存在 × run 不存在 = `no-run-for-branch` (wait; **分支存在性未知 (核验失败) 归并此象限, message 带后缀** — 封闭表成员 + 可选后缀); 分支不存在 = `main-branch-not-found` / `pr-branch-not-found` (fail); `not_found` (backend 态, 主语 run) 与 `*-branch-not-found` (kind, 主语分支) 同词根异义, 并列说明。

### 3. workflow-runner: 观测计数 → 提前交人 (无自动写动作)

#### 3.1 `gate_state` additive 一字段 + `gate_state_helper.py` 接进运行时 (F7; R2 #1/#2/#3)

| 字段 | 类型 | 语义 |
|---|---|---|
| `no_run_observations` | int, 默认 0 | 本 episode (= 一个 `gate_state` 生命期: `is_first` 创建 → green/fail/abort 终态; 终态 state 可被下一 workflow 覆盖 = 新 episode, schema §3.3) 内**连续**带 `gate_error.kind == no-run-for-branch` 的 gate 调用次数 (**含初次**); 某轮非该 kind → 0 |

`format_version` **不 bump** (可选块内 additive 键; v1.1 读者 `.get` 默认 0)。

`gate_state_helper.py` 改动:
- `write_gate_state(..., gate_error_kind: str | None = None)`: 唯一计数点 — `gate_error_kind == "no-run-for-branch" and verdict == waiting` ⇒ `existing.no_run_observations + 1` (`is_first` 时 = 1), 否则 0; 显式 carry-forward 写回 (整块重建**必须**包含该键, SC-11 跨两次调用断言); `retry_count` / `started_at` 语义逐字不变。
- `reset_no_run_observations(state)`: 只置 0, 不碰其它字段。
- **CLI** (`python3 gate_state_helper.py <sub> --state-file <绝对路径>`; **`--state-file` 必填无缺省**, 缺失 exit 2 — 与 `--source` 同形 fail-closed, R6 A4-m2/A1-m4; Python API 默认 cwd 相对不变, 仅测试/复用面), 签名封闭 (R3 #2):
  - `record --name pre_merge --verdict {wait|green|fail}` (**gate 枚举**; CLI 内映射 `wait→GATE_STATUS_WAITING("waiting")`, `green/fail` 同名) `[--gate-error-kind K] [--threshold N]` (默认 3) `[--intervals JSON]` (默认 helper `DEFAULT_INTERVALS_SECONDS`; 调用方传 config `wait_check_intervals`) `[--in-flight-runs JSON] [--raw-message S] --source {production|test}` (必填) → 读-改-写 (沿用文件内 atomic write; **state 文件不存在且 verdict=wait 时先创建骨架** `{"format_version": "1.1", "gate_state": null}`, R3 #7) + 追加一行 telemetry `{"ts", "source", "sub": "record", "verdict", "kind", "no_run_observations", "should_prompt"}` + stdout JSON `{"retry_count", "no_run_observations", "should_prompt": obs >= threshold, "elapsed_seconds", "next_check_at"}`。
  - `reset [--observations] [--retry-count]` (至少一个旗标; `--observations` 只动 `no_run_observations`; `--retry-count` 置 `retry_count=0` **并置 `started_at=now`**, 与 §3.2 exit 2 continue 语义一致 — 具名 helper `reset_retry_count(state)` 与 `reset_no_run_observations` 对称) / `clear` (= `clear_gate_state`)。两者在 state 文件缺失时 exit 2; `record` 在文件缺失且 `verdict != wait` 时亦 exit 2 (只有首个 wait 才建骨架)。
  - exit 0 成功 / 2 输入或文件错 (stderr 说明)。
- **telemetry 分区**: 路径**由 CLI 从 `--state-file` 派生** = `<dirname(state-file)>/gate-state-telemetry.jsonl` (R4 A1-M2: 探针根 = spec 所在仓 = **主仓**; workflow-runner 恒传主仓 `.aria/workflow-state.json`, 即使被合并的是子模块 — gate 的 cwd 契约 (`path_coverage.py:17`) 与 state 文件位置是两回事, 后者从不随子模块走); append-only; 主仓 `.gitignore` 登记 (沿既有三个 telemetry 分区 `:19-21`); 记录 `ts` = `_utcnow_iso()` (ISO 8601, 探针 `fromisoformat` 可解析, epoch 会恒 warn); **`--source` 无缺省, 必填** (`production|test`; 缺失 → exit 2, 忘带旗标 = 红不是假绿, R4 A1-M3); 单测一律 `--source test`, 探针只计 `source == production`。
- **运行时接线** (镜像 `phase1_gate.py` 先例): workflow-runner SKILL §wait_recoverable 实施步骤改为**经 subprocess 调 CLI 维护 gate_state**, 不再由 AI 手写 JSON; 「真被生产调用」的证据 = 本 spec frontmatter `runtime_probe:` 声明 → D.2 归档门一次性核验 (非常驻 state-check: R3 #1 实测本项目 C.2.4 wait episode 稀疏, 14d liveness 恒红)。

#### 3.2 polling loop 与 exit condition (workflow-runner SKILL `:338-358` 实施步骤 + `:332-336` Exit conditions)

```
2.  首个 wait verdict → 创建 gate_state **也经** CLI record (同 3c' 全旗标; is_first ⇒ retry_count=0, obs=1 若带 kind)   # 非 AI 手写 JSON
    所有 CLI 调用**显式传** --state-file <主仓根绝对路径>/.aria/workflow-state.json (R5 A1-m5: helper 默认相对 cwd, 子模块 cwd 下会静默另起 state + 分区)
3c. sleep 结束 → 重调 phase-c-integrator C.2.4 gate → 得 out
3c'. record = CLI record --state-file <主仓 .aria/workflow-state.json 绝对路径> --name pre_merge --verdict out.verdict --intervals <cfg.wait_check_intervals>
                 --in-flight-runs <json(out.in_flight_runs)> --raw-message <out.raw_message> --source production
                 [--gate-error-kind out.gate_error.kind --threshold out.gate_error.prompt_after_observations]
                 # 两旗标仅 out.gate_error.kind == "no-run-for-branch" 时传 (fail 类 kind 无 threshold 键, R4 A4-m1);
                 # in_flight_runs / raw_message 必须透传 (R4 A4-M1: 否则 gate_state 两字段恒空, 与 schema :123 / §5 row 「wait 态携处方文案」互斥); 先自增, 后求值
3d. 按 exit conditions 处理 (输入 = out + record); CLI **退出码 2** → surface 错误 → 直接 abort (终止分支; 不再调 reset — reset 同样会退 2, R4 A1-m4), 禁止回退手写 JSON
```

Exit conditions (first-match-wins, 四条**全部终止 loop** 的类型不变):
1. user Ctrl-C → suspended [不变]
2. `retry_count > max OR elapsed > wait_timeout_seconds` → user prompt; `continue` ⇒ CLI `reset --retry-count --observations` (**两者归零, 且 `reset --retry-count` 同时置 `started_at=now`** — exit 2 实际只由 elapsed 触发, 不重置 started_at 则 continue 后每 30s 再弹, R4 A4-m2 基线 :356 既有缺口顺手补) [原 reset 语义 + 补 observations/started_at]
2.5 **(新)** `out.gate_error.kind == "no-run-for-branch" AND record.should_prompt` → **no-run prompt** (定义一次, 见 3.3): `continue` ⇒ CLI `reset --observations` 回 loop (`retry_count`/`started_at` 继续累计, exit 2 上界不变); `abort` ⇒ `verdict=fail` 语义 (session failed, 保留 gate_state 给 audit trail)
3. `verdict=fail` → stop [不变]
4. `verdict=green` → merge [不变]

时间轴 (默认 `no_run_prompt_after_observations=3`, intervals `[30,60,120,…]`): 初次 gate t=0 → record obs=1 / 重查 #1 t≈30 → obs=2 / 重查 #2 t≈90 → obs=3 ⇒ `should_prompt` ⇒ **首次 gate 调用后 ~90s 交人** (非等满 1800s)。`continue` 后 (retry_count 已 2, 后续 sleep 120/300/300) 再 3 次连续观测在 t≈210 / 510 / **810** ⇒ 第二次 prompt 在 **~810s** (R3 #4 逐轮实算勘正), 仍远早于 1800s。

#### 3.3 no-run prompt (一处定义, §C.2.4 步骤 6 与 workflow-runner 2.5 共同引用)

> 🔴 C.2.4: `<gate_error.message 原文>`。已连续 `<record.no_run_observations>` 次观测到零 run (~`<record.elapsed_seconds>`s)。处方 (择一, 由你执行; AI 不自动执行):
> (a) dispatch 命令行 — **已由 gate 渲染进 `gate_error.message`** (2.3 表 trigger-matched 档, 受 `DISPATCH_VIABLE` 常量与列表非空控制), AI 只填 `<owner>/<repo>`; message 无此行则 (a) 不出现
> (b) 推一个碰 CI 触发路径的实质 commit 到 `<pr_branch>` (`workflow-trigger-matched`: matched workflow 声明的 paths; `workflow-files-changed`: 被改 workflow 自己声明的 paths) — 第二次 push 是普通 diff, paths 正常评; **若 workflow 有 `branches` 过滤且不含本分支, 推 commit 无效 → 改分支名或走 (a)/(c)** (path_coverage 不建模 branches, 人核) **[`unknown`/`empty-diff`/pc=None 档不出现本行: 解析器读不懂的 workflow 不让人猜]**
> (c) 继续等待 (`continue`) / 放弃 (`abort`)

**§C.2.4 步骤 4/5/6 改动**: 步骤 4 映射加 `not_found`; 步骤 5 加 `not_found → wait + kind=no-run-for-branch` / `pr-branch-not-found → fail`; 步骤 6 `wait` 路由加: `gate_error.kind == no-run-for-branch` 时 AI **必须** surface `gate_error.message` 原文 (不得只写「CI pending, 等待中」), 并注明「prompt 由 workflow-runner 2.5 按观测计数触发; 交互式直调 §C.2.4 (无 workflow-runner) 时**无计数**, 读者自行按 message 与上方处方处置」(R2 A1-m5)。

#### 3.4 config

`phase_c_integrator.pre_merge_gate.no_run_prompt_after_observations` 默认 **3** (int ≥ 2; **不提供 1** = 首次即 prompt, 回到 AD-2 假红); 校验见 2.2 `_effective_prompt_threshold`; 登记: SKILL.md 两张配置表 + config-loader + `.aria/config.template.json` (同时补 #122 漏登的 `path_coverage_enabled`) + `DEFAULT_CONFIG`。

#### 3.5 TASK-0a: `workflow_dispatch` 纯 API 探针 (实现前, 不依赖本 spec 代码; R2 #6)

aria-plugin throwaway 分支 (含 path-matched 变更) → 首推 → `forgejo POST …/workflows/issue-triage-tests.yml/dispatches -d '{"ref":"<b>"}'` → 记录 HTTP 码; 轮询 `aether ci status --branch <b> --json` 至 runs 非空或 600s → 记录 Δt; 删分支。结果 = 布尔 **`dispatch_viable := 600s 内观测到 run`** (2xx 但 600s 零 run ⇒ **false**, 证据标 `queued-unobserved`; 4xx/5xx/网络异常 ⇒ false 标 HTTP 码或异常名; R3 #5, R4 A3) + 证据 (HTTP 码 / run id / Δt / 日期) 写入 **traps §6 (仓内 SOT)**, memory `reference_forgejo_new_branch_paths_filter_no_run` 按 traps 镜像修正 (带同一证据)。落点 (条件 scope **只此一处**): `dispatch_viable` → `pre_merge_gate.py` 模块常量 `DISPATCH_VIABLE` (注释引 traps §6 证据行) → 2.3 trigger-matched 档是否渲染 dispatch 行。**若 false: §4 整段 + SC-8 + SC-9 的 `dispatchable` 部分 + `DISPATCH_VIABLE` 常量本身 + 2.3 表的 dispatch 渲染句 + SC-2 的 dispatch 子项 + SC-5 (c2) + 3.3 (a) 行 + §2.1 末段的 `<pr_branch>` `.replace` (占位符随 dispatch 行消失, 回填无对象; (c1) 的「不含占位」断言保留作守卫), 整组从本 spec 删除** (不留零消费方字段/常量, R4 A1-m6), Impact/CHANGELOG 相应不提。

### 4. path_coverage 附带: `dispatchable_workflows[]` (仅当 TASK-0a `dispatch_viable=true`; false 则本节整段删除)

`_parse_workflow` 返回值 additive 加 `"dispatchable": bool` (`on:` 含 `workflow_dispatch`; 标量 / flow 列表 / 块形三种写法; 仍属 `NON_AUTO_TRIGGER_KEYS`, 不改判定); `_evaluate` 结果 additive 加 `"dispatchable_workflows"` (= matched 中 dispatchable 者)。判定规则 1-8 与 reason 封闭集逐字不变 — **reason 族 = 8** (7 条规则终态 + `internal-error`; 模块 docstring `:36`「共 9 个」是既有错, 本 spec 顺手勘正为描述性改动)。`_result()` 加可选参数; 仅规则 6 调用点传 matched 子集, 其余 8 处 `_result` 调用不改。`workflow-files-changed` 下恒 `[]` 是设计限制, **禁**扩成全量列表。

### 5. 文档同步面 (Rule #3; 逐位置; 主仓 vs 插件分列于「文件」栏)

| 文件 | 位置 (@400f0bc) | 改动 |
|---|---|---|
| `phase-c-integrator/SKILL.md` | `:46-54` 顶层配置表 / `:292-302` 节内配置表 | 两表都加 `no_run_prompt_after_observations` (沿 `path_coverage_enabled` :54/:302 先例) |
| 同上 | `:172-183` YAML 摘要块 (`:175` wait 条件 / `:180` 枚举 / `output:` 补 `gate_error`) | 加零 run / `not_found` / `gate_error` |
| 同上 | `:241` 「7 条坑」计数 | 随 traps §6 |
| 同上 | `:248` 步骤 2.2 | 「分支存在性核验: main 恒查; PR 仅 `not_found` 时查」 |
| 同上 | `:252-263` 步骤 4/5/6 | §3.3 |
| 同上 | `:276-290` Output schema / :288 归层注记 / :290 在场条件 | 枚举 + `gate_error` 结构 + 三类在场 + 二维消歧表 |
| `pre_merge_gate.py` | `:181-194` / `:253-256` docstring | 与 :290 同语义 |
| `aether.py` | `:218` docstring | `not_found` |
| `path_coverage.py` | `:36` 「共 9 个」 | 勘正 8 |
| `references/pre-merge-gate-empirical-traps.md` | 新 §六 | 收录 (每条「不能靠读代码想出来」): F3 / F4 (只列已领 + 全量历史 ⇒ 单调) / (b) 轴同形盲区 / F6 端点 404 + dispatch 按文件名 / TASK-0a 结果 `dispatch_viable` + 证据。**不**收 F1 (读码可得, R2 A5-m1) |
| `workflow-runner/SKILL.md` | `:249-264` gate_state JSON 块 / `:313` 触发场景 / `:326` log 文案 / `:332-336` Exit conditions / `:338-358` 实施步骤 / `:345` 字段枚举 / `:389` wait 分支 | §3.1-3.3 |
| `workflow-state-schema.md` | `:38-52` JSON 块 / `:110-131` 字段表 / `:125` raw_message 注 | 新字段 (标 spec 名, format_version 不变) / wait 态携处方文案注 |
| `config-loader/SKILL.md` (`path_coverage_enabled` 已在 `:283`, 只加新 key) · 主仓 `.aria/config.template.json:73-91` (两 key 都缺, 补两个) | — | 登记 |
| 主仓 `.gitignore` | `:19-21` telemetry 分区段 | 加 `.aria/gate-state-telemetry.jsonl` |
| `gate_state_helper.py` | `:2-18` 模块 docstring (自陈 markdown-driven / Usage(Python) — 即 F7 证据) | 改为「CLI 为运行时入口, Python API 为测试/复用面」 |
| `state-scanner/references/runtime-probe-declaration.md` | `:135-139` 「尚无采用者」预言句 | 改为指向本 spec 的已验证事实 (R4 A5-m1) |
| `pre_merge_gate.py` | `:278-288` / `:305-319` / `:404-408` 注释 · `:548-552` `--remote` help | 随改名与新路径更新 |
| 主仓 `docs/decisions/DEC-20260731-001-c24-wait-adjudication-retirement.md` | 「退役裁定」小节 + 文末 | 按 DEC-20260702-001:124-128 先例: 原文**不回改**; 小节内加一行 `📌 前向指针 (2026-08-xx): verdict=wait 自 v1.66.5 另含「结构性零 run」语义, 见文末`; 文末加日期化 `## 📌 前向指针` 段指向本 spec |
| `aria/CHANGELOG.md` + 版本引用点 | — | PATCH **v1.66.5**; 引用点口径 (Aria#177): aria 侧 `plugin.json` / `marketplace.json` **`:3` 与 `:16`** / `VERSION` / `CHANGELOG` / `README`; 主仓侧 **14 个版本字符串点 + gitlink** (Aria#177 逐字点名 + 本 session `grep 1.66.3` 实核): `CLAUDE.md:139` + `:141` (项目状态段插件版本行, **无 custom check 兜底**; v1.66.4 ship 实证这两行确被改, 位置不变) / `VERSION:24` / `README.md:8` badge + `:242` `Plugin Version:` / i18n `README.{zh,ja,ko}.md` 各 badge + Plugin Version 行 + `translated-from` 标记 (= 9; 正文无实质变更不重译, 仅标记/版本) / gitlink。`CLAUDE.md:5` 是主项目版本, 非 #177 所指, 不动 |
| AB 套件 | `phase-c-integrator-pre-merge-gate.json` (`version` bump + `changelog` 行 + `fixtures[]` 新条目) + `-fixtures/NEG-4-no-run-for-branch.json` (元键集 = NEG-3 全集 8 键: `_fixture_id`/`_description`/`_target_behavior`/`_discriminating_question`/`_why_the_distinction_matters`/`_arm_expectations`/`_consumed_by`/`_ships_with`) + `ab-results/<date>-pre-merge-gate-no-run-for-branch/` 执行记录 | 见 rule6_note (NEG-3 自 v1.65.3 **从未被执行**, R3 A3 实核; NEG-4 必须真跑) |

### 6. Phase D 待办 (AI, D.1 执行, 归档门前置; A.2 转 tasks)

1. issue #152: A.1 批准后评论 (裁定 + spec 链接); D.1 收尾留言 (版本 / 行为 / `dispatch_viable` 结果 / memory 修正)。
2. aria-plugin 新 issue: 「Rule #8 (b) 腿对未被领取的 main run 不可见 (`/actions/tasks` 只列已领)」— 引 F4 + 本 spec §1。
3. aria-plugin#127 (open, C.2.4 surface 义务零 eval 覆盖) 追加评论: NEG-4 登记 + 仍缺的序列型 (多轮 prompt) fixture 形态。

### 7. A.2 转 tasks 时须带的 checklist 项 (审计裁定「留 Phase B 顺手」的非阻塞项, 防蒸发; R6 A1-m5)

- `DISPATCH_VIABLE` 读取方式钉为裸全局引用 (可 monkeypatch), 不用默认参捕获 (A2-R5/R6-m)。
- SC-15 的 AB 真跑须覆盖 phase-c-integrator (surface) 与 workflow-runner (should_prompt) 两 skill 行为 (A3-R5-m1)。
- traps §6 两处证据 (TASK-0a / SC-13) 统一带日期字段 (A5-R5-m1)。
- `record` 「文件缺失 + verdict≠wait → exit 2」补一条单测 (A2-R6-m1)。

## Design Decisions

- **AD-1 检测落在 backend 归一层**: 修在信息被丢失的那一行 (`:225`), `not_found` 作一等状态穿过 gate。
- **AD-2 verdict=`wait`, 拒 `fail` 也拒 `green`**: `green` = Rule #8 fail-open; `fail` 在 F4 下是假红。`wait` 保 fail-closed, 「瞬态 vs 结构性」交给**连续观测计数** (F4 单调性保证不回退)。
- **AD-3 复用 `gate_error` 副本通道**; 在场条件三类封闭; 新增机读 `prompt_after_observations` 使 workflow-runner 零解析文案、零读原始 config。
- **AD-4 阈值默认 3 次观测 (~90s), 误判代价 = 一次 prompt**: 依据薄 (一次现场 + 领取秒级常识); v3 下阈值偏低的后果只是早一次问人 (`continue` 即回到等待), 不再有任何自动写动作 ⇒ 不需要更强的经验依据。TASK-0a 的 Δt 是首个数据点; 离线侧信道不可行 (tasks `created_at == run_started_at`)。
- **AD-5 处方 = 给人的具体命令, 不自动执行** (v3 收缩, 理由见 Why 末段)。
- **AD-6 不动 Aether CLI / 不提上游**; 本 Forgejo 无 `/actions/runs`, 「零 run 含瞬态」是常态。
- **AD-7 计数单点 + 判定单点 + 真接线**: 计数只在 `write_gate_state`; 判定只在 CLI `record` 的 `should_prompt`; AI 经 subprocess 调 CLI 而非手写 JSON; 「真被调」的证据走声明式 `runtime_probe:` 归档门 (一次性, 有 source 分区 anti-spoof), 不做常驻 liveness (本项目 wait episode 稀疏, 常驻必恒红 — memory `false_green_dual_is_permanent_red`)。

## Impact

- **行为变化**: 零 run 场景 → `not_found` + `wait` + `gate_error`, ~90s 后带处方交人 (原恒 wait 到 1800s); PR 分支不存在 → `fail` (原恒 wait)。既有 verdict 路径零回归。
- **Schema (additive)**: `pr_ci_status` +`not_found`; `gate_error.kind` +`no-run-for-branch` +`pr-branch-not-found`; `gate_error` +`prompt_after_observations`; `path_coverage` +`dispatchable_workflows`; `gate_state` +`no_run_observations`; config +`no_run_prompt_after_observations` (+ 模板补 `path_coverage_enabled`); 内部签名 additive: `write_gate_state(gate_error_kind=)` / `_parse_workflow["dispatchable"]` / `_result(dispatchable_workflows=)` / 新函数 `_verify_branch_exists` `_effective_prompt_threshold` `_no_run_gate_error` `reset_no_run_observations` `reset_retry_count` + CLI。无删改, `format_version` 不变。
- **新 artifact**: `gate_state_helper.py` CLI / telemetry 分区 `.aria/gate-state-telemetry.jsonl` (gitignored) / `runtime_probe:` 声明 (首个采用者) / NEG-4 fixture + ab-results 记录 / `DISPATCH_VIABLE` 常量。
- **不改 (非「不受影响」)**: (b) 轴 (另案) / not_applicable 短路 / NIE / 六个早退 return 点契约 / path_coverage 规则与 reason 族。
- **版本**: aria-plugin PATCH **v1.66.5** (v1.66.4 已于 2026-08-22 由 #179 占用; 原「带出两个未发版 commit」已随 v1.66.4 带出, 不再适用)。

## Success Criteria (可证伪; 红窗 = 基线 `400f0bc` 必红; 每条能答「它怎么会红」)

| SC | 断言 | 基线 |
|---|---|---|
| SC-1 | `_normalize_pr_ci_status([]) == "not_found"` | 红 |
| SC-2 | `compute_verdict([], "not_found", cfg=None, path_coverage=pc)` 参数化 **2.3 表 6 档对应的 6 个 reason (真实载荷形态) + None** (not_applicable 两 reason 不可达, 由 SC-6 覆盖, R4 A4-m3): `verdict=wait`, `pr_ci_status=not_found`, `gate_error.kind=no-run-for-branch`, `raw_message == gate_error.message`, 含 `no-run-for-branch`; `workflow-trigger-matched` 含 `#152` + 全部 matched 名; `empty-diff` **不含** `#152`; `internal-error` 含「请报 issue」。**dispatch 子项** (仅 `dispatch_viable=true` 时存在, R4 A2-M1): `DISPATCH_VIABLE=True` + `dispatchable_workflows=[".forgejo/workflows/x.yml"]` → message 含 `workflows/x.yml/dispatches` 且**不含** `.forgejo/workflows/x.yml/dispatches` (basename 守卫); 常量 monkeypatch 为 False 或列表空 → message **不含** `dispatches` | 红 (基线 green) |
| SC-3 | `_effective_prompt_threshold`: None→3; `{"no_run_prompt_after_observations":5}`→5; `1`/`0`/`"x"`/`True`/缺键→3, 前四者各 warn 一次; `compute_verdict` 与 `gate_check` 路径对同一 cfg 回显相同 `prompt_after_observations` | 红 |
| SC-4 | `compute_verdict([{"run_id":1}], "not_found")` → `wait` **且 `gate_error.kind == "no-run-for-branch"`** (红窗在 kind; 误序实现此条红) | 红 (kind 缺) |
| SC-5 | gate_check 端到端 (mock backend `not_found`, 新名核验 mock `("ok","")`, `pr_branch="feat/x"`): (a) enabled → `path_coverage` 与 `gate_error` 同场, 六键俱在; (b) disabled → `gate_error` 在场、`path_coverage` 不在场, message 为「评估已关闭」档; (c1) **回填/同步断言** (所有变体): message **不含**字面 `<pr_branch>`, 且 `raw_message == gate_error.message` (副本通道在 gate_check 改写后重同步); (c2) **仅** `dispatch_viable=true` 时存在 (随 §3.5 条件 scope 组删除): enabled + pc stub = trigger-matched 含 dispatchable + `DISPATCH_VIABLE=True` 变体 → message **含** `feat/x` (回填真发生; R6 A1-M1/A4-m1: 其它档封闭表无占位符, 不得断言含分支名); (d) 核验 mock 返 `("verify-failed","boom")` → message 末尾含「核验失败: boom」且 raw_message 同步 | 红 |
| SC-6 | `decision=not_applicable` 下 `query_pr_ci.assert_not_called()` 且无 `gate_error`; 坏实现 (短路漏 `return`) 必红 | 绿 (守卫) |
| SC-7 | **六个早退 return 点 (八个变体)**: enabled:false `:418` / no-backend `:428` (fallback 两值 `:363`/`:376`) / precheck `:434` / main 核验 `:454` (两 kind `:455`/`:458`) / (b) 腿 AetherQueryError `:489` / (a) 腿 `:512` — 键集逐字不变 (前五类六键, main 核验七键); `not_applicable` 短路 `:498` 非早退 (走 compute_verdict, 含 path_coverage), 由 SC-6 覆盖 | 绿 |
| SC-8 | `_parse_workflow` 四例 `dispatchable` T/T/T/F 且 `triggers`/`covered_uncertain` 与基线逐字同 | 红 |
| SC-9 | `evaluate_path_coverage` 参数化 8 reason: `decision/reason/matched_workflows` 与基线逐字同; `dispatchable_workflows` 仅 `workflow-trigger-matched` 可非空且 ⊆ matched | 红 / 不变部分绿 |
| SC-10 | PR 消歧: 新名 mock 返 `not-found` → `verdict=fail`, `kind=pr-branch-not-found`, `raw_message == message`, `path_coverage` 在场 ⇔ enabled (两变体); 返 `verify-failed` → `wait` + `no-run-for-branch` + message 与 raw_message 同含「核验失败」; `pr_ci_status != not_found` 时新名 `assert_not_called`; 旧名包装对 `main_branch=` 关键字调用仍可用 | 红 |
| SC-11 | helper: (a) `write_gate_state(gate_error_kind="no-run-for-branch")` 三次 wait → `no_run_observations` 1/2/3 且 `retry_count` 0/1/2、`started_at` 不变; 中间一次 `None` → 0; (b) `reset_no_run_observations` 后其它键逐字不变; (c) v1.1 旧 state 无该键 `.get` 默认 0; (d) CLI `record --source test` 端到端: **state 文件不存在**起步两次调用 → stdout obs 1→2, **独立重读**落盘文件断言 `gate_state.no_run_observations == 2` 且 `status == "waiting"` 且 `retry_count == 1` (wait→waiting 映射, R3 #2) 且 `next_check_at` 按 `--intervals '[5,7]'` 计算; telemetry 两行 `source == "test"`; `--threshold 2` 第二次 `should_prompt=true`; `reset --observations` 后重读 obs=0 其余不变; `reset --retry-count` 后 `started_at` 更新; `reset`/`clear` 对缺失文件 exit 2; **缺 `--source` 或缺 `--state-file` 各 exit 2**; `--in-flight-runs '[{"run_id":1}]' --raw-message 'x'` 透传到落盘 `gate_state.in_flight_runs` / `raw_message` (R4 A4-M1); telemetry `ts` 可被 `datetime.fromisoformat` 解析; 坏实现 (整块重建漏 carry-forward, 或 stdout 自洽未落盘) 在重读断言必红 | 红 |
| SC-12 | 既有 119 + 22 全绿 + 新增; 跨 skill 全量绿; `:363` 翻转 | — |
| SC-13 | **活体** (实现后): throwaway 分支首推 path-matched 变更 → `pre_merge_gate.py --main-branch master --pr-branch <b>` 实测 `pr_ci_status=not_found` + kind; 经 workflow-runner 路径跑 wait 循环: **gate 在 aria-plugin 子模块根执行** (throwaway 分支在 aria-plugin; 主仓树内构造不出 `workflow-trigger-matched` — 主仓 workflow 的 paths 全指向子模块挂载点, R5 A1-M1), **state 文件 = 主仓 `.aria/workflow-state.json` 绝对路径** (`--state-file` 显式传, 这正是「gate cwd 与 state 文件位置两回事」的活体检验); `wait_check_intervals` 临时配 `[5,5,5]` 以免真等 90s → 主仓 `.aria/workflow-state.json` 出现 `no_run_observations` 且**主仓** `.aria/gate-state-telemetry.jsonl` 有 `source=production` 记录 (R4 A1-M2: 落子模块 `.aria/` 则 SC-16 结构上不可 pass) → 第 3 次观测出 prompt; 处置后轮询至非 `not_found` 或 600s; **先**把证据 (workflow-state 片段 + telemetry 行 + Δt) 抄进 traps §6 (分区本身 gitignored, 评审不可见, R3 #1), **再**收尾: 删分支 + CLI `clear` 主仓 gate_state (`clear` 置 gate_state=None, 抄录必须在其之前, R7 A1-m1; 否则 600s 零 run 那条腿留 `status=waiting` ⇒ 下个 workflow resume 幽灵 gate, R6 A1-m3) | 红 |
| SC-14 | 文档机检: SKILL.md 所有 `pr_ci_status` 枚举行含 `not_found`; `:172-183` 含 `gate_error`; config.template.json 含两 key; DEC 文末含「前向指针」且小节内含 📌 行; `path_coverage.py:36` 为 8 | 红 |
| SC-15 | `NEG-4-no-run-for-branch.json` 存在 **且登记进** catalog `fixtures[]` (含 `test_case_in_unit_tests` 绑定到 SC-2 的 trigger-matched 用例; catalog `version` bump + `changelog`); 元键集 = NEG-3 全集; **且真跑一次** (`/skill-creator` 或等价 harness) 结果落 `ab-results/<date>-pre-merge-gate-no-run-for-branch/` (R3 #9: NEG-3 零执行史不得复制); 回退本 spec 后 `test_case_in_unit_tests` 指向的测试转红 | 红 |
| SC-16 | 三条 (R4 A1-M1: pass 分支按 openspec-archive SKILL.md:234 **不落盘**, 不能同时断言「留 frontmatter」): (a) 前置可达 — A.2 产出 `detailed-tasks.yaml` (否则 L2 proposal-only 子态零评估); (b) **红窗** — SC-13 之前对本 spec 跑 `spec_complete.py` gate: probe outcome=`warn` + `unverified_claims` 含本 partition 条目; (c) SC-13 之后同一命令 outcome=`pass` (机读 gate JSON, 不依赖 frontmatter 落盘) | 红 |

## rule6_note (Rule #6 — 判据表**第三行**)

- §3.2/3.3 (`workflow-runner/SKILL.md` 2.5 + `phase-c-integrator/SKILL.md §C.2.4` 步骤 6): 处方性·运行时指令面, AB 套件覆盖外 — `phase-c-integrator.json` 3 evals / `phase-c-integrator-pre-merge-gate.json` **7** fixtures / `workflow-runner.json` 2 evals 无一到达 `not_found` (照跑 = 测量剧场); 同目录 `NEG-3-internal-error-surface` (#126) 先例走第三行。三义务: **点名行为** (两条, 单步可证伪: surface `gate_error.message` 原文; `should_prompt=true` 时出 prompt 而非继续等) + **定向 fixture** NEG-4 登记进 catalog (SC-15) + **套件缺口** 追加 **aria-plugin#127** (open, 正是 C.2.4 surface 义务零 eval 覆盖的缺口 issue) 评论 (§6.3)。序列型 (多轮 prompt) fixture 形态无消费机制 (`wait_then_green` 自陈 `_consumed_by: no consumer`), 明记为缺口不伪装已测。
- 配置表 / schema / 归层注记 / traps / config-loader / DEC / docstring 勘正: **描述性** → substitute = SC-1~SC-11, SC-14 结构化测试。
- 确定性代码层由 SC 覆盖, 与 AB 并行不互替。

## Out of Scope

- AI 自动执行处方 (dispatch / 推 commit) — v3 收缩, 若 owner 要求另起 follow-up。
- Aether CLI 改端点 (本 Forgejo 无 `/actions/runs`); Forgejo 上游 paths 语义 (候选 C)。
- (b) 轴对未被领取 run 的不可见 (§6.2 另案)。
- GHA backend; `CIBackend` 写能力; 重命名既有 kind; 序列型 AB fixture 消费机制 (#127)。

## Risks (残余)

- R-a (守卫): `gate_error` 全仓零外部消费方; SC-7。
- R-b (有界): 阈值依据薄, 后果 = 早一次 prompt。
- R-c (TASK-0a 裁决): dispatch 可用性只影响处方 (a) 行。
- R-d: 无人值守下 prompt ≡ abort, 与既有 timeout prompt 一致; v2.0 运行时自动处置属 orchestrator 另案。
- R-e: CLI 接线后 workflow-runner 每轮多一次 subprocess (~50ms); CLI 退出码 2 ⇒ AI surface + **直接 abort** (3d 终止分支), 禁回退手写 JSON (写进 SKILL)。
- R-f (新): 本 spec 是 `runtime_probe:` 首个采用者 — 若归档门解析/评估有未被 #95/#113 测试覆盖的缺陷, D.2 会暴露; 按 fail-toward-warn 设计不 block, 但须在 handoff 留痕并回报 state-scanner。

## Cross-references

- 先例: `openspec/archive/2026-07-31-phase-c-gate-path-coverage-not-applicable/` (#122) · aria-plugin #137 (`gate_error` 副本通道 + 核验三禁令) · #126 + NEG-3 (reason 自成一档 + Rule #6 第三行) · #127 (套件缺口) · `docs/decisions/DEC-20260731-001-*` (前向指针衔接, 格式沿 DEC-20260702-001:124-128) · `state-scanner/scripts/phase1_gate.py` + state-check `coordination-gate-invocation` (CLI 接线 + 运行时探针先例)
- 现场: `docs/handoff/2026-08-20-issue-batch-181-147-145-ship-and-gate-blindspot.md` · memory `reference_forgejo_new_branch_paths_filter_no_run` (TASK-0a 后按 traps 镜像修正)
- 审计: `.aria/audit-reports/post_spec-R1-…-aggregated.md` (17 簇) · `post_spec-R2-…-aggregated.md` (14 簇, 缩面判定)
- 规范: `skill-benchmark-exemption.md` (Rule #6) · `configured-gate-authority.md` (Rule #10) · Aria#177 (版本引用点口径) · `docs/decisions/DEC-20260705-001-runtime-probe-into-archive-gate.md` + `state-scanner/references/runtime-probe-declaration.md` (归档门探针声明, 本 spec 首个采用)
- 审计 R3-R6: `post_spec-R3-…-aggregated.md` (10 簇) · `post_spec-R4-…-aggregated.md` (5M → v5; 配额耗尽, owner +2 轮) · `post_spec-R5-…-aggregated.md` (2M → v6; 含对 R4 聚合的 erratum) · `post_spec-R6-…-aggregated.md` (1M → v7; 4/5 PASS + 条件 PASS)

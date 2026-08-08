# Proposal: premerge-gate-mainbranch-failclosed

> **Status**: 📝 **Draft (A.1)** — 待 post_spec
> **Created**: 2026-08-08
> **Spec Level**: **2** (单文件 + 其测试; 无跨模块, 无新需求 —— 缺陷修复但改变闸门语义故不走 Level 1)
> **关联 Issue**: [aria-plugin #137](https://forgejo.10cg.pub/10CG/aria-plugin/issues/137)
> **代码落点**: `aria/` 子模块 `skills/phase-c-integrator/`; Spec 落主仓 (Rule #5)
> **ship target**: aria-plugin v1.65.6 (PATCH — 缺陷修复, 无行为面扩大; 见 §版本)

---

## Why

### 缺陷

Rule #8 pre-merge gate 的「main 无 in-flight CI run」这条腿, 在本项目上**恒真**:

```python
# aria/skills/phase-c-integrator/scripts/pre_merge_gate.py
:300    main_branch: str = "main",                                    # ← 函数签名缺省
:427    parser.add_argument("--main-branch", default="main", ...)     # ← CLI 缺省
```

Aria 主分支是 **`master`**。调用方不显式传参时闸门去查 `main`。

### 为什么它是恒绿而不是报错 (实测, 2026-08-08)

```
$ aether ci status --branch main   --in-flight --json
{"status":"ok","data":{"filters":{"branch":"main","in_flight":true},"repo":"10CG/Aria","runs":[]}}   RC=0
$ aether ci status --branch master --in-flight --json
{"status":"ok","data":{"filters":{"branch":"master","in_flight":true},"repo":"10CG/Aria","runs":[]}}  RC=0
```

**两者返回完全同形。** 而 `AetherBackend.query_branch_in_flight` (`ci_backends/aether.py:117-135`) 只在 `aether` **自身失败**时抛:

```python
ok, data, err = self._query(branch=branch, in_flight_only=True)
if not ok:
    raise AetherQueryError(...)
main_runs_raw = data.get("runs") or []      # ← "分支不存在" 与 "分支无 run" 在此合流
```

⇒ **后端结构上无法区分「分支不存在」与「分支没有 in-flight run」**, 二者都产出 `InFlightStatus(runs=[])` ⇒ verdict 那一支判 green。

### 唯一现有约束是一句散文, 不是兜底

`phase-c-integrator/SKILL.md:242` 写着「`main_branch` 显式传真值 (本项目 `master`), 不依赖 CLI default」。

**那是指令, 不是机械兜底。** 任何忘记传参的路径 (人工直调 / 新写的编排 / 复制粘贴的命令) 都静默拿到恒绿的那条腿。本项目成文判据: memory `feedback_invariant_needs_failclosed_default` —— 「不变量写进文档 ≠ 写进兜底默认值; 枚举分区必须 fail-CLOSED」。**一个 Rule #8 闸门的缺省值指向恒绿, 是方向错的。**

### ⚠️ 对 issue #137 原文的一处订正 (本 Spec 起草时 probe 出)

#137 正文写「**两条腿都不触发且都失败为绿**」—— **只有 (b) 那条成立**。

实读 `path_coverage.py:24` 的规则 1: `git diff 失败 → unknown, reason=git-diff-failed`, 而 `unknown` 是 **fail-toward-covered** ⇒ **main 分支名错时 (a) 那条腿变得更保守, 不是变绿**。(a) 观测到的 `not_applicable` 来自「workflow `paths` 真的不覆盖本次变更文件」这个**设计内条件**, 与分支名无关。

⇒ 本 Spec **只治 (b)**。(a) 的 `not_applicable` 是既有设计, 不在范围。#137 正文已同批评论订正。

### 发现路径 (为什么 15 个 agent 没发现)

发现于 `linked-issue-normalization` 的 post_planning **R4** —— 前三轮 15 个审计 agent 未发现; R4 换 2 席从未接触该 Spec 的新鲜眼睛, 镜头限定「委派/兜底**是否真的拦得住**」, 由该席位**实跑闸门命令**时发现。

⇒ 「某个闸门在守着」这类表述必须**实跑那个闸门并核验它查的是什么**; 闸门存在 ≠ 闸门有判别力。

---

## What Changes

### 1. 两个 fail-OPEN 缺省一起去掉

| 落点 | 现状 | 改为 |
|---|---|---|
| `pre_merge_gate.py:427` CLI | `default="main"` | **无缺省** (`default=None`) |
| `pre_merge_gate.py:300` 函数签名 | `main_branch: str = "main"` | `main_branch: str \| None = None` |

**两处必须同批改。** 只改 CLI 会留下函数签名这条内部调用路径仍恒绿 —— 与本 Spec 要治的病同形。

### 2. 未显式传参时的解析: 从 remote HEAD 取真值, 失败即 abort

`main_branch is None` 时:

1. `git symbolic-ref refs/remotes/<remote>/HEAD` → 取 `origin/master` 的 `master`;
2. 解析失败 (无该 ref / 命令失败 / 输出不可解析) ⇒ **abort, verdict=`error`** —— ⛔ **不得回落任何字面缺省**。

> **为什么不 fallback 到 `master`**: 那只是把 fail-OPEN 从 `main` 挪到 `master`。判据是「**这个信号在健康常态下应是什么值**」—— 解析不出主分支名时, 闸门**没有能力判断**, 正确输出是 `error` 不是 green (memory `feedback_false_green_dual_is_permanent_red`)。

### 3. 分支存在性核验 —— 本 Spec 的承重条款

查 in-flight **之前**, 独立核验该分支在目标 remote 上**存在**:

```
git ls-remote --exit-code --heads <remote> <main_branch>
```

- 存在 → 继续原流程;
- **不存在 → verdict=`error`**, message 点明「主分支 `<name>` 在 remote `<remote>` 上不存在 —— 这不是『无 in-flight run』」;
- **`ls-remote` 自身失败 → 重试后仍失败则 verdict=`error`** (对齐 CLAUDE.md 硬约束 2 的「ls-remote 自身失败 → 重试几次再下结论」), ⛔ 不得当成「存在」也不得当成「不存在」。

> **为什么核验必须在 gate 层而非 backend 层**: backend 是薄适配器 (Aether / GHA-stub 各一份), 存在性核验是**策略**。放 gate 层一处即对所有 backend 生效; 放 backend 层要写 N 份且新 backend 会漏。

### 4. verdict 回显实际查询的分支名

`gate_result` 输出中回显 `main_branch_resolved` + 其来源 (`explicit` / `symbolic-ref`), 使「查错了分支」在 surface 上**可见**而非只能靠读代码推断。

### 5. `SKILL.md:242` 的散文同步

该处「`main_branch` 显式传真值, 不依赖 CLI default」在机械兜底落地后**语义改变** —— 从「你必须记住传」变成「不传会自动解析, 解析不出会 abort」。同批订正措辞。

**Rule #6 (rule6_note)**: 改动面 = `pre_merge_gate.py` 的参数缺省与一段存在性核验 + 其测试 + **一处 SKILL.md 散文勘正**。**零 `description` 变更、零 frontmatter 变更、零运行时指令流程新增** (指令面是**减少**一条人工义务, 由机械兜底替代)。

| hunk | 判据 | 处置 |
|---|---|---|
| `pre_merge_gate.py` + 测试 | 纯 Python, 零 AI 指令面 ⇒ 判据表**第一行「描述性」** | **substitute: SC 级 baseline-failing 结构化测试替代** |
| `SKILL.md:242` 散文勘正 | 该句由「人工义务」降为「机制说明」⇒ 判据表**第一行「勘正」** | **substitute**, 同上 |

**不申请豁免**; substitute 的证据面 = 下方 SC 的 baseline-failing 集合, **须在 Phase B 实跑留证而非声称** (owner 2026-08-02 裁定 `db2e983`)。

---

## 决策记录

| # | 决策 | 要点 |
|---|------|------|
| **D1** | 两个缺省**同批**去掉 | 只改 CLI 会留函数签名这条内部路径恒绿, 与要治的病同形 |
| **D2** | 未传参时从 `refs/remotes/<remote>/HEAD` 解析, **解析失败 abort** | ⛔ 不回落字面缺省 —— 那只是把 fail-OPEN 挪个地方 |
| **D3** | **存在性核验放 gate 层**, 不放 backend | backend 是薄适配器 ×N; 策略放一处才对所有 backend 生效 |
| **D4** | `ls-remote` 自身失败 ⇒ `error`, **不猜** | 对齐 CLAUDE.md 硬约束 2; 「查不到」≠「查到了且是空的」正是本缺陷的要害 |
| **D5** | 回显 `main_branch_resolved` + 来源 | 使假绿在 surface 可见 (D9 可观测性同族) |
| **D6** | **只治 (b) 腿**, 不动 `path_coverage` | probe 实证 (a) 在分支名错时**更保守**; #137 原文该句已订正 |
| **D7** | PATCH 而非 MINOR | 无行为面扩大 —— 修的是「本应能判而判不了」; 且会**使某些此前 green 的调用转 error** (那是修复不是回归, 见 §Impact 风险) |

---

## Success Criteria

| SC | 场景 | 期望 | 怎么会红 |
|----|------|------|---------|
| **SC-1** | CLI 不传 `--main-branch`, repo 的 `refs/remotes/origin/HEAD` → `master` | 解析出 `master` 并据此查询; `gate_result.main_branch_resolved == "master"`, 来源 `symbolic-ref` | 现状 `default="main"` ⇒ 查 `main` ⇒ 必红 |
| **SC-2** | 直接调 `run_gate(...)` **不传** `main_branch` (走函数签名那条路径) | 同 SC-1 | 现状函数签名 `= "main"` ⇒ 必红。**本条是唯一覆盖内部调用路径的用例** |
| **SC-3** | 显式传 `--main-branch master` | 行为与现状一致 (不因本 change 改变) | 负控 —— baseline 应为**绿**; 若红说明改坏了既有路径 |
| **SC-4** | 传一个 remote 上**不存在**的分支 (如 `--main-branch main`) | verdict=**`error`**, message 含分支名与 remote 名, 且**明确区别于「无 in-flight run」** | 现状返回 `InFlightStatus(runs=[])` ⇒ 判 green ⇒ 必红。**本条是本 Spec 的承重断言** |
| **SC-5** | `git symbolic-ref refs/remotes/<remote>/HEAD` 失败 (ref 缺失) 且未显式传参 | verdict=**`error`**, ⛔ **不得**回落 `main` 或 `master` | 「解析失败就用 master」的实现在此必红 |
| **SC-6** | `git ls-remote` 自身失败 (网络/权限) | 重试后仍失败 ⇒ verdict=**`error`**; ⛔ 不得判「存在」也不得判「不存在」 | 把 ls-remote 失败当成「分支不存在」的实现 → 误报; 当成「存在」的实现 → 恒绿。两个方向都红 |
| **SC-7** | 分支存在**且**有 in-flight run | verdict 与现状一致 (`wait`) | 负控 —— 存在性核验不得改变正常路径的判决 |

**substitute 证据面 = SC-1 / SC-2 / SC-4 / SC-5 / SC-6 五条中的 baseline-failing 者** (全表 7 条 SC, 其中 SC-3 / SC-7 为负控), 须于 Phase B **实跑留证**并把红集合写进本文件 (口径同 `linked-issue-normalization` 的 baseline 表)。SC-3 / SC-7 是负控, 恒绿正确, **不算证据面**。

---

## 非目标

- **不改** `path_coverage.py` —— (a) 腿的 `not_applicable` 是设计内条件 (D6);
- **不改** `aether` CLI 的返回语义 —— 「不存在的分支返回 ok+空」是它的行为, 本 Spec 在消费侧兜住, 不改上游;
- **不改** `branch-manager` 的合并动作 —— 那是 **aria-plugin #136** (子模块服务端合并), 独立 Spec;
- **不给** `phase-c-integrator` 加 gate-only 形态 —— 那是 #136 的耦合面 (post_planning R4/C2);
- **不动** `no_ci_fallback` / stub backend 的既有降级语义 (Rule #8 SOT)。

---

## Impact

| 文件 | 变更 |
|------|------|
| `aria/skills/phase-c-integrator/scripts/pre_merge_gate.py` | 两处缺省去掉 (`:300` 签名 / `:427` CLI) + `main_branch` 解析 + 存在性核验 + verdict 回显 `main_branch_resolved` |
| `aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py` | 扩展 — SC-1..SC-7 (既有用例逐字不改) |
| `aria/skills/phase-c-integrator/SKILL.md:242` | 散文勘正 (人工义务 → 机制说明) |
| 发版同步面 | aria 子模块版本面 + 主仓版本引用面 —— **按引用点而非文件数枚举**, 判据见 `linked-issue-normalization` 的 5.11 (整仓差集 + append-only 账本另判); 类级根因见 **Aria #177** |
| 版本 | **v1.65.6 PATCH** |

### 风险

**本 change 会使某些此前判 green 的调用转 `error`** —— 具体是「未显式传 `--main-branch` 且 remote HEAD 解析不出」与「传了不存在的分支」两类。

⇒ **这是修复不是回归**: 那些 green 本来就是假绿 (闸门没有能力判断却放行)。但 Phase B 须核: 仓内**是否存在**依赖旧缺省的调用点 (grep `pre_merge_gate` 全部调用方), 有则同批改为显式传参或依赖新解析。

### 测试基线

`phase-c-integrator` 现 **111** tests (2026-08-08 `run_all_tests.sh` 实测)。本 change 新增按 SC 计 **≥7**。全量跨 skill 套件须绿。

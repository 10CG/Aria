# Proposal: premerge-gate-branch-existence

> **Status**: 📝 **Draft (A.1)** — 由 [DEC-20260812-001](../../../docs/decisions/DEC-20260812-001-premerge-gate-spec-split.md) 从
> `premerge-gate-mainbranch-failclosed` 拆出的 **A 侧**。
> **Created**: 2026-08-12
> **Spec Level**: **2** (proposal only) —— 无架构变更, 无跨仓同步面, 无破坏性契约变更
> **版本**: **MINOR** —— 本 change 全部为 additive (新增可选参数 + 新增核验步 + 新增 additive 输出键),
> **零破坏面** ⇒ 不触发 `pre_merge_gate.py:68/:116` 的 v2.0 弃用到期承诺
> **关联 Issue**: [aria-plugin #137](https://forgejo.10cg.pub/10CG/aria-plugin/issues/137)
> **代码落点**: `aria/` 子模块 `skills/phase-c-integrator/`; Spec 落主仓 (Rule #5)
> **姊妹 Spec**: `premerge-gate-mainbranch-failclosed` (B 侧, Level 3, MAJOR)
>
> ⚠️ **本 Spec 的输入不是从零起草的** —— 下列材料承自 A/B 拆分前的八轮 40 席审计
> (post_spec R1–R5 + post_planning R1–R4), 逐条注明来源。**但拆分后的组合是新的, 须重新过 post_spec。**

---

## Why

### 症状 (承前, 逐字保留)

Rule #8 pre-merge gate 的「main 无 in-flight CI run」这条腿在本项目上**恒真**。
后端**结构上无法区分**「分支不存在」与「分支没有 in-flight run」—— 实测 `--branch main`
与 `--branch master` 返回完全同形 (`status:ok`, `runs:[]`, RC=0); `ci_backends/aether.py:117-135`
只在 aether 自身失败时抛。二者都产出 `InFlightStatus(runs=[])` ⇒ 判 **green**。

### 本 Spec 的范围判定 (DEC-20260812-001 §3)

**存在性核验单独就消除了那个不可区分性** —— 传 `--main-branch main` 而 `main` 在远端不存在时,
核验判 `fail` + `kind="main-branch-not-found"`, **不再 green**。

⇒ 本 Spec **只做这一件事**, 且它是**纯 additive**:
- `gate_check(..., remote: str = "origin")` **带默认值** ⇒ 既有 24 处调用零改动;
- 新增核验步插在既有早退之后 ⇒ 既有分支语义零改动;
- `gate_error` 是 **additive 可选键** ⇒ 六键 schema 零改动。

**⛔ 不在本 Spec 范围** (全部留 B 侧):
`--main-branch` 改必填 (破坏性, 拉 MAJOR 与弃用面) · `SKILL.md` 两处散文收敛为 helper 调用 (D1) ·
折叠块 · helper 路径解析 spike · v2.0 弃用删除面 · 发版同步面 · Rule #6 AB。

> **为什么必填留 B**: 它是**纵深防御的第二层** (防「显式传错分支名」), 价值真实,
> 但**不是关掉恒绿腿的必要条件**; 而它一旦进来就拉着 MAJOR ⇒ v2.0 弃用到期承诺
> ⇒ 跨两仓 5 文件 + 两个 legacy key + `.aria/config.template.json` 这个仓外受众落点。

---

## What Changes

### 1. 新增 `--remote` 参数 (additive)

`gate_check(..., remote: str = "origin")` / CLI `--remote`, 默认 `origin`。

**失效方向不对称的理由** (承 B 侧原 R5 结论): 错 `remote` 走 **128** ⇒ fail-CLOSED;
错 `branch` 走 `runs:[]` ⇒ fail-OPEN。**这就是 `remote` 可以有缺省的理由**
(而 `main_branch` 能否有缺省是 B 侧的题目)。

### 2. 分支存在性核验 — 判据是**精确字符串比对**, 不是 pattern 匹配, 更不是退出码

在查 in-flight **之前**, 独立核验 `<main_branch>` 在 `<remote>` 上确实存在。

**⚠️ 三次受控实验才收敛到正确判据** (前两次均 fail-OPEN):

| 修法 | 实测 | 结论 |
|---|---|---|
| 裸分支名 `--heads <r> master` | 远端只有 `refs/heads/wip/master` 时返 **RC=0** (尾段 glob) | ❌ fail-OPEN |
| 锚定 `--heads <r> "refs/heads/master"` | **锚定也关不掉 glob** —— 受控裸仓实测 `refs/heads/mast*` / `refs/heads/m[a]ster` / `refs/heads/maste?` **仍全部命中** | ❌ 仍 fail-OPEN |
| **对返回的 ref 名做精确字符串比对** | 不依赖 pattern 语义 | ✅ **本 Spec 采用** |

⇒ 判据: **远端返回的 ref 名列表中, 是否存在一条 `== "refs/heads/" + main_branch` 的精确匹配**。

**🔴 两条更底层的事实 (2026-08-11 主 loop 受控裸仓实验; 八轮 40 席从未浮出)**:

- **`ls-remote` 零命中亦返 `rc=0`** —— 实测 `refs/heads/wibble` (不存在) ⇒ **rc=0 + 零行输出**
  ⇒ **任何以退出码判存在性的实现, 对本 Spec 的主场景天然 fail-OPEN**。
  ⇒ **判据必须落在解析出的 ref 名列表上, 不得读退出码。**
- **⛔ 不得使用 `--exit-code`** —— 实测它使「无命中」返 **rc=2**。那是实现者最可能选的
  「更简单」替代路径, 但本 Spec 的退出码表以「其余一切非零 ⇒ `main-branch-verify-failed`」收口
  ⇒ **一个合法缺失的分支会被误分类成「查询失败」而非「分支不存在」** (SC-M6 会抓到它, 但应在 Spec 层直接排除)。

**具体实现形态** (是否仍借 `ls-remote` 取列表 / 如何解析) = **Phase B spike**;
验收由 SC-A6 + SC-A13 钉住。

| 情形 | 判据 | 输出 | 重试? |
|---|---|---|---|
| ref 列表含**精确匹配** | — | 继续原流程 | — |
| ref 列表**取到了但无精确匹配** | 分支不存在 | `verdict=fail` + `gate_error.kind="main-branch-not-found"` | **否** |
| subprocess timeout (`TimeoutExpired`) | 查询失败 | 按 `SKILL.md:259` 既有规范重试; 仍超时 ⇒ `fail` + `kind="main-branch-verify-failed"` | **是** |
| **其余一切** — 非零退出码 (实测 remote 名不存在 / 坏 URL / 网络不可达均为 **128**) · `FileNotFoundError` (git 二进制缺失, **抛异常无退出码**) · `OSError` · 输出不可解析 · **任何未枚举情形** | 查询失败 | `verdict=fail` + `kind="main-branch-verify-failed"` | **否** |

> 本表以「其余一切」**收口 (catch-all)**, 不是正向枚举 —— 正向枚举对未来新增返回码天然 fail-OPEN。
> **不援引 `SKILL.md:260` 的 exit 1-126**: 实测真实失败码是 **128**, 在区间外; 且 `:260` 自带
> `127 → no_ci_fallback` 会使 verdict 变 **green**。

⛔ 任何情形都不得当成「存在」放行。

### 3. 核验点 = 三个早退**之后**、`evaluate_path_coverage` **之前**

**五个行锚已由主 loop 逐个实读命中** (基线 `af87cae`, 落地时按内容锚重定位):

```
:328  if not cfg["enabled"]:            → 早退 (green)
:338  if backend is None:               → 早退
:344  ok, precheck_err = backend.precheck()
:345  if not ok:                        → 早退 (fail)
★ 存在性核验 (本 Spec 新增)              ← 唯一合法插入点
:356  pc: dict[str, Any] | None = None
:357  if cfg.get("path_coverage_enabled", True):
:358      pc = evaluate_path_coverage(main_branch=main_branch, pr_branch=pr_branch)
:366  in_flight = backend.query_branch_in_flight(main_branch)
```

**在三早退之后**: 否则 owner 显式关闭的闸门与 `no_ci_fallback` 既有降级会被变成 `fail`。
**在 path coverage 之前**: 它更早消费 `main_branch`, 放它之后等于放行一次未核验的使用。

⛔ **不得为解析路径而 `cd`** —— 那会使 `ls-remote` 查错仓 (主仓与 `aria` 子模块都有 `master`, 会 RC=0 假通过)。

### 4. 诊断信息: `raw_message` 是主通道, `gate_error` 是 additive 副本

`SKILL.md:255` **逐字**规定 `fail` 的 surface 通道是 `raw_message`
(「`fail` → BLOCK + 输出 verdict + raw_message, phase-c-integrator return failure」),
且 `write_gate_state()` 签名无 `gate_error` 形参。

- **`raw_message` 主通道 (必填)**: 失败时须写入人类可读诊断, **含分支名与 remote 名**,
  且**明确区别于「无 in-flight run」**;
- **`gate_error` 是 additive 可选结构化副本** (沿用 v1.65.0 `path_coverage` 先例):

```json
"gate_error": {
  "kind": "main-branch-not-found",
  "remote": "origin",
  "branch": "<MAIN_BRANCH>",
  "message": "同 raw_message"
}
```

> 示例的 `branch` 用**占位符**而非真值 —— 写 `"main"` 会与 B 侧的 SC 对撞。
> ⚠️ **已知**: `gate_error` 全仓**零消费者** (实测 `grep -rn 'gate_error' aria/` = 0),
> `workflow-runner` 的 verdict 路由只有四条臂、**无异常臂**。
> ⇒ 本 Spec **不依赖**它发红; 发红完全由 `verdict="fail"` + `raw_message` 承担。

**在场范围**: `SKILL.md:279` 逐字是**四类早退** (`enabled:false` / no-backend / precheck 失败 /
backend query 失败) 保持**六键不变**; `gate_error` **只在本 Spec 新增的核验失败路径在场**。

### 5. 异常与重试: 按**轴**分派两个既有先例, ⛔ 不得再造

| 轴 | 先例 | 实测状况 |
|---|---|---|
| **异常枚举** | `path_coverage.py:93` 的 `(TimeoutExpired, FileNotFoundError, OSError)` 三合一 | ✅ 可复用的是**这条 except 元组的枚举**, **不是** `_run_git()` 函数本身 (它把异常与非零退出码折成同一 `ok=False`, 使 SC-A7/A8 无从分辨) |
| **重试** | `aether.py:38` 的 `RETRY_BACKOFF=(5,15,45)` / `MAX_RETRY_ATTEMPTS=3` | ✅ **正是 `SKILL.md:259` 逐字规定的那套**; ⚠️ 但 `_run_with_retry(:164-187)` 硬绑 `[self.binary]`、**只捕 `TimeoutExpired`** (docstring 自陈「other exceptions bubble up」)、无 `cwd` 参数、`text=True` 严格解码 (对 git 输出会抛 `UnicodeDecodeError`, 见 `path_coverage.py:81-84` 的 #124 教训) |

⇒ **复用形态 = Phase B spike**。若需改 `aether.py` 抽取共享重试, 该文件须入 scope,
且**行为等价的判据不得用「`test_ci_backends.py` 25 tests 全绿」** —— 实测
`grep -c '_run_with_retry' tests/test_ci_backends.py` = **0**, 那 25 条**系统性绕过它** ⇒ 该判据恒绿。

### 6. 测试隔离接缝

`test_sc22_no_real_git_subprocess_in_suite` (`:710`) 的 patch **本就全局生效**
(`import subprocess` 使模块对象共享 —— 主 loop 实读 `:718` `mock.patch.object(pc_module.subprocess, "run", ...)` 确认)。
⇒ 本 Spec 新增 gate 层 subprocess 后该守卫会**转红**。

须建**独立打桩接缝**, 使守卫**保持有效而非被放宽**; 同时保证 SC-A6/SC-A13 能用真实 git 受控裸仓。
**粒度 (函数级 vs subprocess 级) 由 Phase B spike 定。**

---

## Success Criteria

> SC 编号用 **`SC-A*`** 前缀 —— 与 B 侧的 `SC-M*` 及既有 `test_path_coverage.py` / `test_pre_merge_gate.py`
> 的 SC 号段**全部不冲突** (B 侧曾因编号冲突被 post_planning 判 Critical, 此处预防)。

| SC | 断言 | 期望 | 今日实测 | 怎么会红 |
|----|------|------|------|---------|
| **SC-A6** | 受控裸仓: 远端只有 `refs/heads/wip/master`, 传 `--main-branch master` | `verdict=fail` + `kind=="main-branch-not-found"` + **`raw_message` 含分支名与 remote 名** | 今日无核验 ⇒ green | 必红。**承重断言**。**用真实 `ls-remote`, 不打桩** |
| **SC-A13** | 受控裸仓: 远端只有 `refs/heads/master`, 传 `--main-branch 'mast*'` (及 `m[a]ster` / `maste?`) | `verdict=fail` + `kind=="main-branch-not-found"` | 三 pattern 实测对该远端**全返 RC=0 且命中** | **锚定 pattern 实现必红** —— 本条钉住「精确比对」而非「锚定」 |
| **SC-A-zero** | 受控裸仓: 远端只有 `refs/heads/master`, 传 `--main-branch develop` (**零命中**) | `verdict=fail` + `kind=="main-branch-not-found"` | `rc=0` + **零行输出** | **读退出码的实现必红** (它会把 rc=0 当成功) |
| **SC-A7** | `ls-remote` 返 **128** (指向不存在的 remote 名, 或 mock) | `fail` + `kind=="main-branch-verify-failed"`, **未重试** | — | 当「不存在」→ 误报 / 当「存在」→ 恒绿, 两向都红 |
| **SC-A8** | `ls-remote` 抛 `TimeoutExpired` (**mock**; 须 mock `time.sleep`) | 3 attempts 后 `fail` + `kind=="main-branch-verify-failed"` | — | 未按 `:259` 重试的实现红; 未 mock sleep 致 >60s 亦红 |
| **SC-A10** | 负控: `enabled=false` 早退 | 六键不变、无 `gate_error`, **且 `assert ls-remote 未被调用`** | — | 缺后半条因果断言则健康与不健康实现都绿 |
| **SC-A10b** | 负控: no-backend (`:338`) 早退 | 同上, **各带 `assert ls-remote 未被调用`** | — | 兄弟早退不同步则该类只修了一个实例 |
| **SC-A10c** | 负控: precheck 失败 (`:345`) 早退 | 同上 | — | 同上 |
| **SC-A11** | 负控: 分支存在且有 in-flight | `verdict=wait` 不变 | — | 核验不得改变正常路径判决 |
| **SC-A14** | catch-all: `FileNotFoundError` / `OSError` / 输出不可解析 | 一律 `fail` + `kind=="main-branch-verify-failed"` | — | 正向枚举的实现对未枚举情形会漏 |
| **SC-A-sc22** | 既有 `test_sc22` (`:710`) 落地后**仍 PASS 且仍能拦住真实 git 子进程** | 用一个**故意违规的桩**验证它会红 | 今日 PASS | 被放宽 (而非建接缝) 的实现红 |
| **SC-A-baseline** | `phase-c-integrator` 全量套件 | **111 + 新增 ≥ 全绿** | **111 passed** (2026-08-11 实跑) | 任何回归红 |

**打桩边界 (钉死)**: **SC-A6 / SC-A13 / SC-A-zero 用真实 `ls-remote` + 受控裸仓**;
**SC-A7 / SC-A8 必须 mock** (真实 `ls-remote` 无法产出确定性 128 或 timeout)。

---

## Rule #6

`rule6_note`: 本 change **不改 `SKILL.md` 的 `description` 或指令流程** ——
`SKILL.md` 侧仅需 `:267` schema 增 `gate_error`、`:279` 四类早退注记同步 (**描述性**)。
按 `standards/conventions/skill-benchmark-exemption.md` 判据表**第一行**
(描述性 / schema / 字段) ⇒ **substitute: SC 级 baseline-failing 结构化测试替代**,
本 Spec 的 SC-A6 / A13 / A-zero 即是。

> ⚠️ **须在 A.2 逐行点名**该 `SKILL.md` 变动并声明非指令语义变更 (SOT `:33` 的附加约束);
> 若届时判定触及指令流程 ⇒ **一律第二行, 照跑 AB, 零裁量**。
> **拿不准照跑** —— 本 Spec 不申请任何豁免。

---

## 非目标

- **不改** `--main-branch` 的缺省 (B 侧 D5);
- **不改** `SKILL.md` 两处散文流程 / 不建折叠块 (B 侧 D1);
- **不引入** `main_branch` 自动解析 —— 实测 `ls-remote --symref` 存在 RC=0 但无 `ref:` 行两态 (unborn / detached), 需独立设计;
- **不改** `path_coverage.py` 代码与行为;
- **不改** `aether` CLI 返回语义;
- **不改** `workflow-runner` 的 `gate_state` schema;
- **不动** `no_ci_fallback` / stub backend 既有降级语义 —— 由 **SC-A10 / A10b / A10c 三条**机械钉住;
- **不修**同形兄弟位置 —— `phase-d-closer/fetch_gate.py` 的字面 `("master","main")` 回落 ·
  `state-scanner/lib/worktree_manager.py:170` 的 `base_branch: str = "master"`。
  ⚠️ **Phase B 实施者不得照抄 `fetch_gate.py`**。开 follow-up。

---

## Impact

| 文件 | 变更 |
|------|------|
| `aria/skills/phase-c-integrator/scripts/pre_merge_gate.py` | `--remote` / `remote` 参数 · `_verify_branch_exists()` · `raw_message` 诊断 + `gate_error` additive 键 · 核验点插入 |
| `aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py` | SC-A* 新增用例 · **为 gate 层核验建独立打桩接缝** |
| `aria/skills/phase-c-integrator/SKILL.md` | **仅描述性**: `:267` schema 增 `gate_error` · `:279` 四类早退注记同步 |
| `aria/skills/phase-c-integrator/scripts/ci_backends/aether.py` | **条件性** —— 仅当 spike 判定须抽取共享重试 helper 时入 scope |
| 外部 | **无外部动作** —— 不改 #137 body, 不发评论。留痕与否由 owner 决定 |
| 发版同步面 | **MINOR, 走常规发版流程**; 不触发 v2.0 弃用删除面 |

### 版本

**MINOR。** 全部为 additive: 新增**带默认值**的可选参数 · 新增核验步 (插在既有早退之后, 既有分支语义零改动) ·
新增 **additive 可选**输出键。**既有 24 处 `gate_check(` 调用零改动。**

⇒ **不触发** `pre_merge_gate.py:68/:116` 的「removed in v2.0」弃用到期承诺 (那是 B 侧的题目)。

### 测试基线

`phase-c-integrator` 现 **111 tests** (`test_pre_merge_gate.py` 46 + `test_ci_backends.py` 25 +
`test_path_coverage.py` 40) —— **2026-08-11 主 loop 实跑 `111 passed` 确认, 红窗前提成立。**

---

## 承自八轮审计的输入 (逐条注明来源, 供 post_spec 复核)

| 事实 | 来源 | 已实测? |
|---|---|---|
| 五个插入点行锚 (`:328`/`:338`/`:344`/`:345`/`:356`/`:357`/`:358`/`:366`) | 原 §6 | ✅ 主 loop 逐行实读命中 |
| `SKILL.md:255` = `fail` 的 surface 通道是 `raw_message` | 原 §7 | ✅ 逐字实读 |
| `SKILL.md:279` = **四类**早退保持六键 | 原 §7 | ✅ 逐字实读 |
| `SKILL.md:259`/`:260` 重试规范与退出码映射 (含 `127 → no_ci_fallback`) | 原 §5 | ✅ 逐字实读 |
| 锚定 pattern 仍 fail-OPEN | 原 §5 (两次实验) + 主 loop 第三次受控裸仓 | ✅ |
| **`ls-remote` 零命中亦返 rc=0** | **主 loop 2026-08-11 新发现** | ✅ 受控裸仓 |
| **`--exit-code` 无命中返 rc=2** | **主 loop 2026-08-11 新发现** | ✅ 受控裸仓 |
| `test_sc22` patch 全局生效 + `:723` 未传 `main_branch` | 原 §测试隔离 | ✅ 实读 |
| `gate_error` 全仓零消费者 / workflow-runner 仅四条臂 | post_planning R1 对抗复核 | ✅ 实跑 |
| `_run_with_retry` 硬绑 binary / 只捕 TimeoutExpired / 无 cwd / `text=True` | post_planning R2/R3 | ✅ 实读 |
| `test_ci_backends.py` 25 tests **零命中** `_run_with_retry` ⇒ 该判据恒绿 | post_planning R2 | ✅ 实跑 |
| 测试基线 111 passed | 主 loop | ✅ 实跑 |

⚠️ **拆分后的组合是新的** —— 上表每条单独已验, 但**它们在本 Spec 里的组合关系未经审计** ⇒ 须走 post_spec。

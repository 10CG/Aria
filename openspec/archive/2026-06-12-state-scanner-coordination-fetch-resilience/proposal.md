# state-scanner-coordination-fetch-resilience

> **Status**: ✅ **SHIPPED 2026-06-12** (aria-plugin **v1.46.0**, PR [#82](https://forgejo.10cg.pub/10CG/aria-plugin/pulls/82) merge `2d9bbb3` + release `e45ed3c` 双远程 parity; 主仓 gitlink → `e45ed3c`)。post_spec R1 REVISE (4/5, 8 major) → Rev1 → **R2 PASS 5/5 unanimous**。Phase B 全 cycle: TG-A/B/C + 12 新测 (803 全绿, 1 已知 flake 无关) + dogfood (no-coord sandbox 修复确证 + Aria 零回归) + code-review (code-reviewer PASS + silent-failure-hunter → 限制文档化 + 3 follow-up)。Closes Aria #141 软错误① + aria-plugin #75。
> **Level**: 2 (Minimal — proposal + tasks)
> **Target skill**: `aria/skills/state-scanner` (aria-plugin)
> **Target version**: v1.45.0 → **v1.46.0** (MINOR — 见 §Impact Versioning; Rev1 PATCH→MINOR per 先例 parity) / 主仓 gitlink bump
> **Forgejo issue**: [Aria #141](https://forgejo.10cg.pub/10CG/Aria/issues/141) 软错误① + [aria-plugin #75](https://forgejo.10cg.pub/10CG/aria-plugin/issues/75) (同一 bug 两处跟踪) — triage verdict `partial-repro` / `major` / `next-cycle` (`.aria/triage-report.json`, comment-12658)
> **triage 范围说明**: #141 软错误②(handoff_multibranch cap) 已在 v1.38.0 #71/#72 修复, **不在本 Spec 范围**; 本 Spec 仅修软错误①(coordination_fetch 原子 fetch)。
> **Rev1 (post_spec R1, 4/5 REVISE → 落地)**: 版本 PATCH→**MINOR** (tech-lead, 先例 git-operation-awareness parity); 锁 4 OQ (benign 三重 AND 闸 / coordination_ref_present 三态 + cache 持久化防漂移 / Fetch ordering 短路 / Fetch2 非 benign = soft_error 无需新 API); `success`/`degraded` 语义变化正视 (shape✅ + 语义⚠); `state-snapshot-schema.md` 新建 (非更新) coordination_fetch section; `lib/coordination_ref.py::fetch_coordination_ref` 显式 out-of-scope + follow-up; normalize DROP_KEYS 裁定不 drop + stability 回归。

## Why

`collectors/coordination_fetch.py` 是 state-scanner Phase 1.16 (multi-terminal-coordination) 的远端协调数据采集器。它在**一条原子 `git fetch`** 里同时拉取分支头 (`+refs/heads/*`) 和协调 ref (`refs/aria/coordination`)。

### Problem — coordination ref 缺失致整条 fetch 原子失败

`_build_fetch_refspecs()` (L75-86) 返回 `["+refs/heads/*:refs/remotes/<remote>/*", "refs/aria/coordination"]`, L246 合成单条 `git fetch <remote> --no-tags <两 refspec>`。

**远端从未发布 `refs/aria/coordination` 的项目** (即多数**未使用多终端协调**的项目, 如 SilkNode) 上, 这条 fetch **每次必失败**:

```
$ git fetch origin --no-tags '+refs/heads/*:refs/remotes/origin/*' refs/aria/coordination
fatal: couldn't find remote ref refs/aria/coordination
fatal: the remote end hung up unexpectedly
Forgejo: Failed to execute git command   → rc=128
```

**根因** (已对 aria submodule `a398b65` v1.45.0 代码核查 + live 复现确认, triage case-1 match=true):
1. git fetch 多 refspec 时, 其中一个 concrete ref 在远端不存在 → **整条 fetch 原子 abort** (rc=128), 即便 `+refs/heads/*` 通配本身有效。
2. `_classify_error(128, stderr)` (L160-193): stderr `couldn't find remote ref` / `the remote end hung up` 不匹配任何 network/auth/non_ff signal → 落 `"other"` → `r.soft_error("coordination_fetch_failed", "other: git fetch failed with rc=128")`。
3. 原子失败连带 `+refs/heads/*` 分支头也**未刷新** —— 该 collector 对远端分支视图的贡献退化 (这些项目**从无**成功 fetch → `_write_cache` 永不触发 → `success=False` 每次发生)。

**关键**: 这是**确定性**失败 (每次 scan 必发), 非环境抖动。手动 `git fetch origin <branch>` 正常, 证明网络/凭据无问题。

### Impact (若不修)

- 所有未发布 `refs/aria/coordination` 的项目 (多数) 每次 `/state-scanner` 都吃一条 `coordination_fetch_failed` soft_error → snapshot `errors[]` 固定噪音 + exit code 10 (而非 0)。
- 该 collector 负责的 `+refs/heads/*` 分支头刷新被原子失败连累, 远端分支视图保鲜依赖其他 collector 兜底。
- `kind=other` 掩盖真实分类 —— 良性的 "coordination 数据未发布" 被误报成未知 fetch 失败, 干扰真实 network/auth 故障辨识。

## What Changes

单一 Level 2 Spec, 三 task group (同属 state-scanner skill, 链式 TG-A→TG-B→TG-C)。

### TG-A — `coordination_fetch.py` 拆两条 fetch + benign 三重 AND 闸

核心: 把单条原子 fetch **拆成两条独立 `git fetch`**, 解耦分支头与协调 ref。

**1. Fetch 1 (分支头, 载重, 先执行)**: `git fetch <remote> --no-tags +refs/heads/*:refs/remotes/<remote>/*`。独立成功才刷新远端分支视图。失败 (network/auth/timeout) = 真故障 → 沿用 `_classify_error` + TASK-007 degraded 降级 (degraded=True 仅在此 fetch 真失败 + 有 stale cache)。

**2. Fetch ordering = 短路** (OQ R1/qa-M2 锁定): **Fetch 1 失败 → 不执行 Fetch 2** (远端不可达时无法判定 coordination 状态)。`coordination_ref_present = None` (unknown), success/degraded 由 Fetch 1 决定。可单测 (断言 Fetch 1 失败时 Fetch 2 的 `_run` 调用次数 = 0)。

**3. Fetch 2 (协调 ref, 仅 Fetch 1 成功后)**: `git fetch <remote> --no-tags refs/aria/coordination`。三路:
   - **benign 缺失** (三重 AND 硬闸, OQ4 锁定): `rc == 128 AND "couldn't find remote ref" in stderr_lower AND "refs/aria/coordination" in stderr_lower` —— 三条全真才 benign = "coordination 数据未发布" → `coordination_ref_present = False`, **不发 soft_error, 不设 degraded, 不算 kind=other**。**求值顺序** (R2 code-reviewer): 三重闸在 `_classify_error` **之前**拦截, 否则 rc=128 会先落 "other"。
   - **拉到**: rc == 0 → `coordination_ref_present = True`。
   - **非 benign 失败** (rc=124 timeout / rc=127 git_missing / network/auth, 或 rc=128 但未过三重闸; 罕见态: Fetch 1 已成功却 Fetch 2 故障) → `coordination_ref_present = None` + **`r.soft_error("coordination_ref_fetch_failed", ...)`** (真故障值得 surface; exit 10 正确)。**无需新 CollectorResult API** (OQ3 锁定: 复用 `soft_error`, 不引入 `note` 原语)。

**4. `coordination_ref_present` 三态 + cache 持久化** (OQ2 锁定): 新增 additive 字段 `coordination_ref_present: bool | None` —— `True`=Fetch 2 拉到 / `False`=benign 确认未发布 / `None`=未知 (Fetch 1 失败短路 或 Fetch 2 非 benign 失败)。**必须写入 cache payload** (`_write_cache` 加 key) 并在 cache-hit / degraded-stale-serve 路径**从 cache 读回**, 保证连续两 scan 该字段稳定 (防 normalize stability 漂移, 见 TG-C)。pure-failure 无 cache → `None`。

**5. success/degraded 重锚定**: `success` 反映 **Fetch 1** (载重); coordination ref 缺失**不**令 `success=False` 亦**不**触发 `degraded`。既有字段名/shape 不变。

**6. `refs_fetched` 取值规则** (backend-arch-minor①): 只含**实际成功**的 refspec —— Fetch 1 成功 → 含分支头 refspec; Fetch 2 拉到 → 追加 `refs/aria/coordination`; benign 缺失 / 失败 → **不**含 coordination refspec (消费者不会误判已拉到)。**注** (R2 code-reviewer): `refs_fetched` 已在 normalize DROP_KEYS, 其取值仅对实时消费者有意义, 不影响 canonical-form stability。

**7. 保留**: 30s TTL cache 主体 (`_read_cache`/`_write_cache` 扩 payload) + `_iso_now_utc`/`_parse_iso_utc` + Rule #7 `capture_output` 合规 (两 _run 调用沿用; benign/note 的 error_msg **不嵌 raw stderr**, 沿用 coerce 短串, code-reviewer-minor)。cache 写入条件 = Fetch 1 成功; `_write_cache` OSError **fail-soft** (沿用现有 L137-138 策略, 不新增, R2 qa)。

### TG-B — 测试 (新建 `tests/test_coordination_fetch.py`)

> **recon 实证**: coordination_fetch collector 当前**无专属单测** (仅 `test_p1_layer_h.py` 测 render 侧 degraded board)。本 Spec **新建** collector 直测文件。

Rule #6 substitute (deterministic collector, per [[feedback_deterministic_structural_skill_rule6_substitute]]) = structural fixture + unit tests + dogfood。测试矩阵 (mock `_run` 模拟双 fetch 返回码/stderr 组合, 参 `tests/_helpers.py` 风格; worktree 隔离 fixture per [[feedback_test_worktree_fixture_isolated_tmpdir]]):

- **(a) coord 缺失**: Fetch1 ok + Fetch2 三重闸命中 → `success=True` + `coordination_ref_present=False` + **无 soft_error** + `degraded=False` + exit-path clean。
- **(b) coord 存在**: 两 fetch ok → `coordination_ref_present=True` + refs_fetched 含 coordination。
- **(c) Fetch1 真失败 + stale cache** → `success=False` + `degraded=True` + 断言既有 `coordination_fetch_degraded` soft_error **保留** (TASK-007 不变, R2 code-reviewer) + 断言 `coordination_ref_present` 从 stale cache **读回**上次值 (非 None, R2 qa — 守 TG-A §4 stale-serve 读回逻辑真执行)。
- **(d) Fetch1 失败短路** (qa-M2): mock Fetch1 rc=128 no-stale-cache → 断言 **Fetch2 `_run` 调用次数 = 0** + `coordination_ref_present=None`。
- **(e) Fetch1 ok + Fetch2 非 benign 失败** (qa-M1): Fetch2 rc=128 但 stderr 不含 benign 关键词 (或 rc=124) → `success=True` + `coordination_ref_present=None` + **有 `coordination_ref_fetch_failed` soft_error** (进 errors[] / exit 10)。
- **(f) benign 负测试** (code-reviewer/qa): rc=128 + "couldn't find remote ref" 但 ref 名**不含** coordination → **不**归 benign (走 soft_error), 防三重闸被绕过。
- **(g) TTL 幂等 + 字段稳定** (qa-minor/M3): cache 新鲜 (last_fetch_at=now-5s) → 断言 `_run` **未被调用** + `coordination_ref_present` 从 cache 读回值**与上次一致** (连续两 run diff=0, 守 `test_two_consecutive_runs_diff_zero`)。
- **回归保护**: 既有 `test_p1_layer_h.py` render 侧 degraded 测试零回归 (degraded 触发条件收紧但 snapshot fixture 仍构造 degraded=True, 不依赖 collector 行为)。
- **dogfood**: 无-coord 项目 (或 sandbox) 跑 collector → `errors[]` 无 `coordination_fetch_failed` + exit 0; Aria 自身 (有 coord ref) 零回归 (`coordination_ref_present=True`, success 不变)。
- description 未改 → 无 /skill-creator AB。

### TG-C — schema + 文档同步 (Rule #3 docs-in-sync)

- **`state-snapshot-schema.md`** (SOT): **新建** `coordination_fetch` 完整 schema section (现**无**独立 section, km-M2/tech-lead 实证) —— 补全 fetch 全字段基线 (success/cached/last_fetch_at/age_seconds/refs_fetched/error_kind/error_msg/degraded/degradation_reason) + 新增 `coordination_ref_present` (additive, v1.46.0+) + **`success`/`degraded` 语义锚定到 Fetch 1 的变更注记** (非 shape 变, 属行为契约变化)。对齐 `handoff_worktrees` 等先例记录粒度。
- **`coordination_fetch.py` 模块 docstring**: 更新 return schema (加 `coordination_ref_present` 三态) + 双 fetch design notes + benign 三重闸 + ordering 短路语义。
- **`references/phase-1-collectors.md` line 41** (tech-lead-minor): 现写 `git fetch origin refs/heads/* refs/aria/coordination --no-tags` —— **双重 stale** (缺真实 `+...:refs/remotes/<remote>/*` 形式 + 现要拆两条)。**重写**为两条独立 fetch 描述。
- **`docs/coordination-ref-schema.md`** (km-minor): grep 确认存在 → 核查是否含 collector fetch 行为 / success / degraded 描述, 有则同步 (layer-l-integration.md 已核查无 coordination_fetch success/degraded 直接引用, 不在触点)。
- **`normalize_snapshot.py` DROP_KEYS 裁定** (code-reviewer-M1/qa-M3): `coordination_ref_present` 语义稳定 (cache 持久化保证 cache-hit 与 fetch-run 同值) → **不进 DROP_KEYS** (与 `cached`/`age_seconds`/`refs_fetched` ephemeral 字段相反)。TG-B (g) 加 stability 回归断言守护。
- **`snapshot_schema_version` 不 bump**: `coordination_ref_present` 是 nested optional additive (default-absent 兼容), 符合 §Versioning additive-only (先例 git-operation-awareness 同不 bump) → 保持 `"1.0"`。注: `success`/`degraded` 是语义变化非 shape 变化, 不触发 schema_version bump (schema_version 跟 shape; 行为契约变化由 plugin **MINOR** 版本承载)。

## Impact

- **Affected**: `collectors/coordination_fetch.py` (TG-A) + `tests/test_coordination_fetch.py` 新建 (TG-B) + `references/state-snapshot-schema.md` 新建 section / `references/phase-1-collectors.md` L41 / `docs/coordination-ref-schema.md` 核查 / `normalize_snapshot.py` DROP_KEYS 裁定 + 模块 docstring (TG-C)。
- **向后兼容** (Rev1 拆两维, km-minor):
  - **shape 兼容 ✅**: 既有字段名/shape 不变; `coordination_ref_present` 纯 additive default-absent。
  - **语义变化 ⚠ (受控修正)**: `success`/`degraded` 重锚定到 Fetch 1 —— 对无-coord 项目, `success` 从"每次 False"变"Fetch1 成功即 True", `coordination_fetch_failed` soft_error 消失, exit 10→0。这是**修复方向** (旧 `success=False` on benign-absent 即 bug 本身), 但属**可观测行为契约变化**, 故 **MINOR** 版本承载 + schema section 注记。消费 TASK-007 degraded 降级路径的代码 (render_track_board L509-515 仅读 degraded/cached/error_msg, 不读 success → 无回归; 已核) 受益于误报消除。
  - **有-coord 项目** (如 Aria 自身): 两 fetch 都成功, 行为完全不变。
- **Rule #6**: deterministic collector → structural fixture + unit tests (7 场景 a-g) + dogfood, 无 capability AB。
- **Versioning**: v1.45.0 → **v1.46.0** (MINOR)。**Rev1 裁定 (PATCH→MINOR, tech-lead-major)**: 直系先例 `git-operation-awareness` (同形: 修 collector 误报 + 加 1 additive nested 字段 + schema 不 bump + 可观测行为变化) shipped 为 **MINOR v1.39.0**。本 Spec 与之同形 (加 `coordination_ref_present` surface + degraded 状态机改写) → MINOR 保 parity, 避免版本语义漂移。CLAUDE.md "Bug 修复=PATCH" 与 "新功能/向后兼容=MINOR" 两条同适用时, 取 surface-扩展 + 行为契约变化 → MINOR (severity=major 描述 bug 影响面, 与版本轴正交, 不矛盾)。

## Out of scope

- #141 软错误② (handoff_multibranch cap) —— 已 v1.38.0 #71/#72 修, triage comment 已说明。
- **`lib/coordination_ref.py::fetch_coordination_ref` (L1065-1154) 的 benign 处理** (code-reviewer-M2): 该函数 (Layer L 协调数据**主动读写**库) L1141 else 分支同样把 "couldn't find remote ref" 归 `fetch_failed` 无 benign。但它是**distinct 路径** —— 仅当项目**主动使用多终端协调** (claim/reconcile) 时调用, 此时 coordination ref **应已 bootstrap 存在** (`init_coordination_ref`), "ref 缺失"良性场景罕见。collector (每次 scan, 所有项目) 是高影响主路径; 本 Spec 修 collector 即闭合 #141/#75。lib 函数 benign 统一记为 **known follow-up** (新 issue), 不在本 Spec (避免 scope 膨胀)。
- 把分支头刷新职责从 collector 迁出 / 与 sync collector 合并 (架构重构)。**注 (tech-lead-minor)**: 本 Spec TG-A 反而**固化** "coordination_fetch 兼任分支头载重" 耦合 (Fetch 1=载重), 解耦是 known follow-up。
- 发布/管理 `refs/aria/coordination` ref 本身 (Layer L) + coordination ref **内容损坏/解析失败** 处理 (正交)。

## Resolved (Rev1 — post_spec R1 收敛)

1. ~~版本粒度~~ → **MINOR v1.46.0** (先例 parity, tech-lead-major)。
2. ~~`coordination_ref_present` 必要性~~ → **显式三态字段** (refs_fetched benign 缺失态为空 `[]` 无法区分"未发布"vs"全失败", 复用丢语义)。
3. ~~Fetch 2 非 benign 失败处置~~ → **`soft_error` (无新 API)** + `coordination_ref_present=None`; Fetch ordering **短路** (Fetch1 失败不跑 Fetch2)。
4. ~~benign stderr 鲁棒性~~ → **TG-A 硬闸三重 AND** (`rc==128 AND "couldn't find remote ref" AND "refs/aria/coordination"`), 防误吞 timeout(rc=124)/真故障。

## 收口

- aria-plugin **#75** → PR merge 后 close。
- Aria **#141** → POST comment (软错误① fixed + ② v1.38.0 已修) 后 close; **PATCH state 单发, 不 PATCH body** (per [[feedback_issue_close_comment_not_body_patch]])。
- 修复落 aria submodule → 主仓 gitlink bump (per [[feedback_sequenced_multirepo_gitlink_bump]]: submodule PR 先 merge → gitlink re-bump → 主仓)。

# concurrent-track-proactive-coordination — 并发多 session 前置检测 + Layer L 主动引导

> **Level**: 2 (Minimal — proposal.md;改动集中在 phase-d-closer + state-scanner SKILL.md 的 process 步骤 + **一处小的 collector 增量**(把既有 renderer-local `_classify_collision` 提升为共享 helper 并持久化到 snapshot,见 Rev1 C1 修正)。非纯 prose-patch,但无新机制、无 API break)
> **Status**: REVISE (Phase A.2 **未收敛**, banked 2026-05-30 待下次 Rev2 + scope 重构) — R1 = NEEDS_FIX (3/3, 2 Critical) → Rev1 → R2 = **1 NEEDS_FIX + 2 PASS_WITH_WARNINGS (未收敛)**。R2 tech-lead + code-reviewer 独立发现 Rev1 又踩 created_at-class:(1) `_classify_collision` 真实输入是 `list[ClaimRecord]` 非 `tracks[]`,迁移含整条 `_track_to_claim_record → reconcile_all` 链(远超"抽函数");(2) **phase1_gate 读 `read_claims()` claim YAML refs,与 snapshot `tracks_multibranch` 是独立数据源 — "两路径共享 collision 字段"架构性错误**,disjointness 仅靠 `enabled` 互斥成立。**下次 Rev2 待办**(见末尾 §R2-CARRY)。审计报告:`.aria/audit-reports/post_spec-R1R2-2026-05-30-concurrent-track-proactive-coordination-consolidated.md`。
>
> **R2-CARRY (下次 Rev2 + scope 重构清单)**:
>   1. **scope 重构决策**(tech-lead N2):把 collision-field-persistence 拆为**独立 Spec**(collision 派生逻辑 + collector 持久化 + renderer 改读 + 回归矩阵),本 Spec 两切口依赖它;否则两切口被一个被低估的重构卡住。
>   2. 修 §What collision 迁移描述:输入 `list[ClaimRecord]`(非 tracks[]),迁移含 `_track_to_claim_record`(可 raise ValueError)+ `reconcile_all` 链;helper 签名应为新函数 `classify(tracks: list[dict])` 包 split+group+set 逻辑,非直接 promote `_classify_collision`。
>   3. 删 §What L48 + AC-4 的"phase1_gate 与切口2 共享字段"机制理由 — phase1_gate 源 = claim refs;collision 字段 consumer 限 renderer + 切口2;disjointness 仅靠 `enabled` 互斥。
>   4. 修 3 处 citation:default-branch 用 `symbolic-ref` 应 cite `sync.py:114`(非 :37-41 rev-parse);ahead/behind 复用 `rev-list --left-right` **pattern** 非调 `git.py` 函数(后者锁 `@{upstream}`);承认 collision helper 是新函数。
>   5. qa minor:AC-1 加 `upm.source_file == null` null-guard(无 UPM → 无强提示)+ `collision.kind!=none & behind>0 & 非 UPM-touch` 中间态 soft-advisory smoke;AC-0 加 renderer 读缺失 collision 字段的 backward-compat fallback(老 snapshot 无此字段)。
>   6. AC-4 注明 phase1_gate 行为 out-of-scope(由 multi-terminal-coordination Spec 管)。
> **Change ID**: `concurrent-track-proactive-coordination`
> **Source**: Forgejo Aria [#133](https://forgejo.10cg.pub/10CG/Aria/issues/133) — SilkNode 双 session 并发 ten-step cycle 致 UPM merge thrash + 矛盾记录;本 session (2026-05-30) dev-claude 自身 2 次撞 `.git/index.lock` 佐证
> **Target version**: aria-plugin v1.36.0+ (tentative — 与 shell-jq-crlf-hardening 并发在途;**Phase B step 0 必须** `cat aria/VERSION + plugin.json` 复核取下一可用 MINOR,不留到 ship 时,见 `feedback_submodule_regression_pitfall`)
> **Risk class**: 防御性 + 纯增量提示。不改既有 Layer L 默认 opt-out 语义(向后兼容);新增提示均 advisory 非阻塞。collector 新增 `collision` 字段为 additive(snapshot schema additive-only 演进)。无 API break。

> **Rev1 changelog (post_spec R1 闭合, 2026-05-30, R1 = NEEDS_FIX/NEEDS_FIX/REVISE, 3/3 抓同一 Critical)**:
>   - **C1 (3/3 unanimous) `tracks_multibranch.collision_type` 字段不存在 — created_at-class 缺陷**: collector (`handoff_multibranch.py`) 只产出 `exists/tracks/branches_scanned/legacy_count/errors`;collision 仅在 renderer-local `track_board.py::_classify_collision` 算 (名为 `collision_kind` 非 `_type`),从不写回 snapshot;`collision_type`/`has_collision` 只存在于**设计意图文档** `layer-l-integration.md:23,69` (从未实现,正是误导本 proposal 的源头)。**修**: (a) 把 `_classify_collision` 提升为**共享 helper**,由 `handoff_multibranch` collector 调用并**持久化** `tracks_multibranch.collision` 字段 (additive);(b) 切口2 + 既有 opt-in phase1_gate 路径**都读这一个字段** (单一真值源,解 I3 disjointness);(c) 同步修正 `layer-l-integration.md:23,69` 的 stale 字段名 → 防下个 Spec 继承假前提 (meta-fix)。承认这是**小 net-new collector 代码**,非纯 prose,Level 头已更新。
>   - **C2 (qa) `coordination.enabled` 是 config 键非 snapshot 字段**: 查找路径 = config-loader 加载的 `.aria/config.json` `state_scanner.coordination.enabled` (state-scanner 阶段 2 已持有 config)。**修**: 切口2 谓词明确为「读 config (config-loader) 的 `coordination.enabled == false`」+「snapshot `tracks_multibranch.collision.kind != none`」二者**与**,非纯 snapshot 谓词。AC-2 已重写。
>   - **I1 (cr+tl) 切口1 default-branch 解析未定**: **修**: 钉死 `git symbolic-ref refs/remotes/origin/HEAD` → fallback `origin/master` → `origin/main` (prior art `collectors/sync.py:36-41`);behind-count 可复用 `collectors/git.py:167` 既有 `(ahead, behind)` 计算手法。
>   - **I2 (cr+tl) "复用 coordination_fetch" 混淆 fetch 机制 vs 降级语义**: **修**: 切口1 在 cycle-end 发**自己的 fresh fetch** (独立于 1.16 的 30s 缓存 — 不同生命周期点,收尾时缓存已陈旧故需新 fetch),显式 `timeout=30`;**仅复用** `error_kind` enum + soft-warn 降级 pattern (非缓存结果);behind-check 是新逻辑。
>   - **I3 (tl+cr) 切口2 与 opt-in 路径 disjointness 未显式**: **修**: 切口2 advisory **iff `coordination.enabled == false`**;既有 `cross_owner → 强提示+phase1_gate` 路径 iff `enabled == true` — 两者在 `enabled` 上互斥,单一 collision 字段供两路径读,绝不双触发。
>   - **I4 (qa) 切口1 "UPM 文件"检测机制未定**: **修**: 机制 = `git log --name-only <oldlocal>..origin/<default-branch>` 的路径集合与 `snapshot.upm.source_file` (collector 已产出 UPM 路径) 求交;非空 → 升级强提示。
>   - **I5 (qa) 切口1 `behind>0` 假阳性 (常规 CI/human commit)**: **修**: 切口1 advisory 仅在 `behind>0` **且** (`tracks_multibranch.collision.kind != none` **或** behind commits 触及 UPM 文件) 时触发;纯 behind>0 无并发信号 → 静默 (防 prompt fatigue)。AC-3 已覆盖此场景。
>   - **I6 (qa) self-serial 同 owner+container 需排除**: **修**: collision 共享 helper 对同 owner+同 container 返回 `none` (沿用 `_classify_collision` 既有语义),切口2 据 `kind != none` 触发,自然排除 self-serial。
>   - **I7 (qa) AC-3 负向断言不可测**: **修**: AC-3 指定具体 fixture (tracks_multibranch.collision.kind==none + behind==0 → 断言 advisory 字符串**不出现**)。
>   - **Minor (tl/cr)**: 切口1 soft-warn 复用 `error_kind` enum 不回显 raw stderr (防 credential URL 泄漏);Target version 复核前移到 Phase B step 0。

---

## Why

#133 暴露:Aria 的 UPM single-source-of-truth + handoff 指针 + 共享 followup 表约定**隐式假设串行 session**。当并发多 session 在同一 repo 跑 ten-step cycle 时,两类失效:

1. **PR merge thrash**:两 session 都改同一 UPM 区域(followup 表同一 #NNN row)→ 一方 push 后另一方 PR 立即 `mergeable:false`,反复解冲突不收敛(SilkNode 实测 A 解 3 次仍 race)。
2. **矛盾记录(更严重)**:两 session 对同一 prod 状态写相反归属,共享 row 成对抗性编辑,污染 SoT。

**安全网已存在但未启用**:Layer L(multi-terminal-coordination,v1.22.x ship)有 claim / cross-owner collision / phase1_gate / track board,但 `state_scanner.coordination.enabled` **默认 opt-out**,受影响项目未启用 → 完全没拦住。`tracks_multibranch` collector(Phase 1.17)**已在采集**跨分支 track 数据(`scan.py` 无条件执行 1.16/1.17,opt-out 下数据仍可用),只是 opt-out 时不消费、不提示。

**根因不是缺机制,是机制不主动 engage + 收尾无前置并发检测。** 本 Spec 补两个最小高 ROI 切口(#133 建议 c + a-lite),不做 b(UPM convention 重构)/ d(worktree-per-session)。

---

## What

### 前置修正 (R1 C1) — 把 collision 分类提升为持久化 snapshot 字段

当前 collision 分类逻辑 `_classify_collision` 只存在于 `renderers/track_board.py` (renderer-local,render 时算,不入 snapshot)。本 Spec 先做一处**小 collector 增量**:

- 抽 `_classify_collision` 为**共享 helper**(例如 `lib/collision.py` 或 collector 内函数),输入 `tracks[]`,输出 `{kind: "none"|"cross_owner"|"self_multi_container", groups: [...]}`。
- `collectors/handoff_multibranch.py` 调用它,在 `tracks_multibranch` 下**持久化** additive 字段 `collision`(snapshot schema additive 演进,bump `state-snapshot-schema.md`)。
- `track_board.py` renderer 改为读这个共享字段(消除重复逻辑,单一真值源)。
- 语义沿用既有 `_classify_collision`:同 owner+同 container → `none`(排除 self-serial,R1 I6);≥2 distinct owner → `cross_owner`;同 owner ≥2 distinct container → `self_multi_container`。

> 这使切口2(opt-out advisory)与既有 phase1_gate(opt-in 强提示)**读同一个 `tracks_multibranch.collision.kind` 字段**,根除 R1 C1 的 phantom-field + R1 I3 的 disjointness divergence。

### 切口 1 (建议 c) — phase-d-closer 收尾前置并发检测

phase-d-closer 在 **D.1 (progress-update 写 UPM) 之前**,新增机械化前置 step:

- **default-branch 解析**(R1 I1):`git symbolic-ref refs/remotes/origin/HEAD` → fallback `origin/master` → `origin/main`(沿用 `collectors/sync.py:36-41` chain)。
- **fresh fetch**(R1 I2):发自己的 `git fetch origin <default-branch>`,显式 `timeout=30`,独立于 state-scanner 1.16 的 30s 缓存(收尾时点缓存已陈旧)。fetch 失败 → **仅复用** `coordination_fetch` 的 `error_kind` enum + soft-warn 降级 pattern(不回显 raw stderr,防 credential URL),不阻塞。
- **behind-check**:比较本地 vs `origin/<default-branch>`(复用 `collectors/git.py:167` 的 `(ahead, behind)` 手法)。
- **触发条件**(R1 I5,防假阳性):仅当 `behind > 0` **且**(`snapshot.tracks_multibranch.collision.kind != none` **或** behind commits 触及 UPM 文件)时提示。纯 behind>0 无并发信号 → 静默。
- **UPM 触及判定**(R1 I4):`git log --name-only <oldlocal>..origin/<default-branch>` 路径集合 ∩ `snapshot.upm.source_file` 非空 → 升级**强提示**("并发对手很可能在改同一 UPM 文件,先 fetch+rebase 再写")。

> **现状对比**:phase-d-closer 当前只有**反应式**冲突 retry(SKILL.md §并发冲突处理 ~line 136),无前置检测。本切口前移到写之前。

### 切口 2 (建议 a-lite) — state-scanner 检测到并发 track 时主动提示启用 coordination

state-scanner 阶段 2,新增 advisory 规则:**iff**

- `snapshot.tracks_multibranch.collision.kind != "none"`(用前置修正持久化的真字段),**且**
- config-loader 加载的 `.aria/config.json` `state_scanner.coordination.enabled == false`(R1 C2:config 读取,非 snapshot 字段)

时,**主动 surface 一条 advisory 提示**(非阻塞):"🔀 检测到并发 track(kind=…,owner/container:…)。本项目 Layer L coordination 当前 **opt-out**,并发安全闸门未启用。建议在 `.aria/config.json` 设 `state_scanner.coordination.enabled = true` 避免 UPM merge thrash + 矛盾记录(#133)。"+ 一键启用 config 片段。

> **disjointness**(R1 I3):本 advisory iff `enabled == false`;既有 `cross_owner → 强提示+phase1_gate` iff `enabled == true` — 在 `enabled` 上互斥,绝不双触发。

### 明确不做 (out of scope, 留独立 Spec)

- **(b)** UPM record convention concurrent-safe 重构 — 独立 Spec。
- **(d)** worktree-per-session 解 `.git/index.lock` — Layer L TASK-024/025 已设计,该线后续。
- 不改 Layer L 默认 opt-out;不改 claim/reconcile 既有逻辑。

---

## Impact

- **改动文件**:
  - `aria/skills/state-scanner/scripts/collectors/handoff_multibranch.py`(+ 新共享 collision helper)+ `renderers/track_board.py`(改读共享字段)+ `references/state-snapshot-schema.md`(additive `collision` 字段)— 前置修正
  - `aria/skills/state-scanner/SKILL.md` 阶段 2 + `RECOMMENDATION_RULES.md`(切口 2 advisory 规则)
  - `aria/skills/phase-d-closer/SKILL.md`(切口 1 前置 step)
  - `aria/skills/state-scanner/references/layer-l-integration.md:23,69`(meta-fix:修 stale `collision_type`/`has_collision` → 正确字段名)
- **复用(精确)**:`coordination_fetch` 的 **error_kind enum + soft-warn 降级 pattern**(非缓存结果);`collectors/sync.py` default-branch chain;`collectors/git.py` ahead/behind 计算;`_classify_collision` 既有分类语义;`tracks_multibranch.tracks[]` + `upm.source_file` 既有 collector 字段。
- **向后兼容**:✅ opt-out 默认不变;新增提示 advisory 非阻塞;`collision` 字段 additive;单 track/无并发场景无额外提示。
- **Rule #6**:含 collector 逻辑增量(collision 派生)+ process 步骤。Phase B 评估 AB benchmark vs Level 2 patch 豁免;collector helper 应配 unit test 跑 committed canonical(`feedback_validator_repo_drift_guard_test`)。

---

## Acceptance Criteria

- **AC-0 (前置修正)**:`tracks_multibranch.collision` additive 字段由 collector 持久化,值 `{kind, groups}`;`collision.kind` 语义沿用 `_classify_collision`(同 owner+container→none);collector helper 配 unit test 跑真实 `tracks[]` fixture(从 `collect_handoff_multibranch` 真实输出构造,非手搓 schema — `feedback_test_mock_pattern_hides_prod_bug`);`track_board` renderer 改读共享字段(回归 0)。
- **AC-1 (切口 1)**:phase-d-closer D.1 前有机械化 step:default-branch 解析(symbolic-ref chain)+ fresh fetch(timeout=30,失败 soft-warn 不阻塞 + 不回显 raw stderr)+ behind-check;**仅在** `behind>0 且 (collision.kind!=none 或 commits 触及 upm.source_file)` 时提示;触及 UPM → 强提示。smoke:构造 origin ahead + UPM-touching commit 验强提示;ahead 但非 UPM + collision none 验**静默**(R1 I5)。
- **AC-2 (切口 2)**:state-scanner 阶段 2 **iff** `tracks_multibranch.collision.kind != none` **且** config `coordination.enabled == false` 时产出 advisory(含启用引导)。fixture 从真实 collector 输出构造。
- **AC-3 (向后兼容 / 无噪音,R1 I7)**:具体可测 — snapshot `tracks_multibranch.collision.kind == none` + `git.upstream.behind == 0` + `coordination.enabled` 任意 → 断言两切口 advisory 字符串**均不出现**(负向 absence assertion)。
- **AC-4 (disjointness,R1 I3)**:`coordination.enabled == true` 时切口2 advisory **不触发**(由既有 opt-in phase1_gate 路径处理);`== false` 时 phase1_gate 不触发、切口2 advisory 触发。两态互斥可测。
- **AC-5 (meta-fix)**:`layer-l-integration.md` 不再引用不存在的 `collision_type`/`has_collision`,改为 `tracks_multibranch.collision.kind` 真实路径(防 created_at-class 复发)。

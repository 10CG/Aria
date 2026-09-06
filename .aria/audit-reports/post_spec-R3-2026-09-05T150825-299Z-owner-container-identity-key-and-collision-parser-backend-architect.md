---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: REVISE
timestamp: 2026-09-05T15:08:25.299Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## R2 处置核对

对照 `.aria/audit-reports/post_spec-R2-2026-09-05T143543-081Z-owner-container-identity-key-and-collision-parser-backend-architect.md` 的 3 条 finding，逐条在 v3 proposal.md 上核对：

- **Finding R2-1 (critical / D1 步骤 3 的「不可归属 owner」处置未挑明，冻结语料上真实误判为 cross_owner)** — **closed**。v3 D1 步骤 3 (proposal.md:34) 把 R2 时含糊的两种读法收窄为唯一措辞：「取**非空且非 `unknown`** 的 owner 串集合（空 owner = 不可归属，**不计为独立 owner**）」。在 `/tmp/claude-1000/-home-dev-Aria/660cdd00-d2ad-4227-a5bb-5312810322f1/scratchpad/r3_v3impl.py` 里按这句字面实现（`classify_claims` 内 `owners = {c.owner for c in active if c.owner not in ("", "unknown")}`），对冻结语料跑生产路径（`split_owner_container` 两段式 → dedupe 键 `(track_id, identity_key)` → `classify`），结果 `996→122, self_multi_container, groups=[["simonfish/dev-claude","simonfish/dev-claude2"], ["dev-claude","simonfishgit/dev-claude"]]`，与 proposal.md:58 实验表 v3 行**逐字一致**——R2-1 点名的 `aria-submodule-gate-block-flip`（`dev-claude` 零段 vs `simonfishgit/dev-claude`）这条真实数据现在正确落在 `self_multi_container`，不再是 R2 时的 `cross_owner` 误报。7 个合成用例（`/tmp/.../scratchpad/r3_synthetic.py`）逐条核验见下方「审计结论」正文，全部与 proposal.md:60 逐字对应。

- **Finding R2-2 (critical / `classify()`/`classify_claims()` 签名无法接收「全语料 owner 等价类」，D3 advisory 数据通路结构上不可达)** — **closed（因架构前提被撤销而消解，非「照原方案打了补丁」）**。v3 彻底放弃了 v2 的「owner 等价类」机制（proposal.md:4 明示撤销），`classify_claims` 改为纯局部判定——只看**同一 track_id** 内 dedupe 后的 active 行按 `identity_key` 计数 + 该 track 内的 owner 集合大小，不再需要跨 track_id、跨时间的等价类信息，因此 `classify()`/`classify_claims()` 签名"不变"这句话不再是自相矛盾的（R2 时 v2 的判定必须依赖只有 `classify()` 拿不到的全语料信息，v3 直接砍掉了对该信息的依赖）。D3 的 `identity_drift_advisories(tracks)` 是一个**独立函数**，不经过 `classify()`/`classify_claims()` 的调用链，实读两处调用点确认它能拿到所需的全量原始 `tracks`：(1) `handoff_multibranch.py:709`（`deduped_tracks, dedupe_stats = dedupe_latest_per_track_container(tracks)` 前一行的局部变量 `tracks` 就是本函数尚未消费的全量非-legacy+legacy 行，`identity_drift_advisories` 若插在这行之前调用，数据可达）；(2) `track_board.py:689` `tracks: list[dict] = tmb.get("tracks") or []`——这正是 collector 写回 `tracks_multibranch.tracks` 字段的同一份原始集合（实读 `handoff_multibranch.py:732` `"tracks": tracks,`，确认持久化的就是未 dedupe 的完整列表），渲染器读快照时拿到的是同一份数据，不是重新扫描。两处不需要给 `classify()` 加第二个参数，R2-2 指出的"结构上不可达"问题因为**判定逻辑本身不再需要那份数据**而消解。

- **Finding R2-3 (major / T3b 挂载点未写清 + `get_container_id()` 无条件 uuid 优先与运行时"拒绝 flip"语义矛盾)** — **partial**。v3 把挂载点从"未写明/可能进 `identity.py`"改为明确的"`phase1_gate` / `release_gate` 启动路径，不进 `identity.py`"（proposal.md:36），这解决了 R2-3 里"identity.py 新增下游依赖 + 每次身份解析多一趟 git 子进程"的性能/分层担忧——`identity.py` 本身零改动、零新依赖。但 R2-3 里第二个更根本的矛盾（"拒绝 flip"是运行时决策，`get_container_id()` 是无状态纯函数，两者如何共存）**没有被写清楚**，只是把它从"住在哪个函数里"的问题变成了"两个挂载点各自能不能真的拦住 flip 的后果"的问题——实读代码发现两个挂载点的可行性完全不对称，这是本轮的新 Major，见下方 Finding R3-1。

**R2 处置三态计数：closed 2 / partial 1 / open 0**（partial 项转化为下方 R3-1，不重复计数）。

## 审计结论

### 实验表与合成用例复现（无新增 finding，供其余席位复核用）

在 `/tmp/claude-1000/-home-dev-Aria/660cdd00-d2ad-4227-a5bb-5312810322f1/scratchpad/r3_v3impl.py` 按 v3 D1 步骤 1/2/3 + D3 字面实现 `split_owner_container` / `identity_key` / `dedupe_new`（键 `(track_id, identity_key)`）/ `classify_claims`（identity_key 计数 + 不可归属排除）/ `identity_drift_advisories`，对 `.aria/repro/handoff-tracks-frozen-2026-09-05.json`（996 行）跑生产路径：

| 变体 | dedupe | kind | groups | 与 proposal.md 对照 |
|---|---|---|---|---|
| A（现状代码未改动，复用 `r2_variantA.py`） | 996→121 | self_multi_container | `[dev-claude, simonfishgit/dev-claude]` | 与 line 56 逐字一致 |
| B（只改两段式解析，dedupe 键不变，复用 `r2_variantB.py`） | 996→122 | cross_owner | 上组 + `[simonfish/dev-claude, simonfish/dev-claude2]` | 与 line 57 逐字一致 |
| v3 D1 全套 | 996→122 | self_multi_container | 同 B 的两组 | 与 line 58 逐字一致 |

D3 advisory（`identity_drift_advisories(nonlegacy)`，dedupe 前全量）：`023236f2: [aria-runner-bot, simonfish]`（first_seen `2026-07-03T12:41:53Z`, last_seen `2026-09-05T06:17:57Z`）、`bfe8285d: [aria-runner-bot, simonfish]`（first_seen `2026-07-05`, last_seen `2026-09-05T09:40:00Z`）——与 proposal.md:62 逐字一致。

7 个合成用例（`r3_synthetic.py`，每组两行同 track_id 不同 `owner_container`）：
1. `alice/aaaa1111` + `bob/bbbb2222` → `cross_owner`（与 line 60 一致）
2. `simonfish/bfe8285d` + `aria-runner-bot/bfe8285d` → dedupe 1/2 → `none` + advisory 1 条 `{bfe8285d: [aria-runner-bot, simonfish]}`（一致）
3. `simonfish/bfe8285d` + `simonfish/023236f2` → `self_multi_container`（一致）
4. `aria-runner-bot/bfe8285d` + `simonfish/023236f2` → `cross_owner`（一致，漂移后无共现仍诚实判 🔴）
5. `aria-runner-bot/023236f2` + `simonfish/bfe8285d`（既有隔离夹具变体）→ `cross_owner`（一致；且实测该夹具对应的真实测试 `test_both_latest_active_different_owners_still_reports_cross_owner` 在 monkeypatch 后**未改动即通过**，见下方任务 6）
6. `dev-claude`（零段）+ `simonfishgit/dev-claude`（两段）→ `self_multi_container`（一致，这正是 R2-1 的真实数据组，现已修复）
7. `erin/eeeeeeee` + `frank/eeeeeeee` → dedupe 1/2 → `none` + advisory（一致）

全部 3 行实验表 + 7 个合成用例与 proposal.md 声称结果**逐字一致，零偏差**。

### Finding R3-1 (major / issue / architecture)
- **scope**: proposal.md D1 末段 (line 36) + T3b (line 103) + SC-3 (line 117)；`aria/skills/state-scanner/lib/identity.py:191-244`（`get_container_id`，逐调用无状态）；`aria/skills/state-scanner/scripts/phase1_gate.py:84,486,773-780`；`aria/skills/state-scanner/scripts/release_gate.py`（全文，无 `identity`/`read_claims` 引用）；`aria/skills/state-scanner/lib/claim_lifecycle.py:377-425`（`release_claim_by_track`）
- **summary**: v3 把 T3b 挂载点从"未写明"收窄为"`phase1_gate` / `release_gate` 启动路径，不进 `identity.py`"，这解决了 R2-3 的性能/分层担忧，但**两个挂载点对"拒绝 flip"这句话的可实现代价完全不对称，proposal 把它们并列写成同等重量的挂载点，掩盖了这个不对称**：
  - `phase1_gate.py` 已经在 `:486` 调用一次 `get_identity()` 得到 `resolved_identity`，并在 `:773-780` 把这个**同一个对象**显式传给 `acquire_claim(track_id, phase, resolved_identity, repo, ...)`（不是让 `acquire_claim` 内部重新调 `get_identity()`）。这意味着 T3b 的守卫**可以**在 `:486` 和 `:773` 之间插入——检测到 `label` 非空且 `claims/<label>/` 有 active 时，用 `dataclasses.replace(resolved_identity, container_id=label)` 覆写这一个局部对象——一次覆写，`acquire_claim` 全程用旧口径，语义自洽，且不碰 `identity.py`。
  - `release_gate.py` 完全不是这个形状：实读全文，它只 `import` 了 `lib.coordination_ref.fetch_coordination_ref`（`:43`）和 `lib.claim_lifecycle.release_claim_by_track`（`:42`），**从未 `import` `lib.identity`**，也从未自己解析过 `Identity`。它在 `:132` 调用 `release_claim_by_track(raw_track_id, status=status, repo_path=repo, now=ts)`——**不传 `identity=` 参数**。`release_claim_by_track` 内部（`claim_lifecycle.py:406` `resolved = _resolve_identity(identity, repo_path)`）在 `identity=None` 时会自己**新鲜调用** `get_identity()`，并用 `resolved.container_id`（T3 flip 落地后即 uuid）去匹配磁盘上 `rec.container == resolved.container_id`（`claim_lifecycle.py:421`）。若磁盘上的 active claim 是 flip 前用旧 label 写入的，这次匹配会落空 → `error="claim_not_found"`（`claim_lifecycle.py:426-427`）——这正是本 Spec 要修的 aria-plugin#135 08-13 那类孤儿 claim 的**同一失败模式**，只是触发点从"迁移期"换成了"release_gate 自己内部的 identity 解析路径"。
  - 要让 `release_gate.py` 具备与 `phase1_gate.py` 同等的"拒绝 flip"能力，需要新增：(1) `import` `lib.identity`（读 container-id 文件的 `label` 字段，目前该文件的 parser 是 `identity.py` 内部私有的 `_parse_container_file`，`release_gate.py` 若要自己判断"label 非空"还拿不到这个函数——它未被导出为公开 API）；(2) `import` `lib.coordination_ref.read_claims`（或等价方式）来检查 `claims/<label>/` 是否有 active；(3) 命中时构造一个覆写过 `container_id` 的 `Identity` 对象，显式传进 `release_claim_by_track(..., identity=override)`。这是三处新代码 + 一个当前不存在的公开接口缺口（`_parse_container_file` 需要提升为公开函数，或 T3b 自己重新实现一遍"读 label"逻辑），proposal 的 Tasks/SC 都没有点名。
- **evidence**:
  - `grep -n "identity\|coordination_ref\|read_claims" aria/skills/state-scanner/scripts/release_gate.py` 只命中 `fetch_coordination_ref`（`:43,56,120`）和注释里的 `identity_error` 字样（`:18`），零 `lib.identity` 引用。
  - `claim_lifecycle.py:406-421`：`_resolve_identity(identity, repo_path)` → `identity is None` 分支调 `get_identity()`；`matches = [rec for rec in read_result.claims if rec.container == resolved.container_id and rec.track_id == norm and rec.status == "active"]`——比对键就是 flip 后的新 `container_id`。
  - `phase1_gate.py:486` `resolved_identity = get_identity()` 与 `:773` `acq: AcquireResult = acquire_claim(track_id, phase, resolved_identity, repo, now=ts, linked_issue=linked_issue)`——同一对象跨两处使用，证实"就地覆写一次即可全程生效"在这个文件里成立。
  - `identity.py` 内 `_parse_container_file`（`:105-123`）是模块内无下划线前缀但未出现在 docstring "Public API" 列表（`:11-16`）里的函数，`release_gate.py` 若要自己读 `label` 字段，要么复制一份解析逻辑（新的重复实现风险），要么请求 `identity.py` 把它提升为公开 API——这两条路径 proposal 都没有选。
- **影响**: SC-3"S1/S2 共同: label 非空且 `claims/<label>/` 有 active 时 `phase1_gate` 输出迁移告警"这句话只点名了 `phase1_gate`（与 D1 正文"挂在 `phase1_gate` / `release_gate`"不完全对齐，SC-3 本身漏了 `release_gate` 分支的验收），且没有一条 SC 断言"`release_gate` 也能在同样条件下拒绝 flip"。若实现者只照 SC-3 字面走，`release_gate.py` 大概率不会获得这个守卫（因为验收标准没要求），T3b 的"迁移期在飞 claim 变孤儿"防护就只覆盖了 acquire 路径，release 路径依旧可能在迁移窗口内产生 `claim_not_found`——即 #135 缺口 3 本 Spec 要修的问题，在 release 路径上原样保留。这不是"实现时顺手决定"的细节，而是一个当前 SC 覆盖不到、需要显式补一条断言 + 补一句"如何读 label / 如何构造覆写 Identity"的实现指引的缺口。

## Verdict

REVISE — 0 Critical + 1 Major + 0 Minor（0C/1M/0m）。R2 处置：2 closed / 1 partial（转化为本轮 R3-1）/ 0 open。

## Vote

REVISE

## 轮次记录

**读了什么**: proposal.md v3 全文逐行（Why/What/D1-D4/实验表/合成用例/决策点 D-0~D-3/Impact/Tasks/SC/非目标/References）；R2 五份报告中本席报告全文；`lib/collision.py` 全文（`split_owner_container`/`track_to_claim_record`/`classify_claims`/`classify`/`linked_issue_overlaps`）；`scripts/collectors/handoff_multibranch.py` 全量 dedupe 模块注释块 + `dedupe_latest_per_track_container` 全函数 + `:680-732` 装配段（`tracks` 变量生命周期、legacy 行 append 点 `:675`、collision 计算 `:700-729`、`"tracks": tracks` 持久化点 `:732`）；`scripts/renderers/track_board.py` 的 import 块 (`:175-186`)、`:681-757`（`tmb.get("tracks")` 读取、`collision_input_tracks` 构造）；`lib/identity.py` 全文（含 `_parse_container_file`/`get_container_id`/`get_identity`，逐行确认无模块级状态、每次调用重新读文件）；`lib/claim_lifecycle.py` 的 import 块 + `_resolve_identity` + `release_claim_by_track` 全函数 (`:377-430`)；`scripts/phase1_gate.py` 的 import 块 (`:65-126`) + `:480-490`（`resolved_identity` 赋值）+ `:760-800`（`acquire_claim` 调用与失败回退段）；`scripts/release_gate.py` 全文（import 块、`run_release`、`:83-145` release 步骤段）——确认零 `identity` 引用。

**跑了什么**（均在 scratchpad 内脚本, 未改仓内文件；import 顺序沿用 R2 的 `sys.path.insert(0, ".../scripts"); sys.path.insert(0, ".../state-scanner")` 规避双 lib 包遮蔽）：
1. `/tmp/.../scratchpad/r3_v3impl.py`：按 v3 D1 三步 + D3 字面重新实现 `split_owner_container`/`identity_key`/`dedupe_new`/`classify_claims`/`classify`/`identity_drift_advisories`，对冻结语料跑生产路径 —— 复现实验表 v3 行（996→122, self_multi_container, 两组）与 D3 advisory 两条，均与 proposal 逐字一致；同时复用 `r2_variantA.py`/`r2_variantB.py` 复核 A/B 两行仍逐字一致（未受 v3 改动影响，作为对照基线）。
2. `/tmp/.../scratchpad/r3_synthetic.py`：构造 proposal.md:60 的全部 7 个合成用例，逐条跑 `dedupe_new` → `classify` → `identity_drift_advisories` —— 7/7 与 proposal 声称结果一致（含 dedupe 折叠 + advisory 产出的两个 "none + advisory" 用例）。
3. `/tmp/.../scratchpad/r3_monkeypatch_run.py`：在真实 `lib.collision`/`collectors.handoff_multibranch` 模块对象上 monkeypatch `split_owner_container`/`classify_claims`/`dedupe_latest_per_track_container` 为 v3 语义（保留 `_dedupe_sort_key` 等未改动的排序逻辑不变），在同一进程内用 `/home/dev/.local/share/uv/tools/pytest/bin/python` 跑 `test_collision.py` + `test_handoff_multibranch_collision_dedupe.py` + `test_reconcile_golden_table.py` + `test_race_window.py` + `test_phase1_gate_advisory.py`（116 项）—— 结果 114 passed / 2 failed，失败的**恰好且仅**是 proposal 点名要重写的两条（`test_split_owner_container_variants`、`test_both_latest_active_still_reports_self_multi_container`），其余 114 项（含"既有隔离夹具" `test_both_latest_active_different_owners_still_reports_cross_owner` 与 `test_owner_segment_participates_in_grouping_key`）零回归。
4. 单独跑 `phase-d-closer/tests/test_fetch_gate.py`（未 monkeypatch，因该测试硬编码 `collision_kind` 字符串字面量，不经过 `lib.collision` 实现）—— 11/11 passed，确认 D4 声称的"行为不变，纯 additive"成立。
5. `grep -n "identity\|coordination_ref\|read_claims" release_gate.py` + 实读 `claim_lifecycle.py::release_claim_by_track` 与 `phase1_gate.py` 的 `resolved_identity` 传递路径 —— 定位 Finding R3-1（`phase1_gate` 与 `release_gate` 两个挂载点对"拒绝 flip"可行性不对称）。

**未发现问题的项**: D3 advisory 的两处数据源一致性（collector `:709` 前的 `tracks` 与 renderer `:689` 的 `tmb.get("tracks")` 确认同源，均为 dedupe 前全量）；D-3(a) 新鲜度截止插入点（`classify()` 内 `records.append(rec)` 前，早于 `reconcile_all()` 调用，`:374-379` 的 stale-winner 回收逻辑结构上看不到被截止的行，proposal 断言成立）；SC-6"归因表由测试计算"对**当前冻结语料**成立（两组均为 `self_multi_container`，按 `classify_claims` 定义本身即"同人多机"，无需额外规则；"真撞车"这一归因桶在当前数据上不被触发，proposal 结论段已自陈"真实语料里没有真正的两人撞车"，不构成本轮可报告缺口）；`identity_drift_advisories` 的 `first_seen`/`last_seen` 取自 `updated_at`——track 字典上没有第二个时间戳字段，非"两种读法的歧义"，是唯一可选项，不构成可报告 finding。

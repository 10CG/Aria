---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-05T15:50:52.857Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## R3 处置核对

对照 `.aria/audit-reports/post_spec-R3-2026-09-05T150825-299Z-owner-container-identity-key-and-collision-parser-backend-architect.md` 的唯一 finding R3-1 (major / `release_gate.py` 侧 T3b 零 identity 耦合, `release_claim_by_track` 内部重解析会重演 #135 孤儿 claim, SC-3 只点名 `phase1_gate`)，在 v4 (`addc8a1`) 上核对：

**closed**。逐项核实：

1. **`identity=` 形参是否需要新增**——实读 `aria/skills/state-scanner/lib/claim_lifecycle.py:377-380,406,412`：`release_claim_by_track(raw_track_id, *, status=..., identity: Optional[Identity] = None, repo_path=None, now=None)`，`identity=None` 时内部 `_resolve_identity` 才会重新调 `get_identity()`。**这个形参今天已经存在**，v4 line 38/107-108/124 的「传 `identity=` 覆盖」是复用既有可选形参，不是新增接口——proposal 没有声称新增，字面读法与代码一致，无歧义。
2. **`release_gate.py` 今天零 identity 耦合，是否已在 v4 补上依赖清单**——`grep -n "identity" aria/skills/state-scanner/scripts/release_gate.py` 仍是零命中（R3 时的证据未变），v4 line 38/107-108 明确列出三个新依赖：`import lib.identity`、新函数 `get_container_label()`（T3 新增，S1 即落）、`lib.coordination_ref.read_claims`（**已存在**公开函数，`coordination_ref.py:596`，返回 `ReadClaimsResult(claims, errors, ref_exists)`，`ClaimRecord.container` 字段可按 label 过滤 active，见 `claim_schema.py:88-89,123`）。三者中两个是现成 API，一个是本 Spec 自己要新增的 accessor——无「当前不存在的公开接口缺口」，R3-1 原文点名的 `_parse_container_file` 未导出问题被 `get_container_label()` 这个新公开 accessor 直接消解（T3 本身就是新增它）。
3. **成本**——`read_claims()` 是一次 `git ls-tree -r` + 逐 blob `git show`，非按 `claims/<label>/` 目录裁剪范围，但这不是新增开销模式：`phase1_gate.py:512` (`Step 5: read_claims after fetch`) 与 `:1334` 已经在 acquire 路径上做同样的全量 `read_claims(repo)` 调用；`release_gate.py` 自身 Step 1 (`:120`) 已经 `fetch_coordination_ref`。在 release 路径上加一次同量级的 `read_claims` 调用是与既有 `phase1_gate` 对称的既定模式，非新增架构负担。
4. **SC-3 覆盖面**——v4 line 124：「S1/S2 共同: … `phase1_gate` **与** `release_gate` 各自输出迁移告警」+「仅 S2: … 复现 #135 08-13 时间线**不再** `claim_not_found`」——R3-1 指出的「SC-3 漏了 release_gate 分支验收」缺口已补上一条可测试的、点名 `release_gate` 的断言，不再是只点名 `phase1_gate` 的半句话。

R3-1 关心的架构性问题（两个挂载点对「拒绝 flip」可行性不对称、`release_gate.py` 缺依赖清单、SC-3 漏验收）在 v4 上逐条有对应文本，且引用的 API（`identity=` 形参、`read_claims`）实读均已存在，`get_container_label()` 是本 Spec 自建项——构造该新函数与本 Spec 范围一致，不构成新增未决接口缺口。**具体的「先尝试默认解析、命中 `claim_not_found` 且 label 非空再用覆写 identity 重试」这一层控制流细节 proposal 未逐字写出**，但这是在既有 building blocks（`identity=` 形参 + `get_container_label()` + `read_claims`）之上的常规实现选择，SC-3 用可执行断言（「不再 `claim_not_found`」）钉住了结果而非过程，符合 Level 2 粒度——不构成本轮可报告的 Major。

**R3 处置三态计数：closed 1 / partial 0 / open 0**（本席 R3 仅此一条 finding）。

## 审计结论

### 无新增 Major

对镜头 1（T3b/release_gate）、3（T13 插入点）、4（SC-6 注入）、5（SC-8 keys 测试）逐项实读，除下方一条 Minor 外未发现新的 Critical/Major。

- **镜头 3 (T13 `layer_h_is_fresh` 插入点)**：v4 line 89 明确「Layer H 记录构造阶段」= `collision.py:340-353` 与 `track_board.py:778-787` 两处结构相同的循环（`for t in collidable/all_collidable: rec = track_to_claim_record(t); records.append(rec)`），两处逐行核对确认结构一致（同一 `try/except ValueError: continue` 形状），在 `records.append(rec)` 之前插入 `if not layer_h_is_fresh(t, now, days): continue`（或等价 mark-stale 分支）在两处都可行、可对称写入，不需要额外重构。SC-11「collector 与 renderer 对同一 fixture 得同一 `kind`/`groups`」在这个插入点下成立——两处循环体本就同源同构。**无新增 finding**。
- **镜头 4 (SC-6 注入合成真撞车组)**：v4 line 127 的机械归因判据（「组内全部行 `updated_at` 早于 `LAYER_H_ACTIVE_WINDOW_DAYS` → `stale`；否则按 `kind` 分真撞车/同人多机」）本身**不依赖**任何「这行是不是注入的」标记就能得出正确归因——只要注入行的 `updated_at` 落在窗口内（測试构造时天然会给近期时间戳，不需要特殊语义），归因表就会把它正确落进「真撞车」桶。T6「显式标注」是测试代码可读性层面的要求（让人一眼看出这几行是构造的，不是冒充语料），不是归因算法的输入契约，proposal 未展开标注格式不构成实现阻塞。**无新增 finding**。
- **镜头 5 (SC-8 恒存在 + 两条 keys 测试)**：独立实读 `aria/skills/state-scanner/tests/test_collision.py` 全部 9 处 `keys()`/全等断言 (`:57,62,89,98,107,130,142,274,290`)。区分两类：(a) 直接调 `collision.classify(...)` 的 6 处 (`:57,62,89,98,107,142` 全等断言 + `:130` `test_classify_emoji_never_persisted` 的 `set(out.keys())==`) —— D3 明示「`classify()`/`classify_claims()` 签名不变」，`identity_advisories` 只在**收集器**装配 `data["collision"]` 时并入（`handoff_multibranch.py`），不进 `classify()` 返回值本身，故这 7 处对 `classify()` 直调的断言不受影响，`test_classify_emoji_never_persisted` 确实是 code-reviewer R4 指出的「不受影响的第三处」，本席独立复核结论一致；(b) 测真实收集器输出 `result.data["collision"]` 的 2 处——`:274` `test_real_collector_emits_cross_owner_collision` (`set(coll.keys())=={"kind","groups"}`) 与 `:290` `test_real_collector_no_collision_is_none` (`coll == {"kind":"none","groups":[]}` 全等)——这两处会在 `identity_advisories` 并入 `data["collision"]` 后失败，**恰好**是 proposal T2 点名要改写的两条。另核对 `test_handoff_multibranch_collision_dedupe.py`（全文 grep `coll ==`/`coll.keys` 零命中，该文件所有 `data["collision"]` 访问都是取具体键如 `["groups"]`，对新增字段容忍）——无第三个隐藏断点。**无新增 finding**。

### Finding R4-1 (minor / renderer / label 精度)
- **scope**: `aria/skills/state-scanner/scripts/renderers/track_board.py:783-787`（`tracks_by_tid` 构造）+ `:409-416`（`_render_collision_lines` 内 `oc_by_key` 查表）；对照 `aria/skills/state-scanner/lib/collision.py:347-354`（`oc_by_tid_key` 构造）
- **summary**: D-0(a) 族键剥离约定只作用于 `track_to_claim_record` 返回的 `ClaimRecord.track_id`。`lib/collision.py::classify()` 内的 `oc_by_tid_key` 是用 `rec.track_id`（剥离后）做外层键（`:353` `oc_by_tid_key.setdefault(rec.track_id, {})[key] = ...`），与 `reconcile_all` 按剥离后 `track_id` 分组、`for tid in sorted(verdicts.keys())` 用剥离后 tid 查表**完全同源、一致**——这条与 proposal 断言相符，无问题。但 `track_board.py:783-787` 的 `tracks_by_tid` 是在同一函数里**独立**构造的第二份索引：`for t in all_collidable: tid = t.get("track_id") or ""; tracks_by_tid.setdefault(tid, []).append(t)`——这里的 `tid` 是**未剥离的原始** `track_id` 字段值，不是经过 `_track_to_claim_record(t).track_id` 剥离后的值。而 `_render_collision_lines(verdicts, tracks_by_track_id)`（`:334`）里 `for tid in sorted(verdicts.keys())`（`:365`）拿到的 `tid` 是**剥离后**的 track_id（因为 `verdicts` 来自对 `claim_records`——即 `_track_to_claim_record` 的输出——跑 `reconcile_all`）。一旦某个真实 8-hex 尾段（非本 Spec「已知限制」里的日期形误剥场景，而是未来真出现的、剥离后确实改变了 track_id 字符串的情形）参与了一次实际渲染的 collision，`:409` `tracks_by_track_id.get(tid)`（用剥离后 tid 查未剥离键构造的字典）会 miss，`oc_by_key` 落空，`:415` `_label()` 退化为 `f"{claim.owner}/{claim.container}/{claim.session}"` 重建串，而不是 proposal 承诺的「用原始 owner_container 串作标签（更可读）」。
- **evidence**:
  - `track_board.py:780-787`：`claim_records.append(_track_to_claim_record(t))` 与 `tracks_by_tid.setdefault(t.get("track_id") or "", []).append(t)` 是两条并列、互不同步的构造语句，前者调用共享函数（会应用未来的剥离逻辑），后者直接读字段（不会）。
  - `track_board.py:365` `for tid in sorted(verdicts.keys())` + `:409` `tracks_by_track_id.get(tid)`——键域不一致时静默返回 `None`/`[]`（`or []` 兜底），不抛异常，不改变 `kind`/collision 判定，只改变展示字符串。
  - 对照组 `collision.py:353` 的 `oc_by_tid_key` 用的是同一个 `rec`（`_track_to_claim_record` 的返回值）的 `.track_id`，两次构造用的是**同一份剥离后字符串**，不存在这个不对称。
  - 冻结语料实测零影响：`aria-plugin-113-gate-result-yaml-20260719`（唯一命中 D-0(a) 剥离形状的 track_id）15 行 `owner_container` 全部是 `aria-runner-bot/023236f2`（单一 `identity_key`），`classify_claims` 恒返回 `none`，该 track 永远不会进入 `verdicts` 里带 `yielders` 的分支，`_render_collision_lines` 对它不产出行——本发现在当前语料上是**结构性存在但零触发**，不影响本 Spec 的实验表/SC-6 归因表结果。
- **影响**: 纯展示层退化（标签文本变丑但不算错——`owner/container/session` 本身也是合法可读格式），不改变 `collision.kind`/`groups` 的判定值，不影响任何一条现有 SC 的可测断言。proposal line 35 的「Layer H 两条路径 `collision.py:347` / `track_board.py:783` 同源」这句话对**共享的 `track_to_claim_record` 函数本身**成立，但没有覆盖到 `track_board.py` 里那份独立的、非共享的 `tracks_by_tid` 标签索引——这是本轮唯一在实读代码后发现的、v3/R3 五席均未点名的新缝隙。B 期顺手修法：把 `track_board.py:785` 的 `tid = t.get("track_id") or ""` 改成 `tid = _track_to_claim_record(t).track_id`（复用同一次转换结果而非重新计算，或干脆用 `claim_records` 里已构造好的 `rec.track_id` 建索引），与 `collision.py` 的 `oc_by_tid_key` 手法对齐即可，两行改动，不需要新增测试断言之外的设计。

## Verdict

PASS_WITH_WARNINGS — 0 Critical + 0 Major + 1 Minor（0C/0M/1m）。R3-1 已 closed。

## Vote

PASS

## 轮次记录

**读了什么**: proposal.md v4 全文相关段落（Why/D1 全段含 T3b 两态描述/实验表/D-0(a)/D-3(a)/T13/T6/SC-3/SC-6/SC-8/SC-11/Tasks 全清单/代码落点行号索引）；R3 五席原始报告本席一份全文 + R3 聚合报告全文（判定表 + Major 簇表 M1-M9 + Minor 表）；`aria/skills/state-scanner/scripts/release_gate.py` 全文（import 块 / `run_release` 全函数 / `_main`）；`lib/claim_lifecycle.py` 的 `_resolve_identity` 与 `release_claim_by_track` 签名段 (`:377-425`)；`lib/coordination_ref.py` 的 `read_claims` 全函数 (`:596-660` 起) 与 `ReadClaimsResult` 定义 (`:119-138`)；`lib/claim_schema.py` 的 `ClaimRecord.container` 字段与路径注释 (`:70-123`)；`lib/identity.py` 全文（`get_container_id`/`_parse_container_file`/`Identity` dataclass，确认 `get_container_label()` 今天不存在，是 T3 新增项）；`lib/collision.py` 的 `track_to_claim_record` (`:86-140`) 与 `classify()` 内 `oc_by_tid_key` 构造段 (`:330-379`)；`scripts/renderers/track_board.py` 的 import 块 (`:140-186`)、`:334-420`（`_render_collision_lines` 全函数）、`:760-800`（reconcile 路径装配段, `claim_records`/`tracks_by_tid` 构造）；`aria/skills/state-scanner/tests/test_collision.py` 全文的全部 `keys()`/全等断言位置 (9 处)；`tests/test_handoff_multibranch_collision_dedupe.py` 全部 `data["collision"]` 访问点 (grep 全量核对无隐藏全等/keys 断言)；`scripts/phase1_gate.py` 的 `read_claims` 调用点 (`:510-520,1330-1336`) 确认既有开销先例。

**跑了什么**（scratchpad 内, 未改仓内文件）: 用 `python3 -c` 对 `.aria/repro/handoff-tracks-frozen-2026-09-05.json` 做正则 `-[0-9a-f]{8}$` 命中统计（15 行, 唯一 track_id `aria-plugin-113-gate-result-yaml-20260719`）与该 track_id 全部 15 行的 `owner_container`/`status`/`updated_at` dump，确认全部 `owner_container` 相同（单一 identity_key），验证 Finding R4-1 在当前冻结语料上零触发。

**未发现问题的项**: T3b 依赖清单完整性（`identity=` 既有形参 / `get_container_label()` 本 Spec 新建 / `read_claims()` 既有公开函数, 三者拼接不缺公开接口）；`read_claims` 全量扫描开销与 `phase1_gate.py` 既有调用模式对称, 非新增架构负担；T13 插入点在两处结构相同循环里对称可行；SC-6 注入行归因不依赖显式标记, 只依赖 `updated_at` 落入正常窗口即天然正确；SC-8 两条待改写测试与一条不受影响测试的边界经独立 grep + 逐处代码核实, 与 code-reviewer R4 结论一致。

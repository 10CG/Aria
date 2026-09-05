---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: REVISE
timestamp: 2026-09-05T22:05:00.000Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/detailed-tasks.yaml
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R1 — backend-architect 席位报告

被审对象: `openspec/changes/owner-container-identity-key-and-collision-parser/{tasks.md, detailed-tasks.yaml}` (commit `60808b2`, 41 TASK) 对照 `proposal.md` (v7, Approved)。镜头: 组 2 (TASK-012..020) 与组 6 (TASK-027..030) 的落点可实现性 + TASK-019/TASK-035 深挖 + TASK-006 fixture + 工时。

实读环境: aria 子模块 checkout 于 `7dd0135` (v1.69.1, `git submodule status` 无 `+` 前缀, 与 metadata.scope_repos 声明一致); 主仓 `60808b2`。全部行号锚点对当前 checkout 逐条 `grep -n` / `sed -n` 核实。

## 审计结论

### Finding 1 — Major

- type: gap
- category: 发布同步面遗漏
- scope: TASK-035 (5.2, 版本 5 文件 bump + 主仓同步面)
- summary: TASK-035 的 deliverables 未列主仓根目录 3 份 i18n README (`README.zh.md` / `README.ja.md` / `README.ko.md`), 但其 verification 明确要求 `i18n-readme-translation-currency` 全绿。
- evidence: 实读 `.aria/state-checks.yaml:141-168` (`i18n-readme-translation-currency` 定义), 该 check 用 `python3` 比对 `README.zh.md` / `README.ja.md` / `README.ko.md` 顶部 `<!-- translated-from: vX.Y.Z -->` 与 `aria/.claude-plugin/plugin.json` 版本。实跑该比对脚本 (当前 checkout): 三份均为 `translated-from: v1.69.1`, 与 `aria/.claude-plugin/plugin.json` 当前版本 `1.69.1` 一致 (故 check 现今为 OK)。TASK-035 deliverables 只列 `CLAUDE.md` / `VERSION` / `README.md` (主仓) + aria 子模块 5 文件 + 两处架构文档, **没有**这三份 i18n README。Spec 落地后 `plugin.json` 会 bump 到 `<vNEXT>` (D5 判据 PATCH, 可能 MINOR), 若不更新这三处 `translated-from` 标记, 该 check 会从 OK 转为 DRIFT/STALE, 与 TASK-035 verification 自称的"全绿"直接矛盾, 也不满足 CLAUDE.md §版本管理"发布同步面"里明列的"i18n README (仅正文实质变更才重译)"一项 (本 Spec 属"仅正文实质变更才重译"的版本串刷新档, 至少三处标记需同步, 不需要重译正文)。
- 附带次要观察 (未单独计分): aria 子模块自身也有 `aria/README.zh.md`, 不受此 check 覆盖、也不在 CLAUDE.md "5 文件" 清单内, 是否需同步刷新版本串未被任何机械 check 兜底, 留作观察项。

### Finding 2 — Major

- type: gap
- category: 跨仓协调门控缺失
- scope: 组 6 (TASK-027 / TASK-028 / TASK-029 / TASK-030) 的 S2 执行前置
- summary: tasks.md 组 6 前言明文"条件: a1-entry B.2 已落地 **且** #174 ack", 但 41 项任务里只有 TASK-029 (6.3, 改写对方 SC-3) 的 verification 显式核对"对方 ack 留言 id 记录"; 决定是否执行 flip 的 TASK-027 (6.1) 与判定 `ship_shape` 的 TASK-000 (0.1) 均不含 ack 判据, 存在"a1-entry 分支已落地 (S2 判定成立) 但 #174 尚未 ack 即执行 flip"的可达路径。
- evidence: 实读 tasks.md "## 6. S2 形态专属" 一行原文: `条件: a1-entry B.2 已落地 且 #174 ack`。detailed-tasks.yaml `TASK-000.verification`: `"metadata.ship_shape ∈ {S1, S2} 且附实读证据 (a1-entry 分支名 / HEAD / lib/identity.py 是否含 get_container_uuid)"` — 判据只含分支/代码实况, 不含 #174 ack 状态。`TASK-027.dependencies: [TASK-000, TASK-00A, TASK-018]`; TASK-00A (0.2) 的 verification 只要求"留言含...请求 ack", 即**发出**请求即满足依赖, 不等待、不核对对方**回复**。`TASK-027.verification` 本身也不含 ack 判据, 只判 uuid 语义。对比 `TASK-029.verification`: `"对方 ack 留言 id 记录; 判据改为..."` —— 唯一显式核对 ack 的任务, 且它改的是 a1-entry 自己的文本, 不是本 Spec 生产代码的 flip 点。结果: 产生实际行为影响面最大的 `get_container_id()` flip (TASK-027, 影响本仓与后续所有消费方) 可以在 TASK-000 判定 ship_shape=S2 后立即执行, 无需等待 #174 ack, 与 proposal §决策点/tasks.md 组 6 前言的"且"条件(AND, 两个必要条件都要满足)不符。这正是本 Spec 试图根治的"未协调即变更身份语义"同类风险 (#135 缺口 3 的教训)。
- 建议: 给 TASK-027 (或新增一个组 6 前置任务) 补一条机械/记录型 verification, 要求先核验 #174 ack 留言存在 (同 TASK-029 的判据), 或把 ack 核验提到 TASK-000/6.0 层级统一把关, 而不是只挂在 TASK-029 一处。

### Finding 3 — Minor

- type: inaccuracy
- category: 行号锚点漂移
- scope: TASK-016 (2.5) verification
- summary: verification 引用 "grep 调用点仅 `collision.py:347` / `track_board.py:783`" 用于核实 `track_to_claim_record` 只有两个非测试调用点。实读该调用在 `lib/collision.py` 实际位于第 349 行 (`rec = track_to_claim_record(t)`), 与引用的 347 相差 2 行; `track_board.py:783` (`claim_records.append(_track_to_claim_record(t))`) 核实准确。
- evidence: `grep -n "track_to_claim_record(" aria/skills/state-scanner/lib/collision.py aria/skills/state-scanner/scripts/renderers/track_board.py` 输出仅两处非文档命中: `lib/collision.py:349` 与 `scripts/renderers/track_board.py:783`。`proposal.md` 本文在 D1 段落同样写 "`collision.py:347`", 说明这 2 行漂移是从 proposal 继承、非 task-planner 新引入; 且该引用只用于"确认恰好 2 处调用"的 grep 计数式核验 (非逐行编辑锚点), 实际实现影响低。建议在 B.1/B.2 落笔前用 `grep -n` 重新核对一次, 顺手勘正 proposal 与 tasks 的该行号。

### Finding 4 — Minor

- type: gap
- category: 任务锚点粒度不一致
- scope: TASK-020 (2.9) deliverables
- summary: TASK-020 (track_board ⚪ 行渲染 + label 并列显示) 的 deliverable 只写文件路径 `aria/skills/state-scanner/scripts/renderers/track_board.py`, 未给行号/插入点, 与同组其余任务 (TASK-014 `:709-716`、TASK-015 `:412-417`、TASK-016 `:778-793`) 的精确度不一致。
- evidence: detailed-tasks.yaml TASK-020 deliverables 字段确认无行号后缀。proposal.md §D3 已指出对称的渲染器插入点在 "`track_board.py:743-747` 已持有原始 tracks...在 dedupe 前同样调用"——与 TASK-017 的依赖锚点 (`track_board.py :743-747 前`) 同一区域, 可直接复用为 TASK-020 的锚点, 但 yaml 未标注。
- 已核实排除的假设 (回应审计任务书第 2 点提出的猜测): TASK-020 的 ⚪ 行渲染基于 `identity_drift_advisories(tracks)` 输出, 按 `identity_key` (非 `track_id`) 聚合 (对照 TASK-009 verification: "fixture 渲染恰 2 条 ⚪ (`023236f2` / `bfe8285d`)", 两者都是 uuid identity_key, 不是 track_id); 而 TASK-016 归一的 `tracks_by_tid` 字典是按剥离后 `track_id` 索引、供 `_render_collision_lines` 的 collision 行标签用, 与 ⚪ 行渲染是两条独立数据路径。因此 TASK-020 现有 dependencies `[TASK-014, TASK-009]` 已足够, **不**存在对 TASK-016 的隐藏依赖。

### Finding 5 — Minor

- type: estimation-risk
- category: 工时
- scope: TASK-017 (2.6, LAYER_H_ACTIVE_WINDOW_DAYS + layer_h_is_fresh)
- summary: 复杂度标 M / 4h, 但 deliverables 跨 4 个文件 (`lib/constants.py` + `lib/collision.py` + `scripts/collectors/handoff_multibranch.py` + `scripts/renderers/track_board.py`), 且约束是"collector/renderer 两处独立调用点必须得出同一结论"+"新鲜度截止不得作用于 D3 advisory 路径"+"不得让 TASK-006 冻结语料退回非 0 组"三条不变式同时成立, 复杂度对比同档的 TASK-013/TASK-014 (各自集中在 1-2 个文件) 明显更跨面。
- evidence: 逐条读 TASK-017 deliverables 与 verification 原文 (yaml TASK-017); 对照 TASK-013 (`lib/collision.py` 一处) / TASK-014 (`lib/collision.py` + `handoff_multibranch.py` 两处) 复杂度标注同为 M/4h, TASK-017 多一个文件且多两条互斥不变式。
- 建议: 复核工时或在 B.2 执行时把"collector 调用点"与"renderer 调用点 + board stale 标注"拆成两个可独立验证的子步骤记录, 便于工时超支时及时预警, 不必阻塞开工。

### Finding 6 — Minor

- type: traceability-gap
- category: fixture 裁剪留痕
- scope: TASK-006 (1.6) deliverables
- summary: `tests/fixtures/handoff-tracks-frozen-2026-09-05.json` (新建) 声明"八字段裁剪自 `.aria/repro/handoff-tracks-frozen-2026-09-05.json`", 但 yaml 只列裁剪后的产物文件, 未落"裁剪脚本/命令"这一中间产物或记录要求, 若日后需要复核裁剪是否忠实于 996 行源语料, 缺一个可复跑的转换留痕。
- evidence: 读 detailed-tasks.yaml TASK-006 deliverables 只有两个"(新建)"文件, verification 未要求记录裁剪命令。`test_collision_frozen_corpus.py` 同时承载 SC-6 (TASK-006, 冻结语料前后对照 + 机械归因) 与 SC-11 (TASK-010, 新鲜度谓词), 两者都基于同一份冻结语料且主题同属"时间维度", 合并到一个测试文件属合理组织, **不算缺陷**。
- 建议: verification 里补一句"裁剪命令/脚本随 handoff 记录 (哪怕是一次性 inline python)", 不必新增仓内常驻脚本文件。

## 逐项复核通过 (未发现问题, 供收敛记录)

- TASK-012 anchor `lib/collision.py:63-84` (`split_owner_container`) — 实读 `grep -n "^def split_owner_container"` = 63, 下一函数 `track_to_claim_record` 起于 86, 区间准确。
- TASK-013 anchor `lib/collision.py:143-168` (`classify_claims`) — 实读该函数 def 起于 143, 至 `return "none", ""` 后空行, 下一函数 `normalize_linked_issue` 起于 178, 区间准确。
- TASK-014 anchor `handoff_multibranch.py:709-716` — 实读 `deduped_tracks, dedupe_stats = dedupe_latest_per_track_container(tracks)` 恰在第 709 行。
- TASK-015 anchor `handoff_multibranch.py:518-523` — 实读 dedupe 分组键构造 `key = (t.get("track_id"), owner, container)` 在第 522 行, 落在区间内; `track_board.py:412-417` — 实读 `oc_by_key[(o, c, s)] = oc` 在第 413 行, 落在区间内。该处"键同源"bug 已核实成立: `oc_by_key` 由 `_render_collision_lines` (334 行起) 内部对原始 track 独立调用 `_split_owner_container` 重算, 与调用方 `render_track_board` (583 行起) 已经由 `_track_to_claim_record(t)` (783 行) 生成的 `ClaimRecord.owner/container/session` (含 `"unknown"` 兜底替换) 是两条独立计算路径, 空/零段串会在两侧产生不同 key ⇒ 查表必失配, 与 proposal §D1 描述的 bug 一致。
- TASK-016 anchor `lib/collision.py:86-140` (`track_to_claim_record`) 与 `track_board.py:778-793` (`tracks_by_tid` 构造) — 实读函数体起止与 `tracks_by_tid.setdefault(tid, []).append(t)` (793 行) 均落在声明区间内。"Layer L claim 不经该函数"核实为真: 全仓 `grep -rn "track_to_claim_record("` 命中仅 `lib/collision.py:349`、`scripts/renderers/track_board.py:783` 两个非测试非文档调用点, `lib/claim_lifecycle.py` / `lib/coordination_ref.py` 均无引用。
- TASK-017 dependencies `[TASK-014, TASK-010, TASK-006]` — 与审计任务书提示的判断一致, 未发现遗漏。
- TASK-018 anchor `lib/identity.py:126-140` — 实读 `_write_container_file` 的模板注释块 (含"Edit the `label` line to add..."一句) 落在区间内。
- TASK-019 三个 deliverables (`phase1_gate.py`, `release_gate.py`, `lib/claim_lifecycle.py`) 逐条核实:
  - `phase1_gate.py:486` = `resolved_identity = get_identity()`, 与"它在 :486 已解析 Identity"一致。
  - `release_gate.py` 实读: 全文件 `grep -n "identity\|Identity\|get_container_label\|read_claims"` 仅命中一处文档字符串 (行 18), **零**实际 import/调用 —— 与 proposal "release_gate.py 今天零 identity 耦合"完全吻合, 确认这是真实新增工作量而非误判。
  - `lib/claim_lifecycle.py::release_claim_by_track` 签名实读: `identity: Optional[Identity] = None` **已存在** (第 377 行起函数签名第 3 参数), 复核 R4 backend-architect 的"既有"结论成立, TASK-019 无需改这个签名本身, 只需在 `release_gate.py` 侧新增调用方传参。
- TASK-027 anchor `lib/identity.py:222` (`get_container_id()` flip 点) — 实读该行原文 `return label if label else uuid`, 与 a1-entry `proposal.md:571` 引用的"`:222` label 优先"完全一致, 两个 Spec 对同一行号的引用互相印证。
- TASK-029 anchor `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:571` — 实读第 571 行确为 SC-3 表格行原文 (`container-short` 前 8 位 ⇒ label 碰撞), 锚点准确。
- TASK-033 "主仓 14 条 state-check" — 实数 `.aria/state-checks.yaml` 恰好 14 个 `- name:` 条目, 计数准确。

## Verdict

REVISE — 0 Critical / 2 Major / 4 Minor。两条 Major 均为可在 B 期落地前修复的计划缺口 (非架构级推倒重来): (1) 版本同步面清单补齐 3 份 i18n README; (2) 组 6 flip 前补 #174 ack 的机械判据。其余锚点/工时/留痕类问题均为 Minor, 不阻断开工。

## Vote

REVISE

## 轮次记录

- Round 1 (本轮, backend-architect 单席): 逐条实读组 2 (TASK-012..020) 与组 6 (TASK-027..030) 全部 deliverable 路径/行号 (aria @ `7dd0135`, 主仓 @ `60808b2`), 深挖 TASK-019 (`release_gate.py` 零 identity 耦合确认为真、`identity=` 形参既有确认为真)、TASK-035 (版本同步面缺口)、TASK-006 (fixture 留痕)、工时 (TASK-017 偏紧); 发现 2 Major (i18n README 同步面缺口 / S2 ack 机械门控缺失) + 4 Minor (行号漂移 2 行 / TASK-020 缺锚点但依赖本身够用 / TASK-017 工时风险 / TASK-006 裁剪留痕)。投票 REVISE, 等待其他席位与后续轮次汇总。

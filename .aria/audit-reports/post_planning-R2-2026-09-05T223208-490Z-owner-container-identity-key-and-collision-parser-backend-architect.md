---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-09-05T22:32:08.490Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/detailed-tasks.yaml
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R2 — backend-architect 席位报告

被审对象: `openspec/changes/owner-container-identity-key-and-collision-parser/{tasks.md, detailed-tasks.yaml}` v2 (commit `03c6a9e`, post_planning R1 rework 后, 38 TASK + 4 S2 保留项) 对照 `proposal.md` v8。镜头: 发布同步面终检 (TASK-041) / tag 流程与语义 (TASK-035→034→036) / TASK-019 release_gate 深挖 / TASK-017 插入点可实现性 / 组 2 依赖完整性。

实读环境: aria 子模块 checkout `7dd0135` (v1.69.1, `git submodule status` 无 `+` 前缀); 主仓工作树当前 HEAD, `git status` clean。全部行号/命令实读, 无引用未跑证据。

## R1 处置核对

| R1 发现 | v2 处置 | 三态 |
|---|---|---|
| Major 1 — TASK-035 漏 i18n README ×3, 与 `i18n-readme-translation-currency` 判据矛盾 | R1 聚合裁决 M1: 新增 TASK-041 (5.7 主仓同步面), 明列 `README.zh.md`/`README.ja.md`/`README.ko.md` 三份 deliverables, 与 TASK-035 (5.2, 仅 aria 子模块 5 文件) 职责拆分 | **resolved** (本轮镜头 1 逐条核验) |
| Major 2 — 组 6 flip (TASK-027) 可在 S2 判定成立、#174 未 ack 时执行 | R1 聚合裁决 C1: 组 6 整体移出 tasks.md checkbox, 改 `metadata.s2_followup`; 激活规则显式要求「TASK-000 判 S2-candidate **且** #174 ack 已到 (TASK-040) **且** TASK-034 未执行」三条 AND, 三者不满足则 TASK-027..030 根本不作为可执行任务存在 | **resolved**, 且强于我 R1 的建议 (原建议只给 TASK-027 补 ack 判据; 实际处置是结构性移除, 不存在"判定成立但未 ack 仍可执行"的可达路径) |
| Minor 3 — TASK-016 行锚 `:347`→ 应 `:349` | v2 TASK-016 verification 已改为 "调用点仅 `collision.py:349` / `track_board.py:783`" | **resolved** (`grep -n "track_to_claim_record("` 复核仍为 349) |
| Minor 4 — TASK-020 deliverables 缺行号插入点 | v2 TASK-020 deliverables 补 "插入点 `:459-475` (kind 分支旁) + dedupe 前调用 `:744`" | **resolved**, 锚点实读准确 |
| Minor 5 — TASK-017 工时 4h 偏紧 | v2 est_hours 改为 6 | **resolved** |
| Minor 6 — TASK-006 fixture 裁剪留痕缺 deliverable | v2 TASK-006 deliverables 新增 `aria/skills/state-scanner/tests/fixtures/freeze_corpus.py` (裁剪脚本) | **resolved** |

三态计数: **resolved 6 / partially 0 / not_resolved 0**（Major 2 项 + Minor 4 项，全部核验为真实落地，非仅文字承诺）。

## 审计结论

### 镜头 1 — TASK-041 发布同步面 vs 5 条版本类 state-check 判据逐条对齐

实读 `.aria/state-checks.yaml` 五条 check 的 `command:` 脚本原文 (非仅 description):

| check | 实际读取的文件 (脚本原文核实) | 是否在 TASK-041 (或 TASK-035) deliverables 内 |
|---|---|---|
| `m6-version-badge-match` | `README.md` (badge) vs `aria/.claude-plugin/plugin.json` | 是 — TASK-041 列 `README.md # badge` |
| `i18n-readme-translation-currency` | `README.zh.md` / `README.ja.md` / `README.ko.md` 顶部 `translated-from` 标记 vs `plugin.json` | 是 — TASK-041 三份均列 (R1 Major 1 缺口点) |
| `plugin-version-arch-docs-match` | `docs/architecture/system-architecture.md` §2.8 aria-plugin 行 / `docs/architecture/version-scheme.md` aria-plugin 行 vs `plugin.json` | 是 — TASK-041 两份架构文档均列 |
| `m6-claude-md-version` | `CLAUDE.md` 顶部 `> **版本**: X` (核对字面量 `2.0.0`, 是 **Aria 方法论版本**, 与 aria-plugin 版本无关) | **不需要** — 本 Spec 不改该字段 (TASK-041 CLAUDE.md 一项明写"项目状态段其余不动"), 该 check 判据与本次 bump 无耦合, 现状本就绿 (实读 `CLAUDE.md:5` = `2.0.0`) |
| `main-project-version-consistency` | `VERSION` 头部 + `CLAUDE.md`「主项目 v…」+ 4×README「Project Version:」+ 两处架构文档「Aria main repo」行 (脚本 `POINTS` 清单实读, 9 点) —— 检的是**主项目版本** (今 `1.7.5`), 不是 aria-plugin 版本 | **不需要** — 本 Spec 只 bump `aria/.claude-plugin/plugin.json` (TASK-035), 不动 root `VERSION`/主项目版本号; 实跑 `python3 .aria/probes/main-project-version-consistency.py` 现为 `OK 主项目版本 1.7.5 — 9 个引用点全部一致`, 与本 Spec 无耦合面 |

结论: 5 条 check 中, 3 条 (`m6-version-badge-match` / `i18n-readme-translation-currency` / `plugin-version-arch-docs-match`) 判据面精确覆盖于 TASK-041 (`README.md` / 3×i18n README / 2×架构文档) 的 10 项 deliverables 内, 逐条无遗漏; 另 2 条 (`m6-claude-md-version` / `main-project-version-consistency`) 判据面是**主项目/方法论版本**而非 aria-plugin 版本, 本 Spec 未触碰该值 (只动 `plugin.json` 一侧), 正确地**不**需要出现在 TASK-041 deliverables 里 —— 若强行把它们塞进 TASK-041 反而是范围蔓延。TASK-033 verification 逐字列出这 5 个 check 名并要求全绿, 与本次核验的覆盖面精确对应, 无缺口。

### 镜头 2 — 发布顺序 (035→034→036) 与 tag 语义 (annotated vs lightweight)

实读版本管理规范 `standards/conventions/version-management.md` §4.3「按需锚点型」(aria 属此类): 更新顺序为 "1. 更新 VERSION (SOT) → 2. 提交+双推 (含 tag) → 3. 逐 remote 独立核验 tag 对象 SHA"。yaml 依赖边 `TASK-034(deps=[TASK-035,TASK-037])` / `TASK-036(deps=[TASK-034])` 与该顺序一致 (bump 先于本地 merge+tag, merge+tag 先于双推核验)。

Tag 类型实读: `git -C aria cat-file -t v1.69.1` = `tag` (**annotated**, 非 lightweight); `git -C aria rev-parse v1.69.1` = `1098ab1e15eb...` (tag 对象 SHA) 而 `git -C aria rev-parse v1.69.1^{commit}` = `7dd0135ae7d1...` (底层 commit, 与 yaml `scope_repos.head` 一致)。

对于 annotated tag, `git ls-remote <remote> refs/tags/vX.Y.Z` (不带 `--tags`/`^{}`) 只返回**一行**——tag 对象 SHA, 与本地 `git rev-parse vX.Y.Z` (同样返回 tag 对象 SHA) 语义一致; 只有显式请求 `refs/tags/vX.Y.Z^{}` 或加 `--tags` 才会额外拿到 peeled 的底层 commit SHA。TASK-036 verification 原文用词是「ls-remote refs/tags/v<NEXT> **对象** SHA == 本地」—— 用词是"对象 SHA"而非"commit SHA", 与 annotated tag 下 `ls-remote`/`rev-parse` 两侧都返回 tag 对象这一实况精确匹配, **不存在语义歧义**; 仓内既有 tag (`v1.68.0`..`v1.69.1`) 抽样核验均为 annotated (`cat-file -t` = `tag`), 与 §4.3 示例 `git tag -a` 一致。此前审计任务书提出的"annotated 与 lightweight 下语义是否一致"疑虑, 经实读确认: 措辞已经是按 annotated tag 精确写的, 无需改动。

### 镜头 3 — TASK-019 `release_gate.py` 的 `identity=` 形参与 `read_claims` 成本

`lib/claim_lifecycle.py:377-384` 实读 `release_claim_by_track(raw_track_id, status="done", identity: Optional[Identity] = None, repo_path=None, *, now=None)` —— `identity=` 形参确认既有 (R1 结论复核成立, TASK-019 无需改函数签名)。

`read_claims()` (`lib/coordination_ref.py:596`) 内部实现: `git ls-tree -r --full-tree refs/aria/coordination` 一次, 随后对 `claims/` 下**每个 blob** 各跑一次 `git show refs/aria/coordination:<path>` —— 是 O(N) 次独立 git 子进程 (N = 当前 ref 树里的 claim blob 数)。实读该函数被 `release_claim_by_track` 内部调用 (`claim_lifecycle.py` 约 417 行附近 `read_result = read_claims(repo_path)`), 是 TASK-019 新增的 `release_gate.py` 调用链的必经开销。

但这**不是新引入的性能面**: 实读 `phase1_gate.py:512` (`rc_result: ReadClaimsResult = read_claims(repo)`, Step 5 "fetch 后确保看到最新远端状态") 已在**每次 phase1_gate 启动** (即 B.0 REQUIRE-claim, 每 session 一次) 调用同一函数、同一开销形态; 实测当前 `refs/aria/coordination` 树 `git ls-tree -r` 共 48 项、`claims/` 下 11 项 —— 与 release_gate (每 cycle 收尾一次, 频率 ≤ phase1_gate) 相比, 数据量级与调用频率均不构成新增瓶颈, 是既有已接受的成本模式复用, 非需要在本 Spec 里额外优化的缺口。

### 镜头 4 — TASK-017 插入点 (`:709` 前 / `:744` 前) 与「被截止行不进 reconcile」可实现性

实读 `handoff_multibranch.py:709` = `deduped_tracks, dedupe_stats = dedupe_latest_per_track_container(tracks)`; `track_board.py:744` = `_dedupe_tracks_for_collision(tracks)[0]` —— 两个锚点分别精确落在"去重函数调用"那一行, 与 verification 描述的插入语义 (在这两处**之前**过滤新鲜度) 完全匹配。

`collision.py:370-390` 落在 `classify(tracks, ...)` (行 300 起) 内部, 是 `reconcile()` winner/superseded "捞回" 逻辑 (`active_claims` 从 `verdict.superseded` 里回收非终态候选) 所在处; 该逻辑只处理**传入 `classify()` 的 `tracks`**。若 `layer_h_is_fresh()` 过滤在 `:709` 前 / `:744` 前 (即 `dedupe_latest_per_track_container` / `_dedupe_tracks_for_collision` 调用之前, 也就是 `classify()` 调用链更上游) 就把过期行从 `tracks` 中剔除, 则这些行**根本不会进入** `classify()` 的输入, 结构上不可能被 `:379-383` 的"捞回"逻辑重新捡回 —— 与 verification 断言"被截止行不进 reconcile"逻辑自洽, 两个插入点位置选择正确, 不存在"过滤晚了、捞回逻辑仍能看到"的漏洞。

### 镜头 5 — 组 2 依赖完整性 (每实现任务至少一个组 1 RED 前置) + TASK-016→TASK-015 顺序

逐条核对 TASK-012..020 (组 2) 的 `dependencies`:

| 任务 | deps | 组 1 RED 前置 |
|---|---|---|
| TASK-012 | [001] | 直接 ✓ |
| TASK-013 | [012, 002] | 直接 ✓ (002) |
| TASK-014 | [013, 004, 005] | 直接 ✓ (004/005) |
| TASK-015 | [013, 003] | 直接 ✓ (003) |
| TASK-016 | [013, 015, 007] | 直接 ✓ (007) |
| TASK-017 | [014, 010, 006] | 直接 ✓ (010/006) |
| TASK-018 | [008] | 直接 ✓ (008) |
| TASK-019 | [018] | **间接** (经 018→008; 018 本身即 008 的实现) |
| TASK-020 | [014, 016, 009] | 直接 ✓ (009) |

八项直接命中, TASK-019 是唯一一项只经传递闭包命中组 1 前置 (verification 文本里显式写 "TASK-008 告警子句转绿", 但 `dependencies` 字段未列 008) —— DAG 拓扑序上不影响正确性 (018 已经先于 019 且 018 依赖 008, 008 必然先于 019 完成), 只是**若有自动化脚本只读 `dependencies` 字段做"组 2 是否有 RED 前置"覆盖率统计, 会把 TASK-019 误判为缺口**。这是可在 B 期顺手补一条 `dependencies: [TASK-018, TASK-008]` (冗余但显式) 的记录型 minor, 不影响执行正确性, 不计入 Critical/Major。

`TASK-016` 依赖 `TASK-015` 核实为**必要且方向正确**: TASK-015 的"键同源"是把 `track_board.py:412-417` 独立调用 `_split_owner_container` 重算 `oc_by_key` 的路径, 改为与 `_track_to_claim_record` (`:783` 处已用) 同源计算, 消灭两条独立路径; TASK-016 随后才修改 `track_to_claim_record` 本体做族键剥离。若顺序反转 (先剥离族键、再同源), 在剥离已发生但同源尚未发生的中间态, 两条独立路径会分别看到"剥离后"与"未同源"的不一致键, 重新制造 TASK-015 本要根治的同一类 bug; 现有顺序 (015 先同源、016 再改同源后的唯一入口) 保证族键语义变化天然经由统一路径传播到两处消费点, 是唯一自洽的顺序。

## 逐项复核通过 (未发现问题, 追加记录)

- TASK-041 10 项 deliverables 与 CLAUDE.md §版本管理"发布同步面"原句逐条比对: 两 gitlink (aria + standards, 后者为本 Spec 新增耦合面, 非 CLAUDE.md 原句字面但属合理超集) / VERSION / README badge / i18n×3 / 架构文档×2 / CLAUDE.md 版本行, 覆盖原句全部同步点, 无遗漏。
- TASK-033 (deps=[TASK-041]) → TASK-039 (deps=[041, 033]) → TASK-038 (deps=[039]) 顺序与 tasks.md 组 5 前言 "→ 5.7 → 4.3 → 5.6 PR → 5.5 回帖" 逐字一致。
- `metadata.s2_followup.activation` 三条件 AND (S2-candidate ∧ #174 ack ∧ TASK-034 未执行) 实读原文确认, 与 R1 aggregated PP1-C1 处置记录一致, 无回退。

## Verdict

PASS — 0 Critical / 0 Major / 0 计分 Minor (仅 1 条 B 期顺手记录型建议, 不影响 verdict)。R1 backend-architect 席全部 2 Major + 4 Minor 均已在 v2 落地为真实结构性修改 (非仅承诺), 本轮五个深挖镜头 (发布同步面判据对齐 / tag 语义 / release_gate 成本 / TASK-017 插入点结构自洽 / 组 2 依赖完整性) 均实读代码/脚本/配置逐条核验, 未发现新 Critical/Major。

## Vote

PASS

## B 期顺手项 (不阻断开工)

- TASK-019 `dependencies` 字段建议补 `TASK-008` (当前只经 TASK-018 传递可达; 直接列出可防未来"仅读 dependencies 字段"的自动化覆盖率脚本误判为缺口)。

## 轮次记录

- Round 1 (backend-architect 单席, `60808b2`): 发现 2 Major (i18n README 同步面缺口 / S2 ack 机械门控缺失) + 4 Minor (行号漂移 / TASK-020 锚点缺失 / TASK-017 工时 / TASK-006 裁剪留痕)。五席聚合 FAIL (2 Critical, 非本席贡献), rework → v2。
- Round 2 (本轮, backend-architect 单席, `03c6a9e`): 逐条核对 R1 处置三态, 全部 resolved; 新增五个深挖镜头 (发布同步面判据逐条对齐 / tag annotated 语义 / release_gate read_claims 成本 / TASK-017 插入点结构自洽 / 组 2 依赖完整性 + TASK-016→015 顺序合理性), 全部实读通过, 未发现新 Critical/Major, 仅 1 条 B 期顺手记录型 minor。投票 PASS。

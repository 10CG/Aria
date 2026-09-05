---
checkpoint: post_planning
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-05T22:57:24.913Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/detailed-tasks.yaml
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R3 — tech-lead 席 (稳定性核查: v3 是否只剩 B 期顺手项)

审计对象: `tasks.md` (组 0-5, 39 checkbox + 「S2 后续」表) + `detailed-tasks.yaml` (39 TASK) @ commit `c27826e`, 依据 `proposal.md` v9。

机械底账 (脚本实跑 `/tmp/claude-1000/-home-dev-Aria/660cdd00-d2ad-4227-a5bb-5312810322f1/scratchpad/dag3.py`, 未触碰仓内文件):
39 任务 / id 唯一 / 依赖全部可解析 / 无环 (topo len = 39) / 总工时 83.0h / parent 唯一无重 / `tasks.md` checkbox 实测 39 == `metadata.total_tasks: 39` / checkbox 编号集合与 yaml `parent` 集合**完全相等** (双向零差) / agent 实计 `backend-architect 15 · qa-engineer 15 · knowledge-manager 9` 与 `metadata.agents` 一致 (v3 已把 knowledge-manager 8→9) / 预留 id `TASK-027..030` 零占用 / 三文件正则扫描零带圈数字零希腊字母。

组 4-5 拓扑实跑序: `4.1 → 4.2 → 5.2 → 5.4 → 5.1 → 5.3 → 5.7 → 4.3 → 5.6 → 5.5 → 5.8`, 与 `tasks.md:81` 宣称的顺序逐段一致 (该行未列 5.4 / 5.8, 见 B 期顺手项)。

---

## R2 处置核对

| R2 finding | v3 三态 | 依据 (实读 / 实跑) |
|---|---|---|
| **M-1** S1 兜底「D 期 Step 7 tracker」不是既有机制 | **closed** (计划面) | 新增 `TASK-042` / `tasks.md:90` (5.8), 是**真 checkbox**。承载链实证: `spec_complete.py:186` `_CHECKBOX_RE` + `:257-290` 只扫 `tasks.md`, 归档要求全部 39 个 `[x]` ⇒ 5.8 未做即 `complete=False`, 归档被挡。这不再依赖 `_build_d_payload` 是否产出。时点「merge 后、归档前」在 DAG 上有承载: `TASK-042 dependencies: [TASK-039, TASK-000, TASK-040]`, 闭包实算 37 项 (只缺按设计并行的 `TASK-038`), 即拓扑上必在 5.6 merge 之后; 「归档前」由归档门本身兜住。**但** `proposal.md:104` 仍写「D 期以 tracker issue 记录 S2 后续 (先例 #192)」, 未改为「5.8 手动开 + #192 是 deferred 非空时的自动路径」⇒ 并入本轮 M-1 |
| **M-2** 组 0 不在 merge 传递闭包内 | **closed** | `detailed-tasks.yaml:544` `TASK-034 dependencies: [TASK-035, TASK-037, TASK-000, TASK-040]`; 闭包实算 `TASK-000 in closure(TASK-034) = True` / `TASK-040 in closure(TASK-034) = True`, 闭包规模 30→32。`ship_shape: "TBD-at-0.1"` 不再可能随 merge 落进 master |
| **M-3** proposal SC-9 仍要求 rule 1.54 代码级测试 | **closed** | `proposal.md:132` 行下的 SC-9 已改为「rule 1.54 为散文规则 (全仓 py 零命中, 无求值引擎) ⇒ 其触发面由**文档断言**承载: `RECOMMENDATION_RULES.md:31` 与 `references/rules/advanced-rules.md:544-572` 的 rule 1.54 行含 token `cross_owner` 与 `identity_advisories`」, 与 `tasks.md:52` (1.11) / yaml `TASK-011` notes / `TASK-024` verification 同文 |
| **M-4** 5.5 回帖在 S1 下超报 | **closed** (计划面) | `tasks.md:87` 与 yaml `TASK-038` verification 均已分档: S1 = 「缺口 3 部分闭合 (解析/身份键/dedupe/advisory), label 陷阱待 S2 或 tracker」; S2 = 「缺口 3 闭合」; 缺口 1/2 均留。**但** `proposal.md:120` T11 仍无条件写「ship 后关 #193, #135 留缺口 1/2」⇒ 并入本轮 M-1 |
| **m-1** TASK-018 对注释该写什么零断言 | **open** | `git diff HEAD~1 HEAD` 对 `TASK-018` 零改动; 实读 verification 仍只有「TASK-008 label accessor 子句转绿; S1 lock-in 仍绿」两条。R1 → R2 → R3 三轮未落 ⇒ 本轮 m-1 |
| **m-2** proposal T10 仍写「主仓 14 state-check」 | **open** | `proposal.md:119` 实读原文仍为「… + 主仓 **14** state-check → SC-7」⇒ 并入本轮 M-1 |
| **m-3** proposal:104 引文被插入句切断 | **closed** | v9 已改为「… SC-3 的 S2 臂不进本 cycle 验收。S2 激活时对方 SC-3 改写为「`get_container_uuid()` 与 flip 后 `get_container_id()` 同值; label 只在 `get_container_label()`」; 未取得 ack 不动对方文本」, 主谓复位; 同一文本也回填进 `tasks.md:100` S2-3 行与 yaml `TASK-029` verification |
| **m-4** TASK-033 未记录「例外是本轮 AI 引入」 | **open** | `TASK-033` verification 实读仍为「… 且 handoff 记录 owner D 期动作 (/plugin marketplace update + /plugin update + 重启)」, 无 Rule #10 复议留痕子句 ⇒ 本轮 m-2 |

三态计数: **closed 5 · open 3 · partial 0**。

R2 聚合报告 `…-aggregated.md` 的「Minor (8 条, **全部纳入 v3**)」一句与实况不符: 本席四条 minor 里 m-1 / m-2 / m-4 三条在 v3 零改动 (`git diff` 逐条核对)。

---

## 本轮镜头逐条答复

**镜头 1 — TASK-042 是否真闭合 M-1, 两分支勾选语义是否再撞归档门**

真闭合, 且两个分支都不会再撞归档门:

- **S1 分支**: 5.8 是普通 checkbox, 内容 = 手动开 tracker issue 并把编号回填「S2 后续」表。它进归档门的必勾集合, 所以「静默丢失」被换成了「不做就归不了档」——这是 R2 M-1 要的那种硬承载。
- **S2 分支**: 追加的 6.1-6.4 不会造成「归档前做不完」的僵局, 因为激活规则 (`tasks.md:103` / yaml:41) 把它们**接入 `TASK-034` (merge) 前置**, 而 merge (`TASK-034`) → PR/merge (`TASK-039`) → 归档 是单向链 (闭包实算 `TASK-039` 闭包 36 项含 034)。6.x 做不完 ⇒ 卡在 merge, 根本走不到归档门。所以**不需要**再写一条「追加即承诺同 cycle 完成, 否则不激活」——那条承诺已由「6.x 是 merge 前置」这条边机械保证, 再写文字反而是重复约束。

唯一残留是反方向的: 激活是**单向**的, 没有回退条款 (见本轮 m-4)。

**镜头 2 — 组 0 入 merge 前置后的传递闭包重算**

`TASK-039` (5.6, PR/merge) 闭包 = 36 项, 闭包外的任务恰为 `TASK-038` (5.5 回帖) 与 `TASK-042` (5.8 tracker) 两个 —— 与预期完全一致, 两者都是设计上的 merge 后动作 (deps 都含 `TASK-039`)。零反向依赖叶子实算 = `TASK-038` / `TASK-042`, 同样只有这两个外向项, 主 DAG 无死支。`TASK-034` (5.1) 闭包 32 项, 闭包外 6 项 = `TASK-033` / `036` / `038` / `039` / `041` / `042`, 全部是设计上排在 merge 之后的项, 无缺口。

**镜头 3 — v3 文本与 proposal v9 一致性**

| 项 | 判定 | 依据 |
|---|---|---|
| 双跑法 | 计划面一致, **proposal 面不一致** | `metadata.test_runner` / `tasks.md:78` (4.2) / `TASK-032` verification 三处都写「两种跑法都必跑」+ 双计数门槛 (≥1476 / ≥1492); `proposal.md:132` SC-7 仍只写 `tests/run_tests.py` ⇒ 本轮 M-1 |
| TASK-020 独立数据路径 | **一致且对真代码成立** | 实读 `track_board.py:743-747` = `collision_input_tracks = _dedupe_tracks_for_collision(tracks)[0]`, 确认 `:744` 是 dedupe 点且顶层 `render_track_board` (`:583` def) 持有原始 `tracks`; `:796` = `collision_lines = _render_collision_lines(verdicts, tracks_by_tid)`, 确认是 collision 段末; `:459-475` 实读为 per-track 循环内的 `collision_kind` 分支 (`elif collision_kind == "none": … pass`), 确认「只有 dedupe 后数据」。与 `proposal.md:47` (D3)「渲染器 `track_board.py:743-747` 已持有原始 `tracks`, 在 dedupe 前同样调用」同向。deps 去掉 `TASK-016` 也自洽 (新路径不经 `tracks_by_tid`) |
| CLAUDE.md :139 | **一致且行号对** | 实读 `CLAUDE.md:139` = 「aria-plugin 方法论轨: v1.52.0–v1.69.1 已 ship — 逐版本史见 aria/CHANGELOG.md (SOT);」, `:141` = 「版本: 插件 aria-plugin v1.69.1 | 主项目 v1.7.5 | …」。`tasks.md:89` 与 `TASK-041` 的「两行 (:141 + :139)」描述与实况逐字吻合; verification 补的 grep 断言填上了「无机械 check 兜底」这个洞 |
| §2.3.5 Amended 注记位置 | **一致且合该文件惯例** | 实读 `standards/conventions/session-handoff.md`: §2.3 (`:101`) 下 `:103-106` 为 `> **Added** / **Purpose** / **Status**` blockquote; §2.3.8 (`:217`) 下 `:219-221` 同形。v3 把注记从「节末小段」改到「紧贴 §2.3.5 标题下方」确与 3/3 既有惯例同形 |
| 回帖措辞 | 计划面一致, **proposal 面不一致** | 见上表 M-4 行 |

**镜头 4 — Level 3 完整性终检 (D1..D5 / SC-1..SC-11 ↔ 任务)**

SC 覆盖脚本实扫: SC-1..SC-11 **无一为空**, 每条至少一个任务在 title/verification/notes 里点名 (SC-1→1.1/4.1, SC-2→1.2/1.5/1.7, SC-3→0.2/1.8, SC-4→1.3, SC-5→3.1/3.2/3.3, SC-6→1.6, SC-7→4.2/4.3, SC-8→1.4, SC-9→1.11/3.4/3.5, SC-10→1.9, SC-11→1.10)。组 2 实现任务不直接引 SC 是设计如此 (它们引「TASK-00x 转绿」, 由 `tasks.md:109-119` 的 SC 映射表补上 RED→GREEN 链)。

D1..D5 逐条落任务: D1 → 2.1/2.2/2.3/2.4/2.5/2.7/2.8; D2 → 3.1/3.2/3.3; D3 → 2.3/2.9; D4 → 3.4/3.5/1.11 (七处文档 = 五文件改 + SKILL.md 明写不改 + templates 3.5); D5 → 5.2/5.7/3.6。D-0(a) 族键 → 1.7/2.5; D-3(a) 新鲜度 → 1.10/2.6/3.2。**唯一缺口**: `proposal.md:110` T2 点名的「`test_normalize_snapshot` 锁字段」在计划三文件里零命中 (见本轮 m-3)。

**scope creep 检查**: 39 个任务无一超出 proposal 的 T1-T13 + §Impact + CLAUDE.md 硬约束; 新增的 `TASK-042` 是 R2 M-1 处置, 对应 `proposal.md:104` 的「以 tracker issue 记录 S2 后续」子句, 不是新范围。

---

## 审计结论

### M-1 (major · issue · documentation) — proposal v9 自称「post_planning R2 后同步」, 但 R2 接受的 1 Critical + 4 Major 里有四处 proposal 面残留未改; 其中 SC-7 在 AC 层原样保留了本轮 Critical 判定为空判据的那个跑法

- **scope**: `proposal.md:4` (Status 自称) · `:132` (SC-7) · `:119` (T10) · `:120` (T11) · `:104` (§Impact ship 形态行)
- **summary**: v3 的 rework 只改了 R2 聚合报告逐字点名的那几行, 没有做同类面清扫。结果是 `tasks.md` + `detailed-tasks.yaml` 两层全部正确, 而 owner Approved 的 proposal 在四个位置停留在 rework 之前的说法。最要命的一处是 SC-7: 本轮唯一的 Critical (PP2-C1) 结论正是「`run_tests.py` 的 `unittest discover` 收不到 `test_collision.py` 的 pytest 裸函数 ⇒ 单跑它对 SC-1/2/8 的交付文件是空判据」, 而 SC-7 这条**验收标准本身**至今仍写着「state-scanner 全套 (`tests/run_tests.py`) 在点名改写后零回归」——把刚被判定为空的判据留在了 AC 层。
- **evidence** (四处均为实读原文):
  - `:132` 「- [ ] SC-7 (T10/T12) state-scanner 全套 (`tests/run_tests.py`) 在点名改写后零回归; …」。对照 `metadata.test_runner` 「两种跑法都必跑 … 差 16 全在 test_collision.py = SC-1/2/8 交付文件」与 `TASK-032` verification 「(a) run_tests.py … 且 Ran 数 ≥ 1476 …; (b) pytest 全套 … 且收集数 ≥ 1492 …」。三层里有一层没跟上。
  - `:119` 「- [ ] T10 全套回归: state-scanner 全套 **pytest** (起草日 1492 个 test 定义; 点名改写项全绿) … + 主仓 **14** state-check → SC-7」。两个问题叠一行: 「pytest」与 `:132` 的「run_tests.py」互斥 (且都不是「两种都跑」); 「14 state-check」是 R2 m-2 原样未动, 与 `:132` 的「13 条全绿 + `plugin-cache-currency` 例外」读法冲突 —— 正是 R1 C-2 要根除的那个读法。
  - `:120` 「- [ ] T11 回帖 … ship 后关 #193, **#135 留缺口 1/2**」, 无 S1/S2 分档。可达性不低: proposal 的 T1-T13 是**字面 `- [ ]` 复选框列表**, 读起来就是一份可执行清单; 执行者若照它办, 会在 S1 形态下对外宣告缺口 3 已闭 —— 这正是 R2 M-4 判定的超报, 且是关 issue + 公开留言这类难回收的外向动作。
  - `:104` 「… 否则 D 期以 tracker issue 记录 S2 后续 (先例 #192)」。R2 M-1 的结论有两半: (a) 该动作不是既有机制, 要有真承载体 (v3 已用 5.8 做到); (b) #192 是 deferred/unverified 非空时的**自动**路径, 与「把一张计划外的后续表登记成 issue」不同型。`tasks.md:103` 已经把 (b) 写清楚了 (「先例 sibling-spec-probe #192 是 deferred 非空时的自动路径」), proposal 这行没有。
  - `:4` Status 自称「v9 = post_planning R2 后同步 (SC-9 rule 1.54 子句改文档断言 / SC-3 S2 宿主句改 S2 后续表 / 孤儿引文清理)」—— 自陈的三项确已做到, 但「R2 后同步」这个标题相对于 R2 实际接受的处置集合是不完整的。按 memory `feedback_status_doc_claims_need_diff_verification_and_variant_sweep`, 「已同步」类声称须对 diff 逐条核对 + 同形变体清扫。
- **缓解因素 (故为 major 而非 critical)**: 执行层 (`tasks.md` + `detailed-tasks.yaml`) 四处全部正确, 且 `tasks.md:4` 明写 yaml 是 verification/deps 的单一 SOT; `tasks.md:115` 的 SC 映射表也写了「SC-7 | 4.2 (**两种跑法**)」。归档门只读 `tasks.md` checkbox (`spec_complete.py:186` + `:257-290` 实读确认, proposal 的 24 个未勾 `- [ ]` 不进归档判定), 所以不构成 ship 阻断。
- **建议**: 四处定点编辑, 全在 `proposal.md` 一个文件、四行:
  1. `:132` SC-7 首句改「state-scanner 全套**两种跑法都零失败** (`tests/run_tests.py` 的 unittest discover + `pytest` 全套; 前者收不到 `test_collision.py` 的裸函数, 单跑对 SC-1/2/8 是空判据 — post_planning R2 C-1)」。
  2. `:119` T10 改「state-scanner 全套两种跑法 (见 SC-7) … + 主仓 state-check (13 条全绿 + `plugin-cache-currency` 例外, 见 SC-7)」。
  3. `:120` T11 补分档, 与 `tasks.md:87` 同文。
  4. `:104` 把「D 期以 tracker issue 记录 (先例 #192)」改成「由 5.8 (`TASK-042`) 在 merge 后、归档前**手动**开 tracker issue; #192 是 deferred 非空时的自动路径, 与本例不同型」。
  5. `:4` Status 的 v9 括注补上以上四项。

### m-1 (minor · risk · documentation) — TASK-018 对「container-id 文件头注释改写成什么」三轮零断言

- **scope**: `tasks.md:62` (2.7) · `detailed-tasks.yaml` `TASK-018` verification
- **summary**: R1 m-1 → R2 m-1 → R3, 三轮未落。v2 只做了减法 (删掉「(label 仅展示)」这个反向措辞), 加法一直没做: 这条注释正是 #135 缺口 3 的诱因本体 (`proposal.md:19` 「文件头注释又邀请填 label ⇒ 填个可读名就静默换了协调身份」), 而任务只锁了 accessor 与 lock-in 两条代码断言, 注释写成什么完全自由。S1 形态下如果注释写成「label 仅用于展示」, 那是**反事实**的 (S1 不 flip, label 仍决定协调身份), 会把用户重新推回同一个坑。
- **evidence**: `TASK-018` verification 实读只有一条: 「TASK-008 label accessor 子句转绿; S1 lock-in 仍绿」。`git diff HEAD~1 HEAD` 对该任务零改动。
- **建议**: 加一条 S1 措辞锁: 「注释须写明 label **当前仍参与**协调身份 (S1), 将在后续版本改为仅展示; 反向 grep 锁「仅展示」不得作为对当前行为的描述单独出现」。

### m-2 (minor · risk · architecture) — TASK-033 未按 Rule #10 记录「`plugin-cache-currency` 例外是 AI 在 Approved 之后引入的」

- **scope**: `proposal.md:4` (Status 仍是原 Approved 戳) · `detailed-tasks.yaml` `TASK-033` verification
- **summary**: 例外本身站得住 (severity=warning + 两份 handoff 的成文先例, 落在 Rule #10 白名单「已成文 lane 降级」), R2 已判定不改。但被改的是一条 enabled 闸的**期望态**, 且发生在 owner 的 Approved 戳之后; Rule #10 末句要求「AI 任何自作主张的流程判断必须写进 handoff 请复议」。现在 verification 只要求记录 owner 的动作。
- **evidence**: `TASK-033` verification 实读: 「SC-7: custom_checks 中除 plugin-cache-currency 外 failed=0; plugin-cache-currency 输出为 STALE (installed < SOT) 且 handoff 记录 owner D 期动作 (/plugin marketplace update + /plugin update + 重启)」。无复议子句。R2 m-4 提出后 v3 零改动。
- **建议**: 追加一句「handoff 同时记录: `plugin-cache-currency` 例外为 post_planning R1 rework 引入 (owner Approved 之后), 请 owner 在 D 期复议」。零成本。

### m-3 (minor · issue · documentation) — proposal T2 点名的「`test_normalize_snapshot` 锁字段」在计划里零承载, 而该断言对真代码不成立

- **scope**: `proposal.md:110` (T2) · 计划三文件 (零命中) · `aria/skills/state-scanner/tests/test_normalize_snapshot.py`
- **summary**: Level 3 完整性终检里唯一的 proposal→任务 缺口。但它不该靠加任务补 —— 实读证明这条 proposal 子句本身就不成立: 该测试文件根本不锁 collision 字段集。计划静默丢弃它在实质上是对的, 只是没留痕。
- **evidence**:
  - `grep -rn "normalize_snapshot"` 对 `tasks.md` / `detailed-tasks.yaml` **零命中**, 只命中 `proposal.md:110`。
  - `aria/skills/state-scanner/tests/test_normalize_snapshot.py` (513 行) 对 `collision` / `identity` / `kind` / `groups` 四个 token **零命中**; `scripts/normalize_snapshot.py` 里仅有的两处 "collision" (`:70` / `:77`) 是「命名冲突」语义的英文注释, 与本 Spec 的 collision 段无关。
  - 新字段 `identity_advisories` 的字段集回归实际由 `tasks.md:45` (1.4, 两条 collector 测试的 `keys == {kind, groups}` 断言改写) + 4.2 双跑全套承担, 覆盖不缺。
- **建议**: 改 `proposal.md:110`, 把「+ `test_normalize_snapshot` 锁字段」删掉或改为「字段集回归由 1.4 的两条 collector `keys` 断言 + 4.2 双跑全套承担 (`test_normalize_snapshot` 实读不锁 collision 段)」。按 memory `feedback_never_write_unverified_impossibility_claims` / `feedback_spec_inherits_upstream_dec_errors`, 继承来的事实断言要么自验要么删。

### m-4 (minor · risk · architecture) — S2 激活是单向的, 没有回退条款; 撤销激活需要删 checkbox, 而删 checkbox 就是动归档门的输入

- **scope**: `tasks.md:103` (激活规则) · `detailed-tasks.yaml:41` (`metadata.s2_followup.activation`)
- **summary**: 镜头 1 的追问在正方向上已被结构解决 (6.x 是 merge 前置, 做不完卡在 merge 而非归档门)。但反方向没写: 激活之后若 S2 前提失效 (a1-entry 被 revert / ack 被撤回), 6.1-6.4 已经是 checkbox 且是 merge 前置, 整个 cycle 会楔死 —— 要回到 S1 只能删掉这四个 checkbox 与 TASK-027..030。而 checkbox 集合正是归档门 (`spec_complete.py`) 的输入, AI 自行删减它属于 Rule #10 语境下的流程判断, 不该临场做。
- **evidence**: `tasks.md:103` 与 yaml:41 的激活规则都只描述「满足三条件 ⇒ 追加」与「任一不满足 ⇒ 维持 S1」, 无「已激活后条件失效」这一支; yaml 头部注释 (`:7-8`) 只写「编号不可变 … 激活时追加 TASK-027..030」, 同样单向。
- **概率评估**: 低 —— 激活的两个条件 (a1-entry B.2 已落地 / #174 ack 已到) 在激活时点都是既成事实, 事后失效需要一次 revert。故 minor 而非 major。
- **建议**: 激活规则末尾加一句「激活后若 S2 前提失效, 回退 S1 须 owner 裁定并记入 handoff; AI 不得自行删除已追加的 6.x checkbox 或 TASK-027..030 (归档门输入, Rule #10)」。

---

## Verdict

PASS_WITH_WARNINGS (Critical 0 / Major 1 / Minor 4)。

计划层 (`tasks.md` + `detailed-tasks.yaml`) 本轮**零结构性缺陷**, 这是三轮里第一次: R2 的两条 Major 结构项都用结构改法解掉并经闭包实算复核 —— 组 0 真进了 merge 闭包 (`TASK-000`/`TASK-040` ∈ closure(TASK-034), 规模 30→32), S2 后续真有了硬承载 (5.8 是归档门必勾的 checkbox, 不再依赖 `_build_d_payload` 会不会产出)。`TASK-039` 闭包外恰为 `TASK-038` / `TASK-042` 两个 merge 后任务, 与预期逐项吻合, 零死支。镜头 1 追问的「6.x 归档前做不完」经 DAG 证明不可能发生 (6.x 是 merge 前置, 卡也卡在 merge), 因此**不需要**再补「追加即承诺同 cycle 完成」条款 —— 那条承诺已经是一条边。四个新引入的文本面 (双跑法 / TASK-020 独立路径 / CLAUDE.md :139 / §2.3.5 Amended 位置) 全部对真代码与真文件实读核验通过, 行号锚点无一漂移。

唯一的 Major 全部落在 `proposal.md` 一个文件的四行上, 根因是同一个: v3 的 rework 只改了 R2 聚合报告逐字点名的行, 没有对同类面做清扫, 于是 owner Approved 的 AC 文档停在了 rework 之前。其中 SC-7 那处的性质值得单独说——它把本轮 Critical 刚判定为「空判据」的那个跑法, 原样留在了验收标准里; 执行层三个位置都改对了, 唯独 AC 层没改, 而归档后 proposal 才是这次变更的长期记录。T11 那处则是把 R2 判定为超报的外向文案留在了一份**看起来可执行的 `- [ ]` 清单**里。四条修法都是定点编辑, 不动 DAG, 不动编号, 不动任何任务的 verification。

四条 minor 里两条是 R2 原样未处置的 carry (m-1 注释断言已连续三轮、m-2 Rule #10 留痕), 两条是本轮新面且都不需要新任务 (m-3 删一句失实的 proposal 子句、m-4 补一句回退授权)。

---

## Vote

REVISE

不投 PASS 的理由只有一条: Major 里的 T11 是外向且难回收的动作 (关 issue + 公开留言), SC-7 是 owner Approved 的验收标准本体, 这两处不适合按「B 期顺手项」处理 —— 顺手项的定义是「执行时带上即可」, 而这两处一旦执行时没带上, 一个已经发出去了, 一个已经归档成了长期记录。但这一轮的 REVISE 与前两轮性质不同: 修改面是**单文件四行**, 零 DAG 影响、零编号影响、零 verification 影响, R4 应是定点确认而非全面重审。

## 轮次记录

| 轮次 | 席位 | 结论 | 备注 |
|------|------|------|------|
| R1 | tech-lead | FAIL (2C / 5M / 2m) | 首轮; 归档门 `deferred-s2` 机制不存在 + `plugin-cache-currency` 不可绿 两个 Critical |
| R2 | tech-lead | PASS_WITH_WARNINGS (0C / 4M / 4m) | 验证 v2 结构改法; Critical 归零但 v2 引入两个新结构面 (S2 兜底无承载 / 组 0 不在 merge 闭包) + 两条 rework 下游漂移。R1 三态 closed 6 · partial 3 · open 0 |
| R3 | tech-lead | PASS_WITH_WARNINGS (0C / 1M / 4m) | 本轮镜头 = 稳定性核查。R2 三态: closed 5 (M-1 / M-2 / M-3 / M-4 / m-3) · open 3 (m-1 / m-2 / m-4)。**计划层零结构性缺陷** (闭包 / 拓扑 / 计数 / 编号 / 符号 全部机械实跑通过); 唯一 Major 集中在 proposal 一个文件的四行, 均为 R2 处置的 AB 面未清扫。严格判据集合 R3 ≠ R2 (Major 从 4 条结构+文档混合收缩为 1 条纯文档簇), converged=null 交编排层判。全部 finding 附实读 file:line 或脚本实跑输出; 未触碰任何仓内文件 |

**B 期顺手项 (不构成 finding, 执行时带上即可)**:
- `tasks.md:81` 的顺序摘要行「5.2 bump → 5.1 merge+tag → 5.3 → 5.7 → 4.3 → 5.6 PR → 5.5 回帖」未列 5.4 与新增的 5.8。拓扑实跑序是 `4.1 → 4.2 → 5.2 → 5.4 → 5.1 → 5.3 → 5.7 → 4.3 → 5.6 → 5.5 → 5.8`; deps 是 SOT, 摘要行只是导读, 执行时以 yaml 为准即可。
- S2 若激活, 除追加 6.1-6.4 与 TASK-027..030 外还须同步 `metadata.total_tasks` (39→43) 与 `metadata.agents` 三个计数 —— 激活规则至今没提这两个字段。v3 本身就是活例证 (加一个 TASK-042 就要动 38→39 与 knowledge-manager 8→9)。
- `TASK-033` 的 verification 含「handoff 记录 owner D 期动作」, 而 handoff 由 `phase-d-closer` 产出 (`tasks.md:19` 边界表已委托), 该条在 TASK-033 自身执行时点不可自验; 执行时按「记入待写 handoff 的 owner action 清单」处理。
- `tasks.md:46` (1.5) 里的 `` `aaaa1111` `` 仍是 backtick 形, D.2 gate 的符号 liveness 会稳定给一条 `ambiguous` unverified_claim (warn, 不 block)。想让 D.2 干净可改成非 backtick 写法。
- `TASK-016` (2.5, 改 `track_board.py:778-793`) 与 `TASK-020` (2.9, 在 `:796` 之后加独立段) 编辑同一文件的相邻区域, 且 v3 之后两者在 DAG 上无先后约束。同一 agent (backend-architect) 串行执行不成问题, 但若并行分派要注意落地顺序。

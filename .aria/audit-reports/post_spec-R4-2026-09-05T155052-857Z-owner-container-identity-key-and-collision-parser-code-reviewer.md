---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-09-05T15:50:52.857Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R4 — code-reviewer 席 (规格合规终检 + v4 全文内部一致性)

审计对象: `openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md` **v4** @ `addc8a1` (151 行)。只审不改, 未修改任何仓内文件。本轮实读: proposal 全文、本席 R3 报告与 R3 聚合、`collision.py` :60-66/:84-90/:111-126/:141-146/:298-302/:330-350/:363-386、`identity.py` :156-192/:220-224/:240-244、`track_board.py` :177-185/:410-418/:428-432/:741-760/:780-786、`handoff_multibranch.py` :516-524/:707-716、`phase1_gate.py` :292-296/:484-488/:771-775、`release_gate.py` :128-136 + 全文件 identity grep、`claim_lifecycle.py` :39/:88/:377-392、`coordination_ref.py:596`、`concurrent_tracks.py` :25/:133、`handoff_autofill.py:391`、`reconcile.py:151`、`constants.py:36`、`fetch_gate.py` :249-256、`test_collision.py` :118-132/:158/:261-296、`test_handoff_multibranch_collision_dedupe.py` :305/:1039、`SKILL.md:149-154`、`advanced-rules.md` :544-546/:570-580、`state-snapshot-schema.md` :1083-1088、`phase-1-collectors.md:75`、`layer-l-integration.md` :25-27/:73/:77、`RECOMMENDATION_RULES.md:31`、`aria/templates/session-handoff.md` owner-container 行、`session-handoff.md` :116/:178-186/:189/:204/:217/:234、a1-entry :571/:660、`.aria/state-checks.yaml` (`- name:` 实数 14)。

## R3 处置核对

| R3 编号 | 三态 | 依据 (v4 实读) |
|---|---|---|
| R3-M1 D-0(a)「语料中出现过」子句重引语料依赖 | **closed** | :35 改为 `track_to_claim_record` 一处纯形状剥离 `-[0-9a-f]{8}$`, 「行内确定, 不查语料」; 成文已知限制 (日期形尾段, 语料 1 例零合并); :71 D-0(a) 后果同步; T9 :114 三条夹具 (`slug-aaaa1111`/`slug-bbbb2222` 同组 / `x-20260719` 零碰撞 / `slug-abcdefg` 不剥) → SC-2 :123 条件用例。落点核对: `collision.py:347` 与 `track_board.py:783` 都经 `track_to_claim_record`, Layer L claim 不经它 ✓ |
| R3-M2 Positive「S1 由 T3b + ⚪ 缓解」可证伪 | **partial** | 核心闭合: :97 改为「label 陷阱结构性消除只在 S2 形态成立; S1 形态下 label 形态既无 flip 也无 ⚪, 只有 T3b 的 inventory 告警」; :38 T3b 两态 (S1 纯告警无抑制 / S2 发布门非运行时开关); SC-3 :124 拆「S1/S2 共同」与「仅 S2」; Rule #6 :101 注明 flip 臂仅 S2。**未纳入**: 本席 R3 修法第三句「SC-3 加 S1 下 `get_container_id()` 行为不变的显式断言」— SC-3 无此臂, 且 state-scanner `tests/` 零处引用 `get_container_id` (grep 空), S1 偷 flip 无任何既有测试变红 (见 m-3) |
| R3-M3 D-3(a) 零落点 | **closed** | T13 :118 (条件) + SC-11 :132; 共享谓词 `layer_h_is_fresh(row, now, days)` + `LAYER_H_ACTIVE_WINDOW_DAYS` 与 `STALE_TTL` 分名分量纲 (:89); collector/renderer 同一调用; SC-11 断「被截止行不出现在 groups」+「两处同 kind/groups」+「谓词只有一个实现」 |
| R3-m1 头部计数 + 两处行号 | **partial** | 「6 个 .py」对 (collision / identity / handoff_multibranch / track_board / phase1_gate / release_gate; constants.py 条件); `track_board.py:743-747` (dedupe 调用) / `:177-185 (import)` / `collision.py:367` 三处行号改对; 但 checkbox 计数写「13」, `grep -c '^- \[ \] T'` = **14** (T1..T13 + T3b) (见 m-1) |
| R3-m2 SC-2 统领句 / 零段 key 字面 | **closed** | SC-2 :123 拆「判定臂 (经 dedupe → classify())」/「advisory 臂 (对 dedupe 前全语料)」; :32 写明零段串 `identity_key = "/" + container` |
| R3-m3 `advanced-rules.md:578` 掉出同步面 | **closed** | :51 / :149 `:544-572,578` |
| R3-m4 SKILL.md「只引用字段名」为假 | **closed** | :51 改为「含取值字面 … 取值不变故不改动, 语义变更经 §2.3.5 + CHANGELOG 明示」; 实读 `SKILL.md:149` 含 `cross-owner / self_multi_container` 字面, 陈述与代码一致 |
| R3-m5 fetch_gate 夹具类别错 | **closed** | :52 「它只收 kind 字符串, 行为不变; 加一条 `kind="cross_owner"` 字符串夹具 (不是两段式夹具)」; `fetch_gate.py:175-181` 签名与 :251 分支一致 |
| R3-m6 SC-5 grep 未枚举 token / 「语料」用词 | **closed** | SC-5 :126 列正向 token (`identity_key` / 三态 / `unknown` / `非空` / `same-identity-multi-owner` / `全集`) 与反向 token (`等价类` / `aria/skills` / `lib/`; `/home/` / `Aether` / `forgejo-token-map`); §2.3.5 第三行 :42 改「采用方仓的 handoff 全集 (跨 track、跨分支)」。反向名单仍缺三个 proposal 自诺不引用的 token (见 m-2) |
| R3-m7 「pytest 基线 104」来源不明 | **closed** | T10 :115 改「起草日 1492 个 test 定义」(本轮 `grep -rc "def test_"` 合计 = 1492 ✓); SC-7 :128 只写「零回归」 |

计数: **closed 8 / partial 2 / open 0**。两条 partial 的残留都是一句断言 / 一个数字, 不动设计。

## 本轮镜头逐项

1. **Tasks ↔ SC 双向映射** (:105-118 ↔ :122-132): T1→SC-1 / T2→SC-2,SC-8 / T3→SC-3 / T3b→SC-3 / T4→SC-4 / T5→SC-5 / T6→SC-6 / T7→SC-9 / T8→SC-10 / T9(条件 D-0(a))→SC-2 条件用例 / T10→SC-7 / T11→无 (自陈文档动作, 归 D 期) / T12→SC-7 / T13(条件 D-3(a))→SC-11。反向 SC-1..SC-11 每条括注的 T 与正向一致, 无孤儿 SC、无断链。决策点→任务: D-0(a)→T9, D-1/D-2→T5 回填, D-3(a)→T13; R3 的孤儿分支已消失。头部 :103「代码 6 个 .py + 1 份规范 + 7 处文档 + 1 处代码消费方; 13 个 checkbox」: 6 个 .py ✓ (constants.py 只在 T13 条件下出现, 未计入可接受, 但 :8 代码落点把 `lib/constants.py` 列为无条件项, 两处口径不一); 1 份规范 ✓; 7 处文档 = D4 :51 七项逐个数 ✓; 1 处代码消费方 = fetch_gate + 其测试 ✓; **13 个 checkbox ✗, 实数 14** (T1 T2 T3 T3b T4 T5 T6 T7 T8 T9 T10 T11 T12 T13)。
2. **行号抽查 12 处**: `track_board.py:177-185` = `dedupe_latest_per_track_container as _dedupe_tracks_for_collision` 的 try/except import 块 ✓ (v4 已标 import); `:743-747` = `collision_input_tracks = _dedupe_tracks_for_collision(tracks)[0] …` ✓ (渲染器持有原始 `tracks` 自行 dedupe, D3 :47 陈述成立); `:783` = `claim_records.append(_track_to_claim_record(t))` ✓; `:412-417` = `oc_by_key[(o, c, s)] = oc` + `_label` 查表 ✓ (建表键用 `_split_owner_container`, 查表键用 `claim.owner/container/session`, 两段式下 `""` vs `"unknown"` 失配的 bug 成立); `collision.py:347` = `rec = track_to_claim_record(t)` ✓; `:367` = `for tid in sorted(verdicts.keys())` ✓; `:374-379` **偏 5 行**: :374-378 是注释, 「stale 捞回」代码在 :379-383 (`active_claims = list(verdict.yielders)` … `extend(c for c in verdict.superseded if c.status not in _TERMINAL)`); `identity.py:158` = `def get_owner()` ✓; `:185` = 无 `@` 分支 `return "unknown"` ✓ (:188 为 except 兜底同值); `:222` = `return label if label else uuid` ✓; `:242` = `return _hostname()` ✓; `phase1_gate.py:486` = `resolved_identity = get_identity()` ✓; `:773` = `acq: AcquireResult = acquire_claim(` ✓; `:294` = `verdict.winner.container == identity.container_id` ✓; `release_gate.py:132` = `rel: AcquireResult = release_claim_by_track(` ✓, 全文件对 `identity` 的引用只有 :18 docstring 的 `identity_error` 字样 ⇒ 「今天零 identity 耦合」✓; `release_claim_by_track` 签名 (`claim_lifecycle.py:377-384`) 确有 `identity: Optional[Identity] = None` 形参, `read_claims` 在 `coordination_ref.py:596` ⇒ T3b :108 的 release_gate 子任务 (import identity + `get_container_label()` + `read_claims` + 传 `identity=`) 可实现 ✓; `fetch_gate.py:251` = `elif collision_kind != "none":` ✓; `handoff_multibranch.py:518-523` dedupe 键构造 ✓ / `:709` dedupe 调用 ✓ / `:714` classify ✓。消费方六处 (`claim_lifecycle.py:39,88` / `concurrent_tracks.py:25,133` / `handoff_autofill.py:391` / `phase1_gate` 三行 / `release_gate:132` 间接) 逐行命中; 全仓 `get_container_id|get_identity()` 非测试调用者 grep 无第七处 ✓。
3. **Rule #6 substitute 集 baseline-failing 核对** (:101 点名 SC-1 / SC-2 / SC-3(S1 臂) / SC-4 / SC-8): SC-1 现值 `("","simonfish","bfe8285d")` / `("","","solo")` ✓ 先红; SC-2 判定臂前三条现 🟡/🟡/none ✓ 先红, advisory 臂函数不存在 ✓ 先红; SC-3 S1 臂 `get_container_label` 不存在 (grep `def get_container_label` 空) + 两 gate 无告警 ✓ 先红; SC-4 同 uuid 双 owner 现 dedupe 键含 owner 不折叠 ✓ 先红, board 键失配 ✓ 先红; SC-8 字段不存在 ✓ 先红。五条全是 baseline-failing 结构化测试 ✓。**SC-3 S1/S2 四处一致**: D1 :37-38 (`get_container_label()` S1 即落 / flip S2 才落 / T3b 两态) = T3 :107 = T3b :108 = Impact :100 (S1 不 flip / S2 flip + 发布门) = Positive :97 = Rule #6 :101 「flip 臂仅 S2」= SC-3 :124 「S1/S2 共同」/「仅 S2」。六处口径一致 ✓。
4. **SC-5 / SC-9 token 对 KM R2/R3 findings 的锁定**: 「非 unknown」→ SC-5 正向 token `unknown` 在 §2.3.1 与 §2.3.5 各一 ✓ (KM R3 A 锁住); 作用域 → 正向 token `全集` ✓ (KM R3 B 锁住); 无 Lab 私有路径 → 反向 `/home/` `Aether` `forgejo-token-map` 锁住 KM R2 C/D 的原始三个点名, **但** proposal 自己在 :140 (`10cglocal`) 与 :150 (Kairos `DEC-2026-09-04`, 「standards 不引用」) 另外自诺了三个不入 standards 的 token, 反向名单没列 (m-2); 七处文档 → SC-9 只对五处 grep (SKILL.md 零改动、template 条件改), 与 D4 :51 一致 ✓; 但「grep token A B C/D 在五文件各至少命中一次」量词歧义, `RECOMMENDATION_RULES.md:31` 今天写 `collision.kind != none`, 无任何取值字面 (m-4)。T2 点名的两条 `keys == {kind, groups}` 测试核对: `test_collision.py:274` 在 `test_real_collector_emits_cross_owner_collision` 体内 ✓; `test_real_collector_no_collision_is_none` :290 断 `coll == {"kind": "none", "groups": []}` 全等, 加字段即红 ✓ 点名正确; 第三处 `:130` 在 `test_classify_emoji_never_persisted` 内, 断的是 `classify()` 返回值 —— D3 :47 明写 `classify()` 签名不变、advisory 由 collector 层写入, 该测试不会红 ✓ 不构成遗漏。
5. **D-0 / D-2 / Level / Linked Issue / 符号**: D-0 四选项 :71-74 每项都有「后果」句, (a) 含已知限制与作用面, (b) 含「依赖对方返工」, (c) 含失去 🔴/🟡, (d) 含范围与 claim 让渡, 对称 ✓; D-2 三选项 :83-85 每项都写 `cross_owner` 可达性 ((a) 同 owner AI 会话间结构性不可达 / (b) 两操作者间可达 / (c) 可达但不可解释) ✓ (R3 TL m-1 闭合); Level 段 :3 「判据上是 Level 3」与「owner 维持 Level 2 = 显式 override」并列, 请 owner 二选一回填, 未替 owner 决定 ✓ (Rule #10); Linked Issue :6 单 code span、`, ` 分隔、行首无空白 ✓; 带圈数字 / 希腊字母 `grep -P` 零命中 (exit 1) ✓ (🔴🟡⚪ 是 collision 等级约定符, 不在禁用集)。
6. **实验表 / 合成用例**: v4 :56-66 与 v3 逐字相同 (判定模型不变), 本席 R3 已对冻结语料实跑复现, 本轮不重跑; 新增 `devbox01` 两 owner 不折叠一例与 R3 本席额外用例结论一致 ✓。

## 审计结论

### Critical

无。

### Major

无。

### Minor

**[R4-m1] 头部计数与一处行号精度 (R3-m1 残留)**
- type: issue / severity: minor / category: documentation / scope: proposal:103, :8, :148
- evidence: 「13 个 checkbox」实数 **14** (T3b 独立 checkbox 未计); :8 代码落点把 `lib/constants.py` 列为无条件项, 而 :103 「6 个 .py」不含它且 T13 是条件任务; :148 「stale 捞回 :374-379」实为注释块, 代码在 `collision.py:379-383`。
- 修法: 「14 个 checkbox (含 T3b; T9 / T13 条件)」; :8 给 `lib/constants.py` 加「(D-3(a) 时)」; 行号改 `:379-383`。B 期顺手。

**[R4-m2] SC-5 §2.3.9 反向 token 名单漏掉 proposal 自诺不入 standards 的三个词**
- type: issue / severity: minor / category: testing / scope: proposal:126 vs :140, :150
- evidence: :140 「不规定容器 `git config` 供给 (10cglocal); standards 不引用 Lab 私有文档」; :150 「Kairos `docs/decisions/DEC-2026-09-04-git-identity-scope.md` … standards 不引用」; SC-5 反向名单只有 `/home/` `Aether` `forgejo-token-map`。D-2 裁定文本回填 §2.3.9 时最容易顺手写进去的正是 Kairos DEC 编号。
- 修法: 反向名单加 `Kairos` `DEC-2026` `10cglocal`。B 期顺手。

**[R4-m3] SC-3 S1 臂缺「`get_container_id()` 行为不变」的 lock-in 断言; 仓内零既有测试锁 label 优先, S1 偷 flip 不会有任何红** (R3-M2 修法第三句未纳入)
- type: issue / severity: minor / category: testing / scope: proposal:124 (SC-3 「仅 S2」臂) / :100 (「未取得 ack 不动对方文本」)
- evidence: `grep -rl get_container_id aria/skills/state-scanner/tests/` 为空; a1-entry SC-3 (:571) 以「直接调 `get_container_id()` 的实现必红」为前提, 若 B.2 在 S1 形态下顺手 flip, 对方 SC-3 静默恒绿, 而 :100 承诺 S1 不 flip、未取得 ack 不动对方语义。SC-3 现在只在「仅 S2」臂断 uuid, S1 臂对 `get_container_id()` 零断言。
- 修法: SC-3 「S1/S2 共同」臂加一句「S1 形态下 `get_container_id()` 对 label 非空的 container-id 文件仍返回 label (与 `identity.py:222` 现值同)」; S2 落地时该断言翻转为 uuid。属 B 期一条断言, 不改设计; 若 owner 直接裁 S2 则自然消解。

**[R4-m4] SC-9 grep 量词歧义; `RECOMMENDATION_RULES.md:31` 今日无取值字面**
- type: issue / severity: minor / category: testing / scope: proposal:130 vs `aria/skills/state-scanner/RECOMMENDATION_RULES.md:31`
- evidence: 「grep token `cross_owner` `self_multi_container` `same-identity-multi-owner`/`identity_advisories` 在五文件各至少命中一次」可读成「每文件至少命中任一 token」(则 `layer-l-integration.md` / `advanced-rules.md` / `snapshot-schema.md` / `phase-1-collectors.md` 四处基线已绿) 或「每文件每 token 至少一次」(则 `RECOMMENDATION_RULES.md:31` 的 `collision.kind != none` 措辞须改, 且 `same-identity-multi-owner` 在 `phase-1-collectors.md:75` 这类只谈 worktree 创建的段落里未必有落点)。SC-9 不在 Rule #6 substitute 集, 基线绿本身可接受, 但断言应可机械执行。
- 修法: 写成两句: 「五文件各含 `cross_owner` 与 `self_multi_container` 至少一次」+「`state-snapshot-schema.md` 与 `advanced-rules.md` 含 `identity_advisories` 至少一次」(其余文件的 ⚪ 措辞按需)。B 期顺手。

### 核验通过、不构成 finding

- Tasks ↔ SC 双向零孤儿; 三个决策点的条件分支各有条件任务或回填任务。
- Rule #6 substitute 五条全部 baseline-failing; S1/S2 六处口径一致。
- 12 处行号抽查 11 处逐字命中, 1 处偏 5 行 (已并入 m-1)。
- T3b release_gate 子任务的三个前置 (`identity=` 形参 / `read_claims` / 零耦合现状) 全部实读成立。
- T2 点名的两条 `keys` 测试正确; 第三处同形断言作用于 `classify()` 返回值, 不受 collector 层新字段影响。
- D-0 / D-2 选项后果对称; Level 段 Rule #10 姿态; Linked Issue 格式; 带圈数字 / 希腊字母零命中; `.aria/state-checks.yaml` `- name:` 实数 14 与 T10/SC-7 一致。

## Verdict

**PASS** — 0 Critical / 0 Major / 4 Minor。

R3 本席 10 条: closed 8 / partial 2 / open 0; 两条 partial 残留 (checkbox 计数、S1 lock-in 断言) 已降为本轮 m-1 / m-3。v4 对 R3 九个 Major 簇的处置全部落在文本里且与代码现状逐行对得上; 判定模型自 v3 起未变, 本轮未发现任何需要在 B 期之前改动的项。

## Vote

**PASS**。理由: 剩余四条全是一个数字 / 三个 token / 一条断言 / 一句量词, 都能在 B.1 入口或 B.2 写测试时顺手落, 不影响 owner 对 D-0 ~ D-3 的裁定基础, 也不影响 Rule #6 substitute 集的成立。**B 期顺手项清单**: (1) m-1 计数与行号; (2) m-2 SC-5 反向 token 加三; (3) m-3 SC-3 S1 臂 lock-in 断言 (若裁 S2 则免); (4) m-4 SC-9 量词拆两句。

## 轮次记录

- R1 (code-reviewer): 0C/4M/5m, PASS_WITH_WARNINGS / REVISE。
- R2 (code-reviewer): 0C/2M/4m, PASS_WITH_WARNINGS / REVISE —— 等价类无数据通路 + 零 baseline-failing SC。
- R3 (code-reviewer): 0C/3M/7m, PASS_WITH_WARNINGS / REVISE —— D-0(a) 语料子句 / S1 缓解声称 / D-3(a) 零落点。
- R4 (本轮, 镜头: 规格合规终检 + v4 内部一致性): 实读 proposal 151 行全文 + R3 本席与聚合 + 上列 30 余处代码/文档/测试锚点; Tasks↔SC 双向映射、头部计数逐字、12 处行号、Rule #6 substitute 集 baseline-failing、S1/S2 六处口径、SC-5/SC-9 token 覆盖、D-0/D-2 对称性、Level/Linked Issue/符号。R3 处置 closed 8 / partial 2 / open 0; 新 0C/0M/4m; **PASS / PASS**。比较键集合与 R3 不重叠 (R3 三 Major 承载体均已改写), 非振荡, 逐轮收窄至 minor。

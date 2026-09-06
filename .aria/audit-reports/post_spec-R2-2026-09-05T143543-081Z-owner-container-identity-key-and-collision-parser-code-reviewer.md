---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-05T14:55:33.335Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R2 — code-reviewer 席 (v2 新增文本内部一致性 + 规格合规复检)

审计对象: `openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md` **v2** @ d23f103 (135 行)。只审不改。复核脚本 `scratchpad/exp_r2.py` (对冻结语料 `.aria/repro/handoff-tracks-frozen-2026-09-05.json` 用真函数跑 A / B / D 三变体 + 反事实「D 去掉步骤 3」+ 四个合成用例)。

## R1 处置核对

| R1 编号 | 结论 | 依据 (v2 实读) |
|---|---|---|
| M-1 实验表绕过生产 dedupe | **closed** | v2 :52-58 改为「冻结语料 996 行, 生产路径 dedupe → classify」; 三行数字全部复现: A `996→121` / `self_multi_container` / `[dev-claude, simonfishgit/dev-claude]`; B `996→122` / `cross_owner` / 上组 + `[simonfish/dev-claude, simonfish/dev-claude2]`; D `996→122` / `self_multi_container` / 同 B 两组。:62 的 advisory 对象 (`023236f2` / `bfe8285d` 各 `[aria-runner-bot, simonfish]`) 与主机名容器 owner 集 (`dev-claude: ['', simonfish, simonfishgit]`, `dev-claude2: ['', simonfish]`) 逐字一致。:64「真实语料里没有真正的两人撞车」被数据支撑 (D 变体两组均为同 owner 串或零段/两段混写, 无 cross_owner) |
| M-2 dedupe「不改逻辑」与 SC-4 互斥 / advisory 数据流 | **partial** | 前半闭合: :34 dedupe 键改 `(track_id, identity_key)` 列为显式改动项, :36 board 键同源列为显式改动项, T4 :100 点名两条既有测试改写。后半**未闭合**: v2 :35 / :46 写「advisory 由 classify() 从全语料并查集产出」, 但 collector 仍只把 dedupe 后的行传给 classify (:709-714 未列入改动), classify 签名 `(tracks, *, now)` (collision.py:300) 无全语料入口; 见新 finding R2-M1 |
| M-3 单 container 多 owner 谓词未定义 | **closed** | :35「先按 identity_key 分组, 同一 identity_key 内多 owner 不参与 collision 计数; 空 / unknown owner 不构成独立类」把并集 vs 代表的歧义消掉 (同 key 恒同类) |
| M-4 (a)+(a) 消解历史双串不成立 | **closed** | :69 D-1(a) 后果句改为「靠 D1 步骤 3 等价类消解 (只覆盖在 uuid 容器上共现过的串); 从未共现的两个串仍会 cross_owner 一次」; :74-77 D-2 不再宣称消解历史; :43 明写历史不 rewrite, 等价类让历史双串归同一身份 —— 与步骤 3 自洽 |
| m-1 9 种串 / 2 台机器 | **closed** | :19「10 种 owner-container 串, 对应 5 个 container 标识 (3 个 uuid + 2 个主机名), 实际 2 台在用的机器」 |
| m-2 契约引入点 83a1a45 | **closed** | :17「契约起点 aria f9306a0 2026-05-20 的 track_board.py, 83a1a45 05-30 迁入 collision.py」; `git -C aria log -1 f9306a0` = 2026-05-20 TASK-016/017, 83a1a45 = 2026-05-30, 一致 |
| m-3 §2.3.3 应引 §2.3.6 | **closed** | :33「§2.3.6: 写入频度 = 会话结束一次」; session-handoff.md:189 = `### 2.3.6`, :198 = 写入频度行 |
| m-4 Rule #6 点名含非测试 SC; advanced-rules:578 未列 | **closed** | :92 点名 SC-1 / SC-2 / SC-3 / SC-4 / SC-8 (五条全是结构化测试, 各自标了「对当前代码先红」的子句); :50 / T7 :103 把 `advanced-rules.md:578` 列入同步面 (实读 :578「collision helper 已按 owner+container 归类」仍在) |
| m-5 T/SC 孤儿 + schema bump 无锁 | **closed** | T8 :104 → SC-7; T9 :105 自陈「文档动作, 无 SC; 归 D 期 closeout」; T2 :97 schema bump → SC-8 :116 + `test_normalize_snapshot` (文件 `tests/test_normalize_snapshot.py` 实存) |

计数: **closed 8 / partial 1 / open 0**。

## 本轮镜头逐项

1. **Tasks ↔ SC 映射** (:96-117): T1→SC-1 / T2→SC-2,SC-8 / T3,T3b→SC-3 / T4→SC-4 / T5→SC-5 / T6→SC-6 / T7→SC-9 / T8→SC-7 / T9→无 (自陈)。反向 SC-1..SC-9 各有 T。无孤儿, T9 无 SC 合理 (回帖 / 关票是 closeout 动作)。但 T4 的「⚪ 行」渲染项没有任何 SC 断言 (见 R2-m4)。
2. **实验表 v2**: 三行数字复现 (见 M-1 行)。合成用例段 (:60) 四例复现: 两人两机 → cross_owner; 同容器双 owner → none; 同人两机 (同串) → self_multi_container; 漂移 `aria-runner-bot/bfe8285d` + `simonfish/023236f2` → **只有用全语料并查集时**才是 self_multi_container, 用输入两行自建并查集或不用等价类都是 cross_owner。前提「等价类由冻结全语料建」在 D1 文本里**没有数据流** (见 R2-M1 / R2-M2)。
3. **D1 步骤 3 与 D-1(a)**: 自洽 (等价只来自共现; 从未共现 → 一次 cross_owner)。SC-2 「同人两机」用同一 owner 串, 用词准确 (同 owner 串 ≠ 同等价类, 文本没混); 代价是 SC-2 完全没有「不同 owner 串、靠等价类归一」的用例 (见 R2-M2)。
4. **Level 复议段** (:3): owner 指令与 R1 审计建议并列, 明写「请 owner 复议」, 不替 owner 决定, Rule #10 姿态正确。数字核对: 「1 份规范」= session-handoff.md, 对; 「3 处消费文档」= D4 三处, 对; 「5 个代码文件」与「9 个任务」**对不上** (见 R2-m1)。
5. **消费方全列** (:90): `grep -rn 'get_container_id\|get_identity' aria/` 非测试命中只落在 identity.py 自身 / `lib/__init__.py` 再导出 / claim_lifecycle.py:39,88 / concurrent_tracks.py:25,133 / phase1_gate.py:84,123,486 / handoff_autofill.py:407-409; release_gate.py 不直接 import identity, 经 `release_claim_by_track` (:132) → claim_lifecycle `_resolve_identity` (:83-88) 间接消费。模块级全列**成立, 无遗漏**; 行号精度三处偏 (见 R2-m2)。
6. **规格**: Linked Issue :6 `10CG/Aria#193, 10CG/aria-plugin#135` 单 code span、`, ` 分隔、行首无空白、ASCII 冒号 (spec-drafter SKILL.md:349-351 三条满足); 带圈数字 / 希腊字母 `grep -P` 零命中 (exit 1); §2.3.6 已改对; f9306a0 已改对; Rule #6 点名集 SC-1/2/3/4/8 全为结构化测试; `.aria/state-checks.yaml` 实数 14 与 T8 / SC-7 一致; References 行号 (collision.py :63/:86/:143/:300/:374-379, identity.py :191/:222/:242, handoff_multibranch :518-523/:709-714, track_board :412-417/:430, reconcile.py:151, constants.py:36, layer-l-integration.md:14,73, RECOMMENDATION_RULES.md:31, advanced-rules.md:578, a1-entry :571/:660) 逐行实读全部命中。

## 审计结论

### Major

**[R2-M1] 「全语料并查集」在两个 classify 调用点都没有数据通路, 且与 Impact Risk (3) 的契约互斥**
- type: issue / severity: major / category: architecture / scope: proposal:35, :46, :89 Risk(3), T2 :97, T4 :100
- summary: D1 步骤 3 与 D3 都要求 classify() 用「collector 扫到的全部非 legacy 行 (不是 dedupe 后的行)」建并查集; 但生产路径只把 dedupe 后的行传入 classify, 渲染器又独立再算一次 classify_claims; Spec 既没改这两处的入参, 又在 Risk (3) 锁「classify 只接受 dedupe 后输入」。实现者按现文可以合法地用 dedupe 后输入建类, 全部 SC 仍绿, 而漂移用例翻成 cross_owner。
- evidence: `collision.py:300` `def classify(tracks, *, now=None)` 无第二输入; `handoff_multibranch.py:709` `deduped_tracks, dedupe_stats = dedupe_latest_per_track_container(tracks)` → `:714 collision = _classify_collision_summary(deduped_tracks)` (v2 未把 :709-714 列入改动, T4 只改 :518-523 的键); `track_board.py:430` `collision_kind, _severity = _classify_collision(active_claims)` 是第二个独立判定点, 只拿到本 track 的 ClaimRecord, v2 :46 仅称「解包不受影响」; proposal:89 Risk (3)「SC 锁『classify 只接受 dedupe 后输入』的契约注释」与 :35「对全语料 … 不是 dedupe 后的行」并读互斥; 脚本输出 `drift self vs other: corpus-uf=self_multi_container / local-uf=cross_owner`。
- 修法: D1 步骤 3 写死并查集的**产地与传递**: 例如 collector 在 dedupe 前对 `tracks` 调一个新函数 `build_owner_classes(tracks)`, 结果经 classify 的新关键字参数 (或随 snapshot additive 字段) 传给 classify 与 track_board; Risk (3) 改为「classify 的 collision 判定只接受 dedupe 后输入, 等价类输入另走 X」; T2 / T4 相应点名 :709-714 与 track_board :430 为改动行。

**[R2-M2] 步骤 3 的共现等价类没有任何 baseline-failing SC: 反事实「不实现等价类」下 SC-2 / SC-6 全绿**
- type: issue / severity: major / category: testing / scope: SC-2 :110, SC-6 :114, 实验表 :60
- summary: 唯一需要共现等价类才能判对的用例 (漂移后本容器 vs 对方容器) 只写在实验表 prose 里, 没进 SC。SC-2 三组 + 端到端 + SC-6 冻结语料在「只做步骤 1 + 步骤 2 + 空 owner 不成类」的实现下结果完全相同。R1-C1 要解的正是这条 (同人两机、串各自漂移), 现在处于无锁状态。
- evidence: 脚本 `D three-step` 与 `D minus step3 (no equivalence)` 在冻结语料上同为 `self_multi_container` + 同两组; 合成用例 `two people two machines / same container dual owner / same person two machines` 三例 `no-equiv` 列与 `corpus-uf` 列结果一致; 仅 `drift self vs other` 分叉 (`corpus-uf=self_multi_container`, `no-equiv=cross_owner`); SC-2 :110 全文无「不同 owner 串经等价类归一」用例。
- 修法: SC-2 增第四组 (对当前代码与「无等价类」实现都先红): 等价类语料含 `simonfish/bfe8285d` 与 `aria-runner-bot/bfe8285d` 共现, 待判两行 `aria-runner-bot/bfe8285d` + `simonfish/023236f2` → `self_multi_container`; 并加一组反例: 语料无共现时同两行 → `cross_owner` (锁 D-1(a) 后果句)。

### Minor

**[R2-m1] Level 复议段的两个计数与正文对不上**
- type: issue / severity: minor / category: documentation / scope: proposal:3 vs :29-50, :96-105
- evidence: 正文点名的代码文件是 `collision.py` / `handoff_multibranch.py` / `track_board.py` / `identity.py` 四个 (:29, :36, :37, :46), 第 5 个未出现 (若算 T6 fixture json 或 `state-snapshot-schema.md` 应注明); Tasks 段 `grep -c '^- \[ \] T'` = **10** (T1..T9 + T3b), 头部写「9 个任务」。
- 修法: 改为「4 个代码文件 (+1 测试 fixture)」与「10 个任务 (含 T3b)」, 或注明口径。

**[R2-m2] 消费方表行号精度: 一处缺、两处指向声明行而非调用行**
- type: issue / severity: minor / category: documentation / scope: proposal:90
- evidence: `scripts/release_gate.py` 无行号, 实为 :132 `release_claim_by_track(` → `claim_lifecycle.py:83-88 _resolve_identity` 间接消费; `handoff_autofill.py:391` 是 `def owner_container():`, `get_identity()` 调用在 :407-409; `phase1_gate.py:294` 是比较式, `get_identity()` 调用在 :486 (:84/:123 import)。模块级全列无遗漏。
- 修法: 补 `release_gate.py:132 (经 claim_lifecycle 间接)`, `handoff_autofill.py:407-409`, `phase1_gate.py:486 (比较点 :294)`。

**[R2-m3] D-3(a) 新鲜度截止是否作用于并查集语料未写, 会让等价类随时间失忆**
- type: risk / severity: minor / category: architecture / scope: proposal:80 D-3(a), :35 步骤 3
- evidence: :80 只说 stale 行「不参与 collision 判定」; :35 说等价类对「全语料」建。若实现把截止套到全语料, `bfe8285d` 上 `simonfish` 行止于 08-27 (:18), 30 天后与 `aria-runner-bot` 不再共现, 漂移用例回到 cross_owner。
- 修法: D-3(a) 加一句「截止只作用于判定集合, 并查集仍用全语料 (含 stale / done 行)」, 并在 SC-2 第四组的语料里放一条超期行验证。

**[R2-m4] D3 看板 ⚪ 行是四个交付面之一, 但没有 SC 断言其渲染**
- type: issue / severity: minor / category: testing / scope: D3 :46, T4 :100, SC-4 :112, SC-8 :116
- evidence: SC-4 只锁 dedupe 折叠 / 不折叠 / 原串回显 / 既有测试仍绿; SC-8 只锁字段存在与旧 snapshot 不崩; 无一条断言「advisory 非空时 board 输出含 ⚪ 行与 identity_key / owners」。
- 修法: SC-4 追加「给定含 1 条 identity_advisories 的 snapshot, `render_track_board` 输出恰 1 行 ⚪, 含 `bfe8285d` 与两 owner」(对当前代码先红)。

## Verdict

**PASS_WITH_WARNINGS** — 0 Critical / 2 Major / 4 Minor。

规格合规复检全部通过 (Linked Issue / 符号 / 引用行号 / Rule #6 点名 / Rule #10 姿态); R1 的 4 Major + 5 minor 有 8 条闭合、1 条 (M-2 后半) 部分闭合。v2 的实验表和三步判定在冻结语料与合成用例上全部复现, 方向正确。剩下的两条 Major 是同一个根: 步骤 3 的「全语料等价类」是 v2 用来闭合 R1-C1 的关键机制, 但它既没有数据通路 (两个 classify 调用点都只拿 dedupe 后 / 本 track 的行, 且 Risk (3) 的契约与它互斥), 也没有任何 SC 能在「没实现它」时变红。这两条是 spec 文本可机械修正的缺口, 不需要推翻设计。

## Vote

**REVISE** (补 R2-M1 数据通路 + R2-M2 第四组 SC 后可进 A.2; 四条 minor 顺手)。

## 轮次记录

- R1 (2026-09-05, code-reviewer): 0C/4M/5m, PASS_WITH_WARNINGS / REVISE — 实验表绕过 dedupe、dedupe 与 SC-4 互斥、谓词未定义、(a)+(a) 消解论证失据。
- R2 (2026-09-05, code-reviewer, 换镜头: v2 新文本内部一致性): 实读 proposal 135 行全文、R1 本席与聚合报告、collision.py :55-215 / :295-403、handoff_multibranch.py :136-152 / :490-545 / :709-714、track_board.py :385-440、identity.py 相关行、claim_lifecycle / phase1_gate / concurrent_tracks / release_gate / handoff_autofill 消费点、session-handoff.md §2.3 标题与 §2.3.5 表、spec-drafter SKILL.md :342-360、a1-entry :571/:660、`.aria/state-checks.yaml` (14); 对冻结语料 996 行用真函数跑 A / B / D + 反事实 + 四合成用例 (`scratchpad/exp_r2.py`)。R1 处置 closed 8 / partial 1 / open 0; 新 0C/2M/4m; PASS_WITH_WARNINGS / REVISE。

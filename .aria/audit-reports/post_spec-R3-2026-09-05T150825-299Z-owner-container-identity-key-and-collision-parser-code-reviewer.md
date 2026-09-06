---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-05T15:08:25.299Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R3 — code-reviewer 席 (规格合规复检 + v3 全文内部一致性)

审计对象: `openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md` **v3** @ `91b86fb` (143 行)。只审不改, 未修改任何仓内文件。复核脚本 `scratchpad/cr_r3_v3.py` (对冻结语料 `.aria/repro/handoff-tracks-frozen-2026-09-05.json` 用真 `track_to_claim_record` / `reconcile_all` / `_dedupe_sort_key` + 按 v3 :31-34 字面实现的两段解析 / `identity_key` / 判定规则跑实验表 v3 行 + 9 个合成用例 + D-0(a) 尾段分析)。已读 tech-lead R3 报告, 涉及同簇处标注, 结论独立得出。

## R2 处置核对

| R2 编号 | 三态 | 依据 (v3 实读) |
|---|---|---|
| R2-M1 全语料并查集在两个 classify 调用点无数据通路, 与 Risk (3) 互斥 | **closed** | 承载体删除: :4 / :34 明写撤销等价类, 判定输入只剩 dedupe 后同 track 的行; advisory 改为独立函数 `identity_drift_advisories(tracks)` (:45), collector 在 `handoff_multibranch.py:709` dedupe **之前**对原始 `tracks` 调用, 渲染器同调。实读 `track_board.py:743-747` 渲染器确实持有原始 `tracks` 并自行 dedupe, 该调用可行。Risk (3)「classify 只接受 dedupe 后输入」与 advisory 不再互斥 (advisory 不经 classify) |
| R2-M2 等价类零 baseline-failing SC | **closed** | 随撤销失效; 我 R2 建议的反例 (语料无共现时 `aria-runner-bot/bfe8285d` + `simonfish/023236f2` → `cross_owner`) 已进 SC-2 :116 第四条并在实验表 :60 成文。本轮实跑: 该用例 v3 规则下 = `cross_owner` |
| R2-m1 头部计数 (5 个代码文件 / 9 个任务) | **partial** | 「4 个 .py」已改对; 但 checkbox 数写「11」, `grep -c '^- \[ \] T'` = **12** (T1..T11 + T3b); 且 T3b 要改 `phase1_gate.py` / `release_gate.py` 启动路径, 「4 个 .py」在 v3 下又变成低估 (见 m-1) |
| R2-m2 消费方行号精度 | **closed** | :94 补 `release_gate.py:132` (间接) / `phase1_gate.py:294` (比较) 与 `:486` (调用) / `handoff_autofill.py:391` 标注 `def owner_container`; 五处逐行实读命中 |
| R2-m3 D-3(a) 截止是否套到 advisory 语料 | **closed** | :45 末句「D-3 的新鲜度截止**不**作用于 advisory (它是漂移史, 不是活跃信号)」 |
| R2-m4 ⚪ 行渲染无 SC | **closed** | T8 :108 → SC-10 :124 (恰 2 条 ⚪ 行 / owners[] + first/last_seen / 无 advisory 不渲染) |

计数: **closed 5 / partial 1 / open 0**。

## 本轮镜头逐项

1. **Tasks ↔ SC 双向映射** (:100-124): T1→SC-1 / T2→SC-2,SC-8 / T3→SC-3 / T3b→SC-3 / T4→SC-4 / T5→SC-5 / T6→SC-6 / T7→SC-9 / T8→SC-10 / T9→SC-2 (条件) / T10→SC-7 / T11→无 (自陈文档动作)。反向 SC-1..SC-10 各有 T, 无孤儿 SC。T9 的条件性与 SC-2 末句「D-0(a) 时…」条件一致; T11 无 SC 合理。**决策点 → 任务方向有一个孤儿**: D-3(a) 选中时要写代码 (常量 + 过滤谓词), 但 Tasks 无条件任务、SC 无机制断言, 只在 SC-6 括注结果计数 (与 tech-lead R3 M-4 同簇, 见 M-3)。头部 :98「4 个 .py + 1 份规范 + 7 处消费面; 11 个 checkbox」: 7 处消费面 = D4 五处文档 + `fetch_gate.py` + `test_fetch_gate.py`, 对; 1 份规范对; 4 个 .py 与 11 个 checkbox 都不对 (m-1)。
2. **实验表 v3 与 7 个合成用例**: 全部按 :31-34 字面规则复现。语料行 `996→122` / `self_multi_container` / 两组 `[simonfish/dev-claude, simonfish/dev-claude2]` + `[dev-claude, simonfishgit/dev-claude]`; advisory 对象 `023236f2` / `bfe8285d` 各 `[aria-runner-bot, simonfish]`。合成 7 例: 两人两机 `cross_owner` / 同容器双 owner `none` + 恰 1 条 advisory / 同人两机 `self_multi_container` / 漂移后 `cross_owner` / 隔离夹具对 `cross_owner` (实读 `test_handoff_multibranch_collision_dedupe.py:305-323` 用的正是 `aria-runner-bot/023236f2` + `simonfish/bfe8285d`) / 零段 vs 两段同主机名 `self_multi_container` / `erin`+`frank` 同机 `none` + advisory。额外两例: 三 owner 同 uuid → advisory owners 长 3; `alice/devbox01` + `bob/devbox01` → 不折叠、`cross_owner` (对抗 `len==8`)。**零段 owner 为空的处理**: :32 公式「否则 ⇒ `owner + "/" + container`」对 owner="" 机械得 `/dev-claude`, 与 `simonfishgit/dev-claude` 是两个 key, 非空 owner 集合 = {simonfishgit} → 🟡; 结论不依赖实现者选 `/dev-claude` 还是 `dev-claude` (两种写法都与两段 key 不同), 所以未写明**不影响结果**, 但 §2.3.1 的标准文本 (:39) 写的是 `<owner>/<container-id>`, 对零段行 `<owner>` 缺席时的字面形应在 SC-1/§2.3.1 里点一句 (并入 m-2 修法)。
3. **D-0(a) 语料条件 vs 纯输入原则**: 矛盾成立, 见 M-1。
4. **S1/S2 × Positive × T3/T3b × SC-3**: SC-3 :117 已按「S2 形态:」「S1/S2 共同:」分臂, T3 :102 标「S2 才落」, Rule #6 行 :96 把 SC-3 列进 baseline-failing 集合在 S1 下仍成立 (告警臂对当前代码先红)。**不一致点**在 Positive :92 末句「S1 形态下由 T3b 检查 + ⚪ 缓解」: ⚪ 结构上覆盖不到 label 形态, T3b 在 S1 无 flip 可拒 (M-2)。
5. **§2.3.5 三行判据用词**: 前两行只用 `identity_key` / `<owner>` / track (均 §2.3.1 定义) ✓; 第三行用了「语料」(标准里无此词) 且 D1 :34 的「非 `unknown`」未出现在标准句里 (`unknown` 是 aria 填充值, 标准只说非空, 可接受)。SC-5 的 grep 断言谓词不可机械执行 (m-6)。
6. **规格**: Linked Issue :6 单 code span、`, ` 分隔、行首无空白 ✓; 带圈数字 / 希腊字母 `grep -P` 零命中 (exit 1) ✓; Level 段 :3 把「判据上是 Level 3」与「owner 维持 Level 2 = 显式 override」写成并列事实并请 owner 二选一回填, 未替 owner 决定 ✓ (Rule #10)。引用行号实读 13 处: `fetch_gate.py:251` ✓ (`elif collision_kind != "none"`), `advanced-rules.md:544-572` ✓ (rule 1.54 conditions..context 段), `phase-1-collectors.md:75` ✓, `state-snapshot-schema.md:1085` ✓ (`kind: str # enum`), `track_board.py:412-417` ✓ / `:430` ✓, `handoff_multibranch.py:518-523` ✓ / `:709-714` ✓, `collision.py:63/:86/:113-124/:143/:300/:374-379` ✓, `identity.py:191/:222/:242` ✓, `session-handoff.md:116/:178-186/:189/:204/:217/:234` ✓, `phase-a-spec-planning.md:126-137` ✓, `layer-l-integration.md:25-27,73,77` ✓, `RECOMMENDATION_RULES.md:31` ✓, a1-entry `:571/:660` ✓, 六处消费方 ✓, `.aria/state-checks.yaml` 实数 14 ✓。**两处偏**: `track_board.py:176-183` 是 import 块不是「它自己 dedupe」的调用点 (调用在 :743-747); `collision.py:363` 是 `overall_kind = "none"`, track_id 分组循环在 **:367** (m-1)。

## 审计结论

### Major

**[R3-M1] D-0(a) 的实现子句「仅当该 8hex 是语料中出现过的 `identity_key`」把语料依赖装回判定链上游, 与 :29「全部是纯输入函数, 不读语料历史」与 :128 非目标互斥; 且该条件在今日全部真实数据上买不到任何区分度** (与 tech-lead R3 M-1 同簇, 独立复现, 给出措辞修法)
- type: issue / severity: major / category: architecture / scope: proposal:67 (D-0 (a)) vs :29, :34, :128
- summary: 族键剥离决定两行是否落同一 `track_id`, 因而决定 `kind`; 剥离条件挂在「语料出现过」= 分组结果随本机 `branches_scanned` 变化 —— 正是 R2 撤销等价类的第二条理由。D-0 是 owner 在 B.1 前要裁的选项, 现在 (a) 带着一条与全篇原则相反的实现子句呈上去。
- evidence: 冻结语料 117 个 distinct `track_id` 中尾段匹配 `-[0-9a-f]{8}$` 的**只有 1 个**: `aria-plugin-113-gate-result-yaml-20260719` (尾段是日期); 其 `20260719` 不在 uuid `identity_key` 集合 `{023236f2, bfe8285d, f9c6e8cd}` 里, 且纯形状剥离后与任何其他 `track_id` 零合并。⇒ 「语料查表」与「纯形状」两个变体在今日数据上输出完全一致, 查表只换来非确定性。
- 措辞修法 (三选一, 不代裁, 但 (a) 必须改成纯输入判据):
  - **形状剥离**: 「分组键 = `track_id` 去掉尾部 `-<8 位小写 hex>` 段 (纯形状, 不查语料)」+ 成文已知限制「尾段恰为 8 位 hex 的非容器后缀 (如日期 `20260719`) 会被剥, 只在剥后前缀与另一条真 track 相同时才产生误合并; 冻结语料实测 0 组」。确定性、零状态, 与 :29 一致。
  - **自匹配**: 「仅当尾段 == 本行 `owner-container` 的 container 段」—— 也是纯单行输入, 且日期尾段不会命中。**但有洞**: §2.3.8.2 (:234) 推荐跨容器接棒时复用同一 frontmatter `track-id`, 容器 B 写出的 `<slug>-<uuidA>` 行尾段 ≠ B 自身 container ⇒ B 的行不剥、A 的行剥 ⇒ 两行分到不同组, 漏报。若选此法须把这个洞成文。
  - 任一写法都要同时写明**作用点只在 Layer H**: 在 `track_to_claim_record` (`collision.py:86`) 改写 `ClaimRecord.track_id`, 该函数只被 `collision.py:347` 与渲染器调用, Layer L 真 claim 不经它 (tech-lead R3 M-2 已展开, 本席核对 `reconcile.py` 分组确为跨层共用, 不重复举证)。

**[R3-M2] Positive :92「S1 形态下由 T3b 检查 + ⚪ 缓解」两个缓解在 S1 下都不成立, 是一句可证伪的效果声称** (与 tech-lead R3 M-3 同簇, 独立举证)
- type: issue / severity: major / category: architecture / scope: proposal:92 (Positive 末句) / :36 (T3b 语义) / :45 (advisory 产出面) / :102-103 / :117
- summary: label 陷阱 = 用户填了 label 后 container 段从 uuid 静默变成 label。⚪ 只对 **uuid 形** `identity_key` 产出 (:45 逐字「输出每个出现 ≥2 个非空 owner 串的 uuid `identity_key`」); label 形态下 `identity_key = owner/label` 是非 uuid 形, 结构上不进 advisory。T3b 的动作「拒绝在本次运行 flip 语义 (走旧口径)」在 S1 无 flip 可拒 (T3 :102「`get_container_id()` uuid 优先 S2 才落」⇒ S1 的 `identity.py:222` 仍是 `return label if label else uuid`, 旧口径就是现状), FAIL 分支只剩打印。
- evidence: 按 :32 规则, 同一台机 flip 前 `simonfish/bfe8285d` → key `bfe8285d`, 填 label 后 `simonfish/mybox` → key `simonfish/mybox`; 两 key 都不满足 :45 的「uuid `identity_key` 出现 ≥2 owner」⇒ 零 ⚪; 判定上两 key + 一个 owner ⇒ 🟡 且无解释行。这恰是 :92 声称被缓解的形态。SC-3 :117 只断言「输出迁移告警」, 无一条断言 flip 被抑制, 因此 B.2 全绿不会暴露。
- 修法: :92 末句改为「S1 形态下 label 陷阱**不消除**, T3b 只做 inventory 告警 (无抑制)」; :36 的「拒绝 flip」句限定到 S2 并写清作用域是发布期闸 (检查不过则本次发布不 flip) 而非运行期分支; SC-3 告警臂加「S1 下 `get_container_id()` 行为不变」的显式断言, 免得实现者在 S1 偷偷 flip。

**[R3-M3] D-3(a) 是唯一「选中即要写代码」却在 Tasks / SC 零落点的决策分支; 其过滤点在 collector (`collision.py:335-338`) 与 renderer (`track_board.py:754-757`) 是两份靠注释对齐的镜像, Spec 未要求同源** (与 tech-lead R3 M-4 同簇; 本席从 Tasks↔SC 映射镜头独立发现)
- type: issue / severity: major / category: implementation / scope: proposal:84 (D-3 (a)) / :98-111 (Tasks) / :120 (SC-6 括注)
- summary: 映射表里 D-0 有 T9 (条件任务)、D-1/D-2 有 T5 回填, D-3(a) 没有任何 T; SC 里只有 SC-6 的「(D-3(a) 时 0 组)」是结果计数, 不断言「早于 N 天的行不参与判定」这个机制。若 owner 选 (a), B.2 没有交付面可勾。
- evidence: Tasks 全表 :100-111 实读, 无「新鲜度 / 截止 / 常量」字样; `collision.py:332-334` 注释逐字「matches track_board.all_collidable filter」= 两份筛子靠注释同步; v3 对 ⚪ 已用「独立 lib 函数两处同调」(:45) 解决同类问题, D-3(a) 缺同样一句。
- 修法: 加 T12 (条件, 与 T9 同形):「D-3(a) 时: `lib/constants.py` 新常量 (名 + 单位写死) + 共享谓词函数 + collector/renderer 同调」→ 新 SC「被截止的行不出现在 groups 且 collector 与 renderer 同结论 (对 fixture: 2 组 → 0 组)」。

### Minor

**[R3-m1] 头部计数与两处行号精度** (R2-m1 的 partial 部分)
- type: issue / severity: minor / category: documentation / scope: proposal:98, :45, :66, :140
- evidence: 「11 个 checkbox」实数 12; 「4 个 .py」不含 T3b 要改的 `scripts/phase1_gate.py` / `scripts/release_gate.py` (D-3(a) 时再加 `lib/constants.py`); `track_board.py:176-183` 是 import 块, 渲染器自 dedupe 调用在 `:743-747`; `collision.py:363` 是 `overall_kind = "none"`, track_id 分组循环在 `:367`。
- 修法: 「6 个 .py (+1 条件) / 12 个 checkbox」; 行号改 `:743-747` / `:367`。

**[R3-m2] SC-2 用「经 dedupe → classify()」统领全部子句, 但 advisory 子句的取数点是 dedupe 前的原始行, 与 D3 :45 数据流不一致**
- type: issue / severity: minor / category: testing / scope: proposal:116 (SC-2 首句 + 「advisory 恰 1 条」「owners[] 长度 3」「legacy 行不产生 advisory」三子句)
- evidence: 同容器双 owner 经 dedupe 后 `2→1` 行 (本轮实跑), classify 永远看不到第二个 owner; advisory 只能由 `identity_drift_advisories(原始 tracks)` 产出。按 SC-2 现文写测试会去 `classify()` 返回值里找 advisory —— 那是 R2-M1 的旧路径。
- 修法: SC-2 拆两句: 「`kind` 经 dedupe → classify()」/「advisory 经 `identity_drift_advisories(原始 tracks)`」; 顺手在 SC-1 或 §2.3.1 补零段行的 `identity_key` 字面形 (`/<container>` 还是 `<container>`), 让 SC-4 的「board 回显原串」有确定的键。

**[R3-m3] `advanced-rules.md:578` 在 v2 T7 点名、v3 换成 `:544-572` 后掉出同步范围, 而该行在 v3 语义下失真**
- type: issue / severity: minor / category: documentation / scope: proposal:49, :107, :123, :141 vs `aria/skills/state-scanner/references/rules/advanced-rules.md:578`
- evidence: :578 逐字「判定不依赖"谁" (collision helper 已按 owner+container 归类, 同 owner/container 全相同→none 不触发)」—— v3 下 uuid 容器 owner 不参与同一性, 同 `identity_key` 多 owner → `none`, 「按 owner+container 归类」不再准确; rule 1.54 整段是 `:531-587`, `:544-572` 只覆盖 conditions..context。
- 修法: D4/T7/SC-9 的范围改 `:531-587` 或显式列 `:544-572, :578`。

**[R3-m4] :49「`SKILL.md:149-154` 只引用字段名不引用取值」事实不准; 结论 (不在同步面) 成立但理由要改, 因 Rule #6 行以它为前提**
- type: issue / severity: minor / category: documentation / scope: proposal:49, :96 vs `aria/skills/state-scanner/SKILL.md:149`
- evidence: `SKILL.md:149` 逐字「`tracks_multibranch.collision.kind` 非空 (cross-owner / self_multi_container)」—— 含两个取值字面。它不需要改的真实理由是「取值名不变且该行不描述取值语义」。
- 修法: :49 改为「引用取值名但不描述其语义, 枚举取值不变故不在同步面」。

**[R3-m5] T7「`fetch_gate.py` 真实两段式 `cross_owner` 夹具」是类别错误; SC-9 末句在基线已绿**
- type: issue / severity: minor / category: testing / scope: proposal:50, :107, :123
- evidence: `run_fetch_gate(project_root, *, collision_kind: str = "none", ...)` (`fetch_gate.py:175-181`) 只收 kind 字符串, 没有任何 owner-container 串进入; 既有 `test_fetch_gate.py:58` 已传 `collision_kind="cross_owner"` 并断 `verdict == "advisory"`; message 由 `:254-255` f-string 内插 `({collision_kind})`, 「文案含 `cross_owner`」基线已真。
- 修法: T7 改为「`fetch_gate` 零改动; `test_fetch_gate.py:58` 补 message 含 `cross_owner` 断言」; SC-9 末句标「回归项 (基线绿)」。

**[R3-m6] SC-5 的 grep 断言谓词未枚举 token, 不可机械执行; §2.3.5 第三行用了标准未定义的词「语料」**
- type: issue / severity: minor / category: testing / scope: proposal:40, :119
- evidence: 「无 aria 代码路径」「Aether 私有路径」不是 grep 模式; KM R2 Finding C/D 要靠这条锁。第三行「同一 `identity_key` 在语料中出现 ≥2 个 `<owner>`」的「语料」在 session-handoff.md 无定义, 采用方会把「没有 ⚪」读成「没有漂移」。
- 修法: SC-5 列 token 白/黑名单: §2.3.5 三行反向 grep `\.py|lib/|aria/skills|等价类`; §2.3.9 反向 grep `/home/|Aether|Kairos|DEC-2026|10cglocal`; 第三行改「在本机扫描到的 handoff frontmatter 集合中」。

**[R3-m7] T10 / SC-7 的「pytest 基线 104」数字来源不明, 与 state-scanner 测试规模不符, 疑似从语料统计移植**
- type: issue / severity: minor / category: testing / scope: proposal:110, :121 vs :46
- evidence: `aria/skills/state-scanner/tests/` 68 个文件、`def test_` 共 1492 个; 最相关两文件 `test_collision.py` 16 + `test_handoff_multibranch_collision_dedupe.py` 17 = 33; 全文唯一另一个 104 是 :46「104 行 `active`」= 冻结语料 `status == active` 实数 (本轮 Counter 核对 = 104)。SC-7 的量化锚点因此不可验证。
- 修法: 写「改前全套 `pytest -q` 通过数 = N (B.1 入口实测填入)」或直接删数字, 保留「零回归」。

### 核验通过、不构成 finding

- v3 判定链 (:31-34) 在冻结语料与 9 个合成用例上全部复现, 无残余「推断同一人」输入; 「非空 owner 不计数」对零段 / 两段混写组给出 🟡 与文本一致。
- 既有测试影响面核对: `test_owner_segment_participates_in_grouping_key` (:1039) 用 `alice/box/s1` vs `bob/box/s2` 三段串, 两段化后仍走三段分支且主机名域不折叠 —— 现文改写为两臂是加固不是修红; `test_split_owner_container_variants` (:158-163) 的 `"b/c"` / `"solo"` 现值与 SC-1「先红」括注逐字一致, `""` → `("","","")` 在新规则下不变。
- `test_both_latest_active_still_reports_self_multi_container` (:305) 夹具串与 :60「既有隔离夹具对」一致, 期望改 `cross_owner` 有据 (原绿因 owner 段解析丢)。
- Level 段 / Linked Issue / 符号 / Rule #10 姿态 / 消费方六处全列: 全部通过。

## Verdict

**PASS_WITH_WARNINGS** — 0 Critical / 3 Major / 7 Minor。

R2 本席 6 条: closed 5 / partial 1 / open 0。v3 的核心模型 (纯输入、零推断、advisory 独立函数两处同源) 经实跑成立, R2 两条 Major 的承载体已整段删除且替代用例已进 SC。三条 Major 全部落在决策点 / ship 形态的**文本**上 (D-0(a) 子句违反自设原则、Positive 一句可证伪的缓解声称、D-3(a) 无交付面), 不要求推翻设计; 与 tech-lead R3 同簇, 两席独立到达。

## Vote

**REVISE**。理由: D-0 按 :64 须在 B.1 前裁定, owner 现在拿到的 (a) 带一条与 :29 互斥的实现子句, 在此状态下裁定 = 在半份后果上裁定; :92 的「⚪ 缓解」是会被采用方当真的效果声称, 批准前须删改; D-3(a) 选中即无任务可执行。三处改动量都是几句话 + 一条条件任务 + 一条 SC, 预期 R4 收敛。7 条 minor 可随同轮顺手。

## 轮次记录

- R1 (code-reviewer): 0C/4M/5m, PASS_WITH_WARNINGS / REVISE。
- R2 (code-reviewer): 0C/2M/4m, PASS_WITH_WARNINGS / REVISE —— 等价类无数据通路 + 零 baseline-failing SC。
- R3 (本轮, 镜头: 规格合规复检 + v3 内部一致性): 实读 proposal 143 行全文、R2 本席与聚合、tech-lead R3、`collision.py` :55-215/:295-403、`handoff_multibranch.py` :510-525/:705-716、`track_board.py` :174-185/:405-432/:740-760、`identity.py` 三行、`fetch_gate.py` :175-181/:245-256、`test_fetch_gate.py` :55-66、三个既有测试体、`advanced-rules.md` :531-587、`phase-1-collectors.md:75`、`state-snapshot-schema.md` :1080-1095、`layer-l-integration.md` / `RECOMMENDATION_RULES.md` / `SKILL.md:149-154`、session-handoff.md 六处、phase-a-spec-planning.md :126-137、a1-entry :571/:660/:104、`.aria/state-checks.yaml`; 冻结语料 996 行按 v3 字面规则实跑 (`scratchpad/cr_r3_v3.py`) + 9 合成用例 + D-0(a) 尾段分析 + 语料 status 计数。R2 处置 closed 5 / partial 1 / open 0; 新 0C/3M/7m; PASS_WITH_WARNINGS / REVISE。比较键集合与 R2 无重叠 (承载体已删), 与 R1 无重叠; 非振荡, 逐轮收窄。
